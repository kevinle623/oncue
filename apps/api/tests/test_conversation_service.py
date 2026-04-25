import json
import uuid
from collections.abc import Sequence
from typing import Any

import pytest

from oncue.adapters.llm import anthropic as llm
from oncue.services import conversation_service
from oncue.tools.base import ToolContext


def _ctx() -> ToolContext:
    return ToolContext(session=None, user_id=uuid.uuid4())  # type: ignore[arg-type]


async def test_run_turn_returns_text_when_no_tool_use(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    async def fake_create(
        *,
        system: str,
        messages: Sequence[llm.LLMMessage],
        tools: Sequence[llm.LLMTool] = (),
        model: str = "",
        max_tokens: int = 0,
    ) -> llm.LLMResponse:
        return llm.LLMResponse(
            content=[llm.LLMTextBlock(text="Hello there.")],
            stop_reason="end_turn",
        )

    monkeypatch.setattr(llm, "create_message", fake_create)

    text, history = await conversation_service.run_turn(_ctx(), "hi")

    assert text == "Hello there."
    assert len(history) == 2
    assert history[0].role == "user"
    assert history[1].role == "assistant"


async def test_run_turn_runs_tool_then_returns_text(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    call_count = 0

    async def fake_create(
        *,
        system: str,
        messages: Sequence[llm.LLMMessage],
        tools: Sequence[llm.LLMTool] = (),
        model: str = "",
        max_tokens: int = 0,
    ) -> llm.LLMResponse:
        nonlocal call_count
        call_count += 1
        if call_count == 1:
            assert any(t.name == "spotify_search_tracks" for t in tools)
            return llm.LLMResponse(
                content=[
                    llm.LLMToolUseBlock(
                        id="tu_1",
                        name="spotify_search_tracks",
                        input={"query": "miles davis"},
                    )
                ],
                stop_reason="tool_use",
            )
        return llm.LLMResponse(
            content=[llm.LLMTextBlock(text="Found So What.")],
            stop_reason="end_turn",
        )

    async def fake_dispatch(
        _registry: dict[str, Any],
        _ctx: ToolContext,
        name: str,
        arguments: dict[str, Any],
    ) -> dict[str, Any]:
        assert name == "spotify_search_tracks"
        assert arguments == {"query": "miles davis"}
        return {"tracks": [{"name": "So What"}]}

    monkeypatch.setattr(llm, "create_message", fake_create)
    monkeypatch.setattr(conversation_service, "dispatch_immediate", fake_dispatch)

    text, history = await conversation_service.run_turn(_ctx(), "find miles davis")

    assert text == "Found So What."
    assert call_count == 2

    tool_result_msg = history[-2]
    assert tool_result_msg.role == "user"
    assert isinstance(tool_result_msg.content, list)
    block = tool_result_msg.content[0]
    assert isinstance(block, llm.LLMToolResultBlock)
    assert block.tool_use_id == "tu_1"
    assert json.loads(block.content) == {"tracks": [{"name": "So What"}]}
    assert block.is_error is False


async def test_run_turn_records_tool_error_and_continues(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    call_count = 0

    async def fake_create(
        *,
        system: str,
        messages: Sequence[llm.LLMMessage],
        tools: Sequence[llm.LLMTool] = (),
        model: str = "",
        max_tokens: int = 0,
    ) -> llm.LLMResponse:
        nonlocal call_count
        call_count += 1
        if call_count == 1:
            return llm.LLMResponse(
                content=[
                    llm.LLMToolUseBlock(
                        id="tu_x",
                        name="spotify_search_tracks",
                        input={"query": "x"},
                    )
                ],
                stop_reason="tool_use",
            )
        return llm.LLMResponse(
            content=[llm.LLMTextBlock(text="Sorry, search failed.")],
            stop_reason="end_turn",
        )

    async def fake_dispatch(
        _registry: dict[str, Any],
        _ctx: ToolContext,
        _name: str,
        _arguments: dict[str, Any],
    ) -> dict[str, Any]:
        raise RuntimeError("upstream 500")

    monkeypatch.setattr(llm, "create_message", fake_create)
    monkeypatch.setattr(conversation_service, "dispatch_immediate", fake_dispatch)

    text, history = await conversation_service.run_turn(_ctx(), "find x")

    assert text == "Sorry, search failed."
    tool_result_msg = history[-2]
    assert isinstance(tool_result_msg.content, list)
    block = tool_result_msg.content[0]
    assert isinstance(block, llm.LLMToolResultBlock)
    assert block.is_error is True
    assert "upstream 500" in block.content


async def test_run_turn_raises_when_iteration_cap_exceeded(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    async def fake_create(
        *,
        system: str,
        messages: Sequence[llm.LLMMessage],
        tools: Sequence[llm.LLMTool] = (),
        model: str = "",
        max_tokens: int = 0,
    ) -> llm.LLMResponse:
        return llm.LLMResponse(
            content=[
                llm.LLMToolUseBlock(id="loop", name="spotify_now_playing", input={})
            ],
            stop_reason="tool_use",
        )

    async def fake_dispatch(
        _registry: dict[str, Any],
        _ctx: ToolContext,
        _name: str,
        _arguments: dict[str, Any],
    ) -> dict[str, Any]:
        return {}

    monkeypatch.setattr(llm, "create_message", fake_create)
    monkeypatch.setattr(conversation_service, "dispatch_immediate", fake_dispatch)

    with pytest.raises(RuntimeError, match="exceeded"):
        await conversation_service.run_turn(_ctx(), "loop")
