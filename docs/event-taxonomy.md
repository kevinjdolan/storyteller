# Event Taxonomy

This document defines the append-only event contract introduced in prompt 15.
The goal is to make session history durable enough for replay, resume debugging,
UI-to-chat coherence, and later real-time fan-out without relying on browser-only state.

## Design Rules

- Every event belongs to exactly one `story_session`.
- Events are append-only and ordered by a per-session `sequence_number`.
- Events always record an actor, a stable `event_type`, a human-readable `summary`,
  optional workflow-stage context, and a JSON payload.
- Payloads are versioned with `schema_version`, even when a caller supplies raw mappings.
- Actor ownership is explicit:
  - `user`: direct user actions from chat or UI.
  - `assistant`: model- or agent-authored actions and outputs.
  - `system`: worker-owned or infrastructure-owned progress events.
  - `service`: synchronous backend orchestration that is not best described as user or worker.

## Canonical Event Types

The backend centralizes these names in `backend/app/models/events.py` as `SessionEventType`.
New event types should be added there before they are emitted anywhere else.

| Event type | Purpose | Typical actor | Typical stage |
| --- | --- | --- | --- |
| `session.created` | Root audit entry for a new session. | `user` | none |
| `workflow.stage_changed` | Durable record of a stage transition and any downstream invalidations. | `user` | the changed stage |
| `selection.recorded` | Accepted or candidate selection for genre, tone, pitch, character sheet, beat sheet, or story setup. | `user` | stage-specific |
| `ai.output.recorded` | AI-generated batch or revision that the session may later accept or refine. | `assistant` | stage-specific |
| `content.user_edit.recorded` | Structured user-authored edits to durable planning or composition records. | `user` | stage-specific |
| `chat.message.recorded` | User, assistant, or system chat/history entry. | varies | optional |
| `ui.action.recorded` | Direct UI interactions that should survive refresh and replay. | `user` | optional |
| `composition.progress.recorded` | Durable composition job progress for replay and worker debugging. | `system` | `composition` |
| `audio.progress.recorded` | Durable narration job progress for replay and worker debugging. | `system` | `audio` |

## Payload Strategy

Known event types use typed Pydantic payload models in `backend/app/models/events.py`.
Those models all inherit from `EventPayload`, which guarantees a `schema_version` field.

Example payload shapes:

```json
{
  "schema_version": 1,
  "working_title": "Starlight Ferry"
}
```

```json
{
  "schema_version": 1,
  "previous_status": "completed",
  "status": "completed",
  "detail": "Accepted a revised brief.",
  "invalidated_stages": ["pitches", "characters", "beats", "composition", "audio", "finalize"],
  "current_stage": "pitches",
  "resume_stage": "pitches",
  "furthest_completed_stage": "story_setup",
  "overall_status": "needs_regeneration"
}
```

For one-off service-owned events that do not yet deserve a first-class payload class,
`SessionEventLogService.append_event(...)` still injects `schema_version: 1`
into raw mapping payloads so stored JSON ages predictably.

## Helper Entry Points

The primary append/read surface is `backend/app/services/event_log.py`.

Available helpers today:

- `record_session_created(...)`
- `record_stage_state_changed(...)`
- `record_selection(...)`
- `record_ai_output(...)`
- `record_user_edit(...)`
- `record_chat_message(...)`
- `record_ui_action(...)`
- `record_composition_progress(...)`
- `record_audio_progress(...)`
- `append_event(...)` for lower-level extension points
- `list_session_history(...)` for timeline reads

The repository below that surface is `EventLogRepository` in
`backend/app/repositories/events.py`. It is responsible for per-session sequencing and
ordered reads. Services should prefer the higher-level helper layer so summaries,
actor defaults, and payload versioning stay consistent.

## Usage Examples

Record a selection event:

```python
from app.models import SelectionKind, WorkflowStage
from app.services.event_log import SessionEventLogService

event_log = SessionEventLogService(db_session)
event_log.record_selection(
    session_id,
    selection_kind=SelectionKind.GENRE,
    stage=WorkflowStage.GENRE,
    selection_id="genre-1",
    slug="quest-fantasy",
    label="Quest Fantasy",
)
```

Record worker progress:

```python
event_log.record_composition_progress(
    session_id,
    job_id=composition_job.id,
    status="in_progress",
    progress_percent=62.5,
    current_segment_index=3,
    total_segments=5,
)
```

Read the durable timeline:

```python
history = event_log.list_session_history(session_id, after_sequence_number=10)
for event in history.events:
    print(event.sequence_number, event.event_type, event.summary)
```

## Extension Rules

- Prefer enriching an existing payload model over creating ad hoc keys in scattered callers.
- Keep payloads small but reconstructive: include stable identifiers, revision numbers,
  and enough context to explain what changed.
- Do not rewrite or delete historical events to "fix" history. Emit a new compensating event.
- When a workflow-stage event changes the truth seen by the UI, attach the emitted event
  back to affected `workflow_stage_states.last_event_id` so snapshots can explain why a stage looks the way it does.
