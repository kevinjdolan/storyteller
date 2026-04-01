# Prompt 34 Summary: UI Events Back Into Agent Context

## What I changed and why

This prompt asked for a durable path from UI-side edits back into the backend agent context so later chat turns stop reasoning from stale state. I implemented that as a normalized `context-updates` pipeline instead of trying to infer UI changes from transient frontend state or re-read the full event log on every model call.

The core change is a new durable `stage_note` update flow:

- The frontend workspace now lets the user save a structured note for the currently selected editable stage.
- The backend accepts that note through a new `POST /api/v1/sessions/{session_id}/context-updates` endpoint.
- The session service normalizes the edit into a `content.user_edit.recorded` history event with durable `field_values` and a compact `summary_text`.
- The session snapshot now exposes `agent_context_summary`, which is rebuilt from snapshot state and latest durable detail rather than scanning all historical events.
- Intent parsing now consumes `snapshot.agent_context_summary` so later agent prompts see the latest UI-originated edits immediately.

This gives the agent a cheap, durable summary path while still preserving replayable raw events.

The prompt 34 code checkpoint is committed as:

- `356d40a` `feat(prompt-34): ui events to agent context`

## Architectural changes across the codebase

### 1. API and model contract

I added explicit request and response models for UI-originated context updates in [backend/app/models/session.py](/Users/kevin/code/storyteller/backend/app/models/session.py) and exposed them through [backend/app/api/v1/routes/sessions.py](/Users/kevin/code/storyteller/backend/app/api/v1/routes/sessions.py).

The new request shape is intentionally normalized:

```json
{
  "target_kind": "stage_note",
  "stage": "beats",
  "control_id": "stage-note-editor",
  "origin": "workspace",
  "values": {
    "detail": "Add a calmer lantern pause before the walk home."
  }
}
```

The response returns both:

- the updated `snapshot`, including `agent_context_summary`
- the newly recorded durable history `event`

That lets the UI update immediately without waiting for a second round trip.

### 2. Durable event pipeline

In [backend/app/services/sessions.py](/Users/kevin/code/storyteller/backend/app/services/sessions.py) I added `SessionService.apply_context_update(...)`.

That service method now:

- validates supported context-update targets
- updates the selected stage snapshot detail
- moves eligible draft or `needs_regeneration` stages back to `in_progress` when the edit is now the active work surface
- invalidates downstream stages when the edited stage should force regeneration
- records the normalized `content.user_edit.recorded` event
- returns an updated `SessionSnapshot`

I also extended [backend/app/services/event_log.py](/Users/kevin/code/storyteller/backend/app/services/event_log.py) and [backend/app/models/events.py](/Users/kevin/code/storyteller/backend/app/models/events.py) so replayable user-edit events can carry:

- `field_values`
- `summary_text`

That summary text is important because the chat replay layer can now use the exact durable wording that the backend authored, rather than re-inventing a UI echo from partial metadata.

### 3. Snapshot-backed agent context summary

I added [backend/app/services/agent_context.py](/Users/kevin/code/storyteller/backend/app/services/agent_context.py), which builds a concise session summary from snapshot state only.

That summary currently rolls up:

- session title
- overall, current, and resume stage
- selected catalog choices
- current structured outputs
- latest durable UI detail
- regeneration status
- active job status

This helper is now used in two places:

- snapshot construction in [backend/app/services/sessions.py](/Users/kevin/code/storyteller/backend/app/services/sessions.py)
- prompt assembly in [backend/app/services/intent_parser.py](/Users/kevin/code/storyteller/backend/app/services/intent_parser.py)

The result is that the intent parser can see a current summary without rehydrating the entire event log for every parse call.

### 4. Frontend workspace wiring

In [frontend/src/api/sessions.ts](/Users/kevin/code/storyteller/frontend/src/api/sessions.ts) I added the matching client contract and `applySessionContextUpdate(...)`.

In [frontend/src/pages/session/SessionWorkspacePage.tsx](/Users/kevin/code/storyteller/frontend/src/pages/session/SessionWorkspacePage.tsx) I added a new stage-note panel that:

- binds to the selected stage
- disables unsupported or locked stages
- saves durable note updates through the new backend route
- hydrates the returned snapshot directly into the runtime store
- appends the returned event into chat immediately
- refetches session history so replay stays consistent

I also updated [frontend/src/features/session/chat/actionEchoes.ts](/Users/kevin/code/storyteller/frontend/src/features/session/chat/actionEchoes.ts) so durable `summary_text` wins when replaying user-edit events into the chat transcript.

### 5. Documentation

[docs/event-taxonomy.md](/Users/kevin/code/storyteller/docs/event-taxonomy.md) now documents the richer `content.user_edit.recorded` payload and calls out that durable UI-side field edits should carry normalized `field_values` plus compact `summary_text`.

## New abstractions, helpers, and extension points

### `SessionService.apply_context_update(...)`

Use this for any UI-originated structured session edit that should become durable agent context.

Current supported path:

```python
result = SessionService(db_session).apply_context_update(
    session_id,
    payload=SessionContextUpdateRequest.model_validate(
        {
            "target_kind": "stage_note",
            "stage": "beats",
            "control_id": "stage-note-editor",
            "origin": "workspace",
            "values": {"detail": "Soften the midpoint and speed up the return home."},
        }
    ),
)
```

`result.snapshot.agent_context_summary` is ready to feed downstream prompt builders.

### `build_session_agent_context_summary(snapshot)`

Use this helper when another backend service needs a stable, cheap session summary and already has a `SessionSnapshot`.

Example:

```python
summary = build_session_agent_context_summary(snapshot)
```

If prompt 35+ adds more agent-facing entrypoints, they should prefer this summary over ad hoc truncation logic.

### `summary_text` on `content.user_edit.recorded`

If a future structured field editor needs a custom chat echo, set `summary_text` deliberately in the backend event payload. The frontend replay layer now respects it.

### Extension path for more UI controls

If a later prompt adds first-class structured editors beyond the generic note field:

1. Add a new `target_kind` and value model in [backend/app/models/session.py](/Users/kevin/code/storyteller/backend/app/models/session.py).
2. Extend `SessionService.apply_context_update(...)` in [backend/app/services/sessions.py](/Users/kevin/code/storyteller/backend/app/services/sessions.py).
3. Record normalized `field_values` and `summary_text`.
4. Surface the request and response types in [frontend/src/api/sessions.ts](/Users/kevin/code/storyteller/frontend/src/api/sessions.ts).
5. Let the UI consume the returned `snapshot` and `event` directly.

## Exact verification work performed

### Backend verification

- `ruff check backend/app backend/tests`
  - Result: pass
- `pytest backend/tests/test_event_log_service.py backend/tests/test_session_service.py backend/tests/test_session_api.py backend/tests/test_intent_parser_service.py -q`
  - Result: `25 passed in 1.20s`
- `pytest backend/tests -q`
  - Result: `82 passed, 5 skipped in 3.22s`

### Frontend verification

- `npm test -- --run SessionWorkspacePage actionEchoes`
  - Result: `9 passed`
- `npm test`
  - Result: `46 passed`
- `npm run lint`
  - Result: pass
- `npm run build`
  - Result: pass

### Browser and visual verification

Because the compose `backend` service is currently blocked by an unrelated local `secrets.yaml` schema mismatch, I did not modify `secrets.yaml`. Instead I ran a host-served QA stack with clean env overrides:

- host backend on `http://localhost:8565`
- host frontend on `http://localhost:9566`
- compose `browser` container driving the host frontend

I seeded a real session in Postgres, opened:

- `http://192.168.86.47:9566/sessions/78bfe213-8e54-42ff-b1c2-18fbf3ec6425?stage=beats`

Then I ran:

- `docker compose -f infra/compose/docker-compose.yml exec browser npm run check -- --spec /workspace/.artifacts/webapp-qa/prompt-34-stage-note.spec.json`

Result:

- pass
- screenshot captured at [prompt-34-stage-note.png](/Users/kevin/code/storyteller/.artifacts/webapp-qa/prompt-34-stage-note.png)

The browser spec verified:

- the workspace rendered the seeded session title
- the `Beat sheet note` editor was visible
- the existing saved detail was present
- saving a new note succeeded
- the chat transcript showed `Updated beat sheet notes from the workspace.`
- the new note text rendered back into the workspace

I also verified the persisted backend state immediately after the browser run:

- `GET /api/v1/sessions/78bfe213-8e54-42ff-b1c2-18fbf3ec6425`
  - `beats_detail` became `Add a calmer lantern pause before the walk home.`
  - `agent_context_summary` contained `Latest saved UI detail: Beat sheet: Add a calmer lantern pause before the walk home.`
- `GET /api/v1/sessions/78bfe213-8e54-42ff-b1c2-18fbf3ec6425/history`
  - latest event was `content.user_edit.recorded`
  - `field_values.detail` matched the saved note
  - `summary_text` matched the chat echo text

### Remaining verification limits

- I did not fix the compose `backend` container because its failure is caused by unrelated local `secrets.yaml` contents:
  - `gemini.api_key_name`
  - `gemini.project_name`
  - `gemini.project_number`
  - `openai`
- Browser verification therefore used a host-run backend/frontend pair against the same Postgres and fake GCS services instead of the compose `backend` service.

## LLM and prompt evaluation suite

This prompt touched LLM-facing context assembly through the intent parser, so I added and exercised targeted evaluation coverage rather than relying only on generic backend tests.

### Criteria and outcomes

- `Fresh UI Context Reaches Prompt Summary`
  - Coverage: [backend/tests/test_intent_parser_service.py](/Users/kevin/code/storyteller/backend/tests/test_intent_parser_service.py)
  - Outcome: pass
  - What it proves: a UI-originated beat-sheet edit is present in the rendered parser prompt summary

- `Context Update Persists Durable Replayable Event`
  - Coverage: [backend/tests/test_session_service.py](/Users/kevin/code/storyteller/backend/tests/test_session_service.py)
  - Outcome: pass
  - What it proves: `apply_context_update(...)` records `content.user_edit.recorded` with normalized `field_values` and `summary_text`

- `Downstream Regeneration Flags Update Correctly`
  - Coverage: [backend/tests/test_session_service.py](/Users/kevin/code/storyteller/backend/tests/test_session_service.py)
  - Outcome: pass
  - What it proves: editing an upstream completed stage invalidates downstream stages instead of leaving stale completions in place

- `API Contract Returns Updated Snapshot And Event`
  - Coverage: [backend/tests/test_session_api.py](/Users/kevin/code/storyteller/backend/tests/test_session_api.py)
  - Outcome: pass
  - What it proves: the frontend can apply the new route in a single round trip

- `Chat Replay Uses Backend Authored Summary Copy`
  - Coverage: [frontend/src/features/session/chat/actionEchoes.test.ts](/Users/kevin/code/storyteller/frontend/src/features/session/chat/actionEchoes.test.ts)
  - Outcome: pass
  - What it proves: replayed UI-edit events stay consistent with the backend event payload wording

- `Workspace Save Flow Updates Runtime State`
  - Coverage: [frontend/src/pages/session/SessionWorkspacePage.test.tsx](/Users/kevin/code/storyteller/frontend/src/pages/session/SessionWorkspacePage.test.tsx)
  - Outcome: pass
  - What it proves: the page hydrates the returned snapshot and appends the returned event after saving a stage note

## Wrong turns, dead ends, and gotchas

- I initially hit a frontend build failure after moving the stage-note state setup earlier in the component to satisfy hook ordering. The remaining issue was a closure over `selectedStage` inside `saveStageNote()`. I fixed it by keying the save path off the already-derived `selectedStageId` guard.
- My first browser run used `docker compose run --rm browser ...`, but that pulled compose dependencies and failed immediately because the compose `backend` service still cannot start with the current local `secrets.yaml`.
- My second browser attempt used `host.docker.internal`, but Vite rejected that host header because [frontend/vite.config.ts](/Users/kevin/code/storyteller/frontend/vite.config.ts) allows only `frontend`, `localhost`, and `127.0.0.1`. I switched the browser spec to the host machine’s LAN IP, which Vite accepted.
- The repo already had unrelated prompt 33 branch-local changes in:
  - `backend/app/ai/intent_parser.py`
  - `backend/app/models/action_policy.py`
  - `backend/app/models/chat_actions.py`
  - `backend/app/services/action_policy.py`
  - `backend/tests/test_action_policy_service.py`
  - `backend/tests/test_chat_action_contracts.py`
  - `backend/tests/test_intent_parser_adapter.py`
  - `prompts/33-action-echoes-in-chat.yolopilot.*`
  I left those untouched and committed only the prompt 34 code checkpoint.

## Assumptions made while working unsupervised

- I assumed the prompt’s “structured field” requirement could be satisfied for now by a normalized `stage_note` abstraction that is durable, replayable, and extensible, even though dedicated per-stage structured editors do not all exist yet.
- I assumed `genre`, `tone`, and `finalize` should remain unsupported for the generic note editor because those stages are selection-driven or terminal-review oriented in the current UI.
- I assumed it was safer to work around the broken local compose backend for verification than to mutate the user’s `secrets.yaml`.
- I assumed leaving existing prompt 33 branch-local changes alone was the right call, since they were not authored in this task and did not block prompt 34 delivery.

## Reviewer notes

The most important files to read first are:

- [backend/app/services/sessions.py](/Users/kevin/code/storyteller/backend/app/services/sessions.py)
- [backend/app/services/agent_context.py](/Users/kevin/code/storyteller/backend/app/services/agent_context.py)
- [backend/app/services/intent_parser.py](/Users/kevin/code/storyteller/backend/app/services/intent_parser.py)
- [frontend/src/pages/session/SessionWorkspacePage.tsx](/Users/kevin/code/storyteller/frontend/src/pages/session/SessionWorkspacePage.tsx)
- [backend/tests/test_session_service.py](/Users/kevin/code/storyteller/backend/tests/test_session_service.py)
- [backend/tests/test_intent_parser_service.py](/Users/kevin/code/storyteller/backend/tests/test_intent_parser_service.py)

Those cover the normalization path, snapshot summary path, prompt grounding path, and the user-visible save flow.
