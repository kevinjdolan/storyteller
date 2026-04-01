import { fireEvent, screen, within } from '@testing-library/react'
import { MemoryRouter, Route, Routes } from 'react-router-dom'
import { afterEach, describe, expect, it, vi } from 'vitest'
import { renderWithAppProviders } from '../../test/renderWithAppProviders.tsx'
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

const sampleHistory = {
  session_id: 'moonlit-harbor',
  latest_sequence_number: 4,
  events: [
    {
      id: 'event-1',
      session_id: 'moonlit-harbor',
      sequence_number: 1,
      actor: {
        actor_type: 'user',
        actor_id: 'local-user',
      },
      event_type: 'session.created',
      stage: null,
      summary: 'Created session: Lanterns Over Juniper Lake.',
      payload: {
        schema_version: 1,
        working_title: 'Lanterns Over Juniper Lake',
      },
      created_at: '2026-04-01T03:00:00Z',
    },
    {
      id: 'event-2',
      session_id: 'moonlit-harbor',
      sequence_number: 2,
      actor: {
        actor_type: 'user',
        actor_id: 'local-user',
      },
      event_type: 'selection.recorded',
      stage: 'genre',
      summary: 'Selected genre: Quest Fantasy.',
      payload: {
        schema_version: 1,
        selection_kind: 'genre',
        label: 'Quest Fantasy',
        accepted: true,
        source: 'ui',
      },
      created_at: '2026-04-01T03:01:00Z',
    },
    {
      id: 'event-3',
      session_id: 'moonlit-harbor',
      sequence_number: 3,
      actor: {
        actor_type: 'user',
        actor_id: 'local-user',
      },
      event_type: 'selection.recorded',
      stage: 'tone',
      summary: 'Selected tone profile: Hushed Wonder.',
      payload: {
        schema_version: 1,
        selection_kind: 'tone_profile',
        label: 'Hushed Wonder',
        accepted: true,
        source: 'ui',
      },
      created_at: '2026-04-01T03:02:00Z',
    },
    {
      id: 'event-4',
      session_id: 'moonlit-harbor',
      sequence_number: 4,
      actor: {
        actor_type: 'assistant',
        actor_id: 'story-planner',
      },
      event_type: 'chat.message.recorded',
      stage: 'beats',
      summary: 'Recorded assistant chat message.',
      payload: {
        schema_version: 1,
        message_role: 'assistant',
        content_preview:
          'The current focus is softening the midpoint before composition starts.',
        content_length: 71,
        source: 'intent_parser',
      },
      created_at: '2026-04-01T03:03:00Z',
    },
  ],
} as const

function buildJsonResponse(status: number, body: unknown) {
  return {
    ok: status >= 200 && status < 300,
    status,
    json: async () => body,
  } as Response
}

function resolveRequestUrl(input: RequestInfo | URL) {
  if (typeof input === 'string') {
    return input
  }

  if (input instanceof URL) {
    return input.toString()
  }

  return input.url
}

function buildUiActionEvent(body: Record<string, unknown>) {
  return {
    id: `ui-event-${String(body.action ?? 'unknown')}`,
    session_id: 'moonlit-harbor',
    sequence_number: 8,
    actor: {
      actor_type: 'user',
      actor_id: 'local-user',
    },
    event_type: 'ui.action.recorded',
    stage: body.stage ?? null,
    summary: `Recorded UI action: ${String(body.action ?? 'unknown')}.`,
    payload: {
      schema_version: 1,
      action: body.action,
      control_id: body.control_id ?? null,
      value_summary: body.value_summary ?? null,
      origin: body.origin ?? 'workspace',
    },
    created_at: '2026-04-01T03:04:00Z',
  }
}

function buildContextUpdateResponse(body: Record<string, unknown>) {
  const detail =
    typeof body.values === 'object' &&
    body.values !== null &&
    'detail' in body.values &&
    typeof body.values.detail === 'string'
      ? body.values.detail
      : ''

  return {
    snapshot: {
      ...sampleSnapshot,
      updated_at: '2026-04-01T03:05:00Z',
      stage_states: sampleSnapshot.stage_states.map((stageState) =>
        stageState.stage === body.stage
          ? {
              ...stageState,
              detail,
              last_event_summary:
                'Updated beat sheet notes from the workspace.',
              last_event_type: 'content.user_edit.recorded',
              last_event_at: '2026-04-01T03:05:00Z',
            }
          : stageState,
      ),
      agent_context_summary: `Session title: Lanterns Over Juniper Lake\nCurrent beat sheet detail: ${detail}`,
    },
    event: {
      id: 'context-update-event',
      session_id: 'moonlit-harbor',
      sequence_number: 9,
      actor: {
        actor_type: 'user',
        actor_id: 'local-user',
      },
      event_type: 'content.user_edit.recorded',
      stage: body.stage ?? null,
      summary: 'Saved user edit for beat sheet.',
      payload: {
        schema_version: 1,
        target_kind: 'beat_sheet',
        changed_fields: ['detail'],
        source: body.origin ?? 'workspace',
        field_values: {
          detail,
          control_id: body.control_id ?? null,
        },
        summary_text: 'Updated beat sheet notes from the workspace.',
      },
      created_at: '2026-04-01T03:05:00Z',
    },
  }
}

function mockWorkspaceApi(options?: {
  history?: unknown
  snapshot?: unknown
  snapshotStatus?: number
  chatIntentResponse?: unknown
}) {
  const history = options?.history ?? sampleHistory
  const snapshot = options?.snapshot ?? sampleSnapshot
  const snapshotStatus = options?.snapshotStatus ?? 200
  const chatIntentResponse = options?.chatIntentResponse ?? {
    schema_version: 1,
    status: 'parsed',
    needs_clarification: false,
    assistant_response:
      'I can open the audio stage so you can review narration settings.',
    clarification_reason: null,
    proposed_actions: {
      schema_version: 1,
      actions: [
        {
          schema_version: 1,
          action_type: 'navigate_to_stage',
          target_stage: 'audio',
          confidence: 0.96,
          rationale: 'The user asked to move to audio controls.',
          requires_confirmation: false,
          extracted_values: {},
        },
      ],
    },
    policy_evaluation: {
      schema_version: 1,
      session_id: 'moonlit-harbor',
      evaluated_actions: [
        {
          action_index: 0,
          action_type: 'navigate_to_stage',
          target_stage: 'audio',
          decision: 'accepted',
          summary: 'Navigation is allowed.',
          reasons: [],
          side_effects: [],
          prerequisite_action_types: [],
        },
      ],
    },
  }

  vi.stubGlobal(
    'fetch',
    vi.fn((input: RequestInfo | URL, init?: RequestInit) => {
      const url = resolveRequestUrl(input)
      const { pathname } = new URL(url, 'http://localhost')

      if (
        pathname === '/api/v1/sessions/moonlit-harbor' &&
        (init?.method == null || init.method === 'GET')
      ) {
        return Promise.resolve(buildJsonResponse(snapshotStatus, snapshot))
      }

      if (pathname === '/api/v1/sessions/moonlit-harbor/history') {
        return Promise.resolve(buildJsonResponse(200, history))
      }

      if (
        pathname === '/api/v1/sessions/moonlit-harbor/chat/intents' &&
        init?.method === 'POST'
      ) {
        return Promise.resolve(
          chatIntentResponse instanceof Response
            ? chatIntentResponse
            : buildJsonResponse(200, chatIntentResponse),
        )
      }

      if (
        pathname === '/api/v1/sessions/moonlit-harbor/ui-actions' &&
        init?.method === 'POST'
      ) {
        const requestBody =
          typeof init.body === 'string'
            ? (JSON.parse(init.body) as Record<string, unknown>)
            : {}

        return Promise.resolve(
          buildJsonResponse(201, buildUiActionEvent(requestBody)),
        )
      }

      if (
        pathname === '/api/v1/sessions/moonlit-harbor/context-updates' &&
        init?.method === 'POST'
      ) {
        const requestBody =
          typeof init.body === 'string'
            ? (JSON.parse(init.body) as Record<string, unknown>)
            : {}

        return Promise.resolve(
          buildJsonResponse(200, buildContextUpdateResponse(requestBody)),
        )
      }

      throw new Error(`Unhandled request: ${init?.method ?? 'GET'} ${url}`)
    }),
  )
}

function renderWorkspaceRoute() {
  return renderWithAppProviders(
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
    expect(screen.getByText('Selected tone: Hushed Wonder')).toBeInTheDocument()
    expect(screen.getByText('5 of 10 stages complete')).toBeInTheDocument()
    expect(
      screen.getByRole('navigation', { name: 'Stage navigator' }),
    ).toBeInTheDocument()
    expect(
      screen.getByRole('heading', {
        level: 2,
        name: 'Refine the Save-the-Cat beats',
      }),
    ).toBeInTheDocument()
    expect(screen.getAllByText('Live feed idle').length).toBeGreaterThan(0)
    expect(screen.getByTestId('live-feed-status')).toHaveTextContent('Idle')
    expect(screen.getByRole('link', { name: 'Return home' })).toHaveAttribute(
      'href',
      '/',
    )
    expect(screen.getByRole('log')).toBeInTheDocument()
    expect(
      screen.getByRole('button', { name: 'Send message' }),
    ).toBeInTheDocument()
    expect(
      screen.getByText(
        'The current focus is softening the midpoint before composition starts.',
      ),
    ).toBeInTheDocument()
    expect(
      screen.getAllByText('Midpoint needs one more bedtime-soft pass.').length,
    ).toBeGreaterThan(0)
    expect(
      screen.getByRole('heading', { level: 3, name: 'Workflow component kit' }),
    ).toBeInTheDocument()
    expect(screen.getByText('Choice cards')).toBeInTheDocument()
  })

  it('supports route-backed stage preview without changing the durable current step', async () => {
    mockWorkspaceApi()

    renderWithAppProviders(
      <MemoryRouter initialEntries={['/sessions/moonlit-harbor?stage=audio']}>
        <Routes>
          <Route
            path="/sessions/:sessionId"
            element={<SessionWorkspacePage />}
          />
        </Routes>
      </MemoryRouter>,
    )

    expect(
      await screen.findByRole('heading', {
        level: 2,
        name: 'Configure narration and music',
      }),
    ).toBeInTheDocument()
    expect(
      screen.getByText(
        /the route is previewing audio via the stage query parameter/i,
      ),
    ).toBeInTheDocument()
    expect(screen.getByRole('link', { name: /audio/i })).toHaveAttribute(
      'href',
      '/sessions/moonlit-harbor?stage=audio',
    )
    expect(screen.getAllByText('?stage=audio').length).toBeGreaterThan(0)
  })

  it('records direct stage-preview clicks as action echoes in the transcript', async () => {
    mockWorkspaceApi()

    renderWorkspaceRoute()

    const audioLink = await screen.findByRole('link', { name: /audio/i })

    fireEvent.click(audioLink)

    expect(
      await screen.findByText('Opened Audio in the main pane.'),
    ).toBeInTheDocument()
  })

  it('shows chat-driven action echoes when a parsed action changes the visible UI', async () => {
    mockWorkspaceApi()

    renderWorkspaceRoute()

    const composer = await screen.findByLabelText('Message composer')

    fireEvent.change(composer, {
      target: {
        value: 'Take me to the audio settings.',
      },
    })
    fireEvent.click(screen.getByRole('button', { name: 'Send message' }))

    expect(
      within(screen.getByRole('log')).getByText(
        'Take me to the audio settings.',
      ),
    ).toBeInTheDocument()
    expect(
      await screen.findByText(
        'I can open the audio stage so you can review narration settings.',
      ),
    ).toBeInTheDocument()
    expect(
      await screen.findByText('Opened Audio in the main pane.'),
    ).toBeInTheDocument()
    expect(
      await screen.findByRole('heading', {
        level: 2,
        name: 'Configure narration and music',
      }),
    ).toBeInTheDocument()
  })

  it('saves a stage note through the durable context update pipeline', async () => {
    mockWorkspaceApi()

    renderWorkspaceRoute()

    const noteField = await screen.findByLabelText('Beat sheet note')

    fireEvent.change(noteField, {
      target: {
        value: 'Add one calmer beat before the return home.',
      },
    })
    fireEvent.click(screen.getByRole('button', { name: 'Save note' }))

    expect(
      await screen.findByText('Updated beat sheet notes from the workspace.'),
    ).toBeInTheDocument()
    expect(screen.getByLabelText('Beat sheet note')).toHaveValue(
      'Add one calmer beat before the return home.',
    )
  })

  it('shows a missing-session state when the snapshot request returns 404', async () => {
    mockWorkspaceApi({
      snapshotStatus: 404,
      snapshot: { detail: 'missing' },
    })

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
