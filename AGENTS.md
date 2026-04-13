# OnCue

Voice assistant: call a Twilio number hands-free, speak naturally, AI tool calling controls apps/services via APIs. Initial integration is Spotify.

## Monorepo Structure

```
apps/web/   — Next.js 16, TypeScript, Tailwind v4, shadcn/ui. Bun. Vitest.
apps/api/   — FastAPI, Python 3.13, Poetry. Ruff (no black/isort). SQLAlchemy async + Alembic + asyncpg. Celery + Redis.
```

## Integrations (API)

Twilio (telephony), Deepgram (STT), ElevenLabs (TTS), Anthropic (LLM + tool calling), Spotipy (Spotify).

## Design Pipeline

Google Stitch generates HTML mockups under `apps/web/design-reference/stitch/<folder>/`. Translate to idiomatic Next.js + shadcn/ui + Tailwind. Design reference is read-only, never shipped.

## Preferences

- Concise, direct communication, no em-dashes
- Step-by-step reasoning when building things
- Don't second-guess decisions already made. Push back with reasoning if you disagree, but don't hedge
- Run lint and build before declaring work done
- See `apps/web/AGENTS.md` and `apps/api/AGENTS.md` for app-specific rules
