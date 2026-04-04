# Prompt 52: Bedtime Safety and Content Guidelines

Implemented on the current branch in commit `61dad11` (`feat(prompt-52): bedtime safety and content guidelines`).

## What I changed and why

This task needed one shared definition of "bedtime-safe" that the planning pipeline can reuse
without copy-pasting slightly different rules into every prompt. I added that shared policy and
threaded it through the live planning prompts so pitch, character, and beat generation all inherit
the same scare ceiling, violence guardrails, emotional-repair rules, and restful-ending
requirements.

Concrete changes:

- Added [`docs/bedtime-guidelines.md`](/Users/kevin/code/storyteller/docs/bedtime-guidelines.md)
  to document the product rules for scare level, violence avoidance, emotional repair,
  reassuring resolution, audio posture, and the audience-age preset plan.
- Added [`backend/app/models/bedtime_guidelines.py`](/Users/kevin/code/storyteller/backend/app/models/bedtime_guidelines.py)
  as the backend-owned registry for:
  - the active preset key `shared_bedtime_default`
  - the prompt-stage enum-like literal set (`pitch`, `character`, `beat`, `composition`, `audio`)
  - planned audience-age preset metadata for future work
  - normalization/validation that currently accepts only active presets
- Added [`backend/app/ai/bedtime_guidelines.py`](/Users/kevin/code/storyteller/backend/app/ai/bedtime_guidelines.py)
  to render a shared prompt fragment with:
  - reusable core bedtime policy lines
  - stage-specific guidance for pitch, character, beat, composition, and audio stages
- Updated the live prompt renderers to inject that shared fragment:
  - [`backend/app/ai/pitch_generation.py`](/Users/kevin/code/storyteller/backend/app/ai/pitch_generation.py)
  - [`backend/app/ai/character_generation.py`](/Users/kevin/code/storyteller/backend/app/ai/character_generation.py)
  - [`backend/app/ai/beat_sheet_generation.py`](/Users/kevin/code/storyteller/backend/app/ai/beat_sheet_generation.py)
- Updated the live prompt templates so the shared policy appears once in a deliberate section
  instead of being rephrased in each template:
  - [`backend/app/ai/prompts/pitch_generation.md`](/Users/kevin/code/storyteller/backend/app/ai/prompts/pitch_generation.md)
  - [`backend/app/ai/prompts/character_generation.md`](/Users/kevin/code/storyteller/backend/app/ai/prompts/character_generation.md)
  - [`backend/app/ai/prompts/beat_sheet_generation.md`](/Users/kevin/code/storyteller/backend/app/ai/prompts/beat_sheet_generation.md)
- Added a future-proof hook to the prompt context models and service entrypoints with
  `bedtime_guideline_preset_key`, defaulting to `shared_bedtime_default`, so later age-aware
  behavior can plug into an existing contract rather than requiring another cross-cutting refactor:
  - [`backend/app/models/pitch_generation.py`](/Users/kevin/code/storyteller/backend/app/models/pitch_generation.py)
  - [`backend/app/models/character_generation.py`](/Users/kevin/code/storyteller/backend/app/models/character_generation.py)
  - [`backend/app/models/beat_sheet_generation.py`](/Users/kevin/code/storyteller/backend/app/models/beat_sheet_generation.py)
  - [`backend/app/services/pitch_generation.py`](/Users/kevin/code/storyteller/backend/app/services/pitch_generation.py)
  - [`backend/app/services/character_generation.py`](/Users/kevin/code/storyteller/backend/app/services/character_generation.py)
  - [`backend/app/services/beat_sheet_generation.py`](/Users/kevin/code/storyteller/backend/app/services/beat_sheet_generation.py)
- Bumped prompt versions to reflect the changed prompt contract:
  - `pitch_generation.v2` -> `pitch_generation.v3`
  - `character_generation.v1` -> `character_generation.v2`
  - `beat_sheet_generation.v1` -> `beat_sheet_generation.v2`
- Added new prompt-level tests/evals and updated existing service assertions for the prompt-version
  bumps:
  - [`backend/tests/test_bedtime_guidelines.py`](/Users/kevin/code/storyteller/backend/tests/test_bedtime_guidelines.py)
  - [`backend/tests/test_pitch_generation_service.py`](/Users/kevin/code/storyteller/backend/tests/test_pitch_generation_service.py)
  - [`backend/tests/test_character_generation_service.py`](/Users/kevin/code/storyteller/backend/tests/test_character_generation_service.py)
  - [`backend/tests/test_beat_sheet_generation_service.py`](/Users/kevin/code/storyteller/backend/tests/test_beat_sheet_generation_service.py)

## Architectural changes across the codebase

The main architectural change is a clean split between policy data and prompt rendering:

- `backend/app/models/bedtime_guidelines.py` is the durable backend-owned policy/registry layer.
  It knows which preset is active and what future presets are planned.
- `backend/app/ai/bedtime_guidelines.py` is the AI-orchestration layer. It turns the policy into a
  prompt fragment tailored to a pipeline stage.
- Prompt contexts and services now carry a preset key but do not duplicate the policy text.
- Prompt templates consume a single substituted fragment, so the bedtime rules remain centralized.

That means future work can:

- add a composition prompt and call the same fragment builder for `stage="composition"`
- add an audio prompt and call the same fragment builder for `stage="audio"`
- activate an age-specific preset later by expanding the allowed preset set in one model module
  instead of editing every prompt separately

## Examples and extension points

### 1. Reuse the shared bedtime fragment in a future prompt

```python
from app.ai.bedtime_guidelines import build_bedtime_guidelines_fragment

fragment = build_bedtime_guidelines_fragment(
    stage="composition",
    preset_key="shared_bedtime_default",
)
```

This returns the shared bedtime policy plus composition-specific instructions. Composition and
audio fragments are available now even though those prompt builders are not yet live in the repo.

### 2. Pass the preset key through a service call

```python
from app.services.pitch_generation import PitchGenerationService

result = PitchGenerationService().generate_pitches(
    candidate_count=3,
    raw_brief="A child follows lanterns through a harbor before bed.",
    bedtime_guideline_preset_key="shared_bedtime_default",
)
```

Right now the validator only allows the active preset. That is intentional: the hook is live, but
the product is not yet exposing age selection.

### 3. Expand the audience-age plan later

The planned presets already exist in the model registry:

- `preschool_gentle_3_to_5`
- `early_reader_calm_6_to_8`
- `older_kids_soft_mystery_9_to_12`

Later work only needs to:

1. decide which planned presets become active
2. define the actual prompt deltas for those active presets
3. thread the selected preset key from session state or brief normalization into the existing
   service APIs

## Verification performed

### Lint

Ran:

```bash
cd backend
ruff check app/ai/__init__.py \
  app/ai/bedtime_guidelines.py \
  app/ai/pitch_generation.py \
  app/ai/character_generation.py \
  app/ai/beat_sheet_generation.py \
  app/models/bedtime_guidelines.py \
  app/models/pitch_generation.py \
  app/models/character_generation.py \
  app/models/beat_sheet_generation.py \
  app/services/pitch_generation.py \
  app/services/character_generation.py \
  app/services/beat_sheet_generation.py \
  tests/test_bedtime_guidelines.py \
  tests/test_pitch_generation_service.py \
  tests/test_character_generation_service.py \
  tests/test_beat_sheet_generation_service.py
```

Result: passed.

### Tests

Ran:

```bash
pytest backend/tests/test_bedtime_guidelines.py \
  backend/tests/test_pitch_generation_service.py \
  backend/tests/test_character_generation_service.py \
  backend/tests/test_beat_sheet_generation_service.py \
  backend/tests/test_session_beat_sheet_service.py \
  backend/tests/test_session_service.py -q
```

Result: `49 passed in 1.87s`.

### Browser checks / screenshots

None run. This task did not change UI rendering, styling, layout, or browser behavior.

### Build / typecheck

No separate build step was relevant to these backend prompt/docs/test changes, so no additional
build command was run.

### Remaining limits

- Composition and audio prompt fragments are implemented and tested directly, but there are no live
  composition/audio prompt builders in this repo yet to inject them into.
- The audience-age presets are planned metadata plus an API hook, not selectable runtime behavior.
  That was intentional for this prompt.

## LLM / prompt evaluation suite

Added [`backend/tests/test_bedtime_guidelines.py`](/Users/kevin/code/storyteller/backend/tests/test_bedtime_guidelines.py)
to act as the prompt-focused evaluation suite for this change.

Criteria and outcomes:

### Shared policy fragment coverage

- `max_scare_level_defined`: pass
- `violence_avoidance_defined`: pass
- `emotional_repair_defined`: pass
- `reassuring_resolution_defined`: pass
- `wonder_and_adventure_preserved`: pass
- `stage_specific_focus_present`: pass

### Audience preset plan coverage

- `one_active_preset_available`: pass
- `default_key_matches_active_preset`: pass
- `planned_presets_exist`: pass
- `planned_presets_document_adjustments`: pass

### Live prompt integration coverage

For `pitch`, `character`, and `beat` prompts:

- `shared_fragment_included`: pass
- `max_scare_level_included`: pass
- `violence_guardrail_included`: pass
- `emotional_repair_included`: pass
- `stage_focus_included`: pass
- `preset_key_serialized_in_context`: pass

### Failure-mode coverage

- `unsupported bedtime guideline preset key raises validation error`: pass

Measured overall result:

- New prompt-eval test file: `4/4` tests passed
- Total targeted verification suite: `49/49` tests passed

## Wrong turns, dead ends, and gotchas

- I initially ran `ruff check` from `backend/` while still using `backend/...` paths, which caused
  a false "No such file or directory" failure. I reran lint with paths relative to the `backend/`
  working directory.
- Once lint was aimed at the right files, `ruff` surfaced a batch of long lines in
  `backend/app/services/beat_sheet_generation.py`. Those were not new behavioral changes, but the
  touched file had to satisfy lint. I reformatted the affected strings instead of suppressing the
  rule.
- I considered putting the preset registry and the prompt fragment renderer into a single module.
  I split them instead so model-layer validation does not depend on the AI-layer prompt assembly
  code.

## Assumptions made while working unsupervised

- I assumed the first shipping version should keep exactly one active bedtime preset and treat the
  age-specific variants as planned-but-disabled. That matched the prompt requirement to stay simple
  now while leaving room for future audience-age defaults.
- I assumed the current repo scope only required wiring the shared policy into the live planning
  prompts (pitch, character, beat), because composition and audio prompt builders do not yet exist
  in the checked-in backend.
- I assumed no browser-based QA was required because the task was limited to docs, prompt
  orchestration, prompt-context models, and backend tests.
