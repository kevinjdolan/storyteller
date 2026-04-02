"""Add durable narration segments for resumable audio generation.

Revision ID: 20260402_10_narration_segments
Revises: 20260402_09_audio_settings
Create Date: 2026-04-02 11:05:00.000000
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op

revision = "20260402_10_narration_segments"
down_revision = "20260402_09_audio_settings"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "narration_segments",
        sa.Column("session_id", sa.String(length=36), nullable=False),
        sa.Column("audio_job_id", sa.String(length=36), nullable=False),
        sa.Column("source_composition_segment_id", sa.String(length=36), nullable=True),
        sa.Column("segment_index", sa.Integer(), nullable=False),
        sa.Column("status", sa.String(length=11), nullable=False, server_default="queued"),
        sa.Column("source_boundary_kind", sa.String(length=7), nullable=False),
        sa.Column("source_outline_card_key", sa.String(length=160), nullable=True),
        sa.Column("source_outline_card_title", sa.String(length=255), nullable=True),
        sa.Column("text_content", sa.Text(), nullable=False),
        sa.Column("word_count", sa.Integer(), nullable=False),
        sa.Column("text_start_offset", sa.Integer(), nullable=False),
        sa.Column("text_end_offset", sa.Integer(), nullable=False),
        sa.Column("pause_after_seconds", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("pause_hint", sa.String(length=13), nullable=False, server_default="none"),
        sa.Column(
            "music_transition_hint",
            sa.String(length=12),
            nullable=False,
            server_default="continue_bed",
        ),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.Column("metadata_json", sa.JSON(), nullable=True),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["audio_job_id"], ["audio_jobs.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(
            ["source_composition_segment_id"],
            ["composition_segments.id"],
            ondelete="SET NULL",
        ),
        sa.ForeignKeyConstraint(["session_id"], ["story_sessions.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "audio_job_id",
            "segment_index",
            name="uq_narration_segments_audio_job_segment",
        ),
    )
    op.create_index(
        "ix_narration_segments_audio_job_id_status",
        "narration_segments",
        ["audio_job_id", "status"],
        unique=False,
    )
    op.create_index(
        "ix_narration_segments_session_id_status",
        "narration_segments",
        ["session_id", "status"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(
        "ix_narration_segments_session_id_status",
        table_name="narration_segments",
    )
    op.drop_index(
        "ix_narration_segments_audio_job_id_status",
        table_name="narration_segments",
    )
    op.drop_table("narration_segments")
