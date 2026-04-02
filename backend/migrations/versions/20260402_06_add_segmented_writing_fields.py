"""Add segmented writing persistence fields.

Revision ID: 20260402_06_segmented_writing
Revises: 20260402_05_model_usage_metrics
Create Date: 2026-04-02 17:25:00.000000
"""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa


revision = "20260402_06_segmented_writing"
down_revision = "20260402_05_model_usage_metrics"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "composition_segments",
        sa.Column("raw_generated_text", sa.Text(), nullable=True),
    )
    op.add_column(
        "composition_segments",
        sa.Column("accepted_text", sa.Text(), nullable=True),
    )
    op.add_column(
        "composition_segments",
        sa.Column("accepted_summary", sa.Text(), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("composition_segments", "accepted_summary")
    op.drop_column("composition_segments", "accepted_text")
    op.drop_column("composition_segments", "raw_generated_text")
