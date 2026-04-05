from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from enum import Enum
from time import sleep as default_sleep
from typing import Any, Callable, Generic, Mapping, TypeVar

import httpx

T = TypeVar("T")


class GeminiFailureKind(str, Enum):
    RATE_LIMITED = "rate_limited"
    QUOTA_EXHAUSTED = "quota_exhausted"
    TRANSIENT = "transient"
    TRANSPORT = "transport"
    INVALID_REQUEST = "invalid_request"
    AUTHENTICATION = "authentication"
    BLOCKED = "blocked"
    INVALID_RESPONSE = "invalid_response"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class GeminiFailureDetail:
    kind: GeminiFailureKind
    message: str
    retryable: bool
    user_action_required: bool
    status_code: int | None = None
    provider_status: str | None = None
    provider_message: str | None = None
    retry_after_seconds: float | None = None

    def to_metadata(self) -> dict[str, Any]:
        return {
            "kind": self.kind.value,
            "message": self.message,
            "retryable": self.retryable,
            "user_action_required": self.user_action_required,
            "status_code": self.status_code,
            "provider_status": self.provider_status,
            "provider_message": self.provider_message,
            "retry_after_seconds": self.retry_after_seconds,
        }


@dataclass(frozen=True)
class GeminiRetryPolicy:
    max_attempts: int
    initial_backoff_seconds: float
    max_backoff_seconds: float

    def __post_init__(self) -> None:
        if self.max_attempts < 1:
            raise ValueError("max_attempts must be at least 1")
        if self.initial_backoff_seconds < 0:
            raise ValueError("initial_backoff_seconds must not be negative")
        if self.max_backoff_seconds < self.initial_backoff_seconds:
            raise ValueError(
                "max_backoff_seconds must be greater than or equal to initial_backoff_seconds",
            )


@dataclass(frozen=True)
class GeminiRetryNotice:
    failure: GeminiFailureDetail
    failed_attempt: int
    next_attempt: int
    max_attempts: int
    delay_seconds: float


@dataclass(frozen=True)
class RetryExecutionResult(Generic[T]):
    value: T
    attempts_used: int


DEFAULT_GEMINI_PLANNING_RETRY_POLICY = GeminiRetryPolicy(
    max_attempts=3,
    initial_backoff_seconds=0.75,
    max_backoff_seconds=4.0,
)
DEFAULT_GEMINI_COMPOSITION_RETRY_POLICY = GeminiRetryPolicy(
    max_attempts=3,
    initial_backoff_seconds=1.0,
    max_backoff_seconds=6.0,
)
DEFAULT_GEMINI_AUDIO_RETRY_POLICY = GeminiRetryPolicy(
    max_attempts=4,
    initial_backoff_seconds=1.0,
    max_backoff_seconds=8.0,
)

_QUOTA_HINTS = (
    "billing",
    "daily limit",
    "exceeded your current quota",
    "free tier",
    "insufficient credits",
    "monthly limit",
    "out of credits",
    "per day",
    "plan and billing",
    "quota",
    "quota metric",
)


def build_blocked_failure(
    *,
    operation_name: str,
    blocked_reason: str,
) -> GeminiFailureDetail:
    normalized_reason = blocked_reason.strip() or "blocked"
    return GeminiFailureDetail(
        kind=GeminiFailureKind.BLOCKED,
        message=(
            f"Gemini blocked the {operation_name} request "
            f"({normalized_reason}). Adjust the prompt or source content and try again."
        ),
        retryable=False,
        user_action_required=True,
        provider_status=normalized_reason,
    )


def build_invalid_response_failure(
    *,
    operation_name: str,
    detail: str,
) -> GeminiFailureDetail:
    normalized_detail = detail.strip()
    return GeminiFailureDetail(
        kind=GeminiFailureKind.INVALID_RESPONSE,
        message=(
            f"Gemini returned an invalid {operation_name} response"
            + (f": {normalized_detail}" if normalized_detail else ".")
        ),
        retryable=True,
        user_action_required=False,
        provider_message=normalized_detail or None,
    )


def classify_gemini_exception(
    exc: Exception,
    *,
    operation_name: str,
) -> GeminiFailureDetail:
    existing = getattr(exc, "failure_detail", None)
    if isinstance(existing, GeminiFailureDetail):
        return existing

    if isinstance(exc, httpx.HTTPStatusError):
        return _classify_http_status_error(exc, operation_name=operation_name)

    if isinstance(exc, (httpx.TimeoutException, httpx.NetworkError)):
        detail = str(exc).strip() or exc.__class__.__name__
        return GeminiFailureDetail(
            kind=GeminiFailureKind.TRANSPORT,
            message=(
                f"Gemini {operation_name} could not reach the provider network reliably: {detail}"
            ),
            retryable=True,
            user_action_required=False,
            provider_message=detail,
        )

    detail = str(exc).strip() or exc.__class__.__name__
    return GeminiFailureDetail(
        kind=GeminiFailureKind.UNKNOWN,
        message=f"Gemini {operation_name} failed: {detail}",
        retryable=False,
        user_action_required=False,
        provider_message=detail,
    )


def execute_with_retry(
    operation: Callable[[], T],
    *,
    policy: GeminiRetryPolicy,
    classify_exception: Callable[[Exception], GeminiFailureDetail],
    on_retry: Callable[[GeminiRetryNotice], None] | None = None,
    sleep_func: Callable[[float], None] = default_sleep,
) -> RetryExecutionResult[T]:
    for failed_attempt in range(1, policy.max_attempts + 1):
        try:
            return RetryExecutionResult(value=operation(), attempts_used=failed_attempt)
        except Exception as exc:
            failure = classify_exception(exc)
            if not failure.retryable or failed_attempt >= policy.max_attempts:
                raise

            delay_seconds = _compute_retry_delay(
                policy=policy,
                failure=failure,
                failed_attempt=failed_attempt,
            )
            if on_retry is not None:
                on_retry(
                    GeminiRetryNotice(
                        failure=failure,
                        failed_attempt=failed_attempt,
                        next_attempt=failed_attempt + 1,
                        max_attempts=policy.max_attempts,
                        delay_seconds=delay_seconds,
                    )
                )
            if delay_seconds > 0:
                sleep_func(delay_seconds)

    raise RuntimeError("retry loop exited without returning or raising")


def safe_json_payload(response: httpx.Response) -> Mapping[str, Any] | list[Any] | str | None:
    try:
        return response.json()
    except ValueError:
        body = response.text.strip()
        return body or None


def _classify_http_status_error(
    exc: httpx.HTTPStatusError,
    *,
    operation_name: str,
) -> GeminiFailureDetail:
    response = exc.response
    payload = safe_json_payload(response)
    provider_status, provider_message = _extract_provider_error(payload)
    status_code = response.status_code
    retry_after_seconds = _parse_retry_after_seconds(response.headers.get("retry-after"))
    haystack = " ".join(
        part for part in (provider_status, provider_message, str(payload)) if part
    ).lower()

    if status_code == 429:
        if any(hint in haystack for hint in _QUOTA_HINTS):
            return GeminiFailureDetail(
                kind=GeminiFailureKind.QUOTA_EXHAUSTED,
                message=(
                    f"Gemini {operation_name} quota is exhausted. "
                    "Wait for quota to reset or increase the available allowance before retrying."
                ),
                retryable=False,
                user_action_required=True,
                status_code=status_code,
                provider_status=provider_status,
                provider_message=provider_message,
                retry_after_seconds=retry_after_seconds,
            )
        return GeminiFailureDetail(
            kind=GeminiFailureKind.RATE_LIMITED,
            message=(
                f"Gemini {operation_name} hit a temporary rate limit. "
                "Retrying after a short backoff may succeed."
            ),
            retryable=True,
            user_action_required=False,
            status_code=status_code,
            provider_status=provider_status,
            provider_message=provider_message,
            retry_after_seconds=retry_after_seconds,
        )

    if status_code in {500, 502, 503, 504}:
        return GeminiFailureDetail(
            kind=GeminiFailureKind.TRANSIENT,
            message=(
                f"Gemini {operation_name} is temporarily unavailable. "
                "Retrying after a short backoff may succeed."
            ),
            retryable=True,
            user_action_required=False,
            status_code=status_code,
            provider_status=provider_status,
            provider_message=provider_message,
            retry_after_seconds=retry_after_seconds,
        )

    if status_code in {401, 403}:
        return GeminiFailureDetail(
            kind=GeminiFailureKind.AUTHENTICATION,
            message=(
                f"Gemini rejected the {operation_name} credentials or permissions. "
                "Update the backend API key or provider access and try again."
            ),
            retryable=False,
            user_action_required=True,
            status_code=status_code,
            provider_status=provider_status,
            provider_message=provider_message,
            retry_after_seconds=retry_after_seconds,
        )

    if status_code in {400, 404}:
        return GeminiFailureDetail(
            kind=GeminiFailureKind.INVALID_REQUEST,
            message=(
                f"Gemini rejected the {operation_name} request as invalid. "
                "Update the request inputs or settings before retrying."
            ),
            retryable=False,
            user_action_required=True,
            status_code=status_code,
            provider_status=provider_status,
            provider_message=provider_message,
            retry_after_seconds=retry_after_seconds,
        )

    return GeminiFailureDetail(
        kind=GeminiFailureKind.UNKNOWN,
        message=(
            f"Gemini {operation_name} failed with status {status_code}. "
            "Retrying is disabled because the provider did not classify the error as transient."
        ),
        retryable=False,
        user_action_required=False,
        status_code=status_code,
        provider_status=provider_status,
        provider_message=provider_message,
        retry_after_seconds=retry_after_seconds,
    )


def _compute_retry_delay(
    *,
    policy: GeminiRetryPolicy,
    failure: GeminiFailureDetail,
    failed_attempt: int,
) -> float:
    backoff_seconds = policy.initial_backoff_seconds * (2 ** (failed_attempt - 1))
    backoff_seconds = min(backoff_seconds, policy.max_backoff_seconds)
    if failure.retry_after_seconds is not None:
        backoff_seconds = max(backoff_seconds, failure.retry_after_seconds)
    return max(backoff_seconds, 0.0)


def _extract_provider_error(
    payload: Mapping[str, Any] | list[Any] | str | None,
) -> tuple[str | None, str | None]:
    if not isinstance(payload, Mapping):
        return None, None

    error_payload = payload.get("error")
    if not isinstance(error_payload, Mapping):
        return None, None

    provider_status = error_payload.get("status")
    provider_message = error_payload.get("message")
    normalized_status = str(provider_status).strip() if provider_status is not None else None
    normalized_message = str(provider_message).strip() if provider_message is not None else None
    return (
        normalized_status or None,
        normalized_message or None,
    )


def _parse_retry_after_seconds(value: str | None) -> float | None:
    if value is None:
        return None

    normalized = value.strip()
    if not normalized:
        return None

    try:
        return max(float(normalized), 0.0)
    except ValueError:
        try:
            retry_at = parsedate_to_datetime(normalized)
        except (TypeError, ValueError):
            return None
        if retry_at.tzinfo is None:
            retry_at = retry_at.replace(tzinfo=timezone.utc)
        return max((retry_at - datetime.now(timezone.utc)).total_seconds(), 0.0)
