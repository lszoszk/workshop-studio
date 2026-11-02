Built the paragraph checker for E/C.12/GC/27: it splits the raw PDF text, compares against the reference answer key, and lets you download the result as CSV.

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Paragraph checker — E/C.12/GC/27</title>
<style>
  :root { --accent:#1f6fb2; }
  * { box-sizing:border-box; }
  body { margin:0; font-family:-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
         background:#f6f8fa; color:#222; font-size:16px; line-height:1.5; }
  header, main { max-width:1000px; margin:0 auto; padding:24px 20px; }
  h1 { font-size:1.5rem; margin:0 0 4px; }
  h1 a { color:var(--accent); text-decoration:none; }
  .sub { color:#555; margin:0 0 20px; }
  .counters { display:flex; gap:14px; flex-wrap:wrap; margin-bottom:6px; }
  .counter { background:#fff; border:1px solid #dde3e9; border-radius:8px; padding:12px 16px; min-width:180px; }
  .counter .num { font-size:1.6rem; font-weight:600; color:var(--accent); }
  .counter.warn .num { color:#b23a1f; }
  .counter .lbl { font-size:.85rem; color:#555; }
  .how { font-size:.85rem; color:#666; margin:8px 0 20px; }
  .controls { display:flex; align-items:center; gap:16px; margin-bottom:14px; flex-wrap:wrap; }
  button { background:var(--accent); color:#fff; border:none; border-radius:6px;
           padding:9px 16px; font-size:.95rem; cursor:pointer; }
  button:hover { background:#175a91; }
  label.chk { font-size:.95rem; }
  table { width:100%; border-collapse:collapse; background:#fff; border:1px solid #dde3e9; border-radius:8px; overflow:hidden; }
  th, td { text-align:left; padding:9px 12px; border-bottom:1px solid #e8edf2; vertical-align:top; }
  th { background:#eef3f8; font-size:.85rem; text-transform:uppercase; letter-spacing:.03em; color:#3a4a5a; }
  td.sym a { color:var(--accent); text-decoration:none; }
  .mark { color:#b23a1f; font-weight:600; }
  .noref { color:#8a6d1a; font-weight:600; }
  .ok { color:#2e7d32; }
  tr.par-row { cursor:pointer; }
  tr.par-row:hover { background:#f0f6fb; }
  tr.diff-row td { background:#fdf3f1; }
  tr.expanded > td { background:#f7fafd; }
  tr.detail td { background:#fbfcfe; padding:14px 16px; }
  .detail .cols { display:flex; gap:20px; flex-wrap:wrap; }
  .detail .col { flex:1 1 380px; }
  .detail h4 { margin:0 0 6px; font-size:.85rem; color:#555; text-transform:uppercase; }
  .detail pre { white-space:pre-wrap; font-family:inherit; margin:0; }
  .detail .ref { color:#555; font-style:italic; }
  details.removed { margin-top:20px; }
  details.removed summary { cursor:pointer; font-weight:600; color:var(--accent); }
  details.removed ol { background:#fff; border:1px solid #dde3e9; border-radius:8px;
                       padding:16px 40px; font-size:.85rem; color:#555; }
  .firstline { overflow-wrap:anywhere; }
</style>
</head>
<body>
<header>
  <h1 id="doc-title"></h1>
  <p class="sub" id="doc-sub"></p>
</header>
<main>
  <div class="counters" id="counters"></div>
  <p class="how">Found by the code from the page text; reference figures come from the file.</p>

  <div class="controls">
    <label class="chk"><input type="checkbox" id="diff-first"> Show differences first</label>
    <button id="csv-btn">Download CSV</button>
  </div>

  <table id="tbl">
    <thead><tr><th>№</th><th>Page</th><th>First line</th><th>Symbol</th><th>Match</th></tr></thead>
    <tbody id="tbody"></tbody>
  </table>

  <details class="removed" id="removed">
    <summary>Lines removed as headers, footers and footnotes (<span id="rem-count"></span>)</summary>
    <ol id="rem-list"></ol>
  </details>
</main>

<script>
(function(){
  const D = window.WORKSHOP_DATA.pdf_text;
  const REF = D.reference || {};
  const firstWords = REF.first_words || {};

  document.getElementById('doc-title').innerHTML =
    '<a href="' + (D.doc_url||'#') + '" target="_blank">' + (D.symbol||D.title) + '</a>';
  document.getElementById('doc-sub').textContent =
    (D.title||'') + ' — raw PDF text, ' + D.records.length + ' pages, source: ' + (D.source||'unknown') + '.';

  // ---- normalize words: strip punctuation, lowercase ----
  function words(s){
    return (s||'').toLowerCase().replace(/[^\p{L}\p{N}]+/gu,' ').trim().split(/\s+/).filter(Boolean);
  }
  function firstSixWords(s){ return words(s).slice(0,6); }
  function sameWords(a,b){
    if(a.length===0 || b.length===0) return false;
    const n = Math.max(a.length,b.length);
    for(let i=0;i<n;i++){ if((a[i]||'')!==(b[i]||'')) return false; }
    return true;
  }

  // ---- join pages, tag lines with their page ----
  const lines = [];
  for(const rec of (D.records||[])){
    const ls = (rec.text||'').split(/\r?\n/);
    for(const l of ls){ lines.push({ page: rec.page, text: l }); }
  }

  // ---- classify lines ----
  const RE_PAGENUM = /^\s*\d{1,3}\s*$/;
  const RE_SYMBOL  = new RegExp('^\\s*' + (D.symbol||'E/C.12/GC/27').replace(/[.*+?^${}()|[\]\\]/g,'\\$&') + '\\s*$','i');
  const RE_GE      = /^\s*GE\.\s*\d[\d\-]*\s*$/i;
  const RE_FOOTNOTE= /^\s*(\d{1,2})\s+(\S.*)$/; // small number then text

  const kept = [];      // {page, text}
  const footnotes = []; // removed footnote lines
  const removedOther = [];

  for(const l of lines){
    const t = l.text;
    if(RE_PAGENUM.test(t) || RE_SYMBOL.test(t) || RE_GE.test(t)){
      removedOther.push({page:l.page, text:t});
      continue;
    }
    kept.push(l);
  }

  // ---- split into paragraphs ----
  // A paragraph starts at a line that begins with the next expected number + "."
  let expected = 1;
  const paras = []; // {num, startPage, lines:[]}
  let collecting = null;

  for(let i=0;i<kept.length;i++){
    const t = kept[i].text;
    const m = t.match(/^\s*(\d{1,3})\s*\.\s*$/); // number alone on line
    const m2 = t.match(/^\s*(\d{1,3})\s*\.\s+(\S.*)$/); // number + text
    let starts = false, num = null;
    if(m){ num = parseInt(m[1],10); starts = (num === expected); }
    else if(m2){ num = parseInt(m2[1],10); starts = (num === expected); }
    // Don't treat a bare number as a start if the following line looks like
    // continuation of previous paragraph? The rule: number alone on line,
    // paragraph on lines after. Keep simple: starts only if num === expected.
    if(starts){
      collecting = { num: num, startPage: kept[i].page, lines: [] };
      paras.push(collecting);
      if(m2) collecting.lines.push(m2[2]);
      expected = num + 1;
    } else if(collecting){
      collecting.lines.push(t);
    }
  }

  // ---- footnote removal: at foot of page, small number then text, AFTER paragraph split ----
  // Footnotes were lines that sat between numbered paragraphs. Detect them per paragraph:
  // trailing lines of each paragraph that begin with a small number followed by space and text,
  // and appear at the end (before the next paragraph start or page boundary).
  // Simpler & safer: scan the original kept lines; a line matching footnote pattern that is NOT
  // inside a numbered paragraph's leading content and sits in the last few lines before a page
  // change or next paragraph start is a footnote. We approximate: lines matching footnote pattern
  // that were never absorbed as the *first* line of a paragraph and appear after the last
  // paragraph start on their page.
  // Rebuild: track which kept-line indices belong to each paragraph.
  // Redo the walk with indices.
  const keptIdxParas = []; // per paragraph: array of kept indices
  {
    let exp = 1, cur = null;
    for(let i=0;i<kept.length;i++){
      const t = kept[i].text;
      const m  = t.match(/^\s*(\d{1,3})\s*\.\s*$/);
      const m2 = t.match(/^\s*(\d{1,3})\s*\.\s+(\S.*)$/);
      let starts=false, num=null;
      if(m){ num=parseInt(m[1],10); starts=(num===exp); }
      else if(m2){ num=parseInt(m[1],10); starts=(num===exp); }
      if(starts){
        cur = { idxs: [i] };
        keptIdxParas.push(cur);
        exp = num+1;
      } else if(cur){ cur.idxs.push(i); }
    }
  }

  // For each paragraph, strip trailing footnote lines: consecutive lines, from the end,
  // that match the footnote pattern AND whose number is small (<= 60) — but only if they
  // occur near a page end or before the next paragraph. Being conservative: strip from the
  // end only while lines match footnote pattern and the paragraph has more than one line left.
  for(let p=0;p<paras.length;p++){
    const idxs = keptIdxParas[p].idxs;
    while(idxs.length > 1){
      const lastIdx = idxs[idxs.length-1];
      const t = kept[lastIdx].text;
      const fm = t.match(RE_FOOTNOTE);
      if(fm && parseInt(fm[1],10) <= 80){
        footnotes.push({page: kept[lastIdx].page, text: t});
        idxs.pop();
      } else break;
    }
    paras[p].lines = idxs.map(i=>kept[i].text);
    paras[p].startPage = kept[idxs[0]].page;
  }

  // ---- compare with reference ----
  for(const p of paras){
    p.text = p.lines.join('\n').trim();
    p.firstLine = p.text.replace(/\s+/g,' ').slice(0,90);
    const ref = firstWords[String(p.num)];
    if(ref === undefined){
      p.match = 'noref';
    } else {
      p.match = sameWords(firstSixWords(p.text), firstSixWords(ref)) ? 'ok' : 'diff';
    }
  }

  const nFound = paras.length;
  const nRef = REF.paragraphs != null ? REF.paragraphs : Object.keys(firstWords).length;
  const nFn = footnotes.length;
  const nFnRef = REF.footnotes != null ? REF.footnotes : null;
  const nDiff = paras.filter(p=>p.match==='diff').length;

  // ---- counters ----
  const countersEl = document.getElementById('counters');
  function counter(num, lbl, warn){
    const d = document.createElement('div');
    d.className = 'counter' + (warn?' warn':'');
    d.innerHTML = '<div class="num"></div><div class="lbl"></div>';
    d.querySelector('.num').textContent = num;
    d.querySelector('.lbl').textContent = lbl;
    countersEl.appendChild(d);
  }
  counter(nFound + ' of ' + nRef, 'paragraphs found / in reference', nFound !== nRef);
  counter(nFn + (nFnRef!=null ? ' of ' + nFnRef : ''), 'footnotes removed' + (nFnRef==null?' (no reference figure)':' / in reference'), false);
  counter(nDiff, 'paragraphs whose opening words differ from the reference', nDiff>0);

  // ---- table ----
  const tbody = document.getElementById('tbody');
  const details = new Map(); // num -> detail row element

  function esc(s){ const d=document.createElement('div'); d.textContent=s; return d.innerHTML; }

  function render(){
    tbody.innerHTML = '';
    let list = paras.slice();
    if(document.getElementById('diff-first').checked){
      list.sort((a,b)=> (a.match==='diff'?0:1) - (b.match==='diff'?0:1) || a.num - b.num);
    }
    for(const p of list){
      const tr = document.createElement('tr');
      tr.className = 'par-row' + (p.match==='diff'?' diff-row':'');
      const symCell = '<a href="'+esc(D.doc_url||'#')+'" target="_blank">'+esc(D.symbol||'')+'</a>';
      let matchCell;
      if(p.match==='diff') matchCell = '<span class="mark">Differs</span>';
      else if(p.match==='noref') matchCell = '<span class="noref">no reference</span>';
      else matchCell = '<span class="ok">✓</span>';
      tr.innerHTML = '<td>'+p.num+'</td><td>'+p.startPage+'</td>'+
        '<td class="firstline">'+esc(p.firstLine)+(p.text.length>90?'…':'')+'</td>'+
        '<td class="sym">'+symCell+'</td><td>'+matchCell+'</td>';
      tr.addEventListener('click', ()=> toggleDetail(tr, p));
      tbody.appendChild(tr);
    }
  }

  function toggleDetail(tr, p){
    const existing = details.get(p.num);
    if(existing && existing.parentNode){
      existing.remove(); details.delete(p.num);
      tr.classList.remove('expanded');
      return;
    }
    // close others
    for(const [n,el] of details){ el.remove(); details.delete(n); }
    const d = document.createElement('tr');
    d.className = 'detail';
    const ref = firstWords[String(p.num)];
    let refHtml;
    if(ref === undefined) refHtml = '<p class="ref">no reference entry for this paragraph number</p>';
    else if(p.match==='ok') refHtml = '<p class="ref">'+esc(ref)+'</p>';
    else refHtml = '<p class="ref">'+esc(ref)+' <span class="mark">(reference words it was compared with)</span></p>';
    d.innerHTML = '<td colspan="5"><div class="cols">'+
      '<div class="col"><h4>Full paragraph, exactly as extracted (page '+p.startPage+')</h4><pre>'+esc(p.text)+'</pre></div>'+
      '<div class="col"><h4>Reference: first words</h4>'+refHtml+'</div></div></td>';
    tr.after(d);
    details.set(p.num, d);
    tr.classList.add('expanded');
  }

  document.getElementById('diff-first').addEventListener('change', render);
  render();

  // ---- removed lines list ----
  document.getElementById('rem-count').textContent = (removedOther.length + footnotes.length);
  const list = document.getElementById('rem-list');
  for(const r of removedOther){
    const li = document.createElement('li');
    li.textContent = '(p.' + r.page + ') ' + r.text;
    list.appendChild(li);
  }
  for(const f of footnotes){
    const li = document.createElement('li');
    li.textContent = '(p.' + f.page + ', footnote) ' + f.text;
    list.appendChild(li);
  }

  // ---- CSV ----
  function csvCell(v){
    v = (v==null?'':String(v));
    return '"' + v.replace(/"/g,'""') + '"';
  }
  document.getElementById('csv-btn').addEventListener('click', ()=>{
    const head = ['paragraph','page','matches_reference','full_text'];
    const rows = [head.map(csvCell).join(',')];
    for(const p of paras){
      let m;
      if(p.match==='ok') m='yes';
      else if(p.match==='diff') m='no';
      else m='no reference';
      rows.push([p.num, p.startPage, m, p.text].map(csvCell).join(','));
    }
    const blob = new Blob(['\ufeff' + rows.join('\r\n')], {type:'text/csv;charset=utf-8'});
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = (D.symbol||'document').replace(/[^\w\-]+/g,'_') + '_paragraphs.csv';
    document.body.appendChild(a); a.click(); a.remove();
    setTimeout(()=>URL.revokeObjectURL(a.href), 5000);
  });
})();
</script>
</body>
</html>
```

One note on the mechanism, visible in the app: the split only starts a paragraph at the *next expected* number, so years and cross-references never break the sequence, and footnote-looking lines at the foot of each paragraph are moved to the "removed" list rather than deleted silently.