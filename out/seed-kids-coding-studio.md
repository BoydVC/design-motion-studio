# Design Motion Studio — Kids Coding Studio

Generated: 2026-10-27 00:22:10 EDT (America/New_York)
Source: /workspace/tokenmax/kids-coding-studio/web/index.html, /workspace/tokenmax/kids-coding-studio/web/app.css, /workspace/tokenmax/kids-coding-studio/web/app.js (40200 chars)

## Brief

Local creative studio for Char (~13) and Vic (~11): age-safe project briefs, block lanes, parent overview, AI helper default off. Port 4331. Needs a warm playful system that does not look like purple neon SaaS slop.

## Slop-Free Score

**100% (A)** — automated 35 pass / 0 fail / 0 review of 35 detectors (catalog 62 rules).

Formula: `max(0, 100 - (8×Critical + 4×High + 1.5×Medium)) on automated fails`

## Design system suggestions

- **Palette:** Playful kids studio (`playful-kids`) — Kid-safe warmth; avoid neon purple on dark for Char/Vic tools.
- **Accent:** `#e4572e` / secondary `#2a9d8f`
- **Type:** Nunito / Nunito / ui-monospace
- **Scale:** 15 · 17 · 22 · 30 · 40
- **Pattern:** Creative studio — kids/makers tools

### Token snippet

```css
:root {
  --bg: #fff8ef;
  --panel: #ffffff;
  --ink: #1e1b2e;
  --muted: #6b6680;
  --line: #eadfce;
  --accent: #e4572e;
  --accent-2: #2a9d8f;
  --radius: 12px;
  --space-1: 4px;
  --space-2: 8px;
  --space-3: 16px;
  --space-4: 24px;
  --space-5: 40px;
  --shadow: 0 1px 0 var(--line);
  --font-display: var(--font-body);
  --font-body: IBM Plex Sans, system-ui, sans-serif;
  --font-mono: IBM Plex Mono, ui-monospace, monospace;
  --font-display: "Nunito", system-ui, sans-serif;
  --font-body: "Nunito", system-ui, sans-serif;
  --font-mono: "ui-monospace", ui-monospace, monospace;
}
```

### Anti-patterns to ban

- No purple-to-blue gradients; accents stay brand-owned.
- No Inter/Roboto-by-default; name the faces in DESIGN.md.
- No three identical feature cards on marketing surfaces.
- Motion explains state change; honor prefers-reduced-motion.
- Copy states a specific outcome — ban unlock/supercharge/seamless.
- Tokens in :root before one-off hex in components.

## Automated fails

_No automated fails._

## Review queue

_No review-flagged items._

## Six-panel motion storyboard

Concept: One motion idea per view: feedback + hierarchy. No parallax, no infinite floats.

### Panel 1 — Idle / entry
- **Intent:** Establish the resting state and what the user can do first.
- **Action:** First paint of the primary surface; no decorative loops.
- **Timing:** 0–150 · none / ease-out
- **Props:** opacity
- **Reduced motion:** Show final idle state immediately.
- **Note:** For Kids Coding Studio: keep this beat tied to the brief — Local creative studio for Char (~13) and Vic (~11): age-safe project briefs, block lanes, parent overview, AI helper def…

### Panel 2 — Focus / hierarchy
- **Intent:** Point attention at the primary action or score.
- **Action:** Subtle emphasis on focal CTA or score number.
- **Timing:** 150–250 · cubic-bezier(0.2, 0.8, 0.2, 1)
- **Props:** opacity, transform (≤4px)
- **Reduced motion:** Static emphasis via weight/contrast only.
- **Note:** For Kids Coding Studio: keep this beat tied to the brief — Local creative studio for Char (~13) and Vic (~11): age-safe project briefs, block lanes, parent overview, AI helper def…

### Panel 3 — Input → busy
- **Intent:** Acknowledge the user's submit/generate action.
- **Action:** Button press (~scale 0.97) then loading affordance.
- **Timing:** 100–200 · ease-out
- **Props:** transform, opacity
- **Reduced motion:** Swap label to 'Working…' with no motion.
- **Note:** For Kids Coding Studio: keep this beat tied to the brief — Local creative studio for Char (~13) and Vic (~11): age-safe project briefs, block lanes, parent overview, AI helper def…

### Panel 4 — Result reveal
- **Intent:** Show the new design system / score without a theme park.
- **Action:** Cross-fade result panel; one staggered list max.
- **Timing:** 200–350 · ease-out
- **Props:** opacity, transform (Y 8px→0)
- **Reduced motion:** Instant swap to result; keep reading order.
- **Note:** For Kids Coding Studio: keep this beat tied to the brief — Local creative studio for Char (~13) and Vic (~11): age-safe project briefs, block lanes, parent overview, AI helper def…

### Panel 5 — Storyboard / detail
- **Intent:** Walk six motion panels or findings without scroll hijacks.
- **Action:** Panel-to-panel continuity; shared element if any.
- **Timing:** 200–300 · ease-out
- **Props:** opacity, transform
- **Reduced motion:** Paginate with no travel; fade only if needed.
- **Note:** For Kids Coding Studio: keep this beat tied to the brief — Local creative studio for Char (~13) and Vic (~11): age-safe project briefs, block lanes, parent overview, AI helper def…

### Panel 6 — Exit / next
- **Intent:** Clear next step: export report, fix fails, or re-run.
- **Action:** CTA settle; toast confirm on save.
- **Timing:** 150–250 · ease-out
- **Props:** opacity, transform
- **Reduced motion:** Toast appears static; no slide.
- **Note:** For Kids Coding Studio: keep this beat tied to the brief — Local creative studio for Char (~13) and Vic (~11): age-safe project briefs, block lanes, parent overview, AI helper def…

## Category scorecard

| Category | pass | fail | review | skip |
|---|---:|---:|---:|---:|
| a11y | 5 | 0 | 0 | 1 |
| ai-slop | 15 | 0 | 0 | 3 |
| assets | 1 | 0 | 0 | 1 |
| color | 1 | 0 | 0 | 5 |
| copy | 0 | 0 | 0 | 2 |
| layout | 4 | 0 | 0 | 4 |
| motion | 5 | 0 | 0 | 1 |
| states | 1 | 0 | 0 | 5 |
| typography | 3 | 0 | 0 | 5 |

## Inspired by

- https://x.com/AmirMushich/status/2113692928824484078
- https://github.com/pbakaus/impeccable
- https://github.com/nextlevelbuilder/ui-ux-pro-max-skill
