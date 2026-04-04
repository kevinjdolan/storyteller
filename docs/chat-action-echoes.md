# Chat Action Echoes

Prompt 33 adds a compact action-echo layer so the transcript reflects direct
workspace interactions and chat-driven UI changes without turning the left pane
into a noisy event dump.

## Summary Rules

- Prefer one short sentence per echo.
- Start with the outcome, not the source implementation.
- Use resolved UI labels such as `Audio` or `Beat sheet`, not raw IDs.
- Use past tense for applied UI changes:
  - `Opened Audio in the main pane.`
  - `Selected genre: Quest Fantasy`
- Use explicit blocker language for rejected chat actions:
  - `Couldn't update story setup yet. Finish Beat sheet first.`
- Use explicit confirmation language for gated actions:
  - `Needs confirmation before it can update story setup.`
- Use `Ready to ...` wording for chat actions that parsed cleanly but are not
  yet durably applied by the current workspace surface.
- Avoid duplicating the same applied action from two sources:
  - accepted chat actions that visibly move the UI should be represented by the
    durable `ui.action.recorded` event
  - `chat.intent.parsed` echoes are reserved for blocked, gated, or not-yet-applied
    outcomes

## Rendering Rules

- Action echoes render as `action_echo` transcript rows, not assistant prose.
- They should read like compact audit breadcrumbs rather than conversational replies.
- The transcript should stay readable when action echoes sit between full user
  and assistant messages.

## Current Wiring

- Durable replay comes from `GET /api/v1/sessions/{session_id}/history`.
- Direct workspace clicks persist through `POST /api/v1/sessions/{session_id}/ui-actions`.
- Chat submissions still go through `POST /api/v1/sessions/{session_id}/chat/intents`.
- The frontend rebuilds transcript echoes from durable history in
  `frontend/src/features/session/chat/actionEchoes.ts`.
