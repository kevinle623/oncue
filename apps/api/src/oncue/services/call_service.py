from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from oncue.dtos.call import CallCreateDTO, CallDTO, CallStatusUpdateDTO
from oncue.repositories import call_repo
from oncue.services import user_service

TERMINAL_STATUSES = frozenset({"completed", "failed", "busy", "no-answer", "canceled"})


async def register_incoming_call(
    session: AsyncSession,
    *,
    call_sid: str,
    from_number: str,
    to_number: str,
    status: str,
) -> CallDTO:
    existing = await call_repo.get_by_sid(session, call_sid)
    if existing is not None:
        return existing
    user = await user_service.get_or_create_by_phone(session, from_number)
    return await call_repo.create(
        session,
        CallCreateDTO(
            call_sid=call_sid,
            user_id=user.id,
            status=status,
            from_number=from_number,
            to_number=to_number,
        ),
    )


async def update_status(
    session: AsyncSession,
    *,
    call_sid: str,
    status: str,
    ended_at: datetime | None = None,
) -> CallDTO | None:
    return await call_repo.update_status(
        session,
        CallStatusUpdateDTO(
            call_sid=call_sid,
            status=status,
            ended_at=ended_at,
        ),
    )
