import { describe, expect, it } from 'vitest'
import type { SessionSnapshot } from '../../api/sessions.ts'
import {
  createInitialSessionRuntimeState,
  createSessionRuntimeStore,
} from './sessionRuntimeStore.ts'

function buildSampleSnapshot(): SessionSnapshot {
  return {
    id: 'session-123',
    display_title: 'Lantern Harbor',
    working_title: 'Lantern Harbor',
    current_stage: 'beats',
    resume_stage: 'beats',
    furthest_completed_stage: 'characters',
    overall_status: 'in_progress',
    created_at: '2026-04-01T08:00:00Z',
    updated_at: '2026-04-01T08:10:00Z',
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
        description: 'Genre',
        status: 'completed',
        detail: 'Accepted quest fantasy.',
      },
      {
        stage: 'tone',
        label: 'Tone',
        description: 'Tone',
        status: 'completed',
        detail: 'Selected a calm tone.',
      },
      {
        stage: 'brief',
        label: 'Story brief',
        description: 'Brief',
        status: 'completed',
        detail: 'Accepted the brief.',
      },
      {
        stage: 'pitches',
        label: 'Pitches',
        description: 'Pitches',
        status: 'completed',
        detail: 'Accepted the pitch.',
      },
      {
        stage: 'characters',
        label: 'Characters',
        description: 'Characters',
        status: 'completed',
        detail: 'Locked the cast.',
      },
      {
        stage: 'beats',
        label: 'Beat sheet',
        description: 'Beats',
        status: 'in_progress',
        detail: 'Refining the midpoint.',
      },
      {
        stage: 'story_setup',
        label: 'Story setup',
        description: 'Story setup',
        status: 'draft',
        detail: null,
      },
      {
        stage: 'composition',
        label: 'Composition',
        description: 'Composition',
        status: 'draft',
        detail: null,
      },
      {
        stage: 'audio',
        label: 'Audio',
        description: 'Audio',
        status: 'draft',
        detail: null,
      },
      {
        stage: 'finalize',
        label: 'Finalize',
        description: 'Finalize',
        status: 'draft',
        detail: null,
      },
    ],
    story_brief: {
      id: 'brief-1',
      revision_number: 1,
      raw_brief: 'A child follows floating lanterns across the harbor.',
      normalized_summary: 'A calm harbor quest.',
    },
    selected_pitch: {
      id: 'pitch-1',
      generation_key: 'pitch-batch-1',
      pitch_index: 0,
      title: 'Lantern Harbor',
      logline:
        'A child helps a shy otter guide lost lanterns home before bedtime.',
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
}

describe('sessionRuntimeStore', () => {
  it('starts empty with idle connection metadata', () => {
    expect(createInitialSessionRuntimeState()).toEqual({
      sessionSnapshot: null,
      chat: {
        messages: [],
      },
      pendingActions: [],
      eventStream: {
        connectionState: 'idle',
        connectionDetail: null,
        channel: null,
        retryCount: 0,
        lastConnectedAt: null,
        lastEventId: null,
        lastSequenceNumber: null,
        events: [],
      },
    })
  })

  it('hydrates the session snapshot and merges workflow stage changes into it', () => {
    const store = createSessionRuntimeStore()

    store.hydrateSessionSnapshot(buildSampleSnapshot())
    store.applyRealtimeEvent({
      schema_version: 1,
      event_id: 'rt-14',
      type: 'workflow.stage_changed',
      session_id: 'session-123',
      channel: 'session:session-123',
      actor: {
        actor_type: 'assistant',
        actor_id: 'story-planner',
      },
      stage: 'beats',
      created_at: '2026-04-01T08:12:00Z',
      correlation_id: 'mutation-9',
      delivery: 'replay',
      replayable: true,
      sequence_number: 14,
      event_log_entry_id: 'event-log-14',
      payload: {
        schema_version: 1,
        previous_status: 'in_progress',
        status: 'completed',
        detail: 'Accepted the softened beat sheet.',
        invalidated_stages: ['composition', 'audio', 'finalize'],
        current_stage: 'story_setup',
        resume_stage: 'story_setup',
        furthest_completed_stage: 'beats',
        overall_status: 'in_progress',
      },
    })

    expect(store.getState().sessionSnapshot?.current_stage).toBe('story_setup')
    expect(
      store
        .getState()
        .sessionSnapshot?.stage_states.find((stage) => stage.stage === 'beats'),
    ).toMatchObject({
      status: 'completed',
      detail: 'Accepted the softened beat sheet.',
      last_event_type: 'workflow.stage_changed',
    })
    expect(
      store
        .getState()
        .sessionSnapshot?.stage_states.find(
          (stage) => stage.stage === 'composition',
        ),
    ).toMatchObject({
      status: 'needs_regeneration',
    })
    expect(store.getState().eventStream.lastSequenceNumber).toBe(14)
  })

  it('adds chat and action-echo events to the transcript while confirming correlated actions', () => {
    const store = createSessionRuntimeStore()

    store.enqueuePendingAction({
      id: 'action-1',
      label: 'Accepted revised beat sheet',
      origin: 'ui',
      createdAt: '2026-04-01T08:00:00Z',
      correlationId: 'mutation-7',
    })
    store.applyRealtimeEvent({
      schema_version: 1,
      event_id: 'rt-15',
      type: 'ui.action_echo',
      session_id: 'session-123',
      channel: 'session:session-123',
      actor: {
        actor_type: 'user',
        actor_id: 'local-user',
      },
      stage: 'beats',
      created_at: '2026-04-01T08:00:01Z',
      correlation_id: 'mutation-7',
      delivery: 'live',
      replayable: true,
      sequence_number: 15,
      event_log_entry_id: 'event-log-15',
      payload: {
        schema_version: 1,
        action: 'accept_beat_sheet',
        result: 'accepted',
        summary: 'Accepted revised beat sheet',
        origin: 'workspace',
      },
    })
    store.applyRealtimeEvent({
      schema_version: 1,
      event_id: 'rt-16',
      type: 'chat.message',
      session_id: 'session-123',
      channel: 'session:session-123',
      actor: {
        actor_type: 'assistant',
        actor_id: 'story-planner',
      },
      stage: 'story_setup',
      created_at: '2026-04-01T08:00:02Z',
      delivery: 'live',
      replayable: true,
      sequence_number: 16,
      event_log_entry_id: 'event-log-16',
      payload: {
        schema_version: 1,
        message_id: 'chat-16',
        message_role: 'assistant',
        content: 'The story setup stage is ready for runtime targets.',
        content_format: 'plain_text',
        source: 'chat',
      },
    })

    expect(store.getState().pendingActions).toEqual([
      {
        id: 'action-1',
        label: 'Accepted revised beat sheet',
        origin: 'ui',
        createdAt: '2026-04-01T08:00:00Z',
        correlationId: 'mutation-7',
        status: 'confirmed',
      },
    ])
    expect(store.getState().chat.messages).toEqual([
      expect.objectContaining({
        role: 'action_echo',
        body: 'Accepted revised beat sheet',
      }),
      expect.objectContaining({
        id: 'chat-16',
        role: 'assistant',
        body: 'The story setup stage is ready for runtime targets.',
      }),
    ])
  })

  it('merges job progress into the snapshot and records connection details', () => {
    const store = createSessionRuntimeStore()

    store.hydrateSessionSnapshot(buildSampleSnapshot())
    store.syncConnectionStatus({
      connectionState: 'open',
      connectionDetail: 'Subscribed to session:session-123.',
      channel: 'session:session-123',
      retryCount: 0,
      lastConnectedAt: '2026-04-01T08:11:00Z',
    })
    store.applyRealtimeEvent({
      schema_version: 1,
      event_id: 'rt-17',
      type: 'job.progress',
      session_id: 'session-123',
      channel: 'session:session-123',
      actor: {
        actor_type: 'system',
        actor_id: 'worker',
      },
      stage: 'composition',
      created_at: '2026-04-01T08:13:00Z',
      delivery: 'live',
      replayable: true,
      sequence_number: 17,
      event_log_entry_id: 'event-log-17',
      payload: {
        schema_version: 1,
        job_id: 'composition-job-1',
        job_kind: 'composition',
        status: 'in_progress',
        progress_percent: 62.5,
        current_segment_index: 3,
        total_segments: 5,
        segment_id: 'segment-3',
        message: 'Writing the harbor crossing.',
      },
    })

    expect(store.getState().eventStream).toMatchObject({
      connectionState: 'open',
      connectionDetail: 'Subscribed to session:session-123.',
      channel: 'session:session-123',
      lastConnectedAt: '2026-04-01T08:11:00Z',
      lastSequenceNumber: 17,
    })
    expect(store.getState().sessionSnapshot?.active_composition_job).toEqual({
      id: 'composition-job-1',
      status: 'in_progress',
      progress_percent: 62.5,
      current_segment_index: 3,
      updated_at: '2026-04-01T08:13:00Z',
    })
    expect(
      store
        .getState()
        .sessionSnapshot?.stage_states.find(
          (stage) => stage.stage === 'composition',
        ),
    ).toMatchObject({
      status: 'in_progress',
      detail: 'Writing the harbor crossing.',
      last_event_type: 'job.progress',
    })
  })
})
