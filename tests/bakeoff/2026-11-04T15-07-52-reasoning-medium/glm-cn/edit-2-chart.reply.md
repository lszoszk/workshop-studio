```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>UN human rights recommendations: Kenya</title>
<style>
  [hidden]{display:none!important}
  :root{--paper:#f4f0e8;--ink:#1d1b18;--rule:#d9d2c3;--red:#9b2335}
  *{box-sizing:border-box}
  body{margin:0;background:var(--paper);color:var(--ink);font:16px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}
  a{color:var(--red)}
  a:focus,button:focus,input:focus,select:focus,summary:focus{outline:2px solid var(--red);outline-offset:2px}
  .mono{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:11px;letter-spacing:.08em;text-transform:uppercase}
  header{padding:20px 24px 14px;border-bottom:1px solid var(--rule)}
  header .mono{color:#6b6257}
  h1{font-family:Georgia,"Times New Roman",serif;font-weight:400;font-size:34px;margin:6px 0 4px}
  .meta{font-size:13.5px;color:#4a443c}
  nav.tabs{display:flex;gap:2px;padding:0 24px;border-bottom:1px solid var(--rule)}
  nav.tabs button{background:none;border:none;border-bottom:3px solid transparent;padding:10px 14px 8px;cursor:pointer;font-family:ui-monospace,Menlo,Consolas,monospace;font-size:12px;letter-spacing:.06em;color:#4a443c}
  nav.tabs button[aria-selected="true"]{color:var(--red);border-bottom-color:var(--red)}
  .layout{display:flex;min-height:600px}
  aside{width:250px;flex:none;border-right:1px solid var(--rule);padding:18px 18px 24px}
  main{flex:1;padding:20px 28px 48px;min-width:0}
  .bignum{font-family:Georgia,serif;font-size:44px;line-height:1.05;margin:8px 0 2px}
  .sharebar{height:5px;background:var(--rule);margin:6px 0 10px;position:relative}
  .sharebar i{position:absolute;left:0;top:0;bottom:0;background:var(--red)}
  .chips{display:flex;flex-wrap:wrap;gap:5px;margin:6px 0 4px}
  .chip{display:inline-flex;align-items:center;gap:5px;border:1px solid var(--rule);background:#fffdf8;border-radius:12px;padding:2px 8px;font-size:12px}
  .chip button{background:none;border:none;cursor:pointer;color:var(--red);font-weight:700;padding:0}
  .acc{border-top:1px solid var(--rule)}
  .acc:last-of-type{border-bottom:1px solid var(--rule)}
  .acc>button{width:100%;display:flex;justify-content:space-between;background:none;border:none;cursor:pointer;padding:10px 2px;font-family:ui-monospace,Menlo,Consolas,monospace;font-size:11px;letter-spacing:.08em;text-transform:uppercase;color:var(--ink)}
  .acc>div{padding:2px 2px 14px}
  .acc label{display:block;font-size:12px;color:#4a443c;margin:8px 0 3px}
  select,input[type=text]{width:100%;padding:6px 8px;border:1px solid var(--rule);background:#fffdf8;font:inherit;font-size:14px}
  .optbtn{display:block;width:100%;text-align:left;background:none;border:none;cursor:pointer;padding:4px 6px;font-size:14px}
  .optbtn[aria-pressed="true"]{color:var(--red);font-weight:700;background:#f7e9eb}
  .hint{font-size:11.5px;color:#6b6257;margin-top:4px}
  .tiles{display:flex;flex-wrap:wrap;gap:28px;margin:8px 0 20px}
  .tile{max-width:340px}
  .tile .bignum{font-size:46px}
  .tile .sub{font-size:13.5px;color:#4a443c}
  .note{font-size:12.5px;color:#6b6257;margin-top:3px;max-width:520px}
  .dot{display:inline-block;width:9px;height:9px;border-radius:50%;margin-right:6px}
  figure{margin:26px 0}
  figcaption{font-family:Georgia,serif;font-size:18px;margin-bottom:8px}
  .figno{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:11px;letter-spacing:.1em;color:#6b6257;display:block;margin-bottom:2px}
  .chartbox{position:relative;max-width:760px}
  table{border-collapse:collapse;width:100%;font-size:14px;margin-top:10px}
  caption{text-align:left;font-size:12.5px;color:#4a443c;padding-bottom:6px}
  th,td{text-align:left;padding:6px 10px;border-bottom:1px solid var(--rule);vertical-align:top}
  th{font-weight:600;font-size:12px;font-family:ui-monospace,Menlo,Consolas,monospace;letter-spacing:.05em;text-transform:uppercase;color:#4a443c}
  th.num,td.num{text-align:right;font-variant-numeric:tabular-nums}
  .doclink{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:12.5px;white-space:nowrap}
  tr.rec{cursor:pointer}
  tr.rec:hover{background:#efe9dd}
  .firstline{max-width:520px}
  mark{background:#f3d9a4;padding:0 1px}
  tr.expand td{background:#fbf8f1}
  .parabig{font-family:Georgia,serif;font-size:34px;color:var(--red);margin-right:14px;float:left}
  .fulltext{white-space:pre-wrap;margin:6px 0 8px;clear:none}
  .lbl{display:inline-block;border:1px solid var(--rule);background:#fffdf8;border-radius:12px;padding:1px 9px;font-size:12px;margin:2px 3px 2px 0}
  button.act{background:none;border:1px solid var(--rule);cursor:pointer;font:inherit;font-size:13px;padding:4px 12px;border-radius:4px}
  button.act:hover{border-color:var(--red);color:var(--red)}
  .copyok{color:var(--red);font-size:12px;margin-left:8px}
  .check{padding:7px 0;border-bottom:1px solid var(--rule);font-size:14px}
  .pass{color:#2d6a4f;font-weight:700}
  .fail{color:var(--red);font-weight:700}
  .warn{color:#a15c00;font-weight:700}
  .card{border:1px solid var(--rule);margin:10px 0;background:#fffdf8}
  .card>button{width:100%;text-align:left;background:none;border:none;cursor:pointer;padding:9px 12px;font:inherit;font-size:14px}
  .card>div{padding:0 14px 12px;border-top:1px solid var(--rule)}
  .inline-list{margin-top:8px;font-size:14px}
  .inline-list li{margin:2px 0}
  .btnrow{display:flex;gap:8px;flex-wrap:wrap;margin-top:14px}
  footer{border-top:1px solid var(--rule);padding:12px 24px;font-family:ui-monospace,Menlo,Consolas,monospace;font-size:11px;color:#6b6257;letter-spacing:.04em}
  .empty{font-family:Georgia,serif;font-size:20px;color:#6b6257;padding:24px 0}
</style>
</head>
<body>
<header id="hdr"></header>
<nav class="tabs" role="tablist" aria-label="Sections" id="tabs"></nav>
<div class="layout">
  <aside id="rail" aria-label="Filters"></aside>
  <main id="main">
    <section id="tab0" role="tabpanel"></section>
    <section id="tab1" role="tabpanel" hidden></section>
    <section id="tab2" role="tabpanel" hidden></section>
    <section id="tab3" role="tabpanel" hidden></section>
  </main>
</div>
<footer id="foot"></footer>

<script>
"use strict";
const U = window.WORKSHOP_DATA.uhri;
const RECS = U.records || [];
const COUNTRY = U.country;
const fmt = n => Number(n).toLocaleString("en-US");
const esc = s => String(s==null?"":s).replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));

/* ---------- derived helpers ---------- */
function paraNum(t){ const m=/^(\d{1,3}(?:\.\d{1,3})?)\.?\s/.exec(t||""); return m?m[1]:null; }
const PARA = RECS.map(r=>paraNum(r.text));
function statesOf(r){
  if(r.mechanism!=="Universal Periodic Review") return null;
  const m=/((?:\s*\((?:[^()]|\([^()]*\))*\))+)\s*[;.]?\s*$/.exec(r.text||"");
  if(!m) return [];
  const groups=m[0].match(/\((?:[^()]|\([^()]*\))*\)/g)||[];
  const out=[];
  for(const g of groups){
    const inner=g.slice(1,-1).trim();
    if(inner && !inner.includes(",") && inner.length<=60) out.push(inner);
  }
  return out;
}
const STATES = RECS.map(r=>statesOf(r));
const YEARS = [...new Set(RECS.map(r=>r.year))].sort((a,b)=>a-b);
const MECHS = [...new Set(RECS.map(r=>r.mechanism))].sort();
const TYPES = [...new Set(RECS.map(r=>r.type))];
const MECHCOLOR = {"Universal Periodic Review":"#c2410c","Treaty bodies":"#0f766e","Special Procedures":"#7c3aed"};
const TYPECOLOR = {"Recommendations":"#9b2335","Concerns/Observations":"#8a8177"};
const mechColor = m => MECHCOLOR[m] || "#555";
const typeColor = t => TYPECOLOR[t] || "#5c5348";

/* ---------- state ---------- */
const S = {kw:"", mech:"all", body:"all", type:"all", st:"all", yFrom:YEARS[0], yTo:YEARS[YEARS.length-1], sdg:"all", themes:[], sortDesc:true, page:1, tab:0, seed:1, sample:null, tally:null};

function filtered(){
  const kws = S.kw.trim().toLowerCase().split(/\s+/).filter(Boolean);
  return RECS.filter((r,i)=>{
    if(S.mech!=="all" && r.mechanism!==S.mech) return false;
    if(S.body!=="all" && r.body!==S.body) return false;
    if(S.type!=="all" && r.type!==S.type) return false;
    if(S.st!=="all" && !(STATES[i]||[]).includes(S.st)) return false;
    if(r.year < Math.min(S.yFrom,S.yTo) || r.year > Math.max(S.yFrom,S.yTo)) return false;
    if(S.sdg!=="all" && !((r.sdgs||[]).includes(Number(S.sdg)))) return false;
    for(const t of S.themes) if(!((r.themes||[]).includes(t))) return false;
    for(const w of kws) if(!((r.text||"").toLowerCase().includes(w) || (r.symbol||"").toLowerCase().includes(w))) return false;
    return true;
  }).map(r=>({r,i:r.__idx}));
}
RECS.forEach((r,i)=>r.__idx=i);

function themeCounts(set){
  const m=new Map();
  for(const {r} of set) for(const t of (r.themes||[])){
    if(!m.has(t)) m.set(t,{c:0,y1:r.year,y2:r.year});
    const o=m.get(t); o.c++; o.y1=Math.min(o.y1,r.year); o.y2=Math.max(o.y2,r.year);
  }
  return [...m.entries()].map(([t,o])=>({theme:t,...o})).sort((a,b)=>b.c-a.c||a.theme.localeCompare(b.theme));
}

/* ---------- header / footer ---------- */
(function(){
  const docs=new Set(RECS.map(r=>r.symbol)).size;
  document.getElementById("hdr").innerHTML =
    `<div class="mono">UHRI · ${esc(COUNTRY)}</div>
     <h1>UN human rights recommendations and observations: ${esc(COUNTRY)}</h1>
     <div class="meta">Source: <a href="${esc(U.source_url)}" target="_blank" rel="noopener">${esc(U.source)}</a> ·
       ${fmt(RECS.length)} records · ${fmt(docs)} documents · ${YEARS[0]}–${YEARS[YEARS.length-1]} ·
       built ${esc(U.built)} · dated by document (the date is the document's, not the recommendation's).</div>`;
  document.getElementById("foot").innerHTML =
    `Built on OHCHR UHRI data · ${fmt(RECS.length)} records · <a href="${esc(U.source_url)}" target="_blank" rel="noopener">source</a> · counts are loops over the records in this page; nothing is estimated.`;
})();

/* ---------- tabs ---------- */
const TABNAMES=["01 OVERVIEW","02 RECORDS","03 CHECK","04 METHOD & EXPORT"];
const tabsEl=document.getElementById("tabs");
TABNAMES.forEach((n,i)=>{
  const b=document.createElement("button");
  b.role="tab"; b.id="tabbtn"+i; b.textContent=n; b.setAttribute("aria-selected",i===0);
  b.setAttribute("aria-controls","tab"+i); b.tabIndex=i===0?0:-1;
  b.addEventListener("click",()=>selectTab(i));
  tabsEl.appendChild(b);
});
tabsEl.addEventListener("keydown",e=>{
  if(e.key!=="ArrowRight"&&e.key!=="ArrowLeft")return;
  e.preventDefault();
  const d=e.key==="ArrowRight"?1:-1;
  selectTab((S.tab+d+TABNAMES.length)%TABNAMES.length);
  tabsEl.children[S.tab].focus();
});
function selectTab(i){
  S.tab=i;
  [...tabsEl.children].forEach((b,j)=>{b.setAttribute("aria-selected",j===i);b.tabIndex=j===i?0:-1;});
  for(let j=0;j<4;j++) document.getElementById("tab"+j).hidden = j!==i;
  document.getElementById("railFilters").hidden = i>=2;
  if(i===0) renderOverview();
  if(i===1) renderTable();
  if(i===2) renderChecks();
  if(i===3) renderMethod();
}

/* ---------- rail ---------- */
const rail=document.getElementById("rail");
rail.innerHTML=`
  <div style="display:flex;justify-content:space-between;align-items:baseline">
    <span class="mono">Filters</span>
    <button class="act" id="clearall" style="font-size:12px;padding:2px 8px">Clear all</button>
  </div>
  <div id="matchcount" aria-live="polite">
    <div class="bignum" id="mcnum"></div>
    <div class="hint" id="mcsub"></div>
    <div class="sharebar"><i id="mcbar"></i></div>
  </div>
  <div class="chips" id="chips"></div>
  <div id="railFilters"></div>`;
document.getElementById("clearall").addEventListener("click",()=>{
  S.kw="";S.mech="all";S.body="all";S.type="all";S.st="all";S.sdg="all";S.themes=[];
  S.yFrom=YEARS[0];S.yTo=YEARS[YEARS.length-1];
  refresh();
});
const RF=document.getElementById("railFilters");
RF.innerHTML=`
  <div class="acc"><button aria-expanded="true" data-acc="0">01 Keyword <span aria-hidden="true"></span></button>
    <div><input type="text" id="kwbox" placeholder="e.g. torture" aria-label="Keyword">
      <div class="hint">literal match, not synonyms · every word must occur in the text or symbol</div></div></div>
  <div class="acc"><button aria-expanded="false" data-acc="1">02 Mechanism, body, type <span aria-hidden="true"></span></button>
    <div id="acc1body" hidden></div></div>
  <div class="acc"><button aria-expanded="false" data-acc="2">03 Years and SDG <span aria-hidden="true"></span></button>
    <div id="acc2body" hidden>
      <label for="yfrom">Year from</label><select id="yfrom"></select>
      <label for="yto">Year to</label><select id="yto"></select>
      <div class="hint">a reversed range is swapped</div>
      <label for="sdgsel">SDG goal (only those present)</label><select id="sdgsel"></select>
    </div></div>`;
RF.querySelectorAll(".acc>button").forEach(b=>{
  b.addEventListener("click",()=>{
    const open=b.getAttribute("aria-expanded")==="true";
    RF.querySelectorAll(".acc>button").forEach(x=>{x.setAttribute("aria-expanded","false");x.nextElementSibling.hidden=true;});
    if(!open){b.setAttribute("aria-expanded","true");b.nextElementSibling.hidden=false;}
  });
});
let kwTimer=null;
document.getElementById("kwbox").addEventListener("input",e=>{
  clearTimeout(kwTimer);
  kwTimer=setTimeout(()=>{S.kw=e.target.value;S.page=1;refresh();},300);
});
function buildAcc1(){
  const mechs=[["all","all mechanisms ("+fmt(RECS.length)+")"]];
  const mc=new Map(); RECS.forEach(r=>mc.set(r.mechanism,(mc.get(r.mechanism)||0)+1));
  [...mc.entries()].sort((a,b)=>b[1]-a[1]).forEach(([m,c])=>mechs.push([m,`${esc(m)} (${fmt(c)})`]));
  const inMech = S.mech==="all"?RECS:RECS.filter(r=>r.mechanism===S.mech);
  const bc=new Map(); inMech.forEach(r=>bc.set(r.body,(bc.get(r.body)||0)+1));
  const bodies=[["all","all bodies and mandates ("+fmt(inMech.length)+")"]];
  [...bc.entries()].sort((a,b)=>b[1]-a[1]).forEach(([m,c])=>bodies.push([m,`${esc(m)} (${fmt(c)})`]));
  const tc=new Map(); inMech.forEach(r=>tc.set(r.type,(tc.get(r.type)||0)+1));
  const types=[["all","all types ("+fmt(inMech.length)+")"]];
  [...tc.entries()].sort((a,b)=>b[1]-a[1]).forEach(([m,c])=>types.push([m,`${esc(m)} (${fmt(c)})`]));
  let stOpts="";
  const allStates=new Map();
  inMech.forEach(r=>(STATES[r.__idx]||[]).forEach(s=>allStates.set(s,(allStates.get(s)||0)+1)));
  if(allStates.size){
    stOpts=`<label for="stsel">Recommending State (UPR)</label><select id="stsel">`+
      `<option value="all">all States (${fmt([...allStates.values()].reduce((a,b)=>a+b,0))} recommendations)</option>`+
      [...allStates.entries()].sort((a,b)=>b[1]-a[1]).map(([s,c])=>`<option value="${esc(s)}"${S.st===s?" selected":""}>${esc(s)} (${fmt(c)})</option>`).join("")+`</select>`;
  }
  document.getElementById("acc1body").innerHTML=
    `<label for="mechsel">Mechanism</label><select id="mechsel">`+mechs.map(([v,l])=>`<option value="${esc(v)}"${S.mech===v?" selected":""}>${l}</option>`).join("")+`</select>
     <label for="bodysel">Body or mandate</label><select id="bodysel">`+bodies.map(([v,l])=>`<option value="${esc(v)}"${S.body===v?" selected":""}>${l}</option>`).join("")+`</select>
     <label for="typesel">Type</label><select id="typesel">`+types.map(([v,l])=>`<option value="${esc(v)}"${S.type===v?" selected":""}>${l}</option>`).join("")+`</select>`+stOpts;
  document.getElementById("mechsel").addEventListener("change",e=>{S.mech=e.target.value;S.body="all";S.type="all";S.st="all";S.page=1;refresh();});
  document.getElementById("bodysel").addEventListener("change",e=>{S.body=e.target.value;S.page=1;refresh();});
  document.getElementById("typesel").addEventListener("change",e=>{S.type=e.target.value;S.page=1;refresh();});
  const st=document.getElementById("stsel");
  if(st) st.addEventListener("change",e=>{S.st=e.target.value;S.page=1;refresh();});
}
(function(){
  const yf=document.getElementById("yfrom"), yt=document.getElementById("yto");
  YEARS.forEach(y=>{yf.add(new Option(y,y));yt.add(new Option(y,y));});
  yf.value=S.yFrom; yt.value=S.yTo;
  function yr(){ if(+yf.value>+yt.value){const t=yf.value;yf.value=yt.value;yt.value=t;} S.yFrom=+yf.value;S.yTo=+yt.value;S.page=1;refresh(); }
  yf.addEventListener("change",yr); yt.addEventListener("change",yr);
  const sdgSel=document.getElementById("sdgsel");
  const present=new Map(); RECS.forEach(r=>(r.sdgs||[]).forEach(g=>present.set(g,(present.get(g)||0)+1)));
  sdgSel.innerHTML=`<option value="all">all (${fmt(RECS.length)} records)</option>`+
    [...present.entries()].sort((a,b)=>a[0]-b[0]).map(([g,c])=>`<option value="${g}">${g}. ${esc((U.sdg_names&&U.sdg_names[String(g)])||"")} (${fmt(c)})</option>`).join("");
  sdgSel.addEventListener("change",e=>{S.sdg=e.target.value;S.page=1;refresh();});
})();

function renderChips(){
  const c=document.getElementById("chips");
  const chips=[];
  const add=(label,fn)=>chips.push({label,fn});
  if(S.kw.trim())add(`keyword: ${S.kw.trim()}`,()=>{S.kw="";document.getElementById("kwbox").value="";});
  if(S.mech!=="all")add(`mechanism: ${S.mech}`,()=>{S.mech="all";S.body="all";S.st="all";});
  if(S.body!=="all")add(`body: ${S.body}`,()=>S.body="all");
  if(S.type!=="all")add(`type: ${S.type}`,()=>S.type="all");
  if(S.st!=="all")add(`State: ${S.st}`,()=>S.st="all");
  if(S.sdg!=="all")add(`SDG ${S.sdg}`,()=>S.sdg="all");
  if(S.yFrom!==YEARS[0]||S.yTo!==YEARS[YEARS.length-1])add(`years: ${S.yFrom}–${S.yTo}`,()=>{S.yFrom=YEARS[0];S.yTo=YEARS[YEARS.length-1];document.getElementById("yfrom").value=S.yFrom;document.getElementById("yto").value=S.yTo;});
  S.themes.forEach(t=>add(`theme: ${t}`,()=>{S.themes=S.themes.filter(x=>x!==t);}));
  c.innerHTML = chips.length?`<span class="mono" style="width:100%">Active filters</span>`:"";
  chips.forEach(ch=>{
    const s=document.createElement("span");s.className="chip";
    s.innerHTML=`${esc(ch.label)} <button aria-label="Remove filter ${esc(ch.label)}">✕</button>`;
    s.querySelector("button").addEventListener("click",()=>{ch.fn();S.page=1;refresh();});
    c.appendChild(s);
  });
}

/* ---------- tab 01: overview ---------- */
let fig1=null,fig2=null,fig3=null;
function renderOverview(){
  const set=filtered(), n=set.length;
  const el=document.getElementById("tab0");
  if(!n){
    el.innerHTML=`<div class="empty">No records match the current filters.</div>`;
    drawMatch();return;
  }
  const docs=new Set(set.map(({r})=>r.symbol)).size;
  const types=new Map(); set.forEach(({r})=>types.set(r.type,(types.get(r.type)||0)+1));
  const typeLine=[...types.entries()].sort((a,b)=>b[1]-a[1]).map(([t,c])=>`${fmt(c)} ${esc(t)}`).join(" · ");
  const themes=themeCounts(set).slice(0,10);
  let tiles = `
    <div class="tiles">
      <div class="tile"><div class="bignum">${fmt(n)}</div>
        <div class="sub">records in the current filter — ${typeLine}</div>
        <div class="note">How computed: every record in the file whose fields pass all active filters; the breakdown counts records per type, spelled as in the data.</div></div>
      <div class="tile"><div class="bignum">${fmt(docs)}</div><div class="sub">documents (distinct symbols)</div>
        <div class="note">How computed: distinct <span class="mono">symbol</span> values among the filtered records.</div></div>
      <div class="tile"><div class="bignum">${Math.min(...set.map(({r})=>r.year))}–${Math.max(...set.map(({r})=>r.year))}</div><div class="sub">years covered</div>
        <div class="note">How computed: minimum and maximum <span class="mono">year</span> of the filtered records; dated by document.</div></div>
    </div>`;
  const mechStats=MECHS.map(m=>{
    const ms=set.filter(({r})=>r.mechanism===m);
    return {m,n:ms.length,d:new Set(ms.map(({r})=>r.symbol)).size,y:ms.length?Math.max(...ms.map(({r})=>r.year)):null,share:ms.length/n};
  }).sort((a,b)=>b.n-a.n);
  tiles+=`<div class="tiles">`+mechStats.map(s=>`
    <div class="tile"><div class="bignum">${fmt(s.n)}</div>
      <div class="sub"><span class="dot" style="background:${mechColor(s.m)}"></span>${esc(s.m)} · ${fmt(s.d)} documents${s.y?` · latest ${s.y}`:""} · ${Math.round(s.share*100)}% of the filtered set</div>
      <div class="note">How computed: filtered records with <span class="mono">mechanism</span> = “${esc(s.m)}”.</div>
      ${s.m==="Universal Periodic Review"?'<div><a href="#" id="seestates">see the States</a> <span class="mono">click = list</span></div><div class="inline-list" id="statelist" hidden></div>':''}
    </div>`).join("")+`</div>`;
  const figTable = themes.length? `
    <table><caption>The same ten themes as the chart, with the year range of the records carrying each. A record can carry several themes, so the counts add up to more than ${fmt(n)}.</caption>
    <thead><tr><th scope="col">Theme</th><th scope="col" class="num">Records</th><th scope="col" class="num">% of filtered</th><th scope="col">Years</th></tr></thead>
    <tbody>${themes.map(t=>`<tr><td>${esc(t.theme)}</td><td class="num">${fmt(t.c)}</td><td class="num">${(100*t.c/n).toFixed(1)}</td><td>${t.y1}–${t.y2}</td></tr>`).join("")}</tbody></table>
    <div class="note">Source: UN records in the current filter; theme labels are the UN's own (UHRI). Percentages are of records, not of labels. Themes concentrated in early years may be legacy labels — check a sample on tab 03.</div>`
    : `<div class="empty">No themes among the filtered records.</div>`;
  el.innerHTML = tiles + `
    <figure><div class="figno">FIG.01</div>
      <figcaption>Ten most frequent themes among ${fmt(n)} filtered records</figcaption>
      <div class="chartbox"><canvas id="c1" height="${Math.max(160,themes.length*30)}"></canvas></div>
      <div class="hint">click a bar = add that theme as a filter</div>${figTable}</figure>
    <figure><div class="figno">FIG.02</div>
      <figcaption>Records per year by mechanism, current filter (${fmt(n)} records)</figcaption>
      <div class="chartbox" style="max-width:860px"><canvas id="c2"></canvas></div>
      <div class="note">How computed: filtered records counted per <span class="mono">year</span> and <span class="mono">mechanism</span>; every year from ${YEARS[0]} to ${YEARS[YEARS.length-1]} appears, so gaps are years with no records in the filter. Source: UN records in the current filter.</div></figure>
    <figure><div class="figno">FIG.03</div>
      <figcaption>Recommendations and observations per year, current filter (${fmt(n)} records)</figcaption>
      <div class="chartbox" style="max-width:860px"><canvas id="c3"></canvas></div>
      <div class="note">How computed: filtered records counted per <span class="mono">year</span> and <span class="mono">type</span>, spelled as in the data; every year from ${YEARS[0]} to ${YEARS[YEARS.length-1]} appears, so gaps are years with no records in the filter. Source: UN records in the current filter; dated by document.</div></figure>`;
  const ss=document.getElementById("seestates");
  if(ss){
    ss.addEventListener("click",e=>{
      e.preventDefault();
      const box=document.getElementById("statelist");
      if(!box.hidden){box.hidden=true;return;}
      const cnt=new Map();
      set.forEach(({r})=>(STATES[r.__idx]||[]).forEach(s=>cnt.set(s,(cnt.get(s)||0)+1)));
      const top=[...cnt.entries()].sort((a,b)=>b[1]-a[1]).slice(0,10);
      box.innerHTML=`<strong>Ten States that made most recommendations to ${esc(COUNTRY)}</strong> (current filter; a record counts once per State named)<ul>`+
        top.map(([s,c])=>`<li>${esc(s)} — ${fmt(c)}</li>`).join("")+`</ul><div class="note">A count of recommendations, not of influence; two States can appear on one line.</div>`;
      box.hidden=false;
    });
  }
  // FIG.01
  if(fig1)fig1.destroy();
  fig1=new Chart(document.getElementById("c1"),{
    type:"bar",
    data:{labels:themes.map(t=>t.theme.length>48?t.theme.slice(0,46)+"…":t.theme),
      datasets:[{data:themes.map(t=>t.c),backgroundColor:"rgba(155,35,53,0.8)"}]},
    options:{indexAxis:"y",responsive:true,maintainAspectRatio:false,
      plugins:{legend:{display:false},tooltip:{callbacks:{title:it=>themes[it[0].dataIndex].theme,label:it=>fmt(it.raw)+" records"}}},
      scales:{x:{grid:{display:false},ticks:{precision:0}},y:{grid:{display:false},ticks:{font:{size:12}}}},
      onClick:(e,els)=>{if(els.length){const t=themes[els[0].index].theme;if(!S.themes.includes(t)){S.themes.push(t);S.page=1;refresh();}}}}
  });
  document.getElementById("c1").style.height=Math.max(160,themes.length*30)+"px";
  // FIG.02
  if(fig2)fig2.destroy();
  const allY=[]; for(let y=YEARS[0];y<=YEARS[YEARS.length-1];y++)allY.push(y);
  const byMech=MECHS.map(m=>allY.map(y=>set.filter(({r})=>r.mechanism===m&&r.year===y).length));
  fig2=new Chart(document.getElementById("c2"),{
    type:"bar",
    data:{labels:allY,datasets:MECHS.map((m,i)=>({label:m,data:byMech[i],backgroundColor:mechColor(m)}))},
    options:{responsive:true,maintainAspectRatio:false,
      plugins:{legend:{position:"top",labels:{boxWidth:10,font:{size:12}}}},
      scales:{x:{stacked:true,grid:{display:false}},y:{stacked:true,grid:{display:false},ticks:{precision:0},title:{display:true,text:"records"}}}}
  });
  // FIG.03
  if(fig3)fig3.destroy();
  const typesHere=TYPES.filter(t=>set.some(({r})=>r.type===t));
  const byType=typesHere.map(t=>allY.map(y=>set.filter(({r})=>r.type===t&&r.year===y).length));
  fig3=new Chart(document.getElementById("c3"),{
    type:"bar",
    data:{labels:allY,datasets:typesHere.map((t,i)=>({label:t,data:byType[i],backgroundColor:typeColor(t)}))},
    options:{responsive:true,maintainAspectRatio:false,
      plugins:{legend:{position:"top",labels:{boxWidth:10,font:{size:12}}}},
      scales:{x:{stacked:true,grid:{display:false}},y:{stacked:true,grid:{display:false},ticks:{precision:0},title:{display:true,text:"records"}}}}
  });
  drawMatch();
}

/* ---------- tab 02: records ---------- */
function firstLine(t){
  if(t.length<=120)return t;
  const cut=t.slice(0,120); const sp=cut.lastIndexOf(" ");
  return cut.slice(0,sp>60?sp:120)+"…";
}
function sortSet(set){
  const a=[...set];
  a.sort((x,y)=>{
    const d=S.sortDesc?new Date(y.r.date)-new Date(x.r.date):new Date(x.r.date)-new Date(y.r.date);
    if(d)return d;
    const b=(x.r.body||"").localeCompare(y.r.body||""); if(b)return b;
    const pn=a=>{const p=PARA[a.i];return p?parseFloat(p):Infinity;};
    return pn(x)-pn(y);
  });
  return a;
}
function hl(text){
  let out=esc(text);
  for(const w of S.kw.trim().toLowerCase().split(/\s+/).filter(Boolean)){
    out=out.replace(new RegExp("("+w.replace(/[.*+?^${}()|[\]\\]/g,"\\$&")+")","gi"),"<mark>$1</mark>");
  }
  return out;
}
function renderTable(){
  const el=document.getElementById("tab1");
  const set=sortSet(filtered());
  const shown=set.slice(0,S.page*50);
  el.innerHTML=`
    <div style="display:flex;gap:12px;align-items:baseline;flex-wrap:wrap">
      <input type="text" id="topsearch" placeholder="Search ${fmt(RECS.length)} records, e.g. torture" style="max-width:420px" value="${esc(S.kw)}" aria-label="Search records">
      <span class="hint">same as the 01 Keyword filter · literal match, not synonyms</span>
    </div>
    ${set.length?`<table>
      <caption id="tcap"></caption>
      <thead><tr>
        <th scope="col"><button class="act" id="sortbtn" style="padding:0;border:none;font:inherit;text-transform:uppercase;letter-spacing:.05em;font-size:12px;font-family:ui-monospace,Menlo,Consolas,monospace">Date ${S.sortDesc?"▾":"▴"}</button></th>
        <th scope="col">Body</th><th scope="col">Symbol</th><th scope="col">Para.</th>
        <th scope="col">First line</th><th scope="col">Recommending State</th></tr></thead>
      <tbody id="tbody"></tbody></table>
      ${set.length>shown.length?'<div class="btnrow"><button class="act" id="more">Show 50 more</button></div>':''}`
    :`<div class="empty">No records match the current filters.</div>`}`;
  document.getElementById("tcap").textContent=`Showing ${fmt(shown.length)} of ${fmt(set.length)} matching records, newest first (click the Date header to reverse). Source: UN records, current filter.`;
  const ts=document.getElementById("topsearch");
  ts.addEventListener("input",e=>{clearTimeout(kwTimer);kwTimer=setTimeout(()=>{S.kw=e.target.value;S.page=1;refresh();},300);});
  const sb=document.getElementById("sortbtn");
  if(sb)sb.addEventListener("click",()=>{S.sortDesc=!S.sortDesc;renderTable();});
  const mb=document.getElementById("more");
  if(mb)mb.addEventListener("click",()=>{S.page++;renderTable();});
  const tb=document.getElementById("tbody");
  shown.forEach(({r,i})=>{
    const p=PARA[i];
    const st=STATES[i];
    const stTxt = st===null?"—":(st.length?st.map(esc).join(", "):'<span class="hint">State not found</span>');
    const tr=document.createElement("tr");
    tr.className="rec";tr.tabIndex=0;tr.setAttribute("aria-expanded","false");
    tr.innerHTML=`<td style="white-space:nowrap">${esc(r.date)}</td><td>${esc(r.body)}</td>
      <td class="doclink"><a href="${esc(r.doc_url)}" target="_blank" rel="noopener" onclick="event.stopPropagation()">${esc(r.symbol)}</a></td>
      <td>${p?esc(p):"—"}</td><td class="firstline">${hl(firstLine(r.text||""))}</td><td>${stTxt}</td>`;
    tr.addEventListener("click",()=>toggleRow(tr,r,i));
    tr.addEventListener("keydown",e=>{if(e.key==="Enter"){e.preventDefault();toggleRow(tr,r,i);}});
    tb.appendChild(tr);
  });
  drawMatch();
}
function toggleRow(tr,r,i){
  const next=tr.nextElementSibling;
  if(next&&next.classList.contains("expand")){next.remove();tr.setAttribute("aria-expanded","false");return;}
  document.querySelectorAll("tr.expand").forEach(x=>{x.previousElementSibling.setAttribute("aria-expanded","false");x.remove();});
  const p=PARA[i];
  const cite=p?`${r.symbol}, para. ${p}`:r.symbol;
  const ex=document.createElement("tr");
  ex.className="expand";
  ex.innerHTML=`<td colspan="6">
    ${p?`<span class="parabig">${esc(p)}</span>`:""}
    <div class="fulltext">${esc(r.text)}</div>
    <div style="clear:both"></div>
    ${r.section?`<div><span class="mono">Section</span> ${esc(r.section)}</div>`:""}
    <div><span class="mono">Themes</span> ${(r.themes||[]).length?r.themes.map(t=>`<span class="lbl">${esc(t)}</span>`).join(""):'<span class="hint">not labelled</span>'}</div>
    <div><span class="mono">SDGs</span> ${(r.sdgs||[]).length?r.sdgs.map(g=>`<span class="lbl">${g}. ${esc((U.sdg_names&&U.sdg_names[String(g)])||"")}</span>`).join("")+(r.sdg_targets&&r.sdg_targets.length?" "+r.sdg_targets.map(t=>`<span class="lbl">${esc(t)}</span>`).join(""):""):'<span class="hint">not labelled</span>'}</div>
    <div><span class="mono">Affected persons</span> ${(r.affected_persons||[]).length?r.affected_persons.map(t=>`<span class="lbl">${esc(t)}</span>`).join(""):'<span class="hint">not labelled</span>'}</div>
    <div class="btnrow">
      <button class="act" data-cite="${esc(cite)}">Copy citation${p?"":" (no paragraph number in this extract)"}</button>
      <a class="act" style="text-decoration:none;padding:4px 12px;border:1px solid var(--rule);border-radius:4px" href="${esc(r.doc_url)}" target="_blank" rel="noopener">Open the UN document</a>
      <span class="copyok" hidden>Copied</span>
    </div></td>`;
  ex.querySelector("[data-cite]").addEventListener("click",function(){
    const ok=this.parentElement.querySelector(".copyok");
    (navigator.clipboard?navigator.clipboard.writeText(this.dataset.cite):Promise.reject()).then(()=>{ok.hidden=false;setTimeout(()=>ok.hidden=true,2000);}).catch(()=>{ok.hidden=false;ok.textContent="Copy blocked — select: "+this.dataset.cite;setTimeout(()=>{ok.hidden=true;ok.textContent="Copied";},4000);});
  });
  tr.after(ex);tr.setAttribute("aria-expanded","true");
}

/* ---------- tab 03: checks ---------- */
function renderChecks(){
  const el=document.getElementById("tab2");
  const N=RECS.length;
  const lines=[];
  const ok=(name,a,b,pass)=>lines.push(`<div class="check"><span class="${pass?"pass":"fail"}">${pass?"✓":"check failed"}</span> ${esc(name)} — ${esc(String(a))}${b!==undefined?" vs "+esc(String(b)):""}</div>`);
  const warn=(name,a,b,pass)=>lines.push(`<div class="check"><span class="${pass?"pass":"warn"}">${pass?"✓":"warning"}</span> ${esc(name)} — ${esc(String(a))}${b!==undefined?" vs "+esc(String(b)):""}</div>`);
  // record count
  ok("Record count: records.length against the file's count field",fmt(N),fmt(Number(U.count)),N===Number(U.count));
  // partitions
  const part=(field)=>{
    const m=new Map();RECS.forEach(r=>{const k=r[field];m.set(k,(m.get(k)||0)+1);});
    const s=[...m.values()].reduce((a,b)=>a+b,0);
    return {s,m};
  };
  ["mechanism","body","type","year"].forEach(f=>{
    const p=part(f);ok(`Counts per ${f} sum to the record count`,fmt(p.s),fmt(N),p.s===N);
  });
  // chart vs table (second loop over current filter)
  const set=filtered(),n=set.length;
  const t1=themeCounts(set);
  const t2=(()=>{const m=new Map();for(const {r} of set)for(const t of (r.themes||[]))m.set(t,(m.get(t)||0)+1);return m;})();
  const same=t1.slice(0,10).every(x=>t2.get(x.theme)===x.c);
  ok(`FIG.01: each bar equals a count recomputed by a second loop (top 10 themes, ${fmt(n)} filtered records)`,"agreed","",same);
  const maxBar=t1.length?Math.max(...t1.map(x=>x.c)):0;
  ok("The largest theme bar is not larger than the filtered record count",fmt(maxBar),fmt(n),maxBar<=n);
  // links
  const badLinks=RECS.filter(r=>{
    if(!(r.doc_url||"").startsWith("https://docs.un.org/"))return true;
    let u=r.doc_url; try{u=decodeURIComponent(u);}catch(e){}
    return !u.toLowerCase().endsWith((r.symbol||"").toLowerCase());
  });
  ok("Every doc_url starts with https://docs.un.org/ and ends with its symbol",`${fmt(N-badLinks.length)} of ${fmt(N)} pass`,badLinks.length?`${fmt(badLinks.length)} fail: `+badLinks.slice(0,5).map(r=>esc(r.symbol)).join(", ")+(badLinks.length>5?" …":""):"",badLinks.length===0);
  // paragraph numbers
  const paraByMech={};
  MECHS.forEach(m=>{const rs=RECS.filter(r=>r.mechanism===m);paraByMech[m]=[rs.filter(r=>PARA[r.__idx]).length,rs.length];});
  const upr=paraByMech["Universal Periodic Review"]||[0,0];
  warn("UPR records with a paragraph number found (expected 100%)",`${fmt(upr[0])} of ${fmt(upr[1])} (${upr[1]?Math.round(100*upr[0]/upr[1]):0}%)`,"",upr[0]===upr[1]);
  MECHS.filter(m=>m!=="Universal Periodic Review").forEach(m=>{
    const [a,b]=paraByMech[m];
    lines.push(`<div class="check"><span class="mono">${esc(m)}</span> ${fmt(a)} of ${fmt(b)} records start with a paragraph number (${b?Math.round(100*a/b):0}%)</div>`);
  });
  // states
  const uprRecs=RECS.filter(r=>r.mechanism==="Universal Periodic Review");
  const withState=uprRecs.filter(r=>(STATES[r.__idx]||[]).length).length;
  const noState=uprRecs.filter(r=>!(STATES[r.__idx]||[]).length);
  ok("UPR records with at least one recommending State found",`${fmt(withState)} of ${fmt(uprRecs.length)}`,noState.length?`${fmt(noState.length)} without: `+noState.slice(0,5).map(r=>`${esc(r.symbol)}${PARA[r.__idx]?" para. "+esc(PARA[r.__idx]):""} ends “${esc((r.text||"").slice(-40))}”`).join(" · ")+(noState.length>5?" …":""):"",noState.length===0);
  // duplicates & gaps
  const ids=new Set(RECS.map(r=>r.id));
  ok("Distinct id equals the record count",fmt(ids.size),fmt(N),ids.size===N);
  const txts=new Map();RECS.forEach(r=>txts.set(r.text,(txts.get(r.text)||0)+1));
  const dup=[...txts.values()].filter(c=>c>1).reduce((a,b)=>a+(b-1),0);
  lines.push(`<div class="check"><span class="${dup?"warn":"pass"}">${dup?"note":"✓"}</span> Duplicate texts: ${fmt(dup)} records repeat the text of another record${dup?" (shown in the table as they are)":""}</div>`);
  [["themes","theme"],["sdgs","SDG"],["affected_persons","affected-persons"]].forEach(([f,l])=>{
    const c=RECS.filter(r=>!(r[f]||[]).length).length;
    lines.push(`<div class="check"><span class="${c?"warn":"pass"}">${c?"note":"✓"}</span> ${fmt(c)} records carry no ${l} label (“not labelled” on expand)</div>`);
  });

  el.innerHTML=`<h2 style="font-family:Georgia,serif;font-weight:400;font-size:26px">Can I trust these numbers?</h2>
    <p class="hint" style="margin-bottom:4px">HOW THE APP CHECKS ITSELF — each check compares two independently computed values; nothing is hidden.</p>
    ${lines.join("")}
    <h3 style="font-family:Georgia,serif;font-weight:400;font-size:20px;margin-top:28px">Random-sample label check</h3>
    <p class="note">Draw ten records from the current filter and judge whether the UN's theme labels fit the text. This is your judgement of the UN's labels; nothing is sent anywhere. The app never changes a UN label.</p>
    <div class="btnrow" style="align-items:center">
      <button class="act" id="draw10">Check 10 at random</button>
      <button class="act" id="drawagain" hidden>Draw again</button>
      <span id="seedwrap" hidden><label class="mono" for="seedbox">seed</label> <input type="text" id="seedbox" style="width:80px;display:inline-block" value="1"> <button class="act" id="drawseed">Draw with this seed</button></span>
    </div>
    <div id="tally" class="note" style="margin-top:8px" aria-live="polite"></div>
    <div id="sample" style="margin-top:6px"></div>`;
  function mulberry32(a){return function(){a|=0;a=a+0x6D2B79F5|0;let t=Math.imul(a^a>>>15,1|a);t=t+Math.imul(t^t>>>7,61|t)^t;return((t^t>>>14)>>>0)/4294967296;};}
  function draw(seed){
    S.seed=seed;S.tally={fit:0,no:0,unsure:0,judged:0,marks:{}};
    const rng=mulberry32(seed);
    const pool=[...set];
    const picks=[];const used=new Set();
    for(let k=0;k<Math.min(10,pool.length);k++){
      let j;do{j=Math.floor(rng()*pool.length);}while(used.has(j));
      used.add(j);picks.push(pool[j]);
    }
    const box=document.getElementById("sample");
    box.innerHTML="";
    picks.forEach(({r,i},idx)=>{
      const card=document.createElement("div");card.className="card";
      card.innerHTML=`<button aria-expanded="false"><strong>${esc(r.symbol)}</strong>${PARA[i]?`, para. ${esc(PARA[i])}`:""} — ${esc(r.body)}, ${esc(r.date)} <span class="hint">click = open</span></button>
        <div hidden>
          <p class="fulltext">${esc(r.text)}</p>
          <div><span class="mono">Themes (the UN's labels)</span> ${(r.themes||[]).map(t=>`<span class="lbl">${esc(t)}</span>`).join("")||'<span class="hint">not labelled</span>'}</div>
          <div class="btnrow" data-idx="${idx}">
            <button class="act" data-v="fit">Fits</button>
            <button class="act" data-v="no">Doesn't fit</button>
            <button class="act" data-v="unsure">Unsure</button>
          </div>
        </div>`;
      const btn=card.querySelector("button"),div=card.querySelector("div");
      btn.addEventListener("click",()=>{const o=!div.hidden;box.querySelectorAll(".card>div").forEach(d=>{d.hidden=true;d.previousElementSibling.setAttribute("aria-expanded","false");});div.hidden=o;btn.setAttribute("aria-expanded",String(!o));});
      card.querySelector(".btnrow").addEventListener("click",e=>{
        const b=e.target.closest("[data-v]");if(!b)return;
        const v=b.dataset.v;
        if(S.tally.marks[idx]!==undefined)S.tally[S.tally.marks[idx]]--;
        S.tally.marks[idx]=v;S.tally[v]++;
        if(S.tally.judged<idx+1)S.tally.judged=Math.max(S.tally.judged,Object.keys(S.tally.marks).length);
        card.querySelectorAll("[data-v]").forEach(x=>x.style.borderColor="");
        b.style.borderColor="var(--red)";
        tallyLine();
      });
      box.appendChild(card);
    });
    document.getElementById("drawagain").hidden=false;
    document.getElementById("seedwrap").hidden=false;
    document.getElementById("seedbox").value=seed;
    tallyLine();
  }
  function tallyLine(){
    const t=S.tally;
    document.getElementById("tally").innerHTML=`Themes: ${t.fit} fit, ${t.no} don't, ${t.unsure} unsure of ${t.judged} judged (your judgement, seed ${S.seed} — a colleague drawing with the same seed and the same filter sees the same ten).`;
  }
  document.getElementById("draw10").addEventListener("click",()=>draw(1+Math.floor(Math.random()*99999)));
  document.getElementById("drawagain").addEventListener("click",()=>draw(1+Math.floor(Math.random()*99999)));
  document.getElementById("drawseed").addEventListener("click",()=>{const v=parseInt(document.getElementById("seedbox").value,10);draw(Number.isFinite(v)?v:1);});
  drawMatch();
}

/* ---------- tab 04: method & export ---------- */
function renderMethod(){
  const el=document.getElementById("tab3");
  const set=filtered(),n=set.length;
  const docs=new Set(set.map(({r})=>r.symbol)).size;
  el.innerHTML=`<h2 style="font-family:Georgia,serif;font-weight:400;font-size:26px">How this was made, and how to take it with you</h2>
    <p style="max-width:680px">Every number on this page is a loop over the records in the file, run in your browser: the headline total is the number of records that pass all active filters; documents are distinct symbols; theme counts count each theme once per record that carries it, so they can sum to more than the record count; the timeline counts records per year and mechanism, with zero for years without records; the paragraph number is the number at the start of the text; the recommending State is read from the parentheses at the end of UPR texts only, and a record counts once for each State named. Nothing is estimated, no model is called, and nothing leaves the browser except the clipboard write when you copy.</p>
    <div class="btnrow">
      <button class="act" id="dlcsv">Download CSV of the current filter (${fmt(n)} records)</button>
      <button class="act" id="copysum">Copy summary</button>
      <span class="copyok" id="sumok" hidden>Copied</span>
    </div>
    <p class="note">The CSV has one row per record with the columns shown in the table plus the full verbatim text, themes, SDGs and targets, affected persons and section, preceded by comment lines with the country, source, build date, filters applied and row count.</p>
    <p class="note">Data: <a href="${esc(U.source_url)}" target="_blank" rel="noopener">${esc(U.source)}</a> · ${esc(U.title)} · built ${esc(U.built)}. Theme, SDG and affected-person labels are the UN's own (UHRI); this app relabels nothing. Data received under OHCHR's terms of use for the Universal Human Rights Index.</p>`;
  document.getElementById("dlcsv").addEventListener("click",()=>{
    const q=v=>`"${String(v==null?"":v).replace(/"/g,'""')}"`;
    const comments=[
      `# ${COUNTRY}: UN human rights recommendations and observations`,
      `# Source: ${U.source} (${U.source_url})`,
      `# Built: ${U.built}; extracted ${U.built}`,
      `# Filters: keyword="${S.kw.trim()}"; mechanism=${S.mech}; body=${S.body}; type=${S.type}; State=${S.st}; years=${S.yFrom}-${S.yTo}; SDG=${S.sdg}; themes=${S.themes.join(" | ")||"(none)"}`,
      `# Rows: ${set.length} of ${RECS.length} records; dated by document`,
    ].join("\n");
    const head=["date","body","mechanism","type","symbol","doc_url","paragraph","recommending_states","text","themes","sdgs","sdg_targets","affected_persons","section"];
    const rows=sortSet(set).map(({r,i})=>[
      r.date,r.body,r.mechanism,r.type,r.symbol,r.doc_url,PARA[i]||"",(STATES[i]||[]).join(" | "),
      r.text,(r.themes||[]).join(" | "),(r.sdgs||[]).join(" | "),(r.sdg_targets||[]).join(" | "),(r.affected_persons||[]).join(" | "),r.section||""
    ].map(q).join(","));
    const blob=new Blob([comments+"\n"+head.join(",")+"\n"+rows.join("\n")],{type:"text/csv"});
    const a=document.createElement("a");a.href=URL.createObjectURL(blob);
    a.download=U.country.replace(/\W+/g,"-").toLowerCase()+"-uhri-records.csv";
    document.body.appendChild(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(a.href),5000);
  });
  document.getElementById("copysum").addEventListener("click",function(){
    const types=new Map();set.forEach(({r})=>types.set(r.type,(types.get(r.type)||0)+1));
    const th=themeCounts(set).slice(0,10);
    const txt=`${COUNTRY}: ${n} UN human rights records (${[...types.entries()].map(([t,c])=>c+" "+t).join(", ")}) from ${docs} documents, ${Math.min(...set.map(({r})=>r.year))}–${Math.max(...set.map(({r})=>r.year))}, matching the filters: ${S.kw.trim()?("keyword “"+S.kw.trim()+"”; "):""}${S.mech!=="all"?"mechanism "+S.mech+"; ":""}${S.themes.length?"themes "+S.themes.join(", ")+"; ":""}${S.sdg!=="all"?"SDG "+S.sdg+"; ":""}years ${S.yFrom}–${S.yTo}. Most frequent themes: ${th.map(t=>t.theme+" ("+t.c+")").join("; ")}. Source: ${U.source}, via the UHRI; counts computed in-browser, dated by document.`;
    (navigator.clipboard?navigator.clipboard.writeText(txt):Promise.reject()).then(()=>{
      const ok=document.getElementById("sumok");ok.hidden=false;setTimeout(()=>ok.hidden=true,2000);
    }).catch(()=>{});
  });
  drawMatch();
}

/* ---------- shared rail number ---------- */
function drawMatch(){
  const n=filtered().length;
  document.getElementById("mcnum").textContent=fmt(n);
  document.getElementById("mcsub").textContent=`matching records of ${fmt(RECS.length)} in the file`;
  document.getElementById("mcbar").style.width=(RECS.length?100*n/RECS.length:0)+"%";
  renderChips();
}
function refresh(){
  buildAcc1();
  drawMatch();
  if(S.tab===0)renderOverview();
  if(S.tab===1)renderTable();
  if(S.tab===2)renderChecks();
  if(S.tab===3)renderMethod();
}

/* init */
selectTab(0);
drawMatch();
</script>
</body>
</html>
```