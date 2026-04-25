import asyncio
from collections.abc import AsyncIterator, Awaitable, Callable

from sqlalchemy.ext.asyncio import AsyncSession

from oncue.adapters.llm import anthropic as llm
from oncue.adapters.stt import deepgram as stt
from oncue.adapters.tts import elevenlabs as tts
from oncue.dtos.call import CallDTO
from oncue.dtos.call_turn import CallTurnCreateDTO
from oncue.repositories import call_turn_repo
from oncue.services import conversation_service
from oncue.tools.base import ToolContext

SendAudioFn = Callable[[bytes], Awaitable[None]]


class CallNotLinkedError(RuntimeError):
    """Raised when a call has no associated user (cannot run tools)."""


async def run_session(
    db_session: AsyncSession,
    *,
    call: CallDTO,
    inbound_audio: AsyncIterator[bytes],
    send_audio: SendAudioFn,
) -> None:
    if call.user_id is None:
        raise CallNotLinkedError(f"Call {call.call_sid} has no associated user")

    ctx = ToolContext(session=db_session, user_id=call.user_id)
    history: list[llm.LLMMessage] = []
    speak_task: asyncio.Task[None] | None = None

    async with stt.open_session() as stt_session:
        pump_task = asyncio.create_task(_pump_audio(inbound_audio, stt_session))
        should_cancel_speak = True
        try:
            async for transcript in stt_session.transcripts():
                if not transcript.is_final:
                    _cancel(speak_task)
                    speak_task = None
                    continue

                _cancel(speak_task)
                speak_task = None

                await call_turn_repo.create(
                    db_session,
                    CallTurnCreateDTO(
                        call_id=call.id,
                        role="user",
                        transcript=transcript.text,
                    ),
                )

                reply, history = await conversation_service.run_turn(
                    ctx, transcript.text, history
                )

                await call_turn_repo.create(
                    db_session,
                    CallTurnCreateDTO(
                        call_id=call.id,
                        role="assistant",
                        transcript=reply,
                    ),
                )
                await db_session.commit()

                if reply:
                    speak_task = asyncio.create_task(_speak(reply, send_audio))
            should_cancel_speak = False
        finally:
            if speak_task is not None:
                if should_cancel_speak and not speak_task.done():
                    speak_task.cancel()
                await asyncio.gather(speak_task, return_exceptions=True)
            pump_task.cancel()
            await asyncio.gather(pump_task, return_exceptions=True)


def _cancel(task: asyncio.Task[None] | None) -> None:
    if task is not None and not task.done():
        task.cancel()
    return None


async def _pump_audio(audio: AsyncIterator[bytes], stt_session: stt.STTSession) -> None:
    async for chunk in audio:
        await stt_session.send_audio(chunk)


async def _speak(text: str, send_audio: SendAudioFn) -> None:
    async for chunk in tts.synthesize(text):
        await send_audio(chunk)
