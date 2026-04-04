# 32 — UI Action Policy Engine

Read `base_prompt.md` first and preserve all prior prompt work.

## Objective

Create a deterministic policy layer that decides whether a proposed action is valid in the current session state and how it should be applied.

## Build
- Implement validation rules based on current stage, selected entities, job status, and whether a change requires regeneration of downstream artifacts.
- Allow the policy engine to mark actions as accepted, rejected, requires confirmation, or accepted-with-side-effects.
- Return structured reasons so the chat and UI can explain what happened.

## Deliverables

- Policy engine for proposed UI actions
- Tests for valid and invalid action sequences
- Clear error or confirmation messages

## Acceptance checks

- The system prevents impossible state changes like selecting a tone before a genre exists unless it first proposes a prerequisite action.
- Downstream invalidation is explicit when upstream inputs change.
- The engine is deterministic and testable without calling Gemini.

## Notes

Treat the model as a proposal generator, not the source of truth.

## Suggested commit label

`feat(prompt-32): ui action policy engine`
