I added a "Who recommends what" tab beside the existing dashboard. It reads UPR recommendations only, extracts the recommending State from the parentheses at the end of each text, shows the top 15 States as a clickable bar chart, a table of each State's most-cited SDGs, and a list of that State's recommendations (symbols linked, full text on click) — plus a count of UPR recommendations with no State in parentheses.

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Human rights recommendations dashboard</title>
<style>
  :root{--accent:#1f6fb2;--accent-dark:#175a91;--accent-soft:#e8f1f8;--ink:#1c2733;--muted:#5b6b7b;--line:#dce3ec;--bg:#f4f6f9;--card:#fff}
  *{box-sizing:border-box}
  html,body{margin:0}
  body{font:16px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif;color:var(--ink);background:var(--bg)}
  .wrap{max-width:1200px;margin:0 auto;padding:30px 26px 70px}
  a{color:var(--accent)}
  h1{font-size:27px;line-height:1.25;margin:0 0 6px}
  h2{font-size:18px;margin:0}
  .desc{margin:0;color:var(--muted)}
  .desc a{font-weight:600}
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
  .btn-ghost{border:1px solid var(--line);background:#fff;color:var(--muted);font:inherit;padding:7px 12px;border-radius:6px;cursor:pointer}
  .btn-ghost:hover{border-color:var(--accent);color:var(--accent)}
  .chips{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin:0 0 12px}
  .chip{display:inline-flex;align-items:center;gap:7px;background:var(--accent-soft);color:var(--accent-dark);border:1px solid #bcd6ea;border-radius:999px;padding:3px 6px 3px 11px;font-size:13px;cursor:pointer}
  .chip:hover{background:#dbeaf6}
  .chip .x{font-weight:700;padding:0 4px}
  .chips .lbl{font-size:13.5px;color:var(--muted)}
  .chart-box{position:relative;height:400px;margin-top:8px}
  .placeholder{display:none;padding:34px 10px;text-align:center;color:var(--muted);background:#f8fafc;border:1px dashed var(--line);border-radius:8px}
  .summary-line{font-size:15px;margin:0}
  .summary-line strong{color:var(--accent);font-size:17px}
  .sort-field{display:flex;align-items:center;gap:8px;font-size:13.5px;color:var(--muted)}
  .sort-field select{padding:5px 8px;border:1px solid var(--line);border-radius:6px;font:inherit;font-size:13.5px;background:#fff;color:var(--ink)}
  .table-scroll{overflow-x:auto;margin-top:4px}
  table.tbl{width:100%;border-collapse:collapse;font-size:15px}
  .tbl th{text-align:left;font-size:11.5px;font-weight:700;text-transform:uppercase;letter-spacing:.05em;color:var(--muted);border-bottom:2px solid var(--line);padding:9px 10px;white-space:nowrap}
  .tbl td{padding:9px 10px;border-bottom:1px solid var(--line);vertical-align:top}
  .tbl .nowrap{white-space:nowrap}
  .tbl .sub{font-size:12.5px;color:var(--muted);margin-top:2px}
  tr.doc{cursor:pointer}
  tr.doc:hover{background:#f2f7fb}
  tr.doc:focus-visible{outline:2px solid var(--accent);outline-offset:-2px}
  tr.doc.open{background:#eef5fb}
  tr.pick{cursor:pointer}
  tr.pick:hover{background:#f2f7fb}
  tr.pick:focus-visible{outline:2px solid var(--accent);outline-offset:-2px}
  tr.pick.sel td{background:#eef5fb}
  .hint{color:var(--muted);font-size:12px;white-space:nowrap}
  tr.detail td{background:#f7fafd;padding:14px 16px 16px}
  .dlabel{font-size:11.5px;font-weight:700;text-transform:uppercase;letter-spacing:.05em;color:var(--muted);margin-bottom:5px}
  .fulltext{white-space:pre-wrap;margin:0 0 12px;font-size:15px}
  .meta-row{display:flex;gap:10px;margin-top:6px;font-size:13.5px}
  .meta-row .mlbl{flex:0 0 130px;color:var(--muted);font-weight:600}
  .tags{display:inline-flex;flex-wrap:wrap;gap:5px}
  .tag{background:var(--accent-soft);color:var(--accent-dark);border-radius:4px;padding:1px 7px;font-size:12.5px}
  .targets{margin:4px 0 0;padding-left:18px;font-size:13px;color:var(--ink)}
  .targets li{margin:1px 0}
  .table-foot{display:flex;justify-content:space-between;align-items:center;gap:12px;flex-wrap:wrap;margin-top:12px;font-size:13.5px;color:var(--muted)}
  .warn{background:#fdf6e7;border:1px solid #ecd9ad;border-radius:10px;padding:14px 18px;margin-top:18px;color:#6b5615}
  .tabs{display:flex;gap:4px;margin-top:22px;border-bottom:2px solid var(--line)}
  .tab{appearance:none;border:none;background:none;font:inherit;font-weight:600;color:var(--muted);padding:10px 16px;cursor:pointer;border-bottom:3px solid transparent;margin-bottom:-2px}
  .tab:hover{color:var(--accent)}
  .tab[aria-selected="true"]{color:var(--accent);border-bottom-color:var(--accent)}
</style>
</head>
<body>
<div class="wrap">
  <header>
    <h1 id="pageTitle">Human rights recommendations &amp; observations</h1>
    <p class="desc" id="pageDesc"></p>
  </header>

  <div id="noDataWarn" class="warn" style="display:none"></div>

  <nav class="tabs" role="tablist" aria-label="Dashboard sections">
    <button class="tab" id="tabOverview" role="tab" type="button" aria-selected="true" aria-controls="panelOverview">Recommendations &amp; observations</button>
    <button class="tab" id="tabStates" role="tab" type="button" aria-selected="false" aria-controls="panelStates" tabindex="-1">Who recommends what</button>
  </nav>

  <section id="panelOverview" role="tabpanel" aria-labelledby="tabOverview">
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
      <p class="note">Filters combine: a record must match all of them. The keyword search is case-insensitive and looks only at the paragraph text and the document symbol. This tab covers all mechanisms; the second tab looks at UPR alone and ignores these filters.</p>
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
  </section>

  <section id="panelStates" role="tabpanel" aria-labelledby="tabStates" hidden>
    <p class="summary-line" id="uprSummary" style="margin-top:18px"></p>
    <section class="kpis" id="uprKpis"></section>
    <p class="note" id="uprScope"></p>

    <section class="card">
      <div class="card-head">
        <h2>Top 15 recommending States</h2>
        <button id="clearStateBtn" class="btn-ghost" type="button" hidden>Clear selection</button>
      </div>
      <div class="chart-box"><canvas id="stateChart" aria-label="Bar chart of the States that made the most UPR recommendations"></canvas></div>
      <div id="stateChartEmpty" class="placeholder"></div>
      <p class="note" id="stateChartNote"></p>
    </section>

    <section class="card">
      <div class="card-head"><h2>SDGs each top State raises most</h2></div>
      <div class="table-scroll">
        <table class="tbl">
          <thead><tr><th>Recommending State</th><th>UPR recs</th><th>Most-cited SDGs</th></tr></thead>
          <tbody id="sdgBody"></tbody>
        </table>
      </div>
      <p class="note">How this is computed: for each of the top 15 States above, its recommendations are counted once for every SDG they cite — a recommendation can cite several SDGs or none. The three SDGs with the highest counts are shown, with the number of that State’s recommendations citing them. Click a State to list its recommendations.</p>
    </section>

    <section class="card">
      <h2 id="stateDetailTitle">Recommendations by State</h2>
      <p class="summary-line" id="stateDetailSummary" style="margin-top:8px"></p>
      <div id="stateDetailEmpty" class="placeholder"></div>
      <div class="table-scroll" id="stateTableWrap">
        <table class="tbl">
          <thead><tr><th>Date</th><th>Symbol</th><th>Recommendation (first line)</th></tr></thead>
          <tbody id="stateTbody"></tbody>
        </table>
      </div>
      <div class="table-foot" id="stateFoot"></div>
      <p class="note">How this is read: each row is one UPR recommendation, newest first; the recommending State is taken from the parentheses at the end of its text. Click a row to read the full, unedited text. Symbols link to the UN document, opened in a new tab. These records also appear in the first tab under the mechanism filter “Universal Periodic Review”.</p>
    </section>
  </section>
</div>

<script>
(function(){
'use strict';

/* ---------- data ---------- */
var U=(window.WORKSHOP_DATA&&window.WORKSHOP_DATA.uhri)?window.WORKSHOP_DATA.uhri:{};
var REC=Array.isArray(U.records)?U.records:[];
var SDG_NAMES=(U.sdg_names&&typeof U.sdg_names==='object')?U.sdg_names:{};
var COUNTRY=U.country||'the country';

/* ---------- helpers ---------- */
function esc(s){return String(s==null?'':s).replace(/[&<>"']/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c];});}
function fmtDate(d){
  if(!d)return '—';
  var s=String(d),m=s.match(/^(\d{4})-(\d{2})-(\d{2})$/);
  if(m){var mo=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];return parseInt(m[3],10)+' '+mo[parseInt(m[2],10)-1]+' '+m[1];}
  return s;
}
function firstLine(t){
  if(!t)return '—';
  var line=String(t).trim().split(/\r?\n/)[0].trim();
  if(line.length>170)line=line.slice(0,170).replace(/\s+\S*$/,'')+'…';
  return line||'—';
}
function tally(fn){var m=new Map();REC.forEach(function(r){var v=fn(r);if(v===null||v===undefined||v==='')return;m.set(v,(m.get(v)||0)+1);});return m;}
function byCountThenAlpha(a,b){return b[1]-a[1]||String(a[0]).localeCompare(String(b[0]));}
function plural(n,w){return n+' '+w+(n===1?'':'s');}
function pct(n,d){return d?Math.round(100*n/d)+'%':'—';}
function wrapLabel(s,max){var words=String(s).split(' '),lines=[],cur='';words.forEach(function(w){if((cur?cur+' '+w:w).length>max&&cur){lines.push(cur);cur=w;}else cur=cur?cur+' '+w:w;});if(cur)lines.push(cur);return lines;}
function topSdgs(recs,howMany){
  var c=new Map();
  recs.forEach(function(r){(Array.isArray(r.sdgs)?r.sdgs:[]).forEach(function(n){if(n!=null){n=Number(n);c.set(n,(c.get(n)||0)+1);}});});
  return Array.from(c).sort(function(a,b){return b[1]-a[1]||a[0]-b[0];}).slice(0,howMany);
}

/* ---------- dataset-level facts (all computed, never hard-coded) ---------- */
var yearsAll=REC.map(function(r){return typeof r.year==='number'?r.year:null;}).filter(function(v){return v!==null;});
var minYear=yearsAll.length?Math.min.apply(null,yearsAll):null;
var maxYear=yearsAll.length?Math.max.apply(null,yearsAll):null;
var nDocs=new Set(REC.map(function(r){return r.symbol||null;}).filter(Boolean)).size;
var bodyTally=tally(function(r){return r.body;});
var typeTally=tally(function(r){return r.type;});
var nRecs=typeTally.get('Recommendations')||0;
var nObs=typeTally.get('Concerns/Observations')||0;
var nOtherType=REC.length-nRecs-nObs;

document.getElementById('pageTitle').textContent='Human rights recommendations & observations addressed to '+COUNTRY;
document.title='UN recommendations — '+COUNTRY;
(function(){
  var bits=[];
  if(U.title)bits.push(esc(U.title));
  if(U.source)bits.push('Source: '+(U.source_url?'<a href="'+esc(U.source_url)+'" target="_blank" rel="noopener">'+esc(U.source)+'</a>':esc(U.source)));
  bits.push('n = '+plural(REC.length,'record'));
  if(minYear!==null)bits.push(minYear===maxYear?String(minYear):minYear+'–'+maxYear);
  if(U.built)bits.push('dataset built '+esc(U.built));
  document.getElementById('pageDesc').innerHTML=bits.join(' &middot; ');
})();
(function(){
  var typeSub=plural(nRecs,'recommendation')+' &middot; '+plural(nObs,'concern / observation');
  if(nOtherType>0)typeSub+=' &middot; '+plural(nOtherType,'other type');
  var period=minYear===null?'—':(minYear===maxYear?String(minYear):minYear+'–'+maxYear);
  document.getElementById('kpis').innerHTML=
    '<div class="kpi"><div class="n">'+REC.length+'</div><div class="lbl">Paragraph records</div><div class="sub">'+typeSub+'</div></div>'+
    '<div class="kpi"><div class="n">'+nDocs+'</div><div class="lbl">UN documents</div><div class="sub">distinct symbols</div></div>'+
    '<div class="kpi"><div class="n">'+bodyTally.size+'</div><div class="lbl">Bodies &amp; mandates</div><div class="sub">treaty bodies, UPR, Special Procedures</div></div>'+
    '<div class="kpi"><div class="n">'+period+'</div><div class="lbl">Period covered</div><div class="sub">years of the records</div></div>';
  document.getElementById('kpiNote').textContent='How this is computed: every number above is counted directly from the loaded records — one record is one paragraph of a UN document (a recommendation or an observation). Nothing is estimated.';
})();
if(!REC.length){
  var w=document.getElementById('noDataWarn');w.style.display='block';
  w.textContent='No records were found in WORKSHOP_DATA.uhri for this country, so there is nothing to filter, chart or list below.';
}

/* ---------- tabs ---------- */
var tabOverview=document.getElementById('tabOverview'),tabStates=document.getElementById('tabStates');
var panelOverview=document.getElementById('panelOverview'),panelStates=document.getElementById('panelStates');
function showTab(which){
  var s=which==='states';
  tabOverview.setAttribute('aria-selected',String(!s));tabStates.setAttribute('aria-selected',String(s));
  tabOverview.tabIndex=s?-1:0;tabStates.tabIndex=s?0:-1;
  panelOverview.hidden=s;panelStates.hidden=!s;
  if(s){ensureStateChart();if(stateChart)stateChart.resize();}
  if(!s&&chart)chart.resize();
}
tabOverview.addEventListener('click',function(){showTab('overview');});
tabStates.addEventListener('click',function(){showTab('states');});

/* ---------- filter state & controls ---------- */
var state={mechanism:'',body:'',sdg:'',yearFrom:minYear,yearTo:maxYear,q:'',theme:''};
var fMech=document.getElementById('fMech'),fBody=document.getElementById('fBody'),
    fFrom=document.getElementById('fFrom'),fTo=document.getElementById('fTo'),
    fSdg=document.getElementById('fSdg'),fQ=document.getElementById('fQ'),fSort=document.getElementById('fSort');
function fillSelect(sel,entries,placeholder){
  sel.innerHTML='';sel.add(new Option(placeholder,''));
  entries.forEach(function(e){sel.add(new Option(e[1],String(e[0])));});
}
fillSelect(fMech,Array.from(tally(function(r){return r.mechanism;})).sort(byCountThenAlpha).map(function(e){return [e[0],e[0]+' ('+e[1]+')'];}),'All mechanisms');
fillSelect(fBody,Array.from(bodyTally).sort(byCountThenAlpha).map(function(e){return [e[0],e[0]+' ('+e[1]+')';}),'All bodies & mandates');
(function(){
  var sdgSet=new Set();
  REC.forEach(function(r){(Array.isArray(r.sdgs)?r.sdgs:[]).forEach(function(n){if(n!=null)sdgSet.add(Number(n));});});
  fillSelect(fSdg,Array.from(sdgSet).sort(function(a,b){return a-b;}).map(function(n){
    var name=SDG_NAMES[String(n)]||SDG_NAMES[n];return [n,'SDG '+n+(name?' — '+name:'')];
  }),'All SDGs');
})();
(function(){
  if(minYear===null){fFrom.disabled=fTo.disabled=true;fFrom.innerHTML=fTo.innerHTML='<option value="">—</option>';return;}
  yearsAll.slice().sort(function(a,b){return a-b;}).forEach(function(y){fFrom.add(new Option(String(y),String(y)));fTo.add(new Option(String(y),String(y)));});
  fFrom.value=String(minYear);fTo.value=String(maxYear);
})();

/* ---------- filtering ---------- */
function getFiltered(){
  var q=state.q?state.q.toLowerCase():'';
  var fullRange=(state.yearFrom===minYear&&state.yearTo===maxYear);
  return REC.filter(function(r){
    if(state.mechanism&&r.mechanism!==state.mechanism)return false;
    if(state.body&&r.body!==state.body)return false;
    if(state.sdg!==''){
      var want=Number(state.sdg),list=Array.isArray(r.sdgs)?r.sdgs:[];
      if(list.indexOf(want)===-1)return false;
    }
    if(!fullRange){
      if(typeof r.year==='number'){if(r.year<state.yearFrom||r.year>state.yearTo)return false;}
      else return false; /* undated records only pass an unfiltered range */
    }
    if(state.theme){
      var th=Array.isArray(r.themes)?r.themes:[];
      if(th.indexOf(state.theme)===-1)return false;
    }
    if(q){var hay=((r.text||'')+' '+(r.symbol||'')).toLowerCase();if(hay.indexOf(q)===-1)return false;}
    return true;
  });
}
function sortList(list){
  var out=list.slice(),dateKey=function(r){return String(r.date||r.year||'');};
  if(fSort.value==='date-asc')out.sort(function(a,b){return dateKey(a).localeCompare(dateKey(b));});
  else if(fSort.value==='body')out.sort(function(a,b){return String(a.body||'').localeCompare(String(b.body||''))||dateKey(b).localeCompare(dateKey(a));});
  else out.sort(function(a,b){return dateKey(b).localeCompare(dateKey(a));});
  return out;
}

/* ---------- theme chart ---------- */
var chart=null,plainLabels=[];
var chartBox=document.querySelector('#panelOverview .chart-box'),chartEmpty=document.getElementById('chartEmpty');
if(typeof window.Chart==='undefined')chartBox.innerHTML='<div class="placeholder" style="display:block">The charts library (Chart.js) is not available in this page, so the theme chart cannot be drawn. The table below still works.</div>';
function makeChart(){
  chart=new window.Chart(document.getElementById('themeChart'),{
    type:'bar',
    data:{labels:[],datasets:[{label:'Records',data:[],backgroundColor:[],borderWidth:0,maxBarThickness:26}]},
    options:{indexAxis:'y',responsive:true,maintainAspectRatio:false,animation:false,
      scales:{x:{beginAtZero:true,ticks:{precision:0},grid:{color:'#e6ebf1'},title:{display:true,text:'Number of records',color:'#5b6b7b',font:{size:12}}},
              y:{ticks:{autoSkip:false,font:{size:13}},grid:{display:false}}},
      plugins:{legend:{display:false},tooltip:{callbacks:{label:function(c){return ' '+plural(c.parsed.x,'record');}}}},
      onClick:function(evt,els){
        if(!els.length||!plainLabels.length)return;
        var t=plainLabels[els[0].index];state.theme=(state.theme===t)?'':t;render();
      },
      onHover:function(evt,els){evt.native.target.style.cursor=els.length?'pointer':'default';}}
  });
}
function renderChart(list){
  var counts=new Map(),noTheme=0;
  list.forEach(function(r){
    var th=(Array.isArray(r.themes)?r.themes:[]).filter(Boolean);
    if(!th.length){noTheme++;return;}
    th.forEach(function(t){counts.set(t,(counts.get(t)||0)+1);});
  });
  var top=Array.from(counts).sort(byCountThenAlpha).slice(0,10);
  plainLabels=top.map(function(e){return e[0];});
  if(!top.length){
    if(typeof window.Chart!=='undefined'&&!chart)makeChart();
    if(chart){chart.data.labels=[];chart.data.datasets[0].data=[];chart.update();}
    chartBox.style.display='none';chartEmpty.style.display='block';
    chartEmpty.textContent='No themed records in the current selection — there is nothing to chart.';
  }else{
    if(typeof window.Chart!=='undefined'&&!chart)makeChart();
    if(chart){
      chart.data.labels=plainLabels.map(function(l){return wrapLabel(l,30);});
      chart.data.datasets[0].data=top.map(function(e){return e[1];});
      chart.data.datasets[0].backgroundColor=plainLabels.map(function(t){return t===state.theme?'#1f6fb2':'rgba(31,111,178,0.45)';});
      chart.update();
    }
    chartBox.style.display='block';chartEmpty.style.display='none';
  }
  var note='How this is computed: each matching record is counted once for every theme it carries, so a record with three themes appears in three bars. '+
    plural(noTheme,'matching record')+' carry no theme and cannot appear here. Top 10 themes shown; bars with the lighter shade are not selected.';
  if(state.theme)note+=' A theme filter is active (“'+state.theme+'”): click its bar again, or its chip below, to clear it.';
  else note+=' Click a bar to filter the table to that theme.';
  document.getElementById('chartNote').textContent=note;
}

/* ---------- chips ---------- */
function renderChips(){
  var chips=[];
  if(state.mechanism)chips.push(['mechanism','Mechanism: '+state.mechanism]);
  if(state.body)chips.push(['body','Body / mandate: '+state.body]);
  if(state.sdg!==''){var nm=SDG_NAMES[String(state.sdg)]||SDG_NAMES[state.sdg];chips.push(['sdg','SDG '+state.sdg+(nm?' — '+nm:'')]);}
  if(minYear!==null&&(state.yearFrom!==minYear||state.yearTo!==maxYear))chips.push(['years','Years: '+state.yearFrom+'–'+state.yearTo]);
  if(state.q)chips.push(['q','Keyword: \u201C'+state.q+'\u201D']);
  if(state.theme)chips.push(['theme','Theme: '+state.theme]);
  document.getElementById('chips').innerHTML=chips.length
    ?'<span class="lbl">Filters applied:</span>'+chips.map(function(c){return '<button type="button" class="chip" data-key="'+c[0]+'">'+esc(c[1])+'<span class="x" aria-hidden="true">&times;</span></button>';}).join('')
    :'<span class="lbl">No filters applied — showing the full dataset.</span>';
}
function clearFilter(key){
  if(key==='mechanism'){state.mechanism='';fMech.value='';}
  if(key==='body'){state.body='';fBody.value='';}
  if(key==='sdg'){state.sdg='';fSdg.value='';}
  if(key==='years'){state.yearFrom=minYear;state.yearTo=maxYear;fFrom.value=String(minYear);fTo.value=String(maxYear);}
  if(key==='q'){state.q='';fQ.value='';}
  if(key==='theme'){state.theme='';}
  render();
}
document.getElementById('chips').addEventListener('click',function(e){
  var chip=e.target.closest('.chip');if(chip)clearFilter(chip.getAttribute('data-key'));
});
document.getElementById('resetBtn').addEventListener('click',function(){['mechanism','body','sdg','years','q','theme'].forEach(clearFilter);});

/* ---------- record rows (shared by both tabs) ---------- */
function docLink(r){
  if(!r.symbol)return '—';
  return r.doc_url?'<a href="'+esc(r.doc_url)+'" target="_blank" rel="noopener">'+esc(r.symbol)+'</a>':esc(r.symbol);
}
function tags(list){return '<span class="tags">'+list.map(esc).map(function(t){return '<span class="tag">'+t+'</span>';}).join('')+'</span>';}
function detailRowHtml(r,colspan){
  var themes=(Array.isArray(r.themes)?r.themes:[]).filter(Boolean);
  var sdgs=(Array.isArray(r.sdgs)?r.sdgs:[]).filter(function(n){return n!=null;});
  var targets=(Array.isArray(r.sdg_targets)?r.sdg_targets:[]).filter(Boolean);
  var persons=(Array.isArray(r.affected_persons)?r.affected_persons:[]).filter(Boolean);
  var sdgHtml=sdgs.map(function(n){var nm=SDG_NAMES[String(n)]||SDG_NAMES[n];return '<span class="tag">SDG '+esc(n)+(nm?' · '+esc(nm):'')+'</span>';}).join(' ');
  if(sdgHtml)sdgHtml='<span class="tags">'+sdgHtml+'</span>';
  if(targets.length)sdgHtml+='<ul class="targets">'+targets.map(function(t){return '<li>'+esc(t)+'</li>';}).join('')+'</ul>';
  var details=[r.mechanism,r.type,r.section?'Section: '+r.section:null,fmtDate(r.date)].filter(Boolean).map(esc).join(' &middot; ');
  return '<tr class="detail"><td colspan="'+colspan+'">'+
    '<div class="dlabel">Full text &mdash; '+docLink(r)+'</div>'+
    '<p class="fulltext">'+(r.text?esc(r.text):'<em>No text was provided in the source data for this record.</em>')+'</p>'+
    '<div class="meta-row"><span class="mlbl">Themes</span><span>'+(themes.length?tags(themes):'—')+'</span></div>'+
    (sdgHtml?'<div class="meta-row"><span class="mlbl">SDGs &amp; targets</span><span>'+sdgHtml+'</span></div>':'')+
    (persons.length?'<div class="meta-row"><span class="mlbl">Affected persons</span><span>'+tags(persons)+'</span></div>':'')+
    '<div class="meta-row"><span class="mlbl">Details</span><span>'+(details||'—')+(r.doc_url?' &middot; <a href="'+esc(r.doc_url)+'" target="_blank" rel="noopener">Open document &nearr;</a>':'')+'</span></div></td></tr>';
}
function rowHtml(r,set,cols){
  var open=set.has(r.id),sub=[r.mechanism,r.type].filter(Boolean).join(' · ');
  return '<tr class="doc'+(open?' open':'')+'" data-id="'+esc(r.id)+'" tabindex="0" aria-expanded="'+open+'">'+
    '<td class="nowrap">'+esc(fmtDate(r.date))+'</td>'+
    (cols===3?'':'<td><strong>'+esc(r.body||'—')+'</strong>'+(sub?'<div class="sub">'+esc(sub)+'</div>':'')+'</td>')+
    '<td class="nowrap">'+docLink(r)+'</td>'+
    '<td>'+esc(firstLine(r.text))+(open?'':' <span class="hint">&#9662; full text</span>')+'</td></tr>'+
    (open?detailRowHtml(r,cols):'');
}
function makeRecordTable(tbodyId,footId,cols,emptyMsg){
  var tbody=document.getElementById(tbodyId),foot=document.getElementById(footId);
  var set=new Set(),visible=50,list=[];
  function render(){
    if(!list.length){
      tbody.innerHTML='<tr><td colspan="'+cols+'" style="padding:26px 10px;text-align:center;color:var(--muted)">'+emptyMsg+'</td></tr>';
      foot.innerHTML='';return;
    }
    var shown=list.slice(0,visible),rem=list.length-shown.length;
    tbody.innerHTML=shown.map(function(r){return rowHtml(r,set,cols);}).join('');
    foot.innerHTML='<span>Showing 1–'+shown.length+' of '+plural(list.length,'record')+'.</span>'+
      (rem>0?'<button type="button" class="btn-ghost showMore">Show 50 more ('+rem+' remaining)</button>':'');
  }
  tbody.addEventListener('click',function(e){
    if(e.target.closest('a'))return;
    var tr=e.target.closest('tr.doc');if(!tr)return;
    var id=tr.getAttribute('data-id');
    if(set.has(id))set.delete(id);else set.add(id);render();
  });
  tbody.addEventListener('keydown',function(e){
    if(e.key!=='Enter'&&e.key!==' ')return;
    var tr=e.target.closest('tr.doc');if(!tr)return;e.preventDefault();
    var id=tr.getAttribute('data-id');
    if(set.has(id))set.delete(id);else set.add(id);render();
  });
  foot.addEventListener('click',function(e){if(e.target.classList.contains('showMore')){visible+=50;render();}});
  return {set:function(l){list=l||[];visible=50;render();}};
}
var mainTable=makeRecordTable('tbody','tableFoot',4,'No records match the current filters. Try removing a filter chip above or clicking “Reset all filters”.');

function renderSummary(){
  document.getElementById('resultSummary').innerHTML='<strong>'+lastFiltered.length+'</strong> of '+REC.length+' records match the current filters.';
}
var lastFiltered=[];
function render(){
  lastFiltered=sortList(getFiltered());
  renderChips();renderSummary();renderChart(lastFiltered);mainTable.set(lastFiltered);
}

/* ---------- overview control events ---------- */
fMech.addEventListener('change',function(){state.mechanism=fMech.value;render();});
fBody.addEventListener('change',function(){state.body=fBody.value;render();});
fSdg.addEventListener('change',function(){state.sdg=fSdg.value;render();});
fSort.addEventListener('change',function(){render();});
fFrom.addEventListener('change',function(){
  if(minYear===null)return;state.yearFrom=Number(fFrom.value);
  if(state.yearFrom>state.yearTo){state.yearTo=state.yearFrom;fTo.value=fFrom.value;}
  render();
});
fTo.addEventListener('change',function(){
  if(minYear===null)return;state.yearTo=Number(fTo.value);
  if(state.yearTo<state.yearFrom){state.yearFrom=state.yearTo;fFrom.value=fTo.value;}
  render();
});
var qTimer=null;
fQ.addEventListener('input',function(){clearTimeout(qTimer);qTimer=setTimeout(function(){state.q=fQ.value.trim();render();},180);});

/* ---------- tab 2: who recommends what (UPR only) ---------- */
var uprAll=REC.filter(function(r){return r.mechanism==='Universal Periodic Review';});
var uprRecs=uprAll.filter(function(r){return !r.type||r.type==='Recommendations';});
var typeFallback=false;
if(!uprRecs.length&&uprAll.length){uprRecs=uprAll;typeFallback=true;}
var uprOther=typeFallback?0:uprAll.length-uprRecs.length;
function lastParenState(t){
  if(!t)return null;
  var m=String(t).trim().match(/\(([^()]*)\)\s*[.;,:]*\s*$/);
  if(!m)return null;
  var s=m[1].trim().replace(/[.;,:]+$/,'').trim();
  if(!s||/^[\d.,\s\/-]+$/.test(s))return null; /* purely numeric content is not a State name */
  return s;
}
var noStateRecs=[],stateMap=new Map();
uprRecs.forEach(function(r){
  var s=lastParenState(r.text);
  if(!s){noStateRecs.push(r);return;}
  if(!stateMap.has(s))stateMap.set(s,[]);
  stateMap.get(s).push(r);
});
var topStates=Array.from(stateMap).map(function(e){return [e[0],e[1].length];}).sort(byCountThenAlpha).slice(0,15);
var plainStates=topStates.map(function(e){return e[0];});
function yearSpan(list){
  var ys=list.map(function(r){return typeof r.year==='number'?r.year:null;}).filter(function(v){return v!==null;});
  if(!ys.length)return '';
  var lo=Math.min.apply(null,ys),hi=Math.max.apply(null,ys);
  return ', '+(lo===hi?String(lo):lo+'–'+hi);
}
(function(){
  document.getElementById('uprSummary').innerHTML='<strong>'+uprRecs.length+'</strong> UPR recommendations to '+esc(COUNTRY)+' (of '+REC.length+' records in this dataset).';
  var scope='Scope: this tab uses only recommendations issued under the Universal Periodic Review'+
    (typeFallback?' (all UPR paragraphs in the data, as none are labelled type “Recommendations”)':' (records with mechanism “Universal Periodic Review” and type “Recommendations”)')+
    ', addressed to '+esc(COUNTRY)+'. It ignores the filters of the first tab. The recommending State is read automatically from the parentheses at the end of each recommendation text, e.g. “(Croatia)”. '+
    plural(noStateRecs.length,'UPR recommendation')+' ('+pct(noStateRecs.length,uprRecs.length)+') had no State in parentheses and are excluded from the chart and tables below — they remain in the first tab under the UPR mechanism filter.';
  if(uprOther)scope+=' '+plural(uprOther,'UPR paragraph')+' of other types (e.g. concerns/observations) are also excluded here.';
  document.getElementById('uprScope').textContent=scope;
  if(uprRecs.length){
    document.getElementById('uprKpis').innerHTML=
      '<div class="kpi"><div class="n">'+uprRecs.length+'</div><div class="lbl">UPR recommendations</div><div class="sub">analysed on this tab</div></div>'+
      '<div class="kpi"><div class="n">'+stateMap.size+'</div><div class="lbl">Recommending States</div><div class="sub">distinct States identified</div></div>'+
      '<div class="kpi"><div class="n">'+noStateRecs.length+'</div><div class="lbl">No State in parentheses</div><div class="sub">excluded from this tab</div></div>'+
      '<div class="kpi"><div class="n">'+(yearSpan(uprRecs).slice(2)||'—')+'</div><div class="lbl">Period covered</div><div class="sub">years of the UPR recommendations</div></div>';
  }
})();

var selState='',stateChart=null;
var stateChartBox=document.getElementById('stateChart').parentNode,stateChartEmpty=document.getElementById('stateChartEmpty');
function stateColor(name){return name===selState?'#1f6fb2':'rgba(31,111,178,0.45)';}
function ensureStateChart(){
  if(stateChart||typeof window.Chart==='undefined'||!plainStates.length)return;
  stateChart=new window.Chart(document.getElementById('stateChart'),{
    type:'bar',
    data:{labels:plainStates.map(function(l){return wrapLabel(l,28);}),
      datasets:[{label:'Recommendations',data:topStates.map(function(e){return e[1];}),backgroundColor:plainStates.map(stateColor),borderWidth:0,maxBarThickness:26}]},
    options:{indexAxis:'y',responsive:true,maintainAspectRatio:false,animation:false,
      scales:{x:{beginAtZero:true,ticks:{precision:0},grid:{color:'#e6ebf1'},title:{display:true,text:'Number of UPR recommendations',color:'#5b6b7b',font:{size:12}}},
              y:{ticks:{autoSkip:false,font:{size:13}},grid:{display:false}}},
      plugins:{legend:{display:false},tooltip:{callbacks:{label:function(c){return ' '+plural(c.parsed.x,'recommendation');}}}},
      onClick:function(evt,els){if(els.length)selectState(plainStates[els[0].index]);},
      onHover:function(evt,els){evt.native.target.style.cursor=els.length?'pointer':'default';}}
  });
}
function renderStateChart(){
  document.getElementById('stateChartNote').textContent='How this is computed: bars count the UPR recommendations whose closing parentheses name that State — counted directly from the data, not estimated. '+
    stateMap.size+' distinct States were identified; the 15 with the most recommendations are shown. Click a bar to list that State’s recommendations below, click it again (or use “Clear selection”) to reset. The '+
    noStateRecs.length+' recommendations without a State in parentheses are not counted here.';
  if(typeof window.Chart==='undefined'){
    stateChartBox.innerHTML='<div class="placeholder" style="display:block">Chart.js is not available, so this chart cannot be drawn. The tables below still work.</div>';
    stateChartEmpty.style.display='none';return;
  }
  if(!topStates.length){
    if(stateChart){stateChart.data.labels=[];stateChart.data.datasets[0].data=[];stateChart.update();}
    stateChartBox.style.display='none';stateChartEmpty.style.display='block';
    stateChartEmpty.textContent=uprRecs.length?'No recommending State could be identified in any UPR recommendation, so there is nothing to chart.':'There are no UPR recommendations in this dataset.';
    return;
  }
  stateChartBox.style.display='block';stateChartEmpty.style.display='none';
  if(stateChart){
    stateChart.data.labels=plainStates.map(function(l){return wrapLabel(l,28);});
    stateChart.data.datasets[0].data=topStates.map(function(e){return e[1];});
    stateChart.data.datasets[0].backgroundColor=plainStates.map(stateColor);
    stateChart.update();
  }
}
var sdgBody=document.getElementById('sdgBody');
function renderSdgTable(){
  if(!topStates.length){
    sdgBody.innerHTML='<tr><td colspan="3" style="padding:22px 10px;text-align:center;color:var(--muted)">No recommending States to show.</td></tr>';
    return;
  }
  sdgBody.innerHTML=topStates.map(function(e){
    var name=e[0],recs=stateMap.get(name),sd=topSdgs(recs,3);
    var sdHtml=sd.length?sd.map(function(p){
      var nm=SDG_NAMES[String(p[0])]||SDG_NAMES[p[0]];
      return '<span class="tag">SDG '+p[0]+(nm?' · '+esc(nm):'')+' — '+p[1]+'</span>';
    }).join(' '):'<span style="color:var(--muted)">no SDGs cited</span>';
    return '<tr class="pick'+(name===selState?' sel':'')+'" data-state="'+esc(name)+'" tabindex="0">'+
      '<td><strong>'+esc(name)+'</strong></td><td class="nowrap">'+recs.length+'</td><td>'+sdHtml+'</td></tr>';
  }).join('');
}
sdgBody.addEventListener('click',function(e){
  var tr=e.target.closest('tr.pick');if(tr)selectState(tr.getAttribute('data-state'));
});
sdgBody.addEventListener('keydown',function(e){
  if(e.key!=='Enter'&&e.key!==' ')return;
  var tr=e.target.closest('tr.pick');if(!tr)return;e.preventDefault();selectState(tr.getAttribute('data-state'));
});
var stateTable=makeRecordTable('stateTbody','stateFoot',3,'This State has no recommendations to list.');
var clearStateBtn=document.getElementById('clearStateBtn'),stateTableWrap=document.getElementById('stateTableWrap');
var stateDetailEmpty=document.getElementById('stateDetailEmpty'),stateDetailTitle=document.getElementById('stateDetailTitle');
var stateDetailSummary=document.getElementById('stateDetailSummary'),stateFoot=document.getElementById('stateFoot');
function selectState(name){
  selState=(selState===name)?'':name;
  renderStates();
  if(selState&&stateTableWrap.scrollIntoView)stateTableWrap.scrollIntoView({block:'start'});
}
clearStateBtn.addEventListener('click',function(){selState='';renderStates();});
function renderStates(){
  renderStateChart();renderSdgTable();
  clearStateBtn.hidden=!selState;
  if(selState){
    var recs=(stateMap.get(selState)||[]).slice().sort(function(a,b){return String(b.date||b.year||'').localeCompare(String(a.date||a.year||''));});
    stateDetailTitle.textContent='Recommendations from '+selState;
    stateDetailSummary.innerHTML='<strong>'+recs.length+'</strong> UPR recommendations from '+esc(selState)+' to '+esc(COUNTRY)+
      yearSpan(recs)+' — '+pct(recs.length,uprRecs.length)+' of all UPR recommendations in this dataset.';
    stateDetailEmpty.style.display='none';stateTableWrap.style.display='block';stateFoot.style.display='flex';
    stateTable.set(recs);
  }else{
    stateDetailTitle.textContent='Recommendations by State';
    stateDetailSummary.textContent='Select a State to list its recommendations.';
    stateDetailEmpty.textContent=topStates.length?'Select a State — click a bar in the chart above or a row in the SDG table — to list its recommendations.':'Nothing to show: no recommending States could be identified in the UPR recommendations.';
    stateDetailEmpty.style.display='block';stateTableWrap.style.display='none';stateFoot.style.display='none';
    stateTable.set([]);
  }
}

render();
renderStates();
})();
</script>
</body>
</html>
```