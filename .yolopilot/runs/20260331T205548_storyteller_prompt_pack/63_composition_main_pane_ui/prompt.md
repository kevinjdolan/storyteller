# 63 — Composition Main-Pane UI

Read `base_prompt.md` first and preserve all prior prompt work.

## Objective

Build the main-pane composition experience with live text, visible progress, and a clear sense of where the story currently is.

## Build
- Create the composition stage UI with a live text area, current segment label, recent segment summary, and overall story progress bar.
- Show the most recently generated text prominently while keeping earlier accepted text accessible.
- Render job controls for pause, resume, request rewrite, and return to plan if applicable.

## Deliverables

- Composition stage UI
- Progress indicators
- Visible controls for live composition

## Acceptance checks

- The UI makes writing feel alive and comprehensible.
- The user can tell how far through the overall story the system is.
- Controls are present without cluttering the experience.

## Notes

Do not bury progress behind small text.

## Suggested commit label

`feat(prompt-63): composition main pane ui`
