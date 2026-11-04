I built the Kenya dashboard on the attached file, in four tabs: overview, records, check and method with export. The country, counts, years and States are all read from the data. No model is called and nothing leaves the browser except the clipboard copy.

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>UN human rights recommendations and observations</title>
<style>
:root{--paper:#f4f0e8;--ink:#1d1b18;--rule:#d9d2c3;--red:#9b2335;--mute:#5c564b}
*{box-sizing:border-box}
[hidden]{display:none!important}
body{margin:0;background:var(--paper);color:var(--ink);font:16px/1.5 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif}
:focus-visible{outline:3px solid var(--red);outline-offset:2px}
a{color:var(--ink);text-decoration-color:var(--red);text-underline-offset:2px}
a:hover{color:var(--red)}
.mono{font:11.5px/1.4 ui-monospace,Menlo,Consolas,monospace;text-transform:uppercase;letter-spacing:.08em;color:var(--mute)}
.hint{font:12px/1.4 ui-monospace,Menlo,Consolas,monospace;color:var(--mute)}
.serif{font-family:Georgia,"Times New Roman",serif}
.wrap{max-width:1320px;margin:0 auto;padding:0 20px}
header.top{padding:22px 0 14px;border-bottom:1px solid var(--rule)}
header.top h1{font:400 34px/1.15 Georgia,"Times New Roman",serif;margin:6px 0 8px}
.metaline{font-size:14px;color:var(--mute)}
.metaline a{color:var(--ink)}
nav[role=tablist]{display:flex;gap:4px;flex-wrap:wrap;border-bottom:1px solid var(--rule);margin-top:6px}
nav button{background:none;border:0;border-bottom:3px solid transparent;padding:12px 16px 9px;cursor:pointer;font:12px ui-monospace,Menlo,Consolas,monospace;letter-spacing:.08em;text-transform:uppercase;color:var(--mute)}
nav button[aria-selected=true]{color:var(--red);border-bottom-color:var(--red);font-weight:700}
.layout{display:grid;grid-template-columns:270px minmax(0,1fr);gap:32px;padding-top:20px;padding-bottom:30px}
aside#rail{position:sticky;top:10px;align-self:start;border-right:1px solid var(--rule);padding-right:22px}
.railhead{display:flex;justify-content:space-between;align-items:baseline}
.linkbtn{background:none;border:0;color:var(--red);text-decoration:underline;cursor:pointer;font:13px system-ui,sans-serif;padding:2px}
#bigN .num{font:400 52px/1 Georgia,serif;display:block;margin-top:8px}
#bigN .lbl{font-size:15px}
.bar{height:4px;background:var(--rule);margin:8px 0 10px}
.bar i{display:block;height:4px;background:var(--red);width:0}
#chips{display:flex;flex-wrap:wrap;gap:6px;margin:6px 0 14px;min-height:4px}
.chip{background:none;border:1px solid var(--red);color:var(--red);padding:1px 8px;font-size:13px;cursor:pointer;border-radius:12px}
.chip:hover{background:var(--red);color:#fff}
.sec{border-top:1px solid var(--rule)}
.sechead{width:100%;text-align:left;background:none;border:0;padding:11px 0;cursor:pointer;font:12px ui-monospace,Menlo,Consolas,monospace;letter-spacing:.08em;text-transform:uppercase;color:var(--ink);display:flex;justify-content:space-between}
.sechead[aria-expanded=true]{color:var(--red);font-weight:700}
.secbody{padding:0 0 14px}
.secbody label{display:block;font:11px ui-monospace,Menlo,monospace;text-transform:uppercase;letter-spacing:.06em;color:var(--mute);margin:10px 0 3px}
input[type=search],input[type=text],input[type=number],select{width:100%;font:15px system-ui,sans-serif;padding:7px 8px;border:1px solid #b9b09c;background:#fffdf8;color:var(--ink);border-radius:2px}
.yrs{display:grid;grid-template-columns:1fr 1fr;gap:8px}
button.btn{font:13px ui-monospace,Menlo,Consolas,monospace;letter-spacing:.04em;padding:8px 14px;border:1px solid var(--ink);background:var(--ink);color:var(--paper);cursor:pointer;border-radius:2px}
button.btn.alt{background:none;color:var(--ink)}
button.btn:hover{background:var(--red);border-color:var(--red);color:#fff}
button.btn[aria-pressed=true]{background:var(--red);border-color:var(--red);color:#fff}
h2.q{font:400 26px/1.2 Georgia,serif;margin:0 0 16px}
h3.fig{font:400 20px/1.25 Georgia,serif;margin:6px 0 4px}
.tiles{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:0;border-top:1px solid var(--rule);border-bottom:1px solid var(--rule)}
.tile{padding:14px 16px 12px 0;margin-right:16px}
.tile .big{font:400 46px/1.05 Georgia,serif;margin:4px 0}
.tile .sub{font-size:13px;color:var(--mute)}
.dot{display:inline-block;width:10px;height:10px;border-radius:50%;margin-right:6px;vertical-align:baseline}
.note{font:12px/1.45 ui-monospace,Menlo,Consolas,monospace;color:var(--mute);margin:6px 0 18px}
figure{margin:26px 0 0;padding-top:14px;border-top:1px solid var(--rule)}
.chartbox{position:relative;height:440px}
.chartbox.short{height:320px}
table{border-collapse:collapse;width:100%;font-size:15px}
caption{text-align:left;font:12px ui-monospace,Menlo,Consolas,monospace;color:var(--mute);padding:6px 0}
th{font:11px ui-monospace,Menlo,Consolas,monospace;letter-spacing:.06em;text-transform:uppercase;text-align:left;color:var(--mute);border-bottom:2px solid var(--ink);padding:6px 8px 6px 0;vertical-align:bottom}
td{border-bottom:1px solid var(--rule);padding:7px 8px 7px 0;vertical-align:top}
th.num,td.num{text-align:right;font-variant-numeric:tabular-nums}
.nw{white-space:nowrap}
tr.row{cursor:pointer}
tr.row:hover td{background:#ece6d8}
.rowbtn{background:none;border:0;text-align:left;font:inherit;color:inherit;cursor:pointer;padding:0}
.thbtn{background:none;border:0;font:inherit;text-transform:inherit;letter-spacing:inherit;color:var(--red);cursor:pointer;padding:0}
tr.detail td{background:#faf7f0;padding:16px 12px 18px 0}
.dwrap{display:grid;grid-template-columns:110px minmax(0,1fr);gap:16px}
.pnum{font:400 42px/1 Georgia,serif;color:var(--red);text-align:right}
.fulltext{white-space:pre-wrap;margin:0 0 12px;max-width:80ch}
dl.lab{margin:0 0 12px;display:grid;grid-template-columns:150px 1fr;gap:4px 12px;font-size:14px}
dl.lab dt{font:11px ui-monospace,Menlo,monospace;text-transform:uppercase;letter-spacing:.06em;color:var(--mute);padding-top:3px}
dl.lab dd{margin:0}
.tag{display:inline-block;border:1px solid var(--rule);background:#fffdf8;padding:0 7px;margin:0 4px 4px 0;font-size:13px;border-radius:10px}
.missing{color:var(--mute);font-style:italic}
mark{background:#f2d98d;color:var(--ink);padding:0 1px}
.copied{font:12px ui-monospace,monospace;color:var(--red);margin-left:8px}
.acts{display:flex;align-items:center;gap:14px;flex-wrap:wrap}
ul.checks{list-style:none;margin:0;padding:0}
ul.checks>li{display:grid;grid-template-columns:130px minmax(0,1fr);gap:12px;padding:10px 0;border-bottom:1px solid var(--rule)}
.mk{font:12px ui-monospace,Menlo,monospace;text-transform:uppercase;letter-spacing:.05em}
.mk.fail{color:var(--red);font-weight:700}
.mk.warn{color:var(--red)}
.mk.pass,.mk.info{color:var(--ink)}
.vals{font:12.5px/1.45 ui-monospace,Menlo,Consolas,monospace;color:var(--mute)}
details{margin-top:4px;font-size:14px}
summary{cursor:pointer;color:var(--red)}
details ul{margin:6px 0 0;padding-left:18px;max-height:260px;overflow:auto}
ol.cards{list-style:none;padding:0;margin:10px 0 0}
ol.cards>li{border-bottom:1px solid var(--rule);padding:8px 0}
.cardline{display:grid;grid-template-columns:28px auto 70px minmax(0,1fr) auto;gap:10px;align-items:baseline}
.cardbody{padding:10px 0 6px 38px}
.sample-tally{font:13px ui-monospace,Menlo,monospace;margin:12px 0 4px;padding:8px 0;border-top:1px solid var(--ink);border-bottom:1px solid var(--rule)}
.method p{max-width:75ch}
textarea#sumbox{width:100%;height:170px;font:13px/1.4 ui-monospace,Menlo,Consolas,monospace;background:#fffdf8;border:1px solid #b9b09c;padding:8px}
footer{border-top:1px solid var(--rule);padding:14px 0 30px}
.statelist{margin:10px 0 0;padding:12px 16px;border:1px solid var(--rule);background:#faf7f0}
.statelist ol{margin:6px 0 0;padding-left:22px;columns:2}
.searchbar{margin-bottom:10px}
@media(max-width:900px){.layout{grid-template-columns:1fr}aside#rail{position:static;border-right:0;padding-right:0}.dwrap{grid-template-columns:1fr}.pnum{text-align:left}ul.checks>li{grid-template-columns:1fr}.cardline{grid-template-columns:24px 1fr}}
</style>
</head>
<body>
<header class="top"><div class="wrap">
  <div class="mono" id="hLabel"></div>
  <h1 id="hTitle"></h1>
  <div class="metaline" id="hMeta"></div>
</div>
<div class="wrap"><nav role="tablist" aria-label="Dashboard sections" id="tabs">
  <button role="tab" id="tab0" aria-controls="p0" aria-selected="true">01 Overview</button>
  <button role="tab" id="tab1" aria-controls="p1" aria-selected="false" tabindex="-1">02 Records</button>
  <button role="tab" id="tab2" aria-controls="p2" aria-selected="false" tabindex="-1">03 Check</button>
  <button role="tab" id="tab3" aria-controls="p3" aria-selected="false" tabindex="-1">04 Method &amp; export</button>
</nav></div>
</header>

<div class="wrap layout">
<aside id="rail" aria-label="Filters">
  <div class="railhead"><span class="mono">Filters</span><button class="linkbtn" data-act="clear" id="clearBtn">Clear all</button></div>
  <div id="bigN" aria-live="polite"></div>
  <div class="bar" aria-hidden="true"><i id="shareBar"></i></div>
  <div id="chips" aria-label="Active filters"></div>
  <div id="secs">
    <div class="sec">
      <button class="sechead" data-act="sec" data-i="0" aria-expanded="false" aria-controls="sb0"><span>01 Keyword</span><span aria-hidden="true">+</span></button>
      <div class="secbody" id="sb0" hidden>
        <input type="search" id="kw1" autocomplete="off" aria-label="Keyword">
        <div class="hint" style="margin-top:4px">literal match, not synonyms</div>
      </div>
    </div>
    <div class="sec">
      <button class="sechead" data-act="sec" data-i="1" aria-expanded="false" aria-controls="sb1"><span>02 Mechanism, body, type</span><span aria-hidden="true">+</span></button>
      <div class="secbody" id="sb1" hidden>
        <label for="fMech">Mechanism</label><select id="fMech"></select>
        <label for="fBody">Body or mandate</label><select id="fBody"></select>
        <label for="fType">Type</label><select id="fType"></select>
        <div id="stateWrap"><label for="fState">Recommending State (UPR)</label><select id="fState"></select></div>
      </div>
    </div>
    <div class="sec">
      <button class="sechead" data-act="sec" data-i="2" aria-expanded="false" aria-controls="sb2"><span>03 Years and SDG</span><span aria-hidden="true">+</span></button>
      <div class="secbody" id="sb2" hidden>
        <div class="yrs"><div><label for="fFrom">Year from</label><select id="fFrom"></select></div><div><label for="fTo">Year to</label><select id="fTo"></select></div></div>
        <label for="fSdg">SDG</label><select id="fSdg"></select>
      </div>
    </div>
  </div>
</aside>

<main>
  <section id="p0" role="tabpanel" aria-labelledby="tab0">
    <h2 class="q">What has the UN said, how much, and when?</h2>
    <div class="tiles" id="tiles"></div>
    <div class="note">How this is computed: records = every record in the current filter, of any type; documents = distinct symbols; years = lowest and highest year.</div>
    <div class="tiles" id="mechTiles"></div>
    <div class="note">How this is computed: per mechanism, records and distinct symbols in the current filter; share = records / filtered records.</div>
    <div id="statesBox"></div>
    <figure>
      <div class="mono">FIG.01</div>
      <h3 class="fig" id="fig1title"></h3>
      <div class="hint">click a bar or a theme name = filter by that theme</div>
      <div class="chartbox" id="c1box"><canvas id="c1" role="img" aria-label="Horizontal bar chart of the ten most frequent themes; the same values are in the table below"></canvas></div>
      <div id="fig1empty" class="missing" hidden>No records match.</div>
      <table id="t1" style="margin-top:10px"><caption>Ten most frequent themes in the current filter</caption>
        <thead><tr><th scope="col">Theme</th><th scope="col" class="num">Records</th><th scope="col" class="num">% of filtered</th><th scope="col">Years</th></tr></thead><tbody></tbody></table>
      <div class="note">How this is computed: each theme on a record counts once; top ten by count, ties alphabetical; % = records with the theme / filtered records. A record can carry several themes, so the bars add up to more than n.</div>
      <div class="note">A wide or very old year range can point to a legacy label. Judge a sample in 03 Check. <span id="src1"></span></div>
    </figure>
    <figure>
      <div class="mono">FIG.02</div>
      <h3 class="fig" id="fig2title"></h3>
      <div class="chartbox short" id="c2box"><canvas id="c2" role="img" aria-label="Stacked bar chart of records per year by mechanism"></canvas></div>
      <div id="fig2empty" class="missing" hidden>No records match.</div>
      <div class="note">How this is computed: records per year of the document, per mechanism, in the current filter; years without records stay as gaps. <span id="src2"></span></div>
    </figure>
  </section>

  <section id="p1" role="tabpanel" aria-labelledby="tab1" hidden>
    <h2 class="q">Which paragraph says it, and in which UN document?</h2>
    <div class="searchbar"><input type="search" id="kw2" autocomplete="off" aria-label="Search records"><div class="hint" style="margin-top:4px">literal match, not synonyms · same box as 01 Keyword</div></div>
    <table id="t2"><caption id="cap2"></caption>
      <thead><tr><th scope="col" id="thDate" aria-sort="descending"><button class="thbtn" data-act="sortdate" id="sortBtn">Date ▼</button></th><th scope="col">Body</th><th scope="col">Symbol</th><th scope="col" class="num">Para.</th><th scope="col">First line <span style="text-transform:none">(click = open)</span></th><th scope="col">Recommending State</th></tr></thead>
      <tbody id="tb2"></tbody></table>
    <div style="margin:14px 0"><button class="btn alt" data-act="more" id="moreBtn" hidden>Show 50 more</button></div>
    <div class="note" id="src3"></div>
  </section>

  <section id="p2" role="tabpanel" aria-labelledby="tab2" hidden>
    <h2 class="q">Can I trust these numbers?</h2>
    <div class="mono">How the app checks itself</div>
    <h3 class="fig">Check this dashboard</h3>
    <ul class="checks" id="checksBox"></ul>
    <h3 class="fig" style="margin-top:28px">Random-sample label check</h3>
    <div id="sampleBox"></div>
  </section>

  <section id="p3" role="tabpanel" aria-labelledby="tab3" hidden>
    <h2 class="q">How was this made, and how do I take it with me?</h2>
    <div class="method" id="methodText"></div>
    <div class="acts" style="margin:16px 0 6px">
      <button class="btn" data-act="csv" id="csvBtn">Download CSV of the current filter</button>
      <button class="btn alt" data-act="copysum" id="sumBtn">Copy summary</button>
      <span class="copied" id="sumStatus" role="status"></span>
    </div>
    <div class="hint" id="csvNote"></div>
    <label class="mono" for="sumbox" style="display:block;margin-top:16px">Summary that will be copied</label>
    <textarea id="sumbox" readonly></textarea>
    <p class="note" id="srcLine"></p>
  </section>
</main>
</div>

<footer><div class="wrap mono" id="foot"></div></footer>

<script>
(function(){
"use strict";
var D=(window.WORKSHOP_DATA&&window.WORKSHOP_DATA.uhri)||{};
var RAW=Array.isArray(D.records)?D.records:[];
var COUNTRY=D.country||"this country";
var SDGN=D.sdg_names||{};
var UPR="Universal Periodic Review";
var $=function(id){return document.getElementById(id)};
function esc(s){return String(s==null?"":s).replace(/[&<>"']/g,function(c){return {"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]})}
function fmt(n){return Number(n).toLocaleString("en-GB")}
function pct(a,b){return b?(100*a/b).toFixed(1)+"%":"–"}
function safeUrl(u){return /^https?:\/\//i.test(u||"")?u:""}

/* ---------- precompute ---------- */
var PARA=/^(\d{1,3}(?:\.\d{1,3})?)\.?\s/;
var TRAIL=/((?:\s*\((?:[^()]|\([^()]*\))*\))+)\s*[;.]?\s*$/;
var GRP=/\((?:[^()]|\([^()]*\))*\)/g;
function firstLine(t){if(t.length<=120)return t;var c=t.slice(0,120),i=c.lastIndexOf(" ");if(i>40)c=c.slice(0,i);return c.replace(/\s+$/,"")+"…"}
var R=RAW.map(function(r,i){
  var text=String(r.text==null?"":r.text),m=text.match(PARA),states=null;
  if(r.mechanism===UPR){
    var t=text.match(TRAIL);
    states=t?Array.prototype.map.call(t[1].match(GRP)||[],function(g){return g.slice(1,-1).trim()}).filter(function(s){return s&&s.indexOf(",")<0&&s.length<=60}):[];
  }
  return Object.assign({},r,{_i:i,_text:text,_para:m?m[1]:null,_states:states,_first:firstLine(text),
    _lc:(text+" "+(r.symbol||"")).toLowerCase(),
    _mech:r.mechanism||"(no mechanism)",_body:r.body||"(no body)",_type:r.type||"(no type)",
    themes:Array.isArray(r.themes)?r.themes:[],sdgs:Array.isArray(r.sdgs)?r.sdgs:[],
    sdg_targets:Array.isArray(r.sdg_targets)?r.sdg_targets:[],affected_persons:Array.isArray(r.affected_persons)?r.affected_persons:[]});
});
var N=R.length;
var YEARS=Array.from(new Set(R.map(function(r){return r.year}).filter(function(y){return typeof y==="number"}))).sort(function(a,b){return a-b});
var YMIN=YEARS.length?YEARS[0]:null,YMAX=YEARS.length?YEARS[YEARS.length-1]:null;
var PREF=[UPR,"Treaty bodies","Special Procedures"];
var MECHS=Array.from(new Set(R.map(function(r){return r._mech}))).sort(function(a,b){var x=PREF.indexOf(a),y=PREF.indexOf(b);x=x<0?9:x;y=y<0?9:y;return x-y||a.localeCompare(b)});
var MCOL={"Universal Periodic Review":"#c2410c","Treaty bodies":"#0f766e","Special Procedures":"#7c3aed"};
function mcol(m){return MCOL[m]||"#6b6459"}
var TYPES=Array.from(new Set(R.map(function(r){return r._type}))).sort();
var ANY_STATES=R.some(function(r){return r._states&&r._states.length});
var DOCS_ALL=new Set(R.map(function(r){return r.symbol})).size;

/* ---------- state ---------- */
var st,F=[],sig="",active=0,openSec=-1,showStates=false,dateDir=-1,page=50,expanded=new Set(),kwWords=[],kwT;
var sample=null,sampleSeed="1",verdict={},openCard=-1,chartA=null,chartB=null,lastFig=null,drawnSig=null;
function freshState(){return {kw:"",mech:"",body:"",type:"",state:"",yFrom:YMIN,yTo:YMAX,sdg:"",themes:[]}}
st=freshState();

/* ---------- header, footer ---------- */
function initHeader(){
  var su=safeUrl(D.source_url);
  var src=D.source?(su?'<a href="'+esc(su)+'" target="_blank" rel="noopener">'+esc(D.source)+'</a>':esc(D.source)):"UHRI";
  $("hLabel").textContent="UHRI · "+COUNTRY;
  $("hTitle").textContent="UN human rights recommendations and observations: "+COUNTRY;
  document.title="UN human rights recommendations: "+COUNTRY;
  $("hMeta").innerHTML="Source: "+src+" · "+fmt(N)+" records · "+fmt(DOCS_ALL)+" documents · "+(YMIN!=null?YMIN+"–"+YMAX:"years unknown")+(D.built?" · built "+esc(D.built):"")+' · <span class="hint">dated by document</span>';
  $("foot").innerHTML="Built on OHCHR UHRI data · "+fmt(N)+" records · "+(su?'<a href="'+esc(su)+'" target="_blank" rel="noopener">source</a>':"source: "+esc(D.source||"UHRI"));
  $("kw1").placeholder="e.g. torture";$("kw2").placeholder="Search "+fmt(N)+" records, e.g. torture";
}

/* ---------- filter controls ---------- */
function fillSel(sel,opts,val){sel.innerHTML=opts.map(function(o){return '<option value="'+esc(o.v)+'">'+esc(o.l)+"</option>"}).join("");sel.value=val}
function bodyOpts(mech){
  var c=new Map();R.forEach(function(r){if(!mech||r._mech===mech)c.set(r._body,(c.get(r._body)||0)+1)});
  var a=Array.from(c.entries()).sort(function(x,y){return y[1]-x[1]||x[0].localeCompare(y[0])});
  return [{v:"",l:"All bodies"}].concat(a.map(function(e){return {v:e[0],l:e[0]+" ("+fmt(e[1])+")"}}));
}
function stateCounts(arr){
  var c=new Map();arr.forEach(function(r){if(r._states)r._states.forEach(function(s){c.set(s,(c.get(s)||0)+1)})});
  return Array.from(c.entries()).sort(function(x,y){return y[1]-x[1]||x[0].localeCompare(y[0])});
}
function initControls(){
  var mc={},tc={};R.forEach(function(r){mc[r._mech]=(mc[r._mech]||0)+1;tc[r._type]=(tc[r._type]||0)+1});
  fillSel($("fMech"),[{v:"",l:"All mechanisms"}].concat(MECHS.map(function(m){return {v:m,l:m+" ("+fmt(mc[m])+")"}})),"");
  fillSel($("fType"),[{v:"",l:"All types"}].concat(TYPES.map(function(t){return {v:t,l:t+" ("+fmt(tc[t])+")"}})),"");
  fillSel($("fBody"),bodyOpts(""),"");
  if(ANY_STATES){fillSel($("fState"),[{v:"",l:"All States"}].concat(stateCounts(R).map(function(e){return {v:e[0],l:e[0]+" ("+fmt(e[1])+")"}})),"")}
  else $("stateWrap").hidden=true;
  var yo=YEARS.map(function(y){return {v:String(y),l:String(y)}});
  fillSel($("fFrom"),yo,String(YMIN));fillSel($("fTo"),yo,String(YMAX));
  var g=new Set();R.forEach(function(r){r.sdgs.forEach(function(x){g.add(Number(x))})});
  fillSel($("fSdg"),[{v:"",l:"All goals"}].concat(Array.from(g).sort(function(a,b){return a-b}).map(function(n){return {v:String(n),l:"SDG "+n+(SDGN[n]?": "+SDGN[n]:"")}})),"");
}
function syncControls(){
  $("kw1").value=st.kw;$("kw2").value=st.kw;$("fMech").value=st.mech;
  fillSel($("fBody"),bodyOpts(st.mech),st.body);$("fType").value=st.type;
  if(ANY_STATES)$("fState").value=st.state;
  if(YMIN!=null){$("fFrom").value=String(st.yFrom);$("fTo").value=String(st.yTo)}
  $("fSdg").value=st.sdg;
}
function yearActive(){return st.yFrom!==YMIN||st.yTo!==YMAX}

/* ---------- filtering ---------- */
function applyFilters(){
  var words=st.kw.trim().toLowerCase().split(/\s+/).filter(Boolean);kwWords=words;
  var ya=yearActive(),sd=st.sdg===""?null:Number(st.sdg);
  F=R.filter(function(r){
    if(st.mech&&r._mech!==st.mech)return false;
    if(st.body&&r._body!==st.body)return false;
    if(st.type&&r._type!==st.type)return false;
    if(st.state&&!(r._states&&r._states.indexOf(st.state)>=0))return false;
    if(ya&&!(typeof r.year==="number"&&r.year>=st.yFrom&&r.year<=st.yTo))return false;
    if(sd!==null&&r.sdgs.map(Number).indexOf(sd)<0)return false;
    for(var i=0;i<st.themes.length;i++)if(r.themes.indexOf(st.themes[i])<0)return false;
    for(var j=0;j<words.length;j++)if(r._lc.indexOf(words[j])<0)return false;
    return true;
  });
  sig=JSON.stringify(st);page=50;sample=null;verdict={};openCard=-1;
  render();
}
function describeFilters(){
  var a=[];
  if(st.kw.trim())a.push('keyword "'+st.kw.trim()+'"');
  if(st.mech)a.push("mechanism = "+st.mech);
  if(st.body)a.push("body = "+st.body);
  if(st.type)a.push("type = "+st.type);
  if(st.state)a.push("recommending State = "+st.state);
  if(yearActive())a.push("years "+st.yFrom+"–"+st.yTo);
  if(st.sdg!=="")a.push("SDG "+st.sdg);
  st.themes.forEach(function(t){a.push("theme = "+t)});
  return a;
}

/* ---------- stats helpers ---------- */
function stats(arr){
  var docs=new Set(),y0=null,y1=null;
  arr.forEach(function(r){docs.add(r.symbol);if(typeof r.year==="number"){if(y0===null||r.year<y0)y0=r.year;if(y1===null||r.year>y1)y1=r.year}});
  return {n:arr.length,docs:docs.size,y0:y0,y1:y1};
}
function typeCounts(arr){var c=new Map();arr.forEach(function(r){c.set(r._type,(c.get(r._type)||0)+1)});return Array.from(c.entries()).sort(function(a,b){return b[1]-a[1]||a[0].localeCompare(b[0])})}
function buildFig(arr){
  var m=new Map();
  arr.forEach(function(r){r.themes.forEach(function(t){var e=m.get(t);if(!e){e={theme:t,n:0,y0:null,y1:null};m.set(t,e)}e.n++;if(typeof r.year==="number"){if(e.y0===null||r.year<e.y0)e.y0=r.year;if(e.y1===null||r.year>e.y1)e.y1=r.year}})});
  var top=Array.from(m.values()).sort(function(a,b){return b.n-a.n||a.theme.localeCompare(b.theme)}).slice(0,10);
  top.forEach(function(e){e.pct=arr.length?(100*e.n/arr.length).toFixed(1):"0.0"});
  return {sig:sig,top:top,nFiltered:arr.length};
}
function cmpPara(a,b){
  var pa=a._para,pb=b._para;if(pa==null&&pb==null)return 0;if(pa==null)return 1;if(pb==null)return -1;
  var x=pa.split(".").map(Number),y=pb.split(".").map(Number);
  if(x[0]!==y[0])return x[0]-y[0];return (x[1]||0)-(y[1]||0);
}
function sortedRows(){
  return F.slice().sort(function(a,b){
    var c=dateDir*String(a.date||"").localeCompare(String(b.date||""));if(c)return c;
    c=String(a.body||"").localeCompare(String(b.body||""));if(c)return c;
    c=cmpPara(a,b);if(c)return c;return a._i-b._i;
  });
}
function hl(text){
  if(!kwWords.length)return esc(text);
  var ws=kwWords.slice().sort(function(a,b){return b.length-a.length}).map(function(w){return w.replace(/[.*+?^${}()|[\]\\]/g,"\\$&")});
  var re=new RegExp("("+ws.join("|")+")","gi");
  return text.split(re).map(function(p,i){return i%2?"<mark>"+esc(p)+"</mark>":esc(p)}).join("");
}
function cite(r){return r._para?r.symbol+", para. "+r._para:r.symbol}
function symLink(r){var u=safeUrl(r.doc_url);return u?'<a href="'+esc(u)+'" target="_blank" rel="noopener">'+esc(r.symbol)+"</a>":esc(r.symbol)}

/* ---------- render: rail ---------- */
function chip(k,v,label){return '<button class="chip" data-act="rm" data-k="'+k+'" data-v="'+esc(v||"")+'" aria-label="Remove filter '+esc(label)+'">'+esc(label)+" ×</button>"}
function renderRail(){
  $("bigN").innerHTML='<span class="num">'+fmt(F.length)+'</span><span class="lbl">matching records</span> <span class="hint">of '+fmt(N)+" in the file</span>";
  $("shareBar").style.width=(N?(100*F.length/N):0)+"%";
  var c=[];
  if(st.kw.trim())c.push(chip("kw","","Keyword: "+st.kw.trim()));
  if(st.mech)c.push(chip("mech","",st.mech));
  if(st.body)c.push(chip("body","","Body: "+st.body));
  if(st.type)c.push(chip("type","","Type: "+st.type));
  if(st.state)c.push(chip("state","","State: "+st.state));
  if(yearActive())c.push(chip("years","","Years: "+st.yFrom+"–"+st.yTo));
  if(st.sdg!=="")c.push(chip("sdg","","SDG "+st.sdg));
  st.themes.forEach(function(t){c.push(chip("theme",t,"Theme: "+t))});
  $("chips").innerHTML=c.join("");
  $("secs").hidden=active>1;
  [0,1,2].forEach(function(i){
    var b=document.querySelector('.sechead[data-i="'+i+'"]');b.setAttribute("aria-expanded",openSec===i);
    b.lastChild.textContent=openSec===i?"–":"+";$("sb"+i).hidden=openSec!==i;
  });
}

/* ---------- render: overview ---------- */
function tile(label,big,sub,dot){return '<div class="tile"><div class="mono">'+(dot?'<span class="dot" style="background:'+dot+'"></span>':"")+esc(label)+'</div><div class="big serif">'+big+'</div><div class="sub">'+sub+"</div></div>"}
function wrap(s,w){var words=String(s).split(" "),lines=[],cur="";words.forEach(function(x){if((cur+" "+x).trim().length>w&&cur){lines.push(cur);cur=x}else cur=(cur+" "+x).trim()});if(cur)lines.push(cur);return lines}
var valuePlugin={id:"valueEnd",afterDatasetsDraw:function(ch){
  var ctx=ch.ctx,meta=ch.getDatasetMeta(0);
  meta.data.forEach(function(bar,i){ctx.save();ctx.fillStyle="#1d1b18";ctx.font="13px ui-monospace,Menlo,Consolas,monospace";ctx.textBaseline="middle";ctx.fillText(fmt(ch.data.datasets[0].data[i]),bar.x+6,bar.y);ctx.restore()});
}};
function renderOverview(){
  var s=stats(F),tc=typeCounts(F);
  $("tiles").innerHTML=
    tile("Records",fmt(s.n),tc.length?tc.map(function(e){return fmt(e[1])+" "+esc(e[0])}).join(" · "):"no records")+
    tile("Documents",fmt(s.docs),"distinct UN document symbols")+
    tile("Years",s.y0!=null?s.y0+"–"+s.y1:"–","first and last year of the documents");
  var g={};MECHS.forEach(function(m){g[m]=[]});F.forEach(function(r){g[r._mech].push(r)});
  $("mechTiles").innerHTML=MECHS.map(function(m){
    var ms=stats(g[m]);
    var extra=(m===UPR&&ANY_STATES)?' · <button class="linkbtn" data-act="states" aria-expanded="'+showStates+'">'+(showStates?"hide the States":"see the States")+"</button>":"";
    return tile(m,fmt(ms.n),fmt(ms.docs)+" documents · latest "+(ms.y1!=null?ms.y1:"–")+" · "+pct(ms.n,s.n)+" of filtered"+extra,mcol(m));
  }).join("");
  var sb=$("statesBox");
  if(showStates&&ANY_STATES){
    var top=stateCounts(g[UPR]||[]).slice(0,10);
    sb.innerHTML='<div class="statelist"><div class="mono">Ten States that made most recommendations to '+esc(COUNTRY)+"</div>"+(top.length?"<ol>"+top.map(function(e){return "<li>"+esc(e[0])+' <span class="hint">'+fmt(e[1])+"</span></li>"}).join("")+"</ol>":'<p class="missing">No UPR records with a State in this filter.</p>')+'<div class="note" style="margin:6px 0 0">How this is computed: States named in the parentheses at the end of UPR texts, in the current filter; a line naming several States counts once for each. A count of recommendations, not of influence.</div></div>';
  }else sb.innerHTML="";
  var fig=buildFig(F);lastFig=fig;drawnSig=sig;
  var srcTxt="Source: "+(D.source||"UHRI")+"; "+COUNTRY+"; "+fmt(F.length)+" of "+fmt(N)+" records.";
  $("src1").textContent=srcTxt;$("src2").textContent=srcTxt;
  $("fig1title").textContent="Ten most frequent themes among "+fmt(F.length)+" filtered records";
  $("fig2title").textContent="Records per year by mechanism, "+fmt(F.length)+" filtered records";
  if(chartA){chartA.destroy();chartA=null}if(chartB){chartB.destroy();chartB=null}
  var empty=F.length===0;
  $("c1box").hidden=empty;$("c2box").hidden=empty;$("fig1empty").hidden=!empty;$("fig2empty").hidden=!empty;
  $("t1").querySelector("tbody").innerHTML=fig.top.map(function(e,i){
    return '<tr data-n="'+e.n+'"><td><button class="linkbtn" style="color:var(--ink);text-align:left" data-act="addtheme" data-ti="'+i+'">'+esc(e.theme)+'</button></td><td class="num">'+fmt(e.n)+'</td><td class="num">'+e.pct+'%</td><td class="nw">'+(e.y0!=null?(e.y0===e.y1?e.y0:e.y0+"–"+e.y1):"–")+"</td></tr>";
  }).join("")||'<tr><td colspan="4" class="missing">No themes in the filtered records.</td></tr>';
  if(empty||!window.Chart)return;
  chartA=new Chart($("c1"),{type:"bar",plugins:[valuePlugin],
    data:{labels:fig.top.map(function(e){return wrap(e.theme,36)}),datasets:[{data:fig.top.map(function(e){return e.n}),backgroundColor:"rgba(155,35,53,0.8)",borderWidth:0,barPercentage:.75}]},
    options:{indexAxis:"y",animation:false,responsive:true,maintainAspectRatio:false,layout:{padding:{right:50}},
      plugins:{legend:{display:false},tooltip:{callbacks:{title:function(it){return fig.top[it[0].dataIndex].theme}}}},
      scales:{x:{display:false,beginAtZero:true,grid:{display:false}},y:{grid:{display:false},ticks:{color:"#1d1b18",font:{size:12}}}},
      onClick:function(e,els){if(els.length)addTheme(fig.top[els[0].index].theme)},
      onHover:function(e,els){if(e.native&&e.native.target)e.native.target.style.cursor=els.length?"pointer":"default"}}});
  var yrs=[];for(var y=s.y0;y!==null&&y<=s.y1;y++)yrs.push(y);
  var cnt={};MECHS.forEach(function(m){cnt[m]={}});F.forEach(function(r){if(typeof r.year==="number")cnt[r._mech][r.year]=(cnt[r._mech][r.year]||0)+1});
  chartB=new Chart($("c2"),{type:"bar",
    data:{labels:yrs.map(String),datasets:MECHS.map(function(m){return {label:m,backgroundColor:mcol(m),data:yrs.map(function(y){return cnt[m][y]||0}),borderWidth:0}})},
    options:{animation:false,responsive:true,maintainAspectRatio:false,
      plugins:{legend:{position:"top",labels:{color:"#1d1b18"}}},
      scales:{x:{stacked:true,grid:{display:false},ticks:{color:"#1d1b18",maxRotation:0,autoSkip:true}},y:{stacked:true,beginAtZero:true,ticks:{precision:0,color:"#1d1b18"},grid:{color:"#e6dfd0"}}}}});
}
function addTheme(t){if(st.themes.indexOf(t)<0){st.themes.push(t);applyFilters()}}

/* ---------- render: records ---------- */
function stateCell(r){
  if(r._states===null)return "–";
  return r._states.length?r._states.map(esc).join("; "):'<span class="missing">State not found</span>';
}
function detailRow(r){
  var nopara=!r._para;
  var sdgs=r.sdgs.map(function(n){return '<span class="tag">SDG '+esc(n)+(SDGN[n]?": "+esc(SDGN[n]):"")+"</span>"}).join("");
  function list(a){return a.length?a.map(function(x){return '<span class="tag">'+esc(x)+"</span>"}).join(""):'<span class="missing">not labelled</span>'}
  return '<tr class="detail"><td colspan="6"><div class="dwrap"><div class="pnum serif" aria-label="Paragraph number">'+(r._para?esc(r._para):"–")+'</div><div>'
   +'<p class="fulltext">'+hl(r._text)+"</p>"
   +'<dl class="lab">'
   +(r.section?"<dt>Section</dt><dd>"+esc(r.section)+"</dd>":"")
   +"<dt>Themes</dt><dd>"+list(r.themes)+"</dd>"
   +"<dt>SDGs</dt><dd>"+(sdgs||'<span class="missing">not labelled</span>')+"</dd>"
   +"<dt>SDG targets</dt><dd>"+list(r.sdg_targets)+"</dd>"
   +"<dt>Affected persons</dt><dd>"+list(r.affected_persons)+"</dd>"
   +(r._states!==null?"<dt>Recommending State</dt><dd>"+stateCell(r)+"</dd>":"")
   +'</dl><div class="acts"><button class="btn" data-act="cite" data-i="'+r._i+'">Copy citation'+(nopara?" (no paragraph number in this extract)":"")+'</button><span class="copied" role="status"></span>'
   +(safeUrl(r.doc_url)?'<a href="'+esc(r.doc_url)+'" target="_blank" rel="noopener">Open the UN document</a>':"")
   +"</div></div></div></td></tr>";
}
function renderRecords(){
  var rows=sortedRows(),show=rows.slice(0,page);
  $("sortBtn").textContent="Date "+(dateDir<0?"▼":"▲");
  $("thDate").setAttribute("aria-sort",dateDir<0?"descending":"ascending");
  $("cap2").textContent=F.length?"Showing "+fmt(show.length)+" of "+fmt(F.length)+" matching records, "+(dateDir<0?"newest first":"oldest first")+". Click the Date header to reverse.":"No records match this filter.";
  $("tb2").innerHTML=show.map(function(r){
    var open=expanded.has(r._i);
    return '<tr class="row" data-row="'+r._i+'"><td class="nw">'+esc(r.date||"")+"</td><td>"+esc(r.body||"")+'</td><td class="nw">'+symLink(r)+'</td><td class="num">'+(r._para?esc(r._para):"–")+'</td><td><button class="rowbtn" aria-expanded="'+open+'">'+hl(r._first)+"</button></td><td>"+stateCell(r)+"</td></tr>"+(open?detailRow(r):"");
  }).join("");
  $("moreBtn").hidden=rows.length<=page;
  $("src3").textContent="Source: "+(D.source||"UHRI")+"; "+COUNTRY+". Date is the date of the UN document, not of the recommendation. Paragraph numbers are read from the start of the text.";
}

/* ---------- checks ---------- */
function linkList(rs){
  if(!rs.length)return "";
  var shown=rs.slice(0,200);
  return '<details><summary>List the '+fmt(rs.length)+" records</summary><ul>"+shown.map(function(r){return "<li>"+symLink(r)+(r._para?", para. "+esc(r._para):"")+' <span class="hint">'+esc(r._text.slice(-90))+"</span></li>"}).join("")+(rs.length>200?"<li>… and "+fmt(rs.length-200)+" more</li>":"")+"</ul></details>";
}
function partition(field,label){
  var present=0;R.forEach(function(r){if(r[field]!==undefined&&r[field]!==null&&r[field]!=="")present++});
  var c=new Map();R.forEach(function(r){var v=r[field];if(v!==undefined&&v!==null&&v!=="")c.set(v,(c.get(v)||0)+1)});
  var sum=0;c.forEach(function(v){sum+=v});
  return {title:"Partition by "+label,ok:sum===N,vals:c.size+" groups sum to "+fmt(sum)+" · records "+fmt(N)+(sum!==N?" ("+fmt(N-sum)+" records have no "+label+")":"")};
}
function runChecks(){
  var out=[];
  var cn=Number(D.count);
  out.push({t:"Record count",ok:cn===N,v:"records.length = "+fmt(N)+" · count in the file = "+(isNaN(cn)?esc(D.count):fmt(cn))});
  ["mechanism","body","year"].forEach(function(f){var p=partition(f,f);out.push({t:p.title,ok:p.ok,v:p.vals})});
  var ts=0;typeCounts(F).forEach(function(e){ts+=e[1]});
  out.push({t:"Type partition (current filter)",ok:ts===F.length,v:"counts per type sum to "+fmt(ts)+" · headline total "+fmt(F.length)});
  // chart vs table
  var fig,src;
  if(drawnSig===sig&&lastFig&&lastFig.sig===sig){fig=lastFig;src="values read from the drawn chart and table"}else{fig=buildFig(F);src="recomputed: tab 01 not drawn for this filter yet"}
  var cnt={};for(var i=0;i<F.length;i++){var th=F[i].themes;for(var j=0;j<th.length;j++)cnt[th[j]]=(cnt[th[j]]||0)+1}
  var barVals=(drawnSig===sig&&chartA)?chartA.data.datasets[0].data.slice():fig.top.map(function(e){return e.n});
  var tblVals=(drawnSig===sig)?Array.prototype.map.call(document.querySelectorAll("#t1 tbody tr[data-n]"),function(tr){return Number(tr.dataset.n)}):fig.top.map(function(e){return e.n});
  var bad=[],mx=0;
  fig.top.forEach(function(e,k){var ex=cnt[e.theme]||0;if(barVals[k]!==ex||tblVals[k]!==ex)bad.push(e.theme+": bar "+barVals[k]+", table "+tblVals[k]+", recount "+ex);if(ex>mx)mx=ex});
  out.push({t:"Chart against table",ok:!bad.length&&mx<=F.length&&barVals.length===tblVals.length,v:fig.top.length+" bars checked; largest "+fmt(mx)+" ≤ filtered "+fmt(F.length)+" · "+src+(bad.length?" · "+esc(bad.join("; ")):"")});
  // links
  var badLinks=R.filter(function(r){
    var u=r.doc_url||"";if(u.indexOf("https://docs.un.org/")!==0)return true;
    var d=u;try{d=decodeURIComponent(u)}catch(e){}
    return d.toLowerCase().slice(-String(r.symbol||"").length)!==String(r.symbol||"").toLowerCase()||!r.symbol;
  });
  out.push({t:"Links to UN documents",ok:!badLinks.length,v:fmt(N-badLinks.length)+" of "+fmt(N)+" doc_url start with https://docs.un.org/ and end with the symbol",extra:linkList(badLinks)});
  // paragraph numbers
  var pp=MECHS.map(function(m){var a=R.filter(function(r){return r._mech===m}),k=a.filter(function(r){return r._para}).length;return {m:m,k:k,n:a.length}});
  var upr=pp.filter(function(p){return p.m===UPR})[0];
  out.push({t:"Paragraph numbers found",ok:true,warn:!!(upr&&upr.k<upr.n),v:pp.map(function(p){return esc(p.m)+": "+pct(p.k,p.n)+" ("+fmt(p.k)+" of "+fmt(p.n)+")"}).join(" · ")+(upr?" · UPR expected 100%":"")});
  // states
  var uprs=R.filter(function(r){return r._states!==null}),noSt=uprs.filter(function(r){return !r._states.length});
  out.push({t:"Recommending States found",ok:true,warn:noSt.length>0,v:fmt(uprs.length-noSt.length)+" of "+fmt(uprs.length)+" UPR records have at least one State"+(noSt.length?" · "+fmt(noSt.length)+" without (see the list)":""),extra:linkList(noSt)});
  // duplicates, gaps
  var ids=new Set(R.map(function(r){return r.id}));
  out.push({t:"Distinct ids",ok:ids.size===N,v:fmt(ids.size)+" distinct ids · records "+fmt(N)});
  var tm=new Map();R.forEach(function(r){tm.set(r._text,(tm.get(r._text)||0)+1)});
  var dup=0;tm.forEach(function(v){if(v>1)dup++});
  out.push({t:"Duplicate texts",ok:true,info:true,v:fmt(dup)+" texts appear more than once; they are kept"});
  out.push({t:"Not labelled",ok:true,info:true,v:"no themes: "+fmt(R.filter(function(r){return !r.themes.length}).length)+" · no SDGs: "+fmt(R.filter(function(r){return !r.sdgs.length}).length)+" · no affected persons: "+fmt(R.filter(function(r){return !r.affected_persons.length}).length)+" (shown as not labelled)"});
  return out;
}
function renderChecks(){
  $("checksBox").innerHTML=runChecks().map(function(c){
    var cls=!c.ok?"fail":c.warn?"warn":c.info?"info":"pass",lab={fail:"✗ check failed",warn:"⚠ warning",info:"i note",pass:"✓ pass"}[cls];
    return '<li><span class="mk '+cls+'">'+lab+'</span><div><strong>'+esc(c.t)+'</strong><div class="vals">'+(c.v.indexOf("<")>=0||c.v.indexOf("&")>=0?c.v:esc(c.v))+"</div>"+(c.extra||"")+"</div></li>";
  }).join("");
}
function mulberry32(a){return function(){a|=0;a=a+0x6D2B79F5|0;var t=Math.imul(a^a>>>15,1|a);t=t+Math.imul(t^t>>>7,61|t)^t;return((t^t>>>14)>>>0)/4294967296}}
function draw(seed){
  var s=parseInt(seed,10);if(isNaN(s))s=1;sampleSeed=String(s);
  var pool=F.slice(),rng=mulberry32(s);
  for(var i=pool.length-1;i>0;i--){var j=Math.floor(rng()*(i+1));var t=pool[i];pool[i]=pool[j];pool[j]=t}
  sample=pool.slice(0,10);verdict={};openCard=-1;renderSample();
}
function renderSample(){
  var b=$("sampleBox");
  var intro='<p class="note" style="margin-top:0">This is your judgement of the UN\'s labels; nothing is sent anywhere. Ten records are drawn from the current filter ('+fmt(F.length)+' matching); each card asks whether the themes as a set fit the paragraph.</p>';
  if(!F.length){b.innerHTML=intro+'<p class="missing">No records match: nothing to draw.</p>';return}
  if(!sample){b.innerHTML=intro+'<button class="btn" data-act="draw-random">Check 10 at random</button>';return}
  var c={fit:0,no:0,un:0};Object.keys(verdict).forEach(function(k){c[verdict[k]]++});
  var judged=c.fit+c.no+c.un;
  b.innerHTML=intro+'<div class="acts"><button class="btn" data-act="draw-random" id="again">Draw again</button><label class="mono" for="seedBox">Seed</label><input type="text" id="seedBox" style="width:110px" value="'+esc(sampleSeed)+'" inputmode="numeric"><button class="btn alt" data-act="draw-seed">Draw with this seed</button></div>'
   +'<div class="sample-tally" aria-live="polite">Themes: '+c.fit+" fit, "+c.no+" don't, "+c.un+" unsure; "+judged+" of "+sample.length+" judged · seed "+esc(sampleSeed)+" · your judgement, not a UN label</div>"
   +'<ol class="cards">'+sample.map(function(r,k){
     var v=verdict[r._i],open=openCard===k;
     var vl=v==="fit"?"Fits":v==="no"?"Doesn't fit":v==="un"?"Unsure":"";
     var body=open?'<div class="cardbody"><p class="fulltext">'+esc(r._text)+'</p><div class="mono" style="margin-bottom:4px">Themes given by the UN</div><div>'+(r.themes.length?r.themes.map(function(t){return '<span class="tag">'+esc(t)+"</span>"}).join(""):'<span class="missing">not labelled</span>')+'</div><div class="acts" style="margin-top:8px">'
       +[["fit","Fits"],["no","Doesn't fit"],["un","Unsure"]].map(function(x){return '<button class="btn alt" id="v-'+r._i+'-'+x[0]+'" data-act="verdict" data-i="'+r._i+'" data-v="'+x[0]+'" aria-pressed="'+(v===x[0])+'">'+x[1]+"</button>"}).join("")+"</div></div>":"";
     return "<li><div class=\"cardline\"><span class=\"mono\">"+(k+1)+"</span><span>"+symLink(r)+'</span><span class="hint">'+(r._para?"para. "+esc(r._para):"no para.")+'</span><button class="rowbtn" id="c-'+k+'" data-act="card" data-k="'+k+'" aria-expanded="'+open+'">'+esc(r._first)+'</button><span class="mono" style="color:var(--red)">'+vl+"</span></div>"+body+"</li>";
   }).join("")+"</ol>";
}

/* ---------- method & export ---------- */
function summaryText(){
  var s=stats(F),fig=buildFig(F),tc=typeCounts(F),f=describeFilters(),g={};
  F.forEach(function(r){g[r._mech]=(g[r._mech]||0)+1});
  return "UHRI, "+COUNTRY+": "+fmt(F.length)+" matching records (of "+fmt(N)+" in the file) from "+fmt(s.docs)+" UN documents, "+(s.y0!=null?s.y0+"–"+s.y1:"years unknown")+". "
   +"Filters: "+(f.length?f.join("; "):"none")+". "
   +"By type: "+(tc.map(function(e){return fmt(e[1])+" "+e[0]}).join(", ")||"none")+". "
   +"By mechanism: "+(MECHS.filter(function(m){return g[m]}).map(function(m){return fmt(g[m])+" "+m}).join(", ")||"none")+". "
   +"Ten most frequent themes (a record can carry several): "+(fig.top.map(function(e,i){return (i+1)+". "+e.theme+" ("+fmt(e.n)+", "+e.pct+"%, "+(e.y0===e.y1?e.y0:e.y0+"–"+e.y1)+")"}).join("; ")||"none")+". "
   +"Source: "+(D.source||"UHRI")+(D.built?", built "+D.built:"")+". Dates are the dates of the UN documents.";
}
function renderMethod(){
  var su=safeUrl(D.source_url);
  $("methodText").innerHTML="<p>Every number is a loop over the records in your browser. Nothing is estimated, no model is called, and nothing leaves the page except the clipboard when you press Copy.</p>"
   +"<p>All filters combine with AND. A keyword matches only if every word occurs, as typed, inside the text or the symbol: it is literal, so “torture” does not find “ill-treatment”.</p>"
   +"<p>Themes: each theme on a record counts once. The ten most frequent are shown with the share of filtered records and the first and last year of the records that carry them. A record can carry several themes, so counts add up to more than the records.</p>"
   +"<p>The paragraph number is the number at the very start of the text (“71” or “144.43”); where none is there, none is shown. The recommending State is read from the parentheses at the end of a Universal Periodic Review text, only for those records, and only if the group has no comma and at most 60 characters.</p>"
   +"<p>Themes, SDGs and affected persons are the UN’s own labels. The app never changes them; the sample in 03 Check lets you judge them. Dates are the dates of the documents, not of the recommendations.</p>"
   +"<p>A citation is the symbol and the paragraph, for example “"+esc(F[0]?cite(F[0]):"SYMBOL, para. N")+"”.</p>";
  $("csvNote").textContent="The CSV holds the "+fmt(F.length)+" rows of the current filter: the table columns plus full text and labels, with comment lines on top (country, source, build date, filters, row count).";
  $("sumbox").value=summaryText();
  $("srcLine").innerHTML="Data source: "+(su?'<a href="'+esc(su)+'" target="_blank" rel="noopener">'+esc(D.source||su)+"</a>":esc(D.source||"UHRI"))+(D.built?" · built "+esc(D.built):"")+" · licence: not stated in the file; see the terms at the source.";
}
function csvCell(v){var s=String(v==null?"":v);return /[",\n\r]/.test(s)?'"'+s.replace(/"/g,'""')+'"':s}
function downloadCsv(){
  var f=describeFilters(),rows=sortedRows();
  var lines=["# Country: "+COUNTRY,"# Source: "+(D.source||"UHRI")+(D.source_url?" ("+D.source_url+")":""),"# Built: "+(D.built||"unknown"),"# Filters: "+(f.length?f.join("; "):"none"),"# Rows: "+rows.length+" of "+N,"# Date is the date of the UN document."];
  lines.push(["date","body","mechanism","type","symbol","doc_url","paragraph","recommending_states","section","text","themes","sdgs","sdg_targets","affected_persons"].join(","));
  rows.forEach(function(r){lines.push([r.date,r.body,r.mechanism,r.type,r.symbol,r.doc_url,r._para||"",r._states?r._states.join(" | "):"",r.section||"",r._text,r.themes.join(" | "),r.sdgs.join(" | "),r.sdg_targets.join(" | "),r.affected_persons.join(" | ")].map(csvCell).join(","))});
  var blob=new Blob(["\uFEFF"+lines.join("\n")],{type:"text/csv;charset=utf-8"});
  var url=URL.createObjectURL(blob),a=document.createElement("a");
  a.href=url;a.download="uhri-"+String(COUNTRY).toLowerCase().replace(/[^a-z0-9]+/g,"-")+"-filtered.csv";
  document.body.appendChild(a);a.click();a.remove();setTimeout(function(){URL.revokeObjectURL(url)},4000);
}
async function copyText(t){
  try{await navigator.clipboard.writeText(t);return true}catch(e){
    try{var ta=document.createElement("textarea");ta.value=t;ta.style.position="fixed";ta.style.opacity="0";document.body.appendChild(ta);ta.select();var ok=document.execCommand("copy");ta.remove();return ok}catch(e2){return false}
  }
}
function flash(el,ok){if(!el)return;el.textContent=ok?"Copied":"Copy failed: select the text by hand";setTimeout(function(){el.textContent=""},2000)}

/* ---------- main render & tabs ---------- */
function render(){
  renderRail();
  if(active===0)renderOverview();
  else if(active===1)renderRecords();
  else if(active===2){renderChecks();renderSample()}
  else renderMethod();
}
var tabs=[0,1,2,3].map(function(i){return $("tab"+i)}),panels=[0,1,2,3].map(function(i){return $("p"+i)});
function showTab(i,focus){
  active=i;
  tabs.forEach(function(t,k){t.setAttribute("aria-selected",k===i);t.tabIndex=k===i?0:-1;panels[k].hidden=k!==i});
  if(focus)tabs[i].focus();render();
}
tabs.forEach(function(t,i){
  t.addEventListener("click",function(){showTab(i,false)});
  t.addEventListener("keydown",function(e){
    var k=null;
    if(e.key==="ArrowRight")k=(i+1)%4;else if(e.key==="ArrowLeft")k=(i+3)%4;else if(e.key==="Home")k=0;else if(e.key==="End")k=3;
    if(k!==null){e.preventDefault();showTab(k,true)}
  });
});

/* ---------- events ---------- */
document.addEventListener("click",function(e){
  var a=e.target.closest("[data-act]");
  if(a){
    var act=a.dataset.act;
    if(act==="sec"){var i=Number(a.dataset.i);openSec=openSec===i?-1:i;renderRail();return}
    if(act==="clear"){st=freshState();syncControls();applyFilters();return}
    if(act==="rm"){
      var k=a.dataset.k;
      if(k==="kw")st.kw="";else if(k==="mech"){st.mech="";}else if(k==="body")st.body="";else if(k==="type")st.type="";else if(k==="state")st.state="";
      else if(k==="years"){st.yFrom=YMIN;st.yTo=YMAX}else if(k==="sdg")st.sdg="";else if(k==="theme")st.themes=st.themes.filter(function(t){return t!==a.dataset.v});
      syncControls();applyFilters();return;
    }
    if(act==="states"){showStates=!showStates;renderOverview();return}
    if(act==="addtheme"){var fg=lastFig&&lastFig.top[Number(a.dataset.ti)];if(fg)addTheme(fg.theme);return}
    if(act==="sortdate"){dateDir=-dateDir;renderRecords();return}
    if(act==="more"){page+=50;renderRecords();return}
    if(act==="cite"){var r=R[Number(a.dataset.i)];copyText(cite(r)).then(function(ok){flash(a.parentNode.querySelector(".copied"),ok)});return}
    if(act==="draw-random"){draw(Math.floor(Math.random()*999999)+1);return}
    if(act==="draw-seed"){draw($("seedBox").value);return}
    if(act==="card"){var kk=Number(a.dataset.k);openCard=openCard===kk?-1:kk;renderSample();var cb=$("c-"+kk);if(cb)cb.focus();return}
    if(act==="verdict"){verdict[a.dataset.i]=a.dataset.v;renderSample();var vb=$("v-"+a.dataset.i+"-"+a.dataset.v);if(vb)vb.focus();return}
    if(act==="csv"){downloadCsv();return}
    if(act==="copysum"){copyText($("sumbox").value).then(function(ok){flash($("sumStatus"),ok)});return}
  }
  if(e.target.closest("a"))return;
  var tr=e.target.closest("tr[data-row]");
  if(tr){var id=Number(tr.dataset.row);if(expanded.has(id))expanded.delete(id);else expanded.add(id);renderRecords();var nb=document.querySelector('tr[data-row="'+id+'"] .rowbtn');if(nb&&e.detail===0)nb.focus()}
});
document.addEventListener("input",function(e){if(e.target.id==="seedBox")sampleSeed=e.target.value});
["kw1","kw2"].forEach(function(id){
  $(id).addEventListener("input",function(e){
    var v=e.target.value;clearTimeout(kwT);
    kwT=setTimeout(function(){var o=$(id==="kw1"?"kw2":"kw1");if(o.value!==v)o.value=v;st.kw=v.trim();applyFilters()},300);
  });
});
$("fMech").addEventListener("change",function(e){st.mech=e.target.value;var ok=bodyOpts(st.mech).some(function(o){return o.v===st.body});if(!ok)st.body="";fillSel($("fBody"),bodyOpts(st.mech),st.body);applyFilters()});
$("fBody").addEventListener("change",function(e){st.body=e.target.value;applyFilters()});
$("fType").addEventListener("change",function(e){st.type=e.target.value;applyFilters()});
$("fState").addEventListener("change",function(e){st.state=e.target.value;applyFilters()});
$("fSdg").addEventListener("change",function(e){st.sdg=e.target.value;applyFilters()});
function yearChange(){
  var a=Number($("fFrom").value),b=Number($("fTo").value);
  if(a>b){var t=a;a=b;b=t;$("fFrom").value=String(a);$("fTo").value=String(b)}
  st.yFrom=a;st.yTo=b;applyFilters();
}
$("fFrom").addEventListener("change",yearChange);$("fTo").addEventListener("change",yearChange);

/* ---------- start ---------- */
initHeader();initControls();applyFilters();
})();
</script>
</body>
</html>
```