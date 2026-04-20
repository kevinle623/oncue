from fastapi import FastAPI

from oncue.api import spotify as spotify_api


def create_app() -> FastAPI:
    app = FastAPI(title="OnCue API", version="0.1.0")

    @app.get("/health")
    async def health() -> dict[str, str]:
        return {"status": "ok"}

    app.include_router(spotify_api.router)
    return app


app = create_app()
