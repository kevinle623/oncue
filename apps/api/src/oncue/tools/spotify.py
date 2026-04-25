from typing import Any

from oncue.services import spotify_service
from oncue.tools.base import Tool, ToolContext


async def _now_playing(ctx: ToolContext, _arguments: dict[str, Any]) -> dict[str, Any]:
    result = await spotify_service.now_playing(ctx.session, ctx.user_id)
    if result is None:
        return {"is_playing": False, "track": None}
    return result.model_dump()


async def _search_tracks(ctx: ToolContext, arguments: dict[str, Any]) -> dict[str, Any]:
    query = str(arguments["query"])
    limit = int(arguments.get("limit", 5))
    tracks = await spotify_service.search_tracks(
        ctx.session, ctx.user_id, query, limit=limit
    )
    return {"tracks": [t.model_dump() for t in tracks]}


async def _play(ctx: ToolContext, arguments: dict[str, Any]) -> dict[str, Any]:
    uris_raw = arguments.get("uris")
    uris: list[str] | None = None
    if isinstance(uris_raw, list):
        uris = [str(uri) for uri in uris_raw]
    await spotify_service.play(
        ctx.session,
        ctx.user_id,
        uris=uris,
        context_uri=(
            str(arguments["context_uri"]) if "context_uri" in arguments else None
        ),
        device_id=str(arguments["device_id"]) if "device_id" in arguments else None,
    )
    return {"ok": True}


async def _pause(ctx: ToolContext, arguments: dict[str, Any]) -> dict[str, Any]:
    await spotify_service.pause(
        ctx.session,
        ctx.user_id,
        device_id=str(arguments["device_id"]) if "device_id" in arguments else None,
    )
    return {"ok": True}


async def _skip(ctx: ToolContext, arguments: dict[str, Any]) -> dict[str, Any]:
    await spotify_service.skip_next(
        ctx.session,
        ctx.user_id,
        device_id=str(arguments["device_id"]) if "device_id" in arguments else None,
    )
    return {"ok": True}


async def _queue(ctx: ToolContext, arguments: dict[str, Any]) -> dict[str, Any]:
    await spotify_service.queue_track(
        ctx.session,
        ctx.user_id,
        uri=str(arguments["uri"]),
        device_id=str(arguments["device_id"]) if "device_id" in arguments else None,
    )
    return {"ok": True}


now_playing_tool = Tool(
    name="spotify_now_playing",
    description="Get the user's currently playing Spotify track, if any.",
    input_schema={
        "type": "object",
        "properties": {},
        "additionalProperties": False,
    },
    bucket="immediate",
    handler=_now_playing,
)

search_tracks_tool = Tool(
    name="spotify_search_tracks",
    description=(
        "Search Spotify for tracks matching a query. "
        "Returns up to `limit` results (default 5)."
    ),
    input_schema={
        "type": "object",
        "properties": {
            "query": {"type": "string", "description": "Search query."},
            "limit": {
                "type": "integer",
                "minimum": 1,
                "maximum": 20,
                "default": 5,
            },
        },
        "required": ["query"],
        "additionalProperties": False,
    },
    bucket="immediate",
    handler=_search_tracks,
)

play_tool = Tool(
    name="spotify_play",
    description=(
        "Start Spotify playback. Provide either `uris` for specific tracks "
        "or `context_uri` for an album/playlist."
    ),
    input_schema={
        "type": "object",
        "properties": {
            "uris": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Track URIs to play.",
            },
            "context_uri": {
                "type": "string",
                "description": "Album or playlist URI to start.",
            },
            "device_id": {
                "type": "string",
                "description": "Optional Spotify device id.",
            },
        },
        "additionalProperties": False,
    },
    bucket="deferred",
    handler=_play,
)

pause_tool = Tool(
    name="spotify_pause",
    description="Pause Spotify playback.",
    input_schema={
        "type": "object",
        "properties": {
            "device_id": {
                "type": "string",
                "description": "Optional Spotify device id.",
            },
        },
        "additionalProperties": False,
    },
    bucket="deferred",
    handler=_pause,
)

skip_tool = Tool(
    name="spotify_skip",
    description="Skip to the next Spotify track.",
    input_schema={
        "type": "object",
        "properties": {
            "device_id": {
                "type": "string",
                "description": "Optional Spotify device id.",
            },
        },
        "additionalProperties": False,
    },
    bucket="deferred",
    handler=_skip,
)

queue_tool = Tool(
    name="spotify_queue",
    description="Add a track URI to the Spotify queue.",
    input_schema={
        "type": "object",
        "properties": {
            "uri": {
                "type": "string",
                "description": "Track URI to queue.",
            },
            "device_id": {
                "type": "string",
                "description": "Optional Spotify device id.",
            },
        },
        "required": ["uri"],
        "additionalProperties": False,
    },
    bucket="deferred",
    handler=_queue,
)


SPOTIFY_TOOLS: list[Tool] = [
    now_playing_tool,
    search_tracks_tool,
    play_tool,
    pause_tool,
    skip_tool,
    queue_tool,
]
