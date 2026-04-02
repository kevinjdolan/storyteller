# Prompt 45 Summary: Pitch Selection and Refinement via Chat

Commit checkpoint: `dd7228ce348d7d414728d242336ada4fc52f3f8b` (`feat(prompt-45): pitch refinement via chat`)

## What changed and why

This prompt needed the pitch stage to behave like a durable collaborative workflow instead of a one-shot batch picker. The user can now:

- select a pitch from the UI or from parsed chat intents
- ask for more pitches without overwriting earlier pitch history
- refine an existing pitch from the UI or from parsed chat intents
- see pitch selections and refinements reflected in the chat transcript
- rely on the refined pitch as the durable selected source for later stages

The key behavior change is that pitch refinement is now a first-class workflow action rather than a variation of pitch regeneration. A refinement creates a new linked pitch batch, auto-selects the refined pitch, records why that refinement happened, and invalidates downstream planning in the same way a new accepted pitch should.

## Architectural changes

### Backend

- Added a first-class `refine_pitch` chat action to the shared chat-to-UI contract in `backend/app/models/chat_actions.py`.
- Added `RefineSessionPitchRequest` plus richer pitch snapshot fields in `backend/app/models/session.py` so snapshots now expose:
  - `generation_kind`
  - `source_pitch_id`
  - `source_pitch_title`
  - `refinement_instructions`
  - `selection_rationale`
- Added `POST /api/v1/sessions/{session_id}/pitches/refine` in `backend/app/api/v1/routes/sessions.py`.
- Implemented `SessionService.refine_pitch(...)` in `backend/app/services/sessions.py`.
  - Generates one refined candidate
  - Persists it as a new pitch row with a new `generation_key`
  - Stores batch/refinement metadata in `Pitch.model_output`
  - Marks the new pitch selected
  - Records both `ai.output.recorded` and `selection.recorded`
  - Advances the session to `characters`
- Extended hydration in `backend/app/services/session_hydration.py` so older and refined pitch batches can coexist and render correctly after reload.
- Extended `backend/app/services/story_tools.py` so chat-intent routing uses a dedicated `REFINE_PITCH` tool call instead of treating refinement as generic regeneration.
- Extended `backend/app/services/action_policy.py` so pitch refinement goes through deterministic prerequisite and confirmation checks like pitch selection does.
- Extended `backend/app/services/event_log.py`, `backend/app/models/events.py`, `backend/app/services/agent_context.py`, and `backend/app/services/conversation_memory.py` so the refinement rationale is durable and visible to later model steps.
- Updated LLM-facing prompt/config surfaces:
  - `backend/app/ai/intent_parser.py`
  - `backend/app/ai/prompts/pitch_generation.md`
  - `backend/app/models/intent_parser.py`
  - `backend/app/models/pitch_generation.py`

### Frontend

- Added refinement metadata and `refineSessionPitch(...)` to `frontend/src/api/sessions.ts`.
- Added a dedicated pitch refinement UI to `frontend/src/features/session/PitchSelectionStage.tsx`.
  - Choose a saved pitch as the refinement base
  - Enter refinement instructions
  - Submit a durable refinement request
  - Show refinement-specific badges and batch summaries
- Added pending confirmation UI in `frontend/src/features/session/chat/SessionChatPane.tsx`.
  - This fixes the confirm-first gap for pitch actions
  - Parsed chat actions that require confirmation no longer disappear silently
- Updated `frontend/src/pages/session/SessionWorkspacePage.tsx` to:
  - apply `refine_pitch` actions
  - queue confirm-first pitch actions in the chat lane
  - confirm or dismiss queued actions
  - keep chat echoes and workspace state in sync
- Updated `frontend/src/features/session/chat/actionEchoes.ts` and `frontend/src/features/session/chat/sessionChat.ts` so pitch refinement rationale shows up in transcript replay and current-session chat state.
- Added chat contract/frontend mirror updates in `frontend/src/features/session/chat/chatToUiActions.ts`.
- Added styling for the new pending confirmation panel in `frontend/src/styles/index.css`.

### Docs and schema

- Updated `docs/chat-to-ui-actions.md`
- Regenerated `docs/chat-to-ui-actions.schema.json`
- Updated `docs/story-workflow-tool-registry.md`

## New abstractions, helpers, and extension points

### `refine_pitch` chat action

The chat intent layer now has a dedicated action instead of overloading `regenerate_pitches`.

Example payload:

```json
{
  "schema_version": 1,
  "action_type": "refine_pitch",
  "target_stage": "pitches",
  "confidence": 0.94,
  "requires_confirmation": true,
  "extracted_values": {
    "pitch_index": 2,
    "instructions": "Make it about siblings who help each other settle down."
  }
}
```

### Durable pitch refinement endpoint

Example API call:

```http
POST /api/v1/sessions/{session_id}/pitches/refine
Content-Type: application/json

{
  "pitch_id": "pitch-123",
  "instructions": "Make it about siblings who help each other settle down.",
  "origin": "chat"
}
```

### Snapshot metadata for pitch lineage

Refined pitch history is exposed through `SessionSnapshot.pitch_batches` and `SessionSnapshot.selected_pitch`.

Example frontend usage:

```ts
if (snapshot.selected_pitch?.generation_kind === 'refinement') {
  console.log(snapshot.selected_pitch.source_pitch_title)
  console.log(snapshot.selected_pitch.refinement_instructions)
  console.log(snapshot.selected_pitch.selection_rationale)
}
```

### Frontend confirmation queue

`SessionWorkspacePage` now keeps pending confirm-first chat actions in local state and passes them into `SessionChatPane`.

This is reusable for later confirm-first actions beyond pitches, because the queue is action-type agnostic and the pane only needs:

- `pendingConfirmations`
- `onConfirmPendingAction`
- `onDismissPendingAction`

## Verification performed

### Backend verification

Ran targeted backend tests while building the feature:

```bash
cd backend
pytest tests/test_action_policy_service.py tests/test_chat_action_contracts.py tests/test_intent_parser_adapter.py tests/test_pitch_generation_service.py tests/test_session_api.py tests/test_session_service.py tests/test_story_tools.py
```

Result: `73 passed`

Ran the full backend unit suite:

```bash
cd backend
pytest
```

Result: `140 passed, 5 skipped`

Ran backend lint:

```bash
cd backend
python -m ruff check app tests
```

Result: `All checks passed!`

### Frontend verification

Ran targeted frontend tests for the changed chat and workspace surfaces:

```bash
cd frontend
npm run test -- src/features/session/chat/chatToUiActions.test.ts src/features/session/chat/actionEchoes.test.ts src/features/session/chat/SessionChatPane.test.tsx src/pages/session/SessionWorkspacePage.test.tsx
```

Result: `4 passed`, `33 passed`

Ran the full frontend unit suite:

```bash
cd frontend
npm run test
```

Result: `14 passed`, `65 passed`

Ran frontend lint:

```bash
cd frontend
npm run lint
```

Result: passed

Ran frontend production build:

```bash
cd frontend
npm run build
```

Result: passed

### Browser and visual QA

Used the live local app and the bundled Puppeteer runner through the existing browser container.

Seeded clean QA sessions via the live API, then ran:

```bash
docker exec storyteller-browser-1 bash -lc 'cd /workspace/tools/webapp-qa && npm run check -- --spec /workspace/.artifacts/webapp-qa/prompt45-ui-refinement.spec.json'
```

Browser assertions covered:

- pitch stage loads for a real session
- refinement UI is visible
- typing refinement instructions into the real textarea works
- clicking `Refine pitch` advances the session to the character stage
- the chat transcript reflects the refinement rationale
- reloading back to `?stage=pitches` shows the refined batch as the latest durable batch

Screenshots captured:

- `/Users/kevin/code/storyteller/.artifacts/webapp-qa/prompt45-ui-refinement-before.png`
- `/Users/kevin/code/storyteller/.artifacts/webapp-qa/prompt45-ui-refinement-after.png`
- `/Users/kevin/code/storyteller/.artifacts/webapp-qa/prompt45-ui-refinement-persisted.png`

Visual review notes:

- the new refinement panel renders correctly in the pitch stage
- the post-refinement transition to characters is visually intact
- after reload, the refined batch stays at the top of the pitch history and the refinement summary text is visible

### Verification limits

- I did not run a live browser chat-intent refinement flow end to end because that path depends on live LLM intent parsing and would make the browser check nondeterministic. That behavior is covered instead by backend tests plus frontend page tests for confirm-first chat actions.
- `make check` does not fully pass in this repository today because `backend-format-check` reports unrelated pre-existing Ruff formatting drift in files outside this prompt’s scope. I did not bulk-format those unrelated files just to satisfy the umbrella target.

## LLM and prompt evaluation coverage

This prompt changed LLM-facing behavior in both the intent parser and the pitch generation prompt, so I added/updated tests around those paths.

### Added or updated coverage

- `backend/tests/test_intent_parser_adapter.py`
  - verifies the intent-parser prompt contract now includes `refine_pitch`
  - verifies the prompt version bump to `intent_parser.v2`
- `backend/tests/test_pitch_generation_service.py`
  - verifies pitch model output now preserves `pitch_generation.v2`
  - adds a refinement fallback eval to ensure refinement-specific prompt context still produces a usable result when the provider fails

### Named evaluation criteria and outcomes

For the refinement fallback path, I ran the service directly and captured the `PitchBatchEvaluation` criteria returned by the backend:

- `candidate_count_matches_request`: pass, measured value `1`
- `all_required_fields_present`: pass, measured value `1`
- `titles_are_distinct`: pass, measured value `1`
- `hooks_are_distinct`: pass, measured value `1`
- `central_conflicts_are_descriptive`: pass, measured value `1`
- `why_it_fits_notes_are_grounded`: pass, measured value `1`

Overall result: `passed=True`

### Behavior assertions covered by tests

- refinement fallback keeps source-pitch identity visible in the refined title and fit note
- refinement fallback keeps the user guidance visible in the refined hook
- trivial-rewrite pitch batches still trigger heuristic fallback instead of being accepted as distinct options
- the checked-in chat action schema bundle matches the backend source of truth

## Wrong turns, dead ends, and gotchas

### 1. Refinement initially tripped the pitch prompt model

I first wired refinement as a one-candidate pitch generation call, but `PitchGenerationPromptContext` still enforced `candidate_count >= 2`. That broke both the API and service tests. I fixed it by making the prompt context accept one candidate for `generation_goal="refinement"` while keeping the multi-candidate requirement for normal alternative generation.

### 2. Hydration broke on mixed datetime awareness

Once refined pitches were being persisted, `build_pitch_batch_views(...)` started sorting a mixture of offset-aware and offset-naive timestamps and threw `TypeError: can't compare offset-naive and offset-aware datetimes`. I fixed that by normalizing timestamps with the existing hydration helper before comparing or sorting batch timestamps.

### 3. Confirm-first pitch actions were not actually actionable in the UI

The existing workspace could parse confirm-first actions, but there was no place in the chat lane to confirm them. Without adding that UI, `refine_pitch` and `select_pitch` chat actions would still feel broken even though the policy engine returned `requires_confirmation`. I added the pending confirmation panel rather than weakening the policy behavior.

### 4. Browser QA through `docker compose run` hit the wrong backend

Following the skill literally with `./scripts/dev-compose.sh run --rm browser ...` caused Compose to try to start the repo’s `backend` service, which currently exits because the Compose backend config rejects extra keys in the local `secrets.yaml`. The live app itself was already running against a different backend container, so I switched to `docker exec storyteller-browser-1 ...` against the existing browser container instead.

### 5. `make check` is not a reliable clean-room gate in the current repo

`make check` stopped at backend format-check because of unrelated repo formatting drift, including files I did not touch such as:

- `backend/app/ai/brief_normalization.py`
- `backend/app/models/story_tools.py`
- `backend/app/services/catalog.py`
- `backend/app/services/intent_parser.py`
- `backend/tests/test_brief_normalization_service.py`
- `backend/tests/test_db_models.py`
- `backend/tests/test_intent_parser_service.py`
- `backend/tests/test_session_hydration_service.py`

I fixed lint issues in the touched files and ran the explicit verification commands listed above instead of widening the diff with unrelated formatting churn.

## Assumptions made while working unsupervised

- A pitch refinement should create one refined candidate, not another full multi-card batch.
- Refining a pitch should auto-select the refined result and advance the workflow the same way selecting a pitch does.
- It is acceptable to persist refinement lineage and rationale inside existing `Pitch.model_output` JSON instead of adding a schema migration for this prompt.
- Earlier pitch batches should remain visible and linked to the same session instead of being overwritten.
- The right UX for confirm-first chat pitch actions is an inline pending-confirmation panel in the chat lane.
- Browser QA should prioritize deterministic UI refinement and reload persistence instead of relying on nondeterministic live LLM chat parsing.

## Reviewer notes

The highest-signal files for review are:

- `backend/app/services/sessions.py`
- `backend/app/services/session_hydration.py`
- `backend/app/services/action_policy.py`
- `backend/app/services/story_tools.py`
- `frontend/src/pages/session/SessionWorkspacePage.tsx`
- `frontend/src/features/session/PitchSelectionStage.tsx`
- `frontend/src/features/session/chat/SessionChatPane.tsx`
- `frontend/src/api/sessions.ts`

If I were extending this next, I would keep `refine_pitch` as the model for later “refine accepted artifact, preserve history, auto-select newest durable revision” flows in characters, beats, and eventually composition redirect/rewrite UX.
