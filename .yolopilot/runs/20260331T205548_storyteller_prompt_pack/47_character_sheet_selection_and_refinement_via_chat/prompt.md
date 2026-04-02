# 47 — Character Sheet Selection and Refinement via Chat

Read `base_prompt.md` first and preserve all prior prompt work.

## Objective

Allow the user to select or refine character sheets through both UI controls and the chat interface.

## Build
- Wire character-related chat intents into structured actions such as selecting a sheet, adjusting a flaw, softening a voice, or regenerating alternatives.
- Reflect accepted character changes back into both the main pane and the chat log.
- Track whether downstream planning needs regeneration when a major character change happens.

## Deliverables

- Character refinement action support
- UI update and invalidation logic
- Persistence for selected/refined character sheet

## Acceptance checks

- A character can be refined conversationally without losing structured data integrity.
- Major character changes correctly flag later stages for refresh.
- The selected character sheet is easy to inspect at any time.

## Notes

Do not let free-form edits silently drift away from durable state.

## Suggested commit label

`feat(prompt-47): character refinement via chat`
