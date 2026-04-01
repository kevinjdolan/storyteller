# 50 — Story Length, Duration, and Chapter Setup

Read `base_prompt.md` first and preserve all prior prompt work.

## Objective

Implement the story setup stage where the user can choose soft planning targets such as word count, estimated read-aloud duration, and chapter organization.

## Build
- Build UI fields for desired word count, target read-aloud duration, chapter count, and optionally approximate scene count.
- Persist these values as preferences rather than hard enforcement rules.
- Explain in the UI that these parameters are correlated suggestions that guide composition instead of rigid constraints.

## Deliverables

- Story setup form UI
- Backend persistence for setup preferences
- Inline explanation of soft-target behavior

## Acceptance checks

- The user can configure planning targets without being tricked into thinking they are guarantees.
- The setup state is durable and revisitable.
- The UI sets expectations clearly about flexible output.

## Notes

Use language that is honest and calming.

## Suggested commit label

`feat(prompt-50): story length duration and chapter setup`
