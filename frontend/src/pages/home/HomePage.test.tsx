import { fireEvent, screen, waitFor } from '@testing-library/react'
import { MemoryRouter } from 'react-router-dom'
import { afterEach, describe, expect, it, vi } from 'vitest'
import { renderWithAppProviders } from '../../test/renderWithAppProviders.tsx'
import { HomePage } from './HomePage.tsx'

const genreCatalog = [
  {
    id: 'genre-1',
    slug: 'quiet-mystery',
    label: 'Quiet Mystery',
    description: 'Soft mysteries for bedtime.',
    bedtime_safety_notes: 'Keep every reveal reassuring.',
    arc_notes: {},
    sort_order: 1,
  },
  {
    id: 'genre-2',
    slug: 'woodland-adventure',
    label: 'Woodland Adventure',
    description: 'Cozy adventure in the woods.',
    bedtime_safety_notes: 'Let the ending land at home.',
    arc_notes: {},
    sort_order: 2,
  },
] as const

const sampleSessions = [
  {
    id: 'juniper-lake',
    display_title: 'Lanterns Over Juniper Lake',
    working_title: 'Lanterns Over Juniper Lake',
    library_summary: {
      display_kind: 'draft_session',
      title_source: 'working_title',
      runtime_seconds: null,
      runtime_source: null,
      artifact_readiness: {
        story_text: 'missing',
        story_docx: 'missing',
        final_audio: 'missing',
        ready_count: 0,
        total_count: 3,
      },
    },
    current_stage: 'beats',
    resume_stage: 'beats',
    overall_status: 'in_progress',
    created_at: '2026-04-10T03:00:00Z',
    updated_at: '2026-04-10T12:15:00Z',
    completed_at: null,
    selected_genre: {
      id: 'genre-1',
      slug: 'quiet-mystery',
      label: 'Quiet Mystery',
    },
    selected_tone_profile: {
      id: 'tone-1',
      slug: 'gentle-glow',
      label: 'Gentle Glow',
    },
    progress: {
      total_stages: 10,
      completed_stages: 5,
      in_progress_stages: 1,
      needs_regeneration_stages: 0,
    },
  },
  {
    id: 'maple-hollow',
    display_title: 'The Moss Door in Maple Hollow',
    working_title: null,
    library_summary: {
      display_kind: 'polished_story',
      title_source: 'pitch_title',
      runtime_seconds: 734,
      runtime_source: 'final_audio',
      artifact_readiness: {
        story_text: 'ready',
        story_docx: 'ready',
        final_audio: 'ready',
        ready_count: 3,
        total_count: 3,
      },
    },
    current_stage: 'finalize',
    resume_stage: 'finalize',
    overall_status: 'completed',
    created_at: '2026-03-15T03:00:00Z',
    updated_at: '2026-03-20T12:15:00Z',
    completed_at: '2026-03-20T12:15:00Z',
    selected_genre: {
      id: 'genre-2',
      slug: 'woodland-adventure',
      label: 'Woodland Adventure',
    },
    selected_tone_profile: {
      id: 'tone-2',
      slug: 'hushed-wonder',
      label: 'Hushed Wonder',
    },
    progress: {
      total_stages: 10,
      completed_stages: 10,
      in_progress_stages: 0,
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

function filterSessionsByUrl(
  url: URL,
  sessions: ReadonlyArray<Record<string, unknown>>,
) {
  const query = url.searchParams.get('query')?.toLowerCase().trim() ?? ''
  const status = url.searchParams.get('status')
  const genreSlug = url.searchParams.get('genre_slug')

  return sessions.filter((session) => {
    const sessionTitle = String(session.display_title ?? '').toLowerCase()
    const sessionStatus = String(session.overall_status ?? '')
    const sessionGenreSlug = String(
      (session.selected_genre as { slug?: string } | null)?.slug ?? '',
    )

    const matchesQuery =
      query.length === 0 || sessionTitle.includes(query.toLowerCase())
    const matchesStatus =
      status == null
        ? true
        : status === 'active'
          ? sessionStatus !== 'completed'
          : sessionStatus === status
    const matchesGenre =
      genreSlug == null || genreSlug.length === 0
        ? true
        : sessionGenreSlug === genreSlug

    return matchesQuery && matchesStatus && matchesGenre
  })
}

function mockSessionsApi({
  postSessionId = 'new-session',
  sessions = sampleSessions,
  sessionStatus = 200,
}: {
  postSessionId?: string
  sessions?: ReadonlyArray<Record<string, unknown>>
  sessionStatus?: number
} = {}) {
  const fetchMock = vi.fn((input: RequestInfo | URL, init?: RequestInit) => {
    const rawUrl = typeof input === 'string' ? input : input.toString()
    const url = new URL(rawUrl, 'http://localhost')

    if (url.pathname === '/api/v1/catalog/genres') {
      return Promise.resolve(buildJsonResponse(200, genreCatalog))
    }

    if (url.pathname === '/api/v1/sessions' && init?.method === 'POST') {
      return Promise.resolve(buildJsonResponse(201, { id: postSessionId }))
    }

    if (url.pathname === '/api/v1/sessions') {
      return Promise.resolve(
        buildJsonResponse(sessionStatus, filterSessionsByUrl(url, sessions)),
      )
    }

    throw new Error(`Unhandled request: ${init?.method ?? 'GET'} ${rawUrl}`)
  })

  vi.stubGlobal('fetch', fetchMock)
  return fetchMock
}

describe('HomePage', () => {
  afterEach(() => {
    vi.restoreAllMocks()
    vi.unstubAllGlobals()
  })

  it('renders the searchable library with month groupings and polished-story metadata', async () => {
    mockSessionsApi()

    renderWithAppProviders(
      <MemoryRouter>
        <HomePage />
      </MemoryRouter>,
    )

    expect(
      await screen.findByText('The Moss Door in Maple Hollow'),
    ).toBeInTheDocument()
    expect(screen.getByLabelText('Search sessions')).toBeInTheDocument()
    expect(
      screen.getByRole('heading', { level: 3, name: 'April 2026' }),
    ).toBeInTheDocument()
    expect(
      screen.getByRole('heading', { level: 3, name: 'March 2026' }),
    ).toBeInTheDocument()
    expect(
      screen.getByRole('link', { name: 'Resume Lanterns Over Juniper Lake' }),
    ).toHaveAttribute('href', '/sessions/juniper-lake')
    expect(
      screen.getByRole('link', {
        name: 'Open story The Moss Door in Maple Hollow',
      }),
    ).toHaveAttribute('href', '/sessions/maple-hollow')
    expect(screen.getByText('Word doc ready')).toBeInTheDocument()
    expect(screen.getByText('Narration ready')).toBeInTheDocument()
    expect(screen.getByText('12m 14s')).toBeInTheDocument()
  })

  it('sends title, status, and genre filters back to the backend query', async () => {
    const fetchMock = mockSessionsApi()

    renderWithAppProviders(
      <MemoryRouter>
        <HomePage />
      </MemoryRouter>,
    )

    expect(
      await screen.findByText('Lanterns Over Juniper Lake'),
    ).toBeInTheDocument()

    fireEvent.change(screen.getByLabelText('Search sessions'), {
      target: { value: 'Moss' },
    })
    fireEvent.change(screen.getByLabelText('Status'), {
      target: { value: 'completed' },
    })
    fireEvent.change(screen.getByLabelText('Genre'), {
      target: { value: 'woodland-adventure' },
    })

    await waitFor(() => {
      expect(
        screen.getByText('The Moss Door in Maple Hollow'),
      ).toBeInTheDocument()
      expect(
        screen.queryByText('Lanterns Over Juniper Lake'),
      ).not.toBeInTheDocument()
    })

    await waitFor(() => {
      const lastSessionRequest = [...fetchMock.mock.calls]
        .map(([input]) =>
          new URL(
            typeof input === 'string' ? input : input.toString(),
            'http://localhost',
          ),
        )
        .reverse()
        .find((url) => url.pathname === '/api/v1/sessions')

      expect(lastSessionRequest?.searchParams.get('query')).toBe('Moss')
      expect(lastSessionRequest?.searchParams.get('status')).toBe('completed')
      expect(lastSessionRequest?.searchParams.get('genre_slug')).toBe(
        'woodland-adventure',
      )
    })
  })

  it('shows an empty filter result state and clears filters back to the full library', async () => {
    mockSessionsApi()

    renderWithAppProviders(
      <MemoryRouter>
        <HomePage />
      </MemoryRouter>,
    )

    expect(
      await screen.findByText('Lanterns Over Juniper Lake'),
    ).toBeInTheDocument()

    fireEvent.change(screen.getByLabelText('Search sessions'), {
      target: { value: 'Nope' },
    })

    expect(
      await screen.findByText('No sessions match those filters.'),
    ).toBeInTheDocument()

    fireEvent.click(screen.getByRole('button', { name: 'Clear filters' }))

    await waitFor(() => {
      expect(
        screen.getByText('Lanterns Over Juniper Lake'),
      ).toBeInTheDocument()
    })
  })

  it('shows an empty state when there are no stored sessions', async () => {
    mockSessionsApi({ sessions: [] })

    renderWithAppProviders(
      <MemoryRouter>
        <HomePage />
      </MemoryRouter>,
    )

    expect(await screen.findByText('No sessions yet.')).toBeInTheDocument()
    expect(
      screen.getByText(
        'Start a fresh bedtime story to open the workspace and begin the first session.',
      ),
    ).toBeInTheDocument()
  })

  it('shows an error state and retries the list request', async () => {
    let sessionGetCount = 0
    const fetchMock = vi.fn((input: RequestInfo | URL, init?: RequestInit) => {
        const rawUrl = typeof input === 'string' ? input : input.toString()
        const url = new URL(rawUrl, 'http://localhost')

        if (url.pathname === '/api/v1/catalog/genres') {
          return Promise.resolve(buildJsonResponse(200, genreCatalog))
        }

        if (url.pathname === '/api/v1/sessions' && init?.method === 'POST') {
          return Promise.resolve(buildJsonResponse(201, { id: 'new-session' }))
        }

        if (url.pathname === '/api/v1/sessions' && init?.method !== 'POST') {
          if (sessionGetCount === 0) {
            sessionGetCount += 1
            return Promise.resolve(buildJsonResponse(500, { detail: 'boom' }))
          }

          return Promise.resolve(buildJsonResponse(200, sampleSessions))
        }

        throw new Error(`Unhandled request: ${init?.method ?? 'GET'} ${rawUrl}`)
      })

    vi.stubGlobal('fetch', fetchMock)

    renderWithAppProviders(
      <MemoryRouter>
        <HomePage />
      </MemoryRouter>,
    )

    expect(
      await screen.findByText('Could not load past sessions.'),
    ).toBeInTheDocument()

    fireEvent.click(screen.getByRole('button', { name: 'Retry' }))

    await waitFor(() => {
      expect(
        screen.getByRole('heading', { level: 2, name: 'Session library' }),
      ).toBeInTheDocument()
    })
  })
})
