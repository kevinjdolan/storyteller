import type { AppShellToast } from '../../state/appShellStore.ts'

type ToastRegionProps = {
  toasts: ReadonlyArray<AppShellToast>
}

export function ToastRegion({ toasts }: ToastRegionProps) {
  return (
    <section className="toast-region" aria-label="Future notification dock">
      <div className="toast-region__heading">
        <p className="eyebrow eyebrow-muted">Toasts</p>
        <span className="toast-region__count">{toasts.length}</span>
      </div>

      {toasts.length === 0 ? (
        <p className="toast-region__empty">
          Workflow notifications, export alerts, and background job updates will
          dock here.
        </p>
      ) : (
        <ul className="toast-region__list">
          {toasts.map((toast) => (
            <li
              key={toast.id}
              className={`toast-region__item toast-region__item--${toast.tone}`}
            >
              <strong>{toast.title}</strong>
              <p>{toast.body}</p>
            </li>
          ))}
        </ul>
      )}
    </section>
  )
}
