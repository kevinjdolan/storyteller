function cx(...classNames: Array<string | false | null | undefined>) {
  return classNames.filter(Boolean).join(' ')
}

export type ButtonTone = 'primary' | 'secondary' | 'ghost'
export type ButtonSize = 'compact' | 'regular'

type ButtonClassNameOptions = {
  className?: string
  fullWidth?: boolean
  size?: ButtonSize
  tone?: ButtonTone
}

export function getButtonClassName({
  className,
  fullWidth = false,
  size = 'regular',
  tone = 'primary',
}: ButtonClassNameOptions = {}) {
  return cx(
    'button',
    `button--${tone}`,
    `button--${size}`,
    fullWidth && 'button--full-width',
    className,
  )
}
