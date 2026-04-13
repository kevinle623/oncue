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

- Tailwind v4 with CSS variables for theming. Dark-only site.
- Tokens live in `app/globals.css` under `@theme inline` and `:root`. Design tokens: `background`, `foreground`, `surface` / `surface-low` / `surface-lowest` / `surface-high`, `muted`, `muted-foreground`, `accent`, `accent-foreground`, `accent-soft`, `border`, `border-strong`.
- Never hardcode hex values in components. Use Tailwind tokens (`bg-surface-low`, `text-accent`, `border-border`, etc).
- Landing page fonts: Inter + Inter Tight via `next/font/google`, wired as `--font-sans` / `--font-heading`.
- `scroll-behavior: smooth` is on globally; `section[id]` has `scroll-margin-top` to clear the fixed nav.

## Component Organization

```
components/
  ui/            shadcn primitives only (button, card, …)
  layout/        nav, footer, doc-page, wordmark
  sections/      one file per landing-page section
  common/        reusable building blocks (container, eyebrow, section, status-dot, radial-glow, section-heading, cta-button)
  illustrations/ visual-only components (hero-visual, faded-image)
  icons/         inline SVG icon components
    brand/       third-party brand glyphs (monochrome, currentColor)
```

Reach for something in `common/` before adding a new one-off. If three callsites end up with the same pattern, extract it.

## Architecture

- App Router, server components by default. Add `"use client"` only when needed.
- Lucide icons for UI iconography. Brand logos are hand-authored monochrome SVGs under `icons/brand/` using `currentColor`.
- Images go through `next/image`. Source files live in `public/images/`. For a soft-edge blend with the background use the `FadedImage` illustration wrapper.

## Modularization (Important)

Route files (`page.tsx`, `layout.tsx`) must stay thin. They compose components, nothing more. All UI logic, sections, and visual structure live in dedicated component files under `components/`.

- **Never** inline large markup blocks in `app/**/page.tsx`. Extract every meaningful section into its own component.
- A `page.tsx` should read like a table of contents: a short list of component imports and a clean JSX tree.
- Landing page sections should use the `Section` wrapper from `common/` to get consistent viewport-height behavior on desktop.
- Sub-pages (privacy, terms, docs) compose through the `DocPage` layout component so they share typography, the back-to-home affordance, and the nav/footer shell.

## Conventions

- CTAs use the `CtaButton` primitive. Pass `disabled` when the destination isn't shipped yet — it renders a dimmed "Coming soon" affordance instead of a live link.
- Nav anchor hrefs are absolute (`/#how`) so they work identically from sub-pages and the home page.
- Interactive elements (buttons, links, clickable cards) must show `cursor: pointer` — the base layer in `globals.css` handles this globally; if you add a custom interactive element that isn't a `button`, `a`, or `[role="button"]`, add `cursor-pointer` explicitly.

## Before Declaring Done

```sh
bun run lint
bun run build
```
