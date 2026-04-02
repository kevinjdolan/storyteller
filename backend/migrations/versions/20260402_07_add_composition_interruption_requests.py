"""Add durable composition interruption requests.

Revision ID: 20260402_07_comp_interrupts
Revises: 20260402_06_segmented_writing
Create Date: 2026-04-02 20:30:00.000000
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op

revision = "20260402_07_comp_interrupts"
down_revision = "20260402_06_segmented_writing"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "composition_interruption_requests",
        sa.Column("session_id", sa.String(length=36), nullable=False),
        sa.Column("composition_job_id", sa.String(length=36), nullable=False),
        sa.Column("request_kind", sa.String(length=8), nullable=False),
        sa.Column("state", sa.String(length=10), nullable=False),
        sa.Column("origin", sa.String(length=64), nullable=False),
        sa.Column("instructions", sa.Text(), nullable=True),
        sa.Column("rewrite_from_segment_index", sa.Integer(), nullable=True),
        sa.Column("requested_status", sa.String(length=11), nullable=True),
        sa.Column("requested_segment_id", sa.String(length=36), nullable=True),
        sa.Column("requested_segment_index", sa.Integer(), nullable=True),
        sa.Column("requested_progress_percent", sa.Numeric(5, 2), nullable=True),
        sa.Column("resolution_summary", sa.Text(), nullable=True),
        sa.Column("metadata_json", sa.JSON(), nullable=True),
        sa.Column("resolved_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(
            ["composition_job_id"],
            ["composition_jobs.id"],
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["requested_segment_id"],
            ["composition_segments.id"],
            ondelete="SET NULL",
        ),
        sa.ForeignKeyConstraint(
            ["session_id"],
            ["story_sessions.id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_comp_interruptions_job_state_created_at",
        "composition_interruption_requests",
        ["composition_job_id", "state", "created_at"],
        unique=False,
    )
    op.create_index(
        "ix_comp_interruptions_session_state_created_at",
        "composition_interruption_requests",
        ["session_id", "state", "created_at"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(
        "ix_comp_interruptions_session_state_created_at",
        table_name="composition_interruption_requests",
    )
    op.drop_index(
        "ix_comp_interruptions_job_state_created_at",
        table_name="composition_interruption_requests",
    )
    op.drop_table("composition_interruption_requests")
