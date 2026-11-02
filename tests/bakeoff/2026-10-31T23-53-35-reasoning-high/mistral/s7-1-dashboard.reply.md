I built a single-file dashboard for the UHRI records addressed to the country named in the data (Kenya in this dataset): header stats with record count and year span, five working filters (mechanism, body/mandate, year range, SDG, keyword), a Chart.js horizontal bar chart of the top 10 themes under the current filter, and an expandable table where each row links its symbol to the UN document and reveals the full paragraph on click. All counting is done deterministically in the browser, with "how this is computed" notes next to every figure.

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>UN human rights recommendations — Kenya</title>
<style>
:root{
  --accent:#1f6fb2; --accent-dark:#17517f; --ink:#1d2733; --muted:#5c6b7a;
  --bg:#f4f6f9; --card:#ffffff; --line:#dde4ec; --soft:#e8f1fa;
}
*{box-sizing:border-box}
html,body{margin:0;padding:0}
body{
  font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif;
  font-size:16px;line-height:1.55;color:var(--ink);background:var(--bg);
}
.wrap{max-width:1100px;margin:0 auto;padding:28px 20px 72px}
header.top{padding:4px 2px 0}
h1{font-size:1.55rem;line-height:1.25;margin:0 0 6px}
h1 .cc{color:var(--accent)}
.lede{margin:0;color:var(--muted);font-size:.95rem}
.lede a{color:var(--accent)}
.card{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:18px 20px;margin-top:18px}
.card h2{font-size:1.12rem;margin:0 0 4px}
.note{font-size:.85rem;color:var(--muted);margin:4px 0 12px}
.filters{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:12px 14px;align-items:end}
.field label{display:block;font-size:.8rem;font-weight:600;color:var(--muted);margin-bottom:4px;letter-spacing:.02em}
.field select,.field input{width:100%;padding:8px 10px;font:inherit;font-size:.92rem;border:1px solid var(--line);border-radius:7px;background:#fff;color:var(--ink)}
.field select:focus,.field input:focus{outline:2px solid var(--accent);outline-offset:1px;border-color:var(--accent)}
.btnrow{display:flex;align-items:flex-end}
button.reset{padding:8px 14px;font:inherit;font-size:.9rem;border:1px solid var(--line);background:#fff;color:var(--accent-dark);border-radius:7px;cursor:pointer;white-space:nowrap}
button.reset:hover{background:var(--soft)}
#filterDesc{font-size:.88rem;color:var(--accent-dark);margin:12px 0 0;font-weight:600}
.stats{display:flex;flex-wrap:wrap;gap:14px 36px;margin-top:2px}
.stat .num{font-size:1.5rem;font-weight:700;color:var(--accent);line-height:1.15}
.stat .lbl{font-size:.82rem;color:var(--muted)}
.chart-box{position:relative;width:100%}
table{width:100%;border-collapse:collapse;margin-top:6px}
th{font-size:.76rem;text-transform:uppercase;letter-spacing:.05em;color:var(--muted);text-align:left;padding:8px 10px;border-bottom:2px solid var(--line)}
td{padding:10px;border-bottom:1px solid var(--line);vertical-align:top;font-size:.93rem}
tr.rec{cursor:pointer}
tr.rec:hover{background:#f0f6fc}
tr.rec.open{background:var(--soft)}
tr.detail td{background:#f8fafd}
.chev{width:20px;color:var(--accent)}
tr.rec.open .chev{font-weight:700}
.cdate{white-space:nowrap;font-variant-numeric:tabular-nums}
.cbody{white-space:nowrap}
.cbody .sub{font-size:.78rem;color:var(--muted);white-space:normal}
.csym a{color:var(--accent);text-decoration:none;font-weight:600}
.csym a:hover{text-decoration:underline}
.ctext{color:#33404d}
.fulltext{white-space:pre-wrap;background:#fff;border:1px solid var(--line);border-radius:8px;padding:12px 14px;font-size:.92rem;margin:6px 0 10px}
.dline{margin:6px 0;font-size:.88rem}
.dsec{margin:2px 0 6px;font-size:.88rem;color:var(--muted)}
.dlist{margin:4px 0 8px;padding-left:20px;font-size:.86rem;color:#33404d}
.chip{display:inline-block;background:var(--soft);color:var(--accent-dark);border-radius:999px;padding:1px 10px;font-size:.78rem;margin:2px 4px 2px 0}
.empty{padding:18px;border:1px dashed var(--line);border-radius:8px;color:var(--muted);background:#fbfcfe;text-align:center}
a{color:var(--accent)}
footer{margin-top:26px;font-size:.82rem;color:var(--muted)}
</style>
</head>
<body>
<div class="wrap">

  <header class="top">
    <h1>UN human rights recommendations &amp; observations addressed to <span class="cc" id="country"></span></h1>
    <p class="lede" id="lede"></p>
  </header>

  <section class="card" aria-label="Filters">
    <h2>Filters</h2>
    <p class="note">Every chart and number on this page updates to the records that pass all filters below. Filtering and counting are done exactly, in your browser, on the loaded dataset — nothing is estimated.</p>
    <div class="filters">
      <div class="field"><label for="fMechanism">Mechanism</label><select id="fMechanism"></select></div>
      <div class="field"><label for="fBody">Treaty body / mandate</label><select id="fBody"></select></div>
      <div class="field"><label for="fFrom">Year from</label><select id="fFrom"></select></div>
      <div class="field"><label for="fTo">Year to</label><select id="fTo"></select></div>
      <div class="field"><label for="fSdg">SDG</label><select id="fSdg"></select></div>
      <div class="field"><label for="fQ">Keyword search</label><input id="fQ" type="search" placeholder="text, theme, symbol…"></div>
      <div class="btnrow"><button class="reset" id="reset" type="button">Reset filters</button></div>
    </div>
    <p id="filterDesc"></p>
  </section>

  <section class="card" aria-label="Overview">
    <h2>Overview of the dataset</h2>
    <div class="stats" id="statsRow"></div>
    <p class="note">How this is computed: each figure is a plain count over the <span id="nNote"></span> records loaded in this page; mechanisms, bodies and years are the distinct values actually found in the data.</p>
  </section>

  <section class="card" aria-label="Themes chart">
    <h2>10 most frequent themes <span id="chartN"></span></h2>
    <p class="note">How this is computed: each matching record adds 1 to every theme it carries (a record with three themes counts once in each of them); the 10 highest counts are charted. Exact counts, no estimates.</p>
    <div class="chart-box" id="chartWrap"><canvas id="themeCanvas"></canvas></div>
    <div id="chartFallback" hidden></div>
    <p class="empty" id="chartEmpty" hidden></p>
  </section>

  <section class="card" aria-label="Records table">
    <h2>Matching records — <span id="matchCount"></span></h2>
    <p class="note">How this is computed: the rows below are exactly the records that pass the filters above, sorted by date (newest first). The last column shows the first line of the paragraph — click a row to read the full text. The symbol links to the UN document and opens in a new tab.</p>
    <table>
      <thead>
        <tr><th></th><th>Date</th><th>Body / mandate</th><th>Symbol</th><th>Text (first line — click row for full text)</th></tr>
      </thead>
      <tbody id="recBody"></tbody>
    </table>
    <p class="empty" id="tableEmpty" hidden>No records match the current filters. Loosen a filter or reset them to see the full list.</p>
  </section>

  <footer id="foot"></footer>
</div>

<script>
(function(){
'use strict';
var DATA = window.WORKSHOP_DATA || {};
var U = DATA.uhri || {};
var records = Array.isArray(U.records) ? U.records : [];
var sdgNames = U.sdg_names || {};
var country = U.country || 'the reviewed country';

function $(id){ return document.getElementById(id); }
function esc(s){ return String(s==null?'':s).replace(/[&<>"']/g,function(c){ return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]; }); }
function arr(v){ return Array.isArray(v)?v:(v==null||v===''?[]:[v]); }
function distinct(key){
  var seen={}, out=[];
  records.forEach(function(r){ var v=r[key]; if(v!=null&&v!==''){ v=String(v); if(!seen[v]){ seen[v]=1; out.push(v); } } });
  return out.sort();
}

var mechanisms = distinct('mechanism');
var bodies = distinct('body');
var yearSet=[], seenY={};
records.forEach(function(r){ if(typeof r.year==='number' && !seenY[r.year]){ seenY[r.year]=1; yearSet.push(r.year); } });
yearSet.sort(function(a,b){ return a-b; });
var yearMin = yearSet.length ? yearSet[0] : null;
var yearMax = yearSet.length ? yearSet[yearSet.length-1] : null;
var sdgList=[], seenS={};
records.forEach(function(r){ arr(r.sdgs).forEach(function(n){ var k=String(n); if(!seenS[k]){ seenS[k]=1; sdgList.push(k); } }); });
sdgList.sort(function(a,b){ return (parseInt(a,10)||0)-(parseInt(b,10)||0); });

var state = { mechanism:'', body:'', from:'', to:'', sdg:'', q:'' };
var currentList = [];
var chart = null;

function fillSelect(el, opts, allLabel){
  el.innerHTML = '<option value="">'+esc(allLabel)+'</option>' + opts.map(function(o){
    return '<option value="'+esc(o.v)+'">'+esc(o.l)+'</option>';
  }).join('');
}
fillSelect($('fMechanism'), mechanisms.map(function(m){ return {v:m,l:m}; }), 'All mechanisms');
fillSelect($('fBody'), bodies.map(function(b){ return {v:b,l:b}; }), 'All bodies / mandates');
fillSelect($('fFrom'), yearSet.map(function(y){ return {v:String(y),l:String(y)}; }), 'From (any)');
fillSelect($('fTo'), yearSet.map(function(y){ return {v:String(y),l:String(y)}; }), 'To (any)');
fillSelect($('fSdg'), sdgList.map(function(n){ return {v:n, l:'SDG '+n+(sdgNames[n]?' — '+sdgNames[n]:'')}; }), 'All SDGs');

/* ---------- header & overview ---------- */
$('country').textContent = country;
document.title = 'UN human rights recommendations — ' + country;
var lede = esc(U.title || 'UN human rights recommendations and observations addressed to ' + country)
  + ' · n = ' + records.length + ' records'
  + (yearMin!=null ? ' · years ' + yearMin + '–' + yearMax + ' (' + yearSet.length + ' distinct years)' : ' · no year information in the data');
if(U.source){ lede += ' · source: ' + (U.source_url ? '<a href="'+esc(U.source_url)+'" target="_blank" rel="noopener noreferrer">'+esc(U.source)+'</a>' : esc(U.source)); }
if(U.built){ lede += ' · dataset built ' + esc(U.built); }
$('lede').innerHTML = lede;

function stat(num, lbl){ return '<div class="stat"><div class="num">'+esc(num)+'</div><div class="lbl">'+esc(lbl)+'</div></div>'; }
$('statsRow').innerHTML =
  stat(records.length, 'records loaded') +
  stat(yearMin!=null ? yearMin+'–'+yearMax : '—', 'year range') +
  stat(yearSet.length, 'distinct years') +
  stat(mechanisms.length, 'mechanisms') +
  stat(bodies.length, 'bodies / mandates');
$('nNote').textContent = records.length;
$('foot').innerHTML = 'Data: ' + esc(U.title || 'UHRI extract') + (U.source ? ' (' + esc(U.source) + ')' : '')
  + '. All data was loaded into this page before it opened; the page makes no network requests. Symbols link to the UN documents and open in a new tab.';

/* ---------- filtering ---------- */
function matches(r){
  if(state.mechanism && String(r.mechanism==null?'':r.mechanism) !== state.mechanism) return false;
  if(state.body && String(r.body==null?'':r.body) !== state.body) return false;
  var y = r.year;
  if(state.from){ if(typeof y!=='number' || y < parseInt(state.from,10)) return false; }
  if(state.to){ if(typeof y!=='number' || y > parseInt(state.to,10)) return false; }
  if(state.sdg){
    var ok=false;
    arr(r.sdgs).forEach(function(n){ if(String(n)===state.sdg) ok=true; });
    if(!ok) return false;
  }
  if(state.q){
    var hay = [r.text, r.symbol, r.body, r.mechanism, r.type, r.section, r.doc_url]
      .concat(arr(r.themes), arr(r.sdg_targets), arr(r.affected_persons), arr(r.countries))
      .join(' ').toLowerCase();
    if(hay.indexOf(state.q) === -1) return false;
  }
  return true;
}

function themeCounts(list){
  var m = {};
  list.forEach(function(r){
    var seen = {};
    arr(r.themes).forEach(function(t){
      var k = String(t);
      if(!seen[k]){ seen[k]=1; m[k] = (m[k]||0)+1; }
    });
  });
  return Object.keys(m).map(function(k){ return [k, m[k]]; })
    .sort(function(a,b){ return b[1]-a[1] || a[0].localeCompare(b[0]); })
    .slice(0,10);
}

/* ---------- chart ---------- */
function renderChart(list){
  var data = themeCounts(list);
  var canvas = $('themeCanvas'), wrap = $('chartWrap'), empty = $('chartEmpty'), fb = $('chartFallback');
  if(!data.length){
    if(chart){ chart.destroy(); chart = null; }
    canvas.style.display='none'; fb.hidden = true; wrap.style.height='0px';
    empty.hidden = false;
    empty.textContent = list.length
      ? 'None of the ' + list.length + ' matching records carries a theme tag.'
      : 'No records match the current filters.';
    return;
  }
  empty.hidden = true;
  if(!window.Chart){
    canvas.style.display='none';
    fb.hidden = false;
    var max = data[0][1];
    fb.innerHTML = data.map(function(d){
      return '<div style="margin:5px 0"><div style="font-size:.85rem">'+esc(d[0])+'</div>'
        + '<div style="background:#e8f1fa;border-radius:4px;padding:2px 8px;width:'+Math.max(8,Math.round(d[1]/max*100))+'%;color:#17517f;font-size:.8rem">'+d[1]+' record'+(d[1]===1?'':'s')+'</div></div>';
    }).join('');
    return;
  }
  fb.hidden = true;
  canvas.style.display = 'block';
  wrap.style.height = Math.max(240, data.length*38 + 70) + 'px';
  var labels = data.map(function(d){ return d[0]; });
  var values = data.map(function(d){ return d[1]; });
  if(chart){
    chart.data.labels = labels;
    chart.data.datasets[0].data = values;
    chart.update();
  } else {
    chart = new Chart(canvas.getContext('2d'), {
      type:'bar',
      data:{ labels:labels, datasets:[{ label:'Matching records', data:values, backgroundColor:'#1f6fb2', borderRadius:4 }] },
      options:{
        indexAxis:'y', responsive:true, maintainAspectRatio:false,
        plugins:{
          legend:{ display:false },
          tooltip:{ callbacks:{ label:function(c){ return ' ' + c.parsed.x + ' record' + (c.parsed.x===1?'':'s'); } } }
        },
        scales:{
          x:{ beginAtZero:true, ticks:{ precision:0 }, title:{ display:true, text:'Matching records tagged with this theme' }, grid:{ color:'#e6ecf2' } },
          y:{ grid:{ display:false }, ticks:{ autoSkip:false, font:{ size:13 } } }
        }
      }
    });
  }
}

/* ---------- table ---------- */
function firstLine(r){
  var t = String(r.text==null?'':r.text).trim();
  if(!t) return '(no text in this record)';
  var nl = t.indexOf('\n');
  var line = nl >= 0 ? t.slice(0, nl) : t;
  if(line.length > 240) line = line.slice(0, 240).replace(/\s+\S*$/,'') + ' …';
  return line;
}
function sortRecords(list){
  return list.slice().sort(function(a,b){
    var da = String(a.date||''), db = String(b.date||'');
    if(da !== db) return db.localeCompare(da);
    var ya = (typeof a.year==='number' ? a.year : -1), yb = (typeof b.year==='number' ? b.year : -1);
    if(ya !== yb) return yb - ya;
    return String(a.symbol||'').localeCompare(String(b.symbol||''));
  });
}
function renderTable(list){
  var tbody = $('recBody'), empty = $('tableEmpty');
  $('matchCount').textContent = 'showing ' + list.length + ' of ' + records.length + ' records';
  if(!list.length){ tbody.innerHTML=''; empty.hidden=false; return; }
  empty.hidden = true;
  tbody.innerHTML = list.map(function(r, i){
    var url = r.doc_url || '#';
    var sym = r.symbol || '(no symbol)';
    var date = r.date || (typeof r.year==='number' ? String(r.year) : '—');
    var meta = [r.mechanism, r.type].filter(Boolean).join(' · ');
    var themes = arr(r.themes).map(function(t){ return '<span class="chip">'+esc(t)+'</span>'; }).join('');
    var sdgs = arr(r.sdgs).map(function(n){
      var nm = sdgNames[String(n)];
      return '<span class="chip">SDG '+esc(n)+(nm?' — '+esc(nm):'')+'</span>';
    }).join('');
    var targets = arr(r.sdg_targets).map(function(t){ return '<li>'+esc(t)+'</li>'; }).join('');
    var persons = arr(r.affected_persons).map(function(p){ return '<span class="chip">'+esc(p)+'</span>'; }).join('');
    var countries = arr(r.countries);
    return '<tr class="rec" data-i="'+i+'" aria-expanded="false" title="Click to show the full text">'
      + '<td class="chev">▸</td>'
      + '<td class="cdate">'+esc(date)+'</td>'
      + '<td class="cbody">'+esc(r.body||'—')+(meta?'<div class="sub">'+esc(meta)+'</div>':'')+'</td>'
      + '<td class="csym"><a href="'+esc(url)+'" target="_blank" rel="noopener noreferrer">'+esc(sym)+'</a></td>'
      + '<td class="ctext">'+esc(firstLine(r))+'</td>'
      + '</tr>'
      + '<tr class="detail" id="d'+i+'" hidden><td colspan="5">'
      + (r.section ? '<p class="dsec"><strong>Section:</strong> '+esc(r.section)+'</p>' : '')
      + '<div class="fulltext">'+esc(r.text||'(no text in this record)')+'</div>'
      + (themes ? '<p class="dline"><strong>Themes:</strong> '+themes+'</p>' : '')
      + (sdgs ? '<p class="dline"><strong>SDGs:</strong> '+sdgs+'</p>' : '')
      + (targets ? '<p class="dline"><strong>SDG targets:</strong></p><ul class="dlist">'+targets+'</ul>' : '')
      + (persons ? '<p class="dline"><strong>Affected persons:</strong> '+persons+'</p>' : '')
      + (countries.length ? '<p class="dline"><strong>Countries:</strong> '+esc(countries.join(', '))+'</p>' : '')
      + '<p class="dline"><a href="'+esc(url)+'" target="_blank" rel="noopener noreferrer">Open the UN document ('+esc(sym)+') ↗</a></p>'
      + '</td></tr>';
  }).join('');
}

$('recBody').addEventListener('click', function(e){
  if(e.target.closest('a')) return;
  var tr = e.target.closest('tr.rec');
  if(!tr) return;
  var det = document.getElementById('d' + tr.dataset.i);
  if(!det) return;
  var willOpen = det.hidden;
  det.hidden = !willOpen;
  tr.classList.toggle('open', willOpen);
  tr.setAttribute('aria-expanded', String(willOpen));
});

/* ---------- update ---------- */
function update(){
  var filtered = records.filter(matches);
  currentList = sortRecords(filtered);
  renderChart(filtered);
  renderTable(currentList);
  var parts = [];
  if(state.mechanism) parts.push('mechanism = ' + state.mechanism);
  if(state.body) parts.push('body/mandate = ' + state.body);
  if(state.from || state.to) parts.push('years ' + (state.from || (yearMin!=null?yearMin:'…')) + '–' + (state.to || (yearMax!=null?yearMax:'…')));
  if(state.sdg) parts.push('SDG ' + state.sdg + (sdgNames[state.sdg] ? ' (' + sdgNames[state.sdg] + ')' : ''));
  if(state.q) parts.push('keyword “' + state.q + '”');
  $('filterDesc').textContent = parts.length
    ? 'Active filters — ' + parts.join('; ')
    : 'No filters applied: all ' + records.length + ' records are shown.';
  $('chartN').textContent = '· ' + filtered.length + ' matching record' + (filtered.length===1?'':'s');
}

/* ---------- events ---------- */
$('fMechanism').addEventListener('change', function(e){ state.mechanism = e.target.value; update(); });
$('fBody').addEventListener('change', function(e){ state.body = e.target.value; update(); });
$('fSdg').addEventListener('change', function(e){ state.sdg = e.target.value; update(); });
$('fFrom').addEventListener('change', function(e){
  state.from = e.target.value;
  if(state.from && state.to && parseInt(state.from,10) > parseInt(state.to,10)){ state.to = state.from; $('fTo').value = state.to; }
  update();
});
$('fTo').addEventListener('change', function(e){
  state.to = e.target.value;
  if(state.from && state.to && parseInt(state.to,10) < parseInt(state.from,10)){ state.from = state.to; $('fFrom').value = state.from; }
  update();
});
$('fQ').addEventListener('input', function(e){ state.q = e.target.value.trim().toLowerCase(); update(); });
$('reset').addEventListener('click', function(){
  state.mechanism = state.body = state.from = state.to = state.sdg = state.q = '';
  ['fMechanism','fBody','fFrom','fTo','fSdg'].forEach(function(id){ $(id).value=''; });
  $('fQ').value = '';
  update();
});

update();
})();
</script>
</body>
</html>
```