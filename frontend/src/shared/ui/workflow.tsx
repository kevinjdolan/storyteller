import {
  type ComponentPropsWithoutRef,
  type InputHTMLAttributes,
  type ReactNode,
  type SelectHTMLAttributes,
  useId,
} from 'react'
import { TextInput } from './primitives.tsx'

function cx(...classNames: Array<string | false | null | undefined>) {
  return classNames.filter(Boolean).join(' ')
}

type FieldDescriptorArgs = {
  'aria-describedby'?: string
  description?: ReactNode
  error?: ReactNode
  id?: string
}

function useFieldDescriptorIds({
  'aria-describedby': ariaDescribedBy,
  description,
  error,
  id,
}: FieldDescriptorArgs) {
  const generatedId = useId()
  const inputId = id ?? generatedId
  const descriptionId =
    description != null ? `${inputId}-description` : undefined
  const errorId = error != null ? `${inputId}-error` : undefined
  const describedBy = [ariaDescribedBy, descriptionId, errorId]
    .filter(Boolean)
    .join(' ')

  return {
    describedBy: describedBy || undefined,
    descriptionId,
    errorId,
    inputId,
  }
}

type FieldShellProps = {
  children: ReactNode
  className?: string
  description?: ReactNode
  descriptionId?: string
  error?: ReactNode
  errorId?: string
  hideLabel?: boolean
  inputId: string
  label: ReactNode
  labelSuffix?: ReactNode
}

function FieldShell({
  children,
  className,
  description,
  descriptionId,
  error,
  errorId,
  hideLabel = false,
  inputId,
  label,
  labelSuffix,
}: FieldShellProps) {
  return (
    <div className={cx('field', error != null && 'field--error', className)}>
      <div className="field__header">
        <label
          className={cx('field__label', hideLabel && 'visually-hidden')}
          htmlFor={inputId}
        >
          {label}
        </label>
        {labelSuffix != null ? (
          <span className="field__value">{labelSuffix}</span>
        ) : null}
      </div>
      {description != null ? (
        <p className="field__description" id={descriptionId}>
          {description}
        </p>
      ) : null}
      {children}
      {error != null ? (
        <p className="field__error" id={errorId} role="alert">
          {error}
        </p>
      ) : null}
    </div>
  )
}

export type SelectFieldOption = {
  disabled?: boolean
  label: ReactNode
  value: string
}

type SelectFieldProps = Omit<
  SelectHTMLAttributes<HTMLSelectElement>,
  'children'
> & {
  className?: string
  description?: ReactNode
  error?: ReactNode
  hideLabel?: boolean
  label: ReactNode
  options: ReadonlyArray<SelectFieldOption>
}

export function SelectField({
  'aria-describedby': ariaDescribedBy,
  className,
  description,
  error,
  hideLabel = false,
  id,
  label,
  options,
  ...props
}: SelectFieldProps) {
  const { describedBy, descriptionId, errorId, inputId } =
    useFieldDescriptorIds({
      'aria-describedby': ariaDescribedBy,
      description,
      error,
      id,
    })

  return (
    <FieldShell
      className={className}
      description={description}
      descriptionId={descriptionId}
      error={error}
      errorId={errorId}
      hideLabel={hideLabel}
      inputId={inputId}
      label={label}
    >
      <select
        aria-describedby={describedBy}
        aria-invalid={error != null || undefined}
        className="select-input"
        id={inputId}
        {...props}
      >
        {options.map((option) => (
          <option
            key={option.value}
            disabled={option.disabled}
            value={option.value}
          >
            {option.label}
          </option>
        ))}
      </select>
    </FieldShell>
  )
}

type NumberFieldProps = Omit<InputHTMLAttributes<HTMLInputElement>, 'size'> & {
  className?: string
  description?: ReactNode
  error?: ReactNode
  hideLabel?: boolean
  inputClassName?: string
  label: ReactNode
}

export function NumberField(props: NumberFieldProps) {
  return <TextInput inputMode="numeric" type="number" {...props} />
}

type SliderFieldProps = Omit<
  InputHTMLAttributes<HTMLInputElement>,
  'size' | 'type'
> & {
  className?: string
  description?: ReactNode
  error?: ReactNode
  hideLabel?: boolean
  label: ReactNode
  valueText?: ReactNode
}

export function SliderField({
  'aria-describedby': ariaDescribedBy,
  className,
  description,
  error,
  hideLabel = false,
  id,
  label,
  valueText,
  ...props
}: SliderFieldProps) {
  const { describedBy, descriptionId, errorId, inputId } =
    useFieldDescriptorIds({
      'aria-describedby': ariaDescribedBy,
      description,
      error,
      id,
    })

  return (
    <FieldShell
      className={className}
      description={description}
      descriptionId={descriptionId}
      error={error}
      errorId={errorId}
      hideLabel={hideLabel}
      inputId={inputId}
      label={label}
      labelSuffix={valueText}
    >
      <input
        aria-describedby={describedBy}
        aria-invalid={error != null || undefined}
        className="range-input"
        id={inputId}
        type="range"
        {...props}
      />
    </FieldShell>
  )
}

type ToggleFieldProps = Omit<
  InputHTMLAttributes<HTMLInputElement>,
  'size' | 'type'
> & {
  className?: string
  description?: ReactNode
  error?: ReactNode
  hideLabel?: boolean
  label: ReactNode
  stateLabel?: ReactNode
}

export function ToggleField({
  'aria-describedby': ariaDescribedBy,
  className,
  description,
  error,
  hideLabel = false,
  id,
  label,
  role = 'switch',
  stateLabel,
  ...props
}: ToggleFieldProps) {
  const { describedBy, descriptionId, errorId, inputId } =
    useFieldDescriptorIds({
      'aria-describedby': ariaDescribedBy,
      description,
      error,
      id,
    })

  return (
    <FieldShell
      className={className}
      description={description}
      descriptionId={descriptionId}
      error={error}
      errorId={errorId}
      hideLabel={hideLabel}
      inputId={inputId}
      label={label}
    >
      <div className="toggle-field">
        <p className="toggle-field__copy">
          {stateLabel ?? 'Enable for this stage.'}
        </p>
        <label className="toggle-field__switch">
          <input
            aria-describedby={describedBy}
            aria-invalid={error != null || undefined}
            className="toggle-field__input"
            id={inputId}
            role={role}
            type="checkbox"
            {...props}
          />
          <span aria-hidden="true" className="toggle-field__track">
            <span className="toggle-field__thumb" />
          </span>
        </label>
      </div>
    </FieldShell>
  )
}

type CardGridProps = ComponentPropsWithoutRef<'div'> & {
  columns?: 2 | 3
}

export function CardGrid({
  children,
  className,
  columns = 2,
  ...props
}: CardGridProps) {
  return (
    <div
      className={cx('card-grid', `card-grid--${columns}`, className)}
      {...props}
    >
      {children}
    </div>
  )
}

type SelectionCardProps = Omit<ComponentPropsWithoutRef<'article'>, 'title'> & {
  description?: ReactNode
  eyebrow?: ReactNode
  footer?: ReactNode
  leading?: ReactNode
  meta?: ReactNode
  selected?: boolean
  title: ReactNode
}

export function SelectionCard({
  children,
  className,
  description,
  eyebrow,
  footer,
  leading,
  meta,
  selected = false,
  title,
  ...props
}: SelectionCardProps) {
  return (
    <article
      className={cx(
        'selection-card',
        selected && 'selection-card--selected',
        className,
      )}
      {...props}
    >
      <header className="selection-card__header">
        {leading != null ? (
          <div className="selection-card__leading">{leading}</div>
        ) : null}
        <div className="selection-card__copy">
          {eyebrow != null ? (
            <p className="selection-card__eyebrow">{eyebrow}</p>
          ) : null}
          <h3 className="selection-card__title">{title}</h3>
          {description != null ? (
            <p className="selection-card__description">{description}</p>
          ) : null}
        </div>
        {meta != null ? (
          <div className="selection-card__meta">{meta}</div>
        ) : null}
      </header>
      {children != null ? (
        <div className="selection-card__body">{children}</div>
      ) : null}
      {footer != null ? (
        <footer className="selection-card__footer">{footer}</footer>
      ) : null}
    </article>
  )
}

type EmptyStateBlockProps = Omit<ComponentPropsWithoutRef<'div'>, 'title'> & {
  action?: ReactNode
  description: ReactNode
  title: ReactNode
}

export function EmptyStateBlock({
  action,
  className,
  description,
  title,
  ...props
}: EmptyStateBlockProps) {
  return (
    <div className={cx('empty-state-block', className)} {...props}>
      <strong className="empty-state-block__title">{title}</strong>
      <p className="empty-state-block__description">{description}</p>
      {action != null ? (
        <div className="empty-state-block__action">{action}</div>
      ) : null}
    </div>
  )
}

type InlineHelpTone = 'info' | 'warning' | 'success'

type InlineHelpProps = Omit<ComponentPropsWithoutRef<'aside'>, 'title'> & {
  title?: ReactNode
  tone?: InlineHelpTone
}

export function InlineHelp({
  children,
  className,
  title,
  tone = 'info',
  ...props
}: InlineHelpProps) {
  return (
    <aside
      className={cx('inline-help', `inline-help--${tone}`, className)}
      {...props}
    >
      {title != null ? (
        <strong className="inline-help__title">{title}</strong>
      ) : null}
      {children != null ? (
        <p className="inline-help__body">{children}</p>
      ) : null}
    </aside>
  )
}

type SummaryPanelTone = 'default' | 'accent'

type SummaryPanelProps = Omit<ComponentPropsWithoutRef<'article'>, 'title'> & {
  description?: ReactNode
  label?: ReactNode
  sticky?: boolean
  title?: ReactNode
  tone?: SummaryPanelTone
}

export function SummaryPanel({
  children,
  className,
  description,
  label,
  sticky = false,
  title,
  tone = 'default',
  ...props
}: SummaryPanelProps) {
  return (
    <article
      className={cx(
        'summary-panel',
        `summary-panel--${tone}`,
        sticky && 'summary-panel--sticky',
        className,
      )}
      {...props}
    >
      {label != null ? <p className="summary-panel__label">{label}</p> : null}
      {title != null ? <h3 className="summary-panel__title">{title}</h3> : null}
      {description != null ? (
        <p className="summary-panel__description">{description}</p>
      ) : null}
      {children != null ? (
        <div className="summary-panel__body">{children}</div>
      ) : null}
    </article>
  )
}

type SplitCardProps = Omit<ComponentPropsWithoutRef<'article'>, 'title'> & {
  aside: ReactNode
  description?: ReactNode
  eyebrow?: ReactNode
  footer?: ReactNode
  meta?: ReactNode
  selected?: boolean
  title: ReactNode
}

export function SplitCard({
  aside,
  children,
  className,
  description,
  eyebrow,
  footer,
  meta,
  selected = false,
  title,
  ...props
}: SplitCardProps) {
  return (
    <article
      className={cx(
        'split-card',
        selected && 'split-card--selected',
        className,
      )}
      {...props}
    >
      <div className="split-card__main">
        <header className="split-card__header">
          <div>
            {eyebrow != null ? (
              <p className="split-card__eyebrow">{eyebrow}</p>
            ) : null}
            <h3 className="split-card__title">{title}</h3>
            {description != null ? (
              <p className="split-card__description">{description}</p>
            ) : null}
          </div>
          {meta != null ? <div className="split-card__meta">{meta}</div> : null}
        </header>
        {children != null ? (
          <div className="split-card__body">{children}</div>
        ) : null}
        {footer != null ? (
          <footer className="split-card__footer">{footer}</footer>
        ) : null}
      </div>
      <aside className="split-card__aside">{aside}</aside>
    </article>
  )
}

export function FormColumns({
  children,
  className,
  ...props
}: ComponentPropsWithoutRef<'div'>) {
  return (
    <div className={cx('form-columns', className)} {...props}>
      {children}
    </div>
  )
}

type StickySummaryLayoutProps = ComponentPropsWithoutRef<'div'> & {
  summary: ReactNode
}

export function StickySummaryLayout({
  children,
  className,
  summary,
  ...props
}: StickySummaryLayoutProps) {
  return (
    <div className={cx('sticky-summary-layout', className)} {...props}>
      <div className="sticky-summary-layout__main">{children}</div>
      <div className="sticky-summary-layout__side">{summary}</div>
    </div>
  )
}
