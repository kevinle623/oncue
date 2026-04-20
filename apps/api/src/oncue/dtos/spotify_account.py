import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class SpotifyAccountDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    user_id: uuid.UUID
    access_token: str
    refresh_token: str
    expires_at: datetime
    scope: str
    created_at: datetime
    updated_at: datetime


class SpotifyAccountUpsertDTO(BaseModel):
    user_id: uuid.UUID
    access_token: str
    refresh_token: str
    expires_at: datetime
    scope: str
