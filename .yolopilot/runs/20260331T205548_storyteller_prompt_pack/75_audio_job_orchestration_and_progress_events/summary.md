# Prompt 75: Audio Job Orchestration and Progress Events

## What I Changed And Why

This task turns narration generation into a durable worker-driven job with explicit step tracking, persistent partial outputs, and realtime progress data that survives browser refreshes.

I implemented the main feature in commit `102d52b feat(prompt-75): audio job orchestration` and then normalized the touched frontend files in `0b40d11 chore(prompt-75): format frontend audio progress files`.

The core change is that audio jobs now behave much more like composition jobs:

- The backend tracks audio job progress as durable state instead of only ephemeral status.
- Each narration segment records retry attempts and segment-by-segment progress.
- Audio progress emits richer event payloads so the frontend can show the current phase, not just a coarse percent.
- The hydration path rebuilds the same audio progress state from durable job records after refresh or reconnect.
- The audio UI shows a progress badge, progress bar, current step text, and step/segment hints while narration is running.

This closes the main acceptance gap from prompt 75:

- audio generation can continue in the worker while the browser refreshes
- the frontend can show which narration stage is active now
- partial outputs are durable for debugging and resume behavior

## Architectural Changes Across The Codebase

### Backend event and snapshot contract

I extended the audio progress contract so the backend can describe durable narration progress with enough detail for both hydration and realtime rendering.

Changed files:

- `backend/app/models/events.py`
- `backend/app/models/session.py`
- `backend/app/services/event_log.py`
- `backend/app/services/session_hydration.py`
- `backend/app/services/session_realtime.py`
- `docs/realtime-events.md`
- `docs/realtime-events.schema.json`

New audio progress fields now include:

- `current_step`
- `current_step_index`
- `total_steps`
- `completed_segments`
- `latest_asset_id`
- `latest_asset_kind`
- `message`
- `progress_percent`

The important architectural point is that these fields are now available in both places that matter:

- durable snapshot hydration
- live `job.progress` events

That means the browser does not need to infer narration state from ad hoc status text anymore.

### Audio worker orchestration

The main orchestration work lives in `backend/app/services/audio_jobs.py`.

I changed the audio job service so it now:

- seeds durable progress metadata into `AudioJob.config_json` when a job starts
- tracks weighted step progress across render, assembly, mix, publish, and completion
- increments `AudioJob.attempt_count` on job reruns
- increments per-segment render attempts in `NarrationSegment.metadata_json`
- records progress after each durable segment save
- records latest segment/final asset IDs so hydration can point back to the most recent artifact
- emits failure progress with a useful `current_step` and `message`

The step model is intentionally explicit:

- queued
- rendering narration segments
- assembling narration master
- mixing background music when enabled
- publishing final audio asset
- completed

I used weighted progress checkpoints instead of evenly splitting all steps:

- segment rendering budget up to 86%
- assembly at 90%
- mix at 96%
- publish at 99%
- completion at 100%

That keeps the progress bar responsive during the long segment-render portion without pretending that final assembly and publishing are free.

### Frontend runtime and UI wiring

Changed files:

- `frontend/src/api/sessions.ts`
- `frontend/src/features/session/sessionRuntimeStore.ts`
- `frontend/src/features/session/sessionRuntimeStore.test.ts`
- `frontend/src/features/session/AudioSettingsStage.tsx`
- `frontend/src/features/session/AudioSettingsStage.test.tsx`
- `frontend/src/features/session/FinalizeStage.tsx`
- `frontend/src/features/session/chat/sessionChat.ts`
- `frontend/src/features/session/chat/actionEchoes.ts`
- `frontend/src/pages/session/SessionWorkspacePage.tsx`

The frontend now consumes the richer audio job model instead of treating narration as a simple percent/status pair.

Notable UI behavior changes:

- the audio stage shows `68% rendered`-style badge copy when narration is active
- the audio stage shows a `ProgressBar` with the backend-provided current step label
- the audio stage hint includes both step count and durable segment count
- workspace production copy prefers `current_step` text over generic status copy
- chat/system progress copy prefers backend-provided narration step text
- finalize view can describe in-progress narration using the same durable step model

## Examples Of New Abstractions And Extension Points

### 1. Recording richer audio progress from worker code

Use `record_audio_progress()` with explicit step metadata instead of only a status and percent.

Example shape:

```python
record_audio_progress(
    db_session,
    session_id=session_id,
    job_id=str(audio_job.id),
    status="in_progress",
    progress_percent=96,
    current_step="Mixing narration with the selected background bed.",
    current_step_index=5,
    total_steps=6,
    completed_segments=3,
    current_segment_index=3,
    total_segments=3,
    latest_asset_id=str(segment_asset.id),
    latest_asset_kind="narration_segment",
    message="Mixing narration with the selected background bed.",
)
```

Why this matters:

- the event log gets a human-readable summary
- hydration can rebuild the same job state later
- the frontend can render progress without guessing

### 2. Durable job config as the resume source of truth

`backend/app/services/audio_jobs.py` now stores narration progress details in `AudioJob.config_json`.

This is the extension point to preserve any future audio phase detail that should survive refreshes, for example:

- upload/publish subtasks
- waveform analysis state
- transcript alignment state
- post-processing quality checks

If future prompts add more narration phases, the pattern is:

1. write the new phase state into `config_json`
2. emit the same fields through `record_audio_progress()`
3. teach `session_hydration.py` and `session_realtime.py` to surface the new fields

### 3. Frontend rendering pattern for durable narration state

`AudioSettingsStage.tsx` now follows a clear display precedence:

1. `current_step`
2. `progress_percent`
3. fallback status text

That pattern is the right extension point for future long-running audio phases because it keeps the backend authoritative and the UI dumb.

## Exact Verification Work

### Backend verification

Ran:

- `cd backend && pytest tests/test_story_tools.py -k "audio_job_service or durable_narration_segments"`
- `cd backend && pytest tests/test_event_log_service.py tests/test_session_hydration_service.py`
- `cd backend && pytest tests/test_story_tools.py -k "audio_job_service or audio_runtime_worker_marks_failures_durably or retries_from_saved_segments_after_failure"`
- `cd backend && pytest tests/test_realtime_contracts.py tests/test_event_log_service.py tests/test_session_hydration_service.py tests/test_story_tools.py -k "audio_job_service or audio_runtime_worker_marks_failures_durably or retries_from_saved_segments_after_failure or durable_narration_segments"`
- `cd backend && ruff check app tests`

Results:

- all listed backend tests passed
- backend lint passed

New or expanded backend coverage includes:

- durable serialization of enriched audio progress payloads
- hydration of new audio job progress fields
- audio job retry-from-partial-output behavior
- segment attempt counting across failed and resumed runs
- realtime contract/schema regeneration coverage

### Frontend verification

Ran before and after the final formatting pass:

- `cd frontend && npm test -- src/features/session/sessionRuntimeStore.test.ts src/features/session/AudioSettingsStage.test.tsx src/features/session/FinalizeStage.test.tsx`
- `cd frontend && npm run lint`
- `cd frontend && npm run build`
- `cd frontend && npx prettier --check src/api/sessions.ts src/features/session/AudioSettingsStage.test.tsx src/features/session/AudioSettingsStage.tsx src/features/session/FinalizeStage.tsx src/features/session/chat/actionEchoes.ts src/features/session/chat/sessionChat.ts src/features/session/sessionRuntimeStore.test.ts src/features/session/sessionRuntimeStore.ts src/pages/session/SessionWorkspacePage.tsx src/styles/index.css`

Results:

- frontend targeted tests passed: 3 test files, 13 tests
- frontend lint passed
- frontend build passed
- touched frontend files pass Prettier check

Build note:

- Vite still reports the pre-existing large chunk warning for `dist/assets/index-*.js` at about 598 kB minified / 168 kB gzip
- this is a warning, not a failing build

### Browser and screenshot verification

I performed browser verification with a host-run Vite preview plus Puppeteer.

Why host-run instead of the normal Docker path:

- the repo QA skill expects Docker Compose
- Docker Desktop’s engine was down in this environment and `docker`/`docker compose` requests hung on the local socket
- I verified that from Docker Desktop logs before switching approaches

Browser verification steps:

1. Started `npm run preview -- --host 127.0.0.1 --port 8566` in `frontend/`
2. Drove `/sessions/moonlit-harbor?stage=audio` with Puppeteer
3. Intercepted API requests to provide a durable hydration payload containing an active audio job with:
   - `progress_percent: 68`
   - `current_step: "Mixing narration with the selected background bed."`
   - `current_step_index: 5`
   - `total_steps: 6`
   - `completed_segments: 3`
4. Asserted the page rendered:
   - `68% rendered`
   - `Mixing narration with the selected background bed.`
   - `Step 5 of 6. 3 of 3 narration segments are durable already. Estimated listening length 13 min.`
5. Captured a screenshot at:
   - `/Users/kevin/code/storyteller/.artifacts/webapp-qa/prompt-75-audio-progress-ui.png`

Browser result:

- passed

Coverage limit for the browser check:

- this verifies the final frontend rendering and hydration path with mocked API responses
- it does not verify a live Compose-backed backend-to-websocket round trip because Docker Desktop was unavailable

### Repo-level verification attempt

I attempted a broader `make check` pass.

Result:

- it failed at frontend Prettier check because the repository already contains unrelated formatting debt outside this prompt-75 change set

Action taken:

- I formatted the frontend files touched by prompt 75
- reran the focused frontend checks against the final filesystem state
- did not broaden the formatting sweep to unrelated files because that would inflate the scope of this task

## LLM Or Prompt Evaluation Suite

No new LLM or prompt evaluation suite was added.

Reason:

- this prompt did not modify prompts, model selection, intent parsing, or other LLM-facing behavior
- the changes were worker orchestration, event contracts, hydration, and frontend presentation

Named criteria status:

- `llm_prompt_changes_present`: `not_applicable`
- `model_wiring_changed`: `not_applicable`
- `prompt_eval_suite_required`: `not_applicable`

## Wrong Turns, Dead Ends, And Gotchas

- Docker Compose was the first verification plan, but `docker version`, `docker ps`, and `docker compose` all hung.
- Docker Desktop logs showed the Linux engine had been explicitly shut down and never came back during this run.
- Because of that, I switched from the normal Compose QA path to a host-run Vite preview plus Puppeteer interception.
- The app shell also probes `/api/hello`, so the browser harness needed to intercept that request in addition to the session hydration route.
- `make check` was not a useful final gate in this repo state because it tripped on existing frontend formatting debt outside the prompt-75 scope.
- One `git status` call raced a commit because I fired it in parallel with the commit command; I re-ran it immediately after and confirmed the tree was clean apart from Yolopilot logs.

## Assumptions I Had To Make

- No database migration was required because durable audio progress could live in existing JSON-backed job state and event payloads.
- The weighted audio progress checkpoints `86/90/96/99/100` are acceptable UX defaults until a later prompt asks for a different weighting policy.
- `current_step` should be the primary backend-to-frontend narration status string and should take precedence over generic status text.
- The latest persisted segment asset is the most useful artifact to surface for resume/debug visibility before final publish completes.
- Host-run browser verification with mocked API responses is an acceptable fallback when the intended Compose-based QA path is blocked by local Docker engine failure.

## Files Of Primary Interest For Review

- `backend/app/services/audio_jobs.py`
- `backend/app/services/session_hydration.py`
- `backend/app/services/session_realtime.py`
- `backend/app/services/event_log.py`
- `backend/app/models/events.py`
- `backend/app/models/session.py`
- `backend/tests/test_story_tools.py`
- `backend/tests/test_event_log_service.py`
- `frontend/src/features/session/AudioSettingsStage.tsx`
- `frontend/src/features/session/sessionRuntimeStore.ts`
- `frontend/src/pages/session/SessionWorkspacePage.tsx`
- `docs/realtime-events.schema.json`

## Final State

The branch is left in a coherent state with two prompt-75 commits:

- `102d52b feat(prompt-75): audio job orchestration`
- `0b40d11 chore(prompt-75): format frontend audio progress files`

The only untracked files left in the working tree are the Yolopilot log artifacts for this run, which I intentionally did not commit.
