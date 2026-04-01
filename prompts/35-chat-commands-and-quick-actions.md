# 35 — Chat Commands and Quick Actions

Read `base_prompt.md` first and preserve all prior prompt work.

## Objective

Add a small set of explicit commands and shortcut actions that make the workspace feel powerful without hiding everything behind free-form chat.

## Build
- Support a few simple slash-style commands or quick action chips such as regenerate pitches, summarize current plan, pause writing, resume writing, or move to next stage.
- Make these commands resolve through the same action schema and policy engine as free-form messages.
- Keep the command list discoverable in the chat UI without overwhelming the user.

## Deliverables

- Quick action UI
- Optional slash command support
- Shared command-to-action mapping

## Acceptance checks

- Explicit commands reduce friction for common actions.
- The implementation reuses the structured action pipeline rather than bypassing it.
- The command surface is small and relevant.

## Notes

Commands should feel like conveniences, not a separate product.

## Suggested commit label

`feat(prompt-35): chat commands and quick actions`
