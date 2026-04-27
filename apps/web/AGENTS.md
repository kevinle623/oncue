# Web App Agent Rules

## Next.js Source of Truth

Before making non-trivial decisions about routing, data fetching, caching, server vs client components, metadata, or other framework concerns, consult the bundled Next.js docs:

```
node_modules/next/dist/docs/01-app/          — App Router guides, API reference, glossary
node_modules/next/dist/docs/01-app/01-getting-started/
node_modules/next/dist/docs/01-app/02-guides/
node_modules/next/dist/docs/01-app/03-api-reference/
```

Grep these paths when uncertain rather than relying on training data. Next.js evolves quickly; bundled docs are authoritative.

Note: Next.js 16 removed `next lint`. Use `bun run lint` which invokes ESLint directly.

## shadcn/ui

- Always read `components/ui/` to see which primitives are already installed before using one.
- Run `bunx shadcn@latest add <name>` to add missing primitives. Never hand-roll what shadcn provides.
- Currently installed: `button`, `card`.

## Styling

- Tailwind v4 with CSS variables for theming. **Light, paper-cream theme** (no dark mode). Source design lives in `design-reference/claude-design/design_handoff_oncue_landing/`.
- Tokens live in `app/globals.css` under `@theme inline` and `:root`. Design tokens: `background`, `foreground`, `surface` / `surface-low` / `surface-lowest` / `surface-high`, `muted`, `muted-foreground`, `accent`, `accent-foreground`, `accent-soft`, `border`, `border-strong`.
- Never hardcode hex values in components. Use Tailwind tokens (`bg-surface-low`, `text-accent`, `border-border`, etc). The two exceptions are inline SVG decoration (hero rings, step icons) and the Spotify brand green `#1DB954`.
- Fonts: Instrument Serif (display, italic-heavy) + DM Sans (body, weights 300/400/500/600), via `next/font/google`, wired as `--font-display` / `--font-body` (and `--font-sans = --font-body`).
- `scroll-behavior: smooth` is on globally; `section[id]` has `scroll-margin-top` to clear the fixed nav.

## Component Organization

```
components/
  ui/         shadcn primitives only (button, card, …)
  layout/     nav, footer, doc-page
  sections/   one file per landing-page section (hero, hero-visual, how-it-works, integrations, why-hands-free, privacy, faq, get-started-cta)
  common/     reusable building blocks (container, section, divider, wordmark, section-label, display-heading, section-body, primary-button, reveal)
  icons/      inline SVG icon components
    brand/    third-party brand glyphs (e.g. spotify)
```

Reach for something in `common/` before adding a new one-off. If three callsites end up with the same pattern, extract it.

### Design system primitives

- `Container` — width-constrained wrapper. `width="default"` (1080px), `narrow` (680px), `prose` (max-w-3xl).
- `Section` — vertical rhythm + tone variants. `tone="default" | "surface-low" | "accent-soft"`, `padding="default" | "compact"`.
- `DisplayHeading` — Instrument Serif headline. `size="sm" | "md" | "lg" | "xl"`. Wraps any `<em>` in italic + accent color automatically.
- `SectionLabel` — 11px uppercase tracking-[0.18em] eyebrow.
- `SectionBody` — muted intro paragraph.
- `Wordmark` — split-opacity `on` + `Cue` in italic Instrument Serif. `size="sm" | "md" | "lg"`.
- `PrimaryButton` — accent-on-cream CTA. Pass `href` for a link (external URLs auto open in a new tab), otherwise renders a `<button>`. `size="sm" | "md"`. When `href` ends in a hash and the target element exists on the current page, the click is intercepted and smooth-scrolled so re-clicking the same hash still scrolls.
- `Reveal` — IntersectionObserver-driven fade/translate-up. Use `delay` (ms) for staggered children.
- `Divider` — 1px max-w-1080 horizontal rule between hero and how-it-works.

## Architecture

- App Router, server components by default. Add `"use client"` only when needed.
- Lucide icons for UI iconography. Brand logos are hand-authored monochrome SVGs under `icons/brand/` using `currentColor`.
- Images go through `next/image`. Source files live in `public/images/`. For a soft-edge blend with the background use the `FadedImage` illustration wrapper.

## Route Structure

The App Router uses route groups to separate the public marketing surface from the (eventual) authed product surface:

```
app/
  layout.tsx           — root layout (fonts, metadata, html/body shell)
  not-found.tsx        — global 404
  globals.css
  icon.svg
  (marketing)/         — public, statically rendered
    page.tsx           — landing page
    privacy/page.tsx
    terms/page.tsx
    docs/page.tsx
  (app)/               — TODO: authed product (dashboard, calls, settings, billing). Add Clerk middleware when this lands.
```

Route groups (`(marketing)`, `(app)`) do not affect URLs. Marketing routes still resolve to `/`, `/privacy`, `/terms`, `/docs`.

## Modularization (Important)

Route files (`page.tsx`, `layout.tsx`) must stay thin. They compose components, nothing more. All UI logic, sections, and visual structure live in dedicated component files under `components/`.

- **Never** inline large markup blocks in `app/**/page.tsx`. Extract every meaningful section into its own component.
- A `page.tsx` should read like a table of contents: a short list of component imports and a clean JSX tree.
- Landing page sections should use the `Section` wrapper from `common/` to get consistent viewport-height behavior on desktop.
- Sub-pages (privacy, terms, docs) compose through the `DocPage` layout component so they share typography, the back-to-home affordance, and the nav/footer shell.

## Conventions

- CTAs use the `PrimaryButton` primitive.
- Nav anchor hrefs are absolute (`/#how`) so they work identically from sub-pages and the home page.
- Interactive elements (buttons, links, clickable cards) must show `cursor: pointer` — the base layer in `globals.css` handles this globally; if you add a custom interactive element that isn't a `button`, `a`, or `[role="button"]`, add `cursor-pointer` explicitly.

## Implementation Status

Track progress here. Update as work lands.

### Done
- Marketing landing page at `/` with hero, how-it-works, integrations, why-hands-free, privacy, faq, get-started CTA.
- Sub-pages: `/privacy`, `/terms`, `/docs` (composed via `DocPage`).
- Design system primitives in `components/common/` (see list above).
- Route groups: `(marketing)/` holds all public routes. `(app)/` is reserved for the authed product and does not exist yet.
- Positioning: "open source today, hosted product coming." Hero CTA and `GetStartedCta` both link to the GitHub repo README.

### Next up
- **Repo README.** The landing CTA terminates at `https://github.com/kevinle623/oncue#readme`. Lift the install runbook from `apps/api/AGENTS.md` into the README so a stranger can self-host in ~30 minutes. This is the bottleneck right now.
- **Cold-clone test.** Run the README on a fresh machine, fix every doc gap.
- **Audio demo on the hero.** 15-second clip embedded in `HeroVisual` or click-to-play.
- **Hosted MVP scaffolding.** When ready, scaffold `(app)/` route group with Clerk middleware + a stub `(app)/dashboard/page.tsx`. Architecture decision is committed: same Next.js app, route groups, JWT-verified calls into `apps/api`. No new monorepo package.

## Landing Page Messaging

The current positioning is **"open source today, hosted product coming."** Two ways to use OnCue:

1. **Today** — clone the repo, plug in your own provider keys (Twilio, Deepgram, ElevenLabs, Anthropic, Spotify), self-host. The hero CTA ("Run it yourself") and the `GetStartedCta` section both lead here. Repo README is the destination.
2. **Eventually** — a hosted version with a full UI. Listed as the first roadmap item ("Hosted app (no setup) — Soon") in `Integrations`. No waitlist signup exists yet; do not invent one in copy.

Spotify is the only live integration. Apple Music is intentionally not on the roadmap (Siri + CarPlay already covers it). Keep copy honest about what's real today vs. what's coming.

## Before Declaring Done

```sh
bun run lint
bun run build
```
