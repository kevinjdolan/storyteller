# 61 — Segmented Writing Engine

Read `base_prompt.md` first and preserve all prior prompt work.

## Objective

Implement the backend writing engine that drafts the story one segment at a time rather than attempting a huge monolithic generation.

## Build
- Choose a sensible segment unit such as chapter, scene, or sub-scene and define how the engine advances from one unit to the next.
- For each segment, assemble context from the current plan, prior accepted text summary, continuity bible, and local segment goals.
- Persist the raw generated text, accepted text, and any summary needed for the next segment.

## Deliverables

- Segmented writing service
- Segment persistence records
- Strategy note for context carryover between segments

## Acceptance checks

- The engine can write incrementally through the story plan.
- Context is carried forward in a structured way instead of blindly concatenating the full draft every time.
- Each segment has durable records suitable for rewrite later.

## Notes

Optimize for controllability and rewrite support.

## Suggested commit label

`feat(prompt-61): segmented writing engine`
