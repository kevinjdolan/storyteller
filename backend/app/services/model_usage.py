from __future__ import annotations

import logging
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Mapping

from sqlalchemy.orm import Session

from app.db import ModelUsageEvent, SessionUsageRollup, utc_now
from app.models.model_usage import (
    ModelCallOutcome,
    ModelTokenUsageView,
    ModelUsageBucket,
    SessionUsageBucketSummaryView,
    SessionUsageDiagnosticsView,
    SessionUsageEventView,
    SessionUsageStageBreakdownView,
    SessionUsageSummaryView,
)
from app.models.workflow import WorkflowStage
from app.observability import log_event
from app.repositories import ModelUsageRepository
from app.settings import AppSettings, get_settings

logger = logging.getLogger(__name__)
_DEFAULT_USAGE_BUCKETS = (
    ModelUsageBucket.PLANNING,
    ModelUsageBucket.COMPOSITION,
    ModelUsageBucket.AUDIO,
)


@dataclass(frozen=True)
class ModelUsageContext:
    session_id: str
    usage_bucket: ModelUsageBucket
    purpose: str
    model_id: str
    workflow_stage: WorkflowStage | None = None
    prompt_version: str | None = None
    provider: str = "gemini"


class SessionModelUsageService:
    def __init__(
        self,
        session: Session,
        *,
        settings: AppSettings | None = None,
    ) -> None:
        self._session = session
        self._settings = settings or get_settings()
        self._usage = ModelUsageRepository(session)

    def record_model_call(
        self,
        *,
        context: ModelUsageContext,
        elapsed_ms: int,
        outcome: ModelCallOutcome,
        raw_response: Mapping[str, Any] | list[Any] | str | None = None,
        error_message: str | None = None,
    ) -> ModelUsageEvent:
        token_usage = extract_gemini_token_usage(raw_response)
        approximate_cost_usd = estimate_approximate_cost_usd(
            settings=self._settings,
            usage_bucket=context.usage_bucket,
            token_usage=token_usage,
        )
        now = utc_now()
        event = self._usage.create_event(
            session_id=context.session_id,
            usage_bucket=context.usage_bucket.value,
            workflow_stage=context.workflow_stage,
            purpose=context.purpose,
            provider=context.provider,
            model_id=context.model_id,
            prompt_version=context.prompt_version,
            outcome=outcome.value,
            elapsed_ms=max(int(elapsed_ms), 0),
            input_tokens=token_usage.input_tokens,
            output_tokens=token_usage.output_tokens,
            total_tokens=token_usage.total_tokens,
            cached_input_tokens=token_usage.cached_input_tokens,
            thought_tokens=token_usage.thought_tokens,
            approximate_cost_usd=approximate_cost_usd,
            error_message=_normalize_error_message(error_message),
            created_at=now,
        )

        rollup = self._usage.get_rollup(context.session_id, context.usage_bucket.value)
        if rollup is None:
            rollup = self._usage.create_rollup(
                session_id=context.session_id,
                usage_bucket=context.usage_bucket.value,
            )
        _apply_rollup_update(
            rollup,
            context=context,
            elapsed_ms=max(int(elapsed_ms), 0),
            outcome=outcome,
            token_usage=token_usage,
            approximate_cost_usd=approximate_cost_usd,
            now=now,
        )

        log_event(
            logger,
            logging.INFO,
            "model.usage.recorded",
            "Recorded model usage diagnostics.",
            session_id=context.session_id,
            usage_bucket=context.usage_bucket.value,
            workflow_stage=(
                context.workflow_stage.value if context.workflow_stage is not None else None
            ),
            purpose=context.purpose,
            provider=context.provider,
            model_id=context.model_id,
            outcome=outcome.value,
            elapsed_ms=max(int(elapsed_ms), 0),
            input_tokens=token_usage.input_tokens,
            output_tokens=token_usage.output_tokens,
            total_tokens=token_usage.total_tokens,
            approximate_cost_usd=approximate_cost_usd,
        )
        return event

    def load_session_summary(self, session_id: str) -> SessionUsageSummaryView:
        rollups_by_bucket = {row.usage_bucket: row for row in self._usage.list_rollups(session_id)}
        bucket_summaries = [
            build_bucket_summary_view(rollups_by_bucket.get(bucket.value), usage_bucket=bucket)
            for bucket in _DEFAULT_USAGE_BUCKETS
        ]
        total_calls = sum(item.total_calls for item in bucket_summaries)
        total_elapsed_ms = sum(item.total_elapsed_ms for item in bucket_summaries)
        max_elapsed_ms = max(
            (item.max_elapsed_ms or 0 for item in bucket_summaries),
            default=0,
        )
        approximate_cost_usd = sum(item.approximate_cost_usd or 0 for item in bucket_summaries)
        return SessionUsageSummaryView(
            total_calls=total_calls,
            succeeded_calls=sum(item.succeeded_calls for item in bucket_summaries),
            failed_calls=sum(item.failed_calls for item in bucket_summaries),
            fallback_calls=sum(item.fallback_calls for item in bucket_summaries),
            token_metadata_call_count=sum(
                item.token_metadata_call_count for item in bucket_summaries
            ),
            cost_estimate_call_count=sum(
                item.cost_estimate_call_count for item in bucket_summaries
            ),
            total_elapsed_ms=total_elapsed_ms,
            average_elapsed_ms=(
                round(total_elapsed_ms / total_calls, 2) if total_calls > 0 else None
            ),
            max_elapsed_ms=max_elapsed_ms if total_calls > 0 else None,
            approximate_cost_usd=_resolve_aggregate_cost(
                total_calls=total_calls,
                cost_estimate_call_count=sum(
                    item.cost_estimate_call_count for item in bucket_summaries
                ),
                approximate_cost_usd_total=approximate_cost_usd,
            ),
            token_usage=ModelTokenUsageView(
                input_tokens=sum(item.token_usage.input_tokens or 0 for item in bucket_summaries),
                output_tokens=sum(item.token_usage.output_tokens or 0 for item in bucket_summaries),
                total_tokens=sum(item.token_usage.total_tokens or 0 for item in bucket_summaries),
                cached_input_tokens=sum(
                    item.token_usage.cached_input_tokens or 0 for item in bucket_summaries
                ),
                thought_tokens=sum(
                    item.token_usage.thought_tokens or 0 for item in bucket_summaries
                ),
            ),
            buckets=bucket_summaries,
        )

    def load_session_diagnostics(
        self,
        session_id: str,
        *,
        recent_limit: int = 20,
        leaderboard_limit: int = 5,
    ) -> SessionUsageDiagnosticsView:
        return SessionUsageDiagnosticsView(
            session_id=session_id,
            generated_at=utc_now(),
            summary=self.load_session_summary(session_id),
            stage_breakdown=[
                build_stage_breakdown_view(row)
                for row in self._usage.list_stage_breakdown(session_id)
            ],
            recent_calls=[
                build_usage_event_view(row)
                for row in self._usage.list_recent_events(session_id, limit=recent_limit)
            ],
            slowest_calls=[
                build_usage_event_view(row)
                for row in self._usage.list_slowest_events(
                    session_id,
                    limit=leaderboard_limit,
                )
            ],
            costliest_calls=[
                build_usage_event_view(row)
                for row in self._usage.list_costliest_events(
                    session_id,
                    limit=leaderboard_limit,
                )
            ],
        )


def extract_gemini_token_usage(
    raw_response: Mapping[str, Any] | list[Any] | str | None,
) -> ModelTokenUsageView:
    usage_payload = _extract_usage_metadata(raw_response)
    if usage_payload is None:
        return ModelTokenUsageView()

    return ModelTokenUsageView(
        input_tokens=_read_optional_int(usage_payload.get("promptTokenCount")),
        output_tokens=_read_optional_int(
            usage_payload.get("candidatesTokenCount") or usage_payload.get("candidateTokenCount")
        ),
        total_tokens=_read_optional_int(usage_payload.get("totalTokenCount")),
        cached_input_tokens=_read_optional_int(usage_payload.get("cachedContentTokenCount")),
        thought_tokens=_read_optional_int(usage_payload.get("thoughtsTokenCount")),
    )


def estimate_approximate_cost_usd(
    *,
    settings: AppSettings,
    usage_bucket: ModelUsageBucket,
    token_usage: ModelTokenUsageView,
) -> float | None:
    if (
        token_usage.total_tokens is None
        and token_usage.input_tokens is None
        and token_usage.output_tokens is None
    ):
        return None

    pricing = getattr(settings.gemini.approximate_pricing, usage_bucket.value)
    input_rate = pricing.input_cost_per_million_tokens_usd
    output_rate = pricing.output_cost_per_million_tokens_usd
    cached_rate = pricing.cached_input_cost_per_million_tokens_usd or input_rate

    input_tokens = token_usage.input_tokens or 0
    output_tokens = token_usage.output_tokens or 0
    cached_tokens = min(token_usage.cached_input_tokens or 0, input_tokens)
    uncached_input_tokens = max(input_tokens - cached_tokens, 0)

    total_cost = 0.0
    any_component = False

    if uncached_input_tokens > 0:
        if input_rate is None:
            return None
        total_cost += (uncached_input_tokens / 1_000_000) * input_rate
        any_component = True

    if cached_tokens > 0:
        if cached_rate is None:
            return None
        total_cost += (cached_tokens / 1_000_000) * cached_rate
        any_component = True

    if output_tokens > 0:
        if output_rate is None:
            return None
        total_cost += (output_tokens / 1_000_000) * output_rate
        any_component = True

    if not any_component:
        return 0.0

    return round(total_cost, 6)


def build_bucket_summary_view(
    rollup: SessionUsageRollup | None,
    *,
    usage_bucket: ModelUsageBucket,
) -> SessionUsageBucketSummaryView:
    if rollup is None:
        return SessionUsageBucketSummaryView(
            usage_bucket=usage_bucket,
            approximate_cost_usd=0.0,
        )

    return SessionUsageBucketSummaryView(
        usage_bucket=usage_bucket,
        total_calls=rollup.total_calls,
        succeeded_calls=rollup.succeeded_calls,
        failed_calls=rollup.failed_calls,
        fallback_calls=rollup.fallback_calls,
        token_metadata_call_count=rollup.token_metadata_call_count,
        cost_estimate_call_count=rollup.cost_estimate_call_count,
        total_elapsed_ms=rollup.total_elapsed_ms,
        average_elapsed_ms=(
            round(rollup.total_elapsed_ms / rollup.total_calls, 2)
            if rollup.total_calls > 0
            else None
        ),
        max_elapsed_ms=rollup.max_elapsed_ms if rollup.total_calls > 0 else None,
        approximate_cost_usd=_resolve_aggregate_cost(
            total_calls=rollup.total_calls,
            cost_estimate_call_count=rollup.cost_estimate_call_count,
            approximate_cost_usd_total=rollup.approximate_cost_usd_total,
        ),
        models_used=_normalize_models_json(rollup.models_json),
        token_usage=ModelTokenUsageView(
            input_tokens=rollup.input_tokens,
            output_tokens=rollup.output_tokens,
            total_tokens=rollup.total_tokens,
            cached_input_tokens=rollup.cached_input_tokens,
            thought_tokens=rollup.thought_tokens,
        ),
        last_model_id=rollup.last_model_id,
        last_purpose=rollup.last_purpose,
        last_called_at=rollup.last_called_at,
    )


def build_stage_breakdown_view(row: Mapping[str, Any]) -> SessionUsageStageBreakdownView:
    return SessionUsageStageBreakdownView(
        usage_bucket=ModelUsageBucket(str(row["usage_bucket"])),
        workflow_stage=row["workflow_stage"],
        model_id=str(row["model_id"]),
        total_calls=int(row["total_calls"] or 0),
        succeeded_calls=int(row["succeeded_calls"] or 0),
        failed_calls=int(row["failed_calls"] or 0),
        fallback_calls=int(row["fallback_calls"] or 0),
        token_metadata_call_count=int(row["token_metadata_call_count"] or 0),
        cost_estimate_call_count=int(row["cost_estimate_call_count"] or 0),
        total_elapsed_ms=int(row["total_elapsed_ms"] or 0),
        average_elapsed_ms=(
            round(float(row["average_elapsed_ms"]), 2)
            if row["average_elapsed_ms"] is not None
            else None
        ),
        max_elapsed_ms=(int(row["max_elapsed_ms"]) if row["max_elapsed_ms"] is not None else None),
        approximate_cost_usd=(
            round(float(row["approximate_cost_usd"]), 6)
            if row["approximate_cost_usd"] is not None
            else None
        ),
        token_usage=ModelTokenUsageView(
            input_tokens=int(row["input_tokens"] or 0),
            output_tokens=int(row["output_tokens"] or 0),
            total_tokens=int(row["total_tokens"] or 0),
            cached_input_tokens=int(row["cached_input_tokens"] or 0),
            thought_tokens=int(row["thought_tokens"] or 0),
        ),
    )


def build_usage_event_view(event: ModelUsageEvent) -> SessionUsageEventView:
    return SessionUsageEventView(
        id=event.id,
        usage_bucket=ModelUsageBucket(event.usage_bucket),
        workflow_stage=event.workflow_stage,
        purpose=event.purpose,
        provider=event.provider,
        model_id=event.model_id,
        prompt_version=event.prompt_version,
        outcome=ModelCallOutcome(event.outcome),
        elapsed_ms=event.elapsed_ms,
        approximate_cost_usd=event.approximate_cost_usd,
        token_usage=ModelTokenUsageView(
            input_tokens=event.input_tokens,
            output_tokens=event.output_tokens,
            total_tokens=event.total_tokens,
            cached_input_tokens=event.cached_input_tokens,
            thought_tokens=event.thought_tokens,
        ),
        error_message=event.error_message,
        created_at=event.created_at,
    )


def _apply_rollup_update(
    rollup: SessionUsageRollup,
    *,
    context: ModelUsageContext,
    elapsed_ms: int,
    outcome: ModelCallOutcome,
    token_usage: ModelTokenUsageView,
    approximate_cost_usd: float | None,
    now: datetime,
) -> None:
    rollup.total_calls += 1
    if outcome == ModelCallOutcome.SUCCEEDED:
        rollup.succeeded_calls += 1
    elif outcome == ModelCallOutcome.FAILED:
        rollup.failed_calls += 1
    else:
        rollup.fallback_calls += 1

    if any(
        value is not None
        for value in (
            token_usage.input_tokens,
            token_usage.output_tokens,
            token_usage.total_tokens,
            token_usage.cached_input_tokens,
            token_usage.thought_tokens,
        )
    ):
        rollup.token_metadata_call_count += 1
    if approximate_cost_usd is not None:
        rollup.cost_estimate_call_count += 1

    rollup.total_elapsed_ms += elapsed_ms
    rollup.max_elapsed_ms = max(rollup.max_elapsed_ms, elapsed_ms)
    rollup.input_tokens += token_usage.input_tokens or 0
    rollup.output_tokens += token_usage.output_tokens or 0
    rollup.total_tokens += token_usage.total_tokens or 0
    rollup.cached_input_tokens += token_usage.cached_input_tokens or 0
    rollup.thought_tokens += token_usage.thought_tokens or 0
    rollup.approximate_cost_usd_total += approximate_cost_usd or 0
    rollup.models_json = _append_model_id(rollup.models_json, context.model_id)
    rollup.last_model_id = context.model_id
    rollup.last_purpose = context.purpose
    rollup.last_called_at = now


def _extract_usage_metadata(
    raw_response: Mapping[str, Any] | list[Any] | str | None,
) -> dict[str, Any] | None:
    if not isinstance(raw_response, Mapping):
        return None

    usage_metadata = raw_response.get("usageMetadata")
    if isinstance(usage_metadata, Mapping):
        return dict(usage_metadata)

    adapter_raw_response = raw_response.get("adapter_raw_response")
    if isinstance(adapter_raw_response, Mapping):
        nested = adapter_raw_response.get("usageMetadata")
        if isinstance(nested, Mapping):
            return dict(nested)

    return None


def _normalize_models_json(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    normalized = [str(item).strip() for item in value if str(item).strip()]
    return sorted(set(normalized))


def _append_model_id(value: Any, model_id: str) -> list[str]:
    models = _normalize_models_json(value)
    if model_id not in models:
        models.append(model_id)
    return sorted(models)


def _normalize_error_message(value: str | None) -> str | None:
    if value is None:
        return None
    normalized = value.strip()
    if not normalized:
        return None
    return normalized[:255]


def _read_optional_int(value: Any) -> int | None:
    if value is None:
        return None
    try:
        return max(int(value), 0)
    except (TypeError, ValueError):
        return None


def _resolve_aggregate_cost(
    *,
    total_calls: int,
    cost_estimate_call_count: int,
    approximate_cost_usd_total: float,
) -> float | None:
    if total_calls == 0:
        return 0.0
    if cost_estimate_call_count == 0:
        return None
    return round(approximate_cost_usd_total, 6)
