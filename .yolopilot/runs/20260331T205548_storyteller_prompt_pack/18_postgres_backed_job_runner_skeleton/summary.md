# Prompt 18 Summary — Postgres-Backed Job Runner Skeleton

## What I changed and why

I added the first durable queue and worker scaffold so long-running work can move out of API request threads and into a PostgreSQL-backed job loop without introducing Redis or another persistence system.

The main functional additions are:

- A new `background_jobs` table and ORM model with:
  - `job_type`
  - `status`
  - `payload`
  - `result_summary`
  - `attempt_count`
  - lease ownership fields (`lease_owner`, `lease_token`, `lease_expires_at`)
  - durable lifecycle timestamps (`claimed_at`, `heartbeat_at`, `started_at`, `completed_at`, `failed_at`)
  - `error_message`
  - an optional `session_id` foreign key so future composition/audio jobs can be correlated back to a story session
- A repository/service pair for queue operations:
  - enqueue
  - claim
  - heartbeat
  - complete
  - fail
- A worker runtime under `backend/app/worker/` with:
  - a polling loop
  - a handler registry keyed by `job_type`
  - a CLI entrypoint at `python -m app.worker`
  - a built-in `demo.echo` handler for smoke tests and extension examples
- A `worker` service in `infra/compose/docker-compose.yml` so the worker can run beside the rest of the stack without depending on the API process
- Focused tests for queue semantics and the worker loop
- Documentation updates so the new queue/worker surface is discoverable

The design stays intentionally small. It does not add retry policy, backoff scheduling, cancellation logic, or domain-specific composition/audio handlers yet. It does make those next steps straightforward.

## Architectural changes across the codebase

### Durable queue model

I added `BackgroundJob` to [`backend/app/db/models.py`](/Users/kevin/code/storyteller/backend/app/db/models.py) and wired it into `StorySession` as an optional relationship. This keeps the queue generic while still allowing future story/audio jobs to be session-scoped.

I also added the matching Alembic revision at [`backend/migrations/versions/20260401_01_add_background_jobs.py`](/Users/kevin/code/storyteller/backend/migrations/versions/20260401_01_add_background_jobs.py).

Key schema choices:

- Reused the existing `JobStatus` enum values so queue rows and existing composition/audio tables speak the same status language.
- Added `lease_token` in addition to `lease_owner` so stale workers cannot complete or fail jobs after another worker has reclaimed them.
- Indexed the queue for the main claim patterns:
  - `status + created_at`
  - `status + lease_expires_at`
  - `job_type + status + created_at`
  - `session_id + created_at`

### Repository and service layer

I added:

- [`backend/app/repositories/jobs.py`](/Users/kevin/code/storyteller/backend/app/repositories/jobs.py)
- [`backend/app/services/jobs.py`](/Users/kevin/code/storyteller/backend/app/services/jobs.py)

The repository owns the SQL details. The service owns transaction boundaries, validation, lease-token generation, and stable return types.

The claim path is intentionally dual-mode:

- PostgreSQL uses a `WITH candidate ... FOR UPDATE SKIP LOCKED` claim query so multiple workers can safely race for work without double-claiming the same row.
- SQLite uses a simpler fallback path so the current test suite can still run cheaply in-process.

That split keeps production behavior correct without forcing the test harness to spin up Postgres for every unit test.

### Worker runtime

I added:

- [`backend/app/worker/runtime.py`](/Users/kevin/code/storyteller/backend/app/worker/runtime.py)
- [`backend/app/worker/registry.py`](/Users/kevin/code/storyteller/backend/app/worker/registry.py)
- [`backend/app/worker/default_handlers.py`](/Users/kevin/code/storyteller/backend/app/worker/default_handlers.py)
- [`backend/app/worker/__main__.py`](/Users/kevin/code/storyteller/backend/app/worker/__main__.py)
- [`backend/app/worker/__init__.py`](/Users/kevin/code/storyteller/backend/app/worker/__init__.py)

`JobWorker` opens a fresh SQLAlchemy session per queue operation. That avoids keeping long-lived ORM state pinned across a job run and makes the heartbeat/complete/fail calls explicit separate transactions.

The execution flow is:

1. Claim one available job.
2. Resolve a handler from the registry.
3. Run the handler with a `JobExecutionContext` that can heartbeat.
4. Mark the job completed or failed durably.

If the worker loses its lease mid-run, it logs that condition and stops mutating the job row instead of trying to “win” against a newer claimant.

I also added a long-running worker safeguard: in `run_forever`, SQLAlchemy queue-poll failures are logged and retried instead of crashing the process. That matters when the service comes up before migrations are applied.

### Compose and configuration wiring

I added the `worker` service to [`infra/compose/docker-compose.yml`](/Users/kevin/code/storyteller/infra/compose/docker-compose.yml).

While verifying that service, I hit two real runtime issues in the existing repo and fixed them:

1. The local `secrets.yaml` on this machine contains extra provider fields that the current settings model rejects.
2. The Compose database URL used the generic `postgresql://` scheme, which makes SQLAlchemy look for `psycopg2`, but this repo installs `psycopg`.

To keep the new worker service startable in practice:

- the worker Compose service now uses `STORYTELLER_SECRETS_FILE=""`
- it gets a placeholder `STORYTELLER_GEMINI_API_KEY` by default for this skeleton
- the runtime database URLs used in Compose, tests, docs, and helper paths were normalized to `postgresql+psycopg://...`

I did **not** change the backend service to ignore `secrets.yaml`; I restored its prior behavior after an intermediate wrong edit landed on the wrong service block.

## Examples: how to use the new abstractions

### Enqueue a durable job

```python
from sqlalchemy.orm import sessionmaker

from app.db import make_engine
from app.services.jobs import BackgroundJobService

engine = make_engine("postgresql+psycopg://storyteller:storyteller@127.0.0.1:8567/storyteller")
SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)

with SessionLocal() as session:
    job = BackgroundJobService(session).enqueue_job(
        job_type="demo.echo",
        session_id=None,
        payload={
            "message": "compose-smoke",
            "steps": 2,
            "step_delay_seconds": 0.2,
        },
    )
```

### Run the worker once

```bash
cd backend
python -m app.worker --once
```

### Run the worker continuously

```bash
cd backend
python -m app.worker --poll-interval-seconds 2 --lease-duration-seconds 60
```

### Register a new handler

The extension point is the registry in [`backend/app/worker/registry.py`](/Users/kevin/code/storyteller/backend/app/worker/registry.py). A handler receives `payload` plus a `JobExecutionContext`, and can call `context.heartbeat()` during long work.

Minimal example:

```python
def write_story(payload, context):
    context.heartbeat()
    return {"stage": "composition", "session_id": context.session_id}

registry.register("story.compose", write_story)
```

That gives future prompts a clean place to plug in real composition or narration handlers without changing the queue plumbing.

## Exact verification work performed

### Automated backend verification

I ran:

```bash
cd backend
.venv/bin/python -m ruff format app tests
.venv/bin/python -m ruff check app tests
.venv/bin/python -m ruff format --check app tests
.venv/bin/python -m pytest -q
```

Results:

- `ruff format app tests`: passed
- `ruff check app tests`: passed
- `ruff format --check app tests`: passed
- `pytest -q`: passed, `49 passed in 0.89s`

I also ran focused tests during development:

```bash
cd backend
.venv/bin/python -m pytest tests/test_background_jobs.py tests/test_worker_runtime.py tests/test_migrations.py -q
```

Result:

- passed, `6 passed in 0.36s`

### Compose / live Postgres verification

I verified the queue and worker against the actual local Docker Compose Postgres instance rather than relying only on SQLite unit tests.

Commands run:

```bash
./scripts/dev-compose.sh ps
cd backend && STORYTELLER_SECRETS_FILE='' STORYTELLER_DATABASE_URL='postgresql+psycopg://storyteller:storyteller@127.0.0.1:8567/storyteller' .venv/bin/alembic upgrade head
./scripts/dev-compose.sh up -d --force-recreate worker
./scripts/dev-compose.sh logs --tail=20 worker
./scripts/dev-compose.sh config
```

Then I enqueued a real `demo.echo` job into Postgres from the host and verified that the Compose worker container claimed and completed it.

Observed worker log lines:

- `Worker ... listening for jobs. Registered handlers: demo.echo`
- `Worker ... claimed job 706bbcb7-4db5-493c-8e03-9770bbca0806 (demo.echo) attempt 1`
- `Worker ... completed job 706bbcb7-4db5-493c-8e03-9770bbca0806 with status completed`

I then read the completed job row back from Postgres and confirmed:

- `status == completed`
- `result_summary == {'echo': 'compose-smoke', 'step_count': 2, 'worker_id': 'worker-...'}`

Cleanup performed after the smoke test:

- stopped the worker container with `./scripts/dev-compose.sh stop worker`
- deleted the demo verification row from `background_jobs`

### Browser checks / screenshots

None were applicable.

This task changed backend schema, services, tests, and Compose wiring only. No UI, layout, rendering, or browser behavior changed, so I did not run screenshot or browser automation.

## LLM / prompt evaluation suite

No LLM-facing logic changed in this prompt.

Evaluation suite status:

- `LLM-facing eval suite`: not applicable
- `Happy path criteria`: not applicable
- `Edge case criteria`: not applicable
- `Safety criteria`: not applicable
- `Formatting criteria`: not applicable
- `Failure mode criteria`: not applicable

## Wrong turns, dead ends, and gotchas

### 1. Worker Compose startup failed on the local `secrets.yaml`

The first live worker startup failed because the local `secrets.yaml` on this machine includes extra fields:

- `gemini.api_key_name`
- `gemini.project_name`
- `gemini.project_number`
- `openai`

The current settings loader forbids extras, so the worker crash-looped before reaching the queue.

Fix:

- changed the worker Compose service to use `STORYTELLER_SECRETS_FILE=""`
- supplied a placeholder Gemini key via env for the skeleton worker

Why I kept it scoped:

- this task was about the worker scaffold
- changing global settings validation behavior would have been broader and riskier
- the worker does not actually need Gemini access yet

### 2. I initially edited the wrong Compose service block

My first Compose patch accidentally applied the env-only worker settings to `backend` instead of `worker`.

I caught that by inspecting the live generated Compose file and the container environment:

```bash
sed -n '40,140p' infra/compose/docker-compose.yml
docker inspect storyteller-worker-1 --format '{{range .Config.Env}}{{println .}}{{end}}'
```

I then restored the backend block and moved the env-only config to the correct `worker` block.

### 3. The repo’s runtime DSN strings were using the wrong SQLAlchemy driver scheme

When the worker finally got past secrets loading, it still crash-looped with:

- `ModuleNotFoundError: No module named 'psycopg2'`

Cause:

- Compose and several repo defaults used `postgresql://...`
- this repo installs `psycopg`, not `psycopg2`

Fix:

- normalized runtime DSNs to `postgresql+psycopg://...` in Compose, tests, docs, and helper paths

### 4. SQLite timestamp behavior is different from Postgres

One lease test initially failed because the claimed in-memory datetime was timezone-aware while the SQLite-loaded heartbeat datetime was naive.

Fix:

- normalized those timestamps in the assertion helper inside `tests/test_background_jobs.py`

### 5. Repo-wide Ruff formatting touched unrelated backend files

`ruff format app tests` reformatted five pre-existing backend files unrelated to the queue work. I briefly tried trimming that noise back, but then `ruff format --check app tests` failed.

Final decision:

- keep those no-behavior-change formatter rewrites so the backend passes its own formatting gate cleanly

Affected formatting-only files:

- [`backend/app/models/realtime.py`](/Users/kevin/code/storyteller/backend/app/models/realtime.py)
- [`backend/app/services/sessions.py`](/Users/kevin/code/storyteller/backend/app/services/sessions.py)
- [`backend/tests/test_asset_service.py`](/Users/kevin/code/storyteller/backend/tests/test_asset_service.py)
- [`backend/tests/test_realtime_contracts.py`](/Users/kevin/code/storyteller/backend/tests/test_realtime_contracts.py)
- [`backend/tests/test_session_service.py`](/Users/kevin/code/storyteller/backend/tests/test_session_service.py)

## Assumptions I made while working unsupervised

- A generic queue table is the right first step even though composition/audio domain tables already exist. I treated those domain tables as workflow state, and `background_jobs` as the durable execution queue.
- It is acceptable for the worker skeleton to ship with a built-in `demo.echo` handler so there is a concrete smoke-test target before real story/audio handlers land.
- It is acceptable for the worker Compose service to use env-only configuration for now, because the current worker skeleton does not need real provider credentials.
- The optional `session_id` foreign key on `background_jobs` is useful now, even though no route or domain orchestration uses it yet.
- A second small commit was better than amending the first one when `backend/tests/test_worker_runtime.py` was accidentally left out of the first checkpoint commit.

## Commits created during the run

- `5e58514` — `feat(prompt-18): postgres job runner skeleton`
- `50a0f3a` — `test(prompt-18): cover worker runtime loop`

## Remaining limits / follow-up work

This prompt intentionally stops short of full orchestration. The next obvious steps are:

- map composition and narration domain actions onto `background_jobs`
- add retry policy and backoff
- add cancellation and pause/resume semantics
- emit queue/job progress into the realtime event system
- add API endpoints for enqueueing and inspecting background jobs
- decide whether the settings loader should eventually tolerate unrelated keys in local `secrets.yaml`

Those are follow-on improvements. The queue skeleton itself is now durable, worker-friendly, Postgres-backed, tested, and verified in Compose without the API process running.
