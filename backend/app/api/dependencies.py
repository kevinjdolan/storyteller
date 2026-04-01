from __future__ import annotations

from collections.abc import Iterator

from fastapi import Request
from sqlalchemy.orm import Session

from app.ai import GeminiIntentParserAdapter, IntentParserAdapter
from app.db.session import get_session_factory
from app.settings import AppSettings, get_settings


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
