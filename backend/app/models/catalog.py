from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field, model_validator


def _normalize_string_list(values: list[str]) -> list[str]:
    normalized = [value.strip() for value in values if value.strip()]
    return list(dict.fromkeys(normalized))


class ToneCatalogSeed(BaseModel):
    slug: str
    label: str
    description: str
    bedtime_notes: str
    descriptors: list[str] = Field(default_factory=list)
    default_planning_hints: dict[str, Any] = Field(default_factory=dict)
    is_active: bool = True

    model_config = ConfigDict(str_strip_whitespace=True)

    @model_validator(mode="after")
    def validate_fields(self) -> "ToneCatalogSeed":
        self.descriptors = _normalize_string_list(self.descriptors)

        if not self.descriptors:
            raise ValueError("tone descriptors must contain at least one non-empty value")

        if not self.default_planning_hints:
            raise ValueError("tone default_planning_hints must not be empty")

        return self


class GenreCatalogSeed(BaseModel):
    slug: str
    label: str
    description: str
    bedtime_safety_notes: str
    arc_notes: dict[str, Any] = Field(default_factory=dict)
    is_active: bool = True
    tones: list[ToneCatalogSeed] = Field(default_factory=list)

    model_config = ConfigDict(str_strip_whitespace=True)

    @model_validator(mode="after")
    def validate_fields(self) -> "GenreCatalogSeed":
        if not self.arc_notes:
            raise ValueError("genre arc_notes must not be empty")

        if not self.tones:
            raise ValueError("genre tones must not be empty")

        tone_slugs = [tone.slug for tone in self.tones]
        if len(tone_slugs) != len(set(tone_slugs)):
            raise ValueError(f"duplicate tone slug detected for genre {self.slug}")

        return self


class GenreToneCatalogDocument(BaseModel):
    genres: list[GenreCatalogSeed] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_fields(self) -> "GenreToneCatalogDocument":
        if not self.genres:
            raise ValueError("catalog must define at least one genre")

        genre_slugs = [genre.slug for genre in self.genres]
        if len(genre_slugs) != len(set(genre_slugs)):
            raise ValueError("duplicate genre slug detected in catalog")

        return self


class ToneCatalogEntry(BaseModel):
    id: str
    genre_id: str
    slug: str
    label: str
    description: str | None = None
    bedtime_notes: str | None = None
    descriptors: list[str] = Field(default_factory=list)
    default_planning_hints: dict[str, Any] = Field(default_factory=dict)
    sort_order: int


class GenreCatalogEntry(BaseModel):
    id: str
    slug: str
    label: str
    description: str | None = None
    bedtime_safety_notes: str | None = None
    arc_notes: dict[str, Any] = Field(default_factory=dict)
    sort_order: int
