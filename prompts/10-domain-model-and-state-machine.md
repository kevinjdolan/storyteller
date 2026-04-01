# 10 — Define the Domain Model and Session State Machine

Read `base_prompt.md` first and preserve all prior prompt work.

## Objective

Model the core business entities and the allowed stage transitions for a story creation session so the backend and frontend can agree on workflow rules.

## Build
- Define the major entities: story session, workflow stage, genre, tone profile, story brief, pitch, selected pitch, character sheet, beat sheet, story setup, composition segment, audio job, export asset, and event log entry.
- Describe the allowed stage order while still allowing safe backward edits and re-entry from past sessions.
- Write down the rules for what counts as `draft`, `in_progress`, `completed`, and `needs_regeneration` state.

## Deliverables

- `docs/domain-model.md`
- State machine diagram or table
- Shared enum or constants plan for workflow stages

## Acceptance checks

- The model supports resuming an unfinished session without guessing from UI state.
- Backward edits are supported intentionally rather than as an accident.
- The stage machine makes room for interruption and rewrite during composition.

## Notes

Treat the session as the durable unit of work.

## Suggested commit label

`feat(prompt-10): domain model and state machine`
