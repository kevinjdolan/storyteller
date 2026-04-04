# Bedtime Safety and Content Guidelines

Storyteller needs one shared definition of "bedtime-safe" so planning, writing, and narration do
not drift into harsher territory as the workflow advances. This file documents the current product
rules and the backend abstractions that carry them into prompts.

## Core Promise

Bedtime-safe does not mean flat or boring. The product should still support:

- wonder
- gentle adventure
- mild mystery
- emotional growth
- meaningful low points that resolve into safety

The constraint is emotional intensity, not imagination. A good bedtime story can move, surprise,
and transform, but it should still guide the listener toward rest.

## Current Safety Rules

### Maximum scare level

- The ceiling is brief shivers, uncertainty, wistful mistakes, or soft suspense.
- Tension can rise, but it should remain readable and buffered by visible safety cues.
- Do not cross into horror, menace, panic spirals, helpless entrapment, predatory pursuit, or
  grotesque imagery.

### Violence avoidance

- Do not depict assault, graphic injury, on-page death, revenge, punishment-driven conflict, or
  weapon-centered action.
- Avoid villains or threats whose primary function is to terrify the child listener.
- Prefer problems that can be solved through care, patience, teamwork, cleverness, repair, or
  emotional honesty.

### Emotional repair after tension

- After each tense or sad turn, quickly re-establish grounding through companionship, named
  feelings, familiar rituals, or other signs that the problem is manageable.
- Characters may worry, doubt themselves, or feel briefly lost, but they should not remain
  emotionally stranded for long.
- Save-the-Cat low points should feel tender or reflective, not traumatic.

### Reassuring resolution

- Endings must visibly restore safety, connection, and calm.
- The last movement of the story should downshift into rest rather than reopening suspense.
- Final images should feel tucked-in, settled, and sleep-compatible.

### Audio-specific posture

- Narration should sound warm, patient, and emotionally regulated.
- Music should support the voice rather than dominate it.
- Avoid performance choices that feel like jump scares, villain turns, or sudden intensity spikes.

## How The Backend Reuses These Rules

The reusable backend source of truth lives in:

- [`backend/app/models/bedtime_guidelines.py`](/Users/kevin/code/storyteller/backend/app/models/bedtime_guidelines.py)
- [`backend/app/ai/bedtime_guidelines.py`](/Users/kevin/code/storyteller/backend/app/ai/bedtime_guidelines.py)

The split is deliberate:

- `backend/app/models/bedtime_guidelines.py` stores the preset key, active-vs-planned audience
  preset plan, and validation helpers.
- `backend/app/ai/bedtime_guidelines.py` renders stage-specific prompt fragments for `pitch`,
  `character`, `beat`, `composition`, and `audio`.

The live prompt builders currently inject the shared fragment into:

- [`backend/app/ai/pitch_generation.py`](/Users/kevin/code/storyteller/backend/app/ai/pitch_generation.py)
- [`backend/app/ai/character_generation.py`](/Users/kevin/code/storyteller/backend/app/ai/character_generation.py)
- [`backend/app/ai/beat_sheet_generation.py`](/Users/kevin/code/storyteller/backend/app/ai/beat_sheet_generation.py)

That keeps the bedtime rules centralized instead of rewording them independently in each template.

## Audience-Age Preset Plan

The first implementation stays simple: the product uses one active preset,
`shared_bedtime_default`, for a broad bedtime read-aloud audience. The backend also stores a plan
for future expansion so later prompts can add age-aware defaults without another structural
rewrite.

Planned follow-on presets:

- `preschool_gentle_3_to_5`
  Bias toward extremely fast reassurance, simpler emotional naming, and near-constant visible
  support.
- `early_reader_calm_6_to_8`
  Allow slightly longer mystery/problem-solving loops while keeping setbacks tender and solvable
  through teamwork.
- `older_kids_soft_mystery_9_to_12`
  Allow more layered ambiguity and reflection while still rejecting horror imagery and hopeless
  endings.

The pipeline hook is already in place through `bedtime_guideline_preset_key` on the prompt context
models. The current validator only accepts the active preset, which keeps production behavior
deterministic until the product explicitly decides to expose age selection.

## Practical Usage

When a new stage prompt is added, reuse the same abstraction instead of copying policy text:

```python
from app.ai.bedtime_guidelines import build_bedtime_guidelines_fragment

fragment = build_bedtime_guidelines_fragment(
    stage="composition",
    preset_key="shared_bedtime_default",
)
```

That call returns the shared bedtime policy plus stage-specific instructions for the requested
pipeline step. Composition and audio fragments already exist even though those prompt templates are
not live in the repository yet.
