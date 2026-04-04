# 93 — Accessibility Pass and Keyboard Support

Read `base_prompt.md` first and preserve all prior prompt work.

## Objective

Polish accessibility across the main workflow so the product remains usable under real conditions.

## Build
- Audit the home screen, workspace, chat, selection cards, composition view, progress indicators, and finalize screen for keyboard support and semantic structure.
- Fix obvious tab-order, focus, aria-label, and live-region issues, especially around chat messages and progress updates.
- Add reduced-motion handling for live composition and progress animations.

## Deliverables

- Accessibility fixes across the app
- Any helper hooks or components needed for a11y
- A checklist of what was covered

## Acceptance checks

- Core product flows are navigable without a mouse.
- Dynamic updates are announced or represented accessibly where reasonable.
- Reduced-motion users are not punished by the live-writing UI.

## Notes

Focus on the real workflow, not a theoretical score.

## Suggested commit label

`feat(prompt-93): accessibility pass and keyboard support`
