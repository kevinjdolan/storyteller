import type { BackendStatus } from '../../hooks/useBackendStatus.ts'
import { Badge, Panel, type BadgeTone } from './primitives.tsx'

type ConnectionStatusBadgeProps = {
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

export function ConnectionStatusBadge({ status }: ConnectionStatusBadgeProps) {
  return (
    <Panel
      actions={
        <Badge tone={getConnectionTone(status.state)}>{status.label}</Badge>
      }
      aria-label="Backend connection status"
      as="section"
      className="connection-indicator"
      eyebrow="Connection"
    >
      <p className="connection-indicator__detail">{status.detail}</p>
      <p className="connection-indicator__message" data-testid="api-message">
        {status.message}
      </p>
    </Panel>
  )
}
