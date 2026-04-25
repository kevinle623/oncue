import uuid
from collections.abc import Awaitable
from datetime import UTC, datetime, timedelta
from inspect import isawaitable
from typing import Any, cast

from sqlalchemy.ext.asyncio import AsyncSession

from oncue.adapters.cache.redis import redis
from oncue.dtos.call import CallDTO
from oncue.dtos.deferred_tool_job import DeferredToolJobCreateDTO, DeferredToolJobDTO
from oncue.repositories import call_repo, deferred_tool_job_repo
from oncue.tools import REGISTRY, dispatch_deferred
from oncue.tools.base import ToolContext

DEFER_SECONDS_AFTER_CALL_COMPLETE = 4
DEFERRED_TOOL_KEY_PREFIX = "deferred:call:"


class DeferredToolExecutionError(RuntimeError):
    """Raised when a deferred tool cannot be executed."""


def _call_queue_key(call_sid: str) -> str:
    return f"{DEFERRED_TOOL_KEY_PREFIX}{call_sid}"


async def _await_maybe(value: Awaitable[Any] | Any) -> Any:
    if isawaitable(value):
        return await value
    return value


async def enqueue_for_call(
    session: AsyncSession,
    *,
    call: CallDTO,
    tool_name: str,
    arguments: dict[str, Any],
) -> DeferredToolJobDTO:
    scheduled_for = datetime.now(UTC) + timedelta(
        seconds=DEFER_SECONDS_AFTER_CALL_COMPLETE
    )
    job = await deferred_tool_job_repo.create(
        session,
        DeferredToolJobCreateDTO(
            call_id=call.id,
            tool_name=tool_name,
            args=arguments,
            status="pending",
            scheduled_for=scheduled_for,
        ),
    )
    await _await_maybe(redis.rpush(_call_queue_key(call.call_sid), str(job.id)))
    return job


async def _drain_call_queue(call_sid: str) -> list[uuid.UUID]:
    key = _call_queue_key(call_sid)
    raw_ids = cast(list[str], await _await_maybe(redis.lrange(key, 0, -1)))
    await _await_maybe(redis.delete(key))
    job_ids: list[uuid.UUID] = []
    for raw_id in raw_ids:
        try:
            job_ids.append(uuid.UUID(raw_id))
        except ValueError:
            continue
    return job_ids


async def _execute_job(session: AsyncSession, job: DeferredToolJobDTO) -> None:
    call = await call_repo.get_by_id(session, job.call_id)
    if call is None or call.user_id is None:
        raise DeferredToolExecutionError(f"Call {job.call_id} not linked to a user")
    ctx = ToolContext(session=session, user_id=call.user_id, call_id=call.id)
    await dispatch_deferred(REGISTRY, ctx, job.tool_name, job.args)


async def run_queued_for_call(session: AsyncSession, *, call_sid: str) -> int:
    now = datetime.now(UTC)
    job_ids = await _drain_call_queue(call_sid)
    jobs = await deferred_tool_job_repo.list_pending_due_by_ids(
        session,
        job_ids=job_ids,
        scheduled_before=now,
    )
    executed_count = 0
    for job in jobs:
        try:
            await _execute_job(session, job)
            await deferred_tool_job_repo.mark_succeeded(
                session,
                job_id=job.id,
                executed_at=datetime.now(UTC),
            )
            executed_count += 1
        except Exception as exc:
            await deferred_tool_job_repo.mark_failed(
                session,
                job_id=job.id,
                executed_at=datetime.now(UTC),
                error=str(exc),
            )
    return executed_count
