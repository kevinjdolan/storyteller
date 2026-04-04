# 57 — Composition Prompt Assembly

Read `base_prompt.md` first and preserve all prior prompt work.

## Objective

Assemble the structured inputs the writing engine will need so segment generation is grounded and consistent.

## Build
- Build a backend prompt-assembly service that gathers genre, tone, brief, selected pitch, character sheet, beat sheet, setup preferences, outline card, continuity facts, and bedtime guidelines.
- Separate stable system instructions from per-segment dynamic context.
- Store or log the assembled prompt context in a debuggable but safe way.

## Deliverables

- Prompt assembly service
- Prompt input schema
- Debug-friendly prompt context logging strategy

## Acceptance checks

- Composition has a single source for prompt assembly rather than hand-built prompts scattered across the codebase.
- Stable guidance and dynamic context are clearly separated.
- The assembled context is inspectable when writing quality goes wrong.

## Notes

Treat prompt assembly as application code, not an afterthought.

## Suggested commit label

`feat(prompt-57): composition prompt assembly`
