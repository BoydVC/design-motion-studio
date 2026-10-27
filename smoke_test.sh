#!/usr/bin/env bash
# Smoke: health, catalog 62, two seed reports, generate API, RESEARCH ≥120
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
BASE="${BASE_URL:-http://127.0.0.1:4334}"
FAIL=0
PASS=0

ok() { echo "OK  $*"; PASS=$((PASS+1)); }
bad() { echo "FAIL $*"; FAIL=$((FAIL+1)); }

echo "== Design Motion Studio smoke =="

need_file() {
  local f="$1"
  if [[ -f "$ROOT/$f" ]]; then ok "file $f"; else bad "missing $f"; fi
}

need_file "README.md"
need_file "DESIGN.md"
need_file "RESEARCH.md"
need_file "server.py"
need_file "engine/checklist.py"
need_file "out/seed-kids-coding-studio.json"
need_file "out/seed-kids-coding-studio.md"
need_file "out/seed-list-brief-pack.json"
need_file "out/seed-list-brief-pack.md"

if [[ -f "$ROOT/RESEARCH.md" ]]; then
  lines=$(wc -l < "$ROOT/RESEARCH.md" | tr -d ' ')
  echo "RESEARCH.md lines=$lines"
  if [[ "$lines" -ge 120 ]]; then ok "RESEARCH.md ≥120"; else bad "RESEARCH.md lines=$lines (<120)"; fi
fi

# catalog size in engine
python3 - <<'PY' && ok "catalog 62 + detectors≥20" || bad "catalog/detectors"
import sys
sys.path.insert(0, ".")
from engine.checklist import CATALOG, DETECTORS
assert len(CATALOG) == 62, len(CATALOG)
assert len(DETECTORS) >= 20, len(DETECTORS)
print(f"catalog={len(CATALOG)} detectors={len(DETECTORS)}")
PY

health=$(curl -s -o /tmp/dms-health.json -w "%{http_code}" "$BASE/api/health" || echo "000")
[[ "$health" == "200" ]] && ok "health $(cat /tmp/dms-health.json)" || bad "health HTTP $health"

home=$(curl -s -o /dev/null -w "%{http_code}" "$BASE/" || echo "000")
[[ "$home" == "200" ]] && ok "home" || bad "home HTTP $home"

for ep in /api/catalog /api/seeds; do
  code=$(curl -s -o /tmp/dms-ep.json -w "%{http_code}" "$BASE$ep" || echo "000")
  [[ "$code" == "200" ]] && ok "$ep" || bad "$ep HTTP $code"
done

python3 - <<'PY' && ok "seeds API count≥2" || bad "seeds API"
import json
d=json.load(open("/tmp/dms-ep.json",encoding="utf-8"))
assert d["count"] >= 2, d
print("seeds", d["count"], [s["stem"] for s in d["seeds"]])
PY

# seed scores substantive
python3 - <<'PY' && ok "seed reports substantive" || bad "seed reports thin"
import json
from pathlib import Path
root = Path(".")
for stem in ("seed-kids-coding-studio", "seed-list-brief-pack"):
    d = json.loads((root/"out"/f"{stem}.json").read_text(encoding="utf-8"))
    assert d["checklist"]["catalog_size"] == 62
    assert d["checklist"]["automated_rules"] >= 20
    assert d["storyboard"]["panel_count"] == 6
    assert d["design_system"]["palette"]["accent"]
    md = (root/"out"/f"{stem}.md").read_text(encoding="utf-8")
    assert len(md.splitlines()) >= 40, stem
    print(stem, d["checklist"]["summary"]["slop_free_score"], d["checklist"]["summary"]["grade"])
PY

# live generate
api=$(curl -s -o /tmp/dms-gen.json -w "%{http_code}" \
  -H 'Content-Type: application/json' \
  -d '{"name":"Smoke Lab","brief":"A short anti-slop lab for TokenMax burn night.","source":"<html lang=\"en\"><head><meta name=\"viewport\" content=\"width=device-width\"><style>:root{--bg:#fff;--ink:#111;--accent:#c45c26} body{font-family:IBM Plex Sans,system-ui;max-width:60rem} button:hover{opacity:.9} button:focus-visible{outline:2px solid #c45c26}</style></head><body><main><h1>Smoke</h1><button>Go</button></main></body></html>","save":true,"stem":"smoke-lab"}' \
  "$BASE/api/generate" || echo "000")
if [[ "$api" == "200" ]]; then
  python3 - <<'PY' && ok "POST /api/generate" || bad "generate payload"
import json
d=json.load(open("/tmp/dms-gen.json",encoding="utf-8"))
assert d.get("ok"), d
assert d["report"]["storyboard"]["panel_count"]==6
assert "paths" in d and d["paths"].get("md")
print("score", d["score"], d["grade"], d["paths"]["stem"])
PY
else
  bad "POST /api/generate HTTP $api"
fi


# brief-025: Demo Encoder Desk fold
need_file "data/brief025.json"

if rg -q "Brief-025 law · demo encoder" "$ROOT/static/index.html"; then ok "UI Brief-025 law panel"
else bad "UI missing Brief-025 law panel"; fi

code=$(curl -s -o /tmp/dms-b25.json -w "%{http_code}" "$BASE/api/brief025" || echo "000")
if [[ "$code" == "200" ]]; then ok "GET /api/brief025 $code"; else bad "GET /api/brief025 HTTP $code"; fi

if python3 << 'PYB25'
import json
b=json.load(open("/tmp/dms-b25.json"))
assert b.get("brief_id")=="brief-025"
assert b["scorecard"]["auto_publish_demo"]==0
assert b["scorecard"]["claim_watched_without_review"]==0
assert b["scorecard"]["live_label_on_synthetic"]==0
assert b["scorecard"]["missing_captions"]==0
assert b["scorecard"]["manifest_sha_mismatch"]==0
assert b["scorecard"]["burn_outbound"]==0
assert b["scorecard"]["kpd_bleed"]==0
assert b["scorecard"]["timezone"]=="America/New_York"
assert b["auto_publish_demo"]["value"]==0
assert b["claim_watched_without_review"]["value"]==0
assert "/api/auto-publish-demo" in b["refused_post_prefixes"]
assert "/api/claim-watched" in b["refused_post_prefixes"]
assert "/api/fabricate-demo" in b["refused_post_prefixes"]
assert "video_review" in b
assert "honesty_captions" in b
assert "desk" in b
lc=b["live_check"]
assert lc["auto_publish_demo"]==0
assert lc["claim_watched_without_review"]==0
assert lc["auto_publish_apis_succeed"] is False
assert lc["claim_watched_apis_succeed"] is False
assert lc["fabricate_demo_apis_succeed"] is False
assert lc["mutation_endpoints_policy"]=="403"
assert lc["video_review_required"] is True
assert lc["paired_with_brief010"] is True
assert lc["timezone"]=="America/New_York"
assert "SYNTHETIC" in lc["honesty_stamps"]
h=json.load(open("/tmp/dms-health.json"))
assert "brief-025" in h.get("briefs_folded", [])
print("brief025_ok", lc.get("served_at_et"))
PYB25
then ok "brief-025 law + live_check"
else bad "brief025 law + live_check"
fi

for deny in /api/auto-publish-demo /api/claim-watched /api/fabricate-demo; do
  post_code=$(curl -s -o /tmp/dms-post-demo.json -w "%{http_code}" -X POST -H 'Content-Type: application/json' -d '{"force":true}' "$BASE$deny" || echo "000")
  if [[ "$post_code" == "403" ]]; then ok "POST $deny → 403"
  else bad "POST $deny unexpectedly HTTP $post_code"; fi
done
if rg -qi "brief-025|refused|demo encoder|auto_publish_demo|claim_watched" /tmp/dms-post-demo.json; then ok "POST body cites brief-025 refuse"
else bad "403 without brief-025 refuse message"; fi

if rg -q 'brief-025|Brief-025|demo encoder' "$ROOT/README.md"; then ok "README brief-025 fold note"
else bad "README missing brief-025 fold note"; fi

echo "-- $PASS passed, $FAIL failed --"
if [[ "$FAIL" -eq 0 ]]; then
  echo "SMOKE PASS"
  exit 0
fi
echo "SMOKE FAIL"
exit 1
