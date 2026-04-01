# Domain Model and Session State Machine

This document defines the durable business objects and workflow rules for a single story-creation session. The goal is to give the backend, frontend, migrations, and later AI orchestration code one shared contract for how a session progresses, pauses, rewinds, and resumes.

## Core Modeling Rules

- The `story_session` is the durable unit of work.
- Workflow truth lives on the backend, not in browser-only UI state.
- Every workflow stage is tracked explicitly, even when later stages are generated from earlier ones.
- Backward edits are allowed on purpose and must mark downstream outputs stale instead of silently pretending they are still current.
- Composition and audio are long-running workflows backed by durable records, not one-shot request responses.
- Event history is append-only and explains how the current snapshot was reached.

## Session Snapshot Contract

The session snapshot returned to the UI should eventually include these fields, even if some land in later prompts:

| Field | Purpose |
| --- | --- |
| `id` | Stable UUID for the story session. |
| `working_title` | Best current human-readable label for lists and search. |
| `current_stage` | Stage the user is actively viewing or editing right now. |
| `resume_stage` | Earliest stage that still needs work when a session is reopened. |
| `furthest_completed_stage` | Highest ordered stage that is still valid and completed. |
| `overall_status` | Session-level rollup such as `draft`, `in_progress`, `completed`, or `needs_regeneration`. |
| `selected_genre_id` | Accepted genre catalog row for the session. |
| `selected_tone_profile_id` | Accepted tone profile row for the session. |
| `selected_pitch_id` | Accepted pitch record. |
| `selected_character_sheet_id` | Accepted character-sheet record. |
| `accepted_beat_sheet_id` | Accepted beat-sheet record. |
| `story_setup_id` | Accepted story-setup preferences record. |
| `active_composition_job_id` | Current composition job, if writing or rewrite work is running. |
| `active_audio_job_id` | Current audio job, if narration work is running. |
| `latest_story_asset_id` | Most recent readable story artifact or aggregate text record. |
| `latest_audio_asset_id` | Most recent playable final audio artifact. |
| `created_at`, `updated_at`, `completed_at` | Audit and list-view timestamps. |

`resume_stage` is the key anti-guessing field. The backend computes it from durable stage states so the frontend does not need to infer where to reopen a session by looking at which panels happen to have data.

Prompt 11 keeps the relational core intentionally one-directional where practical: child records
such as pitches, character sheets, beat sheets, and setup revisions point back to the owning
session, and the accepted row is tracked on the child record itself. The API snapshot can still
surface selected child IDs without forcing the first migration into a web of circular foreign keys.

## Major Entities

| Entity | Durable role | Key fields | Notes |
| --- | --- | --- | --- |
| `story_session` | Root aggregate for one bedtime-story project. | IDs, title, stage pointers, overall status, timestamps. | Owns the current accepted choices and job pointers. |
| `workflow_stage_state` | Per-stage state for the session. | `session_id`, `stage`, `status`, `updated_at`, `last_event_id`. | Stored explicitly so resume does not depend on sparse child tables. |
| `genre` | Curated genre catalog entry. | slug, label, description, bedtime-safety notes, arc notes. | Backend-owned reference data. |
| `tone_profile` | Curated tone option linked to a genre. | `genre_id`, slug, label, descriptors, bedtime notes, default planning hints. | Tone choices are filtered by genre. |
| `story_brief` | User-authored idea plus any normalized planning summary. | raw brief text, normalized summary, revision number. | Keeps user input separate from later generated planning outputs. |
| `pitch` | One candidate story premise. | batch or generation group, summary, hook, bedtime notes, selection flag. | `selected_pitch_id` on the session represents the accepted pitch; selection does not require a separate table. |
| `character_sheet` | Accepted cast and character traits for the chosen direction. | protagonist/supporting cast data, revision, generation metadata. | Multiple revisions may exist; the session points at the accepted one. |
| `beat_sheet` | Structured Save-the-Cat plan. | ordered beats, bedtime-adaptation notes, revision. | Must be editable and versioned. |
| `story_setup` | Soft planning targets. | target words, target runtime, chapter count, chapter style, notes. | These are guides, not hard constraints. |
| `composition_job` | Parent job record for writing or rewriting text. | status, progress, attempt count, stop reason, current segment pointer. | Not listed in the prompt title, but needed to make `composition_segment` durable and resumable. |
| `composition_segment` | One planned or written segment of the story. | segment index, planned summary, text, revision number, superseded segment, status. | Supports interruption, partial persistence, and rewrites of earlier sections. |
| `audio_job` | Parent job record for narration generation. | voice, speed, music setting, progress, status, compiled asset pointer. | Audio should be resumable and segment-aware. |
| `export_asset` | Durable artifact metadata for text and audio outputs. | asset kind, storage key, MIME type, byte size, checksum, readiness status. | Covers `.docx`, final audio, and intermediate durable artifacts when needed. |
| `event_log_entry` | Append-only session history. | actor, event type, stage context, payload, created_at, version. | Supports replay, resume hydration, debugging, and audit. |

## Canonical Workflow Stages

These lowercase identifiers are the wire-format contract. API payloads should use the IDs, not numeric indexes or UI labels.

| Order | Stage ID | UI label | Stage completes when |
| --- | --- | --- | --- |
| 1 | `genre` | Genre | The user accepts a genre for the session. |
| 2 | `tone` | Tone | The user accepts a tone profile for the selected genre. |
| 3 | `brief` | Story brief | The session has an accepted free-form brief and any required normalized summary. |
| 4 | `pitches` | Pitches | One pitch is accepted or the user intentionally keeps a current pitch set for further refinement. |
| 5 | `characters` | Characters | One character sheet is accepted. |
| 6 | `beats` | Beat sheet | One beat sheet is accepted. |
| 7 | `story_setup` | Story setup | The user accepts soft targets such as runtime and chapter plan. |
| 8 | `composition` | Composition | The current story text is complete enough to hand off to narration. |
| 9 | `audio` | Audio | Final narration assets are generated for the current story text and settings. |
| 10 | `finalize` | Finalize | Read/listen/download assets are ready for the current accepted story state. |

Current code mirrors this contract in:

- `backend/app/models/workflow.py`
- `frontend/src/features/session/workflowStages.ts`

The backend remains the authority for validating transitions. The frontend should use the same literal IDs for rendering, navigation, and optimistic display only.

## Stage State Semantics

The same four-state lifecycle should be used for stage rows and for generated artifacts that can become stale.

| State | Meaning | Example |
| --- | --- | --- |
| `draft` | The stage has no accepted durable output yet. Partial input may exist, but the stage is not considered complete. | The user typed part of a brief but has not accepted it yet. |
| `in_progress` | Durable work is actively being produced or updated. | Pitch generation is running, composition is streaming segments, or audio rendering is underway. |
| `completed` | The stage has an accepted output that is still valid relative to all upstream dependencies. | A beat sheet was accepted and no upstream planning change has made it stale. |
| `needs_regeneration` | The stage was completed before, but an upstream change made its accepted output stale. The old output may remain visible for comparison, but it is not the current source of truth. | The user edits characters after a beat sheet exists, so beats, composition, audio, and finalize become stale. |

### Session-Level Rollup

The session-level `overall_status` should be derived, not manually entered:

- `draft`: no stage has reached `completed` yet.
- `in_progress`: at least one stage is `in_progress`, or some stages are completed but the session has not reached a valid finalization state.
- `completed`: `finalize` is `completed` and no stage is `needs_regeneration`.
- `needs_regeneration`: one or more stages are `needs_regeneration`, even if the session also has readable prior outputs.

## Allowed Forward Progression

The default happy-path order is linear:

`genre -> tone -> brief -> pitches -> characters -> beats -> story_setup -> composition -> audio -> finalize`

Forward movement rule:

- The user may enter the next stage once the current stage is `completed`.

Resume rule:

- On reopen, the backend should send the earliest stage whose state is not `completed`.
- If all stages are `completed`, `resume_stage` is `finalize`.

This is the behavior implemented by the `resolve_resume_stage` helper in both the backend and frontend contract files.

## Safe Backward Edits and Regeneration Rules

Backward navigation is allowed to any already-reached earlier stage. The important rule is what happens after the user accepts a change there.

| Edited stage | Stages marked `needs_regeneration` after acceptance |
| --- | --- |
| `genre` | `tone`, `brief`, `pitches`, `characters`, `beats`, `composition`, `audio`, `finalize` |
| `tone` | `brief`, `pitches`, `characters`, `beats`, `composition`, `audio`, `finalize` |
| `brief` | `pitches`, `characters`, `beats`, `composition`, `audio`, `finalize` |
| `pitches` | `characters`, `beats`, `composition`, `audio`, `finalize` |
| `characters` | `beats`, `composition`, `audio`, `finalize` |
| `beats` | `composition`, `audio`, `finalize` |
| `story_setup` | `composition`, `audio`, `finalize` |
| `composition` | `audio`, `finalize` |
| `audio` | `finalize` |
| `finalize` | none |

Why `story_setup` is not invalidated by earlier planning edits:

- Word count, runtime, and chapter preferences are user intent, not generated story content.
- They still influence later composition, but a new pitch or character sheet does not automatically erase the user's preferred target length.

## Composition Interruption and Rewrite Rules

Composition is intentionally more flexible than the earlier planning stages.

- A composition job may move between `in_progress`, paused, resumed, or cancelled states without leaving the `composition` stage.
- Partial text is persisted segment by segment so a refresh or crash does not erase progress.
- A rewrite request against an earlier segment creates a new `composition_job` or new segment revision rather than mutating history in place.
- Superseded segments remain durable for comparison and audit.
- Any accepted composition rewrite marks `audio` and `finalize` as `needs_regeneration`.
- If the user decides the plan itself is wrong, they may navigate back to `beats` or `story_setup`, accept changes there, and let the backend mark `composition` and later stages stale.

## Re-entry From Past Sessions

The system should support these reopen flows without guessing from UI state:

1. Planning session reopened midstream:
   - Example: `genre`, `tone`, and `brief` are `completed`; `pitches` is `in_progress`.
   - Result: open the session on `resume_stage = pitches`.
2. Finished draft reopened for upstream change:
   - Example: `composition`, `audio`, and `finalize` were `completed`, then the user edits the beat sheet.
   - Result: `composition`, `audio`, and `finalize` become `needs_regeneration`, and `resume_stage = composition`.
3. Fully completed story reopened for reading only:
   - Example: every stage is `completed`.
   - Result: open on `resume_stage = finalize`, but still allow explicit navigation back to earlier stages for edits.

## Shared Enum and Constants Plan

The repo does not yet have a generated cross-language schema package, so prompt 10 uses a boring mirrored-contract approach:

- Backend authority: `backend/app/models/workflow.py`
- Frontend mirror for rendering and client-side navigation: `frontend/src/features/session/workflowStages.ts`
- Tests on both sides assert the same stage order, lifecycle states, and regeneration map.

Rules for later prompts:

- Keep the literal stage IDs stable once APIs start returning them.
- Keep the literal stage-state values stable once they enter database rows or websocket payloads.
- If a later prompt introduces JSON Schema or code generation, generate from these same identifiers instead of renaming them.
- The backend service layer, not the frontend, decides whether a requested stage transition is valid for the current session snapshot.
