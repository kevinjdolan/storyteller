from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml
from sqlalchemy import Select, select
from sqlalchemy.orm import Session

from app.db import Genre, ToneProfile
from app.models import (
    GenreCatalogEntry,
    GenreCatalogSeed,
    GenreToneCatalogDocument,
    ToneCatalogEntry,
    ToneCatalogSeed,
)

CATALOG_FILE_PATH = Path(__file__).resolve().parents[1] / "data" / "genre_tone_catalog.yaml"


def _normalize_mapping(value: Any) -> dict[str, Any]:
    if isinstance(value, dict):
        return value

    return {}


def _normalize_string_list(value: Any) -> list[str]:
    if isinstance(value, list):
        return [str(item) for item in value]

    return []


@dataclass(frozen=True)
class CatalogSeedStats:
    created_genres: int = 0
    updated_genres: int = 0
    deactivated_genres: int = 0
    created_tones: int = 0
    updated_tones: int = 0
    deactivated_tones: int = 0


def load_catalog_document(path: Path = CATALOG_FILE_PATH) -> GenreToneCatalogDocument:
    raw_payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    return GenreToneCatalogDocument.model_validate(raw_payload or {})


def _build_genre_entry(row: Genre) -> GenreCatalogEntry:
    return GenreCatalogEntry(
        id=row.id,
        slug=row.slug,
        label=row.label,
        description=row.description,
        bedtime_safety_notes=row.bedtime_safety_notes,
        arc_notes=_normalize_mapping(row.arc_notes),
        sort_order=row.sort_order,
    )


def _build_tone_entry(row: ToneProfile) -> ToneCatalogEntry:
    return ToneCatalogEntry(
        id=row.id,
        genre_id=row.genre_id,
        slug=row.slug,
        label=row.label,
        description=row.description,
        bedtime_notes=row.bedtime_notes,
        descriptors=_normalize_string_list(row.descriptors),
        default_planning_hints=_normalize_mapping(row.default_planning_hints),
        sort_order=row.sort_order,
    )


def find_active_genre(
    session: Session,
    *,
    genre_slug: str | None = None,
    genre_id: str | None = None,
    genre_label: str | None = None,
) -> Genre | None:
    selected_count = sum(
        value is not None for value in (genre_slug, genre_id, genre_label)
    )
    if selected_count != 1:
        raise ValueError("exactly one genre selector is required")

    stmt: Select[tuple[Genre]] = select(Genre).where(Genre.is_active.is_(True))

    if genre_slug is not None:
        stmt = stmt.where(Genre.slug == genre_slug)
    elif genre_id is not None:
        stmt = stmt.where(Genre.id == genre_id)
    else:
        stmt = stmt.where(Genre.label.ilike(genre_label))

    return session.execute(stmt).scalar_one_or_none()


def find_active_tone_for_genre(
    session: Session,
    *,
    genre_id: str,
    tone_profile_id: str | None = None,
    tone_profile_slug: str | None = None,
    tone_profile_label: str | None = None,
) -> ToneProfile | None:
    selected_count = sum(
        value is not None
        for value in (tone_profile_id, tone_profile_slug, tone_profile_label)
    )
    if selected_count != 1:
        raise ValueError("exactly one tone selector is required")

    stmt: Select[tuple[ToneProfile]] = select(ToneProfile).where(
        ToneProfile.genre_id == genre_id,
        ToneProfile.is_active.is_(True),
    )

    if tone_profile_id is not None:
        stmt = stmt.where(ToneProfile.id == tone_profile_id)
    elif tone_profile_slug is not None:
        stmt = stmt.where(ToneProfile.slug == tone_profile_slug)
    else:
        stmt = stmt.where(ToneProfile.label.ilike(tone_profile_label))

    return session.execute(stmt).scalar_one_or_none()


def list_active_genres(session: Session) -> list[GenreCatalogEntry]:
    stmt: Select[tuple[Genre]] = (
        select(Genre)
        .where(Genre.is_active.is_(True))
        .order_by(Genre.sort_order.asc(), Genre.label.asc())
    )
    rows = session.execute(stmt).scalars().all()
    return [_build_genre_entry(row) for row in rows]


def list_active_tones_for_genre(
    session: Session,
    *,
    genre_slug: str | None = None,
    genre_id: str | None = None,
) -> list[ToneCatalogEntry]:
    if genre_slug is None and genre_id is None:
        raise ValueError("genre_slug or genre_id is required")

    stmt: Select[tuple[ToneProfile]] = (
        select(ToneProfile)
        .join(Genre, ToneProfile.genre_id == Genre.id)
        .where(ToneProfile.is_active.is_(True), Genre.is_active.is_(True))
        .order_by(ToneProfile.sort_order.asc(), ToneProfile.label.asc())
    )

    if genre_slug is not None:
        stmt = stmt.where(Genre.slug == genre_slug)

    if genre_id is not None:
        stmt = stmt.where(Genre.id == genre_id)

    rows = session.execute(stmt).scalars().all()
    return [_build_tone_entry(row) for row in rows]


def seed_catalog(
    session: Session,
    catalog: GenreToneCatalogDocument,
    *,
    commit: bool = True,
) -> CatalogSeedStats:
    existing_genres = {
        genre.slug: genre for genre in session.execute(select(Genre)).scalars().all()
    }
    stats = CatalogSeedStats()
    seen_genre_slugs: set[str] = set()

    for genre_index, genre_seed in enumerate(catalog.genres):
        genre, stats = _upsert_genre(
            session,
            genre_seed=genre_seed,
            genre_index=genre_index,
            existing_genres=existing_genres,
            stats=stats,
        )
        seen_genre_slugs.add(genre.slug)

        existing_tones = {tone.slug: tone for tone in genre.tone_profiles}
        seen_tone_slugs: set[str] = set()

        for tone_index, tone_seed in enumerate(genre_seed.tones):
            _tone, stats = _upsert_tone(
                genre=genre,
                tone_seed=tone_seed,
                tone_index=tone_index,
                existing_tones=existing_tones,
                stats=stats,
            )
            seen_tone_slugs.add(tone_seed.slug)

        for tone_slug, tone in existing_tones.items():
            if tone_slug in seen_tone_slugs:
                continue

            if tone.is_active:
                tone.is_active = False
                stats = CatalogSeedStats(
                    created_genres=stats.created_genres,
                    updated_genres=stats.updated_genres,
                    deactivated_genres=stats.deactivated_genres,
                    created_tones=stats.created_tones,
                    updated_tones=stats.updated_tones,
                    deactivated_tones=stats.deactivated_tones + 1,
                )

    for genre_slug, genre in existing_genres.items():
        if genre_slug in seen_genre_slugs:
            continue

        changed = False
        if genre.is_active:
            genre.is_active = False
            changed = True

        for tone in genre.tone_profiles:
            if tone.is_active:
                tone.is_active = False
                stats = CatalogSeedStats(
                    created_genres=stats.created_genres,
                    updated_genres=stats.updated_genres,
                    deactivated_genres=stats.deactivated_genres,
                    created_tones=stats.created_tones,
                    updated_tones=stats.updated_tones,
                    deactivated_tones=stats.deactivated_tones + 1,
                )

        if changed:
            stats = CatalogSeedStats(
                created_genres=stats.created_genres,
                updated_genres=stats.updated_genres,
                deactivated_genres=stats.deactivated_genres + 1,
                created_tones=stats.created_tones,
                updated_tones=stats.updated_tones,
                deactivated_tones=stats.deactivated_tones,
            )

    if commit:
        session.commit()
    else:
        session.flush()

    return stats


def _upsert_genre(
    session: Session,
    *,
    genre_seed: GenreCatalogSeed,
    genre_index: int,
    existing_genres: dict[str, Genre],
    stats: CatalogSeedStats,
) -> tuple[Genre, CatalogSeedStats]:
    genre = existing_genres.get(genre_seed.slug)
    created_genres = stats.created_genres
    updated_genres = stats.updated_genres

    if genre is None:
        genre = Genre(slug=genre_seed.slug)
        session.add(genre)
        existing_genres[genre_seed.slug] = genre
        created_genres += 1
    else:
        updated_genres += 1

    genre.label = genre_seed.label
    genre.description = genre_seed.description
    genre.bedtime_safety_notes = genre_seed.bedtime_safety_notes
    genre.arc_notes = genre_seed.arc_notes
    genre.sort_order = genre_index
    genre.is_active = genre_seed.is_active

    session.flush()

    return genre, CatalogSeedStats(
        created_genres=created_genres,
        updated_genres=updated_genres,
        deactivated_genres=stats.deactivated_genres,
        created_tones=stats.created_tones,
        updated_tones=stats.updated_tones,
        deactivated_tones=stats.deactivated_tones,
    )


def _upsert_tone(
    *,
    genre: Genre,
    tone_seed: ToneCatalogSeed,
    tone_index: int,
    existing_tones: dict[str, ToneProfile],
    stats: CatalogSeedStats,
) -> tuple[ToneProfile, CatalogSeedStats]:
    tone = existing_tones.get(tone_seed.slug)
    created_tones = stats.created_tones
    updated_tones = stats.updated_tones

    if tone is None:
        tone = ToneProfile(slug=tone_seed.slug)
        genre.tone_profiles.append(tone)
        existing_tones[tone_seed.slug] = tone
        created_tones += 1
    else:
        updated_tones += 1

    tone.label = tone_seed.label
    tone.description = tone_seed.description
    tone.bedtime_notes = tone_seed.bedtime_notes
    tone.descriptors = tone_seed.descriptors
    tone.default_planning_hints = tone_seed.default_planning_hints
    tone.sort_order = tone_index
    tone.is_active = tone_seed.is_active

    return tone, CatalogSeedStats(
        created_genres=stats.created_genres,
        updated_genres=stats.updated_genres,
        deactivated_genres=stats.deactivated_genres,
        created_tones=created_tones,
        updated_tones=updated_tones,
        deactivated_tones=stats.deactivated_tones,
    )
