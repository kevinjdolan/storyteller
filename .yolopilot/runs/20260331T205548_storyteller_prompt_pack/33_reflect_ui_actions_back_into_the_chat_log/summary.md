# Prompt 33 Summary: Reflect UI Actions Back Into the Chat Log

## What I changed and why

This prompt was about transcript trust: when the user changes the structured workspace directly, or when chat input causes a UI change, the conversation should still read like one coherent history instead of two drifting timelines.

I implemented that in two layers:

- The backend now exposes durable session history and a dedicated UI-action recording endpoint so direct UI actions can be stored as first-class history entries instead of temporary frontend-only messages.
- The frontend now rebuilds the transcript from durable session history when available, appends compact action echoes for direct UI actions, and appends action echoes for chat-driven actions that were actually applied to the workspace.
- The existing chat UI already supported a distinct `action_echo` role; this work now feeds that role with durable and deterministic data so action summaries are visually separated from normal assistant prose.
- I documented the compact-summary rules and extension points so later prompts can keep using the same mechanism instead of inventing one-off transcript messages.

The result is that a resumed session can show not only what the assistant said, but also what the user actually chose in the workspace and what chat messages actually changed.

## Architectural changes across the codebase

### Backend

- [`backend/app/api/v1/routes/sessions.py`](./backend/app/api/v1/routes/sessions.py) now exposes:
  - `GET /api/v1/sessions/{session_id}/history`
  - `POST /api/v1/sessions/{session_id}/ui-actions`
- [`backend/app/services/sessions.py`](./backend/app/services/sessions.py) now has `record_ui_action(...)`, which validates the session exists and records a durable history event.
- [`backend/app/services/event_log.py`](./backend/app/services/event_log.py) now has `build_event_view(...)` so history items and new UI-action responses use the same `SessionEventView` shape.
- [`backend/app/models/session.py`](./backend/app/models/session.py) now defines `RecordSessionUIActionRequest`, which keeps the endpoint payload explicit and typed.
- Backend tests were expanded in:
  - [`backend/tests/test_session_service.py`](./backend/tests/test_session_service.py)
  - [`backend/tests/test_session_api.py`](./backend/tests/test_session_api.py)

This backend slice matters because it moves action echoes from ad hoc UI state into durable event history. That is what lets replay and resume work cleanly.

### Frontend

- [`frontend/src/api/sessions.ts`](./frontend/src/api/sessions.ts) now exposes typed helpers for:
  - fetching session history
  - recording direct UI actions
  - parsing chat intent with typed policy results
- [`frontend/src/features/session/sessionQueries.ts`](./frontend/src/features/session/sessionQueries.ts) now provides `useSessionHistoryQuery(...)`.
- [`frontend/src/features/session/sessionWorkspaceContext.ts`](./frontend/src/features/session/sessionWorkspaceContext.ts) now exposes `useCurrentSessionHistoryQuery()` so workspace code can consume durable history alongside the snapshot query.
- [`frontend/src/features/session/chat/actionEchoes.ts`](./frontend/src/features/session/chat/actionEchoes.ts) is the new transcript-mapping layer. It:
  - rebuilds chat rows from durable session history
  - converts direct UI-action history into `action_echo` transcript entries
  - converts chat intent outcomes into compact action echoes for rejected or applied actions
  - intentionally skips duplicate “accepted preview” echo rows when the durable `ui.action.recorded` event will become the single source of truth
- [`frontend/src/pages/session/SessionWorkspacePage.tsx`](./frontend/src/pages/session/SessionWorkspacePage.tsx) now:
  - hydrates the chat pane from durable history when it exists
  - persists stage-navigation clicks as UI-action events
  - appends the returned action echo immediately into the live transcript
  - calls the chat intent parser on user messages
  - applies supported preview actions such as stage navigation and finalize-view opening
  - records those applied chat actions through the same UI-action persistence path so the transcript and workspace stay aligned
- Frontend tests were expanded in:
  - [`frontend/src/features/session/chat/actionEchoes.test.ts`](./frontend/src/features/session/chat/actionEchoes.test.ts)
  - [`frontend/src/pages/session/SessionWorkspacePage.test.tsx`](./frontend/src/pages/session/SessionWorkspacePage.test.tsx)

### Documentation and design rules

- [`docs/chat-action-echoes.md`](./docs/chat-action-echoes.md) is the new implementation note for this feature.
- [`docs/README.md`](./docs/README.md) now links that note from the docs index.

The design rules I documented and implemented are:

- Action echoes must be compact and informative, not mini assistant paragraphs.
- The summary should describe the change that actually happened, not just the intent that was parsed.
- Navigation echoes should name the destination explicitly, for example `Opened Audio in the main pane.`
- Rejections should explain why nothing changed.
- Action echoes should render through the distinct `action_echo` transcript role so they are visually scannable apart from assistant narration.

## Key files touched

- [`backend/app/api/v1/routes/sessions.py`](./backend/app/api/v1/routes/sessions.py)
- [`backend/app/services/sessions.py`](./backend/app/services/sessions.py)
- [`backend/app/services/event_log.py`](./backend/app/services/event_log.py)
- [`frontend/src/api/sessions.ts`](./frontend/src/api/sessions.ts)
- [`frontend/src/features/session/chat/actionEchoes.ts`](./frontend/src/features/session/chat/actionEchoes.ts)
- [`frontend/src/pages/session/SessionWorkspacePage.tsx`](./frontend/src/pages/session/SessionWorkspacePage.tsx)
- [`frontend/src/features/session/chat/actionEchoes.test.ts`](./frontend/src/features/session/chat/actionEchoes.test.ts)
- [`frontend/src/pages/session/SessionWorkspacePage.test.tsx`](./frontend/src/pages/session/SessionWorkspacePage.test.tsx)
- [`docs/chat-action-echoes.md`](./docs/chat-action-echoes.md)

## Examples of the new abstractions and extension points

### 1. Record a direct UI action as durable session history

Use the frontend helper in [`frontend/src/api/sessions.ts`](./frontend/src/api/sessions.ts):

```ts
await recordSessionUiAction(sessionId, {
  actionType: 'workspace.stage.opened',
  stage: 'audio',
  target: {
    type: 'stage',
    stage: 'audio',
  },
  summary: 'Opened Audio in the main pane.',
})
```

That produces a backend `ui.action.recorded` event and lets the transcript replay the same summary on reload.

### 2. Rebuild the chat transcript from durable session history

Use the history query plus the mapper in [`frontend/src/features/session/chat/actionEchoes.ts`](./frontend/src/features/session/chat/actionEchoes.ts):

```ts
const historyQuery = useCurrentSessionHistoryQuery()
const messages = buildSessionChatMessagesFromHistory(
  historyQuery.data,
  snapshot,
)
```

This is the main extension point for any future event type that should become visible in the chat pane.

### 3. Add support for a new echoed event type

Extend the event-to-chat mapping in `buildSessionChatMessagesFromHistory(...)` for durable history replay, and extend `buildIntentActionEchoMessages(...)` when the source is a chat-intent result that has not yet been materialized as a durable history event.

This split is intentional:

- durable history replay belongs in `buildSessionChatMessagesFromHistory(...)`
- temporary parse/result echoes belong in `buildIntentActionEchoMessages(...)`

That keeps reload behavior deterministic and avoids double-rendering accepted actions.

## Verification work performed

### Backend automated verification

- `pytest backend/tests/test_session_service.py backend/tests/test_session_api.py backend/tests/test_event_log_service.py -q`
  - Result: `18 passed`
- `ruff check backend/app backend/tests`
  - Result: passed
- `pytest backend/tests -q`
  - Result: `78 passed, 5 skipped`

### Frontend automated verification

- `npm --prefix frontend test -- --run SessionWorkspacePage actionEchoes sessionRuntimeStore SessionChatPane`
  - Result: `14 passed`
- `npm --prefix frontend test`
  - Result: `44 passed`
- `npm --prefix frontend run lint`
  - Result: passed
- `npm --prefix frontend run build`
  - Result: passed

### Browser and visual verification

I verified the UI behavior in Chromium through the running Docker Compose frontend and browser containers. Because the local backend container could not stay up due an unrelated `secrets.yaml` schema issue, I used request interception in the browser runner to exercise the real frontend route with controlled API responses.

Executed:

- `docker compose -f infra/compose/docker-compose.yml exec -T browser node /workspace/.artifacts/webapp-qa/prompt-33-qa.mjs`

What I verified in-browser:

- opening a session route renders the transcript with replayed history
- clicking a stage-nav item appends a compact action echo
- reloading the session keeps the prior echoed action visible through history replay
- sending a chat message that produces a supported navigation action updates the visible workspace
- the applied chat action also appends a compact action echo
- the Finalize stage heading becomes visible after the chat-driven navigation

Screenshot captured:

- `/Users/kevin/code/storyteller/.artifacts/webapp-qa/prompt-33-action-echoes-desktop.png`

### LLM and prompt evaluation coverage

I did not change prompt templates, model IDs, adapters, or provider wiring in this prompt. I did change the frontend consumption of chat-intent results, so I treated that as deterministic LLM-facing behavior and added regression coverage around the decision/output handling.

Evaluation criteria and outcomes:

- `history_replay_preserves_prior_ui_choices`
  - Outcome: pass
  - Evidence: `frontend/src/features/session/chat/actionEchoes.test.ts`
- `blocked_chat_action_reports_policy_outcome_concisely`
  - Outcome: pass
  - Evidence: `frontend/src/features/session/chat/actionEchoes.test.ts`
- `accepted_chat_navigation_updates_workspace_and_echoes_change`
  - Outcome: pass
  - Evidence: `frontend/src/pages/session/SessionWorkspacePage.test.tsx`
- `direct_ui_navigation_records_and_displays_action_echo`
  - Outcome: pass
  - Evidence: `frontend/src/pages/session/SessionWorkspacePage.test.tsx`
- `reloaded_session_replays_action_echo_in_browser`
  - Outcome: pass
  - Evidence: browser QA script plus screenshot

## Wrong turns, dead ends, surprising behavior, and gotchas

- I initially reached for the Odysseus-specific visual QA workflow before switching to the repo’s general webapp QA approach. That was the wrong fit for this repository.
- A full frontend test run exposed a robustness bug after the first implementation pass: `buildSessionChatMessagesFromHistory(...)` assumed `history.events` always existed. One of the broader tests exercised a thinner payload shape, so I added a guard that returns an empty replay list when the event array is missing instead of crashing.
- Restarting the Docker Compose backend exposed an unrelated local-environment issue: the current `secrets.yaml` contains keys the backend settings model rejects (`gemini.api_key_name`, `gemini.project_name`, `gemini.project_number`, and `openai`). That prevented end-to-end browser verification against the live backend, so I used browser-side API interception to keep visual verification moving.
- I briefly considered echoing both the “accepted chat action” preview and the later durable UI-action record as separate transcript rows. That created duplicate noise, so I changed course and kept the durable `ui.action.recorded` echo as the authoritative applied-action row.

## Assumptions I made while working unsupervised

- Stage navigation and finalize-view opening are the highest-value applied UI actions to wire first for this prompt, because they are visible, easy to validate, and central to transcript/workspace coherence.
- Existing durable selection and edit events should be replayed into the chat transcript instead of inventing a second persistence channel for them.
- Compact action echoes should stay as single-sentence summaries, not multi-line assistant commentary.
- If a chat intent is accepted but no supported UI change is actually applied in the current frontend, the transcript should not pretend that something changed.
- It is acceptable to use browser request interception for UI verification when the real frontend is running but the local backend is blocked by unrelated configuration.

## Remaining limits

- This prompt wires durable echoes for stage navigation and chat-applied navigation flows, plus replay of existing durable selection/edit events. It does not yet make every possible main-pane control emit its own dedicated `ui.action.recorded` entry.
- The browser verification was real UI verification, but not a live end-to-end backend verification because of the unrelated local `secrets.yaml` failure described above.
- The action-summary rules are documented and reusable, but future prompts may still want a small shared formatter layer if more UI controls start producing echoes.

## Commit checkpoints created during the run

- `0112c67 feat(prompt-33): add durable chat history endpoints`
- `3f481f2 feat(prompt-33): echo UI and chat actions in transcript`
