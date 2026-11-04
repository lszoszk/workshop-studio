I added corrections to the random-sample check on tab 03. Mark a paragraph "Doesn't fit" or "Unsure", then remove a theme or add one from the labels that occur in the data. The line and switch under the title control whether every count, chart, filter and record shows the UN's labels or yours.

Corrections apply to the UN's themes only. They are kept only while the page is open, so download the CSV to keep them. The CSV has one extra column, "Record id", so a reload matches the right record.

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>UN human rights recommendations and observations</title>
<style>
[hidden]{display:none!important}
:root{--paper:#f4f0e8;--ink:#1d1b18;--rule:#d9d2c3;--red:#9b2335;--mute:#5c564b;--serif:Georgia,"Times New Roman",serif;--mono:ui-monospace,Menlo,Consolas,monospace}
*{box-sizing:border-box}
body{margin:0;background:var(--paper);color:var(--ink);font:16px/1.5 system-ui,-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
.wrap{max-width:1320px;margin:0 auto;padding:20px 24px 40px}
a{color:var(--ink);text-decoration-color:var(--red);text-underline-offset:2px}
a:hover{color:var(--red)}
:focus-visible{outline:3px solid var(--red);outline-offset:2px}
.lbl{font:11.5px var(--mono);letter-spacing:.09em;text-transform:uppercase;color:var(--mute)}
h1{font:400 34px/1.15 var(--serif);margin:4px 0 8px}
.meta{font-size:14px;color:var(--mute);margin:0 0 14px}
.meta a{color:var(--mute)}
.corr{display:flex;flex-wrap:wrap;align-items:center;gap:8px 18px;margin:0 0 8px;font:12.5px var(--mono);color:var(--ink)}
.sw{font:12px var(--mono);letter-spacing:.05em;background:none;border:1px solid var(--ink);padding:5px 10px;cursor:pointer;color:var(--mute);display:inline-flex;gap:10px;align-items:center}
.sw .on{color:var(--red);font-weight:700;text-decoration:underline;text-decoration-color:var(--red)}
.sw .trk{width:30px;height:14px;border:1px solid var(--ink);border-radius:8px;position:relative;background:#fff;display:inline-block}
.sw .trk::after{content:"";position:absolute;top:1px;left:1px;width:10px;height:10px;border-radius:50%;background:var(--ink)}
.sw[aria-checked=true] .trk::after{left:17px;background:var(--red)}
[role=tablist]{display:flex;flex-wrap:wrap;border-bottom:1px solid var(--rule);margin-bottom:22px}
.tab{font:12px var(--mono);letter-spacing:.08em;text-transform:uppercase;background:none;border:0;border-bottom:3px solid transparent;padding:11px 16px;cursor:pointer;color:var(--ink)}
.tab[aria-selected=true]{color:var(--red);border-bottom-color:var(--red)}
.layout{display:grid;grid-template-columns:260px minmax(0,1fr);gap:36px}
.rail{align-self:start;position:sticky;top:8px;max-height:calc(100vh - 16px);overflow:auto;padding-right:6px}
.railhead{display:flex;justify-content:space-between;align-items:baseline;border-bottom:1px solid var(--rule);padding-bottom:6px}
.linkbtn{font:11.5px var(--mono);letter-spacing:.06em;background:none;border:0;text-decoration:underline;text-decoration-color:var(--red);cursor:pointer;color:var(--ink);padding:2px}
.big{font:400 52px/1 var(--serif);margin-top:14px}
.of{font:12px var(--mono);color:var(--mute);margin:4px 0 8px}
.bar{height:4px;background:var(--rule)}
.bar i{display:block;height:100%;background:var(--red);width:0}
.chips{display:flex;flex-wrap:wrap;gap:6px;margin:12px 0}
.fchip{font:12px var(--mono);border:1px solid var(--red);color:var(--red);background:none;padding:2px 8px;cursor:pointer;max-width:100%;text-align:left}
.fchip:hover{background:var(--red);color:#fff}
.acc{border-top:1px solid var(--rule)}
.acch{width:100%;display:flex;gap:10px;font:12px var(--mono);letter-spacing:.08em;text-transform:uppercase;background:none;border:0;padding:12px 0;cursor:pointer;text-align:left;color:var(--ink)}
.acch[aria-expanded=true]{color:var(--red)}
.acch .ar{margin-left:auto}
.num{color:var(--red);font-family:var(--mono)}
.accp{padding:0 0 14px}
.accp label{display:block;font:11.5px var(--mono);letter-spacing:.06em;text-transform:uppercase;color:var(--mute);margin:10px 0 3px}
input[type=search],input[type=number],select{font:inherit;width:100%;padding:7px 8px;border:1px solid var(--ink);background:#fff;color:var(--ink);border-radius:0}
.hint{font:11.5px var(--mono);color:var(--mute);margin-top:4px}
.q{font:italic 400 20px var(--serif);margin:0 0 18px;color:var(--ink)}
.tiles{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:22px 30px;margin-bottom:8px}
.tile{border-top:1px solid var(--ink);padding-top:8px}
.tile .n{font:400 48px/1.05 var(--serif)}
.tile .sub{font-size:14px;color:var(--mute);margin-top:4px}
.dot{display:inline-block;width:10px;height:10px;border-radius:50%;margin-right:6px;vertical-align:middle}
.note{font:11.5px/1.5 var(--mono);color:var(--mute);margin:6px 0 26px;max-width:880px}
.src{font:11.5px var(--mono);color:var(--mute);margin:6px 0 26px}
figure{margin:0 0 10px}
.ftitle{font:400 20px var(--serif)}
figcaption{margin-bottom:10px}
.chartbox{position:relative;height:360px}
.chartbox.s{height:300px}
.empty{padding:30px 0;color:var(--mute);font-style:italic}
table{border-collapse:collapse;width:100%;font-size:15px}
caption{text-align:left;font:12px var(--mono);color:var(--mute);padding:6px 0}
th{font:11.5px var(--mono);letter-spacing:.06em;text-transform:uppercase;text-align:left;color:var(--mute);border-bottom:1px solid var(--ink);padding:6px 8px 6px 0;vertical-align:bottom}
td{border-bottom:1px solid var(--rule);padding:7px 8px 7px 0;vertical-align:top}
th.r,td.r{text-align:right;font-variant-numeric:tabular-nums;padding-right:14px}
.thbtn{font:inherit;letter-spacing:inherit;text-transform:inherit;background:none;border:0;cursor:pointer;color:var(--ink);padding:0;text-decoration:underline;text-decoration-color:var(--red)}
tr.row{cursor:pointer}
tr.row:hover td{background:#ece6d8}
tr.row[aria-expanded=true] td{background:#ece6d8;border-bottom-color:transparent}
.tbtn{font:inherit;background:none;border:0;padding:0;text-align:left;cursor:pointer;color:var(--ink);text-decoration:underline;text-decoration-color:var(--red)}
mark{background:#f0d9a8;color:inherit;padding:0 1px}
.detail td{background:#ece6d8;padding:6px 16px 20px 0}
.dgrid{display:grid;grid-template-columns:120px 1fr;gap:18px}
.pnum{font:400 44px/1 var(--serif);color:var(--red)}
.ptext{white-space:pre-wrap;font-size:16px;margin:0 0 14px;max-width:820px}
dl.lab{margin:0 0 14px;display:grid;grid-template-columns:140px 1fr;gap:6px 12px;font-size:14px}
dl.lab dt{font:11.5px var(--mono);letter-spacing:.06em;text-transform:uppercase;color:var(--mute);padding-top:3px}
dl.lab dd{margin:0}
.tag{display:inline-block;border:1px solid var(--rule);background:var(--paper);font-size:13px;padding:1px 7px;margin:0 5px 4px 0}
.tag.mine{background:#fff;border:1px solid var(--red);color:var(--red);font-weight:600}
.tag.struck{border-style:dashed;color:var(--mute)}
.tag del{text-decoration:line-through;text-decoration-thickness:1.5px}
.ctag{display:inline-block;font:10.5px var(--mono);letter-spacing:.06em;text-transform:uppercase;color:var(--red);border:1px solid var(--red);padding:0 5px;margin:0 0 4px 6px;white-space:nowrap;background:#fff}
.xbtn{font:11px var(--mono);background:none;border:0;border-left:1px solid var(--rule);margin-left:5px;padding:0 4px;cursor:pointer;color:var(--red);text-decoration:underline}
.sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}
.miss{font-style:italic;color:var(--mute)}
.btn{font:13px var(--mono);background:none;border:1px solid var(--ink);padding:7px 13px;cursor:pointer;color:var(--ink);text-decoration:none;display:inline-block;margin:0 8px 6px 0}
.btn:hover:not(:disabled){background:var(--ink);color:var(--paper)}
.btn:disabled{opacity:.45;cursor:default}
.btn[aria-pressed=true]{background:var(--red);border-color:var(--red);color:#fff}
.copied{font:12px var(--mono);color:var(--red)}
ul.checks{list-style:none;margin:0 0 30px;padding:0}
ul.checks li{border-top:1px solid var(--rule);padding:9px 0;display:grid;grid-template-columns:130px 1fr;gap:4px 14px}
.st{font:12px var(--mono);letter-spacing:.04em}
.st.pass{color:#1d1b18}.st.fail{color:var(--red);font-weight:700}.st.warn{color:#8a5a00;font-weight:700}.st.info{color:var(--mute)}
.cn{font-weight:600}
.cd{font-size:14px;color:var(--mute)}
.cx{font:12px/1.5 var(--mono);color:var(--mute);margin-top:4px;white-space:pre-wrap;word-break:break-word}
h3{font:400 24px var(--serif);margin:0 0 4px}
ol.sc{list-style:none;padding:0;margin:12px 0}
.sline{width:100%;display:flex;gap:12px;background:none;border:0;border-top:1px solid var(--rule);padding:10px 0;cursor:pointer;text-align:left;font:inherit;color:var(--ink)}
.sline[aria-expanded=true]{color:var(--red)}
.sline .vm{margin-left:auto;font:12px var(--mono);color:var(--mute);white-space:nowrap}
.sbody{padding:4px 0 18px 34px}
blockquote{margin:8px 0 12px;padding-left:14px;border-left:3px solid var(--red);white-space:pre-wrap;max-width:820px}
.editor{border-top:1px solid var(--rule);margin-top:12px;padding-top:10px;max-width:820px}
.editor select{width:auto;min-width:260px;max-width:100%;margin:0 8px 6px 0}
.tally{font:14px var(--mono);margin:12px 0}
.method p{max-width:780px}
.seed{display:flex;gap:10px;align-items:center;flex-wrap:wrap;margin:10px 0}
.seed input{width:110px}
footer{margin-top:40px;border-top:1px solid var(--rule);padding-top:10px;font:11.5px var(--mono);color:var(--mute)}
footer a{color:var(--mute)}
@media(max-width:860px){.layout{grid-template-columns:1fr}.rail{position:static;max-height:none}.dgrid{grid-template-columns:1fr}h1{font-size:27px}}
</style>
</head>
<body>
<div class="wrap" id="app">
<header>
  <div class="lbl" id="hLabel"></div>
  <h1 id="hTitle"></h1>
  <div class="corr">
    <span id="corrLine" aria-live="polite"></span>
    <button class="sw" id="modeSw" role="switch" aria-checked="true" aria-label="Labels shown: on means with my corrections, off means the UN's own labels"><span id="swUn">UN labels</span><span class="trk" aria-hidden="true"></span><span id="swMine">with my corrections</span></button>
  </div>
  <p class="meta" id="hMeta"></p>
</header>
<div role="tablist" id="tabs" aria-label="Dashboard sections">
  <button class="tab" role="tab" id="tab0" aria-controls="panel0" aria-selected="true">01 Overview</button>
  <button class="tab" role="tab" id="tab1" aria-controls="panel1" aria-selected="false" tabindex="-1">02 Records</button>
  <button class="tab" role="tab" id="tab2" aria-controls="panel2" aria-selected="false" tabindex="-1">03 Check</button>
  <button class="tab" role="tab" id="tab3" aria-controls="panel3" aria-selected="false" tabindex="-1">04 Method &amp; export</button>
</div>
<div class="layout">
<aside class="rail" aria-label="Filters">
  <div class="railhead"><span class="lbl">Filters</span><button class="linkbtn" id="clearAll">Clear all</button></div>
  <div class="big" id="matchN" aria-live="polite">0</div>
  <div class="of" id="matchOf"></div>
  <div class="bar"><i id="matchBar"></i></div>
  <div class="chips" id="chips"></div>
  <div id="facets">
    <div class="acc"><button class="acch" id="b0" aria-expanded="false" aria-controls="a0"><span class="num">01</span> Keyword<span class="ar">+</span></button>
      <div class="accp" id="a0" hidden><input type="search" id="kwRail" aria-label="Keyword filter" autocomplete="off"><div class="hint">literal match, not synonyms</div></div></div>
    <div class="acc"><button class="acch" id="b1" aria-expanded="false" aria-controls="a1"><span class="num">02</span> Mechanism, body, type<span class="ar">+</span></button>
      <div class="accp" id="a1" hidden>
        <label for="selMech">Mechanism</label><select id="selMech"></select>
        <label for="selBody">Body or mandate</label><select id="selBody"></select>
        <label for="selType">Type</label><select id="selType"></select>
        <div id="stateWrap"><label for="selState">Recommending State (UPR)</label><select id="selState"></select></div>
        <div class="hint">counts are for the whole file</div>
      </div></div>
    <div class="acc"><button class="acch" id="b2" aria-expanded="false" aria-controls="a2"><span class="num">03</span> Years and SDG<span class="ar">+</span></button>
      <div class="accp" id="a2" hidden>
        <label for="selFrom">Year from</label><select id="selFrom"></select>
        <label for="selTo">Year to</label><select id="selTo"></select>
        <label for="selSdg">SDG</label><select id="selSdg"></select>
        <div class="hint">dated by document</div>
      </div></div>
  </div>
</aside>
<main>
<section role="tabpanel" id="panel0" aria-labelledby="tab0">
  <h2 class="q" id="q0"></h2>
  <div class="tiles" id="headTiles"></div>
  <p class="note">How this is computed: each tile loops over the records in the current filter; documents are distinct symbols; the years are the lowest and highest year.</p>
  <div class="tiles" id="mechTiles"></div>
  <div id="statePanel" hidden></div>
  <p class="note">How this is computed: records, distinct symbols and latest year per mechanism in the current filter; share = records of that mechanism ÷ matching records.</p>
  <figure>
    <figcaption><span class="lbl">FIG.01</span> <span class="ftitle" id="f1title"></span> <span class="hint">click a bar or a theme = filter</span></figcaption>
    <div class="chartbox" id="c1box"><canvas id="c1" role="img" aria-label="Horizontal bar chart of the ten most frequent themes"></canvas></div>
    <p class="empty" id="c1empty" hidden>No records match.</p>
    <p class="note">How this is computed: each theme on a record counts once (the labels chosen by the switch under the title); the ten highest counts are shown, ties in alphabetical order.</p>
    <table id="themeTable"><caption>The ten themes of FIG.01 as a table</caption>
      <thead><tr><th scope="col">Theme</th><th scope="col" class="r">Records</th><th scope="col" class="r">% of filtered</th><th scope="col">Years (first–last)</th></tr></thead><tbody></tbody></table>
    <p class="note">A record can carry several themes, so the bars add up to more than the number of records. A theme whose records span a short, old range of years may be a legacy label: judge a sample on tab 03.</p>
    <p class="src" id="src1"></p>
  </figure>
  <figure>
    <figcaption><span class="lbl">FIG.02</span> <span class="ftitle" id="f2title"></span></figcaption>
    <div class="chartbox s" id="c2box"><canvas id="c2" role="img" aria-label="Stacked bar chart of records per year by mechanism"></canvas></div>
    <p class="empty" id="c2empty" hidden>No records match.</p>
    <p class="note">How this is computed: records per year of the document and per mechanism in the current filter; years without records stay as gaps.</p>
    <p class="src" id="src2"></p>
  </figure>
</section>
<section role="tabpanel" id="panel1" aria-labelledby="tab1" hidden>
  <h2 class="q">Which paragraph says it, and in which UN document?</h2>
  <input type="search" id="kwMain" aria-label="Search records" autocomplete="off">
  <div class="hint">literal match, not synonyms</div>
  <table id="recTable" style="margin-top:12px"><caption id="recCap"></caption>
    <thead><tr><th scope="col"><button class="thbtn" id="dateSort">Date</button></th><th scope="col">Body</th><th scope="col">Symbol</th><th scope="col" class="r">Para.</th><th scope="col">Recommending State</th><th scope="col">First line</th></tr></thead>
    <tbody id="recBody"></tbody></table>
  <p><button class="btn" id="moreBtn" hidden>Show 50 more</button></p>
  <p class="src" id="src3"></p>
</section>
<section role="tabpanel" id="panel2" aria-labelledby="tab2" hidden>
  <h2 class="q">Can I trust these numbers?</h2>
  <h3>Check this dashboard</h3>
  <p class="lbl" style="margin:0 0 10px">How the app checks itself</p>
  <ul class="checks" id="checks"></ul>
  <h3>Check the UN's labels on a random sample</h3>
  <p class="note" style="margin-bottom:8px">This is your judgement of the UN's labels; nothing is sent anywhere. Mark a paragraph "Doesn't fit" or "Unsure" to correct its themes: your correction is shown beside the UN's label, never instead of it.</p>
  <div id="sampleCtl"></div>
  <div class="tally" id="sampleTally" aria-live="polite"></div>
  <ol class="sc" id="sampleCards"></ol>
  <div id="corrPanel" style="margin-top:34px">
    <h3>Your corrections</h3>
    <p class="note" id="corrIntro" style="margin-bottom:10px"></p>
    <p>
      <button class="btn" id="corrToggle" aria-expanded="false" aria-controls="corrList">Show the list</button>
      <button class="btn" id="corrDl">Download corrections CSV</button>
      <button class="btn" id="corrLoad">Load corrections CSV</button>
      <button class="btn" id="corrUndoAll">Undo all corrections</button>
      <input type="file" id="corrFile" accept=".csv,text/csv,text/plain" hidden aria-label="Choose a corrections CSV file">
    </p>
    <p class="copied" id="corrMsg" role="status"></p>
    <div id="corrList" hidden></div>
  </div>
</section>
<section role="tabpanel" id="panel3" aria-labelledby="tab3" hidden>
  <h2 class="q">How was this made, and how do I take it with me?</h2>
  <div class="method" id="methodText"></div>
  <p><button class="btn" id="csvBtn">Download CSV of the current filter</button><button class="btn" id="sumBtn">Copy summary</button> <span class="copied" id="exportMsg" role="status"></span></p>
  <p class="note" id="srcInfo"></p>
</section>
</main>
</div>
<footer id="foot"></footer>
</div>
<script>
(function(){
"use strict";
const $=id=>document.getElementById(id);
const U=(window.WORKSHOP_DATA||{}).uhri;
if(!U||!Array.isArray(U.records)){$('app').innerHTML='<p>The recommendations file is not attached to this conversation.</p>';return;}
const R=U.records, N=R.length, C=U.country||'this country';
const fmt=n=>Number(n).toLocaleString('en-GB');
const esc=s=>String(s==null?'':s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const reEsc=s=>s.replace(/[.*+?^${}()|[\]\\]/g,'\\$&');
const UPR='Universal Periodic Review';
const MCOL={'Universal Periodic Review':'#c2410c','Treaty bodies':'#0f766e','Special Procedures':'#7c3aed'};
const mcol=m=>MCOL[m]||'#6b6558';
const PARA_RE=/^(\d{1,3}(?:\.\d{1,3})?)\.?\s/;
const STATE_RE=/((?:\s*\((?:[^()]|\([^()]*\))*\))+)\s*[;.]?\s*$/;
const GROUP_RE=/\((?:[^()]|\([^()]*\))*\)/g;
const MARKTXT={fit:'Fits',no:"Doesn't fit",un:'Unsure'};

/* ---- enrich records (the UN's own fields are never changed) ---- */
R.forEach((r,i)=>{
  r._i=i; const t=String(r.text||'');
  const pm=t.match(PARA_RE); r._para=pm?pm[1]:null;
  r._pt=pm?pm[1].split('.').map(Number):null;
  if(r._pt&&r._pt.length<2)r._pt.push(0);
  r._lt=t.toLowerCase(); r._ls=String(r.symbol||'').toLowerCase();
  r._states=[]; r._isUpr=r.mechanism===UPR;
  if(r._isUpr){
    const m=t.match(STATE_RE);
    if(m){(m[1].match(GROUP_RE)||[]).forEach(g=>{
      const s=g.slice(1,-1).replace(/\s+/g,' ').trim();
      if(s&&s.indexOf(',')<0&&s.length<=60&&r._states.indexOf(s)<0)r._states.push(s);
    });}
  }
});
const UNSNAP=R.map(r=>JSON.stringify(r.themes||[]));
const years=[...new Set(R.map(r=>r.year).filter(y=>Number.isFinite(y)))].sort((a,b)=>a-b);
const YMIN=years[0],YMAX=years[years.length-1];
const docsAll=new Set(R.map(r=>r.symbol)).size;
const cnt=(arr,f)=>{const m=new Map();arr.forEach(r=>{const v=f(r);if(v!==undefined&&v!==null&&v!=='')m.set(v,(m.get(v)||0)+1)});return m};
const byCount=m=>[...m.entries()].sort((a,b)=>b[1]-a[1]||String(a[0]).localeCompare(String(b[0])));
const MECHS=byCount(cnt(R,r=>r.mechanism)).map(x=>x[0]);
const stateCountsAll=cnt(R.filter(r=>r._isUpr).flatMap(r=>r._states.map(s=>({s}))),x=>x.s);
const sdgSet=[...new Set(R.flatMap(r=>r.sdgs||[]))].sort((a,b)=>a-b);
const themeCountsAll=new Map();
R.forEach(r=>new Set(r.themes||[]).forEach(t=>themeCountsAll.set(t,(themeCountsAll.get(t)||0)+1)));
const ALLTHEMES=[...themeCountsAll.keys()].sort((a,b)=>a.localeCompare(b));

/* ---- state ---- */
const S={kw:'',mech:'',body:'',type:'',state:'',yFrom:YMIN,yTo:YMAX,sdg:null,themes:[],shown:50,dir:1,showStates:false,useMine:true,corrOpen:false};
let filtered=[],view={},active=0,sample=null,charts={c1:null,c2:null},undoAllT=null;
const openRows=new Set();

/* ---- corrections: CORR holds, per record index, the UN labels you removed (rem) and the labels you added (add).
        MARK holds your verdict per record index. The UN's own arrays are never touched. ---- */
const CORR=new Map(), MARK=new Map();
const unT=r=>Array.isArray(r.themes)?r.themes:[];
function mineT(r){const c=CORR.get(r._i);if(!c)return null;return unT(r).filter(x=>c.rem.indexOf(x)<0).concat(c.add);}
const effT=r=>(S.useMine&&CORR.has(r._i))?mineT(r):unT(r);
function nChanges(){let n=0;CORR.forEach(c=>{n+=c.rem.length+c.add.length});return n;}
const pl=(n,w)=>`${fmt(n)} ${w}${n===1?'':'s'}`;
function editLabel(i,act,l){
  const r=R[i];let c=CORR.get(i);if(!c){c={rem:[],add:[]};CORR.set(i,c);}
  if(act==='rm'){
    if(c.add.indexOf(l)>=0)c.add=c.add.filter(x=>x!==l);
    else if(unT(r).indexOf(l)>=0&&c.rem.indexOf(l)<0)c.rem.push(l);
  }else if(act==='add'){
    if(unT(r).indexOf(l)>=0)c.rem=c.rem.filter(x=>x!==l);
    else if(ALLTHEMES.indexOf(l)>=0&&c.add.indexOf(l)<0)c.add.push(l);
  }
  if(!c.rem.length&&!c.add.length)CORR.delete(i);
}
const corrRecords=()=>[...new Set([...CORR.keys(),...MARK.keys()])].sort((a,b)=>a-b);

/* ---- header / footer ---- */
const srcLink=U.source_url&&/^https?:/.test(U.source_url)?`<a href="${esc(U.source_url)}" target="_blank" rel="noopener">${esc(U.source||'source')}</a>`:esc(U.source||'source not stated');
$('hLabel').textContent='UHRI · '+C;
$('hTitle').textContent='UN human rights recommendations and observations: '+C;
document.title='UN human rights recommendations: '+C;
$('hMeta').innerHTML=`Source: ${srcLink} · ${fmt(N)} records · ${fmt(docsAll)} documents · ${YMIN}–${YMAX} · built ${esc(U.built||'date not stated')} · <span class="lbl">dated by document</span>`;
$('foot').innerHTML=`Built on OHCHR UHRI data · ${fmt(N)} records · ${srcLink}`;
$('q0').textContent=`What has the UN said about ${C}, how much, and when?`;
$('kwMain').placeholder=`Search ${fmt(N)} records, e.g. torture`;
$('kwRail').placeholder='e.g. torture';
function renderCorrLine(){
  const n=nChanges();
  $('corrLine').textContent=`${pl(n,'label')} corrected by you; the UN's own labels are kept`;
  $('modeSw').setAttribute('aria-checked',String(S.useMine));
  $('swUn').className=S.useMine?'':'on';
  $('swMine').className=S.useMine?'on':'';
}
function labelNote(){
  const n=nChanges();
  if(!n)return "Labels: the UN's own.";
  return S.useMine?`Labels: with your ${pl(n,'correction')} on ${pl(CORR.size,'record')}; the UN's own labels are kept.`:`Labels: the UN's own (your ${pl(n,'correction')} switched off).`;
}

/* ---- filters ---- */
function applyFilters(){
  const words=S.kw.trim().toLowerCase().split(/\s+/).filter(Boolean);
  return R.filter(r=>{
    if(S.mech&&r.mechanism!==S.mech)return false;
    if(S.body&&r.body!==S.body)return false;
    if(S.type&&r.type!==S.type)return false;
    if(S.state&&r._states.indexOf(S.state)<0)return false;
    if(r.year<S.yFrom||r.year>S.yTo)return false;
    if(S.sdg!=null&&!(r.sdgs||[]).includes(S.sdg))return false;
    if(S.themes.length){const t=effT(r);if(!S.themes.every(x=>t.includes(x)))return false;}
    for(const w of words){if(r._lt.indexOf(w)<0&&r._ls.indexOf(w)<0)return false;}
    return true;
  });
}
function sortRecords(a){
  return a.slice().sort((x,y)=>{
    const c=String(x.date||'').localeCompare(String(y.date||''));if(c)return -c*S.dir;
    const b=String(x.body||'').localeCompare(String(y.body||''));if(b)return b;
    const px=x._pt||[1e9,0],py=y._pt||[1e9,0];
    if(px[0]!==py[0])return px[0]-py[0];
    if(px[1]!==py[1])return px[1]-py[1];
    return x._i-y._i;
  });
}
function describeFilters(){
  const d=[];
  if(S.kw.trim())d.push(`keyword "${S.kw.trim()}"`);
  if(S.mech)d.push('mechanism = '+S.mech);
  if(S.body)d.push('body = '+S.body);
  if(S.type)d.push('type = '+S.type);
  if(S.state)d.push('recommending State = '+S.state);
  if(S.yFrom!==YMIN||S.yTo!==YMAX)d.push(`years ${S.yFrom}–${S.yTo}`);
  if(S.sdg!=null)d.push('SDG '+S.sdg);
  S.themes.forEach(t=>d.push('theme = '+t));
  return d;
}
function chipList(){
  const c=[];
  if(S.kw.trim())c.push({l:'Keyword: '+S.kw.trim(),f:()=>{S.kw=''}});
  if(S.mech)c.push({l:'Mechanism: '+S.mech,f:()=>{S.mech=''}});
  if(S.body)c.push({l:'Body: '+S.body,f:()=>{S.body=''}});
  if(S.type)c.push({l:'Type: '+S.type,f:()=>{S.type=''}});
  if(S.state)c.push({l:'State: '+S.state,f:()=>{S.state=''}});
  if(S.yFrom!==YMIN||S.yTo!==YMAX)c.push({l:`Years: ${S.yFrom}–${S.yTo}`,f:()=>{S.yFrom=YMIN;S.yTo=YMAX}});
  if(S.sdg!=null)c.push({l:'SDG '+S.sdg,f:()=>{S.sdg=null}});
  S.themes.forEach(t=>c.push({l:'Theme: '+t,f:()=>{S.themes=S.themes.filter(x=>x!==t)}}));
  return c;
}
function setSel(sel,items,cur){
  sel.innerHTML=items.map(([v,l])=>`<option value="${esc(v)}">${esc(l)}</option>`).join('');
  sel.value=cur;if(sel.selectedIndex<0)sel.selectedIndex=0;
}
function buildSelects(){
  setSel($('selMech'),[['',`All (${fmt(N)})`],...byCount(cnt(R,r=>r.mechanism)).map(([v,c])=>[v,`${v} (${fmt(c)})`])],S.mech);
  const pool=S.mech?R.filter(r=>r.mechanism===S.mech):R;
  const bodies=byCount(cnt(pool,r=>r.body));
  if(S.body&&!bodies.some(b=>b[0]===S.body))S.body='';
  setSel($('selBody'),[['',`All (${fmt(pool.length)})`],...bodies.map(([v,c])=>[v,`${v} (${fmt(c)})`])],S.body);
  const pool2=S.body?pool.filter(r=>r.body===S.body):pool;
  const types=byCount(cnt(pool2,r=>r.type));
  if(S.type&&!types.some(b=>b[0]===S.type))S.type='';
  setSel($('selType'),[['',`All (${fmt(pool2.length)})`],...types.map(([v,c])=>[v,`${v} (${fmt(c)})`])],S.type);
  const st=byCount(stateCountsAll);
  $('stateWrap').hidden=!st.length;
  setSel($('selState'),[['',`All (${st.length} States found)`],...st.map(([v,c])=>[v,`${v} (${fmt(c)})`])],S.state);
  setSel($('selFrom'),years.map(y=>[String(y),String(y)]),String(S.yFrom));
  setSel($('selTo'),years.map(y=>[String(y),String(y)]),String(S.yTo));
  const sn=U.sdg_names||{};
  setSel($('selSdg'),[['','All goals'],...sdgSet.map(g=>[String(g),`${g} · ${sn[String(g)]||''}`])],S.sdg==null?'':String(S.sdg));
  $('kwRail').value=S.kw;$('kwMain').value=S.kw;
}
function onFilter(){S.shown=50;sample=null;render();}

/* ---- rail ---- */
function renderRail(){
  const n=filtered.length;
  $('matchN').textContent=fmt(n);
  $('matchOf').textContent=`matching records of ${fmt(N)} in the file`;
  $('matchBar').style.width=(N?n/N*100:0)+'%';
  const cl=chipList();view.chips=cl;
  $('chips').innerHTML=cl.map((c,k)=>`<button class="fchip" data-k="${k}" aria-label="Remove filter ${esc(c.l)}">${esc(c.l)} ×</button>`).join('');
}

/* ---- stats ---- */
function themeStats(arr){
  const m=new Map();
  for(const r of arr){
    for(const t of new Set(effT(r))){
      let e=m.get(t);if(!e){e={t,c:0,min:Infinity,max:-Infinity};m.set(t,e);}
      e.c++;if(Number.isFinite(r.year)){if(r.year<e.min)e.min=r.year;if(r.year>e.max)e.max=r.year;}
    }
  }
  return [...m.values()].sort((a,b)=>b.c-a.c||a.t.localeCompare(b.t));
}
const yrs=(a,b)=>!Number.isFinite(a)?'–':a===b?String(a):`${a}–${b}`;
function typeBreakdown(arr){const m=cnt(arr,r=>r.type||'(no type)');return byCount(m);}
function topStates(arr){
  const m=new Map();arr.forEach(r=>r._states.forEach(s=>m.set(s,(m.get(s)||0)+1)));return byCount(m);
}

/* ---- label display (UN label, your label, struck-through UN label) ---- */
const plainTag=x=>`<span class="tag">${esc(x)}</span>`;
function themeTagsHTML(r,forceDiff){
  const un=unT(r),c=CORR.get(r._i);
  if(c&&(S.useMine||forceDiff)){
    return un.map(x=>c.rem.indexOf(x)>=0?`<span class="tag struck"><del>${esc(x)}</del><span class="sr"> (UN label, removed by you)</span></span>`:plainTag(x)).join('')
      +c.add.map(x=>`<span class="tag mine">${esc(x)}<span class="sr"> (added by you)</span></span>`).join('')
      +'<span class="ctag">corrected by you</span>';
  }
  let h=un.length?un.map(plainTag).join(''):'<span class="miss">not labelled</span>';
  if(c)h+=' <span class="miss">your correction is hidden while "UN labels" is on</span>';
  return h;
}

/* ---- overview ---- */
function renderOverview(){
  const f=filtered,n=f.length;
  const bd=typeBreakdown(f);view.breakdown=bd;
  const docs=new Set(f.map(r=>r.symbol)).size;
  const ys=f.map(r=>r.year).filter(Number.isFinite);
  const y0=ys.length?Math.min(...ys):null,y1=ys.length?Math.max(...ys):null;
  $('headTiles').innerHTML=
   `<div class="tile"><div class="lbl">Records</div><div class="n">${fmt(n)}</div><div class="sub">${n?bd.map(([t,c])=>`${fmt(c)} ${esc(t)}`).join(' · '):'No records match'}</div><div class="sub lbl">of ${fmt(N)} in the file</div></div>
    <div class="tile"><div class="lbl">Documents</div><div class="n">${fmt(docs)}</div><div class="sub">distinct symbols</div></div>
    <div class="tile"><div class="lbl">Years</div><div class="n">${y0==null?'–':y0===y1?y0:y0+'–'+y1}</div><div class="sub">year of the document</div></div>`;
  $('mechTiles').innerHTML=MECHS.map(m=>{
    const a=f.filter(r=>r.mechanism===m),d=new Set(a.map(r=>r.symbol)).size;
    const my=a.map(r=>r.year).filter(Number.isFinite);
    return `<div class="tile"><div class="lbl"><span class="dot" style="background:${mcol(m)}"></span>${esc(m)}</div><div class="n" style="font-size:40px">${fmt(a.length)}</div>
      <div class="sub">${fmt(d)} documents · latest ${my.length?Math.max(...my):'–'} · ${n?(a.length/n*100).toFixed(1)+'%':'–'} of matching</div>
      ${m===UPR?`<div class="sub"><button class="linkbtn" id="stBtn" aria-expanded="${S.showStates}">${S.showStates?'hide the States':'see the States'}</button></div>`:''}</div>`;
  }).join('');
  const sp=$('statePanel');sp.hidden=!S.showStates;
  if(S.showStates){
    const up=f.filter(r=>r._isUpr),ts=topStates(f).slice(0,10),nf=up.filter(r=>!r._states.length).length;
    sp.innerHTML=`<h3 style="font-size:20px">Ten States that made most recommendations to ${esc(C)}</h3>
     ${ts.length?`<table><caption>Recommendations per State in the current filter (${fmt(up.length)} UPR records)</caption><thead><tr><th scope="col">State</th><th scope="col" class="r">Recommendations</th></tr></thead><tbody>${ts.map(([s,c])=>`<tr><td>${esc(s)}</td><td class="r">${fmt(c)}</td></tr>`).join('')}</tbody></table>`:'<p class="empty">No UPR records with a State in the current filter.</p>'}
     <p class="note">A count of recommendations, not of influence; a line made by several States counts once for each. UPR records without a State found: ${fmt(nf)}.</p>`;
  }
  const ts=themeStats(f).slice(0,10);
  view.chartLabels=ts.map(x=>x.t);view.chartValues=ts.map(x=>x.c);
  $('f1title').textContent=n?`Ten most frequent themes among ${fmt(n)} filtered records`:'Themes: no records match';
  $('themeTable').querySelector('tbody').innerHTML=ts.length?ts.map(x=>`<tr><td><button class="tbtn" data-theme="${esc(x.t)}">${esc(x.t)}</button></td><td class="r">${fmt(x.c)}</td><td class="r">${(x.c/n*100).toFixed(1)}%</td><td>${yrs(x.min,x.max)}</td></tr>`).join(''):'<tr><td colspan="4" class="miss">No records match, or none carries a theme.</td></tr>';
  const src=`Source: OHCHR UHRI, ${esc(U.source||'')}; n = ${fmt(n)} of ${fmt(N)} records; filter: ${esc(describeFilters().join('; ')||'none')}. ${esc(labelNote())}`;
  $('src1').innerHTML=src;$('src2').innerHTML=src;
  const fy=f.map(r=>r.year).filter(Number.isFinite);
  view.tl=null;
  if(fy.length){
    const a=Math.min(...fy),b=Math.max(...fy),labels=[];for(let y=a;y<=b;y++)labels.push(y);
    const m=new Map();f.forEach(r=>{const k=r.year+'|'+r.mechanism;m.set(k,(m.get(k)||0)+1)});
    view.tl={labels,sets:MECHS.map(mm=>({label:mm,data:labels.map(y=>m.get(y+'|'+mm)||0),backgroundColor:mcol(mm),borderWidth:0})).filter(s=>s.data.some(v=>v>0))};
    $('f2title').textContent=`Records per year by mechanism, ${a}–${b}, for ${fmt(n)} filtered records`;
  }else $('f2title').textContent='Records per year: no records match';
  if(active===0)drawCharts();
}
const valuePlugin={id:'vals',afterDatasetsDraw(chart){
  const ctx=chart.ctx,meta=chart.getDatasetMeta(0);ctx.save();ctx.fillStyle='#1d1b18';ctx.font='13px ui-monospace,Menlo,Consolas,monospace';ctx.textBaseline='middle';
  meta.data.forEach((bar,i)=>ctx.fillText(fmt(chart.data.datasets[0].data[i]),bar.x+6,bar.y));ctx.restore();}};
function drawCharts(){
  if(typeof Chart==='undefined')return;
  if(charts.c1){charts.c1.destroy();charts.c1=null}
  if(charts.c2){charts.c2.destroy();charts.c2=null}
  const lab=view.chartLabels||[];
  $('c1box').hidden=!lab.length;$('c1empty').hidden=!!lab.length;
  if(lab.length){
    const tr=s=>s.length>40?s.slice(0,39)+'…':s;
    charts.c1=new Chart($('c1'),{type:'bar',data:{labels:lab.map(tr),datasets:[{data:view.chartValues,backgroundColor:'rgba(155,35,53,.8)',borderWidth:0,barPercentage:.78}]},
      options:{indexAxis:'y',animation:false,responsive:true,maintainAspectRatio:false,layout:{padding:{right:46}},
        plugins:{legend:{display:false},tooltip:{callbacks:{title:it=>lab[it[0].dataIndex],label:i=>fmt(i.raw)+' records (click to filter)'}}},
        scales:{x:{display:false,beginAtZero:true,grid:{display:false}},y:{grid:{display:false},border:{display:false},ticks:{color:'#1d1b18',font:{size:13}}}},
        onClick:(e,els)=>{if(els.length)addTheme(lab[els[0].index]);},
        onHover:(e,els)=>{e.native.target.style.cursor=els.length?'pointer':'default'}},plugins:[valuePlugin]});
  }
  const tl=view.tl;
  $('c2box').hidden=!tl;$('c2empty').hidden=!!tl;
  if(tl){
    charts.c2=new Chart($('c2'),{type:'bar',data:{labels:tl.labels.map(String),datasets:tl.sets},
      options:{animation:false,responsive:true,maintainAspectRatio:false,
        plugins:{legend:{position:'top',align:'start',labels:{usePointStyle:true,boxWidth:9,color:'#1d1b18',font:{size:13}}}},
        scales:{x:{stacked:true,grid:{display:false},ticks:{color:'#1d1b18',maxRotation:0,autoSkip:true}},y:{stacked:true,beginAtZero:true,grid:{color:'#e6dfd0'},border:{display:false},ticks:{precision:0,color:'#5c564b'}}}}});
  }
}
function addTheme(t){if(S.themes.indexOf(t)<0){S.themes.push(t);onFilter();}}

/* ---- records ---- */
function hl(raw,words){
  raw=String(raw);if(!words.length)return esc(raw);
  const re=new RegExp(words.slice().sort((a,b)=>b.length-a.length).map(reEsc).join('|'),'gi');
  let out='',last=0,m;
  while((m=re.exec(raw))){if(!m[0]){re.lastIndex++;continue}out+=esc(raw.slice(last,m.index))+'<mark>'+esc(m[0])+'</mark>';last=m.index+m[0].length;}
  return out+esc(raw.slice(last));
}
const kwWords=()=>S.kw.trim().toLowerCase().split(/\s+/).filter(Boolean);
function firstLine(t){
  t=String(t||'');if(t.length<=120)return t;
  let c=t.slice(0,120);const k=c.lastIndexOf(' ');if(k>40)c=c.slice(0,k);
  return c.trimEnd()+'…';
}
const cite=r=>r._para?`${r.symbol}, para. ${r._para}`:String(r.symbol||'');
const stateCell=r=>r._isUpr?(r._states.length?esc(r._states.join('; ')):'<span class="miss">State not found</span>'):'–';
function detailHTML(r){
  const tags=a=>a&&a.length?a.map(plainTag).join(''):'<span class="miss">not labelled</span>';
  const sn=U.sdg_names||{};
  const sd=(r.sdgs||[]).map(g=>`SDG ${g} ${sn[String(g)]||''}`.trim());
  return `<tr class="detail"><td colspan="6"><div class="dgrid"><div><div class="lbl">Paragraph</div><div class="pnum">${r._para?esc(r._para):'–'}</div></div>
  <div><p class="ptext">${hl(r.text,kwWords())}</p>
  <dl class="lab"><dt>Themes</dt><dd>${themeTagsHTML(r,false)}</dd><dt>SDGs</dt><dd>${tags(sd)}</dd><dt>SDG targets</dt><dd>${tags(r.sdg_targets)}</dd><dt>Affected persons</dt><dd>${tags(r.affected_persons)}</dd>
  ${r.section?`<dt>Section</dt><dd>${esc(r.section)}</dd>`:''}<dt>Type</dt><dd>${esc(r.type||'not stated')}</dd>${r._isUpr?`<dt>Recommending State</dt><dd>${r._states.length?esc(r._states.join('; ')):'<span class="miss">State not found</span>'}</dd>`:''}</dl>
  <button class="btn" data-act="cite" data-i="${r._i}">${r._para?'Copy citation':'Copy citation (no paragraph number in this extract)'}</button>
  <a class="btn" href="${esc(r.doc_url)}" target="_blank" rel="noopener">Open the UN document</a> <span class="copied" role="status"></span></div></div></td></tr>`;
}
function rowHTML(r){
  const w=kwWords(),mark=S.useMine&&CORR.has(r._i)?'<span class="ctag">corrected by you</span>':'';
  return `<tr class="row" tabindex="0" data-i="${r._i}" aria-expanded="${openRows.has(r._i)}"><td>${esc(r.date||'')}</td><td>${esc(r.body||'')}</td>
   <td><a href="${esc(r.doc_url)}" target="_blank" rel="noopener">${esc(r.symbol)}</a></td><td class="r">${r._para?esc(r._para):'–'}</td><td>${stateCell(r)}</td><td>${hl(firstLine(r.text),w)}${mark}</td></tr>`+(openRows.has(r._i)?detailHTML(r):'');
}
function renderRecords(){
  const n=filtered.length,rows=filtered.slice(0,S.shown);
  $('recCap').textContent=n?`Showing ${fmt(rows.length)} of ${fmt(n)} matching records, ${S.dir===1?'newest first':'oldest first'}. Click a row to open the full paragraph.`:'No records match the current filter.';
  $('dateSort').textContent='Date '+(S.dir===1?'↓':'↑');
  $('dateSort').setAttribute('aria-label','Date, '+(S.dir===1?'newest first':'oldest first')+'; click to reverse');
  $('recBody').innerHTML=rows.map(rowHTML).join('');
  const more=n-rows.length;$('moreBtn').hidden=more<=0;$('moreBtn').textContent=`Show 50 more (${fmt(more)} left)`;
  $('src3').innerHTML=`Source: OHCHR UHRI, ${esc(U.source||'')}; n = ${fmt(n)} of ${fmt(N)} records. Sorted by date, then body, then paragraph number. ${esc(labelNote())}`;
}
function toggleRow(tr){
  const i=Number(tr.dataset.i),r=R[i];
  if(openRows.has(i)){openRows.delete(i);tr.setAttribute('aria-expanded','false');const nx=tr.nextElementSibling;if(nx&&nx.classList.contains('detail'))nx.remove();}
  else{openRows.add(i);tr.setAttribute('aria-expanded','true');tr.insertAdjacentHTML('afterend',detailHTML(r));}
}
async function copyText(t){
  try{await navigator.clipboard.writeText(t);return true}catch(e){
    try{const ta=document.createElement('textarea');ta.value=t;ta.style.cssText='position:fixed;opacity:0';document.body.appendChild(ta);ta.select();const ok=document.execCommand('copy');ta.remove();return ok}catch(e2){return false}
  }
}
function flash(el,ok){el.textContent=ok?'Copied':'Copy was blocked by the browser';setTimeout(()=>{el.textContent=''},2000);}

/* ---- checks ---- */
function runChecks(){
  const out=[],add=(status,name,detail,extra)=>out.push({status,name,detail,extra});
  const declared=Number(U.count);
  add(declared===N?'pass':'fail','Record count',`records.length = ${fmt(N)}; declared count = ${isNaN(declared)?'missing':fmt(declared)}`);
  [['mechanism'],['body'],['year']].forEach(([f])=>{
    const m=cnt(R,r=>r[f]);let s=0;m.forEach(v=>s+=v);const miss=N-s;
    add(s===N?'pass':'fail',`Counts per ${f} add up`,`${m.size} values; sum ${fmt(s)} vs ${fmt(N)} records${miss?`; ${fmt(miss)} without a value`:''}`);
  });
  const bs=(view.breakdown||[]).reduce((a,x)=>a+x[1],0);
  add(bs===filtered.length?'pass':'fail','Type partition (current filter)',`counts per type sum to ${fmt(bs)}; headline total ${fmt(filtered.length)}`);
  const lab=view.chartLabels||[],vals=view.chartValues||[];
  const badBars=[];lab.forEach((t,i)=>{const c=filtered.filter(r=>effT(r).includes(t)).length;if(c!==vals[i])badBars.push(`${t}: bar ${vals[i]}, recount ${c}`)});
  add(badBars.length?'fail':'pass','Chart against recount',badBars.length?badBars.join('; '):`${lab.length} bars recounted by a second loop (${S.useMine&&CORR.size?'with your corrections':"UN's own labels"}), all equal`);
  const rows=[...document.querySelectorAll('#themeTable tbody tr')].filter(tr=>tr.children.length>1).map(tr=>({t:tr.children[0].textContent,c:Number(tr.children[1].textContent.replace(/,/g,''))}));
  const badRows=lab.length!==rows.length||lab.some((t,i)=>rows[i]&&(rows[i].t!==t||rows[i].c!==vals[i]));
  add(badRows?'fail':'pass','Chart against table',`${lab.length} bars, ${rows.length} table rows; ${badRows?'values differ':'same themes and values'}`);
  const mx=vals.length?Math.max(...vals):0;
  add(mx<=filtered.length?'pass':'fail','Largest bar ≤ filtered count',`largest bar ${fmt(mx)}; filtered records ${fmt(filtered.length)}`);
  /* corrections */
  const changedUN=R.filter((r,i)=>JSON.stringify(r.themes||[])!==UNSNAP[i]);
  add(changedUN.length?'fail':'pass',"UN labels kept",`${fmt(N)} records compared with the copy taken at load; ${fmt(changedUN.length)} differ`);
  const badC=[];CORR.forEach((c,i)=>{const r=R[i],u=unT(r);
    c.add.forEach(x=>{if(ALLTHEMES.indexOf(x)<0)badC.push(`${r.symbol}: "${x}" is not a label in the data`);else if(u.indexOf(x)>=0)badC.push(`${r.symbol}: "${x}" is already a UN label`)});
    c.rem.forEach(x=>{if(u.indexOf(x)<0)badC.push(`${r.symbol}: "${x}" was not a UN label`)});});
  add(badC.length?'fail':'pass','Your corrections are valid',badC.length?badC.slice(0,8).join('; '):`${pl(CORR.size,'corrected record')}; every label you added occurs in the data, every label you removed was a UN label`);
  let sumUN=0,sumView=0,rem=0,ad=0;
  R.forEach(r=>{sumUN+=new Set(unT(r)).size;sumView+=new Set(effT(r)).size;const c=CORR.get(r._i);if(c){rem+=c.rem.length;ad+=c.add.length}});
  const expected=sumUN+(S.useMine?ad-rem:0);
  add(sumView===expected?'pass':'fail','Label totals follow the switch',`labels in view ${fmt(sumView)}; expected ${fmt(sumUN)} UN labels ${S.useMine?`− ${fmt(rem)} removed + ${fmt(ad)} added = ${fmt(expected)}`:'(corrections switched off)'}`);
  /* links, paragraphs, states, ids */
  const badL=R.filter(r=>{const u=String(r.doc_url||'');if(!u.startsWith('https://docs.un.org/')||!r.symbol)return true;let d=u;try{d=decodeURIComponent(u)}catch(e){}return !d.toLowerCase().endsWith(String(r.symbol).toLowerCase())});
  add(badL.length?'fail':'pass','Links to UN documents',`${fmt(N-badL.length)} of ${fmt(N)} doc_url values start with https://docs.un.org/ and end with the symbol`,badL.length?'Failing: '+[...new Set(badL.map(r=>r.symbol))].slice(0,15).join(', ')+(badL.length>15?' …':''):'');
  const pm=MECHS.map(m=>{const a=R.filter(r=>r.mechanism===m),w=a.filter(r=>r._para).length;return {m,w,t:a.length,p:a.length?w/a.length*100:0}});
  const up=pm.find(x=>x.m===UPR);
  add(up&&up.w<up.t?'warn':'pass','Paragraph numbers found',pm.map(x=>`${x.m} ${x.p.toFixed(1)}% (${fmt(x.w)}/${fmt(x.t)})`).join(' · ')+(up?'; UPR expected at 100%':''));
  const upr=R.filter(r=>r._isUpr),noS=upr.filter(r=>!r._states.length);
  add(noS.length?'warn':'pass','States found (UPR)',`${fmt(upr.length-noS.length)} of ${fmt(upr.length)} UPR records have at least one State; ${stateCountsAll.size} distinct States`,
    noS.length?'Without a State: '+noS.slice(0,15).map(r=>`${r.symbol} … ${String(r.text).slice(-70).replace(/\s+/g,' ')}`).join('\n')+(noS.length>15?`\n… and ${noS.length-15} more`:''):'');
  const ids=new Set(R.map(r=>r.id)).size;
  add(ids===N?'pass':'fail','Distinct ids',`${fmt(ids)} distinct id values vs ${fmt(N)} records`);
  const dup=N-new Set(R.map(r=>r.text)).size;
  add(dup?'warn':'pass','Duplicate texts',`${fmt(dup)} records repeat the text of another record (kept, counted as records)`);
  const nl=f=>R.filter(r=>!(r[f]&&r[f].length)).length;
  const nlT=R.filter(r=>!effT(r).length).length,nlTU=nl('themes');
  add('info','Not labelled',`no themes: ${fmt(nlT)}${nlT!==nlTU?` (UN: ${fmt(nlTU)})`:''} · no SDGs: ${fmt(nl('sdgs'))} · no affected persons: ${fmt(nl('affected_persons'))} (of ${fmt(N)}); shown as "not labelled", never filled in`);
  return out;
}
const MARK_ST={pass:'✓ pass',fail:'✗ check failed',warn:'! warning',info:'i note'};
function renderCheck(){
  $('checks').innerHTML=runChecks().map(c=>`<li><span class="st ${c.status}">${MARK_ST[c.status]}</span><div><div class="cn">${esc(c.name)}</div><div class="cd">${esc(c.detail)}</div>${c.extra?`<div class="cx">${esc(c.extra)}</div>`:''}</div></li>`).join('');
  renderSample();
  renderCorrPanel();
}

/* ---- sample ---- */
function mulberry32(a){return function(){a|=0;a=a+0x6D2B79F5|0;let t=Math.imul(a^a>>>15,1|a);t=t+Math.imul(t^t>>>7,61|t)^t;return((t^t>>>14)>>>0)/4294967296}}
function draw(seed){
  const idx=filtered.slice().sort((a,b)=>a._i-b._i).map(r=>r._i),rng=mulberry32(seed),k=Math.min(10,idx.length);
  for(let i=0;i<k;i++){const j=i+Math.floor(rng()*(idx.length-i));const t=idx[i];idx[i]=idx[j];idx[j]=t;}
  sample={seed,ids:idx.slice(0,k),open:null};
  renderSample();
}
function renderSample(){
  const ctl=$('sampleCtl');
  if(!sample){
    ctl.innerHTML=filtered.length?`<button class="btn" data-act="sdraw">Check 10 at random</button><span class="hint">draws ${Math.min(10,filtered.length)} of the ${fmt(filtered.length)} records in the current filter</span>`:'<p class="empty">No records match, so there is nothing to draw.</p>';
    $('sampleTally').textContent='';$('sampleCards').innerHTML='';return;
  }
  const keep=document.activeElement&&document.activeElement.id==='seedIn'?$('seedIn').value:sample.seed;
  ctl.innerHTML=`<div class="seed"><button class="btn" data-act="sagain">Draw again</button><label class="lbl" for="seedIn">Seed</label><input type="number" id="seedIn" min="0" step="1" value="${esc(keep)}"><button class="btn" data-act="sseed">Draw with this seed</button></div><div class="hint">same filter and same seed give the same ten records</div>`;
  renderCards();
}
function editChips(r){
  const un=unT(r),c=CORR.get(r._i)||{rem:[],add:[]},i=r._i;
  const a=un.map(x=>c.rem.indexOf(x)>=0
    ?`<span class="tag struck"><del>${esc(x)}</del><span class="sr"> (UN label, removed by you)</span><button class="xbtn" data-act="lrestore" data-i="${i}" data-l="${esc(x)}" aria-label="Restore the UN label ${esc(x)}">restore</button></span>`
    :`<span class="tag">${esc(x)}<button class="xbtn" data-act="lremove" data-i="${i}" data-l="${esc(x)}" aria-label="Remove the label ${esc(x)} from this paragraph">×</button></span>`).join('');
  const b=c.add.map(x=>`<span class="tag mine">${esc(x)}<span class="sr"> (added by you)</span><button class="xbtn" data-act="lremove" data-i="${i}" data-l="${esc(x)}" aria-label="Remove your label ${esc(x)}">×</button></span>`).join('');
  const none=!un.length&&!c.add.length?'<span class="miss">not labelled by the UN</span>':'';
  return a+b+none+(CORR.has(i)?'<span class="ctag">corrected by you</span>':'');
}
function editorControls(r){
  const cur=mineT(r)||unT(r),opts=ALLTHEMES.filter(x=>cur.indexOf(x)<0);
  return `<div class="editor"><div class="lbl" style="margin-bottom:6px">Correct the themes of this paragraph</div>
   <div class="hint" style="margin:0 0 8px">× removes a label from your view (the UN's label stays, struck through); add only labels that occur in the data</div>
   <label class="sr" for="addSel">Add a label that occurs in the data</label>
   <select id="addSel"><option value="">Add a label that occurs in the data…</option>${opts.map(x=>`<option value="${esc(x)}">${esc(x)} (${fmt(themeCountsAll.get(x)||0)})</option>`).join('')}</select>
   <button class="btn" data-act="ladd" data-i="${r._i}">Add label</button>
   ${CORR.has(r._i)?`<button class="btn" data-act="lundo" data-i="${r._i}">Undo corrections on this paragraph</button>`:''}</div>`;
}
function renderCards(){
  $('sampleCards').innerHTML=sample.ids.map((id,k)=>{
    const r=R[id],v=MARK.get(id),open=sample.open===k,c=CORR.get(id);
    const showEd=open&&(v==='no'||v==='un'||!!c);
    return `<li><button class="sline" data-act="sopen" data-k="${k}" aria-expanded="${open}"><span class="num">${String(k+1).padStart(2,'0')}</span><span>${esc(cite(r))}${c?'<span class="ctag">corrected by you</span>':''}</span><span class="vm">${v?MARKTXT[v]:'not judged'}</span></button>
    <div class="sbody" ${open?'':'hidden'}><div class="lbl"><a href="${esc(r.doc_url)}" target="_blank" rel="noopener">${esc(r.symbol)}</a> · ${r._para?'para. '+esc(r._para):'no paragraph number'} · ${esc(r.date||'')} · ${esc(r.body||'')}</div>
    <blockquote>${esc(r.text)}</blockquote>
    <div class="lbl" style="margin-bottom:4px">UN themes on this paragraph${c?' · your corrections beside them':''}</div><div>${showEd?editChips(r):themeTagsHTML(r,true)}</div>
    <div style="margin-top:8px">${Object.keys(MARKTXT).map(x=>`<button class="btn" data-act="verdict" data-k="${k}" data-v="${x}" aria-pressed="${v===x}">${MARKTXT[x]}</button>`).join('')}</div>
    ${showEd?editorControls(r):(open?'<div class="hint">mark "Doesn\'t fit" or "Unsure" to correct the themes</div>':'')}</div></li>`;
  }).join('');
  const c={fit:0,no:0,un:0};sample.ids.forEach(id=>{const v=MARK.get(id);if(v)c[v]++});
  const j=c.fit+c.no+c.un;
  $('sampleTally').textContent=`Themes: ${c.fit} fit, ${c.no} don't, ${c.un} unsure of ${sample.ids.length} drawn (${j} judged) · seed ${sample.seed} · your judgement, not the UN's`;
}

/* ---- corrections panel, CSV out and in ---- */
function corrListHTML(){
  const ids=corrRecords();
  if(!ids.length)return '<p class="empty">Nothing to list yet.</p>';
  const rows=ids.map(i=>{
    const r=R[i],c=CORR.get(i),un=unT(r),mine=mineT(r)||un;
    const unH=un.length?un.map(x=>c&&c.rem.indexOf(x)>=0?`<span class="tag struck"><del>${esc(x)}</del></span>`:plainTag(x)).join(''):'–';
    const myH=mine.length?mine.map(x=>c&&c.add.indexOf(x)>=0?`<span class="tag mine">${esc(x)}</span>`:plainTag(x)).join(''):'–';
    return `<tr><td><a href="${esc(r.doc_url)}" target="_blank" rel="noopener">${esc(r.symbol)}</a></td><td class="r">${r._para?esc(r._para):'–'}</td><td>${unH}</td><td>${myH}</td><td>${MARK.has(i)?esc(MARKTXT[MARK.get(i)]):'–'}</td><td><button class="btn" data-act="cundo" data-i="${i}" aria-label="Undo the correction and mark on ${esc(cite(r))}">Undo</button></td></tr>`;
  }).join('');
  return `<table><caption>Your corrections and marks: ${pl(ids.length,'record')}. The UN's labels are in the first label column, yours in the second.</caption>
   <thead><tr><th scope="col">Symbol</th><th scope="col" class="r">Para.</th><th scope="col">UN labels</th><th scope="col">My labels</th><th scope="col">My mark</th><th scope="col"><span class="sr">Undo</span></th></tr></thead><tbody>${rows}</tbody></table>
   <p class="src">Source: your judgements in this page; the records are from OHCHR UHRI, ${esc(U.source||'')}.</p>`;
}
function renderCorrPanel(){
  const ids=corrRecords(),nl=nChanges();
  $('corrIntro').textContent=ids.length
    ?`${pl(nl,'label')} changed on ${pl(CORR.size,'record')}; ${pl(MARK.size,'paragraph')} marked. They live only while this page is open: download the CSV to keep them. "Load corrections CSV" merges a file into your current corrections (the file wins on the same record).`
    :'No corrections yet. Open a sampled paragraph above, mark it "Doesn\'t fit" or "Unsure", then remove a label or add one that occurs in the data. Corrections last only while this page is open: download them as CSV to keep them.';
  $('corrDl').disabled=!ids.length;$('corrUndoAll').disabled=!ids.length;$('corrToggle').disabled=!ids.length;
  if(!ids.length)S.corrOpen=false;
  $('corrToggle').setAttribute('aria-expanded',String(S.corrOpen));
  $('corrToggle').textContent=S.corrOpen?'Hide the list':`Show the list (${fmt(ids.length)})`;
  $('corrList').hidden=!S.corrOpen;
  if(S.corrOpen)$('corrList').innerHTML=corrListHTML();
  if(undoAllT){clearTimeout(undoAllT);undoAllT=null;}
  $('corrUndoAll').textContent='Undo all corrections';
}
function afterCorrection(msg,force){
  if(force!==false)S.useMine=true;
  render();
  $('corrMsg').textContent=msg||'';
}
const csvEsc=v=>{const s=String(v==null?'':v);return /[",\n\r]/.test(s)?'"'+s.replace(/"/g,'""')+'"':s};
function buildCorrCSV(){
  const ids=corrRecords();
  const L=['# Your corrections to the UN labels (themes): '+C,'# Source: '+(U.source||'')+' '+(U.source_url||''),'# Data built: '+(U.built||''),
   '# Rows: '+ids.length+' (records you corrected or marked). The UN labels are kept in the column UN labels; yours are in My labels.',
   '# Load this file on the Check tab to restore them.',
   ['Symbol','Paragraph','UN labels','My labels','My mark','Record id'].join(',')];
  ids.forEach(i=>{const r=R[i];L.push([r.symbol,r._para||'',unT(r).join(' | '),(mineT(r)||unT(r)).join(' | '),MARK.has(i)?MARKTXT[MARK.get(i)]:'',r.id].map(csvEsc).join(','));});
  return L.join('\r\n');
}
function parseCSV(text){
  text=text.replace(/^\uFEFF/,'').replace(/^(?:#[^\r\n]*(?:\r\n|\n|\r)?)+/,'');
  const rows=[];let row=[],f='',q=false;
  for(let i=0;i<text.length;i++){
    const ch=text[i];
    if(q){if(ch==='"'){if(text[i+1]==='"'){f+='"';i++;}else q=false;}else f+=ch;}
    else if(ch==='"')q=true;
    else if(ch===','){row.push(f);f='';}
    else if(ch==='\n'||ch==='\r'){if(ch==='\r'&&text[i+1]==='\n')i++;row.push(f);f='';rows.push(row);row=[];}
    else f+=ch;
  }
  if(f!==''||row.length){row.push(f);rows.push(row);}
  return rows.filter(r=>!(r.length===1&&r[0].trim()===''));
}
function markFrom(s){
  s=String(s||'').trim().toLowerCase().replace('’',"'");
  if(!s)return '';
  if(s==='fits'||s==='fit')return 'fit';
  if(s==="doesn't fit"||s==='doesnt fit'||s==='no')return 'no';
  if(s==='unsure'||s==='un')return 'un';
  return '';
}
function loadCorrections(text){
  const rows=parseCSV(text);
  if(!rows.length)return 'The file is empty.';
  const head=rows[0].map(h=>h.trim().toLowerCase());
  const ix=n=>head.indexOf(n);
  const cS=ix('symbol'),cP=ix('paragraph'),cU=ix('un labels'),cM=ix('my labels'),cK=ix('my mark'),cI=ix('record id');
  if(cS<0||cM<0)return 'This does not look like a corrections file: it needs the columns Symbol, Paragraph, UN labels, My labels and My mark.';
  const split=s=>String(s||'').split(' | ').map(x=>x.trim()).filter(Boolean);
  const byId=new Map(R.map(r=>[String(r.id),r]));
  let applied=0,unDiff=0;const unmatched=[],unknown=new Set();
  rows.slice(1).forEach(row=>{
    const g=k=>k<0?'':String(row[k]==null?'':row[k]).trim();
    const sym=g(cS),para=g(cP),unL=split(g(cU)),myL=split(g(cM)),mk=markFrom(g(cK)),id=g(cI);
    let rec=id?byId.get(id)||null:null;
    if(!rec){
      let cands=R.filter(r=>r.symbol===sym&&(para?r._para===para:!r._para));
      if(cands.length>1)cands=cands.filter(r=>unT(r).join(' | ')===unL.join(' | '));
      if(cands.length===1)rec=cands[0];
    }
    if(!rec){unmatched.push(sym+(para?', para. '+para:''));return;}
    const un=unT(rec);
    if(cU>=0&&unL.join(' | ')!==un.join(' | '))unDiff++;
    const known=[];myL.forEach(x=>{if(ALLTHEMES.indexOf(x)<0)unknown.add(x);else if(known.indexOf(x)<0)known.push(x);});
    const rem=un.filter(x=>known.indexOf(x)<0),ad=known.filter(x=>un.indexOf(x)<0);
    if(rem.length||ad.length)CORR.set(rec._i,{rem,add:ad});else CORR.delete(rec._i);
    if(mk)MARK.set(rec._i,mk);else MARK.delete(rec._i);
    applied++;
  });
  let m=`Loaded ${pl(rows.length-1,'row')}: ${pl(applied,'record')} restored.`;
  if(unmatched.length)m+=` ${pl(unmatched.length,'row')} not found in this file (${unmatched.slice(0,5).join('; ')}${unmatched.length>5?' …':''}).`;
  if(unknown.size)m+=` ${pl(unknown.size,'label')} not in the data ignored (${[...unknown].slice(0,3).join('; ')}${unknown.size>3?' …':''}).`;
  if(unDiff)m+=` ${pl(unDiff,'row')} listed UN labels that differ from this file.`;
  return m;
}

/* ---- method & export ---- */
function renderMethod(){
  const fd=describeFilters();
  $('methodText').innerHTML=`<p>The total is the number of records in the file; the breakdown counts records per <em>type</em>, spelled as in the data. Documents are the distinct UN symbols, and years run from the lowest to the highest year of the document, not of the decision.</p>
  <p>Filters combine with AND. Mechanism, body and type are exact matches, years are inclusive, and the keyword is literal: every word must appear in the text or the symbol, so "torture" does not find "ill-treatment".</p>
  <p>Theme counts add one for each theme on each filtered record; the top ten are ranked by count, ties alphabetically, and the years are those of the records carrying the theme. A record can carry several themes, so percentages are of records, not of labels.</p>
  <p>The paragraph number is read from the start of the text ("71" or "144.43"); if there is none, none is shown. The recommending State is read only from UPR texts, from the parentheses at the end; a group with a comma or over 60 characters is not taken as a State.</p>
  <p>Your corrections are stored beside the UN's labels, never over them. The switch under the title decides which labels every count, chart, filter and record uses; the exports below name the labels they used.</p>
  <p>Everything is counted by a loop in your browser. Nothing is estimated, no model is called and nothing leaves the page except what you copy or download. The themes and SDGs are the UN's own labels, which tab 03 lets you test on a sample.</p>
  <p class="lbl">Filters now applied: ${esc(fd.join('; ')||'none')} · ${fmt(filtered.length)} rows · ${esc(labelNote())}</p>`;
  $('srcInfo').innerHTML=`Data: ${srcLink}, ${esc(U.title||'')}; ${fmt(N)} records; built ${esc(U.built||'date not stated')}. Licence: not stated in the data file; check the source page for the terms of reuse.`;
}
function buildCSV(){
  const fd=describeFilters(),lines=[
    '# Country: '+C,'# Source: '+(U.source||'')+' '+(U.source_url||''),'# Built: '+(U.built||''),'# Filters: '+(fd.join('; ')||'none'),'# Rows: '+filtered.length+' of '+N,
    '# '+labelNote(),
    '# Dates are the date of the UN document. UN themes and SDGs are the UN labels, unchanged; the column Themes follows the switch (UN labels or with your corrections).'];
  const head=['Date','Body','Mechanism','Type','Symbol','Paragraph','Recommending State','Section','Text','Themes','UN themes','Corrected by you','SDGs','SDG targets','Affected persons','Document URL'];
  lines.push(head.map(csvEsc).join(','));
  filtered.forEach(r=>lines.push([r.date,r.body,r.mechanism,r.type,r.symbol,r._para||'',r._isUpr?(r._states.join('; ')||'State not found'):'',r.section||'',r.text,effT(r).join(' | '),unT(r).join(' | '),CORR.has(r._i)?'yes':'no',(r.sdgs||[]).join(' | '),(r.sdg_targets||[]).join(' | '),(r.affected_persons||[]).join(' | '),r.doc_url].map(csvEsc).join(',')));
  return lines.join('\r\n');
}
function buildSummary(){
  const f=filtered,n=f.length,ys=f.map(r=>r.year).filter(Number.isFinite);
  const L=[`${C}: UN recommendations and observations (OHCHR UHRI, built ${U.built||'date not stated'}).`,
   `Filters: ${describeFilters().join('; ')||'none'}.`,
   labelNote(),
   `${fmt(n)} matching records of ${fmt(N)}; ${fmt(new Set(f.map(r=>r.symbol)).size)} documents; years ${ys.length?Math.min(...ys)+'–'+Math.max(...ys):'none'} (year of the document).`,
   'By type: '+(typeBreakdown(f).map(([t,c])=>`${fmt(c)} ${t}`).join(', ')||'none')+'.',
   'By mechanism: '+MECHS.map(m=>`${m} ${fmt(f.filter(r=>r.mechanism===m).length)}`).join(', ')+'.',
   'Ten most frequent themes (a record can carry several themes):'];
  themeStats(f).slice(0,10).forEach((x,i)=>L.push(`${i+1}. ${x.t}: ${fmt(x.c)} records (${(x.c/n*100).toFixed(1)}%), ${yrs(x.min,x.max)}`));
  L.push("Counted in the browser from the UHRI file; the UN's own labels were not changed.");
  return L.join('\n');
}
function download(name,content){
  const blob=new Blob(['\uFEFF'+content],{type:'text/csv;charset=utf-8'}),url=URL.createObjectURL(blob),a=document.createElement('a');
  a.href=url;a.download=name;document.body.appendChild(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(url),3000);
}
const slug=()=>String(C).toLowerCase().replace(/[^a-z0-9]+/g,'-');

/* ---- render all ---- */
function render(){
  filtered=sortRecords(applyFilters());
  renderCorrLine();renderRail();renderOverview();renderRecords();renderCheck();renderMethod();
}
function setTab(i,focus){
  active=i;
  [0,1,2,3].forEach(k=>{const t=$('tab'+k);t.setAttribute('aria-selected',k===i);t.tabIndex=k===i?0:-1;$('panel'+k).hidden=k!==i;});
  $('facets').hidden=i>1;
  if(focus)$('tab'+i).focus();
  if(i===0)drawCharts();
}

/* ---- events ---- */
[0,1,2,3].forEach(k=>$('tab'+k).addEventListener('click',()=>setTab(k)));
$('tabs').addEventListener('keydown',e=>{
  if(!['ArrowRight','ArrowLeft','Home','End'].includes(e.key))return;e.preventDefault();
  let i=active;if(e.key==='ArrowRight')i=(i+1)%4;else if(e.key==='ArrowLeft')i=(i+3)%4;else if(e.key==='Home')i=0;else i=3;setTab(i,true);
});
$('modeSw').addEventListener('click',()=>{S.useMine=!S.useMine;render();});
[0,1,2].forEach(k=>$('b'+k).addEventListener('click',()=>{
  const open=$('b'+k).getAttribute('aria-expanded')==='true';
  [0,1,2].forEach(j=>{const o=!open&&j===k;$('b'+j).setAttribute('aria-expanded',o);$('a'+j).hidden=!o;$('b'+j).querySelector('.ar').textContent=o?'–':'+';});
}));
let kwT=null;
function kwInput(src){return()=>{const v=src.value;$('kwRail').value=v;$('kwMain').value=v;clearTimeout(kwT);kwT=setTimeout(()=>{S.kw=v;onFilter();},300);}}
$('kwRail').addEventListener('input',kwInput($('kwRail')));
$('kwMain').addEventListener('input',kwInput($('kwMain')));
$('selMech').addEventListener('change',e=>{S.mech=e.target.value;buildSelects();onFilter();});
$('selBody').addEventListener('change',e=>{S.body=e.target.value;buildSelects();onFilter();});
$('selType').addEventListener('change',e=>{S.type=e.target.value;onFilter();});
$('selState').addEventListener('change',e=>{S.state=e.target.value;onFilter();});
function yearChange(){
  let a=Number($('selFrom').value),b=Number($('selTo').value);
  if(a>b){const t=a;a=b;b=t;}
  S.yFrom=a;S.yTo=b;$('selFrom').value=String(a);$('selTo').value=String(b);onFilter();
}
$('selFrom').addEventListener('change',yearChange);
$('selTo').addEventListener('change',yearChange);
$('selSdg').addEventListener('change',e=>{S.sdg=e.target.value===''?null:Number(e.target.value);onFilter();});
$('clearAll').addEventListener('click',()=>{
  Object.assign(S,{kw:'',mech:'',body:'',type:'',state:'',yFrom:YMIN,yTo:YMAX,sdg:null,themes:[]});
  buildSelects();onFilter();
});
$('chips').addEventListener('click',e=>{
  const b=e.target.closest('.fchip');if(!b)return;
  view.chips[Number(b.dataset.k)].f();buildSelects();onFilter();
});
$('themeTable').addEventListener('click',e=>{const b=e.target.closest('[data-theme]');if(b)addTheme(b.dataset.theme);});
$('mechTiles').addEventListener('click',e=>{if(e.target.id==='stBtn'){S.showStates=!S.showStates;renderOverview();}});
$('dateSort').addEventListener('click',()=>{S.dir=-S.dir;S.shown=50;filtered=sortRecords(filtered);renderRecords();});
$('moreBtn').addEventListener('click',()=>{S.shown+=50;renderRecords();});
$('recBody').addEventListener('click',async e=>{
  const btn=e.target.closest('[data-act="cite"]');
  if(btn){const r=R[Number(btn.dataset.i)];const ok=await copyText(cite(r));flash(btn.parentElement.querySelector('.copied'),ok);return;}
  if(e.target.closest('a'))return;
  const tr=e.target.closest('tr.row');if(tr)toggleRow(tr);
});
$('recBody').addEventListener('keydown',e=>{
  const tr=e.target.closest&&e.target.closest('tr.row');
  if(tr&&e.target===tr&&(e.key==='Enter'||e.key===' ')){e.preventDefault();toggleRow(tr);}
});
function sampleClick(e){
  const b=e.target.closest('[data-act]');if(!b)return;const a=b.dataset.act;
  if(a==='sdraw'||a==='sagain')draw(Math.floor(Math.random()*999999)+1);
  else if(a==='sseed'){const v=Math.floor(Number($('seedIn').value));draw(Number.isFinite(v)&&v>=0?v:1);}
  else if(a==='sopen'){const k=Number(b.dataset.k);sample.open=sample.open===k?null:k;renderCards();const nb=document.querySelector(`[data-act="sopen"][data-k="${k}"]`);if(nb)nb.focus();}
  else if(a==='verdict'){
    const k=Number(b.dataset.k),id=sample.ids[k],v=b.dataset.v;
    if(MARK.get(id)===v)MARK.delete(id);else MARK.set(id,v);
    renderCards();renderCorrPanel();
    const nb=document.querySelector(`[data-act="verdict"][data-k="${k}"][data-v="${v}"]`);if(nb)nb.focus();
  }
  else if(a==='lremove'||a==='lrestore'||a==='ladd'||a==='lundo'){
    const i=Number(b.dataset.i),r=R[i],lab=b.dataset.l;let msg='';
    if(a==='lremove'){
      const mine=CORR.get(i)&&CORR.get(i).add.indexOf(lab)>=0;
      editLabel(i,'rm',lab);
      msg=mine?`Removed your label "${lab}" from ${cite(r)}.`:`Removed "${lab}" from ${cite(r)} in your view; the UN label is kept, struck through.`;
    }else if(a==='lrestore'){editLabel(i,'add',lab);msg=`Restored the UN label "${lab}" on ${cite(r)}.`;}
    else if(a==='ladd'){
      const v=$('addSel')?$('addSel').value:'';
      if(!v){$('corrMsg').textContent='Choose a label from the list first.';return;}
      editLabel(i,'add',v);msg=`Added "${v}" to ${cite(r)}. Counts, charts and filters now use your correction.`;
    }else{CORR.delete(i);msg=`Undid the label corrections on ${cite(r)}.`;}
    afterCorrection(msg,a!=='lundo');
    const t=$('addSel')||document.querySelector('[data-act="sopen"][aria-expanded="true"]');if(t)t.focus();
  }
}
$('sampleCtl').addEventListener('click',sampleClick);
$('sampleCards').addEventListener('click',sampleClick);
$('corrToggle').addEventListener('click',()=>{S.corrOpen=!S.corrOpen;renderCorrPanel();});
$('corrList').addEventListener('click',e=>{
  const b=e.target.closest('[data-act="cundo"]');if(!b)return;
  const i=Number(b.dataset.i),r=R[i];CORR.delete(i);MARK.delete(i);
  afterCorrection(`Undid the correction and mark on ${cite(r)}.`,false);
  if(S.corrOpen&&!$('corrToggle').disabled)$('corrToggle').focus();else $('corrLoad').focus();
});
$('corrDl').addEventListener('click',()=>{
  if(!corrRecords().length){$('corrMsg').textContent='Nothing to download yet.';return;}
  download('uhri-'+slug()+'-my-corrections.csv',buildCorrCSV());
  $('corrMsg').textContent=`Downloaded ${pl(corrRecords().length,'row')}. Load this file later to restore them.`;
});
$('corrLoad').addEventListener('click',()=>$('corrFile').click());
$('corrFile').addEventListener('change',e=>{
  const f=e.target.files&&e.target.files[0];if(!f)return;
  const fr=new FileReader();
  fr.onload=()=>{const msg=loadCorrections(String(fr.result||''));S.useMine=true;afterCorrection(msg,true);$('corrFile').value='';};
  fr.onerror=()=>{$('corrMsg').textContent='The file could not be read.';$('corrFile').value='';};
  fr.readAsText(f);
});
$('corrUndoAll').addEventListener('click',()=>{
  const b=$('corrUndoAll');
  if(!undoAllT){
    b.textContent=`Click again to undo all ${fmt(corrRecords().length)}`;
    undoAllT=setTimeout(()=>{undoAllT=null;b.textContent='Undo all corrections';},4000);
    return;
  }
  clearTimeout(undoAllT);undoAllT=null;
  CORR.clear();MARK.clear();
  afterCorrection('Undid all corrections and marks. The UN labels were never changed.',false);
});
$('csvBtn').addEventListener('click',()=>{
  download('uhri-'+slug()+'-'+(U.built||'data')+'.csv',buildCSV());
  $('exportMsg').textContent=`CSV prepared: ${fmt(filtered.length)} rows`;setTimeout(()=>{$('exportMsg').textContent=''},4000);
});
$('sumBtn').addEventListener('click',async()=>{flash($('exportMsg'),await copyText(buildSummary()));});

buildSelects();
render();
setTab(0);
})();
</script>
</body>
</html>
```