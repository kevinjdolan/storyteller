from __future__ import annotations

import re
from typing import Any

from app.ai import (
    BriefNormalizationAdapter,
    build_brief_normalization_invocation,
)
from app.models import (
    BriefNormalizationPromptContext,
    BriefNormalizationResult,
    NormalizedBriefPreferences,
    normalize_optional_brief_text,
)

_PROTAGONIST_VERBS = (
    "follows",
    "follow",
    "drifts",
    "drift",
    "helps",
    "help",
    "guides",
    "guide",
    "rows",
    "row",
    "sails",
    "sail",
    "travels",
    "travel",
    "crosses",
    "cross",
    "searches",
    "search",
    "sets",
    "set",
    "tries",
    "try",
    "brings",
    "bring",
    "returns",
    "return",
    "journeys",
    "journey",
    "glides",
    "glide",
    "learns",
    "learn",
    "dreams",
    "dream",
    "finds",
    "find",
    "wants",
    "want",
    "must",
    "needs",
    "need",
)
_PROTAGONIST_PATTERN = re.compile(
    r"^((?:A|An|The)\s.+?)\s+(?:" + "|".join(_PROTAGONIST_VERBS) + r")\b",
    re.IGNORECASE,
)
_SETTING_PATTERN = re.compile(
    r"\b(?:in|across|through|at|under|around|near|over|inside|along)\s+"
    r"((?:a|an|the)\s+[^.,;]+?)(?:\s+(?:to|while|before|after|so)\b|[.,;]|$)",
    re.IGNORECASE,
)
_MOTIF_KEYWORDS = (
    "lantern",
    "moon",
    "harbor",
    "lake",
    "otter",
    "fox",
    "rabbit",
    "bear",
    "owl",
    "dragon",
    "lighthouse",
    "river",
    "reed",
    "star",
    "feather",
    "boat",
    "skiff",
    "water",
    "forest",
    "dock",
    "garden",
    "nest",
)
_RISK_KEYWORDS = {
    "fog",
    "storm",
    "shadow",
    "monster",
    "ghost",
    "dark",
    "lost",
    "alone",
    "runaway",
    "cliff",
    "howl",
    "spooky",
    "scary",
}


class BriefNormalizationService:
    def __init__(
        self,
        *,
        adapter: BriefNormalizationAdapter | None = None,
    ) -> None:
        self._adapter = adapter

    def normalize_brief(
        self,
        *,
        raw_brief: str,
        genre_label: str | None = None,
        tone_label: str | None = None,
        story_idea: str | None = None,
        desired_themes: str | None = None,
        key_images: str | None = None,
        audience_notes: str | None = None,
        must_have_elements: str | None = None,
    ) -> BriefNormalizationResult:
        context = BriefNormalizationPromptContext(
            raw_brief=raw_brief,
            genre_label=genre_label,
            tone_label=tone_label,
            story_idea=story_idea,
            desired_themes=desired_themes,
            key_images=key_images,
            audience_notes=audience_notes,
            must_have_elements=must_have_elements,
        )

        if self._adapter is not None:
            invocation = build_brief_normalization_invocation(
                context,
                model_id=self._adapter.model_id,
            )
            try:
                result = self._adapter.normalize(invocation)
                return BriefNormalizationResult(
                    source="gemini",
                    model_id=result.invocation.model_id,
                    prompt_version=result.invocation.prompt_version,
                    normalized_summary=result.structured_output.normalized_summary,
                    normalized_preferences=result.structured_output.normalized_preferences,
                    raw_response=result.raw_response,
                )
            except Exception as exc:
                return _build_heuristic_result(
                    context,
                    fallback_reason=str(exc),
                    fallback_detail=getattr(exc, "failure_detail", None),
                    model_id=invocation.model_id,
                    prompt_version=invocation.prompt_version,
                )

        return _build_heuristic_result(context)


def apply_brief_normalization_overrides(
    base_result: BriefNormalizationResult,
    *,
    raw_brief: str,
    normalized_summary: str | None,
    normalized_summary_provided: bool,
    normalized_preferences: NormalizedBriefPreferences | None,
    normalized_preferences_provided: bool,
) -> BriefNormalizationResult:
    resolved_preferences = (
        normalized_preferences
        if normalized_preferences_provided and normalized_preferences is not None
        else (
            NormalizedBriefPreferences()
            if normalized_preferences_provided
            else base_result.normalized_preferences
        )
    )

    resolved_summary = (
        normalized_summary if normalized_summary_provided else base_result.normalized_summary
    )
    if resolved_summary is None:
        resolved_summary = synthesize_normalized_summary(
            resolved_preferences,
            raw_brief=raw_brief,
        )

    source = base_result.source
    if normalized_summary_provided or normalized_preferences_provided:
        source = f"{base_result.source}_with_user_overrides"

    return BriefNormalizationResult(
        source=source,
        model_id=base_result.model_id,
        prompt_version=base_result.prompt_version,
        normalized_summary=resolved_summary,
        normalized_preferences=resolved_preferences,
        raw_response=base_result.raw_response,
    )


def build_brief_model_output(result: BriefNormalizationResult) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "schema_version": 1,
        "normalization_source": result.source,
    }
    if result.model_id is not None:
        payload["model_id"] = result.model_id
    if result.prompt_version is not None:
        payload["prompt_version"] = result.prompt_version
    if result.raw_response is not None:
        payload["raw_response"] = result.raw_response
    return payload


def build_brief_normalization_result_from_existing(
    *,
    normalized_summary: str | None,
    normalized_preferences: dict[str, Any] | None,
    model_output: dict[str, Any] | list[Any] | None,
) -> BriefNormalizationResult:
    metadata = model_output if isinstance(model_output, dict) else {}
    return BriefNormalizationResult(
        source=str(metadata.get("normalization_source", "existing")),
        model_id=_optional_str(metadata.get("model_id")),
        prompt_version=_optional_str(metadata.get("prompt_version")),
        normalized_summary=normalized_summary,
        normalized_preferences=NormalizedBriefPreferences.model_validate(
            normalized_preferences or {}
        ),
        raw_response=metadata.get("raw_response"),
    )


def synthesize_normalized_summary(
    preferences: NormalizedBriefPreferences,
    *,
    raw_brief: str,
) -> str | None:
    if not preferences.has_content():
        return _truncate(raw_brief, limit=220)

    subject = preferences.protagonist_type or "A bedtime protagonist"
    summary = _sentence_case(subject)
    if preferences.setting is not None:
        summary += f" in {preferences.setting}"
    if preferences.emotional_goal is not None:
        summary += f", aiming for {preferences.emotional_goal}"
    summary += "."

    if preferences.candidate_motifs:
        motifs = ", ".join(preferences.candidate_motifs[:3])
        summary += f" Recurring motifs include {motifs}."

    return summary


def _build_heuristic_result(
    context: BriefNormalizationPromptContext,
    *,
    fallback_reason: str | None = None,
    fallback_detail: Any | None = None,
    model_id: str | None = None,
    prompt_version: str | None = None,
) -> BriefNormalizationResult:
    preferences = NormalizedBriefPreferences(
        protagonist_type=_infer_protagonist_type(context),
        setting=_infer_setting(context),
        emotional_goal=_infer_emotional_goal(context),
        constraint_notes=_infer_constraint_notes(context),
        bedtime_safety_concerns=_infer_bedtime_safety_concerns(context),
        candidate_motifs=_infer_candidate_motifs(context),
    )
    normalized_summary = synthesize_normalized_summary(
        preferences,
        raw_brief=context.raw_brief,
    )
    raw_response: dict[str, Any] = {
        "heuristic_context": context.model_dump(mode="json"),
    }
    if fallback_reason is not None:
        raw_response["fallback_reason"] = fallback_reason
    if hasattr(fallback_detail, "to_metadata"):
        raw_response["fallback_classification"] = fallback_detail.to_metadata()

    return BriefNormalizationResult(
        source="heuristic",
        model_id=model_id,
        prompt_version=prompt_version,
        normalized_summary=normalized_summary,
        normalized_preferences=preferences,
        raw_response=raw_response,
    )


def _infer_protagonist_type(context: BriefNormalizationPromptContext) -> str | None:
    sentence = _first_sentence(context.story_idea or context.raw_brief)
    match = _PROTAGONIST_PATTERN.match(sentence)
    if match:
        return normalize_optional_brief_text(match.group(1))

    lowered = sentence.lower()
    for keyword in (
        "child",
        "fox",
        "rabbit",
        "bear",
        "owl",
        "otter",
        "dragon",
        "sibling",
        "friend",
        "guardian",
    ):
        if keyword in lowered:
            return _sentence_case(f"a {keyword} protagonist")

    return None


def _infer_setting(context: BriefNormalizationPromptContext) -> str | None:
    for source in (context.story_idea, context.raw_brief, context.key_images):
        if source is None:
            continue
        match = _SETTING_PATTERN.search(source)
        if match:
            return normalize_optional_brief_text(match.group(1))

    lowered = context.raw_brief.lower()
    for keyword in (
        "harbor",
        "lake",
        "forest",
        "docks",
        "village",
        "garden",
        "lighthouse",
        "river",
        "shore",
        "nest",
    ):
        if keyword in lowered:
            return f"a {keyword}"

    return None


def _infer_emotional_goal(context: BriefNormalizationPromptContext) -> str | None:
    combined = " ".join(
        value
        for value in (
            context.must_have_elements,
            context.desired_themes,
            context.audience_notes,
            context.raw_brief,
        )
        if value
    ).lower()

    goals: list[str] = []
    if "belong" in combined:
        goals.append("belonging")
    if "brave" in combined or "courage" in combined:
        goals.append("gentle courage")
    if "calm" in combined or "rest" in combined or "sleep" in combined or "bed" in combined:
        goals.append("a restful sense of safety")
    if "home" in combined or "return" in combined or "reunion" in combined:
        goals.append("a safe return home")
    if "repair" in combined or "reassur" in combined or "comfort" in combined:
        goals.append("emotional repair")

    if goals:
        return ", ".join(dict.fromkeys(goals))

    if context.desired_themes is not None:
        return _truncate(context.desired_themes, limit=140)

    return "a calm, reassuring bedtime landing"


def _infer_constraint_notes(context: BriefNormalizationPromptContext) -> list[str]:
    notes: list[str] = []
    for source in (context.must_have_elements, context.audience_notes):
        normalized = normalize_optional_brief_text(source)
        if normalized is None:
            continue
        notes.extend(_split_into_notes(normalized))

    return notes[:4]


def _infer_bedtime_safety_concerns(context: BriefNormalizationPromptContext) -> list[str]:
    combined = " ".join(
        value
        for value in (
            context.audience_notes,
            context.must_have_elements,
            context.raw_brief,
            context.desired_themes,
        )
        if value
    ).lower()

    concerns: list[str] = []
    if "sensitive" in combined:
        concerns.append("Keep the emotional stakes gentle for a sensitive listener.")
    if any(keyword in combined for keyword in _RISK_KEYWORDS):
        concerns.append("Let any mystery or danger resolve quickly and clearly.")
    if any(keyword in combined for keyword in ("lost", "alone", "runaway", "separate")):
        concerns.append("Keep separation brief and pair it with steady reassurance.")
    if "villain" in combined or "spooky" in combined or "scary" in combined:
        concerns.append("Avoid antagonists or imagery that tips into scary territory.")
    if not concerns and any(
        keyword in combined for keyword in ("bed", "sleep", "rest", "calm", "tucked")
    ):
        concerns.append("Ensure the ending lands in a clearly safe, restful place.")

    return concerns[:4]


def _infer_candidate_motifs(context: BriefNormalizationPromptContext) -> list[str]:
    motifs: list[str] = []
    if context.key_images is not None:
        motifs.extend(_split_into_notes(context.key_images))

    search_space = " ".join(
        value for value in (context.story_idea, context.raw_brief) if value is not None
    )
    lowered = search_space.lower()
    for keyword in _MOTIF_KEYWORDS:
        if keyword not in lowered:
            continue
        match = re.search(
            rf"\b(?:[a-z]+\s+){{0,2}}{re.escape(keyword)}(?:s)?\b",
            search_space,
            re.IGNORECASE,
        )
        if match is None:
            motifs.append(keyword)
            continue
        motif = normalize_optional_brief_text(match.group(0))
        if motif is not None:
            motifs.append(motif)

    return list(dict.fromkeys(motifs))[:6]


def _split_into_notes(value: str) -> list[str]:
    normalized: list[str] = []
    for part in re.split(r"[\n;]+|,(?=\s*[a-zA-Z])", value):
        item = normalize_optional_brief_text(part)
        if item is None or item in normalized:
            continue
        normalized.append(item)
    return normalized


def _first_sentence(value: str) -> str:
    match = re.split(r"(?<=[.!?])\s+", value.strip(), maxsplit=1)
    return match[0]


def _sentence_case(value: str) -> str:
    if not value:
        return value
    return value[0].upper() + value[1:]


def _truncate(value: str, *, limit: int) -> str:
    if len(value) <= limit:
        return value
    return f"{value[: limit - 3].rstrip()}..."


def _optional_str(value: Any) -> str | None:
    if value is None:
        return None
    return normalize_optional_brief_text(str(value))
