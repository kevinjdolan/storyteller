# Story Workflow Tool Registry

This document describes the shared backend registry for story-stage operations that may be called by
chat translation, background workers, and future orchestration code.

Code entrypoints:

- [`backend/app/models/story_tools.py`](/Users/kevin/code/storyteller/backend/app/models/story_tools.py)
- [`backend/app/services/story_tools.py`](/Users/kevin/code/storyteller/backend/app/services/story_tools.py)
- [`backend/app/worker/default_handlers.py`](/Users/kevin/code/storyteller/backend/app/worker/default_handlers.py)

## What The Registry Solves

Before prompt 37, the backend had:

- chat actions and prompt catalogs for intent parsing
- a worker job handler registry
- durable session and job services

But it did not have one canonical place to describe story operations such as pitch generation,
beat-sheet generation, setup updates, composition rewrites, or audio start-up.

The story workflow tool registry now centralizes:

- tool name
- workflow stage
- request model
- result model
- preferred execution mode
- worker job type
- related chat actions
- side-effect documentation

## Tool Catalog

| Tool | Stage | Mode | Worker job type | Related chat actions | Result shape | Durable side effects |
| --- | --- | --- | --- | --- | --- | --- |
| `generate_pitches` | `pitches` | `background` | `story.generate_pitches` | `regenerate_pitches` | `StageOperationToolResult` | marks `pitches` in progress and refreshes downstream staleness |
| `refine_pitch` | `pitches` | `background` | `story.refine_pitch` | `regenerate_pitches` | `StageOperationToolResult` | marks `pitches` in progress for a targeted pitch revision |
| `generate_character_sheets` | `characters` | `background` | `story.generate_character_sheets` | `regenerate_character_sheet` | `StageOperationToolResult` | marks `characters` in progress and invalidates later planning |
| `refine_character_sheet` | `characters` | `background` | `story.refine_character_sheet` | `refine_character_sheet` | `StageOperationToolResult` | marks `characters` in progress for a revision pass |
| `generate_beat_sheet` | `beats` | `background` | `story.generate_beat_sheet` | `refine_beat_sheet`, `regenerate_beat_sheet` | `StageOperationToolResult` | marks `beats` in progress and invalidates composition work |
| `update_setup_heuristics` | `story_setup` | `direct` | `story.update_setup_heuristics` | `update_story_setup` | `UpdateSetupHeuristicsToolResult` | creates a selected `story_setups` revision, records user-edit and selection events, invalidates downstream stages, cancels active composition/audio jobs |
| `compose_next_segment` | `composition` | `background` | `story.compose_next_segment` | `start_composition` | `CompositionToolResult` | cancels active composition jobs, creates a composition job, seeds a segment row, records initial progress |
| `rewrite_segments` | `composition` | `background` | `story.rewrite_segments` | `start_composition`, `redirect_composition` | `CompositionToolResult` | cancels active composition jobs, creates a rewrite job, seeds a revised segment row, records initial progress |
| `estimate_audio_length` | `audio` | `direct` | `story.estimate_audio_length` | `start_audio_generation` | `EstimateAudioLengthToolResult` | computes an estimate from composition segments or story-setup targets without mutating durable state |
| `start_audio_generation` | `audio` | `background` | `story.start_audio_generation` | `start_audio_generation` | `StartAudioGenerationToolResult` | cancels active audio jobs, creates an audio job, records an estimate, marks `audio` in progress |

## Shared Interfaces

The registry stores request and response models per tool. Examples:

- `GeneratePitchesToolInput`
- `UpdateSetupHeuristicsToolInput`
- `ComposeNextSegmentToolInput`
- `EstimateAudioLengthToolResult`
- `StartAudioGenerationToolResult`

Those contracts are exported through [`backend/app/models/__init__.py`](/Users/kevin/code/storyteller/backend/app/models/__init__.py), so callers do not need to reach into a private module to use them.

## How Callers Use It

Direct execution:

```python
from app.models import StoryWorkflowToolName
from app.services import StoryWorkflowToolService

result = StoryWorkflowToolService(session).execute(
    tool_name=StoryWorkflowToolName.UPDATE_SETUP_HEURISTICS,
    session_id=session_id,
    arguments={
        "target_runtime_minutes": 8,
        "chapter_count": 2,
    },
)
```

Background enqueue:

```python
queued = StoryWorkflowToolService(session).enqueue(
    tool_name="compose_next_segment",
    session_id=session_id,
    arguments={"instructions": "Write the next calm scene."},
)
```

Chat-action routing:

```python
from app.services import StoryWorkflowActionRouter

plan = StoryWorkflowActionRouter().plan_calls(
    session_id=session_id,
    batch=parsed_chat_actions,
)
```

The action router deliberately maps only story-operation actions. UI-only actions such as stage
navigation or asset download remain outside this registry.

## Worker Integration

[`backend/app/worker/default_handlers.py`](/Users/kevin/code/storyteller/backend/app/worker/default_handlers.py)
now auto-registers one handler per tool job type. Each handler:

1. Looks up the tool definition from the shared registry.
2. Validates the job payload against the tool request model.
3. Opens a database session through `JobExecutionContext.with_session(...)`.
4. Calls `StoryWorkflowToolService.execute(...)`.
5. Returns the typed result as the durable background job summary.

That keeps worker dispatch and direct orchestration on the same tool names and result contracts.

## Prompt Exposure

The intent-parser prompt still emits chat actions, but it now also receives a serialized summary of
the shared tool registry. That gives the LLM-facing layer the same backend vocabulary that workers
and future orchestration code see.

Relevant files:

- [`backend/app/ai/intent_parser.py`](/Users/kevin/code/storyteller/backend/app/ai/intent_parser.py)
- [`backend/app/ai/prompts/intent_parser.md`](/Users/kevin/code/storyteller/backend/app/ai/prompts/intent_parser.md)

## Adding A New Tool Later

1. Add request and result models in [`backend/app/models/story_tools.py`](/Users/kevin/code/storyteller/backend/app/models/story_tools.py).
2. Add a `StoryWorkflowToolDefinition` entry in [`backend/app/services/story_tools.py`](/Users/kevin/code/storyteller/backend/app/services/story_tools.py).
3. Implement the matching executor method on `StoryWorkflowToolService`.
4. Add chat-action routing if the tool should be reachable from parsed chat actions.
5. Add tests for registry listing, direct execution, worker dispatch, and prompt exposure if the tool is LLM-facing.

No extra worker-registration code is needed if the new tool definition includes a unique `job_type`.
