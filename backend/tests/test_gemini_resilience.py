from __future__ import annotations

import httpx
from app.ai.gemini_resilience import (
    GeminiFailureKind,
    GeminiRetryNotice,
    GeminiRetryPolicy,
    classify_gemini_exception,
    execute_with_retry,
)


def _build_status_error(
    status_code: int,
    *,
    payload: dict[str, object],
    headers: dict[str, str] | None = None,
) -> httpx.HTTPStatusError:
    request = httpx.Request(
        "POST",
        "https://generativelanguage.googleapis.com/v1beta/models/test:generateContent",
    )
    response = httpx.Response(
        status_code,
        request=request,
        json=payload,
        headers=headers,
    )
    return httpx.HTTPStatusError(
        f"{status_code} failure",
        request=request,
        response=response,
    )


def test_classify_gemini_exception_marks_generic_429_as_retryable_rate_limit() -> None:
    detail = classify_gemini_exception(
        _build_status_error(
            429,
            payload={
                "error": {
                    "status": "RESOURCE_EXHAUSTED",
                    "message": "Rate limit hit for requests per minute.",
                }
            },
            headers={"retry-after": "2.5"},
        ),
        operation_name="pitch generation",
    )

    assert detail.kind == GeminiFailureKind.RATE_LIMITED
    assert detail.retryable is True
    assert detail.user_action_required is False
    assert detail.retry_after_seconds == 2.5


def test_classify_gemini_exception_marks_quota_exhaustion_as_user_actionable() -> None:
    detail = classify_gemini_exception(
        _build_status_error(
            429,
            payload={
                "error": {
                    "status": "RESOURCE_EXHAUSTED",
                    "message": (
                        "You exceeded your current quota. Check plan and billing details."
                    ),
                }
            },
        ),
        operation_name="beat sheet generation",
    )

    assert detail.kind == GeminiFailureKind.QUOTA_EXHAUSTED
    assert detail.retryable is False
    assert detail.user_action_required is True


def test_execute_with_retry_retries_transport_failures_and_emits_notices() -> None:
    notices: list[GeminiRetryNotice] = []
    sleeps: list[float] = []
    request = httpx.Request(
        "POST",
        "https://generativelanguage.googleapis.com/v1beta/models/test:generateContent",
    )
    attempts = {"count": 0}

    def operation() -> str:
        attempts["count"] += 1
        if attempts["count"] < 3:
            raise httpx.ReadTimeout("provider timed out", request=request)
        return "ok"

    result = execute_with_retry(
        operation,
        policy=GeminiRetryPolicy(
            max_attempts=3,
            initial_backoff_seconds=0.5,
            max_backoff_seconds=2.0,
        ),
        classify_exception=lambda exc: classify_gemini_exception(
            exc,
            operation_name="composition segment generation",
        ),
        on_retry=notices.append,
        sleep_func=sleeps.append,
    )

    assert result.value == "ok"
    assert result.attempts_used == 3
    assert sleeps == [0.5, 1.0]
    assert [(notice.failed_attempt, notice.next_attempt) for notice in notices] == [
        (1, 2),
        (2, 3),
    ]
    assert all(
        notice.failure.kind == GeminiFailureKind.TRANSPORT and notice.failure.retryable
        for notice in notices
    )
