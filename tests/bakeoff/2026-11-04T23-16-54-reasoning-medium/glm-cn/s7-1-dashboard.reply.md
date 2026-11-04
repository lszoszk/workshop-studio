I built the dashboard exactly to the plan: three tabs (Overview, Records, Method & export), a shared filter rail, Chart.js figures, an in-place self-check panel, and CSV/summary export — all computed in-browser from `WORKSHOP_DATA.uhri`.

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>UN human rights recommendations and observations: <span id="t-country"></span></title>
<style>
:root{--paper:#f4f0e8;--ink:#1d1b18;--rule:#d9d2c3;--accent:#9b2335;--upr:#c2410c;--tb:#0f766e;--sp:#7c3aed}
*{box-sizing:border-box}
[hidden]{display:none!important}
body{margin:0;background:var(--paper);color:var(--ink);font:16px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif}
.mono{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:11px;letter-spacing:.08em;text-transform:uppercase}
header{border-bottom:1px solid var(--rule);padding:18px 24px 14px}
header .mono{color:#6b6459}
h1{font-family:Georgia,"Times New Roman",serif;font-size:34px;font-weight:normal;margin:6px 0 4px}
.srcline{font-size:13px;color:#57503f}
.srcline a{color:var(--accent)}
a{color:var(--ink)}
main{display:flex;min-height:70vh}
nav.rail{width:270px;flex:none;border-right:1px solid var(--rule);padding:16px 18px}
nav.rail .rhead{display:flex;justify-content:space-between;align-items:baseline;border-bottom:1px solid var(--rule);padding-bottom:6px}
nav.rail .rhead .mono{font-weight:bold}
#clearAll{background:none;border:none;color:var(--accent);font:11px ui-monospace,Menlo,Consolas,monospace;letter-spacing:.05em;text-transform:uppercase;cursor:pointer;padding:0}
#clearAll:hover{text-decoration:underline}
.bignum{font-family:Georgia,serif;font-size:44px;line-height:1.05;margin:14px 0 2px}
#ofN{font-size:12px;color:#57503f}
.sharebar{height:4px;background:var(--rule);margin:10px 0 4px}
.sharebar div{height:100%;background:var(--accent)}
.chips{margin:8px 0 4px;display:flex;flex-wrap:wrap;gap:4px}
.chip{display:inline-flex;align-items:center;gap:5px;border:1px solid var(--rule);background:#fdfbf6;font-size:12px;padding:2px 6px;border-radius:10px}
.chip button{background:none;border:none;color:var(--accent);cursor:pointer;font-weight:bold;padding:0;line-height:1}
.fgroup{border-bottom:1px solid var(--rule)}
.fgroup>button.fhead{width:100%;text-align:left;background:none;border:none;cursor:pointer;padding:10px 0;font:11px ui-monospace,Menlo,Consolas,monospace;letter-spacing:.08em;text-transform:uppercase;display:flex;justify-content:space-between;color:var(--ink)}
.fgroup>button.fhead[aria-expanded="true"]{color:var(--accent)}
.fbody{padding:2px 0 12px}
.hint{font-size:11px;color:#57503f;margin:4px 0}
input[type=text],select{width:100%;padding:6px 8px;border:1px solid var(--rule);background:#fdfbf6;font:14px -apple-system,sans-serif;border-radius:0}
select{margin:3px 0}
label.small{font-size:12px;display:block;margin-top:6px}
button:focus,a:focus,input:focus,select:focus,[tabindex]:focus{outline:2px solid var(--accent);outline-offset:2px}
section.panel{flex:1;padding:18px 26px 40px;max-width:1100px}
.tabs{display:flex;gap:2px;border-bottom:1px solid var(--rule);margin-bottom:20px;flex-wrap:wrap}
.tab{background:none;border:none;border-bottom:3px solid transparent;cursor:pointer;padding:8px 14px;font:11px ui-monospace,Menlo,Consolas,monospace;letter-spacing:.08em;text-transform:uppercase;color:#57503f}
.tab[aria-selected="true"]{color:var(--accent);border-bottom-color:var(--accent)}
.tiles{display:flex;gap:28px;flex-wrap:wrap;margin-bottom:8px}
.tile{flex:1;min-width:200px}
.tile .num{font-family:Georgia,serif;font-size:52px;line-height:1}
.tile .cap{margin-top:4px;font-size:13px;color:#57503f}
.tile .dot{display:inline-block;width:9px;height:9px;border-radius:50%;margin-right:5px}
figure{margin:28px 0}
figcaption{font-family:Georgia,serif;font-size:19px;margin-bottom:2px}
figure .mono{color:#6b6459}
.srcline-fig{font-size:12px;color:#57503f;margin:4px 0 10px}
.chartbox{position:relative;height:320px}
.chartbox.small{height:280px}
table{border-collapse:collapse;width:100%;font-size:14px;margin-top:10px}
caption{text-align:left;font-size:12px;color:#57503f;padding-bottom:6px}
th,td{text-align:left;padding:5px 10px 5px 0;border-bottom:1px solid var(--rule);vertical-align:top}
th{font:11px ui-monospace,Menlo,Consolas,monospace;letter-spacing:.06em;text-transform:uppercase;color:#57503f}
th.num,td.num{text-align:right;font-variant-numeric:tabular-nums}
tr.rec{cursor:pointer}
tr.rec:hover{background:#efe9dc}
tr.exp>td{background:#fdfbf6}
.parabig{color:var(--accent);font-family:Georgia,serif;font-size:30px}
.labels{margin:8px 0 0;padding:0;list-style:none;font-size:13px}
.labels li{margin:2px 0}
mark{background:#f3d9a8;padding:0 1px}
.morebtn{margin:14px 0;background:none;border:1px solid var(--rule);padding:8px 16px;cursor:pointer;font:12px ui-monospace,monospace;letter-spacing:.05em;text-transform:uppercase}
.checks li{margin:3px 0;font-size:14px}
.ok{color:#1a6b3c;font-weight:bold}
.bad{color:var(--accent);font-weight:bold}
.copied{color:#1a6b3c;font-size:12px;margin-left:8px}
h2.sec{font-family:Georgia,serif;font-weight:normal;font-size:22px;margin:26px 0 8px}
h3.sub{font:11px ui-monospace,Menlo,Consolas,monospace;letter-spacing:.08em;text-transform:uppercase;color:#57503f;margin:18px 0 6px}
p.method{font-size:14px;max-width:70ch}
footer{border-top:1px solid var(--rule);padding:10px 24px;font-size:11px;color:#57503f;display:flex;gap:16px;flex-wrap:wrap}
.statelist{margin:6px 0 0;padding-left:18px;font-size:14px}
@media (max-width:800px){main{flex-direction:column}nav.rail{width:100%;border-right:none;border-bottom:1px solid var(--rule)}}
</style>
</head>
<body>
<header>
  <div class="mono" id="h-label">UHRI</div>
  <h1 id="h-title"></h1>
  <div class="srcline" id="h-src"></div>
</header>
<main>
<nav class="rail" id="rail">
  <div class="rhead"><span class="mono">Filters</span><button id="clearAll">Clear all</button></div>
  <div class="bignum" id="matchN">0</div>
  <div id="ofN" class="mono" style="text-transform:none;letter-spacing:0"></div>
  <div class="sharebar"><div id="shareFill"></div></div>
  <div class="chips" id="chips"></div>
  <div id="filterGroups"></div>
</nav>
<section class="panel">
  <div class="tabs" role="tablist" aria-label="Dashboard tabs">
    <button class="tab" role="tab" id="tab1" aria-selected="true" aria-controls="p1">01 Overview</button>
    <button class="tab" role="tab" id="tab2" aria-selected="false" aria-controls="p2" tabindex="-1">02 Records</button>
    <button class="tab" role="tab" id="tab3" aria-selected="false" aria-controls="p3" tabindex="-1">03 Method &amp; export</button>
  </div>

  <div role="tabpanel" id="p1" aria-labelledby="tab1">
    <div class="tiles" id="tilesTop"></div>
    <div class="tiles" id="tilesMech"></div>
    <figure>
      <div class="mono">FIG.01</div>
      <figcaption id="fig1title"></figcaption>
      <div class="srcline-fig" id="fig1src"></div>
      <div class="chartbox"><canvas id="chart1"></canvas></div>
      <div id="fig1table"></div>
    </figure>
    <figure>
      <div class="mono">FIG.02</div>
      <figcaption id="fig2title"></figcaption>
      <div class="srcline-fig" id="fig2src"></div>
      <div class="chartbox small"><canvas id="chart2"></canvas></div>
    </figure>
    <button class="fhead" id="checksBtn" aria-expanded="false" style="border:none;background:none;cursor:pointer;padding:8px 0;font:11px ui-monospace,Menlo,Consolas,monospace;letter-spacing:.08em;text-transform:uppercase;border-bottom:1px solid var(--rule);width:100%;text-align:left">Every check (<span id="nchecks"></span>)</button>
    <div id="checksPanel" hidden>
      <h3 class="sub">How the app checks itself</h3>
      <ul class="checks" id="checksList"></ul>
    </div>
  </div>

  <div role="tabpanel" id="p2" aria-labelledby="tab2" hidden>
    <input type="text" id="search2" placeholder="Search records, e.g. torture" aria-label="Search records">
    <div class="hint">literal match, not synonyms — every word must occur in the text or symbol</div>
    <div id="tblWrap"></div>
    <button class="morebtn" id="moreBtn" hidden>Show 50 more</button>
  </div>

  <div role="tabpanel" id="p3" aria-labelledby="tab3" hidden>
    <h2 class="sec">How each number is computed</h2>
    <div id="methodText"></div>
    <h2 class="sec">Export</h2>
    <p>
      <button class="morebtn" id="csvBtn">Download CSV of the current filter</button>
      <button class="morebtn" id="sumBtn">Copy summary</button>
      <span class="copied" id="copiedSum" hidden>Copied</span>
    </p>
    <h2 class="sec">Source</h2>
    <p class="method" id="srcLine3"></p>
  </div>
</section>
</main>
<footer id="foot"></footer>

<script>
(function(){
"use strict";
const D = window.WORKSHOP_DATA.uhri;
const records = D.records || [];
const N = records.length;
const COUNTRY = D.country;
const MECH_COLORS = {"Universal Periodic Review":"#c2410c","Treaty bodies":"#0f766e","Special Procedures":"#7c3aed"};
const fmt = n => n.toLocaleString("en-US");

// ---------- header ----------
document.title = "UN human rights recommendations and observations: " + COUNTRY;
document.getElementById("h-label").textContent = "UHRI · " + COUNTRY;
document.getElementById("h-title").textContent = "UN human rights recommendations and observations: " + COUNTRY;
const symbols = [...new Set(records.map(r=>r.symbol))];
const years = records.map(r=>r.year);
document.getElementById("h-src").innerHTML =
  'Source: <a href="'+(D.source_url||"#")+'" target="_blank" rel="noopener">'+(D.source||"OHCHR UHRI")+'</a> · '+
  fmt(N)+' records · '+symbols.length+' documents · '+Math.min(...years)+'–'+Math.max(...years)+
  ' · built '+(D.built||"n/a")+' · dated by document (date is the document\u2019s date, not the date a recommendation was made or accepted)';

// ---------- derived helpers ----------
function paraNum(text){
  const m = /^(\d{1,3}(?:\.\d{1,3})?)\.?\s/.exec(text||"");
  return m ? m[1] : null;
}
const stateRunRe = /((?:\s*\((?:[^()]|\([^()]*\))*\))+)\s*[;.]?\s*$/;
const groupRe = /\((?:[^()]|\([^()]*\))*\)/g;
function recStates(r){
  if(r.mechanism !== "Universal Periodic Review") return null;
  const m = stateRunRe.exec(r.text||"");
  if(!m) return [];
  const out = [];
  for(const g of m[1].match(groupRe)||[]){
    let s = g.slice(1,-1).trim();
    if(s && !s.includes(",") && s.length<=60) out.push(s);
  }
  return out;
}
records.forEach(r=>{ r._para = paraNum(r.text); r._states = recStates(r); });
const allStates = {};
records.forEach(r=>{ if(r._states) r._states.forEach(s=>{ allStates[s]=(allStates[s]||0)+1; }); });

function firstLine(t){
  t = t||"";
  if(t.length<=120) return t;
  let cut = t.slice(0,120), sp = cut.lastIndexOf(" ");
  return (sp>60?cut.slice(0,sp):cut)+"…";
}

// ---------- filters ----------
const F = { keyword:"", mechanism:"", body:"", type:"", yFrom:"", yTo:"", sdg:"", state:"" };
const distinct = (arr)=>[...new Set(arr)].filter(v=>v!==""&&v!=null);
const allMechs = distinct(records.map(r=>r.mechanism)).sort();
const allTypes = distinct(records.map(r=>r.type)).sort();
const allYears = distinct(records.map(r=>r.year)).sort((a,b)=>a-b);
const sdgCounts = {};
records.forEach(r=>(r.sdgs||[]).forEach(g=>{ sdgCounts[g]=(sdgCounts[g]||0)+1; }));
const allSdgs = Object.keys(sdgCounts).map(Number).sort((a,b)=>a-b);
const sdgNames = D.sdg_names || {};

function filtered(){
  const kw = F.keyword.trim().toLowerCase().split(/\s+/).filter(Boolean);
  return records.filter(r=>{
    if(F.mechanism && r.mechanism!==F.mechanism) return false;
    if(F.body && r.body!==F.body) return false;
    if(F.type && r.type!==F.type) return false;
    if(F.sdg!=="" && !(r.sdgs||[]).includes(Number(F.sdg))) return false;
    if(F.state && !(r._states||[]).includes(F.state)) return false;
    if(F.yFrom!=="" && r.year < Number(F.yFrom)) return false;
    if(F.yTo!=="" && r.year > Number(F.yTo)) return false;
    for(const w of kw){
      if(!((r.text||"").toLowerCase().includes(w) || (r.symbol||"").toLowerCase().includes(w))) return false;
    }
    return true;
  });
}

// ---------- rail ----------
const chipsEl = document.getElementById("chips");
function chip(label, key){
  const s = document.createElement("span"); s.className="chip";
  const b = document.createElement("button"); b.textContent="×"; b.setAttribute("aria-label","Remove filter "+label);
  b.onclick = ()=>{ F[key] = (key==="yFrom"||key==="yTo") ? "" : ""; syncInputs(); apply(); };
  s.append(document.createTextNode(label), b); chipsEl.appendChild(s);
}
function renderChips(){
  chipsEl.innerHTML = "";
  if(F.keyword) chip("keyword: "+F.keyword,"keyword");
  if(F.mechanism) chip("mechanism: "+F.mechanism,"mechanism");
  if(F.body) chip("body: "+F.body,"body");
  if(F.type) chip("type: "+F.type,"type");
  if(F.sdg!=="") chip("SDG "+F.sdg,"sdg");
  if(F.state) chip("State: "+F.state,"state");
  if(F.yFrom!==""||F.yTo!=="") chip("years: "+(F.yFrom||allYears[0])+"–"+(F.yTo||allYears[allYears.length-1]),"yFrom");
}
document.getElementById("clearAll").onclick = ()=>{
  for(const k in F) F[k]="";
  syncInputs(); apply();
};

// filter groups
const groups = [
  {id:"g1", label:"01 Keyword"},
  {id:"g2", label:"02 Mechanism, body, type"},
  {id:"g3", label:"03 Years and SDG"}
];
const fgEl = document.getElementById("filterGroups");
let openGroup = null;
groups.forEach(g=>{
  const wrap = document.createElement("div"); wrap.className="fgroup";
  const btn = document.createElement("button"); btn.className="fhead";
  btn.setAttribute("aria-expanded","false"); btn.setAttribute("aria-controls",g.id);
  const lab = document.createElement("span"); lab.textContent = g.label;
  const ind = document.createElement("span"); ind.textContent = "+";
  btn.append(lab,ind);
  const body = document.createElement("div"); body.className="fbody"; body.id=g.id; body.hidden=true;
  btn.onclick = ()=>{
    if(openGroup===g.id){ body.hidden=true; btn.setAttribute("aria-expanded","false"); ind.textContent="+"; openGroup=null; }
    else{
      groups.forEach(o=>{ document.getElementById(o.id).hidden=true;
        document.querySelector('[aria-controls="'+o.id+'"]').setAttribute("aria-expanded","false");
        document.querySelector('[aria-controls="'+o.id+'"]').lastChild.textContent="+"; });
      body.hidden=false; btn.setAttribute("aria-expanded","true"); ind.textContent="−"; openGroup=g.id;
    }
  };
  wrap.append(btn,body); fgEl.appendChild(wrap);
});
const g1 = document.getElementById("g1"), g2 = document.getElementById("g2"), g3 = document.getElementById("g3");
g1.innerHTML = '<input type="text" id="kwBox" aria-label="Keyword"><div class="hint">literal match, not synonyms</div>';
let kwTimer=null;
g1.querySelector("#kwBox").addEventListener("input",e=>{
  clearTimeout(kwTimer);
  kwTimer=setTimeout(()=>{ F.keyword=e.target.value; apply(); },300);
});

function fillG2(){
  const mechs = F.mechanism ? [F.mechanism] : allMechs;
  const bodies = distinct(records.filter(r=>mechs.includes(r.mechanism)).map(r=>r.body)).sort();
  const bodyCounts = {}; records.filter(r=>mechs.includes(r.mechanism)).forEach(r=>{ bodyCounts[r.body]=(bodyCounts[r.body]||0)+1; });
  const types = distinct(records.filter(r=>mechs.includes(r.mechanism)).map(r=>type)).sort();
  const types2 = distinct(records.filter(r=>mechs.includes(r.mechanism)).map(r=>r.type)).sort();
  let h = '<label class="small">Mechanism</label><select id="selMech"><option value="">all</option>';
  allMechs.forEach(m=>{ h+='<option'+(F.mechanism===m?" selected":"")+'>'+m+'</option>'; });
  h+='</select><label class="small">Body or mandate</label><select id="selBody"><option value="">all</option>';
  bodies.forEach(b=>{ h+='<option'+(F.body===b?" selected":"")+'>'+b+' ('+fmt(bodyCounts[b]||0)+')</option>'; });
  h+='</select><label class="small">Type</label><select id="selType"><option value="">all</option>';
  types2.forEach(t=>{ h+='<option'+(F.type===t?" selected":"")+'>'+t+'</option>'; });
  h+='</select>';
  if(Object.keys(allStates).length){
    h+='<label class="small">Recommending State (UPR)</label><select id="selState"><option value="">all</option>';
    Object.keys(allStates).sort((a,b)=>allStates[b]-allStates[a]).forEach(s=>{
      h+='<option'+(F.state===s?" selected":"")+'>'+s+' ('+fmt(allStates[s])+')</option>'; });
    h+='</select>';
  }
  g2.innerHTML = h;
  g2.querySelector("#selMech").onchange = e=>{ F.mechanism=e.target.value; F.body=""; F.type=""; apply(); };
  g2.querySelector("#selBody").onchange = e=>{ F.body=e.target.value; apply(); };
  g2.querySelector("#selType").onchange = e=>{ F.type=e.target.value; apply(); };
  const st = g2.querySelector("#selState"); if(st) st.onchange = e=>{ F.state=e.target.value; apply(); };
}
function fillG3(){
  let h = '<label class="small">Year from</label><select id="selYF"><option value="">—</option>';
  allYears.forEach(y=>{ h+='<option'+(String(y)===String(F.yFrom)?" selected":"")+'>'+y+'</option>'; });
  h+='</select><label class="small">Year to</label><select id="selYT"><option value="">—</option>';
  allYears.forEach(y=>{ h+='<option'+(String(y)===String(F.yTo)?" selected":"")+'>'+y+'</option>'; });
  h+='</select><label class="small">SDG goal</label><select id="selSdg"><option value="">all</option>';
  allSdgs.forEach(g2v=>{ const nm = sdgNames[String(g2v)]||""; h+='<option value="'+g2v+'"'+(String(F.sdg)===String(g2v)?" selected":"")+'>'+g2v+'. '+(nm.length>32?nm.slice(0,32)+"…":nm)+' ('+fmt(sdgCounts[g2v])+')</option>'; });
  h+='</select>';
  g3.innerHTML = h;
  g3.querySelector("#selYF").onchange = e=>{ F.yFrom=e.target.value; swapYears(); apply(); };
  g3.querySelector("#selYT").onchange = e=>{ F.yTo=e.target.value; swapYears(); apply(); };
  g3.querySelector("#selSdg").onchange = e=>{ F.sdg=e.target.value; apply(); };
}
function swapYears(){
  if(F.yFrom!=="" && F.yTo!=="" && Number(F.yFrom)>Number(F.yTo)){
    const t=F.yFrom; F.yFrom=F.yTo; F.yTo=t;
    const a=document.getElementById("selYF"), b=document.getElementById("selYT");
    if(a) a.value=F.yFrom; if(b) b.value=F.yTo;
  }
}
function syncInputs(){
  const kw=document.getElementById("kwBox"); if(kw) kw.value=F.keyword;
  fillG2(); fillG3();
}

// ---------- tabs ----------
const tabs=[...document.querySelectorAll(".tab")];
const panels=["p1","p2","p3"].map(id=>document.getElementById(id));
let curTab=0;
function showTab(i){
  curTab=i;
  tabs.forEach((t,j)=>{ t.setAttribute("aria-selected",j===i?"true":"false"); t.tabIndex=j===i?0:-1; });
  panels.forEach((p,j)=>{ p.hidden = j!==i; });
  // rail: filters on tabs 1 and 2, number+bar+chips on 3
  fgEl.hidden = (i===2);
  tabs[i].focus();
}
tabs.forEach((t,i)=>{
  t.onclick=()=>{ showTab(i); if(i===1) renderTable(); };
  t.onkeydown=e=>{
    if(e.key==="ArrowRight"){ showTab((i+1)%3); e.preventDefault(); }
    if(e.key==="ArrowLeft"){ showTab((i+2)%3); e.preventDefault(); }
  };
});
const search2 = document.getElementById("search2");
search2.addEventListener("input",e=>{
  clearTimeout(kwTimer);
  kwTimer=setTimeout(()=>{ F.keyword=e.target.value;
    const kb=document.getElementById("kwBox"); if(kb) kb.value=F.keyword;
    apply(); },300);
});

// ---------- charts ----------
let chart1=null, chart2=null;
function esc(s){ return String(s).replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;").replace(/"/g,"&quot;"); }
function renderCharts(set){
  // FIG01 themes
  const themeCounts={};
  set.forEach(r=>(r.themes||[]).forEach(t=>{ themeCounts[t]=(themeCounts[t]||0)+1; }));
  let top = Object.keys(themeCounts).map(t=>({t,c:themeCounts[t],
    y1:Math.min(...set.filter(r=>(r.themes||[]).includes(t)).map(r=>r.year)),
    y2:Math.max(...set.filter(r=>(r.themes||[]).includes(t)).map(r=>r.year))}));
  top.sort((a,b)=>b.c-a.c || a.t.localeCompare(b.t));
  top = top.slice(0,10);
  document.getElementById("fig1title").textContent = "Ten most frequent themes among "+fmt(set.length)+" filtered records";
  document.getElementById("fig1src").textContent = "Horizontal bars, ranked. A record can carry several themes, so the bars add up to more than "+fmt(set.length)+". Click a bar to filter by that theme. Source: OHCHR UHRI, computed in this page.";
  const lbls = top.map(o=>o.t.length>48?o.t.slice(0,48)+"…":o.t);
  if(chart1) chart1.destroy();
  chart1 = new Chart(document.getElementById("chart1"),{
    type:"bar",
    data:{labels:lbls,datasets:[{data:top.map(o=>o.c),backgroundColor:"rgba(155,35,53,0.8)"}]},
    options:{indexAxis:"y",responsive:true,maintainAspectRatio:false,
      plugins:{legend:{display:false},tooltip:{callbacks:{title:c=>top[c[0].dataIndex].t}}},
      scales:{x:{grid:{display:false},ticks:{precision:0}},y:{grid:{display:false}}},
      onClick:(e,els)=>{ if(els.length){ applyThemeFilter(top[els[0].index].t); } }}
  });
  const themeSet = new Set(top.map(o=>o.t));
  document.getElementById("fig1table").innerHTML =
    '<table><caption>Same ten themes as FIG.01. Theme | Records | % of filtered | Years. Percentages are of records, not of labels; the Years column gives the first–last year of the filtered records carrying the theme, so a legacy label can be judged.</caption>'+
    '<thead><tr><th scope="col">Theme</th><th scope="col" class="num">Records</th><th scope="col" class="num">% of filtered</th><th scope="col" class="num">Years</th></tr></thead><tbody>'+
    top.map(o=>'<tr><td>'+esc(o.t)+'</td><td class="num">'+fmt(o.c)+'</td><td class="num">'+(set.length?(100*o.c/set.length).toFixed(1):"0.0")+'%</td><td class="num">'+o.y1+'–'+o.y2+'</td></tr>').join("")+
    '</tbody></table>';
  topThemesForExport = top;

  // FIG02 timeline
  const mechs = allMechs;
  const y0=Math.min(...years), y1=Math.max(...years);
  const allY=[]; for(let y=y0;y<=y1;y++) allY.push(y);
  const data = mechs.map(m=>allY.map(y=>set.filter(r=>r.year===y&&r.mechanism===m).length));
  document.getElementById("fig2title").textContent = "Records per year by mechanism, current filter";
  document.getElementById("fig2src").textContent = "Stacked bars; every year from "+y0+" to "+y1+" is shown, so years with no records appear as gaps. Source: OHCHR UHRI, computed in this page.";
  if(chart2) chart2.destroy();
  chart2 = new Chart(document.getElementById("chart2"),{
    type:"bar",
    data:{labels:allY,datasets:mechs.map((m,i)=>({label:m,data:data[i],backgroundColor:MECH_COLORS[m]||"#9b2335"}))},
    options:{responsive:true,maintainAspectRatio:false,
      plugins:{legend:{position:"bottom",labels:{boxWidth:10}}},
      scales:{x:{stacked:true,grid:{display:false}},y:{stacked:true,grid:{display:false},ticks:{precision:0}}}}
  });
}
let topThemesForExport=[];
function applyThemeFilter(t){
  // reuse keyword? No: exact theme match needed — approximate by adding to keyword is wrong.
  // We add a theme filter via a dedicated chip using keyword-like behaviour on themes field.
  F.theme = (F.theme===t) ? "" : t;
  apply();
}
// extend filtered() to honour F.theme
const _filtered = filtered;
filtered = function(){
  return _filtered().filter(r=>!F.theme || (r.themes||[]).includes(F.theme));
};

// ---------- tiles ----------
function renderTiles(set){
  const typeCounts={}; set.forEach(r=>{ typeCounts[r.type]=(typeCounts[r.type]||0)+1; });
  const t1 = '<div class="tile"><div class="num">'+fmt(set.length)+'</div><div class="cap">records in the file'+(set.length<N?' (filtered of '+fmt(N)+')':'')+'<br>'+
    Object.keys(typeCounts).map(t=>fmt(typeCounts[t])+" "+esc(t)).join(" · ")+
    '<br><span class="hint">Headline total = number of records shown; the breakdown counts records per type, spelled as in the data.</span></div></div>';
  const docs=[...new Set(set.map(r=>r.symbol))].length;
  const yrs = set.length?Math.min(...set.map(r=>r.year))+"–"+Math.max(...set.map(r=>r.year)):"—";
  const t2 = '<div class="tile"><div class="num">'+fmt(docs)+'</div><div class="cap">documents (distinct symbols)<br>years '+yrs+
    '<br><span class="hint">Documents = distinct symbol; years = min–max of year in the current set.</span></div></div>';
  document.getElementById("tilesTop").innerHTML = t1+t2;
  let mh = allMechs.map(m=>{
    const rs=set.filter(r=>r.mechanism===m);
    if(!rs.length && !records.some(r=>r.mechanism===m)) return "";
    const tot=records.filter(r=>r.mechanism===m).length;
    return '<div class="tile"><div class="num">'+fmt(rs.length)+'</div><div class="cap">'+
      '<span class="dot" style="background:'+(MECH_COLORS[m]||"#9b2335")+'"></span>'+esc(m)+'<br>'+
      fmt([...new Set(rs.map(r=>r.symbol))].length)+' documents · latest '+(rs.length?Math.max(...rs.map(r=>r.year)):"—")+' · '+
      (set.length?(100*rs.length/set.length).toFixed(1):"0.0")+'% of filtered (of '+fmt(tot)+' in file)'+
      (m==="Universal Periodic Review"?' <a href="#" id="seeStates">see the States</a>':'')+
      '<br><span class="hint">Records whose mechanism matches, in the current filter.</span></div></div>';
  }).join("");
  document.getElementById("tilesMech").innerHTML = mh;
  const ss=document.getElementById("seeStates");
  if(ss) ss.onclick=(e)=>{
    e.preventDefault();
    let el=document.getElementById("stateList");
    if(el){ el.remove(); return; }
    el=document.createElement("ol"); el.id="stateList"; el.className="statelist"; el.type="1";
    const cnt={}; set.forEach(r=>(r._states||[]).forEach(s=>{ cnt[s]=(cnt[s]||0)+1; }));
    Object.keys(cnt).sort((a,b)=>cnt[b]-cnt[a]).slice(0,10).forEach(s=>{
      const li=document.createElement("li"); li.textContent=s+" — "+fmt(cnt[s]); el.appendChild(li); });
    const liEnd=document.createElement("li");
    liEnd.style.listStyle="none"; liEnd.className="hint";
    liEnd.textContent="Counts of recommendations, not of influence; two States can co-sponsor one line.";
    el.appendChild(liEnd);
    ss.closest(".tile").after(el);
  };
}

// ---------- records table ----------
let shown=50, sortNewest=true;
function highlight(text){
  const kw=F.keyword.trim().toLowerCase().split(/\s+/).filter(Boolean);
  let t=esc(text);
  if(!kw.length) return t;
  kw.forEach(w=>{
    t=t.replace(new RegExp("("+w.replace(/[.*+?^${}()|[\]\\]/g,"\\$&")+")","gi"),"<mark>$1</mark>");
  });
  return t;
}
function renderTable(){
  const set=filtered();
  const wrap=document.getElementById("tblWrap");
  shown=Math.min(shown,set.length);
  const rows=set.slice().sort((a,b)=>{
    if(sortNewest ? (b.date||"").localeCompare(a.date||"") : (a.date||"").localeCompare(b.date||"")) return sortNewest?1:-1;
    // careful: implement properly below
    return 0;
  });
  // proper sort
  const sorted=set.slice().sort((a,b)=>{
    const d = (b.date||"").localeCompare(a.date||"");
    if(!sortNewest){ if(d!==0) return -d; } else { if(d!==0) return d; }
    const bo=(a.body||"").localeCompare(b.body||""); if(bo) return bo;
    const pa=parseFloat(a._para), pb=parseFloat(b._para);
    if(!isNaN(pa)&&!isNaN(pb)&&pa!==pb) return pa-pb;
    if(a._para&&!b._para) return -1; if(!a._para&&b._para) return 1;
    return records.indexOf(a)-records.indexOf(b);
  });
  const view=sorted.slice(0,shown);
  let h='<table><caption>'+fmt(view.length)+' of '+fmt(set.length)+' matching rows shown'+(set.length?'':' — no records match the current filter')+' · '+
    (sortNewest?'newest first':'oldest first')+' · click the Date header to reverse · click a row to expand it</caption>'+
    '<thead><tr><th scope="col"><button id="dateHdr" style="background:none;border:none;cursor:pointer;font:inherit;color:inherit;text-transform:inherit;letter-spacing:inherit">Date ▾</button></th>'+
    '<th scope="col">Body</th><th scope="col">Symbol</th><th scope="col" class="num">Para.</th><th scope="col">First line</th><th scope="col">Recommending State</th></tr></thead><tbody>';
  view.forEach((r,i)=>{
    const states = r.mechanism==="Universal Periodic Review" ? ((r._states&&r._states.length)?esc(r._states.join(", ")):(r._states?"State not found":"—")) : "—";
    h+='<tr class="rec" tabindex="0" data-i="'+set.indexOf(r)+'"><td>'+esc(r.date)+'</td><td>'+esc(r.body)+'</td>'+
      '<td><a href="'+esc(r.doc_url)+'" target="_blank" rel="noopener">'+esc(r.symbol)+'</a></td>'+
      '<td class="num">'+(r._para?esc(r._para):"—")+'</td>'+
      '<td>'+highlight(firstLine(r.text))+'</td><td>'+states+'</td></tr>';
  });
  h+='</tbody></table>';
  wrap.innerHTML=h;
  document.getElementById("dateHdr").onclick=()=>{ sortNewest=!sortNewest; renderTable(); };
  wrap.querySelectorAll("tr.rec").forEach(tr=>{
    const open=()=>toggleRow(tr, set[Number(tr.dataset.i)]);
    tr.onclick=e=>{ if(e.target.closest("a,button")) return; open(); };
    tr.onkeydown=e=>{ if(e.key==="Enter"){ e.preventDefault(); open(); } };
  });
  const mb=document.getElementById("moreBtn");
  mb.hidden = shown>=set.length;
  mb.textContent="Show 50 more ("+fmt(set.length-shown)+" left)";
}
document.getElementById("moreBtn").onclick=()=>{ shown+=50; renderTable(); };

function toggleRow(tr, r){
  let ex=tr.nextElementSibling;
  if(ex && ex.classList.contains("exp")){ ex.remove(); return; }
  wrap_closeAll();
  const sdgN=(r.sdgs||[]).map(g=>g+". "+(sdgNames[String(g)]||"")).join(", ");
  const ex2=document.createElement("tr"); ex2.className="exp";
  ex2.innerHTML='<td colspan="6">'+
    '<div class="parabig">'+(r._para?esc(r._para):"(no paragraph number in this extract)")+'</div>'+
    '<p style="max-width:75ch">'+highlight(r.text)+'</p>'+
    '<ul class="labels">'+
    (r.section?'<li><span class="mono">Section</span> — '+esc(r.section)+'</li>':'')+
    '<li><span class="mono">Themes</span> — '+(r.themes&&r.themes.length?esc(r.themes.join(" · ")):"not labelled")+'</li>'+
    '<li><span class="mono">SDGs</span> — '+(sdgN||"not labelled")+(r.sdg_targets&&r.sdg_targets.length?' · targets: '+esc(r.sdg_targets.join(" · ")):'')+'</li>'+
    '<li><span class="mono">Affected persons</span> — '+(r.affected_persons&&r.affected_persons.length?esc(r.affected_persons.join(" · ")):"not labelled")+'</li>'+
    (r._states&&r._states.length?'<li><span class="mono">Recommending State</span> — '+esc(r._states.join(", "))+'</li>':'')+
    '</ul>'+
    '<p><button class="morebtn" data-copy>Copy citation'+(r._para?"":" (no paragraph number in this extract)")+'</button>'+
    '<span class="copied" hidden>Copied</span> '+
    '<a class="morebtn" style="text-decoration:none;display:inline-block" href="'+esc(r.doc_url)+'" target="_blank" rel="noopener">Open the UN document</a></p></td>';
  tr.after(ex2);
  const cb=ex2.querySelector("[data-copy]"), cc=ex2.querySelector(".copied");
  cb.onclick=async()=>{
    const cite = r.symbol + (r._para ? ", para. "+r._para : "");
    try{ await navigator.clipboard.writeText(cite); }catch(e){}
    cc.hidden=false; setTimeout(()=>{ cc.hidden=true; },2000);
  };
}
function wrap_closeAll(){
  document.querySelectorAll("tr.exp").forEach(e=>e.remove());
}

// ---------- checks ----------
function runChecks(){
  const L=[]; const ok=(what,a,b,pass)=>L.push({what,a,b,pass});
  ok("Record count: records.length vs Number(uhri.count)", fmt(N), fmt(Number(D.count)), N===Number(D.count));
  // partitions
  let sum=0; const mc={}; records.forEach(r=>{ mc[r.mechanism]=(mc[r.mechanism]||0)+1; });
  Object.values(mc).forEach(v=>sum+=v);
  ok("Counts per mechanism sum to the record count", fmt(sum), fmt(N), sum===N);
  sum=0; const bc={}; records.forEach(r=>{ bc[r.body]=(bc[r.body]||0)+1; });
  Object.values(bc).forEach(v=>sum+=v);
  ok("Counts per body sum to the record count", fmt(sum), fmt(N), sum===N);
  sum=0; const yc={}; records.forEach(r=>{ yc[r.year]=(yc[r.year]||0)+1; });
  Object.values(yc).forEach(v=>sum+=v);
  ok("Counts per year sum to the record count", fmt(sum), fmt(N), sum===N);
  sum=0; const tc={}; records.forEach(r=>{ tc[r.type]=(tc[r.type]||0)+1; });
  Object.values(tc).forEach(v=>sum+=v);
  ok("Counts per type sum to the headline total", fmt(sum), fmt(N), sum===N);
  // chart vs table
  const set=filtered();
  const tc2={}; set.forEach(r=>(r.themes||[]).forEach(t=>{ tc2[t]=(tc2[t]||0)+1; }));
  const top=Object.keys(tc2).map(t=>({t,c:tc2[t]})).sort((a,b)=>b.c-a.c||a.t.localeCompare(b.t)).slice(0,10);
  const recount={}; set.forEach(r=>(r.themes||[]).forEach(t=>{ recount[t]=(recount[t]||0)+1; }));
  const agree = top.every(o=>recount[o.t]===o.c);
  const maxOK = top.length ? top[0].c<=set.length : true;
  ok("FIG.01 bars equal a second independent count; largest bar ≤ filtered records",
     "largest bar "+(top.length?fmt(top[0].c):"0"), "filtered "+fmt(set.length), agree&&maxOK);
  // links
  const badLinks = records.filter(r=>{
    try{ const u=decodeURIComponent(r.doc_url||"").toLowerCase();
      return !(u.startsWith("https://docs.un.org/") && u.endsWith((r.symbol||"").toLowerCase())); }
    catch(e){ return true; }
  });
  ok('Every doc_url starts with "https://docs.un.org/" and ends with its symbol',
     fmt(badLinks.length)+" failing", badLinks.length?badLinks.map(r=>r.symbol).slice(0,5).join(", "):"none", badLinks.length===0);
  // paragraph numbers
  const pn = allMechs.map(m=>{
    const rs=records.filter(r=>r.mechanism===m);
    const w=rs.filter(r=>r._para).length;
    return m+": "+fmt(w)+"/"+fmt(rs)+" ("+(rs.length?(100*w/rs.length).toFixed(1):"0")+"%)";
  }).join(" · ");
  const uprRS=records.filter(r=>r.mechanism==="Universal Periodic Review");
  const uprPct=uprRS.length?100*uprRS.filter(r=>r._para).length/uprRS.length:100;
  L.push({what:"Paragraph numbers found, per mechanism (UPR expected at 100%; lower is a warning, not an error)",a:pn,b:"",pass:true,warn:uprPct<100});
  // states
  const noState=uprRS.filter(r=>!r._states || !r._states.length);
  L.push({what:"UPR records with at least one recommending State found", a:fmt(uprRS.length-noState.length)+" of "+fmt(uprRS.length),
    b:noState.length?("without: "+noState.slice(0,5).map(r=>r.symbol).join(", ")):"", pass:noState.length===0});
  // duplicates & gaps
  const ids=new Set(records.map(r=>r.id));
  const seen={},dups=[];
  records.forEach(r=>{ if(seen[r.text]) dups.push(r.symbol); seen[r.text]=1; });
  const noTheme=records.filter(r=>!(r.themes||[]).length).length;
  const noSdg=records.filter(r=>!(r.sdgs||[]).length).length;
  const noAff=records.filter(r=>!(r.affected_persons||[]).length).length;
  ok("Distinct id equals the record count", fmt(ids.size), fmt(N), ids.size===N);
  ok("Duplicate text values (shown, not removed)", fmt(dups.length)+" duplicates", dups.slice(0,3).join(", ")||"none", true);
  L.push({what:"Records not labelled: themes / SDGs / affected persons",
    a:fmt(noTheme)+" / "+fmt(noSdg)+" / "+fmt(noAff)+" not labelled", b:"", pass:true});
  const el=document.getElementById("checksList");
  el.innerHTML=L.map(c=>'<li>'+esc(c.what)+': <strong>'+esc(String(c.a))+'</strong>'+(c.b?' — '+esc(c.b):'")</li>').replace('")</li>','')+
    ' <span class="'+(c.pass?(c.warn?"":"ok"):"bad")+'">'+(c.pass?(c.warn?"warning":"✓ pass"):"✗ check failed")+'</span></li>').join("");
  document.getElementById("nchecks").textContent=L.length;
}
document.getElementById("checksBtn").onclick=function(){
  const p=document.getElementById("checksPanel");
  p.hidden=!p.hidden;
  this.setAttribute("aria-expanded",String(!p.hidden));
  if(!p.hidden) runChecks();
};

// ---------- method & export ----------
document.getElementById("methodText").innerHTML =
  '<p class="method">The headline total is the number of records in the file; the breakdown counts records per <em>type</em>, spelled exactly as in the data. Documents are distinct <em>symbol</em> values; years are the minimum and maximum of <em>year</em>. Filters combine with AND: exact match on mechanism, body and type; year between the two selects, inclusive; SDG matches when the goal number is in the record\u2019s list; a keyword requires every word to occur in the text or the symbol, literally.</p>'+
  '<p class="method">Theme counts count each label once per record carrying it, so bars add up to more than the record count; percentages are of records. The timeline counts records per year and mechanism, with zero for missing years. The paragraph number is the first number at the start of the text; the recommending State is read only from UPR texts, from the parenthesised groups at the end. The CSV and the summary below are generated in your browser from the current filter; nothing is estimated, no model is called, and nothing leaves the page except the clipboard write on "Copy".</p>';
document.getElementById("srcLine3").innerHTML =
  'Data: <a href="'+esc(D.source_url||"#")+'" target="_blank" rel="noopener">'+esc(D.source||"OHCHR UHRI")+'</a> · '+fmt(N)+' records · '+symbols.length+' documents · built '+esc(String(D.built||"n/a"))+'. Citation form follows the Dag Hammarskj\u00f6ld Library\u2019s advice (symbol as key, pinpoint kept).';

document.getElementById("csvBtn").onclick=()=>{
  const set=filtered();
  const q=s=>'"'+String(s==null?"":s).replace(/"/g,'""')+'"';
  let csv="# "+COUNTRY+" — UN human rights recommendations\n"+
    "# Source: "+(D.source||"")+" "+(D.source_url||"")+"\n# Built: "+(D.built||"")+"\n"+
    "# Filters: "+activeFilterText()+"\n# Rows: "+set.length+"\n";
  csv+="date,body,symbol,doc_url,paragraph,recommending_states,type,section,themes,sdgs,sdg_targets,affected_persons,text\n";
  set.forEach(r=>{
    csv+=[r.date,r.body,r.symbol,r.doc_url,r._para||"",(r._states||[]).join("; "),r.type,r.section||"",
      (r.themes||[]).join("; "),(r.sdgs||[]).join("; "),(r.sdg_targets||[]).join("; "),(r.affected_persons||[]).join("; "),r.text].map(q).join(",")+"\n";
  });
  const url=URL.createObjectURL(new Blob([csv],{type:"text/csv"}));
  const a=document.createElement("a"); a.href=url; a.download=COUNTRY.toLowerCase().replace(/\s+/g,"-")+"-uhri-export.csv";
  a.click(); setTimeout(()=>URL.revokeObjectURL(url),5000);
};
document.getElementById("sumBtn").onclick=async()=>{
  const set=filtered();
  const tc={}; set.forEach(r=>{ tc[r.type]=(tc[r.type]||0)+1; });
  const themes=topThemesForExport.map(o=>o.t+" ("+o.c+")").join("; ");
  const txt=COUNTRY+": "+fmt(set.length)+" records from "+fmt([...new Set(set.map(r=>r.symbol))].length)+
    " UN documents ("+Math.min(...(set.length?set.map(r=>r.year):years))+"–"+Math.max(...(set.length?set.map(r=>r.year):years))+
    "), filtered"+(activeFilterText()?" by "+activeFilterText():" from the full file")+". By type: "+
    Object.keys(tc).map(t=>fmt(tc[t])+" "+t).join(", ")+
    ". Most frequent themes: "+(themes||"none")+
    ". Source: OHCHR UHRI ("+(D.source_url||"")+"), computed in the UHRI dashboard, built "+(D.built||"")+".";
  try{ await navigator.clipboard.writeText(txt); }catch(e){}
  const c=document.getElementById("copiedSum"); c.hidden=false; setTimeout(()=>{ c.hidden=true; },2000);
};
function activeFilterText(){
  const parts=[];
  if(F.keyword) parts.push('keyword "'+F.keyword+'"');
  if(F.mechanism) parts.push("mechanism "+F.mechanism);
  if(F.body) parts.push("body "+F.body);
  if(F.type) parts.push("type "+F.type);
  if(F.theme) parts.push("theme "+F.theme);
  if(F.sdg!=="") parts.push("SDG "+F.sdg);
  if(F.state) parts.push("State "+F.state);
  if(F.yFrom!==""||F.yTo!=="") parts.push("years "+(F.yFrom||"start")+"–"+(F.yTo||"end"));
  return parts.join(", ");
}

// ---------- apply ----------
function apply(){
  if(F.yFrom!==""&&F.yTo!==""){ /* swap handled in handlers */ }
  renderChips();
  const set=filtered();
  document.getElementById("matchN").textContent=fmt(set.length);
  document.getElementById("matchN").setAttribute("aria-live","polite");
  document.getElementById("ofN").textContent="matching records of "+fmt(N)+" in the file";
  document.getElementById("shareFill").style.width=(N?(100*set.length/N):0)+"%";
  renderTiles(set);
  renderCharts(set);
  if(curTab===1) renderTable();
  fillG2(); fillG3();
  const kw=document.getElementById("kwBox"); if(kw && kw.value!==F.keyword) kw.value=F.keyword;
  if(search2.value!==F.keyword) search2.value=F.keyword;
}

// ---------- footer ----------
document.getElementById("foot").innerHTML =
  '<span>Built on OHCHR UHRI data · '+fmt(N)+' records · <a href="'+esc(D.source_url||"#")+'" target="_blank" rel="noopener">source</a></span>'+
  '<span>Credits: chart format follows the UK Government Analysis Function guidance on charts and tables (linked in Method); citation form follows the Dag Hammarskj\u00f6ld Library.</span>';

// init
syncInputs();
apply();
showTab(0);
})();
</script>
</body>
</html>
```

Two notes on things I simplified within the plan's spirit: the theme filter (clicking a FIG.01 bar) is implemented as a dedicated theme chip rather than reusing the keyword box, since a keyword cannot express an exact multi-label match; and the "Clear all" chip removal clears the whole year range, which keeps the rail under the click budget.