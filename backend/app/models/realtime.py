from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Annotated, Any, Literal, TypeAlias

from pydantic import BaseModel, ConfigDict, Field, TypeAdapter, model_validator

from app.models.events import ChatMessageRole, SessionEventActor, WorkflowStageChangedEventPayload
from app.models.workflow import WorkflowStage

SESSION_CHANNEL_PREFIX = "session:"


def build_session_channel_name(session_id: str) -> str:
    normalized_session_id = session_id.strip()
    if not normalized_session_id:
        raise ValueError("session_id must not be empty")

    return f"{SESSION_CHANNEL_PREFIX}{normalized_session_id}"


class RealtimeEventType(str, Enum):
    CHAT_MESSAGE = "chat.message"
    WORKFLOW_STAGE_CHANGED = "workflow.stage_changed"
    UI_ACTION_ECHO = "ui.action_echo"
    COMPOSITION_CHUNK = "composition.chunk"
    JOB_PROGRESS = "job.progress"
    JOB_STATUS = "job.status"
    ERROR_NOTIFICATION = "error.notification"


class RealtimeDeliveryMode(str, Enum):
    LIVE = "live"
    REPLAY = "replay"


class RealtimeReplayStrategy(str, Enum):
    NONE = "none"
    DELTA = "delta"
    HYDRATE = "hydrate"


class ChatContentFormat(str, Enum):
    PLAIN_TEXT = "plain_text"
    MARKDOWN = "markdown"


class UIActionEchoResult(str, Enum):
    ACCEPTED = "accepted"
    REJECTED = "rejected"


class CompositionChunkKind(str, Enum):
    SEGMENT_START = "segment_start"
    DELTA = "delta"
    SEGMENT_SUMMARY = "segment_summary"


class JobKind(str, Enum):
    COMPOSITION = "composition"
    AUDIO = "audio"


class RealtimeJobStatus(str, Enum):
    QUEUED = "queued"
    IN_PROGRESS = "in_progress"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class ErrorSeverity(str, Enum):
    WARNING = "warning"
    ERROR = "error"


class RealtimeContractModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    schema_version: int = Field(default=1, ge=1)


class SessionSubscriptionRequest(RealtimeContractModel):
    action: Literal["subscribe"] = "subscribe"
    session_id: str = Field(min_length=1)
    tab_id: str = Field(min_length=1)
    last_sequence_number: int | None = Field(default=None, ge=0)
    request_id: str | None = None


class SessionScopedChannelModel(RealtimeContractModel):
    session_id: str = Field(min_length=1)
    channel: str = Field(min_length=1)

    @model_validator(mode="after")
    def validate_channel(self) -> SessionScopedChannelModel:
        expected_channel = build_session_channel_name(self.session_id)
        if self.channel != expected_channel:
            raise ValueError(f"channel must match the session-scoped name {expected_channel!r}")

        return self


class SessionSubscriptionAck(SessionScopedChannelModel):
    action: Literal["subscribed"] = "subscribed"
    connection_id: str = Field(min_length=1)
    tab_id: str = Field(min_length=1)
    accepted_at: datetime
    replay_strategy: RealtimeReplayStrategy = RealtimeReplayStrategy.NONE
    replay_from_sequence_number: int | None = Field(default=None, ge=1)
    latest_sequence_number: int | None = Field(default=None, ge=0)
    request_id: str | None = None
    local_actor: SessionEventActor


class ChatMessageEventPayload(RealtimeContractModel):
    message_id: str = Field(min_length=1)
    message_role: ChatMessageRole
    content: str = Field(min_length=1)
    content_format: ChatContentFormat = ChatContentFormat.PLAIN_TEXT
    source: str = "chat"


class UIActionEchoEventPayload(RealtimeContractModel):
    action: str = Field(min_length=1)
    result: UIActionEchoResult = UIActionEchoResult.ACCEPTED
    summary: str = Field(min_length=1)
    control_id: str | None = None
    value_summary: str | None = None
    origin: str = "workspace"
    detail: str | None = None
    chat_message_id: str | None = None


class CompositionChunkEventPayload(RealtimeContractModel):
    job_id: str = Field(min_length=1)
    segment_id: str = Field(min_length=1)
    segment_index: int = Field(ge=1)
    chunk_index: int = Field(ge=0)
    chunk_kind: CompositionChunkKind = CompositionChunkKind.DELTA
    text: str | None = None
    summary: str | None = None
    cumulative_character_count: int | None = Field(default=None, ge=0)
    cumulative_word_count: int | None = Field(default=None, ge=0)
    is_final_chunk: bool = False

    @model_validator(mode="after")
    def validate_chunk_body(self) -> CompositionChunkEventPayload:
        if self.chunk_kind == CompositionChunkKind.DELTA and not self.text:
            raise ValueError("delta chunks must include text")

        if self.chunk_kind == CompositionChunkKind.SEGMENT_SUMMARY and not self.summary:
            raise ValueError("segment_summary chunks must include summary")

        return self


class JobProgressEventPayload(RealtimeContractModel):
    job_id: str = Field(min_length=1)
    job_kind: JobKind
    status: RealtimeJobStatus
    progress_percent: float | None = Field(default=None, ge=0, le=100)
    current_step: str | None = None
    current_step_index: int | None = Field(default=None, ge=1)
    total_steps: int | None = Field(default=None, ge=1)
    completed_segments: int | None = Field(default=None, ge=0)
    current_segment_index: int | None = Field(default=None, ge=1)
    total_segments: int | None = Field(default=None, ge=1)
    segment_id: str | None = None
    segment_status: str | None = None
    eta_seconds: int | None = Field(default=None, ge=0)
    estimated_duration_seconds: int | None = Field(default=None, ge=0)
    latest_asset_id: str | None = None
    latest_asset_kind: str | None = None
    message: str | None = None


class JobStatusEventPayload(RealtimeContractModel):
    job_id: str = Field(min_length=1)
    job_kind: JobKind
    previous_status: RealtimeJobStatus | None = None
    status: RealtimeJobStatus
    message: str | None = None
    stop_reason: str | None = None
    error_message: str | None = None
    current_segment_index: int | None = Field(default=None, ge=1)
    total_segments: int | None = Field(default=None, ge=1)
    latest_asset_id: str | None = None
    latest_asset_kind: str | None = None


class ErrorNotificationEventPayload(RealtimeContractModel):
    code: str = Field(min_length=1)
    severity: ErrorSeverity = ErrorSeverity.ERROR
    message: str = Field(min_length=1)
    retryable: bool = False
    detail: str | None = None
    job_id: str | None = None
    job_kind: JobKind | None = None


class SessionRealtimeEventBase(SessionScopedChannelModel):
    event_id: str = Field(min_length=1)
    type: str
    actor: SessionEventActor
    stage: WorkflowStage | None = None
    created_at: datetime
    correlation_id: str | None = None


class DurableSessionRealtimeEventBase(SessionRealtimeEventBase):
    replayable: Literal[True] = True
    delivery: RealtimeDeliveryMode = RealtimeDeliveryMode.LIVE
    sequence_number: int = Field(ge=1)
    event_log_entry_id: str = Field(min_length=1)


class EphemeralSessionRealtimeEventBase(SessionRealtimeEventBase):
    replayable: Literal[False] = False
    delivery: Literal[RealtimeDeliveryMode.LIVE] = RealtimeDeliveryMode.LIVE
    sequence_number: None = None
    event_log_entry_id: None = None


class ChatMessageRealtimeEvent(DurableSessionRealtimeEventBase):
    type: Literal[RealtimeEventType.CHAT_MESSAGE] = RealtimeEventType.CHAT_MESSAGE
    payload: ChatMessageEventPayload


class WorkflowStageChangedRealtimeEvent(DurableSessionRealtimeEventBase):
    type: Literal[RealtimeEventType.WORKFLOW_STAGE_CHANGED] = (
        RealtimeEventType.WORKFLOW_STAGE_CHANGED
    )
    payload: WorkflowStageChangedEventPayload


class UIActionEchoRealtimeEvent(DurableSessionRealtimeEventBase):
    type: Literal[RealtimeEventType.UI_ACTION_ECHO] = RealtimeEventType.UI_ACTION_ECHO
    payload: UIActionEchoEventPayload


class CompositionChunkRealtimeEvent(EphemeralSessionRealtimeEventBase):
    type: Literal[RealtimeEventType.COMPOSITION_CHUNK] = RealtimeEventType.COMPOSITION_CHUNK
    stage: Literal[WorkflowStage.COMPOSITION] = WorkflowStage.COMPOSITION
    payload: CompositionChunkEventPayload


class JobProgressRealtimeEvent(DurableSessionRealtimeEventBase):
    type: Literal[RealtimeEventType.JOB_PROGRESS] = RealtimeEventType.JOB_PROGRESS
    payload: JobProgressEventPayload


class JobStatusRealtimeEvent(DurableSessionRealtimeEventBase):
    type: Literal[RealtimeEventType.JOB_STATUS] = RealtimeEventType.JOB_STATUS
    payload: JobStatusEventPayload


class ErrorNotificationRealtimeEvent(DurableSessionRealtimeEventBase):
    type: Literal[RealtimeEventType.ERROR_NOTIFICATION] = RealtimeEventType.ERROR_NOTIFICATION
    payload: ErrorNotificationEventPayload


SessionRealtimeEvent: TypeAlias = Annotated[
    ChatMessageRealtimeEvent
    | WorkflowStageChangedRealtimeEvent
    | UIActionEchoRealtimeEvent
    | CompositionChunkRealtimeEvent
    | JobProgressRealtimeEvent
    | JobStatusRealtimeEvent
    | ErrorNotificationRealtimeEvent,
    Field(discriminator="type"),
]


def get_realtime_contract_schema_bundle() -> dict[str, Any]:
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "title": "Storyteller Realtime Contracts",
        "bundle_schema_version": 1,
        "schemas": {
            "session_subscription_request": SessionSubscriptionRequest.model_json_schema(),
            "session_subscription_ack": SessionSubscriptionAck.model_json_schema(),
            "session_event": TypeAdapter(SessionRealtimeEvent).json_schema(),
        },
    }
