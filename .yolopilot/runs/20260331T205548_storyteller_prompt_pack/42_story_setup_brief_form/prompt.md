# 42 — Story Setup Brief Form

Read `base_prompt.md` first and preserve all prior prompt work.

## Objective

Implement the free-form story brief step where the user describes the kind of story they want to tell.

## Build
- Create the UI for the user to enter a free-form story idea, desired themes, key images, target audience notes, and any must-have elements.
- Persist the brief as durable session state, including revision history or at least last updated time.
- Show a concise summary or preview so the user can see the brief at a glance before moving on.

## Deliverables

- Story brief backend fields and endpoint
- Story setup stage UI
- Basic validation and save behavior

## Acceptance checks

- The user can provide an open-ended prompt rather than being forced into a rigid form only.
- The brief is durable and editable on resume.
- The UI encourages helpful specificity without overwhelming the user.

## Notes

This is the bridge between catalog selections and generative planning.

## Suggested commit label

`feat(prompt-42): story setup brief form`
