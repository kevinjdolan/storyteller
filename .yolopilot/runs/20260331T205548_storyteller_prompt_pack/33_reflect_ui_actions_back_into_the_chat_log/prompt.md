# 33 — Reflect UI Actions Back Into the Chat Log

Read `base_prompt.md` first and preserve all prior prompt work.

## Objective

Make UI changes and chat-driven actions visible inside the conversation so the user sees one coherent history of what happened.

## Build
- When a user clicks or changes something in the main pane, append a compact action message or summary into the chat history.
- When a chat message produces an applied action, add an action echo that explains what changed in the UI.
- Render these action echoes differently from normal assistant text so the history stays readable.

## Deliverables

- Chat action-echo rendering
- Backend or frontend event wiring for echoes
- Design rules for compact action summaries

## Acceptance checks

- The chat log and UI do not drift apart conceptually.
- A resumed session can show how a key choice was made even if it was made in the UI rather than typed.
- Action messages are concise and informative.

## Notes

This feature is about trust and coherence.

## Suggested commit label

`feat(prompt-33): action echoes in chat`
