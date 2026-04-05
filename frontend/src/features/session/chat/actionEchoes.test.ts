import { describe, expect, it } from 'vitest'
import {
  buildIntentActionEchoMessages,
  buildSessionChatMessagesFromHistory,
} from './actionEchoes.ts'

describe('actionEchoes', () => {
  it('rebuilds compact transcript messages from durable history events', () => {
    const messages = buildSessionChatMessagesFromHistory(
      {
        session_id: 'session-123',
        latest_sequence_number: 4,
        events: [
          {
            id: 'event-1',
            session_id: 'session-123',
            sequence_number: 1,
            actor: {
              actor_type: 'user',
              actor_id: 'local-user',
            },
            event_type: 'session.created',
            stage: null,
            summary: 'Created session: Lantern Harbor.',
            payload: {
              schema_version: 1,
              working_title: 'Lantern Harbor',
            },
            created_at: '2026-04-01T08:00:00Z',
          },
          {
            id: 'event-2',
            session_id: 'session-123',
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
            created_at: '2026-04-01T08:01:00Z',
          },
          {
            id: 'event-3',
            session_id: 'session-123',
            sequence_number: 3,
            actor: {
              actor_type: 'user',
              actor_id: 'local-user',
            },
            event_type: 'ui.action.recorded',
            stage: 'audio',
            summary: 'Recorded UI action: navigate_to_stage.',
            payload: {
              schema_version: 1,
              action: 'navigate_to_stage',
              control_id: 'stage-navigator',
              value_summary: 'Audio',
              origin: 'workspace',
            },
            created_at: '2026-04-01T08:02:00Z',
          },
          {
            id: 'event-4',
            session_id: 'session-123',
            sequence_number: 4,
            actor: {
              actor_type: 'assistant',
              actor_id: 'story-planner',
            },
            event_type: 'chat.message.recorded',
            stage: 'audio',
            summary: 'Recorded assistant chat message.',
            payload: {
              schema_version: 1,
              message_role: 'assistant',
              content_preview: 'Audio settings are ready for review.',
              content_length: 36,
              source: 'intent_parser',
            },
            created_at: '2026-04-01T08:03:00Z',
          },
        ],
      },
      {
        resume_stage: 'beats',
      } as never,
    )

    expect(messages).toEqual([
      expect.objectContaining({
        role: 'system',
        body: 'Session opened. Resume at Beat sheet.',
      }),
      expect.objectContaining({
        role: 'action_echo',
        body: 'Selected genre: Quest Fantasy',
      }),
      expect.objectContaining({
        role: 'action_echo',
        body: 'Opened Audio in the main pane.',
      }),
      expect.objectContaining({
        role: 'assistant',
        body: 'Audio settings are ready for review.',
      }),
    ])
  })

  it('renders blocked chat intent outcomes as compact action echoes', () => {
    const messages = buildIntentActionEchoMessages({
      createdAt: '2026-04-01T08:10:00Z',
      result: {
        schema_version: 1,
        status: 'parsed',
        needs_clarification: false,
        assistant_response:
          'I can shorten the story once story setup is ready.',
        clarification_reason: null,
        proposed_actions: {
          schema_version: 1,
          actions: [
            {
              schema_version: 1,
              action_type: 'update_story_setup',
              target_stage: 'story_setup',
              confidence: 0.82,
              rationale: 'The user asked for a shorter runtime.',
              requires_confirmation: false,
              extracted_values: {
                target_runtime_minutes: 8,
              },
            },
          ],
        },
        policy_evaluation: {
          schema_version: 1,
          session_id: 'session-123',
          evaluated_actions: [
            {
              action_index: 0,
              action_type: 'update_story_setup',
              target_stage: 'story_setup',
              decision: 'rejected',
              summary:
                'Complete or regenerate beats before changing story_setup.',
              reasons: [
                {
                  code: 'prerequisite_stage_incomplete',
                  message:
                    'Complete or regenerate beats before changing story_setup.',
                  stage: 'story_setup',
                  related_stages: ['beats'],
                  related_action_types: [],
                },
              ],
              side_effects: [],
              prerequisite_action_types: [],
            },
          ],
        },
      },
    })

    expect(messages).toEqual([
      expect.objectContaining({
        role: 'action_echo',
        body: "Couldn't update story setup yet. Finish Beat sheet first.",
      }),
    ])
  })

  it('prefers explicit user-edit summary text when replaying durable history', () => {
    const messages = buildSessionChatMessagesFromHistory(
      {
        session_id: 'session-123',
        latest_sequence_number: 1,
        events: [
          {
            id: 'event-1',
            session_id: 'session-123',
            sequence_number: 1,
            actor: {
              actor_type: 'user',
              actor_id: 'local-user',
            },
            event_type: 'content.user_edit.recorded',
            stage: 'beats',
            summary: 'Saved user edit for beat sheet.',
            payload: {
              schema_version: 1,
              target_kind: 'beat_sheet',
              changed_fields: ['detail'],
              summary_text: 'Updated beat sheet notes from the workspace.',
            },
            created_at: '2026-04-01T08:12:00Z',
          },
        ],
      },
      {
        resume_stage: 'beats',
      } as never,
    )

    expect(messages).toContainEqual(
      expect.objectContaining({
        role: 'action_echo',
        body: 'Updated beat sheet notes from the workspace.',
      }),
    )
  })

  it('includes character refinement rationale in selection echoes when present', () => {
    const messages = buildSessionChatMessagesFromHistory(
      {
        session_id: 'session-123',
        latest_sequence_number: 1,
        events: [
          {
            id: 'event-1',
            session_id: 'session-123',
            sequence_number: 1,
            actor: {
              actor_type: 'user',
              actor_id: 'local-user',
            },
            event_type: 'selection.recorded',
            stage: 'characters',
            summary: 'Selected character sheet: Lantern Keeper Cast: Softer.',
            payload: {
              schema_version: 1,
              selection_kind: 'character_sheet',
              label: 'Lantern Keeper Cast: Softer',
              rationale:
                'Refined from "Lantern Keeper Cast" with: Soften Mira\'s voice. Change impact: minor.',
              accepted: true,
              source: 'workspace',
            },
            created_at: '2026-04-01T08:14:00Z',
          },
        ],
      },
      {
        resume_stage: 'characters',
      } as never,
    )

    expect(messages).toContainEqual(
      expect.objectContaining({
        role: 'action_echo',
        body: 'Selected character sheet: Lantern Keeper Cast: Softer. Refined from "Lantern Keeper Cast" with: Soften Mira\'s voice. Change impact: minor.',
      }),
    )
  })

  it('includes pitch refinement rationale in selection echoes when present', () => {
    const messages = buildSessionChatMessagesFromHistory(
      {
        session_id: 'session-123',
        latest_sequence_number: 1,
        events: [
          {
            id: 'event-1',
            session_id: 'session-123',
            sequence_number: 1,
            actor: {
              actor_type: 'user',
              actor_id: 'local-user',
            },
            event_type: 'selection.recorded',
            stage: 'pitches',
            summary: 'Selected pitch: Lanterns Over Juniper Lake: Siblings.',
            payload: {
              schema_version: 1,
              selection_kind: 'pitch',
              label: 'Lanterns Over Juniper Lake: Siblings',
              accepted: true,
              source: 'chat',
              rationale:
                'Refined from Lanterns Over Juniper Lake. Make it about siblings who help each other settle down.',
            },
            created_at: '2026-04-01T08:14:00Z',
          },
        ],
      },
      {
        resume_stage: 'pitches',
      } as never,
    )

    expect(messages).toContainEqual(
      expect.objectContaining({
        role: 'action_echo',
        body: 'Selected pitch: Lanterns Over Juniper Lake: Siblings. Refined from Lanterns Over Juniper Lake. Make it about siblings who help each other settle down.',
      }),
    )
  })

  it('renders composition progress history as a compact action echo', () => {
    const messages = buildSessionChatMessagesFromHistory(
      {
        session_id: 'session-123',
        latest_sequence_number: 1,
        events: [
          {
            id: 'event-1',
            session_id: 'session-123',
            sequence_number: 1,
            actor: {
              actor_type: 'system',
              actor_id: 'worker',
            },
            event_type: 'composition.progress.recorded',
            stage: 'composition',
            summary: 'Composition progress 42.0%.',
            payload: {
              schema_version: 1,
              job_id: 'composition-job-1',
              status: 'paused',
              progress_percent: 42,
              current_segment_index: 2,
              total_segments: 4,
              segment_id: 'segment-2',
            },
            created_at: '2026-04-01T08:16:00Z',
          },
        ],
      },
      {
        resume_stage: 'composition',
      } as never,
    )

    expect(messages).toContainEqual(
      expect.objectContaining({
        role: 'action_echo',
        body: 'Writing paused at 42% complete.',
      }),
    )
  })

  it('prefers queued interruption messages over generic composition progress copy', () => {
    const messages = buildSessionChatMessagesFromHistory(
      {
        session_id: 'session-123',
        latest_sequence_number: 1,
        events: [
          {
            id: 'event-1',
            session_id: 'session-123',
            sequence_number: 1,
            actor: {
              actor_type: 'system',
              actor_id: 'worker',
            },
            event_type: 'composition.progress.recorded',
            stage: 'composition',
            summary: 'Composition progress 46.0%.',
            payload: {
              schema_version: 1,
              job_id: 'composition-job-1',
              status: 'in_progress',
              progress_percent: 46,
              current_segment_index: 2,
              total_segments: 5,
              interruption_request: {
                id: 'interrupt-1',
                request_kind: 'redirect',
                state: 'requested',
                origin: 'workspace',
                message:
                  'Rewrite requested from segment 2. The current chunk will finish saving before the redirect applies.',
                created_at: '2026-04-01T08:17:00Z',
                updated_at: '2026-04-01T08:17:00Z',
              },
            },
            created_at: '2026-04-01T08:17:00Z',
          },
        ],
      },
      {
        resume_stage: 'composition',
      } as never,
    )

    expect(messages).toContainEqual(
      expect.objectContaining({
        role: 'action_echo',
        body: 'Rewrite requested from segment 2. The current chunk will finish saving before the redirect applies.',
      }),
    )
  })
})
