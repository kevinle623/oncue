import uuid
from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict

DeferredToolJobStatus = Literal["pending", "succeeded", "failed"]


class DeferredToolJobDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    call_id: uuid.UUID
    tool_name: str
    args: dict[str, Any]
    status: DeferredToolJobStatus
    scheduled_for: datetime
    executed_at: datetime | None
    error: str | None
    created_at: datetime


class DeferredToolJobCreateDTO(BaseModel):
    call_id: uuid.UUID
    tool_name: str
    args: dict[str, Any]
    status: DeferredToolJobStatus = "pending"
    scheduled_for: datetime
