from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Any

from sqlalchemy import Select, select
from sqlalchemy.orm import Session

from app.db import (
    AssetKind,
    AssetStatus,
    AudioJob,
    CompositionSegment,
    CompositionSegmentAcceptanceState,
    JobStatus,
    SessionAsset,
    StorySession,
)
from app.db.base import utc_now
from app.repositories import SessionAggregate, StorySessionRepository
from app.storage import ObjectStorageService, StorageObjectLocation

ARTIFACT_RETENTION_POLICY_VERSION = "artifact_retention.v1"


@dataclass(frozen=True)
class ArtifactRetentionPolicy:
    inactive_draft_snapshot_ttl: timedelta = timedelta(days=14)
    superseded_composition_asset_ttl: timedelta = timedelta(days=14)
    old_audio_segment_ttl: timedelta = timedelta(days=14)
    superseded_export_ttl: timedelta = timedelta(days=30)


@dataclass(frozen=True)
class ArtifactCleanupTarget:
    location: StorageObjectLocation
    role: str


@dataclass(frozen=True)
class ArtifactCleanupCandidate:
    asset_id: str
    session_id: str
    asset_kind: AssetKind
    status: AssetStatus
    rule_key: str
    reason: str
    anchor_at: datetime
    expires_at: datetime
    targets: tuple[ArtifactCleanupTarget, ...]


@dataclass(frozen=True)
class ArtifactCleanupPlan:
    generated_at: datetime
    protected_asset_count: int
    candidates: tuple[ArtifactCleanupCandidate, ...]


@dataclass(frozen=True)
class ArtifactCleanupReport:
    generated_at: datetime
    dry_run: bool
    protected_asset_count: int
    candidate_count: int
    cleaned_asset_count: int
    deleted_object_count: int
    missing_object_count: int
    candidates: tuple[ArtifactCleanupCandidate, ...]


@dataclass(frozen=True)
class _SessionRetentionContext:
    aggregate: SessionAggregate
    protected_asset_ids: frozenset[str]
    protected_composition_segment_ids: frozenset[str]
    latest_audio_job_id: str | None
    latest_audio_asset_job_id: str | None
    composition_segments_by_id: dict[str, CompositionSegment]


class ArtifactRetentionService:
    def __init__(
        self,
        session: Session,
        *,
        object_storage: ObjectStorageService,
        policy: ArtifactRetentionPolicy | None = None,
    ) -> None:
        self._session = session
        self._sessions = StorySessionRepository(session)
        self._object_storage = object_storage
        self._policy = policy or ArtifactRetentionPolicy()

    def build_cleanup_plan(
        self,
        *,
        session_id: str | None = None,
        now: datetime | None = None,
        limit: int | None = None,
    ) -> ArtifactCleanupPlan:
        generated_at = now or utc_now()
        protected_asset_count = 0
        candidates: list[ArtifactCleanupCandidate] = []

        for current_session_id in self._list_session_ids(session_id=session_id):
            aggregate = self._sessions.get_aggregate(current_session_id)
            if aggregate is None:
                continue
            context = self._build_context(aggregate)
            protected_asset_count += len(context.protected_asset_ids)
            session_assets = self._list_session_assets(current_session_id)
            for asset in session_assets:
                candidate = self._build_candidate(
                    asset,
                    context=context,
                    now=generated_at,
                )
                if candidate is not None:
                    candidates.append(candidate)

        candidates.sort(key=lambda item: (item.expires_at, item.anchor_at, item.asset_id))
        if limit is not None:
            candidates = candidates[: max(limit, 0)]

        return ArtifactCleanupPlan(
            generated_at=generated_at,
            protected_asset_count=protected_asset_count,
            candidates=tuple(candidates),
        )

    def cleanup_expired_assets(
        self,
        *,
        session_id: str | None = None,
        now: datetime | None = None,
        dry_run: bool = True,
        limit: int | None = None,
        commit: bool = True,
    ) -> ArtifactCleanupReport:
        plan = self.build_cleanup_plan(session_id=session_id, now=now, limit=limit)

        if dry_run or not plan.candidates:
            return ArtifactCleanupReport(
                generated_at=plan.generated_at,
                dry_run=dry_run,
                protected_asset_count=plan.protected_asset_count,
                candidate_count=len(plan.candidates),
                cleaned_asset_count=0,
                deleted_object_count=0,
                missing_object_count=0,
                candidates=plan.candidates,
            )

        deleted_object_count = 0
        missing_object_count = 0
        cleaned_asset_count = 0

        for candidate in plan.candidates:
            asset = self._session.get(SessionAsset, candidate.asset_id)
            if asset is None:
                continue

            deleted_targets: list[dict[str, str]] = []
            missing_targets: list[dict[str, str]] = []

            for target in candidate.targets:
                deleted = self._object_storage.delete_object(target.location, missing_ok=True)
                target_record = {
                    "bucket": target.location.bucket,
                    "object_path": target.location.key,
                    "role": target.role,
                }
                if deleted:
                    deleted_object_count += 1
                    deleted_targets.append(target_record)
                else:
                    missing_object_count += 1
                    missing_targets.append(target_record)

            self._mark_asset_cleaned(
                asset,
                cleaned_at=plan.generated_at,
                candidate=candidate,
                deleted_targets=deleted_targets,
                missing_targets=missing_targets,
            )
            cleaned_asset_count += 1

        if commit:
            self._session.commit()
        else:
            self._session.flush()

        return ArtifactCleanupReport(
            generated_at=plan.generated_at,
            dry_run=False,
            protected_asset_count=plan.protected_asset_count,
            candidate_count=len(plan.candidates),
            cleaned_asset_count=cleaned_asset_count,
            deleted_object_count=deleted_object_count,
            missing_object_count=missing_object_count,
            candidates=plan.candidates,
        )

    def _build_context(self, aggregate: SessionAggregate) -> _SessionRetentionContext:
        protected_asset_ids: set[str] = set()
        protected_segment_ids: set[str] = set()

        for asset in (
            aggregate.latest_story_asset,
            aggregate.latest_story_export_asset,
            aggregate.latest_audio_asset,
        ):
            if asset is not None:
                protected_asset_ids.add(asset.id)

        if aggregate.latest_draft_snapshot_asset is not None and (
            aggregate.active_composition_job is not None or aggregate.latest_story_asset is None
        ):
            protected_asset_ids.add(aggregate.latest_draft_snapshot_asset.id)

        if aggregate.latest_audio_job is not None and aggregate.latest_audio_job.status in {
            JobStatus.QUEUED,
            JobStatus.IN_PROGRESS,
            JobStatus.PAUSED,
            JobStatus.FAILED,
        }:
            protected_asset_ids.update(asset.id for asset in aggregate.audio_segment_assets)

        composition_segments_by_id = {
            segment.id: segment for segment in aggregate.composition_segments
        }
        for segment in aggregate.composition_segments:
            if (
                segment.acceptance_state
                in {
                    CompositionSegmentAcceptanceState.ACCEPTED,
                    CompositionSegmentAcceptanceState.PENDING,
                }
                and segment.superseded_by_segment_id is None
            ):
                protected_segment_ids.add(segment.id)

        return _SessionRetentionContext(
            aggregate=aggregate,
            protected_asset_ids=frozenset(protected_asset_ids),
            protected_composition_segment_ids=frozenset(protected_segment_ids),
            latest_audio_job_id=(
                aggregate.latest_audio_job.id if aggregate.latest_audio_job is not None else None
            ),
            latest_audio_asset_job_id=(
                aggregate.latest_audio_asset.audio_job_id
                if aggregate.latest_audio_asset is not None
                else None
            ),
            composition_segments_by_id=composition_segments_by_id,
        )

    def _build_candidate(
        self,
        asset: SessionAsset,
        *,
        context: _SessionRetentionContext,
        now: datetime,
    ) -> ArtifactCleanupCandidate | None:
        if _asset_was_cleaned(asset):
            return None
        if asset.id in context.protected_asset_ids:
            return None
        if asset.status in {AssetStatus.PENDING, AssetStatus.IN_PROGRESS}:
            return None

        if asset.asset_kind == AssetKind.DRAFT_TEXT_SNAPSHOT:
            return self._build_draft_snapshot_candidate(asset, now=now)
        if asset.asset_kind == AssetKind.COMPOSITION_SEGMENT:
            return self._build_composition_segment_candidate(asset, context=context, now=now)
        if asset.asset_kind == AssetKind.AUDIO_SEGMENT:
            return self._build_audio_segment_candidate(asset, context=context, now=now)
        if asset.asset_kind in {AssetKind.STORY_TEXT, AssetKind.STORY_DOCX, AssetKind.FINAL_AUDIO}:
            return self._build_superseded_export_candidate(asset, now=now)
        return None

    def _build_draft_snapshot_candidate(
        self,
        asset: SessionAsset,
        *,
        now: datetime,
    ) -> ArtifactCleanupCandidate | None:
        if asset.status not in {AssetStatus.READY, AssetStatus.SUPERSEDED, AssetStatus.FAILED}:
            return None
        return self._build_timed_candidate(
            asset,
            rule_key="inactive_draft_snapshot",
            reason=(
                "Rolling draft snapshot exceeded the inactive-session retention window after a "
                "newer canonical story or session state took over."
            ),
            ttl=self._policy.inactive_draft_snapshot_ttl,
            now=now,
        )

    def _build_composition_segment_candidate(
        self,
        asset: SessionAsset,
        *,
        context: _SessionRetentionContext,
        now: datetime,
    ) -> ArtifactCleanupCandidate | None:
        linked_segment = (
            context.composition_segments_by_id.get(asset.composition_segment_id)
            if asset.composition_segment_id is not None
            else None
        )
        if (
            linked_segment is not None
            and linked_segment.id in context.protected_composition_segment_ids
        ):
            return None
        if (
            linked_segment is not None
            and linked_segment.acceptance_state == CompositionSegmentAcceptanceState.PENDING
        ):
            return None
        if linked_segment is None and asset.status != AssetStatus.SUPERSEDED:
            return None

        if (
            linked_segment is not None
            and linked_segment.acceptance_state == CompositionSegmentAcceptanceState.REJECTED
        ):
            reason = "Rejected rewrite revision exceeded the temporary comparison retention window."
        else:
            reason = "Superseded composition revision exceeded the temporary retention window."

        return self._build_timed_candidate(
            asset,
            rule_key="superseded_composition_revision",
            reason=reason,
            ttl=self._policy.superseded_composition_asset_ttl,
            now=now,
        )

    def _build_audio_segment_candidate(
        self,
        asset: SessionAsset,
        *,
        context: _SessionRetentionContext,
        now: datetime,
    ) -> ArtifactCleanupCandidate | None:
        if asset.audio_job_id is None:
            return None

        audio_job = self._session.get(AudioJob, asset.audio_job_id)
        if audio_job is None:
            return None
        if audio_job.status in {JobStatus.QUEUED, JobStatus.IN_PROGRESS, JobStatus.PAUSED}:
            return None
        if context.latest_audio_job_id == audio_job.id and audio_job.status == JobStatus.FAILED:
            return None
        if (
            context.latest_audio_job_id == audio_job.id
            and audio_job.status == JobStatus.COMPLETED
            and context.latest_audio_asset_job_id != audio_job.id
        ):
            return None

        return self._build_timed_candidate(
            asset,
            rule_key="old_audio_segment",
            reason=(
                "Old audio preview segment exceeded the retention window after its job finished "
                "or was replaced by a newer narration pass."
            ),
            ttl=self._policy.old_audio_segment_ttl,
            now=now,
        )

    def _build_superseded_export_candidate(
        self,
        asset: SessionAsset,
        *,
        now: datetime,
    ) -> ArtifactCleanupCandidate | None:
        if asset.status != AssetStatus.SUPERSEDED:
            return None
        return self._build_timed_candidate(
            asset,
            rule_key="superseded_export",
            reason=(
                "Superseded final export exceeded the conservative retention window and is no "
                "longer a canonical session output."
            ),
            ttl=self._policy.superseded_export_ttl,
            now=now,
        )

    def _build_timed_candidate(
        self,
        asset: SessionAsset,
        *,
        rule_key: str,
        reason: str,
        ttl: timedelta,
        now: datetime,
    ) -> ArtifactCleanupCandidate | None:
        anchor_at = _asset_anchor_at(asset)
        expires_at = anchor_at + ttl
        if expires_at > now:
            return None
        return ArtifactCleanupCandidate(
            asset_id=asset.id,
            session_id=asset.session_id,
            asset_kind=asset.asset_kind,
            status=asset.status,
            rule_key=rule_key,
            reason=reason,
            anchor_at=anchor_at,
            expires_at=expires_at,
            targets=self._build_cleanup_targets(asset),
        )

    def _build_cleanup_targets(self, asset: SessionAsset) -> tuple[ArtifactCleanupTarget, ...]:
        targets: list[ArtifactCleanupTarget] = [
            ArtifactCleanupTarget(
                location=StorageObjectLocation(
                    bucket=asset.storage_bucket,
                    key=asset.object_path,
                ),
                role="asset_payload",
            )
        ]

        if asset.asset_kind == AssetKind.FINAL_AUDIO:
            metadata = _read_mapping(asset.metadata_json)
            debug_metadata = _read_mapping(metadata.get("debug"))
            narration_master_bucket = _read_optional_text(
                debug_metadata.get("narration_master_bucket")
            )
            narration_master_object_path = _read_optional_text(
                debug_metadata.get("narration_master_object_path")
            )
            if narration_master_bucket and narration_master_object_path:
                targets.append(
                    ArtifactCleanupTarget(
                        location=StorageObjectLocation(
                            bucket=narration_master_bucket,
                            key=narration_master_object_path,
                        ),
                        role="narration_master_debug",
                    )
                )

        deduped: list[ArtifactCleanupTarget] = []
        seen_locations: set[tuple[str, str]] = set()
        for target in targets:
            location_key = (target.location.bucket, target.location.key)
            if location_key in seen_locations:
                continue
            seen_locations.add(location_key)
            deduped.append(target)
        return tuple(deduped)

    def _mark_asset_cleaned(
        self,
        asset: SessionAsset,
        *,
        cleaned_at: datetime,
        candidate: ArtifactCleanupCandidate,
        deleted_targets: list[dict[str, str]],
        missing_targets: list[dict[str, str]],
    ) -> None:
        metadata = _read_mapping(asset.metadata_json)
        metadata["retention_cleanup"] = {
            "policy_version": ARTIFACT_RETENTION_POLICY_VERSION,
            "deleted_at": cleaned_at.isoformat(),
            "rule_key": candidate.rule_key,
            "reason": candidate.reason,
            "deleted_objects": deleted_targets,
            "missing_objects": missing_targets,
        }
        asset.metadata_json = metadata
        if asset.status == AssetStatus.READY:
            asset.status = AssetStatus.SUPERSEDED
            asset.superseded_at = cleaned_at

    def _list_session_ids(self, *, session_id: str | None = None) -> list[str]:
        stmt: Select[tuple[str]] = select(StorySession.id).order_by(
            StorySession.updated_at.desc(),
            StorySession.created_at.desc(),
        )
        if session_id is not None:
            stmt = stmt.where(StorySession.id == session_id)
        return list(self._session.execute(stmt).scalars().all())

    def _list_session_assets(self, session_id: str) -> list[SessionAsset]:
        stmt: Select[tuple[SessionAsset]] = (
            select(SessionAsset)
            .where(SessionAsset.session_id == session_id)
            .order_by(
                SessionAsset.created_at.asc(),
                SessionAsset.ready_at.asc(),
                SessionAsset.id.asc(),
            )
        )
        return list(self._session.execute(stmt).scalars().all())


def _asset_anchor_at(asset: SessionAsset) -> datetime:
    return (
        asset.superseded_at
        or asset.failed_at
        or asset.ready_at
        or asset.updated_at
        or asset.created_at
    )


def _asset_was_cleaned(asset: SessionAsset) -> bool:
    cleanup = _read_mapping(asset.metadata_json).get("retention_cleanup")
    if not isinstance(cleanup, Mapping):
        return False
    deleted_at = cleanup.get("deleted_at")
    return isinstance(deleted_at, str) and bool(deleted_at.strip())


def _read_mapping(value: Any) -> dict[str, Any]:
    return dict(value) if isinstance(value, Mapping) else {}


def _read_optional_text(value: Any) -> str | None:
    if value is None:
        return None
    normalized = str(value).strip()
    return normalized or None
