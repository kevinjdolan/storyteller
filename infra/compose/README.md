# Compose

`docker-compose.yml` in this directory is the canonical local stack definition for Storyteller.

Use the repository wrapper script from the repo root:

```bash
./scripts/dev-compose.sh up --build
```

That wrapper keeps the Compose file under `infra/` while preserving a simple developer entrypoint.

Current local services:

- `frontend` on `http://localhost:8566`
- `backend` on `http://localhost:8565`
- `postgres` on `localhost:8567`
- `gcs` on `http://localhost:8568`
- `browser` as the containerized QA runner
