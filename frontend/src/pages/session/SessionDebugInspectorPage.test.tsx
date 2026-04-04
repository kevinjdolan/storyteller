import { screen } from '@testing-library/react'
import { afterEach, describe, expect, it, vi } from 'vitest'
import { MemoryRouter, Route, Routes } from 'react-router-dom'
import { SessionDebugInspectorPage } from './SessionDebugInspectorPage.tsx'
import { renderWithAppProviders } from '../../test/renderWithAppProviders.tsx'

const sampleInspectorResponse = {
  session_id: 'moonlit-harbor',
  generated_at: '2026-04-04T16:20:00Z',
  snapshot: {
    id: 'moonlit-harbor',
    display_title: 'Moonlit Harbor',
    working_title: 'Moonlit Harbor',
    library_summary: {
      display_kind: 'draft_session',
      title_source: 'working_title',
      runtime_seconds: null,
      runtime_source: null,
      artifact_readiness: {
        story_text: 'ready',
        story_docx: 'missing',
        final_audio: 'stale',
        ready_count: 1,
        total_count: 3,
      },
    },
    current_stage: 'composition',
    resume_stage: 'composition',
    furthest_completed_stage: 'story_setup',
    overall_status: 'needs_regeneration',
    created_at: '2026-04-04T14:00:00Z',
    updated_at: '2026-04-04T16:19:00Z',
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
      completed_stages: 7,
      in_progress_stages: 1,
      needs_regeneration_stages: 1,
    },
    stage_states: [],
    current_plan_revision: {
      id: 'plan-7',
      revision_number: 7,
      source_stage: 'story_setup',
      change_summary: 'Rebuilt the outline after softening the midpoint.',
      comparison_summary: null,
      restored_from_revision_number: null,
      changed_artifacts: ['story_outline', 'beat_sheet'],
      pitch: null,
      character_sheet: null,
      beat_sheet: null,
      story_setup: null,
      story_outline: null,
      is_current: true,
      created_at: '2026-04-04T15:55:00Z',
      updated_at: '2026-04-04T15:55:00Z',
    },
    latest_composition_job: {
      id: 'composition-9',
      job_kind: 'rewrite',
      status: 'failed',
      progress_percent: 84,
      total_segments: 6,
      start_segment_index: 2,
      plan_revision_id: 'plan-7',
      plan_revision_number: 7,
      beat_sheet_id: 'beat-4',
      beat_sheet_revision_number: 4,
      story_setup_id: 'setup-2',
      story_setup_revision_number: 2,
      story_outline_id: 'outline-3',
      story_outline_revision_number: 3,
      current_segment_id: 'segment-5',
      current_segment_index: 5,
      rewrite_to_segment_index: 5,
      downstream_regeneration_mode: 'require_confirmation',
      stale_from_segment_index: 5,
      stale_to_segment_index: 6,
      pending_review: false,
      rewrite_candidate_segment_indexes: [5, 6],
      accepted_story_so_far: 'The harbor had almost settled.',
      latest_partial_output: 'Then the fog horn startled everyone awake.',
      latest_segment_summary: 'Midpoint rewrite drifted too tense.',
      interruption_request: null,
      attempt_count: 2,
      stop_reason: 'The midpoint tone no longer matched the bedtime brief.',
      error_message: 'The composition pass exceeded the allowed bedtime tension threshold.',
      started_at: '2026-04-04T16:00:00Z',
      completed_at: '2026-04-04T16:10:00Z',
      created_at: '2026-04-04T15:59:00Z',
      updated_at: '2026-04-04T16:10:00Z',
    },
    latest_audio_job: {
      id: 'audio-4',
      status: 'in_progress',
      voice_key: 'luna',
      playback_speed: 0.95,
      include_background_music: true,
      music_profile: 'soft_piano',
      progress_percent: 50,
      current_step: 'Rendering narration segment 2 of 4.',
      current_step_index: 2,
      total_steps: 4,
      completed_segments: 1,
      estimated_duration_seconds: 780,
      total_segments: 4,
      current_segment_index: 2,
      latest_asset_id: 'asset-audio-2',
      latest_asset_kind: 'audio_segment',
      attempt_count: 1,
      stop_reason: null,
      error_message: null,
      started_at: '2026-04-04T16:12:00Z',
      completed_at: null,
      created_at: '2026-04-04T16:12:00Z',
      updated_at: '2026-04-04T16:18:00Z',
    },
    active_composition_job: null,
    active_audio_job: {
      id: 'audio-4',
      status: 'in_progress',
      voice_key: 'luna',
      playback_speed: 0.95,
      include_background_music: true,
      music_profile: 'soft_piano',
      progress_percent: 50,
      current_step: 'Rendering narration segment 2 of 4.',
      current_step_index: 2,
      total_steps: 4,
      completed_segments: 1,
      estimated_duration_seconds: 780,
      total_segments: 4,
      current_segment_index: 2,
      latest_asset_id: 'asset-audio-2',
      latest_asset_kind: 'audio_segment',
      attempt_count: 1,
      stop_reason: null,
      error_message: null,
      started_at: '2026-04-04T16:12:00Z',
      completed_at: null,
      created_at: '2026-04-04T16:12:00Z',
      updated_at: '2026-04-04T16:18:00Z',
    },
    composition_segments: [],
    audio_segments: [],
    latest_story_asset: null,
    latest_story_export_asset: null,
    latest_audio_asset: null,
    audio_settings: {
      voice_key: 'luna',
      playback_speed: 0.95,
      include_background_music: true,
      music_profile: 'soft_piano',
      music_volume: 0.24,
      narration_style: 'warm',
      narration_volume: 0.92,
      target_duration_minutes: 13,
      estimated_runtime: null,
      updated_at: '2026-04-04T16:11:00Z',
    },
    continuity_bible: null,
    agent_context_summary: 'The harbor midpoint needs to stay calm and reparative.',
  },
  hydration: {
    strategy: 'materialized_with_recent_replay',
    materialized_through_sequence_number: 9,
    replay_from_sequence_number: 10,
    replayed_event_count: 3,
    latest_sequence_number: 12,
    history_event_count: 12,
    history_window_truncated: false,
  },
  recent_history: {
    session_id: 'moonlit-harbor',
    latest_sequence_number: 12,
    events: [
      {
        id: 'event-10',
        session_id: 'moonlit-harbor',
        sequence_number: 10,
        actor: {
          actor_type: 'service',
          actor_id: 'composition-worker',
        },
        event_type: 'composition.progress.recorded',
        stage: 'composition',
        summary: 'Composition rewrite failed after segment 5.',
        payload: {
          schema_version: 1,
          job_id: 'composition-9',
          status: 'failed',
          progress_percent: 84,
        },
        created_at: '2026-04-04T16:10:00Z',
      },
      {
        id: 'event-11',
        session_id: 'moonlit-harbor',
        sequence_number: 11,
        actor: {
          actor_type: 'user',
          actor_id: 'developer',
        },
        event_type: 'ui.action.recorded',
        stage: 'audio',
        summary: 'Recorded UI action: reopened_audio_settings.',
        payload: {
          schema_version: 1,
          action: 'reopened_audio_settings',
          origin: 'workspace',
        },
        created_at: '2026-04-04T16:12:00Z',
      },
      {
        id: 'event-12',
        session_id: 'moonlit-harbor',
        sequence_number: 12,
        actor: {
          actor_type: 'service',
          actor_id: 'audio-worker',
        },
        event_type: 'audio.progress.recorded',
        stage: 'audio',
        summary: 'Audio rendering reached segment 2.',
        payload: {
          schema_version: 1,
          job_id: 'audio-4',
          status: 'in_progress',
          progress_percent: 50,
        },
        created_at: '2026-04-04T16:18:00Z',
      },
    ],
  },
  artifact_inventory: {
    session_id: 'moonlit-harbor',
    generated_at: '2026-04-04T16:20:00Z',
    items: [
      {
        key: 'story_text',
        label: 'Story text',
        artifact_kind: 'story_text',
        status: 'ready',
        status_detail: 'Latest manuscript is available.',
        asset: {
          id: 'asset-story-1',
          asset_kind: 'story_text',
          status: 'ready',
          storage_bucket: 'storyteller-sessions',
          object_path: 'sessions/moonlit-harbor/story.md',
          mime_type: 'text/markdown',
          composition_job_id: 'composition-8',
          audio_job_id: null,
          byte_size: 12044,
          duration_seconds: null,
          checksum_sha256: 'abc123',
          segment_index: null,
          error_message: null,
          details: null,
          access: null,
          public_url: null,
          ready_at: '2026-04-04T15:40:00Z',
          failed_at: null,
          superseded_at: null,
          created_at: '2026-04-04T15:40:00Z',
          updated_at: '2026-04-04T15:40:00Z',
        },
        preview_assets: [],
        preview_asset_count: 0,
        download_path: null,
        stream_path: null,
      },
      {
        key: 'story_docx',
        label: 'Story document',
        artifact_kind: 'story_docx',
        status: 'missing',
        status_detail: 'No export has been generated yet.',
        asset: null,
        preview_assets: [],
        preview_asset_count: 0,
        download_path: null,
        stream_path: null,
      },
      {
        key: 'final_audio',
        label: 'Final audio',
        artifact_kind: 'final_audio',
        status: 'stale',
        status_detail: 'Narration is stale because the composition rewrite failed.',
        asset: null,
        preview_assets: [],
        preview_asset_count: 1,
        download_path: null,
        stream_path: null,
      },
    ],
  },
  usage_diagnostics: {
    session_id: 'moonlit-harbor',
    generated_at: '2026-04-04T16:20:00Z',
    summary: {
      total_calls: 4,
      succeeded_calls: 3,
      failed_calls: 1,
      fallback_calls: 0,
      token_metadata_call_count: 4,
      cost_estimate_call_count: 4,
      total_elapsed_ms: 5020,
      average_elapsed_ms: 1255,
      max_elapsed_ms: 2410,
      approximate_cost_usd: 0.0834,
      token_usage: {
        input_tokens: 2100,
        output_tokens: 1600,
        total_tokens: 3700,
        cached_input_tokens: 120,
        thought_tokens: null,
      },
      buckets: [
        {
          usage_bucket: 'planning',
          total_calls: 2,
          succeeded_calls: 2,
          failed_calls: 0,
          fallback_calls: 0,
          token_metadata_call_count: 2,
          cost_estimate_call_count: 2,
          total_elapsed_ms: 980,
          average_elapsed_ms: 490,
          max_elapsed_ms: 560,
          approximate_cost_usd: 0.0124,
          models_used: ['gemini-3.1-flash-lite'],
          token_usage: {
            input_tokens: 600,
            output_tokens: 420,
            total_tokens: 1020,
            cached_input_tokens: 0,
            thought_tokens: null,
          },
          last_model_id: 'gemini-3.1-flash-lite',
          last_purpose: 'beat_sheet',
          last_called_at: '2026-04-04T15:54:00Z',
        },
        {
          usage_bucket: 'composition',
          total_calls: 2,
          succeeded_calls: 1,
          failed_calls: 1,
          fallback_calls: 0,
          token_metadata_call_count: 2,
          cost_estimate_call_count: 2,
          total_elapsed_ms: 4040,
          average_elapsed_ms: 2020,
          max_elapsed_ms: 2410,
          approximate_cost_usd: 0.071,
          models_used: ['gemini-3.1-pro'],
          token_usage: {
            input_tokens: 1500,
            output_tokens: 1180,
            total_tokens: 2680,
            cached_input_tokens: 120,
            thought_tokens: null,
          },
          last_model_id: 'gemini-3.1-pro',
          last_purpose: 'rewrite_segment',
          last_called_at: '2026-04-04T16:09:00Z',
        },
      ],
    },
    stage_breakdown: [],
    recent_calls: [],
    slowest_calls: [],
    costliest_calls: [],
  },
} as const

function buildJsonResponse(status: number, body: unknown) {
  return {
    ok: status >= 200 && status < 300,
    status,
    json: async () => body,
  } as Response
}

function renderInspectorRoute() {
  return renderWithAppProviders(
    <MemoryRouter initialEntries={['/sessions/moonlit-harbor/debug']}>
      <Routes>
        <Route
          path="/sessions/:sessionId/debug"
          element={<SessionDebugInspectorPage />}
        />
      </Routes>
    </MemoryRouter>,
  )
}

describe('SessionDebugInspectorPage', () => {
  afterEach(() => {
    vi.restoreAllMocks()
    vi.unstubAllGlobals()
  })

  it('renders the hidden inspector with session truth, jobs, events, and artifacts', async () => {
    vi.stubGlobal(
      'fetch',
      vi.fn(() =>
        Promise.resolve(buildJsonResponse(200, sampleInspectorResponse)),
      ),
    )

    renderInspectorRoute()

    expect(
      await screen.findByRole('heading', { name: 'Developer debug inspector' }),
    ).toBeInTheDocument()
    expect(await screen.findByText(/Revision 7/)).toBeInTheDocument()
    expect(
      screen.getAllByText(
        'The composition pass exceeded the allowed bedtime tension threshold.',
      ),
    ).toHaveLength(2)
    expect(screen.getByText('Narration is stale because the composition rewrite failed.')).toBeInTheDocument()
    expect(screen.getByText('Audio rendering reached segment 2.')).toBeInTheDocument()
    expect(screen.getByText(/Session snapshot JSON/)).toBeInTheDocument()
  })

  it('shows a developer-facing unavailable state when the backend flag is off', async () => {
    vi.stubGlobal(
      'fetch',
      vi.fn(() =>
        Promise.resolve(
          buildJsonResponse(404, {
            detail:
              'The developer debug inspector is not enabled for this environment.',
          }),
        ),
      ),
    )

    renderInspectorRoute()

    expect(
      await screen.findByRole('heading', { name: 'Debug inspector unavailable' }),
    ).toBeInTheDocument()
    expect(
      screen.getByText(
        'The developer debug inspector is not enabled for this environment.',
      ),
    ).toBeInTheDocument()
  })
})
