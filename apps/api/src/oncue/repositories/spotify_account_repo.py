import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from oncue.dtos.spotify_account import SpotifyAccountDTO, SpotifyAccountUpsertDTO
from oncue.models.spotify_account import SpotifyAccount


async def get_by_user_id(
    session: AsyncSession, user_id: uuid.UUID
) -> SpotifyAccountDTO | None:
    result = await session.execute(
        select(SpotifyAccount).where(SpotifyAccount.user_id == user_id)
    )
    account = result.scalar_one_or_none()
    return SpotifyAccountDTO.model_validate(account) if account else None


async def upsert(
    session: AsyncSession, data: SpotifyAccountUpsertDTO
) -> SpotifyAccountDTO:
    result = await session.execute(
        select(SpotifyAccount).where(SpotifyAccount.user_id == data.user_id)
    )
    account = result.scalar_one_or_none()
    if account is None:
        account = SpotifyAccount(
            user_id=data.user_id,
            access_token=data.access_token,
            refresh_token=data.refresh_token,
            expires_at=data.expires_at,
            scope=data.scope,
        )
        session.add(account)
    else:
        account.access_token = data.access_token
        account.refresh_token = data.refresh_token
        account.expires_at = data.expires_at
        account.scope = data.scope
    await session.flush()
    await session.refresh(account)
    return SpotifyAccountDTO.model_validate(account)
