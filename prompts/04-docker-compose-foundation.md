# 04 — Docker Compose Foundation

Read `base_prompt.md` first and preserve all prior prompt work.

## Objective

Create a first working `docker-compose.yml` that can orchestrate the web app, API, PostgreSQL, and a file-backed GCS emulator for local development.

## Build
- Add services for `frontend`, `backend`, `postgres`, and `gcs` with sensible container names and ports.
- Use named volumes for PostgreSQL data and for the GCS emulator’s mounted storage directory so data persists across restarts.
- Make sure the GCS emulator can run in an easy local mode and is addressable from the backend through environment variables.

## Deliverables

- `docker-compose.yml`
- Per-service Dockerfiles or a clear placeholder plan if a service Dockerfile comes in the next prompt
- A README section describing how to bring the stack up and tear it down safely

## Acceptance checks

- The compose file includes persistence for both database data and object storage data.
- Container networking and ports are explicit and developer friendly.
- A fresh clone can be brought up without hand-editing the compose file.

## Notes

Favor clear named volumes and explicit env wiring. Keep secrets out of the compose file.

## Suggested commit label

`feat(prompt-04): docker compose foundation`
