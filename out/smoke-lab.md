# Design Motion Studio — Smoke Lab

Generated: 2026-10-27 00:22:10 EDT (America/New_York)
Source: pasted (336 chars)

## Brief

A short anti-slop lab for TokenMax burn night.

## Slop-Free Score

**100% (A)** — automated 34 pass / 0 fail / 1 review of 35 detectors (catalog 62 rules).

Formula: `max(0, 100 - (8×Critical + 4×High + 1.5×Medium)) on automated fails`

## Design system suggestions

- **Palette:** Ink night (restrained dark) (`ink-night`) — Dark only when the brief asks; gold accent instead of purple glow.
- **Accent:** `#e8b86d` / secondary `#6ec6ff`
- **Type:** IBM Plex Sans / IBM Plex Sans / IBM Plex Mono
- **Scale:** 13 · 15 · 18 · 24 · 32 · 44
- **Pattern:** Audit lab — checklists, scorers, design systems

### Token snippet

```css
:root {
  --bg: #0f1419;
  --panel: #1a222c;
  --ink: #e7ecf3;
  --muted: #9aa7b8;
  --line: #2a3544;
  --accent: #e8b86d;
  --accent-2: #6ec6ff;
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
  --font-display: "IBM Plex Sans", system-ui, sans-serif;
  --font-body: "IBM Plex Sans", system-ui, sans-serif;
  --font-mono: "IBM Plex Mono", ui-monospace, monospace;
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

- `type.tokens` — :root present but few custom properties — expand token set.

## Six-panel motion storyboard

Concept: One motion idea per view: feedback + hierarchy. No parallax, no infinite floats.

### Panel 1 — Idle / entry
- **Intent:** Establish the resting state and what the user can do first.
- **Action:** First paint of the primary surface; no decorative loops.
- **Timing:** 0–150 · none / ease-out
- **Props:** opacity
- **Reduced motion:** Show final idle state immediately.
- **Note:** For Smoke Lab: keep this beat tied to the brief — A short anti-slop lab for TokenMax burn night.

### Panel 2 — Focus / hierarchy
- **Intent:** Point attention at the primary action or score.
- **Action:** Subtle emphasis on focal CTA or score number.
- **Timing:** 150–250 · cubic-bezier(0.2, 0.8, 0.2, 1)
- **Props:** opacity, transform (≤4px)
- **Reduced motion:** Static emphasis via weight/contrast only.
- **Note:** For Smoke Lab: keep this beat tied to the brief — A short anti-slop lab for TokenMax burn night.

### Panel 3 — Input → busy
- **Intent:** Acknowledge the user's submit/generate action.
- **Action:** Button press (~scale 0.97) then loading affordance.
- **Timing:** 100–200 · ease-out
- **Props:** transform, opacity
- **Reduced motion:** Swap label to 'Working…' with no motion.
- **Note:** For Smoke Lab: keep this beat tied to the brief — A short anti-slop lab for TokenMax burn night.

### Panel 4 — Result reveal
- **Intent:** Show the new design system / score without a theme park.
- **Action:** Cross-fade result panel; one staggered list max.
- **Timing:** 200–350 · ease-out
- **Props:** opacity, transform (Y 8px→0)
- **Reduced motion:** Instant swap to result; keep reading order.
- **Note:** For Smoke Lab: keep this beat tied to the brief — A short anti-slop lab for TokenMax burn night.

### Panel 5 — Storyboard / detail
- **Intent:** Walk six motion panels or findings without scroll hijacks.
- **Action:** Panel-to-panel continuity; shared element if any.
- **Timing:** 200–300 · ease-out
- **Props:** opacity, transform
- **Reduced motion:** Paginate with no travel; fade only if needed.
- **Note:** For Smoke Lab: keep this beat tied to the brief — A short anti-slop lab for TokenMax burn night.

### Panel 6 — Exit / next
- **Intent:** Clear next step: export report, fix fails, or re-run.
- **Action:** CTA settle; toast confirm on save.
- **Timing:** 150–250 · ease-out
- **Props:** opacity, transform
- **Reduced motion:** Toast appears static; no slide.
- **Note:** For Smoke Lab: keep this beat tied to the brief — A short anti-slop lab for TokenMax burn night.

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
| typography | 2 | 0 | 1 | 5 |

## Inspired by

- https://x.com/AmirMushich/status/2113692928824484078
- https://github.com/pbakaus/impeccable
- https://github.com/nextlevelbuilder/ui-ux-pro-max-skill
