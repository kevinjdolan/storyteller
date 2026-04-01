# 59 — Planning Funnel End-to-End Test

Read `base_prompt.md` first and preserve all prior prompt work.

## Objective

Add an integration or end-to-end test that proves the workflow from genre selection through detailed outline works as one coherent funnel.

## Build
- Simulate or mock the necessary model calls to exercise genre selection, tone selection, brief capture, pitch generation, character generation, beat-sheet generation, and story setup.
- Assert that the session ends the flow with a usable structured outline and consistent stage state.
- Document what remains mocked and what is exercising real infrastructure.

## Deliverables

- Planning-funnel test
- Fixtures or mocks for model outputs
- Short test design note

## Acceptance checks

- A regression in the planning funnel would be caught before shipping.
- The test proves durable state evolves correctly across multiple stages.
- Mocks are realistic enough to exercise UI and backend assumptions.

## Notes

This test should feel close to the real product journey.

## Suggested commit label

`feat(prompt-59): planning funnel e2e test`
