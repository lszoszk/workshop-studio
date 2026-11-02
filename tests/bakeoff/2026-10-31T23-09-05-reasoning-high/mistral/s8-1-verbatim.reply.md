I built a self-contained search tool over the General Comments: a small query parser (AND / OR / NOT / "exact phrases" / parentheses, with implicit AND), committee and year dropdowns built from the data, verbatim paragraph results with `<mark>` highlighting, a per-committee hits bar chart (Chart.js, with a no-Chart fallback), and a "Copy citation" button that puts `symbol, para. N` on the clipboard.

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Search the General Comments of the UN treaty bodies</title>
<style>
  :root{
    --accent:#1f6fb2; --accent-dark:#185a92; --ink:#1c2733; --muted:#5b6b7b;
    --line:#dce3ea; --bg:#f4f6f9; --card:#ffffff;
  }
  *{box-sizing:border-box}
  html{font-size:16px}
  body{margin:0;background:var(--bg);color:var(--ink);
    font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif;line-height:1.55}
  .wrap{max-width:980px;margin:0 auto;padding:28px 20px 72px}
  header h1{font-size:1.65rem;margin:0 0 6px;color:#14324f}
  .desc{color:var(--muted);margin:0 0 4px;max-width:75ch}
  .note{font-size:.85rem;color:var(--muted);margin:.4rem 0 0}
  .card{background:var(--card);border:1px solid var(--line);border-radius:10px;
    padding:16px 18px;box-shadow:0 1px 2px rgba(20,50,79,.05)}
  .controls{margin:18px 0 14px}
  .search-row{display:flex;gap:10px}
  #q{flex:1;min-width:0;padding:12px 14px;font-size:1.05rem;border:1.5px solid #b7c5d3;border-radius:8px;background:#fff;color:var(--ink)}
  #q:focus{outline:none;border-color:var(--accent);box-shadow:0 0 0 3px rgba(31,111,178,.15)}
  .btn{background:var(--accent);color:#fff;border:none;border-radius:8px;padding:12px 18px;font-size:1rem;cursor:pointer}
  .btn:hover{background:var(--accent-dark)}
  .ghost-btn{background:#fff;color:var(--accent);border:1px solid var(--accent);border-radius:8px;padding:8px 14px;font-size:.9rem;cursor:pointer}
  .ghost-btn:hover{background:#eaf2f9}
  .help{font-size:.85rem;color:var(--muted);margin-top:10px;max-width:90ch}
  .help code{background:#eef2f6;border-radius:4px;padding:1px 5px;font-size:.8rem}
  .chips{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin-top:10px;font-size:.85rem;color:var(--muted)}
  .chip{background:#eaf2f9;color:var(--accent);border:1px solid #c6dcf0;border-radius:999px;padding:4px 12px;font-size:.82rem;cursor:pointer}
  .chip:hover{background:#d8e9f7}
  .filters{display:flex;flex-wrap:wrap;gap:14px;align-items:flex-end;margin-top:14px;padding-top:14px;border-top:1px solid var(--line)}
  .filters label{display:flex;flex-direction:column;gap:4px;font-size:.85rem;color:var(--muted)}
  .filters select{padding:8px 10px;border:1px solid #b7c5d3;border-radius:8px;background:#fff;font-size:.95rem;color:var(--ink);min-width:190px;max-width:100%}
  #err{display:none;margin:12px 0;padding:10px 14px;background:#fdecea;border:1px solid #f5c6c0;color:#8f1d14;border-radius:8px;font-size:.9rem}
  .stats-row{display:flex;flex-wrap:wrap;gap:18px;margin:16px 0 8px;align-items:stretch}
  .stats-text{flex:1 1 340px}
  #stats{font-size:1.05rem;margin:0}
  .chart-card{flex:1 1 380px;max-width:470px}
  .chart-wrap{position:relative;height:230px}
  .bar-row{display:flex;align-items:center;gap:8px;margin:5px 0;font-size:.85rem}
  .bar-label{width:70px;text-align:right;flex:none}
  .bar-track{flex:1;background:#eef2f6;border-radius:4px;height:16px;overflow:hidden}
  .bar-fill{display:block;height:100%;background:var(--accent)}
  .bar-val{width:36px;flex:none}
  .res-h{font-size:1.1rem;color:#14324f;margin:20px 0 10px}
  .rec{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:14px 18px;margin:0 0 14px}
  .rec-head{display:flex;flex-wrap:wrap;gap:10px;align-items:baseline}
  .badge{background:#e8f1f9;color:var(--accent);font-weight:600;font-size:.8rem;border-radius:6px;padding:2px 8px;flex:none}
  .gc-short{font-weight:600}
  .rec-meta{margin-left:auto;color:var(--muted);font-size:.88rem}
  .rec-meta a{color:var(--accent)}
  .gc-full{color:var(--muted);font-size:.85rem;margin-top:2px}
  .cite-row{display:flex;flex-wrap:wrap;gap:10px;align-items:center;margin:10px 0 8px}
  .cite-row code{background:#f2f5f8;border:1px solid var(--line);border-radius:6px;padding:4px 8px;font-size:.88rem}
  .copy-btn{background:var(--accent);color:#fff;border:none;border-radius:6px;padding:6px 12px;font-size:.85rem;cursor:pointer}
  .copy-btn:hover{background:var(--accent-dark)}
  .copy-btn.copied{background:#2e7d4f}
  .para{margin:0;background:#f7fafd;border-left:3px solid var(--accent);padding:10px 14px;border-radius:0 8px 8px 0;
    white-space:pre-wrap;word-break:break-word;font-size:.95rem}
  mark{background:#ffe9a8;border-radius:2px;padding:0 1px}
  .muted{color:var(--muted)}
  .more-wrap{margin:4px 0 20px;display:flex;gap:12px;align-items:center;flex-wrap:wrap}
  #empty{display:none;margin:18px 0;padding:18px;text-align:center;color:var(--muted)}
  footer{margin-top:28px;max-width:90ch}
</style>
</head>
<body>
<div class="wrap">

  <header>
    <h1>Search the General Comments of the UN treaty bodies</h1>
    <p class="desc" id="desc"></p>
    <p class="note">All counting, filtering, sorting, highlighting and the chart on this page are computed exactly in your browser from the loaded data — nothing is estimated, and no text is sent anywhere.</p>
  </header>

  <section class="card controls" aria-label="Search and filters">
    <div class="search-row">
      <input id="q" type="search" aria-label="Search the paragraph text"
             placeholder='e.g. women AND discrimination, or "persons with disabilities", or NOT reservations'>
      <button class="btn" id="goBtn" type="button">Search</button>
    </div>
    <div class="help">
      <strong>Syntax:</strong> <code>AND</code> <code>OR</code> <code>NOT</code> (any capitalisation) combine terms ·
      <code>"…"</code> = exact phrase · <code>( )</code> = grouping · words next to each other are combined with AND ·
      single words match whole words, case-insensitive; quoted phrases match the exact characters ·
      the search runs over the <strong>full text of every paragraph</strong> (committee, title and year are shown for context, not searched).
    </div>
    <div class="chips" id="chips">
      <span>Try:</span>
      <button type="button" class="chip" data-q="women AND discrimination">women AND discrimination</button>
      <button type="button" class="chip" data-q='"persons with disabilities"'>"persons with disabilities"</button>
      <button type="button" class="chip" data-q="NOT reservations">NOT reservations</button>
      <button type="button" class="chip" data-q="(detention OR custody) AND children">(detention OR custody) AND children</button>
    </div>
    <div class="filters">
      <label>Committee
        <select id="fCom"></select>
      </label>
      <label>Year
        <select id="fYear"></select>
      </label>
      <button class="ghost-btn" id="resetBtn" type="button">Reset all</button>
    </div>
  </section>

  <div id="err" role="alert"></div>

  <section class="stats-row" aria-label="Result counts and chart">
    <div class="stats-text">
      <p id="stats" aria-live="polite"></p>
      <p class="note" id="statsNote"></p>
    </div>
    <div class="card chart-card">
      <div class="chart-wrap" id="chartWrap"><canvas id="chart"></canvas></div>
      <p class="note" id="chartNote"></p>
    </div>
  </section>

  <h2 class="res-h">Results</h2>
  <section id="results" aria-label="Matching paragraphs"></section>
  <div class="more-wrap" id="moreWrap" hidden>
    <button class="ghost-btn" id="moreBtn" type="button"></button>
    <span class="note" id="shownNote"></span>
  </div>
  <div class="card" id="empty"></div>

  <footer class="note">
    Each result is one paragraph of a General Comment, reproduced <strong>verbatim</strong> from the source document
    (line breaks preserved) — only the matched words are highlighted, nothing is summarised.
    Cite as <em>symbol, para. N</em>; the “Copy citation” button puts exactly that on your clipboard.
    Every row shows the document symbol, linked to its UN document (<code>doc_url</code>) in a new tab.
  </footer>
</div>

<script>
(function(){
  'use strict';

  /* ---------- data ---------- */
  var DATA = window.WORKSHOP_DATA || {};
  var GC = DATA.gc || {};
  var raw = Array.isArray(GC.records) ? GC.records : [];
  var records = raw.map(function(r){
    return {
      symbol: r.symbol || '',
      doc_url: r.doc_url || '',
      paragraph: (r.paragraph == null ? '' : r.paragraph),
      committee: r.committee || '',
      year: (typeof r.year === 'number') ? r.year : null,
      title: r.title || '',
      short_title: r.short_title || '',
      text: (r.text == null) ? '' : String(r.text)
    };
  });
  function comOf(r){ return r.committee || '(unknown)'; }
  var committees = Array.from(new Set(records.map(comOf))).sort();
  var years = Array.from(new Set(records.map(function(r){ return r.year; })
        .filter(function(y){ return y != null; }))).sort(function(a,b){ return b - a; });
  var comTotals = {};
  records.forEach(function(r){ var k = comOf(r); comTotals[k] = (comTotals[k] || 0) + 1; });

  /* ---------- header ---------- */
  var yRange = years.length ? (Math.min.apply(null, years) + '–' + Math.max.apply(null, years)) : 'n/a';
  document.getElementById('desc').textContent =
    'Source: ' + (GC.title || 'General Comments of the UN treaty bodies') +
    (GC.source ? ' — ' + GC.source : '') + '. ' +
    records.length + ' paragraphs from ' + committees.length + ' committees, ' + yRange + '.';

  /* ---------- helpers ---------- */
  function esc(s){
    return String(s).replace(/[&<>"']/g, function(c){
      return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c];
    });
  }
  function escRe(s){ return String(s).replace(/[.*+?^${}()|[\]\\]/g, '\\$&'); }

  /* ---------- query parser: AND / OR / NOT / "phrases" / ( ) ---------- */
  function tokenize(q){
    var toks = [], i = 0, n = q.length;
    while(i < n){
      var c = q[i];
      if(/\s/.test(c)){ i++; continue; }
      if(c === '"'){
        var j = q.indexOf('"', i + 1);
        if(j === -1){ if(n > i + 1) toks.push({t:'phrase', v:q.slice(i+1)}); i = n; }
        else { if(j > i + 1) toks.push({t:'phrase', v:q.slice(i+1, j)}); i = j + 1; }
        continue;
      }
      if(c === '('){ toks.push({t:'lp'}); i++; continue; }
      if(c === ')'){ toks.push({t:'rp'}); i++; continue; }
      var j2 = i;
      while(j2 < n && !/[\s"()]/.test(q[j2])) j2++;
      var w = q.slice(i, j2); i = j2;
      var up = w.toUpperCase();
      if(up === 'AND') toks.push({t:'op', v:'AND'});
      else if(up === 'OR') toks.push({t:'op', v:'OR'});
      else if(up === 'NOT') toks.push({t:'op', v:'NOT'});
      else toks.push({t:'term', v:w});
    }
    return toks;
  }
  function leafRegex(tok){
    var e = escRe(tok.v);
    if(tok.t === 'phrase') return new RegExp(e, 'i');
    try { return new RegExp('(?<![A-Za-z0-9])' + e + '(?![A-Za-z0-9])', 'i'); }
    catch(_) { return new RegExp(e, 'i'); }
  }
  function parse(q){
    var toks = tokenize(q), pos = 0;
    function peek(){ return toks[pos]; }
    function parseOr(){
      var left = parseAnd();
      while(peek() && peek().t === 'op' && peek().v === 'OR'){
        pos++; left = {type:'or', children:[left, parseAnd()]};
      }
      return left;
    }
    function parseAnd(){
      var left = parseNot();
      for(;;){
        var tk = peek();
        if(!tk) break;
        if(tk.t === 'op' && tk.v === 'AND'){ pos++; left = {type:'and', children:[left, parseNot()]}; }
        else if(tk.t === 'op' && tk.v === 'NOT'){ left = {type:'and', children:[left, parseNot()]}; }
        else if(tk.t === 'term' || tk.t === 'phrase' || tk.t === 'lp'){ left = {type:'and', children:[left, parseNot()]}; }
        else break;
      }
      return left;
    }
    function parseNot(){
      var tk = peek();
      if(tk && tk.t === 'op' && tk.v === 'NOT'){ pos++; return {type:'not', child:parseNot()}; }
      return parsePrimary();
    }
    function parsePrimary(){
      var tk = peek();
      if(!tk) throw new Error('query ends unexpectedly');
      if(tk.t === 'lp'){
        pos++; var e = parseOr(); var c = peek();
        if(!c || c.t !== 'rp') throw new Error('missing )');
        pos++; return e;
      }
      if(tk.t === 'rp') throw new Error('unexpected )');
      if(tk.t === 'op') throw new Error('unexpected ' + tk.v);
      pos++;
      return {type:'leaf', kind:tk.t, value:tk.v, rx:leafRegex(tk)};
    }
    if(!toks.length) return null;
    var ast = parseOr();
    if(pos < toks.length) throw new Error('unexpected "' + (toks[pos].v || toks[pos].t) + '"');
    return ast;
  }
  function evalAst(n, text){
    if(n.type === 'leaf') return n.rx.test(text);
    if(n.type === 'and') return n.children.every(function(c){ return evalAst(c, text); });
    if(n.type === 'or')  return n.children.some(function(c){ return evalAst(c, text); });
    return !evalAst(n.child, text); /* not */
  }
  function collectLeaves(n, out){
    if(n.type === 'leaf') out.push(n);
    else if(n.type === 'not') collectLeaves(n.child, out);
    else n.children.forEach(function(c){ collectLeaves(c, out); });
  }
  function bounded(v){
    try { new RegExp('(?<![A-Za-z0-9])x(?![A-Za-z0-9])'); return '(?<![A-Za-z0-9])' + escRe(v) + '(?![A-Za-z0-9])'; }
    catch(_) { return escRe(v); }
  }
  function highlightRegex(leaves){
    if(!leaves.length) return null;
    var seen = {}, parts = [];
    leaves.forEach(function(l){
      var key = l.kind + ':' + l.value.toLowerCase();
      if(seen[key]) return; seen[key] = 1;
      parts.push(l.kind === 'phrase' ? escRe(l.value) : bounded(l.value));
    });
    if(!parts.length) return null;
    parts.sort(function(a,b){ return b.length - a.length; });
    try { return new RegExp('(' + parts.join('|') + ')', 'gi'); }
    catch(_) { return new RegExp('(' + leaves.map(function(l){ return escRe(l.value); }).join('|') + ')', 'gi'); }
  }
  function highlight(text, re){
    if(!re) return esc(text);
    re.lastIndex = 0;
    var parts = text.split(re), out = '';
    for(var i = 0; i < parts.length; i++){
      out += (i % 2 === 1) ? '<mark>' + esc(parts[i]) + '</mark>' : esc(parts[i]);
    }
    return out;
  }

  /* ---------- elements & state ---------- */
  var qEl = document.getElementById('q'),
      fCom = document.getElementById('fCom'),
      fYear = document.getElementById('fYear'),
      errEl = document.getElementById('err'),
      statsEl = document.getElementById('stats'),
      statsNote = document.getElementById('statsNote'),
      chartNote = document.getElementById('chartNote'),
      resultsEl = document.getElementById('results'),
      moreWrap = document.getElementById('moreWrap'),
      moreBtn = document.getElementById('moreBtn'),
      shownNote = document.getElementById('shownNote'),
      emptyEl = document.getElementById('empty');
  var PAGE = 150, shown = PAGE, hits = [], hlRe = null, chart = null;

  fCom.innerHTML = '<option value="*">All committees (' + records.length + ')</option>' +
    committees.map(function(c){
      return '<option value="' + esc(c) + '">' + esc(c) + ' (' + comTotals[c] + ')</option>';
    }).join('');
  fYear.innerHTML = '<option value="*">All years</option>' +
    years.map(function(y){ return '<option value="' + y + '">' + y + '</option>'; }).join('');

  if(!records.length){
    emptyEl.textContent = 'No General Comment paragraphs were loaded (WORKSHOP_DATA.gc.records is empty), so there is nothing to search.';
  }

  /* ---------- run search + filters ---------- */
  function run(){
    var q = qEl.value.trim(), ast = null, leaves = [], err = null;
    if(q){
      try { ast = parse(q); collectLeaves(ast, leaves); }
      catch(e){ err = e.message || String(e); }
    }
    hlRe = ast ? highlightRegex(leaves) : null;

    var com = fCom.value, yr = fYear.value;
    hits = records.filter(function(r){
      if(com !== '*' && comOf(r) !== com) return false;
      if(yr !== '*' && String(r.year) !== yr) return false;
      if(ast && !evalAst(ast, r.text)) return false;
      return true;
    });
    hits.sort(function(a,b){
      var ka = comOf(a), kb = comOf(b);
      if(ka !== kb) return ka < kb ? -1 : 1;
      var ya = a.year == null ? -1 : a.year, yb = b.year == null ? -1 : b.year;
      if(ya !== yb) return yb - ya;
      return (a.paragraph || 0) - (b.paragraph || 0);
    });
    shown = PAGE;

    if(err){
      errEl.style.display = 'block';
      errEl.textContent = 'The search could not be parsed (' + err + '), so the search filter was ignored and all paragraphs matching the committee/year filters are shown below. Valid syntax example: torture AND NOT "death penalty", or (women OR children) AND discrimination.';
    } else {
      errEl.style.display = 'none';
    }
    renderStats(q, err);
    renderChart();
    renderResults();
  }

  function renderStats(q, err){
    var f = [];
    f.push('search: ' + (q ? '“' + esc(q) + '”' : 'none (all paragraph texts)'));
    f.push('committee: ' + (fCom.value === '*' ? 'all' : esc(fCom.value)));
    f.push('year: ' + (fYear.value === '*' ? 'all' : esc(fYear.value)));
    statsEl.innerHTML = '<strong>' + hits.length + '</strong> matching paragraph' + (hits.length === 1 ? '' : 's') +
      ' of <strong>' + records.length + '</strong> loaded — ' + f.join(' · ');
    statsNote.textContent = 'How this is computed: the query is parsed (AND / OR / NOT, "exact phrases", parentheses; neighbouring words are ANDed) and tested against the full text of each of the ' +
      records.length + ' paragraphs; the committee and year filters are applied on top. Counts are exact, computed in this browser — not estimated.' +
      (err ? ' The query could not be parsed, so only the filters were applied.' : '');
  }

  function renderChart(){
    var byCom = {};
    hits.forEach(function(h){ var k = comOf(h); byCom[k] = (byCom[k] || 0) + 1; });
    var entries = Object.keys(byCom).map(function(k){ return [k, byCom[k]]; })
      .sort(function(a,b){ return b[1] - a[1] || (a[0] < b[0] ? -1 : 1); });
    chartNote.textContent = 'How this is computed: each of the ' + hits.length +
      ' matching paragraphs is counted exactly once, under its committee; the bars show the distribution of the current hits across committees.' +
      (hits.length ? '' : ' No hits, so there is nothing to chart.');
    if(window.Chart){
      if(!chart){
        chart = new Chart(document.getElementById('chart').getContext('2d'), {
          type: 'bar',
          data: { labels: [], datasets: [{ label: 'matching paragraphs', data: [], backgroundColor: '#1f6fb2', borderRadius: 4, maxBarThickness: 26 }] },
          options: {
            indexAxis: 'y', responsive: true, maintainAspectRatio: false,
            plugins: {
              legend: { display: false },
              tooltip: { callbacks: { label: function(c){ return ' ' + c.parsed.x + ' matching paragraph' + (c.parsed.x === 1 ? '' : 's'); } } }
            },
            scales: {
              x: { beginAtZero: true, ticks: { precision: 0 }, title: { display: true, text: 'matching paragraphs' } },
              y: { ticks: { autoSkip: false } }
            }
          }
        });
      }
      chart.data.labels = entries.map(function(e){ return e[0]; });
      chart.data.datasets[0].data = entries.map(function(e){ return e[1]; });
      chart.update();
    } else {
      var wrap = document.getElementById('chartWrap');
      if(!entries.length){ wrap.innerHTML = '<p class="muted">No hits to chart.</p>'; }
      else {
        var max = entries[0][1];
        wrap.innerHTML = entries.map(function(e){
          return '<div class="bar-row"><span class="bar-label">' + esc(e[0]) + '</span>' +
            '<span class="bar-track"><span class="bar-fill" style="width:' + Math.round(100 * e[1] / max) + '%"></span></span>' +
            '<span class="bar-val">' + e[1] + '</span></div>';
        }).join('');
      }
    }
  }

  function rowHtml(r){
    var sym = r.symbol || '(no symbol)';
    var link = r.doc_url
      ? '<a href="' + esc(r.doc_url) + '" target="_blank" rel="noopener noreferrer">' + esc(sym) + ' ↗</a>'
      : '<span>' + esc(sym) + '</span>';
    var cite = (r.paragraph !== '' && r.paragraph != null) ? sym + ', para. ' + r.paragraph : sym;
    var head = '<div class="rec-head"><span class="badge">' + esc(comOf(r)) + '</span>' +
      '<span class="gc-short">' + esc(r.short_title || r.title || '(untitled)') + '</span>' +
      '<span class="rec-meta">' + (r.year != null ? r.year : '') +
      (r.paragraph !== '' && r.paragraph != null ? ' · para. ' + esc(r.paragraph) : '') + ' · ' + link + '</span></div>';
    var full = (r.title && r.title !== r.short_title) ? '<div class="gc-full">' + esc(r.title) + '</div>' : '';
    var para = r.text ? highlight(r.text, hlRe) : '<span class="muted">(this record has no paragraph text)</span>';
    return '<article class="rec">' + head + full +
      '<div class="cite-row"><code>' + esc(cite) + '</code>' +
      '<button type="button" class="copy-btn" data-cite="' + esc(cite) + '" data-label="Copy citation">Copy citation</button></div>' +
      '<p class="para">' + para + '</p></article>';
  }

  function renderResults(){
    var slice = hits.slice(0, shown);
    resultsEl.innerHTML = slice.map(rowHtml).join('');
    emptyEl.style.display = hits.length ? 'none' : 'block';
    if(!hits.length && records.length){
      emptyEl.textContent = 'No paragraphs match this search and these filters. Try removing a NOT, clearing the search box, or choosing “All committees” / “All years”.';
    }
    moreWrap.hidden = !hits.length || shown >= hits.length;
    if(hits.length){
      moreBtn.textContent = 'Show more (' + (hits.length - shown) + ' remaining)';
      shownNote.textContent = 'Showing the first ' + slice.length + ' of ' + hits.length +
        ' hits, sorted by committee, then year (newest first), then paragraph number. Paragraph text is verbatim; only matches are highlighted.';
    } else {
      shownNote.textContent = '';
    }
  }

  /* ---------- copy citation ---------- */
  function copyText(text, btn){
    function flash(msg, ok){
      btn.textContent = msg;
      btn.classList.toggle('copied', !!ok);
      clearTimeout(btn._t);
      btn._t = setTimeout(function(){
        btn.textContent = btn.getAttribute('data-label') || 'Copy citation';
        btn.classList.remove('copied');
      }, 1600);
    }
    function fallback(){
      var ta = document.createElement('textarea');
      ta.value = text; ta.setAttribute('readonly', '');
      ta.style.cssText = 'position:fixed;top:0;left:0;opacity:0;';
      document.body.appendChild(ta); ta.select();
      var ok = false;
      try { ok = document.execCommand('copy'); } catch(_){}
      document.body.removeChild(ta);
      if(ok){ flash('Copied ✓', true); }
      else {
        var code = btn.parentElement.querySelector('code');
        if(code){
          var rg = document.createRange(); rg.selectNodeContents(code);
          var sel = window.getSelection(); sel.removeAllRanges(); sel.addRange(rg);
        }
        flash('Press Ctrl+C', false);
      }
    }
    if(navigator.clipboard && navigator.clipboard.writeText){
      navigator.clipboard.writeText(text).then(function(){ flash('Copied ✓', true); }).catch(fallback);
    } else fallback();
  }

  /* ---------- events ---------- */
  var deb = null;
  qEl.addEventListener('input', function(){ clearTimeout(deb); deb = setTimeout(run, 250); });
  qEl.addEventListener('keydown', function(e){ if(e.key === 'Enter'){ clearTimeout(deb); run(); } });
  document.getElementById('goBtn').addEventListener('click', run);
  fCom.addEventListener('change', run);
  fYear.addEventListener('change', run);
  document.getElementById('resetBtn').addEventListener('click', function(){
    qEl.value = ''; fCom.value = '*'; fYear.value = '*'; run();
  });
  document.getElementById('chips').addEventListener('click', function(e){
    var b = e.target.closest('.chip'); if(!b) return;
    qEl.value = b.getAttribute('data-q'); run();
  });
  resultsEl.addEventListener('click', function(e){
    var b = e.target.closest('.copy-btn'); if(!b) return;
    copyText(b.getAttribute('data-cite'), b);
  });
  moreBtn.addEventListener('click', function(){ shown += PAGE; renderResults(); });

  run();
})();
</script>
</body>
</html>
```