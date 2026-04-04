from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from app.models.bedtime_guidelines import (
    DEFAULT_BEDTIME_GUIDELINE_PRESET_KEY,
    normalize_bedtime_guideline_preset_key,
)
from app.models.brief_normalization import NormalizedBriefPreferences
from app.models.pitch_generation import ExistingSelectedPitchContext

CHARACTER_GENERATION_SCHEMA_VERSION = 1
CHARACTER_GENERATION_PROMPT_VERSION = "character_generation.v2"


def normalize_optional_character_text(value: str | None) -> str | None:
    if value is None:
        return None

    normalized = value.strip()
    return normalized or None


def _normalize_string_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []

    normalized: list[str] = []
    for entry in value:
        text = normalize_optional_character_text(str(entry) if entry is not None else None)
        if text is not None:
            normalized.append(text)
    return normalized


class GeneratedCharacterProfile(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str
    role: str
    goal: str
    flaw: str
    comfort_trait: str
    bedtime_safety_notes: str
    relationships: list[str] = Field(default_factory=list)
    visual_anchors: list[str] = Field(default_factory=list)

    @field_validator(
        "name",
        "role",
        "goal",
        "flaw",
        "comfort_trait",
        "bedtime_safety_notes",
        mode="before",
    )
    @classmethod
    def validate_text(cls, value: Any) -> str:
        normalized = normalize_optional_character_text(str(value) if value is not None else None)
        if normalized is None:
            raise ValueError("character profile fields must not be empty")
        return normalized

    @field_validator("relationships", "visual_anchors", mode="before")
    @classmethod
    def validate_string_lists(cls, value: Any) -> list[str]:
        return _normalize_string_list(value)


class ExistingCharacterSheetContext(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str | None = None
    summary: str | None = None
    protagonist_name: str | None = None
    bedtime_safety_notes: str | None = None
    protagonist: GeneratedCharacterProfile | None = None
    supporting_cast: list[GeneratedCharacterProfile] = Field(default_factory=list)

    @field_validator(
        "title",
        "summary",
        "protagonist_name",
        "bedtime_safety_notes",
        mode="before",
    )
    @classmethod
    def validate_text(cls, value: Any) -> str | None:
        if value is None:
            return None
        return normalize_optional_character_text(str(value))


class GeneratedCharacterSheetCandidate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str
    summary: str
    story_function: str
    bedtime_safety_notes: str
    visual_motifs: list[str] = Field(default_factory=list)
    protagonist: GeneratedCharacterProfile
    supporting_cast: list[GeneratedCharacterProfile] = Field(default_factory=list)

    @field_validator(
        "title",
        "summary",
        "story_function",
        "bedtime_safety_notes",
        mode="before",
    )
    @classmethod
    def validate_text(cls, value: Any) -> str:
        normalized = normalize_optional_character_text(str(value) if value is not None else None)
        if normalized is None:
            raise ValueError("character sheet candidate fields must not be empty")
        return normalized

    @field_validator("visual_motifs", mode="before")
    @classmethod
    def validate_visual_motifs(cls, value: Any) -> list[str]:
        return _normalize_string_list(value)


class CharacterGenerationPromptContext(BaseModel):
    model_config = ConfigDict(extra="forbid")

    candidate_count: int = Field(default=3, ge=1, le=5)
    generation_goal: Literal["alternatives", "refinement"] = "alternatives"
    bedtime_guideline_preset_key: str = DEFAULT_BEDTIME_GUIDELINE_PRESET_KEY
    guidance: str | None = None
    change_summary: str | None = None
    focus_character_names: list[str] = Field(default_factory=list)
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
    selected_pitch: ExistingSelectedPitchContext
    existing_character_sheet: ExistingCharacterSheetContext | None = None

    @field_validator(
        "guidance",
        "change_summary",
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
        return normalize_optional_character_text(str(value))

    @field_validator("bedtime_guideline_preset_key", mode="before")
    @classmethod
    def validate_bedtime_guideline_preset_key(cls, value: Any) -> str:
        text = None if value is None else str(value)
        return normalize_bedtime_guideline_preset_key(text)

    @field_validator("focus_character_names", mode="before")
    @classmethod
    def validate_focus_character_names(cls, value: Any) -> list[str]:
        return _normalize_string_list(value)

    @model_validator(mode="after")
    def validate_candidate_count(self) -> CharacterGenerationPromptContext:
        if self.generation_goal == "refinement" and self.candidate_count < 1:
            raise ValueError("character-sheet refinements require at least one candidate")
        if self.generation_goal != "refinement" and self.candidate_count < 2:
            raise ValueError("character-sheet batches require at least two candidates")
        return self


class CharacterGenerationStructuredOutput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    schema_version: int = Field(default=CHARACTER_GENERATION_SCHEMA_VERSION, ge=1)
    character_sheets: list[GeneratedCharacterSheetCandidate] = Field(default_factory=list)


class CharacterGenerationInvocation(BaseModel):
    model_config = ConfigDict(extra="forbid")

    prompt_version: str
    model_id: str
    context: CharacterGenerationPromptContext
    rendered_prompt: str


class CharacterGenerationInvocationResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    invocation: CharacterGenerationInvocation
    structured_output: CharacterGenerationStructuredOutput
    raw_response: dict[str, Any] | list[Any] | str | None = None


class CharacterBatchEvaluationCriterion(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str
    passed: bool
    measured_value: str | int | float | None = None
    detail: str | None = None


class CharacterBatchEvaluation(BaseModel):
    model_config = ConfigDict(extra="forbid")

    passed: bool
    criteria: list[CharacterBatchEvaluationCriterion] = Field(default_factory=list)


class CharacterGenerationResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    source: str
    model_id: str | None = None
    prompt_version: str | None = None
    character_sheets: list[GeneratedCharacterSheetCandidate] = Field(default_factory=list)
    evaluation: CharacterBatchEvaluation
    raw_response: dict[str, Any] | list[Any] | str | None = None
