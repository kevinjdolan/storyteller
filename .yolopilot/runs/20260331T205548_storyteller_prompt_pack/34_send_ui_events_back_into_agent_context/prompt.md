# 34 — Send UI Events Back Into Agent Context

Read `base_prompt.md` first and preserve all prior prompt work.

## Objective

Ensure the agent can see important UI-side changes so follow-up chat turns are grounded in the current session rather than stale assumptions.

## Build
- Whenever the user changes a structured field in the UI, record a normalized event that can be fed into later model prompts or summaries.
- Update the session snapshot and any rolling context summary used by the backend agent services.
- Make sure UI-originated edits can trigger downstream regeneration flags when appropriate.

## Deliverables

- Normalized UI event pipeline
- Session snapshot update logic
- Context summary update path

## Acceptance checks

- The agent can respond accurately after a user changes a field directly in the UI.
- UI-originated updates are durable and replayable.
- The context mechanism avoids re-reading the entire event history on every model call if practical.

## Notes

Do not rely on the browser alone as the source of truth.

## Suggested commit label

`feat(prompt-34): ui events to agent context`
