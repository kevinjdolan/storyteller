import { generatePath } from 'react-router-dom'

export const routePaths = {
  home: '/',
  sessionWorkspace: '/sessions/:sessionId',
  sessionDebugInspector: '/sessions/:sessionId/debug',
  notFound: '*',
} as const

export function buildSessionWorkspacePath(
  sessionId: string,
  options: {
    stage?: string | null
  } = {},
) {
  const path = generatePath(routePaths.sessionWorkspace, { sessionId })

  if (options.stage == null || options.stage === '') {
    return path
  }

  const searchParams = new URLSearchParams({
    stage: options.stage,
  })

  return `${path}?${searchParams.toString()}`
}

export function buildSessionDebugInspectorPath(sessionId: string) {
  return generatePath(routePaths.sessionDebugInspector, { sessionId })
}
