# Prompt 61 Summary: Segmented Writing Engine

## What I changed and why

I implemented the backend writing engine so composition now advances one durable segment at a time instead of trying to generate the whole story in one pass.

The chosen segment unit is the existing outline card. Each outline card now maps cleanly to one `composition_segments` record and one completed segment artifact. That gives the system a stable unit for:

- generating only the next requested part of the story,
- carrying context forward in a bounded way,
- rewriting a single segment later without rebuilding the whole draft,
- compiling the final story from the latest accepted revision of each segment.

To support that, I added a structured context-carryover model, a Gemini-backed segment generation adapter, new segment persistence fields, and service logic that persists both the generated prose and the compact handoff summary needed by the next segment.

## Architectural changes across the codebase

### 1. New composition-generation model layer

Added `backend/app/models/composition_generation.py`.

This file introduces the typed contract for segmented generation:

- `CompositionSegmentCarryoverItem`
- `CompositionSegmentCarryoverContext`
- `CompositionSegmentGenerationPromptContext`
- `CompositionSegmentGenerationStructuredOutput`
- `CompositionSegmentGenerationInvocation`
- `CompositionSegmentGenerationInvocationResult`

Why this matters:

- The prompt payload is now explicit and versioned instead of being an ad hoc dict blob.
- Carryover is modeled as summaries of prior accepted segments, not raw concatenated draft text.
- The AI output contract is strict: every segment generation must return `raw_text`, `accepted_text`, and `carryover_summary`.

### 2. New AI adapter and prompt for segment generation

Added:

- `backend/app/ai/composition_generation.py`
- `backend/app/ai/prompts/composition_segment_generation.md`

This provides a dedicated Gemini adapter for segment writing with JSON-schema-constrained output. The adapter:

- renders a prompt from the typed context,
- asks Gemini for JSON only,
- validates the response against `CompositionSegmentGenerationStructuredOutput`,
- normalizes transport and schema failures into backend-owned adapter errors.

This is intentionally separate from the existing planning/composition prompt assembly. The goal was to keep segmented drafting behind a narrow backend interface so the service layer can swap model internals later without changing orchestration code.

### 3. Composition segment persistence now stores draft, accepted prose, and carryover summary

Updated:

- `backend/app/db/models.py`
- `backend/migrations/versions/20260402_06_add_segmented_writing_fields.py`

New `composition_segments` columns:

- `raw_generated_text`
- `accepted_text`
- `accepted_summary`

These fields separate concerns that were previously collapsed into `text_content`:

- `raw_generated_text`: what the model or writer initially produced
- `accepted_text`: the durable segment text used for compilation/export/playback
- `accepted_summary`: the structured handoff for later segments

`text_content` is still populated for backward compatibility with earlier code paths and streaming assumptions.

### 4. Composition orchestration now carries forward structured context and compiles latest accepted revisions

Most of the implementation work is in `backend/app/services/composition_jobs.py`.

Key changes:

- `GeneratedCompositionSegmentDraft` now carries:
  - `raw_text`
  - `accepted_text`
  - `carryover_summary`
  - `remaining_chunks`
  - `evaluation`
  - `source`
  - provider metadata
- Added `GeminiCompositionSegmentWriter` with a heuristic fallback path.
- The runtime refreshes the current segment payload right before execution, so generation uses the latest plan and continuity state.
- Added `_build_context_carryover()` to assemble bounded structured carryover from earlier completed segments.
- Persisted `payload.context_carryover` on the segment row so later rewrites can inspect the exact input context that was used.
- Completed segments now persist `raw_generated_text`, `accepted_text`, and `accepted_summary`.
- Segment asset metadata now includes carryover/evaluation information for rewrite and review tooling.
- Final story compilation no longer assumes a single linear job run. `_compile_story_text(session_id)` now composes from the latest completed revision of each segment index across the whole session.

That last point is important for rewrite support. If segment 2 is rewritten later, the compiled story now correctly uses:

- latest accepted segment 1,
- latest accepted segment 2 revision,
- latest accepted segment 3,

instead of only the revisions produced by one specific job run.

### 5. Continuity and workflow services now read accepted segment state

Updated:

- `backend/app/services/continuity.py`
- `backend/app/services/story_tools.py`
- `backend/app/worker/default_handlers.py`

Changes:

- Continuity extraction now prefers `accepted_summary` first, then `accepted_text`, then legacy `text_content`.
- Story word-count estimation now deduplicates segment revisions by segment index and uses the latest accepted text.
- Continue-composition flows now resolve the next start segment with `CompositionJobService.resolve_continue_start_segment(session_id)` rather than a naive `max(segment_index) + 1`.
- Worker handler typing was updated so the new writer shape is explicit.

### 6. Strategy note for reviewers and future extension

Added `docs/segmented-writing-context-carryover.md`.

This documents the carryover strategy, what is persisted, why the prompt stays bounded, and how rewrites are expected to work.

## Examples of the new abstractions and extension points

### Example: typed carryover context for a segment-generation call

```python
from app.ai import build_composition_segment_generation_invocation
from app.models import (
    CompositionSegmentCarryoverContext,
    CompositionSegmentCarryoverItem,
    CompositionSegmentGenerationPromptContext,
)

carryover = CompositionSegmentCarryoverContext(
    prior_segment_count=2,
    story_so_far_summary="Mira left the dock, followed the bell, and found the hidden cove.",
    latest_accepted_summary="Mira and Pip entered the cove calmly and stayed together.",
    prior_segments=[
        CompositionSegmentCarryoverItem(
            segment_index=1,
            outline_card_title="Opening Image",
            accepted_summary="Mira heard the bell and chose to follow it.",
            accepted_word_count=480,
        ),
        CompositionSegmentCarryoverItem(
            segment_index=2,
            outline_card_title="Midpoint",
            accepted_summary="Mira and Pip discovered the cove without losing their calm.",
            accepted_word_count=520,
        ),
    ],
)

context = CompositionSegmentGenerationPromptContext(
    composition_prompt=prompt_package,
    carryover=carryover,
)

invocation = build_composition_segment_generation_invocation(
    context,
    model_id=settings.gemini.composition_model,
)
```

This is the contract the Gemini segment adapter consumes. The important design choice is that the prompt uses structured summaries, not the full prior draft text.

### Example: runtime carryover persisted on a segment record

Each generated segment now stores a payload shape like:

```json
{
  "context_carryover": {
    "strategy_version": "segmented_context_carryover.v1",
    "segment_unit": "outline_card",
    "prior_segment_count": 2,
    "story_so_far_summary": "Compact summary of the last few accepted segments.",
    "latest_accepted_summary": "Immediate handoff from the last completed segment.",
    "prior_segments": [
      {
        "segment_index": 1,
        "outline_card_title": "Chapter 1",
        "accepted_summary": "Accepted summary for chapter 1.",
        "accepted_word_count": 510
      }
    ]
  }
}
```

This is the durable input record that later rewrite tooling can inspect or reuse.

### Example: latest revision wins during compilation

The composition service now compiles story text from the latest completed segment row for each `segment_index` across the session. That means later rewrites replace earlier accepted revisions at the same index without disturbing untouched segments.

This is the main extension point that makes per-segment rewrite workflows viable.

## Exact verification work performed

### Static and unit/integration verification

I ran:

1. `python -m compileall backend/app backend/tests`
   - Result: passed

2. `pytest backend/tests/test_composition_generation.py backend/tests/test_story_tools.py backend/tests/test_composition_prompt_assembly.py backend/tests/test_continuity_service.py backend/tests/test_migrations.py backend/tests/test_db_models.py -q`
   - Result: `34 passed in 3.78s`

3. `make backend-format-check`
   - Result: passed

4. `cd backend && .venv/bin/python -m ruff check app/ai/__init__.py app/ai/composition_generation.py app/db/models.py app/models/__init__.py app/models/composition_generation.py app/services/__init__.py app/services/composition_jobs.py app/services/continuity.py app/services/story_tools.py app/worker/default_handlers.py tests/test_composition_generation.py tests/test_story_tools.py tests/test_db_models.py tests/test_migrations.py tests/integration/test_data_layer.py`
   - Result: all checks passed

5. `make backend-test`
   - Result: `218 passed, 5 skipped in 14.96s`

6. `make backend-integration-test`
   - Result: `5 passed in 2.44s`
   - Notes: this started the local integration dependencies, including the persistent Docker Compose PostgreSQL and GCS emulator containers used by the repo.

### Functional behavior verified by tests

In addition to the broader suite, I added/updated tests that verify the new segmented-writing behavior directly:

- `backend/tests/test_composition_generation.py`
  - validates the prompt contract and structured output schema
- `backend/tests/test_story_tools.py::test_composition_job_service_carries_forward_structured_segment_summaries`
  - verifies that a completed segment writes `raw_generated_text`, `accepted_text`, and `accepted_summary`
  - verifies that the next segment receives the prior segment summary inside `payload["context_carryover"]`
- `backend/tests/test_story_tools.py::test_rewrite_job_compiles_story_from_latest_segment_revisions`
  - verifies that final compilation uses the latest accepted revision per segment index across rewrites
- migration/data-layer tests verify the new columns exist and round-trip correctly

### Browser checks and screenshots

None were run.

Reason:

- this task only changed backend composition/orchestration, persistence, and tests,
- no frontend/UI, visual, rendering, layout, or accessibility code changed,
- there was no new browser-facing behavior to validate visually for this prompt.

Remaining limit:

- I did not add a browser-driven end-to-end composition playback test, because the acceptance criteria for this prompt were backend durability and rewrite support rather than UI behavior.

## LLM and prompt evaluation suite

I added a prompt-contract evaluation test in `backend/tests/test_composition_generation.py`.

Named criteria and results:

- `prompt_mentions_segment_scope`: pass
- `prompt_mentions_structured_carryover`: pass
- `carryover_context_includes_prior_segment_summary`: pass
- `response_schema_requires_raw_text`: pass
- `response_schema_requires_accepted_text`: pass
- `response_schema_requires_carryover_summary`: pass

Measured result:

- `6/6` prompt-contract criteria passed

This is not a probabilistic model-quality benchmark; it is a deterministic contract/eval suite that protects the wiring and schema guarantees around the new segmented generation path.

## Wrong turns, dead ends, and gotchas

### 1. Initial compilation logic was too job-local

My first pass at composition orchestration still reasoned too much in terms of “the current job’s segments.” That would have been wrong for rewrites because a later rewrite job for segment 2 could accidentally ignore the earlier accepted segment 1 or fail to replace only segment 2 cleanly.

I corrected this by changing final compilation to session-level latest-revision folding by `segment_index`.

### 2. `make backend-format` touched unrelated files

Running the repo formatter reformatted many backend files unrelated to Prompt 61. I backed those changes out and kept the final diff focused on the segmented-writing work. After that I relied on `make backend-format-check` plus targeted `ruff check` for validation.

### 3. Repository metadata changes during the run

The `.yolopilot` run metadata and log files change while the batch workflow runs. Those files are not part of the feature implementation and should not be reviewed as product changes.

### 4. Parallel git operations created a transient lock

I initially tried to `git add` and `git commit` in parallel. That created a transient `.git/index.lock` conflict. I retried the commit sequentially and the checkpoint commit completed normally after that.

## Assumptions I had to make while working unsupervised

- The correct segment unit for Prompt 61 is the existing outline card. This was the cleanest durable unit already present in the data model and services.
- `accepted_text` should become the source of truth for downstream compilation, while `text_content` remains populated for compatibility with existing streaming/display code.
- The next segment only needs structured summaries of prior accepted segments, not verbatim full-text replay.
- A Gemini-backed segmented-generation adapter should exist now as the production extension point, but local and test flows still need a deterministic heuristic fallback so the repo can be verified without depending on live model calls.
- No UI verification was necessary because the prompt’s acceptance checks were strictly backend-focused.

## Files changed

- `backend/app/ai/__init__.py`
- `backend/app/ai/composition_generation.py`
- `backend/app/ai/prompts/composition_segment_generation.md`
- `backend/app/db/models.py`
- `backend/app/models/__init__.py`
- `backend/app/models/composition_generation.py`
- `backend/app/services/__init__.py`
- `backend/app/services/composition_jobs.py`
- `backend/app/services/continuity.py`
- `backend/app/services/story_tools.py`
- `backend/app/worker/default_handlers.py`
- `backend/migrations/versions/20260402_06_add_segmented_writing_fields.py`
- `backend/tests/integration/test_data_layer.py`
- `backend/tests/test_composition_generation.py`
- `backend/tests/test_db_models.py`
- `backend/tests/test_migrations.py`
- `backend/tests/test_story_tools.py`
- `docs/segmented-writing-context-carryover.md`

## Final repository state

Implementation checkpoint commit created before this summary:

- `7748dd6` — `feat(prompt-61): segmented writing engine`

I wrote this summary file after code changes and verification were complete so the final filesystem change for the run is the reviewer-facing markdown deliverable requested by the prompt.
