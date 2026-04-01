# 79 — Audio Pipeline Tests

Read `base_prompt.md` first and preserve all prior prompt work.

## Objective

Add coverage for narration segmentation, TTS integration boundaries, mixing, assembly, and progress reporting.

## Build
- Test the narration segmentation logic with representative story text and chapter structures.
- Mock the TTS provider adapter and verify worker job state transitions, retries, and asset creation.
- Add at least one test for final assembly and optional music mixing.

## Deliverables

- Audio pipeline test suite
- TTS adapter mocks or fixtures
- Test notes for what is mocked versus real

## Acceptance checks

- The audio pipeline has meaningful automated coverage before polish work begins.
- A failed segment or assembly step is visible in tests.
- The tests prove resumability and asset recording, not just happy-path bytes.

## Notes

This test surface is about reliability.

## Suggested commit label

`feat(prompt-79): audio pipeline tests`
