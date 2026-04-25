from collections.abc import AsyncIterator, Iterator
from typing import Any

import pytest
from fastapi.testclient import TestClient

from oncue.adapters.db.postgresql import get_session
from oncue.dtos.call import CallDTO
from oncue.main import create_app
from oncue.services import call_service


class _NoopSession:
    async def commit(self) -> None:
        return None

    async def rollback(self) -> None:
        return None


async def _fake_get_session() -> AsyncIterator[Any]:
    yield _NoopSession()


@pytest.fixture
def client(monkeypatch: pytest.MonkeyPatch) -> Iterator[TestClient]:
    from oncue import settings as settings_mod

    original = settings_mod.settings.twilio_validate_signature
    settings_mod.settings.twilio_validate_signature = False

    app = create_app()
    app.dependency_overrides[get_session] = _fake_get_session

    with TestClient(app) as c:
        yield c

    settings_mod.settings.twilio_validate_signature = original
    app.dependency_overrides.clear()


def test_incoming_returns_twiml_and_registers_call(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    captured: dict[str, str] = {}

    async def fake_register(
        _session: object,
        *,
        call_sid: str,
        from_number: str,
        to_number: str,
        status: str,
    ) -> CallDTO:
        captured.update(
            call_sid=call_sid,
            from_number=from_number,
            to_number=to_number,
            status=status,
        )
        from datetime import UTC, datetime
        from uuid import uuid4

        return CallDTO(
            id=uuid4(),
            call_sid=call_sid,
            user_id=uuid4(),
            status=status,
            from_number=from_number,
            to_number=to_number,
            started_at=datetime.now(UTC),
            ended_at=None,
        )

    monkeypatch.setattr(call_service, "register_incoming_call", fake_register)

    response = client.post(
        "/voice/incoming",
        data={
            "CallSid": "CA123",
            "From": "+15551234567",
            "To": "+18001234567",
            "CallStatus": "ringing",
        },
    )

    assert response.status_code == 200
    assert response.headers["content-type"].startswith("application/xml")
    assert "<Connect>" in response.text
    assert 'value="CA123"' in response.text
    assert captured == {
        "call_sid": "CA123",
        "from_number": "+15551234567",
        "to_number": "+18001234567",
        "status": "ringing",
    }


def test_incoming_returns_400_when_required_field_missing(
    client: TestClient,
) -> None:
    response = client.post("/voice/incoming", data={"CallSid": "CA123"})
    assert response.status_code == 400


def test_status_updates_call_and_sets_ended_at_on_terminal(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    captured: dict[str, Any] = {}

    async def fake_update(
        _session: object,
        *,
        call_sid: str,
        status: str,
        ended_at: object | None = None,
    ) -> None:
        captured.update(call_sid=call_sid, status=status, ended_at=ended_at)
        return None

    monkeypatch.setattr(call_service, "update_status", fake_update)

    response = client.post(
        "/voice/status",
        data={"CallSid": "CA999", "CallStatus": "completed"},
    )

    assert response.status_code == 204
    assert captured["call_sid"] == "CA999"
    assert captured["status"] == "completed"
    assert captured["ended_at"] is not None


def test_status_does_not_set_ended_at_for_in_progress(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    captured: dict[str, Any] = {}

    async def fake_update(
        _session: object,
        *,
        call_sid: str,
        status: str,
        ended_at: object | None = None,
    ) -> None:
        captured.update(ended_at=ended_at)
        return None

    monkeypatch.setattr(call_service, "update_status", fake_update)

    response = client.post(
        "/voice/status",
        data={"CallSid": "CA1", "CallStatus": "in-progress"},
    )

    assert response.status_code == 204
    assert captured["ended_at"] is None


def test_incoming_rejects_bad_signature_when_validation_enabled(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from oncue import settings as settings_mod

    original = settings_mod.settings.twilio_validate_signature
    settings_mod.settings.twilio_validate_signature = True

    try:
        app = create_app()
        app.dependency_overrides[get_session] = _fake_get_session
        with TestClient(app) as c:
            response = c.post(
                "/voice/incoming",
                data={
                    "CallSid": "CA1",
                    "From": "+1",
                    "To": "+2",
                    "CallStatus": "ringing",
                },
                headers={"X-Twilio-Signature": "definitely-not-valid"},
            )
        assert response.status_code == 403
    finally:
        settings_mod.settings.twilio_validate_signature = original
