# Prompt 42 Summary: Story Setup Brief Form

## What I changed and why

I implemented the free-form story brief step end to end so the session can capture an open-ended bedtime story idea without forcing the user into a rigid questionnaire.

The new behavior covers three layers:

1. Backend persistence and API support for structured brief fields.
2. A dedicated workspace stage UI for drafting, previewing, and saving the brief.
3. Chat-to-UI support so accepted `update_story_brief` actions can save the same durable data path the form uses.

This closes the gap between tone selection and pitch generation with durable state instead of placeholder notes.

## Architectural changes across the codebase

### Backend

- Added explicit `story_brief` prompt fields to the durable model and migration:
  - `story_idea`
  - `desired_themes`
  - `key_images`
  - `audience_notes`
  - `must_have_elements`
- Kept `raw_brief` as the canonical composed text used downstream, but now build it from the structured fields when present.
- Added a dedicated story-brief save request/response contract and endpoint instead of overloading the generic context-update note path.
- Preserved revisioned brief behavior. Saving a brief creates a new active revision and invalidates downstream planning the same way other durable planning changes do.

Relevant backend files:

- `backend/app/services/sessions.py`
- `backend/app/api/v1/routes/sessions.py`
- `backend/app/models/session.py`
- `backend/migrations/versions/20260401_03_add_story_brief_prompt_fields.py`

Key implementation points:

- `backend/app/services/sessions.py:760`
  - Resolves new structured fields and composes canonical `raw_brief`.
- `backend/app/services/sessions.py:894`
  - Builds stage detail text as `Saved story brief: ...`.
- `backend/app/api/v1/routes/sessions.py:198`
  - Adds `POST /api/v1/sessions/{session_id}/story-brief`.
- `backend/app/models/session.py:238`
  - Validates that at least one brief field is populated.
- `backend/migrations/versions/20260401_03_add_story_brief_prompt_fields.py:20`
  - Adds the new nullable columns.

### Frontend

- Added a dedicated `StoryBriefStage` component instead of falling back to the generic note editor.
- The stage now gives the user:
  - A required free-form `Story idea` field.
  - Optional specificity cues for themes, images, audience notes, and must-have elements.
  - A planner-facing preview of the composed brief.
  - Save/reset behavior.
  - Revision and timestamp display when a brief already exists.
  - Locked-state handling when the session has not finished tone selection yet.
- Added a dedicated frontend API mutation for story brief saves.
- Centralized brief mutation/hydration/chat-echo routing inside `applyStoryBriefSave(...)` so direct UI edits and accepted chat actions use the same path.
- Extended chat action parsing and workspace auto-apply support so accepted `update_story_brief` actions now persist structured brief fields.

Relevant frontend files:

- `frontend/src/features/session/StoryBriefStage.tsx`
- `frontend/src/pages/session/SessionWorkspacePage.tsx`
- `frontend/src/api/sessions.ts`
- `frontend/src/features/session/chat/chatToUiActions.ts`
- `frontend/src/styles/index.css`

Key implementation points:

- `frontend/src/features/session/StoryBriefStage.tsx:58`
  - Hydrates form state from structured `story_brief` fields.
- `frontend/src/features/session/StoryBriefStage.tsx:68`
  - Composes the planner preview from structured fields.
- `frontend/src/features/session/StoryBriefStage.tsx:211`
  - Saves via `onSaveStoryBrief(...)`.
- `frontend/src/pages/session/SessionWorkspacePage.tsx:764`
  - Adds the shared `applyStoryBriefSave(...)` runtime mutation helper.
- `frontend/src/pages/session/SessionWorkspacePage.tsx:833`
  - Accepts and applies `update_story_brief` chat actions.
- `frontend/src/pages/session/SessionWorkspacePage.tsx:1205`
  - Mounts `StoryBriefStage` for the `brief` workflow step.
- `frontend/src/api/sessions.ts:50`
  - Extends `StoryBriefView` to include structured fields and `updated_at`.
- `frontend/src/api/sessions.ts:297`
  - Adds `SaveSessionStoryBriefRequest` and `saveSessionStoryBrief(...)`.
- `frontend/src/features/session/chat/chatToUiActions.ts:82`
  - Adds structured extracted values for `update_story_brief`.
- `frontend/src/styles/index.css:2068`
  - Styles the planner preview panel and composed-brief sections.

## New abstractions, helpers, and extension points

### 1. Backend story brief endpoint

Use:

```http
POST /api/v1/sessions/{session_id}/story-brief
Content-Type: application/json
```

Example request body:

```json
{
  "story_idea": "A sleepy child follows floating lanterns across a moonlit harbor to help an otter guardian guide them home.",
  "desired_themes": "Gentle courage, belonging, and a calm return home.",
  "key_images": "Floating lanterns, still water, and a warm harbor light.",
  "audience_notes": "For a sensitive five-year-old who likes rescue stories without villains.",
  "must_have_elements": "An otter friend and a restful final page.",
  "edit_mode": "replace",
  "origin": "workspace"
}
```

Why this matters:

- The backend keeps durable structured inputs.
- It still exposes a composed `raw_brief` for downstream planning code.
- Future UI variants can add or remove form fields without changing the durable mutation pattern.

### 2. Shared frontend brief mutation path

`frontend/src/pages/session/SessionWorkspacePage.tsx:764`

`applyStoryBriefSave(...)` now owns:

- request body shaping
- mutation call
- runtime snapshot hydration
- chat transcript echoing
- route preview advancement to the backend-reported current stage

That means new brief entry points can reuse one path instead of duplicating mutation + hydration logic.

### 3. Dedicated stage component

`frontend/src/features/session/StoryBriefStage.tsx`

The component accepts:

- `snapshot`
- `selectedStage`
- `onSaveStoryBrief(...)`
- `onPreviewStage(...)`

This keeps the stage-specific UI separate from the shared workspace shell and matches the repo’s direction for dedicated genre/tone stage components.

### 4. Chat action extension point

Accepted `update_story_brief` actions can now carry structured extracted values:

```json
{
  "action_type": "update_story_brief",
  "target_stage": "brief",
  "extracted_values": {
    "story_idea": "...",
    "desired_themes": "...",
    "key_images": "...",
    "audience_notes": "...",
    "must_have_elements": "...",
    "edit_mode": "replace"
  }
}
```

This is useful if prompt 43+ wants the intent parser to populate more specific brief fields instead of only a raw paragraph.

## Tests and verification

### Automated verification

#### Frontend

Command:

```bash
npm --prefix frontend test
```

Result:

- `14` test files passed
- `58` tests passed

Command:

```bash
npm --prefix frontend run lint
```

Result:

- Passed with `--max-warnings=0`

Command:

```bash
npm --prefix frontend run build
```

Result:

- Passed
- Vite production build completed successfully

#### Backend

Command:

```bash
cd backend && .venv/bin/python -m pytest tests/test_session_service.py tests/test_session_api.py tests/test_db_models.py tests/test_migrations.py tests/integration/test_data_layer.py -q
```

Result:

- `43 passed`
- `5 skipped`

Command:

```bash
cd backend && .venv/bin/python -m ruff check app tests
```

Result:

- Passed

### Added or expanded automated coverage

Frontend:

- `frontend/src/pages/session/SessionWorkspacePage.test.tsx`
  - Added a story brief save response builder and `/story-brief` fetch mock.
  - Added a UI save test for the brief stage.
  - Added a chat-driven accepted `update_story_brief` test.
  - Updated tone-selection expectations so a tone save transitions into an unsaved brief stage snapshot.
- `frontend/src/features/session/sessionRuntimeStore.test.ts`
  - Updated `StoryBriefView` fixture shape for `updated_at`.

Backend:

- Already added in the earlier backend checkpoint:
  - API tests for `/story-brief`
  - service tests for revision persistence and downstream invalidation
  - model and migration coverage for the new columns

### Browser and visual verification

I used the running Docker Compose frontend/browser workflow plus the compose-network backend alias already wired into the frontend proxy.

Live checks performed:

1. Confirmed the app and API were reachable at:
   - `http://127.0.0.1:8566`
   - `http://127.0.0.1:8565`
2. Seeded real sessions into the live stack by calling:
   - `POST /api/v1/sessions`
   - `POST /api/v1/sessions/{id}/selections/genre`
   - `POST /api/v1/sessions/{id}/selections/tone`
3. Filled the story brief in the browser and confirmed the session advanced to `pitches`.
4. Verified the saved story brief fields were present in the live hydrate response after save.

Screenshot artifacts:

- `/Users/kevin/code/storyteller/.artifacts/webapp-qa/prompt-42-story-brief-desktop.png`
- `/Users/kevin/code/storyteller/.artifacts/webapp-qa/prompt-42-story-brief-mobile-stage.png`
- `/Users/kevin/code/storyteller/.artifacts/webapp-qa/prompt-42-story-brief-after-save-stage.png`

What I visually verified:

- The brief stage renders as a dedicated stage, not the generic note editor.
- The mobile view shows the stage scaffold and the summary cards without collapsing into unusable controls.
- Saving the brief advances the live session from `brief` to `pitches`.

Visual verification limits:

- The clearest stage-specific capture is the mobile-stage artifact. The desktop full-page capture shows the whole stage, but it is dense because the page is tall.
- One intermediate desktop viewport framing pass clipped too much of the left lane; I kept the better artifacts and did not rely on that failed framing for sign-off.

### Live-data verification of the saved session

For the final seeded QA session `454f1ba4-6add-4525-b041-f297c80c92eb`, I confirmed via hydrate response that:

- `snapshot.current_stage == "pitches"`
- `snapshot.story_brief.story_idea` matched the saved free-form idea
- `snapshot.story_brief.desired_themes` matched the saved optional cue

## LLM / prompt / agent-facing evaluation coverage

No prompt text, model selection, or provider wiring changed in this prompt, so I did not add a new probabilistic eval harness.

I did add deterministic regression coverage for the LLM-facing bridge behavior that changed:

- `accepted_chat_story_brief_update_auto_applies`: PASS
  - Verified by `frontend/src/pages/session/SessionWorkspacePage.test.tsx:1731`
- `chat_story_brief_structured_fields_forwarded_to_mutation`: PASS
  - Verified by the same test asserting the outgoing request body
- `workspace_story_brief_ui_save_routes_to_pitches`: PASS
  - Verified by `frontend/src/pages/session/SessionWorkspacePage.test.tsx:1413`
- `story_brief_empty_payload_rejected_by_contract`: PASS
  - Covered by backend request validation in `backend/app/models/session.py:238` and exercised by backend API/service suites
- `story_brief_revision_builds_canonical_raw_brief`: PASS
  - Covered by backend session service tests added in the backend checkpoint
- `story_brief_change_invalidates_downstream_planning`: PASS
  - Covered by backend session service tests added in the backend checkpoint

## Wrong turns, dead ends, and gotchas

1. I initially tried frontend verification with `pnpm`, but the runner did not have a direct `pnpm` binary on `PATH`.
   - I switched to `npm --prefix frontend ...`, which matched the checked-in `package-lock.json` and worked.

2. The first version of `StoryBriefStage` used `event.currentTarget.value` inside state updater functions.
   - In tests, that caused pooled-event `null` access crashes.
   - I fixed it by reading `const value = event.currentTarget.value` before calling `setFormState(...)`.

3. The live backend behind the compose-connected frontend/browser flow was not fully migrated.
   - `POST /api/v1/sessions` returned `500` with `psycopg.errors.UndefinedColumn: column story_briefs.story_idea does not exist`.
   - I ran `alembic upgrade head` inside the running backend container to bring the live DB to `20260401_03`.

4. `docker compose up -d backend` could not start the declared backend service because port `8565` was already bound by an existing container named `storyteller-backend-override`.
   - That container already had the `backend` network alias the frontend proxy uses, so I reused it after upgrading its DB schema instead of forcing a port conflict resolution.

5. My first browser automation pass used inline here-doc scripts through `zsh`.
   - `zsh` history expansion mangled some `!` tokens, which made debugging slower than it should have been.
   - I replaced that approach with a throwaway artifact script under `.artifacts/webapp-qa/` and used that for the successful runs.

6. The first screenshot pass produced technically valid but poorly framed full-page images.
   - I iterated on the capture script and kept the clearer stage-oriented artifacts for reviewer use.

## Assumptions I made while working unsupervised

1. The workspace form should save with `edit_mode: "replace"` because the form represents the complete current brief draft rather than a partial append.

2. `story_idea` is the only required field, and the other structured brief cues should remain optional so the UI stays open-ended and not over-specified.

3. After a successful brief save, the workspace should preview whatever `snapshot.current_stage` the backend returns, which is `pitches` in the current stage progression logic.

4. Reusing the existing `storyteller-backend-override` container for browser QA was acceptable because:
   - it owned the active `8565` binding
   - it carried the `backend` network alias the compose frontend/browser already target
   - the alternative was leaving browser QA blocked behind a port collision

5. The `.artifacts/webapp-qa/` outputs are for verification evidence only and should not be treated as source changes to commit.

## Commit checkpoints created during development

- `0c7d6f3` `feat(prompt-42): add story brief backend persistence`
- `c074b62` `feat(prompt-42): add story brief workspace stage`

## Final state

The branch now has:

- durable backend support for structured story brief fields
- a dedicated story brief workspace stage with validation, preview, and save behavior
- chat auto-apply support for accepted `update_story_brief` actions
- automated coverage for UI save and chat save flows
- successful frontend and backend verification runs
- browser-based proof that a real brief can be entered and saved through the live app
