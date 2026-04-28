# OnCue

Everything, on cue.

A hands-free voice assistant for drivers. Call a phone number, speak naturally, and an LLM with tool-calling controls the apps and services you've connected. Initial integration is Spotify.

## Two ways to use OnCue

- **Today — self-host.** OnCue is open source. Clone the repo, plug in your own provider keys, and you have a working voice assistant in an afternoon. The rest of this README is the runbook.
- **Coming — hosted product.** A managed version with a web UI, account signup, and zero setup is in the works. Until it ships, self-host is the way.

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

---

# Self-Host Runbook

End state: you dial your Twilio number from your phone, say "play something chill," and Spotify starts playing on your linked device after the call ends.

## Prereqs

- **Python 3.13** and **Poetry**
- **Docker** (for local Postgres + Redis)
- **ngrok** (free account works) — Twilio needs a public URL to reach your laptop
- **Bun** (only if you want to run the marketing site locally)
- Accounts on:
  - **Twilio** with a voice-capable phone number purchased
  - **Spotify Developer** with an app created
  - **Deepgram**, **ElevenLabs**, **Anthropic**

## 1. Clone and install

```sh
git clone https://github.com/kevinle623/oncue.git
cd oncue/apps/api
poetry install
cp .env.example .env
```

## 2. Fill in provider keys

Edit `apps/api/.env`. Where each value comes from:

| Var | Where to get it |
|---|---|
| `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN` | Twilio Console → Account → API keys & tokens |
| `SPOTIFY_CLIENT_ID`, `SPOTIFY_CLIENT_SECRET` | https://developer.spotify.com/dashboard → create an app |
| `DEEPGRAM_API_KEY` | Deepgram Console → API Keys |
| `ELEVENLABS_API_KEY`, `ELEVENLABS_VOICE_ID` | ElevenLabs profile → API Key, then Voices → copy a voice ID |
| `ANTHROPIC_API_KEY` | Anthropic Console → API Keys |

Leave `DATABASE_URL`, `REDIS_URL`, `SPOTIFY_REDIRECT_URI`, and `APP_BASE_URL` at their defaults for now. We'll override `APP_BASE_URL` once ngrok is running.

## 3. Start infra and migrate

```sh
docker compose up -d        # postgres + redis
poetry run alembic upgrade head
```

## 4. Expose the API with ngrok

Twilio webhooks and the media stream both need a public URL. The TwiML adapter derives the stream `wss://` URL from `APP_BASE_URL`, so it has to match the public host.

```sh
# terminal 1: API
poetry run uvicorn oncue.main:app --reload --app-dir src

# terminal 2: tunnel
ngrok http 8000
```

Copy the `https://<subdomain>.ngrok-free.app` URL ngrok prints, then in `apps/api/.env`:

```sh
APP_BASE_URL=https://<subdomain>.ngrok-free.app
TWILIO_VALIDATE_SIGNATURE=true
```

Restart the API after editing `.env`. Signature validation is computed against the public URL; any drift returns 403 from `/v1/voice/incoming`.

## 5. Configure your Twilio number

Twilio Console → Phone Numbers → your number → Voice Configuration:

- **A call comes in** → Webhook → `https://<ngrok>/v1/voice/incoming`, HTTP POST.
- **Call status changes** → Webhook → `https://<ngrok>/v1/voice/status`, HTTP POST. (Triggers deferred Spotify mutations after the call ends.)

The media stream (`/v1/voice/stream`) does **not** need to be configured in the Twilio UI — it's emitted in the TwiML response from `/incoming`.

## 6. Configure Spotify redirect URI

Spotify Developer Dashboard → your app → Edit Settings → Redirect URIs. Add the exact value of `SPOTIFY_REDIRECT_URI` from `.env` (default: `http://localhost:8000/v1/spotify/callback`). The redirect can stay on `localhost` even when calls go through ngrok — it's only used by the consent flow in your browser.

## 7. Start the Celery worker

Spotify mutations (play, pause, skip) are deferred until after the call ends — the phone is Spotify's "active device" while the call is connected, so playing music has to wait. The worker executes those.

```sh
# terminal 3
poetry run celery -A oncue.workers.celery_app:celery_app worker --loglevel=info
```

## 8. Link your Spotify account

Open this in a browser, replacing the phone number with **your own phone in E.164 format** (the number you'll be calling *from*):

```
http://localhost:8000/v1/spotify/authorize?phone_number=+15551234567
```

This kicks off Spotify's consent flow, then writes a `users` row keyed to that phone number plus a `spotify_accounts` row with the refresh token. Future calls from that number resolve to the same user automatically.

## 9. Place a test call

Open Spotify on any device so it's the active playback target, then dial your Twilio number from the phone you registered in step 8. Say:

> "Play something chill."

Watch:

- **API log** — `/voice/incoming` 200 → WS upgrade for `/voice/stream` → STT/LLM/TTS frames.
- **Worker log** — about 4s after `call-status=completed`, the deferred queue runs and Spotify starts playing.

## Gotchas

- **ngrok free tier rotates the subdomain on restart.** Re-edit `APP_BASE_URL` and the Twilio webhook URLs each time, or pay for a reserved domain.
- **`TWILIO_VALIDATE_SIGNATURE=false`** is fine for poking endpoints with curl, but leave it on when testing real calls so you catch URL drift early.
- **The phone is Spotify's active device while connected.** Mutations intentionally queue and run after hangup; nothing is broken if music doesn't change mid-call.
- **No active Spotify device** → the worker logs a 404 from Spotify. Open the Spotify app on a phone, desktop, or web player before calling.

---

# Web App (optional)

The marketing site at https://oncue.app. You don't need it to run the voice assistant; it's only here if you want to develop the landing page or docs.

```sh
cd apps/web
bun install
bun run dev       # http://localhost:3000
bun run lint
bun run build
```

## Design

Marketing and product mockups are generated via Claude Design and stored under `apps/web/design-reference/claude-design/` as a read-only reference. Translate them into idiomatic Next.js + shadcn/ui + Tailwind — don't ship the reference directly.

---

## Status

Pre-beta, building in public. Source: https://github.com/kevinle623/oncue
