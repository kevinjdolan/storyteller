import { useEffect, useState } from 'react'
import { resolveApiUrl } from '../../shared/api.ts'

type BackendState = 'loading' | 'online' | 'offline'

type BackendStatus = {
  state: BackendState
  label: string
  detail: string
  message: string
}

const loadingStatus: BackendStatus = {
  state: 'loading',
  label: 'Checking',
  detail: 'Checking whether the local FastAPI backend is reachable.',
  message: 'Checking /api/hello…',
}

export function useBackendStatus() {
  const [status, setStatus] = useState<BackendStatus>(loadingStatus)

  useEffect(() => {
    let isCurrent = true

    async function loadBackendStatus() {
      try {
        const response = await fetch(resolveApiUrl('/api/hello'))

        if (!response.ok) {
          throw new Error(`Unexpected status code: ${response.status}`)
        }

        const payload = (await response.json()) as { message?: string }

        if (!isCurrent) {
          return
        }

        setStatus({
          state: 'online',
          label: 'Online',
          detail:
            'The frontend is talking to the backend through the Vite dev proxy.',
          message: payload.message ?? 'Backend responded without a greeting.',
        })
      } catch (error) {
        if (!isCurrent) {
          return
        }

        setStatus({
          state: 'offline',
          label: 'Offline',
          detail:
            'The app still renders without FastAPI, so npm run dev works in isolation.',
          message: 'Running in frontend-only mode.',
        })

        if (import.meta.env.DEV && import.meta.env.MODE !== 'test') {
          console.warn('Backend status check failed.', error)
        }
      }
    }

    void loadBackendStatus()

    return () => {
      isCurrent = false
    }
  }, [])

  return status
}
