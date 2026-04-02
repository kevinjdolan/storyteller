# Prompt 73 Summary: Gemini TTS Integration

Checkpoint commit: `bef54ac43801e85c91f705c1881151ba56407bc0` (`feat(prompt-73): gemini tts integration`)

## What I changed and why

This prompt asked for a backend-only Gemini text-to-speech integration that the rest of the application could use without depending on provider-specific details. The repo already had durable audio job records, narration planning, storage abstractions, and worker plumbing, but it did not have a real TTS adapter or a durable audio runtime path equivalent to the existing composition runtime. The main work was therefore:

- add a Gemini TTS adapter behind a provider-style interface
- move audio generation onto a durable queued runtime path
- keep TTS model selection centralized in config
- make failures durable and diagnosable
- add targeted tests and prompt/eval coverage around the new adapter

The most important architectural correction was that audio generation had previously been started by creating an `AudioJob` directly in an effectively already-running state. That did not match the rest of the app's background-job architecture and would not have handled retries, resumability, or worker-side failures cleanly. I refactored audio to follow the same queue-and-run pattern already used for story composition.

## Architectural changes across the codebase

### 1. Added a provider-isolated Gemini TTS adapter

New file:

- `backend/app/ai/gemini_tts.py`

This module now owns Gemini-specific TTS behavior:

- `NarrationSynthesisRequest`
  - provider-agnostic request object for narration text plus voice/style settings
- `NarrationSynthesisResult`
  - provider-agnostic result object containing audio bytes plus response metadata
- `GeminiTextToSpeechAdapter`
  - concrete provider adapter that talks to Gemini TTS through the backend
- `TextToSpeechError`
  - durable, user-meaningful provider failure
- `TextToSpeechTransportError`
  - retryable transport/upstream error
- `render_gemini_tts_prompt`
  - centralized prompt renderer so prompt construction is testable
- `GEMINI_TTS_PROMPT_VERSION`
  - explicit versioning for prompt-facing behavior

Why this shape:

- route handlers and services should not know anything about Gemini request JSON
- future provider swaps should happen inside `app.ai`, not inside services or workers
- prompt rendering, response parsing, retry behavior, and provider metadata are easier to test when isolated in one module

Implementation details:

- model ID is read from settings, not hardcoded in call sites
- transient 429, 5xx, and network-style failures are retried
- inline base64 audio payloads are decoded from the Gemini response
- the adapter returns normalized audio metadata instead of leaking raw provider payloads

### 2. Centralized configurable Gemini TTS model selection

Updated file:

- `backend/app/settings/config.py`

Change:

- default `gemini_tts_model` is now `gemini-2.5-flash-preview-tts`
- env override remains supported through `STORYTELLER_GEMINI_TTS_MODEL`

Why:

- prompt acceptance explicitly required model configurability
- model names should not be scattered through services, workers, or prompts
- this keeps future Google model migrations to a config change plus targeted adapter updates

### 3. Added a durable audio runtime service

New file:

- `backend/app/services/audio_jobs.py`

This is the main orchestration layer for audio generation. It parallels the app's composition runtime model and keeps backend-owned business logic out of route handlers.

Key pieces:

- `AUDIO_RUNTIME_JOB_TYPE = "story.run_audio_job"`
- `AudioJobService`
- `AudioJobStartResult`
- `AudioJobNotFoundError`
- `AudioJobStateError`
- helper utilities:
  - `build_wav_bytes`
  - `read_wav_bytes`
  - `build_silence_pcm`

What `AudioJobService.start_job(...)` now does:

- validates that audio generation can start from the current durable session state
- creates a narration plan through the existing segmentation service
- creates a queued `AudioJob`
- stores selected provider/model metadata on the job
- records an audio progress event
- enqueues the background runtime job

What `AudioJobService.run_job(...)` now does:

- transitions the job to `in_progress`
- synthesizes each narration segment through the provider adapter
- stores each segment as a WAV asset in object storage
- records model-usage metadata under `ModelUsageBucket.AUDIO`
- supports resume by reusing already completed segment assets
- concatenates segment PCM with configurable pauses into a final WAV
- stores the final audio artifact and marks the workflow stage completed

What `mark_job_failed(...)` now does:

- records durable failure state on the job and current segment
- emits an audio progress event describing the failure
- marks the audio workflow stage `needs_regeneration`

Why:

- the app requirement is durable, resumable background work
- audio should survive page refreshes, worker restarts, and transient provider failures
- failure messaging needs to be durable and visible in session state, not lost in logs

### 4. Moved story tool audio startup onto the durable service

Updated file:

- `backend/app/services/story_tools.py`

Changes:

- `start_audio_generation` now delegates to `AudioJobService.start_job(...)`
- audio jobs now start as `queued` instead of `in_progress`
- snapshot/session stage messaging now reflects queued durable work instead of pretending generation already started
- job config includes the active TTS model ID

Why:

- audio startup logic should use the same durable orchestration path regardless of caller
- story tools should trigger the workflow, not own provider/runtime details
- this removes provider coupling and fixes an architectural mismatch that existed before this prompt

### 5. Wired the worker runtime to execute audio jobs

Updated file:

- `backend/app/worker/default_handlers.py`

Changes:

- registered `AUDIO_RUNTIME_JOB_TYPE`
- added `build_audio_runtime_handler(...)`
- allowed optional dependency injection of a TTS adapter for tests
- added explicit failure commit helpers so failed jobs are durably recorded before handler exit

Why:

- audio jobs now have an actual worker-side runtime target
- runtime handlers need to commit failure state explicitly to preserve durability guarantees

While touching this area, I also fixed a related footgun in the composition handler path: the failure helper there was not committing after calling `mark_job_failed(...)`. The new helper pattern now commits for both composition and audio failure cases in `default_handlers.py`.

### 6. Exported the new abstractions where the rest of the backend expects them

Updated files:

- `backend/app/ai/__init__.py`
- `backend/app/services/__init__.py`
- `backend/app/worker/README.md`

Why:

- the new adapter and service are now part of the backend's normal public surface
- worker documentation should reflect that both composition and audio runtime handlers exist

## Examples of the new abstractions and extension points

### Example: building a provider-agnostic narration request

```python
from app.ai import NarrationSynthesisRequest

request = NarrationSynthesisRequest(
    text="Once the lanterns dimmed, the forest grew quiet enough for dreams.",
    voice_key="storykeeper",
    speaking_rate=0.92,
    style_prompt="Warm, calm, slightly hushed bedtime narration.",
)
```

This object is intentionally backend-owned and does not expose Gemini request fields. A future non-Google provider can implement the same request contract.

### Example: using the Gemini adapter directly

```python
from app.ai import GeminiTextToSpeechAdapter
from app.settings.config import Settings

settings = Settings()
adapter = GeminiTextToSpeechAdapter(settings=settings)
result = adapter.synthesize(request)

audio_bytes = result.audio_bytes
mime_type = result.mime_type
provider_response_id = result.provider_response_id
```

The service layer does not need to know how Gemini expects prompts, voice names, or response payloads.

### Example: starting durable audio generation from application code

```python
from app.services import AudioJobService

audio_service = AudioJobService(...)
start_result = audio_service.start_job(
    session_id=session_id,
    actor="user",
    voice_key="storykeeper",
    speaking_rate=0.92,
    include_music=False,
)
```

What callers get:

- a durable `AudioJob`
- queued background work
- updated workflow state
- no direct dependency on Gemini, WAV assembly, or storage internals

### Example: swapping the provider later

The extension point is the adapter boundary used by `AudioJobService.run_job(...)`.

- keep `NarrationSynthesisRequest` and `NarrationSynthesisResult`
- implement a different adapter with the same call contract
- inject the new adapter into `build_audio_runtime_handler(...)`
- leave routes, story tools, storage, asset records, and job persistence unchanged

That is the core isolation the prompt required.

## Key files touched

- `backend/app/ai/gemini_tts.py`
- `backend/app/ai/__init__.py`
- `backend/app/services/audio_jobs.py`
- `backend/app/services/__init__.py`
- `backend/app/services/story_tools.py`
- `backend/app/settings/config.py`
- `backend/app/worker/default_handlers.py`
- `backend/app/worker/README.md`
- `backend/tests/test_gemini_tts_adapter.py`
- `backend/tests/test_gemini_tts_evals.py`
- `backend/tests/test_settings.py`
- `backend/tests/test_story_tools.py`

## Verification work performed

This prompt affected backend orchestration, worker runtime behavior, provider integration boundaries, and prompt construction. I verified at four levels: linting, targeted tests, broader regressions, and full backend suite.

### Lint and static quality checks

Command:

```bash
ruff check app tests
```

Result:

- pass
- `All checks passed!`

I also used `ruff check --fix` on the touched files before the final full lint pass to normalize import ordering and formatting-adjacent issues.

### Targeted verification for the new TTS path

Command:

```bash
pytest \
  tests/test_gemini_tts_adapter.py \
  tests/test_gemini_tts_evals.py \
  tests/test_settings.py \
  tests/test_worker_runtime.py \
  tests/test_story_tools.py::test_story_workflow_tool_service_creates_durable_narration_segments \
  tests/test_story_tools.py::test_audio_job_service_renders_segment_assets_and_final_audio \
  tests/test_story_tools.py::test_audio_runtime_worker_marks_failures_durably \
  tests/test_story_tools.py::test_eval_registry_alignment_keeps_worker_and_prompt_catalogs_in_sync
```

Result:

- `20 passed in 1.26s`

What this covered:

- Gemini TTS prompt rendering
- response parsing and audio decoding
- retry behavior on transient errors
- settings default and env override behavior
- durable queue creation for audio jobs
- worker execution of audio jobs
- segment asset persistence
- final WAV assembly
- durable failure behavior

### Broader regression coverage around touched backend areas

Command:

```bash
pytest \
  tests/test_story_tools.py \
  tests/test_asset_service.py \
  tests/test_storage.py \
  tests/test_session_hydration_service.py \
  tests/test_session_service.py
```

Result:

- `76 passed in 10.55s`

Why this mattered:

- `story_tools.py` was refactored to use the new service
- audio generation writes assets and job metadata
- session hydration and session snapshots are sensitive to workflow-state changes

### Full backend suite

Command:

```bash
pytest tests
```

Result:

- `256 passed, 5 skipped in 23.43s`

Notes:

- the skipped tests were existing environment/integration skips already present in the repo
- no newly introduced skips were added for this prompt

### Browser checks, screenshots, and visual verification

No browser checks or screenshots were run for this prompt.

Reason:

- the implementation was backend-only
- there were no changes to frontend UI, layout, visual rendering, or browser interaction flows

Limit:

- I did not verify in-browser playback of the stored final WAV artifact because this prompt did not change frontend playback wiring

## LLM and prompt evaluation suite

This prompt changed prompt-facing behavior inside the Gemini TTS adapter, so I added an evaluation-style test file:

- `backend/tests/test_gemini_tts_evals.py`

The suite is not a benchmark harness with aggregate percentages; it is a deterministic evaluation set expressed as named pass/fail criteria. All criteria below passed.

### Evaluation criteria and outcomes

1. `voice-selection-translates-to-provider-voice`
   - Goal: ensure internal app voice keys map to Gemini voice names in one centralized place
   - Outcome: pass

2. `style-prompt-is-preserved-in-rendered-instructions`
   - Goal: ensure caller-provided narration style guidance is carried into the provider prompt
   - Outcome: pass

3. `speaking-rate-guidance-is-rendered`
   - Goal: ensure speaking-rate settings affect the generated instructions even though Gemini TTS speed is prompt-guided rather than a stable explicit API knob in this integration
   - Outcome: pass

4. `bedtime-tone-guardrails-remain-present`
   - Goal: ensure the adapter prompt preserves calm, bedtime-appropriate narration guidance rather than becoming a generic TTS wrapper
   - Outcome: pass

5. `prompt-versioning-remains-explicit`
   - Goal: ensure prompt behavior is versioned so future adapter changes can be tracked and reasoned about
   - Outcome: pass

Related adapter tests in `test_gemini_tts_adapter.py` also validated:

- transport retry behavior: pass
- non-retryable error propagation: pass
- inline audio payload parsing: pass
- malformed provider payload failure: pass

## Wrong turns, dead ends, surprising repository behavior, and gotchas

### Wrong turn corrected: audio jobs were not truly durable runtime jobs yet

The biggest architectural surprise was that the repo already had durable `AudioJob` records and narration segmentation, but audio generation was still being kicked off from `story_tools.py` in a way that marked the job as effectively active before a worker runtime existed. That was a halfway state: the data model suggested durable background work, but the runtime behavior had not caught up.

I initially approached the task as "add a Gemini adapter and wire it into the existing audio job path." After inspecting the codebase more closely, that would have preserved the wrong boundary. I changed course and introduced `AudioJobService` so audio startup and execution now mirror the composition job pattern. That was the correct architectural move for this prompt.

### Gotcha: failure helpers in worker handlers needed explicit commits

While adding the audio handler, I noticed the worker failure path depended on service methods mutating ORM state but not necessarily committing before handler exit. In background runtime code, that is an easy way to lose the durable failure record the prompt explicitly asked for.

I fixed that in `backend/app/worker/default_handlers.py` by introducing helpers that call the service failure methods and then commit explicitly. I applied the same pattern to the composition failure path while I was there.

### Gotcha: TTS speed is not treated as a strongly typed provider control here

I did not find a stable repo-local abstraction for "provider guarantees a numeric speech-rate parameter." For this integration, the safest path was:

- preserve `speaking_rate` as an app-facing control
- translate it into prompt guidance inside the Gemini adapter
- keep the interface provider-agnostic so a future provider with a true numeric speed control can map it more directly

That means this prompt improves durability and isolation, but not deterministic speed control.

### Gotcha: music settings exist, but music rendering/mixing is not part of this prompt's actual implementation

The repo already models audio settings beyond raw narration, including optional music configuration. This prompt asked specifically for Gemini TTS integration, not soundtrack synthesis or mixing. The service therefore:

- preserves music-related settings in durable metadata
- completes voice rendering cleanly
- does not synthesize or mix background music into the final file yet

This is an important reviewer note because the UI/workflow surface may suggest broader audio capabilities than this prompt actually implemented.

## Assumptions I made while working unsupervised

1. The correct backend transport for Gemini TTS in this repo is the same Google Generative Language REST + API key pattern already used elsewhere, rather than introducing a separate client library.

2. The current Gemini TTS response shape can be treated as inline base64 audio payloads that the backend decodes and then wraps into WAV for storage and playback compatibility.

3. The app's durable storage format for generated narration should be WAV, even if the provider returns raw PCM, because WAV is easier to persist, inspect, concatenate safely, and hand to downstream consumers.

4. The current audio job architecture should preserve existing narration segmentation behavior rather than replacing it with a monolithic single-call narration request.

5. Prompt-guided speaking-rate control is acceptable for this prompt as long as the provider-specific behavior is isolated and tested.

6. Because this task was backend-only, lack of browser verification is acceptable as long as backend test coverage is strong and the full backend suite passes.

## Remaining limits and follow-up risks

1. Background music generation and mixing are still not implemented in the final audio assembly path.

2. The Gemini adapter currently assumes a specific family of response payloads and PCM characteristics; if Google changes that response shape, the parsing logic in `gemini_tts.py` will need a focused update.

3. Speaking-rate behavior is best-effort prompt guidance, not guaranteed exact timing control.

4. I did not run a live end-to-end worker against a real Gemini account in this batch run, so provider authentication, quota behavior, and actual upstream latency were not exercised outside mocked tests.

5. Frontend playback and download UX were not touched here, so end-to-end human validation of the newly generated asset in the browser remains a follow-up integration check rather than part of this prompt.

## Reviewer-oriented summary

This prompt leaves the repo in a materially better state than a simple provider wiring pass would have:

- narration is now behind a provider adapter
- TTS model selection is config-driven
- audio generation is a real durable queued runtime job
- worker failures are committed durably
- segment and final audio assets are persisted cleanly
- targeted tests and prompt-facing evals cover the new behavior

If a future prompt needs to swap Gemini TTS models, add a different provider, or extend audio generation into music mixing, the new seams are in the right place for that work.
