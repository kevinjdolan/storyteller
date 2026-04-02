# Prompt 60: Composition Job Orchestration

## What I Changed And Why

I turned story composition into a durable backend-owned job flow instead of an in-request mutation path.

The main goal for this prompt was to make composition survive browser refreshes, worker restarts, and user pause/resume actions while keeping PostgreSQL as the source of truth for job state and object storage as the place where partial and final text artifacts live.

The core change is a new `CompositionJobService` in `backend/app/services/composition_jobs.py`.
It now owns:

- composition job start, pause, resume, cancel, and failure transitions
- plan-revision capture before composition starts
- pre-seeding durable `CompositionSegment` rows for the selected outline range
- storing runtime metadata such as `start_segment_index`, `total_segments`, `current_segment_id`, and `latest_partial_output`
- persisting partial segment text to object storage as the worker advances
- compiling the finished story text and saving a `STORY_TEXT` asset when the last segment completes

I also changed the existing composition entrypoints so they queue durable work instead of writing inline:

- `StoryWorkflowToolService._compose_next_segment(...)` now calls `CompositionJobService.start_job(...)`
- `StoryWorkflowToolService._rewrite_segments(...)` now calls `CompositionJobService.start_job(...)`
- active composition cancellation in session services now cancels active segment rows as well as the job row

This keeps request handlers and chat/tool orchestration thin while moving durability concerns into a single service boundary.

## Architectural Changes Across The Codebase

### 1. Durable composition orchestration service

`backend/app/services/composition_jobs.py`

- Added `COMPOSITION_RUNTIME_JOB_TYPE = "story.run_composition_job"`.
- Added `CompositionJobService` with explicit lifecycle methods:
  - `start_job(...)`
  - `resolve_continue_start_segment(...)`
  - `pause_job(...)`
  - `resume_job(...)`
  - `cancel_job(...)`
  - `cancel_active_jobs(...)`
  - `run_job(...)`
  - `mark_job_failed(...)`
- Added `HeuristicCompositionSegmentWriter` as the current segment writer behind an injectable interface.
- Added `evaluate_composition_segment_draft(...)` so completed output carries explicit quality checks in asset metadata.

Durability model:

- `CompositionJob` is the long-lived orchestration record.
- `BackgroundJob` of type `story.run_composition_job` is the short-lived worker trigger.
- Each worker execution processes one current segment, persists progress incrementally, and either:
  - requeues the next segment, or
  - finalizes the full story asset if the last segment completed.

This means composition now runs outside the request lifecycle and resume does not depend on the browser staying open.

### 2. API surface for lifecycle control

`backend/app/api/v1/routes/sessions.py`
`backend/app/models/session.py`

Added typed request/response models:

- `StartSessionCompositionRequest`
- `RedirectSessionCompositionRequest`
- `SessionCompositionResponse`

Added new session endpoints:

- `POST /api/v1/sessions/{session_id}/composition/start`
- `POST /api/v1/sessions/{session_id}/composition/{composition_job_id}/pause`
- `POST /api/v1/sessions/{session_id}/composition/{composition_job_id}/resume`
- `POST /api/v1/sessions/{session_id}/composition/{composition_job_id}/cancel`
- `POST /api/v1/sessions/{session_id}/composition/{composition_job_id}/redirect`

These endpoints return the hydrated snapshot, the latest event, and the resolved composition job view so the UI can render state directly from backend truth.

### 3. Session hydration and frontend-facing job shape

`backend/app/services/session_hydration.py`
`backend/app/models/session.py`

Extended `CompositionJobView` to expose:

- `total_segments`
- `current_segment_id`
- `latest_partial_output`

Hydration now preserves those values both from live progress events and from persisted job rows. That gives the UI enough information to show:

- which segment is active
- how far the run has progressed
- the latest partial text that has already been durably written

### 4. Worker integration

`backend/app/worker/default_handlers.py`
`backend/app/worker/__main__.py`

Registered a new default worker handler for `story.run_composition_job`.

The handler:

- validates that a `composition_job_id` exists in the payload
- resolves the job through `CompositionJobService.run_job(...)`
- marks the composition job failed through `mark_job_failed(...)` if the worker raises

I also made the default registry injectable with `object_storage` and `composition_writer` so this runtime can be extended or swapped without patching handler internals.

### 5. Tests

`backend/tests/test_story_tools.py`
`backend/tests/test_session_api.py`

Added coverage for:

- queueing a durable runtime job when composition starts
- resume behavior that does not duplicate queued runtime attempts
- end-to-end worker completion with segment persistence and final story asset creation
- API start/pause/resume/cancel lifecycle behavior
- redirecting an active composition job into a rewrite pass

No schema migration was needed for this prompt because the existing composition tables already had the fields required for orchestration.

## Examples And Extension Points

### HTTP usage

Start a fresh composition pass:

```http
POST /api/v1/sessions/{session_id}/composition/start
Content-Type: application/json

{
  "mode": "fresh",
  "origin": "workspace"
}
```

Resume from the next unfinished segment:

```http
POST /api/v1/sessions/{session_id}/composition/start
Content-Type: application/json

{
  "mode": "continue",
  "origin": "workspace"
}
```

Redirect an active run into a rewrite from segment 2:

```http
POST /api/v1/sessions/{session_id}/composition/{composition_job_id}/redirect
Content-Type: application/json

{
  "instructions": "Soften the midpoint and make the helper visible earlier.",
  "rewrite_from_segment_index": 2,
  "origin": "workspace"
}
```

Pause, resume, or cancel use the dedicated control endpoints with the job id in the URL.

### Python service usage

If another backend surface needs to drive composition directly, it can use the service layer without going through the API:

```python
service = CompositionJobService(session, object_storage=my_storage, writer=my_writer)

start = service.start_job(
    session_id=session_id,
    job_kind=CompositionJobKind.DRAFT,
    start_segment_index=1,
    instructions="Keep the harbor imagery soft.",
    cancel_reason="Cancelled because a new composition pass started.",
)
```

Useful extension points:

- `CompositionJobService(..., object_storage=...)`
  - lets tests or alternate environments supply a custom storage service
- `CompositionJobService(..., writer=...)`
  - lets a future Gemini-backed writer replace the current heuristic writer without changing the orchestration flow
- `build_default_job_handler_registry(object_storage=..., composition_writer=...)`
  - lets worker bootstrapping swap runtime dependencies in one place

## Verification Performed

### Linting

Ran:

```bash
python -m ruff check \
  backend/app/api/v1/routes/sessions.py \
  backend/app/services/composition_jobs.py \
  backend/app/services/story_tools.py \
  backend/app/services/session_hydration.py \
  backend/app/services/__init__.py \
  backend/app/worker/default_handlers.py \
  backend/app/worker/__main__.py \
  backend/app/models/session.py \
  backend/app/models/__init__.py \
  backend/app/services/sessions.py \
  backend/tests/test_story_tools.py \
  backend/tests/test_session_api.py
```

Result: passed.

I also used `python -m ruff format ...` on the touched files while cleaning up long lines and import ordering.

### Automated tests

Targeted composition and hydration tests:

```bash
python -m pytest \
  backend/tests/test_story_tools.py \
  backend/tests/test_session_api.py \
  backend/tests/test_session_hydration_service.py \
  -q
```

Result: `60 passed in 7.60s`

Broader session and action-policy regression pass:

```bash
python -m pytest \
  backend/tests/test_action_policy_service.py \
  backend/tests/test_action_policy_api.py \
  backend/tests/test_session_service.py \
  -q
```

Result: `34 passed in 2.76s`

Full backend suite:

```bash
python -m pytest backend/tests -q
```

Result: `214 passed, 5 skipped in 13.30s`

### Browser checks, screenshots, and UI validation

None performed.

Reason:

- this prompt only changed backend services, worker integration, API routes, and backend tests
- no frontend files were changed
- no UI rendering, styling, layout, or browser behavior changed directly in this task

Limit:

- the new composition control endpoints are backend-ready, but the frontend still needs to call them explicitly if the product should expose these controls in the UI

### Build and type-check notes

I did not run a separate backend build or static type checker because this repository’s backend config currently exposes `ruff` and `pytest` in `backend/pyproject.toml`, and there is no established `mypy` or `pyright` target to run for this prompt.

## Evaluation Suite Added For Composition Output

I added a lightweight composition-output evaluation pass in `evaluate_composition_segment_draft(...)` and persisted its results into the final `STORY_TEXT` asset metadata.

Named criteria:

- `non_empty_output`
- `multiple_paragraphs`
- `protagonist_named`
- `support_visible`
- `restful_close`

Observed results from a completed end-to-end sample worker run:

- `non_empty_output`: pass, measured value `149`
- `multiple_paragraphs`: pass, measured value `3`
- `protagonist_named`: pass, measured value `"Mira"`
- `support_visible`: pass, measured value `"n/a"`
- `restful_close`: pass, measured value was the closing paragraph text, which contained the expected calm/settled language

I collected that sample by running the durable composition flow end to end against the fake object storage test harness and reading the final story asset metadata after worker completion.

This is not a full model-eval harness for Gemini output yet. It is an orchestration-focused evaluator that ensures the durable writer produces a minimally acceptable segment shape and records those checks with the artifact.

## Wrong Turns, Dead Ends, And Gotchas

- I initially left an exception object captured inside the worker failure lambda. In Python, the exception variable from `except Exception as exc` is cleared after the block, so I changed the code to materialize `error_message` before passing it into the callback.
- The fake GCS helper in `backend/tests/test_story_tools.py` needed more realistic request handling than my first pass. In particular, bucket-creation requests needed decoded JSON parsing, and object keys needed URL decoding so uploads/downloads matched the object storage client behavior.
- An ad hoc verification script failed at first because importing test helpers directly does not apply pytest’s environment bootstrap from `backend/tests/conftest.py`. I had to set the `STORYTELLER_*` test environment variables manually and clear the settings cache before using those helpers outside pytest.
- `.yolopilot` run artifacts update while the run is in progress. I intentionally left those out of the code checkpoint commit so the reviewable code change stayed focused on prompt 60.

## Assumptions Made While Working Unsupervised

- The existing composition schema was sufficient for orchestration, so I reused it instead of introducing a migration during this prompt.
- Prompt 60 was backend-first. I did not wire the new endpoints into the frontend client because the acceptance criteria focused on durable background execution and backend-owned progress state.
- Persisting final composed story text as a markdown-backed `STORY_TEXT` asset is acceptable for this stage, even though downstream export flows may eventually transform that content into other formats.
- The current heuristic segment writer is acceptable as the runtime writer for this prompt because the main requirement was durable orchestration. The new writer injection points are intended to make a future Gemini-backed composition runtime a bounded follow-up change.
- Chunk-level pause and cancel checks are sufficient for the first durable version. This implementation does not attempt token-level interruption inside a single chunk write.

## Checkpoint Commit

I made a code checkpoint commit before writing this summary:

- `b49ff26 feat(prompt-60): composition job orchestration`

That commit contains the code and test changes for prompt 60. This summary file was written afterward as the required final artifact for the run.
