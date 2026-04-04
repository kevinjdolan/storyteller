# Prompt 74: Background Music Mixing Pipeline

## What I changed and why

I added an optional background-music pipeline for narration so the final audio can include a gentle curated bed without complicating raw TTS generation.

- Added a backend-owned curated music catalog with three first-party local tracks: `lullaby_piano`, `string_drift`, and `night_ambience`.
- Added deterministic settings-to-mix mapping so saved audio settings now produce a durable `music_mix` plan with narration gain, music gain, ducking parameters, fade-out timing, and track metadata.
- Added an ffmpeg-based post-processing mixer that combines the voice-only narration master with the selected music bed after TTS finishes.
- Persisted extra metadata on the final audio asset so the mixed output is auditable and reproducible later.
- Exposed the music catalog and mix preview through the session API so the frontend can explain what the chosen mix will do before rendering starts.
- Updated the audio settings UI to show backend-provided music guidance, recommended volume ranges, and the current persisted mix preview.
- Added docs, generated local music assets, automated tests, and browser QA coverage.

The main product reason for the shape of this change is to keep voice clarity as the first priority. TTS still generates a clean narration master first, and music remains an optional downstream processing step.

## Architectural changes across the codebase

### Backend domain and API

- `backend/app/models/audio_settings.py`
  - Added `AudioMixStrategy`.
  - Added `AudioMusicProfileOptionView` for frontend-safe catalog data.
  - Added `AudioMixPreviewView` for persisted, human-readable mix previews.
- `backend/app/services/audio_music.py`
  - New service that owns the curated catalog and translates `AudioSettingsView` into a durable `AudioMixPlan`.
  - Centralizes gain math, ducking defaults, recommended music-volume ranges, and serialization/deserialization for job config storage.
- `backend/app/services/audio_mixing.py`
  - New ffmpeg wrapper with `FfmpegAudioMixer`.
  - Mixes narration WAV bytes with the selected curated music track using gain control, sidechain ducking, fade-out, and a bounded output graph.
- `backend/app/services/audio_jobs.py`
  - Audio jobs now persist `config_json["music_mix"]` at job start.
  - Finalization now builds a voice-only narration master first, optionally stores that master as a debug artifact, then applies the mixer to produce the final deliverable WAV.
  - Final asset metadata now includes the mix strategy, track identity, gains, ducking settings, fade timing, narration-master path, and ffmpeg command.
- `backend/app/services/audio_settings.py` and `backend/app/services/sessions.py`
  - Session hydration and saves now return backend-owned music profile options and a persisted mix preview alongside the existing audio settings.
  - Stage detail text now includes the mix-plan summary when music is enabled.
- `backend/Dockerfile`
  - Installed `ffmpeg` so the backend and worker images can run the mixer inside Docker Compose.

### Music asset strategy

- Added `backend/app/data/background_music/README.md` and `generate_curated_music.py`.
- Generated three local WAV loop assets in `backend/app/data/background_music/`.
- Documented the first-version strategy and extension path in `docs/background-music-mixing.md`.

The current strategy is intentionally small and curated:

- Local checked-in WAV loops avoid any provider/runtime dependency for music in development.
- The catalog is code-defined, so product copy, recommended levels, and mix defaults stay aligned.
- The abstraction point is `BackgroundMusicTrackDefinition` plus `AudioMixPlan`, so moving to a DB-backed or object-storage-backed catalog later does not require frontend or job-flow rewrites.

### Frontend

- `frontend/src/api/sessions.ts`
  - Added typed support for `music_profile_options` and `mix_preview`.
- `frontend/src/features/session/AudioSettingsStage.tsx`
  - Replaced hardcoded assumptions with backend-provided catalog data when available.
  - Added “Music mix” guidance that explains bedtime use case, mix note, recommended volume range, and the current persisted mix preview.
  - Kept fallback options so the UI still renders safely if the backend response is older or partial.
- `frontend/src/features/session/AudioSettingsStage.test.tsx`
  - Added coverage for rendering backend-provided music catalog guidance.

## New abstractions and how to use them

### Build a mix plan from saved audio settings

```python
from app.models.audio_settings import AudioSettingsView, AudioMusicProfile
from app.services.audio_music import build_audio_mix_plan

settings = AudioSettingsView(
    include_background_music=True,
    music_profile=AudioMusicProfile.STRING_DRIFT,
    narration_volume=88,
    music_volume=18,
)

plan = build_audio_mix_plan(settings)
assert plan.should_mix is True
print(plan.summary)
```

Use this anywhere backend code needs a deterministic mapping from user settings to actual mix behavior.

### Run the post-processing mixer

```python
from app.services.audio_mixing import FfmpegAudioMixer

mixer = FfmpegAudioMixer()
result = mixer.mix(narration_wav_bytes, plan=plan)

mixed_wav_bytes = result.mixed_wav_bytes
print(result.output_duration_seconds)
print(result.ffmpeg_command)
```

This is the main extension point if we later add:

- more advanced mastering,
- alternate ducking strategies,
- different encoders,
- non-ffmpeg backends.

### Add a new curated track

Add another `BackgroundMusicTrackDefinition` entry in `backend/app/services/audio_music.py` with:

- the profile key,
- copy shown in the UI,
- asset filename,
- recommended volume range,
- base gain,
- ducking defaults,
- fade-out timing.

Then place the WAV asset in `backend/app/data/background_music/`.

### Durable job integration

Audio jobs now store the serialized plan in:

```python
job.config_json["music_mix"]
```

That means future worker retries or background processing changes can reconstruct the intended mix plan without depending on the current session snapshot.

## Key files touched

- `backend/app/services/audio_music.py`
- `backend/app/services/audio_mixing.py`
- `backend/app/services/audio_jobs.py`
- `backend/app/services/audio_settings.py`
- `backend/app/services/sessions.py`
- `backend/app/models/audio_settings.py`
- `frontend/src/features/session/AudioSettingsStage.tsx`
- `frontend/src/api/sessions.ts`
- `backend/app/data/background_music/`
- `docs/background-music-mixing.md`
- `tools/webapp-qa/examples/prompt-74-audio-music.spec.json`

## Verification performed

### Lint

Ran:

```bash
python -m ruff check backend/app/services/audio_mixing.py backend/tests/test_audio_mixing_service.py
```

Result:

- Pass

I also previously ran a broader `ruff check` over the changed backend model/service/test files while iterating.

### Backend tests

Ran:

```bash
cd backend && pytest tests/test_audio_music_service.py tests/test_audio_mixing_service.py tests/test_story_tools.py tests/test_session_service.py tests/test_session_api.py -k 'audio_settings or audio_mix or audio_music or audio_job_service_mixes_background_music_as_post_processing or save_audio_settings_endpoint_persists_durable_audio_preferences'
```

Result:

- `8 passed, 102 deselected in 1.49s`

Covered areas:

- catalog exposure,
- settings-to-mix mapping,
- ffmpeg command construction,
- missing-binary handling,
- durable audio job post-processing mix behavior,
- session audio settings save/hydration behavior,
- API response shape for audio settings.

### Frontend tests

Ran:

```bash
cd frontend && npm test -- --run AudioSettingsStage.test.tsx
```

Result:

- `1` test file passed
- `4` tests passed

Covered areas:

- save payload behavior,
- hydrated field rendering,
- backend-provided music guidance rendering.

### Frontend build

Ran:

```bash
cd frontend && npm run build
```

Result:

- Pass
- Existing chunk-size warning remains for the main frontend bundle after minification.

### Real ffmpeg smoke test in Docker

Because the host machine did not have `ffmpeg` installed, I verified the mixer inside the compose backend container.

Ran an inline Python smoke test through:

```bash
docker compose -f infra/compose/docker-compose.yml exec -T backend python - <<'PY'
# constructs 2.0s narration WAV, builds a mix plan, runs FfmpegAudioMixer
PY
```

Measured result:

- source duration: `2.0s`
- mixed duration: `2.0s`
- sample rate: `24000 Hz`
- channels: `1`
- sample width: `2 bytes`
- ffmpeg invoked: `True`

This confirmed the final graph both mixes successfully and preserves narration duration.

### Browser and visual verification

Started/used the live compose stack:

```bash
docker compose -f infra/compose/docker-compose.yml up -d --build postgres gcs backend worker frontend browser
docker compose -f infra/compose/docker-compose.yml ps
```

Browser QA spec:

- `tools/webapp-qa/examples/prompt-74-audio-music.spec.json`

Ran:

```bash
docker compose -f infra/compose/docker-compose.yml run --rm browser npm run check -- --spec ./examples/prompt-74-audio-music.spec.json
```

Assertions covered:

- audio workspace route loads,
- music-enabled state renders,
- `String drift` appears,
- `Music mix` help appears,
- recommended bed range text appears,
- persisted mix summary appears,
- toggling music off updates the visible state copy to “Narration will render without a background bed.” and “Music off”.

Screenshots captured:

- `.artifacts/webapp-qa/prompt-74-audio-music-on.png`
- `.artifacts/webapp-qa/prompt-74-audio-music-off.png`

Visual confirmation:

- The audio settings screen renders the new music guidance and mix summary.
- The background music switch visibly changes the UI state in the browser.
- The music style selector and music volume slider are present in the enabled state.

### Remaining verification limits

- I did not run a full end-to-end narration job against live Gemini TTS because that would require external provider calls and was outside the scope needed to validate the local mixing pipeline.
- I did not add waveform- or loudness-analysis assertions beyond duration/sample-format validation. Intelligibility is primarily protected here by low default music gains, conservative recommended ranges, and ducking configuration, plus the browser/API previews.

## LLM or prompt evaluation suite

No LLM-facing prompts, model routing, or eval logic changed in this task.

- Evaluation suite added: none
- Criteria: not applicable
- Measured outcomes: not applicable

## Wrong turns, dead ends, and gotchas

- My first ffmpeg graph combined looped music, `sidechaincompress`, and `amix` in a way that hung inside the Docker container. The issue was the boundedness of the graph, not the surrounding job code.
- My first fix changed `amix` to `duration=shortest`, which removed the hang but incorrectly shortened the final output to about `1.451s` for a `2.0s` narration sample.
- The final stable graph uses an explicit narration split, mixes against the voice stream as the authoritative duration, and applies an output trim.
- The host environment did not have `ffmpeg`, so real verification had to happen inside Docker Compose.
- The backend container image does not include tools like `ps`, so container debugging had to be done through inline Python/subprocess checks instead of familiar process-inspection commands.
- The browser runner logs a websocket warning for `/api/v1/sessions/events/ws` during QA. That did not block the static audio-stage verification or the saved/hydrated session rendering in the Vite dev environment.

## Assumptions made while working unsupervised

- A small checked-in curated music set is acceptable for the first version, even though later versions may move assets to object storage or a richer catalog source.
- Storing the voice-only narration master as a debug artifact alongside the mixed final output is acceptable because it materially improves traceability and future remix/debug workflows.
- WAV output is acceptable for the first mixed deliverable because the existing narration pipeline already emits WAV artifacts.
- The existing audio-stage QA session in the local database was safe to reuse for browser verification after seeding its audio settings through the local API.
- No user-uploaded music, licensing workflow, or per-track rights metadata was required for this prompt.

## Commit checkpoint

Implementation checkpoint commit created on the current branch:

- `35ee6f6` — `feat(prompt-74): background music mixing`
