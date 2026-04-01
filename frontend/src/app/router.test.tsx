import { fireEvent, render, screen } from '@testing-library/react'
import { afterEach, describe, expect, it, vi } from 'vitest'
import { createMemoryRouter, RouterProvider } from 'react-router-dom'
import { appRoutes } from './router.tsx'

const sampleSessions = [
  {
    id: 'juniper-lake',
    display_title: 'Lanterns Over Juniper Lake',
    current_stage: 'beats',
    resume_stage: 'beats',
    overall_status: 'in_progress',
    created_at: '2026-04-01T03:00:00Z',
    updated_at: '2026-04-01T05:15:00Z',
    completed_at: null,
    selected_genre: null,
    selected_tone_profile: null,
    progress: {
      total_stages: 10,
      completed_stages: 5,
      in_progress_stages: 1,
      needs_regeneration_stages: 0,
    },
  },
] as const

function buildJsonResponse(status: number, body: unknown) {
  return {
    ok: status >= 200 && status < 300,
    status,
    json: async () => body,
  } as Response
}

function mockBackendOnline({
  createSessionId = 'fresh-session',
  sessions = sampleSessions,
}: {
  createSessionId?: string
  sessions?: ReadonlyArray<Record<string, unknown>>
} = {}) {
  vi.stubGlobal(
    'fetch',
    vi.fn((input: RequestInfo | URL, init?: RequestInit) => {
      const url = typeof input === 'string' ? input : input.toString()

      if (url.endsWith('/api/hello')) {
        return Promise.resolve(
          buildJsonResponse(200, { message: 'Hello from FastAPI!' }),
        )
      }

      if (url.endsWith('/api/v1/sessions') && init?.method === 'POST') {
        return Promise.resolve(buildJsonResponse(201, { id: createSessionId }))
      }

      if (url.includes('/api/v1/sessions?limit=20')) {
        return Promise.resolve(buildJsonResponse(200, sessions))
      }

      throw new Error(`Unhandled request: ${init?.method ?? 'GET'} ${url}`)
    }),
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
      await screen.findByRole('heading', {
        level: 1,
        name: 'Pick up where bedtime left off.',
      }),
    ).toBeInTheDocument()
    expect(
      screen.getByRole('link', { name: 'Resume Lanterns Over Juniper Lake' }),
    ).toHaveAttribute('href', '/sessions/juniper-lake')
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

  it('starts a new session from the home screen and routes into the workspace', async () => {
    mockBackendOnline({ sessions: [] })

    renderRoute('/')

    fireEvent.click(
      await screen.findByRole('button', { name: 'Start a new session' }),
    )

    expect(
      await screen.findByRole('heading', {
        level: 1,
        name: 'Session fresh-session',
      }),
    ).toBeInTheDocument()
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
