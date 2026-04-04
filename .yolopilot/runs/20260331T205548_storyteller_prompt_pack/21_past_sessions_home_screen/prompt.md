# 21 — Past Sessions Home Screen

Read `base_prompt.md` first and preserve all prior prompt work.

## Objective

Implement the first product-facing screen: a page where the user can see prior story sessions, tell whether they are in progress or complete, and resume or start fresh.

## Build
- Build a backend endpoint that lists recent sessions with key metadata like title, last modified time, stage, and completion status.
- Create the home screen UI that renders these sessions in a useful list or card layout and includes a strong ‘new session’ action.
- Support empty, loading, and error states so the screen feels complete.

## Deliverables

- Session list API endpoint
- Home screen page and components
- Basic filtering or grouping by status if it fits cleanly

## Acceptance checks

- A user lands on the past-sessions screen first, not on a blank editor.
- Both in-progress and completed sessions are clearly distinguishable.
- The user can enter an existing session or start a new one from this screen.

## Notes

Keep the first version clean and legible rather than over-designed.

## Suggested commit label

`feat(prompt-21): past sessions home screen`
