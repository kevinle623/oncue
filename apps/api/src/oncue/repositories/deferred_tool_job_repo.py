import uuid
from datetime import datetime

from sqlalchemy import Select, and_, or_, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from oncue.dtos.deferred_tool_job import DeferredToolJobCreateDTO, DeferredToolJobDTO
from oncue.models.deferred_tool_job import DeferredToolJob


async def create(
    session: AsyncSession, data: DeferredToolJobCreateDTO
) -> DeferredToolJobDTO:
    job = DeferredToolJob(
        call_id=data.call_id,
        tool_name=data.tool_name,
        args=data.args,
        status=data.status,
        scheduled_for=data.scheduled_for,
        max_attempts=data.max_attempts,
    )
    session.add(job)
    await session.flush()
    await session.refresh(job)
    return DeferredToolJobDTO.model_validate(job)


async def get_by_id(
    session: AsyncSession, job_id: uuid.UUID
) -> DeferredToolJobDTO | None:
    result = await session.execute(
        select(DeferredToolJob).where(DeferredToolJob.id == job_id)
    )
    job = result.scalar_one_or_none()
    return DeferredToolJobDTO.model_validate(job) if job else None


async def list_pending_due_by_ids(
    session: AsyncSession,
    *,
    job_ids: list[uuid.UUID],
    scheduled_before: datetime,
) -> list[DeferredToolJobDTO]:
    if not job_ids:
        return []
    query: Select[tuple[DeferredToolJob]] = (
        select(DeferredToolJob)
        .where(DeferredToolJob.id.in_(job_ids))
        .where(DeferredToolJob.status == "pending")
        .where(DeferredToolJob.scheduled_for <= scheduled_before)
        .order_by(DeferredToolJob.scheduled_for, DeferredToolJob.created_at)
    )
    result = await session.execute(query)
    return [DeferredToolJobDTO.model_validate(row) for row in result.scalars().all()]


async def list_due_pending_or_stale_processing_for_call(
    session: AsyncSession,
    *,
    call_id: uuid.UUID,
    scheduled_before: datetime,
    processing_stale_before: datetime,
) -> list[DeferredToolJobDTO]:
    query: Select[tuple[DeferredToolJob]] = (
        select(DeferredToolJob)
        .where(DeferredToolJob.call_id == call_id)
        .where(
            or_(
                and_(
                    DeferredToolJob.status == "pending",
                    DeferredToolJob.scheduled_for <= scheduled_before,
                ),
                and_(
                    DeferredToolJob.status == "processing",
                    DeferredToolJob.executed_at.is_not(None),
                    DeferredToolJob.executed_at <= processing_stale_before,
                ),
            )
        )
        .order_by(DeferredToolJob.scheduled_for, DeferredToolJob.created_at)
    )
    result = await session.execute(query)
    return [DeferredToolJobDTO.model_validate(row) for row in result.scalars().all()]


async def claim_for_execution(
    session: AsyncSession,
    *,
    job_id: uuid.UUID,
    scheduled_before: datetime,
    processing_stale_before: datetime,
    claimed_at: datetime,
) -> DeferredToolJobDTO | None:
    stmt = (
        update(DeferredToolJob)
        .where(DeferredToolJob.id == job_id)
        .where(
            or_(
                and_(
                    DeferredToolJob.status == "pending",
                    DeferredToolJob.scheduled_for <= scheduled_before,
                ),
                and_(
                    DeferredToolJob.status == "processing",
                    DeferredToolJob.executed_at.is_not(None),
                    DeferredToolJob.executed_at <= processing_stale_before,
                ),
            )
        )
        .values(
            status="processing",
            executed_at=claimed_at,
            error=None,
        )
        .returning(DeferredToolJob)
    )
    result = await session.execute(stmt)
    job = result.scalar_one_or_none()
    if job is None:
        return None
    await session.flush()
    return DeferredToolJobDTO.model_validate(job)


async def mark_succeeded(
    session: AsyncSession,
    *,
    job_id: uuid.UUID,
    executed_at: datetime,
) -> DeferredToolJobDTO | None:
    result = await session.execute(
        select(DeferredToolJob).where(DeferredToolJob.id == job_id)
    )
    job = result.scalar_one_or_none()
    if job is None:
        return None
    job.status = "succeeded"
    job.executed_at = executed_at
    job.error = None
    await session.flush()
    await session.refresh(job)
    return DeferredToolJobDTO.model_validate(job)


async def mark_failed(
    session: AsyncSession,
    *,
    job_id: uuid.UUID,
    executed_at: datetime,
    error: str,
) -> DeferredToolJobDTO | None:
    result = await session.execute(
        select(DeferredToolJob).where(DeferredToolJob.id == job_id)
    )
    job = result.scalar_one_or_none()
    if job is None:
        return None
    job.status = "failed"
    job.executed_at = executed_at
    job.error = error
    job.attempts = job.attempts + 1
    await session.flush()
    await session.refresh(job)
    return DeferredToolJobDTO.model_validate(job)


async def mark_for_retry(
    session: AsyncSession,
    *,
    job_id: uuid.UUID,
    executed_at: datetime,
    error: str,
    next_scheduled_for: datetime,
) -> DeferredToolJobDTO | None:
    result = await session.execute(
        select(DeferredToolJob).where(DeferredToolJob.id == job_id)
    )
    job = result.scalar_one_or_none()
    if job is None:
        return None
    job.status = "pending"
    job.executed_at = executed_at
    job.error = error
    job.attempts = job.attempts + 1
    job.scheduled_for = next_scheduled_for
    await session.flush()
    await session.refresh(job)
    return DeferredToolJobDTO.model_validate(job)
