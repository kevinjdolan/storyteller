from __future__ import annotations

from app.ai.brief_normalization import BriefNormalizationTransportError
from app.models import (
    BriefNormalizationInvocation,
    BriefNormalizationInvocationResult,
    BriefNormalizationStructuredOutput,
    NormalizedBriefPreferences,
)
from app.services.brief_normalization import (
    BriefNormalizationService,
    apply_brief_normalization_overrides,
    build_brief_model_output,
    build_brief_normalization_result_from_existing,
)


class StubBriefNormalizationAdapter:
    def __init__(self) -> None:
        self.model_id = "gemini-3.1-flash-lite"

    def normalize(
        self,
        invocation: BriefNormalizationInvocation,
    ) -> BriefNormalizationInvocationResult:
        return BriefNormalizationInvocationResult(
            invocation=invocation,
            structured_output=BriefNormalizationStructuredOutput(
                normalized_summary=(
                    "A harbor bedtime quest where each lantern return settles the night."
                ),
                normalized_preferences=NormalizedBriefPreferences(
                    protagonist_type="A child and an otter guardian",
                    setting="a moonlit harbor",
                    emotional_goal="a calm return home",
                    constraint_notes=["End with the harbor settled and safe."],
                    bedtime_safety_concerns=[
                        "Keep every surprise quickly reassuring."
                    ],
                    candidate_motifs=["floating lanterns", "moonlit water"],
                ),
            ),
            raw_response={"stub": True},
        )

    def close(self) -> None:
        return None


class FailingBriefNormalizationAdapter:
    model_id = "gemini-3.1-flash-lite"

    def normalize(
        self,
        invocation: BriefNormalizationInvocation,
    ) -> BriefNormalizationInvocationResult:
        raise BriefNormalizationTransportError("simulated Gemini outage")

    def close(self) -> None:
        return None


def test_eval_structured_extraction_happy_path_uses_adapter_output() -> None:
    service = BriefNormalizationService(adapter=StubBriefNormalizationAdapter())

    result = service.normalize_brief(
        raw_brief=(
            "A child and an otter guardian drift after runaway lanterns to "
            "bring each light home before the harbor sleeps."
        ),
        genre_label="Quest Fantasy",
        tone_label="Hushed Wonder",
        desired_themes="Gentle courage, belonging, and a calm return home.",
        key_images="Floating lanterns, otter paws, and quiet docks.",
        audience_notes="Keep it cozy for a sensitive five-year-old.",
        must_have_elements="End with the harbor settled and the child tucked in safely.",
    )

    assert result.source == "gemini"
    assert result.normalized_preferences.protagonist_type == "A child and an otter guardian"
    assert result.normalized_preferences.setting == "a moonlit harbor"
    assert result.normalized_preferences.candidate_motifs == [
        "floating lanterns",
        "moonlit water",
    ]


def test_eval_fallback_resilience_uses_heuristics_when_adapter_fails() -> None:
    service = BriefNormalizationService(adapter=FailingBriefNormalizationAdapter())

    result = service.normalize_brief(
        raw_brief=(
            "A child and an otter guardian drift after runaway lanterns to "
            "bring each light home before the harbor sleeps."
        ),
        desired_themes="Gentle courage, belonging, and a calm return home.",
        key_images="Floating lanterns, otter paws, and quiet docks.",
        audience_notes="Keep it cozy for a sensitive five-year-old.",
        must_have_elements="End with the harbor settled and the child tucked in safely.",
    )

    assert result.source == "heuristic"
    assert result.model_id == "gemini-3.1-flash-lite"
    assert result.prompt_version == "brief_normalizer.v1"
    assert result.normalized_summary is not None
    assert result.normalized_preferences.protagonist_type == "A child and an otter guardian"
    assert any(
        motif.lower() == "floating lanterns"
        for motif in result.normalized_preferences.candidate_motifs
    )
    assert result.raw_response is not None
    assert result.raw_response["fallback_reason"] == "simulated Gemini outage"


def test_eval_user_override_merging_keeps_manual_corrections() -> None:
    base_result = BriefNormalizationService(
        adapter=StubBriefNormalizationAdapter()
    ).normalize_brief(
        raw_brief=(
            "A child and an otter guardian drift after runaway lanterns to "
            "bring each light home before the harbor sleeps."
        ),
    )

    overridden = apply_brief_normalization_overrides(
        base_result,
        raw_brief=(
            "A child and an otter guardian drift after runaway lanterns to "
            "bring each light home before the harbor sleeps."
        ),
        normalized_summary="A lantern-lit harbor story with a softer, explicitly restful ending.",
        normalized_summary_provided=True,
        normalized_preferences=NormalizedBriefPreferences(
            protagonist_type="A child and an otter guardian",
            setting="a lantern-washed harbor",
            emotional_goal="a restful reunion before sleep",
            constraint_notes=["Keep the ending tucked-in and clearly safe."],
            bedtime_safety_concerns=["Avoid any prolonged separation beat."],
            candidate_motifs=["floating lanterns", "quiet docks", "otter paws"],
        ),
        normalized_preferences_provided=True,
    )

    assert overridden.source == "gemini_with_user_overrides"
    assert (
        overridden.normalized_summary
        == "A lantern-lit harbor story with a softer, explicitly restful ending."
    )
    assert overridden.normalized_preferences.setting == "a lantern-washed harbor"
    assert overridden.normalized_preferences.bedtime_safety_concerns == [
        "Avoid any prolonged separation beat."
    ]


def test_eval_saved_metadata_round_trip_preserves_provider_context() -> None:
    saved = build_brief_normalization_result_from_existing(
        normalized_summary="A harbor bedtime quest where each lantern return settles the night.",
        normalized_preferences={
            "protagonist_type": "A child and an otter guardian",
            "setting": "a moonlit harbor",
            "emotional_goal": "a calm return home",
            "constraint_notes": ["End with the harbor settled and safe."],
            "bedtime_safety_concerns": ["Keep every surprise quickly reassuring."],
            "candidate_motifs": ["floating lanterns", "moonlit water"],
        },
        model_output={
            "schema_version": 1,
            "normalization_source": "gemini",
            "model_id": "gemini-3.1-flash-lite",
            "prompt_version": "brief_normalizer.v1",
            "raw_response": {"stub": True},
        },
    )

    model_output = build_brief_model_output(saved)

    assert saved.source == "gemini"
    assert saved.model_id == "gemini-3.1-flash-lite"
    assert model_output["normalization_source"] == "gemini"
    assert model_output["prompt_version"] == "brief_normalizer.v1"
