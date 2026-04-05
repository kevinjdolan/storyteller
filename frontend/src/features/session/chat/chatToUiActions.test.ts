import { describe, expect, it } from 'vitest'
import {
  getChatToUiActionDefaultPolicy,
  parseChatToUiActionBatch,
} from './chatToUiActions.ts'

describe('chatToUiActions', () => {
  it('parses a valid batch of proposed chat-to-ui actions', () => {
    const batch = parseChatToUiActionBatch({
      schema_version: 1,
      actions: [
        {
          schema_version: 1,
          action_type: 'select_genre',
          target_stage: 'genre',
          confidence: 0.98,
          rationale: 'The user explicitly asked for Quest Fantasy.',
          requires_confirmation: true,
          extracted_values: {
            genre_slug: 'quest-fantasy',
          },
        },
        {
          schema_version: 1,
          action_type: 'refine_beat_sheet',
          target_stage: 'beats',
          confidence: 0.77,
          rationale:
            'The message asked for a gentler midpoint and calmer recovery.',
          requires_confirmation: true,
          extracted_values: {
            instructions:
              'Soften the midpoint and make the comfort beat clearer.',
            beat_names: ['Midpoint', 'Final Image'],
          },
        },
        {
          schema_version: 1,
          action_type: 'refine_pitch',
          target_stage: 'pitches',
          confidence: 0.88,
          rationale:
            'The user wants pitch two to become a calmer sibling story.',
          requires_confirmation: true,
          extracted_values: {
            pitch_index: 2,
            instructions: 'Make pitch two about siblings who help each other.',
          },
        },
        {
          schema_version: 1,
          action_type: 'update_audio_settings',
          target_stage: 'audio',
          confidence: 0.69,
          rationale: 'The user requested slower narration and no music.',
          requires_confirmation: false,
          extracted_values: {
            playback_speed: 0.9,
            include_background_music: false,
          },
        },
      ],
    })

    expect(batch).not.toBeNull()
    expect(batch?.actions).toHaveLength(4)
    expect(batch?.actions[0]).toMatchObject({
      action_type: 'select_genre',
      target_stage: 'genre',
      extracted_values: {
        genre_slug: 'quest-fantasy',
      },
    })
    expect(batch?.actions[2]).toMatchObject({
      action_type: 'refine_pitch',
      extracted_values: {
        pitch_index: 2,
        instructions: 'Make pitch two about siblings who help each other.',
      },
    })
    expect(batch?.actions[3]).toMatchObject({
      action_type: 'update_audio_settings',
      extracted_values: {
        playback_speed: 0.9,
        include_background_music: false,
      },
    })
  })

  it('rejects confirm-first actions that try to skip confirmation', () => {
    expect(
      parseChatToUiActionBatch({
        schema_version: 1,
        actions: [
          {
            schema_version: 1,
            action_type: 'select_pitch',
            target_stage: 'pitches',
            confidence: 0.91,
            requires_confirmation: false,
            extracted_values: {
              pitch_index: 2,
            },
          },
        ],
      }),
    ).toBeNull()
  })

  it('rejects story setup updates with no extracted planning values', () => {
    expect(
      parseChatToUiActionBatch({
        schema_version: 1,
        actions: [
          {
            schema_version: 1,
            action_type: 'update_story_setup',
            target_stage: 'story_setup',
            confidence: 0.52,
            requires_confirmation: false,
            extracted_values: {},
          },
        ],
      }),
    ).toBeNull()
  })

  it('rejects pause and resume actions when the stage does not match the job kind', () => {
    expect(
      parseChatToUiActionBatch({
        schema_version: 1,
        actions: [
          {
            schema_version: 1,
            action_type: 'pause_job',
            target_stage: 'audio',
            confidence: 0.88,
            requires_confirmation: true,
            extracted_values: {
              job_kind: 'composition',
            },
          },
        ],
      }),
    ).toBeNull()
  })

  it('exposes the default auto-apply versus confirm-first policy', () => {
    expect(getChatToUiActionDefaultPolicy('navigate_to_stage')).toBe(
      'auto_apply_candidate',
    )
    expect(getChatToUiActionDefaultPolicy('start_composition')).toBe(
      'confirm_first',
    )
  })

  it('parses targeted character refinements with impact metadata', () => {
    const batch = parseChatToUiActionBatch({
      schema_version: 1,
      actions: [
        {
          schema_version: 1,
          action_type: 'refine_character_sheet',
          target_stage: 'characters',
          confidence: 0.84,
          rationale:
            "The user wants to soften Mira's voice on the saved Lantern Keeper cast.",
          requires_confirmation: true,
          extracted_values: {
            revision_number: 2,
            title: 'Lantern Keeper Cast',
            instructions:
              "Soften Mira's voice and keep the same comfort ritual.",
            focus_character_names: ['Mira'],
            change_summary: 'Keep the same arc but make the dialogue gentler.',
            change_impact: 'minor',
          },
        },
      ],
    })

    expect(batch).not.toBeNull()
    expect(batch?.actions[0]).toMatchObject({
      action_type: 'refine_character_sheet',
      extracted_values: {
        revision_number: 2,
        title: 'Lantern Keeper Cast',
        focus_character_names: ['Mira'],
        change_impact: 'minor',
      },
    })
  })
})
