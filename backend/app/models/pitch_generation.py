from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.models.brief_normalization import NormalizedBriefPreferences

PITCH_GENERATION_SCHEMA_VERSION = 1
PITCH_GENERATION_PROMPT_VERSION = "pitch_generation.v1"


def normalize_optional_pitch_text(value: str | None) -> str | None:
    if value is None:
        return None

    normalized = value.strip()
    return normalized or None


class ExistingSelectedPitchContext(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str
    hook: str
    central_conflict: str | None = None
    why_it_fits: str | None = None

    @field_validator("*", mode="before")
    @classmethod
    def validate_text(cls, value: Any) -> str | None:
        if value is None:
            return None
        return normalize_optional_pitch_text(str(value))


class GeneratedPitchCandidate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str
    hook: str
    central_conflict: str
    why_it_fits: str

    @field_validator("title", "hook", "central_conflict", "why_it_fits", mode="before")
    @classmethod
    def validate_text(cls, value: Any) -> str:
        normalized = normalize_optional_pitch_text(str(value) if value is not None else None)
        if normalized is None:
            raise ValueError("pitch candidate fields must not be empty")
        return normalized


class PitchGenerationPromptContext(BaseModel):
    model_config = ConfigDict(extra="forbid")

    candidate_count: int = Field(default=3, ge=2, le=6)
    guidance: str | None = None
    genre_label: str | None = None
    genre_description: str | None = None
    genre_bedtime_safety_notes: str | None = None
    tone_label: str | None = None
    tone_description: str | None = None
    tone_bedtime_notes: str | None = None
    raw_brief: str
    normalized_summary: str | None = None
    story_idea: str | None = None
    desired_themes: str | None = None
    key_images: str | None = None
    audience_notes: str | None = None
    must_have_elements: str | None = None
    planning_notes: str | None = None
    normalized_preferences: NormalizedBriefPreferences = Field(
        default_factory=NormalizedBriefPreferences
    )
    selected_pitch: ExistingSelectedPitchContext | None = None

    @field_validator(
        "guidance",
        "genre_label",
        "genre_description",
        "genre_bedtime_safety_notes",
        "tone_label",
        "tone_description",
        "tone_bedtime_notes",
        "raw_brief",
        "normalized_summary",
        "story_idea",
        "desired_themes",
        "key_images",
        "audience_notes",
        "must_have_elements",
        "planning_notes",
        mode="before",
    )
    @classmethod
    def validate_text_fields(cls, value: Any) -> str | None:
        if value is None:
            return None
        return normalize_optional_pitch_text(str(value))


class PitchGenerationStructuredOutput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    schema_version: int = Field(default=PITCH_GENERATION_SCHEMA_VERSION, ge=1)
    pitches: list[GeneratedPitchCandidate] = Field(default_factory=list)


class PitchGenerationInvocation(BaseModel):
    model_config = ConfigDict(extra="forbid")

    prompt_version: str
    model_id: str
    context: PitchGenerationPromptContext
    rendered_prompt: str


class PitchGenerationInvocationResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    invocation: PitchGenerationInvocation
    structured_output: PitchGenerationStructuredOutput
    raw_response: dict[str, Any] | list[Any] | str | None = None


class PitchBatchEvaluationCriterion(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str
    passed: bool
    measured_value: str | int | float | None = None
    detail: str | None = None


class PitchBatchEvaluation(BaseModel):
    model_config = ConfigDict(extra="forbid")

    passed: bool
    criteria: list[PitchBatchEvaluationCriterion] = Field(default_factory=list)


class PitchGenerationResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    source: str
    model_id: str | None = None
    prompt_version: str | None = None
    pitches: list[GeneratedPitchCandidate] = Field(default_factory=list)
    evaluation: PitchBatchEvaluation
    raw_response: dict[str, Any] | list[Any] | str | None = None
