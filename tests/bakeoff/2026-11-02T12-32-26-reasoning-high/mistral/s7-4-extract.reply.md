I built a paragraph-checking tool for the attached raw PDF text of E/C.12/GC/27: it splits the pages into numbered paragraphs, compares each opening against the reference answer key, and flags where the converter damaged the text. You can sort differences first, expand any row for the full extracted paragraph beside the reference words, download a CSV, and inspect every removed header, footer and footnote line.

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Paragraph checker</title>
<style>
:root{--accent:#1f6fb2;--ink:#1c2733;--muted:#5b6b7b;--line:#dfe6ee;--bg:#f6f8fa}
*{box-sizing:border-box}
html,body{margin:0;padding:0}
body{font:16px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif;color:var(--ink);background:var(--bg)}
.wrap{max-width:1040px;margin:0 auto;padding:26px 20px 64px}
h1{font-size:1.45rem;line-height:1.3;margin:0 0 8px}
a{color:var(--accent)}
.meta{margin:2px 0;color:var(--muted)}
.card{background:#fff;border:1px solid var(--line);border-radius:10px;padding:16px 18px;margin:18px 0}
.stats{display:flex;gap:14px;flex-wrap:wrap}
.stat{flex:1 1 220px;border:1px solid var(--line);border-radius:10px;padding:12px 16px;background:#fbfcfe}
.stat .big{font-size:1.4rem;font-weight:700;color:var(--accent)}
.stat .lbl{color:var(--muted);font-size:.9rem;margin-top:2px}
.note{color:var(--muted);font-size:.9rem;margin:10px 0 0}
.controls{display:flex;align-items:center;gap:18px;flex-wrap:wrap;margin-bottom:6px}
button{background:var(--accent);color:#fff;border:0;border-radius:8px;padding:9px 16px;font-size:.95rem;cursor:pointer}
button:hover{background:#175a91}
label.chk{display:inline-flex;align-items:center;gap:8px;cursor:pointer;user-select:none}
.tablewrap{overflow-x:auto;margin-top:8px}
table{width:100%;border-collapse:collapse}
th,td{text-align:left;padding:8px 10px;border-bottom:1px solid var(--line);vertical-align:top;font-size:.94rem}
thead th{background:#eef3f8;font-size:.8rem;text-transform:uppercase;letter-spacing:.05em;color:#3d4c5c;white-space:nowrap}
tr.row{cursor:pointer}
tr.row:hover{background:#f2f7fc}
tr.row.diff{background:#fdf4f3}
tr.row.diff:hover{background:#fbeae8}
td.num{font-weight:700;white-space:nowrap}
.firstline{color:#33414f;min-width:280px}
.pill{display:inline-block;padding:2px 10px;border-radius:999px;font-size:.78rem;font-weight:700;white-space:nowrap}
.pill.ok{background:#e6f4ea;color:#1e7e34}
.pill.diff{background:#fbe9e7;color:#b3261e}
.pill.noref{background:#eceff3;color:#5b6b7b}
tr.detail td{background:#fbfcfe;padding:12px 10px}
.detail-flex{display:flex;gap:16px;flex-wrap:wrap}
.fulltext{flex:2 1 460px;white-space:pre-wrap;word-break:break-word;background:#fff;border:1px solid var(--line);border-radius:8px;padding:12px 14px;font-size:.92rem;max-height:360px;overflow:auto}
.refbox{flex:1 1 240px;background:#f2f7fc;border:1px solid var(--line);border-radius:8px;padding:12px 14px;font-size:.92rem}
details.card summary{cursor:pointer;font-weight:700}
.removed-list{list-style:none;margin:12px 0 0;padding:0;max-height:340px;overflow:auto;font-size:.88rem}
.removed-list li{padding:5px 0;border-bottom:1px dashed var(--line);color:#33414f}
.reason{color:var(--muted)}
</style>
</head>
<body>
<div class="wrap">
  <header>
    <h1 id="docTitle"></h1>
    <p class="meta">Symbol: <a id="docLink" target="_blank" rel="noopener"></a></p>
    <p class="meta" id="sourceLine"></p>
  </header>

  <section class="card">
    <div class="stats">
      <div class="stat"><div class="big" id="statParas">–</div><div class="lbl">paragraphs found / in the reference</div></div>
      <div class="stat"><div class="big" id="statFoots">–</div><div class="lbl">footnotes removed / in the reference</div></div>
      <div class="stat"><div class="big" id="statDiffs">–</div><div class="lbl">paragraphs whose opening words differ</div></div>
    </div>
    <p class="note">Found by the code from the page text; reference figures come from the file.</p>
    <p class="note"><strong>How this is computed:</strong> the pages are joined in order. Lines that are only a page number, the document symbol, or a “GE.” distribution code are dropped. Footnote lines (a small number followed by text, at the foot of a page) are removed and counted. A paragraph starts where a line begins with the next expected number and a full stop (“1.”, “2.”, …); all text until the next start belongs to that paragraph. “Differs” means the paragraph’s first six words do not match the reference’s, comparing word by word while ignoring case, punctuation and extra spaces.</p>
  </section>

  <section class="card">
    <div class="controls">
      <label class="chk"><input type="checkbox" id="diffFirst"> Show differences first</label>
      <button id="csvBtn" type="button">Download CSV</button>
    </div>
    <p class="note">One row per paragraph found in the page text; click a row to open the full paragraph exactly as extracted, with the reference’s opening words beside it. Every row links the symbol to the document.</p>
    <div class="tablewrap">
      <table>
        <thead><tr><th>#</th><th>Page</th><th>First line</th><th>Symbol</th><th>Opening words vs reference</th></tr></thead>
        <tbody id="tbody"></tbody>
      </table>
    </div>
  </section>

  <details class="card">
    <summary id="removedSummary">Lines removed as headers, footers and footnotes</summary>
    <ul class="removed-list" id="removedList"></ul>
  </details>
</div>

<script>
(function(){
"use strict";
var D = (window.WORKSHOP_DATA && window.WORKSHOP_DATA.pdf_text) || {};
var records = Array.isArray(D.records) ? D.records : [];
var symbol = D.symbol || "";
var docUrl = D.doc_url || "#";
var source = D.source || "";
var ref = D.reference || {};
var refFirst = ref.first_words || {};
var refParas = (typeof ref.paragraphs === "number") ? ref.paragraphs : null;
var refFoots = (typeof ref.footnotes === "number") ? ref.footnotes : null;

document.title = "Paragraph checker · " + (symbol || "UN document");
document.getElementById("docTitle").textContent = D.title || symbol || "UN document";
var link = document.getElementById("docLink");
link.textContent = symbol || docUrl;
link.href = docUrl;
document.getElementById("sourceLine").textContent =
  "Raw PDF text, " + records.length + " page" + (records.length === 1 ? "" : "s") + ", source: " + source;

/* ---------- split the raw page text into paragraphs ---------- */
function escRe(s){ return String(s).replace(/[.*+?^${}()|[\]\\]/g, "\\$&"); }
var symbolRe = symbol ? new RegExp("^" + escRe(symbol) + "\\s*\\d*$") : null;
function isDigits(l){ return /^\d{1,4}$/.test(l); }
function isDist(l){ return /^GE\.\s*\d/.test(l); }
function isFoot(l){ return /^\d{1,2}\s+\S/.test(l); }
function paraStart(l){ var m = l.match(/^(\d+)\.(?:\s+(.*))?$/); return m ? { num: +m[1], rest: m[2] || "" } : null; }

var removed = [];   /* {page, reason, line} */
var paras = [];     /* {num, page, lines: []} */
var footnotes = 0;
var expected = 1;
var current = null;
var frontSet = new Set();

for (var i = 0; i < records.length; i++){
  var rec = records[i];
  var page = rec.page;
  var rawLines = String(rec.text || "").split(/\r?\n/);
  var footMode = false;
  var prevBlank = false;
  for (var j = 0; j < rawLines.length; j++){
    var l = rawLines[j].trim();
    if (!l){
      if (current && !footMode) current.lines.push("");
      prevBlank = true;
      continue;
    }
    var wasBlank = prevBlank;
    prevBlank = false;
    if (isDigits(l)){ removed.push({ page: page, reason: "page number", line: l }); continue; }
    if (symbolRe && symbolRe.test(l)){ removed.push({ page: page, reason: "document symbol / footer", line: l }); continue; }
    if (isDist(l)){ removed.push({ page: page, reason: "distribution code", line: l }); continue; }
    if (!current){ frontSet.add(l); removed.push({ page: page, reason: "header (before the first paragraph)", line: l }); continue; }
    if (frontSet.has(l)){ removed.push({ page: page, reason: "repeated header", line: l }); continue; }
    var ps = paraStart(l);
    if (ps && ps.num === expected){
      current = { num: expected, page: page, lines: ps.rest ? [ps.rest] : [] };
      paras.push(current);
      expected++;
      footMode = false;
      continue;
    }
    if (isFoot(l) && (footMode || wasBlank)){
      footnotes++;
      footMode = true;
      removed.push({ page: page, reason: "footnote", line: l });
      continue;
    }
    if (footMode){
      removed.push({ page: page, reason: "footnote (continued)", line: l });
      continue;
    }
    current.lines.push(l);
  }
}

/* ---------- helpers ---------- */
function escHtml(s){ return String(s).replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;").replace(/"/g,"&quot;"); }
function normWords(s){
  return String(s).toLowerCase().split(/\s+/)
    .map(function(w){ return w.replace(/[^\p{L}\p{N}]/gu, ""); })
    .filter(Boolean);
}
function paraText(p){ return p.lines.join("\n").replace(/^\n+/, "").replace(/\n+$/, ""); }
function firstLine(p){
  var t = paraText(p).split("\n").map(function(s){ return s.trim(); }).filter(Boolean).join(" ").replace(/\s+/g, " ");
  return t.length > 90 ? t.slice(0, 90) + "…" : t;
}
function statusOf(p){
  if (p._st) return p._st;
  var key = String(p.num), st;
  if (!Object.prototype.hasOwnProperty.call(refFirst, key)){
    st = { code: "noref", label: "no reference" };
  } else {
    var a = normWords(paraText(p)).slice(0, 6);
    var b = normWords(refFirst[key]).slice(0, 6);
    var same = a.length === b.length && a.every(function(w, i){ return w === b[i]; });
    st = same ? { code: "ok", label: "matches" } : { code: "diff", label: "Differs" };
  }
  p._st = st;
  return st;
}

/* ---------- render ---------- */
var tbody = document.getElementById("tbody");
var diffFirstEl = document.getElementById("diffFirst");
var expanded = new Set();

function render(){
  var diffs = 0;
  for (var i = 0; i < paras.length; i++) if (statusOf(paras[i]).code === "diff") diffs++;
  document.getElementById("statParas").textContent = paras.length + (refParas != null ? " of " + refParas : "");
  document.getElementById("statFoots").textContent = footnotes + (refFoots != null ? " of " + refFoots : "");
  document.getElementById("statDiffs").textContent = diffs + " of " + paras.length;

  var order = paras.map(function(p, i){ return { p: p, i: i }; });
  if (diffFirstEl.checked){
    order.sort(function(a, b){
      var d = (statusOf(b.p).code === "diff" ? 1 : 0) - (statusOf(a.p).code === "diff" ? 1 : 0);
      return d || a.i - b.i;
    });
  }
  var html = "";
  if (!paras.length){
    html = '<tr><td colspan="5">No page text was found in the attached file.</td></tr>';
  }
  for (var k = 0; k < order.length; k++){
    var p = order[k].p, st = statusOf(p);
    html += '<tr class="row ' + st.code + '" data-num="' + p.num + '">'
      + "<td class='num'>" + p.num + "</td>"
      + "<td>" + p.page + "</td>"
      + "<td class='firstline'>" + escHtml(firstLine(p)) + "</td>"
      + '<td><a href="' + escHtml(docUrl) + '" target="_blank" rel="noopener">' + escHtml(symbol) + "</a></td>"
      + '<td><span class="pill ' + st.code + '">' + st.label + "</span></td>"
      + "</tr>";
    if (expanded.has(p.num)){
      var key = String(p.num);
      var refTxt = Object.prototype.hasOwnProperty.call(refFirst, key) ? refFirst[key] : null;
      html += '<tr class="detail"><td colspan="5"><div class="detail-flex">'
        + '<div class="fulltext">' + escHtml(paraText(p)) + "</div>"
        + '<div class="refbox"><strong>Reference opening words</strong><br>'
        + (refTxt != null ? escHtml(refTxt) : "No reference entry for paragraph " + p.num + ".")
        + "<br><br><strong>Result:</strong> " + st.label + "</div>"
        + "</div></td></tr>";
    }
  }
  tbody.innerHTML = html;
}

tbody.addEventListener("click", function(e){
  if (e.target.closest("a")) return;
  var tr = e.target.closest("tr.row");
  if (!tr) return;
  var n = +tr.getAttribute("data-num");
  if (expanded.has(n)) expanded.delete(n); else expanded.add(n);
  render();
});
diffFirstEl.addEventListener("change", render);

/* ---------- removed lines list ---------- */
document.getElementById("removedSummary").textContent =
  "Lines removed as headers, footers and footnotes (" + removed.length + ")";
document.getElementById("removedList").innerHTML = removed.map(function(r){
  var t = r.line.length > 160 ? r.line.slice(0, 160) + "…" : r.line;
  return "<li><span class='reason'>p. " + r.page + " · " + escHtml(r.reason) + "</span> — " + escHtml(t) + "</li>";
}).join("");

/* ---------- CSV download ---------- */
document.getElementById("csvBtn").addEventListener("click", function(){
  function f(v){ v = String(v); return '"' + v.replace(/"/g, '""') + '"'; }
  var rows = [["number", "page", "matches_reference", "text"]];
  for (var i = 0; i < paras.length; i++){
    var p = paras[i], st = statusOf(p).code;
    rows.push([p.num, p.page, st === "ok" ? "yes" : (st === "diff" ? "no" : "no reference"), paraText(p)]);
  }
  var csv = rows.map(function(r){ return r.map(f).join(","); }).join("\r\n");
  var blob = new Blob([csv], { type: "text/csv;charset=utf-8" });
  var a = document.createElement("a");
  a.href = URL.createObjectURL(blob);
  a.download = (symbol ? symbol.replace(/[^\w.-]+/g, "_") : "paragraphs") + "_paragraph_check.csv";
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  setTimeout(function(){ URL.revokeObjectURL(a.href); }, 2000);
});

render();
})();
</script>
</body>
</html>
```