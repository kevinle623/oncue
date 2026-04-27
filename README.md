# OnCue

Everything, on cue.

A hands-free voice assistant for drivers. Call a phone number, speak naturally, and an LLM with tool-calling controls the apps and services you've connected. Initial integration is Spotify.

## Monorepo

```
apps/
  web/   Next.js 16 landing page — marketing site, docs, legal
  api/   FastAPI voice backend — telephony, STT, LLM, TTS, integrations
```

Each app has its own `AGENTS.md` with conventions specific to that codebase.

## Tech Stack

**Web** — Next.js 16 (App Router, Turbopack), React 19, TypeScript, Tailwind v4, shadcn/ui, Bun, Vitest.

**API** — FastAPI, Python 3.13, Poetry, SQLAlchemy async + Alembic + asyncpg, Celery + Redis, Ruff.

**Integrations** — Twilio (telephony), Deepgram (STT), ElevenLabs (TTS), Anthropic (LLM + tool calling), Spotipy (Spotify).

## Quickstart

### Web

```sh
cd apps/web
bun install
bun run dev       # http://localhost:3000
bun run lint
bun run build
```

### API

```sh
cd apps/api
poetry install
docker compose up -d      # postgres + redis
poetry run alembic upgrade head
poetry run uvicorn oncue.main:app --reload --app-dir src
```

### API Runbook (Server + Worker)

```sh
# terminal 1: API
cd apps/api
poetry run uvicorn oncue.main:app --reload --app-dir src

# terminal 2: Celery worker (deferred Spotify mutations)
cd apps/api
poetry run celery -A oncue.workers.celery_app:celery_app worker --loglevel=info
```

## Running Locally Against Twilio

A real call (PSTN → STT → LLM → TTS → deferred Spotify) needs the local API reachable from Twilio's edge and a few provider-side knobs set. Once-per-machine setup:

### 1. Provider keys

Fill `apps/api/.env` (copy from `.env.example`). Where each value comes from:

- **Twilio** (`TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN`) — Twilio Console → Account → API keys & tokens.
- **Spotify** (`SPOTIFY_CLIENT_ID`, `SPOTIFY_CLIENT_SECRET`) — https://developer.spotify.com/dashboard → create an app.
- **Deepgram** (`DEEPGRAM_API_KEY`) — Deepgram Console → API Keys.
- **ElevenLabs** (`ELEVENLABS_API_KEY`, `ELEVENLABS_VOICE_ID`) — ElevenLabs profile → API Key, and Voices → copy a voice ID.
- **Anthropic** (`ANTHROPIC_API_KEY`) — Anthropic Console → API Keys.

### 2. Expose the API with ngrok

Twilio webhooks and the media stream both need a public URL. The bundled TwiML adapter derives the stream `wss://` URL from `APP_BASE_URL`, so that one var has to match the public host.

```sh
# terminal 1: start the API on :8000 (see API Runbook above)
# terminal 2: tunnel to it
ngrok http 8000
```

Copy the `https://<subdomain>.ngrok-free.app` URL ngrok prints, then in `apps/api/.env`:

```sh
APP_BASE_URL=https://<subdomain>.ngrok-free.app
TWILIO_VALIDATE_SIGNATURE=true
```

Restart the API after editing `.env`. Signature validation is computed against the public URL, so any drift here returns 403 from `/v1/voice/incoming`.

### 3. Configure your Twilio number

Twilio Console → Phone Numbers → your number → Voice Configuration:

- **A call comes in**: Webhook → `https://<ngrok>/v1/voice/incoming`, HTTP POST.
- **Call status changes**: Webhook → `https://<ngrok>/v1/voice/status`, HTTP POST. (This is what triggers deferred Spotify mutations after the call ends.)

The media stream (`/v1/voice/stream`) does **not** need to be configured in the Twilio UI — it's emitted in the TwiML response from `/incoming`.

### 4. Configure Spotify redirect URI

Spotify Developer Dashboard → your app → Edit Settings → Redirect URIs. Add the exact value of `SPOTIFY_REDIRECT_URI` from `.env` (default: `http://localhost:8000/v1/spotify/callback`). The redirect can stay on `localhost` even when calls go through ngrok — it's only used by the consent flow in your browser.

### 5. Link a Spotify account

Before the assistant can play music, the calling user has to grant Spotify access once:

```
http://localhost:8000/v1/spotify/authorize?user_id=<user-uuid>
```

Open that in a browser, complete consent, and a `spotify_accounts` row gets upserted. Tool calls during a real call will refresh tokens automatically afterward.

### 6. Place a test call

Dial your Twilio number, speak, hang up. Watch:

- **API log** — `/voice/incoming` 200 → WS upgrade for `/voice/stream` → STT/LLM/TTS frames.
- **Worker log** — about 4s after `call-status=completed`, the deferred queue runs (or reschedules with backoff if Spotify rejects).

### Gotchas

- ngrok free tier rotates the subdomain on restart. Re-edit `APP_BASE_URL` and the Twilio webhook URLs each time, or pay for a reserved domain.
- `TWILIO_VALIDATE_SIGNATURE=false` is fine for poking endpoints with curl, but leave it on when testing real calls so you catch URL drift early.
- The phone is Spotify's "active device" while the call is connected. Mutations (play/pause/skip) intentionally queue and run after hangup; nothing is broken if music doesn't change mid-call.

## Design

Marketing mockups are generated via Google Stitch and stored under `apps/web/design-reference/stitch/` as a read-only reference. Translate them into idiomatic Next.js + shadcn/ui + Tailwind — don't ship the reference directly.

## Status

Pre-beta, building in public. Source: https://github.com/kevinle623/oncue
