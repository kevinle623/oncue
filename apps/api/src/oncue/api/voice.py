from datetime import UTC, datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request, Response
from sqlalchemy.ext.asyncio import AsyncSession

from oncue.adapters.db.postgresql import get_session
from oncue.adapters.telephony import twilio as twilio_adapter
from oncue.services import call_service
from oncue.settings import settings

router = APIRouter(prefix="/voice", tags=["voice"])


async def _read_form(request: Request) -> dict[str, str]:
    form = await request.form()
    return {k: str(v) for k, v in form.items()}


def _verify_twilio(request: Request, params: dict[str, str]) -> None:
    if not settings.twilio_validate_signature:
        return
    signature = request.headers.get("X-Twilio-Signature", "")
    url = settings.app_base_url.rstrip("/") + request.url.path
    if not twilio_adapter.validate_signature(url, params, signature):
        raise HTTPException(status_code=403, detail="Invalid Twilio signature")


@router.post("/incoming")
async def incoming(
    request: Request,
    session: Annotated[AsyncSession, Depends(get_session)],
) -> Response:
    params = await _read_form(request)
    _verify_twilio(request, params)

    call_sid = params.get("CallSid")
    from_number = params.get("From")
    to_number = params.get("To")
    status = params.get("CallStatus", "ringing")
    if not call_sid or not from_number or not to_number:
        raise HTTPException(status_code=400, detail="Missing Twilio call fields")

    await call_service.register_incoming_call(
        session,
        call_sid=call_sid,
        from_number=from_number,
        to_number=to_number,
        status=status,
    )
    await session.commit()

    twiml = twilio_adapter.build_voice_twiml(
        call_sid, greeting="Hi, this is OnCue. Go ahead."
    )
    return Response(content=twiml, media_type="application/xml")


@router.post("/status")
async def status(
    request: Request,
    session: Annotated[AsyncSession, Depends(get_session)],
) -> Response:
    params = await _read_form(request)
    _verify_twilio(request, params)

    call_sid = params.get("CallSid")
    call_status = params.get("CallStatus")
    if not call_sid or not call_status:
        raise HTTPException(status_code=400, detail="Missing Twilio status fields")

    ended_at = (
        datetime.now(UTC) if call_status in call_service.TERMINAL_STATUSES else None
    )
    await call_service.update_status(
        session, call_sid=call_sid, status=call_status, ended_at=ended_at
    )
    await session.commit()
    return Response(status_code=204)
