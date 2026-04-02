# Background Music Mixing

The audio pipeline keeps narration generation and music mixing separate on
purpose.

## Curated music catalog

- The first version ships three local loopable `.wav` beds in
  `backend/app/data/background_music/`.
- The session stores only the selected `music_profile`, plus the user-facing
  `include_background_music`, `narration_volume`, and `music_volume` settings.
- When an audio job starts, the backend resolves those settings into a concrete
  mix plan and stores that plan in `audio_jobs.config_json`.

## Mix pipeline

1. Gemini TTS renders each narration segment to WAV.
2. The backend assembles a narration master WAV from the segment assets.
3. If background music is enabled, the backend writes the narration master to a
   debug artifact path and then runs `ffmpeg`.
4. `ffmpeg` loops the curated music bed, trims it to the narration duration,
   applies gain, ducks it under the voice with `sidechaincompress`, fades the
   bed out, and emits the final mixed WAV.

## Mapping rules

- `music_profile` chooses the curated track plus profile-specific ducking and
  fade defaults.
- `music_volume` maps to the music-bed gain before ducking.
- `narration_volume` maps to the narration gain before the final `amix`.
- If music is disabled, the final asset is the narration master without the
  post-processing mix step.
