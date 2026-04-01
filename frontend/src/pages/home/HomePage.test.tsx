import { fireEvent, render, screen, waitFor } from '@testing-library/react'
import { MemoryRouter } from 'react-router-dom'
import { afterEach, describe, expect, it, vi } from 'vitest'
import { HomePage } from './HomePage.tsx'

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
    current_stage: 'finalize',
    resume_stage: 'finalize',
    overall_status: 'completed',
    created_at: '2026-03-29T03:00:00Z',
    updated_at: '2026-03-31T05:15:00Z',
    completed_at: '2026-03-31T05:15:00Z',
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

function mockSessionsApi({
  postSessionId = 'new-session',
  sessions = sampleSessions,
  status = 200,
}: {
  postSessionId?: string
  sessions?: ReadonlyArray<Record<string, unknown>>
  status?: number
} = {}) {
  vi.stubGlobal(
    'fetch',
    vi.fn((input: RequestInfo | URL, init?: RequestInit) => {
      const url = typeof input === 'string' ? input : input.toString()

      if (url.endsWith('/api/v1/sessions') && init?.method === 'POST') {
        return Promise.resolve(buildJsonResponse(201, { id: postSessionId }))
      }

      if (url.includes('/api/v1/sessions?limit=20')) {
        return Promise.resolve(buildJsonResponse(status, sessions))
      }

      throw new Error(`Unhandled request: ${init?.method ?? 'GET'} ${url}`)
    }),
  )
}

describe('HomePage', () => {
  afterEach(() => {
    vi.restoreAllMocks()
    vi.unstubAllGlobals()
  })

  it('renders active and completed sessions from the backend', async () => {
    mockSessionsApi()

    render(
      <MemoryRouter>
        <HomePage />
      </MemoryRouter>,
    )

    expect(
      await screen.findByRole('heading', {
        level: 3,
        name: 'Continue building',
      }),
    ).toBeInTheDocument()
    expect(
      screen.getByRole('heading', { level: 3, name: 'Finished stories' }),
    ).toBeInTheDocument()
    expect(
      screen.getByRole('link', { name: 'Resume Lanterns Over Juniper Lake' }),
    ).toHaveAttribute('href', '/sessions/juniper-lake')
    expect(
      screen.getByRole('link', {
        name: 'Review The Moss Door in Maple Hollow',
      }),
    ).toHaveAttribute('href', '/sessions/maple-hollow')
    expect(screen.getByText('Quiet Mystery')).toBeInTheDocument()
    expect(screen.getByText('5 of 10 stages complete')).toBeInTheDocument()
  })

  it('shows an empty state when there are no stored sessions', async () => {
    mockSessionsApi({ sessions: [] })

    render(
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
    const fetchMock = vi
      .fn()
      .mockResolvedValueOnce(buildJsonResponse(500, { detail: 'boom' }))
      .mockResolvedValueOnce(buildJsonResponse(200, sampleSessions))

    vi.stubGlobal('fetch', fetchMock)

    render(
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
        screen.getByRole('heading', { level: 3, name: 'Continue building' }),
      ).toBeInTheDocument()
    })
  })
})
