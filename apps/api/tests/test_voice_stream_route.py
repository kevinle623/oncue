import base64
import uuid
from collections.abc import AsyncIterator, Awaitable, Callable, Iterator
from datetime import UTC, datetime
from typing import Any

import pytest
from fastapi.testclient import TestClient
from starlette.websockets import WebSocketDisconnect

from oncue.adapters.db.postgresql import get_session
from oncue.dtos.call import CallDTO
from oncue.main import create_app
from oncue.repositories import call_repo
from oncue.services import voice_session_service


class _NoopSession:
    async def commit(self) -> None:
        return None


async def _fake_get_session() -> AsyncIterator[Any]:
    yield _NoopSession()


@pytest.fixture
def client() -> Iterator[TestClient]:
    app = create_app()
    app.dependency_overrides[get_session] = _fake_get_session
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


def _call_dto() -> CallDTO:
    return CallDTO(
        id=uuid.uuid4(),
        call_sid="CA1",
        user_id=uuid.uuid4(),
        status="in-progress",
        from_number="+1555",
        to_number="+1666",
        started_at=datetime.now(UTC),
        ended_at=None,
    )


def test_stream_resolves_call_runs_session_and_bridges_audio(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    captured: dict[str, Any] = {"chunks": []}

    async def fake_get_by_sid(_session: object, sid: str) -> CallDTO:
        captured["resolved_sid"] = sid
        return _call_dto()

    async def fake_run_session(
        _db: object,
        *,
        call: CallDTO,
        inbound_audio: AsyncIterator[bytes],
        send_audio: Callable[[bytes], Awaitable[None]],
    ) -> None:
        captured["call_sid"] = call.call_sid
        async for chunk in inbound_audio:
            captured["chunks"].append(chunk)
            await send_audio(b"\xff\xee")

    monkeypatch.setattr(call_repo, "get_by_sid", fake_get_by_sid)
    monkeypatch.setattr(voice_session_service, "run_session", fake_run_session)

    with client.websocket_connect("/voice/stream") as ws:
        ws.send_json({"event": "connected"})
        ws.send_json(
            {
                "event": "start",
                "start": {"streamSid": "ST1", "callSid": "CA1"},
            }
        )
        ws.send_json(
            {
                "event": "media",
                "media": {"payload": base64.b64encode(b"\x10\x20\x30").decode("ascii")},
            }
        )
        outbound = ws.receive_json()
        ws.send_json({"event": "stop"})

    assert captured["resolved_sid"] == "CA1"
    assert captured["call_sid"] == "CA1"
    assert captured["chunks"] == [b"\x10\x20\x30"]
    assert outbound["event"] == "media"
    assert outbound["streamSid"] == "ST1"
    assert base64.b64decode(outbound["media"]["payload"]) == b"\xff\xee"


def test_stream_closes_when_call_unknown(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    async def fake_get_by_sid(_session: object, _sid: str) -> CallDTO | None:
        return None

    monkeypatch.setattr(call_repo, "get_by_sid", fake_get_by_sid)

    with client.websocket_connect("/voice/stream") as ws:
        ws.send_json(
            {
                "event": "start",
                "start": {"streamSid": "ST1", "callSid": "missing"},
            }
        )
        with pytest.raises(WebSocketDisconnect):
            ws.receive_json()


def test_stream_exits_cleanly_on_immediate_stop(client: TestClient) -> None:
    with client.websocket_connect("/voice/stream") as ws:
        ws.send_json({"event": "stop"})
        with pytest.raises(WebSocketDisconnect):
            ws.receive_json()
