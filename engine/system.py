"""Design-system suggestions from a project brief (UI UX Pro Max–inspired)."""
from __future__ import annotations

import hashlib
import re
from typing import Any


PALETTE_PRESETS = {
    "warm-paper": {
        "label": "Warm paper + ink",
        "surface": "#f6f1ea",
        "elevated": "#fffaf3",
        "ink": "#1c1916",
        "muted": "#6b635a",
        "line": "#e4d8c8",
        "accent": "#c45c26",
        "accent_2": "#2f5d50",
        "why": "Editorial, calm, human — fights the default dark-tech mesh.",
    },
    "cool-zinc": {
        "label": "Cool zinc product",
        "surface": "#f4f4f5",
        "elevated": "#ffffff",
        "ink": "#18181b",
        "muted": "#71717a",
        "line": "#e4e4e7",
        "accent": "#2563eb",
        "accent_2": "#0f766e",
        "why": "Clean product UI; one blue accent, no violet defaults.",
    },
    "ink-night": {
        "label": "Ink night (restrained dark)",
        "surface": "#0f1419",
        "elevated": "#1a222c",
        "ink": "#e7ecf3",
        "muted": "#9aa7b8",
        "line": "#2a3544",
        "accent": "#e8b86d",
        "accent_2": "#6ec6ff",
        "why": "Dark only when the brief asks; gold accent instead of purple glow.",
    },
    "playful-kids": {
        "label": "Playful kids studio",
        "surface": "#fff8ef",
        "elevated": "#ffffff",
        "ink": "#1e1b2e",
        "muted": "#6b6680",
        "line": "#eadfce",
        "accent": "#e4572e",
        "accent_2": "#2a9d8f",
        "why": "Kid-safe warmth; avoid neon purple on dark for Alex/Sam tools.",
    },
    "ops-brief": {
        "label": "Ops brief desk",
        "surface": "#0b1020",
        "elevated": "#17223b",
        "ink": "#e8eefc",
        "muted": "#9aadc9",
        "line": "#243154",
        "accent": "#6ea8ff",
        "accent_2": "#3dd68c",
        "why": "Dense reading desk; IBM-ish clarity, accent for urgency only.",
    },
}

TYPE_PRESETS = {
    "editorial": {
        "display": "Fraunces",
        "body": "Source Serif 4",
        "mono": "IBM Plex Mono",
        "scale": ["14", "16", "20", "28", "40", "56"],
        "notes": "Serif display for point-of-view heroes; body stays readable.",
    },
    "product": {
        "display": "IBM Plex Sans",
        "body": "IBM Plex Sans",
        "mono": "IBM Plex Mono",
        "scale": ["13", "15", "18", "24", "32", "44"],
        "notes": "One grotesk family; hierarchy from size/weight, not a third face.",
    },
    "kids": {
        "display": "Nunito",
        "body": "Nunito",
        "mono": "ui-monospace",
        "scale": ["15", "17", "22", "30", "40"],
        "notes": "Rounded but not cartoon-default; skip Inter/Comic Sans.",
    },
    "terminal": {
        "display": "IBM Plex Sans",
        "body": "IBM Plex Sans",
        "mono": "JetBrains Mono",
        "scale": ["13", "15", "18", "22", "28", "36"],
        "notes": "Mono for logs/briefs; display stays sans.",
    },
}

PATTERN_PRESETS = [
    {
        "id": "split-hero",
        "name": "Split hero + proof rail",
        "when": "product or tool with a clear primary action",
        "structure": ["asymmetric hero", "proof/metrics rail", "varied feature sections", "footer"],
    },
    {
        "id": "desk",
        "name": "Reading desk",
        "when": "digests, briefs, reviews",
        "structure": ["sticky topbar", "tabbed panes", "card stack (not 3-equal marketing)", "action chips"],
    },
    {
        "id": "studio",
        "name": "Creative studio",
        "when": "kids/makers tools",
        "structure": ["identity picker", "brief shelf", "workspace lanes", "parent overview"],
    },
    {
        "id": "lab",
        "name": "Audit lab",
        "when": "checklists, scorers, design systems",
        "structure": ["brief form", "score hero", "category scorecard", "findings list", "storyboard"],
    },
]


def _tokens(text: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+", (text or "").lower()))


def pick_palette(name: str, brief: str) -> dict[str, Any]:
    t = _tokens(f"{name} {brief}")
    if t & {"kid", "kids", "child", "char", "vic", "coding", "studio", "inkwright", "play"}:
        key = "playful-kids"
    elif t & {"brief", "digest", "list", "ops", "fleet", "marketplace", "x"}:
        key = "ops-brief"
    elif t & {"dark", "night", "terminal", "agent", "burn"}:
        key = "ink-night"
    elif t & {"editorial", "story", "magazine", "newspaper"}:
        key = "warm-paper"
    else:
        # stable pseudo-random among product-ish
        h = int(hashlib.sha1(f"{name}|{brief}".encode()).hexdigest(), 16)
        key = ["cool-zinc", "warm-paper", "ink-night"][h % 3]
    pal = dict(PALETTE_PRESETS[key])
    pal["preset_id"] = key
    pal["css_vars"] = {
        "--bg": pal["surface"],
        "--panel": pal["elevated"],
        "--ink": pal["ink"],
        "--muted": pal["muted"],
        "--line": pal["line"],
        "--accent": pal["accent"],
        "--accent-2": pal["accent_2"],
        "--radius": "12px",
        "--space-1": "4px",
        "--space-2": "8px",
        "--space-3": "16px",
        "--space-4": "24px",
        "--space-5": "40px",
        "--shadow": "0 1px 0 var(--line)",
        "--font-display": "var(--font-body)",
        "--font-body": "IBM Plex Sans, system-ui, sans-serif",
        "--font-mono": "IBM Plex Mono, ui-monospace, monospace",
    }
    return pal


def pick_type(name: str, brief: str) -> dict[str, Any]:
    t = _tokens(f"{name} {brief}")
    if t & {"kid", "kids", "child", "char", "vic", "play"}:
        key = "kids"
    elif t & {"story", "editorial", "magazine", "reveal"}:
        key = "editorial"
    elif t & {"log", "terminal", "cli", "agent", "brief"}:
        key = "terminal"
    else:
        key = "product"
    out = dict(TYPE_PRESETS[key])
    out["preset_id"] = key
    return out


def pick_pattern(name: str, brief: str) -> dict[str, Any]:
    t = _tokens(f"{name} {brief}")
    if t & {"kid", "kids", "studio", "brief", "lane"}:
        pid = "studio"
    elif t & {"digest", "list", "ops", "pack"}:
        pid = "desk"
    elif t & {"audit", "slop", "checklist", "design", "motion", "score"}:
        pid = "lab"
    else:
        pid = "split-hero"
    for p in PATTERN_PRESETS:
        if p["id"] == pid:
            return dict(p)
    return dict(PATTERN_PRESETS[0])


def suggest_system(name: str, brief: str) -> dict[str, Any]:
    name = (name or "Untitled").strip()
    brief = (brief or "").strip()
    palette = pick_palette(name, brief)
    typography = pick_type(name, brief)
    pattern = pick_pattern(name, brief)
    anti = [
        "No purple-to-blue gradients; accents stay brand-owned.",
        "No Inter/Roboto-by-default; name the faces in DESIGN.md.",
        "No three identical feature cards on marketing surfaces.",
        "Motion explains state change; honor prefers-reduced-motion.",
        "Copy states a specific outcome — ban unlock/supercharge/seamless.",
        "Tokens in :root before one-off hex in components.",
    ]
    return {
        "project": name,
        "brief": brief,
        "palette": palette,
        "typography": typography,
        "pattern": pattern,
        "anti_patterns": anti,
        "token_snippet": _token_snippet(palette, typography),
    }


def _token_snippet(palette: dict, typography: dict) -> str:
    vars_ = palette["css_vars"]
    lines = [":root {"]
    for k, v in vars_.items():
        lines.append(f"  {k}: {v};")
    lines.append(f"  --font-display: \"{typography['display']}\", system-ui, sans-serif;")
    lines.append(f"  --font-body: \"{typography['body']}\", system-ui, sans-serif;")
    lines.append(f"  --font-mono: \"{typography['mono']}\", ui-monospace, monospace;")
    lines.append("}")
    return "\n".join(lines)
