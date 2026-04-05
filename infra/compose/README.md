# Compose

This directory now holds two Compose shapes:

- `docker-compose.yml`: the base runtime-oriented stack shape
- `docker-compose.dev.yml`: local-development overrides for bind mounts, live reload, and browser QA

## Local development

Use the repository wrapper script from the repo root:

```bash
make bootstrap
make up
```

`./scripts/dev-compose.sh` is the lower-level wrapper behind those `make` targets. It always applies the base file plus the development override together, so local engineers keep the same simple workflow while the checked-in base file stays closer to a deployable runtime definition.

Current local services:

- `frontend` on `http://localhost:8566`
- `backend` on `http://localhost:8565`
- `worker` as the durable background-job runner
- `postgres` on `localhost:8567`
- `gcs` on `http://localhost:8568`
- `browser` as the containerized QA runner

Local-only development behavior comes from `docker-compose.dev.yml`:

- backend and worker source are bind-mounted from `../../backend`
- the backend reads the repo-root `secrets.yaml` through `/workspace/secrets.yaml`
- the frontend runs the Vite dev server with file watching enabled inside the container
- the browser service exists only in the development overlay

The worker container still defaults to env-only Gemini configuration in Compose so it can start independently from the API even when a local `secrets.yaml` contains unrelated provider fields. Override `STORYTELLER_GEMINI_API_KEY` in your shell before `./scripts/dev-compose.sh up -d worker` when a real handler needs Gemini access.

Useful follow-up commands:

- `make logs` to follow service logs
- `make down` to stop containers without removing durable app data
- `make reset` to stop the stack and remove only the Postgres and fake GCS data volumes
- `./scripts/dev-compose.sh config` to inspect the fully merged local stack

## Runtime shape

The base `docker-compose.yml` is intentionally closer to a production handoff:

- app services build from explicit Dockerfile targets instead of depending on bind mounts
- the frontend is a static nginx image that proxies `/api` to the backend service
- the backend and worker run without source mounts or Vite-only settings
- only Postgres and fake GCS declare persistent named volumes

Before starting the base runtime stack, provide either:

- `STORYTELLER_GEMINI_API_KEY` in the shell environment, or
- a mounted secrets file plus `STORYTELLER_SECRETS_FILE`

That base file is still a local reference, not a finished deployment system. It gives future deployment work a cleaner starting point for image builds, runtime environment injection, and platform-specific manifests without forcing local developers to give up hot reload.

Inspect the runtime-only shape with:

```bash
docker compose -f infra/compose/docker-compose.yml config
```

The structured logging field guide is in
[docs/observability-and-logging.md](/Users/kevin/code/storyteller/docs/observability-and-logging.md),
including examples for tracing a `session_id` across API and worker logs.
