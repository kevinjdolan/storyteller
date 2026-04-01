import type { BackendStatus } from '../../hooks/useBackendStatus.ts'

type ConnectionStatusBadgeProps = {
  status: BackendStatus
}

export function ConnectionStatusBadge({ status }: ConnectionStatusBadgeProps) {
  return (
    <section
      aria-label="Backend connection status"
      className="connection-indicator"
    >
      <div className="connection-indicator__heading">
        <p className="eyebrow eyebrow-muted">Connection</p>
        <span
          className={`status-badge status-badge--${status.state}`}
          data-testid="backend-state"
        >
          {status.label}
        </span>
      </div>
      <p className="connection-indicator__detail">{status.detail}</p>
      <p className="connection-indicator__message" data-testid="api-message">
        {status.message}
      </p>
    </section>
  )
}
