from __future__ import annotations

from app.ai.pitch_generation import PitchGenerationTransportError
from app.models import (
    ExistingSelectedPitchContext,
    GeneratedPitchCandidate,
    PitchGenerationInvocation,
    PitchGenerationInvocationResult,
    PitchGenerationStructuredOutput,
)
from app.services.pitch_generation import PitchGenerationService, build_pitch_model_output


class StubPitchGenerationAdapter:
    def __init__(self) -> None:
        self.model_id = "gemini-3.1-pro"

    def generate(
        self,
        invocation: PitchGenerationInvocation,
    ) -> PitchGenerationInvocationResult:
        return PitchGenerationInvocationResult(
            invocation=invocation,
            structured_output=PitchGenerationStructuredOutput(
                pitches=[
                    GeneratedPitchCandidate(
                        title="The Juniper Lake Promise",
                        hook=(
                            "A child and an otter guardian carry drifting lanterns across the "
                            "harbor so every light can find its calm way home."
                        ),
                        central_conflict=(
                            "They must return each lantern before one anxious pause stretches "
                            "the bedtime journey into a longer night."
                        ),
                        why_it_fits=(
                            "It fits Quest Fantasy and Hushed Wonder with soft movement, "
                            "luminous imagery, and a clearly restful reunion."
                        ),
                    ),
                    GeneratedPitchCandidate(
                        title="The Last Lantern Question",
                        hook=(
                            "When one lantern stays awake after the harbor quiets, the child "
                            "follows it to learn what the night still needs."
                        ),
                        central_conflict=(
                            "The mystery must be solved before everyone can settle, but every "
                            "discovery has to remain gentle and reassuring."
                        ),
                        why_it_fits=(
                            "It fits the brief by turning the harbor imagery into a calm "
                            "bedtime mystery with fast emotional repair."
                        ),
                    ),
                    GeneratedPitchCandidate(
                        title="Moonpost Harbor Map",
                        hook=(
                            "A hidden path of lights appears across the docks, leading the "
                            "child and otter toward the night's unfinished kindness."
                        ),
                        central_conflict=(
                            "Each stop asks them to choose patience and care before the final "
                            "route home can become real."
                        ),
                        why_it_fits=(
                            "It fits the selected lane by keeping wonder active while the "
                            "stakes stay soft and bedtime-safe."
                        ),
                    ),
                ]
            ),
            raw_response={"stub": True},
        )

    def close(self) -> None:
        return None


class FailingPitchGenerationAdapter:
    model_id = "gemini-3.1-pro"

    def generate(
        self,
        invocation: PitchGenerationInvocation,
    ) -> PitchGenerationInvocationResult:
        raise PitchGenerationTransportError("simulated Gemini outage")

    def close(self) -> None:
        return None


class TrivialRewritePitchGenerationAdapter:
    model_id = "gemini-3.1-pro"

    def generate(
        self,
        invocation: PitchGenerationInvocation,
    ) -> PitchGenerationInvocationResult:
        repeated = GeneratedPitchCandidate(
            title="Lantern Option",
            hook="A child follows a lantern through the harbor before bed.",
            central_conflict=(
                "The child must stay calm while helping the harbor settle for bedtime."
            ),
            why_it_fits=("It fits the selected lane by staying gentle and clearly bedtime-safe."),
        )
        return PitchGenerationInvocationResult(
            invocation=invocation,
            structured_output=PitchGenerationStructuredOutput(
                pitches=[repeated, repeated, repeated]
            ),
            raw_response={"stub": "trivial"},
        )

    def close(self) -> None:
        return None


def test_eval_structured_pitch_generation_happy_path_uses_adapter_output() -> None:
    service = PitchGenerationService(adapter=StubPitchGenerationAdapter())

    result = service.generate_pitches(
        candidate_count=3,
        raw_brief=(
            "A child follows floating lanterns across a harbor and helps a shy otter guardian "
            "bring each light home before bedtime."
        ),
        genre_label="Quest Fantasy",
        tone_label="Hushed Wonder",
        desired_themes="belonging, gentle courage, and a calm reunion",
        key_images="floating lanterns, moonlit docks, otter paws",
    )

    assert result.source == "gemini"
    assert [pitch.title for pitch in result.pitches] == [
        "The Juniper Lake Promise",
        "The Last Lantern Question",
        "Moonpost Harbor Map",
    ]
    assert result.evaluation.passed is True
    assert {criterion.name: criterion.passed for criterion in result.evaluation.criteria} == {
        "candidate_count_matches_request": True,
        "all_required_fields_present": True,
        "titles_are_distinct": True,
        "hooks_are_distinct": True,
        "central_conflicts_are_descriptive": True,
        "why_it_fits_notes_are_grounded": True,
    }


def test_eval_fallback_resilience_uses_heuristics_when_adapter_fails() -> None:
    service = PitchGenerationService(adapter=FailingPitchGenerationAdapter())

    result = service.generate_pitches(
        candidate_count=4,
        raw_brief=(
            "A child follows floating lanterns across a harbor and helps a shy otter guardian "
            "bring each light home before bedtime."
        ),
        genre_label="Quest Fantasy",
        tone_label="Hushed Wonder",
        desired_themes="belonging, gentle courage, and a calm reunion",
        key_images="floating lanterns, moonlit docks, otter paws",
    )

    assert result.source == "heuristic"
    assert result.model_id == "gemini-3.1-pro"
    assert result.prompt_version == "pitch_generation.v3"
    assert len(result.pitches) == 4
    assert result.evaluation.passed is True
    assert result.raw_response is not None
    assert result.raw_response["fallback_reason"] == "simulated Gemini outage"


def test_eval_validation_guardrail_falls_back_when_adapter_returns_trivial_rewrites() -> None:
    service = PitchGenerationService(adapter=TrivialRewritePitchGenerationAdapter())

    result = service.generate_pitches(
        candidate_count=3,
        raw_brief="A child follows lanterns through a harbor before bed.",
        genre_label="Quest Fantasy",
        tone_label="Hushed Wonder",
    )

    assert result.source == "heuristic"
    assert result.model_id == "gemini-3.1-pro"
    assert result.prompt_version == "pitch_generation.v3"
    assert result.raw_response is not None
    assert "titles_are_distinct" in result.raw_response["fallback_reason"]
    assert "hooks_are_distinct" in result.raw_response["fallback_reason"]
    assert result.evaluation.passed is True


def test_eval_pitch_model_output_preserves_provider_context_and_criteria() -> None:
    result = PitchGenerationService(adapter=StubPitchGenerationAdapter()).generate_pitches(
        candidate_count=3,
        raw_brief="A child follows lanterns through a harbor before bed.",
        genre_label="Quest Fantasy",
        tone_label="Hushed Wonder",
    )

    model_output = build_pitch_model_output(result)

    assert model_output["generation_source"] == "gemini"
    assert model_output["model_id"] == "gemini-3.1-pro"
    assert model_output["prompt_version"] == "pitch_generation.v3"
    assert model_output["evaluation"]["passed"] is True


def test_eval_refinement_fallback_keeps_the_source_pitch_and_guidance_visible() -> None:
    result = PitchGenerationService(adapter=FailingPitchGenerationAdapter()).generate_pitches(
        candidate_count=1,
        generation_goal="refinement",
        raw_brief="A child follows lanterns through a harbor before bed.",
        genre_label="Quest Fantasy",
        tone_label="Hushed Wonder",
        guidance="Make it about siblings who help each other settle down.",
        selected_pitch=ExistingSelectedPitchContext(
            title="The Juniper Lake Promise",
            hook="A child and an otter guardian carry drifting lanterns across the harbor.",
            central_conflict="They must return each lantern before the bedtime calm slips away.",
            why_it_fits="It keeps the harbor imagery gentle and luminous.",
        ),
    )

    assert result.source == "heuristic"
    assert len(result.pitches) == 1
    assert result.pitches[0].title.startswith("Juniper Lake Promise:")
    assert "Make it about siblings" in result.pitches[0].hook
    assert "The Juniper Lake Promise" in result.pitches[0].why_it_fits
