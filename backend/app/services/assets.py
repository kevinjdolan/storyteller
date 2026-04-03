from __future__ import annotations

from collections.abc import Mapping, Sequence
from datetime import datetime
from typing import Any

from sqlalchemy.orm import Session

from app.db import (
    AssetKind,
    AssetStatus,
    AudioJob,
    CompositionJob,
    CompositionSegment,
    SessionAsset,
    StorySession,
)
from app.db.base import utc_now
from app.models import SessionAssetView
from app.repositories import DOWNLOADABLE_ASSET_KINDS, SessionAssetRepository


class AssetServiceError(Exception):
    """Base error for asset service failures."""


class AssetNotFoundError(AssetServiceError):
    """Raised when a requested asset record does not exist."""


class AssetSessionNotFoundError(AssetServiceError):
    """Raised when a requested story session does not exist."""


class AssetOwnershipError(AssetServiceError):
    """Raised when a linked job or segment does not belong to the target session."""


class SessionAssetService:
    def __init__(self, session: Session):
        self._session = session
        self._assets = SessionAssetRepository(session)

    def save_asset_record(
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
        commit: bool = True,
    ) -> SessionAssetView:
        self._require_session(session_id)
        composition_job = self._validate_composition_job(session_id, composition_job_id)
        composition_segment = self._validate_composition_segment(session_id, composition_segment_id)
        audio_job = self._validate_audio_job(session_id, audio_job_id)
        if composition_job is None and composition_segment is not None:
            composition_job = composition_segment.composition_job
        self._validate_asset_links(
            asset_kind=asset_kind,
            composition_job=composition_job,
            composition_segment=composition_segment,
            audio_job=audio_job,
        )

        resolved_segment_index = segment_index
        if resolved_segment_index is None and composition_segment is not None:
            resolved_segment_index = composition_segment.segment_index
        if asset_kind == AssetKind.AUDIO_SEGMENT and resolved_segment_index is None:
            raise ValueError("audio_segment assets require segment_index")

        now = utc_now()
        ready_at = now if status == AssetStatus.READY else None
        failed_at = now if status == AssetStatus.FAILED else None
        normalized_error = _normalize_optional_text(error_message)

        if status == AssetStatus.FAILED and not normalized_error:
            raise ValueError("failed asset records require an error_message")

        asset = self._assets.create(
            session_id=session_id,
            asset_kind=asset_kind,
            storage_bucket=_normalize_required_text(storage_bucket, field_name="storage_bucket"),
            object_path=_normalize_required_text(object_path, field_name="object_path"),
            mime_type=_normalize_required_text(mime_type, field_name="mime_type"),
            status=status,
            composition_job_id=composition_job.id if composition_job else None,
            composition_segment_id=composition_segment.id if composition_segment else None,
            audio_job_id=audio_job.id if audio_job else None,
            segment_index=resolved_segment_index,
            byte_size=byte_size,
            checksum_sha256=_normalize_optional_text(checksum_sha256),
            metadata_json=metadata_json,
            error_message=normalized_error,
            ready_at=ready_at,
            failed_at=failed_at,
        )
        if commit:
            self._session.commit()
        return _build_session_asset_view(asset)

    def upsert_asset_record(
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
        commit: bool = True,
    ) -> SessionAssetView:
        normalized_bucket = _normalize_required_text(
            storage_bucket,
            field_name="storage_bucket",
        )
        normalized_object_path = _normalize_required_text(
            object_path,
            field_name="object_path",
        )
        normalized_mime_type = _normalize_required_text(
            mime_type,
            field_name="mime_type",
        )
        normalized_error = _normalize_optional_text(error_message)
        self._require_session(session_id)

        composition_job = self._validate_composition_job(session_id, composition_job_id)
        composition_segment = self._validate_composition_segment(session_id, composition_segment_id)
        audio_job = self._validate_audio_job(session_id, audio_job_id)
        if composition_job is None and composition_segment is not None:
            composition_job = composition_segment.composition_job
        self._validate_asset_links(
            asset_kind=asset_kind,
            composition_job=composition_job,
            composition_segment=composition_segment,
            audio_job=audio_job,
        )

        resolved_segment_index = segment_index
        if resolved_segment_index is None and composition_segment is not None:
            resolved_segment_index = composition_segment.segment_index
        if asset_kind == AssetKind.AUDIO_SEGMENT and resolved_segment_index is None:
            raise ValueError("audio_segment assets require segment_index")

        if status == AssetStatus.FAILED and not normalized_error:
            raise ValueError("failed asset records require an error_message")

        existing_asset = self._assets.get_by_storage_location(
            storage_bucket=normalized_bucket,
            object_path=normalized_object_path,
        )
        if existing_asset is None:
            return self.save_asset_record(
                session_id=session_id,
                asset_kind=asset_kind,
                storage_bucket=normalized_bucket,
                object_path=normalized_object_path,
                mime_type=normalized_mime_type,
                status=status,
                composition_job_id=composition_job.id if composition_job is not None else None,
                composition_segment_id=(
                    composition_segment.id if composition_segment is not None else None
                ),
                audio_job_id=audio_job.id if audio_job is not None else None,
                segment_index=resolved_segment_index,
                byte_size=byte_size,
                checksum_sha256=checksum_sha256,
                metadata_json=metadata_json,
                error_message=normalized_error,
                commit=commit,
            )

        if existing_asset.session_id != session_id:
            raise AssetOwnershipError(
                f"asset at {normalized_bucket}/{normalized_object_path} does not belong to "
                f"session {session_id!r}"
            )
        if existing_asset.asset_kind != asset_kind:
            raise ValueError(
                "existing asset kind does not match the requested upsert asset_kind"
            )

        existing_asset.status = status
        existing_asset.mime_type = normalized_mime_type
        existing_asset.composition_job_id = composition_job.id if composition_job else None
        existing_asset.composition_segment_id = (
            composition_segment.id if composition_segment else None
        )
        existing_asset.audio_job_id = audio_job.id if audio_job else None
        existing_asset.segment_index = resolved_segment_index
        existing_asset.byte_size = byte_size
        existing_asset.checksum_sha256 = _normalize_optional_text(checksum_sha256)
        existing_asset.metadata_json = metadata_json
        existing_asset.error_message = normalized_error
        existing_asset.superseded_at = None

        now = utc_now()
        existing_asset.ready_at = now if status == AssetStatus.READY else None
        existing_asset.failed_at = now if status == AssetStatus.FAILED else None
        if commit:
            self._session.commit()
        return _build_session_asset_view(existing_asset)

    def mark_asset_ready(
        self,
        asset_id: str,
        *,
        byte_size: int | None = None,
        checksum_sha256: str | None = None,
        metadata_json: dict | list | None = None,
        ready_at: datetime | None = None,
        commit: bool = True,
    ) -> SessionAssetView:
        asset = self._require_asset(asset_id)
        self._assets.mark_ready(
            asset,
            byte_size=byte_size,
            checksum_sha256=_normalize_optional_text(checksum_sha256),
            metadata_json=metadata_json,
            ready_at=ready_at or utc_now(),
        )
        if commit:
            self._session.commit()
        return _build_session_asset_view(asset)

    def mark_asset_failed(
        self,
        asset_id: str,
        *,
        error_message: str,
        metadata_json: dict | list | None = None,
        failed_at: datetime | None = None,
        commit: bool = True,
    ) -> SessionAssetView:
        asset = self._require_asset(asset_id)
        self._assets.mark_failed(
            asset,
            error_message=_normalize_required_text(error_message, field_name="error_message"),
            metadata_json=metadata_json,
            failed_at=failed_at or utc_now(),
        )
        if commit:
            self._session.commit()
        return _build_session_asset_view(asset)

    def supersede_assets(
        self,
        session_id: str,
        *,
        asset_kinds: Sequence[AssetKind],
        exclude_asset_ids: Sequence[str] = (),
        replacement_asset_id: str | None = None,
        replacement_audio_job_id: str | None = None,
        reason: str | None = None,
        superseded_at: datetime | None = None,
        commit: bool = True,
    ) -> list[SessionAssetView]:
        self._require_session(session_id)
        excluded_ids = {asset_id for asset_id in exclude_asset_ids if asset_id}
        rows = self._assets.list_for_session(
            session_id,
            asset_kinds=asset_kinds,
            statuses=(AssetStatus.READY,),
            include_superseded=False,
        )
        if not rows:
            return []

        now = superseded_at or utc_now()
        updated: list[SessionAsset] = []
        for row in rows:
            if row.id in excluded_ids:
                continue
            row.status = AssetStatus.SUPERSEDED
            row.superseded_at = now
            existing_details = _read_mapping(row.metadata_json)
            row.metadata_json = {
                **existing_details,
                "superseded_reason": _normalize_optional_text(reason),
                "superseded_by_asset_id": replacement_asset_id,
                "superseded_by_audio_job_id": replacement_audio_job_id,
            }
            updated.append(row)

        if commit:
            self._session.commit()
        else:
            self._session.flush()

        return [_build_session_asset_view(row) for row in updated]

    def list_session_assets(
        self,
        session_id: str,
        *,
        asset_kinds: Sequence[AssetKind] | None = None,
        statuses: Sequence[AssetStatus] | None = None,
        downloadable_only: bool = False,
        include_superseded: bool = True,
    ) -> list[SessionAssetView]:
        self._require_session(session_id)
        rows = self._assets.list_for_session(
            session_id,
            asset_kinds=asset_kinds,
            statuses=statuses,
            downloadable_only=downloadable_only,
            include_superseded=include_superseded,
        )
        return [_build_session_asset_view(row) for row in rows]

    def list_downloadable_assets(self, session_id: str) -> list[SessionAssetView]:
        return self.list_session_assets(
            session_id,
            asset_kinds=DOWNLOADABLE_ASSET_KINDS,
            statuses=(AssetStatus.READY,),
            downloadable_only=True,
            include_superseded=False,
        )

    def _require_session(self, session_id: str) -> StorySession:
        story_session = self._session.get(StorySession, session_id)
        if story_session is None:
            raise AssetSessionNotFoundError(f"session {session_id!r} was not found")
        return story_session

    def _require_asset(self, asset_id: str) -> SessionAsset:
        asset = self._assets.get_by_id(asset_id)
        if asset is None:
            raise AssetNotFoundError(f"asset {asset_id!r} was not found")
        return asset

    def _validate_composition_job(
        self,
        session_id: str,
        composition_job_id: str | None,
    ) -> CompositionJob | None:
        if composition_job_id is None:
            return None

        composition_job = self._session.get(CompositionJob, composition_job_id)
        if composition_job is None or composition_job.session_id != session_id:
            raise AssetOwnershipError(
                f"composition job {composition_job_id!r} does not belong to session {session_id!r}"
            )
        return composition_job

    def _validate_composition_segment(
        self,
        session_id: str,
        composition_segment_id: str | None,
    ) -> CompositionSegment | None:
        if composition_segment_id is None:
            return None

        composition_segment = self._session.get(CompositionSegment, composition_segment_id)
        if composition_segment is None or composition_segment.session_id != session_id:
            raise AssetOwnershipError(
                f"composition segment {composition_segment_id!r} does not belong to session "
                f"{session_id!r}"
            )
        return composition_segment

    def _validate_audio_job(self, session_id: str, audio_job_id: str | None) -> AudioJob | None:
        if audio_job_id is None:
            return None

        audio_job = self._session.get(AudioJob, audio_job_id)
        if audio_job is None or audio_job.session_id != session_id:
            raise AssetOwnershipError(
                f"audio job {audio_job_id!r} does not belong to session {session_id!r}"
            )
        return audio_job

    def _validate_asset_links(
        self,
        *,
        asset_kind: AssetKind,
        composition_job: CompositionJob | None,
        composition_segment: CompositionSegment | None,
        audio_job: AudioJob | None,
    ) -> None:
        if composition_segment is not None and composition_job is not None:
            if composition_segment.composition_job_id != composition_job.id:
                raise AssetOwnershipError(
                    "composition_segment_id does not belong to the provided composition_job_id"
                )

        if asset_kind == AssetKind.COMPOSITION_SEGMENT:
            if composition_segment is None and composition_job is None:
                raise ValueError(
                    "composition_segment assets require "
                    "composition_segment_id or composition_job_id"
                )

        if asset_kind == AssetKind.AUDIO_SEGMENT and audio_job is None:
            raise ValueError("audio_segment assets require audio_job_id")

        if asset_kind == AssetKind.FINAL_AUDIO and audio_job is None:
            raise ValueError("final_audio assets require audio_job_id")


def _build_session_asset_view(row: SessionAsset) -> SessionAssetView:
    details = _read_mapping(row.metadata_json)
    return SessionAssetView(
        id=row.id,
        asset_kind=row.asset_kind,
        status=row.status,
        storage_bucket=row.storage_bucket,
        object_path=row.object_path,
        mime_type=row.mime_type,
        composition_job_id=row.composition_job_id,
        audio_job_id=row.audio_job_id,
        byte_size=row.byte_size,
        duration_seconds=_read_duration_seconds(details),
        checksum_sha256=row.checksum_sha256,
        segment_index=row.segment_index,
        error_message=row.error_message,
        details=details or None,
        ready_at=row.ready_at,
        failed_at=row.failed_at,
        superseded_at=row.superseded_at,
        created_at=row.created_at,
        updated_at=row.updated_at,
    )


def _read_mapping(value: Any) -> dict[str, Any]:
    return dict(value) if isinstance(value, Mapping) else {}


def _read_duration_seconds(details: dict[str, Any]) -> float | None:
    raw_value = details.get("duration_seconds")
    if raw_value is None:
        return None
    try:
        return float(raw_value)
    except (TypeError, ValueError):
        return None


def _normalize_optional_text(value: str | None) -> str | None:
    if value is None:
        return None

    normalized = value.strip()
    return normalized or None


def _normalize_required_text(value: str, *, field_name: str) -> str:
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} must not be empty")
    return normalized
