from __future__ import annotations

from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, Field, model_validator

from app.models.brief_normalization import NormalizedBriefPreferences
from app.models.chat_actions import CharacterChangeImpact, StoryBriefEditMode
from app.models.events import SessionEventView, SessionHistoryView
from app.models.workflow import WorkflowStage, WorkflowStageState


class SessionCatalogSelection(BaseModel):
    id: str
    slug: str
    label: str


class SessionProgress(BaseModel):
    total_stages: int
    completed_stages: int
    in_progress_stages: int
    needs_regeneration_stages: int


class SessionStageStateView(BaseModel):
    stage: WorkflowStage
    label: str
    description: str
    status: WorkflowStageState
    detail: str | None = None
    started_at: datetime | None = None
    completed_at: datetime | None = None
    last_event_summary: str | None = None
    last_event_type: str | None = None
    last_event_at: datetime | None = None


class StoryBriefView(BaseModel):
    id: str
    revision_number: int
    story_idea: str | None = None
    desired_themes: str | None = None
    key_images: str | None = None
    audience_notes: str | None = None
    must_have_elements: str | None = None
    raw_brief: str
    normalized_summary: str | None = None
    normalized_preferences: NormalizedBriefPreferences | None = None
    planning_notes: str | None = None
    accepted_at: datetime | None = None
    updated_at: datetime


class PitchView(BaseModel):
    id: str
    generation_key: str
    pitch_index: int
    title: str
    hook: str
    central_conflict: str | None = None
    why_it_fits: str | None = None
    logline: str
    summary: str | None = None
    bedtime_notes: str | None = None
    generation_kind: str = "generated"
    source_pitch_id: str | None = None
    source_pitch_title: str | None = None
    refinement_instructions: str | None = None
    selection_rationale: str | None = None
    is_selected: bool = False
    accepted_at: datetime | None = None
    created_at: datetime
    updated_at: datetime


class PitchBatchView(BaseModel):
    generation_key: str
    candidate_count: int
    created_at: datetime
    generation_kind: str = "generated"
    guidance: str | None = None
    source_pitch_id: str | None = None
    source_pitch_title: str | None = None
    source_generation_key: str | None = None
    refinement_instructions: str | None = None
    pitches: list[PitchView] = Field(default_factory=list)


class CharacterProfileView(BaseModel):
    name: str
    role: str | None = None
    goal: str | None = None
    flaw: str | None = None
    comfort_trait: str | None = None
    bedtime_safety_notes: str | None = None
    relationships: list[str] = Field(default_factory=list)
    visual_anchors: list[str] = Field(default_factory=list)


class CharacterSheetView(BaseModel):
    id: str
    revision_number: int
    generation_key: str | None = None
    candidate_index: int | None = None
    title: str | None = None
    protagonist_name: str | None = None
    summary: str | None = None
    story_function: str | None = None
    protagonist: CharacterProfileView | None = None
    supporting_cast: list[CharacterProfileView] = Field(default_factory=list)
    bedtime_notes: str | None = None
    bedtime_safety_notes: str | None = None
    visual_motifs: list[str] = Field(default_factory=list)
    generation_kind: str = "generated"
    source_pitch_id: str | None = None
    source_pitch_title: str | None = None
    source_character_sheet_id: str | None = None
    source_character_sheet_title: str | None = None
    refinement_instructions: str | None = None
    focus_character_names: list[str] = Field(default_factory=list)
    change_summary: str | None = None
    change_impact: CharacterChangeImpact | None = None
    selection_rationale: str | None = None
    is_selected: bool = False
    accepted_at: datetime | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


class CharacterSheetBatchView(BaseModel):
    generation_key: str
    candidate_count: int
    created_at: datetime
    generation_kind: str = "generated"
    guidance: str | None = None
    source_pitch_id: str | None = None
    source_pitch_title: str | None = None
    source_character_sheet_id: str | None = None
    source_character_sheet_title: str | None = None
    refinement_instructions: str | None = None
    focus_character_names: list[str] = Field(default_factory=list)
    change_summary: str | None = None
    change_impact: CharacterChangeImpact | None = None
    character_sheets: list[CharacterSheetView] = Field(default_factory=list)


class BeatSheetView(BaseModel):
    id: str
    revision_number: int
    summary: str | None = None
    beats: dict[str, Any] | list[Any] | None = None
    bedtime_notes: str | None = None
    accepted_at: datetime | None = None


class StorySetupView(BaseModel):
    id: str
    revision_number: int
    target_word_count: int | None = None
    target_runtime_minutes: int | None = None
    chapter_count: int | None = None
    chapter_style: str | None = None
    guidance_notes: str | None = None
    preferences: dict[str, Any] | list[Any] | None = None
    accepted_at: datetime | None = None


class CompositionJobView(BaseModel):
    id: str
    job_kind: str
    status: str
    progress_percent: float
    current_segment_index: int | None = None
    attempt_count: int
    stop_reason: str | None = None
    error_message: str | None = None
    started_at: datetime | None = None
    completed_at: datetime | None = None
    created_at: datetime
    updated_at: datetime


class AudioJobView(BaseModel):
    id: str
    status: str
    voice_key: str | None = None
    playback_speed: float
    include_background_music: bool
    music_profile: str | None = None
    estimated_duration_seconds: int | None = None
    current_segment_index: int | None = None
    attempt_count: int
    stop_reason: str | None = None
    error_message: str | None = None
    started_at: datetime | None = None
    completed_at: datetime | None = None
    created_at: datetime
    updated_at: datetime


class SessionAssetView(BaseModel):
    id: str
    asset_kind: str
    status: str
    storage_bucket: str
    object_path: str
    mime_type: str
    byte_size: int | None = None
    checksum_sha256: str | None = None
    segment_index: int | None = None
    error_message: str | None = None
    ready_at: datetime | None = None
    failed_at: datetime | None = None
    created_at: datetime
    updated_at: datetime


class ConversationMemoryWorkflow(BaseModel):
    current_stage: WorkflowStage
    current_stage_status: WorkflowStageState
    resume_stage: WorkflowStage
    overall_status: WorkflowStageState


class ConversationMemorySummaryData(BaseModel):
    schema_version: int = Field(default=1, ge=1)
    session_title: str
    workflow: ConversationMemoryWorkflow
    story_decisions: list[str] = Field(default_factory=list)
    user_preferences: list[str] = Field(default_factory=list)
    unresolved_questions: list[str] = Field(default_factory=list)
    active_jobs: list[str] = Field(default_factory=list)


class ConversationMemorySnapshotView(BaseModel):
    id: str
    trigger_event_id: str | None = None
    trigger_event_type: str | None = None
    trigger_event_sequence_number: int | None = None
    summary_text: str
    summary_data: ConversationMemorySummaryData
    created_at: datetime


class CreateSessionRequest(BaseModel):
    working_title: str | None = None


class SelectSessionGenreRequest(BaseModel):
    genre_id: str | None = Field(default=None, min_length=1)
    genre_slug: str | None = Field(default=None, min_length=1)
    genre_label: str | None = Field(default=None, min_length=1)
    origin: str = Field(default="workspace", min_length=1)

    @model_validator(mode="after")
    def validate_selector(self) -> "SelectSessionGenreRequest":
        selectors = [
            self.genre_id,
            self.genre_slug,
            self.genre_label,
        ]
        selected_count = sum(value is not None for value in selectors)
        if selected_count != 1:
            raise ValueError("exactly one of genre_id, genre_slug, or genre_label is required")

        return self


class SelectSessionToneRequest(BaseModel):
    tone_profile_id: str | None = Field(default=None, min_length=1)
    tone_profile_slug: str | None = Field(default=None, min_length=1)
    tone_profile_label: str | None = Field(default=None, min_length=1)
    origin: str = Field(default="workspace", min_length=1)

    @model_validator(mode="after")
    def validate_selector(self) -> "SelectSessionToneRequest":
        selectors = [
            self.tone_profile_id,
            self.tone_profile_slug,
            self.tone_profile_label,
        ]
        selected_count = sum(value is not None for value in selectors)
        if selected_count != 1:
            raise ValueError(
                "exactly one of tone_profile_id, tone_profile_slug, or "
                "tone_profile_label is required"
            )

        return self


class SessionSelectionResponse(BaseModel):
    snapshot: "SessionSnapshot"
    event: SessionEventView


class GenerateSessionPitchesRequest(BaseModel):
    candidate_count: int = Field(default=3, ge=2, le=6)
    guidance: str | None = Field(default=None, min_length=1)
    preserve_selected_pitch: bool = False
    origin: str = Field(default="workspace", min_length=1)


class SessionPitchGenerationResponse(BaseModel):
    snapshot: "SessionSnapshot"
    event: SessionEventView


class GenerateSessionCharacterSheetsRequest(BaseModel):
    candidate_count: int = Field(default=3, ge=2, le=5)
    guidance: str | None = Field(default=None, min_length=1)
    origin: str = Field(default="workspace", min_length=1)


class SessionCharacterSheetGenerationResponse(BaseModel):
    snapshot: "SessionSnapshot"
    event: SessionEventView


class SelectSessionPitchRequest(BaseModel):
    pitch_id: str | None = Field(default=None, min_length=1)
    generation_key: str | None = Field(default=None, min_length=1)
    pitch_index: int | None = Field(default=None, ge=1)
    title: str | None = Field(default=None, min_length=1)
    origin: str = Field(default="workspace", min_length=1)

    @model_validator(mode="after")
    def validate_selector(self) -> "SelectSessionPitchRequest":
        selectors = [
            self.pitch_id,
            self.generation_key,
            self.pitch_index,
            self.title,
        ]
        selected_count = sum(value is not None for value in selectors)
        if selected_count == 0:
            raise ValueError("one of pitch_id, generation_key, pitch_index, or title is required")

        return self


class SelectSessionCharacterSheetRequest(BaseModel):
    character_sheet_id: str | None = Field(default=None, min_length=1)
    revision_number: int | None = Field(default=None, ge=1)
    title: str | None = Field(default=None, min_length=1)
    origin: str = Field(default="workspace", min_length=1)

    @model_validator(mode="after")
    def validate_selector(self) -> "SelectSessionCharacterSheetRequest":
        selectors = [
            self.character_sheet_id,
            self.revision_number,
            self.title,
        ]
        selected_count = sum(value is not None for value in selectors)
        if selected_count == 0:
            raise ValueError(
                "one of character_sheet_id, revision_number, or title is required"
            )

        return self


class RefineSessionPitchRequest(BaseModel):
    pitch_id: str | None = Field(default=None, min_length=1)
    generation_key: str | None = Field(default=None, min_length=1)
    pitch_index: int | None = Field(default=None, ge=1)
    title: str | None = Field(default=None, min_length=1)
    instructions: str = Field(min_length=1)
    origin: str = Field(default="workspace", min_length=1)

    @model_validator(mode="after")
    def validate_selector(self) -> "RefineSessionPitchRequest":
        selectors = [
            self.pitch_id,
            self.generation_key,
            self.pitch_index,
            self.title,
        ]
        selected_count = sum(value is not None for value in selectors)
        if selected_count == 0:
            raise ValueError("one of pitch_id, generation_key, pitch_index, or title is required")

        return self


class RefineSessionCharacterSheetRequest(BaseModel):
    character_sheet_id: str | None = Field(default=None, min_length=1)
    revision_number: int | None = Field(default=None, ge=1)
    title: str | None = Field(default=None, min_length=1)
    instructions: str = Field(min_length=1)
    focus_character_names: list[str] = Field(default_factory=list)
    change_summary: str | None = Field(default=None, min_length=1)
    change_impact: CharacterChangeImpact | None = None
    origin: str = Field(default="workspace", min_length=1)


class SaveSessionStoryBriefRequest(BaseModel):
    story_idea: str | None = Field(default=None, min_length=1)
    desired_themes: str | None = Field(default=None, min_length=1)
    key_images: str | None = Field(default=None, min_length=1)
    audience_notes: str | None = Field(default=None, min_length=1)
    must_have_elements: str | None = Field(default=None, min_length=1)
    raw_brief: str | None = Field(default=None, min_length=1)
    normalized_summary: str | None = Field(default=None, min_length=1)
    normalized_preferences: NormalizedBriefPreferences | None = None
    planning_notes: str | None = Field(default=None, min_length=1)
    edit_mode: StoryBriefEditMode = StoryBriefEditMode.REPLACE
    origin: str = Field(default="workspace", min_length=1)

    @model_validator(mode="after")
    def validate_content(self) -> "SaveSessionStoryBriefRequest":
        values = [
            self.story_idea,
            self.desired_themes,
            self.key_images,
            self.audience_notes,
            self.must_have_elements,
            self.raw_brief,
            self.normalized_summary,
            self.normalized_preferences,
            self.planning_notes,
        ]
        if all(value is None for value in values):
            raise ValueError("story brief saves require at least one populated field")

        return self


class SessionStoryBriefResponse(BaseModel):
    snapshot: "SessionSnapshot"
    event: SessionEventView


class RecordSessionUIActionRequest(BaseModel):
    action: str = Field(min_length=1)
    stage: WorkflowStage | None = None
    control_id: str | None = None
    value_summary: str | None = None
    origin: str = Field(default="workspace", min_length=1)


class SessionContextStageNoteValues(BaseModel):
    detail: str | None = None


class SessionContextUpdateRequest(BaseModel):
    target_kind: Literal["stage_note"] = "stage_note"
    stage: WorkflowStage
    control_id: str | None = None
    origin: str = Field(default="workspace", min_length=1)
    values: SessionContextStageNoteValues


class SessionContextUpdateResponse(BaseModel):
    snapshot: "SessionSnapshot"
    event: SessionEventView


class RecentSessionSummary(BaseModel):
    id: str
    display_title: str
    working_title: str | None = None
    current_stage: WorkflowStage
    resume_stage: WorkflowStage
    furthest_completed_stage: WorkflowStage | None = None
    overall_status: WorkflowStageState
    created_at: datetime
    updated_at: datetime
    completed_at: datetime | None = None
    selected_genre: SessionCatalogSelection | None = None
    selected_tone_profile: SessionCatalogSelection | None = None
    progress: SessionProgress


class SessionSnapshot(BaseModel):
    id: str
    display_title: str
    working_title: str | None = None
    current_stage: WorkflowStage
    resume_stage: WorkflowStage
    furthest_completed_stage: WorkflowStage | None = None
    overall_status: WorkflowStageState
    created_at: datetime
    updated_at: datetime
    completed_at: datetime | None = None
    selected_genre: SessionCatalogSelection | None = None
    selected_tone_profile: SessionCatalogSelection | None = None
    progress: SessionProgress
    stage_states: list[SessionStageStateView] = Field(default_factory=list)
    story_brief: StoryBriefView | None = None
    pitch_batches: list[PitchBatchView] = Field(default_factory=list)
    selected_pitch: PitchView | None = None
    character_sheet_batches: list[CharacterSheetBatchView] = Field(default_factory=list)
    selected_character_sheet: CharacterSheetView | None = None
    selected_beat_sheet: BeatSheetView | None = None
    selected_story_setup: StorySetupView | None = None
    latest_composition_job: CompositionJobView | None = None
    latest_audio_job: AudioJobView | None = None
    active_composition_job: CompositionJobView | None = None
    active_audio_job: AudioJobView | None = None
    latest_story_asset: SessionAssetView | None = None
    latest_audio_asset: SessionAssetView | None = None
    conversation_memory: ConversationMemorySnapshotView | None = None
    agent_context_summary: str | None = None


class SessionHydrationMetadata(BaseModel):
    strategy: Literal["materialized_only", "materialized_with_recent_replay"] = "materialized_only"
    materialized_through_sequence_number: int | None = Field(default=None, ge=1)
    replay_from_sequence_number: int | None = Field(default=None, ge=1)
    replayed_event_count: int = Field(default=0, ge=0)
    latest_sequence_number: int | None = Field(default=None, ge=0)
    history_event_count: int = Field(default=0, ge=0)
    history_window_truncated: bool = False


class SessionHydrationView(BaseModel):
    snapshot: SessionSnapshot
    recent_history: SessionHistoryView
    hydration: SessionHydrationMetadata


ExportAssetView = SessionAssetView


SessionContextUpdateResponse.model_rebuild()
SessionCharacterSheetGenerationResponse.model_rebuild()
SessionPitchGenerationResponse.model_rebuild()
SessionSelectionResponse.model_rebuild()
SessionStoryBriefResponse.model_rebuild()
SessionHydrationView.model_rebuild()
