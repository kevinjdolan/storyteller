"""Add model usage metrics tables.

Revision ID: 20260402_05_model_usage_metrics
Revises: 20260402_04_plan_revisions
Create Date: 2026-04-02 16:10:00.000000
"""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "20260402_05_model_usage_metrics"
down_revision = "20260402_04_plan_revisions"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "model_usage_events",
        sa.Column("session_id", sa.String(length=36), nullable=False),
        sa.Column("usage_bucket", sa.String(length=32), nullable=False),
        sa.Column("workflow_stage", sa.String(length=32), nullable=True),
        sa.Column("purpose", sa.String(length=120), nullable=False),
        sa.Column("provider", sa.String(length=40), nullable=False),
        sa.Column("model_id", sa.String(length=120), nullable=False),
        sa.Column("prompt_version", sa.String(length=120), nullable=True),
        sa.Column("outcome", sa.String(length=40), nullable=False),
        sa.Column("elapsed_ms", sa.Integer(), nullable=False),
        sa.Column("input_tokens", sa.Integer(), nullable=True),
        sa.Column("output_tokens", sa.Integer(), nullable=True),
        sa.Column("total_tokens", sa.Integer(), nullable=True),
        sa.Column("cached_input_tokens", sa.Integer(), nullable=True),
        sa.Column("thought_tokens", sa.Integer(), nullable=True),
        sa.Column("approximate_cost_usd", sa.Numeric(12, 6, asdecimal=False), nullable=True),
        sa.Column("error_message", sa.String(length=255), nullable=True),
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["session_id"], ["story_sessions.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_model_usage_events")),
    )
    op.create_index(
        "ix_model_usage_events_session_id_created_at",
        "model_usage_events",
        ["session_id", "created_at"],
        unique=False,
    )
    op.create_index(
        "ix_model_usage_events_session_id_usage_bucket",
        "model_usage_events",
        ["session_id", "usage_bucket"],
        unique=False,
    )
    op.create_index(
        "ix_model_usage_events_session_id_elapsed_ms",
        "model_usage_events",
        ["session_id", "elapsed_ms"],
        unique=False,
    )

    op.create_table(
        "session_usage_rollups",
        sa.Column("session_id", sa.String(length=36), nullable=False),
        sa.Column("usage_bucket", sa.String(length=32), nullable=False),
        sa.Column("total_calls", sa.Integer(), nullable=False),
        sa.Column("succeeded_calls", sa.Integer(), nullable=False),
        sa.Column("failed_calls", sa.Integer(), nullable=False),
        sa.Column("fallback_calls", sa.Integer(), nullable=False),
        sa.Column("token_metadata_call_count", sa.Integer(), nullable=False),
        sa.Column("cost_estimate_call_count", sa.Integer(), nullable=False),
        sa.Column("total_elapsed_ms", sa.Integer(), nullable=False),
        sa.Column("max_elapsed_ms", sa.Integer(), nullable=False),
        sa.Column("input_tokens", sa.Integer(), nullable=False),
        sa.Column("output_tokens", sa.Integer(), nullable=False),
        sa.Column("total_tokens", sa.Integer(), nullable=False),
        sa.Column("cached_input_tokens", sa.Integer(), nullable=False),
        sa.Column("thought_tokens", sa.Integer(), nullable=False),
        sa.Column("approximate_cost_usd_total", sa.Numeric(12, 6, asdecimal=False), nullable=False),
        sa.Column("models_json", sa.JSON(), nullable=False),
        sa.Column("last_model_id", sa.String(length=120), nullable=True),
        sa.Column("last_purpose", sa.String(length=120), nullable=True),
        sa.Column("last_called_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["session_id"], ["story_sessions.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_session_usage_rollups")),
        sa.UniqueConstraint(
            "session_id",
            "usage_bucket",
            name="uq_session_usage_rollups_session_id_usage_bucket",
        ),
    )
    op.create_index(
        "ix_session_usage_rollups_session_id_last_called_at",
        "session_usage_rollups",
        ["session_id", "last_called_at"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(
        "ix_session_usage_rollups_session_id_last_called_at",
        table_name="session_usage_rollups",
    )
    op.drop_table("session_usage_rollups")

    op.drop_index("ix_model_usage_events_session_id_elapsed_ms", table_name="model_usage_events")
    op.drop_index(
        "ix_model_usage_events_session_id_usage_bucket",
        table_name="model_usage_events",
    )
    op.drop_index("ix_model_usage_events_session_id_created_at", table_name="model_usage_events")
    op.drop_table("model_usage_events")
