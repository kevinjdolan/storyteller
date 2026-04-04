# 51 — Correlation Heuristics for Word Count, Runtime, and Chapters

Read `base_prompt.md` first and preserve all prior prompt work.

## Objective

Build simple heuristics that connect the user’s soft planning targets so the app can suggest coherent ranges and explain tradeoffs.

## Build
- Implement a heuristic service that estimates likely runtime from word count and narration speed assumptions, and likely chapter size from total words and chapter count.
- Allow one field to suggest updates to related fields while still preserving user control.
- Surface the heuristic assumptions in a compact, understandable way.

## Deliverables

- Planning heuristic service
- Frontend hints or calculated summaries
- Tests for the core calculations

## Acceptance checks

- Changing one planning field can influence the others helpfully without feeling authoritarian.
- Assumptions are inspectable rather than hidden.
- The heuristics are simple enough to maintain and adjust later.

## Notes

Do not oversell precision here. Keep it explicitly approximate.

## Suggested commit label

`feat(prompt-51): correlation heuristics`
