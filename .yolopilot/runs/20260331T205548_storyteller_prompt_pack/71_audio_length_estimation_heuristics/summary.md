# Prompt 71 Summary

Commit checkpoint: `0dbcfd6` (`feat(prompt-71): audio length estimation`)

## What I changed and why

I added a dedicated audio-length heuristic so the audio stage can show a plausible narration runtime before generation starts, and so that runtime can react immediately when the user changes playback speed.

The previous implementation reused the broader planning runtime heuristic and only returned a word-count-based duration band. It did not account for chapter pauses, and the UI only reflected the persisted snapshot instead of showing a live preview while the user adjusted speed. This task required a more explicit audio-focused estimate and a UI that makes the approximation transparent.

## Architectural changes across the codebase

### Backend

- Added a new service at [backend/app/services/audio_length_estimation.py](/Users/kevin/code/storyteller/backend/app/services/audio_length_estimation.py).
  - Centralizes audio runtime estimation behind `estimate_audio_length(...)`.
  - Uses the repo’s existing bedtime narration pacing defaults as the baseline.
  - Adds a configurable chapter-pause heuristic.
  - Rounds to 15-second buckets to avoid fake precision.

- Expanded [backend/app/models/audio_settings.py](/Users/kevin/code/storyteller/backend/app/models/audio_settings.py) so `AudioRuntimeEstimateView` now exposes:
  - `estimated_chapter_count`
  - `chapter_pause_count`
  - `chapter_pause_seconds`
  - `total_chapter_pause_seconds`
  - `assumed_words_per_minute`
  - `minimum_words_per_minute`
  - `maximum_words_per_minute`

- Updated [backend/app/services/audio_settings.py](/Users/kevin/code/storyteller/backend/app/services/audio_settings.py) to:
  - Build estimates via the new audio estimator.
  - Resolve chapter count from selected story setup first, then fall back to a selected chapter outline.
  - Include chapter-pause assumptions in stage detail text when relevant.

- Updated [backend/app/services/session_hydration.py](/Users/kevin/code/storyteller/backend/app/services/session_hydration.py), [backend/app/services/sessions.py](/Users/kevin/code/storyteller/backend/app/services/sessions.py), and [backend/app/services/conversation_memory.py](/Users/kevin/code/storyteller/backend/app/services/conversation_memory.py) so the richer estimate shape is carried consistently through session snapshot loading, audio-settings saves, and memory summaries.

### Frontend

- Expanded the API type in [frontend/src/api/sessions.ts](/Users/kevin/code/storyteller/frontend/src/api/sessions.ts) to match the richer backend payload.

- Added [frontend/src/features/session/audioEstimation.ts](/Users/kevin/code/storyteller/frontend/src/features/session/audioEstimation.ts).
  - Recomputes the estimate client-side from backend-provided assumptions.
  - Lets the UI preview unsaved playback-speed changes without another API call.
  - Keeps the frontend logic intentionally thin by consuming explicit backend assumptions instead of hardcoding hidden constants.

- Updated [frontend/src/features/session/AudioSettingsStage.tsx](/Users/kevin/code/storyteller/frontend/src/features/session/AudioSettingsStage.tsx) to:
  - Show `Approx.` labeling instead of a more precise-sounding duration.
  - Recalculate the estimate live as the speed slider changes.
  - Explain the estimate basis (`accepted draft text` vs `story setup target`) and the assumptions used.

### Tests

- Added backend coverage in [backend/tests/test_audio_length_estimation_service.py](/Users/kevin/code/storyteller/backend/tests/test_audio_length_estimation_service.py).
- Added frontend coverage in [frontend/src/features/session/audioEstimation.test.ts](/Users/kevin/code/storyteller/frontend/src/features/session/audioEstimation.test.ts).
- Updated UI/workspace fixtures in:
  - [frontend/src/features/session/AudioSettingsStage.test.tsx](/Users/kevin/code/storyteller/frontend/src/features/session/AudioSettingsStage.test.tsx)
  - [frontend/src/pages/session/SessionWorkspacePage.test.tsx](/Users/kevin/code/storyteller/frontend/src/pages/session/SessionWorkspacePage.test.tsx)

## New abstractions and extension points

### Backend estimator

Use the backend service directly when a future audio job, preview endpoint, or export flow needs the same heuristic:

```python
from app.services.audio_length_estimation import (
    AudioLengthEstimateInput,
    estimate_audio_length,
)

estimate = estimate_audio_length(
    AudioLengthEstimateInput(
        word_count=1800,
        playback_speed=0.95,
        chapter_count=3,
    )
)
```

Current default assumptions are intentionally centralized in one place:

- `140` assumed bedtime words per minute
- `120-160` words per minute typical range
- `3` seconds per chapter break
- `15` second duration rounding

If product wants a different pause model or a different rounding bucket later, [backend/app/services/audio_length_estimation.py](/Users/kevin/code/storyteller/backend/app/services/audio_length_estimation.py) is the place to change it.

### Frontend preview helper

Use the frontend helper when the UI needs an unsaved preview from a persisted estimate:

```ts
const preview = deriveAudioRuntimeEstimatePreview(
  snapshot.audio_settings?.runtime_estimate,
  formState.playbackSpeed,
)
```

This helper only works because the backend now returns the assumptions explicitly. That keeps backend and frontend responsibilities clean:

- Backend decides the heuristic inputs and assumption values.
- Frontend only previews the effect of local playback-speed edits.

## Verification performed

### Automated backend verification

- `pytest backend/tests/test_audio_length_estimation_service.py -q`
  - Result: `4 passed`
- `pytest backend/tests/test_session_service.py -k audio_settings -q`
  - Result: `1 passed, 29 deselected`
- `pytest backend/tests/test_session_api.py -k audio_settings -q`
  - Result: `1 passed, 40 deselected`
- `pytest backend/tests/test_audio_length_estimation_service.py backend/tests/test_session_service.py backend/tests/test_session_api.py backend/tests/test_session_hydration_service.py -q`
  - Result: `77 passed`

What these covered:

- core duration math
- playback-speed scaling
- chapter-pause inclusion
- story-setup-target basis
- composition-segment basis
- session snapshot hydration
- audio-settings persistence/API behavior

### Automated frontend verification

- `npm --prefix frontend test -- --run AudioSettingsStage.test.tsx audioEstimation.test.ts SessionWorkspacePage.test.tsx`
  - Result: `3 passed files, 37 passed tests`
- `npm --prefix frontend run build`
  - Result: success
  - Note: Vite emitted an existing chunk-size warning for the main JS bundle after build; build still completed successfully.
- `npm --prefix frontend run lint`
  - Result: success

### Static hygiene

- `ruff check backend/app/models/audio_settings.py backend/app/services/audio_length_estimation.py backend/app/services/audio_settings.py backend/app/services/session_hydration.py backend/app/services/conversation_memory.py backend/app/services/sessions.py backend/tests/test_audio_length_estimation_service.py`
  - Result: success

### Browser and screenshot verification

The Docker Compose stack was already running, so I reused it instead of starting separate servers.

I seeded a real session in the live Compose Postgres DB with:

- completed prerequisite stages through composition
- a selected story setup of `1800` words / `12` minutes / `3` chapters
- audio stage set to in-progress

Seeded session ID:

- `a059941d-503d-468f-94b5-fca2b62dc4f7`

Browser QA was run inside the Compose `browser` container against the live frontend on `http://localhost:8566`.

Screenshots captured:

- default estimate: [/Users/kevin/code/storyteller/.artifacts/webapp-qa/prompt-71-audio-estimate-default.png](/Users/kevin/code/storyteller/.artifacts/webapp-qa/prompt-71-audio-estimate-default.png)
- slower-speed preview: [/Users/kevin/code/storyteller/.artifacts/webapp-qa/prompt-71-audio-estimate-slower.png](/Users/kevin/code/storyteller/.artifacts/webapp-qa/prompt-71-audio-estimate-slower.png)

What I verified visually:

- the audio stage shows an explicitly approximate label (`Approx. 14 min`) at the saved `0.95x` speed
- moving playback speed to `0.85x` updates the card live to `Approx. 15 min`
- the inline help updates to mention the live playback preview and the chapter-pause assumption
- the UI copy clearly frames the result as approximate rather than exact

Coverage limit of browser QA:

- the live browser scenario covered the `story_setup_target` basis
- the `composition_segments` basis was covered by backend tests rather than by an additional browser setup

## LLM/prompt evaluation suite

No LLM-facing prompts, adapters, model routing, evals, or safety policies were modified in this task.

Evaluation suite status:

- `Not applicable`

## Wrong turns, dead ends, and gotchas

- I first tried to seed the browser-QA session by importing `WorkflowStage` from `app.db`; the enum actually lives in `app.models`.
- My first browser automation attempt changed the range input with direct `input.value = ...`, which did not reliably trigger React’s state path for the live preview. Switching to the native input-value setter plus `input` and `change` events fixed it.
- Inline `node` browser scripts run through `zsh -lc` were briefly mangled by shell history expansion on `!`. I resolved that with `set +H` and by avoiding unnecessary `!` usage in the script body.
- The Odysseus-style visual-QA guidance assumes a common `5173` dev port, but this repo’s canonical Compose frontend runs on `8566`. I used the repo’s actual Compose targets.

## Assumptions made while working unsupervised

- I kept the existing bedtime pacing baseline (`140` wpm midpoint, `120-160` range) because prompt 50 already established it elsewhere in the product.
- I assumed a short chapter-break pause should mean `3` seconds per break. That is now centralized and easy to change.
- I assumed that rounding to `15`-second buckets is a better fit for “good heuristic, not fake precision” than exposing exact second-level estimates.
- I assumed chapter-count source priority should be:
  1. selected story setup `chapter_count`
  2. selected chapter outline card count
  3. no chapter-pause buffer
- I used a seeded live session for browser QA instead of hand-driving the full planning funnel because the task was about the audio-stage estimate itself, not the entire session-authoring journey.

## Remaining limits or follow-up considerations

- The estimate still reflects a simple global pause heuristic. If the product later introduces explicit chapter metadata or narration-segment boundaries, the estimator should read those instead of inferring from chapter count.
- Background music settings currently do not affect duration. That seems correct for this stage, but if future rendering adds intros/outros or musical transitions, the estimator will need another adjustment point.
- The frontend build still reports the existing large-bundle warning from Vite.

## Final repo state notes

- The feature code is committed on the current branch at `0dbcfd6`.
- The remaining dirty/untracked files in `git status` are unrelated `.yolopilot` run artifacts that predated or were generated alongside the task run; I did not modify or revert them as part of the feature commit.
