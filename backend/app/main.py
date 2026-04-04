from __future__ import annotations

import logging
from contextlib import asynccontextmanager
from time import perf_counter
from typing import AsyncIterator

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import router as api_router
from app.api.v1.router import router as api_v1_router
from app.models.identity import LOCAL_DEVELOPMENT_IDENTITY
from app.observability import (
    REQUEST_ID_HEADER,
    clear_log_context,
    configure_structured_logging,
    log_event,
    new_request_id,
    update_log_context,
)
from app.settings import AppSettings, SettingsValidationError, get_settings
from app.storage import build_object_storage_service

logger = logging.getLogger(__name__)


def configure_logging(settings: AppSettings) -> None:
    configure_structured_logging(settings.log_level)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    settings = get_settings()
    configure_logging(settings)
    object_storage = build_object_storage_service(settings)
    app.state.settings = settings
    app.state.object_storage = object_storage
    app.state.storage_paths = object_storage.paths
    app.state.request_identity = LOCAL_DEVELOPMENT_IDENTITY

    log_event(
        logger,
        logging.INFO,
        "app.lifecycle.started",
        "Application startup completed.",
        app_name=settings.app_name,
        environment=settings.environment,
        host=settings.host,
        port=settings.port,
    )

    try:
        yield
    finally:
        brief_normalization_adapter = getattr(app.state, "brief_normalization_adapter", None)
        if brief_normalization_adapter is not None:
            brief_normalization_adapter.close()
        intent_parser_adapter = getattr(app.state, "intent_parser_adapter", None)
        if intent_parser_adapter is not None:
            intent_parser_adapter.close()
        pitch_generation_adapter = getattr(app.state, "pitch_generation_adapter", None)
        if pitch_generation_adapter is not None:
            pitch_generation_adapter.close()
        object_storage.close()
        log_event(
            logger,
            logging.INFO,
            "app.lifecycle.stopped",
            "Application shutdown completed.",
            app_name=settings.app_name,
        )


def create_app() -> FastAPI:
    try:
        settings = get_settings()
    except SettingsValidationError as exc:
        raise SystemExit(exc.format_for_cli()) from None

    docs_enabled = settings.feature_flags.enable_api_docs

    app = FastAPI(
        title=settings.app_name,
        version=settings.version,
        lifespan=lifespan,
        docs_url="/docs" if docs_enabled else None,
        redoc_url="/redoc" if docs_enabled else None,
        openapi_url="/openapi.json" if docs_enabled else None,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=list(settings.cors_allowed_origins),
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.middleware("http")
    async def request_logging_middleware(
        request: Request,
        call_next,
    ) -> Response:
        request_id = request.headers.get(REQUEST_ID_HEADER) or new_request_id()
        request.state.request_id = request_id
        update_log_context(request_id=request_id)
        started_at = perf_counter()

        log_event(
            logger,
            logging.INFO,
            "http.request.started",
            "HTTP request started.",
            http_method=request.method,
            path=request.url.path,
        )

        try:
            response = await call_next(request)
        except Exception:
            resolved_session_id = request.path_params.get("session_id")
            if resolved_session_id:
                update_log_context(session_id=resolved_session_id)
            log_event(
                logger,
                logging.ERROR,
                "http.request.failed",
                "HTTP request failed.",
                http_method=request.method,
                path=request.url.path,
                duration_ms=max(round((perf_counter() - started_at) * 1000), 0),
            )
            clear_log_context()
            raise

        resolved_session_id = request.path_params.get("session_id")
        if resolved_session_id:
            update_log_context(session_id=resolved_session_id)
        response.headers[REQUEST_ID_HEADER] = request_id
        log_event(
            logger,
            logging.INFO,
            "http.request.completed",
            "HTTP request completed.",
            http_method=request.method,
            path=request.url.path,
            status_code=response.status_code,
            duration_ms=max(round((perf_counter() - started_at) * 1000), 0),
        )
        clear_log_context()
        return response

    app.include_router(api_router)
    app.include_router(api_v1_router, prefix=settings.api_v1_prefix)

    return app


app = create_app()
