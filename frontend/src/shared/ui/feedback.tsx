import type { ComponentPropsWithoutRef, ReactNode } from 'react'
import { Badge, Button, Panel, type BadgeTone } from './primitives.tsx'

function cx(...classNames: Array<string | false | null | undefined>) {
  return classNames.filter(Boolean).join(' ')
}

export type FeedbackTone = 'info' | 'success' | 'warning' | 'danger'

type InlineSpinnerProps = Omit<ComponentPropsWithoutRef<'span'>, 'children'> & {
  label?: string
}

export function InlineSpinner({
  className,
  label = 'Loading',
  ...props
}: InlineSpinnerProps) {
  return (
    <span
      aria-label={label}
      className={cx('inline-spinner', className)}
      role="status"
      {...props}
    >
      <span aria-hidden="true" className="inline-spinner__dot" />
      <span className="visually-hidden">{label}</span>
    </span>
  )
}

type SkeletonBlockProps = ComponentPropsWithoutRef<'div'>

export function SkeletonBlock({ className, ...props }: SkeletonBlockProps) {
  return (
    <div
      aria-hidden="true"
      className={cx('loading-block', className)}
      {...props}
    />
  )
}

function getFeedbackBadgeTone(tone: FeedbackTone): BadgeTone {
  if (tone === 'success') {
    return 'success'
  }

  if (tone === 'warning') {
    return 'warning'
  }

  if (tone === 'danger') {
    return 'danger'
  }

  return 'brand'
}

function getFeedbackToneLabel(tone: FeedbackTone) {
  if (tone === 'success') {
    return 'Resolved'
  }

  if (tone === 'warning') {
    return 'Retry available'
  }

  if (tone === 'danger') {
    return 'Needs attention'
  }

  return 'In progress'
}

type FeedbackBannerProps = {
  actions?: ReactNode
  className?: string
  description: ReactNode
  icon?: ReactNode
  title: ReactNode
  tone?: FeedbackTone
}

export function FeedbackBanner({
  actions,
  className,
  description,
  icon,
  title,
  tone = 'info',
}: FeedbackBannerProps) {
  return (
    <section
      className={cx('feedback-banner', `feedback-banner--${tone}`, className)}
      role={tone === 'danger' || tone === 'warning' ? 'alert' : 'status'}
    >
      <div className="feedback-banner__header">
        <div className="feedback-banner__title-row">
          {icon != null ? (
            <span className="feedback-banner__icon">{icon}</span>
          ) : null}
          <strong>{title}</strong>
        </div>
        <Badge tone={getFeedbackBadgeTone(tone)}>
          {getFeedbackToneLabel(tone)}
        </Badge>
      </div>
      <p className="feedback-banner__description">{description}</p>
      {actions != null ? (
        <div className="feedback-banner__actions">{actions}</div>
      ) : null}
    </section>
  )
}

type BlockingFeedbackProps = {
  actions?: ReactNode
  bannerTitle?: string
  className?: string
  description: ReactNode
  eyebrow?: ReactNode
  headingLevel?: 1 | 2 | 3 | 4 | 5 | 6
  title: string
  tone?: FeedbackTone
}

export function BlockingFeedback({
  actions,
  bannerTitle = 'What happened',
  className,
  description,
  eyebrow,
  headingLevel = 1,
  title,
  tone = 'warning',
}: BlockingFeedbackProps) {
  return (
    <Panel
      as="article"
      className={cx('blocking-feedback', className)}
      eyebrow={eyebrow}
      headingLevel={headingLevel}
      title={title}
    >
      <FeedbackBanner
        actions={actions}
        className="blocking-feedback__banner"
        description={description}
        title={bannerTitle}
        tone={tone}
      />
    </Panel>
  )
}

type ToastDismissButtonProps = {
  onClick: () => void
}

export function ToastDismissButton({ onClick }: ToastDismissButtonProps) {
  return (
    <Button
      aria-label="Dismiss notification"
      className="toast-dismiss"
      size="compact"
      tone="ghost"
      onClick={onClick}
    >
      Dismiss
    </Button>
  )
}
