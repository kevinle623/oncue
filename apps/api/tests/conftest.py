from collections.abc import Callable, Iterator

import httpx
import pytest


@pytest.fixture
def mock_httpx(
    monkeypatch: pytest.MonkeyPatch,
) -> Iterator[Callable[[Callable[[httpx.Request], httpx.Response], str], None]]:
    def install(
        handler: Callable[[httpx.Request], httpx.Response], module_path: str
    ) -> None:
        transport = httpx.MockTransport(handler)
        original = httpx.AsyncClient

        class _MockedClient(original):  # type: ignore[misc, valid-type]
            def __init__(self, *args: object, **kwargs: object) -> None:
                kwargs.pop("transport", None)
                super().__init__(*args, transport=transport, **kwargs)  # type: ignore[arg-type]

        monkeypatch.setattr(f"{module_path}.httpx.AsyncClient", _MockedClient)

    yield install
