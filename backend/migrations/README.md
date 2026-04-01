# Backend Migrations

This directory contains the Alembic environment and schema history for Storyteller's PostgreSQL
database.

## Current scope

The initial revision creates the first durable relational core for:

- genre and tone catalog rows
- story sessions and per-stage state snapshots
- story briefs, pitches, character sheets, beat sheets, and story setup revisions
- composition jobs and composition segments
- audio jobs
- export assets
- append-only event log entries

## Local commands

Upgrade a fresh local database to the latest revision:

```bash
cd backend
STORYTELLER_SECRETS_FILE="" \
STORYTELLER_DATABASE_URL="postgresql+psycopg://storyteller:storyteller@127.0.0.1:8567/storyteller" \
alembic upgrade head
```

Roll back to an empty schema:

```bash
cd backend
STORYTELLER_SECRETS_FILE="" \
STORYTELLER_DATABASE_URL="postgresql+psycopg://storyteller:storyteller@127.0.0.1:8567/storyteller" \
alembic downgrade base
```

Generate a follow-on revision after updating the ORM models:

```bash
cd backend
STORYTELLER_SECRETS_FILE="" \
STORYTELLER_DATABASE_URL="postgresql+psycopg://storyteller:storyteller@127.0.0.1:8567/storyteller" \
alembic revision --autogenerate -m "describe change"
```

Keep this directory focused on schema history and migration tooling rather than application runtime
code.
