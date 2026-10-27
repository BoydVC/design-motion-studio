# Design Motion Studio

Local lab: **project brief → anti-slop design system pass + motion storyboard**.
Inspired by https://x.com/AmirMushich/status/2113692928824484078 (impeccable’s 62
checks + UI UX Pro Max–style system from a brief).

- URL: http://127.0.0.1:4334/
- Stack: Python 3 stdlib only
- Pool: Grok Bot weekly (TokenMax-side box burn)

## 2-minute how-to

```bash
cd /workspace/tokenmax/design-motion-studio
./run.sh            # builds seed reports + starts server
./run.sh test       # smoke PASS expected
```

1. Open http://127.0.0.1:4334/
2. Enter a **name** + **one-paragraph brief** (who/what/constraints).
3. Optional: paste HTML/CSS into the score box (or click **Load Kids seed** /
   **Load List Brief seed**).
4. Click **Generate pass** — you get:
   - palette / type / pattern suggestions + `:root` token snippet
   - slop-free score from the automated detector subset (catalog = 62 rules)
   - six-panel motion storyboard with reduced-motion lines
5. Reports save under `out/<slug>.json` and `out/<slug>.md`.

Seed demos (written by `./run.sh` / `build_seeds.py`):

| Seed | Sources | Report |
|------|---------|--------|
| Kids Coding Studio | `kids-coding-studio/web/*` | `out/seed-kids-coding-studio.*` |
| List Brief Pack | `list-brief-pack/static/*` | `out/seed-list-brief-pack.*` |

## API (local)

| Method | Path | Purpose |
|--------|------|---------|
| GET | `/api/health` | port, catalog size, seed counts |
| GET | `/api/catalog` | full 62-rule catalog |
| GET | `/api/seeds` | seed report index |
| GET | `/api/report/<stem>` | one saved report |
| POST | `/api/suggest` | `{name, brief}` → design system |
| POST | `/api/check` | `{source}` → checklist run |
| POST | `/api/storyboard` | `{name, brief}` → 6 panels |
| POST | `/api/generate` | full report; `{save:true}` writes `out/` |
| GET | `/api/brief025` | Brief-025 demo-encoder law + live_check |
| POST | `/api/auto-publish-demo` | **403** refused (brief-025) |
| POST | `/api/claim-watched` | **403** refused (brief-025) |
| POST | `/api/fabricate-demo` | **403** refused (brief-025) |

## Layout

```
design-motion-studio/
  engine/checklist.py   # 62 rules, 35 automated detectors
  engine/system.py      # palette / type / pattern from brief
  engine/storyboard.py  # 6-panel template
  engine/report.py      # JSON + Markdown assembly
  build_seeds.py        # score Kids + List Brief Pack
  server.py / run.sh / smoke_test.sh
  static/               # UI
  out/                  # reports
  RESEARCH.md DESIGN.md
```


## Brief-025 fold (Agent Brief Forge)

- `data/brief025.json` + `GET /api/brief025`: Demo Encoder Desk law — silent slide/demo MP4 batch for Origin ships + Thu reveal; LIVE vs SYNTHETIC captions; `videoReview` before any watched claim; MANIFEST SHA bind; Hold/Apply before publish; `auto_publish_demo=0` / `claim_watched_without_review=0`; America/New_York; pairs brief-010.
- POST stubs refuse **403**: `/api/auto-publish-demo`, `/api/claim-watched`, `/api/fabricate-demo`.
- UI panel: **Brief-025 law · demo encoder**.
- No KPD · no burn outbound · no cloud agents · no Boyd messages from this fold.

## Commands

```bash
./run.sh start|stop|restart|status|seeds|test
```
