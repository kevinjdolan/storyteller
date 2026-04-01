"""add durable session memory snapshots

Revision ID: 20260401_02
Revises: 20260401_01
Create Date: 2026-04-01 12:15:00.000000
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "20260401_02"
down_revision = "20260401_01"
branch_labels = None
depends_on = None


def timestamp_column(name: str, *, nullable: bool = False) -> sa.Column:
    return sa.Column(
        name,
        sa.DateTime(timezone=True),
        nullable=nullable,
        server_default=sa.text("CURRENT_TIMESTAMP") if not nullable else None,
    )


def upgrade() -> None:
    op.create_table(
        "session_memory_snapshots",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("session_id", sa.String(length=36), nullable=False),
        sa.Column("trigger_event_id", sa.String(length=36), nullable=True),
        sa.Column("trigger_event_type", sa.String(length=120), nullable=True),
        sa.Column("trigger_event_sequence_number", sa.Integer(), nullable=True),
        sa.Column("summary_text", sa.Text(), nullable=False),
        sa.Column("summary_data", sa.JSON(), nullable=False),
        timestamp_column("created_at"),
        sa.ForeignKeyConstraint(
            ["session_id"],
            ["story_sessions.id"],
            name="fk_session_memory_snapshots_session_id_story_sessions",
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["trigger_event_id"],
            ["event_log_entries.id"],
            name="fk_session_memory_snapshots_trigger_event_id_event_log_entries",
            ondelete="SET NULL",
        ),
        sa.PrimaryKeyConstraint("id", name="pk_session_memory_snapshots"),
        sa.UniqueConstraint(
            "trigger_event_id",
            name="uq_session_memory_snapshots_trigger_event_id",
        ),
    )
    op.create_index(
        "ix_session_memory_snapshots_session_id_created_at",
        "session_memory_snapshots",
        ["session_id", "created_at"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(
        "ix_session_memory_snapshots_session_id_created_at",
        table_name="session_memory_snapshots",
    )
    op.drop_table("session_memory_snapshots")
