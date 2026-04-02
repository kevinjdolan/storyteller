from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

BedtimePromptStage = Literal["pitch", "character", "beat", "composition", "audio"]
BedtimeAudiencePresetStatus = Literal["active", "planned"]

DEFAULT_BEDTIME_GUIDELINE_PRESET_KEY = "shared_bedtime_default"
BEDTIME_PROMPT_STAGES: tuple[BedtimePromptStage, ...] = (
    "pitch",
    "character",
    "beat",
    "composition",
    "audio",
)


class BedtimeAudiencePresetPlan(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    key: str
    label: str
    status: BedtimeAudiencePresetStatus
    age_band: str
    summary: str
    prompt_adjustments: list[str] = Field(default_factory=list)


BEDTIME_AUDIENCE_PRESET_PLAN: tuple[BedtimeAudiencePresetPlan, ...] = (
    BedtimeAudiencePresetPlan(
        key=DEFAULT_BEDTIME_GUIDELINE_PRESET_KEY,
        label="Shared Bedtime Default",
        status="active",
        age_band="Broad bedtime audience",
        summary=(
            "The current production preset keeps tension gentle enough for a wide bedtime "
            "read-aloud audience while still allowing adventure, wonder, and mild mystery."
        ),
        prompt_adjustments=[
            "Treat fear as brief uncertainty or wistfulness, not terror or menace.",
            "Restore visible safety before ending any tense sequence.",
            "Favor warm, rhythmic language that naturally settles toward sleep.",
        ],
    ),
    BedtimeAudiencePresetPlan(
        key="preschool_gentle_3_to_5",
        label="Preschool Gentle",
        status="planned",
        age_band="Ages 3-5",
        summary=(
            "Future preset that further lowers the tension ceiling, shortens uncertainty "
            "windows, and relies on very explicit reassurance."
        ),
        prompt_adjustments=[
            "Reduce abstract peril and keep support figures present almost constantly.",
            "Use simpler emotional naming and faster repair beats after surprises.",
        ],
    ),
    BedtimeAudiencePresetPlan(
        key="early_reader_calm_6_to_8",
        label="Early Reader Calm Adventure",
        status="planned",
        age_band="Ages 6-8",
        summary=(
            "Future preset that preserves calm mystery and quest momentum while allowing a "
            "slightly wider emotional range than the preschool track."
        ),
        prompt_adjustments=[
            "Allow slightly longer puzzle-solving stretches as long as safe exits remain visible.",
            "Keep setbacks tender and resolvable through teamwork rather than confrontation.",
        ],
    ),
    BedtimeAudiencePresetPlan(
        key="older_kids_soft_mystery_9_to_12",
        label="Older Kids Soft Mystery",
        status="planned",
        age_band="Ages 9-12",
        summary=(
            "Future preset that supports richer mystery structure and more reflective low "
            "points without abandoning the bedtime emotional landing."
        ),
        prompt_adjustments=[
            "Permit more layered ambiguity while avoiding horror imagery or hopeless despair.",
            "Use reflective emotional repair rather than flattening every scene into cheerfulness.",
        ],
    ),
)

_ACTIVE_BEDTIME_GUIDELINE_PRESET_KEYS = frozenset(
    preset.key for preset in BEDTIME_AUDIENCE_PRESET_PLAN if preset.status == "active"
)


def normalize_bedtime_guideline_preset_key(value: str | None) -> str:
    if value is None:
        return DEFAULT_BEDTIME_GUIDELINE_PRESET_KEY

    normalized = value.strip()
    if not normalized:
        return DEFAULT_BEDTIME_GUIDELINE_PRESET_KEY

    if normalized not in _ACTIVE_BEDTIME_GUIDELINE_PRESET_KEYS:
        raise ValueError(f"unsupported bedtime guideline preset key: {normalized}")

    return normalized


def get_bedtime_audience_preset_plan() -> tuple[BedtimeAudiencePresetPlan, ...]:
    return BEDTIME_AUDIENCE_PRESET_PLAN
