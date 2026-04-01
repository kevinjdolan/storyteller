import { render, screen } from '@testing-library/react'
import { MemoryRouter } from 'react-router-dom'
import { afterEach, describe, expect, it, vi } from 'vitest'
import { SessionWorkspaceErrorBoundary } from './SessionWorkspaceErrorBoundary.tsx'

function CrashyChild() {
  throw new Error('The stage scaffold crashed during render.')

  return null
}

describe('SessionWorkspaceErrorBoundary', () => {
  afterEach(() => {
    vi.restoreAllMocks()
  })

  it('shows a recovery surface when the workspace throws during render', () => {
    vi.spyOn(console, 'error').mockImplementation(() => undefined)

    render(
      <MemoryRouter>
        <SessionWorkspaceErrorBoundary sessionId="session-123">
          <CrashyChild />
        </SessionWorkspaceErrorBoundary>
      </MemoryRouter>,
    )

    expect(
      screen.getByRole('heading', { level: 1, name: 'Workspace crashed' }),
    ).toBeInTheDocument()
    expect(
      screen.getByText('The stage scaffold crashed during render.'),
    ).toBeInTheDocument()
    expect(
      screen.getByRole('button', { name: 'Retry workspace' }),
    ).toBeInTheDocument()
    expect(screen.getByRole('link', { name: 'Return home' })).toHaveAttribute(
      'href',
      '/',
    )
  })
})
