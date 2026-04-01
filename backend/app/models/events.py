from __future__ import annotations

from collections.abc import Mapping
from datetime import datetime
from enum import Enum
from typing import Any, TypeAlias

from pydantic import BaseModel, ConfigDict, Field

from app.models.intent_parser import ParsedChatIntentResponse
from app.models.workflow import WorkflowStage, WorkflowStageState


class SessionEventType(str, Enum):
    SESSION_CREATED = "session.created"
    WORKFLOW_STAGE_CHANGED = "workflow.stage_changed"
    SELECTION_RECORDED = "selection.recorded"
    AI_OUTPUT_RECORDED = "ai.output.recorded"
    USER_EDIT_RECORDED = "content.user_edit.recorded"
    CHAT_MESSAGE_RECORDED = "chat.message.recorded"
    CHAT_INTENT_PARSED = "chat.intent.parsed"
    UI_ACTION_RECORDED = "ui.action.recorded"
    COMPOSITION_PROGRESS_RECORDED = "composition.progress.recorded"
    AUDIO_PROGRESS_RECORDED = "audio.progress.recorded"


class SelectionKind(str, Enum):
    GENRE = "genre"
    TONE_PROFILE = "tone_profile"
    PITCH = "pitch"
    CHARACTER_SHEET = "character_sheet"
    BEAT_SHEET = "beat_sheet"
    STORY_SETUP = "story_setup"


class AIOutputKind(str, Enum):
    PITCH_BATCH = "pitch_batch"
    CHARACTER_SHEET = "character_sheet"
    BEAT_SHEET = "beat_sheet"
    STORY_SETUP = "story_setup"
    COMPOSITION_SEGMENT = "composition_segment"
    AUDIO_SEGMENT = "audio_segment"


class UserEditTargetKind(str, Enum):
    STORY_BRIEF = "story_brief"
    PITCH = "pitch"
    CHARACTER_SHEET = "character_sheet"
    BEAT_SHEET = "beat_sheet"
    STORY_SETUP = "story_setup"
    COMPOSITION_SEGMENT = "composition_segment"
    AUDIO_SETTINGS = "audio_settings"


class ChatMessageRole(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"
    TOOL = "tool"


class EventActorType(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"
    SERVICE = "service"


class SessionEventActor(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    actor_type: EventActorType
    actor_id: str | None = None


class EventPayload(BaseModel):
    model_config = ConfigDict(extra="forbid")

    schema_version: int = Field(default=1, ge=1)


class SessionCreatedEventPayload(EventPayload):
    working_title: str | None = None


class WorkflowStageChangedEventPayload(EventPayload):
    previous_status: WorkflowStageState
    status: WorkflowStageState
    detail: str | None = None
    invalidated_stages: list[WorkflowStage] = Field(default_factory=list)
    current_stage: WorkflowStage
    resume_stage: WorkflowStage
    furthest_completed_stage: WorkflowStage | None = None
    overall_status: WorkflowStageState


class SelectionRecordedEventPayload(EventPayload):
    selection_kind: SelectionKind
    selection_id: str | None = None
    slug: str | None = None
    label: str | None = None
    previous_selection_id: str | None = None
    source: str = "unknown"
    accepted: bool = True


class AIOutputRecordedEventPayload(EventPayload):
    output_kind: AIOutputKind
    resource_id: str | None = None
    generation_key: str | None = None
    candidate_count: int | None = None
    model_id: str | None = None
    summary: str | None = None


class UserEditRecordedEventPayload(EventPayload):
    target_kind: UserEditTargetKind
    target_id: str | None = None
    revision_number: int | None = None
    changed_fields: list[str] = Field(default_factory=list)
    source: str = "unknown"
    field_values: dict[str, Any] | None = None
    summary_text: str | None = None


class ChatMessageRecordedEventPayload(EventPayload):
    message_role: ChatMessageRole
    message_id: str | None = None
    content_preview: str
    content_length: int
    source: str = "chat"


class ChatIntentParsedEventPayload(EventPayload):
    prompt_version: str
    model_id: str
    current_stage: WorkflowStage
    stage_label: str
    stage_description: str
    stage_status: WorkflowStageState
    stage_detail: str | None = None
    session_summary: str
    user_message: str
    rendered_prompt: str
    result: ParsedChatIntentResponse
    raw_response: dict[str, Any] | list[Any] | str | None = None


class UIActionRecordedEventPayload(EventPayload):
    action: str
    control_id: str | None = None
    value_summary: str | None = None
    origin: str = "workspace"


class CompositionProgressEventPayload(EventPayload):
    job_id: str
    status: str
    progress_percent: float | None = None
    current_segment_index: int | None = None
    total_segments: int | None = None
    segment_id: str | None = None


class AudioProgressEventPayload(EventPayload):
    job_id: str
    status: str
    progress_percent: float | None = None
    current_segment_index: int | None = None
    total_segments: int | None = None
    segment_id: str | None = None
    estimated_duration_seconds: int | None = None
    voice_key: str | None = None


SessionEventPayload: TypeAlias = (
    SessionCreatedEventPayload
    | WorkflowStageChangedEventPayload
    | SelectionRecordedEventPayload
    | AIOutputRecordedEventPayload
    | UserEditRecordedEventPayload
    | ChatMessageRecordedEventPayload
    | ChatIntentParsedEventPayload
    | UIActionRecordedEventPayload
    | CompositionProgressEventPayload
    | AudioProgressEventPayload
)

_EVENT_PAYLOAD_MODELS: dict[str, type[EventPayload]] = {
    SessionEventType.SESSION_CREATED.value: SessionCreatedEventPayload,
    SessionEventType.WORKFLOW_STAGE_CHANGED.value: WorkflowStageChangedEventPayload,
    SessionEventType.SELECTION_RECORDED.value: SelectionRecordedEventPayload,
    SessionEventType.AI_OUTPUT_RECORDED.value: AIOutputRecordedEventPayload,
    SessionEventType.USER_EDIT_RECORDED.value: UserEditRecordedEventPayload,
    SessionEventType.CHAT_MESSAGE_RECORDED.value: ChatMessageRecordedEventPayload,
    SessionEventType.CHAT_INTENT_PARSED.value: ChatIntentParsedEventPayload,
    SessionEventType.UI_ACTION_RECORDED.value: UIActionRecordedEventPayload,
    SessionEventType.COMPOSITION_PROGRESS_RECORDED.value: CompositionProgressEventPayload,
    SessionEventType.AUDIO_PROGRESS_RECORDED.value: AudioProgressEventPayload,
}


class SessionEventView(BaseModel):
    id: str
    session_id: str
    sequence_number: int
    actor: SessionEventActor
    event_type: str
    stage: WorkflowStage | None = None
    summary: str
    payload: SessionEventPayload | dict[str, Any] | list[Any] | None = None
    created_at: datetime


class SessionHistoryView(BaseModel):
    session_id: str
    latest_sequence_number: int | None = None
    events: list[SessionEventView] = Field(default_factory=list)


def serialize_event_payload(
    payload: EventPayload | Mapping[str, Any] | None,
) -> dict[str, Any]:
    if payload is None:
        return {"schema_version": 1}

    if isinstance(payload, EventPayload):
        return payload.model_dump(mode="json")

    normalized_payload = dict(payload)
    normalized_payload.setdefault("schema_version", 1)
    return normalized_payload


def parse_event_payload(
    event_type: str,
    payload: Mapping[str, Any] | list[Any] | None,
) -> SessionEventPayload | dict[str, Any] | list[Any] | None:
    if payload is None:
        return None

    if isinstance(payload, list):
        return payload

    normalized_payload = dict(payload)
    normalized_payload.setdefault("schema_version", 1)
    payload_model = _EVENT_PAYLOAD_MODELS.get(event_type)

    if payload_model is None:
        return normalized_payload

    return payload_model.model_validate(normalized_payload)
