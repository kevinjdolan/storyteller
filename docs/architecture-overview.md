# Architecture Overview

## System Picture

Storyteller is a full-stack application with a browser client, a backend-owned workflow engine, durable relational state, durable object storage, and resumable background jobs.

```text
React + Vite client
        |
        v
FastAPI API layer
        |
        +--> domain services and policy layer
        |         |
        |         +--> AI adapters for planning, composition, and narration
        |         |
        |         +--> repositories for sessions, workflow state, jobs, and event log
        |
        +--> background workers for composition and audio generation
                  |
                  +--> PostgreSQL for durable structured state
                  +--> file-backed GCS emulator for artifacts and intermediate blobs
```

## Why Gemini Calls Must Stay on the Backend

All Gemini access belongs on the server side for four reasons:

1. Secrets control: provider credentials live in local `secrets.yaml` and must never enter the browser.
2. Policy enforcement: chat-to-UI actions and workflow transitions need deterministic server validation before the model can change session state.
3. Durable orchestration: prompts, structured outputs, retries, and model selection need to be coordinated with persistent session data and job records.
4. Provider flexibility: keeping Gemini behind backend adapters lets the app keep a stable internal interface while model IDs, structured output tactics, or narration providers evolve.

The frontend should only call the backend's API and subscribe to backend-owned progress events.

## Why Composition and Audio Must Use Resumable Server-Side Jobs

Composition and narration are long-running operations that cannot safely live inside request threads or browser memory. They need server-side jobs because:

- a user must be able to refresh the page or return later without losing progress
- partial story text and audio segments need durable checkpoints
- progress updates need a single source of truth that both chat and UI can observe
- retries, cancellation, and resume logic need explicit job state rather than transient in-memory state

The durable model should include job records, segment records, asset metadata, and an event log that can reconstruct session progress after interruption.

## Intended Backend Shape

The target backend should separate concerns explicitly:

- `api/`: HTTP routes and websocket endpoints
- `settings/`: environment and secrets loading
- `db/`: database engine, migrations, and persistence setup
- `models/`: typed domain models and persistence schemas
- `repositories/`: database access for sessions, events, jobs, and assets
- `services/`: workflow logic and policy enforcement
- `ai/`: Gemini planning, composition, and narration adapters
- `worker/`: background job execution for writing and audio
- `storage/`: object storage abstraction over the local GCS emulator

## Durable Domain Concepts

The system should persist the following concepts as first-class records:

- Session
- Workflow stage
- Event log
- Selected genre
- Selected tone
- Story brief
- Pitch batch and selected pitch
- Character batch and selected character sheet
- Beat sheet
- Story setup preferences
- Outline or chapter plan
- Continuity bible
- Composition job and segments
- Audio job and segments
- Asset metadata

## Current Repository State

The repository currently contains an initial scaffold:

- `frontend/`: Vite React app
- `backend/`: FastAPI app
- `docker-compose.yml`: local frontend, backend, and browser QA services
- `tools/webapp-qa/`: containerized browser automation support

PostgreSQL, the file-backed GCS emulator, background workers, and most domain layers are still planned work. This document records the required direction so later prompts can extend the scaffold without changing the architectural contract.
