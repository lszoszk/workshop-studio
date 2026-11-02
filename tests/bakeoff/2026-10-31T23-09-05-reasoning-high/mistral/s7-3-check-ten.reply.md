I added a "Spot-check" card below the table: "Check 10 at random" draws a random sample (Math.random, noted on screen) from the records matching the current filters, shows each record's full text plus the SDGs/targets the UN index assigned, and offers Right / Wrong / Arguable buttons per record. Once all are marked it shows the agreement rate with a "how this is computed" note, lists the wrong and arguable examples with linked symbols, and enables a CSV download of the 10 records with your marks (built in-browser as a Blob, no network). "Draw again" re-samples and resets the marks.

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
    padding:10px 12px;border-radius:0 6px 6px 0;font-size:.95rem;margin-top:8px;
  }
  .meta{margin-top:10px;font-size:.85rem;color:var(--muted)}
  .pills{display:flex;flex-wrap:wrap;gap:6px;margin-top:6px}
  .pill{background:#eef3f8;border:1px solid var(--line);border-radius:999px;padding:2px 10px;font-size:.8rem;color:#33414f}
  .pill.sdg{background:#eaf2fa;color:var(--accent-dark);border-color:#cfe2f2}
  .doclink{display:inline-block;margin-top:10px;color:var(--accent);font-weight:600;text-decoration:none}
  .doclink:hover{text-decoration:underline}
  /* spot-check */
  .spot-item{border:1px solid var(--line);border-radius:8px;padding:14px 16px;margin-top:14px;background:#fbfdff}
  .spot-head{display:flex;flex-wrap:wrap;gap:10px;align-items:baseline}
  .marks{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin-top:12px}
  .marks .lbl{font-size:.85rem;color:var(--muted);margin-right:4px}
  .mbtn{font:inherit;font-size:.88rem;padding:6px 14px;border:1px solid var(--line);background:#fff;color:var(--ink);border-radius:999px;cursor:pointer}
  .mbtn:hover{border-color:var(--accent);color:var(--accent)}
  .mbtn.sel{background:var(--accent);border-color:var(--accent);color:#fff}
  .markstate{font-size:.85rem;color:var(--accent-dark);font-weight:600}
  #spotSummary h3{font-size:1rem;margin:18px 0 6px}
  details{margin-top:10px}
  summary{cursor:pointer;color:var(--accent);font-size:.88rem}
  #csvBtn{margin-top:14px}
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
    <p class="note">All filters combine (AND). The chart, the table and the random spot-check below all use the current filter.</p>
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

  <section class="card" id="spotCard">
    <h2>Spot-check 10 random records</h2>
    <p class="note">Draws up to 10 records at random (Math.random — a fresh, non-reproducible sample each time) from the records
      matching the filters above. For each record, read the full text and the SDGs the UN index assigned to it, then mark them
      Right, Wrong or Arguable. You can change a mark at any time. When every drawn record is marked, the agreement rate,
      the wrong/arguable examples and a CSV download appear below.</p>
    <div class="frow">
      <button id="drawBtn" type="button">Check 10 at random</button>
      <button id="redrawBtn" type="button" hidden>Draw again</button>
    </div>
    <p class="note" id="drawInfo"></p>
    <p class="showing" id="markProgress" hidden></p>
    <div id="spotList"></div>
    <div id="spotSummary" hidden>
      <h3>Result of the spot-check</h3>
      <p id="agreeRate"></p>
      <p class="note" id="agreeNote"></p>
      <div id="badExamples"></div>
      <button id="csvBtn" type="button">Download the drawn records with my marks (CSV)</button>
      <p class="note">The CSV is generated in your browser from the drawn records and your marks; nothing is sent anywhere.</p>
    </div>
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
  function sdgLabel(s){
    var nm = sdgNames[String(s)] || sdgNames[String(Number(s))];
    return "SDG " + s + (nm ? " — " + nm : "");
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

  /* ---------- table ---------- */
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

    var sorted = list.slice().sort(function(a,b){
      var da = a.date || "", db = b.date || "";
      if(da !== db) return db.localeCompare(da);
      return String(b.symbol || "").localeCompare(String(a.symbol || ""));
    });

    sorted.forEach(function(r){
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

  /* ---------- random spot-check ---------- */
  var drawn = [];        // [{rec, mark}]
  var drawnPool = 0;     // how many records matched the filter at draw time

  function sdgBlock(r){
    var sdgs = r.sdgs || [], targets = r.sdg_targets || [];
    if(!sdgs.length && !targets.length){
      return '<p class="note">The UN index assigned no SDGs to this record.</p>';
    }
    var h = '<div class="pills">' + sdgs.map(function(s){
      return '<span class="pill sdg">' + esc(sdgLabel(s)) + "</span>";
    }).join("") + "</div>";
    if(targets.length){
      h += '<div class="pills">' + targets.map(function(t){
        return '<span class="pill sdg">' + esc(t) + "</span>";
      }).join("") + "</div>";
    }
    return h;
  }

  function drawRandom(){
    var pool = filtered();
    drawnPool = pool.length;
    var arr = pool.slice();
    for(var i = arr.length - 1; i > 0; i--){
      var j = Math.floor(Math.random() * (i + 1));
      var t = arr[i]; arr[i] = arr[j]; arr[j] = t;
    }
    var n = Math.min(10, arr.length);
    drawn = arr.slice(0, n).map(function(r){ return {rec: r, mark: null}; });

    var info;
    if(!pool.length){
      info = "No records match the current filters — nothing to draw. Widen the filters and try again.";
    } else {
      info = "Drawn at random: " + n + " of the " + pool.length + " record(s) matching the filters when you clicked" +
             (pool.length < 10 ? " (fewer than 10 match, so all of them were drawn)." : ".");
    }
    $("drawInfo").textContent = info;
    $("redrawBtn").hidden = !pool.length ? true : false;
    $("spotSummary").hidden = true;
    renderSpot();
  }

  function renderSpot(){
    var list = $("spotList");
    list.innerHTML = "";
    drawn.forEach(function(d, i){
      var r = d.rec;
      var item = document.createElement("div");
      item.className = "spot-item";
      var sym = r.symbol
        ? (r.doc_url
            ? '<a class="sym" href="' + esc(r.doc_url) + '" target="_blank" rel="noopener">' + esc(r.symbol) + "</a>"
            : esc(r.symbol))
        : "—";
      item.innerHTML =
        '<div class="spot-head">' + sym +
          '<span class="mech">' + esc([r.date || r.year, r.body, r.mechanism, r.type].filter(Boolean).join(" · ")) + "</span>" +
        "</div>" +
        '<div class="fulltext">' + esc(r.text || "(no text in the dataset)") + "</div>" +
        '<div><span class="note">SDGs assigned by the UN index:</span>' + sdgBlock(r) + "</div>" +
        '<div class="marks"><span class="lbl">Mark the SDGs of this record:</span>' +
          '<button type="button" class="mbtn" data-idx="' + i + '" data-mark="right">Right</button>' +
          '<button type="button" class="mbtn" data-idx="' + i + '" data-mark="wrong">Wrong</button>' +
          '<button type="button" class="mbtn" data-idx="' + i + '" data-mark="arguable">Arguable</button>' +
          '<span class="markstate"></span>' +
        "</div>";
      list.appendChild(item);
    });
    paintMarks();
    refreshSummary();
  }

  function paintMarks(){
    var marked = 0;
    var items = $("spotList").children;
    drawn.forEach(function(d, i){
      if(d.mark) marked++;
      var item = items[i];
      if(!item) return;
      var btns = item.querySelectorAll(".mbtn");
      for(var k = 0; k < btns.length; k++){
        btns[k].classList.toggle("sel", btns[k].getAttribute("data-mark") === d.mark);
      }
      var ms = item.querySelector(".markstate");
      if(ms) ms.textContent = d.mark ? "Marked: " + d.mark : "";
    });
    var prog = $("markProgress");
    if(drawn.length){
      prog.hidden = false;
      prog.textContent = "Marked " + marked + " of " + drawn.length +
        (marked === drawn.length ? " — all marked, result below." : ".");
    } else {
      prog.hidden = true;
    }
  }

  $("spotList").addEventListener("click", function(e){
    var btn = e.target.closest ? e.target.closest(".mbtn") : null;
    if(!btn) return;
    var idx = Number(btn.getAttribute("data-idx"));
    if(!drawn[idx]) return;
    drawn[idx].mark = btn.getAttribute("data-mark");
    paintMarks();
    refreshSummary();
  });

  function refreshSummary(){
    var sum = $("spotSummary");
    if(!drawn.length || drawn.some(function(d){ return !d.mark; })){ sum.hidden = true; return; }

    var n = drawn.length;
    var right = drawn.filter(function(d){ return d.mark === "right"; }).length;
    var wrong = drawn.filter(function(d){ return d.mark === "wrong"; });
    var arguable = drawn.filter(function(d){ return d.mark === "arguable"; });
    var pct = Math.round(right / n * 1000) / 10;

    $("agreeRate").innerHTML = "Agreement rate: <strong>" + right + " of " + n + " drawn records marked “Right” (" +
      pct + "%)</strong> · Wrong: " + wrong.length + " · Arguable: " + arguable.length + ".";
    $("agreeNote").textContent =
      "How this is computed: agreement rate = records you marked “Right” ÷ the " + n + " drawn records. The sample was drawn at random " +
      "(Math.random) from the " + drawnPool + " record(s) that matched the filters when you clicked the button — it is your own marking of a " +
      "random sample, not a measured statistic about all " + recs.length + " records in the dataset.";

    var ex = wrong.concat(arguable);
    var h;
    if(!ex.length){
      h = '<p class="note">No drawn record was marked Wrong or Arguable.</p>';
    } else {
      h = "<h3>Wrong and arguable examples (" + ex.length + ")</h3>";
      ex.forEach(function(d){
        var r = d.rec;
        var sym = r.symbol
          ? (r.doc_url
              ? '<a class="sym" href="' + esc(r.doc_url) + '" target="_blank" rel="noopener">' + esc(r.symbol) + "</a>"
              : esc(r.symbol))
          : "—";
        h += '<div class="spot-item">' +
          '<div class="spot-head"><span class="chip">' + esc(d.mark) + '</span> ' + sym +
          ' <span class="mech">' + esc([r.date || r.year, r.body, r.mechanism].filter(Boolean).join(" · ")) + "</span></div>" +
          '<div class="pills">' + (r.sdgs || []).map(function(s){
            return '<span class="pill sdg">' + esc(sdgLabel(s)) + "</span>";
          }).join("") + "</div>" +
          "<details><summary>Full text of this record</summary><div class=\"fulltext\">" + esc(r.text || "") + "</div></details>" +
          "</div>";
      });
    }
    $("badExamples").innerHTML = h;
    sum.hidden = false;
  }

  function csvCell(v){
    var s = v == null ? "" : String(v);
    return '"' + s.replace(/"/g, '""') + '"';
  }

  $("csvBtn").addEventListener("click", function(){
    if(!drawn.length) return;
    var cols = ["id","symbol","doc_url","date","year","body","mechanism","type","section",
                "themes","sdgs_assigned_by_un_index","sdg_targets","affected_persons","text","my_mark"];
    var lines = [cols.join(",")];
    drawn.forEach(function(d){
      var r = d.rec;
      lines.push([
        r.id, r.symbol, r.doc_url, r.date, r.year, r.body, r.mechanism, r.type, r.section,
        (r.themes || []).join(" | "),
        (r.sdgs || []).map(sdgLabel).join(" | "),
        (r.sdg_targets || []).join(" | "),
        (r.affected_persons || []).join(" | "),
        r.text, d.mark
      ].map(csvCell).join(","));
    });
    var csv = "\uFEFF" + lines.join("\r\n"); // BOM so spreadsheet apps read UTF-8
    var blob = new Blob([csv], {type: "text/csv;charset=utf-8"});
    var url = URL.createObjectURL(blob);
    var a = document.createElement("a");
    var slug = country.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-+|-+$/g, "") || "country";
    a.href = url;
    a.download = "sdg-spotcheck-" + slug + "-" + new Date().toISOString().slice(0, 10) + ".csv";
    document.body.appendChild(a);
    a.click();
    a.remove();
    setTimeout(function(){ URL.revokeObjectURL(url); }, 1000);
  });

  $("drawBtn").addEventListener("click", drawRandom);
  $("redrawBtn").addEventListener("click", drawRandom);

  /* ---------- update ---------- */
  function update(){
    var list = filtered();
    $("showing").textContent = "Showing " + list.length + " of " + recs.length + " records";
    renderChart(list);
    renderTable(list);
    if(drawn.length){
      $("drawInfo").textContent += " The filters now match " + list.length +
        " record(s); the drawn sample above is from the filter as it was at draw time.";
    }
  }

  update();
})();
</script>
</body>
</html>
```