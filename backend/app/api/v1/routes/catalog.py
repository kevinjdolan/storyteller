from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies import get_db_session
from app.models import GenreCatalogEntry
from app.services.catalog import list_active_genres

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
