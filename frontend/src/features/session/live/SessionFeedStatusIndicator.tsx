import type { BadgeTone } from '../../../shared/ui/primitives.tsx'
import { Badge } from '../../../shared/ui/primitives.tsx'
import type { SessionEventStreamState } from '../sessionRuntimeStore.ts'

type SessionFeedStatusIndicatorProps = {
  eventStream: SessionEventStreamState
}

const connectionTimestampFormatter = new Intl.DateTimeFormat(undefined, {
  hour: 'numeric',
  minute: '2-digit',
})

function getConnectionTone(
  connectionState: SessionEventStreamState['connectionState'],
): BadgeTone {
  if (connectionState === 'open') {
    return 'success'
  }

  if (connectionState === 'error') {
    return 'danger'
  }

  if (connectionState === 'closed') {
    return 'warning'
  }

  return 'brand'
}

function getConnectionLabel(
  connectionState: SessionEventStreamState['connectionState'],
) {
  if (connectionState === 'open') {
    return 'Connected'
  }

  if (connectionState === 'connecting') {
    return 'Connecting'
  }

  if (connectionState === 'reconnecting') {
    return 'Reconnecting'
  }

  if (connectionState === 'closed') {
    return 'Paused'
  }

  if (connectionState === 'error') {
    return 'Unavailable'
  }

  return 'Idle'
}

function buildConnectionDetail(eventStream: SessionEventStreamState) {
  if (eventStream.connectionDetail != null) {
    return eventStream.connectionDetail
  }

  const details = []

  if (eventStream.channel != null) {
    details.push(eventStream.channel)
  }

  if (eventStream.lastSequenceNumber != null) {
    details.push(`Seq ${eventStream.lastSequenceNumber}`)
  }

  if (eventStream.retryCount > 0) {
    details.push(`Retry ${eventStream.retryCount}`)
  }

  if (eventStream.lastConnectedAt != null) {
    details.push(
      `Connected ${connectionTimestampFormatter.format(
        new Date(eventStream.lastConnectedAt),
      )}`,
    )
  }

  return details.length > 0
    ? details.join(' • ')
    : 'Awaiting live session events.'
}

export function SessionFeedStatusIndicator({
  eventStream,
}: SessionFeedStatusIndicatorProps) {
  return (
    <div className="workspace-feed-status" data-testid="live-feed-status">
      <Badge tone={getConnectionTone(eventStream.connectionState)}>
        {getConnectionLabel(eventStream.connectionState)}
      </Badge>
      <p className="workspace-feed-status__detail">
        {buildConnectionDetail(eventStream)}
      </p>
    </div>
  )
}
