import type { SessionChatMessageRole } from '../chat/sessionChat.ts'
import type { CompositionInterruptionRequestView } from '../../../api/sessions.ts'
import {
  type WorkflowStageId,
  type WorkflowStageState,
  isWorkflowStageId,
} from '../workflowStages.ts'

export const SESSION_REALTIME_SCHEMA_VERSION = 1
export const SESSION_CHANNEL_PREFIX = 'session:'

export type SessionEventActorType = 'user' | 'assistant' | 'system' | 'service'

export type SessionEventActor = {
  actor_type: SessionEventActorType
  actor_id: string
}

export type SessionRealtimeDeliveryMode = 'live' | 'replay'

export type SessionRealtimeReplayStrategy = 'none' | 'delta' | 'hydrate'

export type ChatContentFormat = 'plain_text' | 'markdown'

export type UIActionEchoResult = 'accepted' | 'rejected'

export type CompositionChunkKind = 'segment_start' | 'delta' | 'segment_summary'

export type SessionJobKind = 'composition' | 'audio'

export type SessionJobStatus =
  | 'queued'
  | 'in_progress'
  | 'paused'
  | 'completed'
  | 'failed'
  | 'cancelled'

export type ErrorSeverity = 'warning' | 'error'

export type SessionSubscriptionRequest = {
  schema_version: typeof SESSION_REALTIME_SCHEMA_VERSION
  action: 'subscribe'
  session_id: string
  tab_id: string
  last_sequence_number?: number | null
  request_id?: string | null
}

export type SessionSubscriptionAck = {
  schema_version: typeof SESSION_REALTIME_SCHEMA_VERSION
  action: 'subscribed'
  session_id: string
  channel: string
  connection_id: string
  tab_id: string
  accepted_at: string
  replay_strategy: SessionRealtimeReplayStrategy
  replay_from_sequence_number?: number | null
  latest_sequence_number?: number | null
  request_id?: string | null
  local_actor: SessionEventActor
}

export type ChatMessageEventPayload = {
  schema_version: typeof SESSION_REALTIME_SCHEMA_VERSION
  message_id: string
  message_role: SessionChatMessageRole
  content: string
  content_format: ChatContentFormat
  source: string
}

export type WorkflowStageChangedEventPayload = {
  schema_version: typeof SESSION_REALTIME_SCHEMA_VERSION
  previous_status?: WorkflowStageState | null
  status: WorkflowStageState
  detail?: string | null
  invalidated_stages: WorkflowStageId[]
  current_stage: WorkflowStageId
  resume_stage: WorkflowStageId
  furthest_completed_stage?: WorkflowStageId | null
  overall_status: WorkflowStageState
}

export type UIActionEchoEventPayload = {
  schema_version: typeof SESSION_REALTIME_SCHEMA_VERSION
  action: string
  result: UIActionEchoResult
  summary: string
  control_id?: string | null
  value_summary?: string | null
  origin: string
  detail?: string | null
  chat_message_id?: string | null
}

export type CompositionChunkEventPayload = {
  schema_version: typeof SESSION_REALTIME_SCHEMA_VERSION
  job_id: string
  segment_id: string
  segment_index: number
  chunk_index: number
  chunk_kind: CompositionChunkKind
  text?: string | null
  summary?: string | null
  cumulative_character_count?: number | null
  cumulative_word_count?: number | null
  is_final_chunk: boolean
}

export type JobProgressEventPayload = {
  schema_version: typeof SESSION_REALTIME_SCHEMA_VERSION
  job_id: string
  job_kind: SessionJobKind
  status: SessionJobStatus
  progress_percent?: number | null
  current_step?: string | null
  current_step_index?: number | null
  total_steps?: number | null
  completed_segments?: number | null
  current_segment_index?: number | null
  total_segments?: number | null
  segment_id?: string | null
  segment_status?: string | null
  eta_seconds?: number | null
  estimated_duration_seconds?: number | null
  latest_asset_id?: string | null
  latest_asset_kind?: string | null
  message?: string | null
  interruption_request?: CompositionInterruptionRequestView | null
}

export type JobStatusEventPayload = {
  schema_version: typeof SESSION_REALTIME_SCHEMA_VERSION
  job_id: string
  job_kind: SessionJobKind
  previous_status?: SessionJobStatus | null
  status: SessionJobStatus
  message?: string | null
  stop_reason?: string | null
  error_message?: string | null
  current_segment_index?: number | null
  total_segments?: number | null
  latest_asset_id?: string | null
  latest_asset_kind?: string | null
  interruption_request?: CompositionInterruptionRequestView | null
}

export type ErrorNotificationEventPayload = {
  schema_version: typeof SESSION_REALTIME_SCHEMA_VERSION
  code: string
  severity: ErrorSeverity
  message: string
  retryable: boolean
  detail?: string | null
  job_id?: string | null
  job_kind?: SessionJobKind | null
}

type SessionRealtimeEventBase = {
  schema_version: typeof SESSION_REALTIME_SCHEMA_VERSION
  event_id: string
  session_id: string
  channel: string
  actor: SessionEventActor
  stage?: WorkflowStageId | null
  created_at: string
  correlation_id?: string | null
}

type DurableSessionRealtimeEventBase = SessionRealtimeEventBase & {
  replayable: true
  delivery: SessionRealtimeDeliveryMode
  sequence_number: number
  event_log_entry_id: string
}

type EphemeralSessionRealtimeEventBase = SessionRealtimeEventBase & {
  replayable: false
  delivery: 'live'
  sequence_number?: null
  event_log_entry_id?: null
}

export type ChatMessageRealtimeEvent = DurableSessionRealtimeEventBase & {
  type: 'chat.message'
  payload: ChatMessageEventPayload
}

export type WorkflowStageChangedRealtimeEvent =
  DurableSessionRealtimeEventBase & {
    type: 'workflow.stage_changed'
    payload: WorkflowStageChangedEventPayload
  }

export type UIActionEchoRealtimeEvent = DurableSessionRealtimeEventBase & {
  type: 'ui.action_echo'
  payload: UIActionEchoEventPayload
}

export type CompositionChunkRealtimeEvent =
  EphemeralSessionRealtimeEventBase & {
    type: 'composition.chunk'
    stage: 'composition'
    payload: CompositionChunkEventPayload
  }

export type JobProgressRealtimeEvent = DurableSessionRealtimeEventBase & {
  type: 'job.progress'
  payload: JobProgressEventPayload
}

export type JobStatusRealtimeEvent = DurableSessionRealtimeEventBase & {
  type: 'job.status'
  payload: JobStatusEventPayload
}

export type ErrorNotificationRealtimeEvent = DurableSessionRealtimeEventBase & {
  type: 'error.notification'
  payload: ErrorNotificationEventPayload
}

export type SessionRealtimeEvent =
  | ChatMessageRealtimeEvent
  | WorkflowStageChangedRealtimeEvent
  | UIActionEchoRealtimeEvent
  | CompositionChunkRealtimeEvent
  | JobProgressRealtimeEvent
  | JobStatusRealtimeEvent
  | ErrorNotificationRealtimeEvent

export type SessionFeedMessage = SessionSubscriptionAck | SessionRealtimeEvent

type JsonRecord = Record<string, unknown>

const sessionChatRoles = ['assistant', 'user', 'system', 'action_echo'] as const
const workflowStageStates = [
  'draft',
  'in_progress',
  'completed',
  'needs_regeneration',
] as const
const realtimeReplayStrategies = ['none', 'delta', 'hydrate'] as const
const realtimeDeliveries = ['live', 'replay'] as const
const actorTypes = ['user', 'assistant', 'system', 'service'] as const
const contentFormats = ['plain_text', 'markdown'] as const
const uiActionEchoResults = ['accepted', 'rejected'] as const
const compositionChunkKinds = [
  'segment_start',
  'delta',
  'segment_summary',
] as const
const jobKinds = ['composition', 'audio'] as const
const jobStatuses = [
  'queued',
  'in_progress',
  'paused',
  'completed',
  'failed',
  'cancelled',
] as const
const errorSeverities = ['warning', 'error'] as const

function isRecord(value: unknown): value is JsonRecord {
  return typeof value === 'object' && value !== null && !Array.isArray(value)
}

function isOneOf<T extends string>(
  value: unknown,
  allowed: readonly T[],
): value is T {
  return typeof value === 'string' && allowed.includes(value as T)
}

function readRequiredString(record: JsonRecord, key: string) {
  const value = record[key]

  return typeof value === 'string' && value.length > 0 ? value : null
}

function readOptionalString(record: JsonRecord, key: string) {
  const value = record[key]

  if (value == null) {
    return null
  }

  return typeof value === 'string' ? value : null
}

function readOptionalBoolean(record: JsonRecord, key: string) {
  const value = record[key]

  if (value == null) {
    return null
  }

  return typeof value === 'boolean' ? value : null
}

function readOptionalNumber(record: JsonRecord, key: string) {
  const value = record[key]

  if (value == null) {
    return null
  }

  return typeof value === 'number' && Number.isFinite(value) ? value : null
}

function readActor(record: JsonRecord, key: string): SessionEventActor | null {
  const value = record[key]

  if (!isRecord(value)) {
    return null
  }

  const actorType = value.actor_type
  const actorId = value.actor_id

  if (!isOneOf(actorType, actorTypes) || typeof actorId !== 'string') {
    return null
  }

  return {
    actor_type: actorType,
    actor_id: actorId,
  }
}

function readStage(value: unknown): WorkflowStageId | null {
  return typeof value === 'string' && isWorkflowStageId(value) ? value : null
}

function readWorkflowStageState(value: unknown): WorkflowStageState | null {
  return isOneOf(value, workflowStageStates) ? value : null
}

function readStringArray(
  record: JsonRecord,
  key: string,
  predicate?: (value: string) => boolean,
) {
  const value = record[key]

  if (!Array.isArray(value)) {
    return null
  }

  const strings = value.filter(
    (entry): entry is string => typeof entry === 'string',
  )

  if (strings.length !== value.length) {
    return null
  }

  if (predicate != null && strings.some((entry) => !predicate(entry))) {
    return null
  }

  return strings
}

export function buildSessionChannelName(sessionId: string) {
  const normalizedSessionId = sessionId.trim()

  if (normalizedSessionId.length === 0) {
    throw new Error('sessionId must not be empty.')
  }

  return `${SESSION_CHANNEL_PREFIX}${normalizedSessionId}`
}

export function buildSessionSubscriptionRequest(options: {
  sessionId: string
  tabId: string
  lastSequenceNumber?: number | null
  requestId?: string | null
}): SessionSubscriptionRequest {
  return {
    schema_version: SESSION_REALTIME_SCHEMA_VERSION,
    action: 'subscribe',
    session_id: options.sessionId,
    tab_id: options.tabId,
    last_sequence_number: options.lastSequenceNumber ?? null,
    request_id: options.requestId ?? null,
  }
}

function parseSubscriptionAck(
  record: JsonRecord,
): SessionSubscriptionAck | null {
  if (record.action !== 'subscribed') {
    return null
  }

  const sessionId = readRequiredString(record, 'session_id')
  const channel = readRequiredString(record, 'channel')
  const connectionId = readRequiredString(record, 'connection_id')
  const tabId = readRequiredString(record, 'tab_id')
  const acceptedAt = readRequiredString(record, 'accepted_at')
  const replayStrategy = isOneOf(
    record.replay_strategy,
    realtimeReplayStrategies,
  )
    ? record.replay_strategy
    : 'none'
  const localActor = readActor(record, 'local_actor')

  if (
    sessionId == null ||
    channel == null ||
    connectionId == null ||
    tabId == null ||
    acceptedAt == null ||
    localActor == null
  ) {
    return null
  }

  if (channel !== buildSessionChannelName(sessionId)) {
    return null
  }

  return {
    schema_version: SESSION_REALTIME_SCHEMA_VERSION,
    action: 'subscribed',
    session_id: sessionId,
    channel,
    connection_id: connectionId,
    tab_id: tabId,
    accepted_at: acceptedAt,
    replay_strategy: replayStrategy,
    replay_from_sequence_number: readOptionalNumber(
      record,
      'replay_from_sequence_number',
    ),
    latest_sequence_number: readOptionalNumber(
      record,
      'latest_sequence_number',
    ),
    request_id: readOptionalString(record, 'request_id'),
    local_actor: localActor,
  }
}

function parseChatMessagePayload(
  record: JsonRecord,
): ChatMessageEventPayload | null {
  const messageId = readRequiredString(record, 'message_id')
  const messageRole = isOneOf(record.message_role, sessionChatRoles)
    ? record.message_role
    : null
  const content = readRequiredString(record, 'content')
  const contentFormat = isOneOf(record.content_format, contentFormats)
    ? record.content_format
    : 'plain_text'

  if (messageId == null || messageRole == null || content == null) {
    return null
  }

  return {
    schema_version: SESSION_REALTIME_SCHEMA_VERSION,
    message_id: messageId,
    message_role: messageRole,
    content,
    content_format: contentFormat,
    source: readOptionalString(record, 'source') ?? 'chat',
  }
}

function parseWorkflowStageChangedPayload(
  record: JsonRecord,
): WorkflowStageChangedEventPayload | null {
  const status = readWorkflowStageState(record.status)
  const currentStage = readStage(record.current_stage)
  const resumeStage = readStage(record.resume_stage)
  const overallStatus = readWorkflowStageState(record.overall_status)
  const invalidatedStages = readStringArray(
    record,
    'invalidated_stages',
    isWorkflowStageId,
  ) as WorkflowStageId[] | null
  const previousStatus =
    record.previous_status == null
      ? null
      : readWorkflowStageState(record.previous_status)
  const furthestCompletedStage =
    record.furthest_completed_stage == null
      ? null
      : readStage(record.furthest_completed_stage)

  if (
    status == null ||
    currentStage == null ||
    resumeStage == null ||
    overallStatus == null ||
    invalidatedStages == null
  ) {
    return null
  }

  return {
    schema_version: SESSION_REALTIME_SCHEMA_VERSION,
    previous_status: previousStatus,
    status,
    detail: readOptionalString(record, 'detail'),
    invalidated_stages: invalidatedStages,
    current_stage: currentStage,
    resume_stage: resumeStage,
    furthest_completed_stage: furthestCompletedStage,
    overall_status: overallStatus,
  }
}

function parseUiActionEchoPayload(
  record: JsonRecord,
): UIActionEchoEventPayload | null {
  const action = readRequiredString(record, 'action')
  const summary = readRequiredString(record, 'summary')
  const result = isOneOf(record.result, uiActionEchoResults)
    ? record.result
    : 'accepted'

  if (action == null || summary == null) {
    return null
  }

  return {
    schema_version: SESSION_REALTIME_SCHEMA_VERSION,
    action,
    result,
    summary,
    control_id: readOptionalString(record, 'control_id'),
    value_summary: readOptionalString(record, 'value_summary'),
    origin: readOptionalString(record, 'origin') ?? 'workspace',
    detail: readOptionalString(record, 'detail'),
    chat_message_id: readOptionalString(record, 'chat_message_id'),
  }
}

function parseCompositionChunkPayload(
  record: JsonRecord,
): CompositionChunkEventPayload | null {
  const jobId = readRequiredString(record, 'job_id')
  const segmentId = readRequiredString(record, 'segment_id')
  const segmentIndex = readOptionalNumber(record, 'segment_index')
  const chunkIndex = readOptionalNumber(record, 'chunk_index')
  const chunkKind = isOneOf(record.chunk_kind, compositionChunkKinds)
    ? record.chunk_kind
    : null
  const text = readOptionalString(record, 'text')
  const summary = readOptionalString(record, 'summary')

  if (
    jobId == null ||
    segmentId == null ||
    segmentIndex == null ||
    chunkIndex == null ||
    chunkKind == null
  ) {
    return null
  }

  if (chunkKind === 'delta' && (text == null || text.length === 0)) {
    return null
  }

  if (
    chunkKind === 'segment_summary' &&
    (summary == null || summary.length === 0)
  ) {
    return null
  }

  return {
    schema_version: SESSION_REALTIME_SCHEMA_VERSION,
    job_id: jobId,
    segment_id: segmentId,
    segment_index: segmentIndex,
    chunk_index: chunkIndex,
    chunk_kind: chunkKind,
    text,
    summary,
    cumulative_character_count: readOptionalNumber(
      record,
      'cumulative_character_count',
    ),
    cumulative_word_count: readOptionalNumber(record, 'cumulative_word_count'),
    is_final_chunk: readOptionalBoolean(record, 'is_final_chunk') ?? false,
  }
}

function parseCompositionInterruptionRequest(
  record: JsonRecord,
): CompositionInterruptionRequestView | null {
  const id = readRequiredString(record, 'id')
  const requestKind = readRequiredString(record, 'request_kind')
  const state = readRequiredString(record, 'state')
  const origin = readRequiredString(record, 'origin')
  const message = readRequiredString(record, 'message')
  const createdAt = readRequiredString(record, 'created_at')
  const updatedAt = readRequiredString(record, 'updated_at')

  if (
    id == null ||
    requestKind == null ||
    state == null ||
    origin == null ||
    message == null ||
    createdAt == null ||
    updatedAt == null
  ) {
    return null
  }

  return {
    id,
    request_kind: requestKind,
    state,
    origin,
    message,
    instructions: readOptionalString(record, 'instructions'),
    rewrite_from_segment_index: readOptionalNumber(
      record,
      'rewrite_from_segment_index',
    ),
    requested_status: readOptionalString(record, 'requested_status'),
    requested_segment_id: readOptionalString(record, 'requested_segment_id'),
    requested_segment_index: readOptionalNumber(record, 'requested_segment_index'),
    requested_progress_percent: readOptionalNumber(
      record,
      'requested_progress_percent',
    ),
    resolution_summary: readOptionalString(record, 'resolution_summary'),
    created_at: createdAt,
    updated_at: updatedAt,
    resolved_at: readOptionalString(record, 'resolved_at'),
  }
}

function parseJobProgressPayload(
  record: JsonRecord,
): JobProgressEventPayload | null {
  const jobId = readRequiredString(record, 'job_id')
  const jobKind = isOneOf(record.job_kind, jobKinds) ? record.job_kind : null
  const status = isOneOf(record.status, jobStatuses) ? record.status : null

  if (jobId == null || jobKind == null || status == null) {
    return null
  }

  return {
    schema_version: SESSION_REALTIME_SCHEMA_VERSION,
    job_id: jobId,
    job_kind: jobKind,
    status,
    progress_percent: readOptionalNumber(record, 'progress_percent'),
    current_step: readOptionalString(record, 'current_step'),
    current_step_index: readOptionalNumber(record, 'current_step_index'),
    total_steps: readOptionalNumber(record, 'total_steps'),
    completed_segments: readOptionalNumber(record, 'completed_segments'),
    current_segment_index: readOptionalNumber(record, 'current_segment_index'),
    total_segments: readOptionalNumber(record, 'total_segments'),
    segment_id: readOptionalString(record, 'segment_id'),
    segment_status: readOptionalString(record, 'segment_status'),
    eta_seconds: readOptionalNumber(record, 'eta_seconds'),
    estimated_duration_seconds: readOptionalNumber(
      record,
      'estimated_duration_seconds',
    ),
    latest_asset_id: readOptionalString(record, 'latest_asset_id'),
    latest_asset_kind: readOptionalString(record, 'latest_asset_kind'),
    message: readOptionalString(record, 'message'),
    interruption_request: isRecord(record.interruption_request)
      ? parseCompositionInterruptionRequest(record.interruption_request)
      : null,
  }
}

function parseJobStatusPayload(
  record: JsonRecord,
): JobStatusEventPayload | null {
  const jobId = readRequiredString(record, 'job_id')
  const jobKind = isOneOf(record.job_kind, jobKinds) ? record.job_kind : null
  const status = isOneOf(record.status, jobStatuses) ? record.status : null
  const previousStatus =
    record.previous_status == null
      ? null
      : isOneOf(record.previous_status, jobStatuses)
        ? record.previous_status
        : null

  if (jobId == null || jobKind == null || status == null) {
    return null
  }

  return {
    schema_version: SESSION_REALTIME_SCHEMA_VERSION,
    job_id: jobId,
    job_kind: jobKind,
    previous_status: previousStatus,
    status,
    message: readOptionalString(record, 'message'),
    stop_reason: readOptionalString(record, 'stop_reason'),
    error_message: readOptionalString(record, 'error_message'),
    current_segment_index: readOptionalNumber(record, 'current_segment_index'),
    total_segments: readOptionalNumber(record, 'total_segments'),
    latest_asset_id: readOptionalString(record, 'latest_asset_id'),
    latest_asset_kind: readOptionalString(record, 'latest_asset_kind'),
    interruption_request: isRecord(record.interruption_request)
      ? parseCompositionInterruptionRequest(record.interruption_request)
      : null,
  }
}

function parseErrorNotificationPayload(
  record: JsonRecord,
): ErrorNotificationEventPayload | null {
  const code = readRequiredString(record, 'code')
  const message = readRequiredString(record, 'message')
  const severity = isOneOf(record.severity, errorSeverities)
    ? record.severity
    : 'error'
  const retryable = readOptionalBoolean(record, 'retryable') ?? false
  const jobKind =
    record.job_kind == null
      ? null
      : isOneOf(record.job_kind, jobKinds)
        ? record.job_kind
        : null

  if (code == null || message == null) {
    return null
  }

  return {
    schema_version: SESSION_REALTIME_SCHEMA_VERSION,
    code,
    severity,
    message,
    retryable,
    detail: readOptionalString(record, 'detail'),
    job_id: readOptionalString(record, 'job_id'),
    job_kind: jobKind,
  }
}

function parseRealtimeEvent(record: JsonRecord): SessionRealtimeEvent | null {
  const type = readRequiredString(record, 'type')
  const sessionId = readRequiredString(record, 'session_id')
  const channel = readRequiredString(record, 'channel')
  const eventId = readRequiredString(record, 'event_id')
  const createdAt = readRequiredString(record, 'created_at')
  const actor = readActor(record, 'actor')
  const rawPayload = record.payload

  if (
    type == null ||
    sessionId == null ||
    channel == null ||
    eventId == null ||
    createdAt == null ||
    actor == null ||
    !isRecord(rawPayload)
  ) {
    return null
  }

  if (channel !== buildSessionChannelName(sessionId)) {
    return null
  }

  const stage =
    record.stage == null ? null : (readStage(record.stage) ?? undefined)
  const delivery = isOneOf(record.delivery, realtimeDeliveries)
    ? record.delivery
    : 'live'
  const correlationId = readOptionalString(record, 'correlation_id')

  if (record.stage != null && stage === undefined) {
    return null
  }

  if (type === 'composition.chunk') {
    const payload = parseCompositionChunkPayload(rawPayload)

    if (payload == null) {
      return null
    }

    return {
      schema_version: SESSION_REALTIME_SCHEMA_VERSION,
      event_id: eventId,
      type,
      session_id: sessionId,
      channel,
      actor,
      stage: 'composition',
      created_at: createdAt,
      correlation_id: correlationId,
      delivery: 'live',
      replayable: false,
      sequence_number: null,
      event_log_entry_id: null,
      payload,
    }
  }

  const sequenceNumber = readOptionalNumber(record, 'sequence_number')
  const eventLogEntryId = readRequiredString(record, 'event_log_entry_id')

  if (sequenceNumber == null || eventLogEntryId == null) {
    return null
  }

  const base = {
    schema_version: SESSION_REALTIME_SCHEMA_VERSION,
    event_id: eventId,
    session_id: sessionId,
    channel,
    actor,
    stage,
    created_at: createdAt,
    correlation_id: correlationId,
    delivery,
    replayable: true as const,
    sequence_number: sequenceNumber,
    event_log_entry_id: eventLogEntryId,
  } as const

  if (type === 'chat.message') {
    const payload = parseChatMessagePayload(rawPayload)

    return payload == null ? null : { ...base, type, payload }
  }

  if (type === 'workflow.stage_changed') {
    const payload = parseWorkflowStageChangedPayload(rawPayload)

    return payload == null ? null : { ...base, type, payload }
  }

  if (type === 'ui.action_echo') {
    const payload = parseUiActionEchoPayload(rawPayload)

    return payload == null ? null : { ...base, type, payload }
  }

  if (type === 'job.progress') {
    const payload = parseJobProgressPayload(rawPayload)

    return payload == null ? null : { ...base, type, payload }
  }

  if (type === 'job.status') {
    const payload = parseJobStatusPayload(rawPayload)

    return payload == null ? null : { ...base, type, payload }
  }

  if (type === 'error.notification') {
    const payload = parseErrorNotificationPayload(rawPayload)

    return payload == null ? null : { ...base, type, payload }
  }

  return null
}

export function parseSessionFeedMessage(
  value: unknown,
): SessionFeedMessage | null {
  if (!isRecord(value)) {
    return null
  }

  if (value.schema_version !== SESSION_REALTIME_SCHEMA_VERSION) {
    return null
  }

  return parseSubscriptionAck(value) ?? parseRealtimeEvent(value)
}
