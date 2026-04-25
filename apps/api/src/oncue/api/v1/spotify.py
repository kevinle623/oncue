from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

from oncue.adapters.db.postgresql import get_session
from oncue.services import spotify_service

router = APIRouter(prefix="/spotify", tags=["spotify"])


@router.get("/authorize")
async def authorize(
    phone_number: Annotated[str, Query(min_length=4, max_length=32)],
    session: Annotated[AsyncSession, Depends(get_session)],
) -> RedirectResponse:
    url = await spotify_service.start_authorization(session, phone_number)
    await session.commit()
    return RedirectResponse(url=url, status_code=302)


@router.get("/callback")
async def callback(
    session: Annotated[AsyncSession, Depends(get_session)],
    code: str | None = None,
    state: str | None = None,
    error: str | None = None,
) -> dict[str, str]:
    if error is not None:
        raise HTTPException(status_code=400, detail=f"Spotify error: {error}")
    if code is None or state is None:
        raise HTTPException(status_code=400, detail="Missing code or state")
    try:
        account = await spotify_service.complete_authorization(session, code, state)
    except spotify_service.InvalidStateError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    await session.commit()
    return {"status": "connected", "user_id": str(account.user_id)}
