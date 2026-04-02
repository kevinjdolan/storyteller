from __future__ import annotations

from app.ai.character_generation import CharacterGenerationTransportError
from app.models import (
    CharacterGenerationInvocation,
    CharacterGenerationInvocationResult,
    CharacterGenerationStructuredOutput,
    ExistingCharacterSheetContext,
    ExistingSelectedPitchContext,
    GeneratedCharacterProfile,
    GeneratedCharacterSheetCandidate,
)
from app.services.character_generation import (
    CharacterGenerationService,
    build_character_model_output,
)


class StubCharacterGenerationAdapter:
    def __init__(self) -> None:
        self.model_id = "gemini-3.1-pro"

    def generate(
        self,
        invocation: CharacterGenerationInvocation,
    ) -> CharacterGenerationInvocationResult:
        return CharacterGenerationInvocationResult(
            invocation=invocation,
            structured_output=CharacterGenerationStructuredOutput(
                character_sheets=[
                    GeneratedCharacterSheetCandidate(
                        title="Juniper Keeper Cast",
                        summary=(
                            "Mira leads the harbor story with a calm helper dynamic and clear "
                            "relationship stakes."
                        ),
                        story_function=(
                            "The cast supports the selected pitch by turning the bedtime quest "
                            "into a teamwork-driven repair story."
                        ),
                        bedtime_safety_notes=(
                            "Every worry is buffered by visible helpers, named feelings, and a "
                            "clearly restorative ending."
                        ),
                        visual_motifs=["lantern glow", "moonlit docks", "otter paws"],
                        protagonist=GeneratedCharacterProfile(
                            name="Mira",
                            role="sleepy lantern-keeper in training",
                            goal="guide the last harbor lights home before everyone settles",
                            flaw="tries to fix every worry alone before asking for help",
                            comfort_trait="counts steady reflections until their breathing slows",
                            bedtime_safety_notes=(
                                "Mira stays emotionally safe because the rest of the cast keeps "
                                "close, calm support in every scene."
                            ),
                            relationships=[
                                "Trusts Otis to steady the plan when emotions spike.",
                                "Learns to accept playful guidance from Lark.",
                            ],
                            visual_anchors=[
                                "lantern glow on sleeves",
                                "moonlit satchel strap",
                            ],
                        ),
                        supporting_cast=[
                            GeneratedCharacterProfile(
                                name="Otis",
                                role="patient otter guardian",
                                goal="help Mira slow the pacing whenever the night feels bigger",
                                flaw="over-explains instead of letting Mira discover the answer",
                                comfort_trait="grounds scenes with practical rituals",
                                bedtime_safety_notes=(
                                    "Otis makes every obstacle feel small, readable, and quickly "
                                    "reassuring."
                                ),
                                relationships=[
                                    "Acts as Mira's calm sounding board.",
                                ],
                                visual_anchors=["soft river coat", "tidy satchel"],
                            )
                        ],
                    ),
                    GeneratedCharacterSheetCandidate(
                        title="Harbor Listener Cast",
                        summary=(
                            "Pip centers the same pitch around noticing, conversation, and a "
                            "gentler mystery rhythm."
                        ),
                        story_function=(
                            "The cast makes the pitch emotionally observant so later beats can "
                            "lean on dialogue and calm discovery."
                        ),
                        bedtime_safety_notes=(
                            "The mystery stays bedtime-safe because each reveal is named, "
                            "shared, and softened right away."
                        ),
                        visual_motifs=["still water", "sleepy reeds", "silver light"],
                        protagonist=GeneratedCharacterProfile(
                            name="Pip",
                            role="quiet listener for the sleeping shoreline",
                            goal="understand what the night still needs so everyone can settle",
                            flaw="hesitates to speak when a worried feeling first appears",
                            comfort_trait="matches footsteps to the hush of water",
                            bedtime_safety_notes=(
                                "Pip's worries stay readable and quickly supported by the whole "
                                "cast."
                            ),
                            relationships=[
                                "Leans on Rowan when emotions need clearer words.",
                                "Feels braver around Pebble's playful energy.",
                            ],
                            visual_anchors=[
                                "silver pockets",
                                "reed-shadow patterns",
                            ],
                        ),
                        supporting_cast=[
                            GeneratedCharacterProfile(
                                name="Rowan",
                                role="older sibling translator",
                                goal="turn worry into practical kindness whenever the mood dips",
                                flaw="tries to protect everyone before listening fully",
                                comfort_trait="restates feelings in calmer words",
                                bedtime_safety_notes=(
                                    "Rowan keeps discoveries gentle by naming them before they "
                                    "can feel overwhelming."
                                ),
                                relationships=[
                                    "Helps Pip speak the hidden worry aloud.",
                                ],
                                visual_anchors=["striped scarf", "reed basket"],
                            )
                        ],
                    ),
                ]
            ),
            raw_response={"stub": True},
        )

    def close(self) -> None:
        return None


class FailingCharacterGenerationAdapter:
    model_id = "gemini-3.1-pro"

    def generate(
        self,
        invocation: CharacterGenerationInvocation,
    ) -> CharacterGenerationInvocationResult:
        raise CharacterGenerationTransportError("simulated Gemini outage")

    def close(self) -> None:
        return None


class TrivialCharacterGenerationAdapter:
    model_id = "gemini-3.1-pro"

    def generate(
        self,
        invocation: CharacterGenerationInvocation,
    ) -> CharacterGenerationInvocationResult:
        repeated = GeneratedCharacterSheetCandidate(
            title="Lantern Cast",
            summary="A calm cast for the harbor bedtime story.",
            story_function="The cast supports the pitch with a gentle bedtime lane.",
            bedtime_safety_notes=(
                "Everything stays safe because it is calm and bedtime-friendly."
            ),
            visual_motifs=["lantern"],
            protagonist=GeneratedCharacterProfile(
                name="Mira",
                role="lead child",
                goal="bring the lanterns home",
                flaw="worries too much",
                comfort_trait="counts quietly",
                bedtime_safety_notes="Mira stays safe because helpers stay nearby always.",
                relationships=["Trusts the friend."],
                visual_anchors=["lantern coat"],
            ),
            supporting_cast=[
                GeneratedCharacterProfile(
                    name="Otis",
                    role="friend",
                    goal="help the lead",
                    flaw="gets distracted",
                    comfort_trait="uses jokes softly",
                    bedtime_safety_notes="Otis keeps each obstacle gentle and readable.",
                    relationships=["Supports Mira."],
                    visual_anchors=["otter paws"],
                )
            ],
        )
        return CharacterGenerationInvocationResult(
            invocation=invocation,
            structured_output=CharacterGenerationStructuredOutput(
                character_sheets=[repeated, repeated, repeated]
            ),
            raw_response={"stub": "trivial"},
        )

    def close(self) -> None:
        return None


def test_eval_structured_character_generation_happy_path_uses_adapter_output() -> None:
    service = CharacterGenerationService(adapter=StubCharacterGenerationAdapter())

    result = service.generate_character_sheets(
        candidate_count=2,
        selected_pitch=ExistingSelectedPitchContext(
            title="Lanterns Over Juniper Lake",
            hook="A child and an otter guardian guide the last lanterns home before bed.",
        ),
        raw_brief=(
            "A child follows floating lanterns through a harbor and helps a shy otter guardian "
            "bring each light home before bedtime."
        ),
        genre_label="Quest Fantasy",
        tone_label="Hushed Wonder",
    )

    assert result.source == "gemini"
    assert [character_sheet.title for character_sheet in result.character_sheets] == [
        "Juniper Keeper Cast",
        "Harbor Listener Cast",
    ]
    assert result.evaluation.passed is True
    assert {criterion.name: criterion.passed for criterion in result.evaluation.criteria} == {
        "candidate_count_matches_request": True,
        "all_required_fields_present": True,
        "titles_are_distinct": True,
        "protagonist_names_are_distinct": True,
        "supporting_cast_present": True,
        "relationships_are_grounded": True,
        "bedtime_safety_notes_are_grounded": True,
    }


def test_eval_fallback_resilience_uses_heuristics_when_adapter_fails() -> None:
    service = CharacterGenerationService(adapter=FailingCharacterGenerationAdapter())

    result = service.generate_character_sheets(
        candidate_count=3,
        selected_pitch=ExistingSelectedPitchContext(
            title="Lanterns Over Juniper Lake",
            hook="A child and an otter guardian guide the last lanterns home before bed.",
        ),
        raw_brief="A child follows lanterns through a harbor before bed.",
        genre_label="Quest Fantasy",
        tone_label="Hushed Wonder",
    )

    assert result.source == "heuristic"
    assert len(result.character_sheets) == 3
    assert result.evaluation.passed is True
    assert result.raw_response is not None
    assert result.raw_response["fallback_reason"] == "simulated Gemini outage"


def test_eval_validation_guardrail_falls_back_when_adapter_returns_trivial_rewrites() -> None:
    service = CharacterGenerationService(adapter=TrivialCharacterGenerationAdapter())

    result = service.generate_character_sheets(
        candidate_count=3,
        selected_pitch=ExistingSelectedPitchContext(
            title="Lanterns Over Juniper Lake",
            hook="A child follows lanterns through a harbor before bed.",
        ),
        raw_brief="A child follows lanterns through a harbor before bed.",
        genre_label="Quest Fantasy",
        tone_label="Hushed Wonder",
    )

    assert result.source == "heuristic"
    assert result.raw_response is not None
    assert "titles_are_distinct" in result.raw_response["fallback_reason"]
    assert "protagonist_names_are_distinct" in result.raw_response["fallback_reason"]
    assert result.evaluation.passed is True


def test_eval_character_model_output_preserves_provider_context_and_criteria() -> None:
    result = CharacterGenerationService(
        adapter=StubCharacterGenerationAdapter()
    ).generate_character_sheets(
        candidate_count=2,
        selected_pitch=ExistingSelectedPitchContext(
            title="Lanterns Over Juniper Lake",
            hook="A child follows lanterns through a harbor before bed.",
        ),
        raw_brief="A child follows lanterns through a harbor before bed.",
        genre_label="Quest Fantasy",
        tone_label="Hushed Wonder",
    )

    model_output = build_character_model_output(result)

    assert model_output["generation_source"] == "gemini"
    assert model_output["model_id"] == "gemini-3.1-pro"
    assert model_output["prompt_version"] == "character_generation.v2"
    assert model_output["evaluation"]["passed"] is True


def test_eval_refinement_fallback_keeps_the_source_sheet_and_guidance_visible() -> None:
    result = CharacterGenerationService(
        adapter=FailingCharacterGenerationAdapter()
    ).generate_character_sheets(
        candidate_count=1,
        generation_goal="refinement",
        selected_pitch=ExistingSelectedPitchContext(
            title="Lanterns Over Juniper Lake",
            hook="A child follows lanterns through a harbor before bed.",
        ),
        raw_brief="A child follows lanterns through a harbor before bed.",
        genre_label="Quest Fantasy",
        tone_label="Hushed Wonder",
        guidance="Make the cast about siblings who help each other settle down.",
        focus_character_names=["Mira", "Otis"],
        existing_character_sheet=ExistingCharacterSheetContext(
            title="Juniper Keeper Cast",
            summary="A harbor cast with a calm helper dynamic.",
            protagonist_name="Mira",
        ),
    )

    assert result.source == "heuristic"
    assert len(result.character_sheets) == 1
    assert result.character_sheets[0].title == "Juniper Keeper Cast: Revised"
    assert "siblings who help each other settle down" in result.character_sheets[0].summary
    assert "Lanterns Over Juniper Lake" in result.character_sheets[0].story_function
