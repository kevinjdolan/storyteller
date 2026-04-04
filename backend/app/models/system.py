from __future__ import annotations

from typing import Dict, Literal, Optional

from pydantic import BaseModel, Field


class DependencyStatus(BaseModel):
    status: str
    detail: str


class HealthResponse(BaseModel):
    status: Literal["ok"]
    service: str
    environment: str
    version: str
    api_version: Optional[str] = None
    dependencies: Dict[str, DependencyStatus] = Field(default_factory=dict)


class HelloResponse(BaseModel):
    message: str
