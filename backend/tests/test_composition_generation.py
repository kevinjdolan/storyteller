from __future__ import annotations

from app.ai import (
    get_composition_segment_generation_response_schema,
    render_composition_segment_generation_prompt,
)
from app.models import (
    CompositionPromptPackage,
    CompositionSegmentCarryoverContext,
    CompositionSegmentCarryoverItem,
    CompositionSegmentGenerationPromptContext,
)


def test_composition_segment_generation_prompt_includes_structured_carryover() -> None:
    context = _build_prompt_context()

    prompt = render_composition_segment_generation_prompt(context)

    assert "structured carryover summaries" in prompt
    assert '"prior_segments"' in prompt
    assert '"story_so_far_summary"' in prompt
    assert "Moonlit Harbor" in prompt
    assert "Chapter 2: Midpoint" in prompt


def test_eval_composition_segment_generation_contract_exposes_required_fields() -> None:
    context = _build_prompt_context()
    prompt = render_composition_segment_generation_prompt(context)
    schema = get_composition_segment_generation_response_schema()

    criteria = {
        "prompt_mentions_segment_scope": "Write only the requested segment" in prompt,
        "prompt_mentions_structured_carryover": "structured carryover summaries" in prompt,
        "carryover_context_includes_prior_segment_summary": (
            context.carryover.prior_segments[0].accepted_summary in prompt
        ),
        "response_schema_requires_raw_text": "raw_text" in schema["properties"],
        "response_schema_requires_accepted_text": "accepted_text" in schema["properties"],
        "response_schema_requires_carryover_summary": ("carryover_summary" in schema["properties"]),
    }

    assert all(criteria.values()), criteria


def _build_prompt_context() -> CompositionSegmentGenerationPromptContext:
    return CompositionSegmentGenerationPromptContext(
        composition_prompt=CompositionPromptPackage.model_validate(
            {
                "schema_version": 1,
                "assembly_version": "composition_prompt_assembly.v1",
                "system_instructions": {
                    "prompt_version": "composition_prompt_assembly.v1",
                    "bedtime_guideline_preset_key": "shared_bedtime_default",
                    "writer_role": "Backend-owned bedtime story composition engine",
                    "mission": "Draft the next bedtime-safe story segment from durable state.",
                    "output_contract": [
                        "Write only the requested segment, not the whole story.",
                        "Honor continuity facts and previously locked details.",
                    ],
                    "storytelling_guardrails": [
                        "Keep the narration calm and bedtime-safe.",
                        "End on a settled handoff.",
                    ],
                    "bedtime_guidelines_fragment": (
                        "Stage focus for composition: keep repair visible."
                    ),
                },
                "dynamic_context": {
                    "session_id": "session-123",
                    "display_title": "Moonlit Harbor",
                    "bedtime_guideline_preset_key": "shared_bedtime_default",
                    "job_kind": "draft",
                    "segment_index": 2,
                    "request_instructions": "Keep the midpoint especially gentle.",
                    "segment_goal_summary": "Chapter 2 should center the midpoint reveal softly.",
                    "genre": {
                        "label": "Quest Fantasy",
                        "description": "A calm harbor quest.",
                    },
                    "tone": {
                        "label": "Hushed Wonder",
                        "description": "Soft and luminous.",
                    },
                    "brief": {
                        "raw_brief": "A harbor fox follows a silver bell and returns home calm.",
                    },
                    "selected_pitch": {
                        "title": "The Silver Bell Buoy",
                        "hook": "A silver bell drifts through moonlit water.",
                        "central_conflict": "Mira must guide it home before sleep.",
                        "why_it_fits": "Gentle wonder and visible repair.",
                    },
                    "selected_character_sheet": {
                        "title": "Mira and the Bell",
                        "protagonist_name": "Mira",
                        "supporting_cast": [
                            {
                                "name": "Pip",
                                "role": "steady helper",
                                "goal": "Keep Mira company until the bell is safe.",
                                "flaw": "Worries when the water goes too quiet.",
                                "comfort_trait": "Answers every worry with a grounding detail.",
                                "bedtime_safety_notes": "Keep Pip visibly near Mira.",
                            }
                        ],
                    },
                    "beat_sheet": {
                        "revision_number": 1,
                        "summary": "A soft Save-the-Cat arc.",
                    },
                    "story_setup": {
                        "revision_number": 1,
                        "target_word_count": 1600,
                        "target_runtime_minutes": 11,
                    },
                    "outline_card": {
                        "story_outline_id": "outline-123",
                        "story_outline_revision_number": 1,
                        "outline_kind": "chapter",
                        "card_key": "chapter-2",
                        "position": 2,
                        "title": "Chapter 2: Midpoint",
                        "summary": "Let the hidden cove feel awe-filled instead of sharp.",
                        "drafting_brief": "Chapter 2 centers the midpoint reveal softly.",
                    },
                    "continuity": {
                        "continuity_bible_id": "continuity-123",
                        "revision_number": 2,
                        "summary_text": "Mira and Pip are already safely away from the dock.",
                        "facts": [
                            {
                                "key": "promise:1",
                                "category": "promise",
                                "title": "Bell promise",
                                "detail": "The bell still needs to be guided home.",
                                "source_stage": "beats",
                                "source_label": "Revision 1",
                            }
                        ],
                    },
                },
                "debug_context": {
                    "prompt_version": "composition_prompt_assembly.v1",
                    "session_id": "session-123",
                    "display_title": "Moonlit Harbor",
                    "job_kind": "draft",
                    "segment_index": 2,
                    "outline_card_key": "chapter-2",
                    "outline_card_title": "Chapter 2: Midpoint",
                    "story_outline_revision_number": 1,
                    "beat_sheet_revision_number": 1,
                    "story_setup_revision_number": 1,
                    "continuity_revision_number": 2,
                    "continuity_fact_count": 1,
                    "selected_pitch_title": "The Silver Bell Buoy",
                    "selected_character_sheet_title": "Mira and the Bell",
                    "requested_instruction_excerpt": "Keep the midpoint especially gentle.",
                    "segment_goal_summary": "Chapter 2 should center the midpoint reveal softly.",
                },
            }
        ),
        carryover=CompositionSegmentCarryoverContext(
            prior_segment_count=1,
            story_so_far_summary=(
                "Segment 1 established the quiet harbor and sent Mira after the drifting bell."
            ),
            latest_accepted_summary=(
                "Mira left the dock with Pip beside her and promised the harbor a calm return."
            ),
            prior_segments=[
                CompositionSegmentCarryoverItem(
                    segment_index=1,
                    outline_card_title="Chapter 1: Opening Image to Catalyst",
                    accepted_summary=(
                        "Mira left the dock with Pip beside her and promised the harbor a calm "
                        "return."
                    ),
                    accepted_word_count=510,
                )
            ],
        ),
    )
