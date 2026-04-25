import uuid
from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict


class CallTurnDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    call_id: uuid.UUID
    role: str
    transcript: str | None
    tool_calls: list[dict[str, Any]] | None
    created_at: datetime


class CallTurnCreateDTO(BaseModel):
    call_id: uuid.UUID
    role: str
    transcript: str | None = None
    tool_calls: list[dict[str, Any]] | None = None
