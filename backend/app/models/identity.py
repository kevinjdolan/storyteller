from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

LOCAL_DEVELOPMENT_OWNER_ID = "local-user"
LOCAL_DEVELOPMENT_OWNER_DISPLAY_NAME = "Local Developer"


class RequestIdentity(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    subject: str = Field(min_length=1)
    display_name: str = Field(min_length=1)
    auth_mode: Literal["local_dev"] = "local_dev"


LOCAL_DEVELOPMENT_IDENTITY = RequestIdentity(
    subject=LOCAL_DEVELOPMENT_OWNER_ID,
    display_name=LOCAL_DEVELOPMENT_OWNER_DISPLAY_NAME,
)
