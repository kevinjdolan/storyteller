from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.models.composition_prompt import CompositionPromptPackage

COMPOSITION_SEGMENT_GENERATION_SCHEMA_VERSION = 1
COMPOSITION_SEGMENT_GENERATION_PROMPT_VERSION = "composition_segment_generation.v1"
SEGMENT_CONTEXT_CARRYOVER_VERSION = "segmented_context_carryover.v1"


def normalize_optional_composition_generation_text(value: str | None) -> str | None:
    if value is None:
        return None

    normalized = value.strip()
    return normalized or None


class CompositionSegmentCarryoverItem(BaseModel):
    model_config = ConfigDict(extra="forbid")

    segment_index: int = Field(ge=1)
    outline_card_title: str | None = None
    accepted_summary: str
    accepted_word_count: int | None = Field(default=None, ge=1)

    @field_validator("outline_card_title", "accepted_summary", mode="before")
    @classmethod
    def validate_text_fields(cls, value: Any) -> str | None:
        if value is None:
            return None
        return normalize_optional_composition_generation_text(str(value))


class CompositionSegmentCarryoverContext(BaseModel):
    model_config = ConfigDict(extra="forbid")

    strategy_version: str = SEGMENT_CONTEXT_CARRYOVER_VERSION
    segment_unit: str = "outline_card"
    prior_segment_count: int = Field(ge=0)
    story_so_far_summary: str | None = None
    latest_accepted_summary: str | None = None
    prior_segments: list[CompositionSegmentCarryoverItem] = Field(default_factory=list)

    @field_validator(
        "strategy_version",
        "segment_unit",
        "story_so_far_summary",
        "latest_accepted_summary",
        mode="before",
    )
    @classmethod
    def validate_text_fields(cls, value: Any) -> str | None:
        if value is None:
            return None
        return normalize_optional_composition_generation_text(str(value))


class CompositionSegmentGenerationPromptContext(BaseModel):
    model_config = ConfigDict(extra="forbid")

    composition_prompt: CompositionPromptPackage
    carryover: CompositionSegmentCarryoverContext


class CompositionSegmentGenerationStructuredOutput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    schema_version: int = Field(default=COMPOSITION_SEGMENT_GENERATION_SCHEMA_VERSION, ge=1)
    raw_text: str
    accepted_text: str
    carryover_summary: str

    @field_validator("raw_text", "accepted_text", "carryover_summary", mode="before")
    @classmethod
    def validate_required_text_fields(cls, value: Any) -> str:
        normalized = normalize_optional_composition_generation_text(
            str(value) if value is not None else None
        )
        if normalized is None:
            raise ValueError("composition segment output text fields must not be empty")
        return normalized


class CompositionSegmentGenerationInvocation(BaseModel):
    model_config = ConfigDict(extra="forbid")

    prompt_version: str
    model_id: str
    context: CompositionSegmentGenerationPromptContext
    rendered_prompt: str


class CompositionSegmentGenerationInvocationResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    invocation: CompositionSegmentGenerationInvocation
    structured_output: CompositionSegmentGenerationStructuredOutput
    raw_response: dict[str, Any] | list[Any] | str | None = None
