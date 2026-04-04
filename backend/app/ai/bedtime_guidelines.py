from __future__ import annotations

from functools import lru_cache

from app.models.bedtime_guidelines import (
    DEFAULT_BEDTIME_GUIDELINE_PRESET_KEY,
    BedtimePromptStage,
    normalize_bedtime_guideline_preset_key,
)

_SHARED_POLICY_LINES: tuple[str, ...] = (
    "Audience preset: Shared Bedtime Default for a broad bedtime read-aloud audience.",
    (
        "Adventure, wonder, discovery, and mild mystery are welcome when the world keeps "
        "offering visible safety, trustworthy companionship, and a believable path back to calm."
    ),
    (
        "Maximum scare level: brief shivers, uncertainty, wistful mistakes, or soft suspense. "
        "Never escalate into horror, menace, cruelty, panic spirals, helpless entrapment, or "
        "grotesque imagery."
    ),
    (
        "Violence avoidance: do not depict assault, graphic injury, weapons use, revenge, "
        "on-page death, predatory pursuit, or punishment-driven conflict. Resolve problems "
        "through care, patience, teamwork, cleverness, or emotional honesty."
    ),
    (
        "Emotional repair: after every tense or sad beat, quickly add grounding actions, named "
        "feelings, supportive relationships, and evidence that the problem is manageable."
    ),
    (
        "Resolution requirement: the ending must land in safety, reconnection, and restful "
        "release. The final images should invite sleep instead of reopening suspense."
    ),
)

_STAGE_SPECIFIC_LINES: dict[BedtimePromptStage, tuple[str, ...]] = {
    "pitch": (
        "Keep the core conflict curious, tender, or gently urgent rather than perilous.",
        "Make the repair path legible in the hook or fit note so the bedtime promise is clear.",
    ),
    "character": (
        "Give the lead a comfort trait and at least one reliable source of support.",
        "Avoid cruel dynamics, humiliating authority figures, or isolated children with no help.",
    ),
    "beat": (
        (
            "Treat Save-the-Cat low points as tiredness, doubt, sadness, or misread signals "
            "instead of threat escalation."
        ),
        (
            "Pressure beats should pivot quickly toward reassurance, insight, or renewed "
            "togetherness."
        ),
    ),
    "composition": (
        (
            "Use calm sensory language, steady pacing, and orienting cues when mystery or "
            "tension rises."
        ),
        (
            "Avoid shock verbs, nightmare imagery, graphic detail, or cliffhanger endings "
            "that spike arousal."
        ),
    ),
    "audio": (
        (
            "Narration should sound warm, patient, and emotionally regulated rather than "
            "theatrical or alarming."
        ),
        (
            "Keep music subordinate to speech clarity and avoid sudden stingers, jump-scare "
            "phrasing, or aggressive performance cues."
        ),
    ),
}


@lru_cache(maxsize=None)
def build_bedtime_guidelines_fragment(
    *,
    stage: BedtimePromptStage,
    preset_key: str = DEFAULT_BEDTIME_GUIDELINE_PRESET_KEY,
) -> str:
    normalized_preset_key = normalize_bedtime_guideline_preset_key(preset_key)
    if normalized_preset_key != DEFAULT_BEDTIME_GUIDELINE_PRESET_KEY:
        raise ValueError(f"unsupported bedtime guideline preset key: {normalized_preset_key}")

    lines = [
        "Shared bedtime safety policy:",
        *[f"- {line}" for line in _SHARED_POLICY_LINES],
        f"Stage focus for {stage}:",
        *[f"- {line}" for line in _STAGE_SPECIFIC_LINES[stage]],
    ]
    return "\n".join(lines)
