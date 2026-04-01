# Scripts

This directory holds small developer entrypoints and helper scripts.

Current scripts:

- `check-secret-hygiene.sh`: blocks staged local-only config files and obvious secret material
- `dev-compose.sh`: wraps the canonical Compose file under `infra/compose/`
- `install-git-hooks.sh`: points `core.hooksPath` at the repo-managed `.githooks/` directory

Keep scripts narrow in scope and readable enough that engineers can trust them at a glance.

Common usage:

- `./scripts/dev-compose.sh up --build` to start or rebuild the local stack
- `./scripts/dev-compose.sh down` to stop while preserving Postgres and GCS volumes
- `./scripts/dev-compose.sh down --volumes` to intentionally reset persistent local infrastructure data
- `./scripts/install-git-hooks.sh` to enable the lightweight pre-commit secret guard for this clone
