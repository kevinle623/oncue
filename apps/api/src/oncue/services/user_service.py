from sqlalchemy.ext.asyncio import AsyncSession

from oncue.dtos.user import UserCreateDTO, UserDTO
from oncue.repositories import user_repo


async def get_or_create_by_phone(session: AsyncSession, phone_number: str) -> UserDTO:
    existing = await user_repo.get_by_phone(session, phone_number)
    if existing is not None:
        return existing
    return await user_repo.create(session, UserCreateDTO(phone_number=phone_number))
