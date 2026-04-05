from __future__ import annotations

from collections.abc import Sequence

from app.models.story_outline import (
    OutlineCardKind,
    StoryOutlineBeatInput,
    StoryOutlineCard,
    StoryOutlinePlan,
    StoryOutlinePlanningContext,
)

_SAVE_THE_CAT_BEAT_PROGRESS = {
    "opening_image": 0,
    "theme_stated": 5,
    "set_up": 8,
    "catalyst": 12,
    "debate": 18,
    "break_into_two": 22,
    "b_story": 28,
    "fun_and_games": 38,
    "midpoint": 50,
    "bad_guys_close_in": 65,
    "all_is_lost": 75,
    "dark_night_of_the_soul": 80,
    "break_into_three": 84,
    "finale": 92,
    "final_image": 100,
}


class StoryOutlineGenerationServiceError(Exception):
    """Raised when story outline generation cannot proceed."""


class StoryOutlineGenerationService:
    def generate_outline(
        self,
        context: StoryOutlinePlanningContext,
    ) -> StoryOutlinePlan:
        beats = sorted(context.beats, key=lambda beat: beat.order)
        if not beats:
            raise StoryOutlineGenerationServiceError(
                "story outline generation requires at least one beat",
            )

        outline_kind = _resolve_outline_kind(context)
        card_count = _resolve_card_count(outline_kind, context, len(beats))
        groups = _group_beats(beats, card_count)
        weights = [max(1, len(group)) for group in groups]
        word_targets = _distribute_targets(context.target_word_count, weights)
        runtime_targets = _distribute_targets(context.target_runtime_minutes, weights)
        scene_targets = _resolve_scene_targets(
            outline_kind,
            context.approximate_scene_count,
            len(groups),
            weights,
        )

        cards = [
            _build_card(
                outline_kind=outline_kind,
                position=index + 1,
                group=group,
                genre_label=context.genre_label,
                tone_label=context.tone_label,
                target_word_count=word_targets[index],
                target_runtime_minutes=runtime_targets[index],
                target_scene_count=scene_targets[index],
                chapter_style=context.chapter_style,
                guidance_notes=context.guidance_notes,
            )
            for index, group in enumerate(groups)
        ]

        return StoryOutlinePlan(
            outline_kind=outline_kind,
            summary=_build_outline_summary(
                outline_kind=outline_kind,
                cards=cards,
                beat_sheet_summary=context.beat_sheet_summary,
                genre_label=context.genre_label,
                tone_label=context.tone_label,
            ),
            cards=cards,
            metadata={
                "genre_label": context.genre_label,
                "tone_label": context.tone_label,
                "tone_description": context.tone_description,
                "target_word_count": context.target_word_count,
                "target_runtime_minutes": context.target_runtime_minutes,
                "chapter_count": context.chapter_count,
                "approximate_scene_count": context.approximate_scene_count,
                "chapter_style": context.chapter_style,
                "guidance_notes": context.guidance_notes,
                "bedtime_goal": context.bedtime_goal,
                "preferences": context.preferences,
            },
        )

    def regenerate_card(
        self,
        *,
        context: StoryOutlinePlanningContext,
        card: StoryOutlineCard,
        position: int | None = None,
    ) -> StoryOutlineCard:
        beats_by_key = {
            beat.key: beat for beat in sorted(context.beats, key=lambda beat: beat.order)
        }
        group = [beats_by_key[beat_key] for beat_key in card.beat_keys if beat_key in beats_by_key]
        if not group:
            raise StoryOutlineGenerationServiceError(
                "story outline card regeneration requires matching supporting beats",
            )

        regenerated = _build_card(
            outline_kind=card.card_type,
            position=position or card.position,
            group=group,
            genre_label=context.genre_label,
            tone_label=context.tone_label,
            target_word_count=card.target_word_count,
            target_runtime_minutes=card.target_runtime_minutes,
            target_scene_count=card.target_scene_count,
            chapter_style=context.chapter_style,
            guidance_notes=context.guidance_notes,
        )
        return regenerated.model_copy(update={"card_key": card.card_key})


def _resolve_outline_kind(context: StoryOutlinePlanningContext) -> OutlineCardKind:
    if context.chapter_count is not None and context.chapter_count > 0:
        return "chapter"
    return "scene"


def _resolve_card_count(
    outline_kind: OutlineCardKind,
    context: StoryOutlinePlanningContext,
    beat_count: int,
) -> int:
    if outline_kind == "chapter":
        desired_count = context.chapter_count or max(3, min(5, beat_count // 3))
    else:
        desired_count = context.approximate_scene_count or max(4, min(8, beat_count // 2))

    return max(1, min(desired_count, beat_count))


def _group_beats(
    beats: Sequence[StoryOutlineBeatInput],
    card_count: int,
) -> list[list[StoryOutlineBeatInput]]:
    boundaries = [(index + 1) * (100 / card_count) for index in range(card_count - 1)]
    groups: list[list[StoryOutlineBeatInput]] = [[] for _ in range(card_count)]
    group_index = 0

    for beat in beats:
        progress = _SAVE_THE_CAT_BEAT_PROGRESS.get(
            beat.key,
            round(((beat.order - 1) / max(1, len(beats) - 1)) * 100),
        )
        while group_index < len(boundaries) and progress > boundaries[group_index]:
            group_index += 1
        groups[group_index].append(beat)

    if all(groups):
        return groups

    return _rebalance_evenly(beats, card_count)


def _rebalance_evenly(
    beats: Sequence[StoryOutlineBeatInput],
    card_count: int,
) -> list[list[StoryOutlineBeatInput]]:
    groups: list[list[StoryOutlineBeatInput]] = []
    beat_count = len(beats)
    for index in range(card_count):
        start = round(index * beat_count / card_count)
        end = round((index + 1) * beat_count / card_count)
        groups.append(list(beats[start:end]))
    return groups


def _distribute_targets(
    total: int | None,
    weights: Sequence[int],
) -> list[int | None]:
    if total is None or total <= 0:
        return [None for _ in weights]

    total_weight = sum(weights)
    if total_weight <= 0:
        return [None for _ in weights]

    allocations = [max(1, round(total * (weight / total_weight))) for weight in weights]
    delta = total - sum(allocations)
    step = 1 if delta > 0 else -1
    index = 0

    while delta != 0 and allocations:
        current_index = index % len(allocations)
        if step < 0 and allocations[current_index] <= 1:
            index += 1
            if index > len(allocations) * 4:
                break
            continue
        allocations[current_index] += step
        delta -= step
        index += 1

    return allocations


def _resolve_scene_targets(
    outline_kind: OutlineCardKind,
    approximate_scene_count: int | None,
    card_count: int,
    weights: Sequence[int],
) -> list[int | None]:
    if outline_kind == "scene":
        return [1 for _ in range(card_count)]

    return _distribute_targets(approximate_scene_count, weights)


def _build_card(
    *,
    outline_kind: OutlineCardKind,
    position: int,
    group: Sequence[StoryOutlineBeatInput],
    genre_label: str | None,
    tone_label: str | None,
    target_word_count: int | None,
    target_runtime_minutes: int | None,
    target_scene_count: int | None,
    chapter_style: str | None,
    guidance_notes: str | None,
) -> StoryOutlineCard:
    start = group[0]
    end = group[-1]
    card_label = "Chapter" if outline_kind == "chapter" else "Scene"
    title_range = start.label if start.key == end.key else f"{start.label} to {end.label}"
    bedtime_guardrail = _coalesce_detail(
        [beat.bedtime_softening_note for beat in group],
        fallback="Keep tension brief, readable, and quickly repaired before the next turn.",
    )
    tone_direction = _build_tone_direction(genre_label=genre_label, tone_label=tone_label)

    return StoryOutlineCard(
        card_key=f"{outline_kind}-{position}",
        card_type=outline_kind,
        position=position,
        title=f"{card_label} {position}: {title_range}",
        purpose=_build_card_purpose(group),
        summary=_build_card_summary(group),
        beat_keys=[beat.key for beat in group],
        beat_labels=[beat.label for beat in group],
        emotional_shift=_build_emotional_shift(group),
        target_word_count=target_word_count,
        target_runtime_minutes=target_runtime_minutes,
        target_scene_count=target_scene_count,
        tone_direction=tone_direction,
        bedtime_guardrail=bedtime_guardrail,
        drafting_brief=_build_drafting_brief(
            outline_kind=outline_kind,
            position=position,
            group=group,
            genre_label=genre_label,
            tone_label=tone_label,
            target_word_count=target_word_count,
            target_runtime_minutes=target_runtime_minutes,
            target_scene_count=target_scene_count,
            bedtime_guardrail=bedtime_guardrail,
            chapter_style=chapter_style,
            guidance_notes=guidance_notes,
        ),
    )


def _build_card_purpose(group: Sequence[StoryOutlineBeatInput]) -> str:
    start = group[0]
    end = group[-1]
    if start.key == end.key:
        return (
            f"Deliver the {start.label.lower()} turn clearly enough that the next card "
            "can draft forward without re-explaining the beat."
        )

    return (
        f"Bridge the story from {start.label.lower()} into {end.label.lower()} as one "
        "readable stretch of forward motion."
    )


def _build_card_summary(group: Sequence[StoryOutlineBeatInput]) -> str:
    if len(group) == 1:
        return group[0].summary.strip()

    opening = group[0].summary.strip().rstrip(".")
    landing = group[-1].summary.strip()
    middle_labels = ", ".join(beat.label for beat in group[1:-1])

    if middle_labels:
        return (
            f"{opening}. Move through {middle_labels.lower()} before landing on "
            f"{landing[0].lower() + landing[1:]}"
        )

    return f"{opening}. Then land on {landing[0].lower() + landing[1:]}"


def _build_emotional_shift(group: Sequence[StoryOutlineBeatInput]) -> str:
    first_intent = _read_first_non_empty([group[0].emotional_intent])
    last_intent = _read_first_non_empty([group[-1].emotional_intent])

    if first_intent and last_intent and first_intent != last_intent:
        return f"Move from {first_intent.lower()} toward {last_intent.lower()}."

    if last_intent:
        return last_intent

    if first_intent:
        return first_intent

    return (
        f"Guide the mood from {group[0].label.lower()} into {group[-1].label.lower()} "
        "without losing the bedtime landing."
    )


def _build_tone_direction(
    *,
    genre_label: str | None,
    tone_label: str | None,
) -> str | None:
    parts = []
    if tone_label:
        parts.append(f"Stay anchored in the {tone_label} tone")
    if genre_label:
        parts.append(f"while advancing the {genre_label} lane")
    if not parts:
        return None
    return " ".join(parts) + "."


def _build_drafting_brief(
    *,
    outline_kind: OutlineCardKind,
    position: int,
    group: Sequence[StoryOutlineBeatInput],
    genre_label: str | None,
    tone_label: str | None,
    target_word_count: int | None,
    target_runtime_minutes: int | None,
    target_scene_count: int | None,
    bedtime_guardrail: str | None,
    chapter_style: str | None,
    guidance_notes: str | None,
) -> str:
    beats = ", ".join(beat.label for beat in group)
    length_bits = [
        f"about {target_word_count} words" if target_word_count is not None else None,
        f"around {target_runtime_minutes} minutes" if target_runtime_minutes is not None else None,
        (
            f"roughly {target_scene_count} scene{'s' if target_scene_count != 1 else ''}"
            if target_scene_count is not None and outline_kind == "chapter"
            else None
        ),
    ]
    scope_bits = ", ".join(bit for bit in length_bits if bit)
    lane_bits = " / ".join(
        bit for bit in [genre_label, tone_label, chapter_style] if bit is not None
    )
    guidance_suffix = f" Additional guidance: {guidance_notes.strip()}" if guidance_notes else ""
    return (
        f"{'Chapter' if outline_kind == 'chapter' else 'Scene'} {position} should cover {beats}."
        f" Keep the lane aligned with {lane_bits or 'the accepted plan'}."
        " Draft for "
        f"{scope_bits or 'a compact writing segment'} and protect this bedtime guardrail:"
        f" {bedtime_guardrail or 'resolve any spike in tension quickly and visibly.'}"
        f"{guidance_suffix}"
    )


def _build_outline_summary(
    *,
    outline_kind: OutlineCardKind,
    cards: Sequence[StoryOutlineCard],
    beat_sheet_summary: str | None,
    genre_label: str | None,
    tone_label: str | None,
) -> str:
    lane_bits = " / ".join(bit for bit in [genre_label, tone_label] if bit is not None)
    card_label = "chapters" if outline_kind == "chapter" else "scenes"
    summary_parts = [
        f"{len(cards)} draftable {card_label} mapped from the accepted beat sheet.",
        beat_sheet_summary,
        f"Lane: {lane_bits}." if lane_bits else None,
    ]
    return " ".join(part.strip() for part in summary_parts if part and part.strip())


def _coalesce_detail(values: Sequence[str | None], *, fallback: str) -> str:
    first = _read_first_non_empty(values)
    return first or fallback


def _read_first_non_empty(values: Sequence[str | None]) -> str | None:
    for value in values:
        if value is None:
            continue
        normalized = value.strip()
        if normalized:
            return normalized
    return None
