# 69 — Composition Loop End-to-End Test

Read `base_prompt.md` first and preserve all prior prompt work.

## Objective

Add an integration or end-to-end test that proves segmented writing, streaming progress, interruption, and resume all work together.

## Build
- Simulate a composition job with mocked model outputs and verify that progress, chunk events, and final text land in durable state correctly.
- Test at least one interruption or rewrite path mid-composition.
- Assert that a resumed session shows the right latest story text and job state.

## Deliverables

- Composition-loop test
- Mock or fixture outputs for segments
- Documentation of what the test exercises

## Acceptance checks

- A regression in the most dynamic part of the app would be caught.
- The test covers durability plus live updates, not only static text generation.
- Resume behavior is verified under realistic circumstances.

## Notes

Keep the test scenario focused but real.

## Suggested commit label

`feat(prompt-69): composition loop e2e test`
