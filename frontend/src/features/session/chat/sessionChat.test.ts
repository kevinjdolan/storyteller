import { describe, expect, it } from 'vitest'
import type { SessionSnapshot } from '../../../api/sessions.ts'
import { buildInitialSessionChatMessages } from './sessionChat.ts'

function buildSampleSnapshot(): SessionSnapshot {
  return {
    id: 'session-123',
    display_title: 'Lantern Harbor',
    current_stage: 'composition',
    resume_stage: 'composition',
    furthest_completed_stage: 'story_setup',
    overall_status: 'in_progress',
    created_at: '2026-04-01T08:00:00Z',
    updated_at: '2026-04-01T08:10:00Z',
    completed_at: null,
    progress: {
      total_stages: 10,
      completed_stages: 7,
      in_progress_stages: 1,
      needs_regeneration_stages: 0,
    },
    stage_states: [
      {
        stage: 'composition',
        label: 'Composition',
        description: 'Draft the story durably in segments.',
        status: 'in_progress',
        detail: 'Drafting the midpoint.',
        started_at: '2026-04-01T08:05:00Z',
      },
    ],
    active_composition_job: {
      id: 'composition-job-1',
      status: 'in_progress',
      progress_percent: 42,
      current_segment_index: 2,
      total_segments: 3,
      status_message:
        'Gemini hit a temporary rate limit while drafting segment 2 of 3. Retrying in 2s (attempt 2 of 3).',
      updated_at: '2026-04-01T08:10:00Z',
    },
    latest_composition_job: {
      id: 'composition-job-1',
      status: 'in_progress',
      progress_percent: 42,
      current_segment_index: 2,
      total_segments: 3,
      status_message:
        'Gemini hit a temporary rate limit while drafting segment 2 of 3. Retrying in 2s (attempt 2 of 3).',
      updated_at: '2026-04-01T08:10:00Z',
    },
    active_audio_job: null,
    latest_story_asset: null,
    latest_audio_asset: null,
  } as SessionSnapshot
}

describe('sessionChat', () => {
  it('prefers the composition status message over generic progress copy', () => {
    const messages = buildInitialSessionChatMessages(buildSampleSnapshot())

    expect(messages.at(-1)?.body).toBe(
      'Gemini hit a temporary rate limit while drafting segment 2 of 3. Retrying in 2s (attempt 2 of 3).',
    )
  })
})
