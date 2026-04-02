# Prompt 43 Summary: Normalize the User Brief Into Structured Preferences

Commit checkpoint: `4e98ad6` (`feat(prompt-43): brief normalization service`)

## What I changed and why

I added a durable brief-normalization flow so the backend no longer has to keep reparsing raw prose every time later planning stages need structured guidance.

The backend now:

- normalizes the saved story brief into typed structured preferences,
- stores those preferences alongside the raw brief and normalized summary,
- preserves provider metadata about how the normalization was produced,
- falls back to deterministic heuristics if the Gemini normalization call fails,
- lets the user override the extracted interpretation without losing the link to the raw brief.

The frontend now exposes that interpretation directly in the brief stage instead of hiding it as implicit backend behavior. The user can review and edit:

- normalized summary,
- protagonist type,
- setting,
- emotional goal,
- constraint notes,
- bedtime-safety concerns,
- candidate motifs.

That satisfies the acceptance bar that later generators can rely on structured preferences, the normalized view stays tied to the original brief, and the user can correct the extraction.

## Architectural changes across the codebase

### Backend model and storage changes

- Added `backend/app/models/brief_normalization.py` with typed normalization models:
  - `NormalizedBriefPreferences`
  - `BriefNormalizationPromptContext`
  - `BriefNormalizationStructuredOutput`
  - `BriefNormalizationInvocation`
  - `BriefNormalizationInvocationResult`
  - `BriefNormalizationResult`
- Added `normalized_preferences` to `StoryBrief` in `backend/app/db/models.py`.
- Added migration `backend/migrations/versions/20260401_04_add_story_brief_normalized_preferences.py`.
- Extended API/session view models in `backend/app/models/session.py` so `StoryBriefView` and `SaveSessionStoryBriefRequest` both understand `normalized_preferences`.

### AI adapter layer

- Added `backend/app/ai/brief_normalization.py`.
- Added strict prompt template `backend/app/ai/prompts/brief_normalization.md`.
- Wired adapter construction in `backend/app/api/dependencies.py`.
- Wired adapter shutdown in `backend/app/main.py`.

The adapter mirrors the existing Gemini structured-output pattern already used elsewhere in the repo:

- prompt rendering is isolated,
- response schema is explicit,
- Gemini JSON schema is sanitized before request submission,
- parsing happens into typed Python models instead of ad hoc dict access.

### Service layer

- Added `backend/app/services/brief_normalization.py`.

That service centralizes:

- Gemini normalization invocation,
- deterministic fallback extraction,
- normalized summary synthesis,
- override merging,
- durable `model_output` assembly,
- reconstruction of saved normalization state from existing rows.

I then injected this service into `SessionService` in `backend/app/services/sessions.py`, so saving the story brief now becomes the single durability point for both raw brief text and normalized interpretation.

### Session save semantics

I changed the story-brief save flow so it distinguishes between:

- fields omitted by the client,
- fields intentionally cleared by the client,
- fields that should be regenerated because the raw brief changed and the user did not manually override the interpretation.

This matters because the UI should not accidentally erase or lock stale normalized data just by saving a raw brief change.

### Downstream context consumers

I updated:

- `backend/app/services/agent_context.py`
- `backend/app/services/conversation_memory.py`

Both now read normalized brief preferences directly and include them in downstream planning context as first-class structured preferences instead of forcing later stages to infer everything again from raw prose.

### Frontend UX changes

- Added `NormalizedBriefPreferencesView` to `frontend/src/api/sessions.ts`.
- Extended the brief stage in `frontend/src/features/session/StoryBriefStage.tsx`.
- Updated `frontend/src/pages/session/SessionWorkspacePage.tsx` to preserve omission vs explicit null behavior for normalized fields.
- Added CSS in `frontend/src/styles/index.css` for the interpretation panel and summary treatment.

The brief stage now has two visible surfaces:

1. the raw free-form bedtime brief,
2. the editable interpretation generated from it.

That keeps the extraction legible and correctable instead of magical.

## New abstractions, helpers, and extension points

### `BriefNormalizationService`

Primary backend entry point for normalization.

Example use:

```python
result = brief_normalization_service.normalize_brief(
    raw_brief=raw_brief,
    prompt_context=BriefNormalizationPromptContext(
        genre_label="Quest Fantasy",
        tone_label="Hushed Wonder",
    ),
)
```

This returns normalized structured preferences plus provider/fallback metadata suitable for persistence.

### `apply_brief_normalization_overrides`

Use this when a caller has saved model output but wants user corrections to become the durable interpretation.

Example use:

```python
effective = apply_brief_normalization_overrides(
    generated_preferences=result.preferences,
    generated_summary=result.normalized_summary,
    override_preferences=request.normalized_preferences,
    override_summary=request.normalized_summary,
)
```

### `build_brief_normalization_result_from_existing`

Use this when existing persistence should be reconstructed without rerunning Gemini.

This is the reuse path when the raw brief did not change and the client is not asking for a fresh normalization.

### API payload extension

`POST /api/v1/sessions/{session_id}/story-brief` now accepts optional `normalized_preferences`.

Example payload with manual corrections:

```json
{
  "story_idea": "A child and an otter guardian drift after runaway lanterns to bring each light home before the harbor sleeps.",
  "normalized_summary": "A harbor bedtime adventure about belonging, gentle courage, and a safe return home.",
  "normalized_preferences": {
    "protagonist_type": "A child and an otter guardian",
    "setting": "a harbor",
    "emotional_goal": "belonging and calm reassurance",
    "constraint_notes": [
      "End with the harbor settled",
      "Keep conflict gentle"
    ],
    "bedtime_safety_concerns": [
      "Resolve mystery quickly",
      "Avoid villains"
    ],
    "candidate_motifs": [
      "floating lanterns",
      "moonlit water"
    ]
  },
  "origin": "workspace"
}
```

The important extension-point behavior is that callers can omit `normalized_summary` and `normalized_preferences` entirely to request regeneration-by-save, or send them explicitly to persist user overrides.

## Files touched

Key implementation files:

- `backend/app/models/brief_normalization.py`
- `backend/app/ai/brief_normalization.py`
- `backend/app/ai/prompts/brief_normalization.md`
- `backend/app/services/brief_normalization.py`
- `backend/app/services/sessions.py`
- `backend/app/services/agent_context.py`
- `backend/app/services/conversation_memory.py`
- `backend/app/models/session.py`
- `backend/app/db/models.py`
- `backend/migrations/versions/20260401_04_add_story_brief_normalized_preferences.py`
- `frontend/src/features/session/StoryBriefStage.tsx`
- `frontend/src/pages/session/SessionWorkspacePage.tsx`
- `frontend/src/api/sessions.ts`
- `frontend/src/styles/index.css`

Key test files:

- `backend/tests/test_brief_normalization_adapter.py`
- `backend/tests/test_brief_normalization_service.py`
- `backend/tests/test_session_service.py`
- `backend/tests/test_session_api.py`
- `frontend/src/pages/session/SessionWorkspacePage.test.tsx`

## Verification performed

### Backend verification

Commands run:

- `ruff check backend/app backend/tests --fix`
- `pytest backend/tests/test_brief_normalization_adapter.py backend/tests/test_brief_normalization_service.py backend/tests/test_session_service.py backend/tests/test_session_api.py backend/tests/test_migrations.py backend/tests/test_db_models.py`
- `pytest backend/tests/test_session_hydration_service.py backend/tests/test_conversation_memory_evals.py backend/tests/test_action_policy_service.py backend/tests/test_intent_parser_service.py`
- `pytest backend/tests`

Results:

- targeted normalization/session backend tests: `51 passed`
- broader touched-area backend tests: `18 passed`
- full backend suite: `130 passed, 5 skipped`

### Frontend verification

Commands run:

- `npm test -- --run src/pages/session/SessionWorkspacePage.test.tsx`
- `npm run lint`
- `npm run build`
- `npm test`

Results:

- targeted workspace page test file: `16 passed`
- full frontend test suite: `59 passed`
- lint: passed
- production build: passed

### Browser and visual verification

I verified the new interpretation UI against the running Docker Compose app and a seeded real session:

- session used: `b7725d68-5ab4-4516-a37c-4a9e5eb3ac1f`
- host route checked: `http://localhost:8566/sessions/b7725d68-5ab4-4516-a37c-4a9e5eb3ac1f?stage=brief`

Browser assertions covered:

- `Editable interpretation`
- `Normalized summary`
- `Bedtime-safety concerns`
- concrete extracted values such as `A child and an otter guardian` and `Floating lanterns`

Artifacts captured:

- full-page desktop: `/Users/kevin/code/storyteller/.artifacts/webapp-qa/prompt-43-brief-desktop.png`
- full-page mobile: `/Users/kevin/code/storyteller/.artifacts/webapp-qa/prompt-43-brief-mobile.png`
- focused desktop viewport: `/Users/kevin/code/storyteller/.artifacts/webapp-qa/prompt-43-brief-panel-desktop-viewport.png`
- focused mobile viewport: `/Users/kevin/code/storyteller/.artifacts/webapp-qa/prompt-43-brief-panel-mobile-viewport.png`

Visual conclusions:

- the brief stage now visibly shows the editable interpretation section rather than hiding normalization,
- normalized summary and extracted preference fields render in the brief stage,
- the mobile layout keeps the interpretation editor readable,
- the desktop two-pane layout still renders correctly, although the most readable focused artifact is the mobile viewport capture and the desktop full-page artifact is more useful than the narrow panel crop for overall layout context.

Remaining visual limit:

- I did not run a full manual interaction flow inside the browser to edit the interpretation fields and save them through the UI after screenshot capture. That path is covered by automated frontend tests and API tests, but the browser verification focused on rendered presence and responsive layout.

## LLM and prompt evaluation suite

Because this prompt changes Gemini-facing structured output behavior, I added targeted evaluation-style tests. Named criteria and outcomes:

- `structured_extraction_happy_path_uses_adapter_output`: Pass
- `fallback_resilience_uses_heuristics_when_adapter_fails`: Pass
- `user_override_merging_keeps_manual_corrections`: Pass
- `saved_metadata_round_trip_preserves_provider_context`: Pass
- `prompt_includes_rules_and_context`: Pass
- `schema_sanitization_strips_unsupported_keywords`: Pass
- `adapter_requests_json_schema_and_parses_structured_response`: Pass

What those criteria cover:

- happy-path structured extraction,
- fallback behavior when Gemini is unavailable or malformed,
- regression protection for user-edited interpretation overrides,
- persistence of provider metadata for later auditing/debugging,
- prompt strictness and contextual grounding,
- Gemini schema compatibility,
- adapter request/response contract correctness.

## Wrong turns, dead ends, and gotchas

### Compose backend startup was broken by local secrets shape

The repo’s normal `docker compose up` backend path failed because the local `secrets.yaml` mounted into `/workspace/secrets.yaml` contains extra keys that the current settings model does not accept:

- `gemini.api_key_name`
- `gemini.project_name`
- `gemini.project_number`
- `openai`

I did not edit user secrets. Instead I brought up a one-off backend container with:

- `STORYTELLER_SECRETS_FILE=`
- `STORYTELLER_GEMINI_API_KEY=test-gemini-key`

That let the frontend proxy reach a healthy backend for browser QA without mutating local secret configuration.

### The browser harness initially retriggered the broken backend dependency chain

`docker compose run --rm browser ...` tried to start the compose-managed backend service because of service dependencies. That failed for the same secrets reason. I worked around it by executing the QA runner inside the already-running `storyteller-browser-1` container instead of invoking a new compose run that bootstraps dependencies.

### A pre-existing docs artifact drift surfaced during the full backend suite

The full backend suite exposed that `docs/chat-to-ui-actions.schema.json` was stale relative to the generated schema bundle. I regenerated the file so the suite passed cleanly. This was not directly caused by brief normalization logic, but it was necessary to leave the repo in a passing state.

### Omitted vs explicit-null request semantics mattered more than expected

While wiring the frontend and backend together, I found an integration bug risk: the frontend had a path that coerced absent normalized fields into `null`, which collapses the distinction between:

- "user did not touch interpretation fields"
- "user explicitly cleared interpretation fields"

That would have broken the intended auto-regeneration behavior. I fixed the request plumbing so omission remains omission.

### Reviewer-friendly screenshoting took an extra pass

The first desktop/mobile captures proved DOM presence but cropped before the interesting UI. I reran them as full-page screenshots and added focused viewport captures to make the interpretation panel legible.

## Assumptions made while working unsupervised

- Saving the story brief should remain durable even if Gemini normalization fails, so heuristic fallback is preferable to blocking the save.
- Later planning stages should consume normalized preferences from durable session state instead of reparsing raw prose.
- The right UX for this prompt is to surface normalized interpretation directly inside the brief stage rather than in a separate hidden/debug-only area.
- If the raw brief changes and the user does not touch the interpretation fields, regeneration on save is the intended behavior.
- If the user edits normalized fields, those edits should become the authoritative interpretation for that revision even if model output differs.
- Keeping provider metadata in `model_output` is worth the extra payload because prompt/model debugging will matter as the planning pipeline evolves.

## Final state

The prompt-43 implementation is in place, committed, and verified. The codebase now has a dedicated brief-normalization service, typed normalized brief persistence, UI editing for extracted preferences, downstream context usage of structured preferences, and a passing test/build/lint baseline with browser evidence for the new UI.
