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
  - `storage/`: object storage abstraction, bucket/path strategy, and emulator smoke test
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
python -m app.seed_catalog
python -m app.storage.smoke_test
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

## Seeded catalog

The curated genre and tone catalog is stored in
[`app/data/genre_tone_catalog.yaml`](/Users/kevin/code/storyteller/backend/app/data/genre_tone_catalog.yaml)
and seeded with:

```bash
cd backend
python -m app.seed_catalog
```

For local Compose Postgres:

```bash
cd backend
STORYTELLER_SECRETS_FILE="" \
STORYTELLER_DATABASE_URL="postgresql+psycopg://storyteller:storyteller@127.0.0.1:8567/storyteller" \
python -m app.seed_catalog
```

Use `--dry-run` to validate the YAML file and report the expected write counts without committing.
Catalog provenance and editing guidance live in
[docs/genre-tone-catalog.md](/Users/kevin/code/storyteller/docs/genre-tone-catalog.md).

## Object storage

The storage abstraction now lives in
[`backend/app/storage`](/Users/kevin/code/storyteller/backend/app/storage). It hides the current
GCS JSON API calls behind a small service so later prompts can keep business logic focused on
session artifacts rather than bucket bootstrapping or emulator-specific HTTP details.

Core entrypoints:

- `build_object_storage_service(settings)`: build the runtime storage client from backend settings
- `object_storage.paths`: predictable bucket/key builders for draft, audio, export, and debug paths
- `python -m app.storage.smoke_test`: write and read a sample object through the configured backend

The bucket and prefix conventions are documented in
[docs/storage-buckets-and-prefixes.md](/Users/kevin/code/storyteller/docs/storage-buckets-and-prefixes.md).

To verify the local fake GCS server from the repository root:

```bash
make backend-storage-smoke
```

That target defaults to `http://127.0.0.1:8568` so it can talk to the local emulator from the host
shell even when the main Compose backend container uses `http://gcs:4443` internally.

## Health routes

- `GET /health`: primary service health endpoint
- `GET /api/v1/health`: versioned API health endpoint
- `GET /api/hello`: compatibility endpoint kept for the current frontend scaffold

More detail on file discovery, supported YAML shape, and matching environment variables is in [docs/secrets-and-local-config.md](/Users/kevin/code/storyteller/docs/secrets-and-local-config.md).
