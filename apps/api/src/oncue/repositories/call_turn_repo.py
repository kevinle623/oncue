import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from oncue.dtos.call_turn import CallTurnCreateDTO, CallTurnDTO
from oncue.models.call_turn import CallTurn


async def create(session: AsyncSession, data: CallTurnCreateDTO) -> CallTurnDTO:
    turn = CallTurn(
        call_id=data.call_id,
        role=data.role,
        transcript=data.transcript,
        tool_calls=data.tool_calls,
    )
    session.add(turn)
    await session.flush()
    await session.refresh(turn)
    return CallTurnDTO.model_validate(turn)


async def list_by_call(session: AsyncSession, call_id: uuid.UUID) -> list[CallTurnDTO]:
    result = await session.execute(
        select(CallTurn)
        .where(CallTurn.call_id == call_id)
        .order_by(CallTurn.created_at)
    )
    return [CallTurnDTO.model_validate(row) for row in result.scalars().all()]
