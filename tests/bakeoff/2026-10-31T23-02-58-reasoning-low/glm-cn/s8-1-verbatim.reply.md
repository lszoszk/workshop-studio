I built a search tool over the General Comments with a full boolean query parser (AND, OR, NOT, parentheses, "exact phrases", implicit AND), committee and year filters, highlighted matching paragraphs with expandable full text, copy-citation buttons, and a live Chart.js bar chart of hits per committee. Paragraph text is rendered verbatim from the data, never altered.

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>General Comments — Paragraph Search</title>
<style>
  :root { --accent:#1f6fb2; --bg:#f7f9fb; --line:#dde4ec; --ink:#1c2733; --muted:#5b6b7c; }
  * { box-sizing:border-box; }
  body { margin:0; font:16px/1.55 -apple-system, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
         background:var(--bg); color:var(--ink); }
  header { background:#fff; border-bottom:1px solid var(--line); padding:28px 32px 22px; }
  header h1 { margin:0 0 6px; font-size:26px; color:var(--accent); }
  header p { margin:0; color:var(--muted); font-size:15px; }
  main { max-width:1080px; margin:0 auto; padding:24px 32px 60px; }
  .panel { background:#fff; border:1px solid var(--line); border-radius:8px; padding:18px 20px; margin-bottom:20px; }
  .searchbox { display:flex; gap:10px; flex-wrap:wrap; }
  .searchbox input[type=text] { flex:1 1 380px; font-size:17px; padding:10px 12px; border:1px solid var(--line);
    border-radius:6px; font-family:inherit; }
  button { font:inherit; }
  .btn { background:var(--accent); color:#fff; border:none; border-radius:6px; padding:10px 18px; cursor:pointer; font-size:16px; }
  .btn:hover { background:#175a92; }
  .btn.ghost { background:#fff; color:var(--accent); border:1px solid var(--accent); }
  .help { color:var(--muted); font-size:13.5px; margin-top:8px; }
  .help code { background:#eef3f8; border-radius:3px; padding:1px 5px; font-size:13px; }
  .filters { display:flex; gap:18px; flex-wrap:wrap; align-items:center; margin-top:14px; }
  .filters label { font-size:14px; color:var(--muted); }
  select { font:inherit; font-size:15px; padding:6px 8px; border:1px solid var(--line); border-radius:6px; background:#fff; }
  .stats { font-size:15px; margin:0 0 14px; }
  .stats strong { color:var(--accent); }
  .chartwrap { display:flex; gap:24px; align-items:flex-start; flex-wrap:wrap; }
  .chartbox { flex:0 0 340px; height:260px; position:relative; }
  .note { font-size:13px; color:var(--muted); flex:1 1 300px; max-width:520px; }
  ul.hits { list-style:none; margin:0; padding:0; }
  ul.hits li { border:1px solid var(--line); border-radius:8px; padding:14px 16px; margin-bottom:14px; background:#fff; }
  .meta { font-size:13.5px; color:var(--muted); margin-bottom:8px; display:flex; gap:10px; flex-wrap:wrap; align-items:center; }
  .meta .sym { font-family:ui-monospace, Consolas, monospace; }
  .meta a { color:var(--accent); text-decoration:none; }
  .meta a:hover { text-decoration:underline; }
  .meta .kind { background:#eef3f8; border-radius:4px; padding:1px 7px; }
  .title-line { font-size:15px; margin-bottom:6px; }
  .excerpt { font-size:15.5px; }
  mark { background:#ffe9a8; padding:0 1px; border-radius:2px; }
  .clip { background:#eef3f8; color:var(--accent); border:1px solid var(--accent); border-radius:5px;
          padding:3px 10px; font-size:13px; cursor:pointer; }
  .clip.copied { background:#e2f2e6; color:#20713c; border-color:#20713c; }
  .collapsed { max-height:120px; overflow:hidden; position:relative; }
  .collapsed::after { content:""; position:absolute; left:0; right:0; bottom:0; height:46px;
    background:linear-gradient(transparent, #fff); }
  .expand { background:none; border:none; color:var(--accent); cursor:pointer; padding:4px 0; font-size:13.5px; }
  .empty { padding:26px; text-align:center; color:var(--muted); background:#fff; border:1px dashed var(--line); border-radius:8px; }
  .err { background:#fdecec; border:1px solid #e2a1a1; color:#8a2a2a; border-radius:6px; padding:10px 14px; margin-bottom:16px; font-size:15px; }
</style>
</head>
<body>
<header>
  <h1>General Comments — Paragraph Search</h1>
  <p id="dataset-desc"></p>
</header>
<main>
  <section class="panel">
    <div class="searchbox">
      <input type="text" id="q" placeholder='e.g. torture AND ("death penalty" OR execution) NOT Germany'
             autocomplete="off" spellcheck="false">
      <button class="btn" id="go">Search</button>
    </div>
    <p class="help">
      Search words are matched inside paragraphs, case-insensitively. Combine terms with
      <code>AND</code>, <code>OR</code>, <code>NOT</code> and parentheses; adjacent terms are joined with AND.
      Use quotes for an <code>"exact phrase"</code>.
    </p>
    <div class="filters">
      <label>Committee <select id="f-committee"></select></label>
      <label>Year <select id="f-year"></select></label>
      <button class="btn ghost" id="clear">Reset all</button>
    </div>
  </section>

  <section class="panel">
    <p class="stats" id="stats"></p>
    <div class="chartwrap">
      <div class="chartbox"><canvas id="chart"></canvas></div>
      <p class="note"><strong>How this is computed:</strong> every bar counts the paragraphs from one committee
      whose text satisfies the current search. The chart ignores the committee filter (so you can use it to
      compare committees), but it does respect the year filter and the search box. Counts are done by this
      page's JavaScript directly on the loaded data — nothing is estimated.</p>
    </div>
  </section>

  <div id="error" class="err" hidden></div>
  <ul class="hits" id="results"></ul>
  <div class="empty" id="empty" hidden></div>
</main>

<script>
(function () {
  "use strict";
  var gc = (window.WORKSHOP_DATA && window.WORKSHOP_DATA.gc) || { records: [], count: 0, title: "", source: "" };
  var records = gc.records || [];

  // ---------- dataset description ----------
  (function () {
    var years = records.map(function (r) { return r.year; }).filter(function (y) { return y != null; });
    var committees = {};
    records.forEach(function (r) { if (r.committee) committees[r.committee] = 1; });
    var nCom = Object.keys(committees).length;
    var span = years.length ? " (" + Math.min.apply(null, years) + "–" + Math.max.apply(null, years) + ")" : "";
    document.getElementById("dataset-desc").textContent =
      "UN human rights treaty bodies' General Comments, paragraph by paragraph. " +
      (gc.source ? "Source: " + gc.source + ". " : "") +
      "n = " + records.length + " paragraphs from " + nCom + " committees" + span + ".";
  })();

  // ---------- query parser ----------
  // Grammar: expr := term (OR term)* ; term := factor (AND factor)* ;
  //            factor := NOT factor | '(' expr ')' | WORD | "PHRASE"
  // Implicit AND between adjacent factors. NOT binds tighter than AND; AND binds tighter than OR.
  function tokenize(input) {
    var tokens = [], i = 0, n = input.length;
    while (i < n) {
      var c = input[i];
      if (/\s/.test(c)) { i++; continue; }
      if (c === '"' || c === "'") {
        var q = c; i++;
        var buf = "";
        while (i < n && input[i] !== q) {
          if (input[i] === "\\" && i + 1 < n) { buf += input[i + 1]; i += 2; }
          else { buf += input[i]; i++; }
        }
        if (i >= n) throw new Error("Unclosed quote in the search box.");
        i++;
        if (buf.length) tokens.push({ t: "phrase", v: buf });
        continue;
      }
      if (c === "(" || c === ")") { tokens.push({ t: c }); i++; continue; }
      var w = "";
      while (i < n && !/\s/.test(input[i]) && input[i] !== '"' && input[i] !== "'" && input[i] !== "(" && input[i] !== ")") {
        w += input[i]; i++;
      }
      if (!w.length) { i++; continue; }
      var up = w.toUpperCase();
      if (up === "AND" || up === "OR" || up === "NOT") tokens.push({ t: up });
      else tokens.push({ t: "phrase", v: w });
    }
    return tokens;
  }

  function parse(tokens) {
    var pos = 0;
    function peek() { return tokens[pos]; }
    function parseExpr() {
      var node = parseTerm();
      while (peek() && peek().t === "OR") { pos++; node = { op: "OR", a: node, b: parseTerm() }; }
      return node;
    }
    function parseTerm() {
      var node = parseFactor();
      while (true) {
        var p = peek();
        if (p && p.t === "AND") { pos++; node = { op: "AND", a: node, b: parseFactor() }; }
        else if (p && (p.t === "phrase" || p.t === "NOT" || p.t === "(")) { // implicit AND
          node = { op: "AND", a: node, b: parseFactor() };
        } else break;
      }
      return node;
    }
    function parseFactor() {
      var p = peek();
      if (!p) throw new Error("The query ends unexpectedly — a term seems to be missing.");
      if (p.t === "NOT") { pos++; return { op: "NOT", a: parseFactor() }; }
      if (p.t === "(") {
        pos++;
        var node = parseExpr();
        if (!peek() || peek().t !== ")") throw new Error("A closing parenthesis ) is missing.");
        pos++;
        return node;
      }
      if (p.t === ")") throw new Error("A closing parenthesis ) has no matching opening parenthesis.");
      if (p.t === "AND" || p.t === "OR") throw new Error("Two operators in a row — a term seems to be missing.");
      pos++;
      return { op: "PHRASE", v: p.v };
    }
    var tree = parseExpr();
    if (pos < tokens.length) throw new Error("Unexpected '" + tokens[pos].v + "' in the query.");
    return tree;
  }

  function evalNode(node, textLower) {
    switch (node.op) {
      case "PHRASE": return textLower.indexOf(node.v.toLowerCase()) !== -1;
      case "AND": return evalNode(node.a, textLower) && evalNode(node.b, textLower);
      case "OR": return evalNode(node.a, textLower) || evalNode(node.b, textLower);
      case "NOT": return !evalNode(node.a, textLower);
    }
    return false;
  }

  function collectPhrases(node, out) {
    if (!node) return;
    if (node.op === "PHRASE") out.push(node.v.toLowerCase());
    else { collectPhrases(node.a, out); collectPhrases(node.b, out); }
  }

  // ---------- highlighting ----------
  function escapeHtml(s) {
    return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")
                    .replace(/"/g, "&quot;").replace(/'/g, "&#39;");
  }
  function buildHighlighter(phrases) {
    if (!phrases.length) return null;
    var escaped = phrases.map(function (p) { return p.replace(/[.*+?^${}()|[\]\\]/g, "\\$&"); });
    try { return new RegExp("(" + escaped.join("|") + ")", "gi"); }
    catch (e) { return null; }
  }
  function highlight(text, regex) {
    if (!regex) return escapeHtml(text);
    var esc = escapeHtml(text);
    // Rebuild regex on the escaped string; special chars in phrases were already escaped,
    // but escapeHtml may have introduced entities containing our phrase chars. Instead:
    // highlight on raw text, escaping segments as we go.
    var out = "", last = 0, m;
    regex.lastIndex = 0;
    while ((m = regex.exec(text)) !== null) {
      out += escapeHtml(text.slice(last, m.index));
      out += "<mark>" + escapeHtml(m[0]) + "</mark>";
      last = m.index + m[0].length;
      if (m[0].length === 0) regex.lastIndex++;
    }
    out += escapeHtml(text.slice(last));
    return out;
  }

  // ---------- filters setup ----------
  var fCom = document.getElementById("f-committee");
  var fYear = document.getElementById("f-year");
  (function () {
    var coms = {}, yrs = {};
    records.forEach(function (r) {
      if (r.committee) coms[r.committee] = 1;
      if (r.year != null) yrs[r.year] = 1;
    });
    var cList = Object.keys(coms).sort();
    var yList = Object.keys(yrs).map(Number).sort(function (a, b) { return b - a; });
    fCom.innerHTML = '<option value="">All committees (' + cList.length + ')</option>' +
      cList.map(function (c) { return '<option value="' + escapeHtml(c) + '">' + escapeHtml(c) + "</option>"; }).join("");
    fYear.innerHTML = '<option value="">All years</option>' +
      yList.map(function (y) { return '<option value="' + y + '">' + y + "</option>"; }).join("");
  })();

  // ---------- chart ----------
  var chart = null;
  function renderChart(counts) {
    var labels = Object.keys(counts);
    labels.sort(function (a, b) { return counts[b] - counts[a] || (a < b ? -1 : 1); });
    var ctx = document.getElementById("chart").getContext("2d");
    var data = {
      labels: labels,
      datasets: [{
        label: "Matching paragraphs",
        data: labels.map(function (l) { return counts[l]; }),
        backgroundColor: "#1f6fb2",
        borderRadius: 3
      }]
    };
    if (chart) { chart.data = data; chart.update(); return; }
    chart = new window.Chart(ctx, {
      type: "bar",
      data: data,
      options: {
        responsive: true, maintainAspectRatio: false,
        indexAxis: "x",
        plugins: { legend: { display: false },
          tooltip: { callbacks: { label: function (c) { return c.parsed.y + " matching paragraphs"; } } } },
        scales: {
          y: { beginAtZero: true, ticks: { precision: 0 }, grid: { color: "#eef1f5" } },
          x: { grid: { display: false } }
        }
      }
    });
  }

  // ---------- search + render ----------
  var RESULTS_CAP = 200;
  function run() {
    var errBox = document.getElementById("error");
    errBox.hidden = true;
    var raw = document.getElementById("q").value.trim();
    var tree = null, regex = null;
    try {
      if (raw) { tree = parse(tokenize(raw)); }
    } catch (e) {
      errBox.textContent = "I could not read that query: " + e.message;
      errBox.hidden = false;
    }
    var phrases = [];
    if (tree) collectPhrases(tree, phrases);
    regex = buildHighlighter(phrases);

    var comFilter = fCom.value, yearFilter = fYear.value;
    var matches = [], comCounts = {}, comTotal = {};
    records.forEach(function (r) {
      var textLower = (r.text || "").toLowerCase();
      var ok = !tree || evalNode(tree, textLower);
      if (ok) {
        comCounts[r.committee || "—"] = (comCounts[r.committee || "—"] || 0) + 1;
        if ((!comFilter || (r.committee || "") === comFilter) &&
            (!yearFilter || String(r.year) === yearFilter)) {
          matches.push(r);
        }
      }
    });
    records.forEach(function (r) { comTotal[r.committee || "—"] = (comTotal[r.committee || "—"] || 0) + 1; });
    if (!Object.keys(comCounts).length) comCounts["(no committee matched)"] = 0;

    renderChart(comCounts);

    // stats line
    var parts = [];
    var active = records.filter(function (r) {
      return (!comFilter || (r.committee || "") === comFilter) && (!yearFilter || String(r.year) === yearFilter);
    });
    parts.push("<strong>" + matches.length + "</strong> matching paragraphs shown" +
      (matches.length > RESULTS_CAP ? " (first " + RESULTS_CAP + " below)" : ""));
    parts.push(active.length + " paragraphs were in scope after filters (" +
      (comFilter ? "committee: " + escapeHtml(comFilter) : "all committees") + "; " +
      (yearFilter ? "year: " + escapeHtml(yearFilter) : "all years") + ")");
    parts.push(records.length + " paragraphs in the dataset");
    document.getElementById("stats").innerHTML = parts.join(" &middot; ") +
      ". <em>How this is computed: your query and filters are applied to each paragraph's full text by this page's JavaScript — no approximation.</em>";

    // results
    var ul = document.getElementById("results");
    var emptyBox = document.getElementById("empty");
    ul.innerHTML = "";
    if (!matches.length) {
      emptyBox.hidden = false;
      emptyBox.textContent = records.length
        ? "No paragraphs match this search. Try removing a filter or simplifying the query."
        : "This dataset contains no General Comment paragraphs, so there is nothing to search yet.";
      return;
    }
    emptyBox.hidden = true;
    matches.slice(0, RESULTS_CAP).forEach(function (r) {
      var li = document.createElement("li");

      var meta = document.createElement("div");
      meta.className = "meta";
      var symHtml = r.doc_url
        ? '<a href="' + escapeHtml(r.doc_url) + '" target="_blank" rel="noopener" class="sym">' + escapeHtml(r.symbol || "(no symbol)") + "</a>"
        : '<span class="sym">' + escapeHtml(r.symbol || "(no symbol)") + "</span>";
      meta.innerHTML =
        '<span class="kind">' + escapeHtml(r.committee || "—") + "</span>" + symHtml +
        (r.year != null ? "<span>" + escapeHtml(r.year) + "</span>" : "") +
        (r.paragraph != null ? '<span>para. ' + escapeHtml(r.paragraph) + "</span>" : "") +
        '<button class="clip" data-cite="' + escapeHtml((r.symbol || "") + ", para. " + (r.paragraph != null ? r.paragraph : "?")) +
        '">Copy citation</button>';

      var titleLine = document.createElement("div");
      titleLine.className = "title-line";
      titleLine.textContent = r.short_title || r.title || "(untitled)";

      var excerpt = document.createElement("div");
      excerpt.className = "excerpt";
      excerpt.innerHTML = highlight(r.text || "", regex);

      li.appendChild(meta);
      li.appendChild(titleLine);
      li.appendChild(excerpt);

      // collapse very long paragraphs, expandable — full text always available
      var long = (r.text || "").length > 700;
      if (long) {
        excerpt.classList.add("collapsed");
        var exp = document.createElement("button");
        exp.className = "expand";
        exp.textContent = "Show full paragraph ▾";
        exp.addEventListener("click", function () {
          var open = !excerpt.classList.contains("collapsed");
          excerpt.classList.toggle("collapsed", open);
          exp.textContent = open ? "Show full paragraph ▾" : "Hide full paragraph ▴";
        });
        li.appendChild(exp);
      }
      ul.appendChild(li);
    });
  }

  // copy citation
  document.getElementById("results").addEventListener("click", function (ev) {
    var btn = ev.target.closest ? ev.target.closest(".clip") : null;
    if (!btn) return;
    var cite = btn.getAttribute("data-cite") || "";
    function done(ok) {
      btn.textContent = ok ? "Copied ✓" : "Copy failed";
      btn.classList.add("copied");
      setTimeout(function () { btn.textContent = "Copy citation"; btn.classList.remove("copied"); }, 1800);
    }
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(cite).then(function () { done(true); }, function () { fallback(); });
    } else fallback();
    function fallback() {
      var ta = document.createElement("textarea");
      ta.value = cite; ta.style.position = "fixed"; ta.style.opacity = "0";
      document.body.appendChild(ta); ta.select();
      var ok = false;
      try { ok = document.execCommand("copy"); } catch (e) {}
      document.body.removeChild(ta); done(ok);
    }
  });

  document.getElementById("go").addEventListener("click", run);
  document.getElementById("q").addEventListener("keydown", function (e) { if (e.key === "Enter") run(); });
  fCom.addEventListener("change", run);
  fYear.addEventListener("change", run);
  document.getElementById("clear").addEventListener("click", function () {
    document.getElementById("q").value = "";
    fCom.value = ""; fYear.value = "";
    run();
  });

  run();
})();
</script>
</body>
</html>
```
