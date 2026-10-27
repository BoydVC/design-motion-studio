# DESIGN.md — Design Motion Studio

## Point of view

This is the lab that **scores TokenMax UIs for AI-slop tells** and hands back a
restrained system + motion brief — not another dark purple gradient dashboard.

## Palette (shipped UI)

Warm paper, not neon mesh:

| Token | Value | Role |
|-------|-------|------|
| `--bg` | `#f6f1ea` | page |
| `--panel` | `#fffaf3` | cards |
| `--ink` | `#1c1916` | text |
| `--muted` | `#6b635a` | secondary |
| `--line` | `#e4d8c8` | borders |
| `--accent` | `#c45c26` | primary CTA |
| `--accent-2` | `#2f5d50` | score / success |

No purple primary. Gradients are banned in chrome; the mark is a flat terracotta tile.

## Type

- UI: IBM Plex Sans (with system-ui fallbacks)
- Mono: IBM Plex Mono for tokens / pasted source
- Display tracking slightly tight on the H1 (`-0.02em`)
- Scale roughly 13 / 15 / 18 / 24 / 32 / 48 (score numeral)

## Layout pattern

**Audit lab:** brief form → score hero → system + fails → six-panel storyboard →
seed report list. Not hero → three feature cards.

## Motion

- One concept: press feedback + result reveal.
- Button `:active { transform: scale(0.97) }`; disabled under `prefers-reduced-motion`.
- No infinite animations, no `transition: all`, no scroll hijacks.
- Storyboard panels are static frames (documentation), not a carousel.

## States

- Hover on `.btn` / ghost buttons
- `:focus-visible` rings on inputs and buttons
- Toast for save/load confirmation
- Empty seeds / no-fail copy are written, not blank

## Anti-patterns (this app)

- [ ] No Inter/Roboto as the only face
- [ ] No purple→blue gradients
- [ ] No ✨ Introducing pill
- [ ] No emoji logo (uses "DM" wordmark tile)
- [ ] No three equal marketing cards
- [ ] Tokens live in `:root` before component paint

## Content voice

Plain ops English. Scores and rule ids over "unlock your design potential."
