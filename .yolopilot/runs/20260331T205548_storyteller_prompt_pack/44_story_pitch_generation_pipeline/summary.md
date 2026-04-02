# Prompt 44: Story Pitch Generation Pipeline

## What I changed and why

I implemented the missing pitch-generation stage end to end so a session can now move from a saved brief into a durable set of multiple candidate story pitches, and the user can review and select those pitches in the workspace UI.

The main product goal for this prompt was not just "call a model and show text." The stage needed three things at once:

1. Multiple meaningful pitch options generated from the selected genre, tone, and saved brief.
2. Durable persistence so the user can leave and resume later without losing the options.
3. A comparison-oriented main-pane UI that makes the cards easy to scan and select.

I kept the implementation aligned with the existing architecture by:

- adding a dedicated backend pitch-generation service instead of burying prompt logic in route handlers
- persisting pitch batches through the existing `pitches` table and session hydration flow instead of inventing a new opaque blob store
- exposing generation and selection through explicit API routes
- wiring the frontend stage through the same snapshot-driven workspace model the app already uses

I committed the product changes on the current branch as:

- `d3b4ece feat(prompt-44): pitch generation pipeline`

## Architectural changes

### Backend pitch-generation stack

I added a new pitch-generation backend slice with a clear separation between prompt construction, provider I/O, result validation, fallback behavior, and persistence.

New backend pieces:

- `backend/app/ai/pitch_generation.py`
  - Gemini adapter for structured pitch generation
  - prompt rendering
  - JSON schema sanitization for Gemini response schema support
  - transport/error normalization
- `backend/app/ai/prompts/pitch_generation.md`
  - stable prompt template for pitch generation
- `backend/app/models/pitch_generation.py`
  - typed pitch-generation request/result/evaluation models
- `backend/app/services/pitch_generation.py`
  - orchestration service
  - candidate differentiation evaluation
  - heuristic fallback when Gemini fails or returns trivial rewrites
  - model-output persistence payload builder

Key behavior:

- The service requests a stable structured output shape with:
  - `title`
  - `hook`
  - `central_conflict`
  - `why_it_fits`
- The service evaluates returned batches before trusting them.
- If the adapter fails or returns low-quality trivial rewrites, the service falls back to a deterministic heuristic generator instead of leaving the stage unusable.

### Durable session integration

I extended the existing session and hydration flows so pitch batches are first-class session state.

Changed backend session flow:

- `backend/app/services/sessions.py`
  - new `generate_pitches(...)`
  - new `select_pitch(...)`
  - downstream invalidation when pitches change
  - stage event recording
  - AI output recording
- `backend/app/repositories/sessions.py`
  - repository aggregate now loads pitch rows with the session
- `backend/app/services/session_hydration.py`
  - snapshot now includes `pitch_batches`
  - pitch rows grouped by `generation_key` into durable pitch batches
- `backend/app/services/event_log.py`
  - AI output recording now refreshes conversation memory snapshots, keeping the chat/history bridge aligned with generated pitch output

I reused the existing `pitches` persistence model rather than adding a migration in this prompt. The current schema already had the needed durable pitch record fields, so I mapped the new stable UI shape onto those stored columns:

- `hook` persisted through existing `logline`
- `central_conflict` persisted through existing `summary`
- `why_it_fits` persisted through existing `bedtime_notes`

This avoided unnecessary schema churn while still giving the frontend a clean, explicit API shape.

### API surface

I added explicit versioned routes for pitch generation and selection in `backend/app/api/v1/routes/sessions.py`:

- `POST /api/v1/sessions/{session_id}/pitches/generate`
- `POST /api/v1/sessions/{session_id}/selections/pitch`

Dependency injection was extended in `backend/app/api/dependencies.py` so the pitch-generation adapter is created in one place and closed during app shutdown in `backend/app/main.py`.

### Tooling and workflow integration

I updated `backend/app/services/story_tools.py` so chat-driven workflow tools no longer stub pitch generation. The `generate_pitches` tool path now calls the real session service and returns a stage result backed by the same durable session snapshot as direct UI usage.

### Frontend workspace stage

I added the actual pitch stage UI in:

- `frontend/src/features/session/PitchSelectionStage.tsx`

This stage now renders:

- batch summary cards
- generation controls
- latest pitch cards
- earlier batch history
- selection actions

I integrated it into the workspace flow in:

- `frontend/src/pages/session/SessionWorkspacePage.tsx`

and extended the API client in:

- `frontend/src/api/sessions.ts`

to support:

- `generateSessionPitches(...)`
- `selectSessionPitch(...)`
- `snapshot.pitch_batches`

I also updated the chat bridge so generated pitch batches show up as assistant-style echoes and hydrated sessions can surface a "pitch batch ready" message on resume:

- `frontend/src/features/session/chat/actionEchoes.ts`
- `frontend/src/features/session/chat/sessionChat.ts`

## New abstractions and extension points

### 1. `PitchGenerationService`

This is the main extension point for future pitch-generation behavior.

Example:

```python
from app.services.pitch_generation import PitchGenerationService

service = PitchGenerationService(adapter=my_adapter)
result = service.generate_pitches(
    candidate_count=4,
    raw_brief="A fox returns a lantern across a sleepy harbor.",
    genre_label="Quest Fantasy",
    tone_label="Hushed Wonder",
)
```

What this buys us:

- adapter-backed structured generation when the provider works
- deterministic fallback when the provider fails
- consistent quality evaluation regardless of source

### 2. Pitch batch evaluation criteria

The generated pitch batch is now evaluated against named criteria before the app accepts it as trusted provider output:

- `candidate_count_matches_request`
- `all_required_fields_present`
- `titles_are_distinct`
- `hooks_are_distinct`
- `central_conflicts_are_descriptive`
- `why_it_fits_notes_are_grounded`

This is the main guardrail against trivial rewrites and thin low-signal output.

### 3. Durable `pitch_batches` in the session snapshot

The frontend now hydrates past batches directly from the session snapshot.

Example API shape:

```json
{
  "pitch_batches": [
    {
      "generation_key": "pitch-batch-7af5f08bcb96",
      "candidate_count": 4,
      "created_at": "2026-04-02T04:19:00Z",
      "pitches": [
        {
          "id": "…",
          "title": "The Silver Harbor Water Promise",
          "hook": "…",
          "central_conflict": "…",
          "why_it_fits": "…",
          "is_selected": false
        }
      ]
    }
  ]
}
```

This makes resume/review straightforward and gives later prompts an obvious extension point for pitch refinement and history-aware UX.

### 4. Explicit pitch selection endpoint

The stage no longer depends on implicit local state to move forward. Selection is durable and server-owned.

Example request:

```json
POST /api/v1/sessions/{session_id}/selections/pitch
{
  "pitch_id": "pitch-uuid",
  "generation_key": "pitch-batch-7af5f08bcb96",
  "pitch_index": 1,
  "title": "The Silver Harbor Water Promise",
  "origin": "workspace"
}
```

## Verification performed

## Automated backend verification

I ran these backend checks successfully after implementation and again after formatting the touched backend files:

- `backend/.venv/bin/python -m ruff check backend/app backend/tests`
  - result: passed
- `backend/.venv/bin/python -m ruff format --check backend/app/ai/__init__.py backend/app/ai/pitch_generation.py backend/app/api/dependencies.py backend/app/api/v1/routes/sessions.py backend/app/main.py backend/app/models/__init__.py backend/app/models/pitch_generation.py backend/app/models/session.py backend/app/repositories/sessions.py backend/app/services/__init__.py backend/app/services/event_log.py backend/app/services/pitch_generation.py backend/app/services/session_hydration.py backend/app/services/sessions.py backend/app/services/story_tools.py backend/tests/test_pitch_generation_service.py backend/tests/test_session_api.py`
  - result: `17 files already formatted`
- `backend/.venv/bin/python -m pytest backend/tests/test_pitch_generation_service.py backend/tests/test_session_api.py backend/tests/test_story_tools.py backend/tests/test_session_service.py`
  - result: `55 passed`

Additional earlier targeted backend run:

- `backend/.venv/bin/python -m pytest backend/tests/test_session_service.py backend/tests/test_session_api.py backend/tests/test_story_tools.py backend/tests/test_brief_normalization_service.py`
  - result: `53 passed`

## Automated frontend verification

I ran these frontend checks successfully:

- `npm --prefix frontend run test -- --run src/pages/session/SessionWorkspacePage.test.tsx`
  - result: `18 passed`
- `npm --prefix frontend run lint`
  - result: passed
- `npm --prefix frontend run build`
  - result: passed

I reran those frontend checks after fixing Prettier formatting in the touched files.

## Browser and visual verification

I verified the real compose-backed app instead of only relying on unit tests.

Live environment details:

- compose entrypoint used: `./scripts/dev-compose.sh`
- frontend URL: `http://127.0.0.1:8566`
- backend URL: `http://127.0.0.1:8565`

Why this mattered:

- the repo does not expose `docker compose` directly from the repo root
- the compose file lives under `infra/compose/docker-compose.yml`
- using the repo wrapper matched the project’s actual local-dev contract

For browser QA, I created a real session through the backend API, drove it through:

- session creation
- genre selection
- tone selection
- brief save
- pitch generation

The generated QA session was:

- session id: `78337a7b-2239-4eaf-a292-dccb68801ec8`
- generation key: `pitch-batch-7af5f08bcb96`

The generated pitch titles were:

- `The Silver Harbor Water Promise`
- `The Lantern Reflections Question`
- `The Quiet Docks Map`
- `The Sleeping Gulls Song`

That live run confirmed the stage produced differentiated options and stored them durably enough to render through the real frontend.

Browser evidence captured:

- `/Users/kevin/code/storyteller/.artifacts/webapp-qa/prompt-44-pitches-desktop-stage.png`
- `/Users/kevin/code/storyteller/.artifacts/webapp-qa/prompt-44-pitches-mobile-stage.png`
- `/Users/kevin/code/storyteller/.artifacts/webapp-qa/prompt-44-pitches-desktop-stage-viewport.png`
- `/Users/kevin/code/storyteller/.artifacts/webapp-qa/prompt-44-pitches-mobile-stage-viewport.png`

Functional browser assertions performed through Puppeteer/containerized QA:

- the pitch stage rendered successfully
- `4` `Choose pitch` buttons were present before reload on desktop
- `4` `Choose pitch` buttons were present after reload on desktop
- `4` `Choose pitch` buttons were present before reload on mobile
- `4` `Choose pitch` buttons were present after reload on mobile

This gave direct evidence that the durable pitch batch survived a fresh hydration cycle, not just an in-memory client transition.

## Canonical repo verification target

I also ran:

- `make check`

Result:

- failed, but the failure was not caused by prompt 44 behavior
- it failed in the repo-wide backend format check because unrelated files outside this prompt already have formatting drift

Representative unrelated files reported by the global format check:

- `app/services/catalog.py`
- `app/services/conversation_memory.py`
- `tests/test_db_models.py`

I did not mass-reformat unrelated backend files because that would have created a broad opportunistic diff outside the scope of this prompt. Instead, I formatted and rechecked every backend file touched by prompt 44 specifically.

## LLM and prompt evaluation suite

I added `backend/tests/test_pitch_generation_service.py` as the prompt-facing evaluation suite for this change.

### Evaluation case: `test_eval_structured_pitch_generation_happy_path_uses_adapter_output`

Outcome:

- pass

Measured criteria:

- `candidate_count_matches_request`: pass, measured value `3`
- `all_required_fields_present`: pass, measured value `3`
- `titles_are_distinct`: pass, measured value `3`
- `hooks_are_distinct`: pass, measured value `3`
- `central_conflicts_are_descriptive`: pass, measured value `3`
- `why_it_fits_notes_are_grounded`: pass, measured value `3`

This verifies the happy path where adapter output is accepted directly.

### Evaluation case: `test_eval_fallback_resilience_uses_heuristics_when_adapter_fails`

Outcome:

- pass

Measured outcomes:

- provider source switched to `heuristic`
- returned pitch count: `4`
- final batch evaluation: pass
- fallback reason preserved: `simulated Gemini outage`

This verifies the app still produces usable pitch cards when the provider call fails.

### Evaluation case: `test_eval_validation_guardrail_falls_back_when_adapter_returns_trivial_rewrites`

Outcome:

- pass

Measured outcomes:

- invalid adapter output triggered fallback
- fallback reason included failed criteria:
  - `titles_are_distinct`
  - `hooks_are_distinct`
- final heuristic batch evaluation: pass

This verifies that low-quality "same idea three times" model output is rejected instead of silently accepted.

### Evaluation case: `test_eval_pitch_model_output_preserves_provider_context_and_criteria`

Outcome:

- pass

Measured outcomes:

- `generation_source == "gemini"`: pass
- `model_id == "gemini-3.1-pro"`: pass
- `prompt_version == "pitch_generation.v1"`: pass
- `evaluation.passed == true`: pass

This verifies that durable model metadata and evaluation details are persisted for later debugging and auditability.

## Wrong turns, dead ends, and gotchas

### 1. The initial story-tool path was still a stub

I found that `StoryWorkflowToolService._generate_pitches(...)` did not actually generate pitches yet; it only updated stage state. I replaced that stub with the real session-service-backed generation path so chat-driven workflow actions use the same durable pipeline as the UI.

### 2. The repo’s compose contract is not plain `docker compose` from the root

My first compose-state check using `docker compose ps --format json` from the repo root failed because there is no root compose file. The correct project contract is `./scripts/dev-compose.sh` or the root `Makefile` targets. I adjusted the QA flow accordingly.

### 3. Local Playwright CLI availability did not mean the `playwright` package was importable

`npm --prefix frontend exec playwright --version` worked, but importing `playwright` from a local Node script in `frontend/` failed because the package was not actually present there as a normal dependency. I switched to the repo’s dedicated browser QA container and the bundled Puppeteer tooling instead of forcing a dependency workaround.

### 4. Full-page screenshots were technically valid but visually poor

The first automated screenshots captured the entire long workspace page, which compressed the pitch cards too much to be reviewer-useful. I reran browser QA with a focused scroll-to-stage Puppeteer script and captured readable stage-level artifacts instead.

### 5. `make check` is currently not a fully reliable green gate for scoped prompt work

The global format check is blocked by unrelated backend files that predate this prompt’s diff. I preserved scope discipline rather than introducing a noisy repo-wide formatting commit.

## Assumptions I made while working unsupervised

- The existing `pitches` table was sufficient for this prompt, so I reused it instead of adding a migration solely to rename storage columns to the new UI vocabulary.
- Durable pitch history should preserve prior batches instead of deleting old ones; I implemented batch grouping by `generation_key` and surfaced older batches in the UI.
- If the provider is unavailable during local development, the stage should still be functional. I treated deterministic heuristic fallback as the right product behavior for this prompt.
- Clearing the selected pitch on regeneration unless `preserve_selected_pitch` is requested is the safest default, because a newly generated batch conceptually reopens the pitch decision.
- Stage invalidation should follow the repo’s existing pattern: mark downstream planning as needing refresh rather than attempting aggressive record deletion in this prompt.

## Reviewer notes

If you want to inspect the implementation quickly, start with these files:

- `backend/app/services/pitch_generation.py`
- `backend/app/services/sessions.py`
- `backend/app/services/session_hydration.py`
- `backend/app/api/v1/routes/sessions.py`
- `frontend/src/features/session/PitchSelectionStage.tsx`
- `frontend/src/pages/session/SessionWorkspacePage.tsx`
- `backend/tests/test_pitch_generation_service.py`
- `frontend/src/pages/session/SessionWorkspacePage.test.tsx`

That slice shows the full end-to-end path from generation logic, to persistence, to hydration, to UI rendering, to test coverage.
