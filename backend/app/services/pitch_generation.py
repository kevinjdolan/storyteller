from __future__ import annotations

import re
from typing import Any

from app.ai import PitchGenerationAdapter, build_pitch_generation_invocation
from app.models import (
    ExistingSelectedPitchContext,
    GeneratedPitchCandidate,
    NormalizedBriefPreferences,
    PitchBatchEvaluation,
    PitchBatchEvaluationCriterion,
    PitchGenerationPromptContext,
    PitchGenerationResult,
    normalize_optional_pitch_text,
)
from app.models.bedtime_guidelines import DEFAULT_BEDTIME_GUIDELINE_PRESET_KEY

_TITLE_STOPWORDS = {
    "a",
    "an",
    "and",
    "at",
    "before",
    "for",
    "from",
    "in",
    "into",
    "of",
    "on",
    "or",
    "the",
    "to",
    "with",
}
_LENS_LIBRARY = (
    {
        "title_suffix": "Promise",
        "hook": (
            "{protagonist} agrees to carry {primary_motif} across {setting} so the whole "
            "night can settle into place."
        ),
        "conflict": (
            "To finish the journey before bedtime, {hero} must solve a string of small, "
            "comfort-sized problems without letting the route home grow frightening."
        ),
        "fit": (
            "It fits {genre} and {tone} by turning the brief into a gentle quest with steady "
            "movement, soft stakes, and a clearly restful landing."
        ),
    },
    {
        "title_suffix": "Question",
        "hook": (
            "When one last {secondary_motif} stays awake in {setting}, {protagonist} follows "
            "the hush behind it to learn what the night still needs."
        ),
        "conflict": (
            "The mystery has to be solved before everyone can rest, but {hero} must keep each "
            "discovery reassuring instead of escalating the tension."
        ),
        "fit": (
            "It fits {genre} and {tone} by offering bedtime-safe mystery, luminous imagery, "
            "and a soothing answer instead of a harsh twist."
        ),
    },
    {
        "title_suffix": "Map",
        "hook": (
            "{protagonist} discovers a hidden path of {primary_motif} that quietly points "
            "toward the night's most important unfinished kindness."
        ),
        "conflict": (
            "Each clue asks {hero} to choose patience and care before the final stop can turn "
            "{emotional_goal} into something real."
        ),
        "fit": (
            "It fits {genre} and {tone} because the brief becomes a calm treasure trail, with "
            "wonder carrying the emotional repair instead of danger."
        ),
    },
    {
        "title_suffix": "Song",
        "hook": (
            "A quiet rhythm starts moving through {setting}, and {protagonist} follows it to "
            "help a worried friend settle the night."
        ),
        "conflict": (
            "{hero_cap} has to understand what the rhythm is asking for before a small bedtime "
            "imbalance keeps everyone from relaxing."
        ),
        "fit": (
            "It fits {genre} and {tone} by leaning into sensory calm, companionship, and a "
            "repair-focused conflict that stays soft all the way through."
        ),
    },
    {
        "title_suffix": "Errand",
        "hook": (
            "{protagonist} is entrusted with one last sleepy errand through {setting}, where "
            "each stop reveals a gentler version of the night's worry."
        ),
        "conflict": (
            "The errand only works if {hero} can keep helping others without losing sight of "
            "the safe return promised in the brief."
        ),
        "fit": (
            "It fits {genre} and {tone} because the structure supports warm encounters, "
            "bedtime pacing, and a final return that feels earned and calm."
        ),
    },
    {
        "title_suffix": "Reunion",
        "hook": (
            "Just before sleep, {protagonist} notices that {secondary_motif} is quietly leading "
            "everyone toward a hidden nighttime reunion in {setting}."
        ),
        "conflict": (
            "To reach the reunion in time, {hero} must interpret the signs correctly while "
            "keeping the emotional atmosphere gentle and reassuring."
        ),
        "fit": (
            "It fits {genre} and {tone} by giving the story a cozy reveal, a shared emotional "
            "goal, and bedtime-safe suspense that resolves into belonging."
        ),
    },
)


class PitchGenerationService:
    def __init__(
        self,
        *,
        adapter: PitchGenerationAdapter | None = None,
    ) -> None:
        self._adapter = adapter

    def generate_pitches(
        self,
        *,
        candidate_count: int,
        generation_goal: str = "alternatives",
        bedtime_guideline_preset_key: str = DEFAULT_BEDTIME_GUIDELINE_PRESET_KEY,
        raw_brief: str,
        genre_label: str | None = None,
        genre_description: str | None = None,
        genre_bedtime_safety_notes: str | None = None,
        tone_label: str | None = None,
        tone_description: str | None = None,
        tone_bedtime_notes: str | None = None,
        normalized_summary: str | None = None,
        story_idea: str | None = None,
        desired_themes: str | None = None,
        key_images: str | None = None,
        audience_notes: str | None = None,
        must_have_elements: str | None = None,
        planning_notes: str | None = None,
        normalized_preferences: NormalizedBriefPreferences | None = None,
        guidance: str | None = None,
        selected_pitch: ExistingSelectedPitchContext | None = None,
    ) -> PitchGenerationResult:
        context = PitchGenerationPromptContext(
            candidate_count=candidate_count,
            generation_goal=generation_goal,
            bedtime_guideline_preset_key=bedtime_guideline_preset_key,
            guidance=guidance,
            genre_label=genre_label,
            genre_description=genre_description,
            genre_bedtime_safety_notes=genre_bedtime_safety_notes,
            tone_label=tone_label,
            tone_description=tone_description,
            tone_bedtime_notes=tone_bedtime_notes,
            raw_brief=raw_brief,
            normalized_summary=normalized_summary,
            story_idea=story_idea,
            desired_themes=desired_themes,
            key_images=key_images,
            audience_notes=audience_notes,
            must_have_elements=must_have_elements,
            planning_notes=planning_notes,
            normalized_preferences=normalized_preferences or NormalizedBriefPreferences(),
            selected_pitch=selected_pitch,
        )

        if self._adapter is not None:
            invocation = build_pitch_generation_invocation(
                context,
                model_id=self._adapter.model_id,
            )
            try:
                result = self._adapter.generate(invocation)
                evaluation = evaluate_pitch_batch(
                    result.structured_output.pitches,
                    requested_count=candidate_count,
                )
                if evaluation.passed:
                    return PitchGenerationResult(
                        source="gemini",
                        model_id=result.invocation.model_id,
                        prompt_version=result.invocation.prompt_version,
                        pitches=result.structured_output.pitches,
                        evaluation=evaluation,
                        raw_response=result.raw_response,
                    )
                return _build_heuristic_result(
                    context,
                    fallback_reason=_build_validation_failure_reason(evaluation),
                    adapter_raw_response=result.raw_response,
                    model_id=invocation.model_id,
                    prompt_version=invocation.prompt_version,
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


def evaluate_pitch_batch(
    pitches: list[GeneratedPitchCandidate],
    *,
    requested_count: int,
) -> PitchBatchEvaluation:
    normalized_titles = {_normalize_compare(candidate.title) for candidate in pitches}
    normalized_hooks = {_normalize_compare(candidate.hook) for candidate in pitches}
    filled_fields = sum(
        1
        for candidate in pitches
        if all(
            normalize_optional_pitch_text(value) is not None
            for value in (
                candidate.title,
                candidate.hook,
                candidate.central_conflict,
                candidate.why_it_fits,
            )
        )
    )
    descriptive_conflicts = sum(
        1 for candidate in pitches if len(candidate.central_conflict.split()) >= 6
    )
    grounded_fit_notes = sum(1 for candidate in pitches if len(candidate.why_it_fits.split()) >= 6)

    criteria = [
        PitchBatchEvaluationCriterion(
            name="candidate_count_matches_request",
            passed=len(pitches) == requested_count,
            measured_value=len(pitches),
            detail=f"Requested {requested_count} pitch candidates.",
        ),
        PitchBatchEvaluationCriterion(
            name="all_required_fields_present",
            passed=filled_fields == len(pitches),
            measured_value=filled_fields,
            detail="Each candidate must include title, hook, central conflict, and why it fits.",
        ),
        PitchBatchEvaluationCriterion(
            name="titles_are_distinct",
            passed=len(normalized_titles) == len(pitches),
            measured_value=len(normalized_titles),
            detail="Distinct titles help the user compare options quickly.",
        ),
        PitchBatchEvaluationCriterion(
            name="hooks_are_distinct",
            passed=len(normalized_hooks) == len(pitches),
            measured_value=len(normalized_hooks),
            detail="Hooks should not collapse into trivial rewrites.",
        ),
        PitchBatchEvaluationCriterion(
            name="central_conflicts_are_descriptive",
            passed=descriptive_conflicts == len(pitches),
            measured_value=descriptive_conflicts,
            detail="Conflicts should say more than a fragment.",
        ),
        PitchBatchEvaluationCriterion(
            name="why_it_fits_notes_are_grounded",
            passed=grounded_fit_notes == len(pitches),
            measured_value=grounded_fit_notes,
            detail="Fit notes should explicitly explain the bedtime match.",
        ),
    ]

    return PitchBatchEvaluation(
        passed=all(criterion.passed for criterion in criteria),
        criteria=criteria,
    )


def build_pitch_model_output(result: PitchGenerationResult) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "schema_version": 1,
        "generation_source": result.source,
        "evaluation": result.evaluation.model_dump(mode="json"),
    }
    if result.model_id is not None:
        payload["model_id"] = result.model_id
    if result.prompt_version is not None:
        payload["prompt_version"] = result.prompt_version
    if result.raw_response is not None:
        payload["raw_response"] = result.raw_response
    return payload


def _build_heuristic_result(
    context: PitchGenerationPromptContext,
    *,
    fallback_reason: str | None = None,
    fallback_detail: Any | None = None,
    adapter_raw_response: dict[str, Any] | list[Any] | str | None = None,
    model_id: str | None = None,
    prompt_version: str | None = None,
) -> PitchGenerationResult:
    pitches = _build_heuristic_pitches(context)
    evaluation = evaluate_pitch_batch(
        pitches,
        requested_count=context.candidate_count,
    )
    raw_response: dict[str, Any] = {
        "heuristic": True,
    }
    if fallback_reason is not None:
        raw_response["fallback_reason"] = fallback_reason
    if hasattr(fallback_detail, "to_metadata"):
        raw_response["fallback_classification"] = fallback_detail.to_metadata()
    if adapter_raw_response is not None:
        raw_response["adapter_raw_response"] = adapter_raw_response

    return PitchGenerationResult(
        source="heuristic",
        model_id=model_id,
        prompt_version=prompt_version,
        pitches=pitches,
        evaluation=evaluation,
        raw_response=raw_response,
    )


def _build_heuristic_pitches(
    context: PitchGenerationPromptContext,
) -> list[GeneratedPitchCandidate]:
    if context.generation_goal == "refinement" and context.selected_pitch is not None:
        return _build_heuristic_refined_pitches(context)

    protagonist = (
        context.normalized_preferences.protagonist_type
        or context.story_idea
        or _extract_subject_phrase(context.raw_brief)
        or "A gentle bedtime hero"
    )
    setting = (
        context.normalized_preferences.setting
        or _extract_setting_phrase(context.raw_brief)
        or "a calm night landscape"
    )
    emotional_goal = context.normalized_preferences.emotional_goal or "a safe return home"
    motifs = _collect_motifs(context)
    themes = _collect_themes(context)
    genre = context.genre_label or "the selected genre"
    tone = context.tone_label or "the selected tone"
    hero = _subject_tail(protagonist)
    hero_cap = hero[:1].upper() + hero[1:] if hero else "They"
    primary_motif = motifs[0]
    secondary_motif = motifs[1] if len(motifs) > 1 else motifs[0]

    candidates: list[GeneratedPitchCandidate] = []
    for index, lens in enumerate(_LENS_LIBRARY[: context.candidate_count]):
        title_seed = motifs[index % len(motifs)]
        title = _build_title(title_seed, lens["title_suffix"])
        hook = lens["hook"].format(
            protagonist=protagonist,
            primary_motif=primary_motif.lower(),
            secondary_motif=secondary_motif.lower(),
            setting=setting,
        )
        conflict = lens["conflict"].format(
            hero=hero,
            hero_cap=hero_cap,
            emotional_goal=emotional_goal,
        )
        fit = lens["fit"].format(
            genre=genre,
            tone=tone,
        )

        if themes:
            fit = f"{fit} It keeps {themes[0]} at the center."
        if context.guidance:
            fit = f"{fit} Guidance applied: {context.guidance}"

        candidates.append(
            GeneratedPitchCandidate(
                title=title,
                hook=hook,
                central_conflict=conflict,
                why_it_fits=fit,
            )
        )

    return candidates


def _build_heuristic_refined_pitches(
    context: PitchGenerationPromptContext,
) -> list[GeneratedPitchCandidate]:
    assert context.selected_pitch is not None

    source_pitch = context.selected_pitch
    guidance = context.guidance or "Keep the pitch bedtime-safe while preserving its core premise."
    protagonist = (
        context.normalized_preferences.protagonist_type
        or context.story_idea
        or _extract_subject_phrase(context.raw_brief)
        or "A gentle bedtime hero"
    )
    setting = (
        context.normalized_preferences.setting
        or _extract_setting_phrase(context.raw_brief)
        or "a calm night landscape"
    )
    source_title_core = re.sub(r"^The\s+", "", source_pitch.title).strip()
    title_suffix = _extract_candidate_phrases(guidance)[:1]
    title = (
        f"{source_title_core}: {_title_case_phrase(title_suffix[0])}"
        if title_suffix
        else f"{source_title_core}: Softened"
    )
    hook = (
        f"{source_pitch.hook} This refinement keeps the same bedtime lane while applying: "
        f"{guidance}."
    )
    conflict = source_pitch.central_conflict or (
        f"{protagonist} must solve one gentle nighttime problem in "
        f"{setting} before rest can return."
    )
    fit = (
        f"This refinement preserves the core appeal of {source_pitch.title} while applying the "
        f"requested change: {guidance}."
    )

    return [
        GeneratedPitchCandidate(
            title=title,
            hook=hook,
            central_conflict=conflict,
            why_it_fits=fit,
        )
    ]


def _build_validation_failure_reason(evaluation: PitchBatchEvaluation) -> str:
    failed = [criterion.name for criterion in evaluation.criteria if not criterion.passed]
    return "generated pitches failed validation: " + ", ".join(failed)


def _normalize_compare(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", value.lower()).strip()


def _build_title(motif: str, suffix: str) -> str:
    motif_words = [word for word in re.split(r"\s+", motif) if word]
    title_words = [
        word.capitalize() for word in motif_words if word.lower() not in _TITLE_STOPWORDS
    ]
    title_core = " ".join(title_words[:3]) or "Quiet Light"
    return f"The {title_core} {suffix}"


def _title_case_phrase(value: str) -> str:
    words = [word for word in re.split(r"\s+", value.strip()) if word]
    if not words:
        return "Softened"
    return " ".join(word.capitalize() for word in words[:4])


def _collect_motifs(context: PitchGenerationPromptContext) -> list[str]:
    motifs = list(context.normalized_preferences.candidate_motifs)
    for source in (context.key_images, context.raw_brief):
        if source is None:
            continue
        motifs.extend(_extract_candidate_phrases(source))

    unique: list[str] = []
    for motif in motifs:
        normalized = normalize_optional_pitch_text(motif)
        if normalized is None or normalized.lower() in {item.lower() for item in unique}:
            continue
        unique.append(normalized)

    return unique[:5] or ["Quiet Light", "Moonlit Path"]


def _collect_themes(context: PitchGenerationPromptContext) -> list[str]:
    if context.desired_themes is None:
        return []
    return [
        item
        for item in re.split(r"[\n,;]+", context.desired_themes)
        if normalize_optional_pitch_text(item) is not None
    ]


def _extract_candidate_phrases(value: str) -> list[str]:
    phrases = []
    for candidate in re.split(r"[\n,;]+", value):
        normalized = normalize_optional_pitch_text(candidate)
        if normalized is None:
            continue
        phrases.append(normalized)
    return phrases


def _extract_subject_phrase(value: str) -> str | None:
    match = re.match(
        r"^((?:A|An|The)\s+[^.,;]+?)\s+(?:follows|drifts|guides|helps|carries|rows|sails|"
        r"travels|sets|tries|returns|searches|finds|discovers|wants|must)\b",
        value,
        re.IGNORECASE,
    )
    if match is None:
        return None
    return normalize_optional_pitch_text(match.group(1))


def _extract_setting_phrase(value: str) -> str | None:
    match = re.search(
        r"\b(?:in|across|through|over|near|along|inside)\s+((?:a|an|the)\s+[^.,;]+?)(?:\s+"
        r"(?:to|while|before|after|so)\b|[.,;]|$)",
        value,
        re.IGNORECASE,
    )
    if match is None:
        return None
    return normalize_optional_pitch_text(match.group(1))


def _subject_tail(value: str) -> str:
    normalized = re.sub(r"^(a|an|the)\s+", "", value, flags=re.IGNORECASE).strip()
    return normalized[:1].lower() + normalized[1:] if normalized else "they"
