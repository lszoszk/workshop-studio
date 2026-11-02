I added the "Suggest SDGs with AI" card below the records table. It sends the first 50 matching records in batches of 25, then shows the UN's SDGs, the AI's SDGs and whether they agree, with the agreement rate and a data-sharing notice at the top. "Run again" re-sends the same 50 records and adds another column pair, so runs sit side by side. The page cannot see which model sits behind `studio.ask`, so the notice says that instead of naming one.

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>UN human rights recommendations dashboard</title>
<style>
  :root { --accent:#1f6fb2; --ink:#1d2733; --muted:#5b6876; --line:#d9e0e7; --bg:#f5f8fb; }
  * { box-sizing: border-box; }
  body { margin:0; background:var(--bg); color:var(--ink); font:16px/1.5 -apple-system, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; }
  .wrap { max-width:1200px; margin:0 auto; padding:28px 24px 60px; }
  h1 { margin:0 0 4px; font-size:1.8rem; color:var(--accent); }
  h2 { margin:0 0 6px; font-size:1.2rem; }
  .desc { color:var(--muted); margin:0 0 20px; }
  .card { background:#fff; border:1px solid var(--line); border-radius:8px; padding:20px; margin-bottom:20px; }
  .stats { display:grid; grid-template-columns:repeat(auto-fit,minmax(200px,1fr)); gap:16px; margin-bottom:20px; }
  .stat { background:#fff; border:1px solid var(--line); border-left:4px solid var(--accent); border-radius:8px; padding:14px 18px; }
  .stat .n { font-size:1.9rem; font-weight:600; color:var(--accent); line-height:1.2; }
  .stat .l { color:var(--muted); font-size:.9rem; }
  .filters { display:grid; grid-template-columns:repeat(auto-fit,minmax(190px,1fr)); gap:14px; align-items:end; }
  label { display:block; font-size:.85rem; font-weight:600; color:var(--muted); margin-bottom:4px; }
  select, input[type=search] { width:100%; padding:8px 10px; font-size:1rem; border:1px solid #b9c4cf; border-radius:6px; background:#fff; color:var(--ink); }
  button { font:inherit; cursor:pointer; padding:8px 14px; border-radius:6px; border:1px solid var(--accent); background:var(--accent); color:#fff; }
  button.ghost { background:#fff; color:var(--accent); }
  button:disabled { opacity:.5; cursor:not-allowed; }
  .note { font-size:.88rem; color:var(--muted); background:#eef4fa; border-radius:6px; padding:8px 12px; margin-top:12px; }
  .chartbox { position:relative; height:400px; }
  .chip { display:inline-block; background:#e3effa; color:var(--accent); border-radius:14px; padding:2px 10px; font-size:.9rem; margin:0 6px 8px 0; }
  .chip button { padding:0 4px; margin-left:4px; background:none; border:none; color:var(--accent); font-weight:700; }
  table { width:100%; border-collapse:collapse; }
  th { text-align:left; font-size:.85rem; color:var(--muted); border-bottom:2px solid var(--line); padding:8px; }
  td { padding:9px 8px; border-bottom:1px solid var(--line); vertical-align:top; }
  tr.row, tr.airow { cursor:pointer; }
  tr.row:hover td, tr.airow:hover td { background:#f1f6fb; }
  tr.row:focus, tr.airow:focus { outline:2px solid var(--accent); outline-offset:-2px; }
  td.date { white-space:nowrap; }
  a { color:var(--accent); }
  tr.full td { background:#fafcfe; padding:14px 18px; }
  .full .txt { white-space:pre-wrap; border-left:3px solid var(--accent); padding-left:12px; margin:0 0 10px; }
  .full .meta { font-size:.88rem; color:var(--muted); }
  .empty { padding:24px; text-align:center; color:var(--muted); }
  .toolbar { display:flex; justify-content:space-between; flex-wrap:wrap; gap:10px; align-items:center; margin-bottom:8px; }
  .toolbar select { width:auto; }
  /* AI section */
  .ai-notice { background:#fff6dc; border:1px solid #e0b64a; border-radius:8px; padding:12px 16px; margin:14px 0; font-size:.95rem; }
  .ai-notice ul { margin:6px 0 0; padding-left:20px; }
  [data-source="ai"] { background:#fff6dc; box-shadow:inset 0 -2px 0 #e0b64a; }
  .stat [data-source="ai"].n { display:inline-block; padding:0 8px; border-radius:4px; }
  .sdg { display:inline-block; min-width:26px; text-align:center; background:#e3effa; color:#0d4373; border-radius:5px; padding:0 6px; margin:0 4px 4px 0; font-weight:600; font-size:.9rem; }
  [data-source="ai"] .sdg { background:#ffe7a8; color:#5c4100; }
  .none { color:var(--muted); font-style:italic; font-size:.9rem; }
  .sm { font-size:.85rem; color:var(--muted); }
  .badge { font-weight:600; white-space:nowrap; }
  .b-agree { color:#1a7a3c; } .b-partial { color:#9a6700; } .b-differ { color:#b3261e; } .b-na { color:var(--muted); font-weight:400; }
  .scroll { overflow-x:auto; }
  .aitbl { font-size:.93rem; }
  .btns { display:flex; gap:10px; flex-wrap:wrap; align-items:center; margin:10px 0 4px; }
  .errs { color:#b3261e; font-size:.9rem; margin:6px 0; }
  @media (max-width:700px){ td.body, th.body { display:none; } }
</style>
</head>
<body>
<div class="wrap">
  <h1 id="title">UN human rights recommendations</h1>
  <p class="desc" id="desc"></p>

  <div class="stats">
    <div class="stat"><div class="n" id="sTotal">–</div><div class="l">records in the dataset</div></div>
    <div class="stat"><div class="n" id="sYears">–</div><div class="l">years covered (earliest to latest)</div></div>
    <div class="stat"><div class="n" id="sMatch">–</div><div class="l">records matching current filters</div></div>
  </div>

  <div class="card">
    <h2>Filters</h2>
    <div class="filters">
      <div><label for="fMech">Mechanism</label><select id="fMech"></select></div>
      <div><label for="fBody">Treaty body or mandate</label><select id="fBody"></select></div>
      <div><label for="fFrom">Year from</label><select id="fFrom"></select></div>
      <div><label for="fTo">Year to</label><select id="fTo"></select></div>
      <div><label for="fSdg">SDG</label><select id="fSdg"></select></div>
      <div><label for="fQ">Keyword search</label><input type="search" id="fQ" placeholder="e.g. detention, land, refugees"></div>
      <div><button class="ghost" id="reset" type="button">Reset all filters</button></div>
    </div>
    <div class="note">How this is computed: a record is kept only if it passes every filter at once. Keyword search is not case-sensitive; with several words, each word must appear somewhere in the paragraph text, symbol, body or theme names. The list of treaty bodies/mandates follows the mechanism you choose.</div>
  </div>

  <div class="card">
    <h2>Ten most frequent themes in the current selection</h2>
    <div id="chips"></div>
    <div class="chartbox"><canvas id="chart"></canvas></div>
    <div id="chartMsg" class="empty" style="display:none"></div>
    <div class="note" id="chartNote"></div>
  </div>

  <div class="card">
    <div class="toolbar">
      <h2 id="tblTitle">Matching records</h2>
      <div><label for="fSort" style="display:inline;margin-right:6px">Sort</label>
        <select id="fSort"><option value="desc">Newest first</option><option value="asc">Oldest first</option></select></div>
    </div>
    <div id="tblWrap"></div>
    <div style="text-align:center;margin-top:12px"><button id="more" type="button" style="display:none">Show more</button></div>
    <div class="note">How this is computed: the table lists exactly the records that pass the filters above. "First line" is the opening of the paragraph (about 160 characters). Click a row to show the full, unaltered text and its tags; click the symbol to open the UN document in a new tab.</div>
  </div>

  <div class="card" id="aiCard">
    <h2>Suggest SDGs with AI (experimental)</h2>
    <p class="desc" style="margin-bottom:6px">Compare the SDG tags already in the dataset ("the UN's SDGs") with SDGs suggested by a language model for the first 50 records of the current filter.</p>
    <div class="btns">
      <button id="aiRun" type="button">Suggest SDGs with AI</button>
      <button id="aiAgain" type="button" class="ghost" style="display:none">Run again</button>
      <button id="aiStop" type="button" class="ghost" style="display:none">Stop</button>
      <span id="aiStatus" class="sm" aria-live="polite"></span>
    </div>
    <div class="sm" id="aiHint"></div>
    <div id="aiOut"></div>
    <div class="note">How this is computed: <strong>the UN's SDGs</strong> are the <code>sdgs</code> tags stored with each record; they are not sent to the model. <strong>The AI's SDGs</strong> come from the model reading only the paragraph text (long texts are cut at 1,500 characters). Our code then compares the two lists: <strong>Agree</strong> = exactly the same set of SDG numbers (two empty lists also agree); <strong>Partly</strong> = at least one SDG in common but not identical; <strong>Differ</strong> = nothing in common. The agreement rate = Agree ÷ records that received an AI answer. Agreement is not accuracy: neither list is a verified "right answer". "Run again" re-sends the same records, so differences between runs show how unstable the model's answers are. "Suggest SDGs with AI" always starts a fresh set and discards earlier runs.</div>
  </div>
</div>

<script>
(function(){
  const D = (window.WORKSHOP_DATA && window.WORKSHOP_DATA.uhri) || {};
  const recs = Array.isArray(D.records) ? D.records : [];
  const sdgNames = D.sdg_names || {};
  const $ = id => document.getElementById(id);
  const esc = s => String(s == null ? "" : s).replace(/[&<>"']/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
  const arr = x => Array.isArray(x) ? x : [];
  const PAGE = 100;

  const country = D.country || "the country";
  const years = recs.map(r => r.year).filter(y => Number.isFinite(y));
  const minY = years.length ? Math.min(...years) : null;
  const maxY = years.length ? Math.max(...years) : null;

  $("title").textContent = "UN human rights recommendations and observations: " + country;
  document.title = $("title").textContent;
  let d = (D.title ? D.title + ". " : "") + "Source: " + (D.source || "UHRI / OHCHR") + ". " + recs.length + " paragraphs";
  if (minY !== null) d += ", " + minY + "–" + maxY;
  d += D.built ? ". Dataset built " + D.built + "." : ".";
  $("desc").textContent = d;
  $("sTotal").textContent = recs.length.toLocaleString();
  $("sYears").textContent = minY === null ? "–" : (minY === maxY ? String(minY) : minY + "–" + maxY);

  const state = { mech:"", body:"", from:minY, to:maxY, sdg:"", q:"", theme:"", sort:"desc", limit:PAGE };
  const expanded = new Set();
  let chart = null;
  let current = [];

  // ---------- build static selects
  function fillSelect(sel, items, value){
    sel.innerHTML = items.map(i => '<option value="'+esc(i.v)+'">'+esc(i.l)+'</option>').join("");
    sel.value = value;
    if (sel.value !== value) sel.value = items.length ? items[0].v : "";
  }
  function countBy(list, fn){ const m = {}; list.forEach(r => { const k = fn(r); if (k) m[k] = (m[k]||0)+1; }); return m; }

  const mechCounts = countBy(recs, r => r.mechanism);
  fillSelect($("fMech"), [{v:"",l:"All mechanisms ("+recs.length+")"}].concat(
    Object.keys(mechCounts).sort().map(k => ({v:k,l:k+" ("+mechCounts[k]+")"}))), "");

  function fillBodies(){
    const base = recs.filter(r => !state.mech || r.mechanism === state.mech);
    const c = countBy(base, r => r.body);
    const items = [{v:"",l:"All ("+base.length+")"}].concat(Object.keys(c).sort().map(k => ({v:k,l:k+" ("+c[k]+")"})));
    if (state.body && !c[state.body]) state.body = "";
    fillSelect($("fBody"), items, state.body);
  }

  const uniqYears = Array.from(new Set(years)).sort((a,b)=>a-b);
  const yItems = uniqYears.map(y => ({v:String(y), l:String(y)}));
  fillSelect($("fFrom"), yItems, minY === null ? "" : String(minY));
  fillSelect($("fTo"), yItems, maxY === null ? "" : String(maxY));

  const sdgCount = {};
  recs.forEach(r => arr(r.sdgs).forEach(g => { sdgCount[g] = (sdgCount[g]||0)+1; }));
  fillSelect($("fSdg"), [{v:"",l:"All SDGs / none"}].concat(
    Object.keys(sdgCount).sort((a,b)=>a-b).map(g => ({v:g, l:"SDG "+g+(sdgNames[g]?" – "+sdgNames[g]:"")+" ("+sdgCount[g]+")"}))), "");

  // ---------- filtering
  function haystack(r){
    if (r._h) return r._h;
    r._h = [r.text, r.symbol, r.body, arr(r.themes).join(" ")].join(" ").toLowerCase();
    return r._h;
  }
  function apply(){
    let lo = state.from, hi = state.to;
    if (lo !== null && hi !== null && lo > hi) { const t = lo; lo = hi; hi = t; }
    const words = state.q.toLowerCase().split(/\s+/).filter(Boolean);
    current = recs.filter(r => {
      if (state.mech && r.mechanism !== state.mech) return false;
      if (state.body && r.body !== state.body) return false;
      if (lo !== null && Number.isFinite(r.year) && r.year < lo) return false;
      if (hi !== null && Number.isFinite(r.year) && r.year > hi) return false;
      if ((lo !== null || hi !== null) && !Number.isFinite(r.year)) return false;
      if (state.sdg && !arr(r.sdgs).map(String).includes(state.sdg)) return false;
      if (state.theme && !arr(r.themes).includes(state.theme)) return false;
      if (words.length) { const h = haystack(r); for (const w of words) if (!h.includes(w)) return false; }
      return true;
    });
    current.sort((a,b) => {
      const x = a.date || "", y = b.date || "";
      return state.sort === "asc" ? x.localeCompare(y) : y.localeCompare(x);
    });
    $("sMatch").textContent = current.length.toLocaleString();
    renderChips(); renderChart(); renderTable(); updateAiHint();
  }

  function renderChips(){
    const parts = [];
    if (state.theme) parts.push('<span class="chip">Theme: '+esc(state.theme)+'<button type="button" id="clrTheme" aria-label="Remove theme filter">×</button></span>');
    $("chips").innerHTML = parts.join("");
    const b = $("clrTheme");
    if (b) b.onclick = () => { state.theme = ""; state.limit = PAGE; apply(); };
  }

  // ---------- chart
  function renderChart(){
    const c = {};
    let untagged = 0;
    current.forEach(r => {
      const t = Array.from(new Set(arr(r.themes)));
      if (!t.length) untagged++;
      t.forEach(k => { c[k] = (c[k]||0)+1; });
    });
    const top = Object.keys(c).map(k => [k,c[k]]).sort((a,b)=> b[1]-a[1] || a[0].localeCompare(b[0])).slice(0,10);
    const msg = $("chartMsg");
    const note = "How this is computed: each record can carry several themes (or none). For every theme we count how many matching records carry it, then show the 10 highest. Click a bar to filter the table to that theme.";
    $("chartNote").textContent = note + " Based on " + current.length + " matching records; " + untagged + " of them have no theme tag.";
    if (!top.length) {
      if (chart) { chart.destroy(); chart = null; }
      document.querySelector(".chartbox").style.display = "none";
      msg.style.display = "block";
      msg.textContent = current.length ? "None of the matching records carries a theme tag." : "No records match the current filters.";
      return;
    }
    msg.style.display = "none";
    document.querySelector(".chartbox").style.display = "block";
    const labels = top.map(t => t[0]), vals = top.map(t => t[1]);
    if (chart) chart.destroy();
    chart = new Chart($("chart"), {
      type: "bar",
      data: { labels, datasets: [{ label: "Records", data: vals,
        backgroundColor: labels.map(l => l === state.theme ? "#0d4373" : "#1f6fb2") }] },
      options: {
        indexAxis: "y", responsive: true, maintainAspectRatio: false, animation: false,
        plugins: { legend: { display: false },
          tooltip: { callbacks: { title: it => it[0].label, label: it => it.parsed.x + " records" } } },
        scales: {
          x: { beginAtZero: true, ticks: { precision: 0, font: { size: 13 } }, title: { display: true, text: "Number of records" } },
          y: { ticks: { font: { size: 13 }, callback: function(v){ const l = this.getLabelForValue(v); return l.length > 48 ? l.slice(0,46)+"…" : l; } } }
        },
        onClick: (e, els) => {
          if (!els.length) return;
          const t = labels[els[0].index];
          state.theme = state.theme === t ? "" : t; state.limit = PAGE; apply();
        }
      }
    });
  }

  // ---------- table
  function firstLine(t, max){
    max = max || 160;
    t = String(t || "").replace(/\s+/g," ").trim();
    if (t.length <= max) return t;
    const cut = t.slice(0,max), i = cut.lastIndexOf(" ");
    return (i > max*0.6 ? cut.slice(0,i) : cut) + "…";
  }
  function renderTable(){
    const n = current.length;
    $("tblTitle").textContent = "Matching records (" + n.toLocaleString() + " of " + recs.length.toLocaleString() + ")";
    if (!n) { $("tblWrap").innerHTML = '<div class="empty">No records match the current filters.</div>'; $("more").style.display = "none"; return; }
    const shown = current.slice(0, state.limit);
    let h = '<table><thead><tr><th>Date</th><th class="body">Body</th><th>Symbol</th><th>Text (first line)</th></tr></thead><tbody>';
    shown.forEach(r => {
      const open = expanded.has(r.id);
      const sym = r.doc_url ? '<a href="'+esc(r.doc_url)+'" target="_blank" rel="noopener">'+esc(r.symbol || "document")+'</a>' : esc(r.symbol || "");
      h += '<tr class="row" tabindex="0" data-id="'+esc(r.id)+'" aria-expanded="'+open+'">'
        + '<td class="date">'+esc(r.date || r.year || "")+'</td>'
        + '<td class="body">'+esc(r.body || "")+'</td>'
        + '<td>'+sym+'</td>'
        + '<td>'+(open ? "▾ " : "▸ ")+esc(firstLine(r.text))+'</td></tr>';
      if (open) {
        const meta = [];
        meta.push("Mechanism: " + esc(r.mechanism || "n/a") + " · Type: " + esc(r.type || "n/a") + (r.section ? " · Section: " + esc(r.section) : ""));
        if (arr(r.themes).length) meta.push("Themes: " + arr(r.themes).map(esc).join("; "));
        if (arr(r.affected_persons).length) meta.push("Affected persons: " + arr(r.affected_persons).map(esc).join("; "));
        if (arr(r.sdgs).length) meta.push("SDGs: " + arr(r.sdgs).map(g => "SDG "+esc(g)+(sdgNames[g]?" ("+esc(sdgNames[g])+")":"")).join("; "));
        h += '<tr class="full"><td colspan="4"><p class="txt">'+esc(r.text || "(no text)")+'</p><div class="meta">'+meta.join("<br>")+'</div></td></tr>';
      }
    });
    h += '</tbody></table>';
    if (shown.length < n) h += '<p class="desc" style="margin-top:10px">Showing the first '+shown.length+' of '+n+' matching records.</p>';
    $("tblWrap").innerHTML = h;
    $("more").style.display = shown.length < n ? "inline-block" : "none";
    $("more").textContent = "Show " + Math.min(PAGE, n - shown.length) + " more";
  }
  $("tblWrap").addEventListener("click", e => {
    if (e.target.closest("a")) return;
    const tr = e.target.closest("tr.row"); if (!tr) return;
    toggle(tr.dataset.id);
  });
  $("tblWrap").addEventListener("keydown", e => {
    if (e.key !== "Enter" && e.key !== " ") return;
    const tr = e.target.closest && e.target.closest("tr.row");
    if (!tr || e.target.closest("a")) return;
    e.preventDefault(); toggle(tr.dataset.id);
  });
  function toggle(id){
    if (expanded.has(id)) expanded.delete(id); else expanded.add(id);
    renderTable();
    const el = document.querySelector('tr.row[data-id="'+(window.CSS && CSS.escape ? CSS.escape(id) : id)+'"]');
    if (el) el.focus({preventScroll:true});
  }
  $("more").onclick = () => { state.limit += PAGE; renderTable(); };

  // ---------- AI SDG suggestions
  const AI_MAX = 50, BATCH = 25, TXT_CAP = 1500, MAX_RUNS = 4;
  const ai = { runs:[], recs:[], busy:false, stop:false, filterDesc:"", matchCount:0, open:new Set(), status:"" };
  const sdgList = x => Array.from(new Set(arr(x).map(Number).filter(n => n >= 1 && n <= 17))).sort((a,b)=>a-b);
  const pills = l => l.length ? l.map(n => '<span class="sdg" title="'+esc(sdgNames[n]||"")+'">'+n+'</span>').join("") : '<span class="none">none</span>';
  const LABEL = { agree:["b-agree","✔ Agree"], partial:["b-partial","◐ Partly"], differ:["b-differ","✖ Differ"], na:["b-na","– no AI answer"] };
  function compare(a, b){
    if (a.length === b.length && a.every((v,i) => v === b[i])) return "agree";
    return a.some(v => b.includes(v)) ? "partial" : "differ";
  }
  function describeFilter(){
    const p = [];
    if (state.mech) p.push("mechanism = " + state.mech);
    if (state.body) p.push("body = " + state.body);
    if (state.from !== minY || state.to !== maxY) p.push("years " + state.from + "–" + state.to);
    if (state.sdg) p.push("SDG " + state.sdg);
    if (state.theme) p.push("theme = " + state.theme);
    if (state.q) p.push("keyword “" + state.q + "”");
    return p.length ? p.join("; ") : "no filter (all records)";
  }
  function updateAiHint(){
    const n = Math.min(AI_MAX, current.length);
    $("aiHint").textContent = n
      ? "Clicking “Suggest SDGs with AI” will send the text of the first " + n + " matching paragraph" + (n === 1 ? "" : "s") + " (in the current sort order) out of your browser to an external language model, in " + Math.ceil(n / BATCH) + " batch" + (Math.ceil(n / BATCH) === 1 ? "" : "es") + ". Nothing is sent until you click."
      : "No matching records to send.";
    $("aiRun").disabled = ai.busy || !n;
  }
  function modelName(){
    try { const m = typeof studio !== "undefined" && studio && (studio.model || studio.modelName); if (m) return String(m); } catch(e){}
    return "";
  }
  function buildPrompt(batch, run){
    const goals = Object.keys(sdgNames).sort((a,b)=>a-b).map(k => k + ": " + sdgNames[k]).join("; ");
    const items = batch.map(r => {
      let t = String(r.text || "");
      if (t.length > TXT_CAP) { t = t.slice(0, TXT_CAP) + " […]"; run.truncated++; }
      return { id: r.id, text: t };
    });
    return "You are helping a human rights researcher tag paragraphs from UN human rights documents with Sustainable Development Goals (SDGs).\n"
      + "For each paragraph below, give the SDG numbers (integers from 1 to 17) that the content clearly relates to. Use an empty list if none clearly applies. Base your answer only on the paragraph text.\n"
      + (goals ? "The SDGs are: " + goals + ".\n" : "Use the standard 17 UN Sustainable Development Goals.\n")
      + "Return ONLY JSON, with one entry for every id given, no commentary, in exactly this shape:\n"
      + '{"results":[{"id":"<id exactly as given>","sdgs":[16,5]}]}\n\n'
      + "Paragraphs:\n" + JSON.stringify(items);
  }
  function cleanSdgs(v){
    if (v && !Array.isArray(v) && typeof v === "object") v = v.sdgs;
    if (v == null) return [];
    if (!Array.isArray(v)) v = String(v).match(/\d+/g) || [];
    return sdgList(v.map(x => parseInt(String(x).replace(/\D/g, ""), 10)));
  }
  function tryParse(s){
    try { return JSON.parse(s); } catch(e){}
    for (const [o,c] of [["{","}"],["[","]"]]) {
      const a = s.indexOf(o), b = s.lastIndexOf(c);
      if (a >= 0 && b > a) { try { return JSON.parse(s.slice(a, b + 1)); } catch(e){} }
    }
    return null;
  }
  function parseAnswer(raw){
    const out = new Map();
    let data = raw;
    if (typeof raw === "string") data = tryParse(raw.trim().replace(/^```(?:json)?\s*/i, "").replace(/```\s*$/, "").trim());
    if (!data || typeof data !== "object") return out;
    let list = data;
    if (!Array.isArray(data)) {
      list = Array.isArray(data.results) ? data.results : Array.isArray(data.records) ? data.records : null;
      if (!list) { Object.keys(data).forEach(k => out.set(String(k).trim(), cleanSdgs(data[k]))); return out; }
    }
    list.forEach(o => { if (o && o.id != null) out.set(String(o.id).trim(), cleanSdgs(o.sdgs != null ? o.sdgs : o.SDGs)); });
    return out;
  }

  async function runAi(fresh){
    if (ai.busy) return;
    if (typeof studio === "undefined" || !studio || typeof studio.ask !== "function") {
      ai.status = "The AI service (studio.ask) is not available in this page."; renderAi(); return;
    }
    if (fresh) {
      ai.recs = current.slice(0, AI_MAX); ai.runs = []; ai.open = new Set();
      ai.filterDesc = describeFilter(); ai.matchCount = current.length;
    }
    if (!ai.recs.length) { ai.status = "There are no records to send."; renderAi(); return; }
    const run = { answers:{}, errors:[], sent:0, truncated:0, stopped:false, batches:0 };
    ai.runs.push(run); ai.busy = true; ai.stop = false;
    const nb = Math.ceil(ai.recs.length / BATCH), runNo = ai.runs.length;
    for (let i = 0; i < ai.recs.length; i += BATCH) {
      if (ai.stop) { run.stopped = true; break; }
      const k = i / BATCH + 1, batch = ai.recs.slice(i, i + BATCH);
      ai.status = "Run " + runNo + ": batch " + k + " of " + nb + " sent (" + batch.length + " paragraphs). Waiting for the model…";
      renderAi();
      run.sent += batch.length; run.batches++;
      try {
        const raw = await studio.ask(buildPrompt(batch, run), { json: true });
        const parsed = parseAnswer(raw);
        let got = 0;
        batch.forEach(r => { if (parsed.has(String(r.id))) { run.answers[r.id] = parsed.get(String(r.id)); got++; } });
        if (got < batch.length) run.errors.push("Batch " + k + ": the model answered for " + got + " of " + batch.length + " records" + (parsed.size === 0 ? " (its reply could not be read as JSON)" : "") + ".");
      } catch (e) {
        run.errors.push("Batch " + k + " failed: " + ((e && e.message) || e));
      }
      renderAi();
    }
    ai.busy = false;
    ai.status = run.stopped ? "Run " + runNo + " stopped; records not yet sent have no AI answer." : "Run " + runNo + " finished.";
    updateAiHint(); renderAi();
  }

  function runStats(run){
    const s = { agree:0, partial:0, differ:0, na:0 };
    ai.recs.forEach(r => {
      const a = run.answers[r.id];
      if (a === undefined) s.na++; else s[compare(sdgList(r.sdgs), a)]++;
    });
    s.answered = ai.recs.length - s.na;
    s.rate = s.answered ? Math.round(100 * s.agree / s.answered) : null;
    return s;
  }
  function consistency(run, first){
    let both = 0, same = 0;
    ai.recs.forEach(r => {
      const a = first.answers[r.id], b = run.answers[r.id];
      if (a !== undefined && b !== undefined) { both++; if (compare(a, b) === "agree") same++; }
    });
    return { both, same, rate: both ? Math.round(100 * same / both) : null };
  }

  function renderAi(){
    const out = $("aiOut"), has = ai.runs.length > 0;
    $("aiAgain").style.display = has ? "inline-block" : "none";
    $("aiAgain").disabled = ai.busy || !has || ai.runs.length >= MAX_RUNS;
    $("aiStop").style.display = ai.busy ? "inline-block" : "none";
    $("aiStatus").textContent = ai.status;
    if (!has) { out.innerHTML = ""; return; }

    const mdl = modelName();
    const totalSent = ai.runs.reduce((s, r) => s + r.sent, 0);
    let h = '<div class="ai-notice"><strong>Your data left this browser.</strong> The full text of '
      + ai.recs.length + ' paragraphs from ' + esc(country) + ' (the first ' + ai.recs.length + ' of ' + ai.matchCount.toLocaleString()
      + ' matching records; filter: ' + esc(ai.filterDesc) + ') was sent to an external language model through the workshop’s <code>studio.ask</code> service, in batches of up to ' + BATCH + '. '
      + 'Model: ' + (mdl ? '<strong>' + esc(mdl) + '</strong>' : '<strong>not reported to this page</strong> (ask the workshop facilitators which model is configured)') + '. '
      + '<strong>Running it again can give different answers</strong> — AI output is not deterministic. '
      + 'The UN’s SDG tags were not sent to the model.<ul>'
      + ai.runs.map((r, i) => '<li>Run ' + (i + 1) + ': ' + r.sent + ' paragraphs sent in ' + r.batches + ' batch' + (r.batches === 1 ? '' : 'es')
          + (r.stopped ? ' (stopped by you)' : '') + (r.truncated ? '; ' + r.truncated + ' long text(s) cut at ' + TXT_CAP + ' characters' : '') + '</li>').join("")
      + '</ul>Total sent in this session: ' + totalSent + ' paragraph-texts.</div>';

    // agreement rates
    h += '<div class="stats">';
    const first = ai.runs[0];
    ai.runs.forEach((run, i) => {
      const s = runStats(run);
      h += '<div class="stat"><div class="n" data-source="ai">' + (s.rate === null ? "–" : s.rate + "%") + '</div><div class="l"><strong>Run ' + (i + 1) + ': agreement with the UN’s SDGs</strong> — identical SDG sets for '
        + s.agree + ' of ' + s.answered + ' answered records. Partly overlapping: ' + s.partial + ' · No overlap: ' + s.differ + ' · No AI answer: ' + s.na + '.</div></div>';
      if (i > 0) {
        const c = consistency(run, first);
        h += '<div class="stat"><div class="n" data-source="ai">' + (c.rate === null ? "–" : c.rate + "%") + '</div><div class="l"><strong>Run ' + (i + 1) + ' vs Run 1: same answer</strong> for ' + c.same + ' of ' + c.both + ' records answered in both runs.</div></div>';
      }
    });
    h += '</div>';
    const errs = ai.runs.flatMap((r, i) => r.errors.map(e => "Run " + (i + 1) + " – " + e));
    if (errs.length) h += '<div class="errs">' + errs.map(esc).join("<br>") + '</div>';

    // comparison table
    const cols = 2 + 2 * ai.runs.length;
    h += '<div class="scroll"><table class="aitbl"><thead><tr><th>Record</th><th>UN’s SDGs</th>';
    ai.runs.forEach((_, i) => { h += '<th>AI’s SDGs (run ' + (i + 1) + ')</th><th>Agree? (run ' + (i + 1) + ')</th>'; });
    h += '</tr></thead><tbody>';
    ai.recs.forEach(r => {
      const open = ai.open.has(r.id), un = sdgList(r.sdgs);
      const sym = r.doc_url ? '<a href="' + esc(r.doc_url) + '" target="_blank" rel="noopener">' + esc(r.symbol || "document") + '</a>' : esc(r.symbol || "");
      h += '<tr class="airow" tabindex="0" data-id="' + esc(r.id) + '" aria-expanded="' + open + '"><td>' + sym
        + '<div class="sm">' + esc(r.date || r.year || "") + ' · ' + esc(r.body || "") + '</div>'
        + '<div class="sm">' + (open ? "▾ " : "▸ ") + esc(firstLine(r.text, 110)) + '</div></td><td>' + pills(un) + '</td>';
      ai.runs.forEach(run => {
        const a = run.answers[r.id];
        const cmp = a === undefined ? "na" : compare(un, a);
        h += '<td data-source="ai">' + (a === undefined ? '<span class="none">–</span>' : pills(a)) + '</td>'
          + '<td><span class="badge ' + LABEL[cmp][0] + '">' + LABEL[cmp][1] + '</span></td>';
      });
      h += '</tr>';
      if (open) h += '<tr class="full"><td colspan="' + cols + '"><p class="txt">' + esc(r.text || "(no text)") + '</p></td></tr>';
    });
    h += '</tbody></table></div><div class="sm" style="margin-top:8px">Shaded cells with amber SDG numbers are AI output. Click a row to read the full paragraph; hover an SDG number to see its name.</div>';
    out.innerHTML = h;
  }
  $("aiOut").addEventListener("click", e => {
    if (e.target.closest("a")) return;
    const tr = e.target.closest("tr.airow"); if (!tr) return;
    const id = tr.dataset.id;
    if (ai.open.has(id)) ai.open.delete(id); else ai.open.add(id);
    renderAi();
  });
  $("aiOut").addEventListener("keydown", e => {
    if (e.key !== "Enter" && e.key !== " ") return;
    const tr = e.target.closest && e.target.closest("tr.airow");
    if (!tr || e.target.closest("a")) return;
    e.preventDefault();
    const id = tr.dataset.id;
    if (ai.open.has(id)) ai.open.delete(id); else ai.open.add(id);
    renderAi();
  });
  $("aiRun").onclick = () => runAi(true);
  $("aiAgain").onclick = () => runAi(false);
  $("aiStop").onclick = () => { ai.stop = true; ai.status = "Stopping after the current batch finishes…"; renderAi(); };

  // ---------- events
  function changed(){ state.limit = PAGE; apply(); }
  $("fMech").onchange = e => { state.mech = e.target.value; fillBodies(); changed(); };
  $("fBody").onchange = e => { state.body = e.target.value; changed(); };
  $("fFrom").onchange = e => { state.from = e.target.value === "" ? null : +e.target.value; changed(); };
  $("fTo").onchange = e => { state.to = e.target.value === "" ? null : +e.target.value; changed(); };
  $("fSdg").onchange = e => { state.sdg = e.target.value; changed(); };
  $("fSort").onchange = e => { state.sort = e.target.value; changed(); };
  let timer = null;
  $("fQ").oninput = e => { clearTimeout(timer); const v = e.target.value; timer = setTimeout(() => { state.q = v; changed(); }, 200); };
  $("reset").onclick = () => {
    Object.assign(state, { mech:"", body:"", from:minY, to:maxY, sdg:"", q:"", theme:"", limit:PAGE });
    $("fMech").value = ""; fillBodies();
    $("fFrom").value = minY === null ? "" : String(minY);
    $("fTo").value = maxY === null ? "" : String(maxY);
    $("fSdg").value = ""; $("fQ").value = "";
    apply();
  };

  if (!recs.length) {
    $("desc").textContent = "No records were found in the dataset (WORKSHOP_DATA.uhri is empty).";
  }
  fillBodies();
  apply();
  renderAi();
})();
</script>
</body>
</html>
```