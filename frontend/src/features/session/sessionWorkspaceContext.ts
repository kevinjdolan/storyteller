import { createContext, useContext, useSyncExternalStore } from 'react'
import {
  type SessionRuntimeState,
  type SessionRuntimeStore,
} from './sessionRuntimeStore.ts'
import { useSessionSnapshotQuery } from './sessionQueries.ts'

export type SessionWorkspaceContextValue = {
  sessionId: string
  runtimeStore: SessionRuntimeStore
}

export const SessionWorkspaceContext =
  createContext<SessionWorkspaceContextValue | null>(null)

function useSessionWorkspaceContext() {
  const context = useContext(SessionWorkspaceContext)

  if (context === null) {
    throw new Error(
      'Session workspace hooks must be used inside SessionWorkspaceProvider.',
    )
  }

  return context
}

export function useCurrentSessionSnapshotQuery() {
  const { sessionId } = useSessionWorkspaceContext()

  return useSessionSnapshotQuery(sessionId)
}

export function useSessionRuntimeSelector<T>(
  selector: (state: SessionRuntimeState) => T,
) {
  const { runtimeStore } = useSessionWorkspaceContext()

  return useSyncExternalStore(
    runtimeStore.subscribe,
    () => selector(runtimeStore.getState()),
    () => selector(runtimeStore.getState()),
  )
}

export function useSessionPendingActions() {
  return useSessionRuntimeSelector((state) => state.pendingActions)
}

export function useSessionEventStream() {
  return useSessionRuntimeSelector((state) => state.eventStream)
}

export function useSessionRuntimeActions() {
  const { runtimeStore } = useSessionWorkspaceContext()

  return runtimeStore
}
