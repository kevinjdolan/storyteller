from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass

from app.models.story_outline import (
    StoryOutlineCard,
    StoryOutlineChangeImpact,
    StoryOutlinePlanningContext,
)
from app.models.workflow import WorkflowStage, get_invalidated_stages_after_edit
from app.services.outline_generation import StoryOutlineGenerationService

_TEXTUAL_OUTLINE_FIELDS = {
    "title",
    "purpose",
    "summary",
    "emotional_shift",
    "drafting_brief",
}

_STRUCTURAL_OUTLINE_FIELDS = {
    "card_type",
    "position",
    "beat_keys",
    "beat_labels",
    "target_word_count",
    "target_runtime_minutes",
    "target_scene_count",
}


@dataclass(frozen=True)
class StoryOutlineEditAssessment:
    changed_fields: tuple[str, ...]
    changed_card_keys: tuple[str, ...]
    regenerated_card_keys: tuple[str, ...]
    change_impact: StoryOutlineChangeImpact
    reordered: bool
    refreshes_downstream: bool
    invalidated_stages: tuple[WorkflowStage, ...]
    summary_text: str


def normalize_story_outline_cards(
    cards: Sequence[StoryOutlineCard],
) -> list[StoryOutlineCard]:
    return [
        card.model_copy(update={"position": index + 1})
        for index, card in enumerate(cards)
    ]


def regenerate_story_outline_cards(
    *,
    cards: Sequence[StoryOutlineCard],
    regenerate_card_keys: Sequence[str],
    context: StoryOutlinePlanningContext,
    generator: StoryOutlineGenerationService,
) -> list[StoryOutlineCard]:
    normalized_cards = normalize_story_outline_cards(cards)
    requested_regenerations = {
        card_key.strip() for card_key in regenerate_card_keys if card_key.strip()
    }
    if not requested_regenerations:
        return normalized_cards

    return [
        (
            generator.regenerate_card(
                context=context,
                card=card,
                position=index + 1,
            )
            if card.card_key in requested_regenerations
            else card
        )
        for index, card in enumerate(normalized_cards)
    ]


def assess_story_outline_edit(
    *,
    current_cards: Sequence[StoryOutlineCard],
    requested_cards: Sequence[StoryOutlineCard],
    regenerate_card_keys: Sequence[str] = (),
) -> StoryOutlineEditAssessment:
    normalized_current = normalize_story_outline_cards(current_cards)
    normalized_requested = normalize_story_outline_cards(requested_cards)
    current_by_key = {card.card_key: card for card in normalized_current}
    requested_by_key = {card.card_key: card for card in normalized_requested}
    invalidated_stages = get_invalidated_stages_after_edit(WorkflowStage.STORY_SETUP)

    changed_fields: set[str] = set()
    changed_card_keys: list[str] = []
    current_order = [card.card_key for card in normalized_current]
    requested_order = [card.card_key for card in normalized_requested]
    reordered = current_order != requested_order

    if current_order != requested_order:
        changed_fields.add("card_order")

    if set(current_by_key) != set(requested_by_key):
        changed_fields.add("card_set")

    for card in normalized_requested:
        current = current_by_key.get(card.card_key)
        if current is None:
            changed_card_keys.append(card.card_key)
            continue

        current_dump = current.model_dump(mode="json")
        requested_dump = card.model_dump(mode="json")
        field_differences = {
            field_name
            for field_name, field_value in requested_dump.items()
            if current_dump.get(field_name) != field_value
        }
        if field_differences:
            changed_card_keys.append(card.card_key)
            changed_fields.update(field_differences)

    regenerated = tuple(
        card_key.strip()
        for card_key in regenerate_card_keys
        if card_key.strip() and card_key.strip() in requested_by_key
    )
    if regenerated:
        changed_fields.add("regenerated_card")

    structural_change = (
        reordered
        or "card_set" in changed_fields
        or bool(changed_fields.intersection(_STRUCTURAL_OUTLINE_FIELDS))
        or len(set(changed_card_keys)) > 1
    )
    if not changed_card_keys and regenerated:
        structural_change = False
    if not changed_card_keys:
        # Regenerated cards should still count as changed.
        changed_card_keys = list(regenerated)

    impact: StoryOutlineChangeImpact = "major" if structural_change else "minor"
    changed_count = len(set(changed_card_keys))
    invalidated_labels = _format_invalidated_stages(invalidated_stages)

    if impact == "major":
        if reordered:
            summary = (
                f"Saved a structural outline revision after reordering {changed_count} "
                f"card{'s' if changed_count != 1 else ''}. {invalidated_labels} need regeneration."
            )
        else:
            summary = (
                f"Saved a structural outline revision across {changed_count} "
                f"card{'s' if changed_count != 1 else ''}. {invalidated_labels} need regeneration."
            )
    elif regenerated:
        summary = (
            f"Regenerated {len(regenerated)} card{'s' if len(regenerated) != 1 else ''} "
            f"and saved the outline revision. {invalidated_labels} should refresh before reuse."
        )
    else:
        summary = (
            f"Updated {changed_count} outline card{'s' if changed_count != 1 else ''}. "
            f"{invalidated_labels} should refresh before reuse."
        )

    return StoryOutlineEditAssessment(
        changed_fields=tuple(sorted(changed_fields)),
        changed_card_keys=tuple(dict.fromkeys(changed_card_keys)),
        regenerated_card_keys=regenerated,
        change_impact=impact,
        reordered=reordered,
        refreshes_downstream=True,
        invalidated_stages=invalidated_stages,
        summary_text=summary,
    )


def _format_invalidated_stages(stages: Sequence[WorkflowStage]) -> str:
    labels = [stage.value.replace("_", " ") for stage in stages]
    if not labels:
        return "No downstream stages"
    if len(labels) == 1:
        return labels[0].capitalize()
    if len(labels) == 2:
        return f"{labels[0].capitalize()} and {labels[1]}"
    return f"{', '.join(labels[:-1]).capitalize()}, and {labels[-1]}"
