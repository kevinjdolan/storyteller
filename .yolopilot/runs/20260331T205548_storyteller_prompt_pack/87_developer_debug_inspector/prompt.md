# 87 — Developer Debug Inspector

Read `base_prompt.md` first and preserve all prior prompt work.

## Objective

Add a hidden or developer-only inspector for session internals so it is easier to debug long AI-driven workflows.

## Build
- Create a developer surface that can show current session snapshot, plan revision, active jobs, recent events, and current artifact inventory.
- Gate it behind a development flag or route not intended for end users.
- Use it to make troubleshooting easier during future prompts.

## Deliverables

- Developer debug inspector
- Config flag for enabling it
- A short note explaining how to use it

## Acceptance checks

- Developers can inspect what the system thinks is true without manually querying the database.
- The inspector stays out of the main user experience.
- It helps explain failures in composition or audio generation.

## Notes

This is for trust during development, not for product polish.

## Suggested commit label

`feat(prompt-87): developer debug inspector`
