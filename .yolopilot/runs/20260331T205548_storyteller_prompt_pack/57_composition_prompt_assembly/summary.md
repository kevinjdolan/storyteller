# Prompt 57: Composition Prompt Assembly

## What I changed and why

I added a dedicated backend composition prompt assembly path so composition jobs no longer hand-build prompt context out of scattered outline and continuity fragments inside `story_tools`.

The new code assembles one structured package containing:

- stable system instructions
- per-segment dynamic context
- a compact debug context for inspection and logging

This package pulls together the accepted genre, tone, brief, selected pitch, selected character sheet, selected beat sheet, story setup preferences, current outline card, refreshed continuity facts, and the shared composition-stage bedtime guidelines. The package is then persisted into composition job metadata and segment payloads so prompt state is inspectable later when writing quality drifts.

## Architectural changes

### New prompt schema

Added [`backend/app/models/composition_prompt.py`](/Users/kevin/code/storyteller/backend/app/models/composition_prompt.py) with explicit models for:

- `CompositionPromptAssemblyInput`
- `CompositionSystemInstructions`
- `CompositionPromptDynamicContext`
- `CompositionPromptDebugContext`
- `CompositionPromptPackage`
- nested context models for genre/tone, brief, beat sheet, story setup, outline card, and continuity

This makes prompt assembly first-class application code instead of an implicit dict shape.

### New assembly service

Added [`backend/app/services/composition_prompt_assembly.py`](/Users/kevin/code/storyteller/backend/app/services/composition_prompt_assembly.py).

Key behaviors:

- loads the canonical session aggregate from repositories
- validates required planning state
- refreshes the continuity bible for composition/rewrite runs
- resolves the current outline card for the requested segment index
- builds stable system instructions separately from dynamic context
- creates a bounded debug context for logging and storage
- exposes `build_storage_payload()` through the package so callers persist one consistent shape

### Composition tool integration

Updated [`backend/app/services/story_tools.py`](/Users/kevin/code/storyteller/backend/app/services/story_tools.py) so both:

- `compose_next_segment`
- `rewrite_segments`

now use `CompositionPromptAssemblyService` as the single source of prompt context.

The resulting package is stored in:

- `CompositionJob.metadata_json["composition_prompt"]`
- `CompositionSegment.payload["composition_prompt"]`

For backward compatibility and easier inspection, the storage payload also continues to surface top-level outline and continuity fields such as:

- `outline_card_key`
- `outline_card_title`
- `continuity_bible_id`
- `continuity_summary`

### Export surface

Updated:

- [`backend/app/models/__init__.py`](/Users/kevin/code/storyteller/backend/app/models/__init__.py)
- [`backend/app/services/__init__.py`](/Users/kevin/code/storyteller/backend/app/services/__init__.py)

so the new schema and service are available through the existing package entrypoints.

### Tests

Added [`backend/tests/test_composition_prompt_assembly.py`](/Users/kevin/code/storyteller/backend/tests/test_composition_prompt_assembly.py) and expanded [`backend/tests/test_story_tools.py`](/Users/kevin/code/storyteller/backend/tests/test_story_tools.py).

The new tests cover:

- nominal draft prompt assembly
- rewrite prompt assembly and instruction propagation
- storage payload persistence
- missing-outline fallback behavior
- clear failure when required selected planning state is missing
- integration of the shared prompt package into job/segment persistence

## How to use the new abstraction

Direct service usage:

```python
from app.models import CompositionPromptAssemblyInput
from app.services import CompositionPromptAssemblyService

package = CompositionPromptAssemblyService(session).assemble_prompt_package(
    CompositionPromptAssemblyInput(
        session_id=session_id,
        job_kind="draft",
        segment_index=1,
        instructions="Keep the opening especially gentle.",
    )
)

system_instructions = package.system_instructions
dynamic_context = package.dynamic_context
storage_payload = package.build_storage_payload()
```

What future composition code should rely on:

- use `package.system_instructions` for stable writer rules
- use `package.dynamic_context` for segment-specific inputs
- use `package.debug_context` and `package.build_storage_payload()` for debugging and persistence

Current integration example:

- `StoryWorkflowToolService._compose_next_segment()` assembles the package and persists it before seeding the `CompositionJob` and `CompositionSegment`
- `StoryWorkflowToolService._rewrite_segments()` does the same for rewrite passes

## Debugging strategy

The prompt context debugging strategy is:

1. Persist the full structured package in job and segment JSON metadata.
2. Keep stable instructions and dynamic context in separate fields.
3. Store a compact `debug_context` with high-signal identifiers, segment info, revision numbers, and instruction excerpts.
4. Log only bounded identifiers and counts from the service, not the full assembled payload.

This gives enough context to diagnose bad generations without depending on provider logs and without putting secrets into the stored prompt context.

## Verification performed

### Automated tests

Ran targeted prompt-assembly and composition-tool tests:

```bash
cd backend && python -m pytest tests/test_composition_prompt_assembly.py tests/test_story_tools.py -q
```

Result:

- `21 passed in 1.81s`

Ran the full backend suite after integration and again after final formatting:

```bash
cd backend && python -m pytest -q
```

Result:

- `205 passed, 5 skipped in 10.55s`
- `205 passed, 5 skipped in 10.57s`

### Lint and formatting

Ran targeted formatting/lint on touched files:

```bash
cd backend && python -m ruff format app/models/composition_prompt.py app/models/__init__.py app/services/__init__.py app/services/composition_prompt_assembly.py app/services/story_tools.py tests/test_composition_prompt_assembly.py tests/test_story_tools.py
cd backend && python -m ruff format --check app/models/composition_prompt.py app/models/__init__.py app/services/__init__.py app/services/composition_prompt_assembly.py app/services/story_tools.py tests/test_composition_prompt_assembly.py tests/test_story_tools.py
cd backend && python -m ruff check app/models/composition_prompt.py app/models/__init__.py app/services/__init__.py app/services/composition_prompt_assembly.py app/services/story_tools.py tests/test_composition_prompt_assembly.py tests/test_story_tools.py
```

Result:

- touched files formatted cleanly
- targeted Ruff checks passed

I also ran:

```bash
cd backend && python -m ruff format --check app tests
```

Result:

- failed because the repository already has an unrelated formatting baseline across 28 existing files outside this task

### Browser checks and screenshots

None performed. This prompt only changed backend prompt assembly, persistence, and tests. No frontend/UI behavior changed.

## Evaluation suite

Because this task changes LLM-facing prompt wiring, I added prompt-specific eval coverage in [`backend/tests/test_composition_prompt_assembly.py`](/Users/kevin/code/storyteller/backend/tests/test_composition_prompt_assembly.py).

### Eval: required grounding and debug signals

Source test:

- `test_eval_composition_prompt_package_covers_required_grounding_and_debug_signals`

Criteria and outcomes:

- `stable_instructions_present`: Pass
- `composition_stage_guidelines_present`: Pass
- `required_story_inputs_present`: Pass
- `continuity_facts_attached`: Pass
- `debug_context_is_inspectable`: Pass
- `debug_context_avoids_secret_fields`: Pass

### Eval: missing-outline fallback

Source test:

- `test_eval_composition_prompt_package_falls_back_when_outline_is_missing`

Criteria and outcomes:

- `outline_card_can_be_absent_without_crashing`: Pass
- `instruction_becomes_segment_goal_summary`: Pass
- `debug_context_records_missing_outline`: Pass
- `continuity_still_available`: Pass

### Eval: failure mode for invalid planning state

Source test:

- `test_eval_composition_prompt_package_rejects_missing_selected_pitch`

Criteria and outcomes:

- `clear_error_on_missing_selected_pitch`: Pass

### Eval: rewrite propagation into durable composition records

Source tests:

- `test_composition_prompt_assembly_service_storage_payload_is_debuggable_and_safe`
- `test_story_workflow_tool_service_persists_rewrite_prompt_package`

Criteria and outcomes:

- `rewrite_job_kind_persisted`: Pass
- `rewrite_instruction_propagated_to_dynamic_context`: Pass
- `rewrite_instruction_propagated_to_segment_summary`: Pass
- `stored_prompt_payload_avoids_secret_fields`: Pass

## Wrong turns, dead ends, and gotchas

- I first tried to run verification with `/usr/bin/python3`; that interpreter did not have `pytest` or `ruff` installed. I switched to the active conda `python`, which has the project tooling available.
- I considered reusing the private prompt-shaping helpers hidden inside `sessions.py`, but that would have left composition prompt assembly split across modules again. I instead created a dedicated schema/service pair so composition has one canonical assembly path.
- Repo-wide Ruff format checks are not currently clean; unrelated files outside this task would still be reformatted. I kept the touched files clean and relied on the full backend pytest run for broader regression protection.

## Assumptions made while working unsupervised

- I assumed composition should remain tolerant of a missing selected outline. The new assembler therefore leaves `outline_card=None` and falls back to user instructions or higher-level planning text instead of hard-failing the workflow.
- I assumed it is acceptable to persist structured prompt inputs in `metadata_json`/`payload` because they contain durable planning state and user-authored content, not provider secrets.
- I assumed this prompt is about assembly and persistence only, not yet about rendering the final provider prompt string for Gemini. Stable instructions are therefore stored as structured data plus the composition bedtime guideline fragment, ready for the later writing-engine prompt renderer.

## Commit

Created checkpoint commit:

- `71aa06e feat(prompt-57): composition prompt assembly`
