"""add durable background jobs for worker execution

Revision ID: 20260401_01
Revises: 20260331_03
Create Date: 2026-04-01 09:30:00.000000
"""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "20260401_01"
down_revision = "20260331_03"
branch_labels = None
depends_on = None


JOB_STATUS_VALUES = (
    "queued",
    "in_progress",
    "paused",
    "completed",
    "failed",
    "cancelled",
)


def job_status_enum() -> sa.Enum:
    return sa.Enum(*JOB_STATUS_VALUES, name="job_status", native_enum=False)


def timestamp_column(name: str, *, nullable: bool = False) -> sa.Column:
    return sa.Column(
        name,
        sa.DateTime(timezone=True),
        nullable=nullable,
        server_default=sa.text("CURRENT_TIMESTAMP") if not nullable else None,
    )


def upgrade() -> None:
    op.create_table(
        "background_jobs",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("session_id", sa.String(length=36), nullable=True),
        sa.Column("job_type", sa.String(length=120), nullable=False),
        sa.Column(
            "status",
            job_status_enum(),
            nullable=False,
            server_default="queued",
        ),
        sa.Column("payload", sa.JSON(), nullable=False),
        sa.Column("result_summary", sa.JSON(), nullable=True),
        sa.Column("attempt_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("lease_owner", sa.String(length=120), nullable=True),
        sa.Column("lease_token", sa.String(length=36), nullable=True),
        sa.Column("lease_expires_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("claimed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("heartbeat_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("failed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("error_message", sa.Text(), nullable=True),
        timestamp_column("created_at"),
        timestamp_column("updated_at"),
        sa.ForeignKeyConstraint(
            ["session_id"],
            ["story_sessions.id"],
            name="fk_background_jobs_session_id_story_sessions",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name="pk_background_jobs"),
    )
    op.create_index(
        "ix_background_jobs_status_created_at",
        "background_jobs",
        ["status", "created_at"],
        unique=False,
    )
    op.create_index(
        "ix_background_jobs_status_lease_expires_at",
        "background_jobs",
        ["status", "lease_expires_at"],
        unique=False,
    )
    op.create_index(
        "ix_background_jobs_job_type_status_created_at",
        "background_jobs",
        ["job_type", "status", "created_at"],
        unique=False,
    )
    op.create_index(
        "ix_background_jobs_session_id_created_at",
        "background_jobs",
        ["session_id", "created_at"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index("ix_background_jobs_session_id_created_at", table_name="background_jobs")
    op.drop_index("ix_background_jobs_job_type_status_created_at", table_name="background_jobs")
    op.drop_index("ix_background_jobs_status_lease_expires_at", table_name="background_jobs")
    op.drop_index("ix_background_jobs_status_created_at", table_name="background_jobs")
    op.drop_table("background_jobs")
