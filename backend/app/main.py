from __future__ import annotations

import logging
from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import router as api_router
from app.api.v1.router import router as api_v1_router
from app.settings import AppSettings, SettingsValidationError, get_settings
from app.storage import build_object_storage_service

logger = logging.getLogger(__name__)


def configure_logging(settings: AppSettings) -> None:
    logging.basicConfig(
        level=getattr(logging, settings.log_level, logging.INFO),
        format="%(levelname)s %(name)s %(message)s",
    )


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    settings = get_settings()
    configure_logging(settings)
    object_storage = build_object_storage_service(settings)
    app.state.settings = settings
    app.state.object_storage = object_storage
    app.state.storage_paths = object_storage.paths

    logger.info(
        "Starting %s in %s mode on %s:%s",
        settings.app_name,
        settings.environment,
        settings.host,
        settings.port,
    )

    try:
        yield
    finally:
        object_storage.close()
        logger.info("Stopping %s", settings.app_name)


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

    app.include_router(api_router)
    app.include_router(api_v1_router, prefix=settings.api_v1_prefix)

    return app


app = create_app()
