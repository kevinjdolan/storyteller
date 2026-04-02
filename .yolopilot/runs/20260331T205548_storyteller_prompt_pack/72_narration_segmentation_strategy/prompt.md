# 72 — Narration Segmentation Strategy

Read `base_prompt.md` first and preserve all prior prompt work.

## Objective

Break the final story into narration-friendly segments so audio generation is resumable and aligned with chapter or scene structure.

## Build
- Create a service that splits story text into audio-generation segments using chapter or scene boundaries where possible.
- Preserve metadata about segment order, text source range, and any pause or music transition hints.
- Store the narration plan durably so the worker can resume from the last completed segment.

## Deliverables

- Narration segmentation service
- Segment metadata model
- Rules for chapter pauses and boundaries

## Acceptance checks

- Audio work can be resumed segment by segment rather than restarted wholesale.
- Segments map back to the story text cleanly.
- Segmentation respects logical story boundaries where possible.

## Notes

Segment design should balance quality and recoverability.

## Suggested commit label

`feat(prompt-72): narration segmentation`
