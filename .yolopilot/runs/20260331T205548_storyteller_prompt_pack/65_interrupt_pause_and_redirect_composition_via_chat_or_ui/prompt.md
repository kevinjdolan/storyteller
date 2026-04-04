# 65 — Interrupt, Pause, and Redirect Composition via Chat or UI

Read `base_prompt.md` first and preserve all prior prompt work.

## Objective

Let the user meaningfully steer composition while it is happening instead of treating writing as an uninterruptible batch job.

## Build
- Support pause and redirect actions through both chat and explicit UI controls.
- When interrupted, capture what segment was active and the user’s requested change so the worker can re-plan safely.
- Create a deterministic backend path for how active composition responds to interruptions.

## Deliverables

- Interrupt/pause/resume control flow
- Persistence for interruption requests
- User-visible status changes during interruption handling

## Acceptance checks

- The user can alter direction mid-composition without corrupting session state.
- The system explains whether it is pausing, applying a redirect, or waiting for confirmation.
- Interruptions are durable and replayable.

## Notes

Be explicit about how in-flight work is handled.

## Suggested commit label

`feat(prompt-65): interrupt and redirect composition`
