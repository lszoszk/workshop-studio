I built a paragraph-splitting tool for `WORKSHOP_DATA.pdf_text`: it strips page headers/footers and footnotes, extracts paragraphs starting at "N.", and checks each against the reference. It shows found-vs-reference counts, a clickable table with first lines and mismatch flags, and a CSV export — all offline in the browser.

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Numbered-paragraph splitter — UN document raw PDF text</title>
<style>
:root{
  --accent:#1f6fb2; --ink:#1d2b38; --muted:#5c6c7c; --bg:#f4f6f9;
  --line:#d8e0e9; --ok-bg:#e6f3ea; --ok-ink:#1d6b3a;
  --warn-bg:#fdf1de; --warn-ink:#8a5300; --warn-line:#f0d9b0;
}
*{box-sizing:border-box}
html,body{margin:0;padding:0}
body{background:var(--bg);color:var(--ink);font:16px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif}
.wrap{max-width:1040px;margin:0 auto;padding:26px 18px 64px}
h1{font-size:1.45rem;line-height:1.25;margin:0 0 8px}
h2{font-size:1.05rem;margin:0 0 8px}
.sub{margin:2px 0;color:var(--muted)}
a{color:var(--accent)}
.card{background:#fff;border:1px solid var(--line);border-radius:10px;padding:16px 18px;margin:14px 0}
.how{font-size:.86rem;color:var(--muted);background:#edf3f9;border-left:3px solid var(--accent);padding:8px 12px;border-radius:0 8px 8px 0;margin-top:10px}
.stats{display:flex;flex-wrap:wrap;gap:12px;margin:14px 0}
.stat{flex:1 1 170px;background:#fff;border:1px solid var(--line);border-radius:10px;padding:12px 14px}
.stat .big{font-size:1.7rem;font-weight:700;color:var(--accent);line-height:1.1}
.stat .lbl{font-weight:600;margin-top:2px}
.stat .note{font-size:.83rem;color:var(--muted);margin-top:5px}
.stat.warn{border-color:var(--warn-line);background:var(--warn-bg)}
.stat.warn .big{color:var(--warn-ink)}
.toolbar{display:flex;gap:10px;align-items:center;flex-wrap:wrap;margin:16px 0 10px}
button{background:var(--accent);color:#fff;border:0;border-radius:8px;padding:9px 16px;font-size:.95rem;cursor:pointer}
button.ghost{background:#fff;color:var(--accent);border:1px solid var(--accent)}
input[type=search]{padding:8px 12px;border:1px solid var(--line);border-radius:8px;font-size:.95rem;min-width:230px}
table{width:100%;border-collapse:collapse;background:#fff;table-layout:fixed}
th,td{padding:9px 12px;border-bottom:1px solid var(--line);text-align:left;vertical-align:top;font-size:.95rem}
th{background:#edf3f9;font-size:.78rem;text-transform:uppercase;letter-spacing:.05em;color:#3d4d5d}
th.c-num{width:58px} th.c-page{width:90px} th.c-badge{width:140px}
tbody tr.data{cursor:pointer}
tbody tr.data:hover{background:#f1f7fc}
tr.data.diff{background:var(--warn-bg)}
tr.data.diff:hover{background:#fae8c8}
td.num{font-weight:700}
td.firstline{overflow:hidden;text-overflow:ellipsis;white-space:nowrap;color:#33424f}
.badge{display:inline-block;font-size:.76rem;font-weight:700;padding:2px 9px;border-radius:999px;white-space:nowrap}
.badge.ok{background:var(--ok-bg);color:var(--ok-ink)}
.badge.diff{background:#f6dfae;color:var(--warn-ink)}
.badge.noref{background:#e7edf3;color:var(--muted)}
tr.detail td{background:#fbfcfe}
.full{white-space:pre-wrap;word-break:break-word;background:#fff;border:1px solid var(--line);border-radius:8px;padding:12px 14px;margin:10px 0;max-height:360px;overflow:auto;font-size:.93rem}
.meta{font-size:.88rem;color:var(--muted)}
.meta b{color:var(--ink)}
.notice{background:#fff;border:1px solid var(--line);border-radius:10px;padding:20px}
footer{margin-top:22px;color:var(--muted);font-size:.85rem}
</style>
</head>
<body>
<div class="wrap">
  <div id="head"></div>
  <div id="stats"></div>
  <div class="card">
    <h2>How this is computed</h2>
    <div id="method"></div>
  </div>
  <div class="toolbar">
    <button id="csvBtn" type="button">Download CSV</button>
    <button id="toggleAll" type="button" class="ghost">Expand all</button>
    <input id="filter" type="search" placeholder="Filter by number or text…">
    <span class="meta" id="shown"></span>
  </div>
  <div class="card" style="padding:0;overflow:hidden">
    <table id="tbl">
      <thead><tr><th class="c-num">¶</th><th class="c-page">Page</th><th>First line of the paragraph</th><th class="c-badge">First words vs reference</th></tr></thead>
      <tbody id="tbody"></tbody>
    </table>
  </div>
  <div class="how" id="tableNote"></div>
  <footer>All counting, filtering, sorting and CSV generation are done by this script in your browser from <code>window.WORKSHOP_DATA.pdf_text</code>. No data leaves the page; no model is called.</footer>
</div>

<script>
(function(){
"use strict";
var DATA = window.WORKSHOP_DATA || {};
var pdf = DATA.pdf_text || null;
var head = document.getElementById("head");
var stats = document.getElementById("stats");
var tbody = document.getElementById("tbody");

function esc(s){
  return String(s==null?"":s).replace(/[&<>"']/g,function(c){
    return {"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c];
  });
}

if(!pdf || !Array.isArray(pdf.records) || pdf.records.length===0){
  head.innerHTML = '<h1>Numbered-paragraph splitter</h1><p class="sub">No PDF text is loaded: <code>WORKSHOP_DATA.pdf_text</code> is missing or has no page records, so there is nothing to split.</p>';
  document.querySelector(".toolbar").style.display = "none";
  document.getElementById("tbl").style.display = "none";
  document.getElementById("tableNote").textContent = "";
  return;
}

var symbol = pdf.symbol || "";
var docUrl = pdf.doc_url || "";
var title = pdf.title || "(untitled)";
var source = pdf.source || "unknown source";
var ref = (pdf.reference && typeof pdf.reference === "object") ? pdf.reference : {};
var refParas = (typeof ref.paragraphs === "number") ? ref.paragraphs : null;
var refFoots = (typeof ref.footnotes === "number") ? ref.footnotes : null;
var refFW = (ref.first_words && typeof ref.first_words === "object") ? ref.first_words : {};
var pages = pdf.records.slice().sort(function(a,b){ return (Number(a && a.page)||0) - (Number(b && b.page)||0); });
var nPages = (typeof pdf.count === "number") ? pdf.count : pages.length;
var footnoteLimit = (refFoots && refFoots > 0) ? refFoots : 99;

var MONTHS = "January|February|March|April|May|June|July|August|September|October|November|December";
var symCore = symbol.replace(/[\d\s]/g,"");

/* Lines that are page furniture, not document text */
function isBoilerplate(line){
  var t = line.replace(/\s+/g," ").trim();
  if(!t) return true;
  if(symCore && t.replace(/[\d\s]/g,"") === symCore) return true;          /* symbol, with or without a page number */
  if(/^United Nations$/i.test(t)) return true;
  if(/^United Nations\s+(Economic and Social Council|General Assembly|Human Rights Council|Security Council|Trusteeship Council)$/i.test(t)) return true;
  if(/^(Economic and Social Council|General Assembly|Human Rights Council|Security Council|Trusteeship Council|International Court of Justice|Secretariat)$/i.test(t)) return true;
  if(/^(Distr|Distribution|Original|Language|Status)\s*[.:]/i.test(t)) return true;
  if(new RegExp("^\\d{1,2}\\s+(?:"+MONTHS+")\\s+\\d{4}\\.?$","i").test(t)) return true;
  if(new RegExp("^(?:"+MONTHS+")\\s+\\d{4}\\.?$","i").test(t)) return true;
  if(/^\d{1,4}$/.test(t)) return true;                                     /* lone page number */
  if(/^GE\.\d+/i.test(t)) return true;
  if(/^[-_—]{3,}$/.test(t)) return true;                                   /* horizontal rules */
  if(/^[*\s]{3,}$/.test(t)) return true;                                   /* "* * *" separators */
  return false;
}

/* Split into numbered paragraphs; keep footnotes out of the text */
var paras = [];
var cur = null;
var lastFoot = 0;
var footnoteCount = 0;

pages.forEach(function(p){
  var pageNo = (p && p.page != null) ? p.page : "?";
  var lines = String((p && p.text) || "").split(/\r?\n/);
  var footnoteMode = false;
  for(var i=0;i<lines.length;i++){
    if(isBoilerplate(lines[i])) continue;
    var t = lines[i].trim();
    var pm = t.match(/^(\d{1,3})\.(?:\s+(.*))?$/);                          /* "N." or "N. text" */
    if(pm){
      var n = parseInt(pm[1],10);
      if(!cur || n > cur.num){                                               /* paragraph numbers increase */
        cur = { num:n, lines: pm[2] ? [pm[2].trim()] : [], page: pageNo };
        paras.push(cur);
        footnoteMode = false;
        continue;
      }
    }
    if(footnoteMode) continue;
    var fm = t.match(/^(\d{1,2})\s+([A-Za-z(])/);                            /* footnote: "1 See …" */
    if(fm){
      var fn = parseInt(fm[1],10);
      if(fn <= footnoteLimit && fn > lastFoot){
        lastFoot = fn; footnoteCount++; footnoteMode = true; continue;
      }
    }
    if(/^[*†‡§¶]\s+\S/.test(t)){ footnoteCount++; footnoteMode = true; continue; }  /* "* …" footnote */
    if(cur) cur.lines.push(t);
  }
});

function flat(p){ return p.lines.join(" ").replace(/\s+/g," ").trim(); }
function firstWords(s,k){ return String(s||"").split(/\s+/).filter(Boolean).slice(0,k).join(" "); }
function norm(s){ return String(s==null?"":s).replace(/-\s+/g,"-").replace(/\s+/g," ").trim(); }

paras.forEach(function(p){
  p.text = flat(p);
  p.firstLine = p.lines.filter(function(l){ return l && l.trim(); })[0] || "";
  var rv = refFW[String(p.num)];
  if(rv == null){
    p.status = "noref"; p.foundWords = firstWords(p.text,6); p.refWords = "";
  } else {
    p.refWords = String(rv);
    var k = Math.max(6, p.refWords.split(/\s+/).filter(Boolean).length);
    p.foundWords = firstWords(p.text, k);
    p.status = (norm(p.foundWords) === norm(p.refWords)) ? "ok" : "diff";
  }
});
var diffs = paras.filter(function(p){ return p.status==="diff"; }).length;

/* Header: title + one-line description of the data */
var adoptedTxt = ref.adopted ? " · adopted " + esc(ref.adopted) : "";
head.innerHTML =
  '<h1>Split a UN document into its numbered paragraphs</h1>' +
  '<p class="sub"><b>' + esc(title) + '</b> — symbol <a href="' + esc(docUrl) + '" target="_blank" rel="noopener">' + esc(symbol || "(no symbol)") + '</a> (opens the UN document in a new tab)</p>' +
  '<p class="sub">Data: the raw PDF text of this one document, page by page — source: ' + esc(source) +
  ', n = ' + nPages + ' pages (' + pages.length + ' page records)' + adoptedTxt +
  '. Reference shipped with the data: ' + (refParas!=null ? refParas + " paragraphs" : "no paragraph count") +
  ', ' + (refFoots!=null ? refFoots + " footnotes" : "no footnote count") + '.</p>';

/* Method note */
document.getElementById("method").innerHTML =
  "<p style='margin:0 0 6px'>Each page's raw text is split into lines. Page furniture is dropped: the document symbol (with or without a page number), UN masthead lines, <i>Distr.:</i> / <i>Original:</i> lines, date lines, lone page numbers and rule lines. A new paragraph starts at any line beginning with <b>“N.”</b> where N is larger than the previous paragraph number. Footnotes — lines at the foot of a page beginning with a number (“1 …”) or with “*” — are counted separately and kept out of the paragraph text. Nothing is paraphrased: every paragraph is shown verbatim.</p>" +
  '<div class="how">All counting is done by this script in your browser, deterministically, from <code>window.WORKSHOP_DATA.pdf_text</code>. The “reference” numbers come from <code>pdf_text.reference</code>.</div>';

/* Summary numbers, each with its own note */
function stat(big, lbl, note, warn){
  return '<div class="stat' + (warn ? " warn" : "") + '"><div class="big">' + big + '</div><div class="lbl">' + lbl + '</div><div class="note">' + note + '</div></div>';
}
var paraNote = refParas!=null
  ? "Reference says " + refParas + " — " + (paras.length===refParas ? "exact match ✓" : "DIFFERENT ⚠")
  : "No reference count in the data.";
var footNote = refFoots!=null
  ? "Reference says " + refFoots + " — " + (footnoteCount===refFoots ? "exact match ✓" : "DIFFERENT ⚠")
  : "No reference count in the data.";
stats.innerHTML = '<div class="stats">' +
  stat(paras.length + (refParas!=null ? " / " + refParas : ""), "paragraphs found / reference",
       "Counted by this script: lines starting with “N.” (N increasing). " + paraNote,
       refParas!=null && paras.length!==refParas) +
  stat(footnoteCount + (refFoots!=null ? " / " + refFoots : ""), "footnotes found / reference",
       "Counted by this script: numbered or “*” lines at the foot of a page, kept out of the paragraphs. " + footNote,
       refFoots!=null && footnoteCount!==refFoots) +
  stat(diffs, "paragraphs differing from reference",
       "First words of each found paragraph compared with pdf_text.reference.first_words, of " + paras.length + " found.", diffs>0) +
  stat(pages.length, "pages of raw text", "Page records in pdf_text.records (n = " + nPages + " in the data header).") +
  '</div>';

/* Table */
var html = "";
paras.forEach(function(p, idx){
  var badge = p.status==="ok" ? '<span class="badge ok">✓ matches</span>'
            : p.status==="diff" ? '<span class="badge diff">⚠ differs</span>'
            : '<span class="badge noref">no reference</span>';
  html += '<tr class="data' + (p.status==="diff" ? " diff" : "") + '" data-idx="' + idx + '">'
       +  '<td class="num">' + p.num + '</td>'
       +  '<td>' + esc(p.page) + '</td>'
       +  '<td class="firstline" title="' + esc(p.firstLine) + '">' + esc(p.firstLine) + '</td>'
       +  '<td>' + badge + '</td></tr>';
  html += '<tr class="detail" data-idx="' + idx + '" style="display:none"><td colspan="4">'
       +  '<div class="meta">Paragraph <b>' + p.num + '</b> · starts on page <b>' + esc(p.page) + '</b> · document: <a href="' + esc(docUrl) + '" target="_blank" rel="noopener">' + esc(symbol) + '</a></div>'
       +  '<div class="full">' + esc(p.lines.join("\n")) + '</div>'
       +  '<div class="meta">First words found by this script: <b>' + esc(p.foundWords) + '</b><br>'
       +  'Reference first words: <b>' + esc(p.refWords || "(none in reference)") + '</b><br>'
       +  'Comparison: ' + badge + '</div>'
       +  '</td></tr>';
});
tbody.innerHTML = html || '<tr><td colspan="4">No numbered paragraphs were found in the raw text — the cleaning rules above may need adjusting for this document.</td></tr>';

document.getElementById("tableNote").innerHTML =
  "How this table is computed: rows are the paragraphs found by the rules above, in document order. “First line” is the first non-empty line of the cleaned paragraph. The badge compares the first six words of the paragraph with <code>reference.first_words</code> — ⚠ means they differ. Click any row to see the full verbatim paragraph text. The CSV download contains the same rows: paragraph, page, first words found, reference first words, match, full text.";

/* Interactions */
var open = {};
tbody.addEventListener("click", function(e){
  var tr = e.target.closest ? e.target.closest("tr.data") : null;
  if(!tr) return;
  var idx = tr.getAttribute("data-idx");
  var det = tbody.querySelector('tr.detail[data-idx="' + idx + '"]');
  if(!det) return;
  open[idx] = !open[idx];
  det.style.display = open[idx] ? "" : "none";
});

var allOpen = false;
document.getElementById("toggleAll").addEventListener("click", function(){
  allOpen = !allOpen;
  paras.forEach(function(p, idx){
    open[idx] = allOpen;
    var det = tbody.querySelector('tr.detail[data-idx="' + idx + '"]');
    if(det) det.style.display = allOpen ? "" : "none";
  });
  this.textContent = allOpen ? "Collapse all" : "Expand all";
});

document.getElementById("filter").addEventListener("input", function(){
  var q = this.value.trim().toLowerCase();
  var shown = 0;
  paras.forEach(function(p, idx){
    var hay = (p.num + " " + p.text).toLowerCase();
    var show = !q || hay.indexOf(q) !== -1;
    if(show) shown++;
    var d = tbody.querySelector('tr.data[data-idx="' + idx + '"]');
    var det = tbody.querySelector('tr.detail[data-idx="' + idx + '"]');
    if(d) d.style.display = show ? "" : "none";
    if(det) det.style.display = (show && open[idx]) ? "" : "none";
  });
  document.getElementById("shown").textContent = "Showing " + shown + " of " + paras.length + " paragraphs";
});
document.getElementById("shown").textContent = "Showing " + paras.length + " of " + paras.length + " paragraphs";

/* CSV download */
document.getElementById("csvBtn").addEventListener("click", function(){
  var rows = [["paragraph","starts_on_page","first_words_found","first_words_reference","matches_reference","full_text_verbatim"]];
  paras.forEach(function(p){
    rows.push([String(p.num), String(p.page), p.foundWords, p.refWords,
      p.status==="ok" ? "yes" : (p.status==="diff" ? "NO" : "no reference"),
      p.lines.join("\n")]);
  });
  var csv = "\uFEFF" + rows.map(function(r){
    return r.map(function(c){
      c = String(c==null ? "" : c);
      return '"' + c.replace(/"/g,'""') + '"';
    }).join(",");
  }).join("\r\n");
  var blob = new Blob([csv], {type:"text/csv;charset=utf-8"});
  var a = document.createElement("a");
  a.href = URL.createObjectURL(blob);
  a.download = (symbol ? symbol.replace(/[^\w.-]+/g,"_") : "document") + "_paragraphs.csv";
  document.body.appendChild(a);
  a.click();
  setTimeout(function(){ URL.revokeObjectURL(a.href); a.remove(); }, 600);
});
})();
</script>
</body>
</html>
```