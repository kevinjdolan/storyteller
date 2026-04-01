# 67 — Diff and Compare UI for Rewrites

Read `base_prompt.md` first and preserve all prior prompt work.

## Objective

Give the user a practical way to compare rewritten story text against prior text before accepting changes.

## Build
- Build a simple compare view that shows old versus new text for a segment or highlighted diff regions.
- Allow the user to accept the rewrite, reject it, or keep exploring alternatives.
- Make the compare UI available from both the composition stage and later final review if practical.

## Deliverables

- Rewrite compare UI
- Accept/reject controls
- Backend support for selecting active text version

## Acceptance checks

- Users can understand what changed without reading two unrelated walls of text blindly.
- Accepting a rewrite updates the canonical text cleanly.
- Rejected rewrites do not pollute the live draft.

## Notes

Readable compare beats sophisticated compare.

## Suggested commit label

`feat(prompt-67): diff and compare ui`
