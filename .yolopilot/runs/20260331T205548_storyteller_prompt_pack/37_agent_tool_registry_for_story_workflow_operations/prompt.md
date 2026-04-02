# 37 — Agent Tool Registry for Story Workflow Operations

Read `base_prompt.md` first and preserve all prior prompt work.

## Objective

Organize the backend’s callable story operations into a clear registry so planning, generation, and chat translation can share the same action vocabulary.

## Build
- Define backend tools or service functions for operations like generate pitches, refine pitch, generate character sheets, refine character sheet, generate beat sheet, update setup heuristics, compose next segment, rewrite segments, estimate audio length, and start audio generation.
- Describe the inputs, outputs, and side effects of each tool in a central registry.
- Use the registry to reduce duplicate logic across routes, workers, and future model orchestration.

## Deliverables

- Tool registry or capability map
- Centralized tool interfaces
- Documentation of side effects and expected outputs

## Acceptance checks

- Story operations are discoverable in one place.
- The chat/action layer and the worker layer call the same domain services.
- Adding a new stage operation later would be straightforward.

## Notes

Keep tools thin wrappers around real business services.

## Suggested commit label

`feat(prompt-37): agent tool registry`
