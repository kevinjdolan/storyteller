from __future__ import annotations

import time
from typing import Any

from app.worker.registry import JobHandlerRegistry
from app.worker.runtime import JobExecutionContext


def build_default_job_handler_registry() -> JobHandlerRegistry:
    registry = JobHandlerRegistry()
    registry.register("demo.echo", demo_echo_handler)
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
