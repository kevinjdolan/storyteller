from __future__ import annotations

from enum import Enum
from typing import Annotated, Any, Literal, TypeAlias

from pydantic import BaseModel, ConfigDict, Field, TypeAdapter, model_validator

from app.models.workflow import WORKFLOW_STAGE_SEQUENCE, WorkflowStage

CHAT_TO_UI_ACTION_SCHEMA_VERSION = 1


class ChatToUIActionType(str, Enum):
    NAVIGATE_TO_STAGE = "navigate_to_stage"
    SELECT_GENRE = "select_genre"
    SELECT_TONE = "select_tone"
    UPDATE_STORY_BRIEF = "update_story_brief"
    REGENERATE_PITCHES = "regenerate_pitches"
    SELECT_PITCH = "select_pitch"
    SELECT_CHARACTER_SHEET = "select_character_sheet"
    REFINE_CHARACTER_SHEET = "refine_character_sheet"
    REGENERATE_CHARACTER_SHEET = "regenerate_character_sheet"
    ACCEPT_BEAT_SHEET = "accept_beat_sheet"
    REFINE_BEAT_SHEET = "refine_beat_sheet"
    REGENERATE_BEAT_SHEET = "regenerate_beat_sheet"
    UPDATE_STORY_SETUP = "update_story_setup"
    START_COMPOSITION = "start_composition"
    PAUSE_JOB = "pause_job"
    RESUME_JOB = "resume_job"
    REDIRECT_COMPOSITION = "redirect_composition"
    UPDATE_AUDIO_SETTINGS = "update_audio_settings"
    START_AUDIO_GENERATION = "start_audio_generation"
    OPEN_FINALIZE_VIEW = "open_finalize_view"
    DOWNLOAD_ASSET = "download_asset"


class ChatToUIActionDefaultPolicy(str, Enum):
    AUTO_APPLY_CANDIDATE = "auto_apply_candidate"
    CONFIRM_FIRST = "confirm_first"


class ChatToUIJobKind(str, Enum):
    COMPOSITION = "composition"
    AUDIO = "audio"


class StoryBriefEditMode(str, Enum):
    REPLACE = "replace"
    APPEND = "append"
    MERGE = "merge"


class CompositionStartMode(str, Enum):
    FRESH = "fresh"
    CONTINUE = "continue"
    REWRITE = "rewrite"


class FinalizeView(str, Enum):
    READER = "reader"
    PLAYER = "player"


class DownloadAssetKind(str, Enum):
    STORY_DOCX = "story_docx"
    FINAL_AUDIO = "final_audio"


DEFAULT_CHAT_TO_UI_ACTION_POLICIES: dict[ChatToUIActionType, ChatToUIActionDefaultPolicy] = {
    ChatToUIActionType.NAVIGATE_TO_STAGE: ChatToUIActionDefaultPolicy.AUTO_APPLY_CANDIDATE,
    ChatToUIActionType.SELECT_GENRE: ChatToUIActionDefaultPolicy.CONFIRM_FIRST,
    ChatToUIActionType.SELECT_TONE: ChatToUIActionDefaultPolicy.CONFIRM_FIRST,
    ChatToUIActionType.UPDATE_STORY_BRIEF: ChatToUIActionDefaultPolicy.AUTO_APPLY_CANDIDATE,
    ChatToUIActionType.REGENERATE_PITCHES: ChatToUIActionDefaultPolicy.CONFIRM_FIRST,
    ChatToUIActionType.SELECT_PITCH: ChatToUIActionDefaultPolicy.CONFIRM_FIRST,
    ChatToUIActionType.SELECT_CHARACTER_SHEET: ChatToUIActionDefaultPolicy.CONFIRM_FIRST,
    ChatToUIActionType.REFINE_CHARACTER_SHEET: ChatToUIActionDefaultPolicy.CONFIRM_FIRST,
    ChatToUIActionType.REGENERATE_CHARACTER_SHEET: ChatToUIActionDefaultPolicy.CONFIRM_FIRST,
    ChatToUIActionType.ACCEPT_BEAT_SHEET: ChatToUIActionDefaultPolicy.CONFIRM_FIRST,
    ChatToUIActionType.REFINE_BEAT_SHEET: ChatToUIActionDefaultPolicy.CONFIRM_FIRST,
    ChatToUIActionType.REGENERATE_BEAT_SHEET: ChatToUIActionDefaultPolicy.CONFIRM_FIRST,
    ChatToUIActionType.UPDATE_STORY_SETUP: ChatToUIActionDefaultPolicy.AUTO_APPLY_CANDIDATE,
    ChatToUIActionType.START_COMPOSITION: ChatToUIActionDefaultPolicy.CONFIRM_FIRST,
    ChatToUIActionType.PAUSE_JOB: ChatToUIActionDefaultPolicy.CONFIRM_FIRST,
    ChatToUIActionType.RESUME_JOB: ChatToUIActionDefaultPolicy.CONFIRM_FIRST,
    ChatToUIActionType.REDIRECT_COMPOSITION: ChatToUIActionDefaultPolicy.CONFIRM_FIRST,
    ChatToUIActionType.UPDATE_AUDIO_SETTINGS: ChatToUIActionDefaultPolicy.AUTO_APPLY_CANDIDATE,
    ChatToUIActionType.START_AUDIO_GENERATION: ChatToUIActionDefaultPolicy.CONFIRM_FIRST,
    ChatToUIActionType.OPEN_FINALIZE_VIEW: ChatToUIActionDefaultPolicy.AUTO_APPLY_CANDIDATE,
    ChatToUIActionType.DOWNLOAD_ASSET: ChatToUIActionDefaultPolicy.AUTO_APPLY_CANDIDATE,
}


def get_chat_to_ui_action_default_policy(
    action_type: ChatToUIActionType,
) -> ChatToUIActionDefaultPolicy:
    return DEFAULT_CHAT_TO_UI_ACTION_POLICIES[action_type]


class ChatToUIModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    schema_version: int = Field(default=CHAT_TO_UI_ACTION_SCHEMA_VERSION, ge=1)


class ChatToUIExtractedValues(BaseModel):
    model_config = ConfigDict(extra="forbid")


def _require_any_identifier(
    *values: str | int | None,
    error_message: str,
) -> None:
    if all(value is None for value in values):
        raise ValueError(error_message)


def _require_any_field(
    values: dict[str, object | None],
    error_message: str,
) -> None:
    if all(value is None for value in values.values()):
        raise ValueError(error_message)


class SelectGenreValues(ChatToUIExtractedValues):
    genre_id: str | None = Field(default=None, min_length=1)
    genre_slug: str | None = Field(default=None, min_length=1)
    genre_label: str | None = Field(default=None, min_length=1)

    @model_validator(mode="after")
    def validate_identifier(self) -> SelectGenreValues:
        _require_any_identifier(
            self.genre_id,
            self.genre_slug,
            self.genre_label,
            error_message="select_genre requires a genre_id, genre_slug, or genre_label",
        )
        return self


class SelectToneValues(ChatToUIExtractedValues):
    tone_profile_id: str | None = Field(default=None, min_length=1)
    tone_profile_slug: str | None = Field(default=None, min_length=1)
    tone_profile_label: str | None = Field(default=None, min_length=1)

    @model_validator(mode="after")
    def validate_identifier(self) -> SelectToneValues:
        _require_any_identifier(
            self.tone_profile_id,
            self.tone_profile_slug,
            self.tone_profile_label,
            error_message=(
                "select_tone requires a tone_profile_id, tone_profile_slug, or tone_profile_label"
            ),
        )
        return self


class UpdateStoryBriefValues(ChatToUIExtractedValues):
    raw_brief: str | None = Field(default=None, min_length=1)
    normalized_summary: str | None = Field(default=None, min_length=1)
    planning_notes: str | None = Field(default=None, min_length=1)
    edit_mode: StoryBriefEditMode = StoryBriefEditMode.MERGE

    @model_validator(mode="after")
    def validate_story_brief(self) -> UpdateStoryBriefValues:
        _require_any_field(
            {
                "raw_brief": self.raw_brief,
                "normalized_summary": self.normalized_summary,
                "planning_notes": self.planning_notes,
            },
            error_message=(
                "update_story_brief requires raw_brief, normalized_summary, or planning_notes"
            ),
        )
        return self


class RegeneratePitchesValues(ChatToUIExtractedValues):
    candidate_count: int | None = Field(default=None, ge=2, le=6)
    guidance: str | None = Field(default=None, min_length=1)
    preserve_selected_pitch: bool = False


class SelectPitchValues(ChatToUIExtractedValues):
    pitch_id: str | None = Field(default=None, min_length=1)
    generation_key: str | None = Field(default=None, min_length=1)
    pitch_index: int | None = Field(default=None, ge=1)
    title: str | None = Field(default=None, min_length=1)

    @model_validator(mode="after")
    def validate_identifier(self) -> SelectPitchValues:
        _require_any_identifier(
            self.pitch_id,
            self.generation_key,
            self.pitch_index,
            self.title,
            error_message=(
                "select_pitch requires a pitch_id, generation_key, pitch_index, or title"
            ),
        )
        return self


class SelectCharacterSheetValues(ChatToUIExtractedValues):
    character_sheet_id: str | None = Field(default=None, min_length=1)
    revision_number: int | None = Field(default=None, ge=1)
    title: str | None = Field(default=None, min_length=1)

    @model_validator(mode="after")
    def validate_identifier(self) -> SelectCharacterSheetValues:
        _require_any_identifier(
            self.character_sheet_id,
            self.revision_number,
            self.title,
            error_message=(
                "select_character_sheet requires a character_sheet_id, revision_number, or title"
            ),
        )
        return self


class RefineCharacterSheetValues(ChatToUIExtractedValues):
    instructions: str = Field(min_length=1)
    focus_character_names: list[str] = Field(default_factory=list)
    change_summary: str | None = Field(default=None, min_length=1)


class RegenerateCharacterSheetValues(ChatToUIExtractedValues):
    guidance: str | None = Field(default=None, min_length=1)


class AcceptBeatSheetValues(ChatToUIExtractedValues):
    beat_sheet_id: str | None = Field(default=None, min_length=1)
    revision_number: int | None = Field(default=None, ge=1)

    @model_validator(mode="after")
    def validate_identifier(self) -> AcceptBeatSheetValues:
        _require_any_identifier(
            self.beat_sheet_id,
            self.revision_number,
            error_message="accept_beat_sheet requires a beat_sheet_id or revision_number",
        )
        return self


class RefineBeatSheetValues(ChatToUIExtractedValues):
    instructions: str = Field(min_length=1)
    beat_names: list[str] = Field(default_factory=list)
    bedtime_goal: str | None = Field(default=None, min_length=1)


class RegenerateBeatSheetValues(ChatToUIExtractedValues):
    guidance: str | None = Field(default=None, min_length=1)
    focus_beats: list[str] = Field(default_factory=list)


class UpdateStorySetupValues(ChatToUIExtractedValues):
    target_word_count: int | None = Field(default=None, ge=100, le=10000)
    target_runtime_minutes: int | None = Field(default=None, ge=1, le=180)
    chapter_count: int | None = Field(default=None, ge=1, le=24)
    chapter_style: str | None = Field(default=None, min_length=1)
    guidance_notes: str | None = Field(default=None, min_length=1)

    @model_validator(mode="after")
    def validate_story_setup(self) -> UpdateStorySetupValues:
        _require_any_field(
            {
                "target_word_count": self.target_word_count,
                "target_runtime_minutes": self.target_runtime_minutes,
                "chapter_count": self.chapter_count,
                "chapter_style": self.chapter_style,
                "guidance_notes": self.guidance_notes,
            },
            error_message=(
                "update_story_setup requires at least one structured planning preference"
            ),
        )
        return self


class StartCompositionValues(ChatToUIExtractedValues):
    mode: CompositionStartMode = CompositionStartMode.FRESH
    instructions: str | None = Field(default=None, min_length=1)
    restart_from_segment_index: int | None = Field(default=None, ge=1)


class JobControlValues(ChatToUIExtractedValues):
    job_kind: ChatToUIJobKind
    job_id: str | None = Field(default=None, min_length=1)
    reason: str | None = Field(default=None, min_length=1)


class RedirectCompositionValues(ChatToUIExtractedValues):
    instructions: str = Field(min_length=1)
    rewrite_from_segment_index: int | None = Field(default=None, ge=1)
    preserve_completed_segments: bool = True


class UpdateAudioSettingsValues(ChatToUIExtractedValues):
    voice_key: str | None = Field(default=None, min_length=1)
    playback_speed: float | None = Field(default=None, ge=0.5, le=2.0)
    include_background_music: bool | None = None
    music_profile: str | None = Field(default=None, min_length=1)
    guidance_notes: str | None = Field(default=None, min_length=1)

    @model_validator(mode="after")
    def validate_audio_settings(self) -> UpdateAudioSettingsValues:
        _require_any_field(
            {
                "voice_key": self.voice_key,
                "playback_speed": self.playback_speed,
                "include_background_music": self.include_background_music,
                "music_profile": self.music_profile,
                "guidance_notes": self.guidance_notes,
            },
            error_message=(
                "update_audio_settings requires at least one audio setting or guidance note"
            ),
        )
        return self


class StartAudioGenerationValues(ChatToUIExtractedValues):
    voice_key: str | None = Field(default=None, min_length=1)
    playback_speed: float | None = Field(default=None, ge=0.5, le=2.0)
    include_background_music: bool | None = None
    music_profile: str | None = Field(default=None, min_length=1)
    regenerate_existing_audio: bool = False


class OpenFinalizeViewValues(ChatToUIExtractedValues):
    view: FinalizeView


class DownloadAssetValues(ChatToUIExtractedValues):
    asset_kind: DownloadAssetKind


class ChatToUIActionBase(ChatToUIModel):
    action_type: ChatToUIActionType
    target_stage: WorkflowStage
    confidence: float = Field(ge=0, le=1)
    rationale: str | None = Field(default=None, min_length=1)
    requires_confirmation: bool

    @model_validator(mode="after")
    def validate_confirmation_requirement(self) -> ChatToUIActionBase:
        if (
            get_chat_to_ui_action_default_policy(self.action_type)
            == ChatToUIActionDefaultPolicy.CONFIRM_FIRST
            and not self.requires_confirmation
        ):
            raise ValueError(
                f"{self.action_type.value} must require confirmation under the default policy"
            )

        return self


class NavigateToStageAction(ChatToUIActionBase):
    action_type: Literal[ChatToUIActionType.NAVIGATE_TO_STAGE] = (
        ChatToUIActionType.NAVIGATE_TO_STAGE
    )
    target_stage: WorkflowStage
    extracted_values: ChatToUIExtractedValues = Field(default_factory=ChatToUIExtractedValues)


class SelectGenreAction(ChatToUIActionBase):
    action_type: Literal[ChatToUIActionType.SELECT_GENRE] = ChatToUIActionType.SELECT_GENRE
    target_stage: Literal[WorkflowStage.GENRE] = WorkflowStage.GENRE
    extracted_values: SelectGenreValues


class SelectToneAction(ChatToUIActionBase):
    action_type: Literal[ChatToUIActionType.SELECT_TONE] = ChatToUIActionType.SELECT_TONE
    target_stage: Literal[WorkflowStage.TONE] = WorkflowStage.TONE
    extracted_values: SelectToneValues


class UpdateStoryBriefAction(ChatToUIActionBase):
    action_type: Literal[ChatToUIActionType.UPDATE_STORY_BRIEF] = (
        ChatToUIActionType.UPDATE_STORY_BRIEF
    )
    target_stage: Literal[WorkflowStage.BRIEF] = WorkflowStage.BRIEF
    extracted_values: UpdateStoryBriefValues


class RegeneratePitchesAction(ChatToUIActionBase):
    action_type: Literal[ChatToUIActionType.REGENERATE_PITCHES] = (
        ChatToUIActionType.REGENERATE_PITCHES
    )
    target_stage: Literal[WorkflowStage.PITCHES] = WorkflowStage.PITCHES
    extracted_values: RegeneratePitchesValues = Field(default_factory=RegeneratePitchesValues)


class SelectPitchAction(ChatToUIActionBase):
    action_type: Literal[ChatToUIActionType.SELECT_PITCH] = ChatToUIActionType.SELECT_PITCH
    target_stage: Literal[WorkflowStage.PITCHES] = WorkflowStage.PITCHES
    extracted_values: SelectPitchValues


class SelectCharacterSheetAction(ChatToUIActionBase):
    action_type: Literal[ChatToUIActionType.SELECT_CHARACTER_SHEET] = (
        ChatToUIActionType.SELECT_CHARACTER_SHEET
    )
    target_stage: Literal[WorkflowStage.CHARACTERS] = WorkflowStage.CHARACTERS
    extracted_values: SelectCharacterSheetValues


class RefineCharacterSheetAction(ChatToUIActionBase):
    action_type: Literal[ChatToUIActionType.REFINE_CHARACTER_SHEET] = (
        ChatToUIActionType.REFINE_CHARACTER_SHEET
    )
    target_stage: Literal[WorkflowStage.CHARACTERS] = WorkflowStage.CHARACTERS
    extracted_values: RefineCharacterSheetValues


class RegenerateCharacterSheetAction(ChatToUIActionBase):
    action_type: Literal[ChatToUIActionType.REGENERATE_CHARACTER_SHEET] = (
        ChatToUIActionType.REGENERATE_CHARACTER_SHEET
    )
    target_stage: Literal[WorkflowStage.CHARACTERS] = WorkflowStage.CHARACTERS
    extracted_values: RegenerateCharacterSheetValues = Field(
        default_factory=RegenerateCharacterSheetValues
    )


class AcceptBeatSheetAction(ChatToUIActionBase):
    action_type: Literal[ChatToUIActionType.ACCEPT_BEAT_SHEET] = (
        ChatToUIActionType.ACCEPT_BEAT_SHEET
    )
    target_stage: Literal[WorkflowStage.BEATS] = WorkflowStage.BEATS
    extracted_values: AcceptBeatSheetValues


class RefineBeatSheetAction(ChatToUIActionBase):
    action_type: Literal[ChatToUIActionType.REFINE_BEAT_SHEET] = (
        ChatToUIActionType.REFINE_BEAT_SHEET
    )
    target_stage: Literal[WorkflowStage.BEATS] = WorkflowStage.BEATS
    extracted_values: RefineBeatSheetValues


class RegenerateBeatSheetAction(ChatToUIActionBase):
    action_type: Literal[ChatToUIActionType.REGENERATE_BEAT_SHEET] = (
        ChatToUIActionType.REGENERATE_BEAT_SHEET
    )
    target_stage: Literal[WorkflowStage.BEATS] = WorkflowStage.BEATS
    extracted_values: RegenerateBeatSheetValues = Field(default_factory=RegenerateBeatSheetValues)


class UpdateStorySetupAction(ChatToUIActionBase):
    action_type: Literal[ChatToUIActionType.UPDATE_STORY_SETUP] = (
        ChatToUIActionType.UPDATE_STORY_SETUP
    )
    target_stage: Literal[WorkflowStage.STORY_SETUP] = WorkflowStage.STORY_SETUP
    extracted_values: UpdateStorySetupValues


class StartCompositionAction(ChatToUIActionBase):
    action_type: Literal[ChatToUIActionType.START_COMPOSITION] = (
        ChatToUIActionType.START_COMPOSITION
    )
    target_stage: Literal[WorkflowStage.COMPOSITION] = WorkflowStage.COMPOSITION
    extracted_values: StartCompositionValues = Field(default_factory=StartCompositionValues)


class PauseJobAction(ChatToUIActionBase):
    action_type: Literal[ChatToUIActionType.PAUSE_JOB] = ChatToUIActionType.PAUSE_JOB
    target_stage: Literal[WorkflowStage.COMPOSITION, WorkflowStage.AUDIO]
    extracted_values: JobControlValues

    @model_validator(mode="after")
    def validate_stage_matches_job_kind(self) -> PauseJobAction:
        expected_stage = (
            WorkflowStage.COMPOSITION
            if self.extracted_values.job_kind == ChatToUIJobKind.COMPOSITION
            else WorkflowStage.AUDIO
        )
        if self.target_stage != expected_stage:
            raise ValueError("pause_job target_stage must match the extracted job_kind")

        return self


class ResumeJobAction(ChatToUIActionBase):
    action_type: Literal[ChatToUIActionType.RESUME_JOB] = ChatToUIActionType.RESUME_JOB
    target_stage: Literal[WorkflowStage.COMPOSITION, WorkflowStage.AUDIO]
    extracted_values: JobControlValues

    @model_validator(mode="after")
    def validate_stage_matches_job_kind(self) -> ResumeJobAction:
        expected_stage = (
            WorkflowStage.COMPOSITION
            if self.extracted_values.job_kind == ChatToUIJobKind.COMPOSITION
            else WorkflowStage.AUDIO
        )
        if self.target_stage != expected_stage:
            raise ValueError("resume_job target_stage must match the extracted job_kind")

        return self


class RedirectCompositionAction(ChatToUIActionBase):
    action_type: Literal[ChatToUIActionType.REDIRECT_COMPOSITION] = (
        ChatToUIActionType.REDIRECT_COMPOSITION
    )
    target_stage: Literal[WorkflowStage.COMPOSITION] = WorkflowStage.COMPOSITION
    extracted_values: RedirectCompositionValues


class UpdateAudioSettingsAction(ChatToUIActionBase):
    action_type: Literal[ChatToUIActionType.UPDATE_AUDIO_SETTINGS] = (
        ChatToUIActionType.UPDATE_AUDIO_SETTINGS
    )
    target_stage: Literal[WorkflowStage.AUDIO] = WorkflowStage.AUDIO
    extracted_values: UpdateAudioSettingsValues


class StartAudioGenerationAction(ChatToUIActionBase):
    action_type: Literal[ChatToUIActionType.START_AUDIO_GENERATION] = (
        ChatToUIActionType.START_AUDIO_GENERATION
    )
    target_stage: Literal[WorkflowStage.AUDIO] = WorkflowStage.AUDIO
    extracted_values: StartAudioGenerationValues = Field(default_factory=StartAudioGenerationValues)


class OpenFinalizeViewAction(ChatToUIActionBase):
    action_type: Literal[ChatToUIActionType.OPEN_FINALIZE_VIEW] = (
        ChatToUIActionType.OPEN_FINALIZE_VIEW
    )
    target_stage: Literal[WorkflowStage.FINALIZE] = WorkflowStage.FINALIZE
    extracted_values: OpenFinalizeViewValues


class DownloadAssetAction(ChatToUIActionBase):
    action_type: Literal[ChatToUIActionType.DOWNLOAD_ASSET] = ChatToUIActionType.DOWNLOAD_ASSET
    target_stage: Literal[WorkflowStage.FINALIZE] = WorkflowStage.FINALIZE
    extracted_values: DownloadAssetValues


ChatToUIAction: TypeAlias = Annotated[
    NavigateToStageAction
    | SelectGenreAction
    | SelectToneAction
    | UpdateStoryBriefAction
    | RegeneratePitchesAction
    | SelectPitchAction
    | SelectCharacterSheetAction
    | RefineCharacterSheetAction
    | RegenerateCharacterSheetAction
    | AcceptBeatSheetAction
    | RefineBeatSheetAction
    | RegenerateBeatSheetAction
    | UpdateStorySetupAction
    | StartCompositionAction
    | PauseJobAction
    | ResumeJobAction
    | RedirectCompositionAction
    | UpdateAudioSettingsAction
    | StartAudioGenerationAction
    | OpenFinalizeViewAction
    | DownloadAssetAction,
    Field(discriminator="action_type"),
]


class ChatToUIActionBatch(ChatToUIModel):
    actions: list[ChatToUIAction] = Field(default_factory=list)


def get_chat_to_ui_action_schema_bundle() -> dict[str, Any]:
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "bundle_schema_version": CHAT_TO_UI_ACTION_SCHEMA_VERSION,
        "workflow_stages": [stage.value for stage in WORKFLOW_STAGE_SEQUENCE],
        "default_policy_by_action": {
            action_type.value: policy.value
            for action_type, policy in DEFAULT_CHAT_TO_UI_ACTION_POLICIES.items()
        },
        "schemas": {
            "chat_to_ui_action": TypeAdapter(ChatToUIAction).json_schema(),
            "chat_to_ui_action_batch": ChatToUIActionBatch.model_json_schema(),
        },
    }
