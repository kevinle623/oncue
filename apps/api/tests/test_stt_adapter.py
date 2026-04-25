import json
from collections.abc import AsyncIterator
from typing import Any

from oncue.adapters.stt import deepgram


def test_parse_transcript_returns_text_and_finality() -> None:
    payload = {
        "type": "Results",
        "is_final": True,
        "channel": {"alternatives": [{"transcript": "play some jazz"}]},
    }
    result = deepgram._parse_transcript(payload)
    assert result is not None
    assert result.text == "play some jazz"
    assert result.is_final is True


def test_parse_transcript_skips_empty_text() -> None:
    payload = {
        "type": "Results",
        "is_final": False,
        "channel": {"alternatives": [{"transcript": "   "}]},
    }
    assert deepgram._parse_transcript(payload) is None


def test_parse_transcript_skips_non_results_messages() -> None:
    assert deepgram._parse_transcript({"type": "Metadata"}) is None


def test_build_url_includes_streaming_params() -> None:
    url = deepgram._build_url(
        encoding="mulaw", sample_rate=8000, model="nova-3", interim=True
    )
    assert url.startswith(deepgram.DEEPGRAM_LISTEN_URL + "?")
    assert "encoding=mulaw" in url
    assert "sample_rate=8000" in url
    assert "model=nova-3" in url
    assert "interim_results=true" in url


class _FakeWS:
    def __init__(self, messages: list[str | bytes]) -> None:
        self._messages = messages
        self.sent: list[str | bytes] = []
        self.closed = False

    async def send(self, data: str | bytes) -> None:
        self.sent.append(data)

    async def close(self) -> None:
        self.closed = True

    def __aiter__(self) -> AsyncIterator[str | bytes]:
        return self._iter()

    async def _iter(self) -> AsyncIterator[str | bytes]:
        for msg in self._messages:
            yield msg


async def test_session_yields_transcripts_in_order() -> None:
    messages: list[str | bytes] = [
        json.dumps(
            {
                "type": "Results",
                "is_final": False,
                "channel": {"alternatives": [{"transcript": "hello"}]},
            }
        ),
        b"\x00\x01",  # binary frames are skipped
        "not-json",  # malformed is skipped
        json.dumps(
            {
                "type": "Results",
                "is_final": True,
                "channel": {"alternatives": [{"transcript": "hello world"}]},
            }
        ),
    ]
    ws = _FakeWS(messages)
    session = deepgram.STTSession(ws)

    received: list[deepgram.Transcript] = []
    async for t in session.transcripts():
        received.append(t)

    assert [(t.text, t.is_final) for t in received] == [
        ("hello", False),
        ("hello world", True),
    ]


async def test_session_send_audio_writes_to_ws() -> None:
    ws = _FakeWS([])
    session = deepgram.STTSession(ws)
    await session.send_audio(b"\x10\x20\x30")
    assert ws.sent == [b"\x10\x20\x30"]


async def test_session_close_sends_close_stream_frame() -> None:
    ws = _FakeWS([])
    session = deepgram.STTSession(ws)
    await session.close()
    assert ws.closed is True
    assert any(
        isinstance(s, str) and json.loads(s).get("type") == "CloseStream"
        for s in ws.sent
    )


async def test_session_close_is_idempotent() -> None:
    ws = _FakeWS([])
    session = deepgram.STTSession(ws)
    await session.close()
    await session.close()
    sends = [s for s in ws.sent if isinstance(s, str)]
    assert len(sends) == 1


def test_module_has_open_session_factory() -> None:
    # Sanity that the factory is exported (full WS test would need a fake server).
    assert callable(deepgram.open_session)
    _ = Any  # silence "unused"
