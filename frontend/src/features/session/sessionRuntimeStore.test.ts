import { describe, expect, it } from 'vitest'
import {
  createInitialSessionRuntimeState,
  createSessionRuntimeStore,
} from './sessionRuntimeStore.ts'

describe('sessionRuntimeStore', () => {
  it('starts with an idle live stream and no pending actions', () => {
    expect(createInitialSessionRuntimeState()).toEqual({
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
    })
  })

  it('tracks pending actions and confirms them when a matching live event arrives', () => {
    const store = createSessionRuntimeStore()

    store.enqueuePendingAction({
      id: 'action-1',
      label: 'Accepted revised beat sheet',
      origin: 'ui',
      createdAt: '2026-04-01T08:00:00Z',
      correlationId: 'mutation-7',
    })

    store.appendLiveEvent({
      eventId: 'event-1',
      type: 'ui.action_echo',
      createdAt: '2026-04-01T08:00:01Z',
      delivery: 'live',
      correlationId: 'mutation-7',
      sequenceNumber: 19,
      payload: {
        summary: 'Accepted revised beat sheet',
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
    expect(store.getState().eventStream.lastEventId).toBe('event-1')
    expect(store.getState().eventStream.lastSequenceNumber).toBe(19)
  })

  it('tracks chat transcript messages separately from the live event buffer', () => {
    const store = createSessionRuntimeStore()

    store.appendChatMessage({
      id: 'chat-1',
      role: 'system',
      body: 'Session opened.',
      createdAt: '2026-04-01T08:00:00Z',
    })

    expect(store.getState().chat.messages).toEqual([
      {
        id: 'chat-1',
        role: 'system',
        body: 'Session opened.',
        createdAt: '2026-04-01T08:00:00Z',
      },
    ])
    expect(store.getState().eventStream.events).toEqual([])
  })

  it('updates the connection state and allows failed pending actions', () => {
    const store = createSessionRuntimeStore()

    store.enqueuePendingAction({
      id: 'action-2',
      label: 'Requested fresh pitches',
      origin: 'chat',
      createdAt: '2026-04-01T08:05:00Z',
    })
    store.setConnectionState('connecting')
    store.resolvePendingAction({
      actionId: 'action-2',
      status: 'failed',
    })

    expect(store.getState().eventStream.connectionState).toBe('connecting')
    expect(store.getState().pendingActions).toEqual([
      {
        id: 'action-2',
        label: 'Requested fresh pitches',
        origin: 'chat',
        createdAt: '2026-04-01T08:05:00Z',
        status: 'failed',
      },
    ])
  })
})
