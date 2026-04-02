"""Add plan revisions and composition lineage.

Revision ID: 20260402_04_plan_revisions
Revises: 20260402_03_continuity_bibles
Create Date: 2026-04-02 14:20:00.000000
"""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "20260402_04_plan_revisions"
down_revision = "20260402_03_continuity_bibles"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "plan_revisions",
        sa.Column("session_id", sa.String(length=36), nullable=False),
        sa.Column("revision_number", sa.Integer(), nullable=False),
        sa.Column("source_stage", sa.String(length=32), nullable=True),
        sa.Column("change_summary", sa.Text(), nullable=True),
        sa.Column("restored_from_plan_revision_id", sa.String(length=36), nullable=True),
        sa.Column("pitch_id", sa.String(length=36), nullable=True),
        sa.Column("character_sheet_id", sa.String(length=36), nullable=True),
        sa.Column("beat_sheet_id", sa.String(length=36), nullable=True),
        sa.Column("story_setup_id", sa.String(length=36), nullable=True),
        sa.Column("story_outline_id", sa.String(length=36), nullable=True),
        sa.Column("is_current", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["beat_sheet_id"], ["beat_sheets.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(
            ["character_sheet_id"], ["character_sheets.id"], ondelete="SET NULL"
        ),
        sa.ForeignKeyConstraint(["pitch_id"], ["pitches.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(
            ["restored_from_plan_revision_id"], ["plan_revisions.id"], ondelete="SET NULL"
        ),
        sa.ForeignKeyConstraint(["session_id"], ["story_sessions.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["story_outline_id"], ["story_outlines.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["story_setup_id"], ["story_setups.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_plan_revisions")),
        sa.UniqueConstraint(
            "session_id",
            "revision_number",
            name="uq_plan_revisions_session_id_revision_number",
        ),
    )
    op.create_index(
        "ix_plan_revisions_session_id_is_current",
        "plan_revisions",
        ["session_id", "is_current"],
        unique=False,
    )

    with op.batch_alter_table("composition_jobs", schema=None) as batch_op:
        batch_op.add_column(sa.Column("plan_revision_id", sa.String(length=36), nullable=True))
        batch_op.create_index(
            "ix_composition_jobs_plan_revision_id",
            ["plan_revision_id"],
            unique=False,
        )
        batch_op.create_foreign_key(
            "fk_composition_jobs_plan_revision_id_plan_revisions",
            "plan_revisions",
            ["plan_revision_id"],
            ["id"],
            ondelete="SET NULL",
        )


def downgrade() -> None:
    with op.batch_alter_table("composition_jobs", schema=None) as batch_op:
        batch_op.drop_constraint(
            "fk_composition_jobs_plan_revision_id_plan_revisions",
            type_="foreignkey",
        )
        batch_op.drop_index("ix_composition_jobs_plan_revision_id")
        batch_op.drop_column("plan_revision_id")

    op.drop_index("ix_plan_revisions_session_id_is_current", table_name="plan_revisions")
    op.drop_table("plan_revisions")
