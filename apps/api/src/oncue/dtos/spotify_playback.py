from typing import Any

from pydantic import BaseModel


class TrackDTO(BaseModel):
    id: str
    name: str
    uri: str
    artists: list[str]
    album: str
    duration_ms: int

    @classmethod
    def from_spotify(cls, payload: dict[str, Any]) -> "TrackDTO":
        return cls(
            id=payload["id"],
            name=payload["name"],
            uri=payload["uri"],
            artists=[a["name"] for a in payload.get("artists", [])],
            album=payload.get("album", {}).get("name", ""),
            duration_ms=int(payload.get("duration_ms", 0)),
        )


class NowPlayingDTO(BaseModel):
    track: TrackDTO
    is_playing: bool
    progress_ms: int
    device_name: str | None = None
