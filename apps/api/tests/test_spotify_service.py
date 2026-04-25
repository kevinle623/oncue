import uuid
from datetime import UTC, datetime, timedelta

import pytest

from oncue.adapters.music import spotify as spotify_adapter
from oncue.dtos.spotify_account import SpotifyAccountDTO, SpotifyAccountUpsertDTO
from oncue.repositories import spotify_account_repo
from oncue.services import spotify_service


def _account(expires_at: datetime) -> SpotifyAccountDTO:
    now = datetime.now(UTC)
    return SpotifyAccountDTO(
        id=uuid.uuid4(),
        user_id=uuid.uuid4(),
        access_token="cached-token",
        refresh_token="refresh-token",
        expires_at=expires_at,
        scope="user-read-private",
        created_at=now,
        updated_at=now,
    )


async def test_get_fresh_access_token_returns_cached_when_valid(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    account = _account(datetime.now(UTC) + timedelta(minutes=30))

    async def fake_get_by_user_id(
        _session: object, _uid: uuid.UUID
    ) -> SpotifyAccountDTO:
        return account

    refreshed = False

    async def fake_refresh(_rt: str) -> spotify_adapter.SpotifyTokens:
        nonlocal refreshed
        refreshed = True
        raise AssertionError("should not refresh")

    monkeypatch.setattr(spotify_account_repo, "get_by_user_id", fake_get_by_user_id)
    monkeypatch.setattr(spotify_adapter, "refresh_access_token", fake_refresh)

    token = await spotify_service.get_fresh_access_token(
        session=None,  # type: ignore[arg-type]
        user_id=account.user_id,
    )

    assert token == "cached-token"
    assert refreshed is False


async def test_get_fresh_access_token_refreshes_when_expired(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    account = _account(datetime.now(UTC) - timedelta(seconds=5))

    async def fake_get_by_user_id(
        _session: object, _uid: uuid.UUID
    ) -> SpotifyAccountDTO:
        return account

    async def fake_refresh(rt: str) -> spotify_adapter.SpotifyTokens:
        assert rt == "refresh-token"
        return spotify_adapter.SpotifyTokens(
            access_token="new-token",
            refresh_token="refresh-token",
            expires_in=3600,
            scope="user-read-private",
        )

    upserted: dict[str, SpotifyAccountUpsertDTO] = {}

    async def fake_upsert(
        _session: object, data: SpotifyAccountUpsertDTO
    ) -> SpotifyAccountDTO:
        upserted["data"] = data
        now = datetime.now(UTC)
        return SpotifyAccountDTO(
            id=account.id,
            user_id=data.user_id,
            access_token=data.access_token,
            refresh_token=data.refresh_token,
            expires_at=data.expires_at,
            scope=data.scope,
            created_at=now,
            updated_at=now,
        )

    monkeypatch.setattr(spotify_account_repo, "get_by_user_id", fake_get_by_user_id)
    monkeypatch.setattr(spotify_account_repo, "upsert", fake_upsert)
    monkeypatch.setattr(spotify_adapter, "refresh_access_token", fake_refresh)

    token = await spotify_service.get_fresh_access_token(
        session=None,  # type: ignore[arg-type]
        user_id=account.user_id,
    )

    assert token == "new-token"
    assert upserted["data"].access_token == "new-token"


async def test_get_fresh_access_token_raises_when_not_connected(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    async def fake_get_by_user_id(
        _session: object, _uid: uuid.UUID
    ) -> SpotifyAccountDTO | None:
        return None

    monkeypatch.setattr(spotify_account_repo, "get_by_user_id", fake_get_by_user_id)

    with pytest.raises(spotify_service.NotConnectedError):
        await spotify_service.get_fresh_access_token(
            session=None,  # type: ignore[arg-type]
            user_id=uuid.uuid4(),
        )
