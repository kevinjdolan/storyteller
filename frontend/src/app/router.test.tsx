import { render, screen } from '@testing-library/react'
import { afterEach, describe, expect, it, vi } from 'vitest'
import { createMemoryRouter, RouterProvider } from 'react-router-dom'
import { appRoutes } from './router.tsx'

function mockBackendOnline() {
  vi.stubGlobal(
    'fetch',
    vi.fn().mockResolvedValue({
      ok: true,
      json: async () => ({ message: 'Hello from FastAPI!' }),
    } as Response),
  )
}

function renderRoute(initialEntry: string) {
  const router = createMemoryRouter(appRoutes, {
    initialEntries: [initialEntry],
  })

  return render(<RouterProvider router={router} />)
}

describe('app router', () => {
  afterEach(() => {
    vi.restoreAllMocks()
    vi.unstubAllGlobals()
  })

  it('renders the home screen inside the shared shell', async () => {
    mockBackendOnline()

    renderRoute('/')

    expect(screen.getByRole('link', { name: 'Sessions' })).toHaveAttribute(
      'href',
      '/',
    )
    expect(
      screen.getByRole('heading', {
        level: 2,
        name: 'Past sessions come first',
      }),
    ).toBeInTheDocument()
    expect(await screen.findByText('Hello from FastAPI!')).toBeInTheDocument()
  })

  it('renders the session workspace route with a session id', async () => {
    mockBackendOnline()

    renderRoute('/sessions/moonlit-harbor')

    expect(
      screen.getByRole('heading', { level: 1, name: 'Session moonlit-harbor' }),
    ).toBeInTheDocument()
    expect(screen.getByTestId('workspace-route')).toBeInTheDocument()
    expect(screen.getByText('/sessions/moonlit-harbor')).toBeInTheDocument()
  })

  it('renders the not-found fallback for unknown routes', async () => {
    mockBackendOnline()

    renderRoute('/does-not-exist')

    expect(
      screen.getByRole('heading', { level: 1, name: 'Page not found' }),
    ).toBeInTheDocument()
    expect(screen.getByText('/does-not-exist')).toBeInTheDocument()
  })
})
