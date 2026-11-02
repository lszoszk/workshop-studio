I added an "AI SDG suggestions" card at the bottom of the dashboard: it sends the first 50 records of the current filter to the model in batches of 25, with live progress, a stop button, and a privacy notice naming the model and warning that repeats may differ. Results appear as per-run agreement cards plus a side-by-side table (record, UN's SDGs, each run's AI SDGs, agree/differ), where every model-derived value is marked with `data-source="ai"` and highlighted.

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Human rights recommendations dashboard</title>
<style>
  :root{--accent:#1f6fb2;--accent-dark:#175a91;--accent-soft:#e8f1f8;--ink:#1c2733;--muted:#5b6b7b;--line:#dce3ec;--bg:#f4f6f9;--card:#fff;--ai-bg:#fbf2dd;--ai-line:#e7d4a3}
  *{box-sizing:border-box}html,body{margin:0}
  body{font:16px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif;color:var(--ink);background:var(--bg)}
  .wrap{max-width:1200px;margin:0 auto;padding:30px 26px 70px}
  a{color:var(--accent)}
  h1{font-size:27px;line-height:1.25;margin:0 0 6px}
  h2{font-size:18px;margin:0}
  .desc{margin:0;color:var(--muted)}.desc a{font-weight:600}
  .card{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:18px 20px;margin-top:18px}
  .note{font-size:13.5px;color:var(--muted);margin:10px 0 0}
  .kpis{display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));gap:14px;margin-top:18px}
  .kpi{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:14px 16px}
  .kpi .n{font-size:30px;font-weight:700;color:var(--accent);line-height:1.2}
  .kpi .lbl{font-size:12.5px;font-weight:700;text-transform:uppercase;letter-spacing:.05em;color:var(--muted);margin-top:2px}
  .kpi .sub{font-size:13px;color:var(--muted);margin-top:4px}
  .card-head{display:flex;justify-content:space-between;align-items:center;gap:12px;flex-wrap:wrap;margin-bottom:12px}
  .filters{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:12px}
  .field-wide{grid-column:1 / -1}
  .field label{display:block;font-size:12.5px;font-weight:600;color:var(--muted);margin-bottom:4px}
  .field select,.field input{width:100%;padding:8px 10px;border:1px solid var(--line);border-radius:6px;background:#fff;font:inherit;color:var(--ink)}
  .btn{border:1px solid var(--accent);background:var(--accent);color:#fff;font:inherit;font-weight:600;padding:8px 14px;border-radius:6px;cursor:pointer}
  .btn:hover{background:var(--accent-dark)}
  .btn:disabled{opacity:.45;cursor:not-allowed}
  .btn-ghost{border:1px solid var(--line);background:#fff;color:var(--muted);font:inherit;padding:7px 12px;border-radius:6px;cursor:pointer}
  .btn-ghost:hover{border-color:var(--accent);color:var(--accent)}
  .btn-ghost:disabled{opacity:.45;cursor:not-allowed}
  .chips{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin:0 0 12px}
  .chip{display:inline-flex;align-items:center;gap:7px;background:var(--accent-soft);color:var(--accent-dark);border:1px solid #bcd6ea;border-radius:999px;padding:3px 6px 3px 11px;font-size:13px;cursor:pointer}
  .chip:hover{background:#dbeaf6}.chip .x{font-weight:700;padding:0 4px}
  .chips .lbl{font-size:13.5px;color:var(--muted)}
  .chart-box{position:relative;height:400px;margin-top:8px}
  .placeholder{display:none;padding:34px 10px;text-align:center;color:var(--muted);background:#f8fafc;border:1px dashed var(--line);border-radius:8px}
  .summary-line{font-size:15px;margin:0}.summary-line strong{color:var(--accent);font-size:17px}
  .sort-field{display:flex;align-items:center;gap:8px;font-size:13.5px;color:var(--muted)}
  .sort-field select{padding:5px 8px;border:1px solid var(--line);border-radius:6px;font:inherit;font-size:13.5px;background:#fff;color:var(--ink)}
  .table-scroll{overflow-x:auto;margin-top:4px}
  table.tbl{width:100%;border-collapse:collapse;font-size:15px}
  .tbl th{text-align:left;font-size:11.5px;font-weight:700;text-transform:uppercase;letter-spacing:.05em;color:var(--muted);border-bottom:2px solid var(--line);padding:9px 10px;white-space:nowrap}
  .tbl td{padding:9px 10px;border-bottom:1px solid var(--line);vertical-align:top}
  .tbl .nowrap{white-space:nowrap}
  .tbl .sub,.sub{font-size:12.5px;color:var(--muted);margin-top:2px}
  tr.doc{cursor:pointer}tr.doc:hover{background:#f2f7fb}
  tr.doc:focus-visible{outline:2px solid var(--accent);outline-offset:-2px}
  tr.doc.open{background:#eef5fb}
  .hint{color:var(--muted);font-size:12px;white-space:nowrap}
  tr.detail td{background:#f7fafd;padding:14px 16px 16px}
  .dlabel{font-size:11.5px;font-weight:700;text-transform:uppercase;letter-spacing:.05em;color:var(--muted);margin-bottom:5px}
  .fulltext{white-space:pre-wrap;margin:0 0 12px;font-size:15px}
  .meta-row{display:flex;gap:10px;margin-top:6px;font-size:13.5px}
  .meta-row .mlbl{flex:0 0 130px;color:var(--muted);font-weight:600}
  .tags{display:inline-flex;flex-wrap:wrap;gap:5px}
  .tag{background:var(--accent-soft);color:var(--accent-dark);border-radius:4px;padding:1px 7px;font-size:12.5px}
  .targets{margin:4px 0 0;padding-left:18px;font-size:13px;color:var(--ink)}.targets li{margin:1px 0}
  .table-foot{display:flex;justify-content:space-between;align-items:center;gap:12px;flex-wrap:wrap;margin-top:12px;font-size:13.5px;color:var(--muted)}
  .warn{background:#fdf6e7;border:1px solid #ecd9ad;border-radius:10px;padding:14px 18px;margin-top:18px;color:#6b5615}
  code{background:#eef1f5;padding:1px 5px;border-radius:4px;font-size:12.5px}
  /* AI section */
  .ai-bar{display:flex;gap:10px;flex-wrap:wrap;align-items:center;margin-top:14px}
  .badge{font-size:11.5px;font-weight:700;letter-spacing:.05em;text-transform:uppercase;color:#8a6d1f;background:var(--ai-bg);border:1px solid var(--ai-line);border-radius:999px;padding:3px 10px}
  .progress-bar{height:8px;background:#e6ebf1;border-radius:4px;overflow:hidden;margin-top:14px}
  .progress-fill{height:100%;background:var(--accent);width:0}
  .notice-ai{background:var(--ai-bg);border:1px solid var(--ai-line);border-radius:8px;padding:12px 16px;margin-top:14px;font-size:14.5px;color:#5f4c17}
  .run-strip{display:flex;gap:12px;flex-wrap:wrap;margin-top:14px}
  .run-card{border:1px solid var(--line);border-radius:8px;padding:10px 14px;background:#fafbfc;min-width:210px}
  .run-card .rk{font-size:12.5px;font-weight:700;text-transform:uppercase;letter-spacing:.05em;color:var(--muted)}
  .run-card .pct{font-size:26px;font-weight:700;color:var(--accent);line-height:1.3}
  [data-source="ai"]{background:var(--ai-bg);border-radius:4px;padding:1px 6px}
  .mut{color:var(--muted)}
  .v-ok{color:#1e7d46;font-weight:700}
  .v-no{color:#a2492f;font-weight:700}
</style>
</head>
<body>
<div class="wrap">
  <header>
    <h1 id="pageTitle">Human rights recommendations &amp; observations</h1>
    <p class="desc" id="pageDesc"></p>
  </header>

  <div id="noDataWarn" class="warn" style="display:none"></div>

  <section class="kpis" id="kpis"></section>
  <p class="note" id="kpiNote"></p>

  <section class="card">
    <div class="card-head">
      <h2>Filters</h2>
      <button id="resetBtn" class="btn-ghost" type="button">Reset all filters</button>
    </div>
    <div class="filters">
      <div class="field"><label for="fMech">Mechanism</label><select id="fMech"></select></div>
      <div class="field"><label for="fBody">Treaty body / mandate</label><select id="fBody"></select></div>
      <div class="field"><label for="fFrom">From year</label><select id="fFrom"></select></div>
      <div class="field"><label for="fTo">To year</label><select id="fTo"></select></div>
      <div class="field"><label for="fSdg">SDG</label><select id="fSdg"></select></div>
      <div class="field field-wide"><label for="fQ">Keyword search (paragraph text &amp; document symbol)</label>
        <input id="fQ" type="search" placeholder="e.g. education, detention, birth registration…" autocomplete="off"></div>
    </div>
    <p class="note">Filters combine: a record must match all of them. The keyword search is case-insensitive and looks only at the paragraph text and the document symbol.</p>
  </section>

  <section class="card">
    <div class="card-head"><h2>Most frequent themes</h2></div>
    <div class="chart-box"><canvas id="themeChart" aria-label="Bar chart of the ten most frequent themes"></canvas></div>
    <div id="chartEmpty" class="placeholder"></div>
    <p class="note" id="chartNote"></p>
  </section>

  <section class="card">
    <div class="card-head">
      <h2>Matching records</h2>
      <div class="sort-field">
        <label for="fSort">Sort by</label>
        <select id="fSort">
          <option value="date-desc">Date, newest first</option>
          <option value="date-asc">Date, oldest first</option>
          <option value="body">Body / mandate (A–Z)</option>
        </select>
      </div>
    </div>
    <p class="summary-line" id="resultSummary"></p>
    <div class="chips" id="chips"></div>
    <div class="table-scroll">
      <table class="tbl">
        <thead><tr><th>Date</th><th>Body / mandate</th><th>Symbol</th><th>Text (first line)</th></tr></thead>
        <tbody id="tbody"></tbody>
      </table>
    </div>
    <div class="table-foot" id="tableFoot"></div>
    <p class="note">Each row is one paragraph from a UN document. The last column shows only the first line — click any row to read the full, unedited paragraph. The symbol links to the official document, opened in a new tab.</p>
  </section>

  <!-- ===== AI SDG suggestions ===== -->
  <section class="card" id="aiCard">
    <div class="card-head">
      <h2>AI assistant: SDG suggestions &amp; comparison</h2>
      <span class="badge">External model &middot; slow &middot; costs money</span>
    </div>
    <p class="desc">Sends the paragraph texts of the first 50 records of the current filter to an external language model, asks it to suggest SDG goal numbers, and compares its suggestions with the UN&rsquo;s own SDG tags. This is the only part of the page that uses an external model; everything else is computed locally in your browser.</p>
    <div class="ai-bar">
      <button id="aiRunBtn" type="button" class="btn">Suggest SDGs with AI</button>
      <button id="aiAgainBtn" type="button" class="btn" style="display:none">Run again</button>
      <button id="aiStopBtn" type="button" class="btn-ghost" style="display:none">Stop</button>
      <button id="aiClearBtn" type="button" class="btn-ghost" style="display:none">Clear AI results</button>
    </div>
    <p class="note" id="aiScope"></p>
    <div id="aiProgressBox" style="display:none">
      <div class="progress-bar"><div class="progress-fill" id="aiFill"></div></div>
      <p class="note" id="aiProgressText"></p>
    </div>
    <div id="aiNotice" class="notice-ai" style="display:none"></div>
    <div class="run-strip" id="aiRuns"></div>
    <p class="note" id="aiVarNote"></p>
    <p class="note" id="aiLegend" style="display:none"></p>
    <div class="table-scroll">
      <table class="tbl" id="aiTable" style="display:none">
        <thead id="aiHead"></thead>
        <tbody id="aiBody"></tbody>
      </table>
    </div>
    <p class="note" id="aiFoot"></p>
    <p class="note">How this is computed: the button takes the first 50 records of the current filter, in the order of the table above, and sends their paragraph texts to the model in batches of 25 (two calls for 50 records). The model is never shown the UN&rsquo;s SDG tags. &ldquo;Agree&rdquo; means the model&rsquo;s set of goal numbers is exactly the UN&rsquo;s set for that record — order is ignored, and two empty sets count as agreement. A run&rsquo;s agreement rate is the share of records the model answered where the two sets match; records with no answer are shown as &ldquo;no answer&rdquo; and excluded from that rate.</p>
  </section>
</div>

<script>
(function(){
'use strict';

/* ---------- data ---------- */
var U = (window.WORKSHOP_DATA && window.WORKSHOP_DATA.uhri) ? window.WORKSHOP_DATA.uhri : {};
var REC = Array.isArray(U.records) ? U.records : [];
var SDG_NAMES = (U.sdg_names && typeof U.sdg_names === 'object') ? U.sdg_names : {};
var COUNTRY = U.country || 'the country';

/* ---------- helpers ---------- */
function esc(s){
  return String(s == null ? '' : s).replace(/[&<>"']/g, function(c){
    return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c];
  });
}
function fmtDate(d){
  if(!d) return '—';
  var s = String(d), m = s.match(/^(\d{4})-(\d{2})-(\d{2})$/);
  if(m){
    var mo = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
    return parseInt(m[3],10) + ' ' + mo[parseInt(m[2],10)-1] + ' ' + m[1];
  }
  return s;
}
function firstLine(t){
  if(!t) return '—';
  var line = String(t).trim().split(/\r?\n/)[0].trim();
  if(line.length > 170) line = line.slice(0,170).replace(/\s+\S*$/,'') + '…';
  return line || '—';
}
function snippet(t, n){
  t = String(t || '').trim().replace(/\s+/g,' ');
  if(t.length > n) t = t.slice(0, n).replace(/\s+\S*$/,'') + '…';
  return t || '—';
}
function tally(fn){
  var m = new Map();
  REC.forEach(function(r){ var v = fn(r); if(v === null || v === undefined || v === '') return; m.set(v, (m.get(v)||0) + 1); });
  return m;
}
function byCountThenAlpha(a,b){ return b[1]-a[1] || String(a[0]).localeCompare(String(b[0])); }
function plural(n, w){ return n + ' ' + w + (n === 1 ? '' : 's'); }
function wrapLabel(s, max){
  var words = String(s).split(' '), lines = [], cur = '';
  words.forEach(function(w){
    if((cur ? cur + ' ' + w : w).length > max && cur){ lines.push(cur); cur = w; }
    else cur = cur ? cur + ' ' + w : w;
  });
  if(cur) lines.push(cur);
  return lines;
}
function setsEqual(a,b){
  if(a.length !== b.length) return false;
  for(var i=0;i<a.length;i++) if(a[i] !== b[i]) return false;
  return true;
}
function unSdgs(r){
  var a = Array.isArray(r.sdgs) ? r.sdgs : [], out = [];
  a.forEach(function(n){ n = Number(n); if(n>=1 && n<=17 && Math.floor(n)===n && out.indexOf(n)===-1) out.push(n); });
  out.sort(function(x,y){ return x-y; });
  return out;
}
function sdgTitle(arr){
  return arr.map(function(n){ var nm = SDG_NAMES[String(n)] || SDG_NAMES[n]; return 'SDG ' + n + (nm ? ' — ' + nm : ''); }).join('\n');
}

/* ---------- dataset-level facts ---------- */
var yearsAll = REC.map(function(r){ return typeof r.year === 'number' ? r.year : null; }).filter(function(v){ return v !== null; });
var minYear = yearsAll.length ? Math.min.apply(null, yearsAll) : null;
var maxYear = yearsAll.length ? Math.max.apply(null, yearsAll) : null;
var nDocs = new Set(REC.map(function(r){ return r.symbol || null; }).filter(Boolean)).size;
var bodyTally = tally(function(r){ return r.body; });
var nBodies = bodyTally.size;
var typeTally = tally(function(r){ return r.type; });
var nRecs = typeTally.get('Recommendations') || 0;
var nObs = typeTally.get('Concerns/Observations') || 0;
var nOtherType = REC.length - nRecs - nObs;

/* ---------- header & KPIs ---------- */
document.getElementById('pageTitle').textContent =
  'Human rights recommendations & observations addressed to ' + COUNTRY;
document.title = 'UN recommendations — ' + COUNTRY;
(function(){
  var bits = [];
  if(U.title) bits.push(esc(U.title));
  if(U.source){
    bits.push('Source: ' + (U.source_url
      ? '<a href="' + esc(U.source_url) + '" target="_blank" rel="noopener">' + esc(U.source) + '</a>'
      : esc(U.source)));
  }
  bits.push('n = ' + plural(REC.length, 'record'));
  if(minYear !== null) bits.push(minYear === maxYear ? String(minYear) : minYear + '–' + maxYear);
  if(U.built) bits.push('dataset built ' + esc(U.built));
  document.getElementById('pageDesc').innerHTML = bits.join(' &middot; ');
})();
(function(){
  var typeSub = plural(nRecs,'recommendation') + ' &middot; ' + plural(nObs,'concern / observation');
  if(nOtherType > 0) typeSub += ' &middot; ' + plural(nOtherType,'other type');
  var period = minYear === null ? '—' : (minYear === maxYear ? String(minYear) : minYear + '–' + maxYear);
  document.getElementById('kpis').innerHTML =
    '<div class="kpi"><div class="n">' + REC.length + '</div><div class="lbl">Paragraph records</div><div class="sub">' + typeSub + '</div></div>' +
    '<div class="kpi"><div class="n">' + nDocs + '</div><div class="lbl">UN documents</div><div class="sub">distinct symbols</div></div>' +
    '<div class="kpi"><div class="n">' + nBodies + '</div><div class="lbl">Bodies &amp; mandates</div><div class="sub">treaty bodies, UPR, Special Procedures</div></div>' +
    '<div class="kpi"><div class="n">' + period + '</div><div class="lbl">Period covered</div><div class="sub">years of the records</div></div>';
  document.getElementById('kpiNote').textContent =
    'How this is computed: every number above is counted directly from the loaded records — one record is one paragraph of a UN document (a recommendation or an observation). Nothing is estimated.';
})();
var noDataWarn = document.getElementById('noDataWarn');
if(!REC.length){
  noDataWarn.style.display = 'block';
  noDataWarn.textContent = 'No records were found in WORKSHOP_DATA.uhri for this country, so there is nothing to filter, chart or list below.';
}

/* ---------- filter state & controls ---------- */
var state = { mechanism:'', body:'', sdg:'', yearFrom:minYear, yearTo:maxYear, q:'', theme:'' };
var visible = 50, expanded = new Set(), lastFiltered = [];
var fMech = document.getElementById('fMech'), fBody = document.getElementById('fBody'),
    fFrom = document.getElementById('fFrom'), fTo = document.getElementById('fTo'),
    fSdg = document.getElementById('fSdg'), fQ = document.getElementById('fQ'),
    fSort = document.getElementById('fSort');

function fillSelect(sel, entries, placeholder){
  sel.innerHTML = '';
  sel.add(new Option(placeholder, ''));
  entries.forEach(function(e){ sel.add(new Option(e[1], String(e[0]))); });
}
fillSelect(fMech, Array.from(tally(function(r){ return r.mechanism; })).sort(byCountThenAlpha)
    .map(function(e){ return [e[0], e[0] + ' (' + e[1] + ')']; }), 'All mechanisms');
fillSelect(fBody, Array.from(bodyTally).sort(byCountThenAlpha)
    .map(function(e){ return [e[0], e[0] + ' (' + e[1] + ')']; }), 'All bodies & mandates');
(function(){
  var sdgSet = new Set();
  REC.forEach(function(r){ (Array.isArray(r.sdgs) ? r.sdgs : []).forEach(function(n){ if(n != null) sdgSet.add(Number(n)); }); });
  fillSelect(fSdg, Array.from(sdgSet).sort(function(a,b){ return a-b; }).map(function(n){
    var name = SDG_NAMES[String(n)] || SDG_NAMES[n];
    return [n, 'SDG ' + n + (name ? ' — ' + name : '')];
  }), 'All SDGs');
})();
(function(){
  if(minYear === null){
    fFrom.disabled = fTo.disabled = true;
    fFrom.innerHTML = fTo.innerHTML = '<option value="">—</option>';
    return;
  }
  yearsAll.slice().sort(function(a,b){ return a-b; }).forEach(function(y){
    fFrom.add(new Option(String(y), String(y))); fTo.add(new Option(String(y), String(y)));
  });
  fFrom.value = String(minYear); fTo.value = String(maxYear);
})();

/* ---------- filtering & sorting ---------- */
function getFiltered(){
  var q = state.q ? state.q.toLowerCase() : '';
  var fullRange = (state.yearFrom === minYear && state.yearTo === maxYear);
  return REC.filter(function(r){
    if(state.mechanism && r.mechanism !== state.mechanism) return false;
    if(state.body && r.body !== state.body) return false;
    if(state.sdg !== ''){
      var list = Array.isArray(r.sdgs) ? r.sdgs : [];
      if(list.indexOf(Number(state.sdg)) === -1) return false;
    }
    if(!fullRange){
      if(typeof r.year === 'number'){ if(r.year < state.yearFrom || r.year > state.yearTo) return false; }
      else return false;
    }
    if(state.theme && (Array.isArray(r.themes) ? r.themes : []).indexOf(state.theme) === -1) return false;
    if(q && (((r.text || '') + ' ' + (r.symbol || '')).toLowerCase().indexOf(q) === -1)) return false;
    return true;
  });
}
function sortList(list){
  var out = list.slice(), dateKey = function(r){ return String(r.date || r.year || ''); };
  if(fSort.value === 'date-asc') out.sort(function(a,b){ return dateKey(a).localeCompare(dateKey(b)); });
  else if(fSort.value === 'body') out.sort(function(a,b){
    return String(a.body || '').localeCompare(String(b.body || '')) || dateKey(b).localeCompare(dateKey(a));
  });
  else out.sort(function(a,b){ return dateKey(b).localeCompare(dateKey(a)); });
  return out;
}

/* ---------- chart ---------- */
var chart = null, plainLabels = [];
var chartBox = document.querySelector('.chart-box'), chartEmpty = document.getElementById('chartEmpty');
var chartNote = document.getElementById('chartNote');
if(typeof window.Chart === 'undefined'){
  chartBox.innerHTML = '<div class="placeholder" style="display:block">The charts library (Chart.js) is not available in this page, so the theme chart cannot be drawn. The table below still works.</div>';
}
function makeChart(){
  chart = new window.Chart(document.getElementById('themeChart'), {
    type: 'bar',
    data: { labels: [], datasets: [{ label: 'Records', data: [], backgroundColor: [], borderWidth: 0, maxBarThickness: 26 }] },
    options: {
      indexAxis: 'y', responsive: true, maintainAspectRatio: false, animation: false,
      scales: {
        x: { beginAtZero: true, ticks: { precision: 0 }, grid: { color: '#e6ebf1' },
             title: { display: true, text: 'Number of records', color: '#5b6b7b', font: { size: 12 } } },
        y: { ticks: { autoSkip: false, font: { size: 13 } }, grid: { display: false } }
      },
      plugins: {
        legend: { display: false },
        tooltip: { callbacks: { label: function(c){ return ' ' + plural(c.parsed.x, 'record'); } } }
      },
      onClick: function(evt, els){
        if(!els.length || !plainLabels.length) return;
        var t = plainLabels[els[0].index];
        state.theme = (state.theme === t) ? '' : t;
        visible = 50; render();
      },
      onHover: function(evt, els){ evt.native.target.style.cursor = els.length ? 'pointer' : 'default'; }
    }
  });
}
function renderChart(list){
  var counts = new Map(), noTheme = 0;
  list.forEach(function(r){
    var th = (Array.isArray(r.themes) ? r.themes : []).filter(Boolean