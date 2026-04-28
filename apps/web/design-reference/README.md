# Design Reference

Mockups used as visual reference only. Not shipped to production. Claude Code reads these to translate into real Next.js + shadcn/ui + Tailwind components.

## Structure

```
design-reference/
├── claude-design/   — current source. New designs go here.
└── stitch/          — legacy. Older Google Stitch outputs, kept for reference.
```

Each subfolder under `claude-design/` (or `stitch/`) contains the raw HTML, CSS, and any image assets exported from a single design generation. Folder names should describe the screen or surface (e.g. `dashboard`, `calls`, `settings`, `billing`, `oncue_landing_page`).

When iterating on a new design, create a new subfolder rather than overwriting an existing one — keeps the history of explorations intact for reference.
