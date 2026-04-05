import { describe, expect, it } from 'vitest'
import type { SessionSnapshot } from '../../../api/sessions.ts'
import {
  buildSessionChatQuickActions,
  buildSessionChatQuickActionSubmission,
  buildSessionChatSlashCommandHint,
  resolveSessionChatSlashCommand,
} from './chatCommands.ts'

const sampleSnapshot: SessionSnapshot = {
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
  stage_states: [],
  story_brief: null,
  selected_pitch: {
    id: 'pitch-1',
    generation_key: 'batch-1',
    pitch_index: 0,
    title: 'Lanterns Over Juniper Lake',
    logline: 'A child and an otter guardian follow drifting lanterns.',
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
}

describe('chatCommands', () => {
  it('builds a small discoverable quick-action list for the current stage', () => {
    const quickActions = buildSessionChatQuickActions({
      snapshot: sampleSnapshot,
      selectedStage: 'beats',
    })

    expect(quickActions).toMatchObject([
      {
        commandId: 'next_stage',
        label: 'Next stage',
        slashCommand: '/next-stage',
      },
      {
        commandId: 'regenerate_pitches',
        label: 'Regenerate pitches',
        slashCommand: '/regenerate-pitches',
      },
      {
        commandId: 'summarize_plan',
        label: 'Summarize plan',
        slashCommand: '/plan',
      },
    ])
    expect(buildSessionChatSlashCommandHint(quickActions)).toBe(
      '/next-stage, /regenerate-pitches, /plan',
    )
  })

  it('turns a slash command into an explicit command request with action batch', () => {
    const submission = resolveSessionChatSlashCommand({
      input: '/next-stage',
      snapshot: sampleSnapshot,
      selectedStage: 'beats',
    })

    expect(submission).not.toBeNull()
    expect(submission).toMatchObject({
      explicitCommand: {
        command_id: 'next_stage',
        source: 'slash_command',
        proposed_actions: {
          schema_version: 1,
          actions: [
            {
              action_type: 'navigate_to_stage',
              target_stage: 'story_setup',
            },
          ],
        },
      },
    })
  })

  it('builds a quick-action submission for pausing composition jobs', () => {
    const submission = buildSessionChatQuickActionSubmission({
      commandId: 'pause_writing',
      snapshot: {
        ...sampleSnapshot,
        current_stage: 'composition',
        active_composition_job: {
          id: 'composition-job-1',
          status: 'in_progress',
          progress_percent: 48,
          current_segment_index: 2,
        },
      },
      selectedStage: 'composition',
    })

    expect(submission).not.toBeNull()
    expect(submission).toMatchObject({
      message: '/pause-writing',
      explicitCommand: {
        command_id: 'pause_writing',
        source: 'quick_action',
        proposed_actions: {
          schema_version: 1,
          actions: [
            {
              action_type: 'pause_job',
              target_stage: 'composition',
              extracted_values: {
                job_kind: 'composition',
                job_id: 'composition-job-1',
              },
            },
          ],
        },
      },
    })
  })

  it('hides pause quick actions while another composition interruption is pending', () => {
    const quickActions = buildSessionChatQuickActions({
      snapshot: {
        ...sampleSnapshot,
        current_stage: 'composition',
        active_composition_job: {
          id: 'composition-job-1',
          status: 'in_progress',
          progress_percent: 48,
          current_segment_index: 2,
          interruption_request: {
            id: 'interrupt-1',
            request_kind: 'redirect',
            state: 'requested',
            origin: 'workspace',
            message:
              'Rewrite requested from segment 2. The current chunk will finish saving before the redirect applies.',
            created_at: '2026-04-01T05:16:00Z',
            updated_at: '2026-04-01T05:16:00Z',
          },
        },
      },
      selectedStage: 'composition',
    })

    expect(
      quickActions.some((action) => action.commandId === 'pause_writing'),
    ).toBe(false)
  })
})
