"""Six-panel motion storyboard template."""
from __future__ import annotations

from typing import Any


PANEL_TEMPLATE = [
    {
        "panel": 1,
        "beat": "Idle / entry",
        "intent": "Establish the resting state and what the user can do first.",
        "primary_action": "First paint of the primary surface; no decorative loops.",
        "duration_ms": "0–150",
        "easing": "none / ease-out",
        "properties": "opacity",
        "reduced_motion": "Show final idle state immediately.",
    },
    {
        "panel": 2,
        "beat": "Focus / hierarchy",
        "intent": "Point attention at the primary action or score.",
        "primary_action": "Subtle emphasis on focal CTA or score number.",
        "duration_ms": "150–250",
        "easing": "cubic-bezier(0.2, 0.8, 0.2, 1)",
        "properties": "opacity, transform (≤4px)",
        "reduced_motion": "Static emphasis via weight/contrast only.",
    },
    {
        "panel": 3,
        "beat": "Input → busy",
        "intent": "Acknowledge the user's submit/generate action.",
        "primary_action": "Button press (~scale 0.97) then loading affordance.",
        "duration_ms": "100–200",
        "easing": "ease-out",
        "properties": "transform, opacity",
        "reduced_motion": "Swap label to 'Working…' with no motion.",
    },
    {
        "panel": 4,
        "beat": "Result reveal",
        "intent": "Show the new design system / score without a theme park.",
        "primary_action": "Cross-fade result panel; one staggered list max.",
        "duration_ms": "200–350",
        "easing": "ease-out",
        "properties": "opacity, transform (Y 8px→0)",
        "reduced_motion": "Instant swap to result; keep reading order.",
    },
    {
        "panel": 5,
        "beat": "Storyboard / detail",
        "intent": "Walk six motion panels or findings without scroll hijacks.",
        "primary_action": "Panel-to-panel continuity; shared element if any.",
        "duration_ms": "200–300",
        "easing": "ease-out",
        "properties": "opacity, transform",
        "reduced_motion": "Paginate with no travel; fade only if needed.",
    },
    {
        "panel": 6,
        "beat": "Exit / next",
        "intent": "Clear next step: export report, fix fails, or re-run.",
        "primary_action": "CTA settle; toast confirm on save.",
        "duration_ms": "150–250",
        "easing": "ease-out",
        "properties": "opacity, transform",
        "reduced_motion": "Toast appears static; no slide.",
    },
]


def build_storyboard(project: str, brief: str) -> dict[str, Any]:
    project = (project or "Untitled").strip()
    brief = (brief or "").strip()
    panels = []
    for p in PANEL_TEMPLATE:
        row = dict(p)
        row["note"] = f"For {project}: keep this beat tied to the brief — {brief[:120]}{'…' if len(brief) > 120 else ''}"
        panels.append(row)
    return {
        "project": project,
        "concept": "One motion idea per view: feedback + hierarchy. No parallax, no infinite floats.",
        "principles": [
            "Animate transform/opacity only",
            "UI feedback 100–300ms; narrative ≤700ms",
            "Honor prefers-reduced-motion every time",
            "Nothing loops forever for decoration",
            "Interruptible; never block input >800ms",
        ],
        "panels": panels,
        "panel_count": 6,
    }
