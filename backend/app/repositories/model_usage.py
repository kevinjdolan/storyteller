from __future__ import annotations

from sqlalchemy import Select, case, func, select
from sqlalchemy.engine import RowMapping
from sqlalchemy.orm import Session

from app.db import ModelUsageEvent, SessionUsageRollup


class ModelUsageRepository:
    def __init__(self, session: Session):
        self._session = session

    def create_event(self, **kwargs) -> ModelUsageEvent:
        event = ModelUsageEvent(**kwargs)
        self._session.add(event)
        self._session.flush()
        return event

    def get_rollup(self, session_id: str, usage_bucket: str) -> SessionUsageRollup | None:
        stmt: Select[tuple[SessionUsageRollup]] = select(SessionUsageRollup).where(
            SessionUsageRollup.session_id == session_id,
            SessionUsageRollup.usage_bucket == usage_bucket,
        )
        return self._session.execute(stmt).scalar_one_or_none()

    def create_rollup(self, *, session_id: str, usage_bucket: str) -> SessionUsageRollup:
        rollup = SessionUsageRollup(session_id=session_id, usage_bucket=usage_bucket)
        self._session.add(rollup)
        self._session.flush()
        return rollup

    def list_rollups(self, session_id: str) -> list[SessionUsageRollup]:
        stmt: Select[tuple[SessionUsageRollup]] = (
            select(SessionUsageRollup)
            .where(SessionUsageRollup.session_id == session_id)
            .order_by(SessionUsageRollup.usage_bucket.asc())
        )
        return list(self._session.execute(stmt).scalars().all())

    def list_recent_events(self, session_id: str, *, limit: int) -> list[ModelUsageEvent]:
        stmt: Select[tuple[ModelUsageEvent]] = (
            select(ModelUsageEvent)
            .where(ModelUsageEvent.session_id == session_id)
            .order_by(ModelUsageEvent.created_at.desc(), ModelUsageEvent.id.desc())
            .limit(limit)
        )
        return list(self._session.execute(stmt).scalars().all())

    def list_slowest_events(self, session_id: str, *, limit: int) -> list[ModelUsageEvent]:
        stmt: Select[tuple[ModelUsageEvent]] = (
            select(ModelUsageEvent)
            .where(ModelUsageEvent.session_id == session_id)
            .order_by(ModelUsageEvent.elapsed_ms.desc(), ModelUsageEvent.created_at.desc())
            .limit(limit)
        )
        return list(self._session.execute(stmt).scalars().all())

    def list_costliest_events(self, session_id: str, *, limit: int) -> list[ModelUsageEvent]:
        stmt: Select[tuple[ModelUsageEvent]] = (
            select(ModelUsageEvent)
            .where(
                ModelUsageEvent.session_id == session_id,
                ModelUsageEvent.approximate_cost_usd.is_not(None),
            )
            .order_by(
                ModelUsageEvent.approximate_cost_usd.desc(),
                ModelUsageEvent.created_at.desc(),
            )
            .limit(limit)
        )
        return list(self._session.execute(stmt).scalars().all())

    def list_stage_breakdown(self, session_id: str) -> list[RowMapping]:
        succeeded_calls = func.sum(
            case((ModelUsageEvent.outcome == "succeeded", 1), else_=0)
        ).label("succeeded_calls")
        failed_calls = func.sum(
            case((ModelUsageEvent.outcome == "failed", 1), else_=0)
        ).label("failed_calls")
        fallback_calls = func.sum(
            case((ModelUsageEvent.outcome == "succeeded_with_fallback", 1), else_=0)
        ).label("fallback_calls")
        token_metadata_call_count = func.sum(
            case((ModelUsageEvent.total_tokens.is_not(None), 1), else_=0)
        ).label("token_metadata_call_count")
        cost_estimate_call_count = func.sum(
            case((ModelUsageEvent.approximate_cost_usd.is_not(None), 1), else_=0)
        ).label("cost_estimate_call_count")
        stmt = (
            select(
                ModelUsageEvent.usage_bucket.label("usage_bucket"),
                ModelUsageEvent.workflow_stage.label("workflow_stage"),
                ModelUsageEvent.model_id.label("model_id"),
                func.count(ModelUsageEvent.id).label("total_calls"),
                succeeded_calls,
                failed_calls,
                fallback_calls,
                token_metadata_call_count,
                cost_estimate_call_count,
                func.sum(ModelUsageEvent.elapsed_ms).label("total_elapsed_ms"),
                func.avg(ModelUsageEvent.elapsed_ms).label("average_elapsed_ms"),
                func.max(ModelUsageEvent.elapsed_ms).label("max_elapsed_ms"),
                func.sum(ModelUsageEvent.input_tokens).label("input_tokens"),
                func.sum(ModelUsageEvent.output_tokens).label("output_tokens"),
                func.sum(ModelUsageEvent.total_tokens).label("total_tokens"),
                func.sum(ModelUsageEvent.cached_input_tokens).label("cached_input_tokens"),
                func.sum(ModelUsageEvent.thought_tokens).label("thought_tokens"),
                func.sum(ModelUsageEvent.approximate_cost_usd).label("approximate_cost_usd"),
            )
            .where(ModelUsageEvent.session_id == session_id)
            .group_by(
                ModelUsageEvent.usage_bucket,
                ModelUsageEvent.workflow_stage,
                ModelUsageEvent.model_id,
            )
            .order_by(
                ModelUsageEvent.usage_bucket.asc(),
                ModelUsageEvent.workflow_stage.asc(),
                ModelUsageEvent.model_id.asc(),
            )
        )
        return list(self._session.execute(stmt).mappings().all())
