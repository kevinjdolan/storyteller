"""create the initial storyteller relational schema

Revision ID: 20260331_01
Revises:
Create Date: 2026-03-31 22:30:00.000000
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "20260331_01"
down_revision = None
branch_labels = None
depends_on = None


WORKFLOW_STAGE_VALUES = (
    "genre",
    "tone",
    "brief",
    "pitches",
    "characters",
    "beats",
    "story_setup",
    "composition",
    "audio",
    "finalize",
)
WORKFLOW_STAGE_STATE_VALUES = (
    "draft",
    "in_progress",
    "completed",
    "needs_regeneration",
)
JOB_STATUS_VALUES = (
    "queued",
    "in_progress",
    "paused",
    "completed",
    "failed",
    "cancelled",
)
COMPOSITION_JOB_KIND_VALUES = ("draft", "rewrite")
ASSET_KIND_VALUES = ("story_text", "story_docx", "audio_segment", "final_audio")
ASSET_STATUS_VALUES = ("pending", "ready", "failed", "superseded")
EVENT_ACTOR_TYPE_VALUES = ("user", "assistant", "system", "service")


def workflow_stage_enum() -> sa.Enum:
    return sa.Enum(*WORKFLOW_STAGE_VALUES, name="workflow_stage", native_enum=False)


def workflow_stage_state_enum() -> sa.Enum:
    return sa.Enum(
        *WORKFLOW_STAGE_STATE_VALUES,
        name="workflow_stage_state",
        native_enum=False,
    )


def job_status_enum() -> sa.Enum:
    return sa.Enum(*JOB_STATUS_VALUES, name="job_status", native_enum=False)


def composition_job_kind_enum() -> sa.Enum:
    return sa.Enum(
        *COMPOSITION_JOB_KIND_VALUES,
        name="composition_job_kind",
        native_enum=False,
    )


def asset_kind_enum() -> sa.Enum:
    return sa.Enum(*ASSET_KIND_VALUES, name="asset_kind", native_enum=False)


def asset_status_enum() -> sa.Enum:
    return sa.Enum(*ASSET_STATUS_VALUES, name="asset_status", native_enum=False)


def event_actor_type_enum() -> sa.Enum:
    return sa.Enum(*EVENT_ACTOR_TYPE_VALUES, name="event_actor_type", native_enum=False)


def timestamp_column(name: str, *, nullable: bool = False) -> sa.Column:
    return sa.Column(
        name,
        sa.DateTime(timezone=True),
        nullable=nullable,
        server_default=sa.text("CURRENT_TIMESTAMP") if not nullable else None,
    )


def upgrade() -> None:
    op.create_table(
        "genres",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("slug", sa.String(length=80), nullable=False),
        sa.Column("label", sa.String(length=120), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("bedtime_safety_notes", sa.Text(), nullable=True),
        sa.Column("arc_notes", sa.JSON(), nullable=True),
        sa.Column("sort_order", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        timestamp_column("created_at"),
        timestamp_column("updated_at"),
        sa.PrimaryKeyConstraint("id", name="pk_genres"),
        sa.UniqueConstraint("slug", name="uq_genres_slug"),
    )
    op.create_index("ix_genres_sort_order", "genres", ["sort_order"], unique=False)
    op.create_index("ix_genres_is_active", "genres", ["is_active"], unique=False)

    op.create_table(
        "tone_profiles",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("genre_id", sa.String(length=36), nullable=False),
        sa.Column("slug", sa.String(length=80), nullable=False),
        sa.Column("label", sa.String(length=120), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("bedtime_notes", sa.Text(), nullable=True),
        sa.Column("descriptors", sa.JSON(), nullable=True),
        sa.Column("sort_order", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        timestamp_column("created_at"),
        timestamp_column("updated_at"),
        sa.ForeignKeyConstraint(
            ["genre_id"],
            ["genres.id"],
            name="fk_tone_profiles_genre_id_genres",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name="pk_tone_profiles"),
        sa.UniqueConstraint("genre_id", "slug", name="uq_tone_profiles_genre_id_slug"),
    )
    op.create_index(
        "ix_tone_profiles_genre_id_sort_order",
        "tone_profiles",
        ["genre_id", "sort_order"],
        unique=False,
    )
    op.create_index(
        "ix_tone_profiles_genre_id_is_active",
        "tone_profiles",
        ["genre_id", "is_active"],
        unique=False,
    )

    op.create_table(
        "story_sessions",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("working_title", sa.String(length=255), nullable=True),
        sa.Column("current_stage", workflow_stage_enum(), nullable=False, server_default="genre"),
        sa.Column("resume_stage", workflow_stage_enum(), nullable=False, server_default="genre"),
        sa.Column("furthest_completed_stage", workflow_stage_enum(), nullable=True),
        sa.Column(
            "overall_status",
            workflow_stage_state_enum(),
            nullable=False,
            server_default="draft",
        ),
        sa.Column("selected_genre_id", sa.String(length=36), nullable=True),
        sa.Column("selected_tone_profile_id", sa.String(length=36), nullable=True),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        timestamp_column("created_at"),
        timestamp_column("updated_at"),
        sa.ForeignKeyConstraint(
            ["selected_genre_id"],
            ["genres.id"],
            name="fk_story_sessions_selected_genre_id_genres",
            ondelete="SET NULL",
        ),
        sa.ForeignKeyConstraint(
            ["selected_tone_profile_id"],
            ["tone_profiles.id"],
            name="fk_story_sessions_selected_tone_profile_id_tone_profiles",
            ondelete="SET NULL",
        ),
        sa.PrimaryKeyConstraint("id", name="pk_story_sessions"),
    )
    op.create_index(
        "ix_story_sessions_overall_status_updated_at",
        "story_sessions",
        ["overall_status", "updated_at"],
        unique=False,
    )
    op.create_index(
        "ix_story_sessions_resume_stage",
        "story_sessions",
        ["resume_stage"],
        unique=False,
    )
    op.create_index(
        "ix_story_sessions_current_stage",
        "story_sessions",
        ["current_stage"],
        unique=False,
    )
    op.create_index(
        "ix_story_sessions_selected_genre_id",
        "story_sessions",
        ["selected_genre_id"],
        unique=False,
    )

    op.create_table(
        "event_log_entries",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("session_id", sa.String(length=36), nullable=False),
        sa.Column("sequence_number", sa.Integer(), nullable=False),
        sa.Column("actor_type", event_actor_type_enum(), nullable=False),
        sa.Column("actor_id", sa.String(length=120), nullable=True),
        sa.Column("event_type", sa.String(length=120), nullable=False),
        sa.Column("stage", workflow_stage_enum(), nullable=True),
        sa.Column("summary", sa.Text(), nullable=False),
        sa.Column("payload", sa.JSON(), nullable=True),
        timestamp_column("created_at"),
        sa.ForeignKeyConstraint(
            ["session_id"],
            ["story_sessions.id"],
            name="fk_event_log_entries_session_id_story_sessions",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name="pk_event_log_entries"),
        sa.UniqueConstraint(
            "session_id",
            "sequence_number",
            name="uq_event_log_entries_session_id_sequence_number",
        ),
    )
    op.create_index(
        "ix_event_log_entries_session_id_created_at",
        "event_log_entries",
        ["session_id", "created_at"],
        unique=False,
    )
    op.create_index(
        "ix_event_log_entries_session_id_stage",
        "event_log_entries",
        ["session_id", "stage"],
        unique=False,
    )

    op.create_table(
        "workflow_stage_states",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("session_id", sa.String(length=36), nullable=False),
        sa.Column("stage", workflow_stage_enum(), nullable=False),
        sa.Column(
            "status",
            workflow_stage_state_enum(),
            nullable=False,
            server_default="draft",
        ),
        sa.Column("detail", sa.Text(), nullable=True),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("last_event_id", sa.String(length=36), nullable=True),
        timestamp_column("created_at"),
        timestamp_column("updated_at"),
        sa.ForeignKeyConstraint(
            ["last_event_id"],
            ["event_log_entries.id"],
            name="fk_workflow_stage_states_last_event_id_event_log_entries",
            ondelete="SET NULL",
        ),
        sa.ForeignKeyConstraint(
            ["session_id"],
            ["story_sessions.id"],
            name="fk_workflow_stage_states_session_id_story_sessions",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name="pk_workflow_stage_states"),
        sa.UniqueConstraint(
            "session_id",
            "stage",
            name="uq_workflow_stage_states_session_id_stage",
        ),
    )
    op.create_index(
        "ix_workflow_stage_states_session_id_status",
        "workflow_stage_states",
        ["session_id", "status"],
        unique=False,
    )

    op.create_table(
        "story_briefs",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("session_id", sa.String(length=36), nullable=False),
        sa.Column("revision_number", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("raw_brief", sa.Text(), nullable=False),
        sa.Column("normalized_summary", sa.Text(), nullable=True),
        sa.Column("planning_notes", sa.Text(), nullable=True),
        sa.Column("model_output", sa.JSON(), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("accepted_at", sa.DateTime(timezone=True), nullable=True),
        timestamp_column("created_at"),
        timestamp_column("updated_at"),
        sa.ForeignKeyConstraint(
            ["session_id"],
            ["story_sessions.id"],
            name="fk_story_briefs_session_id_story_sessions",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name="pk_story_briefs"),
        sa.UniqueConstraint(
            "session_id",
            "revision_number",
            name="uq_story_briefs_session_id_revision_number",
        ),
    )
    op.create_index(
        "ix_story_briefs_session_id_is_active",
        "story_briefs",
        ["session_id", "is_active"],
        unique=False,
    )

    op.create_table(
        "pitches",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("session_id", sa.String(length=36), nullable=False),
        sa.Column("story_brief_id", sa.String(length=36), nullable=True),
        sa.Column("generation_key", sa.String(length=80), nullable=False),
        sa.Column("pitch_index", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("logline", sa.Text(), nullable=False),
        sa.Column("summary", sa.Text(), nullable=True),
        sa.Column("bedtime_notes", sa.Text(), nullable=True),
        sa.Column("model_output", sa.JSON(), nullable=True),
        sa.Column("is_selected", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("accepted_at", sa.DateTime(timezone=True), nullable=True),
        timestamp_column("created_at"),
        timestamp_column("updated_at"),
        sa.ForeignKeyConstraint(
            ["session_id"],
            ["story_sessions.id"],
            name="fk_pitches_session_id_story_sessions",
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["story_brief_id"],
            ["story_briefs.id"],
            name="fk_pitches_story_brief_id_story_briefs",
            ondelete="SET NULL",
        ),
        sa.PrimaryKeyConstraint("id", name="pk_pitches"),
        sa.UniqueConstraint(
            "session_id",
            "generation_key",
            "pitch_index",
            name="uq_pitches_session_id_generation_key_pitch_index",
        ),
    )
    op.create_index(
        "ix_pitches_session_id_is_selected",
        "pitches",
        ["session_id", "is_selected"],
        unique=False,
    )

    op.create_table(
        "character_sheets",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("session_id", sa.String(length=36), nullable=False),
        sa.Column("pitch_id", sa.String(length=36), nullable=True),
        sa.Column("revision_number", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("title", sa.String(length=255), nullable=True),
        sa.Column("summary", sa.Text(), nullable=True),
        sa.Column("protagonist_name", sa.String(length=120), nullable=True),
        sa.Column("supporting_cast", sa.JSON(), nullable=True),
        sa.Column("character_data", sa.JSON(), nullable=True),
        sa.Column("bedtime_notes", sa.Text(), nullable=True),
        sa.Column("is_selected", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("accepted_at", sa.DateTime(timezone=True), nullable=True),
        timestamp_column("created_at"),
        timestamp_column("updated_at"),
        sa.ForeignKeyConstraint(
            ["pitch_id"],
            ["pitches.id"],
            name="fk_character_sheets_pitch_id_pitches",
            ondelete="SET NULL",
        ),
        sa.ForeignKeyConstraint(
            ["session_id"],
            ["story_sessions.id"],
            name="fk_character_sheets_session_id_story_sessions",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name="pk_character_sheets"),
        sa.UniqueConstraint(
            "session_id",
            "revision_number",
            name="uq_character_sheets_session_id_revision_number",
        ),
    )
    op.create_index(
        "ix_character_sheets_session_id_is_selected",
        "character_sheets",
        ["session_id", "is_selected"],
        unique=False,
    )

    op.create_table(
        "beat_sheets",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("session_id", sa.String(length=36), nullable=False),
        sa.Column("character_sheet_id", sa.String(length=36), nullable=True),
        sa.Column("revision_number", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("summary", sa.Text(), nullable=True),
        sa.Column("beats", sa.JSON(), nullable=True),
        sa.Column("bedtime_notes", sa.Text(), nullable=True),
        sa.Column("is_selected", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("accepted_at", sa.DateTime(timezone=True), nullable=True),
        timestamp_column("created_at"),
        timestamp_column("updated_at"),
        sa.ForeignKeyConstraint(
            ["character_sheet_id"],
            ["character_sheets.id"],
            name="fk_beat_sheets_character_sheet_id_character_sheets",
            ondelete="SET NULL",
        ),
        sa.ForeignKeyConstraint(
            ["session_id"],
            ["story_sessions.id"],
            name="fk_beat_sheets_session_id_story_sessions",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name="pk_beat_sheets"),
        sa.UniqueConstraint(
            "session_id",
            "revision_number",
            name="uq_beat_sheets_session_id_revision_number",
        ),
    )
    op.create_index(
        "ix_beat_sheets_session_id_is_selected",
        "beat_sheets",
        ["session_id", "is_selected"],
        unique=False,
    )

    op.create_table(
        "story_setups",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("session_id", sa.String(length=36), nullable=False),
        sa.Column("beat_sheet_id", sa.String(length=36), nullable=True),
        sa.Column("revision_number", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("target_word_count", sa.Integer(), nullable=True),
        sa.Column("target_runtime_minutes", sa.Integer(), nullable=True),
        sa.Column("chapter_count", sa.Integer(), nullable=True),
        sa.Column("chapter_style", sa.String(length=120), nullable=True),
        sa.Column("guidance_notes", sa.Text(), nullable=True),
        sa.Column("preferences", sa.JSON(), nullable=True),
        sa.Column("is_selected", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("accepted_at", sa.DateTime(timezone=True), nullable=True),
        timestamp_column("created_at"),
        timestamp_column("updated_at"),
        sa.ForeignKeyConstraint(
            ["beat_sheet_id"],
            ["beat_sheets.id"],
            name="fk_story_setups_beat_sheet_id_beat_sheets",
            ondelete="SET NULL",
        ),
        sa.ForeignKeyConstraint(
            ["session_id"],
            ["story_sessions.id"],
            name="fk_story_setups_session_id_story_sessions",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name="pk_story_setups"),
        sa.UniqueConstraint(
            "session_id",
            "revision_number",
            name="uq_story_setups_session_id_revision_number",
        ),
    )
    op.create_index(
        "ix_story_setups_session_id_is_selected",
        "story_setups",
        ["session_id", "is_selected"],
        unique=False,
    )

    op.create_table(
        "composition_jobs",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("session_id", sa.String(length=36), nullable=False),
        sa.Column("beat_sheet_id", sa.String(length=36), nullable=True),
        sa.Column("story_setup_id", sa.String(length=36), nullable=True),
        sa.Column(
            "job_kind",
            composition_job_kind_enum(),
            nullable=False,
            server_default="draft",
        ),
        sa.Column("status", job_status_enum(), nullable=False, server_default="queued"),
        sa.Column(
            "progress_percent",
            sa.Numeric(5, 2, asdecimal=False),
            nullable=False,
            server_default="0",
        ),
        sa.Column("current_segment_index", sa.Integer(), nullable=True),
        sa.Column("attempt_count", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("stop_reason", sa.String(length=255), nullable=True),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.Column("metadata_json", sa.JSON(), nullable=True),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        timestamp_column("created_at"),
        timestamp_column("updated_at"),
        sa.ForeignKeyConstraint(
            ["beat_sheet_id"],
            ["beat_sheets.id"],
            name="fk_composition_jobs_beat_sheet_id_beat_sheets",
            ondelete="SET NULL",
        ),
        sa.ForeignKeyConstraint(
            ["session_id"],
            ["story_sessions.id"],
            name="fk_composition_jobs_session_id_story_sessions",
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["story_setup_id"],
            ["story_setups.id"],
            name="fk_composition_jobs_story_setup_id_story_setups",
            ondelete="SET NULL",
        ),
        sa.PrimaryKeyConstraint("id", name="pk_composition_jobs"),
    )
    op.create_index(
        "ix_composition_jobs_session_id_status_created_at",
        "composition_jobs",
        ["session_id", "status", "created_at"],
        unique=False,
    )
    op.create_index(
        "ix_composition_jobs_session_id_job_kind",
        "composition_jobs",
        ["session_id", "job_kind"],
        unique=False,
    )

    op.create_table(
        "composition_segments",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("session_id", sa.String(length=36), nullable=False),
        sa.Column("composition_job_id", sa.String(length=36), nullable=False),
        sa.Column("superseded_by_segment_id", sa.String(length=36), nullable=True),
        sa.Column("segment_index", sa.Integer(), nullable=False),
        sa.Column("revision_number", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("status", job_status_enum(), nullable=False, server_default="queued"),
        sa.Column("planned_summary", sa.Text(), nullable=True),
        sa.Column("text_content", sa.Text(), nullable=True),
        sa.Column("word_count", sa.Integer(), nullable=True),
        sa.Column("payload", sa.JSON(), nullable=True),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        timestamp_column("created_at"),
        timestamp_column("updated_at"),
        sa.ForeignKeyConstraint(
            ["composition_job_id"],
            ["composition_jobs.id"],
            name="fk_composition_segments_composition_job_id_composition_jobs",
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["session_id"],
            ["story_sessions.id"],
            name="fk_composition_segments_session_id_story_sessions",
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["superseded_by_segment_id"],
            ["composition_segments.id"],
            name="fk_comp_segments_superseded_by",
            ondelete="SET NULL",
        ),
        sa.PrimaryKeyConstraint("id", name="pk_composition_segments"),
        sa.UniqueConstraint(
            "composition_job_id",
            "segment_index",
            "revision_number",
            name="uq_composition_segments_job_segment_revision",
        ),
    )
    op.create_index(
        "ix_composition_segments_session_id_status",
        "composition_segments",
        ["session_id", "status"],
        unique=False,
    )

    op.create_table(
        "audio_jobs",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("session_id", sa.String(length=36), nullable=False),
        sa.Column("source_composition_job_id", sa.String(length=36), nullable=True),
        sa.Column("status", job_status_enum(), nullable=False, server_default="queued"),
        sa.Column("voice_key", sa.String(length=120), nullable=True),
        sa.Column(
            "playback_speed",
            sa.Numeric(4, 2, asdecimal=False),
            nullable=False,
            server_default="1.0",
        ),
        sa.Column(
            "include_background_music",
            sa.Boolean(),
            nullable=False,
            server_default=sa.false(),
        ),
        sa.Column("music_profile", sa.String(length=120), nullable=True),
        sa.Column("estimated_duration_seconds", sa.Integer(), nullable=True),
        sa.Column("current_segment_index", sa.Integer(), nullable=True),
        sa.Column("attempt_count", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("stop_reason", sa.String(length=255), nullable=True),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.Column("config_json", sa.JSON(), nullable=True),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        timestamp_column("created_at"),
        timestamp_column("updated_at"),
        sa.ForeignKeyConstraint(
            ["session_id"],
            ["story_sessions.id"],
            name="fk_audio_jobs_session_id_story_sessions",
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["source_composition_job_id"],
            ["composition_jobs.id"],
            name="fk_audio_jobs_source_composition_job_id_composition_jobs",
            ondelete="SET NULL",
        ),
        sa.PrimaryKeyConstraint("id", name="pk_audio_jobs"),
    )
    op.create_index(
        "ix_audio_jobs_session_id_status_created_at",
        "audio_jobs",
        ["session_id", "status", "created_at"],
        unique=False,
    )

    op.create_table(
        "export_assets",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("session_id", sa.String(length=36), nullable=False),
        sa.Column("composition_job_id", sa.String(length=36), nullable=True),
        sa.Column("audio_job_id", sa.String(length=36), nullable=True),
        sa.Column("asset_kind", asset_kind_enum(), nullable=False),
        sa.Column("status", asset_status_enum(), nullable=False, server_default="pending"),
        sa.Column("storage_bucket", sa.String(length=120), nullable=False),
        sa.Column("storage_key", sa.String(length=255), nullable=False),
        sa.Column("mime_type", sa.String(length=120), nullable=False),
        sa.Column("byte_size", sa.Integer(), nullable=True),
        sa.Column("checksum_sha256", sa.String(length=64), nullable=True),
        sa.Column("metadata_json", sa.JSON(), nullable=True),
        sa.Column("ready_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("superseded_at", sa.DateTime(timezone=True), nullable=True),
        timestamp_column("created_at"),
        timestamp_column("updated_at"),
        sa.ForeignKeyConstraint(
            ["audio_job_id"],
            ["audio_jobs.id"],
            name="fk_export_assets_audio_job_id_audio_jobs",
            ondelete="SET NULL",
        ),
        sa.ForeignKeyConstraint(
            ["composition_job_id"],
            ["composition_jobs.id"],
            name="fk_export_assets_composition_job_id_composition_jobs",
            ondelete="SET NULL",
        ),
        sa.ForeignKeyConstraint(
            ["session_id"],
            ["story_sessions.id"],
            name="fk_export_assets_session_id_story_sessions",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name="pk_export_assets"),
        sa.UniqueConstraint(
            "storage_bucket",
            "storage_key",
            name="uq_export_assets_storage_bucket_storage_key",
        ),
    )
    op.create_index(
        "ix_export_assets_session_id_asset_kind_status",
        "export_assets",
        ["session_id", "asset_kind", "status"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index("ix_export_assets_session_id_asset_kind_status", table_name="export_assets")
    op.drop_table("export_assets")

    op.drop_index("ix_audio_jobs_session_id_status_created_at", table_name="audio_jobs")
    op.drop_table("audio_jobs")

    op.drop_index("ix_composition_segments_session_id_status", table_name="composition_segments")
    op.drop_table("composition_segments")

    op.drop_index("ix_composition_jobs_session_id_job_kind", table_name="composition_jobs")
    op.drop_index(
        "ix_composition_jobs_session_id_status_created_at",
        table_name="composition_jobs",
    )
    op.drop_table("composition_jobs")

    op.drop_index("ix_story_setups_session_id_is_selected", table_name="story_setups")
    op.drop_table("story_setups")

    op.drop_index("ix_beat_sheets_session_id_is_selected", table_name="beat_sheets")
    op.drop_table("beat_sheets")

    op.drop_index(
        "ix_character_sheets_session_id_is_selected",
        table_name="character_sheets",
    )
    op.drop_table("character_sheets")

    op.drop_index("ix_pitches_session_id_is_selected", table_name="pitches")
    op.drop_table("pitches")

    op.drop_index("ix_story_briefs_session_id_is_active", table_name="story_briefs")
    op.drop_table("story_briefs")

    op.drop_index(
        "ix_workflow_stage_states_session_id_status",
        table_name="workflow_stage_states",
    )
    op.drop_table("workflow_stage_states")

    op.drop_index(
        "ix_event_log_entries_session_id_stage",
        table_name="event_log_entries",
    )
    op.drop_index(
        "ix_event_log_entries_session_id_created_at",
        table_name="event_log_entries",
    )
    op.drop_table("event_log_entries")

    op.drop_index("ix_story_sessions_selected_genre_id", table_name="story_sessions")
    op.drop_index("ix_story_sessions_current_stage", table_name="story_sessions")
    op.drop_index("ix_story_sessions_resume_stage", table_name="story_sessions")
    op.drop_index(
        "ix_story_sessions_overall_status_updated_at",
        table_name="story_sessions",
    )
    op.drop_table("story_sessions")

    op.drop_index(
        "ix_tone_profiles_genre_id_is_active",
        table_name="tone_profiles",
    )
    op.drop_index(
        "ix_tone_profiles_genre_id_sort_order",
        table_name="tone_profiles",
    )
    op.drop_table("tone_profiles")

    op.drop_index("ix_genres_is_active", table_name="genres")
    op.drop_index("ix_genres_sort_order", table_name="genres")
    op.drop_table("genres")
