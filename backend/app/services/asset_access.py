from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Iterable
from urllib.parse import quote

from sqlalchemy.orm import Session

from app.db import AssetKind, AssetStatus, SessionAsset, StorySession
from app.models import SessionAssetAccessView
from app.repositories import SessionAssetRepository
from app.services.assets import AssetSessionNotFoundError
from app.services.story_exports import (
    StoryDocxExportService,
    StoryExportUnavailableError,
    resolve_asset_filename,
)
from app.settings import get_settings
from app.storage import ObjectStorageService, StorageObjectLocation


class SessionArtifactHandle(str, Enum):
    STORY_TEXT = "story-text"
    STORY_DOCX = "story-docx"
    FINAL_AUDIO = "final-audio"


class SessionArtifactAccessError(Exception):
    """Base error for session artifact access failures."""


class SessionArtifactNotFoundError(SessionArtifactAccessError):
    """Raised when a session or asset target does not exist."""


class SessionArtifactUnavailableError(SessionArtifactAccessError):
    """Raised when a session exists but the target asset is not ready."""


@dataclass(frozen=True)
class SessionAssetContent:
    asset: SessionAsset
    payload: bytes
    filename: str


class SessionArtifactAccessService:
    def __init__(
        self,
        session: Session,
        *,
        object_storage: ObjectStorageService,
    ) -> None:
        self._session = session
        self._assets = SessionAssetRepository(session)
        self._object_storage = object_storage

    def load_named_artifact(
        self,
        session_id: str,
        artifact_handle: SessionArtifactHandle,
    ) -> SessionAsset:
        self._require_session(session_id)

        if artifact_handle == SessionArtifactHandle.STORY_DOCX:
            try:
                return StoryDocxExportService(
                    self._session,
                    object_storage=self._object_storage,
                ).ensure_docx_asset(session_id)
            except AssetSessionNotFoundError as exc:
                raise SessionArtifactNotFoundError(str(exc)) from exc
            except StoryExportUnavailableError as exc:
                raise SessionArtifactUnavailableError(str(exc)) from exc

        asset_kind = {
            SessionArtifactHandle.STORY_TEXT: AssetKind.STORY_TEXT,
            SessionArtifactHandle.FINAL_AUDIO: AssetKind.FINAL_AUDIO,
        }.get(artifact_handle)
        if asset_kind is None:
            raise SessionArtifactNotFoundError("The requested artifact target is not supported.")

        asset = self._assets.get_latest_ready(session_id, asset_kinds=(asset_kind,))
        if asset is None:
            raise SessionArtifactUnavailableError(
                "The requested artifact is not ready for this session."
            )
        return asset

    def load_ready_asset(self, session_id: str, asset_id: str) -> SessionAsset:
        asset = self._assets.get_by_id(asset_id)
        if asset is None or asset.session_id != session_id:
            self._require_session(session_id)
            raise SessionArtifactNotFoundError(
                "The requested asset was not found for this session."
            )
        if asset.status != AssetStatus.READY:
            raise SessionArtifactUnavailableError("The requested asset is not ready yet.")
        return asset

    def load_asset_content(self, asset: SessionAsset) -> SessionAssetContent:
        payload = self._object_storage.download_bytes(
            StorageObjectLocation(
                bucket=asset.storage_bucket,
                key=asset.object_path,
            )
        )
        return SessionAssetContent(
            asset=asset,
            payload=payload,
            filename=resolve_asset_filename(asset),
        )

    def _require_session(self, session_id: str) -> StorySession:
        story_session = self._session.get(StorySession, session_id)
        if story_session is None:
            raise SessionArtifactNotFoundError(f"session {session_id!r} was not found")
        return story_session


def build_session_asset_access_view(
    row: SessionAsset,
) -> SessionAssetAccessView | None:
    if row.status != AssetStatus.READY:
        return None

    return SessionAssetAccessView(
        download_path=build_session_asset_content_path(
            session_id=row.session_id,
            asset_id=row.id,
            disposition="attachment",
        ),
        stream_path=(
            build_session_asset_content_path(
                session_id=row.session_id,
                asset_id=row.id,
                disposition="inline",
            )
            if asset_supports_inline_stream(row)
            else None
        ),
        filename=resolve_asset_filename(row),
    )


def build_session_asset_content_path(
    *,
    session_id: str,
    asset_id: str,
    disposition: str,
) -> str:
    prefix = get_settings().api_v1_prefix.rstrip("/")
    return (
        f"{prefix}/sessions/{quote(session_id, safe='')}/assets/{quote(asset_id, safe='')}"
        f"/content?disposition={quote(disposition, safe='')}"
    )


def build_named_session_artifact_path(
    *,
    session_id: str,
    artifact_handle: SessionArtifactHandle,
    disposition: str = "attachment",
) -> str:
    prefix = get_settings().api_v1_prefix.rstrip("/")
    return (
        f"{prefix}/sessions/{quote(session_id, safe='')}/artifacts/"
        f"{quote(artifact_handle.value, safe='')}?disposition={quote(disposition, safe='')}"
    )


def asset_supports_inline_stream(asset: SessionAsset) -> bool:
    if asset.asset_kind in {AssetKind.AUDIO_SEGMENT, AssetKind.FINAL_AUDIO, AssetKind.STORY_TEXT}:
        return True
    return asset.mime_type.startswith(("audio/", "text/"))


def iter_content_chunks(payload: bytes, *, chunk_size: int = 64 * 1024) -> Iterable[bytes]:
    for start_index in range(0, len(payload), chunk_size):
        yield payload[start_index : start_index + chunk_size]
