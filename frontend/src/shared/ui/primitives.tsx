import {
  type ButtonHTMLAttributes,
  type ComponentPropsWithoutRef,
  type InputHTMLAttributes,
  type ReactNode,
  type TextareaHTMLAttributes,
  useId,
} from 'react'
import {
  getButtonClassName,
  type ButtonSize,
  type ButtonTone,
} from './buttonStyles.ts'

function cx(...classNames: Array<string | false | null | undefined>) {
  return classNames.filter(Boolean).join(' ')
}

type ButtonProps = ButtonHTMLAttributes<HTMLButtonElement> & {
  fullWidth?: boolean
  size?: ButtonSize
  tone?: ButtonTone
}

export function Button({
  className,
  fullWidth,
  size,
  tone,
  type = 'button',
  ...props
}: ButtonProps) {
  return (
    <button
      className={getButtonClassName({ className, fullWidth, size, tone })}
      type={type}
      {...props}
    />
  )
}

export type BadgeTone =
  | 'neutral'
  | 'brand'
  | 'accent'
  | 'success'
  | 'warning'
  | 'danger'

type BadgeProps = ComponentPropsWithoutRef<'span'> & {
  tone?: BadgeTone
}

export function Badge({ className, tone = 'neutral', ...props }: BadgeProps) {
  return (
    <span className={cx('badge', `badge--${tone}`, className)} {...props} />
  )
}

type PanelTone = 'default' | 'hero' | 'subtle'
type PanelHeadingLevel = 1 | 2 | 3 | 4 | 5 | 6

type PanelBaseProps = {
  actions?: ReactNode
  className?: string
  description?: ReactNode
  eyebrow?: ReactNode
  headingLevel?: PanelHeadingLevel
  title?: ReactNode
  tone?: PanelTone
}

type PanelArticleProps = PanelBaseProps &
  Omit<ComponentPropsWithoutRef<'article'>, 'children' | 'className'> & {
    as?: 'article'
    children?: ReactNode
  }

type PanelSectionProps = PanelBaseProps &
  Omit<ComponentPropsWithoutRef<'section'>, 'children' | 'className'> & {
    as: 'section'
    children?: ReactNode
  }

type PanelAsideProps = PanelBaseProps &
  Omit<ComponentPropsWithoutRef<'aside'>, 'children' | 'className'> & {
    as: 'aside'
    children?: ReactNode
  }

type PanelDivProps = PanelBaseProps &
  Omit<ComponentPropsWithoutRef<'div'>, 'children' | 'className'> & {
    as: 'div'
    children?: ReactNode
  }

type PanelHeaderProps = PanelBaseProps &
  Omit<ComponentPropsWithoutRef<'header'>, 'children' | 'className'> & {
    as: 'header'
    children?: ReactNode
  }

type PanelProps =
  | PanelArticleProps
  | PanelSectionProps
  | PanelAsideProps
  | PanelDivProps
  | PanelHeaderProps

export function Panel({
  actions,
  as = 'article',
  children,
  className,
  description,
  eyebrow,
  headingLevel = 2,
  title,
  tone = 'default',
  ...props
}: PanelProps) {
  const Component = as
  const HeadingTag = `h${headingLevel}` as const
  const hasHeader =
    eyebrow != null || title != null || description != null || actions != null

  return (
    <Component className={cx('panel', `panel--${tone}`, className)} {...props}>
      {hasHeader ? (
        <div className="panel__header">
          <div className="panel__copy">
            {eyebrow != null ? (
              <p className="panel__eyebrow eyebrow">{eyebrow}</p>
            ) : null}
            {title != null ? (
              <HeadingTag className="panel__title">{title}</HeadingTag>
            ) : null}
            {description != null ? (
              <div className="panel__description">{description}</div>
            ) : null}
          </div>
          {actions != null ? (
            <div className="panel__actions">{actions}</div>
          ) : null}
        </div>
      ) : null}
      {children}
    </Component>
  )
}

type ProgressBarTone = 'brand' | 'moss' | 'accent'

type ProgressBarProps = {
  'aria-label'?: string
  className?: string
  hint?: ReactNode
  label?: ReactNode
  max?: number
  tone?: ProgressBarTone
  value: number
  valueText?: ReactNode
}

function clamp(value: number, minimum: number, maximum: number) {
  return Math.min(Math.max(value, minimum), maximum)
}

export function ProgressBar({
  'aria-label': ariaLabel,
  className,
  hint,
  label,
  max = 100,
  tone = 'brand',
  value,
  valueText,
}: ProgressBarProps) {
  const safeMax = max <= 0 ? 100 : max
  const safeValue = clamp(value, 0, safeMax)
  const percentage = Math.round((safeValue / safeMax) * 100)
  const resolvedValueText = valueText ?? `${percentage}%`

  return (
    <div className={cx('progress', `progress--${tone}`, className)}>
      {label != null || valueText != null ? (
        <div className="progress__meta">
          {label != null ? (
            <span className="progress__label">{label}</span>
          ) : (
            <span />
          )}
          <span className="progress__value">{resolvedValueText}</span>
        </div>
      ) : null}
      <div
        aria-label={
          ariaLabel ?? (typeof label === 'string' ? label : 'Progress')
        }
        aria-valuemax={safeMax}
        aria-valuemin={0}
        aria-valuenow={Math.round(safeValue)}
        aria-valuetext={
          typeof resolvedValueText === 'string' ? resolvedValueText : undefined
        }
        className="progress__track"
        role="progressbar"
      >
        <span
          aria-hidden="true"
          className="progress__fill"
          style={{ width: `${percentage}%` }}
        />
      </div>
      {hint != null ? <p className="progress__hint">{hint}</p> : null}
    </div>
  )
}

type UnorderedStackedListProps = Omit<
  ComponentPropsWithoutRef<'ul'>,
  'className'
> & {
  as?: 'ul'
  className?: string
}

type OrderedStackedListProps = Omit<
  ComponentPropsWithoutRef<'ol'>,
  'className'
> & {
  as: 'ol'
  className?: string
}

type StackedListProps = UnorderedStackedListProps | OrderedStackedListProps

export function StackedList({ as, className, ...props }: StackedListProps) {
  if (as === 'ol') {
    return <ol className={cx('stacked-list', className)} {...props} />
  }

  return <ul className={cx('stacked-list', className)} {...props} />
}

type StackedListItemTone = 'default' | 'accent' | 'brand' | 'success'

type StackedListItemProps = ComponentPropsWithoutRef<'li'> & {
  tone?: StackedListItemTone
}

export function StackedListItem({
  className,
  tone = 'default',
  ...props
}: StackedListItemProps) {
  return (
    <li
      className={cx(
        'stacked-list__item',
        `stacked-list__item--${tone}`,
        className,
      )}
      {...props}
    />
  )
}

type TextInputProps = Omit<InputHTMLAttributes<HTMLInputElement>, 'size'> & {
  className?: string
  description?: ReactNode
  error?: ReactNode
  hideLabel?: boolean
  inputClassName?: string
  label: ReactNode
}

export function TextInput({
  'aria-describedby': ariaDescribedBy,
  className,
  description,
  error,
  hideLabel = false,
  id,
  inputClassName,
  label,
  ...props
}: TextInputProps) {
  const generatedId = useId()
  const inputId = id ?? generatedId
  const descriptionId =
    description != null ? `${inputId}-description` : undefined
  const errorId = error != null ? `${inputId}-error` : undefined
  const describedBy = [ariaDescribedBy, descriptionId, errorId]
    .filter(Boolean)
    .join(' ')

  return (
    <div className={cx('field', error != null && 'field--error', className)}>
      <label
        className={cx('field__label', hideLabel && 'visually-hidden')}
        htmlFor={inputId}
      >
        {label}
      </label>
      {description != null ? (
        <p className="field__description" id={descriptionId}>
          {description}
        </p>
      ) : null}
      <input
        aria-describedby={describedBy || undefined}
        aria-invalid={error != null || undefined}
        className={cx('text-input', inputClassName)}
        id={inputId}
        {...props}
      />
      {error != null ? (
        <p className="field__error" id={errorId} role="alert">
          {error}
        </p>
      ) : null}
    </div>
  )
}

type TextAreaProps = Omit<
  TextareaHTMLAttributes<HTMLTextAreaElement>,
  'rows'
> & {
  className?: string
  description?: ReactNode
  error?: ReactNode
  hideLabel?: boolean
  label: ReactNode
  rows?: number
}

export function TextArea({
  'aria-describedby': ariaDescribedBy,
  className,
  description,
  error,
  hideLabel = false,
  id,
  label,
  rows = 4,
  ...props
}: TextAreaProps) {
  const generatedId = useId()
  const inputId = id ?? generatedId
  const descriptionId =
    description != null ? `${inputId}-description` : undefined
  const errorId = error != null ? `${inputId}-error` : undefined
  const describedBy = [ariaDescribedBy, descriptionId, errorId]
    .filter(Boolean)
    .join(' ')

  return (
    <div className={cx('field', error != null && 'field--error', className)}>
      <label
        className={cx('field__label', hideLabel && 'visually-hidden')}
        htmlFor={inputId}
      >
        {label}
      </label>
      {description != null ? (
        <p className="field__description" id={descriptionId}>
          {description}
        </p>
      ) : null}
      <textarea
        aria-describedby={describedBy || undefined}
        aria-invalid={error != null || undefined}
        className="text-area"
        id={inputId}
        rows={rows}
        {...props}
      />
      {error != null ? (
        <p className="field__error" id={errorId} role="alert">
          {error}
        </p>
      ) : null}
    </div>
  )
}
