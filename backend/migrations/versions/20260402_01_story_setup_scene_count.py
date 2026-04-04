"""Add approximate scene count to story setups.

Revision ID: 20260402_01_story_setup_scene_count
Revises: 20260401_04
Create Date: 2026-04-02 10:00:00.000000
"""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa


revision = "20260402_01_story_setup_scenes"
down_revision = "20260401_04"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "story_setups",
        sa.Column("approximate_scene_count", sa.Integer(), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("story_setups", "approximate_scene_count")
