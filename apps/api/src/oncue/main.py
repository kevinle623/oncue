from fastapi import APIRouter, FastAPI

from oncue.api.v1 import spotify as spotify_api
from oncue.api.v1 import voice as voice_api


def create_app() -> FastAPI:
    app = FastAPI(title="OnCue API", version="0.1.0")

    @app.get("/health")
    async def health() -> dict[str, str]:
        return {"status": "ok"}

    v1 = APIRouter(prefix="/v1")
    v1.include_router(spotify_api.router)
    v1.include_router(voice_api.router)
    app.include_router(v1)
    return app


app = create_app()
