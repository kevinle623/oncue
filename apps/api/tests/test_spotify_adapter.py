from collections.abc import Callable

import httpx
import pytest

from oncue.adapters.music import spotify as spotify_adapter

MockInstaller = Callable[[Callable[[httpx.Request], httpx.Response], str], None]


async def test_get_currently_playing_returns_payload(mock_httpx: MockInstaller) -> None:
    captured: dict[str, str] = {}

    def handler(request: httpx.Request) -> httpx.Response:
        captured["path"] = request.url.path
        captured["auth"] = request.headers["authorization"]
        return httpx.Response(
            200,
            json={
                "is_playing": True,
                "progress_ms": 1234,
                "item": {
                    "id": "abc",
                    "name": "Track",
                    "uri": "spotify:track:abc",
                    "artists": [{"name": "Artist"}],
                    "album": {"name": "Album"},
                    "duration_ms": 200000,
                },
            },
        )

    mock_httpx(handler, "oncue.adapters.music.spotify")

    payload = await spotify_adapter.get_currently_playing("token-123")

    assert payload is not None
    assert payload["item"]["id"] == "abc"
    assert captured["path"].endswith("/me/player/currently-playing")
    assert captured["auth"] == "Bearer token-123"


async def test_get_currently_playing_returns_none_on_204(
    mock_httpx: MockInstaller,
) -> None:
    mock_httpx(lambda _r: httpx.Response(204), "oncue.adapters.music.spotify")
    assert await spotify_adapter.get_currently_playing("t") is None


async def test_search_tracks_passes_query(mock_httpx: MockInstaller) -> None:
    captured: dict[str, str] = {}

    def handler(request: httpx.Request) -> httpx.Response:
        captured["q"] = request.url.params["q"]
        captured["type"] = request.url.params["type"]
        captured["limit"] = request.url.params["limit"]
        return httpx.Response(200, json={"tracks": {"items": []}})

    mock_httpx(handler, "oncue.adapters.music.spotify")

    await spotify_adapter.search_tracks("t", "miles davis", limit=3)

    assert captured == {"q": "miles davis", "type": "track", "limit": "3"}


async def test_request_raises_on_error(mock_httpx: MockInstaller) -> None:
    mock_httpx(
        lambda _r: httpx.Response(401, text="bad token"),
        "oncue.adapters.music.spotify",
    )

    with pytest.raises(spotify_adapter.SpotifyAPIError) as exc:
        await spotify_adapter.get_currently_playing("t")

    assert exc.value.status_code == 401
