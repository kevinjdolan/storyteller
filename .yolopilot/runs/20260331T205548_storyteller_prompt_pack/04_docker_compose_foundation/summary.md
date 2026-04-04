# Prompt 04 Summary: Docker Compose Foundation

## What I changed and why

I turned the existing minimal Compose scaffold into a first working local stack that includes the four required application services:

- `frontend` on `http://localhost:8566`
- `backend` on `http://localhost:8565`
- `postgres` on `localhost:8567`
- `gcs` on `http://localhost:8568`

I preserved the pre-existing `browser` QA container because it is already part of the repo’s local verification workflow and still composes cleanly with the new stack.

The main implementation changes were:

- Expanded [`infra/compose/docker-compose.yml`](/Users/kevin/code/storyteller/infra/compose/docker-compose.yml) to add:
  - a pinned `postgres:16-alpine` service
  - a pinned `fsouza/fake-gcs-server:1.54.0` service in HTTP + filesystem-backed mode
  - named volumes for PostgreSQL and fake GCS persistence
  - backend environment wiring for database and storage coordinates
  - a top-level Compose project name so the runtime gets stable, reviewer-friendly volume names like `storyteller_postgres_data` instead of generic `compose_*`
- Extended backend settings in [`backend/app/settings/config.py`](/Users/kevin/code/storyteller/backend/app/settings/config.py) to read the new local object-storage environment contract:
  - `STORYTELLER_GCS_BUCKET_NAME`
  - `STORYTELLER_GCS_ENDPOINT`
  - `STORYTELLER_GCS_PROJECT_ID`
  - `STORYTELLER_GCS_PUBLIC_URL`
- Added a minimal storage-status surface in [`backend/app/storage/status.py`](/Users/kevin/code/storyteller/backend/app/storage/status.py) and wired it into [`backend/app/services/health.py`](/Users/kevin/code/storyteller/backend/app/services/health.py) so the running backend can report whether object storage is configured, not just the database.
- Added/updated backend tests in:
  - [`backend/tests/test_health.py`](/Users/kevin/code/storyteller/backend/tests/test_health.py)
  - [`backend/tests/test_settings.py`](/Users/kevin/code/storyteller/backend/tests/test_settings.py)
- Updated repo docs so a fresh clone can start, stop, and reset the stack safely:
  - [`README.md`](/Users/kevin/code/storyteller/README.md)
  - [`infra/compose/README.md`](/Users/kevin/code/storyteller/infra/compose/README.md)
  - [`infra/persistence/README.md`](/Users/kevin/code/storyteller/infra/persistence/README.md)
  - [`scripts/README.md`](/Users/kevin/code/storyteller/scripts/README.md)
  - [`docs/architecture-overview.md`](/Users/kevin/code/storyteller/docs/architecture-overview.md)

## Architectural changes across the codebase

### 1. Compose moved from app-only scaffolding to actual local infrastructure orchestration

Before this prompt, the canonical Compose file only brought up the frontend, backend, and browser QA runner. After this change, the stack matches the project contract more closely:

- structured state has a local Postgres service
- blob/object state has a file-backed local GCS emulator
- both persistence layers have named Docker volumes
- the backend gets its infrastructure coordinates through environment variables rather than hardcoded knowledge

This is a meaningful architecture step because later prompts can now add repositories, migrations, and storage adapters against already-defined local infrastructure instead of inventing container/runtime assumptions ad hoc.

### 2. The backend now has a small but explicit storage configuration contract

I intentionally did not build a full storage adapter yet because later prompts are expected to own that. Instead, I added the minimum stable contract future code can build on:

- settings fields for database and GCS emulator coordinates
- a storage dependency status helper
- health response exposure so runtime config can be inspected from the app itself

That keeps prompt 04 boring and forward-compatible. The app still does not talk to Postgres or GCS directly yet, but it now knows where those services live and can report whether the runtime is configured for them.

### 3. Persistence is explicit and documented

I documented the volume behavior because “persistent across restarts” is a runtime property, not just a YAML property. The docs now distinguish:

- `./scripts/dev-compose.sh down`
  - stops containers and preserves data
- `./scripts/dev-compose.sh down --volumes`
  - intentionally wipes the Postgres and fake GCS volumes

## Examples of new abstractions, helpers, and extension points

### Compose usage

Start the local stack:

```bash
./scripts/dev-compose.sh up --build
```

Stop it but keep persistent data:

```bash
./scripts/dev-compose.sh down
```

Reset the local database and object storage:

```bash
./scripts/dev-compose.sh down --volumes
```

### Backend configuration contract

The backend now expects these runtime coordinates:

```text
STORYTELLER_DATABASE_URL=postgresql://storyteller:storyteller@postgres:5432/storyteller
STORYTELLER_GCS_ENDPOINT=http://gcs:4443
STORYTELLER_GCS_BUCKET_NAME=storyteller-dev
STORYTELLER_GCS_PROJECT_ID=storyteller-local
STORYTELLER_GCS_PUBLIC_URL=http://localhost:8568
```

Future repository/storage code can consume these through `get_settings()` instead of reaching into Compose assumptions directly.

### Health response extension point

The backend health payload now reports both infrastructure dependencies:

```json
{
  "dependencies": {
    "database": {
      "status": "configured"
    },
    "object_storage": {
      "status": "configured"
    }
  }
}
```

That gives later prompts a stable place to surface richer dependency diagnostics once real DB/storage clients are added.

## Exact verification work performed

### Static and test verification

I ran:

- `./scripts/dev-compose.sh config`
  - Passed. Verified the final rendered Compose file, service graph, explicit port mappings, and named volumes.
- `python -m pytest` from [`backend/`](/Users/kevin/code/storyteller/backend)
  - Passed: `4 passed in 0.01s`

Backend test coverage added/updated:

- `test_health_endpoint_returns_service_metadata`
- `test_versioned_health_endpoint_marks_the_api_version`
- `test_legacy_hello_endpoint_remains_available_for_existing_frontend_checks`
- `test_settings_read_database_and_object_storage_environment`

### Runtime Docker verification

I ran:

- `./scripts/dev-compose.sh up --build -d`
  - Passed. Built the local `frontend`, `backend`, and `browser` images and started all services.
- `./scripts/dev-compose.sh ps`
  - Confirmed:
    - `storyteller-backend-1` healthy
    - `storyteller-frontend-1` healthy
    - `storyteller-gcs-1` healthy
    - `storyteller-postgres-1` healthy
    - `storyteller-browser-1` running
- `curl -s http://localhost:8565/health`
  - Passed. Backend returned `database.status=configured` and `object_storage.status=configured`.
- `curl -s http://localhost:8566`
  - Passed. Frontend served the Vite HTML shell on the documented port.
- `curl -s http://localhost:8568/storage/v1/b`
  - Passed. Fake GCS responded on the documented port.
- `./scripts/dev-compose.sh exec -T postgres psql -U storyteller -d storyteller -c 'select 1 as ready;'`
  - Passed. Postgres returned `1`.
- `docker volume inspect storyteller_postgres_data storyteller_gcs_data`
  - Passed. Confirmed both named volumes exist with the expected Compose labels and mountpoints.
- `./scripts/dev-compose.sh down`
  - Passed. Stopped the stack cleanly while preserving the named volumes.

### Browser checks and screenshots

No browser screenshot run was added for this prompt.

Reason:

- I did not change any UI code, styles, layout, accessibility, or rendering behavior.
- I still verified the frontend container and dev server functionally by bringing the full stack up and fetching the served HTML over HTTP.

### Remaining verification limits

- I did not validate real application reads/writes against Postgres because the repository does not yet have database integration code.
- I did not validate real object uploads/downloads against the GCS emulator because the repository does not yet have a storage adapter or client code.
- I verified persistence structurally through named volume creation and Compose wiring, not through end-to-end application-level writes, because those higher-level integrations belong to later prompts.

## LLM or prompt evaluation suite

No LLM-facing behavior changed in this prompt.

Modified areas:

- Docker Compose
- runtime environment wiring
- backend health/config scaffolding
- documentation

Evaluation suite status:

- `happy_path_generation`: not applicable
- `structured_output_determinism`: not applicable
- `formatting_expectations`: not applicable
- `safety_constraints`: not applicable
- `failure_modes`: not applicable

Result:

- No LLM evaluation suite was added because prompt/model logic was not touched.

## Wrong turns, dead ends, and gotchas

- The repo already had a minimal Compose file in `infra/compose/`, so this prompt was an extension of existing scaffolding rather than a brand-new file. I preserved that direction instead of relocating Compose to the repository root.
- The active conda environment did not have the backend requirements installed. `pytest` was not on `PATH`, and `python -m pytest` initially failed with `No module named pytest`. I resolved that by installing the already-declared `backend/requirements.txt` into the active environment before running tests.
- The top-level Compose project name mattered more than it first appeared. Because the canonical file lives under `infra/compose/`, leaving the project unnamed would have produced generic volume names derived from that directory rather than the application name. Adding `name: storyteller` fixed that and made the persistence docs truthful and stable.
- I preserved the existing `browser` QA service even though the prompt only asked for four primary services. Removing it would have been a regression against the repo’s current development workflow.

## Assumptions I made while working unsupervised

- I assumed local, non-production Postgres credentials in Compose are acceptable for this prompt because they are development defaults, not provider secrets. I kept actual secret handling out of Compose and did not introduce any API-key material there.
- I assumed the existing `infra/compose/docker-compose.yml` location is intentional because the repo already ships `scripts/dev-compose.sh` as the developer entrypoint.
- I assumed adding a small backend storage-config surface in prompt 04 is preferable to keeping storage knowledge buried only in Compose, because later prompts will need those settings anyway.
- I assumed pinning the fake GCS image to a concrete tag is preferable to using `latest`, to keep local development reproducible.

## Final state

The repository now has a working local Compose foundation for:

- frontend
- backend
- PostgreSQL
- file-backed GCS emulation
- persistent local volumes

The stack starts from a fresh clone without hand-editing the Compose file, the runtime ports are explicit, the persistence paths are documented, and the backend can report its local infrastructure wiring through health/status output.
