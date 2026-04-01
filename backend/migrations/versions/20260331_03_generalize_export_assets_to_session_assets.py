"""generalize export assets into session asset records

Revision ID: 20260331_03
Revises: 20260331_02
Create Date: 2026-03-31 23:55:00.000000
"""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "20260331_03"
down_revision = "20260331_02"
branch_labels = None
depends_on = None


CURRENT_ASSET_KIND_VALUES = (
    "draft_text_snapshot",
    "composition_segment",
    "story_text",
    "story_docx",
    "audio_segment",
    "final_audio",
)
CURRENT_ASSET_STATUS_VALUES = (
    "pending",
    "in_progress",
    "ready",
    "failed",
    "superseded",
)
LEGACY_ASSET_KIND_VALUES = ("story_text", "story_docx", "audio_segment", "final_audio")
LEGACY_ASSET_STATUS_VALUES = ("pending", "ready", "failed", "superseded")


def asset_kind_enum(values: tuple[str, ...]) -> sa.Enum:
    return sa.Enum(*values, name="asset_kind", native_enum=False)


def asset_status_enum(values: tuple[str, ...]) -> sa.Enum:
    return sa.Enum(*values, name="asset_status", native_enum=False)


def timestamp_column(name: str, *, nullable: bool = False) -> sa.Column:
    return sa.Column(
        name,
        sa.DateTime(timezone=True),
        nullable=nullable,
        server_default=sa.text("CURRENT_TIMESTAMP") if not nullable else None,
    )


def upgrade() -> None:
    op.create_table(
        "session_assets",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("session_id", sa.String(length=36), nullable=False),
        sa.Column("composition_job_id", sa.String(length=36), nullable=True),
        sa.Column("composition_segment_id", sa.String(length=36), nullable=True),
        sa.Column("audio_job_id", sa.String(length=36), nullable=True),
        sa.Column("asset_kind", asset_kind_enum(CURRENT_ASSET_KIND_VALUES), nullable=False),
        sa.Column(
            "status",
            asset_status_enum(CURRENT_ASSET_STATUS_VALUES),
            nullable=False,
            server_default="pending",
        ),
        sa.Column("storage_bucket", sa.String(length=120), nullable=False),
        sa.Column("object_path", sa.String(length=255), nullable=False),
        sa.Column("mime_type", sa.String(length=120), nullable=False),
        sa.Column("byte_size", sa.Integer(), nullable=True),
        sa.Column("checksum_sha256", sa.String(length=64), nullable=True),
        sa.Column("metadata_json", sa.JSON(), nullable=True),
        sa.Column("segment_index", sa.Integer(), nullable=True),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.Column("ready_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("failed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("superseded_at", sa.DateTime(timezone=True), nullable=True),
        timestamp_column("created_at"),
        timestamp_column("updated_at"),
        sa.ForeignKeyConstraint(
            ["audio_job_id"],
            ["audio_jobs.id"],
            name="fk_session_assets_audio_job_id_audio_jobs",
            ondelete="SET NULL",
        ),
        sa.ForeignKeyConstraint(
            ["composition_job_id"],
            ["composition_jobs.id"],
            name="fk_session_assets_composition_job_id_composition_jobs",
            ondelete="SET NULL",
        ),
        sa.ForeignKeyConstraint(
            ["composition_segment_id"],
            ["composition_segments.id"],
            name="fk_session_assets_composition_segment_id_composition_segments",
            ondelete="SET NULL",
        ),
        sa.ForeignKeyConstraint(
            ["session_id"],
            ["story_sessions.id"],
            name="fk_session_assets_session_id_story_sessions",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name="pk_session_assets"),
        sa.UniqueConstraint(
            "storage_bucket",
            "object_path",
            name="uq_session_assets_storage_bucket_object_path",
        ),
    )
    op.create_index(
        "ix_session_assets_session_id_asset_kind_status",
        "session_assets",
        ["session_id", "asset_kind", "status"],
        unique=False,
    )
    op.create_index(
        "ix_session_assets_audio_job_id_asset_kind_segment_index",
        "session_assets",
        ["audio_job_id", "asset_kind", "segment_index"],
        unique=False,
    )
    op.create_index(
        "ix_session_assets_composition_job_id_asset_kind_segment_index",
        "session_assets",
        ["composition_job_id", "asset_kind", "segment_index"],
        unique=False,
    )

    op.execute(
        """
        INSERT INTO session_assets (
            id,
            session_id,
            composition_job_id,
            audio_job_id,
            asset_kind,
            status,
            storage_bucket,
            object_path,
            mime_type,
            byte_size,
            checksum_sha256,
            metadata_json,
            ready_at,
            superseded_at,
            created_at,
            updated_at
        )
        SELECT
            id,
            session_id,
            composition_job_id,
            audio_job_id,
            asset_kind,
            status,
            storage_bucket,
            storage_key,
            mime_type,
            byte_size,
            checksum_sha256,
            metadata_json,
            ready_at,
            superseded_at,
            created_at,
            updated_at
        FROM export_assets
        """
    )

    op.drop_table("export_assets")


def downgrade() -> None:
    op.create_table(
        "export_assets",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("session_id", sa.String(length=36), nullable=False),
        sa.Column("composition_job_id", sa.String(length=36), nullable=True),
        sa.Column("audio_job_id", sa.String(length=36), nullable=True),
        sa.Column("asset_kind", asset_kind_enum(LEGACY_ASSET_KIND_VALUES), nullable=False),
        sa.Column(
            "status",
            asset_status_enum(LEGACY_ASSET_STATUS_VALUES),
            nullable=False,
            server_default="pending",
        ),
        sa.Column("storage_bucket", sa.String(length=120), nullable=False),
        sa.Column("storage_key", sa.String(length=255), nullable=False),
        sa.Column("mime_type", sa.String(length=120), nullable=False),
        sa.Column("byte_size", sa.Integer(), nullable=True),
        sa.Column("checksum_sha256", sa.String(length=64), nullable=True),
        sa.Column("metadata_json", sa.JSON(), nullable=True),
        sa.Column("ready_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("superseded_at", sa.DateTime(timezone=True), nullable=True),
        timestamp_column("created_at"),
        timestamp_column("updated_at"),
        sa.ForeignKeyConstraint(
            ["audio_job_id"],
            ["audio_jobs.id"],
            name="fk_export_assets_audio_job_id_audio_jobs",
            ondelete="SET NULL",
        ),
        sa.ForeignKeyConstraint(
            ["composition_job_id"],
            ["composition_jobs.id"],
            name="fk_export_assets_composition_job_id_composition_jobs",
            ondelete="SET NULL",
        ),
        sa.ForeignKeyConstraint(
            ["session_id"],
            ["story_sessions.id"],
            name="fk_export_assets_session_id_story_sessions",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name="pk_export_assets"),
        sa.UniqueConstraint(
            "storage_bucket",
            "storage_key",
            name="uq_export_assets_storage_bucket_storage_key",
        ),
    )
    op.create_index(
        "ix_export_assets_session_id_asset_kind_status",
        "export_assets",
        ["session_id", "asset_kind", "status"],
        unique=False,
    )

    op.execute(
        """
        INSERT INTO export_assets (
            id,
            session_id,
            composition_job_id,
            audio_job_id,
            asset_kind,
            status,
            storage_bucket,
            storage_key,
            mime_type,
            byte_size,
            checksum_sha256,
            metadata_json,
            ready_at,
            superseded_at,
            created_at,
            updated_at
        )
        SELECT
            id,
            session_id,
            composition_job_id,
            audio_job_id,
            CASE
                WHEN asset_kind IN ('draft_text_snapshot', 'composition_segment')
                    THEN 'story_text'
                ELSE asset_kind
            END AS asset_kind,
            CASE
                WHEN status = 'in_progress' THEN 'pending'
                ELSE status
            END AS status,
            storage_bucket,
            object_path,
            mime_type,
            byte_size,
            checksum_sha256,
            metadata_json,
            ready_at,
            superseded_at,
            created_at,
            updated_at
        FROM session_assets
        """
    )

    op.drop_index(
        "ix_session_assets_composition_job_id_asset_kind_segment_index",
        table_name="session_assets",
    )
    op.drop_index(
        "ix_session_assets_audio_job_id_asset_kind_segment_index",
        table_name="session_assets",
    )
    op.drop_index("ix_session_assets_session_id_asset_kind_status", table_name="session_assets")
    op.drop_table("session_assets")
