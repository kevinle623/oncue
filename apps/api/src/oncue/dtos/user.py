import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class UserDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    phone_number: str
    display_name: str | None
    created_at: datetime
    updated_at: datetime


class UserCreateDTO(BaseModel):
    phone_number: str
    display_name: str | None = None
