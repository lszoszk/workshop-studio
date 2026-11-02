I added a "Check 10 at random" card between the chart and the table. It draws 10 records from your current filter and shows each one's full text and its UN-assigned SDGs, with Right / Wrong / Arguable buttons. Once all are marked, it shows the agreement rate, the wrong and arguable examples, and a CSV download, and "Draw again" gives a new sample.

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
  tr.row { cursor:pointer; }
  tr.row:hover td { background:#f1f6fb; }
  tr.row:focus { outline:2px solid var(--accent); outline-offset:-2px; }
  td.date { white-space:nowrap; }
  a { color:var(--accent); }
  tr.full td { background:#fafcfe; padding:14px 18px; }
  .full .txt { white-space:pre-wrap; border-left:3px solid var(--accent); padding-left:12px; margin:0 0 10px; }
  .full .meta { font-size:.88rem; color:var(--muted); }
  .empty { padding:24px; text-align:center; color:var(--muted); }
  .toolbar { display:flex; justify-content:space-between; flex-wrap:wrap; gap:10px; align-items:center; margin-bottom:8px; }
  .toolbar select { width:auto; }
  /* SDG check */
  .btnrow { display:flex; gap:10px; flex-wrap:wrap; align-items:center; margin:10px 0; }
  .aitem { border:1px solid var(--line); border-radius:8px; padding:14px 16px; margin-bottom:14px; background:#fff; }
  .aitem.done { border-left:4px solid var(--accent); }
  .ahead { display:flex; flex-wrap:wrap; gap:6px 14px; align-items:baseline; margin-bottom:8px; font-size:.95rem; }
  .ahead .k { font-weight:700; color:var(--accent); }
  .atext { white-space:pre-wrap; border-left:3px solid var(--line); padding-left:12px; margin:0 0 10px; }
  .sdgbox { background:#f1f6fb; border-radius:6px; padding:8px 12px; margin-bottom:10px; font-size:.95rem; }
  .sdgbox ul { margin:4px 0 0 18px; padding:0; color:var(--muted); font-size:.9rem; }
  .sdgchip { display:inline-block; background:var(--accent); color:#fff; border-radius:14px; padding:1px 10px; margin:0 6px 4px 0; font-size:.88rem; }
  .marks { display:flex; flex-wrap:wrap; gap:6px 18px; }
  .marks label { display:inline-flex; align-items:center; gap:6px; font-size:1rem; font-weight:600; color:var(--ink); margin:0; cursor:pointer; }
  .marks input { width:18px; height:18px; }
  .progress { font-weight:600; color:var(--muted); margin:6px 0; }
  .result { border:2px solid var(--accent); border-radius:8px; padding:16px 18px; margin-top:16px; background:#f8fbfe; }
  .rate { font-size:2.2rem; font-weight:700; color:var(--accent); line-height:1.1; }
  .ex { border-top:1px solid var(--line); padding:8px 0; }
  .tag { display:inline-block; border-radius:4px; padding:0 8px; font-size:.82rem; font-weight:700; color:#fff; margin-right:6px; }
  .tag.wrong { background:#b3372f; } .tag.arguable { background:#9a6a00; }
  details summary { cursor:pointer; color:var(--accent); }
  textarea.csv { width:100%; height:120px; font:12px monospace; margin-top:6px; }
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
    <div class="note" id="chartNote">How this is computed: each record can carry several themes (or none). For every theme we count how many matching records carry it, then show the 10 highest. Click a bar to filter the table to that theme.</div>
  </div>

  <div class="card" id="audit">
    <h2>Check the SDG tagging: 10 records at random</h2>
    <p class="desc" style="margin-bottom:6px">Draw 10 paragraphs from the current filter, read each one, and mark whether the SDGs assigned by the UN index fit it.</p>
    <div class="btnrow">
      <button id="btnCheck" type="button">Check 10 at random</button>
      <button id="btnAgain" type="button" style="display:none">Draw again</button>
    </div>
    <div id="auditInfo"></div>
    <div id="auditBody"></div>
    <div id="auditSummary"></div>
    <div class="note">How this is computed: the 10 records are picked at random by the browser (every matching record has the same chance, no record twice) from the records matching the filters at the moment you click. The SDGs shown are the ones stored in the UN index; nothing is added by an AI. The marks are yours: Right = the SDGs fit (for a record with no SDG, "right" means none is needed); Wrong = they do not fit or an obvious one is missing; Arguable = reasonable people could differ. Agreement rate = records marked Right ÷ records checked. Ten records is a small sample: it gives an impression, not a statistically reliable error rate.</div>
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
  const SAMPLE = 10;

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
    $("btnCheck").disabled = $("btnAgain").disabled = current.length === 0;
    renderChips(); renderChart(); renderTable();
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
  function firstLine(t){
    t = String(t || "").replace(/\s+/g," ").trim();
    if (t.length <= 160) return t;
    const cut = t.slice(0,160), i = cut.lastIndexOf(" ");
    return (i > 100 ? cut.slice(0,i) : cut) + "…";
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

  // ---------- SDG check (random sample, marked by the user)
  let sample = null; // {items:[{r, mark}], desc, pool}
  const MARKS = { right:"Right", wrong:"Wrong", arguable:"Arguable" };

  function filterDesc(){
    const p = [];
    if (state.mech) p.push("mechanism = " + state.mech);
    if (state.body) p.push("body = " + state.body);
    if (state.from !== minY || state.to !== maxY) p.push("years " + state.from + "–" + state.to);
    if (state.sdg) p.push("SDG " + state.sdg);
    if (state.theme) p.push("theme = " + state.theme);
    if (state.q.trim()) p.push('keyword "' + state.q.trim() + '"');
    return p.length ? p.join("; ") : "no filter (all records)";
  }
  function sdgHtml(r){
    const g = arr(r.sdgs), t = arr(r.sdg_targets);
    if (!g.length && !t.length) return '<strong>SDGs assigned by the UN index:</strong> none.';
    let h = '<strong>SDGs assigned by the UN index:</strong><br>' +
      g.map(x => '<span class="sdgchip">SDG '+esc(x)+(sdgNames[x] ? ' – '+esc(sdgNames[x]) : '')+'</span>').join("");
    if (t.length) h += '<ul>' + t.map(x => '<li>'+esc(x)+'</li>').join("") + '</ul>';
    return h;
  }
  function draw(){
    if (!current.length) { sample = null; renderAudit(); return; }
    const pool = current.slice();
    const k = Math.min(SAMPLE, pool.length);
    for (let i = 0; i < k; i++) {
      const j = i + Math.floor(Math.random() * (pool.length - i));
      const t = pool[i]; pool[i] = pool[j]; pool[j] = t;
    }
    sample = { items: pool.slice(0, k).map(r => ({ r, mark:"" })), desc: filterDesc(), pool: current.length };
    renderAudit();
    $("auditInfo").scrollIntoView({ block:"start" });
  }
  function renderAudit(){
    const info = $("auditInfo"), body = $("auditBody");
    $("btnCheck").style.display = sample ? "none" : "inline-block";
    $("btnAgain").style.display = sample ? "inline-block" : "none";
    if (!sample) {
      info.innerHTML = current.length ? "" : '<div class="empty">No records match the current filters, so there is nothing to draw.</div>';
      body.innerHTML = ""; $("auditSummary").innerHTML = ""; return;
    }
    const n = sample.items.length;
    info.innerHTML = '<p class="desc" style="margin-bottom:8px">Drawn at random from <strong>'+sample.pool.toLocaleString()+'</strong> matching records (filter: '+esc(sample.desc)+').' +
      (n < SAMPLE ? ' Fewer than '+SAMPLE+' records match, so all '+n+' are shown.' : '') + '</p>';
    body.innerHTML = sample.items.map((it, i) => {
      const r = it.r;
      const sym = r.doc_url ? '<a href="'+esc(r.doc_url)+'" target="_blank" rel="noopener">'+esc(r.symbol || "document")+'</a>' : esc(r.symbol || "");
      return '<div class="aitem" id="ai'+i+'"><div class="ahead"><span class="k">'+(i+1)+' of '+n+'</span>' +
        '<span>'+sym+'</span><span>'+esc(r.date || r.year || "")+'</span><span>'+esc(r.body || "")+'</span><span>'+esc(r.mechanism || "")+'</span></div>' +
        '<p class="atext">'+esc(r.text || "(no text)")+'</p>' +
        '<div class="sdgbox">'+sdgHtml(r)+'</div>' +
        '<div class="marks" role="radiogroup" aria-label="Your verdict on the SDGs of record '+(i+1)+'">' +
        Object.keys(MARKS).map(m => '<label><input type="radio" name="m'+i+'" value="'+m+'" data-i="'+i+'"> '+MARKS[m]+'</label>').join("") +
        '</div></div>';
    }).join("");
    renderSummary();
  }
  function renderSummary(){
    const box = $("auditSummary");
    if (!sample) { box.innerHTML = ""; return; }
    const items = sample.items, n = items.length;
    const marked = items.filter(x => x.mark).length;
    items.forEach((x, i) => { const el = $("ai"+i); if (el) el.classList.toggle("done", !!x.mark); });
    if (marked < n) { box.innerHTML = '<div class="progress">'+marked+' of '+n+' marked. The result appears when all are marked.</div>'; return; }
    const cnt = m => items.filter(x => x.mark === m).length;
    const right = cnt("right"), wrong = cnt("wrong"), arg = cnt("arguable");
    const pct = Math.round(100 * right / n);
    const list = items.map((x, i) => ({ x, i })).filter(o => o.x.mark !== "right");
    let h = '<div class="result"><div class="rate">'+pct+'%</div>' +
      '<div><strong>Agreement rate:</strong> '+right+' of '+n+' records marked Right. Wrong: '+wrong+'. Arguable: '+arg+'.</div>' +
      '<div class="desc" style="margin:4px 0 0">Sample of '+n+' drawn from '+sample.pool.toLocaleString()+' records (filter: '+esc(sample.desc)+'). Too small to be a reliable error rate.</div>';
    if (list.length) {
      h += '<h2 style="margin-top:16px">Wrong and arguable examples</h2>';
      h += list.map(o => {
        const r = o.x.r;
        const sym = r.doc_url ? '<a href="'+esc(r.doc_url)+'" target="_blank" rel="noopener">'+esc(r.symbol || "document")+'</a>' : esc(r.symbol || "");
        const sd = arr(r.sdgs).length ? arr(r.sdgs).map(g => "SDG "+esc(g)).join(", ") : "no SDG";
        return '<div class="ex"><span class="tag '+o.x.mark+'">'+MARKS[o.x.mark]+'</span> #'+(o.i+1)+' · '+sym+' · '+esc(r.date || "")+' · assigned: '+sd +
          '<details><summary>Show full text</summary><p class="atext" style="margin-top:6px">'+esc(r.text || "")+'</p></details></div>';
      }).join("");
    } else h += '<p>No wrong or arguable examples: you marked every record Right.</p>';
    h += '<div class="btnrow" style="margin-top:14px"><button type="button" id="btnCsv">Download these '+n+' records with my marks (CSV)</button></div>' +
      '<details><summary>Download blocked? Copy the CSV from here</summary><textarea class="csv" readonly id="csvText"></textarea></details></div>';
    box.innerHTML = h;
    $("csvText").value = buildCsv();
  }
  function csvCell(v){ v = String(v == null ? "" : v); return /[",\n\r]/.test(v) ? '"' + v.replace(/"/g, '""') + '"' : v; }
  function buildCsv(){
    const head = ["n","my_mark","symbol","doc_url","date","body","mechanism","sdgs_assigned","sdg_targets_assigned","text","id","filter_applied"];
    const rows = sample.items.map((x, i) => {
      const r = x.r;
      return [i+1, x.mark, r.symbol, r.doc_url, r.date, r.body, r.mechanism, arr(r.sdgs).join("; "), arr(r.sdg_targets).join("; "), r.text, r.id, sample.desc].map(csvCell).join(",");
    });
    return [head.join(",")].concat(rows).join("\r\n");
  }
  function downloadCsv(){
    const blob = new Blob(["\ufeff" + buildCsv()], { type:"text/csv;charset=utf-8" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    const slug = String(country).toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "") || "country";
    a.href = url; a.download = "sdg-check-" + slug + "-" + new Date().toISOString().slice(0,10) + ".csv";
    document.body.appendChild(a); a.click(); a.remove();
    setTimeout(() => URL.revokeObjectURL(url), 2000);
  }
  $("btnCheck").onclick = draw;
  $("btnAgain").onclick = draw;
  $("audit").addEventListener("change", e => {
    const t = e.target;
    if (!t.matches || !t.matches('input[type=radio][data-i]') || !sample) return;
    sample.items[+t.dataset.i].mark = t.value;
    renderSummary();
  });
  $("audit").addEventListener("click", e => { if (e.target.id === "btnCsv") downloadCsv(); });

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
})();
</script>
</body>
</html>
```