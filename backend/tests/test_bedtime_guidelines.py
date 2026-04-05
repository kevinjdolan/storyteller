from __future__ import annotations

import pytest
from app.ai import (
    build_bedtime_guidelines_fragment,
    render_beat_sheet_generation_prompt,
    render_character_generation_prompt,
    render_pitch_generation_prompt,
)
from app.models import (
    BeatSheetGenerationPromptContext,
    CharacterGenerationPromptContext,
    ExistingCharacterSheetContext,
    ExistingSelectedPitchContext,
    GeneratedCharacterProfile,
    PitchGenerationPromptContext,
)
from app.models.bedtime_guidelines import (
    BEDTIME_PROMPT_STAGES,
    DEFAULT_BEDTIME_GUIDELINE_PRESET_KEY,
    get_bedtime_audience_preset_plan,
)


def _build_pitch_context() -> PitchGenerationPromptContext:
    return PitchGenerationPromptContext(
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


def _build_selected_pitch() -> ExistingSelectedPitchContext:
    return ExistingSelectedPitchContext(
        title="The Silver Bell Buoy",
        hook="Mira follows a bell-lit clue across the harbor before bed.",
        central_conflict="She must help the harbor settle before the night stretches too long.",
        why_it_fits="It keeps wonder active while the emotional repair stays soft.",
    )


def _build_character_sheet() -> ExistingCharacterSheetContext:
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


def _build_character_context() -> CharacterGenerationPromptContext:
    return CharacterGenerationPromptContext(
        candidate_count=2,
        selected_pitch=_build_selected_pitch(),
        raw_brief=(
            "A child follows floating lanterns across a harbor and helps a shy otter guardian "
            "bring each light home before bedtime."
        ),
        genre_label="Quest Fantasy",
        tone_label="Hushed Wonder",
    )


def _build_beat_context() -> BeatSheetGenerationPromptContext:
    return BeatSheetGenerationPromptContext(
        selected_pitch=_build_selected_pitch(),
        selected_character_sheet=_build_character_sheet(),
        raw_brief="A harbor child follows a silver bell and helps the docks settle before bed.",
        genre_label="Quest Fantasy",
        tone_label="Hushed Wonder",
        bedtime_goal="leave the child listener ready to drift off feeling tucked in",
    )


def test_eval_bedtime_guideline_policy_fragment_covers_core_safety_criteria() -> None:
    fragments = {
        stage: build_bedtime_guidelines_fragment(stage=stage) for stage in BEDTIME_PROMPT_STAGES
    }
    criteria = {
        "max_scare_level_defined": all(
            "Maximum scare level" in fragment for fragment in fragments.values()
        ),
        "violence_avoidance_defined": all(
            "Violence avoidance" in fragment for fragment in fragments.values()
        ),
        "emotional_repair_defined": all(
            "Emotional repair" in fragment for fragment in fragments.values()
        ),
        "reassuring_resolution_defined": all(
            "Resolution requirement" in fragment for fragment in fragments.values()
        ),
        "wonder_and_adventure_preserved": all(
            "Adventure, wonder, discovery, and mild mystery are welcome" in fragment
            for fragment in fragments.values()
        ),
        "stage_specific_focus_present": all(
            f"Stage focus for {stage}" in fragments[stage] for stage in BEDTIME_PROMPT_STAGES
        ),
    }

    assert all(criteria.values()), criteria


def test_eval_audience_preset_plan_exposes_live_default_and_planned_extensions() -> None:
    presets = get_bedtime_audience_preset_plan()
    active_presets = [preset for preset in presets if preset.status == "active"]
    planned_presets = [preset for preset in presets if preset.status == "planned"]
    criteria = {
        "one_active_preset_available": len(active_presets) == 1,
        "default_key_matches_active_preset": active_presets[0].key
        == DEFAULT_BEDTIME_GUIDELINE_PRESET_KEY,
        "planned_presets_exist": len(planned_presets) >= 2,
        "planned_presets_document_adjustments": all(
            len(preset.prompt_adjustments) >= 1 for preset in planned_presets
        ),
    }

    assert all(criteria.values()), criteria


@pytest.mark.parametrize(
    ("stage", "renderer", "context"),
    [
        ("pitch", render_pitch_generation_prompt, _build_pitch_context()),
        ("character", render_character_generation_prompt, _build_character_context()),
        ("beat", render_beat_sheet_generation_prompt, _build_beat_context()),
    ],
)
def test_eval_stage_prompts_include_shared_bedtime_policy(
    stage: str,
    renderer,
    context,
) -> None:
    prompt = renderer(context)
    criteria = {
        "shared_fragment_included": "Shared bedtime safety policy" in prompt,
        "max_scare_level_included": "Maximum scare level" in prompt,
        "violence_guardrail_included": "Violence avoidance" in prompt,
        "emotional_repair_included": "Emotional repair" in prompt,
        "stage_focus_included": f"Stage focus for {stage}" in prompt,
        "preset_key_serialized_in_context": (
            f'"bedtime_guideline_preset_key": "{DEFAULT_BEDTIME_GUIDELINE_PRESET_KEY}"' in prompt
        ),
    }

    assert all(criteria.values()), criteria


def test_eval_prompt_context_rejects_unsupported_bedtime_preset_key() -> None:
    with pytest.raises(ValueError, match="unsupported bedtime guideline preset key"):
        PitchGenerationPromptContext(
            candidate_count=3,
            bedtime_guideline_preset_key="preschool_gentle_3_to_5",
            raw_brief="A child follows lanterns through a harbor before bed.",
        )
