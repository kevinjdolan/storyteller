import { generatePath } from 'react-router-dom'

export const routePaths = {
  home: '/',
  sessionWorkspace: '/sessions/:sessionId',
  notFound: '*',
} as const

export function buildSessionWorkspacePath(sessionId: string) {
  return generatePath(routePaths.sessionWorkspace, { sessionId })
}
