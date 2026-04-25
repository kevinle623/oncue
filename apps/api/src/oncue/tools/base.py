import uuid
from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from typing import Any, Literal

from sqlalchemy.ext.asyncio import AsyncSession

ToolBucket = Literal["immediate", "deferred"]


@dataclass(frozen=True)
class ToolContext:
    session: AsyncSession
    user_id: uuid.UUID


ToolHandler = Callable[[ToolContext, dict[str, Any]], Awaitable[Any]]


@dataclass(frozen=True)
class Tool:
    name: str
    description: str
    input_schema: dict[str, Any]
    bucket: ToolBucket
    handler: ToolHandler


class UnknownToolError(KeyError):
    pass


class ToolNotAllowedError(RuntimeError):
    """Raised when a deferred tool is invoked during an active call."""


def build_registry(tools: list[Tool]) -> dict[str, Tool]:
    registry: dict[str, Tool] = {}
    for tool in tools:
        if tool.name in registry:
            raise ValueError(f"Duplicate tool name: {tool.name}")
        registry[tool.name] = tool
    return registry


async def dispatch_immediate(
    registry: dict[str, Tool],
    ctx: ToolContext,
    name: str,
    arguments: dict[str, Any],
) -> Any:
    tool = registry.get(name)
    if tool is None:
        raise UnknownToolError(name)
    if tool.bucket != "immediate":
        raise ToolNotAllowedError(
            f"Tool {name!r} is deferred and cannot run during an active call"
        )
    return await tool.handler(ctx, arguments)
