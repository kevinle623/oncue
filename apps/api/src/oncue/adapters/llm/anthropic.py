from collections.abc import Sequence
from dataclasses import dataclass
from typing import Any, Literal, cast

from anthropic import AsyncAnthropic

from oncue.settings import settings

DEFAULT_MODEL = "claude-haiku-4-5-20251001"
DEFAULT_MAX_TOKENS = 1024


@dataclass(frozen=True)
class LLMTextBlock:
    text: str


@dataclass(frozen=True)
class LLMToolUseBlock:
    id: str
    name: str
    input: dict[str, Any]


@dataclass(frozen=True)
class LLMToolResultBlock:
    tool_use_id: str
    content: str
    is_error: bool = False


LLMOutputBlock = LLMTextBlock | LLMToolUseBlock
LLMInputBlock = LLMTextBlock | LLMToolUseBlock | LLMToolResultBlock


@dataclass(frozen=True)
class LLMMessage:
    role: Literal["user", "assistant"]
    content: str | Sequence[LLMInputBlock]


@dataclass(frozen=True)
class LLMTool:
    name: str
    description: str
    input_schema: dict[str, Any]


@dataclass(frozen=True)
class LLMResponse:
    content: list[LLMOutputBlock]
    stop_reason: str


_client: AsyncAnthropic | None = None


def _get_client() -> AsyncAnthropic:
    global _client
    if _client is None:
        _client = AsyncAnthropic(api_key=settings.anthropic_api_key)
    return _client


def _serialize_block(block: LLMInputBlock) -> dict[str, Any]:
    if isinstance(block, LLMTextBlock):
        return {"type": "text", "text": block.text}
    if isinstance(block, LLMToolUseBlock):
        return {
            "type": "tool_use",
            "id": block.id,
            "name": block.name,
            "input": block.input,
        }
    return {
        "type": "tool_result",
        "tool_use_id": block.tool_use_id,
        "content": block.content,
        "is_error": block.is_error,
    }


def _serialize_message(msg: LLMMessage) -> dict[str, Any]:
    if isinstance(msg.content, str):
        return {"role": msg.role, "content": msg.content}
    return {
        "role": msg.role,
        "content": [_serialize_block(b) for b in msg.content],
    }


def _parse_response(response: Any) -> LLMResponse:
    blocks: list[LLMOutputBlock] = []
    for block in response.content:
        btype = getattr(block, "type", None)
        if btype == "text":
            blocks.append(LLMTextBlock(text=str(block.text)))
        elif btype == "tool_use":
            blocks.append(
                LLMToolUseBlock(
                    id=str(block.id),
                    name=str(block.name),
                    input=dict(block.input or {}),
                )
            )
    return LLMResponse(content=blocks, stop_reason=str(response.stop_reason))


async def create_message(
    *,
    system: str,
    messages: Sequence[LLMMessage],
    tools: Sequence[LLMTool] = (),
    model: str = DEFAULT_MODEL,
    max_tokens: int = DEFAULT_MAX_TOKENS,
) -> LLMResponse:
    client = _get_client()
    response = await client.messages.create(
        model=model,
        system=system,
        max_tokens=max_tokens,
        messages=cast(Any, [_serialize_message(m) for m in messages]),
        tools=cast(
            Any,
            [
                {
                    "name": t.name,
                    "description": t.description,
                    "input_schema": t.input_schema,
                }
                for t in tools
            ],
        ),
    )
    return _parse_response(response)
