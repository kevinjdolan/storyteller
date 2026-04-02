# Prompt 68: Autosave Drafts And Partial Outputs

## What I changed and why

This prompt needed durable autosave for partially composed stories, plus reliable resume behavior after reconnects, refreshes, or worker interruption. The repository already persisted per-segment text during composition and kept live manuscript text in `composition_jobs.metadata_json`, but it did not create a dedicated rolling draft snapshot asset and it could not recover from that asset if the job metadata was incomplete.

I implemented a bounded, session-level rolling draft snapshot that:

- stores the latest stable manuscript view at a fixed object-storage key instead of creating a new blob for every autosave
- records a `draft_text_snapshot` asset row that gets updated in place instead of accumulating duplicate asset rows
- refreshes on composition autosave checkpoints, segment completion, and manual manuscript-changing flows such as rewrite acceptance, rewrite rejection, and segment-version restoration
- hydrates the composition workspace from that draft snapshot when job metadata is missing the manuscript text

The result is that composition now has a durable “latest stable checkpoint” artifact, and the workspace can recover the manuscript text from that checkpoint on resume.

## Architectural changes

### Storage path strategy

I added a dedicated rolling draft checkpoint path:

- [`backend/app/storage/paths.py`](/Users/kevin/code/storyteller/backend/app/storage/paths.py)

`SessionArtifactStoragePaths.draft_text_snapshot(session_id=...)` now resolves to:

```python
location = object_storage.paths.draft_text_snapshot(session_id=session_id)
# sessions/{session_id}/composition/drafts/latest-stable.md
```

This is intentionally session-level and fixed-name. It bounds blob churn because autosave overwrites the same object instead of creating unbounded immutable snapshots.

### Asset upsert support

I added storage-location-based asset upsert support:

- [`backend/app/repositories/assets.py`](/Users/kevin/code/storyteller/backend/app/repositories/assets.py)
- [`backend/app/services/assets.py`](/Users/kevin/code/storyteller/backend/app/services/assets.py)

The new `SessionAssetService.upsert_asset_record(...)` lets backend services reuse a stable asset row for rolling artifacts:

```python
asset_service.upsert_asset_record(
    session_id=session_id,
    asset_kind=AssetKind.DRAFT_TEXT_SNAPSHOT,
    storage_bucket=location.bucket,
    object_path=location.key,
    mime_type="text/markdown",
    status=AssetStatus.READY,
    composition_job_id=job.id,
    segment_index=current_segment_index,
    byte_size=metadata.size_bytes,
    metadata_json={"checkpoint_reason": "autosave"},
)
```

That is the key enabler for “rolling artifact, bounded metadata growth”.

### Composition autosave orchestration

I extended composition orchestration in:

- [`backend/app/services/composition_jobs.py`](/Users/kevin/code/storyteller/backend/app/services/composition_jobs.py)

Key changes:

- added `_persist_draft_snapshot(...)` to write the rolling manuscript checkpoint and upsert its asset row
- added `_should_autosave_draft_snapshot(...)` to checkpoint on first chunk and every `_DRAFT_SNAPSHOT_CHUNK_CADENCE` chunks, while avoiding redundant end-of-segment autosaves
- persisted draft snapshots during:
  - mid-segment autosave checkpoints
  - pause application
  - segment completion
  - rewrite rejection
  - manual manuscript refreshes routed through `_persist_story_text_snapshot(...)`
- kept the autosave artifact session-scoped while preserving `composition_job_id` ownership for the producing job
- made draft snapshot persistence best-effort on storage transport failures for non-runtime/manual paths, so rejecting or restoring text is not blocked by an unreachable storage endpoint

The existing per-segment draft upload remains in place. The new rolling snapshot is additive and represents the latest stable manuscript view, not a replacement for segment artifacts.

### Resume hydration fallback

I extended session aggregation and hydration in:

- [`backend/app/repositories/sessions.py`](/Users/kevin/code/storyteller/backend/app/repositories/sessions.py)
- [`backend/app/services/session_hydration.py`](/Users/kevin/code/storyteller/backend/app/services/session_hydration.py)

Changes:

- `SessionAggregate` now includes `latest_draft_snapshot_asset`
- hydration loads that asset and, when `accepted_story_so_far` / `latest_partial_output` are missing from the relevant composition job view, it downloads the rolling snapshot text and patches the hydrated job view with it
- the fallback is job-aware: it only applies when the snapshot asset belongs to the active/latest job being hydrated

This keeps the normal path fast and DB-backed, but gives resume a durable fallback when manuscript text is missing from the job row.

### Documentation

I updated:

- [`docs/storage-buckets-and-prefixes.md`](/Users/kevin/code/storyteller/docs/storage-buckets-and-prefixes.md)

That document now includes the rolling draft snapshot key shape.

## Files touched

- [`backend/app/storage/paths.py`](/Users/kevin/code/storyteller/backend/app/storage/paths.py)
- [`backend/app/repositories/assets.py`](/Users/kevin/code/storyteller/backend/app/repositories/assets.py)
- [`backend/app/services/assets.py`](/Users/kevin/code/storyteller/backend/app/services/assets.py)
- [`backend/app/repositories/sessions.py`](/Users/kevin/code/storyteller/backend/app/repositories/sessions.py)
- [`backend/app/services/session_hydration.py`](/Users/kevin/code/storyteller/backend/app/services/session_hydration.py)
- [`backend/app/services/composition_jobs.py`](/Users/kevin/code/storyteller/backend/app/services/composition_jobs.py)
- [`backend/tests/test_asset_service.py`](/Users/kevin/code/storyteller/backend/tests/test_asset_service.py)
- [`backend/tests/test_session_hydration_service.py`](/Users/kevin/code/storyteller/backend/tests/test_session_hydration_service.py)
- [`backend/tests/test_story_tools.py`](/Users/kevin/code/storyteller/backend/tests/test_story_tools.py)
- [`docs/storage-buckets-and-prefixes.md`](/Users/kevin/code/storyteller/docs/storage-buckets-and-prefixes.md)

## Examples and extension points

### Example: resolve the rolling draft snapshot location

```python
location = object_storage.paths.draft_text_snapshot(session_id=session_id)
```

Use this if another backend workflow needs to refresh the latest stable manuscript view without inventing its own key convention.

### Example: reuse the new asset upsert support

```python
SessionAssetService(session).upsert_asset_record(
    session_id=session_id,
    asset_kind=AssetKind.DRAFT_TEXT_SNAPSHOT,
    storage_bucket=location.bucket,
    object_path=location.key,
    mime_type="text/markdown",
    status=AssetStatus.READY,
    composition_job_id=job.id,
    metadata_json={"checkpoint_reason": "autosave"},
)
```

This is the intended pattern for any future rolling artifact that should keep one stable storage key and one stable asset row.

### Example: hydrate from the rolling snapshot

No new public API was added. The extension point is implicit:

- ensure a `draft_text_snapshot` asset exists for the session/job
- ensure its `composition_job_id` matches the job you want to hydrate
- if `accepted_story_so_far` or `latest_partial_output` are absent, `SessionHydrationService` will recover them from the stored object

## Verification performed

### Targeted backend verification

1. `pytest backend/tests/test_asset_service.py backend/tests/test_session_hydration_service.py backend/tests/test_story_tools.py -q`
   - Result: `43 passed in 6.39s`
2. `python -m compileall backend/app`
   - Result: passed

### Broader backend regression verification

1. `cd backend && python -m ruff check app tests`
   - Result: `All checks passed!`
2. `pytest backend/tests/test_asset_service.py backend/tests/test_session_hydration_service.py backend/tests/test_story_tools.py backend/tests/test_session_api.py backend/tests/test_session_service.py -q`
   - Result: `108 passed in 15.20s`
3. `python -m compileall backend/app`
   - Result: passed

### Browser / refresh verification

I used the local browser QA flow against the Docker Compose stack because this prompt changes what the composition workspace shows after reload.

Commands run:

1. `make up`
2. Seeded a compose-backed session directly into Postgres/GCS with:
   - a paused composition job
   - missing `accepted_story_so_far` / `latest_partial_output` in the job metadata
   - a valid rolling `draft_text_snapshot` object and asset row
3. `docker compose -f infra/compose/docker-compose.yml run --rm browser npm run check -- --spec /workspace/.artifacts/webapp-qa/prompt-68-refresh-resume.spec.json`
   - Result: passed
4. `make down`

The browser spec:

- loaded `/sessions/<seeded-session-id>`
- asserted the recovered manuscript text was visible
- reloaded the same route
- asserted the same recovered manuscript text was still visible after reload
- captured a screenshot

Screenshot evidence:

- [`prompt-68-refresh-resume.png`](/Users/kevin/code/storyteller/.artifacts/webapp-qa/prompt-68-refresh-resume.png)

Browser verification limits:

- I verified the paused/reload recovery path, not a live in-progress stream reconnect while chunks are actively arriving.
- I cleaned the seeded QA session back out of Postgres afterward, but I did not implement fake-GCS object deletion for the temporary seeded draft object. That leaves one low-impact local-only object in the emulator volume.

## LLM / prompt evaluation suite

No new prompt templates, model routing, eval harnesses, or LLM-facing contracts were changed for this prompt.

- Evaluation suite added: none
- Named criteria: none
- Measured outcomes: not applicable

## Wrong turns, dead ends, and gotchas

### 1. Rewrite rejection initially linked the rolling snapshot to the wrong segment owner

My first implementation tried to attach the rolling draft snapshot asset to the currently accepted segment during rewrite rejection, even when that accepted segment belonged to an older job. That violated the asset ownership validation path and failed [`backend/tests/test_story_tools.py`](/Users/kevin/code/storyteller/backend/tests/test_story_tools.py). I fixed it by making the rolling draft snapshot keep the producing `composition_job_id` while only attaching `composition_segment_id` when the segment actually belongs to that job.

### 2. Manual snapshot refresh paths initially assumed object storage was always reachable

The broader API suite failed on rewrite rejection because those tests do not run against a resolvable GCS hostname, and the new rolling snapshot write tried to open a live HTTP connection. I changed `_persist_draft_snapshot(...)` and the hydration download fallback to treat storage transport failures as non-blocking for these fallback/manual paths. The configured happy path still persists normally.

### 3. Browser QA seeding hit duplicate catalog rows

My first compose-backed seed script inserted raw `Genre` / `ToneProfile` rows and immediately hit the unique `slug` constraint because the compose Postgres volume already had catalog data. I switched the script to the existing idempotent catalog seeder from [`backend/app/services/catalog.py`](/Users/kevin/code/storyteller/backend/app/services/catalog.py).

### 4. Session creation in the browser seed needed full runtime env

`SessionService.create_session()` hydrates immediately, and hydration reaches `get_settings()`. My first one-off seed script only built a local `settings` object, which was not enough. Exporting the same `STORYTELLER_*` env vars that the app uses fixed that.

## Assumptions made while working unsupervised

- I assumed the right storage-growth tradeoff for this prompt was one rolling session-level draft snapshot object, not immutable per-checkpoint draft blobs.
- I assumed manual manuscript-changing flows should refresh the same rolling snapshot so the workspace resume view stays coherent after rewrite accept/reject/restore actions.
- I assumed storage fallback for hydration should be best-effort and should not fail the whole session load when storage is temporarily unreachable.
- I assumed leaving the existing per-segment partial uploads intact was preferable to replacing them, because they already support segment-level durability and debugability.
- I assumed no frontend code changes were necessary because the existing composition stage already renders `accepted_story_so_far` / `latest_partial_output` from the hydrated snapshot.

## Final state

The implementation is committed as:

- `441fe16 feat(prompt-68): autosave drafts and partials`

The working tree after the commit only had pre-existing YoloPilot run artifacts outside the code changes. No production code changes were left uncommitted.
