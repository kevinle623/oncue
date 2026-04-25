from dataclasses import dataclass
from typing import Any
from urllib.parse import urlencode

import httpx

from oncue.settings import settings

SPOTIFY_AUTH_URL = "https://accounts.spotify.com/authorize"
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
SPOTIFY_API_BASE = "https://api.spotify.com/v1"

DEFAULT_SCOPES = (
    "user-modify-playback-state",
    "user-read-playback-state",
    "user-read-currently-playing",
    "user-read-private",
)


@dataclass(frozen=True)
class SpotifyTokens:
    access_token: str
    refresh_token: str
    expires_in: int
    scope: str


class SpotifyAPIError(Exception):
    def __init__(self, status_code: int, message: str) -> None:
        super().__init__(f"Spotify API {status_code}: {message}")
        self.status_code = status_code


def build_authorize_url(state: str, scopes: tuple[str, ...] = DEFAULT_SCOPES) -> str:
    params = {
        "response_type": "code",
        "client_id": settings.spotify_client_id,
        "scope": " ".join(scopes),
        "redirect_uri": settings.spotify_redirect_uri,
        "state": state,
    }
    return f"{SPOTIFY_AUTH_URL}?{urlencode(params)}"


async def exchange_code(code: str) -> SpotifyTokens:
    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.post(
            SPOTIFY_TOKEN_URL,
            data={
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": settings.spotify_redirect_uri,
            },
            auth=(settings.spotify_client_id, settings.spotify_client_secret),
        )
    response.raise_for_status()
    payload = response.json()
    return SpotifyTokens(
        access_token=payload["access_token"],
        refresh_token=payload["refresh_token"],
        expires_in=int(payload["expires_in"]),
        scope=payload.get("scope", ""),
    )


async def refresh_access_token(refresh_token: str) -> SpotifyTokens:
    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.post(
            SPOTIFY_TOKEN_URL,
            data={
                "grant_type": "refresh_token",
                "refresh_token": refresh_token,
            },
            auth=(settings.spotify_client_id, settings.spotify_client_secret),
        )
    response.raise_for_status()
    payload = response.json()
    return SpotifyTokens(
        access_token=payload["access_token"],
        refresh_token=payload.get("refresh_token", refresh_token),
        expires_in=int(payload["expires_in"]),
        scope=payload.get("scope", ""),
    )


def _auth_headers(access_token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {access_token}"}


async def _request(
    method: str,
    path: str,
    access_token: str,
    *,
    params: dict[str, Any] | None = None,
    json: dict[str, Any] | None = None,
) -> dict[str, Any] | None:
    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.request(
            method,
            f"{SPOTIFY_API_BASE}{path}",
            headers=_auth_headers(access_token),
            params=params,
            json=json,
        )
    if response.status_code == 204 or not response.content:
        return None
    if response.status_code >= 400:
        raise SpotifyAPIError(response.status_code, response.text)
    data: dict[str, Any] = response.json()
    return data


async def get_currently_playing(access_token: str) -> dict[str, Any] | None:
    return await _request("GET", "/me/player/currently-playing", access_token)


async def search_tracks(
    access_token: str, query: str, limit: int = 5
) -> dict[str, Any]:
    result = await _request(
        "GET",
        "/search",
        access_token,
        params={"q": query, "type": "track", "limit": limit},
    )
    return result or {}


async def start_playback(
    access_token: str,
    *,
    uris: list[str] | None = None,
    context_uri: str | None = None,
    device_id: str | None = None,
) -> None:
    body: dict[str, Any] = {}
    if uris is not None:
        body["uris"] = uris
    if context_uri is not None:
        body["context_uri"] = context_uri
    params = {"device_id": device_id} if device_id else None
    await _request(
        "PUT", "/me/player/play", access_token, params=params, json=body or None
    )


async def pause_playback(access_token: str, *, device_id: str | None = None) -> None:
    params = {"device_id": device_id} if device_id else None
    await _request("PUT", "/me/player/pause", access_token, params=params)


async def skip_to_next(access_token: str, *, device_id: str | None = None) -> None:
    params = {"device_id": device_id} if device_id else None
    await _request("POST", "/me/player/next", access_token, params=params)


async def add_to_queue(
    access_token: str, uri: str, *, device_id: str | None = None
) -> None:
    params: dict[str, Any] = {"uri": uri}
    if device_id:
        params["device_id"] = device_id
    await _request("POST", "/me/player/queue", access_token, params=params)
