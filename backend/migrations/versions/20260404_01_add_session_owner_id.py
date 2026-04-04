"""add durable session owner ids for local identity

Revision ID: 20260404_01_owner_id
Revises: 20260402_10_narration_segments
Create Date: 2026-04-04 10:15:00.000000
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op

revision = "20260404_01_owner_id"
down_revision = "20260402_10_narration_segments"
branch_labels = None
depends_on = None

LOCAL_DEVELOPMENT_OWNER_ID = "local-user"


def upgrade() -> None:
    dialect_name = op.get_bind().dialect.name

    op.add_column(
        "story_sessions",
        sa.Column(
            "owner_id",
            sa.String(length=120),
            nullable=False,
            server_default=LOCAL_DEVELOPMENT_OWNER_ID,
        ),
    )
    op.create_index(
        "ix_story_sessions_owner_id_updated_at",
        "story_sessions",
        ["owner_id", "updated_at"],
        unique=False,
    )

    op.execute(
        sa.text(
            """
            UPDATE story_sessions
            SET owner_id = :owner_id
            WHERE owner_id IS NULL OR owner_id = ''
            """
        ).bindparams(owner_id=LOCAL_DEVELOPMENT_OWNER_ID)
    )

    if dialect_name != "sqlite":
        op.alter_column("story_sessions", "owner_id", server_default=None)


def downgrade() -> None:
    op.drop_index("ix_story_sessions_owner_id_updated_at", table_name="story_sessions")
    op.drop_column("story_sessions", "owner_id")
