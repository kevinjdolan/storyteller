# Composition Loop End-to-End Test

The backend composition loop now has a focused end-to-end regression test in
`backend/tests/test_story_tools.py`:

- `test_composition_loop_e2e_streams_pause_resume_and_hydrates`

## What It Exercises

1. Starts a real durable composition job against a seeded session with a selected brief, pitch,
   character sheet, beat sheet, story setup, and outline.
2. Captures an initial `SessionRealtimeService` chunk cursor before any text exists so later reads
   behave like a live client that subscribed before writing started.
3. Runs `CompositionJobService.run_job()` with deterministic multi-chunk segment output, pauses the
   job mid-segment, and verifies the rolling draft snapshot plus paused job state persist.
4. Hydrates the session after the interruption and confirms the latest saved text is available from
   durable state, not only in-memory worker state.
5. Replays composition chunk deltas from the saved realtime cursor to prove live updates can be
   reconstructed after reconnect.
6. Resumes the paused job, finishes the interrupted segment, confirms the next segment is queued,
   and verifies a hydrated session sees the carried-forward manuscript text and resumed job
   position.
7. Completes the remaining segments and checks the final compiled story asset and completed
   composition snapshot.

## Why This Matters

This test covers the most failure-prone composition path as one scenario instead of isolated unit
assertions:

- segmented writing
- chunk-by-chunk durable progress
- interruption handling
- resume behavior
- reconnect-safe realtime replay
- hydration from persisted state
