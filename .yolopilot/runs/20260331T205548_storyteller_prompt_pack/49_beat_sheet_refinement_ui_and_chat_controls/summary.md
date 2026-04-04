# Prompt 49: Beat Sheet Refinement UI and Chat Controls

## What I Changed

I implemented durable beat-sheet editing so the beat sheet behaves like a living plan instead of a one-shot generated artifact.

On the backend, I added a new beat edit contract and endpoint:

- `POST /api/v1/sessions/{session_id}/beats/edit`
- request model: `EditSessionBeatSheetRequest`
- response model: `SessionBeatSheetUpdateResponse`

This route updates the targeted beat sheet in place, records a durable `content.user_edit.recorded` event, appends a revision-local edit history entry, and invalidates downstream stages when the edited revision is the currently accepted one.

On the frontend, I replaced the previous beat stage shell with a fuller editing experience that now includes:

- a beat editor for top-level revision fields and per-beat fields
- durable save/reset controls
- visible change tracking history
- downstream refresh messaging when the selected beat plan changes
- synchronization with the chat/action-echo lane via the persisted history event

I also kept the existing chat-based refinement path intact. I did not add a brand-new chat action type; instead, direct structured editing now complements the already-supported `refine_beat_sheet` flow.

## Why These Changes Were Needed

Prompt 49 asked for three things that were missing:

1. A beat editor UI that exposes the ordered beat plan and lets the user tune it directly.
2. Backend actions that make those edits durable and safe.
3. Change tracking so downstream planning/composition knows when the accepted beat sheet has materially changed.

The main gap in the repo was that beat work was revision generation plus revision acceptance, but not true in-place shaping. This change closes that gap without introducing a new table or a migration-heavy rewrite.

## Architectural Changes

### Backend

I extended the beat sheet view model to carry direct-edit history:

- `backend/app/models/session.py`
- `BeatSheetEditView`
- `BeatSheetView.edit_history`
- request/response models for beat edits

I taught session hydration to read edit history out of the beat-sheet persistence payload:

- `backend/app/services/session_hydration.py`

I added the main editing flow to the session service:

- `backend/app/services/sessions.py`

Key behavior there:

- resolve the target beat sheet by `beat_sheet_id` or `revision_number`
- update top-level fields:
  - `summary`
  - `bedtime_notes`
  - `bedtime_goal`
- update per-beat fields:
  - `summary`
  - `emotional_intent`
  - `bedtime_softening_note`
- append `edit_history` into the existing `beat_sheets.beats` JSON payload
- emit a durable `content.user_edit.recorded` event
- invalidate downstream stages when the edited beat sheet is selected

I also updated the workflow invalidation graph so beat-sheet edits now mark `story_setup` stale in addition to later composition/audio/finalize work:

- `backend/app/models/workflow.py`

That change matters because story setup is downstream planning, and the accepted beat structure is part of what story setup is supposed to inherit.

### Frontend

I extended the session API client and beat-sheet types:

- `frontend/src/api/sessions.ts`

The main UI work happened in:

- `frontend/src/features/session/BeatSheetStage.tsx`

That component now supports:

- selecting which beat within a revision to edit
- editing top-level revision framing
- editing the selected beat’s summary, emotional intent, and bedtime softening note
- save/reset behavior
- edit-history rendering
- refresh warnings for accepted beat plans

I wired the new save flow into the workspace page:

- `frontend/src/pages/session/SessionWorkspacePage.tsx`

The workspace now:

- calls `editSessionBeatSheet(...)`
- hydrates the returned snapshot into the runtime store
- replays the returned durable event into the chat lane
- leaves the previewed stage stable instead of forcing a navigation jump

I also updated styling hooks for the editor and history presentation:

- `frontend/src/styles/index.css`

### Tests and Contracts

I expanded automated coverage across both the explicit edit flow and the changed invalidation graph:

- `backend/tests/test_session_beat_sheet_service.py`
- `backend/tests/test_session_api.py`
- `backend/tests/test_session_service.py`
- `backend/tests/test_workflow.py`
- `frontend/src/pages/session/SessionWorkspacePage.test.tsx`
- `frontend/src/features/session/workflowStages.test.ts`

## New Abstractions and Extension Points

### Durable beat edit API

Example usage:

```python
result = service.edit_beat_sheet(
    session_id,
    payload=EditSessionBeatSheetRequest.model_validate(
        {
            "beat_sheet_id": selected_id,
            "summary": "A calmer revision with a more wondrous midpoint.",
            "beat_updates": [
                {
                    "key": "midpoint",
                    "summary": "The midpoint trades urgency for lantern-lit awe.",
                    "emotional_intent": "Let this feel revelatory instead of sharp.",
                }
            ],
            "origin": "workspace",
        }
    ),
)
```

What you get back:

- a fully rehydrated session snapshot
- a durable history event for the edit
- updated `selected_beat_sheet.edit_history`

### Frontend beat edit transport

Example usage:

```ts
await editSessionBeatSheet(sessionId, {
  beat_sheet_id: selectedBeatSheet.id,
  revision_number: selectedBeatSheet.revision_number,
  bedtime_notes: 'Keep the midpoint luminous and the late turn sleepier.',
  beat_updates: [
    {
      key: 'midpoint',
      summary: 'The midpoint becomes a lantern-halo pause that trades urgency for wonder.',
    },
  ],
  origin: 'workspace',
})
```

### View-model support for history

`BeatSheetView` now exposes:

- `edit_history?: BeatSheetEditView[]`

Each history item carries:

- `summary_text`
- `origin`
- `changed_fields`
- `beat_keys`
- `material_change`
- `refreshes_downstream`
- `created_at`

That makes it easy to add future UI affordances like filtering, diffing, or separating workspace edits from chat-originated edits without another persistence refactor.

## Verification Performed

### Targeted automated verification

Ran:

- `pytest backend/tests/test_session_beat_sheet_service.py backend/tests/test_chat_action_contracts.py backend/tests/test_intent_parser_service.py backend/tests/test_intent_parser_adapter.py`
- `npm test -- src/pages/session/SessionWorkspacePage.test.tsx`

Results:

- backend targeted suite: passed
- frontend beat/workspace suite: passed

### Broader automated verification

Ran:

- `pytest backend/tests`
- `npm test`
- `npm run lint`
- `npm run build`

Results:

- backend full suite: `166 passed, 5 skipped`
- frontend full suite: `14 passed`, `76 passed`
- frontend lint: passed
- frontend build: passed

Build note:

- Vite emitted its existing large-chunk warning for the production bundle (`dist/assets/index-DIijN08F.js` over 500 kB after minification). The build still completed successfully.

### Browser and visual verification

I used the repo’s compose-based browser QA flow from `infra/compose`.

Environment checks:

- `odysseus --help` failed because the dedicated `odysseus` CLI is not installed in this environment.
- Fell back to the compose/browser workflow from the available skills.
- `docker compose ps --format json` from `infra/compose` confirmed the stack was already running and healthy.

I created a deterministic QA session directly through the live backend service layer using local stub generation services, then exercised the beat editor in the browser against that persisted session:

- QA session id: `8155bbd7-2de7-4d4c-a961-d35485225ed0`

Browser checks run:

- desktop interactive save spec:
  - `/Users/kevin/code/storyteller/.artifacts/webapp-qa/prompt-49-beat-editor-desktop.spec.json`
- mobile persisted-state spec:
  - `/Users/kevin/code/storyteller/.artifacts/webapp-qa/prompt-49-beat-editor-mobile.spec.json`
- desktop viewport capture spec:
  - `/Users/kevin/code/storyteller/.artifacts/webapp-qa/prompt-49-beat-editor-desktop-viewport.spec.json`
- mobile viewport capture spec:
  - `/Users/kevin/code/storyteller/.artifacts/webapp-qa/prompt-49-beat-editor-mobile-viewport.spec.json`

Generated screenshots:

- `/Users/kevin/code/storyteller/.artifacts/webapp-qa/prompt-49-beat-editor-desktop-before.png`
- `/Users/kevin/code/storyteller/.artifacts/webapp-qa/prompt-49-beat-editor-desktop-after.png`
- `/Users/kevin/code/storyteller/.artifacts/webapp-qa/prompt-49-beat-editor-mobile.png`
- `/Users/kevin/code/storyteller/.artifacts/webapp-qa/prompt-49-beat-editor-desktop-viewport.png`
- `/Users/kevin/code/storyteller/.artifacts/webapp-qa/prompt-49-beat-editor-mobile-viewport.png`
- `/Users/kevin/code/storyteller/.artifacts/webapp-qa/prompt-49-beat-editor-desktop-focused.png`
- `/Users/kevin/code/storyteller/.artifacts/webapp-qa/prompt-49-beat-editor-mobile-focused.png`

What I verified visually and functionally:

- the beat stage renders the new `Beat editor` and `Change tracking` sections
- a workspace-originated beat edit persists successfully
- the chat lane shows the returned durable edit summary
- the change-tracking area shows the new entry with origin and downstream-refresh badges
- accepted beat-sheet edits mark downstream stages as `Needs refresh`
- the editor remains readable on a narrow/mobile viewport

Visual coverage limits:

- the most informative captures for layout review were the focused editor screenshots; the plain viewport captures landed high in the workspace before I switched to a scroll-aware script
- I did not run a manual pixel-level diff between screenshots

## LLM / Prompt Evaluation Work

I did not modify prompt templates, model routing, or parser prompt text in this task.

Because of that, I did not add a new standalone LLM evaluation suite.

I still ran the existing chat- and intent-related regression coverage to make sure the beat-edit changes did not break chat-driven stage behavior:

- `backend/tests/test_chat_action_contracts.py`: pass
- `backend/tests/test_intent_parser_service.py`: pass
- `backend/tests/test_intent_parser_adapter.py`: pass

## Wrong Turns, Dead Ends, and Gotchas

### 1. Beat invalidation depth was initially too shallow

My first pass kept the existing beat invalidation graph: `composition`, `audio`, `finalize`.

The broader backend tests exposed that this was no longer correct once direct beat edits were introduced. Editing the accepted beat sheet should also invalidate `story_setup`, because story setup is downstream planning that depends on the accepted beats.

I fixed that by updating both backend and frontend workflow metadata, then aligning the API/service/workflow tests to the new graph.

### 2. The editor had a real React event-pooling bug

The first frontend test run crashed inside `BeatSheetStage`.

Cause:

- several editor `onChange` handlers referenced `event.currentTarget.value` inside a `setState` updater callback

That is unsafe once React releases the synthetic event. I fixed it by capturing `const nextValue = event.currentTarget.value` before entering the updater.

This was a real runtime bug, not just a test quirk.

### 3. Initial viewport screenshots were misleading

The first compose screenshots technically passed, but they mostly showed the top of the workspace rather than the beat editor section.

The root issue was that a plain viewport capture does not automatically scroll to the changed UI.

I corrected that by using a short Puppeteer script to scroll the live page to the `Beat editor` heading before capturing the focused desktop/mobile screenshots.

### 4. The new backend behavior affected existing context-update assumptions

Once beat edits started invalidating `story_setup`, some existing tests around beat-stage note edits and hydration replay had to be updated.

Those failures were useful; they confirmed the new stage graph was being applied consistently across:

- direct beat edits
- hydrated snapshots
- agent context summaries
- workflow helper tests

## Assumptions Made While Working Unsupervised

- I treated direct edits to the accepted beat sheet as material changes by default.
- I assumed `story_setup` should be considered downstream planning for beat changes and should be invalidated alongside composition when it already exists.
- I assumed chat-based beat shaping should continue through the existing `refine_beat_sheet` path instead of introducing a new chat action type for direct structured edits in this prompt.
- I assumed storing `edit_history` inside the existing beat-sheet JSON payload was preferable to adding a new relational table for this prompt, because it avoided a migration and still delivered durable history.
- I assumed visual QA should be fully local and deterministic, so I seeded a compose-backed QA session with stub generation services instead of relying on live provider-backed generation endpoints.

## Key Files Touched

- `backend/app/api/v1/routes/sessions.py`
- `backend/app/models/session.py`
- `backend/app/models/workflow.py`
- `backend/app/services/session_hydration.py`
- `backend/app/services/sessions.py`
- `frontend/src/api/sessions.ts`
- `frontend/src/features/session/BeatSheetStage.tsx`
- `frontend/src/features/session/workflowStages.ts`
- `frontend/src/pages/session/SessionWorkspacePage.tsx`
- `frontend/src/styles/index.css`
- `backend/tests/test_session_beat_sheet_service.py`
- `frontend/src/pages/session/SessionWorkspacePage.test.tsx`

## Final Repository State

I created a checkpoint commit for the production code changes on the current branch:

- `ce7254d` `feat(prompt-49): beat sheet refinement ui and chat`

The repository is left with the implementation changes committed, and this summary file written as the final action for reviewer handoff.
