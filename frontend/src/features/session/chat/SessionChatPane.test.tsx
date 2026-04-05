import { fireEvent, render, screen, waitFor } from '@testing-library/react'
import { describe, expect, it, vi } from 'vitest'
import { SessionChatPane } from './SessionChatPane.tsx'

const sampleMessages = [
  {
    id: 'message-1',
    role: 'system',
    body: 'Session opened. Resume at Beat sheet.',
    createdAt: '2026-04-01T08:00:00Z',
  },
  {
    id: 'message-2',
    role: 'action_echo',
    body: 'Selected genre: Quest Fantasy',
    createdAt: '2026-04-01T08:01:00Z',
  },
  {
    id: 'message-3',
    role: 'assistant',
    body: 'Accepted pitch: Lanterns Over Juniper Lake.',
    createdAt: '2026-04-01T08:02:00Z',
  },
  {
    id: 'message-4',
    role: 'user',
    body: 'Please soften the midpoint.',
    createdAt: '2026-04-01T08:03:00Z',
  },
] as const

function buildLargeTranscript(count: number) {
  return Array.from({ length: count }, (_, index) => {
    const role: 'assistant' | 'user' = index % 2 === 0 ? 'assistant' : 'user'

    return {
      id: `message-${index + 1}`,
      role,
      body: `Transcript message ${index + 1}`,
      createdAt: `2026-04-01T08:${String(index % 60).padStart(2, '0')}:00Z`,
    }
  })
}

describe('SessionChatPane', () => {
  it('renders the transcript as a chat log with all supported message roles', () => {
    render(
      <SessionChatPane
        activityLabel="Ready for notes."
        connectionLabel="Live feed connected"
        connectionTone="success"
        messages={sampleMessages}
        onSubmit={() => undefined}
      />,
    )

    expect(screen.getByRole('log')).toBeInTheDocument()
    expect(
      screen.getByText('Session opened. Resume at Beat sheet.'),
    ).toBeInTheDocument()
    expect(
      screen.getByText('Selected genre: Quest Fantasy'),
    ).toBeInTheDocument()
    expect(
      screen.getByText('Accepted pitch: Lanterns Over Juniper Lake.'),
    ).toBeInTheDocument()
    expect(screen.getByText('Please soften the midpoint.')).toBeInTheDocument()
    expect(screen.getByText('Action echo')).toBeInTheDocument()
  })

  it('submits the draft with Enter and clears the composer after the callback resolves', async () => {
    let resolveSubmit: (() => void) | undefined
    const onSubmit = vi.fn(
      () =>
        new Promise<void>((resolve) => {
          resolveSubmit = resolve
        }),
    )

    render(
      <SessionChatPane
        activityLabel="Ready for notes."
        connectionLabel="Live feed connected"
        connectionTone="success"
        messages={sampleMessages}
        onSubmit={onSubmit}
      />,
    )

    const composer = screen.getByLabelText('Message composer')

    fireEvent.change(composer, {
      target: {
        value: 'Please add one calmer beat before the finale.',
      },
    })
    fireEvent.keyDown(composer, {
      key: 'Enter',
      code: 'Enter',
    })

    expect(onSubmit).toHaveBeenCalledWith(
      'Please add one calmer beat before the finale.',
    )
    expect(screen.getByRole('button', { name: /Sending/ })).toBeDisabled()

    expect(resolveSubmit).toBeDefined()
    resolveSubmit?.()

    await waitFor(() => {
      expect(composer).toHaveValue('')
    })
  })

  it('disables the composer when the pane receives a disabled reason', () => {
    render(
      <SessionChatPane
        activityLabel="Narration rendering is active."
        connectionLabel="Live feed connected"
        connectionTone="success"
        disabledReason="The composer is paused while audio generation is active."
        messages={sampleMessages}
        onSubmit={() => undefined}
      />,
    )

    const composer = screen.getByLabelText('Message composer')

    expect(composer).toBeDisabled()
    expect(
      screen.getByText(
        'The composer is paused while audio generation is active.',
      ),
    ).toBeInTheDocument()
    expect(screen.getByRole('button', { name: 'Send message' })).toBeDisabled()
  })

  it('renders pending confirmations and routes confirm and dismiss clicks', async () => {
    const onConfirmPendingAction = vi.fn(async () => undefined)
    const onDismissPendingAction = vi.fn()

    render(
      <SessionChatPane
        activityLabel="One chat-requested pitch change is waiting for review."
        connectionLabel="Live feed connected"
        connectionTone="success"
        messages={sampleMessages}
        onConfirmPendingAction={onConfirmPendingAction}
        onDismissPendingAction={onDismissPendingAction}
        onSubmit={() => undefined}
        pendingConfirmations={[
          {
            id: 'pending-1',
            title: 'Refine this pitch',
            summary:
              'Generate a targeted revision from pitch two before locking the choice.',
          },
        ]}
      />,
    )

    expect(screen.getByText('Pending confirmations')).toBeInTheDocument()
    expect(screen.getByText('Refine this pitch')).toBeInTheDocument()
    expect(
      screen.getByText(
        'Generate a targeted revision from pitch two before locking the choice.',
      ),
    ).toBeInTheDocument()

    fireEvent.click(screen.getByRole('button', { name: 'Confirm' }))

    await waitFor(() => {
      expect(onConfirmPendingAction).toHaveBeenCalledWith('pending-1')
    })

    fireEvent.click(screen.getByRole('button', { name: 'Dismiss' }))

    expect(onDismissPendingAction).toHaveBeenCalledWith('pending-1')
  })

  it('renders a recent transcript window first and can reveal older messages', () => {
    const messages = buildLargeTranscript(100)

    render(
      <SessionChatPane
        activityLabel="Ready for notes."
        connectionLabel="Live feed connected"
        connectionTone="success"
        messages={messages}
        onSubmit={() => undefined}
        windowKey="session-a"
      />,
    )

    expect(
      screen.getByText(
        'Showing the most recent 80 messages to keep the transcript responsive.',
      ),
    ).toBeInTheDocument()
    expect(screen.queryByText('Transcript message 1')).not.toBeInTheDocument()
    expect(screen.getByText('Transcript message 100')).toBeInTheDocument()

    fireEvent.click(screen.getByRole('button', { name: 'Show 20 older' }))

    expect(screen.getByText('Transcript message 1')).toBeInTheDocument()
  })
})
