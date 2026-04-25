import asyncio
import base64
from collections.abc import AsyncIterator
from datetime import UTC, datetime
from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Request,
    Response,
    WebSocket,
    WebSocketDisconnect,
)
from sqlalchemy.ext.asyncio import AsyncSession

from oncue.adapters.db.postgresql import get_session
from oncue.adapters.telephony import twilio as twilio_adapter
from oncue.repositories import call_repo
from oncue.services import call_service, voice_session_service
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


@router.websocket("/stream")
async def stream(
    ws: WebSocket,
    db_session: Annotated[AsyncSession, Depends(get_session)],
) -> None:
    await ws.accept()

    stream_sid: str | None = None
    call_sid: str | None = None
    while stream_sid is None:
        event = await ws.receive_json()
        etype = event.get("event")
        if etype == "start":
            stream_sid = event["start"]["streamSid"]
            call_sid = event["start"]["callSid"]
        elif etype == "stop":
            await ws.close()
            return
        # ignore "connected" and any other preamble events

    assert call_sid is not None
    call = await call_repo.get_by_sid(db_session, call_sid)
    if call is None:
        await ws.close(code=1008)
        return

    audio_queue: asyncio.Queue[bytes | None] = asyncio.Queue()

    async def inbound() -> AsyncIterator[bytes]:
        while True:
            chunk = await audio_queue.get()
            if chunk is None:
                return
            yield chunk

    async def send_audio(chunk: bytes) -> None:
        await ws.send_json(
            {
                "event": "media",
                "streamSid": stream_sid,
                "media": {"payload": base64.b64encode(chunk).decode("ascii")},
            }
        )

    session_task = asyncio.create_task(
        voice_session_service.run_session(
            db_session,
            call=call,
            inbound_audio=inbound(),
            send_audio=send_audio,
        )
    )

    try:
        while True:
            event = await ws.receive_json()
            etype = event.get("event")
            if etype == "media":
                payload = event["media"]["payload"]
                await audio_queue.put(base64.b64decode(payload))
            elif etype == "stop":
                break
    except WebSocketDisconnect:
        pass
    finally:
        await audio_queue.put(None)
        await asyncio.gather(session_task, return_exceptions=True)
        try:
            await ws.close()
        except RuntimeError:
            pass
