from __future__ import annotations

import re
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator

BRIEF_NORMALIZATION_SCHEMA_VERSION = 1
BRIEF_NORMALIZATION_PROMPT_VERSION = "brief_normalizer.v1"


def normalize_optional_brief_text(value: str | None) -> str | None:
    if value is None:
        return None

    normalized = value.strip()
    return normalized or None


def _normalize_string_list(value: Any) -> list[str]:
    if value is None:
        return []

    if isinstance(value, str):
        candidates = re.split(r"[\n,;]+", value)
    elif isinstance(value, (list, tuple, set)):
        candidates = [str(item) for item in value]
    else:
        raise ValueError("expected a list of strings")

    normalized: list[str] = []
    for candidate in candidates:
        item = normalize_optional_brief_text(candidate)
        if item is None or item in normalized:
            continue
        normalized.append(item)

    return normalized


class NormalizedBriefPreferences(BaseModel):
    model_config = ConfigDict(extra="forbid")

    protagonist_type: str | None = None
    setting: str | None = None
    emotional_goal: str | None = None
    constraint_notes: list[str] = Field(default_factory=list)
    bedtime_safety_concerns: list[str] = Field(default_factory=list)
    candidate_motifs: list[str] = Field(default_factory=list)

    @field_validator("protagonist_type", "setting", "emotional_goal", mode="before")
    @classmethod
    def validate_optional_text(cls, value: Any) -> str | None:
        if value is None:
            return None
        return normalize_optional_brief_text(str(value))

    @field_validator(
        "constraint_notes",
        "bedtime_safety_concerns",
        "candidate_motifs",
        mode="before",
    )
    @classmethod
    def validate_string_list(cls, value: Any) -> list[str]:
        return _normalize_string_list(value)

    def has_content(self) -> bool:
        return any(
            (
                self.protagonist_type,
                self.setting,
                self.emotional_goal,
                self.constraint_notes,
                self.bedtime_safety_concerns,
                self.candidate_motifs,
            )
        )


class BriefNormalizationPromptContext(BaseModel):
    model_config = ConfigDict(extra="forbid")

    raw_brief: str
    genre_label: str | None = None
    tone_label: str | None = None
    story_idea: str | None = None
    desired_themes: str | None = None
    key_images: str | None = None
    audience_notes: str | None = None
    must_have_elements: str | None = None

    @field_validator(
        "raw_brief",
        "genre_label",
        "tone_label",
        "story_idea",
        "desired_themes",
        "key_images",
        "audience_notes",
        "must_have_elements",
        mode="before",
    )
    @classmethod
    def validate_context_text(cls, value: Any) -> str | None:
        if value is None:
            return None
        return normalize_optional_brief_text(str(value))


class BriefNormalizationStructuredOutput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    schema_version: int = Field(default=BRIEF_NORMALIZATION_SCHEMA_VERSION, ge=1)
    normalized_summary: str | None = None
    normalized_preferences: NormalizedBriefPreferences = Field(
        default_factory=NormalizedBriefPreferences
    )

    @field_validator("normalized_summary", mode="before")
    @classmethod
    def validate_summary(cls, value: Any) -> str | None:
        if value is None:
            return None
        return normalize_optional_brief_text(str(value))


class BriefNormalizationInvocation(BaseModel):
    model_config = ConfigDict(extra="forbid")

    prompt_version: str
    model_id: str
    context: BriefNormalizationPromptContext
    rendered_prompt: str


class BriefNormalizationInvocationResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    invocation: BriefNormalizationInvocation
    structured_output: BriefNormalizationStructuredOutput
    raw_response: dict[str, Any] | list[Any] | str | None = None


class BriefNormalizationResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    source: str
    model_id: str | None = None
    prompt_version: str | None = None
    normalized_summary: str | None = None
    normalized_preferences: NormalizedBriefPreferences = Field(
        default_factory=NormalizedBriefPreferences
    )
    raw_response: dict[str, Any] | list[Any] | str | None = None

    @field_validator("normalized_summary", mode="before")
    @classmethod
    def validate_result_summary(cls, value: Any) -> str | None:
        if value is None:
            return None
        return normalize_optional_brief_text(str(value))
