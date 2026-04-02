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
        body:
          snapshot.selected_pitch.selection_rationale != null
            ? `Accepted pitch: ${snapshot.selected_pitch.title}. ${snapshot.selected_pitch.selection_rationale}`
            : `Accepted pitch: ${snapshot.selected_pitch.title}. ${snapshot.selected_pitch.logline}`,
        createdAt: getStageTimestamp(snapshot, 'pitches'),
      }),
    )
  }

  const latestCharacterBatch = snapshot.character_sheet_batches?.[0]
  if (
    snapshot.selected_character_sheet == null &&
    latestCharacterBatch != null &&
    latestCharacterBatch.candidate_count > 0
  ) {
    messages.push(
      createSessionChatMessage({
        id: 'character-batch-ready',
        role: 'assistant',
        body: `Character options ready: ${latestCharacterBatch.candidate_count} candidates are waiting in the newest batch.`,
        createdAt: latestCharacterBatch.created_at,
      }),
    )
  }

  if (snapshot.selected_character_sheet != null) {
    const selectedCharacterLabel =
      snapshot.selected_character_sheet.title ??
      snapshot.selected_character_sheet.protagonist_name ??
      'Selected character sheet'
    messages.push(
      createSessionChatMessage({
        id: 'accepted-character-sheet',
        role: 'assistant',
        body:
          snapshot.selected_character_sheet.selection_rationale != null
            ? `Selected character sheet: ${selectedCharacterLabel}. ${snapshot.selected_character_sheet.selection_rationale}`
            : `Selected character sheet: ${selectedCharacterLabel}.`,
        createdAt: getStageTimestamp(snapshot, 'characters'),
      }),
    )
  }

  if (snapshot.selected_story_outline != null) {
    const cardLabel =
      snapshot.selected_story_outline.outline_kind === 'chapter'
        ? 'chapters'
        : 'scenes'
    const latestOutlineChange =
      snapshot.selected_story_outline.last_change_summary
    messages.push(
      createSessionChatMessage({
        id: 'selected-story-outline',
        role: 'assistant',
        body:
          latestOutlineChange != null
            ? `Outline ready: ${snapshot.selected_story_outline.cards.length} ${cardLabel} are mapped to the beat sheet for drafting. ${latestOutlineChange}`
            : `Outline ready: ${snapshot.selected_story_outline.cards.length} ${cardLabel} are mapped to the beat sheet for drafting.`,
        createdAt: getStageTimestamp(snapshot, 'story_setup'),
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
        body:
          snapshot.active_composition_job.interruption_request?.message ??
          `Writing progress: ${Math.round(snapshot.active_composition_job.progress_percent)}% complete.`,
        createdAt: snapshot.updated_at,
      }),
    )
  } else if (snapshot.active_audio_job != null) {
    const progressPrefix =
      snapshot.active_audio_job.progress_percent != null
        ? `Narration ${Math.round(snapshot.active_audio_job.progress_percent)}% complete. `
        : ''
    messages.push(
      createSessionChatMessage({
        id: 'audio-progress',
        role: 'system',
        body:
          snapshot.active_audio_job.current_step ??
          `${progressPrefix}Audio is ${snapshot.active_audio_job.status.replace(/_/g, ' ')}.`,
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
