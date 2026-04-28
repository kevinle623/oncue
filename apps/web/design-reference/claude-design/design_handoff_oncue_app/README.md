# Handoff: OnCue Product UI — Dashboard, Calls, Settings, Billing

## Overview
Four authenticated product screens for **OnCue** — a hands-free AI voice assistant for drivers. Users call a saved phone number, speak naturally, and an LLM with tool-calling controls connected services (Spotify live; more on roadmap).

## About the Design File
`OnCue App.html` is a **high-fidelity, fully interactive React prototype** — open it in any browser to click through all four screens. It is a design reference, not production code. Your task is to **recreate these screens in the target codebase** (Next.js App Router + shadcn/ui + Tailwind v4 recommended) using its established patterns, matching the visual output pixel-for-pixel.

## Fidelity
**High-fidelity.** All copy, colours, spacing, typography, and interactions are final. Match them precisely.

---

## Design Tokens

```css
/* globals.css */
:root {
  --background:        #F4F1EB;  /* warm cream page bg */
  --foreground:        #1A1814;
  --surface:           #EDEAE3;  /* sidebar bg */
  --surface-low:       #E5E2DA;
  --muted:             #C8C4BC;
  --muted-foreground:  #787268;
  --accent:            #4E7B61;  /* sage green — CTAs, active states, badges */
  --accent-foreground: #F4F1EB;
  --accent-soft:       #EAF0EC;  /* green tint for badges, selected rows */
  --border:            #D8D4CC;
  --border-strong:     #B8B4AC;
  --card:              #FFFFFF;  /* white cards on cream bg */
}
```

## Typography
- **Display / numbers:** `Instrument Serif` italic (Google Fonts)
- **Body / UI:** `DM Sans` weights 300, 400, 500, 600

```html
<link href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=DM Sans:wght@300;400;500;600&display=swap" rel="stylesheet" />
```

---

## Layout Shell

### Sidebar (256px fixed, collapsible to 66px)
- `background: var(--surface)` (#EDEAE3), `border-right: 1px solid var(--border)`
- **Wordmark** at top: inline-flex baseline — `on` (Instrument Serif italic, 22px, opacity 0.35) + `Cue` (Instrument Serif italic, 22px, full opacity, letter-spacing -0.02em)
- **Nav items** (icon + label, 14px DM Sans): default `color: var(--muted-foreground)`, hover `background: rgba(26,24,20,0.05)`, active `background: var(--accent-soft)` + `color: var(--accent)` + `font-weight: 500`
- **User row** at bottom: 28px circle avatar (bg `var(--accent)`, initials), name + email, logout icon
- Nav screens: Dashboard, Calls, Settings, Billing

### Main content area
- `background: var(--background)`, `flex: 1`, `overflow-y: auto`
- Max content width: **860px**, padding: `40px 48px`
- Exception: Calls screen is a full-height master-detail split (no max-width, no padding wrapper)

---

## Screen 1 — Dashboard

### Page header
- Greeting: `"Good morning, [name]."` — Instrument Serif 28px
- Sub: `"Your onCue number is active and ready to take calls."` — 13px, muted-foreground, weight 300

### OnCue number card
- Full-width white card
- Left: number in Instrument Serif italic 36px + helper text below
- Right: **Copy** button (ghost, small) + **Call now** primary button
- Copy button shows "✓ Copied" on click for 2s

### Connected integrations (3-column grid)
Each card: `border: 1px solid var(--border)`, `border-radius: 8px`, `padding: 18px 20px`, white bg
- **Spotify** (connected): green icon, account email, green "Connected" badge
- **Trip Planning** (soon): muted icon, "Launching 2026", muted "Soon" badge, `background: #F4F1EB`
- **Food & Coffee** (soon): same treatment as Trip Planning
- "Manage" ghost button top-right links to Settings screen

### Recent calls (3 rows)
White card, rows separated by `border-bottom: 1px solid #EDEAE3`
Each row: 28px dot icon (music icon) + summary text + time/duration meta + chevron-right
Click any row → navigates to Calls screen
"View all" ghost button → navigates to Calls screen

### Stat strip (3-column)
`background: var(--border)` gap grid, each cell white:
- **24** total calls
- **87** commands run
- **14m** minutes used this month
Numbers in Instrument Serif italic 32px

---

## Screen 2 — Calls

### Layout: master-detail, full viewport height
- **Left panel** (300px fixed, scrollable): `background: var(--background)`, `border-right: 1px solid var(--border)`
- **Right panel** (flex 1, scrollable): `background: #ffffff`

### Left panel — Call list
Page title "Calls" in Instrument Serif 22px at top (padding 24px 16px 12px)
Grouped by day with uppercase date headers (10px, spaced, muted)
Each call row (padding 14px 16px, border-radius 6px):
- 28px circle dot with music icon
- Summary text (13px, foreground)
- Time + duration meta (11px, #B8B4AC)
- Selected state: `background: var(--accent-soft)`, dot border green

Mock data:
```
Today:
  9:41 AM · 2m 14s · "Played focus playlist, adjusted volume twice"
  8:03 AM · 0m 47s · "Skipped track, asked what was playing"
Yesterday:
  6:28 PM · 4m 02s · "Queued road trip playlist, turned volume up"
  2:15 PM · 1m 08s · "Asked what song was playing"
```

### Right panel — Transcript
Call metadata strip at top (4 fields in columns: Number, Started, Ended, Duration — 10px uppercase label + 13px value)
"Transcript" section label
Turn-by-turn transcript:
- Speaker label (52px fixed width, right-aligned, 10px uppercase): "You" (muted) or "OnCue" (accent green)
- Tool-call turns: green card (`background: var(--accent-soft)`, green border, zap icon + text)
- Text turns: 14px body + 10px timestamp offset below

Mock transcript (call 1 — 9:41 AM):
```
00:02  You: "Play something to help me focus."
00:04  [TOOL] Searched Spotify for "focus" playlists
00:04  OnCue: "Playing Deep Focus on Spotify."
00:34  You: "Turn it down a bit."
00:36  [TOOL] Set Spotify volume to 60%
00:36  OnCue: "Done, volume at 60%."
01:12  You: "What's this song?"
01:14  OnCue: "That's Weightless by Marconi Union."
```

### Empty state
Centred card: "No calls yet" + OnCue number + "Call this number to get started."

---

## Screen 3 — Settings

### Layout
Max-width 860px page, sections as white cards stacked with 28px gap between.

### Profile card
Form rows (`border-bottom: 1px solid #EDEAE3`, padding 16px 0):
- **Display name** — editable text input (`min-width: 220px`, `background: var(--background)`, border, border-radius 5px)
- **Email** — read-only, disabled styling
- **OnCue phone number** — disabled input + "Verify different number" ghost button
- Inline "Save profile" primary button bottom-right; shows "✓ Saved" for 2s after click

### Voice & Behavior card
- **Voice** — select dropdown (Aria, Nova, Echo, Fable) + "▶ Preview" ghost button
- **Response length** — segmented control: Terse / Standard / Chatty (selected = white pill on bg surface, unselected = transparent)
- **Wake confirmation tone** — toggle switch (track bg `var(--muted)` off, `var(--accent)` on; 36×20px track, 16px thumb)
- Inline "Save preferences" button

### Integrations card
Spotify row: icon + name + Connected badge + "Disconnect" danger ghost button
Below divider: **Default playback device** select (Last active device / My iPhone / MacBook Pro)
Inline "Save" button

### Danger zone
Separate card: `border: 1px solid rgba(192,57,43,0.2)`, red-tinted label "DANGER ZONE"
Delete account row: description + "Delete account" danger button

---

## Screen 4 — Billing

### Current plan card
Left: plan name "Starter" in Instrument Serif italic 32px + price "$9" serif 28px + "/month" + next billing date
Right: included features list (checkmarks)
Far right: "Manage plan" ghost button

### Usage this month card
"14 of 60 minutes used" — 14 in Instrument Serif italic 28px
Progress bar: height 6px, `border-radius: 3px`, filled `var(--accent)`, warn state (>80%) `#C8813A`
3-cell mini stat grid below (serif numbers): total calls, commands run, minutes

### Payment method card
Visa card chip graphic (44×28px dark rectangle, "VISA" label) + "Visa ending in 4242" + "Expires 08/27" + "Update" ghost button

### Invoices card
Table: Date / Amount / Status / (download)
- Amount in Instrument Serif 14px
- Status: green "Paid" badge
- Download: green link "↓ PDF"

---

## Interactions & Behavior

| Interaction | Behavior |
|---|---|
| Sidebar nav click | Switches active screen; active item highlighted in sage green |
| Copy button | Copies to clipboard; shows "✓ Copied" for 2s |
| FAQ row click | Accordion open/close |
| Settings save buttons | Per-section; show "✓ Saved" confirmation for 2s |
| Toggle | Controlled React state |
| Segmented control | Active pill animates between options |
| Call row click | Selects call, loads transcript in right panel |
| "View all" / "Manage" | Navigate to corresponding screen |

---

## Suggested Claude Code Prompt

```
I have a high-fidelity HTML prototype for the OnCue product UI (Dashboard, Calls, 
Settings, Billing screens). Open design_handoff_oncue_app/OnCue App.html in a browser 
— it's a fully clickable React prototype showing all four screens with real interactions.

Please implement these as authenticated app screens in Next.js App Router using 
shadcn/ui and Tailwind v4. Route structure:
  /dashboard   → Dashboard screen
  /calls       → Calls screen (master-detail)
  /settings    → Settings screen
  /billing     → Billing screen

Use a shared layout at app/(app)/layout.tsx with the sidebar component.

The README.md in design_handoff_oncue_app/ has full specs: design tokens, 
typography, every component's dimensions/colours/copy, interaction behaviour, 
and mock data for the calls transcript. Start with the design tokens in 
globals.css, then the sidebar layout, then build each screen as its own page.
```
