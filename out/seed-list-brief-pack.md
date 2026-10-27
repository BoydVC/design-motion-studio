# Design Motion Studio — List Brief Pack

Generated: 2026-10-27 00:22:10 EDT (America/New_York)
Source: /workspace/tokenmax/list-brief-pack/static/index.html, /workspace/tokenmax/list-brief-pack/static/styles.css, /workspace/tokenmax/list-brief-pack/static/app.js (11947 chars)

## Brief

X Lists → daily digest + Roemmele-style marketplace templates. Local desk on 4332 with synthetic digests and a live sample. Ops reading UI: clear hierarchy, urgency badges, copyable prompts — anti-slop for dense tool chrome.

## Slop-Free Score

**84% (B)** — automated 30 pass / 3 fail / 2 review of 35 detectors (catalog 62 rules).

Formula: `max(0, 100 - (8×Critical + 4×High + 1.5×Medium)) on automated fails`

## Design system suggestions

- **Palette:** Ops brief desk (`ops-brief`) — Dense reading desk; IBM-ish clarity, accent for urgency only.
- **Accent:** `#6ea8ff` / secondary `#3dd68c`
- **Type:** IBM Plex Sans / IBM Plex Sans / JetBrains Mono
- **Scale:** 13 · 15 · 18 · 22 · 28 · 36
- **Pattern:** Creative studio — kids/makers tools

### Token snippet

```css
:root {
  --bg: #0b1020;
  --panel: #17223b;
  --ink: #e8eefc;
  --muted: #9aadc9;
  --line: #243154;
  --accent: #6ea8ff;
  --accent-2: #3dd68c;
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
  --font-mono: "JetBrains Mono", ui-monospace, monospace;
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

- **HIGH** `ai.purple-gradient` — Purple/violet gradient: Purple/violet hue appears inside a gradient — classic AI-slop tell. _Fix:_ Swap to brand accent; flat fills first.
- **HIGH** `ai.multi-hue-gradient` — Cross-family AI gradient: Multi-hue 'AI' gradient (cross-family) detected. _Fix:_ Collapse to one hue or remove.
- **CRITICAL** `a11y.focus-visible` — focus-visible CSS: No focus / focus-visible styles — keyboard users need a ring. _Fix:_ Add :focus-visible rules.

## Review queue

- `ai.eyebrows` — Uppercase / wide-track labels present — watch eyebrow overuse.
- `layout.max-width` — max-width present but not obviously prose-tuned (45–75ch).

## Six-panel motion storyboard

Concept: One motion idea per view: feedback + hierarchy. No parallax, no infinite floats.

### Panel 1 — Idle / entry
- **Intent:** Establish the resting state and what the user can do first.
- **Action:** First paint of the primary surface; no decorative loops.
- **Timing:** 0–150 · none / ease-out
- **Props:** opacity
- **Reduced motion:** Show final idle state immediately.
- **Note:** For List Brief Pack: keep this beat tied to the brief — X Lists → daily digest + Roemmele-style marketplace templates. Local desk on 4332 with synthetic digests and a live samp…

### Panel 2 — Focus / hierarchy
- **Intent:** Point attention at the primary action or score.
- **Action:** Subtle emphasis on focal CTA or score number.
- **Timing:** 150–250 · cubic-bezier(0.2, 0.8, 0.2, 1)
- **Props:** opacity, transform (≤4px)
- **Reduced motion:** Static emphasis via weight/contrast only.
- **Note:** For List Brief Pack: keep this beat tied to the brief — X Lists → daily digest + Roemmele-style marketplace templates. Local desk on 4332 with synthetic digests and a live samp…

### Panel 3 — Input → busy
- **Intent:** Acknowledge the user's submit/generate action.
- **Action:** Button press (~scale 0.97) then loading affordance.
- **Timing:** 100–200 · ease-out
- **Props:** transform, opacity
- **Reduced motion:** Swap label to 'Working…' with no motion.
- **Note:** For List Brief Pack: keep this beat tied to the brief — X Lists → daily digest + Roemmele-style marketplace templates. Local desk on 4332 with synthetic digests and a live samp…

### Panel 4 — Result reveal
- **Intent:** Show the new design system / score without a theme park.
- **Action:** Cross-fade result panel; one staggered list max.
- **Timing:** 200–350 · ease-out
- **Props:** opacity, transform (Y 8px→0)
- **Reduced motion:** Instant swap to result; keep reading order.
- **Note:** For List Brief Pack: keep this beat tied to the brief — X Lists → daily digest + Roemmele-style marketplace templates. Local desk on 4332 with synthetic digests and a live samp…

### Panel 5 — Storyboard / detail
- **Intent:** Walk six motion panels or findings without scroll hijacks.
- **Action:** Panel-to-panel continuity; shared element if any.
- **Timing:** 200–300 · ease-out
- **Props:** opacity, transform
- **Reduced motion:** Paginate with no travel; fade only if needed.
- **Note:** For List Brief Pack: keep this beat tied to the brief — X Lists → daily digest + Roemmele-style marketplace templates. Local desk on 4332 with synthetic digests and a live samp…

### Panel 6 — Exit / next
- **Intent:** Clear next step: export report, fix fails, or re-run.
- **Action:** CTA settle; toast confirm on save.
- **Timing:** 150–250 · ease-out
- **Props:** opacity, transform
- **Reduced motion:** Toast appears static; no slide.
- **Note:** For List Brief Pack: keep this beat tied to the brief — X Lists → daily digest + Roemmele-style marketplace templates. Local desk on 4332 with synthetic digests and a live samp…

## Category scorecard

| Category | pass | fail | review | skip |
|---|---:|---:|---:|---:|
| a11y | 4 | 1 | 0 | 1 |
| ai-slop | 12 | 2 | 1 | 3 |
| assets | 1 | 0 | 0 | 1 |
| color | 1 | 0 | 0 | 5 |
| copy | 0 | 0 | 0 | 2 |
| layout | 3 | 0 | 1 | 4 |
| motion | 5 | 0 | 0 | 1 |
| states | 1 | 0 | 0 | 5 |
| typography | 3 | 0 | 0 | 5 |

## Inspired by

- https://x.com/AmirMushich/status/2113692928824484078
- https://github.com/pbakaus/impeccable
- https://github.com/nextlevelbuilder/ui-ux-pro-max-skill
