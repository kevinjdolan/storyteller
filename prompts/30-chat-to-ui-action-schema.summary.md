# Prompt 30 Summary: Chat-to-UI Action Schema

## What I changed and why

This prompt needed a stable, typed contract that a future intent parser can
emit before any model suggestion is allowed to mutate workspace state. I added
that contract in three places:

- Backend source of truth in `backend/app/models/chat_actions.py`
- Frontend mirror and runtime parser in
  `frontend/src/features/session/chat/chatToUiActions.ts`
- Reviewer and machine-readable docs in `docs/chat-to-ui-actions.md` and
  `docs/chat-to-ui-actions.schema.json`

The new schema covers the staged workflow the product brief requires:

- Navigation: `navigate_to_stage`
- Genre and tone: `select_genre`, `select_tone`
- Brief: `update_story_brief`
- Pitches: `regenerate_pitches`, `select_pitch`
- Characters: `select_character_sheet`, `refine_character_sheet`,
  `regenerate_character_sheet`
- Beats: `accept_beat_sheet`, `refine_beat_sheet`, `regenerate_beat_sheet`
- Story setup: `update_story_setup`
- Composition: `start_composition`, `pause_job`, `resume_job`,
  `redirect_composition`
- Audio: `update_audio_settings`, `start_audio_generation`, `pause_job`,
  `resume_job`
- Finalize: `open_finalize_view`, `download_asset`

Every action now carries the same envelope:

- `action_type`
- `target_stage`
- `confidence`
- `rationale`
- `requires_confirmation`
- `extracted_values`

That gives prompt 31 a concrete output shape to target and gives prompt 32 a
deterministic proposal object to validate.

## Architectural changes across the codebase

### Backend contract layer

`backend/app/models/chat_actions.py` is the new backend contract module.

- Added a discriminated union of proposed UI actions keyed by `action_type`
- Added typed `extracted_values` models per action
- Added default confirmation policy mapping with
  `get_chat_to_ui_action_default_policy(...)`
- Added structural validation for:
  - confirm-first actions trying to skip confirmation
  - missing structured values on actions that require them
  - job/stage mismatch for `pause_job` and `resume_job`
- Added `get_chat_to_ui_action_schema_bundle()` so the checked-in JSON schema
  is generated from the backend source of truth rather than hand-maintained

I also updated `backend/app/models/__init__.py` so later prompts can import the
new contract through the existing public model surface.

### Frontend mirror

`frontend/src/features/session/chat/chatToUiActions.ts` mirrors the backend
contract in TypeScript.

- Added frontend action/value types matching the backend model names
- Added `parseChatToUiActionBatch(...)` so future UI work can validate unknown
  payloads before rendering quick actions or suggested confirmations
- Added the same default policy map on the client to keep “confirm first”
  behavior aligned before prompt 32 adds the full policy engine
- Tightened number parsing so integer-only fields such as `pitch_index`,
  `revision_number`, `target_word_count`, and `chapter_count` do not drift from
  backend expectations

### Documentation and schema artifact

- Added `docs/chat-to-ui-actions.md` as the policy note requested by the prompt
- Added `docs/chat-to-ui-actions.schema.json` as the machine-readable schema
  bundle
- Updated `docs/README.md` to point reviewers at the new docs

The schema JSON is generated from the backend model function, not maintained
manually. That keeps docs drift testable.

## Examples and extension points

### Backend validation example

```python
from app.models import ChatToUIActionBatch

payload = {
    "schema_version": 1,
    "actions": [
        {
            "schema_version": 1,
            "action_type": "update_story_setup",
            "target_stage": "story_setup",
            "confidence": 0.81,
            "rationale": "The user asked for a shorter read-aloud target.",
            "requires_confirmation": False,
            "extracted_values": {
                "target_runtime_minutes": 10,
                "chapter_count": 3,
            },
        }
    ],
}

batch = ChatToUIActionBatch.model_validate(payload)
```

### Frontend parsing example

```ts
import {
  getChatToUiActionDefaultPolicy,
  parseChatToUiActionBatch,
} from './chatToUiActions.ts'

const batch = parseChatToUiActionBatch(serverPayload)

if (batch != null) {
  const firstAction = batch.actions[0]
  const defaultPolicy = getChatToUiActionDefaultPolicy(firstAction.action_type)
}
```

### Adding a new action later

To add a future action cleanly:

1. Add the backend `ChatToUIActionType` enum member
2. Add the backend `extracted_values` model and action model
3. Add the action to `DEFAULT_CHAT_TO_UI_ACTION_POLICIES`
4. Mirror the type and parser branch in `chatToUiActions.ts`
5. Regenerate `docs/chat-to-ui-actions.schema.json`
6. Add backend and frontend contract tests

That gives later prompts a predictable path instead of ad hoc JSON growth.

## Verification work performed

### Backend verification

Ran:

- `cd backend && pytest tests/test_chat_action_contracts.py -q`
- `cd backend && ruff check app tests && pytest tests/test_realtime_contracts.py tests/test_chat_action_contracts.py -q`

Results:

- `tests/test_chat_action_contracts.py`: 6/6 passing
- Combined contract regression run: 11/11 passing
- `ruff check`: passing

### Frontend verification

Ran:

- `cd frontend && npx vitest run src/features/session/chat/chatToUiActions.test.ts`
- `cd frontend && npm run lint`
- `cd frontend && npm run build`
- `cd frontend && npx prettier --check ../docs/chat-to-ui-actions.md ../docs/chat-to-ui-actions.schema.json`

Results:

- `chatToUiActions.test.ts`: 5/5 passing
- ESLint: passing
- TypeScript + Vite production build: passing
- Prettier check for the new docs artifacts: passing

### Browser, screenshots, and visual QA

None were run, intentionally.

- This prompt introduced no rendered UI, layout, styling, accessibility, or
  browser behavior changes.
- The work is pure contract/model/parser/documentation work.
- Because there was no visual surface change, browser screenshots would not
  have increased confidence meaningfully here.

## LLM and prompt evaluation suite

This prompt changed LLM-facing contract shape rather than prompt text or model
selection, so I added contract-focused evaluation tests instead of model-call
evals. The goal was to ensure future structured outputs have a safe, stable
shape before prompt 31 starts emitting them.

Evaluation criteria and outcomes:

- `stage_specific_discriminated_actions`: PASS
  - Backend validates a mixed batch of genre, beat, and audio-setting actions
  - Frontend parser accepts the same mixed batch
- `confirm_first_enforcement`: PASS
  - Confirm-first actions such as `select_genre` and `select_pitch` are rejected
    when `requires_confirmation` is false
- `missing_structured_values_rejected`: PASS
  - Actions like `update_story_setup` fail validation when no structured values
    are extracted
- `job_stage_alignment`: PASS
  - `pause_job` and `resume_job` reject mismatched `job_kind` and
    `target_stage`
- `schema_bundle_parity`: PASS
  - The checked-in `docs/chat-to-ui-actions.schema.json` matches the backend
    generated schema exactly
- `frontend_backend_mirror_parity`: PASS
  - The frontend mirror parses the same canonical action shapes the backend
    accepts, including action-type and target-stage narrowing

Measured outcomes:

- Backend evaluation tests: 6/6 passing
- Frontend evaluation tests: 5/5 passing

## Wrong turns, dead ends, and gotchas

- I initially let `extracted_values` inherit the same base model as the outer
  action envelope, which would have forced a nested `schema_version` inside
  every extracted payload. That made the schema noisier than necessary, so I
  corrected it before finalizing the frontend mirror.
- The first frontend parser draft accepted integer-only fields as generic
  numbers. That would have let payloads through on the client that the backend
  would reject. I tightened those fields to integer parsing.
- The first TypeScript implementation leaned too hard on object spreads from a
  generic base object. `tsc` widened `action_type`, `target_stage`, and
  `schema_version` enough to break discriminated-union assignability during the
  build. I fixed that by explicitly narrowing returned branches where needed.
- The checked-in schema file is large enough that manually maintaining it would
  be error-prone. I generated it directly from the backend schema bundle
  function and added a backend parity test so drift is caught automatically.

## Assumptions made while working unsupervised

- I treated selection actions, regenerate actions, and job-control actions as
  default `confirm_first` because they can invalidate downstream work or change
  accepted state in a way that is materially user-visible.
- I treated `navigate_to_stage`, `update_story_brief`, `update_story_setup`,
  `update_audio_settings`, `open_finalize_view`, and `download_asset` as
  default `auto_apply_candidate` actions, with the expectation that prompt 32
  can escalate them to confirmation when downstream invalidation or other state
  rules require it.
- I included finalize-stage actions now even though no finalize UI exists yet,
  because the acceptance criteria asked for action coverage across the required
  workflow stages.
- I did not add any API route, persistence change, or UI rendering integration
  yet because prompt 30 is specifically the contract layer; prompt 31 and prompt
  32 are better places for parser and policy execution wiring.

## Repository state notes

- I created a checkpoint commit on the current branch:
  - `f32e5a0` `feat(prompt-30): chat to ui action schema`
- I left unrelated prompt log files and prior prompt metadata untouched.
- This summary file was written after code changes and verification completed,
  per the prompt requirement.
