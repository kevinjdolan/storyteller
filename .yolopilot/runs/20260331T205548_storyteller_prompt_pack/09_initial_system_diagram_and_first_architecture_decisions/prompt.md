# 09 — Initial System Diagram and First Architecture Decisions

Read `base_prompt.md` first and preserve all prior prompt work.

## Objective

Capture the core architecture decisions early so later prompts can build on a stable mental model.

## Build
- Write an ADR or equivalent note for the main architectural choices: backend-owned AI calls, Postgres-backed durable state, file-backed GCS emulator for assets, WebSocket-based live updates, and a separate worker process for long-running jobs.
- Add one lightweight system diagram in Markdown or Mermaid showing browser, API, worker, database, object storage, and Gemini integrations.
- Record the decision that word count, runtime, and chapter count are soft planning hints rather than hard constraints.

## Deliverables

- `docs/adr/` or similar notes
- A simple system diagram
- A written statement of the product’s soft-constraint philosophy

## Acceptance checks

- Later contributors can tell where real-time updates and long-running tasks belong.
- The diagram includes session resume and durable event history as first-class concepts.
- The architecture notes reflect the actual product brief instead of a generic app template.

## Notes

Use plain language. This doc is for builders, not for impressing anyone.

## Suggested commit label

`feat(prompt-09): initial system diagram and adr`
