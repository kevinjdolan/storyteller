# Compose

`docker-compose.yml` in this directory is the canonical local stack definition for Storyteller.

Use the repository wrapper script from the repo root:

```bash
make bootstrap
make up
```

The `Makefile` keeps the day-to-day command surface small, while `./scripts/dev-compose.sh` remains the lower-level wrapper that always targets the canonical compose file under `infra/`.

Current local services:

- `frontend` on `http://localhost:8566`
- `backend` on `http://localhost:8565`
- `worker` as the durable background-job runner
- `postgres` on `localhost:8567`
- `gcs` on `http://localhost:8568`
- `browser` as the containerized QA runner

The backend container reads the repo-root `secrets.yaml` through `STORYTELLER_SECRETS_FILE=/workspace/secrets.yaml`, so the local Gemini API key stays server-side even during Compose development.
The worker container defaults to env-only configuration in Compose so it can start independently from the API even when a local `secrets.yaml` contains unrelated provider fields. Override `STORYTELLER_GEMINI_API_KEY` in your shell before `./scripts/dev-compose.sh up -d worker` when a real handler needs Gemini access.

Useful follow-up commands:

- `make logs` to follow service logs
- `make down` to stop containers without removing durable app data
- `make reset` to stop the stack and remove only the Postgres and fake GCS data volumes
