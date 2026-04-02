# 00 — Project Charter and Success Criteria

Read `base_prompt.md` first and preserve all prior prompt work.

## Objective

Create the initial project framing for a full-stack app that helps a user build a bedtime story, turn it into audio, and resume past sessions.

## Build
- Write a top-level README that explains the product vision, the end-to-end story workflow, the required stages, and the major technical choices already fixed by the brief.
- Document the non-negotiable requirements: React + Vite frontend, Python FastAPI backend, PostgreSQL for all structured data, a file-backed GCS emulator for blobs, Docker Compose for local orchestration, and `secrets.yaml` kept out of git.
- Add a short architecture note describing why all Gemini calls must happen on the backend and why long-running composition and audio jobs need resumable server-side state.

## Deliverables

- `README.md` with product overview and local development expectations
- `docs/product-brief.md` or equivalent design note
- `docs/architecture-overview.md` with the first cut of the system picture

## Acceptance checks

- A new engineer can read the repo root and understand what is being built.
- The required story stages from the brief are explicitly listed in order.
- The first screen requirement — a past-sessions screen for resume/edit/create — is called out early, not buried.

## Notes

Do not generate implementation code yet beyond lightweight documentation scaffolding.

## Suggested commit label

`feat(prompt-00): project charter`
