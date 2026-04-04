# Prompt 72: Narration Segmentation Strategy

## What I Changed and Why

I added a durable narration-planning layer so audio generation can run and resume segment by segment instead of treating the whole story as one opaque blob.

The core change is a new `narration_segments` table plus a `NarrationSegmentationService` that builds an audio plan from the latest accepted story text. The planner uses accepted composition segments as the primary source of truth, because they already represent the current manuscript and already carry outline metadata from the composition flow. That gave us three useful properties immediately:

1. The audio plan maps back to the exact persisted manuscript, not an inferred reconstruction.
2. Logical boundaries are preserved by default, because composition segments already align with chapter or scene cards when available.
3. Resume state is durable, because each planned narration segment has its own row, status, offsets, and hints.

I wired plan creation into `start_audio_generation`, so every new audio job now persists a narration plan before the job is surfaced as active. The audio job also records the planned segment count in `config_json`, and hydration/realtime plumbing now exposes that count through `AudioJobView`.

## Architectural Changes

### Durable Data Model

I added `NarrationSegment` in [backend/app/db/models.py](/Users/kevin/code/storyteller/backend/app/db/models.py) and a matching Alembic migration in [backend/migrations/versions/20260402_10_add_narration_segments.py](/Users/kevin/code/storyteller/backend/migrations/versions/20260402_10_add_narration_segments.py).

Each narration segment stores:

- `audio_job_id` and `session_id` so the plan is owned durably by the audio job/session.
- `segment_index` so the worker can resume sequentially.
- `status` so segment-by-segment progress can be tracked.
- `source_composition_segment_id` plus `text_start_offset` and `text_end_offset` so the plan maps back to the final story text cleanly.
- `source_boundary_kind`, `pause_hint`, `pause_after_seconds`, and `music_transition_hint` so later audio synthesis can honor chapter/scene semantics.
- `text_content` and `word_count` so a worker does not need to rebuild slices from scratch to render a segment.

I also added enum support and exports in [backend/app/db/__init__.py](/Users/kevin/code/storyteller/backend/app/db/__init__.py).

### Segmentation Service

The new implementation lives in [backend/app/services/narration_segmentation.py](/Users/kevin/code/storyteller/backend/app/services/narration_segmentation.py).

The service works like this:

- It loads the latest accepted current composition segments for the session.
- It derives chapter/scene context from stored composition payload metadata, falling back to the selected outline when necessary.
- It keeps each accepted composition segment intact when it is already narration-friendly.
- If a segment is too large, it splits it conservatively using paragraph boundaries first, then sentence boundaries, then fixed word groups as a last resort.
- It computes exact character offsets against the canonical compiled manuscript form, using the same `"\n\n"` join strategy as the composition pipeline.
- It assigns pause and music hints using simple deterministic rules:
  - chapter ending, not final segment: `chapter_break` + 3 second pause + `soft_reset`
  - scene or intra-chapter continuation: no pause + `continue_bed`
  - final segment: no pause + `end_story`

### Workflow Integration

I updated [backend/app/services/story_tools.py](/Users/kevin/code/storyteller/backend/app/services/story_tools.py) so `_start_audio_generation` now:

- creates the `AudioJob`
- immediately materializes its narration plan through `NarrationSegmentationService`
- stores `total_segments`, `planned_word_count`, `compiled_text_length`, and a plan version in `audio_job.config_json`
- emits the initial audio progress event with `total_segments`

This keeps the existing audio-start entry point intact while making it ready for a future segment-aware worker loop.

### Hydration, Realtime, and Frontend Contract Alignment

I updated:

- [backend/app/models/session.py](/Users/kevin/code/storyteller/backend/app/models/session.py)
- [backend/app/services/session_hydration.py](/Users/kevin/code/storyteller/backend/app/services/session_hydration.py)
- [backend/app/services/session_realtime.py](/Users/kevin/code/storyteller/backend/app/services/session_realtime.py)
- [frontend/src/api/sessions.ts](/Users/kevin/code/storyteller/frontend/src/api/sessions.ts)
- [frontend/src/features/session/sessionRuntimeStore.ts](/Users/kevin/code/storyteller/frontend/src/features/session/sessionRuntimeStore.ts)

`AudioJobView` now carries `total_segments`, hydration reads that from `audio_job.config_json`, realtime audio events preserve it, and the frontend runtime store keeps it when snapshot data and realtime updates merge.

## New Abstractions and How to Use Them

### `NarrationSegmentationService`

Basic usage:

```python
from app.services.narration_segmentation import NarrationSegmentationService

plan = NarrationSegmentationService(db_session).create_plan(
    session_id=session_id,
    audio_job_id=audio_job.id,
)

audio_job.current_segment_index = plan.segments[0].segment_index
audio_job.config_json = {
    **(audio_job.config_json or {}),
    "total_segments": plan.total_segments,
}
```

What this gives you:

- `plan.segments`: persisted `NarrationSegment` rows ready for execution
- `plan.total_segments`: deterministic planned count for UI and resume logic
- `plan.total_words`: planned narration word count
- `plan.compiled_text_length`: size of the canonical compiled manuscript used for offsets

### Worker Extension Point

The intended next-step worker usage is straightforward:

```python
next_segment = (
    db_session.query(NarrationSegment)
    .filter(
        NarrationSegment.audio_job_id == audio_job.id,
        NarrationSegment.status.in_([JobStatus.QUEUED, JobStatus.FAILED]),
    )
    .order_by(NarrationSegment.segment_index.asc())
    .first()
)
```

That worker can synthesize `next_segment.text_content`, persist an `AUDIO_SEGMENT` asset for `segment_index`, mark the narration segment `COMPLETED`, and then advance `audio_job.current_segment_index`.

### Plan Rules Encoded in Data

The new table is intentionally explicit enough that downstream code does not need to rediscover policy:

- `source_boundary_kind` tells the renderer whether the source material came from a chapter or scene boundary.
- `pause_hint` and `pause_after_seconds` tell the renderer whether to inject a chapter pause.
- `music_transition_hint` tells the renderer whether to keep the current bed, softly reset it, or resolve at the end.

## Verification Performed

### Backend Tests

I ran:

```bash
pytest backend/tests/test_narration_segmentation_service.py \
       backend/tests/test_story_tools.py \
       backend/tests/test_db_models.py \
       backend/tests/test_migrations.py \
       backend/tests/test_session_hydration_service.py -q
```

Result: `47 passed in 7.77s`

I also ran:

```bash
pytest backend/tests/test_session_api.py backend/tests/test_session_service.py -q
```

Result: `67 passed in 10.47s`

### Integration Migration Check

I ran:

```bash
pytest backend/tests/integration/test_data_layer.py -q
```

Result: `5 skipped in 0.03s`

Limit: those integration tests require the broader Postgres-backed integration setup, so they were skipped in this environment rather than failing.

### Lint

I ran:

```bash
ruff check backend/app backend/tests
```

Result: passed

One lint issue surfaced during development in the new service and was fixed before the final pass.

### Frontend Tests

I ran the targeted runtime-store test first because the frontend contract changed:

```bash
npm test -- sessionRuntimeStore.test.ts
```

Result: `1 passed, 6 tests passed`

Then I ran the full frontend suite:

```bash
npm test
```

Result: `21 passed, 108 tests passed`

### Frontend Build

I ran:

```bash
npm run build
```

Result: passed

Limit: Vite reported the existing large-chunk warning for the main bundle after build. That warning pre-existed the narration work and did not block the build.

### Browser Checks and Screenshots

None performed.

Reason: this task did not change rendered UI, layout, styling, or interaction flow. The frontend changes were type/runtime contract plumbing only, so I verified them through Vitest and a production build instead of browser screenshots.

## LLM / Prompt Evaluation Suite

No new LLM or prompt evaluation suite was added.

Reason: this task did not modify prompt text, eval logic, model routing, structured-output schemas for model calls, or any other LLM-facing behavior. The change is deterministic planning/persistence around already-generated story text.

Named criteria and outcomes:

- `llm_prompt_changes_present`: `pass` for “no prompt changes made”
- `llm_eval_suite_required`: `pass` for “not applicable`

## Wrong Turns, Dead Ends, and Gotchas

The main design branch I rejected was storing the narration plan only inside `audio_job.config_json`.

That would have been quicker, but it would not have satisfied the durability and resume requirements cleanly:

- no per-segment durable status
- no stable relational target for a worker to claim/update
- weaker source mapping
- harder migration path to segment-level asset tracking

I also hit one subtle implementation bug while building the splitter: sentence and paragraph regex spans can include trailing whitespace. If I had persisted raw offsets while storing stripped text, the plan would have contained mismatched text slices and source ranges. I fixed that by trimming spans before writing both the offsets and `text_content`.

Another repository behavior worth calling out: the existing codebase already treated `start_audio_generation` as a background-style workflow tool, but there is not yet a segment-aware audio worker analogous to the composition worker. This prompt therefore stops at durable planning and workflow wiring, which is the right seam for the next prompt to build on.

## Assumptions I Made

- The canonical compiled manuscript for source offsets is the same `"\n\n"`-joined form already used by the composition pipeline.
- The latest accepted current composition segments are the authoritative source for narration planning.
- Chapter pauses should only be injected at chapter endings, not at scene boundaries.
- Scene boundaries should preserve continuous bed music by default.
- Final-segment music handling should be explicit in the plan (`end_story`) even though the current repo does not yet execute a segment-level audio worker.
- It was acceptable to expose `total_segments` through hydration/realtime/frontend contracts without adding a full narration-plan UI, because the current prompt only required durable planning and resumability foundations.

## Files Most Relevant to Review

- [backend/app/services/narration_segmentation.py](/Users/kevin/code/storyteller/backend/app/services/narration_segmentation.py)
- [backend/app/services/story_tools.py](/Users/kevin/code/storyteller/backend/app/services/story_tools.py)
- [backend/app/db/models.py](/Users/kevin/code/storyteller/backend/app/db/models.py)
- [backend/migrations/versions/20260402_10_add_narration_segments.py](/Users/kevin/code/storyteller/backend/migrations/versions/20260402_10_add_narration_segments.py)
- [backend/app/services/session_hydration.py](/Users/kevin/code/storyteller/backend/app/services/session_hydration.py)
- [backend/app/services/session_realtime.py](/Users/kevin/code/storyteller/backend/app/services/session_realtime.py)
- [backend/tests/test_narration_segmentation_service.py](/Users/kevin/code/storyteller/backend/tests/test_narration_segmentation_service.py)
- [backend/tests/test_story_tools.py](/Users/kevin/code/storyteller/backend/tests/test_story_tools.py)
