import secrets
import uuid
from datetime import UTC, datetime, timedelta

from sqlalchemy.ext.asyncio import AsyncSession

from oncue.adapters.cache.redis import redis
from oncue.adapters.music.spotify import build_authorize_url, exchange_code
from oncue.dtos.spotify_account import SpotifyAccountDTO, SpotifyAccountUpsertDTO
from oncue.repositories import spotify_account_repo
from oncue.services import user_service

STATE_TTL_SECONDS = 600
STATE_KEY_PREFIX = "spotify:oauth:state:"


class InvalidStateError(Exception):
    pass


async def start_authorization(session: AsyncSession, phone_number: str) -> str:
    user = await user_service.get_or_create_by_phone(session, phone_number)
    state = secrets.token_urlsafe(32)
    await redis.set(f"{STATE_KEY_PREFIX}{state}", str(user.id), ex=STATE_TTL_SECONDS)
    return build_authorize_url(state)


async def complete_authorization(
    session: AsyncSession, code: str, state: str
) -> SpotifyAccountDTO:
    key = f"{STATE_KEY_PREFIX}{state}"
    raw_user_id = await redis.get(key)
    if raw_user_id is None:
        raise InvalidStateError("Unknown or expired state")
    await redis.delete(key)

    user_id = uuid.UUID(raw_user_id)
    tokens = await exchange_code(code)
    expires_at = datetime.now(UTC) + timedelta(seconds=tokens.expires_in)
    return await spotify_account_repo.upsert(
        session,
        SpotifyAccountUpsertDTO(
            user_id=user_id,
            access_token=tokens.access_token,
            refresh_token=tokens.refresh_token,
            expires_at=expires_at,
            scope=tokens.scope,
        ),
    )
