# 66 — Rewrite Prior Segments and Regenerate Downstream Text

Read `base_prompt.md` first and preserve all prior prompt work.

## Objective

Allow the system to revisit already written portions of the story and cascade necessary updates forward when upstream changes matter.

## Build
- Create a rewrite flow that can target a selected segment or range of segments with explicit user instructions.
- Mark downstream segments as stale when a rewrite would affect continuity and decide whether to auto-regenerate or require confirmation.
- Preserve prior versions so the user can compare before accepting a rewrite.

## Deliverables

- Rewrite service for segments
- Stale/downstream invalidation logic
- Version preservation for rewritten text

## Acceptance checks

- The product can support serious mid-stream course corrections.
- Continuity-aware downstream handling is explicit.
- Older segment versions remain inspectable.

## Notes

This is a core differentiator. Treat it carefully.

## Suggested commit label

`feat(prompt-66): rewrite prior segments`
