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

## shadcn/ui

- Always read `components/ui/` to see which primitives are already installed before using one.
- Run `bunx shadcn@latest add <name>` to add missing primitives. Never hand-roll what shadcn provides.
- Currently installed: `button`, `card`.

## Styling

- Tailwind v4 with CSS variables for theming.
- Never hardcode hex values in components. Use CSS variables / Tailwind tokens.
- Landing page fonts: Inter Tight + Inter. App-wide default: Geist.

## Component Organization

- Section components: `components/sections/`
- Layout components: `components/layout/`
- Icons: `components/icons/`
- shadcn primitives: `components/ui/`

## Architecture

- App Router, server components by default. Add `"use client"` only when needed.
- Nova preset, Lucide icons, Radix primitives (via shadcn).

## Modularization (Important)

Route files (`page.tsx`, `layout.tsx`) must stay thin. They compose components, nothing more. All UI logic, sections, and visual structure live in dedicated component files under `components/`.

- **Never** inline large markup blocks in `app/**/page.tsx`. Extract every meaningful section into its own component.
- A `page.tsx` should read like a table of contents: a short list of component imports and a clean JSX tree.
- This keeps pages scannable, components reusable, and diffs focused on what actually changed.
- When a component grows beyond a single responsibility, split it further. Prefer many small files over few large ones.

## Before Declaring Done

```sh
bun run lint
bun run build
```
