from __future__ import annotations

import re
from typing import Any

from app.ai import CharacterGenerationAdapter, build_character_generation_invocation
from app.models import (
    CharacterBatchEvaluation,
    CharacterBatchEvaluationCriterion,
    CharacterGenerationPromptContext,
    CharacterGenerationResult,
    ExistingCharacterSheetContext,
    ExistingSelectedPitchContext,
    GeneratedCharacterProfile,
    GeneratedCharacterSheetCandidate,
    NormalizedBriefPreferences,
    normalize_optional_character_text,
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
_CHARACTER_ARCHETYPE_LIBRARY = (
    {
        "title_suffix": "Keeper",
        "protagonist_role": "sleepy lantern-keeper in training",
        "goal": "guide the last glowing errands home before the harbor can rest",
        "flaw": "tries to solve every worry alone before asking for help",
        "comfort_trait": "counts steady lights until their breathing slows down",
        "support_roles": (
            "patient otter guardian who models calm teamwork",
            "drowsy heron courier who notices the night's quiet clues",
        ),
        "story_function": (
            "This cast turns the pitch into a gentle teamwork story where care and rhythm carry "
            "the bedtime momentum."
        ),
    },
    {
        "title_suffix": "Listener",
        "protagonist_role": "quiet listener for the sleeping shoreline",
        "goal": "understand what the night still needs so everyone can settle",
        "flaw": "hesitates to speak when a worried feeling first appears",
        "comfort_trait": "matches footsteps to the hush of water or leaves",
        "support_roles": (
            "older sibling who translates worry into practical kindness",
            "small moonlit animal friend who keeps discoveries playful instead of tense",
        ),
        "story_function": (
            "This cast makes the pitch feel emotionally observant, with reassurance arriving "
            "through conversation and noticing."
        ),
    },
    {
        "title_suffix": "Guide",
        "protagonist_role": "gentle route-maker for sleepy nighttime travelers",
        "goal": "lead one lingering friend or object back toward a safe ending",
        "flaw": "overplans each step and worries when the route changes",
        "comfort_trait": "returns to familiar rituals whenever the story needs grounding",
        "support_roles": (
            "warmhearted mentor who reframes obstacles as small invitations",
            "sleepy companion who turns each stop into a calmer scene",
        ),
        "story_function": (
            "This cast supports a quest structure with steady movement, small repairs, and a "
            "very readable path home."
        ),
    },
    {
        "title_suffix": "Singer",
        "protagonist_role": "soft-voiced helper who notices the rhythm beneath the night",
        "goal": "follow a repeating nighttime pattern until a worried friend can relax",
        "flaw": "doubts whether their quiet style is enough to lead",
        "comfort_trait": "hums or taps a steady pattern that calms other characters",
        "support_roles": (
            "playful sibling who gives courage without making the story loud",
            "tiny watchful creature who turns visual motifs into reassuring signals",
        ),
        "story_function": (
            "This cast leans into sensory calm and emotional repair, making the pitch feel "
            "lullaby-like without losing forward motion."
        ),
    },
)
_PROTAGONIST_NAMES = ("Mira", "Pip", "Junie", "Tavi", "Nora", "Sage")
_SUPPORTING_NAMES = (
    ("Otis", "Lark"),
    ("Rowan", "Pebble"),
    ("Ember", "Bramble"),
    ("Tala", "Moss"),
    ("Ivo", "Drift"),
    ("Poppy", "Reed"),
)


class CharacterGenerationService:
    def __init__(
        self,
        *,
        adapter: CharacterGenerationAdapter | None = None,
    ) -> None:
        self._adapter = adapter

    def generate_character_sheets(
        self,
        *,
        candidate_count: int,
        generation_goal: str = "alternatives",
        bedtime_guideline_preset_key: str = DEFAULT_BEDTIME_GUIDELINE_PRESET_KEY,
        selected_pitch: ExistingSelectedPitchContext,
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
        change_summary: str | None = None,
        focus_character_names: list[str] | None = None,
        existing_character_sheet: ExistingCharacterSheetContext | None = None,
    ) -> CharacterGenerationResult:
        context = CharacterGenerationPromptContext(
            candidate_count=candidate_count,
            generation_goal=generation_goal,
            bedtime_guideline_preset_key=bedtime_guideline_preset_key,
            guidance=guidance,
            change_summary=change_summary,
            focus_character_names=focus_character_names or [],
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
            existing_character_sheet=existing_character_sheet,
        )

        if self._adapter is not None:
            try:
                invocation = build_character_generation_invocation(
                    context,
                    model_id=self._adapter.model_id,
                )
                result = self._adapter.generate(invocation)
                evaluation = evaluate_character_sheet_batch(
                    result.structured_output.character_sheets,
                    requested_count=candidate_count,
                )
                if evaluation.passed:
                    return CharacterGenerationResult(
                        source="gemini",
                        model_id=result.invocation.model_id,
                        prompt_version=result.invocation.prompt_version,
                        character_sheets=result.structured_output.character_sheets,
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


def evaluate_character_sheet_batch(
    character_sheets: list[GeneratedCharacterSheetCandidate],
    *,
    requested_count: int,
) -> CharacterBatchEvaluation:
    normalized_titles = {_normalize_compare(candidate.title) for candidate in character_sheets}
    normalized_protagonist_names = {
        _normalize_compare(candidate.protagonist.name) for candidate in character_sheets
    }
    filled_fields = sum(
        1
        for candidate in character_sheets
        if all(
            normalize_optional_character_text(value) is not None
            for value in (
                candidate.title,
                candidate.summary,
                candidate.story_function,
                candidate.bedtime_safety_notes,
                candidate.protagonist.name,
                candidate.protagonist.role,
                candidate.protagonist.goal,
                candidate.protagonist.flaw,
                candidate.protagonist.comfort_trait,
                candidate.protagonist.bedtime_safety_notes,
            )
        )
    )
    sheets_with_support = sum(
        1 for candidate in character_sheets if len(candidate.supporting_cast) >= 1
    )
    grounded_relationships = sum(
        1
        for candidate in character_sheets
        if len(candidate.protagonist.relationships) >= 1
        and any(len(support.relationships) >= 1 for support in candidate.supporting_cast)
    )
    grounded_safety_notes = sum(
        1
        for candidate in character_sheets
        if len(candidate.bedtime_safety_notes.split()) >= 6
        and len(candidate.protagonist.bedtime_safety_notes.split()) >= 6
    )

    criteria = [
        CharacterBatchEvaluationCriterion(
            name="candidate_count_matches_request",
            passed=len(character_sheets) == requested_count,
            measured_value=len(character_sheets),
            detail=f"Requested {requested_count} character-sheet candidates.",
        ),
        CharacterBatchEvaluationCriterion(
            name="all_required_fields_present",
            passed=filled_fields == len(character_sheets),
            measured_value=filled_fields,
            detail=(
                "Each candidate must include summary, story function, bedtime notes, and a "
                "fully described protagonist."
            ),
        ),
        CharacterBatchEvaluationCriterion(
            name="titles_are_distinct",
            passed=len(normalized_titles) == len(character_sheets),
            measured_value=len(normalized_titles),
            detail="Distinct titles make the character concepts easier to compare.",
        ),
        CharacterBatchEvaluationCriterion(
            name="protagonist_names_are_distinct",
            passed=len(normalized_protagonist_names) == len(character_sheets),
            measured_value=len(normalized_protagonist_names),
            detail="Distinct lead-character names reduce trivial rewrites.",
        ),
        CharacterBatchEvaluationCriterion(
            name="supporting_cast_present",
            passed=sheets_with_support == len(character_sheets),
            measured_value=sheets_with_support,
            detail="Each sheet should include supporting cast details.",
        ),
        CharacterBatchEvaluationCriterion(
            name="relationships_are_grounded",
            passed=grounded_relationships == len(character_sheets),
            measured_value=grounded_relationships,
            detail="Relationships should be concrete enough to guide later beats.",
        ),
        CharacterBatchEvaluationCriterion(
            name="bedtime_safety_notes_are_grounded",
            passed=grounded_safety_notes == len(character_sheets),
            measured_value=grounded_safety_notes,
            detail="Bedtime-safety notes should explicitly explain the calming posture.",
        ),
    ]

    return CharacterBatchEvaluation(
        passed=all(criterion.passed for criterion in criteria),
        criteria=criteria,
    )


def build_character_model_output(result: CharacterGenerationResult) -> dict[str, Any]:
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
    context: CharacterGenerationPromptContext,
    *,
    fallback_reason: str | None = None,
    adapter_raw_response: dict[str, Any] | list[Any] | str | None = None,
) -> CharacterGenerationResult:
    character_sheets = _build_heuristic_character_sheets(context)
    evaluation = evaluate_character_sheet_batch(
        character_sheets,
        requested_count=context.candidate_count,
    )
    raw_response: dict[str, Any] = {
        "heuristic": True,
    }
    if fallback_reason is not None:
        raw_response["fallback_reason"] = fallback_reason
    if adapter_raw_response is not None:
        raw_response["adapter_raw_response"] = adapter_raw_response

    return CharacterGenerationResult(
        source="heuristic",
        character_sheets=character_sheets,
        evaluation=evaluation,
        raw_response=raw_response,
    )


def _build_heuristic_character_sheets(
    context: CharacterGenerationPromptContext,
) -> list[GeneratedCharacterSheetCandidate]:
    if context.generation_goal == "refinement":
        return [_build_refined_heuristic_character_sheet(context)]

    motifs = _read_motifs(context)
    setting = _read_setting(context)
    emotional_goal = _read_emotional_goal(context)
    support_name_pairs = list(_SUPPORTING_NAMES)
    generated: list[GeneratedCharacterSheetCandidate] = []

    for index in range(context.candidate_count):
        lens = _CHARACTER_ARCHETYPE_LIBRARY[index % len(_CHARACTER_ARCHETYPE_LIBRARY)]
        protagonist_name = _PROTAGONIST_NAMES[index % len(_PROTAGONIST_NAMES)]
        support_names = support_name_pairs[index % len(support_name_pairs)]
        motif = motifs[index % len(motifs)]
        secondary_motif = motifs[(index + 1) % len(motifs)]
        title = f"{_format_title_token(motif)} {lens['title_suffix']} Cast"
        protagonist = GeneratedCharacterProfile(
            name=protagonist_name,
            role=str(lens["protagonist_role"]),
            goal=_inject_context_into_sentence(str(lens["goal"]), setting=setting, motif=motif),
            flaw=str(lens["flaw"]),
            comfort_trait=str(lens["comfort_trait"]),
            bedtime_safety_notes=(
                f"{protagonist_name} never faces the night's pressure alone; helpers stay close "
                "and every worry resolves into a calmer next step."
            ),
            relationships=[
                f"Trusts {support_names[0]} to steady the plan when emotions spike.",
                f"Learns to accept playful guidance from {support_names[1]}.",
            ],
            visual_anchors=[
                f"{motif} glow on their sleeves",
                f"a pocket token tied to {secondary_motif}",
                f"quiet movement through {setting}",
            ],
        )
        supporting_cast = [
            GeneratedCharacterProfile(
                name=support_names[0],
                role=str(lens["support_roles"][0]),
                goal=(
                    f"Help {protagonist_name} move toward {emotional_goal} without letting the "
                    "journey feel rushed."
                ),
                flaw="can over-explain instead of letting the lead character discover the answer",
                comfort_trait="slows scenes down with a grounding reminder or ritual",
                bedtime_safety_notes=(
                    "Keeps each obstacle small, named, and emotionally readable before the story "
                    "moves on."
                ),
                relationships=[
                    f"Acts as {protagonist_name}'s calm sounding board.",
                    f"Teams up with {support_names[1]} to make discoveries feel safe.",
                ],
                visual_anchors=[
                    f"a satchel of {motif}",
                    f"soft reflections of {secondary_motif}",
                ],
            ),
            GeneratedCharacterProfile(
                name=support_names[1],
                role=str(lens["support_roles"][1]),
                goal=(
                    f"Keep the journey playful enough that {protagonist_name} can stay curious "
                    "instead of overwhelmed."
                ),
                flaw="gets distracted by charming details before refocusing",
                comfort_trait="finds one reassuring image in every new place",
                bedtime_safety_notes=(
                    "Turns surprises into gentle, quickly understandable moments instead of "
                    "letting them escalate."
                ),
                relationships=[
                    f"Reminds {protagonist_name} how to notice wonder again.",
                    f"Looks to {support_names[0]} for reassurance when the mood dips.",
                ],
                visual_anchors=[
                    f"a trail of {secondary_motif}",
                    f"sleepy touches of {motif}",
                ],
            ),
        ]
        summary = (
            f"{protagonist_name} leads {context.selected_pitch.title} through {setting}, with "
            f"{support_names[0]} and {support_names[1]} shaping the story into a bedtime-safe "
            "repair arc."
        )
        generated.append(
            GeneratedCharacterSheetCandidate(
                title=title,
                summary=summary,
                story_function=(
                    f"{lens['story_function']} It fits {context.selected_pitch.title} by keeping "
                    f"the cast focused on {emotional_goal}."
                ),
                bedtime_safety_notes=(
                    "The cast keeps tension gentle through visible helpers, named feelings, and "
                    "a clearly restorative ending."
                ),
                visual_motifs=[motif, secondary_motif, setting],
                protagonist=protagonist,
                supporting_cast=supporting_cast,
            )
        )

    return generated


def _build_refined_heuristic_character_sheet(
    context: CharacterGenerationPromptContext,
) -> GeneratedCharacterSheetCandidate:
    existing = context.existing_character_sheet
    setting = _read_setting(context)
    motifs = _read_motifs(context)
    motif = motifs[0]
    guidance = context.guidance or "refine the emotional balance"
    protagonist_name = (
        existing.protagonist_name
        if existing is not None and existing.protagonist_name is not None
        else _PROTAGONIST_NAMES[0]
    )
    base_title = (
        existing.title
        if existing is not None and existing.title is not None
        else "Refined Cast"
    )
    focus_names = (
        ", ".join(context.focus_character_names)
        if context.focus_character_names
        else None
    )
    support_names = _SUPPORTING_NAMES[0]

    protagonist = GeneratedCharacterProfile(
        name=protagonist_name,
        role=(
            existing.protagonist.role
            if existing is not None and existing.protagonist is not None
            else "bedtime-story lead with a calmer revised dynamic"
        ),
        goal=(
            existing.protagonist.goal
            if existing is not None and existing.protagonist is not None
            else f"carry {context.selected_pitch.title} toward a more restful landing"
        ),
        flaw=(
            existing.protagonist.flaw
            if existing is not None and existing.protagonist is not None
            else "holds tension inside until someone invites them to share it"
        ),
        comfort_trait=(
            existing.protagonist.comfort_trait
            if existing is not None and existing.protagonist is not None
            else "returns to a familiar rhythm whenever the story needs grounding"
        ),
        bedtime_safety_notes=(
            f"The revision keeps {protagonist_name}'s worries readable and quickly supported by "
            "the rest of the cast."
        ),
        relationships=[
            f"Leans on {support_names[0]} when the revised scene needs steadier pacing.",
            f"Feels more openly understood by {support_names[1]} after the refinement.",
        ],
        visual_anchors=[
            f"{motif} held close to the chest",
            f"quiet movement through {setting}",
        ],
    )
    supporting_cast = [
        GeneratedCharacterProfile(
            name=support_names[0],
            role="revised steadying companion",
            goal=f"help {protagonist_name} apply the requested change without losing warmth",
            flaw="wants to protect everyone before listening fully",
            comfort_trait="slows the pace with practical kindness",
            bedtime_safety_notes=(
                "Gives the refinement emotional guardrails so the new version stays safe for "
                "bedtime."
            ),
            relationships=[f"Works in closer sync with {protagonist_name} after the revision."],
            visual_anchors=[f"a pocket of {motif}", f"soft details from {setting}"],
        ),
        GeneratedCharacterProfile(
            name=support_names[1],
            role="revised supporting mirror",
            goal=(
                "highlight the refined emotional lane while keeping "
                f"{context.selected_pitch.title} recognizable"
            ),
            flaw="rushes toward reassurance before hearing the full feeling",
            comfort_trait="notices one calming image in every transition",
            bedtime_safety_notes=(
                "Keeps surprises gentle and translates them into cozy, visual reassurance."
            ),
            relationships=[f"Reflects {protagonist_name}'s growth in a lighter key."],
            visual_anchors=[f"a thread of {motif}", f"sleepy cues from {setting}"],
        ),
    ]

    summary_parts = [
        f"This revision keeps {base_title} recognizable while applying: {guidance}.",
    ]
    if focus_names is not None:
        summary_parts.append(f"Focus characters: {focus_names}.")

    return GeneratedCharacterSheetCandidate(
        title=f"{base_title}: Revised",
        summary=" ".join(summary_parts),
        story_function=(
            "The refined cast preserves the existing bedtime lane for "
            f"{context.selected_pitch.title} while tightening the requested emotional "
            "or relationship change."
        ),
        bedtime_safety_notes=(
            "The revision keeps all emotional pressure buffered by companionship, clear naming, "
            "and a visibly safe return to calm."
        ),
        visual_motifs=motifs[:3],
        protagonist=protagonist,
        supporting_cast=supporting_cast,
    )


def _read_setting(context: CharacterGenerationPromptContext) -> str:
    return (
        context.normalized_preferences.setting
        or context.story_idea
        or context.normalized_summary
        or "a calm nighttime landscape"
    )


def _read_emotional_goal(context: CharacterGenerationPromptContext) -> str:
    return (
        context.normalized_preferences.emotional_goal
        or context.desired_themes
        or "a calm return home"
    )


def _read_motifs(context: CharacterGenerationPromptContext) -> list[str]:
    motifs = [
        normalize_optional_character_text(motif)
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
            ],
        )
    )
    tokens = [
        token
        for token in re.findall(r"[A-Za-z][A-Za-z'-]{2,}", text)
        if token.lower() not in _TITLE_STOPWORDS
    ]
    if tokens:
        return [_format_title_token(token) for token in tokens[:4]]
    return ["Lantern", "Moonlight", "Harbor", "Hush"]


def _inject_context_into_sentence(sentence: str, *, setting: str, motif: str) -> str:
    return sentence.replace("the harbor", setting).replace("glowing errands", motif)


def _format_title_token(value: str) -> str:
    normalized = normalize_optional_character_text(value) or "Lantern"
    return " ".join(part.capitalize() for part in re.split(r"[\s_-]+", normalized) if part)


def _build_validation_failure_reason(evaluation: CharacterBatchEvaluation) -> str:
    failed = [criterion.name for criterion in evaluation.criteria if not criterion.passed]
    return "character sheet validation failed: " + ", ".join(failed)


def _normalize_compare(value: str | None) -> str:
    normalized = normalize_optional_character_text(value)
    if normalized is None:
        return ""
    return re.sub(r"[^a-z0-9]+", " ", normalized.lower()).strip()
