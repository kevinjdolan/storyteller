# 17 — Real-Time Event Schema and Channel Plan

Read `base_prompt.md` first and preserve all prior prompt work.

## Objective

Define the payload contracts for server-to-client live updates before implementing the transport in detail.

## Build
- Design event shapes for chat messages, stage changes, UI action echoes, composition chunk streams, progress updates, job status, and error notifications.
- Decide how session-scoped channels or subscriptions work so only the right browser tab sees the right updates.
- Document how the same underlying event log relates to the ephemeral real-time feed.

## Deliverables

- `docs/realtime-events.md`
- Shared event type definitions or JSON schemas
- A short note on channel/auth assumptions for local development

## Acceptance checks

- Frontend engineers know what payloads to expect before the sockets are built.
- Progress events are expressive enough for both composition and audio workflows.
- The schema leaves room for optimistic UI updates and later replay.

## Notes

Keep names plain and payloads boring.

## Suggested commit label

`feat(prompt-17): realtime event schema`
