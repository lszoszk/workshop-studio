I added a second tab, "Who recommends what", next to the existing overview. It parses the recommending State from the closing parentheses of each UPR recommendation, charts the top 15 States, shows a table of the SDGs each raises most, and lets you click a State (bar or row) to list its recommendations with linked symbols — plus an explicit count of UPR recommendations with no State in parentheses.

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>UN human rights recommendations dashboard</title>
<style>
:root{--accent:#1f6fb2;--accent-dark:#17517f;--ink:#1d2833;--muted:#5c6b7a;--bg:#f4f6f9;--card:#ffffff;--line:#dce3ec;--soft:#eaf2fa;}
*{box-sizing:border-box}
[hidden]{display:none!important}
html,body{margin:0;padding:0}
body{font:16px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif;background:var(--bg);color:var(--ink)}
.wrap{max-width:1140px;margin:0 auto;padding:28px 20px 64px}
header.masthead{background:var(--card);border:1px solid var(--line);border-left:6px solid var(--accent);border-radius:10px;padding:20px 24px;margin-bottom:20px}
h1{font-size:1.55rem;margin:0 0 8px;line-height:1.25}
.sub{color:var(--ink);margin:0 0 6px;font-weight:600}
.note{font-size:.9rem;color:var(--muted);margin:6px 0 0}
.tabs{display:flex;gap:8px;margin-bottom:20px;flex-wrap:wrap}
.tab{font:inherit;font-weight:600;padding:9px 18px;border-radius:8px;border:1px solid var(--line);background:#fff;color:var(--ink);cursor:pointer}
.tab.active{background:var(--accent);border-color:var(--accent);color:#fff}
.card{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:18px 20px;margin-bottom:20px}
h2{font-size:1.15rem;margin:0 0 10px}
.filters{display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:14px;align-items:end}
.field label{display:block;font-size:.78rem;font-weight:700;letter-spacing:.05em;text-transform:uppercase;color:var(--muted);margin-bottom:5px}
.field select,.field input{width:100%;padding:8px 10px;border:1px solid var(--line);border-radius:7px;font:inherit;background:#fff;color:var(--ink)}
.field select:focus,.field input:focus{outline:2px solid var(--accent);outline-offset:1px}
button{font:inherit;padding:8px 14px;border-radius:7px;border:1px solid var(--accent);background:var(--accent);color:#fff;cursor:pointer}
button.ghost{background:#fff;color:var(--accent-dark)}
button:hover{filter:brightness(1.06)}
.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:14px;margin-bottom:20px}
.stat{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:14px 18px}
.stat .k{font-size:.78rem;text-transform:uppercase;letter-spacing:.05em;color:var(--muted);font-weight:700}
.stat .v{font-size:1.55rem;font-weight:700;color:var(--accent-dark);margin:2px 0}
.stat .s{font-size:.88rem;color:var(--muted)}
.chips{margin-top:6px}
.chip{display:inline-block;background:var(--soft);color:var(--accent-dark);border-radius:999px;padding:2px 10px;font-size:.82rem;margin:2px 4px 2px 0}
.chartbox{position:relative;width:100%}
table{width:100%;border-collapse:collapse;font-size:.95rem}
th{text-align:left;font-size:.76rem;text-transform:uppercase;letter-spacing:.05em;color:var(--muted);border-bottom:2px solid var(--line);padding:8px 10px;vertical-align:bottom}
td{padding:9px 10px;border-bottom:1px solid var(--line);vertical-align:top;word-break:break-word}
col.c-date{width:92px}col.c-mech{width:145px}col.c-body{width:110px}col.c-sym{width:175px}
tr.data-row{cursor:pointer}
tr.data-row:hover,tr.data-row.open{background:var(--soft)}
tr.sel-row{cursor:pointer}
tr.sel-row:hover{background:var(--soft)}
tr.sel-row.selected{background:var(--soft);box-shadow:inset 3px 0 0 var(--accent)}
td.txt{color:#33414f}
tr.detail td{background:#f8fafd}
.fulltext{white-space:pre-wrap;background:#fff;border:1px solid var(--line);border-radius:8px;padding:12px 14px;margin:4px 0 10px;font-size:.95rem}
.meta{font-size:.88rem;color:var(--muted);margin:5px 0}
.meta b{color:var(--ink)}
a{color:var(--accent)}
.nowrap{white-space:nowrap}
.muted{color:var(--muted);font-weight:400}
.rec{border:1px solid var(--line);border-radius:8px;margin-bottom:8px;background:#fff}
.rec-head{padding:9px 12px;cursor:pointer;display:flex;gap:10px;flex-wrap:wrap;align-items:baseline}
.rec-head:hover{background:var(--soft)}
.rec-head .sym{font-weight:700;white-space:nowrap}
.rec-head .line{color:#33414f;flex:1;min-width:240px}
.rec-body{border-top:1px solid var(--line);padding:10px 12px;background:#f8fafd}
footer{margin-top:26px;font-size:.85rem;color:var(--muted)}
</style>
</head>
<body>
<div class="wrap">

<header class="masthead">
  <h1 id="title">UN human rights recommendations &amp; observations</h1>
  <p class="sub" id="desc"></p>
  <p class="note" id="howTop"></p>
</header>

<nav class="tabs" aria-label="Views">
  <button id="tabDash" class="tab active" type="button">Overview</button>
  <button id="tabWho" class="tab" type="button">Who recommends what</button>
</nav>

<div id="paneDash">

<section class="card" aria-label="Filters">
  <h2>Filters</h2>
  <div class="filters">
    <div class="field"><label for="fMech">Mechanism</label><select id="fMech"></select></div>
    <div class="field"><label for="fBody">Treaty body / mandate</label><select id="fBody"></select></div>
    <div class="field"><label for="fY0">From year</label><select id="fY0"></select></div>
    <div class="field"><label for="fY1">To year</label><select id="fY1"></select></div>
    <div class="field"><label for="fSdg">SDG</label><select id="fSdg"></select></div>
    <div class="field"><label for="fQ">Keyword search</label><input id="fQ" type="search" placeholder="e.g. education, torture, women…"></div>
    <div class="field"><button id="fReset" class="ghost" type="button">Reset filters</button></div>
  </div>
</section>

<section class="stats" id="stats" aria-label="Counts"></section>

<section class="card">
  <h2>Most frequent themes <span class="muted" id="chartCount"></span></h2>
  <p class="note">How this is computed: a record can carry several theme tags and counts once in each theme it carries. The chart shows the 10 most frequent themes among the records matching the current filters. Counts are exact, computed in your browser from the loaded records — not estimated.</p>
  <div class="chartbox" id="chartBox"><canvas id="themeChart"></canvas></div>
  <p class="note" id="chartEmpty" hidden>No theme tags on the records matching the current filters.</p>
</section>

<section class="card">
  <h2>Matching records <span class="muted" id="tblCount"></span></h2>
  <p class="note">Each row shows the date, mechanism, issuing body, the document symbol (the link opens the UN document in a new tab) and the first line of the paragraph. Click a row (or press Enter on it) to read the full text, themes, SDGs and affected groups. Sorted by date, newest first.</p>
  <table>
    <colgroup><col class="c-date"><col class="c-mech"><col class="c-body"><col class="c-sym"><col></colgroup>
    <thead><tr><th>Date</th><th>Mechanism</th><th>Body</th><th>Symbol</th><th>Text (first line)</th></tr></thead>
    <tbody id="tbody"></tbody>
  </table>
  <p class="note" id="tblEmpty" hidden>No records match the current filters — try widening the year range or clearing the keyword.</p>
  <div style="margin-top:12px"><button id="fMore" class="ghost" type="button" hidden></button></div>
</section>

</div><!-- /paneDash -->

<div id="paneWho" hidden>

<section class="stats" id="whoStats" aria-label="UPR counts"></section>

<section class="card">
  <h2>States making the most UPR recommendations to <span id="whoCountry"></span></h2>
  <p class="note">How this is computed: only records with mechanism “Universal Periodic Review” are considered. The recommending State is read from the last parentheses at the end of the recommendation text (e.g. “…for all children (Croatia).”). The chart shows the 15 States with the most recommendations; ties are broken alphabetically. All counts are exact and computed in your browser — not estimated. Click a bar to list that State’s recommendations below.</p>
  <div class="chartbox" id="whoChartBox"><canvas id="whoChart"></canvas></div>
  <p class="note" id="whoChartEmpty" hidden>No UPR recommendations with a recommending State were found in the data.</p>
</section>

<section class="card">
  <h2>SDGs each of the top States raises most</h2>
  <p class="note">For each of the States shown in the chart, the three SDGs most often tagged on that State’s recommendations, with the number of its recommendations carrying that SDG. A recommendation can carry several SDGs and counts once per SDG. Click a row to list that State’s recommendations below.</p>
  <table id="whoTable">
    <thead><tr><th>Recommending State</th><th>Recommendations</th><th>SDGs raised most (top 3, with counts)</th></tr></thead>
    <tbody id="whoTbody"></tbody>
  </table>
  <p class="note" id="whoTblEmpty" hidden>No States to show.</p>
</section>

<section class="card" id="whoDetailCard">
  <h2 id="whoDetailTitle">Recommendations by a State</h2>
  <p class="note" id="whoDetailNote">Click a State in the chart or the table above to list its recommendations here. Each entry shows the document symbol (linked to the UN document in a new tab), date and first line; click an entry to read the full text.</p>
  <div id="whoList"></div>
</section>

</div><!-- /paneWho -->

<footer>Workshop dashboard · Data: <code>window.WORKSHOP_DATA.uhri</code> · All filtering, counting and charting happens locally in your browser; no data leaves this page.</footer>
<div id="fatal" class="card" hidden></div>

</div>

<script>
(function(){
"use strict";
function esc(s){return String(s==null?"":s).replace(/[&<>"']/g,function(c){return{"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c];});}

var root=window.WORKSHOP_DATA;
if(!root||!root.uhri||!Array.isArray(root.uhri.records)){
  var f=document.getElementById('fatal');
  f.hidden=false;
  f.textContent='The workshop data (window.WORKSHOP_DATA.uhri) is missing or has no records, so this dashboard cannot be built.';
  return;
}
var D=root.uhri;
var records=D.records;
var country=D.country||'the reviewed State';
var sdgNames=D.sdg_names||{};

document.title='UN human rights recommendations to '+country+' — dashboard';
document.getElementById('title').textContent='UN human rights recommendations & observations addressed to '+country;
document.getElementById('whoCountry').textContent=country;

var years=[];
records.forEach(function(r){if(typeof r.year==='number'&&years.indexOf(r.year)===-1)years.push(r.year);});
years.sort(function(a,b){return a-b;});
var yMin=years.length?years[0]:null, yMax=years.length?years[years.length-1]:null;
var loaded=records.length;
var countTxt=(typeof D.count==='number'&&D.count!==loaded)?(D.count+' records in the source file, '+loaded+' loaded here'):(loaded+' records');
var src=D.source||'OHCHR Universal Human Rights Index (UHRI)';
document.getElementById('desc').textContent='Source: '+src+' — '+countTxt+' addressed to '+country+', covering '+(yMin!=null?(yMin+'–'+yMax):'no dated records')+(D.built?', data built '+D.built:'')+'.';
document.getElementById('howTop').textContent='How this is computed: every count, filter, chart and table on this page is calculated in your browser from the loaded records; nothing is estimated.';

function uniq(key){var s=[];records.forEach(function(r){var v=r[key];if(v!=null&&v!==''&&s.indexOf(v)===-1)s.push(v);});return s.sort();}
var mechanisms=uniq('mechanism');
var bodies=uniq('body');
var sdgSet=[];
records.forEach(function(r){(r.sdgs||[]).forEach(function(s){if(sdgSet.indexOf(s)===-1)sdgSet.push(s);});});
sdgSet.sort(function(a,b){return Number(a)-Number(b);});

function fill(sel,items,labelFn,allLabel){
  sel.innerHTML='';
  var o=document.createElement('option');o.value='all';o.textContent=allLabel;sel.appendChild(o);
  items.forEach(function(it){var op=document.createElement('option');op.value=String(it);op.textContent=labelFn?labelFn(it):String(it);sel.appendChild(op);});
}
var fMech=document.getElementById('fMech'),fBody=document.getElementById('fBody'),
    fY0=document.getElementById('fY0'),fY1=document.getElementById('fY1'),
    fSdg=document.getElementById('fSdg'),fQ=document.getElementById('fQ');
fill(fMech,mechanisms,null,'All mechanisms');
fill(fBody,bodies,null,'All bodies / mandates');
fill(fSdg,sdgSet,function(s){return 'SDG '+s+(sdgNames[String(s)]?' — '+sdgNames[String(s)]:'');},'All SDGs');
if(years.length){
  fill(fY0,years,null,'Earliest year');
  fill(fY1,years,null,'Latest year');
  fY0.value=String(yMin);fY1.value=String(yMax);
}else{
  [fY0,fY1].forEach(function(sel){sel.innerHTML='<option value="">no years in data</option>';sel.disabled=true;});
}

var state={mechanism:'all',body:'all',y0:yMin,y1:yMax,sdg:'all',q:''};
var current=[],chart=null,showAll=false,PAGE=150;

function filtered(){
  var q=state.q.trim().toLowerCase();
  return records.filter(function(r){
    if(state.mechanism!=='all'&&r.mechanism!==state.mechanism)return false;
    if(state.body!=='all'&&r.body!==state.body)return false;
    if(yMin!=null){
      if(typeof r.year==='number'){if(r.year<state.y0||r.year>state.y1)return false;}
      else if(state.y0!==yMin||state.y1!==yMax)return false;
    }
    if(state.sdg!=='all'){var arr=(r.sdgs||[]).map(Number);if(arr.indexOf(Number(state.sdg))===-1)return false;}
    if(q){
      var hay=[r.text,r.symbol,r.section,r.body,r.type,r.mechanism,
        (r.themes||[]).join(' '),(r.affected_persons||[]).join(' '),
        (r.sdg_targets||[]).join(' '),(r.countries||[]).join(' ')].join(' ').toLowerCase();
      if(hay.indexOf(q)===-1)return false;
    }
    return true;
  }).sort(function(a,b){
    var da=a.date||'',db=b.date||'';
    if(da!==db)return da<db?1:-1;
    var ya=a.year||0,yb=b.year||0;if(ya!==yb)return yb-ya;
    return String(a.symbol||'').localeCompare(String(b.symbol||''));
  });
}

function statHtml(k,v,s){return '<div class="stat"><div class="k">'+esc(k)+'</div><div class="v">'+esc(v)+'</div><div class="s">'+esc(s)+'</div></div>';}
function renderStats(list){
  var fy=list.map(function(r){return r.year;}).filter(function(y){return typeof y==='number';});
  var fmin=fy.length?Math.min.apply(null,fy):null,fmax=fy.length?Math.max.apply(null,fy):null;
  var mech={};
  list.forEach(function(r){var m=r.mechanism||'Unspecified';mech[m]=(mech[m]||0)+1;});
  var chips=Object.keys(mech).sort().map(function(m){return '<span class="chip">'+esc(m)+': '+mech[m]+'</span>';}).join('');
  document.getElementById('stats').innerHTML=
    statHtml('Records in dataset',String(loaded),yMin!=null?('Years '+yMin+'–'+yMax):'no dated records')+
    statHtml('Matching current filters',String(list.length),(fmin!=null?('Years '+fmin+'–'+fmax):'no dated records in selection'))+
    '<div class="stat"><div class="k">By mechanism (current filters)</div><div class="chips">'+(chips||'<span class="muted">none</span>')+'</div></div>';
}

function renderChart(list){
  var counts={};
  list.forEach(function(r){(r.themes||[]).forEach(function(t){counts[t]=(counts[t]||0)+1;});});
  var keys=Object.keys(counts);
  var top=keys.map(function(k){return[k,counts[k]];}).sort(function(a,b){return b[1]-a[1]||a[0].localeCompare(b[0]);}).slice(0,10);
  document.getElementById('chartCount').textContent='— top '+top.length+' of '+keys.length+' themes across '+list.length+' matching records';
  if(chart){chart.destroy();chart=null;}
  var box=document.getElementById('chartBox'),empty=document.getElementById('chartEmpty');
  if(!top.length){box.hidden=true;empty.hidden=false;return;}
  empty.hidden=true;box.hidden=false;
  box.style.height=Math.max(220,top.length*38+50)+'px';
  var ctx=document.getElementById('themeChart').getContext('2d');
  chart=new Chart(ctx,{
    type:'bar',
    data:{labels:top.map(function(t){return t[0];}),datasets:[{label:'Records',data:top.map(function(t){return t[1];}),backgroundColor:'#1f6fb2',borderRadius:4}]},
    options:{indexAxis:'y',responsive:true,maintainAspectRatio:false,
      plugins:{legend:{display:false},tooltip:{callbacks:{label:function(c){return ' '+c.parsed.x+' record'+(c.parsed.x===1?'':'s');}}}},
      scales:{x:{beginAtZero:true,ticks:{precision:0},title:{display:true,text:'Number of matching records'}},y:{ticks:{autoSkip:false}}}}
  });
}

function firstLine(t){
  t=String(t==null?'':t).trim();if(!t)return'—';
  var nl=t.split('\n')[0].trim(),base=nl||t;
  return base.length>240?base.slice(0,240).replace(/\s+\S*$/,'')+' …':base;
}
function sdgLabel(s){return 'SDG '+s+(sdgNames[String(s)]?' — '+sdgNames[String(s)]:'');}
function recommenderOf(r){
  var t=String(r.text||'').replace(/\s+$/,'');
  var m=t.match(/\(([^()]+)\)\s*\.?\s*$/);
  if(!m)return null;
  var s=m[1].trim().replace(/\.+$/,'').trim();
  return s||null;
}
function detailHtml(r){
  var rec=recommenderOf(r),h='';
  h+='<div class="fulltext">'+esc(r.text||'(no text available)')+'</div>';
  h+='<div class="meta"><b>Type:</b> '+esc(r.type||'—')+(r.section?' &nbsp;·&nbsp; <b>Section:</b> '+esc(r.section):'')+(r.date?' &nbsp;·&nbsp; <b>Date:</b> '+esc(r.date):'')+' &nbsp;·&nbsp; <b>Document:</b> '+(r.doc_url?'<a href="'+esc(r.doc_url)+'" target="_blank" rel="noopener">'+esc(r.symbol||r.doc_url)+'</a>':esc(r.symbol||'—'))+'</div>';
  if(rec)h+='<div class="meta"><b>Recommended by:</b> '+esc(rec)+' (read from the last parentheses at the end of the text)</div>';
  if(r.themes&&r.themes.length)h+='<div class="meta"><b>Themes:</b> '+r.themes.map(function(t){return '<span class="chip">'+esc(t)+'</span>';}).join('')+'</div>';
  if(r.sdgs&&r.sdgs.length)h+='<div class="meta"><b>SDGs:</b> '+r.sdgs.map(function(s){return '<span class="chip">'+esc(sdgLabel(s))+'</span>';}).join('')+'</div>';
  if(r.sdg_targets&&r.sdg_targets.length)h+='<div class="meta"><b>SDG targets:</b> '+esc(r.sdg_targets.join('; '))+'</div>';
  if(r.affected_persons&&r.affected_persons.length)h+='<div class="meta"><b>Affected persons/groups:</b> '+r.affected_persons.map(function(t){return '<span class="chip">'+esc(t)+'</span>';}).join('')+'</div>';
  return h;
}
function paintTable(){
  var list=current,shown=showAll?list:list.slice(0,PAGE);
  document.getElementById('tblCount').textContent='— '+list.length+' of '+loaded+' records';
  document.getElementById('tblEmpty').hidden=list.length>0;
  document.getElementById('tbody').innerHTML=shown.map(function(r,i){
    var sym=r.symbol?('<a href="'+esc(r.doc_url||'#')+'" target="_blank" rel="noopener">'+esc(r.symbol)+'</a>'):'—';
    return '<tr class="data-row" data-i="'+i+'" tabindex="0" aria-expanded="false">'+
      '<td class="nowrap">'+esc(r.date||(r.year||''))+'</td>'+
      '<td>'+esc(r.mechanism||'')+'</td>'+
      '<td>'+esc(r.body||'')+'</td>'+
      '<td>'+sym+'</td>'+
      '<td class="txt">'+esc(firstLine(r.text))+'</td></tr>'+
      '<tr class="detail" hidden><td colspan="5">'+detailHtml(r)+'</td></tr>';
  }).join('');
  var btn=document.getElementById('fMore');
  if(list.length>PAGE){btn.hidden=false;btn.textContent=showAll?('Show fewer (first '+PAGE+' of '+list.length+')'):('Show all '+list.length+' records');}
  else btn.hidden=true;
}
function render(){current=filtered();renderStats(current);renderChart(current);showAll=false;paintTable();}

fMech.addEventListener('change',function(){state.mechanism=this.value;render();});
fBody.addEventListener('change',function(){state.body=this.value;render();});
fSdg.addEventListener('change',function(){state.sdg=this.value;render();});
fY0.addEventListener('change',function(){state.y0=Number(this.value);if(state.y0>state.y1){state.y1=state.y0;fY1.value=String(state.y1);}render();});
fY1.addEventListener('change',function(){state.y1=Number(this.value);if(state.y1<state.y0){state.y0=state.y1;fY0.value=String(state.y0);}render();});
var deb;
fQ.addEventListener('input',function(){var v=this.value;clearTimeout(deb);deb=setTimeout(function(){state.q=v;render();},180);});
document.getElementById('fReset').addEventListener('click',function(){
  state={mechanism:'all',body:'all',y0:yMin,y1:yMax,sdg:'all',q:''};
  fMech.value='all';fBody.value='all';fSdg.value='all';fQ.value='';
  if(years.length){fY0.value=String(yMin);fY1.value=String(yMax);}
  render();
});
document.getElementById('fMore').addEventListener('click',function(){showAll=!showAll;paintTable();});

function toggleRow(tr){
  var det=tr.nextElementSibling,open=tr.classList.toggle('open');
  if(det)det.hidden=!open;
  tr.setAttribute('aria-expanded',open?'true':'false');
}
document.getElementById('tbody').addEventListener('click',function(e){
  if(e.target.closest('a'))return;
  var tr=e.target.closest('tr.data-row');if(tr)toggleRow(tr);
});
document.getElementById('tbody').addEventListener('keydown',function(e){
  if(e.key!=='Enter'&&e.key!==' ')return;
  var tr=e.target.closest('tr.data-row');if(tr){e.preventDefault();toggleRow(tr);}
});

/* ---------- Tab: Who recommends what ---------- */
var who={upr:[],byState:{},states:[],top15:[],noState:0,selected:null,chart:null,built:false};
var paneDash=document.getElementById('paneDash'),paneWho=document.getElementById('paneWho');
var tabDash=document.getElementById('tabDash'),tabWho=document.getElementById('tabWho');

function buildWho(){
  who.upr=records.filter(function(r){
    return r.mechanism==='Universal Periodic Review'&&(!r.type||/recommend/i.test(r.type));
  });
  who.byState={};who.noState=0;
  who.upr.forEach(function(r){
    var s=recommenderOf(r);
    if(s){(who.byState[s]=who.byState[s]||[]).push(r);}else who.noState++;
  });
  who.states=Object.keys(who.byState).map(function(k){return{k:k,n:who.byState[k].length};})
    .sort(function(a,b){return b.n-a.n||a.k.localeCompare(b.k);});
  who.top15=who.states.slice(0,15);
  who.built=true;
}
function topSdgs(list){
  var c={};
  list.forEach(function(r){(r.sdgs||[]).forEach(function(s){c[s]=(c[s]||0)+1;});});
  return Object.keys(c).map(function(k){return[k,c[k]];})
    .sort(function(a,b){return b[1]-a[1]||Number(a[0])-Number(b[0]);}).slice(0,3);
}
function renderWho(){
  if(!who.built)buildWho();
  var withState=who.upr.length-who.noState;
  document.getElementById('whoStats').innerHTML=
    statHtml('UPR recommendations to '+country,String(who.upr.length),'mechanism = Universal Periodic Review, type = Recommendations')+
    statHtml('With a recommending State in parentheses',String(withState),'read from the last parentheses at the end of the text')+
    statHtml('UPR recommendations with no State in parentheses',String(who.noState),(who.noState>0?'these are excluded from the chart and table below':'none — every UPR recommendation names a State'))+
    statHtml('Distinct recommending States',String(who.states.length),'top 15 shown in the chart and table');
  // chart
  if(who.chart){who.chart.destroy();who.chart=null;}
  var box=document.getElementById('whoChartBox'),empty=document.getElementById('whoChartEmpty');
  if(!who.top15.length){box.hidden=true;empty.hidden=false;}
  else{
    empty.hidden=true;box.hidden=false;
    box.style.height=Math.max(240,who.top15.length*36+50)+'px';
    var ctx=document.getElementById('whoChart').getContext('2d');
    who.chart=new Chart(ctx,{
      type:'bar',
      data:{labels:who.top15.map(function(s){return s.k;}),datasets:[{label:'UPR recommendations',data:who.top15.map(function(s){return s.n;}),backgroundColor:'#1f6fb2',borderRadius:4}]},
      options:{indexAxis:'y',responsive:true,maintainAspectRatio:false,
        onClick:function(evt,els){
          if(els&&els.length){selectState(who.top15[els[0].index].k);}
        },
        plugins:{legend:{display:false},tooltip:{callbacks:{label:function(c){return ' '+c.parsed.x+' recommendation'+(c.parsed.x===1?'':'s')+' — click to list them';}}}},
        scales:{x:{beginAtZero:true,ticks:{precision:0},title:{display:true,text:'Number of UPR recommendations to '+country}},y:{ticks:{autoSkip:false}}}}
    });
  }
  // SDG table
  var tb=document.getElementById('whoTbody');
  document.getElementById('whoTblEmpty').hidden=who.top15.length>0;
  tb.innerHTML=who.top15.map(function(s,i){
    var tops=topSdgs(who.byState[s.k]);
    var chips=tops.length?tops.map(function(t){
      return '<span class="chip" title="'+esc(sdgNames[String(t[0])]||'')+'">SDG '+esc(t[0])+' ('+t[1]+')</span>';
    }).join(''):'<span class="muted">no SDG tags</span>';
    return '<tr class="sel-row'+(who.selected===s.k?' selected':'')+'" data-k="'+esc(s.k)+'" tabindex="0">'+
      '<td><b>'+esc(s.k)+'</b></td><td>'+s.n+'</td><td>'+chips+'</td></tr>';
  }).join('');
  renderWhoList();
}
function selectState(k){
  who.selected=(who.selected===k)?null:k;
  renderWho();
  if(who.selected){
    document.getElementById('whoDetailCard').scrollIntoView({block:'start'});
  }
}
function renderWhoList(){
  var title=document.getElementById('whoDetailTitle'),note=document.getElementById('whoDetailNote'),list=document.getElementById('whoList');
  var k=who.selected;
  if(!k){
    title.textContent='Recommendations by a State';
    note.textContent='Click a State in the chart or the table above to list its recommendations here. Each entry shows the document symbol (linked to the UN document in a new tab), date and first line; click an entry to read the full text.';
    list.innerHTML='';return;
  }
  var recs=who.byState[k].slice().sort(function(a,b){
    var da=a.date||'',db=b.date||'';if(da!==db)return da<db?1:-1;
    return String(a.symbol||'').localeCompare(String(b.symbol||''));
  });
  title.textContent='Recommendations by '+k+' ('+recs.length+')';
  note.textContent='All '+recs.length+' UPR recommendations to '+country+' whose text ends with “('+k+')”. Sorted by date, newest first. Click an entry to read the full paragraph.';
  list.innerHTML=recs.map(function(r,i){
    var sym=r.symbol?('<a href="'+esc(r.doc_url||'#')+'" target="_blank" rel="noopener">'+esc(r.symbol)+'</a>'):'—';
    return '<div class="rec"><div class="rec-head" data-i="'+i+'" tabindex="0" role="button" aria-expanded="false">'+
      '<span class="sym">'+sym+'</span>'+
      '<span class="muted nowrap">'+esc(r.date||(r.year||''))+(r.body?' · '+esc(r.body):'')+'</span>'+
      '<span class="line">'+esc(firstLine(r.text))+'</span></div>'+
      '<div class="rec-body" hidden>'+detailHtml(r)+'</div></div>';
  }).join('');
}
document.getElementById('whoTbody').addEventListener('click',function(e){
  var tr=e.target.closest('tr.sel-row');if(tr)selectState(tr.getAttribute('data-k'));
});
document.getElementById('whoTbody').addEventListener('keydown',function(e){
  if(e.key!=='Enter'&&e.key!==' ')return;
  var tr=e.target.closest('tr.sel-row');if(tr){e.preventDefault();selectState(tr.getAttribute('data-k'));}
});
document.getElementById('whoList').addEventListener('click',function(e){
  if(e.target.closest('a'))return;
  var h=e.target.closest('.rec-head');if(!h)return;
  var body=h.nextElementSibling,open=body.hidden;
  body.hidden=!open;h.setAttribute('aria-expanded',open?'true':'false');
});
document.getElementById('whoList').addEventListener('keydown',function(e){
  if(e.key!=='Enter'&&e.key!==' ')return;
  var h=e.target.closest('.rec-head');if(!h)return;
  e.preventDefault();
  var body=h.nextElementSibling,open=body.hidden;
  body.hidden=!open;h.setAttribute('aria-expanded',open?'true':'false');
});

function showTab(which){
  var dash=which==='dash';
  paneDash.hidden=!dash;
  paneWho.hidden=dash;
  tabDash.classList.toggle('active',dash);
  tabWho.classList.toggle('active',!dash);
  if(!dash)renderWho();
}
tabDash.addEventListener('click',function(){showTab('dash');});
tabWho.addEventListener('click',function(){showTab('who');});

render();
})();
</script>
</body>
</html>
```