from __future__ import annotations

from dataclasses import dataclass
from uuid import uuid4

from sqlalchemy import Select, select
from sqlalchemy.orm import Session

from app.db import AudioJob, CompositionJob, CompositionJobKind, CompositionSegment, JobStatus
from app.db.base import utc_now
from app.models.events import (
    AudioProgressEventPayload,
    ChatMessageRecordedEventPayload,
    CompositionProgressEventPayload,
    SessionEventType,
    SessionEventView,
    UIActionRecordedEventPayload,
    WorkflowStageChangedEventPayload,
)
from app.models.realtime import (
    ChatContentFormat,
    ChatMessageEventPayload,
    ChatMessageRealtimeEvent,
    CompositionChunkEventPayload,
    CompositionChunkKind,
    CompositionChunkRealtimeEvent,
    JobKind,
    JobProgressEventPayload,
    JobProgressRealtimeEvent,
    JobStatusEventPayload,
    JobStatusRealtimeEvent,
    RealtimeDeliveryMode,
    RealtimeJobStatus,
    SessionRealtimeEvent,
    SessionSubscriptionAck,
    UIActionEchoEventPayload,
    UIActionEchoRealtimeEvent,
    UIActionEchoResult,
    WorkflowStageChangedRealtimeEvent,
    build_session_channel_name,
)
from app.services.composition_streaming import split_text_for_streaming
from app.services.event_log import (
    DEFAULT_LOCAL_USER_ACTOR,
    DEFAULT_SYSTEM_ACTOR,
    SessionEventLogService,
)

_ACTIVE_COMPOSITION_JOB_STATUSES = (
    JobStatus.QUEUED,
    JobStatus.IN_PROGRESS,
    JobStatus.PAUSED,
)
_REPLAYABLE_JOB_STATUS_VALUES = {
    RealtimeJobStatus.QUEUED,
    RealtimeJobStatus.PAUSED,
    RealtimeJobStatus.COMPLETED,
    RealtimeJobStatus.FAILED,
    RealtimeJobStatus.CANCELLED,
}
_COMPOSITION_COMPLETION_MESSAGE = "Writing finished and the latest draft is ready for review."


@dataclass(frozen=True)
class SessionRealtimeSubscription:
    ack: SessionSubscriptionAck
    replay_events: list[SessionRealtimeEvent]
    latest_sequence_number: int | None


@dataclass(frozen=True)
class CompositionChunkCursor:
    job_id: str | None = None
    segment_id: str | None = None
    story_text: str = ""
    latest_segment_summary: str | None = None


@dataclass(frozen=True)
class CompositionStreamState:
    job_id: str
    job_kind: CompositionJobKind
    job_status: JobStatus
    progress_percent: float
    total_segments: int | None
    current_segment_id: str
    current_segment_index: int
    current_segment_status: JobStatus | None
    current_segment_summary: str | None
    accepted_story_so_far: str
    latest_segment_summary: str | None
    latest_summary_segment_id: str | None
    latest_summary_segment_index: int | None


class SessionRealtimeService:
    def __init__(self, session: Session):
        self._session = session
        self._events = SessionEventLogService(session)

    def build_subscription(
        self,
        *,
        session_id: str,
        connection_id: str,
        last_sequence_number: int | None,
        request_id: str | None,
        tab_id: str,
    ) -> SessionRealtimeSubscription:
        history = self._events.list_session_history(
            session_id,
            limit=1,
        )
        latest_sequence_number = history.latest_sequence_number
        replay_events = self.list_realtime_events(
            session_id,
            after_sequence_number=last_sequence_number,
            delivery=RealtimeDeliveryMode.REPLAY,
        )
        replay_strategy = (
            "delta"
            if replay_events
            else "none"
        )
        replay_from_sequence_number = (
            (last_sequence_number or 0) + 1 if replay_events else None
        )

        ack = SessionSubscriptionAck(
            session_id=session_id,
            channel=build_session_channel_name(session_id),
            connection_id=connection_id,
            tab_id=tab_id,
            replay_strategy=replay_strategy,
            replay_from_sequence_number=replay_from_sequence_number,
            latest_sequence_number=latest_sequence_number,
            request_id=request_id,
            local_actor=DEFAULT_LOCAL_USER_ACTOR,
            accepted_at=utc_now(),
        )
        return SessionRealtimeSubscription(
            ack=ack,
            replay_events=replay_events,
            latest_sequence_number=latest_sequence_number,
        )

    def list_realtime_events(
        self,
        session_id: str,
        *,
        after_sequence_number: int | None,
        delivery: RealtimeDeliveryMode,
    ) -> list[SessionRealtimeEvent]:
        history = self._events.list_session_history(
            session_id,
            after_sequence_number=after_sequence_number,
        )
        realtime_events: list[SessionRealtimeEvent] = []
        for event in history.events:
            mapped = self._map_history_event(
                session_id=session_id,
                event=event,
                delivery=delivery,
            )
            if mapped is not None:
                realtime_events.append(mapped)

        return realtime_events

    def read_composition_chunk_events(
        self,
        session_id: str,
        *,
        cursor: CompositionChunkCursor,
    ) -> tuple[list[CompositionChunkRealtimeEvent], CompositionChunkCursor]:
        state = self._load_active_composition_stream_state(session_id)
        if state is None:
            return [], CompositionChunkCursor()

        next_cursor = cursor
        events: list[CompositionChunkRealtimeEvent] = []
        is_initial_baseline = (
            cursor.job_id is None
            and cursor.segment_id is None
            and cursor.story_text == ""
            and cursor.latest_segment_summary is None
        )
        if state.job_id != cursor.job_id or state.current_segment_id != cursor.segment_id:
            events.append(
                self._build_composition_chunk_event(
                    session_id=session_id,
                    state=state,
                    chunk_index=0,
                    chunk_kind=CompositionChunkKind.SEGMENT_START,
                    summary=state.current_segment_summary,
                )
            )
            next_cursor = CompositionChunkCursor(
                job_id=state.job_id,
                segment_id=state.current_segment_id,
                story_text=(
                    state.accepted_story_so_far
                    if is_initial_baseline
                    else (
                        cursor.story_text
                        if state.accepted_story_so_far.startswith(cursor.story_text)
                        else state.accepted_story_so_far
                    )
                ),
                latest_segment_summary=(
                    state.latest_segment_summary
                    if is_initial_baseline
                    else cursor.latest_segment_summary
                ),
            )

        if not state.accepted_story_so_far.startswith(next_cursor.story_text):
            next_cursor = CompositionChunkCursor(
                job_id=state.job_id,
                segment_id=state.current_segment_id,
                story_text=state.accepted_story_so_far,
                latest_segment_summary=state.latest_segment_summary,
            )
            return events, next_cursor

        delta_text = state.accepted_story_so_far[len(next_cursor.story_text) :]
        if delta_text:
            chunks = split_text_for_streaming("", delta_text)
            running_story_text = next_cursor.story_text
            for chunk_index, chunk in enumerate(chunks, start=1):
                running_story_text += chunk
                events.append(
                    self._build_composition_chunk_event(
                        session_id=session_id,
                        state=state,
                        chunk_index=chunk_index,
                        chunk_kind=CompositionChunkKind.DELTA,
                        text=chunk,
                        cumulative_character_count=len(running_story_text),
                        cumulative_word_count=_count_words(running_story_text),
                    )
                )
            next_cursor = CompositionChunkCursor(
                job_id=state.job_id,
                segment_id=state.current_segment_id,
                story_text=running_story_text,
                latest_segment_summary=next_cursor.latest_segment_summary,
            )

        if (
            state.latest_segment_summary is not None
            and state.latest_segment_summary != next_cursor.latest_segment_summary
        ):
            summary_segment_id = state.latest_summary_segment_id or state.current_segment_id
            summary_segment_index = (
                state.latest_summary_segment_index or state.current_segment_index
            )
            events.append(
                CompositionChunkRealtimeEvent(
                    event_id=_build_ephemeral_chunk_event_id(
                        state.job_id,
                        summary_segment_id,
                        "segment-summary",
                    ),
                    session_id=session_id,
                    channel=build_session_channel_name(session_id),
                    actor=DEFAULT_SYSTEM_ACTOR,
                    created_at=utc_now(),
                    payload=CompositionChunkEventPayload(
                        job_id=state.job_id,
                        segment_id=summary_segment_id,
                        segment_index=summary_segment_index,
                        chunk_index=max(len(events), 0),
                        chunk_kind=CompositionChunkKind.SEGMENT_SUMMARY,
                        summary=state.latest_segment_summary,
                        cumulative_character_count=len(state.accepted_story_so_far),
                        cumulative_word_count=_count_words(state.accepted_story_so_far),
                        is_final_chunk=state.job_status == JobStatus.COMPLETED,
                    ),
                )
            )
            next_cursor = CompositionChunkCursor(
                job_id=next_cursor.job_id,
                segment_id=next_cursor.segment_id,
                story_text=next_cursor.story_text,
                latest_segment_summary=state.latest_segment_summary,
            )

        return events, next_cursor

    def _map_history_event(
        self,
        *,
        session_id: str,
        event: SessionEventView,
        delivery: RealtimeDeliveryMode,
    ) -> SessionRealtimeEvent | None:
        if event.event_type == SessionEventType.WORKFLOW_STAGE_CHANGED.value:
            payload = WorkflowStageChangedEventPayload.model_validate(event.payload)
            return WorkflowStageChangedRealtimeEvent(
                event_id=_build_realtime_event_id(event),
                session_id=session_id,
                channel=build_session_channel_name(session_id),
                actor=event.actor,
                stage=event.stage,
                created_at=event.created_at,
                delivery=delivery,
                sequence_number=event.sequence_number,
                event_log_entry_id=event.id,
                payload=payload,
            )

        if event.event_type == SessionEventType.UI_ACTION_RECORDED.value:
            payload = UIActionRecordedEventPayload.model_validate(event.payload)
            return UIActionEchoRealtimeEvent(
                event_id=_build_realtime_event_id(event),
                session_id=session_id,
                channel=build_session_channel_name(session_id),
                actor=event.actor,
                stage=event.stage,
                created_at=event.created_at,
                delivery=delivery,
                sequence_number=event.sequence_number,
                event_log_entry_id=event.id,
                payload=UIActionEchoEventPayload(
                    action=payload.action,
                    result=UIActionEchoResult.ACCEPTED,
                    summary=payload.value_summary or event.summary,
                    control_id=payload.control_id,
                    value_summary=payload.value_summary,
                    origin=payload.origin,
                ),
            )

        if event.event_type == SessionEventType.CHAT_MESSAGE_RECORDED.value:
            payload = ChatMessageRecordedEventPayload.model_validate(event.payload)
            content_format = (
                ChatContentFormat(payload.content_format)
                if payload.content_format in {mode.value for mode in ChatContentFormat}
                else ChatContentFormat.PLAIN_TEXT
            )
            return ChatMessageRealtimeEvent(
                event_id=_build_realtime_event_id(event),
                session_id=session_id,
                channel=build_session_channel_name(session_id),
                actor=event.actor,
                stage=event.stage,
                created_at=event.created_at,
                delivery=delivery,
                sequence_number=event.sequence_number,
                event_log_entry_id=event.id,
                payload=ChatMessageEventPayload(
                    message_id=payload.message_id or f"chat-{event.sequence_number}",
                    message_role=payload.message_role,
                    content=payload.content or payload.content_preview,
                    content_format=content_format,
                    source=payload.source,
                ),
            )

        if event.event_type == SessionEventType.COMPOSITION_PROGRESS_RECORDED.value:
            payload = CompositionProgressEventPayload.model_validate(event.payload)
            return self._build_composition_job_event(
                session_id=session_id,
                event=event,
                payload=payload,
                delivery=delivery,
            )

        if event.event_type == SessionEventType.AUDIO_PROGRESS_RECORDED.value:
            payload = AudioProgressEventPayload.model_validate(event.payload)
            return self._build_audio_job_event(
                session_id=session_id,
                event=event,
                payload=payload,
                delivery=delivery,
            )

        return None

    def _build_composition_job_event(
        self,
        *,
        session_id: str,
        event: SessionEventView,
        payload: CompositionProgressEventPayload,
        delivery: RealtimeDeliveryMode,
    ) -> SessionRealtimeEvent:
        job = self._session.get(CompositionJob, payload.job_id)
        segment = self._load_segment(
            session_id=session_id,
            segment_id=payload.segment_id,
            fallback_segment_index=payload.current_segment_index,
        )
        status = RealtimeJobStatus(payload.status)
        total_segments = payload.total_segments or _read_metadata_int(job, "total_segments")
        current_segment_index = payload.current_segment_index
        completed_segments = _resolve_completed_segments(
            job=job,
            current_segment_index=current_segment_index,
            total_segments=total_segments,
            status=status,
        )
        message = _build_composition_message(
            job=job,
            current_segment_index=current_segment_index,
            interruption_request=payload.interruption_request,
            planned_summary=segment.planned_summary if segment is not None else None,
            progress_percent=payload.progress_percent,
            status=status,
            total_segments=total_segments,
        )

        if status in _REPLAYABLE_JOB_STATUS_VALUES:
            return JobStatusRealtimeEvent(
                event_id=_build_realtime_event_id(event),
                session_id=session_id,
                channel=build_session_channel_name(session_id),
                actor=event.actor,
                stage=event.stage,
                created_at=event.created_at,
                delivery=delivery,
                sequence_number=event.sequence_number,
                event_log_entry_id=event.id,
                payload=JobStatusEventPayload(
                    job_id=payload.job_id,
                    job_kind=JobKind.COMPOSITION,
                    status=status,
                    message=message,
                    stop_reason=job.stop_reason if job is not None else None,
                    error_message=job.error_message if job is not None else None,
                    current_segment_index=current_segment_index,
                    total_segments=total_segments,
                    interruption_request=payload.interruption_request,
                ),
            )

        return JobProgressRealtimeEvent(
            event_id=_build_realtime_event_id(event),
            session_id=session_id,
            channel=build_session_channel_name(session_id),
            actor=event.actor,
            stage=event.stage,
            created_at=event.created_at,
            delivery=delivery,
            sequence_number=event.sequence_number,
            event_log_entry_id=event.id,
            payload=JobProgressEventPayload(
                job_id=payload.job_id,
                job_kind=JobKind.COMPOSITION,
                status=status,
                progress_percent=payload.progress_percent,
                current_step=segment.planned_summary if segment is not None else None,
                current_step_index=current_segment_index,
                total_steps=total_segments,
                completed_segments=completed_segments,
                current_segment_index=current_segment_index,
                total_segments=total_segments,
                segment_id=payload.segment_id,
                segment_status=segment.status.value if segment is not None else None,
                message=message,
                interruption_request=payload.interruption_request,
            ),
        )

    def _build_audio_job_event(
        self,
        *,
        session_id: str,
        event: SessionEventView,
        payload: AudioProgressEventPayload,
        delivery: RealtimeDeliveryMode,
    ) -> SessionRealtimeEvent:
        job = self._session.get(AudioJob, payload.job_id)
        status = RealtimeJobStatus(payload.status)
        total_segments = payload.total_segments
        message = _build_audio_message(
            estimated_duration_seconds=payload.estimated_duration_seconds,
            progress_percent=payload.progress_percent,
            status=status,
        )

        if status in _REPLAYABLE_JOB_STATUS_VALUES:
            return JobStatusRealtimeEvent(
                event_id=_build_realtime_event_id(event),
                session_id=session_id,
                channel=build_session_channel_name(session_id),
                actor=event.actor,
                stage=event.stage,
                created_at=event.created_at,
                delivery=delivery,
                sequence_number=event.sequence_number,
                event_log_entry_id=event.id,
                payload=JobStatusEventPayload(
                    job_id=payload.job_id,
                    job_kind=JobKind.AUDIO,
                    status=status,
                    message=message,
                    stop_reason=job.stop_reason if job is not None else None,
                    error_message=job.error_message if job is not None else None,
                    current_segment_index=payload.current_segment_index,
                    total_segments=total_segments,
                ),
            )

        return JobProgressRealtimeEvent(
            event_id=_build_realtime_event_id(event),
            session_id=session_id,
            channel=build_session_channel_name(session_id),
            actor=event.actor,
            stage=event.stage,
            created_at=event.created_at,
            delivery=delivery,
            sequence_number=event.sequence_number,
            event_log_entry_id=event.id,
            payload=JobProgressEventPayload(
                job_id=payload.job_id,
                job_kind=JobKind.AUDIO,
                status=status,
                progress_percent=payload.progress_percent,
                current_step_index=payload.current_segment_index,
                total_steps=total_segments,
                current_segment_index=payload.current_segment_index,
                total_segments=total_segments,
                segment_id=payload.segment_id,
                estimated_duration_seconds=payload.estimated_duration_seconds,
                message=message,
            ),
        )

    def _load_active_composition_stream_state(
        self,
        session_id: str,
    ) -> CompositionStreamState | None:
        stmt: Select[tuple[CompositionJob]] = (
            select(CompositionJob)
            .where(
                CompositionJob.session_id == session_id,
                CompositionJob.status.in_(_ACTIVE_COMPOSITION_JOB_STATUSES),
            )
            .order_by(CompositionJob.updated_at.desc())
            .limit(1)
        )
        job = self._session.execute(stmt).scalar_one_or_none()
        if job is None or job.current_segment_index is None:
            return None

        metadata = job.metadata_json if isinstance(job.metadata_json, dict) else {}
        current_segment_id = metadata.get("current_segment_id")
        current_segment = self._load_segment(
            session_id=session_id,
            segment_id=current_segment_id if isinstance(current_segment_id, str) else None,
            fallback_segment_index=job.current_segment_index,
        )
        if current_segment is None:
            return None

        latest_completed_segment = self._load_latest_completed_segment(
            session_id=session_id,
            before_segment_index=None,
        )
        accepted_story_so_far = metadata.get("accepted_story_so_far")
        if not isinstance(accepted_story_so_far, str):
            accepted_story_so_far = (
                current_segment.accepted_text
                or current_segment.text_content
                or ""
            )

        latest_segment_summary = metadata.get("latest_segment_summary")
        if not isinstance(latest_segment_summary, str):
            latest_segment_summary = (
                latest_completed_segment.accepted_summary
                if latest_completed_segment is not None
                else None
            )

        return CompositionStreamState(
            job_id=job.id,
            job_kind=job.job_kind,
            job_status=job.status,
            progress_percent=job.progress_percent,
            total_segments=_read_metadata_int(job, "total_segments"),
            current_segment_id=current_segment.id,
            current_segment_index=current_segment.segment_index,
            current_segment_status=current_segment.status,
            current_segment_summary=current_segment.planned_summary,
            accepted_story_so_far=accepted_story_so_far,
            latest_segment_summary=latest_segment_summary,
            latest_summary_segment_id=(
                latest_completed_segment.id if latest_completed_segment is not None else None
            ),
            latest_summary_segment_index=(
                latest_completed_segment.segment_index
                if latest_completed_segment is not None
                else None
            ),
        )

    def _load_segment(
        self,
        *,
        session_id: str,
        segment_id: str | None,
        fallback_segment_index: int | None,
    ) -> CompositionSegment | None:
        if segment_id is not None:
            segment = self._session.get(CompositionSegment, segment_id)
            if segment is not None and segment.session_id == session_id:
                return segment

        if fallback_segment_index is None:
            return None

        stmt: Select[tuple[CompositionSegment]] = (
            select(CompositionSegment)
            .where(
                CompositionSegment.session_id == session_id,
                CompositionSegment.segment_index == fallback_segment_index,
            )
            .order_by(CompositionSegment.revision_number.desc())
            .limit(1)
        )
        return self._session.execute(stmt).scalar_one_or_none()

    def _load_latest_completed_segment(
        self,
        *,
        session_id: str,
        before_segment_index: int | None,
    ) -> CompositionSegment | None:
        stmt: Select[tuple[CompositionSegment]] = (
            select(CompositionSegment)
            .where(
                CompositionSegment.session_id == session_id,
                CompositionSegment.status == JobStatus.COMPLETED,
            )
            .order_by(
                CompositionSegment.segment_index.desc(),
                CompositionSegment.revision_number.desc(),
            )
            .limit(1)
        )
        if before_segment_index is not None:
            stmt = stmt.where(CompositionSegment.segment_index < before_segment_index)

        return self._session.execute(stmt).scalar_one_or_none()

    def _build_composition_chunk_event(
        self,
        *,
        session_id: str,
        state: CompositionStreamState,
        chunk_index: int,
        chunk_kind: CompositionChunkKind,
        text: str | None = None,
        summary: str | None = None,
        cumulative_character_count: int | None = None,
        cumulative_word_count: int | None = None,
    ) -> CompositionChunkRealtimeEvent:
        return CompositionChunkRealtimeEvent(
            event_id=_build_ephemeral_chunk_event_id(
                state.job_id,
                state.current_segment_id,
                f"{chunk_kind.value}-{chunk_index}",
            ),
            session_id=session_id,
            channel=build_session_channel_name(session_id),
            actor=DEFAULT_SYSTEM_ACTOR,
            created_at=utc_now(),
            payload=CompositionChunkEventPayload(
                job_id=state.job_id,
                segment_id=state.current_segment_id,
                segment_index=state.current_segment_index,
                chunk_index=chunk_index,
                chunk_kind=chunk_kind,
                text=text,
                summary=summary,
                cumulative_character_count=cumulative_character_count,
                cumulative_word_count=cumulative_word_count,
                is_final_chunk=state.job_status == JobStatus.COMPLETED,
            ),
        )


def _build_realtime_event_id(event: SessionEventView) -> str:
    return f"rt-{event.sequence_number}-{event.id}"


def _build_ephemeral_chunk_event_id(job_id: str, segment_id: str, suffix: str) -> str:
    return f"rt-chunk-{job_id}-{segment_id}-{suffix}-{uuid4()}"


def _build_composition_message(
    *,
    job: CompositionJob | None,
    current_segment_index: int | None,
    interruption_request,
    planned_summary: str | None,
    progress_percent: float | None,
    status: RealtimeJobStatus,
    total_segments: int | None,
) -> str:
    if interruption_request is not None:
        return interruption_request.message

    if status == RealtimeJobStatus.QUEUED:
        if job is not None and job.job_kind == CompositionJobKind.REWRITE:
            return (
                f"Queued a rewrite from segment {current_segment_index} of {total_segments}."
                if current_segment_index is not None and total_segments is not None
                else "Queued a rewrite."
            )
        if progress_percent not in (None, 0):
            return (
                f"Queued writing to resume at segment {current_segment_index} of {total_segments}."
                if current_segment_index is not None and total_segments is not None
                else "Queued writing to resume."
            )
        return (
            f"Queued writing from segment {current_segment_index} of {total_segments}."
            if current_segment_index is not None and total_segments is not None
            else "Queued writing."
        )

    if status == RealtimeJobStatus.IN_PROGRESS:
        if current_segment_index is not None and total_segments is not None and planned_summary:
            return (
                f"Composing segment {current_segment_index} of {total_segments}. "
                f"{planned_summary}"
            )
        if current_segment_index is not None and total_segments is not None:
            return f"Composing segment {current_segment_index} of {total_segments}."
        if progress_percent is not None:
            return f"Writing {round(progress_percent)}% complete."
        return "Writing is in progress."

    if status == RealtimeJobStatus.PAUSED:
        if progress_percent is not None:
            return f"Writing paused at {round(progress_percent)}% complete."
        return "Writing is paused."

    if status == RealtimeJobStatus.COMPLETED:
        return _COMPOSITION_COMPLETION_MESSAGE

    if status == RealtimeJobStatus.CANCELLED:
        return job.stop_reason if job is not None and job.stop_reason else "Writing was cancelled."

    return job.error_message if job is not None and job.error_message else "Writing failed."


def _build_audio_message(
    *,
    estimated_duration_seconds: int | None,
    progress_percent: float | None,
    status: RealtimeJobStatus,
) -> str:
    if status == RealtimeJobStatus.IN_PROGRESS and progress_percent is not None:
        return f"Narration {round(progress_percent)}% complete."
    if status == RealtimeJobStatus.COMPLETED:
        if estimated_duration_seconds is not None:
            minutes = max(round(estimated_duration_seconds / 60), 1)
            return f"Narration completed. Estimated length {minutes} min."
        return "Narration completed."
    return f"Narration {status.value.replace('_', ' ')}."


def _resolve_completed_segments(
    *,
    job: CompositionJob | None,
    current_segment_index: int | None,
    total_segments: int | None,
    status: RealtimeJobStatus,
) -> int | None:
    if total_segments is None:
        return None
    if status == RealtimeJobStatus.COMPLETED:
        return total_segments
    if current_segment_index is None or job is None:
        return None

    start_segment_index = _read_metadata_int(job, "start_segment_index")
    if start_segment_index is None:
        return None
    return max(current_segment_index - start_segment_index, 0)


def _read_metadata_int(job: CompositionJob | None, key: str) -> int | None:
    if job is None or not isinstance(job.metadata_json, dict):
        return None
    value = job.metadata_json.get(key)
    return value if isinstance(value, int) and value >= 0 else None


def _count_words(text: str) -> int:
    return len([part for part in text.split() if part.strip()])
