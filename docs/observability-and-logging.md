# Observability And Logging

Storyteller now emits structured JSON logs from the FastAPI app, the worker, and Gemini-backed
model adapters. The goal is to trace one failing session across request handling, durable queue
handoff, worker execution, model retries, and final artifact publication without dumping raw story
content into logs.

## What Is Correlated

Common fields now flow automatically when they are known:

- `request_id`: assigned by the API middleware or echoed from the inbound `X-Request-ID` header
- `session_id`: bound for session-scoped API routes and worker-backed jobs
- `background_job_id` and `background_job_type`: emitted when runtime jobs are enqueued and claimed
- `composition_job_id` or `audio_job_id`: emitted from the orchestration services during segment
  generation and publication
- `worker_id`: emitted by the durable worker loop

Model adapter logs also add:

- `operation`
- `model_id`
- `prompt_version`
- `attempts_used`
- retry metadata such as `failure_kind`, `failed_attempt`, `next_attempt`, and `delay_seconds`

## Event Families

High-signal events to look for:

- `http.request.started`
- `http.request.completed`
- `http.request.failed`
- `worker.job.enqueued`
- `worker.job.claimed`
- `worker.job.completed`
- `worker.job.failed`
- `composition.job.queued`
- `composition.segment.started`
- `composition.segment.completed`
- `composition.job.completed`
- `composition.job.failed`
- `audio.job.queued`
- `audio.segment.completed`
- `audio.job.completed`
- `audio.job.failed`
- `ai.request.started`
- `ai.request.retry_scheduled`
- `ai.request.succeeded`
- `ai.request.failed`
- `model.usage.recorded`

## Local Development

Follow the live Compose logs:

```bash
make logs
```

Filter a single session if you have `jq` installed:

```bash
make logs | jq -c 'select(.session_id == "session-123")'
```

If `jq` is not available, `rg` still works well:

```bash
make logs | rg '"session_id":"session-123"'
```

Correlate a composition or audio request into worker execution:

1. Find the API request by `request_id` or `session_id`.
2. Note the `composition_job_id` or `audio_job_id`.
3. Find the matching `worker.job.enqueued` event to capture the `background_job_id`.
4. Follow `worker.job.claimed` and the downstream `composition.*`, `audio.*`, and `ai.*` events.

Example sequence:

```text
http.request.completed
worker.job.enqueued
worker.job.claimed
composition.segment.started
ai.request.started
ai.request.retry_scheduled
ai.request.succeeded
composition.segment.completed
composition.job.completed
```

## CI And Test Failures

When a backend test fails locally or in CI, rerun the narrow scope with stdout logging left on:

```bash
cd backend
python -m pytest -s tests/test_health.py tests/test_worker_runtime.py
```

For integration failures, keep the stack running and inspect both backend and worker streams:

```bash
./scripts/dev-compose.sh logs -f backend worker
```

Because the logs are JSON, artifact and queue failures are easier to search by exact field values
than by free-text messages.

## Privacy Guardrails

The logs are intentionally metadata-heavy and content-light.

- Request logs do not include request bodies.
- Gemini adapter logs do not include rendered prompts or story text.
- Composition and audio lifecycle logs record identifiers, counts, timing, and failure classes,
  not full generated content.
- Detailed user-facing content remains in durable session state, artifacts, and the event log where
  it already belongs.
