from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field, model_validator

OutlineCardKind = Literal["chapter", "scene"]
StoryOutlineChangeImpact = Literal["minor", "major"]


class StoryOutlineBeatInput(BaseModel):
    key: str = Field(min_length=1)
    label: str = Field(min_length=1)
    order: int = Field(ge=1)
    summary: str = Field(min_length=1)
    emotional_intent: str | None = None
    bedtime_softening_note: str | None = None


class StoryOutlinePlanningContext(BaseModel):
    genre_label: str | None = None
    tone_label: str | None = None
    tone_description: str | None = None
    beat_sheet_summary: str | None = None
    beats: list[StoryOutlineBeatInput] = Field(default_factory=list)
    target_word_count: int | None = Field(default=None, ge=1)
    target_runtime_minutes: int | None = Field(default=None, ge=1)
    chapter_count: int | None = Field(default=None, ge=1)
    approximate_scene_count: int | None = Field(default=None, ge=1)
    chapter_style: str | None = None
    guidance_notes: str | None = None
    bedtime_goal: str | None = None
    preferences: dict[str, Any] | list[Any] | None = None

    @model_validator(mode="after")
    def validate_beats(self) -> "StoryOutlinePlanningContext":
        if not self.beats:
            raise ValueError("story outline planning requires at least one beat")
        return self


class StoryOutlineCard(BaseModel):
    card_key: str = Field(min_length=1)
    card_type: OutlineCardKind
    position: int = Field(ge=1)
    title: str = Field(min_length=1)
    purpose: str | None = Field(default=None, min_length=1)
    summary: str = Field(min_length=1)
    beat_keys: list[str] = Field(default_factory=list)
    beat_labels: list[str] = Field(default_factory=list)
    emotional_shift: str = Field(min_length=1)
    target_word_count: int | None = Field(default=None, ge=1)
    target_runtime_minutes: int | None = Field(default=None, ge=1)
    target_scene_count: int | None = Field(default=None, ge=1)
    tone_direction: str | None = None
    bedtime_guardrail: str | None = None
    drafting_brief: str | None = None

    @model_validator(mode="after")
    def validate_beats(self) -> "StoryOutlineCard":
        if not self.beat_keys:
            raise ValueError("story outline cards require at least one supporting beat")
        return self


class StoryOutlinePlan(BaseModel):
    outline_kind: OutlineCardKind
    summary: str = Field(min_length=1)
    cards: list[StoryOutlineCard] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)

    @model_validator(mode="after")
    def validate_cards(self) -> "StoryOutlinePlan":
        if not self.cards:
            raise ValueError("story outline plans require at least one card")
        return self
