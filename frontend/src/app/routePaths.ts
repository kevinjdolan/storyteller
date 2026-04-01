import { generatePath } from 'react-router-dom'

export const routePaths = {
  home: '/',
  sessionWorkspace: '/sessions/:sessionId',
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
