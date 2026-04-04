# 45 — Pitch Selection and Refinement via Chat

Read `base_prompt.md` first and preserve all prior prompt work.

## Objective

Let the user choose a pitch, request alternatives, or refine a pitch through chat without breaking the structured workflow.

## Build
- Connect pitch-related chat intents to the action pipeline so messages like ‘give me three more that are gentler’ or ‘take pitch two but make it about siblings’ work.
- Add UI affordances for selecting a pitch card or asking for another batch.
- Persist the selected pitch and any refinement rationale.

## Deliverables

- Pitch refinement actions
- Pitch selection persistence
- UI and chat wiring for alternatives/refinements

## Acceptance checks

- The user can refine the pitch both through direct UI clicks and through chat.
- Selecting or refining a pitch is reflected in the chat history.
- The final selected pitch becomes the durable source for later stages.

## Notes

Keep alternate batches linked to the same session rather than overwriting blindly.

## Suggested commit label

`feat(prompt-45): pitch refinement via chat`
