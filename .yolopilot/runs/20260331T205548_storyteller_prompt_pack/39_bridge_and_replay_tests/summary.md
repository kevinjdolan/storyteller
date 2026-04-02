# Prompt 39 Summary: Bridge and Replay Tests

## What I changed and why

I added end-to-end-ish coverage around the currently shipped chat/UI bridge rather than inventing unimplemented workflow-application logic.

On the backend, I expanded `backend/tests/test_session_api.py` to cover:

- accepted chat navigation flowing through `POST /api/v1/sessions/:id/chat/intents`, then into a durable `ui.action.recorded` entry, then back out through `GET /api/v1/sessions/:id/hydrate`
- replay of a durable UI context edit into a resumed hydrated snapshot, including downstream invalidation state
- a negative path where a context update targets a valid editable stage but violates workflow prerequisites

To support that last case cleanly, I updated `backend/app/api/v1/routes/sessions.py` so `InvalidStageTransitionError` is returned as `409 Conflict` instead of surfacing as an internal error. That makes the rejection path explicit and testable.

On the frontend, I expanded `frontend/src/pages/session/SessionWorkspacePage.test.tsx` to cover:

- a rejected chat-derived action showing a durable action-echo style message without moving the visible workspace stage
- replay of `ui.action.recorded` and `content.user_edit.recorded` history into a resumed transcript, while the hydrated snapshot restores the latest saved stage detail into the editor

I also updated `frontend/src/app/router.test.tsx` so the router test harness mocks the current workspace hydration contract (`/hydrate`) instead of the older direct snapshot fetch. That was necessary to keep the broader frontend suite aligned with the current app architecture.

## Architectural impact

I did not add a new bridge service or new workflow mutation layer. The tests now explicitly validate the architecture that already exists:

1. chat message -> intent parsing / policy evaluation
2. accepted safe preview action -> durable UI action recording
3. UI-originated durable edit -> persisted snapshot changes plus invalidation rollups
4. hydration -> rebuilt recent history plus resumed snapshot state

The only production behavior change is the API-level conflict mapping for invalid stage transitions.

This keeps the codebase aligned with the existing separation of concerns:

- parsing and policy stay backend-owned
- safe preview auto-application stays frontend-owned
- durable state changes stay in session services
- replay/resume stays in hydration

## Examples and extension points

Representative accepted bridge flow now covered:

```http
POST /api/v1/sessions/:id/chat/intents
{
  "message": "/next-stage",
  "explicit_command": {
    "command_id": "next_stage",
    "source": "quick_action",
    "proposed_actions": {
      "schema_version": 1,
      "actions": [
        {
          "schema_version": 1,
          "action_type": "navigate_to_stage",
          "target_stage": "tone",
          "confidence": 1,
          "requires_confirmation": false,
          "extracted_values": {}
        }
      ]
    }
  }
}
```

Then:

```http
POST /api/v1/sessions/:id/ui-actions
{
  "action": "navigate_to_stage",
  "stage": "tone",
  "control_id": "chat-intent",
  "value_summary": "Tone",
  "origin": "chat"
}
```

Then hydration proves the durable bridge history is replayable:

```http
GET /api/v1/sessions/:id/hydrate
```

Representative rejection path now covered:

```http
POST /api/v1/sessions/:id/context-updates
{
  "target_kind": "stage_note",
  "stage": "story_setup",
  "values": {
    "detail": "Target a shorter read-aloud."
  }
}
```

Expected outcome: `409 Conflict` with a prerequisite-transition message.

If a future prompt adds a real backend action-application service for parsed chat actions, the new API tests are a good place to extend coverage from "parsed + recorded + replayed" to "parsed + applied + replayed".

## Verification performed

Targeted backend verification:

- `pytest backend/tests/test_session_api.py backend/tests/test_intent_parser_api.py backend/tests/test_intent_parser_service.py backend/tests/test_session_hydration_service.py`
- Result: `26 passed`

Targeted frontend verification:

- `npm test -- --run src/pages/session/SessionWorkspacePage.test.tsx src/features/session/chat/actionEchoes.test.ts src/features/session/sessionRuntimeStore.test.ts`
- Result: `17 passed`

Broader backend verification:

- `pytest backend/tests -m 'not integration'`
- Result: `106 passed, 5 deselected`

Frontend quality gates:

- `npm test`
- Result: `53 passed`
- `npm run lint`
- Result: passed
- `npm run build`
- Result: passed

Additional targeted check after repairing the router harness:

- `npm test -- --run src/app/router.test.tsx`
- Result: `5 passed`

Browser checks / screenshots:

- None performed
- Reason: this task changed tests and one API error mapping, not runtime UI rendering or styling
- Remaining limit: transcript/replay behavior was verified through React/Vitest integration tests rather than a live browser session

## Bridge verification criteria

No new LLM evaluation suite was added because no prompts, model wiring, or agent behavior changed.

The bridge-focused verification criteria covered by tests were:

- `accepted_chat_navigation_persists_history`: PASS
- `rejected_story_setup_change_stays_in_place`: PASS
- `ui_note_resume_replay_restores_snapshot_detail`: PASS
- `invalid_transition_returns_conflict`: PASS

## Wrong turns, dead ends, and gotchas

The main surprise was that the broader frontend suite was already stale around workspace loading.

`src/app/router.test.tsx` was still mocking `/api/v1/sessions/:id`, but the workspace route now loads `/api/v1/sessions/:id/hydrate`. That caused the router suite to fail with the existing "Workspace unavailable" screen even though the feature code was fine. I fixed the test harness so broader verification reflects the current contract.

I also checked for a generic backend "apply parsed chat action" endpoint before adding tests. It does not exist yet. Rather than fabricate one in prompt 39, I anchored coverage on the real shipped bridge:

- parser + policy evaluation
- frontend auto-apply of safe preview actions
- durable UI action recording
- durable context updates
- hydration replay

## Assumptions made while working unsupervised

- explicit commands such as `/next-stage` are acceptable representative chat messages for the accepted bridge path
- stage navigation remains preview-only by design and should not mutate backend `current_stage` / `resume_stage`
- the correct rejection semantics for invalid durable transitions are `409 Conflict`
- no live browser QA was required because the task did not modify production UI behavior

## Commit

Implementation checkpoint commit created on the current branch:

- `e741993` — `feat(prompt-39): bridge and replay tests`
