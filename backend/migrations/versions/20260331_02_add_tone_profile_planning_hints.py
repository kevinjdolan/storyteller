"""add default planning hints to tone profiles

Revision ID: 20260331_02
Revises: 20260331_01
Create Date: 2026-03-31 23:25:00.000000
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "20260331_02"
down_revision = "20260331_01"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "tone_profiles",
        sa.Column("default_planning_hints", sa.JSON(), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("tone_profiles", "default_planning_hints")
