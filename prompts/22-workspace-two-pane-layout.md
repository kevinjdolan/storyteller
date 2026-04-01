# 22 — Workspace Two-Pane Layout

Read `base_prompt.md` first and preserve all prior prompt work.

## Objective

Build the session workspace shell with a left chat pane taking roughly one-third of the screen and a main pane using the remaining space.

## Build
- Create the session workspace page with a responsive two-pane layout that honors the 1/3 chat and 2/3 main-pane requirement on desktop.
- Add a compact header showing session name, current stage, save status, and primary actions like return to home.
- Make the layout degrade gracefully on smaller screens without losing the conceptual two-pane model.

## Deliverables

- Workspace page layout
- Stage/status header
- Responsive behavior rules

## Acceptance checks

- On desktop, the chat pane visibly occupies about one-third of the width.
- The main pane has enough room for form workflows and live composition views.
- The workspace feels like one product surface rather than two unrelated pages.

## Notes

Use simple layout primitives. Fancy chrome can wait.

## Suggested commit label

`feat(prompt-22): workspace two pane layout`
