from __future__ import annotations

from enum import Enum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, model_validator

from app.models.chat_actions import CharacterChangeImpact, ChatToUIActionType
from app.models.story_outline import StoryOutlineCard
from app.models.workflow import WorkflowStage, WorkflowStageState

STORY_WORKFLOW_TOOL_SCHEMA_VERSION = 1


class StoryWorkflowToolName(str, Enum):
    GENERATE_PITCHES = "generate_pitches"
    REFINE_PITCH = "refine_pitch"
    GENERATE_CHARACTER_SHEETS = "generate_character_sheets"
    REFINE_CHARACTER_SHEET = "refine_character_sheet"
    GENERATE_BEAT_SHEET = "generate_beat_sheet"
    UPDATE_SETUP_HEURISTICS = "update_setup_heuristics"
    UPDATE_STORY_OUTLINE = "update_story_outline"
    COMPOSE_NEXT_SEGMENT = "compose_next_segment"
    REWRITE_SEGMENTS = "rewrite_segments"
    ESTIMATE_AUDIO_LENGTH = "estimate_audio_length"
    START_AUDIO_GENERATION = "start_audio_generation"


class StoryWorkflowToolExecutionMode(str, Enum):
    DIRECT = "direct"
    BACKGROUND = "background"


class StoryWorkflowToolSideEffectKind(str, Enum):
    UPDATE_WORKFLOW_STAGE = "update_workflow_stage"
    PERSIST_SELECTION = "persist_selection"
    CREATE_REVISION = "create_revision"
    CREATE_JOB = "create_job"
    CREATE_SEGMENT = "create_segment"
    CANCEL_ACTIVE_JOB = "cancel_active_job"
    COMPUTE_ESTIMATE = "compute_estimate"


class AudioLengthEstimateSource(str, Enum):
    COMPOSITION_SEGMENTS = "composition_segments"
    STORY_SETUP_TARGET = "story_setup_target"
    REQUEST_OVERRIDE = "request_override"
    UNKNOWN = "unknown"


class StoryWorkflowToolModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    schema_version: int = Field(default=STORY_WORKFLOW_TOOL_SCHEMA_VERSION, ge=1)


def _require_any_identifier(
    *values: str | int | None,
    error_message: str,
) -> None:
    if all(value is None for value in values):
        raise ValueError(error_message)


def _require_any_field(
    values: dict[str, object | None],
    *,
    error_message: str,
) -> None:
    if all(value is None for value in values.values()):
        raise ValueError(error_message)


class GeneratePitchesToolInput(StoryWorkflowToolModel):
    candidate_count: int = Field(default=3, ge=2, le=6)
    guidance: str | None = Field(default=None, min_length=1)
    preserve_selected_pitch: bool = False


class RefinePitchToolInput(StoryWorkflowToolModel):
    pitch_id: str | None = Field(default=None, min_length=1)
    generation_key: str | None = Field(default=None, min_length=1)
    pitch_index: int | None = Field(default=None, ge=1)
    title: str | None = Field(default=None, min_length=1)
    instructions: str = Field(min_length=1)

    @model_validator(mode="after")
    def validate_identifier(self) -> RefinePitchToolInput:
        _require_any_identifier(
            self.pitch_id,
            self.generation_key,
            self.pitch_index,
            self.title,
            error_message=(
                "refine_pitch requires a pitch_id, generation_key, pitch_index, or title"
            ),
        )
        return self


class GenerateCharacterSheetsToolInput(StoryWorkflowToolModel):
    guidance: str | None = Field(default=None, min_length=1)


class RefineCharacterSheetToolInput(StoryWorkflowToolModel):
    character_sheet_id: str | None = Field(default=None, min_length=1)
    revision_number: int | None = Field(default=None, ge=1)
    title: str | None = Field(default=None, min_length=1)
    instructions: str = Field(min_length=1)
    focus_character_names: list[str] = Field(default_factory=list)
    change_summary: str | None = Field(default=None, min_length=1)
    change_impact: CharacterChangeImpact | None = None


class GenerateBeatSheetToolInput(StoryWorkflowToolModel):
    guidance: str | None = Field(default=None, min_length=1)
    instructions: str | None = Field(default=None, min_length=1)
    focus_beats: list[str] = Field(default_factory=list)
    bedtime_goal: str | None = Field(default=None, min_length=1)


class UpdateSetupHeuristicsToolInput(StoryWorkflowToolModel):
    target_word_count: int | None = Field(default=None, ge=100, le=10000)
    target_runtime_minutes: int | None = Field(default=None, ge=1, le=180)
    chapter_count: int | None = Field(default=None, ge=1, le=24)
    approximate_scene_count: int | None = Field(default=None, ge=1, le=48)
    chapter_style: str | None = Field(default=None, min_length=1)
    guidance_notes: str | None = Field(default=None, min_length=1)
    origin: str = Field(default="story_tool", min_length=1)

    @model_validator(mode="after")
    def validate_payload(self) -> UpdateSetupHeuristicsToolInput:
        editable_fields = {
            "target_word_count",
            "target_runtime_minutes",
            "chapter_count",
            "approximate_scene_count",
            "chapter_style",
            "guidance_notes",
        }
        if not editable_fields.intersection(self.model_fields_set):
            raise ValueError("update_setup_heuristics requires at least one planning preference")
        return self


class ComposeNextSegmentToolInput(StoryWorkflowToolModel):
    instructions: str | None = Field(default=None, min_length=1)
    restart_from_segment_index: int | None = Field(default=None, ge=1)


class RewriteSegmentsToolInput(StoryWorkflowToolModel):
    instructions: str = Field(min_length=1)
    rewrite_from_segment_index: int = Field(ge=1)
    preserve_completed_segments: bool = True


class EstimateAudioLengthToolInput(StoryWorkflowToolModel):
    playback_speed: float = Field(default=1.0, ge=0.5, le=2.0)
    word_count_override: int | None = Field(default=None, ge=1)
    voice_key: str | None = Field(default=None, min_length=1)


class StartAudioGenerationToolInput(StoryWorkflowToolModel):
    voice_key: str | None = Field(default=None, min_length=1)
    playback_speed: float = Field(default=1.0, ge=0.5, le=2.0)
    include_background_music: bool = False
    music_profile: str | None = Field(default=None, min_length=1)
    regenerate_existing_audio: bool = False


class StoryWorkflowToolSideEffect(StoryWorkflowToolModel):
    kind: StoryWorkflowToolSideEffectKind
    summary: str = Field(min_length=1)
    stages: list[WorkflowStage] = Field(default_factory=list)
    writes_to: list[str] = Field(default_factory=list)


class StoryWorkflowToolCall(StoryWorkflowToolModel):
    tool_name: StoryWorkflowToolName
    session_id: str = Field(min_length=1)
    arguments: dict[str, Any] = Field(default_factory=dict)
    source_action_type: ChatToUIActionType | None = None


class StoryWorkflowToolPlan(StoryWorkflowToolModel):
    calls: list[StoryWorkflowToolCall] = Field(default_factory=list)


class StoryWorkflowToolResultBase(StoryWorkflowToolModel):
    tool_name: StoryWorkflowToolName
    stage: WorkflowStage
    summary: str = Field(min_length=1)


class StageOperationToolResult(StoryWorkflowToolResultBase):
    stage_status: WorkflowStageState
    detail: str | None = None


class UpdateSetupHeuristicsToolResult(StoryWorkflowToolResultBase):
    stage_status: WorkflowStageState
    story_setup_id: str
    revision_number: int = Field(ge=1)


class UpdateStoryOutlineToolInput(StoryWorkflowToolModel):
    outline_id: str | None = Field(default=None, min_length=1)
    summary: str | None = Field(default=None, min_length=1)
    cards: list[StoryOutlineCard] = Field(default_factory=list)
    regenerate_card_keys: list[str] = Field(default_factory=list)
    origin: str = Field(default="workspace", min_length=1)

    @model_validator(mode="after")
    def validate_payload(self) -> "UpdateStoryOutlineToolInput":
        if not self.cards:
            raise ValueError("update_story_outline requires at least one card")
        return self


class UpdateStoryOutlineToolResult(StoryWorkflowToolResultBase):
    stage_status: WorkflowStageState
    story_outline_id: str
    revision_number: int = Field(ge=1)


class CompositionToolResult(StoryWorkflowToolResultBase):
    stage_status: WorkflowStageState
    composition_job_id: str
    segment_id: str
    segment_index: int = Field(ge=1)


class EstimateAudioLengthToolResult(StoryWorkflowToolResultBase):
    estimated_duration_seconds: int = Field(ge=0)
    estimated_word_count: int = Field(ge=0)
    playback_speed: float = Field(ge=0.5, le=2.0)
    basis_source: AudioLengthEstimateSource


class StartAudioGenerationToolResult(StoryWorkflowToolResultBase):
    stage_status: WorkflowStageState
    audio_job_id: str
    estimated_duration_seconds: int = Field(ge=0)
