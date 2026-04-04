# 89 — Full Journey End-to-End Test

Read `base_prompt.md` first and preserve all prior prompt work.

## Objective

Add a comprehensive test that walks through the entire product from starting a session to downloading finished artifacts.

## Build
- Cover the full user journey: create session, pick genre/tone, enter brief, choose/refine pitch, choose/refine character sheet, review beat sheet, set story length, compose, configure audio, generate outputs, and finalize.
- Mock model-heavy operations where necessary but keep database, storage, job state, and UI navigation realistic.
- Assert that the final session has readable text, a docx asset, and an audio asset.

## Deliverables

- Full journey test
- Supporting fixtures and mocks
- Short note on current blind spots

## Acceptance checks

- The product can be exercised as one coherent system in automated form.
- The test proves artifact generation and session resumability assumptions.
- The biggest user-facing regressions would be caught.

## Notes

This is the confidence test for the whole app.

## Suggested commit label

`feat(prompt-89): full journey e2e test`
