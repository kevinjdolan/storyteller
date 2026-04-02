from __future__ import annotations

from app.db import Base, make_engine
from app.models import ModelCallOutcome, ModelUsageBucket, WorkflowStage
from app.services.model_usage import ModelUsageContext, SessionModelUsageService
from app.services.sessions import SessionService
from sqlalchemy.orm import sessionmaker


def _enable_sqlite_foreign_keys(engine) -> None:
    with engine.begin() as connection:
        connection.exec_driver_sql("PRAGMA foreign_keys=ON")


def test_model_usage_service_builds_rollups_and_diagnostics() -> None:
    engine = make_engine("sqlite+pysqlite:///:memory:")
    _enable_sqlite_foreign_keys(engine)
    Base.metadata.create_all(engine)
    db_session = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)()

    try:
        session_id = SessionService(db_session).create_session(working_title="Metrics").id
        usage = SessionModelUsageService(db_session)

        usage.record_model_call(
            context=ModelUsageContext(
                session_id=session_id,
                usage_bucket=ModelUsageBucket.PLANNING,
                workflow_stage=None,
                purpose="pitch_generation",
                model_id="gemini-3.1-pro",
                prompt_version="pitch_generation.v3",
            ),
            elapsed_ms=820,
            outcome=ModelCallOutcome.SUCCEEDED,
            raw_response={
                "usageMetadata": {
                    "promptTokenCount": 1000,
                    "candidatesTokenCount": 200,
                    "totalTokenCount": 1200,
                }
            },
        )
        usage.record_model_call(
            context=ModelUsageContext(
                session_id=session_id,
                usage_bucket=ModelUsageBucket.PLANNING,
                workflow_stage=None,
                purpose="beat_sheet_generation",
                model_id="gemini-3.1-pro",
                prompt_version="beat_sheet_generation.v2",
            ),
            elapsed_ms=1400,
            outcome=ModelCallOutcome.SUCCEEDED_WITH_FALLBACK,
            raw_response={
                "fallback_reason": "validation failed",
                "adapter_raw_response": {
                    "usageMetadata": {
                        "promptTokenCount": 400,
                        "candidatesTokenCount": 100,
                        "totalTokenCount": 500,
                    }
                },
            },
            error_message="validation failed",
        )
        db_session.commit()

        diagnostics = usage.load_session_diagnostics(session_id)
        planning_bucket = next(
            bucket for bucket in diagnostics.summary.buckets if bucket.usage_bucket == "planning"
        )

        assert planning_bucket.total_calls == 2
        assert planning_bucket.fallback_calls == 1
        assert planning_bucket.token_metadata_call_count == 2
        assert planning_bucket.token_usage.total_tokens == 1700
        assert planning_bucket.models_used == ["gemini-3.1-pro"]
        assert planning_bucket.approximate_cost_usd == 0.00066
        assert diagnostics.slowest_calls[0].purpose == "beat_sheet_generation"
        assert diagnostics.costliest_calls[0].purpose == "pitch_generation"
        assert diagnostics.recent_calls[0].purpose == "beat_sheet_generation"
        assert diagnostics.recent_calls[0].error_message == "validation failed"
    finally:
        db_session.close()
        engine.dispose()


def test_session_snapshot_includes_usage_summary() -> None:
    engine = make_engine("sqlite+pysqlite:///:memory:")
    _enable_sqlite_foreign_keys(engine)
    Base.metadata.create_all(engine)
    db_session = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)()

    try:
        service = SessionService(db_session)
        session_id = service.create_session(working_title="Snapshot Metrics").id

        SessionModelUsageService(db_session).record_model_call(
            context=ModelUsageContext(
                session_id=session_id,
                usage_bucket=ModelUsageBucket.COMPOSITION,
                workflow_stage=WorkflowStage.COMPOSITION,
                purpose="composition_generation",
                model_id="gemini-3.1-pro",
                prompt_version="composition.v1",
            ),
            elapsed_ms=2200,
            outcome=ModelCallOutcome.SUCCEEDED,
            raw_response={
                "usageMetadata": {
                    "promptTokenCount": 2200,
                    "candidatesTokenCount": 600,
                    "totalTokenCount": 2800,
                }
            },
        )
        db_session.commit()

        snapshot = service.load_session_snapshot(session_id)
        composition_bucket = next(
            bucket
            for bucket in snapshot.usage_summary.buckets
            if bucket.usage_bucket == "composition"
        )

        assert snapshot.usage_summary.total_calls == 1
        assert composition_bucket.total_calls == 1
        assert composition_bucket.token_usage.total_tokens == 2800
        assert composition_bucket.last_model_id == "gemini-3.1-pro"
    finally:
        db_session.close()
        engine.dispose()
