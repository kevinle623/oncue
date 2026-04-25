from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from oncue.dtos.call import CallCreateDTO, CallDTO, CallStatusUpdateDTO
from oncue.models.call import Call


async def get_by_sid(session: AsyncSession, call_sid: str) -> CallDTO | None:
    result = await session.execute(select(Call).where(Call.call_sid == call_sid))
    call = result.scalar_one_or_none()
    return CallDTO.model_validate(call) if call else None


async def create(session: AsyncSession, data: CallCreateDTO) -> CallDTO:
    call = Call(
        call_sid=data.call_sid,
        user_id=data.user_id,
        status=data.status,
        from_number=data.from_number,
        to_number=data.to_number,
    )
    session.add(call)
    await session.flush()
    await session.refresh(call)
    return CallDTO.model_validate(call)


async def update_status(
    session: AsyncSession, data: CallStatusUpdateDTO
) -> CallDTO | None:
    result = await session.execute(select(Call).where(Call.call_sid == data.call_sid))
    call = result.scalar_one_or_none()
    if call is None:
        return None
    call.status = data.status
    if data.ended_at is not None:
        call.ended_at = data.ended_at
    await session.flush()
    await session.refresh(call)
    return CallDTO.model_validate(call)
