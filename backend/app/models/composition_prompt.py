from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.models.beat_sheet_generation import GeneratedBeatSheetBeat
from app.models.bedtime_guidelines import (
    DEFAULT_BEDTIME_GUIDELINE_PRESET_KEY,
    normalize_bedtime_guideline_preset_key,
)
from app.models.brief_normalization import NormalizedBriefPreferences
from app.models.character_generation import ExistingCharacterSheetContext
from app.models.continuity import ContinuityFact
from app.models.pitch_generation import ExistingSelectedPitchContext

COMPOSITION_PROMPT_ASSEMBLY_SCHEMA_VERSION = 1
COMPOSITION_PROMPT_ASSEMBLY_VERSION = "composition_prompt_assembly.v1"
CompositionPromptJobKind = Literal["draft", "rewrite"]


def normalize_optional_composition_prompt_text(value: str | None) -> str | None:
    if value is None:
        return None

    normalized = value.strip()
    return normalized or None


def _normalize_string_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []

    normalized: list[str] = []
    for entry in value:
        text = normalize_optional_composition_prompt_text(str(entry) if entry is not None else None)
        if text is None:
            continue
        normalized.append(text)
    return normalized


class CompositionPromptAssemblyInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    session_id: str = Field(min_length=1)
    job_kind: CompositionPromptJobKind = "draft"
    segment_index: int = Field(ge=1)
    instructions: str | None = None
    restart_from_segment_index: int | None = Field(default=None, ge=1)
    rewrite_from_segment_index: int | None = Field(default=None, ge=1)
    bedtime_guideline_preset_key: str = DEFAULT_BEDTIME_GUIDELINE_PRESET_KEY

    @field_validator("session_id", "instructions", mode="before")
    @classmethod
    def validate_text_fields(cls, value: Any) -> str | None:
        if value is None:
            return None
        return normalize_optional_composition_prompt_text(str(value))

    @field_validator("bedtime_guideline_preset_key", mode="before")
    @classmethod
    def validate_bedtime_guideline_preset_key(cls, value: Any) -> str:
        text = None if value is None else str(value)
        return normalize_bedtime_guideline_preset_key(text)


class CompositionCatalogContext(BaseModel):
    model_config = ConfigDict(extra="forbid")

    label: str
    description: str | None = None
    bedtime_notes: str | None = None
    curation_notes: list[str] = Field(default_factory=list)

    @field_validator("label", "description", "bedtime_notes", mode="before")
    @classmethod
    def validate_text_fields(cls, value: Any) -> str | None:
        if value is None:
            return None
        return normalize_optional_composition_prompt_text(str(value))

    @field_validator("curation_notes", mode="before")
    @classmethod
    def validate_curation_notes(cls, value: Any) -> list[str]:
        return _normalize_string_list(value)


class CompositionBriefContext(BaseModel):
    model_config = ConfigDict(extra="forbid")

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

    @field_validator(
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
        return normalize_optional_composition_prompt_text(str(value))


class CompositionBeatSheetContext(BaseModel):
    model_config = ConfigDict(extra="forbid")

    revision_number: int = Field(ge=1)
    summary: str | None = None
    bedtime_notes: str | None = None
    bedtime_goal: str | None = None
    beats: list[GeneratedBeatSheetBeat] = Field(default_factory=list)

    @field_validator("summary", "bedtime_notes", "bedtime_goal", mode="before")
    @classmethod
    def validate_text_fields(cls, value: Any) -> str | None:
        if value is None:
            return None
        return normalize_optional_composition_prompt_text(str(value))


class CompositionSetupPreferencesContext(BaseModel):
    model_config = ConfigDict(extra="forbid")

    revision_number: int = Field(ge=1)
    target_word_count: int | None = Field(default=None, ge=1)
    target_runtime_minutes: int | None = Field(default=None, ge=1)
    chapter_count: int | None = Field(default=None, ge=1)
    approximate_scene_count: int | None = Field(default=None, ge=1)
    chapter_style: str | None = None
    guidance_notes: str | None = None
    preferences: dict[str, Any] | list[Any] | None = None

    @field_validator("chapter_style", "guidance_notes", mode="before")
    @classmethod
    def validate_text_fields(cls, value: Any) -> str | None:
        if value is None:
            return None
        return normalize_optional_composition_prompt_text(str(value))


class CompositionOutlineCardContext(BaseModel):
    model_config = ConfigDict(extra="forbid")

    story_outline_id: str = Field(min_length=1)
    story_outline_revision_number: int = Field(ge=1)
    outline_kind: str = Field(min_length=1)
    card_key: str = Field(min_length=1)
    position: int = Field(ge=1)
    title: str = Field(min_length=1)
    summary: str | None = None
    drafting_brief: str | None = None
    beat_keys: list[str] = Field(default_factory=list)
    beat_labels: list[str] = Field(default_factory=list)
    emotional_shift: str | None = None
    tone_direction: str | None = None
    bedtime_guardrail: str | None = None
    target_word_count: int | None = Field(default=None, ge=1)
    target_runtime_minutes: int | None = Field(default=None, ge=1)
    target_scene_count: int | None = Field(default=None, ge=1)

    @field_validator(
        "story_outline_id",
        "outline_kind",
        "card_key",
        "title",
        "summary",
        "drafting_brief",
        "emotional_shift",
        "tone_direction",
        "bedtime_guardrail",
        mode="before",
    )
    @classmethod
    def validate_text_fields(cls, value: Any) -> str | None:
        if value is None:
            return None
        return normalize_optional_composition_prompt_text(str(value))

    @field_validator("beat_keys", "beat_labels", mode="before")
    @classmethod
    def validate_string_lists(cls, value: Any) -> list[str]:
        return _normalize_string_list(value)


class CompositionContinuityContext(BaseModel):
    model_config = ConfigDict(extra="forbid")

    continuity_bible_id: str | None = None
    revision_number: int | None = Field(default=None, ge=1)
    summary_text: str | None = None
    facts: list[ContinuityFact] = Field(default_factory=list)

    @field_validator("continuity_bible_id", "summary_text", mode="before")
    @classmethod
    def validate_text_fields(cls, value: Any) -> str | None:
        if value is None:
            return None
        return normalize_optional_composition_prompt_text(str(value))


class CompositionPromptDynamicContext(BaseModel):
    model_config = ConfigDict(extra="forbid")

    session_id: str = Field(min_length=1)
    display_title: str = Field(min_length=1)
    bedtime_guideline_preset_key: str = DEFAULT_BEDTIME_GUIDELINE_PRESET_KEY
    job_kind: CompositionPromptJobKind = "draft"
    segment_index: int = Field(ge=1)
    request_instructions: str | None = None
    segment_goal_summary: str | None = None
    genre: CompositionCatalogContext
    tone: CompositionCatalogContext
    brief: CompositionBriefContext
    selected_pitch: ExistingSelectedPitchContext
    selected_character_sheet: ExistingCharacterSheetContext
    beat_sheet: CompositionBeatSheetContext
    story_setup: CompositionSetupPreferencesContext
    outline_card: CompositionOutlineCardContext | None = None
    continuity: CompositionContinuityContext = Field(default_factory=CompositionContinuityContext)

    @field_validator(
        "session_id",
        "display_title",
        "request_instructions",
        "segment_goal_summary",
        mode="before",
    )
    @classmethod
    def validate_text_fields(cls, value: Any) -> str | None:
        if value is None:
            return None
        return normalize_optional_composition_prompt_text(str(value))

    @field_validator("bedtime_guideline_preset_key", mode="before")
    @classmethod
    def validate_bedtime_guideline_preset_key(cls, value: Any) -> str:
        text = None if value is None else str(value)
        return normalize_bedtime_guideline_preset_key(text)


class CompositionSystemInstructions(BaseModel):
    model_config = ConfigDict(extra="forbid")

    prompt_version: str = COMPOSITION_PROMPT_ASSEMBLY_VERSION
    bedtime_guideline_preset_key: str = DEFAULT_BEDTIME_GUIDELINE_PRESET_KEY
    writer_role: str
    mission: str
    output_contract: list[str] = Field(default_factory=list)
    storytelling_guardrails: list[str] = Field(default_factory=list)
    bedtime_guidelines_fragment: str

    @field_validator("prompt_version", "writer_role", "mission", "bedtime_guidelines_fragment")
    @classmethod
    def validate_required_text_fields(cls, value: Any) -> str:
        normalized = normalize_optional_composition_prompt_text(
            str(value) if value is not None else None
        )
        if normalized is None:
            raise ValueError("system instruction text fields must not be empty")
        return normalized

    @field_validator("bedtime_guideline_preset_key", mode="before")
    @classmethod
    def validate_bedtime_guideline_preset_key(cls, value: Any) -> str:
        text = None if value is None else str(value)
        return normalize_bedtime_guideline_preset_key(text)

    @field_validator("output_contract", "storytelling_guardrails", mode="before")
    @classmethod
    def validate_string_lists(cls, value: Any) -> list[str]:
        return _normalize_string_list(value)


class CompositionPromptDebugContext(BaseModel):
    model_config = ConfigDict(extra="forbid")

    prompt_version: str = COMPOSITION_PROMPT_ASSEMBLY_VERSION
    session_id: str = Field(min_length=1)
    display_title: str = Field(min_length=1)
    job_kind: CompositionPromptJobKind = "draft"
    segment_index: int = Field(ge=1)
    outline_card_key: str | None = None
    outline_card_title: str | None = None
    story_outline_revision_number: int | None = Field(default=None, ge=1)
    beat_sheet_revision_number: int = Field(ge=1)
    story_setup_revision_number: int = Field(ge=1)
    continuity_revision_number: int | None = Field(default=None, ge=1)
    continuity_fact_count: int = Field(ge=0)
    selected_pitch_title: str
    selected_character_sheet_title: str | None = None
    requested_instruction_excerpt: str | None = None
    segment_goal_summary: str | None = None

    @field_validator(
        "prompt_version",
        "session_id",
        "display_title",
        "outline_card_key",
        "outline_card_title",
        "selected_pitch_title",
        "selected_character_sheet_title",
        "requested_instruction_excerpt",
        "segment_goal_summary",
        mode="before",
    )
    @classmethod
    def validate_text_fields(cls, value: Any) -> str | None:
        if value is None:
            return None
        return normalize_optional_composition_prompt_text(str(value))


class CompositionPromptPackage(BaseModel):
    model_config = ConfigDict(extra="forbid")

    schema_version: int = Field(default=COMPOSITION_PROMPT_ASSEMBLY_SCHEMA_VERSION, ge=1)
    assembly_version: str = COMPOSITION_PROMPT_ASSEMBLY_VERSION
    system_instructions: CompositionSystemInstructions
    dynamic_context: CompositionPromptDynamicContext
    debug_context: CompositionPromptDebugContext

    @field_validator("assembly_version", mode="before")
    @classmethod
    def validate_assembly_version(cls, value: Any) -> str:
        normalized = normalize_optional_composition_prompt_text(
            str(value) if value is not None else None
        )
        if normalized is None:
            raise ValueError("assembly_version must not be empty")
        return normalized

    def build_storage_payload(self) -> dict[str, Any]:
        outline = self.dynamic_context.outline_card
        continuity = self.dynamic_context.continuity
        payload: dict[str, Any] = {
            "prompt_assembly_version": self.assembly_version,
            "composition_prompt": self.model_dump(mode="json"),
            "continuity_bible_id": continuity.continuity_bible_id,
            "continuity_revision_number": continuity.revision_number,
            "continuity_summary": continuity.summary_text,
            "continuity_facts": [fact.model_dump(mode="json") for fact in continuity.facts],
        }
        if outline is not None:
            payload.update(
                {
                    "story_outline_id": outline.story_outline_id,
                    "story_outline_revision_number": outline.story_outline_revision_number,
                    "outline_kind": outline.outline_kind,
                    "outline_card_key": outline.card_key,
                    "outline_card_position": outline.position,
                    "outline_card_title": outline.title,
                    "outline_card_summary": outline.summary,
                    "outline_card_drafting_brief": outline.drafting_brief,
                    "outline_card_beat_keys": list(outline.beat_keys),
                    "outline_card_emotional_shift": outline.emotional_shift,
                }
            )
        return payload
