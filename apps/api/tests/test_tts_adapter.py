from collections.abc import Callable

import httpx

from oncue.adapters.tts import elevenlabs

MockInstaller = Callable[[Callable[[httpx.Request], httpx.Response], str], None]


async def test_synthesize_streams_chunks_and_sends_correct_request(
    mock_httpx: MockInstaller,
) -> None:
    captured: dict[str, object] = {}

    def handler(request: httpx.Request) -> httpx.Response:
        captured["method"] = request.method
        captured["path"] = request.url.path
        captured["voice_in_path"] = "test-voice-id" in request.url.path
        captured["output_format"] = request.url.params.get("output_format")
        captured["xi_api_key"] = request.headers.get("xi-api-key")
        captured["body"] = request.content
        return httpx.Response(200, content=b"\xaa\xbb\xcc\xdd")

    mock_httpx(handler, "oncue.adapters.tts.elevenlabs")

    chunks: list[bytes] = []
    async for chunk in elevenlabs.synthesize("hello there", voice_id="test-voice-id"):
        chunks.append(chunk)

    assert b"".join(chunks) == b"\xaa\xbb\xcc\xdd"
    assert captured["method"] == "POST"
    assert captured["voice_in_path"] is True
    assert captured["path"].endswith("/stream")  # type: ignore[union-attr]
    assert captured["output_format"] == elevenlabs.DEFAULT_OUTPUT_FORMAT
    assert b"hello there" in captured["body"]  # type: ignore[operator]


async def test_synthesize_raises_on_http_error(mock_httpx: MockInstaller) -> None:
    mock_httpx(
        lambda _r: httpx.Response(401, content=b"unauthorized"),
        "oncue.adapters.tts.elevenlabs",
    )

    raised = False
    try:
        async for _ in elevenlabs.synthesize("hi", voice_id="v"):
            pass
    except httpx.HTTPStatusError:
        raised = True
    assert raised
