from oncue.services.deferred_tool_service import DEFER_SECONDS_AFTER_CALL_COMPLETE
from oncue.workers.tasks import process_call_deferred_tools


def enqueue_call_completion(call_sid: str) -> None:
    process_call_deferred_tools.apply_async(
        args=[call_sid],
        countdown=DEFER_SECONDS_AFTER_CALL_COMPLETE,
    )
