from __future__ import annotations

import time
from typing import Any

from app.services.story_tools import (
    StoryWorkflowToolService,
    get_story_workflow_tool_registry,
)
from app.worker.registry import JobHandlerRegistry
from app.worker.runtime import JobExecutionContext


def build_default_job_handler_registry() -> JobHandlerRegistry:
    registry = JobHandlerRegistry()
    registry.register("demo.echo", demo_echo_handler)
    tool_registry = get_story_workflow_tool_registry()
    for definition in tool_registry.list_tools():
        registry.register(
            definition.job_type,
            build_story_workflow_tool_handler(definition.job_type),
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
