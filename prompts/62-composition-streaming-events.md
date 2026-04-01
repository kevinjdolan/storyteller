# 62 — Composition Streaming Events

Read `base_prompt.md` first and preserve all prior prompt work.

## Objective

Stream composition progress and text chunks to the frontend in a way that supports a live typewriter-style experience.

## Build
- Emit real-time events for segment start, chunk streamed, segment summary, overall progress, pause, rewrite, and completion.
- Choose chunk sizes and timing that make the text feel lively and faster than typical reading pace without overwhelming the UI.
- Persist enough progress metadata that the UI can recover after reconnect.

## Deliverables

- Real-time composition event emission
- Chunking strategy
- Reconnect/recovery behavior for streaming state

## Acceptance checks

- The frontend can display a live writing experience rather than only final text dumps.
- Chunk timing feels intentional and readable.
- A reconnecting client can recover the latest accepted state.

## Notes

Keep event names aligned with the real-time schema from earlier prompts.

## Suggested commit label

`feat(prompt-62): composition streaming events`
