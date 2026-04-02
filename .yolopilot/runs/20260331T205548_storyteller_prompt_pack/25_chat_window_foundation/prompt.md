# 25 — Chat Window Foundation

Read `base_prompt.md` first and preserve all prior prompt work.

## Objective

Create the foundational chat UI in the left pane so later prompts can connect it to agent behavior and UI control.

## Build
- Build a chat message list, a message composer, timestamps, and basic message role styling.
- Support assistant, user, system, and action-echo message types from the start.
- Add loading and disabled states that will later reflect composition or audio work.

## Deliverables

- Chat pane components
- Message type rendering rules
- Composer component with submit handling

## Acceptance checks

- The chat pane feels like a real conversational surface, not a placeholder textarea.
- The UI can render multiple message roles cleanly.
- The message list is scrollable and stable under streaming updates later.

## Notes

Do not wire AI yet beyond mock or local state behavior if needed.

## Suggested commit label

`feat(prompt-25): chat window foundation`
