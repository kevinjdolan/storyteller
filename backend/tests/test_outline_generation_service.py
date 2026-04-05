from __future__ import annotations

from app.models.story_outline import StoryOutlineBeatInput, StoryOutlinePlanningContext
from app.services.outline_generation import StoryOutlineGenerationService


def _build_beats() -> list[StoryOutlineBeatInput]:
    return [
        StoryOutlineBeatInput(
            key="opening_image",
            label="Opening Image",
            order=1,
            summary="Mira watches lanterns drift across the moonlit harbor.",
            emotional_intent="Begin with stillness and wonder.",
        ),
        StoryOutlineBeatInput(
            key="theme_stated",
            label="Theme Stated",
            order=2,
            summary="Otis reminds Mira that every light finds home when it is guided gently.",
            emotional_intent="Set trust beside curiosity.",
        ),
        StoryOutlineBeatInput(
            key="set_up",
            label="Set-Up",
            order=3,
            summary="The harbor routines and Mira's worries become clear before the night deepens.",
            emotional_intent="Keep the world readable and safe.",
        ),
        StoryOutlineBeatInput(
            key="catalyst",
            label="Catalyst",
            order=4,
            summary="One lantern drifts away from the others and asks for help.",
            emotional_intent="Introduce a gentle problem.",
        ),
        StoryOutlineBeatInput(
            key="debate",
            label="Debate",
            order=5,
            summary="Mira wonders whether she is ready to leave the dock and follow it.",
            emotional_intent="Let hesitation stay brief and held.",
        ),
        StoryOutlineBeatInput(
            key="break_into_two",
            label="Break Into Two",
            order=6,
            summary="Mira and Otis step onto the water path to begin the quiet search.",
            emotional_intent="Turn hesitation into motion.",
        ),
        StoryOutlineBeatInput(
            key="b_story",
            label="B Story",
            order=7,
            summary="Otis shares a calmer way to listen when the harbor feels too large.",
            emotional_intent="Deepen the bond and the bedtime tone.",
        ),
        StoryOutlineBeatInput(
            key="fun_and_games",
            label="Fun and Games",
            order=8,
            summary="The pair follows reflected clues through glowing boats and sleepy gulls.",
            emotional_intent="Make discovery feel playful and warm.",
        ),
        StoryOutlineBeatInput(
            key="midpoint",
            label="Midpoint",
            order=9,
            summary="The lantern reveals the hidden cove where the harbor's last promise waits.",
            emotional_intent="Lift wonder while keeping tension soft.",
            bedtime_softening_note="Keep the surprise luminous and quickly reassuring.",
        ),
        StoryOutlineBeatInput(
            key="bad_guys_close_in",
            label="Bad Guys Close In",
            order=10,
            summary="The tide turns and Mira fears they may miss the harbor's bedtime rhythm.",
            emotional_intent="Narrow the space without making the danger harsh.",
        ),
        StoryOutlineBeatInput(
            key="all_is_lost",
            label="All Is Lost",
            order=11,
            summary="The lantern dims for a moment and Mira thinks she has failed.",
            emotional_intent="Let the low point feel temporary and held.",
            bedtime_softening_note="Buffer the low point with visible companionship.",
        ),
        StoryOutlineBeatInput(
            key="dark_night_of_the_soul",
            label="Dark Night of the Soul",
            order=12,
            summary="Otis helps Mira name the fear and remember the harbor's patient rhythm.",
            emotional_intent="Turn fear into reflection and comfort.",
        ),
        StoryOutlineBeatInput(
            key="break_into_three",
            label="Break Into Three",
            order=13,
            summary="Mira chooses a gentler route home that uses the harbor's own lights.",
            emotional_intent="Shift from doubt into steady resolve.",
        ),
        StoryOutlineBeatInput(
            key="finale",
            label="Finale",
            order=14,
            summary="The lantern returns to its doorstep and the whole harbor settles together.",
            emotional_intent="Deliver repair, belonging, and visible calm.",
        ),
        StoryOutlineBeatInput(
            key="final_image",
            label="Final Image",
            order=15,
            summary="Mira falls asleep watching the restored lights ripple over still water.",
            emotional_intent="End in softness and rest.",
        ),
    ]


def test_generate_outline_uses_chapter_count_to_build_chapter_cards() -> None:
    plan = StoryOutlineGenerationService().generate_outline(
        StoryOutlinePlanningContext(
            genre_label="Quest Fantasy",
            tone_label="Hushed Wonder",
            beat_sheet_summary="A harbor quest that lands in calm belonging.",
            beats=_build_beats(),
            target_word_count=1800,
            target_runtime_minutes=12,
            chapter_count=3,
            approximate_scene_count=8,
            chapter_style="three gentle chapters",
            guidance_notes="Keep each chapter ending calmer than it began.",
        )
    )

    assert plan.outline_kind == "chapter"
    assert len(plan.cards) == 3
    assert all(card.card_type == "chapter" for card in plan.cards)
    assert all(card.beat_keys for card in plan.cards)
    assert all(card.purpose is not None for card in plan.cards)
    assert plan.cards[0].target_scene_count is not None
    assert plan.cards[0].tone_direction == (
        "Stay anchored in the Hushed Wonder tone while advancing the Quest Fantasy lane."
    )
    assert "Quest Fantasy" in plan.summary


def test_generate_outline_falls_back_to_scene_cards_when_no_chapter_count_exists() -> None:
    plan = StoryOutlineGenerationService().generate_outline(
        StoryOutlinePlanningContext(
            genre_label="Cozy Mystery",
            tone_label="Sleepy Curiosity",
            beat_sheet_summary="A calm mystery that resolves before bed.",
            beats=_build_beats(),
            approximate_scene_count=5,
            target_word_count=1500,
            target_runtime_minutes=10,
        )
    )

    assert plan.outline_kind == "scene"
    assert len(plan.cards) == 5
    assert all(card.card_type == "scene" for card in plan.cards)
    assert all(card.target_scene_count == 1 for card in plan.cards)
    assert all(card.purpose is not None for card in plan.cards)
    assert all(card.drafting_brief is not None for card in plan.cards)


def test_generate_outline_preserves_ordered_beat_coverage() -> None:
    plan = StoryOutlineGenerationService().generate_outline(
        StoryOutlinePlanningContext(
            genre_label="Quest Fantasy",
            tone_label="Hushed Wonder",
            beat_sheet_summary="A harbor quest that lands in calm belonging.",
            beats=_build_beats(),
            chapter_count=4,
            approximate_scene_count=8,
        )
    )

    flattened = [beat_key for card in plan.cards for beat_key in card.beat_keys]

    assert flattened == [beat.key for beat in _build_beats()]
    assert all(card.emotional_shift for card in plan.cards)


def test_eval_outline_chapter_plan_preserves_targets_tone_and_guardrails() -> None:
    plan = StoryOutlineGenerationService().generate_outline(
        StoryOutlinePlanningContext(
            genre_label="Quest Fantasy",
            tone_label="Hushed Wonder",
            beat_sheet_summary="A harbor quest that lands in calm belonging.",
            beats=_build_beats(),
            target_word_count=1800,
            target_runtime_minutes=12,
            chapter_count=4,
            approximate_scene_count=8,
            guidance_notes="Keep each chapter ending calmer than it began.",
        )
    )

    assert plan.outline_kind == "chapter"
    assert len(plan.cards) == 4
    assert sum(card.target_word_count or 0 for card in plan.cards) == 1800
    assert sum(card.target_runtime_minutes or 0 for card in plan.cards) == 12
    assert all(card.tone_direction is not None for card in plan.cards)
    assert all(card.purpose is not None for card in plan.cards)
    assert all(card.drafting_brief is not None for card in plan.cards)
    assert all(card.bedtime_guardrail is not None for card in plan.cards)
    assert any(
        "visible companionship" in (card.bedtime_guardrail or "").lower() for card in plan.cards
    )
    assert "Lane: Quest Fantasy / Hushed Wonder." in plan.summary


def test_eval_outline_scene_mode_uses_softened_beats_in_scene_cards() -> None:
    plan = StoryOutlineGenerationService().generate_outline(
        StoryOutlinePlanningContext(
            genre_label="Cozy Mystery",
            tone_label="Sleepy Curiosity",
            beat_sheet_summary="A calm harbor mystery that resolves before bed.",
            beats=_build_beats(),
            approximate_scene_count=6,
            target_word_count=1500,
            target_runtime_minutes=10,
            guidance_notes="Keep the emotional lows brief and visibly supported.",
        )
    )

    midpoint_card = next(card for card in plan.cards if "midpoint" in card.beat_keys)
    all_is_lost_card = next(card for card in plan.cards if "all_is_lost" in card.beat_keys)

    assert plan.outline_kind == "scene"
    assert len(plan.cards) == 6
    assert all(card.card_type == "scene" for card in plan.cards)
    assert all(card.target_scene_count == 1 for card in plan.cards)
    assert "luminous and quickly reassuring" in (midpoint_card.bedtime_guardrail or "")
    assert "visible companionship" in (all_is_lost_card.bedtime_guardrail or "")
    assert all("Sleepy Curiosity" in (card.drafting_brief or "") for card in plan.cards)
