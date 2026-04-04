from __future__ import annotations

import json
import logging
import sys
from contextlib import contextmanager
from contextvars import ContextVar, Token
from datetime import date, datetime, time, timezone
from enum import Enum
from typing import Any, Iterator, Mapping
from uuid import uuid4

REQUEST_ID_HEADER = "X-Request-ID"
_STRUCTURED_HANDLER_NAME = "storyteller-structured-json"
_LOG_CONTEXT: ContextVar[dict[str, Any]] = ContextVar("storyteller_log_context", default={})


def configure_structured_logging(level_name: str) -> None:
    normalized_level = getattr(logging, str(level_name).upper(), logging.INFO)
    root_logger = logging.getLogger()
    root_logger.setLevel(normalized_level)

    preserved_handlers = [
        handler
        for handler in root_logger.handlers
        if handler.__class__.__module__.startswith("_pytest.logging")
    ]
    root_logger.handlers = preserved_handlers
    for handler in preserved_handlers:
        _attach_context_filter(handler)

    handler = logging.StreamHandler(sys.stdout)
    handler.set_name(_STRUCTURED_HANDLER_NAME)
    handler.setLevel(normalized_level)
    handler.setFormatter(StructuredJsonFormatter())
    _attach_context_filter(handler)
    root_logger.addHandler(handler)


def new_request_id() -> str:
    return f"req-{uuid4().hex}"


def get_log_context() -> dict[str, Any]:
    return dict(_LOG_CONTEXT.get())


def update_log_context(**fields: Any) -> dict[str, Any]:
    current = get_log_context()
    for key, value in fields.items():
        if value is None:
            current.pop(key, None)
            continue
        current[key] = value
    _LOG_CONTEXT.set(current)
    return current


def clear_log_context() -> None:
    _LOG_CONTEXT.set({})


def push_log_context(**fields: Any) -> Token[dict[str, Any]]:
    merged = {**get_log_context(), **{k: v for k, v in fields.items() if v is not None}}
    return _LOG_CONTEXT.set(merged)


def pop_log_context(token: Token[dict[str, Any]]) -> None:
    _LOG_CONTEXT.reset(token)


@contextmanager
def bound_log_context(**fields: Any) -> Iterator[dict[str, Any]]:
    token = push_log_context(**fields)
    try:
        yield get_log_context()
    finally:
        pop_log_context(token)


def log_event(
    logger: logging.Logger,
    level: int,
    event: str,
    message: str,
    **fields: Any,
) -> None:
    merged_fields = get_log_context()
    merged_fields.update({key: value for key, value in fields.items() if value is not None})
    logger.log(
        level,
        message,
        extra={
            "event": event,
            "event_fields": merged_fields,
        },
    )


class StructuredJsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        payload: dict[str, Any] = {
            "timestamp": datetime.fromtimestamp(
                record.created,
                tz=timezone.utc,
            )
            .isoformat(timespec="milliseconds")
            .replace("+00:00", "Z"),
            "level": record.levelname,
            "logger": record.name,
            "event": getattr(record, "event", record.name),
            "message": record.getMessage(),
        }
        fields = getattr(record, "log_context_fields", {})
        if isinstance(fields, Mapping):
            payload.update({key: _serialize_log_value(value) for key, value in fields.items()})
        if record.exc_info:
            payload["exception"] = self.formatException(record.exc_info)
        return json.dumps(payload, ensure_ascii=True, sort_keys=True)


class _ContextEnrichingFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        context_fields = get_log_context()
        event_fields = getattr(record, "event_fields", {})
        merged_fields: dict[str, Any] = {}
        if isinstance(context_fields, Mapping):
            merged_fields.update(context_fields)
        if isinstance(event_fields, Mapping):
            merged_fields.update(event_fields)
        record.log_context_fields = merged_fields
        return True


def _attach_context_filter(handler: logging.Handler) -> None:
    handler.filters = [
        existing
        for existing in handler.filters
        if not isinstance(existing, _ContextEnrichingFilter)
    ]
    handler.addFilter(_ContextEnrichingFilter())


def _serialize_log_value(value: Any) -> Any:
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, datetime):
        if value.tzinfo is None:
            return value.isoformat(timespec="seconds")
        return (
            value.astimezone(timezone.utc)
            .isoformat(timespec="seconds")
            .replace(
                "+00:00",
                "Z",
            )
        )
    if isinstance(value, (date, time)):
        return value.isoformat()
    if isinstance(value, Mapping):
        return {str(key): _serialize_log_value(item) for key, item in value.items()}
    if isinstance(value, (list, tuple, set, frozenset)):
        return [_serialize_log_value(item) for item in value]
    return str(value)
