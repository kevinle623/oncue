# Handoff: OnCue Marketing Landing Page

## Overview
A single long-scroll marketing page for **OnCue** — a hands-free AI voice assistant for drivers. Users call a phone number, speak naturally, and an LLM with tool-calling handles connected apps (Spotify live; more on the roadmap). The page's primary goal is waitlist signups. There is no authenticated area.

## About the Design Files
`OnCue Landing Page v2.html` is a **high-fidelity design reference built in HTML/CSS/JS**. It is not production code — do not ship it directly. Your task is to **recreate this design in Next.js 15+ App Router** using **shadcn/ui primitives** and **Tailwind v4 with CSS variables**, matching the visual output pixel-for-pixel. The HTML file is your source of truth for layout, copy, spacing, color, and interaction.

Open the file in a browser to see the live prototype. All copy is final.

## Fidelity
**High-fidelity.** Colours, typography, spacing, copy, and interactions are all final. Recreate them precisely using shadcn/ui and Tailwind v4 tokens — do not substitute your own values.

---

## Design Tokens
Paste this block into `app/globals.css` under `@theme inline` and `:root`:

```css
@theme inline {
  --color-background:        #F4F1EB;
  --color-foreground:        #1A1814;
  --color-surface:           #EDEAE3;
  --color-surface-low:       #E5E2DA;
  --color-surface-lowest:    #DAD7CF;
  --color-surface-high:      #F0EDE6;
  --color-muted:             #C8C4BC;
  --color-muted-foreground:  #787268;
  --color-accent:            #1A1814;
  --color-accent-foreground: #F4F1EB;
  --color-accent-soft:       #E0DDD5;
  --color-border:            #D8D4CC;
  --color-border-strong:     #B8B4AC;
}

:root {
  --background:        #F4F1EB;
  --foreground:        #1A1814;
  --surface:           #EDEAE3;
  --surface-low:       #E5E2DA;
  --surface-lowest:    #DAD7CF;
  --surface-high:      #F0EDE6;
  --muted:             #C8C4BC;
  --muted-foreground:  #787268;
  --accent:            #1A1814;
  --accent-foreground: #F4F1EB;
  --accent-soft:       #E0DDD5;
  --border:            #D8D4CC;
  --border-strong:     #B8B4AC;
}
```

## Typography
- **Display / headings:** `Instrument Serif` (Google Fonts) — italic variant is used heavily
- **Body / UI:** `DM Sans` (Google Fonts) — weights 300, 400, 500, 600 used

```html
<link href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=DM+Sans:wght@300;400;500;600&display=swap" rel="stylesheet" />
```

---

## Sections

### 1. Navigation Bar
- Fixed, full-width, `z-index: 100`
- On load: transparent with a top-to-bottom gradient fade (`rgba(244,241,235,0.9)` → transparent)
- On scroll past 60px: solid `rgba(244,241,235,0.94)` + `backdrop-filter: blur(12px)` + 1px bottom border (`--border`)
- **Wordmark:** inline-flex, baseline-aligned
  - `on` — Instrument Serif italic, 24px, opacity 0.35
  - `Cue` — Instrument Serif italic, 24px, full opacity, `letter-spacing: -0.02em`
- **CTA button** (right): "Join waitlist" — DM Sans 500, 13px, `letter-spacing: 0.06em`, uppercase, `background: var(--accent)`, `color: var(--accent-foreground)`, `padding: 9px 20px`, `border-radius: 3px`. Scrolls to `#waitlist` section on click.

---

### 2. Hero
- Full viewport height (`100svh`), centered content, `overflow: hidden`
- **Eyebrow:** "Hands-free AI voice assistant for drivers" — 11px, DM Sans 500, `letter-spacing: 0.18em`, uppercase, `color: var(--accent)`, `margin-bottom: 24px`
- **Headline:** "Drive. Speak. / Everything onCue."
  - Font: Instrument Serif italic
  - Size: `clamp(44px, 8vw, 88px)`, `line-height: 1.0`, `letter-spacing: -0.02em`
  - "on" in second line: `opacity: 0.35` — this is intentional brand styling
  - Full headline is italic (inside `<em>` from second line)
- **Sub-copy:** "Your voice is the interface." — `clamp(16px, 2.5vw, 20px)`, DM Sans 300, `color: var(--muted-foreground)`, `line-height: 1.5`, `max-width: 480px`
- **CTA:** "Join the waitlist" primary button — same style as nav CTA but `padding: 16px 40px`
  - Hover: `opacity: 0.9`, `transform: translateY(-2px)`, box-shadow glow
- **Note below CTA:** "Free during beta · No app to install" — 12px, `color: var(--muted-foreground)`
- **Ambient visual (background SVG):**
  - Animated concentric sonar rings (SVG `<circle>` with `<animate>` expanding from r=80 to r=260, fading out, 3 rings offset 1s apart, stroke `#1A1814`, 3s duration, repeat infinite)
  - Horizontal speed lines (7× `<rect>` elements, varying widths/opacities, `<animateTransform>` translating from off-left to off-right, durations 2.5–4.1s, staggered `begin` values, fill `#1A1814`, overall `opacity: 0.18`)
  - Radial gradient overlay: centre transparent → edges `rgba(244,241,235,0.85)`
- **Scroll hint:** 1px vertical line, 48px, gradient fade, subtle pulse animation

---

### 3. How It Works
- Background: `var(--background)`; max-width 1080px centred; padding 100px 24px
- **Section label:** "How it works" — 11px, DM Sans 500, `letter-spacing: 0.18em`, uppercase, `color: var(--accent)`
- **Title:** "Three steps. / That's the whole thing." — Instrument Serif, `clamp(34px, 5vw, 56px)`
- **Steps grid:** 3 columns on ≥768px, stacked on mobile
  - Desktop: columns divided by `border-left: 1px solid var(--border)`, first column no border
  - Mobile: rows divided by `border-top: 1px solid var(--border)`
  - Each step: step number (01/02/03) in `color: var(--accent)`, 13px, `letter-spacing: 0.1em`; small SVG icon (56×56); step title in Instrument Serif 28px; body in DM Sans 300 15px `color: var(--muted-foreground)`
- Step copy:
  - 01 — **Call the number** — "Any phone, any carrier. Dial it from any phone, any carrier. No internet required — just a call."
  - 02 — **Speak naturally** — "\"Play something chill.\" \"Skip this track.\" \"Turn it up.\" OnCue understands you the way you actually talk."
  - 03 — **The assistant does it** — "Actions happen instantly. You get a brief audio confirmation and you're back to the road."

---

### 4. What It Controls Today (Integrations)
- Background: `var(--surface-low)`, `border-top` and `border-bottom: 1px solid var(--border)`
- **Section label:** "What it controls today"
- **Title:** "Start with music. / The rest is coming." — italic `music.`
- **Body:** "Spotify is live. We're adding more integrations through 2025 — not because we're slow, but because each one has to work perfectly before it ships."
- **Layout:** row on ≥768px — live card (fixed 240px wide) + roadmap list (flex 1)
- **Live card** (`border: 1px solid var(--border-strong)`, `border-radius: 8px`, `background: var(--surface)`, padding 28px):
  - Label: "Live now" — 10px, letter-spaced, `color: var(--accent)`
  - Spotify logo: 32px circle `background: #1DB954`, SVG icon inside
  - Example commands: "Play something to focus." / "Skip." / "Turn it down a bit." / "What's this song?"
- **Roadmap list:**
  - Title: "On the roadmap" — 13px, uppercase, `color: var(--muted-foreground)`
  - Items (each `border: 1px solid var(--border)`, `border-radius: 6px`, `background: var(--surface)`):
    1. Apple Music — **Soon**
    2. Trip Planning — **2026**
    3. Food & Coffee Orders — **2026**
    4. Smart Home — **Later**

---

### 5. Why Hands-Free Matters
- Background: `var(--background)`; max-width 1080px
- **Title:** "Eyes on the road. / *Always.*"
- **Stats grid:** 2×2 on mobile, 4-column on ≥768px; `background: var(--border)` gap-1px grid; each cell `background: var(--surface)`; `border-radius: 4px overflow: hidden`
  - 9× — "more crashes when dialing manually vs. hands-free"
  - 5s — "average eyes-off-road time to skip a track"
  - 88% — "of drivers admit to phone use while driving"
  - 0 — "screen interactions required with OnCue"
  - Stat numbers: Instrument Serif, `clamp(36px, 5vw, 52px)`, `color: var(--accent)`
- **Two-column copy** (≥768px): Two paragraphs in DM Sans 300 16px, `color: var(--muted-foreground)`, bold words use `<strong>` at `font-weight: 400`, `color: var(--foreground)`

---

### 6. Privacy & Trust
- Background: `var(--accent-soft)` (`#E0DDD5`); border top/bottom `rgba(26,24,20,0.12)`; padding 80px 24px
- **Layout:** 2-column on ≥768px — title+body left, checklist right; centred alignment
- **Title:** "Your voice. / *Not our data.*" — Instrument Serif, `clamp(30px, 4vw, 44px)`
- **Body:** "Trust is a precondition for hands-free. We built the privacy model first, then the product."
- **Checklist** (3 items, each `background: rgba(255,255,255,0.5)`, `border: 1px solid rgba(26,24,20,0.1)`, `border-radius: 6px`, padding 18px 20px):
  - Checkbox icon: 20×20px, `border: 1px solid var(--accent)`, `border-radius: 3px`, SVG checkmark inside
  - "Calls are never recorded or used to train models. Audio is processed in real-time and discarded."
  - "You control which services OnCue can access. Revoke any integration from your account page, instantly."
  - "OnCue only acts on explicit commands. No passive listening, no background activity between calls."

---

### 7. FAQ
- Background: `var(--background)`; max-width 680px centred
- **Title:** "Questions."
- **6 accordion items** — `border-top: 1px solid var(--border)` on list, `border-bottom` on each item
  - Click toggles open/close; only one open at a time
  - Closed: question text + `+` icon (two perpendicular 12px lines)
  - Open: `+` rotates to `−` (vertical bar fades/rotates), answer slides in (`max-height` transition from 0 → 300px)
  - Questions & answers:
    1. **How much does OnCue cost?** — Free during beta. After launch, simple monthly plan. Waitlist members get extended free period + locked-in pricing.
    2. **Does it work on any phone?** — Any phone that can make a standard call. No app required.
    3. **What happens if I lose signal mid-call?** — Call ends gracefully. Any in-progress action completed or rolled back. Call again when reconnected.
    4. **Can I hang up in the middle of a command?** — Anytime. OnCue finishes the current action then goes idle.
    5. **Does it work with Bluetooth / CarPlay / Android Auto?** — Yes, plays through whatever audio output is connected.
    6. **What languages are supported?** — English at launch; Spanish, French, German in development.

---

### 8. Waitlist CTA (id="waitlist")
- Background: `var(--surface-low)`, `border-top: 1px solid var(--border)`; padding 120px 24px; text-align centre
- **Title:** "Say the word. / *We'll handle it.*" — Instrument Serif, `clamp(36px, 6vw, 64px)`
- **Sub-copy:** "Ready to keep your eyes on the road?"
- **Form:** inline row on ≥480px, stacked on mobile
  - Email input: `background: var(--surface)`, `border: 1px solid var(--border-strong)`, `color: var(--foreground)`, DM Sans 14px, `padding: 14px 18px`, `border-radius: 3px`; focus state: `border-color: var(--accent)`; validation highlights border on invalid submit
  - Submit button: "Reserve spot" — same style as primary CTA
  - On valid submit: form hides, success message shows: "✓  You're on the list. We'll be in touch." in `color: var(--accent)`
  - Enter key on input triggers submit

---

### 9. Footer
- Max-width 1080px centred; padding 48px 24px
- Row layout on ≥768px: wordmark left, nav links centre, legal right
- **Wordmark:** same treatment as nav (Instrument Serif italic, *on* at opacity 0.35, Cue full)
- **Links:** Privacy · Terms · Contact — 12px, `letter-spacing: 0.06em`, uppercase, `color: var(--muted-foreground)`; hover `color: var(--foreground)`
- **Legal:** "© 2026 OnCue. All rights reserved." — 12px, `color: var(--muted-foreground)`

---

## Interactions & Animations

### Scroll reveal
All major sections use a `.reveal` class: `opacity: 0; transform: translateY(24px)` on load, transitions to `opacity: 1; transform: none` when entering viewport (IntersectionObserver, threshold 0.12). Staggered children use `transition-delay` increments of 0.1s.

### Nav on scroll
Sticky nav adds `.scrolled` class at 60px scroll depth — solid background + backdrop blur + border.

### Hero entrance
Each hero element fades up in sequence: eyebrow (0.2s delay), headline (0.35s), sub (0.5s), CTA group (0.65s), scroll hint (1.2s). All use `animation: fadeUp 0.8s forwards`.

### FAQ accordion
`max-height` transition (0 → 300px) with `ease` easing, 0.35s. Plus icon morphs: vertical bar opacity fades to 0 + rotates 90°.

### Primary button hover
`opacity: 0.9`, `transform: translateY(-2px)`, `box-shadow: 0 8px 32px rgba(26,24,20,0.12)`, `transition: 0.2s`.

---

## Responsive Breakpoints
- **Mobile-first** — all base styles are 390px
- `≥480px` — waitlist form becomes inline row
- `≥768px` — How it works becomes 3-col; Integrations becomes row; Stats become 4-col; Why copy becomes 2-col; Privacy becomes 2-col; Footer becomes row

---

## Assets
No external images. All visual elements are inline SVG or CSS. The Spotify icon is an inline SVG path.

---

## Files in This Package
| File | Purpose |
|------|---------|
| `OnCue Landing Page v2.html` | Full hi-fi prototype — open in any browser to see the live design |
| `README.md` | This document |

---

## Suggested Claude Code Prompt

Paste this to get started:

```
I have a high-fidelity HTML design prototype for a marketing landing page (OnCue). 
Please implement it as a Next.js App Router page at app/page.tsx using shadcn/ui 
and Tailwind v4. The design reference is in design_handoff_oncue_landing/OnCue Landing Page v2.html 
— open it in a browser and use it as your pixel-perfect source of truth. 
The README.md in the same folder has all tokens, copy, interactions, and 
component-by-component specs. Start by adding the design tokens to app/globals.css, 
then build each section as a separate component in components/landing/.
```
