# Scripts

This directory holds small developer entrypoints and helper scripts.

Current scripts:

- `dev-compose.sh`: wraps the canonical Compose file under `infra/compose/`

Keep scripts narrow in scope and readable enough that engineers can trust them at a glance.

Common usage:

- `./scripts/dev-compose.sh up --build` to start or rebuild the local stack
- `./scripts/dev-compose.sh down` to stop while preserving Postgres and GCS volumes
- `./scripts/dev-compose.sh down --volumes` to intentionally reset persistent local infrastructure data
