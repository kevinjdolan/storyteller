import type { FormEvent, KeyboardEvent } from 'react'
import { useEffect, useRef, useState } from 'react'
import {
  Badge,
  Button,
  TextArea,
  type BadgeTone,
} from '../../../shared/ui/primitives.tsx'
import { FeedbackBanner, InlineSpinner } from '../../../shared/ui/feedback.tsx'
import {
  formatSessionChatTimestamp,
  type SessionChatMessage,
  type SessionChatMessageRole,
} from './sessionChat.ts'

type SessionChatPaneProps = {
  activityLabel: string
  connectionLabel: string
  connectionTone: BadgeTone
  disabledReason?: string | null
  isBusy?: boolean
  messages: ReadonlyArray<SessionChatMessage>
  onSubmit: (message: string) => Promise<void> | void
}

type MessageRoleCopy = {
  badgeTone: BadgeTone
  label: string
}

const autoScrollThresholdPx = 80

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
}: {
  disabledReason?: string | null
  isBusy: boolean
  isSubmitting: boolean
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

  return 'Press Enter to send. Press Shift+Enter for a new line.'
}

export function SessionChatPane({
  activityLabel,
  connectionLabel,
  connectionTone,
  disabledReason = null,
  isBusy = false,
  messages,
  onSubmit,
}: SessionChatPaneProps) {
  const transcriptRef = useRef<HTMLOListElement | null>(null)
  const shouldStickToBottomRef = useRef(true)
  const [draft, setDraft] = useState('')
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [submissionError, setSubmissionError] = useState<string | null>(null)

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

  const composerHint = getComposerHint({
    disabledReason,
    isBusy,
    isSubmitting,
  })
  const composerIsDisabled = disabledReason != null || isSubmitting

  return (
    <>
      <div className="pane-heading workspace-chat-pane__heading">
        <div>
          <h2>Chat lane</h2>
          <p className="body-copy">
            Messages, action echoes, and redirect notes stay visible beside the
            structured workflow.
          </p>
        </div>
        <Badge tone={connectionTone}>{connectionLabel}</Badge>
      </div>

      <p className="workspace-chat-pane__status body-copy">{activityLabel}</p>

      <ol
        ref={transcriptRef}
        aria-busy={isBusy || isSubmitting}
        aria-live="polite"
        aria-relevant="additions text"
        className="workspace-chat-transcript"
        onScroll={updateStickiness}
        role="log"
      >
        {messages.map((message) => {
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
