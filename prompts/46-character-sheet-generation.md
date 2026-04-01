# 46 — Character Sheet Generation Pipeline

Read `base_prompt.md` first and preserve all prior prompt work.

## Objective

Generate candidate character sheets for the chosen pitch in a form the user can compare and refine.

## Build
- Build a character-sheet generator that outputs several candidate sets or several candidate lead-character concepts with supporting cast details.
- Include fields like role, goal, flaw, comfort trait, bedtime-safety notes, relationships, and visual anchors.
- Persist these candidates and render them as readable comparison cards or panels.

## Deliverables

- Character sheet service
- Character persistence model
- Character sheet comparison UI

## Acceptance checks

- Character sheets feel distinct and useful for decision-making.
- The output format supports later beat-sheet generation.
- Candidates are durable and resumable like pitches.

## Notes

Optimize for story function, not encyclopedia-level biography.

## Suggested commit label

`feat(prompt-46): character sheet generation`
