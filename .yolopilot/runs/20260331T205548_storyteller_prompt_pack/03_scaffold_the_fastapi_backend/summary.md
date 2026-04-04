# 03 FastAPI Scaffold Summary

## What I changed and why

I replaced the backend's single-file FastAPI stub with a small, production-minded package layout that makes startup, routing, settings, and future service boundaries explicit.

The main implementation changes were:

- I turned `backend/app/main.py` from an inline app definition into an app factory with a lifespan hook.
  - `create_app()` now owns FastAPI initialization, router registration, and CORS setup.
  - The lifespan hook logs startup and shutdown and stores the resolved settings on `app.state`.
  - This gives later prompts a stable place to attach database setup, telemetry, or other runtime initialization without dumping more logic into route modules.

- I added a real configuration layer under `backend/app/settings/`.
  - `AppSettings` is a dataclass populated from `STORYTELLER_*` environment variables.
  - The settings loader currently handles app name, environment, version, host, port, reload mode, CORS origins, log level, API v1 prefix, and a placeholder database URL.
  - I kept the implementation boring and env-backed instead of jumping ahead to secrets-file loading because prompt 05 is explicitly about deeper settings and secrets handling.

- I introduced an API package with both unversioned and versioned routers.
  - `GET /health` is the primary service health endpoint.
  - `GET /api/v1/health` is the versioned health route under the configurable API v1 prefix.
  - `GET /api/hello` remains available as a compatibility route for the existing frontend status hook and prompt-02 smoke checks.

- I added backend-owned models and a simple service layer instead of returning anonymous dicts directly from routes.
  - `backend/app/models/system.py` contains `HealthResponse`, `HelloResponse`, and `DependencyStatus`.
  - `backend/app/services/health.py` builds the response payloads.
  - `backend/app/db/status.py` provides a minimal database status placeholder that reports configuration state without pretending a real database exists yet.

- I added a local entrypoint and backend tests.
  - `backend/app/__main__.py` allows `python -m app` from the `backend/` directory.
  - `backend/tests/test_health.py` verifies `/health`, `/api/v1/health`, and `/api/hello`.
  - `backend/tests/conftest.py` creates a `TestClient` fixture and clears cached settings between tests.

- I updated the developer-facing and container-facing wiring.
  - `backend/README.md` now documents the package layout, local run command, test command, and health routes.
  - `backend/Dockerfile` now defaults to `python -m app`.
  - `infra/compose/docker-compose.yml` now starts the backend with `python -m app` and uses `/health` for the container health check.
  - `README.md` and `docs/architecture-overview.md` were updated so the repo documentation matches the new backend shape.

I created one checkpoint commit during the run:

- `72e6065` — `feat(prompt-03): fastapi scaffold`

## Architectural changes across the codebase

### Backend runtime shape

The backend is no longer a single `FastAPI(...)` instance plus one inline route. The current structure is:

- `backend/app/main.py`: app factory, CORS registration, lifespan startup/shutdown
- `backend/app/__main__.py`: local run entrypoint
- `backend/app/settings/`: environment-backed settings resolution
- `backend/app/api/`: unversioned routes and shared router assembly
- `backend/app/api/v1/`: versioned route assembly
- `backend/app/models/`: response and future domain models
- `backend/app/services/`: backend-owned business logic
- `backend/app/db/`: persistence integration placeholders
- `backend/tests/`: backend-specific test coverage

This is intentionally plain and explicit. It makes future prompts easier to implement because there are obvious homes for route handlers, policy logic, and persistence wiring before the codebase grows.

### Startup and configuration flow

The app now resolves configuration once through `get_settings()`, builds the FastAPI app from those settings, and reuses that same configuration during startup. The current defaults are development-friendly, but every important value can already be overridden with `STORYTELLER_*` environment variables.

That gives later prompts a clean migration path for:

- secrets-backed config
- Postgres connection settings
- worker-specific config
- environment-specific API prefixes or CORS overrides

### API contract evolution without regressions

Prompt 03 asked for versioned router structure, but prompt 02 already shipped a frontend that talks to `/api/hello`. I treated preserving that route as a compatibility requirement, not dead weight.

The resulting contract is:

- `/health`: canonical health check for the service and Compose
- `/api/v1/health`: versioned route for future frontend/backend API growth
- `/api/hello`: temporary compatibility route for the existing frontend scaffold

That lets the repo move forward without breaking prior prompt work.

### Database boundary is visible but not fake

I did not invent a pretend database layer just to satisfy folder naming. Instead, `backend/app/db/status.py` exposes the single bit of truthful information the scaffold can currently provide: whether a database URL is configured.

The health responses therefore include:

- `database.status = "not-configured"` when no database URL exists
- a human-readable detail string explaining that real database wiring lands in a later prompt

This keeps the backend honest while still making the future persistence seam obvious.

## Key files touched

- `backend/app/main.py`
- `backend/app/__main__.py`
- `backend/app/settings/config.py`
- `backend/app/api/router.py`
- `backend/app/api/routes/health.py`
- `backend/app/api/routes/legacy.py`
- `backend/app/api/v1/router.py`
- `backend/app/api/v1/routes/health.py`
- `backend/app/models/system.py`
- `backend/app/services/health.py`
- `backend/app/db/status.py`
- `backend/tests/conftest.py`
- `backend/tests/test_health.py`
- `backend/README.md`
- `backend/Dockerfile`
- `backend/requirements.txt`
- `infra/compose/docker-compose.yml`
- `README.md`
- `docs/architecture-overview.md`

## Examples of how to use the new abstractions, helpers, and extension points

### Run the backend locally

From `backend/`:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m app
```

This uses the new `backend/app/__main__.py` entrypoint and the environment-backed settings loader.

### Override the API prefix or port

```bash
STORYTELLER_API_V1_PREFIX=/api/internal/v1 STORYTELLER_PORT=9000 python -m app
```

The app will still mount the unversioned routes normally and will move the versioned router under the configured prefix.

### Add a new v1 route

The intended pattern is:

1. Add a route module under `backend/app/api/v1/routes/`.
2. Import that router into `backend/app/api/v1/router.py`.
3. Put payload-building or policy logic in `backend/app/services/`.
4. Add any new response models under `backend/app/models/`.

A future sessions route would follow the same shape as the health route instead of growing `main.py`.

### Extend health/dependency reporting

If a later prompt wires in Postgres, the natural extension point is `backend/app/db/status.py`. The health service already composes dependency data from there, so a real database check can replace the placeholder without changing the route signatures.

## Exact verification work performed

I verified the work locally, through automated tests, and through the Docker Compose stack.

### Python environment bootstrap

I ran:

```bash
python3 -m venv backend/.venv
source backend/.venv/bin/activate
pip install -r backend/requirements.txt
```

Result:

- Passed.
- Installed `fastapi`, `uvicorn`, `pytest`, and `httpx` into a repo-local venv for backend verification.

### Automated backend tests

I ran:

```bash
backend/.venv/bin/python -m pytest backend/tests
```

Result:

- Passed.
- 3 tests collected, 3 passed.

Measured outcomes:

- `test_health_endpoint_returns_service_metadata` — passed
- `test_versioned_health_endpoint_marks_the_api_version` — passed
- `test_legacy_hello_endpoint_remains_available_for_existing_frontend_checks` — passed

### Backend compile sanity check

I ran:

```bash
backend/.venv/bin/python -m compileall backend/app
```

Result:

- Passed.
- The new package layout compiled cleanly under the local Python 3.9 environment.

### Local live runtime verification

I ran the backend directly from the `backend/` directory:

```bash
.venv/bin/python -m app
```

Then I verified the live endpoints:

```bash
curl -fsS http://127.0.0.1:8565/health
curl -fsS http://127.0.0.1:8565/api/v1/health
curl -fsS http://127.0.0.1:8565/api/hello
```

Results:

- All three endpoints returned `200 OK`.
- `/health` returned `status=ok`, `service=Storyteller API`, `environment=development`, `version=0.1.0`, and `database.status=not-configured`.
- `/api/v1/health` returned the same payload plus `api_version=v1`.
- `/api/hello` returned the unchanged compatibility message `Hello from FastAPI!`.

### Docker Compose validation

I ran:

```bash
./scripts/dev-compose.sh up -d --build
./scripts/dev-compose.sh ps
curl -fsS http://127.0.0.1:8565/health
curl -fsS http://127.0.0.1:8566 | sed -n '1,40p'
```

Results:

- Passed.
- `backend`, `frontend`, and `browser` all built and started successfully.
- Compose reported:
  - `compose-backend-1` healthy
  - `compose-frontend-1` healthy
  - `compose-browser-1` running
- The backend health check succeeded against the new `/health` route.
- The frontend still served the expected Vite HTML shell on `http://127.0.0.1:8566`.

### Browser-based integration smoke check

Even though this prompt was backend-focused, I ran the existing browser smoke spec to confirm the preserved `/api/hello` path still supports the prompt-02 frontend.

Command:

```bash
./scripts/dev-compose.sh run --rm browser npm run check -- --spec ./examples/homepage.spec.json
```

Result:

- Passed.
- The browser runner completed the existing homepage spec successfully.
- Screenshot written to:
  - `.artifacts/webapp-qa/homepage.png`

This was not a visual-change prompt, so I did not do a manual visual review beyond confirming the smoke run completed and saved its artifact.

### Patch hygiene

I ran:

```bash
git diff --check
```

Result:

- Passed with no whitespace or patch-formatting issues.

### Cleanup

I ran:

```bash
./scripts/dev-compose.sh down
find backend -type d -name '__pycache__' -prune -exec rm -rf {} +
```

Result:

- Passed.
- The Compose stack was shut down cleanly.
- Generated Python bytecode directories were removed after verification.

## Tests, builds, browser checks, screenshots, and remaining limits

- Automated tests added:
  - `backend/tests/test_health.py`
- Automated tests run:
  - backend pytest suite: passed
- Build/compile checks run:
  - `backend/.venv/bin/python -m compileall backend/app`: passed
- Runtime checks run:
  - local backend process via `python -m app`: passed
  - live curl checks for `/health`, `/api/v1/health`, `/api/hello`: passed
  - Docker Compose stack startup: passed
- Browser checks run:
  - existing homepage smoke spec: passed
- Screenshot artifacts:
  - `.artifacts/webapp-qa/homepage.png`

Current limitations after this prompt:

- The backend does not connect to PostgreSQL yet; it only reports database configuration state.
- Settings are env-backed only; `secrets.yaml` integration is still future work.
- The `models/`, `services/`, and `db/` packages are intentionally minimal scaffolds, not full business/domain layers yet.
- There is not yet a backend formatter, type checker, or richer API contract test suite beyond the health endpoints.

## LLM and prompt evaluation suite

No LLM-facing code, prompts, model wiring, or agent behavior changed in this prompt.

Evaluation suite status:

- `LLM happy paths` — not applicable
- `LLM edge cases` — not applicable
- `LLM regression checks` — not applicable
- `LLM safety checks` — not applicable
- `LLM formatting checks` — not applicable
- `LLM failure-mode checks` — not applicable

## Wrong turns, dead ends, surprising behavior, and gotchas

### Initial pytest import failure from the repo root

My first backend test run failed because `backend/tests/conftest.py` tried to import `app` while pytest was executing from the repository root, where `backend/` was not on `sys.path`.

I fixed that by explicitly inserting the backend directory into `sys.path` inside `backend/tests/conftest.py`, so `backend/.venv/bin/python -m pytest backend/tests` now works reliably from the repo root.

### First browser smoke command used the wrong working directory

I initially launched:

```bash
./scripts/dev-compose.sh run --rm browser npm run check -- --spec ./examples/homepage.spec.json
```

from `tools/webapp-qa/`, which failed because `./scripts/dev-compose.sh` is a repo-root path, not a tools-directory path.

I reran the exact same command from the repository root and it passed.

### Frontend health startup takes noticeably longer than backend health

During Compose verification, the backend became healthy before the frontend. That was not a backend failure; it was the existing Vite container plus its health/start period behavior. The final result was healthy, but the wait is worth noting so a reviewer does not interpret the intermediate `Waiting` state as a regression.

## Assumptions I made while working unsupervised

- I assumed prompt 03 should not break the already-shipped prompt-02 frontend, so I preserved `/api/hello` instead of forcing the frontend to move to `/health` immediately.
- I assumed a plain env-backed settings loader was the right depth for this prompt because prompt 05 is dedicated to settings and secrets loading.
- I assumed the service health endpoint should remain green even without a real database, and should report `database.status = not-configured` rather than failing health checks before Postgres exists.
- I assumed adding a focused backend pytest suite was preferable to relying only on Compose health checks, since the execution context explicitly asked for targeted tests for touched areas.
- I assumed it was appropriate to verify frontend/backend compatibility with the existing browser smoke test even though this prompt did not directly change UI code, because the preserved legacy route is part of the compatibility contract.
