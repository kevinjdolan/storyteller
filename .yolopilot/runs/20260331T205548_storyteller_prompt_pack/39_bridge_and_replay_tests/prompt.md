# 39 — Bridge and Replay Tests

Read `base_prompt.md` first and preserve all prior prompt work.

## Objective

Add end-to-end-ish coverage around the chat/UI bridge and session replay before deeper workflow logic is layered on top.

## Build
- Test representative user messages turning into structured actions and then into durable state changes.
- Test that UI-originated changes appear in chat history and can be replayed into a resumed session snapshot.
- Add a few negative tests for invalid actions and rejected transitions.

## Deliverables

- Backend tests for the action pipeline
- Frontend or integration tests for action echoes
- Replay/resume coverage

## Acceptance checks

- The bridge behavior is proven before it becomes central to the product experience.
- A bad proposed action produces a clear rejection path.
- Replay and hydration logic are not left untested.

## Notes

These tests are about product integrity more than implementation detail.

## Suggested commit label

`feat(prompt-39): bridge and replay tests`
