import { resolveApiUrl } from '../../../api/client.ts'
import type { SessionFeedConnectionStatusUpdate } from './sessionFeedConnection.ts'
import {
  buildSessionSubscriptionRequest,
  parseSessionFeedMessage,
  type SessionFeedMessage,
  type SessionRealtimeEvent,
  type SessionSubscriptionAck,
} from './sessionRealtime.ts'

type WebSocketLike = {
  close: (code?: number, reason?: string) => void
  send: (data: string) => void
  onclose:
    | ((event: { code?: number; reason?: string; wasClean?: boolean }) => void)
    | null
  onerror: (() => void) | null
  onmessage: ((event: { data: unknown }) => void) | null
  onopen: (() => void) | null
}

type SessionRealtimeConnectionOptions = {
  sessionId: string
  getLastSequenceNumber?: () => number | null
  onEvent: (event: SessionRealtimeEvent) => void
  onConnectionStateChange?: (update: SessionFeedConnectionStatusUpdate) => void
}

type SessionRealtimeClientOptions = {
  createTabId?: () => string
  reconnectDelaysMs?: number[]
  resolveWebSocketUrl?: () => string | null
  socketFactory?: (url: string) => WebSocketLike | null
}

export type SessionRealtimeConnectionController = {
  disconnect: () => void
  reconnect: () => void
}

export type SessionRealtimeClient = {
  connect: (
    options: SessionRealtimeConnectionOptions,
  ) => SessionRealtimeConnectionController
}

const defaultReconnectDelaysMs = [1_000, 2_000, 5_000, 10_000]

function createOpaqueId(prefix: string) {
  if (
    typeof crypto !== 'undefined' &&
    typeof crypto.randomUUID === 'function'
  ) {
    return `${prefix}-${crypto.randomUUID()}`
  }

  return `${prefix}-${Date.now()}-${Math.round(Math.random() * 1_000)}`
}

function createBrowserWebSocket(url: string): WebSocketLike | null {
  if (typeof WebSocket === 'undefined') {
    return null
  }

  return new WebSocket(url) as unknown as WebSocketLike
}

function buildReconnectDelayLabel(delayMs: number) {
  return delayMs >= 1_000 ? `${delayMs / 1_000}s` : `${delayMs}ms`
}

function buildAckDetail(ack: SessionSubscriptionAck) {
  if (
    ack.replay_strategy === 'delta' &&
    ack.replay_from_sequence_number != null
  ) {
    return `Subscribed to ${ack.channel}. Replaying from sequence ${ack.replay_from_sequence_number}.`
  }

  if (ack.replay_strategy === 'hydrate') {
    return `Subscribed to ${ack.channel}. The workspace should refresh from the durable snapshot endpoint.`
  }

  return `Subscribed to ${ack.channel}.`
}

function buildCloseDetail(event?: {
  code?: number
  reason?: string
  wasClean?: boolean
}) {
  const pieces = ['Live feed disconnected.']

  if (event?.code != null) {
    pieces.push(`Code ${event.code}.`)
  }

  if (event?.reason) {
    pieces.push(event.reason)
  }

  if (event?.wasClean === false) {
    pieces.push('The socket closed unexpectedly.')
  }

  return pieces.join(' ')
}

function parseIncomingMessage(rawMessage: unknown): SessionFeedMessage | null {
  if (typeof rawMessage !== 'string') {
    return null
  }

  try {
    return parseSessionFeedMessage(JSON.parse(rawMessage))
  } catch {
    return null
  }
}

function resolveWebSocketBase() {
  const apiBaseUrl = resolveApiUrl('/')

  if (/^https?:\/\//.test(apiBaseUrl)) {
    return apiBaseUrl
  }

  if (typeof window !== 'undefined') {
    return new URL(apiBaseUrl, window.location.origin).toString()
  }

  return 'http://127.0.0.1/'
}

export function resolveSessionRealtimeWebSocketUrl() {
  const configuredUrl = import.meta.env.VITE_SESSION_EVENTS_WS_URL?.trim()

  if (!configuredUrl) {
    return null
  }

  const url = new URL(configuredUrl, resolveWebSocketBase())

  if (url.protocol === 'http:') {
    url.protocol = 'ws:'
  } else if (url.protocol === 'https:') {
    url.protocol = 'wss:'
  }

  return url.toString()
}

export function createSessionRealtimeClient(
  clientOptions: SessionRealtimeClientOptions = {},
): SessionRealtimeClient {
  const resolveWebSocketUrl =
    clientOptions.resolveWebSocketUrl ?? resolveSessionRealtimeWebSocketUrl
  const reconnectDelaysMs =
    clientOptions.reconnectDelaysMs ?? defaultReconnectDelaysMs
  const createTabId = clientOptions.createTabId ?? (() => createOpaqueId('tab'))
  const socketFactory =
    clientOptions.socketFactory ??
    ((url: string) => createBrowserWebSocket(url))

  return {
    connect: ({
      getLastSequenceNumber,
      onConnectionStateChange,
      onEvent,
      sessionId,
    }) => {
      let activeSocket: WebSocketLike | null = null
      let activeRetryCount = 0
      let activeRetryTimer: ReturnType<typeof setTimeout> | null = null
      let manuallyClosed = false
      let suppressReconnectOnClose = false
      let lastConnectedAt: string | null = null
      let lastKnownChannel: string | null = null
      const tabId = createTabId()

      function emitConnectionState(update: SessionFeedConnectionStatusUpdate) {
        onConnectionStateChange?.({
          retryCount: activeRetryCount,
          channel: lastKnownChannel,
          lastConnectedAt,
          ...update,
        })
      }

      function clearRetryTimer() {
        if (activeRetryTimer != null) {
          clearTimeout(activeRetryTimer)
          activeRetryTimer = null
        }
      }

      function scheduleReconnect(detail: string) {
        clearRetryTimer()

        const delayMs =
          reconnectDelaysMs[
            Math.min(activeRetryCount, reconnectDelaysMs.length - 1)
          ] ??
          defaultReconnectDelaysMs.at(-1) ??
          10_000

        activeRetryCount += 1
        emitConnectionState({
          connectionState: 'reconnecting',
          connectionDetail: `${detail} Retrying in ${buildReconnectDelayLabel(delayMs)}.`,
          retryCount: activeRetryCount,
        })

        activeRetryTimer = setTimeout(() => {
          activeRetryTimer = null
          openSocket(true)
        }, delayMs)
      }

      function handleMalformedMessage() {
        emitConnectionState({
          connectionState: 'error',
          connectionDetail:
            'Received a malformed live-update frame. Closing the socket before reconnect.',
        })
        activeSocket?.close()
      }

      function handleSocketMessage(message: SessionFeedMessage) {
        if ('action' in message) {
          activeRetryCount = 0
          lastConnectedAt = message.accepted_at
          lastKnownChannel = message.channel
          emitConnectionState({
            connectionState: 'open',
            connectionDetail: buildAckDetail(message),
            retryCount: 0,
            channel: message.channel,
            lastConnectedAt: message.accepted_at,
          })
          return
        }

        onEvent(message)
      }

      function openSocket(isReconnect: boolean) {
        clearRetryTimer()

        const webSocketUrl = resolveWebSocketUrl()

        if (webSocketUrl == null) {
          emitConnectionState({
            connectionState: 'idle',
            connectionDetail:
              'Set VITE_SESSION_EVENTS_WS_URL to enable live updates.',
          })
          return
        }

        const socket = socketFactory(webSocketUrl)

        if (socket == null) {
          emitConnectionState({
            connectionState: 'idle',
            connectionDetail: 'WebSocket is unavailable in this environment.',
          })
          return
        }

        activeSocket = socket
        emitConnectionState({
          connectionState: isReconnect ? 'reconnecting' : 'connecting',
          connectionDetail: isReconnect
            ? 'Reopening the live session feed.'
            : 'Opening the live session feed.',
        })

        socket.onopen = () => {
          const request = buildSessionSubscriptionRequest({
            sessionId,
            tabId,
            lastSequenceNumber: getLastSequenceNumber?.() ?? null,
            requestId: createOpaqueId('subscribe'),
          })

          socket.send(JSON.stringify(request))
        }

        socket.onmessage = (event) => {
          const parsedMessage = parseIncomingMessage(event.data)

          if (parsedMessage == null) {
            handleMalformedMessage()
            return
          }

          handleSocketMessage(parsedMessage)
        }

        socket.onerror = () => {
          emitConnectionState({
            connectionState: 'error',
            connectionDetail: 'The live session feed reported a socket error.',
          })
        }

        socket.onclose = (event) => {
          activeSocket = null

          if (suppressReconnectOnClose) {
            suppressReconnectOnClose = false
            return
          }

          if (manuallyClosed) {
            emitConnectionState({
              connectionState: 'closed',
              connectionDetail: 'Live updates paused for this workspace.',
            })
            return
          }

          scheduleReconnect(buildCloseDetail(event))
        }
      }

      openSocket(false)

      return {
        disconnect: () => {
          manuallyClosed = true
          clearRetryTimer()
          activeSocket?.close(1_000, 'Workspace feed closed by client.')
          activeSocket = null
        },
        reconnect: () => {
          manuallyClosed = false
          clearRetryTimer()
          if (activeSocket != null) {
            suppressReconnectOnClose = true
            activeSocket.close(1_000, 'Workspace feed reconnect requested.')
          }
          activeSocket = null
          openSocket(true)
        },
      }
    },
  }
}
