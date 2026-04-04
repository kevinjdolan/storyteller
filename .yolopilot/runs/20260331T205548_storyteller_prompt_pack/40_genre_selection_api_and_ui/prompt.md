# 40 — Genre Selection API and UI

Read `base_prompt.md` first and preserve all prior prompt work.

## Objective

Implement the first real workflow step: selecting a genre from the curated catalog.

## Build
- Add a backend endpoint that returns the available genres with descriptions and any lightweight bedtime-safety notes.
- Build the genre selection stage UI with selectable cards, helpful descriptions, and a clear next-step path.
- Persist the selected genre durably and reflect the action in the session history and chat log.

## Deliverables

- Genre catalog endpoint
- Genre selection stage UI
- Persistence for the selected genre

## Acceptance checks

- The user can pick from the researched genre list rather than free-typing a genre from scratch.
- The selected genre survives page refresh and session resume.
- The UI makes it obvious that tone choices will be filtered next.

## Notes

Use the seeded catalog as the source of truth.

## Suggested commit label

`feat(prompt-40): genre selection api and ui`
