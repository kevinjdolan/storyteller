import { afterEach, describe, expect, it, vi } from 'vitest'
import { createSessionRealtimeClient } from './sessionRealtimeClient.ts'

class FakeWebSocket {
  public readonly url: string
  public onclose:
    | ((event: { code?: number; reason?: string; wasClean?: boolean }) => void)
    | null = null
  public onerror: (() => void) | null = null
  public onmessage: ((event: { data: unknown }) => void) | null = null
  public onopen: (() => void) | null = null
  public readonly sentMessages: string[] = []

  constructor(url: string) {
    this.url = url
  }

  close(code?: number, reason?: string) {
    this.onclose?.({
      code,
      reason,
      wasClean: true,
    })
  }

  send(data: string) {
    this.sentMessages.push(data)
  }

  emitClose(
    event: { code?: number; reason?: string; wasClean?: boolean } = {},
  ) {
    this.onclose?.(event)
  }

  emitMessage(message: unknown) {
    this.onmessage?.({
      data: JSON.stringify(message),
    })
  }

  emitOpen() {
    this.onopen?.()
  }
}

describe('sessionRealtimeClient', () => {
  afterEach(() => {
    vi.useRealTimers()
  })

  it('stays idle when no websocket endpoint is configured', () => {
    const statuses: string[] = []
    const client = createSessionRealtimeClient({
      resolveWebSocketUrl: () => null,
    })

    client.connect({
      sessionId: 'session-123',
      onEvent: () => {
        throw new Error('no events expected')
      },
      onConnectionStateChange: (update) => {
        statuses.push(update.connectionState)
      },
    })

    expect(statuses).toEqual(['idle'])
  })

  it('subscribes, dispatches typed events, and reconnects with the latest sequence number', () => {
    vi.useFakeTimers()

    const sockets: FakeWebSocket[] = []
    const statuses: Array<{
      channel?: string | null
      connectionState: string
      retryCount?: number
    }> = []
    const acknowledgements: string[] = []
    const events: Array<{ sequenceNumber: number | null; type: string }> = []
    let latestSequenceNumber: number | null = null

    const client = createSessionRealtimeClient({
      createTabId: () => 'tab-1',
      reconnectDelaysMs: [500],
      resolveWebSocketUrl: () => 'ws://example.test/realtime',
      socketFactory: (url) => {
        const socket = new FakeWebSocket(url)
        sockets.push(socket)
        return socket
      },
    })

    client.connect({
      sessionId: 'session-123',
      getLastSequenceNumber: () => latestSequenceNumber,
      onEvent: (event) => {
        latestSequenceNumber = event.sequence_number ?? latestSequenceNumber
        events.push({
          sequenceNumber: event.sequence_number ?? null,
          type: event.type,
        })
      },
      onSubscribed: (ack) => {
        acknowledgements.push(ack.connection_id)
      },
      onConnectionStateChange: (update) => {
        statuses.push({
          connectionState: update.connectionState,
          channel: update.channel,
          retryCount: update.retryCount,
        })
      },
    })

    expect(sockets).toHaveLength(1)
    expect(sockets[0]?.url).toBe('ws://example.test/realtime')
    expect(statuses.at(-1)).toMatchObject({
      connectionState: 'connecting',
    })

    sockets[0]?.emitOpen()

    expect(JSON.parse(sockets[0]?.sentMessages[0] ?? '{}')).toMatchObject({
      action: 'subscribe',
      session_id: 'session-123',
      tab_id: 'tab-1',
      last_sequence_number: null,
    })

    sockets[0]?.emitMessage({
      schema_version: 1,
      action: 'subscribed',
      session_id: 'session-123',
      channel: 'session:session-123',
      connection_id: 'conn-1',
      tab_id: 'tab-1',
      accepted_at: '2026-04-01T08:30:00Z',
      replay_strategy: 'delta',
      replay_from_sequence_number: 18,
      latest_sequence_number: 20,
      local_actor: {
        actor_type: 'user',
        actor_id: 'local-user',
      },
    })

    expect(statuses.at(-1)).toMatchObject({
      connectionState: 'open',
      channel: 'session:session-123',
      retryCount: 0,
    })
    expect(acknowledgements).toEqual(['conn-1'])

    sockets[0]?.emitMessage({
      schema_version: 1,
      event_id: 'rt-20',
      type: 'chat.message',
      session_id: 'session-123',
      channel: 'session:session-123',
      actor: {
        actor_type: 'assistant',
        actor_id: 'story-planner',
      },
      stage: 'story_setup',
      created_at: '2026-04-01T08:31:00Z',
      delivery: 'live',
      replayable: true,
      sequence_number: 20,
      event_log_entry_id: 'event-log-20',
      payload: {
        schema_version: 1,
        message_id: 'chat-20',
        message_role: 'assistant',
        content: 'Runtime targets are ready.',
        content_format: 'plain_text',
        source: 'chat',
      },
    })

    expect(events).toEqual([
      {
        sequenceNumber: 20,
        type: 'chat.message',
      },
    ])

    sockets[0]?.emitClose({
      code: 1_011,
      reason: 'worker restart',
      wasClean: false,
    })

    expect(statuses.at(-1)).toMatchObject({
      connectionState: 'reconnecting',
      retryCount: 1,
    })

    vi.advanceTimersByTime(500)

    expect(sockets).toHaveLength(2)
    sockets[1]?.emitOpen()

    expect(JSON.parse(sockets[1]?.sentMessages[0] ?? '{}')).toMatchObject({
      action: 'subscribe',
      session_id: 'session-123',
      tab_id: 'tab-1',
      last_sequence_number: 20,
    })
  })
})
