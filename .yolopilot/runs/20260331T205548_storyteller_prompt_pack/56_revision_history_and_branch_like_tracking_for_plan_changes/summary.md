# Prompt 56: Revision History And Branch-Like Tracking For Plan Changes

Checkpoint commit on the working branch: `753f7a2` (`feat(prompt-56): revision history and branches`).

## What I changed and why

This prompt asked for a simple, understandable revision model so users can change planning decisions without feeling one click away from losing prior accepted work. I implemented that as durable session-level plan snapshots instead of a full branching system.

The core behavior change is:

- important planning artifacts now participate in a unified `plan_revisions` history
- the session knows which plan revision is current
- composition jobs explicitly point at the plan revision they were created from
- restoring an earlier plan does not overwrite history; it creates a new current revision that records where it was restored from
- the planning UI now exposes a lightweight history/compare/restore surface across the stages where users are still shaping the plan

This keeps the model understandable:

- revisions are linear, numbered snapshots
- each revision stores pointers to the selected `pitch`, `character_sheet`, `beat_sheet`, `story_setup`, and `story_outline`
- restore is additive, not destructive
- the composition lineage is visible in hydrated session state

## Architectural changes across the codebase

### Persistence and database model

I added a new `plan_revisions` table in [backend/migrations/versions/20260402_04_add_plan_revisions.py](/Users/kevin/code/storyteller/backend/migrations/versions/20260402_04_add_plan_revisions.py) and the corresponding ORM model in [backend/app/db/models.py](/Users/kevin/code/storyteller/backend/app/db/models.py).

Each `PlanRevision` row stores:

- `session_id`
- `revision_number`
- `source_stage`
- `change_summary`
- `restored_from_plan_revision_id`
- `pitch_id`
- `character_sheet_id`
- `beat_sheet_id`
- `story_setup_id`
- `story_outline_id`
- `is_current`

I also added `plan_revision_id` to `composition_jobs`, so composition can now say exactly which accepted plan snapshot it was based on instead of only implying lineage through loose metadata.

### Repository and hydration layer

The session aggregate in [backend/app/repositories/sessions.py](/Users/kevin/code/storyteller/backend/app/repositories/sessions.py) now loads:

- all `plan_revisions`
- the `current_plan_revision`
- `CompositionJob.plan_revision`

The snapshot/hydration layer in [backend/app/services/session_hydration.py](/Users/kevin/code/storyteller/backend/app/services/session_hydration.py) now builds:

- `PlanArtifactRefView`
- `PlanRevisionView`
- `snapshot.plan_revisions`
- `snapshot.current_plan_revision`
- composition lineage fields on `CompositionJobView`

The composition view contract in [backend/app/models/session.py](/Users/kevin/code/storyteller/backend/app/models/session.py) now exposes:

- `plan_revision_id`
- `plan_revision_number`
- `beat_sheet_revision_number`
- `story_setup_revision_number`
- `story_outline_revision_number`

That is what lets the UI say “composition is using plan revision X” instead of inferring it.

### Backend services

I added [backend/app/services/plan_revisions.py](/Users/kevin/code/storyteller/backend/app/services/plan_revisions.py), which centralizes the new revision behavior.

Important methods:

- `capture_current_state(...)`: snapshot the currently selected planning artifacts
- `ensure_current_revision(...)`: lazily create a first revision before composition if none exists yet
- `list_revisions(...)`
- `get_current_revision(...)`
- `get_revision_by_number(...)`

I then integrated that service into:

- [backend/app/services/sessions.py](/Users/kevin/code/storyteller/backend/app/services/sessions.py)
- [backend/app/services/story_tools.py](/Users/kevin/code/storyteller/backend/app/services/story_tools.py)

Key behavior changes in `SessionService`:

- selecting/refining a pitch captures a new plan revision
- selecting/refining a character sheet captures a new plan revision
- selecting/refining/editing a beat sheet captures a new plan revision
- restoring a revision reselects the referenced artifacts, updates stage state, cancels invalid downstream jobs, and creates a new current revision instead of mutating the old one
- beat-sheet editing is now revision-preserving rather than editing the selected revision in place

Key behavior changes in `StoryWorkflowToolService`:

- saving story setup or outline revisions captures a new current plan revision
- `compose_next_segment` and `rewrite_segments` call `ensure_current_revision(...)`
- new composition jobs store `plan_revision_id`

### API layer

I added a restore endpoint in [backend/app/api/v1/routes/sessions.py](/Users/kevin/code/storyteller/backend/app/api/v1/routes/sessions.py):

`POST /api/v1/sessions/{session_id}/plan-revisions/{revision_number}/restore`

Request body:

```json
{
  "origin": "workspace"
}
```

The event contract also gained `SelectionKind.PLAN_REVISION` in [backend/app/models/events.py](/Users/kevin/code/storyteller/backend/app/models/events.py), which lets chat/UI history explain restores clearly.

### Frontend and UX

I extended the session API types in [frontend/src/api/sessions.ts](/Users/kevin/code/storyteller/frontend/src/api/sessions.ts) so the client can read plan revisions and composition lineage and call the restore endpoint.

I added [frontend/src/features/session/PlanRevisionHistoryPanel.tsx](/Users/kevin/code/storyteller/frontend/src/features/session/PlanRevisionHistoryPanel.tsx), which renders:

- the current saved plan revision
- the artifact refs captured by that revision
- whether composition is aligned to the current revision
- earlier revisions
- a lightweight compare summary against the current revision
- a restore button for prior revisions

I mounted that panel in:

- [frontend/src/features/session/PitchSelectionStage.tsx](/Users/kevin/code/storyteller/frontend/src/features/session/PitchSelectionStage.tsx)
- [frontend/src/features/session/CharacterSelectionStage.tsx](/Users/kevin/code/storyteller/frontend/src/features/session/CharacterSelectionStage.tsx)
- [frontend/src/features/session/BeatSheetStage.tsx](/Users/kevin/code/storyteller/frontend/src/features/session/BeatSheetStage.tsx)
- [frontend/src/features/session/StorySetupStage.tsx](/Users/kevin/code/storyteller/frontend/src/features/session/StorySetupStage.tsx)

The page orchestration in [frontend/src/pages/session/SessionWorkspacePage.tsx](/Users/kevin/code/storyteller/frontend/src/pages/session/SessionWorkspacePage.tsx) now wires `applyPlanRevisionRestore(...)` through those stages.

I also updated [frontend/src/features/session/chat/actionEchoes.ts](/Users/kevin/code/storyteller/frontend/src/features/session/chat/actionEchoes.ts) so the transcript shows restore events as `Restored saved plan: ...`.

## Examples and extension points

### Capturing a revision after any future planning action

If a future prompt adds another editable planning artifact, the extension pattern is:

```python
from app.models import WorkflowStage
from app.services.plan_revisions import PlanRevisionService

PlanRevisionService(session).capture_current_state(
    session_id,
    source_stage=WorkflowStage.STORY_SETUP,
    change_summary="Accepted revised outline notes.",
)
```

That preserves the currently selected plan as one durable snapshot.

### Restoring a revision from backend code

```python
result = SessionService(session).restore_plan_revision(
    session_id,
    revision_number=1,
    origin="workspace",
)
```

The result returns:

- a refreshed snapshot
- a durable selection event with `selection_kind == "plan_revision"`
- a new current revision instead of reactivating revision 1 in place

### Reading composition lineage in the UI

The hydrated snapshot now includes:

```ts
snapshot.latest_composition_job?.plan_revision_number
snapshot.latest_composition_job?.story_outline_revision_number
snapshot.latest_composition_job?.beat_sheet_revision_number
snapshot.latest_composition_job?.story_setup_revision_number
```

That is the intended UI contract for any future “drafted from revision X” or “this draft is stale relative to plan revision Y” messaging.

### Lightweight compare behavior

The compare model is intentionally simple: a revision only says which top-level artifact refs differ from the current snapshot. It does not attempt beat-level or card-level structural diffing. That matches the prompt’s “simple revision model is enough” guidance.

## Exact verification work performed

### Targeted backend tests

Ran:

```bash
pytest backend/tests/test_story_tools.py backend/tests/test_session_service.py backend/tests/test_session_beat_sheet_service.py backend/tests/test_migrations.py -q
```

Result:

- `45 passed in 4.30s`

What this covered:

- plan revision restore behavior
- beat-sheet revision preservation
- composition job plan lineage
- migration creation/upgrade behavior

### Targeted frontend tests

Ran:

```bash
cd frontend
npm test -- StorySetupStage.test.tsx SessionWorkspacePage.test.tsx actionEchoes.test.ts
```

Result:

- `3 files, 43 tests passed`

What this covered:

- stage-level revision history rendering
- restore callback wiring from the workspace page
- chat/action-echo wording for restored plan revisions

### Additional backend API/hydration tests

Ran:

```bash
pytest backend/tests/test_session_api.py backend/tests/test_session_hydration_service.py -q
```

Result:

- `38 passed in 4.31s`

What this covered:

- API contract stability for session payloads
- workspace hydration behavior after snapshot changes

### Post-lint regression rerun

After fixing Ruff issues in the task-touched Python files, I reran:

```bash
pytest backend/tests/test_story_tools.py backend/tests/test_session_service.py backend/tests/test_session_beat_sheet_service.py backend/tests/test_migrations.py backend/tests/test_session_api.py backend/tests/test_session_hydration_service.py -q
```

Result:

- `83 passed in 7.90s`

### Frontend lint and build

Ran:

```bash
cd frontend
npm run lint && npm run build
```

Result:

- lint passed
- production build passed
- Vite emitted a chunk-size warning for the existing main bundle (`>500 kB` after minification), but the build completed successfully

### Focused backend lint on touched files

Ran:

```bash
cd backend
.venv/bin/python -m ruff check \
  app/api/v1/routes/sessions.py \
  app/db/__init__.py \
  app/models/__init__.py \
  app/repositories/sessions.py \
  app/services/plan_revisions.py \
  app/services/session_hydration.py \
  app/services/sessions.py \
  app/services/story_tools.py \
  tests/test_session_api.py \
  tests/test_session_beat_sheet_service.py \
  tests/test_session_service.py \
  tests/test_story_tools.py
```

Result:

- `All checks passed!`

### Browser / visual verification

I used the repo’s Docker Compose stack and browser container.

Commands and actions:

```bash
make up
./scripts/dev-compose.sh exec -T backend alembic upgrade head
```

I then seeded a real Postgres-backed session through the backend service layer with:

- title: `Revision History QA`
- two pitch candidates
- pitch revision 1 selected first
- pitch revision 2 selected second

After that, I verified in the live UI that clicking Restore on revision 1 changed the current saved plan back to the earlier pitch.

Artifacts:

- before screenshot: `.artifacts/webapp-qa/revision-history-before.png`
- after screenshot: `.artifacts/webapp-qa/revision-history-after.png`

The browser assertion checked the actual current-plan artifact label, not just generic page text:

- before restore: `Otter Bell Moonpath`
- after restore: `Lantern Harbor Promise`

I also verified the durable backend state after the click:

```bash
curl -sf http://localhost:8565/api/v1/sessions/16b30070-2006-457f-bcae-f9ca147cff40 | jq '{current_stage, selected_pitch: .selected_pitch.title, current_plan_revision: .current_plan_revision.revision_number, restored_from: .current_plan_revision.restored_from_revision_number, revisions: [.plan_revisions[].revision_number]}'
```

Observed result:

- `current_stage: "characters"`
- `selected_pitch: "Lantern Harbor Promise"`
- `current_plan_revision: 3`
- `restored_from: 1`
- `revisions: [3, 2, 1]`

### Verification limits

- I did not run the entire backend test suite, only the feature-adjacent and contract-adjacent suites.
- I did not add visual diff/snapshot automation to the repo itself; the browser verification used the existing QA container plus saved screenshots.
- I did not run full repo-wide Ruff formatting because the repository already has unrelated format drift in untouched files.

## LLM / prompt evaluation work

No new LLM evaluation suite was added.

Reason:

- this prompt did not change prompts, model routing, adapters, safety policies, or other LLM-facing logic
- the change is about durable revision tracking, restore semantics, and UI/contract exposure

So the LLM-eval requirement was not applicable for this task.

## Wrong turns, dead ends, and gotchas

### 1. Live compose DB was behind the code

The first attempt to seed a browser-verification session against the running stack failed with:

- `psycopg.errors.UndefinedTable: relation "plan_revisions" does not exist`

Cause:

- `make up` did not automatically migrate the existing local Postgres volume to the new schema

Resolution:

- I ran `./scripts/dev-compose.sh exec -T backend alembic upgrade head` before proceeding with live verification

### 2. The first browser smoke assertions were too loose

My first QA attempt used the generic JSON spec runner with plain text assertions like `Plan history` and `Revision 3`.

That failed for two reasons:

- the rendered page text is uppercased in places (`PLAN HISTORY`)
- unrelated parts of the page already contained other revision numbers, so those text assertions were not specific enough for restore verification

Resolution:

- I switched to selector-scoped Puppeteer assertions that read the current artifact label inside the plan-history panel before and after the click

### 3. Backend repo-wide formatting/lint is not clean at baseline

Running repo-wide backend checks exposed pre-existing Ruff formatting and lint issues in many untouched files.

Resolution:

- I cleaned and verified the Python files touched by this task
- I did not mass-reformat unrelated files, because that would create a noisy prompt-56 diff with low reviewer value

### 4. Beat-sheet edit preservation required a behavior correction

The earlier implementation path for beat-sheet edits still behaved too destructively for this prompt. I changed that flow so editing creates a new beat-sheet revision instead of mutating the selected row in place. That was necessary to make the revision model consistent rather than only partially preserved.

## Assumptions made while working unsupervised

- A linear revision history with restore provenance is sufficient for this prompt; I did not implement true branching or merge semantics.
- The right granularity is a session-level plan snapshot that references current selected artifacts, not independent branch trees per artifact.
- A lightweight compare summary based on changed top-level artifact refs is enough for now; deeper diff UIs would be follow-on work.
- It is acceptable for browser verification to use a manually seeded session in the live compose database when real AI-backed generation is not required to verify the feature.
- It is acceptable to run `alembic upgrade head` manually during verification because the running local Postgres volume was older than the new migration.

## Reviewer notes

The most important files to review first are:

- [backend/app/services/plan_revisions.py](/Users/kevin/code/storyteller/backend/app/services/plan_revisions.py)
- [backend/app/services/sessions.py](/Users/kevin/code/storyteller/backend/app/services/sessions.py)
- [backend/app/services/story_tools.py](/Users/kevin/code/storyteller/backend/app/services/story_tools.py)
- [backend/app/services/session_hydration.py](/Users/kevin/code/storyteller/backend/app/services/session_hydration.py)
- [backend/migrations/versions/20260402_04_add_plan_revisions.py](/Users/kevin/code/storyteller/backend/migrations/versions/20260402_04_add_plan_revisions.py)
- [frontend/src/features/session/PlanRevisionHistoryPanel.tsx](/Users/kevin/code/storyteller/frontend/src/features/session/PlanRevisionHistoryPanel.tsx)
- [frontend/src/pages/session/SessionWorkspacePage.tsx](/Users/kevin/code/storyteller/frontend/src/pages/session/SessionWorkspacePage.tsx)

Those files contain the core persistence, restore semantics, hydration contract, and UI exposure for the new revision-history model.
