from __future__ import annotations

from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, Field, model_validator

from app.models.audio_settings import (
    AudioMusicProfile,
    AudioNarrationStyle,
    AudioSettingsView,
    AudioVoiceKey,
)
from app.models.brief_normalization import NormalizedBriefPreferences
from app.models.chat_actions import (
    CharacterChangeImpact,
    CompositionStartMode,
    StoryBriefEditMode,
)
from app.models.composition_interruptions import CompositionInterruptionRequestView
from app.models.continuity import ContinuityBibleView
from app.models.events import SessionEventView, SessionHistoryView
from app.models.model_usage import (
    SessionUsageDiagnosticsView,
    SessionUsageSummaryView,
)
from app.models.story_outline import StoryOutlineCard, StoryOutlineChangeImpact
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


class SessionArtifactReadinessView(BaseModel):
    story_text: Literal["ready", "missing"] = "missing"
    story_docx: Literal["ready", "missing"] = "missing"
    final_audio: Literal["ready", "missing", "stale"] = "missing"
    ready_count: int = Field(default=0, ge=0, le=3)
    total_count: int = Field(default=3, ge=3, le=3)


class SessionLibrarySummaryView(BaseModel):
    display_kind: Literal["draft_session", "completed_story", "polished_story"]
    title_source: Literal[
        "working_title",
        "pitch_title",
        "story_idea",
        "normalized_summary",
        "raw_brief",
        "fallback",
    ]
    runtime_seconds: int | None = Field(default=None, ge=1)
    runtime_source: Literal["final_audio", "audio_job_estimate", "story_setup"] | None = None
    artifact_readiness: SessionArtifactReadinessView


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


class BeatSheetBeatView(BaseModel):
    key: str
    label: str
    order: int
    summary: str
    emotional_intent: str | None = None
    bedtime_softening_note: str | None = None


class BeatSheetEditView(BaseModel):
    id: str
    summary_text: str
    origin: str = "workspace"
    changed_fields: list[str] = Field(default_factory=list)
    beat_keys: list[str] = Field(default_factory=list)
    material_change: bool = False
    refreshes_downstream: bool = False
    created_at: datetime


class BeatSheetView(BaseModel):
    id: str
    revision_number: int
    generation_kind: str = "generated"
    summary: str | None = None
    beats: list[BeatSheetBeatView] = Field(default_factory=list)
    bedtime_notes: str | None = None
    source_beat_sheet_id: str | None = None
    source_beat_sheet_revision_number: int | None = None
    guidance: str | None = None
    refinement_instructions: str | None = None
    focus_beats: list[str] = Field(default_factory=list)
    bedtime_goal: str | None = None
    selection_rationale: str | None = None
    edit_history: list[BeatSheetEditView] = Field(default_factory=list)
    is_selected: bool = False
    accepted_at: datetime | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


class StorySetupView(BaseModel):
    id: str
    revision_number: int
    target_word_count: int | None = None
    target_runtime_minutes: int | None = None
    chapter_count: int | None = None
    approximate_scene_count: int | None = None
    chapter_style: str | None = None
    guidance_notes: str | None = None
    preferences: dict[str, Any] | list[Any] | None = None
    accepted_at: datetime | None = None


class StoryOutlineEditView(BaseModel):
    summary_text: str
    origin: str
    changed_fields: list[str] = Field(default_factory=list)
    changed_card_keys: list[str] = Field(default_factory=list)
    regenerated_card_keys: list[str] = Field(default_factory=list)
    change_impact: StoryOutlineChangeImpact | None = None
    reordered: bool = False
    refreshes_downstream: bool = False
    invalidated_stages: list[WorkflowStage] = Field(default_factory=list)
    created_at: datetime


class StoryOutlineView(BaseModel):
    id: str
    revision_number: int
    outline_kind: str
    summary: str | None = None
    cards: list[StoryOutlineCard] = Field(default_factory=list)
    genre_label: str | None = None
    tone_label: str | None = None
    target_word_count: int | None = None
    target_runtime_minutes: int | None = None
    chapter_count: int | None = None
    approximate_scene_count: int | None = None
    chapter_style: str | None = None
    guidance_notes: str | None = None
    bedtime_goal: str | None = None
    last_change_summary: str | None = None
    change_impact: StoryOutlineChangeImpact | None = None
    refreshes_downstream: bool = False
    invalidated_stages: list[WorkflowStage] = Field(default_factory=list)
    edit_history: list[StoryOutlineEditView] = Field(default_factory=list)
    is_selected: bool = False
    accepted_at: datetime | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


class PlanArtifactRefView(BaseModel):
    id: str
    label: str
    revision_number: int | None = None


class PlanRevisionView(BaseModel):
    id: str
    revision_number: int
    source_stage: WorkflowStage | None = None
    change_summary: str | None = None
    comparison_summary: str | None = None
    restored_from_revision_number: int | None = None
    changed_artifacts: list[str] = Field(default_factory=list)
    pitch: PlanArtifactRefView | None = None
    character_sheet: PlanArtifactRefView | None = None
    beat_sheet: PlanArtifactRefView | None = None
    story_setup: PlanArtifactRefView | None = None
    story_outline: PlanArtifactRefView | None = None
    is_current: bool = False
    created_at: datetime
    updated_at: datetime


class CompositionSegmentVersionView(BaseModel):
    id: str
    composition_job_id: str
    job_kind: str
    segment_index: int
    revision_number: int
    status: str
    acceptance_state: str
    is_current: bool = False
    is_stale: bool = False
    planned_summary: str | None = None
    accepted_summary: str | None = None
    text_content: str | None = None
    word_count: int | None = None
    created_at: datetime
    updated_at: datetime
    completed_at: datetime | None = None


class CompositionSegmentView(BaseModel):
    segment_index: int
    outline_card_title: str | None = None
    outline_card_summary: str | None = None
    current_version_id: str | None = None
    current_revision_number: int | None = None
    pending_version_id: str | None = None
    pending_revision_number: int | None = None
    is_stale: bool = False
    stale_reason: str | None = None
    versions: list[CompositionSegmentVersionView] = Field(default_factory=list)


class CompositionJobView(BaseModel):
    id: str
    job_kind: str
    status: str
    progress_percent: float
    total_segments: int | None = None
    start_segment_index: int | None = None
    plan_revision_id: str | None = None
    plan_revision_number: int | None = None
    beat_sheet_id: str | None = None
    beat_sheet_revision_number: int | None = None
    story_setup_id: str | None = None
    story_setup_revision_number: int | None = None
    story_outline_id: str | None = None
    story_outline_revision_number: int | None = None
    current_segment_id: str | None = None
    current_segment_index: int | None = None
    rewrite_to_segment_index: int | None = None
    downstream_regeneration_mode: str = "none"
    stale_from_segment_index: int | None = None
    stale_to_segment_index: int | None = None
    pending_review: bool = False
    rewrite_candidate_segment_indexes: list[int] = Field(default_factory=list)
    accepted_story_so_far: str | None = None
    latest_partial_output: str | None = None
    latest_segment_summary: str | None = None
    status_message: str | None = None
    interruption_request: CompositionInterruptionRequestView | None = None
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
    progress_percent: float = 0
    current_step: str | None = None
    current_step_index: int | None = None
    total_steps: int | None = None
    completed_segments: int | None = None
    estimated_duration_seconds: int | None = None
    total_segments: int | None = None
    current_segment_index: int | None = None
    latest_asset_id: str | None = None
    latest_asset_kind: str | None = None
    attempt_count: int
    stop_reason: str | None = None
    error_message: str | None = None
    started_at: datetime | None = None
    completed_at: datetime | None = None
    created_at: datetime
    updated_at: datetime


class SessionAssetAccessView(BaseModel):
    download_path: str
    filename: str
    stream_path: str | None = None


class SessionAssetView(BaseModel):
    id: str
    asset_kind: str
    status: str
    storage_bucket: str
    object_path: str
    mime_type: str
    composition_job_id: str | None = None
    audio_job_id: str | None = None
    byte_size: int | None = None
    duration_seconds: float | None = None
    checksum_sha256: str | None = None
    segment_index: int | None = None
    error_message: str | None = None
    details: dict[str, Any] | None = None
    access: SessionAssetAccessView | None = None
    public_url: str | None = None
    ready_at: datetime | None = None
    failed_at: datetime | None = None
    superseded_at: datetime | None = None
    created_at: datetime
    updated_at: datetime


class SessionArtifactInventoryItemView(BaseModel):
    key: Literal["story_text", "story_docx", "final_audio"]
    label: str
    artifact_kind: str
    status: Literal["missing", "generating", "ready", "failed", "stale"]
    status_detail: str
    asset: SessionAssetView | None = None
    preview_assets: list[SessionAssetView] = Field(default_factory=list)
    preview_asset_count: int = Field(default=0, ge=0)
    download_path: str | None = None
    stream_path: str | None = None


class SessionArtifactInventoryView(BaseModel):
    session_id: str
    generated_at: datetime
    items: list[SessionArtifactInventoryItemView] = Field(default_factory=list)


class NarrationSegmentView(BaseModel):
    id: str
    audio_job_id: str
    segment_index: int
    status: str
    source_boundary_kind: str
    source_outline_card_title: str | None = None
    word_count: int
    pause_after_seconds: int = 0
    pause_hint: str
    split_reason: str | None = None
    text_preview: str | None = None
    error_message: str | None = None
    completed_at: datetime | None = None
    preview_asset: SessionAssetView | None = None


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


class GenerateSessionBeatSheetRequest(BaseModel):
    guidance: str | None = Field(default=None, min_length=1)
    focus_beats: list[str] = Field(default_factory=list)
    bedtime_goal: str | None = Field(default=None, min_length=1)
    origin: str = Field(default="workspace", min_length=1)


class SessionBeatSheetGenerationResponse(BaseModel):
    snapshot: "SessionSnapshot"
    event: SessionEventView


class SaveSessionStorySetupRequest(BaseModel):
    target_word_count: int | None = Field(default=None, ge=100, le=10000)
    target_runtime_minutes: int | None = Field(default=None, ge=1, le=180)
    chapter_count: int | None = Field(default=None, ge=1, le=24)
    approximate_scene_count: int | None = Field(default=None, ge=1, le=48)
    guidance_notes: str | None = Field(default=None, min_length=1)
    origin: str = Field(default="workspace", min_length=1)

    @model_validator(mode="after")
    def validate_content(self) -> "SaveSessionStorySetupRequest":
        editable_fields = {
            "target_word_count",
            "target_runtime_minutes",
            "chapter_count",
            "approximate_scene_count",
            "guidance_notes",
        }
        if not editable_fields.intersection(self.model_fields_set):
            raise ValueError("story setup saves require at least one provided field")

        return self


class SessionStorySetupResponse(BaseModel):
    snapshot: "SessionSnapshot"
    event: SessionEventView


class SaveSessionAudioSettingsRequest(BaseModel):
    voice_key: AudioVoiceKey | None = None
    narration_style: AudioNarrationStyle | None = None
    playback_speed: float | None = Field(default=None, ge=0.5, le=2.0)
    include_background_music: bool | None = None
    music_profile: AudioMusicProfile | None = None
    narration_volume: int | None = Field(default=None, ge=0, le=100)
    music_volume: int | None = Field(default=None, ge=0, le=100)
    guidance_notes: str | None = Field(default=None, min_length=1)
    origin: str = Field(default="workspace", min_length=1)

    @model_validator(mode="after")
    def validate_content(self) -> "SaveSessionAudioSettingsRequest":
        editable_fields = {
            "voice_key",
            "narration_style",
            "playback_speed",
            "include_background_music",
            "music_profile",
            "narration_volume",
            "music_volume",
            "guidance_notes",
        }
        if not editable_fields.intersection(self.model_fields_set):
            raise ValueError("audio settings saves require at least one provided field")

        return self


class SessionAudioSettingsResponse(BaseModel):
    snapshot: "SessionSnapshot"
    event: SessionEventView


class EditSessionStoryOutlineCardRequest(BaseModel):
    card_key: str = Field(min_length=1)
    card_type: str = Field(min_length=1)
    position: int = Field(ge=1)
    title: str = Field(min_length=1)
    purpose: str | None = Field(default=None, min_length=1)
    summary: str = Field(min_length=1)
    beat_keys: list[str] = Field(default_factory=list)
    beat_labels: list[str] = Field(default_factory=list)
    emotional_shift: str = Field(min_length=1)
    target_word_count: int | None = Field(default=None, ge=1)
    target_runtime_minutes: int | None = Field(default=None, ge=1)
    target_scene_count: int | None = Field(default=None, ge=1)
    tone_direction: str | None = Field(default=None, min_length=1)
    bedtime_guardrail: str | None = Field(default=None, min_length=1)
    drafting_brief: str | None = Field(default=None, min_length=1)

    @model_validator(mode="after")
    def validate_beats(self) -> "EditSessionStoryOutlineCardRequest":
        if not self.beat_keys:
            raise ValueError("story outline cards require at least one supporting beat")
        return self


class SaveSessionStoryOutlineRequest(BaseModel):
    outline_id: str | None = Field(default=None, min_length=1)
    summary: str | None = Field(default=None, min_length=1)
    cards: list[EditSessionStoryOutlineCardRequest] = Field(default_factory=list)
    regenerate_card_keys: list[str] = Field(default_factory=list)
    origin: str = Field(default="workspace", min_length=1)

    @model_validator(mode="after")
    def validate_cards(self) -> "SaveSessionStoryOutlineRequest":
        if not self.cards:
            raise ValueError("story outline saves require at least one card")
        return self


class SessionStoryOutlineResponse(BaseModel):
    snapshot: "SessionSnapshot"
    event: SessionEventView


class StartSessionCompositionRequest(BaseModel):
    mode: CompositionStartMode = CompositionStartMode.FRESH
    instructions: str | None = Field(default=None, min_length=1)
    restart_from_segment_index: int | None = Field(default=None, ge=1)
    rewrite_to_segment_index: int | None = Field(default=None, ge=1)
    downstream_regeneration_mode: (
        Literal["none", "auto_regenerate", "require_confirmation"] | None
    ) = None
    origin: str = Field(default="workspace", min_length=1)

    @model_validator(mode="after")
    def validate_mode_requirements(self) -> "StartSessionCompositionRequest":
        if self.mode == CompositionStartMode.REWRITE and self.restart_from_segment_index is None:
            raise ValueError("rewrite composition starts require restart_from_segment_index")
        if (
            self.restart_from_segment_index is not None
            and self.rewrite_to_segment_index is not None
            and self.rewrite_to_segment_index < self.restart_from_segment_index
        ):
            raise ValueError(
                "rewrite_to_segment_index cannot be earlier than "
                "restart_from_segment_index"
            )
        return self


class RedirectSessionCompositionRequest(BaseModel):
    instructions: str = Field(min_length=1)
    rewrite_from_segment_index: int | None = Field(default=None, ge=1)
    rewrite_to_segment_index: int | None = Field(default=None, ge=1)
    downstream_regeneration_mode: (
        Literal["none", "auto_regenerate", "require_confirmation"] | None
    ) = None
    origin: str = Field(default="workspace", min_length=1)

    @model_validator(mode="after")
    def validate_range(self) -> "RedirectSessionCompositionRequest":
        if (
            self.rewrite_from_segment_index is not None
            and self.rewrite_to_segment_index is not None
            and self.rewrite_to_segment_index < self.rewrite_from_segment_index
        ):
            raise ValueError(
                "rewrite_to_segment_index cannot be earlier than "
                "rewrite_from_segment_index"
            )
        return self


class AcceptRewriteSessionCompositionRequest(BaseModel):
    origin: str = Field(default="workspace", min_length=1)


class RejectRewriteSessionCompositionRequest(BaseModel):
    origin: str = Field(default="workspace", min_length=1)


class SelectCompositionSegmentVersionRequest(BaseModel):
    origin: str = Field(default="workspace", min_length=1)


class SessionCompositionResponse(BaseModel):
    snapshot: "SessionSnapshot"
    event: SessionEventView
    job: CompositionJobView


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
            raise ValueError("one of character_sheet_id, revision_number, or title is required")

        return self


class SelectSessionBeatSheetRequest(BaseModel):
    beat_sheet_id: str | None = Field(default=None, min_length=1)
    revision_number: int | None = Field(default=None, ge=1)
    origin: str = Field(default="workspace", min_length=1)

    @model_validator(mode="after")
    def validate_selector(self) -> "SelectSessionBeatSheetRequest":
        selectors = [
            self.beat_sheet_id,
            self.revision_number,
        ]
        selected_count = sum(value is not None for value in selectors)
        if selected_count == 0:
            raise ValueError("one of beat_sheet_id or revision_number is required")

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


class RefineSessionBeatSheetRequest(BaseModel):
    beat_sheet_id: str | None = Field(default=None, min_length=1)
    revision_number: int | None = Field(default=None, ge=1)
    instructions: str = Field(min_length=1)
    beat_names: list[str] = Field(default_factory=list)
    bedtime_goal: str | None = Field(default=None, min_length=1)
    origin: str = Field(default="workspace", min_length=1)


class EditSessionBeatSheetBeatRequest(BaseModel):
    key: str = Field(min_length=1)
    summary: str | None = Field(default=None, min_length=1)
    emotional_intent: str | None = Field(default=None, min_length=1)
    bedtime_softening_note: str | None = Field(default=None, min_length=1)

    @model_validator(mode="after")
    def validate_content(self) -> "EditSessionBeatSheetBeatRequest":
        if (
            self.summary is None
            and self.emotional_intent is None
            and self.bedtime_softening_note is None
        ):
            raise ValueError("beat updates require at least one edited field")

        return self


class EditSessionBeatSheetRequest(BaseModel):
    beat_sheet_id: str | None = Field(default=None, min_length=1)
    revision_number: int | None = Field(default=None, ge=1)
    summary: str | None = Field(default=None, min_length=1)
    bedtime_notes: str | None = Field(default=None, min_length=1)
    bedtime_goal: str | None = Field(default=None, min_length=1)
    beat_updates: list[EditSessionBeatSheetBeatRequest] = Field(default_factory=list)
    summary_text: str | None = Field(default=None, min_length=1)
    origin: str = Field(default="workspace", min_length=1)

    @model_validator(mode="after")
    def validate_content(self) -> "EditSessionBeatSheetRequest":
        values = [
            self.summary,
            self.bedtime_notes,
            self.bedtime_goal,
        ]
        if not self.beat_updates and all(value is None for value in values):
            raise ValueError("beat-sheet edits require at least one top-level field or beat update")

        return self


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


class SessionBeatSheetUpdateResponse(BaseModel):
    snapshot: "SessionSnapshot"
    event: SessionEventView


class RestoreSessionPlanRevisionRequest(BaseModel):
    origin: str = Field(default="workspace", min_length=1)


class RecentSessionSummary(BaseModel):
    id: str
    owner_id: str
    display_title: str
    working_title: str | None = None
    library_summary: SessionLibrarySummaryView
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
    owner_id: str
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
    beat_sheet_revisions: list[BeatSheetView] = Field(default_factory=list)
    selected_beat_sheet: BeatSheetView | None = None
    selected_story_setup: StorySetupView | None = None
    story_outline_revisions: list[StoryOutlineView] = Field(default_factory=list)
    selected_story_outline: StoryOutlineView | None = None
    plan_revisions: list[PlanRevisionView] = Field(default_factory=list)
    current_plan_revision: PlanRevisionView | None = None
    latest_composition_job: CompositionJobView | None = None
    latest_audio_job: AudioJobView | None = None
    active_composition_job: CompositionJobView | None = None
    active_audio_job: AudioJobView | None = None
    composition_segments: list[CompositionSegmentView] = Field(default_factory=list)
    audio_segments: list[NarrationSegmentView] = Field(default_factory=list)
    latest_story_asset: SessionAssetView | None = None
    latest_story_export_asset: SessionAssetView | None = None
    latest_audio_asset: SessionAssetView | None = None
    audio_settings: AudioSettingsView
    continuity_bible: ContinuityBibleView | None = None
    usage_summary: SessionUsageSummaryView = Field(default_factory=SessionUsageSummaryView)
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


class SessionDebugInspectorView(BaseModel):
    session_id: str
    generated_at: datetime
    snapshot: SessionSnapshot
    hydration: SessionHydrationMetadata
    recent_history: SessionHistoryView
    artifact_inventory: SessionArtifactInventoryView
    usage_diagnostics: SessionUsageDiagnosticsView


ExportAssetView = SessionAssetView


SessionContextUpdateResponse.model_rebuild()
SessionAudioSettingsResponse.model_rebuild()
SessionBeatSheetGenerationResponse.model_rebuild()
SessionBeatSheetUpdateResponse.model_rebuild()
SessionCharacterSheetGenerationResponse.model_rebuild()
SessionPitchGenerationResponse.model_rebuild()
SessionSelectionResponse.model_rebuild()
SessionStoryBriefResponse.model_rebuild()
SessionStoryOutlineResponse.model_rebuild()
SessionStorySetupResponse.model_rebuild()
SessionArtifactInventoryView.model_rebuild()
SessionHydrationView.model_rebuild()
SessionDebugInspectorView.model_rebuild()
