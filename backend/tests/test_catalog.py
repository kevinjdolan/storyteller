from __future__ import annotations

import pytest
from app.db import Base, Genre, ToneProfile, make_engine
from app.models import GenreCatalogSeed, GenreToneCatalogDocument
from app.services.catalog import (
    CATALOG_FILE_PATH,
    list_active_genres,
    list_active_tones_for_genre,
    load_catalog_document,
    seed_catalog,
)
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker


def _enable_sqlite_foreign_keys(engine) -> None:
    with engine.begin() as connection:
        connection.exec_driver_sql("PRAGMA foreign_keys=ON")


def _make_session():
    engine = make_engine("sqlite+pysqlite:///:memory:")
    _enable_sqlite_foreign_keys(engine)
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)()


def test_catalog_document_loads_seeded_genres_and_tones() -> None:
    catalog = load_catalog_document(CATALOG_FILE_PATH)

    assert [genre.slug for genre in catalog.genres] == [
        "quest-fantasy",
        "gentle-mystery",
        "cozy-animal-adventure",
        "magical-friendship",
        "dreamworld-voyage",
        "soft-science-wonder",
    ]
    assert all(len(genre.tones) == 3 for genre in catalog.genres)
    assert catalog.genres[0].tones[0].slug == "hushed-wonder"


def test_seed_catalog_is_idempotent_and_genre_filtered() -> None:
    catalog = load_catalog_document(CATALOG_FILE_PATH)
    total_tones = sum(len(genre.tones) for genre in catalog.genres)
    session = _make_session()

    try:
        first = seed_catalog(session, catalog)
        second = seed_catalog(session, catalog)

        assert first.created_genres == len(catalog.genres)
        assert first.created_tones == total_tones
        assert second.created_genres == 0
        assert second.created_tones == 0
        assert second.updated_genres == len(catalog.genres)
        assert second.updated_tones == total_tones

        genres = list_active_genres(session)
        tones = list_active_tones_for_genre(session, genre_slug="quest-fantasy")

        assert [genre.slug for genre in genres] == [genre.slug for genre in catalog.genres]
        assert [tone.slug for tone in tones] == [
            "hushed-wonder",
            "lantern-brave",
            "fireside-reassurance",
        ]
        assert tones[0].default_planning_hints["pacing"] == "unhurried"
        assert set(tones[1].descriptors) == {
            "steady",
            "reassuring",
            "warmhearted",
            "lightly adventurous",
        }
    finally:
        session.close()


def test_seed_catalog_deactivates_rows_removed_from_source() -> None:
    catalog = load_catalog_document(CATALOG_FILE_PATH)
    trimmed = GenreToneCatalogDocument(
        genres=[
            catalog.genres[0].model_copy(
                deep=True,
                update={"tones": catalog.genres[0].tones[:2]},
            ),
            *catalog.genres[1:5],
        ]
    )
    session = _make_session()

    try:
        seed_catalog(session, catalog)
        stats = seed_catalog(session, trimmed)

        removed_genre = session.execute(
            select(Genre).where(Genre.slug == "soft-science-wonder")
        ).scalar_one()
        removed_tone = session.execute(
            select(ToneProfile).where(ToneProfile.slug == "fireside-reassurance")
        ).scalar_one()

        assert removed_genre.is_active is False
        assert removed_tone.is_active is False
        assert stats.deactivated_genres == 1
        assert stats.deactivated_tones >= 1
    finally:
        session.close()


def test_seed_document_rejects_duplicate_tone_slugs() -> None:
    duplicated_tone = load_catalog_document(CATALOG_FILE_PATH).genres[0].tones[0]

    with pytest.raises(ValueError, match="duplicate tone slug"):
        GenreCatalogSeed(
            slug="duplicate-test",
            label="Duplicate Test",
            description="A temporary test genre.",
            bedtime_safety_notes="Keep it calm.",
            arc_notes={"core_arc": "test"},
            tones=[duplicated_tone, duplicated_tone.model_copy(deep=True)],
        )
