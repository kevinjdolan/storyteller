from __future__ import annotations

import time
from typing import Any

from app.services.composition_jobs import (
    COMPOSITION_RUNTIME_JOB_TYPE,
    CompositionJobService,
    CompositionJobServiceError,
    CompositionSegmentWriter,
)
from app.services.story_tools import (
    StoryWorkflowToolService,
    get_story_workflow_tool_registry,
)
from app.storage import ObjectStorageService
from app.worker.registry import JobHandlerRegistry
from app.worker.runtime import JobExecutionContext


def build_default_job_handler_registry(
    *,
    composition_chunk_delay_seconds: float = 0.0,
    object_storage: ObjectStorageService | None = None,
    composition_writer: CompositionSegmentWriter | None = None,
) -> JobHandlerRegistry:
    registry = JobHandlerRegistry()
    registry.register("demo.echo", demo_echo_handler)
    tool_registry = get_story_workflow_tool_registry()
    for definition in tool_registry.list_tools():
        registry.register(
            definition.job_type,
            build_story_workflow_tool_handler(definition.job_type),
        )
    registry.register(
        COMPOSITION_RUNTIME_JOB_TYPE,
        build_composition_runtime_handler(
            chunk_delay_seconds=composition_chunk_delay_seconds,
            object_storage=object_storage,
            composition_writer=composition_writer,
        ),
    )
    return registry


def demo_echo_handler(
    payload: dict[str, Any] | list[Any] | None,
    context: JobExecutionContext,
) -> dict[str, Any]:
    payload_dict = payload if isinstance(payload, dict) else {}
    step_count = max(int(payload_dict.get("steps", 1)), 1)
    step_delay_seconds = max(float(payload_dict.get("step_delay_seconds", 0)), 0.0)

    for _ in range(step_count):
        if step_delay_seconds > 0:
            time.sleep(step_delay_seconds)
        context.heartbeat()

    return {
        "echo": payload_dict.get("message", payload),
        "step_count": step_count,
        "worker_id": context.worker_id,
    }


def build_story_workflow_tool_handler(job_type: str):
    def handler(
        payload: dict[str, Any] | list[Any] | None,
        context: JobExecutionContext,
    ) -> dict[str, Any]:
        if context.session_id is None:
            raise ValueError(f"job type {job_type!r} requires a session_id")

        payload_dict = payload if isinstance(payload, dict) else {}
        tool_registry = get_story_workflow_tool_registry()
        definition = tool_registry.get_by_job_type(job_type)
        context.heartbeat()
        result = context.with_session(
            lambda session: StoryWorkflowToolService(session, tool_registry).execute(
                tool_name=definition.name,
                session_id=context.session_id,
                arguments=payload_dict,
            )
        )
        return result.model_dump(mode="json")

    return handler


def build_composition_runtime_handler(
    *,
    chunk_delay_seconds: float = 0.0,
    object_storage: ObjectStorageService | None = None,
    composition_writer: CompositionSegmentWriter | None = None,
):
    def handler(
        payload: dict[str, Any] | list[Any] | None,
        context: JobExecutionContext,
    ) -> dict[str, Any]:
        payload_dict = payload if isinstance(payload, dict) else {}
        composition_job_id = payload_dict.get("composition_job_id")
        if not isinstance(composition_job_id, str) or not composition_job_id.strip():
            raise CompositionJobServiceError(
                "composition runtime jobs require a composition_job_id payload",
            )

        try:
            return context.with_session(
                lambda session: CompositionJobService(
                    session,
                    chunk_delay_seconds=chunk_delay_seconds,
                    object_storage=object_storage,
                    writer=composition_writer,
                ).run_job(
                    composition_job_id.strip(),
                )
            )
        except Exception as exc:
            error_message = str(exc).strip() or exc.__class__.__name__
            context.with_session(
                lambda session: CompositionJobService(
                    session,
                    chunk_delay_seconds=chunk_delay_seconds,
                    object_storage=object_storage,
                    writer=composition_writer,
                ).mark_job_failed(
                    composition_job_id.strip(),
                    error_message=error_message,
                )
            )
            raise

    return handler
