import { render, screen } from '@testing-library/react'
import { MemoryRouter, Route, Routes } from 'react-router-dom'
import { afterEach, describe, expect, it, vi } from 'vitest'
import { SessionWorkspacePage } from './SessionWorkspacePage.tsx'

const sampleSnapshot = {
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
      stage: 'tone',
      label: 'Tone',
      description:
        'Choose the emotional texture and bedtime-safety posture for the session.',
      status: 'completed',
      detail: 'Selected a soft adventurous tone.',
    },
    {
      stage: 'brief',
      label: 'Story brief',
      description:
        "Capture the user's free-form idea and any normalized planning summary derived from it.",
      status: 'completed',
      detail: 'Accepted normalized brief.',
    },
    {
      stage: 'pitches',
      label: 'Pitches',
      description:
        'Generate, compare, refine, and accept candidate story directions.',
      status: 'completed',
      detail: 'Accepted the harbor lantern pitch.',
    },
    {
      stage: 'characters',
      label: 'Characters',
      description:
        'Define the accepted character sheet that later planning and writing will reference.',
      status: 'completed',
      detail: 'Locked the character sheet.',
    },
    {
      stage: 'beats',
      label: 'Beat sheet',
      description:
        'Store the accepted Save-the-Cat beat sheet for the session.',
      status: 'in_progress',
      detail: 'Midpoint needs one more bedtime-soft pass.',
    },
    {
      stage: 'story_setup',
      label: 'Story setup',
      description:
        'Store soft planning targets such as word count, runtime, and chapter structure.',
      status: 'draft',
      detail: null,
    },
    {
      stage: 'composition',
      label: 'Composition',
      description:
        'Write the story durably in segments, with room for interruption and targeted rewrites.',
      status: 'draft',
      detail: null,
    },
    {
      stage: 'audio',
      label: 'Audio',
      description:
        'Configure narration settings and generate resumable audio artifacts.',
      status: 'draft',
      detail: null,
    },
    {
      stage: 'finalize',
      label: 'Finalize',
      description: 'Read, listen, review final assets, and download exports.',
      status: 'draft',
      detail: null,
    },
  ],
  story_brief: {
    id: 'brief-1',
    revision_number: 1,
    raw_brief:
      'A child follows floating lanterns across a harbor and helps a shy otter guardian bring them home.',
    normalized_summary:
      'A harbor bedtime quest where floating lanterns guide a child and an otter toward a calm reunion.',
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
  selected_story_setup: {
    id: 'setup-1',
    revision_number: 1,
    target_word_count: 1500,
    target_runtime_minutes: 12,
    chapter_count: 4,
    chapter_style: 'short',
  },
  active_composition_job: null,
  active_audio_job: null,
  latest_story_asset: null,
  latest_audio_asset: null,
} as const

function buildJsonResponse(status: number, body: unknown) {
  return {
    ok: status >= 200 && status < 300,
    status,
    json: async () => body,
  } as Response
}

function mockWorkspaceApi(status = 200, body: unknown = sampleSnapshot) {
  vi.stubGlobal(
    'fetch',
    vi.fn((input: RequestInfo | URL) => {
      const url = typeof input === 'string' ? input : input.toString()

      if (url.includes('/api/v1/sessions/moonlit-harbor')) {
        return Promise.resolve(buildJsonResponse(status, body))
      }

      throw new Error(`Unhandled request: GET ${url}`)
    }),
  )
}

function renderWorkspaceRoute() {
  return render(
    <MemoryRouter initialEntries={['/sessions/moonlit-harbor']}>
      <Routes>
        <Route path="/sessions/:sessionId" element={<SessionWorkspacePage />} />
      </Routes>
    </MemoryRouter>,
  )
}

describe('SessionWorkspacePage', () => {
  afterEach(() => {
    vi.restoreAllMocks()
    vi.unstubAllGlobals()
  })

  it('renders the session snapshot inside the workspace shell', async () => {
    mockWorkspaceApi()

    renderWorkspaceRoute()

    expect(
      await screen.findByRole('heading', {
        level: 1,
        name: 'Lanterns Over Juniper Lake',
      }),
    ).toBeInTheDocument()
    expect(screen.getByTestId('workspace-route')).toBeInTheDocument()
    expect(
      screen.getByText('Selected genre: Quest Fantasy'),
    ).toBeInTheDocument()
    expect(screen.getByText('5 of 10 stages complete')).toBeInTheDocument()
    expect(screen.getByRole('link', { name: 'Return home' })).toHaveAttribute(
      'href',
      '/',
    )
    expect(
      screen.getByText('Midpoint needs one more bedtime-soft pass.'),
    ).toBeInTheDocument()
  })

  it('shows a missing-session state when the snapshot request returns 404', async () => {
    mockWorkspaceApi(404, { detail: 'missing' })

    renderWorkspaceRoute()

    expect(
      await screen.findByRole('heading', {
        level: 1,
        name: 'Workspace unavailable',
      }),
    ).toBeInTheDocument()
    expect(
      screen.getByText(
        'The session moonlit-harbor could not be found in the durable store.',
      ),
    ).toBeInTheDocument()
  })
})
