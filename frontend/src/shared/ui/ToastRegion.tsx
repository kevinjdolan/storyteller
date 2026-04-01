import type { AppShellToast } from '../../state/appShellStore.ts'
import { Badge, Panel, StackedList, StackedListItem } from './primitives.tsx'

type ToastRegionProps = {
  toasts: ReadonlyArray<AppShellToast>
}

function getToastTone(tone: AppShellToast['tone']) {
  if (tone === 'success') {
    return 'success'
  }

  if (tone === 'warning') {
    return 'accent'
  }

  return 'brand'
}

export function ToastRegion({ toasts }: ToastRegionProps) {
  return (
    <Panel
      actions={<Badge tone="brand">{toasts.length}</Badge>}
      aria-label="Future notification dock"
      as="section"
      className="toast-region"
      eyebrow="Toasts"
      tone="subtle"
    >
      {toasts.length === 0 ? (
        <p className="toast-region__empty">
          Workflow notifications, export alerts, and background job updates will
          dock here.
        </p>
      ) : (
        <StackedList className="toast-region__list">
          {toasts.map((toast) => (
            <StackedListItem
              key={toast.id}
              className={`toast-region__item toast-region__item--${toast.tone}`}
              tone={getToastTone(toast.tone)}
            >
              <strong>{toast.title}</strong>
              <p>{toast.body}</p>
            </StackedListItem>
          ))}
        </StackedList>
      )}
    </Panel>
  )
}
