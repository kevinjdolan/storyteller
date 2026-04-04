import { fireEvent, screen } from '@testing-library/react'
import { afterEach, describe, expect, it, vi } from 'vitest'
import { createMemoryRouter, RouterProvider } from 'react-router-dom'
import { renderWithAppProviders } from '../test/renderWithAppProviders.tsx'
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

const sampleSessionSnapshot = {
  id: 'moonlit-harbor',
  display_title: 'Lanterns Over Juniper Lake',
  working_title: 'Lanterns Over Juniper Lake',
  current_stage: 'beats',
  resume_stage: 'beats',
  furthest_completed_stage: 'characters',
  overall_status: 'in_progress',
  created_at: '2026-04-01T03:00:00Z',
  updated_at: '2026-04-01T05:15:00Z',
  completed_at: null,
  selected_genre: {
    id: 'genre-1',
    slug: 'quest-fantasy',
    label: 'Quest Fantasy',
  },
  selected_tone_profile: {
    id: 'tone-1',
    slug: 'hushed-wonder',
    label: 'Hushed Wonder',
  },
  progress: {
    total_stages: 10,
    completed_stages: 5,
    in_progress_stages: 1,
    needs_regeneration_stages: 0,
  },
  stage_states: [
    {
      stage: 'genre',
      label: 'Genre',
      description:
        'Choose the overall bedtime-story lane before the rest of the plan is shaped.',
      status: 'completed',
      detail: 'Accepted quest fantasy.',
    },
    {
      stage: 'beats',
      label: 'Beat sheet',
      description:
        'Store the accepted Save-the-Cat beat sheet for the session.',
      status: 'in_progress',
      detail: 'Midpoint needs one more bedtime-soft pass.',
    },
  ],
  story_brief: {
    id: 'brief-1',
    revision_number: 1,
    raw_brief: 'A lantern-filled harbor bedtime quest.',
    normalized_summary: 'A child follows lanterns across the harbor.',
  },
  selected_pitch: {
    id: 'pitch-1',
    generation_key: 'batch-1',
    pitch_index: 0,
    title: 'Lanterns Over Juniper Lake',
    logline:
      'A child and an otter guardian follow drifting lanterns across the harbor to return each light before bedtime.',
  },
  selected_character_sheet: null,
  selected_story_setup: null,
  active_composition_job: null,
  active_audio_job: null,
  latest_story_asset: null,
  latest_audio_asset: null,
} as const

const sampleSessionHydration = {
  snapshot: sampleSessionSnapshot,
  recent_history: {
    session_id: sampleSessionSnapshot.id,
    latest_sequence_number: 1,
    events: [],
  },
  hydration: {
    strategy: 'materialized_only',
    materialized_through_sequence_number: 1,
    replay_from_sequence_number: null,
    replayed_event_count: 0,
    latest_sequence_number: 1,
    history_event_count: 0,
    history_window_truncated: false,
  },
} as const

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
  sessionHydration = sampleSessionHydration,
}: {
  createSessionId?: string
  sessions?: ReadonlyArray<Record<string, unknown>>
  sessionHydration?: Record<string, unknown>
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

      if (url.includes('/api/v1/sessions/moonlit-harbor/hydrate')) {
        return Promise.resolve(buildJsonResponse(200, sessionHydration))
      }

      if (url.includes('/api/v1/sessions/fresh-session/hydrate')) {
        return Promise.resolve(
          buildJsonResponse(200, {
            ...sessionHydration,
            snapshot: {
              ...(sessionHydration.snapshot as Record<string, unknown>),
              id: 'fresh-session',
              display_title: 'Fresh Session',
              working_title: 'Fresh Session',
            },
            recent_history: {
              ...(sessionHydration.recent_history as Record<string, unknown>),
              session_id: 'fresh-session',
            },
          }),
        )
      }

      throw new Error(`Unhandled request: ${init?.method ?? 'GET'} ${url}`)
    }),
  )
}

function renderRoute(initialEntry: string) {
  const router = createMemoryRouter(appRoutes, {
    initialEntries: [initialEntry],
  })

  return renderWithAppProviders(<RouterProvider router={router} />)
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
      await screen.findByRole('link', {
        name: 'Resume Lanterns Over Juniper Lake',
      }),
    ).toHaveAttribute('href', '/sessions/juniper-lake')
    expect(await screen.findByText('Hello from FastAPI!')).toBeInTheDocument()
  })

  it('renders the session workspace route with a session id', async () => {
    mockBackendOnline()

    renderRoute('/sessions/moonlit-harbor')

    expect(
      await screen.findByRole('heading', {
        level: 1,
        name: 'Lanterns Over Juniper Lake',
      }),
    ).toBeInTheDocument()
    expect(screen.getByTestId('workspace-route')).toBeInTheDocument()
    expect(screen.getByRole('link', { name: 'Return home' })).toHaveAttribute(
      'href',
      '/',
    )
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
        name: 'Fresh Session',
      }),
    ).toBeInTheDocument()
  })

  it('shows an inline banner and toast when creating a session fails', async () => {
    vi.stubGlobal(
      'fetch',
      vi.fn((input: RequestInfo | URL, init?: RequestInit) => {
        const url = typeof input === 'string' ? input : input.toString()

        if (url.endsWith('/api/hello')) {
          return Promise.resolve(
            buildJsonResponse(200, { message: 'Hello from FastAPI!' }),
          )
        }

        if (url.includes('/api/v1/sessions?limit=20')) {
          return Promise.resolve(buildJsonResponse(200, []))
        }

        if (url.endsWith('/api/v1/sessions') && init?.method === 'POST') {
          return Promise.resolve(buildJsonResponse(500, { detail: 'boom' }))
        }

        throw new Error(`Unhandled request: ${init?.method ?? 'GET'} ${url}`)
      }),
    )

    renderRoute('/')

    fireEvent.click(
      await screen.findByRole('button', { name: 'Start a new session' }),
    )

    expect(
      await screen.findByText(
        'Could not start a new session. Please try again.',
      ),
    ).toBeInTheDocument()
    expect(
      screen.getByText(
        'The home screen could not open a new workspace. Try the request again.',
      ),
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
