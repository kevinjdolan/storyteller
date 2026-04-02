# Prompt 11 Summary: PostgreSQL Schema and Database Migrations

## What I changed and why

I implemented the first real relational persistence layer for Storyteller so the backend now has an explicit PostgreSQL schema instead of only settings placeholders and prose documentation.

The work centered on three goals:

1. establish a durable relational core for the session workflow
2. make schema changes reproducible from zero with Alembic
3. prove the schema works both in automated tests and against a real PostgreSQL instance

The main code changes are:

- `backend/app/db/base.py`
  - Added the shared SQLAlchemy declarative base.
  - Added naming conventions for constraints and indexes so future migrations stay stable.
  - Added UUID and timestamp mixins for consistent primary-key and audit columns.
- `backend/app/db/session.py`
  - Added engine and session-factory helpers.
  - Added SQLite connection handling for local metadata and migration tests.
- `backend/app/db/models.py`
  - Added the first ORM model set for the relational core.
  - Introduced enums for jobs, assets, and event actors.
  - Added relational models for:
    - `genres`
    - `tone_profiles`
    - `story_sessions`
    - `workflow_stage_states`
    - `story_briefs`
    - `pitches`
    - `character_sheets`
    - `beat_sheets`
    - `story_setups`
    - `composition_jobs`
    - `composition_segments`
    - `audio_jobs`
    - `export_assets`
    - `event_log_entries`
- `backend/alembic.ini`
  - Added the Alembic CLI entrypoint.
- `backend/migrations/env.py`
  - Added migration runtime wiring to the SQLAlchemy metadata.
  - Made Alembic prefer an explicitly configured database URL and then `STORYTELLER_DATABASE_URL` before falling back to full app settings.
- `backend/migrations/versions/20260331_01_initial_storyteller_schema.py`
  - Added the first schema revision with all tables, foreign keys, indexes, and downgrade steps.
- `backend/tests/test_db_models.py`
  - Added ORM-level tests that create realistic in-progress and completed sessions without collapsing everything into a JSON blob.
- `backend/tests/test_migrations.py`
  - Added an Alembic zero-to-head-to-base-to-head cycle test against a temporary SQLite database.
- `backend/README.md`
  - Documented local migration commands and how the migration environment resolves database URLs.
- `backend/migrations/README.md`
  - Documented the current migration scope and the operational migration commands.
- `docs/domain-model.md`
  - Clarified how prompt 11 keeps the relational core mostly one-directional to avoid circular foreign-key problems in the first schema.
- `docs/architecture-overview.md`
  - Updated the architecture notes to reflect the new SQLAlchemy and Alembic foundation.
- `backend/Dockerfile`
  - Included `alembic.ini` and `migrations/` in the backend image so the migration tooling is available inside the container build context.

## Architectural changes across the codebase

### 1. The backend now has a real persistence foundation

Before this prompt, `backend/app/db/` was effectively a placeholder. After this change it contains:

- shared SQLAlchemy metadata and naming conventions
- concrete ORM models
- engine and session helpers
- migration-aware schema ownership

That gives later prompts a stable base for repositories, services, workers, and durable job orchestration instead of forcing each prompt to invent ad hoc tables or direct SQL.

### 2. The schema matches the workflow contract instead of hiding state in a single blob

The relational design intentionally preserves the workflow model established in prompt 10:

- `story_sessions` stores the session-level snapshot fields needed for lists and resume behavior
- `workflow_stage_states` stores per-stage truth explicitly
- generated planning records such as pitches, character sheets, beat sheets, and story setup revisions are versioned rows tied to the session
- composition and audio work are represented as durable job records
- composition segment rows already exist so the writing pipeline can resume incrementally later
- `event_log_entries` gives the backend an append-only audit trail
- `export_assets` separates artifact metadata from the database rows that reference those assets

This means an in-progress or completed session can now be modeled relationally with direct query paths instead of relying on one giant JSON snapshot.

### 3. The first migration is explicit, not magic

I kept the initial revision hand-written rather than blindly relying on autogenerate output. That made a few things much clearer and safer:

- table creation order is intentional
- foreign-key `ondelete` behavior is deliberate
- the downgrade path is explicit
- indexes for obvious session, job, and audit queries are spelled out

### 4. The first schema avoids fragile circular dependencies

One deliberate design choice in prompt 11 is that accepted planning rows are tracked on the child records themselves, for example `is_selected` or `is_active`, while those rows point back to the owning session.

I chose that shape because it keeps the initial relational core clean and avoids a web of circular foreign keys between `story_sessions` and every accepted child table on day one. The API can still expose selected child IDs by querying the accepted child rows. I documented that choice in `docs/domain-model.md`.

## New abstractions, helpers, and extension points

### SQLAlchemy base and mixins

Use the shared base and mixins from `backend/app/db/base.py` for any future durable table:

```python
from app.db.base import Base, TimestampMixin, UUIDPrimaryKeyMixin


class ExampleRecord(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "example_records"
```

This keeps primary keys, timestamps, and naming conventions aligned across future revisions.

### Database engine/session helpers

Use `make_engine()` when tests or scripts need an explicit connection, and `get_engine()` / `get_session_factory()` when application code should use the configured runtime database:

```python
from app.db import get_session_factory, make_engine

engine = make_engine("sqlite+pysqlite:///:memory:")
SessionFactory = get_session_factory()
```

### Migration commands

Upgrade the local Compose PostgreSQL database to the latest schema:

```bash
cd backend
STORYTELLER_SECRETS_FILE="" \
STORYTELLER_DATABASE_URL="postgresql+psycopg://storyteller:storyteller@127.0.0.1:8567/storyteller" \
alembic upgrade head
```

Generate a follow-on revision after model changes:

```bash
cd backend
STORYTELLER_SECRETS_FILE="" \
STORYTELLER_DATABASE_URL="postgresql+psycopg://storyteller:storyteller@127.0.0.1:8567/storyteller" \
alembic revision --autogenerate -m "describe change"
```

### Session modeling example

The new ORM layer can represent a resumable session with explicit relational links instead of a large opaque payload:

```python
story_session = StorySession(
    current_stage=WorkflowStage.COMPOSITION,
    resume_stage=WorkflowStage.COMPOSITION,
    overall_status=WorkflowStageState.IN_PROGRESS,
)

stage_state = WorkflowStageSnapshot(
    session=story_session,
    stage=WorkflowStage.COMPOSITION,
    status=WorkflowStageState.IN_PROGRESS,
)

composition_job = CompositionJob(
    session=story_session,
    job_kind=CompositionJobKind.DRAFT,
    status=JobStatus.IN_PROGRESS,
)
```

That is exactly the kind of shape the new tests exercise.

## Exact verification work performed

### Focused backend verification during implementation

Command:

```bash
cd backend && .venv/bin/python -m ruff check app tests
```

Result:

- Passed after fixing import ordering and the long-line issue in the new ORM tests.

Command:

```bash
cd backend && .venv/bin/python -m pytest \
  tests/test_db_models.py \
  tests/test_migrations.py \
  tests/test_workflow.py \
  tests/test_health.py \
  tests/test_settings.py
```

Result:

- Passed.
- 19 backend tests passed.

Coverage of interest:

- realistic relational modeling for in-progress and completed sessions
- expected tables, indexes, and foreign keys
- Alembic zero-to-head-to-base-to-head cycle on SQLite
- preservation of existing workflow, health, and settings behavior

### Broad repository verification

Command:

```bash
make check
```

Result:

- Passed twice: once after the main implementation and again after the live Postgres fixes.
- Frontend Prettier check passed.
- Frontend ESLint passed.
- Backend Ruff format check and lint passed.
- Backend pytest suite passed: 19 tests.
- Frontend Vitest passed: 5 tests across 2 files.
- Frontend production build passed.

### Live PostgreSQL migration verification

I explicitly validated the Alembic history against the real Compose PostgreSQL service instead of relying only on SQLite.

Commands used:

```bash
./scripts/dev-compose.sh up -d postgres
./scripts/dev-compose.sh exec -T postgres psql -U storyteller -d postgres \
  -c "DROP DATABASE IF EXISTS storyteller_prompt11;" \
  -c "CREATE DATABASE storyteller_prompt11;"

cd backend
STORYTELLER_SECRETS_FILE="" \
STORYTELLER_DATABASE_URL="postgresql+psycopg://storyteller:storyteller@127.0.0.1:8567/storyteller_prompt11" \
  .venv/bin/alembic upgrade head

./scripts/dev-compose.sh exec -T postgres psql -U storyteller -d storyteller_prompt11 \
  -c "SELECT tablename FROM pg_tables WHERE schemaname = 'public' ORDER BY tablename;"

cd backend
STORYTELLER_SECRETS_FILE="" \
STORYTELLER_DATABASE_URL="postgresql+psycopg://storyteller:storyteller@127.0.0.1:8567/storyteller_prompt11" \
  .venv/bin/alembic downgrade base

cd backend
STORYTELLER_SECRETS_FILE="" \
STORYTELLER_DATABASE_URL="postgresql+psycopg://storyteller:storyteller@127.0.0.1:8567/storyteller_prompt11" \
  .venv/bin/alembic upgrade head
```

Observed results:

- `upgrade head` succeeded against PostgreSQL after the Alembic URL-resolution fix and the long identifier fix.
- The migrated database contained the expected application tables plus `alembic_version`.
- `downgrade base` succeeded.
- After downgrade, only `alembic_version` remained in the temporary database.
- A second `upgrade head` succeeded.
- I removed the temporary verification database afterward with:

```bash
./scripts/dev-compose.sh exec -T postgres psql -U storyteller -d postgres \
  -c "DROP DATABASE IF EXISTS storyteller_prompt11;"
```

### Browser checks, screenshots, and UI verification

Not applicable for this prompt.

Reason:

- The task only changed backend persistence, migrations, and documentation.
- No frontend rendering, styling, or interactive UI behavior changed.

### Remaining verification limits

- I did not add repository-layer integration tests yet because repositories do not exist in this prompt.
- I did not run application startup against the full backend service path with migrations wired into container startup, because automatic migration-on-boot is not part of this prompt.
- I did not seed genres or tones yet; seeding belongs more naturally with the later prompt focused on catalog data.

## LLM or prompt evaluation suite

No LLM or prompt-facing logic changed in this prompt.

Result:

- No evaluation suite was added.
- Named criteria: not applicable.
- Measured values: not applicable.

## Wrong turns, dead ends, surprising behavior, and gotchas

### 1. Alembic initially still depended on unrelated app settings

My first `migrations/env.py` implementation would only use the Alembic config URL or else fall back to `get_settings()`. During live PostgreSQL verification that failed because the migration command only needs a database URL, but the full app settings loader also requires Gemini and GCS settings.

Fix:

- I changed the environment to prefer an explicit `sqlalchemy.url` first, then `STORYTELLER_DATABASE_URL`, and only then fall back to full app settings.

Why it mattered:

- Without that fix, `alembic upgrade head` would be operationally annoying and brittle in local or CI contexts that only want schema access.

### 2. PostgreSQL caught a constraint-name limit that SQLite did not

The self-referential foreign key on `composition_segments.superseded_by_segment_id` originally used a very long generated-style name. SQLite tests passed, but PostgreSQL rejected it because the identifier exceeded the 63-character limit.

Fix:

- I shortened that constraint to `fk_comp_segments_superseded_by` in both the ORM model and the initial migration.

Why it mattered:

- This is exactly why I ran the live Postgres verification rather than declaring success after the SQLite migration test.

### 3. The test environment’s default Postgres URL can interfere with Alembic tests

`backend/tests/conftest.py` sets a default `STORYTELLER_DATABASE_URL` for the existing test suite. Once I taught Alembic to honor that environment variable, the migration test started accidentally targeting PostgreSQL instead of its temporary SQLite database.

Fix:

- I kept the resolver order as:
  1. explicit Alembic config URL
  2. `STORYTELLER_DATABASE_URL`
  3. full app settings

That preserved the SQLite migration test while still making live local migrations easy to run.

## Assumptions I made while working unsupervised

- The initial schema should favor a clean relational core over storing every “selected child ID” directly on `story_sessions` if doing so would introduce a large number of circular foreign keys in the first revision.
- Generic `JSON` columns are sufficient for the flexible model-output portions of prompt 11; there was no need to lock into PostgreSQL-only `JSONB` yet.
- Composition needs a `composition_segments` table now, even though the prompt did not list it explicitly, because resumable writing is already part of the documented domain model and the schema would be underspecified without it.
- Audio segments can wait for a later prompt focused on narration segmentation; a durable `audio_jobs` table is enough for prompt 11.
- Migration commands should be documented in the backend docs rather than introduced as new top-level `make` targets in this prompt.
- No browser-based verification was necessary because there were no UI changes.

## Reviewer-oriented takeaway

This prompt leaves the repository with:

- a real SQLAlchemy data model
- a first Alembic revision that migrates a fresh database from zero to head
- automated proof that the schema can model real session state
- documentation for how to run and extend migrations locally
- successful verification on both SQLite and real PostgreSQL

That should unblock the next prompts around repositories, session services, catalog seeding, event replay, and job orchestration without another persistence foundation refactor.
