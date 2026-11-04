I built the four-tab dashboard for Kenya with the filter rail, the self-check panel and the random label check. It calls no model and makes no network request, so the only thing that leaves the page is the clipboard write on "Copy". I have not run it against your file, so please check the numbers on the Check tab first.

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>UN human rights recommendations dashboard</title>
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>
[hidden]{display:none!important}
*{box-sizing:border-box}
body{margin:0;background:#f4f0e8;color:#1d1b18;font:16px/1.5 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif}
a{color:#9b2335}
:focus-visible{outline:3px solid #9b2335;outline-offset:2px}
.mono{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:11.5px;letter-spacing:.08em;text-transform:uppercase}
.serif{font-family:Georgia,"Times New Roman",serif}
header.top{padding:14px 24px 10px;border-bottom:1px solid #d9d2c3}
header.top h1{font:400 30px/1.15 Georgia,"Times New Roman",serif;margin:4px 0 6px}
.meta{font-size:14px;color:#4a463f}
nav[role=tablist]{display:flex;gap:4px;padding:0 24px;border-bottom:1px solid #d9d2c3;flex-wrap:wrap}
nav button{background:none;border:0;border-bottom:3px solid transparent;padding:10px 14px;cursor:pointer;color:#1d1b18}
nav button[aria-selected=true]{border-bottom-color:#9b2335;color:#9b2335;font-weight:700}
.layout{display:grid;grid-template-columns:260px minmax(0,1fr);gap:0;min-height:60vh}
aside{border-right:1px solid #d9d2c3;padding:16px 18px}
main{padding:18px 24px 30px;min-width:0}
.rhead{display:flex;justify-content:space-between;align-items:center}
.linkbtn{background:none;border:0;color:#9b2335;text-decoration:underline;cursor:pointer;padding:2px;font:inherit}
.big{font:400 52px/1 Georgia,"Times New Roman",serif}
#matchn{margin-top:10px}
.bar{height:4px;background:#d9d2c3;margin:6px 0 10px}.bar i{display:block;height:100%;background:#9b2335}
.chips{display:flex;flex-wrap:wrap;gap:5px;margin-bottom:10px}
.chip{border:1px solid #9b2335;color:#9b2335;background:#fff8;border-radius:12px;padding:1px 9px;font-size:13px;cursor:pointer}
.chip.plain{border-color:#d9d2c3;color:#1d1b18;cursor:default}
.sec{border-top:1px solid #d9d2c3}
.sec>button{width:100%;text-align:left;background:none;border:0;padding:10px 0;cursor:pointer;display:flex;justify-content:space-between}
.sec .body{padding:0 0 12px}
.sec label{display:block;font-size:13px;margin:8px 0 2px}
input,select{font:inherit;width:100%;padding:6px;border:1px solid #bdb4a1;background:#fffdf8;color:#1d1b18}
.hint{font-size:12px;color:#5b564c;margin-top:4px}
.row2{display:grid;grid-template-columns:1fr 1fr;gap:8px}
h2.q{font:400 24px/1.2 Georgia,serif;margin:0 0 14px}
h3.fig{font:400 19px/1.25 Georgia,serif;margin:26px 0 2px}
.note{font-size:13px;color:#5b564c;margin:4px 0 8px}
.note b{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:11px;letter-spacing:.06em;text-transform:uppercase;font-weight:400;color:#1d1b18}
.tiles{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:0;border-top:1px solid #d9d2c3;border-left:1px solid #d9d2c3}
.tile{padding:12px 14px;border-right:1px solid #d9d2c3;border-bottom:1px solid #d9d2c3}
.tile .big{font-size:44px}
.tile .sub{font-size:13px;color:#4a463f}
.dot{display:inline-block;width:10px;height:10px;border-radius:50%;margin-right:6px}
table{border-collapse:collapse;width:100%;font-size:15px}
caption{text-align:left;font-size:13px;color:#4a463f;padding:4px 0 6px}
th,td{border-bottom:1px solid #d9d2c3;padding:6px 8px;text-align:left;vertical-align:top}
th{font:600 11.5px ui-monospace,Menlo,Consolas,monospace;letter-spacing:.06em;text-transform:uppercase;background:none}
th.n,td.n{text-align:right;font-variant-numeric:tabular-nums}
th button{all:unset;cursor:pointer;color:#9b2335;text-decoration:underline}
tr.rec{cursor:pointer}tr.rec:hover{background:#ece6d8}
tr.open td.first{font-weight:600}
td.detail{background:#fbf8f1;padding:14px 18px}
.pnum{font:400 44px/1 Georgia,serif;color:#9b2335}
.fulltext{white-space:pre-wrap;margin:8px 0;max-width:80ch}
.lbl{margin:6px 0;font-size:14px}.lbl .mono{margin-right:6px;color:#5b564c}
.btn{background:#1d1b18;color:#f4f0e8;border:0;padding:7px 12px;cursor:pointer;font:inherit;font-size:14px;margin:4px 6px 4px 0}
.btn.alt{background:none;color:#1d1b18;border:1px solid #1d1b18}
.btn.sel{background:#9b2335;color:#fff;border-color:#9b2335}
mark{background:#f3d9a4}
.muted{color:#7a7467}
.checks{list-style:none;padding:0;margin:0}
.checks li{border-bottom:1px solid #d9d2c3;padding:8px 0}
.ok{color:#1d6b3a;font-weight:700}.warn{color:#8a5a00;font-weight:700}.fail{color:#9b2335;font-weight:700}
details summary{cursor:pointer;color:#5b564c;font-size:13px}
.card{border-bottom:1px solid #d9d2c3}
.cardline{display:flex;gap:10px;align-items:baseline;padding:8px 0;flex-wrap:wrap}
.cardline button.t{all:unset;cursor:pointer;flex:1;min-width:200px}
.cardline button.t:focus-visible{outline:3px solid #9b2335}
.cardbody{padding:4px 0 14px 12px;border-left:3px solid #9b2335}
pre#sumbox{white-space:pre-wrap;background:#fffdf8;border:1px solid #d9d2c3;padding:10px;font-size:13px}
.chartbox{position:relative;width:100%}
footer{border-top:1px solid #d9d2c3;padding:12px 24px;color:#4a463f}
@media(max-width:800px){.layout{grid-template-columns:1fr}aside{border-right:0;border-bottom:1px solid #d9d2c3}}
</style>
</head>
<body>
<header class="top">
  <div class="mono" id="hlabel"></div>
  <h1 id="htitle"></h1>
  <div class="meta" id="hmeta"></div>
</header>
<nav role="tablist" aria-label="Dashboard questions" id="tabs">
  <button role="tab" id="tab1" aria-selected="true" aria-controls="p1" class="mono">01 Overview</button>
  <button role="tab" id="tab2" aria-selected="false" aria-controls="p2" tabindex="-1" class="mono">02 Records</button>
  <button role="tab" id="tab3" aria-selected="false" aria-controls="p3" tabindex="-1" class="mono">03 Check</button>
  <button role="tab" id="tab4" aria-selected="false" aria-controls="p4" tabindex="-1" class="mono">04 Method &amp; export</button>
</nav>
<div class="layout">
<aside>
  <div class="rhead"><span class="mono">Filters</span><button class="linkbtn" id="clearall">Clear all</button></div>
  <div id="matchn" class="big" aria-live="polite"></div>
  <div class="note" id="matchof"></div>
  <div class="bar"><i id="sharebar" style="width:100%"></i></div>
  <div class="chips" id="chips"></div>
  <div id="filters">
    <div class="sec"><button class="mono" aria-expanded="false" data-sec="0"><span>01 Keyword</span><span>+</span></button>
      <div class="body" hidden><label for="kw1">Words in text or symbol</label><input id="kw1" type="search" autocomplete="off"><div class="hint mono">literal match, not synonyms</div></div></div>
    <div class="sec"><button class="mono" aria-expanded="false" data-sec="1"><span>02 Mechanism, body, type</span><span>+</span></button>
      <div class="body" hidden>
        <label for="fmech">Mechanism</label><select id="fmech"></select>
        <label for="fbody">Body or mandate</label><select id="fbody"></select>
        <label for="ftype">Type</label><select id="ftype"></select>
        <div id="statewrap"><label for="fstate">Recommending State (UPR)</label><select id="fstate"></select></div>
      </div></div>
    <div class="sec"><button class="mono" aria-expanded="false" data-sec="2"><span>03 Years and SDG</span><span>+</span></button>
      <div class="body" hidden>
        <div class="row2"><div><label for="yfrom">From</label><select id="yfrom"></select></div><div><label for="yto">To</label><select id="yto"></select></div></div>
        <label for="fsdg">SDG</label><select id="fsdg"></select>
      </div></div>
  </div>
</aside>
<main>
<section id="p1" role="tabpanel" aria-labelledby="tab1">
  <h2 class="q">What has the UN said, how much, and when?</h2>
  <div class="tiles" id="tiles1"></div>
  <div class="note"><b>How this is computed</b> Every tile is a loop over the filtered records; documents are distinct symbols.</div>
  <div id="statelist" hidden></div>
  <div id="mtiles" class="tiles" style="margin-top:14px"></div>
  <div class="note"><b>How this is computed</b> Records, distinct symbols and latest year per mechanism in the filtered set; share = records / filtered records.</div>
  <h3 class="fig" id="fig1t"></h3>
  <div class="mono muted">FIG.01 · click a bar to filter</div>
  <div id="fig1empty" class="note" hidden>No records match.</div>
  <div class="chartbox" id="c1box" style="height:380px"><canvas id="c1" aria-label="Ten most frequent themes"></canvas></div>
  <table id="themetable"></table>
  <div class="note"><b>How this is computed</b> Each theme counts once per record carrying it; a record can carry several themes, so bars add up to more than n. Percent = count / filtered records. Source: OHCHR UHRI labels, unchanged.</div>
  <h3 class="fig" id="fig2t"></h3>
  <div class="mono muted">FIG.02</div>
  <div id="fig2empty" class="note" hidden>No records match.</div>
  <div class="chartbox" id="c2box" style="height:320px"><canvas id="c2" aria-label="Records per year by mechanism"></canvas></div>
  <div class="note"><b>How this is computed</b> Records per document year and mechanism in the filtered set; years without records show as gaps. Dated by document.</div>
</section>
<section id="p2" role="tabpanel" aria-labelledby="tab2" hidden>
  <h2 class="q">Which paragraph says it, and in which UN document?</h2>
  <label for="kw2" class="mono">Search</label>
  <input id="kw2" type="search" autocomplete="off">
  <div class="hint mono">literal match, not synonyms · click a row to open it</div>
  <table id="rectable" style="margin-top:10px"></table>
  <div style="margin:10px 0"><button class="btn alt" id="more" hidden>Show 50 more</button></div>
  <div class="note"><b>How this is computed</b> Rows match all filters. Paragraph number = first number at the start of the text. Recommending State = the parentheses ending a UPR text. Source: OHCHR UHRI.</div>
</section>
<section id="p3" role="tabpanel" aria-labelledby="tab3" hidden>
  <h2 class="q">Can I trust these numbers?</h2>
  <h3 class="fig" style="margin-top:0">Check this dashboard</h3>
  <div class="mono muted">How the app checks itself</div>
  <ul class="checks" id="checks"></ul>
  <h3 class="fig">Random-sample label check</h3>
  <p class="note">This is your judgement of the UN's labels; nothing is sent anywhere.</p>
  <div id="samplectl"></div>
  <div id="tally" class="note"></div>
  <div id="cards"></div>
</section>
<section id="p4" role="tabpanel" aria-labelledby="tab4" hidden>
  <h2 class="q">How was this made, and how do I take it with me?</h2>
  <div id="method"></div>
  <div style="margin:14px 0"><button class="btn" id="dl">Download CSV of the current filter</button><button class="btn alt" id="copysum">Copy summary</button> <span id="copied4" class="note" hidden>Copied</span></div>
  <pre id="sumbox"></pre>
  <div class="note" id="srcline"></div>
</section>
</main>
</div>
<footer class="mono" id="foot"></footer>

<script>
(function(){
const D=window.WORKSHOP_DATA.uhri||{};
const COUNTRY=D.country||"the country";
const SDGN=D.sdg_names||{};
const MECHCOL={"Universal Periodic Review":"#c2410c","Treaty bodies":"#0f766e","Special Procedures":"#7c3aed"};
const fmt=n=>Number(n).toLocaleString("en-GB");
const esc=s=>String(s==null?"":s).replace(/[&<>"]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
const $=id=>document.getElementById(id);
const STATE_RUN=/((?:\s*\((?:[^()]|\([^()]*\))*\))+)\s*[;.]?\s*$/;
const STATE_GRP=/\((?:[^()]|\([^()]*\))*\)/g;
const PARA=/^(\d{1,3}(?:\.\d{1,3})?)\.?\s/;
const UPR="Universal Periodic Review";

const R=(D.records||[]).map((r,i)=>{
  const t=r.text||"";
  const pm=t.match(PARA);
  let states=null;
  if(r.mechanism===UPR){
    states=[];
    const m=t.match(STATE_RUN);
    if(m){
      const gs=(m[1].match(STATE_GRP)||[]).map(g=>g.slice(1,-1).trim());
      if(gs.length&&gs.every(g=>g&&g.indexOf(",")<0&&g.length<=60)) states=gs;
    }
  }
  let first=t;
  if(t.length>120){const c=t.slice(0,120);const sp=c.lastIndexOf(" ");first=(sp>20?c.slice(0,sp):c)+"…";}
  return Object.assign({},r,{_i:i,_para:pm?pm[1]:null,_states:states,_first:first,_lc:(t+" "+(r.symbol||"")).toLowerCase(),
    themes:r.themes||[],sdgs:r.sdgs||[],sdg_targets:r.sdg_targets||[],affected_persons:r.affected_persons||[]});
});
const N=R.length;
const years=[...new Set(R.map(r=>r.year).filter(y=>y!=null))].sort((a,b)=>a-b);
const symbols=new Set(R.map(r=>r.symbol));
const mechs=[...new Set(R.map(r=>r.mechanism))].sort();
const types=[...new Set(R.map(r=>r.type))].sort();
const countBy=(arr,f)=>{const o={};arr.forEach(r=>{const k=f(r);o[k]=(o[k]||0)+1});return o};
const stateCounts={};R.forEach(r=>(r._states||[]).forEach(s=>stateCounts[s]=(stateCounts[s]||0)+1));
const hasStates=Object.keys(stateCounts).length>0;
const sdgsPresent=[...new Set(R.flatMap(r=>r.sdgs))].sort((a,b)=>a-b);

const F0={kw:"",mech:"",body:"",type:"",state:"",yf:years[0],yt:years[years.length-1],sdg:"",themes:[]};
let F=Object.assign({},F0,{themes:[]});
let filtered=[],tab=1,shown=50,dirDesc=true,openRows=new Set(),openSec=null,charts={},sample=null;

/* header */
$("hlabel").textContent="UHRI · "+COUNTRY;
$("htitle").textContent="UN human rights recommendations and observations: "+COUNTRY;
$("hmeta").innerHTML=`Source: ${D.source_url?`<a href="${esc(D.source_url)}" target="_blank" rel="noopener">${esc(D.source||"source")}</a>`:esc(D.source||"not given")} · ${fmt(N)} records · ${fmt(symbols.size)} documents · ${years.length?years[0]+"–"+years[years.length-1]:"no years"} · built ${esc(D.built||"date not given")} · <i>dated by document</i>`;
$("foot").innerHTML=`Built on OHCHR UHRI data · ${fmt(N)} records · ${D.source_url?`<a href="${esc(D.source_url)}" target="_blank" rel="noopener">source</a>`:"source not given"}`;

/* filter widgets */
function opt(v,l){return `<option value="${esc(v)}">${esc(l)}</option>`}
$("fmech").innerHTML=opt("","All")+mechs.map(m=>opt(m,m+" ("+fmt(R.filter(r=>r.mechanism===m).length)+")")).join("");
const tc=countBy(R,r=>r.type);
$("ftype").innerHTML=opt("","All")+types.map(t=>opt(t,t+" ("+fmt(tc[t])+")")).join("");
function buildBody(){
  const sub=F.mech?R.filter(r=>r.mechanism===F.mech):R;
  const bc=countBy(sub,r=>r.body);
  $("fbody").innerHTML=opt("","All")+Object.keys(bc).sort().map(b=>opt(b,b+" ("+fmt(bc[b])+")")).join("");
  $("fbody").value=F.body;
}
buildBody();
$("statewrap").hidden=!hasStates;
$("fstate").innerHTML=opt("","All")+Object.keys(stateCounts).sort().map(s=>opt(s,s+" ("+fmt(stateCounts[s])+")")).join("");
const yopts=years.map(y=>opt(y,y)).join("");
$("yfrom").innerHTML=yopts;$("yto").innerHTML=yopts;
$("yfrom").value=F.yf;$("yto").value=F.yt;
$("fsdg").innerHTML=opt("","All")+sdgsPresent.map(g=>opt(g,"SDG "+g+(SDGN[g]?": "+SDGN[g]:""))).join("");
$("kw2").placeholder="Search "+fmt(N)+" records, e.g. torture";

function words(){return F.kw.trim().toLowerCase().split(/\s+/).filter(Boolean)}
function applyFilters(){
  const w=words();
  filtered=R.filter(r=>{
    if(F.mech&&r.mechanism!==F.mech)return false;
    if(F.body&&r.body!==F.body)return false;
    if(F.type&&r.type!==F.type)return false;
    if(F.state&&!(r._states||[]).includes(F.state))return false;
    if(F.yf!=null&&r.year<F.yf)return false;
    if(F.yt!=null&&r.year>F.yt)return false;
    if(F.sdg!==""&&!r.sdgs.includes(Number(F.sdg)))return false;
    if(F.themes.length&&!F.themes.every(t=>r.themes.includes(t)))return false;
    for(const x of w)if(r._lc.indexOf(x)<0)return false;
    return true;
  });
}
function chipList(){
  const c=[];
  if(F.kw.trim())c.push(["Keyword: "+F.kw.trim(),()=>{F.kw="";syncKw()}]);
  if(F.mech)c.push([F.mech,()=>{F.mech="";F.body="";buildBody();$("fmech").value=""}]);
  if(F.body)c.push([F.body,()=>{F.body="";$("fbody").value=""}]);
  if(F.type)c.push([F.type,()=>{F.type="";$("ftype").value=""}]);
  if(F.state)c.push(["State: "+F.state,()=>{F.state="";$("fstate").value=""}]);
  if(F.yf!==F0.yf||F.yt!==F0.yt)c.push(["Years "+F.yf+"–"+F.yt,()=>{F.yf=F0.yf;F.yt=F0.yt;$("yfrom").value=F.yf;$("yto").value=F.yt}]);
  if(F.sdg!=="")c.push(["SDG "+F.sdg,()=>{F.sdg="";$("fsdg").value=""}]);
  F.themes.forEach(t=>c.push(["Theme: "+t,()=>{F.themes=F.themes.filter(x=>x!==t)}]));
  return c;
}
function describeFilters(){return chipList().map(c=>c[0])}
function syncKw(){$("kw1").value=F.kw;$("kw2").value=F.kw}

/* sorting */
function pkey(r){return r._para?r._para.split(".").map(Number):[1e9]}
function cmp(a,b){
  if(a.date!==b.date)return a.date<b.date?1:-1;
  const bc=String(a.body).localeCompare(String(b.body));if(bc)return bc;
  const pa=pkey(a),pb=pkey(b);
  for(let i=0;i<Math.max(pa.length,pb.length);i++){const x=pa[i]==null?-1:pa[i],y=pb[i]==null?-1:pb[i];if(x!==y)return x-y}
  return a._i-b._i;
}

/* themes */
function topThemes(arr){
  const m={};
  arr.forEach(r=>r.themes.forEach(t=>{const o=m[t]||(m[t]={n:0,a:1e9,b:-1e9});o.n++;if(r.year<o.a)o.a=r.year;if(r.year>o.b)o.b=r.year}));
  return Object.keys(m).map(t=>({t,n:m[t].n,a:m[t].a,b:m[t].b})).sort((x,y)=>y.n-x.n||x.t.localeCompare(y.t)).slice(0,10);
}
function hl(text,w){
  if(!w.length)return esc(text);
  const re=new RegExp("("+w.map(x=>x.replace(/[.*+?^${}()|[\]\\]/g,"\\$&")).join("|")+")","gi");
  return text.split(re).map((p,i)=>i%2?"<mark>"+esc(p)+"</mark>":esc(p)).join("");
}
function citation(r){return r._para?r.symbol+", para. "+r._para:r.symbol}
function stateCell(r){
  if(r.mechanism!==UPR)return "–";
  return r._states&&r._states.length?esc(r._states.join("; ")):'<span class="muted">State not found</span>';
}

/* render */
function render(){
  applyFilters();shown=50;
  const n=filtered.length;
  $("matchn").textContent=fmt(n);
  $("matchof").textContent="matching records · of "+fmt(N)+" in the file";
  $("sharebar").style.width=(N?n/N*100:0)+"%";
  const cl=$("chips");cl.innerHTML="";
  chipList().forEach(c=>{const b=document.createElement("button");b.className="chip";b.textContent=c[0]+" ×";b.setAttribute("aria-label","Remove filter "+c[0]);b.onclick=()=>{c[1]();render()};cl.appendChild(b)});
  sample=null;
  renderTab();
}
function renderTab(){
  if(tab===1)renderOverview();
  if(tab===2)renderRecords();
  if(tab===3)renderCheck();
  if(tab===4)renderMethod();
}

function tile(label,big,sub,dot){return `<div class="tile"><div class="mono">${dot?`<span class="dot" style="background:${dot}"></span>`:""}${esc(label)}</div><div class="big">${big}</div><div class="sub">${sub}</div></div>`}
function renderOverview(){
  const n=filtered.length;
  const tcnt=countBy(filtered,r=>r.type);
  const tb=Object.keys(tcnt).sort((a,b)=>tcnt[b]-tcnt[a]).map(k=>fmt(tcnt[k])+" "+esc(k)).join(" · ")||"no records";
  const docs=new Set(filtered.map(r=>r.symbol));
  const ys=filtered.map(r=>r.year);
  $("tiles1").innerHTML=tile("All records",fmt(n),tb)+tile("Documents",fmt(docs.size),"distinct symbols")+tile("Years",n?Math.min(...ys)+"–"+Math.max(...ys):"–","first–last document year");
  const ms=[...new Set(R.map(r=>r.mechanism))].sort();
  $("mtiles").innerHTML=ms.map(m=>{
    const rs=filtered.filter(r=>r.mechanism===m);
    const extra=(m===UPR&&hasStates)?` · <button class="linkbtn" id="seestates">see the States</button>`:"";
    return tile(m,fmt(rs.length),`${fmt(new Set(rs.map(r=>r.symbol)).size)} documents · latest ${rs.length?Math.max(...rs.map(r=>r.year)):"–"} · ${n?(rs.length/n*100).toFixed(1):"0.0"}% of filtered${extra}`,MECHCOL[m]||"#666");
  }).join("");
  const ss=$("seestates");
  if(ss)ss.onclick=()=>{
    const el=$("statelist");
    if(!el.hidden){el.hidden=true;return}
    const sc={};filtered.forEach(r=>(r._states||[]).forEach(s=>sc[s]=(sc[s]||0)+1));
    const top=Object.keys(sc).sort((a,b)=>sc[b]-sc[a]||a.localeCompare(b)).slice(0,10);
    el.innerHTML=`<h3 class="fig">Ten States that made most recommendations to ${esc(COUNTRY)}</h3>`+(top.length?`<table><caption>For the current filter; a recommendation with several States counts once for each.</caption><thead><tr><th scope="col">State</th><th scope="col" class="n">Recommendations</th></tr></thead><tbody>${top.map(s=>`<tr><td>${esc(s)}</td><td class="n">${fmt(sc[s])}</td></tr>`).join("")}</tbody></table>`:'<p class="note">No State found in the filtered records.</p>')+`<div class="note"><b>How this is computed</b> Names in the parentheses ending each UPR text; a count of recommendations, not of influence.</div>`;
    el.hidden=false;
  };
  /* FIG1 */
  const top=topThemes(filtered);
  $("fig1t").textContent=`Ten most frequent themes among ${fmt(n)} filtered records`;
  $("fig1empty").hidden=top.length>0;$("c1box").hidden=!top.length;
  if(charts.c1){charts.c1.destroy();charts.c1=null}
  if(top.length){
    charts.c1=new Chart($("c1"),{type:"bar",data:{labels:top.map(x=>x.t),datasets:[{data:top.map(x=>x.n),backgroundColor:"rgba(155,35,53,.8)"}]},
      options:{indexAxis:"y",animation:false,maintainAspectRatio:false,responsive:true,layout:{padding:{right:40}},
        plugins:{legend:{display:false},tooltip:{enabled:true}},
        scales:{x:{grid:{display:false},ticks:{display:false},border:{display:false}},y:{grid:{display:false},ticks:{color:"#1d1b18",font:{size:12},callback:function(v){const l=this.getLabelForValue(v);return l.length>42?l.slice(0,41)+"…":l}}}},
        onClick:(e,els,ch)=>{const p=ch.getElementsAtEventForMode(e,"nearest",{intersect:true},true);if(p.length){addTheme(top[p[0].index].t)}},
        onHover:(e,els)=>{e.native.target.style.cursor=els.length?"pointer":"default"}},
      plugins:[{id:"vals",afterDatasetsDraw(ch){const c=ch.ctx;c.save();c.fillStyle="#1d1b18";c.font="12px system-ui";c.textBaseline="middle";ch.getDatasetMeta(0).data.forEach((b,i)=>c.fillText(fmt(ch.data.datasets[0].data[i]),b.x+6,b.y));c.restore()}}]});
  }
  $("themetable").innerHTML=`<caption>The same ten rows as FIG.01 (n = ${fmt(n)} filtered records)</caption><thead><tr><th scope="col">Theme</th><th scope="col" class="n">Records</th><th scope="col" class="n">% of filtered</th><th scope="col">Years</th></tr></thead><tbody>`+
    (top.length?top.map((x,i)=>`<tr><td><button class="linkbtn" data-th="${i}">${esc(x.t)}</button></td><td class="n">${fmt(x.n)}</td><td class="n">${(x.n/n*100).toFixed(1)}</td><td>${x.a===x.b?x.a:x.a+"–"+x.b}</td></tr>`).join(""):'<tr><td colspan="4">No records match.</td></tr>')+"</tbody>";
  $("themetable").querySelectorAll("[data-th]").forEach(b=>b.onclick=()=>addTheme(top[b.dataset.th].t));
  /* FIG2 */
  $("fig2t").textContent=`Records per year by mechanism, ${fmt(n)} filtered records`;
  $("fig2empty").hidden=n>0;$("c2box").hidden=!n;
  if(charts.c2){charts.c2.destroy();charts.c2=null}
  if(n){
    const ys=filtered.map(r=>r.year);const y0=Math.min(...ys),y1=Math.max(...ys);
    const yl=[];for(let y=y0;y<=y1;y++)yl.push(y);
    const mm=[...new Set(filtered.map(r=>r.mechanism))].sort();
    const cnt={};filtered.forEach(r=>{const k=r.mechanism+"|"+r.year;cnt[k]=(cnt[k]||0)+1});
    charts.c2=new Chart($("c2"),{type:"bar",data:{labels:yl,datasets:mm.map(m=>({label:m,data:yl.map(y=>cnt[m+"|"+y]||0),backgroundColor:MECHCOL[m]||"#666"}))},
      options:{animation:false,maintainAspectRatio:false,responsive:true,plugins:{legend:{position:"bottom"}},scales:{x:{stacked:true,grid:{display:false},ticks:{autoSkip:false,maxRotation:0,font:{size:11}}},y:{stacked:true,beginAtZero:true,grid:{color:"#e6dfd0"},ticks:{precision:0}}}}});
  }
}
function addTheme(t){if(!F.themes.includes(t))F.themes.push(t);render()}

function renderRecords(){
  const w=words();
  const rows=filtered.slice().sort(cmp);if(!dirDesc)rows.reverse();
  const n=rows.length,vis=rows.slice(0,shown);
  let h=`<caption>${n?`Showing ${fmt(vis.length)} of ${fmt(n)} matching records, ${dirDesc?"newest first":"oldest first"}`:"No records match."}</caption><thead><tr><th scope="col"><button id="datesort" title="Reverse the order">Date ${dirDesc?"↓":"↑"}</button></th><th scope="col">Body</th><th scope="col">Symbol</th><th scope="col">Para.</th><th scope="col">First line</th>${hasStates?'<th scope="col">Recommending State</th>':""}</tr></thead><tbody>`;
  const cols=hasStates?6:5;
  vis.forEach(r=>{
    const o=openRows.has(r._i);
    h+=`<tr class="rec ${o?"open":""}" tabindex="0" aria-expanded="${o}" data-i="${r._i}"><td>${esc(r.date)}</td><td>${esc(r.body)}</td><td><a href="${esc(r.doc_url)}" target="_blank" rel="noopener">${esc(r.symbol)}</a></td><td>${r._para?esc(r._para):"–"}</td><td class="first">${hl(r._first,w)}</td>${hasStates?`<td>${stateCell(r)}</td>`:""}</tr>`;
    if(o){
      h+=`<tr><td class="detail" colspan="${cols}">${r._para?`<div class="pnum">${esc(r._para)}</div>`:'<div class="mono muted">no paragraph number found in the text</div>'}<div class="fulltext">${hl(r.text,w)}</div>`+
      (r.section?`<div class="lbl"><span class="mono">Section</span>${esc(r.section)}</div>`:"")+
      `<div class="lbl"><span class="mono">Themes</span>${r.themes.length?r.themes.map(esc).join("; "):'<span class="muted">not labelled</span>'}</div>`+
      `<div class="lbl"><span class="mono">SDGs</span>${r.sdgs.length?r.sdgs.map(g=>esc("SDG "+g+(SDGN[g]?": "+SDGN[g]:""))).join("; "):'<span class="muted">not labelled</span>'}</div>`+
      (r.sdg_targets.length?`<div class="lbl"><span class="mono">SDG targets</span>${r.sdg_targets.map(esc).join("; ")}</div>`:"")+
      `<div class="lbl"><span class="mono">Affected persons</span>${r.affected_persons.length?r.affected_persons.map(esc).join("; "):'<span class="muted">not labelled</span>'}</div>`+
      `<button class="btn" data-copy="${r._i}">Copy citation${r._para?"":" (no paragraph number in this extract)"}</button><a class="btn alt" style="text-decoration:none;display:inline-block" href="${esc(r.doc_url)}" target="_blank" rel="noopener">Open the UN document</a> <span class="note" data-ok="${r._i}" hidden>Copied</span></td></tr>`;
    }
  });
  h+="</tbody>";
  $("rectable").innerHTML=h;
  $("more").hidden=n<=shown;
  $("more").textContent="Show 50 more ("+fmt(n-shown)+" left)";
  $("datesort").onclick=()=>{dirDesc=!dirDesc;renderRecords()};
  $("rectable").querySelectorAll("tr.rec").forEach(tr=>{
    const tog=()=>{const i=Number(tr.dataset.i);openRows.has(i)?openRows.delete(i):openRows.add(i);renderRecords();const nt=$("rectable").querySelector(`tr.rec[data-i="${i}"]`);if(nt)nt.focus()};
    tr.onclick=e=>{if(e.target.closest("a"))return;tog()};
    tr.onkeydown=e=>{if((e.key==="Enter"||e.key===" ")&&e.target===tr){e.preventDefault();tog()}};
  });
  $("rectable").querySelectorAll("[data-copy]").forEach(b=>b.onclick=()=>{
    const i=b.dataset.copy;copyText(citation(R[i]));
    const s=$("rectable").querySelector(`[data-ok="${i}"]`);s.hidden=false;setTimeout(()=>s.hidden=true,2000);
  });
}
$("more").onclick=()=>{shown+=50;renderRecords()};

function copyText(t){
  if(navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText(t).catch(()=>fb(t))}else fb(t);
  function fb(x){const a=document.createElement("textarea");a.value=x;document.body.appendChild(a);a.select();try{document.execCommand("copy")}catch(e){}a.remove()}
}

/* checks */
function sumObj(o){return Object.values(o).reduce((a,b)=>a+b,0)}
function renderCheck(){
  const L=[];
  const add=(label,a,b,ok,extra,warnOnly)=>L.push({label,a,b,ok,extra,warnOnly});
  add("Record count: records in the file vs the file's stated count",fmt(N),fmt(Number(D.count)),N===Number(D.count));
  [["mechanism",r=>r.mechanism],["body",r=>r.body],["year",r=>r.year]].forEach(([k,f])=>{const s=sumObj(countBy(R,f));add(`Partition: counts per ${k} added up vs records`,fmt(s),fmt(N),s===N)});
  const tcnt=countBy(R,r=>r.type);add("Type partition: counts per type added up vs headline total ("+Object.keys(tcnt).map(k=>k+" "+fmt(tcnt[k])).join(", ")+")",fmt(sumObj(tcnt)),fmt(N),sumObj(tcnt)===N);
  /* chart vs table */
  const top=topThemes(filtered);
  let bad=[];
  top.forEach(x=>{let c=0;for(let i=0;i<filtered.length;i++)if(filtered[i].themes.indexOf(x.t)>=0)c++;if(c!==x.n)bad.push(x.t+": bar "+x.n+" vs recount "+c)});
  const tblVals=[...$("themetable").querySelectorAll("tbody tr")].map(tr=>tr.children[1]?tr.children[1].textContent.replace(/,/g,""):"");
  if(top.length&&tab===3&&tblVals.length&&tblVals.some((v,i)=>Number(v)!==top[i].n))bad.push("table rows differ from bars");
  const mx=top.length?top[0].n:0;
  if(mx>filtered.length)bad.push("largest bar "+mx+" exceeds filtered count "+filtered.length);
  add("Chart against table: each of the "+top.length+" bars vs a second count over the "+fmt(filtered.length)+" filtered records; largest bar "+fmt(mx)+" not above filtered count",top.length+" bars",bad.length?bad.length+" differ":"all equal",!bad.length,bad.join("; "));
  /* links */
  const lf=R.filter(r=>{let u="";try{u=decodeURIComponent(r.doc_url||"").toLowerCase()}catch(e){u=String(r.doc_url||"").toLowerCase()}return !(u.startsWith("https://docs.un.org/")&&u.endsWith(String(r.symbol||"").toLowerCase()))});
  add("Links: doc_url starts with https://docs.un.org/ and ends with the symbol",fmt(N-lf.length)+" pass",fmt(lf.length)+" fail",lf.length===0,lf.slice(0,30).map(r=>r.symbol+" → "+r.doc_url).join("\n"));
  /* para */
  const pm=[...new Set(R.map(r=>r.mechanism))].sort().map(m=>{const rs=R.filter(r=>r.mechanism===m);const p=rs.filter(r=>r._para).length;return {m,p,n:rs.length}});
  pm.forEach(x=>{const ok=x.m===UPR?x.p===x.n:true;add(`Paragraph numbers found, ${x.m}${x.m===UPR?" (expected 100%)":""}`,fmt(x.p)+" of "+fmt(x.n),(x.n?(x.p/x.n*100).toFixed(1):"0.0")+"%",ok,"",true)});
  /* states */
  const up=R.filter(r=>r.mechanism===UPR),nf=up.filter(r=>!r._states||!r._states.length);
  add("States found: UPR records with at least one State vs UPR records",fmt(up.length-nf.length),fmt(up.length),nf.length===0,nf.slice(0,60).map(r=>r.symbol+" — …"+r.text.slice(-70)).join("\n"),true);
  /* dups */
  add("Distinct id vs records",fmt(new Set(R.map(r=>r.id)).size),fmt(N),new Set(R.map(r=>r.id)).size===N);
  const tx={};let dup=0;R.forEach(r=>{if(tx[r.text])dup++;else tx[r.text]=1});
  add("Records whose text exactly repeats an earlier record",fmt(dup),"0 expected",dup===0,"",true);
  [["themes","themes"],["sdgs","sdgs"],["affected_persons","affected_persons"]].forEach(([k,l])=>{const c=R.filter(r=>!r[k].length).length;add(`Not labelled: records with no ${l}`,fmt(c),fmt(N),true,"",true)});
  $("checks").innerHTML=L.map(c=>{
    const st=c.ok?'<span class="ok">✓ pass</span>':(c.warnOnly?'<span class="warn">⚠ warning</span>':'<span class="fail">✕ check failed</span>');
    const isInfo=/Not labelled/.test(c.label);
    return `<li>${isInfo?'<span class="muted">· info</span>':st} ${esc(c.label)}: <b>${esc(c.a)}</b> vs <b>${esc(c.b)}</b>${c.extra?`<details><summary>Show records</summary><pre style="white-space:pre-wrap;font-size:12px">${esc(c.extra)}</pre></details>`:""}</li>`;
  }).join("");
  renderSampleCtl();
}
function mulberry32(a){return function(){a|=0;a=a+0x6D2B79F5|0;let t=Math.imul(a^a>>>15,1|a);t=t+Math.imul(t^t>>>7,61|t)^t;return((t^t>>>14)>>>0)/4294967296}}
function draw(seed){
  const rng=mulberry32(seed),a=filtered.slice();
  for(let i=a.length-1;i>0;i--){const j=Math.floor(rng()*(i+1));[a[i],a[j]]=[a[j],a[i]]}
  sample={seed,ids:a.slice(0,10).map(r=>r._i),v:{},open:null};
  renderSampleCtl();
}
function renderSampleCtl(){
  const c=$("samplectl");
  if(!filtered.length){c.innerHTML='<p class="note">No records match, nothing to draw.</p>';$("tally").textContent="";$("cards").innerHTML="";return}
  if(!sample){
    c.innerHTML=`<button class="btn" id="d0">Check 10 at random</button><span class="note">from the ${fmt(filtered.length)} filtered records</span>`;
    $("d0").onclick=()=>draw(1+Math.floor(Math.random()*999999));
    $("tally").textContent="";$("cards").innerHTML="";return;
  }
  c.innerHTML=`<button class="btn" id="d1">Draw again</button><label class="mono" for="seed" style="margin-left:8px">Seed</label> <input id="seed" type="number" value="${sample.seed}" style="width:110px;display:inline-block"> <button class="btn alt" id="d2">Draw with this seed</button>`;
  $("d1").onclick=()=>draw(1+Math.floor(Math.random()*999999));
  $("d2").onclick=()=>draw(Number($("seed").value)||1);
  renderCards();
}
function renderCards(){
  const s=sample;let f=0,d=0,u=0;
  Object.values(s.v).forEach(v=>{if(v==="fit")f++;else if(v==="no")d++;else u++});
  $("tally").innerHTML=`Themes: <b>${f}</b> fit, <b>${d}</b> don't, <b>${u}</b> unsure of <b>${f+d+u}</b> judged · seed ${s.seed} · your judgement, not the UN's`;
  $("cards").innerHTML=s.ids.map((i,k)=>{
    const r=R[i],o=s.open===i,v=s.v[i];
    return `<div class="card"><div class="cardline"><span class="mono">${k+1}</span><a href="${esc(r.doc_url)}" target="_blank" rel="noopener">${esc(r.symbol)}</a><span>${r._para?"para. "+esc(r._para):"–"}</span><button class="t" data-o="${i}" aria-expanded="${o}">${esc(r._first)}</button><span class="mono">${v==="fit"?"fits":v==="no"?"doesn't fit":v==="unsure"?"unsure":""}</span></div>`+
    (o?`<div class="cardbody"><div class="fulltext">${esc(r.text)}</div><div class="chips">${r.themes.length?r.themes.map(t=>`<span class="chip plain">${esc(t)}</span>`).join(""):'<span class="muted">not labelled</span>'}</div><div class="note">Do the themes, as a set, fit this paragraph?</div>${[["fit","Fits"],["no","Doesn't fit"],["unsure","Unsure"]].map(([x,l])=>`<button class="btn alt ${v===x?"sel":""}" data-v="${x}" data-i="${i}">${l}</button>`).join("")}</div>`:"")+"</div>";
  }).join("");
  $("cards").querySelectorAll("[data-o]").forEach(b=>b.onclick=()=>{const i=Number(b.dataset.o);s.open=s.open===i?null:i;renderCards();const nb=$("cards").querySelector(`[data-o="${i}"]`);if(nb)nb.focus()});
  $("cards").querySelectorAll("[data-v]").forEach(b=>b.onclick=()=>{const i=Number(b.dataset.i);s.v[i]=b.dataset.v;renderCards();const nb=$("cards").querySelector(`[data-v="${b.dataset.v}"][data-i="${i}"]`);if(nb)nb.focus()});
}

/* method & export */
function summaryText(){
  const n=filtered.length,top=topThemes(filtered);
  const tcnt=countBy(filtered,r=>r.type);
  const ys=filtered.map(r=>r.year);
  return `${COUNTRY}: UN recommendations and observations (OHCHR UHRI, built ${D.built||"n/a"})\n`+
  `Filters: ${describeFilters().join("; ")||"none"}\n`+
  `${fmt(n)} records of ${fmt(N)} in the file, from ${fmt(new Set(filtered.map(r=>r.symbol)).size)} documents, ${n?Math.min(...ys)+"–"+Math.max(...ys):"no years"} (dated by document).\n`+
  `By type: ${Object.keys(tcnt).map(k=>k+" "+fmt(tcnt[k])).join(", ")||"none"}.\n`+
  `Ten most frequent themes (a record can carry several): ${top.map(x=>x.t+" "+fmt(x.n)+" ("+(x.a===x.b?x.a:x.a+"–"+x.b)+")").join("; ")||"none"}.`;
}
function renderMethod(){
  $("method").innerHTML=`<p>The total is the number of records in the file; documents are distinct UN symbols, and years run from the earliest to the latest document year. The type breakdown uses each <code>type</code> value exactly as spelled in the data.</p>
  <p>Filters combine with AND. Mechanism, body and type are exact matches; the year range is inclusive; SDG matches the goal number; the keyword must have every word occur in the text or symbol, literally, so "torture" does not find "ill-treatment".</p>
  <p>Theme counts add one for each record carrying a theme, so they sum to more than the number of records. The year range under each theme shows when it was used: a label that only appears in old documents may be a legacy label, so check it with the random sample.</p>
  <p>The paragraph number is the first number at the start of the text (for example 71, or 144.43 in UPR). The recommending State is read from the parentheses ending a UPR text; groups with a comma or over 60 characters are rejected and shown as "State not found".</p>
  <p>The citation copies the symbol and paragraph number. Nothing is estimated, no model is called, and nothing leaves your browser except what you copy.</p>`;
  $("sumbox").textContent=summaryText();
  $("srcline").innerHTML=`Data source: ${D.source_url?`<a href="${esc(D.source_url)}" target="_blank" rel="noopener">${esc(D.source||D.source_url)}</a>`:esc(D.source||"not given")} · built ${esc(D.built||"not given")} · licence: not stated in the file; check the source before reuse.`;
}
$("copysum").onclick=()=>{copyText(summaryText());const e=$("copied4");e.hidden=false;setTimeout(()=>e.hidden=true,2000)};
$("dl").onclick=()=>{
  const q=v=>'"'+String(v==null?"":v).replace(/"/g,'""')+'"';
  const rows=filtered.slice().sort(cmp);
  const head=["date","body","mechanism","type","symbol","doc_url","paragraph","recommending_states","section","text","themes","sdgs","sdg_targets","affected_persons"];
  let out=`# Country: ${COUNTRY}\n# Source: ${D.source||""} ${D.source_url||""}\n# Built: ${D.built||""}\n# Filters: ${describeFilters().join("; ")||"none"}\n# Rows: ${rows.length}\n`;
  out+=head.join(",")+"\n"+rows.map(r=>[r.date,r.body,r.mechanism,r.type,r.symbol,r.doc_url,r._para||"",r.mechanism===UPR?(r._states||[]).join(" | "):"",r.section||"",r.text,r.themes.join(" | "),r.sdgs.join(" | "),r.sdg_targets.join(" | "),r.affected_persons.join(" | ")].map(q).join(",")).join("\n");
  const url=URL.createObjectURL(new Blob(["\ufeff"+out],{type:"text/csv;charset=utf-8"}));
  const a=document.createElement("a");a.href=url;a.download="uhri-"+COUNTRY.toLowerCase().replace(/\W+/g,"-")+".csv";document.body.appendChild(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(url),2000);
};

/* wiring */
let kt=null;
function onKw(e){const v=e.target.value;clearTimeout(kt);kt=setTimeout(()=>{F.kw=v;syncKw();render()},300)}
$("kw1").oninput=onKw;$("kw2").oninput=onKw;
$("fmech").onchange=e=>{F.mech=e.target.value;F.body="";buildBody();render()};
$("fbody").onchange=e=>{F.body=e.target.value;render()};
$("ftype").onchange=e=>{F.type=e.target.value;render()};
$("fstate").onchange=e=>{F.state=e.target.value;render()};
function yr(){let a=Number($("yfrom").value),b=Number($("yto").value);if(a>b){[a,b]=[b,a];$("yfrom").value=a;$("yto").value=b}F.yf=a;F.yt=b;render()}
$("yfrom").onchange=yr;$("yto").onchange=yr;
$("fsdg").onchange=e=>{F.sdg=e.target.value;render()};
$("clearall").onclick=()=>{F=Object.assign({},F0,{themes:[]});syncKw();$("fmech").value="";buildBody();$("ftype").value="";$("fstate").value="";$("yfrom").value=F.yf;$("yto").value=F.yt;$("fsdg").value="";render()};
document.querySelectorAll("[data-sec]").forEach(b=>b.onclick=()=>{
  const i=Number(b.dataset.sec);openSec=openSec===i?null:i;
  document.querySelectorAll("[data-sec]").forEach(x=>{const o=Number(x.dataset.sec)===openSec;x.setAttribute("aria-expanded",o);x.nextElementSibling.hidden=!o;x.lastElementChild.textContent=o?"−":"+"});
});
function setTab(n,focus){
  tab=n;
  for(let i=1;i<=4;i++){const t=$("tab"+i);t.setAttribute("aria-selected",i===n);t.tabIndex=i===n?0:-1;$("p"+i).hidden=i!==n}
  $("filters").hidden=n>2;
  if(focus)$("tab"+n).focus();
  renderTab();
}
[1,2,3,4].forEach(i=>{
  $("tab"+i).onclick=()=>setTab(i);
  $("tab"+i).onkeydown=e=>{
    let j=null;
    if(e.key==="ArrowRight")j=i%4+1;else if(e.key==="ArrowLeft")j=(i+2)%4+1;else if(e.key==="Home")j=1;else if(e.key==="End")j=4;
    if(j){e.preventDefault();setTab(j,true)}
  };
});
syncKw();
render();
})();
</script>
</body>
</html>
```