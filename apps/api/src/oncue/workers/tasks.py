import asyncio
from datetime import UTC, datetime

from oncue.adapters.db.postgresql import SessionLocal
from oncue.services import deferred_tool_service
from oncue.services.deferred_tool_service import RunResult
from oncue.workers.celery_app import celery_app


async def _run_deferred_for_call(call_sid: str) -> RunResult:
    async with SessionLocal() as session:
        result = await deferred_tool_service.run_queued_for_call(
            session, call_sid=call_sid
        )
        await session.commit()
        return result


@celery_app.task(name="oncue.deferred_tools.process_call", bind=True)  # type: ignore[untyped-decorator]
def process_call_deferred_tools(self: object, call_sid: str) -> int:
    result = asyncio.run(_run_deferred_for_call(call_sid))
    if result.next_retry_at is not None:
        countdown = max(1.0, (result.next_retry_at - datetime.now(UTC)).total_seconds())
        process_call_deferred_tools.apply_async(args=[call_sid], countdown=countdown)
    return result.executed
