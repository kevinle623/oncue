import json
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from dataclasses import dataclass
from typing import Any, Protocol
from urllib.parse import urlencode

import websockets

from oncue.settings import settings

DEEPGRAM_LISTEN_URL = "wss://api.deepgram.com/v1/listen"
DEFAULT_MODEL = "nova-3"


@dataclass(frozen=True)
class Transcript:
    text: str
    is_final: bool


class _WebSocketLike(Protocol):
    async def send(self, data: str | bytes) -> None: ...
    async def close(self) -> None: ...
    def __aiter__(self) -> AsyncIterator[str | bytes]: ...


class STTSession:
    def __init__(self, ws: _WebSocketLike) -> None:
        self._ws = ws
        self._closed = False

    async def send_audio(self, chunk: bytes) -> None:
        await self._ws.send(chunk)

    async def transcripts(self) -> AsyncIterator[Transcript]:
        async for raw in self._ws:
            if isinstance(raw, bytes):
                continue
            try:
                payload = json.loads(raw)
            except json.JSONDecodeError:
                continue
            transcript = _parse_transcript(payload)
            if transcript is not None:
                yield transcript

    async def close(self) -> None:
        if self._closed:
            return
        self._closed = True
        try:
            await self._ws.send(json.dumps({"type": "CloseStream"}))
        except Exception:
            pass
        await self._ws.close()


def _parse_transcript(payload: dict[str, Any]) -> Transcript | None:
    msg_type = payload.get("type")
    if msg_type not in (None, "Results"):
        return None
    channel = payload.get("channel") or {}
    alternatives = channel.get("alternatives") or []
    if not alternatives:
        return None
    text = (alternatives[0].get("transcript") or "").strip()
    if not text:
        return None
    return Transcript(text=text, is_final=bool(payload.get("is_final", False)))


def _build_url(*, encoding: str, sample_rate: int, model: str, interim: bool) -> str:
    params = {
        "encoding": encoding,
        "sample_rate": str(sample_rate),
        "channels": "1",
        "model": model,
        "interim_results": "true" if interim else "false",
    }
    return f"{DEEPGRAM_LISTEN_URL}?{urlencode(params)}"


@asynccontextmanager
async def open_session(
    *,
    encoding: str = "mulaw",
    sample_rate: int = 8000,
    model: str = DEFAULT_MODEL,
    interim_results: bool = True,
) -> AsyncIterator[STTSession]:
    url = _build_url(
        encoding=encoding,
        sample_rate=sample_rate,
        model=model,
        interim=interim_results,
    )
    headers = [("Authorization", f"Token {settings.deepgram_api_key}")]
    async with websockets.connect(url, additional_headers=headers) as ws:
        session = STTSession(ws)
        try:
            yield session
        finally:
            await session.close()
