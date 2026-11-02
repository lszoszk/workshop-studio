I built a search tool over the General Comments paragraphs with AND / OR / NOT / "exact phrase" search, committee and year filters, and highlighted results. Each result has a "Copy citation" button, and a bar chart shows hits per committee. The app shows how it read your query, and every paragraph appears in full as it is in the data.

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>General Comments: paragraph search</title>
<style>
  :root { --accent:#1f6fb2; --ink:#1d2733; --muted:#5b6876; --line:#d9e0e7; --bg:#f6f8fa; }
  * { box-sizing:border-box; }
  body { margin:0; background:var(--bg); color:var(--ink); font:16px/1.5 system-ui,-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif; }
  .wrap { max-width:1100px; margin:0 auto; padding:28px 20px 60px; }
  h1 { margin:0 0 4px; font-size:1.9rem; color:var(--accent); }
  h2 { font-size:1.15rem; margin:0 0 8px; }
  .desc { color:var(--muted); margin:0 0 20px; }
  .panel { background:#fff; border:1px solid var(--line); border-radius:8px; padding:18px 20px; margin-bottom:18px; }
  .searchrow { display:flex; gap:10px; }
  input[type=search] { flex:1; font-size:1.05rem; padding:10px 12px; border:1px solid #aab5c1; border-radius:6px; min-width:0; }
  select { font-size:1rem; padding:8px 10px; border:1px solid #aab5c1; border-radius:6px; background:#fff; max-width:100%; }
  button { font:inherit; cursor:pointer; border-radius:6px; border:1px solid var(--accent); background:var(--accent); color:#fff; padding:8px 16px; }
  button.ghost { background:#fff; color:var(--accent); padding:5px 12px; font-size:.9rem; }
  button:hover { filter:brightness(.95); }
  .filters { display:flex; flex-wrap:wrap; gap:18px; margin-top:14px; align-items:end; }
  .filters label { display:flex; flex-direction:column; font-size:.85rem; color:var(--muted); gap:3px; }
  .interp { margin-top:12px; font-size:.95rem; color:var(--muted); }
  .interp code { background:#eef3f8; padding:2px 6px; border-radius:4px; color:var(--ink); }
  .err { color:#a12622; font-weight:600; }
  .note { font-size:.88rem; color:var(--muted); margin-top:10px; border-left:3px solid var(--line); padding-left:10px; }
  details { margin-top:12px; font-size:.95rem; }
  details summary { cursor:pointer; color:var(--accent); }
  details ul { margin:8px 0 0; padding-left:20px; }
  .summary { font-size:1.1rem; margin:0 0 6px; }
  .summary b { color:var(--accent); font-size:1.3rem; }
  .chartbox { position:relative; width:100%; }
  .card { background:#fff; border:1px solid var(--line); border-radius:8px; padding:14px 18px; margin-bottom:12px; }
  .meta { display:flex; flex-wrap:wrap; gap:8px 12px; align-items:center; margin-bottom:8px; font-size:.95rem; }
  .badge { background:var(--accent); color:#fff; font-weight:600; border-radius:4px; padding:1px 8px; font-size:.85rem; }
  .gctitle { font-weight:600; }
  .meta a { color:var(--accent); }
  .yr { color:var(--muted); }
  .ptext { white-space:pre-wrap; margin:0; }
  .ptext.clamp { max-height:15em; overflow:hidden; position:relative; -webkit-mask-image:linear-gradient(#000 70%,transparent); mask-image:linear-gradient(#000 70%,transparent); }
  mark { background:#ffe08a; color:inherit; padding:0 1px; border-radius:2px; }
  .actions { margin-top:10px; display:flex; gap:8px; flex-wrap:wrap; }
  .more { text-align:center; margin:16px 0; }
  .empty { color:var(--muted); padding:20px; text-align:center; }
  [data-hidden] { display:none; }
</style>
</head>
<body>
<div class="wrap">
  <h1>General Comments: paragraph search</h1>
  <p class="desc" id="desc"></p>

  <div class="panel">
    <div class="searchrow">
      <input type="search" id="q" placeholder='e.g.  torture AND "non-refoulement"   or   detention NOT children' aria-label="Search words">
      <button id="go">Search</button>
    </div>
    <div class="interp" id="interp"></div>
    <details>
      <summary>How to write a search</summary>
      <ul>
        <li><b>Several words</b> are combined with AND: <code>torture detention</code> finds paragraphs containing both.</li>
        <li><b>AND, OR, NOT</b> must be typed in capitals: <code>torture OR "ill-treatment"</code>, <code>detention NOT children</code>.</li>
        <li><b>"Exact phrase"</b> in double quotes finds those words next to each other, in that order.</li>
        <li><b>Brackets</b> group: <code>(torture OR "ill-treatment") AND remedy</code>. NOT is applied first, then AND, then OR.</li>
        <li>A word matches whole words only. Add <code>*</code> to match word beginnings: <code>detain*</code> finds detained, detainee, detention…</li>
        <li>Upper and lower case do not matter. Leave the box empty to list every paragraph that passes the filters.</li>
      </ul>
    </details>
    <div class="filters">
      <label>Committee <select id="fc"></select></label>
      <label>Year from <select id="fy1"></select></label>
      <label>Year to <select id="fy2"></select></label>
      <label>Order
        <select id="fs">
          <option value="new">Newest first</option>
          <option value="old">Oldest first</option>
          <option value="com">Committee A–Z</option>
        </select>
      </label>
      <button class="ghost" id="reset">Reset all</button>
    </div>
  </div>

  <div class="panel">
    <p class="summary" id="summary"></p>
    <div class="note" id="filtnote"></div>
  </div>

  <div class="panel">
    <h2>Hits per committee</h2>
    <div class="chartbox" id="chartbox"><canvas id="chart"></canvas></div>
    <div class="empty" id="nochart" data-hidden>No hits to chart.</div>
    <div class="note"><b>How this is computed:</b> each bar counts the paragraphs that match your search words and the year range. It ignores the committee filter on purpose, so you can compare committees. Click a bar to filter the results to that committee. One paragraph is counted once.</div>
  </div>

  <h2>Matching paragraphs</h2>
  <div id="results"></div>
  <div class="more" id="more" data-hidden><button id="morebtn">Show more</button></div>
  <div class="note"><b>How this is computed:</b> the search compares your words with the exact paragraph text in the data; nothing is summarised, ranked by guesswork or estimated. Highlighted words are the positive search words (words after NOT are not highlighted). Citation format: <i>document symbol, para. number</i>.</div>
</div>

<script>
(function(){
const D = window.WORKSHOP_DATA || {};
const gc = D.gc || {};
const norm = s => String(s == null ? '' : s).replace(/[\u2018\u2019\u02bc]/g,"'").replace(/[\u201c\u201d]/g,'"');
const esc = s => String(s == null ? '' : s).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const escRe = s => s.replace(/[.*+?^${}()|[\]\\\/]/g,'\\$&');

const items = (Array.isArray(gc.records) ? gc.records : [])
  .filter(r => r && typeof r.text === 'string')
  .map(r => ({ r, n: norm(r.text), com: r.committee || 'Unknown' }));

const years = [...new Set(items.map(i => i.r.year).filter(y => typeof y === 'number'))].sort((a,b)=>a-b);
const minY = years.length ? years[0] : null, maxY = years.length ? years[years.length-1] : null;
const committees = [...new Set(items.map(i => i.com))].sort((a,b)=>a.localeCompare(b));
const $ = id => document.getElementById(id);

$('desc').textContent = items.length
  ? (gc.title || 'General Comments') + ' · Source: ' + (gc.source || 'UN treaty bodies') + ' · n = ' + items.length + ' paragraphs · ' +
    (minY !== null ? minY + '–' + maxY + ' · ' : '') + committees.length + ' committees'
  : 'No General Comment paragraphs were found in the data.';

// ---- filters
$('fc').innerHTML = '<option value="">All committees</option>' + committees.map(c => {
  const n = items.filter(i => i.com === c).length;
  return '<option value="' + esc(c) + '">' + esc(c) + ' (' + n + ')</option>';
}).join('');
const yopts = years.map(y => '<option value="' + y + '">' + y + '</option>').join('');
$('fy1').innerHTML = yopts; $('fy2').innerHTML = yopts;
if (minY !== null) { $('fy1').value = minY; $('fy2').value = maxY; }

// ---- query parser: OR < AND < NOT, brackets, "phrases", word*
function tokenize(q) {
  if ((q.match(/"/g) || []).length % 2) throw new Error('A quotation mark is not closed. Quotes must come in pairs.');
  const toks = [], re = /"([^"]*)"|\(|\)|[^\s()"]+/g; let m;
  while ((m = re.exec(q))) {
    if (m[1] !== undefined) { if (m[1].trim()) toks.push({t:'phrase', v:m[1].trim()}); }
    else if (m[0] === '(' || m[0] === ')') toks.push({t:m[0]});
    else if (m[0] === 'AND' || m[0] === 'OR' || m[0] === 'NOT') toks.push({t:m[0]});
    else toks.push({t:'word', v:m[0]});
  }
  return toks;
}
function mkTerm(v, phrase) {
  let s = v.trim(), prefix = false;
  if (!phrase && /\*$/.test(s)) { prefix = true; s = s.replace(/\*+$/, ''); }
  if (!s) throw new Error('A search word is empty (only "*").');
  const body = s.split(/\s+/).map(escRe).join('\\s+');
  const re = new RegExp('(?<![\\p{L}\\p{N}])' + body + (prefix ? '' : '(?![\\p{L}\\p{N}])'), 'iu');
  return { k:'term', re, label: phrase ? '"' + s + '"' : s + (prefix ? '*' : '') };
}
function parse(q) {
  const toks = tokenize(q); let p = 0;
  const peek = () => toks[p];
  function parseOr() {
    let left = parseAnd();
    while (peek() && peek().t === 'OR') { p++; left = { k:'or', a:left, b:parseAnd() }; }
    return left;
  }
  function parseAnd() {
    let left = parseNot();
    while (peek() && (peek().t === 'AND' || ['word','phrase','NOT','('].includes(peek().t))) {
      if (peek().t === 'AND') p++;
      left = { k:'and', a:left, b:parseNot() };
    }
    return left;
  }
  function parseNot() {
    if (peek() && peek().t === 'NOT') { p++; return { k:'not', a:parseNot() }; }
    return parsePrimary();
  }
  function parsePrimary() {
    const t = peek();
    if (!t) throw new Error('The search ends too early: a word is missing after an operator.');
    if (t.t === '(') {
      p++; const e = parseOr();
      if (peek() && peek().t === ')') p++; else throw new Error('A bracket is not closed.');
      return e;
    }
    if (t.t === 'word' || t.t === 'phrase') { p++; return mkTerm(t.v, t.t === 'phrase'); }
    throw new Error('Unexpected "' + (t.t === ')' ? ')' : t.t) + '": a search word or phrase was expected there.');
  }
  const ast = parseOr();
  if (p < toks.length) throw new Error('Unexpected "' + toks[p].t + '" in the search.');
  return ast;
}
function ev(n, text) {
  switch (n.k) {
    case 'term': return n.re.test(text);
    case 'and': return ev(n.a, text) && ev(n.b, text);
    case 'or': return ev(n.a, text) || ev(n.b, text);
    case 'not': return !ev(n.a, text);
  }
}
function show(n) {
  if (n.k === 'term') return n.label;
  if (n.k === 'not') return 'NOT ' + show(n.a);
  return '(' + show(n.a) + ' ' + n.k.toUpperCase() + ' ' + show(n.b) + ')';
}
function positives(n, neg, out) {
  if (n.k === 'term') { if (!neg) out.push(new RegExp(n.re.source, 'giu')); }
  else if (n.k === 'not') positives(n.a, !neg, out);
  else { positives(n.a, neg, out); positives(n.b, neg, out); }
  return out;
}
function highlight(text, regs) {
  const ranges = [];
  regs.forEach(re => { re.lastIndex = 0; let m; while ((m = re.exec(text))) { if (!m[0].length) { re.lastIndex++; continue; } ranges.push([m.index, m.index + m[0].length]); } });
  ranges.sort((a,b) => a[0]-b[0] || b[1]-a[1]);
  const merged = [];
  ranges.forEach(r => { const l = merged[merged.length-1]; if (l && r[0] <= l[1]) l[1] = Math.max(l[1], r[1]); else merged.push(r.slice()); });
  let out = '', pos = 0;
  merged.forEach(r => { out += esc(text.slice(pos, r[0])) + '<mark>' + esc(text.slice(r[0], r[1])) + '</mark>'; pos = r[1]; });
  return out + esc(text.slice(pos));
}

// ---- state + run
const PAGE = 25;
let results = [], shown = PAGE, regs = [], chart = null;

function run() {
  const q = norm($('q').value).trim();
  let ast = null, error = '';
  if (q) { try { ast = parse(q); } catch (e) { error = e.message; } }
  regs = ast ? positives(ast, false, []) : [];

  $('interp').innerHTML = error
    ? '<span class="err">Could not read the search: ' + esc(error) + '</span> Showing nothing until it is fixed.'
    : ast ? 'Read as: <code>' + esc(show(ast)) + '</code>'
          : 'No search words: every paragraph that passes the filters is listed.';

  let a = +$('fy1').value, b = +$('fy2').value;
  if (a > b) { const t = a; a = b; b = t; }
  const full = (a === minY && b === maxY);
  const com = $('fc').value;

  const searched = error ? [] : items.filter(i => {
    const y = i.r.year;
    const yOk = typeof y === 'number' ? (y >= a && y <= b) : full;
    return yOk && (!ast || ev(ast, i.n));
  });
  results = searched.filter(i => !com || i.com === com);

  const s = $('fs').value;
  const yv = i => typeof i.r.year === 'number' ? i.r.year : 0;
  results.sort((x, y) => {
    let d = 0;
    if (s === 'new') d = yv(y) - yv(x);
    else if (s === 'old') d = yv(x) - yv(y);
    else d = x.com.localeCompare(y.com) || yv(x) - yv(y);
    return d || String(x.r.symbol).localeCompare(String(y.r.symbol)) || (x.r.paragraph || 0) - (y.r.paragraph || 0);
  });
  shown = PAGE;

  $('summary').innerHTML = '<b>' + results.length + '</b> of ' + items.length + ' paragraphs match.';
  const f = [];
  f.push('Search: ' + (q ? (error ? '“' + q + '” (not readable)' : '“' + q + '”') : 'none'));
  f.push('Committee: ' + (com || 'all'));
  f.push('Years: ' + (minY === null ? 'n/a' : a + '–' + b));
  $('filtnote').textContent = 'Filters applied → ' + f.join(' · ');

  drawChart(searched, com);
  drawResults();
}

function drawChart(searched, com) {
  const counts = {};
  searched.forEach(i => counts[i.com] = (counts[i.com] || 0) + 1);
  const rows = Object.entries(counts).sort((a,b) => b[1]-a[1] || a[0].localeCompare(b[0]));
  if (chart) { chart.destroy(); chart = null; }
  const has = rows.length && window.Chart;
  $('chartbox').style.display = has ? '' : 'none';
  $('nochart').toggleAttribute('data-hidden', !!has || !!rows.length);
  if (!has) return;
  $('chartbox').style.height = (rows.length * 30 + 60) + 'px';
  chart = new Chart($('chart'), {
    type: 'bar',
    data: { labels: rows.map(r => r[0]), datasets: [{ data: rows.map(r => r[1]),
      backgroundColor: rows.map(r => !com || r[0] === com ? '#1f6fb2' : '#b9cfe3') }] },
    options: {
      indexAxis: 'y', responsive: true, maintainAspectRatio: false, animation: false,
      plugins: { legend: { display: false }, tooltip: { callbacks: { label: c => c.parsed.x + ' paragraphs' } } },
      scales: { x: { beginAtZero: true, ticks: { precision: 0 }, title: { display: true, text: 'Matching paragraphs' } } },
      onClick: (e, els) => { if (els.length) { const c = rows[els[0].index][0]; $('fc').value = ($('fc').value === c ? '' : c); run(); } },
      onHover: (e, els) => { e.native.target.style.cursor = els.length ? 'pointer' : 'default'; }
    }
  });
}

function card(i, idx) {
  const r = i.r, long = r.text.length > 1200;
  const cite = (r.symbol || '') + ', para. ' + (r.paragraph != null ? r.paragraph : '?');
  const sym = r.doc_url
    ? '<a href="' + esc(r.doc_url) + '" target="_blank" rel="noopener">' + esc(r.symbol) + '</a>'
    : esc(r.symbol);
  return '<div class="card" data-idx="' + idx + '">' +
    '<div class="meta"><span class="badge">' + esc(i.com) + '</span>' +
    '<span class="gctitle" title="' + esc(r.title) + '">' + esc(r.short_title || r.title || '(no title)') + '</span>' +
    '<span>' + sym + ', para. ' + esc(r.paragraph) + '</span>' +
    (r.year != null ? '<span class="yr">' + esc(r.year) + '</span>' : '') + '</div>' +
    '<p class="ptext' + (long ? ' clamp' : '') + '">' + highlight(i.n, regs) + '</p>' +
    '<div class="actions"><button class="ghost" data-act="copy" data-cite="' + esc(cite) + '">Copy citation</button>' +
    (long ? '<button class="ghost" data-act="expand">Show full paragraph (' + r.text.length + ' characters)</button>' : '') +
    '</div></div>';
}
function drawResults() {
  const box = $('results');
  if (!results.length) {
    box.innerHTML = '<div class="card empty">' + (items.length ? 'No paragraph matches this search and these filters.' : 'No data available.') + '</div>';
  } else {
    box.innerHTML = results.slice(0, shown).map(card).join('');
  }
  $('more').toggleAttribute('data-hidden', results.length <= shown);
  $('morebtn').textContent = 'Show more (' + Math.min(PAGE, results.length - shown) + ' of ' + (results.length - shown) + ' remaining)';
}
// card() used with map passes (item,index) -> idx is position in results

async function copyText(text) {
  try { await navigator.clipboard.writeText(text); return true; } catch (e) {}
  const ta = document.createElement('textarea');
  ta.value = text; ta.style.position = 'fixed'; ta.style.opacity = '0';
  document.body.appendChild(ta); ta.select();
  let ok = false; try { ok = document.execCommand('copy'); } catch (e) {}
  ta.remove(); return ok;
}
$('results').addEventListener('click', async e => {
  const btn = e.target.closest('button[data-act]'); if (!btn) return;
  if (btn.dataset.act === 'copy') {
    const ok = await copyText(btn.dataset.cite), old = 'Copy citation';
    btn.textContent = ok ? 'Copied: ' + btn.dataset.cite : 'Copy failed, select the text manually';
    setTimeout(() => btn.textContent = old, 2000);
  } else {
    const p = btn.closest('.card').querySelector('.ptext');
    const open = p.classList.toggle('clamp');
    btn.textContent = open ? btn.textContent.replace('Collapse paragraph', 'Show full paragraph') : 'Collapse paragraph';
    if (open) btn.textContent = 'Show full paragraph';
  }
});
$('morebtn').addEventListener('click', () => { shown += PAGE; drawResults(); });
$('go').addEventListener('click', run);
let t; $('q').addEventListener('input', () => { clearTimeout(t); t = setTimeout(run, 250); });
$('q').addEventListener('keydown', e => { if (e.key === 'Enter') { clearTimeout(t); run(); } });
['fc','fy1','fy2','fs'].forEach(id => $(id).addEventListener('change', run));
$('reset').addEventListener('click', () => {
  $('q').value = ''; $('fc').value = ''; $('fs').value = 'new';
  if (minY !== null) { $('fy1').value = minY; $('fy2').value = maxY; }
  run();
});
run();
})();
</script>
</body>
</html>
```