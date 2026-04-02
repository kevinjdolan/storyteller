# 23 — Frontend State Foundation

Read `base_prompt.md` first and preserve all prior prompt work.

## Objective

Introduce a predictable frontend state model for session snapshots, live events, and optimistic UI interactions.

## Build
- Choose and wire the frontend data tools you will rely on, such as React Query for server state and a small local store for live session state.
- Model the current session snapshot, pending UI actions, and live event stream state separately so responsibilities stay clear.
- Add thin API hooks for fetching the home-screen list and a single session snapshot.

## Deliverables

- Frontend data/state setup
- Session data hooks
- A short state architecture note

## Acceptance checks

- The frontend is not forced into prop-drilling for session state.
- Server state and transient UI state are clearly separated.
- The new state layer can support real-time updates later.

## Notes

Keep the state model understandable to someone new to the repo.

## Suggested commit label

`feat(prompt-23): frontend state foundation`
