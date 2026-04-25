import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class CallDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    call_sid: str
    user_id: uuid.UUID | None
    status: str
    from_number: str
    to_number: str
    started_at: datetime
    ended_at: datetime | None


class CallCreateDTO(BaseModel):
    call_sid: str
    user_id: uuid.UUID | None
    status: str
    from_number: str
    to_number: str


class CallStatusUpdateDTO(BaseModel):
    call_sid: str
    status: str
    ended_at: datetime | None = None
