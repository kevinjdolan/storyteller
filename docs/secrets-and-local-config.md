# Secrets and Local Config

Storyteller loads backend configuration from two sources:

1. `secrets.yaml` for local-only values
2. `STORYTELLER_*` environment variables

Precedence is simple:

1. built-in defaults
2. `secrets.yaml`
3. environment variables

Environment variables always win over `secrets.yaml`.

## Commit Hygiene

`secrets.yaml` is the live local credentials file. It must never be committed, copied into tracked examples, or pasted into checked-in docs. The repository keeps exactly one tracked template for that shape: `secrets.example.yaml`.

When contributors need a safe sample file, it should use an example-style name such as:

- `secrets.example.yaml`
- `.env.example`
- `.env.local.example`

Tracked examples must contain placeholders only. Real credentials belong in local-only files such as `secrets.yaml` or in shell environment variables that stay outside git.

The repository also ignores `.env`, `.env.*`, and reserved local persistence paths under `infra/persistence/` so machine-specific config and runtime data do not pollute `git status`.

## File Discovery

The backend looks for `secrets.yaml` in this order:

1. the path from `STORYTELLER_SECRETS_FILE`, if that variable is set to a non-empty value
2. the current working directory
3. `backend/`
4. the repository root

If `STORYTELLER_SECRETS_FILE` is set to an empty string, file discovery is disabled and only environment variables are used.

The Docker Compose backend service mounts the repository at `/workspace` and sets:

```text
STORYTELLER_SECRETS_FILE=/workspace/secrets.yaml
```

That means a local developer can copy the example file, add a Gemini key, and start the full stack without exposing the key to the browser.

## Create a Local File

Start from the example at the repository root:

```bash
cp secrets.example.yaml secrets.yaml
```

Then replace `gemini.api_key` with a real local key before starting the backend.

To enable the repo-managed pre-commit guard for this clone, run:

```bash
./scripts/install-git-hooks.sh
```

The hook blocks commits that stage `secrets.yaml`, `.env` files, or obvious Gemini/private-key material.

## Supported Shape

`secrets.yaml` uses the same nested structure as the backend settings object:

```yaml
database:
  url: postgresql+psycopg://storyteller:storyteller@postgres:5432/storyteller

gemini:
  api_key: your-gemini-api-key-here
  approximate_pricing:
    planning:
      input_cost_per_million_tokens_usd: 0.30
      output_cost_per_million_tokens_usd: 0.80
      cached_input_cost_per_million_tokens_usd: 0.03
    composition:
      input_cost_per_million_tokens_usd: 1.25
      output_cost_per_million_tokens_usd: 5.00
      cached_input_cost_per_million_tokens_usd: 0.13
    audio: {}

gcs:
  endpoint: http://gcs:4443
  project_id: storyteller-local
  public_url: http://localhost:8568
  buckets:
    sessions: storyteller-sessions
    audio: storyteller-audio
    exports: storyteller-exports

cors:
  allowed_origins:
    - http://localhost:8566

feature_flags:
  enable_api_docs: true
  enable_audio_generation: false
  enable_debug_inspector: false
```

The required values today are:

- `database.url`
- `gemini.api_key`
- `gcs.endpoint`
- `gcs.project_id`
- `gcs.buckets.sessions`
- `gcs.buckets.audio`
- `gcs.buckets.exports`

`gcs.public_url` is optional.

`gemini.approximate_pricing` is optional but recommended for usable cost diagnostics. The
checked-in defaults are intentionally lightweight approximations for local development, and you
can override them in `secrets.yaml` if your configured models use different pricing.

## Matching Environment Variables

The main environment-variable equivalents are:

- `STORYTELLER_DATABASE_URL`
- `STORYTELLER_GEMINI_API_KEY`
- `STORYTELLER_GEMINI_PLANNING_MODEL`
- `STORYTELLER_GEMINI_COMPOSITION_MODEL`
- `STORYTELLER_GEMINI_TTS_MODEL`
- `STORYTELLER_GCS_ENDPOINT`
- `STORYTELLER_GCS_PROJECT_ID`
- `STORYTELLER_GCS_PUBLIC_URL`
- `STORYTELLER_GCS_SESSIONS_BUCKET_NAME`
- `STORYTELLER_GCS_AUDIO_BUCKET_NAME`
- `STORYTELLER_GCS_EXPORTS_BUCKET_NAME`
- `STORYTELLER_CORS_ALLOWED_ORIGINS`
- `STORYTELLER_FEATURE_ENABLE_API_DOCS`
- `STORYTELLER_FEATURE_ENABLE_AUDIO_GENERATION`
- `STORYTELLER_FEATURE_ENABLE_DEBUG_INSPECTOR`

For compatibility with the earlier scaffold, `STORYTELLER_GCS_BUCKET_NAME` still works as a fallback and fills all three bucket names when the more specific variables are absent.

## Validation Behavior

Startup fails fast when required values are missing or malformed. The backend reports a short error list instead of a long Python traceback when launched with:

```bash
python -m app
```

The frontend never receives the Gemini API key. The browser only talks to the FastAPI backend, and all Gemini access stays in backend-owned services and adapters.
