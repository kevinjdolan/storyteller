# 68 — Autosave Drafts and Partial Outputs

Read `base_prompt.md` first and preserve all prior prompt work.

## Objective

Persist partial story drafts during composition so crashes or reconnects do not destroy progress.

## Build
- Save accepted text snapshots and/or rolling draft artifacts during composition to durable storage.
- Record enough metadata to restore the latest stable draft view on session resume.
- Avoid excessive blob churn by choosing a sane autosave cadence or checkpoint strategy.

## Deliverables

- Autosave logic for composition
- Partial draft asset records
- Resume logic for latest stable text

## Acceptance checks

- A partially composed story can survive worker restarts or browser refreshes.
- Autosave does not create uncontrolled storage growth.
- The latest stable text is easy to reconstruct.

## Notes

Checkpointing strategy matters here.

## Suggested commit label

`feat(prompt-68): autosave drafts and partials`
