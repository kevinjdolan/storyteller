# 73 — Gemini TTS Integration

Read `base_prompt.md` first and preserve all prior prompt work.

## Objective

Integrate the backend with Gemini text-to-speech generation behind a clean provider adapter.

## Build
- Create a TTS service adapter that accepts narration text plus voice/style settings and returns audio bytes or stored assets.
- Keep the selected TTS model ID configurable so the app can track Google’s evolving Gemini TTS offerings without scattering model names through the codebase.
- Handle local development, failures, retries, and response metadata cleanly.

## Deliverables

- Backend TTS adapter service
- Config-driven TTS model selection
- Error handling and retry policy for TTS calls

## Acceptance checks

- The rest of the app can request narration without knowing provider-specific details.
- TTS integration is isolated enough to change model IDs later.
- Failures produce durable job status and useful error messages.

## Notes

Keep this adapter separate from text-generation services.

## Suggested commit label

`feat(prompt-73): gemini tts integration`
