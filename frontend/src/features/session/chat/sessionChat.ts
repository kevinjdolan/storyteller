import type { SessionSnapshot } from '../../../api/sessions.ts'
import { workflowStageDefinitions } from '../workflowStages.ts'

export type SessionChatMessageRole =
  | 'assistant'
  | 'user'
  | 'system'
  | 'action_echo'

export type SessionChatMessage = {
  id: string
  role: SessionChatMessageRole
  body: string
  createdAt: string
}

type CreateSessionChatMessageInput = Omit<SessionChatMessage, 'id'> & {
  id?: string
}

const chatTimestampFormatter = new Intl.DateTimeFormat(undefined, {
  month: 'short',
  day: 'numeric',
  hour: 'numeric',
  minute: '2-digit',
})

function getStageLabel(stageId: string) {
  return (
    workflowStageDefinitions.find((stage) => stage.id === stageId)?.label ??
    stageId
  )
}

function getStageTimestamp(snapshot: SessionSnapshot, stageId: string) {
  const stage = snapshot.stage_states.find((entry) => entry.stage === stageId)

  return (
    stage?.completed_at ??
    stage?.last_event_at ??
    stage?.started_at ??
    snapshot.updated_at
  )
}

function buildGeneratedMessageId() {
  if (
    typeof crypto !== 'undefined' &&
    typeof crypto.randomUUID === 'function'
  ) {
    return crypto.randomUUID()
  }

  return `chat-${Date.now()}-${Math.round(Math.random() * 1000)}`
}

export function createSessionChatMessage({
  body,
  createdAt,
  id,
  role,
}: CreateSessionChatMessageInput): SessionChatMessage {
  return {
    id: id ?? buildGeneratedMessageId(),
    role,
    body,
    createdAt,
  }
}

export function formatSessionChatTimestamp(value: string) {
  return chatTimestampFormatter.format(new Date(value))
}

export function buildInitialSessionChatMessages(
  snapshot: SessionSnapshot,
): SessionChatMessage[] {
  const messages: SessionChatMessage[] = [
    createSessionChatMessage({
      id: 'workspace-opened',
      role: 'system',
      body: `Session opened. Resume at ${getStageLabel(snapshot.resume_stage)}.`,
      createdAt: snapshot.created_at,
    }),
  ]

  if (snapshot.selected_genre != null) {
    messages.push(
      createSessionChatMessage({
        id: 'selected-genre',
        role: 'action_echo',
        body: `Selected genre: ${snapshot.selected_genre.label}`,
        createdAt: getStageTimestamp(snapshot, 'genre'),
      }),
    )
  }

  if (snapshot.selected_tone_profile != null) {
    messages.push(
      createSessionChatMessage({
        id: 'selected-tone',
        role: 'action_echo',
        body: `Selected tone: ${snapshot.selected_tone_profile.label}`,
        createdAt: getStageTimestamp(snapshot, 'tone'),
      }),
    )
  }

  if (snapshot.story_brief?.raw_brief != null) {
    messages.push(
      createSessionChatMessage({
        id: 'story-brief',
        role: 'user',
        body: snapshot.story_brief.raw_brief,
        createdAt: getStageTimestamp(snapshot, 'brief'),
      }),
    )
  }

  const latestPitchBatch = snapshot.pitch_batches?.[0]
  if (
    snapshot.selected_pitch == null &&
    latestPitchBatch != null &&
    latestPitchBatch.candidate_count > 0
  ) {
    messages.push(
      createSessionChatMessage({
        id: 'pitch-batch-ready',
        role: 'assistant',
        body: `Pitch options ready: ${latestPitchBatch.candidate_count} candidates are waiting in the newest batch.`,
        createdAt: latestPitchBatch.created_at,
      }),
    )
  }

  if (snapshot.selected_pitch != null) {
    messages.push(
      createSessionChatMessage({
        id: 'accepted-pitch',
        role: 'assistant',
        body: `Accepted pitch: ${snapshot.selected_pitch.title}. ${snapshot.selected_pitch.logline}`,
        createdAt: getStageTimestamp(snapshot, 'pitches'),
      }),
    )
  }

  const currentStage = snapshot.stage_states.find(
    (stage) => stage.stage === snapshot.current_stage,
  )

  if (currentStage?.detail != null) {
    messages.push(
      createSessionChatMessage({
        id: 'current-stage-focus',
        role: 'assistant',
        body: `Current focus: ${currentStage.detail}`,
        createdAt:
          currentStage.last_event_at ??
          currentStage.started_at ??
          snapshot.updated_at,
      }),
    )
  }

  if (snapshot.active_composition_job != null) {
    messages.push(
      createSessionChatMessage({
        id: 'composition-progress',
        role: 'system',
        body: `Writing progress: ${Math.round(snapshot.active_composition_job.progress_percent)}% complete.`,
        createdAt: snapshot.updated_at,
      }),
    )
  } else if (snapshot.active_audio_job != null) {
    messages.push(
      createSessionChatMessage({
        id: 'audio-progress',
        role: 'system',
        body: `Audio is ${snapshot.active_audio_job.status.replace(/_/g, ' ')}.`,
        createdAt: snapshot.updated_at,
      }),
    )
  } else if (snapshot.latest_audio_job?.status === 'failed') {
    messages.push(
      createSessionChatMessage({
        id: 'audio-failed',
        role: 'system',
        body:
          snapshot.latest_audio_job.error_message ??
          snapshot.latest_audio_job.stop_reason ??
          'The most recent narration run failed.',
        createdAt: snapshot.latest_audio_job.updated_at ?? snapshot.updated_at,
      }),
    )
  } else if (snapshot.latest_composition_job?.status === 'failed') {
    messages.push(
      createSessionChatMessage({
        id: 'composition-failed',
        role: 'system',
        body:
          snapshot.latest_composition_job.error_message ??
          snapshot.latest_composition_job.stop_reason ??
          'The most recent writing run failed.',
        createdAt:
          snapshot.latest_composition_job.updated_at ?? snapshot.updated_at,
      }),
    )
  } else {
    messages.push(
      createSessionChatMessage({
        id: 'save-status',
        role: 'system',
        body: 'Latest durable save checkpoint recorded for this session.',
        createdAt: snapshot.updated_at,
      }),
    )
  }

  return messages
}

export function buildMockAssistantChatReply(
  input: string,
  snapshot: SessionSnapshot,
  createdAt: string,
) {
  const currentStageLabel = getStageLabel(snapshot.current_stage).toLowerCase()
  const compactInput = input.trim().replace(/\s+/g, ' ')

  return createSessionChatMessage({
    role: 'assistant',
    body: `Captured for ${currentStageLabel}. "${compactInput}" will stay in the transcript until the agent bridge starts applying chat requests to durable workflow actions.`,
    createdAt,
  })
}
