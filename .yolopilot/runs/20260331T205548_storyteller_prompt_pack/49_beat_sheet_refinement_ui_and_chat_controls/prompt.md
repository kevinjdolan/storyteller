# 49 — Beat Sheet Refinement UI and Chat Controls

Read `base_prompt.md` first and preserve all prior prompt work.

## Objective

Let the user inspect, tweak, and regenerate specific beats through both structured UI controls and chat messages.

## Build
- Create a beat editor that shows the ordered beats, their summaries, and any stage-specific notes.
- Support chat actions like intensify midpoint wonder, soften all-is-lost, or make the finale more playful.
- Keep refinement history and mark downstream composition prompts as needing refresh after material beat changes.

## Deliverables

- Beat editor UI
- Beat refinement backend actions
- Change tracking for beat edits

## Acceptance checks

- The beat sheet feels like a living plan the user can shape.
- Beat changes flow cleanly into later planning and composition.
- Chat-based beat edits and UI edits stay synchronized.

## Notes

Favor clarity over dense plotting jargon in the UI.

## Suggested commit label

`feat(prompt-49): beat sheet refinement ui and chat`
