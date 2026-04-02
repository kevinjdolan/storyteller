import type { PropsWithChildren } from 'react'
import { useEffect, useEffectEvent, useState } from 'react'
import { fetchSessionSnapshot } from '../../api/sessions.ts'
import type { SessionFeedConnectionStatusUpdate } from './live/sessionFeedConnection.ts'
import { createSessionRealtimeClient } from './live/sessionRealtimeClient.ts'
import type {
  SessionRealtimeEvent,
  SessionSubscriptionAck,
} from './live/sessionRealtime.ts'
import { createSessionRuntimeStore } from './sessionRuntimeStore.ts'
import { SessionWorkspaceContext } from './sessionWorkspaceContext.ts'

export function SessionWorkspaceProvider({
  children,
  sessionId,
}: PropsWithChildren<{ sessionId: string }>) {
  const [runtimeStore] = useState(createSessionRuntimeStore)
  const [sessionRealtimeClient] = useState(createSessionRealtimeClient)
  const handleRealtimeEvent = useEffectEvent((event: SessionRealtimeEvent) => {
    runtimeStore.applyRealtimeEvent(event)

    if (
      event.type === 'job.status' &&
      event.payload.job_kind === 'composition' &&
      (event.payload.status === 'completed' ||
        event.payload.status === 'cancelled' ||
        event.payload.status === 'failed')
    ) {
      void fetchSessionSnapshot(sessionId)
        .then((snapshot) => {
          runtimeStore.hydrateSessionSnapshot(snapshot)
        })
        .catch(() => {})
    }
  })
  const handleSubscribed = useEffectEvent((ack: SessionSubscriptionAck) => {
    const snapshot = runtimeStore.getState().sessionSnapshot
    const shouldRefreshSnapshot =
      ack.replay_strategy === 'hydrate' ||
      snapshot?.active_composition_job != null ||
      snapshot?.latest_composition_job?.status === 'paused'

    if (!shouldRefreshSnapshot) {
      return
    }

    void fetchSessionSnapshot(sessionId)
      .then((nextSnapshot) => {
        runtimeStore.hydrateSessionSnapshot(nextSnapshot)
      })
      .catch(() => {})
  })
  const handleConnectionStateChange = useEffectEvent(
    (update: SessionFeedConnectionStatusUpdate) => {
      runtimeStore.syncConnectionStatus(update)
    },
  )

  useEffect(() => {
    runtimeStore.reset()

    const connection = sessionRealtimeClient.connect({
      sessionId,
      getLastSequenceNumber: () =>
        runtimeStore.getState().eventStream.lastSequenceNumber,
      onEvent: handleRealtimeEvent,
      onSubscribed: handleSubscribed,
      onConnectionStateChange: handleConnectionStateChange,
    })

    return () => {
      connection.disconnect()
    }
  }, [runtimeStore, sessionId, sessionRealtimeClient])

  return (
    <SessionWorkspaceContext.Provider
      value={{
        sessionId,
        runtimeStore,
      }}
    >
      {children}
    </SessionWorkspaceContext.Provider>
  )
}
