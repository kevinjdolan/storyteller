import type { WorkflowStageId } from './workflowStages.ts'
import type { SessionChatMessage } from './chat/sessionChat.ts'

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

export type SessionFeedConnectionState =
  | 'idle'
  | 'connecting'
  | 'open'
  | 'reconnecting'
  | 'closed'
  | 'error'

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
  lastEventId: string | null
  lastSequenceNumber: number | null
  events: SessionFeedEvent[]
}

export type SessionRuntimeState = {
  chat: {
    messages: SessionChatMessage[]
  }
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
  replaceChatMessages: (messages: SessionChatMessage[]) => void
  appendChatMessage: (message: SessionChatMessage) => void
  enqueuePendingAction: (action: PendingSessionActionInput) => void
  resolvePendingAction: (options: {
    actionId?: string
    correlationId?: string | null
    status: Exclude<PendingSessionActionStatus, 'pending'>
  }) => void
  removePendingAction: (actionId: string) => void
  appendLiveEvent: (event: SessionFeedEvent) => void
  setConnectionState: (connectionState: SessionFeedConnectionState) => void
  reset: () => void
}

const maxBufferedLiveEvents = 50
const maxBufferedChatMessages = 200

export function createInitialSessionRuntimeState(): SessionRuntimeState {
  return {
    chat: {
      messages: [],
    },
    pendingActions: [],
    eventStream: {
      connectionState: 'idle',
      lastEventId: null,
      lastSequenceNumber: null,
      events: [],
    },
  }
}

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
    appendLiveEvent: (event) => {
      const nextEvents = [...state.eventStream.events, event].slice(
        -maxBufferedLiveEvents,
      )

      setState({
        ...state,
        pendingActions:
          event.correlationId != null
            ? state.pendingActions.map((action) =>
                action.correlationId === event.correlationId
                  ? {
                      ...action,
                      status: 'confirmed',
                    }
                  : action,
              )
            : state.pendingActions,
        eventStream: {
          ...state.eventStream,
          lastEventId: event.eventId,
          lastSequenceNumber:
            event.sequenceNumber ?? state.eventStream.lastSequenceNumber,
          events: nextEvents,
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
