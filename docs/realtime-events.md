# Realtime Events

This document defines the server-to-client live-update contract introduced in
prompt 17. It is intentionally boring: session-scoped channels, a small number
of event families, and explicit links back to the durable event log.

The machine-readable schema bundle lives at
[docs/realtime-events.schema.json](/Users/kevin/code/storyteller/docs/realtime-events.schema.json).
The canonical backend source for that bundle is
[backend/app/models/realtime.py](/Users/kevin/code/storyteller/backend/app/models/realtime.py).

## Design Rules

- Every live event belongs to exactly one story session.
- The browser subscribes to one session channel at a time: `session:{session_id}`.
- Durable feed events carry `sequence_number` and `event_log_entry_id` so the
  client can replay or deduplicate them.
- High-frequency typing chunks stay ephemeral. The UI can feel live without
  forcing every partial token into the append-only event log.
- Clients may optimistically render local actions, but server-emitted events stay
  authoritative. `correlation_id` is reserved for matching optimistic UI state
  back to confirmed server events.
- Segment indexes are 1-based. `chunk_index` is 0-based within a segment.

## Channel Plan

One workspace tab opens one live connection and sends a session subscription
frame:

```json
{
  "schema_version": 1,
  "action": "subscribe",
  "session_id": "session-123",
  "tab_id": "tab-9",
  "last_sequence_number": 41,
  "request_id": "subscribe-1"
}
```

The server responds with an acknowledgement:

```json
{
  "schema_version": 1,
  "action": "subscribed",
  "session_id": "session-123",
  "channel": "session:session-123",
  "connection_id": "conn-22",
  "tab_id": "tab-9",
  "accepted_at": "2026-04-01T08:30:00Z",
  "replay_strategy": "delta",
  "replay_from_sequence_number": 42,
  "latest_sequence_number": 48,
  "request_id": "subscribe-1",
  "local_actor": {
    "actor_type": "user",
    "actor_id": "local-user"
  }
}
```

Rules:

- Only connections subscribed to `session:{session_id}` receive that session's
  events.
- Multiple tabs can subscribe to the same session and all receive the same
  server truth.
- A tab viewing a different session should open a separate subscription instead
  of multiplexing unrelated sessions through one feed.
- `last_sequence_number` is the last durable event the client has already
  applied. The server uses it to decide whether replay can be a cheap delta or
  whether the tab should rehydrate from the session snapshot endpoint.

## Event Envelope

Every session event shares the same outer shape:

```json
{
  "schema_version": 1,
  "event_id": "rt-88",
  "type": "job.progress",
  "session_id": "session-123",
  "channel": "session:session-123",
  "actor": {
    "actor_type": "system",
    "actor_id": "worker"
  },
  "stage": "audio",
  "created_at": "2026-04-01T08:32:00Z",
  "correlation_id": "mutation-17",
  "delivery": "live",
  "replayable": true,
  "sequence_number": 48,
  "event_log_entry_id": "event-log-48",
  "payload": {}
}
```

Envelope fields:

- `event_id`: unique realtime-delivery identifier.
- `type`: one of the event families below.
- `channel`: always `session:{session_id}`.
- `actor`: who caused the change, reusing the durable event-log actor model.
- `stage`: optional stage context when the update clearly belongs to one stage.
- `correlation_id`: optional client-supplied mutation id echoed back by the
  server to reconcile optimistic UI state.
- `delivery`: `live` for freshly emitted events, `replay` for durable catch-up
  after reconnect.
- `replayable`: `true` for events backed by the event log, `false` for ephemeral
  stream hints such as text chunks.
- `sequence_number` and `event_log_entry_id`: required on replayable events,
  absent on ephemeral ones.

## Event Families

| Event type | Replayable | Purpose |
| --- | --- | --- |
| `chat.message` | yes | Full chat/history entry for the left pane. |
| `workflow.stage_changed` | yes | Stage state transition plus invalidation context for the main workflow UI. |
| `ui.action_echo` | yes | Compact structured echo of a UI or chat-applied action. |
| `composition.chunk` | no | Live typewriter chunk stream for composition. |
| `job.progress` | yes | Progress checkpoint for composition or audio jobs. |
| `job.status` | yes | Queue, start, pause, completion, cancellation, or failure transition for a job. |
| `error.notification` | yes | User-visible session or job error that should survive replay. |

### `chat.message`

Use this for complete chat content, not previews. Payload fields:

- `message_id`
- `message_role`
- `content`
- `content_format`
- `source`

This is the live counterpart to `chat.message.recorded`, which only stores a
durable preview in the event log.

### `workflow.stage_changed`

The payload is intentionally the same shape as the durable
`WorkflowStageChangedEventPayload`:

- `previous_status`
- `status`
- `detail`
- `invalidated_stages`
- `current_stage`
- `resume_stage`
- `furthest_completed_stage`
- `overall_status`

The changed stage itself stays on the outer `stage` field.

### `ui.action_echo`

Payload fields:

- `action`
- `result`
- `summary`
- `control_id`
- `value_summary`
- `origin`
- `detail`
- `chat_message_id`

This event exists so the UI and chat history stay coherent after direct clicks,
form edits, or accepted chat-driven actions.

### `composition.chunk`

Payload fields:

- `job_id`
- `segment_id`
- `segment_index`
- `chunk_index`
- `chunk_kind`
- `text`
- `summary`
- `cumulative_character_count`
- `cumulative_word_count`
- `is_final_chunk`

`chunk_kind` values:

- `segment_start`
- `delta`
- `segment_summary`

This one event family leaves room for prompt 62 requirements:

- segment start is `chunk_kind: "segment_start"`
- streamed typing is `chunk_kind: "delta"`
- the periodic segment recap is `chunk_kind: "segment_summary"`

These events are intentionally ephemeral. Reconnect behavior should rebuild the
accepted story state from durable composition records and then resume streaming
new chunks.

### `job.progress`

This event is the replayable progress checkpoint for both composition and audio.
Payload fields:

- `job_id`
- `job_kind`
- `status`
- `progress_percent`
- `current_step`
- `current_step_index`
- `total_steps`
- `completed_segments`
- `current_segment_index`
- `total_segments`
- `segment_id`
- `segment_status`
- `eta_seconds`
- `estimated_duration_seconds`
- `latest_asset_id`
- `latest_asset_kind`
- `message`

Notes:

- `job_kind` is `composition` or `audio`.
- `status` mirrors the durable job states: `queued`, `in_progress`, `paused`,
  `completed`, `failed`, and `cancelled`.
- `estimated_duration_seconds` is mainly for audio UX, but it stays available on
  both job kinds so the transport stays uniform.
- `latest_asset_id` and `latest_asset_kind` leave room for later preview UIs to
  notice that a segment or final artifact became ready.

### `job.status`

Use this for durable status transitions rather than numeric progress ticks.
Payload fields:

- `job_id`
- `job_kind`
- `previous_status`
- `status`
- `message`
- `stop_reason`
- `error_message`
- `current_segment_index`
- `total_segments`
- `latest_asset_id`
- `latest_asset_kind`

Typical examples:

- composition queued
- composition paused
- audio completed
- audio failed with `error_message`

### `error.notification`

Payload fields:

- `code`
- `severity`
- `message`
- `retryable`
- `detail`
- `job_id`
- `job_kind`

Use this when the user should be told something went wrong and the information
should still be present after refresh or replay. Connection-level transport
errors that are not session-specific should stay out of this feed and live in
socket-level status instead.

## Durable Event Log vs Live Feed

The event log remains the source of truth for replayable session history. The
realtime feed is a delivery mechanism layered on top of that truth.

Relationship rules:

- Replayable live events should correspond 1:1 to durable `event_log_entries`
  and copy over the same `sequence_number` and `event_log_entry_id`.
- `delivery: "replay"` means the server is replaying already-persisted events
  after a reconnect or a late subscription.
- `composition.chunk` is the exception. It is not stored in the append-only
  event log and should not be relied on for recovery.
- When a reconnect misses ephemeral chunks, the client should rehydrate from the
  latest session snapshot and then continue applying future live events.
- The session snapshot endpoint from prompt 38 is the fallback when replay alone
  is not enough or the server returns `replay_strategy: "hydrate"` in the
  subscription acknowledgement.

## Local Development Auth Assumptions

Local development is still single-user and permissive for now.

- The backend treats the current browser as `local-user`.
- No bearer-token requirement is assumed for the initial local socket handshake.
- The server must still verify that the requested session exists before
  accepting the subscription.
- Future real auth should keep the same channel model and simply replace the
  local identity assumption with session ownership checks before joining
  `session:{session_id}`.

## Optimistic UI Note

Clients may immediately render a local pending state for actions such as
selecting a tone or changing runtime targets. Those pending states should clear
only when the server echoes back matching durable events carrying the same
`correlation_id`. If the action is rejected, the client should revert the
optimistic state and surface the `ui.action_echo` or `error.notification`
explaining why.
