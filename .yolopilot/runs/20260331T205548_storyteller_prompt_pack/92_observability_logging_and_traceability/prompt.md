# 92 — Observability, Logging, and Traceability

Read `base_prompt.md` first and preserve all prior prompt work.

## Objective

Make it practical to understand what happened inside the app across API requests, worker jobs, model calls, and artifact generation.

## Build
- Add structured logging with request IDs or session IDs flowing through API, worker, and model-service layers.
- Log important lifecycle events for composition and audio jobs without dumping excessive private content.
- Document how to inspect logs during local development and CI failures.

## Deliverables

- Structured logging setup
- Correlated identifiers across services
- Developer observability notes

## Acceptance checks

- A developer can trace a failing session through logs.
- Logs are useful for debugging but avoid gratuitous raw content exposure.
- The worker and API logs can be correlated.

## Notes

Good logging will save you repeatedly.

## Suggested commit label

`feat(prompt-92): observability and logging`
