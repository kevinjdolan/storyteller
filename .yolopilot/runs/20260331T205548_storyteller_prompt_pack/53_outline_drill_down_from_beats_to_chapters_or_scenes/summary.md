# Prompt 53: Outline Drill-Down From Beats to Chapters or Scenes

## What Changed and Why

This prompt adds a durable bridge between the accepted beat sheet and actual draftable writing segments.

I implemented the feature in three checkpoint commits:

- `d067b8f` `feat(prompt-53): backend story outline planning`
- `0977e25` `feat(prompt-53): outline workspace editor`
- `7dc8b20` `test(prompt-53): add outline drill-down evals`

The resulting behavior is:

- saving story setup targets now produces a structured chapter-or-scene outline from the selected beat sheet
- the outline is stored durably as revisioned data, not transient UI state
- composition jobs inherit outline card metadata and drafting briefs so the writing engine has a concrete segment plan
- the story setup stage now shows the draftable outline, card-level beat coverage, emotional shifts, and an editor for revising card copy without breaking the accepted beat sheet

The main reason for this shape is practical execution. The product now has a real, persisted planning artifact between high-level Save-the-Cat beats and segment-by-segment composition.

## Architectural Changes

### Backend domain and persistence

I added a first-class `story_outlines` persistence model and migration.

- New SQLAlchemy model: `backend/app/db/models.py`
- New Alembic migration: `backend/migrations/versions/20260402_02_add_story_outlines.py`
- New typed outline models: `backend/app/models/story_outline.py`

The table stores:

- the session, beat sheet, and story setup it was derived from
- revision number and selected revision state
- outline kind: `chapter` or `scene`
- outline summary
- structured card payloads
- metadata copied from story setup and lane context

This keeps outline state editable and revisioned instead of flattening it into an opaque JSON blob on the setup record.

### Outline generation service

I added `StoryOutlineGenerationService` in `backend/app/services/outline_generation.py`.

It takes a `StoryOutlinePlanningContext` and deterministically produces a `StoryOutlinePlan`:

- groups ordered Save-the-Cat beats into chapter or scene cards
- derives per-card word/runtime/scene targets from saved setup heuristics
- carries tone and genre direction into each card
- derives bedtime guardrails from beat-level softening notes
- produces a drafting brief for composition

The service is deterministic by design so it is stable under tests and safe to call from backend-owned policy logic.

### Session hydration and API

Session snapshots and hydrations now include outline revisions and the selected outline:

- `SessionSnapshot.story_outline_revisions`
- `SessionSnapshot.selected_story_outline`

API additions:

- `POST /api/v1/sessions/{session_id}/story-outline`

Story setup save behavior also changed:

- `POST /api/v1/sessions/{session_id}/story-setup` now auto-materializes an outline revision for the current selected beat sheet and setup targets

### Story tool orchestration

`StoryWorkflowToolService` now owns outline lifecycle work:

- auto-create outline revisions on story setup saves
- create new outline revisions on outline edits
- cancel invalidated composition/audio jobs when the outline materially changes
- inject outline card metadata into composition job and segment payloads

That means the durable planning funnel is now:

`beat_sheet -> story_setup -> story_outline -> composition segment plan`

### Frontend workspace

The story setup stage now exposes the new planning layer directly:

- a “Draftable outline” panel with revision summary, beat coverage, and planner carry-through
- a chapter/scene card rail showing beat support, emotional shift, tone direction, bedtime guardrail, and drafting brief
- an “Outline editor” panel for revising card title, summary, emotional shift, and drafting brief
- updated next-step copy so composition is only presented as ready when an outline exists

Frontend wiring changes:

- new outline types and save API in `frontend/src/api/sessions.ts`
- workspace save handler in `frontend/src/pages/session/SessionWorkspacePage.tsx`
- stage UI in `frontend/src/features/session/StorySetupStage.tsx`
- chat hydration message in `frontend/src/features/session/chat/sessionChat.ts`

## Key Files Touched

Backend:

- `backend/app/models/story_outline.py`
- `backend/app/db/models.py`
- `backend/app/models/session.py`
- `backend/app/models/events.py`
- `backend/app/models/story_tools.py`
- `backend/app/repositories/sessions.py`
- `backend/app/services/outline_generation.py`
- `backend/app/services/session_hydration.py`
- `backend/app/services/story_tools.py`
- `backend/app/services/conversation_memory.py`
- `backend/app/services/agent_context.py`
- `backend/app/api/v1/routes/sessions.py`
- `backend/migrations/versions/20260402_02_add_story_outlines.py`

Frontend:

- `frontend/src/api/sessions.ts`
- `frontend/src/features/session/StorySetupStage.tsx`
- `frontend/src/features/session/chat/sessionChat.ts`
- `frontend/src/pages/session/SessionWorkspacePage.tsx`
- `frontend/src/styles/index.css`

Tests:

- `backend/tests/test_outline_generation_service.py`
- `backend/tests/test_story_tools.py`
- `backend/tests/test_session_api.py`
- `backend/tests/test_migrations.py`
- `backend/tests/test_db_models.py`
- `frontend/src/features/session/StorySetupStage.test.tsx`
- `frontend/src/pages/session/SessionWorkspacePage.test.tsx`

## How To Use the New Abstractions

### 1. Generate an outline from saved setup heuristics

The main extension point is the planner service:

```python
from app.models.story_outline import StoryOutlinePlanningContext
from app.services.outline_generation import StoryOutlineGenerationService

plan = StoryOutlineGenerationService().generate_outline(
    StoryOutlinePlanningContext(
        genre_label="Quest Fantasy",
        tone_label="Hushed Wonder",
        beat_sheet_summary="A harbor quest that settles into calm belonging.",
        beats=beat_inputs,
        target_word_count=1800,
        target_runtime_minutes=14,
        chapter_count=4,
        approximate_scene_count=10,
        guidance_notes="Keep each chapter ending calmer than it began.",
    )
)
```

This returns a `StoryOutlinePlan` with:

- `outline_kind`
- `summary`
- revision-ready `cards`
- metadata suitable for persistence

### 2. Save an edited outline revision through the API

The backend edit path is revisioned, not in-place mutation.

```json
POST /api/v1/sessions/<session-id>/story-outline
{
  "outline_id": "71375dfe-5bd9-4d17-aba0-78c64e24740b",
  "summary": "4 draftable chapters mapped from the accepted beat sheet.",
  "cards": [
    {
      "card_key": "chapter-1",
      "card_type": "chapter",
      "position": 1,
      "title": "Chapter 1: Lantern Wake and Gentle Departure",
      "summary": "Open with a calmer harbor image, then send Mira after the drifting bell.",
      "beat_keys": ["opening_image", "catalyst"],
      "beat_labels": ["Opening Image", "Catalyst"],
      "emotional_shift": "Move from stillness toward gentle motion.",
      "target_word_count": 720,
      "target_runtime_minutes": 5,
      "target_scene_count": 4,
      "tone_direction": "Stay anchored in the Hushed Wonder tone while advancing the Quest Fantasy lane.",
      "bedtime_guardrail": "Keep the problem small, visible, and quickly reassuring.",
      "drafting_brief": "Chapter 1 should move from harbor stillness into a visibly safe departure."
    }
  ],
  "origin": "workspace"
}
```

This creates a new outline revision and refreshes downstream production state.

### 3. Wire the UI save callback

The frontend stage now expects an outline save handler:

```ts
<StorySetupStage
  onPreviewStage={setPreviewStage}
  onSaveStorySetup={applyStorySetupSave}
  onSaveStoryOutline={applyStoryOutlineSave}
  selectedStage={selectedStage}
  snapshot={snapshot}
/>
```

That handler ultimately calls `saveSessionStoryOutline()` in `frontend/src/api/sessions.ts`.

### 4. Extend composition planning later

The safest place to extend outline-driven composition behavior is the metadata bundle created in `backend/app/services/story_tools.py`.

The composition job and segment payload already receive:

- `story_outline_id`
- `outline_card_key`
- `outline_card_position`
- `outline_card_title`
- `outline_card_summary`
- `outline_card_drafting_brief`
- `outline_card_beat_keys`
- `outline_card_emotional_shift`

That gives later prompts a clean place to add richer prompt assembly without changing the session API shape again.

## Verification

### Backend tests

Initial targeted backend verification during implementation:

- `pytest backend/tests/test_outline_generation_service.py backend/tests/test_story_tools.py backend/tests/test_session_api.py backend/tests/test_migrations.py backend/tests/test_db_models.py -q`
- Result: `49 passed`

Final targeted verification for the new eval suite:

- `pytest backend/tests/test_outline_generation_service.py backend/tests/test_story_tools.py -q`
- Result: `17 passed`

Final full backend regression:

- `pytest backend/tests -q`
- Result: `189 passed, 5 skipped`

### Frontend tests and build

Targeted frontend verification:

- `npm --prefix frontend test -- --run src/features/session/StorySetupStage.test.tsx src/pages/session/SessionWorkspacePage.test.tsx src/features/session/chat/actionEchoes.test.ts src/features/session/chat/chatCommands.test.ts`
- Result: `42 passed`

Full frontend regression:

- `npm --prefix frontend test`
- Result: `86 tests passed`

Frontend lint:

- `npm --prefix frontend run lint`
- Result: passed

Frontend production build:

- `npm --prefix frontend run build`
- Result: passed

Note: Vite still emits the existing chunk-size warning for the main bundle. It did not block the build and was unrelated to this prompt.

### Python lint

- `ruff check backend/tests/test_outline_generation_service.py backend/tests/test_story_tools.py`
- Result: passed

### Browser-based UI verification

I used the running Docker Compose app and browser container rather than a separate local server.

Environment checks and prep:

- `docker compose -f infra/compose/docker-compose.yml ps --format json`
- `docker compose -f infra/compose/docker-compose.yml exec -T backend alembic upgrade head`

Why the migration command was necessary:

- the compose Postgres volume was behind the new `story_outlines` migration
- session snapshot and hydration requests were failing with `relation "story_outlines" does not exist`
- after migration, `GET /api/v1/sessions/<id>` and hydrate succeeded

Live browser verification route:

- `http://frontend:8566/sessions/8155bbd7-2de7-4d4c-a961-d35485225ed0?stage=story_setup`

Live browser checks performed:

- verified the story setup stage rendered the new “Draftable outline” panel
- verified “4 cards ready” summary text appeared
- verified “Outline editor” rendered with editable fields
- edited the first card title in-browser and saved it
- verified the UI advanced to `Revision 2`
- verified the saved title persisted through the API
- verified mobile rendering for the outline panel

API confirmation after live save:

- selected outline revision became `2`
- selected outline retained `4` cards
- first card title persisted as `Chapter 1: Lantern Wake and Gentle Departure`

Screenshot artifacts captured:

- `/Users/kevin/code/storyteller/.artifacts/webapp-qa/prompt-53-outline-desktop-before.png`
- `/Users/kevin/code/storyteller/.artifacts/webapp-qa/prompt-53-outline-desktop-after-save.png`
- `/Users/kevin/code/storyteller/.artifacts/webapp-qa/prompt-53-outline-mobile.png`
- `/Users/kevin/code/storyteller/.artifacts/webapp-qa/prompt-53-outline-panel-desktop.png`
- `/Users/kevin/code/storyteller/.artifacts/webapp-qa/prompt-53-outline-editor-panel-desktop.png`
- `/Users/kevin/code/storyteller/.artifacts/webapp-qa/prompt-53-outline-panel-mobile.png`

Screenshot quality note:

- the full-page captures proved the end-to-end flow worked but were too compressed to be reviewer-friendly
- I recaptured focused panel-level artifacts afterward; those are the ones worth opening first

### Remaining verification limits

- I verified one real compose-backed session and one mobile width, not an exhaustive breakpoint matrix
- I did not run a full browser automation sweep across every prior stage because this prompt changed only story setup and downstream composition metadata
- I applied the new migration to the existing compose database manually; I did not change the stack startup flow in this prompt

## LLM / Prompt-Facing Evaluation Suite

I did modify prompt-facing composition inputs by having composition inherit outline card briefs and metadata, so I added explicit deterministic eval coverage instead of relying only on broader service tests.

Named criteria and outcomes:

1. `outline_chapter_plan_preserves_targets_tone_and_guardrails`
- Source: `test_eval_outline_chapter_plan_preserves_targets_tone_and_guardrails`
- Outcome: Pass
- Checks:
  - chapter-mode planning selected
  - target word and runtime totals preserved exactly
  - tone direction present on every card
  - drafting brief present on every card
  - bedtime guardrails present on every card
  - low-point companionship guardrail survives into card output

2. `outline_scene_mode_uses_softened_beats_in_scene_cards`
- Source: `test_eval_outline_scene_mode_uses_softened_beats_in_scene_cards`
- Outcome: Pass
- Checks:
  - scene-mode fallback selected when no chapter count exists
  - each scene gets `target_scene_count == 1`
  - midpoint card preserves luminous reassurance note
  - all-is-lost card preserves visible-companionship note
  - drafting briefs continue to carry tone guidance

3. `composition_payload_inherits_outline_metadata_and_drafting_brief`
- Source: `test_eval_composition_payload_inherits_outline_metadata_and_drafting_brief`
- Outcome: Pass
- Checks:
  - composition job metadata includes selected outline id
  - segment payload includes card key, position, beat keys, and drafting brief
  - `planned_summary` defaults to the outline drafting brief

4. `outline_edit_revisions_keep_locked_structure_and_refresh_downstream`
- Source: `test_eval_outline_edit_revisions_keep_locked_structure_and_refresh_downstream`
- Outcome: Pass
- Checks:
  - editing creates a new revision instead of mutating in place
  - editable text fields change
  - locked structure fields like `beat_keys` and target sizing remain stable
  - composition and audio stages move to `needs_regeneration`

## Wrong Turns, Dead Ends, and Gotchas

### Compose database lagged behind migrations

The biggest surprise during live verification was not code logic. The compose-backed Postgres instance had not applied the new migration, which caused real session snapshot requests to 500 even though the test suite was green.

This showed up as:

- `relation "story_outlines" does not exist`

Resolution:

- ran `docker compose -f infra/compose/docker-compose.yml exec -T backend alembic upgrade head`

### Existing QA session predated the new outline table

After the migration, the existing compose session still had no outline because its story setup had been saved before the new table existed.

Resolution:

- re-saved story setup through the real API for that session
- that materialized the first outline revision
- then I exercised the in-browser outline edit flow against it

### Beat payload shape was not uniform

During backend implementation, I found that selected beat sheets are not always stored as a raw list. Some persisted rows store beats under a dict payload like `{"beats": [...]}`.

Resolution:

- `_build_outline_beat_inputs()` was updated to read both shapes

Without that change, outline generation would have silently failed or generated empty inputs for some existing data.

### Screenshot capture took two passes

My first browser captures were full-page and technically correct but not useful to review because the workspace is dense and tall.

Resolution:

- recaptured focused panel-level screenshots for the outline panel and editor

## Assumptions Made While Working Unsupervised

- Story setup should auto-generate or refresh an outline revision rather than introducing a separate “Generate outline” button in this prompt.
- `chapter_count` should force chapter-mode planning; otherwise the planner should fall back to scene-mode using `approximate_scene_count`.
- For this prompt, outline edits should stay scoped to editable drafting copy:
  - title
  - summary
  - emotional shift
  - drafting brief

I intentionally did not make beat coverage or target sizing editable yet because prompt 54 is explicitly about a chapter/scene card editor and likely broadens that surface.

- Composition should inherit outline card metadata and the drafting brief automatically when the user has not supplied a more specific rewrite or redirect instruction.
- Reusing an existing compose-backed QA session was acceptable for live verification in this unsupervised run.
- Harness-managed `.yolopilot` files are not part of the feature and should remain untouched in commits.

## Final State

The repository is left in a coherent state with three prompt-53 commits on the current branch and no tracked source changes left uncommitted outside the harness-owned `.yolopilot` run files.

Feature checkpoints:

- `d067b8f` backend outline planning and persistence
- `0977e25` frontend outline presentation and editor
- `7dc8b20` named deterministic eval coverage for outline-driven composition inputs
