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

More detail is in [docs/product-brief.md](/Users/kevin/code/storyteller/docs/product-brief.md), [docs/architecture-overview.md](/Users/kevin/code/storyteller/docs/architecture-overview.md), [docs/system-diagram.md](/Users/kevin/code/storyteller/docs/system-diagram.md), and [docs/adr/0001-core-runtime-architecture.md](/Users/kevin/code/storyteller/docs/adr/0001-core-runtime-architecture.md).

## Local Development Expectations

The repo is intended to run locally with Docker Compose. At the current scaffold stage:

- `frontend/` contains a Vite React app served on `http://localhost:8566`
- `backend/` contains a FastAPI app served on `http://localhost:8565`
- `infra/compose/` holds the canonical Compose file for local orchestration
- `tools/webapp-qa/` contains the browser automation container used for local UI verification

Bootstrap a new clone with:

```bash
make bootstrap
```

That command:

- creates `secrets.yaml` from `secrets.example.yaml` if it does not exist yet
- installs the repo-managed Git hooks
- creates or refreshes `backend/.venv`
- syncs `frontend/node_modules`

Then start the local stack with:

```bash
make up
```

The local Compose stack includes:

- `frontend` on `http://localhost:8566`
- `backend` on `http://localhost:8565`
- `postgres` on `localhost:8567`
- `gcs` on `http://localhost:8568`

`secrets.yaml` is already gitignored and reserved for local-only credentials. `make bootstrap` will create it from `secrets.example.yaml` when needed, but you still need to replace the placeholder Gemini API key before using AI-backed workflows. The repo-managed Git hook blocks accidental commits of `secrets.yaml`, `.env` files, and obvious live key material. The compose file uses development defaults for Postgres and the GCS emulator, while the backend loads secrets from the repo-root `secrets.yaml` at container startup.

## Daily Workflow

The repository now exposes a small top-level command surface through the root `Makefile`:

```bash
make help
```

The most common daily commands are:

- `make bootstrap`: first-run setup for hooks, local Python deps, frontend deps, and a local `secrets.yaml`
- `make up`: build and start the Docker Compose stack in detached mode
- `make logs`: follow the compose logs without restarting anything
- `make down`: stop the stack and preserve local Postgres and fake GCS data
- `make reset`: stop the stack and remove only the Postgres and fake GCS data volumes
- `make format`: apply Prettier to the frontend and Ruff formatting to the backend
- `make format-check`: verify formatting for both stacks without changing files
- `make lint`: run frontend ESLint and backend Ruff lint checks
- `make test`: run backend pytest and frontend Vitest
- `make build`: run the frontend production build
- `make check`: run formatting checks, lint, tests, and the frontend build in one pass

Suggested daily loop:

1. `make up`
2. make changes in `frontend/` or `backend/`
3. `make format` before or after a focused edit pass
4. `make logs` when you need live service output
5. `make test` for targeted automated coverage
6. `make check` before handing work off or committing
7. `make down` when you are done

For frontend-only work, `make frontend-format`, `make frontend-format-check`, `make frontend-lint`, `make frontend-test`, and `make frontend-build` are available as narrower targets. For backend-only work, use `make backend-format`, `make backend-format-check`, `make backend-lint`, and `make backend-test`.

## Docker Compose Local Stack

Use `make up`, `make down`, and `make logs` for the common compose workflow. The existing wrapper script remains the canonical compose entrypoint underneath those targets, so advanced commands can still go through:

```bash
./scripts/dev-compose.sh ps
```

Persistent data lives in named Docker volumes:

- `storyteller_postgres_data` for PostgreSQL
- `storyteller_gcs_data` for the file-backed GCS emulator

`make reset` removes only those two data volumes so schema or seed-data changes can start from a clean slate without forcing frontend or QA dependency reinstallation. If you intentionally want a full compose wipe, including cached dependency volumes, `./scripts/dev-compose.sh down --volumes` remains available as the deeper reset path.

The backend receives the local infrastructure coordinates through environment variables in Compose:

- `STORYTELLER_DATABASE_URL=postgresql://storyteller:storyteller@postgres:5432/storyteller`
- `STORYTELLER_GCS_ENDPOINT=http://gcs:4443`
- `STORYTELLER_GCS_SESSIONS_BUCKET_NAME=storyteller-sessions`
- `STORYTELLER_GCS_AUDIO_BUCKET_NAME=storyteller-audio`
- `STORYTELLER_GCS_EXPORTS_BUCKET_NAME=storyteller-exports`
- `STORYTELLER_GCS_PROJECT_ID=storyteller-local`
- `STORYTELLER_GCS_PUBLIC_URL=http://localhost:8568`

The backend settings layer merges defaults, `secrets.yaml`, and environment variables in that order. More detail is in [docs/secrets-and-local-config.md](/Users/kevin/code/storyteller/docs/secrets-and-local-config.md).

The root `Makefile` and the scripts under `scripts/` are written for `bash` and are intended for macOS, Linux, or WSL-based development environments. They expect `make`, Docker, `npm`, and Python 3.10 or newer to be available locally.

## Repository Shape

```text
.
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── db/
│   │   ├── models/
│   │   ├── services/
│   │   ├── settings/
│   │   ├── main.py
│   │   └── worker/
│   ├── tests/
│   ├── migrations/
│   ├── Dockerfile
│   ├── README.md
│   └── requirements.txt
├── docs/
├── frontend/
├── infra/
│   ├── compose/
│   │   └── docker-compose.yml
│   └── persistence/
├── prompts/
├── scripts/
├── test-assets/
└── tools/
    └── webapp-qa/
```

- `frontend/`: browser client and TypeScript UI foundation
- `backend/`: FastAPI API code, settings, services, tests, worker home, and migration home
- `infra/`: Compose definitions and infrastructure notes
- `docs/`: product notes, architecture notes, and future ADRs
- `scripts/`: developer entrypoints such as `dev-compose.sh`
- `test-assets/`: reusable fixtures for UI, audio, and integration testing
- `prompts/`: sequential build prompts and task summaries
- `tools/`: local QA and developer tooling

## What Success Looks Like

A new engineer should be able to open this repository and quickly understand:

- the first screen is the past-sessions home for resume, edit, and create flows
- the story workflow is staged and ordered
- the final product writes stories and generates narration audio durably
- the backend owns AI access, long-running jobs, and persistent state
