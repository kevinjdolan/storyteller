# 75 — Audio Job Orchestration and Progress Events

Read `base_prompt.md` first and preserve all prior prompt work.

## Objective

Turn audio generation into a durable worker job with clear progress reporting just like composition.

## Build
- Create an audio job type with segment-by-segment progress, retries, failure handling, and final assembly status.
- Emit real-time progress events the frontend can use for bars, logs, and status text.
- Persist partial audio segment artifacts and mark the final compiled audio when ready.

## Deliverables

- Audio worker flow
- Progress event emission for audio
- Durable audio job records

## Acceptance checks

- Audio generation can survive browser refreshes and continue in the worker.
- The frontend can show which stage of audio generation is happening now.
- Partial outputs are durable for resume or debugging.

## Notes

Mirror the composition job model where it makes sense.

## Suggested commit label

`feat(prompt-75): audio job orchestration`
