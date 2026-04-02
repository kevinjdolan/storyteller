"""Add durable continuity bibles.

Revision ID: 20260402_03_continuity_bibles
Revises: 20260402_02_story_outlines
Create Date: 2026-04-02 15:05:00.000000
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op


revision = "20260402_03_continuity_bibles"
down_revision = "20260402_02_story_outlines"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "continuity_bibles",
        sa.Column("session_id", sa.String(length=36), nullable=False),
        sa.Column("revision_number", sa.Integer(), nullable=False),
        sa.Column("source_stage", sa.String(length=32), nullable=True),
        sa.Column("source_summary", sa.Text(), nullable=True),
        sa.Column("summary_text", sa.Text(), nullable=False),
        sa.Column("summary_data", sa.JSON(), nullable=False),
        sa.Column("is_selected", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["session_id"], ["story_sessions.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "session_id",
            "revision_number",
            name="uq_continuity_bibles_session_id_revision_number",
        ),
    )
    op.create_index(
        "ix_continuity_bibles_session_id_is_selected",
        "continuity_bibles",
        ["session_id", "is_selected"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(
        "ix_continuity_bibles_session_id_is_selected",
        table_name="continuity_bibles",
    )
    op.drop_table("continuity_bibles")
