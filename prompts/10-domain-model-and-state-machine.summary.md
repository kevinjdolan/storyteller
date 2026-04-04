# Prompt 10 Summary: Domain Model and Session State Machine

## What I changed and why

I defined the first concrete workflow contract for Storyteller so later backend services, database schema work, and frontend session UI can agree on the same stage identifiers and lifecycle rules instead of relying on prose scattered across the README and prompts.

The main deliverables are:

- `docs/domain-model.md`
  - Documents the durable session snapshot contract.
  - Defines the major business entities for sessions, planning records, composition, audio, assets, and the event log.
  - Defines the canonical ordered workflow stages.
  - Defines the lifecycle semantics for `draft`, `in_progress`, `completed`, and `needs_regeneration`.
  - Defines the safe backward-edit invalidation rules and the resume behavior.
  - Documents the mirrored backend/frontend constants plan.
- `backend/app/models/workflow.py`
  - Adds backend-owned workflow stage enums, lifecycle enums, per-stage metadata, invalidation helpers, and resume-stage resolution.
- `frontend/src/features/session/workflowStages.ts`
  - Adds the frontend mirror of the workflow-stage contract so the UI can render and reason about the same stage IDs and state semantics.
- `backend/tests/test_workflow.py`
  - Adds backend coverage for stage order, lifecycle-state identifiers, invalidation mapping, and resume-stage behavior.
- `frontend/src/features/session/workflowStages.test.ts`
  - Adds matching frontend coverage for the same contract.
- `frontend/src/features/home/HomeRoute.tsx`
  - Stops hard-coding the stage list and renders from the shared frontend workflow definition instead.
- `tools/webapp-qa/examples/homepage-workflow-contract.spec.json`
  - Adds a browser smoke spec that asserts the home route shows the workflow contract and captures a screenshot.

I also updated `docs/README.md` and `docs/architecture-overview.md` so the new domain model doc is discoverable from the existing architecture docs.

## Architectural changes across the codebase

### 1. Introduced a concrete workflow contract module in the backend

`backend/app/models/workflow.py` is now the backend-side source of truth for:

- workflow stage IDs
- stage lifecycle state IDs
- stage ordering
- stage metadata
- downstream invalidation rules after upstream edits
- resume-stage resolution

This gives later prompts a stable place to hang:

- database enums and stage-state rows
- service-layer transition validation
- websocket/realtime payload literals
- event-log stage context

### 2. Introduced a mirrored workflow contract module in the frontend

`frontend/src/features/session/workflowStages.ts` mirrors the backend literals so the UI can:

- render stage labels from stable IDs
- decide which stage to reopen when only stage-state data is available
- understand which later stages become stale after upstream edits

At this prompt stage I intentionally used mirrored constants rather than inventing a cross-language build/codegen layer. The repo does not yet have a shared package or schema generation path, and adding one here would have been premature complexity.

### 3. Made the home scaffold consume the contract

The home route now renders the workflow list from `workflowStageDefinitions` instead of a local string array. That is small, but it matters because it starts pushing the UI toward contract-driven stage rendering instead of copy drift.

### 4. Added explicit documentation for durable resume behavior

The new domain-model doc defines `resume_stage` as a backend-computed field, not something the frontend infers from random child data or last-opened tab state. That directly supports the acceptance requirement that an unfinished session can be resumed without guessing from UI state.

## New abstractions and how to use them

### Backend: resolve the correct resume stage

```python
from app.models import WorkflowStage, WorkflowStageState, resolve_resume_stage

resume_stage = resolve_resume_stage(
    {
        WorkflowStage.GENRE: WorkflowStageState.COMPLETED,
        WorkflowStage.TONE: WorkflowStageState.COMPLETED,
        WorkflowStage.BRIEF: WorkflowStageState.NEEDS_REGENERATION,
        WorkflowStage.PITCHES: WorkflowStageState.COMPLETED,
    }
)

assert resume_stage == WorkflowStage.BRIEF
```

Use this when later session services need to shape a resume snapshot for the UI.

### Backend: determine which stages become stale after an edit

```python
from app.models import WorkflowStage, get_invalidated_stages_after_edit

stale = get_invalidated_stages_after_edit(WorkflowStage.BEATS)

assert stale == (
    WorkflowStage.COMPOSITION,
    WorkflowStage.AUDIO,
    WorkflowStage.FINALIZE,
)
```

Use this in future service-layer transition code when accepting upstream edits.

### Frontend: render stage UI from canonical definitions

```ts
import { workflowStageDefinitions } from '../session/workflowStages.ts'

workflowStageDefinitions.map((stage) => stage.label)
```

The home route now uses exactly this pattern.

### Frontend: reopen the earliest incomplete stage

```ts
import { resolveResumeStage } from './workflowStages.ts'

const resumeStage = resolveResumeStage({
  genre: 'completed',
  tone: 'completed',
  brief: 'in_progress',
})

// resumeStage === 'brief'
```

## Exact verification work performed

### Focused backend verification

Command:

```bash
cd backend && .venv/bin/python -m pytest tests/test_workflow.py tests/test_health.py
```

Result:

- Passed.
- 8 tests passed.

Coverage of interest:

- canonical stage order
- canonical lifecycle-state IDs
- invalidation map behavior
- resume-stage behavior
- existing health endpoint behavior

### Focused frontend verification

Command:

```bash
npm --prefix frontend run test -- --run src/features/session/workflowStages.test.ts src/features/home/HomeRoute.test.tsx
```

Result:

- Passed.
- 2 test files passed.
- 5 tests passed.

Coverage of interest:

- canonical stage order
- canonical lifecycle-state IDs
- invalidation map behavior
- resume-stage behavior
- home route still renders correctly

### Broad repo verification

Command:

```bash
make check
```

Result:

- Passed.
- Frontend Prettier check passed.
- Backend Ruff format/lint passed.
- Backend pytest suite passed: 16 tests passed.
- Frontend Vitest suite passed: 5 tests passed.
- Frontend production build passed.

### Browser and visual verification

Commands:

```bash
make up
./scripts/dev-compose.sh up -d --no-deps frontend
./scripts/dev-compose.sh run --rm --no-deps browser npm run check -- --spec ./examples/homepage-workflow-contract.spec.json
```

Observed result:

- The dedicated browser QA spec passed.
- Screenshot saved to `.artifacts/webapp-qa/homepage-workflow-contract.png`.
- The screenshot shows the home route rendering the canonical stage list including `Story setup`.
- The browser spec also verified the frontend-only fallback text and offline badge.

Important verification limit:

- `make up` could not bring up the full backend-inclusive compose stack because the local `secrets.yaml` currently contains unsupported keys for the backend settings schema:
  - `gemini.api_key_name`
  - `gemini.project_name`
  - `gemini.project_number`
  - `openai`
- This failure existed in local runtime configuration, not in the new workflow-stage code.
- Because of that, browser QA was completed by starting the frontend service without backend dependencies and verifying the intended offline-safe rendering path.

## LLM or prompt evaluation suite

No LLM-facing logic, prompt assembly, model selection, or agent behavior was changed in this task.

Because of that:

- No prompt/LLM evaluation suite was added.
- No model-quality criteria were measured.
- This is intentional, not missing work.

## Wrong turns, dead ends, and surprising behavior

- I first tried targeted frontend Vitest filtering with repository-root-relative paths. Vitest expects paths relative to the frontend package root, so the initial command found no tests. I reran with `src/...` paths.
- I first tried backend pytest with the host `python3`, but the host interpreter did not have `pytest` installed. The repo already had `backend/.venv`, so I switched to that environment for the focused backend run.
- `make check` initially failed twice during cleanup:
  - first on frontend Prettier formatting for the new TS contract file
  - then on Ruff line-length violations in the new Python contract file
  - both were fixed before the final successful check
- The full compose startup failed because of the local `secrets.yaml` shape, which is unrelated to the prompt-10 code but materially affected browser-verification strategy.
- `docker compose run browser` tried to start backend dependencies again, so I had to switch to `--no-deps` to get browser QA running against the already-started standalone frontend container.

## Assumptions made while working unsupervised

- I treated `story_setup` preferences as persistent user intent rather than generated content, so upstream planning edits do not automatically invalidate the `story_setup` record itself. They still invalidate `composition`, `audio`, and `finalize`.
- I treated accepted choices like `selected_pitch_id` and `selected_character_sheet_id` as pointers on `story_session` rather than separate selection tables. The event log still preserves change history.
- I introduced `workflow_stage_state` as an explicit durable concept in the docs even though the prompt list did not name it directly, because resume behavior and stale-stage handling are much cleaner if each stage has its own tracked state row.
- I added `composition_job` to the entity model even though the prompt build list called out `composition_segment` rather than the parent job. A durable segment model without a parent job record would make later worker orchestration awkward.
- I assumed mirrored backend/frontend constants are the right level of rigor for prompt 10. A generated shared schema package would be better later if the contract grows, but it would be overbuilt for the current repo state.

## Files touched

- `backend/app/models/__init__.py`
- `backend/app/models/workflow.py`
- `backend/tests/test_workflow.py`
- `docs/README.md`
- `docs/architecture-overview.md`
- `docs/domain-model.md`
- `frontend/src/features/home/HomeRoute.tsx`
- `frontend/src/features/session/workflowStages.ts`
- `frontend/src/features/session/workflowStages.test.ts`
- `tools/webapp-qa/examples/homepage-workflow-contract.spec.json`
