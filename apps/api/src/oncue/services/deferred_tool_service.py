import random
import uuid
from collections.abc import Awaitable
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from inspect import isawaitable
from typing import Any, cast

import httpx
from sqlalchemy.ext.asyncio import AsyncSession

from oncue.adapters.cache.redis import redis
from oncue.adapters.music.spotify import SpotifyAPIError
from oncue.dtos.call import CallDTO
from oncue.dtos.deferred_tool_job import DeferredToolJobCreateDTO, DeferredToolJobDTO
from oncue.repositories import call_repo, deferred_tool_job_repo
from oncue.tools import REGISTRY, dispatch_deferred
from oncue.tools.base import ToolContext, ToolNotAllowedError, UnknownToolError

DEFER_SECONDS_AFTER_CALL_COMPLETE = 4
PROCESSING_STALE_AFTER_SECONDS = 120
DEFERRED_TOOL_KEY_PREFIX = "deferred:call:"
FINAL_STATUSES = frozenset({"succeeded", "failed"})
RETRY_BASE_SECONDS = 5
RETRY_MAX_SECONDS = 300
TRANSIENT_SPOTIFY_STATUSES = frozenset({401, 408, 429})


class DeferredToolExecutionError(RuntimeError):
    """Raised when a deferred tool cannot be executed."""


@dataclass(frozen=True)
class RunResult:
    executed: int
    next_retry_at: datetime | None


def _is_transient(exc: BaseException) -> bool:
    if isinstance(exc, DeferredToolExecutionError):
        return False
    if isinstance(exc, UnknownToolError | ToolNotAllowedError):
        return False
    if isinstance(exc, SpotifyAPIError):
        return exc.status_code in TRANSIENT_SPOTIFY_STATUSES or exc.status_code >= 500
    if isinstance(exc, httpx.HTTPError | TimeoutError | ConnectionError):
        return True
    return True


def _compute_backoff(attempt: int) -> timedelta:
    seconds = min(RETRY_BASE_SECONDS * (2**attempt), RETRY_MAX_SECONDS)
    jitter = random.uniform(0, seconds * 0.25)
    return timedelta(seconds=seconds + jitter)


def _call_queue_key(call_sid: str) -> str:
    return f"{DEFERRED_TOOL_KEY_PREFIX}{call_sid}"


async def _await_maybe(value: Awaitable[Any] | Any) -> Any:
    if isawaitable(value):
        return await value
    return value


def _parse_job_id(raw_id: str) -> uuid.UUID | None:
    try:
        return uuid.UUID(raw_id)
    except ValueError:
        return None


async def _list_queue_ids(call_sid: str) -> list[str]:
    key = _call_queue_key(call_sid)
    raw_ids = cast(list[Any], await _await_maybe(redis.lrange(key, 0, -1)))
    return [str(raw_id) for raw_id in raw_ids]


async def _remove_queue_id(call_sid: str, raw_id: str, removed: set[str]) -> None:
    if raw_id in removed:
        return
    await _await_maybe(redis.lrem(_call_queue_key(call_sid), 0, raw_id))
    removed.add(raw_id)


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
    try:
        await _await_maybe(redis.rpush(_call_queue_key(call.call_sid), str(job.id)))
    except Exception:
        # DB is the source of truth; execution can still discover jobs by call_id.
        pass
    return job


async def _execute_job(session: AsyncSession, job: DeferredToolJobDTO) -> None:
    call = await call_repo.get_by_id(session, job.call_id)
    if call is None or call.user_id is None:
        raise DeferredToolExecutionError(f"Call {job.call_id} not linked to a user")
    ctx = ToolContext(session=session, user_id=call.user_id, call_id=call.id)
    await dispatch_deferred(REGISTRY, ctx, job.tool_name, job.args)


async def run_queued_for_call(session: AsyncSession, *, call_sid: str) -> RunResult:
    call = await call_repo.get_by_sid(session, call_sid)
    if call is None:
        return RunResult(executed=0, next_retry_at=None)

    now = datetime.now(UTC)
    processing_stale_before = now - timedelta(seconds=PROCESSING_STALE_AFTER_SECONDS)
    due_jobs = (
        await deferred_tool_job_repo.list_due_pending_or_stale_processing_for_call(
            session,
            call_id=call.id,
            scheduled_before=now,
            processing_stale_before=processing_stale_before,
        )
    )

    queued_raw_ids = await _list_queue_ids(call_sid)
    removed_from_queue: set[str] = set()

    candidate_ids: list[uuid.UUID] = []
    seen_ids: set[uuid.UUID] = set()
    for job in due_jobs:
        if job.id not in seen_ids:
            candidate_ids.append(job.id)
            seen_ids.add(job.id)

    for raw_id in queued_raw_ids:
        parsed = _parse_job_id(raw_id)
        if parsed is None:
            await _remove_queue_id(call_sid, raw_id, removed_from_queue)
            continue
        if parsed not in seen_ids:
            candidate_ids.append(parsed)
            seen_ids.add(parsed)

    executed_count = 0
    earliest_retry_at: datetime | None = None
    for job_id in candidate_ids:
        claimed = await deferred_tool_job_repo.claim_for_execution(
            session,
            job_id=job_id,
            scheduled_before=datetime.now(UTC),
            processing_stale_before=datetime.now(UTC)
            - timedelta(seconds=PROCESSING_STALE_AFTER_SECONDS),
            claimed_at=datetime.now(UTC),
        )
        if claimed is None:
            continue
        retried = False
        try:
            await _execute_job(session, claimed)
            await deferred_tool_job_repo.mark_succeeded(
                session,
                job_id=claimed.id,
                executed_at=datetime.now(UTC),
            )
            executed_count += 1
        except Exception as exc:
            next_attempt = claimed.attempts + 1
            now = datetime.now(UTC)
            if _is_transient(exc) and next_attempt < claimed.max_attempts:
                retry_at = now + _compute_backoff(claimed.attempts)
                await deferred_tool_job_repo.mark_for_retry(
                    session,
                    job_id=claimed.id,
                    executed_at=now,
                    error=str(exc),
                    next_scheduled_for=retry_at,
                )
                if earliest_retry_at is None or retry_at < earliest_retry_at:
                    earliest_retry_at = retry_at
                retried = True
            else:
                await deferred_tool_job_repo.mark_failed(
                    session,
                    job_id=claimed.id,
                    executed_at=now,
                    error=str(exc),
                )
        finally:
            if not retried:
                await _remove_queue_id(call_sid, str(claimed.id), removed_from_queue)

    for raw_id in queued_raw_ids:
        if raw_id in removed_from_queue:
            continue
        parsed = _parse_job_id(raw_id)
        if parsed is None:
            continue
        existing_job = await deferred_tool_job_repo.get_by_id(session, parsed)
        if existing_job is None or existing_job.status in FINAL_STATUSES:
            await _remove_queue_id(call_sid, raw_id, removed_from_queue)

    return RunResult(executed=executed_count, next_retry_at=earliest_retry_at)
