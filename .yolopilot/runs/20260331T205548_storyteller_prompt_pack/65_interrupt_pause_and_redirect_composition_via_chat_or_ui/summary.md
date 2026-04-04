# Prompt 65: Interrupt, Pause, and Redirect Composition via Chat or UI

## What changed and why

This prompt needed composition to behave like a durable, steerable runtime instead of a fire-and-forget batch job. The core change is that pause and redirect are now modeled as first-class interruption requests that can be queued while writing is in progress, persisted in the database, replayed through session hydration/realtime, and applied only at safe worker checkpoints.

Before this change:

- `pause` could flip job state immediately even if the worker was still mid-segment.
- `redirect` could jump directly into rewrite behavior without preserving enough information about where the running draft actually was.
- the UI had partial pause/resume/rewrite affordances, but it did not have a durable backend-owned interruption state to explain "queued", "applying", or "waiting for a checkpoint".

After this change:

- active composition jobs can receive durable pause or redirect requests from either the UI or chat command paths;
- the backend records which job, segment, progress percentage, and instructions were active when the interruption was requested;
- the worker applies interruptions only after a saved checkpoint or segment boundary, with explicit status messages;
- the hydrated snapshot and realtime stream include interruption request state so the workspace can show `Pause queued` or `Redirect queued` with matching explanatory copy;
- the pending request is replayable after refresh and can be superseded or resolved explicitly.

## Architectural changes

### Durable interruption model

I added a new database concept in [backend/app/db/models.py](/Users/kevin/code/storyteller/backend/app/db/models.py) and migration [backend/migrations/versions/20260402_07_add_composition_interruption_requests.py](/Users/kevin/code/storyteller/backend/migrations/versions/20260402_07_add_composition_interruption_requests.py):

- `CompositionInterruptionRequest`
- `CompositionInterruptionKind`: `pause`, `redirect`
- `CompositionInterruptionState`: `requested`, `applying`, `applied`, `superseded`

Each request captures:

- the owning session and composition job
- origin (`workspace`, chat path, etc.)
- redirect instructions
- `rewrite_from_segment_index`
- the requested segment/progress snapshot at request time
- resolution summary and resolution timestamp
- request metadata used for replay/debugging

I also added the typed view model and shared copy helper in [backend/app/models/composition_interruptions.py](/Users/kevin/code/storyteller/backend/app/models/composition_interruptions.py) so the same interruption message can be reused in hydration, realtime payloads, and UI rendering.

### Composition job state machine

The main orchestration work lives in [backend/app/services/composition_jobs.py](/Users/kevin/code/storyteller/backend/app/services/composition_jobs.py).

Key behavior changes:

- `pause_job(...)` now queues a durable interruption request when the job is already `in_progress`. For a merely `queued` job it can still pause immediately.
- `request_redirect(...)` now mirrors that behavior: queue while `in_progress`, apply immediately only when the job is in a safe state.
- the worker loop checks for pending interruptions before starting queued work, after chunk checkpoints, and after completed segments.
- redirect application explicitly captures the safe rewrite boundary and starts the rewrite only after the prior draft is cancelled at a durable checkpoint.
- pending interruption requests are superseded when a newer interruption wins or when resume/cancel makes the queued request irrelevant.

Two helper surfaces are intended to be reused:

```python
result = CompositionJobService(session).request_redirect(
    session_id,
    composition_job_id,
    instructions="Introduce the otter earlier and soften the midpoint.",
    rewrite_from_segment_index=2,
    origin="workspace",
)

# result.response_job_id is the job the caller should resolve back to the UI.
```

```python
CompositionJobService(session).pause_job(session_id, composition_job_id)

# For in-progress jobs this now records a durable interruption request instead of
# pretending the worker has already stopped.
```

### Replay, hydration, realtime, and policy propagation

The interruption state is now carried end-to-end:

- [backend/app/models/session.py](/Users/kevin/code/storyteller/backend/app/models/session.py)
- [backend/app/models/events.py](/Users/kevin/code/storyteller/backend/app/models/events.py)
- [backend/app/models/realtime.py](/Users/kevin/code/storyteller/backend/app/models/realtime.py)
- [backend/app/services/session_hydration.py](/Users/kevin/code/storyteller/backend/app/services/session_hydration.py)
- [backend/app/services/session_realtime.py](/Users/kevin/code/storyteller/backend/app/services/session_realtime.py)
- [backend/app/services/event_log.py](/Users/kevin/code/storyteller/backend/app/services/event_log.py)

That means a hydrated snapshot now exposes:

```python
snapshot.active_composition_job.interruption_request.message
```

and the realtime progress/status events can replay the same interruption payload to reconnecting clients.

### UI and chat surface updates

The workspace now treats interruption state as a first-class composition status:

- [frontend/src/features/session/CompositionStage.tsx](/Users/kevin/code/storyteller/frontend/src/features/session/CompositionStage.tsx)
- [frontend/src/features/session/sessionRuntimeStore.ts](/Users/kevin/code/storyteller/frontend/src/features/session/sessionRuntimeStore.ts)
- [frontend/src/features/session/live/sessionRealtime.ts](/Users/kevin/code/storyteller/frontend/src/features/session/live/sessionRealtime.ts)
- [frontend/src/pages/session/SessionWorkspacePage.tsx](/Users/kevin/code/storyteller/frontend/src/pages/session/SessionWorkspacePage.tsx)
- [frontend/src/features/session/chat/sessionChat.ts](/Users/kevin/code/storyteller/frontend/src/features/session/chat/sessionChat.ts)
- [frontend/src/features/session/chat/actionEchoes.ts](/Users/kevin/code/storyteller/frontend/src/features/session/chat/actionEchoes.ts)
- [frontend/src/features/session/chat/chatCommands.ts](/Users/kevin/code/storyteller/frontend/src/features/session/chat/chatCommands.ts)

User-visible effects:

- a pending badge: `Pause queued` or `Redirect queued`
- a dedicated `Pending change` summary panel
- interruption-aware rewrite note copy
- controls disabled while an interruption request is already pending
- chat/progress copy preferring interruption state over generic job-status phrasing
- quick actions hiding redundant pause requests when one is already pending

## Verification

### Automated verification

Backend:

- `pytest backend/tests/test_story_tools.py backend/tests/test_migrations.py -q`
  - `29 passed`
- `pytest backend/tests/test_realtime_contracts.py -q`
  - `5 passed`
- `pytest backend/tests/test_intent_parser_service.py -q`
  - `6 passed`
- `pytest backend/tests -q`
  - `230 passed, 5 skipped`
- `ruff check backend/app/repositories/events.py backend/app/services/composition_jobs.py backend/app/services/event_log.py backend/app/api/v1/routes/sessions.py backend/app/services/session_hydration.py backend/app/services/session_realtime.py backend/app/services/action_policy.py backend/app/services/intent_parser.py backend/app/models/composition_interruptions.py backend/app/models/__init__.py backend/app/models/session.py backend/app/models/events.py backend/app/models/realtime.py backend/app/db/__init__.py backend/app/db/models.py backend/tests/test_story_tools.py backend/tests/test_migrations.py`
  - passed

Frontend:

- `npm test -- src/features/session/CompositionStage.test.tsx src/features/session/chat/chatCommands.test.ts src/features/session/chat/actionEchoes.test.ts src/features/session/sessionRuntimeStore.test.ts`
  - `4 files passed, 20 tests passed`
- `npm test`
  - `17 files passed, 98 tests passed`
- `npm run lint`
  - passed
- `npm run build`
  - passed
  - remaining note: Vite still emits the existing chunk-size warning for the main frontend bundle

New or expanded tests that matter most for this prompt:

- [backend/tests/test_story_tools.py](/Users/kevin/code/storyteller/backend/tests/test_story_tools.py)
  - `test_composition_pause_request_is_durable_and_applies_after_checkpoint`
  - `test_composition_redirect_request_is_durable_and_starts_rewrite_after_checkpoint`
- [frontend/src/features/session/CompositionStage.test.tsx](/Users/kevin/code/storyteller/frontend/src/features/session/CompositionStage.test.tsx)
  - queued interruption state is rendered and relevant controls are locked
- [frontend/src/features/session/sessionRuntimeStore.test.ts](/Users/kevin/code/storyteller/frontend/src/features/session/sessionRuntimeStore.test.ts)
  - replayable interruption details merge correctly into runtime state
- [frontend/src/features/session/chat/actionEchoes.test.ts](/Users/kevin/code/storyteller/frontend/src/features/session/chat/actionEchoes.test.ts)
  - chat history prefers interruption-aware copy
- [frontend/src/features/session/chat/chatCommands.test.ts](/Users/kevin/code/storyteller/frontend/src/features/session/chat/chatCommands.test.ts)
  - redundant pause quick actions disappear when one is already pending
- [backend/tests/test_migrations.py](/Users/kevin/code/storyteller/backend/tests/test_migrations.py)
  - added a guard that every Alembic revision id fits the live `alembic_version` column width
- [backend/tests/test_intent_parser_service.py](/Users/kevin/code/storyteller/backend/tests/test_intent_parser_service.py)
  - explicit `/plan` summaries now cover interruption-aware copy

### Browser and visual verification

The compose stack was already running, so I reused it. The dedicated `odysseus` CLI mentioned by the visual-QA skill was not installed in this repo context, so I used the compose `browser` service with Puppeteer.

I also had to run:

- `docker compose -f infra/compose/docker-compose.yml exec -T backend alembic upgrade head`

because the live compose database had not yet been migrated to include the new interruption table.

Browser artifacts:

- [prompt-65-pause-queued-desktop.png](/Users/kevin/code/storyteller/.artifacts/webapp-qa/prompt-65-pause-queued-desktop.png)
- [prompt-65-redirect-queued-desktop.png](/Users/kevin/code/storyteller/.artifacts/webapp-qa/prompt-65-redirect-queued-desktop.png)
- [prompt-65-redirect-queued-mobile.png](/Users/kevin/code/storyteller/.artifacts/webapp-qa/prompt-65-redirect-queued-mobile.png)

What I visually verified:

- desktop pause state shows the `Pause queued` panel and explanation
- desktop redirect state shows the `Redirect queued` panel and explanation
- mobile/narrow layout still surfaces the pending-change card and the disabled rewrite area without layout breakage

What I functionally verified in-browser:

- `pause-desktop: pauseDisabled=true rewriteDisabled=true`
- `redirect-desktop: pauseDisabled=true rewriteDisabled=true`

These DOM checks were performed against the live compose frontend after seeding real session data into the running Postgres database.

### LLM / prompt-facing evaluation notes

I did not change model IDs, prompt schemas, or generation prompts for this task, so I did not add a new broad LLM evaluation harness.

I did add deterministic coverage for the one prompt-adjacent behavior that changed:

- `explicit_plan_summary_includes_pending_composition_interruption`
  - criterion: explicit `/plan` summaries must surface the interruption-aware composition message when a pending redirect exists
  - result: `PASS`

## Wrong turns, surprises, and gotchas

- The new concurrency-style pause test exposed a real event-log race: `EventLogRepository.append()` was still doing `MAX(sequence_number) + 1` as a separate read before insert. Under concurrent worker/user writes this caused `UNIQUE constraint failed` on `(session_id, sequence_number)`. I fixed that by retrying event inserts inside a savepointed unique-conflict loop in [backend/app/repositories/events.py](/Users/kevin/code/storyteller/backend/app/repositories/events.py).
- The first live compose migration attempt failed even though the migration itself was correct, because the Alembic revision id `20260402_07_composition_interruptions` exceeded the live `alembic_version.version_num` width. I shortened the revision id to `20260402_07_comp_interrupts` and added a migration test so this fails in CI instead of during local upgrade.
- The compose database was not on the latest schema even though the app containers were up. I migrated it in place for QA.
- My first mobile screenshot scrolled to the chat textarea instead of the composition rewrite controls because the page has more than one textarea. I retook the narrow capture anchored on the pending-change card and rewrite button.
- While wiring redirect application, I hit an `autoflush=False` interaction: marking an interruption request `APPLIED` and then querying for active requests could accidentally reclassify it as `SUPERSEDED` unless the request state was flushed before cancellation logic queried again. That explicit flush remains in the redirect path for correctness.

## Assumptions made while working unsupervised

- I assumed it was acceptable to migrate the running local compose database in place because this repo’s visual-QA workflow depends on the live dev stack and the migration is part of the prompt’s production path.
- I assumed seeding temporary QA-only sessions directly into the compose Postgres database was preferable to depending on live Gemini calls, because the task required deterministic browser verification and there was no interactive human available to resolve flaky provider behavior.
- I assumed `.yolopilot` run metadata was automation noise and should remain unmodified except for the required final summary file.
- I assumed the existing Vite chunk-size warning was not introduced by this prompt, since the frontend build stayed green and the warning remained informational rather than failing the build.

## Commit checkpoints

- `f9cb89b` `feat(prompt-65): add durable composition interruptions`
- `7ab27b3` `feat(prompt-65): surface composition interruption state in the workspace`
- `d7df006` `test(prompt-65): cover interruption-aware plan summaries`
