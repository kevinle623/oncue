from collections.abc import AsyncIterator

import httpx

from oncue.settings import settings

ELEVENLABS_BASE = "https://api.elevenlabs.io/v1"
DEFAULT_MODEL = "eleven_turbo_v2_5"
DEFAULT_OUTPUT_FORMAT = "ulaw_8000"


async def synthesize(
    text: str,
    *,
    voice_id: str | None = None,
    model_id: str = DEFAULT_MODEL,
    output_format: str = DEFAULT_OUTPUT_FORMAT,
) -> AsyncIterator[bytes]:
    voice = voice_id or settings.elevenlabs_voice_id
    url = f"{ELEVENLABS_BASE}/text-to-speech/{voice}/stream"
    headers = {
        "xi-api-key": settings.elevenlabs_api_key,
        "accept": "*/*",
        "content-type": "application/json",
    }
    body = {"text": text, "model_id": model_id}

    async with httpx.AsyncClient(timeout=30.0) as client:
        async with client.stream(
            "POST",
            url,
            params={"output_format": output_format},
            headers=headers,
            json=body,
        ) as response:
            response.raise_for_status()
            async for chunk in response.aiter_bytes():
                if chunk:
                    yield chunk
