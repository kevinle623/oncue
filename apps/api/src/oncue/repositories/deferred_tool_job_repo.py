import uuid
from datetime import datetime

from sqlalchemy import Select, select
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
    await session.flush()
    await session.refresh(job)
    return DeferredToolJobDTO.model_validate(job)
