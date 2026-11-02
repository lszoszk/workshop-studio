I added an "AI SDG suggestions" card between the chart and the records table: it takes the first 50 records of the current filter, sends them to `studio.ask` in batches of 25 with live progress and a Stop button, and renders each run (kept side by side on wide screens) with its agreement rate, a prominent notice that the texts left the browser for the external model, and a per-record table of UN vs. AI SDGs with exact-match agreement — all AI-returned values are wrapped in `data-source="ai"` amber cells.

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
    --line:#dfe6ee; --bg:#f4f7fa; --card:#ffffff; --ai:#d99a2b;
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
  code{background:#eef3f8;padding:1px 5px;border-radius:4px;font-size:.9em}
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
  button{
    font:inherit;padding:8px 18px;border:1px solid var(--accent);background:var(--accent);
    color:#fff;border-radius:7px;cursor:pointer;
  }
  button:hover{background:var(--accent-dark)}
  button.ghost{background:#fff;color:var(--accent)}
  button.ghost:hover{background:#eaf2fa}
  button:disabled{opacity:.55;cursor:not-allowed}
  .btnrow{display:flex;flex-wrap:wrap;gap:10px;margin-top:14px;align-items:center}
  .showing{margin:14px 0 0;font-weight:600}
  #aiStatus{margin:12px 0 0;font-size:.92rem;color:var(--muted)}
  #aiStatus.busy{color:var(--accent-dark);font-weight:600}
  [data-source="ai"]{background:#fdf3e0;box-shadow:inset 3px 0 0 var(--ai);padding:1px 6px;border-radius:3px}
  .runs{display:grid;grid-template-columns:1fr;gap:16px;margin-top:16px}
  @media(min-width:1150px){.runs{grid-template-columns:1fr 1fr}}
  .run{border:1px solid var(--line);border-radius:10px;padding:14px 16px;background:#fbfdff}
  .run h3{margin:0 0 6px;font-size:1rem}
  .agree{font-size:.95rem;margin:4px 0}
  .agree b{color:var(--accent-dark)}
  .notice{background:#fdf3e0;border:1px solid #ecd9ae;border-radius:8px;padding:9px 12px;font-size:.86rem;margin:10px 0}
  .runmeta{font-size:.82rem;color:var(--muted);margin:6px 0 0}
  table{width:100%;border-collapse:collapse;table-layout:fixed;margin-top:12px}
  table.ai{table-layout:auto}
  table.ai td{padding:7px 8px}
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
  .ok{color:#1a7f37;font-weight:700}
  .no{color:#b3261e;font-weight:700}
  .na{color:var(--muted)}
  .sdgcell{font-size:.86rem}
  .rec-sym{font-weight:600;color:var(--accent);text-decoration:none;word-break:break-all}
  .rec-sym:hover{text-decoration:underline}
  .rec-sub{font-size:.78rem;color:var(--muted)}
  .chartbox{position:relative;width:100%;margin-top:12px}
  .empty{color:var(--muted);font-style:italic;margin:14px 0 4px}
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
</header>

<main class="wrap">

  <section class="card">
    <h2>Filters</h2>
    <p class="note">All filters combine (AND). The chart, the table and the AI section below all react to every change.</p>
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
      <button id="reset" type="button">Reset filters</button>
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
    <h2>Suggest SDGs with AI</h2>
    <p class="note">This works on the <b>first 50 records of the current filter</b> (sorted newest first, like the table below).
      On click only — never on page load — their <b>full paragraph text is sent to an external language model</b> through
      <code>studio.ask</code>, in batches of at most 25 records per call, and the model is asked to return JSON mapping each record id
      to the SDG numbers it would assign. It is slow and each run may take a while; you can stop between batches.
      The comparison with the UN-tagged SDGs is computed here in the browser, exactly, not estimated.
      Amber cells marked <code>data-source="ai"</code> contain values returned by the model.</p>
    <div class="btnrow">
      <button id="btnAI" type="button">Suggest SDGs with AI</button>
      <button id="btnAgain" type="button" class="ghost" hidden>Run again (keep previous runs)</button>
      <button id="btnStop" type="button" class="ghost" hidden>Stop</button>
    </div>
    <p id="aiStatus"></p>
    <p class="showing" id="aiSummary" hidden></p>
    <div class="runs" id="runs"></div>
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
  function sortRecs(arr){
    return arr.slice().sort(function(a,b){
      var da = a.date || "", db = b.date || "";
      if(da !== db) return db.localeCompare(da);
      return String(b.symbol || "").localeCompare(String(a.symbol || ""));
    });
  }

  var state = { mech:"", body:"", yFrom:"", yTo:"", sdg:"", kw:"" };

  /* ---------- header ---------- */
  var years = yearsOf();
  $("title").textContent = "UN human rights recommendations & observations addressed to " + country;

  var desc = esc(U.title || "UN Human Rights Recommendations Index (UHRI)");
  if(U.source){
    desc += " — source: " + (U.source_url
      ? '<a href="' + esc(U.source_url) + '" target="_blank" rel="noopener">' + esc(U.source) + "</a>"
      : esc(U.source));
  }
  desc += " · n = " + recs.length + " records";
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

  /* ---------- filter controls ---------- */
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

  /* ---------- filtering ---------- */
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

  /* ---------- chart ---------- */
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

  /* ---------- records table ---------- */
  function pills(items, cls){
    if(!items || !items.length) return "";
    return '<div class="pills">' + items.map(function(t){
      return '<span class="pill ' + (cls || "") + '">' + esc(t) + "</span>";
    }).join("") + "</div>";
  }

  function renderTable(list){
    var tb = $("tbody");
    tb.innerHTML = "";
    var has = list.length > 0;
    $("tblEmpty").hidden = has;
    $("tbl").style.display = has ? "table" : "none";
    if(!has) return;

    sortRecs(list).forEach(function(r){
      var tr = document.createElement("tr");
      tr.className = "rec";
      var dateTxt = r.date || (typeof r.year === "number" ? String(r.year) : "—");
      var sym = r.symbol
        ? (r.doc_url
            ? '<a class="sym" href="' + esc(r.doc_url) + '" target="_blank" rel="noopener">' + esc(r.symbol) + "</a>"
            : '<span class="sym">' + esc(r.symbol) + "</span>")
        : "—";
      var sub = [r.mechanism, r.type].filter(Boolean).join(" · ") || "—";
      tr.innerHTML =
        '<td class="tw"><span>▸</span></td>' +
        '<td>' + esc(dateTxt) + "</td>" +
        '<td><div class="body">' + esc(r.body || "—") + '</div><div class="mech">' + esc(sub) + "</div></td>" +
        '<td>' + sym + "</td>" +
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

  /* ---------- AI SDG suggestions (only on user click) ---------- */
  var runs = [], running = false, stopFlag = false;
  var BATCH = 25, MAXREC = 50;

  function modelName(){
    var s = window.studio || {};
    return s.model || s.modelName || s.model_name || s.name ||
      "the language model exposed by this workshop as studio.ask (the API does not publish a model name)";
  }
  function filterDesc(){
    return "mechanism: " + (state.mech || "all") +
      " · body/mandate: " + (state.body || "all") +
      " · years: " + (state.yFrom || "any") + "–" + (state.yTo || "any") +
      " · SDG: " + (state.sdg || "all") +
      " · keyword: " + (state.kw.trim() || "none");
  }
  function sdgLabel(n){
    var nm = sdgNames[String(n)];
    return "SDG " + n + (nm ? " — " + nm : "");
  }
  function sdgCell(nums, fromAI){
    if(!nums || !nums.length) return '<span class="sdgcell na">— none tagged</span>';
    var inner = nums.map(function(n){ return "SDG " + n; }).join(", ");
    var tip = nums.map(sdgLabel).join("; ");
    if(fromAI) return '<span class="sdgcell" data-source="ai" title="' + esc(tip) + ' — returned by the external model via studio.ask">' + esc(inner) + "</span>";
    return '<span class="sdgcell" title="' + esc(tip) + '">' + esc(inner) + "</span>";
  }
  function buildPrompt(batch){
    var sdgList = Object.keys(sdgNames).sort(function(a,b){ return Number(a) - Number(b); })
      .map(function(k){ return "SDG " + k + " = " + sdgNames[k]; }).join("; ");
    var lines = batch.map(function(r){ return JSON.stringify({id: r.id, text: r.text || ""}); }).join("\n");
    return "You tag paragraphs of UN human rights documents with Sustainable Development Goals (SDGs).\n" +
      "Below are " + batch.length + " records; each line is a JSON object with \"id\" and \"text\" (one paragraph of a UN document addressed to " + country + ").\n" +
      "For each record, decide which SDGs the text relates to. Available SDGs: " + sdgList + ".\n" +
      "Reply with ONLY a JSON object mapping every given id to an array of SDG numbers (integers 1 to 17), e.g. {\"id-a\":[16,10],\"id-b\":[]}. Include every id. No prose, no markdown fences.\n\n" + lines;
  }
  function parseAnswer(ans){
    if(typeof ans !== "string") return null;
    var s = ans.trim().replace(/^```[a-z]*\s*/i, "").replace(/```\s*$/i, "").trim();
    var a = s.indexOf("{"), b = s.lastIndexOf("}");
    if(a < 0 || b <= a) return null;
    try {
      var o = JSON.parse(s.slice(a, b + 1));
      return (o && typeof o === "object" && !Array.isArray(o)) ? o : null;
    } catch(e){ return null; }
  }
  function sameSet(a, b){
    var x = a.slice().sort(function(p,q){ return p - q; }).join(",");
    var y = b.slice().sort(function(p,q){ return p - q; }).join(",");
    return x === y;
  }
  function agreeStats(run){
    var sent = run.list.length, answered = 0, match = 0;
    run.list.forEach(function(r){
      var v = run.results[r.id];
      if(!Array.isArray(v)) return;
      answered++;
      if(sameSet((r.sdgs || []).map(Number), v)) match++;
    });
    return {sent: sent, answered: answered, match: match};
  }

  function renderRuns(){
    var box = $("runs");
    box.innerHTML = "";
    runs.forEach(function(run, idx){
      var st = agreeStats(run);
      var pct = st.sent ? Math.round(100 * st.match / st.sent) : 0;
      var totalBatches = Math.ceil(run.list.length / BATCH);
      var statusTxt = run.status === "running"
        ? "running… batch " + run.batches + " of " + totalBatches + " sent, waiting for the model"
        : run.status === "stopped"
          ? "stopped by the user after " + run.batches + " of " + totalBatches + " batch(es)"
          : "done — " + run.batches + " of " + totalBatches + " batch(es) sent";
      var div = document.createElement("div");
      div.className = "run";
      div.innerHTML =
        "<h3>Run " + (idx + 1) + " · " + esc(run.time) + "</h3>" +
        '<div class="agree">Agreement rate: <b>' + st.match + " / " + st.sent + " records (" + pct + "%)</b> agree exactly" +
          (st.answered < st.sent ? " · the model returned a parseable SDG list for " + st.answered + " of " + st.sent + " records" : "") + "</div>" +
        '<p class="note">How this is computed: in the browser, each record’s UN-tagged SDG set is compared with the model-returned set; “agree” means exactly the same set of SDG numbers. Deterministic, not estimated.</p>' +
        '<p class="notice">⚠ <b>These texts left the browser:</b> on ' + esc(run.time) + ", the first " + run.list.length + " of " + run.matchCount +
          " record(s) matching the filter then active (" + esc(run.filterDesc) + ") were sent — full paragraph text included — to the external model <b>" +
          esc(run.model) + "</b> via <code>studio.ask</code>, in " + totalBatches + " batch(es) of at most " + BATCH +
          " records. The amber cells below (data-source=\"ai\") are that model’s answers. Language models are not deterministic: <b>running again can give different answers</b>.</p>" +
        '<p class="runmeta">Status: ' + esc(statusTxt) + (run.error ? " · " + esc(run.error) : "") + "</p>";
      var tbl = document.createElement("table");
      tbl.className = "ai";
      tbl.innerHTML = "<thead><tr><th>Record</th><th>UN’s SDGs</th><th>AI’s SDGs</th><th>Agree?</th></tr></thead>";
      var tb = document.createElement("tbody");
      run.list.forEach(function(r){
        var v = run.results[r.id];
        var sym = r.doc_url
          ? '<a class="rec-sym" href="' + esc(r.doc_url) + '" target="_blank" rel="noopener">' + esc(r.symbol || "(no symbol)") + "</a>"
          : esc(r.symbol || "(no symbol)");
        var agree;
        if(!Array.isArray(v)) agree = '<span class="na">' + (v === null ? "no answer" : "not sent") + "</span>";
        else agree = sameSet((r.sdgs || []).map(Number), v) ? '<span class="ok">Yes</span>' : '<span class="no">No</span>';
        var tr = document.createElement("tr");
        tr.innerHTML =
          "<td>" + sym + '<div class="rec-sub">' + esc(String(r.date || r.year || "")) + (r.body ? " · " + esc(r.body) : "") + "</div></td>" +
          "<td>" + sdgCell((r.sdgs || []).map(Number), false) + "</td>" +
          "<td>" + (Array.isArray(v) ? sdgCell(v, true) : '<span class="na">—</span>') + "</td>" +
          "<td>" + agree + "</td>";
        tb.appendChild(tr);
      });
      tbl.appendChild(tb);
      div.appendChild(tbl);
      box.appendChild(div);
    });
    var sum = $("aiSummary");
    if(runs.length){
      var last = runs[runs.length - 1], ls = agreeStats(last);
      var lpct = ls.sent ? Math.round(100 * ls.match / ls.sent) : 0;
      sum.hidden = false;
      sum.textContent = "Runs so far: " + runs.length + " · latest run agreement rate: " + ls.match + "/" + ls.sent + " (" + lpct + "%) exact matches";
    } else {
      sum.hidden = true;
    }
  }

  async function startRun(){
    if(running) return;
    var all = filtered();
    var list = sortRecs(all).slice(0, MAXREC);
    var st = $("aiStatus");
    if(!list.length){
      st.className = "";
      st.textContent = "No records match the current filter — nothing was sent.";
      return;
    }
    if(!window.studio || typeof window.studio.ask !== "function"){
      st.className = "";
      st.textContent = "studio.ask is not available in this environment — no text can be sent to a model.";
      return;
    }
    running = true; stopFlag = false;
    $("btnAI").disabled = true; $("btnAgain").disabled = true; $("btnStop").hidden = false;
    var run = {
      list: list, matchCount: all.length, time: new Date().toLocaleString(),
      filterDesc: filterDesc(), model: modelName(),
      results: {}, batches: 0, status: "running", error: ""
    };
    runs.push(run);
    $("btnAgain").hidden = false;
    var totalBatches = Math.ceil(list.length / BATCH);
    st.className = "busy";
    st.textContent = "Sending the first " + list.length + " of " + all.length + " matching record(s) — full text included — to the external model (" +
      run.model + ") via studio.ask. These texts are leaving the browser now, in " + totalBatches + " batch(es) of at most " + BATCH + " records.";
    renderRuns();
    for(var i = 0; i < list.length; i += BATCH){
      if(stopFlag) break;
      var batch = list.slice(i, i + BATCH);
      st.textContent = "Batch " + (run.batches + 1) + "/" + totalBatches + ": " + batch.length +
        " record texts sent to the model, waiting for the answer…";
      try {
        var ans = await window.studio.ask(buildPrompt(batch), {json: true});
        var parsed = parseAnswer(ans);
        run.batches++;
        batch.forEach(function(r){
          var v = parsed ? parsed[r.id] : undefined;
          run.results[r.id] = Array.isArray(v)
            ? v.map(Number).filter(function(n){ return isFinite(n) && n >= 1 && n <= 17; })
            : null;
        });
        if(!parsed) run.error = "at least one batch returned text that could not be parsed as JSON; its records are marked “no answer”.";
      } catch(err){
        run.batches++;
        run.error = "batch " + run.batches + " failed (" + String(err && err.message || err) + "); its records are marked “no answer”.";
        batch.forEach(function(r){ if(!(r.id in run.results)) run.results[r.id] = null; });
      }
      renderRuns();
    }
    run.status = (stopFlag && run.batches < totalBatches) ? "stopped" : "done";
    running = false;
    $("btnAI").disabled = false; $("btnAgain").disabled = false; $("btnStop").hidden = true;
    st.className = "";
    st.textContent = "Run " + runs.length + " " + run.status + ": " + run.batches + " batch(es) sent; " + list.length +
      " record texts went to the external model (see the notice inside the run). Running again can give different answers.";
    renderRuns();
  }

  $("btnAI").addEventListener("click", startRun);
  $("btnAgain").addEventListener("click", startRun);
  $("btnStop").addEventListener("click", function(){
    if(running){
      stopFlag = true;
      $("aiStatus").textContent = "Stopping after the current batch returns…";
    }
  });

  /* ---------- update ---------- */
  function update(){
    var list = filtered();
    $("showing").textContent = "Showing " + list.length + " of " + recs.length + " records";
    renderChart(list);
    renderTable(list);
  }

  update();
})();
</script>
</body>
</html>
```