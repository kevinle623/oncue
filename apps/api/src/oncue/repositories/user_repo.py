import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from oncue.dtos.user import UserCreateDTO, UserDTO
from oncue.models.user import User


async def get_by_id(session: AsyncSession, user_id: uuid.UUID) -> UserDTO | None:
    result = await session.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    return UserDTO.model_validate(user) if user else None


async def get_by_phone(session: AsyncSession, phone_number: str) -> UserDTO | None:
    result = await session.execute(
        select(User).where(User.phone_number == phone_number)
    )
    user = result.scalar_one_or_none()
    return UserDTO.model_validate(user) if user else None


async def create(session: AsyncSession, data: UserCreateDTO) -> UserDTO:
    user = User(phone_number=data.phone_number, display_name=data.display_name)
    session.add(user)
    await session.flush()
    await session.refresh(user)
    return UserDTO.model_validate(user)
