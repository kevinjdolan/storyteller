# Storyteller

Storyteller is a local-first, full-stack app for creating bedtime stories from first idea to finished text and finished narration audio. The product is session-based: the first meaningful screen is a past-sessions view where a user can resume work in progress, reopen a completed story, or start a new session.

This repository currently contains the first scaffold for that system. The project charter in this README and the supporting docs define the product and architecture that later prompts will implement.

## Product Vision

The app should feel like a guided bedtime story studio, not a generic prompt box. A user should be able to:

- See past sessions first and continue where they left off.
- Collaborate through both chat and direct UI controls.
- Move through a structured planning workflow before long-form writing starts.
- Watch story composition and audio generation progress in real time.
- Return later to read, listen, download, or revise completed work.

The tone of the product should stay calm, readable, and trustworthy. Wonder, mystery, and adventure are welcome, but bedtime suitability is a hard requirement: emotional stakes should resolve safely and the ending should feel restful.

## Required Story Workflow

The application is being built around this ordered workflow:

1. Genre selection
2. Tone selection
3. Story setup / free-form brief
4. Story pitches
5. Character sheet
6. Save-the-Cat beat sheet
7. Story setup preferences such as word count, runtime, and chapters
8. Composition
9. Audio configuration and audio generation
10. Finalize / read / listen / download

Each stage must be durable, resumable, and editable. Chat messages can propose actions in the workflow, and direct UI actions must also be reflected back into the session chat log as compact summaries.

## Fixed Technical Decisions

These choices are not optional for this project:

- Frontend: React + Vite + TypeScript
- Backend: Python + FastAPI
- Structured data: PostgreSQL
- Blob storage: file-backed GCS emulator in local development
- Local orchestration: Docker Compose
- Secrets handling: local `secrets.yaml`, never committed to git
- AI access: Gemini 3.1 family behind backend-owned adapters and services

Two architectural rules follow from those constraints:

- The browser must never hold provider secrets or call Gemini directly.
- Long-running story composition and narration generation must be durable background jobs with resumable server-side state.

More detail is in [docs/product-brief.md](/Users/kevin/code/storyteller/docs/product-brief.md) and [docs/architecture-overview.md](/Users/kevin/code/storyteller/docs/architecture-overview.md).

## Local Development Expectations

The repo is intended to run locally with Docker Compose. At the current scaffold stage:

- `frontend/` contains a Vite React app served on `http://localhost:8566`
- `backend/` contains a FastAPI app served on `http://localhost:8565`
- `tools/webapp-qa/` contains the browser automation container used for local UI verification

Start the current stack with:

```bash
docker compose up --build
```

The current scaffold does not yet include PostgreSQL or the file-backed GCS emulator, but both are required parts of the target system and will be added through later prompt work. `secrets.yaml` is already gitignored and reserved for local-only credentials.

## Repository Shape

- `frontend/`: React + Vite client application
- `backend/`: FastAPI application and future domain services
- `docs/`: product and architecture notes
- `prompts/`: sequential build prompts and task summaries
- `tools/`: local QA and developer tooling

## What Success Looks Like

A new engineer should be able to open this repository and quickly understand:

- the first screen is the past-sessions home for resume, edit, and create flows
- the story workflow is staged and ordered
- the final product writes stories and generates narration audio durably
- the backend owns AI access, long-running jobs, and persistent state
