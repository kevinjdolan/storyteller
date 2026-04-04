# 14 — Repository Layer and Session Service

Read `base_prompt.md` first and preserve all prior prompt work.

## Objective

Build the first real backend service layer around story sessions so the app stops thinking in terms of raw tables.

## Build
- Add repository or data-access helpers for the most important session queries and updates.
- Implement a session service that can create a new session, load a session snapshot, update stage state, and list recent sessions.
- Make sure the service returns data shaped for the UI instead of leaking ORM internals.

## Deliverables

- Session repositories or DAOs
- Session service layer
- Backend tests for session creation and retrieval

## Acceptance checks

- The backend has a clean path for the future past-sessions home screen.
- Business rules about stage transitions live in the service layer, not in route handlers.
- Tests prove the service can round-trip real database state.

## Notes

Favor explicit service methods over a generic catch-all CRUD layer.

## Suggested commit label

`feat(prompt-14): repositories and session service`
