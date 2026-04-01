# 71 — Audio Length Estimation Heuristics

Read `base_prompt.md` first and preserve all prior prompt work.

## Objective

Estimate how long the completed narration will be based on draft length and audio settings so the user has a realistic expectation before generation begins.

## Build
- Implement a heuristic that converts story length into estimated narrated runtime while accounting for speed settings and optionally chapter pauses.
- Show the estimate in the audio stage UI and update it when the user changes speed or when the story draft changes materially.
- Make the assumptions transparent and easy to adjust later.

## Deliverables

- Audio length estimation service
- UI display of estimated runtime
- Tests around the core estimate calculations

## Acceptance checks

- Users can see a plausible length estimate before committing to audio generation.
- The estimate updates when the main influencing inputs change.
- The UI labels the result as approximate.

## Notes

A good heuristic is enough; fake precision is not.

## Suggested commit label

`feat(prompt-71): audio length estimation`
