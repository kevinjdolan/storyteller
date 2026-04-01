# Backend Worker

This package contains the first durable worker scaffold for long-running Storyteller jobs.

Current pieces:

- `python -m app.worker`: polling worker entrypoint
- `runtime.py`: single-process worker loop that claims, heartbeats, completes, and fails jobs
- `registry.py`: handler registry for mapping `job_type` strings to Python callables
- `default_handlers.py`: starter handlers, including `demo.echo` for smoke tests

The worker claims rows from the PostgreSQL-backed `background_jobs` table using leases instead of
tying work to API request threads. Future prompts should register composition and narration handlers
here rather than embedding that logic in FastAPI routes.
