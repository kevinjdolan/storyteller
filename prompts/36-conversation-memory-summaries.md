# 36 — Conversation Memory and Rolling Summaries

Read `base_prompt.md` first and preserve all prior prompt work.

## Objective

Create a compact memory mechanism so the system can retain story decisions and conversation context across long sessions without stuffing full chat history into every prompt.

## Build
- Implement a rolling session summary that captures current story decisions, unresolved questions, and user preferences at key checkpoints.
- Update the summary after meaningful events such as pitch selection, character selection, beat revisions, and composition interruptions.
- Store both the latest summary and any useful previous snapshots so debugging and replay stay possible.

## Deliverables

- Rolling summary service
- Summary update triggers
- Tests around summary correctness or basic coverage

## Acceptance checks

- Later model calls can stay grounded without receiving the entire raw chat log.
- The summary reflects the latest accepted decisions rather than stale drafts.
- A resumed session can restore context quickly.

## Notes

Summaries should be factual and structured, not flowery.

## Suggested commit label

`feat(prompt-36): conversation memory summaries`
