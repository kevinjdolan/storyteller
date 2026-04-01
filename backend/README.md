# Backend

This directory is the home for the FastAPI application, backend-owned workflow logic, durable
relational models, and future background job processing.

## Current layout

- `app/`: live application code
  - `api/`: unversioned and versioned route modules
  - `db/`: SQLAlchemy metadata, ORM models, engine/session helpers, and health placeholders
  - `models/`: API response models and future domain models
  - `services/`: backend-owned business logic
  - `settings/`: environment-backed application settings
  - `worker/`: future background job runners
- `alembic.ini`: migration configuration entrypoint
- `migrations/`: Alembic schema history and migration environment
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

For local development, copy the repository-root example file and add a Gemini key:

```bash
cp ../secrets.example.yaml ../secrets.yaml
```

The settings module merges built-in defaults, `secrets.yaml`, and then `STORYTELLER_*` environment variables. Environment variables win when both sources set the same field. The backend-only Gemini key lives in `secrets.yaml` or the backend process environment and is never sent to the browser.

Useful commands:

```bash
pytest
python -m ruff check app tests
python -m ruff format app tests
uvicorn app.main:app --reload --host 0.0.0.0 --port 8565
alembic upgrade head
alembic downgrade base
```

## Database migrations

The first PostgreSQL schema now lives in SQLAlchemy models under
[`backend/app/db`](/Users/kevin/code/storyteller/backend/app/db) and the matching Alembic history
under [`backend/migrations`](/Users/kevin/code/storyteller/backend/migrations).

Run migrations against the local Compose Postgres instance:

```bash
cd backend
STORYTELLER_SECRETS_FILE="" \
STORYTELLER_DATABASE_URL="postgresql+psycopg://storyteller:storyteller@127.0.0.1:8567/storyteller" \
alembic upgrade head
```

Create a new revision after the models change:

```bash
cd backend
STORYTELLER_SECRETS_FILE="" \
STORYTELLER_DATABASE_URL="postgresql+psycopg://storyteller:storyteller@127.0.0.1:8567/storyteller" \
alembic revision --autogenerate -m "describe change"
```

The migration environment prefers an explicit `sqlalchemy.url` or `STORYTELLER_DATABASE_URL`. If
neither is supplied, it falls back to the application settings loader.

## Health routes

- `GET /health`: primary service health endpoint
- `GET /api/v1/health`: versioned API health endpoint
- `GET /api/hello`: compatibility endpoint kept for the current frontend scaffold

More detail on file discovery, supported YAML shape, and matching environment variables is in [docs/secrets-and-local-config.md](/Users/kevin/code/storyteller/docs/secrets-and-local-config.md).
