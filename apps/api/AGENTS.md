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

## Implementation Status

Track progress here. Update as work lands.

### Done
- Models: `user`, `spotify_account`, `call`, `call_turn`, `deferred_tool_job`
- Spotify OAuth: `/spotify/authorize` and `/spotify/callback` (Redis-backed state)
- Spotify adapter: auth URL, code exchange, refresh, playback HTTP wrappers (currently-playing, search, play, pause, skip, queue) + `SpotifyAPIError`
- Spotify service: `get_fresh_access_token` (skew-aware refresh + persist), `now_playing`, `search_tracks`
- DTOs: `TrackDTO`, `NowPlayingDTO`
- Tools registry: `tools/base.py` (`Tool`, `ToolContext`, `dispatch_immediate` enforces immediate-only during calls)
- Immediate Spotify tools: `spotify_now_playing`, `spotify_search_tracks`
- LLM adapter (`adapters/llm/anthropic.py`): SDK-agnostic types (`LLMMessage`, `LLMTool`, `LLMResponse`, content blocks) wrapping `AsyncAnthropic.messages.create`. Default model `claude-haiku-4-5-20251001`.
- Conversation service (`services/conversation_service.py`): `run_turn(ctx, user_text, history)` — loops LLM call → `dispatch_immediate` → tool_result → repeat until text response. Exposes only immediate tools. Iteration cap.
- Tests: adapter (httpx MockTransport), service token-refresh, tool dispatch, conversation loop (no-tool, tool_use, tool error, iteration cap). `pytest-asyncio` auto mode configured.

### Remaining
- **Telephony adapter** (`adapters/telephony/twilio.py`): empty. Needs signature validation, TwiML helpers, Media Streams setup.
- **STT adapter** (`adapters/stt/deepgram.py`): empty.
- **TTS adapter** (`adapters/tts/elevenlabs.py`): empty.
- **Deferred tools**: register Spotify mutation tools (`play`, `pause`, `skip`, `queue`) as `bucket="deferred"`. Adapter HTTP wrappers already exist.
- **Workers** (`workers/`): empty. Needs Celery app, Redis queue keyed by `CallSid`, and a task that drains the queue ~4s after Twilio `call-status=completed`.
- **Voice routes**: no `/voice` Twilio webhook endpoints yet. Need entry point + per-turn handler that wires STT → LLM (immediate tools) → TTS, and persists `call` + `call_turn` rows.
- **Repos for call/call_turn/deferred_tool_job**: models exist, repositories not written.
- **Settings**: no `webhook_base_url` / `app_base_url` for Twilio callback registration yet.

## Before Declaring Done

```sh
poetry run ruff format .
poetry run ruff check .
poetry run mypy src
poetry run pytest
```
