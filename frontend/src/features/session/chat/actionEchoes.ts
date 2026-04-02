import type {
  ParsedChatIntentResponse,
  SessionActionDecision,
  SessionActionPolicyEvaluationItem,
  SessionHistory,
  SessionHistoryEvent,
  SessionSnapshot,
} from '../../../api/sessions.ts'
import type { ChatToUiAction, ChatToUiActionType } from './chatToUiActions.ts'
import {
  createSessionChatMessage,
  type SessionChatMessageRole,
} from './sessionChat.ts'
import { getWorkflowStageLabel } from '../workflowStages.ts'

type JsonRecord = Record<string, unknown>

const uiPreviewActionTypes = new Set<ChatToUiActionType>([
  'navigate_to_stage',
  'open_finalize_view',
])

function isRecord(value: unknown): value is JsonRecord {
  return typeof value === 'object' && value !== null && !Array.isArray(value)
}

function readString(record: JsonRecord, key: string) {
  const value = record[key]

  return typeof value === 'string' && value.length > 0 ? value : null
}

function readBoolean(record: JsonRecord, key: string) {
  const value = record[key]

  return typeof value === 'boolean' ? value : null
}

function readNumber(record: JsonRecord, key: string) {
  const value = record[key]

  return typeof value === 'number' && Number.isFinite(value) ? value : null
}

function readStringArray(record: JsonRecord, key: string) {
  const value = record[key]

  if (!Array.isArray(value)) {
    return []
  }

  return value.filter((entry): entry is string => typeof entry === 'string')
}

function humanizeToken(value: string) {
  return value.replace(/_/g, ' ')
}

function humanizeFieldList(fields: string[]) {
  const labels = fields.map(humanizeToken)

  if (labels.length === 0) {
    return null
  }

  if (labels.length === 1) {
    return labels[0]
  }

  if (labels.length === 2) {
    return `${labels[0]} and ${labels[1]}`
  }

  return `${labels.slice(0, -1).join(', ')}, and ${labels.at(-1)}`
}

function getResumeStageLabel(snapshot?: SessionSnapshot | null) {
  if (snapshot == null) {
    return null
  }

  return getWorkflowStageLabel(snapshot.resume_stage)
}

function mapChatRole(role: string | null): SessionChatMessageRole {
  if (role === 'assistant' || role === 'user' || role === 'system') {
    return role
  }

  return 'system'
}

function buildSelectionEcho(event: SessionHistoryEvent) {
  if (!isRecord(event.payload)) {
    return event.summary
  }

  const selectionKind = readString(event.payload, 'selection_kind')
  const label =
    readString(event.payload, 'label') ??
    readString(event.payload, 'slug') ??
    readString(event.payload, 'selection_id') ??
    'selection'
  const rationale = readString(event.payload, 'rationale')
  const accepted = readBoolean(event.payload, 'accepted') ?? true

  if (!accepted) {
    return `Recorded ${humanizeToken(selectionKind ?? 'selection')} candidate: ${label}`
  }

  if (selectionKind === 'genre') {
    return `Selected genre: ${label}`
  }

  if (selectionKind === 'tone_profile') {
    return `Selected tone: ${label}`
  }

  if (selectionKind === 'pitch') {
    return rationale != null
      ? `Selected pitch: ${label}. ${rationale}`
      : `Selected pitch: ${label}`
  }

  if (selectionKind === 'character_sheet') {
    return rationale != null
      ? `Selected character sheet: ${label}. ${rationale}`
      : `Selected character sheet: ${label}`
  }

  if (selectionKind === 'beat_sheet') {
    return `Accepted beat sheet: ${label}`
  }

  if (selectionKind === 'story_setup') {
    return `Accepted story setup: ${label}`
  }

  if (selectionKind === 'plan_revision') {
    return rationale != null
      ? `Restored saved plan: ${label}. ${rationale}`
      : `Restored saved plan: ${label}`
  }

  return event.summary
}

function buildUserEditEcho(event: SessionHistoryEvent) {
  if (!isRecord(event.payload)) {
    return event.summary
  }

  const summaryText = readString(event.payload, 'summary_text')
  if (summaryText != null) {
    return summaryText
  }

  const targetKind = readString(event.payload, 'target_kind')
  const changedFields = humanizeFieldList(
    readStringArray(event.payload, 'changed_fields'),
  )
  const targetLabel =
    targetKind == null
      ? 'content'
      : humanizeToken(targetKind).replace(/\b\w/g, (match) =>
          match.toLowerCase(),
        )

  if (changedFields == null) {
    return `Updated ${targetLabel}.`
  }

  return `Updated ${targetLabel}: ${changedFields}.`
}

function buildRecordedUiActionEcho(event: SessionHistoryEvent) {
  if (!isRecord(event.payload)) {
    return event.summary
  }

  const action = readString(event.payload, 'action')
  const valueSummary = readString(event.payload, 'value_summary')

  if (action === 'navigate_to_stage') {
    return `Opened ${valueSummary ?? 'the requested stage'} in the main pane.`
  }

  if (action === 'open_finalize_view') {
    return `Opened ${valueSummary ?? 'the finalize view'}.`
  }

  if (valueSummary != null) {
    return `${humanizeToken(action ?? 'updated workspace')}: ${valueSummary}`
  }

  if (action != null) {
    return `${humanizeToken(action).replace(/\b\w/g, (match) => match.toUpperCase())}.`
  }

  return event.summary
}

function buildAiOutputEcho(event: SessionHistoryEvent) {
  if (!isRecord(event.payload)) {
    return event.summary
  }

  const outputKind = readString(event.payload, 'output_kind')
  const candidateCount = event.payload.candidate_count
  const summary = readString(event.payload, 'summary')
  const countLabel =
    typeof candidateCount === 'number' ? `${candidateCount} ` : ''

  if (outputKind === 'pitch_batch') {
    if (summary != null) {
      return `Generated ${countLabel}pitch options. ${summary}`
    }

    return `Generated ${countLabel}pitch options.`
  }

  if (outputKind === 'character_sheet') {
    if (summary != null) {
      return `Generated ${countLabel}character sheets. ${summary}`
    }

    return `Generated ${countLabel}character sheets.`
  }

  return event.summary
}

function buildJobProgressEcho(event: SessionHistoryEvent) {
  if (!isRecord(event.payload)) {
    return event.summary
  }

  const interruptionPayload = isRecord(event.payload.interruption_request)
    ? event.payload.interruption_request
    : null
  const interruptionMessage =
    interruptionPayload != null
      ? readString(interruptionPayload, 'message')
      : null
  if (interruptionMessage != null) {
    return interruptionMessage
  }

  const status = readString(event.payload, 'status')
  const progressPercent = readNumber(event.payload, 'progress_percent')
  const currentSegmentIndex = readNumber(event.payload, 'current_segment_index')
  const totalSegments = readNumber(event.payload, 'total_segments')

  if (event.event_type === 'composition.progress.recorded') {
    if (
      status === 'queued' &&
      currentSegmentIndex != null &&
      totalSegments != null
    ) {
      return progressPercent != null && progressPercent > 0
        ? `Queued writing to resume at segment ${currentSegmentIndex} of ${totalSegments}.`
        : `Queued writing from segment ${currentSegmentIndex} of ${totalSegments}.`
    }

    if (
      status === 'in_progress' &&
      currentSegmentIndex != null &&
      totalSegments != null
    ) {
      return `Writing segment ${currentSegmentIndex} of ${totalSegments}.`
    }

    if (status === 'paused' && progressPercent != null) {
      return `Writing paused at ${Math.round(progressPercent)}% complete.`
    }

    if (status === 'completed') {
      return 'Writing finished and the latest draft is ready for review.'
    }

    if (status === 'cancelled') {
      return 'Writing was cancelled.'
    }

    if (status === 'failed') {
      return 'Writing failed and needs another attempt.'
    }
  }

  if (event.event_type === 'audio.progress.recorded') {
    if (status === 'completed') {
      return 'Narration completed.'
    }

    if (progressPercent != null) {
      return `Narration ${Math.round(progressPercent)}% complete.`
    }

    if (status != null) {
      return `Narration ${humanizeToken(status)}.`
    }
  }

  return event.summary
}

function describeActionIntent(action: ChatToUiAction) {
  switch (action.action_type) {
    case 'navigate_to_stage':
      return `open ${getWorkflowStageLabel(action.target_stage)}`
    case 'open_finalize_view':
      return 'open Finalize'
    case 'select_genre':
      return 'change the genre'
    case 'select_tone':
      return 'change the tone'
    case 'update_story_brief':
      return 'update the story brief'
    case 'regenerate_pitches':
      return 'refresh the pitch options'
    case 'refine_pitch':
      return 'refine the selected pitch'
    case 'select_pitch':
      return 'change the selected pitch'
    case 'select_character_sheet':
      return 'change the character sheet'
    case 'refine_character_sheet':
      return 'refine the character sheet'
    case 'regenerate_character_sheet':
      return 'refresh the character sheet'
    case 'accept_beat_sheet':
      return 'accept the beat sheet'
    case 'refine_beat_sheet':
      return 'refine the beat sheet'
    case 'regenerate_beat_sheet':
      return 'refresh the beat sheet'
    case 'update_story_setup':
      return 'update story setup'
    case 'start_composition':
      return 'start composition'
    case 'pause_job':
      return 'pause the active job'
    case 'resume_job':
      return 'resume the paused job'
    case 'redirect_composition':
      return 'redirect composition'
    case 'update_audio_settings':
      return 'update audio settings'
    case 'start_audio_generation':
      return 'start audio generation'
    case 'download_asset':
      return 'download the export'
  }
}

function buildReasonTail(
  evaluation: SessionActionPolicyEvaluationItem,
  action: ChatToUiAction,
) {
  const primaryReason = evaluation.reasons[0]

  if (primaryReason == null) {
    return evaluation.summary
  }

  if (
    primaryReason.code === 'prerequisite_stage_incomplete' &&
    primaryReason.related_stages.length > 0
  ) {
    const stageNames = primaryReason.related_stages.map(getWorkflowStageLabel)

    if (stageNames.length === 1) {
      return `Finish ${stageNames[0]} first.`
    }

    return `Finish ${stageNames.slice(0, -1).join(', ')} and ${stageNames.at(-1)} first.`
  }

  if (
    primaryReason.code === 'confirmation_required_due_to_side_effects' &&
    evaluation.side_effects.length > 0
  ) {
    return evaluation.side_effects[0]?.message ?? primaryReason.message
  }

  if (primaryReason.code === 'action_is_noop') {
    return primaryReason.message
  }

  if (primaryReason.message.length > 0) {
    return primaryReason.message
  }

  return `${describeActionIntent(action)} is blocked right now.`
}

function buildDecisionSummary(
  decision: SessionActionDecision,
  evaluation: SessionActionPolicyEvaluationItem,
  action: ChatToUiAction,
) {
  if (
    (decision === 'accepted' || decision === 'accepted_with_side_effects') &&
    uiPreviewActionTypes.has(action.action_type)
  ) {
    return null
  }

  if (decision === 'rejected') {
    return `Couldn't ${describeActionIntent(action)} yet. ${buildReasonTail(evaluation, action)}`
  }

  if (decision === 'requires_confirmation') {
    return `Needs confirmation before it can ${describeActionIntent(action)}. ${buildReasonTail(evaluation, action)}`
  }

  if (decision === 'accepted_with_side_effects') {
    const sideEffect = evaluation.side_effects[0]?.message

    if (sideEffect != null) {
      return `Ready to ${describeActionIntent(action)}. ${sideEffect}`
    }
  }

  return `Ready to ${describeActionIntent(action)}.`
}

function buildIntentEchoMessages(
  result: ParsedChatIntentResponse,
  createdAt: string,
  idPrefix: string,
) {
  const evaluation = result.policy_evaluation

  if (evaluation == null) {
    return []
  }

  return evaluation.evaluated_actions.flatMap((item) => {
    const action = result.proposed_actions.actions[item.action_index]

    if (action == null) {
      return []
    }

    const body = buildDecisionSummary(item.decision, item, action)

    if (body == null) {
      return []
    }

    return createSessionChatMessage({
      id: `${idPrefix}-${item.action_index}`,
      role: 'action_echo',
      body,
      createdAt,
    })
  })
}

export function buildIntentActionEchoMessages(options: {
  result: ParsedChatIntentResponse
  createdAt: string
  idPrefix?: string
}) {
  return buildIntentEchoMessages(
    options.result,
    options.createdAt,
    options.idPrefix ?? `chat-intent-${options.createdAt}`,
  )
}

function buildMessagesForHistoryEvent(
  event: SessionHistoryEvent,
  snapshot?: SessionSnapshot | null,
) {
  if (event.event_type === 'session.created') {
    const resumeStage = getResumeStageLabel(snapshot)

    return [
      createSessionChatMessage({
        id: event.id,
        role: 'system',
        body:
          resumeStage == null
            ? 'Session opened.'
            : `Session opened. Resume at ${resumeStage}.`,
        createdAt: event.created_at,
      }),
    ]
  }

  if (event.event_type === 'chat.message.recorded') {
    if (!isRecord(event.payload)) {
      return []
    }

    const contentPreview = readString(event.payload, 'content_preview')

    if (contentPreview == null) {
      return []
    }

    return [
      createSessionChatMessage({
        id: event.id,
        role: mapChatRole(readString(event.payload, 'message_role')),
        body: contentPreview,
        createdAt: event.created_at,
      }),
    ]
  }

  if (event.event_type === 'selection.recorded') {
    return [
      createSessionChatMessage({
        id: event.id,
        role: 'action_echo',
        body: buildSelectionEcho(event),
        createdAt: event.created_at,
      }),
    ]
  }

  if (event.event_type === 'content.user_edit.recorded') {
    return [
      createSessionChatMessage({
        id: event.id,
        role: 'action_echo',
        body: buildUserEditEcho(event),
        createdAt: event.created_at,
      }),
    ]
  }

  if (event.event_type === 'ui.action.recorded') {
    return [
      createSessionChatMessage({
        id: event.id,
        role: 'action_echo',
        body: buildRecordedUiActionEcho(event),
        createdAt: event.created_at,
      }),
    ]
  }

  if (event.event_type === 'ai.output.recorded') {
    return [
      createSessionChatMessage({
        id: event.id,
        role: 'assistant',
        body: buildAiOutputEcho(event),
        createdAt: event.created_at,
      }),
    ]
  }

  if (
    event.event_type === 'composition.progress.recorded' ||
    event.event_type === 'audio.progress.recorded'
  ) {
    return [
      createSessionChatMessage({
        id: event.id,
        role: 'action_echo',
        body: buildJobProgressEcho(event),
        createdAt: event.created_at,
      }),
    ]
  }

  if (event.event_type === 'chat.intent.parsed') {
    if (!isRecord(event.payload)) {
      return []
    }

    const rawResult = event.payload.result

    if (!isRecord(rawResult)) {
      return []
    }

    return buildIntentEchoMessages(
      rawResult as ParsedChatIntentResponse,
      event.created_at,
      event.id,
    )
  }

  return []
}

export function buildSessionChatMessagesFromHistory(
  history: SessionHistory,
  snapshot?: SessionSnapshot | null,
) {
  if (!Array.isArray(history.events)) {
    return []
  }

  return history.events.flatMap((event) =>
    buildMessagesForHistoryEvent(event, snapshot),
  )
}
