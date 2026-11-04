#!/usr/bin/env python3
"""Score Kids Coding Studio + List Brief Pack static HTML against the checklist."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from engine.report import build_report, save_report

SEEDS = [
    {
        "stem": "seed-kids-coding-studio",
        "name": "Kids Coding Studio",
        "brief": (
            "Local creative studio for Alex (~13) and Sam (~11): age-safe project briefs, "
            "block lanes, parent overview, AI helper default off. Port 4331. Needs a warm "
            "playful system that does not look like purple neon SaaS slop."
        ),
        "paths": [
            Path("/workspace/tokenmax/kids-coding-studio/web/index.html"),
            Path("/workspace/tokenmax/kids-coding-studio/web/app.css"),
            Path("/workspace/tokenmax/kids-coding-studio/web/app.js"),
        ],
    },
    {
        "stem": "seed-list-brief-pack",
        "name": "List Brief Pack",
        "brief": (
            "X Lists → daily digest + Roemmele-style marketplace templates. Local desk on "
            "4332 with synthetic digests and a live sample. Ops reading UI: clear hierarchy, "
            "urgency badges, copyable prompts — anti-slop for dense tool chrome."
        ),
        "paths": [
            Path("/workspace/tokenmax/list-brief-pack/static/index.html"),
            Path("/workspace/tokenmax/list-brief-pack/static/styles.css"),
            Path("/workspace/tokenmax/list-brief-pack/static/app.js"),
        ],
    },
]


def load_source(paths: list[Path]) -> str:
    chunks = []
    for p in paths:
        if not p.is_file():
            raise FileNotFoundError(p)
        chunks.append(f"\n/* ===== {p} ===== */\n")
        chunks.append(p.read_text(encoding="utf-8"))
    return "".join(chunks)


def main() -> int:
    wrote = []
    for seed in SEEDS:
        src = load_source(seed["paths"])
        # also stash a combined seed file for the UI
        seed_path = ROOT / "seeds" / f"{seed['stem']}.html"
        seed_path.parent.mkdir(parents=True, exist_ok=True)
        seed_path.write_text(src, encoding="utf-8")
        report = build_report(
            seed["name"],
            seed["brief"],
            src,
            source_label=", ".join(str(p) for p in seed["paths"]),
        )
        paths = save_report(report, stem=seed["stem"])
        s = report["checklist"]["summary"]
        print(
            f"{seed['stem']}: score={s['slop_free_score']}% grade={s['grade']} "
            f"auto_fail={s['automated_fail']} -> {paths['md']}"
        )
        wrote.append(paths)
    print(f"seed_reports={len(wrote)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
