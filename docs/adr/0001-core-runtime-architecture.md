# ADR 0001: Core Runtime Architecture

- Status: Accepted
- Date: 2026-03-31

## Context

Storyteller is a session-based bedtime story studio, not a single-shot prompt demo. A user needs to move through a staged workflow, leave, come back later, and still see the current plan, generated text, generated audio, and recent activity.

That product shape creates a few non-negotiable technical pressures:

- the browser cannot hold Gemini credentials or call provider APIs directly
- session state needs to survive refreshes, restarts, and long-running work
- composition and audio generation are too slow and failure-prone to run inside request threads
- chat and direct UI actions both need an audit trail that can be replayed during resume
- generated files need durable storage that behaves like object storage during local development

This ADR records the first architecture decisions that later prompts should assume unless another ADR replaces them.

## Decision

### 1. AI calls stay on the backend

All Gemini text, planning, composition, and narration calls belong behind backend-owned adapters and services.

- The browser talks only to backend APIs and websocket streams.
- Provider secrets stay in local server-side configuration such as `secrets.yaml`.
- Model IDs stay centralized in backend settings and adapter code, not in frontend code or route handlers.
- The backend policy layer decides whether a model-suggested action is valid for the current workflow stage before state changes are accepted.

### 2. PostgreSQL is the durable source of truth

PostgreSQL owns the structured state required to resume a story session.

At minimum, later prompts should treat these as first-class durable records:

- session
- workflow stage
- durable event history
- selected genre and tone
- brief, pitch batch, selected pitch
- character sheet candidates and selection
- beat sheet
- story setup preferences
- composition jobs and segment progress
- audio jobs and segment progress
- asset metadata and references

Session resume should come from durable state, not browser cache. The event history is part of the product, not just an internal log, because it supports replay, auditability, and UI-to-chat echoes.

### 3. Generated artifacts live in object storage

Large generated files should not live inside PostgreSQL rows.

- PostgreSQL stores metadata, lifecycle state, references, and relationships.
- Story exports, intermediate composition files, narration segments, and final audio artifacts live in object storage.
- In local development, that object storage is the file-backed GCS emulator already defined in Docker Compose.

This keeps the local environment close to the production storage model without introducing a separate cloud dependency during development.

### 4. Live progress uses websocket delivery

The browser needs live updates during composition and audio generation, and those updates need to remain tied to durable backend state.

- HTTP handles regular reads, writes, and workflow actions.
- WebSockets handle session progress, job status, and incremental event delivery.
- On reconnect, the client should rehydrate from durable session state and recent event history before continuing with live updates.

The websocket channel is a delivery mechanism, not the source of truth. If a socket drops, the session must still be recoverable from PostgreSQL and storage.

### 5. Long-running generation runs in a separate worker process

Composition and audio generation run in a worker process that is separate from the API process.

- API routes create or update durable job records.
- Workers claim pending jobs, call Gemini or narration providers, persist partial outputs, and append durable events.
- The API remains responsible for request handling, policy checks, and websocket fan-out.

This separation keeps request latency predictable and makes pause, resume, retry, and interruption logic easier to reason about.

### 6. Word count, runtime, and chapter count are soft planning hints

Word count, estimated runtime, and chapter count are planning targets, not hard execution constraints.

- They guide pitch generation, beat planning, and composition prompts.
- They should influence heuristics, summaries, warnings, and progress estimates.
- They should not be enforced as exact cutoffs that distort story quality or bedtime tone.

The product should prefer a coherent, calm bedtime story over exact numeric compliance. If the system misses a target, it should do so transparently and gracefully rather than by truncating or padding the story unnaturally.

## Consequences

### Positive

- Secrets stay out of the browser.
- Resume and replay have a clear home in durable data.
- Long-running work can survive refreshes and restarts.
- Asset storage matches the product brief instead of turning the database into a file bucket.
- Later prompts have a clear split between API responsibilities and worker responsibilities.

### Costs and constraints

- The system is more complex than a single FastAPI process with synchronous handlers.
- Websocket delivery and worker orchestration add coordination work that later prompts must implement carefully.
- Developers need to think about job state transitions and event ordering early.

## Implementation Notes for Later Prompts

- Put websocket endpoints under backend API ownership, not in the frontend dev server.
- Treat the durable event history as product data that can be queried during session resume.
- Keep asset metadata relational even when the files themselves live in object storage.
- Resist pushing model calls into route handlers or browser-side helpers.
- If a later prompt needs to change any of these choices, record the override in a new ADR instead of silently drifting.
