from __future__ import annotations

from collections.abc import Mapping
from datetime import datetime

from sqlalchemy.orm import Session

from app.db import AudioJob, CompositionJob, JobStatus, SessionAsset
from app.models import (
    WORKFLOW_STAGE_SEQUENCE,
    AudioJobView,
    AudioProgressEventPayload,
    BeatSheetView,
    CharacterSheetView,
    CompositionJobView,
    CompositionProgressEventPayload,
    ConversationMemorySnapshotView,
    NormalizedBriefPreferences,
    PitchBatchView,
    PitchView,
    RecentSessionSummary,
    SessionAssetView,
    SessionCatalogSelection,
    SessionEventType,
    SessionHydrationMetadata,
    SessionHydrationView,
    SessionProgress,
    SessionSnapshot,
    SessionStageStateView,
    StoryBriefView,
    StorySetupView,
    WorkflowStage,
    WorkflowStageChangedEventPayload,
    WorkflowStageState,
    get_workflow_stage_definition,
    resolve_resume_stage,
)
from app.repositories import SessionAggregate, StorySessionRepository
from app.services.agent_context import build_session_agent_context_summary
from app.services.conversation_memory import SessionMemoryService
from app.services.event_log import SessionEventLogService

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
    def __init__(self, session: Session):
        self._session = session
        self._sessions = StorySessionRepository(session)
        self._memory = SessionMemoryService(session)
        self._events = SessionEventLogService(session)

    def load_session_snapshot(self, session_id: str) -> SessionSnapshot:
        aggregate = self._sessions.get_aggregate(session_id)
        if aggregate is None:
            raise SessionHydrationNotFoundError(f"session {session_id!r} was not found")

        return build_session_snapshot(
            aggregate,
            conversation_memory=self._memory.load_latest_snapshot(session_id),
        )

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
) -> SessionSnapshot:
    story_session = aggregate.session
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
        selected_character_sheet=build_character_sheet_view(aggregate.selected_character_sheet),
        selected_beat_sheet=build_beat_sheet_view(aggregate.selected_beat_sheet),
        selected_story_setup=build_story_setup_view(aggregate.selected_story_setup),
        latest_composition_job=build_composition_job_view(aggregate.latest_composition_job),
        latest_audio_job=build_audio_job_view(aggregate.latest_audio_job),
        active_composition_job=build_composition_job_view(aggregate.active_composition_job),
        active_audio_job=build_audio_job_view(aggregate.active_audio_job),
        latest_story_asset=build_session_asset_view(aggregate.latest_story_asset),
        latest_audio_asset=build_session_asset_view(aggregate.latest_audio_asset),
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
    return CompositionJobView(
        id=payload.job_id,
        job_kind=current_job.job_kind if current_job is not None else "draft",
        status=payload.status,
        progress_percent=progress_percent,
        current_segment_index=(
            payload.current_segment_index
            if payload.current_segment_index is not None
            else current_job.current_segment_index
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
        estimated_duration_seconds=(
            payload.estimated_duration_seconds
            if payload.estimated_duration_seconds is not None
            else current_job.estimated_duration_seconds
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
    if job.status == JobStatus.COMPLETED.value:
        return "Narration finished and the latest audio is ready for review."
    if job.status == JobStatus.PAUSED.value:
        return "Narration is paused."
    if job.status == JobStatus.FAILED.value:
        return "Narration failed and needs another pass."
    if job.estimated_duration_seconds is not None:
        minutes = round(job.estimated_duration_seconds / 60)
        return f"Narration {job.status.replace('_', ' ')}. Estimated length {minutes} min."
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
        batch_created_at[row.generation_key] = min(
            batch_created_at.get(row.generation_key, row.created_at),
            row.created_at,
        )

    ordered_keys = sorted(
        batches,
        key=lambda generation_key: (
            batch_created_at[generation_key],
            generation_key,
        ),
        reverse=True,
    )

    return [
        PitchBatchView(
            generation_key=generation_key,
            candidate_count=len(batches[generation_key]),
            created_at=batch_created_at[generation_key],
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


def build_character_sheet_view(row) -> CharacterSheetView | None:
    if row is None:
        return None

    return CharacterSheetView(
        id=row.id,
        revision_number=row.revision_number,
        title=row.title,
        protagonist_name=row.protagonist_name,
        summary=row.summary,
        supporting_cast=row.supporting_cast,
        bedtime_notes=row.bedtime_notes,
        accepted_at=row.accepted_at,
    )


def build_beat_sheet_view(row) -> BeatSheetView | None:
    if row is None:
        return None

    return BeatSheetView(
        id=row.id,
        revision_number=row.revision_number,
        summary=row.summary,
        beats=row.beats,
        bedtime_notes=row.bedtime_notes,
        accepted_at=row.accepted_at,
    )


def build_story_setup_view(row) -> StorySetupView | None:
    if row is None:
        return None

    return StorySetupView(
        id=row.id,
        revision_number=row.revision_number,
        target_word_count=row.target_word_count,
        target_runtime_minutes=row.target_runtime_minutes,
        chapter_count=row.chapter_count,
        chapter_style=row.chapter_style,
        guidance_notes=row.guidance_notes,
        preferences=row.preferences,
        accepted_at=row.accepted_at,
    )


def build_composition_job_view(row: CompositionJob | None) -> CompositionJobView | None:
    if row is None:
        return None

    return CompositionJobView(
        id=row.id,
        job_kind=row.job_kind,
        status=row.status,
        progress_percent=row.progress_percent,
        current_segment_index=row.current_segment_index,
        attempt_count=row.attempt_count,
        stop_reason=row.stop_reason,
        error_message=row.error_message,
        started_at=row.started_at,
        completed_at=row.completed_at,
        created_at=row.created_at,
        updated_at=row.updated_at,
    )


def build_audio_job_view(row: AudioJob | None) -> AudioJobView | None:
    if row is None:
        return None

    return AudioJobView(
        id=row.id,
        status=row.status,
        voice_key=row.voice_key,
        playback_speed=row.playback_speed,
        include_background_music=row.include_background_music,
        music_profile=row.music_profile,
        estimated_duration_seconds=row.estimated_duration_seconds,
        current_segment_index=row.current_segment_index,
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

    return SessionAssetView(
        id=row.id,
        asset_kind=row.asset_kind,
        status=row.status,
        storage_bucket=row.storage_bucket,
        object_path=row.object_path,
        mime_type=row.mime_type,
        byte_size=row.byte_size,
        checksum_sha256=row.checksum_sha256,
        segment_index=row.segment_index,
        error_message=row.error_message,
        ready_at=row.ready_at,
        failed_at=row.failed_at,
        created_at=row.created_at,
        updated_at=row.updated_at,
    )


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
