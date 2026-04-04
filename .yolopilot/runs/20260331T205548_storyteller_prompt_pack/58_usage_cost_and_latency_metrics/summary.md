# Prompt 58: Usage, Cost, and Latency Metrics

## What I changed and why

I added a lightweight but durable model-usage telemetry path so the backend can answer three questions without guesswork:

- which model was used for a session step
- how long the call took
- how many tokens and roughly how much money the call consumed

The implementation persists both per-call detail and per-session rollups. That gives the app cheap session hydration for summary views while still preserving enough event-level detail for developer diagnostics.

The work was committed as:

- `8ed00ed` `feat(prompt-58): usage cost and latency metrics`

## Architectural changes

### 1. New durable telemetry tables

Added a migration and SQLAlchemy models for:

- `model_usage_events`
  - append-only record per model call
  - stores bucket, workflow stage, purpose, model, prompt version, outcome, elapsed time, token metadata, approximate cost, and optional error text
- `session_usage_rollups`
  - one row per `session_id + usage_bucket`
  - stores counters and accumulated totals for planning, composition, and audio buckets

Files:

- [backend/app/db/models.py](/Users/kevin/code/storyteller/backend/app/db/models.py)
- [backend/migrations/versions/20260402_05_add_model_usage_metrics.py](/Users/kevin/code/storyteller/backend/migrations/versions/20260402_05_add_model_usage_metrics.py)
- [backend/app/db/__init__.py](/Users/kevin/code/storyteller/backend/app/db/__init__.py)

### 2. New usage models, repository, and service

Added a dedicated telemetry layer:

- [backend/app/models/model_usage.py](/Users/kevin/code/storyteller/backend/app/models/model_usage.py)
  - API-facing summary, bucket, stage-breakdown, and event models
- [backend/app/repositories/model_usage.py](/Users/kevin/code/storyteller/backend/app/repositories/model_usage.py)
  - persistence/query helpers for events, rollups, and grouped breakdowns
- [backend/app/services/model_usage.py](/Users/kevin/code/storyteller/backend/app/services/model_usage.py)
  - extracts Gemini `usageMetadata`
  - estimates approximate cost from configurable pricing defaults
  - updates rollups
  - emits concise structured log lines

The service is intentionally generic so future composition and audio model adapters can call the same recorder instead of inventing a second telemetry system.

### 3. Instrumented the existing Gemini-backed planning flows

I threaded usage recording through the current live Gemini paths:

- brief normalization
- pitch generation and refinement
- character generation and refinement
- beat-sheet generation and refinement
- free-form chat intent parsing

Files:

- [backend/app/services/sessions.py](/Users/kevin/code/storyteller/backend/app/services/sessions.py)
- [backend/app/services/intent_parser.py](/Users/kevin/code/storyteller/backend/app/services/intent_parser.py)

I also preserved attempted `model_id` and `prompt_version` on heuristic fallbacks so failed or discarded Gemini calls still show up in metrics instead of disappearing.

Files:

- [backend/app/services/brief_normalization.py](/Users/kevin/code/storyteller/backend/app/services/brief_normalization.py)
- [backend/app/services/pitch_generation.py](/Users/kevin/code/storyteller/backend/app/services/pitch_generation.py)
- [backend/app/services/character_generation.py](/Users/kevin/code/storyteller/backend/app/services/character_generation.py)
- [backend/app/services/beat_sheet_generation.py](/Users/kevin/code/storyteller/backend/app/services/beat_sheet_generation.py)

### 4. Exposed per-session summaries and developer diagnostics

Session snapshots now include a usage summary, and there is a dedicated diagnostics endpoint:

- `GET /api/v1/sessions/{session_id}/usage`

That response includes:

- summary rollups for `planning`, `composition`, and `audio`
- per-stage/model breakdowns
- recent calls
- slowest calls
- costliest calls

Files:

- [backend/app/models/session.py](/Users/kevin/code/storyteller/backend/app/models/session.py)
- [backend/app/services/session_hydration.py](/Users/kevin/code/storyteller/backend/app/services/session_hydration.py)
- [backend/app/api/v1/routes/sessions.py](/Users/kevin/code/storyteller/backend/app/api/v1/routes/sessions.py)

## New abstractions and extension points

### Record a model call manually

```python
from app.models import ModelCallOutcome, ModelUsageBucket, WorkflowStage
from app.services.model_usage import ModelUsageContext, SessionModelUsageService

SessionModelUsageService(db_session).record_model_call(
    context=ModelUsageContext(
        session_id=session_id,
        usage_bucket=ModelUsageBucket.PLANNING,
        workflow_stage=WorkflowStage.PITCHES,
        purpose="pitch_generation",
        model_id="gemini-3.1-pro",
        prompt_version="pitch_generation.v3",
    ),
    elapsed_ms=860,
    outcome=ModelCallOutcome.SUCCEEDED,
    raw_response={
        "usageMetadata": {
            "promptTokenCount": 540,
            "candidatesTokenCount": 210,
            "totalTokenCount": 750,
        }
    },
)
```

This is the intended hook for future composition and audio adapters.

### Query diagnostics from the API

```bash
curl http://localhost:8565/api/v1/sessions/<session_id>/usage
```

Useful fields in the response:

- `summary.buckets[*].models_used`
- `summary.buckets[*].approximate_cost_usd`
- `stage_breakdown[*].average_elapsed_ms`
- `slowest_calls`
- `costliest_calls`

### Pricing configuration

Approximate pricing is now configurable under `gemini.approximate_pricing` in `secrets.yaml`.

Files:

- [secrets.example.yaml](/Users/kevin/code/storyteller/secrets.example.yaml)
- [docs/secrets-and-local-config.md](/Users/kevin/code/storyteller/docs/secrets-and-local-config.md)

The defaults are deliberately lightweight development approximations, not a claim of exact provider billing.

## Verification performed

### Lint

Changed-file lint passed:

```bash
python -m ruff check backend/app/db/__init__.py backend/app/models/__init__.py backend/app/services/sessions.py backend/tests/test_session_api.py backend/tests/test_settings.py backend/app/repositories/model_usage.py backend/app/services/model_usage.py backend/app/services/intent_parser.py backend/app/services/session_hydration.py backend/app/services/brief_normalization.py backend/app/services/pitch_generation.py backend/app/services/character_generation.py backend/app/services/beat_sheet_generation.py backend/tests/test_model_usage_service.py backend/tests/test_brief_normalization_service.py backend/tests/test_pitch_generation_service.py backend/tests/test_character_generation_service.py backend/tests/test_beat_sheet_generation_service.py backend/tests/test_migrations.py
```

Result:

- pass

I did not use full-repo `ruff check` as a release gate because it surfaced unrelated pre-existing style issues outside this task in files such as `backend/app/services/action_policy.py`, `backend/tests/test_chat_action_contracts.py`, and `backend/tests/test_intent_parser_service.py`.

### Targeted test runs

```bash
pytest backend/tests/test_model_usage_service.py backend/tests/test_session_api.py backend/tests/test_settings.py backend/tests/test_migrations.py backend/tests/test_brief_normalization_service.py backend/tests/test_pitch_generation_service.py backend/tests/test_character_generation_service.py backend/tests/test_beat_sheet_generation_service.py
```

Result:

- `64 passed`

### Broader touched-area regression run

```bash
pytest backend/tests/test_session_service.py backend/tests/test_session_hydration_service.py backend/tests/test_intent_parser_service.py backend/tests/test_db_models.py
```

Result:

- `37 passed`

### Broad backend regression run

```bash
pytest backend/tests
```

Result:

- `208 passed`
- `5 skipped`
  - skipped integration tests were the expected opt-in data-layer integration suite

### Browser checks / screenshots / UI verification

- not applicable
- this task did not change frontend rendering or user-facing UI
- the new diagnostics surface is API-only in this prompt, so no browser screenshot work was needed

## LLM and prompt verification

I did not add a standalone eval harness script, but I did expand the automated verification around the LLM-facing flows. The relevant criteria and outcomes were:

- `usage_summary_rollup_accuracy`
  - pass
  - covered by [backend/tests/test_model_usage_service.py](/Users/kevin/code/storyteller/backend/tests/test_model_usage_service.py)
  - asserted planning rollup totals including `total_tokens == 1700` and `approximate_cost_usd == 0.00066`
- `usage_endpoint_contract`
  - pass
  - covered by [backend/tests/test_session_api.py](/Users/kevin/code/storyteller/backend/tests/test_session_api.py)
  - asserted API rollup totals including `total_tokens == 1062`, non-null approximate cost, model list, and recent-call ordering
- `fallback_model_metadata_retention`
  - pass
  - covered by:
    - [backend/tests/test_brief_normalization_service.py](/Users/kevin/code/storyteller/backend/tests/test_brief_normalization_service.py)
    - [backend/tests/test_pitch_generation_service.py](/Users/kevin/code/storyteller/backend/tests/test_pitch_generation_service.py)
    - [backend/tests/test_character_generation_service.py](/Users/kevin/code/storyteller/backend/tests/test_character_generation_service.py)
    - [backend/tests/test_beat_sheet_generation_service.py](/Users/kevin/code/storyteller/backend/tests/test_beat_sheet_generation_service.py)
  - each now verifies that heuristic fallbacks preserve the attempted `model_id` and `prompt_version`
- `session_snapshot_usage_hydration`
  - pass
  - covered by [backend/tests/test_model_usage_service.py](/Users/kevin/code/storyteller/backend/tests/test_model_usage_service.py)
  - verified that snapshot hydration now includes rollup data

## Wrong turns, dead ends, and gotchas

- I first tried to exercise the new usage endpoint in the API test by driving the story-brief route and then generating pitches. That hit an unrelated workflow-state conflict for the brief step in the chosen fixture setup, so I changed the test to seed usage records directly. That made the endpoint contract test much more isolated and stable.
- Full-repo `ruff` is not currently clean. I hit unrelated pre-existing style violations outside this task, so I used changed-file linting plus the full backend pytest suite as the validation boundary.
- The current repository does not yet have real composition or audio provider calls. The telemetry infrastructure supports those buckets, but live usage today is concentrated in the planning/classification flows.

## Assumptions made while working unsupervised

- I treated “developer-facing summary view or log report” as satisfied by an API diagnostics endpoint plus structured backend log lines, rather than adding a frontend inspector UI in this prompt.
- I treated approximate cost as configurable heuristics, not exact billing. The checked-in pricing defaults are intentionally lightweight and are meant to be overridden in local config if the team changes models or wants tighter estimates.
- I assumed it was more valuable to preserve attempted model metadata on fallback results than to keep heuristic result objects completely “model-free,” because otherwise failed Gemini calls would disappear from observability.
- I assumed it was acceptable to leave the new summary available through session hydration JSON without updating frontend TypeScript views yet, because no frontend surface currently consumes it and the prompt only required a developer-facing summary output.
