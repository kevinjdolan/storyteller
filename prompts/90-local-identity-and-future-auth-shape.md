# 90 — Local Identity Model and Future Authentication Shape

Read `base_prompt.md` first and preserve all prior prompt work.

## Objective

Decide how the app identifies a user in local development and leave a clean seam for real authentication later.

## Build
- Implement a simple local single-user mode or lightweight identity stub so sessions can be associated with an owner without adding full auth complexity yet.
- Keep session ownership and route assumptions compatible with a future multi-user setup.
- Document the current auth stance plainly in the README and architecture notes.

## Deliverables

- Local identity stub or single-user assumption in code
- Ownership field wiring where needed
- Docs for current and future auth assumptions

## Acceptance checks

- The app works cleanly in local development without a full sign-in system.
- The data model does not paint future auth into a corner.
- Ownership assumptions are explicit.

## Notes

Do not overbuild auth for v1.

## Suggested commit label

`feat(prompt-90): local identity and future auth shape`
