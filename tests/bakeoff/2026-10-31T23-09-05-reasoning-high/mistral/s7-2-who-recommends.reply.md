I added a second tab, "Who recommends what", next to the dashboard. It parses the recommending State from the final parentheses of every UPR recommendation, charts the top 15 States, shows each one's most-raised SDGs in a small clickable table, and clicking a State (bar or row) opens its full list of recommendations with linked symbols — plus a clear count of UPR recommendations with no State in parentheses.

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>UN human rights recommendations dashboard</title>
<style>
  :root{
    --accent:#1f6fb2; --accent-dark:#175a94; --ink:#1c2733; --muted:#5b6b7b;
    --line:#dfe6ee; --bg:#f4f7fa; --card:#ffffff;
  }
  *{box-sizing:border-box}
  html{font-size:16px}
  body{
    margin:0; background:var(--bg); color:var(--ink); line-height:1.5;
    font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif;
  }
  .wrap{max-width:1120px;margin:0 auto;padding:0 20px}
  header{padding:34px 0 8px}
  h1{font-size:1.65rem;margin:0 0 6px}
  .desc{margin:0 0 18px;color:var(--muted)}
  .desc a{color:var(--accent)}
  .stats{display:flex;flex-wrap:wrap;gap:14px;margin:0 0 6px}
  .stat{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:12px 18px;min-width:140px}
  .stat .num{display:block;font-size:1.55rem;font-weight:700;color:var(--accent);line-height:1.2}
  .stat .lbl{font-size:.84rem;color:var(--muted)}
  .stat.wide{flex:1;min-width:280px}
  .chips{display:flex;flex-wrap:wrap;gap:6px;margin-top:8px}
  .chip{background:#eaf2fa;color:var(--accent-dark);border-radius:999px;padding:2px 11px;font-size:.82rem}
  .note{font-size:.85rem;color:var(--muted);margin:8px 0 0}
  .tabs{display:flex;gap:8px;margin-top:20px}
  .tab{
    font:inherit;padding:9px 20px;border:1px solid var(--line);background:var(--card);
    color:var(--ink);border-radius:8px;cursor:pointer;
  }
  .tab.active{background:var(--accent);border-color:var(--accent);color:#fff;font-weight:600}
  main{padding-bottom:56px}
  .card{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:18px 20px;margin:18px 0}
  .card h2{font-size:1.08rem;margin:0 0 4px}
  .fgrid{display:grid;grid-template-columns:repeat(auto-fit,minmax(185px,1fr));gap:12px;margin-top:14px}
  label.f{display:flex;flex-direction:column;gap:4px;font-size:.84rem;color:var(--muted)}
  select,input[type=search]{
    font:inherit;padding:7px 9px;border:1px solid var(--line);border-radius:7px;
    background:#fff;color:var(--ink);width:100%;
  }
  select:focus,input[type=search]:focus{outline:2px solid var(--accent);outline-offset:1px}
  .frow{display:flex;flex-wrap:wrap;gap:12px;align-items:flex-end;margin-top:12px}
  .frow label.f{flex:1;min-width:230px}
  button.act{
    font:inherit;padding:8px 18px;border:1px solid var(--accent);background:var(--accent);
    color:#fff;border-radius:7px;cursor:pointer;
  }
  button.act:hover{background:var(--accent-dark)}
  .showing{margin:14px 0 0;font-weight:600}
  .chartbox{position:relative;width:100%;margin-top:12px}
  .empty{color:var(--muted);font-style:italic;margin:14px 0 4px}
  table{width:100%;border-collapse:collapse;table-layout:fixed;margin-top:12px}
  th{
    text-align:left;font-size:.78rem;text-transform:uppercase;letter-spacing:.04em;
    color:var(--muted);border-bottom:2px solid var(--line);padding:8px;vertical-align:bottom;
  }
  td{padding:9px 8px;border-bottom:1px solid var(--line);vertical-align:top;overflow-wrap:anywhere}
  col.c-tw{width:28px} col.c-date{width:106px} col.c-body{width:185px} col.c-sym{width:215px}
  tr.rec{cursor:pointer}
  tr.rec:hover td{background:#f2f7fc}
  tr.rec.open td{background:#eaf2fa}
  td.tw{color:var(--accent);text-align:center}
  td.tw span{display:inline-block}
  tr.rec.open td.tw span{transform:rotate(90deg)}
  .body{font-weight:600}
  .mech{font-size:.78rem;color:var(--muted)}
  a.sym{color:var(--accent);font-weight:600;text-decoration:none;word-break:break-all}
  a.sym:hover{text-decoration:underline}
  td.txt{color:#33414f}
  tr.detail td{background:#fbfdff;padding:14px 16px}
  .fulltext{
    white-space:pre-wrap;background:#f4f8fc;border-left:3px solid var(--accent);
    padding:10px 12px;border-radius:0 6px 6px 0;font-size:.95rem;
  }
  .meta{margin-top:10px;font-size:.85rem;color:var(--muted)}
  .pills{display:flex;flex-wrap:wrap;gap:6px;margin-top:6px}
  .pill{background:#eef3f8;border:1px solid var(--line);border-radius:999px;padding:2px 10px;font-size:.8rem;color:#33414f}
  .pill.sdg{background:#eaf2fa;color:var(--accent-dark);border-color:#cfe2f2}
  .doclink{display:inline-block;margin-top:10px;color:var(--accent);font-weight:600;text-decoration:none}
  .doclink:hover{text-decoration:underline}
  /* who-recommends-what tab */
  #sdgTbl col.c-state{width:26%} #sdgTbl col.c-n{width:150px}
  #sdgTbl tbody tr{cursor:pointer}
  #sdgTbl tbody tr:hover td{background:#f2f7fc}
  #sdgTbl tbody tr.sel td{background:#eaf2fa;font-weight:600}
  .sdgline{font-size:.9rem}
  details.rec-item{border-bottom:1px solid var(--line)}
  details.rec-item summary{
    cursor:pointer;list-style:none;padding:10px 6px;display:flex;gap:10px;align-items:baseline;flex-wrap:wrap;
  }
  details.rec-item summary::-webkit-details-marker{display:none}
  details.rec-item summary::before{content:"▸";color:var(--accent);flex:0 0 auto}
  details.rec-item[open] summary::before{content:"▾"}
  details.rec-item summary:hover{background:#f2f7fc}
  .s-sym{font-weight:600}
  .s-sym a{color:var(--accent);text-decoration:none;word-break:break-all}
  .s-sym a:hover{text-decoration:underline}
  .s-date{color:var(--muted);font-size:.88rem;white-space:nowrap}
  .s-line{color:#33414f;flex:1;min-width:240px}
  details.rec-item .inner{padding:0 6px 14px 26px}
</style>
</head>
<body>

<header class="wrap">
  <h1 id="title">UN human rights recommendations dashboard</h1>
  <p class="desc" id="desc"></p>
  <div class="stats">
    <div class="stat"><span class="num" id="statN">–</span><span class="lbl">records</span></div>
    <div class="stat"><span class="num" id="statYears">–</span><span class="lbl">years covered</span></div>
    <div class="stat wide"><span class="lbl">records by mechanism</span><span class="chips" id="statMech"></span></div>
  </div>
  <p class="note" id="statsNote"></p>
  <nav class="tabs" aria-label="Views">
    <button class="tab active" data-tab="dash" type="button">Dashboard</button>
    <button class="tab" data-tab="who" type="button">Who recommends what</button>
  </nav>
</header>

<main class="wrap">

  <!-- ============ TAB 1: DASHBOARD ============ -->
  <div id="tab-dash">

    <section class="card">
      <h2>Filters</h2>
      <p class="note">All filters combine (AND). The chart and table below react to every change.</p>
      <div class="fgrid">
        <label class="f">Mechanism
          <select id="fMech"></select>
        </label>
        <label class="f">Treaty body / mandate
          <select id="fBody"></select>
        </label>
        <label class="f">Year from
          <select id="fFrom"></select>
        </label>
        <label class="f">Year to
          <select id="fTo"></select>
        </label>
        <label class="f">SDG
          <select id="fSdg"></select>
        </label>
      </div>
      <div class="frow">
        <label class="f">Keyword search (text, symbol, theme, SDG target…)
          <input type="search" id="kw" placeholder="e.g. education, torture, women, birth registration…">
        </label>
        <button class="act" id="reset" type="button">Reset filters</button>
      </div>
      <p class="showing" id="showing"></p>
    </section>

    <section class="card">
      <h2>10 most frequent themes among the matching records</h2>
      <p class="note" id="chartNote"></p>
      <div class="chartbox" id="chartBox"><canvas id="chart"></canvas></div>
      <p class="empty" id="chartEmpty" hidden>No themes are tagged on the matching records.</p>
    </section>

    <section class="card">
      <h2>Matching records</h2>
      <p class="note">How this is computed: the records matching all filters above, sorted by date, newest first.
        The text column shows the first line of the paragraph; click any row to read the full text exactly as it appears in the UN document.</p>
      <table id="tbl">
        <colgroup>
          <col class="c-tw"><col class="c-date"><col class="c-body"><col class="c-sym"><col>
        </colgroup>
        <thead>
          <tr><th></th><th>Date</th><th>Body / mechanism</th><th>Symbol (UN document)</th><th>Text (first line)</th></tr>
        </thead>
        <tbody id="tbody"></tbody>
      </table>
      <p class="empty" id="tblEmpty" hidden>No records match the current filters. Try widening the year range or clearing the keyword.</p>
    </section>

  </div>

  <!-- ============ TAB 2: WHO RECOMMENDS WHAT ============ -->
  <div id="tab-who" hidden>

    <section class="card">
      <h2>Recommending States in UPR recommendations to <span id="whoCountry"></span></h2>
      <p class="note" id="whoNote"></p>
      <div class="stats">
        <div class="stat"><span class="num" id="whoN">–</span><span class="lbl">UPR recommendations</span></div>
        <div class="stat"><span class="num" id="whoWith">–</span><span class="lbl">with a State in parentheses</span></div>
        <div class="stat"><span class="num" id="whoWithout">–</span><span class="lbl">with no State in parentheses</span></div>
      </div>
      <p class="note" id="whoMissing"></p>
      <h2 style="margin-top:18px">15 States that made the most UPR recommendations — click a bar to list them</h2>
      <p class="note" id="whoChartNote"></p>
      <div class="chartbox" id="whoChartBox"><canvas id="whoChart"></canvas></div>
      <p class="empty" id="whoChartEmpty" hidden></p>
    </section>

    <section class="card">
      <h2>SDGs most raised by the top 15 recommending States — click a row to list them</h2>
      <p class="note" id="sdgNote"></p>
      <table id="sdgTbl">
        <colgroup><col class="c-state"><col class="c-n"><col></colgroup>
        <thead>
          <tr><th>Recommending State</th><th>UPR recommendations</th><th>Most-raised SDGs (with counts)</th></tr>
        </thead>
        <tbody id="sdgBody"></tbody>
      </table>
      <p class="empty" id="sdgEmpty" hidden>No UPR recommendations with a recommending State were found in the dataset.</p>
    </section>

    <section class="card" id="stateDetailCard" hidden>
      <h2 id="stateDetailTitle"></h2>
      <p class="note" id="stateDetailNote"></p>
      <div id="stateList"></div>
    </section>

  </div>

</main>

<script>
(function(){
  "use strict";

  var U = (window.WORKSHOP_DATA && window.WORKSHOP_DATA.uhri) || {};
  var recs = Array.isArray(U.records) ? U.records : [];
  var country = U.country || "the reviewed country";
  var sdgNames = U.sdg_names || {};

  function $(id){ return document.getElementById(id); }
  function esc(s){
    return String(s == null ? "" : s).replace(/[&<>"']/g, function(c){
      return {"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c];
    });
  }
  function uniqSorted(vals){
    var seen = {}, out = [];
    vals.forEach(function(v){
      if(v === null || v === undefined || v === "") return;
      var k = String(v);
      if(!seen[k]){ seen[k] = 1; out.push(k); }
    });
    return out.sort(function(a,b){ return a.localeCompare(b); });
  }
  function yearsOf(){
    var s = {}, out = [];
    recs.forEach(function(r){
      if(typeof r.year === "number" && !s[r.year]){ s[r.year] = 1; out.push(r.year); }
    });
    return out.sort(function(a,b){ return a - b; });
  }
  function firstLine(t){
    if(!t) return "";
    var lines = String(t).split("\n"), line = "";
    for(var i = 0; i < lines.length; i++){
      if(lines[i].trim()){ line = lines[i].trim(); break; }
    }
    if(!line) line = String(t).replace(/\s+/g, " ").trim();
    return line.length > 220 ? line.slice(0, 220).replace(/\s+\S*$/, "") + " …" : line;
  }
  function pills(items, cls){
    if(!items || !items.length) return "";
    return '<div class="pills">' + items.map(function(t){
      return '<span class="pill ' + (cls || "") + '">' + esc(t) + "</span>";
    }).join("") + "</div>";
  }
  function symLink(r){
    if(!r.symbol) return "—";
    return r.doc_url
      ? '<a href="' + esc(r.doc_url) + '" target="_blank" rel="noopener">' + esc(r.symbol) + "</a>"
      : esc(r.symbol);
  }

  /* ---------- header ---------- */
  var years = yearsOf();
  $("title").textContent = "UN human rights recommendations dashboard";
  $("whoCountry").textContent = country;

  var desc = esc(U.title || "UN Human Rights Recommendations Index (UHRI)");
  if(U.source){
    desc += " — source: " + (U.source_url
      ? '<a href="' + esc(U.source_url) + '" target="_blank" rel="noopener">' + esc(U.source) + "</a>"
      : esc(U.source));
  }
  desc += " · n = " + recs.length + " records addressed to " + esc(country);
  if(U.count != null && U.count !== recs.length) desc += " (source reports " + esc(U.count) + ")";
  desc += years.length ? " · years " + years[0] + "–" + years[years.length - 1] : " · no year information in the data";
  if(U.built) desc += " · dataset built " + esc(U.built);
  $("desc").innerHTML = desc;

  $("statN").textContent = recs.length;
  $("statYears").textContent = years.length ? years[0] + "–" + years[years.length - 1] : "—";

  var mechCounts = {};
  recs.forEach(function(r){
    var m = r.mechanism || "(unspecified)";
    mechCounts[m] = (mechCounts[m] || 0) + 1;
  });
  $("statMech").innerHTML = Object.keys(mechCounts).sort(function(a,b){
    return mechCounts[b] - mechCounts[a] || a.localeCompare(b);
  }).map(function(m){
    return '<span class="chip">' + esc(m) + " · " + mechCounts[m] + "</span>";
  }).join("");

  $("statsNote").textContent =
    "How this is computed: one record = one paragraph of a UN document addressed to " + country +
    ". n counts all records in the dataset; the year range uses each record's year field (records without a year are left out of the range). " +
    "Mechanism chips count records per mechanism. Nothing here is estimated.";

  /* ---------- tabs ---------- */
  var whoBuilt = false;
  document.querySelectorAll(".tab").forEach(function(b){
    b.addEventListener("click", function(){
      document.querySelectorAll(".tab").forEach(function(x){ x.classList.toggle("active", x === b); });
      var who = b.dataset.tab === "who";
      $("tab-dash").hidden = who;
      $("tab-who").hidden = !who;
      if(who) buildWho();
    });
  });

  /* ---------- dashboard filters ---------- */
  var state = { mech:"", body:"", yFrom:"", yTo:"", sdg:"", kw:"" };

  function fillSelect(sel, options, allLabel){
    sel.innerHTML = "";
    var o0 = document.createElement("option");
    o0.value = ""; o0.textContent = allLabel;
    sel.appendChild(o0);
    options.forEach(function(o){
      var op = document.createElement("option");
      op.value = o.v; op.textContent = o.l;
      sel.appendChild(op);
    });
  }

  fillSelect($("fMech"), uniqSorted(recs.map(function(r){ return r.mechanism; }))
    .map(function(v){ return {v:v, l:v}; }), "All mechanisms");
  fillSelect($("fBody"), uniqSorted(recs.map(function(r){ return r.body; }))
    .map(function(v){ return {v:v, l:v}; }), "All treaty bodies / mandates");
  fillSelect($("fFrom"), years.map(function(y){ return {v:String(y), l:String(y)}; }), "From (earliest)");
  fillSelect($("fTo"), years.map(function(y){ return {v:String(y), l:String(y)}; }), "To (latest)");

  var sdgKeys = {}, allSdgs = [];
  Object.keys(sdgNames).forEach(function(k){
    var n = Number(k);
    if(!isNaN(n) && !sdgKeys[n]){ sdgKeys[n] = 1; allSdgs.push(n); }
  });
  recs.forEach(function(r){
    (r.sdgs || []).forEach(function(s){
      var n = Number(s);
      if(!isNaN(n) && !sdgKeys[n]){ sdgKeys[n] = 1; allSdgs.push(n); }
    });
  });
  allSdgs.sort(function(a,b){ return a - b; });
  fillSelect($("fSdg"), allSdgs.map(function(n){
    var name = sdgNames[String(n)];
    return {v:String(n), l:"SDG " + n + (name ? " — " + name : "")};
  }), "All SDGs");

  $("fMech").addEventListener("change", function(e){ state.mech = e.target.value; update(); });
  $("fBody").addEventListener("change", function(e){ state.body = e.target.value; update(); });
  $("fFrom").addEventListener("change", function(e){ state.yFrom = e.target.value; update(); });
  $("fTo").addEventListener("change", function(e){ state.yTo = e.target.value; update(); });
  $("fSdg").addEventListener("change", function(e){ state.sdg = e.target.value; update(); });
  $("kw").addEventListener("input", function(e){ state.kw = e.target.value; update(); });
  $("reset").addEventListener("click", function(){
    state.mech = state.body = state.yFrom = state.yTo = state.sdg = state.kw = "";
    ["fMech","fBody","fFrom","fTo","fSdg"].forEach(function(id){ $(id).value = ""; });
    $("kw").value = "";
    update();
  });

  function filtered(){
    var kw = state.kw.trim().toLowerCase();
    return recs.filter(function(r){
      if(state.mech && r.mechanism !== state.mech) return false;
      if(state.body && (r.body || "") !== state.body) return false;
      if(state.yFrom || state.yTo){
        if(typeof r.year !== "number") return false;
        if(state.yFrom && r.year < Number(state.yFrom)) return false;
        if(state.yTo && r.year > Number(state.yTo)) return false;
      }
      if(state.sdg){
        var sdgs = (r.sdgs || []).map(Number);
        if(sdgs.indexOf(Number(state.sdg)) === -1) return false;
      }
      if(kw){
        var hay = [r.text, r.symbol, r.body, r.mechanism, r.type, r.section,
                   (r.themes || []).join(" "), (r.sdg_targets || []).join(" "),
                   (r.affected_persons || []).join(" ")].join(" ").toLowerCase();
        if(hay.indexOf(kw) === -1) return false;
      }
      return true;
    });
  }

  /* ---------- dashboard chart ---------- */
  var chart = null;
  function themeCounts(list){
    var m = {};
    list.forEach(function(r){
      (r.themes || []).forEach(function(t){
        if(t) m[t] = (m[t] || 0) + 1;
      });
    });
    return Object.keys(m).map(function(k){ return [k, m[k]]; })
      .sort(function(a,b){ return b[1] - a[1] || a[0].localeCompare(b[0]); })
      .slice(0, 10);
  }

  function renderChart(list){
    var data = themeCounts(list);
    var labels = data.map(function(d){ return d[0]; });
    var vals = data.map(function(d){ return d[1]; });

    $("chartNote").textContent =
      "How this is computed: among the " + list.length + " record(s) matching the filters above, each record is counted once per theme it carries " +
      "(a record can carry several themes, so theme counts can add up to more than " + list.length + "). The 10 most frequent themes are shown; ties are ordered alphabetically. Counted in the browser from the dataset — not estimated.";

    var has = data.length > 0;
    $("chartEmpty").hidden = has;
    $("chartBox").style.display = has ? "block" : "none";
    if(!has) return;

    $("chartBox").style.height = Math.max(200, labels.length * 38 + 70) + "px";

    if(!window.Chart){
      $("chartEmpty").hidden = false;
      $("chartEmpty").textContent = "Chart.js is not available in this environment; the theme counts could not be drawn.";
      return;
    }
    if(!chart){
      chart = new Chart($("chart").getContext("2d"), {
        type: "bar",
        data: {
          labels: labels,
          datasets: [{
            label: "matching records",
            data: vals,
            backgroundColor: "#1f6fb2",
            hoverBackgroundColor: "#175a94",
            borderRadius: 3
          }]
        },
        options: {
          indexAxis: "y",
          maintainAspectRatio: false,
          plugins: {
            legend: { display: false },
            tooltip: {
              callbacks: {
                label: function(c){
                  var n = c.parsed.x;
                  return " " + n + (n === 1 ? " record" : " records");
                }
              }
            }
          },
          scales: {
            x: {
              beginAtZero: true,
              ticks: { precision: 0 },
              title: { display: true, text: "matching records" }
            },
            y: { ticks: { autoSkip: false, font: { size: 13 } } }
          }
        }
      });
    } else {
      chart.data.labels = labels;
      chart.data.datasets[0].data = vals;
      chart.update();
    }
  }

  /* ---------- dashboard table ---------- */
  function renderTable(list){
    var tb = $("tbody");
    tb.innerHTML = "";
    var has = list.length > 0;
    $("tblEmpty").hidden = has;
    $("tbl").style.display = has ? "table" : "none";
    if(!has) return;

    var sorted = list.slice().sort(function(a,b){
      var da = a.date || "", db = b.date || "";
      if(da !== db) return db.localeCompare(da);
      return String(b.symbol || "").localeCompare(String(a.symbol || ""));
    });

    sorted.forEach(function(r){
      var tr = document.createElement("tr");
      tr.className = "rec";
      var dateTxt = r.date || (typeof r.year === "number" ? String(r.year) : "—");
      var sub = [r.mechanism, r.type].filter(Boolean).join(" · ") || "—";
      tr.innerHTML =
        '<td class="tw"><span>▸</span></td>' +
        '<td>' + esc(dateTxt) + "</td>" +
        '<td><div class="body">' + esc(r.body || "—") + '</div><div class="mech">' + esc(sub) + "</div></td>" +
        '<td><span class="sym">' + symLink(r) + "</span></td>" +
        '<td class="txt">' + esc(firstLine(r.text)) + "</td>";
      tb.appendChild(tr);

      var det = document.createElement("tr");
      det.className = "detail";
      det.hidden = true;
      var meta = [];
      if(r.section) meta.push("Section: " + r.section);
      if(r.year) meta.push("Year: " + r.year);
      det.innerHTML = '<td colspan="5">' +
        '<div class="fulltext">' + esc(r.text || "(no text in the dataset)") + "</div>" +
        (meta.length ? '<div class="meta">' + esc(meta.join(" · ")) + "</div>" : "") +
        pills(r.themes) +
        pills(r.sdg_targets, "sdg") +
        pills(r.affected_persons) +
        (r.doc_url ? '<a class="doclink" href="' + esc(r.doc_url) + '" target="_blank" rel="noopener">Open the UN document (' + esc(r.symbol || "symbol") + ") ↗</a>" : "") +
        "</td>";
      tb.appendChild(det);
    });
  }

  $("tbody").addEventListener("click", function(e){
    var tr = e.target.closest ? e.target.closest("tr.rec") : null;
    if(!tr) return;
    var det = tr.nextElementSibling;
    if(!det || !det.classList.contains("detail")) return;
    var open = det.hidden;
    det.hidden = !open;
    tr.classList.toggle("open", open);
  });

  function update(){
    var list = filtered();
    $("showing").textContent = "Showing " + list.length + " of " + recs.length + " records";
    renderChart(list);
    renderTable(list);
  }

  /* ================= TAB 2: WHO RECOMMENDS WHAT ================= */

  // Recommending State = text inside the last parentheses at the end of the recommendation
  function recommendingState(text){
    if(!text) return null;
    var t = String(text).trim();
    var m = t.match(/\(([^()]*)\)\s*\.?\s*$/);
    if(!m) return null;
    var s = m[1].trim();
    return s || null;
  }

  var uprRecs = recs.filter(function(r){
    return r.mechanism === "Universal Periodic Review" && (!r.type || /recommend/i.test(r.type));
  });

  var byState = {}, noState = 0;
  uprRecs.forEach(function(r){
    var s = recommendingState(r.text);
    if(!s){ noState++; return; }
    (byState[s] = byState[s] || []).push(r);
  });

  var topStates = Object.keys(byState).map(function(k){ return [k, byState[k].length]; })
    .sort(function(a,b){ return b[1] - a[1] || a[0].localeCompare(b[0]); })
    .slice(0, 15);

  var whoChart = null, selectedState = null;

  function sdgLabel(n){
    var name = sdgNames[String(n)];
    return "SDG " + n + (name ? " — " + name : "");
  }

  function topSdgsFor(stateName){
    var m = {};
    byState[stateName].forEach(function(r){
      (r.sdgs || []).forEach(function(s){
        var n = Number(s);
        if(!isNaN(n)) m[n] = (m[n] || 0) + 1;
      });
    });
    return Object.keys(m).map(function(k){ return [Number(k), m[k]]; })
      .sort(function(a,b){ return b[1] - a[1] || a[0] - b[0]; })
      .slice(0, 3);
  }

  function renderSdgTable(){
    var tb = $("sdgBody");
    tb.innerHTML = "";
    var has = topStates.length > 0;
    $("sdgEmpty").hidden = has;
    $("sdgTbl").style.display = has ? "table" : "none";
    if(!has) return;
    topStates.forEach(function(pair){
      var name = pair[0], n = pair[1];
      var sdgs = topSdgsFor(name);
      var sdgTxt = sdgs.length
        ? sdgs.map(function(d){ return esc(sdgLabel(d[0])) + " (" + d[1] + ")"; }).join("; ")
        : "no SDG tagged";
      var tr = document.createElement("tr");
      if(name === selectedState) tr.className = "sel";
      tr.innerHTML =
        "<td>" + esc(name) + "</td>" +
        "<td>" + n + "</td>" +
        '<td class="sdgline">' + sdgTxt + "</td>";
      tr.addEventListener("click", function(){ selectState(name); });
      tb.appendChild(tr);
    });
  }

  function renderWhoChart(){
    var labels = topStates.map(function(d){ return d[0]; });
    var vals = topStates.map(function(d){ return d[1]; });
    var has = labels.length > 0;
    $("whoChartEmpty").hidden = has;
    $("whoChartBox").style.display = has ? "block" : "none";
    if(!has){
      $("whoChartEmpty").textContent = "No UPR recommendations with a recommending State were found in the dataset.";
      return;
    }
    $("whoChartBox").style.height = Math.max(220, labels.length * 36 + 70) + "px";
    if(!window.Chart){
      $("whoChartEmpty").hidden = false;
      $("whoChartEmpty").textContent = "Chart.js is not available in this environment; the State counts could not be drawn.";
      return;
    }
    var opts = {
      indexAxis: "y",
      maintainAspectRatio: false,
      onClick: function(evt, elements){
        if(elements && elements.length){
          selectState(topStates[elements[0].index][0]);
        }
      },
      plugins: {
        legend: { display: false },
        tooltip: {
          callbacks: {
            label: function(c){
              var n = c.parsed.x;
              return " " + n + (n === 1 ? " UPR recommendation" : " UPR recommendations");
            }
          }
        }
      },
      scales: {
        x: {
          beginAtZero: true,
          ticks: { precision: 0 },
          title: { display: true, text: "UPR recommendations to " + country }
        },
        y: { ticks: { autoSkip: false, font: { size: 13 } } }
      }
    };
    if(!whoChart){
      whoChart = new Chart($("whoChart").getContext("2d"), {
        type: "bar",
        data: {
          labels: labels,
          datasets: [{
            label: "UPR recommendations",
            data: vals,
            backgroundColor: "#1f6fb2",
            hoverBackgroundColor: "#175a94",
            borderRadius: 3
          }]
        },
        options: opts
      });
    } else {
      whoChart.data.labels = labels;
      whoChart.data.datasets[0].data = vals;
      whoChart.options = opts;
      whoChart.update();
      whoChart.resize();
    }
  }

  function selectState(name){
    selectedState = name;
    renderSdgTable();
    var card = $("stateDetailCard");
    card.hidden = false;
    $("stateDetailTitle").textContent = "UPR recommendations by " + name + " to " + country;
    var list = byState[name] || [];
    $("stateDetailNote").textContent =
      "How this is computed: all " + list.length + " UPR recommendation(s) to " + country +
      " whose text ends with \"(" + name + ")\" in the final parentheses, sorted by date, newest first. " +
      "Click a row to read the full paragraph exactly as it appears in the UN document; the symbol links to the document.";
    var sorted = list.slice().sort(function(a,b){
      var da = a.date || "", db = b.date || "";
      if(da !== db) return db.localeCompare(da);
      return String(b.symbol || "").localeCompare(String(a.symbol || ""));
    });
    $("stateList").innerHTML = sorted.map(function(r){
      var dateTxt = r.date || (typeof r.year === "number" ? String(r.year) : "—");
      return '<details class="rec-item">' +
        "<summary>" +
          '<span class="s-sym">' + symLink(r) + "</span>" +
          '<span class="s-date">' + esc(dateTxt) + (r.body ? " · " + esc(r.body) : "") + "</span>" +
          '<span class="s-line">' + esc(firstLine(r.text)) + "</span>" +
        "</summary>" +
        '<div class="inner">' +
          '<div class="fulltext">' + esc(r.text || "(no text in the dataset)") + "</div>" +
          (r.section ? '<div class="meta">Section: ' + esc(r.section) + "</div>" : "") +
          pills(r.themes) +
          pills(r.sdg_targets, "sdg") +
          pills(r.affected_persons) +
          (r.doc_url ? '<a class="doclink" href="' + esc(r.doc_url) + '" target="_blank" rel="noopener">Open the UN document (' + esc(r.symbol || "symbol") + ") ↗</a>" : "") +
        "</div>" +
      "</details>";
    }).join("");
    card.scrollIntoView();
  }

  function buildWho(){
    $("whoN").textContent = uprRecs.length;
    $("whoWith").textContent = uprRecs.length - noState;
    $("whoWithout").textContent = noState;

    $("whoNote").textContent =
      "How this is computed: only records with mechanism \"Universal Periodic Review\" (type Recommendations) are used — n = " + uprRecs.length +
      " of " + recs.length + " records in the dataset, independent of the filters on the Dashboard tab. " +
      "The recommending State is read from the last parentheses at the end of the recommendation text (UPR recommendations end e.g. \"…for all children (Croatia).\"). " +
      "Counted in the browser from the dataset — not estimated.";

    $("whoMissing").textContent =
      noState > 0
        ? noState + " of the " + uprRecs.length + " UPR recommendations had no State in parentheses at the end of the text; they are not attributed to any State and are left out of the chart and tables below."
        : "All " + uprRecs.length + " UPR recommendations had a State in parentheses at the end of the text.";

    $("whoChartNote").textContent =
      "How this is computed: each UPR recommendation is attributed to the State named in its final parentheses; the 15 States with the most recommendations are shown (ties ordered alphabetically). " +
      "The " + noState + " recommendation(s) without a State in parentheses are not counted here. Click a bar to see that State's recommendations below.";

    $("sdgNote").textContent =
      "How this is computed: for each of the 15 States above, SDGs are counted across all of that State's UPR recommendations to " + country +
      " (one recommendation can raise several SDGs, so counts can exceed the number of recommendations). The up to 3 most-raised SDGs are shown with their counts; SDG names come from the dataset's sdg_names. Click a row to list that State's recommendations.";

    renderWhoChart();
    renderSdgTable();
    if(selectedState && byState[selectedState]) selectState(selectedState);
    whoBuilt = true;
  }

  update();
})();
</script>
</body>
</html>
```