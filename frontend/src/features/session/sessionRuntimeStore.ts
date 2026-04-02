import type {
  SessionSnapshot,
  SessionStageStateView,
} from '../../api/sessions.ts'
import {
  type SessionFeedConnectionState,
  type SessionFeedConnectionStatusUpdate,
} from './live/sessionFeedConnection.ts'
import type { SessionRealtimeEvent } from './live/sessionRealtime.ts'
import {
  createSessionChatMessage,
  type SessionChatMessage,
} from './chat/sessionChat.ts'
import {
  getWorkflowStageLabel,
  type WorkflowStageId,
  type WorkflowStageState,
} from './workflowStages.ts'

export type PendingSessionActionStatus = 'pending' | 'confirmed' | 'failed'

export type PendingSessionAction = {
  id: string
  label: string
  origin: 'chat' | 'ui'
  createdAt: string
  correlationId?: string | null
  detail?: string | null
  status: PendingSessionActionStatus
}

export type SessionEventDelivery = 'live' | 'replay'

export type SessionFeedEvent = {
  eventId: string
  type: string
  createdAt: string
  delivery: SessionEventDelivery
  stage?: WorkflowStageId | null
  correlationId?: string | null
  sequenceNumber?: number | null
  payload: Record<string, unknown>
}

export type SessionEventStreamState = {
  connectionState: SessionFeedConnectionState
  connectionDetail: string | null
  channel: string | null
  retryCount: number
  lastConnectedAt: string | null
  lastEventId: string | null
  lastSequenceNumber: number | null
  events: SessionFeedEvent[]
}

export type SessionCompositionStreamSource = 'none' | 'snapshot' | 'live'

export type SessionCompositionStreamState = {
  jobId: string | null
  status: string | null
  currentSegmentId: string | null
  currentSegmentIndex: number | null
  totalSegments: number | null
  storyText: string
  latestPartialOutput: string
  latestSegmentSummary: string | null
  lastChunkText: string | null
  source: SessionCompositionStreamSource
  updatedAt: string | null
}

export type SessionRuntimeState = {
  sessionSnapshot: SessionSnapshot | null
  chat: {
    messages: SessionChatMessage[]
  }
  composition: SessionCompositionStreamState
  pendingActions: PendingSessionAction[]
  eventStream: SessionEventStreamState
}

type SessionRuntimeListener = () => void

type PendingSessionActionInput = Omit<PendingSessionAction, 'status'> & {
  status?: PendingSessionActionStatus
}

export type SessionRuntimeStore = {
  getState: () => SessionRuntimeState
  subscribe: (listener: SessionRuntimeListener) => () => void
  hydrateSessionSnapshot: (snapshot: SessionSnapshot) => void
  replaceChatMessages: (messages: SessionChatMessage[]) => void
  appendChatMessage: (message: SessionChatMessage) => void
  enqueuePendingAction: (action: PendingSessionActionInput) => void
  resolvePendingAction: (options: {
    actionId?: string
    correlationId?: string | null
    status: Exclude<PendingSessionActionStatus, 'pending'>
  }) => void
  removePendingAction: (actionId: string) => void
  applyRealtimeEvent: (event: SessionRealtimeEvent) => void
  syncConnectionStatus: (update: SessionFeedConnectionStatusUpdate) => void
  setConnectionState: (connectionState: SessionFeedConnectionState) => void
  reset: () => void
}

const maxBufferedLiveEvents = 50
const maxBufferedChatMessages = 200

function resolvePendingActionMatch(
  action: PendingSessionAction,
  actionId?: string,
  correlationId?: string | null,
) {
  if (actionId != null) {
    return action.id === actionId
  }

  if (correlationId != null) {
    return action.correlationId === correlationId
  }

  return false
}

function recalculateSessionProgress(stageStates: SessionStageStateView[]) {
  return {
    total_stages: stageStates.length,
    completed_stages: stageStates.filter(
      (stage) => stage.status === 'completed',
    ).length,
    in_progress_stages: stageStates.filter(
      (stage) => stage.status === 'in_progress',
    ).length,
    needs_regeneration_stages: stageStates.filter(
      (stage) => stage.status === 'needs_regeneration',
    ).length,
  }
}

function appendChatMessageIfMissing(
  messages: SessionChatMessage[],
  message: SessionChatMessage,
) {
  if (messages.some((entry) => entry.id === message.id)) {
    return messages
  }

  return [...messages, message].slice(-maxBufferedChatMessages)
}

function createInitialCompositionStreamState(): SessionCompositionStreamState {
  return {
    jobId: null,
    status: null,
    currentSegmentId: null,
    currentSegmentIndex: null,
    totalSegments: null,
    storyText: '',
    latestPartialOutput: '',
    latestSegmentSummary: null,
    lastChunkText: null,
    source: 'none',
    updatedAt: null,
  }
}

function buildCompositionStreamFromSnapshot(
  snapshot: SessionSnapshot | null,
  currentState: SessionCompositionStreamState,
): SessionCompositionStreamState {
  const compositionJob =
    snapshot?.active_composition_job ?? snapshot?.latest_composition_job ?? null

  if (compositionJob == null) {
    return createInitialCompositionStreamState()
  }

  const snapshotStoryText = compositionJob.accepted_story_so_far ?? ''
  const shouldPreserveLiveStoryText =
    currentState.jobId === compositionJob.id &&
    currentState.storyText.length > snapshotStoryText.length &&
    currentState.source === 'live'

  return {
    jobId: compositionJob.id,
    status: compositionJob.status,
    currentSegmentId: compositionJob.current_segment_id ?? null,
    currentSegmentIndex: compositionJob.current_segment_index ?? null,
    totalSegments: compositionJob.total_segments ?? null,
    storyText: shouldPreserveLiveStoryText
      ? currentState.storyText
      : snapshotStoryText,
    latestPartialOutput:
      compositionJob.latest_partial_output ??
      (shouldPreserveLiveStoryText ? currentState.latestPartialOutput : ''),
    latestSegmentSummary:
      compositionJob.latest_segment_summary ??
      (shouldPreserveLiveStoryText ? currentState.latestSegmentSummary : null),
    lastChunkText: shouldPreserveLiveStoryText ? currentState.lastChunkText : null,
    source:
      snapshotStoryText.length > 0 || compositionJob.status.length > 0
        ? 'snapshot'
        : 'none',
    updatedAt:
      compositionJob.updated_at ?? snapshot?.updated_at ?? currentState.updatedAt,
  }
}

function bufferRealtimeEvent(event: SessionRealtimeEvent): SessionFeedEvent {
  return {
    eventId: event.event_id,
    type: event.type,
    createdAt: event.created_at,
    delivery: event.delivery,
    stage: event.stage,
    correlationId: event.correlation_id,
    sequenceNumber: event.sequence_number ?? null,
    payload: event.payload as Record<string, unknown>,
  }
}

function updateStageState(
  stageState: SessionStageStateView,
  update: Partial<SessionStageStateView>,
): SessionStageStateView {
  return {
    ...stageState,
    ...update,
  }
}

function applyCompositionChunkEvent(
  composition: SessionCompositionStreamState,
  event: Extract<SessionRealtimeEvent, { type: 'composition.chunk' }>,
): SessionCompositionStreamState {
  if (event.payload.chunk_kind === 'segment_start') {
    return {
      ...composition,
      jobId: event.payload.job_id,
      currentSegmentId: event.payload.segment_id,
      currentSegmentIndex: event.payload.segment_index,
      latestPartialOutput: '',
      lastChunkText: null,
      source: 'live',
      updatedAt: event.created_at,
    }
  }

  if (event.payload.chunk_kind === 'segment_summary') {
    return {
      ...composition,
      jobId: event.payload.job_id,
      currentSegmentId: event.payload.segment_id,
      currentSegmentIndex: event.payload.segment_index,
      latestPartialOutput: '',
      latestSegmentSummary: event.payload.summary ?? composition.latestSegmentSummary,
      lastChunkText: null,
      source: 'live',
      updatedAt: event.created_at,
    }
  }

  const delta = event.payload.text ?? ''

  return {
    ...composition,
    jobId: event.payload.job_id,
    currentSegmentId: event.payload.segment_id,
    currentSegmentIndex: event.payload.segment_index,
    storyText: `${composition.storyText}${delta}`,
    latestPartialOutput: `${composition.latestPartialOutput}${delta}`,
    lastChunkText: delta,
    source: 'live',
    updatedAt: event.created_at,
  }
}

function applyWorkflowStageChangedEvent(
  snapshot: SessionSnapshot,
  event: Extract<SessionRealtimeEvent, { type: 'workflow.stage_changed' }>,
) {
  const changedStage = event.stage
  const changedStageLabel =
    changedStage == null
      ? 'another workflow step'
      : getWorkflowStageLabel(changedStage)

  const stageStates = snapshot.stage_states.map((stageState) => {
    if (changedStage != null && stageState.stage === changedStage) {
      const startedAt =
        event.payload.status === 'in_progress' ||
        event.payload.status === 'completed'
          ? (stageState.started_at ?? event.created_at)
          : stageState.started_at
      const completedAt =
        event.payload.status === 'completed'
          ? (stageState.completed_at ?? event.created_at)
          : stageState.completed_at

      return updateStageState(stageState, {
        status: event.payload.status,
        detail: event.payload.detail ?? stageState.detail,
        started_at: startedAt,
        completed_at: completedAt,
        last_event_summary:
          event.payload.detail ?? stageState.last_event_summary,
        last_event_type: event.type,
        last_event_at: event.created_at,
      })
    }

    if (event.payload.invalidated_stages.includes(stageState.stage)) {
      return updateStageState(stageState, {
        status: 'needs_regeneration',
        last_event_summary: `Marked for regeneration after ${changedStageLabel.toLowerCase()} changed.`,
        last_event_type: event.type,
        last_event_at: event.created_at,
      })
    }

    return stageState
  })

  return {
    ...snapshot,
    current_stage: event.payload.current_stage,
    resume_stage: event.payload.resume_stage,
    furthest_completed_stage: event.payload.furthest_completed_stage ?? null,
    overall_status: event.payload.overall_status,
    updated_at: event.created_at,
    progress: recalculateSessionProgress(stageStates),
    stage_states: stageStates,
  }
}

function mapJobStatusToStageState(
  status:
    | 'queued'
    | 'in_progress'
    | 'paused'
    | 'completed'
    | 'failed'
    | 'cancelled',
): WorkflowStageState {
  if (status === 'completed') {
    return 'completed'
  }

  if (status === 'failed' || status === 'cancelled') {
    return 'needs_regeneration'
  }

  return 'in_progress'
}

function isActiveJobStatus(
  status:
    | 'queued'
    | 'in_progress'
    | 'paused'
    | 'completed'
    | 'failed'
    | 'cancelled',
) {
  return status === 'queued' || status === 'in_progress' || status === 'paused'
}

function applyJobStageUpdate(
  snapshot: SessionSnapshot,
  options: {
    detail: string
    eventType: 'job.progress' | 'job.status'
    stage: WorkflowStageId
    status:
      | 'queued'
      | 'in_progress'
      | 'paused'
      | 'completed'
      | 'failed'
      | 'cancelled'
    updatedAt: string
  },
) {
  const stageStates = snapshot.stage_states.map((stageState) =>
    stageState.stage === options.stage
      ? updateStageState(stageState, {
          status: mapJobStatusToStageState(options.status),
          detail: options.detail,
          started_at:
            options.status === 'in_progress' || options.status === 'completed'
              ? (stageState.started_at ?? options.updatedAt)
              : stageState.started_at,
          completed_at:
            options.status === 'completed'
              ? (stageState.completed_at ?? options.updatedAt)
              : stageState.completed_at,
          last_event_summary: options.detail,
          last_event_type: options.eventType,
          last_event_at: options.updatedAt,
        })
      : stageState,
  )

  return {
    ...snapshot,
    updated_at: options.updatedAt,
    progress: recalculateSessionProgress(stageStates),
    stage_states: stageStates,
  }
}

function buildProgressDetail(
  event:
    | Extract<SessionRealtimeEvent, { type: 'job.progress' }>
    | Extract<SessionRealtimeEvent, { type: 'job.status' }>,
) {
  if (event.payload.job_kind === 'composition') {
    const interruptionMessage = event.payload.interruption_request?.message
    if (interruptionMessage != null && interruptionMessage.length > 0) {
      return interruptionMessage
    }
  }

  if (event.type === 'job.progress') {
    if (event.payload.message != null) {
      return event.payload.message
    }

    if (
      event.payload.job_kind === 'composition' &&
      event.payload.progress_percent != null
    ) {
      return `Writing ${Math.round(event.payload.progress_percent)}% complete.`
    }

    if (
      event.payload.job_kind === 'audio' &&
      event.payload.progress_percent != null
    ) {
      return `Narration ${Math.round(event.payload.progress_percent)}% complete.`
    }
  }

  if (event.type === 'job.status' && event.payload.error_message != null) {
    return event.payload.error_message
  }

  if (event.payload.message != null) {
    return event.payload.message
  }

  return `${event.payload.job_kind} ${event.payload.status.replace(/_/g, ' ')}.`
}

function applyJobProgressEvent(
  snapshot: SessionSnapshot,
  event:
    | Extract<SessionRealtimeEvent, { type: 'job.progress' }>
    | Extract<SessionRealtimeEvent, { type: 'job.status' }>,
) {
  const detail = buildProgressDetail(event)

  if (event.payload.job_kind === 'composition') {
    const currentProgress =
      snapshot.active_composition_job?.progress_percent ??
      snapshot.latest_composition_job?.progress_percent ??
      0
    const nextProgress =
      event.type === 'job.progress'
        ? (event.payload.progress_percent ?? currentProgress)
        : event.payload.status === 'completed'
          ? 100
          : currentProgress
    const nextInterruptionRequest =
      event.payload.interruption_request?.state === 'applied' ||
      event.payload.interruption_request?.state === 'superseded'
        ? null
        : (event.payload.interruption_request ??
          snapshot.latest_composition_job?.interruption_request ??
          snapshot.active_composition_job?.interruption_request ??
          null)
    const nextJob = {
      ...(snapshot.latest_composition_job ?? snapshot.active_composition_job),
      id: event.payload.job_id,
      status: event.payload.status,
      progress_percent: nextProgress,
      current_segment_index:
        event.payload.current_segment_index ??
        snapshot.latest_composition_job?.current_segment_index ??
        snapshot.active_composition_job?.current_segment_index ??
        null,
      interruption_request: nextInterruptionRequest,
      updated_at: event.created_at,
    }

    return applyJobStageUpdate(
      {
        ...snapshot,
        latest_composition_job: nextJob,
        active_composition_job: isActiveJobStatus(event.payload.status)
          ? nextJob
          : null,
      },
      {
        detail,
        eventType: event.type,
        stage: 'composition',
        status: event.payload.status,
        updatedAt: event.created_at,
      },
    )
  }

  const nextAudioJob = {
    ...(snapshot.latest_audio_job ?? snapshot.active_audio_job),
    id: event.payload.job_id,
    status: event.payload.status,
    voice_key:
      snapshot.latest_audio_job?.voice_key ??
      snapshot.active_audio_job?.voice_key ??
      null,
    estimated_duration_seconds:
      event.type === 'job.progress'
        ? (event.payload.estimated_duration_seconds ??
          snapshot.latest_audio_job?.estimated_duration_seconds ??
          snapshot.active_audio_job?.estimated_duration_seconds ??
          null)
        : (snapshot.latest_audio_job?.estimated_duration_seconds ??
          snapshot.active_audio_job?.estimated_duration_seconds ??
          null),
    total_segments:
      event.payload.total_segments ??
      snapshot.latest_audio_job?.total_segments ??
      snapshot.active_audio_job?.total_segments ??
      null,
    current_segment_index:
      event.payload.current_segment_index ??
      snapshot.latest_audio_job?.current_segment_index ??
      snapshot.active_audio_job?.current_segment_index ??
      null,
    updated_at: event.created_at,
  }

  return applyJobStageUpdate(
    {
      ...snapshot,
      latest_audio_job: nextAudioJob,
      active_audio_job: isActiveJobStatus(event.payload.status)
        ? nextAudioJob
        : null,
    },
    {
      detail,
      eventType: event.type,
      stage: 'audio',
      status: event.payload.status,
      updatedAt: event.created_at,
    },
  )
}

function applyCompositionJobEvent(
  composition: SessionCompositionStreamState,
  event:
    | Extract<SessionRealtimeEvent, { type: 'job.progress' }>
    | Extract<SessionRealtimeEvent, { type: 'job.status' }>,
) {
  if (event.payload.job_kind !== 'composition') {
    return composition
  }

  const isSameJob = composition.jobId === event.payload.job_id
  const segmentId =
    event.type === 'job.progress' ? event.payload.segment_id ?? null : null

  return {
    ...composition,
    jobId: event.payload.job_id,
    status: event.payload.status,
    currentSegmentId:
      segmentId ?? (isSameJob ? composition.currentSegmentId : null),
    currentSegmentIndex:
      event.payload.current_segment_index ??
      (isSameJob ? composition.currentSegmentIndex : null),
    totalSegments:
      event.payload.total_segments ??
      (isSameJob ? composition.totalSegments : null),
    latestPartialOutput: isSameJob ? composition.latestPartialOutput : '',
    latestSegmentSummary: isSameJob ? composition.latestSegmentSummary : null,
    lastChunkText: isSameJob ? composition.lastChunkText : null,
    source: isSameJob ? composition.source : 'snapshot',
    updatedAt: event.created_at,
  }
}

function applyRealtimeEventToSnapshot(
  snapshot: SessionSnapshot | null,
  event: SessionRealtimeEvent,
) {
  if (snapshot == null) {
    return snapshot
  }

  if (event.type === 'workflow.stage_changed') {
    return applyWorkflowStageChangedEvent(snapshot, event)
  }

  if (event.type === 'job.progress' || event.type === 'job.status') {
    return applyJobProgressEvent(snapshot, event)
  }

  if (event.type === 'ui.action_echo' && event.stage != null) {
    const stageStates = snapshot.stage_states.map((stageState) =>
      stageState.stage === event.stage
        ? updateStageState(stageState, {
            detail: event.payload.summary,
            last_event_summary: event.payload.summary,
            last_event_type: event.type,
            last_event_at: event.created_at,
          })
        : stageState,
    )

    return {
      ...snapshot,
      updated_at: event.created_at,
      stage_states: stageStates,
    }
  }

  if (event.replayable) {
    return {
      ...snapshot,
      updated_at: event.created_at,
    }
  }

  return snapshot
}

function shouldHydrateSnapshot(
  currentSnapshot: SessionSnapshot | null,
  nextSnapshot: SessionSnapshot,
) {
  if (currentSnapshot == null || currentSnapshot.id !== nextSnapshot.id) {
    return true
  }

  return (
    Date.parse(nextSnapshot.updated_at) >=
    Date.parse(currentSnapshot.updated_at)
  )
}

export function createInitialSessionRuntimeState(): SessionRuntimeState {
  return {
    sessionSnapshot: null,
    chat: {
      messages: [],
    },
    composition: createInitialCompositionStreamState(),
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
  }
}

export function createSessionRuntimeStore(): SessionRuntimeStore {
  let state = createInitialSessionRuntimeState()
  const listeners = new Set<SessionRuntimeListener>()

  function emitChange() {
    listeners.forEach((listener) => listener())
  }

  function setState(nextState: SessionRuntimeState) {
    state = nextState
    emitChange()
  }

  return {
    getState: () => state,
    subscribe: (listener) => {
      listeners.add(listener)

      return () => {
        listeners.delete(listener)
      }
    },
    hydrateSessionSnapshot: (snapshot) => {
      if (!shouldHydrateSnapshot(state.sessionSnapshot, snapshot)) {
        return
      }

      setState({
        ...state,
        sessionSnapshot: snapshot,
        composition: buildCompositionStreamFromSnapshot(snapshot, state.composition),
      })
    },
    replaceChatMessages: (messages) => {
      setState({
        ...state,
        chat: {
          messages: messages.slice(-maxBufferedChatMessages),
        },
      })
    },
    appendChatMessage: (message) => {
      setState({
        ...state,
        chat: {
          messages: [...state.chat.messages, message].slice(
            -maxBufferedChatMessages,
          ),
        },
      })
    },
    enqueuePendingAction: (action) => {
      setState({
        ...state,
        pendingActions: [
          ...state.pendingActions,
          {
            ...action,
            status: action.status ?? 'pending',
          },
        ],
      })
    },
    resolvePendingAction: ({ actionId, correlationId, status }) => {
      setState({
        ...state,
        pendingActions: state.pendingActions.map((action) =>
          resolvePendingActionMatch(action, actionId, correlationId)
            ? {
                ...action,
                status,
              }
            : action,
        ),
      })
    },
    removePendingAction: (actionId) => {
      setState({
        ...state,
        pendingActions: state.pendingActions.filter(
          (action) => action.id !== actionId,
        ),
      })
    },
    applyRealtimeEvent: (event) => {
      if (
        event.sequence_number != null &&
        state.eventStream.lastSequenceNumber != null &&
        event.sequence_number <= state.eventStream.lastSequenceNumber
      ) {
        return
      }

      let nextMessages = state.chat.messages

      if (event.type === 'chat.message') {
        nextMessages = appendChatMessageIfMissing(
          nextMessages,
          createSessionChatMessage({
            id: event.payload.message_id,
            role: event.payload.message_role,
            body: event.payload.content,
            createdAt: event.created_at,
          }),
        )
      } else if (event.type === 'ui.action_echo') {
        nextMessages = appendChatMessageIfMissing(
          nextMessages,
          createSessionChatMessage({
            id: event.payload.chat_message_id ?? event.event_id,
            role: 'action_echo',
            body: event.payload.summary,
            createdAt: event.created_at,
          }),
        )
      }

      const nextEvents = [
        ...state.eventStream.events,
        bufferRealtimeEvent(event),
      ].slice(-maxBufferedLiveEvents)

      setState({
        ...state,
        sessionSnapshot: applyRealtimeEventToSnapshot(
          state.sessionSnapshot,
          event,
        ),
        composition:
          event.type === 'composition.chunk'
            ? applyCompositionChunkEvent(state.composition, event)
            : event.type === 'job.progress' || event.type === 'job.status'
              ? applyCompositionJobEvent(state.composition, event)
              : state.composition,
        chat: {
          messages: nextMessages,
        },
        pendingActions:
          event.correlation_id != null
            ? state.pendingActions.map((action) =>
                action.correlationId === event.correlation_id
                  ? {
                      ...action,
                      status:
                        event.type === 'ui.action_echo' &&
                        event.payload.result === 'rejected'
                          ? 'failed'
                          : 'confirmed',
                    }
                  : action,
              )
            : state.pendingActions,
        eventStream: {
          ...state.eventStream,
          lastEventId: event.event_id,
          lastSequenceNumber:
            event.sequence_number ?? state.eventStream.lastSequenceNumber,
          events: nextEvents,
        },
      })
    },
    syncConnectionStatus: (update) => {
      setState({
        ...state,
        eventStream: {
          ...state.eventStream,
          connectionState: update.connectionState,
          connectionDetail:
            update.connectionDetail !== undefined
              ? update.connectionDetail
              : state.eventStream.connectionDetail,
          channel:
            update.channel !== undefined
              ? update.channel
              : state.eventStream.channel,
          retryCount: update.retryCount ?? state.eventStream.retryCount,
          lastConnectedAt:
            update.lastConnectedAt !== undefined
              ? update.lastConnectedAt
              : state.eventStream.lastConnectedAt,
        },
      })
    },
    setConnectionState: (connectionState) => {
      setState({
        ...state,
        eventStream: {
          ...state.eventStream,
          connectionState,
        },
      })
    },
    reset: () => {
      setState(createInitialSessionRuntimeState())
    },
  }
}
