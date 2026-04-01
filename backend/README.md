# Backend

This directory is the home for the FastAPI application, backend-owned workflow logic, and future durable job processing.

Current contents:

- `app/`: live application code
- `migrations/`: reserved for database migrations
- `requirements.txt`: Python dependencies
- `Dockerfile`: backend container image

Planned expansion inside `app/` follows the architecture notes in [docs/architecture-overview.md](/Users/kevin/code/storyteller/docs/architecture-overview.md), including explicit homes for API routes, settings, repositories, services, AI adapters, storage, and worker execution.
