# Full Journey E2E Test

[`backend/tests/integration/test_full_journey_e2e.py`](/Users/kevin/code/storyteller/backend/tests/integration/test_full_journey_e2e.py)
drives one session through the entire product journey with real FastAPI routing, migrated
Postgres persistence, fake-GCS object storage, durable worker jobs, artifact downloads, and
workspace hydration reloads.

## What It Covers

1. Creates a session and confirms it appears in the recent-session library contract.
2. Walks the planning funnel through genre, tone, brief, pitch generation, pitch refinement,
   character generation, character refinement, beat-sheet review, and story setup.
3. Starts composition through the API, runs the durable worker until the manuscript finishes, and
   verifies the published story text survives a hydration reload.
4. Generates the `.docx` export, saves audio settings, starts narration through the API, runs the
   durable audio worker, and verifies the compiled audio asset survives a hydration reload.
5. Downloads the final story text, Word export, and final audio artifact and validates that the
   content is readable.

## Current Blind Spots

- No browser automation is involved yet. The test exercises the backend contract that the workspace
  UI consumes rather than the React surface itself.
- Gemini planning, composition, and TTS providers stay mocked at the adapter boundary. The test is
  deterministic by design and does not validate live provider behavior or prompt drift.
- Audio mixing remains out of scope because the journey keeps background music disabled to avoid
  pulling `ffmpeg` into the integration contract.
