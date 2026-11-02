I built a search page over the General Comments paragraphs, with AND, OR, NOT, "exact phrases" and (brackets). It has committee and year filters, highlighted results, a Copy citation button on each result, and a clickable bar chart of hits per committee. Everything is computed by plain code in your browser, and no AI is used.

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>General Comments search</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
  :root { --accent:#1f6fb2; --ink:#1d2733; --muted:#5b6876; --line:#d9e0e7; --bg:#f5f8fb; }
  * { box-sizing:border-box; }
  body { margin:0; font:16px/1.5 system-ui,-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif; color:var(--ink); background:var(--bg); }
  main { max-width:1100px; margin:0 auto; padding:28px 20px 60px; }
  h1 { margin:0 0 4px; font-size:1.8rem; }
  h2 { font-size:1.1rem; margin:0 0 8px; }
  .lead { color:var(--muted); margin:0 0 20px; }
  .panel { background:#fff; border:1px solid var(--line); border-radius:8px; padding:18px 20px; margin-bottom:18px; }
  .note { font-size:.9rem; color:var(--muted); margin-top:10px; }
  .note b { color:var(--ink); }
  label { display:block; font-weight:600; font-size:.9rem; margin-bottom:4px; }
  input[type=search], select { width:100%; font:inherit; padding:9px 11px; border:1px solid #b9c4cf; border-radius:6px; background:#fff; color:var(--ink); }
  input[type=search] { font-size:1.1rem; }
  input:focus, select:focus, button:focus-visible { outline:3px solid #9cc7ea; outline-offset:1px; }
  .filters { display:grid; grid-template-columns:2fr 1fr 1fr 1.4fr; gap:14px; margin-top:14px; }
  .examples { margin-top:10px; font-size:.9rem; color:var(--muted); }
  .chip { display:inline-block; font:inherit; font-size:.85rem; background:#eaf2f9; color:var(--accent); border:1px solid #c5dbee; border-radius:14px; padding:2px 10px; margin:2px 4px 2px 0; cursor:pointer; }
  .chip:hover { background:#d9e9f6; }
  .interp { margin-top:10px; font-size:.95rem; }
  .interp code { background:#eef3f8; padding:2px 6px; border-radius:4px; word-break:break-word; }
  .err { color:#a33a1d; font-weight:600; }
  .two { display:grid; grid-template-columns:minmax(0,1fr); gap:18px; }
  .chartbox { position:relative; width:100%; }
  .summary { font-weight:600; margin:0 0 12px; }
  .card { background:#fff; border:1px solid var(--line); border-left:4px solid var(--accent); border-radius:6px; padding:14px 16px; margin-bottom:12px; }
  .meta { display:flex; flex-wrap:wrap; gap:8px 14px; align-items:center; font-size:.9rem; color:var(--muted); margin-bottom:6px; }
  .badge { background:var(--accent); color:#fff; border-radius:4px; padding:1px 8px; font-weight:700; font-size:.85rem; }
  .gctitle { font-weight:600; color:var(--ink); font-size:1rem; }
  .cite { font-size:.9rem; margin-bottom:8px; }
  .cite a { color:var(--accent); font-weight:600; }
  .para { white-space:pre-wrap; margin:6px 0 10px; }
  mark { background:#ffe58a; color:inherit; padding:0 1px; border-radius:2px; }
  button.act { font:inherit; font-size:.88rem; background:#fff; color:var(--accent); border:1px solid var(--accent); border-radius:6px; padding:4px 12px; cursor:pointer; }
  button.act:hover { background:#eaf2f9; }
  button.act.done { background:var(--accent); color:#fff; }
  button.more { font:inherit; background:var(--accent); color:#fff; border:0; border-radius:6px; padding:10px 20px; cursor:pointer; }
  .arts { font-size:.82rem; color:var(--muted); margin-left:6px; }
  .empty { color:var(--muted); padding:20px; text-align:center; }
  @media (max-width:800px){ .filters { grid-template-columns:1fr 1fr; } }
</style>
</head>
<body>
<main>
  <h1>General Comments: paragraph search</h1>
  <p class="lead" id="datainfo"></p>

  <section class="panel">
    <label for="q">Search the paragraphs</label>
    <input type="search" id="q" placeholder='e.g.  "fair trial" AND (children OR minors) NOT detention' autocomplete="off">
    <div class="examples">Examples (click to try):
      <button class="chip" data-q='torture OR "ill-treatment"'>torture OR "ill-treatment"</button>
      <button class="chip" data-q='"effective remedy" AND NOT compensation'>"effective remedy" AND NOT compensation</button>
      <button class="chip" data-q='(women OR girls) AND violence'>(women OR girls) AND violence</button>
    </div>
    <div class="filters">
      <div><label for="fc">Committee</label><select id="fc"></select></div>
      <div><label for="fy1">Year from</label><select id="fy1"></select></div>
      <div><label for="fy2">Year to</label><select id="fy2"></select></div>
      <div><label for="sort">Sort results by</label>
        <select id="sort">
          <option value="rel">Most matches first</option>
          <option value="new">Year, newest first</option>
          <option value="old">Year, oldest first</option>
          <option value="doc">Document and paragraph number</option>
        </select></div>
    </div>
    <div class="interp" id="interp"></div>
    <p class="note"><b>How the search works.</b> Write <b>AND</b>, <b>OR</b>, <b>NOT</b> in capital letters; lower-case "and" or "or" are searched as ordinary words. Two words side by side mean AND. Put <b>"exact phrases"</b> in quotes and use (brackets) to group. A word matches from the start of a word, so <i>tortur</i> finds <i>torture</i> and <i>tortured</i>. Upper/lower case is ignored. Order of precedence: NOT, then AND, then OR.</p>
  </section>

  <section class="panel">
    <h2>Hits per committee</h2>
    <div class="chartbox" id="chartbox"><canvas id="chart"></canvas></div>
    <p class="note" id="chartnote"></p>
    <p class="note"><b>How this is computed.</b> Each bar counts the paragraphs that satisfy your search words and the year range. It ignores the committee filter, so you can compare committees. Click a bar to filter to that committee (click again to clear). One paragraph counts once, however many times the words occur in it.</p>
  </section>

  <section>
    <p class="summary" id="summary"></p>
    <div id="results"></div>
    <div style="text-align:center"><button class="more" id="more" hidden>Show more</button></div>
    <p class="note"><b>How this is computed.</b> Every paragraph is tested one by one against your query and filters; nothing is estimated or summarised. The paragraph text is shown exactly as it is in the data. The yellow marks show the words from your query (words after NOT are not highlighted). "Most matches first" counts how many highlighted passages a paragraph contains.</p>
  </section>
</main>

<script>
(function(){
  const D = (window.WORKSHOP_DATA && window.WORKSHOP_DATA.gc) || {};
  const recs = Array.isArray(D.records) ? D.records : [];
  const $ = id => document.getElementById(id);
  const esc = s => String(s == null ? '' : s).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const PAGE = 50;
  let shownCount = PAGE, current = [], chart = null, chartCodes = [];

  // ---------- header ----------
  const years = recs.map(r => r.year).filter(y => typeof y === 'number');
  const minY = years.length ? Math.min(...years) : null, maxY = years.length ? Math.max(...years) : null;
  const committees = [...new Set(recs.map(r => r.committee).filter(Boolean))].sort();
  $('datainfo').textContent = recs.length
    ? `Source: ${D.source || D.title || 'UN treaty body General Comments'}. ${recs.length.toLocaleString()} paragraphs from ${committees.length} committees` + (minY !== null ? `, years ${minY}–${maxY}.` : '.')
    : 'No General Comment records were found in the data.';

  // ---------- filters ----------
  $('fc').innerHTML = '<option value="">All committees</option>' + committees.map(c => `<option value="${esc(c)}">${esc(c)}</option>`).join('');
  const yl = minY === null ? [] : Array.from({length: maxY - minY + 1}, (_, i) => minY + i);
  $('fy1').innerHTML = yl.map(y => `<option>${y}</option>`).join('');
  $('fy2').innerHTML = yl.map(y => `<option>${y}</option>`).join('');
  if (yl.length) { $('fy1').value = minY; $('fy2').value = maxY; }

  // ---------- query parser ----------
  function tokenize(s) {
    const t = []; let i = 0;
    while (i < s.length) {
      const c = s[i];
      if (/\s/.test(c)) { i++; continue; }
      if (c === '(' || c === ')') { t.push({k: c}); i++; continue; }
      if (c === '"' || c === '\u201c') {
        let j = i + 1; while (j < s.length && s[j] !== '"' && s[j] !== '\u201d') j++;
        const p = s.slice(i + 1, j).trim(); if (p) t.push({k: 'term', v: p, phrase: true});
        i = j + 1; continue;
      }
      let j = i; while (j < s.length && !/[\s()"\u201c\u201d]/.test(s[j])) j++;
      const w = s.slice(i, j);
      if (w === 'AND' || w === 'OR' || w === 'NOT') t.push({k: w}); else t.push({k: 'term', v: w});
      i = j;
    }
    return t;
  }
  function termRe(v, flags) {
    const body = v.trim().split(/\s+/).map(w => w.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')).join('\\s+');
    return new RegExp('(?<![\\p{L}\\p{N}])' + body, flags);
  }
  function parse(s) {
    const tk = tokenize(s); let p = 0, warn = '';
    const peek = () => tk[p] ? tk[p].k : null;
    function expr() {
      let left = andE();
      while (peek() === 'OR') { p++; const r = andE(); left = left && r ? {t: 'or', a: left, b: r} : (left || r); }
      return left;
    }
    function andE() {
      let left = notE();
      while (peek() && peek() !== 'OR' && peek() !== ')') {
        if (peek() === 'AND') p++;
        const r = notE(); left = left && r ? {t: 'and', a: left, b: r} : (left || r);
      }
      return left;
    }
    function notE() {
      if (peek() === 'NOT') { p++; const x = notE(); return x ? {t: 'not', x} : null; }
      return prim();
    }
    function prim() {
      const k = peek();
      if (k === 'term') { const x = tk[p++]; return {t: 'term', v: x.v, phrase: !!x.phrase, re: termRe(x.v, 'iu')}; }
      if (k === '(') { p++; const e = expr(); if (peek() === ')') p++; else warn = 'A closing bracket ) seems to be missing; the search assumed it at the end.'; return e; }
      if (k === 'AND' || k === 'OR') { p++; return prim(); }
      if (k === ')') { p++; warn = 'There is an extra closing bracket ); it was ignored.'; return null; }
      return null;
    }
    let ast = expr();
    while (p < tk.length) { if (tk[p].k === ')') warn = 'There is an extra closing bracket ); it was ignored.'; p++; const e = expr(); if (e) ast = ast ? {t: 'and', a: ast, b: e} : e; }
    return {ast, warn};
  }
  function evalN(n, text) {
    if (!n) return true;
    switch (n.t) {
      case 'term': return n.re.test(text);
      case 'and': return evalN(n.a, text) && evalN(n.b, text);
      case 'or': return evalN(n.a, text) || evalN(n.b, text);
      case 'not': return !evalN(n.x, text);
    }
    return true;
  }
  function positives(n, out) {
    if (!n) return out;
    if (n.t === 'term') out.push(n.v);
    else if (n.t === 'and' || n.t === 'or') { positives(n.a, out); positives(n.b, out); }
    return out; // NOT subtrees are skipped on purpose
  }
  function toStr(n) {
    if (!n) return '';
    if (n.t === 'term') return n.phrase ? `the exact phrase “${n.v}”` : `“${n.v}”`;
    if (n.t === 'not') return `NOT (${toStr(n.x)})`;
    return `(${toStr(n.a)} ${n.t.toUpperCase()} ${toStr(n.b)})`;
  }

  // ---------- main run ----------
  function run(resetPage) {
    if (resetPage) shownCount = PAGE;
    const qs = $('q').value.trim();
    const {ast, warn} = qs ? parse(qs) : {ast: null, warn: ''};
    const y1 = Number($('fy1').value), y2 = Number($('fy2').value);
    const fullRange = !yl.length || (y1 <= minY && y2 >= maxY);
    const com = $('fc').value;

    const terms = positives(ast, []).sort((a, b) => b.length - a.length);
    const hlRe = terms.length ? new RegExp(terms.map(v => termRe(v, '').source).join('|'), 'giu') : null;

    $('interp').innerHTML = qs
      ? (ast ? `Understood as: <code>${esc(toStr(ast))}</code>` : '<span class="err">Nothing searchable found in the search box, so all paragraphs are shown.</span>') + (warn ? `<br><span class="err">${esc(warn)}</span>` : '')
      : 'No search words entered: all paragraphs in the selected committees and years are listed.';

    const base = recs.filter(r => {
      const okY = typeof r.year === 'number' ? (r.year >= y1 && r.year <= y2) : fullRange;
      return okY && evalN(ast, String(r.text || ''));
    });

    // chart counts (ignore committee filter)
    const counts = {};
    base.forEach(r => { const c = r.committee || 'Unknown'; counts[c] = (counts[c] || 0) + 1; });
    drawChart(counts, com);

    const list = base.filter(r => !com || r.committee === com);
    const hits = new Map();
    if (hlRe) list.forEach(r => { const m = String(r.text || '').match(hlRe); hits.set(r, m ? m.length : 0); });
    const sort = $('sort').value;
    const docCmp = (a, b) => String(a.symbol).localeCompare(String(b.symbol)) || (a.paragraph - b.paragraph);
    list.sort((a, b) => {
      if (sort === 'new') return (b.year || 0) - (a.year || 0) || docCmp(a, b);
      if (sort === 'old') return (a.year || 0) - (b.year || 0) || docCmp(a, b);
      if (sort === 'rel' && hlRe) return (hits.get(b) - hits.get(a)) || docCmp(a, b);
      return docCmp(a, b);
    });
    current = list;

    const filt = [];
    if (qs) filt.push(`search: ${qs}`);
    if (com) filt.push(`committee: ${com}`);
    if (!fullRange) filt.push(`years ${y1}–${y2}`);
    $('summary').textContent = `${list.length.toLocaleString()} of ${recs.length.toLocaleString()} paragraphs match` + (filt.length ? ` (${filt.join('; ')})` : ' (no filter applied)') + '.';
    renderList(hlRe);
  }

  function hl(text, re) {
    if (!re) return esc(text);
    let out = '', last = 0, m; re.lastIndex = 0;
    while ((m = re.exec(text))) {
      if (!m[0]) { re.lastIndex++; continue; }
      out += esc(text.slice(last, m.index)) + '<mark>' + esc(m[0]) + '</mark>';
      last = m.index + m[0].length;
    }
    return out + esc(text.slice(last));
  }

  function renderList(hlRe) {
    const box = $('results');
    if (!current.length) { box.innerHTML = '<div class="panel empty">No paragraphs match. Try fewer words, OR instead of AND, or widen the years.</div>'; $('more').hidden = true; return; }
    const slice = current.slice(0, shownCount);
    box.innerHTML = slice.map((r, i) => {
      const arts = (r.cited_articles || []).length ? `<span class="arts">Articles cited: ${esc(r.cited_articles.join('; '))}</span>` : '';
      const sym = r.doc_url ? `<a href="${esc(r.doc_url)}" target="_blank" rel="noopener">${esc(r.symbol)}</a>` : esc(r.symbol);
      return `<article class="card">
        <div class="meta"><span class="badge">${esc(r.committee || '?')}</span>
          <span class="gctitle">${esc(r.short_title || r.title || '')}</span>
          <span>${r.year != null ? esc(r.year) : 'year unknown'}</span></div>
        <div class="cite">${sym}, para. ${esc(r.paragraph)}${arts}</div>
        <div class="para">${hl(String(r.text || ''), hlRe)}</div>
        <button class="act" data-i="${i}">Copy citation</button>
      </article>`;
    }).join('');
    const rest = current.length - slice.length;
    $('more').hidden = rest <= 0;
    $('more').textContent = `Show ${Math.min(PAGE, rest)} more (${rest.toLocaleString()} not yet shown)`;
  }

  // ---------- chart ----------
  function drawChart(counts, sel) {
    const entries = Object.entries(counts).sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]));
    chartCodes = entries.map(e => e[0]);
    $('chartnote').textContent = entries.length ? '' : 'No hits, so there is nothing to chart.';
    $('chartbox').style.display = entries.length ? '' : 'none';
    if (!window.Chart) { $('chartnote').textContent = 'The chart library is not available.'; return; }
    $('chartbox').style.height = (entries.length * 28 + 50) + 'px';
    const data = {
      labels: entries.map(e => `${e[0]} (${e[1].toLocaleString()})`),
      datasets: [{data: entries.map(e => e[1]), backgroundColor: entries.map(e => !sel || sel === e[0] ? '#1f6fb2' : '#b8cfe3'), borderRadius: 3}]
    };
    if (chart) { chart.data = data; chart.update('none'); return; }
    chart = new Chart($('chart'), {
      type: 'bar', data,
      options: {
        indexAxis: 'y', responsive: true, maintainAspectRatio: false, animation: false,
        plugins: {legend: {display: false}, tooltip: {callbacks: {label: c => `${c.parsed.x} matching paragraphs`}}},
        scales: {x: {beginAtZero: true, ticks: {precision: 0}, title: {display: true, text: 'Matching paragraphs'}}, y: {ticks: {font: {size: 13}}}},
        onClick: (e, els) => {
          if (!els.length) return;
          const code = chartCodes[els[0].index];
          $('fc').value = $('fc').value === code ? '' : code;
          run(true);
        }
      }
    });
  }

  // ---------- copy ----------
  function copyText(t) {
    const fallback = () => { const a = document.createElement('textarea'); a.value = t; a.style.position = 'fixed'; a.style.opacity = '0'; document.body.appendChild(a); a.select(); let ok = false; try { ok = document.execCommand('copy'); } catch (e) {} a.remove(); return ok; };
    if (navigator.clipboard && navigator.clipboard.writeText) return navigator.clipboard.writeText(t).then(() => true, () => fallback());
    return Promise.resolve(fallback());
  }
  $('results').addEventListener('click', e => {
    const b = e.target.closest('button[data-i]'); if (!b) return;
    const r = current[Number(b.dataset.i)]; if (!r) return;
    const cite = `${r.symbol}, para. ${r.paragraph}`;
    copyText(cite).then(ok => {
      b.textContent = ok ? 'Copied: ' + cite : 'Copy failed. Select the citation above by hand.';
      b.classList.add('done');
      setTimeout(() => { b.textContent = 'Copy citation'; b.classList.remove('done'); }, 2200);
    });
  });

  // ---------- events ----------
  let timer;
  $('q').addEventListener('input', () => { clearTimeout(timer); timer = setTimeout(() => run(true), 200); });
  ['fc', 'fy1', 'fy2', 'sort'].forEach(id => $(id).addEventListener('change', () => {
    if (id === 'fy1' && Number($('fy1').value) > Number($('fy2').value)) $('fy2').value = $('fy1').value;
    if (id === 'fy2' && Number($('fy2').value) < Number($('fy1').value)) $('fy1').value = $('fy2').value;
    run(true);
  }));
  $('more').addEventListener('click', () => { shownCount += PAGE; run(false); });
  document.querySelectorAll('.chip').forEach(c => c.addEventListener('click', () => { $('q').value = c.dataset.q; run(true); }));

  run(true);
})();
</script>
</body>
</html>
```