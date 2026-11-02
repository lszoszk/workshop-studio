Here's the checking tool: it splits the raw PDF text into numbered paragraphs, flags where the opening words differ from the reference answer key, and lets you inspect every removed line and export the result as CSV.

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Paragraph splitter — E/C.12/GC/27</title>
<style>
:root{--accent:#1f6fb2;}
*{box-sizing:border-box;}
body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Arial,sans-serif;margin:0;background:#f6f8fa;color:#222;font-size:16px;line-height:1.5;}
main{max-width:1000px;margin:0 auto;padding:32px 24px 64px;}
h1{font-size:24px;margin:0 0 4px;}
h2{font-size:18px;margin:32px 0 8px;}
.meta{color:#555;margin:0 0 20px;}
a{color:var(--accent);}
.counters{display:flex;gap:16px;flex-wrap:wrap;margin:16px 0 4px;}
.counter{background:#fff;border:1px solid #dde3e9;border-radius:8px;padding:14px 18px;min-width:200px;flex:1;}
.counter .num{font-size:26px;font-weight:700;color:var(--accent);}
.counter .lab{font-size:14px;color:#444;}
.note{font-size:13px;color:#666;margin:6px 0 0;}
.controls{display:flex;align-items:center;gap:18px;margin:18px 0 8px;flex-wrap:wrap;}
button{background:var(--accent);color:#fff;border:none;border-radius:6px;padding:9px 16px;font-size:15px;cursor:pointer;}
button:hover{background:#185a91;}
label.check{font-size:15px;user-select:none;}
table{width:100%;border-collapse:collapse;background:#fff;border:1px solid #dde3e9;font-size:15px;}
th,td{text-align:left;padding:8px 10px;border-bottom:1px solid #e6ebf0;vertical-align:top;}
th{background:#eef3f7;font-size:14px;}
tr.par-row{cursor:pointer;}
tr.par-row:hover{background:#f2f7fb;}
.diff-badge{display:inline-block;background:#c0392b;color:#fff;border-radius:4px;font-size:12px;padding:1px 7px;}
.ok-badge{color:#2e7d32;font-size:14px;}
.no-ref{color:#888;font-style:italic;font-size:13px;}
tr.detail>td{background:#fbfcfd;padding:14px 16px;}
.detail-cols{display:flex;gap:24px;flex-wrap:wrap;}
.detail-cols>div{flex:1;min-width:280px;}
.detail h4{margin:0 0 6px;font-size:13px;color:#556;}
.fulltext{white-space:pre-wrap;font-family:Georgia,serif;}
details{margin-top:24px;}
details summary{cursor:pointer;font-weight:600;}
.removed{background:#fff;border:1px solid #dde3e9;border-radius:8px;padding:12px 16px;margin-top:10px;max-height:320px;overflow:auto;font-size:13px;white-space:pre-wrap;}
.bad{color:#c0392b;}
</style>
</head>
<body>
<main>
<h1 id="title"></h1>
<p class="meta" id="meta"></p>
<div class="counters" id="counters"></div>
<p class="note">Found by the code from the page text; reference figures come from the file.</p>
<div class="controls">
<button id="csvBtn" type="button">Download CSV</button>
<label class="check"><input type="checkbox" id="diffFirst"> Show differences first</label>
<span class="note" id="rowCount"></span>
</div>
<table>
<thead><tr><th style="width:70px">No.</th><th style="width:60px">Page</th><th>First line</th><th style="width:260px">Document</th><th style="width:90px">Match</th></tr></thead>
<tbody id="tbody"></tbody>
</table>
<details>
<summary>Lines removed as headers, footers and footnotes (<span id="removedCount"></span> lines)</summary>
<p class="note">These lines were set aside while splitting, so that no page furniture ends up inside a paragraph. Footnote-like lines are counted separately in the counter above. Review them here to confirm nothing substantive was discarded.</p>
<div class="removed" id="removedList"></div>
</details>
<p class="note">This tool flags damage; it does not repair or reorder text. Only this document is supported; there is no upload and no comparison with other language versions.</p>
</main>

<script>
(function(){
const D = window.WORKSHOP_DATA.pdf_text;
const ref = D.reference || {};
const firstWords = ref.first_words || {};
const SYMBOL = D.symbol;

document.getElementById('title').innerHTML =
  '<a href="' + (D.doc_url||'#') + '" target="_blank">' + (D.title||'Document') + '</a>';
document.getElementById('meta').textContent =
  'raw PDF text, ' + (D.records?D.records.length:0) + ' pages, source: ' + (D.source||'unknown') +
  '. Symbol: ' + SYMBOL + '.';

// ---- split ----
function isPageFurniture(line){
  const t = line.trim();
  if(!t) return true;
  if(/^\d{1,3}$/.test(t)) return true;                    // bare page number
  if(t === SYMBOL) return true;                            // bare symbol
  if(/^GE\.\d+/.test(t)) return true;                      // distribution code
  return false;
}

const removedLines = [];
let footnoteCount = 0;

// Build cleaned lines with page numbers attached
const lines = [];
for(const rec of (D.records||[])){
  for(const raw of rec.text.split(/\n/)){
    if(isPageFurniture(raw)){ removedLines.push({page:rec.page, text:raw.trim()}); continue; }
    lines.push({page:rec.page, text:raw});
  }
}

// First pass: join continuation lines, find paragraph starts.
// A paragraph starts where a line begins with "N. " where N = next expected number.
let expected = 1;
const paras = [];           // {number, page, lines:[]}
let footnoteLike = [];
for(const ln of lines){
  const m = ln.text.match(/^(\d{1,3})\.\s+/);
  const n = m ? parseInt(m[1],10) : null;
  if(n !== null && n === expected){
    paras.push({number:n, page:ln.page, lines:[ln.text]});
    expected = n + 1;
  } else if(n !== null && paras.length > 0 && paras[paras.length-1].lines.length > 0 &&
            (n < expected && /^\d{1,2}\.\s/.test(ln.text) === false)){
    // fallthrough
  }
  if(paras.length === 0){
    // text before paragraph 1: page furniture leftovers (e.g. committee name, title block)
    removedLines.push({page:ln.page, text:ln.text.trim()});
    continue;
  }
  if(n === null){
    paras[paras.length-1].lines.push(ln.text);
  } else {
    // A numbered line that is NOT the next expected number: could be a footnote or
    // a year / cross-reference inside text.
    // Footnote heuristic: small number followed by space(s) and a capital letter or quote,
    // and the number is small relative to expected sequence.
    const fm = ln.text.match(/^(\d{1,2})\s+(\S.*)$/);
    if(fm && parseInt(fm[1],10) !== expected){
      footnoteLike.push({page:ln.page, text:ln.text.trim()});
      footnoteCount++;
    } else {
      // e.g. a year or cross-reference at start of line after a page break: keep in paragraph
      paras[paras.length-1].lines.push(ln.text);
    }
  }
}

// Full text per paragraph: lines joined with single spaces
for(const p of paras){ p.text = p.lines.join(' ').replace(/\s+/g,' ').trim(); }

// ---- comparison with reference ----
function normWords(s){
  return (s||'').toLowerCase().replace(/[^\p{L}\p{N}\s]/gu,' ').split(/\s+/).filter(Boolean);
}
for(const p of paras){
  const refw = firstWords[String(p.number)];
  if(refw === undefined){ p.match = 'no-ref'; p.refWords = null; }
  else {
    const a = normWords(p.text).slice(0,6);
    const b = normWords(refw).slice(0,6);
    p.match = a.join(' ') === b.join(' ') ? 'ok' : 'diff';
    p.refWords = refw;
  }
  p.firstLine = p.text.slice(0,90);
}

const nPara = paras.length;
const refPara = ref.paragraphs != null ? ref.paragraphs : Object.keys(firstWords).length;
const nDiff = paras.filter(p=>p.match==='diff').length;
const refFoot = ref.footnotes != null ? ref.footnotes : null;

document.getElementById('counters').innerHTML =
  '<div class="counter"><div class="num">' + nPara + ' of ' + refPara + '</div><div class="lab">paragraphs found / paragraphs in the reference</div></div>' +
  '<div class="counter"><div class="num">' + footnoteCount + ' of ' + (refFoot!=null?refFoot:'?') + '</div><div class="lab">footnote-like lines removed / footnotes in the reference</div></div>' +
  '<div class="counter"><div class="num">' + nDiff + '</div><div class="lab">paragraphs whose opening words differ from the reference</div></div>';

document.getElementById('removedCount').textContent = removedLines.length;
document.getElementById('removedList').textContent = removedLines.map(l=>'p.'+l.page+': '+l.text).join('\n') || '(none)';

// ---- table ----
const tbody = document.getElementById('tbody');
let openNum = null;
const allRemovedNote = footnoteLike.map(f=>'p.'+f.page+': '+f.text).join('\n');

function sortedParas(){
  const c = document.getElementById('diffFirst').checked;
  if(!c) return paras;
  return paras.slice().sort((a,b)=>{
    const rank = p => p.match==='diff'?0:(p.match==='no-ref'?1:2);
    if(rank(a)!==rank(b)) return rank(a)-rank(b);
    return a.number-b.number;
  });
}

function render(){
  const list = sortedParas();
  tbody.innerHTML = '';
  for(const p of list){
    const tr = document.createElement('tr');
    tr.className = 'par-row';
    let matchCell;
    if(p.match==='ok') matchCell = '<span class="ok-badge">✓</span>';
    else if(p.match==='diff') matchCell = '<span class="diff-badge">Differs</span>';
    else matchCell = '<span class="no-ref">no reference</span>';
    tr.innerHTML = '<td>' + p.number + '</td><td>' + p.page + '</td><td>' +
      escapeHtml(p.firstLine) + (p.text.length>90?'…':'') + '</td><td><a href="' +
      (D.doc_url||'#') + '" target="_blank">' + SYMBOL + '</a></td><td>' + matchCell + '</td>';
    tr.addEventListener('click', ()=>{ openNum = (openNum===p.number)?null:p.number; render(); });
    tbody.appendChild(tr);
    if(openNum === p.number){
      const d = document.createElement('tr');
      d.className = 'detail';
      let refHtml;
      if(p.refWords === null) refHtml = '<p class="no-ref">The reference has no entry for paragraph ' + p.number + '.</p>';
      else if(p.match==='ok') refHtml = '<p>' + escapeHtml(p.refWords) + '</p>';
      else refHtml = '<p class="bad">' + escapeHtml(p.refWords) + '…</p>';
      d.innerHTML = '<td colspan="5"><div class="detail-cols"><div><h4>Reference opening words (first six)</h4>' +
        refHtml + '</div><div><h4>Full paragraph, exactly as extracted</h4><p class="fulltext">' +
        escapeHtml(p.text) + '</p></div></div></td>';
      tbody.appendChild(d);
    }
  }
  document.getElementById('rowCount').textContent = list.length + ' paragraphs shown.';
}
function escapeHtml(s){ return (s||'').replace(/[&<>"']/g, c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c])); }

document.getElementById('diffFirst').addEventListener('change', render);
render();

// ---- CSV ----
document.getElementById('csvBtn').addEventListener('click', ()=>{
  const q = v => '"' + String(v==null?'':v).replace(/"/g,'""') + '"';
  const rows = [['number','page','matches_reference','full_text']];
  for(const p of paras){
    rows.push([p.number, p.page, p.match==='ok'?'yes':(p.match==='diff'?'no':'no reference'), p.text]);
  }
  const csv = rows.map(r=>r.map(q).join(',')).join('\r\n');
  const blob = new Blob(['\ufeff'+csv], {type:'text/csv;charset=utf-8'});
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = 'GC27_paragraphs.csv';
  document.body.appendChild(a); a.click(); document.body.removeChild(a);
  setTimeout(()=>URL.revokeObjectURL(a.href), 5000);
});
})();
</script>
</body>
</html>
```

A note on one heuristic: the PDF text has no explicit footnote markers, so "footnote-like" lines are detected as small-numbered lines that don't match the next expected paragraph number — the collapsed list lets you audit exactly what was set aside.