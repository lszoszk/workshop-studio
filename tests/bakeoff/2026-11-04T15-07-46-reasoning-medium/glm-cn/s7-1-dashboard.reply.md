I built the four-tab dashboard for Kenya's UN recommendations: overview with theme and timeline charts, a records table with in-place expansion and citations, a self-check panel with a random label-check, and method plus CSV export. Every number is computed in the browser from the attached file.

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>UN human rights recommendations and observations: Kenya</title>
<style>
:root{--paper:#f4f0e8;--ink:#1d1b18;--rule:#d9d2c3;--accent:#9b2335;--upr:#c2410c;--tb:#0f766e;--sp:#7c3aed}
*{box-sizing:border-box}
[hidden]{display:none!important}
body{margin:0;background:var(--paper);color:var(--ink);font:16px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif}
a{color:var(--accent)}
a:focus,button:focus,input:focus,select:focus,[tabindex]:focus{outline:2px solid var(--accent);outline-offset:2px}
.wrap{max-width:1200px;margin:0 auto;padding:16px 20px 40px}
.mono{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:11px;letter-spacing:.08em;text-transform:uppercase}
header.site{border-bottom:1px solid var(--rule);padding-bottom:12px}
.datalabel{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:12px;letter-spacing:.08em}
h1{font-family:Georgia,"Times New Roman",serif;font-weight:400;font-size:32px;margin:6px 0 4px}
.metaline{font-size:13px;color:#57503f}
.layout{display:flex;gap:24px;align-items:flex-start;margin-top:16px}
nav.rail{width:250px;flex:none;border-right:1px solid var(--rule);padding-right:18px}
main{flex:1;min-width:0}
[role=tablist]{display:flex;gap:4px;list-style:none;padding:0;margin:0 0 16px;border-bottom:1px solid var(--rule);flex-wrap:wrap}
[role=tab]{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:11.5px;letter-spacing:.06em;background:none;border:none;border-bottom:3px solid transparent;padding:8px 12px 6px;cursor:pointer;color:var(--ink);text-transform:uppercase}
[role=tab][aria-selected=true]{color:var(--accent);border-bottom-color:var(--accent)}
.bignum{font-family:Georgia,serif;font-size:46px;line-height:1.1}
.chips{display:flex;flex-wrap:wrap;gap:6px;margin:6px 0}
.chip{display:inline-flex;align-items:center;gap:6px;border:1px solid var(--rule);background:#fff;padding:2px 8px;font-size:13px;border-radius:12px}
.chip button{background:none;border:none;cursor:pointer;font-size:14px;line-height:1;padding:0;color:var(--accent)}
.sharebar{height:5px;background:var(--rule);margin:8px 0}
.sharebar>div{height:100%;background:var(--accent)}
.fhead{display:flex;justify-content:space-between;align-items:center;width:100%;background:none;border:none;border-top:1px solid var(--rule);padding:8px 0;cursor:pointer;font:inherit;text-align:left}
.fhead .n{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:11px;letter-spacing:.08em;color:#7a6f57}
.fbody{padding:4px 0 12px}
.fbody label{display:block;font-size:13px;margin:8px 0 2px}
.fbody input[type=text],.fbody select{width:100%;padding:5px 6px;font:inherit;border:1px solid var(--rule);background:#fff}
.tiles{display:flex;flex-wrap:wrap;gap:22px;margin:6px 0 18px}
.tile{border-top:1px solid var(--rule);padding-top:8px;min-width:150px}
.tile .sub{font-size:12.5px;color:#57503f;margin-top:2px}
.dot{display:inline-block;width:9px;height:9px;border-radius:50%;margin-right:5px}
.note{font-size:12.5px;color:#57503f;margin-top:2px}
figure{margin:26px 0}
figure figcaption{font-family:Georgia,serif;font-size:19px;margin-bottom:2px}
.figno{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:11px;letter-spacing:.08em;color:#7a6f57}
.chartbox{position:relative;height:auto;margin:10px 0 6px}
table{border-collapse:collapse;width:100%;font-size:14px}
th,td{text-align:left;padding:5px 8px;border-bottom:1px solid var(--rule);vertical-align:top}
th{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:11px;letter-spacing:.06em;text-transform:uppercase;font-weight:400;color:#7a6f57}
th.num,td.num{text-align:right;font-variant-numeric:tabular-nums}
caption{text-align:left;font-size:13px;color:#57503f;padding-bottom:5px}
table.rec td{font-size:13.5px}
tr.rec{cursor:pointer}
tr.rec:hover{background:#efe9dc}
tr.exp>td{background:#faf7f0}
.para-big{font-family:Georgia,serif;font-size:34px;color:var(--accent)}
mark{background:#f3d9a4}
button.btn{background:var(--accent);color:#fff;border:none;padding:6px 12px;font:inherit;font-size:13.5px;cursor:pointer}
button.btn.ghost{background:none;border:1px solid var(--accent);color:var(--accent)}
button.btn.small{padding:3px 9px;font-size:12.5px}
.checkline{border-top:1px solid var(--rule);padding:7px 0;font-size:14px;display:flex;gap:8px;align-items:baseline}
.pass{color:#0f766e;font-weight:600}
.fail{color:var(--accent);font-weight:600}
.warn{color:#a16207;font-weight:600}
.card{border:1px solid var(--rule);background:#faf7f0;margin:10px 0}
.card>button{width:100%;background:none;border:none;text-align:left;padding:8px 10px;cursor:pointer;font:inherit;font-size:14px}
.card .inner{padding:0 12px 12px}
.tally{border:1px solid var(--rule);background:#fff;padding:8px 12px;font-size:14px;margin:10px 0}
.seedbox{width:90px;padding:3px 6px;border:1px solid var(--rule);font:inherit}
footer.site{border-top:1px solid var(--rule);margin-top:30px;padding-top:10px;font-family:ui-monospace,Menlo,Consolas,monospace;font-size:11px;letter-spacing:.05em;color:#7a6f57}
h2.sec{font-family:Georgia,serif;font-weight:400;font-size:22px;margin:22px 0 8px}
.statecol{white-space:nowrap;font-size:12.5px}
</style>
</head>
<body>
<div class="wrap">
<header class="site">
  <div class="datalabel" id="datalabel"></div>
  <h1 id="title"></h1>
  <div class="metaline" id="metaline"></div>
</header>

<div class="layout">
<nav class="rail" aria-label="Filters">
  <div style="display:flex;justify-content:space-between;align-items:center">
    <span class="mono">Filters</span>
    <button class="mono" id="clearall" style="background:none;border:none;cursor:pointer;color:var(--accent);font-size:11px;letter-spacing:.08em;text-transform:uppercase">Clear all</button>
  </div>
  <div style="margin-top:6px">
    <div class="bignum" id="matchcount" aria-live="polite">0</div>
    <div style="font-size:12.5px;color:#57503f">of <span id="totalcount">0</span> in the file</div>
  </div>
  <div class="sharebar" role="img" aria-label="Share of file matching"><div id="sharefill" style="width:0"></div></div>
  <div class="chips" id="chips"></div>
  <div id="railfilters">
    <button class="fhead" aria-expanded="false" data-fh="kw"><span>Keyword</span><span class="n">01</span></button>
    <div class="fbody" data-fb="kw" hidden>
      <input type="text" id="kwbox" placeholder="e.g. torture" aria-label="Keyword filter">
      <div class="note">Literal match, not synonyms. Every word must occur in the text or symbol.</div>
    </div>
    <button class="fhead" aria-expanded="false" data-fh="mbt"><span>Mechanism, body, type</span><span class="n">02</span></button>
    <div class="fbody" data-fb="mbt" hidden>
      <label for="fmech">Mechanism</label><select id="fmech"></select>
      <label for="fbody">Body or mandate</label><select id="fbody"></select>
      <label for="ftype">Type</label><select id="ftype"></select>
      <div id="fstatewrap" hidden><label for="fstate">Recommending State (UPR)</label><select id="fstate"></select></div>
    </div>
    <button class="fhead" aria-expanded="false" data-fh="yr"><span>Years and SDG</span><span class="n">03</span></button>
    <div class="fbody" data-fb="yr" hidden>
      <label for="fyearfrom">Year from</label><select id="fyearfrom"></select>
      <label for="fyearto">to</label><select id="fyearto"></select>
      <label for="fsdg">SDG goal</label><select id="fsdg"></select>
    </div>
  </div>
</nav>

<main>
  <ul role="tablist" id="tabs">
    <li role="presentation"><button role="tab" id="tab-0" aria-selected="true" aria-controls="panel-0">01 Overview</button></li>
    <li role="presentation"><button role="tab" id="tab-1" aria-selected="false" aria-controls="panel-1">02 Records</button></li>
    <li role="presentation"><button role="tab" id="tab-2" aria-selected="false" aria-controls="panel-2">03 Check</button></li>
    <li role="presentation"><button role="tab" id="tab-3" aria-selected="false" aria-controls="panel-3">04 Method &amp; export</button></li>
  </ul>

  <section role="tabpanel" id="panel-0" aria-labelledby="tab-0">
    <div class="tiles" id="tiles"></div>
    <figure>
      <div class="figno">FIG.01</div>
      <figcaption id="fig1title"></figcaption>
      <div class="chartbox"><canvas id="fig1"></canvas></div>
      <div id="fig1empty" hidden style="padding:20px 0;color:#57503f">No records match the current filters.</div>
      <table id="fig1table"><caption></caption>
        <thead><tr><th scope="col">Theme</th><th scope="col" class="num">Records</th><th scope="col" class="num">% of filtered</th><th scope="col">Years</th></tr></thead>
        <tbody></tbody>
      </table>
      <div class="note">How this is computed: each value in a record's <em>themes</em> counts once, so bars add up to more than the number of records. Click a bar or a row to filter by that theme. Source: OHCHR UHRI labels, as published.</div>
    </figure>
    <figure>
      <div class="figno">FIG.02</div>
      <figcaption id="fig2title"></figcaption>
      <div class="chartbox"><canvas id="fig2"></canvas></div>
      <div class="note">How this is computed: records counted per year and per mechanism in the current filter; years with no records appear as gaps. Source: OHCHR UHRI, document dates ("dated by document").</div>
    </figure>
  </section>

  <section role="tabpanel" id="panel-1" aria-labelledby="tab-1" hidden>
    <div style="display:flex;gap:10px;align-items:center;margin-bottom:10px;flex-wrap:wrap">
      <input type="text" id="searchbox" placeholder="Search records" aria-label="Search records" style="flex:1;min-width:200px;padding:6px 8px;font:inherit;border:1px solid var(--rule)">
      <span class="mono" style="color:#7a6f57">Same as keyword filter</span>
    </div>
    <table class="rec"><caption id="reccaption"></caption>
      <thead><tr><th scope="col" id="thdate" style="cursor:pointer" title="Click to reverse order">Date ↑↓</th><th scope="col">Body</th><th scope="col">Symbol</th><th scope="col" class="num">Para.</th><th scope="col">First line</th><th scope="col">Recommending State</th></tr></thead>
      <tbody id="recbody"></tbody>
    </table>
    <div class="note" id="recnote"></div>
    <div style="margin-top:10px"><button class="btn ghost" id="morebtn">Show 50 more</button></div>
  </section>

  <section role="tabpanel" id="panel-2" aria-labelledby="tab-2" hidden>
    <h2 class="sec">How the app checks itself</h2>
    <div class="note">Every check compares two independently computed values. Nothing is hidden: a failed check is shown in red with its values.</div>
    <div id="checks"></div>
    <h2 class="sec">Check the UN's labels on a random sample</h2>
    <div class="note">This is your judgement of the UN's labels; nothing is sent anywhere. The labels are the weakest part of the data: a theme can be a legacy tag that no longer fits.</div>
    <div style="margin:10px 0;display:flex;gap:8px;flex-wrap:wrap;align-items:center">
      <button class="btn" id="drawbtn">Check 10 at random</button>
      <button class="btn ghost" id="redrawbtn" hidden>Draw again</button>
      <span id="seedwrap" hidden style="font-size:13px">Seed <input type="text" id="seedbox" class="seedbox" value="1" aria-label="Seed"> <button class="btn ghost small" id="seedbtn">Draw with this seed</button></span>
    </div>
    <div class="tally" id="tally" hidden></div>
    <div id="cards"></div>
  </section>

  <section role="tabpanel" id="panel-3" aria-labelledby="tab-3" hidden>
    <h2 class="sec">How each number is computed</h2>
    <div id="method" style="max-width:70ch"></div>
    <h2 class="sec">Take it with you</h2>
    <div style="display:flex;gap:10px;flex-wrap:wrap">
      <button class="btn" id="csvbtn">Download CSV of the current filter</button>
      <button class="btn ghost" id="sumbtn">Copy summary</button>
      <span id="sumcopied" class="mono" style="color:#0f766e" hidden>Copied</span>
    </div>
    <div class="note" style="margin-top:6px">The CSV opens with comment lines stating the country, source, build date, filters applied and row count. Nothing leaves the browser except the clipboard write on "Copy".</div>
    <h2 class="sec">Data</h2>
    <div id="sourcedata" style="max-width:70ch;font-size:14px"></div>
  </section>
</main>
</div>

<footer class="site" id="footer"></footer>
</div>

<script>
(function(){
"use strict";
const D = window.WORKSHOP_DATA && window.WORKSHOP_DATA.uhri;
if(!D || !D.records){document.body.innerHTML='<p style="padding:20px">No UHRI data loaded.</p>';return;}
const recs = D.records;
const fmt = n => n.toLocaleString('en-US');
const country = D.country || '';

/* ---------- derived basics ---------- */
const paraRe = /^(\d{1,3}(?:\.\d{1,3})?)\.?\s/;
function paraNum(t){const m=(t||'').match(paraRe);return m?m[1]:null;}
const stateRunRe = /((?:\s*\((?:[^()]|\([^()]*\))*\))+)\s*[;.]?\s*$/;
const stateGrpRe = /\((?:[^()]|\([^()]*\))*\)/g;
function uprStates(t){
  const m=(t||'').match(stateRunRe);
  if(!m)return [];
  const groups=m[1].match(stateGrpRe)||[];
  const out=[];
  for(const g of groups){
    let inner=g.replace(/^\(/,'').replace(/\)$/,'').trim();
    if(!inner)continue;
    if(inner.includes(',')||inner.length>60){return null;}
    out.push(inner);
  }
  return out.length?out:null;
}
recs.forEach(r=>{
  r._para = paraNum(r.text);
  r._states = (r.mechanism==='Universal Periodic Review')?uprStates(r.text):null;
});
const years=[...new Set(recs.map(r=>r.year))].sort((a,b)=>a-b);
const syms=[...new Set(recs.map(r=>r.symbol))];
const mechColor={'Universal Periodic Review':'#c2410c','Treaty bodies':'#0f766e','Special Procedures':'#7c3aed'};

/* ---------- header / footer ---------- */
document.getElementById('datalabel').textContent='UHRI · '+country;
document.getElementById('title').textContent='UN human rights recommendations and observations: '+country;
document.getElementById('metaline').innerHTML='Source: <a href="'+(D.source_url||'')+'" target="_blank" rel="noopener">'+(D.source||'OHCHR Universal Human Rights Index')+'</a> · '+fmt(recs.length)+' records · '+syms.length+' documents · '+years[0]+'–'+years[years.length-1]+' · built '+(D.built||'')+' · dated by document (the date is the document\u2019s, not the recommendation\u2019s).';
document.getElementById('totalcount').textContent=fmt(recs.length);
document.getElementById('footer').innerHTML='Built on OHCHR UHRI data · '+fmt(recs.length)+' records · <a href="'+(D.source_url||'')+'" target="_blank" rel="noopener">source</a>';

/* ---------- state filter values ---------- */
const stateCounts={};
recs.forEach(r=>{if(r.mechanism==='Universal Periodic Review'&&r._states){r._states.forEach(s=>stateCounts[s]=(stateCounts[s]||0)+1);}});
const stateList=Object.keys(stateCounts).sort((a,b)=>stateCounts[b]-stateCounts[a]);

/* ---------- filter state ---------- */
const F={kw:'',mech:'',body:'',type:'',state:'',yfrom:'',yto:'',sdg:'',theme:''};
function filtered(){
  return recs.filter(r=>{
    if(F.mech&&r.mechanism!==F.mech)return false;
    if(F.body&&r.body!==F.body)return false;
    if(F.type&&r.type!==F.type)return false;
    if(F.state&&!(r._states&&r._states.includes(F.state)))return false;
    if(F.theme&&!(r.themes&&r.themes.includes(F.theme)))return false;
    if(F.yfrom!==''&&r.year<+F.yfrom)return false;
    if(F.yto!==''&&r.year>+F.yto)return false;
    if(F.sdg!==''&&!(r.sdgs&&r.sdgs.includes(+F.sdg)))return false;
    if(F.kw){
      const hay=(r.text+' '+r.symbol).toLowerCase();
      const ws=F.kw.trim().toLowerCase().split(/\s+/).filter(Boolean);
      for(const w of ws)if(!hay.includes(w))return false;
    }
    return true;
  });
}

/* ---------- rail ---------- */
function sel(id,opts,val){
  const s=document.getElementById(id);
  s.innerHTML=opts.map(o=>'<option'+(o.v===val?' selected':'')+' value="'+esc(o.v)+'">'+esc(o.t)+'</option>').join('');
}
function esc(s){return String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));}
function fillMech(){
  const mechs=[...new Set(recs.map(r=>r.mechanism))];
  sel('fmech',[{v:'',t:'all'}].concat(mechs.map(m=>({v:m,t:m}))),F.mech);
  const pool=F.mech?recs.filter(r=>r.mechanism===F.mech):recs;
  const bc={};pool.forEach(r=>bc[r.body]=(bc[r.body]||0)+1);
  const bodies=Object.keys(bc).sort((a,b)=>bc[b]-bc[a]);
  sel('fbody',[{v:'',t:'all'}].concat(bodies.map(b=>({v:b,t:b+' ('+bc[b]+')'}))),F.body);
  const tc={};pool.forEach(r=>tc[r.type]=(tc[r.type]||0)+1);
  sel('ftype',[{v:'',t:'all'}].concat(Object.keys(tc).map(t=>({v:t,t:t+' ('+tc[t]+')'}))),F.type);
  sel('fstate',[{v:'',t:'all'}].concat(stateList.map(s=>({v:s,t:s+' ('+stateCounts[s]+')'}))),F.state);
  document.getElementById('fstatewrap').hidden = !stateList.length;
}
function fillYearsSdg(){
  sel('fyearfrom',[{v:'',t:'—'}].concat(years.map(y=>({v:y,t:y}))),F.yfrom);
  sel('fyearto',[{v:'',t:'—'}].concat(years.map(y=>({v:y,t:y}))),F.yto);
  const g={};recs.forEach(r=>(r.sdgs||[]).forEach(s=>g[s]=(g[s]||0)+1));
  const names=D.sdg_names||{};
  sel('fsdg',[{v:'',t:'all'}].concat(Object.keys(g).map(Number).sort((a,b)=>a-b).map(s=>({v:s,t:'SDG '+s+': '+(names[String(s)]||'')+' ('+g[s]+')'}))),F.sdg);
}
fillMech();fillYearsSdg();

/* collapsible filter headings: one open at a time */
let openFh=null;
document.querySelectorAll('.fhead').forEach(h=>{
  h.addEventListener('click',()=>{
    const k=h.dataset.fh;
    if(openFh===k){h.setAttribute('aria-expanded','false');document.querySelector('[data-fb="'+k+'"]').hidden=true;openFh=null;return;}
    if(openFh){const oh=document.querySelector('.fhead[data-fh="'+openFh+'"]');oh.setAttribute('aria-expanded','false');document.querySelector('[data-fb="'+openFh+'"]').hidden=true;}
    openFh=k;h.setAttribute('aria-expanded','true');document.querySelector('[data-fb="'+k+'"]').hidden=false;
  });
});

/* chips */
function chips(){
  const c=document.getElementById('chips');c.innerHTML='';
  const add=(label,key)=>{const d=document.createElement('span');d.className='chip';d.innerHTML=esc(label)+' <button aria-label="Remove filter '+esc(label)+'">×</button>';d.querySelector('button').onclick=()=>{F[key]='';syncInputs();apply();};c.appendChild(d);};
  if(F.kw)add('“'+F.kw+'”','kw');
  if(F.mech)add(F.mech,'mech');
  if(F.body)add(F.body,'body');
  if(F.type)add(F.type,'type');
  if(F.state)add(F.state,'state');
  if(F.theme)add('Theme: '+F.theme,'theme');
  if(F.yfrom!==''||F.yto!=='')add('Years: '+(F.yfrom||years[0])+'–'+(F.yto||years[years.length-1]),'years');
  if(F.sdg!=='')add('SDG '+F.sdg,'sdg');
}
document.getElementById('clearall').onclick=()=>{F.kw='';F.mech='';F.body='';F.type='';F.state='';F.theme='';F.yfrom='';F.yto='';F.sdg='';syncInputs();apply();};

function syncInputs(){
  document.getElementById('kwbox').value=F.kw;
  document.getElementById('searchbox').value=F.kw;
  fillMech();fillYearsSdg();
}

/* keyword: 300ms debounce, two boxes */
let kwT=null;
function kwSet(v){clearTimeout(kwT);kwT=setTimeout(()=>{F.kw=v;apply();},300);}
document.getElementById('kwbox').addEventListener('input',e=>kwSet(e.target.value));
document.getElementById('searchbox').addEventListener('input',e=>{document.getElementById('kwbox').value=e.target.value;kwSet(e.target.value);});

document.getElementById('fmech').onchange=e=>{F.mech=e.target.value;F.body='';F.type='';fillMech();apply();};
document.getElementById('fbody').onchange=e=>{F.body=e.target.value;apply();};
document.getElementById('ftype').onchange=e=>{F.type=e.target.value;apply();};
document.getElementById('fstate').onchange=e=>{F.state=e.target.value;apply();};
document.getElementById('fyearfrom').onchange=e=>{F.yfrom=e.target.value;fixYears();apply();};
document.getElementById('fyearto').onchange=e=>{F.yto=e.target.value;fixYears();apply();};
document.getElementById('fsdg').onchange=e=>{F.sdg=e.target.value;apply();};
function fixYears(){
  if(F.yfrom!==''&&F.yto!==''&&+F.yfrom>+F.yto){const t=F.yfrom;F.yfrom=F.yto;F.yto=t;syncInputs();}
}

/* ---------- tabs ---------- */
let curTab=0;
const tabs=[...document.querySelectorAll('[role=tab]')];
function showTab(i){
  curTab=i;
  tabs.forEach((t,j)=>{t.setAttribute('aria-selected',j===i?'true':'false');document.getElementById('panel-'+j).hidden=j!==i;});
  document.getElementById('railfilters').hidden=(i>=2);
  if(i===0){drawOverview();}
  if(i===1){renderRows();}
  if(i===2){renderChecks();}
  if(i===3){renderMethod();}
}
tabs.forEach((t,i)=>{
  t.addEventListener('click',()=>showTab(i));
  t.addEventListener('keydown',e=>{
    let j=null;
    if(e.key==='ArrowRight')j=(i+1)%tabs.length;
    if(e.key==='ArrowLeft')j=(i-1+tabs.length)%tabs.length;
    if(e.key==='Home')j=0;if(e.key==='End')j=tabs.length-1;
    if(j!==null){e.preventDefault();tabs[j].focus();showTab(j);}
  });
});

/* ---------- overview ---------- */
let ch1=null,ch2=null;
function topThemes(set){
  const c={};
  set.forEach(r=>(r.themes||[]).forEach(t=>c[t]=(c[t]||0)+1));
  const list=Object.keys(c).map(t=>({t,n:c[t]}));
  list.sort((a,b)=>b.n-a.n||a.t.localeCompare(b.t));
  return list.slice(0,10);
}
function tiles(set){
  const tc={};set.forEach(r=>tc[r.type]=(tc[r.type]||0)+1);
  const breakdown=Object.keys(tc).sort((a,b)=>tc[b]-tc[a]).map(t=>fmt(tc[t])+' '+t).join(' · ')||'—';
  const ds=[...new Set(set.map(r=>r.symbol))];
  const ys=set.map(r=>r.year);
  let html='<div class="tile"><div class="bignum">'+fmt(set.length)+'</div><div class="sub">records in the current filter<br>'+esc(breakdown)+'</div><div class="note">Type filter starts on "all". How computed: count of records; breakdown counts each <em>type</em> as spelled in the data.</div></div>';
  html+='<div class="tile"><div class="bignum">'+fmt(ds.length)+'</div><div class="sub">documents</div><div class="note">Distinct <em>symbol</em> in the current filter.</div></div>';
  if(ys.length)html+='<div class="tile"><div class="bignum" style="font-size:34px;padding-top:8px">'+Math.min(...ys)+'–'+Math.max(...ys)+'</div><div class="sub">years covered</div><div class="note">Min and max <em>year</em> in the current filter.</div></div>';
  const mechs=[...new Set(recs.map(r=>r.mechanism))];
  mechs.forEach(m=>{
    const ms=set.filter(r=>r.mechanism===m);
    const md=[...new Set(ms.map(r=>r.symbol))];
    const my=ms.length?Math.max(...ms.map(r=>r.year)):'—';
    const share=set.length?Math.round(100*ms.length/set.length)+'%':'0%';
    html+='<div class="tile"><div style="margin-top:8px"><span class="dot" style="background:'+(mechColor[m]||'#888')+'"></span><span class="mono">'+esc(m)+'</span></div><div class="bignum" style="font-size:30px">'+fmt(ms.length)+'</div><div class="sub">'+md.length+' documents · latest '+my+' · '+share+' of filtered</div>'
      +(m==='Universal Periodic Review'?'<div class="note"><a href="#" id="seestates">see the States</a></div>':'')+'</div>';
  });
  document.getElementById('tiles').innerHTML=html;
  const ss=document.getElementById('seestates');
  if(ss)ss.onclick=e=>{e.preventDefault();showStates(set);};
}
function showStates(set){
  const upr=set.filter(r=>r.mechanism==='Universal Periodic Review'&&r._states);
  const c={};upr.forEach(r=>r._states.forEach(s=>c[s]=(c[s]||0)+1));
  const top=Object.keys(c).sort((a,b)=>c[b]-c[a]).slice(0,10);
  if(!top.length)return;
  let h='<table><caption>Ten States that made most recommendations to '+esc(country)+' (current filter). A record counts once for each State named in it: this is a count of recommendations, not of influence.</caption><thead><tr><th scope="col">State</th><th scope="col" class="num">Recommendations</th></tr></thead><tbody>';
  top.forEach(s=>h+='<tr><td>'+esc(s)+'</td><td class="num">'+fmt(c[s])+'</td></tr>');
  h+='</tbody></table>';
  let el=document.getElementById('statesbox');
  if(!el){el=document.createElement('div');el.id='statesbox';document.getElementById('tiles').after(el);}
  el.innerHTML=h;el.scrollIntoView({behavior:'smooth',block:'nearest'});
}
function drawOverview(){
  const set=filtered();
  tiles(set);
  document.getElementById('fig1title').textContent='Ten most frequent themes among '+fmt(set.length)+' filtered records';
  const tt=topThemes(set);
  const fig1empty=document.getElementById('fig1empty');
  document.getElementById('fig1table').hidden=!tt.length;
  if(ch1)ch1.destroy();
  if(!tt.length){fig1empty.hidden=false;return;}
  fig1empty.hidden=true;
  ch1=new Chart(document.getElementById('fig1'),{
    type:'bar',
    data:{labels:tt.map(x=>x.t),datasets:[{data:tt.map(x=>x.n),backgroundColor:'rgba(155,35,53,0.8)',borderColor:'#9b2335',borderWidth:0}]},
    options:{indexAxis:'y',responsive:true,maintainAspectRatio:false,
      height:tt.length*32,
      onClick:(e,els)=>{if(els.length){F.theme=tt[els[0].index].t;apply();}},
      onHover:(e,els)=>{e.native.target.style.cursor=els.length?'pointer':'default';},
      plugins:{legend:{display:false},tooltip:{callbacks:{label:c=>' '+fmt(c.raw)+' records (a record can carry several themes)'}}},
      scales:{x:{beginAtZero:true,ticks:{precision:0}},y:{ticks:{font:{size:12},autoSkip:false}}}}
  });
  document.querySelector('#fig1table caption').textContent='The same ten themes as the chart. A record can carry several themes, so counts sum to more than '+fmt(set.length)+'.';
  document.querySelector('#fig1table tbody').innerHTML=tt.map(x=>{
    const ys=set.filter(r=>r.themes&&r.themes.includes(x.t)).map(r=>r.year);
    const pct=set.length?(100*x.n/set.length).toFixed(1):'0.0';
    return '<tr style="cursor:pointer"><td><a href="#" data-theme="'+esc(x.t)+'">'+esc(x.t)+'</a></td><td class="num">'+fmt(x.n)+'</td><td class="num">'+pct+'</td><td>'+Math.min(...ys)+'–'+Math.max(...ys)+'</td></tr>';
  }).join('');
  document.querySelectorAll('#fig1table a[data-theme]').forEach(a=>a.onclick=e=>{e.preventDefault();F.theme=a.dataset.theme;apply();});

  document.getElementById('fig2title').textContent='Records per year by mechanism ('+fmt(set.length)+' filtered records)';
  const allY=[];for(let y=years[0];y<=years[years.length-1];y++)allY.push(y);
  const mechs=[...new Set(recs.map(r=>r.mechanism))];
  if(ch2)ch2.destroy();
  ch2=new Chart(document.getElementById('fig2'),{
    type:'bar',
    data:{labels:allY,datasets:mechs.map(m=>({label:m,data:allY.map(y=>set.filter(r=>r.year===y&&r.mechanism===m).length),backgroundColor:mechColor[m]||'#888'}))},
    options:{responsive:true,maintainAspectRatio:false,
      plugins:{legend:{position:'bottom',labels:{boxWidth:10}},tooltip:{}},
      scales:{x:{stacked:true,title:{display:true,text:'Year (dated by document)'}},y:{stacked:true,beginAtZero:true,ticks:{precision:0}}}}
  });
}

/* ---------- records table ---------- */
let sortDesc=true, shown=0, rowSet=[];
function firstLine(t){
  t=t||'';
  if(t.length<=120)return t;
  const cut=t.slice(0,120);const sp=cut.lastIndexOf(' ');
  return cut.slice(0,sp>0?sp:120)+'…';
}
function hl(s){
  let out=esc(s);
  if(F.kw){F.kw.trim().toLowerCase().split(/\s+/).filter(Boolean).forEach(w=>{
    out=out.replace(new RegExp('('+w.replace(/[.*+?^${}()|[\]\\]/g,'\\$&')+')','gi'),'<mark>$1</mark>');
  });}
  return out;
}
function rowSort(a,b){
  if(sortDesc){
    if(a.date!==b.date)return a.date<b.date?1:-1;
  }else{
    if(a.date!==b.date)return a.date>b.date?1:-1;
  }
  if(a.body!==b.body)return a.body<b.body?-1:1;
  const pa=a._para?parseFloat(a._para):Infinity, pb=b._para?parseFloat(b._para):Infinity;
  if(pa!==pb)return pa-pb;
  return recs.indexOf(a)-recs.indexOf(b);
}
function renderRows(keep){
  if(!keep){rowSet=filtered().slice().sort(rowSort);shown=Math.min(50,rowSet.length);}
  const tb=document.getElementById('recbody');
  document.getElementById('reccaption').textContent=(rowSet.length?fmt(shown)+' rows shown of '+fmt(rowSet.length)+' matching':'No records match the current filters')+' · sorted by date '+(sortDesc?'descending (newest first)':'ascending')+' · click a row to read the full paragraph';
  tb.innerHTML='';
  rowSet.slice(0,shown).forEach((r,i)=>{
    const tr=document.createElement('tr');tr.className='rec';tr.tabIndex=0;tr.setAttribute('aria-expanded','false');
    const st=r.mechanism==='Universal Periodic Review'?(r._states?esc(r._states.join(', ')):'State not found'):'—';
    tr.innerHTML='<td>'+esc(r.date)+'</td><td>'+esc(r.body)+'</td><td><a href="'+esc(r.doc_url)+'" target="_blank" rel="noopener" onclick="event.stopPropagation()">'+esc(r.symbol)+'</a></td><td class="num">'+(r._para?esc(r._para):'—')+'</td><td>'+hl(firstLine(r.text))+'</td><td class="statecol">'+st+'</td>';
    tr.addEventListener('click',()=>toggleRow(tr,r));
    tr.addEventListener('keydown',e=>{if(e.key==='Enter'){e.preventDefault();toggleRow(tr,r);}});
    tb.appendChild(tr);
  });
  document.getElementById('morebtn').hidden=shown>=rowSet.length;
  document.getElementById('morebtn').textContent='Show 50 more ('+fmt(rowSet.length-shown)+' left)';
}
function toggleRow(tr,r){
  const next=tr.nextElementSibling;
  if(next&&next.classList.contains('exp')){next.remove();tr.setAttribute('aria-expanded','false');return;}
  document.querySelectorAll('tr.exp').forEach(e=>e.remove());
  document.querySelectorAll('tr.rec').forEach(e=>e.setAttribute('aria-expanded','false'));
  const names=D.sdg_names||{};
  const chipsHtml=(r.themes&&r.themes.length?r.themes.map(t=>'<span class="chip">'+esc(t)+'</span>').join(''):'<span class="note">not labelled (no themes)</span>');
  const sdgHtml=(r.sdgs&&r.sdgs.length?r.sdgs.map(s=>'SDG '+s+': '+esc(names[String(s)]||'')).join(' · '):'<span class="note">not labelled (no SDGs)</span>');
  const targets=(r.sdg_targets&&r.sdg_targets.length)?'<div class="note">Targets: '+esc(r.sdg_targets.join(' · '))+'</div>':'';
  const ap=(r.affected_persons&&r.affected_persons.length)?esc(r.affected_persons.join(' · ')):'<span class="note">not labelled (no affected persons)</span>';
  const citation=r._para?r.symbol+', para. '+r._para:r.symbol;
  const ex=document.createElement('tr');ex.className='exp';
  ex.innerHTML='<td colspan="6"><div style="display:flex;gap:18px;align-items:flex-start">'
    +'<div class="para-big">'+(r._para?esc(r._para):'—')+'</div>'
    +'<div style="flex:1"><p style="margin:0 0 8px">'+esc(r.text)+'</p>'
    +'<div class="chips">'+chipsHtml+'</div>'
    +'<div class="note">'+sdgHtml+'</div>'+targets
    +'<div class="note">Affected persons: '+ap+'</div>'
    +(r.section?'<div class="note">Section: '+esc(r.section)+'</div>':'')
    +'<div style="margin-top:8px;display:flex;gap:8px;flex-wrap:wrap;align-items:center">'
    +'<button class="btn small" data-copy="'+esc(citation)+'">Copy citation'+(r._para?'':' (no paragraph number in this extract)')+'</button>'
    +'<a class="btn ghost small" style="text-decoration:none;display:inline-block;padding:3px 9px;font-size:12.5px" href="'+esc(r.doc_url)+'" target="_blank" rel="noopener">Open the UN document</a>'
    +'<span class="mono" style="color:#0f766e" hidden>Copied</span></div>'
    +'<div class="note">Citation form: symbol, para. N. The text is verbatim from the extract; nothing is paraphrased.</div>'
    +'</div></div></td>';
  ex.querySelector('[data-copy]').addEventListener('click',function(e){
    e.stopPropagation();
    const span=this.parentNode.querySelector('span[hidden]');
    copy(this.dataset.copy,span);
  });
  ex.addEventListener('click',e=>e.stopPropagation());
  tr.after(ex);tr.setAttribute('aria-expanded','true');
}
document.getElementById('morebtn').onclick=()=>{shown=Math.min(shown+50,rowSet.length);renderRows(true);};
document.getElementById('thdate').onclick=()=>{sortDesc=!sortDesc;renderRows();};

function copy(text,confirmEl){
  const done=()=>{if(confirmEl){confirmEl.hidden=false;setTimeout(()=>confirmEl.hidden=true,2000);}};
  if(navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText(text).then(done).catch(()=>fallback());}
  else fallback();
  function fallback(){const ta=document.createElement('textarea');ta.value=text;document.body.appendChild(ta);ta.select();try{document.execCommand('copy');}catch(e){}ta.remove();done();}
}

/* ---------- checks ---------- */
function renderChecks(){
  const box=document.getElementById('checks');box.innerHTML='';
  const line=(what,a,b,pass,cls)=>{const d=document.createElement('div');d.className='checkline';
    d.innerHTML='<span class="'+(pass?'pass':(cls||'fail'))+'">'+(pass?'✓ pass':(cls==='warn'?'⚠ warning':'✗ check failed'))+'</span><span>'+esc(what)+'</span><span style="margin-left:auto;font-size:13px;color:#57503f">'+esc(a)+' vs '+esc(b)+'</span>';box.appendChild(d);return d;};
  const total=recs.length, decl=Number(D.count);
  line('Record count: records.length vs the file\u2019s declared count',fmt(total),fmt(decl),total===decl);
  // partitions
  let ok=true,det=[];
  ['mechanism','body','year','type'].forEach(f=>{
    const c={};recs.forEach(r=>c[f==='year'?r.year:r[f]]=(c[f==='year'?r.year:r[f]]||0)+1);
    const s=Object.values(c).reduce((a,b)=>a+b,0);
    const p=s===total;ok=ok&&p;if(!p)det.push(f+' sums to '+s);
  });
  line('Partitions: counts per mechanism, body, year and type each sum to the record count',det.length?('failed: '+det.join('; ')):'all four partitions',fmt(total),ok);
  // chart vs table (recompute over current filter)
  const set=filtered();const tt=topThemes(set);
  let chartOk=set.length===0||true, mismatch=null;
  if(tt.length){
    const c={};set.forEach(r=>(r.themes||[]).forEach(t=>c[t]=(c[t]||0)+1));
    const maxN=Math.max(...tt.map(x=>x.n));
    chartOk=tt.every(x=>x.n===c[x.t])&&maxN<=set.length;
    if(!chartOk)mismatch='a bar differs from its recomputed count';
  }
  line('Chart against table: each FIG.01 bar equals a second independent count of that theme; the largest bar is not larger than the filtered count',mismatch||'all bars match',fmt(set.length)+' filtered',chartOk);
  // links
  const bad=[];
  recs.forEach(r=>{
    let u=r.doc_url||'';
    let okUrl=u.startsWith('https://docs.un.org/');
    try{const dec=decodeURIComponent(u).replace(/\/+$/,'').toLowerCase();const sym=r.symbol.toLowerCase().replace(/\s+/g,'');okUrl=okUrl&&dec.endsWith(sym);}catch(e){okUrl=false;}
    if(!okUrl)bad.push(r.symbol);
  });
  const lk=document.createElement('div');lk.className='checkline';
  lk.innerHTML='<span class="'+(bad.length?'fail':'pass')+'">'+(bad.length?'✗ check failed':'✓ pass')+'</span><span>Links: every doc_url starts with https://docs.un.org/ and ends with its symbol</span><span style="margin-left:auto;font-size:13px;color:#57503f">'+(bad.length?esc(bad.slice(0,8).join(', '))+(bad.length>8?' +'+(bad.length-8)+' more':''):fmt(recs.length)+' links')+'</span>';
  box.appendChild(lk);
  // paragraph numbers
  const mechs=[...new Set(recs.map(r=>r.mechanism))];
  mechs.forEach(m=>{
    const ms=recs.filter(r=>r.mechanism===m);
    const withP=ms.filter(r=>r._para).length;
    const pct=ms.length?100*withP/ms.length:100;
    const full=m==='Universal Periodic Review';
    line('Paragraph numbers found: '+m,fmt(withP)+' of '+fmt(ms.length)+' ('+(ms.length?(100*withP/ms.length).toFixed(1):'0')+'%)','UPR expected at 100%',pct>=(full?100:0)?(pct<100&&!full?'pass':'pass'):false,pct<100&&full?'warn':(pct<100?'warn':undefined));
  });
  // states
  const upr=recs.filter(r=>r.mechanism==='Universal Periodic Review');
  const withS=upr.filter(r=>r._states).length;
  const noS=upr.filter(r=>!r._states).map(r=>r.symbol+' \u2014 ends: \u2026'+(r.text||'').slice(-60));
  const st=document.createElement('div');st.className='checkline';
  st.innerHTML='<span class="'+(withS===upr.length?'pass':'warn')+'">'+(withS===upr.length?'✓ pass':'⚠ warning')+'</span><span>States found: UPR records with at least one recommending State extracted</span><span style="margin-left:auto;font-size:13px;color:#57503f">'+fmt(withS)+' of '+fmt(upr.length)+(noS.length?' · without: '+noS.slice(0,5).map(esc).join(' | ')+(noS.length>5?' +'+(noS.length-5)+' more':''):'')+'</span>';
  box.appendChild(st);
  // duplicates and gaps
  const ids=new Set(recs.map(r=>r.id));
  const txts={};let dup=0;recs.forEach(r=>{if(txts[r.text])dup++;else txts[r.text]=1;});
  const noTheme=recs.filter(r=>!r.themes||!r.themes.length).length;
  const noSdg=recs.filter(r=>!r.sdgs||!r.sdgs.length).length;
  const noAp=recs.filter(r=>!r.affected_persons||!r.affected_persons.length).length;
  line('Duplicates and gaps: distinct id vs record count',fmt(ids.size),fmt(total),ids.size===total);
  line('Duplicate texts (records whose text is identical to another\u2019s)',fmt(dup),'duplicates',true);
  const gl=document.createElement('div');gl.className='checkline';
  gl.innerHTML='<span class="pass">✓ shown</span><span>Not labelled: records with no themes, no SDGs, no affected persons</span><span style="margin-left:auto;font-size:13px;color:#57503f">'+fmt(noTheme)+' · '+fmt(noSdg)+' · '+fmt(noAp)+' (shown as "not labelled" on expand)</span>';
  box.appendChild(gl);
}

/* ---------- random sample label check ---------- */
function mulberry32(a){return function(){a|=0;a=a+0x6D2B79F5|0;let t=Math.imul(a^a>>>15,1|a);t=t+Math.imul(t^t>>>7,61|t)^t;return((t^t>>>14)>>>0)/4294967296;};}
let sample=null, verdicts={};
function drawSample(seed){
  const set=filtered();
  if(!set.length){document.getElementById('cards').innerHTML='<p class="note">No records match the current filters.</p>';return;}
  const rnd=mulberry32(seed);
  const idx=new Set();
  while(idx.size<Math.min(10,set.length))idx.add(Math.floor(rnd()*set.length));
  sample=[...idx].map(i=>set[i]);
  verdicts={};
  const cards=document.getElementById('cards');cards.innerHTML='';
  sample.forEach((r,i)=>{
    const c=document.createElement('div');c.className='card';
    const themes=(r.themes&&r.themes.length)?r.themes.map(t=>'<span class="chip">'+esc(t)+'</span>').join(''):'<span class="note">not labelled (no themes)</span>';
    c.innerHTML='<button aria-expanded="false">'+esc(r.symbol)+(r._para?', para. '+esc(r._para):'')+' <span style="color:#7a6f57">'+esc(r.body)+' · '+esc(r.date)+'</span></button>'
      +'<div class="inner" hidden><p style="margin:0 0 8px">'+esc(r.text)+'</p><div class="chips">'+themes+'</div>'
      +'<div style="margin-top:8px;display:flex;gap:6px;flex-wrap:wrap" data-v="'+i+'">'
      +'<button class="btn small">Fits</button><button class="btn ghost small">Doesn\u2019t fit</button><button class="btn ghost small">Unsure</button>'
      +'<a class="btn ghost small" style="text-decoration:none;padding:3px 9px;font-size:12.5px" href="'+esc(r.doc_url)+'" target="_blank" rel="noopener">Open document</a></div></div>';
    const btn=c.querySelector('button');const inner=c.querySelector('.inner');
    btn.onclick=()=>{const o=!inner.hidden;inner.hidden=o;btn.setAttribute('aria-expanded',String(!o));};
    const vb=c.querySelector('[data-v]');const id=r.id;
    const mark=[...vb.querySelectorAll('.btn')];
    vb.addEventListener('click',e=>{
      const b=e.target.closest('button');if(!b)return;
      verdicts[id]=mark.indexOf(b);
      mark.forEach((m,j)=>{m.className=j===mark.indexOf(b)?'btn small':'btn ghost small';});
      tally();
    });
    cards.appendChild(c);
  });
  document.getElementById('redrawbtn').hidden=false;
  document.getElementById('seedwrap').hidden=false;
  document.getElementById('seedbox').value=String(seed);
  tally();
}
function tally(){
  const t=document.getElementById('tally');t.hidden=false;
  const v=Object.values(verdicts);
  const f=v.filter(x=>x===0).length,d=v.filter(x=>x===1).length,u=v.filter(x=>x===2).length;
  t.innerHTML='Themes: <strong>'+f+' fit, '+d+' don\u2019t, '+u+' unsure of '+v.length+' judged</strong> (drawn with seed <strong>'+esc(document.getElementById('seedbox').value)+'</strong>; a colleague can draw the same ten). This tally is your judgement, labelled as such; the app never changes a UN label.';
}
document.getElementById('drawbtn').onclick=()=>drawSample(1);
document.getElementById('redrawbtn').onclick=()=>drawSample(Math.floor(Math.random()*1e6)+1);
document.getElementById('seedbtn').onclick=()=>{const s=parseInt(document.getElementById('seedbox').value,10);drawSample(isNaN(s)?1:s);};

/* ---------- method & export ---------- */
function renderMethod(){
  const m=document.getElementById('method');
  if(m.dataset.done)return;
  m.innerHTML=['<p><strong>Headline total</strong> = the number of records in the file; the breakdown counts records per <em>type</em>, using the UN\u2019s own spelling. <strong>Documents</strong> = distinct <em>symbol</em>; <strong>years</strong> = the minimum and maximum <em>year</em>.</p>',
  '<p><strong>Filters</strong> combine with AND. Mechanism, body, type, State and theme are exact matches on the field. Year is inclusive between the two selects; a reversed range is swapped. SDG matches records listing that goal. The keyword is lower-cased and every word must occur as a substring of the text or symbol \u2014 literal, not synonyms.</p>',
  '<p><strong>Theme counts</strong>: each value in a record\u2019s <em>themes</em> counts once, so theme counts sum to more than the record count; percentages are of records. The year range per theme is the first and last year of the records carrying it.</p>',
  '<p><strong>Paragraph number</strong> = the first number at the start of the text (\u201c71\u201d or \u201c144.43\u201d); no match means no number. <strong>Recommending State</strong> is extracted only from UPR records, from the parenthesised groups at the end of the text; a record counts once for each State named. <strong>Citation</strong> = symbol plus \u201c, para. N\u201d when a number was found.</p>',
  '<p><strong>First line</strong> = the text up to 120 characters, cut at a word. The full text is always shown unchanged on expand.</p>',
  '<p>Nothing is estimated and no model is called: every count is a loop over the records in JavaScript, in this page.</p>'].join('');
  m.dataset.done='1';
  const src=document.getElementById('sourcedata');
  src.innerHTML='Source: <a href="'+esc(D.source_url||'')+'" target="_blank" rel="noopener">'+esc(D.source||'')+'</a> · '+fmt(recs.length)+' records · '+syms.length+' documents · years '+years[0]+'–'+years[years.length-1]+' · built '+esc(D.built||'')+'. <br>Licence: OHCHR data, used here for this workshop; cite the Universal Human Rights Index. Design follows UK Government Analysis Function guidance on charts and tables, OHCHR\u2019s Human Rights-Based Approach to Data, and the Dag Hammarskj\u00f6ld Library\u2019s citation advice.';
}
document.getElementById('csvbtn').onclick=()=>{
  const set=filtered().slice().sort(rowSort);
  const q=s=>'"'+String(s==null?'':s).replace(/"/g,'""')+'"';
  const lines=[];
  lines.push('# '+country+' \u2014 UN human rights recommendations and observations (UHRI)');
  lines.push('# Source: '+(D.source||'')+' '+(D.source_url||''));
  lines.push('# Built: '+(D.built||'')+' · dated by document');
  lines.push('# Filters applied: '+(F.kw?'keyword="'+F.kw+'" ':'')+(F.mech?'mechanism='+F.mech+' ':'')+(F.body?'body='+F.body+' ':'')+(F.type?'type='+F.type+' ':'')+(F.state?'state='+F.state+' ':'')+(F.theme?'theme='+F.theme+' ':'')+((F.yfrom!==''||F.yto!=='')?'years='+ (F.yfrom||years[0])+'-'+(F.yto||years[years.length-1])+' ':'')+(F.sdg!==''?'sdg='+F.sdg+' ':'')+'(none)' .replace(' (none)',''));
  lines.push('# Rows: '+set.length+' of '+recs.length);
  lines.push(['date','body','mechanism','type','symbol','doc_url','paragraph','recommending_states','section','themes','sdgs','sdg_targets','affected_persons','text'].map(q).join(','));
  set.forEach(r=>{
    lines.push([r.date,r.body,r.mechanism,r.type,r.symbol,r.doc_url,r._para||'',(r._states||[]).join('; '),r.section||'',(r.themes||[]).join('; '),(r.sdgs||[]).join('; '),(r.sdg_targets||[]).join('; '),(r.affected_persons||[]).join('; '),r.text].map(q).join(','));
  });
  const blob=new Blob([lines.join('\r\n')],{type:'text/csv'});
  const a=document.createElement('a');a.href=URL.createObjectURL(blob);
  a.download='uhri_'+country.replace(/\s+/g,'_').toLowerCase()+'.csv';a.click();
  setTimeout(()=>URL.revokeObjectURL(a.href),5000);
};
document.getElementById('sumbtn').onclick=()=>{
  const set=filtered();
  const tt=topThemes(set);
  const mechs=[...new Set(recs.map(r=>r.mechanism))];
  const txt=country+': '+fmt(set.length)+' UN human rights records ('+syms.length+' documents, '+years[0]+'\u2013'+years[years.length-1]+'), from the OHCHR Universal Human Rights Index (built '+D.built+'). By mechanism: '+mechs.map(m=>fmt(set.filter(r=>r.mechanism===m).length)+' '+m).join(', ')+'. Most frequent themes: '+tt.map(t=>t.t+' ('+t.n+')').join('; ')+'. Numbers computed in-browser from UHRI data; theme counts sum to more than the record count because a record can carry several themes.';
  copy(txt,document.getElementById('sumcopied'));
};

/* ---------- apply & boot ---------- */
function apply(){
  chips();
  const set=filtered();
  document.getElementById('matchcount').textContent=fmt(set.length);
  document.getElementById('sharefill').style.width=recs.length?(100*set.length/recs.length)+'%':'0';
  if(curTab===0)drawOverview();
  if(curTab===1)renderRows();
  if(curTab===2)renderChecks();
}
apply();showTab(0);
})();
</script>
</body>
</html>
```