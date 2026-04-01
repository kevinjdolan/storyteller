# Backend

This directory is the home for the FastAPI application, backend-owned workflow logic, and future durable job processing.

## Current layout

- `app/`: live application code
  - `api/`: unversioned and versioned route modules
  - `db/`: database integration points and health placeholders
  - `models/`: API response models and future domain models
  - `services/`: backend-owned business logic
  - `settings/`: environment-backed application settings
  - `worker/`: future background job runners
- `migrations/`: reserved for database migrations
- `tests/`: backend test suite
- `requirements.txt`: Python dependencies
- `Dockerfile`: backend container image

Planned expansion inside `app/` follows the architecture notes in [docs/architecture-overview.md](/Users/kevin/code/storyteller/docs/architecture-overview.md), including explicit homes for repositories, AI adapters, storage, and worker execution.

## Local run

Install dependencies and start the app from this directory:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m app
```

The local entrypoint reads `STORYTELLER_*` environment variables and defaults to:

- host: `0.0.0.0`
- port: `8565`
- environment: `development`
- versioned API prefix: `/api/v1`

Useful commands:

```bash
pytest
uvicorn app.main:app --reload --host 0.0.0.0 --port 8565
```

## Health routes

- `GET /health`: primary service health endpoint
- `GET /api/v1/health`: versioned API health endpoint
- `GET /api/hello`: compatibility endpoint kept for the current frontend scaffold
