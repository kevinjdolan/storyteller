from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.models.brief_normalization import NormalizedBriefPreferences
from app.models.character_generation import ExistingCharacterSheetContext
from app.models.pitch_generation import ExistingSelectedPitchContext

BEAT_SHEET_GENERATION_SCHEMA_VERSION = 1
BEAT_SHEET_GENERATION_PROMPT_VERSION = "beat_sheet_generation.v1"
SAVE_THE_CAT_BEAT_SEQUENCE: tuple[tuple[str, str], ...] = (
    ("opening_image", "Opening Image"),
    ("theme_stated", "Theme Stated"),
    ("set_up", "Set-Up"),
    ("catalyst", "Catalyst"),
    ("debate", "Debate"),
    ("break_into_two", "Break into Two"),
    ("b_story", "B Story"),
    ("fun_and_games", "Fun and Games"),
    ("midpoint", "Midpoint"),
    ("bad_guys_close_in", "Bad Guys Close In"),
    ("all_is_lost", "All Is Lost"),
    ("dark_night_of_the_soul", "Dark Night of the Soul"),
    ("break_into_three", "Break into Three"),
    ("finale", "Finale"),
    ("final_image", "Final Image"),
)
SAVE_THE_CAT_BEAT_KEYS: tuple[str, ...] = tuple(
    beat_key for beat_key, _ in SAVE_THE_CAT_BEAT_SEQUENCE
)
SAVE_THE_CAT_BEAT_LABELS: dict[str, str] = dict(SAVE_THE_CAT_BEAT_SEQUENCE)


def normalize_optional_beat_text(value: str | None) -> str | None:
    if value is None:
        return None

    normalized = value.strip()
    return normalized or None


def _normalize_string_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []

    normalized: list[str] = []
    for entry in value:
        text = normalize_optional_beat_text(str(entry) if entry is not None else None)
        if text is not None:
            normalized.append(text)
    return normalized


class GeneratedBeatSheetBeat(BaseModel):
    model_config = ConfigDict(extra="forbid")

    key: str
    label: str
    summary: str
    emotional_intent: str
    bedtime_softening_note: str

    @field_validator(
        "key",
        "label",
        "summary",
        "emotional_intent",
        "bedtime_softening_note",
        mode="before",
    )
    @classmethod
    def validate_text(cls, value: Any) -> str:
        normalized = normalize_optional_beat_text(str(value) if value is not None else None)
        if normalized is None:
            raise ValueError("beat fields must not be empty")
        return normalized


class ExistingBeatSheetContext(BaseModel):
    model_config = ConfigDict(extra="forbid")

    revision_number: int
    summary: str | None = None
    bedtime_notes: str | None = None
    beats: list[GeneratedBeatSheetBeat] = Field(default_factory=list)

    @field_validator("summary", "bedtime_notes", mode="before")
    @classmethod
    def validate_text(cls, value: Any) -> str | None:
        if value is None:
            return None
        return normalize_optional_beat_text(str(value))


class GeneratedBeatSheetCandidate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    summary: str
    bedtime_notes: str
    beats: list[GeneratedBeatSheetBeat] = Field(default_factory=list)

    @field_validator("summary", "bedtime_notes", mode="before")
    @classmethod
    def validate_text(cls, value: Any) -> str:
        normalized = normalize_optional_beat_text(str(value) if value is not None else None)
        if normalized is None:
            raise ValueError("beat-sheet candidate fields must not be empty")
        return normalized


class BeatSheetGenerationPromptContext(BaseModel):
    model_config = ConfigDict(extra="forbid")

    generation_goal: Literal["initial", "refinement"] = "initial"
    guidance: str | None = None
    instructions: str | None = None
    focus_beats: list[str] = Field(default_factory=list)
    bedtime_goal: str | None = None
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
    selected_character_sheet: ExistingCharacterSheetContext
    existing_beat_sheet: ExistingBeatSheetContext | None = None

    @field_validator(
        "guidance",
        "instructions",
        "bedtime_goal",
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
        return normalize_optional_beat_text(str(value))

    @field_validator("focus_beats", mode="before")
    @classmethod
    def validate_focus_beats(cls, value: Any) -> list[str]:
        return _normalize_string_list(value)


class BeatSheetGenerationStructuredOutput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    schema_version: int = Field(default=BEAT_SHEET_GENERATION_SCHEMA_VERSION, ge=1)
    beat_sheet: GeneratedBeatSheetCandidate


class BeatSheetGenerationInvocation(BaseModel):
    model_config = ConfigDict(extra="forbid")

    prompt_version: str
    model_id: str
    context: BeatSheetGenerationPromptContext
    rendered_prompt: str


class BeatSheetGenerationInvocationResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    invocation: BeatSheetGenerationInvocation
    structured_output: BeatSheetGenerationStructuredOutput
    raw_response: dict[str, Any] | list[Any] | str | None = None


class BeatSheetEvaluationCriterion(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str
    passed: bool
    measured_value: str | int | float | None = None
    detail: str | None = None


class BeatSheetEvaluation(BaseModel):
    model_config = ConfigDict(extra="forbid")

    passed: bool
    criteria: list[BeatSheetEvaluationCriterion] = Field(default_factory=list)


class BeatSheetGenerationResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    source: str
    model_id: str | None = None
    prompt_version: str | None = None
    beat_sheet: GeneratedBeatSheetCandidate
    evaluation: BeatSheetEvaluation
    raw_response: dict[str, Any] | list[Any] | str | None = None
