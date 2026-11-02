I built a single-file dashboard for the UHRI records addressed to the country named in the data: header stats (n, year range, mechanism breakdown), five working filters (mechanism, body/mandate, year range, SDG, keyword), a Chart.js bar chart of the top 10 themes under the current filter, and an expandable table where every row links its symbol to the UN document and shows the full paragraph on click. All counting and filtering is done in the browser from `WORKSHOP_DATA.uhri`, with "how this is computed" notes under each number.

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
    padding:10px 12px;border-radius:0 6px 6px 0;font-size:.95rem;
  }
  .meta{margin-top:10px;font-size:.85rem;color:var(--muted)}
  .pills{display:flex;flex-wrap:wrap;gap:6px;margin-top:6px}
  .pill{background:#eef3f8;border:1px solid var(--line);border-radius:999px;padding:2px 10px;font-size:.8rem;color:#33414f}
  .pill.sdg{background:#eaf2fa;color:var(--accent-dark);border-color:#cfe2f2}
  .doclink{display:inline-block;margin-top:10px;color:var(--accent);font-weight:600;text-decoration:none}
  .doclink:hover{text-decoration:underline}
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
      var html = '<td colspan="5">' +
        '<div class="fulltext">' + esc(r.text || "(no text in the dataset)") + "</div>" +
        (meta.length ? '<div class="meta">' + esc(meta.join(" · ")) + "</div>" : "") +
        pills(r.themes) +
        pills(r.sdg_targets, "sdg") +
        pills(r.affected_persons) +
        (r.doc_url ? '<a class="doclink" href="' + esc(r.doc_url) + '" target="_blank" rel="noopener">Open the UN document (' + esc(r.symbol || "symbol") + ") ↗</a>" : "") +
        "</td>";
      det.innerHTML = html;
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