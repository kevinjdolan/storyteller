# Prompt 35 Summary: Chat Commands and Quick Actions

## What I changed and why

I added a small, explicit command surface to the session workspace so common chat-side actions no longer require free-form phrasing every time. The goal was to make the chat lane feel faster and more powerful without creating a second action system.

The resulting command set is intentionally narrow:

- `Next stage`
- `Summarize plan`
- `Regenerate pitches`
- `Pause writing`
- `Resume writing`

These now work in two discoverable forms:

- quick-action chips in the chat composer
- slash commands in the message box, such as `/next-stage` and `/plan`

I kept the existing action pipeline intact. Commands do not bypass the structured action schema or the policy engine. Instead, the client maps a quick action or slash command into the same `ChatToUiActionBatch` shape that the free-form intent parser already returns, and the backend evaluates that batch through the same policy service used for normal parsed chat messages.

## Architectural changes

### Frontend

I introduced a shared command mapping module at [frontend/src/features/session/chat/chatCommands.ts](/Users/kevin/code/storyteller/frontend/src/features/session/chat/chatCommands.ts). This is the single source of truth for:

- the supported command ids
- the slash aliases
- which quick actions are visible in the current workspace state
- how each command becomes a structured action batch

The workspace page now uses that module in both entry paths:

- quick-action button clicks
- slash-command detection in the chat composer

Both paths now funnel into one submission helper in [frontend/src/pages/session/SessionWorkspacePage.tsx](/Users/kevin/code/storyteller/frontend/src/pages/session/SessionWorkspacePage.tsx), which:

- appends the user message locally
- calls the backend chat-intent endpoint
- appends the assistant reply
- appends action echoes from the policy evaluation
- auto-applies the existing preview-only actions that were already supported (`navigate_to_stage` and `open_finalize_view`)

The chat pane UI in [frontend/src/features/session/chat/SessionChatPane.tsx](/Users/kevin/code/storyteller/frontend/src/features/session/chat/SessionChatPane.tsx) now renders:

- a compact quick-action strip
- a slash-command hint line
- the same submit-state/error handling for typed messages and quick-action clicks

Styling for the new command strip lives in [frontend/src/styles/index.css](/Users/kevin/code/storyteller/frontend/src/styles/index.css).

### Backend

I extended the chat-intent request contract in [backend/app/models/intent_parser.py](/Users/kevin/code/storyteller/backend/app/models/intent_parser.py) with an optional `explicit_command` payload.

That payload carries:

- `command_id`
- `source` (`slash_command` or `quick_action`)
- `proposed_actions`

I also added backend-side validation so the command id and action batch cannot drift apart. For example:

- `summarize_plan` must carry zero actions
- `next_stage` may only produce `navigate_to_stage`
- `pause_writing` must produce a composition `pause_job`
- `resume_writing` must produce a composition `resume_job`

In [backend/app/services/intent_parser.py](/Users/kevin/code/storyteller/backend/app/services/intent_parser.py), the service now has two modes:

- free-form mode: uses the Gemini-backed intent parser exactly as before
- explicit-command mode: skips the model call, builds a deterministic assistant response, and still runs the resulting action batch through the existing `SessionActionPolicyService`

This preserves the original architecture:

- one chat-intent endpoint
- one action schema
- one policy engine
- one event-log path for parsed chat activity

I updated the route in [backend/app/api/v1/routes/sessions.py](/Users/kevin/code/storyteller/backend/app/api/v1/routes/sessions.py) so it only initializes the parser adapter when a free-form message actually needs model parsing. Explicit commands now work even though they do not need the model at all.

## New abstractions and extension points

### Frontend command helpers

Examples from [frontend/src/features/session/chat/chatCommands.ts](/Users/kevin/code/storyteller/frontend/src/features/session/chat/chatCommands.ts):

- `buildSessionChatQuickActions({ snapshot, selectedStage })`
  Returns the context-aware quick-action list for the current workspace.

- `resolveSessionChatSlashCommand({ input, snapshot, selectedStage })`
  Detects slash commands like `/plan` or `/next-stage` and returns the explicit-command payload to send to the backend.

- `buildSessionChatQuickActionSubmission({ commandId, snapshot, selectedStage })`
  Converts a clicked quick-action chip into the same explicit-command payload used by slash commands.

Example:

```ts
const submission = resolveSessionChatSlashCommand({
  input: '/next-stage',
  snapshot,
  selectedStage: selectedStage.stage,
})

// submission.explicitCommand.proposed_actions.actions[0]
// => { action_type: 'navigate_to_stage', target_stage: 'story_setup', ... }
```

### Backend explicit-command contract

The chat-intent endpoint now accepts this shape:

```json
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
          "rationale": "Explicit command requested navigation to Tone.",
          "requires_confirmation": false,
          "extracted_values": {}
        }
      ]
    }
  }
}
```

That request still returns the normal `ParsedChatIntentResponse`, including `policy_evaluation`.

## Files touched

- [backend/app/api/v1/routes/sessions.py](/Users/kevin/code/storyteller/backend/app/api/v1/routes/sessions.py)
- [backend/app/models/__init__.py](/Users/kevin/code/storyteller/backend/app/models/__init__.py)
- [backend/app/models/intent_parser.py](/Users/kevin/code/storyteller/backend/app/models/intent_parser.py)
- [backend/app/services/intent_parser.py](/Users/kevin/code/storyteller/backend/app/services/intent_parser.py)
- [backend/tests/test_intent_parser_api.py](/Users/kevin/code/storyteller/backend/tests/test_intent_parser_api.py)
- [frontend/src/api/sessions.ts](/Users/kevin/code/storyteller/frontend/src/api/sessions.ts)
- [frontend/src/features/session/chat/SessionChatPane.tsx](/Users/kevin/code/storyteller/frontend/src/features/session/chat/SessionChatPane.tsx)
- [frontend/src/features/session/chat/chatCommands.ts](/Users/kevin/code/storyteller/frontend/src/features/session/chat/chatCommands.ts)
- [frontend/src/features/session/chat/chatCommands.test.ts](/Users/kevin/code/storyteller/frontend/src/features/session/chat/chatCommands.test.ts)
- [frontend/src/pages/session/SessionWorkspacePage.tsx](/Users/kevin/code/storyteller/frontend/src/pages/session/SessionWorkspacePage.tsx)
- [frontend/src/pages/session/SessionWorkspacePage.test.tsx](/Users/kevin/code/storyteller/frontend/src/pages/session/SessionWorkspacePage.test.tsx)
- [frontend/src/styles/index.css](/Users/kevin/code/storyteller/frontend/src/styles/index.css)

## Verification performed

### Automated tests and static checks

I ran these exact commands:

- `cd frontend && npm test -- --run src/features/session/chat/chatCommands.test.ts src/pages/session/SessionWorkspacePage.test.tsx src/features/session/chat/chatToUiActions.test.ts`
- `cd frontend && npm run build`
- `cd frontend && npm run lint`
- `pytest backend/tests/test_intent_parser_api.py backend/tests/test_action_policy_service.py`
- `ruff check backend/app backend/tests`

Results:

- Frontend targeted tests: pass
- Frontend build: pass
- Frontend lint: pass
- Backend targeted tests: pass
- Ruff: pass

### Browser and visual verification

I verified the live UI with the repo’s browser runner and captured screenshots at two viewports.

Desktop check:

- Command:
  `cd infra/compose && docker compose run --rm --no-deps browser npm run check -- --spec /workspace/.artifacts/webapp-qa/chat-commands.spec.json`
- Screenshot:
  [chat-commands-workspace.png](/Users/kevin/code/storyteller/.artifacts/webapp-qa/chat-commands-workspace.png)
- What I verified:
  - quick-action strip renders in the chat composer
  - slash-command hint text is visible
  - `Next stage` quick action can be clicked
  - the assistant reply appears
  - the workspace advances to the next stage in the main pane

Mobile-width check:

- Command:
  `cd infra/compose && docker compose run --rm --no-deps browser npm run check -- --spec /workspace/.artifacts/webapp-qa/chat-commands-mobile.spec.json`
- Screenshot:
  [chat-commands-mobile.png](/Users/kevin/code/storyteller/.artifacts/webapp-qa/chat-commands-mobile.png)
- What I verified:
  - quick actions remain visible at a narrow viewport
  - the command strip still fits as the chat pane stacks vertically

### LLM / prompt evaluation suite

Because this change touched LLM-facing chat behavior, I treated the backend explicit-command tests plus the existing free-form parser API test as the evaluation suite.

Criteria and outcomes:

- `free_text_parser_regression`: pass
  Covered by `test_parse_chat_intents_endpoint_returns_structured_actions_and_logs_audit_event`
  Outcome: free-form chat still returns structured actions and still logs the intent-parser audit event.

- `explicit_command_bypasses_parser`: pass
  Covered by `test_parse_chat_intents_endpoint_handles_explicit_commands_without_calling_the_parser`
  Outcome: explicit commands return structured results, still receive policy evaluation, and do not call the parser adapter.

- `summary_command_zero_actions`: pass
  Covered by `test_parse_chat_intents_endpoint_supports_summary_commands_with_no_actions`
  Outcome: `/plan` returns a deterministic assistant summary with zero proposed actions and no policy evaluation.

Suite result:

- 3 of 3 named criteria passed

## Wrong turns, dead ends, and gotchas

- I initially ran the frontend Vitest command from `frontend/` using repository-root file paths. Vitest reported “No test files found.” I corrected the paths to `src/...`.
- The normal Compose `backend` service is currently crashing for an unrelated local configuration issue in `secrets.yaml`. The error is:
  `gemini.api_key_name`, `gemini.project_name`, `gemini.project_number`, and `openai` are treated as extra inputs.
- Because of that unrelated backend crash, I could not use the stock Compose backend for browser QA. I worked around it by starting a temporary backend container on the Compose network with `STORYTELLER_SECRETS_FILE=` so the browser runner could still exercise the real frontend against the current backend code.
- `docker compose run browser ...` tried to start the broken `backend` service and collided with port `8565`, so the successful browser runs used `--no-deps`.

## Assumptions made while working unsupervised

- I kept the command set intentionally small instead of trying to expose every existing action type. That matched the prompt’s “small and relevant” requirement.
- I treated `summarize plan` as an informational explicit command that deliberately returns zero actions. It still goes through the chat-intent endpoint and event log, but there is nothing for the policy engine to evaluate.
- I used the currently previewed stage, not only the durable current stage, as the context for `/next-stage`. That makes the shortcut feel aligned with what the user is looking at in the main pane.
- I preserved the existing behavior where only preview/navigation actions are auto-applied in the frontend. Confirm-first commands like pause, resume, and regenerate still surface as policy-evaluated proposals rather than silently mutating durable state, because the workspace does not yet have a separate confirmation/apply UI for those actions.

## Remaining limits

- Non-navigation quick actions are still proposals, not one-click durable mutations. This is consistent with the current action-confirmation model, but it means `Pause writing`, `Resume writing`, and `Regenerate pitches` mainly reduce phrasing friction right now.
- The browser verification depended on a temporary backend container because the local Compose backend configuration is currently invalid. The application code itself tested cleanly, but the local infrastructure issue should still be fixed separately.
