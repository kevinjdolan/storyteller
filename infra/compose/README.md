# Compose

`docker-compose.yml` in this directory is the canonical local stack definition for Storyteller.

Use the repository wrapper script from the repo root:

```bash
cp secrets.example.yaml secrets.yaml
./scripts/dev-compose.sh up --build
```

That wrapper keeps the Compose file under `infra/` while preserving a simple developer entrypoint.

Current local services:

- `frontend` on `http://localhost:8566`
- `backend` on `http://localhost:8565`
- `postgres` on `localhost:8567`
- `gcs` on `http://localhost:8568`
- `browser` as the containerized QA runner

The backend container reads the repo-root `secrets.yaml` through `STORYTELLER_SECRETS_FILE=/workspace/secrets.yaml`, so the local Gemini API key stays server-side even during Compose development.
