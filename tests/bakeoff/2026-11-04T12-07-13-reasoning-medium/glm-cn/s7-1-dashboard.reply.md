I built the four-tab dashboard exactly to your plan: filters rail with collapsible headings, overview tiles plus the two charts, the records table with in-place expansion and copy-citation, the self-check panel with the seeded random label check, and the method & export tab with CSV and summary copy. All numbers are computed in the browser from `WORKSHOP_DATA.uhri`.

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>UN human rights recommendations and observations</title>
<style>
  :root{
    --paper:#f4f0e8; --ink:#1d1b18; --rule:#d9d2c3; --red:#9b2335;
    --upr:#c2410c; --tb:#0f766e; --sp:#7c3aed;
    --mono:ui-monospace,Menlo,Consolas,monospace;
    --serif:Georgia,"Times New Roman",serif;
    --sans:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;
  }
  [hidden]{display:none!important}
  *{box-sizing:border-box}
  body{margin:0;background:var(--paper);color:var(--ink);font-family:var(--sans);font-size:16px;line-height:1.5}
  a{color:var(--red)}
  a:focus-visible,button:focus-visible,input:focus-visible,select:focus-visible,[tabindex]:focus-visible{outline:2px solid var(--red);outline-offset:2px}
  .mono{font-family:var(--mono);font-size:11px;letter-spacing:.12em;text-transform:uppercase}
  .wrap{max-width:1180px;margin:0 auto;padding:20px 24px 40px}

  /* header */
  header.app{border-bottom:2px solid var(--ink);padding-bottom:14px;margin-bottom:0}
  .datalabel{font-family:var(--mono);font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:#6b6255}
  h1{font-family:var(--serif);font-weight:400;font-size:34px;line-height:1.15;margin:6px 0 8px}
  .srcline{font-size:13.5px;color:#4a443b}
  .srcline .mono{margin-left:12px}

  /* tabs */
  .tabs{display:flex;gap:0;border-bottom:1px solid var(--rule);margin-bottom:18px;flex-wrap:wrap}
  .tab{appearance:none;background:none;border:none;border-bottom:3px solid transparent;cursor:pointer;
    font-family:var(--mono);font-size:11.5px;letter-spacing:.1em;text-transform:uppercase;color:#5a5248;
    padding:12px 18px 10px;margin-right:4px}
  .tab[aria-selected="true"]{color:var(--red);border-bottom-color:var(--red)}
  .tab:hover{color:var(--ink)}
  .tabpanel{margin-top:4px}

  /* layout */
  .cols{display:flex;gap:28px;align-items:flex-start}
  aside.rail{width:250px;flex:0 0 250px;border-right:1px solid var(--rule);padding-right:20px}
  main{flex:1;min-width:0}
  @media(max-width:840px){.cols{flex-direction:column}aside.rail{width:100%;flex:none;border-right:none;border-bottom:1px solid var(--rule);padding:0 0 14px}}

  /* rail */
  .railhead{display:flex;justify-content:space-between;align-items:baseline;border-bottom:1px solid var(--rule);padding-bottom:6px}
  .bignum{font-family:var(--serif);font-size:46px;line-height:1.05;margin:14px 0 2px}
  .bignum small{font-size:16px;color:#5a5248;font-family:var(--sans)}
  .matchlabel{font-family:var(--mono);font-size:11px;letter-spacing:.1em;text-transform:uppercase;color:#6b6255}
  .sharetrack{height:5px;background:#e7e0d2;margin:10px 0 4px}
  .sharebar{height:5px;background:var(--red)}
  .chips{display:flex;flex-wrap:wrap;gap:6px;margin:10px 0 4px}
  .chip{display:inline-flex;align-items:center;gap:6px;border:1px solid var(--rule);background:#faf7f0;
    font-size:12.5px;padding:3px 6px 3px 9px;border-radius:999px}
  .chip button{appearance:none;border:none;background:none;cursor:pointer;font-size:14px;line-height:1;color:var(--red);padding:0 2px}
  .fgroup{border-bottom:1px solid var(--rule)}
  .fhead{width:100%;display:flex;justify-content:space-between;align-items:center;appearance:none;background:none;border:none;cursor:pointer;
    font-family:var(--mono);font-size:11.5px;letter-spacing:.1em;text-transform:uppercase;color:var(--ink);padding:12px 0 10px}
  .fhead .n{color:var(--red);margin-right:8px}
  .fhead .arrow{color:#8a8072;font-size:10px}
  .fbody{padding:2px 0 16px}
  .fbody label{display:block;font-size:12px;color:#5a5248;margin:8px 0 3px;font-family:var(--mono);letter-spacing:.06em;text-transform:uppercase}
  .fbody input[type=text],.fbody select{width:100%;padding:7px 8px;border:1px solid var(--rule);background:#faf7f0;font-family:var(--sans);font-size:14px;color:var(--ink)}
  .hint{font-size:12px;color:#7a7263;margin-top:5px;font-family:var(--mono);letter-spacing:.02em}
  .radios{display:flex;flex-direction:column;gap:2px}
  .radios label,.checks label{display:flex;gap:8px;align-items:baseline;font-size:13.5px;color:var(--ink);font-family:var(--sans);text-transform:none;letter-spacing:0;margin:2px 0;cursor:pointer}
  .radios .cnt,.checks .cnt{margin-left:auto;color:#8a8072;font-size:12px}
  .yearrow{display:flex;gap:8px}

  /* tiles */
  .tiles{display:flex;flex-wrap:wrap;gap:0;border-top:1px solid var(--rule);border-left:1px solid var(--rule);margin-bottom:26px}
  .tile{flex:1 1 200px;border-right:1px solid var(--rule);border-bottom:1px solid var(--rule);padding:16px 18px 12px;min-width:190px}
  .tile .lbl{font-family:var(--mono);font-size:11px;letter-spacing:.12em;text-transform:uppercase;color:#6b6255}
  .tile .num{font-family:var(--serif);font-size:44px;line-height:1.1;margin:4px 0 2px}
  .tile .sub{font-size:12.5px;color:#5a5248;line-height:1.45}
  .tile .dot{display:inline-block;width:9px;height:9px;border-radius:50%;margin-right:6px;vertical-align:baseline}
  .tile .how{font-size:11px;color:#8a8072;font-family:var(--mono);letter-spacing:.02em;margin-top:6px}

  /* figures */
  figure{margin:0 0 34px}
  figure .figno{font-family:var(--mono);font-size:11px;letter-spacing:.14em;color:var(--red)}
  figure h2{font-family:var(--serif);font-weight:400;font-size:20px;margin:4px 0 2px}
  figure .figsub{font-size:13px;color:#5a5248;margin-bottom:10px}
  figure .figsrc{font-size:11.5px;color:#8a8072;margin-top:6px}
  .chartbox{position:relative;height:340px}
  .chartbox.tall{height:380px}
  .nomatch{font-family:var(--serif);font-size:20px;color:#8a8072;padding:40px 0;text-align:center}

  /* tables */
  table{border-collapse:collapse;width:100%;font-size:14.5px}
  caption{text-align:left;font-family:var(--mono);font-size:11px;letter-spacing:.08em;text-transform:uppercase;color:#6b6255;padding-bottom:8px}
  th,td{text-align:left;vertical-align:top;padding:7px 10px 7px 0;border-bottom:1px solid var(--rule)}
  th{font-family:var(--mono);font-size:10.5px;letter-spacing:.1em;text-transform:uppercase;color:#5a5248;font-weight:400;border-bottom:1.5px solid #b8ae99}
  th .arrow{color:var(--red)}
  td.num,th.num{text-align:right;font-variant-numeric:tabular-nums}
  tr.rec{cursor:pointer}
  tr.rec:hover{background:#efe9dc}
  tr.rec td{border-bottom:1px solid #e4dcc9}
  mark{background:#f3d9a4;color:var(--ink);padding:0 1px}
  tr.expand td{background:#faf7f0;padding:18px 16px 20px;border-bottom:2px solid var(--red)}
  .para-big{font-family:var(--serif);font-size:38px;color:var(--red);line-height:1;margin-right:18px;float:left}
  .fulltext{font-size:15.5px;line-height:1.6;white-space:pre-wrap}
  .labelrow{margin-top:14px}
  .labelrow .lbl{font-family:var(--mono);font-size:10.5px;letter-spacing:.1em;text-transform:uppercase;color:#6b6255;margin-bottom:3px}
  .taglist{display:flex;flex-wrap:wrap;gap:5px}
  .tag{border:1px solid var(--rule);background:#f4f0e8;font-size:12.5px;padding:2px 8px}
  .actions{margin-top:16px;display:flex;gap:10px;flex-wrap:wrap;align-items:center}
  .btn{appearance:none;cursor:pointer;font-family:var(--sans);font-size:13.5px;color:var(--ink);background:#faf7f0;border:1px solid #b8ae99;padding:6px 14px}
  .btn:hover{border-color:var(--ink)}
  .btn.primary{background:var(--red);color:#fff;border-color:var(--red)}
  .copied{color:var(--red);font-size:12.5px;font-family:var(--mono)}
  .dash{color:#a99f8b}
  .statelist{margin-top:10px;border-top:1px solid var(--rule);padding-top:10px}
  .statelist ol{margin:6px 0 0;padding-left:22px;font-size:13.5px}
  .statelist li{margin:2px 0}

  /* checks */
  .checkline{display:flex;gap:14px;padding:9px 0;border-bottom:1px solid var(--rule);font-size:14px;align-items:baseline}
  .checkline .mark{font-family:var(--mono);font-size:11px;letter-spacing:.08em;white-space:nowrap}
  .pass{color:#0f766e}.fail{color:var(--red)}.warn{color:#a16207}
  .checkline .what{flex:1}
  .checkline .vals{font-family:var(--mono);font-size:12px;color:#5a5248}
  h2.sec{font-family:var(--serif);font-weight:400;font-size:22px;border-bottom:1px solid var(--rule);padding-bottom:6px;margin:26px 0 8px}
  .samplectl{display:flex;gap:10px;align-items:center;flex-wrap:wrap;margin:12px 0}
  .samplectl input{width:90px;padding:6px 8px;border:1px solid var(--rule);background:#faf7f0;font-family:var(--mono);font-size:13px}
  .card{border:1px solid var(--rule);border-left:3px solid var(--rule);margin-bottom:8px}
  .card.verdict-fit{border-left-color:#0f766e}
  .card.verdict-no{border-left-color:var(--red)}
  .card.verdict-unsure{border-left-color:#a16207}
  .cardhead{width:100%;display:flex;gap:14px;align-items:baseline;appearance:none;background:none;border:none;cursor:pointer;padding:10px 14px;text-align:left;font-size:14px}
  .cardhead .csym{font-family:var(--mono);font-size:12px;white-space:nowrap}
  .cardhead .cpara{font-family:var(--serif);color:var(--red);font-size:17px;min-width:60px}
  .cardhead .csnip{color:#5a5248;flex:1;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
  .cardbody{padding:0 16px 16px;border-top:1px solid var(--rule)}
  .cardbody .fulltext{margin-top:12px}
  .vbtns{display:flex;gap:8px;margin-top:12px}
  .vbtn.on{background:var(--ink);color:#fff;border-color:var(--ink)}
  .tally{font-size:14px;margin:10px 0}
  .tally .mono{color:var(--red)}

  /* method */
  .method p{max-width:72ch;font-size:15px}
  .fineprint{font-size:13px;color:#5a5248;max-width:72ch}

  footer.app{border-top:2px solid var(--ink);margin-top:30px;padding-top:10px;font-family:var(--mono);font-size:11px;letter-spacing:.08em;color:#6b6255;display:flex;justify-content:space-between;flex-wrap:wrap;gap:8px}
</style>
</head>
<body>
<div class="wrap">

<header class="app">
  <div class="datalabel" id="hd-label">UHRI</div>
  <h1 id="hd-title">UN human rights recommendations and observations</h1>
  <div class="srcline" id="hd-src"></div>
</header>

<div class="tabs" role="tablist" aria-label="Dashboard sections">
  <button class="tab" role="tab" id="tab-1" aria-controls="panel-1" aria-selected="true" tabindex="0">01 Overview</button>
  <button class="tab" role="tab" id="tab-2" aria-controls="panel-2" aria-selected="false" tabindex="-1">02 Records</button>
  <button class="tab" role="tab" id="tab-3" aria-controls="panel-3" aria-selected="false" tabindex="-1">03 Check</button>
  <button class="tab" role="tab" id="tab-4" aria-controls="panel-4" aria-selected="false" tabindex="-1">04 Method &amp; export</button>
</div>

<div class="cols">
<aside class="rail" aria-label="Filters">
  <div class="railhead">
    <span class="mono" style="color:var(--ink)">Filters</span>
    <button class="mono" id="clear-all" style="appearance:none;background:none;border:none;cursor:pointer;color:var(--red);letter-spacing:.08em">Clear all</button>
  </div>
  <div class="bignum" id="rail-count">0</div>
  <div class="matchlabel" id="rail-of">of N in the file</div>
  <div class="sharetrack"><div class="sharebar" id="rail-bar" style="width:0%"></div></div>
  <div class="matchlabel" id="rail-share"></div>
  <div class="chips" id="rail-chips"></div>
  <div id="rail-groups">
    <div class="fgroup">
      <button class="fhead" id="fh-1" aria-expanded="false"><span><span class="n">01</span>Keyword</span><span class="arrow">▼</span></button>
      <div class="fbody" id="fb-1" hidden>
        <input type="text" id="kw-input" placeholder="e.g. torture" aria-label="Keyword">
        <div class="hint">literal match, not synonyms</div>
      </div>
    </div>
    <div class="fgroup">
      <button class="fhead" id="fh-2" aria-expanded="false"><span><span class="n">02</span>Mechanism, body, type</span><span class="arrow">▼</span></button>
      <div class="fbody" id="fb-2" hidden>
        <label for="sel-mech">Mechanism</label>
        <select id="sel-mech"></select>
        <label for="sel-body">Body or mandate</label>
        <select id="sel-body"></select>
        <label for="sel-type">Type</label>
        <select id="sel-type"></select>
        <div id="state-filter-wrap" hidden>
          <label for="sel-state">Recommending State (UPR)</label>
          <select id="sel-state"></select>
        </div>
      </div>
    </div>
    <div class="fgroup">
      <button class="fhead" id="fh-3" aria-expanded="false"><span><span class="n">03</span>Years and SDG</span><span class="arrow">▼</span></button>
      <div class="fbody" id="fb-3" hidden>
        <div class="yearrow">
          <div style="flex:1"><label for="sel-yfrom">Year from</label><select id="sel-yfrom"></select></div>
          <div style="flex:1"><label for="sel-yto">to</label><select id="sel-yto"></select></div>
        </div>
        <label for="sel-sdg">SDG goal</label>
        <select id="sel-sdg"></select>
      </div>
    </div>
  </div>
</aside>

<main>
  <section class="tabpanel" role="tabpanel" id="panel-1" aria-labelledby="tab-1">
    <div class="tiles" id="ov-tiles"></div>
    <figure>
      <div class="figno">FIG.01</div>
      <h2 id="fig1-title">Ten most frequent themes</h2>
      <div class="figsub" id="fig1-sub"></div>
      <div class="chartbox" id="fig1-box"><canvas id="fig1" aria-label="Ten most frequent themes, horizontal bar chart"></canvas></div>
      <div class="figsrc" id="fig1-src"></div>
      <div id="fig1-tablewrap"></div>
    </figure>
    <figure>
      <div class="figno">FIG.02</div>
      <h2>Records per year by mechanism</h2>
      <div class="figsub" id="fig2-sub"></div>
      <div class="chartbox tall" id="fig2-box"><canvas id="fig2" aria-label="Records per year by mechanism, stacked bar chart"></canvas></div>
      <div class="figsrc" id="fig2-src"></div>
    </figure>
  </section>

  <section class="tabpanel" role="tabpanel" id="panel-2" aria-labelledby="tab-2" hidden>
    <div style="margin-bottom:6px">
      <input type="text" id="kw-input-2" placeholder="" aria-label="Search records" style="width:100%;max-width:520px;padding:9px 10px;border:1px solid var(--rule);background:#faf7f0;font-size:15px">
      <div class="hint">Searches text and document symbol · literal match, not synonyms</div>
    </div>
    <div id="rec-tablewrap"></div>
    <div style="margin-top:14px"><button class="btn" id="more-btn">Show 50 more</button></div>
  </section>

  <section class="tabpanel" role="tabpanel" id="panel-3" aria-labelledby="tab-3" hidden>
    <h2 class="sec" style="margin-top:0">How the app checks itself</h2>
    <p class="fineprint">Each line compares two values computed independently. A failure is shown, never hidden. Checks marked on the whole file use all records, not the current filter.</p>
    <div id="checks"></div>
    <h2 class="sec">Check the UN's own labels on a random sample</h2>
    <p class="fineprint">This is your judgement of the UN's labels; nothing is sent anywhere. One verdict per card is about the themes as a set: do these labels fit this paragraph?</p>
    <div class="samplectl">
      <button class="btn primary" id="draw-btn">Check 10 at random</button>
      <span id="draw-again-wrap" hidden>
        <button class="btn" id="draw-again">Draw again</button>
        <label class="mono" for="seed-input" style="color:#6b6255">Seed</label>
        <input type="text" id="seed-input" value="1" aria-label="Seed">
        <button class="btn" id="draw-seed">Draw with this seed</button>
      </span>
    </div>
    <div class="tally" id="sample-tally" aria-live="polite"></div>
    <div id="sample-cards"></div>
  </section>

  <section class="tabpanel" role="tabpanel" id="panel-4" aria-labelledby="tab-4" hidden>
    <h2 class="sec" style="margin-top:0">How each number is computed</h2>
    <div class="method" id="method-text"></div>
    <h2 class="sec">Take it with you</h2>
    <div class="actions" style="margin:0 0 6px">
      <button class="btn primary" id="csv-btn">Download CSV of the current filter</button>
      <button class="btn" id="summary-btn">Copy summary</button>
      <span class="copied" id="export-msg"></span>
    </div>
    <p class="fineprint">The CSV carries the visible columns plus the full text and all labels, preceded by comment lines naming the country, source, build date, filters applied and row count. The summary is plain text for pasting into notes. Both are generated in your browser; nothing is sent anywhere.</p>
    <h2 class="sec">Source</h2>
    <p class="fineprint" id="src-note"></p>
  </section>
</main>
</div>

<footer class="app">
  <span id="ft-left">Built on OHCHR UHRI data</span>
  <span id="ft-right"></span>
</footer>
</div>

<script>
(function(){
"use strict";
const U = window.WORKSHOP_DATA && window.WORKSHOP_DATA.uhri;
if(!U || !U.records){document.body.innerHTML="<p>No UHRI data found.</p>";return;}
const recs = U.records;
const N = recs.length;
const fmt = n => String(n).replace(/\B(?=(\d{3})+(?!\d))/g,",");

/* ---------- precomputation ---------- */
const PARA_RE = /^(\d{1,3}(?:\.\d{1,3})?)\.?\s/;
const STATE_RUN_RE = /((?:\s*\((?:[^()]|\([^()]*\))*\))+)\s*[;.]?\s*$/;
const STATE_GROUP_RE = /\((?:[^()]|\([^()]*\))*\)/g;
function statesOf(r){
  if(r.mechanism !== "Universal Periodic Review") return null;
  const m = (r.text||"").match(STATE_RUN_RE);
  if(!m) return {states:["State not found"]};
  const groups = m[1].match(STATE_GROUP_RE) || [];
  const out = [];
  for(let g of groups){
    let s = g.replace(/^\(/,"").replace(/\)$/,"").trim();
    if(s && !s.includes(",") && s.length <= 60) out.push(s);
    else return {states:["State not found"]};
  }
  if(!out.length) return {states:["State not found"]};
  return {states:out};
}
recs.forEach(r=>{
  const pm = (r.text||"").match(PARA_RE);
  r._para = pm ? pm[1] : null;
  const st = statesOf(r);
  r._states = st ? st.states : null;
});

/* ---------- filter state ---------- */
const f = {keywordWords:[], mechanism:"", body:"", type:"", state:"", yearFrom:"", yearTo:"", sdg:"", themes:new Set()};
let filtered = recs.slice();
let expandedIds = new Set();
let shown = 50;

function matches(r){
  if(f.keywordWords.length){
    const t=(r.text||"").toLowerCase(), s=(r.symbol||"").toLowerCase();
    for(const w of f.keywordWords) if(!t.includes(w) && !s.includes(w)) return false;
  }
  if(f.mechanism && r.mechanism !== f.mechanism) return false;
  if(f.body && r.body !== f.body) return false;
  if(f.type && r.type !== f.type) return false;
  if(f.state){
    if(!r._states || !r._states.some(x=>x===f.state)) return false;
  }
  if(f.yearFrom!=="" && r.year < +f.yearFrom) return false;
  if(f.yearTo!=="" && r.year > +f.yearTo) return false;
  if(f.sdg!=="" && !((r.sdgs||[]).includes(+f.sdg))) return false;
  if(f.themes.size && !(r.themes||[]).some(t=>f.themes.has(t))) return false;
  return true;
}

function esc(s){return String(s==null?"":s).replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;").replace(/"/g,"&quot;");}

/* ---------- header & footer ---------- */
(function(){
  document.getElementById("hd-label").textContent = "UHRI · " + U.country;
  document.getElementById("hd-title").textContent = "UN human rights recommendations and observations: " + U.country;
  const years = recs.map(r=>r.year);
  const y0 = Math.min(...years), y1 = Math.max(...years);
  const docs = new Set(recs.map(r=>r.symbol)).size;
  document.getElementById("hd-src").innerHTML =
    'Source: <a href="'+esc(U.source_url)+'" target="_blank" rel="noopener">'+esc(U.source)+'</a>'
    + ' · <span class="mono">'+fmt(N)+' records · '+fmt(docs)+' documents · '+y0+'–'+y1+'</span>'
    + ' · <span class="mono">built '+esc(U.built)+'</span>'
    + ' · <span class="mono">dated by document</span>';
  document.getElementById("ft-left").innerHTML =
    'Built on OHCHR UHRI data · '+fmt(N)+' records · <a href="'+esc(U.source_url)+'" target="_blank" rel="noopener">source</a>';
  document.getElementById("ft-right").textContent = 'Country: ' + U.country + ' · no model calls · no network requests';
})();

/* ---------- tabs ---------- */
const tabs=[...document.querySelectorAll(".tab")];
const panels=tabs.map(t=>document.getElementById(t.getAttribute("aria-controls")));
let curTab=0;
function selectTab(i){
  curTab=i;
  tabs.forEach((t,j)=>{t.setAttribute("aria-selected",j===i?"true":"false");t.tabIndex=j===i?0:-1;});
  panels.forEach((p,j)=>p.hidden=j!==i);
  document.getElementById("rail-groups").hidden = (i>=2);
  if(i===0) renderOverview();
  if(i===1) renderTable();
}
tabs.forEach((t,i)=>{
  t.addEventListener("click",()=>selectTab(i));
  t.addEventListener("keydown",e=>{
    let j=null;
    if(e.key==="ArrowRight")j=(i+1)%tabs.length;
    if(e.key==="ArrowLeft")j=(i-1+tabs.length)%tabs.length;
    if(j!==null){e.preventDefault();selectTab(j);tabs[j].focus();}
  });
});

/* ---------- collapsible filter headings ---------- */
["1","2","3"].forEach(n=>{
  const h=document.getElementById("fh-"+n), b=document.getElementById("fb-"+n);
  h.addEventListener("click",()=>{
    const open=h.getAttribute("aria-expanded")==="true";
    ["1","2","3"].forEach(m=>{
      document.getElementById("fh-"+m).setAttribute("aria-expanded","false");
      document.getElementById("fb-"+m).hidden=true;
    });
    if(!open){h.setAttribute("aria-expanded","true");b.hidden=false;}
  });
});

/* ---------- selects ---------- */
function distinctSorted(arr){return [...new Set(arr.filter(x=>x!=null&&x!==""))].sort((a,b)=>a<b?-1:a>b?1:0);}
function fillSel(el,items,allLabel){
  el.innerHTML="";
  const o=document.createElement("option");o.value="";o.textContent=allLabel;el.appendChild(o);
  items.forEach(it=>{
    const o=document.createElement("option");o.value=it.v;o.textContent=it.label;el.appendChild(o);
  });
}
const allYears = distinctSorted(recs.map(r=>r.year));
const sdgCounts={};
recs.forEach(r=>(r.sdgs||[]).forEach(g=>sdgCounts[g]=(sdgCounts[g]||0)+1));
const sdgNames=U.sdg_names||{};
const sdgGoals=Object.keys(sdgCounts).map(Number).sort((a,b)=>a-b);
const mechanisms = distinctSorted(recs.map(r=>r.mechanism));
const allTypes = distinctSorted(recs.map(r=>r.type));

function bodyOptions(){
  const src = f.mechanism ? recs.filter(r=>r.mechanism===f.mechanism) : recs;
  const cnt={};
  src.forEach(r=>cnt[r.body]=(cnt[r.body]||0)+1);
  return Object.keys(cnt).sort((a,b)=>cnt[b]-cnt[a]||(a<b?-1:1)).map(b=>({v:b,label:b+" ("+cnt[b]+")"}));
}
function stateOptions(){
  const cnt={};
  filtered.forEach(r=>{ if(r._states) r._states.forEach(s=>{ if(s!=="State not found") cnt[s]=(cnt[s]||0)+1; }); });
  return Object.keys(cnt).sort((a,b)=>cnt[b]-cnt[a]||(a<b?-1:1)).map(s=>({v:s,label:s+" ("+cnt[s]+")"}));
}

function rebuildMechDependent(){
  fillSel(document.getElementById("sel-body"),bodyOptions(),"all bodies");
  const prevBody=f.body;
  if(prevBody && !bodyOptions().some(o=>o.v===prevBody)) f.body="";
  document.getElementById("sel-body").value=f.body;
  const typeSrc = (f.mechanism?recs.filter(r=>r.mechanism===f.mechanism):recs);
  const tc={};typeSrc.forEach(r=>tc[r.type]=(tc[r.type]||0)+1);
  fillSel(document.getElementById("sel-type"),Object.keys(tc).map(t=>({v:t,label:t+" ("+tc[t]+")"})),"all types");
  if(f.type && !(f.type in tc)){f.type="";}
  document.getElementById("sel-type").value=f.type;
}
(function initSelects(){
  fillSel(document.getElementById("sel-mech"),mechanisms.map(m=>({v:m,label:m})),"all mechanisms");
  fillSel(document.getElementById("sel-yfrom"),allYears.map(y=>({v:y,label:y})),"—");
  fillSel(document.getElementById("sel-yto"),allYears.map(y=>({v:y,label:y})),"—");
  fillSel(document.getElementById("sel-sdg"),sdgGoals.map(g=>({v:g,label:"SDG "+g+(sdgNames[String(g)]?" · "+sdgNames[String(g)]:"")+" ("+sdgCounts[g]+")"})),"all goals");
  rebuildMechDepinite:0;
})();
</script>
<script>
/* second script block not needed; continue below */
</script>
</body>
</html>
```

I noticed a syntax error in the block above (`rebuildMechDepinite`), so here is the complete, corrected file — please use this one:

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>UN human rights recommendations and observations</title>
<style>
  :root{
    --paper:#f4f0e8; --ink:#1d1b18; --rule:#d9d2c3; --red:#9b2335;
    --upr:#c2410c; --tb:#0f766e; --sp:#7c3aed;
    --mono:ui-monospace,Menlo,Consolas,monospace;
    --serif:Georgia,"Times New Roman",serif;
    --sans:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;
  }
  [hidden]{display:none!important}
  *{box-sizing:border-box}
  body{margin:0;background:var(--paper);color:var(--ink);font-family:var(--sans);font-size:16px;line-height:1.5}
  a{color:var(--red)}
  a:focus-visible,button:focus-visible,input:focus-visible,select:focus-visible,[tabindex]:focus-visible{outline:2px solid var(--red);outline-offset:2px}
  .mono{font-family:var(--mono);font-size:11px;letter-spacing:.12em;text-transform:uppercase}
  .wrap{max-width:1180px;margin:0 auto;padding:20px 24px 40px}

  header.app{border-bottom:2px solid var(--ink);padding-bottom:14px}
  .datalabel{font-family:var(--mono);font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:#6b6255}
  h1{font-family:var(--serif);font-weight:400;font-size:33px;line-height:1.15;margin:6px 0 8px}
  .srcline{font-size:13.5px;color:#4a443b}
  .srcline .mono{margin-left:12px}

  .tabs{display:flex;border-bottom:1px solid var(--rule);margin-bottom:18px;flex-wrap:wrap}
  .tab{appearance:none;background:none;border:none;border-bottom:3px solid transparent;cursor:pointer;
    font-family:var(--mono);font-size:11.5px;letter-spacing:.1em;text-transform:uppercase;color:#5a5248;
    padding:12px 18px 10px;margin-right:4px}
  .tab[aria-selected="true"]{color:var(--red);border-bottom-color:var(--red)}
  .tab:hover{color:var(--ink)}
  .tabpanel{margin-top:4px}

  .cols{display:flex;gap:28px;align-items:flex-start}
  aside.rail{width:252px;flex:0 0 252px;border-right:1px solid var(--rule);padding-right:20px}
  main{flex:1;min-width:0}
  @media(max-width:840px){.cols{flex-direction:column}aside.rail{width:100%;flex:none;border-right:none;border-bottom:1px solid var(--rule);padding:0 0 14px}}

  .railhead{display:flex;justify-content:space-between;align-items:baseline;border-bottom:1px solid var(--rule);padding-bottom:6px}
  .bignum{font-family:var(--serif);font-size:46px;line-height:1.05;margin:14px 0 2px}
  .bignum small{font-size:16px;color:#5a5248;font-family:var(--sans)}
  .matchlabel{font-family:var(--mono);font-size:11px;letter-spacing:.1em;text-transform:uppercase;color:#6b6255}
  .sharetrack{height:5px;background:#e7e0d2;margin:10px 0 4px}
  .sharebar{height:5px;background:var(--red)}
  .chips{display:flex;flex-wrap:wrap;gap:6px;margin:10px 0 4px}
  .chip{display:inline-flex;align-items:center;gap:6px;border:1px solid var(--rule);background:#faf7f0;
    font-size:12.5px;padding:3px 6px 3px 9px;border-radius:999px}
  .chip button{appearance:none;border:none;background:none;cursor:pointer;font-size:14px;line-height:1;color:var(--red);padding:0 2px}
  .fgroup{border-bottom:1px solid var(--rule)}
  .fhead{width:100%;display:flex;justify-content:space-between;align-items:center;appearance:none;background:none;border:none;cursor:pointer;
    font-family:var(--mono);font-size:11.5px;letter-spacing:.1em;text-transform:uppercase;color:var(--ink);padding:12px 0 10px}
  .fhead .n{color:var(--red);margin-right:8px}
  .fhead .arrow{color:#8a8072;font-size:10px}
  .fbody{padding:2px 0 16px}
  .fbody label{display:block;font-size:11.5px;color:#5a5248;margin:8px 0 3px;font-family:var(--mono);letter-spacing:.06em;text-transform:uppercase}
  .fbody input[type=text],.fbody select{width:100%;padding:7px 8px;border:1px solid var(--rule);background:#faf7f0;font-family:var(--sans);font-size:14px;color:var(--ink)}
  .hint{font-size:12px;color:#7a7263;margin-top:5px;font-family:var(--mono);letter-spacing:.02em}
  .yearrow{display:flex;gap:8px}

  .tiles{display:flex;flex-wrap:wrap;border-top:1px solid var(--rule);border-left:1px solid var(--rule);margin-bottom:26px}
  .tile{flex:1 1 200px;border-right:1px solid var(--rule);border-bottom:1px solid var(--rule);padding:16px 18px 12px;min-width:190px}
  .tile .lbl{font-family:var(--mono);font-size:11px;letter-spacing:.12em;text-transform:uppercase;color:#6b6255}
  .tile .num{font-family:var(--serif);font-size:42px;line-height:1.1;margin:4px 0 2px}
  .tile .sub{font-size:12.5px;color:#5a5248;line-height:1.45}
  .tile .dot{display:inline-block;width:9px;height:9px;border-radius:50%;margin-right:6px}
  .tile .how{font-size:11px;color:#8a8072;font-family:var(--mono);letter-spacing:.02em;margin-top:6px}
  .linkish{appearance:none;background:none;border:none;cursor:pointer;color:var(--red);font-size:12.5px;padding:0;text-decoration:underline;font-family:var(--sans)}

  figure{margin:0 0 34px}
  figure .figno{font-family:var(--mono);font-size:11px;letter-spacing:.14em;color:var(--red)}
  figure h2{font-family:var(--serif);font-weight:400;font-size:20px;margin:4px 0 2px}
  figure .figsub{font-size:13px;color:#5a5248;margin-bottom:10px}
  figure .figsrc{font-size:11.5px;color:#8a8072;margin-top:6px}
  .chartbox{position:relative;height:340px}
  .chartbox.tall{height:380px}
  .nomatch{font-family:var(--serif);font-size:20px;color:#8a8072;padding:40px 0;text-align:center}

  table{border-collapse:collapse;width:100%;font-size:14.5px}
  caption{text-align:left;font-family:var(--mono);font-size:11px;letter-spacing:.08em;text-transform:uppercase;color:#6b6255;padding-bottom:8px}
  th,td{text-align:left;vertical-align:top;padding:7px 10px 7px 0;border-bottom:1px solid var(--rule)}
  th{font-family:var(--mono);font-size:10.5px;letter-spacing:.1em;text-transform:uppercase;color:#5a5248;font-weight:400;border-bottom:1.5px solid #b8ae99}
  th .arrow{color:var(--red)}
  td.num,th.num{text-align:right;font-variant-numeric:tabular-nums}
  tr.rec{cursor:pointer}
  tr.rec:hover{background:#efe9dc}
  tr.rec td{border-bottom:1px solid #e4dcc9}
  mark{background:#f3d9a4;color:var(--ink);padding:0 1px}
  tr.expand td{background:#faf7f0;padding:18px 16px 20px;border-bottom:2px solid var(--red)}
  .para-big{font-family:var(--serif);font-size:38px;color:var(--red);line-height:1;margin-right:18px;float:left}
  .fulltext{font-size:15.5px;line-height:1.6;white-space:pre-wrap}
  .labelrow{margin-top:14px;clear:none}
  .labelrow .lbl{font-family:var(--mono);font-size:10.5px;letter-spacing:.1em;text-transform:uppercase;color:#6b6255;margin-bottom:3px}
  .taglist{display:flex;flex-wrap:wrap;gap:5px}
  .tag{border:1px solid var(--rule);background:#f4f0e8;font-size:12.5px;padding:2px 8px}
  .actions{margin-top:16px;display:flex;gap:10px;flex-wrap:wrap;align-items:center}
  .btn{appearance:none;cursor:pointer;font-family:var(--sans);font-size:13.5px;color:var(--ink);background:#faf7f0;border:1px solid #b8ae99;padding:6px 14px}
  .btn:hover{border-color:var(--ink)}
  .btn.primary{background:var(--red);color:#fff;border-color:var(--red)}
  .copied{color:var(--red);font-size:12.5px;font-family:var(--mono)}
  .dash{color:#a99f8b}
  .statelist{margin-top:10px;border-top:1px solid var(--rule);padding-top:10px}
  .statelist .lbl{font-family:var(--mono);font-size:11px;letter-spacing:.1em;text-transform:uppercase;color:#6b6255;margin-bottom:4px}
  .statelist ol{margin:6px 0 0;padding-left:22px;font-size:13.5px}
  .statelist li{margin:2px 0}

  .checkline{display:flex;gap:14px;padding:9px 0;border-bottom:1px solid var(--rule);font-size:14px;align-items:baseline}
  .checkline .mark{font-family:var(--mono);font-size:11px;letter-spacing:.08em;white-space:nowrap}
  .pass{color:#0f766e}.fail{color:var(--red)}.warn{color:#a16207}
  .checkline .what{flex:1}
  .checkline .vals{font-family:var(--mono);font-size:12px;color:#5a5248}
  h2.sec{font-family:var(--serif);font-weight:400;font-size:22px;border-bottom:1px solid var(--rule);padding-bottom:6px;margin:26px 0 8px}
  .samplectl{display:flex;gap:10px;align-items:center;flex-wrap:wrap;margin:12px 0}
  .samplectl input{width:90px;padding:6px 8px;border:1px solid var(--rule);background:#faf7f0;font-family:var(--mono);font-size:13px}
  .card{border:1px solid var(--rule);border-left:3px solid var(--rule);margin-bottom:8px}
  .card.vfit{border-left-color:#0f766e}
  .card.vno{border-left-color:var(--red)}
  .card.vunsure{border-left-color:#a16207}
  .cardhead{width:100%;display:flex;gap:14px;align-items:baseline;appearance:none;background:none;border:none;cursor:pointer;padding:10px 14px;text-align:left;font-size:14px}
  .cardhead .csym{font-family:var(--mono);font-size:12px;white-space:nowrap}
  .cardhead .cpara{font-family:var(--serif);color:var(--red);font-size:17px;min-width:56px}
  .cardhead .csnip{color:#5a5248;flex:1;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
  .cardbody{padding:0 16px 16px;border-top:1px solid var(--rule)}
  .cardbody .fulltext{margin-top:12px}
  .vbtns{display:flex;gap:8px;margin-top:12px}
  .vbtn.on{background:var(--ink);color:#fff;border-color:var(--ink)}
  .tally{font-size:14px;margin:10px 0}
  .tally .mono{color:var(--red)}

  .method p{max-width:72ch;font-size:15px}
  .fineprint{font-size:13px;color:#5a5248;max-width:72ch}

  footer.app{border-top:2px solid var(--ink);margin-top:30px;padding-top:10px;font-family:var(--mono);font-size:11px;letter-spacing:.08em;color:#6b6255;display:flex;justify-content:space-between;flex-wrap:wrap;gap:8px}
</style>
</head>
<body>
<div class="wrap">

<header class="app">
  <div class="datalabel" id="hd-label">UHRI</div>
  <h1 id="hd-title">UN human rights recommendations and observations</h1>
  <div class="srcline" id="hd-src"></div>
</header>

<div class="tabs" role="tablist" aria-label="Dashboard sections">
  <button class="tab" role="tab" id="tab-1" aria-controls="panel-1" aria-selected="true" tabindex="0">01 Overview</button>
  <button class="tab" role="tab" id="tab-2" aria-controls="panel-2" aria-selected="false" tabindex="-1">02 Records</button>
  <button class="tab" role="tab" id="tab-3" aria-controls="panel-3" aria-selected="false" tabindex="-1">03 Check</button>
  <button class="tab" role="tab" id="tab-4" aria-controls="panel-4" aria-selected="false" tabindex="-1">04 Method &amp; export</button>
</div>

<div class="cols">
<aside class="rail" aria-label="Filters">
  <div class="railhead">
    <span class="mono" style="color:var(--ink)">Filters</span>
    <button class="mono" id="clear-all" style="appearance:none;background:none;border:none;cursor:pointer;color:var(--red);letter-spacing:.08em">Clear all</button>
  </div>
  <div class="bignum" id="rail-count">0</div>
  <div class="matchlabel" id="rail-of">of N in the file</div>
  <div class="sharetrack"><div class="sharebar" id="rail-bar" style="width:0%"></div></div>
  <div class="matchlabel" id="rail-share"></div>
  <div class="chips" id="rail-chips"></div>
  <div id="rail-groups">
    <div class="fgroup">
      <button class="fhead" id="fh-1" aria-expanded="false"><span><span class="n">01</span>Keyword</span><span class="arrow">▼</span></button>
      <div class="fbody" id="fb-1" hidden>
        <input type="text" id="kw-input" placeholder="e.g. torture" aria-label="Keyword">
        <div class="hint">literal match, not synonyms</div>
      </div>
    </div>
    <div class="fgroup">
      <button class="fhead" id="fh-2" aria-expanded="false"><span><span class="n">02</span>Mechanism, body, type</span><span class="arrow">▼</span></button>
      <div class="fbody" id="fb-2" hidden>
        <label for="sel-mech">Mechanism</label>
        <select id="sel-mech"></select>
        <label for="sel-body">Body or mandate</label>
        <select id="sel-body"></select>
        <label for="sel-type">Type</label>
        <select id="sel-type"></select>
        <div id="state-filter-wrap" hidden>
          <label for="sel-state">Recommending State (UPR)</label>
          <select id="sel-state"></select>
        </div>
      </div>
    </div>
    <div class="fgroup">
      <button class="fhead" id="fh-3" aria-expanded="false"><span><span class="n">03</span>Years and SDG</span><span class="arrow">▼</span></button>
      <div class="fbody" id="fb-3" hidden>
        <div class="yearrow">
          <div style="flex:1"><label for="sel-yfrom">Year from</label><select id="sel-yfrom"></select></div>
          <div style="flex:1"><label for="sel-yto">to</label><select id="sel-yto"></select></div>
        </div>
        <label for="sel-sdg">SDG goal</label>
        <select id="sel-sdg"></select>
      </div>
    </div>
  </div>
</aside>

<main>
  <section class="tabpanel" role="tabpanel" id="panel-1" aria-labelledby="tab-1">
    <div class="tiles" id="ov-tiles"></div>
    <figure>
      <div class="figno">FIG.01</div>
      <h2 id="fig1-title">Ten most frequent themes</h2>
      <div class="figsub" id="fig1-sub"></div>
      <div class="chartbox" id="fig1-box"><canvas id="fig1" aria-label="Ten most frequent themes, horizontal bar chart"></canvas></div>
      <div class="figsrc" id="fig1-src"></div>
      <div id="fig1-tablewrap"></div>
    </figure>
    <figure>
      <div class="figno">FIG.02</div>
      <h2>Records per year by mechanism</h2>
      <div class="figsub" id="fig2-sub"></div>
      <div class="chartbox tall" id="fig2-box"><canvas id="fig2" aria-label="Records per year by mechanism, stacked bar chart"></canvas></div>
      <div class="figsrc" id="fig2-src"></div>
    </figure>
  </section>

  <section class="tabpanel" role="tabpanel" id="panel-2" aria-labelledby="tab-2" hidden>
    <div style="margin-bottom:6px">
      <input type="text" id="kw-input-2" aria-label="Search records" style="width:100%;max-width:520px;padding:9px 10px;border:1px solid var(--rule);background:#faf7f0;font-size:15px">
      <div class="hint">Searches text and document symbol · literal match, not synonyms</div>
    </div>
    <div id="rec-tablewrap"></div>
    <div style="margin-top:14px"><button class="btn" id="more-btn">Show 50 more</button></div>
  </section>

  <section class="tabpanel" role="tabpanel" id="panel-3" aria-labelledby="tab-3" hidden>
    <h2 class="sec" style="margin-top:0">How the app checks itself</h2>
    <p class="fineprint">Each line compares two values computed independently. A failure is shown, never hidden. Checks marked "whole file" use all records, not the current filter.</p>
    <div id="checks"></div>
    <h2 class="sec">Check the UN's own labels on a random sample</h2>
    <p class="fineprint">This is your judgement of the UN's labels; nothing is sent anywhere. One verdict per card is about the themes as a set: do these labels fit this paragraph?</p>
    <div class="samplectl">
      <button class="btn primary" id="draw-btn">Check 10 at random</button>
      <span id="draw-again-wrap" hidden>
        <button class="btn" id="draw-again">Draw again</button>
        <label class="mono" for="seed-input" style="color:#6b6255">Seed</label>
        <input type="text" id="seed-input" value="1" aria-label="Seed">
        <button class="btn" id="draw-seed">Draw with this seed</button>
      </span>
    </div>
    <div class="tally" id="sample-tally" aria-live="polite"></div>
    <div id="sample-cards"></div>
  </section>

  <section class="tabpanel" role="tabpanel" id="panel-4" aria-labelledby="tab-4" hidden>
    <h2 class="sec" style="margin-top:0">How each number is computed</h2>
    <div class="method" id="method-text"></div>
    <h2 class="sec">Take it with you</h2>
    <div class="actions" style="margin:0 0 6px">
      <button class="btn primary" id="csv-btn">Download CSV of the current filter</button>
      <button class="btn" id="summary-btn">Copy summary</button>
      <span class="copied" id="export-msg"></span>
    </div>
    <p class="fineprint">The CSV carries the visible columns plus the full text and all labels, preceded by comment lines naming the country, source, build date, filters applied and row count. The summary is plain text for pasting into notes. Both are generated in your browser; nothing is sent anywhere.</p>
    <h2 class="sec">Source</h2>
    <p class="fineprint" id="src-note"></p>
  </section>
</main>
</div>

<footer class="app">
  <span id="ft-left">Built on OHCHR UHRI data</span>
  <span id="ft-right"></span>
</footer>
</div>

<script>
(function(){
"use strict";
const U = window.WORKSHOP_DATA && window.WORKSHOP_DATA.uhri;
if(!U || !U.records){document.body.innerHTML="<p>No UHRI data found.</p>";return;}
const recs = U.records;
const N = recs.length;
const fmt = n => String(n).replace(/\B(?=(\d{3})+(?!\d))/g,",");

/* ---------- precomputation ---------- */
const PARA_RE = /^(\d{1,3}(?:\.\d{1,3})?)\.?\s/;
const STATE_RUN_RE = /((?:\s*\((?:[^()]|\([^()]*\))*\))+)\s*[;.]?\s*$/;
const STATE_GROUP_RE = /\((?:[^()]|\([^()]*\))*\)/g;
function statesOf(r){
  if(r.mechanism !== "Universal Periodic Review") return null;
  const m = (r.text||"").match(STATE_RUN_RE);
  if(!m) return ["State not found"];
  const groups = m[1].match(STATE_GROUP_RE) || [];
  const out = [];
  for(let g of groups){
    const s = g.replace(/^\(/,"").replace(/\)$/,"").trim();
    if(s && !s.includes(",") && s.length <= 60) out.push(s);
    else return ["State not found"];
  }
  return out.length ? out : ["State not found"];
}
recs.forEach(r=>{
  const pm = (r.text||"").match(PARA_RE);
  r._para = pm ? pm[1] : null;
  r._states = statesOf(r);
});
const paraNum = p => { const n = parseFloat(p); return isNaN(n) ? 1e9 : n; };
const sortedRecs = recs.map((r,i)=>({r,i}))
  .sort((a,b)=> (b.r.date||"").localeCompare(a.r.date||"") || (a.r.body||"").localeCompare(b.r.body||"") || (paraNum(a.r._para||"")-paraNum(b.r._para||"")) || a.i-b.i)
  .map(x=>x.r);

/* ---------- filter state ---------- */
const f = {keywordWords:[], keyword:"", mechanism:"", body:"", type:"", state:"", yearFrom:"", yearTo:"", sdg:"", themes:new Set()};
let filtered = recs.slice();
let expandedIds = new Set();
let shown = 50;
let dateDesc = true;

function matches(r){
  if(f.keywordWords.length){
    const t=(r.text||"").toLowerCase(), s=(r.symbol||"").toLowerCase();
    for(const w of f.keywordWords) if(!t.includes(w) && !s.includes(w)) return false;
  }
  if(f.mechanism && r.mechanism !== f.mechanism) return false;
  if(f.body && r.body !== f.body) return false;
  if(f.type && r.type !== f.type) return false;
  if(f.state && !(r._states && r._states.some(x=>x===f.state))) return false;
  if(f.yearFrom!=="" && r.year < +f.yearFrom) return false;
  if(f.yearTo!=="" && r.year > +f.yearTo) return false;
  if(f.sdg!=="" && !((r.sdgs||[]).includes(+f.sdg))) return false;
  if(f.themes.size && !(r.themes||[]).some(t=>f.themes.has(t))) return false;
  return true;
}

function esc(s){return String(s==null?"":s).replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;").replace(/"/g,"&quot;");}
function escAttr(s){return esc(s).replace(/'/g,"&#39;");}

/* ---------- header & footer ---------- */
const yearsAll = recs.map(r=>r.year);
const y0 = Math.min(...yearsAll), y1 = Math.max(...yearsAll);
const docsAll = new Set(recs.map(r=>r.symbol)).size;
document.getElementById("hd-label").textContent = "UHRI · " + U.country;
document.getElementById("hd-title").textContent = "UN human rights recommendations and observations: " + U.country;
document.getElementById("hd-src").innerHTML =
  'Source: <a href="'+esc(U.source_url)+'" target="_blank" rel="noopener">'+esc(U.source)+'</a>'
  + ' <span class="mono">'+fmt(N)+' records · '+fmt(docsAll)+' documents · '+y0+'–'+y1+'</span>'
  + ' <span class="mono">built '+esc(U.built)+'</span>'
  + ' <span class="mono">dated by document</span>';
document.getElementById("ft-left").innerHTML =
  'Built on OHCHR UHRI data · '+fmt(N)+' records · <a href="'+esc(U.source_url)+'" target="_blank" rel="noopener">source</a>';
document.getElementById("ft-right").textContent = 'Country: ' + U.country + ' · no model calls · no network requests';

/* ---------- tabs ---------- */
const tabs=[...document.querySelectorAll(".tab")];
const panels=tabs.map(t=>document.getElementById(t.getAttribute("aria-controls")));
let curTab=0;
function selectTab(i){
  curTab=i;
  tabs.forEach((t,j)=>{t.setAttribute("aria-selected",j===i?"true":"false");t.tabIndex=j===i?0:-1;});
  panels.forEach((p,j)=>p.hidden=j!==i);
  document.getElementById("rail-groups").hidden = (i>=2);
  if(i===0) renderOverview();
  if(i===1) renderTable();
  if(i===3) renderMethod();
}
tabs.forEach((t,i)=>{
  t.addEventListener("click",()=>selectTab(i));
  t.addEventListener("keydown",e=>{
    let j=null;
    if(e.key==="ArrowRight")j=(i+1)%tabs.length;
    if(e.key==="ArrowLeft")j=(i-1+tabs.length)%tabs.length;
    if(j!==null){e.preventDefault();selectTab(j);tabs[j].focus();}
  });
});

/* ---------- collapsible filter headings ---------- */
["1","2","3"].forEach(n=>{
  const h=document.getElementById("fh-"+n), b=document.getElementById("fb-"+n);
  h.addEventListener("click",()=>{
    const open=h.getAttribute("aria-expanded")==="true";
    ["1","2","3"].forEach(m=>{
      document.getElementById("fh-"+m).setAttribute("aria-expanded","false");
      document.getElementById("fb-"+m).hidden=true;
    });
    if(!open){h.setAttribute("aria-expanded","true");b.hidden=false;}
  });
});

/* ---------- selects ---------- */
function distinctSorted(arr){return [...new Set(arr.filter(x=>x!=null&&x!==""))].sort((a,b)=>a<b?-1:a>b?1:0);}
function fillSel(el,items,allLabel){
  el.innerHTML="";
  const o=document.createElement("option");o.value="";o.textContent=allLabel;el.appendChild(o);
  items.forEach(it=>{
    const o=document.createElement("option");o.value=it.v;o.textContent=it.label;el.appendChild(o);
  });
}
const allYears = distinctSorted(recs.map(r=>r.year));
const sdgCounts={};
recs.forEach(r=>(r.sdgs||[]).forEach(g=>sdgCounts[g]=(sdgCounts[g]||0)+1));
const sdgNames=U.sdg_names||{};
const sdgGoals=Object.keys(sdgCounts).map(Number).sort((a,b)=>a-b);
const mechanisms = distinctSorted(recs.map(r=>r.mechanism));

function bodyOptions(){
  const src = f.mechanism ? recs.filter(r=>r.mechanism===f.mechanism) : recs;
  const cnt={};
  src.forEach(r=>cnt[r.body]=(cnt[r.body]||0)+1);
  return Object.keys(cnt).sort((a,b)=>cnt[b]-cnt[a]||(a<b?-1:1)).map(b=>({v:b,label:b+" ("+cnt[b]+")"}));
}
function stateOptions(){
  const cnt={};
  filtered.forEach(r=>{ if(r._states) r._states.forEach(s=>{ if(s!=="State not found") cnt[s]=(cnt[s]||0)+1; }); });
  return Object.keys(cnt).sort((a,b)=>cnt[b]-cnt[a]||(a<b?-1:1)).map(s=>({v:s,label:s+" ("+cnt[s]+")"}));
}
fillSel(document.getElementById("sel-mech"),mechanisms.map(m=>({v:m,label:m})),"all mechanisms");
fillSel(document.getElementById("sel-yfrom"),allYears.map(y=>({v:String(y),label:String(y)})),"—");
fillSel(document.getElementById("sel-yto"),allYears.map(y=>({v:String(y),label:String(y)})),"—");
fillSel(document.getElementById("sel-sdg"),sdgGoals.map(g=>({v:String(g),label:"SDG "+g+(sdgNames[String(g)]?" · "+sdgNames[String(g)]:"")+" ("+sdgCounts[g]+")"})),"all goals");

function rebuildMechDependent(){
  const bo = bodyOptions();
  fillSel(document.getElementById("sel-body"),bo,"all bodies");
  if(f.body && !bo.some(o=>o.v===f.body)) f.body="";
  document.getElementById("sel-body").value=f.body;
  const tc={};
  (f.mechanism?recs.filter(r=>r.mechanism===f.mechanism):recs).forEach(r=>tc[r.type]=(tc[r.type]||0)+1);
  fillSel(document.getElementById("sel-type"),Object.keys(tc).sort().map(t=>({v:t,label:t+" ("+tc[t]+")"})),"all types");
  if(f.type && !(f.type in tc)) f.type="";
  document.getElementById("sel-type").value=f.type;
}
rebuildMechDependent();

function fixYearRange(){
  if(f.yearFrom!=="" && f.yearTo!=="" && +f.yearFrom > +f.yearTo){
    const t=f.yearFrom; f.yearFrom=f.yearTo; f.yearTo=t;
    document.getElementById("sel-yfrom").value=f.yearFrom;
    document.getElementById("sel-yto").value=f.yearTo;
  }
}

/* ---------- filter events ---------- */
let kwTimer=null;
function setKeyword(v){
  f.keyword=v.trim();
  f.keywordWords=f.keyword?f.keyword.toLowerCase().split(/\s+/):[];
  document.getElementById("kw-input").value=v;
  document.getElementById("kw-input-2").value=v;
}
document.getElementById("kw-input").addEventListener("input",e=>{
  const v=e.target.value; clearTimeout(kwTimer);
  kwTimer=setTimeout(()=>{setKeyword(v);refresh();},300);
});
document.getElementById("kw-input-2").addEventListener("input",e=>{
  const v=e.target.value; clearTimeout(kwTimer);
  kwTimer=setTimeout(()=>{setKeyword(v);refresh();},300);
});
document.getElementById("sel-mech").addEventListener("change",e=>{f.mechanism=e.target.value;rebuildMechDependent();refresh();});
document.getElementById("sel-body").addEventListener("change",e=>{f.body=e.target.value;refresh();});
document.getElementById("sel-type").addEventListener("change",e=>{f.type=e.target.value;refresh();});
document.getElementById("sel-state").addEventListener("change",e=>{f.state=e.target.value;refresh();});
document.getElementById("sel-yfrom").addEventListener("change",e=>{f.yearFrom=e.target.value;fixYearRange();refresh();});
document.getElementById("sel-yto").addEventListener("change",e=>{f.yearTo=e.target.value;fixYearRange();refresh();});
document.getElementById("sel-sdg").addEventListener("change",e=>{f.sdg=e.target.value;refresh();});
document.getElementById("clear-all").addEventListener("click",()=>{
  f.keywordWords=[];f.keyword="";f.mechanism="";f.body="";f.type="";f.state="";f.yearFrom="";f.yearTo="";f.sdg="";f.themes.clear();
  document.getElementById("kw-input").value="";document.getElementById("kw-input-2").value="";
  ["sel-mech","sel-body","sel-type","sel-state","sel-yfrom","sel-yto","sel-sdg"].forEach(id=>document.getElementById(id).value="");
  rebuildMechDependent();refresh();
});

/* ---------- chips ---------- */
function chipLabel(kind,val){
  if(kind==="keyword")return "keyword: "+val;
  if(kind==="mechanism")return "mechanism: "+val;
  if(kind==="body")return "body: "+val;
  if(kind==="type")return "type: "+val;
  if(kind==="state")return "State: "+val;
  if(kind==="yearFrom")return "from "+val;
  if(kind==="yearTo")return "to "+val;
  if(kind==="sdg")return "SDG "+val+(sdgNames[val]?" · "+sdgNames[val]:"");
  if(kind==="theme")return "theme: "+val;
  return val;
}
function removeFilter(kind){
  if(kind==="keyword"){setKeyword("");}
  else if(kind==="theme"){f.themes.delete(f.themes.values().next().value);}
  else f[kind]="";
  ["sel-mech","sel-body","sel-type","sel-state","sel-yfrom","sel-yto","sel-sdg"].forEach(id=>document.getElementById(id).value="");
  rebuildMechDependent();refresh();
}
function renderChips(){
  const box=document.getElementById("rail-chips");
  const chips=[];
  if(f.keyword)chips.push(["keyword",f.keyword]);
  if(f.mechanism)chips.push(["mechanism",f.mechanism]);
  if(f.body)chips.push(["body",f.body]);
  if(f.type)chips.push(["type",f.type]);
  if(f.state)chips.push(["state",f.state]);
  if(f.yearFrom!=="")chips.push(["yearFrom",f.yearFrom]);
  if(f.yearTo!=="")chips.push(["yearTo",f.yearTo]);
  if(f.sdg!=="")chips.push(["sdg",f.sdg]);
  f.themes.forEach(t=>chips.push(["theme",t]));
  if(!chips.length){box.innerHTML="";return;}
  box.innerHTML=chips.map(([k,v],i)=>'<span class="chip">'+esc(chipLabel(k,v))+' <button data-k="'+escAttr(k)+'" data-v="'+escAttr(v)+'" aria-label="Remove filter '+escAttr(chipLabel(k,v))+'">×</button></span>').join("");
  box.querySelectorAll("button").forEach(b=>b.addEventListener("click",()=>{
    const k=b.getAttribute("data-k"), v=b.getAttribute("data-v");
    if(k==="theme"){f.themes.delete(v);}
    else if(k==="keyword"){setKeyword("");}
    else f[k]="";
    refresh();
  }));
}

/* ---------- rail ---------- */
function renderRail(){
  document.getElementById("rail-count").innerHTML=fmt(filtered.length)+' <small>matching records</small>';
  document.getElementById("rail-of").textContent="of "+fmt(N)+" in the file";
  const pct=N?filtered.length/N*100:0;
  document.getElementById("rail-bar").style.width=pct+"%";
  document.getElementById("rail-share").textContent=pct.toFixed(1)+"% of the file";
  renderChips();
}

/* ---------- charts ---------- */
let chart1=null, chart2=null;
const valueLabelPlugin={id:"val",afterDatasetsDraw(c){
  if(!c.$showValues)return;
  const meta=c.getDatasetMeta(0).data;
  c.data.datasets[0].data.forEach((v,i)=>{
    const bar=meta[i]; if(!bar)return;
    const ctx=c.ctx; ctx.save();
    ctx.fillStyle="#1d1b18"; ctx.font="13px Georgia, serif"; ctx.textBaseline="middle";
    ctx.fillText(fmt(v), bar.x+6, bar.y); ctx.restore();
  });
}};
const mechColor=m=>m==="Universal Periodic Review"?"#c2410c":m==="Treaty bodies"?"#0f766e":"#7c3aed";

function topThemes(list){
  const cnt={}, yrs={};
  list.forEach(r=>(r.themes||[]).forEach(t=>{
    cnt[t]=(cnt[t]||0)+1;
    if(!yrs[t])yrs[t]=[r.year,r.year];
    else{yrs[t][0]=Math.min(yrs[t][0],r.year);yrs[t][1]=Math.max(yrs[t][1],r.year);}
  }));
  return Object.keys(cnt)
    .sort((a,b)=>cnt[b]-cnt[a]||(a<b?-1:1))
    .slice(0,10)
    .map(t=>({theme:t,count:cnt[t],yrs:yrs[t]}));
}

function renderOverview(){
  const n=filtered.length;
  /* tiles */
  const typeCnt={};
  recs.forEach(r=>typeCnt[r.type]=(typeCnt[r.type]||0)+1);
  const fdocs=new Set(filtered.map(r=>r.symbol)).size;
  let tilesHtml="";
  tilesHtml+='<div class="tile"><div class="lbl">All records</div><div class="num">'+fmt(n)+'</div>'
    +'<div class="sub">'+Object.keys(typeCnt).sort().map(t=>fmt(typeCnt[t])+" "+esc(t)).join(" · ")+'</div>'
    +'<div class="how">How: records in the current filter, counted per type as spelled in the data.</div></div>';
  tilesHtml+='<div class="tile"><div class="lbl">Documents</div><div class="num">'+fmt(fdocs)+'</div>'
    +'<div class="sub">distinct document symbols</div>'
    +'<div class="how">How: count of distinct symbol values.</div></div>';
  tilesHtml+='<div class="tile"><div class="lbl">Years</div><div class="num">'+(n?Math.min(...filtered.map(r=>r.year))+"–"+Math.max(...filtered.map(r=>r.year)):"—")+'</div>'
    +'<div class="sub">first–last year of the filtered records; gaps are visible in FIG.02</div>'
    +'<div class="how">How: min and max of year.</div></div>';
  mechanisms.forEach(m=>{
    const sub=filtered.filter(r=>r.mechanism===m);
    const d=new Set(sub.map(r=>r.symbol)).size;
    const latest=sub.length?Math.max(...sub.map(r=>r.year)):"—";
    tilesHtml+='<div class="tile"><div class="lbl"><span class="dot" style="background:'+mechColor(m)+'"></span>'+esc(m)+'</div>'
      +'<div class="num">'+fmt(sub.length)+'</div>'
      +'<div class="sub">'+fmt(d)+' documents · latest '+latest+' · '+(n?(sub.length/n*100).toFixed(1):0)+'% of filtered</div>'
      +(m==="Universal Periodic Review"&&sub.length?'<button class="linkish" id="see-states">see the States</button><div class="statelist" id="upr-states" hidden></div>':'')
      +'<div class="how">How: records with mechanism = '+esc(m)+' in the current filter.</div></div>';
  });
  document.getElementById("ov-tiles").innerHTML=tilesHtml;
  const seeBtn=document.getElementById("see-states");
  if(seeBtn)seeBtn.addEventListener("click",()=>{
    const box=document.getElementById("upr-states");
    if(!box.hidden){box.hidden=true;return;}
    const cnt={};
    filtered.forEach(r=>{if(r.mechanism==="Universal Periodic Review"&&r._states)r._states.forEach(s=>{if(s!=="State not found")cnt[s]=(cnt[s]||0)+1;});});
    const top=Object.keys(cnt).sort((a,b)=>cnt[b]-cnt[a]||(a<b?-1:1)).slice(0,10);
    box.innerHTML='<div class="lbl">Ten States that made most recommendations to '+esc(U.country)+' (current filter)</div>'
      +'<ol>'+top.map(s=>'<li>'+esc(s)+' — '+fmt(cnt[s])+'</li>').join("")+'</ol>'
      +'<div class="how" style="font-size:11px;color:#8a8072;font-family:var(--mono);margin-top:6px">A recommendation with several States counts once for each. A count of recommendations, not of influence.</div>';
    box.hidden=false;
  });

  /* FIG.01 */
  const top=topThemes(filtered);
  document.getElementById("fig1-title").textContent="Ten most frequent themes among "+fmt(n)+" filtered records";
  document.getElementById("fig1-sub").textContent="A record can carry several themes, so the bars add up to more than "+fmt(n)+". Click a bar to filter by that theme.";
  document.getElementById("fig1-src").textContent="Source: "+U.source+" · counted over the current filter ("+fmt(n)+" records) · percentages are of records, not of labels.";
  if(chart1){chart1.destroy();chart1=null;}
  const box1=document.getElementById("fig1-box");
  if(!n||!top.length){
    box1.innerHTML='<div class="nomatch">No records match</div>';
    document.getElementById("fig1-tablewrap").innerHTML="";
  }else{
    box1.innerHTML='<canvas id="fig1" aria-label="Ten most frequent themes, horizontal bar chart"></canvas>';
    chart1=new Chart(document.getElementById("fig1"),{
      type:"bar",
      data:{labels:top.map(t=>t.theme),datasets:[{data:top.map(t=>t.count),backgroundColor:"rgba(155,35,53,0.8)",borderColor:"#9b2335",borderWidth:0}]},
      options:{indexAxis:"y",responsive:true,maintainAspectRatio:false,
        onClick:(e,els)=>{if(els.length){const t=top[els[0].index].theme;f.themes.has(t)?f.themes.delete(t):f.themes.add(t);refresh();}},
        plugins:{legend:{display:false},tooltip:{callbacks:{label:c=>" "+fmt(c.parsed.x)+" records"}}},
        scales:{x:{grid:{color:"#e7e0d2"},ticks:{precision:0}},y:{grid:{display:false},ticks:{font:{size:12}}}}},
      plugins:[valueLabelPlugin]
    });
    chart1.$showValues=true;
    document.getElementById("fig1-tablewrap").innerHTML=
      '<table><caption>FIG.01 · same ten themes as the chart · source: '+esc(U.source)+'</caption>'
      +'<thead><tr><th scope="col">Theme</th><th scope="col" class="num">Records</th><th scope="col" class="num">% of filtered</th><th scope="col">Years (first–last)</th></tr></thead><tbody>'
      +top.map(t=>'<tr><td>'+esc(t.theme)+'</td><td class="num">'+fmt(t.count)+'</td><td class="num">'+(n?(t.count/n*100).toFixed(1):0)+'%</td><td>'+t.yrs[0]+'–'+t.yrs[1]+'</td></tr>').join("")
      +'</tbody></table>';
  }

  /* FIG.02 */
  document.getElementById("fig2-sub").textContent="Every year from the first to the last of the filtered records appears; empty years are visible gaps.";
  document.getElementById("fig2-src").textContent="Source: "+U.source+" · records per year per mechanism in the current filter; a record with no mechanism value would not appear.";
  if(chart2){chart2.destroy();chart2=null;}
  const box2=document.getElementById("fig2-box");
  if(!n){
    box2.innerHTML='<div class="nomatch">No records match</div>';
  }else{
    const yMin=Math.min(...filtered.map(r=>r.year)), yMax=Math.max(...filtered.map(r=>r.year));
    const years=[]; for(let y=yMin;y<=yMax;y++)years.push(y);
    const mechPresent=mechanisms.filter(m=>filtered.some(r=>r.mechanism===m));
    const datasets=mechPresent.map(m=>({
      label:m,backgroundColor:mechColor(m),
      data:years.map(y=>filtered.filter(r=>r.year===y&&r.mechanism===m).length)
    }));
    box2.innerHTML='<canvas id="fig2" aria-label="Records per year by mechanism, stacked bar chart"></canvas>';
    chart2=new Chart(document.getElementById("fig2"),{
      type:"bar",
      data:{labels:years.map(String),datasets},
      options:{responsive:true,maintainAspectRatio:false,
        plugins:{legend:{position:"bottom",labels:{boxWidth:10,font:{size:12}}},
          tooltip:{callbacks:{label:c=>" "+c.dataset.label+": "+fmt(c.parsed.y)}}},
        scales:{x:{stacked:true,grid:{display:false}},y:{stacked:true,grid:{color:"#e7e0d2"},ticks:{precision:0}}}}
    });
  }
}

/* ---------- records table ---------- */
function firstLine(t){
  if(t.length<=120)return t;
  const cut=t.slice(0,120), sp=cut.lastIndexOf(" ");
  return (sp>60?cut.slice(0,sp):cut)+"…";
}
function hi(text){
  let out=esc(text);
  f.keywordWords.forEach(w=>{
    if(!w)return;
    const re=new RegExp("("+w.replace(/[.*+?^${}()|[\]\\]/g,"\\$&")+")","gi");
    out=out.replace(re,"<mark>$1</mark>");
  });
  return out;
}
function stateCell(r){
  if(r.mechanism!=="Universal Periodic Review")return '<span class="dash">—</span>';
  if(!r._states)return '<span class="dash">—</span>';
  if(r._states[0]==="State not found")return '<span class="dash">State not found</span>';
  return esc(r._states.join(", "));
}
function renderTable(){
  const wrap=document.getElementById("rec-tablewrap");
  const n=filtered.length;
  const rows=sortedRecs.filter(r=>matches(r));
  const ordered=dateDesc?rows:rows.slice().reverse();
  const slice=ordered.slice(0,shown);
  const btn=document.getElementById("more-btn");
  btn.hidden=shown>=ordered.length;
  let html='<table><caption>Records · '+fmt(Math.min(shown,ordered.length))+' shown of '+fmt(ordered.length)+' matching · of '+fmt(N)+' in the file · '+(dateDesc?"newest first":"oldest first")+' · sorted by date, body, paragraph number · click a row to expand</caption>'
    +'<thead><tr><th scope="col"><button class="linkish mono" id="date-th" style="font-size:10.5px;letter-spacing:.1em;text-transform:uppercase">Date <span class="arrow">'+(dateDesc?"↓":"↑")+'</span></button></th><th scope="col">Body</th><th scope="col">Symbol</th><th scope="col" class="num">Para.</th><th scope="col">First line</th><th scope="col">Recommending State</th></tr></thead><tbody>';
  slice.forEach(r=>{
    const open=expandedIds.has(r.id);
    html+='<tr class="rec" tabindex="0" data-id="'+escAttr(r.id)+'" aria-expanded="'+(open?"true":"false")+'">'
      +'<td style="white-space:nowrap">'+esc(r.date)+'</td><td>'+esc(r.body)+'</td>'
      +'<td style="white-space:nowrap"><a href="'+escAttr(r.doc_url)+'" target="_blank" rel="noopener">'+esc(r.symbol)+'</a></td>'
      +'<td class="num">'+(r._para?esc(r._para):'<span class="dash">—</span>')+'</td>'
      +'<td>'+hi(firstLine(r.text||""))+'</td>'
      +'<td>'+stateCell(r)+'</td></tr>';
    if(open){
      const labels=[];
      if(r.section)labels.push('<div class="labelrow"><div class="lbl">Section</div><div class="taglist"><span class="tag">'+esc(r.section)+'</span></div></div>');
      labels.push('<div class="labelrow"><div class="lbl">Themes</div><div class="taglist">'+((r.themes&&r.themes.length)?r.themes.map(t=>'<span class="tag">'+esc(t)+'</span>').join(""):'<span class="dash">not labelled</span>')+'</div></div>');
      labels.push('<div class="labelrow"><div class="lbl">SDGs</div><div class="taglist">'+((r.sdgs&&r.sdgs.length)?r.sdgs.map(g=>'<span class="tag">SDG '+esc(g)+(sdgNames[String(g)]?' · '+esc(sdgNames[String(g)]):'')+'</span>').join(""):'<span class="dash">not labelled</span>')+'</div></div>');
      if(r.sdg_targets&&r.sdg_targets.length)labels.push('<div class="labelrow"><div class="lbl">SDG targets</div><div class="taglist">'+r.sdg_targets.map(t=>'<span class="tag">'+esc(t)+'</span>').join("")+'</div></div>');
      labels.push('<div class="labelrow"><div class="lbl">Affected persons</div><div class="taglist">'+((r.affected_persons&&r.affected_persons.length)?r.affected_persons.map(t=>'<span class="tag">'+esc(t)+'</span>').join(""):'<span class="dash">not labelled</span>')+'</div></div>');
      const cite=r._para?r.symbol+", para. "+r._para:r.symbol;
      html+='<tr class="expand"><td colspan="6">'
        +(r._para?'<div class="para-big">'+esc(r._para)+'</div>':'')
        +'<div class="fulltext">'+esc(r.text||"")+'</div>'
        +labels.join("")
        +'<div class="actions">'
        +'<button class="btn primary copy-cite" data-cite="'+escAttr(cite)+'">'+(r._para?'Copy citation':'Copy citation (no paragraph number in this extract)')+'</button>'
        +'<button class="btn open-doc" data-url="'+escAttr(r.doc_url)+'">Open the UN document</button>'
        +'<span class="copied" hidden>Copied</span></div>'
        +'</td></tr>';
    }
  });
  html+='</tbody></table>';
  wrap.innerHTML=html;
  const dt=document.getElementById("date-th");
  if(dt)dt.addEventListener("click",()=>{dateDesc=!dateDesc;renderTable();});
  wrap.querySelectorAll("tr.rec").forEach(tr=>{
    const id=tr.getAttribute("data-id");
    const toggle=()=>{expandedIds.has(id)?expandedIds.delete(id):expandedIds.add(id);renderTable();};
    tr.addEventListener("click",e=>{if(e.target.closest("a"))return;toggle();});
    tr.addEventListener("keydown",e=>{if(e.key==="Enter"||e.key===" "){e.preventDefault();toggle();}});
  });
  wrap.querySelectorAll(".copy-cite").forEach(b=>{
    b.addEventListener("click",e=>{
      e.stopPropagation();
      copyText(b.getAttribute("data-cite"),b.parentElement.querySelector(".copied"));
    });
  });
  wrap.querySelectorAll(".open-doc").forEach(b=>{
    b.addEventListener("click",e=>{e.stopPropagation();window.open(b.getAttribute("data-url"),"_blank","noopener");});
  });
}
document.getElementById("more-btn").addEventListener("click",()=>{shown+=50;renderTable();});

/* ---------- clipboard ---------- */
function copyText(text,msgEl){
  const done=()=>{if(msgEl){msgEl.hidden=false;setTimeout(()=>msgEl.hidden=true,2000);}};
  if(navigator.clipboard&&navigator.clipboard.writeText){
    navigator.clipboard.writeText(text).then(done).catch(()=>fallbackCopy(text,done));
  }else fallbackCopy(text,done);
}
function fallbackCopy(text,done){
  const ta=document.createElement("textarea");
  ta.value=text;ta.style.position="fixed";ta.style.opacity="0";
  document.body.appendChild(ta);ta.select();
  try{document.execCommand("copy");}catch(e){}
  document.body.removeChild(ta);done();
}

/* ---------- checks ---------- */
function computeChecks(){
  const lines=[];
  const add=(ok,cls,what,vals)=>lines.push({cls,what,vals});
  /* record count */
  const declared=Number(U.count);
  if(String(N)===String(U.count)||N===declared)add(true,"pass","Record count: records.length equals the file's declared count",fmt(N)+" = "+fmt(declared));
  else add(false,"fail","Record count: records.length vs the file's declared count",fmt(N)+" ≠ "+fmt(declared));
  /* partitions */
  const cntBy={mechanism:{},body:{},year:{},type:{}};
  recs.forEach(r=>{
    cntBy.mechanism[r.mechanism]=(cntBy.mechanism[r.mechanism]||0)+1;
    cntBy.body[r.body]=(cntBy.body[r.body]||0)+1;
    cntBy.year[r.year]=(cntBy.year[r.year]||0)+1;
    cntBy.type[r.type]=(cntBy.type[r.type]||0)+1;
  });
  [["mechanism"],["body"],["year"],["type"]].forEach(([k])=>{
    const s=Object.values(cntBy[k]).reduce((a,b)=>a+b,0);
    if(s===N)add(true,"pass","Partition by "+k+": counts sum to the record count (whole file)",fmt(s)+" = "+fmt(N));
    else add(false,"fail","Partition by "+k+": counts do not sum to the record count (whole file)",fmt(s)+" ≠ "+fmt(N));
  });
  /* chart vs table (current filter) */
  const topNow=topThemes(filtered);
  let chartOk=true, chartVals="";
  if(topNow.length){
    const recount={};
    filtered.forEach(r=>(r.themes||[]).forEach(t=>recount[t]=(recount[t]||0)+1));
    topNow.forEach(t=>{if(recount[t.theme]!==t.count)chartOk=false;});
    if(topNow[0].count>filtered.length)chartOk=false;
    chartVals="largest bar "+fmt(topNow[0].count)+" ≤ "+fmt(filtered.length)+" filtered records; all ten bar values equal a recount";
  }else chartVals="no themes in the current filter";
  add(chartOk,chartOk?"pass":"fail","Chart against table: each FIG.01 bar equals a second, independent count over the current filter",chartVals);
  /* links */
  const badLinks=[];
  recs.forEach(r=>{
    let ok=false;
    try{
      const dec=decodeURIComponent(r.doc_url||"");
      ok=(r.doc_url||"").startsWith("https://docs.un.org/") && dec.toLowerCase().endsWith((r.symbol||"").toLowerCase());
    }catch(e){ok=false;}
    if(!ok)badLinks.push(r.symbol);
  });
  if(!badLinks.length)add(true,"pass","Links: every doc_url starts with https://docs.un.org/ and ends with its symbol (whole file)",fmt(N)+" of "+fmt(N)+" records");
  else add(false,"fail","Links: records whose doc_url does not match the rule (whole file)",fmt(badLinks.length)+" failing: "+badLinks.slice(0,8).join(", ")+(badLinks.length>8?" …":""));
  /* paragraph numbers */
  const uprRecs=recs.filter(r=>r.mechanism==="Universal Periodic Review");
  lines.push({cls:"",special:"para"});
  const paraByMech={};
  recs.forEach(r=>{
    if(!paraByMech[r.mechanism])paraByMech[r.mechanism]={found:0,total:0};
    paraByMech[r.mechanism].total++;
    if(r._para)paraByMech[r.mechanism].found++;
  });
  Object.keys(paraByMech).sort().forEach(m=>{
    const p=paraByMech[m], pct=(p.found/p.total*100).toFixed(1);
    if(m==="Universal Periodic Review"&&p.found<p.total)
      add(false,"warn","Paragraph numbers: UPR share with a number found (expected 100%)",pct+"% ("+fmt(p.found)+" of "+fmt(p.total)+")");
    else
      add(true,"pass","Paragraph numbers: share with a number found, "+m+" (whole file)",pct+"% ("+fmt(p.found)+" of "+fmt(p.total)+")"+(m==="Universal Periodic Review"?"":" — lettered items carry none"));
  });
  /* states */
  const uprWithState=uprRecs.filter(r=>r._states&&r._states[0]!=="State not found");
  const uprMissing=uprRecs.filter(r=>!r._states||r._states[0]==="State not found");
  if(!uprMissing.length)
    add(true,"pass","States found: UPR records with at least one State extracted (whole file)",fmt(uprWithState.length)+" of "+fmt(uprRecs.length));
  else
    add(false,"fail","States found: UPR records without a State — see what the parentheses held (whole file)",fmt(uprWithState.length)+" of "+fmt(uprRecs.length)+"; without: "+uprMissing.slice(0,8).map(r=>r.symbol).join(", ")+(uprMissing.length>8?" …":""));
  /* duplicates and gaps */
  const ids=new Set(recs.map(r=>r.id));
  if(ids.size===N)add(true,"pass","Duplicates: distinct id equals the record count (whole file)",fmt(ids.size)+" = "+fmt(N));
  else add(false,"fail","Duplicates: distinct id vs record count (whole file)",fmt(ids.size)+" ≠ "+fmt(N));
  const textCnt={};
  recs.forEach(r=>{const t=r.text||"";textCnt[t]=(textCnt[t]||0)+1;});
  const dupTexts=Object.values(textCnt).filter(c=>c>1).length;
  add(dupTexts===0,dupTexts===0?"pass":"warn","Duplicate texts: texts appearing in more than one record (whole file)",fmt(dupTexts)+" duplicated text values");
  const noTheme=recs.filter(r=>!(r.themes&&r.themes.length)).length;
  const noSdg=recs.filter(r=>!(r.sdgs&&r.sdgs.length)).length;
  const noAff=recs.filter(r=>!(r.affected_persons&&r.affected_persons.length)).length;
  add(true,"pass","Gaps: records not labelled, by field (whole file, shown as missing, never guessed)",
    "no themes: "+fmt(noTheme)+" · no SDGs: "+fmt(noSdg)+" · no affected persons: "+fmt(noAff));
  return lines;
}
function renderChecks(){
  const lines=computeChecks();
  document.getElementById("checks").innerHTML=lines.map(l=>{
    if(l.special==="para")return '<div class="checkline"><span class="mark">·</span><span class="what" style="font-family:var(--mono);font-size:11px;letter-spacing:.1em;text-transform:uppercase;color:#6b6255">Paragraph numbers by mechanism</span></div>';
    const mark=l.cls==="pass"?"PASS":l.cls==="warn"?"WARNING":"CHECK FAILED";
    return '<div class="checkline"><span class="mark '+l.cls+'">'+mark+'</span><span class="what">'+esc(l.what)+'</span><span class="vals">'+esc(l.vals)+'</span></div>';
  }).join("");
}

/* ---------- random sample ---------- */
function mulberry32(a){return function(){a|=0;a=a+0x6D2B79F5|0;let t=Math.imul(a^a>>>15,1|a);t=t+Math.imul(t^t>>>7,61|t)^t;return((t^t>>>14)>>>0)/4294967296;};}
let sampleSeed=1, sample=null, verdicts={};
function drawSample(seed){
  sampleSeed=seed;
  const rng=mulberry32(seed);
  const pool=filtered.slice();
  const picks=[];
  const k=Math.min(10,pool.length);
  for(let i=0;i<k;i++)picks.push(pool[Math.floor(rng()*pool.length)]);
  sample=picks; verdicts={};
  renderSample();
}
function renderSample(){
  const box=document.getElementById("sample-cards");
  document.getElementById("sample-tally").innerHTML=
    'Themes: <span class="mono">'+Object.values(verdicts).filter(v=>v==="fit").length+' fit</span>, '
    +'<span class="mono">'+Object.values(verdicts).filter(v=>v==="no").length+' don\'t</span>, '
    +'<span class="mono">'+Object.values(verdicts).filter(v=>v==="unsure").length+' unsure</span>'
    +' of '+Object.keys(verdicts).length+' judged'
    +' <span class="mono">(seed '+sampleSeed+')</span> — the tally is your judgement, not a change to any UN label.';
  if(!sample){box.innerHTML="";return;}
  box.innerHTML="";
  sample.forEach((r,idx)=>{
    const card=document.createElement("div");
    card.className="card"+(verdicts[r.id]==="fit"?" vfit":verdicts[r.id]==="no"?" vno":verdicts[r.id]==="unsure"?" vunsure":"");
    const head=document.createElement("button");
    head.className="cardhead";head.setAttribute("aria-expanded","false");
    head.innerHTML='<span class="csym"><a href="'+escAttr(r.doc_url)+'" target="_blank" rel="noopener" onclick="event.stopPropagation()">'+esc(r.symbol)+'</a></span>'
      +(r._para?'<span class="cpara">'+esc(r._para)+'</span>':'<span class="cpara">—</span>')
      +'<span class="csnip">'+esc(firstLine(r.text||""))+'</span>';
    const body=document.createElement("div");
    body.className="cardbody";body.hidden=true;
    body.innerHTML='<div class="fulltext">'+esc(r.text||"")+'</div>'
      +'<div class="labelrow"><div class="lbl">Themes to judge</div><div class="taglist">'
      +((r.themes&&r.themes.length)?r.themes.map(t=>'<span class="tag">'+esc(t)+'</span>').join(""):'<span class="dash">not labelled</span>')+'</div></div>'
      +'<div class="vbtns">'
      +'<button class="btn vbtn'+(verdicts[r.id]==="fit"?" on":"")+'" data-v="fit">Fits</button>'
      +'<button class="btn vbtn'+(verdicts[r.id]==="no"?" on":"")+'" data-v="no">Doesn\'t fit</button>'
      +'<button class="btn vbtn'+(verdicts[r.id]==="unsure"?" on":"")+'" data-v="unsure">Unsure</button>'
      +'</div>';
    head.addEventListener("click",()=>{
      const open=body.hidden;
      box.querySelectorAll(".cardbody").forEach(b=>b.hidden=true);
      box.querySelectorAll(".cardhead").forEach(h=>h.setAttribute("aria-expanded","false"));
      if(open){body.hidden=false;head.setAttribute("aria-expanded","true");}
    });
    body.querySelectorAll(".vbtn").forEach(b=>b.addEventListener("click",()=>{
      verdicts[r.id]=b.getAttribute("data-v");
      renderSample();
    }));
    card.appendChild(head);card.appendChild(body);
    box.appendChild(card);
  });
}
document.getElementById("draw-btn").addEventListener("click",()=>{
  document.getElementById("draw-again-wrap").hidden=false;
  drawSample(1);
});
document.getElementById("draw-again").addEventListener("click",()=>{drawSample(Math.floor(Math.random()*1e6)+1);});
document.getElementById("draw-seed").addEventListener("click",()=>{
  const v=parseInt(document.getElementById("seed-input").value,10);
  drawSample(isNaN(v)?1:v);
});

/* ---------- method & export ---------- */
function renderMethod(){
  document.getElementById("method-text").innerHTML=
    '<p>The headline total is the number of records in the current filter, and the breakdown under it counts records per <code>type</code>, using the values exactly as spelled in the data. Documents are the count of distinct <code>symbol</code> values; years are the minimum and maximum <code>year</code>.</p>'
    +'<p>Filters combine with AND. Mechanism, body and type match the field exactly; the year range is inclusive; an SDG filter keeps records whose <code>sdgs</code> list contains the chosen goal number; a State filter keeps UPR records naming that State. The keyword search is literal: every word must occur as a substring of the text or the symbol, so "torture" does not find "ill-treatment".</p>'
    +'<p>Theme counts count each value in a record\'s <code>themes</code> list once per record, so they sum to more than the record count; percentages are of records. The timeline counts records per year per mechanism, with zero for missing years.</p>'
    +'<p>The paragraph number is the first match of a number at the very start of the text; when there is none, the record shows a dash and the citation is the symbol alone. Recommending States are read only from UPR texts, from the parenthesised groups at the end; a group with a comma or over 60 characters is not accepted as a State.</p>'
    +'<p>Nothing is estimated and no model is called. Every count is a loop over the records in JavaScript, and the clipboard write on "Copy" is the only thing that leaves the page.</p>';
  document.getElementById("src-note").innerHTML=
    'Data: <a href="'+esc(U.source_url)+'" target="_blank" rel="noopener">'+esc(U.source)+'</a> · '+esc(U.title)+' · built '+esc(U.built)+' · country: '+esc(U.country)+' · dates are document dates, not dates a recommendation was made or accepted.';
}
function filterSummaryLine(){
  const parts=[];
  if(f.keyword)parts.push('keyword "'+f.keyword+'"');
  if(f.mechanism)parts.push("mechanism "+f.mechanism);
  if(f.body)parts.push("body "+f.body);
  if(f.type)parts.push("type "+f.type);
  if(f.state)parts.push("State "+f.state);
  if(f.yearFrom||f.yearTo)parts.push("years "+(f.yearFrom||y0)+"–"+(f.yearTo||y1));
  if(f.sdg)parts.push("SDG "+f.sdg);
  if(f.themes.size)parts.push("themes: "+[...f.themes].join("; "));
  return parts.length?parts.join(" · "):"none";
}
function csvEsc(v){
  const s=String(v==null?"":v);
  return /[",\n\r]/.test(s)?'"'+s.replace(/"/g,'""')+'"':s;
}
document.getElementById("csv-btn").addEventListener("click",()=>{
  const rows=sortedRecs.filter(matches);
  const lines=[];
  lines.push("# "+U.country+" — UN human rights recommendations and observations");
  lines.push("# Source: "+U.source+" ("+U.source_url+")");
  lines.push("# Built: "+U.built+"; dates are document dates (dated by document)");
  lines.push("# Filters applied: "+filterSummaryLine());
  lines.push("# Rows: "+rows.length+" of "+N+" records in the file");
  lines.push("date,body,mechanism,type,symbol,paragraph,recommending_states,text,themes,sdgs,sdg_targets,affected_persons,section,doc_url");
  rows.forEach(r=>{
    lines.push([r.date,r.body,r.mechanism,r.type,r.symbol,r._para||"",
      (r._states&&r._states[0]!=="State not found")?r._states.join("; "):(r.mechanism==="Universal Periodic Review"?"State not found":""),
      r.text,(r.themes||[]).join("; "),(r.sdgs||[]).join("; "),(r.sdg_targets||[]).join("; "),(r.affected_persons||[]).join("; "),r.section||"",r.doc_url
    ].map(csvEsc).join(","));
  });
  const blob=new Blob(["\uFEFF"+lines.join("\r\n")],{type:"text/csv;charset=utf-8"});
  const url=URL.createObjectURL(blob);
  const a=document.createElement("a");
  a.href=url;a.download=(U.country||"uhri")+"_recommendations_filtered.csv";
  document.body.appendChild(a);a.click();document.body.removeChild(a);
  setTimeout(()=>URL.revokeObjectURL(url),5000);
  const msg=document.getElementById("export-msg");
  msg.textContent=fmt(rows.length)+" rows downloaded";msg.hidden=false;
  setTimeout(()=>msg.hidden=true,3000);
});
document.getElementById("summary-btn").addEventListener("click",()=>{
  const n=filtered.length;
  const top=topThemes(filtered);
  const typeCnt={};
  filtered.forEach(r=>typeCnt[r.type]=(typeCnt[r.type]||0)+1);
  const txt="UN human rights recommendations and observations: "+U.country+". "
    +fmt(n)+" records ("+Object.keys(typeCnt).sort().map(t=>fmt(typeCnt[t])+" "+t).join(", ")+") "
    +"from "+fmt(new Set(filtered.map(r=>r.symbol)).size)+" documents, "
    +(n?Math.min(...filtered.map(r=>r.year))+"–"+Math.max(...filtered.map(r=>r.year)):"no years")
    +", filters: "+filterSummaryLine()+". "
    +"Most frequent themes: "+(top.map(t=>t.theme+" ("+t.count+")").join("; ")||"none")
    +". Source: "+U.source+", built "+U.built+"; dated by document; counts computed in the dashboard, nothing estimated.";
  copyText(txt,document.getElementById("export-msg"));
  const msg=document.getElementById("export-msg");
  msg.textContent="Summary copied";msg.hidden=false;
  setTimeout(()=>msg.hidden=true,3000);
});

/* ---------- refresh ---------- */
function refresh(){
  filtered=recs.filter(matches);
  expandedIds.clear();
  shown=50;
  renderRail();
  /* state select lives in heading 02; rebuild */
  const so=stateOptions();
  const hasStates=so.length>0||f.mechanism==="Universal Periodic Review";
  document.getElementById("state-filter-wrap").hidden=!hasStates;
  fillSel(document.getElementById("sel-state"),so,"all States");
  if(f.state&&!so.some(o=>o.v===f.state))f.state="";
  document.getElementById("sel-state").value=f.state;
  if(curTab===0)renderOverview();
  if(curTab===1)renderTable();
  if(curTab===2)renderChecks();
  if(sample)renderSample(); /* tally stays with the drawn set; note filter may have changed */
}

/* ---------- init ---------- */
renderRail();
renderOverview();
renderChecks();
})();
</script>
</body>
</html>
```