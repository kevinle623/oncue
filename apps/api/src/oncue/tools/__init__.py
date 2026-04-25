from oncue.tools.base import (
    Tool,
    ToolContext,
    ToolNotAllowedError,
    UnknownToolError,
    build_registry,
    dispatch_immediate,
)
from oncue.tools.spotify import SPOTIFY_TOOLS

ALL_TOOLS: list[Tool] = [*SPOTIFY_TOOLS]
REGISTRY: dict[str, Tool] = build_registry(ALL_TOOLS)

__all__ = [
    "ALL_TOOLS",
    "REGISTRY",
    "Tool",
    "ToolContext",
    "ToolNotAllowedError",
    "UnknownToolError",
    "build_registry",
    "dispatch_immediate",
]
