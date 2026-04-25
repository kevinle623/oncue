import secrets
import uuid
from datetime import UTC, datetime, timedelta

from sqlalchemy.ext.asyncio import AsyncSession

from oncue.adapters.cache.redis import redis
from oncue.adapters.music import spotify as spotify_adapter
from oncue.dtos.spotify_account import SpotifyAccountDTO, SpotifyAccountUpsertDTO
from oncue.dtos.spotify_playback import NowPlayingDTO, TrackDTO
from oncue.repositories import spotify_account_repo
from oncue.services import user_service

STATE_TTL_SECONDS = 600
STATE_KEY_PREFIX = "spotify:oauth:state:"
TOKEN_REFRESH_SKEW = timedelta(seconds=60)


class InvalidStateError(Exception):
    pass


class NotConnectedError(Exception):
    pass


async def start_authorization(session: AsyncSession, phone_number: str) -> str:
    user = await user_service.get_or_create_by_phone(session, phone_number)
    state = secrets.token_urlsafe(32)
    await redis.set(f"{STATE_KEY_PREFIX}{state}", str(user.id), ex=STATE_TTL_SECONDS)
    return spotify_adapter.build_authorize_url(state)


async def complete_authorization(
    session: AsyncSession, code: str, state: str
) -> SpotifyAccountDTO:
    key = f"{STATE_KEY_PREFIX}{state}"
    raw_user_id = await redis.get(key)
    if raw_user_id is None:
        raise InvalidStateError("Unknown or expired state")
    await redis.delete(key)

    user_id = uuid.UUID(raw_user_id)
    tokens = await spotify_adapter.exchange_code(code)
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


async def get_fresh_access_token(session: AsyncSession, user_id: uuid.UUID) -> str:
    account = await spotify_account_repo.get_by_user_id(session, user_id)
    if account is None:
        raise NotConnectedError(f"No Spotify account linked for user {user_id}")
    if account.expires_at - TOKEN_REFRESH_SKEW > datetime.now(UTC):
        return account.access_token

    tokens = await spotify_adapter.refresh_access_token(account.refresh_token)
    expires_at = datetime.now(UTC) + timedelta(seconds=tokens.expires_in)
    refreshed = await spotify_account_repo.upsert(
        session,
        SpotifyAccountUpsertDTO(
            user_id=user_id,
            access_token=tokens.access_token,
            refresh_token=tokens.refresh_token,
            expires_at=expires_at,
            scope=tokens.scope or account.scope,
        ),
    )
    return refreshed.access_token


async def now_playing(
    session: AsyncSession, user_id: uuid.UUID
) -> NowPlayingDTO | None:
    token = await get_fresh_access_token(session, user_id)
    payload = await spotify_adapter.get_currently_playing(token)
    if payload is None:
        return None
    item = payload.get("item")
    if not item:
        return None
    return NowPlayingDTO(
        track=TrackDTO.from_spotify(item),
        is_playing=bool(payload.get("is_playing", False)),
        progress_ms=int(payload.get("progress_ms", 0)),
        device_name=(payload.get("device") or {}).get("name"),
    )


async def search_tracks(
    session: AsyncSession, user_id: uuid.UUID, query: str, limit: int = 5
) -> list[TrackDTO]:
    token = await get_fresh_access_token(session, user_id)
    payload = await spotify_adapter.search_tracks(token, query, limit=limit)
    items = (payload.get("tracks") or {}).get("items") or []
    return [TrackDTO.from_spotify(item) for item in items]
