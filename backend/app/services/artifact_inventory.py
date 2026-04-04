from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from sqlalchemy.orm import Session

from app.db import AssetKind, AssetStatus, JobStatus, SessionAsset
from app.db.base import utc_now
from app.models import SessionArtifactInventoryItemView, SessionArtifactInventoryView
from app.repositories import SessionAggregate, SessionAssetRepository, StorySessionRepository
from app.services.asset_access import (
    SessionArtifactHandle,
    build_named_session_artifact_path,
)
from app.services.session_hydration import build_session_asset_view

_ACTIVE_JOB_STATUSES = {
    JobStatus.QUEUED,
    JobStatus.IN_PROGRESS,
    JobStatus.PAUSED,
}
_FAILED_JOB_STATUSES = {
    JobStatus.FAILED,
    JobStatus.CANCELLED,
}
_PREVIEW_ASSET_LIMIT = 3


class SessionArtifactInventoryError(Exception):
    """Base error for session artifact inventory lookups."""


class SessionArtifactInventoryNotFoundError(SessionArtifactInventoryError):
    """Raised when the target story session does not exist."""


class SessionArtifactInventoryService:
    def __init__(self, session: Session) -> None:
        self._session = session
        self._sessions = StorySessionRepository(session)
        self._assets = SessionAssetRepository(session)

    def load_inventory(self, session_id: str) -> SessionArtifactInventoryView:
        aggregate = self._sessions.get_aggregate(session_id)
        if aggregate is None:
            raise SessionArtifactInventoryNotFoundError(
                f"session {session_id!r} was not found"
            )

        return SessionArtifactInventoryView(
            session_id=session_id,
            generated_at=utc_now(),
            items=[
                self._build_story_text_item(aggregate),
                self._build_story_docx_item(aggregate),
                self._build_final_audio_item(aggregate),
            ],
        )

    def _build_story_text_item(
        self,
        aggregate: SessionAggregate,
    ) -> SessionArtifactInventoryItemView:
        story_asset = aggregate.latest_story_asset
        display_job = aggregate.active_composition_job or aggregate.latest_composition_job

        status = "missing"
        status_detail = (
            "The accepted manuscript has not been published into durable storage yet."
        )
        download_path = None
        stream_path = None

        if story_asset is not None:
            status = "ready"
            status_detail = (
                "The accepted manuscript is stored and ready for in-app reading or download."
            )
            download_path = build_named_session_artifact_path(
                session_id=aggregate.session.id,
                artifact_handle=SessionArtifactHandle.STORY_TEXT,
                disposition="attachment",
            )
            stream_path = build_named_session_artifact_path(
                session_id=aggregate.session.id,
                artifact_handle=SessionArtifactHandle.STORY_TEXT,
                disposition="inline",
            )
        elif display_job is not None and display_job.status in _ACTIVE_JOB_STATUSES:
            status = "generating"
            status_detail = (
                display_job.current_step
                or "The manuscript is still being assembled from accepted composition segments."
            )
        elif display_job is not None and display_job.status in _FAILED_JOB_STATUSES:
            status = "failed"
            status_detail = (
                display_job.error_message
                or display_job.stop_reason
                or "The last manuscript publish did not complete."
            )

        return SessionArtifactInventoryItemView(
            key="story_text",
            label="Final story text",
            artifact_kind=AssetKind.STORY_TEXT.value,
            status=status,
            status_detail=status_detail,
            asset=build_session_asset_view(story_asset),
            download_path=download_path,
            stream_path=stream_path,
        )

    def _build_story_docx_item(
        self,
        aggregate: SessionAggregate,
    ) -> SessionArtifactInventoryItemView:
        story_asset = aggregate.latest_story_asset
        docx_asset = self._latest_asset(
            aggregate.session.id,
            asset_kind=AssetKind.STORY_DOCX,
        )

        status = "missing"
        status_detail = (
            "The Word export will unlock after the accepted manuscript is published."
        )
        download_path = None

        if story_asset is not None:
            download_path = build_named_session_artifact_path(
                session_id=aggregate.session.id,
                artifact_handle=SessionArtifactHandle.STORY_DOCX,
                disposition="attachment",
            )
            if docx_asset is None:
                status_detail = (
                    "No Word export has been packaged yet. Generate one from the current story."
                )
            elif docx_asset.status in _ACTIVE_JOB_STATUSES:
                status = "generating"
                status_detail = (
                    "The Word export is packaging now from the current accepted manuscript."
                )
            elif docx_asset.status == AssetStatus.FAILED:
                status = "failed"
                status_detail = (
                    docx_asset.error_message
                    or "The last Word export attempt failed before the file was published."
                )
            elif _docx_matches_story_asset(docx_asset, story_asset):
                status = "ready"
                status_detail = (
                    "This Word export matches the latest accepted manuscript."
                )
            else:
                status = "stale"
                status_detail = (
                    "The manuscript changed after the last Word export. Refresh it before "
                    "sharing or downloading."
                )

        return SessionArtifactInventoryItemView(
            key="story_docx",
            label="Word document",
            artifact_kind=AssetKind.STORY_DOCX.value,
            status=status,
            status_detail=status_detail,
            asset=build_session_asset_view(docx_asset),
            download_path=download_path,
        )

    def _build_final_audio_item(
        self,
        aggregate: SessionAggregate,
    ) -> SessionArtifactInventoryItemView:
        final_audio_asset = aggregate.latest_audio_asset
        display_job = aggregate.active_audio_job or aggregate.latest_audio_job
        ready_preview_assets = [
            asset
            for asset in aggregate.audio_segment_assets
            if asset.status == AssetStatus.READY
        ]
        preview_asset_views = [
            view
            for view in (
                build_session_asset_view(asset)
                for asset in ready_preview_assets[:_PREVIEW_ASSET_LIMIT]
            )
            if view is not None
        ]

        status = "missing"
        status_detail = (
            "No compiled narration master has been published for this session yet."
        )
        download_path = None
        stream_path = None

        if final_audio_asset is None:
            if display_job is not None and display_job.status in _ACTIVE_JOB_STATUSES:
                status = "generating"
                status_detail = _build_generating_audio_detail(
                    _read_audio_job_step(display_job),
                    preview_asset_count=len(ready_preview_assets),
                )
            elif display_job is not None and display_job.status in _FAILED_JOB_STATUSES:
                status = "failed"
                status_detail = (
                    display_job.error_message
                    or display_job.stop_reason
                    or "The latest narration pass stopped before a master was published."
                )
            elif display_job is not None and display_job.status == JobStatus.COMPLETED:
                status_detail = (
                    "The latest narration pass completed without publishing a compiled master."
                )
        else:
            download_path = build_named_session_artifact_path(
                session_id=aggregate.session.id,
                artifact_handle=SessionArtifactHandle.FINAL_AUDIO,
                disposition="attachment",
            )
            stream_path = build_named_session_artifact_path(
                session_id=aggregate.session.id,
                artifact_handle=SessionArtifactHandle.FINAL_AUDIO,
                disposition="inline",
            )

            if (
                display_job is not None
                and final_audio_asset.audio_job_id is not None
                and final_audio_asset.audio_job_id != display_job.id
            ):
                status = "stale"
                status_detail = _build_replacement_audio_detail(display_job.status)
            elif _audio_asset_is_outdated(
                final_audio_asset,
                aggregate.latest_story_asset,
            ):
                status = "stale"
                status_detail = (
                    "The manuscript changed after this narration master was published. "
                    "Run audio again to catch up."
                )
            else:
                status = "ready"
                status_detail = (
                    "The compiled narration master matches the latest published session state."
                )

        return SessionArtifactInventoryItemView(
            key="final_audio",
            label="Final narration",
            artifact_kind=AssetKind.FINAL_AUDIO.value,
            status=status,
            status_detail=status_detail,
            asset=build_session_asset_view(final_audio_asset),
            preview_assets=preview_asset_views,
            preview_asset_count=len(ready_preview_assets),
            download_path=download_path,
            stream_path=stream_path,
        )

    def _latest_asset(self, session_id: str, *, asset_kind: AssetKind) -> SessionAsset | None:
        assets = self._assets.list_for_session(
            session_id,
            asset_kinds=(asset_kind,),
            include_superseded=True,
        )
        return assets[0] if assets else None


def _docx_matches_story_asset(docx_asset: SessionAsset, story_asset: SessionAsset) -> bool:
    if docx_asset.status != AssetStatus.READY:
        return False

    metadata = _read_mapping(docx_asset.metadata_json)
    return metadata.get("source_story_asset_id") == story_asset.id


def _audio_asset_is_outdated(
    audio_asset: SessionAsset,
    story_asset: SessionAsset | None,
) -> bool:
    if story_asset is None:
        return False

    generation = _read_nested_mapping(_read_mapping(audio_asset.metadata_json), "generation")
    source_composition_job_id = _read_optional_text(
        generation.get("source_composition_job_id")
    )
    if (
        story_asset.composition_job_id is not None
        and source_composition_job_id is not None
        and story_asset.composition_job_id != source_composition_job_id
    ):
        return True

    if (
        story_asset.ready_at is not None
        and audio_asset.ready_at is not None
        and story_asset.ready_at > audio_asset.ready_at
    ):
        return True

    return False


def _build_generating_audio_detail(
    current_step: str | None,
    *,
    preview_asset_count: int,
) -> str:
    base_detail = current_step or "Narration is rendering segment by segment."
    if preview_asset_count <= 0:
        return base_detail
    suffix = (
        "One preview clip is already available."
        if preview_asset_count == 1
        else f"{preview_asset_count} preview clips are already available."
    )
    return f"{base_detail} {suffix}"


def _build_replacement_audio_detail(status: JobStatus) -> str:
    if status in _ACTIVE_JOB_STATUSES:
        return (
            "A newer narration pass is still running. The previous published master "
            "remains available in the meantime."
        )
    if status in _FAILED_JOB_STATUSES:
        return (
            "The latest narration attempt stopped, but the previous published master "
            "is still available."
        )
    return (
        "A newer narration pass has not published a replacement master yet, so the "
        "previous master is still the downloadable version."
    )


def _read_mapping(value: Any) -> dict[str, Any]:
    return dict(value) if isinstance(value, Mapping) else {}


def _read_nested_mapping(value: Mapping[str, Any], key: str) -> dict[str, Any]:
    nested = value.get(key)
    return dict(nested) if isinstance(nested, Mapping) else {}


def _read_optional_text(value: Any) -> str | None:
    if not isinstance(value, str):
        return None
    normalized = value.strip()
    return normalized or None


def _read_audio_job_step(job) -> str | None:
    return _read_optional_text(_read_mapping(job.config_json).get("current_step"))
