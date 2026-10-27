"""62-style anti-slop checklist with a real detector subset.

Inspired by pbakaus/impeccable (62 deterministic rules) and public anti-slop
audits (design.yaps.ai, jb.desishub.com, agent-design.com). Not a fork —
local TokenMax subset Boyd can run on pasted HTML/CSS.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, asdict
from typing import Callable, Optional

SEVERITY = ("critical", "high", "medium", "info")


@dataclass
class Rule:
    id: str
    name: str
    category: str
    severity: str
    description: str
    automated: bool
    fix: str


@dataclass
class Finding:
    rule_id: str
    name: str
    category: str
    severity: str
    status: str  # pass | fail | skip | review
    detail: str
    automated: bool
    fix: str


def _rx(pattern: str, flags=re.I | re.M) -> re.Pattern:
    return re.compile(pattern, flags)


# --- Detectors: return (status, detail). status in pass|fail|review ---

def _has(src: str, *pats: str) -> bool:
    return any(_rx(p).search(src) for p in pats)


def d_purple_gradient(src: str):
    if _has(src, r"purple|violet|#7c3aed|#8b5cf6|#a78bfa|#6d28d9|#7c5cff|#5b6bff"):
        if _has(src, r"linear-gradient|radial-gradient|bg-gradient"):
            return "fail", "Purple/violet hue appears inside a gradient — classic AI-slop tell."
    return "pass", "No purple/violet gradient detected."


def d_multi_hue_gradient(src: str):
    # purple→pink/orange or cyan→purple style
    if _has(
        src,
        r"linear-gradient\([^)]*(?:purple|violet|#7c|#8b5|#a78|#6d2|#7c5)[^)]*(?:pink|orange|fuchsia|#ec|#f47|#fb7)",
        r"linear-gradient\([^)]*(?:#3d7cff|#3b82f6|blue|cyan)[^)]*(?:#7b5cff|#7c5cff|purple|violet)",
        r"linear-gradient\([^)]*(?:#5eead4|teal|cyan)[^)]*(?:#7c5cff|purple|violet)",
    ):
        return "fail", "Multi-hue 'AI' gradient (cross-family) detected."
    return "pass", "No cross-family AI gradient pattern matched."


def d_gradient_text(src: str):
    if _has(src, r"background-clip\s*:\s*text|bg-clip-text|-webkit-background-clip\s*:\s*text"):
        return "fail", "Gradient text (background-clip: text) found — reserve for one moment or drop."
    return "pass", "No gradient text clipping."


def d_inter_default(src: str):
    if _has(src, r"['\"]Inter['\"]|fonts\.google.*Inter|font-family:[^;]*\bInter\b"):
        return "fail", "Inter detected as a face — pick an intentional typeface instead of the LLM default."
    return "pass", "Inter not referenced."


def d_roboto_default(src: str):
    if _has(src, r"\bRoboto\b"):
        return "fail", "Roboto detected — often an unchosen agent default."
    return "pass", "Roboto not referenced."


def d_system_only_stack(src: str):
    # font-family that is only system-ui/sans-serif with no named face
    m = re.findall(r"font-family\s*:\s*([^;{]+)", src, re.I)
    named = 0
    bare = 0
    for fam in m:
        if re.search(r"[\"']?[A-Z][A-Za-z ]+[\"']?", fam) and not re.search(
            r"^(system-ui|sans-serif|serif|monospace|ui-sans|ui-mono|ui-serif)", fam.strip(), re.I
        ):
            named += 1
        elif re.search(r"system-ui|sans-serif", fam, re.I):
            bare += 1
    if bare and not named:
        return "fail", "Font stacks look system-only with no chosen display/body face."
    return "pass", f"Named faces referenced in {named} font-family declarations."


def d_lorem(src: str):
    if _has(src, r"\blorem ipsum\b", r"\bpain itself\b", r"\bconsectetur adipiscing\b"):
        return "fail", "Placeholder Lorem ipsum copy found."
    return "pass", "No Lorem ipsum."


def d_slop_verbs(src: str):
    hits = re.findall(
        r"\b(unlock|supercharge|seamless|elevate|leverage|effortless|next-?generation|revolutionize|empower)\b",
        src,
        re.I,
    )
    if hits:
        uniq = sorted({h.lower() for h in hits})
        return "fail", f"Slop marketing verbs: {', '.join(uniq)}"
    return "pass", "No classic slop verbs in copy."


def d_emoji_as_icon(src: str):
    # emoji in class=logo / aria / heading-adjacent common patterns
    if _has(src, r"class=[\"'][^\"']*logo[^\"']*[\"'][^>]*>\s*[^\w\s<]{1,3}\s*<"):
        return "fail", "Emoji/symbol used as logo mark."
    # common sparkle AI badge
    if "✨" in src or "🚀" in src[:5000]:
        return "review", "Decorative emoji present — confirm it's not standing in for an icon library."
    return "pass", "No emoji-as-logo pattern matched."


def d_introducing_pill(src: str):
    if _has(src, r"✨\s*Introducing", r"\bIntroducing\b.{0,40}\b", r"class=[\"'][^\"']*badge[^\"']*[\"'][^>]*>\s*✨"):
        return "fail", "Centred 'Introducing…' pill badge pattern detected."
    return "pass", "No Introducing pill."


def d_three_equal_cards(src: str):
    # grid of 3 identical feature cards is hard; flag repeat(3 / 1fr) feature grids
    if _has(
        src,
        r"grid-template-columns\s*:\s*repeat\(\s*3\s*,",
        r"grid-cols-3",
        r"three.?feature",
    ):
        return "fail", "Three-column equal card grid pattern — vary composition."
    return "pass", "No explicit 3-equal-column feature grid."


def d_transition_all(src: str):
    if _has(src, r"transition\s*:\s*all\b", r"transition-all"):
        return "fail", "transition: all / transition-all found — name properties."
    return "pass", "No transition-all."


def d_bounce_easing(src: str):
    if _has(src, r"ease-in-out-bounce|cubic-bezier\([^)]*\)[^;]*bounce|\banimation:[^;]*bounce\b|@keyframes\s+bounce"):
        return "fail", "Bounce/elastic motion tell detected."
    if _has(src, r"\bbounce\b"):
        return "review", "Word 'bounce' appears — verify no elastic easing on UI."
    return "pass", "No bounce easing."


def d_layout_props_animated(src: str):
    if _has(
        src,
        r"transition\s*:[^;]*(?:\bwidth\b|\bheight\b|\btop\b|\bleft\b|\bright\b|\bbottom\b)",
        r"transition-(?:width|height|top|left)",
    ):
        return "fail", "Animating layout properties (width/height/top/left) — prefer transform/opacity."
    return "pass", "No layout-property transitions matched."


def d_prefers_reduced_motion(src: str):
    if _has(src, r"prefers-reduced-motion"):
        return "pass", "prefers-reduced-motion media query present."
    # only fail if there is motion
    if _has(src, r"@keyframes|animation\s*:|transition\s*:"):
        return "fail", "Motion present but no prefers-reduced-motion guard."
    return "pass", "Little/no CSS motion; reduced-motion not required yet."


def d_css_tokens(src: str):
    vars_ = re.findall(r"--[a-zA-Z0-9_-]+", src)
    if len(set(vars_)) >= 4:
        return "pass", f"{len(set(vars_))} distinct CSS custom properties (token-ish)."
    if _has(src, r":root\s*\{"):
        return "review", ":root present but few custom properties — expand token set."
    return "fail", "No meaningful CSS custom property token system detected."


def d_one_h1(src: str):
    h1s = len(re.findall(r"<h1\b", src, re.I))
    if h1s == 0:
        return "fail", "No <h1> — page needs one clear title."
    if h1s > 1:
        return "fail", f"{h1s} <h1> elements — use exactly one."
    return "pass", "Exactly one <h1>."


def d_heading_skip(src: str):
    levels = [int(x) for x in re.findall(r"<h([1-6])\b", src, re.I)]
    if not levels:
        return "review", "No heading tags found (SPA shell?) — verify runtime headings."
    prev = levels[0]
    for lv in levels[1:]:
        if lv > prev + 1:
            return "fail", f"Heading skip h{prev} → h{lv}."
        prev = lv
    return "pass", f"Heading order looks sequential ({len(levels)} headings)."


def d_focus_visible(src: str):
    if _has(src, r":focus-visible", r"focus-visible:"):
        return "pass", "focus-visible styles present."
    if _has(src, r":focus\b"):
        return "review", ":focus present but no :focus-visible — prefer focus-visible rings."
    return "fail", "No focus / focus-visible styles — keyboard users need a ring."


def d_button_hover(src: str):
    if _has(src, r"button:hover|\.btn:hover|\.chip:hover|\.tab:hover"):
        return "pass", "Hover styles on interactive controls found."
    return "fail", "No button/tab/chip :hover styles detected."


def d_viewport_meta(src: str):
    if _has(src, r'<meta[^>]+name=["\']viewport["\']'):
        return "pass", "Viewport meta present."
    return "fail", "Missing viewport meta — mobile layout risk."


def d_lang_attr(src: str):
    if _has(src, r"<html[^>]+lang="):
        return "pass", "html[lang] set."
    return "fail", "Missing lang attribute on <html>."


def d_semantic_main(src: str):
    if _has(src, r"<main\b"):
        return "pass", "<main> landmark present."
    return "fail", "No <main> landmark."


def d_clickable_div(src: str):
    if _has(src, r"<div[^>]+onclick=", r"<span[^>]+onclick="):
        return "fail", "Clickable div/span — use <button> or <a>."
    return "pass", "No onclick on div/span."


def d_heavy_shadow(src: str):
    # large blur shadows
    m = re.findall(r"box-shadow\s*:\s*([^;]+)", src, re.I)
    heavy = 0
    for s in m:
        nums = [float(x) for x in re.findall(r"(\d+(?:\.\d+)?)\s*px", s)]
        if any(n >= 40 for n in nums):
            heavy += 1
    if heavy >= 2:
        return "fail", f"{heavy} heavy drop-shadows (≥40px blur) — prefer hairlines / light elevation."
    if heavy == 1:
        return "review", "One heavy shadow — ok if reserved for a single focal surface."
    return "pass", "No stacked heavy shadows."


def d_rounded_everything(src: str):
    radii = re.findall(r"border-radius\s*:\s*([^;]+)", src, re.I)
    big = sum(1 for r in radii if re.search(r"\b(1[6-9]|[2-9]\d)\s*px\b|1\.?[0-9]?rem|999px|9999px", r))
    if len(radii) >= 8 and big >= 6:
        return "fail", f"Rounded-everything: {big}/{len(radii)} large radii — vary or tokenise."
    return "pass", f"Radius usage looks restrained ({len(radii)} declarations)."


def d_dark_glow(src: str):
    dark = _has(src, r"#0[0-9a-f]{5}|#111|#0b1020|--bg:\s*#0")
    glow = _has(src, r"box-shadow:[^;]*0\s+0\s+\d+px[^;]*(?:#|rgba?|hsl)", r"filter:\s*drop-shadow")
    if dark and glow:
        return "review", "Dark surface + glow combo — classic AI aesthetic; keep only if brand-owned."
    return "pass", "No dark-glow combo flagged."


def d_fake_live_badge(src: str):
    if _has(src, r"\bLive\b", r"\bOnline\b", r"badge\.live|class=[\"'][^\"']*live[^\"']*"):
        # allow if clearly synthetic disclaimer nearby
        if _has(src, r"SYNTHETIC|synthetic digests|not a live feed"):
            return "pass", "Live-ish badge present but synthetic disclaimer found."
        return "review", "'Live/Online' badge — ensure it reflects real state."
    return "pass", "No fake liveness badge."


def d_section_eyebrows(src: str):
    if _has(src, r"\b0[0-9]\s*[—–-]\s*", r"letter-spacing:\s*\.0[6-9]em", r"text-transform:\s*uppercase[^}]{0,80}letter-spacing"):
        # many uppercase wide-track labels
        count = len(re.findall(r"text-transform:\s*uppercase", src, re.I))
        if count >= 4:
            return "fail", f"{count} uppercase eyebrow-style rules — cap eyebrows (~1 per 3 sections)."
        return "review", "Uppercase / wide-track labels present — watch eyebrow overuse."
    return "pass", "No heavy eyebrow pattern."


def d_picsum_placeholder(src: str):
    if _has(src, r"picsum\.photos|placehold\.co|via\.placeholder|source\.unsplash\.com/random"):
        return "fail", "Placeholder image host used as content."
    return "pass", "No placeholder image hosts."


def d_pure_black_white(src: str):
    if _has(src, r"(?:background|color)\s*:\s*#000\b", r"(?:background|color)\s*:\s*black\b"):
        if _has(src, r"(?:background|color)\s*:\s*#fff\b", r"(?:background|color)\s*:\s*white\b"):
            return "review", "Pure black/white pairing — soft neutrals usually read better."
    return "pass", "No pure black/white body pairing."


def d_nested_cards(src: str):
    # .card .card or card inside card in HTML
    if _has(src, r"\.card[^{]*\{[^}]*\.card", r'class="card"[^>]*>[\s\S]{0,400}class="card"'):
        return "fail", "Nested cards detected — flatten hierarchy."
    return "pass", "No nested-card pattern matched."


def d_glassmorphism(src: str):
    if _has(src, r"backdrop-filter\s*:\s*blur"):
        return "review", "Glassmorphism (backdrop-filter blur) — ok once; cheap if everywhere."
    return "pass", "No backdrop blur."


def d_infinite_animation(src: str):
    if _has(src, r"animation:[^;]*infinite", r"animate-pulse|animate-spin"):
        return "fail", "Infinite loop animation — avoid decorative forever-loops."
    return "pass", "No infinite CSS animations."


def d_max_width_prose(src: str):
    if _has(src, r"max-width\s*:\s*(?:6[0-9]|7[0-5])ch\b", r"max-w-prose", r"max-width\s*:\s*(?:40|42|45|48|50|52|55|60)rem"):
        return "pass", "Prose/line-length constraint found."
    if _has(src, r"max-width\s*:\s*\d"):
        return "review", "max-width present but not obviously prose-tuned (45–75ch)."
    return "fail", "No max-width on content containers — long lines risk."


# Catalog: 62 rules. automated=True ones have detectors.
DETECTORS: dict[str, Callable[[str], tuple[str, str]]] = {
    "ai.purple-gradient": d_purple_gradient,
    "ai.multi-hue-gradient": d_multi_hue_gradient,
    "ai.gradient-text": d_gradient_text,
    "ai.inter-default": d_inter_default,
    "ai.roboto-default": d_roboto_default,
    "ai.system-only-stack": d_system_only_stack,
    "ai.lorem": d_lorem,
    "ai.slop-verbs": d_slop_verbs,
    "ai.emoji-logo": d_emoji_as_icon,
    "ai.introducing-pill": d_introducing_pill,
    "ai.three-cards": d_three_equal_cards,
    "ai.dark-glow": d_dark_glow,
    "ai.fake-live": d_fake_live_badge,
    "ai.eyebrows": d_section_eyebrows,
    "ai.glassmorphism": d_glassmorphism,
    "type.tokens": d_css_tokens,
    "type.one-h1": d_one_h1,
    "type.heading-skip": d_heading_skip,
    "a11y.focus-visible": d_focus_visible,
    "a11y.lang": d_lang_attr,
    "a11y.main": d_semantic_main,
    "a11y.clickable-div": d_clickable_div,
    "a11y.viewport": d_viewport_meta,
    "motion.transition-all": d_transition_all,
    "motion.bounce": d_bounce_easing,
    "motion.layout-props": d_layout_props_animated,
    "motion.reduced": d_prefers_reduced_motion,
    "motion.infinite": d_infinite_animation,
    "layout.heavy-shadow": d_heavy_shadow,
    "layout.rounded-all": d_rounded_everything,
    "layout.nested-cards": d_nested_cards,
    "layout.max-width": d_max_width_prose,
    "state.button-hover": d_button_hover,
    "asset.placeholder-img": d_picsum_placeholder,
    "color.pure-bw": d_pure_black_white,
}


def _catalog() -> list[Rule]:
    """Full 62-rule catalog. Subset wired to DETECTORS."""
    rows: list[tuple] = [
        # AI slop (18)
        ("ai.purple-gradient", "Purple/violet gradient", "ai-slop", "high", "No purple→blue/pink gradients as default chrome.", True, "Swap to brand accent; flat fills first."),
        ("ai.multi-hue-gradient", "Cross-family AI gradient", "ai-slop", "high", "Gradients stay in one hue family.", True, "Collapse to one hue or remove."),
        ("ai.gradient-text", "Gradient clipped text", "ai-slop", "medium", "background-clip:text only for rare brand moments.", True, "Use solid ink for headings."),
        ("ai.inter-default", "Inter as default face", "ai-slop", "high", "Inter is the LLM typography default.", True, "Choose a deliberate grotesk/serif/mono."),
        ("ai.roboto-default", "Roboto as default face", "ai-slop", "medium", "Roboto is another common agent default.", True, "Replace with brand face."),
        ("ai.system-only-stack", "System-only font stack", "ai-slop", "medium", "Stacks should name a chosen face, not only system-ui.", True, "Add a named family before fallbacks."),
        ("ai.lorem", "Lorem ipsum copy", "ai-slop", "critical", "Placeholder Latin never ships.", True, "Write real product copy."),
        ("ai.slop-verbs", "Slop marketing verbs", "ai-slop", "high", "Ban unlock/supercharge/seamless/elevate/leverage…", True, "State a falsifiable outcome."),
        ("ai.emoji-logo", "Emoji as logo/icon", "ai-slop", "high", "Emoji is not a brand mark.", True, "Use SVG from one icon set."),
        ("ai.introducing-pill", "Introducing pill badge", "ai-slop", "high", "Centred ✨ Introducing… is a tell.", True, "Drop the pill; lead with the job."),
        ("ai.three-cards", "Three equal feature cards", "ai-slop", "high", "Hero→3 cards is the LLM floorplan.", True, "Vary section layouts."),
        ("ai.dark-glow", "Dark mode + glow accents", "ai-slop", "medium", "Dark mesh + neon glow is stock agent aesthetic.", True, "Earn glow from a light source."),
        ("ai.fake-live", "Fake Live/Online badges", "ai-slop", "medium", "Liveness badges must reflect real state.", True, "Wire real status or remove."),
        ("ai.eyebrows", "Section eyebrow overuse", "ai-slop", "medium", "Uppercase wide-track labels on every section.", True, "Cap ~1 eyebrow per 3 sections."),
        ("ai.glassmorphism", "Glassmorphism everywhere", "ai-slop", "medium", "backdrop-filter blur as default chrome.", True, "One glass surface max."),
        ("ai.blob-hero", "Orphan hero blob glow", "ai-slop", "medium", "Soft blurred blob behind hero with no light story.", False, "Give light a source or remove."),
        ("ai.centered-everything", "Everything-centered layout", "ai-slop", "medium", "All blocks centre-aligned with no editorial axis.", False, "Introduce asymmetry on purpose."),
        ("ai.sparkle-ai", "Sparkle = AI icon", "ai-slop", "medium", "✨ standing in for 'this is AI'.", False, "Use a real mark or none."),
        # Typography (8)
        ("type.tokens", "CSS design tokens present", "typography", "high", "Colors/spacing/radii live in custom properties.", True, "Extract :root tokens."),
        ("type.one-h1", "Exactly one H1", "typography", "high", "One h1 per view.", True, "Demote extras to h2."),
        ("type.heading-skip", "No skipped heading levels", "typography", "medium", "h1→h2→h3 without jumps.", True, "Repair outline order."),
        ("type.scale", "Consistent type scale", "typography", "medium", "Sizes from a defined ramp, not ad-hoc.", False, "Document 14/16/20/28/40 (or similar)."),
        ("type.two-families", "≤2 font families", "typography", "medium", "Display/body (+ optional mono).", False, "Drop the third face."),
        ("type.line-length", "Body 45–75ch", "typography", "medium", "Comfortable measure.", False, "Constrain prose containers."),
        ("type.weight-contrast", "Deliberate weight contrast", "typography", "info", "Not everything medium.", False, "Regular body, semibold labels."),
        ("type.tracking-display", "Tight display tracking", "typography", "info", "Large display uses negative tracking.", False, "tracking −0.02 to −0.05em on heroes."),
        # Color (6)
        ("color.aa-body", "WCAG AA body contrast", "color", "critical", "Body text ≥4.5:1.", False, "Darken ink or lighten surface."),
        ("color.one-accent", "One primary accent", "color", "high", "Competing accents read as noise.", False, "Pick one; demote the rest."),
        ("color.semantic", "Semantic red/green use", "color", "medium", "Red=danger, green=success.", False, "Retarget misused hues."),
        ("color.not-only-signal", "Color not sole signal", "color", "high", "Errors also have text/icon.", False, "Add non-color cue."),
        ("color.pure-bw", "Avoid pure black/white", "color", "info", "Soft neutrals usually win.", True, "Shift to ink/paper tokens."),
        ("color.surface-levels", "3 surface levels", "color", "medium", "bg / elevated / border.", False, "Define --bg,--panel,--line."),
        # Layout (8)
        ("layout.focal", "One focal point", "layout", "high", "Primary action is most prominent.", False, "Resize/recolor competing CTAs."),
        ("layout.grid", "Consistent grid/gutters", "layout", "medium", "Align to a rhythm.", False, "8px spacing scale."),
        ("layout.heavy-shadow", "No stacked heavy shadows", "layout", "medium", "Hairlines > giant blurs.", True, "Reduce blur radius."),
        ("layout.rounded-all", "Radius not universal", "layout", "medium", "One radius on everything is slop.", True, "Tokenise --radius-sm/md."),
        ("layout.nested-cards", "No nested cards", "layout", "high", "Card-in-card flattens hierarchy.", True, "Use flat sections."),
        ("layout.max-width", "Content max-width", "layout", "medium", "Containers constrain line length.", True, "Set max-width on main."),
        ("layout.mobile-stack", "Mobile stack designed", "layout", "high", "Not just shrunk desktop.", False, "Check 375px order + CTA."),
        ("layout.whitespace", "Whitespace as material", "layout", "info", "Earned air, not slide-deck voids.", False, "Pick a density target."),
        # Interaction states (6)
        ("state.button-hover", "Hover on controls", "states", "high", "Buttons/tabs show hover.", True, "Add :hover border/fill."),
        ("state.focus-ring", "Focus-visible ring", "states", "critical", "Keyboard focus is visible.", False, "Add :focus-visible outline."),
        ("state.active", "Active/pressed", "states", "medium", "Press feedback (~scale 0.97).", False, "Add :active transform."),
        ("state.disabled", "Disabled styles", "states", "medium", "Disabled looks disabled.", False, "Lower opacity + pointer-events."),
        ("state.loading", "Loading state", "states", "medium", "Submit shows progress.", False, "Busy button / skeleton."),
        ("state.empty-error", "Empty + error states", "states", "high", "Empty/error are designed.", False, "Write empty copy + error style."),
        # Accessibility (6)
        ("a11y.focus-visible", "focus-visible CSS", "a11y", "critical", "Visible focus styles exist.", True, "Add :focus-visible rules."),
        ("a11y.lang", "html lang", "a11y", "high", "Document language set.", True, 'Add lang="en".'),
        ("a11y.main", "main landmark", "a11y", "high", "<main> wraps content.", True, "Wrap primary content."),
        ("a11y.clickable-div", "No clickable divs", "a11y", "high", "Use button/a.", True, "Replace div onclick."),
        ("a11y.viewport", "Viewport meta", "a11y", "high", "Mobile viewport configured.", True, "Add width=device-width meta."),
        ("a11y.touch-44", "44px touch targets", "a11y", "high", "Controls ≥44×44 on touch.", False, "Pad compact chips."),
        # Motion (6)
        ("motion.transition-all", "No transition:all", "motion", "high", "Name transitioned properties.", True, "transition: transform, opacity."),
        ("motion.bounce", "No bounce easing", "motion", "high", "Bounce/elastic = toy UI.", True, "Use ease-out / custom curve."),
        ("motion.layout-props", "No layout-prop animation", "motion", "high", "Don't animate width/top/left.", True, "Use transform."),
        ("motion.reduced", "prefers-reduced-motion", "motion", "critical", "Honor OS reduced motion.", True, "Wrap motion in media query."),
        ("motion.infinite", "No infinite decorative loops", "motion", "high", "Forever pulses are wallpaper.", True, "Run once or on interaction."),
        ("motion.one-concept", "One motion concept / view", "motion", "medium", "Not a theme park.", False, "Pick fade-up OR hover-lift."),
        # Content / assets (4)
        ("asset.placeholder-img", "No placeholder image hosts", "assets", "critical", "picsum/placehold never final.", True, "Request real assets."),
        ("asset.real-screenshots", "Real product screenshots", "assets", "high", "No div-rectangle fake UIs as proof.", False, "Capture real UI."),
        ("copy.specific-headline", "Specific outcome headline", "copy", "high", "Names the job-to-be-done.", False, "Rewrite hero."),
        ("copy.falsifiable-bullets", "Falsifiable feature bullets", "copy", "medium", "User can verify each claim.", False, "Cut vague lines."),
    ]
    assert len(rows) == 62, len(rows)
    out = []
    for rid, name, cat, sev, desc, auto, fix in rows:
        # force automated flag from DETECTORS
        auto = rid in DETECTORS
        out.append(Rule(rid, name, cat, sev, desc, auto, fix))
    return out


CATALOG = _catalog()


def score_findings(findings: list[Finding]) -> dict:
    crit = sum(1 for f in findings if f.status == "fail" and f.severity == "critical")
    high = sum(1 for f in findings if f.status == "fail" and f.severity == "high")
    med = sum(1 for f in findings if f.status == "fail" and f.severity == "medium")
    # JB formula, ignore info fails (we don't fail info usually)
    raw = 100 - (8 * crit + 4 * high + 1.5 * med)
    score = max(0, int(round(raw)))
    if score >= 90:
        grade = "A"
    elif score >= 75:
        grade = "B"
    elif score >= 60:
        grade = "C"
    else:
        grade = "D"
    auto = [f for f in findings if f.automated]
    auto_fail = sum(1 for f in auto if f.status == "fail")
    auto_pass = sum(1 for f in auto if f.status == "pass")
    return {
        "slop_free_score": score,
        "grade": grade,
        "critical_fails": crit,
        "high_fails": high,
        "medium_fails": med,
        "automated_total": len(auto),
        "automated_pass": auto_pass,
        "automated_fail": auto_fail,
        "automated_review": sum(1 for f in auto if f.status == "review"),
        "manual_review_count": sum(1 for f in findings if not f.automated),
        "formula": "max(0, 100 - (8×Critical + 4×High + 1.5×Medium)) on automated fails",
    }


def run_checks(source: str, *, include_manual: bool = True) -> dict:
    """Run detectors against concatenated HTML/CSS/JS source text."""
    source = source or ""
    findings: list[Finding] = []
    for rule in CATALOG:
        if rule.id in DETECTORS:
            status, detail = DETECTORS[rule.id](source)
            findings.append(
                Finding(
                    rule.id,
                    rule.name,
                    rule.category,
                    rule.severity,
                    status,
                    detail,
                    True,
                    rule.fix,
                )
            )
        elif include_manual:
            findings.append(
                Finding(
                    rule.id,
                    rule.name,
                    rule.category,
                    rule.severity,
                    "skip",
                    "Manual / visual review — not auto-scored in this subset.",
                    False,
                    rule.fix,
                )
            )
    summary = score_findings(findings)
    by_cat: dict[str, dict] = {}
    for f in findings:
        bucket = by_cat.setdefault(f.category, {"pass": 0, "fail": 0, "review": 0, "skip": 0})
        bucket[f.status] = bucket.get(f.status, 0) + 1
    return {
        "catalog_size": len(CATALOG),
        "automated_rules": len(DETECTORS),
        "summary": summary,
        "by_category": by_cat,
        "findings": [asdict(f) for f in findings],
        "fails": [asdict(f) for f in findings if f.status == "fail"],
        "reviews": [asdict(f) for f in findings if f.status == "review"],
    }


def catalog_public() -> list[dict]:
    return [asdict(r) for r in CATALOG]
