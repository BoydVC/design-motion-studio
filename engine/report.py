"""Assemble and persist Design Motion Studio reports."""
from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

from .checklist import run_checks
from .storyboard import build_storyboard
from .system import suggest_system

TZ = ZoneInfo("America/New_York")
ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "out"


def _slug(s: str) -> str:
    s = re.sub(r"[^a-zA-Z0-9]+", "-", (s or "project").strip().lower()).strip("-")
    return s[:64] or "project"


def _now() -> str:
    return datetime.now(TZ).strftime("%Y-%m-%d %H:%M:%S %Z")


def build_report(
    name: str,
    brief: str,
    source: str = "",
    *,
    source_label: str = "pasted",
) -> dict[str, Any]:
    system = suggest_system(name, brief)
    checks = run_checks(source) if source.strip() else run_checks("")
    storyboard = build_storyboard(name, brief)
    report = {
        "generated_at": _now(),
        "project": name,
        "brief": brief,
        "source_label": source_label,
        "source_chars": len(source or ""),
        "design_system": system,
        "checklist": checks,
        "storyboard": storyboard,
        "inspired_by": {
            "post": "https://x.com/AmirMushich/status/2113692928824484078",
            "impeccable": "https://github.com/pbakaus/impeccable",
            "ui_ux_pro_max": "https://github.com/nextlevelbuilder/ui-ux-pro-max-skill",
        },
    }
    return report


def render_markdown(report: dict[str, Any]) -> str:
    s = report["design_system"]
    c = report["checklist"]
    sum_ = c["summary"]
    sb = report["storyboard"]
    lines = [
        f"# Design Motion Studio — {report['project']}",
        "",
        f"Generated: {report['generated_at']} (America/New_York)",
        f"Source: {report['source_label']} ({report['source_chars']} chars)",
        "",
        "## Brief",
        "",
        report["brief"] or "_empty_",
        "",
        "## Slop-Free Score",
        "",
        f"**{sum_['slop_free_score']}% ({sum_['grade']})** — "
        f"automated {sum_['automated_pass']} pass / {sum_['automated_fail']} fail / "
        f"{sum_['automated_review']} review of {sum_['automated_total']} detectors "
        f"(catalog {c['catalog_size']} rules).",
        "",
        f"Formula: `{sum_['formula']}`",
        "",
        "## Design system suggestions",
        "",
        f"- **Palette:** {s['palette']['label']} (`{s['palette']['preset_id']}`) — {s['palette']['why']}",
        f"- **Accent:** `{s['palette']['accent']}` / secondary `{s['palette']['accent_2']}`",
        f"- **Type:** {s['typography']['display']} / {s['typography']['body']} / {s['typography']['mono']}",
        f"- **Scale:** {' · '.join(s['typography']['scale'])}",
        f"- **Pattern:** {s['pattern']['name']} — {s['pattern']['when']}",
        "",
        "### Token snippet",
        "",
        "```css",
        s["token_snippet"],
        "```",
        "",
        "### Anti-patterns to ban",
        "",
    ]
    for a in s["anti_patterns"]:
        lines.append(f"- {a}")
    lines += ["", "## Automated fails", ""]
    fails = c.get("fails") or []
    if not fails:
        lines.append("_No automated fails._")
    else:
        for f in fails:
            lines.append(
                f"- **{f['severity'].upper()}** `{f['rule_id']}` — {f['name']}: {f['detail']} "
                f"_Fix:_ {f['fix']}"
            )
    lines += ["", "## Review queue", ""]
    revs = c.get("reviews") or []
    if not revs:
        lines.append("_No review-flagged items._")
    else:
        for f in revs:
            lines.append(f"- `{f['rule_id']}` — {f['detail']}")
    lines += ["", "## Six-panel motion storyboard", "", f"Concept: {sb['concept']}", ""]
    for p in sb["panels"]:
        lines += [
            f"### Panel {p['panel']} — {p['beat']}",
            f"- **Intent:** {p['intent']}",
            f"- **Action:** {p['primary_action']}",
            f"- **Timing:** {p['duration_ms']} · {p['easing']}",
            f"- **Props:** {p['properties']}",
            f"- **Reduced motion:** {p['reduced_motion']}",
            f"- **Note:** {p['note']}",
            "",
        ]
    lines += [
        "## Category scorecard",
        "",
        "| Category | pass | fail | review | skip |",
        "|---|---:|---:|---:|---:|",
    ]
    for cat, b in sorted(c["by_category"].items()):
        lines.append(
            f"| {cat} | {b.get('pass',0)} | {b.get('fail',0)} | {b.get('review',0)} | {b.get('skip',0)} |"
        )
    lines += [
        "",
        "## Inspired by",
        "",
        f"- {report['inspired_by']['post']}",
        f"- {report['inspired_by']['impeccable']}",
        f"- {report['inspired_by']['ui_ux_pro_max']}",
        "",
    ]
    return "\n".join(lines)


def save_report(report: dict[str, Any], stem: str | None = None) -> dict[str, str]:
    OUT.mkdir(parents=True, exist_ok=True)
    stem = _slug(stem or report["project"])
    json_path = OUT / f"{stem}.json"
    md_path = OUT / f"{stem}.md"
    tmp_j = json_path.with_suffix(".json.tmp")
    tmp_m = md_path.with_suffix(".md.tmp")
    tmp_j.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    tmp_j.replace(json_path)
    tmp_m.write_text(render_markdown(report), encoding="utf-8")
    tmp_m.replace(md_path)
    return {"json": str(json_path), "md": str(md_path), "stem": stem}
