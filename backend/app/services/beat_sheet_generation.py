from __future__ import annotations

import re
from typing import Any

from app.ai import BeatSheetGenerationAdapter, build_beat_sheet_generation_invocation
from app.models import (
    SAVE_THE_CAT_BEAT_KEYS,
    SAVE_THE_CAT_BEAT_SEQUENCE,
    BeatSheetEvaluation,
    BeatSheetEvaluationCriterion,
    BeatSheetGenerationPromptContext,
    BeatSheetGenerationResult,
    ExistingBeatSheetContext,
    ExistingCharacterSheetContext,
    ExistingSelectedPitchContext,
    GeneratedBeatSheetBeat,
    GeneratedBeatSheetCandidate,
    NormalizedBriefPreferences,
    normalize_optional_beat_text,
)
from app.models.bedtime_guidelines import DEFAULT_BEDTIME_GUIDELINE_PRESET_KEY

_TENSION_BEAT_KEYS = {
    "catalyst",
    "debate",
    "midpoint",
    "bad_guys_close_in",
    "all_is_lost",
    "dark_night_of_the_soul",
    "finale",
}


class BeatSheetGenerationService:
    def __init__(
        self,
        *,
        adapter: BeatSheetGenerationAdapter | None = None,
    ) -> None:
        self._adapter = adapter

    def generate_beat_sheet(
        self,
        *,
        generation_goal: str = "initial",
        bedtime_guideline_preset_key: str = DEFAULT_BEDTIME_GUIDELINE_PRESET_KEY,
        selected_pitch: ExistingSelectedPitchContext,
        selected_character_sheet: ExistingCharacterSheetContext,
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
        instructions: str | None = None,
        focus_beats: list[str] | None = None,
        bedtime_goal: str | None = None,
        existing_beat_sheet: ExistingBeatSheetContext | None = None,
    ) -> BeatSheetGenerationResult:
        context = BeatSheetGenerationPromptContext(
            generation_goal="refinement" if generation_goal == "refinement" else "initial",
            bedtime_guideline_preset_key=bedtime_guideline_preset_key,
            guidance=guidance,
            instructions=instructions,
            focus_beats=focus_beats or [],
            bedtime_goal=bedtime_goal,
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
            selected_character_sheet=selected_character_sheet,
            existing_beat_sheet=existing_beat_sheet,
        )

        if self._adapter is not None:
            try:
                invocation = build_beat_sheet_generation_invocation(
                    context,
                    model_id=self._adapter.model_id,
                )
                result = self._adapter.generate(invocation)
                evaluation = evaluate_beat_sheet(result.structured_output.beat_sheet)
                if evaluation.passed:
                    return BeatSheetGenerationResult(
                        source="gemini",
                        model_id=result.invocation.model_id,
                        prompt_version=result.invocation.prompt_version,
                        beat_sheet=result.structured_output.beat_sheet,
                        evaluation=evaluation,
                        raw_response=result.raw_response,
                    )
                return _build_heuristic_result(
                    context,
                    fallback_reason=_build_validation_failure_reason(evaluation),
                    adapter_raw_response=result.raw_response,
                )
            except Exception as exc:
                return _build_heuristic_result(
                    context,
                    fallback_reason=str(exc),
                )

        return _build_heuristic_result(context)


def evaluate_beat_sheet(beat_sheet: GeneratedBeatSheetCandidate) -> BeatSheetEvaluation:
    keys = [beat.key for beat in beat_sheet.beats]
    present_keys = {key for key in keys if key in SAVE_THE_CAT_BEAT_KEYS}
    summaries_present = sum(1 for beat in beat_sheet.beats if len(beat.summary.split()) >= 4)
    emotional_intents_present = sum(
        1 for beat in beat_sheet.beats if len(beat.emotional_intent.split()) >= 3
    )
    bedtime_notes_present = sum(
        1 for beat in beat_sheet.beats if len(beat.bedtime_softening_note.split()) >= 4
    )
    tension_beats_softened = sum(
        1
        for beat in beat_sheet.beats
        if beat.key in _TENSION_BEAT_KEYS and len(beat.bedtime_softening_note.split()) >= 5
    )

    criteria = [
        BeatSheetEvaluationCriterion(
            name="all_required_beats_present",
            passed=present_keys == set(SAVE_THE_CAT_BEAT_KEYS)
            and len(keys) == len(SAVE_THE_CAT_BEAT_KEYS),
            measured_value=len(present_keys),
            detail="The beat sheet must include the full Save-the-Cat progression.",
        ),
        BeatSheetEvaluationCriterion(
            name="beat_order_matches_framework",
            passed=keys == list(SAVE_THE_CAT_BEAT_KEYS),
            measured_value=len(
                [key for key, expected in zip(keys, SAVE_THE_CAT_BEAT_KEYS) if key == expected]
            ),
            detail="Beat ordering should follow the canonical Save-the-Cat sequence.",
        ),
        BeatSheetEvaluationCriterion(
            name="summaries_are_present_for_every_beat",
            passed=summaries_present == len(SAVE_THE_CAT_BEAT_KEYS),
            measured_value=summaries_present,
            detail="Each beat needs a short planning summary.",
        ),
        BeatSheetEvaluationCriterion(
            name="emotional_intents_are_present_for_every_beat",
            passed=emotional_intents_present == len(SAVE_THE_CAT_BEAT_KEYS),
            measured_value=emotional_intents_present,
            detail="Each beat needs an explicit emotional intent.",
        ),
        BeatSheetEvaluationCriterion(
            name="bedtime_softening_notes_are_present_for_every_beat",
            passed=bedtime_notes_present == len(SAVE_THE_CAT_BEAT_KEYS),
            measured_value=bedtime_notes_present,
            detail="Each beat needs a bedtime-softening note.",
        ),
        BeatSheetEvaluationCriterion(
            name="tension_beats_include_extra_softening",
            passed=tension_beats_softened == len(_TENSION_BEAT_KEYS),
            measured_value=tension_beats_softened,
            detail="Pressure beats must stay explicitly bedtime-safe.",
        ),
        BeatSheetEvaluationCriterion(
            name="overall_summary_and_bedtime_notes_are_present",
            passed=(
                len(beat_sheet.summary.split()) >= 5
                and len(beat_sheet.bedtime_notes.split()) >= 5
            ),
            measured_value=2,
            detail="The beat sheet needs a high-level summary and overall bedtime notes.",
        ),
    ]

    return BeatSheetEvaluation(
        passed=all(criterion.passed for criterion in criteria),
        criteria=criteria,
    )


def build_beat_sheet_model_output(result: BeatSheetGenerationResult) -> dict[str, Any]:
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
    context: BeatSheetGenerationPromptContext,
    *,
    fallback_reason: str | None = None,
    adapter_raw_response: dict[str, Any] | list[Any] | str | None = None,
) -> BeatSheetGenerationResult:
    beat_sheet = _build_heuristic_beat_sheet(context)
    evaluation = evaluate_beat_sheet(beat_sheet)
    raw_response: dict[str, Any] = {
        "heuristic": True,
    }
    if fallback_reason is not None:
        raw_response["fallback_reason"] = fallback_reason
    if adapter_raw_response is not None:
        raw_response["adapter_raw_response"] = adapter_raw_response

    return BeatSheetGenerationResult(
        source="heuristic",
        beat_sheet=beat_sheet,
        evaluation=evaluation,
        raw_response=raw_response,
    )


def _build_heuristic_beat_sheet(
    context: BeatSheetGenerationPromptContext,
) -> GeneratedBeatSheetCandidate:
    protagonist_name = _read_protagonist_name(context.selected_character_sheet)
    helper_name = _read_helper_name(context.selected_character_sheet)
    setting = _read_setting(context)
    emotional_goal = _read_emotional_goal(context)
    motifs = _read_motifs(context)
    lead_dynamic = _read_lead_dynamic(context.selected_character_sheet)
    focus_beats = {beat.lower() for beat in context.focus_beats}
    guidance_text = context.instructions or context.guidance
    existing_beat_entries = (
        context.existing_beat_sheet.beats if context.existing_beat_sheet is not None else []
    )
    existing_beats = {
        beat.key: beat for beat in existing_beat_entries
    }

    beats: list[GeneratedBeatSheetBeat] = []
    for index, (key, label) in enumerate(SAVE_THE_CAT_BEAT_SEQUENCE):
        existing = existing_beats.get(key)
        beat = _build_heuristic_beat(
            key=key,
            label=label,
            index=index,
            protagonist_name=protagonist_name,
            helper_name=helper_name,
            setting=setting,
            emotional_goal=emotional_goal,
            motifs=motifs,
            lead_dynamic=lead_dynamic,
            pitch=context.selected_pitch,
            focus_beats=focus_beats,
            guidance_text=guidance_text,
            bedtime_goal=context.bedtime_goal,
            existing=existing,
            is_refinement=context.generation_goal == "refinement",
        )
        beats.append(beat)

    summary = (
        f"{protagonist_name} moves through a full Save-the-Cat arc in {setting}, with each beat "
        f"guiding the story toward {emotional_goal}."
    )
    if context.generation_goal == "refinement" and guidance_text is not None:
        summary = (
            f"{summary} This revision preserves the core plan while applying: "
            f"{guidance_text}."
        )

    bedtime_notes = (
        "Keep the tension readable, the helpers visible, and the final emotional landing "
        "unmistakably safe and sleepy."
    )
    if context.bedtime_goal is not None:
        bedtime_notes = f"{bedtime_notes} Bedtime goal: {context.bedtime_goal}."

    return GeneratedBeatSheetCandidate(
        summary=summary,
        bedtime_notes=bedtime_notes,
        beats=beats,
    )


def _build_heuristic_beat(
    *,
    key: str,
    label: str,
    index: int,
    protagonist_name: str,
    helper_name: str,
    setting: str,
    emotional_goal: str,
    motifs: list[str],
    lead_dynamic: str,
    pitch: ExistingSelectedPitchContext,
    focus_beats: set[str],
    guidance_text: str | None,
    bedtime_goal: str | None,
    existing: GeneratedBeatSheetBeat | None,
    is_refinement: bool,
) -> GeneratedBeatSheetBeat:
    motif = motifs[index % len(motifs)]
    templates = {
        "opening_image": (
            (
                f"{protagonist_name} is introduced in {setting}, surrounded by {motif} and the "
                "everyday rhythm that makes the night feel safe."
            ),
            "Signal calm curiosity and a stable bedtime baseline.",
            "Use familiar routines and soft sensory cues so the opening already feels sheltered.",
        ),
        "theme_stated": (
            (
                f"{helper_name} or another trusted voice hints that rest will come when "
                f"{protagonist_name} stops carrying every worry alone."
            ),
            "Plant the reassurance lesson early and gently.",
            "Keep the theme phrased as comfort or belonging, not a stern moral.",
        ),
        "set_up": (
            (
                f"The story establishes {lead_dynamic}, the night's small imbalance, and the "
                f"tender stakes behind {pitch.title}."
            ),
            "Build investment without rushing the bedtime pace.",
            "Frame the problem as manageable and emotionally readable from the start.",
        ),
        "catalyst": (
            (
                f"A clear but gentle disruption appears around {motif}, giving "
                f"{protagonist_name} one reason they cannot simply go to sleep yet."
            ),
            "Spark forward motion while keeping the disturbance soft.",
            "Treat the disruption as intriguing or wistful rather than frightening.",
        ),
        "debate": (
            (
                f"{protagonist_name} hesitates, weighing whether to stay with the familiar calm "
                f"or follow the night's quiet invitation with {helper_name}."
            ),
            "Let the listener feel a small, relatable wobble before the adventure opens.",
            "Keep the hesitation brief and buffered by companionship, ritual, or visible safety.",
        ),
        "break_into_two": (
            (
                f"{protagonist_name} chooses the bedtime-safe adventure and steps into a more "
                f"magical side of {setting}."
            ),
            "Turn curiosity into a committed but gentle sense of movement.",
            "Make the transition feel like crossing into wonder, not danger.",
        ),
        "b_story": (
            (
                f"The bond with {helper_name} deepens, giving the story a relational thread "
                "that will carry the emotional repair."
            ),
            "Anchor the plot in comfort, trust, and connection.",
            "Use the relationship to explain feelings aloud whenever tension rises.",
        ),
        "fun_and_games": (
            (
                f"{protagonist_name} explores the promise of the premise through small "
                f"discoveries, soft obstacles, and {motif}-lit delights."
            ),
            "Deliver wonder, play, and bedtime-safe novelty.",
            "Prefer cozy surprises and satisfying patterns over escalating risk.",
        ),
        "midpoint": (
            (
                "A luminous breakthrough makes the mission feel real, but it also reveals the "
                f"deeper feeling that still needs repair before {emotional_goal}."
            ),
            "Create a memorable lift with a touch of tender seriousness.",
            (
                "Let the midpoint feel awe-filled and emotionally clarifying, never sharp or "
                "overwhelming."
            ),
        ),
        "bad_guys_close_in": (
            (
                "Old worries, fading confidence, or the night's ticking softness start "
                "pressing closer as the journey home grows more delicate."
            ),
            "Increase pressure without turning the story harsh.",
            "Translate pressure into tiredness, doubt, or misread signals instead of threats.",
        ),
        "all_is_lost": (
            (
                f"{protagonist_name} briefly believes they may not restore the night's calm "
                f"after all, especially when the {motif} seems to dim."
            ),
            "Allow one low ebb so the comfort to come feels earned.",
            "Keep the loss moment brief, specific, and visibly survivable with support nearby.",
        ),
        "dark_night_of_the_soul": (
            (
                f"In the quiet after the setback, {protagonist_name} names the true feeling "
                "underneath the journey and understands what kindness is still needed."
            ),
            "Turn sadness into reflection and emotional honesty.",
            "Use stillness, not despair, so the scene feels hushed and comforting.",
        ),
        "break_into_three": (
            (
                f"{protagonist_name} and {helper_name} combine what they have learned into one "
                "final, gentler plan."
            ),
            "Restore confidence through insight and togetherness.",
            "Make the plan feel simple, warm, and guided by care rather than force.",
        ),
        "finale": (
            (
                "The story resolves the outer problem through patient action and shared care, "
                f"bringing the world back toward {emotional_goal}."
            ),
            "Deliver release, competence, and emotional repair.",
            "Let the climax peak in reassurance, reunion, and a visibly safe landing.",
        ),
        "final_image": (
            (
                f"{protagonist_name} returns to rest in {setting}, now changed by the night's "
                "lesson and surrounded by a calmer version of the opening image."
            ),
            "Leave the listener soothed, complete, and ready for sleep.",
            "Echo the opening with added softness so the ending feels tucked in.",
        ),
    }
    summary, emotional_intent, bedtime_softening_note = templates[key]

    if existing is not None and is_refinement:
        summary = (
            f"{existing.summary} This revision keeps the core beat but nudges it toward "
            f"{guidance_text or 'the requested change'}."
        )
        emotional_intent = existing.emotional_intent
        bedtime_softening_note = existing.bedtime_softening_note

    if guidance_text is not None and (key in focus_beats or label.lower() in focus_beats):
        summary = f"{summary} Focus this beat on: {guidance_text}."
        bedtime_softening_note = (
            f"{bedtime_softening_note} Apply the requested adjustment without losing the "
            "overall calm trajectory."
        )

    if bedtime_goal is not None and key in {"finale", "final_image"}:
        bedtime_softening_note = (
            f"{bedtime_softening_note} Land this beat in service of the bedtime goal: "
            f"{bedtime_goal}."
        )

    return GeneratedBeatSheetBeat(
        key=key,
        label=label,
        summary=summary,
        emotional_intent=emotional_intent,
        bedtime_softening_note=bedtime_softening_note,
    )


def _read_protagonist_name(character_sheet: ExistingCharacterSheetContext) -> str:
    protagonist = character_sheet.protagonist
    if protagonist is not None and protagonist.name:
        return protagonist.name
    if character_sheet.protagonist_name is not None:
        return character_sheet.protagonist_name
    return "The bedtime hero"


def _read_helper_name(character_sheet: ExistingCharacterSheetContext) -> str:
    if character_sheet.supporting_cast:
        first_support = character_sheet.supporting_cast[0]
        if first_support.name:
            return first_support.name
    protagonist_name = _read_protagonist_name(character_sheet)
    return f"{protagonist_name}'s trusted helper"


def _read_lead_dynamic(character_sheet: ExistingCharacterSheetContext) -> str:
    protagonist = character_sheet.protagonist
    if protagonist is None:
        return "the lead character's emotional lane"

    pieces = [
        protagonist.role,
        protagonist.goal,
        protagonist.flaw,
    ]
    normalized = [piece for piece in pieces if piece]
    if normalized:
        return ", ".join(normalized[:3])
    return "the lead character's emotional lane"


def _read_setting(context: BeatSheetGenerationPromptContext) -> str:
    return (
        context.normalized_preferences.setting
        or context.story_idea
        or context.normalized_summary
        or "a calm nighttime landscape"
    )


def _read_emotional_goal(context: BeatSheetGenerationPromptContext) -> str:
    return (
        context.bedtime_goal
        or context.normalized_preferences.emotional_goal
        or context.desired_themes
        or "a safe, sleepy return home"
    )


def _read_motifs(context: BeatSheetGenerationPromptContext) -> list[str]:
    motifs = [
        normalize_optional_beat_text(motif)
        for motif in context.normalized_preferences.candidate_motifs
    ]
    normalized = [motif for motif in motifs if motif is not None]
    if normalized:
        return normalized[:4]

    text = " ".join(
        filter(
            None,
            [
                context.key_images,
                context.selected_pitch.title,
                context.selected_pitch.hook,
                context.selected_character_sheet.summary,
            ],
        )
    )
    tokens = [
        token
        for token in re.findall(r"[A-Za-z][A-Za-z'-]{2,}", text)
        if token.lower() not in {"and", "the", "with", "for", "into", "before"}
    ]
    if tokens:
        return [_title_case_phrase(token) for token in tokens[:4]]

    return ["Moonlight", "Lanterns", "Soft Water", "Sleepy Trail"]


def _title_case_phrase(value: str) -> str:
    words = [word for word in re.split(r"[\s_-]+", value.strip()) if word]
    if not words:
        return "Moonlight"
    return " ".join(word.capitalize() for word in words[:3])


def _build_validation_failure_reason(evaluation: BeatSheetEvaluation) -> str:
    failed = [criterion.name for criterion in evaluation.criteria if not criterion.passed]
    return "beat sheet validation failed: " + ", ".join(failed)
