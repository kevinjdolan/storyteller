from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from enum import Enum


class WorkflowStage(str, Enum):
    GENRE = "genre"
    TONE = "tone"
    BRIEF = "brief"
    PITCHES = "pitches"
    CHARACTERS = "characters"
    BEATS = "beats"
    STORY_SETUP = "story_setup"
    COMPOSITION = "composition"
    AUDIO = "audio"
    FINALIZE = "finalize"


class WorkflowStageState(str, Enum):
    DRAFT = "draft"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    NEEDS_REGENERATION = "needs_regeneration"


@dataclass(frozen=True)
class WorkflowStageDefinition:
    id: WorkflowStage
    label: str
    description: str
    invalidates_on_edit: tuple[WorkflowStage, ...]


WORKFLOW_STAGE_DEFINITIONS: tuple[WorkflowStageDefinition, ...] = (
    WorkflowStageDefinition(
        id=WorkflowStage.GENRE,
        label="Genre",
        description="Choose the overall bedtime-story lane before the rest of the plan is shaped.",
        invalidates_on_edit=(
            WorkflowStage.TONE,
            WorkflowStage.BRIEF,
            WorkflowStage.PITCHES,
            WorkflowStage.CHARACTERS,
            WorkflowStage.BEATS,
            WorkflowStage.COMPOSITION,
            WorkflowStage.AUDIO,
            WorkflowStage.FINALIZE,
        ),
    ),
    WorkflowStageDefinition(
        id=WorkflowStage.TONE,
        label="Tone",
        description="Choose the emotional texture and bedtime-safety posture for the session.",
        invalidates_on_edit=(
            WorkflowStage.BRIEF,
            WorkflowStage.PITCHES,
            WorkflowStage.CHARACTERS,
            WorkflowStage.BEATS,
            WorkflowStage.COMPOSITION,
            WorkflowStage.AUDIO,
            WorkflowStage.FINALIZE,
        ),
    ),
    WorkflowStageDefinition(
        id=WorkflowStage.BRIEF,
        label="Story brief",
        description=(
            "Capture the user's free-form idea and any normalized planning summary derived from it."
        ),
        invalidates_on_edit=(
            WorkflowStage.PITCHES,
            WorkflowStage.CHARACTERS,
            WorkflowStage.BEATS,
            WorkflowStage.COMPOSITION,
            WorkflowStage.AUDIO,
            WorkflowStage.FINALIZE,
        ),
    ),
    WorkflowStageDefinition(
        id=WorkflowStage.PITCHES,
        label="Pitches",
        description="Generate, compare, refine, and accept candidate story directions.",
        invalidates_on_edit=(
            WorkflowStage.CHARACTERS,
            WorkflowStage.BEATS,
            WorkflowStage.COMPOSITION,
            WorkflowStage.AUDIO,
            WorkflowStage.FINALIZE,
        ),
    ),
    WorkflowStageDefinition(
        id=WorkflowStage.CHARACTERS,
        label="Characters",
        description=(
            "Define the accepted character sheet that later planning and writing will reference."
        ),
        invalidates_on_edit=(
            WorkflowStage.BEATS,
            WorkflowStage.COMPOSITION,
            WorkflowStage.AUDIO,
            WorkflowStage.FINALIZE,
        ),
    ),
    WorkflowStageDefinition(
        id=WorkflowStage.BEATS,
        label="Beat sheet",
        description="Store the accepted Save-the-Cat beat sheet for the session.",
        invalidates_on_edit=(
            WorkflowStage.STORY_SETUP,
            WorkflowStage.COMPOSITION,
            WorkflowStage.AUDIO,
            WorkflowStage.FINALIZE,
        ),
    ),
    WorkflowStageDefinition(
        id=WorkflowStage.STORY_SETUP,
        label="Story setup",
        description=(
            "Store soft planning targets such as word count, runtime, and chapter structure."
        ),
        invalidates_on_edit=(
            WorkflowStage.COMPOSITION,
            WorkflowStage.AUDIO,
            WorkflowStage.FINALIZE,
        ),
    ),
    WorkflowStageDefinition(
        id=WorkflowStage.COMPOSITION,
        label="Composition",
        description=(
            "Write the story durably in segments, with room for interruption and targeted rewrites."
        ),
        invalidates_on_edit=(
            WorkflowStage.AUDIO,
            WorkflowStage.FINALIZE,
        ),
    ),
    WorkflowStageDefinition(
        id=WorkflowStage.AUDIO,
        label="Audio",
        description="Configure narration settings and generate resumable audio artifacts.",
        invalidates_on_edit=(WorkflowStage.FINALIZE,),
    ),
    WorkflowStageDefinition(
        id=WorkflowStage.FINALIZE,
        label="Finalize",
        description="Read, listen, review final assets, and download exports.",
        invalidates_on_edit=(),
    ),
)

WORKFLOW_STAGE_SEQUENCE: tuple[WorkflowStage, ...] = tuple(
    definition.id for definition in WORKFLOW_STAGE_DEFINITIONS
)

WORKFLOW_STAGE_STATES: tuple[WorkflowStageState, ...] = tuple(WorkflowStageState)

_WORKFLOW_STAGE_METADATA = {definition.id: definition for definition in WORKFLOW_STAGE_DEFINITIONS}


def get_workflow_stage_definition(stage: WorkflowStage) -> WorkflowStageDefinition:
    return _WORKFLOW_STAGE_METADATA[stage]


def get_invalidated_stages_after_edit(stage: WorkflowStage) -> tuple[WorkflowStage, ...]:
    return get_workflow_stage_definition(stage).invalidates_on_edit


def resolve_resume_stage(
    stage_states: Mapping[WorkflowStage, WorkflowStageState],
) -> WorkflowStage:
    for stage in WORKFLOW_STAGE_SEQUENCE:
        if stage_states.get(stage, WorkflowStageState.DRAFT) != WorkflowStageState.COMPLETED:
            return stage

    return WorkflowStage.FINALIZE
