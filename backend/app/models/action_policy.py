from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, ConfigDict, Field

from app.models.chat_actions import ChatToUIAction, ChatToUIActionBatch, ChatToUIActionType
from app.models.workflow import WorkflowStage

SESSION_ACTION_POLICY_SCHEMA_VERSION = 1


class SessionActionDecision(str, Enum):
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    REQUIRES_CONFIRMATION = "requires_confirmation"
    ACCEPTED_WITH_SIDE_EFFECTS = "accepted_with_side_effects"


class SessionActionReasonCode(str, Enum):
    CONFIRMATION_REQUIRED_BY_DEFAULT = "confirmation_required_by_default"
    CONFIRMATION_REQUIRED_DUE_TO_SIDE_EFFECTS = (
        "confirmation_required_due_to_side_effects"
    )
    PREREQUISITE_STAGE_INCOMPLETE = "prerequisite_stage_incomplete"
    PREREQUISITE_SELECTION_MISSING = "prerequisite_selection_missing"
    TARGET_STAGE_STALE = "target_stage_stale"
    CATALOG_ENTRY_NOT_FOUND = "catalog_entry_not_found"
    CATALOG_ENTRY_AMBIGUOUS = "catalog_entry_ambiguous"
    CATALOG_ENTRY_MISMATCH = "catalog_entry_mismatch"
    SESSION_RESOURCE_NOT_FOUND = "session_resource_not_found"
    SESSION_RESOURCE_AMBIGUOUS = "session_resource_ambiguous"
    JOB_NOT_ACTIVE = "job_not_active"
    JOB_STATE_CONFLICT = "job_state_conflict"
    ASSET_NOT_READY = "asset_not_ready"
    ASSET_REGENERATION_REQUIRED = "asset_regeneration_required"
    ACTION_IS_NOOP = "action_is_noop"


class SessionActionSideEffectKind(str, Enum):
    INVALIDATE_STAGES = "invalidate_stages"
    STOP_ACTIVE_JOB = "stop_active_job"
    SUPERSEDE_ASSET = "supersede_asset"
    CLEAR_SELECTION = "clear_selection"


class SessionActionPolicyReason(BaseModel):
    model_config = ConfigDict(extra="forbid")

    code: SessionActionReasonCode
    message: str = Field(min_length=1)
    stage: WorkflowStage | None = None
    related_stages: list[WorkflowStage] = Field(default_factory=list)
    related_action_types: list[ChatToUIActionType] = Field(default_factory=list)


class SessionActionPolicySideEffect(BaseModel):
    model_config = ConfigDict(extra="forbid")

    kind: SessionActionSideEffectKind
    message: str = Field(min_length=1)
    stages: list[WorkflowStage] = Field(default_factory=list)
    selection_field: str | None = Field(default=None, min_length=1)
    job_kind: str | None = Field(default=None, min_length=1)
    asset_kind: str | None = Field(default=None, min_length=1)


class SessionActionPolicyRequestItem(BaseModel):
    model_config = ConfigDict(extra="forbid")

    action: ChatToUIAction
    confirmation_granted: bool = False


class SessionActionPolicyEvaluationRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    schema_version: int = Field(default=SESSION_ACTION_POLICY_SCHEMA_VERSION, ge=1)
    actions: list[SessionActionPolicyRequestItem] = Field(default_factory=list)


class SessionActionPolicyEvaluationItem(BaseModel):
    model_config = ConfigDict(extra="forbid")

    action_index: int = Field(ge=0)
    action_type: ChatToUIActionType
    target_stage: WorkflowStage
    decision: SessionActionDecision
    summary: str = Field(min_length=1)
    reasons: list[SessionActionPolicyReason] = Field(default_factory=list)
    side_effects: list[SessionActionPolicySideEffect] = Field(default_factory=list)
    prerequisite_action_types: list[ChatToUIActionType] = Field(default_factory=list)


class SessionActionPolicyEvaluation(BaseModel):
    model_config = ConfigDict(extra="forbid")

    schema_version: int = Field(default=SESSION_ACTION_POLICY_SCHEMA_VERSION, ge=1)
    session_id: str
    evaluated_actions: list[SessionActionPolicyEvaluationItem] = Field(default_factory=list)


def build_action_policy_request_from_batch(
    batch: ChatToUIActionBatch,
    *,
    confirmation_granted: bool = False,
) -> SessionActionPolicyEvaluationRequest:
    return SessionActionPolicyEvaluationRequest(
        actions=[
            SessionActionPolicyRequestItem(
                action=action,
                confirmation_granted=confirmation_granted,
            )
            for action in batch.actions
        ]
    )
