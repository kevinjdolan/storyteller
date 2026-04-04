from __future__ import annotations

from collections.abc import Iterator

from fastapi import Request
from sqlalchemy.orm import Session

from app.ai import (
    BeatSheetGenerationAdapter,
    BriefNormalizationAdapter,
    CharacterGenerationAdapter,
    GeminiBeatSheetGenerationAdapter,
    GeminiBriefNormalizationAdapter,
    GeminiCharacterGenerationAdapter,
    GeminiIntentParserAdapter,
    GeminiPitchGenerationAdapter,
    IntentParserAdapter,
    PitchGenerationAdapter,
)
from app.db.session import get_session_factory
from app.settings import AppSettings, get_settings
from app.storage import ObjectStorageService, build_object_storage_service


def get_db_session() -> Iterator[Session]:
    session = get_session_factory()()

    try:
        yield session
    finally:
        session.close()


def get_app_settings(request: Request) -> AppSettings:
    settings = getattr(request.app.state, "settings", None)
    if settings is None:
        settings = get_settings()
    return settings


def get_object_storage_service(request: Request) -> ObjectStorageService:
    object_storage = getattr(request.app.state, "object_storage", None)
    if object_storage is None:
        object_storage = build_object_storage_service(get_app_settings(request))
        request.app.state.object_storage = object_storage
    return object_storage


def get_intent_parser_adapter(request: Request) -> IntentParserAdapter:
    adapter = getattr(request.app.state, "intent_parser_adapter", None)
    if adapter is None:
        settings = get_app_settings(request)
        adapter = GeminiIntentParserAdapter(
            credential=settings.gemini_api_key,
            model_id=settings.gemini.planning_model,
        )
        request.app.state.intent_parser_adapter = adapter

    return adapter


def get_brief_normalization_adapter(request: Request) -> BriefNormalizationAdapter:
    adapter = getattr(request.app.state, "brief_normalization_adapter", None)
    if adapter is None:
        settings = get_app_settings(request)
        adapter = GeminiBriefNormalizationAdapter(
            credential=settings.gemini_api_key,
            model_id=settings.gemini.planning_model,
        )
        request.app.state.brief_normalization_adapter = adapter

    return adapter


def get_beat_sheet_generation_adapter(request: Request) -> BeatSheetGenerationAdapter:
    adapter = getattr(request.app.state, "beat_sheet_generation_adapter", None)
    if adapter is None:
        settings = get_app_settings(request)
        adapter = GeminiBeatSheetGenerationAdapter(
            credential=settings.gemini_api_key,
            model_id=settings.gemini.planning_model,
        )
        request.app.state.beat_sheet_generation_adapter = adapter

    return adapter


def get_pitch_generation_adapter(request: Request) -> PitchGenerationAdapter:
    adapter = getattr(request.app.state, "pitch_generation_adapter", None)
    if adapter is None:
        settings = get_app_settings(request)
        adapter = GeminiPitchGenerationAdapter(
            credential=settings.gemini_api_key,
            model_id=settings.gemini.planning_model,
        )
        request.app.state.pitch_generation_adapter = adapter

    return adapter


def get_character_generation_adapter(request: Request) -> CharacterGenerationAdapter:
    adapter = getattr(request.app.state, "character_generation_adapter", None)
    if adapter is None:
        settings = get_app_settings(request)
        adapter = GeminiCharacterGenerationAdapter(
            credential=settings.gemini_api_key,
            model_id=settings.gemini.planning_model,
        )
        request.app.state.character_generation_adapter = adapter

    return adapter
