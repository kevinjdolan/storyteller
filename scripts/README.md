# Scripts

This directory holds small developer entrypoints and helper scripts.

Current scripts:

- `bootstrap-dev.sh`: creates `secrets.yaml` if needed, installs repo hooks, prepares `backend/.venv`, and syncs frontend dependencies
- `check-secret-hygiene.sh`: blocks staged local-only config files and obvious secret material
- `dev-compose.sh`: wraps the canonical Compose file under `infra/compose/`
- `install-git-hooks.sh`: points `core.hooksPath` at the repo-managed `.githooks/` directory
- `reset-local-data.sh`: stops the compose stack and removes only the Postgres and fake GCS persistent volumes

Keep scripts narrow in scope and readable enough that engineers can trust them at a glance.

Common usage:

- `make bootstrap` for first-run local setup
- `make up` to start or rebuild the local stack in detached mode
- `make logs` to follow the running stack logs
- `make down` to stop while preserving Postgres and GCS volumes
- `make reset` to intentionally wipe only the database and object-storage data
- `./scripts/dev-compose.sh down --volumes` for a deeper reset that also clears dependency cache volumes
