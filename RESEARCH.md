# Design Motion Studio — Research

Local TokenMax lab (burn night, America/New_York). Turns a project brief into a
design-system suggestion pass, a 62-style anti-slop checklist with a real
detector subset, and a six-panel motion storyboard. Inspired by Alex's bookmark
of AmirMušić's "10 GitHub repos to turn you into a design/motion studio" post.

## Bookmark seed

- Post: https://x.com/AmirMushich/status/2113692928824484078
- Author: AmirMušić (@AmirMushich)
- Created: 2026-10-23 14:03 America/New_York (2026-10-23T18:03:59.000Z)
- Headline claim: 10 repos, ~550K stars combined, for design/motion studio workflows.
- Repo #1 called out: **impeccable** — anti AI-slop design skill with **62 rule-based checks**
  (https://github.com/pbakaus/impeccable).
- Repo #2: **UI UX Pro Max** — generates a full design system (pattern, palette, type)
  from a project brief (https://github.com/nextlevelbuilder/ui-ux-pro-max-skill).
- Other named tools in the same post: Blender MCP, img2threejs, video-shotcraft,
  HyperFrames, Penpot, Remotion, lemo-opuscar, diagram-design.

This studio deliberately implements a **local subset** of that stack: brief → system
suggestions (Pro Max–shaped) + 62-rule catalog with automated detectors (impeccable–shaped),
plus a motion storyboard so the "motion" half of the bookmark is not just a link list.

## What "AI slop" means in UI

Public write-ups converge on the same tells. Design for AI's anti-slop principles
(https://design.yaps.ai/docs/principles) lists purple-to-blue gradients, orphan hero
blobs, "✨ Introducing…" pills, three identical feature cards, emoji-as-icons,
glassmorphism everywhere, Inter at default tracking, and empty verbs
(Unlock / Supercharge / Seamless / Elevate). Agent's Design (Jul 4, 2026)
(https://agent-design.com/blog/anti-slop-design-checklist) frames the same failure
as a **specification** problem: agents get components without constraints, so they
fall back to training-data defaults.

JB's portable Anti-AI-Slop Design Audit (Aug 2026)
(https://jb.desishub.com/blog/anti-ai-slop-design-audit) turns those tells into a
scored audit across eleven categories (A–K): tokens, type, contrast, layout,
eight interaction states, a11y, responsive safety, motion hygiene, copy honesty,
classic AI tells, and asset integrity. The headline metric is repeatable:

`Slop-Free Score = max(0, 100 - (8 × Critical + 4 × High + 1.5 × Medium))`

Design Motion Studio uses that formula on **automated fails only**, so seed scores
are stable across runs on the same HTML/CSS.

## Impeccable's 62 detectors (reference, not a fork)

pbakaus/impeccable documents 62 **deterministic** detector rules runnable without
an LLM (`npx impeccable detect`), covering AI-slop tells (side-tab borders, purple
gradients, bounce easing, dark glows) and general quality (line length, cramped
padding, small touch targets, skipped headings). Docs also note Inter-for-everything,
cards nested in cards, and gray text on colored backgrounds as the default fail
mode when agents skip guidance (https://github.com/pbakaus/impeccable).

Our catalog mirrors the **count and spirit** (62 rules across ai-slop, typography,
color, layout, states, a11y, motion, assets/copy) with **35 local regex/heuristic
detectors** Alex can run on pasted HTML/CSS. Manual/visual rules stay in the
catalog as `skip` so the scorecard still shows the full surface area. This is not
a binary of impeccable's engine; it is a TokenMax-side lab that stays on Python
stdlib and the box.

## Design tokens as the fix surface

Anti-slop checklists keep repeating the same remediation: fix against the project's
**own** tokens, do not invent one-off hex. The Design Tokens Community Group shipped
stable Format / Color / Resolver modules as **2025.10** Final Community Group
Reports (https://www.designtokens.org/TR/2025.10/format/,
https://www.w3.org/community/design-tokens/). FAQ guidance: core format is safe for
production use even though it is not on the W3C Standards Track
(https://www.designtokens.org/faq/).

Practical emission path for this lab: suggest a `:root` CSS custom-property snippet
(palette, radii, spacing, font roles) so later UI work has somewhere to bind. Tools
like Design Token Kit document CSS emission with theme overrides under
`[data-theme="…"]` and aliases as `var(--name)`
(https://design-token-kit.github.io/docs/core/conversion/). We stay on plain CSS
variables — enough for local TokenMax apps without a DTCG toolchain.

## Motion: storyboard before keyframes

The bookmark's "motion studio" half is easy to fake with decorative loops. Better
practice from motion planning skills and studios:

1. Write intent, primary action, hierarchy, duration, easing, properties, hold, and
   a **reduced-motion** alternative **before** keyframing
   (ui-motion-choreography planning list via Figma Community skill summaries).
2. Treat a motion storyboard / animatic as the cheap revision layer — panels for
   beats, timing, and transitions — before production polish
   (https://olafmotion.com/tips/how-to-storyboard-motion-graphics-for-client-projects/,
   https://www.linearity.io/guide/animation-motion-design/).
3. UI durations stay short: micro-interactions ~100–200ms, panels/drawers ~200–350ms,
   modals ~150–300ms (Linearity UI animation table; Agent's Design 150–300ms band).
4. Animate **transform/opacity**, never width/height/top/left; never `transition: all`;
   never infinite decorative loops (design.yaps.ai rule 6; kylezantos design-motion
   anti-checklist themes; Agent's Design motion section).
5. Accessibility is non-optional: honor `prefers-reduced-motion`, limit concurrent
   movers, give pause/stop where motion autoplays
   (https://www.ta11y.org/en/learning/web/moving-content/motion-and-animation/,
   Atlassian Motion foundations — Human / Clarity / Accessible / Performant —
   https://atlassian.design/foundations/motion).

Design Motion Studio's six panels are a fixed beat map: Idle → Focus → Busy →
Result → Detail → Exit/Next. Each panel carries duration, properties, and a
reduced-motion line so a later Remotion/HyperFrames pass (repos 6–8 in the
bookmark) has a brief instead of vibes.

## Seed targets on this box

1. **Kids Coding Studio** (`/workspace/tokenmax/kids-coding-studio/web/`) — playful
   dark UI with purple/teal gradients, emoji logo mark, sticky glass topbar. Useful
   stress test for ai-slop detectors without dismissing kid warmth.
2. **List Brief Pack** (`/workspace/tokenmax/list-brief-pack/static/`) — ops desk,
   IBM Plex, blue→violet mark gradient, live/synth badges. Tests whether "tool chrome"
   still trips marketing-oriented rules (and whether synthetic disclaimers calm
   fake-live detection).

Reports land under `out/seed-*.json` + `.md` with scores, fails, system suggestions,
and the storyboard filled for that brief.

## Product constraints (TokenMax burn)

- Python **stdlib only** HTTP server on `127.0.0.1:4334`.
- No Cursor cloud agents; no kpdlawgroup; on-demand off.
- Heavy work stays on the box to burn **Grok Bot weekly**, not Cursor Models.
- Cite public sources; do not claim we vendored impeccable's binary.

## Citation list (fetched / searched this build)

1. https://x.com/AmirMushich/status/2113692928824484078 — design/motion repo roundup.
2. https://github.com/pbakaus/impeccable — 62 deterministic anti-slop detectors.
3. https://github.com/nextlevelbuilder/ui-ux-pro-max-skill — brief → system skill.
4. https://design.yaps.ai/docs/principles — ten anti-slop principles + agent checklist.
5. https://jb.desishub.com/blog/anti-ai-slop-design-audit — scored A–K audit + formula.
6. https://agent-design.com/blog/anti-slop-design-checklist — vibe-coder pre-ship audit.
7. https://www.designtokens.org/TR/2025.10/format/ — DTCG Format Module 2025.10.
8. https://www.designtokens.org/faq/ — production-readiness of DTCG 2025.10.
9. https://www.w3.org/community/design-tokens/ — DTCG announcements / modules.
10. https://design-token-kit.github.io/docs/core/conversion/ — CSS custom property emission.
11. https://atlassian.design/foundations/motion — motion principles (accessible/performant).
12. https://www.ta11y.org/en/learning/web/moving-content/motion-and-animation/ — reduced motion strategies.
13. https://olafmotion.com/tips/how-to-storyboard-motion-graphics-for-client-projects/ — motion storyboards.
14. https://www.linearity.io/guide/animation-motion-design/ — animatics + UI duration bands.
15. https://github.com/kylezantos/design-motion-principles — motion anti-patterns (reference).

## How this research shaped the implementation

- **62 catalog rows** so the UI can say "impeccable-shaped" honestly about coverage.
- **35 automated detectors** chosen for signals visible in static HTML/CSS (gradients,
  Inter/Roboto, transition-all, prefers-reduced-motion, h1 count, tokens, etc.).
- **JB score formula** for a single comparable number across Kids vs List Brief seeds.
- **Warm-paper default chrome** in our own studio UI (not dark purple mesh) to dogfood
  the restraint we recommend.
- **Six-panel storyboard** always emitted, even when no HTML is pasted, so motion is
  a first-class deliverable beside the checklist.
- **Seed builder** concatenates real TokenMax app sources so reports reflect shipping
  local UIs, not toy fixtures.

## Open follow-ups (not this burn)

- Optional bridge to `npx impeccable detect` when Node is available — compare scores.
- DTCG JSON export beside the CSS snippet.
- Browser-computed contrast (needs a renderer); today AA contrast stays manual.
- Remotion/HyperFrames export of the six panels as a silent animatic.

## Session note

Built as Grok Bot weekly burn under `/workspace/tokenmax/design-motion-studio/` on
2026-10-26 evening America/New_York. Peer of Brief Forge (:4330), Kids Studio (:4331),
List Brief Pack (:4332), Peer Review Arena (:4333).
