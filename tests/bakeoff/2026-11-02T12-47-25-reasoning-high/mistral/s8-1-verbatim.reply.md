I'll build the General Comments search app: a single self-contained page with the AND/OR/NOT/phrase search, committee and year filters, a per-committee bar chart, and result cards with highlighting and a copy-citation button.html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>General Comments search</title>
<style>
  :root{
    --accent:#1f6fb2;
    --accent-dark:#175a92;
    --bg:#f4f6f9;
    --card:#ffffff;
    --border:#d9e1ea;
    --text:#1c2733;
    --muted:#5b6b7b;
  }
  *{box-sizing:border-box;}
  body{
    margin:0;
    background:var(--bg);
    color:var(--text);
    font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif;
    font-size:16px;
    line-height:1.5;
  }
  .wrap{max-width:960px;margin:0 auto;padding:24px 20px 60px;}
  h1{font-size:1.6rem;margin:0 0 6px;color:var(--accent-dark);}
  .source-line{color:var(--muted);margin:0 0 20px;font-size:0.95rem;}
  .panel{
    background:var(--card);
    border:1px solid var(--border);
    border-radius:8px;
    padding:16px 18px;
    margin-bottom:18px;
  }
  form.search-row{display:flex;gap:10px;flex-wrap:wrap;}
  #q{
    flex:1 1 320px;
    font-size:1rem;
    padding:9px 12px;
    border:1px solid var(--border);
    border-radius:6px;
    font-family:inherit;
  }
  #q:focus{outline:2px solid var(--accent);outline-offset:0;border-color:var(--accent);}
  button{
    font-family:inherit;
    font-size:0.95rem;
    background:var(--accent);
    color:#fff;
    border:none;
    border-radius:6px;
    padding:9px 16px;
    cursor:pointer;
  }
  button:hover{background:var(--accent-dark);}
  .help{color:var(--muted);font-size:0.9rem;margin:8px 0 0;}
  .help code{background:#eef2f7;padding:1px 5px;border-radius:4px;font-size:0.85rem;}
  .filters{display:flex;gap:14px;flex-wrap:wrap;align-items:flex-end;margin-top:14px;}
  .filters label{display:flex;flex-direction:column;font-size:0.85rem;color:var(--muted);gap:4px;}
  .filters select,.filters input{
    font-family:inherit;
    font-size:0.95rem;
    padding:7px 9px;
    border:1px solid var(--border);
    border-radius:6px;
    background:#fff;
    color:var(--text);
    min-width:120px;
  }
  .filters input{width:110px;}
  #count-line{font-weight:600;margin:0 0 10px;}
  .chart-note,.how{color:var(--muted);font-size:0.85rem;margin:6px 0 0;}
  .chart-box{position:relative;height:260px;margin-top:10px;}
  .card{
    background:var(--card);
    border:1px solid var(--border);
    border-radius:8px;
    padding:14px 18px;
    margin-bottom:14px;
  }
  .card-head{display:flex;flex-wrap:wrap;align-items:baseline;gap:8px 12px;margin-bottom:8px;}
  .badge{
    background:var(--accent);
    color:#fff;
    font-size:0.8rem;
    font-weight:700;
    letter-spacing:0.04em;
    padding:2px 9px;
    border-radius:20px;
    white-space:nowrap;
  }
  .gc-title{font-weight:600;}
  .year{color:var(--muted);font-size:0.9rem;}
  .symbol{font-weight:600;color:var(--accent);text-decoration:none;}
  .symbol:hover{text-decoration:underline;}
  .symbol.plain{color:var(--text);font-weight:600;}
  .para-label{color:var(--muted);font-size:0.9rem;}
  .para-text{margin:0 0 10px;white-space:pre-wrap;word-wrap:break-word;}
  mark{background:#ffe08a;color:inherit;padding:0 1px;border-radius:2px;}
  .copy-btn{background:#eef4fa;color:var(--accent-dark);border:1px solid var(--accent);font-weight:600;}
  .copy-btn:hover{background:#dcebf7;}
  .copy-btn.copied{background:#2e7d4f;color:#fff;border-color:#2e7d4f;}
  #empty{
    display:none;
    background:var(--card);
    border:1px dashed var(--border);
    border-radius:8px;
    padding:22px;
    text-align:center;
    color:var(--muted);
  }
  #empty strong{color:var(--text);display:block;margin-bottom:4px;}
</style>
</head>
<body>
<div class="wrap">
  <h1>General Comments search</h1>
  <p class="source-line" id="source-line"></p>

  <div class="panel">
    <form class="search-row" id="search-form">
      <input id="q" type="text" placeholder='Search the paragraph text, e.g. "best interests" AND child' autocomplete="off">
      <button type="submit">Search</button>
    </form>
    <p class="help">Words are combined with <strong>AND</strong> unless you write <strong>OR</strong>; <strong>NOT</strong> excludes a word; <strong>"quotes"</strong> find an exact phrase. Example: <code>"best interests" AND child</code></p>
    <div class="filters">
      <label>Committee
        <select id="committee-filter"></select>
      </label>
      <label>Year from
        <input id="year-from" type="number" placeholder="from" min="0">
      </label>
      <label>Year to
        <input id="year-to" type="number" placeholder="to" min="0">
      </label>
    </div>
  </div>

  <p id="count-line"></p>

  <div class="panel">
    <strong>Matching paragraphs per committee</strong>
    <div class="chart-box"><canvas id="chart"></canvas></div>
    <p class="how">How this is computed: each bar counts the paragraphs in the current result list (after the committee and year filters and the search) that belong to that committee. The bars add up to the N shown above.</p>
  </div>

  <div id="results"></div>
  <div id="empty">
    <strong>No paragraph contains these words</strong>
    Try OR instead of AND, or fewer words.
  </div>
</div>

<script>
(function(){
  "use strict";
  var DATA = window.WORKSHOP_DATA.gc;
  var records = (DATA && DATA.records) || [];

  var qInput = document.getElementById('q');
  var form = document.getElementById('search-form');
  var commSel = document.getElementById('committee-filter');
  var yearFrom = document.getElementById('year-from');
  var yearTo = document.getElementById('year-to');
  var countLine = document.getElementById('count-line');
  var resultsEl = document.getElementById('results');
  var emptyEl = document.getElementById('empty');
  var sourceLine = document.getElementById('source-line');

  /* ---------- header line, all read from the data ---------- */
  var years = records.map(function(r){ return r.year; }).filter(function(y){ return typeof y === 'number'; });
  var minY = years.length ? Math.min.apply(null, years) : null;
  var maxY = years.length ? Math.max.apply(null, years) : null;
  sourceLine.textContent =
    'Source: ' + (DATA.source || 'General Comments database') +
    ' · ' + records.length + ' paragraphs' +
    ' · years ' + (minY !== null ? minY + '–' + maxY : 'unknown');

  /* ---------- committee filter options ---------- */
  var committees = [];
  records.forEach(function(r){ if (r.committee && committees.indexOf(r.committee) === -1) committees.push(r.committee); });
  committees.sort();
  commSel.innerHTML = '<option value="All">All</option>' + committees.map(function(c){
    return '<option value="' + escAttr(c) + '">' + escHtml(c) + '</option>';
  }).join('');

  /* ---------- search parsing: AND / OR / NOT / "phrases" ---------- */
  function tokenize(q){
    var tokens = [], i = 0;
    while (i < q.length){
      var c = q[i];
      if (/\s/.test(c)) { i++; continue; }
      if (c === '"'){
        var end = q.indexOf('"', i + 1);
        if (end === -1){
          var rest = q.slice(i + 1).trim();
          if (rest) tokens.push({ type:'phrase', value: rest });
          break;
        }
        var ph = q.slice(i + 1, end).trim();
        if (ph) tokens.push({ type:'phrase', value: ph });
        i = end + 1;
      } else {
        var j = i;
        while (j < q.length && !/\s/.test(q[j]) && q[j] !== '"') j++;
        tokens.push({ type:'word', value: q.slice(i, j) });
        i = j;
      }
    }
    return tokens;
  }

  // Split on OR into groups; inside a group terms are ANDed; NOT marks the next term negative.
  function parseQuery(q){
    var tokens = tokenize(q);
    var groups = [[]];
    var neg = false;
    tokens.forEach(function(t){
      var up = t.value.toUpperCase();
      if (t.type === 'word' && up === 'OR'){ groups.push([]); neg = false; return; }
      if (t.type === 'word' && up === 'NOT'){ neg = true; return; }
      groups[groups.length - 1].push({ neg: neg, value: t.value, phrase: t.type === 'phrase' });
      neg = false;
    });
    return groups.map(function(g){
      return {
        pos: g.filter(function(x){ return !x.neg; }),
        neg: g.filter(function(x){ return x.neg; })
      };
    });
  }

  function escRe(s){ return s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'); }

  // Whole-word, case-insensitive; a quoted phrase matches that exact sequence of words.
  function termRegex(term){
    var words = term.phrase ? term.value.split(/\s+/).filter(Boolean) : [term.value];
    var body = words.map(escRe).join('\\s+');
    return new RegExp('(?<![\\p{L}\\p{N}_])' + body + '(?![\\p{L}\\p{N}_])', 'giu');
  }

  function matches(text, groups){
    if (!text) return false; // empty text never matches, but is still counted in M
    return groups.some(function(g){
      var posOk = g.pos.length === 0 || g.pos.some(function(t){ return termRegex(t).test(text); });
      if (!posOk) return false;
      return !g.neg.some(function(t){ return termRegex(t).test(text); });
    });
  }

  // Ranges of the original text covered by any positive term, merged, for highlighting.
  function highlightRanges(text, posTerms){
    var ranges = [];
    posTerms.forEach(function(t){
      var re = termRegex(t), m;
      while ((m = re.exec(text)) !== null){
        ranges.push([m.index, m.index + m[0].length]);
        if (m[0].length === 0) re.lastIndex++;
      }
    });
    ranges.sort(function(a,b){ return a[0] - b[0] || a[1] - b[1]; });
    var merged = [];
    ranges.forEach(function(r){
      var last = merged[merged.length - 1];
      if (last && r[0] <= last[1]) { if (r[1] > last[1]) last[1] = r[1]; }
      else merged.push([r[0], r[1]]);
    });
    return merged;
  }

  /* ---------- escaping & rendering ---------- */
  function escHtml(s){ return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;'); }
  function escAttr(s){ return escHtml(s).replace(/"/g,'&quot;'); }

  function renderHighlighted(text, ranges){
    var out = '', pos = 0;
    ranges.forEach(function(r){
      out += escHtml(text.slice(pos, r[0])) + '<mark>' + escHtml(text.slice(r[0], r[1])) + '</mark>';
      pos = r[1];
    });
    out += escHtml(text.slice(pos));
    return out;
  }

  /* ---------- filters + search ---------- */
  function filteredRecords(){
    var comm = commSel.value;
    var yf = yearFrom.value.trim(), yt = yearTo.value.trim();
    return records.filter(function(r){
      if (comm !== 'All' && r.committee !== comm) return false;
      if (yf !== '' || yt !== ''){
        if (typeof r.year !== 'number') return false; // unknown year excluded by a range
        if (yf !== '' && r.year < +yf) return false;
        if (yt !== '' && r.year > +yt) return false;
      }
      return true;
    });
  }

  function yearFilterDesc(){
    var yf = yearFrom.value.trim(), yt = yearTo.value.trim();
    if (yf === '' && yt === '') return 'all years';
    if (yf !== '' && yt !== '') return yf + '–' + yt;
    if (yf !== '') return 'from ' + yf;
    return 'to ' + yt;
  }

  var chart = null;

  function runSearch(){
    var query = qInput.value;
    var groups = parseQuery(query);
    var posTerms = [];
    groups.forEach(function(g){ g.pos.forEach(function(t){ posTerms.push(t); }); });

    var pool = filteredRecords();
    var results = pool.filter(function(r){ return matches(r.text, groups); });

    // newest General Comment first
    results.sort(function(a,b){
      var ya = typeof a.year === 'number' ? a.year : -Infinity;
      var yb = typeof b.year === 'number' ? b.year : -Infinity;
      if (yb !== ya) return yb - ya;
      var sa = a.symbol || '', sb = b.symbol || '';
      if (sa !== sb) return sa < sb ? -1 : 1;
      return (b.paragraph || 0) - (a.paragraph || 0);
    });

    var n = results.length, m = records.length;
    countLine.textContent = n + (n === 1 ? ' paragraph matches' : ' paragraphs match') +
      ' out of ' + m + ', filters: committee ' + (commSel.value === 'All' ? 'All' : commSel.value) +
      ', years ' + yearFilterDesc();

    // chart: matching paragraphs per committee, from the same result list
    var byComm = {};
    results.forEach(function(r){
      var c = r.committee || 'unknown';
      byComm[c] = (byComm[c] || 0) + 1;
    });
    var labels = Object.keys(byComm).sort(function(a,b){
      return byComm[b] - byComm[a] || (a < b ? -1 : 1);
    });
    var values = labels.map(function(l){ return byComm[l]; });
    if (chart){
      chart.data.labels = labels;
      chart.data.datasets[0].data = values;
      chart.update();
    }

    // cards
    emptyEl.style.display = n === 0 ? 'block' : 'none';
    resultsEl.innerHTML = results.map(function(r){
      var title = r.short_title || r.title || r.symbol || '(untitled)';
      var yearTxt = (typeof r.year === 'number') ? r.year : 'year unknown';
      var symbolHtml = r.doc_url
        ? '<a class="symbol" href="' + escAttr(r.doc_url) + '" target="_blank" rel="noopener noreferrer">' + escHtml(r.symbol || '(no symbol)') + '</a>'
        : '<span class="symbol plain">' + escHtml(r.symbol || '(no symbol)') + '</span>';
      var paraTxt = (r.paragraph !== null && r.paragraph !== undefined) ? 'para. ' + r.paragraph : '';
      var ranges = posTerms.length ? highlightRanges(r.text || '', posTerms) : [];
      var body = r.text ? renderHighlighted(r.text, ranges) : '<em>(empty paragraph)</em>';
      var citation = (r.symbol || '') + (r.paragraph !== null && r.paragraph !== undefined ? ', para. ' + r.paragraph : '');
      return '<article class="card">' +
        '<div class="card-head">' +
          '<span class="badge">' + escHtml(r.committee || 'unknown') + '</span>' +
          '<span class="gc-title">' + escHtml(title) + '</span>' +
          '<span class="year">' + escHtml(yearTxt) + '</span>' +
          symbolHtml +
          (paraTxt ? '<span class="para-label">' + escHtml(paraTxt) + '</span>' : '') +
        '</div>' +
        '<p class="para-text">' + body + '</p>' +
        '<button class="copy-btn" data-citation="' + escAttr(citation) + '">Copy citation</button>' +
      '</article>';
    }).join('');
  }

  /* ---------- copy citation ---------- */
  function legacyCopy(t){
    var ta = document.createElement('textarea');
    ta.value = t;
    ta.style.position = 'fixed';
    ta.style.opacity = '0';
    document.body.appendChild(ta);
    ta.select();
    try { document.execCommand('copy'); } catch(e){}
    document.body.removeChild(ta);
  }
  resultsEl.addEventListener('click', function(ev){
    var btn = ev.target.closest('.copy-btn');
    if (!btn) return;
    var text = btn.getAttribute('data-citation');
    var done = function(){
      btn.textContent = 'Copied';
      btn.classList.add('copied');
      setTimeout(function(){
        btn.textContent = 'Copy citation';
        btn.classList.remove('copied');
      }, 2000);
    };
    if (navigator.clipboard && navigator.clipboard.writeText){
      navigator.clipboard.writeText(text).then(done, function(){ legacyCopy(text); done(); });
    } else {
      legacyCopy(text); done();
    }
  });

  /* ---------- events ---------- */
  form.addEventListener('submit', function(ev){ ev.preventDefault(); runSearch(); });
  commSel.addEventListener('change', runSearch);
  yearFrom.addEventListener('input', runSearch);
  yearTo.addEventListener('input', runSearch);

  /* ---------- chart ---------- */
  if (window.Chart){
    chart = new Chart(document.getElementById('chart').getContext('2d'), {
      type: 'bar',
      data: { labels: [], datasets: [{ label: 'Matching paragraphs', data: [], backgroundColor: '#1f6fb2', borderRadius: 4 }] },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: { legend: { display: false } },
        scales: {
          y: { beginAtZero: true, ticks: { precision: 0 }, title: { display: true, text: 'Paragraphs' } },
          x: { ticks: { autoSkip: false } }
        }
      }
    });
  }

  runSearch();
})();
</script>
</body>
</html>
```