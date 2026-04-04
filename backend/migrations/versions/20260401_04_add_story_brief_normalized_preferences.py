"""add structured normalized preferences to story briefs

Revision ID: 20260401_04
Revises: 20260401_03
Create Date: 2026-04-01 20:40:00.000000
"""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa


revision = "20260401_04"
down_revision = "20260401_03"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("story_briefs", sa.Column("normalized_preferences", sa.JSON(), nullable=True))


def downgrade() -> None:
    op.drop_column("story_briefs", "normalized_preferences")
