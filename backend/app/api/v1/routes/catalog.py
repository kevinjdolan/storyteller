from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_db_session
from app.models import GenreCatalogEntry, ToneCatalogEntry
from app.services.catalog import find_active_genre, list_active_genres, list_active_tones_for_genre

router = APIRouter(prefix="/catalog", tags=["catalog"])


@router.get(
    "/genres",
    response_model=list[GenreCatalogEntry],
    summary="List the active bedtime story genres",
)
def get_genre_catalog(
    db_session: Annotated[Session, Depends(get_db_session)],
) -> list[GenreCatalogEntry]:
    return list_active_genres(db_session)


@router.get(
    "/genres/{genre_slug}/tones",
    response_model=list[ToneCatalogEntry],
    summary="List the active tone profiles for a specific bedtime story genre",
)
def get_tone_catalog_for_genre(
    genre_slug: str,
    db_session: Annotated[Session, Depends(get_db_session)],
) -> list[ToneCatalogEntry]:
    if find_active_genre(db_session, genre_slug=genre_slug) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"no active genre matched {genre_slug!r}",
        )

    return list_active_tones_for_genre(db_session, genre_slug=genre_slug)
