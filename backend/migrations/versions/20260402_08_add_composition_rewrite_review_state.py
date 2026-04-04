"""Add rewrite review and downstream stale state for composition segments.

Revision ID: 20260402_08_comp_rewrite_review
Revises: 20260402_07_comp_interrupts
Create Date: 2026-04-02 22:15:00.000000
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op

revision = "20260402_08_comp_rewrite_review"
down_revision = "20260402_07_comp_interrupts"
branch_labels = None
depends_on = None


def upgrade() -> None:
    dialect_name = op.get_bind().dialect.name

    op.add_column(
        "composition_jobs",
        sa.Column("rewrite_to_segment_index", sa.Integer(), nullable=True),
    )
    op.add_column(
        "composition_jobs",
        sa.Column(
            "downstream_regeneration_mode",
            sa.String(length=20),
            nullable=False,
            server_default="none",
        ),
    )
    op.add_column(
        "composition_jobs",
        sa.Column("stale_from_segment_index", sa.Integer(), nullable=True),
    )
    op.add_column(
        "composition_jobs",
        sa.Column("stale_to_segment_index", sa.Integer(), nullable=True),
    )

    op.add_column(
        "composition_segments",
        sa.Column(
            "acceptance_state",
            sa.String(length=8),
            nullable=False,
            server_default="accepted",
        ),
    )
    op.add_column(
        "composition_segments",
        sa.Column("is_stale", sa.Boolean(), nullable=False, server_default=sa.false()),
    )
    op.add_column(
        "composition_segments",
        sa.Column("stale_reason", sa.Text(), nullable=True),
    )
    op.add_column(
        "composition_segments",
        sa.Column("stale_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.add_column(
        "composition_segments",
        sa.Column("stale_by_job_id", sa.String(length=36), nullable=True),
    )
    with op.batch_alter_table("composition_segments") as batch_op:
        batch_op.create_foreign_key(
            "fk_comp_segments_stale_by_job",
            "composition_jobs",
            ["stale_by_job_id"],
            ["id"],
            ondelete="SET NULL",
        )
    op.create_index(
        "ix_composition_segments_session_id_acceptance_state",
        "composition_segments",
        ["session_id", "acceptance_state"],
        unique=False,
    )
    op.create_index(
        "ix_composition_segments_session_id_is_stale",
        "composition_segments",
        ["session_id", "is_stale"],
        unique=False,
    )

    op.execute(
        sa.text(
            """
            UPDATE composition_jobs
            SET downstream_regeneration_mode = 'none'
            WHERE downstream_regeneration_mode IS NULL
            """
        )
    )
    op.execute(
        sa.text(
            """
            UPDATE composition_segments
            SET acceptance_state = 'accepted', is_stale = FALSE
            WHERE acceptance_state IS NULL
            """
        )
    )

    if dialect_name != "sqlite":
        op.alter_column(
            "composition_jobs",
            "downstream_regeneration_mode",
            server_default=None,
        )
        op.alter_column(
            "composition_segments",
            "acceptance_state",
            server_default=None,
        )
        op.alter_column(
            "composition_segments",
            "is_stale",
            server_default=None,
        )


def downgrade() -> None:
    op.drop_index(
        "ix_composition_segments_session_id_is_stale",
        table_name="composition_segments",
    )
    op.drop_index(
        "ix_composition_segments_session_id_acceptance_state",
        table_name="composition_segments",
    )
    with op.batch_alter_table("composition_segments") as batch_op:
        batch_op.drop_constraint(
            "fk_comp_segments_stale_by_job",
            type_="foreignkey",
        )
    op.drop_column("composition_segments", "stale_by_job_id")
    op.drop_column("composition_segments", "stale_at")
    op.drop_column("composition_segments", "stale_reason")
    op.drop_column("composition_segments", "is_stale")
    op.drop_column("composition_segments", "acceptance_state")
    op.drop_column("composition_jobs", "stale_to_segment_index")
    op.drop_column("composition_jobs", "stale_from_segment_index")
    op.drop_column("composition_jobs", "downstream_regeneration_mode")
    op.drop_column("composition_jobs", "rewrite_to_segment_index")
