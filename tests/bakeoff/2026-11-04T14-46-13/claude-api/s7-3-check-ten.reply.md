I added correction of labels to the random-sample check on the Check tab. Open a card, press "Correct these labels", remove a UN label or add one from the labels in the data, and mark it wrong or arguable. The switch under the title applies your corrections to every number, chart and filter; the UN labels are never changed. Undo, CSV download and CSV load sit in "Your corrections" on the Check tab. I added a `record_id` column to the CSV so a reload finds the exact record. I haven't run this against your actual file.

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>UN human rights recommendations: UHRI dashboard</title>
<style>
:root{--paper:#f4f0e8;--ink:#1d1b18;--rule:#d9d2c3;--red:#9b2335;--mute:#5b564c;--serif:Georgia,"Times New Roman",serif;--mono:ui-monospace,Menlo,Consolas,monospace}
*{box-sizing:border-box}
[hidden]{display:none!important}
body{margin:0;background:var(--paper);color:var(--ink);font:16px/1.5 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif}
:focus-visible{outline:3px solid var(--red);outline-offset:2px}
a{color:var(--red)}
.wrap{max-width:1320px;margin:0 auto;padding:0 20px}
.mono{font:11.5px/1.4 var(--mono);letter-spacing:.08em;text-transform:uppercase}
.hint,.how,.srcnote{font:12px/1.5 var(--mono);color:var(--mute);letter-spacing:.02em}
.how{margin:8px 0 0}
.srcnote{margin:6px 0 0}
header{padding:22px 0 14px;border-bottom:1px solid var(--ink)}
h1{font:400 34px/1.15 var(--serif);margin:6px 0 8px}
.srcline{margin:8px 0 0;color:var(--mute);font-size:14px}
.corrline{display:flex;flex-wrap:wrap;gap:8px 16px;align-items:center;font:13px var(--mono);margin:4px 0 0}
.seg{display:inline-flex}
.segbtn{border:1px solid var(--ink);background:transparent;color:var(--ink);padding:5px 10px;font:11.5px var(--mono);letter-spacing:.08em;text-transform:uppercase;cursor:pointer}
.segbtn+.segbtn{border-left:0}
.segbtn[aria-pressed=true]{background:var(--red);border-color:var(--red);color:#fff}
.layout{display:grid;grid-template-columns:250px minmax(0,1fr);gap:32px;padding:18px 0 30px}
@media(max-width:860px){.layout{grid-template-columns:1fr}h1{font-size:26px}}
.rail{border-right:1px solid var(--rule);padding-right:20px}
@media(max-width:860px){.rail{border-right:0;padding-right:0;border-bottom:1px solid var(--rule);padding-bottom:14px}}
.railhead{display:flex;justify-content:space-between;align-items:center;min-height:28px}
.textbtn{background:none;border:0;padding:2px 0;color:var(--red);font:11.5px var(--mono);letter-spacing:.08em;text-transform:uppercase;cursor:pointer;text-decoration:underline}
.bigmatch{font:400 52px/1 var(--serif);margin-top:10px}
.matchlbl{font-size:15px}
.sharebar{height:4px;background:var(--rule);margin:8px 0}
.sharebar i{display:block;height:100%;background:var(--red);width:0}
#chips{margin:8px 0;display:flex;flex-wrap:wrap;gap:4px}
.chip{border:1px solid var(--red);background:transparent;color:var(--red);font:11.5px var(--mono);padding:2px 8px;cursor:pointer;text-align:left}
.chip:hover{background:var(--red);color:#fff}
.acc{border-top:1px solid var(--rule)}
.acchead{width:100%;display:flex;justify-content:space-between;background:none;border:0;padding:11px 0;cursor:pointer;color:var(--ink);text-align:left}
.acchead::after{content:"+";font:16px var(--mono)}
.acchead[aria-expanded=true]::after{content:"–"}
.acchead[aria-expanded=true] span{color:var(--red)}
.accbody{padding:0 0 14px}
.accbody label{display:block;margin:10px 0 3px;color:var(--mute)}
input[type=search],input[type=number],select,textarea{width:100%;font:15px system-ui,sans-serif;padding:7px;border:1px solid #8f8778;background:#fffdf8;color:var(--ink)}
.tabs{display:flex;flex-wrap:wrap;border-bottom:1px solid var(--rule);margin-bottom:18px}
.tab{background:none;border:0;border-bottom:3px solid transparent;padding:10px 16px 8px 0;margin-right:18px;font:12px var(--mono);letter-spacing:.08em;text-transform:uppercase;color:var(--mute);cursor:pointer}
.tab[aria-selected=true]{color:var(--red);border-bottom-color:var(--red)}
h2.q{font:400 24px/1.2 var(--serif);margin:0 0 14px}
h3.fig{font:400 20px/1.25 var(--serif);margin:26px 0 8px}
h3.fig .mono{color:var(--red);margin-right:8px}
.tiles{display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:0 24px;border-top:1px solid var(--rule)}
.tile{padding:12px 0;border-bottom:1px solid var(--rule)}
.tile .n{font:400 48px/1.05 var(--serif)}
.tile .sub{font-size:13px;color:var(--mute)}
.dot{display:inline-block;width:10px;height:10px;border-radius:50%;margin-right:6px}
.linkbtn{background:none;border:0;padding:0;color:var(--red);text-decoration:underline;font:12px var(--mono);cursor:pointer}
.chartbox{position:relative;height:340px;border-top:1px solid var(--rule);padding-top:8px}
.chartbox.short{height:290px}
table{width:100%;border-collapse:collapse;font-size:15px}
caption{text-align:left;font:12px var(--mono);color:var(--mute);padding:6px 0;letter-spacing:.02em}
th{font:11.5px var(--mono);letter-spacing:.08em;text-transform:uppercase;text-align:left;border-bottom:1px solid var(--ink);padding:6px 8px 6px 0;vertical-align:bottom}
td{border-bottom:1px solid var(--rule);padding:7px 8px 7px 0;vertical-align:top}
.num{text-align:right;font-variant-numeric:tabular-nums}
th.num{text-align:right}
.themebtn,.rowbtn{background:none;border:0;padding:0;font:inherit;color:var(--ink);cursor:pointer;text-align:left;text-decoration:underline dotted}
.rowbtn::before{content:"▸ ";color:var(--red)}
.rowbtn[aria-expanded=true]::before{content:"▾ "}
.sortbtn{background:none;border:0;padding:0;font:inherit;letter-spacing:inherit;text-transform:inherit;cursor:pointer;color:var(--ink)}
tr.open td{border-bottom:0;background:#efe9dc}
td.sym{overflow-wrap:anywhere}
.detail{display:grid;grid-template-columns:100px 1fr;gap:16px;padding:12px 4px 16px}
tr.det td{background:#efe9dc}
.pnum{font:400 46px/1 var(--serif);color:var(--red)}
.fulltext{white-space:pre-wrap;margin:0 0 10px;font-size:16px}
mark{background:#f3d9a8;color:inherit;padding:0 1px}
.labels{margin:0 0 10px;font-size:14px}
.labels dt{font:11px var(--mono);letter-spacing:.08em;text-transform:uppercase;color:var(--mute);margin-top:6px}
.labels dd{margin:0}
.tag{display:inline-block;border:1px solid var(--rule);padding:0 7px;margin:2px 4px 2px 0;font-size:13px;background:#fbf8f1;color:var(--ink)}
.tag.mine{border-color:var(--red);color:var(--red);background:#f7e6e9;font-style:italic}
.tag.gone{color:#6b655b;border-style:dashed}
button.tag{font:inherit;font-size:13px;cursor:pointer}
button.tag .act{font:10.5px var(--mono);letter-spacing:.06em;text-transform:uppercase;color:var(--red);margin-left:4px;font-style:normal}
.corrtag{display:inline-block;font:10.5px var(--mono);letter-spacing:.06em;text-transform:uppercase;color:#fff;background:var(--red);padding:1px 6px;margin-left:4px;vertical-align:middle;border:1px solid var(--red)}
.corrtag.off{background:transparent;color:var(--red);border-style:dashed}
.sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}
.btn{border:1px solid var(--ink);background:transparent;color:var(--ink);padding:8px 12px;font:11.5px var(--mono);letter-spacing:.08em;text-transform:uppercase;cursor:pointer}
.btn:hover{background:var(--ink);color:var(--paper)}
.btn:disabled{opacity:.45;cursor:not-allowed;background:transparent;color:var(--ink)}
.btn.primary{background:var(--red);border-color:var(--red);color:#fff}
.btn[aria-pressed=true]{background:var(--red);border-color:var(--red);color:#fff}
.copied{margin-left:10px;font:12px var(--mono);color:var(--red)}
.panel{border-top:1px solid var(--ink);padding:10px 0 20px;margin-bottom:12px}
.panel h3{margin:0 0 4px}
ol.checks,ol.cards{list-style:none;padding:0;margin:10px 0 0}
.chk{border-bottom:1px solid var(--rule);padding:9px 0}
.chkh{display:flex;gap:12px;align-items:baseline;flex-wrap:wrap}
.chkh span{font:11.5px var(--mono);letter-spacing:.06em;text-transform:uppercase;white-space:nowrap}
.ok{color:#17653a}.bad{color:var(--red);font-weight:700}.warnm{color:#8a5a00}.inf{color:var(--mute)}
.vals{font-size:14px;color:var(--mute);margin-top:2px}
details{margin-top:4px;font-size:14px}
summary{cursor:pointer;font:11.5px var(--mono);color:var(--red)}
details ul{margin:6px 0;padding-left:18px}
.cardline{display:flex;gap:12px;align-items:baseline;border-bottom:1px solid var(--rule);padding:7px 0;flex-wrap:wrap}
.cardtoggle{flex:1;min-width:200px;background:none;border:0;text-align:left;font:inherit;cursor:pointer;padding:0;color:var(--ink)}
.cardtoggle::before{content:"▸ ";color:var(--red)}
.cardtoggle[aria-expanded=true]::before{content:"▾ "}
.vtag{font:11.5px var(--mono);color:var(--red);min-width:80px;text-align:right}
.cardbody{padding:10px 0 16px 18px;border-bottom:1px solid var(--rule);background:#efe9dc}
.verds{display:flex;gap:8px;flex-wrap:wrap;margin-top:10px}
.editor{border-top:1px solid var(--rule);margin-top:12px;padding-top:8px}
.tally{font:14px var(--mono);margin:12px 0 0}
.seedrow{display:flex;gap:10px;align-items:center;flex-wrap:wrap;margin-top:8px}
.seedrow input[type=number]{width:110px}
.corrlist{list-style:none;padding:0;margin:8px 0}
.corrlist li{border-bottom:1px solid var(--rule);padding:7px 0}
#corrDet{margin-top:14px;border-top:1px solid var(--rule);padding-top:8px}
pre.summary{white-space:pre-wrap;background:#fbf8f1;border:1px solid var(--rule);padding:10px;font:13px/1.5 var(--mono);margin:10px 0}
.method p{max-width:75ch}
.statebox{border:1px solid var(--rule);padding:10px 14px;margin-top:12px;background:#fbf8f1}
.statebox ol{margin:6px 0;padding-left:22px}
footer{border-top:1px solid var(--rule);padding:12px 0 24px;font:11.5px var(--mono);color:var(--mute);letter-spacing:.04em}
.empty{padding:24px 0;color:var(--mute);font-style:italic}
</style>
</head>
<body>
<div class="wrap">
<header>
  <div class="mono" id="hLabel"></div>
  <h1 id="hTitle"></h1>
  <div class="corrline">
    <span id="corrText" aria-live="polite"></span>
    <span class="seg" role="group" aria-label="Which labels every number, chart and filter uses">
      <button class="segbtn" id="viewUN" aria-pressed="true">UN labels</button><button class="segbtn" id="viewMine" aria-pressed="false">With my corrections</button>
    </span>
  </div>
  <p class="srcline" id="hSrc"></p>
</header>

<div class="layout">
  <aside class="rail" aria-label="Filters">
    <div class="railhead"><span class="mono">Filters</span><button class="textbtn" id="clearAll" hidden>Clear all</button></div>
    <div aria-live="polite"><div class="bigmatch" id="matchN">0</div><div class="matchlbl">matching records</div><div class="hint" id="ofN"></div></div>
    <div class="sharebar" aria-hidden="true"><i id="shareFill"></i></div>
    <div id="chips"></div>
    <div id="accs">
      <div class="acc"><h3 style="margin:0"><button class="acchead mono" aria-expanded="false" aria-controls="a0" data-a="0"><span>01 Keyword</span></button></h3>
        <div class="accbody" id="a0" hidden>
          <input type="search" id="kwRail" aria-label="Keyword" placeholder="e.g. torture">
          <p class="hint">literal match, not synonyms</p>
        </div></div>
      <div class="acc"><h3 style="margin:0"><button class="acchead mono" aria-expanded="false" aria-controls="a1" data-a="1"><span>02 Mechanism, body, type</span></button></h3>
        <div class="accbody" id="a1" hidden>
          <label class="mono" for="selMech">Mechanism</label><select id="selMech"></select>
          <label class="mono" for="selBody">Body or mandate</label><select id="selBody"></select>
          <label class="mono" for="selType">Type</label><select id="selType"></select>
          <div id="stateWrap"><label class="mono" for="selState">Recommending State (UPR)</label><select id="selState"></select></div>
        </div></div>
      <div class="acc"><h3 style="margin:0"><button class="acchead mono" aria-expanded="false" aria-controls="a2" data-a="2"><span>03 Years and SDG</span></button></h3>
        <div class="accbody" id="a2" hidden>
          <label class="mono" for="selYf">Year from</label><select id="selYf"></select>
          <label class="mono" for="selYt">Year to</label><select id="selYt"></select>
          <label class="mono" for="selSdg">SDG</label><select id="selSdg"></select>
        </div></div>
    </div>
  </aside>

  <main>
    <div class="tabs" role="tablist" aria-label="Dashboard sections" id="tabs">
      <button class="tab" role="tab" id="t0" aria-controls="p0" aria-selected="true">01 Overview</button>
      <button class="tab" role="tab" id="t1" aria-controls="p1" aria-selected="false" tabindex="-1">02 Records</button>
      <button class="tab" role="tab" id="t2" aria-controls="p2" aria-selected="false" tabindex="-1">03 Check</button>
      <button class="tab" role="tab" id="t3" aria-controls="p3" aria-selected="false" tabindex="-1">04 Method &amp; export</button>
    </div>

    <section role="tabpanel" id="p0" aria-labelledby="t0">
      <h2 class="q">What has the UN said, how much, and when?</h2>
      <div class="tiles" id="headTiles"></div>
      <p class="how" id="howHead"></p>
      <div class="tiles" id="mechTiles" style="margin-top:14px"></div>
      <p class="how" id="howMech"></p>
      <div class="statebox" id="stateBox" hidden></div>

      <h3 class="fig"><span class="mono">FIG.01</span><span id="fig1title"></span></h3>
      <div class="chartbox" id="chart1box"><canvas id="chart1" role="img" aria-label="Horizontal bar chart of the ten most frequent themes; the same values are in the table below"></canvas></div>
      <div class="empty" id="fig1empty" hidden>No records match</div>
      <p class="hint">click a bar or a theme name = add it as a filter</p>
      <table>
        <caption>The ten themes in FIG.01 as a table</caption>
        <thead><tr><th scope="col">Theme</th><th scope="col" class="num">Records</th><th scope="col" class="num">% of filtered</th><th scope="col">Years (first–last)</th></tr></thead>
        <tbody id="themeBody"></tbody>
      </table>
      <p class="how">How this is computed: each theme counts once per record that carries it; a record can carry several themes, so the bars add up to more than the records. The labels are the UN's own, or with your corrections when that switch is on. A theme whose years stop early may be an old label: check a sample on tab 03.</p>
      <p class="srcnote" id="src1"></p>

      <h3 class="fig"><span class="mono">FIG.02</span><span id="fig2title"></span></h3>
      <div class="chartbox short" id="chart2box"><canvas id="chart2" role="img" aria-label="Stacked bar chart of records per year by mechanism"></canvas></div>
      <div class="empty" id="fig2empty" hidden>No records match</div>
      <p class="how">How this is computed: records of the filtered set counted per document year and mechanism; every year from the first to the last is shown, so empty years are gaps.</p>
      <p class="srcnote" id="src2"></p>
    </section>

    <section role="tabpanel" id="p1" aria-labelledby="t1" hidden>
      <h2 class="q">Which paragraph says it, and in which UN document?</h2>
      <input type="search" id="kwTop" aria-label="Search the records">
      <p class="hint">literal match on text and symbol, not synonyms</p>
      <table id="tbl">
        <caption id="cap"></caption>
        <thead><tr>
          <th scope="col"><button class="sortbtn" id="sortDate" title="Click to reverse the order"></button></th>
          <th scope="col">Body</th><th scope="col">Symbol</th><th scope="col" class="num">Para.</th><th scope="col">First line</th><th scope="col">Recommending State (UPR)</th>
        </tr></thead>
        <tbody id="tb"></tbody>
      </table>
      <p style="margin-top:12px"><button class="btn" id="more">Show 50 more</button></p>
      <p class="srcnote" id="src3"></p>
    </section>

    <section role="tabpanel" id="p2" aria-labelledby="t2" hidden>
      <h2 class="q">Can I trust these numbers?</h2>
      <div class="panel">
        <h3 class="mono">Check this dashboard</h3>
        <p class="hint">How the app checks itself: each line compares two values it computed in different ways.</p>
        <ol class="checks" id="checks"></ol>
      </div>
      <div class="panel">
        <h3 class="mono">Random-sample label check</h3>
        <p class="how" style="margin:2px 0 8px">This is your judgement of the UN's labels; nothing is sent anywhere. Corrections stay in this page until you download them.</p>
        <div class="seedrow">
          <button class="btn primary" id="drawFirst">Check 10 at random</button>
          <button class="btn" id="drawAgain" hidden>Draw again</button>
          <label class="mono" for="seed">Seed</label><input type="number" id="seed" value="1" step="1">
          <button class="btn" id="drawSeed" hidden>Draw with this seed</button>
        </div>
        <p class="how" id="sampleInfo"></p>
        <p class="tally" id="tally" aria-live="polite"></p>
        <details id="corrDet">
          <summary id="corrSum"></summary>
          <div id="corrList"></div>
          <div class="seedrow">
            <button class="btn" id="undoAll" hidden>Undo all corrections</button>
            <button class="btn" id="dlCorr">Download my corrections (CSV)</button>
            <button class="btn" id="loadBtn">Load corrections from CSV</button>
            <input type="file" id="corrFile" accept=".csv,text/csv,text/plain" hidden>
          </div>
          <p class="hint" style="margin-bottom:2px">Columns: symbol, paragraph, un_labels, my_labels, my_mark, record_id. Loading merges: a row replaces your earlier correction of the same record.</p>
          <label class="mono" for="corrPaste">Or paste the CSV text here</label>
          <textarea id="corrPaste" rows="3"></textarea>
          <div class="seedrow"><button class="btn" id="loadPaste">Load pasted text</button></div>
          <p class="how" id="corrMsg" role="status"></p>
        </details>
        <ol class="cards" id="cards"></ol>
      </div>
    </section>

    <section role="tabpanel" id="p3" aria-labelledby="t3" hidden class="method">
      <h2 class="q">How was this made, and how do I take it with me?</h2>
      <div id="methodText"></div>
      <p><button class="btn primary" id="dlCsv">Download CSV of the current filter</button> <button class="btn" id="cpSummary">Copy summary</button> <span class="copied" id="exportMsg" role="status"></span></p>
      <pre class="summary" id="summaryPre" aria-label="Summary text"></pre>
      <p class="hint" id="dataInfo"></p>
    </section>
  </main>
</div>
<footer id="foot"></footer>
</div>

<script>
(function(){
'use strict';
const D=(window.WORKSHOP_DATA&&window.WORKSHOP_DATA.uhri)||{};
const RAW=Array.isArray(D.records)?D.records:[];
const country=D.country||'this country';
const SDGN=D.sdg_names||{};
const UPR='Universal Periodic Review';
const STATE_RUN=/((?:\s*\((?:[^()]|\([^()]*\))*\))+)\s*[;.]?\s*$/;
const GROUP=/\((?:[^()]|\([^()]*\))*\)/g;
const PARA=/^(\d{1,3}(?:\.\d{1,3})?)\.?\s/;
const MECHCOL={'Universal Periodic Review':'#c2410c','Treaty bodies':'#0f766e','Special Procedures':'#7c3aed'};
const $=s=>document.querySelector(s);
const esc=s=>String(s==null?'':s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const fmt=n=>Number(n).toLocaleString('en-GB');
const pct=(a,b)=>b?(100*a/b).toFixed(1)+'%':'0.0%';
const arr=x=>Array.isArray(x)?x:[];
const uniq=a=>[...new Set(a)];
const safeUrl=u=>/^https?:\/\//i.test(u||'')?u:'';
const reEsc=s=>s.replace(/[.*+?^${}()|[\]\\]/g,'\\$&');
function countBy(list,fn){const m=new Map();list.forEach(x=>{const k=fn(x);m.set(k,(m.get(k)||0)+1);});return m;}
const mechColor=m=>MECHCOL[m]||'#6b655b';

/* ---------- prepare records ---------- */
function extractStates(text){
  const m=STATE_RUN.exec(text);
  if(!m) return {states:[],tail:''};
  const groups=m[1].match(GROUP)||[];
  const out=[];
  groups.forEach(g=>{const s=g.slice(1,-1).trim(); if(s&&s.indexOf(',')<0&&s.length<=60&&out.indexOf(s)<0) out.push(s);});
  return {states:out,tail:m[1].trim()};
}
function firstLine(t){
  t=t.replace(/\s+/g,' ').trim();
  if(t.length<=120) return t;
  let c=t.slice(0,120); const sp=c.lastIndexOf(' ');
  if(sp>40) c=c.slice(0,sp);
  return c.replace(/[\s,;:.]+$/,'')+'…';
}
const keySeen=new Set();
const recs=RAW.map((r,i)=>{
  const text=String(r.text==null?'':r.text);
  const pm=PARA.exec(text);
  const para=pm?pm[1]:null;
  let pkey=Infinity;
  if(para){const p=para.split('.'); pkey=Number(p[0])*10000+(p[1]?Number(p[1]):0);}
  const mech=String(r.mechanism||'(no mechanism)');
  let states=null,tail='';
  if(mech===UPR){const e=extractStates(text.trim()); states=e.states; tail=e.tail;}
  const symbol=String(r.symbol||'');
  let key=(r.id!=null&&r.id!=='')?String(r.id):'row'+i;
  if(keySeen.has(key)) key=key+'#'+i; keySeen.add(key);
  const themesUN=uniq(arr(r.themes).map(String));
  return {i,key,id:r.id,text,symbol,url:String(r.doc_url||''),date:String(r.date||''),year:Number(r.year),
    body:String(r.body||'(no body)'),mech,type:String(r.type||'(no type)'),section:String(r.section||''),
    themesUN,themes:themesUN.slice(),sdgs:arr(r.sdgs).map(Number),targets:arr(r.sdg_targets).map(String),persons:arr(r.affected_persons).map(String),
    para,pkey,states,tail,hay:(text+' '+symbol).toLowerCase(),first:firstLine(text)};
});
const N=recs.length;
const byKey=new Map(recs.map(x=>[x.key,x]));
const bySP=(function(){const m=new Map();recs.forEach(x=>{const k=x.symbol.toLowerCase()+'\u0001'+(x.para||'');if(!m.has(k))m.set(k,[]);m.get(k).push(x);});return m;})();
const themeUNCount=(function(){const m=new Map();recs.forEach(x=>x.themesUN.forEach(t=>m.set(t,(m.get(t)||0)+1)));return m;})();
const ALLTHEMES=[...themeUNCount.entries()].sort((a,b)=>a[0].localeCompare(b[0]));
const yearsAll=[...new Set(recs.map(x=>x.year).filter(Number.isFinite))].sort((a,b)=>a-b);
const minY=yearsAll.length?yearsAll[0]:0, maxY=yearsAll.length?yearsAll[yearsAll.length-1]:0;
const nDocs=new Set(recs.map(x=>x.symbol)).size;
const mechList=[...new Set(recs.map(x=>x.mech))].sort((a,b)=>{const o=[UPR,'Treaty bodies','Special Procedures'];const ia=o.indexOf(a),ib=o.indexOf(b);return (ia<0?9:ia)-(ib<0?9:ib)||a.localeCompare(b);});
const typeCountsAll=[...countBy(recs,x=>x.type).entries()].sort((a,b)=>b[1]-a[1]);
const stateAll=(function(){const m=new Map();recs.forEach(x=>(x.states||[]).forEach(s=>m.set(s,(m.get(s)||0)+1)));return [...m.entries()].sort((a,b)=>b[1]-a[1]||a[0].localeCompare(b[0]));})();
const sdgAll=(function(){const m=new Map();recs.forEach(x=>new Set(x.sdgs).forEach(g=>m.set(g,(m.get(g)||0)+1)));return [...m.entries()].filter(e=>Number.isFinite(e[0])).sort((a,b)=>a[0]-b[0]);})();

/* ---------- state ---------- */
const S={q:'',mech:'',body:'',type:'',st:'',yf:minY,yt:maxY,sdg:'',themes:[],tab:0,acc:-1,dateDir:-1,shown:50,expanded:new Set(),showStates:false,sample:null,verdict:{},card:-1,view:'un',edit:-1,pend:'wrong'};
let F=[],V={top:[]},W=[],chart1=null,chart2=null,fileChecksCache=null;

/* ---------- corrections (the UN's labels in themesUN are never touched) ---------- */
const corr=new Map(); // key -> {remove:[], add:[], mark:'wrong'|'arguable'}
const labelCount=()=>{let n=0;corr.forEach(c=>{n+=c.remove.length+c.add.length;});return n;};
function applied(x,c){
  const rm=new Set(c.remove); const out=x.themesUN.filter(t=>!rm.has(t));
  c.add.forEach(t=>{if(out.indexOf(t)<0)out.push(t);}); return out;
}
function effThemes(x){const c=corr.get(x.key); return (S.view==='mine'&&c)?applied(x,c):x.themesUN;}
function refreshThemes(){recs.forEach(x=>{x.themes=effThemes(x);});}
const usingMine=()=>S.view==='mine'&&corr.size>0;
const viewNote=()=>usingMine()?'labels: the UN\'s own, with '+fmt(labelCount())+' correction'+(labelCount()===1?'':'s')+' by you':'labels: the UN\'s own';
function keepFocus(fn){
  const a=document.activeElement; const k=a&&a.getAttribute?a.getAttribute('data-fk'):null;
  fn();
  if(k){const e=document.querySelector('[data-fk="'+k.replace(/"/g,'\\"')+'"]'); if(e)e.focus();}
}
function corrChanged(){
  keepFocus(()=>{
    fileChecksCache=null; refreshThemes(); renderView(); render();
  });
}
function mutate(x,fn){
  let c=corr.get(x.key); if(!c) c={remove:[],add:[],mark:S.pend};
  fn(c);
  if(!c.remove.length&&!c.add.length) corr.delete(x.key); else corr.set(x.key,c);
  S.view='mine'; corrChanged();
}
function renderView(){
  const n=labelCount(),k=corr.size;
  $('#corrText').innerHTML=fmt(n)+' label'+(n===1?'':'s')+' corrected by you; the UN\'s own labels are kept'+(k?' <span class="hint">(in '+fmt(k)+' record'+(k===1?'':'s')+(S.view==='un'?'; not applied now':'')+')</span>':'');
  $('#viewUN').setAttribute('aria-pressed',S.view==='un');
  $('#viewMine').setAttribute('aria-pressed',S.view==='mine');
}
function corrTag(x){
  if(!corr.has(x.key)) return '';
  return '<span class="corrtag'+(S.view==='mine'?'':' off')+'">corrected by you'+(S.view==='mine'?'':' · not applied')+'</span>';
}
function plainTag(t){return '<span class="tag">'+esc(t)+'</span>';}
function themesHtml(x){
  const c=corr.get(x.key);
  if(!c||S.view!=='mine'){
    const base=x.themesUN.length?x.themesUN.map(plainTag).join(''):'<span class="hint">not labelled</span>';
    return base+(c?corrTag(x):'');
  }
  const rm=new Set(c.remove);
  const parts=x.themesUN.map(t=>rm.has(t)?'<span class="tag gone"><s>'+esc(t)+'</s><span class="sr"> (the UN\'s label, removed by you)</span></span>':plainTag(t))
    .concat(c.add.map(t=>'<span class="tag mine">+ '+esc(t)+'<span class="sr"> (added by you)</span></span>'));
  if(!parts.length) parts.push('<span class="hint">not labelled</span>');
  return parts.join('')+'<span class="corrtag">corrected by you · marked '+esc(c.mark)+'</span>';
}

/* ---------- filters ---------- */
function words(){return S.q.trim().toLowerCase().split(/\s+/).filter(Boolean);}
function applyFilters(){
  const w=words(); const full=(S.yf===minY&&S.yt===maxY); const g=S.sdg===''?null:Number(S.sdg);
  return recs.filter(x=>
    (!S.mech||x.mech===S.mech)&&(!S.body||x.body===S.body)&&(!S.type||x.type===S.type)&&
    (!S.st||(x.states&&x.states.indexOf(S.st)>=0))&&
    (full||(Number.isFinite(x.year)&&x.year>=S.yf&&x.year<=S.yt))&&
    (g===null||x.sdgs.indexOf(g)>=0)&&
    S.themes.every(t=>x.themes.indexOf(t)>=0)&&
    w.every(t=>x.hay.indexOf(t)>=0));
}
function activeFilters(){
  const a=[];
  if(S.q.trim()) a.push({label:'Keyword: “'+S.q.trim()+'”',rm(){S.q='';$('#kwRail').value='';$('#kwTop').value='';}});
  if(S.mech) a.push({label:'Mechanism: '+S.mech,rm(){S.mech='';S.body='';}});
  if(S.body) a.push({label:'Body: '+S.body,rm(){S.body='';}});
  if(S.type) a.push({label:'Type: '+S.type,rm(){S.type='';}});
  if(S.st) a.push({label:'State: '+S.st,rm(){S.st='';}});
  if(S.yf!==minY||S.yt!==maxY) a.push({label:'Years: '+S.yf+'–'+S.yt,rm(){S.yf=minY;S.yt=maxY;}});
  if(S.sdg!=='') a.push({label:'SDG '+S.sdg+(SDGN[S.sdg]?' · '+SDGN[S.sdg]:''),rm(){S.sdg='';}});
  S.themes.forEach(t=>a.push({label:'Theme: '+t,rm(){S.themes=S.themes.filter(x=>x!==t);}}));
  return a;
}
const describeFilters=()=>activeFilters().map(f=>f.label);
function clearAll(){S.q='';S.mech='';S.body='';S.type='';S.st='';S.yf=minY;S.yt=maxY;S.sdg='';S.themes=[];$('#kwRail').value='';$('#kwTop').value='';}
function changed(){S.shown=50;render();}

/* ---------- derived ---------- */
function topThemes(list){
  const m=new Map();
  list.forEach(x=>{new Set(x.themes).forEach(t=>{
    let e=m.get(t); if(!e){e={name:t,n:0,y0:Infinity,y1:-Infinity};m.set(t,e);}
    e.n++; if(Number.isFinite(x.year)){e.y0=Math.min(e.y0,x.year);e.y1=Math.max(e.y1,x.year);}
  });});
  return [...m.values()].sort((a,b)=>b.n-a.n||a.name.localeCompare(b.name)).slice(0,10);
}
const yrange=t=>t.y0===Infinity?'—':(t.y0===t.y1?String(t.y0):t.y0+'–'+t.y1);
function stateCounts(list){
  const m=new Map();
  list.forEach(x=>{if(x.mech===UPR)(x.states||[]).forEach(s=>m.set(s,(m.get(s)||0)+1));});
  return [...m.entries()].sort((a,b)=>b[1]-a[1]||a[0].localeCompare(b[0]));
}
function sortedRows(list){
  return list.slice().sort((a,b)=>{
    if(a.date!==b.date) return (a.date<b.date?-1:1)*S.dateDir;
    const c=a.body.localeCompare(b.body); if(c) return c;
    if(a.pkey!==b.pkey) return a.pkey<b.pkey?-1:1;
    return a.i-b.i;
  });
}
const cite=x=>x.para?x.symbol+', para. '+x.para:x.symbol;
function hl(str){
  if(!W.length) return esc(str);
  const ws=W.slice().sort((a,b)=>b.length-a.length).map(reEsc);
  const re=new RegExp(ws.join('|'),'gi'); let out='',last=0,m;
  while((m=re.exec(str))){ if(m[0]===''){re.lastIndex++;continue;} out+=esc(str.slice(last,m.index))+'<mark>'+esc(m[0])+'</mark>'; last=m.index+m[0].length; }
  return out+esc(str.slice(last));
}
function copyText(t){
  return new Promise(res=>{
    const fb=()=>{try{const ta=document.createElement('textarea');ta.value=t;ta.style.position='fixed';ta.style.opacity='0';document.body.appendChild(ta);ta.select();const ok=document.execCommand('copy');document.body.removeChild(ta);res(ok);}catch(e){res(false);}};
    if(navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText(t).then(()=>res(true),fb);}else fb();
  });
}
function flash(el,msg){el.textContent=msg;setTimeout(()=>{if(el.textContent===msg)el.textContent='';},2000);}
function saveText(name,text,type){
  const blob=new Blob(['\ufeff'+text],{type:type||'text/csv;charset=utf-8'});
  const u=URL.createObjectURL(blob); const a=document.createElement('a');
  a.href=u; a.download=name; document.body.appendChild(a); a.click(); document.body.removeChild(a); setTimeout(()=>URL.revokeObjectURL(u),4000);
}
const slug=()=>String(country).toLowerCase().replace(/[^a-z0-9]+/g,'-');

/* ---------- header, footer, static selects ---------- */
function initStatic(){
  $('#hLabel').textContent='UHRI · '+country;
  $('#hTitle').textContent='UN human rights recommendations and observations: '+country;
  const src=D.source?(safeUrl(D.source_url)?'<a href="'+esc(D.source_url)+'" target="_blank" rel="noopener">'+esc(D.source)+'</a>':esc(D.source)):'source not stated';
  $('#hSrc').innerHTML='Source: '+src+' · '+fmt(N)+' records · '+fmt(nDocs)+' documents · '+(yearsAll.length?minY+'–'+maxY:'no years')+(D.built?' · built '+esc(D.built):'')+' · <span class="hint">dated by document</span>';
  $('#foot').innerHTML='Built on OHCHR UHRI data · '+fmt(N)+' records · '+(safeUrl(D.source_url)?'<a href="'+esc(D.source_url)+'" target="_blank" rel="noopener">source</a>':'source link not in the file');
  $('#kwTop').placeholder='Search '+fmt(N)+' records, e.g. torture';
  const opt=(v,l)=>'<option value="'+esc(v)+'">'+esc(l)+'</option>';
  $('#selMech').innerHTML=opt('','All mechanisms')+mechList.map(m=>opt(m,m+' ('+fmt(recs.filter(x=>x.mech===m).length)+')')).join('');
  $('#selType').innerHTML=opt('','All types')+typeCountsAll.map(e=>opt(e[0],e[0]+' ('+fmt(e[1])+')')).join('');
  $('#selState').innerHTML=opt('','All States')+stateAll.map(e=>opt(e[0],e[0]+' ('+fmt(e[1])+')')).join('');
  $('#stateWrap').hidden=!stateAll.length;
  const yo=yearsAll.map(y=>opt(y,y)).join('');
  $('#selYf').innerHTML=yo; $('#selYt').innerHTML=yo;
  $('#selSdg').innerHTML=opt('','All goals')+sdgAll.map(e=>opt(e[0],'SDG '+e[0]+(SDGN[e[0]]?' · '+SDGN[e[0]]:'')+' ('+fmt(e[1])+')')).join('');
}

/* ---------- rail ---------- */
function renderRail(){
  $('#matchN').textContent=fmt(F.length);
  $('#ofN').textContent='of '+fmt(N)+' in the file';
  $('#shareFill').style.width=(N?100*F.length/N:0)+'%';
  const chips=activeFilters(); V.chips=chips;
  $('#chips').innerHTML=chips.map((c,k)=>'<button class="chip" data-c="'+k+'" aria-label="Remove filter: '+esc(c.label)+'">'+esc(c.label)+' ✕</button>').join('');
  $('#clearAll').hidden=!chips.length;
  const bodies=[...countBy(recs.filter(x=>!S.mech||x.mech===S.mech),x=>x.body).entries()].sort((a,b)=>b[1]-a[1]||a[0].localeCompare(b[0]));
  $('#selBody').innerHTML='<option value="">All bodies</option>'+bodies.map(e=>'<option value="'+esc(e[0])+'">'+esc(e[0])+' ('+fmt(e[1])+')</option>').join('');
  $('#selMech').value=S.mech;$('#selBody').value=S.body;$('#selType').value=S.type;$('#selState').value=S.st;
  $('#selYf').value=String(S.yf);$('#selYt').value=String(S.yt);$('#selSdg').value=S.sdg;
  $('#accs').hidden=!(S.tab===0||S.tab===1);
  document.querySelectorAll('.acchead').forEach(b=>{const i=Number(b.dataset.a);b.setAttribute('aria-expanded',S.acc===i);$('#a'+i).hidden=S.acc!==i;});
}

/* ---------- overview ---------- */
function renderOverview(){
  const n=F.length;
  const types=[...countBy(F,x=>x.type).entries()].sort((a,b)=>b[1]-a[1]);
  const docs=new Set(F.map(x=>x.symbol)).size;
  const ys=F.map(x=>x.year).filter(Number.isFinite);
  let a=Infinity,b=-Infinity; ys.forEach(y=>{if(y<a)a=y;if(y>b)b=y;});
  $('#headTiles').innerHTML=
   '<div class="tile"><div class="mono">Records</div><div class="n">'+fmt(n)+'</div><div class="sub">'+(n?types.map(e=>fmt(e[1])+' '+esc(e[0])).join(' · '):'—')+'</div></div>'+
   '<div class="tile"><div class="mono">Documents</div><div class="n">'+fmt(docs)+'</div><div class="sub">distinct symbols</div></div>'+
   '<div class="tile"><div class="mono">Years</div><div class="n" style="font-size:40px">'+(ys.length?a+'–'+b:'—')+'</div><div class="sub">first and last year</div></div>';
  $('#howHead').textContent='How this is computed: records = every record in the current filter, split by its type as spelled in the data; documents = distinct symbols; years = lowest and highest year.';
  $('#mechTiles').innerHTML=mechList.map(m=>{
    const L=F.filter(x=>x.mech===m); const d=new Set(L.map(x=>x.symbol)).size;
    let last=-Infinity; L.forEach(x=>{if(Number.isFinite(x.year)&&x.year>last)last=x.year;});
    const extra=(m===UPR&&stateAll.length)?' <button class="linkbtn" id="seeStates" aria-expanded="'+S.showStates+'">see the States</button>':'';
    return '<div class="tile"><div class="mono"><span class="dot" style="background:'+mechColor(m)+'"></span>'+esc(m)+extra+'</div><div class="n" style="font-size:40px">'+fmt(L.length)+'</div><div class="sub">'+fmt(d)+' documents · latest '+(L.length&&last>-Infinity?last:'—')+' · '+pct(L.length,n)+' of filtered</div></div>';
  }).join('');
  $('#howMech').textContent='How this is computed: per mechanism, the records of the current filter, their distinct symbols, their latest year and their share of the filtered records.';
  const box=$('#stateBox'); box.hidden=!S.showStates;
  if(S.showStates){
    const sc=stateCounts(F).slice(0,10); const upr=F.filter(x=>x.mech===UPR); const nf=upr.filter(x=>!(x.states&&x.states.length)).length;
    box.innerHTML='<div class="mono">Ten States that made most recommendations to '+esc(country)+'</div>'+
     (sc.length?'<ol>'+sc.map(e=>'<li><button class="themebtn" data-st="'+esc(e[0])+'">'+esc(e[0])+'</button> — '+fmt(e[1])+'</li>').join('')+'</ol>':'<p class="empty">No State found in the current filter.</p>')+
     '<p class="how">How this is computed: UPR recommendations only; the State is read from the parentheses at the end of the text, and a recommendation made by several States counts once for each. '+fmt(nf)+' of '+fmt(upr.length)+' UPR records here have no State found. A count of recommendations, not of influence. Click a name = filter.</p>';
  }
  const top=V.top;
  $('#fig1title').textContent='Ten most frequent themes among '+fmt(n)+' filtered records'+(usingMine()?' (with your corrections)':'');
  $('#themeBody').innerHTML=top.length?top.map(t=>'<tr><td><button class="themebtn" data-t="'+esc(t.name)+'">'+esc(t.name)+'</button></td><td class="num">'+fmt(t.n)+'</td><td class="num">'+pct(t.n,n)+'</td><td>'+yrange(t)+'</td></tr>').join(''):'<tr><td colspan="4" class="empty">No records match</td></tr>';
  const src='Source: UHRI (OHCHR), '+esc(country)+'; '+fmt(n)+' of '+fmt(N)+' records'+(describeFilters().length?'; filter: '+esc(describeFilters().join('; ')):'; no filter')+'; '+esc(viewNote())+'.';
  $('#src1').innerHTML=src; $('#src2').innerHTML=src;
  $('#chart1box').hidden=!top.length; $('#fig1empty').hidden=!!top.length;
  $('#fig2title').textContent='Records per year by mechanism, '+fmt(n)+' filtered records';
  if(S.tab===0){drawChart1();drawChart2();}
}
const valueLabels={id:'valueLabels',afterDatasetsDraw(chart){
  const ctx=chart.ctx,meta=chart.getDatasetMeta(0); ctx.save(); ctx.fillStyle='#1d1b18'; ctx.font='600 12px ui-monospace,Menlo,Consolas,monospace'; ctx.textBaseline='middle';
  meta.data.forEach((bar,i)=>{ctx.fillText(fmt(chart.data.datasets[0].data[i]),bar.x+6,bar.y);}); ctx.restore();}};
function wrapLabel(s){
  if(s.length<=36) return s; const out=[]; let cur='';
  s.split(' ').forEach(w=>{ if((cur+' '+w).trim().length>36&&cur){out.push(cur);cur=w;} else cur=(cur+' '+w).trim(); });
  if(cur) out.push(cur); return out;
}
function drawChart1(){
  if(chart1){chart1.destroy();chart1=null;}
  const top=V.top; if(!top.length||typeof Chart==='undefined') return;
  chart1=new Chart($('#chart1'),{type:'bar',
    data:{labels:top.map(t=>wrapLabel(t.name)),datasets:[{data:top.map(t=>t.n),backgroundColor:'rgba(155,35,53,0.8)',borderWidth:0}]},
    options:{indexAxis:'y',responsive:true,maintainAspectRatio:false,animation:false,layout:{padding:{right:50}},
      plugins:{legend:{display:false},tooltip:{callbacks:{title:i=>top[i[0].dataIndex].name}}},
      scales:{x:{display:false,beginAtZero:true,grid:{display:false}},y:{grid:{display:false},border:{display:false},ticks:{color:'#1d1b18',font:{size:12}}}},
      onClick:(e,els)=>{if(els.length)addTheme(top[els[0].index].name);},
      onHover:(e,els)=>{if(e.native&&e.native.target)e.native.target.style.cursor=els.length?'pointer':'default';}},
    plugins:[valueLabels]});
}
function drawChart2(){
  if(chart2){chart2.destroy();chart2=null;}
  const ys=F.map(x=>x.year).filter(Number.isFinite);
  $('#chart2box').hidden=!ys.length; $('#fig2empty').hidden=!!ys.length;
  if(!ys.length||typeof Chart==='undefined') return;
  let a=Infinity,b=-Infinity; ys.forEach(y=>{if(y<a)a=y;if(y>b)b=y;});
  const labels=[]; for(let y=a;y<=b;y++) labels.push(String(y));
  const mechs=mechList.filter(m=>F.some(x=>x.mech===m));
  const ds=mechs.map(m=>{const c=countBy(F.filter(x=>x.mech===m),x=>x.year);return {label:m,backgroundColor:mechColor(m),borderWidth:0,data:labels.map(l=>c.get(Number(l))||0)};});
  $('#chart2').setAttribute('aria-label','Stacked bar chart of records per year from '+a+' to '+b+' by mechanism');
  chart2=new Chart($('#chart2'),{type:'bar',data:{labels,datasets:ds},options:{responsive:true,maintainAspectRatio:false,animation:false,
    plugins:{legend:{position:'top',labels:{boxWidth:12,color:'#1d1b18'}}},
    scales:{x:{stacked:true,grid:{display:false},ticks:{autoSkip:false,maxRotation:90,minRotation:0,color:'#1d1b18',font:{size:11}}},y:{stacked:true,beginAtZero:true,grid:{color:'#e6e0d2'},ticks:{color:'#1d1b18'},title:{display:true,text:'Records'}}}}});
}
function addTheme(t){if(S.themes.indexOf(t)<0)S.themes.push(t);changed();}

/* ---------- records ---------- */
function renderRecords(){
  const n=F.length; const rows=sortedRows(F); const shown=rows.slice(0,S.shown);
  $('#cap').textContent=n?('Showing '+fmt(shown.length)+' of '+fmt(n)+' matching rows, '+(S.dateDir<0?'newest first':'oldest first')+' (dated by document)'):'No records match the current filters.';
  $('#sortDate').innerHTML='Date '+(S.dateDir<0?'▼':'▲');
  $('#tb').innerHTML=shown.map(x=>{
    const open=S.expanded.has(x.i); const url=safeUrl(x.url);
    const st=x.mech===UPR?(x.states&&x.states.length?esc(x.states.join('; ')):'<span class="hint">State not found</span>'):'—';
    let h='<tr class="rec'+(open?' open':'')+'" data-i="'+x.i+'"><td><button class="rowbtn" aria-expanded="'+open+'" data-i="'+x.i+'">'+esc(x.date||'—')+'</button></td><td>'+hl(x.body)+'</td><td class="sym">'+(url?'<a href="'+esc(url)+'" target="_blank" rel="noopener">'+hl(x.symbol)+'</a>':hl(x.symbol))+'</td><td class="num">'+(x.para?esc(x.para):'—')+'</td><td>'+hl(x.first)+corrTag(x)+'</td><td>'+st+'</td></tr>';
    if(open){
      const lab=(t,items)=>'<dt>'+t+'</dt><dd>'+(items.length?items.map(i=>'<span class="tag">'+esc(i)+'</span>').join(''):'<span class="hint">not labelled</span>')+'</dd>';
      h+='<tr class="det"><td colspan="6"><div class="detail"><div class="pnum">'+(x.para?esc(x.para):'—')+'</div><div><p class="fulltext">'+hl(x.text)+'</p><dl class="labels">'+
        (x.section?'<dt>Section</dt><dd>'+esc(x.section)+'</dd>':'')+
        '<dt>Themes (the UN\'s labels'+(corr.has(x.key)?'; yours in red':'')+')</dt><dd>'+themesHtml(x)+'</dd>'+
        lab('SDGs',x.sdgs.map(g=>'SDG '+g+(SDGN[g]?' · '+SDGN[g]:'')))+lab('SDG targets',x.targets)+lab('Affected persons',x.persons)+
        '</dl><div><button class="btn copycite" data-i="'+x.i+'">Copy citation'+(x.para?'':' (no paragraph number in this extract)')+'</button> '+(url?'<a href="'+esc(url)+'" target="_blank" rel="noopener">Open the UN document</a>':'')+(corr.has(x.key)?' <button class="btn" data-undo="'+esc(x.key)+'">Undo my correction</button>':'')+' <span class="copied" role="status"></span></div></div></div></td></tr>';
    }
    return h;
  }).join('')||'<tr><td colspan="6" class="empty">No records match</td></tr>';
  $('#more').hidden=S.shown>=n;
  $('#more').textContent='Show '+Math.min(50,n-S.shown)+' more';
  $('#src3').innerHTML='Source: UHRI (OHCHR), '+esc(country)+'; rows are paragraphs of UN documents, linked by symbol. Sorted by document date, body, paragraph number. '+esc(viewNote())+'.';
}

/* ---------- checks ---------- */
function linkOk(x){
  if(x.url.indexOf('https://docs.un.org/')!==0) return false;
  let u=x.url; try{u=decodeURIComponent(u);}catch(e){}
  return u.toLowerCase().endsWith(x.symbol.toLowerCase());
}
function chk(status,name,vals,extra){
  const mark={pass:'<span class="ok">✓ pass</span>',fail:'<span class="bad">✕ check failed</span>',warn:'<span class="warnm">▲ warning</span>',info:'<span class="inf">○ note</span>'}[status];
  return '<li class="chk"><div class="chkh">'+mark+'<strong>'+esc(name)+'</strong></div><div class="vals">'+vals+'</div>'+(extra||'')+'</li>';
}
function listDetails(label,items,cap){
  if(!items.length) return '';
  cap=cap||40; return '<details><summary>'+esc(label)+' ('+fmt(items.length)+')</summary><ul>'+items.slice(0,cap).join('')+(items.length>cap?'<li>… and '+fmt(items.length-cap)+' more</li>':'')+'</ul></details>';
}
function fileChecks(){
  if(fileChecksCache) return fileChecksCache;
  const out=[];
  const cnt=Number(D.count);
  out.push(chk(cnt===RAW.length?'pass':'fail','Record count','records.length = '+fmt(RAW.length)+' · count field in the file = '+(Number.isFinite(cnt)?fmt(cnt):esc(String(D.count)))));
  const sum=m=>[...m.values()].reduce((a,b)=>a+b,0);
  const sm=sum(countBy(recs,x=>x.mech)),sb=sum(countBy(recs,x=>x.body)),sy=sum(countBy(recs,x=>String(x.year)));
  out.push(chk(sm===N&&sb===N&&sy===N?'pass':'fail','Partitions','sum per mechanism = '+fmt(sm)+' · per body = '+fmt(sb)+' · per year = '+fmt(sy)+' · records = '+fmt(N)));
  const bad=recs.filter(x=>!linkOk(x));
  out.push(chk(bad.length?'fail':'pass','Links','Records whose doc_url starts with https://docs.un.org/ and ends with the symbol: '+fmt(N-bad.length)+' of '+fmt(N),listDetails('records that fail',bad.map(x=>'<li>'+esc(x.symbol)+' → '+esc(x.url||'(empty)')+'</li>'))));
  const pm=mechList.map(m=>{const L=recs.filter(x=>x.mech===m);const f=L.filter(x=>x.para).length;return {m,f,t:L.length};});
  const upr=pm.find(p=>p.m===UPR);
  out.push(chk(upr&&upr.f<upr.t?'warn':'pass','Paragraph numbers found',pm.map(p=>esc(p.m)+': '+fmt(p.f)+' of '+fmt(p.t)+' ('+pct(p.f,p.t)+')').join(' · ')+' · UPR is expected at 100%'));
  const uprR=recs.filter(x=>x.mech===UPR); const noSt=uprR.filter(x=>!(x.states&&x.states.length));
  out.push(chk(noSt.length?'warn':'pass','States found','UPR records with at least one State: '+fmt(uprR.length-noSt.length)+' of '+fmt(uprR.length),
    listDetails('UPR records without a State',noSt.map(x=>'<li>'+esc(x.symbol)+' — '+(x.tail?'parentheses held: <code>'+esc(x.tail.slice(0,120))+'</code>':'no parenthesis at the end of the text')+'</li>'))));
  const ids=new Set(recs.map(x=>x.id)).size; const tm=countBy(recs,x=>x.text); let dt=0,sur=0; tm.forEach(v=>{if(v>1){dt++;sur+=v-1;}});
  out.push(chk(ids===N?'pass':'fail','Identifiers','distinct id = '+fmt(ids)+' · records = '+fmt(N)));
  out.push(chk('info','Duplicates and gaps',fmt(dt)+' text values appear more than once ('+fmt(sur)+' surplus records) · not labelled (labels as shown now): '+fmt(recs.filter(x=>!x.themes.length).length)+' without themes, '+fmt(recs.filter(x=>!x.sdgs.length).length)+' without SDGs, '+fmt(recs.filter(x=>!x.persons.length).length)+' without affected persons'));
  fileChecksCache=out; return out;
}
function corrChecks(){
  const out=[];
  let same=0; recs.forEach((x,k)=>{if(JSON.stringify(uniq(arr(RAW[k].themes).map(String)))===JSON.stringify(x.themesUN))same++;});
  out.push(chk(same===N?'pass':'fail',"The UN's labels are kept",'records whose original themes are unchanged: '+fmt(same)+' of '+fmt(N)));
  let sumUN=0,sumNow=0,rem=0,add=0; recs.forEach(x=>{sumUN+=x.themesUN.length;sumNow+=x.themes.length;const c=corr.get(x.key);if(c){rem+=c.remove.length;add+=c.add.length;}});
  const exp=S.view==='mine'?sumUN-rem+add:sumUN;
  out.push(chk(sumNow===exp?'pass':'fail','Your corrections','labels in the file: UN '+fmt(sumUN)+' · shown now ('+(S.view==='mine'?'with your corrections':'UN labels')+') '+fmt(sumNow)+' · expected '+fmt(exp)+(S.view==='mine'?' = UN − '+fmt(rem)+' removed + '+fmt(add)+' added':' (corrections are applied only with the switch on)')+' · '+fmt(labelCount())+' label'+(labelCount()===1?'':'s')+' corrected in '+fmt(corr.size)+' record'+(corr.size===1?'':'s')));
  return out;
}
function renderChecks(){
  const out=[]; const f=fileChecks();
  out.push(f[0],f[1]);
  const tc=countBy(F,x=>x.type); const st=[...tc.values()].reduce((a,b)=>a+b,0);
  out.push(chk(st===F.length?'pass':'fail','Type partition (current filter)','sum per type = '+fmt(st)+' · headline total = '+fmt(F.length)));
  const top=V.top; const second=top.map(t=>F.filter(x=>x.themes.indexOf(t.name)>=0).length);
  const dom=[...document.querySelectorAll('#themeBody tr')].filter(tr=>tr.children.length>1).map(tr=>Number(tr.children[1].textContent.replace(/[^\d]/g,'')));
  const bars=top.map(t=>t.n);
  const eq=(a,b)=>a.length===b.length&&a.every((v,i)=>v===b[i]);
  const mx=bars.length?Math.max.apply(null,bars):0;
  const ok=eq(bars,second)&&eq(bars,dom)&&mx<=F.length;
  out.push(chk(ok?'pass':'fail','Chart against table','bar values: '+(bars.map(fmt).join(', ')||'none')+' · recounted by a second loop: '+(second.map(fmt).join(', ')||'none')+' · table cells: '+(dom.map(fmt).join(', ')||'none')+' · largest bar '+fmt(mx)+' ≤ '+fmt(F.length)+' filtered records'));
  out.push(f[2],f[3],f[4],f[5],f[6]);
  corrChecks().forEach(c=>out.push(c));
  $('#checks').innerHTML=out.join('');
}

/* ---------- random sample ---------- */
function mulberry32(a){return function(){a|=0;a=a+0x6D2B79F5|0;let t=Math.imul(a^a>>>15,1|a);t=t+Math.imul(t^t>>>7,61|t)^t;return((t^t>>>14)>>>0)/4294967296;};}
function draw(seed){
  seed=Math.floor(Number(seed)); if(!Number.isFinite(seed)) seed=1;
  $('#seed').value=seed;
  const rnd=mulberry32(seed); const idx=F.map((_,k)=>k); const take=Math.min(10,F.length);
  for(let k=0;k<take;k++){const j=k+Math.floor(rnd()*(idx.length-k));const t=idx[k];idx[k]=idx[j];idx[j]=t;}
  S.sample={seed,recs:idx.slice(0,take).map(k=>F[k]),filter:describeFilters().join('; ')||'no filter',n:F.length};
  S.verdict={};S.card=-1;S.edit=-1;
  $('#drawFirst').hidden=true;$('#drawAgain').hidden=false;$('#drawSeed').hidden=false;
  renderSample();
}
const VLAB={fit:'Fits',no:"Doesn't fit",unsure:'Unsure'};
function editorHtml(x){
  const c=corr.get(x.key)||{remove:[],add:[],mark:S.pend}; const rm=new Set(c.remove);
  const avail=ALLTHEMES.filter(e=>x.themesUN.indexOf(e[0])<0&&c.add.indexOf(e[0])<0);
  return '<div class="editor"><p class="hint">The UN\'s labels are kept. Your change is stored beside them and, with the switch on "With my corrections", changes every count, chart and filter.</p>'+
   '<div class="mono">The UN\'s labels: click to remove, click again to restore</div><div>'+
   (x.themesUN.length?x.themesUN.map((t,j)=>'<button class="tag" data-rmt="'+esc(t)+'" data-i="'+x.i+'" aria-pressed="'+rm.has(t)+'" data-fk="rm'+x.i+'-'+j+'">'+(rm.has(t)?'<s>'+esc(t)+'</s> <span class="act">restore</span>':esc(t)+' <span class="act">remove</span>')+'</button>').join(''):'<span class="hint">none</span>')+'</div>'+
   '<div class="mono" style="margin-top:8px">Labels you added</div><div>'+
   (c.add.length?c.add.map((t,j)=>'<button class="tag mine" data-dropt="'+esc(t)+'" data-i="'+x.i+'" data-fk="dp'+x.i+'-'+j+'">+ '+esc(t)+' <span class="act">drop</span></button>').join(''):'<span class="hint">none yet</span>')+'</div>'+
   (avail.length?'<div class="seedrow"><label class="mono" for="addSel">Add a label that occurs in the data</label><select id="addSel" data-fk="addsel" style="max-width:380px">'+avail.map(e=>'<option value="'+esc(e[0])+'">'+esc(e[0])+' ('+fmt(e[1])+' records)</option>').join('')+'</select><button class="btn" data-addt="'+x.i+'" data-fk="addbtn">Add</button></div>':'')+
   '<div class="seedrow"><span class="mono">My mark</span>'+['wrong','arguable'].map(m=>'<button class="btn" data-mark="'+m+'" data-i="'+x.i+'" aria-pressed="'+(c.mark===m)+'" data-fk="mk'+x.i+m+'">'+(m==='wrong'?'Wrong':'Arguable')+'</button>').join('')+
   (corr.has(x.key)?'<button class="btn" data-undo="'+esc(x.key)+'" data-fk="undo'+x.i+'">Undo this correction</button>':'')+'</div></div>';
}
function renderSample(){
  const sm=S.sample;
  if(!sm){$('#cards').innerHTML='';$('#sampleInfo').textContent='Draws ten records from the current filter with a seeded generator, so a colleague can draw the same ten.';$('#tally').textContent='Nothing judged yet.';return;}
  $('#sampleInfo').textContent='Drawn from '+fmt(sm.n)+' records (filter: '+sm.filter+') with seed '+sm.seed+'. Same filter and seed give the same ten (with the same labels in force).';
  if(!sm.recs.length){$('#cards').innerHTML='<li class="empty">No records match: nothing to draw.</li>';$('#tally').textContent='';return;}
  $('#cards').innerHTML=sm.recs.map((x,k)=>{
    const open=S.card===k; const v=S.verdict[x.i]; const url=safeUrl(x.url); const ed=S.edit===x.i;
    const link=url?'<a href="'+esc(url)+'" target="_blank" rel="noopener">'+esc(x.symbol)+'</a>':esc(x.symbol);
    return '<li><div class="cardline"><button class="cardtoggle" aria-expanded="'+open+'" data-k="'+k+'" data-fk="tog'+k+'"><span class="mono">'+String(k+1).padStart(2,'0')+'</span> '+esc(x.first)+'</button><span class="hint">'+link+(x.para?' · para. '+esc(x.para):'')+'</span>'+corrTag(x)+'<span class="vtag">'+(v?esc(VLAB[v]):'')+'</span></div>'+
     (open?'<div class="cardbody"><p class="mono">'+link+' · '+(x.para?'para. '+esc(x.para):'no paragraph number')+'</p><p class="fulltext">'+esc(x.text)+'</p><div class="mono" style="margin-bottom:4px">Themes (the UN\'s labels'+(corr.has(x.key)&&S.view==='mine'?'; yours in red':'')+')</div><div>'+themesHtml(x)+'</div>'+
     '<div class="verds" role="group" aria-label="Do the themes fit this paragraph, as a set?">'+['fit','no','unsure'].map(c=>'<button class="btn verd" data-v="'+c+'" data-i="'+x.i+'" aria-pressed="'+(v===c)+'" data-fk="v'+x.i+c+'">'+esc(VLAB[c])+'</button>').join('')+'</div>'+
     '<div style="margin-top:10px"><button class="btn" data-ed="'+x.i+'" aria-expanded="'+ed+'" data-fk="ed'+x.i+'">Correct these labels</button></div>'+(ed?editorHtml(x):'')+'</div>':'')+'</li>';
  }).join('');
  const vs=sm.recs.map(x=>S.verdict[x.i]).filter(Boolean);
  const c=k=>vs.filter(v=>v===k).length;
  $('#tally').textContent='Themes: '+c('fit')+' fit, '+c('no')+" don't, "+c('unsure')+' unsure of '+vs.length+' judged · seed '+sm.seed+' · your judgement of the UN’s labels; the app never changes a UN label';
}

/* ---------- corrections panel, CSV out and in ---------- */
let armed=false,armT=null;
function renderCorr(){
  const list=recs.filter(x=>corr.has(x.key)); const n=labelCount();
  $('#corrSum').textContent='Your corrections: '+fmt(n)+' label'+(n===1?'':'s')+' in '+fmt(list.length)+' record'+(list.length===1?'':'s')+' (undo, download, load)';
  $('#corrList').innerHTML=list.length?'<ol class="corrlist">'+list.map(x=>{
    const c=corr.get(x.key); const url=safeUrl(x.url);
    return '<li><div><strong>'+(url?'<a href="'+esc(url)+'" target="_blank" rel="noopener">'+esc(x.symbol)+'</a>':esc(x.symbol))+'</strong>'+(x.para?' · para. '+esc(x.para):' · no paragraph number')+' · <span class="hint">marked '+esc(c.mark)+'</span></div><div>'+
      c.remove.map(t=>'<span class="tag gone"><s>'+esc(t)+'</s><span class="sr"> (removed by you)</span></span>').join('')+c.add.map(t=>'<span class="tag mine">+ '+esc(t)+'<span class="sr"> (added by you)</span></span>').join('')+
      '</div><button class="textbtn" data-undo="'+esc(x.key)+'">Undo this correction</button></li>';}).join('')+'</ol>'
    :'<p class="hint">No corrections yet. Open one of the ten cards below, then “Correct these labels”.</p>';
  $('#undoAll').hidden=!list.length;
  if(!armed) $('#undoAll').textContent='Undo all '+fmt(n)+' label'+(n===1?'':'s');
  $('#dlCorr').disabled=!list.length;
}
const joinL=a=>a.join(' | ');
const splitL=s=>String(s||'').split('|').map(t=>t.trim()).filter(Boolean);
const csvCell=s=>'"'+String(s==null?'':s).replace(/"/g,'""')+'"';
function downloadCorr(){
  const list=recs.filter(x=>corr.has(x.key)); if(!list.length) return;
  const one=s=>String(s).replace(/[\r\n]+/g,' ');
  const lines=["# Your corrections to the UN's theme labels: "+one(country),'# Source: '+one((D.source||'')+(D.source_url?' ('+D.source_url+')':'')),'# Built: '+one(D.built||''),
   "# un_labels are the UN's own and are kept; my_labels is what you want shown instead; labels are separated by ' | '",'# Rows: '+list.length,
   'symbol,paragraph,un_labels,my_labels,my_mark,record_id'];
  list.forEach(x=>{const c=corr.get(x.key);lines.push([x.symbol,x.para||'',joinL(x.themesUN),joinL(applied(x,c)),c.mark,x.id==null?'':x.id].map(csvCell).join(','));});
  saveText('uhri-'+slug()+'-my-corrections.csv',lines.join('\r\n'));
  flash($('#corrMsg'),'Downloaded '+fmt(list.length)+' corrected record'+(list.length===1?'':'s'));
}
function parseCsv(text){
  text=String(text).replace(/^\ufeff/,'');
  const lines=text.split(/\r?\n/); let start=0;
  while(start<lines.length&&(lines[start].trim()===''||lines[start].charAt(0)==='#')) start++;
  const body=lines.slice(start).join('\n'); const rows=[]; let row=[],cell='',q=false;
  for(let i=0;i<body.length;i++){
    const c=body[i];
    if(q){ if(c==='"'){ if(body[i+1]==='"'){cell+='"';i++;} else q=false; } else cell+=c; }
    else if(c==='"') q=true;
    else if(c===','){row.push(cell);cell='';}
    else if(c==='\n'){row.push(cell);cell='';rows.push(row);row=[];}
    else if(c!=='\r') cell+=c;
  }
  if(cell!==''||row.length){row.push(cell);rows.push(row);}
  return rows.filter(r=>r.some(c=>c.trim()!==''));
}
function loadCorr(text){
  const msg=$('#corrMsg'); $('#corrDet').open=true;
  const rows=parseCsv(text);
  if(rows.length<2){msg.textContent='Nothing loaded: no data rows found.';return;}
  const head=rows[0].map(h=>h.trim().toLowerCase().replace(/[^a-z0-9]+/g,'_'));
  const ix=n=>head.indexOf(n);
  const need=['symbol','paragraph','un_labels','my_labels','my_mark'].filter(n=>ix(n)<0);
  if(need.length){msg.textContent='Nothing loaded: this does not look like a corrections file (missing columns: '+need.join(', ')+').';return;}
  let restored=0,replaced=0,skipped=0,differ=0; const lost=[],unk=[];
  rows.slice(1).forEach(r=>{
    const get=n=>ix(n)<0?'':String(r[ix(n)]==null?'':r[ix(n)]).trim();
    const sym=get('symbol'),para=get('paragraph'),un=splitL(get('un_labels')),mine=splitL(get('my_labels')),id=get('record_id');
    let rec=null;
    if(id&&byKey.has(id)&&(!sym||byKey.get(id).symbol.toLowerCase()===sym.toLowerCase())) rec=byKey.get(id);
    if(!rec){
      let cand=(bySP.get(sym.toLowerCase()+'\u0001'+para)||[]);
      if(cand.length>1) cand=cand.filter(x=>joinL(x.themesUN)===joinL(un));
      if(cand.length===1) rec=cand[0];
    }
    if(!rec){lost.push(sym+(para?' para. '+para:''));return;}
    if(joinL(rec.themesUN)!==joinL(un)) differ++;
    const remove=rec.themesUN.filter(t=>mine.indexOf(t)<0);
    const add=[]; mine.forEach(t=>{if(rec.themesUN.indexOf(t)<0&&add.indexOf(t)<0){ if(themeUNCount.has(t)) add.push(t); else unk.push(t);} });
    if(!remove.length&&!add.length){skipped++;return;}
    if(corr.has(rec.key)) replaced++;
    corr.set(rec.key,{remove,add,mark:/arguable/i.test(get('my_mark'))?'arguable':'wrong'}); restored++;
  });
  if(restored) S.view='mine';
  corrChanged();
  msg.textContent='Loaded: '+fmt(restored)+' record'+(restored===1?'':'s')+' restored'+(replaced?' ('+fmt(replaced)+' replaced an earlier correction of yours)':'')+'; '+fmt(lost.length)+' row'+(lost.length===1?'':'s')+' not matched to a record in this file'+(lost.length?' ('+lost.slice(0,8).join('; ')+(lost.length>8?'; …':'')+')':'')+'; '+fmt(skipped)+' row'+(skipped===1?'':'s')+' without a change skipped'+(unk.length?'; labels not found in the data ignored: '+uniq(unk).slice(0,5).join('; '):'')+(differ?'; '+fmt(differ)+' row'+(differ===1?'':'s')+' where the UN labels in the CSV differ from this file (restored anyway)':'')+'.';
}

/* ---------- method and export ---------- */
function summaryText(){
  const n=F.length; const types=[...countBy(F,x=>x.type).entries()].sort((a,b)=>b[1]-a[1]);
  const ys=F.map(x=>x.year).filter(Number.isFinite); let a=Infinity,b=-Infinity; ys.forEach(y=>{if(y<a)a=y;if(y>b)b=y;});
  const mt=mechList.map(m=>m+' '+fmt(F.filter(x=>x.mech===m).length)).join(', ');
  const lines=['UN human rights recommendations and observations: '+country,
   'Source: '+(D.source||'')+(D.source_url?' ('+D.source_url+')':'')+(D.built?', built '+D.built:''),
   'Filter: '+(describeFilters().join('; ')||'none'),
   'Theme '+viewNote()+(corr.size?' ('+fmt(corr.size)+' record'+(corr.size===1?'':'s')+' corrected by the reader; the UN labels are kept)':''),
   fmt(n)+' of '+fmt(N)+' records from '+fmt(new Set(F.map(x=>x.symbol)).size)+' documents'+(ys.length?', document years '+a+'–'+b:'')+' (dated by document).',
   'By type: '+(types.map(e=>e[0]+' '+fmt(e[1])).join(', ')||'none'),'By mechanism: '+mt,
   'Ten most frequent themes (a record can carry several; percentages are of records):'];
  V.top.forEach((t,i)=>lines.push((i+1)+'. '+t.name+': '+fmt(t.n)+' records, '+pct(t.n,n)+', years '+yrange(t)));
  if(!V.top.length) lines.push('(no records match)');
  lines.push('All figures are counts made in the browser from the file; themes are the UN’s own labels unless stated.');
  return lines.join('\n');
}
function renderMethod(){
  $('#methodText').innerHTML=
   '<p>Every number is a count made by JavaScript in your browser over the records of the file; nothing is estimated and no model is called.</p>'+
   '<p>Filters combine with AND. Mechanism, body and type are exact matches; years are inclusive; the SDG is matched by goal number; for the keyword, every word must occur literally in the paragraph text or the document symbol.</p>'+
   '<p>A record can carry several themes. Each theme counts once per record that carries it, so the bars of FIG.01 add up to more than the records, and percentages are of records, not of labels.</p>'+
   '<p>The paragraph number is the number at the start of the text (for example 71, or 144.43 for UPR); where none is found, citations carry the symbol alone. The recommending State is read only from UPR texts, from the parentheses at the end; a group with a comma or more than 60 characters is not taken as a State.</p>'+
   '<p>Dates are the dates of the documents, not of the recommendations. Themes, SDGs and affected persons are the UN’s labels: the app never changes them, and tab 03 lets you judge a random sample. Follow-up and acceptance of UPR recommendations are not in this file.</p>'+
   '<p>Your corrections to theme labels are stored beside the UN’s labels, never over them. The switch under the title decides whether every count, chart, filter and export uses the UN’s labels or yours. They are kept only while this page is open: download them from tab 03 and load the file again to restore them.</p>'+
   '<p class="hint">Labels now: '+esc(viewNote())+'.</p>';
  $('#summaryPre').textContent=summaryText();
  $('#dataInfo').innerHTML='Data: '+(D.source?esc(D.source):'UHRI')+(safeUrl(D.source_url)?' — <a href="'+esc(D.source_url)+'" target="_blank" rel="noopener">source page</a>':'')+' · built '+esc(D.built||'date not stated')+' · licence: '+esc(D.licence||D.license||'not stated in the file; check the terms of use of the source before republishing')+'.';
}
function downloadCsv(){
  const rows=sortedRows(F); const one=s=>String(s).replace(/[\r\n]+/g,' ');
  const lines=['# Country: '+one(country),'# Source: '+one((D.source||'')+(D.source_url?' ('+D.source_url+')':'')),'# Built: '+one(D.built||''),'# Filters: '+one(describeFilters().join('; ')||'none'),'# Rows: '+rows.length,'# Theme '+one(viewNote())+'; themes_un always holds the UN labels','# Dates are document dates; themes, SDGs and persons are the UN labels unless corrected_by_you is yes'];
  lines.push(['date','body','mechanism','type','symbol','doc_url','paragraph','recommending_states','first_line','text','section','themes','themes_un','corrected_by_you','sdgs','sdg_targets','affected_persons'].join(','));
  rows.forEach(x=>lines.push([x.date,x.body,x.mech,x.type,x.symbol,x.url,x.para||'',x.mech===UPR?(x.states&&x.states.length?x.states.join(' | '):'State not found'):'',x.first,x.text,x.section,x.themes.join(' | '),x.themesUN.join(' | '),corr.has(x.key)?'yes':'no',x.sdgs.map(g=>g+(SDGN[g]?' '+SDGN[g]:'')).join(' | '),x.targets.join(' | '),x.persons.join(' | ')].map(csvCell).join(',')));
  saveText('uhri-'+slug()+'-'+rows.length+'-rows.csv',lines.join('\r\n'));
  flash($('#exportMsg'),'CSV prepared: '+fmt(rows.length)+' rows');
}

/* ---------- render and events ---------- */
function render(){
  W=words(); F=applyFilters(); V.top=topThemes(F);
  renderRail(); renderOverview();
  if(S.tab===1) renderRecords();
  if(S.tab===2){renderChecks(); renderSample(); renderCorr();}
  if(S.tab===3) renderMethod();
}
function setTab(i,focus){
  S.tab=i;
  [0,1,2,3].forEach(k=>{const t=$('#t'+k);t.setAttribute('aria-selected',k===i);t.tabIndex=k===i?0:-1;$('#p'+k).hidden=k!==i;});
  if(focus)$('#t'+i).focus();
  render();
}
function setView(v){S.view=v;fileChecksCache=null;refreshThemes();renderView();render();}
function wire(){
  $('#viewUN').addEventListener('click',()=>setView('un'));
  $('#viewMine').addEventListener('click',()=>setView('mine'));
  $('#tabs').addEventListener('click',e=>{const b=e.target.closest('.tab');if(b)setTab(Number(b.id.slice(1)));});
  $('#tabs').addEventListener('keydown',e=>{
    let i=S.tab; const k=e.key;
    if(k==='ArrowRight')i=(i+1)%4;else if(k==='ArrowLeft')i=(i+3)%4;else if(k==='Home')i=0;else if(k==='End')i=3;else return;
    e.preventDefault();setTab(i,true);
  });
  document.querySelectorAll('.acchead').forEach(b=>b.addEventListener('click',()=>{const i=Number(b.dataset.a);S.acc=S.acc===i?-1:i;renderRail();}));
  $('#clearAll').addEventListener('click',()=>{clearAll();changed();});
  $('#chips').addEventListener('click',e=>{const b=e.target.closest('.chip');if(!b)return;V.chips[Number(b.dataset.c)].rm();changed();});
  let tm;
  const typed=(src,other)=>e=>{const v=e.target.value;other.value=v;clearTimeout(tm);tm=setTimeout(()=>{S.q=v;changed();},300);};
  $('#kwRail').addEventListener('input',typed($('#kwRail'),$('#kwTop')));
  $('#kwTop').addEventListener('input',typed($('#kwTop'),$('#kwRail')));
  $('#selMech').addEventListener('change',e=>{S.mech=e.target.value;S.body='';changed();});
  $('#selBody').addEventListener('change',e=>{S.body=e.target.value;changed();});
  $('#selType').addEventListener('change',e=>{S.type=e.target.value;changed();});
  $('#selState').addEventListener('change',e=>{S.st=e.target.value;changed();});
  $('#selSdg').addEventListener('change',e=>{S.sdg=e.target.value;changed();});
  const yr=which=>e=>{const v=Number(e.target.value);if(which==='f')S.yf=v;else S.yt=v;if(S.yf>S.yt){const t=S.yf;S.yf=S.yt;S.yt=t;}changed();};
  $('#selYf').addEventListener('change',yr('f'));$('#selYt').addEventListener('change',yr('t'));
  $('#p0').addEventListener('click',e=>{
    const t=e.target.closest('[data-t]'); if(t){addTheme(t.dataset.t);return;}
    const s=e.target.closest('[data-st]'); if(s){S.st=s.dataset.st;changed();return;}
    if(e.target.closest('#seeStates')){S.showStates=!S.showStates;renderOverview();const b=$('#seeStates');if(b)b.focus();}
  });
  $('#sortDate').addEventListener('click',()=>{S.dateDir=-S.dateDir;renderRecords();$('#sortDate').focus();});
  $('#more').addEventListener('click',()=>{S.shown+=50;renderRecords();});
  $('#tb').addEventListener('click',e=>{
    const cp=e.target.closest('.copycite');
    if(cp){const x=recs[Number(cp.dataset.i)];const msg=cp.parentElement.querySelector('.copied');copyText(cite(x)).then(ok=>flash(msg,ok?'Copied':'Copy failed: select the text by hand'));return;}
    if(e.target.closest('a')||e.target.closest('[data-undo]'))return;
    const tr=e.target.closest('tr.rec'); if(!tr)return;
    const i=Number(tr.dataset.i); if(S.expanded.has(i))S.expanded.delete(i);else S.expanded.add(i);
    renderRecords(); const b=document.querySelector('.rowbtn[data-i="'+i+'"]'); if(b&&document.activeElement!==b&&e.target.closest('button'))b.focus();
  });
  $('#drawFirst').addEventListener('click',()=>draw($('#seed').value));
  $('#drawAgain').addEventListener('click',()=>draw(Math.floor(Math.random()*1000000)+2));
  $('#drawSeed').addEventListener('click',()=>draw($('#seed').value));
  $('#cards').addEventListener('click',e=>{
    const t=e.target.closest('.cardtoggle');
    if(t){const k=Number(t.dataset.k);S.card=S.card===k?-1:k;S.edit=-1;keepFocus(renderSample);return;}
    const v=e.target.closest('.verd');
    if(v){S.verdict[v.dataset.i]=v.dataset.v;keepFocus(renderSample);return;}
    const ed=e.target.closest('[data-ed]');
    if(ed){const i=Number(ed.dataset.ed);S.edit=S.edit===i?-1:i;keepFocus(renderSample);return;}
    const rmb=e.target.closest('[data-rmt]');
    if(rmb){const x=recs[Number(rmb.dataset.i)],t2=rmb.dataset.rmt;if(x.themesUN.indexOf(t2)<0)return;
      mutate(x,c=>{const k=c.remove.indexOf(t2);if(k<0)c.remove.push(t2);else c.remove.splice(k,1);});return;}
    const dr=e.target.closest('[data-dropt]');
    if(dr){const x=recs[Number(dr.dataset.i)],t2=dr.dataset.dropt;mutate(x,c=>{const k=c.add.indexOf(t2);if(k>=0)c.add.splice(k,1);});return;}
    const ad=e.target.closest('[data-addt]');
    if(ad){const x=recs[Number(ad.dataset.addt)];const sel=$('#addSel');const t2=sel?sel.value:'';
      if(!t2||!themeUNCount.has(t2)||x.themesUN.indexOf(t2)>=0)return;
      mutate(x,c=>{if(c.add.indexOf(t2)<0)c.add.push(t2);});return;}
    const mk=e.target.closest('[data-mark]');
    if(mk){S.pend=mk.dataset.mark;const x=recs[Number(mk.dataset.i)];
      if(corr.has(x.key)){corr.get(x.key).mark=S.pend;corrChanged();}else keepFocus(renderSample);return;}
  });
  document.addEventListener('click',e=>{
    const u=e.target.closest&&e.target.closest('[data-undo]');
    if(u&&corr.has(u.dataset.undo)){corr.delete(u.dataset.undo);corrChanged();}
  });
  $('#undoAll').addEventListener('click',()=>{
    if(!armed){armed=true;$('#undoAll').textContent='Click again to undo all';armT=setTimeout(()=>{armed=false;renderCorr();},4000);return;}
    clearTimeout(armT);armed=false;corr.clear();corrChanged();
  });
  $('#dlCorr').addEventListener('click',downloadCorr);
  $('#loadBtn').addEventListener('click',()=>$('#corrFile').click());
  $('#corrFile').addEventListener('change',e=>{
    const f=e.target.files&&e.target.files[0]; if(!f)return;
    const rd=new FileReader(); rd.onload=()=>{loadCorr(String(rd.result||''));}; rd.onerror=()=>{$('#corrMsg').textContent='The file could not be read; paste its text below instead.';};
    rd.readAsText(f); e.target.value='';
  });
  $('#loadPaste').addEventListener('click',()=>{const t=$('#corrPaste').value; if(!t.trim()){$('#corrMsg').textContent='Nothing to load: the box is empty.';return;} loadCorr(t);});
  $('#dlCsv').addEventListener('click',downloadCsv);
  $('#cpSummary').addEventListener('click',()=>{copyText(summaryText()).then(ok=>flash($('#exportMsg'),ok?'Copied':'Copy failed: select the text below by hand'));});
}
initStatic();
wire();
renderView();
renderSample();
if(!N){document.querySelector('main').insertAdjacentHTML('afterbegin','<p class="empty">The file holds no records, so there is nothing to show.</p>');}
render();
})();
</script>
</body>
</html>
```