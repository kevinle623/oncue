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
- Models: `user`, `spotify_account`, `call`, `call_turn`, `deferred_tool_job`.
- DTOs/repos:
  - calls: `dtos/call.py`, `repositories/call_repo.py` (`get_by_id`, `get_by_sid`, `create`, `update_status`)
  - call turns: `dtos/call_turn.py`, `repositories/call_turn_repo.py`
  - deferred jobs: `dtos/deferred_tool_job.py`, `repositories/deferred_tool_job_repo.py`
- Spotify auth + token lifecycle:
  - routes: `/spotify/authorize`, `/spotify/callback` (Redis-backed state)
  - adapter: auth URL, code exchange, refresh, playback wrappers + `SpotifyAPIError`
  - service: `get_fresh_access_token`, `now_playing`, `search_tracks`, `play`, `pause`, `skip_next`, `queue_track`
- Tools:
  - registry + dispatch: `dispatch_immediate`, `dispatch_deferred`
  - immediate: `spotify_now_playing`, `spotify_search_tracks`
  - deferred: `spotify_play`, `spotify_pause`, `spotify_skip`, `spotify_queue`
- Conversation service (`services/conversation_service.py`):
  - `run_turn(ctx, user_text, history)` supports both immediate and deferred tool calls
  - deferred tool calls are queued as `deferred_tool_jobs` and returned to the LLM as queued tool results
  - iteration cap enforced
- Telephony + voice routes:
  - Twilio adapter validates signatures and builds TwiML with `<Connect><Stream>`
  - `POST /voice/incoming` registers call + returns TwiML
  - `POST /voice/status` updates call status and enqueues deferred tool execution on `completed`
  - `WS /voice/stream` bridges Twilio media frames ↔ STT ↔ conversation ↔ TTS and persists `CallTurn` rows
- Deferred execution pipeline:
  - Redis queue keyed by `CallSid` stores deferred job IDs as a scheduling hint
  - DB is source of truth for due jobs; worker can execute due jobs even if Redis enqueue fails
  - Celery app/task in `workers/` executes deferred jobs ~4s after completion webhook
  - atomic claim for execution (`pending` or stale `processing`), then mark `succeeded` / `failed`
  - stale `processing` jobs are reclaimable after timeout to recover from interrupted workers
- STT/TTS adapters:
  - Deepgram streaming via `websockets` (SDK not used)
  - ElevenLabs streaming via `httpx` (SDK not used)
- Settings:
  - `app_base_url`, `twilio_validate_signature`, `elevenlabs_voice_id` documented in settings + `.env.example`
- Tests:
  - adapter/service/tool/conversation coverage
  - voice routes + voice stream route coverage
  - deferred tool service coverage

### Remaining
- **Unused SDK deps**: `deepgram-sdk` and `elevenlabs` are listed in `pyproject.toml` but not used (we went direct via `websockets` + `httpx`). Candidate for removal in a cleanup pass.
- **Worker ops**: add a short operational runbook (commands, logs, and basic smoke checks) for running API + worker locally.
- **Deferred retry policy**: current behavior reclaims stale `processing` jobs, but functional retries/backoff by error type are not implemented.

## Local Runbook

```sh
# terminal 1: API
cd apps/api
poetry run uvicorn oncue.main:app --reload --app-dir src

# terminal 2: Celery worker
cd apps/api
poetry run celery -A oncue.workers.celery_app:celery_app worker --loglevel=info
```

## Before Declaring Done

```sh
poetry run ruff format .
poetry run ruff check .
poetry run mypy src
poetry run pytest
```
