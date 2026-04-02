# 74 — Background Music Mixing Pipeline

Read `base_prompt.md` first and preserve all prior prompt work.

## Objective

Add optional background music handling so the final audio can include a gentle soundtrack when the user wants it.

## Build
- Define how music tracks are selected, stored, and associated with the session, even if the first version uses a small local curated set.
- Build a mixing step using a dependable backend toolchain such as ffmpeg to combine narration and music with volume ducking or simple gain control.
- Keep music optional and make sure voice clarity stays the priority.

## Deliverables

- Music asset strategy
- Backend mixing pipeline
- Settings-to-mix parameter mapping

## Acceptance checks

- The user can choose narration with or without background music.
- Mixed audio remains intelligible.
- Music handling works as a later processing step instead of complicating raw TTS generation.

## Notes

Start with a small, curated music surface.

## Suggested commit label

`feat(prompt-74): background music mixing`
