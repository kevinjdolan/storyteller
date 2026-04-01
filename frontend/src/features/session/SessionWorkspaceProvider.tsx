import type { PropsWithChildren } from 'react'
import { useState } from 'react'
import { createSessionRuntimeStore } from './sessionRuntimeStore.ts'
import { SessionWorkspaceContext } from './sessionWorkspaceContext.ts'

export function SessionWorkspaceProvider({
  children,
  sessionId,
}: PropsWithChildren<{ sessionId: string }>) {
  const [runtimeStore] = useState(createSessionRuntimeStore)

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
