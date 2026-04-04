# 38 — Session Replay and Resume Hydration

Read `base_prompt.md` first and preserve all prior prompt work.

## Objective

Make session resume trustworthy by defining how the backend rebuilds the current workspace state from durable records.

## Build
- Implement backend logic that can build a full session snapshot from relational records plus the latest accepted artifacts and summaries.
- Decide when to use event replay, when to use materialized session state, and how to reconcile the two safely.
- Expose a session hydration endpoint used by the workspace route on load.

## Deliverables

- Session hydration endpoint
- Backend replay/hydration service
- Tests for resuming sessions in different stages

## Acceptance checks

- A user can leave mid-session and return to a coherent workspace.
- Hydration works for completed sessions as well as in-progress ones.
- The restore path can represent active or failed jobs honestly.

## Notes

Fast hydration matters, but correctness matters more.

## Suggested commit label

`feat(prompt-38): session replay and resume hydration`
