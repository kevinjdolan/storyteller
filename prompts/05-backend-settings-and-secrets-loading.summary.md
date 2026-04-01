# Prompt 05 Summary: Backend Settings and `secrets.yaml` Loading

## What Changed and Why

I replaced the original loose `os.getenv()`-driven backend config reader with a typed, validated settings system under `backend/app/settings/config.py`. The previous version silently accepted missing values by returning empty strings for required runtime dependencies like the database URL and GCS coordinates. That was fine for the scaffold, but it did not satisfy this prompt's acceptance criteria around local `secrets.yaml` support, readable failure modes, or backend-owned Gemini credentials.

The new loader now:

- builds a typed `AppSettings` object backed by nested Pydantic models for `database`, `gemini`, `gcs`, `cors`, and `feature_flags`
- loads configuration from built-in defaults, then `secrets.yaml`, then `STORYTELLER_*` environment variables
- discovers `secrets.yaml` from `STORYTELLER_SECRETS_FILE`, the current working directory, `backend/`, or the repo root
- fails fast with a short, source-aware error list when required values are missing or malformed
- keeps the Gemini API key on the backend only and exposes it as a secret-backed value in the settings object

I also added a repo-root `secrets.example.yaml` and a dedicated configuration doc so a developer can copy the example, add a Gemini key, and start the stack without inventing their own file shape.

## Architectural Changes

### 1. Typed settings model

`backend/app/settings/config.py` now owns the full runtime configuration contract.

The main models are:

- `AppSettings`
- `DatabaseSettings`
- `GeminiSettings`
- `GCSSettings`
- `StorageBucketsSettings`
- `CorsSettings`
- `FeatureFlagsSettings`
- `SettingsValidationError`

This gives the backend a single place to evolve configuration instead of spreading `os.getenv()` calls across route handlers and services.

### 2. Explicit source-merging pipeline

I implemented a small source loader instead of bringing in `pydantic-settings`.

The merge order is:

1. built-in defaults
2. `secrets.yaml`
3. environment variables

That logic lives in `load_settings()`, which builds a merged payload and validates it once at the boundary. The caching contract remains in `get_settings()`.

### 3. Readable startup failure path

The backend startup entrypoints now turn configuration failures into short process-level messages instead of noisy tracebacks:

- `backend/app/__main__.py`
- `backend/app/main.py`

Both catch `SettingsValidationError` and exit with a concise message. This matters most for the documented local entrypoint, `python -m app`.

### 4. Compose integration for repo-root secrets

The backend container originally only mounted `backend/`, which meant the repo-root `secrets.yaml` was invisible inside Docker Compose. I fixed that by mounting the repo read-only at `/workspace` and setting:

```text
STORYTELLER_SECRETS_FILE=/workspace/secrets.yaml
```

That change is in `infra/compose/docker-compose.yml`. It makes the documented repo-root `secrets.yaml` actually usable in the canonical dev stack.

### 5. Health/status adaptation

Because required runtime config is now validated up front, a running app should always report configured database and object storage settings. I updated the existing status helpers accordingly:

- `backend/app/db/status.py`
- `backend/app/storage/status.py`

I also changed the storage status message to reflect multiple named buckets instead of the previous single-bucket scaffold.

## New Abstractions and How to Use Them

### Load settings directly

For test code or one-off tooling:

```python
from app.settings import load_settings

settings = load_settings(
    {
        "STORYTELLER_DATABASE_URL": "postgresql://storyteller:storyteller@postgres:5432/storyteller",
        "STORYTELLER_GEMINI_API_KEY": "local-key",
        "STORYTELLER_GCS_ENDPOINT": "http://gcs:4443",
        "STORYTELLER_GCS_PROJECT_ID": "storyteller-local",
        "STORYTELLER_GCS_SESSIONS_BUCKET_NAME": "storyteller-sessions",
        "STORYTELLER_GCS_AUDIO_BUCKET_NAME": "storyteller-audio",
        "STORYTELLER_GCS_EXPORTS_BUCKET_NAME": "storyteller-exports",
        "STORYTELLER_SECRETS_FILE": "",
    },
)
```

Use `load_settings()` when you want an uncached settings object from explicit inputs. Use `get_settings()` for normal application runtime.

### Access nested settings

Examples from the new settings shape:

```python
settings.database.url
settings.gemini.api_key
settings.gcs.buckets.sessions
settings.feature_flags.enable_api_docs
```

I kept compatibility properties like `settings.database_url`, `settings.gcs_endpoint`, and `settings.cors_allowed_origins` so existing application code did not need a broad rewrite in this prompt.

### Disable secrets-file lookup

Tests can opt out of local file discovery by setting:

```text
STORYTELLER_SECRETS_FILE=""
```

That keeps pytest isolated from any real `secrets.yaml` a developer may have on disk.

### Feature flags

The initial typed feature flags are:

- `enable_api_docs`
- `enable_audio_generation`
- `enable_debug_inspector`

`enable_api_docs` is already wired into `FastAPI(...)` so `/docs`, `/redoc`, and `/openapi.json` can be disabled through config. The other two are placeholders for later prompts and give future work a typed home immediately.

## Documentation and Local Developer Flow

I added:

- `secrets.example.yaml`
- `docs/secrets-and-local-config.md`

I also updated:

- `README.md`
- `backend/README.md`
- `infra/compose/README.md`

The intended local flow is now:

```bash
cp secrets.example.yaml secrets.yaml
./scripts/dev-compose.sh up --build
```

The example file includes:

- database URL
- Gemini API key placeholder
- GCS endpoint/project/public URL
- three named bucket settings
- CORS origins
- feature flags

## Verification Performed

### Automated tests

I expanded the backend test suite in `backend/tests/test_settings.py` and updated the existing health tests.

Commands run:

```bash
python -m pip install -r backend/requirements.txt
pytest backend/tests -q
```

Outcome:

- `11 passed in 0.13s`

Coverage added or updated:

- environment-only config loading
- secrets-file loading
- env-over-secrets precedence
- legacy single-bucket fallback behavior
- runtime effect of `enable_api_docs=false`
- readable missing-config failures
- readable invalid-YAML failures
- `python -m app` startup failure without traceback
- health endpoint expectations for configured dependencies

### Direct runtime checks

I also ran targeted command-line checks outside pytest:

```bash
STORYTELLER_SECRETS_FILE='' STORYTELLER_DATABASE_URL='postgresql://storyteller:storyteller@postgres:5432/storyteller' STORYTELLER_GEMINI_API_KEY='verify-gemini-key' STORYTELLER_GCS_ENDPOINT='http://gcs:4443' STORYTELLER_GCS_PROJECT_ID='storyteller-local' STORYTELLER_GCS_SESSIONS_BUCKET_NAME='storyteller-sessions' STORYTELLER_GCS_AUDIO_BUCKET_NAME='storyteller-audio' STORYTELLER_GCS_EXPORTS_BUCKET_NAME='storyteller-exports' python - <<'PY'
from app.main import create_app
app = create_app()
print(app.title)
print(app.docs_url)
PY
```

Observed output:

- `Storyteller API`
- `/docs`

I also checked the failure path directly:

```bash
STORYTELLER_SECRETS_FILE='' python -m app
```

Observed behavior:

- short configuration error list
- no traceback
- missing fields called out by env-var name and YAML key path

### Compose verification

I validated the updated Compose file shape with:

```bash
./scripts/dev-compose.sh config
```

Outcome:

- command succeeded
- the backend service resolves with the new `/workspace` mount and the `STORYTELLER_SECRETS_FILE` override

### Browser checks and screenshots

None were run for this task.

Reason:

- the prompt only changed backend configuration, startup behavior, and Compose wiring
- there was no frontend rendering, layout, accessibility, or UI interaction change to verify visually

That is the main verification limit for this task: I verified the backend behavior thoroughly, but there was no UI change to inspect in a browser.

## LLM / Prompt Evaluation Suite

No LLM or prompt-facing logic changed in this task.

Added evaluation suite:

- none

Named criteria and outcomes:

- not applicable

## Wrong Turns, Dead Ends, and Gotchas

### Generic Pydantic missing-field errors

My first validation pass produced messages like `database.url: Field required`. That was technically correct but weaker than the acceptance bar. I changed the validation error translation so missing values now point to both the matching env var and the YAML key path.

### Compose could not actually see repo-root secrets

The prompt and existing docs assumed a repo-root `secrets.yaml`, but the backend container only mounted `backend/`. Without changing Compose, `secrets.yaml` support would have worked locally outside Docker and failed in the canonical dev stack. I fixed that by adding the read-only repo mount and explicit secrets-file path.

### Existing tests imported `app.main` too early

`backend/tests/conftest.py` imports `create_app` at module import time, which means settings validation happens before fixtures run. Once configuration became required, that import path would have broken on a developer machine with no env seeded. I fixed that by setting safe backend test defaults before importing `app.main`.

### Single bucket vs multiple bucket names

The prompt asked for bucket names plural, but the existing scaffold only had `STORYTELLER_GCS_BUCKET_NAME`. I moved the settings model to three named buckets and kept the old single variable as a fallback so the change is forward-looking without being brittle.

## Assumptions Made While Running Unsupervised

- I treated `python -m app` as the canonical startup path that needed the cleanest error message because it is already the documented backend entrypoint.
- I assumed three bucket names were enough for this prompt: `sessions`, `audio`, and `exports`. Future prompts can add prefixes or extra buckets without changing the basic structure.
- I assumed the Gemini API key should be required at backend startup, even though no Gemini calls exist yet, because the prompt explicitly called it out as required configuration.
- I assumed it was acceptable to keep compatibility properties on `AppSettings` to avoid a large unrelated refactor in early prompts.
- I assumed `STORYTELLER_SECRETS_FILE=""` as an explicit opt-out was worthwhile for tests and local tooling even though it is not part of the main user-facing flow.
- I assumed no browser-based verification was necessary because this prompt did not alter any user-facing UI behavior.

## Files Touched

Primary implementation files:

- `backend/app/settings/config.py`
- `backend/app/settings/__init__.py`
- `backend/app/main.py`
- `backend/app/__main__.py`
- `backend/app/db/status.py`
- `backend/app/storage/status.py`

Docs and examples:

- `secrets.example.yaml`
- `docs/secrets-and-local-config.md`
- `README.md`
- `backend/README.md`
- `infra/compose/README.md`

Runtime wiring:

- `infra/compose/docker-compose.yml`
- `backend/requirements.txt`

Tests:

- `backend/tests/conftest.py`
- `backend/tests/test_settings.py`
- `backend/tests/test_health.py`
