/* Design Motion Studio UI */
const $ = (id) => document.getElementById(id);

function toast(msg) {
  const el = $("toast");
  el.textContent = msg;
  el.hidden = false;
  clearTimeout(toast._t);
  toast._t = setTimeout(() => { el.hidden = true; }, 2200);
}

async function api(path, opts) {
  const res = await fetch(path, opts);
  if (!res.ok) throw new Error(`${path} HTTP ${res.status}`);
  return res.json();
}

function renderSystem(system) {
  if (!system) return;
  const p = system.palette;
  const t = system.typography;
  $("system").innerHTML = `
    <p><strong>${p.label}</strong> — ${p.why}</p>
    <p class="muted">Type: ${t.display} / ${t.body} · Pattern: ${system.pattern.name}</p>
    <ul>${system.anti_patterns.map((a) => `<li>${a}</li>`).join("")}</ul>
    <pre class="token">${system.token_snippet.replace(/</g, "&lt;")}</pre>
  `;
  $("palette-swatches").innerHTML = ["surface", "elevated", "ink", "accent", "accent_2", "line"]
    .map((k) => `<div class="swatch" title="${k}" style="background:${p[k]}"></div>`)
    .join("");
}

function renderFails(checklist) {
  const fails = checklist.fails || [];
  if (!fails.length) {
    $("fails").innerHTML = `<p class="muted">No automated fails. Grade ${checklist.summary.grade}.</p>`;
    return;
  }
  $("fails").innerHTML = fails.map((f) => `
    <div class="fail">
      <b>${f.severity}</b> <code>${f.rule_id}</code> — ${f.name}<br/>
      ${f.detail}<br/><span class="muted">Fix: ${f.fix}</span>
    </div>
  `).join("");
}

function renderStoryboard(sb) {
  $("storyboard").innerHTML = (sb.panels || []).map((p) => `
    <div class="frame">
      <div class="n">Panel ${p.panel}</div>
      <h3>${p.beat}</h3>
      <p>${p.intent}</p>
      <p><strong>${p.duration_ms}</strong> · ${p.properties}</p>
      <p>Reduced: ${p.reduced_motion}</p>
    </div>
  `).join("");
}

function showReport(payload) {
  const report = payload.report || payload;
  const sum = report.checklist.summary;
  $("score-panel").hidden = false;
  $("score").textContent = `${sum.slop_free_score}% ${sum.grade}`;
  $("score-meta").textContent =
    `${sum.automated_pass} pass · ${sum.automated_fail} fail · ${sum.automated_review} review · catalog ${report.checklist.catalog_size}`;
  renderSystem(report.design_system);
  renderFails(report.checklist);
  renderStoryboard(report.storyboard);
}

async function generate() {
  const name = $("name").value.trim() || "Untitled";
  const brief = $("brief").value.trim();
  const source = $("source").value;
  const data = await api("/api/generate", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name, brief, source, save: true }),
  });
  showReport(data);
  toast(`Saved ${data.paths?.stem || name} · ${data.score}% ${data.grade}`);
  loadSeeds();
}

async function checkOnly() {
  const source = $("source").value;
  const data = await api("/api/check", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ source }),
  });
  $("score-panel").hidden = false;
  const sum = data.summary;
  $("score").textContent = `${sum.slop_free_score}% ${sum.grade}`;
  $("score-meta").textContent = `check-only · ${sum.automated_fail} fails`;
  renderFails(data);
  toast(`Score ${sum.slop_free_score}%`);
}

async function loadSeedReport(stem, fillForm) {
  const report = await api(`/api/report/${stem}`);
  if (fillForm) {
    $("name").value = report.project || "";
    $("brief").value = report.brief || "";
  }
  showReport({ report });
  toast(`Loaded ${stem}`);
}

async function loadSeeds() {
  const data = await api("/api/seeds");
  if (!data.seeds.length) {
    $("seeds").innerHTML = `<p class="muted">No seed reports yet — run ./run.sh</p>`;
    return;
  }
  $("seeds").innerHTML = data.seeds.map((s) => `
    <div class="card">
      <div>
        <strong>${s.project}</strong>
        <div class="muted">${s.stem}</div>
      </div>
      <div class="row">
        <span class="badge">${s.score}% ${s.grade}</span>
        <button type="button" class="btn ghost" data-stem="${s.stem}">Open</button>
      </div>
    </div>
  `).join("");
  $("seeds").querySelectorAll("button[data-stem]").forEach((btn) => {
    btn.addEventListener("click", () => loadSeedReport(btn.dataset.stem, true));
  });
}


async function loadBrief025() {
  const el = document.getElementById("brief025-live");
  if (!el) return;
  try {
    const b = await fetch("/api/brief025", { cache: "no-store" }).then((r) => r.json());
    const lc = b.live_check || {};
    const sc = b.scorecard || {};
    el.innerHTML =
      `<strong>live_check</strong> · auto_publish_demo=<code>${sc.auto_publish_demo ?? lc.auto_publish_demo}</code>` +
      ` · claim_watched_without_review=<code>${sc.claim_watched_without_review ?? lc.claim_watched_without_review}</code>` +
      ` · missing_captions=<code>${lc.missing_captions}</code>` +
      ` · live_on_synth=<code>${lc.live_label_on_synthetic}</code>` +
      ` · publish_apis=<code>${lc.auto_publish_apis_succeed}</code>` +
      ` · claim_apis=<code>${lc.claim_watched_apis_succeed}</code>` +
      ` · policy=<code>${lc.mutation_endpoints_policy}</code>` +
      ` · paired_brief010=<code>${lc.paired_with_brief010}</code>` +
      ` · ${escapeHtml(lc.served_at_et || "")}`;
  } catch (err) {
    el.textContent = "live_check unavailable";
  }
}

function escapeHtml(s) {
  return String(s)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

async function boot() {
  const h = await api("/api/health");
  $("stats").innerHTML = `
    <span class="pill">catalog <b>${h.catalog_size}</b></span>
    <span class="pill">seeds <b>${h.seed_reports}</b></span>
    <span class="pill">reports <b>${h.report_count}</b></span>
    <span class="pill">port <b>${h.port}</b></span>
  `;
  // empty storyboard scaffold
  const sb = await api("/api/storyboard", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name: "Design Motion Studio", brief: "Local anti-slop lab" }),
  });
  renderStoryboard(sb.storyboard);
  await loadSeeds();
  await loadBrief025();
}

$("btn-generate").addEventListener("click", () => generate().catch((e) => toast(String(e))));
$("btn-check").addEventListener("click", () => checkOnly().catch((e) => toast(String(e))));
$("btn-load-kids").addEventListener("click", () => loadSeedReport("seed-kids-coding-studio", true).catch((e) => toast(String(e))));
$("btn-load-list").addEventListener("click", () => loadSeedReport("seed-list-brief-pack", true).catch((e) => toast(String(e))));

boot().catch((e) => toast(String(e)));
