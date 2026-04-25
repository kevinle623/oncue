import uuid
from collections.abc import AsyncIterator, Sequence
from contextlib import asynccontextmanager
from datetime import UTC, datetime
from typing import Any

import pytest

from oncue.adapters.llm import anthropic as llm
from oncue.adapters.stt import deepgram as stt
from oncue.adapters.tts import elevenlabs as tts
from oncue.dtos.call import CallDTO
from oncue.dtos.call_turn import CallTurnCreateDTO, CallTurnDTO
from oncue.repositories import call_turn_repo
from oncue.services import conversation_service, voice_session_service


def _call(user_id: uuid.UUID | None = None) -> CallDTO:
    now = datetime.now(UTC)
    return CallDTO(
        id=uuid.uuid4(),
        call_sid="CA-test",
        user_id=user_id or uuid.uuid4(),
        status="in-progress",
        from_number="+1555",
        to_number="+1666",
        started_at=now,
        ended_at=None,
    )


class _FakeSTTSession:
    def __init__(self, transcripts: Sequence[stt.Transcript]) -> None:
        self._transcripts = list(transcripts)
        self.received_audio: list[bytes] = []

    async def send_audio(self, chunk: bytes) -> None:
        self.received_audio.append(chunk)

    async def transcripts(self) -> AsyncIterator[stt.Transcript]:
        for t in self._transcripts:
            yield t


def _patch_stt(
    monkeypatch: pytest.MonkeyPatch, transcripts: Sequence[stt.Transcript]
) -> None:
    @asynccontextmanager
    async def _open(**_kwargs: Any) -> AsyncIterator[_FakeSTTSession]:
        yield _FakeSTTSession(transcripts)

    monkeypatch.setattr(stt, "open_session", _open)


def _patch_tts(monkeypatch: pytest.MonkeyPatch, chunks: Sequence[bytes]) -> None:
    async def fake_synthesize(_text: str, **_kwargs: Any) -> AsyncIterator[bytes]:
        for c in chunks:
            yield c

    monkeypatch.setattr(tts, "synthesize", fake_synthesize)


class _NoopSession:
    async def commit(self) -> None:
        return None


async def _empty_audio() -> AsyncIterator[bytes]:
    if False:
        yield b""  # pragma: no cover


def _patch_call_turn_repo(
    monkeypatch: pytest.MonkeyPatch,
) -> list[CallTurnCreateDTO]:
    captured: list[CallTurnCreateDTO] = []

    async def fake_create(_session: object, data: CallTurnCreateDTO) -> CallTurnDTO:
        captured.append(data)
        return CallTurnDTO(
            id=uuid.uuid4(),
            call_id=data.call_id,
            role=data.role,
            transcript=data.transcript,
            tool_calls=data.tool_calls,
            created_at=datetime.now(UTC),
        )

    monkeypatch.setattr(call_turn_repo, "create", fake_create)
    return captured


async def test_run_session_processes_final_transcript_end_to_end(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _patch_stt(monkeypatch, [stt.Transcript(text="play jazz", is_final=True)])
    _patch_tts(monkeypatch, [b"\x01\x02", b"\x03"])
    turns = _patch_call_turn_repo(monkeypatch)

    async def fake_run_turn(
        _ctx: object, user_text: str, history: list[llm.LLMMessage] | None
    ) -> tuple[str, list[llm.LLMMessage]]:
        assert user_text == "play jazz"
        return "Sure thing.", [llm.LLMMessage(role="user", content=user_text)]

    monkeypatch.setattr(conversation_service, "run_turn", fake_run_turn)

    sent: list[bytes] = []

    async def send_audio(chunk: bytes) -> None:
        sent.append(chunk)

    call = _call()
    await voice_session_service.run_session(
        _NoopSession(),  # type: ignore[arg-type]
        call=call,
        inbound_audio=_empty_audio(),
        send_audio=send_audio,
    )

    assert [t.role for t in turns] == ["user", "assistant"]
    assert turns[0].transcript == "play jazz"
    assert turns[1].transcript == "Sure thing."
    assert sent == [b"\x01\x02", b"\x03"]


async def test_run_session_threads_history_across_turns(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _patch_stt(
        monkeypatch,
        [
            stt.Transcript(text="first", is_final=True),
            stt.Transcript(text="second", is_final=True),
        ],
    )
    _patch_tts(monkeypatch, [b"x"])
    _patch_call_turn_repo(monkeypatch)

    seen_histories: list[int] = []

    async def fake_run_turn(
        _ctx: object, user_text: str, history: list[llm.LLMMessage] | None
    ) -> tuple[str, list[llm.LLMMessage]]:
        seen_histories.append(len(history or []))
        new_history = list(history or [])
        new_history.append(llm.LLMMessage(role="user", content=user_text))
        new_history.append(llm.LLMMessage(role="assistant", content="ok"))
        return "ok", new_history

    monkeypatch.setattr(conversation_service, "run_turn", fake_run_turn)

    async def send_audio(_chunk: bytes) -> None:
        return None

    await voice_session_service.run_session(
        _NoopSession(),  # type: ignore[arg-type]
        call=_call(),
        inbound_audio=_empty_audio(),
        send_audio=send_audio,
    )

    assert seen_histories == [0, 2]


async def test_run_session_skips_interim_transcripts(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _patch_stt(
        monkeypatch,
        [
            stt.Transcript(text="par", is_final=False),
            stt.Transcript(text="partial", is_final=False),
        ],
    )
    _patch_tts(monkeypatch, [b"x"])
    turns = _patch_call_turn_repo(monkeypatch)

    called = False

    async def fake_run_turn(*_args: Any, **_kwargs: Any) -> tuple[str, list[Any]]:
        nonlocal called
        called = True
        return "", []

    monkeypatch.setattr(conversation_service, "run_turn", fake_run_turn)

    async def send_audio(_chunk: bytes) -> None:
        return None

    await voice_session_service.run_session(
        _NoopSession(),  # type: ignore[arg-type]
        call=_call(),
        inbound_audio=_empty_audio(),
        send_audio=send_audio,
    )

    assert called is False
    assert turns == []


async def test_run_session_raises_when_call_has_no_user(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _patch_stt(monkeypatch, [])

    call = CallDTO(
        id=uuid.uuid4(),
        call_sid="CA-x",
        user_id=None,
        status="in-progress",
        from_number="+1",
        to_number="+2",
        started_at=datetime.now(UTC),
        ended_at=None,
    )

    async def send_audio(_chunk: bytes) -> None:
        return None

    with pytest.raises(voice_session_service.CallNotLinkedError):
        await voice_session_service.run_session(
            _NoopSession(),  # type: ignore[arg-type]
            call=call,
            inbound_audio=_empty_audio(),
            send_audio=send_audio,
        )
