from __future__ import annotations

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field

from app.models.workflow import WorkflowStage


class ModelUsageBucket(str, Enum):
    PLANNING = "planning"
    COMPOSITION = "composition"
    AUDIO = "audio"


class ModelCallOutcome(str, Enum):
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    SUCCEEDED_WITH_FALLBACK = "succeeded_with_fallback"


class ModelTokenUsageView(BaseModel):
    model_config = ConfigDict(extra="forbid")

    input_tokens: int | None = Field(default=None, ge=0)
    output_tokens: int | None = Field(default=None, ge=0)
    total_tokens: int | None = Field(default=None, ge=0)
    cached_input_tokens: int | None = Field(default=None, ge=0)
    thought_tokens: int | None = Field(default=None, ge=0)


class SessionUsageBucketSummaryView(BaseModel):
    model_config = ConfigDict(extra="forbid")

    usage_bucket: ModelUsageBucket
    total_calls: int = Field(default=0, ge=0)
    succeeded_calls: int = Field(default=0, ge=0)
    failed_calls: int = Field(default=0, ge=0)
    fallback_calls: int = Field(default=0, ge=0)
    token_metadata_call_count: int = Field(default=0, ge=0)
    cost_estimate_call_count: int = Field(default=0, ge=0)
    total_elapsed_ms: int = Field(default=0, ge=0)
    average_elapsed_ms: float | None = Field(default=None, ge=0)
    max_elapsed_ms: int | None = Field(default=None, ge=0)
    approximate_cost_usd: float | None = Field(default=None, ge=0)
    models_used: list[str] = Field(default_factory=list)
    token_usage: ModelTokenUsageView = Field(default_factory=ModelTokenUsageView)
    last_model_id: str | None = None
    last_purpose: str | None = None
    last_called_at: datetime | None = None


class SessionUsageSummaryView(BaseModel):
    model_config = ConfigDict(extra="forbid")

    total_calls: int = Field(default=0, ge=0)
    succeeded_calls: int = Field(default=0, ge=0)
    failed_calls: int = Field(default=0, ge=0)
    fallback_calls: int = Field(default=0, ge=0)
    token_metadata_call_count: int = Field(default=0, ge=0)
    cost_estimate_call_count: int = Field(default=0, ge=0)
    total_elapsed_ms: int = Field(default=0, ge=0)
    average_elapsed_ms: float | None = Field(default=None, ge=0)
    max_elapsed_ms: int | None = Field(default=None, ge=0)
    approximate_cost_usd: float | None = Field(default=None, ge=0)
    token_usage: ModelTokenUsageView = Field(default_factory=ModelTokenUsageView)
    buckets: list[SessionUsageBucketSummaryView] = Field(default_factory=list)


class SessionUsageStageBreakdownView(BaseModel):
    model_config = ConfigDict(extra="forbid")

    usage_bucket: ModelUsageBucket
    workflow_stage: WorkflowStage | None = None
    model_id: str
    total_calls: int = Field(default=0, ge=0)
    succeeded_calls: int = Field(default=0, ge=0)
    failed_calls: int = Field(default=0, ge=0)
    fallback_calls: int = Field(default=0, ge=0)
    token_metadata_call_count: int = Field(default=0, ge=0)
    cost_estimate_call_count: int = Field(default=0, ge=0)
    total_elapsed_ms: int = Field(default=0, ge=0)
    average_elapsed_ms: float | None = Field(default=None, ge=0)
    max_elapsed_ms: int | None = Field(default=None, ge=0)
    approximate_cost_usd: float | None = Field(default=None, ge=0)
    token_usage: ModelTokenUsageView = Field(default_factory=ModelTokenUsageView)


class SessionUsageEventView(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    usage_bucket: ModelUsageBucket
    workflow_stage: WorkflowStage | None = None
    purpose: str
    provider: str
    model_id: str
    prompt_version: str | None = None
    outcome: ModelCallOutcome
    elapsed_ms: int = Field(ge=0)
    approximate_cost_usd: float | None = Field(default=None, ge=0)
    token_usage: ModelTokenUsageView = Field(default_factory=ModelTokenUsageView)
    error_message: str | None = None
    created_at: datetime


class SessionUsageDiagnosticsView(BaseModel):
    model_config = ConfigDict(extra="forbid")

    session_id: str
    generated_at: datetime
    summary: SessionUsageSummaryView = Field(default_factory=SessionUsageSummaryView)
    stage_breakdown: list[SessionUsageStageBreakdownView] = Field(default_factory=list)
    recent_calls: list[SessionUsageEventView] = Field(default_factory=list)
    slowest_calls: list[SessionUsageEventView] = Field(default_factory=list)
    costliest_calls: list[SessionUsageEventView] = Field(default_factory=list)
