"""add explicit prompt fields to story briefs

Revision ID: 20260401_03
Revises: 20260401_02
Create Date: 2026-04-01 20:05:00.000000
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "20260401_03"
down_revision = "20260401_02"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("story_briefs", sa.Column("story_idea", sa.Text(), nullable=True))
    op.add_column("story_briefs", sa.Column("desired_themes", sa.Text(), nullable=True))
    op.add_column("story_briefs", sa.Column("key_images", sa.Text(), nullable=True))
    op.add_column("story_briefs", sa.Column("audience_notes", sa.Text(), nullable=True))
    op.add_column("story_briefs", sa.Column("must_have_elements", sa.Text(), nullable=True))


def downgrade() -> None:
    op.drop_column("story_briefs", "must_have_elements")
    op.drop_column("story_briefs", "audience_notes")
    op.drop_column("story_briefs", "key_images")
    op.drop_column("story_briefs", "desired_themes")
    op.drop_column("story_briefs", "story_idea")
