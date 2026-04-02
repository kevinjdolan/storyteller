# Prompt 66: Rewrite Prior Segments And Regenerate Downstream Text

Commit: `34a45bb` (`feat(prompt-66): rewrite prior segments`)

## What I changed and why

This prompt needed three product behaviors to become real rather than implied:

1. A user must be able to target an already-written segment or segment range with explicit rewrite instructions.
2. The system must make downstream continuity impact visible instead of silently mutating later text.
3. Rewritten text must not overwrite accepted manuscript text until the user explicitly accepts it.

I implemented that as a rewrite-review workflow rather than an immediate destructive rewrite.

On the backend, rewrites now produce candidate segment revisions with preserved history. Accepted manuscript revisions stay current until the rewrite is accepted. When a rewrite only changes part of the manuscript and downstream text exists, the job records whether downstream text should be auto-regenerated or marked stale pending confirmation. That stale state is stored durably per segment and surfaced in the session snapshot.

On the frontend, the composition stage now exposes a dedicated rewrite range UI, a review/compare state for pending rewrite candidates, and explicit stale downstream indicators after acceptance. The user can inspect current accepted text, pending rewrite text, and older revisions side by side.

## Architectural changes across the codebase

### Database and persistence

- Added rewrite/staleness job metadata to `composition_jobs`:
  - `rewrite_to_segment_index`
  - `downstream_regeneration_mode`
  - `stale_from_segment_index`
  - `stale_to_segment_index`
- Added review/staleness metadata to `composition_segments`:
  - `acceptance_state`
  - `is_stale`
  - `stale_reason`
  - `stale_at`
  - `stale_by_job_id`
- Added enums for downstream handling and segment acceptance state.
- Added Alembic revision `backend/migrations/versions/20260402_08_add_composition_rewrite_review_state.py`.

### Backend services

- `CompositionJobService.start_job(...)` now understands rewrite ranges and downstream handling.
- Added rewrite planning logic so a rewrite can:
  - stay local to the requested range,
  - auto-extend through downstream segments,
  - or require acceptance first and then mark downstream segments stale.
- Added `CompositionJobService.accept_rewrite_job(...)` to:
  - promote pending rewrite candidates to accepted revisions,
  - supersede prior accepted revisions,
  - rebuild the final story asset,
  - mark downstream segments stale when confirmation mode was requested,
  - update composition stage status to either `completed` or `needs_regeneration`.
- Extended hydration to emit `composition_segments` with per-version history, current revision ids, pending revision ids, and stale flags.
- Fixed a worker durability bug in `run_job()` by committing persisted state before returning from:
  - `queued_next_segment`
  - `pending_review`
  - `completed`

### API surface

- Extended composition start/redirect request models with:
  - `rewrite_to_segment_index`
  - `downstream_regeneration_mode`
- Added `POST /api/v1/sessions/{session_id}/composition/{composition_job_id}/accept`
- Extended session snapshot/job views to include rewrite review and stale-range metadata.

### Frontend

- Extended `frontend/src/api/sessions.ts` with rewrite-review fields and the accept endpoint client.
- Reworked `frontend/src/features/session/CompositionStage.tsx` to support:
  - rewrite-from / rewrite-through controls
  - downstream handling selection
  - pending rewrite review UI
  - accepted-vs-pending compare cards
  - version history rendering
  - stale downstream badges and summaries
- Wired accept/rewrite actions through `SessionWorkspacePage`.
- Added/updated styles in `frontend/src/styles/index.css`.

## New abstractions, helpers, and extension points

### Rewrite request payloads

The composition API now accepts range-aware rewrite requests.

```json
{
  "mode": "rewrite",
  "instructions": "Soften the harbor opening and bring Pip into view immediately.",
  "restart_from_segment_index": 1,
  "rewrite_to_segment_index": 1,
  "downstream_regeneration_mode": "require_confirmation",
  "origin": "workspace"
}
```

The redirect path accepts the same rewrite range/downstream options:

```json
{
  "instructions": "Rewrite the midpoint and keep the reveal gentler.",
  "rewrite_from_segment_index": 2,
  "rewrite_to_segment_index": 3,
  "downstream_regeneration_mode": "auto_regenerate",
  "origin": "workspace"
}
```

### Rewrite acceptance

Backend service entry point:

```python
CompositionJobService(session).accept_rewrite_job(session_id, composition_job_id)
```

HTTP entry point:

```text
POST /api/v1/sessions/{session_id}/composition/{composition_job_id}/accept
```

### Hydrated segment version model

`SessionSnapshot.composition_segments` now carries durable per-segment review state. Each segment includes:

- `current_version_id`
- `pending_version_id`
- `is_stale`
- `stale_reason`
- `versions[]` with revision number, acceptance state, text, and job lineage

That gives future UI work a stable extension point for richer diffing, selective rollback, or bulk-regeneration flows.

## Verification work performed

### Automated verification

Commands run:

- `pytest backend/tests/test_story_tools.py -k "rewrite_job_requires_acceptance_before_promoting_segment_revisions or accepting_manual_rewrite_marks_downstream_segments_stale"`  
  Result: passed
- `npm --prefix frontend test -- CompositionStage.test.tsx`  
  Result: passed
- `pytest backend/tests/test_story_tools.py -k "persists_draft_progress_across_sessions or persists_rewrite_review_state_across_sessions"`  
  Result: passed
- `pytest backend/tests/test_story_tools.py backend/tests/test_session_hydration_service.py backend/tests/test_session_api.py`  
  Result: `75 passed`
- `pytest backend/tests/test_migrations.py -k "upgrade_from_zero_to_head_and_back"`  
  Result: passed
- `ruff check backend/app backend/tests`  
  Result: passed
- `ruff check backend/migrations/versions/20260402_08_add_composition_rewrite_review_state.py`  
  Result: passed
- `npm --prefix frontend run lint`  
  Result: passed
- `npm --prefix frontend run build`  
  Result: passed, with an existing Vite chunk-size warning for the frontend bundle

### Browser and visual verification

I used the repo’s `webapp-qa` flow against the compose stack at `http://localhost:8566`.

Browser checks completed:

- Pending review screenshot spec:  
  `docker compose -f infra/compose/docker-compose.yml run --rm browser npm run check -- --spec ../../.artifacts/webapp-qa/prompt-66-rewrite-review.spec.json`  
  Result: passed
- Accepted stale-state screenshot spec:  
  `docker compose -f infra/compose/docker-compose.yml run --rm browser npm run check -- --spec ../../.artifacts/webapp-qa/prompt-66-rewrite-accept.spec.json`  
  Result: passed
- Direct Puppeteer accept click:
  - clicked the review-state accept button inside the live composition workspace
  - verified via API snapshot that `pending_review` became `false`
  - verified via API snapshot that stale segments were `[2, 3]`

Screenshot outputs:

- `.artifacts/webapp-qa/prompt-66-rewrite-review.png`
- `.artifacts/webapp-qa/prompt-66-rewrite-accepted.png`

Visual coverage notes:

- The browser container reported a WebSocket connection warning for `ws://frontend:8566/api/v1/sessions/events/ws`. The workspace still functioned through HTTP hydration and action responses, and the accept flow updated durable backend state correctly.
- For reliable browser QA, I seeded a deterministic local session state with the backend service layer and the deterministic `RecordingCompositionWriter` used in backend tests. I did not depend on a live Gemini generation pass.

## LLM-facing evaluation suite

I did not change model IDs, prompt templates, or provider selection. I did change composition orchestration behavior around rewrite persistence and acceptance, so I treated the new deterministic backend regression tests as the evaluation suite for the LLM-facing workflow.

Named criteria and outcomes:

- `rewrite_queue_persistence`  
  Backed by `test_run_job_persists_draft_progress_across_sessions`  
  Result: pass
- `rewrite_review_persistence`  
  Backed by `test_run_job_persists_rewrite_review_state_across_sessions`  
  Result: pass
- `rewrite_acceptance_gate`  
  Backed by `test_rewrite_job_requires_acceptance_before_promoting_segment_revisions`  
  Result: pass
- `rewrite_downstream_invalidation`  
  Backed by `test_accepting_manual_rewrite_marks_downstream_segments_stale`  
  Result: pass

These tests cover the core workflow contract: queued segment persistence, candidate rewrite review, explicit acceptance before manuscript replacement, and durable downstream invalidation.

## Wrong turns, dead ends, and gotchas

- I initially added the new `stale_by_job_id` foreign key without constraining the ORM relationships, which introduced an `AmbiguousForeignKeysError` between `composition_jobs` and `composition_segments`.
- Hydration initially referenced `_read_mapping(...)` without defining it in `session_hydration.py`.
- The Alembic revision first used `is_stale = 0`, which broke the live Postgres upgrade because `is_stale` is a boolean column there.
- The same migration also failed the repo migration test because:
  - plain `create_foreign_key` is not SQLite-safe
  - plain `ALTER COLUMN ... DROP DEFAULT` is not SQLite-safe
  I corrected both by using batch mode for the FK and skipping `DROP DEFAULT` on SQLite.
- The most important real bug surfaced during live QA, not unit tests: `CompositionJobService.run_job()` returned `queued_next_segment`, `pending_review`, and `completed` states without committing them. That meant worker-owned session state was not durable across sessions, and re-running a queued job could reopen the already-written segment and collide on the same segment asset path. I fixed that and added fresh-session regression tests.
- Browser timing around the accept button was flaky in the QA container, so I separated the proof into:
  - a pending-review screenshot spec
  - a direct Puppeteer accept click
  - an accepted-state screenshot spec
  plus an API snapshot check for stale segment ids

## Assumptions made while working unsupervised

- I assumed the correct UX was “rewrite candidates require explicit acceptance” whenever accepted manuscript text is being replaced, even if downstream text does not need staleness handling.
- I assumed downstream handling should remain explicit and user-visible even when the actual regeneration action is deferred to future work.
- I assumed using the deterministic writer from backend tests was the safest way to verify the browser flow locally without relying on live provider keys or nondeterministic model output.
- I assumed it was acceptable to use an existing local composition session for browser QA seeding, because that state change was only for local verification and not part of the committed code.

## Final state

The code checkpoint for prompt 66 is committed at `34a45bb`.

The only remaining uncommitted files in the worktree after the commit were yolopilot bookkeeping/log files outside the prompt-66 code changes and this summary file itself.
