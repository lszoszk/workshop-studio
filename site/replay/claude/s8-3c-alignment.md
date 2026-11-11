I added a second tab, “02 Map” (the existing view is now “01 Votes”, unchanged): every other State is placed on a square chart by how often it votes the same way as State A (across) and State B (up), coloured by UN regional group, with the dashed equal-agreement diagonal and a hover card. It follows the State pickers and the resolutions/amendments/all switch.

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Comparing two States’ votes at the Human Rights Council</title>
<style>
:root{
  --accent:#1f6fb2; --accent-soft:#e8f1fa; --ink:#1d2833; --muted:#5c6b7a;
  --line:#d8e1ea; --bg:#f4f7fa; --card:#ffffff;
  --yes-bg:#e2f1e4; --yes-ink:#1e6b2f;
  --no-bg:#fbe3e3; --no-ink:#a02121;
  --abs-bg:#eceff3; --abs-ink:#55606c;
  --warn:#9a6200;
}
*{box-sizing:border-box}
html,body{margin:0;padding:0}
body{font:16px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif;color:var(--ink);background:var(--bg)}
.wrap{max-width:1100px;margin:0 auto;padding:0 20px}
header.top{background:var(--card);border-bottom:1px solid var(--line);padding:22px 0 18px}
h1{margin:0 0 6px;font-size:1.5rem;line-height:1.25;color:var(--accent)}
p.desc{margin:0;color:var(--muted);max-width:75ch}
main{padding:20px 0 40px}
h2{font-size:1.12rem;margin:30px 0 6px}
.controls{display:flex;flex-wrap:wrap;gap:16px 26px;align-items:flex-end;background:var(--card);border:1px solid var(--line);border-radius:10px;padding:16px 18px;margin-top:18px}
.field{display:flex;flex-direction:column;gap:6px}
.field>label{font-size:.82rem;font-weight:600;color:var(--muted);text-transform:uppercase;letter-spacing:.04em}
select,button{font:inherit}
select{padding:8px 10px;border:1px solid var(--line);border-radius:7px;background:#fff;color:var(--ink);max-width:300px}
.seg{display:flex;border:1px solid var(--line);border-radius:7px;overflow:hidden}
.seg button{border:0;background:#fff;padding:8px 14px;cursor:pointer;color:var(--ink);border-right:1px solid var(--line)}
.seg button:last-child{border-right:0}
.seg button.active{background:var(--accent);color:#fff}
.seg button:focus-visible,select:focus-visible{outline:2px solid var(--accent);outline-offset:1px}
p.note{color:var(--muted);font-size:.9rem;margin:10px 2px 0;max-width:95ch}
.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));gap:14px;margin-top:18px}
.card{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:14px 16px}
.card .num{font-size:1.9rem;font-weight:700;color:var(--accent);line-height:1.15}
.card .lbl{color:var(--muted);font-size:.92rem;margin-top:2px}
p.breakdown{margin:10px 2px 0;font-size:.95rem}
p.how{color:var(--muted);font-size:.86rem;margin:8px 2px 0;max-width:95ch}
.chartWrap{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:14px 16px 8px;margin-top:10px;height:380px}
.tableWrap{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:6px 16px 14px;margin-top:10px;overflow-x:auto}
table{width:100%;border-collapse:collapse;font-size:.93rem}
th{text-align:left;font-size:.78rem;text-transform:uppercase;letter-spacing:.05em;color:var(--muted);padding:10px 10px 8px;border-bottom:2px solid var(--line);white-space:nowrap}
td{padding:9px 10px;border-bottom:1px solid var(--line);vertical-align:top}
tbody tr:hover{background:#f7fafd}
td.date{white-space:nowrap;color:var(--muted)}
td.titlecell{overflow-wrap:anywhere;min-width:260px}
a{color:var(--accent)}
.sym{color:var(--muted);font-size:.85rem}
.kind{display:inline-block;padding:2px 9px;border-radius:999px;font-size:.78rem;font-weight:600;white-space:nowrap}
.kind.resolution{background:var(--accent-soft);color:var(--accent)}
.kind.amendment{background:#f1e8f8;color:#6b3fa0}
.vote{display:inline-block;padding:2px 9px;border-radius:999px;font-size:.82rem;font-weight:600;white-space:nowrap}
.vote.Y{background:var(--yes-bg);color:var(--yes-ink)}
.vote.N{background:var(--no-bg);color:var(--no-ink)}
.vote.A{background:var(--abs-bg);color:var(--abs-ink)}
.match .ok{color:var(--yes-ink);font-weight:600;white-space:nowrap}
.match .no{color:var(--no-ink);font-weight:600;white-space:nowrap}
.warn{display:inline-block;margin-left:8px;color:var(--warn);font-size:.78rem;font-weight:600;cursor:help}
.msg{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:16px 18px;margin-top:18px;color:var(--muted)}
.tabs{display:flex;gap:4px;border-bottom:1px solid var(--line);margin-top:22px}
.tabs button{font:600 .78rem ui-monospace,Menlo,Consolas,monospace;letter-spacing:.08em;text-transform:uppercase;border:0;border-bottom:3px solid transparent;margin-bottom:-1px;background:none;padding:10px 16px;color:var(--muted);cursor:pointer}
.tabs button[aria-selected="true"]{color:var(--accent);border-bottom-color:var(--accent)}
.tabs button:focus-visible{outline:2px solid var(--accent);outline-offset:-2px}
.mapWrap{position:relative;max-width:660px;margin:12px auto 0;background:var(--card);border:1px solid var(--line);border-radius:10px;padding:8px}
.mapWrap svg{display:block;width:100%;height:auto}
.mapWrap text{font-family:inherit;fill:var(--muted)}
.mapWrap .axTitle{fill:var(--ink);font-weight:600}
.mapWrap circle.dot{stroke:#fff;stroke-width:1.2;fill-opacity:.88}
.mapWrap circle.dot.hot{stroke:var(--ink);stroke-width:2}
#mapTip{position:absolute;z-index:2;pointer-events:none;background:#1d2833;color:#fff;border-radius:7px;padding:8px 10px;font-size:.84rem;line-height:1.4;max-width:290px;box-shadow:0 2px 8px rgba(0,0,0,.25)}
#mapTip b{display:block;font-size:.9rem}
#mapTip .sep{display:block;margin-top:5px;padding-top:5px;border-top:1px solid #4b5a69}
.legend{display:flex;flex-wrap:wrap;gap:6px 18px;justify-content:center;max-width:760px;margin:12px auto 0;font-size:.88rem}
.legend span{display:inline-flex;align-items:center;gap:6px;white-space:nowrap}
.legend i{display:inline-block;width:12px;height:12px;border-radius:50%}
.legend em{font-style:normal;color:var(--muted)}
.legend .diag{display:inline-block;width:22px;border-top:2px dashed #5c6b7a;height:0}
.mapNote{max-width:660px;margin:10px auto 0}
[hidden]{display:none !important}
footer{color:var(--muted);font-size:.85rem;padding:26px 0 8px}
</style>
</head>
<body>
<header class="top"><div class="wrap">
  <h1>Comparing two States’ votes at the Human Rights Council</h1>
  <p class="desc" id="sourceLine"></p>
</div></header>
<main><div class="wrap">

  <section class="controls" id="controls" aria-label="Comparison settings">
    <div class="field"><label for="selA">State A</label><select id="selA"></select></div>
    <div class="field"><label for="selB">State B</label><select id="selB"></select></div>
    <div class="field"><label id="kindLbl">Votes included</label><div class="seg" id="kindSeg" role="group" aria-labelledby="kindLbl"></div></div>
    <div class="field"><label for="showAll">List below</label>
      <select id="showAll">
        <option value="diff">Differing votes only</option>
        <option value="all">All joint votes</option>
      </select>
    </div>
  </section>
  <p class="note" id="membersNote"></p>
  <p class="msg" id="fatal" hidden></p>
  <p class="msg" id="sameMsg" hidden></p>

  <section id="results" hidden>
    <div class="tabs" id="tabs" role="tablist" aria-label="Views">
      <button type="button" role="tab" id="tabVotes" aria-controls="panelVotes" aria-selected="true">01 Votes</button>
      <button type="button" role="tab" id="tabMap" aria-controls="panelMap" aria-selected="false" tabindex="-1">02 Map</button>
    </div>
    <div id="panelVotes" role="tabpanel" aria-labelledby="tabVotes">
    <div class="cards">
      <div class="card"><div class="num" id="statJoint">0</div><div class="lbl">recorded votes both States took part in</div></div>
      <div class="card"><div class="num" id="statSame">0</div><div class="lbl">of those, votes where they voted the same</div></div>
      <div class="card"><div class="num" id="statDiff">0</div><div class="lbl">votes where they differed</div></div>
    </div>
    <p class="breakdown" id="breakdown"></p>
    <p class="how" id="howStats"></p>

    <h2>Timeline by year</h2>
    <div class="chartWrap" id="chartWrap"><canvas id="chart" aria-label="Timeline of joint votes by year"></canvas></div>
    <p class="msg" id="chartEmpty" hidden>No recorded votes in the current filter where both States took part, so there is no timeline to draw.</p>
    <p class="how" id="howChart"></p>

    <h2 id="listTitle"></h2>
    <p class="how" id="howList"></p>
    <div class="tableWrap">
      <table>
        <thead><tr>
          <th>Date</th><th>Kind</th><th>Vote (title &amp; symbol)</th>
          <th id="thA">State A</th><th id="thB">State B</th><th>Same?</th>
        </tr></thead>
        <tbody id="tbody"></tbody>
      </table>
      <p class="msg" id="emptyList" hidden></p>
    </div>
    </div>

    <div id="panelMap" role="tabpanel" aria-labelledby="tabMap" hidden>
      <h2 id="mapTitle">Who votes like whom</h2>
      <p class="how" id="mapIntro"></p>
      <p class="msg" id="mapEmpty" hidden></p>
      <div id="mapBody">
        <div class="mapWrap" id="mapWrap"><svg id="mapSvg" viewBox="0 0 640 640" role="img" aria-label="Scatter chart of States by agreement with the two States picked"></svg><div id="mapTip" hidden></div></div>
        <div class="legend" id="mapLegend"></div>
      </div>
      <p class="how mapNote" id="mapRule"></p>
      <p class="how mapNote" id="mapLeaves"></p>
    </div>
  </section>

  <footer>All counts, filters, the chart and the list on this page are computed in your browser from the loaded dataset. Nothing is estimated, and no data leaves the page.</footer>
</div></main>

<script>
(function(){
"use strict";
var DATA = window.WORKSHOP_DATA || {};
var HRC = DATA.hrc || {};
var records = Array.isArray(HRC.records) ? HRC.records : [];
var countryNames = HRC.countries || {};
var voteCodes = HRC.vote_codes || {};

function $(id){ return document.getElementById(id); }
function esc(s){ return String(s==null?'':s).replace(/[&<>"']/g, function(c){ return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]; }); }
var FALLBACK_VOTES = {Y:'Yes', N:'No', A:'Abstain'};
function voteLabel(code){ return (voteCodes && voteCodes[code]) || FALLBACK_VOTES[code] || code; }
function yearOf(r){ if (typeof r.year === 'number') return r.year; var m = /^(\d{4})/.exec(r.date||''); return m ? +m[1] : null; }
function kindLabel(k){ return k==='all' ? 'all recorded votes (resolutions and amendments)' : (k==='resolution' ? 'resolutions only' : 'amendments only'); }
function kindBadge(r){
  var k = r.kind || '';
  var label = k==='resolution' ? 'Resolution' : k==='amendment' ? 'Amendment' : (k || '—');
  return '<span class="kind ' + esc(k) + '">' + esc(label) + '</span>';
}
function rollCall(r){
  var c = {Y:0, N:0, A:0}; var v = r.votes || {};
  for (var iso in v){ if (Object.prototype.hasOwnProperty.call(v,iso) && c[v[iso]]!==undefined) c[v[iso]]++; }
  return c;
}
function mismatchInfo(r){
  if (typeof r.yes!=='number' || typeof r.no!=='number' || typeof r.abstain!=='number') return null;
  var c = rollCall(r);
  if (c.Y===r.yes && c.N===r.no && c.A===r.abstain) return null;
  return c;
}

/* Index: ISO3 -> Map(record object -> vote code), built only from roll calls */
var byCountry = new Map();
records.forEach(function(r){
  var v = r.votes || {};
  for (var iso in v){
    if (!Object.prototype.hasOwnProperty.call(v, iso)) continue;
    if (!byCountry.has(iso)) byCountry.set(iso, new Map());
    byCountry.get(iso).set(r, v[iso]);
  }
});
var members = Array.from(byCountry.keys()).map(function(iso){
  return {iso: iso, name: countryNames[iso] || iso};
}).sort(function(a,b){ return a.name.localeCompare(b.name); });

var selA=$('selA'), selB=$('selB'), showAllSel=$('showAll'), results=$('results');
var currentKind = 'all';
var chart = null;
var activeTab = 'votes';

function fillSelect(sel, selectedIso){
  sel.innerHTML = '';
  members.forEach(function(m){
    var o = document.createElement('option');
    o.value = m.iso; o.textContent = m.name + ' (' + m.iso + ')';
    if (m.iso === selectedIso) o.selected = true;
    sel.appendChild(o);
  });
  if (selectedIso) sel.value = selectedIso;
}
function defaultA(){
  var uc = (DATA.uhri && DATA.uhri.country) || '';
  var m = members.find(function(x){ return x.name === uc; });
  return (m || members[0] || {}).iso;
}
function defaultB(isoA){
  var mapA = byCountry.get(isoA); var best = null;
  members.forEach(function(m){
    if (m.iso === isoA) return;
    var mapB = byCountry.get(m.iso), joint = 0, diff = 0;
    records.forEach(function(r){
      var va = mapA.get(r), vb = mapB.get(r);
      if (va!==undefined && vb!==undefined){ joint++; if (va!==vb) diff++; }
    });
    if (!best || diff>best.diff || (diff===best.diff && joint>best.joint) ||
        (diff===best.diff && joint===best.joint && m.name<best.name))
      best = {iso:m.iso, diff:diff, joint:joint, name:m.name};
  });
  return best ? best.iso : (members[1] || {}).iso;
}
function fillHeader(){
  var ys = records.map(yearOf).filter(function(y){ return y!=null; });
  var range = ys.length ? Math.min.apply(null,ys) + '–' + Math.max.apply(null,ys) : 'n/a';
  $('sourceLine').textContent =
    'Source: ' + (HRC.title || 'Human Rights Council recorded votes') + ' — ' + records.length +
    ' recorded votes, ' + range + '. Each record is a recorded vote (resolution or amendment) with the roll call of the Council members ' +
    '(Y/N/A = ' + voteLabel('Y') + ' / ' + voteLabel('N') + ' / ' + voteLabel('A') + '). Only States that appear in at least one roll call are offered below.';
}
function buildKindSeg(){
  var nRes = records.filter(function(r){ return r.kind==='resolution'; }).length;
  var nAmd = records.filter(function(r){ return r.kind==='amendment'; }).length;
  var seg = $('kindSeg'); seg.innerHTML = '';
  [['all','All ('+records.length+')'], ['resolution','Resolutions ('+nRes+')'], ['amendment','Amendments ('+nAmd+')']]
  .forEach(function(pair){
    var k = pair[0], b = document.createElement('button');
    b.type = 'button'; b.textContent = pair[1]; b.dataset.kind = k;
    b.className = (k===currentKind) ? 'active' : '';
    b.setAttribute('aria-pressed', k===currentKind ? 'true' : 'false');
    b.addEventListener('click', function(){
      currentKind = k;
      Array.prototype.forEach.call(seg.children, function(c){
        var on = c.dataset.kind === k;
        c.classList.toggle('active', on);
        c.setAttribute('aria-pressed', on ? 'true' : 'false');
      });
      render();
    });
    seg.appendChild(b);
  });
}

function render(){
  var isoA = selA.value, isoB = selB.value;
  if (!isoA || !isoB){ results.hidden = true; return; }
  var nameA = countryNames[isoA] || isoA, nameB = countryNames[isoB] || isoB;
  if (isoA === isoB){
    results.hidden = true;
    var sm = $('sameMsg'); sm.hidden = false;
    sm.textContent = 'State A and State B are the same State (' + nameA + '). Pick two different States to compare.';
    return;
  }
  $('sameMsg').hidden = true;
  results.hidden = false;

  var mapA = byCountry.get(isoA), mapB = byCountry.get(isoB);
  var rows = [];
  records.forEach(function(r){
    if (currentKind !== 'all' && r.kind !== currentKind) return;
    var va = mapA.get(r), vb = mapB.get(r);
    if (va === undefined || vb === undefined) return;
    rows.push({r:r, va:va, vb:vb, same: va===vb});
  });

  var joint = rows.length, same = 0, both = {Y:0, N:0, A:0};
  rows.forEach(function(x){ if (x.same){ same++; if (both[x.va]!==undefined) both[x.va]++; } });
  var diff = joint - same;

  $('statJoint').textContent = joint;
  $('statSame').textContent = joint ? same + ' (' + Math.round(100*same/joint) + '%)' : '0';
  $('statDiff').textContent = diff;
  $('breakdown').textContent = 'Of the ' + joint + ' joint votes: both Yes ' + both.Y +
    ', both No ' + both.N + ', both Abstain ' + both.A + '. Filter: ' + kindLabel(currentKind) + '.';
  $('howStats').textContent = 'How this is computed: for every recorded vote in the current filter, each State’s roll-call code (Y/N/A) is looked up. ' +
    '“Both took part” = both States appear in that vote’s roll call; “same” = identical code. These are exact counts of the loaded records, not estimates.';

  renderChart(rows);
  renderList(rows, nameA, nameB);
  if (activeTab === 'map') renderMap(isoA, isoB, nameA, nameB);
}

function renderChart(rows){
  var byYear = new Map();
  rows.forEach(function(x){
    var y = yearOf(x.r); if (y == null) return;
    if (!byYear.has(y)) byYear.set(y, {joint:0, same:0});
    var e = byYear.get(y); e.joint++; if (x.same) e.same++;
  });
  var years = Array.from(byYear.keys()).sort(function(a,b){ return a-b; });
  if (chart){ chart.destroy(); chart = null; }
  if (!years.length || !window.Chart){
    $('chartWrap').style.display = 'none'; $('chartEmpty').hidden = false; return;
  }
  $('chartWrap').style.display = ''; $('chartEmpty').hidden = true;
  var jointArr = years.map(function(y){ return byYear.get(y).joint; });
  var sameArr  = years.map(function(y){ return byYear.get(y).same; });
  var pctArr   = years.map(function(y){ var e = byYear.get(y); return e.joint ? Math.round(100*e.same/e.joint) : null; });

  chart = new Chart($('chart').getContext('2d'), {
    type: 'bar',
    data: { labels: years.map(String), datasets: [
      {type:'bar',  label:'Votes both took part', data:jointArr, backgroundColor:'#1f6fb2', borderRadius:3, maxBarThickness:42},
      {type:'bar',  label:'Voted the same',       data:sameArr,  backgroundColor:'#a9cdea', borderRadius:3, maxBarThickness:42},
      {type:'line', label:'% voted the same',     data:pctArr,   yAxisID:'y1', borderColor:'#2e7d32', backgroundColor:'#2e7d32', fill:false, tension:.25, pointRadius:3}
    ]},
    options: {
      responsive:true, maintainAspectRatio:false,
      interaction:{mode:'index', intersect:false},
      plugins:{
        legend:{position:'bottom'},
        tooltip:{ callbacks:{ label:function(ctx){
          if (ctx.datasetIndex === 2){
            var e = byYear.get(years[ctx.dataIndex]);
            return '% voted the same: ' + pctArr[ctx.dataIndex] + '% (' + e.same + ' of ' + e.joint + ')';
          }
          return ctx.dataset.label + ': ' + ctx.parsed.y;
        }}}
      },
      scales:{
        y:{beginAtZero:true, title:{display:true, text:'Recorded votes'}, ticks:{precision:0}},
        y1:{position:'right', min:0, max:100, title:{display:true, text:'% voted the same'},
            grid:{drawOnChartArea:false}, ticks:{callback:function(v){ return v+'%'; }}}
      }
    }
  });
  $('howChart').textContent = 'How this is computed: one group of bars per year (each record’s year), counting only votes in the current filter where both States appear in the roll call; ' +
    'the green line is the share of those joint votes that were the same (right axis).';
}

function voteBadge(code){
  return '<span class="vote ' + esc(code) + '" title="Roll-call code ' + esc(code) + '">' + esc(voteLabel(code)) + ' (' + esc(code) + ')</span>';
}
function buildRow(x){
  var r = x.r;
  var link = r.doc_url || r.record_url || '';
  var sym = r.symbol ? (link ? '<a href="'+esc(link)+'" target="_blank" rel="noopener">'+esc(r.symbol)+'</a>' : esc(r.symbol)) : '—';
  var title = r.title ? (link ? '<a href="'+esc(link)+'" target="_blank" rel="noopener">'+esc(r.title)+'</a>' : esc(r.title)) : '(untitled vote)';
  var warn = '';
  var mm = mismatchInfo(r);
  if (mm) warn = ' <span class="warn" title="Official totals (yes/no/abstain) are ' + r.yes + '/' + r.no + '/' + r.abstain +
    ', but counting the roll call gives ' + mm.Y + '/' + mm.N + '/' + mm.A +
    '. Both figures are shown; neither is silently preferred.">⚠ totals ' + r.yes + '/' + r.no + '/' + r.abstain +
    ' ≠ roll call ' + mm.Y + '/' + mm.N + '/' + mm.A + '</span>';
  var tr = document.createElement('tr');
  tr.innerHTML =
    '<td class="date">' + esc(r.date || '—') + '</td>' +
    '<td>' + kindBadge(r) + '</td>' +
    '<td class="titlecell">' + title + '<br><span class="sym">' + sym + '</span>' + warn + '</td>' +
    '<td>' + voteBadge(x.va) + '</td>' +
    '<td>' + voteBadge(x.vb) + '</td>' +
    '<td class="match">' + (x.same ? '<span class="ok">✓ same</span>' : '<span class="no">✗ differs</span>') + '</td>';
  return tr;
}
function renderList(rows, nameA, nameB){
  var showAll = showAllSel.value === 'all';
  var list = showAll ? rows.slice() : rows.filter(function(x){ return !x.same; });
  list.sort(function(a,b){
    var da = a.r.date || '', db = b.r.date || '';
    if (da !== db) return da < db ? 1 : -1;
    return String(a.r.symbol||'').localeCompare(String(b.r.symbol||''));
  });
  $('listTitle').textContent = showAll ? 'All joint votes (' + list.length + ')'
                                      : 'Votes where ' + nameA + ' and ' + nameB + ' differed (' + list.length + ')';
  $('howList').textContent = 'How this is computed: every recorded vote in the current filter (' + kindLabel(currentKind) +
    ') where both States appear in the roll call' + (showAll ? '' : ' and their codes differ') +
    ', most recent first. The symbol links to the UN document in a new tab. ⚠ marks records where the official totals (yes/no/abstain) do not match counting the roll call — both figures are shown.';
  $('thA').textContent = nameA; $('thB').textContent = nameB;
  var tb = $('tbody'); tb.innerHTML = '';
  list.forEach(function(x){ tb.appendChild(buildRow(x)); });
  $('emptyList').hidden = list.length > 0;
  if (!list.length) $('emptyList').textContent = 'No votes to show for this combination of States and filter.';
}


/* ---------- Tabs ---------- */
var tabBtns = {votes: $('tabVotes'), map: $('tabMap')};
var panels = {votes: $('panelVotes'), map: $('panelMap')};
function setTab(name, focus){
  activeTab = name;
  Object.keys(tabBtns).forEach(function(k){
    var on = k === name;
    tabBtns[k].setAttribute('aria-selected', on ? 'true' : 'false');
    tabBtns[k].tabIndex = on ? 0 : -1;
    panels[k].hidden = !on;
  });
  if (focus) tabBtns[name].focus();
  if (name === 'map') render(); else if (chart) chart.resize();
}
Object.keys(tabBtns).forEach(function(k){
  tabBtns[k].addEventListener('click', function(){ setTab(k, false); });
  tabBtns[k].addEventListener('keydown', function(e){
    var order = ['votes','map'], i = order.indexOf(k), n = null;
    if (e.key === 'ArrowRight' || e.key === 'ArrowDown') n = order[(i+1) % order.length];
    else if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') n = order[(i+order.length-1) % order.length];
    else if (e.key === 'Home') n = order[0];
    else if (e.key === 'End') n = order[order.length-1];
    if (n){ e.preventDefault(); setTab(n, true); }
  });
});

/* ---------- Map: agreement with State A (across) and State B (up) ---------- */
var GROUPS = HRC.groups || {};
var GROUP_ORDER = [
  ['African States', '#c4501b'],
  ['Asia-Pacific States', '#1f6fb2'],
  ['Eastern European States', '#7b3fa0'],
  ['Latin American and Caribbean States', '#1e8a4c'],
  ['Western European and other States', '#9a7400']
];
var OTHER_GROUP = ['Other', '#7f8a96'];
var GROUP_COLOR = {}; GROUP_ORDER.forEach(function(g){ GROUP_COLOR[g[0]] = g[1]; });
function groupOf(iso){ var g = GROUPS[iso]; return GROUP_COLOR[g] ? g : OTHER_GROUP[0]; }
function colorOf(g){ return GROUP_COLOR[g] || OTHER_GROUP[1]; }

var MIN_SHARED = 10;
var PLOT = {x0:76, y0:20, size:540};   /* plot square inside the 640x640 viewBox */
var mapPts = [];
var SVGNS = 'http://www.w3.org/2000/svg';
function svgEl(name, attrs, text){
  var e = document.createElementNS(SVGNS, name);
  for (var k in attrs) e.setAttribute(k, attrs[k]);
  if (text != null) e.textContent = text;
  return e;
}
function pct1(n, d){ return (100*n/d).toFixed(1) + '%'; }
function computeMap(isoA, isoB){
  var recs = records.filter(function(r){ return currentKind === 'all' || r.kind === currentKind; });
  var pts = [], left = 0, total = 0;
  Object.keys(countryNames).forEach(function(iso){
    if (iso === isoA || iso === isoB) return;
    total++;
    var sa=0, na=0, sb=0, nb=0;
    recs.forEach(function(r){
      var v = r.votes || {}, x = v[iso];
      if (x === undefined) return;
      var a = v[isoA], b = v[isoB];
      if (a !== undefined){ na++; if (a === x) sa++; }
      if (b !== undefined){ nb++; if (b === x) sb++; }
    });
    if (na < MIN_SHARED || nb < MIN_SHARED){ left++; return; }
    pts.push({iso:iso, name:countryNames[iso] || iso, group:groupOf(iso), sa:sa, na:na, sb:sb, nb:nb, ax:100*sa/na, ay:100*sb/nb});
  });
  return {pts:pts, left:left, total:total, nrec:recs.length};
}
function renderMap(isoA, isoB, nameA, nameB){
  var m = computeMap(isoA, isoB);
  mapPts = m.pts;
  $('mapIntro').textContent = 'Each dot is a State. Across: how often it votes the same way as ' + nameA +
    '. Up: how often it votes the same way as ' + nameB + '. Dots above the dashed line agree more with ' + nameB +
    '; dots below it agree more with ' + nameA + '. Votes included: ' + kindLabel(currentKind) + ' (' + m.nrec + ' recorded votes).';
  $('mapRule').textContent = 'How this is computed: a State’s agreement with ' + nameA + ' (or ' + nameB +
    ') = recorded votes where both voted the same ÷ recorded votes where both took part; Yes, No and Abstain each count as a choice of its own. ' +
    'The two shares use different sets of votes, and only States with at least ' + MIN_SHARED + ' shared votes with each are drawn: ' +
    m.pts.length + ' drawn, ' + m.left + ' left out (' + nameA + ' and ' + nameB + ' themselves are not plotted).';
  $('mapLeaves').textContent = 'What this map leaves out: texts adopted without a vote. They have no roll call, so they are not in this data; ' +
    'the map shows how States split on the votes that were called, not how they agree on the rest.';
  var svg = $('mapSvg'); svg.innerHTML = '';
  $('mapTip').hidden = true;
  var empty = $('mapEmpty');
  if (!m.pts.length){
    $('mapBody').hidden = true; empty.hidden = false;
    empty.textContent = 'No State has at least ' + MIN_SHARED + ' shared votes with both ' + nameA + ' and ' + nameB +
      ' in this selection (' + m.left + ' States left out), so there is nothing to plot. Try “All” votes or other States.';
    return;
  }
  $('mapBody').hidden = false; empty.hidden = true;

  var P = PLOT, X = function(v){ return P.x0 + v/100*P.size; }, Y = function(v){ return P.y0 + P.size - v/100*P.size; };
  svg.appendChild(svgEl('rect', {x:P.x0, y:P.y0, width:P.size, height:P.size, fill:'#fbfcfd', stroke:'#c3cfdb'}));
  for (var t = 0; t <= 100; t += 20){
    if (t > 0 && t < 100){
      svg.appendChild(svgEl('line', {x1:X(t), y1:P.y0, x2:X(t), y2:P.y0+P.size, stroke:'#e6ecf2'}));
      svg.appendChild(svgEl('line', {x1:P.x0, y1:Y(t), x2:P.x0+P.size, y2:Y(t), stroke:'#e6ecf2'}));
    }
    svg.appendChild(svgEl('text', {x:X(t), y:P.y0+P.size+20, 'text-anchor':'middle', 'font-size':14}, t + '%'));
    svg.appendChild(svgEl('text', {x:P.x0-10, y:Y(t)+5, 'text-anchor':'end', 'font-size':14}, t + '%'));
  }
  svg.appendChild(svgEl('line', {x1:X(0), y1:Y(0), x2:X(100), y2:Y(100), stroke:'#5c6b7a', 'stroke-width':1.6, 'stroke-dasharray':'7 5'}));
  svg.appendChild(svgEl('text', {x:P.x0+P.size/2, y:P.y0+P.size+48, 'text-anchor':'middle', 'font-size':16, 'class':'axTitle'}, 'Agreement with ' + nameA));
  svg.appendChild(svgEl('text', {x:0, y:0, 'text-anchor':'middle', 'font-size':16, 'class':'axTitle',
    transform:'translate(20,' + (P.y0+P.size/2) + ') rotate(-90)'}, 'Agreement with ' + nameB));
  var order = GROUP_ORDER.map(function(g){ return g[0]; }).concat([OTHER_GROUP[0]]);
  var dots = m.pts.slice().sort(function(a,b){
    return order.indexOf(a.group) - order.indexOf(b.group) || a.name.localeCompare(b.name);
  });
  dots.forEach(function(p){
    p.cx = X(p.ax); p.cy = Y(p.ay);
    p.el = svgEl('circle', {'class':'dot', cx:p.cx, cy:p.cy, r:6, fill:colorOf(p.group), 'data-iso':p.iso});
    svg.appendChild(p.el);
  });
  var counts = {}; m.pts.forEach(function(p){ counts[p.group] = (counts[p.group]||0) + 1; });
  var lg = $('mapLegend'); lg.innerHTML = '';
  GROUP_ORDER.concat(counts[OTHER_GROUP[0]] ? [OTHER_GROUP] : []).forEach(function(g){
    var s = document.createElement('span');
    s.innerHTML = '<i style="background:' + g[1] + '"></i>' + esc(g[0]) + ' <em>(' + (counts[g[0]]||0) + ')</em>';
    lg.appendChild(s);
  });
  var d = document.createElement('span');
  d.innerHTML = '<span class="diag"></span>equal agreement with both';
  lg.appendChild(d);
  mapTipNames = {a:nameA, b:nameB};
}
var mapTipNames = {a:'State A', b:'State B'};
function tipHtml(p){
  return '<b>' + esc(p.name) + '</b>' + esc(p.group) +
    '<span class="sep">With ' + esc(mapTipNames.a) + ': ' + pct1(p.sa, p.na) + ' (' + p.sa + ' of ' + p.na + ' shared votes)</span>' +
    'With ' + esc(mapTipNames.b) + ': ' + pct1(p.sb, p.nb) + ' (' + p.sb + ' of ' + p.nb + ' shared votes)';
}
(function(){
  var svg = $('mapSvg'), tip = $('mapTip'), wrap = $('mapWrap'), hot = [];
  function clear(){ hot.forEach(function(p){ p.el.classList.remove('hot'); }); hot = []; tip.hidden = true; }
  svg.addEventListener('mousemove', function(e){
    var box = svg.getBoundingClientRect(), k = 640 / box.width;
    var mx = (e.clientX - box.left) * k, my = (e.clientY - box.top) * k;
    var near = mapPts.filter(function(p){ return Math.hypot(p.cx-mx, p.cy-my) <= 9; })
      .sort(function(a,b){ return Math.hypot(a.cx-mx,a.cy-my) - Math.hypot(b.cx-mx,b.cy-my); }).slice(0,3);
    if (!near.length){ clear(); return; }
    hot.forEach(function(p){ p.el.classList.remove('hot'); });
    hot = near; near.forEach(function(p){ p.el.classList.add('hot'); });
    tip.innerHTML = near.map(tipHtml).join('<span class="sep"></span>');
    tip.hidden = false;
    var wb = wrap.getBoundingClientRect();
    var left = e.clientX - wb.left + 14, top = e.clientY - wb.top + 14;
    if (left + tip.offsetWidth > wb.width - 4) left = e.clientX - wb.left - tip.offsetWidth - 14;
    if (top + tip.offsetHeight > wb.height - 4) top = e.clientY - wb.top - tip.offsetHeight - 14;
    tip.style.left = Math.max(4, left) + 'px'; tip.style.top = Math.max(4, top) + 'px';
  });
  svg.addEventListener('mouseleave', clear);
})();

selA.addEventListener('change', render);
selB.addEventListener('change', render);
showAllSel.addEventListener('change', render);

function main(){
  if (!records.length){
    $('controls').style.display = 'none';
    $('fatal').hidden = false;
    $('fatal').textContent = 'The loaded dataset contains no recorded votes, so there is nothing to compare.';
    return;
  }
  fillHeader();
  if (members.length < 2){
    $('controls').style.display = 'none';
    $('fatal').hidden = false;
    $('fatal').textContent = 'Fewer than two States appear in any roll call in the loaded data, so no comparison is possible.';
    return;
  }
  var a = defaultA(), b = defaultB(a);
  fillSelect(selA, a);
  fillSelect(selB, b);
  buildKindSeg();
  $('membersNote').textContent = members.length + ' States appear in at least one roll call (i.e. were Council members for at least one recorded vote) and can be picked above. ' +
    'Vote codes: Y = ' + voteLabel('Y') + ', N = ' + voteLabel('N') + ', A = ' + voteLabel('A') + '. “Both took part” means both States appear in a vote’s roll call.';
  render();
}
main();
})();
</script>
</body>
</html>
```
