# Planning Funnel E2E Test

## Purpose

[`backend/tests/test_planning_funnel_e2e.py`](/Users/kevin/code/storyteller/backend/tests/test_planning_funnel_e2e.py) drives one session through the planning funnel from genre selection to a saved story setup with a generated chapter outline. The goal is to catch regressions where individually healthy planning endpoints stop composing into one durable user journey.

## What Is Real

- FastAPI routing, request validation, and dependency wiring
- SQLAlchemy persistence, session hydration, event log writes, stage-state rollups, and usage tracking
- Catalog seeding and selection lookups
- The real story-setup tool path, including automatic outline generation and plan revision capture
- Snapshot reloads and hydration reads that mirror what the workspace consumes

## What Stays Mocked

- Brief normalization
- Pitch generation
- Character generation
- Beat-sheet generation

Those four model-facing adapters are replaced with deterministic but realistic structured outputs. They include token metadata and domain-shaped content so the test still exercises downstream assumptions about candidate counts, selected artifacts, beat coverage, and outline drafting fields.

## Why This Shape

- It runs in the default backend suite, so the funnel is checked before shipping instead of hiding behind optional integration flags.
- It verifies durable state after reloading and hydrating the session, not only in the immediate mutation responses.
- It keeps the only mocks at the provider boundary, which makes failures point at actual workflow wiring rather than a synthetic test-only path.

## Current Limits

- Persistence runs on a temporary SQLite database rather than Postgres.
- No browser automation is involved; this test covers the backend contract that the workspace UI consumes.
- Blob storage is intentionally out of scope because the planning funnel does not create assets.
