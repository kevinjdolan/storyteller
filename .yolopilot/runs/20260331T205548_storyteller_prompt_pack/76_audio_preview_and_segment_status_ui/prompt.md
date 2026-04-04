# 76 — Audio Preview and Segment Status UI

Read `base_prompt.md` first and preserve all prior prompt work.

## Objective

Show the user a trustworthy view of audio generation progress and allow spot-checking when useful.

## Build
- Build the audio stage UI with a progress bar, segment status list, estimated remaining work, and any ready-for-preview audio clips if available.
- Allow the user to inspect which narration segments are complete, pending, or failed.
- Keep the UI calm and understandable even while jobs are active.

## Deliverables

- Audio progress UI
- Segment status rendering
- Optional preview player for ready segments

## Acceptance checks

- The user can tell whether audio is queued, generating, mixing, failed, or done.
- Progress is detailed enough to inspire trust.
- Ready previews are clearly distinguished from the final compiled file.

## Notes

Use the same design language as composition progress.

## Suggested commit label

`feat(prompt-76): audio preview and segment status ui`
