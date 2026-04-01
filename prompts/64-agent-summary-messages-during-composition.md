# 64 — Agent Summary Messages During Composition

Read `base_prompt.md` first and preserve all prior prompt work.

## Objective

Have the agent periodically post compact chat summaries of what it is currently writing so the user can intervene meaningfully.

## Build
- Emit periodic chat-style assistant summaries describing the current segment, narrative direction, and any immediate thematic focus.
- Link these summaries to the composition progress so they arrive at meaningful checkpoints rather than random intervals.
- Ensure the summaries are grounded in actual generated work, not hallucinated meta-commentary.

## Deliverables

- Composition summary message logic
- Chat integration for summaries
- Checkpoint strategy for when summaries appear

## Acceptance checks

- The user can understand what the system is doing mid-stream.
- Summary messages help the user decide whether to interrupt or let it continue.
- Summaries are concise and tied to real progress.

## Notes

Think of these as narration of process, not filler.

## Suggested commit label

`feat(prompt-64): agent summary messages during composition`
