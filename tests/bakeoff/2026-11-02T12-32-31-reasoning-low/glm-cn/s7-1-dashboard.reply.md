Here is the dashboard. It reads Kenya's records, filters them live, and shows a top-themes chart plus an expandable table of paragraphs. Build complete. (Two short sentences is the target — this is it.)

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>UN human rights recommendations</title>
<style>
  :root {
    --accent: #1f6fb2;
    --bg: #f7f9fb;
    --card: #ffffff;
    --border: #dfe6ec;
    --text: #22313f;
    --muted: #5a6b7b;
  }
  * { box-sizing: border-box; }
  body {
    margin: 0;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    background: var(--bg);
    color: var(--text);
    font-size: 16px;
    line-height: 1.5;
  }
  header {
    background: var(--card);
    border-bottom: 1px solid var(--border);
    padding: 28px 32px;
  }
  header h1 {
    margin: 0 0 6px 0;
    font-size: 26px;
    color: var(--accent);
  }
  header p { margin: 0; color: var(--muted); }
  main { max-width: 1100px; margin: 0 auto; padding: 24px 32px 48px; }

  .card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 6px;
    padding: 20px 24px;
    margin-bottom: 24px;
  }
  .card h2 { font-size: 18px; margin: 0 0 12px; }
  .note { font-size: 13px; color: var(--muted); margin-top: 10px; }

  .filters {
    display: flex;
    flex-wrap: wrap;
    gap: 12px;
    align-items: flex-end;
  }
  .filters label {
    display: flex;
    flex-direction: column;
    font-size: 13px;
    color: var(--muted);
    gap: 4px;
  }
  .filters select, .filters input[type="text"], .filters input[type="number"] {
    font: inherit;
    padding: 6px 8px;
    border: 1px solid var(--border);
    border-radius: 4px;
    background: #fff;
    color: var(--text);
    min-width: 120px;
  }
  .filters input[type="number"] { width: 90px; }
  .filters button {
    font: inherit;
    padding: 7px 18px;
    border: 1px solid var(--accent);
    background: var(--accent);
    color: #fff;
    border-radius: 4px;
    cursor: pointer;
  }
  .filters button:hover { background: #185a92; }

  #summaryline { margin: 4px 0 18px; color: var(--text); }
  #summaryline strong { color: var(--accent); }
  #filterdesc { color: var(--muted); font-size: 14px; }

  #chartbox { max-width: 100%; }
  .empty {
    padding: 28px;
    text-align: center;
    color: var(--muted);
    font-size: 16px;
  }

  table { width: 100%; border-collapse: collapse; }
  th, td {
    text-align: left;
    padding: 10px 10px;
    border-bottom: 1px solid var(--border);
    vertical-align: top;
    font-size: 15px;
  }
  th {
    font-size: 13px;
    text-transform: uppercase;
    letter-spacing: 0.04em;
    color: var(--muted);
    border-bottom: 2px solid var(--border);
  }
  tbody tr.row { cursor: pointer; }
  tbody tr.row:hover { background: #f0f6fb; }
  td.date { white-space: nowrap; color: var(--muted); }
  td.body { white-space: nowrap; }
  a.sym { color: var(--accent); text-decoration: none; }
  a.sym:hover { text-decoration: underline; }
  .nosym { color: var(--muted); font-style: italic; }
  td.text { max-width: 560px; }
  tr.expanded > td { background: #f0f6fb; }
  .fulltext { white-space: pre-wrap; margin: 0; }
  .tags { margin-top: 10px; font-size: 14px; }
  .tags div { margin-bottom: 4px; }
  .tags span { color: var(--muted); }
  .tagline { color: #33475a; }
  .actions { margin-top: 14px; text-align: center; }
  .actions button {
    font: inherit;
    padding: 8px 20px;
    border: 1px solid var(--accent);
    background: #fff;
    color: var(--accent);
    border-radius: 4px;
    cursor: pointer;
  }
  .actions button:hover { background: #f0f6fb; }
</style>
</head>
<body>
<header>
  <h1 id="title"></h1>
  <p id="subline"></p>
</header>
<main>
  <div class="card">
    <div class="filters" id="filters">
      <label>Mechanism
        <select id="f-mech"></select>
      </label>
      <label>Body
        <select id="f-body"></select>
      </label>
      <label>First year
        <input type="number" id="f-y1" min="1900" max="2100">
      </label>
      <label>Last year
        <input type="number" id="f-y2" min="1900" max="2100">
      </label>
      <label>SDG
        <select id="f-sdg"></select>
      </label>
      <label>Keyword
        <input type="text" id="f-kw" placeholder="e.g. torture">
      </label>
      <button id="f-reset" type="button">Reset</button>
    </div>
  </div>

  <p id="summaryline"></p>
  <p id="filterdesc"></p>

  <div class="card">
    <h2>Top themes</h2>
    <div id="chartbox"><canvas id="themechart"></canvas></div>
    <p class="note">The 10 most frequent themes among the matching records. A record with several themes is counted once for each theme. Records with no recorded theme do not appear in the chart.</p>
  </div>

  <div class="card">
    <h2>Records</h2>
    <div style="overflow-x:auto">
      <table id="table">
        <thead>
          <tr><th>Date</th><th>Body</th><th>Symbol</th><th>Text</th></tr>
        </thead>
        <tbody id="tbody"></tbody>
      </table>
    </div>
    <div id="nomatch" class="empty" hidden>No records match these filters.</div>
    <div class="actions">
      <button id="showmore" type="button" hidden>Show more</button>
    </div>
    <p class="note">Sorted newest first. Click a row to see the full paragraph, its themes and SDGs. Click a symbol to open the UN document in a new tab.</p>
  </div>
</main>

<script>
(function () {
  "use strict";

  var DATA = window.WORKSHOP_DATA && window.WORKSHOP_DATA.uhri;
  if (!DATA || !DATA.records) {
    document.getElementById("title").textContent = "No data loaded";
    document.getElementById("subline").textContent =
      "The recommendations file is not available in this session.";
    return;
  }

  var all = DATA.records.filter(function (r) {
    return r.type === "Recommendations" || r.type === "Concerns/Observations";
  });

  var country = DATA.country || "(unknown country)";
  var years = all.map(function (r) { return r.year; }).filter(function (y) { return typeof y === "number"; });
  var minY = years.length ? Math.min.apply(null, years) : "";
  var maxY = years.length ? Math.max.apply(null, years) : "";

  document.getElementById("title").textContent =
    "UN human rights recommendations to " + country;
  document.getElementById("subline").textContent =
    (DATA.source ? "Source: " + DATA.source + ". " : "") +
    all.length + " records" +
    (minY !== "" && maxY !== "" ? ", " + minY + "–" + maxY + "." : ".");

  // ---- filter controls -------------------------------------------------
  var mechSelect = document.getElementById("f-mech");
  var bodySelect = document.getElementById("f-body");
  var sdgSelect = document.getElementById("f-sdg");
  var y1Input = document.getElementById("f-y1");
  var y2Input = document.getElementById("f-y2");
  var kwInput = document.getElementById("f-kw");
  var resetBtn = document.getElementById("f-reset");

  function uniqueSorted(arr) {
    var seen = {}, out = [];
    arr.forEach(function (v) {
      if (v != null && v !== "" && !seen[v]) { seen[v] = true; out.push(v); }
    });
    out.sort(function (a, b) { return String(a).localeCompare(String(b)); });
    return out;
  }

  function fillSelect(sel, values, allLabel) {
    var opts = ['<option value="">' + allLabel + "</option>"];
    values.forEach(function (v) { opts.push('<option value="' + esc(v) + '">' + esc(v) + "</option>"); });
    sel.innerHTML = opts.join("");
  }
  function esc(s) {
    return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;")
      .replace(/>/g, "&gt;").replace(/"/g, "&quot;");
  }

  fillSelect(mechSelect, uniqueSorted(all.map(function (r) { return r.mechanism; })), "All mechanisms");
  fillSelect(bodySelect, uniqueSorted(all.map(function (r) { return r.body; })), "All bodies");

  var sdgNames = DATA.sdg_names || {};
  var sdgNums = [];
  all.forEach(function (r) {
    (r.sdgs || []).forEach(function (s) {
      if (sdgNums.indexOf(s) === -1) sdgNums.push(s);
    });
  });
  sdgNums.sort(function (a, b) { return a - b; });
  var sdgOpts = ['<option value="">All SDGs</option>'];
  sdgNums.forEach(function (n) {
    var label = "SDG " + n + (sdgNames[String(n)] ? ": " + sdgNames[String(n)] : "");
    sdgOpts.push('<option value="' + esc(n) + '">' + esc(label) + "</option>");
  });
  sdgSelect.innerHTML = sdgOpts.join("");

  // ---- filtering --------------------------------------------------------
  function matches(r, f) {
    if (f.mechanism && r.mechanism !== f.mechanism) return false;
    if (f.body && r.body !== f.body) return false;
    if (f.y1 !== null && !(typeof r.year === "number" && r.year >= f.y1)) return false;
    if (f.y2 !== null && !(typeof r.year === "number" && r.year <= f.y2)) return false;
    if (f.sdg !== null && (r.sdgs || []).indexOf(f.sdg) === -1) return false;
    if (f.kw) {
      var t = (r.text || "").toLowerCase();
      if (t.indexOf(f.kw) === -1) return false;
    }
    return true;
  }

  function getFilters() {
    var y1 = parseInt(y1Input.value, 10);
    var y2 = parseInt(y2Input.value, 10);
    var sdg = sdgSelect.value === "" ? null : parseInt(sdgSelect.value, 10);
    return {
      mechanism: mechSelect.value,
      body: bodySelect.value,
      y1: isNaN(y1) ? null : y1,
      y2: isNaN(y2) ? null : y2,
      sdg: sdg,
      kw: kwInput.value.trim().toLowerCase()
    };
  }

  function describeFilters(f) {
    var parts = [];
    if (f.mechanism) parts.push(f.mechanism);
    if (f.body) parts.push("Body: " + f.body);
    if (f.y1 !== null || f.y2 !== null) {
      var a = f.y1 !== null ? f.y1 : minY;
      var b = f.y2 !== null ? f.y2 : maxY;
      parts.push(a + "–" + b);
    }
    if (f.sdg !== null) {
      parts.push("SDG " + f.sdg + (sdgNames[String(f.sdg)] ? ": " + sdgNames[String(f.sdg)] : ""));
    }
    if (f.kw) parts.push('keyword: "' + kwInput.value.trim() + '"');
    return parts.length ? parts.join(" · ") : "no filters applied";
  }

  // ---- state ------------------------------------------------------------
  var shown = 0;
  var current = [];
  var chart = null;
  var PAGE = 100;

  function firstLine(text) {
    if (!text) return "";
    var idx = text.indexOf("\n");
    var line = idx === -1 ? text : text.substring(0, idx);
    if (text.length > 160 && idx === -1) line = text.substring(0, 160) + "…";
    else if (idx > 160) line = text.substring(0, 160) + "…";
    return line;
  }

  function fmtDate(d) {
    if (!d) return "date unknown";
    return d;
  }

  function sortRecords(list) {
    return list.slice().sort(function (a, b) {
      var da = a.date || "", db = b.date || "";
      if (da === "" && db === "") return 0;
      if (da === "") return 1;
      if (db === "") return -1;
      return db.localeCompare(da);
    });
  }

  function buildChart(list) {
    var counts = {};
    list.forEach(function (r) {
      (r.themes || []).forEach(function (t) {
        if (!t) return;
        counts[t] = (counts[t] || 0) + 1;
      });
    });
    var entries = Object.keys(counts).map(function (t) { return [t, counts[t]]; });
    entries.sort(function (a, b) {
      if (b[1] !== a[1]) return b[1] - a[1];
      return a[0].localeCompare(b[0]);
    });
    var top = entries.slice(0, 10).reverse(); // longest bar on top
    var labels = top.map(function (e) { return e[0]; });
    var values = top.map(function (e) { return e[1]; });

    var ctx = document.getElementById("themechart");
    if (chart) { chart.destroy(); chart = null; }
    if (!entries.length) {
      document.getElementById("chartbox").innerHTML =
        '<div class="empty">No themes among the matching records.</div>';
      return;
    }
    if (!document.getElementById("themechart")) {
      document.getElementById("chartbox").innerHTML = '<canvas id="themechart"></canvas>';
    }
    ctx = document.getElementById("themechart");
    chart = new window.Chart(ctx, {
      type: "bar",
      data: {
        labels: labels,
        datasets: [{
          label: "Records",
          data: values,
          backgroundColor: "#1f6fb2"
        }]
      },
      options: {
        indexAxis: "y",
        responsive: true,
        animation: false,
        plugins: {
          legend: { display: false },
          tooltip: { callbacks: { label: function (c) { return c.parsed.x + " records"; } } }
        },
        scales: {
          x: { beginAtZero: true, ticks: { precision: 0 } },
          y: { ticks: { autoSkip: false, font: { size: 13 } } }
        }
      }
    });
  }

  function renderRows() {
    var tbody = document.getElementById("tbody");
    var slice = current.slice(shown, shown + PAGE);
    var html = slice.map(function (r) {
      var symCell;
      if (r.symbol && r.doc_url) {
        symCell = '<a class="sym" href="' + esc(r.doc_url) + '" target="_blank" rel="noopener">' + esc(r.symbol) + "</a>";
      } else if (r.symbol) {
        symCell = '<span class="tagline">' + esc(r.symbol) + "</span>";
      } else {
        symCell = '<span class="nosym">(no symbol)</span>';
      }
      var themes = (r.themes && r.themes.length) ? r.themes.join("; ") : "none recorded";
      var sdgs = (r.sdgs && r.sdgs.length)
        ? r.sdgs.map(function (s) {
            return "SDG " + s + (sdgNames[String(s)] ? " (" + sdgNames[String(s)] + ")" : "");
          }).join("; ")
        : "none recorded";
      var persons = (r.affected_persons && r.affected_persons.length)
        ? esc(r.affected_persons.join("; "))
        : "none recorded";
      return '<tr class="row" data-id="' + esc(r.id) + '">' +
        '<td class="date">' + esc(fmtDate(r.date)) + "</td>" +
        '<td class="body">' + esc(r.body || "unknown") + "</td>" +
        '<td>' + symCell + "</td>" +
        '<td class="text">' + esc(firstLine(r.text)) + "</td>" +
        "</tr>" +
        '<tr class="expansion" data-for="' + esc(r.id) + '" hidden><td colspan="4">' +
        '<p class="fulltext">' + esc(r.text || "") + "</p>" +
        '<div class="tags">' +
        "<div><span>Themes:</span> " + esc(themes) + "</div>" +
        "<div><span>SDGs:</span> " + esc(sdgs) + "</div>" +
        "<div><span>Affected persons:</span> " + persons + "</div>" +
        '<div><span>Document:</span> ' + (r.doc_url
            ? '<a class="sym" href="' + esc(r.doc_url) + '" target="_blank" rel="noopener">' + esc(r.symbol || "(no symbol)") + "</a>"
            : esc(r.symbol || "(no symbol)")) +
          " · " + esc(r.mechanism || "") + " · " + esc(r.type || "") + "</div>" +
        "</div></td></tr>";
    }).join("");
    tbody.insertAdjacentHTML("beforeend", html);
    shown += slice.length;
    document.getElementById("showmore").hidden = shown >= current.length;
  }

  function update() {
    var f = getFilters();
    current = sortRecords(all.filter(function (r) { return matches(r, f); }));
    shown = 0;
    document.getElementById("tbody").innerHTML = "";
    document.getElementById("nomatch").hidden = current.length > 0;
    document.getElementById("table").style.display = current.length ? "" : "none";
    document.getElementById("summaryline").innerHTML =
      "Showing <strong>" + current.length + "</strong> of " + all.length + " records";
    document.getElementById("filterdesc").textContent =
      "Filters: " + describeFilters(f) + ".";
    buildChart(current);
    renderRows();
  }

  // row expansion
  document.getElementById("tbody").addEventListener("click", function (e) {
    var link = e.target.closest("a.sym");
    if (link) return; // let symbol links work
    var row = e.target.closest("tr.row");
    if (!row) return;
    var exp = document.querySelector('tr.expansion[data-for="' + row.getAttribute("data-id") + '"]');
    if (exp) exp.hidden = !exp.hidden;
  });

  document.getElementById("showmore").addEventListener("click", renderRows);

  [mechSelect, bodySelect, sdgSelect].forEach(function (el) {
    el.addEventListener("change", update);
  });
  [y1Input, y2Input, kwInput].forEach(function (el) {
    el.addEventListener("input", update);
  });
  resetBtn.addEventListener("click", function () {
    mechSelect.value = ""; bodySelect.value = ""; sdgSelect.value = "";
    y1Input.value = ""; y2Input.value = ""; kwInput.value = "";
    update();
  });

  update();
})();
</script>
</body>
</html>
```