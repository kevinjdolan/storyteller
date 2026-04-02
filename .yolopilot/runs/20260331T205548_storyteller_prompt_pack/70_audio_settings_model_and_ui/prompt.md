# 70 — Audio Settings Model and UI

Read `base_prompt.md` first and preserve all prior prompt work.

## Objective

Implement the audio stage where the user can choose narration voice, background music behavior, playback speed, and other audio preferences.

## Build
- Create backend and frontend models for audio preferences such as voice ID, narration style, speed multiplier, music toggle, music style, and volume preferences.
- Build the audio settings stage UI with clear explanations of what each setting changes.
- Persist these settings as durable session state and reflect them in chat/action history when changed.

## Deliverables

- Audio settings data model
- Audio settings stage UI
- Persistence for selected audio options

## Acceptance checks

- The user can configure voice, music, and speed in one coherent place.
- Settings survive refresh and session resume.
- The product communicates that final runtime is estimated, not guaranteed.

## Notes

Keep the initial control set useful but not overwhelming.

## Suggested commit label

`feat(prompt-70): audio settings model and ui`
