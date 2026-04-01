# Prompt 15 Summary: Event Log and Audit Trail

## What changed and why

I implemented the missing application layer around the existing `event_log_entries` table so session changes are now recorded through a consistent append-only contract instead of living only in materialized session rows.

The main goals were:

- make session history durable and queryable without browser-local state
- distinguish user, assistant, system/worker, and service-owned actions
- give event payloads a stable, versioned shape that can survive future prompt work
- wire current session mutations into the event log now, while also creating helper entry points for later prompts such as chat, UI echoes, composition streaming, and audio progress

The result is a new typed event taxonomy, a repository and service layer for appending and reading history, and service/test wiring so the current session lifecycle actually emits durable events.

## Architectural changes

### 1. Added a typed event taxonomy

New file: `backend/app/models/events.py`

This centralizes:

- canonical event type names in `SessionEventType`
- actor ownership via `EventActorType` and `SessionEventActor`
- typed payload models for:
  - session creation
  - workflow stage changes
  - selections
  - AI outputs
  - user edits
  - chat messages
  - UI actions
  - composition progress
  - audio progress
- payload serialization/parsing helpers
- `SessionEventView` and `SessionHistoryView` read models

Important design choice:

- I did **not** add a new database migration for payload versioning.
- The `event_log_entries` table already existed from prompt 11, so I made payloads durable by guaranteeing `schema_version` inside the JSON payload envelope.
- I updated docs to match that implemented shape.

### 2. Added an event repository

New file: `backend/app/repositories/events.py`

This repository is responsible for:

- appending events with a per-session `sequence_number`
- returning session history in sequence order
- supporting incremental reads with `after_sequence_number`
- returning the latest known sequence number for a session

Notable behavior:

- `list_for_session(limit=N)` returns the most recent `N` events in ascending order.
- `list_for_session(after_sequence_number=X)` returns tail events after `X`, also ascending.

### 3. Added a higher-level event logging service

New file: `backend/app/services/event_log.py`

This is the main abstraction future prompt work should call. It wraps the repository and provides:

- `append_event(...)`
- `record_session_created(...)`
- `record_stage_state_changed(...)`
- `record_selection(...)`
- `record_ai_output(...)`
- `record_user_edit(...)`
- `record_chat_message(...)`
- `record_ui_action(...)`
- `record_composition_progress(...)`
- `record_audio_progress(...)`
- `list_session_history(...)`

This layer also standardizes:

- default actor ownership
- event summaries
- payload version injection
- typed payload parsing on reads

### 4. Wired current session mutations into the event log

Updated file: `backend/app/services/sessions.py`

Changes:

- `create_session(...)` now records a `session.created` event
- `update_stage_state(...)` now records a `workflow.stage_changed` event
- stage changes now capture:
  - previous status
  - new status
  - detail
  - downstream invalidated stages
  - current/resume/furthest-completed/overall rollups
- affected `workflow_stage_states.last_event_id` pointers are updated so snapshots can explain why a stage is in its current state
- `SessionService.load_session_history(...)` now exposes the durable timeline via the service layer

This means the current snapshot model and the new event history now reinforce each other:

- snapshot rows stay fast to read
- event history explains how the snapshot was reached

### 5. Small supporting changes

Updated files:

- `backend/app/db/models.py`
- `backend/app/models/__init__.py`
- `backend/app/repositories/__init__.py`
- `backend/app/repositories/sessions.py`
- `backend/app/services/__init__.py`

Key supporting work:

- moved `EventActorType` into the model layer so event models do not depend on `app.db`
- exported the new models and services
- added `StorySessionRepository.exists(...)` for history reads

### 6. Added documentation for the taxonomy

New file: `docs/event-taxonomy.md`

This documents:

- actor ownership rules
- canonical event families
- payload versioning strategy
- helper entry points
- extension rules
- concrete usage examples

Also updated:

- `docs/README.md` to link the new doc
- `docs/domain-model.md` so the event entry describes payload versioning correctly

## How to use the new abstractions

### Record a selection

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

### Record a stage transition from another service

```python
event_log.record_stage_state_changed(
    session_id,
    stage=WorkflowStage.BRIEF,
    previous_status=WorkflowStageState.COMPLETED,
    status=WorkflowStageState.COMPLETED,
    detail="Accepted a revised brief.",
    invalidated_stages=[WorkflowStage.PITCHES, WorkflowStage.CHARACTERS],
    current_stage=WorkflowStage.PITCHES,
    resume_stage=WorkflowStage.PITCHES,
    furthest_completed_stage=WorkflowStage.STORY_SETUP,
    overall_status=WorkflowStageState.NEEDS_REGENERATION,
)
```

### Append a lower-level custom event

```python
from app.db import EventActorType
from app.models import SessionEventActor

event_log.append_event(
    session_id,
    actor=SessionEventActor(actor_type=EventActorType.SERVICE, actor_id="timeline-api"),
    event_type="timeline.custom_synced",
    summary="Synced session history for an API consumer.",
    payload={"source": "timeline-api"},
)
```

Even the raw mapping case above is normalized to include:

```json
{"schema_version": 1, "source": "timeline-api"}
```

### Read history

```python
history = SessionService(db_session).load_session_history(
    session_id,
    after_sequence_number=10,
)
```

That returns:

- `latest_sequence_number`
- ordered `events`
- typed payloads for known event types
- raw mappings for unknown event types

## Verification performed

### Targeted verification

Commands run:

- `pytest backend/tests/test_event_log_service.py backend/tests/test_session_service.py`
- `ruff check backend/app backend/tests`

Results:

- targeted pytest run: `10 passed`
- ruff: passed

### Broader backend verification

Command run:

- `pytest backend/tests`

Result:

- full backend suite: `36 passed`

Coverage from the new tests includes:

- session creation emits a durable `session.created` event
- stage changes emit `workflow.stage_changed` events
- downstream invalidations attach the same causal event to stale stages
- event history loads in sequence order
- typed payloads round-trip through the service layer
- incremental history reads with `after_sequence_number` work
- user, assistant, system, and service actors are all distinguishable

### Builds, browser checks, screenshots, and UI verification

- No frontend files or browser-visible behavior changed.
- No browser checks or screenshots were run.
- No frontend build or UI visual QA was necessary for this prompt.

### LLM or prompt evaluation suite

- No LLM-facing prompts, model wiring, eval harnesses, or prompt assembly logic were changed.
- No LLM evaluation suite was added for this task.
- Evaluation status: `N/A`

## Wrong turns, dead ends, and gotchas

### Wrong turn: circular import

My first pass put `EventActorType` in `app.db` and imported it into the new event models.
That created a circular import during test collection because `app.db.models` depends on `app.models.workflow`, while `app.models.__init__` now loads the new event module.

Fix:

- moved `EventActorType` into `backend/app/models/events.py`
- made `backend/app/db/models.py` import it from there

That cleaned up the dependency direction and kept the model layer from depending on the DB package.

### Surprising existing repository behavior

The schema already had:

- `event_log_entries`
- `workflow_stage_states.last_event_id`

but there was no append/read access layer using them.

That meant the right implementation was not a new table, but rather activating an already-planned part of the schema with a real service contract.

### Versioning gotcha

The domain docs mentioned a version field for event entries, but the table did not have a dedicated version column.

Decision:

- keep the table stable
- version the payload envelope with `schema_version`
- document that explicitly

This avoids churn in the migration chain while still meeting the durability goal.

### Worktree gotcha

There were unrelated YoloPilot prompt artifacts already present in the worktree:

- `prompts/14-repositories-and-session-service.yolopilot.jsonlines`
- `prompts/14-repositories-and-session-service.yolopilot.md`
- `prompts/15-event-log-and-audit-trail.codex.jsonlines`
- `prompts/15-event-log-and-audit-trail.yolopilot.jsonlines`
- `prompts/15-event-log-and-audit-trail.yolopilot.md`

I left those untouched and committed only the prompt 15 code/docs/test changes.

## Assumptions made while working unsupervised

- Since prompt 90 has not landed yet, user-authored session mutations still default to the local identity shape `user/local-user`.
- Worker-owned progress events are currently modeled as `system/worker`.
- Service-owned synchronous backend activity can use `service/...` when a caller wants that distinction.
- The existing event table from prompt 11 was the intended durable home for this work, so adding a second event table would have been the wrong move.
- Because the current codebase has no session API endpoints yet, exposing history through the backend service layer was the right incremental step for prompt 15.

## Final state

The repository now has:

- a typed, documented event taxonomy
- a reusable append/read event service
- durable history reads through `SessionService.load_session_history(...)`
- event emission for current session lifecycle changes
- tests proving the audit trail works without browser-local state
