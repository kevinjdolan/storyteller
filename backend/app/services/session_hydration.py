from __future__ import annotations

from collections.abc import Mapping
from datetime import datetime
from typing import Any

import httpx
from sqlalchemy.orm import Session

from app.db import (
    AudioJob,
    CompositionInterruptionRequest,
    CompositionInterruptionState,
    CompositionJob,
    JobStatus,
    NarrationSegment,
    SessionAsset,
)
from app.models import (
    SAVE_THE_CAT_BEAT_LABELS,
    SAVE_THE_CAT_BEAT_SEQUENCE,
    WORKFLOW_STAGE_SEQUENCE,
    AudioJobView,
    AudioProgressEventPayload,
    BeatSheetBeatView,
    BeatSheetEditView,
    BeatSheetView,
    CharacterProfileView,
    CharacterSheetBatchView,
    CharacterSheetView,
    CompositionInterruptionRequestView,
    CompositionJobView,
    CompositionProgressEventPayload,
    CompositionSegmentVersionView,
    CompositionSegmentView,
    ContinuityBibleData,
    ContinuityBibleView,
    ContinuityFact,
    ConversationMemorySnapshotView,
    NarrationSegmentView,
    NormalizedBriefPreferences,
    PitchBatchView,
    PitchView,
    PlanArtifactRefView,
    PlanRevisionView,
    RecentSessionSummary,
    SessionAssetView,
    SessionCatalogSelection,
    SessionEventType,
    SessionHydrationMetadata,
    SessionHydrationView,
    SessionProgress,
    SessionSnapshot,
    SessionStageStateView,
    SessionUsageSummaryView,
    StoryBriefView,
    StoryOutlineCard,
    StoryOutlineEditView,
    StoryOutlineView,
    StorySetupView,
    WorkflowStage,
    WorkflowStageChangedEventPayload,
    WorkflowStageState,
    get_workflow_stage_definition,
    resolve_resume_stage,
)
from app.models.composition_interruptions import build_composition_interruption_message
from app.repositories import SessionAggregate, StorySessionRepository
from app.services.agent_context import build_session_agent_context_summary
from app.services.asset_access import build_session_asset_access_view
from app.services.audio_settings import build_audio_settings_view
from app.services.conversation_memory import SessionMemoryService
from app.services.event_log import SessionEventLogService
from app.services.model_usage import SessionModelUsageService
from app.settings import get_settings
from app.storage import (
    ObjectNotFoundError,
    ObjectStorageService,
    StorageError,
    StorageObjectLocation,
    build_object_storage_service,
)

_ACTIVE_JOB_STATUS_VALUES = {
    JobStatus.QUEUED.value,
    JobStatus.IN_PROGRESS.value,
    JobStatus.PAUSED.value,
}


class SessionHydrationServiceError(Exception):
    """Base error for session hydration failures."""


class SessionHydrationNotFoundError(SessionHydrationServiceError):
    """Raised when a requested session cannot be hydrated."""


class SessionHydrationService:
    def __init__(
        self,
        session: Session,
        *,
        object_storage: ObjectStorageService | None = None,
    ):
        self._session = session
        self._sessions = StorySessionRepository(session)
        self._memory = SessionMemoryService(session)
        self._events = SessionEventLogService(session)
        self._object_storage = object_storage

    def load_session_snapshot(self, session_id: str) -> SessionSnapshot:
        aggregate = self._sessions.get_aggregate(session_id)
        if aggregate is None:
            raise SessionHydrationNotFoundError(f"session {session_id!r} was not found")

        snapshot = build_session_snapshot(
            aggregate,
            conversation_memory=self._memory.load_latest_snapshot(session_id),
            usage_summary=SessionModelUsageService(self._session).load_session_summary(session_id),
        )
        self._apply_draft_snapshot_fallback(snapshot, aggregate.latest_draft_snapshot_asset)
        return snapshot

    def hydrate_session(
        self,
        session_id: str,
        *,
        history_limit: int = 40,
    ) -> SessionHydrationView:
        if history_limit <= 0:
            raise ValueError("history_limit must be greater than zero")

        aggregate = self._sessions.get_aggregate(session_id)
        if aggregate is None:
            raise SessionHydrationNotFoundError(f"session {session_id!r} was not found")

        conversation_memory = self._memory.load_latest_snapshot(session_id)
        base_snapshot = build_session_snapshot(
            aggregate,
            conversation_memory=conversation_memory,
            usage_summary=SessionModelUsageService(self._session).load_session_summary(session_id),
        )
        self._apply_draft_snapshot_fallback(
            base_snapshot,
            aggregate.latest_draft_snapshot_asset,
        )
        recent_history = self._events.list_session_history(session_id, limit=history_limit)
        materialized_sequence = resolve_materialized_sequence_number(
            aggregate,
            conversation_memory=conversation_memory,
        )
        replay_events = select_replay_events(
            recent_history.events,
            materialized_sequence_number=materialized_sequence,
        )
        hydrated_snapshot, replayed_event_count = replay_session_snapshot(
            base_snapshot,
            replay_events,
        )
        hydrated_snapshot.agent_context_summary = build_session_agent_context_summary(
            hydrated_snapshot,
            use_conversation_memory=False,
        )

        first_history_sequence = (
            recent_history.events[0].sequence_number if recent_history.events else None
        )
        latest_sequence_number = recent_history.latest_sequence_number
        replay_from_sequence_number = None
        if latest_sequence_number is not None:
            if materialized_sequence is None:
                replay_from_sequence_number = first_history_sequence
            elif latest_sequence_number > materialized_sequence:
                replay_from_sequence_number = materialized_sequence + 1

        return SessionHydrationView(
            snapshot=hydrated_snapshot,
            recent_history=recent_history,
            hydration=SessionHydrationMetadata(
                strategy=(
                    "materialized_with_recent_replay"
                    if replayed_event_count > 0
                    else "materialized_only"
                ),
                materialized_through_sequence_number=materialized_sequence,
                replay_from_sequence_number=replay_from_sequence_number,
                replayed_event_count=replayed_event_count,
                latest_sequence_number=latest_sequence_number,
                history_event_count=len(recent_history.events),
                history_window_truncated=(
                    first_history_sequence is not None and first_history_sequence > 1
                ),
            ),
        )

    def _apply_draft_snapshot_fallback(
        self,
        snapshot: SessionSnapshot,
        draft_snapshot_asset: SessionAsset | None,
    ) -> None:
        target_fields = [
            field_name
            for field_name in ("active_composition_job", "latest_composition_job")
            if _job_needs_draft_snapshot_fallback(
                getattr(snapshot, field_name),
                draft_snapshot_asset,
            )
        ]
        if not target_fields or draft_snapshot_asset is None:
            return

        draft_text = self._load_draft_snapshot_text(draft_snapshot_asset)
        if draft_text is None:
            return

        for field_name in target_fields:
            current_job = getattr(snapshot, field_name)
            if current_job is None:
                continue
            setattr(
                snapshot,
                field_name,
                current_job.model_copy(
                    update={
                        "accepted_story_so_far": (
                            current_job.accepted_story_so_far or draft_text
                        ),
                        "latest_partial_output": (
                            current_job.latest_partial_output or draft_text
                        ),
                    }
                ),
            )

    def _load_draft_snapshot_text(self, draft_snapshot_asset: SessionAsset) -> str | None:
        try:
            return self._storage().download_text(
                StorageObjectLocation(
                    bucket=draft_snapshot_asset.storage_bucket,
                    key=draft_snapshot_asset.object_path,
                )
            )
        except (ObjectNotFoundError, StorageError, httpx.HTTPError):
            return None

    def _storage(self) -> ObjectStorageService:
        if self._object_storage is None:
            self._object_storage = build_object_storage_service(get_settings())
        return self._object_storage


def build_recent_session_summary(story_session) -> RecentSessionSummary:
    return RecentSessionSummary(
        id=story_session.id,
        display_title=resolve_display_title(working_title=story_session.working_title),
        working_title=story_session.working_title,
        current_stage=story_session.current_stage,
        resume_stage=story_session.resume_stage,
        furthest_completed_stage=story_session.furthest_completed_stage,
        overall_status=story_session.overall_status,
        created_at=story_session.created_at,
        updated_at=story_session.updated_at,
        completed_at=story_session.completed_at,
        selected_genre=build_catalog_selection(story_session.selected_genre),
        selected_tone_profile=build_catalog_selection(story_session.selected_tone_profile),
        progress=build_progress(story_session.workflow_stage_states),
    )


def build_session_snapshot(
    aggregate: SessionAggregate,
    *,
    conversation_memory: ConversationMemorySnapshotView | None,
    usage_summary: SessionUsageSummaryView,
) -> SessionSnapshot:
    story_session = aggregate.session
    plan_revision_views = build_plan_revision_views(aggregate.plan_revisions)
    current_plan_revision_view = next(
        (revision for revision in plan_revision_views if revision.is_current),
        None,
    )
    snapshot = SessionSnapshot(
        id=story_session.id,
        display_title=resolve_display_title(
            working_title=story_session.working_title,
            pitch_title=aggregate.selected_pitch.title if aggregate.selected_pitch else None,
            story_idea=(
                aggregate.active_story_brief.story_idea if aggregate.active_story_brief else None
            ),
            normalized_summary=(
                aggregate.active_story_brief.normalized_summary
                if aggregate.active_story_brief
                else None
            ),
            raw_brief=(
                aggregate.active_story_brief.raw_brief if aggregate.active_story_brief else None
            ),
        ),
        working_title=story_session.working_title,
        current_stage=story_session.current_stage,
        resume_stage=story_session.resume_stage,
        furthest_completed_stage=story_session.furthest_completed_stage,
        overall_status=story_session.overall_status,
        created_at=story_session.created_at,
        updated_at=story_session.updated_at,
        completed_at=story_session.completed_at,
        selected_genre=build_catalog_selection(story_session.selected_genre),
        selected_tone_profile=build_catalog_selection(story_session.selected_tone_profile),
        progress=build_progress(story_session.workflow_stage_states),
        stage_states=build_stage_state_views(story_session.workflow_stage_states),
        story_brief=build_story_brief_view(aggregate.active_story_brief),
        pitch_batches=build_pitch_batch_views(aggregate.pitches),
        selected_pitch=build_pitch_view(aggregate.selected_pitch),
        character_sheet_batches=build_character_sheet_batch_views(aggregate.character_sheets),
        selected_character_sheet=build_character_sheet_view(aggregate.selected_character_sheet),
        beat_sheet_revisions=build_beat_sheet_views(aggregate.beat_sheets),
        selected_beat_sheet=build_beat_sheet_view(aggregate.selected_beat_sheet),
        selected_story_setup=build_story_setup_view(aggregate.selected_story_setup),
        story_outline_revisions=build_story_outline_views(aggregate.story_outlines),
        selected_story_outline=build_story_outline_view(aggregate.selected_story_outline),
        plan_revisions=plan_revision_views,
        current_plan_revision=current_plan_revision_view,
        latest_composition_job=build_composition_job_view(aggregate.latest_composition_job),
        latest_audio_job=build_audio_job_view(aggregate.latest_audio_job),
        active_composition_job=build_composition_job_view(aggregate.active_composition_job),
        active_audio_job=build_audio_job_view(aggregate.active_audio_job),
        composition_segments=build_composition_segment_views(aggregate.composition_segments),
        audio_segments=build_narration_segment_views(
            aggregate.audio_segments,
            aggregate.audio_segment_assets,
        ),
        latest_story_asset=build_session_asset_view(aggregate.latest_story_asset),
        latest_audio_asset=build_session_asset_view(aggregate.latest_audio_asset),
        audio_settings=build_audio_settings_view(
            story_session=story_session,
            latest_audio_job=aggregate.latest_audio_job,
            composition_segments=aggregate.composition_segments,
            selected_story_setup=aggregate.selected_story_setup,
            selected_story_outline=aggregate.selected_story_outline,
        ),
        continuity_bible=build_continuity_bible_view(aggregate.selected_continuity_bible),
        usage_summary=usage_summary,
        conversation_memory=conversation_memory,
    )
    snapshot.agent_context_summary = build_session_agent_context_summary(
        snapshot,
        use_conversation_memory=False,
    )
    return snapshot


def resolve_materialized_sequence_number(
    aggregate: SessionAggregate,
    *,
    conversation_memory: ConversationMemorySnapshotView | None,
) -> int | None:
    sequence_numbers = [
        stage_state.last_event.sequence_number
        for stage_state in aggregate.session.workflow_stage_states
        if getattr(stage_state, "last_event", None) is not None
    ]

    return max(sequence_numbers) if sequence_numbers else None


def select_replay_events(
    events,
    *,
    materialized_sequence_number: int | None,
):
    if materialized_sequence_number is None:
        return [
            event
            for event in events
            if event.event_type
            in {
                SessionEventType.WORKFLOW_STAGE_CHANGED.value,
                SessionEventType.COMPOSITION_PROGRESS_RECORDED.value,
                SessionEventType.AUDIO_PROGRESS_RECORDED.value,
            }
        ]

    return [
        event
        for event in events
        if event.sequence_number > materialized_sequence_number
        and event.event_type
        in {
            SessionEventType.WORKFLOW_STAGE_CHANGED.value,
            SessionEventType.COMPOSITION_PROGRESS_RECORDED.value,
            SessionEventType.AUDIO_PROGRESS_RECORDED.value,
        }
    ]


def replay_session_snapshot(
    snapshot: SessionSnapshot,
    events,
):
    if not events:
        return snapshot, 0

    hydrated = snapshot.model_copy(deep=True)
    replayed_event_count = 0

    for event in events:
        applied = False
        if event.event_type == SessionEventType.WORKFLOW_STAGE_CHANGED.value and isinstance(
            event.payload, WorkflowStageChangedEventPayload
        ):
            apply_workflow_stage_changed_event(hydrated, event)
            applied = True
        elif (
            event.event_type == SessionEventType.COMPOSITION_PROGRESS_RECORDED.value
            and isinstance(event.payload, CompositionProgressEventPayload)
        ):
            apply_job_progress_event(
                hydrated,
                stage=WorkflowStage.COMPOSITION,
                job_kind="composition",
                payload=event.payload,
                event_created_at=event.created_at,
                event_summary=event.summary,
            )
            applied = True
        elif event.event_type == SessionEventType.AUDIO_PROGRESS_RECORDED.value and isinstance(
            event.payload, AudioProgressEventPayload
        ):
            apply_job_progress_event(
                hydrated,
                stage=WorkflowStage.AUDIO,
                job_kind="audio",
                payload=event.payload,
                event_created_at=event.created_at,
                event_summary=event.summary,
            )
            applied = True

        if applied:
            replayed_event_count += 1

    hydrated.progress = build_progress(hydrated.stage_states)
    recompute_rollups(hydrated)
    return hydrated, replayed_event_count


def apply_workflow_stage_changed_event(snapshot: SessionSnapshot, event) -> None:
    payload = event.payload
    if not isinstance(payload, WorkflowStageChangedEventPayload) or event.stage is None:
        return

    for index, stage_state in enumerate(snapshot.stage_states):
        if stage_state.stage == event.stage and is_event_newer(
            stage_state.last_event_at,
            event.created_at,
        ):
            started_at = stage_state.started_at
            if payload.status in {
                WorkflowStageState.IN_PROGRESS,
                WorkflowStageState.COMPLETED,
            }:
                started_at = started_at or event.created_at
            completed_at = stage_state.completed_at
            if payload.status == WorkflowStageState.COMPLETED:
                completed_at = completed_at or event.created_at
            elif payload.status != WorkflowStageState.COMPLETED:
                completed_at = None

            snapshot.stage_states[index] = stage_state.model_copy(
                update={
                    "status": payload.status,
                    "detail": payload.detail if payload.detail is not None else stage_state.detail,
                    "started_at": started_at,
                    "completed_at": completed_at,
                    "last_event_summary": event.summary,
                    "last_event_type": event.event_type,
                    "last_event_at": event.created_at,
                }
            )
            continue

        if stage_state.stage in payload.invalidated_stages and is_event_newer(
            stage_state.last_event_at, event.created_at
        ):
            snapshot.stage_states[index] = stage_state.model_copy(
                update={
                    "status": WorkflowStageState.NEEDS_REGENERATION,
                    "last_event_summary": event.summary,
                    "last_event_type": event.event_type,
                    "last_event_at": event.created_at,
                }
            )

    snapshot.current_stage = payload.current_stage
    snapshot.resume_stage = payload.resume_stage
    snapshot.furthest_completed_stage = payload.furthest_completed_stage
    snapshot.overall_status = payload.overall_status
    if is_event_newer(snapshot.updated_at, event.created_at):
        snapshot.updated_at = event.created_at


def apply_job_progress_event(
    snapshot: SessionSnapshot,
    *,
    stage: WorkflowStage,
    job_kind: str,
    payload: CompositionProgressEventPayload | AudioProgressEventPayload,
    event_created_at: datetime,
    event_summary: str,
) -> None:
    if job_kind == "composition":
        latest_job = merge_composition_job_view(
            snapshot.latest_composition_job,
            payload,
            event_created_at=event_created_at,
        )
        snapshot.latest_composition_job = latest_job
        if latest_job is not None and latest_job.status in _ACTIVE_JOB_STATUS_VALUES:
            snapshot.active_composition_job = latest_job
        elif (
            snapshot.active_composition_job is not None
            and snapshot.active_composition_job.id == payload.job_id
        ):
            snapshot.active_composition_job = None
        job_detail = build_composition_job_detail(
            latest_job,
            fallback_summary=event_summary,
        )
    else:
        latest_job = merge_audio_job_view(
            snapshot.latest_audio_job,
            payload,
            event_created_at=event_created_at,
        )
        snapshot.latest_audio_job = latest_job
        if latest_job is not None and latest_job.status in _ACTIVE_JOB_STATUS_VALUES:
            snapshot.active_audio_job = latest_job
        elif (
            snapshot.active_audio_job is not None and snapshot.active_audio_job.id == payload.job_id
        ):
            snapshot.active_audio_job = None
        job_detail = build_audio_job_detail(
            latest_job,
            fallback_summary=event_summary,
        )

    update_stage_state_from_job(
        snapshot,
        stage=stage,
        status_value=payload.status,
        detail=job_detail,
        event_created_at=event_created_at,
        event_type=(
            SessionEventType.COMPOSITION_PROGRESS_RECORDED.value
            if job_kind == "composition"
            else SessionEventType.AUDIO_PROGRESS_RECORDED.value
        ),
        event_summary=event_summary,
    )

    if is_event_newer(snapshot.updated_at, event_created_at):
        snapshot.updated_at = event_created_at


def merge_composition_job_view(
    current_job: CompositionJobView | None,
    payload: CompositionProgressEventPayload,
    *,
    event_created_at: datetime,
) -> CompositionJobView | None:
    if current_job is not None and current_job.id != payload.job_id:
        if normalize_sortable_datetime(current_job.updated_at) > normalize_sortable_datetime(
            event_created_at
        ):
            return current_job
        current_job = None

    progress_percent = (
        payload.progress_percent
        if payload.progress_percent is not None
        else current_job.progress_percent
        if current_job is not None
        else 0
    )
    interruption_request = (
        payload.interruption_request
        if payload.interruption_request is not None
        else (current_job.interruption_request if current_job is not None else None)
    )
    if interruption_request is not None and interruption_request.state in {"applied", "superseded"}:
        interruption_request = None
    return CompositionJobView(
        id=payload.job_id,
        job_kind=current_job.job_kind if current_job is not None else "draft",
        status=payload.status,
        progress_percent=progress_percent,
        total_segments=(
            payload.total_segments
            if payload.total_segments is not None
            else current_job.total_segments
            if current_job is not None
            else None
        ),
        start_segment_index=current_job.start_segment_index if current_job is not None else None,
        plan_revision_id=current_job.plan_revision_id if current_job is not None else None,
        plan_revision_number=(
            current_job.plan_revision_number if current_job is not None else None
        ),
        beat_sheet_id=current_job.beat_sheet_id if current_job is not None else None,
        beat_sheet_revision_number=(
            current_job.beat_sheet_revision_number if current_job is not None else None
        ),
        story_setup_id=current_job.story_setup_id if current_job is not None else None,
        story_setup_revision_number=(
            current_job.story_setup_revision_number if current_job is not None else None
        ),
        story_outline_id=current_job.story_outline_id if current_job is not None else None,
        story_outline_revision_number=(
            current_job.story_outline_revision_number if current_job is not None else None
        ),
        current_segment_id=(
            payload.segment_id
            if payload.segment_id is not None
            else current_job.current_segment_id
            if current_job is not None
            else None
        ),
        current_segment_index=(
            payload.current_segment_index
            if payload.current_segment_index is not None
            else current_job.current_segment_index
            if current_job is not None
            else None
        ),
        rewrite_to_segment_index=(
            current_job.rewrite_to_segment_index if current_job is not None else None
        ),
        downstream_regeneration_mode=(
            current_job.downstream_regeneration_mode if current_job is not None else "none"
        ),
        stale_from_segment_index=(
            current_job.stale_from_segment_index if current_job is not None else None
        ),
        stale_to_segment_index=(
            current_job.stale_to_segment_index if current_job is not None else None
        ),
        pending_review=current_job.pending_review if current_job is not None else False,
        rewrite_candidate_segment_indexes=(
            list(current_job.rewrite_candidate_segment_indexes)
            if current_job is not None
            else []
        ),
        accepted_story_so_far=(
            current_job.accepted_story_so_far if current_job is not None else None
        ),
        latest_partial_output=(
            current_job.latest_partial_output if current_job is not None else None
        ),
        latest_segment_summary=(
            current_job.latest_segment_summary if current_job is not None else None
        ),
        interruption_request=interruption_request,
        attempt_count=current_job.attempt_count if current_job is not None else 1,
        stop_reason=current_job.stop_reason if current_job is not None else None,
        error_message=current_job.error_message if current_job is not None else None,
        started_at=current_job.started_at if current_job is not None else event_created_at,
        completed_at=(
            event_created_at
            if payload.status == JobStatus.COMPLETED.value
            else current_job.completed_at
            if current_job is not None
            else None
        ),
        created_at=current_job.created_at if current_job is not None else event_created_at,
        updated_at=event_created_at,
    )


def merge_audio_job_view(
    current_job: AudioJobView | None,
    payload: AudioProgressEventPayload,
    *,
    event_created_at: datetime,
) -> AudioJobView | None:
    if current_job is not None and current_job.id != payload.job_id:
        if normalize_sortable_datetime(current_job.updated_at) > normalize_sortable_datetime(
            event_created_at
        ):
            return current_job
        current_job = None

    return AudioJobView(
        id=payload.job_id,
        status=payload.status,
        voice_key=payload.voice_key
        if payload.voice_key is not None
        else (current_job.voice_key if current_job is not None else None),
        playback_speed=current_job.playback_speed if current_job is not None else 1.0,
        include_background_music=(
            current_job.include_background_music if current_job is not None else False
        ),
        music_profile=current_job.music_profile if current_job is not None else None,
        progress_percent=(
            payload.progress_percent
            if payload.progress_percent is not None
            else current_job.progress_percent
            if current_job is not None
            else 0
        ),
        current_step=(
            payload.current_step
            if payload.current_step is not None
            else payload.message
            if payload.message is not None
            else current_job.current_step
            if current_job is not None
            else None
        ),
        current_step_index=(
            payload.current_step_index
            if payload.current_step_index is not None
            else current_job.current_step_index
            if current_job is not None
            else None
        ),
        total_steps=(
            payload.total_steps
            if payload.total_steps is not None
            else current_job.total_steps
            if current_job is not None
            else None
        ),
        completed_segments=(
            payload.completed_segments
            if payload.completed_segments is not None
            else current_job.completed_segments
            if current_job is not None
            else None
        ),
        estimated_duration_seconds=(
            payload.estimated_duration_seconds
            if payload.estimated_duration_seconds is not None
            else current_job.estimated_duration_seconds
            if current_job is not None
            else None
        ),
        total_segments=(
            payload.total_segments
            if payload.total_segments is not None
            else current_job.total_segments
            if current_job is not None
            else None
        ),
        current_segment_index=(
            payload.current_segment_index
            if payload.current_segment_index is not None
            else current_job.current_segment_index
            if current_job is not None
            else None
        ),
        latest_asset_id=(
            payload.latest_asset_id
            if payload.latest_asset_id is not None
            else current_job.latest_asset_id
            if current_job is not None
            else None
        ),
        latest_asset_kind=(
            payload.latest_asset_kind
            if payload.latest_asset_kind is not None
            else current_job.latest_asset_kind
            if current_job is not None
            else None
        ),
        attempt_count=current_job.attempt_count if current_job is not None else 1,
        stop_reason=current_job.stop_reason if current_job is not None else None,
        error_message=current_job.error_message if current_job is not None else None,
        started_at=current_job.started_at if current_job is not None else event_created_at,
        completed_at=(
            event_created_at
            if payload.status == JobStatus.COMPLETED.value
            else current_job.completed_at
            if current_job is not None
            else None
        ),
        created_at=current_job.created_at if current_job is not None else event_created_at,
        updated_at=event_created_at,
    )


def update_stage_state_from_job(
    snapshot: SessionSnapshot,
    *,
    stage: WorkflowStage,
    status_value: str,
    detail: str,
    event_created_at: datetime,
    event_type: str,
    event_summary: str,
) -> None:
    stage_status = map_job_status_to_stage_state(status_value)
    for index, stage_state in enumerate(snapshot.stage_states):
        if stage_state.stage != stage:
            continue
        if not is_event_newer(stage_state.last_event_at, event_created_at):
            return

        snapshot.stage_states[index] = stage_state.model_copy(
            update={
                "status": stage_status,
                "detail": detail,
                "started_at": (
                    stage_state.started_at
                    if stage_state.started_at is not None
                    else event_created_at
                ),
                "completed_at": (
                    event_created_at
                    if status_value == JobStatus.COMPLETED.value
                    else stage_state.completed_at
                    if stage_status == WorkflowStageState.COMPLETED
                    else None
                ),
                "last_event_summary": event_summary,
                "last_event_type": event_type,
                "last_event_at": event_created_at,
            }
        )
        return


def map_job_status_to_stage_state(status_value: str) -> WorkflowStageState:
    if status_value == JobStatus.COMPLETED.value:
        return WorkflowStageState.COMPLETED
    if status_value in {JobStatus.FAILED.value, JobStatus.CANCELLED.value}:
        return WorkflowStageState.NEEDS_REGENERATION
    return WorkflowStageState.IN_PROGRESS


def build_composition_job_detail(
    job: CompositionJobView | None,
    *,
    fallback_summary: str,
) -> str:
    if job is None:
        return fallback_summary
    if job.interruption_request is not None:
        return job.interruption_request.message
    if job.error_message:
        return job.error_message
    if job.stop_reason:
        return job.stop_reason
    if job.status == JobStatus.COMPLETED.value:
        return "Writing finished and the latest draft is ready for review."
    if job.status == JobStatus.PAUSED.value and job.progress_percent is not None:
        return f"Writing paused at {round(job.progress_percent)}% complete."
    if job.status == JobStatus.FAILED.value:
        return "Writing failed and needs another pass."
    if job.progress_percent is not None:
        return f"Writing {round(job.progress_percent)}% complete."
    return fallback_summary


def build_audio_job_detail(
    job: AudioJobView | None,
    *,
    fallback_summary: str,
) -> str:
    if job is None:
        return fallback_summary
    if job.error_message:
        return job.error_message
    if job.stop_reason:
        return job.stop_reason
    if job.current_step:
        return job.current_step
    if job.status == JobStatus.COMPLETED.value:
        return "Narration finished and the latest audio is ready for review."
    if job.status == JobStatus.PAUSED.value:
        return "Narration is paused."
    if job.status == JobStatus.FAILED.value:
        return "Narration failed and needs another pass."
    if job.estimated_duration_seconds is not None:
        minutes = round(job.estimated_duration_seconds / 60)
        segment_detail = ""
        if job.current_segment_index is not None and job.total_segments is not None:
            segment_detail = (
                f" Segment {job.current_segment_index} of {job.total_segments} is active."
            )
        return (
            f"Narration {job.status.replace('_', ' ')}. Estimated length {minutes} min."
            f"{segment_detail}"
        )
    return fallback_summary


def recompute_rollups(snapshot: SessionSnapshot) -> None:
    statuses = {stage.stage: stage.status for stage in snapshot.stage_states}
    snapshot.resume_stage = resolve_resume_stage(statuses)
    snapshot.current_stage = snapshot.resume_stage
    snapshot.furthest_completed_stage = resolve_furthest_completed_stage(statuses)
    snapshot.overall_status = resolve_overall_status(statuses)
    snapshot.completed_at = (
        snapshot.updated_at if snapshot.overall_status == WorkflowStageState.COMPLETED else None
    )


def build_catalog_selection(row) -> SessionCatalogSelection | None:
    if row is None:
        return None

    return SessionCatalogSelection(
        id=row.id,
        slug=row.slug,
        label=row.label,
    )


def build_progress(stage_states) -> SessionProgress:
    stage_state_map = {stage_state.stage: stage_state for stage_state in stage_states}
    completed_stages = sum(
        1
        for stage in WORKFLOW_STAGE_SEQUENCE
        if stage_state_map.get(stage, None)
        and stage_state_map[stage].status == WorkflowStageState.COMPLETED
    )
    in_progress_stages = sum(
        1
        for stage in WORKFLOW_STAGE_SEQUENCE
        if stage_state_map.get(stage, None)
        and stage_state_map[stage].status == WorkflowStageState.IN_PROGRESS
    )
    needs_regeneration_stages = sum(
        1
        for stage in WORKFLOW_STAGE_SEQUENCE
        if stage_state_map.get(stage, None)
        and stage_state_map[stage].status == WorkflowStageState.NEEDS_REGENERATION
    )
    return SessionProgress(
        total_stages=len(WORKFLOW_STAGE_SEQUENCE),
        completed_stages=completed_stages,
        in_progress_stages=in_progress_stages,
        needs_regeneration_stages=needs_regeneration_stages,
    )


def build_stage_state_views(stage_states) -> list[SessionStageStateView]:
    stage_state_map = {stage_state.stage: stage_state for stage_state in stage_states}
    views: list[SessionStageStateView] = []

    for stage in WorkflowStage:
        definition = get_workflow_stage_definition(stage)
        snapshot = stage_state_map.get(stage)
        views.append(
            SessionStageStateView(
                stage=stage,
                label=definition.label,
                description=definition.description,
                status=snapshot.status if snapshot else WorkflowStageState.DRAFT,
                detail=snapshot.detail if snapshot else None,
                started_at=snapshot.started_at if snapshot else None,
                completed_at=snapshot.completed_at if snapshot else None,
                last_event_summary=(
                    snapshot.last_event.summary if snapshot and snapshot.last_event else None
                ),
                last_event_type=(
                    snapshot.last_event.event_type if snapshot and snapshot.last_event else None
                ),
                last_event_at=(
                    snapshot.last_event.created_at if snapshot and snapshot.last_event else None
                ),
            )
        )

    return views


def build_story_brief_view(row) -> StoryBriefView | None:
    if row is None:
        return None

    return StoryBriefView(
        id=row.id,
        revision_number=row.revision_number,
        story_idea=row.story_idea,
        desired_themes=row.desired_themes,
        key_images=row.key_images,
        audience_notes=row.audience_notes,
        must_have_elements=row.must_have_elements,
        raw_brief=row.raw_brief,
        normalized_summary=row.normalized_summary,
        normalized_preferences=NormalizedBriefPreferences.model_validate(
            row.normalized_preferences or {}
        )
        if row.normalized_preferences is not None
        else None,
        planning_notes=row.planning_notes,
        accepted_at=row.accepted_at,
        updated_at=row.updated_at,
    )


def build_pitch_view(row) -> PitchView | None:
    if row is None:
        return None

    batch_metadata = _read_pitch_batch_metadata(row)
    refinement_metadata = _read_pitch_refinement_metadata(row)

    return PitchView(
        id=row.id,
        generation_key=row.generation_key,
        pitch_index=row.pitch_index,
        title=row.title,
        hook=row.logline,
        central_conflict=row.summary,
        why_it_fits=row.bedtime_notes,
        logline=row.logline,
        summary=row.summary,
        bedtime_notes=row.bedtime_notes,
        generation_kind=batch_metadata.get("generation_kind", "generated"),
        source_pitch_id=refinement_metadata.get("source_pitch_id"),
        source_pitch_title=refinement_metadata.get("source_pitch_title"),
        refinement_instructions=refinement_metadata.get("refinement_instructions"),
        selection_rationale=refinement_metadata.get("selection_rationale"),
        is_selected=row.is_selected,
        accepted_at=row.accepted_at,
        created_at=row.created_at,
        updated_at=row.updated_at,
    )


def build_pitch_batch_views(rows) -> list[PitchBatchView]:
    batches: dict[str, list] = {}
    batch_created_at: dict[str, datetime] = {}

    for row in rows or []:
        batches.setdefault(row.generation_key, []).append(row)
        existing_created_at = batch_created_at.get(row.generation_key)
        if existing_created_at is None or normalize_sortable_datetime(
            row.created_at
        ) < normalize_sortable_datetime(existing_created_at):
            batch_created_at[row.generation_key] = row.created_at

    ordered_keys = sorted(
        batches,
        key=lambda generation_key: (
            normalize_sortable_datetime(batch_created_at[generation_key]),
            generation_key,
        ),
        reverse=True,
    )

    return [
        PitchBatchView(
            generation_key=generation_key,
            candidate_count=len(batches[generation_key]),
            created_at=batch_created_at[generation_key],
            generation_kind=_read_pitch_batch_metadata(batches[generation_key][0]).get(
                "generation_kind",
                "generated",
            ),
            guidance=_read_pitch_batch_metadata(batches[generation_key][0]).get("guidance"),
            source_pitch_id=_read_pitch_refinement_metadata(batches[generation_key][0]).get(
                "source_pitch_id"
            ),
            source_pitch_title=_read_pitch_refinement_metadata(batches[generation_key][0]).get(
                "source_pitch_title"
            ),
            source_generation_key=_read_pitch_refinement_metadata(batches[generation_key][0]).get(
                "source_generation_key"
            ),
            refinement_instructions=_read_pitch_refinement_metadata(batches[generation_key][0]).get(
                "refinement_instructions"
            ),
            pitches=[
                build_pitch_view(row)
                for row in sorted(
                    batches[generation_key],
                    key=lambda pitch: pitch.pitch_index,
                )
            ],
        )
        for generation_key in ordered_keys
    ]


def _read_pitch_batch_metadata(row) -> dict[str, Any]:
    if not isinstance(getattr(row, "model_output", None), Mapping):
        return {}

    batch_metadata = row.model_output.get("batch_metadata")
    return dict(batch_metadata) if isinstance(batch_metadata, Mapping) else {}


def _read_pitch_refinement_metadata(row) -> dict[str, Any]:
    if not isinstance(getattr(row, "model_output", None), Mapping):
        return {}

    refinement_metadata = row.model_output.get("refinement")
    return dict(refinement_metadata) if isinstance(refinement_metadata, Mapping) else {}


def _read_character_candidate_data(row) -> dict[str, Any]:
    if not isinstance(getattr(row, "character_data", None), Mapping):
        return {}

    candidate = row.character_data.get("candidate")
    return dict(candidate) if isinstance(candidate, Mapping) else {}


def _read_character_batch_metadata(row) -> dict[str, Any]:
    if not isinstance(getattr(row, "character_data", None), Mapping):
        return {}

    batch_metadata = row.character_data.get("batch_metadata")
    return dict(batch_metadata) if isinstance(batch_metadata, Mapping) else {}


def _read_character_refinement_metadata(row) -> dict[str, Any]:
    if not isinstance(getattr(row, "character_data", None), Mapping):
        return {}

    refinement_metadata = row.character_data.get("refinement")
    return dict(refinement_metadata) if isinstance(refinement_metadata, Mapping) else {}


def _read_mapping(value: object) -> Mapping[str, Any]:
    if isinstance(value, Mapping):
        return value
    return {}


def _enum_value(value: Any) -> str:
    return getattr(value, "value", value)


def _read_optional_mapping_text(data: Mapping[str, Any] | dict[str, Any], key: str) -> str | None:
    value = data.get(key)
    return value if isinstance(value, str) else None


def _read_optional_mapping_int(data: Mapping[str, Any] | dict[str, Any], key: str) -> int | None:
    value = data.get(key)
    return value if isinstance(value, int) else None


def _read_optional_mapping_float(
    data: Mapping[str, Any] | dict[str, Any],
    key: str,
) -> float | None:
    value = data.get(key)
    if isinstance(value, (int, float)):
        return float(value)
    return None


def _read_optional_mapping_bool(
    data: Mapping[str, Any] | dict[str, Any],
    key: str,
) -> bool | None:
    value = data.get(key)
    return value if isinstance(value, bool) else None


def _read_string_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []

    return [entry for entry in value if isinstance(entry, str)]


def _build_text_preview(value: str | None, *, limit: int = 132) -> str | None:
    if value is None:
        return None

    normalized = " ".join(value.split())
    if not normalized:
        return None
    if len(normalized) <= limit:
        return normalized
    return f"{normalized[: limit - 3].rstrip()}..."


def _read_beat_sheet_payload(row) -> dict[str, Any]:
    raw = getattr(row, "beats", None)
    return dict(raw) if isinstance(raw, Mapping) else {}


def _read_beat_sheet_refinement_metadata(row) -> dict[str, Any]:
    payload = _read_beat_sheet_payload(row)
    refinement = payload.get("refinement")
    return dict(refinement) if isinstance(refinement, Mapping) else {}


def _build_beat_sheet_edit_history(
    payload: Mapping[str, Any] | dict[str, Any],
) -> list[BeatSheetEditView]:
    raw_history = payload.get("edit_history")
    if not isinstance(raw_history, list):
        return []

    history: list[BeatSheetEditView] = []
    for raw_entry in raw_history:
        if not isinstance(raw_entry, Mapping):
            continue

        edit_id = raw_entry.get("id") if isinstance(raw_entry.get("id"), str) else None
        summary_text = (
            raw_entry.get("summary_text")
            if isinstance(raw_entry.get("summary_text"), str)
            else None
        )
        created_at_value = raw_entry.get("created_at")
        if edit_id is None or summary_text is None or not isinstance(created_at_value, str):
            continue

        try:
            created_at = datetime.fromisoformat(created_at_value.replace("Z", "+00:00"))
        except ValueError:
            continue

        history.append(
            BeatSheetEditView(
                id=edit_id,
                summary_text=summary_text,
                origin=(
                    raw_entry.get("origin")
                    if isinstance(raw_entry.get("origin"), str)
                    else "workspace"
                ),
                changed_fields=_read_string_list(raw_entry.get("changed_fields")),
                beat_keys=_read_string_list(raw_entry.get("beat_keys")),
                material_change=bool(raw_entry.get("material_change")),
                refreshes_downstream=bool(raw_entry.get("refreshes_downstream")),
                created_at=created_at,
            )
        )

    return sorted(history, key=lambda entry: entry.created_at, reverse=True)


def _build_story_outline_edit_history(
    metadata: Mapping[str, Any] | dict[str, Any],
) -> list[StoryOutlineEditView]:
    raw_history = metadata.get("edit_history")
    if not isinstance(raw_history, list):
        return []

    history: list[StoryOutlineEditView] = []
    for raw_entry in raw_history:
        if not isinstance(raw_entry, Mapping):
            continue

        created_at_value = raw_entry.get("created_at")
        if not isinstance(created_at_value, str):
            continue

        try:
            created_at = datetime.fromisoformat(created_at_value.replace("Z", "+00:00"))
        except ValueError:
            continue

        history.append(
            StoryOutlineEditView(
                summary_text=_read_optional_mapping_text(raw_entry, "summary_text")
                or "Updated story outline cards.",
                origin=_read_optional_mapping_text(raw_entry, "origin") or "workspace",
                changed_fields=_read_string_list(raw_entry.get("changed_fields")),
                changed_card_keys=_read_string_list(raw_entry.get("changed_card_keys")),
                regenerated_card_keys=_read_string_list(raw_entry.get("regenerated_card_keys")),
                change_impact=_read_optional_mapping_text(raw_entry, "change_impact"),
                reordered=_read_optional_mapping_bool(raw_entry, "reordered") or False,
                refreshes_downstream=_read_optional_mapping_bool(
                    raw_entry,
                    "refreshes_downstream",
                )
                or False,
                invalidated_stages=_read_string_list(raw_entry.get("invalidated_stages")),
                created_at=created_at,
            )
        )

    return sorted(history, key=lambda entry: entry.created_at, reverse=True)


def build_beat_entries(row) -> list[BeatSheetBeatView]:
    raw = getattr(row, "beats", None)
    if isinstance(raw, Mapping):
        nested_beats = raw.get("beats")
        if isinstance(nested_beats, list):
            return _build_beat_entries_from_list(nested_beats)
        return _build_beat_entries_from_mapping(raw)
    if isinstance(raw, list):
        return _build_beat_entries_from_list(raw)
    return []


def _build_beat_entries_from_list(value: list[Any]) -> list[BeatSheetBeatView]:
    beats: list[BeatSheetBeatView] = []
    for fallback_order, raw_entry in enumerate(value, start=1):
        if not isinstance(raw_entry, Mapping):
            continue
        key = (
            raw_entry.get("key")
            if isinstance(raw_entry.get("key"), str)
            else f"beat-{fallback_order}"
        )
        label = (
            raw_entry.get("label")
            if isinstance(raw_entry.get("label"), str)
            else SAVE_THE_CAT_BEAT_LABELS.get(key, key.replace("_", " ").title())
        )
        order = (
            raw_entry.get("order") if isinstance(raw_entry.get("order"), int) else fallback_order
        )
        summary = raw_entry.get("summary") if isinstance(raw_entry.get("summary"), str) else ""
        if not summary:
            continue
        beats.append(
            BeatSheetBeatView(
                key=key,
                label=label,
                order=order,
                summary=summary,
                emotional_intent=(
                    raw_entry.get("emotional_intent")
                    if isinstance(raw_entry.get("emotional_intent"), str)
                    else None
                ),
                bedtime_softening_note=(
                    raw_entry.get("bedtime_softening_note")
                    if isinstance(raw_entry.get("bedtime_softening_note"), str)
                    else None
                ),
            )
        )
    return sorted(beats, key=lambda beat: beat.order)


def _build_beat_entries_from_mapping(value: Mapping[str, Any]) -> list[BeatSheetBeatView]:
    beats: list[BeatSheetBeatView] = []
    for order, (key, label) in enumerate(SAVE_THE_CAT_BEAT_SEQUENCE, start=1):
        summary = value.get(key)
        if not isinstance(summary, str) or not summary:
            continue
        beats.append(
            BeatSheetBeatView(
                key=key,
                label=label,
                order=order,
                summary=summary,
            )
        )
    return beats


def _resolve_character_batch_key(row) -> str:
    return _read_character_batch_metadata(row).get(
        "generation_key",
        f"legacy-character-{getattr(row, 'revision_number', 'unknown')}",
    )


def _resolve_character_candidate_index(row) -> int:
    candidate_index = _read_character_batch_metadata(row).get("candidate_index")
    if isinstance(candidate_index, int) and candidate_index >= 1:
        return candidate_index

    revision_number = getattr(row, "revision_number", None)
    return revision_number if isinstance(revision_number, int) and revision_number >= 1 else 1


def _read_character_visual_motifs(candidate_payload: Mapping[str, Any]) -> list[str]:
    visual_motifs = candidate_payload.get("visual_motifs")
    if not isinstance(visual_motifs, list):
        return []

    return [value for value in visual_motifs if isinstance(value, str)]


def build_character_profile_view(
    value,
    *,
    fallback_name: str | None = None,
) -> CharacterProfileView | None:
    if isinstance(value, Mapping):
        name = value.get("name") if isinstance(value.get("name"), str) else fallback_name
        if name is None:
            return None

        return CharacterProfileView(
            name=name,
            role=value.get("role") if isinstance(value.get("role"), str) else None,
            goal=value.get("goal") if isinstance(value.get("goal"), str) else None,
            flaw=value.get("flaw") if isinstance(value.get("flaw"), str) else None,
            comfort_trait=(
                value.get("comfort_trait") if isinstance(value.get("comfort_trait"), str) else None
            ),
            bedtime_safety_notes=(
                value.get("bedtime_safety_notes")
                if isinstance(value.get("bedtime_safety_notes"), str)
                else None
            ),
            relationships=[
                entry for entry in value.get("relationships", []) if isinstance(entry, str)
            ]
            if isinstance(value.get("relationships"), list)
            else [],
            visual_anchors=[
                entry for entry in value.get("visual_anchors", []) if isinstance(entry, str)
            ]
            if isinstance(value.get("visual_anchors"), list)
            else [],
        )

    if fallback_name is not None:
        return CharacterProfileView(name=fallback_name)

    return None


def build_character_supporting_cast_views(
    value,
    *,
    fallback,
) -> list[CharacterProfileView]:
    if isinstance(value, list):
        cast = [build_character_profile_view(entry) for entry in value]
        return [entry for entry in cast if entry is not None]

    if isinstance(fallback, list):
        cast = [build_character_profile_view(entry) for entry in fallback]
        return [entry for entry in cast if entry is not None]

    if isinstance(fallback, Mapping):
        return [
            CharacterProfileView(
                name=str(name),
                role=role if isinstance(role, str) else None,
            )
            for name, role in fallback.items()
        ]

    return []


def build_character_sheet_view(row) -> CharacterSheetView | None:
    if row is None:
        return None

    candidate_payload = _read_character_candidate_data(row)
    refinement_metadata = _read_character_refinement_metadata(row)
    batch_metadata = _read_character_batch_metadata(row)

    return CharacterSheetView(
        id=row.id,
        revision_number=row.revision_number,
        generation_key=batch_metadata.get("generation_key"),
        candidate_index=batch_metadata.get("candidate_index"),
        title=row.title,
        protagonist_name=row.protagonist_name,
        summary=row.summary,
        story_function=_read_optional_mapping_text(candidate_payload, "story_function"),
        protagonist=build_character_profile_view(
            candidate_payload.get("protagonist"),
            fallback_name=row.protagonist_name,
        ),
        supporting_cast=build_character_supporting_cast_views(
            candidate_payload.get("supporting_cast"),
            fallback=row.supporting_cast,
        ),
        bedtime_notes=row.bedtime_notes,
        bedtime_safety_notes=(
            _read_optional_mapping_text(candidate_payload, "bedtime_safety_notes")
            or row.bedtime_notes
        ),
        visual_motifs=_read_character_visual_motifs(candidate_payload),
        generation_kind=batch_metadata.get("generation_kind", "generated"),
        source_pitch_id=refinement_metadata.get("source_pitch_id"),
        source_pitch_title=refinement_metadata.get("source_pitch_title"),
        source_character_sheet_id=refinement_metadata.get("source_character_sheet_id"),
        source_character_sheet_title=refinement_metadata.get("source_character_sheet_title"),
        refinement_instructions=refinement_metadata.get("refinement_instructions"),
        focus_character_names=_read_string_list(refinement_metadata.get("focus_character_names")),
        change_summary=_read_optional_mapping_text(refinement_metadata, "change_summary"),
        change_impact=_read_optional_mapping_text(refinement_metadata, "change_impact"),
        selection_rationale=refinement_metadata.get("selection_rationale"),
        is_selected=row.is_selected,
        accepted_at=row.accepted_at,
        created_at=row.created_at,
        updated_at=row.updated_at,
    )


def build_character_sheet_batch_views(rows) -> list[CharacterSheetBatchView]:
    batches: dict[str, list] = {}
    batch_created_at: dict[str, datetime] = {}

    for row in rows or []:
        generation_key = _resolve_character_batch_key(row)
        batches.setdefault(generation_key, []).append(row)
        existing_created_at = batch_created_at.get(generation_key)
        if existing_created_at is None or normalize_sortable_datetime(
            row.created_at
        ) < normalize_sortable_datetime(existing_created_at):
            batch_created_at[generation_key] = row.created_at

    ordered_keys = sorted(
        batches,
        key=lambda generation_key: (
            normalize_sortable_datetime(batch_created_at[generation_key]),
            generation_key,
        ),
        reverse=True,
    )

    return [
        CharacterSheetBatchView(
            generation_key=generation_key,
            candidate_count=len(batches[generation_key]),
            created_at=batch_created_at[generation_key],
            generation_kind=_read_character_batch_metadata(batches[generation_key][0]).get(
                "generation_kind",
                "generated",
            ),
            guidance=_read_character_batch_metadata(batches[generation_key][0]).get("guidance"),
            source_pitch_id=_read_character_refinement_metadata(batches[generation_key][0]).get(
                "source_pitch_id"
            ),
            source_pitch_title=_read_character_refinement_metadata(batches[generation_key][0]).get(
                "source_pitch_title"
            ),
            source_character_sheet_id=_read_character_refinement_metadata(
                batches[generation_key][0]
            ).get("source_character_sheet_id"),
            source_character_sheet_title=_read_character_refinement_metadata(
                batches[generation_key][0]
            ).get("source_character_sheet_title"),
            refinement_instructions=_read_character_refinement_metadata(
                batches[generation_key][0]
            ).get("refinement_instructions"),
            focus_character_names=_read_string_list(
                _read_character_refinement_metadata(batches[generation_key][0]).get(
                    "focus_character_names"
                )
            ),
            change_summary=_read_optional_mapping_text(
                _read_character_refinement_metadata(batches[generation_key][0]),
                "change_summary",
            ),
            change_impact=_read_optional_mapping_text(
                _read_character_refinement_metadata(batches[generation_key][0]),
                "change_impact",
            ),
            character_sheets=[
                build_character_sheet_view(row)
                for row in sorted(
                    batches[generation_key],
                    key=lambda character_sheet: _resolve_character_candidate_index(character_sheet),
                )
            ],
        )
        for generation_key in ordered_keys
    ]


def build_beat_sheet_view(row) -> BeatSheetView | None:
    if row is None:
        return None

    payload = _read_beat_sheet_payload(row)
    refinement_metadata = _read_beat_sheet_refinement_metadata(row)

    return BeatSheetView(
        id=row.id,
        revision_number=row.revision_number,
        generation_kind=_read_optional_mapping_text(payload, "generation_kind") or "generated",
        summary=row.summary,
        beats=build_beat_entries(row),
        bedtime_notes=row.bedtime_notes,
        source_beat_sheet_id=_read_optional_mapping_text(
            refinement_metadata,
            "source_beat_sheet_id",
        ),
        source_beat_sheet_revision_number=_read_optional_mapping_int(
            refinement_metadata,
            "source_beat_sheet_revision_number",
        ),
        guidance=_read_optional_mapping_text(payload, "guidance"),
        refinement_instructions=_read_optional_mapping_text(
            refinement_metadata,
            "refinement_instructions",
        ),
        focus_beats=_read_string_list(payload.get("focus_beats")),
        bedtime_goal=_read_optional_mapping_text(payload, "bedtime_goal"),
        selection_rationale=_read_optional_mapping_text(
            refinement_metadata,
            "selection_rationale",
        ),
        edit_history=_build_beat_sheet_edit_history(payload),
        is_selected=row.is_selected,
        accepted_at=row.accepted_at,
        created_at=row.created_at,
        updated_at=row.updated_at,
    )


def build_beat_sheet_views(rows) -> list[BeatSheetView]:
    if rows is None:
        return []

    return [
        view
        for view in (
            build_beat_sheet_view(row)
            for row in sorted(
                rows,
                key=lambda beat_sheet: (getattr(beat_sheet, "revision_number", 0),),
                reverse=True,
            )
        )
        if view is not None
    ]


def build_story_setup_view(row) -> StorySetupView | None:
    if row is None:
        return None

    return StorySetupView(
        id=row.id,
        revision_number=row.revision_number,
        target_word_count=row.target_word_count,
        target_runtime_minutes=row.target_runtime_minutes,
        chapter_count=row.chapter_count,
        approximate_scene_count=row.approximate_scene_count,
        chapter_style=row.chapter_style,
        guidance_notes=row.guidance_notes,
        preferences=row.preferences,
        accepted_at=row.accepted_at,
    )


def build_story_outline_view(row) -> StoryOutlineView | None:
    if row is None:
        return None

    metadata = row.metadata_json if isinstance(row.metadata_json, dict) else {}
    raw_cards = row.cards if isinstance(row.cards, list) else []
    cards = [StoryOutlineCard.model_validate(card) for card in raw_cards if isinstance(card, dict)]
    edit_history = _build_story_outline_edit_history(metadata)

    return StoryOutlineView(
        id=row.id,
        revision_number=row.revision_number,
        outline_kind=row.outline_kind,
        summary=row.summary,
        cards=cards,
        genre_label=_read_optional_mapping_text(metadata, "genre_label"),
        tone_label=_read_optional_mapping_text(metadata, "tone_label"),
        target_word_count=_read_optional_mapping_int(metadata, "target_word_count"),
        target_runtime_minutes=_read_optional_mapping_int(metadata, "target_runtime_minutes"),
        chapter_count=_read_optional_mapping_int(metadata, "chapter_count"),
        approximate_scene_count=_read_optional_mapping_int(metadata, "approximate_scene_count"),
        chapter_style=_read_optional_mapping_text(metadata, "chapter_style"),
        guidance_notes=_read_optional_mapping_text(metadata, "guidance_notes"),
        bedtime_goal=_read_optional_mapping_text(metadata, "bedtime_goal"),
        last_change_summary=_read_optional_mapping_text(metadata, "last_change_summary"),
        change_impact=_read_optional_mapping_text(metadata, "change_impact"),
        refreshes_downstream=_read_optional_mapping_bool(
            metadata,
            "refreshes_downstream",
        )
        or False,
        invalidated_stages=_read_string_list(metadata.get("invalidated_stages")),
        edit_history=edit_history,
        is_selected=row.is_selected,
        accepted_at=row.accepted_at,
        created_at=row.created_at,
        updated_at=row.updated_at,
    )


def build_story_outline_views(rows) -> list[StoryOutlineView]:
    if rows is None:
        return []

    return [
        view
        for view in (
            build_story_outline_view(row)
            for row in sorted(
                rows,
                key=lambda story_outline: (getattr(story_outline, "revision_number", 0),),
                reverse=True,
            )
        )
        if view is not None
    ]


def build_plan_revision_views(rows) -> list[PlanRevisionView]:
    if rows is None:
        return []

    ordered_rows = sorted(
        rows,
        key=lambda plan_revision: getattr(plan_revision, "revision_number", 0),
    )
    previous_revision = None
    views: list[PlanRevisionView] = []

    for row in ordered_rows:
        view = build_plan_revision_view(row, previous_revision=previous_revision)
        if view is not None:
            views.append(view)
        previous_revision = row

    return list(reversed(views))


def build_plan_revision_view(
    row,
    *,
    previous_revision,
) -> PlanRevisionView | None:
    if row is None:
        return None

    changed_artifacts = _resolve_plan_revision_changed_artifacts(row, previous_revision)
    restored_from_revision = getattr(row, "restored_from_plan_revision", None)

    return PlanRevisionView(
        id=row.id,
        revision_number=row.revision_number,
        source_stage=row.source_stage,
        change_summary=row.change_summary,
        comparison_summary=_build_plan_revision_comparison_summary(
            row,
            changed_artifacts=changed_artifacts,
            previous_revision=previous_revision,
        ),
        restored_from_revision_number=(
            restored_from_revision.revision_number if restored_from_revision is not None else None
        ),
        changed_artifacts=changed_artifacts,
        pitch=_build_plan_artifact_ref_view("pitch", getattr(row, "pitch", None)),
        character_sheet=_build_plan_artifact_ref_view(
            "character_sheet",
            getattr(row, "character_sheet", None),
        ),
        beat_sheet=_build_plan_artifact_ref_view("beat_sheet", getattr(row, "beat_sheet", None)),
        story_setup=_build_plan_artifact_ref_view("story_setup", getattr(row, "story_setup", None)),
        story_outline=_build_plan_artifact_ref_view(
            "story_outline",
            getattr(row, "story_outline", None),
        ),
        is_current=row.is_current,
        created_at=row.created_at,
        updated_at=row.updated_at,
    )


def _build_plan_artifact_ref_view(kind: str, row) -> PlanArtifactRefView | None:
    if row is None:
        return None

    if kind == "pitch":
        label = getattr(row, "title", None) or "Selected pitch"
        revision_number = None
    elif kind == "character_sheet":
        label = (
            getattr(row, "title", None)
            or getattr(row, "protagonist_name", None)
            or f"Character revision {getattr(row, 'revision_number', '?')}"
        )
        revision_number = getattr(row, "revision_number", None)
    elif kind == "beat_sheet":
        label = f"Beat sheet revision {getattr(row, 'revision_number', '?')}"
        revision_number = getattr(row, "revision_number", None)
    elif kind == "story_setup":
        revision_number = getattr(row, "revision_number", None)
        label = _build_story_setup_artifact_label(row)
    else:
        revision_number = getattr(row, "revision_number", None)
        outline_kind = getattr(row, "outline_kind", "story")
        label = f"{outline_kind.capitalize()} outline revision {revision_number or '?'}"

    return PlanArtifactRefView(
        id=row.id,
        label=label,
        revision_number=revision_number,
    )


def _build_story_setup_artifact_label(row) -> str:
    parts: list[str] = []
    runtime = getattr(row, "target_runtime_minutes", None)
    if runtime is not None:
        parts.append(f"~{runtime} min")
    chapters = getattr(row, "chapter_count", None)
    if chapters is not None:
        parts.append(f"{chapters} chapters")
    scenes = getattr(row, "approximate_scene_count", None)
    if scenes is not None:
        parts.append(f"{scenes} scenes")
    return ", ".join(parts) if parts else "Story setup preferences"


def _resolve_plan_revision_changed_artifacts(row, previous_revision) -> list[str]:
    artifact_ids = {
        "pitch": getattr(row, "pitch_id", None),
        "character_sheet": getattr(row, "character_sheet_id", None),
        "beat_sheet": getattr(row, "beat_sheet_id", None),
        "story_setup": getattr(row, "story_setup_id", None),
        "story_outline": getattr(row, "story_outline_id", None),
    }
    if previous_revision is None:
        return [artifact_kind for artifact_kind, artifact_id in artifact_ids.items() if artifact_id]

    changed_artifacts: list[str] = []
    for artifact_kind, artifact_id in artifact_ids.items():
        if artifact_id != getattr(previous_revision, f"{artifact_kind}_id", None):
            changed_artifacts.append(artifact_kind)
    return changed_artifacts


def _build_plan_revision_comparison_summary(
    row,
    *,
    changed_artifacts: list[str],
    previous_revision,
) -> str:
    restored_from_revision = getattr(row, "restored_from_plan_revision", None)
    if restored_from_revision is not None:
        return f"Restored from plan revision {restored_from_revision.revision_number}."

    if previous_revision is None:
        return "Captured the first durable plan snapshot."

    if not changed_artifacts:
        return "Re-saved the same selected plan snapshot."

    return f"Changed {humanize_joined_tokens(changed_artifacts)}."


def build_continuity_bible_view(row) -> ContinuityBibleView | None:
    if row is None:
        return None

    raw_summary_data = getattr(row, "summary_data", None)
    data = (
        ContinuityBibleData.model_validate(raw_summary_data)
        if isinstance(raw_summary_data, Mapping)
        else ContinuityBibleData()
    )

    return ContinuityBibleView(
        id=row.id,
        revision_number=row.revision_number,
        source_stage=row.source_stage,
        source_summary=row.source_summary,
        summary_text=row.summary_text,
        facts=[ContinuityFact.model_validate(fact) for fact in data.facts],
        created_at=row.created_at,
        updated_at=row.updated_at,
    )


def build_composition_interruption_request_view(
    row: CompositionInterruptionRequest | None,
) -> CompositionInterruptionRequestView | None:
    if row is None:
        return None

    return CompositionInterruptionRequestView(
        id=row.id,
        request_kind=row.request_kind,
        state=row.state,
        origin=row.origin,
        message=build_composition_interruption_message(
            request_kind=row.request_kind,
            state=row.state,
            requested_progress_percent=row.requested_progress_percent,
            requested_segment_index=row.requested_segment_index,
            rewrite_from_segment_index=row.rewrite_from_segment_index,
            resolution_summary=row.resolution_summary,
        ),
        instructions=row.instructions,
        rewrite_from_segment_index=row.rewrite_from_segment_index,
        requested_status=row.requested_status,
        requested_segment_id=row.requested_segment_id,
        requested_segment_index=row.requested_segment_index,
        requested_progress_percent=row.requested_progress_percent,
        resolution_summary=row.resolution_summary,
        created_at=row.created_at,
        updated_at=row.updated_at,
        resolved_at=row.resolved_at,
    )


def _resolve_active_composition_interruption_request(
    row: CompositionJob,
) -> CompositionInterruptionRequest | None:
    active_requests = [
        request
        for request in getattr(row, "interruption_requests", [])
        if request.state
        in {
            CompositionInterruptionState.REQUESTED,
            CompositionInterruptionState.APPLYING,
        }
    ]
    if not active_requests:
        return None

    active_requests.sort(key=lambda request: request.created_at, reverse=True)
    return active_requests[0]


def build_composition_job_view(row: CompositionJob | None) -> CompositionJobView | None:
    if row is None:
        return None

    metadata = row.metadata_json if isinstance(row.metadata_json, Mapping) else {}
    rewrite_candidate_segment_indexes = sorted(
        {
            segment.segment_index
            for segment in getattr(row, "segments", [])
            if (
                row.status == JobStatus.COMPLETED
                and getattr(segment, "status", None) == JobStatus.COMPLETED
                and (
                    getattr(segment, "acceptance_state", None) == "pending"
                    or getattr(segment, "acceptance_state", None) == "PENDING"
                )
            )
        }
    )
    story_outline_id = _read_optional_mapping_text(metadata, "story_outline_id")
    story_outline_revision_number = _read_optional_mapping_int(
        metadata,
        "story_outline_revision_number",
    )
    total_segments = _read_optional_mapping_int(metadata, "total_segments")
    start_segment_index = _read_optional_mapping_int(metadata, "start_segment_index")
    current_segment_id = _read_optional_mapping_text(metadata, "current_segment_id")
    accepted_story_so_far = _read_optional_mapping_text(metadata, "accepted_story_so_far")
    latest_partial_output = _read_optional_mapping_text(metadata, "latest_partial_output")
    latest_segment_summary = _read_optional_mapping_text(metadata, "latest_segment_summary")
    interruption_request = build_composition_interruption_request_view(
        _resolve_active_composition_interruption_request(row)
    )

    return CompositionJobView(
        id=row.id,
        job_kind=row.job_kind,
        status=row.status,
        progress_percent=row.progress_percent,
        total_segments=total_segments,
        start_segment_index=start_segment_index,
        plan_revision_id=row.plan_revision_id,
        plan_revision_number=(
            row.plan_revision.revision_number
            if getattr(row, "plan_revision", None) is not None
            else None
        ),
        beat_sheet_id=row.beat_sheet_id,
        beat_sheet_revision_number=(
            row.beat_sheet.revision_number if getattr(row, "beat_sheet", None) is not None else None
        ),
        story_setup_id=row.story_setup_id,
        story_setup_revision_number=(
            row.story_setup.revision_number
            if getattr(row, "story_setup", None) is not None
            else None
        ),
        story_outline_id=story_outline_id,
        story_outline_revision_number=story_outline_revision_number,
        current_segment_id=current_segment_id,
        current_segment_index=row.current_segment_index,
        rewrite_to_segment_index=row.rewrite_to_segment_index,
        downstream_regeneration_mode=row.downstream_regeneration_mode,
        stale_from_segment_index=row.stale_from_segment_index,
        stale_to_segment_index=row.stale_to_segment_index,
        pending_review=bool(rewrite_candidate_segment_indexes),
        rewrite_candidate_segment_indexes=rewrite_candidate_segment_indexes,
        accepted_story_so_far=accepted_story_so_far,
        latest_partial_output=latest_partial_output,
        latest_segment_summary=latest_segment_summary,
        interruption_request=interruption_request,
        attempt_count=row.attempt_count,
        stop_reason=row.stop_reason,
        error_message=row.error_message,
        started_at=row.started_at,
        completed_at=row.completed_at,
        created_at=row.created_at,
        updated_at=row.updated_at,
    )


def build_composition_segment_views(rows) -> list[CompositionSegmentView]:
    by_segment: dict[int, list] = {}
    for row in rows:
        by_segment.setdefault(row.segment_index, []).append(row)

    segment_views: list[CompositionSegmentView] = []
    for segment_index in sorted(by_segment):
        segment_rows = sorted(
            by_segment[segment_index],
            key=lambda item: (item.revision_number, item.created_at),
            reverse=True,
        )
        current_version = next(
            (
                row
                for row in segment_rows
                if row.acceptance_state == "accepted" and row.superseded_by_segment_id is None
            ),
            None,
        )
        pending_version = next(
            (row for row in segment_rows if row.acceptance_state == "pending"),
            None,
        )
        outline_title = None
        outline_summary = None
        source_row = pending_version or current_version or segment_rows[0]
        payload = _read_mapping(getattr(source_row, "payload", None))
        outline_title = _read_optional_mapping_text(payload, "outline_card_title")
        outline_summary = _read_optional_mapping_text(payload, "outline_card_summary")
        segment_views.append(
            CompositionSegmentView(
                segment_index=segment_index,
                outline_card_title=outline_title,
                outline_card_summary=outline_summary,
                current_version_id=getattr(current_version, "id", None),
                current_revision_number=getattr(current_version, "revision_number", None),
                pending_version_id=getattr(pending_version, "id", None),
                pending_revision_number=getattr(pending_version, "revision_number", None),
                is_stale=bool(getattr(current_version, "is_stale", False)),
                stale_reason=getattr(current_version, "stale_reason", None),
                versions=[
                    build_composition_segment_version_view(version)
                    for version in segment_rows
                ],
            )
        )

    return segment_views


def build_composition_segment_version_view(row) -> CompositionSegmentVersionView:
    return CompositionSegmentVersionView(
        id=row.id,
        composition_job_id=row.composition_job_id,
        job_kind=(
            row.composition_job.job_kind
            if getattr(row, "composition_job", None) is not None
            else "draft"
        ),
        segment_index=row.segment_index,
        revision_number=row.revision_number,
        status=row.status,
        acceptance_state=row.acceptance_state,
        is_current=row.acceptance_state == "accepted" and row.superseded_by_segment_id is None,
        is_stale=bool(getattr(row, "is_stale", False)),
        planned_summary=row.planned_summary,
        accepted_summary=row.accepted_summary,
        text_content=row.accepted_text or row.text_content,
        word_count=row.word_count,
        created_at=row.created_at,
        updated_at=row.updated_at,
        completed_at=row.completed_at,
    )


def build_narration_segment_views(
    rows: list[NarrationSegment],
    preview_assets: list[SessionAsset],
) -> list[NarrationSegmentView]:
    latest_preview_asset_by_segment: dict[int, SessionAsset] = {}
    for asset in preview_assets:
        if asset.segment_index is None or asset.segment_index in latest_preview_asset_by_segment:
            continue
        latest_preview_asset_by_segment[asset.segment_index] = asset

    return [
        build_narration_segment_view(
            row,
            preview_asset=latest_preview_asset_by_segment.get(row.segment_index),
        )
        for row in rows
    ]


def build_narration_segment_view(
    row: NarrationSegment,
    *,
    preview_asset: SessionAsset | None = None,
) -> NarrationSegmentView:
    metadata = _read_mapping(row.metadata_json)

    return NarrationSegmentView(
        id=row.id,
        audio_job_id=row.audio_job_id,
        segment_index=row.segment_index,
        status=row.status,
        source_boundary_kind=_enum_value(row.source_boundary_kind),
        source_outline_card_title=row.source_outline_card_title,
        word_count=row.word_count,
        pause_after_seconds=row.pause_after_seconds,
        pause_hint=_enum_value(row.pause_hint),
        split_reason=_read_optional_mapping_text(metadata, "split_reason"),
        text_preview=_build_text_preview(row.text_content),
        error_message=row.error_message,
        completed_at=row.completed_at,
        preview_asset=build_session_asset_view(preview_asset),
    )


def humanize_joined_tokens(values: list[str]) -> str:
    labels = [value.replace("_", " ") for value in values]

    if len(labels) == 1:
        return labels[0]
    if len(labels) == 2:
        return f"{labels[0]} and {labels[1]}"
    return f"{', '.join(labels[:-1])}, and {labels[-1]}"


def build_audio_job_view(row: AudioJob | None) -> AudioJobView | None:
    if row is None:
        return None

    config = _read_mapping(row.config_json)
    return AudioJobView(
        id=row.id,
        status=row.status,
        voice_key=row.voice_key,
        playback_speed=row.playback_speed,
        include_background_music=row.include_background_music,
        music_profile=row.music_profile,
        progress_percent=_read_optional_mapping_float(config, "progress_percent") or 0,
        current_step=_read_optional_mapping_text(config, "current_step"),
        current_step_index=_read_optional_mapping_int(config, "current_step_index"),
        total_steps=_read_optional_mapping_int(config, "total_steps"),
        completed_segments=_read_optional_mapping_int(config, "completed_segments"),
        estimated_duration_seconds=row.estimated_duration_seconds,
        total_segments=_read_optional_mapping_int(config, "total_segments"),
        current_segment_index=row.current_segment_index,
        latest_asset_id=_read_optional_mapping_text(config, "latest_asset_id"),
        latest_asset_kind=_read_optional_mapping_text(config, "latest_asset_kind"),
        attempt_count=row.attempt_count,
        stop_reason=row.stop_reason,
        error_message=row.error_message,
        started_at=row.started_at,
        completed_at=row.completed_at,
        created_at=row.created_at,
        updated_at=row.updated_at,
    )


def build_session_asset_view(row: SessionAsset | None) -> SessionAssetView | None:
    if row is None:
        return None

    details = _read_mapping(row.metadata_json)
    access = build_session_asset_access_view(row)
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
        duration_seconds=_read_optional_mapping_float(details, "duration_seconds"),
        checksum_sha256=row.checksum_sha256,
        segment_index=row.segment_index,
        error_message=row.error_message,
        details=details or None,
        access=access,
        public_url=access.stream_path if access is not None else None,
        ready_at=row.ready_at,
        failed_at=row.failed_at,
        superseded_at=row.superseded_at,
        created_at=row.created_at,
        updated_at=row.updated_at,
    )


def _job_needs_draft_snapshot_fallback(
    job: CompositionJobView | None,
    draft_snapshot_asset: SessionAsset | None,
) -> bool:
    if job is None or draft_snapshot_asset is None:
        return False

    if job.accepted_story_so_far and job.latest_partial_output:
        return False

    if (
        draft_snapshot_asset.composition_job_id is not None
        and draft_snapshot_asset.composition_job_id != job.id
    ):
        return False

    return True


def resolve_display_title(
    *,
    working_title: str | None,
    pitch_title: str | None = None,
    story_idea: str | None = None,
    normalized_summary: str | None = None,
    raw_brief: str | None = None,
) -> str:
    for candidate in (working_title, pitch_title, story_idea, normalized_summary, raw_brief):
        normalized = normalize_optional_text(candidate)
        if normalized:
            return normalized[:120]

    return "Untitled bedtime story"


def normalize_optional_text(value: str | None) -> str | None:
    if value is None:
        return None

    normalized = value.strip()
    return normalized or None


def resolve_overall_status(
    stage_states: Mapping[WorkflowStage, WorkflowStageState],
) -> WorkflowStageState:
    statuses = tuple(stage_states.values())
    if any(status == WorkflowStageState.NEEDS_REGENERATION for status in statuses):
        return WorkflowStageState.NEEDS_REGENERATION
    if stage_states.get(WorkflowStage.FINALIZE) == WorkflowStageState.COMPLETED:
        return WorkflowStageState.COMPLETED
    if any(status == WorkflowStageState.IN_PROGRESS for status in statuses):
        return WorkflowStageState.IN_PROGRESS
    if any(status == WorkflowStageState.COMPLETED for status in statuses):
        return WorkflowStageState.IN_PROGRESS
    return WorkflowStageState.DRAFT


def resolve_furthest_completed_stage(
    stage_states: Mapping[WorkflowStage, WorkflowStageState],
) -> WorkflowStage | None:
    furthest_stage: WorkflowStage | None = None
    for stage in WORKFLOW_STAGE_SEQUENCE:
        if stage_states.get(stage) == WorkflowStageState.COMPLETED:
            furthest_stage = stage

    return furthest_stage


def is_event_newer(existing_at: datetime | None, event_at: datetime) -> bool:
    if existing_at is None:
        return True
    return normalize_sortable_datetime(event_at) >= normalize_sortable_datetime(existing_at)


def normalize_sortable_datetime(value: datetime) -> datetime:
    return value if value.tzinfo is not None else value.replace(tzinfo=event_timezone_utc())


def event_timezone_utc():
    from datetime import timezone

    return timezone.utc
