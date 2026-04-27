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

## Direction

The open-source self-host story is feature-complete. The next phase is a hosted product (web UI so users don't have to run their own infra).

Architectural decision: the hosted product lives in `apps/web/app/(app)/` as a route group alongside the existing `(marketing)/` group — same Next.js app, same design system, one deploy. **Not** a new monorepo package. `apps/api` stays the source of truth for all business logic; the dashboard is a thin client that calls FastAPI with a JWT (Clerk or similar).

App-level "next up" lists live in `apps/web/AGENTS.md` and `apps/api/AGENTS.md` under "Implementation Status." Update those as work lands; do not maintain a long-lived roadmap here — it goes stale.

## Preferences

- Concise, direct communication, no em-dashes
- Step-by-step reasoning when building things
- Don't second-guess decisions already made. Push back with reasoning if you disagree, but don't hedge
- Run lint and build before declaring work done
- Keep agent context docs up to date after each change (especially `apps/api/AGENTS.md` / `apps/web/AGENTS.md` implementation status and local runbook notes)
- See `apps/web/AGENTS.md` and `apps/api/AGENTS.md` for app-specific rules
