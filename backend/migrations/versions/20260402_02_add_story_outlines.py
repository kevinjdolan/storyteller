"""Add story outlines for drill-down planning.

Revision ID: 20260402_02_story_outlines
Revises: 20260402_01_story_setup_scenes
Create Date: 2026-04-02 12:30:00.000000
"""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa


revision = "20260402_02_story_outlines"
down_revision = "20260402_01_story_setup_scenes"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "story_outlines",
        sa.Column("session_id", sa.String(length=36), nullable=False),
        sa.Column("beat_sheet_id", sa.String(length=36), nullable=True),
        sa.Column("story_setup_id", sa.String(length=36), nullable=True),
        sa.Column("revision_number", sa.Integer(), nullable=False),
        sa.Column("outline_kind", sa.String(length=32), nullable=False),
        sa.Column("summary", sa.Text(), nullable=True),
        sa.Column("cards", sa.JSON(), nullable=True),
        sa.Column("metadata_json", sa.JSON(), nullable=True),
        sa.Column("is_selected", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("accepted_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["beat_sheet_id"], ["beat_sheets.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["session_id"], ["story_sessions.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["story_setup_id"], ["story_setups.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "session_id",
            "revision_number",
            name="uq_story_outlines_session_id_revision_number",
        ),
    )
    op.create_index(
        "ix_story_outlines_session_id_is_selected",
        "story_outlines",
        ["session_id", "is_selected"],
        unique=False,
    )
    op.create_index(
        "ix_story_outlines_story_setup_id",
        "story_outlines",
        ["story_setup_id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index("ix_story_outlines_story_setup_id", table_name="story_outlines")
    op.drop_index("ix_story_outlines_session_id_is_selected", table_name="story_outlines")
    op.drop_table("story_outlines")
