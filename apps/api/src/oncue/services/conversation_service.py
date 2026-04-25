import json
from typing import Any

from oncue.adapters.llm import anthropic as llm
from oncue.tools import REGISTRY, dispatch_immediate
from oncue.tools.base import ToolBucket, ToolContext

SYSTEM_PROMPT = (
    "You are OnCue, a hands-free voice assistant on a phone call. "
    "Keep replies short and natural for spoken delivery. "
    "Use the provided tools to answer questions about the user's music. "
    "Mutations like play, pause, skip, or queue cannot run during the call; "
    "if the user asks for one, confirm clearly that it will execute as soon "
    "as the call ends."
)

MAX_TOOL_ITERATIONS = 5


def _llm_tools_for_bucket(bucket: ToolBucket) -> list[llm.LLMTool]:
    return [
        llm.LLMTool(
            name=tool.name,
            description=tool.description,
            input_schema=tool.input_schema,
        )
        for tool in REGISTRY.values()
        if tool.bucket == bucket
    ]


async def run_turn(
    ctx: ToolContext,
    user_text: str,
    history: list[llm.LLMMessage] | None = None,
) -> tuple[str, list[llm.LLMMessage]]:
    messages: list[llm.LLMMessage] = list(history or [])
    messages.append(llm.LLMMessage(role="user", content=user_text))
    tools = _llm_tools_for_bucket("immediate")

    for _ in range(MAX_TOOL_ITERATIONS):
        response = await llm.create_message(
            system=SYSTEM_PROMPT, messages=messages, tools=tools
        )
        messages.append(
            llm.LLMMessage(role="assistant", content=list(response.content))
        )

        tool_uses = [
            block
            for block in response.content
            if isinstance(block, llm.LLMToolUseBlock)
        ]
        if not tool_uses:
            text_parts = [
                block.text
                for block in response.content
                if isinstance(block, llm.LLMTextBlock)
            ]
            return "\n".join(text_parts).strip(), messages

        results: list[llm.LLMInputBlock] = []
        for tu in tool_uses:
            try:
                result: Any = await dispatch_immediate(REGISTRY, ctx, tu.name, tu.input)
                results.append(
                    llm.LLMToolResultBlock(
                        tool_use_id=tu.id,
                        content=json.dumps(result, default=str),
                    )
                )
            except Exception as exc:
                results.append(
                    llm.LLMToolResultBlock(
                        tool_use_id=tu.id,
                        content=str(exc),
                        is_error=True,
                    )
                )

        messages.append(llm.LLMMessage(role="user", content=results))

    raise RuntimeError(f"Conversation exceeded {MAX_TOOL_ITERATIONS} tool iterations")
