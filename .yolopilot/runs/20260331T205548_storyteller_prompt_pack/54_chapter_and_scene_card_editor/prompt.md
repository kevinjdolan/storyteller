# 54 — Chapter and Scene Card Editor

Read `base_prompt.md` first and preserve all prior prompt work.

## Objective

Let the user inspect and lightly edit the detailed outline before composition begins.

## Build
- Build UI for chapter or scene cards with title, purpose, linked beat, target length, and summary.
- Support reorder, light edits, and regenerate-this-card interactions where sensible.
- Make downstream invalidation explicit if the user edits cards significantly.

## Deliverables

- Outline card editor UI
- Card update actions
- Change propagation rules

## Acceptance checks

- The user can shape the plan at a granular level without redoing the entire pipeline.
- Each card has enough information to guide composition.
- Edits are durable and reflected in the session summary.

## Notes

Keep editing structured. Avoid turning this into a full free-form outliner.

## Suggested commit label

`feat(prompt-54): chapter scene card editor`
