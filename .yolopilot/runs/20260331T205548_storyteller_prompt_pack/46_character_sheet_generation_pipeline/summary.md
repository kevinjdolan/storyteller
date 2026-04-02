# Prompt 46 Summary: Character Sheet Generation Pipeline

Commit checkpoint: `56a6ed7` (`feat(prompt-46): character sheet generation`)

## What I changed and why

I implemented the character-sheet stage as a durable generation-and-selection pipeline that mirrors the pitch workflow instead of treating characters as a transient blob.

The backend now generates multiple candidate character sheets for the selected pitch, supports targeted refinements of an existing sheet, persists every generated candidate durably, and exposes that state through hydration and explicit session routes. The frontend now renders those batches as comparison cards, lets the user generate, refine, and select character sheets from the workspace, and routes accepted chat actions through the same durable endpoints so chat and UI stay aligned.

This was necessary to satisfy the prompt’s core requirements:

- multiple distinct character-sheet candidates
- durable and resumable persistence
- fields that support later beat-sheet generation
- readable comparison UI instead of raw JSON

## Architectural changes across the codebase

### Backend AI and prompt layer

- Added [`backend/app/models/character_generation.py`](/Users/kevin/code/storyteller/backend/app/models/character_generation.py) to define the character-generation contract:
  - prompt context
  - invocation/result models
  - candidate sheet/profile models
  - evaluation criteria models
- Added [`backend/app/ai/character_generation.py`](/Users/kevin/code/storyteller/backend/app/ai/character_generation.py) plus [`backend/app/ai/prompts/character_generation.md`](/Users/kevin/code/storyteller/backend/app/ai/prompts/character_generation.md) for the Gemini-facing adapter and prompt template.
- Wired the adapter through [`backend/app/ai/__init__.py`](/Users/kevin/code/storyteller/backend/app/ai/__init__.py) and [`backend/app/api/dependencies.py`](/Users/kevin/code/storyteller/backend/app/api/dependencies.py).

### Backend domain and persistence layer

- Added [`backend/app/services/character_generation.py`](/Users/kevin/code/storyteller/backend/app/services/character_generation.py) as the domain service for:
  - generation
  - refinement
  - fallback heuristics
  - structured evaluation of output quality
- Extended [`backend/app/services/sessions.py`](/Users/kevin/code/storyteller/backend/app/services/sessions.py) with:
  - `generate_character_sheets`
  - `refine_character_sheet`
  - `select_character_sheet`
  - stage invalidation and detail/summary helpers
  - persistence metadata for generation keys, refinement lineage, and selection state
- Extended [`backend/app/repositories/sessions.py`](/Users/kevin/code/storyteller/backend/app/repositories/sessions.py) so session aggregates now load `character_sheets` and the selected character sheet directly.
- Extended [`backend/app/services/session_hydration.py`](/Users/kevin/code/storyteller/backend/app/services/session_hydration.py) so snapshots now expose:
  - `character_sheet_batches`
  - richer `selected_character_sheet`
  - protagonist/supporting-cast/visual-motif views
  - backward-tolerant parsing of older `character_data` payloads

### API surface

- Added character routes in [`backend/app/api/v1/routes/sessions.py`](/Users/kevin/code/storyteller/backend/app/api/v1/routes/sessions.py):
  - `POST /api/v1/sessions/{session_id}/characters/generate`
  - `POST /api/v1/sessions/{session_id}/characters/refine`
  - `POST /api/v1/sessions/{session_id}/selections/character-sheet`
- Extended [`backend/app/models/session.py`](/Users/kevin/code/storyteller/backend/app/models/session.py) with request/response/view models for character generation, refinement, selection, and hydrated batches.

### Frontend workspace and chat bridge

- Added [`frontend/src/features/session/CharacterSelectionStage.tsx`](/Users/kevin/code/storyteller/frontend/src/features/session/CharacterSelectionStage.tsx) for the character workflow UI:
  - batch generation controls
  - refinement controls
  - latest batch comparison cards
  - earlier batch history panels
  - selected-sheet summary
- Extended [`frontend/src/api/sessions.ts`](/Users/kevin/code/storyteller/frontend/src/api/sessions.ts) with character request types, response types, and batch-aware snapshot types.
- Updated [`frontend/src/pages/session/SessionWorkspacePage.tsx`](/Users/kevin/code/storyteller/frontend/src/pages/session/SessionWorkspacePage.tsx) so the workspace can:
  - render the character stage
  - call the new character endpoints
  - apply accepted chat actions for character selection, regeneration, and refinement
- Updated [`frontend/src/features/session/chat/actionEchoes.ts`](/Users/kevin/code/storyteller/frontend/src/features/session/chat/actionEchoes.ts) so character-sheet outputs appear in the transcript as durable action echoes.
- Updated [`frontend/src/styles/index.css`](/Users/kevin/code/storyteller/frontend/src/styles/index.css) with layout support for the new card grid and earlier-batch history blocks.

### Story tools integration

- Updated [`backend/app/services/story_tools.py`](/Users/kevin/code/storyteller/backend/app/services/story_tools.py) so the backend tool layer now invokes the session-owned character-generation flow instead of placeholder stage movement.

## Persistence model decision

I did not add a new migration for this prompt.

Instead, I reused the existing `character_sheets` table and stored generation metadata inside `character_data` JSON:

- `batch_metadata`
- `generation_key`
- `generation_kind`
- `guidance`
- `candidate_index`
- refinement lineage back to the source character sheet and source pitch

That kept the durable model aligned with the pitch stage and avoided introducing a new relational table before the character workflow semantics were fully stable.

## New abstractions, helpers, and extension points

### 1. Character generation service

Use [`CharacterGenerationService.generate_character_sheets(...)`](/Users/kevin/code/storyteller/backend/app/services/character_generation.py) when a caller needs structured candidates without knowing whether the provider path or heuristic fallback will win.

```python
from app.models import ExistingSelectedPitchContext
from app.services.character_generation import CharacterGenerationService

result = CharacterGenerationService().generate_character_sheets(
    candidate_count=3,
    generation_goal="alternatives",
    selected_pitch=ExistingSelectedPitchContext(
        title="The Mapped Lanterns Promise",
        hook="A sleepy apprentice agrees to carry mapped lanterns across a moonlit harbor.",
        central_conflict="The apprentice must finish the route before their worries distort the map.",
        why_it_fits="The story stays gentle, visual, and bedtime-safe.",
    ),
    raw_brief="A sleepy apprentice follows the last lanterns around a harbor before bed.",
    guidance="Keep the support cast compact.",
)
```

Extension point:

- pass a real `CharacterGenerationAdapter` into the service for provider-backed generation
- omit the adapter for deterministic heuristic fallback in tests, local seeding, or degraded mode

### 2. Session-owned durable character workflow

Use [`SessionService.generate_character_sheets(...)`](/Users/kevin/code/storyteller/backend/app/services/sessions.py), [`SessionService.refine_character_sheet(...)`](/Users/kevin/code/storyteller/backend/app/services/sessions.py), and [`SessionService.select_character_sheet(...)`](/Users/kevin/code/storyteller/backend/app/services/sessions.py) to keep persistence, stage transitions, event logging, and invalidation behavior in one place.

```python
response = session_service.generate_character_sheets(
    session_id,
    candidate_count=4,
    guidance="Make one option sibling-focused.",
    character_generation_service=CharacterGenerationService(),
)
```

### 3. API contracts

Generate a new character batch:

```json
POST /api/v1/sessions/{session_id}/characters/generate
{
  "candidate_count": 4,
  "guidance": "Keep the support cast compact and clearly cozy.",
  "origin": "workspace"
}
```

Refine an existing character sheet:

```json
POST /api/v1/sessions/{session_id}/characters/refine
{
  "character_sheet_id": "character-generated-1",
  "revision_number": 21,
  "title": "Juniper Keeper Cast",
  "instructions": "Make the support cast siblings who settle together.",
  "focus_character_names": [],
  "change_summary": null,
  "origin": "workspace"
}
```

Hydration consumers should now expect `snapshot.character_sheet_batches` plus the richer `snapshot.selected_character_sheet` view.

## Verification work

### Targeted automated checks

- `cd backend && pytest tests/test_character_generation_service.py tests/test_session_service.py tests/test_session_api.py`
  - Result: `56 passed`
- `cd frontend && npm test -- SessionWorkspacePage.test.tsx`
  - Result: `24 passed`

### Broader automated checks

- `cd backend && ruff check app tests`
  - Result: passed
- `cd backend && pytest`
  - Result: `151 passed, 5 skipped`
- `cd frontend && npm run lint`
  - Result: passed
- `cd frontend && npm run build`
  - Result: passed
- `cd frontend && npm test`
  - Result: `69 passed`

### Browser and screenshot verification

I used the `webapp-qa` workflow against the live Docker Compose app.

Because the local `secrets.yaml` on this machine contains legacy keys that the current backend settings model now rejects, I used a temporary compose override only for QA to disable file-based secrets loading and keep repository code unchanged. I then seeded a real durable session directly through `SessionService` using heuristic pitch and character generation so the UI verification exercised actual persisted backend state rather than mocks.

Seeded session used for verification:

- session id: `71281140-6108-4b8f-a1d1-f26c5ebeb4b4`
- durable state: selected pitch, generated character batch, selected character sheet, and refined character batch

Browser checks run:

- desktop screenshot:
  - `docker compose -f infra/compose/docker-compose.yml -f .artifacts/webapp-qa/prompt-46-compose.override.yml run --rm browser npm run check -- --spec /workspace/.artifacts/webapp-qa/prompt-46-character-stage-desktop.spec.json`
  - final artifact: [`prompt-46-character-stage-desktop.png`](/Users/kevin/code/storyteller/.artifacts/webapp-qa/prompt-46-character-stage-desktop.png)
- mobile screenshot:
  - `docker compose -f infra/compose/docker-compose.yml -f .artifacts/webapp-qa/prompt-46-compose.override.yml run --rm browser npm run check -- --spec /workspace/.artifacts/webapp-qa/prompt-46-character-stage-mobile.spec.json`
  - final artifact: [`prompt-46-character-stage-mobile.png`](/Users/kevin/code/storyteller/.artifacts/webapp-qa/prompt-46-character-stage-mobile.png)

What I visually verified:

- the route-backed character preview renders correctly even when the durable current stage is already `beat sheet`
- the selected refined character sheet appears in the summary cards
- the latest refined batch renders as a comparison card
- earlier generated batches remain visible and resumable
- the generate/refine controls are present and readable on desktop and mobile widths

Visual verification limits:

- I verified rendering of persisted character data, not live provider-backed Gemini output
- I did not visually exercise a live click-through generation request from the browser because I intentionally used deterministic seeded backend data to avoid coupling QA to local credential state

## LLM and prompt evaluation suite

This prompt changed LLM-facing logic, so I added a structured evaluation layer in [`backend/app/services/character_generation.py`](/Users/kevin/code/storyteller/backend/app/services/character_generation.py) and covered it with [`backend/tests/test_character_generation_service.py`](/Users/kevin/code/storyteller/backend/tests/test_character_generation_service.py).

Named criteria from a concrete evaluation run of the new service:

- `candidate_count_matches_request`: pass, measured `3`
- `all_required_fields_present`: pass, measured `3`
- `titles_are_distinct`: pass, measured `3`
- `protagonist_names_are_distinct`: pass, measured `3`
- `supporting_cast_present`: pass, measured `3`
- `relationships_are_grounded`: pass, measured `3`
- `bedtime_safety_notes_are_grounded`: pass, measured `3`

Additional eval-related automated coverage now checks:

- provider output passes through unchanged when valid
- adapter failure falls back to heuristic generation
- trivial/reflection-like outputs are replaced by stronger fallback candidates
- provider metadata is preserved
- refinement fallback preserves source-sheet guidance

## Wrong turns, dead ends, and gotchas

- I initially ran `npm test -- --runInBand SessionWorkspacePage.test.tsx` out of Jest habit. This repo uses Vitest, so `--runInBand` is invalid. I reran with `npm test -- SessionWorkspacePage.test.tsx`.
- Two frontend tests were failing because the assertions had drifted from the actual UI copy:
  - one expected a bare refined pitch title instead of the rendered `Selected pitch: ...` detail
  - one expected `generated 5 character options` instead of the current `5 cast cards ready` summary
- The first desktop browser spec failed because I asserted `beats` while the UI correctly labels the stage `beat sheet`.
- Docker Compose browser QA was blocked twice by local environment issues unrelated to the feature:
  - an orphan `storyteller-backend-override` container was still holding port `8565`
  - the local `secrets.yaml` contains legacy keys (`gemini.api_key_name`, `gemini.project_name`, `gemini.project_number`, `openai`) that the current settings model forbids

## Assumptions made while working unsupervised

- Reusing the existing `character_sheets` table plus `character_data` metadata was the right persistence tradeoff for this prompt, and a new migration was not yet warranted.
- The existing catalog slugs `quest-fantasy` and `hushed-wonder` remain the correct canonical examples for QA seeding.
- Heuristic generation is an acceptable degraded path for local development, automated tests, and browser QA seeding when provider access is unavailable or intentionally avoided.
- Character hydration must stay tolerant of mixed historical payload shapes, because earlier prompt work may already have written less-structured `character_data`.

## Remaining risks or follow-up notes

- The compose backend service still points at `/workspace/secrets.yaml`; on this machine that local file currently contains legacy fields that prevent startup without an override. That is an environment/config hygiene problem, not a character-stage code problem, but it will keep affecting local full-stack runs until the file is cleaned up or the compose flow is made more tolerant.
- Character persistence is intentionally JSON-heavy for now. If later prompts need richer querying across relationship graphs or visual motifs, a relational decomposition may become worthwhile.
