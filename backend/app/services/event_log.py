from __future__ import annotations

from collections.abc import Mapping, Sequence
from enum import Enum
from typing import Any

from sqlalchemy.orm import Session

from app.db import EventActorType, EventLogEntry
from app.models import WorkflowStage, WorkflowStageState
from app.models.events import (
    AIOutputKind,
    AIOutputRecordedEventPayload,
    AudioProgressEventPayload,
    ChatIntentParsedEventPayload,
    ChatMessageRecordedEventPayload,
    ChatMessageRole,
    CompositionProgressEventPayload,
    EventPayload,
    SelectionKind,
    SelectionRecordedEventPayload,
    SessionCreatedEventPayload,
    SessionEventActor,
    SessionEventType,
    SessionEventView,
    SessionHistoryView,
    UIActionRecordedEventPayload,
    UserEditRecordedEventPayload,
    UserEditTargetKind,
    WorkflowStageChangedEventPayload,
    parse_event_payload,
    serialize_event_payload,
)
from app.models.intent_parser import ParsedChatIntentResponse
from app.repositories import EventLogRepository
from app.services.conversation_memory import SessionMemoryService

DEFAULT_LOCAL_USER_ACTOR = SessionEventActor(
    actor_type=EventActorType.USER,
    actor_id="local-user",
)
DEFAULT_ASSISTANT_ACTOR = SessionEventActor(
    actor_type=EventActorType.ASSISTANT,
    actor_id="story-planner",
)
DEFAULT_SYSTEM_ACTOR = SessionEventActor(
    actor_type=EventActorType.SYSTEM,
    actor_id="worker",
)
DEFAULT_INTENT_PARSER_ACTOR = SessionEventActor(
    actor_type=EventActorType.SERVICE,
    actor_id="intent-parser",
)


class SessionEventLogService:
    def __init__(self, session: Session):
        self._session = session
        self._events = EventLogRepository(session)

    def append_event(
        self,
        session_id: str,
        *,
        actor: SessionEventActor,
        event_type: SessionEventType | str,
        summary: str,
        payload: EventPayload | Mapping[str, Any] | None = None,
        stage: WorkflowStage | None = None,
    ) -> EventLogEntry:
        normalized_summary = summary.strip()
        if not normalized_summary:
            raise ValueError("event summary must not be empty")

        return self._events.append(
            session_id=session_id,
            actor_type=actor.actor_type,
            actor_id=actor.actor_id,
            event_type=_enum_value(event_type),
            summary=normalized_summary,
            payload=serialize_event_payload(payload),
            stage=stage,
        )

    def list_session_history(
        self,
        session_id: str,
        *,
        limit: int | None = None,
        after_sequence_number: int | None = None,
    ) -> SessionHistoryView:
        rows = self._events.list_for_session(
            session_id,
            limit=limit,
            after_sequence_number=after_sequence_number,
        )
        latest_sequence_number = self._events.get_latest_sequence_number(session_id)
        return SessionHistoryView(
            session_id=session_id,
            latest_sequence_number=latest_sequence_number,
            events=[_build_session_event_view(row) for row in rows],
        )

    def build_event_view(self, entry: EventLogEntry) -> SessionEventView:
        return _build_session_event_view(entry)

    def record_session_created(
        self,
        session_id: str,
        *,
        working_title: str | None,
        actor: SessionEventActor | None = None,
    ) -> EventLogEntry:
        title = working_title or "Untitled bedtime story"
        event = self.append_event(
            session_id,
            actor=actor or DEFAULT_LOCAL_USER_ACTOR,
            event_type=SessionEventType.SESSION_CREATED,
            summary=f"Created session: {title}.",
            payload=SessionCreatedEventPayload(working_title=working_title),
        )
        self._refresh_memory_snapshot(session_id, event)
        return event

    def record_stage_state_changed(
        self,
        session_id: str,
        *,
        stage: WorkflowStage,
        previous_status: WorkflowStageState,
        status: WorkflowStageState,
        detail: str | None,
        invalidated_stages: Sequence[WorkflowStage],
        current_stage: WorkflowStage,
        resume_stage: WorkflowStage,
        furthest_completed_stage: WorkflowStage | None,
        overall_status: WorkflowStageState,
        actor: SessionEventActor | None = None,
    ) -> EventLogEntry:
        invalidated = list(invalidated_stages)
        if invalidated:
            invalidated_summary = ", ".join(stage_id.value for stage_id in invalidated)
            summary = (
                f"Updated {stage.value} stage to {status.value} and invalidated "
                f"{invalidated_summary}."
            )
        else:
            summary = f"Updated {stage.value} stage to {status.value}."

        event = self.append_event(
            session_id,
            actor=actor or DEFAULT_LOCAL_USER_ACTOR,
            event_type=SessionEventType.WORKFLOW_STAGE_CHANGED,
            summary=summary,
            stage=stage,
            payload=WorkflowStageChangedEventPayload(
                previous_status=previous_status,
                status=status,
                detail=detail,
                invalidated_stages=invalidated,
                current_stage=current_stage,
                resume_stage=resume_stage,
                furthest_completed_stage=furthest_completed_stage,
                overall_status=overall_status,
            ),
        )
        self._refresh_memory_snapshot(session_id, event)
        return event

    def record_selection(
        self,
        session_id: str,
        *,
        selection_kind: SelectionKind,
        stage: WorkflowStage | None,
        label: str | None = None,
        selection_id: str | None = None,
        slug: str | None = None,
        rationale: str | None = None,
        previous_selection_id: str | None = None,
        source: str = "ui",
        accepted: bool = True,
        actor: SessionEventActor | None = None,
    ) -> EventLogEntry:
        selection_label = label or slug or selection_id or selection_kind.value
        action = "Selected" if accepted else "Recorded candidate"
        event = self.append_event(
            session_id,
            actor=actor or DEFAULT_LOCAL_USER_ACTOR,
            event_type=SessionEventType.SELECTION_RECORDED,
            summary=f"{action} {selection_kind.value.replace('_', ' ')}: {selection_label}.",
            stage=stage,
            payload=SelectionRecordedEventPayload(
                selection_kind=selection_kind,
                selection_id=selection_id,
                slug=slug,
                label=label,
                rationale=rationale,
                previous_selection_id=previous_selection_id,
                source=source,
                accepted=accepted,
            ),
        )
        self._refresh_memory_snapshot(session_id, event)
        return event

    def record_ai_output(
        self,
        session_id: str,
        *,
        output_kind: AIOutputKind,
        stage: WorkflowStage | None,
        resource_id: str | None = None,
        generation_key: str | None = None,
        candidate_count: int | None = None,
        model_id: str | None = None,
        summary_text: str | None = None,
        actor: SessionEventActor | None = None,
    ) -> EventLogEntry:
        event = self.append_event(
            session_id,
            actor=actor or DEFAULT_ASSISTANT_ACTOR,
            event_type=SessionEventType.AI_OUTPUT_RECORDED,
            summary=f"Recorded AI output for {output_kind.value}.",
            stage=stage,
            payload=AIOutputRecordedEventPayload(
                output_kind=output_kind,
                resource_id=resource_id,
                generation_key=generation_key,
                candidate_count=candidate_count,
                model_id=model_id,
                summary=summary_text,
            ),
        )
        self._refresh_memory_snapshot(session_id, event)
        return event

    def record_user_edit(
        self,
        session_id: str,
        *,
        target_kind: UserEditTargetKind,
        stage: WorkflowStage | None,
        changed_fields: Sequence[str],
        target_id: str | None = None,
        revision_number: int | None = None,
        changed_item_keys: Sequence[str] = (),
        regenerated_item_keys: Sequence[str] = (),
        change_impact: str | None = None,
        reordered: bool = False,
        refreshes_downstream: bool = False,
        invalidated_stages: Sequence[WorkflowStage] = (),
        source: str = "ui",
        field_values: Mapping[str, Any] | None = None,
        summary_text: str | None = None,
        actor: SessionEventActor | None = None,
    ) -> EventLogEntry:
        event = self.append_event(
            session_id,
            actor=actor or DEFAULT_LOCAL_USER_ACTOR,
            event_type=SessionEventType.USER_EDIT_RECORDED,
            summary=f"Saved user edit for {target_kind.value.replace('_', ' ')}.",
            stage=stage,
            payload=UserEditRecordedEventPayload(
                target_kind=target_kind,
                target_id=target_id,
                revision_number=revision_number,
                changed_fields=list(changed_fields),
                changed_item_keys=list(changed_item_keys),
                regenerated_item_keys=list(regenerated_item_keys),
                change_impact=change_impact,
                reordered=reordered,
                refreshes_downstream=refreshes_downstream,
                invalidated_stages=list(invalidated_stages),
                source=source,
                field_values=dict(field_values) if field_values is not None else None,
                summary_text=summary_text,
            ),
        )
        self._refresh_memory_snapshot(session_id, event)
        return event

    def record_chat_message(
        self,
        session_id: str,
        *,
        message_role: ChatMessageRole,
        content: str,
        stage: WorkflowStage | None = None,
        message_id: str | None = None,
        source: str = "chat",
        actor: SessionEventActor | None = None,
    ) -> EventLogEntry:
        normalized_content = content.strip()
        return self.append_event(
            session_id,
            actor=actor or _default_actor_for_chat_role(message_role),
            event_type=SessionEventType.CHAT_MESSAGE_RECORDED,
            summary=f"Recorded {message_role.value} chat message.",
            stage=stage,
            payload=ChatMessageRecordedEventPayload(
                message_role=message_role,
                message_id=message_id,
                content_preview=_truncate_preview(normalized_content),
                content_length=len(normalized_content),
                source=source,
            ),
        )

    def record_chat_intent_parsed(
        self,
        session_id: str,
        *,
        prompt_version: str,
        model_id: str,
        current_stage: WorkflowStage,
        stage_label: str,
        stage_description: str,
        stage_status: WorkflowStageState,
        stage_detail: str | None,
        session_summary: str,
        user_message: str,
        rendered_prompt: str,
        result: ParsedChatIntentResponse,
        raw_response: Mapping[str, Any] | list[Any] | str | None = None,
        actor: SessionEventActor | None = None,
    ) -> EventLogEntry:
        action_count = len(result.proposed_actions.actions)
        if action_count == 0:
            summary = "Parsed chat intent without actionable UI changes."
        elif action_count == 1:
            summary = "Parsed chat intent into 1 proposed action."
        else:
            summary = f"Parsed chat intent into {action_count} proposed actions."

        return self.append_event(
            session_id,
            actor=actor or DEFAULT_INTENT_PARSER_ACTOR,
            event_type=SessionEventType.CHAT_INTENT_PARSED,
            summary=summary,
            stage=current_stage,
            payload=ChatIntentParsedEventPayload(
                prompt_version=prompt_version,
                model_id=model_id,
                current_stage=current_stage,
                stage_label=stage_label,
                stage_description=stage_description,
                stage_status=stage_status,
                stage_detail=stage_detail,
                session_summary=session_summary,
                user_message=user_message,
                rendered_prompt=rendered_prompt,
                result=result,
                raw_response=raw_response,
            ),
        )

    def record_ui_action(
        self,
        session_id: str,
        *,
        action: str,
        stage: WorkflowStage | None = None,
        control_id: str | None = None,
        value_summary: str | None = None,
        origin: str = "workspace",
        actor: SessionEventActor | None = None,
    ) -> EventLogEntry:
        return self.append_event(
            session_id,
            actor=actor or DEFAULT_LOCAL_USER_ACTOR,
            event_type=SessionEventType.UI_ACTION_RECORDED,
            summary=f"Recorded UI action: {action}.",
            stage=stage,
            payload=UIActionRecordedEventPayload(
                action=action,
                control_id=control_id,
                value_summary=value_summary,
                origin=origin,
            ),
        )

    def record_composition_progress(
        self,
        session_id: str,
        *,
        job_id: str,
        status: str | Enum,
        progress_percent: float | None = None,
        current_segment_index: int | None = None,
        total_segments: int | None = None,
        segment_id: str | None = None,
        actor: SessionEventActor | None = None,
    ) -> EventLogEntry:
        summary = (
            f"Composition progress {progress_percent:.1f}%."
            if progress_percent is not None
            else "Recorded composition progress."
        )
        event = self.append_event(
            session_id,
            actor=actor or DEFAULT_SYSTEM_ACTOR,
            event_type=SessionEventType.COMPOSITION_PROGRESS_RECORDED,
            summary=summary,
            stage=WorkflowStage.COMPOSITION,
            payload=CompositionProgressEventPayload(
                job_id=job_id,
                status=_enum_value(status),
                progress_percent=progress_percent,
                current_segment_index=current_segment_index,
                total_segments=total_segments,
                segment_id=segment_id,
            ),
        )
        if _should_refresh_memory_for_job_status(_enum_value(status)):
            self._refresh_memory_snapshot(session_id, event)
        return event

    def record_audio_progress(
        self,
        session_id: str,
        *,
        job_id: str,
        status: str | Enum,
        progress_percent: float | None = None,
        current_segment_index: int | None = None,
        total_segments: int | None = None,
        segment_id: str | None = None,
        estimated_duration_seconds: int | None = None,
        voice_key: str | None = None,
        actor: SessionEventActor | None = None,
    ) -> EventLogEntry:
        summary = (
            f"Audio progress {progress_percent:.1f}%."
            if progress_percent is not None
            else "Recorded audio progress."
        )
        event = self.append_event(
            session_id,
            actor=actor or DEFAULT_SYSTEM_ACTOR,
            event_type=SessionEventType.AUDIO_PROGRESS_RECORDED,
            summary=summary,
            stage=WorkflowStage.AUDIO,
            payload=AudioProgressEventPayload(
                job_id=job_id,
                status=_enum_value(status),
                progress_percent=progress_percent,
                current_segment_index=current_segment_index,
                total_segments=total_segments,
                segment_id=segment_id,
                estimated_duration_seconds=estimated_duration_seconds,
                voice_key=voice_key,
            ),
        )
        if _should_refresh_memory_for_job_status(_enum_value(status)):
            self._refresh_memory_snapshot(session_id, event)
        return event

    def _refresh_memory_snapshot(
        self,
        session_id: str,
        event: EventLogEntry,
    ) -> None:
        SessionMemoryService(self._session).refresh_summary(
            session_id,
            trigger_event=event,
        )


def _build_session_event_view(row: EventLogEntry) -> SessionEventView:
    return SessionEventView(
        id=row.id,
        session_id=row.session_id,
        sequence_number=row.sequence_number,
        actor=SessionEventActor(
            actor_type=row.actor_type,
            actor_id=row.actor_id,
        ),
        event_type=row.event_type,
        stage=row.stage,
        summary=row.summary,
        payload=parse_event_payload(row.event_type, row.payload),
        created_at=row.created_at,
    )


def _default_actor_for_chat_role(message_role: ChatMessageRole) -> SessionEventActor:
    if message_role == ChatMessageRole.USER:
        return DEFAULT_LOCAL_USER_ACTOR
    if message_role == ChatMessageRole.ASSISTANT:
        return DEFAULT_ASSISTANT_ACTOR
    return DEFAULT_SYSTEM_ACTOR


def _enum_value(value: str | Enum) -> str:
    if isinstance(value, Enum):
        return value.value
    return value


def _truncate_preview(value: str, *, limit: int = 160) -> str:
    if len(value) <= limit:
        return value
    return f"{value[: limit - 3].rstrip()}..."


def _should_refresh_memory_for_job_status(status: str) -> bool:
    return status in {"paused", "failed", "cancelled", "completed"}
