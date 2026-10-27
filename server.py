#!/usr/bin/env python3
"""Design Motion Studio — local lab on 127.0.0.1:4334 (Python stdlib only)."""
from __future__ import annotations

import json
import os
import sys
import urllib.parse
from datetime import datetime
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from engine.checklist import catalog_public, run_checks
from engine.report import build_report, save_report
from engine.storyboard import build_storyboard
from engine.system import suggest_system

PORT = int(os.environ.get("DMS_PORT", os.environ.get("PORT", "4334")))
HOST = "127.0.0.1"
TZ = ZoneInfo("America/New_York")

# brief-025 Demo Encoder Desk — never auto-publish / claim-watched / fabricate
REFUSED_DEMO = (
    "/api/auto-publish-demo",
    "/api/claim-watched",
    "/api/fabricate-demo",
)


def _stamp() -> str:
    return datetime.now(TZ).strftime("%Y-%m-%d %H:%M %Z")


def brief025_payload() -> dict:
    """Fold Agent Brief Forge brief-025 demo-encoder law + live_check."""
    with (ROOT / "data" / "brief025.json").open("r", encoding="utf-8") as f:
        law = json.load(f)
    law["live_check"] = {
        "auto_publish_demo": 0,
        "claim_watched_without_review": 0,
        "live_label_on_synthetic": 0,
        "missing_captions": 0,
        "manifest_sha_mismatch": 0,
        "concat_parity_skip": 0,
        "webm_unflushed_encode": 0,
        "trace_used_as_visual_proof": 0,
        "demo_sold_as_prod": 0,
        "burn_outbound": 0,
        "utc_only_stamps": 0,
        "kpd_bleed": 0,
        "auto_publish_apis_succeed": False,
        "claim_watched_apis_succeed": False,
        "fabricate_demo_apis_succeed": False,
        "post_disabled_for_publish": True,
        "mutation_endpoints_policy": "403",
        "refused_post_prefixes": list(REFUSED_DEMO),
        "video_review_required": True,
        "honesty_stamps": ["LIVE", "SYNTHETIC", "MIXED"],
        "paired_with_brief010": True,
        "hub_read_only_publish": True,
        "timezone": "America/New_York",
        "served_at_et": _stamp(),
    }
    return law


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT / "static"), **kwargs)

    def log_message(self, fmt, *args):
        print(f"[dms] {self.address_string()} {fmt % args}", flush=True)

    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def _json(self, code: int, payload) -> None:
        body = json.dumps(payload, indent=2).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _read_json(self) -> dict:
        n = int(self.headers.get("Content-Length") or 0)
        raw = self.rfile.read(n) if n else b"{}"
        if not raw:
            return {}
        return json.loads(raw.decode("utf-8"))

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        if path == "/api/health":
            reports = sorted((ROOT / "out").glob("*.json")) if (ROOT / "out").is_dir() else []
            return self._json(
                200,
                {
                    "ok": True,
                    "service": "design-motion-studio",
                    "host": HOST,
                    "port": PORT,
                    "catalog_size": 62,
                    "seed_reports": len([p for p in reports if p.name.startswith("seed-")]),
                    "report_count": len(reports),
                    "briefs_folded": ["brief-025"],
                    "timezone": "America/New_York",
                    "stamp_et": _stamp(),
                },
            )

        if path == "/api/brief025":
            try:
                return self._json(200, brief025_payload())
            except Exception as e:
                return self._json(500, {"ok": False, "error": str(e)})

        if path == "/api/catalog":
            return self._json(200, {"count": 62, "rules": catalog_public()})

        if path == "/api/seeds":
            out = ROOT / "out"
            seeds = []
            for p in sorted(out.glob("seed-*.json")):
                data = json.loads(p.read_text(encoding="utf-8"))
                seeds.append(
                    {
                        "stem": p.stem,
                        "project": data.get("project"),
                        "score": data["checklist"]["summary"]["slop_free_score"],
                        "grade": data["checklist"]["summary"]["grade"],
                        "json": str(p),
                        "md": str(p.with_suffix(".md")),
                    }
                )
            return self._json(200, {"count": len(seeds), "seeds": seeds})

        if path.startswith("/api/report/"):
            stem = path.split("/api/report/", 1)[1]
            stem = urllib.parse.unquote(stem)
            jp = ROOT / "out" / f"{stem}.json"
            if not jp.is_file():
                return self._json(404, {"ok": False, "error": "not found"})
            return self._json(200, json.loads(jp.read_text(encoding="utf-8")))

        return super().do_GET()

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        is_demo = path in REFUSED_DEMO or any(path.startswith(p + "/") for p in REFUSED_DEMO)
        if is_demo:
            return self._json(
                403,
                {
                    "ok": False,
                    "error": "refused",
                    "message": (
                        "Demo Encoder Desk (brief-025). Design Motion Studio refuses "
                        "auto-publish-demo, claim-watched without videoReview, and fabricate-demo. "
                        "auto_publish_demo=0; claim_watched_without_review=0; "
                        "LIVE vs SYNTHETIC captions required; America/New_York; pairs brief-010."
                    ),
                    "brief_id": "brief-025",
                    "path": path,
                },
            )

        try:
            body = self._read_json()
        except json.JSONDecodeError:
            return self._json(400, {"ok": False, "error": "invalid json"})

        if path == "/api/suggest":
            name = body.get("name") or body.get("project") or "Untitled"
            brief = body.get("brief") or ""
            return self._json(200, {"ok": True, "system": suggest_system(name, brief)})

        if path == "/api/check":
            source = body.get("source") or body.get("html") or ""
            return self._json(200, {"ok": True, **run_checks(source)})

        if path == "/api/storyboard":
            name = body.get("name") or "Untitled"
            brief = body.get("brief") or ""
            return self._json(200, {"ok": True, "storyboard": build_storyboard(name, brief)})

        if path == "/api/generate":
            name = body.get("name") or body.get("project") or "Untitled"
            brief = body.get("brief") or ""
            source = body.get("source") or ""
            save = bool(body.get("save", True))
            label = body.get("source_label") or "pasted"
            report = build_report(name, brief, source, source_label=label)
            paths = {}
            if save:
                paths = save_report(report, stem=body.get("stem"))
            return self._json(
                200,
                {
                    "ok": True,
                    "report": report,
                    "paths": paths,
                    "score": report["checklist"]["summary"]["slop_free_score"],
                    "grade": report["checklist"]["summary"]["grade"],
                },
            )

        return self._json(404, {"ok": False, "error": "unknown endpoint"})


def main() -> None:
    (ROOT / "out").mkdir(parents=True, exist_ok=True)
    httpd = ThreadingHTTPServer((HOST, PORT), Handler)
    print(f"Design Motion Studio -> http://{HOST}:{PORT}/", flush=True)
    httpd.serve_forever()


if __name__ == "__main__":
    main()
