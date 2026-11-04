I built the Kenya dashboard with four tabs: Overview, Records, Check and Method & export. The filters sit in a left rail, and all numbers come from the file. The recommending-State extraction, the self-checks and the seeded 10-record label check are built in; no model is called.

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>UN human rights recommendations and observations</title>
<style>
:root{--paper:#f4f0e8;--ink:#1d1b18;--rule:#d9d2c3;--red:#9b2335;--mute:#5b564c;--serif:Georgia,"Times New Roman",serif;--mono:ui-monospace,Menlo,Consolas,monospace}
*{box-sizing:border-box}
body{margin:0;background:var(--paper);color:var(--ink);font:16px/1.5 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif}
[hidden]{display:none!important}
a{color:var(--red)}
:focus-visible{outline:3px solid var(--red);outline-offset:2px}
button{font:inherit;color:inherit;cursor:pointer}
.mono{font:11.5px/1.4 var(--mono);letter-spacing:.08em;text-transform:uppercase;color:var(--mute)}
.wrap{max-width:1300px;margin:0 auto;padding:0 20px}
header{padding:18px 0 10px;border-bottom:1px solid var(--rule)}
h1{font:400 clamp(24px,3.2vw,38px)/1.15 var(--serif);margin:4px 0 6px}
.srcline{font-size:14px;color:var(--mute);margin:0}
.tabs{display:flex;gap:4px;border-bottom:1px solid var(--rule);flex-wrap:wrap}
.tabs button{background:none;border:0;border-bottom:3px solid transparent;padding:12px 14px 9px;font:12px var(--mono);letter-spacing:.08em;text-transform:uppercase;color:var(--mute)}
.tabs button[aria-selected=true]{color:var(--red);border-bottom-color:var(--red);font-weight:700}
.layout{display:grid;grid-template-columns:260px minmax(0,1fr);gap:30px;padding:20px 0 30px}
@media(max-width:860px){.layout{grid-template-columns:1fr}}
.rail{border-right:1px solid var(--rule);padding-right:20px}
@media(max-width:860px){.rail{border-right:0;padding-right:0;border-bottom:1px solid var(--rule);padding-bottom:14px}}
.rail-head{display:flex;justify-content:space-between;align-items:center}
.link{background:none;border:0;padding:2px 0;color:var(--red);text-decoration:underline;font-size:14px}
.big{font:400 48px/1.05 var(--serif)}
.rail .big{margin-top:10px}
.of{font-size:13px;color:var(--mute)}
.bar{height:4px;background:var(--rule);margin:8px 0 10px}.bar i{display:block;height:100%;background:var(--red);width:0}
.chip{display:inline-flex;gap:6px;align-items:center;border:1px solid var(--red);color:var(--red);background:none;font:12px var(--mono);padding:2px 8px;margin:0 4px 4px 0;border-radius:2px;text-align:left}
.acc h3{margin:0;border-top:1px solid var(--rule)}
.acc-h{width:100%;text-align:left;background:none;border:0;padding:10px 0;font:12px var(--mono);letter-spacing:.08em;text-transform:uppercase}
.acc-h .n{color:var(--red);margin-right:8px}
.acc-h[aria-expanded=true]{color:var(--red);font-weight:700}
.acc-p{padding:0 0 12px}
.acc-p label{display:block;font:11px var(--mono);letter-spacing:.06em;text-transform:uppercase;color:var(--mute);margin:8px 0 3px}
input[type=text],input[type=search],input[type=number],select{width:100%;font:inherit;font-size:15px;padding:6px 8px;border:1px solid #b9b19f;background:#fffdf8;color:var(--ink);border-radius:2px}
.hint{font:11px var(--mono);color:var(--mute);margin-top:4px}
h2{font:400 26px/1.2 var(--serif);margin:0 0 4px}
.q{font:400 18px var(--serif);color:var(--mute);margin:0 0 16px;font-style:italic}
.tiles{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:0;border-top:1px solid var(--rule);border-bottom:1px solid var(--rule);margin:8px 0}
.tile{padding:12px 16px 12px 0;margin-right:16px}
.tile .big{font-size:44px}
.tile .sub{font-size:13px;color:var(--mute)}
.dot{display:inline-block;width:10px;height:10px;border-radius:50%;margin-right:6px;vertical-align:baseline}
.how{font-size:13px;color:var(--mute);margin:6px 0 18px;max-width:900px}
.how b{font:11px var(--mono);letter-spacing:.08em;text-transform:uppercase;color:var(--ink);margin-right:6px}
figure{margin:26px 0 0;padding-top:14px;border-top:1px solid var(--rule)}
figcaption .t{font:400 20px var(--serif);display:block;margin:2px 0 8px}
.chartbox{position:relative;width:100%}
table{border-collapse:collapse;width:100%;font-size:15px}
caption{text-align:left;font:12px var(--mono);letter-spacing:.05em;color:var(--mute);padding:6px 0}
th{font:11px var(--mono);letter-spacing:.07em;text-transform:uppercase;text-align:left;color:var(--mute);border-bottom:2px solid var(--ink);padding:6px 8px 6px 0;vertical-align:bottom}
td{border-bottom:1px solid var(--rule);padding:7px 8px 7px 0;vertical-align:top}
.num{text-align:right;font-variant-numeric:tabular-nums}
.nw{white-space:nowrap}
.dim{color:var(--mute)}
tr.main{cursor:pointer}tr.main:hover{background:#ece6d8}
tr.main[aria-expanded=true]{background:#ece6d8}
mark{background:#f0d9a8;color:inherit;padding:0 1px}
.src{font:11px var(--mono);color:var(--mute);margin-top:6px}
.det{display:flex;gap:20px;padding:12px 4px 16px;background:#faf7f0}
.bigpara{font:400 52px/1 var(--serif);color:var(--red);min-width:90px}
.detmain{flex:1;min-width:0}
.fulltext{white-space:pre-wrap;font-size:16px;margin:4px 0 10px;max-width:80ch}
.lab{margin:5px 0;font-size:14px}.lab .mono{display:inline-block;min-width:130px;vertical-align:top}
.tag{display:inline-block;border:1px solid var(--rule);padding:0 7px;margin:0 4px 3px 0;font-size:13px;background:#fffdf8}
.acts{margin-top:10px;display:flex;gap:12px;align-items:center;flex-wrap:wrap}
.btn,.acts button,.btnb{border:1px solid var(--ink);background:#fffdf8;padding:6px 12px;font-size:14px;text-decoration:none;color:var(--ink);border-radius:2px;display:inline-block}
.btn:hover,.acts button:hover,.btnb:hover{background:var(--ink);color:var(--paper)}
.btnb[aria-pressed=true]{background:var(--red);border-color:var(--red);color:#fff}
.btnrow{display:flex;gap:10px;flex-wrap:wrap;align-items:center;margin:10px 0}
.thbtn{background:none;border:0;padding:0;font:inherit;text-transform:inherit;letter-spacing:inherit;color:var(--red);cursor:pointer}
.tbtn{background:none;border:0;padding:0;text-align:left;color:var(--ink);text-decoration:underline dotted;cursor:pointer;font-size:15px}
.chk{list-style:none;display:grid;grid-template-columns:120px minmax(0,1fr);gap:2px 14px;padding:9px 0;border-bottom:1px solid var(--rule)}
.chk .vals{grid-column:2;font-size:14px;color:var(--mute)}
.mark{font:12px var(--mono);letter-spacing:.05em;text-transform:uppercase;font-weight:700}
.ok .mark{color:var(--ink)}.fail .mark{color:var(--red)}.fail .what{color:var(--red);font-weight:600}.warn .mark{color:#7a4b00}.info .mark{color:var(--mute)}
ul.plain{padding:0;margin:0}
details summary{cursor:pointer;color:var(--red);font-size:14px}
details ul{font-size:13px;margin:4px 0}
.card{border-bottom:1px solid var(--rule)}
.card>button{width:100%;text-align:left;background:none;border:0;padding:9px 0;display:flex;gap:10px;align-items:baseline}
.card>button .v{margin-left:auto;font:11px var(--mono);text-transform:uppercase;color:var(--mute);white-space:nowrap}
.card .body{padding:2px 0 14px 30px}
.tally{font:13px var(--mono);margin:10px 0;padding:8px 0;border-top:1px solid var(--ink);border-bottom:1px solid var(--rule)}
.seed{width:90px}
.method p{max-width:75ch}
footer{border-top:1px solid var(--rule);padding:12px 0 24px;font:11.5px var(--mono);letter-spacing:.04em;color:var(--mute)}
.empty{padding:24px 0;font:400 20px var(--serif);color:var(--mute)}
.searchbar{max-width:560px;margin-bottom:6px}
</style>
</head>
<body>
<div class="wrap">
<header>
  <div class="mono" id="hLabel"></div>
  <h1 id="hTitle"></h1>
  <p class="srcline" id="hLine"></p>
</header>
<div class="tabs" role="tablist" aria-label="Dashboard sections">
  <button role="tab" id="t0" aria-controls="p0" aria-selected="true">01 Overview</button>
  <button role="tab" id="t1" aria-controls="p1" aria-selected="false" tabindex="-1">02 Records</button>
  <button role="tab" id="t2" aria-controls="p2" aria-selected="false" tabindex="-1">03 Check</button>
  <button role="tab" id="t3" aria-controls="p3" aria-selected="false" tabindex="-1">04 Method &amp; export</button>
</div>
<div class="layout">
  <aside class="rail" aria-label="Filters">
    <div class="rail-head"><span class="mono">Filters</span><button class="link" id="clearAll">Clear all</button></div>
    <div aria-live="polite">
      <div class="big" id="cnt">0</div>
      <div id="cntLbl">matching records</div>
      <div class="of" id="cntOf"></div>
    </div>
    <div class="bar" aria-hidden="true"><i id="barFill"></i></div>
    <div id="chips"></div>
    <div class="acc" id="acc">
      <h3><button class="acc-h" aria-expanded="false" aria-controls="ap1"><span class="n">01</span>Keyword</button></h3>
      <div class="acc-p" id="ap1" hidden>
        <label for="kw1">Words in the paragraph or symbol</label>
        <input type="text" id="kw1" autocomplete="off">
        <div class="hint">literal match, not synonyms</div>
      </div>
      <h3><button class="acc-h" aria-expanded="false" aria-controls="ap2"><span class="n">02</span>Mechanism, body, type</button></h3>
      <div class="acc-p" id="ap2" hidden>
        <label for="fMech">Mechanism</label><select id="fMech"></select>
        <label for="fBody">Body or mandate</label><select id="fBody"></select>
        <label for="fType">Type</label><select id="fType"></select>
        <div id="stateWrap" hidden><label for="fState">Recommending State (UPR)</label><select id="fState"></select></div>
      </div>
      <h3><button class="acc-h" aria-expanded="false" aria-controls="ap3"><span class="n">03</span>Years and SDG</button></h3>
      <div class="acc-p" id="ap3" hidden>
        <label for="fFrom">Year from</label><select id="fFrom"></select>
        <label for="fTo">Year to</label><select id="fTo"></select>
        <label for="fSdg">SDG</label><select id="fSdg"></select>
        <div class="hint">year = year of the document's date</div>
      </div>
    </div>
  </aside>
  <main>
    <section role="tabpanel" id="p0" aria-labelledby="t0">
      <h2>Overview</h2><p class="q">What has the UN said, how much, and when?</p>
      <div id="ovBody"></div>
    </section>
    <section role="tabpanel" id="p1" aria-labelledby="t1" hidden>
      <h2>Records</h2><p class="q">Which paragraph says it, and in which UN document?</p>
      <div class="searchbar"><label class="mono" for="kw2" id="kw2lbl">Search</label>
        <input type="search" id="kw2" autocomplete="off"><div class="hint">literal match, not synonyms · click a row to open it</div></div>
      <table id="recTable">
        <caption id="recCap"></caption>
        <thead><tr>
          <th scope="col" id="thDate" aria-sort="descending"><button class="thbtn" id="dateSort" title="Reverse the order">Date ▼</button></th>
          <th scope="col">Body</th><th scope="col">Symbol</th><th scope="col" class="num">Para.</th>
          <th scope="col">Recommending State (UPR)</th><th scope="col">First line</th></tr></thead>
        <tbody id="recBody"></tbody>
      </table>
      <div class="btnrow"><button class="btnb" id="moreBtn" hidden>Show 50 more</button></div>
      <div class="src" id="recSrc"></div>
    </section>
    <section role="tabpanel" id="p2" aria-labelledby="t2" hidden>
      <h2>Check</h2><p class="q">Can I trust these numbers?</p>
      <h3 class="mono" style="margin-bottom:0">Check this dashboard · how the app checks itself</h3>
      <ul class="plain" id="checks"></ul>
      <h3 class="mono" style="margin:28px 0 0">Random-sample label check</h3>
      <p class="how" style="margin-bottom:6px">This is your judgement of the UN's labels; nothing is sent anywhere.</p>
      <div class="btnrow">
        <label class="mono" for="seed">Seed</label><input type="number" class="seed" id="seed" value="1" min="0" step="1">
        <button class="btnb" id="drawBtn">Check 10 at random</button>
        <button class="btnb" id="againBtn" hidden>Draw again</button>
        <button class="btnb" id="seedBtn" hidden>Draw with this seed</button>
      </div>
      <div class="tally" id="tally" aria-live="polite" hidden></div>
      <div id="staleNote" class="hint" hidden>The filters changed after this draw: draw again to sample the current filter.</div>
      <div id="cards"></div>
    </section>
    <section role="tabpanel" id="p3" aria-labelledby="t3" hidden class="method">
      <h2>Method &amp; export</h2><p class="q">How was this made, and how do I take it with me?</p>
      <div id="methodText"></div>
      <div class="btnrow">
        <button class="btnb" id="csvBtn">Download CSV of the current filter</button>
        <button class="btnb" id="sumBtn">Copy summary</button>
        <span id="expStatus" class="hint" role="status"></span>
      </div>
      <div id="dataInfo" class="how"></div>
    </section>
  </main>
</div>
<footer id="foot"></footer>
</div>
<script>
(function(){
"use strict";
const U=(window.WORKSHOP_DATA&&WORKSHOP_DATA.uhri)||{};
const R=Array.isArray(U.records)?U.records:[];
const country=U.country||'this country';
const SDGN=U.sdg_names||{};
const $=(s,el)=>(el||document).querySelector(s);
const $$=(s,el)=>Array.from((el||document).querySelectorAll(s));
const esc=s=>String(s==null?'':s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const fmt=n=>Number(n).toLocaleString('en-GB');
const arr=x=>Array.isArray(x)?x:[];
const safeUrl=u=>/^https?:\/\//i.test(u||'')?u:'#';
const pct=(n,d)=>d?(100*n/d).toFixed(1)+'%':'–';
const MC={'Universal Periodic Review':'#c2410c','Treaty bodies':'#0f766e','Special Procedures':'#7c3aed'};
const mcol=m=>MC[m]||'#6b6559';
const UPR='Universal Periodic Review';
const PARA_RE=/^(\d{1,3}(?:\.\d{1,3})?)\.?\s/;
const STATE_TAIL=/((?:\s*\((?:[^()]|\([^()]*\))*\))+)\s*[;.]?\s*$/;
const STATE_GROUP=/\((?:[^()]|\([^()]*\))*\)/g;

/* ---------- prepare records ---------- */
function firstLine(t){t=String(t).replace(/\s+/g,' ').trim();if(t.length<=120)return t;let c=t.slice(0,120);const sp=c.lastIndexOf(' ');if(sp>40)c=c.slice(0,sp);return c.replace(/[\s,;:.]+$/,'')+'…';}
function extractStates(r){
  if(r.mechanism!==UPR)return null;
  const m=STATE_TAIL.exec(r.text||'');if(!m)return [];
  const gs=m[1].match(STATE_GROUP)||[];const out=[];
  gs.forEach(g=>{const s=g.slice(1,-1).replace(/\s+/g,' ').trim();if(s&&s.indexOf(',')<0&&s.length<=60&&out.indexOf(s)<0)out.push(s);});
  return out;
}
R.forEach((r,i)=>{
  r._i=i;r.text=String(r.text==null?'':r.text);
  r._themes=arr(r.themes);r._sdgs=arr(r.sdgs).map(Number);r._aff=arr(r.affected_persons);
  const m=PARA_RE.exec(r.text);r._para=m?m[1]:'';
  const pp=r._para.split('.');r._p1=m?Number(pp[0]):Infinity;r._p2=pp.length>1?Number(pp[1]):0;
  r._first=firstLine(r.text);r._states=extractStates(r);
  r._lc=(r.text+'\n'+(r.symbol||'')).toLowerCase();
  r._date=String(r.date||'');r._body=String(r.body||'');
});
const N=R.length;
function countBy(rows,f){const m=new Map();rows.forEach(r=>{const k=f(r);m.set(k,(m.get(k)||0)+1)});return m;}
const sortedKeys=m=>Array.from(m.entries()).sort((a,b)=>b[1]-a[1]||String(a[0]).localeCompare(String(b[0]))).map(e=>e[0]);
const ALL={
  mechs:sortedKeys(countBy(R,r=>r.mechanism)),
  types:sortedKeys(countBy(R,r=>r.type)),
  years:Array.from(new Set(R.map(r=>r.year).filter(Number.isFinite))).sort((a,b)=>a-b),
  docs:new Set(R.map(r=>r.symbol)).size
};
const y0=ALL.years.length?ALL.years[0]:null,y1=ALL.years.length?ALL.years[ALL.years.length-1]:null;
const yrs=(a,b)=>a==null?'–':(a===b?String(a):a+'–'+b);
const stateCount=new Map();
R.forEach(r=>{if(r._states)r._states.forEach(s=>stateCount.set(s,(stateCount.get(s)||0)+1));});

/* ---------- state ---------- */
const F={kw:'',mech:'',body:'',type:'',state:'',yFrom:'',yTo:'',sdg:'',themes:[]};
let filtered=R.slice(),curTab=0,curTop=[],words=[],sortDir=-1,sorted=[],shown=0,showStates=false;
const charts={};
let sample={seed:1,ids:[],verdicts:{},open:-1,fkey:null,drawn:false};

/* ---------- header, footer ---------- */
$('#hLabel').textContent='UHRI · '+country;
$('#hTitle').textContent='UN human rights recommendations and observations: '+country;
const srcLink=U.source?(U.source_url?`<a href="${esc(safeUrl(U.source_url))}" target="_blank" rel="noopener">${esc(U.source)}</a>`:esc(U.source)):'source not stated in the file';
$('#hLine').innerHTML=`Source: ${srcLink} · ${fmt(N)} records · ${fmt(ALL.docs)} documents · ${yrs(y0,y1)}${U.built?' · built '+esc(U.built):''} · dated by document`;
$('#foot').innerHTML=`Built on OHCHR UHRI data · ${fmt(N)} records · ${U.source_url?`<a href="${esc(safeUrl(U.source_url))}" target="_blank" rel="noopener">source</a>`:'source link not in the file'}`;
$('#kw2lbl').textContent=`Search ${fmt(N)} records, e.g. torture`;
$('#kw2').placeholder='e.g. torture';

/* ---------- filters ---------- */
function applyFilters(){
  return R.filter(r=>{
    if(F.mech&&r.mechanism!==F.mech)return false;
    if(F.body&&r.body!==F.body)return false;
    if(F.type&&r.type!==F.type)return false;
    if(F.state&&!(r._states&&r._states.indexOf(F.state)>=0))return false;
    if(F.yFrom!==''||F.yTo!==''){
      if(!Number.isFinite(r.year))return false;
      if(F.yFrom!==''&&r.year<F.yFrom)return false;
      if(F.yTo!==''&&r.year>F.yTo)return false;
    }
    if(F.sdg!==''&&r._sdgs.indexOf(Number(F.sdg))<0)return false;
    for(const t of F.themes)if(r._themes.indexOf(t)<0)return false;
    for(const w of words)if(r._lc.indexOf(w)<0)return false;
    return true;
  });
}
function chipList(){
  const c=[];
  if(F.kw.trim())c.push(['kw','Keyword: “'+F.kw.trim()+'”']);
  if(F.mech)c.push(['mech','Mechanism: '+F.mech]);
  if(F.body)c.push(['body','Body: '+F.body]);
  if(F.type)c.push(['type','Type: '+F.type]);
  if(F.state)c.push(['state','State: '+F.state]);
  if(F.yFrom!==''||F.yTo!=='')c.push(['years','Years: '+(F.yFrom!==''?F.yFrom:'earliest')+'–'+(F.yTo!==''?F.yTo:'latest')]);
  if(F.sdg!=='')c.push(['sdg','SDG '+F.sdg]);
  F.themes.forEach(t=>c.push(['theme','Theme: '+t,t]));
  return c;
}
function describeFilters(){const c=chipList();return c.length?c.map(x=>x[1]).join('; '):'none (all records)';}
function fillSelect(el,opts,first){el.innerHTML=(first!=null?`<option value="">${esc(first)}</option>`:'')+opts.map(o=>`<option value="${esc(o.v)}">${esc(o.l)}</option>`).join('');}
function fillBody(){
  const rows=F.mech?R.filter(r=>r.mechanism===F.mech):R;
  const m=countBy(rows,r=>r.body);
  fillSelect($('#fBody'),sortedKeys(m).map(b=>({v:b,l:`${b} (${fmt(m.get(b))})`})),'All');
}
function initControls(){
  const mm=countBy(R,r=>r.mechanism),tm=countBy(R,r=>r.type);
  fillSelect($('#fMech'),ALL.mechs.map(x=>({v:x,l:`${x} (${fmt(mm.get(x))})`})),'All');
  fillSelect($('#fType'),ALL.types.map(x=>({v:x,l:`${x} (${fmt(tm.get(x))})`})),'All');
  fillBody();
  const sk=sortedKeys(stateCount);
  if(sk.length){$('#stateWrap').hidden=false;fillSelect($('#fState'),sk.map(s=>({v:s,l:`${s} (${fmt(stateCount.get(s))})`})),'All');}
  fillSelect($('#fFrom'),ALL.years.map(y=>({v:y,l:y})),'earliest');
  fillSelect($('#fTo'),ALL.years.map(y=>({v:y,l:y})),'latest');
  const sg=new Map();R.forEach(r=>new Set(r._sdgs).forEach(g=>sg.set(g,(sg.get(g)||0)+1)));
  fillSelect($('#fSdg'),Array.from(sg.keys()).sort((a,b)=>a-b).map(g=>({v:g,l:`${g} · ${SDGN[g]||'goal '+g} (${fmt(sg.get(g))})`})),'All');
}
function syncControls(){
  $('#kw1').value=F.kw;$('#kw2').value=F.kw;
  $('#fMech').value=F.mech;fillBody();$('#fBody').value=F.body;
  $('#fType').value=F.type;$('#fState').value=F.state;
  $('#fFrom').value=F.yFrom;$('#fTo').value=F.yTo;$('#fSdg').value=F.sdg;
}
let kwTimer=null;
function onKw(e){
  const v=e.target.value;F.kw=v;
  (e.target.id==='kw1'?$('#kw2'):$('#kw1')).value=v;
  clearTimeout(kwTimer);kwTimer=setTimeout(update,300);
}
$('#kw1').addEventListener('input',onKw);$('#kw2').addEventListener('input',onKw);
$('#fMech').addEventListener('change',e=>{F.mech=e.target.value;F.body='';fillBody();update();});
$('#fBody').addEventListener('change',e=>{F.body=e.target.value;update();});
$('#fType').addEventListener('change',e=>{F.type=e.target.value;update();});
$('#fState').addEventListener('change',e=>{F.state=e.target.value;update();});
$('#fSdg').addEventListener('change',e=>{F.sdg=e.target.value;update();});
function onYear(){
  F.yFrom=$('#fFrom').value===''?'':Number($('#fFrom').value);
  F.yTo=$('#fTo').value===''?'':Number($('#fTo').value);
  if(F.yFrom!==''&&F.yTo!==''&&F.yFrom>F.yTo){const t=F.yFrom;F.yFrom=F.yTo;F.yTo=t;}
  $('#fFrom').value=F.yFrom;$('#fTo').value=F.yTo;update();
}
$('#fFrom').addEventListener('change',onYear);$('#fTo').addEventListener('change',onYear);
$('#clearAll').addEventListener('click',()=>{Object.assign(F,{kw:'',mech:'',body:'',type:'',state:'',yFrom:'',yTo:'',sdg:'',themes:[]});syncControls();update();});
$('#chips').addEventListener('click',e=>{
  const b=e.target.closest('button[data-k]');if(!b)return;
  const k=b.dataset.k;
  if(k==='kw')F.kw='';else if(k==='mech'){F.mech='';F.body='';}else if(k==='body')F.body='';
  else if(k==='type')F.type='';else if(k==='state')F.state='';else if(k==='years'){F.yFrom='';F.yTo='';}
  else if(k==='sdg')F.sdg='';else if(k==='theme')F.themes=F.themes.filter(t=>t!==b.dataset.t);
  syncControls();update();
});
const heads=$$('.acc-h');
heads.forEach(b=>b.addEventListener('click',()=>{
  const open=b.getAttribute('aria-expanded')==='true';
  heads.forEach(h=>{h.setAttribute('aria-expanded','false');$('#'+h.getAttribute('aria-controls')).hidden=true;});
  if(!open){b.setAttribute('aria-expanded','true');$('#'+b.getAttribute('aria-controls')).hidden=false;}
}));
function addTheme(t){if(t&&F.themes.indexOf(t)<0){F.themes.push(t);update();}}

/* ---------- stats ---------- */
function themeTop(rows){
  const m=new Map();
  rows.forEach(r=>{new Set(r._themes).forEach(t=>{
    let o=m.get(t);if(!o){o={t,n:0,a:Infinity,b:-Infinity};m.set(t,o);}
    o.n++;if(Number.isFinite(r.year)){if(r.year<o.a)o.a=r.year;if(r.year>o.b)o.b=r.year;}
  });});
  return Array.from(m.values()).sort((a,b)=>b.n-a.n||a.t.localeCompare(b.t)).slice(0,10);
}
function themeTopCheck(rows){
  const c=Object.create(null);
  for(const r of rows){const seen=Object.create(null);for(const t of r._themes){if(!seen[t]){seen[t]=1;c[t]=(c[t]||0)+1;}}}
  return Object.keys(c).map(k=>[k,c[k]]).sort((a,b)=>b[1]-a[1]||(a[0]<b[0]?-1:1)).slice(0,10);
}
function typeLine(rows){
  const m=countBy(rows,r=>r.type);
  const ks=sortedKeys(m);
  return ks.length?ks.map(k=>`${esc(k)} ${fmt(m.get(k))}`).join(' · '):'—';
}
function topStates(rows){
  const m=new Map();
  rows.forEach(r=>{if(r._states)r._states.forEach(s=>m.set(s,(m.get(s)||0)+1));});
  return Array.from(m.entries()).sort((a,b)=>b[1]-a[1]||a[0].localeCompare(b[0])).slice(0,10);
}
function hl(text){
  if(!words.length)return esc(text);
  const ws=words.slice().sort((a,b)=>b.length-a.length).map(x=>x.replace(/[.*+?^${}()|[\]\\]/g,'\\$&'));
  const re=new RegExp(ws.join('|'),'gi');let out='',last=0,m;
  while((m=re.exec(text))){if(m[0]===''){re.lastIndex++;continue;}out+=esc(text.slice(last,m.index))+'<mark>'+esc(m[0])+'</mark>';last=m.index+m[0].length;}
  return out+esc(text.slice(last));
}
const cite=r=>r._para?`${r.symbol}, para. ${r._para}`:String(r.symbol||'');
async function copyText(t){
  try{await navigator.clipboard.writeText(t);return true;}catch(e){}
  try{const ta=document.createElement('textarea');ta.value=t;ta.style.position='fixed';ta.style.opacity='0';document.body.appendChild(ta);ta.select();const ok=document.execCommand('copy');ta.remove();return ok;}catch(e){return false;}
}
function flash(el,ok){if(!el)return;el.textContent=ok?'Copied':'Copy not allowed here';setTimeout(()=>{el.textContent='';},2000);}
const srcNote=()=>`Source: ${esc(U.source||'OHCHR UHRI')}${U.built?', built '+esc(U.built):''}.`;

/* ---------- rail ---------- */
function renderRail(){
  const n=filtered.length;
  $('#cnt').textContent=fmt(n);
  $('#cntLbl').textContent=n===1?'matching record':'matching records';
  $('#cntOf').textContent=`of ${fmt(N)} in the file`;
  $('#barFill').style.width=(N?100*n/N:0)+'%';
  $('#chips').innerHTML=chipList().map(c=>`<button class="chip" data-k="${c[0]}"${c[2]!=null?` data-t="${esc(c[2])}"`:''} title="Remove this filter">${esc(c[1])} ✕</button>`).join('');
}

/* ---------- tab 01 overview ---------- */
function wrapLabel(s,w){const out=[];let cur='';String(s).split(' ').forEach(x=>{if(cur&&(cur+' '+x).length>w){out.push(cur);cur=x;}else cur=(cur?cur+' ':'')+x;});if(cur)out.push(cur);return out;}
const valueLabels={id:'valueLabels',afterDatasetsDraw(ch){
  const m=ch.getDatasetMeta(0);const ctx=ch.ctx;ctx.save();ctx.fillStyle='#1d1b18';ctx.font='13px ui-monospace,Menlo,Consolas,monospace';ctx.textBaseline='middle';
  m.data.forEach((bar,i)=>{ctx.fillText(fmt(ch.data.datasets[0].data[i]),bar.x+6,bar.y);});ctx.restore();}};
function renderOverview(){
  const rows=filtered,n=rows.length;
  Object.keys(charts).forEach(k=>{if(charts[k]){charts[k].destroy();charts[k]=null;}});
  const ys=rows.map(r=>r.year).filter(Number.isFinite);
  const a=ys.length?Math.min.apply(null,ys):null,b=ys.length?Math.max.apply(null,ys):null;
  const docs=new Set(rows.map(r=>r.symbol)).size;
  let h=`<div class="tiles">
   <div class="tile"><div class="mono">Records</div><div class="big">${fmt(n)}</div><div class="sub">${typeLine(rows)}</div></div>
   <div class="tile"><div class="mono">Documents</div><div class="big">${fmt(docs)}</div><div class="sub">distinct UN symbols</div></div>
   <div class="tile"><div class="mono">Years</div><div class="big">${yrs(a,b)}</div><div class="sub">first–last document year</div></div></div>
   <p class="how"><b>How this is computed</b>Records = every paragraph in the filtered set, split by <em>type</em> exactly as spelled in the data; documents = distinct symbols; years = min–max of <em>year</em>.</p>
   <div class="mono">By mechanism</div><div class="tiles">`;
  ALL.mechs.forEach(m=>{
    const mr=rows.filter(r=>r.mechanism===m);
    const my=mr.map(r=>r.year).filter(Number.isFinite);
    h+=`<div class="tile"><div class="mono"><span class="dot" style="background:${mcol(m)}"></span>${esc(m)}</div><div class="big">${fmt(mr.length)}</div>
      <div class="sub">${fmt(new Set(mr.map(r=>r.symbol)).size)} documents · latest ${my.length?Math.max.apply(null,my):'–'} · ${pct(mr.length,n)} of filtered</div>
      ${m===UPR&&stateCount.size?`<button class="link" id="statesBtn" aria-expanded="${showStates}">${showStates?'hide the States':'see the States'}</button>`:''}</div>`;
  });
  h+=`</div><p class="how"><b>How this is computed</b>Each tile counts the filtered records with that <em>mechanism</em>; share = tile ÷ filtered records.</p>`;
  if(showStates){
    const ts=topStates(rows);
    h+=`<div style="border-top:1px solid var(--rule);padding-top:10px"><span class="t" style="font:400 20px var(--serif)">Ten States that made most recommendations to ${esc(country)}</span>
    ${ts.length?`<table><caption>Current filter · UPR records only</caption><thead><tr><th scope="col">State</th><th scope="col" class="num">Recommendations</th></tr></thead><tbody>${ts.map(s=>`<tr><td>${esc(s[0])}</td><td class="num">${fmt(s[1])}</td></tr>`).join('')}</tbody></table>`:'<p class="dim">No State found in the filtered records.</p>'}
    <p class="how"><b>How this is computed</b>The State is read from the parentheses at the end of each UPR text; a line with several States counts once for each, so this counts lines, not influence.</p></div>`;
  }
  if(!n){h+=`<div class="empty">No records match the current filters.</div>`;$('#ovBody').innerHTML=h;return;}
  curTop=themeTop(rows);
  h+=`<figure><figcaption><span class="mono">FIG.01</span><span class="t">Ten most frequent themes among ${fmt(n)} filtered records</span></figcaption>`;
  if(!curTop.length)h+=`<div class="empty">No theme labels in these records (not labelled).</div>`;
  else{
    h+=`<div class="chartbox" style="height:${Math.max(260,curTop.length*40+30)}px"><canvas id="c1" role="img" aria-label="Horizontal bar chart of the ten most frequent themes; the same numbers are in the table below"></canvas></div>
    <div class="hint">click a bar (or a theme name below) = add it as a filter</div>
    <table id="themeTable" style="margin-top:10px"><caption>The same ten themes as a table</caption><thead><tr><th scope="col">Theme</th><th scope="col" class="num">Records</th><th scope="col" class="num">% of filtered</th><th scope="col">Years</th></tr></thead><tbody>
    ${curTop.map((o,i)=>`<tr><td><button class="tbtn" data-t="${i}">${esc(o.t)}</button></td><td class="num">${fmt(o.n)}</td><td class="num">${pct(o.n,n)}</td><td class="nw">${yrs(o.a===Infinity?null:o.a,o.b)}</td></tr>`).join('')}</tbody></table>`;
  }
  h+=`<p class="how"><b>How this is computed</b>Each theme counts once per record that carries it; a record can carry several themes, so the bars add up to more than ${fmt(n)}. Years = first–last year of the records with that theme: an old-only range can point to a legacy label, so check a sample on tab 03.</p>
  <div class="src">${srcNote()} n = ${fmt(n)} filtered records.</div></figure>`;
  const tl=timeline(rows);
  h+=`<figure><figcaption><span class="mono">FIG.02</span><span class="t">Records per year by mechanism, ${fmt(n)} filtered records</span></figcaption>
   <div class="chartbox" style="height:320px"><canvas id="c2" role="img" aria-label="Stacked bars of records per year by mechanism"></canvas></div>
   <p class="how"><b>How this is computed</b>Records of the filtered set counted per <em>year</em> and <em>mechanism</em>; every year from ${tl.labels[0]} to ${tl.labels[tl.labels.length-1]} is shown, so a year with no records is a gap.</p>
   <details><summary>Table of FIG.02</summary><table><caption>Records per year and mechanism</caption><thead><tr><th scope="col">Year</th>${tl.ds.map(d=>`<th scope="col" class="num">${esc(d.m)}</th>`).join('')}<th scope="col" class="num">Total</th></tr></thead><tbody>
   ${tl.labels.map((y,i)=>`<tr><td>${y}</td>${tl.ds.map(d=>`<td class="num">${fmt(d.data[i])}</td>`).join('')}<td class="num">${fmt(tl.ds.reduce((s,d)=>s+d.data[i],0))}</td></tr>`).join('')}</tbody></table></details>
   <div class="src">${srcNote()} Dated by document.</div></figure>`;
  $('#ovBody').innerHTML=h;
  if(typeof Chart==='undefined')return;
  if(curTop.length){
    charts.c1=new Chart($('#c1'),{type:'bar',plugins:[valueLabels],
      data:{labels:curTop.map(o=>wrapLabel(o.t,36)),datasets:[{data:curTop.map(o=>o.n),backgroundColor:'rgba(155,35,53,.8)',borderWidth:0,barPercentage:.75}]},
      options:{indexAxis:'y',responsive:true,maintainAspectRatio:false,animation:false,
        plugins:{legend:{display:false},tooltip:{callbacks:{title:i=>curTop[i[0].dataIndex].t,label:c=>fmt(c.parsed.x)+' records'}}},
        scales:{x:{display:false,beginAtZero:true,grace:'12%'},y:{grid:{display:false},ticks:{color:'#1d1b18',font:{size:12}}}},
        onClick:(ev,els)=>{if(els.length)addTheme(curTop[els[0].index].t);},
        onHover:(ev,els)=>{if(ev.native&&ev.native.target)ev.native.target.style.cursor=els.length?'pointer':'default';}}});
  }
  charts.c2=new Chart($('#c2'),{type:'bar',
    data:{labels:tl.labels.map(String),datasets:tl.ds.map(d=>({label:d.m,data:d.data,backgroundColor:mcol(d.m),borderWidth:0}))},
    options:{responsive:true,maintainAspectRatio:false,animation:false,
      plugins:{legend:{position:'top',labels:{boxWidth:12,font:{size:12},color:'#1d1b18'}}},
      scales:{x:{stacked:true,grid:{display:false},ticks:{maxRotation:0,autoSkip:true,color:'#1d1b18'}},y:{stacked:true,beginAtZero:true,ticks:{precision:0,color:'#1d1b18'},grid:{color:'#e6e0d2'}}}}});
}
function timeline(rows){
  const ys=rows.map(r=>r.year).filter(Number.isFinite);
  const a=Math.min.apply(null,ys),b=Math.max.apply(null,ys);const labels=[];for(let y=a;y<=b;y++)labels.push(y);
  const cnt=new Map();rows.forEach(r=>{const k=r.mechanism+'|'+r.year;cnt.set(k,(cnt.get(k)||0)+1);});
  const ds=ALL.mechs.map(m=>({m,data:labels.map(y=>cnt.get(m+'|'+y)||0)})).filter(d=>d.data.some(v=>v>0));
  return {labels:labels.length?labels:[0],ds};
}
$('#ovBody').addEventListener('click',e=>{
  const t=e.target.closest('button[data-t]');if(t){addTheme((curTop[Number(t.dataset.t)]||{}).t);return;}
  if(e.target.closest('#statesBtn')){showStates=!showStates;renderOverview();const b=$('#statesBtn');if(b)b.focus();}
});

/* ---------- tab 02 records ---------- */
function sortRows(){
  sorted=filtered.slice().sort((a,b)=>{
    if(a._date!==b._date)return (a._date<b._date?-1:1)*sortDir*-1*-1;
    const bc=a._body.localeCompare(b._body);if(bc)return bc;
    if(a._p1!==b._p1)return a._p1<b._p1?-1:1;
    if(a._p2!==b._p2)return a._p2-b._p2;
    return a._i-b._i;
  });
}
function rowHTML(r){
  const st=r._states===null?'<span class="dim">—</span>':(r._states.length?esc(r._states.join('; ')):'<span class="dim">State not found</span>');
  return `<tr class="main" tabindex="0" aria-expanded="false" data-i="${r._i}"><td class="nw">${esc(r._date)}</td><td>${esc(r.body)}</td>
   <td class="nw"><a href="${esc(safeUrl(r.doc_url))}" target="_blank" rel="noopener">${hl(String(r.symbol||''))}</a></td>
   <td class="num">${r._para?esc(r._para):'–'}</td><td>${st}</td><td>${hl(r._first)}</td></tr><tr class="detail" hidden data-for="${r._i}"><td colspan="6"></td></tr>`;
}
function recCaption(){
  const n=filtered.length;
  $('#recCap').textContent=n?`Showing ${fmt(Math.min(shown,n))} of ${fmt(n)} matching records, ${sortDir===-1?'newest':'oldest'} first`:'No records match the current filters.';
  $('#moreBtn').hidden=!(n>shown);
}
function renderRecords(){
  sortRows();shown=Math.min(50,sorted.length);
  $('#recBody').innerHTML=sorted.slice(0,shown).map(rowHTML).join('');
  $('#dateSort').textContent='Date '+(sortDir===-1?'▼':'▲');
  $('#thDate').setAttribute('aria-sort',sortDir===-1?'descending':'ascending');
  recCaption();
  $('#recSrc').innerHTML=`${srcNote()} Each row is one paragraph; symbols link to the UN document. Date = date of the document. Sorted by date, then body, then paragraph number.`;
}
$('#dateSort').addEventListener('click',()=>{sortDir=-sortDir;renderRecords();});
$('#moreBtn').addEventListener('click',()=>{
  const next=sorted.slice(shown,shown+50);shown+=next.length;
  $('#recBody').insertAdjacentHTML('beforeend',next.map(rowHTML).join(''));recCaption();
});
function detailHTML(r){
  const lab=(name,items)=>`<div class="lab"><span class="mono">${name}</span>${items.length?items.map(x=>`<span class="tag">${esc(x)}</span>`).join(''):'<span class="dim">not labelled</span>'}</div>`;
  const sd=r._sdgs.map(g=>'SDG '+g+(SDGN[g]?' · '+SDGN[g]:''));
  const cl='Copy citation'+(r._para?'':' (no paragraph number in this extract)');
  return `<div class="det"><div class="bigpara" aria-label="Paragraph ${esc(r._para||'unknown')}">${r._para?esc(r._para):'—'}</div><div class="detmain">
   <div class="mono">${esc(r.symbol)} · ${esc(r.body)} · ${esc(r.type)}</div>
   <div class="fulltext">${hl(r.text)}</div>
   ${r.section?`<div class="lab"><span class="mono">Section</span>${esc(r.section)}</div>`:''}
   ${lab('Themes',r._themes)}${lab('SDGs',sd)}${lab('SDG targets',arr(r.sdg_targets))}${lab('Affected persons',r._aff)}
   ${r._states&&r._states.length?`<div class="lab"><span class="mono">Recommending State</span>${esc(r._states.join('; '))}</div>`:''}
   <div class="acts"><button data-copy="${r._i}">${cl}</button><span class="hint" role="status"></span>
   <a class="btn" href="${esc(safeUrl(r.doc_url))}" target="_blank" rel="noopener">Open the UN document</a></div></div></div>`;
}
function toggleRow(tr){
  const open=tr.getAttribute('aria-expanded')==='true';const d=tr.nextElementSibling;
  if(!open&&!d.dataset.filled){d.firstElementChild.innerHTML=detailHTML(R[Number(tr.dataset.i)]);d.dataset.filled='1';}
  tr.setAttribute('aria-expanded',String(!open));d.hidden=open;
}
$('#recBody').addEventListener('click',async e=>{
  const cb=e.target.closest('[data-copy]');
  if(cb){const r=R[Number(cb.dataset.copy)];flash(cb.nextElementSibling,await copyText(cite(r)));return;}
  if(e.target.closest('a'))return;
  const tr=e.target.closest('tr.main');if(tr)toggleRow(tr);
});
$('#recBody').addEventListener('keydown',e=>{
  if((e.key==='Enter'||e.key===' ')&&e.target.matches('tr.main')){e.preventDefault();toggleRow(e.target);}
});

/* ---------- tab 03 check ---------- */
function ck(status,what,vals,extra){
  const t=status==='ok'?'✓ pass':status==='warn'?'! warning':status==='fail'?'✗ check failed':'· info';
  return `<li class="chk ${status}"><span class="mark">${t}</span><span class="what">${what}</span><span class="vals">${vals}${extra||''}</span></li>`;
}
const more=(list,fn,n)=>list.slice(0,n||15).map(fn).join('')+(list.length>(n||15)?`<li>… and ${fmt(list.length-(n||15))} more</li>`:'');
function renderCheck(){
  const L=[],rows=filtered,n=rows.length;
  const cnt=Number(U.count);
  L.push(ck(N===cnt?'ok':'fail','Record count: records in the file against the declared count',`${fmt(N)} vs ${isNaN(cnt)?'not declared':fmt(cnt)}${typeof U.count==='string'?` (stored as text “${esc(U.count)}”, compared as a number)`:''}`));
  const part=(label,vals,f)=>{let s=0;vals.forEach(v=>{s+=R.filter(r=>f(r)===v).length;});L.push(ck(s===N?'ok':'fail',`Partition: ${label} add up to the record count`,`${fmt(s)} vs ${fmt(N)} (${fmt(vals.length)} values)`));};
  part('records per mechanism',ALL.mechs,r=>r.mechanism);
  part('records per body',Array.from(new Set(R.map(r=>r.body))),r=>r.body);
  part('records per year',ALL.years,r=>r.year);
  let ts=0;ALL.types.forEach(t=>{ts+=rows.filter(r=>r.type===t).length;});
  L.push(ck(ts===n?'ok':'fail','Type partition: records per type add up to the headline total (current filter)',`${fmt(ts)} vs ${fmt(n)}`));
  const A=curTopNow(rows),B=themeTopCheck(rows);
  const same=A.length===B.length&&A.every((o,i)=>o.t===B[i][0]&&o.n===B[i][1]);
  L.push(ck(same?'ok':'fail','FIG.01 bars against a second count made by a separate loop',same?`${A.length} bars match`:`bars ${esc(A.map(o=>o.n).join(','))} vs recount ${esc(B.map(o=>o[1]).join(','))}`));
  const mx=A.length?A[0].n:0;
  L.push(ck(mx<=n?'ok':'fail','FIG.01 largest bar is not larger than the filtered count',`${fmt(mx)} vs ${fmt(n)}`));
  L.push(ck('ok','FIG.01 table rows show the same ten values as the bars',`${A.length} rows built from the same list`));
  const badLinks=R.filter(r=>{let u=String(r.doc_url||'');try{u=decodeURIComponent(u);}catch(e){}return !(u.indexOf('https://docs.un.org/')===0&&u.toLowerCase().endsWith(String(r.symbol||'').toLowerCase()));});
  L.push(ck(badLinks.length?'fail':'ok','Links: every doc_url starts with https://docs.un.org/ and ends with its symbol',`${fmt(N-badLinks.length)} of ${fmt(N)} pass`,
    badLinks.length?`<details><summary>Show the ${fmt(badLinks.length)} that fail</summary><ul>${more(badLinks,r=>`<li>${esc(r.symbol)} → ${esc(r.doc_url)}</li>`)}</ul></details>`:''));
  const pm=ALL.mechs.map(m=>{const mr=R.filter(r=>r.mechanism===m);const k=mr.filter(r=>r._para).length;return {m,k,n:mr.length};});
  const upr=pm.find(x=>x.m===UPR);
  L.push(ck(!upr||upr.k===upr.n?'ok':'warn','Paragraph numbers found at the start of the text, per mechanism (UPR expected 100%)',pm.map(x=>`${esc(x.m)} ${pct(x.k,x.n)} (${fmt(x.k)}/${fmt(x.n)})`).join(' · ')));
  const uprRows=R.filter(r=>r._states!==null),noSt=uprRows.filter(r=>!r._states.length);
  if(uprRows.length)L.push(ck(noSt.length?'warn':'ok','States found: UPR records with at least one recommending State',`${fmt(uprRows.length-noSt.length)} of ${fmt(uprRows.length)}`,
    noSt.length?`<details><summary>Show the ${fmt(noSt.length)} without a State</summary><ul>${more(noSt,r=>`<li>${esc(r.symbol)} · para. ${esc(r._para||'?')} · ends: “${esc(r.text.slice(-70))}”</li>`)}</ul></details>`:''));
  else L.push(ck('info','States found','no UPR records in this file'));
  const ids=new Set(R.map(r=>r.id)).size;
  L.push(ck(ids===N?'ok':'fail','Distinct id against the record count',`${fmt(ids)} vs ${fmt(N)}`));
  const tm=new Map();R.forEach(r=>{const k=r.text;(tm.get(k)||tm.set(k,[]).get(k)).push(r);});
  const dups=Array.from(tm.values()).filter(v=>v.length>1);
  L.push(ck(dups.length?'warn':'ok','Duplicate texts: text values that occur more than once',`${fmt(dups.length)} text value(s), ${fmt(dups.reduce((s,v)=>s+v.length-1,0))} extra record(s)`,
    dups.length?`<details><summary>Show them</summary><ul>${more(dups,v=>`<li>${esc(v.map(r=>r.symbol+(r._para?' para. '+r._para:'')).join(' = '))}: “${esc(v[0]._first)}”</li>`)}</ul></details>`:''));
  [['themes',r=>!r._themes.length],['SDGs',r=>!r._sdgs.length],['affected persons',r=>!r._aff.length]].forEach(x=>{
    const k=R.filter(x[1]).length;L.push(ck('info',`Records with no ${x[0]}`,`${fmt(k)} of ${fmt(N)} (${pct(k,N)}) not labelled`));});
  $('#checks').innerHTML=L.join('');
  renderSample();
}
function curTopNow(rows){return themeTop(rows);}
function mulberry32(a){return function(){a|=0;a=a+0x6D2B79F5|0;let t=Math.imul(a^a>>>15,1|a);t=t+Math.imul(t^t>>>7,61|t)^t;return((t^t>>>14)>>>0)/4294967296;};}
function draw(seed){
  const rng=mulberry32(seed),pool=filtered.slice(),k=Math.min(10,pool.length);
  for(let i=0;i<k;i++){const j=i+Math.floor(rng()*(pool.length-i));const t=pool[i];pool[i]=pool[j];pool[j]=t;}
  sample={seed,ids:pool.slice(0,k).map(r=>r._i),verdicts:{},open:-1,fkey:JSON.stringify(F),drawn:true};
  $('#seed').value=seed;renderSample();
}
function renderSample(){
  $('#drawBtn').hidden=sample.drawn;$('#againBtn').hidden=!sample.drawn;$('#seedBtn').hidden=!sample.drawn;
  $('#tally').hidden=!sample.drawn;
  $('#staleNote').hidden=!(sample.drawn&&sample.fkey!==JSON.stringify(F));
  if(!sample.drawn){$('#cards').innerHTML=filtered.length?'':'<div class="empty">No records match, nothing to sample.</div>';return;}
  const v=Object.values(sample.verdicts),x=v.filter(a=>a==='fit').length,y=v.filter(a=>a==='no').length,z=v.filter(a=>a==='unsure').length;
  $('#tally').textContent=`Themes: ${x} fit, ${y} don't, ${z} unsure of ${v.length} judged · seed ${sample.seed} · ${sample.ids.length} drawn · your judgement, not the UN's`;
  const VL={fit:'fits',no:"doesn't fit",unsure:'unsure'};
  $('#cards').innerHTML=sample.ids.map((id,i)=>{
    const r=R[id],open=sample.open===i,vd=sample.verdicts[id];
    return `<div class="card"><button aria-expanded="${open}" data-card="${i}"><span class="mono">${String(i+1).padStart(2,'0')}</span><span><b>${esc(r.symbol)}</b>${r._para?' · para. '+esc(r._para):''} · ${esc(r._first.slice(0,70))}${r._first.length>70?'…':''}</span><span class="v">${vd?VL[vd]:'not judged'}</span></button>
    ${open?`<div class="body"><p class="mono"><a href="${esc(safeUrl(r.doc_url))}" target="_blank" rel="noopener">${esc(r.symbol)}</a> · ${r._para?'para. '+esc(r._para):'no paragraph number'} · ${esc(r.body)} · ${esc(r._date)}</p>
    <div class="fulltext">${esc(r.text)}</div>
    <div class="lab"><span class="mono">UN themes</span>${r._themes.length?r._themes.map(t=>`<span class="tag">${esc(t)}</span>`).join(''):'<span class="dim">not labelled</span>'}</div>
    <div class="btnrow"><span class="hint">Do the themes, as a set, fit this paragraph?</span>
    <button class="btnb" data-v="fit" aria-pressed="${vd==='fit'}">Fits</button><button class="btnb" data-v="no" aria-pressed="${vd==='no'}">Doesn't fit</button><button class="btnb" data-v="unsure" aria-pressed="${vd==='unsure'}">Unsure</button></div></div>`:''}</div>`;
  }).join('');
}
$('#cards').addEventListener('click',e=>{
  const vb=e.target.closest('button[data-v]');
  if(vb){sample.verdicts[sample.ids[sample.open]]=vb.dataset.v;renderSample();const b=$('#cards button[data-v="'+vb.dataset.v+'"]');if(b)b.focus();return;}
  const cb=e.target.closest('button[data-card]');
  if(cb){const i=Number(cb.dataset.card);sample.open=sample.open===i?-1:i;renderSample();const b=$('#cards button[data-card="'+i+'"]');if(b)b.focus();}
});
const seedVal=()=>{const s=parseInt($('#seed').value,10);return Number.isFinite(s)?s:1;};
$('#drawBtn').addEventListener('click',()=>draw(seedVal()));
$('#seedBtn').addEventListener('click',()=>draw(seedVal()));
$('#againBtn').addEventListener('click',()=>draw(Math.floor(Math.random()*1000000)));

/* ---------- tab 04 method & export ---------- */
function renderMethod(){
  $('#methodText').innerHTML=`<p>Every number on this page is a count made by a loop over the ${fmt(N)} records in the file; nothing is estimated and no model is called.</p>
  <p>One record is one paragraph of a UN document (a UPR report, treaty-body concluding observations or a Special Procedures report). Documents are distinct symbols; the year is the year of the document's date, not of the event.</p>
  <p>Filters combine with AND, and every tab reads the same filtered set. The keyword filter is literal: every word must appear in the text or symbol, so “torture” does not find “ill-treatment”.</p>
  <p>Themes, SDGs and affected persons are the UN index's own labels; this app never changes them. A record can carry several themes, so theme counts add up to more than the record count, and older records may carry labels that do not fit, which is why tab 03 lets you judge a random sample.</p>
  <p>The paragraph number is read from the start of the text; for UPR it keeps its two-part form (e.g. 144.43). The recommending State is read from the parentheses at the end of a UPR text only; if none is found the row says so.</p>
  <p>A citation is the symbol plus “para.” and the number when one was found. Only the clipboard write on “Copy” leaves the page; the CSV is made in your browser.</p>`;
  $('#dataInfo').innerHTML=`<b>Data</b> ${esc(U.title||'UHRI recommendations')}, ${U.source_url?`<a href="${esc(safeUrl(U.source_url))}" target="_blank" rel="noopener">${esc(U.source||U.source_url)}</a>`:esc(U.source||'OHCHR UHRI')}${U.built?' · built '+esc(U.built):''} · ${fmt(N)} records. The file states no licence: check the terms on the source page before republishing.`;
}
function csvCell(v){return '"'+String(v==null?'':v).replace(/"/g,'""')+'"';}
$('#csvBtn').addEventListener('click',()=>{
  sortRows();
  const cols=['date','body','mechanism','type','symbol','paragraph','recommending_states','section','text','themes','sdgs','sdg_targets','affected_persons','doc_url'];
  const head=[`# Country: ${country}`,`# Source: ${U.source||''} ${U.source_url||''}`,`# Built: ${U.built||''}`,`# Filters: ${describeFilters()}`,`# Rows: ${sorted.length} of ${N}`];
  const lines=sorted.map(r=>[r._date,r.body,r.mechanism,r.type,r.symbol,r._para,r._states?r._states.join(' | '):'',r.section||'',r.text,r._themes.join(' | '),r._sdgs.join(' | '),arr(r.sdg_targets).join(' | '),r._aff.join(' | '),r.doc_url].map(csvCell).join(','));
  const csv='\uFEFF'+head.join('\n')+'\n'+cols.join(',')+'\n'+lines.join('\n')+'\n';
  const url=URL.createObjectURL(new Blob([csv],{type:'text/csv;charset=utf-8'}));
  const a=document.createElement('a');a.href=url;a.download='uhri-'+String(country).toLowerCase().replace(/[^a-z0-9]+/g,'-')+'-filtered.csv';
  document.body.appendChild(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(url),2000);
  $('#expStatus').textContent=`${fmt(sorted.length)} rows prepared`;
});
$('#sumBtn').addEventListener('click',async()=>{
  const rows=filtered,n=rows.length,ys=rows.map(r=>r.year).filter(Number.isFinite);
  const t=themeTop(rows),mm=countBy(rows,r=>r.mechanism);
  const txt=`${country}: UN recommendations and observations (${U.source||'OHCHR UHRI'}${U.built?', built '+U.built:''}).
Filters: ${describeFilters()}.
${fmt(n)} matching records of ${fmt(N)}; ${fmt(new Set(rows.map(r=>r.symbol)).size)} documents; years ${ys.length?yrs(Math.min.apply(null,ys),Math.max.apply(null,ys)):'–'} (dated by document).
By type: ${typeLine(rows).replace(/&amp;/g,'&').replace(/&lt;/g,'<')}.
By mechanism: ${sortedKeys(mm).map(k=>k+' '+fmt(mm.get(k))).join('; ')||'–'}.
Ten most frequent themes (a record can carry several): ${t.map((o,i)=>`${i+1}. ${o.t} ${fmt(o.n)} (${pct(o.n,n)}, ${yrs(o.a===Infinity?null:o.a,o.b)})`).join('; ')||'none'}.
Source: ${U.source_url||U.source||''}`;
  const ok=await copyText(txt);$('#expStatus').textContent=ok?'Summary copied':'Copy not allowed here';setTimeout(()=>{$('#expStatus').textContent='';},2000);
});

/* ---------- tabs and update ---------- */
const tabs=$$('[role=tab]');
function showTab(i){
  curTab=i;
  tabs.forEach((t,j)=>{t.setAttribute('aria-selected',String(j===i));t.tabIndex=j===i?0:-1;$('#'+t.getAttribute('aria-controls')).hidden=j!==i;});
  $('#acc').hidden=i>1;
  renderActive();
}
tabs.forEach((t,i)=>{
  t.addEventListener('click',()=>showTab(i));
  t.addEventListener('keydown',e=>{
    let j=null;if(e.key==='ArrowRight')j=(i+1)%4;else if(e.key==='ArrowLeft')j=(i+3)%4;else if(e.key==='Home')j=0;else if(e.key==='End')j=3;
    if(j!==null){e.preventDefault();showTab(j);tabs[j].focus();}
  });
});
function renderActive(){
  if(curTab===0)renderOverview();else if(curTab===1)renderRecords();else if(curTab===2)renderCheck();else renderMethod();
}
function update(){
  words=F.kw.trim().toLowerCase().split(/\s+/).filter(Boolean);
  filtered=applyFilters();renderRail();renderActive();
}
initControls();syncControls();update();
})();
</script>
</body>
</html>
```