I added the correction workflow to the Check tab, a switch under the title, and a new tab "04 Corrections" for undo, CSV download and CSV load. The UN's themes are never changed: your edits sit on top and every count, chart and filter follows the switch. Corrections exist only in the open page, so download the CSV to keep them.

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
.sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}
.wrap{max-width:1320px;margin:0 auto;padding:0 20px}
header.top{padding:22px 0 14px;border-bottom:1px solid var(--rule)}
header.top h1{font:400 34px/1.15 Georgia,"Times New Roman",serif;margin:6px 0 8px}
.metaline{font-size:14px;color:var(--mute)}
.metaline a{color:var(--ink)}
.corrrow{display:flex;gap:8px 22px;align-items:center;flex-wrap:wrap;margin:0 0 6px;font-size:15px}
#sw{display:inline-flex;align-items:center;gap:8px;background:none;border:0;cursor:pointer;font:12px ui-monospace,Menlo,Consolas,monospace;text-transform:uppercase;letter-spacing:.06em;color:var(--mute);padding:4px 2px}
#sw .trk{width:36px;height:18px;border:1px solid var(--ink);border-radius:10px;position:relative;background:#fffdf8;display:inline-block}
#sw .trk::after{content:"";position:absolute;top:2px;left:2px;width:12px;height:12px;border-radius:50%;background:var(--ink)}
#sw[aria-checked=true] .trk{background:var(--red);border-color:var(--red)}
#sw[aria-checked=true] .trk::after{left:20px;background:#fff}
#sw[aria-checked=true] .s1{color:var(--red);font-weight:700}
#sw[aria-checked=false] .s0{color:var(--ink);font-weight:700}
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
.btn{display:inline-block;font:13px ui-monospace,Menlo,Consolas,monospace;letter-spacing:.04em;padding:8px 14px;border:1px solid var(--ink);background:var(--ink);color:var(--paper);cursor:pointer;border-radius:2px;position:relative}
.btn.alt{background:none;color:var(--ink)}
.btn:hover{background:var(--red);border-color:var(--red);color:#fff}
.btn[aria-pressed=true]{background:var(--red);border-color:var(--red);color:#fff}
.btn:disabled{opacity:.45;cursor:not-allowed;background:none;color:var(--mute);border-color:var(--rule)}
.filebtn input{position:absolute;opacity:0;width:1px;height:1px;left:0;top:0}
.filebtn:focus-within{outline:3px solid var(--red);outline-offset:2px}
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
.tag{display:inline-block;border:1px solid var(--rule);background:#fffdf8;padding:0 7px;margin:0 4px 4px 0;font-size:13px;border-radius:10px;color:var(--ink)}
button.tag{font:inherit;font-size:13px;cursor:pointer;text-align:left}
button.tag:hover{border-color:var(--red)}
.tag.struck{color:var(--mute);border-style:dashed}
.tag.struck s{text-decoration:line-through;text-decoration-thickness:2px;text-decoration-color:var(--red)}
.tag.mine{background:#f6e3e6;border-color:var(--red);color:#6d1020;font-style:italic}
.corrtag{display:inline-block;font:10.5px/1.5 ui-monospace,Menlo,monospace;text-transform:uppercase;letter-spacing:.06em;color:var(--red);border:1px solid var(--red);padding:0 5px;margin-left:6px;border-radius:2px;white-space:nowrap}
.missing{color:var(--mute);font-style:italic}
mark{background:#f2d98d;color:var(--ink);padding:0 1px}
.copied{font:12px ui-monospace,monospace;color:var(--red);margin-left:8px}
.acts{display:flex;align-items:center;gap:10px 14px;flex-wrap:wrap}
.editor{margin-top:12px;padding:10px 12px;border-left:3px solid var(--red);background:#f8f2ea}
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
  <div class="corrrow">
    <span id="corrLine" aria-live="polite"></span>
    <button id="sw" role="switch" aria-checked="true" aria-label="Show labels with my corrections (off: the UN's own labels)" data-act="sw"><span class="s0">UN labels</span><span class="trk" aria-hidden="true"></span><span class="s1">with my corrections</span></button>
    <span class="hint" id="corrHint"></span>
  </div>
  <div class="metaline" id="hMeta"></div>
</div>
<div class="wrap"><nav role="tablist" aria-label="Dashboard sections" id="tabs">
  <button role="tab" id="tab0" aria-controls="p0" aria-selected="true">01 Overview</button>
  <button role="tab" id="tab1" aria-controls="p1" aria-selected="false" tabindex="-1">02 Records</button>
  <button role="tab" id="tab2" aria-controls="p2" aria-selected="false" tabindex="-1">03 Check</button>
  <button role="tab" id="tab3" aria-controls="p3" aria-selected="false" tabindex="-1">04 Corrections</button>
  <button role="tab" id="tab4" aria-controls="p4" aria-selected="false" tabindex="-1">05 Method &amp; export</button>
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
      <div class="note">How this is computed: each theme on a record counts once; top ten by count, ties alphabetical; % = records with the theme / filtered records. A record can carry several themes, so the bars add up to more than n. Counts follow the switch under the title.</div>
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
    <h2 class="q" id="corrTitle" tabindex="-1">What have I corrected?</h2>
    <p class="hint" id="corrIntro"></p>
    <table id="tCorr"><caption id="capCorr"></caption>
      <thead><tr><th scope="col">Symbol</th><th scope="col" class="num">Para.</th><th scope="col">UN's labels <span style="text-transform:none">(struck = removed by you; click = restore)</span></th><th scope="col">My labels <span style="text-transform:none">(italic = added by you; click = undo)</span></th><th scope="col">My mark</th><th scope="col">Undo</th></tr></thead>
      <tbody id="tbCorr"></tbody></table>
    <div class="acts" style="margin:16px 0 6px">
      <button class="btn" id="dlCorr" data-act="dlcorr">Download my corrections (CSV)</button>
      <label class="btn alt filebtn">Load corrections (CSV)<input type="file" id="corrFile" accept=".csv,text/csv,text/plain"></label>
      <button class="btn alt" id="undoAll" data-act="undoall">Undo all</button>
    </div>
    <div class="hint" role="status" id="corrMsg"></div>
    <div class="note">How this works: a correction removes a UN theme from your version of a record or adds one that occurs elsewhere in the data. The UN's themes stay in the file and in the CSV. Loading a CSV replaces your corrections for the records it names and keeps the others.</div>
  </section>

  <section id="p4" role="tabpanel" aria-labelledby="tab4" hidden>
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
var seenK=new Set();
var R=RAW.map(function(r,i){
  var text=String(r.text==null?"":r.text),m=text.match(PARA),states=null;
  if(r.mechanism===UPR){
    var t=text.match(TRAIL);
    states=t?Array.prototype.map.call(t[1].match(GRP)||[],function(g){return g.slice(1,-1).trim()}).filter(function(s){return s&&s.indexOf(",")<0&&s.length<=60}):[];
  }
  var key=(r.id!=null&&r.id!==""&&!seenK.has(String(r.id)))?String(r.id):"#"+i;seenK.add(key);
  var un=Array.isArray(r.themes)?r.themes.slice():[];
  return Object.assign({},r,{_i:i,_k:key,_text:text,_para:m?m[1]:null,_states:states,_first:firstLine(text),
    _lc:(text+" "+(r.symbol||"")).toLowerCase(),
    _mech:r.mechanism||"(no mechanism)",_body:r.body||"(no body)",_type:r.type||"(no type)",
    un:un,themes:un,sdgs:Array.isArray(r.sdgs)?r.sdgs:[],
    sdg_targets:Array.isArray(r.sdg_targets)?r.sdg_targets:[],affected_persons:Array.isArray(r.affected_persons)?r.affected_persons:[]});
});
var N=R.length;
var KEYMAP=new Map();R.forEach(function(r){KEYMAP.set(r._k,r)});
var ALL_THEMES=Array.from(new Set([].concat.apply([],R.map(function(r){return r.un})))).sort(function(a,b){return a.localeCompare(b)});
var YEARS=Array.from(new Set(R.map(function(r){return r.year}).filter(function(y){return typeof y==="number"}))).sort(function(a,b){return a-b});
var YMIN=YEARS.length?YEARS[0]:null,YMAX=YEARS.length?YEARS[YEARS.length-1]:null;
var PREF=[UPR,"Treaty bodies","Special Procedures"];
var MECHS=Array.from(new Set(R.map(function(r){return r._mech}))).sort(function(a,b){var x=PREF.indexOf(a),y=PREF.indexOf(b);x=x<0?9:x;y=y<0?9:y;return x-y||a.localeCompare(b)});
var MCOL={"Universal Periodic Review":"#c2410c","Treaty bodies":"#0f766e","Special Procedures":"#7c3aed"};
function mcol(m){return MCOL[m]||"#6b6459"}
var TYPES=Array.from(new Set(R.map(function(r){return r._type}))).sort();
var ANY_STATES=R.some(function(r){return r._states&&r._states.length});
var DOCS_ALL=new Set(R.map(function(r){return r.symbol})).size;
var MARKL={fit:"Fits",no:"Doesn't fit",un:"Unsure"};

/* ---------- state ---------- */
var st,F=[],sig="",active=0,openSec=-1,showStates=false,dateDir=-1,page=50,expanded=new Set(),kwWords=[],kwT;
var sample=null,sampleSeed="1",openCard=-1,chartA=null,chartB=null,lastFig=null,drawnSig=null;
var mode="mine",corr={},marks={},ver=0,corrMsg="",undoAllArmed=false;
function freshState(){return {kw:"",mech:"",body:"",type:"",state:"",yFrom:YMIN,yTo:YMAX,sdg:"",themes:[]}}
st=freshState();

/* ---------- corrections (the UN's labels in r.un are never changed) ---------- */
function effList(r){var c=corr[r._k];return c?r.un.filter(function(t){return c.rem.indexOf(t)<0}).concat(c.add):r.un}
function refreshLabels(){ver++;R.forEach(function(r){r.themes=(mode==="mine"&&corr[r._k])?effList(r):r.un})}
function nLabels(){var n=0;Object.keys(corr).forEach(function(k){n+=corr[k].rem.length+corr[k].add.length});return n}
function tidy(k){var c=corr[k];if(c&&!c.rem.length&&!c.add.length)delete corr[k]}
function removeLabel(k,t){
  var r=KEYMAP.get(k);if(!r)return;var c=corr[k]||(corr[k]={rem:[],add:[]});
  if(c.add.indexOf(t)>=0)c.add=c.add.filter(function(x){return x!==t});
  else if(r.un.indexOf(t)>=0&&c.rem.indexOf(t)<0)c.rem.push(t);
  tidy(k);
}
function addLabel(k,t){
  var r=KEYMAP.get(k);if(!r||ALL_THEMES.indexOf(t)<0)return;var c=corr[k]||(corr[k]={rem:[],add:[]});
  if(c.rem.indexOf(t)>=0)c.rem=c.rem.filter(function(x){return x!==t});
  else if(r.un.indexOf(t)<0&&c.add.indexOf(t)<0)c.add.push(t);
  tidy(k);
}
function undoLabel(k,t,kind){var c=corr[k];if(!c)return;if(kind==="rem")c.rem=c.rem.filter(function(x){return x!==t});else c.add=c.add.filter(function(x){return x!==t});tidy(k)}

/* label chips: view "un" = the UN's labels only; "mine" = my version with the UN's removed labels struck; "edit" = same, clickable */
var EMPTY='<span class="missing">not labelled</span>';
function tagPlain(t){return '<span class="tag">'+esc(t)+"</span>"}
function chipsFor(r,view){
  if(view==="un")return r.un.length?r.un.map(tagPlain).join(""):EMPTY;
  var c=corr[r._k]||{rem:[],add:[]},h="",k=esc(r._k),edit=view==="edit";
  r.un.forEach(function(t){
    var tt=esc(t);
    if(c.rem.indexOf(t)>=0){
      h+=edit?'<button class="tag struck" data-act="undolabel" data-kind="rem" data-k="'+k+'" data-t="'+tt+'" title="Click to restore the UN label"><s>'+tt+'</s><span class="sr"> UN label removed by you; click to restore it</span></button>'
             :'<span class="tag struck"><s>'+tt+'</s><span class="sr"> (UN label, removed by you)</span></span>';
    }else{
      h+=edit?'<button class="tag" data-act="rmlabel" data-k="'+k+'" data-t="'+tt+'" title="Remove this label from your version; the UN label is kept">'+tt+' <span aria-hidden="true">×</span><span class="sr"> click to remove this label</span></button>':tagPlain(t);
    }
  });
  c.add.forEach(function(t){
    var tt=esc(t);
    h+=edit?'<button class="tag mine" data-act="undolabel" data-kind="add" data-k="'+k+'" data-t="'+tt+'" title="Label added by you; click to undo"><span aria-hidden="true">✎ </span>'+tt+'<span class="sr"> label added by you; click to undo</span></button>'
           :'<span class="tag mine"><span aria-hidden="true">✎ </span>'+tt+'<span class="sr"> (label added by you)</span></span>';
  });
  return h||EMPTY;
}
function themesDD(r){
  var c=corr[r._k];
  if(c&&mode==="mine")return chipsFor(r,"mine")+'<span class="corrtag">corrected by you</span>';
  if(c)return chipsFor(r,"un")+' <span class="hint">you corrected this record; switch to “with my corrections” to see it</span>';
  return chipsFor(r,"un");
}
function labelsDesc(){var n=nLabels();return mode==="mine"?(n?"with your corrections ("+fmt(n)+" label"+(n===1?"":"s")+")":"UN labels (no corrections yet)"):"UN labels only"}

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
function renderHeaderCorr(){
  var n=nLabels();
  $("corrLine").textContent=(n===1?"1 label":fmt(n)+" labels")+" corrected by you; the UN's own labels are kept";
  $("sw").setAttribute("aria-checked",mode==="mine"?"true":"false");
  $("corrHint").textContent=(mode==="un"&&n)?"showing the UN's labels only":"";
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
function applyFilters(keep){
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
  sig=JSON.stringify(st)+"|"+ver;
  if(!keep){page=50;sample=null;openCard=-1}
  render();
}
function commit(forceMine){if(forceMine)mode="mine";refreshLabels();applyFilters(true)}
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
  var srcTxt="Source: "+(D.source||"UHRI")+"; "+COUNTRY+"; "+fmt(F.length)+" of "+fmt(N)+" records. Labels: "+labelsDesc()+".";
  $("src1").textContent=srcTxt;$("src2").textContent=srcTxt;
  $("fig1title").textContent="Ten most frequent themes among "+fmt(F.length)+" filtered records"+(mode==="mine"&&nLabels()?", with your corrections":"");
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
   +"<dt>Themes</dt><dd>"+themesDD(r)+"</dd>"
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
    var open=expanded.has(r._i),ct=(mode==="mine"&&corr[r._k])?'<span class="corrtag">corrected by you</span>':"";
    return '<tr class="row" data-row="'+r._i+'"><td class="nw">'+esc(r.date||"")+"</td><td>"+esc(r.body||"")+'</td><td class="nw">'+symLink(r)+'</td><td class="num">'+(r._para?esc(r._para):"–")+'</td><td><button class="rowbtn" aria-expanded="'+open+'">'+hl(r._first)+"</button>"+ct+"</td><td>"+stateCell(r)+"</td></tr>"+(open?detailRow(r):"");
  }).join("");
  $("moreBtn").hidden=rows.length<=page;
  $("src3").textContent="Source: "+(D.source||"UHRI")+"; "+COUNTRY+". Date is the date of the UN document, not of the recommendation. Paragraph numbers are read from the start of the text. Labels: "+labelsDesc()+".";
}

/* ---------- checks ---------- */
function linkList(rs){
  if(!rs.length)return "";
  var shown=rs.slice(0,200);
  return '<details><summary>List the '+fmt(rs.length)+" records</summary><ul>"+shown.map(function(r){return "<li>"+symLink(r)+(r._para?", para. "+esc(r._para):"")+' <span class="hint">'+esc(r._text.slice(-90))+"</span></li>"}).join("")+(rs.length>200?"<li>… and "+fmt(rs.length-200)+" more</li>":"")+"</ul></details>";
}
function partition(field,label){
  var c=new Map();R.forEach(function(r){var v=r[field];if(v!==undefined&&v!==null&&v!=="")c.set(v,(c.get(v)||0)+1)});
  var sum=0;c.forEach(function(v){sum+=v});
  return {title:"Partition by "+label,ok:sum===N,vals:c.size+" groups sum to "+fmt(sum)+" · records "+fmt(N)+(sum!==N?" ("+fmt(N-sum)+" records have no "+label+")":"")};
}
function runChecks(){
  var out=[];
  var cn=Number(D.count);
  out.push({t:"Record count",ok:cn===N,v:"records.length = "+fmt(N)+" · count in the file = "+(isNaN(cn)?esc(D.count):fmt(cn))});
  ["mechanism","body","year"].forEach(function(f){var p=partition(f,f);out.push({t:p.title,ok:p.ok,v:esc(p.vals)})});
  var ts=0;typeCounts(F).forEach(function(e){ts+=e[1]});
  out.push({t:"Type partition (current filter)",ok:ts===F.length,v:"counts per type sum to "+fmt(ts)+" · headline total "+fmt(F.length)});
  var fig,src;
  if(drawnSig===sig&&lastFig&&lastFig.sig===sig){fig=lastFig;src="values read from the drawn chart and table"}else{fig=buildFig(F);src="recomputed: tab 01 not drawn for this filter yet"}
  var cnt={};for(var i=0;i<F.length;i++){var th=F[i].themes;for(var j=0;j<th.length;j++)cnt[th[j]]=(cnt[th[j]]||0)+1}
  var barVals=(drawnSig===sig&&chartA)?chartA.data.datasets[0].data.slice():fig.top.map(function(e){return e.n});
  var tblVals=(drawnSig===sig)?Array.prototype.map.call(document.querySelectorAll("#t1 tbody tr[data-n]"),function(tr){return Number(tr.dataset.n)}):fig.top.map(function(e){return e.n});
  var bad=[],mx=0;
  fig.top.forEach(function(e,k){var ex=cnt[e.theme]||0;if(barVals[k]!==ex||tblVals[k]!==ex)bad.push(e.theme+": bar "+barVals[k]+", table "+tblVals[k]+", recount "+ex);if(ex>mx)mx=ex});
  out.push({t:"Chart against table",ok:!bad.length&&mx<=F.length&&barVals.length===tblVals.length,v:fig.top.length+" bars checked; largest "+fmt(mx)+" ≤ filtered "+fmt(F.length)+" · "+src+(bad.length?" · "+esc(bad.join("; ")):"")});
  var badLinks=R.filter(function(r){
    var u=r.doc_url||"";if(u.indexOf("https://docs.un.org/")!==0)return true;
    var d=u;try{d=decodeURIComponent(u)}catch(e){}
    return d.toLowerCase().slice(-String(r.symbol||"").length)!==String(r.symbol||"").toLowerCase()||!r.symbol;
  });
  out.push({t:"Links to UN documents",ok:!badLinks.length,v:fmt(N-badLinks.length)+" of "+fmt(N)+" doc_url start with https://docs.un.org/ and end with the symbol",extra:linkList(badLinks)});
  var pp=MECHS.map(function(m){var a=R.filter(function(r){return r._mech===m}),k=a.filter(function(r){return r._para}).length;return {m:m,k:k,n:a.length}});
  var upr=pp.filter(function(p){return p.m===UPR})[0];
  out.push({t:"Paragraph numbers found",ok:true,warn:!!(upr&&upr.k<upr.n),v:pp.map(function(p){return esc(p.m)+": "+pct(p.k,p.n)+" ("+fmt(p.k)+" of "+fmt(p.n)+")"}).join(" · ")+(upr?" · UPR expected 100%":"")});
  var uprs=R.filter(function(r){return r._states!==null}),noSt=uprs.filter(function(r){return !r._states.length});
  out.push({t:"Recommending States found",ok:true,warn:noSt.length>0,v:fmt(uprs.length-noSt.length)+" of "+fmt(uprs.length)+" UPR records have at least one State"+(noSt.length?" · "+fmt(noSt.length)+" without (see the list)":""),extra:linkList(noSt)});
  var ids=new Set(R.map(function(r){return r.id}));
  out.push({t:"Distinct ids",ok:ids.size===N,v:fmt(ids.size)+" distinct ids · records "+fmt(N)});
  var tm=new Map();R.forEach(function(r){tm.set(r._text,(tm.get(r._text)||0)+1)});
  var dup=0;tm.forEach(function(v){if(v>1)dup++});
  out.push({t:"Duplicate texts",ok:true,info:true,v:fmt(dup)+" texts appear more than once; they are kept"});
  out.push({t:"Not labelled (UN labels)",ok:true,info:true,v:"no themes: "+fmt(R.filter(function(r){return !r.un.length}).length)+" · no SDGs: "+fmt(R.filter(function(r){return !r.sdgs.length}).length)+" · no affected persons: "+fmt(R.filter(function(r){return !r.affected_persons.length}).length)+" (shown as not labelled)"});
  // corrections
  var ck=Object.keys(corr),nl=nLabels(),aN=0,rN=0,badC=[];
  ck.forEach(function(k){var r=KEYMAP.get(k),c=corr[k];if(!r){badC.push(k);return}
    c.rem.forEach(function(t){rN++;if(r.un.indexOf(t)<0)badC.push(r.symbol+": removed label is not a UN label of the record")});
    c.add.forEach(function(t){aN++;if(ALL_THEMES.indexOf(t)<0||r.un.indexOf(t)>=0)badC.push(r.symbol+": added label is not valid")});});
  out.push({t:"Your corrections are valid",ok:!badC.length,v:fmt(nl)+" labels on "+fmt(ck.length)+" records ("+fmt(rN)+" removed, "+fmt(aN)+" added); every removed label was a UN label of its record, every added label occurs in the data"+(badC.length?" · problems: "+esc(badC.slice(0,5).join("; ")):"")});
  var diff=0;R.forEach(function(r,i){var o=Array.isArray(RAW[i].themes)?RAW[i].themes:[];if(JSON.stringify(o)!==JSON.stringify(r.un))diff++});
  out.push({t:"UN labels kept",ok:diff===0,v:fmt(N-diff)+" of "+fmt(N)+" records still hold exactly the UN's themes as in the file"});
  var expT=0,actT=0;R.forEach(function(r){var c=corr[r._k];expT+=(mode==="mine"&&c)?r.un.length-c.rem.length+c.add.length:r.un.length;actT+=r.themes.length});
  out.push({t:"Counts follow the switch",ok:expT===actT,v:"labels in use: "+fmt(actT)+" · recount from the UN's labels and your corrections ("+(mode==="mine"?"with my corrections":"UN labels only")+"): "+fmt(expT)});
  return out;
}
function renderChecks(){
  $("checksBox").innerHTML=runChecks().map(function(c){
    var cls=!c.ok?"fail":c.warn?"warn":c.info?"info":"pass",lab={fail:"✗ check failed",warn:"⚠ warning",info:"i note",pass:"✓ pass"}[cls];
    return '<li><span class="mk '+cls+'">'+lab+'</span><div><strong>'+esc(c.t)+'</strong><div class="vals">'+c.v+"</div>"+(c.extra||"")+"</div></li>";
  }).join("");
}
function mulberry32(a){return function(){a|=0;a=a+0x6D2B79F5|0;var t=Math.imul(a^a>>>15,1|a);t=t+Math.imul(t^t>>>7,61|t)^t;return((t^t>>>14)>>>0)/4294967296}}
function draw(seed){
  var s=parseInt(seed,10);if(isNaN(s))s=1;sampleSeed=String(s);
  var pool=F.slice(),rng=mulberry32(s);
  for(var i=pool.length-1;i>0;i--){var j=Math.floor(rng()*(i+1));var t=pool[i];pool[i]=pool[j];pool[j]=t}
  sample=pool.slice(0,10);openCard=-1;renderSample();
}
function renderSample(){
  var b=$("sampleBox");
  var intro='<p class="note" style="margin-top:0">This is your judgement of the UN\'s labels; nothing is sent anywhere. Ten records are drawn from the current filter ('+fmt(F.length)+' matching); each card asks whether the themes as a set fit the paragraph.</p>'
    +'<p class="note" style="margin-top:-10px">Mark a card Doesn\'t fit or Unsure to correct it: remove a label, or add one that occurs in the data. The UN\'s label is kept, struck through beside yours.</p>';
  if(!sample){
    b.innerHTML=intro+(F.length?'<button class="btn" data-act="draw-random">Check 10 at random</button>':'<p class="missing">No records match: nothing to draw.</p>');
    return;
  }
  var c={fit:0,no:0,un:0};sample.forEach(function(r){var m=marks[r._k];if(m)c[m]++});
  var judged=c.fit+c.no+c.un;
  b.innerHTML=intro+'<div class="acts"><button class="btn" data-act="draw-random" id="again">Draw again</button><label class="mono" for="seedBox">Seed</label><input type="text" id="seedBox" style="width:110px" value="'+esc(sampleSeed)+'" inputmode="numeric"><button class="btn alt" data-act="draw-seed">Draw with this seed</button></div>'
   +'<div class="sample-tally" aria-live="polite">Themes: '+c.fit+" fit, "+c.no+" don't, "+c.un+" unsure of "+sample.length+" judged ("+judged+" so far) · seed "+esc(sampleSeed)+" · your judgement, not a UN label</div>"
   +'<ol class="cards">'+sample.map(function(r,k){
     var m=marks[r._k],cc=corr[r._k],open=openCard===k,editable=(m==="no"||m==="un"||!!cc);
     var vl=m?MARKL[m]:"";
     var body="";
     if(open){
       var editor;
       if(editable){
         var opts=ALL_THEMES.filter(function(t){return r.un.indexOf(t)<0&&(!cc||cc.add.indexOf(t)<0)});
         editor='<div class="editor"><div class="mono">Correct the labels · click a label to remove it; click a struck or italic label to undo · editing turns on “with my corrections”</div>'
          +'<div class="acts" style="margin-top:8px"><label class="mono" for="ad-'+r._i+'">Add a label from the data</label><select id="ad-'+r._i+'" style="width:auto;max-width:380px"><option value="">Choose a label…</option>'+opts.map(function(t){return '<option value="'+esc(t)+'">'+esc(t)+"</option>"}).join("")+'</select>'
          +'<button class="btn alt" data-act="addlabel" data-k="'+esc(r._k)+'" data-i="'+r._i+'">Add label</button>'
          +(cc?'<button class="btn alt" data-act="undorec" data-k="'+esc(r._k)+'">Undo all for this record</button>':"")+"</div></div>";
       }else editor='<div class="hint" style="margin-top:8px">Mark Doesn\'t fit or Unsure to correct a label.</div>';
       body='<div class="cardbody"><p class="fulltext">'+esc(r._text)+'</p><div class="mono" style="margin-bottom:4px">Themes'+(editable?" (UN\'s labels kept; your edits marked)":" given by the UN")+'</div><div>'+chipsFor(r,editable?"edit":"un")+'</div><div class="acts" style="margin-top:8px">'
       +[["fit","Fits"],["no","Doesn't fit"],["un","Unsure"]].map(function(x){return '<button class="btn alt" id="v-'+r._i+'-'+x[0]+'" data-act="verdict" data-k="'+esc(r._k)+'" data-i="'+r._i+'" data-v="'+x[0]+'" aria-pressed="'+(m===x[0])+'">'+x[1]+"</button>"}).join("")+"</div>"+editor+"</div>";
     }
     return "<li><div class=\"cardline\"><span class=\"mono\">"+(k+1)+"</span><span>"+symLink(r)+'</span><span class="hint">'+(r._para?"para. "+esc(r._para):"no para.")+'</span><button class="rowbtn" id="c-'+k+'" data-act="card" data-k="'+k+'" aria-expanded="'+open+'">'+esc(r._first)+'</button><span class="mono" style="color:var(--red)">'+vl+(cc?'<span class="corrtag">corrected by you</span>':"")+"</span></div>"+body+"</li>";
   }).join("")+"</ol>";
}
function focusAfter(k){
  var r=KEYMAP.get(k),el=r?$("ad-"+r._i):null;
  if(!el&&sample){var kk=-1;sample.forEach(function(x,i){if(x._k===k)kk=i});if(kk>=0)el=$("c-"+kk)}
  if(el)el.focus();
}

/* ---------- corrections tab ---------- */
var CSVHEAD=["symbol","paragraph","un_labels","my_labels","my_mark","record_id"];
function renderCorrections(){
  var rows=R.filter(function(r){return corr[r._k]}),n=nLabels();
  $("corrIntro").textContent=rows.length?"Corrections live only in this page: download the CSV to keep them, load it later to restore them. Labels shown: "+labelsDesc()+".":"No corrections yet. In 03 Check, draw ten records, mark one Doesn't fit or Unsure, then remove a label or add one. Corrections live only in this page: download the CSV to keep them.";
  $("tCorr").hidden=!rows.length;
  $("capCorr").textContent="Your corrections: "+fmt(n)+" label"+(n===1?"":"s")+" on "+fmt(rows.length)+" record"+(rows.length===1?"":"s");
  $("tbCorr").innerHTML=rows.map(function(r){
    var c=corr[r._k],k=esc(r._k);
    var unCell=r.un.length?r.un.map(function(t){
      return c.rem.indexOf(t)>=0?'<button class="tag struck" data-act="undolabel" data-kind="rem" data-k="'+k+'" data-t="'+esc(t)+'" title="Click to restore the UN label"><s>'+esc(t)+'</s><span class="sr"> removed by you; click to restore</span></button>':tagPlain(t);
    }).join(""):EMPTY;
    var my=r.un.filter(function(t){return c.rem.indexOf(t)<0}).map(tagPlain).join("")+c.add.map(function(t){
      return '<button class="tag mine" data-act="undolabel" data-kind="add" data-k="'+k+'" data-t="'+esc(t)+'" title="Added by you; click to undo"><span aria-hidden="true">✎ </span>'+esc(t)+'<span class="sr"> added by you; click to undo</span></button>';
    }).join("");
    var mk=marks[r._k];
    return '<tr><td class="nw">'+symLink(r)+'</td><td class="num">'+(r._para?esc(r._para):"–")+"</td><td>"+unCell+"</td><td>"+(my||EMPTY)+'</td><td class="nw">'+(mk?esc(MARKL[mk]):'<span class="missing">–</span>')+'</td><td><button class="btn alt" data-act="undorec" data-k="'+k+'" aria-label="Undo all corrections on '+esc(cite(r))+'">Undo</button></td></tr>';
  }).join("");
  $("dlCorr").disabled=!rows.length;
  var ua=$("undoAll");ua.disabled=!rows.length;ua.textContent=undoAllArmed?"Really undo all "+fmt(n)+"? Click again":"Undo all";
  $("corrMsg").textContent=corrMsg;
}
function saveBlob(name,text,type){
  var blob=new Blob(["\uFEFF"+text],{type:type});
  var url=URL.createObjectURL(blob),a=document.createElement("a");
  a.href=url;a.download=name;document.body.appendChild(a);a.click();a.remove();setTimeout(function(){URL.revokeObjectURL(url)},4000);
}
function slug(){return String(COUNTRY).toLowerCase().replace(/[^a-z0-9]+/g,"-")}
function csvCell(v){var s=String(v==null?"":v);return /[",\n\r]/.test(s)?'"'+s.replace(/"/g,'""')+'"':s}
function downloadCorr(){
  var rows=R.filter(function(r){return corr[r._k]});if(!rows.length)return;
  var lines=["# My corrections to the UN's theme labels: "+COUNTRY,"# Source: "+(D.source||"UHRI")+(D.source_url?" ("+D.source_url+")":""),"# Built: "+(D.built||"unknown"),"# Saved: "+new Date().toISOString().slice(0,10),
    "# "+nLabels()+" labels corrected on "+rows.length+" records; the UN's own labels are kept in the un_labels column","# Load this file in the dashboard (tab 04 Corrections) to restore the corrections. Labels are separated by ' | '."];
  lines.push(CSVHEAD.join(","));
  rows.forEach(function(r){lines.push([r.symbol,r._para||"",r.un.join(" | "),effList(r).join(" | "),marks[r._k]?MARKL[marks[r._k]]:"",r._k].map(csvCell).join(","))});
  saveBlob("uhri-"+slug()+"-my-corrections.csv",lines.join("\n"),"text/csv;charset=utf-8");
  corrMsg="Downloaded "+rows.length+" records with corrections.";renderCorrections();
}
function parseLine(line){
  var out=[],cur="",q=false;
  for(var i=0;i<line.length;i++){var ch=line.charAt(i);
    if(q){if(ch==='"'){if(line.charAt(i+1)==='"'){cur+='"';i++}else q=false}else cur+=ch}
    else{if(ch==='"')q=true;else if(ch===","){out.push(cur);cur=""}else cur+=ch}}
  out.push(cur);return out;
}
function splitLabels(s){return String(s||"").split("|").map(function(x){return x.trim()}).filter(Boolean)}
function loadCorr(text){
  var lines=String(text).replace(/^\uFEFF/,"").split(/\r?\n/).filter(function(l){return l.trim()&&l.charAt(0)!=="#"});
  if(!lines.length){corrMsg="The file is empty: nothing loaded.";return}
  var head=parseLine(lines[0]).map(function(h){return h.trim().toLowerCase()});
  var ix={};CSVHEAD.forEach(function(h){ix[h]=head.indexOf(h)});
  if(ix.symbol<0||ix.my_labels<0){corrMsg="This does not look like a corrections file: the columns symbol and my_labels are needed. Nothing loaded.";return}
  var bySP=new Map();R.forEach(function(r){var key=r.symbol+"|"+(r._para||"");if(!bySP.has(key))bySP.set(key,[]);bySP.get(key).push(r)});
  var applied=0,labels=0,notFound=0,ambiguous=0,nochange=0,ignored=0,unDiff=0,marked=0;
  lines.slice(1).forEach(function(line){
    var f=parseLine(line),sym=(f[ix.symbol]||"").trim(),para=ix.paragraph>=0?(f[ix.paragraph]||"").trim():"",rid=ix.record_id>=0?(f[ix.record_id]||"").trim():"";
    var rec=null;
    if(rid&&KEYMAP.has(rid)&&(!sym||KEYMAP.get(rid).symbol===sym))rec=KEYMAP.get(rid);
    if(!rec){var cand=bySP.get(sym+"|"+para)||[];if(cand.length===1)rec=cand[0];else if(cand.length>1){ambiguous++;return}}
    if(!rec){notFound++;return}
    var mine=splitLabels(f[ix.my_labels]).filter(function(t){if(ALL_THEMES.indexOf(t)<0){ignored++;return false}return true});
    if(ix.un_labels>=0){var u=splitLabels(f[ix.un_labels]);if(u.length!==rec.un.length||u.some(function(t){return rec.un.indexOf(t)<0}))unDiff++}
    var rem=rec.un.filter(function(t){return mine.indexOf(t)<0}),add=mine.filter(function(t,i){return rec.un.indexOf(t)<0&&mine.indexOf(t)===i});
    var mk="";if(ix.my_mark>=0){var mv=(f[ix.my_mark]||"").trim().toLowerCase();mk=mv==="fits"?"fit":(mv==="doesn't fit"||mv==="doesn’t fit")?"no":mv==="unsure"?"un":""}
    if(mk){marks[rec._k]=mk;marked++}
    if(!rem.length&&!add.length){delete corr[rec._k];nochange++;return}
    corr[rec._k]={rem:rem,add:add};applied++;labels+=rem.length+add.length;
  });
  corrMsg="Loaded: "+applied+" records restored ("+labels+" labels), "+nochange+" without a change, "+notFound+" not found in this file, "+ambiguous+" ambiguous (symbol and paragraph match several records)"
    +(ignored?", "+ignored+" labels ignored because they do not occur in the data":"")+(unDiff?"; for "+unDiff+" records the UN's labels in the CSV differ from this file (your labels were applied anyway)":"")+(marked?"; "+marked+" marks restored":"")+". Corrections for other records were kept.";
  mode="mine";refreshLabels();applyFilters(true);
}

/* ---------- method & export ---------- */
function summaryText(){
  var s=stats(F),fig=buildFig(F),tc=typeCounts(F),f=describeFilters(),g={};
  F.forEach(function(r){g[r._mech]=(g[r._mech]||0)+1});
  return "UHRI, "+COUNTRY+": "+fmt(F.length)+" matching records (of "+fmt(N)+" in the file) from "+fmt(s.docs)+" UN documents, "+(s.y0!=null?s.y0+"–"+s.y1:"years unknown")+". "
   +"Filters: "+(f.length?f.join("; "):"none")+". "
   +"Labels: "+labelsDesc()+". "
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
   +"<p>Themes, SDGs and affected persons are the UN’s own labels, and the app never changes them. Your corrections to the themes are kept apart and applied on top only while the switch under the title says “with my corrections”; then every count, chart and filter uses them. Dates are the dates of the documents, not of the recommendations.</p>"
   +"<p>A citation is the symbol and the paragraph, for example “"+esc(F[0]?cite(F[0]):"SYMBOL, para. N")+"”.</p>";
  $("csvNote").textContent="The CSV holds the "+fmt(F.length)+" rows of the current filter: the table columns plus full text and labels (as the switch shows them, with the UN's themes and a corrected-by-you flag beside), with comment lines on top (country, source, build date, filters, row count).";
  $("sumbox").value=summaryText();
  $("srcLine").innerHTML="Data source: "+(su?'<a href="'+esc(su)+'" target="_blank" rel="noopener">'+esc(D.source||su)+"</a>":esc(D.source||"UHRI"))+(D.built?" · built "+esc(D.built):"")+" · licence: not stated in the file; see the terms at the source.";
}
function downloadCsv(){
  var f=describeFilters(),rows=sortedRows();
  var lines=["# Country: "+COUNTRY,"# Source: "+(D.source||"UHRI")+(D.source_url?" ("+D.source_url+")":""),"# Built: "+(D.built||"unknown"),"# Filters: "+(f.length?f.join("; "):"none"),"# Labels in the themes column: "+labelsDesc(),"# Rows: "+rows.length+" of "+N,"# Date is the date of the UN document."];
  lines.push(["date","body","mechanism","type","symbol","doc_url","paragraph","recommending_states","section","text","themes","themes_un","corrected_by_you","sdgs","sdg_targets","affected_persons"].join(","));
  rows.forEach(function(r){lines.push([r.date,r.body,r.mechanism,r.type,r.symbol,r.doc_url,r._para||"",r._states?r._states.join(" | "):"",r.section||"",r._text,r.themes.join(" | "),r.un.join(" | "),corr[r._k]?"yes":"no",r.sdgs.join(" | "),r.sdg_targets.join(" | "),r.affected_persons.join(" | ")].map(csvCell).join(","))});
  saveBlob("uhri-"+slug()+"-filtered.csv",lines.join("\n"),"text/csv;charset=utf-8");
}
async function copyText(t){
  try{await navigator.clipboard.writeText(t);return true}catch(e){
    try{var ta=document.createElement("textarea");ta.value=t;ta.style.position="fixed";ta.style.opacity="0";document.body.appendChild(ta);ta.select();var ok=document.execCommand("copy");ta.remove();return ok}catch(e2){return false}
  }
}
function flash(el,ok){if(!el)return;el.textContent=ok?"Copied":"Copy failed: select the text by hand";setTimeout(function(){el.textContent=""},2000)}

/* ---------- main render & tabs ---------- */
function render(){
  renderHeaderCorr();renderRail();
  if(active===0)renderOverview();
  else if(active===1)renderRecords();
  else if(active===2){renderChecks();renderSample()}
  else if(active===3)renderCorrections();
  else renderMethod();
}
var NT=5;
var tabs=[0,1,2,3,4].map(function(i){return $("tab"+i)}),panels=[0,1,2,3,4].map(function(i){return $("p"+i)});
function showTab(i,focus){
  active=i;
  tabs.forEach(function(t,k){t.setAttribute("aria-selected",k===i);t.tabIndex=k===i?0:-1;panels[k].hidden=k!==i});
  if(focus)tabs[i].focus();render();
}
tabs.forEach(function(t,i){
  t.addEventListener("click",function(){showTab(i,false)});
  t.addEventListener("keydown",function(e){
    var k=null;
    if(e.key==="ArrowRight")k=(i+1)%NT;else if(e.key==="ArrowLeft")k=(i+NT-1)%NT;else if(e.key==="Home")k=0;else if(e.key==="End")k=NT-1;
    if(k!==null){e.preventDefault();showTab(k,true)}
  });
});

/* ---------- events ---------- */
document.addEventListener("click",function(e){
  var a=e.target.closest("[data-act]");
  if(undoAllArmed&&!(a&&a.dataset.act==="undoall")){undoAllArmed=false;if(active===3)renderCorrections()}
  if(a){
    var act=a.dataset.act;
    if(act==="sec"){var i=Number(a.dataset.i);openSec=openSec===i?-1:i;renderRail();return}
    if(act==="clear"){st=freshState();syncControls();applyFilters();return}
    if(act==="sw"){mode=mode==="mine"?"un":"mine";refreshLabels();applyFilters(true);return}
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
    if(act==="verdict"){marks[a.dataset.k]=a.dataset.v;renderSample();var vb=$("v-"+a.dataset.i+"-"+a.dataset.v);if(vb)vb.focus();return}
    if(act==="rmlabel"){removeLabel(a.dataset.k,a.dataset.t);commit(true);focusAfter(a.dataset.k);return}
    if(act==="addlabel"){
      var sel=$("ad-"+a.dataset.i);if(!sel)return;if(!sel.value){sel.focus();return}
      addLabel(a.dataset.k,sel.value);commit(true);focusAfter(a.dataset.k);return;
    }
    if(act==="undolabel"){undoLabel(a.dataset.k,a.dataset.t,a.dataset.kind);corrMsg="Undone: one label.";commit(false);if(active===3)$("corrTitle").focus();else focusAfter(a.dataset.k);return}
    if(act==="undorec"){delete corr[a.dataset.k];corrMsg="Undone: all corrections on one record.";commit(false);if(active===3)$("corrTitle").focus();else focusAfter(a.dataset.k);return}
    if(act==="undoall"){
      if(!undoAllArmed){undoAllArmed=true;renderCorrections();return}
      undoAllArmed=false;corr={};corrMsg="Undone: all corrections. The UN's labels were never changed.";commit(false);$("corrTitle").focus();return;
    }
    if(act==="dlcorr"){downloadCorr();return}
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
$("corrFile").addEventListener("change",function(e){
  var f=e.target.files&&e.target.files[0];if(!f)return;
  var rd=new FileReader();
  rd.onload=function(){loadCorr(String(rd.result||""));renderHeaderCorr();if(active===3)renderCorrections();$("corrFile").value=""};
  rd.onerror=function(){corrMsg="The file could not be read. Nothing loaded.";renderCorrections();$("corrFile").value=""};
  rd.readAsText(f);
});

/* ---------- start ---------- */
initHeader();initControls();refreshLabels();applyFilters();
})();
</script>
</body>
</html>
```