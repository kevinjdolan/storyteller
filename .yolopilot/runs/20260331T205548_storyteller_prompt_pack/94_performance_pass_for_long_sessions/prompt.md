# 94 — Performance Pass for Long Sessions

Read `base_prompt.md` first and preserve all prior prompt work.

## Objective

Keep the app responsive when a session accumulates lots of chat messages, revisions, segments, and artifacts.

## Build
- Profile or inspect the heaviest frontend and backend paths that will grow over long sessions.
- Optimize obvious hotspots such as large chat renders, session hydration payload size, and repeated expensive recomputations.
- Document any pagination, virtualization, or lazy-loading choices for long histories.

## Deliverables

- Performance fixes or guard rails
- Notes on long-session scaling decisions
- Any virtualization or pagination introduced

## Acceptance checks

- Longer sessions remain practical to open and use.
- Hydration payloads and UI rendering do not grow uncontrollably.
- The performance choices are documented so future work does not undo them.

## Notes

Tackle real hotspots, not imagined ones.

## Suggested commit label

`feat(prompt-94): performance pass`
