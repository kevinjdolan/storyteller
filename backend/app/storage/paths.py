from __future__ import annotations

import re
from dataclasses import dataclass

from app.settings import AppSettings
from app.storage.models import StorageObjectLocation

_INVALID_COMPONENT_PATTERN = re.compile(r"[^A-Za-z0-9._-]+")


def _normalize_component(value: str, *, label: str) -> str:
    normalized = _INVALID_COMPONENT_PATTERN.sub("-", value.strip()).strip(".-_")

    if not normalized:
        raise ValueError(f"{label} must not be empty")

    return normalized


def _normalize_extension(extension: str | None) -> str:
    if extension is None:
        return ""

    normalized = _normalize_component(extension.lstrip("."), label="extension")
    return f".{normalized}"


def _format_segment_index(segment_index: int) -> str:
    if segment_index < 0:
        raise ValueError("segment_index must be greater than or equal to zero")

    return f"{segment_index:04d}"


@dataclass(frozen=True)
class SessionArtifactStoragePaths:
    sessions_bucket: str
    audio_bucket: str
    exports_bucket: str

    @classmethod
    def from_settings(cls, settings: AppSettings) -> "SessionArtifactStoragePaths":
        bucket_names = settings.gcs_bucket_names
        return cls(
            sessions_bucket=bucket_names.sessions,
            audio_bucket=bucket_names.audio,
            exports_bucket=bucket_names.exports,
        )

    def bucket_names(self) -> tuple[str, ...]:
        return (
            self.sessions_bucket,
            self.audio_bucket,
            self.exports_bucket,
        )

    def partial_draft_segment(
        self,
        *,
        session_id: str,
        job_id: str,
        segment_index: int,
        extension: str = "md",
    ) -> StorageObjectLocation:
        return StorageObjectLocation(
            bucket=self.sessions_bucket,
            key=(
                f"{self._session_prefix(session_id)}/composition/jobs/"
                f"{self._component(job_id, label='job_id')}/segments/"
                f"{_format_segment_index(segment_index)}{_normalize_extension(extension)}"
            ),
        )

    def audio_segment(
        self,
        *,
        session_id: str,
        job_id: str,
        segment_index: int,
        extension: str = "mp3",
    ) -> StorageObjectLocation:
        return StorageObjectLocation(
            bucket=self.audio_bucket,
            key=(
                f"{self._session_prefix(session_id)}/audio/jobs/"
                f"{self._component(job_id, label='job_id')}/segments/"
                f"{_format_segment_index(segment_index)}{_normalize_extension(extension)}"
            ),
        )

    def final_audio(
        self,
        *,
        session_id: str,
        job_id: str,
        extension: str = "mp3",
        file_stem: str = "story",
    ) -> StorageObjectLocation:
        return StorageObjectLocation(
            bucket=self.audio_bucket,
            key=(
                f"{self._session_prefix(session_id)}/audio/jobs/"
                f"{self._component(job_id, label='job_id')}/final/"
                f"{self._component(file_stem, label='file_stem')}{_normalize_extension(extension)}"
            ),
        )

    def export_asset(
        self,
        *,
        session_id: str,
        export_kind: str,
        export_id: str,
        extension: str,
    ) -> StorageObjectLocation:
        return StorageObjectLocation(
            bucket=self.exports_bucket,
            key=(
                f"{self._session_prefix(session_id)}/exports/"
                f"{self._component(export_kind, label='export_kind')}/"
                f"{self._component(export_id, label='export_id')}{_normalize_extension(extension)}"
            ),
        )

    def debug_artifact(
        self,
        *,
        session_id: str,
        artifact_group: str,
        artifact_name: str,
        extension: str | None = None,
    ) -> StorageObjectLocation:
        return StorageObjectLocation(
            bucket=self.sessions_bucket,
            key=(
                f"{self._session_prefix(session_id)}/debug/"
                f"{self._component(artifact_group, label='artifact_group')}/"
                f"{self._component(artifact_name, label='artifact_name')}"
                f"{_normalize_extension(extension)}"
            ),
        )

    def _session_prefix(self, session_id: str) -> str:
        return f"sessions/{self._component(session_id, label='session_id')}"

    def _component(self, value: str, *, label: str) -> str:
        return _normalize_component(value, label=label)
