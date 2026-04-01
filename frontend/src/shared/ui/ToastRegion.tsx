import type { AppShellToast } from '../../state/appShellStore.ts'
import { dismissAppShellToast } from '../../state/appShellStore.ts'
import { Badge } from './primitives.tsx'
import { ToastDismissButton } from './feedback.tsx'

type ToastRegionProps = {
  toasts: ReadonlyArray<AppShellToast>
}

function getToastTone(tone: AppShellToast['tone']) {
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

export function ToastRegion({ toasts }: ToastRegionProps) {
  if (toasts.length === 0) {
    return null
  }

  return (
    <section aria-label="Notifications" className="toast-region" role="region">
      <ol
        aria-atomic="false"
        aria-live="polite"
        aria-relevant="additions removals"
        className="toast-region__list"
      >
        {toasts.map((toast) => (
          <li
            key={toast.id}
            className={`toast-region__item toast-region__item--${toast.tone}`}
          >
            <article className="toast-card">
              <div className="toast-card__header">
                <Badge tone={getToastTone(toast.tone)}>{toast.title}</Badge>
                <ToastDismissButton
                  onClick={() => dismissAppShellToast(toast.id)}
                />
              </div>
              <p className="toast-card__body">{toast.body}</p>
            </article>
          </li>
        ))}
      </ol>
    </section>
  )
}
