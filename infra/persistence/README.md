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

Current Compose-backed persistent volumes:

- `storyteller_postgres_data`: mounted into `/var/lib/postgresql/data`
- `storyteller_gcs_data`: mounted into `/data` for the local fake GCS server

Safe cleanup guidance:

- `./scripts/dev-compose.sh down` stops containers and preserves both volumes
- `./scripts/dev-compose.sh down --volumes` removes the containers and both named volumes
- avoid deleting volumes unless you want to wipe the local database and object storage state
