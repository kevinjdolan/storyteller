# Persistence Notes

Use this directory for notes about local durable data as infrastructure services are added.

Examples that belong here:

- where Docker volumes store PostgreSQL state in development
- how the file-backed GCS emulator persists blobs across restarts
- backup, reset, and cleanup guidance for local persistent data

This directory is for documentation and conventions, not checked-in database dumps or generated runtime data.

If future local infrastructure work needs host-mounted runtime state instead of named Docker volumes, keep that data under one of these reserved ignored paths:

- `infra/persistence/runtime/`
- `infra/persistence/postgres-data/`
- `infra/persistence/gcs-data/`
- `infra/persistence/local/`

Those directories are gitignored so local persistence experiments and recovered data do not pollute commits.

Current Compose-backed persistent volumes from the base stack:

- `storyteller_postgres_data`: mounted into `/var/lib/postgresql/data`
- `storyteller_gcs_data`: mounted into `/data` for the local fake GCS server

Local development also creates dependency cache volumes through the dev override:

- `storyteller_frontend_node_modules`: mounted into `/app/node_modules` inside the frontend container
- `storyteller_webapp_qa_node_modules`: mounted into `/workspace/tools/webapp-qa/node_modules`

Treat those cache volumes as disposable. They speed up rebuilds, but they do not contain durable application state.

Safe cleanup guidance:

- `make down` stops containers and preserves both volumes
- `make reset` stops the stack and removes only `storyteller_postgres_data` and `storyteller_gcs_data`
- `./scripts/dev-compose.sh down --volumes` removes all compose-declared volumes, including dependency caches
- avoid deleting volumes unless you want to wipe the local database and object storage state
