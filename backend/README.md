# Backend

This directory is the home for the FastAPI application, backend-owned workflow logic, durable
relational models, and durable background job processing.

## Current layout

- `app/`: live application code
  - `api/`: unversioned and versioned route modules
  - `db/`: SQLAlchemy metadata, ORM models, engine/session helpers, and health placeholders
  - `models/`: API response models and future domain models
  - `services/`: backend-owned business logic, including the shared story workflow tool registry
  - `settings/`: environment-backed application settings
  - `storage/`: object storage abstraction, bucket/path strategy, and emulator smoke test
  - `worker/`: the durable PostgreSQL-backed worker loop and handler registry
- `alembic.ini`: migration configuration entrypoint
- `migrations/`: Alembic schema history and migration environment
- `tests/`: backend test suite
- `requirements.txt`: Python dependencies
- `Dockerfile`: multi-stage backend container image for development and runtime targets

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
pytest --run-integration -m integration tests/integration
python -m ruff check app tests
python -m ruff format app tests
uvicorn app.main:app --reload --host 0.0.0.0 --port 8565
python -m app.worker --once
alembic upgrade head
alembic downgrade base
python -m app.seed_catalog
python -m app.storage.smoke_test
python -m app.maintenance.artifact_cleanup
```

## Container targets

`backend/Dockerfile` now exposes two explicit targets:

- `development`: installs the full Python dependency set from `requirements.txt` for local bind-mounted Compose development
- `runtime`: installs only `requirements.runtime.txt` so the API and worker can share a smaller production-oriented image

The local Compose wrapper uses the `development` target through
[`infra/compose/docker-compose.dev.yml`](/Users/kevin/code/storyteller/infra/compose/docker-compose.dev.yml).
The base runtime compose file uses the `runtime` target for both `backend` and `worker`.

Structured logging and request or job correlation notes live in
[docs/observability-and-logging.md](/Users/kevin/code/storyteller/docs/observability-and-logging.md).

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

## Integration tests

The durable data-layer integration suite lives under
[`backend/tests/integration`](/Users/kevin/code/storyteller/backend/tests/integration). These
tests talk to the real local Postgres service and the file-backed fake GCS server instead of using
SQLite or mocked HTTP transports.

Run the suite from the repo root:

```bash
make backend-integration-test
```

That target starts `postgres` and `gcs` if needed, creates a disposable PostgreSQL database with
Alembic, reuses the local fake GCS server on `http://127.0.0.1:8568`, and runs only
`pytest.mark.integration` tests. The default `make backend-test` path keeps skipping these tests so
the fast unit loop stays fast.

Manual invocation from `backend/` is also supported:

```bash
STORYTELLER_RUN_INTEGRATION_TESTS=1 \
STORYTELLER_INTEGRATION_POSTGRES_ADMIN_URL="postgresql+psycopg://storyteller:storyteller@127.0.0.1:8567/postgres" \
STORYTELLER_INTEGRATION_GCS_ENDPOINT="http://127.0.0.1:8568" \
python -m pytest --run-integration -m integration tests/integration
```

GitHub Actions now treats `make backend-integration-test` as the durable-state gate after booting
the same Compose-backed infrastructure. That keeps local and CI behavior aligned and makes
migration, queue-claim, and storage regressions visible before higher-level workflow prompts add
more state.

## Background jobs

The durable queue now lives in the `background_jobs` table and is claimed directly from PostgreSQL,
so long-running story and audio work can move out of API request threads without adding Redis or a
second queue store.

Core entrypoints:

- `BackgroundJobService.enqueue_job(...)`: create a queued job row with a JSON payload
- `BackgroundJobService.claim_next_job(...)`: lease one queued or expired in-progress job
- `BackgroundJobService.heartbeat_job(...)`: extend the lease while work is still running
- `python -m app.worker`: run the polling worker against the configured database

The default worker registry includes:

- `demo.echo`: smoke-test handler for queue verification
- `story.*`: registry-backed story workflow tool handlers such as pitch generation, setup updates,
  composition, and audio start-up

The shared story workflow tool registry lives in
[`backend/app/services/story_tools.py`](/Users/kevin/code/storyteller/backend/app/services/story_tools.py)
with typed request and result models in
[`backend/app/models/story_tools.py`](/Users/kevin/code/storyteller/backend/app/models/story_tools.py).
Reviewer-facing documentation for the registry is in
[docs/story-workflow-tool-registry.md](/Users/kevin/code/storyteller/docs/story-workflow-tool-registry.md).

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
- `python -m app.maintenance.artifact_cleanup`: dry-run or apply conservative artifact cleanup

The bucket and prefix conventions are documented in
[docs/storage-buckets-and-prefixes.md](/Users/kevin/code/storyteller/docs/storage-buckets-and-prefixes.md).

To verify the local fake GCS server from the repository root:

```bash
make backend-storage-smoke
make backend-artifact-cleanup-dry-run
```

That target defaults to `http://127.0.0.1:8568` so it can talk to the local emulator from the host
shell even when the main Compose backend container uses `http://gcs:4443` internally.

Artifact lifecycle rules and the cleanup policy are documented in
[docs/artifact-retention-policy.md](/Users/kevin/code/storyteller/docs/artifact-retention-policy.md).

## Health routes

- `GET /health`: primary service health endpoint
- `GET /api/v1/health`: versioned API health endpoint
- `GET /api/hello`: compatibility endpoint kept for the current frontend scaffold

More detail on file discovery, supported YAML shape, and matching environment variables is in [docs/secrets-and-local-config.md](/Users/kevin/code/storyteller/docs/secrets-and-local-config.md).
