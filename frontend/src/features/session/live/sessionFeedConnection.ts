export type SessionFeedConnectionState =
  | 'idle'
  | 'connecting'
  | 'open'
  | 'reconnecting'
  | 'closed'
  | 'error'

export type SessionFeedConnectionStatusUpdate = {
  connectionState: SessionFeedConnectionState
  connectionDetail?: string | null
  channel?: string | null
  retryCount?: number
  lastConnectedAt?: string | null
}
