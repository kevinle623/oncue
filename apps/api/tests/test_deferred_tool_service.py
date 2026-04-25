import uuid
from datetime import UTC, datetime
from typing import Any

import pytest

from oncue.dtos.call import CallDTO
from oncue.dtos.deferred_tool_job import DeferredToolJobDTO
from oncue.services import deferred_tool_service


def _call() -> CallDTO:
    now = datetime.now(UTC)
    return CallDTO(
        id=uuid.uuid4(),
        call_sid="CA42",
        user_id=uuid.uuid4(),
        status="in-progress",
        from_number="+1",
        to_number="+2",
        started_at=now,
        ended_at=None,
    )


class _NoopSession:
    async def commit(self) -> None:
        return None


async def test_enqueue_for_call_persists_job_and_pushes_redis(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    call = _call()
    pushed: list[tuple[str, str]] = []

    async def fake_create(_session: object, data: Any) -> DeferredToolJobDTO:
        return DeferredToolJobDTO(
            id=uuid.uuid4(),
            call_id=data.call_id,
            tool_name=data.tool_name,
            args=data.args,
            status=data.status,
            scheduled_for=data.scheduled_for,
            executed_at=None,
            error=None,
            created_at=datetime.now(UTC),
        )

    async def fake_rpush(key: str, value: str) -> None:
        pushed.append((key, value))

    monkeypatch.setattr(
        deferred_tool_service.deferred_tool_job_repo, "create", fake_create
    )
    monkeypatch.setattr(deferred_tool_service.redis, "rpush", fake_rpush)

    job = await deferred_tool_service.enqueue_for_call(
        _NoopSession(),  # type: ignore[arg-type]
        call=call,
        tool_name="spotify_pause",
        arguments={},
    )

    assert job.tool_name == "spotify_pause"
    assert pushed == [("deferred:call:CA42", str(job.id))]


async def test_run_queued_for_call_executes_success_and_failure(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    now = datetime.now(UTC)
    call = _call()
    good_id = uuid.uuid4()
    bad_id = uuid.uuid4()
    succeeded: list[uuid.UUID] = []
    failed: list[uuid.UUID] = []

    jobs = [
        DeferredToolJobDTO(
            id=good_id,
            call_id=call.id,
            tool_name="spotify_pause",
            args={},
            status="pending",
            scheduled_for=now,
            executed_at=None,
            error=None,
            created_at=now,
        ),
        DeferredToolJobDTO(
            id=bad_id,
            call_id=call.id,
            tool_name="spotify_skip",
            args={},
            status="pending",
            scheduled_for=now,
            executed_at=None,
            error=None,
            created_at=now,
        ),
    ]

    async def fake_lrange(_key: str, _start: int, _end: int) -> list[str]:
        return [str(good_id), str(bad_id), "not-a-uuid"]

    async def fake_delete(_key: str) -> int:
        return 1

    async def fake_list_pending_due_by_ids(
        _session: object,
        *,
        job_ids: list[uuid.UUID],
        scheduled_before: datetime,
    ) -> list[DeferredToolJobDTO]:
        assert set(job_ids) == {good_id, bad_id}
        assert scheduled_before <= datetime.now(UTC)
        return jobs

    async def fake_get_by_id(_session: object, _call_id: uuid.UUID) -> CallDTO:
        return call

    async def fake_dispatch(
        _registry: dict[str, Any],
        _ctx: Any,
        name: str,
        arguments: dict[str, Any],
    ) -> dict[str, Any]:
        if name == "spotify_skip":
            raise RuntimeError("upstream failed")
        assert arguments == {}
        return {"ok": True}

    async def fake_mark_succeeded(
        _session: object,
        *,
        job_id: uuid.UUID,
        executed_at: datetime,
    ) -> DeferredToolJobDTO | None:
        assert executed_at <= datetime.now(UTC)
        succeeded.append(job_id)
        return jobs[0]

    async def fake_mark_failed(
        _session: object,
        *,
        job_id: uuid.UUID,
        executed_at: datetime,
        error: str,
    ) -> DeferredToolJobDTO | None:
        assert executed_at <= datetime.now(UTC)
        assert "upstream failed" in error
        failed.append(job_id)
        return jobs[1]

    monkeypatch.setattr(deferred_tool_service.redis, "lrange", fake_lrange)
    monkeypatch.setattr(deferred_tool_service.redis, "delete", fake_delete)
    monkeypatch.setattr(
        deferred_tool_service.deferred_tool_job_repo,
        "list_pending_due_by_ids",
        fake_list_pending_due_by_ids,
    )
    monkeypatch.setattr(deferred_tool_service.call_repo, "get_by_id", fake_get_by_id)
    monkeypatch.setattr(deferred_tool_service, "dispatch_deferred", fake_dispatch)
    monkeypatch.setattr(
        deferred_tool_service.deferred_tool_job_repo,
        "mark_succeeded",
        fake_mark_succeeded,
    )
    monkeypatch.setattr(
        deferred_tool_service.deferred_tool_job_repo,
        "mark_failed",
        fake_mark_failed,
    )

    executed = await deferred_tool_service.run_queued_for_call(
        _NoopSession(),  # type: ignore[arg-type]
        call_sid="CA42",
    )

    assert executed == 1
    assert succeeded == [good_id]
    assert failed == [bad_id]
