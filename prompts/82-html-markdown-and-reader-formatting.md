# 82 — Story Formatting for In-App Reading

Read `base_prompt.md` first and preserve all prior prompt work.

## Objective

Prepare clean, readable formatted story text for the in-app reader and any lightweight text export needs.

## Build
- Create a backend or frontend formatting layer that turns canonical story text into readable chaptered HTML or structured rich text for the app reader.
- Preserve paragraph breaks, chapter headings, and any simple emphasis safely.
- Keep the formatting pipeline deterministic so reading output and export output stay consistent.

## Deliverables

- Reader formatting pipeline
- In-app story rendering component
- Formatting tests for chapter and paragraph structure

## Acceptance checks

- The in-app story text is pleasant to read.
- Formatting is not brittle or dependent on model quirks.
- Chapter structure, when present, is reflected clearly.

## Notes

Reader clarity matters more than ornamental typography.

## Suggested commit label

`feat(prompt-82): html markdown and reader formatting`
