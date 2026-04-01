# 80 — Finalize Screen With Read and Listen Modes

Read `base_prompt.md` first and preserve all prior prompt work.

## Objective

Implement the final review stage where the user can read the finished story, listen to the audio, and confirm the session feels complete.

## Build
- Build the finalize stage UI with tabs or sections for reading the final story text and listening to the final audio.
- Show the final selected genre, tone, length settings, and generation status summaries in a compact review panel.
- Make the stage tolerant of partial completion so, for example, story text can be ready before audio is ready.

## Deliverables

- Finalize stage UI
- Read and listen surfaces
- Session completion summary panel

## Acceptance checks

- A user can consume the finished story directly in the app.
- The UI gracefully handles cases where audio is still processing or has failed.
- The final stage feels like a real finish line.

## Notes

Keep the reading experience calm and uncluttered.

## Suggested commit label

`feat(prompt-80): finalize screen read and listen`
