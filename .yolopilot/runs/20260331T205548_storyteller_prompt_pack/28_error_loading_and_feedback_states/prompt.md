# 28 — Error, Loading, and Feedback States

Read `base_prompt.md` first and preserve all prior prompt work.

## Objective

Prepare the frontend to communicate progress and failure clearly before real asynchronous workflows arrive.

## Build
- Add skeletons, inline spinners, toast notifications, banner errors, and connection-state UI that match the product style.
- Create a consistent feedback pattern for retriable errors versus blocking errors.
- Add a simple error boundary around the workspace so unexpected crashes fail loudly but usefully.

## Deliverables

- Common feedback components
- Toast or notification layer
- Workspace error boundary

## Acceptance checks

- The app has a consistent way to report async state across screens.
- A failed API call does not leave the UI mysteriously blank.
- The error boundary makes debugging easier during development.

## Notes

Calm and clear beats flashy.

## Suggested commit label

`feat(prompt-28): error loading and feedback states`
