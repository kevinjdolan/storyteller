# 44 — Story Pitch Generation Pipeline

Read `base_prompt.md` first and preserve all prior prompt work.

## Objective

Generate a handful of candidate story pitches grounded in the selected genre, tone, and user brief.

## Build
- Implement a backend pitch-generation service that creates multiple differentiated pitches, each with a title, short hook, central conflict, and why-it-fits note.
- Store generated pitch sets durably so the user can revisit them later.
- Add UI rendering for the pitch cards in the main pane.

## Deliverables

- Pitch generation service
- Pitch persistence
- Pitch selection UI cards

## Acceptance checks

- The app generates several meaningful options, not trivial rewrites of the same idea.
- Pitch cards are easy to compare quickly.
- The user can resume later and still see the previously generated options.

## Notes

Keep output shape stable and predictable.

## Suggested commit label

`feat(prompt-44): pitch generation pipeline`
