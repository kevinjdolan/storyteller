# 85 — Audio Player With Hooks for Text Synchronization

Read `base_prompt.md` first and preserve all prior prompt work.

## Objective

Build the in-app audio playback experience and prepare for basic text/audio coordination where practical.

## Build
- Add an audio player UI with play, pause, seek, elapsed time, and playback speed controls for the final audio file.
- If the pipeline captures usable segment timestamps, expose lightweight hooks for syncing playback position to chapter or segment markers.
- Keep the player stable across page updates and reloads where possible.

## Deliverables

- Finalize-stage audio player
- Optional marker or segment sync support
- Playback state handling

## Acceptance checks

- The user can listen to the final story directly in the UI.
- Playback controls are straightforward and reliable.
- If text sync is only partial, the UI communicates that honestly.

## Notes

Basic stable playback is more important than fancy synchronized karaoke.

## Suggested commit label

`feat(prompt-85): audio player with text sync hooks`
