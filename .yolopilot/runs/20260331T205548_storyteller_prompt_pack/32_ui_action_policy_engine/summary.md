# Prompt 32 Summary: UI Action Policy Engine

## What I Changed And Why

I added a deterministic backend policy layer for proposed UI actions so Gemini can remain a proposal generator while the server stays the source of truth for whether a change is valid, whether it needs confirmation, and what downstream work it would invalidate.

The main product gap in the repo before this change was that prompt 31 could parse chat into typed UI actions, but nothing in the backend decided whether those actions were actually legal for the current session state. That meant impossible action sequences such as selecting a tone before a genre, editing story setup while composition was actively running, or opening finalize views with stale outputs would still look structurally valid. Prompt 32 closes that gap.

The implementation now supports four explicit policy outcomes:

- `accepted`
- `rejected`
- `requires_confirmation`
- `accepted_with_side_effects`

Each result also carries structured reasons and explicit side effects so both chat-driven workflows and future direct-UI mutation routes can explain what happened in a consistent way.

## Architectural Changes Across The Codebase

### New typed action-policy contract

Added `backend/app/models/action_policy.py`.

This file defines the public contract for policy evaluation:

- request wrappers for action batches with per-action `confirmation_granted`
- decision enums
- reason codes
- side-effect models
- evaluation response models

This gives the backend a stable response shape instead of returning ad hoc dictionaries from the service layer.

### New deterministic policy service

Added `backend/app/services/action_policy.py`.

This is the core of the feature. It:

- loads the durable session snapshot
- builds a simulated policy state from stage statuses, selected entities, active jobs, and ready assets
- evaluates actions in batch order so earlier accepted actions can satisfy later prerequisites
- resolves catalog and session resources from the database
- distinguishes between hard rejections and confirmation gates
- computes downstream invalidation side effects
- simulates accepted state changes in-memory so sequential batch evaluation is deterministic

Important rule categories implemented here:

- prerequisite stage completion checks
- prerequisite selection checks
- stale target-stage checks when an existing candidate set is no longer trustworthy
- job-state checks for pause/resume/start conflicts
- asset readiness checks for finalize and export actions
- confirmation escalation for auto-apply candidates when non-draft downstream stages, active jobs, or ready assets would be invalidated

### Session API surface

Updated `backend/app/api/v1/routes/sessions.py`.

Added:

- `POST /api/v1/sessions/{session_id}/actions/evaluate`

This endpoint evaluates proposed UI actions against the durable session state without calling Gemini and without mutating the session.

### Chat-intent response now includes policy evaluation

Updated:

- `backend/app/models/intent_parser.py`
- `backend/app/services/intent_parser.py`

The existing chat-intents route still returns parsed actions, but now also attaches `policy_evaluation` when the parse succeeded and produced actions.

That means the current chat flow can immediately tell the frontend which parsed actions are:

- valid and safe
- blocked by prerequisites
- waiting on confirmation
- valid but side-effecting

### Shared exports

Updated:

- `backend/app/models/__init__.py`
- `backend/app/services/__init__.py`

These now re-export the new policy types and service for the rest of the backend.

### Documentation

Updated:

- `docs/chat-to-ui-actions.md`
- `docs/README.md`

The docs now describe the policy evaluator, the new API endpoint, the decision vocabulary, and the reason/side-effect structure.

## Examples And Extension Points

### Evaluating a direct UI action

Example request to the new endpoint:

```json
{
  "actions": [
    {
      "confirmation_granted": false,
      "action": {
        "schema_version": 1,
        "action_type": "update_story_setup",
        "target_stage": "story_setup",
        "confidence": 0.84,
        "rationale": "The user asked for a shorter read-aloud target.",
        "requires_confirmation": false,
        "extracted_values": {
          "target_runtime_minutes": 8
        }
      }
    }
  ]
}
```

If composition is already in progress, the response can now say:

- decision: `requires_confirmation`
- reason code: `confirmation_required_due_to_side_effects`
- side effects:
  - invalidate `composition`
  - stop active composition job

### Using the policy engine from chat parsing

The existing parse response now includes a sibling `policy_evaluation` field. That lets the frontend show something like:

- parsed action: `update_story_setup`
- policy result: rejected because `beats` is incomplete

without having to invent its own rules client-side.

### Stable extension points

The main extension points for future prompts are:

- `SessionActionPolicyService._evaluate_action(...)`
  Add new action types or tighten rules without changing the API contract.
- `SessionActionPolicyService._build_stage_edit_side_effects(...)`
  Extend downstream invalidation, job-stop, or asset-supersession logic.
- `SessionActionPolicyEvaluationRequest`
  Already supports per-action confirmation state, which is useful for future UI confirm dialogs.
- `build_action_policy_request_from_batch(...)`
  Lets chat-intent flows turn a `ChatToUIActionBatch` into a policy request without duplicating wrapper logic.

## Exact Verification Work Performed

### Focused backend checks

Ran:

```bash
pytest backend/tests/test_action_policy_service.py backend/tests/test_action_policy_api.py backend/tests/test_intent_parser_service.py backend/tests/test_intent_parser_api.py -q
```

Result:

- `12 passed`

What this covered:

- missing prerequisite rejection for `select_tone`
- sequential batch evaluation where confirmed `select_genre` unlocks later `select_tone`
- confirmation escalation for story-setup edits that would invalidate active composition work
- confirmed acceptance with side effects
- audio-generation rejection when story text is not ready
- job-state rejection for invalid `resume_job`
- chat-intent responses including `policy_evaluation`
- API response shape for the new evaluation endpoint

### Lint / static verification

Ran:

```bash
ruff check backend/app backend/tests
```

Result:

- passed

### Broader backend regression suite

Ran:

```bash
pytest backend/tests -q
```

Result:

- `74 passed`
- `5 skipped`

### Browser checks / screenshots

None performed.

Reason:

- this prompt only changed backend policy logic, API responses, and docs
- there were no UI rendering, layout, styling, or interaction changes to verify visually

## LLM / Prompt Evaluation Suite

I did not change Gemini prompts, model selection, or provider wiring in this prompt. The only LLM-adjacent change was deterministic post-processing of parsed actions.

I treated the following tests as the evaluation suite for the LLM-facing integration point because they verify that parsed actions are now deterministically judged after parsing:

- `parsed_actions_receive_policy_evaluation`
  Outcome: pass
  Evidence: `backend/tests/test_intent_parser_service.py`
- `parsed_api_response_exposes_policy_decisions`
  Outcome: pass
  Evidence: `backend/tests/test_intent_parser_api.py`
- `invalid_model_proposals_are_blocked_by_server_prerequisites`
  Outcome: pass
  Evidence: parser tests plus `test_action_policy_service.py`
- `downstream_side_effects_are_explained_before_apply`
  Outcome: pass
  Evidence: `test_policy_escalates_story_setup_edits_when_an_active_composition_job_would_be_invalidated`
- `job_control_guardrails_remain_deterministic`
  Outcome: pass
  Evidence: `test_policy_rejects_resume_job_when_audio_job_is_not_paused`

Measured values:

- all named criteria passed
- no failing deterministic evaluations remained in the backend test suite

## Wrong Turns, Dead Ends, And Gotchas

- I initially only considered exposing the policy engine as a standalone endpoint. That would have satisfied the backend requirement, but it would have left the current chat-intents path unable to surface policy results. I changed course and threaded the same evaluator into `SessionIntentParserService` so the existing parse route now returns actionable policy output immediately.
- One test initially failed because the test helper merged `confirmation_granted=True` and then overwrote it with a dumped request payload containing `false`. That was a test-construction bug, not a service bug.
- The existing session aggregate exposes only the latest story asset, not all story asset kinds. That was not enough for precise export decisions like `.docx` readiness, so the policy service now queries ready asset kinds directly instead of relying only on the snapshot’s single “latest story asset”.
- The existing “beats” session helper used by parser tests does not create selected pitch, character-sheet, or beat-sheet rows even though some stage statuses are advanced. That means the new policy engine correctly rejects those parser proposals. This surfaced a real distinction in the repo between stage-status progression and selected-entity presence.

## Assumptions I Had To Make While Working Unsupervised

- I assumed direct UI callers will eventually send `confirmation_granted` per action instead of requiring a separate apply-only endpoint in this prompt.
- I assumed confirm-first actions that are true no-ops, such as re-selecting the already selected genre or tone, should be accepted immediately rather than forcing redundant confirmation.
- I assumed auto-apply candidates should be escalated to confirmation whenever they would invalidate non-draft downstream stages, stop active jobs, or supersede ready assets.
- I assumed finalize-reader access should require any ready story asset, while `.docx` download specifically requires a ready `story_docx` asset.
- I assumed prompt 32’s responsibility ends at deterministic evaluation, not durable mutation. The policy engine simulates accepted state transitions in-memory for batch determinism, but it does not yet persist changes.

## Files Most Relevant To Review

- `backend/app/models/action_policy.py`
- `backend/app/services/action_policy.py`
- `backend/app/api/v1/routes/sessions.py`
- `backend/app/services/intent_parser.py`
- `backend/tests/test_action_policy_service.py`
- `backend/tests/test_action_policy_api.py`
- `docs/chat-to-ui-actions.md`
