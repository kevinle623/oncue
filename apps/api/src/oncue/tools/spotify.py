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


SPOTIFY_TOOLS: list[Tool] = [now_playing_tool, search_tracks_tool]
