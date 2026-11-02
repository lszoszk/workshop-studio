I added a "Spot-check: 10 random records" section to the dashboard: it draws 10 random records from the current filter result, shows each full paragraph with its UN-index SDGs for you to mark right / wrong / arguable, then computes the agreement rate locally, lists the wrong and arguable examples, and offers a CSV download of the 10 records with your marks; "Draw again" re-rolls the sample.

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
.card{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:18px 20px;margin-bottom:20px}
h2{font-size:1.15rem;margin:0 0 10px}
h3{font-size:1rem;margin:14px 0 4px}
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
td.txt{color:#33414f}
tr.detail td{background:#f8fafd}
.fulltext{white-space:pre-wrap;background:#fff;border:1px solid var(--line);border-radius:8px;padding:12px 14px;margin:4px 0 10px;font-size:.95rem}
.meta{font-size:.88rem;color:var(--muted);margin:5px 0}
.meta b{color:var(--ink)}
a{color:var(--accent)}
.nowrap{white-space:nowrap}
.muted{color:var(--muted);font-weight:400}
.btnrow{display:flex;gap:10px;flex-wrap:wrap;margin:10px 0 4px}
.draw-card{border:1px solid var(--line);border-radius:8px;background:#fbfcfe;padding:14px 16px;margin:12px 0}
.draw-head{font-size:.92rem;color:var(--muted);margin-bottom:8px}
.draw-head b{color:var(--ink)}
.sdg-item{display:flex;flex-wrap:wrap;align-items:center;gap:6px;margin:6px 0}
.sdg-label{background:var(--soft);color:var(--accent-dark);border-radius:999px;padding:2px 10px;font-size:.85rem}
button.mk{font-size:.8rem;padding:3px 9px;border-radius:999px;border:1px solid var(--line);background:#fff;color:var(--muted);cursor:pointer}
button.mk:hover{border-color:var(--accent);color:var(--accent-dark)}
button.mk.on-right{background:#e6f4ea;border-color:#2e7d32;color:#1e5c24;font-weight:700}
button.mk.on-wrong{background:#fdecea;border-color:#c0392b;color:#8e2a1e;font-weight:700}
button.mk.on-arguable{background:#fdf3e0;border-color:#b26a00;color:#7a4a00;font-weight:700}
.summary-box{border:1px solid var(--line);border-radius:8px;background:#f8fafd;padding:14px 16px;margin-top:14px}
.summary-big{font-size:1.6rem;font-weight:700;color:var(--accent-dark)}
ul.examples{margin:6px 0 12px;padding-left:20px}
ul.examples li{margin:4px 0}
a.btn{display:inline-block;text-decoration:none;padding:8px 14px;border-radius:7px;border:1px solid var(--accent);background:var(--accent);color:#fff;font:inherit;cursor:pointer}
a.btn:hover{filter:brightness(1.06)}
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

<section class="card" id="spotCard">
  <h2>Spot-check: 10 random records</h2>
  <p class="note">Click <b>Check 10 at random</b> to draw 10 different records at random (without replacement) from the records matching the current filters above. For each record you see the full paragraph text, verbatim, and the SDGs the UN index assigned to it — mark each SDG as <b>✓ right</b>, <b>✗ wrong</b> or <b>? arguable</b>. The draw itself is random; every count, rate and the CSV below are computed locally in your browser from your clicks. Nothing is sent anywhere.</p>
  <div class="btnrow">
    <button id="btnDraw" type="button">Check 10 at random</button>
    <button id="btnRedraw" type="button" class="ghost" hidden>Draw again</button>
  </div>
  <p class="note" id="drawMsg"></p>
  <p class="note" id="drawProgress"></p>
  <div id="drawList"></div>
  <div id="drawSummary" class="summary-box" hidden></div>
</section>

<footer>Workshop dashboard · Data: <code>window.WORKSHOP_DATA.uhri</code> · All filtering, counting, charting and marking happens locally in your browser; no data leaves this page.</footer>
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

var years=[];
records.forEach(function(r){if(typeof r.year==='number'&&years.indexOf(r.year)===-1)years.push(r.year);});
years.sort(function(a,b){return a-b;});
var yMin=years.length?years[0]:null, yMax=years.length?years[years.length-1]:null;
var loaded=records.length;
var countTxt=(typeof D.count==='number'&&D.count!==loaded)?(D.count+' records in the source file, '+loaded+' loaded here'):(loaded+' records');
document.getElementById('desc').textContent='Source: '+(D.source||'OHCHR Universal Human Rights Index (UHRI)')+' — '+countTxt+' addressed to '+country+', covering '+(yMin!=null?(yMin+'–'+yMax):'no dated records')+(D.built?', data built '+D.built:'')+'.';
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
function recommender(r){
  if(r.mechanism!=='Universal Periodic Review')return null;
  var m=String(r.text||'').match(/\(([^()]+)\)\s*\.?\s*$/);
  return m?m[1].trim():null;
}
function detailHtml(r){
  var rec=recommender(r),h='';
  h+='<div class="fulltext">'+esc(r.text||'(no text available)')+'</div>';
  h+='<div class="meta"><b>Type:</b> '+esc(r.type||'—')+(r.section?' &nbsp;·&nbsp; <b>Section:</b> '+esc(r.section):'')+(r.date?' &nbsp;·&nbsp; <b>Date:</b> '+esc(r.date):'')+' &nbsp;·&nbsp; <b>Document:</b> '+(r.doc_url?'<a href="'+esc(r.doc_url)+'" target="_blank" rel="noopener">'+esc(r.symbol||r.doc_url)+'</a>':esc(r.symbol||'—'))+'</div>';
  if(rec)h+='<div class="meta"><b>Recommended by:</b> '+esc(rec)+' (read from the closing parentheses of the UPR recommendation text)</div>';
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

/* ---------- Spot-check: 10 random records ---------- */
var drawRecs=[],marks={},csvUrl=null;
var drawList=document.getElementById('drawList'),
    drawMsg=document.getElementById('drawMsg'),
    drawProgress=document.getElementById('drawProgress'),
    drawSummary=document.getElementById('drawSummary'),
    btnDraw=document.getElementById('btnDraw'),
    btnRedraw=document.getElementById('btnRedraw');

function sample(arr,n){
  var a=arr.slice();
  for(var i=a.length-1;i>0;i--){var j=Math.floor(Math.random()*(i+1));var t=a[i];a[i]=a[j];a[j]=t;}
  return a.slice(0,Math.min(n,a.length));
}
function sdgKey(r,s){return String(r.id)+'|'+String(s);}
function recItems(r){
  var seen={},out=[];
  (r.sdgs||[]).forEach(function(s){var k=String(s);if(!seen[k]){seen[k]=1;out.push(s);}});
  return out;
}
function recMarked(r){
  var items=recItems(r);
  if(!items.length)return marks[sdgKey(r,'')]!=null;
  return items.every(function(s){return marks[sdgKey(r,s)]!=null;});
}
function markBtns(k){
  var defs=[['right','✓ right','This SDG assignment is right'],['wrong','✗ wrong','This SDG assignment is wrong'],['arguable','? arguable','Arguable / uncertain']];
  return defs.map(function(d){
    return '<button type="button" class="mk" data-key="'+esc(k)+'" data-mark="'+d[0]+'" title="'+esc(d[2])+'">'+d[1]+'</button>';
  }).join(' ');
}
function drawCardHtml(r,i){
  var items=recItems(r);
  var sym=r.symbol?('<a href="'+esc(r.doc_url||'#')+'" target="_blank" rel="noopener">'+esc(r.symbol)+'</a>'):'—';
  var sdgHtml;
  if(items.length){
    sdgHtml=items.map(function(s){
      return '<div class="sdg-item"><span class="sdg-label">'+esc(sdgLabel(s))+'</span>'+markBtns(sdgKey(r,s))+'</div>';
    }).join('');
  }else{
    sdgHtml='<div class="sdg-item"><span class="sdg-label muted">No SDGs assigned by the index</span>'+markBtns(sdgKey(r,''))+'</div>';
  }
  return '<div class="draw-card">'+
    '<div class="draw-head"><b>#'+(i+1)+' of '+drawRecs.length+'</b> &nbsp;·&nbsp; '+esc(r.date||r.year||'')+' &nbsp;·&nbsp; '+esc(r.mechanism||'')+' &nbsp;·&nbsp; '+esc(r.body||'')+' &nbsp;·&nbsp; '+sym+'</div>'+
    '<div class="fulltext">'+esc(r.text||'(no text available)')+'</div>'+
    '<div class="meta"><b>SDGs assigned by the UN index — mark each one:</b></div>'+sdgHtml+
  '</div>';
}
function doDraw(){
  marks={};
  drawSummary.hidden=true;
  if(!current.length){
    drawRecs=[];
    drawList.innerHTML='';
    btnRedraw.hidden=true;
    drawProgress.textContent='';
    drawMsg.textContent='No records match the current filters — widen the filters above first, then draw again.';
    return;
  }
  drawRecs=sample(current,10);
  btnRedraw.hidden=false;
  drawMsg.textContent='Drawn at random (without replacement) from the '+current.length+' records matching the current filters when you clicked'+
    (drawRecs.length<10?' — only '+drawRecs.length+' records were available':'')+'. A record counts as marked when every SDG assigned to it has a mark.';
  drawList.innerHTML=drawRecs.map(drawCardHtml).join('');
  updateProgress();
}
function updateProgress(){
  if(!drawRecs.length){drawProgress.textContent='';return;}
  var marked=drawRecs.filter(recMarked).length;
  var total=Object.keys(marks).length;
  drawProgress.textContent='Marked '+marked+' of '+drawRecs.length+' records · '+total+' SDG mark'+(total===1?'':'s')+' so far.';
  if(marked===drawRecs.length)showSummary();else drawSummary.hidden=true;
}
function exLi(e){
  var r=e.r,sym=r.symbol?('<a href="'+esc(r.doc_url||'#')+'" target="_blank" rel="noopener">'+esc(r.symbol)+'</a>'):'—';
  var sdgTxt=e.sdg===''?'no SDG assigned':sdgLabel(e.sdg);
  return '<li>'+sym+' — '+esc(sdgTxt)+' — '+esc(firstLine(r.text))+'</li>';
}
function csvCell(v){return '"'+String(v==null?'':v).replace(/"/g,'""')+'"';}
function buildCsv(){
  var head=['draw_no','id','symbol','doc_url','date','year','body','mechanism','type','section','text','sdg','sdg_name','mark'];
  var lines=[head.map(csvCell).join(',')];
  drawRecs.forEach(function(r,i){
    var items=recItems(r);if(!items.length)items=[''];
    items.forEach(function(s){
      var k=sdgKey(r,s);
      lines.push([i+1,r.id,r.symbol,r.doc_url,r.date,r.year,r.body,r.mechanism,r.type,r.section,r.text,
        (s===''?'':s),(s===''?'':(sdgNames[String(s)]||'')),marks[k]||''].map(csvCell).join(','));
    });
  });
  return lines.join('\r\n');
}
function showSummary(){
  var total=Object.keys(marks).length,right=0,wrong=[],arg=[];
  var byId={};drawRecs.forEach(function(r){byId[String(r.id)]=r;});
  Object.keys(marks).forEach(function(k){
    var p=k.split('|'),rid=p[0],sdg=p.slice(1).join('|');
    var r=byId[rid];if(!r)return;
    var m=marks[k];
    if(m==='right')right++;
    else if(m==='wrong')wrong.push({r:r,sdg:sdg});
    else arg.push({r:r,sdg:sdg});
  });
  var rate=total?right/total:0;
  var csvName='sdg-spotcheck-'+country.toLowerCase().replace(/[^a-z0-9]+/g,'-')+'-'+new Date().toISOString().slice(0,10)+'.csv';
  drawSummary.innerHTML=
    '<div class="summary-big">Agreement rate: '+(rate*100).toFixed(1)+'%</div>'+
    '<p class="note">How this is computed: agreement rate = marks “right” ('+right+') ÷ all marks ('+total+'), calculated locally in your browser from your clicks — not estimated. Wrong marks: '+wrong.length+' · arguable marks: '+arg.length+'.</p>'+
    (wrong.length?'<h3>Wrong examples ('+wrong.length+')</h3><ul class="examples">'+wrong.map(exLi).join('')+'</ul>':'')+
    (arg.length?'<h3>Arguable examples ('+arg.length+')</h3><ul class="examples">'+arg.map(exLi).join('')+'</ul>':'')+
    '<p><a class="btn" id="csvLink" download="'+esc(csvName)+'">Download the '+drawRecs.length+' records with your marks as CSV ('+total+' marks)</a></p>';
  drawSummary.hidden=false;
  var blob=new Blob(['\ufeff'+buildCsv()],{type:'text/csv;charset=utf-8'});
  if(csvUrl)URL.revokeObjectURL(csvUrl);
  csvUrl=URL.createObjectURL(blob);
  document.getElementById('csvLink').href=csvUrl;
}
btnDraw.addEventListener('click',doDraw);
btnRedraw.addEventListener('click',doDraw);
drawList.addEventListener('click',function(e){
  var b=e.target.closest('button.mk');if(!b)return;
  var key=b.getAttribute('data-key'),m=b.getAttribute('data-mark');
  marks[key]=m;
  var card=b.closest('.draw-card');
  var sel='button.mk[data-key="'+key.replace(/"/g,'\\"')+'"]';
  card.querySelectorAll(sel).forEach(function(x){
    x.classList.remove('on-right','on-wrong','on-arguable');
    if(x.getAttribute('data-mark')===m)x.classList.add('on-'+m);
  });
  updateProgress();
});

render();
})();
</script>
</body>
</html>
```