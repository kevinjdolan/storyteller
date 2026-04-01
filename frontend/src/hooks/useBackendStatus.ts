import { useEffect, useState } from 'react'
import { fetchBackendHello } from '../api/system.ts'

export type BackendState = 'loading' | 'online' | 'offline'

export type BackendStatus = {
  state: BackendState
  label: string
  detail: string
  message: string
}

const loadingStatus: BackendStatus = {
  state: 'loading',
  label: 'Checking',
  detail: 'Checking whether the local FastAPI backend is reachable.',
  message: 'Checking /api/hello...',
}

export function useBackendStatus() {
  const [status, setStatus] = useState<BackendStatus>(loadingStatus)

  useEffect(() => {
    let isCurrent = true

    async function loadBackendStatus() {
      try {
        const payload = await fetchBackendHello()

        if (!isCurrent) {
          return
        }

        setStatus({
          state: 'online',
          label: 'Online',
          detail:
            'The app shell is connected to FastAPI through the Vite development proxy.',
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
            'The shell still renders without FastAPI so frontend work can continue in isolation.',
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
