# Prompt 17 Summary: Realtime Event Schema and Channel Plan

## What I Changed and Why

This prompt established the payload contracts for server-to-client live updates before any websocket transport is implemented in detail.

The main outcome is a canonical realtime contract layer in the backend plus a checked-in JSON schema bundle and reviewer-facing documentation. I chose that shape because prompt 17 explicitly called for shared event definitions or JSON schemas, and the repository does not yet have a shared cross-language package. A transport-neutral schema bundle gives frontend and backend work a single contract without inventing an extra build step.

Concretely, I added:

- a new backend model module for realtime contracts,
- a generated schema bundle in `docs/`,
- a design document covering channel scope, replay, and event-log relationships,
- targeted contract tests and a schema snapshot check,
- small docs/index updates so the new contract is discoverable.

The design stays intentionally boring:

- one session channel per session id,
- a short list of event families,
- replayable events tied back to durable event-log sequence numbers,
- one explicitly ephemeral event family for composition text chunks.

That keeps the future websocket work straightforward and preserves room for replay, optimistic UI, and reconnect recovery.

## Architectural Changes Across the Codebase

### 1. Added a canonical realtime contract module

New file:

- `backend/app/models/realtime.py`

This module is now the canonical backend source for prompt-17 realtime contracts.

It introduces:

- `SessionSubscriptionRequest`
- `SessionSubscriptionAck`
- `SessionRealtimeEvent` as a discriminated union
- event payload models for:
  - `chat.message`
  - `workflow.stage_changed`
  - `ui.action_echo`
  - `composition.chunk`
  - `job.progress`
  - `job.status`
  - `error.notification`
- helper enums for delivery mode, replay strategy, job kind, job status, chunk kind, and severity
- `build_session_channel_name(session_id)` to keep channel naming centralized
- `get_realtime_contract_schema_bundle()` to export the checked-in JSON schema bundle

Important design decisions in this module:

- Replayable events and ephemeral events are separated structurally.
  - Durable events require `sequence_number` and `event_log_entry_id`.
  - Ephemeral events do not carry those fields.
- `composition.chunk` is the only ephemeral event family right now.
- `workflow.stage_changed` intentionally reuses the existing durable `WorkflowStageChangedEventPayload` so stage semantics do not drift between the event log and the live feed.
- `job.progress` and `job.status` now use explicit realtime job-status enums instead of free-form strings.

### 2. Exposed the new contracts through the existing model export surface

Updated file:

- `backend/app/models/__init__.py`

This keeps later backend work simple. Future transport code can import realtime contracts from `app.models` without knowing the file layout.

### 3. Added a machine-readable schema bundle

New file:

- `docs/realtime-events.schema.json`

This is generated from the canonical backend models and includes schemas for:

- `session_subscription_request`
- `session_subscription_ack`
- `session_event`

This is the shared contract artifact I chose instead of hand-maintained frontend/backend duplicate definitions.

### 4. Added the channel/replay design document

New file:

- `docs/realtime-events.md`

This doc explains:

- session-scoped channel naming
- subscription frames and acknowledgement frames
- the common event envelope
- each event family and its payload intent
- the durable event-log relationship
- local-development auth assumptions
- how `correlation_id` is reserved for optimistic UI reconciliation

### 5. Added contract tests and schema drift protection

New file:

- `backend/tests/test_realtime_contracts.py`

This test coverage verifies:

- channel naming rules,
- durable vs ephemeral event validation,
- invalid chunk payload rejection,
- checked-in schema bundle parity with generated output,
- reuse of existing event-actor semantics.

### 6. Updated docs navigation

Updated file:

- `docs/README.md`

This now lists both the human-readable realtime design doc and the schema bundle.

## Examples: How to Use the New Abstractions and Extension Points

### Build a canonical session channel name

```python
from app.models import build_session_channel_name

channel = build_session_channel_name("session-123")
assert channel == "session:session-123"
```

Use this instead of hardcoding channel formatting in future websocket handlers.

### Validate a subscription request

```python
from app.models import SessionSubscriptionRequest

request = SessionSubscriptionRequest.model_validate(
    {
        "action": "subscribe",
        "session_id": "session-123",
        "tab_id": "tab-9",
        "last_sequence_number": 41,
    }
)
```

This is the expected browser-to-server control frame for joining a session feed.

### Validate a replayable session event

```python
from app.models import SessionRealtimeEvent
from pydantic import TypeAdapter

event = TypeAdapter(SessionRealtimeEvent).validate_python(
    {
        "event_id": "rt-1",
        "type": "job.progress",
        "session_id": "session-123",
        "channel": "session:session-123",
        "actor": {"actor_type": "system", "actor_id": "worker"},
        "stage": "audio",
        "created_at": "2026-04-01T08:32:00Z",
        "delivery": "live",
        "sequence_number": 48,
        "event_log_entry_id": "event-log-48",
        "payload": {
            "job_id": "audio-job-1",
            "job_kind": "audio",
            "status": "in_progress",
            "progress_percent": 72.5,
        },
    }
)
```

This is the future transport-facing entrypoint for validating live session events.

### Export the schema bundle for tooling or code generation

```python
from app.models import get_realtime_contract_schema_bundle

bundle = get_realtime_contract_schema_bundle()
print(bundle["schemas"].keys())
```

This is the extension point I used to generate `docs/realtime-events.schema.json`, and it can later support codegen or transport smoke tests.

### Add a new realtime event family later

The intended extension path is:

1. Add a new payload model in `backend/app/models/realtime.py`.
2. Add a new concrete event model with a fixed `type`.
3. Add that event model to the `SessionRealtimeEvent` union.
4. Regenerate `docs/realtime-events.schema.json`.
5. Add contract tests covering validation and schema drift.

That keeps event additions explicit and auditable.

## Exact Verification Work Performed

### Schema generation

Ran:

```bash
cd backend
./.venv/bin/python - <<'PY'
from __future__ import annotations

import json
from pathlib import Path

from app.models import get_realtime_contract_schema_bundle

output_path = Path('..') / 'docs' / 'realtime-events.schema.json'
output_path.write_text(
    json.dumps(get_realtime_contract_schema_bundle(), indent=2, sort_keys=True) + '\n'
)
print(output_path.resolve())
PY
```

Result:

- regenerated `docs/realtime-events.schema.json` from the backend contract models

### Targeted lint verification

Ran:

```bash
cd backend
./.venv/bin/ruff check app/models/realtime.py app/models/__init__.py tests/test_realtime_contracts.py
```

Result:

- passed

I also ran:

```bash
cd backend
./.venv/bin/ruff check --fix app/models/__init__.py
```

Reason:

- Ruff reported one import-order issue after I tightened the export surface. This was a mechanical fix only.

### Targeted automated tests

Ran:

```bash
cd backend
./.venv/bin/pytest tests/test_realtime_contracts.py tests/test_event_log_service.py
```

Result:

- 7 tests collected
- 7 tests passed

Coverage from this pass:

- realtime contract validation
- schema bundle drift protection
- compatibility with the existing durable event-log service

### Full backend regression suite

Ran:

```bash
cd backend
./.venv/bin/pytest
```

Result:

- 44 tests collected
- 44 tests passed

Reason for the broader run:

- `app.models.__init__` is a shared import surface and I wanted to make sure the new realtime exports did not accidentally break existing model consumers.

### Browser checks, screenshots, and UI verification

None performed.

Reason:

- this prompt changed backend contracts, documentation, and generated schemas only
- no frontend rendering, styling, layout, accessibility, or interactive UI behavior changed

### Builds and type checks not run

I did not run frontend build or frontend tests.

Reason:

- no frontend source files changed
- the shared contract deliverable for this prompt is the JSON schema bundle, not a new frontend runtime module

## LLM / Prompt Evaluation Suite

No LLM or prompt evaluation suite was added for this prompt.

Reason:

- I did not modify prompt text, model wiring, tool selection logic, or inference behavior
- this task was limited to transport/event-schema definition and documentation

Evaluation status:

- not applicable

## Wrong Turns, Dead Ends, Surprising Behavior, and Gotchas

### 1. I initially left job status fields as plain strings

That was too loose for a contract file whose main job is to stabilize transport expectations. Before final verification, I changed `job.progress.status` and `job.status.status` to use an explicit realtime job-status enum:

- `queued`
- `in_progress`
- `paused`
- `completed`
- `failed`
- `cancelled`

That made the schema materially better for future frontend handling and code generation.

### 2. I considered adding a separate frontend TypeScript mirror of the same schema

I decided against that for this prompt because it would create two hand-maintained sources of truth immediately. The repository does not yet have a shared cross-language package, so the cleaner move here was:

- canonical backend models
- generated JSON schema bundle
- documentation explaining usage and replay behavior

If prompt 29 or later transport work wants ergonomic frontend types, those should be derived from or kept intentionally adjacent to this schema rather than silently diverging from it.

### 3. The checked-in schema bundle is large

That is expected because Pydantic emits a full discriminated-union schema with all referenced definitions. I kept it anyway because:

- it is machine-readable,
- it is generated from canonical models,
- and the schema drift test prevents accidental mismatch.

### 4. The worktree started dirty

Unrelated prompt-run artifact files were already modified or untracked when I began:

- `prompts/16-asset-metadata-and-file-records.yolopilot.jsonlines`
- `prompts/16-asset-metadata-and-file-records.yolopilot.md`
- prompt-17 runner artifact files under `prompts/`

I left those untouched and committed only the prompt-17 implementation files.

## Assumptions I Had to Make While Working Unsupervised

### 1. JSON schema counts as the required shared contract artifact

I assumed the prompt’s “shared event type definitions or JSON schemas” requirement is satisfied by a generated schema bundle checked into `docs/`. That seemed like the best fit for the current repo shape.

### 2. One browser workspace tab subscribes to one session at a time

I assumed that is the intended transport model for the initial socket design. Multiple tabs can still subscribe to the same session, but a single tab should not multiplex unrelated sessions through one feed.

### 3. `composition.chunk` should remain ephemeral

I assumed partial typewriter chunks should not be persisted into the durable event log. That keeps the log useful for replay without turning it into a token stream. Recovery is instead expected to come from session hydration plus durable progress/status events.

### 4. Replay fallback will use the future session hydration endpoint

Prompt 38 has not been implemented yet, but prompt 17 needed a replay/hydration story now. I assumed it is correct to reserve `replay_strategy: "hydrate"` in the acknowledgement contract and document that fallback rather than inventing a temporary alternate path.

### 5. Local development auth remains permissive but session-scoped

I assumed the local single-user environment should not require real auth yet, while still documenting that future auth should gate channel joins by session ownership.

## Commit Checkpoint

I created a checkpoint commit for the implementation work before writing this summary:

- `784700f` — `feat(prompt-17): realtime event schema`

This summary file was intentionally written after implementation and verification, as required.
