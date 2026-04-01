# 53 — Outline Drill-Down From Beats to Chapters or Scenes

Read `base_prompt.md` first and preserve all prior prompt work.

## Objective

Transform the high-level beat sheet into a more detailed chapter or scene plan that composition can execute in segments.

## Build
- Create a planning service that expands beats into chapter or scene cards based on the current story setup preferences.
- Show which beat or beats each chapter card supports and what emotional shift it should carry.
- Persist the resulting outline as structured data that can be edited later.

## Deliverables

- Detailed outline generation service
- Chapter/scene card UI
- Outline persistence model

## Acceptance checks

- The system has a clear bridge from beat sheet to draftable writing segments.
- Chapter cards preserve the selected tone, genre, and setup constraints.
- The outline remains editable rather than frozen.

## Notes

The goal is a practical writing plan, not an over-elaborate artifact.

## Suggested commit label

`feat(prompt-53): outline drill down`
