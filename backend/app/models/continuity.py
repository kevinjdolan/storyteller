from __future__ import annotations

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field

from app.models.workflow import WorkflowStage


class ContinuityFactCategory(str, Enum):
    CHARACTER = "character"
    LOCATION = "location"
    OBJECT = "object"
    PROMISE = "promise"
    VOICE_CONSTRAINT = "voice_constraint"
    UNRESOLVED_THREAD = "unresolved_thread"
    LOCKED_DETAIL = "locked_detail"


class ContinuityFact(BaseModel):
    key: str
    category: ContinuityFactCategory
    title: str
    detail: str
    source_stage: WorkflowStage | None = None
    source_label: str | None = None


class ContinuityBibleData(BaseModel):
    schema_version: int = Field(default=1, ge=1)
    facts: list[ContinuityFact] = Field(default_factory=list)


class ContinuityBibleView(BaseModel):
    id: str
    revision_number: int
    source_stage: WorkflowStage | None = None
    source_summary: str | None = None
    summary_text: str
    facts: list[ContinuityFact] = Field(default_factory=list)
    created_at: datetime
    updated_at: datetime
