from app.models import (
    WORKFLOW_STAGE_DEFINITIONS,
    WORKFLOW_STAGE_SEQUENCE,
    WORKFLOW_STAGE_STATES,
    WorkflowStage,
    WorkflowStageState,
    get_invalidated_stages_after_edit,
    resolve_resume_stage,
)


def test_workflow_stage_sequence_matches_the_product_contract() -> None:
    assert WORKFLOW_STAGE_SEQUENCE == (
        WorkflowStage.GENRE,
        WorkflowStage.TONE,
        WorkflowStage.BRIEF,
        WorkflowStage.PITCHES,
        WorkflowStage.CHARACTERS,
        WorkflowStage.BEATS,
        WorkflowStage.STORY_SETUP,
        WorkflowStage.COMPOSITION,
        WorkflowStage.AUDIO,
        WorkflowStage.FINALIZE,
    )
    assert tuple(definition.id for definition in WORKFLOW_STAGE_DEFINITIONS) == (
        WORKFLOW_STAGE_SEQUENCE
    )
    assert WORKFLOW_STAGE_STATES == (
        WorkflowStageState.DRAFT,
        WorkflowStageState.IN_PROGRESS,
        WorkflowStageState.COMPLETED,
        WorkflowStageState.NEEDS_REGENERATION,
    )


def test_editing_upstream_stages_invalidates_only_the_required_dependents() -> None:
    assert get_invalidated_stages_after_edit(WorkflowStage.GENRE) == (
        WorkflowStage.TONE,
        WorkflowStage.BRIEF,
        WorkflowStage.PITCHES,
        WorkflowStage.CHARACTERS,
        WorkflowStage.BEATS,
        WorkflowStage.COMPOSITION,
        WorkflowStage.AUDIO,
        WorkflowStage.FINALIZE,
    )
    assert get_invalidated_stages_after_edit(WorkflowStage.BEATS) == (
        WorkflowStage.COMPOSITION,
        WorkflowStage.AUDIO,
        WorkflowStage.FINALIZE,
    )
    assert get_invalidated_stages_after_edit(WorkflowStage.COMPOSITION) == (
        WorkflowStage.AUDIO,
        WorkflowStage.FINALIZE,
    )
    assert get_invalidated_stages_after_edit(WorkflowStage.FINALIZE) == ()


def test_resume_stage_uses_the_earliest_non_completed_stage() -> None:
    stage_states = {
        WorkflowStage.GENRE: WorkflowStageState.COMPLETED,
        WorkflowStage.TONE: WorkflowStageState.COMPLETED,
        WorkflowStage.BRIEF: WorkflowStageState.COMPLETED,
        WorkflowStage.PITCHES: WorkflowStageState.IN_PROGRESS,
        WorkflowStage.CHARACTERS: WorkflowStageState.DRAFT,
    }

    assert resolve_resume_stage(stage_states) == WorkflowStage.PITCHES


def test_resume_stage_prioritizes_regeneration_before_later_completed_stages() -> None:
    stage_states = {
        WorkflowStage.GENRE: WorkflowStageState.COMPLETED,
        WorkflowStage.TONE: WorkflowStageState.COMPLETED,
        WorkflowStage.BRIEF: WorkflowStageState.NEEDS_REGENERATION,
        WorkflowStage.PITCHES: WorkflowStageState.COMPLETED,
        WorkflowStage.CHARACTERS: WorkflowStageState.COMPLETED,
        WorkflowStage.BEATS: WorkflowStageState.COMPLETED,
        WorkflowStage.STORY_SETUP: WorkflowStageState.COMPLETED,
        WorkflowStage.COMPOSITION: WorkflowStageState.COMPLETED,
    }

    assert resolve_resume_stage(stage_states) == WorkflowStage.BRIEF


def test_resume_stage_returns_finalize_when_every_stage_is_complete() -> None:
    stage_states = {stage: WorkflowStageState.COMPLETED for stage in WORKFLOW_STAGE_SEQUENCE}

    assert resolve_resume_stage(stage_states) == WorkflowStage.FINALIZE
