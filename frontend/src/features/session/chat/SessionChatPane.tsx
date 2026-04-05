import type { FormEvent, KeyboardEvent } from 'react'
import { useEffect, useId, useRef, useState } from 'react'
import {
  Badge,
  Button,
  TextArea,
  type BadgeTone,
} from '../../../shared/ui/primitives.tsx'
import { LiveRegion } from '../../../shared/ui/a11y.tsx'
import { FeedbackBanner, InlineSpinner } from '../../../shared/ui/feedback.tsx'
import {
  formatSessionChatTimestamp,
  type SessionChatMessage,
  type SessionChatMessageRole,
} from './sessionChat.ts'
import type { SessionChatQuickAction } from './chatCommands.ts'

type SessionChatPaneProps = {
  activityLabel: string
  connectionLabel: string
  connectionTone: BadgeTone
  disabledReason?: string | null
  isBusy?: boolean
  messages: ReadonlyArray<SessionChatMessage>
  onConfirmPendingAction?: (actionId: string) => Promise<void> | void
  onDismissPendingAction?: (actionId: string) => void
  onQuickAction?: (
    commandId: SessionChatQuickAction['commandId'],
  ) => Promise<void> | void
  onSubmit: (message: string) => Promise<void> | void
  pendingConfirmations?: ReadonlyArray<{
    id: string
    title: string
    summary: string
  }>
  quickActions?: ReadonlyArray<SessionChatQuickAction>
  slashCommandHint?: string | null
  windowKey?: string
}

type MessageRoleCopy = {
  badgeTone: BadgeTone
  label: string
}

const autoScrollThresholdPx = 80
const defaultVisibleMessageCount = 80
const visibleMessageStep = 80

function getMessageRoleCopy(role: SessionChatMessageRole): MessageRoleCopy {
  if (role === 'assistant') {
    return {
      badgeTone: 'success',
      label: 'Assistant',
    }
  }

  if (role === 'user') {
    return {
      badgeTone: 'accent',
      label: 'You',
    }
  }

  if (role === 'action_echo') {
    return {
      badgeTone: 'brand',
      label: 'Action echo',
    }
  }

  return {
    badgeTone: 'neutral',
    label: 'System',
  }
}

function getComposerHint({
  disabledReason,
  isBusy,
  isSubmitting,
  slashCommandHint,
}: {
  disabledReason?: string | null
  isBusy: boolean
  isSubmitting: boolean
  slashCommandHint?: string | null
}) {
  if (disabledReason != null) {
    return disabledReason
  }

  if (isSubmitting) {
    return 'Sending your latest note into the transcript.'
  }

  if (isBusy) {
    return 'Background work is active in the workspace. Chat stays available for notes and redirects.'
  }

  if (slashCommandHint != null) {
    return `Press Enter to send. Press Shift+Enter for a new line. Try ${slashCommandHint}.`
  }

  return 'Press Enter to send. Press Shift+Enter for a new line.'
}

export function SessionChatPane({
  activityLabel,
  connectionLabel,
  connectionTone,
  disabledReason = null,
  isBusy = false,
  messages,
  onConfirmPendingAction,
  onDismissPendingAction,
  onQuickAction,
  onSubmit,
  pendingConfirmations = [],
  quickActions = [],
  slashCommandHint = null,
  windowKey,
}: SessionChatPaneProps) {
  const transcriptRef = useRef<HTMLOListElement | null>(null)
  const shouldStickToBottomRef = useRef(true)
  const [draft, setDraft] = useState('')
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [submissionError, setSubmissionError] = useState<string | null>(null)
  const [visibleMessageCount, setVisibleMessageCount] = useState(
    defaultVisibleMessageCount,
  )
  const chatHeadingId = useId()
  const activityId = useId()
  const pendingHeadingId = useId()

  useEffect(() => {
    setVisibleMessageCount(defaultVisibleMessageCount)
  }, [windowKey])

  useEffect(() => {
    const transcript = transcriptRef.current

    if (transcript == null || !shouldStickToBottomRef.current) {
      return
    }

    transcript.scrollTop = transcript.scrollHeight
  }, [messages.length])

  function updateStickiness() {
    const transcript = transcriptRef.current

    if (transcript == null) {
      return
    }

    const distanceFromBottom =
      transcript.scrollHeight - transcript.scrollTop - transcript.clientHeight

    shouldStickToBottomRef.current = distanceFromBottom <= autoScrollThresholdPx
  }

  function handleComposerKeyDown(event: KeyboardEvent<HTMLTextAreaElement>) {
    if (
      event.key === 'Enter' &&
      !event.shiftKey &&
      !event.nativeEvent.isComposing
    ) {
      event.preventDefault()
      void submitDraft()
    }
  }

  async function submitDraft() {
    const nextDraft = draft.trim()

    if (nextDraft.length === 0 || isSubmitting || disabledReason != null) {
      return
    }

    setSubmissionError(null)
    setIsSubmitting(true)

    try {
      await onSubmit(nextDraft)
      setDraft('')
      shouldStickToBottomRef.current = true
    } catch (error) {
      setSubmissionError(
        error instanceof Error
          ? error.message
          : 'The message could not be added to the chat transcript.',
      )
    } finally {
      setIsSubmitting(false)
    }
  }

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    await submitDraft()
  }

  async function runQuickAction(
    commandId: SessionChatQuickAction['commandId'],
  ) {
    if (isSubmitting || disabledReason != null || onQuickAction == null) {
      return
    }

    setSubmissionError(null)
    setIsSubmitting(true)

    try {
      await onQuickAction(commandId)
      shouldStickToBottomRef.current = true
    } catch (error) {
      setSubmissionError(
        error instanceof Error
          ? error.message
          : 'The quick action could not be added to the chat transcript.',
      )
    } finally {
      setIsSubmitting(false)
    }
  }

  async function runPendingConfirmation(actionId: string) {
    if (
      isSubmitting ||
      disabledReason != null ||
      onConfirmPendingAction == null
    ) {
      return
    }

    setSubmissionError(null)
    setIsSubmitting(true)

    try {
      await onConfirmPendingAction(actionId)
      shouldStickToBottomRef.current = true
    } catch (error) {
      setSubmissionError(
        error instanceof Error
          ? error.message
          : 'The chat-requested change could not be confirmed right now.',
      )
    } finally {
      setIsSubmitting(false)
    }
  }

  const composerHint = getComposerHint({
    disabledReason,
    isBusy,
    isSubmitting,
    slashCommandHint,
  })
  const composerIsDisabled = disabledReason != null || isSubmitting
  const hiddenMessageCount = Math.max(0, messages.length - visibleMessageCount)
  const visibleMessages =
    hiddenMessageCount > 0 ? messages.slice(-visibleMessageCount) : messages
  const pendingConfirmationAnnouncement =
    pendingConfirmations.length > 0
      ? `${pendingConfirmations.length} chat-requested change${pendingConfirmations.length === 1 ? '' : 's'} waiting for confirmation.`
      : 'All chat-requested changes have been cleared.'

  return (
    <>
      <LiveRegion
        announcementKey={pendingConfirmations.map((item) => item.id).join(',')}
        text={pendingConfirmationAnnouncement}
      />

      <div className="pane-heading workspace-chat-pane__heading">
        <div>
          <h2 id={chatHeadingId}>Chat lane</h2>
          <p className="body-copy">
            Messages, action echoes, and redirect notes stay visible beside the
            structured workflow.
          </p>
        </div>
        <Badge tone={connectionTone}>{connectionLabel}</Badge>
      </div>

      <p
        className="workspace-chat-pane__status body-copy"
        id={activityId}
        role="status"
      >
        {activityLabel}
      </p>

      {hiddenMessageCount > 0 ? (
        <div className="workspace-chat-pane__history-window">
          <p className="body-copy">
            Showing the most recent {visibleMessages.length} messages to keep
            the transcript responsive.
          </p>
          <Button
            onClick={() => {
              setVisibleMessageCount(
                (currentCount) => currentCount + visibleMessageStep,
              )
            }}
            size="compact"
            tone="ghost"
            type="button"
          >
            Show {Math.min(hiddenMessageCount, visibleMessageStep)} older
          </Button>
        </div>
      ) : null}

      <ol
        ref={transcriptRef}
        aria-describedby={activityId}
        aria-labelledby={chatHeadingId}
        aria-busy={isBusy || isSubmitting}
        aria-relevant="additions text"
        className="workspace-chat-transcript"
        onScroll={updateStickiness}
        role="log"
      >
        {visibleMessages.map((message) => {
          const roleCopy = getMessageRoleCopy(message.role)

          return (
            <li
              key={message.id}
              className={`workspace-chat-entry workspace-chat-entry--${message.role}`}
            >
              <article className="workspace-chat-bubble">
                <header className="workspace-chat-entry__meta">
                  <Badge tone={roleCopy.badgeTone}>{roleCopy.label}</Badge>
                  <time dateTime={message.createdAt}>
                    {formatSessionChatTimestamp(message.createdAt)}
                  </time>
                </header>
                <p>{message.body}</p>
              </article>
            </li>
          )
        })}
      </ol>

      {pendingConfirmations.length > 0 ? (
        <section
          aria-labelledby={pendingHeadingId}
          className="workspace-chat-pending"
        >
          <div className="workspace-chat-pending__header">
            <h3 id={pendingHeadingId}>Pending confirmations</h3>
            <p>
              Apply the chat-requested change once the summary looks correct.
            </p>
          </div>
          <div className="workspace-chat-pending__list">
            {pendingConfirmations.map((confirmation) => (
              <article
                key={confirmation.id}
                className="workspace-chat-pending__item"
              >
                <div className="workspace-chat-pending__copy">
                  <strong>{confirmation.title}</strong>
                  <p>{confirmation.summary}</p>
                </div>
                <div className="cta-row">
                  <Button
                    disabled={composerIsDisabled}
                    onClick={() => {
                      void runPendingConfirmation(confirmation.id)
                    }}
                    tone="primary"
                  >
                    Confirm
                  </Button>
                  <Button
                    disabled={composerIsDisabled}
                    onClick={() => {
                      onDismissPendingAction?.(confirmation.id)
                    }}
                    tone="ghost"
                  >
                    Dismiss
                  </Button>
                </div>
              </article>
            ))}
          </div>
        </section>
      ) : null}

      <form className="workspace-chat-composer" onSubmit={handleSubmit}>
        <div className="workspace-chat-composer__header">
          <div>
            <strong>Message composer</strong>
            <p className="body-copy">
              Send approvals, nudges, or revision notes without leaving the
              current workspace stage.
            </p>
          </div>
          <Badge tone={composerIsDisabled ? 'warning' : 'brand'}>
            {composerIsDisabled
              ? 'Unavailable'
              : isSubmitting
                ? 'Sending'
                : 'Ready'}
          </Badge>
        </div>

        {quickActions.length > 0 ? (
          <section
            aria-label="Quick chat actions"
            className="workspace-chat-quick-actions"
          >
            <div className="workspace-chat-quick-actions__header">
              <div>
                <strong>Quick actions</strong>
                <p className="body-copy">
                  Run a common action in one tap, or type the slash version.
                </p>
              </div>
              <Badge tone="neutral">Commands</Badge>
            </div>

            <div className="workspace-chat-quick-actions__list">
              {quickActions.map((action) => (
                <Button
                  key={action.commandId}
                  size="compact"
                  title={`${action.description} (${action.slashCommand})`}
                  tone="ghost"
                  disabled={composerIsDisabled}
                  onClick={() => {
                    void runQuickAction(action.commandId)
                  }}
                >
                  {action.label}
                </Button>
              ))}
            </div>

            {slashCommandHint != null ? (
              <p className="workspace-chat-quick-actions__hint body-copy">
                Slash commands: {slashCommandHint}
              </p>
            ) : null}
          </section>
        ) : null}

        <TextArea
          description={composerHint}
          disabled={composerIsDisabled}
          hideLabel
          label="Message composer"
          maxLength={1200}
          name="chat-message"
          onChange={(event) => {
            setDraft(event.target.value)
            if (submissionError != null) {
              setSubmissionError(null)
            }
          }}
          onKeyDown={handleComposerKeyDown}
          placeholder="Guide the story, approve a choice, or leave a note for the next pass."
          rows={4}
          value={draft}
        />

        {submissionError != null ? (
          <FeedbackBanner
            description="The draft is still in the composer, so you can adjust it and retry without losing the note."
            title={submissionError}
            tone="warning"
          />
        ) : null}

        <div className="workspace-chat-composer__footer">
          <p className="body-copy">{draft.trim().length}/1200 characters</p>
          <Button
            size="compact"
            type="submit"
            disabled={composerIsDisabled || draft.trim().length === 0}
          >
            {isSubmitting ? (
              <>
                <InlineSpinner label="Sending message" />
                Sending...
              </>
            ) : (
              'Send message'
            )}
          </Button>
        </div>
      </form>
    </>
  )
}
