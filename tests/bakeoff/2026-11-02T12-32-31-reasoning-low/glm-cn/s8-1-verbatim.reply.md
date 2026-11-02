Built the General Comments search app exactly to the plan: query parser with AND/OR/NOT and quoted phrases, committee and year filters, a per-committee bar chart of the matches, and result cards with highlighted text and a copy-citation button.

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>General Comments search</title>
<style>
  :root { --accent:#1f6fb2; }
  * { box-sizing:border-box; }
  body { margin:0; font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif; background:#f6f8fa; color:#222; font-size:16px; line-height:1.5; }
  .wrap { max-width:1000px; margin:0 auto; padding:28px 20px 60px; }
  h1 { font-size:26px; margin:0 0 4px; color:#123; }
  .subtitle { color:#555; margin:0 0 22px; }
  .panel { background:#fff; border:1px solid #e2e6ea; border-radius:8px; padding:16px 18px; margin-bottom:18px; }
  .searchrow { display:flex; gap:8px; flex-wrap:wrap; }
  .searchrow input[type=text] { flex:1; min-width:220px; padding:9px 10px; font-size:16px; border:1px solid #c3cbd3; border-radius:6px; }
  button { font-size:16px; padding:9px 16px; border-radius:6px; border:1px solid var(--accent); background:var(--accent); color:#fff; cursor:pointer; }
  button:hover { background:#185a91; }
  .help { color:#555; font-size:14px; margin-top:8px; }
  .help code { background:#eef2f6; padding:1px 5px; border-radius:4px; }
  .filters { display:flex; gap:16px; flex-wrap:wrap; align-items:center; margin-top:14px; }
  .filters label { font-size:14px; color:#333; }
  .filters select, .filters input[type=number] { padding:6px 8px; font-size:15px; border:1px solid #c3cbd3; border-radius:6px; }
  .countline { margin:0 0 6px; }
  .note { font-size:13px; color:#666; margin:6px 0 0; }
  .chartbox { height:220px; }
  .card { background:#fff; border:1px solid #e2e6ea; border-radius:8px; padding:14px 18px; margin-bottom:14px; }
  .card .meta { font-size:14px; color:#555; margin-bottom:6px; }
  .card .meta .sym a, .card .meta .sym span.nolink { color:var(--accent); }
  .card .meta a { color:var(--accent); text-decoration:none; }
  .card .meta a:hover { text-decoration:underline; }
  .card p { margin:0 0 10px; white-space:pre-wrap; }
  mark { background:#ffe9a8; padding:0 1px; border-radius:2px; }
  .copybtn { background:#fff; color:var(--accent); padding:5px 12px; font-size:14px; }
  .copybtn:hover { background:#eef4fa; }
  .copybtn.copied { background:#2e8b57; border-color:#2e8b57; color:#fff; }
  .empty { background:#fff; border:1px solid #e2e6ea; border-radius:8px; padding:22px; text-align:center; color:#444; }
  .empty .tip { color:#777; font-size:14px; }
</style>
</head>
<body>
<div class="wrap">
  <h1>General Comments search</h1>
  <p class="subtitle" id="subtitle"></p>

  <div class="panel">
    <div class="searchrow">
      <input type="text" id="q" placeholder='Search paragraph text, e.g. "best interests" AND child' aria-label="Search">
      <button id="searchBtn">Search</button>
    </div>
    <p class="help">Words are combined with <code>AND</code> unless you write <code>OR</code>; <code>NOT</code> excludes a word; <code>"quotes"</code> find an exact phrase. Example: <code>"best interests" AND child</code>. Matching is case-insensitive; a plain word matches a whole word only ("right" does not match "rights").</p>
    <div class="filters">
      <label>Committee <select id="committee"></select></label>
      <label>Year from <input type="number" id="yearFrom" style="width:90px"></label>
      <label>to <input type="number" id="yearTo" style="width:90px"></label>
    </div>
  </div>

  <div class="panel">
    <p class="countline" id="countline"></p>
    <div class="chartbox"><canvas id="chart"></canvas></div>
    <p class="note"><strong>How this is computed:</strong> the bars count the paragraphs that match the current search and filters, grouped by the committee field of each paragraph. The bars always add up to the match count shown above.</p>
  </div>

  <div id="results"></div>
</div>

<script>
(function () {
  var data = window.WORKSHOP_DATA.gc;
  var records = (data && data.records) ? data.records : [];

  // ---- subtitle: source, n paragraphs, year range ----
  var years = records.map(function (r) { return r.year; }).filter(function (y) { return typeof y === "number"; });
  var yearPart;
  if (years.length) {
    yearPart = Math.min.apply(null, years) + "–" + Math.max.apply(null, years);
  } else {
    yearPart = "no dated paragraphs";
  }
  document.getElementById("subtitle").textContent =
    "Source: " + (data.title || "General Comments, paragraph by paragraph") +
    " — " + records.length + " paragraphs, " + yearPart + ".";

  // ---- committee filter options ----
  var committees = [];
  records.forEach(function (r) {
    if (r.committee && committees.indexOf(r.committee) === -1) committees.push(r.committee);
  });
  committees.sort();
  var committeeSel = document.getElementById("committee");
  var allOpt = document.createElement("option");
  allOpt.value = "";
  allOpt.textContent = "All (" + committees.length + " committees)";
  committeeSel.appendChild(allOpt);
  committees.forEach(function (c) {
    var o = document.createElement("option");
    o.value = c; o.textContent = c;
    committeeSel.appendChild(o);
  });

  // ---- query parsing ----
  // Tokenise into: term (plain word or quoted phrase), and operators AND OR NOT.
  function tokenize(q) {
    var tokens = [];
    var i = 0;
    while (i < q.length) {
      var ch = q[i];
      if (/\s/.test(ch)) { i++; continue; }
      if (ch === '"') {
        var j = q.indexOf('"', i + 1);
        if (j === -1) j = q.length;
        var phrase = q.slice(i + 1, j).trim();
        if (phrase) tokens.push({ type: "term", phrase: true, value: phrase });
        i = j + 1;
        continue;
      }
      var m = /^[^\s"]+/.exec(q.slice(i));
      var word = m[0];
      var up = word.toUpperCase();
      if (up === "AND" || up === "OR" || up === "NOT") {
        tokens.push({ type: up });
      } else if (word) {
        tokens.push({ type: "term", phrase: false, value: word });
      }
      i += word.length;
    }
    return tokens;
  }

  // Build structure: array of OR-alternatives; each alternative is an array of
  // {negate:bool, term:{phrase,value}} joined by AND.
  function parseQuery(q) {
    var tokens = tokenize(q);
    var orGroups = [];
    var current = [];
    function pushCurrent() { if (current.length) { orGroups.push(current); current = []; } }
    var negateNext = false;
    for (var t = 0; t < tokens.length; t++) {
      var tok = tokens[t];
      if (tok.type === "OR") { pushCurrent(); negateNext = false; }
      else if (tok.type === "AND") { /* default */ negateNext = false; }
      else if (tok.type === "NOT") { negateNext = true; }
      else {
        current.push({ negate: negateNext, term: tok });
        negateNext = false;
      }
    }
    pushCurrent();
    if (!orGroups.length && tokens.some(function (tk) { return tk.type === "NOT"; })) {
      // e.g. only "NOT word": treat as AND-group with the negation alone
      orGroups.push(current);
    }
    return orGroups;
  }

  function escapeRe(s) { return s.replace(/[.*+?^${}()|[\]\\]/g, "\\$&"); }

  function makeMatcher(term) {
    var words = term.value.toLowerCase().split(/\s+/).filter(Boolean);
    if (!words.length) return null;
    var re = new RegExp("(?:\\b" + words.map(escapeRe).join("\\s+") + "\\b)", "i");
    return { re: re, plain: !term.phrase && words.length === 1, word: words[0] };
  }

  // Evaluate one OR-group (array of AND items) against lowercase text.
  function evalGroup(group, matchers, textLower) {
    for (var g = 0; g < group.length; g++) {
      var item = group[g];
      var m = matchers[g];
      if (!m) continue;
      var found = m.re.test(textLower);
      if (item.negate && found) return false;
      if (!item.negate && !found) return false;
    }
    return true;
  }

  // ---- highlighting ----
  // Highlight positive (non-negated) terms only.
  function buildHighlightRegex(orGroups, matchersList) {
    var patterns = [];
    orGroups.forEach(function (group, gi) {
      group.forEach(function (item, ii) {
        if (!item.negate) {
          var m = matchersList[gi][ii];
          if (m) {
            var words = m.re.source.replace(/^\(\?:\\b/, "").replace(/\\b\)$/, "");
            patterns.push(words);
          }
        }
      });
    });
    if (!patterns.length) return null;
    try { return new RegExp("\\b(?:" + patterns.join("|") + ")\\b", "gi"); }
    catch (e) { return null; }
  }

  function highlightText(text, hlRe) {
    if (!hlRe) return [text];
    var parts = [];
    var last = 0;
    hlRe.lastIndex = 0;
    var m;
    while ((m = hlRe.exec(text)) !== null) {
      if (m.index > last) parts.push(text.slice(last, m.index));
      parts.push({ mark: m[0] });
      last = m.index + m[0].length;
      if (m[0].length === 0) hlRe.lastIndex++;
    }
    if (last < text.length) parts.push(text.slice(last));
    return parts;
  }

  function renderHighlighted(text, hlRe) {
    var parts = highlightText(text, hlRe);
    var frag = document.createDocumentFragment();
    parts.forEach(function (p) {
      if (typeof p === "string") {
        frag.appendChild(document.createTextNode(p));
      } else {
        var mk = document.createElement("mark");
        mk.textContent = p.mark;
        frag.appendChild(mk);
      }
    });
    return frag;
  }

  // ---- state and search ----
  var lastQuery = "";
  var chart = null;

  function yearOk(r, from, to) {
    var hasFrom = from !== null, hasTo = to !== null;
    if (!hasFrom && !hasTo) return true; // open filter: include everything, incl. unknown years
    if (typeof r.year !== "number") return false; // a from-to range excludes unknown years
    if (hasFrom && r.year < from) return false;
    if (hasTo && r.year > to) return false;
    return true;
  }

  function computeResults() {
    var q = document.getElementById("q").value.trim();
    var committee = committeeSel.value;
    var from = parseYear(document.getElementById("yearFrom").value);
    var to = parseYear(document.getElementById("yearTo").value);

    // filters first
    var filtered = records.filter(function (r) {
      if (committee && r.committee !== committee) return false;
      return yearOk(r, from, to);
    });

    var orGroups = q ? parseQuery(q) : [];
    var matchersList = orGroups.map(function (group) {
      return group.map(function (item) { return makeMatcher(item.term); });
    });
    var hlRe = q ? buildHighlightRegex(orGroups, matchersList) : null;

    var results;
    if (!orGroups.length) {
      results = filtered.slice();
    } else {
      results = filtered.filter(function (r) {
        var text = (r.text || "").toLowerCase();
        if (!r.text) return false; // empty text never matches
        for (var gi = 0; gi < orGroups.length; gi++) {
          if (evalGroup(orGroups[gi], matchersList[gi], text)) return true;
        }
        return false;
      });
    }

    // sort newest General Comment first
    results.sort(function (a, b) {
      var ya = typeof a.year === "number" ? a.year : -Infinity;
      var yb = typeof b.year === "number" ? b.year : -Infinity;
      if (yb !== ya) return yb - ya;
      var ta = a.short_title || a.title || a.symbol || "";
      var tb = b.short_title || b.title || b.symbol || "";
      return ta.localeCompare(tb);
    });

    return { results: results, filtered: filtered, q: q, committee: committee, from: from, to: to, hlRe: hlRe };
  }

  function parseYear(v) {
    if (!v) return null;
    var n = parseInt(v, 10);
    return isNaN(n) ? null : n;
  }

  // ---- rendering ----
  function filterDescription(st) {
    var bits = [];
    bits.push(st.committee ? "committee: " + st.committee : "committee: all");
    if (st.from === null && st.to === null) bits.push("years: all");
    else {
      var yr = "years: ";
      if (st.from !== null) yr += st.from;
      yr += "–";
      if (st.to !== null) yr += st.to;
      if (st.from === null) yr = "years: up to " + (st.to !== null ? st.to : "?");
      if (st.to === null && st.from !== null) yr = "years: from " + st.from;
      bits.push(yr);
    }
    return bits.join(", ");
  }

  function citation(r) {
    return (r.symbol || "") + ", para. " + r.paragraph;
  }

  function renderCard(r, hlRe) {
    var card = document.createElement("div");
    card.className = "card";

    var meta = document.createElement("div");
    meta.className = "meta";

    var committee = document.createElement("strong");
    committee.textContent = r.committee || "Unknown committee";
    meta.appendChild(committee);
    meta.appendChild(document.createTextNode(" · "));

    var label = r.short_title || r.title || r.symbol || "Untitled General Comment";
    var titleSpan = document.createElement("span");
    titleSpan.textContent = label + " · ";
    meta.appendChild(titleSpan);

    var yearTxt = (typeof r.year === "number") ? String(r.year) : "year unknown";
    meta.appendChild(document.createTextNode(yearTxt + " · "));

    var symSpan = document.createElement("span");
    symSpan.className = "sym";
    if (r.doc_url) {
      var a = document.createElement("a");
      a.href = r.doc_url;
      a.target = "_blank";
      a.rel = "noopener";
      a.textContent = r.symbol || "(no symbol)";
      symSpan.appendChild(a);
    } else {
      var s = document.createElement("span");
      s.className = "nolink";
      s.textContent = r.symbol || "(no symbol)";
      symSpan.appendChild(s);
    }
    meta.appendChild(symSpan);

    card.appendChild(meta);

    var p = document.createElement("p");
    p.appendChild(renderHighlighted(r.text || "", hlRe));
    card.appendChild(p);

    var btn = document.createElement("button");
    btn.className = "copybtn";
    btn.textContent = "Copy citation";
    btn.addEventListener("click", function () {
      copyToClipboard(citation(r), btn);
    });
    card.appendChild(btn);

    return card;
  }

  function copyToClipboard(text, btn) {
    function done() {
      btn.textContent = "Copied";
      btn.classList.add("copied");
      setTimeout(function () {
        btn.textContent = "Copy citation";
        btn.classList.remove("copied");
      }, 2000);
    }
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(text).then(done, function () { fallbackCopy(text, done); });
    } else {
      fallbackCopy(text, done);
    }
  }

  function fallbackCopy(text, done) {
    var ta = document.createElement("textarea");
    ta.value = text;
    ta.style.position = "fixed";
    ta.style.opacity = "0";
    document.body.appendChild(ta);
    ta.select();
    try { document.execCommand("copy"); } catch (e) {}
    document.body.removeChild(ta);
    done();
  }

  function renderChart(results) {
    var counts = {};
    var order = [];
    results.forEach(function (r) {
      var c = r.committee || "Unknown";
      if (!counts[c]) { counts[c] = 0; order.push(c); }
      counts[c]++;
    });
    order.sort();

    var ctx = document.getElementById("chart").getContext("2d");
    var config = {
      type: "bar",
      data: {
        labels: order,
        datasets: [{
          label: "Matching paragraphs",
          data: order.map(function (c) { return counts[c]; }),
          backgroundColor: "#1f6fb2"
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: { legend: { display: false } },
        scales: {
          y: { beginAtZero: true, ticks: { precision: 0 }, title: { display: true, text: "Matching paragraphs" } },
          x: { title: { display: true, text: "Committee" } }
        }
      }
    };
    if (chart) {
      chart.data = config.data;
      chart.options = config.options;
      chart.update();
    } else if (window.Chart) {
      chart = new window.Chart(ctx, config);
    }
  }

  function runSearch() {
    var st = computeResults();
    var results = st.results;

    var countline = document.getElementById("countline");
    countline.textContent = results.length + " paragraph" + (results.length === 1 ? "" : "s") +
      " match out of " + records.length + ", filters: " + filterDescription(st) +
      (st.q ? ", search: “" + st.q + "”" : "") + ".";

    renderChart(results);

    var container = document.getElementById("results");
    container.innerHTML = "";

    if (!results.length) {
      var empty = document.createElement("div");
      empty.className = "empty";
      var main = document.createElement("p");
      main.textContent = "No paragraph contains these words.";
      var tip = document.createElement("p");
      tip.className = "tip";
      tip.textContent = "Tip: try OR to combine alternatives, or use fewer words (each word must appear in the paragraph).";
      empty.appendChild(main);
      empty.appendChild(tip);
      container.appendChild(empty);
      return;
    }

    results.forEach(function (r) {
      container.appendChild(renderCard(r, st.hlRe));
    });
  }

  // ---- events ----
  document.getElementById("searchBtn").addEventListener("click", runSearch);
  document.getElementById("q").addEventListener("keydown", function (e) {
    if (e.key === "Enter") runSearch();
  });
  committeeSel.addEventListener("change", runSearch);
  document.getElementById("yearFrom").addEventListener("input", runSearch);
  document.getElementById("yearTo").addEventListener("input", runSearch);

  runSearch();
})();
</script>
</body>
</html>
```