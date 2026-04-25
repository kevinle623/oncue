import asyncio

from oncue.adapters.db.postgresql import SessionLocal
from oncue.services import deferred_tool_service
from oncue.workers.celery_app import celery_app


async def _run_deferred_for_call(call_sid: str) -> int:
    async with SessionLocal() as session:
        executed = await deferred_tool_service.run_queued_for_call(
            session, call_sid=call_sid
        )
        await session.commit()
        return executed


@celery_app.task(name="oncue.deferred_tools.process_call")  # type: ignore[untyped-decorator]
def process_call_deferred_tools(call_sid: str) -> int:
    return asyncio.run(_run_deferred_for_call(call_sid))
