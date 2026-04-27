import uuid
from datetime import UTC, datetime
from typing import Any

import pytest

from oncue.adapters.music.spotify import SpotifyAPIError
from oncue.dtos.call import CallDTO
from oncue.dtos.deferred_tool_job import DeferredToolJobDTO
from oncue.services import deferred_tool_service
from oncue.tools.base import UnknownToolError


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
            attempts=0,
            max_attempts=3,
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


async def test_enqueue_for_call_survives_redis_push_failure(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    call = _call()
    now = datetime.now(UTC)

    async def fake_create(_session: object, _data: Any) -> DeferredToolJobDTO:
        return DeferredToolJobDTO(
            id=uuid.uuid4(),
            call_id=call.id,
            tool_name="spotify_pause",
            args={},
            status="pending",
            scheduled_for=now,
            executed_at=None,
            error=None,
            attempts=0,
            max_attempts=3,
            created_at=now,
        )

    async def fake_rpush(_key: str, _value: str) -> None:
        raise RuntimeError("redis unavailable")

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

    assert job.call_id == call.id
    assert job.tool_name == "spotify_pause"


async def test_run_queued_for_call_executes_success_failure_and_prunes_queue(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    now = datetime.now(UTC)
    call = _call()
    good_id = uuid.uuid4()
    bad_id = uuid.uuid4()
    db_only_id = uuid.uuid4()
    done_id = uuid.uuid4()
    succeeded: list[uuid.UUID] = []
    failed: list[uuid.UUID] = []
    removed_ids: list[str] = []

    due_jobs = [
        DeferredToolJobDTO(
            id=good_id,
            call_id=call.id,
            tool_name="spotify_pause",
            args={},
            status="pending",
            scheduled_for=now,
            executed_at=None,
            error=None,
            attempts=0,
            max_attempts=3,
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
            attempts=0,
            max_attempts=3,
            created_at=now,
        ),
        DeferredToolJobDTO(
            id=db_only_id,
            call_id=call.id,
            tool_name="spotify_pause",
            args={},
            status="pending",
            scheduled_for=now,
            executed_at=None,
            error=None,
            attempts=0,
            max_attempts=3,
            created_at=now,
        ),
    ]

    async def fake_lrange(_key: str, _start: int, _end: int) -> list[str]:
        return [str(good_id), str(done_id), "not-a-uuid", str(bad_id)]

    async def fake_lrem(_key: str, _count: int, value: str) -> int:
        removed_ids.append(value)
        return 1

    async def fake_get_by_sid(_session: object, _call_sid: str) -> CallDTO:
        return call

    async def fake_get_by_id(_session: object, _call_id: uuid.UUID) -> CallDTO:
        return call

    async def fake_list_due_pending_or_stale_processing_for_call(
        _session: object,
        *,
        call_id: uuid.UUID,
        scheduled_before: datetime,
        processing_stale_before: datetime,
    ) -> list[DeferredToolJobDTO]:
        assert call_id == call.id
        assert scheduled_before <= datetime.now(UTC)
        assert processing_stale_before <= datetime.now(UTC)
        return due_jobs

    async def fake_claim_for_execution(
        _session: object,
        *,
        job_id: uuid.UUID,
        scheduled_before: datetime,
        processing_stale_before: datetime,
        claimed_at: datetime,
    ) -> DeferredToolJobDTO | None:
        assert scheduled_before <= datetime.now(UTC)
        assert processing_stale_before <= datetime.now(UTC)
        assert claimed_at <= datetime.now(UTC)
        if job_id == done_id:
            return None
        if job_id == good_id:
            return due_jobs[0]
        if job_id == bad_id:
            return due_jobs[1]
        if job_id == db_only_id:
            return due_jobs[2]
        return None

    async def fake_dispatch(
        _registry: dict[str, Any],
        _ctx: Any,
        name: str,
        arguments: dict[str, Any],
    ) -> dict[str, Any]:
        if name == "spotify_skip":
            raise UnknownToolError("upstream failed")
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
        return due_jobs[0]

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
        return due_jobs[1]

    async def fake_get_job_by_id(
        _session: object, job_id: uuid.UUID
    ) -> DeferredToolJobDTO | None:
        if job_id == done_id:
            return DeferredToolJobDTO(
                id=done_id,
                call_id=call.id,
                tool_name="spotify_pause",
                args={},
                status="succeeded",
                scheduled_for=now,
                executed_at=now,
                error=None,
                attempts=0,
                max_attempts=3,
                created_at=now,
            )
        return None

    monkeypatch.setattr(deferred_tool_service.redis, "lrange", fake_lrange)
    monkeypatch.setattr(deferred_tool_service.redis, "lrem", fake_lrem)
    monkeypatch.setattr(deferred_tool_service.call_repo, "get_by_sid", fake_get_by_sid)
    monkeypatch.setattr(deferred_tool_service.call_repo, "get_by_id", fake_get_by_id)
    monkeypatch.setattr(
        deferred_tool_service.deferred_tool_job_repo,
        "list_due_pending_or_stale_processing_for_call",
        fake_list_due_pending_or_stale_processing_for_call,
    )
    monkeypatch.setattr(
        deferred_tool_service.deferred_tool_job_repo,
        "claim_for_execution",
        fake_claim_for_execution,
    )
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
    monkeypatch.setattr(
        deferred_tool_service.deferred_tool_job_repo,
        "get_by_id",
        fake_get_job_by_id,
    )

    result = await deferred_tool_service.run_queued_for_call(
        _NoopSession(),  # type: ignore[arg-type]
        call_sid="CA42",
    )

    assert result.executed == 2
    assert result.next_retry_at is None
    assert succeeded == [good_id, db_only_id]
    assert failed == [bad_id]
    assert set(removed_ids) == {
        "not-a-uuid",
        str(good_id),
        str(bad_id),
        str(db_only_id),
        str(done_id),
    }


def _patch_for_single_job(
    monkeypatch: pytest.MonkeyPatch,
    *,
    job: DeferredToolJobDTO,
    call: CallDTO,
    raise_exc: Exception,
    retried: list[tuple[uuid.UUID, datetime]],
    failed: list[tuple[uuid.UUID, str]],
    removed_ids: list[str],
) -> None:
    async def fake_lrange(_key: str, _start: int, _end: int) -> list[str]:
        return [str(job.id)]

    async def fake_lrem(_key: str, _count: int, value: str) -> int:
        removed_ids.append(value)
        return 1

    async def fake_get_by_sid(_session: object, _sid: str) -> CallDTO:
        return call

    async def fake_get_by_id_call(_session: object, _id: uuid.UUID) -> CallDTO:
        return call

    async def fake_list_due(
        _session: object,
        *,
        call_id: uuid.UUID,
        scheduled_before: datetime,
        processing_stale_before: datetime,
    ) -> list[DeferredToolJobDTO]:
        return [job]

    async def fake_claim(
        _session: object,
        *,
        job_id: uuid.UUID,
        scheduled_before: datetime,
        processing_stale_before: datetime,
        claimed_at: datetime,
    ) -> DeferredToolJobDTO | None:
        return job if job_id == job.id else None

    async def fake_dispatch(
        _registry: dict[str, Any],
        _ctx: Any,
        _name: str,
        _arguments: dict[str, Any],
    ) -> dict[str, Any]:
        raise raise_exc

    async def fake_mark_for_retry(
        _session: object,
        *,
        job_id: uuid.UUID,
        executed_at: datetime,
        error: str,
        next_scheduled_for: datetime,
    ) -> DeferredToolJobDTO | None:
        retried.append((job_id, next_scheduled_for))
        return job

    async def fake_mark_failed(
        _session: object,
        *,
        job_id: uuid.UUID,
        executed_at: datetime,
        error: str,
    ) -> DeferredToolJobDTO | None:
        failed.append((job_id, error))
        return job

    async def fake_get_by_id_job(
        _session: object, job_id: uuid.UUID
    ) -> DeferredToolJobDTO | None:
        return job if job_id == job.id else None

    monkeypatch.setattr(deferred_tool_service.redis, "lrange", fake_lrange)
    monkeypatch.setattr(deferred_tool_service.redis, "lrem", fake_lrem)
    monkeypatch.setattr(deferred_tool_service.call_repo, "get_by_sid", fake_get_by_sid)
    monkeypatch.setattr(
        deferred_tool_service.call_repo, "get_by_id", fake_get_by_id_call
    )
    monkeypatch.setattr(
        deferred_tool_service.deferred_tool_job_repo,
        "list_due_pending_or_stale_processing_for_call",
        fake_list_due,
    )
    monkeypatch.setattr(
        deferred_tool_service.deferred_tool_job_repo, "claim_for_execution", fake_claim
    )
    monkeypatch.setattr(deferred_tool_service, "dispatch_deferred", fake_dispatch)
    monkeypatch.setattr(
        deferred_tool_service.deferred_tool_job_repo,
        "mark_for_retry",
        fake_mark_for_retry,
    )
    monkeypatch.setattr(
        deferred_tool_service.deferred_tool_job_repo, "mark_failed", fake_mark_failed
    )
    monkeypatch.setattr(
        deferred_tool_service.deferred_tool_job_repo, "get_by_id", fake_get_by_id_job
    )


def _job(call: CallDTO, *, attempts: int, max_attempts: int = 3) -> DeferredToolJobDTO:
    now = datetime.now(UTC)
    return DeferredToolJobDTO(
        id=uuid.uuid4(),
        call_id=call.id,
        tool_name="spotify_pause",
        args={},
        status="pending",
        scheduled_for=now,
        executed_at=None,
        error=None,
        attempts=attempts,
        max_attempts=max_attempts,
        created_at=now,
    )


async def test_transient_failure_reschedules_with_backoff(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    call = _call()
    job = _job(call, attempts=0)
    retried: list[tuple[uuid.UUID, datetime]] = []
    failed: list[tuple[uuid.UUID, str]] = []
    removed_ids: list[str] = []

    _patch_for_single_job(
        monkeypatch,
        job=job,
        call=call,
        raise_exc=SpotifyAPIError(503, "service unavailable"),
        retried=retried,
        failed=failed,
        removed_ids=removed_ids,
    )

    result = await deferred_tool_service.run_queued_for_call(
        _NoopSession(),  # type: ignore[arg-type]
        call_sid=call.call_sid,
    )

    assert result.executed == 0
    assert len(retried) == 1
    assert retried[0][0] == job.id
    assert retried[0][1] > datetime.now(UTC)
    assert result.next_retry_at == retried[0][1]
    assert failed == []
    # Retried jobs must stay in the redis queue so the worker can pick them up
    assert str(job.id) not in removed_ids


async def test_permanent_failure_marks_failed_without_retry(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    call = _call()
    job = _job(call, attempts=0)
    retried: list[tuple[uuid.UUID, datetime]] = []
    failed: list[tuple[uuid.UUID, str]] = []
    removed_ids: list[str] = []

    _patch_for_single_job(
        monkeypatch,
        job=job,
        call=call,
        raise_exc=SpotifyAPIError(403, "forbidden"),
        retried=retried,
        failed=failed,
        removed_ids=removed_ids,
    )

    result = await deferred_tool_service.run_queued_for_call(
        _NoopSession(),  # type: ignore[arg-type]
        call_sid=call.call_sid,
    )

    assert result.executed == 0
    assert result.next_retry_at is None
    assert retried == []
    assert len(failed) == 1
    assert failed[0][0] == job.id
    assert str(job.id) in removed_ids


async def test_max_attempts_exhaustion_marks_failed(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    call = _call()
    # attempts=2, max_attempts=3 → next attempt would be 3, which is not < 3
    job = _job(call, attempts=2, max_attempts=3)
    retried: list[tuple[uuid.UUID, datetime]] = []
    failed: list[tuple[uuid.UUID, str]] = []
    removed_ids: list[str] = []

    _patch_for_single_job(
        monkeypatch,
        job=job,
        call=call,
        raise_exc=SpotifyAPIError(503, "service unavailable"),
        retried=retried,
        failed=failed,
        removed_ids=removed_ids,
    )

    result = await deferred_tool_service.run_queued_for_call(
        _NoopSession(),  # type: ignore[arg-type]
        call_sid=call.call_sid,
    )

    assert result.executed == 0
    assert result.next_retry_at is None
    assert retried == []
    assert len(failed) == 1
    assert str(job.id) in removed_ids
