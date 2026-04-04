# Prompt 50 Summary: Story Length, Duration, and Chapter Setup

## What I changed and why

I implemented the `story_setup` stage as a durable, revisitable planning step for soft composition targets. The goal of this prompt was not to enforce exact output length, but to let the user guide the writing stage with calm, honest expectations around pacing and structure.

The final result adds:

- a dedicated story-setup workspace form in the frontend
- a backend API for persisting story-setup preferences
- persistence for target word count, target read-aloud duration, chapter count, optional approximate scene count, and pacing notes
- inline UI language that repeatedly frames these values as correlated suggestions rather than guarantees
- chat/workspace integration so structured chat actions can update story setup without losing omitted fields
- LLM-facing summary coverage so durable memory and prompt context now include approximate scene counts

## Architectural changes across the codebase

### Backend persistence and API

I extended the durable `story_setups` model with `approximate_scene_count` and added an Alembic migration:

- `backend/app/db/models.py`
- `backend/migrations/versions/20260402_01_story_setup_scene_count.py`

I added explicit request/response types for saving story setup through the session API:

- `backend/app/models/session.py`
- `backend/app/models/story_tools.py`

I exposed a new route:

- `POST /api/v1/sessions/{session_id}/story-setup`
- implemented in `backend/app/api/v1/routes/sessions.py`

That route delegates to the existing workflow tool layer rather than bypassing it, which keeps stage transitions, event emission, invalidation behavior, and replayability in one place.

### Tool-service integration

I extended `UpdateSetupHeuristicsToolInput` and the `StoryWorkflowToolService` implementation so story-setup saves now support:

- `target_word_count`
- `target_runtime_minutes`
- `chapter_count`
- `approximate_scene_count`
- `guidance_notes`
- `origin`

The important behavioral detail is that the tool now distinguishes omitted fields from explicit `null` clears by using `model_fields_set`. That prevents chat actions or UI saves from wiping values the user did not actually change.

Files:

- `backend/app/models/story_tools.py`
- `backend/app/services/story_tools.py`

### Hydration, memory, and agent context

I updated the session summary builders so saved story-setup preferences flow into:

- hydrated session summaries
- conversation-memory snapshots
- agent context summaries
- intent-parser prompt context

This keeps the new planning targets visible to later AI-assisted steps without turning them into hard constraints.

Files:

- `backend/app/services/session_hydration.py`
- `backend/app/services/conversation_memory.py`
- `backend/app/services/agent_context.py`
- `backend/app/services/intent_parser.py`

### Frontend workspace UI

I added a dedicated stage component instead of using the generic stage-note editor:

- `frontend/src/features/session/StorySetupStage.tsx`

This component provides:

- numeric fields for word count, runtime, chapter count, and approximate scene count
- a text area for pacing notes
- client-side range validation
- a summary rail with correlation hints for runtime/word-count and chapter/scene shape
- inline copy explaining that these are soft targets
- durable save/reset behavior
- preview links back to beats and forward to composition

I then wired that component into the session workspace and chat-action application path:

- `frontend/src/pages/session/SessionWorkspacePage.tsx`
- `frontend/src/api/sessions.ts`

### Tests and evaluation coverage

I updated the workspace tests to cover both direct form saves and chat-driven story-setup application:

- `frontend/src/pages/session/SessionWorkspacePage.test.tsx`

I updated backend API, migration, model, and tool tests for the new field and endpoint:

- `backend/tests/test_session_api.py`
- `backend/tests/test_story_tools.py`
- `backend/tests/test_db_models.py`
- `backend/tests/test_migrations.py`

Because prompt 50 touched LLM-facing memory and prompt context, I also extended the existing durable-memory evaluation suite:

- `backend/tests/test_conversation_memory_evals.py`

## New abstractions, helpers, and extension points

### Frontend API helper

`saveSessionStorySetup()` is now the typed client entrypoint for story-setup saves.

Example:

```ts
await saveSessionStorySetup(sessionId, {
  targetWordCount: 1800,
  targetRuntimeMinutes: 14,
  chapterCount: 4,
  approximateSceneCount: 10,
  guidanceNotes: 'Keep each chapter ending calmer than it began.',
  origin: 'workspace',
  previewCurrentStage: false,
})
```

Key behavior:

- omit a field to leave it unchanged
- send `null` to clear a previously saved field
- keep `previewCurrentStage: false` when the UI should stay on `story_setup` after save

### Workspace component

`StorySetupStage` is the dedicated extension point for future story-setup controls. If later prompts add scene pacing presets, chapter style controls, or duration heuristics, they should live in this component rather than returning to the generic note editor path.

### Backend route and tool path

The new session route intentionally reuses the story workflow tool service instead of writing directly to repositories. That means future story-setup fields should usually be added in this order:

1. extend `SaveSessionStorySetupRequest`
2. extend `UpdateSetupHeuristicsToolInput`
3. update `StoryWorkflowToolService._update_setup_heuristics`
4. surface the field in hydration and summaries
5. expose it in the frontend API/types

## Exact verification work performed

### Automated backend verification

Targeted backend tests after the initial implementation:

```bash
pytest backend/tests/test_story_tools.py backend/tests/test_session_api.py backend/tests/test_migrations.py backend/tests/test_db_models.py -q
```

Result:

- `43 passed`

After the migration-ID fix:

```bash
python -m pytest backend/tests/test_migrations.py -q
```

Result:

- `1 passed`

Full backend suite rerun after the final changes:

```bash
cd backend && python -m pytest -q
```

Result:

- `168 passed, 5 skipped`

LLM-facing evaluation coverage:

```bash
python -m pytest backend/tests/test_conversation_memory_evals.py -q
```

Result:

- `5 passed`

### Automated frontend verification

Targeted workspace test during development:

```bash
cd frontend && npm test -- --run src/pages/session/SessionWorkspacePage.test.tsx
```

Result:

- `31 passed`

Full frontend test suite:

```bash
cd frontend && npm test
```

Result:

- `14 files passed`
- `78 tests passed`

Frontend lint:

```bash
cd frontend && npm run lint
```

Result:

- passed

Frontend production build:

```bash
cd frontend && npm run build
```

Result:

- passed
- Vite emitted an existing chunk-size warning for the main bundle, but the build completed successfully

### Browser and visual verification

I used the real Docker Compose stack:

- frontend: `http://127.0.0.1:8566`
- backend: `http://127.0.0.1:8565`

I verified the live app against an existing durable session at:

- session id: `8155bbd7-2de7-4d4c-a961-d35485225ed0`

Browser workflow I executed:

1. opened `/sessions/8155bbd7-2de7-4d4c-a961-d35485225ed0?stage=story_setup`
2. entered:
   - word count: `1800`
   - runtime: `14`
   - chapters: `4`
   - scenes: `10`
   - pacing note: `Keep each chapter ending calmer than it began.`
3. saved through the real UI
4. reloaded the page
5. confirmed the saved revision and all field values persisted
6. confirmed the API reflected the saved setup
7. captured desktop and narrow screenshots

Saved screenshots:

- `/Users/kevin/code/storyteller/.artifacts/webapp-qa/prompt-50-story-setup-desktop.png`
- `/Users/kevin/code/storyteller/.artifacts/webapp-qa/prompt-50-story-setup-mobile.png`
- `/Users/kevin/code/storyteller/.artifacts/webapp-qa/prompt-50-story-setup-form-desktop.png`
- `/Users/kevin/code/storyteller/.artifacts/webapp-qa/prompt-50-story-setup-form-mobile.png`
- `/Users/kevin/code/storyteller/.artifacts/webapp-qa/prompt-50-story-setup-form-desktop-crop.png`

What I visually verified:

- the saved-state summary cards render with calm, non-deceptive “guides, not guarantees” language
- the new approximate scene count field is present and labeled clearly
- the mobile layout keeps the form readable and the fields stacked in a usable order
- the story-setup save survives a reload and displays revision/save-state cues

Visual coverage limits:

- the desktop split-workspace screenshots naturally compress the form because the product keeps chat and workflow panes visible at once
- the mobile form screenshot is the clearest evidence of the input controls themselves

### Live infrastructure verification

I checked Compose service health with:

```bash
docker compose -f infra/compose/docker-compose.yml ps --format json
```

The stack was already running. During verification I also had to apply the new migration to the live Compose database:

```bash
./scripts/dev-compose.sh exec -T backend alembic upgrade head
```

This succeeded after I fixed the migration revision identifier.

### Linting limit discovered

Backend Ruff lint is not clean at repository baseline:

```bash
cd backend && python -m ruff check app tests
```

Result:

- failed

Reason:

- many unrelated pre-existing import-order and line-length violations outside prompt 50
- I did not broaden scope into repo-wide lint cleanup because it was not caused by this prompt and would have been a large unrelated edit set

## Evaluation suite added for LLM/prompt-facing work

I extended the existing evaluation file `backend/tests/test_conversation_memory_evals.py` rather than creating a second overlapping framework.

Named criteria and outcomes:

- `memory_preserves_scene_targets`
  - evidence: `test_eval_user_preferences_keep_runtime_and_guidance_notes`
  - outcome: pass
  - verified that durable memory summaries now include `about 9 scenes` alongside runtime, words, chapters, and guidance notes

- `intent_parser_prompt_receives_scene_targets`
  - evidence: `test_eval_intent_parser_prompt_uses_durable_memory_summary_sections`
  - outcome: pass
  - verified that the rendered prompt context includes `Story setup: 1600 words, 10 minutes, 2 chapters, about 7 scenes`

- `durable_memory_section_grounding`
  - evidence: existing assertions in `test_eval_intent_parser_prompt_uses_durable_memory_summary_sections`
  - outcome: pass
  - verified the prompt still contains `Story decisions`, `User preferences`, and `Unresolved questions` sections after the prompt-50 changes

## Wrong turns, dead ends, and gotchas

### 1. Alembic revision identifier was too long for the live schema table

The first version of the migration used:

- `20260402_01_story_setup_scene_count`

That exceeds the effective width of the live `alembic_version.version_num` column in this repo’s database history. The migration body ran, but version-table update failed with:

- `psycopg.errors.StringDataRightTruncation`

I fixed this by shortening the revision id to:

- `20260402_01_story_setup_scenes`

This was a real production-style failure that only showed up against the live Compose database, not the fresh ephemeral migration test.

### 2. The migration chain had already needed one correction earlier in the run

The new migration originally pointed at the wrong predecessor and effectively created a second head. I corrected `down_revision` to the actual current head:

- `20260401_04`

That issue was fixed before the frontend/UI verification phase.

### 3. Chat action application initially risked unintended clears

In the frontend chat-to-UI application path for `update_story_setup`, I initially defaulted missing extracted values with `?? null`. That would have converted “field omitted” into “clear the saved value,” which is wrong for partial updates.

I fixed this by passing extracted values through without forcing omitted fields to `null`, so the backend can preserve the difference between:

- omitted field
- explicit clear

### 4. Browser screenshots initially framed the wrong part of the page

My first desktop capture proved the workspace loaded, but it landed on the top of the session shell instead of the story-setup form. I recaptured with stage-anchored and form-anchored screenshots so the evidence actually showed the prompt-50 UI.

## Assumptions I made while working unsupervised

- I assumed the existing `story_setup` stage should reuse the workflow tool service instead of creating a one-off repository write path.
- I assumed `approximate_scene_count` belongs in the durable story-setup model rather than in a frontend-only draft state or generic JSON blob.
- I assumed the appropriate place for LLM-facing regression coverage was the existing `test_conversation_memory_evals.py` suite, not a brand-new evaluation harness.
- I assumed it was acceptable to use an existing durable Compose session for browser QA instead of creating a fresh session through the UI, because the acceptance criteria were about durability, revisitation, and expectation-setting rather than onboarding flow.
- I assumed the repo-wide Ruff failures were pre-existing baseline debt and should be reported rather than fixed as unrelated scope expansion.

## Commits created during the run

- `2729705` `feat(prompt-50): add story setup persistence api`
- `5108ec6` `feat(prompt-50): add story setup workspace form`
- `f1b6fb7` `test(prompt-50): cover story setup prompt grounding`

## Final state

Prompt 50 is complete end to end:

- backend persistence exists
- the stage has a real workspace form
- the copy clearly frames these values as flexible planning targets
- state is durable and survives reload
- chat/workspace update plumbing respects partial updates
- LLM-facing summaries and prompt context include the new scene-count signal
