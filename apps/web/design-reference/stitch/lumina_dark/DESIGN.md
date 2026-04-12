# Design System Specification: The Obsidian Standard

## 1. Overview & Creative North Star
**Creative North Star: "The Digital Monolith"**

This design system is built on the principles of precision, intentionality, and quiet confidence. It moves away from the "busy" nature of modern SaaS to embrace a high-end editorial feel inspired by the craft of Linear and the rhythmic minimalism of Rauno.me. 

The aesthetic is characterized by **Hard Precision**. We reject soft shadows and blurred glass in favor of razor-sharp hairline borders, high-contrast typography scales, and a near-void background. By utilizing intentional asymmetry and expansive negative space, we create an environment where every pixel feels deliberate. The goal is not just a dark mode; it is a "Dark Room" experience where the content is the only light source.

---

## 2. Colors & Surface Logic

The color palette is anchored in a monochromatic near-black spectrum, punctuated by a singular, warm amber sun. 

### The Palette
*   **Background (`#0A0A0B` / `surface`):** The absolute foundation. A deep, ink-like black that grounds all components.
*   **Primary (`#FFB547` / `primary_container`):** Our Warm Amber. Used sparingly for moments of maximum impact: CTAs, active states, and the logo mark.
*   **On-Surface (`#F5F5F4` / `on_surface`):** An off-white that prevents visual fatigue while maintaining extreme legibility.

### The "No-Line" Sectioning Rule
Traditional 1px solid borders for sectioning are prohibited. To separate large logical areas, use **Background Tonal Shifts**. 
*   Move from `surface` (#131314) to `surface_container_low` (#1C1B1C) to define headers or footers.
*   The transition must be felt, not seen.

### Surface Hierarchy & Nesting
Instead of shadows, we use **Tonal Stacking** to create depth.
1.  **Base Layer:** `surface` (#131314)
2.  **Middle Layer (Sections):** `surface_container_low` (#1C1B1C)
3.  **Top Layer (Interactive Cards):** `surface_container_high` (#2A2A2B)

### Signature Textures: Radial Glows
To avoid a "flat" appearance, use faint radial gradients centered behind primary elements. 
*   **Formula:** `radial-gradient(circle at center, rgba(255, 181, 71, 0.05) 0%, rgba(10, 10, 11, 0) 70%)`.
*   This provides a subtle "soul" to the layout without compromising the minimal aesthetic.

---

## 3. Typography

The typographic system relies on the contrast between the rhythmic density of **Inter Tight** and the functional clarity of **Inter**.

*   **Display & Headlines (Inter Tight):** Used for `display-lg` through `headline-sm`. 
    *   *Styling:* Set with `-2%` to `-4%` letter spacing (tight tracking). This creates a "block" of text that feels architectural and premium.
*   **Titles & Body (Inter):** Used for `title-lg` through `body-sm`. 
    *   *Styling:* Standard tracking. Focus on generous line-height (`1.6` for body) to ensure the dark theme remains breathable.
*   **Labels (Inter):** Used for `label-md` and `label-sm`. 
    *   *Styling:* Uppercase with `+5%` letter spacing. This differentiates functional metadata from narrative content.

---

## 4. Elevation & Precision

This system explicitly forbids glassmorphism and traditional shadows. We communicate "lift" through precision.

*   **The Hairline Border:** The only allowed border style is a `1px` stroke using `rgba(255, 255, 255, 0.08)`. This creates a "razor's edge" look common in high-end hardware interfaces.
*   **The Layering Principle:** Place `surface_container_highest` (#353436) cards on top of `surface_dim` (#131314) backgrounds. The contrast in value provides all the "elevation" needed.
*   **The "Ghost Border" Fallback:** For interactive states (hover), increase the hairline opacity from `0.08` to `0.2`. Never use 100% opaque borders.
*   **Corner Radii:** We use a "Humanist Geometric" scale. 
    *   `DEFAULT` (4px) for buttons and inputs.
    *   `lg` (8px) for cards.
    *   No "extra-large" or pill-shaped containers unless they are `full` (9999px) for specific tags.

---

## 5. Components

### Buttons
*   **Primary:** Background `primary_container` (#FFB547), text `on_primary_fixed` (#291800). No gradient, no shadow.
*   **Secondary:** Background `transparent`, border `1px hairline`, text `on_surface`.
*   **Tertiary:** Background `transparent`, text `on_surface_variant`, no border.

### Cards & Lists
*   **Strict Rule:** No dividers. Use **Vertical White Space** (32px or 48px) to separate list items. 
*   **Hover State:** Change the card background from `surface_container_low` to `surface_container_high`.

### Input Fields
*   **Static:** `surface_container_low` background, 1px hairline border.
*   **Focus:** Border color shifts to `primary` (#FFD9AB) at `40%` opacity. 
*   **Typography:** Labels must use the `label-sm` uppercase style for an editorial look.

### The "Status" Indicator
A signature component for this system. A small 6px solid circle using the `primary` amber, placed next to headlines to indicate "Live" or "Active" states, mimicking high-end stereo equipment LEDs.

---

## 6. Do's and Don'ts

### Do
*   **Do** use extreme white space. If a layout feels "empty," it’s likely working.
*   **Do** use tight tracking on large headings to create visual gravity.
*   **Do** align everything to a strict 8px grid, but break it intentionally with asymmetric image placements.

### Don't
*   **Don't** use box shadows. Not even subtle ones. Use tonal shifts.
*   **Don't** use pure white (#FFFFFF) for body text; it "bleeds" on dark backgrounds. Use `on_surface` (#F5F5F4).
*   **Don't** use icons as primary navigation. Always prefer text labels in `label-md` uppercase for a more sophisticated, editorial feel.
*   **Don't** use glassmorphism or background blurs. Containers must be opaque and solid.