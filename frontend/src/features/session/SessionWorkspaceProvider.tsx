import type { PropsWithChildren } from 'react'
import { useEffect, useEffectEvent, useState } from 'react'
import type { SessionFeedConnectionStatusUpdate } from './live/sessionFeedConnection.ts'
import { createSessionRealtimeClient } from './live/sessionRealtimeClient.ts'
import type { SessionRealtimeEvent } from './live/sessionRealtime.ts'
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
