import uuid
from typing import Any

import pytest

from oncue import tools as tools_pkg
from oncue.dtos.spotify_playback import NowPlayingDTO, TrackDTO
from oncue.services import spotify_service
from oncue.tools.base import (
    Tool,
    ToolContext,
    ToolNotAllowedError,
    UnknownToolError,
    build_registry,
    dispatch_immediate,
)


def test_registry_contains_spotify_tools() -> None:
    assert "spotify_now_playing" in tools_pkg.REGISTRY
    assert "spotify_search_tracks" in tools_pkg.REGISTRY
    assert tools_pkg.REGISTRY["spotify_now_playing"].bucket == "immediate"


def test_build_registry_rejects_duplicates() -> None:
    async def noop(_ctx: ToolContext, _args: dict[str, Any]) -> None:
        return None

    tool = Tool(
        name="dup",
        description="",
        input_schema={"type": "object"},
        bucket="immediate",
        handler=noop,
    )
    with pytest.raises(ValueError):
        build_registry([tool, tool])


async def test_dispatch_immediate_runs_now_playing(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    track = TrackDTO(
        id="abc",
        name="Track",
        uri="spotify:track:abc",
        artists=["Artist"],
        album="Album",
        duration_ms=1000,
    )

    async def fake_now_playing(_session: object, _user_id: uuid.UUID) -> NowPlayingDTO:
        return NowPlayingDTO(
            track=track, is_playing=True, progress_ms=10, device_name="Phone"
        )

    monkeypatch.setattr(spotify_service, "now_playing", fake_now_playing)

    ctx = ToolContext(session=None, user_id=uuid.uuid4())  # type: ignore[arg-type]
    result = await dispatch_immediate(
        tools_pkg.REGISTRY, ctx, "spotify_now_playing", {}
    )

    assert result["is_playing"] is True
    assert result["track"]["id"] == "abc"


async def test_dispatch_immediate_unknown_tool() -> None:
    ctx = ToolContext(session=None, user_id=uuid.uuid4())  # type: ignore[arg-type]
    with pytest.raises(UnknownToolError):
        await dispatch_immediate(tools_pkg.REGISTRY, ctx, "nope", {})


async def test_dispatch_immediate_rejects_deferred_tool() -> None:
    async def noop(_ctx: ToolContext, _args: dict[str, Any]) -> None:
        return None

    deferred = Tool(
        name="deferred_op",
        description="",
        input_schema={"type": "object"},
        bucket="deferred",
        handler=noop,
    )
    registry = build_registry([deferred])
    ctx = ToolContext(session=None, user_id=uuid.uuid4())  # type: ignore[arg-type]
    with pytest.raises(ToolNotAllowedError):
        await dispatch_immediate(registry, ctx, "deferred_op", {})
