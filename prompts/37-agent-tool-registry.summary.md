# Prompt 37 Summary: Agent Tool Registry for Story Workflow Operations

## What I Changed And Why

I added a shared story workflow tool system so backend story operations are described once and can
be consumed consistently by chat translation, background workers, and future orchestration code.

The main gap before this prompt was that the backend had:

- chat-to-UI actions and action-policy rules
- durable session and job services
- a worker job handler registry

but no central registry for story operations like pitch generation, beat generation, setup updates,
composition, or audio start-up. The action vocabulary was effectively split across prompt text,
action-policy logic, and worker job types.

This prompt adds that missing middle layer.

## Architectural Changes

### 1. Added typed story tool contracts

New file:

- `backend/app/models/story_tools.py`

This file defines:

- canonical tool names such as `generate_pitches`, `update_setup_heuristics`,
  `compose_next_segment`, and `start_audio_generation`
- typed request models for each tool
- typed result models for each tool
- side-effect metadata models
- generic `StoryWorkflowToolCall` and `StoryWorkflowToolPlan` structures used by the
  chat-action router

Why this matters:

- tool inputs and outputs are now explicit instead of being implied by prompt text or worker code
- later prompts can add tools without inventing new ad hoc payload formats

### 2. Added the shared registry and executor service

New file:

- `backend/app/services/story_tools.py`

This file contains:

- `StoryWorkflowToolDefinition`
- `StoryWorkflowToolRegistry`
- `StoryWorkflowToolService`
- `StoryWorkflowActionRouter`
- registry export helpers for schema and prompt catalogs

The registry is now the single source of truth for:

- tool name
- target workflow stage
- preferred execution mode
- worker job type
- request model
- result model
- related chat action types
- side-effect documentation

The executor service provides real business behavior for the tools that are already meaningful in
the current repo state:

- `update_setup_heuristics`
  - creates a new selected `StorySetup` revision
  - records user-edit and selection events
  - invalidates downstream stages
  - cancels active composition and audio jobs
- `compose_next_segment`
  - cancels active composition jobs
  - creates a new `CompositionJob`
  - seeds a `CompositionSegment`
  - records initial composition progress
- `rewrite_segments`
  - creates rewrite-mode composition jobs and segment revisions
- `estimate_audio_length`
  - estimates duration from composition segment word counts or story-setup targets
- `start_audio_generation`
  - cancels active audio jobs
  - creates a new `AudioJob`
  - records initial audio progress

For earlier planning tools like `generate_pitches`, `refine_pitch`, `generate_character_sheets`,
and `generate_beat_sheet`, the current implementation moves the appropriate stage into
`in_progress` with durable detail text. That is intentional for the current repository state,
because the actual Gemini-backed generation adapters for those stages are not implemented yet.

### 3. Connected chat-action routing to the same tool vocabulary

`StoryWorkflowActionRouter` now translates applicable `ChatToUIActionBatch` actions into
`StoryWorkflowToolCall` items.

Examples:

- `update_story_setup` -> `update_setup_heuristics`
- `start_composition` -> `compose_next_segment` or `rewrite_segments`
- `redirect_composition` -> `rewrite_segments`
- `start_audio_generation` -> `start_audio_generation`

This keeps UI/chat actions and backend story-operation names aligned without forcing UI-only actions
like stage navigation or asset download into the tool registry.

### 4. Connected worker dispatch to the same registry

Updated files:

- `backend/app/worker/runtime.py`
- `backend/app/worker/default_handlers.py`

Changes:

- `JobExecutionContext` now has `with_session(...)` so worker handlers can safely open a database
  session without duplicating session-management code
- the default worker registry now auto-registers one handler per story tool job type
- those handlers look up the tool definition from the shared registry and call
  `StoryWorkflowToolService.execute(...)`

This is the key alignment point for the acceptance criteria: worker execution now uses the same
tool registry and domain service layer as direct orchestration code.

### 5. Exposed the shared tool catalog to the intent parser prompt

Updated files:

- `backend/app/ai/intent_parser.py`
- `backend/app/ai/prompts/intent_parser.md`

The intent-parser prompt still emits chat actions, but it now receives a serialized summary of the
shared story tool registry under a dedicated "Related backend tool registry" section.

That gives the LLM-facing chat translation layer visibility into the same backend operation names
that workers and future model orchestration will use.

### 6. Exported the new interfaces through package surfaces

Updated files:

- `backend/app/models/__init__.py`
- `backend/app/services/__init__.py`

This keeps the new contracts discoverable from the same import surfaces the rest of the backend
already uses.

### 7. Added reviewer-facing documentation

Updated files:

- `docs/story-workflow-tool-registry.md`
- `docs/README.md`
- `backend/README.md`

The new doc explains:

- the registry structure
- the tool catalog
- how direct execution works
- how background enqueue works
- how chat actions map into tool calls
- how to add another tool later

## Examples And Extension Points

### Direct execution

```python
result = StoryWorkflowToolService(session).execute(
    tool_name="update_setup_heuristics",
    session_id=session_id,
    arguments={"target_runtime_minutes": 8, "chapter_count": 2},
)
```

### Queueing through the same registry

```python
queued = StoryWorkflowToolService(session).enqueue(
    tool_name="compose_next_segment",
    session_id=session_id,
    arguments={"instructions": "Write the next calm scene."},
)
```

### Routing parsed chat actions into tool calls

```python
plan = StoryWorkflowActionRouter().plan_calls(
    session_id=session_id,
    batch=parsed_chat_actions,
)
```

### Adding a new tool

1. Add request/result models in `backend/app/models/story_tools.py`.
2. Add a `StoryWorkflowToolDefinition` entry in `backend/app/services/story_tools.py`.
3. Implement the executor method in `StoryWorkflowToolService`.
4. Add action-router coverage if chat actions should reach it.
5. Add registry, worker, and prompt-alignment tests.

Because worker registration is generated from the registry, a new tool does not need separate
boilerplate in `default_handlers.py` as long as it has a unique `job_type`.

## Exact Verification Performed

### Automated verification

Ran:

- `python -m ruff check app/models/story_tools.py app/services/story_tools.py app/worker/runtime.py app/worker/default_handlers.py app/ai/intent_parser.py app/models/__init__.py app/services/__init__.py tests/test_story_tools.py`
- `python -m pytest tests/test_story_tools.py tests/test_worker_runtime.py tests/test_intent_parser_adapter.py tests/test_intent_parser_service.py -q`
- `python -m pytest -q`
- `python -m ruff check app tests`

Results:

- `ruff check app tests`: passed
- focused pytest run: `17 passed`
- full backend pytest run: `97 passed, 5 skipped`

### UI / browser / screenshot verification

Not applicable for this prompt.

This was a backend-only registry and worker/orchestration task. I did not modify frontend code,
layout, styling, rendering, or browser behavior, so no browser checks or screenshots were relevant.

### LLM / prompt evaluation suite

Because I changed the intent-parser prompt inputs, I added explicit registry-alignment evaluation
tests in `backend/tests/test_story_tools.py`.

Named criteria and outcomes:

- `test_eval_prompt_exposes_story_tool_catalog_for_chat_translation`: pass
- `test_eval_registry_alignment_keeps_worker_and_prompt_catalogs_in_sync`: pass
- `test_eval_background_tool_modes_cover_long_running_story_operations`: pass

Interpretation:

- the prompt now receives the shared tool catalog
- the prompt-facing catalog and worker job registrations are generated from the same registry
- long-running stages are explicitly marked as background-capable in the registry

## Wrong Turns, Dead Ends, And Gotchas

- I initially read backend file paths as `backend/backend/...` because I prefixed `rg --files`
  output incorrectly. I corrected that before making changes.
- The first attempt to expose the tool catalog to `app.ai.intent_parser` introduced an import cycle
  because `app.ai` imported `app.services`, and `app.services.__init__` already re-exported
  `SessionIntentParserService`. I fixed that by moving the story-tool import to function scope in
  `render_intent_parser_prompt(...)`.
- While building worker-backed tests, I hit a real workflow constraint: the session state machine
  does not allow `audio` to move to `in_progress` unless `composition` is `completed`. To test
  downstream invalidation behavior, I had to seed a deliberately mixed state where the composition
  stage is marked completed while an in-progress composition job row still exists. That mismatch is
  acceptable in the test because the registry service explicitly cancels active jobs and then
  repairs stage state.
- The current repo does not yet have Gemini-backed pitch/character/beat generation services. I did
  not fake creative outputs. For those tools, the executor persists stage-progress intent and
  durable detail text, which is consistent with the current codebase maturity and keeps the
  registry honest about what it can do today.

## Assumptions I Made While Working Unsupervised

- The prompt’s primary requirement was registry architecture, not full AI generation for every
  stage, so I treated unimplemented planning/generation tools as durable stage-operation intents
  instead of inventing placeholder story content.
- A base narration rate of `140` words per minute is a reasonable heuristic for
  `estimate_audio_length`; playback speed scales that value linearly.
- The tool registry should cover backend story operations only. Pure UI actions like navigation,
  selection acceptance, opening finalize views, or downloading assets remain outside the tool layer.
- It was acceptable to expose the tool catalog to the intent parser prompt as descriptive context
  without changing the existing chat-action response schema.

## Remaining Limits

- `generate_pitches`, `refine_pitch`, `generate_character_sheets`, `refine_character_sheet`, and
  `generate_beat_sheet` do not yet create final AI outputs. They currently manage durable stage
  execution state and shared contracts so later prompts can attach real adapters without changing
  the registry shape.
- There is still no public API route for direct tool invocation. The registry is ready for one, but
  this prompt did not require adding that surface.
