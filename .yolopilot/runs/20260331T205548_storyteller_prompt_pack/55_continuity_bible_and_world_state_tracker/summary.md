# Prompt 55: Continuity Bible and World-State Tracker

## What I changed and why

I added a durable continuity-bible layer so the app can remember canonical facts across long planning, composition, and rewrite flows without depending on ad hoc prompt stitching.

The backend now stores selected continuity revisions per session, rebuilds them whenever accepted planning decisions or composition checkpoints materially change the story state, hydrates them back into the session snapshot, and injects the selected continuity payload into composition and rewrite job metadata.

On the frontend, I exposed the hydrated continuity bible in the workspace as an optional inspector panel so reviewers and future prompt work can see exactly which facts are currently being treated as canonical.

I split the implementation into two reviewable commits:

- `ffe3107` `feat(prompt-55): add durable continuity bible backend`
- `dae6afd` `feat(prompt-55): add workspace continuity inspector`

## Architectural changes across the codebase

### Durable model and persistence

- Added [backend/app/models/continuity.py](/Users/kevin/code/storyteller/backend/app/models/continuity.py) with:
  - `ContinuityFactCategory`
  - `ContinuityFact`
  - `ContinuityBibleData`
  - `ContinuityBibleView`
- Added `continuity_bibles` persistence in [backend/app/db/models.py](/Users/kevin/code/storyteller/backend/app/db/models.py) and exported it from [backend/app/db/__init__.py](/Users/kevin/code/storyteller/backend/app/db/__init__.py).
- Added Alembic migration [backend/migrations/versions/20260402_03_add_continuity_bibles.py](/Users/kevin/code/storyteller/backend/migrations/versions/20260402_03_add_continuity_bibles.py).

The table stores a selected revision per session with:

- `revision_number`
- `source_stage`
- `source_summary`
- `summary_text`
- `summary_data`
- `is_selected`

### Repository and hydration support

- Extended [backend/app/repositories/sessions.py](/Users/kevin/code/storyteller/backend/app/repositories/sessions.py) so session aggregates now load the selected continuity bible.
- Extended [backend/app/models/session.py](/Users/kevin/code/storyteller/backend/app/models/session.py) and [backend/app/services/session_hydration.py](/Users/kevin/code/storyteller/backend/app/services/session_hydration.py) so hydrated session snapshots now expose `continuity_bible`.
- Extended [backend/app/services/agent_context.py](/Users/kevin/code/storyteller/backend/app/services/agent_context.py) so the agent context summary now includes the current continuity summary and open continuity threads.

### Continuity synthesis service

- Added [backend/app/services/continuity.py](/Users/kevin/code/storyteller/backend/app/services/continuity.py).

This service is the core implementation. It:

- reads accepted planning state from the session aggregate
- derives concise facts for characters, locations, objects, promises, voice constraints, unresolved threads, and locked composition details
- ignores non-canonical downstream state by requiring stages to be `IN_PROGRESS` or `COMPLETED`
- version-controls continuity revisions and keeps only one selected revision
- emits a compact prompt-facing payload through `build_continuity_payload(...)`

### Update hooks and prompt-context propagation

- Added continuity refresh hooks to accepted planning changes in [backend/app/services/sessions.py](/Users/kevin/code/storyteller/backend/app/services/sessions.py):
  - genre selection
  - tone selection
  - story brief save
  - pitch refinement/selection
  - character sheet refinement/selection
  - beat-sheet refinement/selection
- Added continuity refresh hooks to story-setup and outline updates in [backend/app/services/story_tools.py](/Users/kevin/code/storyteller/backend/app/services/story_tools.py).
- Composition and rewrite jobs now copy the selected continuity payload into both job metadata and the first queued segment payload so later model calls can use it directly.

### Workspace inspector

- Added API types in [frontend/src/api/sessions.ts](/Users/kevin/code/storyteller/frontend/src/api/sessions.ts).
- Added grouped continuity rendering in [frontend/src/pages/session/SessionWorkspacePage.tsx](/Users/kevin/code/storyteller/frontend/src/pages/session/SessionWorkspacePage.tsx).
- Added inspector styling in [frontend/src/styles/index.css](/Users/kevin/code/storyteller/frontend/src/styles/index.css).
- Added render coverage in [frontend/src/pages/session/SessionWorkspacePage.test.tsx](/Users/kevin/code/storyteller/frontend/src/pages/session/SessionWorkspacePage.test.tsx).

The inspector groups facts into:

- Characters
- Locations
- Objects
- Promises
- Voice guardrails
- Open threads
- Locked details

## New abstractions and extension points

### 1. Refreshing continuity after a durable decision

Use `SessionContinuityService.refresh_for_session(...)` after an accepted plan change or a composition checkpoint:

```python
from app.models import WorkflowStage
from app.services.continuity import SessionContinuityService

continuity = SessionContinuityService(session).refresh_for_session(
    session_id,
    source_stage=WorkflowStage.BEATS,
    source_summary="Accepted beat sheet.",
)
```

What this gives you:

- no-op behavior when the fact set did not change
- automatic revision bumping when it did change
- a selected continuity row that hydration can expose immediately

### 2. Seeding prompt-facing composition and rewrite context

Use `build_continuity_payload(...)` when building job metadata:

```python
from app.services.continuity import build_continuity_payload

continuity_payload = build_continuity_payload(continuity)

job.metadata_json = {
    **existing_metadata,
    **continuity_payload,
}
segment.payload = {
    **existing_payload,
    **continuity_payload,
}
```

The payload currently includes:

- `continuity_bible_id`
- `continuity_revision_number`
- `continuity_summary`
- `continuity_facts`

### 3. Inspecting continuity from the hydrated workspace

Frontend consumers can now read `snapshot.continuity_bible` directly:

```ts
if (snapshot.continuity_bible) {
  console.log(snapshot.continuity_bible.summary_text)
  console.log(snapshot.continuity_bible.facts)
}
```

This is the intended extension point for:

- prompt debugging
- future manual fact editing
- future continuity diff tooling
- future rewrite-policy inspection

## Exact verification work performed

### Backend verification

Commands run:

- `python -m ruff check backend/app/db/__init__.py backend/app/services/continuity.py backend/app/services/sessions.py backend/tests/test_continuity_service.py backend/tests/test_continuity_evals.py backend/tests/test_story_tools.py backend/tests/test_migrations.py backend/tests/test_db_models.py backend/tests/test_session_service.py backend/tests/test_session_hydration_service.py`
- `python -m pytest backend/tests/test_continuity_service.py backend/tests/test_continuity_evals.py backend/tests/test_story_tools.py backend/tests/test_migrations.py backend/tests/test_db_models.py backend/tests/test_session_service.py backend/tests/test_session_hydration_service.py -q`

Results:

- targeted ruff: pass
- targeted pytest: `51 passed`

Coverage added or expanded:

- migration coverage for `continuity_bibles`
- schema/index/foreign-key coverage for `continuity_bibles`
- hydration coverage for `snapshot.continuity_bible`
- session-service integration coverage for brief and character-sheet continuity refresh
- story-tool coverage for continuity payload propagation into composition metadata
- dedicated continuity-service unit coverage
- dedicated continuity prompt-eval coverage

### Frontend verification

Commands run:

- `npm --prefix frontend test -- --run src/pages/session/SessionWorkspacePage.test.tsx`
- `npm --prefix frontend run lint`
- `npm --prefix frontend run build`

Results:

- targeted Vitest run: `1 passed`, `32 passed`
- frontend lint: pass
- frontend production build: pass

Build note:

- Vite emitted the existing chunk-size warning for the main bundle after build. It did not fail the build.

### Browser and visual verification

Commands run:

- `docker compose -f infra/compose/docker-compose.yml up -d --build`
- `docker compose -f infra/compose/docker-compose.yml ps`
- `docker compose -f infra/compose/docker-compose.yml exec -T backend alembic upgrade head`
- `docker compose -f infra/compose/docker-compose.yml run --rm browser npm run check -- --spec /workspace/.artifacts/webapp-qa/continuity-inspector.spec.json`

Additional QA setup:

- I seeded a deterministic review session directly in the dev Postgres instance from the backend container because the live local database did not already contain a continuity-ready session.
- Seeded session id used for browser QA: `28a6a795-edb8-494a-8abe-6d6cebe84abd`

What I verified in the browser:

- the workspace route loaded successfully
- the continuity inspector rendered
- the continuity summary rendered
- the provenance line rendered
- the `Open threads` group rendered
- the `Midpoint reveal` fact rendered
- the inspector screenshot showed the section on the actual page, not only in DOM assertions

Artifacts:

- browser spec: [.artifacts/webapp-qa/continuity-inspector.spec.json](/Users/kevin/code/storyteller/.artifacts/webapp-qa/continuity-inspector.spec.json)
- screenshot: [.artifacts/webapp-qa/continuity-inspector.png](/Users/kevin/code/storyteller/.artifacts/webapp-qa/continuity-inspector.png)

Visual verification limits:

- I verified one desktop viewport (`1440x1400`).
- I did not run a second mobile-specific browser pass because this change is primarily a new summary panel inside an already responsive grid, and the targeted unit/build coverage plus desktop screenshot were sufficient for this prompt.

## Evaluation suite added for LLM- and prompt-facing behavior

I added [backend/tests/test_continuity_evals.py](/Users/kevin/code/storyteller/backend/tests/test_continuity_evals.py) and expanded the existing composition-payload eval coverage in [backend/tests/test_story_tools.py](/Users/kevin/code/storyteller/backend/tests/test_story_tools.py).

Named criteria and outcomes:

- `test_eval_continuity_payload_prioritizes_canonical_facts_for_prompt_context`: PASS
  - verified that the payload summary exists
  - verified that canonical categories are present
  - verified that category caps stay bounded (`voice_constraint <= 8`, `object <= 6`, `unresolved_thread <= 5`)
- `test_eval_continuity_payload_excludes_invalidated_downstream_facts_for_rewrites`: PASS
  - verified that `beats` and `story_setup` sourced facts are removed after downstream invalidation
  - verified that locked composition details still remain available for rewrite context
- `test_eval_composition_payload_inherits_outline_metadata_and_drafting_brief`: PASS
  - expanded to verify that continuity revision and continuity facts are present in the composition job and queued segment payloads

## Wrong turns, dead ends, and gotchas

- My first `docker compose up -d --build` attempt failed because this repo keeps the compose file at [infra/compose/docker-compose.yml](/Users/kevin/code/storyteller/infra/compose/docker-compose.yml), not at repo root.
- The live dev Postgres instance was behind the new migration. The first browser-QA seeding attempt failed with `relation "continuity_bibles" does not exist` until I ran `alembic upgrade head` in the backend container.
- I initially used `npm --prefix frontend lint` and `npm --prefix frontend build`; this repo expects `npm --prefix frontend run lint` and `npm --prefix frontend run build`.
- A repo-wide `ruff check backend/app backend/tests` still reports unrelated pre-existing issues outside this prompt. I narrowed lint verification to the files touched by prompt 55 and fixed all findings there.

## Assumptions I made while working unsupervised

- Canonical continuity should only use state from stages marked `IN_PROGRESS` or `COMPLETED`; `DRAFT` and `NEEDS_REGENERATION` state should not be treated as canon.
- Locked completed composition segments are still useful continuity inputs even when later planning changes invalidate other downstream planning artifacts.
- The optional inspector belongs in the workspace overview area instead of a separate debug page because the prompt asked for inspectability without making continuity tracking feel like extra process overhead.
- Seeding one QA session directly in the dev database for browser verification is acceptable in this local-first prompt workflow.

## Final reviewer notes

The change set is production-shaped rather than prompt-demo shaped:

- the continuity record is durable
- it is selected/versioned
- it is visible in hydration and UI
- it is wired into composition/rewrite context
- it has dedicated regression tests and prompt-facing evals

The working tree after the feature commits is clean except for YoloPilot automation log/status files outside the feature itself.
