I built the four-tab Kenya dashboard on the attached file. The checks panel and the 10-record label sample are on tab 03. I have not run it against your data, so the numbers and the State extraction are untested. The data has no licence field, so tab 04 says to check the licence on the source page.

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>UN human rights recommendations dashboard</title>
<style>
[hidden]{display:none!important}
*{box-sizing:border-box}
body{margin:0;background:#f4f0e8;color:#1d1b18;font:16px/1.5 system-ui,-apple-system,"Segoe UI",sans-serif}
.mono,.hint,th,.tab,.acch,.chip,.how,.lab{font-family:ui-monospace,Menlo,Consolas,monospace}
.mono{font-size:11.5px;text-transform:uppercase;letter-spacing:.08em}
.serif,h1,h2,h3,.big{font-family:Georgia,"Times New Roman",serif;font-weight:400}
a{color:#9b2335}
:focus-visible{outline:3px solid #9b2335;outline-offset:2px}
header{padding:16px 24px 10px;border-bottom:1px solid #d9d2c3}
h1{font-size:28px;line-height:1.2;margin:4px 0 6px}
.src{font-size:14px;color:#4d483f;margin:0}
.layout{display:grid;grid-template-columns:272px minmax(0,1fr)}
aside{padding:16px 18px;border-right:1px solid #d9d2c3}
main{padding:0 24px 28px;min-width:0}
.rh{display:flex;justify-content:space-between;align-items:center}
.lnk{background:none;border:0;color:#9b2335;text-decoration:underline;cursor:pointer;font:inherit;font-size:13px;padding:2px}
#cnt{font-size:52px;line-height:1.05;display:block;margin-top:8px}
.of{font-size:13px;color:#4d483f}
.barw{height:4px;background:#d9d2c3;margin:8px 0}
#bar{height:4px;background:#9b2335;width:0}
#chips{display:flex;flex-wrap:wrap;gap:6px;margin:8px 0 12px;min-height:4px}
.chip{background:none;border:1px solid #9b2335;color:#9b2335;font-size:11px;padding:2px 8px;border-radius:12px;cursor:pointer;text-align:left}
.acc{border-top:1px solid #d9d2c3}
.acch{width:100%;text-align:left;background:none;border:0;padding:10px 0;cursor:pointer;font-size:12px;text-transform:uppercase;letter-spacing:.08em;color:#1d1b18;display:flex;justify-content:space-between}
.acch[aria-expanded=true]{color:#9b2335}
.accb{padding:0 0 12px}
label.lab{display:block;font-size:11px;text-transform:uppercase;letter-spacing:.06em;margin:8px 0 2px;color:#4d483f}
input[type=text],input[type=search],input[type=number],select{width:100%;font:inherit;font-size:15px;padding:6px;border:1px solid #b9b19f;background:#fffdf8;color:#1d1b18}
.hint{font-size:11px;color:#5a554c}
.tabs{display:flex;gap:2px;border-bottom:1px solid #d9d2c3;margin-bottom:18px;flex-wrap:wrap}
.tab{background:none;border:0;border-bottom:3px solid transparent;padding:12px 14px;cursor:pointer;font-size:12px;text-transform:uppercase;letter-spacing:.08em;color:#1d1b18}
.tab[aria-selected=true]{color:#9b2335;border-bottom-color:#9b2335}
h2{font-size:22px;margin:0 0 12px}
h3{font-size:19px;margin:22px 0 4px}
.tiles{display:flex;flex-wrap:wrap;gap:0;border-top:1px solid #d9d2c3;border-bottom:1px solid #d9d2c3;margin-bottom:6px}
.tile{padding:12px 22px 10px 0;margin-right:22px;min-width:150px;flex:1}
.big{font-size:46px;line-height:1.1;display:block}
.tile .sub{font-size:13px;color:#4d483f}
.dot{display:inline-block;width:10px;height:10px;border-radius:50%;margin-right:6px}
.how{font-size:11px;color:#5a554c;margin:4px 0 10px}
.figt{display:flex;gap:10px;align-items:baseline}
table{border-collapse:collapse;width:100%;font-size:15px}
caption{text-align:left;font-size:13px;color:#4d483f;padding:6px 0}
th{font-size:11px;text-transform:uppercase;letter-spacing:.07em;text-align:left;border-bottom:1px solid #1d1b18;padding:6px 8px 6px 0;vertical-align:bottom}
td{border-bottom:1px solid #d9d2c3;padding:6px 8px 6px 0;vertical-align:top}
.n{text-align:right;font-variant-numeric:tabular-nums}
th.n{text-align:right}
tr.row{cursor:pointer}
tr.row:hover td{background:#ece6d8}
tr.exp td{background:#fbf8f1;padding:14px 12px}
.pn{font-family:Georgia,serif;font-size:40px;color:#9b2335;line-height:1}
.full{white-space:pre-wrap;margin:8px 0;max-width:80ch}
.lbl{font-size:13px;margin:4px 0}
.lbl b{font-family:ui-monospace,Menlo,monospace;font-size:11px;text-transform:uppercase;letter-spacing:.06em;font-weight:400;color:#5a554c}
mark{background:#f3d9a4;color:inherit}
button.b{font:inherit;font-size:14px;padding:6px 12px;border:1px solid #1d1b18;background:#fffdf8;color:#1d1b18;cursor:pointer;margin:4px 6px 4px 0}
button.b:hover{background:#ece6d8}
button.b[aria-pressed=true]{background:#9b2335;color:#fff;border-color:#9b2335}
.chartbox{position:relative;height:360px}
.chartbox.s{height:300px}
.checks{list-style:none;padding:0;margin:0}
.checks li{border-bottom:1px solid #d9d2c3;padding:8px 0;font-size:15px}
.mk{font-family:ui-monospace,Menlo,monospace;font-size:11px;text-transform:uppercase;letter-spacing:.06em;display:inline-block;min-width:92px;font-weight:700}
.pass .mk{color:#1b6b3a}.fail .mk{color:#9b2335}.warn .mk{color:#8a5a00}
.fail{background:#f6e3e3}
details{margin-top:4px;font-size:13px}
.cards{list-style:none;padding:0;margin:8px 0}
.card{border-bottom:1px solid #d9d2c3;padding:6px 0}
.cl{display:flex;gap:10px;align-items:baseline;flex-wrap:wrap}
.cl .t{flex:1;min-width:200px;background:none;border:0;text-align:left;font:inherit;font-size:15px;cursor:pointer;padding:2px 0}
.cb{padding:8px 0 8px 8px;border-left:3px solid #9b2335;margin:6px 0 6px 4px}
.chiplab{display:inline-block;border:1px solid #b9b19f;padding:1px 8px;margin:2px 4px 2px 0;font-size:13px;border-radius:12px}
.empty{padding:30px 0;color:#4d483f}
footer{border-top:1px solid #d9d2c3;padding:12px 24px;font-size:11px;color:#4d483f}
.row2{display:flex;gap:8px;align-items:center;flex-wrap:wrap}
.row2 input[type=number]{width:90px}
@media(max-width:900px){.layout{grid-template-columns:1fr}aside{border-right:0;border-bottom:1px solid #d9d2c3}}
</style>
</head>
<body>
<header>
  <div class="mono" id="hlab"></div>
  <h1 id="htitle"></h1>
  <p class="src" id="hsrc"></p>
</header>
<div class="layout">
<aside aria-label="Filters">
  <div class="rh"><span class="mono">Filters</span><button class="lnk" id="clear">Clear all</button></div>
  <span class="big" id="cnt" aria-live="polite">0</span>
  <div class="mono">matching records</div>
  <div class="of" id="of"></div>
  <div class="barw" aria-hidden="true"><div id="bar"></div></div>
  <div id="chips"></div>
  <div id="accs">
    <div class="acc"><button class="acch" aria-expanded="false" data-a="0">01 Keyword <span aria-hidden="true">+</span></button>
      <div class="accb" hidden>
        <label class="lab" for="kw1">Words in text or symbol</label>
        <input type="text" id="kw1" autocomplete="off">
        <div class="hint">literal match, not synonyms</div>
      </div></div>
    <div class="acc"><button class="acch" aria-expanded="false" data-a="1">02 Mechanism, body, type <span aria-hidden="true">+</span></button>
      <div class="accb" hidden>
        <label class="lab" for="fmech">Mechanism</label><select id="fmech"></select>
        <label class="lab" for="fbody">Body or mandate</label><select id="fbody"></select>
        <label class="lab" for="ftype">Type</label><select id="ftype"></select>
        <div id="fstw"><label class="lab" for="fst">Recommending State (UPR)</label><select id="fst"></select></div>
      </div></div>
    <div class="acc"><button class="acch" aria-expanded="false" data-a="2">03 Years and SDG <span aria-hidden="true">+</span></button>
      <div class="accb" hidden>
        <label class="lab" for="fyf">Year from</label><select id="fyf"></select>
        <label class="lab" for="fyt">Year to</label><select id="fyt"></select>
        <label class="lab" for="fsdg">SDG</label><select id="fsdg"></select>
      </div></div>
  </div>
</aside>
<main>
  <div class="tabs" role="tablist" aria-label="Views" id="tabs">
    <button class="tab" role="tab" id="t0" aria-controls="p0" aria-selected="true">01 Overview</button>
    <button class="tab" role="tab" id="t1" aria-controls="p1" aria-selected="false" tabindex="-1">02 Records</button>
    <button class="tab" role="tab" id="t2" aria-controls="p2" aria-selected="false" tabindex="-1">03 Check</button>
    <button class="tab" role="tab" id="t3" aria-controls="p3" aria-selected="false" tabindex="-1">04 Method &amp; export</button>
  </div>

  <section id="p0" role="tabpanel" aria-labelledby="t0">
    <h2>What has the UN said, how much, and when?</h2>
    <div id="tiles1" class="tiles"></div>
    <p class="how" id="how1"></p>
    <div id="tiles2" class="tiles"></div>
    <p class="how" id="how2"></p>
    <div id="statelist" hidden></div>
    <h3 id="f1t"></h3>
    <div class="mono">FIG.01 · click a bar = filter by that theme</div>
    <div id="nomatch1" class="empty" hidden>No records match.</div>
    <div class="chartbox" id="cb1"><canvas id="c1" role="img" aria-label="Bar chart of the ten most frequent themes; the same values are in the table below"></canvas></div>
    <p class="how">How this is computed: each theme on a record counts once; top ten by count, ties alphabetical. A record can carry several themes, so bars add up to more than n.</p>
    <table id="thtable"><caption>Ten most frequent themes, same values as FIG.01</caption>
      <thead><tr><th scope="col">Theme</th><th scope="col" class="n">Records</th><th scope="col" class="n">% of filtered</th><th scope="col">Years</th></tr></thead><tbody></tbody></table>
    <p class="how" id="thnote"></p>
    <h3 id="f2t"></h3>
    <div class="mono">FIG.02</div>
    <div class="chartbox s" id="cb2"><canvas id="c2" role="img" aria-label="Stacked bars of records per year by mechanism"></canvas></div>
    <p class="how">How this is computed: records per year and mechanism in the filtered set; every year from first to last is shown, empty years are gaps. Years are the document's year.</p>
  </section>

  <section id="p1" role="tabpanel" aria-labelledby="t1" hidden>
    <h2>Which paragraph says it, and in which UN document?</h2>
    <label class="lab" for="kw2">Search</label>
    <input type="search" id="kw2" autocomplete="off">
    <div class="hint">literal match, not synonyms · same box as 01 Keyword</div>
    <table style="margin-top:10px"><caption id="cap2"></caption>
      <thead><tr><th scope="col" id="thdate" aria-sort="descending"><button class="lnk" id="sortd" style="font:inherit;text-transform:uppercase;letter-spacing:.07em;font-size:11px;text-decoration:none;color:inherit;padding:0">Date ▼</button></th><th scope="col">Body</th><th scope="col">Symbol</th><th scope="col" class="n">Para.</th><th scope="col">First line</th><th scope="col">Recommending State</th></tr></thead>
      <tbody id="tb2"></tbody></table>
    <p><button class="b" id="more" hidden>Show 50 more</button></p>
    <p class="how">How this is computed: sorted by document date, then body, then paragraph number (numeric), then file order. Click a row to read the full paragraph. Source: OHCHR UHRI.</p>
  </section>

  <section id="p2" role="tabpanel" aria-labelledby="t2" hidden>
    <h2>Can I trust these numbers?</h2>
    <h3 style="margin-top:0">Check this dashboard</h3>
    <div class="mono">How the app checks itself</div>
    <ul class="checks" id="checks"></ul>
    <h3>Check the UN's labels on a random sample</h3>
    <p class="hint" style="font-size:12px">This is your judgement of the UN's labels; nothing is sent anywhere. Ten records are drawn from the current filter.</p>
    <div class="row2">
      <button class="b" id="draw0">Check 10 at random</button>
      <span id="drawmore" hidden class="row2">
        <button class="b" id="draw1">Draw again</button>
        <label class="lab" for="seed" style="margin:0">Seed</label><input type="number" id="seed" value="1" min="0" step="1">
        <button class="b" id="draw2">Draw with this seed</button>
      </span>
    </div>
    <p id="tally" class="mono" aria-live="polite"></p>
    <ul class="cards" id="cards"></ul>
  </section>

  <section id="p3" role="tabpanel" aria-labelledby="t3" hidden>
    <h2>How was this made, and how do I take it with me?</h2>
    <p class="hint" style="font-size:12px">METHOD</p>
    <p>Every number is a loop over the records in your browser; nothing is estimated and no model is called. The headline total is the number of records in the current filter, split by the <code>type</code> value exactly as spelled in the data. Documents are distinct symbols; years run from the earliest to the latest <code>year</code>. Filters combine with AND; the keyword filter needs every word to occur literally in the text or symbol.</p>
    <p>Theme counts add each theme once per record, so a record with three themes adds to three bars; percentages are shares of records, not of labels. The paragraph number is the first number at the start of the text. The recommending State is read only from UPR texts: the parentheses at the very end, accepted when they have no comma and at most 60 characters.</p>
    <p>The themes, SDGs and affected groups are the UN's own labels. The app never changes them; the sample check on tab 03 lets you judge them. <b>Dates</b> are those of the document, not of when a recommendation was made or accepted.</p>
    <div class="row2" style="margin:14px 0">
      <button class="b" id="csv">Download CSV of the current filter</button>
      <button class="b" id="sum">Copy summary</button>
      <span id="msg4" class="hint" aria-live="polite"></span>
    </div>
    <p class="hint" style="font-size:12px">DATA SOURCE</p>
    <p id="srcinfo"></p>
  </section>
</main>
</div>
<footer class="mono" id="foot"></footer>

<script>
(function(){
const D=(window.WORKSHOP_DATA&&WORKSHOP_DATA.uhri)||{};
const R=Array.isArray(D.records)?D.records:[];
const N=R.length;
const COUNTRY=D.country||'(country not given)';
const SDGN=D.sdg_names||{};
const $=id=>document.getElementById(id);
const esc=s=>String(s==null?'':s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const fmt=n=>Number(n).toLocaleString('en-GB');
const UPR='Universal Periodic Review';
const MCOL={'Universal Periodic Review':'#c2410c','Treaty bodies':'#0f766e','Special Procedures':'#7c3aed'};
const PARA=/^(\d{1,3}(?:\.\d{1,3})?)\.?\s/;
const TAIL=/((?:\s*\((?:[^()]|\([^()]*\))*\))+)\s*[;.]?\s*$/;
const GRP=/\((?:[^()]|\([^()]*\))*\)/g;

R.forEach((r,i)=>{
  r._i=i;
  const t=typeof r.text==='string'?r.text:'';
  r._t=t;
  r._th=Array.isArray(r.themes)?r.themes:[];
  r._sd=Array.isArray(r.sdgs)?r.sdgs:[];
  r._tg=Array.isArray(r.sdg_targets)?r.sdg_targets:[];
  r._ap=Array.isArray(r.affected_persons)?r.affected_persons:[];
  const m=PARA.exec(t);
  r._p=m?m[1]:null;
  r._pk=m?m[1].split('.').map(Number):null;
  r._s=null;
  if(r.mechanism===UPR){
    r._s=[];
    const m2=TAIL.exec(t);
    if(m2){
      const g=(m2[1].match(GRP)||[]).map(x=>x.slice(1,-1).trim()).filter(s=>s&&s.indexOf(',')<0&&s.length<=60);
      r._s=g.filter((s,k)=>g.indexOf(s)===k);
    }
  }
  r._lc=(t+' '+(r.symbol||'')).toLowerCase();
  r._fl=firstLine(t);
});
function firstLine(t){
  if(t.length<=120)return t;
  let c=t.slice(0,120);const k=c.lastIndexOf(' ');
  if(k>0)c=c.slice(0,k);
  return c+'…';
}
const uniq=a=>[...new Set(a)];
const years=uniq(R.map(r=>r.year).filter(y=>y!=null)).sort((a,b)=>a-b);
const mechs=uniq(R.map(r=>r.mechanism).filter(Boolean));
const types=uniq(R.map(r=>r.type==null||r.type===''?'(no type)':r.type));
const allSdg=uniq([].concat(...R.map(r=>r._sd))).sort((a,b)=>a-b);
const stCount={};R.forEach(r=>(r._s||[]).forEach(s=>stCount[s]=(stCount[s]||0)+1));
const stList=Object.keys(stCount).sort((a,b)=>stCount[b]-stCount[a]||a.localeCompare(b));
const nDocs=uniq(R.map(r=>r.symbol)).length;
const y0=years.length?years[0]:'–',y1=years.length?years[years.length-1]:'–';
const typeOf=r=>r.type==null||r.type===''?'(no type)':r.type;

const S={tab:0,open:-1,kw:'',mech:'',body:'',type:'',state:'',yf:'',yt:'',sdg:'',themes:[],shown:50,desc:true,exp:new Set(),seed:1,sample:null,sig:'',verd:{},sopen:-1,showStates:false};
let F=[],CH=[],c1=null,c2=null,statCache=null;

/* header & footer */
$('hlab').textContent='UHRI · '+COUNTRY;
$('htitle').textContent='UN human rights recommendations and observations: '+COUNTRY;
$('hsrc').innerHTML='Source: '+(D.source_url?'<a href="'+esc(D.source_url)+'" target="_blank" rel="noopener">'+esc(D.source||'OHCHR UHRI')+'</a>':esc(D.source||'OHCHR UHRI'))+' · '+fmt(N)+' records · '+fmt(nDocs)+' documents · '+y0+'–'+y1+(D.built?' · built '+esc(D.built):'')+' · <span class="hint">dated by document</span>';
$('foot').innerHTML='Built on OHCHR UHRI data · '+fmt(N)+' records · '+(D.source_url?'<a href="'+esc(D.source_url)+'" target="_blank" rel="noopener">source</a>':'source not given');
$('srcinfo').innerHTML=esc(D.title||'')+' · '+esc(D.source||'OHCHR UHRI')+(D.source_url?' · <a href="'+esc(D.source_url)+'" target="_blank" rel="noopener">source page</a>':'')+' · built '+esc(D.built||'(date not given)')+' · n = '+fmt(N)+'. The data carries no licence field; check the terms on the source page before republishing.';

/* controls setup */
function opt(v,l){return '<option value="'+esc(v)+'">'+esc(l)+'</option>'}
$('fmech').innerHTML=opt('','All mechanisms')+mechs.map(m=>opt(m,m+' ('+fmt(R.filter(r=>r.mechanism===m).length)+')')).join('');
$('ftype').innerHTML=opt('','All types')+types.map(t=>opt(t,t+' ('+fmt(R.filter(r=>typeOf(r)===t).length)+')')).join('');
$('fyf').innerHTML=opt('','Earliest')+years.map(y=>opt(y,y)).join('');
$('fyt').innerHTML=opt('','Latest')+years.map(y=>opt(y,y)).join('');
$('fsdg').innerHTML=opt('','All goals')+allSdg.map(g=>opt(g,g+'. '+(SDGN[g]||'(name not given)'))).join('');
$('fst').innerHTML=opt('','All States')+stList.map(s=>opt(s,s+' ('+fmt(stCount[s])+')')).join('');
if(!stList.length)$('fstw').hidden=true;
function fillBody(){
  const rs=S.mech?R.filter(r=>r.mechanism===S.mech):R;
  const c={};rs.forEach(r=>{const b=r.body||'(no body)';c[b]=(c[b]||0)+1});
  $('fbody').innerHTML=opt('','All bodies')+Object.keys(c).sort().map(b=>opt(b,b+' ('+fmt(c[b])+')')).join('');
  if(S.body&&!c[S.body])S.body='';
}
fillBody();

/* filtering */
function filt(){
  const w=S.kw.trim().toLowerCase().split(/\s+/).filter(Boolean);
  const yf=S.yf===''?-Infinity:+S.yf,yt=S.yt===''?Infinity:+S.yt;
  return R.filter(r=>{
    if(S.mech&&r.mechanism!==S.mech)return false;
    if(S.body&&(r.body||'(no body)')!==S.body)return false;
    if(S.type&&typeOf(r)!==S.type)return false;
    if(S.state&&!(r._s&&r._s.includes(S.state)))return false;
    if(r.year<yf||r.year>yt)return false;
    if(S.sdg!==''&&!r._sd.includes(S.sdg))return false;
    for(const t of S.themes)if(!r._th.includes(t))return false;
    for(const x of w)if(r._lc.indexOf(x)<0)return false;
    return true;
  });
}
function chips(){
  const c=[];
  if(S.kw.trim())c.push({l:'Keyword: '+S.kw.trim(),f:()=>{S.kw=''}});
  if(S.mech)c.push({l:'Mechanism: '+S.mech,f:()=>{S.mech='';S.body='';fillBody()}});
  if(S.body)c.push({l:'Body: '+S.body,f:()=>{S.body=''}});
  if(S.type)c.push({l:'Type: '+S.type,f:()=>{S.type=''}});
  if(S.state)c.push({l:'State: '+S.state,f:()=>{S.state=''}});
  if(S.yf!=='')c.push({l:'From '+S.yf,f:()=>{S.yf=''}});
  if(S.yt!=='')c.push({l:'To '+S.yt,f:()=>{S.yt=''}});
  if(S.sdg!=='')c.push({l:'SDG '+S.sdg,f:()=>{S.sdg=''}});
  S.themes.forEach(t=>c.push({l:'Theme: '+t,f:()=>{S.themes=S.themes.filter(x=>x!==t)}}));
  return c;
}
const sig=()=>JSON.stringify([S.kw.trim(),S.mech,S.body,S.type,S.state,S.yf,S.yt,S.sdg,S.themes]);

function update(reset){
  if(reset!==false)S.shown=50;
  F=filt();
  CH=chips();
  syncControls();
  $('cnt').textContent=fmt(F.length);
  $('of').textContent='of '+fmt(N)+' in the file';
  $('bar').style.width=(N?F.length/N*100:0)+'%';
  $('chips').innerHTML=CH.map((c,i)=>'<button class="chip" data-c="'+i+'" aria-label="Remove filter '+esc(c.l)+'">'+esc(c.l.length>40?c.l.slice(0,40)+'…':c.l)+' ×</button>').join('');
  renderTab();
}
function syncControls(){
  $('fmech').value=S.mech;$('fbody').value=S.body;$('ftype').value=S.type;$('fst').value=S.state;
  $('fyf').value=S.yf;$('fyt').value=S.yt;$('fsdg').value=S.sdg;
  [['kw1'],['kw2']].forEach(([id])=>{const e=$(id);if(document.activeElement!==e&&e.value!==S.kw)e.value=S.kw});
  $('kw2').placeholder='Search '+fmt(N)+' records, e.g. torture';
}

/* events: filters */
let tm=null;
function onKw(e){const v=e.target.value;clearTimeout(tm);tm=setTimeout(()=>{S.kw=v;update()},300)}
$('kw1').addEventListener('input',onKw);$('kw2').addEventListener('input',onKw);
$('fmech').onchange=e=>{S.mech=e.target.value;fillBody();update()};
$('fbody').onchange=e=>{S.body=e.target.value;update()};
$('ftype').onchange=e=>{S.type=e.target.value;update()};
$('fst').onchange=e=>{S.state=e.target.value;update()};
function yr(){if(S.yf!==''&&S.yt!==''&&+S.yf>+S.yt){const t=S.yf;S.yf=S.yt;S.yt=t}update()}
$('fyf').onchange=e=>{S.yf=e.target.value;yr()};
$('fyt').onchange=e=>{S.yt=e.target.value;yr()};
$('fsdg').onchange=e=>{S.sdg=e.target.value===''?'':+e.target.value;update()};
$('clear').onclick=()=>{S.kw='';S.mech='';S.body='';S.type='';S.state='';S.yf='';S.yt='';S.sdg='';S.themes=[];fillBody();$('kw1').value='';$('kw2').value='';update()};
$('chips').onclick=e=>{const b=e.target.closest('[data-c]');if(!b)return;CH[+b.dataset.c].f();update()};
document.querySelectorAll('.acch').forEach(b=>b.onclick=()=>{
  const a=+b.dataset.a;S.open=S.open===a?-1:a;
  document.querySelectorAll('.acch').forEach((x,i)=>{x.setAttribute('aria-expanded',S.open===i);x.nextElementSibling.hidden=S.open!==i;x.lastElementChild.textContent=S.open===i?'−':'+'});
});

/* tabs */
const tabs=[0,1,2,3].map(i=>$('t'+i));
function setTab(i,focus){
  S.tab=i;
  tabs.forEach((t,k)=>{t.setAttribute('aria-selected',k===i);t.tabIndex=k===i?0:-1;$('p'+k).hidden=k!==i});
  $('accs').hidden=i>1;
  if(focus)tabs[i].focus();
  renderTab();
}
tabs.forEach((t,i)=>{
  t.onclick=()=>setTab(i);
  t.onkeydown=e=>{
    let k=null;
    if(e.key==='ArrowRight')k=(i+1)%4;else if(e.key==='ArrowLeft')k=(i+3)%4;
    else if(e.key==='Home')k=0;else if(e.key==='End')k=3;
    if(k!==null){e.preventDefault();setTab(k,true)}
  };
});
function renderTab(){
  if(S.tab===0)renderOv();else if(S.tab===1)renderRecs();else if(S.tab===2)renderCheck();else render4();
}

/* helpers */
function themeTop(arr){
  const m=new Map();
  arr.forEach(r=>{new Set(r._th).forEach(t=>{let o=m.get(t);if(!o){o={t,c:0,a:1e9,b:-1e9};m.set(t,o)}o.c++;if(r.year<o.a)o.a=r.year;if(r.year>o.b)o.b=r.year})});
  return [...m.values()].sort((x,y)=>y.c-x.c||x.t.localeCompare(y.t)).slice(0,10);
}
function stateCounts(arr){
  const c={};let none=0,upr=0;
  arr.forEach(r=>{if(r._s){upr++;if(!r._s.length)none++;r._s.forEach(s=>c[s]=(c[s]||0)+1)}});
  return{list:Object.keys(c).sort((a,b)=>c[b]-c[a]||a.localeCompare(b)).map(s=>[s,c[s]]),none,upr};
}
const yrs=(a,b)=>a===b?String(a):a+'–'+b;

/* tab 1 */
function renderOv(){
  const tc={};F.forEach(r=>{const t=typeOf(r);tc[t]=(tc[t]||0)+1});
  const dF=uniq(F.map(r=>r.symbol)).length;
  const fy=F.map(r=>r.year);
  const a=fy.length?Math.min(...fy):'–',b=fy.length?Math.max(...fy):'–';
  $('tiles1').innerHTML=
   '<div class="tile"><span class="big">'+fmt(F.length)+'</span><span class="mono">records</span><div class="sub">'+(Object.keys(tc).length?Object.keys(tc).map(t=>fmt(tc[t])+' '+esc(t)).join(' · '):'none')+'</div></div>'+
   '<div class="tile"><span class="big">'+fmt(dF)+'</span><span class="mono">documents</span></div>'+
   '<div class="tile"><span class="big" style="font-size:38px">'+(F.length?yrs(a,b):'–')+'</span><span class="mono">years</span></div>';
  $('how1').textContent='How this is computed: records = rows in the current filter, split by the type value as spelled in the data; documents = distinct symbols; years = first and last year of those records.';
  const g={};F.forEach(r=>{const m=r.mechanism||'(none)';(g[m]=g[m]||[]).push(r)});
  $('tiles2').innerHTML=mechs.map(m=>{
    const x=g[m]||[];const ly=x.length?Math.max(...x.map(r=>r.year)):'–';
    return '<div class="tile"><span class="big">'+fmt(x.length)+'</span><span class="mono"><span class="dot" style="background:'+(MCOL[m]||'#666')+'"></span>'+esc(m)+'</span><div class="sub">'+fmt(uniq(x.map(r=>r.symbol)).length)+' documents · latest '+ly+' · '+(F.length?(x.length/F.length*100).toFixed(1):'0.0')+'% of filtered'+
      (m===UPR&&stList.length?'<br><button class="lnk" id="seest" aria-expanded="'+S.showStates+'">see the States</button>':'')+'</div></div>';
  }).join('');
  $('how2').textContent='How this is computed: one tile per mechanism, counting records of the current filter; share = records of that mechanism / filtered records.';
  const sl=$('statelist');
  sl.hidden=!(S.showStates&&stList.length);
  if(!sl.hidden){
    const sc=stateCounts(F);
    sl.innerHTML='<h3 style="margin-top:6px">Ten States that made most recommendations to '+esc(COUNTRY)+'</h3><table><caption>Current filter; a recommendation naming several States counts for each</caption><thead><tr><th scope="col">State</th><th scope="col" class="n">Recommendations</th></tr></thead><tbody>'+
      (sc.list.slice(0,10).map(([s,c])=>'<tr><td>'+esc(s)+'</td><td class="n">'+fmt(c)+'</td></tr>').join('')||'<tr><td colspan="2">No UPR recommendations in this filter.</td></tr>')+
      '</tbody></table><p class="how">How this is computed: State names read from the parentheses ending each UPR text; '+fmt(sc.none)+' of '+fmt(sc.upr)+' UPR records in this filter have no State found. A count of recommendations, not of influence.</p>';
  }
  const top=themeTop(F);
  $('f1t').textContent='Ten most frequent themes among '+fmt(F.length)+' filtered records';
  $('f2t').textContent='Records per year by mechanism, '+fmt(F.length)+' filtered records';
  $('nomatch1').hidden=F.length>0;
  $('cb1').hidden=!F.length;$('cb2').hidden=!F.length;
  $('thtable').querySelector('tbody').innerHTML=top.map(r=>'<tr><td>'+esc(r.t)+'</td><td class="n">'+fmt(r.c)+'</td><td class="n">'+(r.c/F.length*100).toFixed(1)+'%</td><td>'+yrs(r.a,r.b)+'</td></tr>').join('')||'<tr><td colspan="4">No records match.</td></tr>';
  $('thnote').textContent='A record can carry several themes, so bars add up to more than n. A label whose years are far from the rest may be a legacy label: judge a sample on tab 03. Source: OHCHR UHRI labels, unchanged.';
  if(c1){c1.destroy();c1=null}
  if(c2){c2.destroy();c2=null}
  if(!F.length||!window.Chart)return;
  c1=new Chart($('c1'),{type:'bar',
    data:{labels:top.map(r=>r.t),datasets:[{data:top.map(r=>r.c),backgroundColor:'rgba(155,35,51,.8)'}]},
    options:{indexAxis:'y',responsive:true,maintainAspectRatio:false,animation:false,layout:{padding:{right:50}},
      plugins:{legend:{display:false},tooltip:{callbacks:{title:i=>top[i[0].dataIndex].t}}},
      scales:{x:{grid:{display:false},ticks:{display:false},border:{display:false},grace:'8%'},y:{grid:{display:false},ticks:{color:'#1d1b18',font:{size:13},callback:function(v){const l=this.getLabelForValue(v);return l.length>42?l.slice(0,41)+'…':l}}}},
      onClick:(e,els)=>{if(els.length){const t=top[els[0].index].t;if(!S.themes.includes(t)){S.themes.push(t);update()}}},
      onHover:(e,els)=>{e.native.target.style.cursor=els.length?'pointer':'default'}},
    plugins:[{id:'val',afterDatasetsDraw(c){const x=c.ctx;c.getDatasetMeta(0).data.forEach((bar,i)=>{x.save();x.fillStyle='#1d1b18';x.font='13px ui-monospace,Menlo,monospace';x.textBaseline='middle';x.fillText(fmt(c.data.datasets[0].data[i]),bar.x+6,bar.y);x.restore()})})}]});
  const ys=[];for(let y=a;y<=b;y++)ys.push(y);
  const ms=mechs.concat(F.some(r=>!r.mechanism)?['(none)']:[]);
  const cnt={};F.forEach(r=>{const k=(r.mechanism||'(none)')+'|'+r.year;cnt[k]=(cnt[k]||0)+1});
  c2=new Chart($('c2'),{type:'bar',
    data:{labels:ys,datasets:ms.map(m=>({label:m,data:ys.map(y=>cnt[m+'|'+y]||0),backgroundColor:MCOL[m]||'#666'}))},
    options:{responsive:true,maintainAspectRatio:false,animation:false,
      plugins:{legend:{position:'top',labels:{color:'#1d1b18',boxWidth:12}}},
      scales:{x:{stacked:true,grid:{display:false},ticks:{color:'#1d1b18',autoSkip:false,maxRotation:90,font:{size:11}}},y:{stacked:true,grid:{color:'#e6dfd0'},ticks:{color:'#1d1b18'},beginAtZero:true}}}});
}
$('tiles2').onclick=e=>{if(e.target.id==='seest'){S.showStates=!S.showStates;renderOv()}};

/* tab 2 */
function cmp(a,b){
  if(a.date!==b.date)return a.date<b.date?1:-1;
  const bb=(a.body||'').localeCompare(b.body||'');if(bb)return bb;
  if(a._pk&&b._pk){if(a._pk[0]!==b._pk[0])return a._pk[0]-b._pk[0];const x=a._pk[1]||0,y=b._pk[1]||0;if(x!==y)return x-y}
  else if(a._pk)return -1;else if(b._pk)return 1;
  return a._i-b._i;
}
function hl(t,words){
  let s=esc(t);
  words.forEach(w=>{const e=esc(w).replace(/[.*+?^${}()|[\]\\]/g,'\\$&');if(e)s=s.replace(new RegExp(e,'gi'),m=>'<mark>'+m+'</mark>')});
  return s;
}
function cite(r){return r.symbol+(r._p?', para. '+r._p:'')}
function renderRecs(){
  const words=S.kw.trim().toLowerCase().split(/\s+/).filter(Boolean);
  const rows=F.slice().sort((a,b)=>S.desc?cmp(a,b):cmp(b,a));
  const show=rows.slice(0,S.shown);
  $('cap2').textContent=F.length?('Showing '+fmt(show.length)+' of '+fmt(F.length)+' matching records, '+(S.desc?'newest first':'oldest first')):'No records match.';
  $('sortd').textContent='Date '+(S.desc?'▼':'▲');
  $('thdate').setAttribute('aria-sort',S.desc?'descending':'ascending');
  $('tb2').innerHTML=show.map(r=>{
    const open=S.exp.has(r._i);
    let h='<tr class="row" data-i="'+r._i+'" tabindex="0" aria-expanded="'+open+'"><td>'+esc(r.date||'')+'</td><td>'+esc(r.body||'')+'</td><td><a href="'+esc(r.doc_url||'#')+'" target="_blank" rel="noopener">'+esc(r.symbol)+'</a></td><td class="n">'+(r._p?esc(r._p):'–')+'</td><td>'+hl(r._fl,words)+'</td><td>'+(r._s?(r._s.length?esc(r._s.join(', ')):'<span class="hint">State not found</span>'):'–')+'</td></tr>';
    if(open)h+=expRow(r,words);
    return h;
  }).join('');
  $('more').hidden=rows.length<=S.shown;
}
function expRow(r,words){
  const sd=r._sd.map(g=>g+' '+(SDGN[g]||'')).join('; ');
  const L=(k,v)=>v?'<div class="lbl"><b>'+k+'</b> '+esc(v)+'</div>':'';
  return '<tr class="exp"><td colspan="6">'+(r._p?'<div class="pn">'+esc(r._p)+'</div>':'')+
   '<div class="full">'+hl(r._t,words)+'</div>'+
   (r.section?L('Section',r.section):'')+
   L('Themes',r._th.join('; ')||'not labelled')+L('SDGs',sd||'not labelled')+
   (r._tg.length?L('SDG targets',r._tg.join('; ')):'')+L('Affected persons',r._ap.join('; ')||'not labelled')+
   '<button class="b" data-copy="'+r._i+'" data-l="Copy citation'+(r._p?'':' (no paragraph number in this extract)')+'">Copy citation'+(r._p?'':' (no paragraph number in this extract)')+'</button>'+
   '<a class="b" style="display:inline-block;text-decoration:none;font-size:14px;padding:6px 12px;border:1px solid #1d1b18;color:#1d1b18" href="'+esc(r.doc_url||'#')+'" target="_blank" rel="noopener">Open the UN document</a></td></tr>';
}
function copyText(t,btn,label){
  const done=()=>{if(!btn)return;btn.textContent='Copied';setTimeout(()=>{btn.textContent=label||btn.dataset.l||''},2000)};
  if(navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText(t).then(done,()=>fb())}else fb();
  function fb(){const a=document.createElement('textarea');a.value=t;document.body.appendChild(a);a.select();try{document.execCommand('copy')}catch(e){}a.remove();done()}
}
function togRow(tr){const i=+tr.dataset.i;S.exp.has(i)?S.exp.delete(i):S.exp.add(i);renderRecs();const n=$('tb2').querySelector('tr[data-i="'+i+'"]');if(n)n.focus()}
$('tb2').onclick=e=>{
  const c=e.target.closest('[data-copy]');
  if(c){const r=R[+c.dataset.copy];copyText(cite(r),c);return}
  if(e.target.closest('a'))return;
  const tr=e.target.closest('tr.row');if(tr)togRow(tr);
};
$('tb2').onkeydown=e=>{if((e.key==='Enter'||e.key===' ')&&e.target.matches('tr.row')){e.preventDefault();togRow(e.target)}};
$('more').onclick=()=>{S.shown+=50;renderRecs()};
$('sortd').onclick=()=>{S.desc=!S.desc;renderRecs()};

/* tab 3 */
function sumOf(key){const m={};R.forEach(r=>{const k=r[key]==null?'(missing)':r[key];m[k]=(m[k]||0)+1});return Object.values(m).reduce((a,b)=>a+b,0)}
function runChecks(){
  const out=[];
  const add=(n,d,st,extra)=>out.push({n,d,st,extra:extra||''});
  const cn=Number(D.count);
  add('Record count','records.length = '+fmt(N)+' · count in the file = '+(isNaN(cn)?'(not a number)':fmt(cn)),N===cn?'pass':'fail');
  const pm=sumOf('mechanism'),pb=sumOf('body'),py=sumOf('year');
  add('Partitions','records per mechanism sum to '+fmt(pm)+', per body to '+fmt(pb)+', per year to '+fmt(py)+'; expected '+fmt(N),(pm===N&&pb===N&&py===N)?'pass':'fail');
  const tm=types.reduce((a,t)=>a+R.filter(r=>typeOf(r)===t).length,0);
  add('Type partition','counts per type sum to '+fmt(tm)+'; headline total '+fmt(N),tm===N?'pass':'fail');
  const top=themeTop(F);
  let bad=[];top.forEach(x=>{const c=F.filter(r=>r._th.includes(x.t)).length;if(c!==x.c)bad.push(x.t+': bar '+x.c+' vs recount '+c)});
  const mx=top.length?top[0].c:0;
  add('Chart against table','the '+top.length+' bars and table rows (same values) recounted by a second loop over '+fmt(F.length)+' filtered records; largest bar '+fmt(mx)+' ≤ '+fmt(F.length),(!bad.length&&mx<=F.length)?'pass':'fail',bad.join('; '));
  const lb=R.filter(r=>{const s=(r.symbol||'').toLowerCase();let u=r.doc_url||'';try{u=decodeURIComponent(u)}catch(e){}u=u.toLowerCase();return !(u.startsWith('https://docs.un.org/')&&u.endsWith(s))});
  add('Links','doc_url starts with https://docs.un.org/ and ends with the symbol: '+fmt(N-lb.length)+' of '+fmt(N)+' pass',lb.length?'fail':'pass',lb.length?'<details><summary>'+fmt(lb.length)+' records that fail</summary>'+lb.slice(0,50).map(r=>esc(r.symbol)+' → '+esc(r.doc_url)).join('<br>')+'</details>':'');
  const pp=mechs.map(m=>{const x=R.filter(r=>r.mechanism===m);const k=x.filter(r=>r._p).length;return{m,k,n:x.length}});
  const uprBad=pp.some(p=>p.m===UPR&&p.k<p.n);
  add('Paragraph numbers','share of records with a number found: '+pp.map(p=>p.m+' '+fmt(p.k)+'/'+fmt(p.n)+' ('+(p.n?(p.k/p.n*100).toFixed(0):0)+'%)').join(' · ')+'. UPR is expected at 100%',uprBad?'warn':'pass');
  const up=R.filter(r=>r._s),nf=up.filter(r=>!r._s.length);
  add('States found','UPR records with at least one State: '+fmt(up.length-nf.length)+' of '+fmt(up.length),nf.length?'warn':'pass',nf.length?'<details><summary>'+fmt(nf.length)+' UPR records without a State</summary>'+nf.slice(0,60).map(r=>esc(r.symbol)+' · …'+esc(r._t.slice(-70))).join('<br>')+'</details>':'');
  const ids=uniq(R.map(r=>r.id)).length;
  const tx={};R.forEach(r=>tx[r._t]=(tx[r._t]||0)+1);
  const dup=Object.values(tx).filter(c=>c>1).reduce((a,c)=>a+c-1,0);
  add('Duplicates','distinct id = '+fmt(ids)+' of '+fmt(N)+' records · duplicate texts: '+fmt(dup),ids===N?'pass':'fail');
  add('Gaps','not labelled: '+fmt(R.filter(r=>!r._th.length).length)+' without themes · '+fmt(R.filter(r=>!r._sd.length).length)+' without SDGs · '+fmt(R.filter(r=>!r._ap.length).length)+' without affected persons','pass');
  return out;
}
function renderCheck(){
  $('checks').innerHTML=runChecks().map(c=>'<li class="'+c.st+'"><span class="mk">'+(c.st==='pass'?'✓ pass':c.st==='fail'?'check failed':'warning')+'</span> <b>'+esc(c.n)+'.</b> '+esc(c.d)+(c.st==='fail'&&c.extra&&c.extra.indexOf('<')<0?' — '+esc(c.extra):'')+(c.extra&&c.extra.indexOf('<')>=0?c.extra:'')+'</li>').join('');
  if(S.sample&&S.sig!==sig())drawSample(S.seed);
  renderSample();
}
function mulberry32(a){return function(){a|=0;a=a+0x6D2B79F5|0;let t=Math.imul(a^a>>>15,1|a);t=t+Math.imul(t^t>>>7,61|t)^t;return((t^t>>>14)>>>0)/4294967296}}
function drawSample(seed){
  S.seed=seed;const rnd=mulberry32(seed);
  const idx=F.map(r=>r._i);const k=Math.min(10,idx.length);
  for(let i=0;i<k;i++){const j=i+Math.floor(rnd()*(idx.length-i));const t=idx[i];idx[i]=idx[j];idx[j]=t}
  S.sample=idx.slice(0,k);S.sig=sig();S.verd={};S.sopen=-1;
  $('seed').value=seed;
}
function renderSample(focusKey){
  $('drawmore').hidden=!S.sample;$('draw0').hidden=!!S.sample;
  if(!S.sample){$('tally').textContent='';$('cards').innerHTML='';return}
  const v=Object.values(S.verd);
  const cc=k=>v.filter(x=>x===k).length;
  $('tally').textContent='Themes (your judgement): '+cc('fit')+' fit, '+cc('no')+' don\'t, '+cc('unsure')+' unsure of '+v.length+' judged · '+S.sample.length+' drawn · seed '+S.seed;
  if(!S.sample.length){$('cards').innerHTML='<li class="empty">No records match.</li>';return}
  $('cards').innerHTML=S.sample.map((ri,k)=>{
    const r=R[ri],o=S.sopen===k,vd=S.verd[ri];
    const vl=vd==='fit'?'Fits':vd==='no'?"Doesn't fit":vd==='unsure'?'Unsure':'not judged';
    return '<li class="card"><div class="cl"><a href="'+esc(r.doc_url||'#')+'" target="_blank" rel="noopener">'+esc(r.symbol)+'</a><span class="hint">'+(r._p?'para. '+esc(r._p):'no para. number')+'</span><button class="t" data-so="'+k+'" aria-expanded="'+o+'">'+esc(r._fl)+'</button><span class="hint">'+vl+'</span></div>'+
     (o?'<div class="cb"><div class="full">'+esc(r._t)+'</div><div class="lbl"><b>Themes</b></div>'+(r._th.length?r._th.map(t=>'<span class="chiplab">'+esc(t)+'</span>').join(''):'<span class="hint">not labelled</span>')+'<div>'+
      [['fit','Fits'],['no',"Doesn't fit"],['unsure','Unsure']].map(([x,l])=>'<button class="b" data-v="'+ri+'" data-x="'+x+'" aria-pressed="'+(vd===x)+'">'+l+'</button>').join('')+'</div></div>':'')+'</li>';
  }).join('');
  if(focusKey){const b=$('cards').querySelector('[data-so="'+focusKey+'"]');if(b)b.focus()}
}
$('cards').onclick=e=>{
  const so=e.target.closest('[data-so]');
  if(so){const k=+so.dataset.so;S.sopen=S.sopen===k?-1:k;renderSample(k);return}
  const vb=e.target.closest('[data-v]');
  if(vb){S.verd[vb.dataset.v]=vb.dataset.x;renderSample();const n=$('cards').querySelector('[data-v="'+vb.dataset.v+'"][data-x="'+vb.dataset.x+'"]');if(n)n.focus()}
};
$('draw0').onclick=()=>{drawSample(1+Math.floor(Math.random()*999999));renderSample()};
$('draw1').onclick=()=>{drawSample(1+Math.floor(Math.random()*999999));renderSample()};
$('draw2').onclick=()=>{const s=parseInt($('seed').value,10);drawSample(isNaN(s)?1:s);renderSample()};

/* tab 4 */
function render4(){}
const fdesc=()=>CH.length?CH.map(c=>c.l).join('; '):'none';
function csvq(v){return '"'+String(v==null?'':v).replace(/"/g,'""')+'"'}
$('csv').onclick=()=>{
  const rows=F.slice().sort(cmp);
  let o='\ufeff# Country: '+COUNTRY+'\n# Source: '+(D.source||'')+' '+(D.source_url||'')+'\n# Built: '+(D.built||'')+'\n# Filters applied: '+fdesc().replace(/\n/g,' ')+'\n# Rows: '+rows.length+'\n';
  o+=['date','mechanism','body','type','symbol','paragraph','recommending_states','section','first_line','text','themes','sdgs','sdg_targets','affected_persons','doc_url'].join(',')+'\n';
  rows.forEach(r=>{o+=[r.date,r.mechanism,r.body,r.type,r.symbol,r._p||'',r._s?r._s.join('; '):'',r.section||'',r._fl,r._t,r._th.join('; '),r._sd.map(g=>g+' '+(SDGN[g]||'')).join('; '),r._tg.join('; '),r._ap.join('; '),r.doc_url].map(csvq).join(',')+'\n'});
  const u=URL.createObjectURL(new Blob([o],{type:'text/csv;charset=utf-8'}));
  const a=document.createElement('a');a.href=u;a.download='uhri-'+COUNTRY.toLowerCase().replace(/[^a-z0-9]+/g,'-')+'-filtered.csv';document.body.appendChild(a);a.click();a.remove();
  setTimeout(()=>URL.revokeObjectURL(u),5000);
  $('msg4').textContent=fmt(rows.length)+' rows prepared.';
};
$('sum').onclick=()=>{
  const tc={};F.forEach(r=>{const t=typeOf(r);tc[t]=(tc[t]||0)+1});
  const mc={};F.forEach(r=>{const m=r.mechanism||'(none)';mc[m]=(mc[m]||0)+1});
  const fy=F.map(r=>r.year);
  const top=themeTop(F);
  const t=COUNTRY+': '+fmt(F.length)+' of '+fmt(N)+' records in OHCHR UHRI ('+(D.source||'')+', built '+(D.built||'n/a')+'), from '+fmt(uniq(F.map(r=>r.symbol)).length)+' documents, '+(fy.length?yrs(Math.min(...fy),Math.max(...fy)):'no years')+' (dated by document). Filters: '+fdesc()+'. By type: '+Object.keys(tc).map(k=>fmt(tc[k])+' '+k).join(', ')+'. By mechanism: '+Object.keys(mc).map(k=>fmt(mc[k])+' '+k).join(', ')+'. Ten most frequent themes (a record can carry several): '+top.map((x,i)=>(i+1)+'. '+x.t+' ('+fmt(x.c)+', '+(x.c/F.length*100).toFixed(1)+'%, '+yrs(x.a,x.b)+')').join('; ')+'.';
  copyText(t,$('sum'),'Copy summary');
  $('msg4').textContent='';
};

setTab(0);
update();
})();
</script>
</body>
</html>
```