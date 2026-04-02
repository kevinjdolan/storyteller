# 26 — Main Pane Stage Scaffold

Read `base_prompt.md` first and preserve all prior prompt work.

## Objective

Create the main-pane scaffolding for the multi-stage story workflow without yet implementing every stage’s business logic.

## Build
- Render a stage navigator or progress indicator that shows the ordered workflow from genre selection through finalize.
- Create placeholder stage panels for each required step so the product flow is visible end-to-end.
- Support stage-aware routing or local navigation in a way that can coexist with durable backend stage state.

## Deliverables

- Stage navigator UI
- Stage placeholder views
- Stage-to-route or stage-to-panel mapping

## Acceptance checks

- Every required stage from the brief exists in the UI skeleton.
- The main pane makes it obvious which step the user is on.
- The navigation pattern can later support locked, unlocked, and revisitable stages.

## Notes

Keep the first stage scaffold thin but coherent.

## Suggested commit label

`feat(prompt-26): main pane stage scaffold`
