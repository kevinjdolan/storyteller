from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any

from sqlalchemy import (
    JSON,
    Boolean,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    Numeric,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy import (
    Enum as SQLAlchemyEnum,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin, UUIDPrimaryKeyMixin, utc_now
from app.models.events import EventActorType
from app.models.workflow import WorkflowStage, WorkflowStageState


def _enum_values(enum_cls: type[Enum]) -> list[str]:
    return [member.value for member in enum_cls]


def build_enum(enum_cls: type[Enum], name: str) -> SQLAlchemyEnum:
    return SQLAlchemyEnum(
        enum_cls,
        name=name,
        native_enum=False,
        values_callable=_enum_values,
        validate_strings=True,
    )


class JobStatus(str, Enum):
    QUEUED = "queued"
    IN_PROGRESS = "in_progress"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class CompositionJobKind(str, Enum):
    DRAFT = "draft"
    REWRITE = "rewrite"


class AssetKind(str, Enum):
    STORY_TEXT = "story_text"
    STORY_DOCX = "story_docx"
    AUDIO_SEGMENT = "audio_segment"
    FINAL_AUDIO = "final_audio"


class AssetStatus(str, Enum):
    PENDING = "pending"
    READY = "ready"
    FAILED = "failed"
    SUPERSEDED = "superseded"


WORKFLOW_STAGE_ENUM = build_enum(WorkflowStage, "workflow_stage")
WORKFLOW_STAGE_STATE_ENUM = build_enum(WorkflowStageState, "workflow_stage_state")
JOB_STATUS_ENUM = build_enum(JobStatus, "job_status")
COMPOSITION_JOB_KIND_ENUM = build_enum(CompositionJobKind, "composition_job_kind")
ASSET_KIND_ENUM = build_enum(AssetKind, "asset_kind")
ASSET_STATUS_ENUM = build_enum(AssetStatus, "asset_status")
EVENT_ACTOR_TYPE_ENUM = build_enum(EventActorType, "event_actor_type")


class Genre(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "genres"

    slug: Mapped[str] = mapped_column(String(80), nullable=False, unique=True)
    label: Mapped[str] = mapped_column(String(120), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    bedtime_safety_notes: Mapped[str | None] = mapped_column(Text)
    arc_notes: Mapped[dict[str, Any] | list[Any] | None] = mapped_column(JSON)
    sort_order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    tone_profiles: Mapped[list["ToneProfile"]] = relationship(
        back_populates="genre",
        cascade="all, delete-orphan",
    )
    sessions: Mapped[list["StorySession"]] = relationship(back_populates="selected_genre")

    __table_args__ = (
        Index("ix_genres_sort_order", "sort_order"),
        Index("ix_genres_is_active", "is_active"),
    )


class ToneProfile(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "tone_profiles"

    genre_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("genres.id", ondelete="CASCADE"),
        nullable=False,
    )
    slug: Mapped[str] = mapped_column(String(80), nullable=False)
    label: Mapped[str] = mapped_column(String(120), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    bedtime_notes: Mapped[str | None] = mapped_column(Text)
    descriptors: Mapped[dict[str, Any] | list[Any] | None] = mapped_column(JSON)
    default_planning_hints: Mapped[dict[str, Any] | list[Any] | None] = mapped_column(JSON)
    sort_order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    genre: Mapped["Genre"] = relationship(back_populates="tone_profiles")
    sessions: Mapped[list["StorySession"]] = relationship(back_populates="selected_tone_profile")

    __table_args__ = (
        UniqueConstraint("genre_id", "slug", name="uq_tone_profiles_genre_id_slug"),
        Index("ix_tone_profiles_genre_id_sort_order", "genre_id", "sort_order"),
        Index("ix_tone_profiles_genre_id_is_active", "genre_id", "is_active"),
    )


class StorySession(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "story_sessions"

    working_title: Mapped[str | None] = mapped_column(String(255))
    current_stage: Mapped[WorkflowStage] = mapped_column(
        WORKFLOW_STAGE_ENUM,
        nullable=False,
        default=WorkflowStage.GENRE,
    )
    resume_stage: Mapped[WorkflowStage] = mapped_column(
        WORKFLOW_STAGE_ENUM,
        nullable=False,
        default=WorkflowStage.GENRE,
    )
    furthest_completed_stage: Mapped[WorkflowStage | None] = mapped_column(WORKFLOW_STAGE_ENUM)
    overall_status: Mapped[WorkflowStageState] = mapped_column(
        WORKFLOW_STAGE_STATE_ENUM,
        nullable=False,
        default=WorkflowStageState.DRAFT,
    )
    selected_genre_id: Mapped[str | None] = mapped_column(
        String(36),
        ForeignKey("genres.id", ondelete="SET NULL"),
    )
    selected_tone_profile_id: Mapped[str | None] = mapped_column(
        String(36),
        ForeignKey("tone_profiles.id", ondelete="SET NULL"),
    )
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    selected_genre: Mapped["Genre | None"] = relationship(back_populates="sessions")
    selected_tone_profile: Mapped["ToneProfile | None"] = relationship(back_populates="sessions")
    workflow_stage_states: Mapped[list["WorkflowStageSnapshot"]] = relationship(
        back_populates="session",
        cascade="all, delete-orphan",
    )
    story_briefs: Mapped[list["StoryBrief"]] = relationship(
        back_populates="session",
        cascade="all, delete-orphan",
    )
    pitches: Mapped[list["Pitch"]] = relationship(
        back_populates="session",
        cascade="all, delete-orphan",
    )
    character_sheets: Mapped[list["CharacterSheet"]] = relationship(
        back_populates="session",
        cascade="all, delete-orphan",
    )
    beat_sheets: Mapped[list["BeatSheet"]] = relationship(
        back_populates="session",
        cascade="all, delete-orphan",
    )
    story_setups: Mapped[list["StorySetup"]] = relationship(
        back_populates="session",
        cascade="all, delete-orphan",
    )
    composition_jobs: Mapped[list["CompositionJob"]] = relationship(
        back_populates="session",
        cascade="all, delete-orphan",
    )
    composition_segments: Mapped[list["CompositionSegment"]] = relationship(
        back_populates="session",
        cascade="all, delete-orphan",
    )
    audio_jobs: Mapped[list["AudioJob"]] = relationship(
        back_populates="session",
        cascade="all, delete-orphan",
    )
    export_assets: Mapped[list["ExportAsset"]] = relationship(
        back_populates="session",
        cascade="all, delete-orphan",
    )
    event_log_entries: Mapped[list["EventLogEntry"]] = relationship(
        back_populates="session",
        cascade="all, delete-orphan",
    )

    __table_args__ = (
        Index("ix_story_sessions_overall_status_updated_at", "overall_status", "updated_at"),
        Index("ix_story_sessions_resume_stage", "resume_stage"),
        Index("ix_story_sessions_current_stage", "current_stage"),
        Index("ix_story_sessions_selected_genre_id", "selected_genre_id"),
    )


class EventLogEntry(UUIDPrimaryKeyMixin, Base):
    __tablename__ = "event_log_entries"

    session_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("story_sessions.id", ondelete="CASCADE"),
        nullable=False,
    )
    sequence_number: Mapped[int] = mapped_column(Integer, nullable=False)
    actor_type: Mapped[EventActorType] = mapped_column(EVENT_ACTOR_TYPE_ENUM, nullable=False)
    actor_id: Mapped[str | None] = mapped_column(String(120))
    event_type: Mapped[str] = mapped_column(String(120), nullable=False)
    stage: Mapped[WorkflowStage | None] = mapped_column(WORKFLOW_STAGE_ENUM)
    summary: Mapped[str] = mapped_column(Text, nullable=False)
    payload: Mapped[dict[str, Any] | list[Any] | None] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now,
    )

    session: Mapped["StorySession"] = relationship(back_populates="event_log_entries")
    workflow_stage_states: Mapped[list["WorkflowStageSnapshot"]] = relationship(
        back_populates="last_event",
    )

    __table_args__ = (
        UniqueConstraint(
            "session_id", "sequence_number", name="uq_event_log_entries_session_id_sequence_number"
        ),
        Index("ix_event_log_entries_session_id_created_at", "session_id", "created_at"),
        Index("ix_event_log_entries_session_id_stage", "session_id", "stage"),
    )


class WorkflowStageSnapshot(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "workflow_stage_states"

    session_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("story_sessions.id", ondelete="CASCADE"),
        nullable=False,
    )
    stage: Mapped[WorkflowStage] = mapped_column(WORKFLOW_STAGE_ENUM, nullable=False)
    status: Mapped[WorkflowStageState] = mapped_column(
        WORKFLOW_STAGE_STATE_ENUM,
        nullable=False,
        default=WorkflowStageState.DRAFT,
    )
    detail: Mapped[str | None] = mapped_column(Text)
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    last_event_id: Mapped[str | None] = mapped_column(
        String(36),
        ForeignKey("event_log_entries.id", ondelete="SET NULL"),
    )

    session: Mapped["StorySession"] = relationship(back_populates="workflow_stage_states")
    last_event: Mapped["EventLogEntry | None"] = relationship(
        back_populates="workflow_stage_states"
    )

    __table_args__ = (
        UniqueConstraint("session_id", "stage", name="uq_workflow_stage_states_session_id_stage"),
        Index("ix_workflow_stage_states_session_id_status", "session_id", "status"),
    )


class StoryBrief(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "story_briefs"

    session_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("story_sessions.id", ondelete="CASCADE"),
        nullable=False,
    )
    revision_number: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    raw_brief: Mapped[str] = mapped_column(Text, nullable=False)
    normalized_summary: Mapped[str | None] = mapped_column(Text)
    planning_notes: Mapped[str | None] = mapped_column(Text)
    model_output: Mapped[dict[str, Any] | list[Any] | None] = mapped_column(JSON)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    accepted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    session: Mapped["StorySession"] = relationship(back_populates="story_briefs")
    pitches: Mapped[list["Pitch"]] = relationship(back_populates="story_brief")

    __table_args__ = (
        UniqueConstraint(
            "session_id", "revision_number", name="uq_story_briefs_session_id_revision_number"
        ),
        Index("ix_story_briefs_session_id_is_active", "session_id", "is_active"),
    )


class Pitch(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "pitches"

    session_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("story_sessions.id", ondelete="CASCADE"),
        nullable=False,
    )
    story_brief_id: Mapped[str | None] = mapped_column(
        String(36),
        ForeignKey("story_briefs.id", ondelete="SET NULL"),
    )
    generation_key: Mapped[str] = mapped_column(String(80), nullable=False)
    pitch_index: Mapped[int] = mapped_column(Integer, nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    logline: Mapped[str] = mapped_column(Text, nullable=False)
    summary: Mapped[str | None] = mapped_column(Text)
    bedtime_notes: Mapped[str | None] = mapped_column(Text)
    model_output: Mapped[dict[str, Any] | list[Any] | None] = mapped_column(JSON)
    is_selected: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    accepted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    session: Mapped["StorySession"] = relationship(back_populates="pitches")
    story_brief: Mapped["StoryBrief | None"] = relationship(back_populates="pitches")
    character_sheets: Mapped[list["CharacterSheet"]] = relationship(back_populates="pitch")

    __table_args__ = (
        UniqueConstraint(
            "session_id",
            "generation_key",
            "pitch_index",
            name="uq_pitches_session_id_generation_key_pitch_index",
        ),
        Index("ix_pitches_session_id_is_selected", "session_id", "is_selected"),
    )


class CharacterSheet(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "character_sheets"

    session_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("story_sessions.id", ondelete="CASCADE"),
        nullable=False,
    )
    pitch_id: Mapped[str | None] = mapped_column(
        String(36),
        ForeignKey("pitches.id", ondelete="SET NULL"),
    )
    revision_number: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    title: Mapped[str | None] = mapped_column(String(255))
    summary: Mapped[str | None] = mapped_column(Text)
    protagonist_name: Mapped[str | None] = mapped_column(String(120))
    supporting_cast: Mapped[dict[str, Any] | list[Any] | None] = mapped_column(JSON)
    character_data: Mapped[dict[str, Any] | list[Any] | None] = mapped_column(JSON)
    bedtime_notes: Mapped[str | None] = mapped_column(Text)
    is_selected: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    accepted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    session: Mapped["StorySession"] = relationship(back_populates="character_sheets")
    pitch: Mapped["Pitch | None"] = relationship(back_populates="character_sheets")
    beat_sheets: Mapped[list["BeatSheet"]] = relationship(back_populates="character_sheet")

    __table_args__ = (
        UniqueConstraint(
            "session_id",
            "revision_number",
            name="uq_character_sheets_session_id_revision_number",
        ),
        Index("ix_character_sheets_session_id_is_selected", "session_id", "is_selected"),
    )


class BeatSheet(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "beat_sheets"

    session_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("story_sessions.id", ondelete="CASCADE"),
        nullable=False,
    )
    character_sheet_id: Mapped[str | None] = mapped_column(
        String(36),
        ForeignKey("character_sheets.id", ondelete="SET NULL"),
    )
    revision_number: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    summary: Mapped[str | None] = mapped_column(Text)
    beats: Mapped[dict[str, Any] | list[Any] | None] = mapped_column(JSON)
    bedtime_notes: Mapped[str | None] = mapped_column(Text)
    is_selected: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    accepted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    session: Mapped["StorySession"] = relationship(back_populates="beat_sheets")
    character_sheet: Mapped["CharacterSheet | None"] = relationship(back_populates="beat_sheets")
    story_setups: Mapped[list["StorySetup"]] = relationship(back_populates="beat_sheet")
    composition_jobs: Mapped[list["CompositionJob"]] = relationship(back_populates="beat_sheet")

    __table_args__ = (
        UniqueConstraint(
            "session_id", "revision_number", name="uq_beat_sheets_session_id_revision_number"
        ),
        Index("ix_beat_sheets_session_id_is_selected", "session_id", "is_selected"),
    )


class StorySetup(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "story_setups"

    session_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("story_sessions.id", ondelete="CASCADE"),
        nullable=False,
    )
    beat_sheet_id: Mapped[str | None] = mapped_column(
        String(36),
        ForeignKey("beat_sheets.id", ondelete="SET NULL"),
    )
    revision_number: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    target_word_count: Mapped[int | None] = mapped_column(Integer)
    target_runtime_minutes: Mapped[int | None] = mapped_column(Integer)
    chapter_count: Mapped[int | None] = mapped_column(Integer)
    chapter_style: Mapped[str | None] = mapped_column(String(120))
    guidance_notes: Mapped[str | None] = mapped_column(Text)
    preferences: Mapped[dict[str, Any] | list[Any] | None] = mapped_column(JSON)
    is_selected: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    accepted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    session: Mapped["StorySession"] = relationship(back_populates="story_setups")
    beat_sheet: Mapped["BeatSheet | None"] = relationship(back_populates="story_setups")
    composition_jobs: Mapped[list["CompositionJob"]] = relationship(back_populates="story_setup")

    __table_args__ = (
        UniqueConstraint(
            "session_id", "revision_number", name="uq_story_setups_session_id_revision_number"
        ),
        Index("ix_story_setups_session_id_is_selected", "session_id", "is_selected"),
    )


class CompositionJob(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "composition_jobs"

    session_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("story_sessions.id", ondelete="CASCADE"),
        nullable=False,
    )
    beat_sheet_id: Mapped[str | None] = mapped_column(
        String(36),
        ForeignKey("beat_sheets.id", ondelete="SET NULL"),
    )
    story_setup_id: Mapped[str | None] = mapped_column(
        String(36),
        ForeignKey("story_setups.id", ondelete="SET NULL"),
    )
    job_kind: Mapped[CompositionJobKind] = mapped_column(
        COMPOSITION_JOB_KIND_ENUM,
        nullable=False,
        default=CompositionJobKind.DRAFT,
    )
    status: Mapped[JobStatus] = mapped_column(
        JOB_STATUS_ENUM,
        nullable=False,
        default=JobStatus.QUEUED,
    )
    progress_percent: Mapped[float] = mapped_column(
        Numeric(5, 2, asdecimal=False),
        nullable=False,
        default=0,
    )
    current_segment_index: Mapped[int | None] = mapped_column(Integer)
    attempt_count: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    stop_reason: Mapped[str | None] = mapped_column(String(255))
    error_message: Mapped[str | None] = mapped_column(Text)
    metadata_json: Mapped[dict[str, Any] | list[Any] | None] = mapped_column(JSON)
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    session: Mapped["StorySession"] = relationship(back_populates="composition_jobs")
    beat_sheet: Mapped["BeatSheet | None"] = relationship(back_populates="composition_jobs")
    story_setup: Mapped["StorySetup | None"] = relationship(back_populates="composition_jobs")
    segments: Mapped[list["CompositionSegment"]] = relationship(
        back_populates="composition_job",
        cascade="all, delete-orphan",
    )
    export_assets: Mapped[list["ExportAsset"]] = relationship(back_populates="composition_job")

    __table_args__ = (
        Index(
            "ix_composition_jobs_session_id_status_created_at", "session_id", "status", "created_at"
        ),
        Index("ix_composition_jobs_session_id_job_kind", "session_id", "job_kind"),
    )


class CompositionSegment(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "composition_segments"

    session_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("story_sessions.id", ondelete="CASCADE"),
        nullable=False,
    )
    composition_job_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("composition_jobs.id", ondelete="CASCADE"),
        nullable=False,
    )
    superseded_by_segment_id: Mapped[str | None] = mapped_column(
        String(36),
        ForeignKey(
            "composition_segments.id",
            ondelete="SET NULL",
            name="fk_comp_segments_superseded_by",
        ),
    )
    segment_index: Mapped[int] = mapped_column(Integer, nullable=False)
    revision_number: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    status: Mapped[JobStatus] = mapped_column(
        JOB_STATUS_ENUM,
        nullable=False,
        default=JobStatus.QUEUED,
    )
    planned_summary: Mapped[str | None] = mapped_column(Text)
    text_content: Mapped[str | None] = mapped_column(Text)
    word_count: Mapped[int | None] = mapped_column(Integer)
    payload: Mapped[dict[str, Any] | list[Any] | None] = mapped_column(JSON)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    session: Mapped["StorySession"] = relationship(back_populates="composition_segments")
    composition_job: Mapped["CompositionJob"] = relationship(back_populates="segments")
    superseded_by_segment: Mapped["CompositionSegment | None"] = relationship(
        remote_side="CompositionSegment.id"
    )

    __table_args__ = (
        UniqueConstraint(
            "composition_job_id",
            "segment_index",
            "revision_number",
            name="uq_composition_segments_job_segment_revision",
        ),
        Index("ix_composition_segments_session_id_status", "session_id", "status"),
    )


class AudioJob(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "audio_jobs"

    session_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("story_sessions.id", ondelete="CASCADE"),
        nullable=False,
    )
    source_composition_job_id: Mapped[str | None] = mapped_column(
        String(36),
        ForeignKey("composition_jobs.id", ondelete="SET NULL"),
    )
    status: Mapped[JobStatus] = mapped_column(
        JOB_STATUS_ENUM,
        nullable=False,
        default=JobStatus.QUEUED,
    )
    voice_key: Mapped[str | None] = mapped_column(String(120))
    playback_speed: Mapped[float] = mapped_column(
        Numeric(4, 2, asdecimal=False),
        nullable=False,
        default=1.0,
    )
    include_background_music: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    music_profile: Mapped[str | None] = mapped_column(String(120))
    estimated_duration_seconds: Mapped[int | None] = mapped_column(Integer)
    current_segment_index: Mapped[int | None] = mapped_column(Integer)
    attempt_count: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    stop_reason: Mapped[str | None] = mapped_column(String(255))
    error_message: Mapped[str | None] = mapped_column(Text)
    config_json: Mapped[dict[str, Any] | list[Any] | None] = mapped_column(JSON)
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    session: Mapped["StorySession"] = relationship(back_populates="audio_jobs")
    source_composition_job: Mapped["CompositionJob | None"] = relationship()
    export_assets: Mapped[list["ExportAsset"]] = relationship(back_populates="audio_job")

    __table_args__ = (
        Index("ix_audio_jobs_session_id_status_created_at", "session_id", "status", "created_at"),
    )


class ExportAsset(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "export_assets"

    session_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("story_sessions.id", ondelete="CASCADE"),
        nullable=False,
    )
    composition_job_id: Mapped[str | None] = mapped_column(
        String(36),
        ForeignKey("composition_jobs.id", ondelete="SET NULL"),
    )
    audio_job_id: Mapped[str | None] = mapped_column(
        String(36),
        ForeignKey("audio_jobs.id", ondelete="SET NULL"),
    )
    asset_kind: Mapped[AssetKind] = mapped_column(ASSET_KIND_ENUM, nullable=False)
    status: Mapped[AssetStatus] = mapped_column(
        ASSET_STATUS_ENUM,
        nullable=False,
        default=AssetStatus.PENDING,
    )
    storage_bucket: Mapped[str] = mapped_column(String(120), nullable=False)
    storage_key: Mapped[str] = mapped_column(String(255), nullable=False)
    mime_type: Mapped[str] = mapped_column(String(120), nullable=False)
    byte_size: Mapped[int | None] = mapped_column(Integer)
    checksum_sha256: Mapped[str | None] = mapped_column(String(64))
    metadata_json: Mapped[dict[str, Any] | list[Any] | None] = mapped_column(JSON)
    ready_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    superseded_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    session: Mapped["StorySession"] = relationship(back_populates="export_assets")
    composition_job: Mapped["CompositionJob | None"] = relationship(back_populates="export_assets")
    audio_job: Mapped["AudioJob | None"] = relationship(back_populates="export_assets")

    __table_args__ = (
        UniqueConstraint(
            "storage_bucket", "storage_key", name="uq_export_assets_storage_bucket_storage_key"
        ),
        Index(
            "ix_export_assets_session_id_asset_kind_status", "session_id", "asset_kind", "status"
        ),
    )
