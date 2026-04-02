"""add session audio settings

Revision ID: 20260402_09
Revises: 20260402_08
Create Date: 2026-04-02 10:15:00.000000
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "20260402_09"
down_revision: str | None = "20260402_08"
branch_labels: Sequence[str] | None = None
depends_on: Sequence[str] | None = None


def upgrade() -> None:
    op.add_column("story_sessions", sa.Column("audio_voice_key", sa.String(length=120), nullable=True))
    op.add_column(
        "story_sessions",
        sa.Column("audio_narration_style", sa.String(length=60), nullable=True),
    )
    op.add_column(
        "story_sessions",
        sa.Column("audio_playback_speed", sa.Numeric(precision=4, scale=2, asdecimal=False), nullable=True),
    )
    op.add_column(
        "story_sessions",
        sa.Column("audio_include_background_music", sa.Boolean(), nullable=True),
    )
    op.add_column(
        "story_sessions",
        sa.Column("audio_music_profile", sa.String(length=120), nullable=True),
    )
    op.add_column(
        "story_sessions",
        sa.Column("audio_narration_volume", sa.Integer(), nullable=True),
    )
    op.add_column(
        "story_sessions",
        sa.Column("audio_music_volume", sa.Integer(), nullable=True),
    )
    op.add_column(
        "story_sessions",
        sa.Column("audio_guidance_notes", sa.Text(), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("story_sessions", "audio_guidance_notes")
    op.drop_column("story_sessions", "audio_music_volume")
    op.drop_column("story_sessions", "audio_narration_volume")
    op.drop_column("story_sessions", "audio_music_profile")
    op.drop_column("story_sessions", "audio_include_background_music")
    op.drop_column("story_sessions", "audio_playback_speed")
    op.drop_column("story_sessions", "audio_narration_style")
    op.drop_column("story_sessions", "audio_voice_key")
