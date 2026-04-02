# Prompt 62 Summary: Composition Streaming Events

## What I Changed and Why

I implemented end-to-end composition streaming so the composition stage can render a live, typewriter-style manuscript instead of waiting for finished segment dumps.

On the backend, I added a realtime session feed for composition-aware updates, introduced chunking helpers that split accepted prose into readable deltas, and persisted enough composition metadata on the durable job row for reconnect recovery. The key behavior change is that a reconnecting client no longer depends on catching every live chunk in order; it can rebuild from the accepted checkpoint already stored in the session snapshot, then continue with fresh deltas.

On the frontend, I added a dedicated `CompositionStage` UI and runtime state for composition streams. The workspace now shows the current manuscript, the live/saved source badge, progress, the latest segment recap, and composition controls for start, pause, resume, cancel, and rewrite. The runtime store merges durable snapshot state with ephemeral `composition.chunk` events so the page can feel live without treating the browser as the source of truth.

I also split the work into reviewable commits:

- `bcced2e` `feat(prompt-62): stream composition events from backend`
- `5bf4792` `feat(prompt-62): render live composition chunks in workspace`
- `c9ebf5d` `test(prompt-62): verify streaming chunk pacing`

## Architectural Changes

### Backend realtime pipeline

- Added [`backend/app/api/v1/routes/session_events.py`](/Users/kevin/code/storyteller/backend/app/api/v1/routes/session_events.py), a websocket endpoint at `/api/v1/sessions/events/ws`.
- Added [`backend/app/services/session_realtime.py`](/Users/kevin/code/storyteller/backend/app/services/session_realtime.py), which:
  - replays durable event-log entries into the existing realtime contract,
  - synthesizes `composition.chunk` events from active composition job metadata,
  - tracks per-connection chunk cursors so reconnecting clients only receive the missing delta text,
  - uses replay strategies that distinguish plain delta replay from durable snapshot hydration.
- Wired the router through [`backend/app/api/v1/router.py`](/Users/kevin/code/storyteller/backend/app/api/v1/router.py).

### Composition chunking and durability

- Added [`backend/app/services/composition_streaming.py`](/Users/kevin/code/storyteller/backend/app/services/composition_streaming.py).
- Introduced:
  - `build_accepted_story_so_far(completed_segments, current_text=None)`
  - `split_text_for_streaming(prefix, remaining_text)`
  - `STREAMING_MIN_CHUNK_WORDS = 8`
  - `STREAMING_MAX_CHUNK_WORDS = 22`
  - `STREAMING_TARGET_CHUNK_CHARACTERS = 120`
- Updated [`backend/app/services/composition_jobs.py`](/Users/kevin/code/storyteller/backend/app/services/composition_jobs.py) so composition jobs now persist:
  - `accepted_story_so_far`
  - `latest_partial_output`
  - `latest_segment_summary`
  - `current_segment_id`
- Added an intentional local-dev chunk delay in the worker entrypoint:
  - [`backend/app/worker/__main__.py`](/Users/kevin/code/storyteller/backend/app/worker/__main__.py) now runs composition jobs with `composition_chunk_delay_seconds=0.12`
  - tests still use the default zero-delay path so backend suites stay fast

### Snapshot and event contract updates

- Extended [`backend/app/models/session.py`](/Users/kevin/code/storyteller/backend/app/models/session.py) and [`backend/app/services/session_hydration.py`](/Users/kevin/code/storyteller/backend/app/services/session_hydration.py) so composition snapshots expose the new durable checkpoint fields.
- Updated [`backend/app/models/events.py`](/Users/kevin/code/storyteller/backend/app/models/events.py) and [`backend/app/services/event_log.py`](/Users/kevin/code/storyteller/backend/app/services/event_log.py) so chat-message events retain the full message content plus an explicit plain-text format marker. That keeps chat replay compatible with the realtime feed instead of only replaying previews.

### Frontend live composition runtime

- Added [`frontend/src/features/session/CompositionStage.tsx`](/Users/kevin/code/storyteller/frontend/src/features/session/CompositionStage.tsx), a dedicated composition panel.
- Expanded [`frontend/src/features/session/sessionRuntimeStore.ts`](/Users/kevin/code/storyteller/frontend/src/features/session/sessionRuntimeStore.ts) with `SessionCompositionStreamState`, plus helpers to:
  - hydrate from snapshot,
  - apply `composition.chunk`,
  - apply `job.progress`,
  - apply `job.status`,
  - reset transient chunk state at segment boundaries.
- Added `useSessionCompositionStream()` via [`frontend/src/features/session/sessionWorkspaceContext.ts`](/Users/kevin/code/storyteller/frontend/src/features/session/sessionWorkspaceContext.ts).
- Updated [`frontend/src/features/session/SessionWorkspaceProvider.tsx`](/Users/kevin/code/storyteller/frontend/src/features/session/SessionWorkspaceProvider.tsx) so websocket subscription acks can trigger snapshot refresh when the server says the client should hydrate.
- Updated [`frontend/src/pages/session/SessionWorkspacePage.tsx`](/Users/kevin/code/storyteller/frontend/src/pages/session/SessionWorkspacePage.tsx) to:
  - render the new composition stage,
  - call start/pause/resume/cancel/rewrite APIs,
  - bridge composition actions through chat commands.
- Updated [`frontend/src/api/sessions.ts`](/Users/kevin/code/storyteller/frontend/src/api/sessions.ts) with composition control endpoints and the richer composition job view.
- Updated [`frontend/src/features/session/chat/actionEchoes.ts`](/Users/kevin/code/storyteller/frontend/src/features/session/chat/actionEchoes.ts) so job progress/status history is represented in the chat log as compact UI-originated summaries.

### Frontend transport and local dev plumbing

- Updated [`frontend/src/features/session/live/sessionRealtimeClient.ts`](/Users/kevin/code/storyteller/frontend/src/features/session/live/sessionRealtimeClient.ts) to expose the subscription ack to the workspace layer.
- Enabled websocket proxying in [`frontend/vite.config.ts`](/Users/kevin/code/storyteller/frontend/vite.config.ts).
- Added `VITE_SESSION_EVENTS_WS_URL: /api/v1/sessions/events/ws` in [`infra/compose/docker-compose.yml`](/Users/kevin/code/storyteller/infra/compose/docker-compose.yml).
- Added composition-stage CSS in [`frontend/src/styles/index.css`](/Users/kevin/code/storyteller/frontend/src/styles/index.css).

## New Helpers and Extension Points

### 1. Splitting accepted prose into live deltas

Example:

```python
from app.services.composition_streaming import split_text_for_streaming

accepted_text = "Mira followed the bell. Otis stayed close. The harbor quieted."
chunks = split_text_for_streaming("", accepted_text)
```

Use this helper when a durable accepted segment needs to be replayed as intentional UI-sized chunks. It preserves exact text reconstruction while aiming for readable chunk sizes instead of token-by-token noise.

### 2. Realtime subscription handshake

Example first-frame payload:

```json
{
  "schema_version": 1,
  "action": "subscribe",
  "session_id": "f188d7f8-d670-478c-9750-03a723027dd5",
  "tab_id": "tab-123",
  "last_sequence_number": 41
}
```

The server responds with a `subscribed` ack that includes:

- the session-scoped channel name,
- the accepted replay strategy,
- the latest durable sequence number,
- whether the client should replay deltas or rehydrate from the snapshot API.

### 3. Frontend composition runtime state

If another stage needs to layer ephemeral live events on top of durable snapshots, the pattern in [`frontend/src/features/session/sessionRuntimeStore.ts`](/Users/kevin/code/storyteller/frontend/src/features/session/sessionRuntimeStore.ts) is the intended extension point:

- keep the durable snapshot as canonical,
- keep ephemeral live state in a narrow, stage-specific branch,
- rebuild that branch from snapshot on reconnect,
- treat websocket deltas as enhancements, not the only truth.

## Exact Verification Work

### Backend tests

Ran:

```bash
cd backend
pytest tests/test_session_api.py::test_session_events_websocket_replays_composition_job_status \
  tests/test_session_api.py::test_session_realtime_service_streams_composition_chunk_deltas \
  tests/test_session_api.py::test_session_realtime_service_suppresses_initial_chunk_baseline_and_keeps_snapshot_recoverable \
  tests/test_story_tools.py::test_split_text_for_streaming_preserves_exact_story_text
```

Result: passed.

Ran:

```bash
cd backend
pytest tests/test_session_api.py::test_composition_control_endpoints_manage_durable_job_state \
  tests/test_session_api.py::test_redirect_composition_endpoint_queues_rewrite_job \
  tests/test_realtime_contracts.py
```

Result: passed.

Ran after the final pacing test was added:

```bash
cd backend
pytest tests/test_story_tools.py::test_split_text_for_streaming_preserves_exact_story_text \
  tests/test_story_tools.py::test_split_text_for_streaming_targets_readable_live_chunks
```

Result: `2 passed`.

### Frontend tests

Ran:

```bash
cd frontend
npm test -- --run \
  src/features/session/sessionRuntimeStore.test.ts \
  src/features/session/live/sessionRealtimeClient.test.ts \
  src/features/session/CompositionStage.test.tsx \
  src/features/session/chat/actionEchoes.test.ts \
  src/pages/session/SessionWorkspacePage.test.tsx
```

Result: passed.

### Lint and build

Ran:

```bash
cd frontend
npm run lint
npm run build
```

Result:

- `npm run lint`: passed
- `npm run build`: passed
- Vite still reported the existing large-chunk warning for the main bundle; the build succeeded and I did not scope creep into unrelated bundle splitting work

Ran:

```bash
cd backend
ruff check app/services/composition_jobs.py \
  app/services/session_realtime.py \
  app/api/v1/routes/session_events.py \
  tests/test_session_api.py \
  tests/test_story_tools.py
```

Result: passed.

Limit:

- a repo-wide `ruff check app tests` still fails because of unrelated pre-existing issues in files outside this prompt’s scope, including `app/services/action_policy.py`, `tests/test_chat_action_contracts.py`, and `tests/test_intent_parser_service.py`

### Browser and live-stack verification

Used the `webapp-qa` workflow against the Docker Compose stack.

Ran:

```bash
cd infra/compose
docker compose up -d --build
docker compose ps
docker compose exec -T backend alembic upgrade head
```

The migration step was necessary because the persisted local Postgres volume was behind the current schema.

To seed browser-verifiable composition-stage sessions against the live Postgres database, I used the existing stub generation adapters from `backend/tests/test_session_api.py` via a host-side `TestClient`, so the live frontend/backend containers could operate on durable, composition-ready sessions without requiring external model success for upstream planning stages.

Created dedicated browser QA sessions:

- live chunk session: `f188d7f8-d670-478c-9750-03a723027dd5`
- reconnect session: `129bc8da-af28-4cb2-a806-88057dffaeec`

Ran:

```bash
cd infra/compose
docker compose run --rm browser npm run check -- --spec /workspace/.artifacts/webapp-qa/composition-live.spec.json
docker compose run --rm browser npm run check -- --spec /workspace/.artifacts/webapp-qa/composition-reconnect.spec.json
```

Result: both passed.

Artifacts:

- live stream screenshot: [`composition-live.png`](/Users/kevin/code/storyteller/.artifacts/webapp-qa/composition-live.png)
- reconnect screenshot: [`composition-reconnect.png`](/Users/kevin/code/storyteller/.artifacts/webapp-qa/composition-reconnect.png)
- live spec: [`composition-live.spec.json`](/Users/kevin/code/storyteller/.artifacts/webapp-qa/composition-live.spec.json)
- reconnect spec: [`composition-reconnect.spec.json`](/Users/kevin/code/storyteller/.artifacts/webapp-qa/composition-reconnect.spec.json)

What I visually verified:

- the composition stage renders the live manuscript surface in the workspace
- starting composition from the UI transitions the stage into the live state and shows the `Live chunks` badge
- manuscript text appears during the run instead of only after completion
- refreshing the page on an in-flight session still shows the recovered accepted manuscript state

Browser-run caveat:

- the Puppeteer logs showed transient websocket-close warnings around page lifecycle changes, but the composition stage still reached the `Live chunks` state and reconnect recovery spec passed

## Evaluation Coverage

I did not add a new prompt-eval harness because this prompt did not change prompt templates, model selection, or provider wiring. The change was in streaming, replay, and checkpoint recovery around already-generated text.

I did add deterministic coverage for the behavior that matters here. The effective evaluation criteria and outcomes are:

- `Exact story reconstruction from chunks`: pass
  - verified by `test_split_text_for_streaming_preserves_exact_story_text`
- `Readable live chunk pacing bounds`: pass
  - verified by `test_split_text_for_streaming_targets_readable_live_chunks`
- `Realtime chunk delta replay from active job metadata`: pass
  - verified by `test_session_realtime_service_streams_composition_chunk_deltas`
- `Suppress initial chunk baseline while preserving snapshot-based recovery`: pass
  - verified by `test_session_realtime_service_suppresses_initial_chunk_baseline_and_keeps_snapshot_recoverable`
- `Durable websocket replay of job status events`: pass
  - verified by `test_session_events_websocket_replays_composition_job_status`

## Wrong Turns, Dead Ends, and Gotchas

- I initially ran browser specs against a session that had already started composing. The live-stream assertion became timing-sensitive and occasionally missed the live window. I changed approach and created composition-ready sessions that start writing from the UI during the browser run.
- I initially wrote browser spec files under `/tmp`. The browser container could not see those host paths. I moved the specs to the repo-mounted `.artifacts/webapp-qa/` directory.
- The persisted Compose Postgres volume was behind the repo’s migrations. Seeding a live session failed on a missing `session_usage_rollups` table until I ran `alembic upgrade head` inside the backend container.
- My first instinct for websocket verification was to assert exact frame sequencing at the socket layer. That was brittle and slower than necessary. I shifted the critical replay coverage into deterministic service-level cursor tests and kept the browser verification focused on observable UI behavior.

## Assumptions I Had To Make

- Synthesizing `composition.chunk` events from durable job and segment metadata was acceptable and preferable to introducing a separate transient event broker just for local development.
- A 120ms chunk delay in the worker is a good local default for a lively typewriter effect without slowing automated backend tests; tests continue to use the zero-delay service path.
- Snapshot hydration is the right reconnect strategy whenever the server believes the client might have missed in-flight chunk state, especially for active or paused composition jobs.
- Full message content belongs in replayable chat events so the chat pane and workspace controls can stay aligned after reconnect, even though earlier code only stored previews.
