import type { BackendStatus } from '../../hooks/useBackendStatus.ts'
import { FeedbackBanner, InlineSpinner } from './feedback.tsx'
import { Badge, Button, Panel, type BadgeTone } from './primitives.tsx'

type ConnectionStatusBadgeProps = {
  onRefresh: () => void
  status: BackendStatus
}

function getConnectionTone(state: BackendStatus['state']): BadgeTone {
  if (state === 'online') {
    return 'success'
  }

  if (state === 'offline') {
    return 'danger'
  }

  return 'warning'
}

function formatCheckedAt(value: string | null) {
  if (value == null) {
    return 'Checking backend reachability now.'
  }

  return `Last checked ${new Intl.DateTimeFormat(undefined, {
    hour: 'numeric',
    minute: '2-digit',
  }).format(new Date(value))}.`
}

export function ConnectionStatusBadge({
  onRefresh,
  status,
}: ConnectionStatusBadgeProps) {
  return (
    <Panel
      actions={
        <div className="connection-indicator__actions">
          <Badge tone={getConnectionTone(status.state)}>{status.label}</Badge>
          <Button
            disabled={status.isRefreshing}
            size="compact"
            tone="ghost"
            onClick={onRefresh}
          >
            {status.isRefreshing ? (
              <>
                <InlineSpinner label="Refreshing backend status" />
                Checking
              </>
            ) : (
              'Check again'
            )}
          </Button>
        </div>
      }
      aria-label="Backend connection status"
      as="section"
      className="connection-indicator"
      description={formatCheckedAt(status.checkedAt)}
      eyebrow="Connection"
      title="Backend reachability"
    >
      <p className="connection-indicator__detail">{status.detail}</p>
      <p className="connection-indicator__message" data-testid="api-message">
        {status.message}
      </p>
      {status.state === 'offline' ? (
        <FeedbackBanner
          className="connection-indicator__banner"
          description="Blocking loads will offer retry actions. Non-blocking failures surface in the notification stack."
          title="Requests may fail until FastAPI returns"
          tone="warning"
        />
      ) : null}
    </Panel>
  )
}
