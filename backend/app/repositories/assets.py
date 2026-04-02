from __future__ import annotations

from collections.abc import Sequence
from datetime import datetime

from sqlalchemy import Select, select
from sqlalchemy.orm import Session

from app.db import AssetKind, AssetStatus, SessionAsset

DOWNLOADABLE_ASSET_KINDS = (
    AssetKind.STORY_TEXT,
    AssetKind.STORY_DOCX,
    AssetKind.FINAL_AUDIO,
)


class SessionAssetRepository:
    def __init__(self, session: Session):
        self._session = session

    def create(
        self,
        *,
        session_id: str,
        asset_kind: AssetKind,
        storage_bucket: str,
        object_path: str,
        mime_type: str,
        status: AssetStatus = AssetStatus.PENDING,
        composition_job_id: str | None = None,
        composition_segment_id: str | None = None,
        audio_job_id: str | None = None,
        segment_index: int | None = None,
        byte_size: int | None = None,
        checksum_sha256: str | None = None,
        metadata_json: dict | list | None = None,
        error_message: str | None = None,
        ready_at: datetime | None = None,
        failed_at: datetime | None = None,
        superseded_at: datetime | None = None,
    ) -> SessionAsset:
        asset = SessionAsset(
            session_id=session_id,
            composition_job_id=composition_job_id,
            composition_segment_id=composition_segment_id,
            audio_job_id=audio_job_id,
            asset_kind=asset_kind,
            status=status,
            storage_bucket=storage_bucket,
            object_path=object_path,
            mime_type=mime_type,
            byte_size=byte_size,
            checksum_sha256=checksum_sha256,
            metadata_json=metadata_json,
            segment_index=segment_index,
            error_message=error_message,
            ready_at=ready_at,
            failed_at=failed_at,
            superseded_at=superseded_at,
        )
        self._session.add(asset)
        self._session.flush()
        return asset

    def get_by_id(self, asset_id: str) -> SessionAsset | None:
        return self._session.get(SessionAsset, asset_id)

    def get_by_storage_location(
        self,
        *,
        storage_bucket: str,
        object_path: str,
    ) -> SessionAsset | None:
        stmt: Select[tuple[SessionAsset]] = (
            select(SessionAsset)
            .where(
                SessionAsset.storage_bucket == storage_bucket,
                SessionAsset.object_path == object_path,
            )
            .limit(1)
        )
        return self._session.execute(stmt).scalar_one_or_none()

    def list_for_session(
        self,
        session_id: str,
        *,
        asset_kinds: Sequence[AssetKind] | None = None,
        statuses: Sequence[AssetStatus] | None = None,
        downloadable_only: bool = False,
        include_superseded: bool = True,
    ) -> list[SessionAsset]:
        stmt: Select[tuple[SessionAsset]] = select(SessionAsset).where(
            SessionAsset.session_id == session_id
        )

        if asset_kinds is not None:
            stmt = stmt.where(SessionAsset.asset_kind.in_(tuple(asset_kinds)))

        if statuses is not None:
            stmt = stmt.where(SessionAsset.status.in_(tuple(statuses)))

        if downloadable_only:
            stmt = stmt.where(SessionAsset.asset_kind.in_(DOWNLOADABLE_ASSET_KINDS))

        if not include_superseded:
            stmt = stmt.where(SessionAsset.status != AssetStatus.SUPERSEDED)

        stmt = stmt.order_by(
            SessionAsset.created_at.desc(),
            SessionAsset.segment_index.asc(),
            SessionAsset.id.desc(),
        )
        return list(self._session.execute(stmt).scalars().all())

    def get_latest_ready(
        self,
        session_id: str,
        *,
        asset_kinds: Sequence[AssetKind],
    ) -> SessionAsset | None:
        stmt: Select[tuple[SessionAsset]] = (
            select(SessionAsset)
            .where(
                SessionAsset.session_id == session_id,
                SessionAsset.asset_kind.in_(tuple(asset_kinds)),
                SessionAsset.status == AssetStatus.READY,
            )
            .order_by(SessionAsset.ready_at.desc(), SessionAsset.created_at.desc())
            .limit(1)
        )
        return self._session.execute(stmt).scalar_one_or_none()

    def mark_ready(
        self,
        asset: SessionAsset,
        *,
        byte_size: int | None = None,
        checksum_sha256: str | None = None,
        metadata_json: dict | list | None = None,
        ready_at: datetime,
    ) -> SessionAsset:
        asset.status = AssetStatus.READY
        asset.byte_size = byte_size if byte_size is not None else asset.byte_size
        asset.checksum_sha256 = checksum_sha256 or asset.checksum_sha256
        asset.metadata_json = metadata_json if metadata_json is not None else asset.metadata_json
        asset.error_message = None
        asset.failed_at = None
        asset.ready_at = ready_at
        self._session.flush()
        return asset

    def mark_failed(
        self,
        asset: SessionAsset,
        *,
        error_message: str,
        metadata_json: dict | list | None = None,
        failed_at: datetime,
    ) -> SessionAsset:
        asset.status = AssetStatus.FAILED
        asset.error_message = error_message
        asset.metadata_json = metadata_json if metadata_json is not None else asset.metadata_json
        asset.failed_at = failed_at
        asset.ready_at = None
        self._session.flush()
        return asset
