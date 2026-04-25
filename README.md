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

## Design

Marketing mockups are generated via Google Stitch and stored under `apps/web/design-reference/stitch/` as a read-only reference. Translate them into idiomatic Next.js + shadcn/ui + Tailwind — don't ship the reference directly.

## Status

Pre-beta, building in public. Source: https://github.com/kevinle623/oncue
