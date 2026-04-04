import { useCallback, useEffect, useRef, useState } from 'react'
import { fetchBackendHello } from '../api/system.ts'

export type BackendState = 'loading' | 'online' | 'offline'

export type BackendStatus = {
  checkedAt: string | null
  isRefreshing: boolean
  state: BackendState
  label: string
  detail: string
  message: string
}

const loadingStatus: BackendStatus = {
  checkedAt: null,
  isRefreshing: true,
  state: 'loading',
  label: 'Checking',
  detail: 'Checking whether the local FastAPI backend is reachable.',
  message: 'Checking /api/hello...',
}

export function useBackendStatus() {
  const [status, setStatus] = useState<BackendStatus>(loadingStatus)
  const isMountedRef = useRef(true)
  const refreshStatus = useCallback(async () => {
    setStatus((currentStatus) =>
      currentStatus.state === 'loading'
        ? currentStatus
        : {
            ...currentStatus,
            isRefreshing: true,
          },
    )

    try {
      const payload = await fetchBackendHello()

      if (!isMountedRef.current) {
        return
      }

      setStatus({
        checkedAt: new Date().toISOString(),
        isRefreshing: false,
        state: 'online',
        label: 'Online',
        detail:
          'The app shell is connected to FastAPI through the Vite development proxy.',
        message: payload.message ?? 'Backend responded without a greeting.',
      })
    } catch (error) {
      if (!isMountedRef.current) {
        return
      }

      setStatus({
        checkedAt: new Date().toISOString(),
        isRefreshing: false,
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
  }, [])

  useEffect(() => {
    isMountedRef.current = true
    let intervalId: number | undefined

    async function primeStatus() {
      await refreshStatus()

      if (!isMountedRef.current) {
        return
      }

      intervalId = window.setInterval(() => {
        void refreshStatus()
      }, 30_000)
    }

    void primeStatus()

    return () => {
      isMountedRef.current = false

      if (intervalId != null) {
        window.clearInterval(intervalId)
      }
    }
  }, [refreshStatus])

  return {
    refresh: () => refreshStatus(),
    status,
  }
}
