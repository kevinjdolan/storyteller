from __future__ import annotations

from app.ai.beat_sheet_generation import BeatSheetGenerationTransportError
from app.models import (
    BeatSheetGenerationInvocation,
    BeatSheetGenerationInvocationResult,
    BeatSheetGenerationStructuredOutput,
    ExistingBeatSheetContext,
    ExistingCharacterSheetContext,
    ExistingSelectedPitchContext,
    GeneratedBeatSheetBeat,
    GeneratedBeatSheetCandidate,
    GeneratedCharacterProfile,
)
from app.services.beat_sheet_generation import (
    BeatSheetGenerationService,
    build_beat_sheet_model_output,
)


def _build_complete_stub_beat_sheet() -> GeneratedBeatSheetCandidate:
    return GeneratedBeatSheetCandidate(
        summary=(
            "Mira moves through a full Save-the-Cat harbor arc where each beat turns wonder into "
            "restful belonging."
        ),
        bedtime_notes=(
            "Pressure stays gentle, helpers stay visible, and the final landing clearly returns "
            "the story to safety and sleep."
        ),
        beats=[
            GeneratedBeatSheetBeat(
                key=key,
                label=label,
                summary=f"{label} keeps the harbor story moving in a calm, high-level way.",
                emotional_intent=f"{label} should feel reassuring and emotionally legible.",
                bedtime_softening_note=(
                    f"{label} stays bedtime-safe by keeping the tension readable and quickly "
                    "buffered by comfort."
                ),
            )
            for key, label in (
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
        ],
    )


class StubBeatSheetGenerationAdapter:
    def __init__(self) -> None:
        self.model_id = "gemini-3.1-pro"

    def generate(
        self,
        invocation: BeatSheetGenerationInvocation,
    ) -> BeatSheetGenerationInvocationResult:
        return BeatSheetGenerationInvocationResult(
            invocation=invocation,
            structured_output=BeatSheetGenerationStructuredOutput(
                beat_sheet=_build_complete_stub_beat_sheet()
            ),
            raw_response={"stub": True},
        )

    def close(self) -> None:
        return None


class FailingBeatSheetGenerationAdapter:
    model_id = "gemini-3.1-pro"

    def generate(
        self,
        invocation: BeatSheetGenerationInvocation,
    ) -> BeatSheetGenerationInvocationResult:
        raise BeatSheetGenerationTransportError("simulated Gemini outage")

    def close(self) -> None:
        return None


class IncompleteBeatSheetGenerationAdapter:
    model_id = "gemini-3.1-pro"

    def generate(
        self,
        invocation: BeatSheetGenerationInvocation,
    ) -> BeatSheetGenerationInvocationResult:
        candidate = _build_complete_stub_beat_sheet()
        candidate.beats = candidate.beats[:-2]
        return BeatSheetGenerationInvocationResult(
            invocation=invocation,
            structured_output=BeatSheetGenerationStructuredOutput(beat_sheet=candidate),
            raw_response={"stub": "incomplete"},
        )

    def close(self) -> None:
        return None


def _build_character_context() -> ExistingCharacterSheetContext:
    return ExistingCharacterSheetContext(
        title="Juniper Keeper Cast",
        summary="Mira and Otis carry the harbor story together.",
        protagonist_name="Mira",
        bedtime_safety_notes="Every worry is buffered by visible helpers.",
        protagonist=GeneratedCharacterProfile(
            name="Mira",
            role="sleepy lantern-keeper in training",
            goal="guide the last harbor lights home before everyone settles",
            flaw="tries to fix every worry alone before asking for help",
            comfort_trait="counts steady reflections until breathing slows",
            bedtime_safety_notes="Mira stays emotionally safe because helpers remain close.",
            relationships=["Trusts Otis to steady the plan."],
            visual_anchors=["lantern sleeves", "soft satchel"],
        ),
        supporting_cast=[
            GeneratedCharacterProfile(
                name="Otis",
                role="patient otter guardian",
                goal="help Mira slow the pacing whenever the night feels bigger",
                flaw="over-explains instead of letting Mira discover the answer",
                comfort_trait="grounds scenes with practical rituals",
                bedtime_safety_notes="Otis keeps each obstacle small and reassuring.",
                relationships=["Acts as Mira's calm sounding board."],
                visual_anchors=["river coat", "tidy satchel"],
            )
        ],
    )


def test_eval_structured_beat_sheet_happy_path_uses_adapter_output() -> None:
    service = BeatSheetGenerationService(adapter=StubBeatSheetGenerationAdapter())

    result = service.generate_beat_sheet(
        selected_pitch=ExistingSelectedPitchContext(
            title="The Silver Bell Buoy",
            hook="Mira follows a bell-lit clue across the harbor before bed.",
            central_conflict="She must help the harbor settle before the night stretches too long.",
            why_it_fits="It keeps wonder active while the emotional repair stays soft.",
        ),
        selected_character_sheet=_build_character_context(),
        raw_brief="A harbor child follows a silver bell and helps the docks settle before bed.",
        genre_label="Quest Fantasy",
        tone_label="Hushed Wonder",
    )

    assert result.source == "gemini"
    assert result.evaluation.passed is True
    assert {criterion.name: criterion.passed for criterion in result.evaluation.criteria} == {
        "all_required_beats_present": True,
        "beat_order_matches_framework": True,
        "summaries_are_present_for_every_beat": True,
        "emotional_intents_are_present_for_every_beat": True,
        "bedtime_softening_notes_are_present_for_every_beat": True,
        "tension_beats_include_extra_softening": True,
        "overall_summary_and_bedtime_notes_are_present": True,
    }


def test_eval_fallback_resilience_uses_heuristics_when_adapter_fails() -> None:
    service = BeatSheetGenerationService(adapter=FailingBeatSheetGenerationAdapter())

    result = service.generate_beat_sheet(
        selected_pitch=ExistingSelectedPitchContext(
            title="The Silver Bell Buoy",
            hook="Mira follows a bell-lit clue across the harbor before bed.",
        ),
        selected_character_sheet=_build_character_context(),
        raw_brief="A harbor child follows a silver bell and helps the docks settle before bed.",
        genre_label="Quest Fantasy",
        tone_label="Hushed Wonder",
        bedtime_goal="leave the child listener ready to drift off feeling tucked in",
    )

    assert result.source == "heuristic"
    assert len(result.beat_sheet.beats) == 15
    assert result.evaluation.passed is True
    assert result.raw_response is not None
    assert result.raw_response["fallback_reason"] == "simulated Gemini outage"


def test_eval_validation_guardrail_falls_back_when_adapter_misses_required_beats() -> None:
    service = BeatSheetGenerationService(adapter=IncompleteBeatSheetGenerationAdapter())

    result = service.generate_beat_sheet(
        selected_pitch=ExistingSelectedPitchContext(
            title="The Silver Bell Buoy",
            hook="Mira follows a bell-lit clue across the harbor before bed.",
        ),
        selected_character_sheet=_build_character_context(),
        raw_brief="A harbor child follows a silver bell and helps the docks settle before bed.",
        genre_label="Quest Fantasy",
        tone_label="Hushed Wonder",
    )

    assert result.source == "heuristic"
    assert result.raw_response is not None
    assert "all_required_beats_present" in result.raw_response["fallback_reason"]
    assert "beat_order_matches_framework" in result.raw_response["fallback_reason"]
    assert result.evaluation.passed is True


def test_eval_refinement_fallback_keeps_source_revision_and_guidance_visible() -> None:
    service = BeatSheetGenerationService(adapter=FailingBeatSheetGenerationAdapter())

    result = service.generate_beat_sheet(
        generation_goal="refinement",
        selected_pitch=ExistingSelectedPitchContext(
            title="The Silver Bell Buoy",
            hook="Mira follows a bell-lit clue across the harbor before bed.",
        ),
        selected_character_sheet=_build_character_context(),
        raw_brief="A harbor child follows a silver bell and helps the docks settle before bed.",
        instructions=(
            "Soften the midpoint and all-is-lost beats so they feel more awestruck than tense."
        ),
        focus_beats=["midpoint", "all_is_lost"],
        bedtime_goal="end on a very sleepy exhale",
        existing_beat_sheet=ExistingBeatSheetContext(
            revision_number=2,
            summary="Existing harbor beat sheet.",
            bedtime_notes="Keep every turn reassuring.",
            beats=_build_complete_stub_beat_sheet().beats,
        ),
    )

    assert result.source == "heuristic"
    assert result.beat_sheet.summary.startswith("Mira moves through a full Save-the-Cat arc")
    midpoint = next(beat for beat in result.beat_sheet.beats if beat.key == "midpoint")
    assert "Soften the midpoint" in midpoint.summary
    final_image = next(beat for beat in result.beat_sheet.beats if beat.key == "final_image")
    assert "very sleepy exhale" in final_image.bedtime_softening_note


def test_eval_beat_sheet_model_output_preserves_provider_context_and_criteria() -> None:
    result = BeatSheetGenerationService(
        adapter=StubBeatSheetGenerationAdapter()
    ).generate_beat_sheet(
        selected_pitch=ExistingSelectedPitchContext(
            title="The Silver Bell Buoy",
            hook="Mira follows a bell-lit clue across the harbor before bed.",
        ),
        selected_character_sheet=_build_character_context(),
        raw_brief="A harbor child follows a silver bell and helps the docks settle before bed.",
    )

    model_output = build_beat_sheet_model_output(result)

    assert model_output["generation_source"] == "gemini"
    assert model_output["model_id"] == "gemini-3.1-pro"
    assert model_output["prompt_version"] == "beat_sheet_generation.v2"
    assert model_output["evaluation"]["passed"] is True
