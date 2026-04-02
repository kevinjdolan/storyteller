# Prompt 48 Summary: Save-the-Cat Beat Sheet Generation

## What I changed and why

I completed prompt 48 end to end by adding durable Save-the-Cat beat-sheet generation on the backend and a real beat-sheet workflow stage in the frontend workspace.

The backend now generates a structured, revisioned beat sheet from the accepted pitch and character sheet, persists it as a structured artifact, supports refinement and selection, and exposes the new behavior through session APIs. The beat sheet is explicit, high level, bedtime-adapted, and shaped to feed later composition work without turning into prose too early.

The frontend now has a dedicated beat-sheet stage instead of the old generic placeholder. The stage can:

- generate a new beat-sheet revision
- refine an existing beat-sheet revision
- accept a revision and advance to story setup
- show the full 15-beat Save-the-Cat outline with summary, emotional intent, and bedtime softening notes
- handle beat-sheet actions coming from chat as well as direct UI interactions

I also verified the new stage visually against the live Docker Compose app on both desktop and mobile viewports.

Two implementation commits were created during development:

- `790de93` `feat(prompt-48): add beat sheet generation backend`
- `51300fc` `feat(prompt-48): add beat sheet workspace UI`

## Architectural changes across the codebase

### Backend

I added a dedicated beat-sheet domain model and service path instead of hiding beat data in opaque JSON blobs.

Key backend changes:

- `backend/app/models/beat_sheet_generation.py`
  Added typed generation inputs/outputs for Save-the-Cat beat generation.
- `backend/app/ai/beat_sheet_generation.py`
  Added the Gemini-facing adapter and fallback/evaluation logic for beat-sheet generation.
- `backend/app/ai/prompts/beat_sheet_generation.md`
  Added the planning prompt used to generate bedtime-adapted Save-the-Cat beats.
- `backend/app/services/beat_sheet_generation.py`
  Added orchestration that turns pitch + character context into a structured beat-sheet result.
- `backend/app/services/sessions.py`
  Added session-level generation, refinement, and selection flows for beat sheets, including stage invalidation behavior.
- `backend/app/services/session_hydration.py`
  Added hydration support so stored beat sheets come back as typed `BeatSheetView` objects instead of raw payloads.
- `backend/app/repositories/sessions.py`
  Added repository support for loading beat-sheet revisions and the selected beat sheet.
- `backend/app/api/v1/routes/sessions.py`
  Added:
  - `POST /api/v1/sessions/{session_id}/beats/generate`
  - `POST /api/v1/sessions/{session_id}/beats/refine`
  - `POST /api/v1/sessions/{session_id}/selections/beat-sheet`

The beat sheet reuses the existing `BeatSheet.beats` JSON column, so no migration was required. The persisted payload now stores:

- generation metadata
- bedtime goal
- focus beats
- generation/refinement lineage
- the full ordered beat list

Each beat entry is structured as:

- `key`
- `label`
- `order`
- `summary`
- `emotional_intent`
- `bedtime_softening_note`

The canonical 15 beats are:

- `opening_image`
- `theme_stated`
- `set_up`
- `catalyst`
- `debate`
- `break_into_two`
- `b_story`
- `fun_and_games`
- `midpoint`
- `bad_guys_close_in`
- `all_is_lost`
- `dark_night_of_the_soul`
- `break_into_three`
- `finale`
- `final_image`

### Frontend

The frontend stage shell now treats beats like pitches and character sheets: revisioned, selectable, previewable, and chat-addressable.

Key frontend changes:

- `frontend/src/api/sessions.ts`
  Expanded the beat-sheet API contract to include:
  - `BeatSheetBeatView`
  - richer `BeatSheetView`
  - `beat_sheet_revisions` on `SessionSnapshot`
  - request/response types for generate/refine/select beat-sheet actions
  - API helpers:
    - `generateSessionBeatSheet`
    - `refineSessionBeatSheet`
    - `selectSessionBeatSheet`
- `frontend/src/features/session/BeatSheetStage.tsx`
  New dedicated beat-sheet stage UI.
- `frontend/src/pages/session/SessionWorkspacePage.tsx`
  Wired the stage into the main workspace, added chat action support, and added frontend action dispatchers for generate/refine/select flows.
- `frontend/src/pages/session/SessionWorkspacePage.test.tsx`
  Added/updated workspace integration coverage for the beat-sheet stage and chat-driven beat actions.
- `frontend/src/styles/index.css`
  Added beat-stage layout and outline-preview styling.

The beat-sheet stage replaced the old placeholder scaffolding for the `beats` stage. That changed one subtle behavior: the generic stage-note editor is no longer shown on the beat stage because the stage now has dedicated controls. The generic stage-note tests were moved to `story_setup`, which still uses the placeholder note editor path.

## Examples: new abstractions, helpers, and extension points

### Backend API usage

Generate a beat sheet:

```http
POST /api/v1/sessions/{session_id}/beats/generate
Content-Type: application/json

{
  "guidance": "Keep the midpoint more awestruck than tense.",
  "focus_beats": ["midpoint"],
  "bedtime_goal": "Land in a visibly sleepy ending.",
  "origin": "workspace"
}
```

Refine a beat sheet:

```http
POST /api/v1/sessions/{session_id}/beats/refine
Content-Type: application/json

{
  "beat_sheet_id": "<existing_revision_id>",
  "instructions": "Soften the midpoint and all-is-lost beats.",
  "beat_names": ["midpoint", "all_is_lost"],
  "bedtime_goal": "End on a very sleepy exhale.",
  "origin": "workspace"
}
```

Accept a beat sheet:

```http
POST /api/v1/sessions/{session_id}/selections/beat-sheet
Content-Type: application/json

{
  "beat_sheet_id": "<revision_id>",
  "origin": "workspace"
}
```

### Frontend API helper usage

The new frontend API helpers follow the same session mutation pattern as pitches and character sheets:

```ts
await generateSessionBeatSheet(sessionId, {
  guidance: 'Keep the midpoint more awestruck than tense.',
  focus_beats: ['midpoint'],
  bedtime_goal: 'Land in a visibly sleepy ending.',
  origin: 'workspace',
})

await refineSessionBeatSheet(sessionId, {
  beat_sheet_id: selectedBeatSheet.id,
  revision_number: selectedBeatSheet.revision_number,
  instructions: 'Soften the midpoint and all-is-lost beats.',
  beat_names: ['midpoint', 'all_is_lost'],
  bedtime_goal: 'End on a very sleepy exhale.',
  origin: 'workspace',
})

await selectSessionBeatSheet(sessionId, {
  beat_sheet_id: selectedBeatSheet.id,
  revision_number: selectedBeatSheet.revision_number,
  origin: 'workspace',
})
```

### Frontend stage integration

`BeatSheetStage` is now the extension point for future beat-level editing or richer comparison behavior. It already accepts the three core workspace actions as props:

```tsx
<BeatSheetStage
  onGenerateBeatSheet={applyBeatSheetGeneration}
  onPreviewStage={setPreviewStage}
  onRefineBeatSheet={applyBeatSheetRefinement}
  onSelectBeatSheet={applyBeatSheetSelection}
  selectedStage={selectedStage}
  snapshot={snapshot}
/>
```

This keeps the stage UI isolated from transport concerns while the workspace page remains the orchestration layer for runtime hydration, chat echo handling, and route-stage sync.

## Verification

### Backend verification

I ran targeted backend tests after the backend implementation commit:

```bash
pytest backend/tests/test_beat_sheet_generation_service.py \
       backend/tests/test_session_beat_sheet_service.py \
       backend/tests/test_session_api.py -q
```

Result:

- `38 passed in 2.75s`

### Frontend verification

I ran the beat-stage workspace tests directly:

```bash
cd frontend
npm test -- --run src/pages/session/SessionWorkspacePage.test.tsx
```

Result:

- `28 passed`

I then ran the full frontend test suite:

```bash
cd frontend
npm test
```

Result:

- `14 files passed`
- `75 tests passed`

I ran lint:

```bash
cd frontend
npm run lint
```

Result:

- passed

I ran a production build:

```bash
cd frontend
npm run build
```

Result:

- passed

I also checked formatting:

```bash
cd frontend
npm run format:check
```

Result:

- failed, but only on preexisting unrelated files:
  - `src/features/session/CharacterSelectionStage.tsx`
  - `src/features/session/chat/actionEchoes.test.ts`
  - `src/features/session/chat/chatToUiActions.test.ts`

I formatted the files I changed, but I did not churn those unrelated existing files.

### Browser and visual verification

I used the `webapp-qa` Docker Compose flow and the bundled Puppeteer runner.

Desktop browser check:

```bash
docker compose -f infra/compose/docker-compose.yml run --rm browser \
  npm run check -- --spec /workspace/.artifacts/webapp-qa/beat-stage.spec.json
```

Result:

- passed
- screenshot saved to `/Users/kevin/code/storyteller/.artifacts/webapp-qa/beat-stage.png`

Mobile browser check:

```bash
docker compose -f infra/compose/docker-compose.yml run --rm browser \
  npm run check -- --spec /workspace/.artifacts/webapp-qa/beat-stage-mobile.spec.json
```

Result:

- passed
- screenshot saved to `/Users/kevin/code/storyteller/.artifacts/webapp-qa/beat-stage-mobile.png`

What I visually verified from those screenshots:

- the beat stage renders as a dedicated stage, not the old placeholder shell
- the generation and refinement panels are visible and readable
- saved beat revisions are visible as cards
- the full beat outline preview is present and ordered
- the stage remains usable on a narrow mobile viewport with the content stacked vertically instead of overlapping

### Live-session QA setup used for the browser pass

To drive browser QA against a real session instead of mocks, I seeded one local session through the backend API up to the beat stage, then opened:

- `http://localhost:8566/sessions/28df1027-fc7f-435f-95a2-18de6ae3c5f3?stage=beats`

That session was used only for local verification.

## LLM and prompt evaluation suite

Because this prompt added LLM-facing beat-sheet generation behavior, I treated the backend service tests as the evaluation suite for the generation contract.

Named criteria asserted in `backend/tests/test_beat_sheet_generation_service.py`:

- `all_required_beats_present`: pass
- `beat_order_matches_framework`: pass
- `summaries_are_present_for_every_beat`: pass
- `emotional_intents_are_present_for_every_beat`: pass
- `bedtime_softening_notes_are_present_for_every_beat`: pass
- `tension_beats_include_extra_softening`: pass
- `overall_summary_and_bedtime_notes_are_present`: pass

Scenario coverage:

- `test_eval_structured_beat_sheet_happy_path_uses_adapter_output`
  - source: `gemini`
  - overall evaluation: pass
  - all seven criteria: pass
- `test_eval_fallback_resilience_uses_heuristics_when_adapter_fails`
  - source: `heuristic`
  - overall evaluation: pass
  - 15 beats produced
  - fallback reason captured: `simulated Gemini outage`
- `test_eval_validation_guardrail_falls_back_when_adapter_misses_required_beats`
  - source: `heuristic`
  - overall evaluation: pass
  - fallback reason includes failed adapter validation conditions
- `test_eval_refinement_fallback_keeps_source_revision_and_guidance_visible`
  - source: `heuristic`
  - refinement lineage and guidance preserved under fallback

This gives the change a concrete prompt/eval surface instead of leaving the beat prompt unverified.

## Wrong turns, dead ends, and gotchas

### 1. The compose rebuild surfaced a real local-config problem

The first live browser QA attempt failed because rebuilding the compose stack recreated the backend container, and the backend then refused to start. The cause was not the code I wrote for prompt 48; it was local `secrets.yaml` drift:

- unsupported `openai` block
- unsupported `gemini.api_key_name`
- unsupported `gemini.project_name`
- unsupported `gemini.project_number`

I fixed the local-only file by removing those unsupported keys so the stricter settings model would accept it again. I did not commit `secrets.yaml`.

### 2. The beat stage no longer exposes the generic stage-note editor

Existing workspace tests expected `Beat sheet note` because the beat stage used to be a placeholder stage. After adding a dedicated beat-sheet component, that generic note editor is intentionally gone for `beats`. I moved the generic stage-note pipeline checks to `story_setup`, which still exercises the same durable note-saving code path.

### 3. The first Vitest invocation used the wrong relative path

Running:

```bash
npm test -- --run frontend/src/pages/session/SessionWorkspacePage.test.tsx
```

from inside `frontend/` did not match any test files. The correct filter from that directory is:

```bash
npm test -- --run src/pages/session/SessionWorkspacePage.test.tsx
```

### 4. The frontend mock fixture needed cleanup once beats became real

After adding real `beat_sheet_revisions` and `selected_character_sheet` to the shared sample snapshot, earlier-stage mock responses started inheriting downstream state accidentally. I had to explicitly clear character/beat/story-setup fields in earlier stage builders so the staged integration tests stayed logically correct.

## Assumptions I made while working unsupervised

- It was acceptable to persist the richer beat-sheet structure inside the existing beat-sheet JSON payload instead of adding a new relational schema or migration.
- Beat focus inputs can remain free-form comma/newline text in the UI for now, because the backend already accepts beat names/keys and later prompts can harden that input if needed.
- Replacing the beat-stage placeholder with a dedicated component was the correct interpretation of “Beat-sheet stage UI,” even though it changed the old placeholder-based test shape.
- Updating local-only `secrets.yaml` to restore Docker Compose health for QA was acceptable because the file is explicitly local-only and is not part of the commit.

## Remaining limits

- `npm run format:check` still fails due unrelated preexisting files outside this prompt’s change scope.
- The beat stage currently treats focus-beat entry as free-form text rather than a richer multi-select UI.
- Browser QA covered the beats stage directly on desktop and mobile, but I did not add a second browser spec for the accept-to-story-setup transition because that flow is already covered in the workspace integration tests.
