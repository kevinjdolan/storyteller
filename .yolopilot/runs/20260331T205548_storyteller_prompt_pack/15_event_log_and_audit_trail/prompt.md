# 15 — Event Log and Audit Trail

Read `base_prompt.md` first and preserve all prior prompt work.

## Objective

Create an append-only event history that can explain how a session changed over time and later power resume, replay, and debugging.

## Build
- Define an event log table or model that captures actor, event type, payload, timestamps, and optional stage context.
- Record meaningful events for session creation, selections, AI outputs, user edits, chat messages, UI actions, composition progress, and audio progress.
- Add helper utilities for appending events in a consistent way.

## Deliverables

- Event log model and access layer
- Common event helpers
- Documentation for the event taxonomy

## Acceptance checks

- A session’s history can be reconstructed without relying on browser local storage.
- Events distinguish between user actions, agent actions, and system/worker actions.
- Event payloads are typed or at least versioned enough to age well.

## Notes

Think of this as product telemetry plus durable replay support.

## Suggested commit label

`feat(prompt-15): event log and audit trail`
