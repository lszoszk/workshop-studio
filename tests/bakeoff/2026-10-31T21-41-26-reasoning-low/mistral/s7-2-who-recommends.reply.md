I added a second tab, "Who recommends what", alongside the existing dashboard. It parses the recommending State from the last parentheses of every UPR recommendation, charts the top 15 States, shows a per-State SDG table, and opens a clickable list of that State's recommendations with linked symbols — plus an explicit count of UPR recommendations with no State in parentheses. The whole previous dashboard is unchanged, just wrapped in its own tab panel.

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>UN human rights recommendations dashboard</title>
<style>
  :root{
    --accent:#1f6fb2; --accent-dark:#17537f; --bg:#f4f6f9; --card:#ffffff;
    --border:#dde3ea; --text:#1c2733; --muted:#5b6b7b;
  }
  *{box-sizing:border-box}
  body{
    margin:0; background:var(--bg); color:var(--text);
    font-family:system-ui,-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
    font-size:16px; line-height:1.5;
  }
  .wrap{max-width:1120px; margin:0 auto; padding:26px 20px 64px}
  header{border-bottom:3px solid var(--accent); padding-bottom:14px}
  h1{font-size:1.55rem; margin:0 0 6px; color:#12314a}
  h2{font-size:1.15rem; margin:0 0 4px; color:#12314a}
  .muted{color:var(--muted)}
  a{color:var(--accent)}
  .tabs{display:flex; gap:6px; margin-top:18px; border-bottom:1px solid var(--border); flex-wrap:wrap}
  .tab{
    background:none; border:none; border-bottom:3px solid transparent; padding:10px 16px;
    font-size:1rem; font-weight:600; color:var(--muted); cursor:pointer; font-family:inherit;
  }
  .tab:hover{color:var(--accent-dark)}
  .tab.active{color:var(--accent); border-bottom-color:var(--accent)}
  .card{background:var(--card); border:1px solid var(--border); border-radius:10px; padding:18px 20px; margin-top:18px}
  .note{
    font-size:.88rem; color:var(--muted); background:#f2f6fa;
    border-left:3px solid var(--accent); border-radius:0 8px 8px 0;
    padding:8px 12px; margin:10px 0 14px;
  }
  .stats{display:flex; flex-wrap:wrap; gap:14px; margin-top:18px}
  .stat{background:var(--card); border:1px solid var(--border); border-radius:10px; padding:12px 18px; min-width:150px; flex:1}
  .stat .num{font-size:1.6rem; font-weight:700; color:var(--accent)}
  .stat .lbl{font-size:.85rem; color:var(--muted)}
  .filters-grid{display:grid; grid-template-columns:repeat(auto-fit,minmax(215px,1fr)); gap:14px 18px; margin-top:6px}
  .field label{display:block; font-size:.85rem; font-weight:600; color:var(--muted); margin-bottom:4px}
  .field select,.field input{
    width:100%; padding:8px 10px; font-size:1rem; color:var(--text);
    border:1px solid var(--border); border-radius:8px; background:#fff;
  }
  .field select:focus,.field input:focus{outline:2px solid var(--accent); outline-offset:1px}
  .year-range{display:flex; align-items:center; gap:8px}
  .year-range span{color:var(--muted); white-space:nowrap}
  .filter-actions{display:flex; align-items:center; gap:12px; margin-top:16px; flex-wrap:wrap}
  .btn{background:var(--accent); color:#fff; border:none; border-radius:8px; padding:9px 16px; font-size:1rem; cursor:pointer}
  .btn:hover{background:var(--accent-dark)}
  .btn.secondary{background:#fff; color:var(--accent); border:1px solid var(--accent)}
  .btn.secondary:hover{background:#eaf3fb}
  #activeFilters{font-size:.9rem; color:var(--muted)}
  .chart-wrap{position:relative; width:100%}
  .table-wrap{overflow-x:auto}
  table{width:100%; border-collapse:collapse; table-layout:fixed; font-size:.95rem}
  th{
    text-align:left; font-size:.76rem; text-transform:uppercase; letter-spacing:.05em;
    color:var(--muted); border-bottom:2px solid var(--border); padding:8px 10px; white-space:nowrap;
  }
  td{padding:10px; border-bottom:1px solid var(--border); vertical-align:top; overflow-wrap:anywhere}
  col.c-date{width:108px} col.c-body{width:150px} col.c-type{width:140px} col.c-symbol{width:190px}
  tr.rec{cursor:pointer}
  tr.rec:hover{background:#f2f7fc}
  tr.rec.open{background:#eaf3fb}
  td.date{white-space:nowrap; color:var(--muted)}
  td.symbol a{word-break:break-all}
  td.preview{color:#33414f; display:-webkit-box; -webkit-line-clamp:2; -webkit-box-orient:vertical; overflow:hidden}
  tr.details td{background:#f8fafc}
  .fulltext{white-space:pre-wrap; margin:0 0 12px}
  .meta{display:flex; flex-wrap:wrap; gap:6px 20px; color:var(--muted); font-size:.9rem; margin-bottom:12px}
  .lbl2{font-weight:600; color:var(--muted); font-size:.85rem; margin-right:6px}
  .chips div{margin:4px 0}
  .chip{display:inline-block; background:#e8f1f9; color:var(--accent-dark); border-radius:999px; padding:2px 10px; margin:2px 4px 2px 0; font-size:.85rem}
  .empty-cell{color:var(--muted); text-align:center; padding:22px 10px}
  #matchLine{font-weight:600; margin:2px 0 10px}
  /* who-recommends-what tab */
  #whoNoState{font-weight:600; margin:2px 0 12px}
  tr.state-row{cursor:pointer}
  tr.state-row:hover{background:#f2f7fc}
  tr.state-row.sel{background:#eaf3fb}
  td.state-name{font-weight:600}
  td.num-cell{white-space:nowrap}
  .rec-item{border:1px solid var(--border); border-radius:8px; margin-bottom:10px; overflow:hidden; background:#fff}
  .rec-head{padding:10px 12px; cursor:pointer; display:flex; gap:12px; flex-wrap:wrap; align-items:baseline}
  .rec-head:hover{background:#f2f7fc}
  .rec-item.open .rec-head{background:#eaf3fb}
  .rec-head .date{color:var(--muted); white-space:nowrap}
  .rec-head .preview{flex:1; min-width:220px; color:#33414f}
  .rec-full{border-top:1px solid var(--border); padding:12px; background:#f8fafc; white-space:pre-wrap}
  footer{margin-top:26px; font-size:.85rem; color:var(--muted)}
</style>
</head>
<body>
<div class="wrap">

  <header>
    <h1 id="title">UN human rights recommendations &amp; observations</h1>
    <p id="subtitle" class="muted">Loading…</p>
  </header>

  <nav class="tabs" role="tablist" aria-label="Views">
    <button type="button" class="tab active" id="tabDash" role="tab" aria-selected="true" aria-controls="panelDash">Dashboard</button>
    <button type="button" class="tab" id="tabWho" role="tab" aria-selected="false" aria-controls="panelWho">Who recommends what</button>
  </nav>

  <div id="panelDash" role="tabpanel" aria-labelledby="tabDash">

    <section class="stats" id="stats" aria-label="Dataset overview"></section>
    <p class="note" id="statsNote"></p>

    <section class="card" aria-label="Filters">
      <h2>Filters</h2>
      <p class="note">All filters combine (a record must match every one of them). The numbers in brackets show how many records each option has in the full dataset. The keyword search looks inside the paragraph text, symbol, body, section, themes, SDG targets and affected persons.</p>
      <div class="filters-grid">
        <div class="field">
          <label for="fMech">Mechanism</label>
          <select id="fMech"></select>
        </div>
        <div class="field">
          <label for="fBody">Treaty body / mandate</label>
          <select id="fBody"></select>
        </div>
        <div class="field">
          <label for="fYearFrom">Year range</label>
          <div class="year-range">
            <input id="fYearFrom" type="number" inputmode="numeric" aria-label="From year">
            <span>to</span>
            <input id="fYearTo" type="number" inputmode="numeric" aria-label="To year">
          </div>
        </div>
        <div class="field">
          <label for="fSdg">SDG (a record matches if it carries this goal)</label>
          <select id="fSdg"></select>
        </div>
        <div class="field">
          <label for="fQ">Keyword search</label>
          <input id="fQ" type="search" placeholder="e.g. education, torture, women…">
        </div>
      </div>
      <div class="filter-actions">
        <button class="btn secondary" id="fReset" type="button">Reset all filters</button>
        <span id="activeFilters"></span>
      </div>
    </section>

    <section class="card" aria-label="Themes chart">
      <h2>Most frequent themes (top 10)</h2>
      <p class="note" id="chartNote"></p>
      <div class="chart-wrap" id="chartWrap"><canvas id="themeChart"></canvas></div>
      <p id="chartEmpty" class="note" hidden>No records match the current filters, so there are no themes to count. Loosen a filter to see the chart.</p>
    </section>

    <section class="card" aria-label="Matching records">
      <h2>Matching records</h2>
      <p class="note">How this is computed: the rows below are exactly the records that match all the filters above, sorted by date (newest first). The preview column shows the first line of the paragraph — click any row to read the full text, themes, SDG targets and affected persons. The symbol links to the UN document and opens in a new tab.</p>
      <p id="matchLine"></p>
      <div class="table-wrap">
        <table>
          <colgroup><col class="c-date"><col class="c-body"><col class="c-type"><col class="c-symbol"><col></colgroup>
          <thead>
            <tr><th>Date</th><th>Body / mandate</th><th>Type</th><th>Symbol (UN document)</th><th>Text (first line — click row for full text)</th></tr>
          </thead>
          <tbody id="tbody"></tbody>
        </table>
      </div>
      <p style="margin:12px 0 0"><button class="btn secondary" id="showAll" type="button" hidden></button></p>
    </section>

  </div>

  <div id="panelWho" role="tabpanel" aria-labelledby="tabWho" hidden>

    <section class="card" aria-label="Top recommending States">
      <h2>States that recommend most (UPR only)</h2>
      <p class="note" id="whoNote"></p>
      <p id="whoNoState"></p>
      <div class="chart-wrap" id="whoChartWrap"><canvas id="whoChart"></canvas></div>
      <p id="whoEmpty" class="note" hidden></p>
    </section>

    <section class="card" aria-label="SDGs by recommending State">
      <h2>SDGs each State raises most</h2>
      <p class="note" id="whoTableNote"></p>
      <div class="table-wrap">
        <table id="whoTable">
          <colgroup><col style="width:26%"><col style="width:12%"><col></colgroup>
          <thead>
            <tr><th>Recommending State (click to list its recommendations)</th><th>UPR recommendations</th><th>SDGs raised most (top 3, with counts)</th></tr>
          </thead>
          <tbody id="whoTbody"></tbody>
        </table>
      </div>
    </section>

    <section class="card" id="whoDetailCard" aria-label="Recommendations by selected State" hidden>
      <h2 id="whoDetailTitle"></h2>
      <p class="note" id="whoDetailNote"></p>
      <div id="whoDetailList"></div>
    </section>

  </div>

  <footer id="foot"></footer>
</div>

<script>
(function(){
  "use strict";
  var DATA = window.WORKSHOP_DATA || {};
  var uhri = DATA.uhri || {};
  var records = Array.isArray(uhri.records) ? uhri.records : [];
  var sdgNames = uhri.sdg_names || {};
  var country = uhri.country || "the participant country";

  var esc = function(s){
    return String(s == null ? "" : s).replace(/[&<>"']/g, function(c){
      return {"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c];
    });
  };

  var el = {
    title: document.getElementById("title"),
    subtitle: document.getElementById("subtitle"),
    stats: document.getElementById("stats"),
    statsNote: document.getElementById("statsNote"),
    mech: document.getElementById("fMech"),
    body: document.getElementById("fBody"),
    yFrom: document.getElementById("fYearFrom"),
    yTo: document.getElementById("fYearTo"),
    sdg: document.getElementById("fSdg"),
    q: document.getElementById("fQ"),
    reset: document.getElementById("fReset"),
    active: document.getElementById("activeFilters"),
    chartNote: document.getElementById("chartNote"),
    chartWrap: document.getElementById("chartWrap"),
    chartEmpty: document.getElementById("chartEmpty"),
    canvas: document.getElementById("themeChart"),
    tbody: document.getElementById("tbody"),
    matchLine: document.getElementById("matchLine"),
    showAll: document.getElementById("showAll"),
    foot: document.getElementById("foot"),
    tabDash: document.getElementById("tabDash"),
    tabWho: document.getElementById("tabWho"),
    panelDash: document.getElementById("panelDash"),
    panelWho: document.getElementById("panelWho"),
    whoNote: document.getElementById("whoNote"),
    whoNoState: document.getElementById("whoNoState"),
    whoChartWrap: document.getElementById("whoChartWrap"),
    whoChartCanvas: document.getElementById("whoChart"),
    whoEmpty: document.getElementById("whoEmpty"),
    whoTableNote: document.getElementById("whoTableNote"),
    whoTbody: document.getElementById("whoTbody"),
    whoDetailCard: document.getElementById("whoDetailCard"),
    whoDetailTitle: document.getElementById("whoDetailTitle"),
    whoDetailNote: document.getElementById("whoDetailNote"),
    whoDetailList: document.getElementById("whoDetailList")
  };

  var years = records.map(function(r){ return r.year; }).filter(function(y){ return typeof y === "number" && isFinite(y); });
  var minYear = years.length ? Math.min.apply(null, years) : null;
  var maxYear = years.length ? Math.max.apply(null, years) : null;

  var byId = {};
  records.forEach(function(r){ if(r && r.id != null) byId[r.id] = r; });

  var state = { mechanism:"", body:"", yearFrom:-Infinity, yearTo:Infinity, sdg:"", q:"" };
  var currentList = [];
  var renderAll = false;
  var CAP = 200;
  var chart = null;

  /* ---------- header & stats ---------- */
  el.title.textContent = "UN human rights recommendations & observations addressed to " + country;

  var srcHtml;
  if (uhri.source) {
    srcHtml = uhri.source_url
      ? '<a href="' + esc(uhri.source_url) + '" target="_blank" rel="noopener">' + esc(uhri.source) + "</a>"
      : esc(uhri.source);
  } else {
    srcHtml = "UN human rights bodies (UHRI database)";
  }
  var yearSpan = (minYear != null && maxYear != null) ? (minYear + "–" + maxYear) : "unknown";
  el.subtitle.innerHTML =
    srcHtml + " · <strong>" + records.length + "</strong> records addressed to <strong>" + esc(country) + "</strong>" +
    " · years " + esc(yearSpan) +
    (uhri.built ? " · dataset built " + esc(uhri.built) : "");

  function uniqueCount(key){
    var s = {};
    records.forEach(function(r){ var v = r && r[key] ? r[key] : "(not specified)"; s[v] = true; });
    return Object.keys(s).length;
  }

  el.stats.innerHTML =
    '<div class="stat"><div class="num">' + records.length + '</div><div class="lbl">records in the dataset</div></div>' +
    '<div class="stat"><div class="num">' + esc(yearSpan) + '</div><div class="lbl">years covered (earliest–latest)</div></div>' +
    '<div class="stat"><div class="num">' + uniqueCount("body") + '</div><div class="lbl">treaty bodies / mandates</div></div>' +
    '<div class="stat"><div class="num">' + uniqueCount("mechanism") + '</div><div class="lbl">mechanisms</div></div>';
  el.statsNote.textContent =
    "How this is computed: these are plain counts over the " + records.length + " records loaded for " + country +
    " (source: " + (uhri.source || "UHRI") + "). The year span is the smallest and largest year value found in the records; records without a year are not included in that span.";

  /* ---------- filter controls ---------- */
  function countBy(key){
    var m = {};
    records.forEach(function(r){
      var v = r && r[key] ? String(r[key]) : "(not specified)";
      m[v] = (m[v] || 0) + 1;
    });
    return Object.keys(m).sort(function(a,b){ return a.localeCompare(b); }).map(function(k){ return [k, m[k]]; });
  }
  function fillSelect(sel, entries, allLabel){
    sel.innerHTML = '<option value="">' + esc(allLabel) + "</option>" + entries.map(function(e){
      return '<option value="' + esc(e[0]) + '">' + esc(e[0]) + " (" + e[1] + ")</option>";
    }).join("");
  }
  fillSelect(el.mech, countBy("mechanism"), "All mechanisms");
  fillSelect(el.body, countBy("body"), "All bodies / mandates");

  var sdgSet = {};
  records.forEach(function(r){
    (Array.isArray(r.sdgs) ? r.sdgs : []).forEach(function(s){
      var n = Number(s);
      if (isFinite(n)) sdgSet[n] = true;
    });
  });
  var sdgNums = Object.keys(sdgSet).map(Number).sort(function(a,b){ return a - b; });
  el.sdg.innerHTML = '<option value="">All SDGs</option>' + sdgNums.map(function(n){
    var name = sdgNames[String(n)];
    return '<option value="' + n + '">SDG ' + n + (name ? " — " + esc(name) : "") + "</option>";
  }).join("");

  if (minYear != null) { el.yFrom.value = minYear; el.yFrom.min = minYear; el.yFrom.max = maxYear; }
  if (maxYear != null) { el.yTo.value = maxYear; el.yTo.min = minYear; el.yTo.max = maxYear; }

  /* ---------- filtering ---------- */
  function readState(){
    state.mechanism = el.mech.value;
    state.body = el.body.value;
    var f = parseInt(el.yFrom.value, 10), t = parseInt(el.yTo.value, 10);
    state.yearFrom = isFinite(f) ? f : -Infinity;
    state.yearTo = isFinite(t) ? t : Infinity;
    state.sdg = el.sdg.value;
    state.q = el.q.value.trim().toLowerCase();
  }
  function matches(r){
    if (state.mechanism && String(r.mechanism || "") !== state.mechanism) return false;
    if (state.body && String(r.body || "") !== state.body) return false;
    if (typeof r.year === "number" && isFinite(r.year)) {
      if (r.year < state.yearFrom || r.year > state.yearTo) return false;
    }
    if (state.sdg !== "") {
      var sdgs = (Array.isArray(r.sdgs) ? r.sdgs : []).map(Number);
      if (sdgs.indexOf(Number(state.sdg)) === -1) return false;
    }
    if (state.q) {
      var hay = [r.text, r.symbol, r.body, r.section, r.type, r.mechanism]
        .concat(Array.isArray(r.themes) ? r.themes : [])
        .concat(Array.isArray(r.sdg_targets) ? r.sdg_targets : [])
        .concat(Array.isArray(r.affected_persons) ? r.affected_persons : [])
        .concat(Array.isArray(r.countries) ? r.countries : [])
        .join(" ").toLowerCase();
      if (hay.indexOf(state.q) === -1) return false;
    }
    return true;
  }
  function cmp(a, b){
    return String(b.date || "").localeCompare(String(a.date || "")) ||
           String(a.symbol || "").localeCompare(String(b.symbol || ""));
  }

  /* ---------- theme chart ---------- */
  function themeCounts(list){
    var m = {};
    list.forEach(function(r){
      (Array.isArray(r.themes) ? r.themes : []).forEach(function(t){
        if (t) m[t] = (m[t] || 0) + 1;
      });
    });
    return Object.keys(m).map(function(k){ return [k, m[k]]; })
      .sort(function(a, b){ return b[1] - a[1] || a[0].localeCompare(b[0]); })
      .slice(0, 10);
  }
  function renderChart(list){
    if (chart) { chart.destroy(); chart = null; }
    var counts = themeCounts(list);
    if (!counts.length || !window.Chart) {
      el.chartWrap.style.display = "none";
      el.chartEmpty.hidden = false;
      el.chartNote.textContent = "How this is computed: no records match the current filters (or no chart library is available), so there are no themes to count.";
      return;
    }
    el.chartEmpty.hidden = true;
    el.chartWrap.style.display = "block";
    el.chartWrap.style.height = Math.max(220, counts.length * 40 + 70) + "px";
    el.chartNote.textContent =
      "How this is computed: each of the " + list.length + " matching record(s) is counted once for every theme it carries " +
      "(a record can carry several themes, so the bars can add up to more than " + list.length + "). " +
      "Only the " + counts.length + " most frequent theme(s) are shown, sorted by count, highest first.";
    chart = new Chart(el.canvas.getContext("2d"), {
      type: "bar",
      data: {
        labels: counts.map(function(c){ return c[0]; }),
        datasets: [{
          label: "Number of matching records",
          data: counts.map(function(c){ return c[1]; }),
          backgroundColor: "#1f6fb2",
          borderRadius: 4
        }]
      },
      options: {
        indexAxis: "y",
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false },
          tooltip: { callbacks: { label: function(c){ return " " + c.parsed.x + " record(s)"; } } }
        },
        scales: {
          x: { beginAtZero: true, ticks: { precision: 0 }, title: { display: true, text: "Number of matching records" } },
          y: { ticks: { autoSkip: false } }
        }
      }
    });
  }

  /* ---------- table ---------- */
  function firstLine(t){
    if (!t) return "";
    var line = String(t).split("\n")[0].trim();
    return line.length > 240 ? line.slice(0, 240).trimEnd() + "…" : line;
  }
  function rowHtml(r){
    var link = r.doc_url
      ? '<a href="' + esc(r.doc_url) + '" target="_blank" rel="noopener" title="Open the UN document in a new tab">' + esc(r.symbol || "(no symbol)") + " ↗</a>"
      : esc(r.symbol || "—");
    return '<tr class="rec" data-id="' + esc(r.id) + '">' +
      '<td class="date">' + esc(r.date || "—") + "</td>" +
      '<td class="body">' + esc(r.body || "—") + "</td>" +
      '<td class="type">' + esc(r.type || "—") + "</td>" +
      '<td class="symbol">' + link + "</td>" +
      '<td class="preview">' + esc(firstLine(r.text)) + "</td>" +
      "</tr>";
  }
  function chipsHtml(r){
    var chips = [];
    function chipRow(label, arr){
      if (Array.isArray(arr) && arr.length) {
        chips.push('<div><span class="lbl2">' + esc(label) + '</span>' +
          arr.map(function(t){ return '<span class="chip">' + esc(t) + "</span>"; }).join("") + "</div>");
      }
    }
    chipRow("Themes:", r.themes);
    chipRow("SDG targets:", r.sdg_targets);
    chipRow("Affected persons:", r.affected_persons);
    chipRow("Countries mentioned:", r.countries);
    return chips.length ? '<div class="chips">' + chips.join("") + "</div>" : "";
  }
  function detailsHtml(r){
    var meta = [];
    if (r.date) meta.push("<span><strong>Date:</strong> " + esc(r.date) + "</span>");
    if (r.mechanism) meta.push("<span><strong>Mechanism:</strong> " + esc(r.mechanism) + "</span>");
    if (r.type) meta.push("<span><strong>Type:</strong> " + esc(r.type) + "</span>");
    if (r.section) meta.push("<span><strong>Section:</strong> " + esc(r.section) + "</span>");
    if (r.doc_url) meta.push('<span><a href="' + esc(r.doc_url) + '" target="_blank" rel="noopener">Open the UN document (' + esc(r.symbol) + ") ↗</a></span>");
    return '<div class="meta">' + meta.join("") + "</div>" +
      '<p class="fulltext">' + esc(r.text || "(no text available)") + "</p>" + chipsHtml(r);
  }
  function renderTable(list){
    var total = list.length;
    var shown = renderAll ? list : list.slice(0, CAP);
    if (!total) {
      el.tbody.innerHTML = '<tr><td colspan="5" class="empty-cell">No records match the current filters. Loosen or reset a filter to see records.</td></tr>';
    } else {
      el.tbody.innerHTML = shown.map(rowHtml).join("");
    }
    el.matchLine.textContent = "Showing " + shown.length + " of " + total + " matching record(s), out of " + records.length + " in the dataset.";
    if (total > shown.length) {
      el.showAll.hidden = false;
      el.showAll.textContent = "Show all " + total + " matching records (currently showing the first " + shown.length + ")";
    } else {
      el.showAll.hidden = true;
    }
  }
  el.tbody.addEventListener("click", function(e){
    if (e.target.closest("a")) return;
    var tr = e.target.closest("tr.rec");
    if (!tr) return;
    var id = tr.getAttribute("data-id");
    var next = tr.nextElementSibling;
    if (next && next.classList.contains("details") && next.getAttribute("data-for") === id) {
      next.remove(); tr.classList.remove("open"); return;
    }
    Array.prototype.forEach.call(el.tbody.querySelectorAll("tr.details"), function(d){ d.remove(); });
    Array.prototype.forEach.call(el.tbody.querySelectorAll("tr.rec.open"), function(t){ t.classList.remove("open"); });
    var r = byId[id];
    if (!r) return;
    var det = document.createElement("tr");
    det.className = "details";
    det.setAttribute("data-for", id);
    det.innerHTML = '<td colspan="5">' + detailsHtml(r) + "</td>";
    tr.after(det);
    tr.classList.add("open");
  });
  el.showAll.addEventListener("click", function(){ renderAll = true; renderTable(currentList); });

  /* ---------- active filter summary ---------- */
  function renderActive(){
    var parts = [];
    if (state.mechanism) parts.push("mechanism = “" + state.mechanism + "”");
    if (state.body) parts.push("body/mandate = “" + state.body + "”");
    if (minYear != null && state.yearFrom > minYear) parts.push("year ≥ " + state.yearFrom);
    if (maxYear != null && state.yearTo < maxYear) parts.push("year ≤ " + state.yearTo);
    if (state.sdg) parts.push("SDG " + state.sdg + (sdgNames[String(state.sdg)] ? " (" + sdgNames[String(state.sdg)] + ")" : ""));
    if (state.q) parts.push("keyword contains “" + el.q.value.trim() + "”");
    el.active.textContent = parts.length ? "Active filters: " + parts.join(" · ") : "No filters active — all records are shown.";
  }

  /* ---------- update ---------- */
  function update(){
    readState();
    renderAll = false;
    currentList = records.filter(matches).sort(cmp);
    renderChart(currentList);
    renderTable(currentList);
    renderActive();
  }

  var deb;
  el.q.addEventListener("input", function(){ clearTimeout(deb); deb = setTimeout(update, 200); });
  el.mech.addEventListener("change", update);
  el.body.addEventListener("change", update);
  el.sdg.addEventListener("change", update);
  el.yFrom.addEventListener("change", update);
  el.yTo.addEventListener("change", update);
  el.reset.addEventListener("click", function(){
    el.mech.value = ""; el.body.value = ""; el.sdg.value = ""; el.q.value = "";
    if (minYear != null) el.yFrom.value = minYear;
    if (maxYear != null) el.yTo.value = maxYear;
    update();
  });

  /* =====================================================
     Tab 2 — "Who recommends what" (UPR recommending States)
     ===================================================== */
  function recommendingState(text){
    if (!text) return null;
    var t = String(text).trim();
    var m = t.match(/\(([^()]*)\)\s*\.?\s*$/);   /* last parentheses at the end of the text */
    if (!m) return null;
    var s = m[1].trim().replace(/\.+$/, "").trim();
    return s ? s : null;
  }

  var uprAll = records.filter(function(r){ return r.mechanism === "Universal Periodic Review"; });
  var uprList = uprAll.filter(function(r){ return /recommend/i.test(String(r.type || "")); });
  if (!uprList.length) uprList = uprAll;   /* fall back if no UPR record is typed "Recommendations" */

  var stateRecs = {};   /* State -> [records] */
  var noStateCount = 0;
  uprList.forEach(function(r){
    var s = recommendingState(r.text);
    if (s) { (stateRecs[s] = stateRecs[s] || []).push(r); }
    else noStateCount++;
  });
  var topStates = Object.keys(stateRecs).map(function(k){ return [k, stateRecs[k]]; })
    .sort(function(a, b){ return b[1].length - a[1].length || a[0].localeCompare(b[0]); })
    .slice(0, 15);

  function topSdgs(recs, k){
    var m = {};
    recs.forEach(function(r){
      var seen = {};
      (Array.isArray(r.sdgs) ? r.sdgs : []).forEach(function(s){
        var n = Number(s);
        if (isFinite(n) && !seen[n]) { seen[n] = 1; m[n] = (m[n] || 0) + 1; }
      });
    });
    return Object.keys(m).map(Number)
      .sort(function(a, b){ return (m[b] - m[a]) || (a - b); })
      .slice(0, k)
      .map(function(n){ return { n: n, c: m[n], name: sdgNames[String(n)] || "" }; });
  }

  var whoChart = null;
  var whoChartBuilt = false;

  function renderWhoChart(){
    if (whoChart) { whoChart.destroy(); whoChart = null; }
    if (!topStates.length || !window.Chart) {
      el.whoChartWrap.style.display = "none";
      el.whoEmpty.hidden = false;
      el.whoEmpty.textContent = topStates.length
        ? "The chart library is not available, so the bars cannot be drawn; the table below still lists the States."
        : "There are no UPR recommendations with a recommending State in parentheses for " + country + ", so there is nothing to chart.";
      return;
    }
    el.whoEmpty.hidden = true;
    el.whoChartWrap.style.display = "block";
    el.whoChartWrap.style.height = Math.max(240, topStates.length * 36 + 80) + "px";
    whoChart = new Chart(el.whoChartCanvas.getContext("2d"), {
      type: "bar",
      data: {
        labels: topStates.map(function(s){ return s[0]; }),
        datasets: [{
          label: "UPR recommendations to " + country,
          data: topStates.map(function(s){ return s[1].length; }),
          backgroundColor: "#1f6fb2",
          borderRadius: 4
        }]
      },
      options: {
        indexAxis: "y",
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false },
          tooltip: { callbacks: { label: function(c){ return " " + c.parsed.x + " recommendation(s)"; } } }
        },
        scales: {
          x: { beginAtZero: true, ticks: { precision: 0 }, title: { display: true, text: "Number of UPR recommendations" } },
          y: { ticks: { autoSkip: false } }
        }
      }
    });
    whoChartBuilt = true;
  }

  function renderWhoTable(){
    if (!topStates.length) {
      el.whoTbody.innerHTML = '<tr><td colspan="3" class="empty-cell">No UPR recommendations with a recommending State were found for ' + esc(country) + ".</td></tr>";
      return;
    }
    el.whoTbody.innerHTML = topStates.map(function(s){
      var name = s[0], recs = s[1];
      var sdgs = topSdgs(recs, 3);
      var sdgText = sdgs.length
        ? sdgs.map(function(o){ return "SDG " + o.n + (o.name ? " — " + o.name : "") + " (" + o.c + ")"; }).join("; ")
        : "— (no SDG tagged on these recommendations)";
      return '<tr class="state-row" data-state="' + esc(name) + '">' +
        '<td class="state-name">' + esc(name) + "</td>" +
        '<td class="num-cell">' + recs.length + "</td>" +
        '<td class="sdg-cell">' + esc(sdgText) + "</td>" +
        "</tr>";
    }).join("");
  }

  function selectState(name){
    Array.prototype.forEach.call(el.whoTbody.querySelectorAll("tr.state-row.sel"), function(t){ t.classList.remove("sel"); });
    var row = el.whoTbody.querySelector('tr.state-row[data-state="' + CSS.escape(name) + '"]');
    if (row) row.classList.add("sel");
    var recs = (stateRecs[name] || []).slice().sort(cmp);
    el.whoDetailCard.hidden = false;
    el.whoDetailTitle.textContent = "Recommendations by " + name + " (" + recs.length + ")";
    el.whoDetailNote.textContent =
      "How this is computed: all " + recs.length + " UPR recommendation(s) addressed to " + country +
      " whose paragraph text ends with “(" + name + ")”, sorted by date (newest first). Click an item to read the full paragraph; the symbol links to the UN document and opens in a new tab.";
    el.whoDetailList.innerHTML = recs.map(function(r){
      var link = r.doc_url
        ? '<a href="' + esc(r.doc_url) + '" target="_blank" rel="noopener">' + esc(r.symbol || "(no symbol)") + " ↗</a>"
        : esc(r.symbol || "—");
      return '<div class="rec-item" data-id="' + esc(r.id) + '">' +
        '<div class="rec-head"><span class="date">' + esc(r.date || "—") + "</span> " + link +
        '<span class="preview">' + esc(firstLine(r.text)) + "</span></div>" +
        '<div class="rec-full" hidden>' + esc(r.text || "(no text available)") + chipsHtml(r) + "</div>" +
        "</div>";
    }).join("");
    el.whoDetailCard.scrollIntoView({ block: "nearest" });
  }

  el.whoTbody.addEventListener("click", function(e){
    var tr = e.target.closest("tr.state-row");
    if (!tr) return;
    selectState(tr.getAttribute("data-state"));
  });
  el.whoDetailList.addEventListener("click", function(e){
    if (e.target.closest("a")) return;
    var item = e.target.closest(".rec-item");
    if (!item) return;
    var full = item.querySelector(".rec-full");
    var open = !full.hidden;
    Array.prototype.forEach.call(el.whoDetailList.querySelectorAll(".rec-item.open"), function(o){
      o.classList.remove("open"); o.querySelector(".rec-full").hidden = true;
    });
    if (!open) { full.hidden = false; item.classList.add("open"); }
  });

  function renderWhoNotes(){
    var typeNote = (uprList.length && uprList.length !== uprAll.length)
      ? " (of the " + uprAll.length + " UPR records, only those of type “Recommendations” are used)"
      : "";
    el.whoNote.textContent =
      "How this is computed: only the " + uprList.length + " record(s) with mechanism “Universal Periodic Review”" + typeNote +
      " addressed to " + country + " are used — one record is one paragraph, i.e. one recommendation. The recommending State is extracted with a regex " +
      "from the last parentheses at the end of the paragraph text (e.g. “…for all children (Croatia).” → Croatia). The chart shows the 15 States that made the most recommendations to " +
      country + ", sorted by count, highest first.";
    el.whoNoState.textContent =
      noStateCount + " of the " + uprList.length + " UPR recommendations had no State in parentheses at the end of the text — they are not attributed to any State and are excluded from the chart and table below.";
    el.whoTableNote.textContent =
      "How this is computed: for each of the " + topStates.length + " States shown in the chart, every SDG goal tagged on its recommendations is counted once per recommendation " +
      "(a recommendation carrying several SDGs counts once for each). The 3 most frequent goals per State are listed with their counts. Click a State row to list all of its recommendations below.";
  }

  /* ---------- tabs ---------- */
  function showTab(which){
    var dash = which === "dash";
    el.panelDash.hidden = !dash;
    el.panelWho.hidden = dash;
    el.tabDash.classList.toggle("active", dash);
    el.tabWho.classList.toggle("active", !dash);
    el.tabDash.setAttribute("aria-selected", dash ? "true" : "false");
    el.tabWho.setAttribute("aria-selected", dash ? "false" : "true");
    if (!dash && !whoChartBuilt) renderWhoChart();
    if (!dash && whoChart) whoChart.resize();
  }
  el.tabDash.addEventListener("click", function(){ showTab("dash"); });
  el.tabWho.addEventListener("click", function(){ showTab("who"); });

  el.foot.textContent =
    "Source: " + (uhri.source || "UHRI") + (uhri.source_url ? " (" + uhri.source_url + ")" : "") +
    ". All counting, filtering, sorting and State extraction on this page is done locally in your browser from the loaded dataset; nothing is estimated and no data leaves the page.";

  renderWhoNotes();
  renderWhoTable();
  update();
})();
</script>
</body>
</html>
```