# Prompt 64: Agent Summary Messages During Composition

## What I changed and why

I implemented durable, checkpoint-based assistant summary messages during story composition so the chat pane now tells the user what the system is currently writing, where the narrative is headed next, and what immediate thematic focus is being worked on. The goal was to make interruption decisions informed and timely instead of forcing the user to infer progress from raw text streaming alone.

The implementation is tied to actual composition progress rather than timers. Mid-segment summary messages are emitted at meaningful chunk-based checkpoints, and a final handoff summary is emitted when the segment finishes. All summaries are grounded in already generated segment text plus the active segment prompt metadata, so they describe real work in progress instead of generic process narration.

The code change was committed as:

- `1378882` — `feat(prompt-64): agent summary messages during composition`

## Architectural changes across the codebase

### Backend composition service

Most of the work lives in `backend/app/services/composition_jobs.py`.

I added a lightweight checkpoint model and a summary pipeline inside the existing composition job flow:

- `CompositionSummaryCheckpoint`
  - Stores the checkpoint key, target chunk index, and progress ratio used to determine when to emit a summary.
- `_plan_composition_summary_checkpoints(total_chunks)`
  - Converts chunk counts into meaningful progress checkpoints.
  - Current strategy is roughly one-third and two-thirds progress for multi-chunk segments.
- `_record_composition_summary_checkpoint(...)`
  - Builds and records the chat-style assistant message when a checkpoint is reached.
- `_build_composition_summary_message(...)`
  - Produces the compact user-facing message body.
- `_build_generated_summary_excerpt(...)`
  - Pulls grounded phrasing from generated story text instead of inventing a meta summary.
- `_resolve_summary_direction(...)`
  - Derives the next narrative direction from the segment prompt.
- `_resolve_summary_focus(...)`
  - Extracts the immediate thematic or beat-level focus from the segment prompt.
- `_build_composition_summary_message_id(job_id, segment_id, checkpoint_key)`
  - Produces stable message IDs so replay/resume behavior stays deterministic.

### Durable deduplication for resume safety

Composition can resume or re-enter a partially completed job, so summary emission had to be idempotent. I added durable checkpoint tracking inside composition job metadata:

- Metadata key: `composition_job.metadata_json["emitted_summary_checkpoints"]`
- Helper methods:
  - `_read_summary_checkpoint_state`
  - `_has_emitted_summary_checkpoint`
  - `_mark_summary_checkpoint_emitted`

This prevents duplicate assistant summary messages if a job is retried or the worker restarts after some progress has already been recorded.

### Chat integration

I intentionally reused the existing durable chat/event pipeline instead of introducing a new realtime event contract. Summary messages are recorded through `SessionEventLogService.record_chat_message(...)` with:

- `role = ChatMessageRole.ASSISTANT`
- `source = "composition_summary"`
- `actor = DEFAULT_ASSISTANT_ACTOR`

That means:

- existing chat hydration picks them up automatically
- existing realtime session updates deliver them automatically
- existing session replay behavior does not need a frontend-specific patch

### Frontend impact

No frontend code changes were required. The existing transcript rendering and session hydration logic already handled durable assistant chat messages, so the backend integration was enough to make summaries appear live and persist across refresh/replay.

## Checkpoint strategy

The summary cadence is progress-driven, not time-driven.

Current strategy:

- 1 chunk: no mid-segment summary, because there is no meaningful checkpoint before completion
- 2 chunks: one mid-segment summary at the first chunk boundary
- 3+ chunks: summaries at approximately 34% and 67% progress
- segment completion: a final handoff summary after the segment is fully generated

This gives the user insight at narrative checkpoints that usually correspond to real movement in the scene instead of arbitrary wall-clock intervals.

## New abstractions, helpers, and extension points

### 1. Adjusting summary cadence

The cadence is controlled by:

- `_COMPOSITION_SUMMARY_PROGRESS_CHECKPOINTS = (0.34, 0.67)`

If a later prompt or product decision wants denser updates, that tuple is the main extension point. For example, moving to `(0.25, 0.5, 0.75)` would produce three mid-segment checkpoints for sufficiently chunked segments.

### 2. Adjusting message copy

The message body is centralized in:

- `_build_composition_summary_message(...)`

If product copy changes later, this is the place to adjust phrasing, compactness, or the balance between:

- progress
- generated excerpt
- direction
- focus

### 3. Swapping grounding heuristics

The grounding behavior is intentionally isolated:

- `_build_generated_summary_excerpt(...)`
- `_normalize_summary_fragment(...)`
- `_truncate_summary_text(...)`

If later prompts want better semantic summarization, these helpers are the natural insertion point for a richer summarizer without having to restructure the job loop.

### 4. Persisted idempotency behavior

Resume-safe emission is isolated behind:

- `_has_emitted_summary_checkpoint(...)`
- `_mark_summary_checkpoint_emitted(...)`

That means future background-job features can reuse the same pattern for checkpointed chat notifications without having to invent a second dedupe mechanism.

## Example usage patterns

### Example: where summaries are emitted in the job loop

During `CompositionJobService.run_job`, each streamed chunk advances composition progress. When the loop reaches a planned checkpoint, the service records a durable assistant chat message before continuing.

Conceptually:

1. stream segment chunks
2. append generated text
3. compare current chunk index to planned summary checkpoints
4. if a checkpoint is newly reached, emit `composition_summary` assistant message
5. continue streaming
6. emit final segment handoff summary when the segment completes

### Example: reading dedupe state

The persisted metadata shape is effectively:

```json
{
  "emitted_summary_checkpoints": {
    "<segment-id>": ["progress-34", "progress-67", "segment-complete"]
  }
}
```

That state ensures a resumed worker does not replay already-emitted summaries.

### Example: expected summary style

The summaries are intentionally short and operational. In live verification they looked like:

- `Writing update 89% (3/3): ... Direction: ... Focus: ...`
- `Segment 3/3 handoff: ...`

The exact wording varies with the generated text and segment prompt, but the structure is compact enough to scan quickly in the chat lane.

## Files touched

- `backend/app/services/composition_jobs.py`
- `backend/tests/test_story_tools.py`

## Verification work performed

I verified this feature at the unit, integration, lint, frontend build, and browser/live-system levels.

### Automated backend verification

Command:

```bash
pytest backend/tests/test_story_tools.py -q
```

Result:

- `26 passed in 3.04s`

This includes the new summary-checkpoint tests described below.

Command:

```bash
pytest backend/tests/test_session_api.py -q -k 'session_realtime_service_streams_composition_chunk_deltas or session_realtime_service_suppresses_initial_chunk_baseline_and_keeps_snapshot_recoverable or hydrate_session_endpoint_preserves_chat_navigation_bridge_history'
```

Result:

- `3 passed, 36 deselected in 1.17s`

This was a regression check that the existing session hydration and realtime behavior still worked with the new durable chat messages flowing through the same pipeline.

### Lint verification

Command:

```bash
ruff check backend/app/services/composition_jobs.py backend/tests/test_story_tools.py
```

Result:

- `All checks passed!`

### Frontend regression verification

Command:

```bash
cd frontend && npm test -- --run src/features/session/chat/actionEchoes.test.ts src/features/session/sessionRuntimeStore.test.ts
```

Result:

- `Test Files 2 passed`
- `Tests 11 passed`

This was a targeted frontend regression check because the new messages rely on the existing transcript/session runtime flow rather than new UI code.

### Frontend build verification

Command:

```bash
cd frontend && npm run build
```

Result:

- build succeeded

Observed limit:

- Vite reported the existing large-chunk warning for `dist/assets/index-BdA0BHU3.js` at `560.51 kB` after minification.
- This did not fail the build and is not introduced by this task.

## Browser checks, live verification, and screenshots

Because this change affects the live user-facing composition experience, I also verified it through the running Docker Compose stack and browser UI.

### Compose environment

The local stack was already running on:

- backend: `http://127.0.0.1:8565`
- frontend: `http://127.0.0.1:8566`

I discovered that the running `backend` and `worker` containers were serving code loaded before my local changes, so I recreated the relevant services to ensure the live verification was hitting the new implementation:

```bash
docker compose -f infra/compose/docker-compose.yml up -d --force-recreate backend worker frontend
```

### Live session verification

I seeded a real session via the live API and ran it through the workflow into composition. The verified session ID was:

- `b3957146-e941-40d2-aa37-f611a1c8695b`

The seeding flow used the live backend endpoints to:

1. create a session
2. select genre and tone
3. save the story brief
4. generate and select a pitch
5. generate and select a character sheet
6. generate and select a beat sheet
7. save setup preferences
8. start composition

I then observed the chat transcript in the browser and confirmed that assistant summary messages appeared during active composition rather than only at the end.

### Screenshot evidence

Verified screenshot:

- `/Users/kevin/code/storyteller/.yolopilot/runs/20260331T205548_storyteller_prompt_pack/64_agent_summary_messages_during_composition/prompt64-summary-viewport.png`

What the screenshot demonstrates:

- assistant summary messages appear in the chat transcript during composition
- messages include progress context and concise narrative guidance
- the transcript persists the messages in the same conversation lane as other assistant output

### Visual coverage limits

I verified the presence and readability of the summaries in the transcript, but I did not exhaustively test multiple viewport sizes for this specific feature because the frontend rendering path itself did not change. The primary visual objective for this task was confirming that the new messages appear at the right moment in the live UI and remain readable in the existing chat layout.

## Evaluation suite for LLM/prompt-facing behavior

This task modified LLM-adjacent composition behavior, so I added explicit evaluation-style test coverage in `backend/tests/test_story_tools.py`.

### Evaluation: `test_eval_composition_summary_messages_stay_grounded_and_compact`

Criteria and outcomes:

- `mentions_progress`: pass
- `grounds_excerpt_in_generated_text`: pass
- `includes_direction`: pass
- `includes_focus`: pass
- `stays_compact_for_history_replay`: pass

Measured outcome:

- 5 of 5 criteria passed

This test checks the message-construction helper directly and confirms the summaries remain grounded, informative, and compact.

### Evaluation: `test_composition_job_service_records_checkpointed_summary_chat_messages`

Criteria and outcomes:

- `segment_completed_and_requeued`: pass
- `three_checkpoint_messages`: pass
- `assistant_role_only`: pass
- `composition_stage_only`: pass
- `stable_checkpoint_ids`: pass
- `checkpoint_state_persisted`: pass
- `messages_include_direction_and_focus`: pass

Measured outcome:

- 7 of 7 criteria passed

This verifies the end-to-end service behavior for checkpoint emission and durable persistence.

### Strategy test: `test_composition_summary_checkpoints_follow_meaningful_progress_steps`

Outcome:

- pass

Coverage:

- no meaningless mid-summary for one-chunk segments
- single midpoint for two-chunk segments
- two progress checkpoints for larger multi-chunk segments

## Wrong turns, dead ends, surprising behavior, and gotchas

### 1. First live verification appeared to fail

My first live API verification produced no composition summary messages for session:

- `a7dbebf9-0104-40e9-9e62-9e3f8977e50c`

The feature implementation was not actually wrong. The problem was that the already-running compose `backend` and `worker` processes had not reloaded the imported Python code after my edit. Recreating the services fixed that, and the subsequent live verification worked as expected.

### 2. Chat transcript layout made screenshot capture less straightforward

The page currently grows with the transcript in this state rather than cleanly constraining the transcript to an internal scroll region for all capture scenarios. That did not break the feature, but it did mean I had to scroll the page to capture the summary bubbles clearly. I did not change this behavior because it is outside the scope of prompt 64.

### 3. Local Gemini model calls returned 404s in this environment

During live verification, the configured local provider path returned 404s for Gemini model requests in this compose environment. The application’s existing fallback behavior still produced usable planning/composition outputs, so the feature could still be verified end to end. I did not change provider wiring as part of this task because that would have been a separate scope expansion.

## Assumptions I made while working unsupervised

- Reusing the existing durable `chat.message.recorded` pipeline was preferable to creating a new frontend-visible event type for composition summaries.
- A compact summary target around the current message length was the right tradeoff for transcript readability and session hydration history.
- Roughly one-third and two-thirds checkpoints, plus a final handoff, satisfy the prompt’s requirement for meaningful progress-linked updates.
- Summary grounding should prioritize already generated text plus active prompt metadata instead of making another model call, because that keeps the feature deterministic, cheap, and durable.
- No frontend code change was necessary because the existing transcript system already renders durable assistant chat messages correctly.

## Remaining limits and follow-up risks

- Summary cadence is heuristic and chunk-count-based rather than beat-aware. If later prompts want even smarter intervention timing, a beat-aware checkpoint planner would be a natural extension.
- The summary extractor is intentionally lightweight. It is grounded, but not semantically deep. If the product later needs richer mid-stream summaries, the helper boundary is ready for that upgrade.
- The live verification depended on fallback composition behavior because of the local provider 404 issue. The feature itself was still validated, but production-model phrasing could differ somewhat.

## Reviewer summary

This task adds compact, durable, progress-linked assistant summary messages during story composition without introducing new frontend contracts. The implementation is resume-safe, tied to actual generated work, and already integrated into the existing session hydration and chat replay system. Automated tests cover cadence, grounding, compactness, stable IDs, persistence, and end-to-end emission, and browser verification confirms the summaries appear in the live transcript during composition.
