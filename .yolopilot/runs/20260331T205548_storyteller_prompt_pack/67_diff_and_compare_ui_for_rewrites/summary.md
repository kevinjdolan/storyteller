# Prompt 67: Diff and Compare UI for Rewrites

## What I changed and why

I implemented a readable rewrite compare flow across the backend and frontend so users can see what changed before they promote rewritten text into the canonical manuscript.

The shipped behavior now covers three concrete decisions:

- Review a pending rewrite against the current manuscript with highlighted diff regions and side-by-side text.
- Accept the rewrite, reject it, or request another rewrite pass without contaminating the live draft.
- Revisit older accepted segment revisions later and restore one as the active text version.

That directly addresses the prompt goals:

- Users no longer have to compare two unrelated walls of text blindly.
- The canonical manuscript only changes on explicit accept or restore actions.
- Rejected pending rewrites stay out of the live manuscript.

## Architectural changes

### Backend

I added two new composition actions to the session API and wired them into the composition service:

- `POST /api/v1/sessions/{session_id}/composition/{composition_job_id}/reject`
- `POST /api/v1/sessions/{session_id}/composition/segments/{segment_index}/versions/{version_id}/select`

The backend changes live mainly in:

- [sessions.py](/Users/kevin/code/storyteller/backend/app/api/v1/routes/sessions.py)
- [session.py](/Users/kevin/code/storyteller/backend/app/models/session.py)
- [composition_jobs.py](/Users/kevin/code/storyteller/backend/app/services/composition_jobs.py)

The service-layer behavior is now:

- `accept_rewrite_job(...)` records the acceptance origin and writes a user-edit event summarizing the active-version change.
- `reject_rewrite_job(...)` dismisses pending rewrite candidates, keeps current accepted segments canonical, and records a user-edit event.
- `select_active_segment_version(...)` restores an older accepted segment revision, marks downstream accepted segments stale when continuity changes, persists a fresh story snapshot, and records a user-edit event.

I also extracted reusable composition snapshot helpers:

- `_resolve_current_story_stage_state(...)`
- `_has_stale_current_story_segments(...)`
- `_mark_current_story_segments_stale_after(...)`
- `_persist_story_text_snapshot(...)`

One important backend fix came out of verification: restoring an older version initially reused the accepted rewrite’s story asset path and hit a unique-constraint failure on `session_assets(storage_bucket, object_path)`. I fixed that by allowing `_persist_story_text_snapshot(...)` to take an artifact-name suffix and giving restore operations a unique snapshot suffix.

### Frontend

The frontend work is centered around a reusable compare browser instead of one-off stage logic:

- [SegmentVersionComparePanel.tsx](/Users/kevin/code/storyteller/frontend/src/features/session/SegmentVersionComparePanel.tsx)
- [segmentVersionDiff.ts](/Users/kevin/code/storyteller/frontend/src/features/session/segmentVersionDiff.ts)
- [CompositionStage.tsx](/Users/kevin/code/storyteller/frontend/src/features/session/CompositionStage.tsx)
- [FinalizeStage.tsx](/Users/kevin/code/storyteller/frontend/src/features/session/FinalizeStage.tsx)
- [SessionWorkspacePage.tsx](/Users/kevin/code/storyteller/frontend/src/pages/session/SessionWorkspacePage.tsx)
- [index.css](/Users/kevin/code/storyteller/frontend/src/styles/index.css)

Key UI changes:

- Added `buildSegmentDiffSummary(...)` to produce highlighted parts, changed regions, and word-change counts.
- Added `SegmentVersionComparePanel` to render:
  - segment selection
  - revision history
  - highlighted compare cards
  - accept/reject/keep-exploring controls for pending rewrites
  - restore controls for archived accepted revisions
- Reworked `CompositionStage` to use the reusable compare panel instead of inline rewrite-only compare markup.
- Added a dedicated `FinalizeStage` so compare and restore remain available from later review.
- Updated `SessionWorkspacePage` to call the new reject/select APIs and to reuse the same compare/restore actions from both composition and finalize stage previews.

### New abstractions and extension points

#### `buildSegmentDiffSummary(beforeText, afterText)`

Use this when a UI needs a lightweight, readable segment diff without introducing a full diff engine.

Example:

```ts
const diff = buildSegmentDiffSummary(currentText, candidateText)
console.log(diff.changedRegionCount, diff.addedWords, diff.removedWords)
```

#### `SegmentVersionComparePanel`

Use this when a stage needs revision browsing plus action controls.

Example:

```tsx
<SegmentVersionComparePanel
  compareContext="composition"
  reviewJob={reviewJob}
  segments={snapshot.composition_segments ?? []}
  onAcceptRewrite={(jobId) => void accept(jobId)}
  onRejectRewrite={(jobId) => void reject(jobId)}
  onKeepExploring={(segmentIndex) => reopenRewriteControls(segmentIndex)}
  onRestoreVersion={(segmentIndex, versionId) =>
    void restore(segmentIndex, versionId)
  }
/>
```

#### `select_active_segment_version(...)`

Use this backend service action when a saved accepted revision should become canonical again.

Example:

```py
CompositionJobService(session).select_active_segment_version(
    session_id,
    segment_index=1,
    version_id=archived_version_id,
    origin="workspace",
)
```

This is intended for accepted archived revisions only. Pending rewrite versions still have to flow through accept/reject review.

## Files touched

Backend:

- [sessions.py](/Users/kevin/code/storyteller/backend/app/api/v1/routes/sessions.py)
- [session.py](/Users/kevin/code/storyteller/backend/app/models/session.py)
- [__init__.py](/Users/kevin/code/storyteller/backend/app/models/__init__.py)
- [composition_jobs.py](/Users/kevin/code/storyteller/backend/app/services/composition_jobs.py)
- [test_session_api.py](/Users/kevin/code/storyteller/backend/tests/test_session_api.py)
- [test_story_tools.py](/Users/kevin/code/storyteller/backend/tests/test_story_tools.py)

Frontend:

- [sessions.ts](/Users/kevin/code/storyteller/frontend/src/api/sessions.ts)
- [segmentVersionDiff.ts](/Users/kevin/code/storyteller/frontend/src/features/session/segmentVersionDiff.ts)
- [segmentVersionDiff.test.ts](/Users/kevin/code/storyteller/frontend/src/features/session/segmentVersionDiff.test.ts)
- [SegmentVersionComparePanel.tsx](/Users/kevin/code/storyteller/frontend/src/features/session/SegmentVersionComparePanel.tsx)
- [CompositionStage.tsx](/Users/kevin/code/storyteller/frontend/src/features/session/CompositionStage.tsx)
- [CompositionStage.test.tsx](/Users/kevin/code/storyteller/frontend/src/features/session/CompositionStage.test.tsx)
- [FinalizeStage.tsx](/Users/kevin/code/storyteller/frontend/src/features/session/FinalizeStage.tsx)
- [FinalizeStage.test.tsx](/Users/kevin/code/storyteller/frontend/src/features/session/FinalizeStage.test.tsx)
- [SessionWorkspacePage.tsx](/Users/kevin/code/storyteller/frontend/src/pages/session/SessionWorkspacePage.tsx)
- [index.css](/Users/kevin/code/storyteller/frontend/src/styles/index.css)

## Verification performed

### Automated tests

Backend:

- `pytest backend/tests/test_story_tools.py backend/tests/test_session_api.py`
  - Result: `73 passed`

Frontend targeted component tests:

- `npm test -- --run src/features/session/segmentVersionDiff.test.ts src/features/session/CompositionStage.test.tsx src/features/session/FinalizeStage.test.tsx`
  - Result: `8 passed`

Frontend workspace integration:

- `npm test -- --run src/pages/session/SessionWorkspacePage.test.tsx`
  - Result: `32 passed`

### Lint, build, and static checks

Backend:

- `ruff check app tests`
  - Result: passed

Frontend:

- `npm run lint`
  - Result: passed
- `npm run build`
  - Result: passed
  - Note: Vite reported an existing chunk-size warning for the built JS bundle exceeding 500 kB after minification. The build still succeeded.

### Browser and visual verification

I reused the running Docker Compose stack instead of launching separate servers.

Stack check:

- `docker compose -f infra/compose/docker-compose.yml ps --format json`
  - Result: `frontend`, `backend`, `worker`, `postgres`, `gcs`, and `browser` were already running and healthy enough for QA.

Live browser QA:

- Created a deterministic pending-review session in the live app database through the backend service layer:
  - Session ID: `2915f590-5ec3-4461-8471-baa5089ea847`
  - Purpose: verify the composition-stage compare UI and accept/reject/keep-exploring controls against real rendered state.
- Reused the existing session:
  - Session ID: `3193b0ba-3739-4a74-a1e7-91b1cd456493`
  - Purpose: verify archived revision restore from later review (`?stage=finalize`).

Browser script:

- `node tools/webapp-qa/.artifacts/prompt67-browser-qa.mjs`
  - Result: passed

Screenshots captured:

- [composition-pending-desktop.png](/Users/kevin/code/storyteller/tools/webapp-qa/.artifacts/prompt-67/composition-pending-desktop.png)
- [composition-pending-panel.png](/Users/kevin/code/storyteller/tools/webapp-qa/.artifacts/prompt-67/composition-pending-panel.png)
- [composition-pending-mobile.png](/Users/kevin/code/storyteller/tools/webapp-qa/.artifacts/prompt-67/composition-pending-mobile.png)
- [finalize-restore-desktop.png](/Users/kevin/code/storyteller/tools/webapp-qa/.artifacts/prompt-67/finalize-restore-desktop.png)
- [finalize-restore-panel.png](/Users/kevin/code/storyteller/tools/webapp-qa/.artifacts/prompt-67/finalize-restore-panel.png)

What I visually verified:

- The pending rewrite compare panel renders in the composition stage.
- Accept/reject/try-another controls are visibly attached to the compare UI.
- The narrow/mobile layout still exposes the pending rewrite decision controls.
- The finalize-stage compare view renders from `?stage=finalize`.
- Selecting the archived Chapter 1 revision in finalize exposes `Restore this revision`.

Observed runtime limitation during headless QA:

- The app shell logged a websocket warning for `ws://127.0.0.1:8566/api/v1/sessions/events/ws` closing before establishment in headless runs.
- Hydration and rendered compare UI still loaded correctly, so the screenshots and static-stage verification remained valid.

## LLM and prompt evaluation suite

No prompt assembly, model selection, eval criteria, or other LLM-facing behavior changed in this task.

Evaluation suite status:

- Not applicable

## Wrong turns, dead ends, and gotchas

- I initially wrote frontend test assertions that assumed a more aggressive diff merge strategy than `buildSegmentDiffSummary(...)` actually uses. I corrected the tests to reflect the real token-level behavior instead of overfitting the helper to the test.
- The first backend restore test uncovered a real production bug: restoring an archived revision wrote a second story asset to the same object path as the accepted rewrite snapshot. That failed on the unique `(storage_bucket, object_path)` constraint. The fix was to persist restored-version story snapshots under a unique artifact suffix.
- I accidentally introduced a regression in the accept route by deleting the request payload before reading `payload.origin`. Ruff caught the undefined-name bug before finalization, and I fixed it before the final verification pass.
- The initial browser QA scripts failed twice for uninteresting reasons:
  - shell quoting mangled inline JS heredocs
  - the first text wait was case-sensitive against uppercased UI labels
- The desktop viewport screenshots of the full page were too high in the shell chrome to be reviewer-friendly, so I added panel-focused captures as a second pass.

## Assumptions made while working unsupervised

- I assumed it was acceptable to create a disposable live QA session in the local Compose-backed development database because the run was explicitly unsupervised and the prompt required browser-based verification.
- I assumed restoring archived revisions should only be allowed for accepted saved versions, not pending rewrite candidates. Pending rewrite candidates still go through accept/reject review.
- I assumed a unique immutable story asset should be written whenever an archived version is restored, even if the same composition job originally produced the currently selected text.
- I assumed it was sufficient for final-review availability to be implemented through the workspace stage preview route (`?stage=finalize`) rather than requiring the durable session stage itself to be finalized.

## Final state

Code changes are committed on the current branch in:

- `1e1d30c` — `feat(prompt-67): diff and compare ui`

The remaining uncommitted filesystem noise at the end of the run is limited to `.yolopilot` run-log files plus this summary file.
