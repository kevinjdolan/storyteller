# Prompt 77: Final Audio Assembly and Metadata

## What I changed and why

This prompt asked for the final compiled narration artifact to become a first-class durable output instead of a loose byproduct of segment generation. I implemented that in three layers:

1. A dedicated backend assembly service now builds the narration master from ordered segment assets, optionally mixes background music, uploads the compiled output to object storage, and writes durable metadata about the published file.
2. Asset persistence now tracks richer final-audio metadata and explicit supersession instead of silently overwriting history.
3. The session API and audio-stage UI now expose and render the published master more clearly, including runtime, voice/mix details, download access, and the distinction between the current in-progress audio job and the last published master.

The most important behavioral fix was changing regeneration semantics. Before this work, the existing flow superseded the previous `final_audio` asset as soon as a new audio job started. That created a bad failure mode: a rerender or failed rerender could temporarily remove the last good master from the session. The new flow keeps the previous published master available until a replacement has been successfully assembled and published, then marks the old outputs superseded with replacement metadata.

Checkpoint commit created during the run:

- `cc349e1 feat(prompt-77): final audio assembly`

## Architectural changes across the codebase

### 1. Final audio assembly is now a dedicated service

New file:

- `backend/app/services/final_audio_assembly.py`

This service owns the assembly/publish pipeline instead of leaving it as ad hoc logic inside `audio_jobs.py`.

It provides:

- `build_narration_master(...)`
  - Reads rendered narration segments in order.
  - Concatenates them into one PCM stream.
  - Inserts configured inter-segment pauses.
  - Produces a master build result with duration and segment metadata.
- `persist_narration_master_debug_artifact(...)`
  - Writes an intermediate narration-only artifact when needed for inspection/debugging.
- `mix_narration_master(...)`
  - Applies optional music mixing over the narration master.
  - Preserves narration-first behavior by keeping music subordinate to the voice.
- `publish_final_audio(...)`
  - Uploads the final compiled audio artifact.
  - Creates the durable `session_assets` record.
  - Records generation and media metadata.
  - Supersedes older published masters only after the replacement is ready.

This separation keeps route/worker orchestration simple and gives the app one obvious extension point for future output formats or more sophisticated mastering.

### 2. WAV assembly helpers are centralized

New file:

- `backend/app/services/audio_wave.py`

The old inline wave helpers in `audio_jobs.py` were split into reusable functions:

- `build_wav_bytes`
- `read_wav_bytes`
- `wav_duration_seconds`
- `build_silence_pcm`

This gives audio assembly and segment persistence a shared codec surface instead of duplicating byte-level wave handling in orchestration code.

### 3. Asset records now carry richer final-audio metadata

Updated files:

- `backend/app/services/assets.py`
- `backend/app/models/session.py`
- `backend/app/services/session_hydration.py`
- `frontend/src/api/sessions.ts`

`SessionAssetView` now exposes additional final-audio context:

- `composition_job_id`
- `audio_job_id`
- `duration_seconds`
- `details`
- `superseded_at`

`AssetService` now supports:

- commit-control on asset mutations (`commit: bool = True`) so higher-level workflows can stage multi-step writes cleanly.
- `supersede_assets(...)` for marking older outputs superseded with durable replacement metadata.

Published final-audio assets now store useful metadata in `metadata_json`, including:

- `duration_seconds`
- `narration_master_duration_seconds`
- `segment_count`
- `segment_indexes`
- `pause_seconds_total`
- `estimated_duration_seconds`
- `supersedes_asset_ids`
- nested `media`
- nested `generation`
- nested `mix`
- nested `debug`

That metadata is enough to explain what was generated, how it was produced, and what it replaced.

### 4. Audio job orchestration now publishes through the assembly service

Updated file:

- `backend/app/services/audio_jobs.py`

Changes:

- Removed the old inline final-assembly logic.
- Reused shared WAV helpers from `audio_wave.py`.
- Delegated final publish to `FinalAudioAssemblyService`.
- Stopped superseding prior masters at job start.
- Left the last good master playable/downloadable while a replacement job is still running.

### 5. The audio-stage UI now treats the compiled master as a first-class artifact

Updated files:

- `frontend/src/features/session/AudioSettingsStage.tsx`
- `frontend/src/styles/index.css`

The compiled narration panel now:

- shows runtime metadata
- shows voice metadata
- shows whether music mixing was applied
- shows published timestamp metadata
- surfaces a dedicated `Download narration` action when `public_url` exists
- warns when the visible master belongs to a previous audio job and a replacement is still assembling

This is the important UI bridge for the backend behavior change. The user now has a clear explanation for why an older master may still be shown while a newer audio job is in progress.

## Key files touched

- `backend/app/services/final_audio_assembly.py`
- `backend/app/services/audio_wave.py`
- `backend/app/services/audio_jobs.py`
- `backend/app/services/assets.py`
- `backend/app/models/session.py`
- `backend/app/services/session_hydration.py`
- `backend/app/services/__init__.py`
- `backend/tests/test_asset_service.py`
- `backend/tests/test_story_tools.py`
- `frontend/src/api/sessions.ts`
- `frontend/src/features/session/AudioSettingsStage.tsx`
- `frontend/src/features/session/AudioSettingsStage.test.tsx`
- `frontend/src/styles/index.css`

`git show --stat` for the checkpoint commit:

- 13 files changed
- 977 insertions
- 232 deletions

## How to use the new abstractions, helpers, and extension points

### Publish a compiled final audio artifact

The main intended integration point is `FinalAudioAssemblyService.publish_final_audio(...)`.

Use it after all narration segments for an audio job are rendered and persisted:

1. Collect the ordered rendered segment assets for the current audio job.
2. Pass the owning session/audio job plus the generation settings into `publish_final_audio(...)`.
3. Let the service:
   - build the narration master
   - optionally mix music
   - upload the final file
   - create the durable asset record
   - supersede prior published masters after success

That keeps regeneration semantics correct by construction.

### Reuse the low-level wave helpers

If a later prompt needs another audio transform, use the shared helpers in `backend/app/services/audio_wave.py` instead of re-implementing byte parsing:

- `read_wav_bytes(...)` to turn stored WAV bytes into PCM/sample metadata
- `build_wav_bytes(...)` to serialize PCM back to a WAV file
- `wav_duration_seconds(...)` to derive duration consistently
- `build_silence_pcm(...)` to insert deterministic pauses/gaps

These are the right extension points for format-preserving edits such as fade padding, inter-chapter pauses, or alternate compilation strategies.

### Supersede old finals without losing history

Use `AssetService.supersede_assets(...)` when a new canonical output replaces older ready assets.

This method is appropriate when you want both:

- durable history of superseded outputs
- metadata that explains what replacement superseded them and why

It is not appropriate to call this at job start for final audio. The fix in this prompt is specifically to defer supersession until the replacement artifact exists.

### Render richer compiled-audio UI

Frontend code can read the new asset fields from `SessionAssetView`:

- `audio_job_id`
- `duration_seconds`
- `details`
- `superseded_at`

The current `AudioSettingsStage.tsx` implementation shows the intended pattern:

- compare `latest_audio_asset.audio_job_id` to `active_audio_job.id`
- if they differ and the active job is still running, keep showing the old master but label it as the previously published one
- derive runtime/voice/mix pills from `details`
- use `public_url` as the download/playback source

## Verification work performed

### Backend tests

Targeted backend tests for audio assembly, supersession behavior, and hydration metadata:

```bash
pytest backend/tests/test_asset_service.py backend/tests/test_story_tools.py -k 'audio or supersede'
```

Result:

- `8 passed, 38 deselected`

Additional hydration/API coverage for audio-related session snapshots:

```bash
pytest backend/tests/test_session_hydration_service.py backend/tests/test_session_api.py -k 'audio'
```

Result:

- `3 passed, 46 deselected`

### Backend linting

```bash
ruff check \
  backend/app/services/audio_jobs.py \
  backend/app/services/assets.py \
  backend/app/services/final_audio_assembly.py \
  backend/app/services/audio_wave.py \
  backend/app/services/session_hydration.py \
  backend/app/models/session.py \
  backend/tests/test_asset_service.py \
  backend/tests/test_story_tools.py
```

Result:

- Passed with no reported issues.

### Frontend tests and build

Focused frontend test coverage for the compiled narration panel:

```bash
cd frontend
npm test -- --run src/features/session/AudioSettingsStage.test.tsx
```

Result:

- `1 file, 5 tests` passed

Focused frontend linting:

```bash
cd frontend
npm run lint -- \
  src/features/session/AudioSettingsStage.tsx \
  src/features/session/AudioSettingsStage.test.tsx \
  src/api/sessions.ts
```

Result:

- Passed

Frontend production build:

```bash
cd frontend
npm run build
```

Result:

- Passed
- Vite emitted the usual chunk-size warning for `dist/assets/index-BfeNTyPy.js` being over 500 kB. I treated that as non-blocking for this prompt because it did not originate from the final-audio changes.

### Browser and visual QA

Because the UI changed, I attempted live browser verification rather than relying only on unit tests.

#### Docker path

I first tried the repo’s preferred Docker-based QA flow:

```bash
docker compose -f infra/compose/docker-compose.yml up -d --build
```

This failed immediately because Docker was unavailable in the environment:

- `Cannot connect to the Docker daemon at unix:///Users/kevin/.docker/run/docker.sock. Is the docker daemon running?`

#### Host-run fallback

I then used a host-run fallback:

- seeded a local sqlite QA database at `.artifacts/webapp-qa/prompt77.db`
- started the FastAPI app on `127.0.0.1:8565`
- started the Vite dev server on `127.0.0.1:8566`
- seeded a QA session: `96474c5c-d84f-4157-8a01-ba97fa241742`

I verified by API that the seeded snapshot exposed the intended replacement-state scenario:

- `latest_audio_asset` was a ready `final_audio` asset
- that asset carried `audio_job_id`, `duration_seconds`, and `details`
- `active_audio_job` was in progress with a different `audio_job_id`

I confirmed that with:

```bash
curl -sf http://127.0.0.1:8565/api/v1/sessions/96474c5c-d84f-4157-8a01-ba97fa241742/hydrate
```

The live browser pass reached the workspace route and rendered the real app shell. The captured page text included:

- the seeded session title
- `Current stage: Audio`
- `Live feed idle`
- stage navigation showing `Audio` in progress and `Finalize` as needs refresh

However, the host-seeded browser scenario fell back to the generic audio stage scaffold instead of rendering the compiled narration panel state I expected from the fixture, and repeated `page.screenshot()` attempts stalled without producing a usable image artifact. I also had to correct one QA tooling issue mid-run: a direct Puppeteer launch from `frontend/` failed because `puppeteer` is only installed under `tools/webapp-qa/`.

Net result:

- browser verification was partially successful for route/render/hydration sanity
- I do **not** have a reliable prompt-77 screenshot artifact to attach
- the strongest verification for the new compiled-audio UI remains the focused React test coverage plus the hydration/API checks

### Remaining verification limits

- I did not verify an end-to-end Docker compose flow because the Docker daemon was unavailable.
- I did not produce a successful browser screenshot for the new prompt-77 UI state because the host fallback stalled during screenshot capture.
- I did not run a full repo-wide test suite; I ran the targeted backend/frontend suites relevant to the touched code and a frontend production build.

## LLM or prompt evaluation suite

No prompt templates, model routing, or LLM-facing behavior changed in this prompt.

Because of that:

- no LLM evaluation suite was added
- no prompt regression criteria were needed

Status:

- `LLM/prompt eval suite required`: No
- `LLM/prompt eval suite added`: None

## Wrong turns, dead ends, surprising behavior, and gotchas

### 1. Existing regeneration behavior was too eager

The biggest product bug I found was in the pre-existing regeneration semantics: the old flow superseded the current published final audio at audio-job start. That meant a failed rerender could remove the last known-good master from the session. I changed course there and made successful publish the only place that supersession happens.

### 2. Browser QA package resolution was easy to get wrong

I initially launched a one-off Puppeteer diagnostic from `frontend/`, which failed with `ERR_MODULE_NOT_FOUND` because `puppeteer` is installed in `tools/webapp-qa/`, not in the frontend package. After switching to the correct package root, browser launch worked.

### 3. The host-run browser scenario did not match the seeded API state cleanly

Even though the hydration API exposed the expected final-audio replacement metadata, the host-rendered page showed the generic audio stage scaffold instead of the compiled narration panel. That suggests the ad hoc seed path was enough for API/state verification but not a perfect reproduction of the full UI state machine.

### 4. Full-page screenshot capture stalled in this environment

The browser session could render and dump page text, but the actual screenshot write never completed reliably. I treated that as an environment/tooling limit instead of spending the rest of the run debugging headless capture internals.

## Assumptions I made while working unsupervised

- Storing final-audio runtime and generation details in `session_assets.metadata_json` is an acceptable durable metadata surface for this prompt.
- The correct product behavior is to keep the prior published final audio visible/playable until a replacement final artifact has actually been published.
- Using the existing asset `public_url` for playback and download is sufficient for prompt 77; a dedicated download endpoint was not necessary here.
- A WAV final artifact is acceptable as the current first-class compiled output format for local development and prompt acceptance.
- Focused backend/frontend tests plus a frontend production build were the right validation scope for this prompt once Docker-based end-to-end verification was blocked by the environment.

## Reviewer-oriented outcome summary

Prompt 77 is complete in the repo at the code level:

- the backend now assembles and publishes a coherent final narration artifact from audio segments
- the final asset carries durable runtime/generation metadata
- regenerated audio no longer silently overwrites history
- older masters are superseded explicitly and traceably only after replacement publish succeeds
- the session API and audio-stage UI expose enough metadata for the user to understand what they are hearing/downloading

The main remaining gap is environmental, not architectural:

- Docker-based browser QA was blocked by an unavailable daemon
- host-based browser capture was only partially successful and did not yield a final screenshot artifact

Everything else requested by the prompt was implemented and covered by targeted automated verification.
