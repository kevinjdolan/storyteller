import { render, screen } from '@testing-library/react'
import { afterEach, describe, expect, it, vi } from 'vitest'
import { HomeRoute } from './HomeRoute.tsx'

describe('HomeRoute', () => {
  afterEach(() => {
    vi.restoreAllMocks()
    vi.unstubAllGlobals()
  })

  it('renders the branded scaffold and reports a healthy backend', async () => {
    const fetchMock = vi.fn().mockResolvedValue({
      ok: true,
      json: async () => ({ message: 'Hello from FastAPI!' }),
    } as Response)

    vi.stubGlobal('fetch', fetchMock)

    render(<HomeRoute />)

    expect(
      screen.getByRole('heading', { level: 1, name: 'Storyteller' }),
    ).toBeInTheDocument()
    expect(screen.getByText('Past sessions come first')).toBeInTheDocument()
    expect(await screen.findByText('Hello from FastAPI!')).toBeInTheDocument()
    expect(screen.getByTestId('backend-state')).toHaveTextContent('Online')
  })

  it('falls back to frontend-only mode when the backend is unavailable', async () => {
    const fetchMock = vi.fn().mockRejectedValue(new Error('offline'))

    vi.stubGlobal('fetch', fetchMock)

    render(<HomeRoute />)

    expect(
      await screen.findByText('Running in frontend-only mode.'),
    ).toBeInTheDocument()
    expect(screen.getByTestId('backend-state')).toHaveTextContent('Offline')
  })
})
