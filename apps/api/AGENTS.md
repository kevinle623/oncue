# API Agent Rules

## Architecture

### Service + Repository Pattern

- SQLAlchemy models live in `models/` (one class per file, plus `models/base.py` with the shared `DeclarativeBase`).
- Repositories own all database access and are the only layer allowed to import from `models/`. Never import models from `services/`, `api/`, or anywhere else.
- Services accept and return Pydantic DTOs only. DTOs live in `dtos/`.
- Routes call services, services call repositories. No skipping layers.

### Adapters Pattern

Adapters decouple the application from specific third-party providers. Services depend on adapter interfaces, never on provider SDKs directly. Each adapter category has its own subdirectory with provider-specific implementations:

```
adapters/
  db/postgresql.py         — database
  tts/elevenlabs.py        — text-to-speech
  stt/deepgram.py          — speech-to-text
  llm/anthropic.py         — language model
  telephony/twilio.py      — telephony
  music/spotify.py         — music streaming
```

When adding a new provider, add a new file under the appropriate category (e.g. `tts/cartesia.py`). When adding a new category, create a new subdirectory with an `__init__.py`.

### Tool Architecture

Tools split into two buckets:

- **Immediate**: read-only, executed during the active call. Safe because they don't affect Spotify playback state.
- **Deferred**: mutations (play, pause, skip, queue). Queued in Redis keyed by `CallSid`. Executed by Celery ~4s after Twilio's `call-status completed` webhook fires. Reason: the phone occupies Spotify's active device during the call, so mutations must wait until the call ends.

Never execute Spotify mutations during an active call.

### Style

- Functional programming preferred. Classes only when required by the framework (SQLAlchemy declarative models, Pydantic `BaseModel`, Celery task classes).
- No unnecessary OOP.

## Type Safety

- Type hints everywhere. This codebase targets `mypy --strict`.
- No untyped functions, no `Any` unless genuinely unavoidable.

## Async by Default

- FastAPI routes: `async def`.
- SQLAlchemy: async engine + `AsyncSession`.
- HTTP calls: `httpx.AsyncClient`.
- Never mix sync and async DB sessions.

## Dependencies

Before adding a dependency, check if the stdlib or an existing dep handles it. Prefer fewer dependencies.

Current stack: FastAPI, Pydantic, pydantic-settings, SQLAlchemy, Alembic, asyncpg, Celery, Redis, httpx, Twilio, Spotipy, Deepgram SDK, ElevenLabs, Anthropic.

## Config and Secrets

- Never commit `.env`. All config goes through `oncue.settings.settings` (pydantic-settings `BaseSettings`).
- Required vars have no default (pydantic fails at startup if missing). Optional vars with local defaults have a default value.
- New env vars must be added to both `Settings` and `.env.example`.

## Webhooks

All Twilio webhooks must validate the `X-Twilio-Signature` header before processing.

## Before Declaring Done

```sh
poetry run ruff format .
poetry run ruff check .
poetry run mypy src
poetry run pytest
```
