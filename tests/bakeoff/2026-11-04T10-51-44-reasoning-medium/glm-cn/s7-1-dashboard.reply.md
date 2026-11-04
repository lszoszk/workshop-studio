Here's the dashboard, built exactly to the plan: four tabs, shared filters in a left rail, self-checks on tab 03, and CSV export on tab 04. All numbers are computed in the browser from `WORKSHOP_DATA.uhri` — nothing is hard-coded.

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>UN human rights recommendations and observations: Kenya</title>
<style>
:root{
  --paper:#f4f0e8; --ink:#1d1b18; --rule:#d9d2c3; --accent:#9b2335;
  --upr:#c2410c; --tb:#0f766e; --sp:#7c3aed;
}
*{box-sizing:border-box}
[hidden]{display:none!important}
html,body{margin:0;padding:0}
body{background:var(--paper);color:var(--ink);font:16px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif}
a{color:var(--accent)}
a:focus,button:focus,input:focus,select:focus,[tabindex]:focus{outline:2px solid var(--accent);outline-offset:2px}
.mono{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:11.5px;letter-spacing:.08em;text-transform:uppercase}
.serif{font-family:Georgia,"Times New Roman",serif}
.hint{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:11.5px;color:#6b6355;letter-spacing:.02em}
.rule{border:0;border-top:1px solid var(--rule);margin:0}

/* header */
header{padding:18px 24px 14px;border-bottom:1px solid var(--rule)}
header .mono{color:#6b6355}
header h1{font-family:Georgia,"Times New Roman",serif;font-size:28px;font-weight:normal;margin:6px 0 4px}
header .meta{font-size:13.5px;color:#4a453d}
header .meta a{color:var(--accent)}

/* layout */
.layout{display:flex;min-height:calc(100vh - 130px)}
nav.rail{width:270px;flex:0 0 270px;border-right:1px solid var(--rule);padding:16px 18px}
main{flex:1;padding:20px 28px 60px;min-width:0}

/* rail */
.rail-head{display:flex;justify-content:space-between;align-items:baseline}
.rail-head .mono{color:#6b6355}
.rail-head button{background:none;border:0;color:var(--accent);font-family:ui-monospace,Menlo,Consolas,monospace;font-size:11px;letter-spacing:.05em;cursor:pointer;padding:0}
.bignum{font-family:Georgia,"Times New Roman",serif;font-size:46px;line-height:1.05;margin:10px 0 2px}
.bignum small{font-size:16px;color:#6b6355;font-family:ui-monospace,Menlo,Consolas,monospace;letter-spacing:.02em}
.sharebar{height:5px;background:#e6dfd0;margin:8px 0 4px;position:relative}
.sharebar span{position:absolute;left:0;top:0;bottom:0;background:var(--accent)}
.chips{margin:10px 0 4px;display:flex;flex-wrap:wrap;gap:6px}
.chip{display:inline-flex;align-items:center;gap:6px;border:1px solid var(--rule);background:#fbf8f1;border-radius:12px;padding:2px 6px 2px 10px;font-size:12.5px}
.chip button{border:0;background:none;color:var(--accent);cursor:pointer;font-size:14px;line-height:1;padding:0 2px}
details.filter{border-top:1px solid var(--rule);margin-top:10px}
details.filter summary{cursor:pointer;list-style:none;display:flex;justify-content:space-between;align-items:center;padding:8px 0;font-family:ui-monospace,Menlo,Consolas,monospace;font-size:11.5px;letter-spacing:.08em;text-transform:uppercase}
details.filter summary::-webkit-details-marker{display:none}
details.filter summary .num{color:var(--accent)}
details.filter .inner{padding:2px 0 12px;display:flex;flex-direction:column;gap:8px}
label.fld{display:block;font-size:13px}
label.fld .hint{display:block;margin-bottom:2px}
input[type=text],select{width:100%;padding:6px 8px;border:1px solid var(--rule);background:#fbf8f1;font:14px -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;color:var(--ink)}
.radios{display:flex;flex-wrap:wrap;gap:4px}
.radios label{font-size:13px;border:1px solid var(--rule);padding:2px 8px;cursor:pointer;background:#fbf8f1}
.radios input{margin-right:4px}
.radios label.on{border-color:var(--accent);color:var(--accent)}
.cnt{color:#6b6355;font-size:11.5px}

/* tabs */
.tabs{display:flex;gap:0;border-bottom:1px solid var(--rule);padding:0 28px}
.tab{background:none;border:0;border-bottom:3px solid transparent;padding:10px 16px 8px;cursor:pointer;font-family:ui-monospace,Menlo,Consolas,monospace;font-size:12px;letter-spacing:.06em;color:#4a453d}
.tab[aria-selected="true"]{color:var(--accent);border-bottom-color:var(--accent)}
.tab:hover{color:var(--accent)}

/* tiles */
.tiles{display:flex;flex-wrap:wrap;gap:26px;margin:8px 0 6px}
.tile{min-width:200px}
.tile .n{font-family:Georgia,"Times New Roman",serif;font-size:48px;line-height:1.05}
.tile .lbl{margin:2px 0}
.tile .sub{font-size:13px;color:#4a453d}
.dot{display:inline-block;width:9px;height:9px;border-radius:50%;margin-right:6px}
.note{font-size:12.5px;color:#6b6355;margin:2px 0 14px;font-family:ui-monospace,Menlo,Consolas,monospace;letter-spacing:.01em}
figure{margin:26px 0}
figure .figtitle{font-family:Georgia,"Times New Roman",serif;font-size:19px;margin:0 0 2px}
figure .figno{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:11.5px;letter-spacing:.08em;color:var(--accent);margin-bottom:4px}
.chartwrap{position:relative;height:auto}

/* tables */
table{border-collapse:collapse;width:100%;font-size:14.5px}
caption{text-align:left;font-family:ui-monospace,Menlo,Consolas,monospace;font-size:11.5px;color:#6b6355;padding:4px 0;letter-spacing:.03em}
th,td{text-align:left;padding:6px 10px;border-bottom:1px solid var(--rule);vertical-align:top}
th{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:11px;letter-spacing:.06em;text-transform:uppercase;font-weight:normal;color:#4a453d;cursor:default}
th.sortable{cursor:pointer}
td.num,th.num{text-align:right;font-variant-numeric:tabular-nums}
tr.rec{cursor:pointer}
tr.rec:hover{background:#efe9dc}
tr.exp>td{background:#fbf8f1}
.para-big{font-family:Georgia,"Times New Roman",serif;font-size:34px;color:var(--accent);line-height:1;margin-right:14px}
.fulltext{font-family:Georgia,"Times New Roman",serif;font-size:16.5px;line-height:1.55;margin:8px 0;white-space:pre-wrap}
.labels{margin:10px 0;display:flex;flex-wrap:wrap;gap:6px}
.lchip{border:1px solid var(--rule);background:#fbf8f1;border-radius:3px;padding:1px 8px;font-size:12.5px}
.lchip.sdgt{border-color:#c9bfa9}
.btn{background:none;border:1px solid var(--accent);color:var(--accent);padding:5px 12px;cursor:pointer;font-family:ui-monospace,Menlo,Consolas,monospace;font-size:11.5px;letter-spacing:.05em}
.btn:hover{background:var(--accent);color:#f4f0e8}
mark{background:#f0d9a8;padding:0 1px}
.states-list{margin:6px 0 0;padding-left:0;list-style:none;columns:2;column-gap:30px;font-size:13.5px}
.states-list li{break-inside:avoid;padding:2px 0;border-bottom:1px dotted var(--rule)}

/* checks */
.check{display:flex;gap:14px;padding:8px 0;border-bottom:1px solid var(--rule);font-size:14px}
.check .mark{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:12px;white-space:nowrap;min-width:70px}
.pass{color:#0f766e}.fail{color:var(--accent)}.warn{color:#b45309}
.check .what{flex:1}
.check .vals{color:#4a453d;font-size:13px}
.samplecard{border:1px solid var(--rule);margin:8px 0;background:#fbf8f1}
.samplecard>button{width:100%;text-align:left;background:none;border:0;padding:9px 12px;cursor:pointer;font-size:14px;display:flex;gap:10px;align-items:baseline}
.samplecard .body{padding:0 14px 14px;border-top:1px solid var(--rule)}
.verdicts{display:flex;gap:8px;margin-top:8px}
.verdicts .btn.sel{background:var(--accent);color:#f4f0e8}
h2.sec{font-family:Georgia,"Times New Roman",serif;font-size:22px;font-weight:normal;margin:26px 0 6px}
.method p{max-width:70ch}
footer{border-top:1px solid var(--rule);padding:10px 24px;font-family:ui-monospace,Menlo,Consolas,monospace;font-size:11px;color:#6b6355;letter-spacing:.04em;display:flex;justify-content:space-between;flex-wrap:wrap;gap:6px}
.nomatch{font-family:Georgia,"Times New Roman",serif;font-size:22px;color:#6b6355;padding:30px 0}
.legend{display:flex;gap:16px;font-size:12.5px;margin:4px 0 8px}
.legend span.dot{margin-right:5px}
@media(max-width:900px){.layout{flex-direction:column}nav.rail{width:100%;flex:none;border-right:0;border-bottom:1px solid var(--rule)}}
</style>
</head>
<body>

<header>
  <div class="mono" id="hd-label"></div>
  <h1 id="hd-title"></h1>
  <div class="meta" id="hd-meta"></div>
</header>

<div class="tabs" role="tablist" aria-label="Dashboard tabs">
  <button class="tab" role="tab" id="tab-01" aria-controls="panel-01" aria-selected="true" tabindex="0">01 OVERVIEW</button>
  <button class="tab" role="tab" id="tab-02" aria-controls="panel-02" aria-selected="false" tabindex="-1">02 RECORDS</button>
  <button class="tab" role="tab" id="tab-03" aria-controls="panel-03" aria-selected="false" tabindex="-1">03 CHECK</button>
  <button class="tab" role="tab" id="tab-04" aria-controls="panel-04" aria-selected="false" tabindex="-1">04 METHOD &amp; EXPORT</button>
</div>

<div class="layout">
<nav class="rail" aria-label="Filters">
  <div class="rail-head"><span class="mono">FILTERS</span><button id="clear-all" hidden>Clear all</button></div>
  <div class="bignum" aria-live="polite"><span id="match-n">0</span><small> of <span id="total-n">0</span><br>matching records</small></div>
  <div class="sharebar"><span id="sharebar-fill"></span></div>
  <div class="hint" id="sharebar-note"></div>
  <div class="chips" id="chips"></div>
  <div id="rail-filters"></div>
</nav>

<main>
  <section id="panel-01" role="tabpanel" aria-labelledby="tab-01" tabindex="0"></section>
  <section id="panel-02" role="tabpanel" aria-labelledby="tab-02" tabindex="0" hidden></section>
  <section id="panel-03" role="tabpanel" aria-labelledby="tab-03" tabindex="0" hidden></section>
  <section id="panel-04" role="tabpanel" aria-labelledby="tab-04" tabindex="0" hidden></section>
</main>
</div>

<footer>
  <span id="ft-left"></span>
  <span>Nothing leaves this browser except the clipboard write on “Copy”.</span>
</footer>

<script>
"use strict";
const uhri = window.WORKSHOP_DATA.uhri;
const records = uhri.records;
const country = uhri.country;
const sdgNames = uhri.sdg_names || {};
const N = records.length;

/* ---------- derived per-record ---------- */
const PARA_RE = /^(\d{1,3}(?:\.\d{1,3})?)\.?\s/;
const STATE_RUN_RE = /((?:\s*\((?:[^()]|\([^()]*\))*\))+)\s*[;.]?\s*$/;
const STATE_GRP_RE = /\((?:[^()]|\([^()]*\))*\)/g;
function paraNo(r){ const m = (r.text||"").match(PARA_RE); return m ? m[1] : null; }
function states(r){
  if (r.mechanism !== "Universal Periodic Review") return null;
  const m = (r.text||"").match(STATE_RUN_RE);
  if (!m) return ["(State not found)"];
  const out = [];
  let g;
  const re = /\((?:[^()]|\([^()]*\))*\)/g;
  while ((g = re.exec(m[1])) !== null){
    let s = g[0].slice(1,-1).trim();
    if (!s.includes(",") && s.length <= 60) out.push(s);
    else if (out.length === 0 && s) return ["(State not found)"];
  }
  return out.length ? out : ["(State not found)"];
}
records.forEach(r => {
  r._para = paraNo(r);
  r._states = states(r);
  r._themes = r.themes || [];
  r._sdgs = r.sdgs || [];
  r._ap = r.affected_persons || [];
  r._targets = r.sdg_targets || [];
});

/* ---------- state ---------- */
let filt = { kw:"", mechanism:"", body:"", type:"", state:"", yFrom:"", yTo:"", sdg:"", themes:new Set() };
let sortDir = -1;           // date descending by default
let shown = 50;             // table pagination
let tab = "01";
let charts = {};

/* ---------- filtering ---------- */
function filtered(){
  const kw = filt.kw.trim().toLowerCase();
  const words = kw ? kw.split(/\s+/) : [];
  return records.filter(r => {
    if (filt.mechanism && r.mechanism !== filt.mechanism) return false;
    if (filt.body && r.body !== filt.body) return false;
    if (filt.type && r.type !== filt.type) return false;
    if (filt.state && !(r._states && r._states.includes(filt.state))) return false;
    if (filt.yFrom && r.year < +filt.yFrom) return false;
    if (filt.yTo && r.year > +filt.yTo) return false;
    if (filt.sdg && !r._sdgs.includes(+filt.sdg)) return false;
    for (const t of filt.themes) if (!r._themes.includes(t)) return false;
    if (words.length){
      const hay = (r.text + " " + r.symbol).toLowerCase();
      for (const w of words) if (!hay.includes(w)) return false;
    }
    return true;
  });
}
function activeFilterCount(){
  return (filt.kw?1:0)+(filt.mechanism?1:0)+(filt.body?1:0)+(filt.type?1:0)+(filt.state?1:0)
       + (filt.yFrom?1:0)+(filt.yTo?1:0)+(filt.sdg?1:0)+filt.themes.size;
}

/* ---------- helpers ---------- */
const esc = s => String(s).replace(/[&<>"']/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
const fmt = n => n.toLocaleString("en-US");
function firstLine(t){
  t = t || "";
  if (t.length <= 120) return t;
  let cut = t.slice(0,120), sp = cut.lastIndexOf(" ");
  if (sp > 60) cut = cut.slice(0, sp);
  return cut.replace(/[,;:]$/,"") + "…";
}
function markText(t, kw){
  const words = kw.trim() ? kw.trim().split(/\s+/).map(w => w.replace(/[.*+?^${}()|[\]\\]/g,"\\$&")) : [];
  if (!words.length) return esc(t);
  let s = esc(t);
  for (const w of words) s = s.replace(new RegExp("(" + w + ")","gi"), "<mark>$1</mark>");
  return s;
}
function distinct(arr){ return [...new Set(arr)]; }
function sortedRows(list){
  return list.slice().sort((a,b) => {
    if (a.date !== b.date) return (a.date < b.date ? 1 : -1) * -sortDir;
    if (a.body !== b.body) return a.body < b.body ? -1 : 1;
    const pa = a._para ? parseFloat(a._para) : Infinity, pb = b._para ? parseFloat(b._para) : Infinity;
    if (pa !== pb) return pa - pb;
    return 0;
  });
}

/* ---------- header & footer ---------- */
(function(){
  const years = records.map(r=>r.year);
  const docs = distinct(records.map(r=>r.symbol)).length;
  document.getElementById("hd-label").textContent = "UHRI · " + country;
  document.getElementById("hd-title").textContent = "UN human rights recommendations and observations: " + country;
  document.getElementById("hd-meta").innerHTML =
    'Source: <a href="'+esc(uhri.source_url)+'" target="_blank" rel="noopener">'+esc(uhri.source)+'</a> · '
    + fmt(N) + ' records · ' + fmt(docs) + ' documents · ' + Math.min(...years) + '–' + Math.max(...years)
    + ' · built ' + esc(uhri.built) + ' · <span class="hint">dated by document</span>';
  document.getElementById("ft-left").innerHTML = 'Built on OHCHR UHRI data · ' + fmt(N) + ' records · <a href="'+esc(uhri.source_url)+'" target="_blank" rel="noopener">source</a>';
  document.getElementById("total-n").textContent = fmt(N);
})();

/* ---------- tabs ---------- */
const tabIds = ["01","02","03","04"];
const tabs = tabIds.map(t => document.getElementById("tab-"+t));
tabs.forEach((tb,i) => {
  tb.addEventListener("click", () => selectTab(tabIds[i]));
  tb.addEventListener("keydown", e => {
    let j = null;
    if (e.key === "ArrowRight") j = (i+1) % tabIds.length;
    if (e.key === "ArrowLeft") j = (i-1+tabIds.length) % tabIds.length;
    if (j !== null){ e.preventDefault(); selectTab(tabIds[j]); tabs[j].focus(); }
  });
});
function selectTab(t){
  tab = t;
  tabs.forEach(tb => {
    const on = tb.id === "tab-"+t;
    tb.setAttribute("aria-selected", on);
    tb.tabIndex = on ? 0 : -1;
  });
  tabIds.forEach(x => document.getElementById("panel-"+x).hidden = (x !== t));
  render();
}

/* ---------- rail ---------- */
let kwTimer = null;
function railHTML(){
  const years = distinct(records.map(r=>r.year)).sort((a,b)=>a-b);
  const mechs = distinct(records.map(r=>r.mechanism)).sort();
  let h = "";
  // 01 KEYWORD
  h += '<details class="filter" id="f-kw"><summary><span><span class="num">01</span> KEYWORD</span><span class="hint">toggle</span></summary><div class="inner">'
     + '<label class="fld"><span class="hint">literal match, not synonyms</span>'
     + '<input type="text" id="kw-input" value="'+esc(filt.kw)+'" placeholder="e.g. torture"></label></div></details>';
  // 02 MECHANISM, BODY, TYPE
  h += '<details class="filter" id="f-mbt"><summary><span><span class="num">02</span> MECHANISM, BODY, TYPE</span><span class="hint">toggle</span></summary><div class="inner">';
  h += '<label class="fld"><span class="hint">Mechanism</span><select id="sel-mech"><option value="">all</option>'
     + mechs.map(m=>'<option value="'+esc(m)+'"'+(filt.mechanism===m?" selected":"")+'>'+esc(m)+'</option>').join("")
     + '</select></label>';
  const inMech = records.filter(r=>!filt.mechanism || r.mechanism===filt.mechanism);
  const bodies = {};
  inMech.forEach(r=>bodies[r.body]=(bodies[r.body]||0)+1);
  h += '<label class="fld"><span class="hint">Body or mandate</span><select id="sel-body"><option value="">all</option>'
     + Object.keys(bodies).sort().map(b=>'<option value="'+esc(b)+'"'+(filt.body===b?" selected":"")+'>'+esc(b)+' <span class="cnt">('+bodies[b]+')</span></option>').join("")
     + '</select></label>';
  const types = {};
  inMech.forEach(r=>types[r.type]=(types[r.type]||0)+1);
  h += '<label class="fld"><span class="hint">Type</span><select id="sel-type"><option value="">all</option>'
     + Object.keys(types).sort().map(t=>'<option value="'+esc(t)+'"'+(filt.type===t?" selected":"")+'>'+esc(t)+' <span class="cnt">('+types[t]+')</span></option>').join("")
     + '</select></label>';
  const stAll = {};
  records.forEach(r=>{ if (r._states) r._states.forEach(s=>{ if (s!=="(State not found)") stAll[s]=(stAll[s]||0)+1; }); });
  const stKeys = Object.keys(stAll).sort();
  if (stKeys.length){
    h += '<label class="fld"><span class="hint">Recommending State (UPR)</span><select id="sel-state"><option value="">all</option>'
       + stKeys.map(s=>'<option value="'+esc(s)+'"'+(filt.state===s?" selected":"")+'>'+esc(s)+' ('+stAll[s]+')</option>').join("")
       + '</select></label>';
  }
  h += '</div></details>';
  // 03 YEARS AND SDG
  h += '<details class="filter" id="f-ys"><summary><span><span class="num">03</span> YEARS AND SDG</span><span class="hint">toggle</span></summary><div class="inner">'
     + '<label class="fld"><span class="hint">Year from</span><select id="sel-yf"><option value="">(earliest)</option>'
     + years.map(y=>'<option value="'+y+'"'+(String(filt.yFrom)===String(y)?" selected":"")+'>'+y+'</option>').join("")
     + '</select></label>'
     + '<label class="fld"><span class="hint">Year to</span><select id="sel-yf2" id="sel-yt"><option value="">(latest)</option>' // id fixed below
     + years.map(y=>'<option value="'+y+'"'+(String(filt.yTo)===String(y)?" selected":"")+'>'+y+'</option>').join("")
     + '</select></label>';
  const goals = {};
  records.forEach(r=>r._sdgs.forEach(g=>{ goals[g]=(goals[g]||0)+1; }));
  h += '<label class="fld"><span class="hint">SDG goal</span><select id="sel-sdg"><option value="">all</option>'
     + Object.keys(goals).map(Number).sort((a,b)=>a-b).map(g=>'<option value="'+g+'"'+(String(filt.sdg)===String(g)?" selected":"")+'>SDG '+g+' · '+esc(sdgNames[String(g)]||"(name missing)")+' <span class="cnt">('+goals[g]+')</span></option>').join("")
     + '</select></label></div></details>';
  return h;
}
function wireRail(){
  const kw = document.getElementById("kw-input");
  if (kw){
    kw.addEventListener("input", () => {
      clearTimeout(kwTimer);
      kwTimer = setTimeout(()=>{ filt.kw = kw.value; shown = 50; render(); }, 300);
    });
  }
  const bind = (id, key) => {
    const el = document.getElementById(id);
    if (el) el.addEventListener("change", () => {
      filt[key] = el.value;
      if (key === "mechanism" && filt.body && !records.some(r=>r.mechanism===filt.mechanism && r.body===filt.body)) filt.body = "";
      if (key === "yFrom" || key === "yTo"){
        let a = filt.yFrom ? +filt.yFrom : -Infinity, b = filt.yTo ? +filt.yTo : Infinity;
        if (a > b){ const t = filt.yFrom; filt.yFrom = filt.yTo; filt.yTo = t; }
      }
      shown = 50; render();
    });
  };
  bind("sel-mech","mechanism"); bind("sel-body","body"); bind("sel-type","type"); bind("sel-state","state");
  bind("sel-yf","yFrom"); bind("sel-yt","yTo"); bind("sel-sdg","sdg");
  document.querySelectorAll("details.filter").forEach(d => {
    d.addEventListener("toggle", () => { if (d.open) document.querySelectorAll("details.filter").forEach(o=>{ if (o!==d) o.open=false; }); });
  });
}
function chipsHTML(){
  const chips = [];
  const add = (key,label) => chips.push({key,label});
  if (filt.kw) add("kw", 'keyword: “'+filt.kw+'”');
  if (filt.mechanism) add("mechanism", filt.mechanism);
  if (filt.body) add("body", filt.body);
  if (filt.type) add("type", filt.type);
  if (filt.state) add("state", "State: "+filt.state);
  if (filt.yFrom || filt.yTo) add("years", "years "+(filt.yFrom||"…")+"–"+(filt.yTo||"…"));
  if (filt.sdg) add("sdg", "SDG "+filt.sdg);
  filt.themes.forEach(t => add("theme:"+t, "theme: "+t));
  return chips.map(c => '<span class="chip">'+esc(c.label)+' <button data-chip="'+esc(c.key)+'" aria-label="Remove filter '+esc(c.label)+'">×</button></span>').join("");
}

/* ---------- theme stats ---------- */
function themeStats(list){
  const map = {};
  list.forEach(r => r._themes.forEach(t => {
    if (!map[t]) map[t] = { n:0, y1:Infinity, y2:-Infinity };
    map[t].n++;
    if (r.year < map[t].y1) map[t].y1 = r.year;
    if (r.year > map[t].y2) map[t].y2 = r.year;
  }));
  return Object.keys(map).map(t => ({theme:t, n:map[t].n, y1:map[t].y1, y2:map[t].y2}))
    .sort((a,b) => b.n - a.n || (a.theme < b.theme ? -1 : 1));
}

/* ---------- charts ---------- */
const MECH_COLOR = {"Universal Periodic Review":"#c2410c","Treaty bodies":"#0f766e","Special Procedures":"#7c3aed"};
const valueLabelPlugin = {
  id:"vlabel",
  afterDatasetsDraw(chart){
    const {ctx} = chart;
    const meta = chart.getDatasetMeta(0);
    const max = chart.scales.x.max;
    meta.data.forEach((bar,i) => {
      const v = chart.data.datasets[0].data[i];
      ctx.save();
      ctx.fillStyle = "#1d1b18";
      ctx.font = "12.5px -apple-system, sans-serif";
      ctx.textAlign = "left";
      ctx.textBaseline = "middle";
      const x = Math.min(bar.x + 6, chart.chartArea.right - 24);
      ctx.fillText(fmt(v), x, bar.y);
      ctx.restore();
    });
  }
};
function drawFig1(list){
  const el = document.getElementById("fig1-canvas");
  if (!el) return;
  const top = themeStats(list).slice(0,10);
  if (charts.f1) charts.f1.destroy();
  charts.f1 = new Chart(el, {
    type:"bar",
    data:{ labels: top.map(t=>t.theme), datasets:[{ data: top.map(t=>t.n), backgroundColor:"rgba(155,35,53,0.8)" }]},
    options:{
      indexAxis:"y", maintainAspectRatio:false,
      height: Math.max(180, top.length*34+40),
      scales:{
        x:{ beginAtZero:true, grid:{display:false}, ticks:{font:{size:12}} },
        y:{ grid:{display:false}, ticks:{font:{size:13}, crossAlign:"far"} }
      },
      plugins:{ legend:{display:false}, tooltip:{enabled:false} },
      onClick(e, els){ if (els.length){ const t = top[els[0].index].theme; filt.themes.has(t)?filt.themes.delete(t):filt.themes.add(t); render(); } },
      onHover(e, els){ e.native.target.style.cursor = els.length ? "pointer":"default"; }
    },
    plugins:[valueLabelPlugin]
  });
  charts.f1._stats = top;
  const tbl = document.getElementById("fig1-table");
  if (tbl){
    if (!top.length){ tbl.innerHTML = '<p class="nomatch">No records match.</p>'; }
    else {
      tbl.innerHTML = '<table><caption>Same ten themes as the chart · a record can carry several themes, so the Records column sums to more than '+fmt(list.length)+' · Source: '+esc(uhri.source)+'</caption>'
      + '<thead><tr><th scope="col">Theme</th><th scope="col" class="num">Records</th><th scope="col" class="num">% of filtered</th><th scope="col">Years</th></tr></thead><tbody>'
      + top.map(t => '<tr><td>'+esc(t.theme)+'</td><td class="num">'+fmt(t.n)+'</td><td class="num">'+(100*t.n/list.length).toFixed(1)+'%</td><td>'+t.y1+'–'+t.y2+'</td></tr>').join("")
      + '</tbody></table>';
    }
  }
}
function drawFig2(list){
  const el = document.getElementById("fig2-canvas");
  if (!el) return;
  if (charts.f2) charts.f2.destroy();
  const mechs = distinct(records.map(r=>r.mechanism)).sort();
  const years = [];
  for (let y = Math.min(...records.map(r=>r.year)); y <= Math.max(...records.map(r=>r.year)); y++) years.push(y);
  const counts = {};
  list.forEach(r => { counts[r.year] = counts[r.year] || {}; counts[r.year][r.mechanism] = (counts[r.year][r.mechanism]||0)+1; });
  charts.f2 = new Chart(el, {
    type:"bar",
    data:{ labels: years, datasets: mechs.map(m => ({ label:m, data: years.map(y => (counts[y]&&counts[y][m])||0), backgroundColor: MECH_COLOR[m]||"#9b2335" }))},
    options:{
      maintainAspectRatio:false,
      scales:{
        x:{ stacked:true, grid:{display:false}, title:{display:true,text:"Year (empty years are visible gaps)",font:{size:11}} },
        y:{ stacked:true, beginAtZero:true, grid:{color:"#e6dfd0"}, ticks:{precision:0} }
      },
      plugins:{ legend:{position:"bottom", labels:{boxWidth:10,font:{size:12}}}, tooltip:{enabled:true} }
    }
  });
}

/* ---------- TAB 01 ---------- */
function renderOverview(list){
  const el = document.getElementById("panel-01");
  const docs = distinct(list.map(r=>r.symbol)).length;
  const years = list.map(r=>r.year);
  const types = {}; list.forEach(r=>types[r.type]=(types[r.type]||0)+1);
  const typeLine = Object.keys(types).sort().map(t=>fmt(types[t])+" "+t).join(" · ") || "—";
  const mechs = {};
  list.forEach(r=>{ mechs[r.mechanism] = mechs[r.mechanism] || {n:0,docs:new Set(),y2:-Infinity}; mechs[r.mechanism].n++; mechs[r.mechanism].docs.add(r.symbol); if (r.year>mechs[r.mechanism].y2) mechs[r.mechanism].y2=r.year; });
  const mechKeys = Object.keys(mechs).sort((a,b)=>mechs[b].n-mechs[a].n);
  let h = '<div class="tiles">'
    + '<div class="tile"><div class="n">'+fmt(list.length)+'</div><div class="lbl mono">ALL RECORDS</div><div class="sub">'+typeLine+'</div></div>'
    + '<div class="tile"><div class="n">'+fmt(docs)+'</div><div class="lbl mono">DOCUMENTS</div><div class="sub">distinct symbols</div></div>'
    + (years.length ? '<div class="tile"><div class="n">'+Math.min(...years)+'–'+Math.max(...years)+'</div><div class="lbl mono">YEARS</div><div class="sub">min–max of year</div></div>' : '<div class="tile"><div class="n">—</div><div class="lbl mono">YEARS</div></div>')
    + '</div>'
    + '<p class="note">How this is computed: every count is a loop over the filtered records · Type breakdown uses the UN’s own type values.</p>';
  if (!list.length) h += '<p class="nomatch">No records match.</p>';
  else {
    h += '<div class="tiles">';
    mechKeys.forEach(m => {
      h += '<div class="tile"><div class="lbl mono"><span class="dot" style="background:'+(MECH_COLOR[m]||"#9b2335")+'"></span>'+esc(m).toUpperCase()+'</div>'
         + '<div class="n" style="font-size:36px">'+fmt(mechs[m].n)+'</div>'
         + '<div class="sub">'+fmt(mechs[m].docs.size)+' documents · latest '+mechs[m].y2+' · '+(100*mechs[m].n/list.length).toFixed(0)+'% of filtered set</div></div>';
    });
    h += '</div>';
    // UPR states link
    const uprList = list.filter(r=>r.mechanism==="Universal Periodic Review");
    if (uprList.length){
      h += '<div id="upr-states-wrap"><button class="btn" id="upr-states-btn">see the States</button>'
         + '<span class="hint" style="margin-left:8px">Ten States that made most recommendations to '+esc(country)+' — opens in place</span><div id="upr-states" hidden></div></div>';
    }
  }
  h += '<figure><div class="figno">FIG.01</div><p class="figtitle">Ten most frequent themes among '+fmt(list.length)+' filtered records</p>'
     + '<div class="chartwrap" style="height:'+Math.max(220, Math.min(10, themeStats(list).length)*34+50)+'px"><canvas id="fig1-canvas" aria-label="Bar chart of ten most frequent themes"></canvas></div>'
     + '<p class="note">Click a bar to filter by that theme · a record can carry several themes, so the bars add up to more than '+fmt(list.length)+' · % is of records, not labels.</p>'
     + '<div id="fig1-table"></div></figure>'
     + '<figure><div class="figno">FIG.02</div><p class="figtitle">Records per year by mechanism, '+fmt(list.length)+' filtered records</p>'
     + '<div class="chartwrap" style="height:300px"><canvas id="fig2-canvas" aria-label="Stacked bar chart of records per year by mechanism"></canvas></div>'
     + '<p class="note">How this is computed: records per year per mechanism in the filtered set, zero for missing combinations · Source: '+esc(uhri.source)+'</p></figure>';
  el.innerHTML = h;
  if (list.length){
    // UPR states
    const btn = document.getElementById("upr-states-btn");
    if (btn) btn.addEventListener("click", () => {
      const box = document.getElementById("upr-states");
      if (!box.hidden){ box.hidden = true; return; }
      const sc = {};
      uprList.forEach(r=>r._states.forEach(s=>{ if (s!=="(State not found)") sc[s]=(sc[s]||0)+1; }));
      const top = Object.keys(sc).sort((a,b)=>sc[b]-sc[a]|| (a<b?-1:1)).slice(0,10);
      box.innerHTML = '<p class="mono" style="margin:10px 0 4px">TEN STATES THAT MADE MOST RECOMMENDATIONS TO '+esc(country).toUpperCase()+'</p>'
        + '<ol class="states-list">' + top.map(s=>'<li>'+esc(s)+' <span class="cnt">'+sc[s]+'</span></li>').join("") + "</ol>"
        + '<p class="note">Counts recommendations, not influence · two States can co-sponsor one line · Source: '+esc(uhri.source)+'</p>';
      box.hidden = false;
    });
    drawFig1(list);
    drawFig2(list);
  }
}

/* ---------- TAB 02 ---------- */
function renderRecords(list){
  const el = document.getElementById("panel-02");
  let h = '<label class="fld" style="max-width:420px;margin-bottom:14px"><span class="hint">Search '+fmt(list.length)+' records · literal match, not synonyms</span>'
        + '<input type="text" id="rec-search" value="'+esc(filt.kw)+'" placeholder="e.g. torture"></label>';
  if (!list.length){
    h += '<p class="nomatch">No records match.</p>';
    el.innerHTML = h; wireRecSearch(); return;
  }
  const rows = sortedRows(list);
  const slice = rows.slice(0, shown);
  h += '<table><caption id="rec-caption">Showing '+fmt(slice.length)+' of '+fmt(rows.length)+' matching records (of '+fmt(N)+' in the file) · newest first · click the Date header to reverse · click a row to expand</caption>'
     + '<thead><tr><th scope="col" class="sortable" id="th-date" aria-sort="'+(sortDir===-1?"descending":"ascending")+'">Date ↕</th><th scope="col">Body</th><th scope="col">Symbol</th><th scope="col" class="num">Para.</th><th scope="col">First line</th><th scope="col">Recommending State</th></tr></thead><tbody>';
  slice.forEach(r => {
    const st = r._states ? r._states.filter(s=>s!=="(State not found)").join(", ") : null;
    h += '<tr class="rec" data-id="'+esc(r.id)+'" tabindex="0" aria-expanded="false">'
       + '<td style="white-space:nowrap">'+esc(r.date)+'</td>'
       + '<td>'+esc(r.body)+'</td>'
       + '<td><a href="'+esc(r.doc_url)+'" target="_blank" rel="noopener">'+esc(r.symbol)+'</a></td>'
       + '<td class="num">'+(r._para?esc(r._para):"—")+'</td>'
       + '<td>'+markText(firstLine(r.text), filt.kw)+'</td>'
       + '<td>'+(st ? esc(st) : (r._states ? "—" : "—"))+'</td>'
       + '</tr>';
  });
  h += '</tbody></table>';
  if (shown < rows.length) h += '<p><button class="btn" id="more-btn">Show 50 more</button> <span class="hint">'+fmt(rows.length - shown)+' more rows</span></p>';
  el.innerHTML = h;
  wireRecSearch();
  const more = document.getElementById("more-btn");
  if (more) more.addEventListener("click", () => { shown += 50; render(); });
  document.getElementById("th-date").addEventListener("click", () => { sortDir = -sortDir; render(); });
  el.querySelectorAll("tr.rec").forEach(tr => {
    const toggle = () => expandRow(tr, list);
    tr.addEventListener("click", e => { if (e.target.closest("a,button")) return; toggle(); });
    tr.addEventListener("keydown", e => { if (e.key === "Enter"){ e.preventDefault(); toggle(); } });
  });
}
function wireRecSearch(){
  const s = document.getElementById("rec-search");
  if (!s) return;
  s.addEventListener("input", () => {
    clearTimeout(kwTimer);
    kwTimer = setTimeout(()=>{ filt.kw = s.value; shown = 50; render();
      const railKw = document.getElementById("kw-input"); if (railKw && railKw !== document.activeElement) railKw.value = s.value;
    }, 300);
  });
}
function expandRow(tr, list){
  const next = tr.nextElementSibling;
  if (next && next.classList.contains("exp")){ next.remove(); tr.setAttribute("aria-expanded","false"); return; }
  document.querySelectorAll("tr.exp").forEach(x => { x.previousElementSibling.setAttribute("aria-expanded","false"); x.remove(); });
  const r = records.find(x => x.id === tr.dataset.id);
  const labels = [];
  r._themes.forEach(t => labels.push('<span class="lchip">'+esc(t)+'</span>'));
  if (r._sdgs.length) labels.push('<span class="lchip sdgt">SDG '+r._sdgs.join(", ")+'</span>');
  r._sdgs.forEach(g => { if (sdgNames[String(g)]) labels.push('<span class="lchip sdgt">SDG '+g+' · '+esc(sdgNames[String(g)])+'</span>'); });
  r._targets.forEach(t => labels.push('<span class="lchip sdgt">'+esc(t)+'</span>'));
  r._ap.forEach(p => labels.push('<span class="lchip">affected: '+esc(p)+'</span>'));
  if (r.section) labels.push('<span class="lchip">section: '+esc(r.section)+'</span>');
  if (!r._themes.length) labels.push('<span class="lchip">no themes (not labelled)</span>');
  if (!r._sdgs.length) labels.push('<span class="lchip">no SDGs (not labelled)</span>');
  if (!r._ap.length) labels.push('<span class="lchip">no affected persons (not labelled)</span>');
  const cite = r._para ? r.symbol + ", para. " + r._para : r.symbol;
  const row = document.createElement("tr");
  row.className = "exp";
  row.innerHTML = '<td colspan="6"><div style="display:flex;align-items:flex-start">'
    + '<span class="para-big">'+(r._para?esc(r._para):"—")+'</span>'
    + '<div style="flex:1"><p class="fulltext">'+markText(r.text, filt.kw)+'</p>'
    + '<div class="labels">'+labels.join("")+'</div>'
    + '<button class="btn" data-copy="'+esc(cite)+'">'+(r._para ? "Copy citation" : "Copy citation (no paragraph number in this extract)")+'</button> '
    + '<a class="btn" style="text-decoration:none;display:inline-block;margin-left:8px" href="'+esc(r.doc_url)+'" target="_blank" rel="noopener">Open the UN document</a>'
    + ' <span class="hint" style="margin-left:10px">citation: '+esc(cite)+'</span>'
    + '</div></div></td>';
  tr.after(row);
  tr.setAttribute("aria-expanded","true");
  row.querySelector("[data-copy]").addEventListener("click", e => {
    copyText(e.target.dataset.copy, e.target);
  });
}
function copyText(text, btn){
  const done = () => {
    if (!btn) return;
    const old = btn.textContent;
    btn.textContent = "Copied";
    setTimeout(()=>{ btn.textContent = old; }, 2000);
  };
  if (navigator.clipboard && navigator.clipboard.writeText){
    navigator.clipboard.writeText(text).then(done).catch(()=>fallbackCopy(text, done));
  } else fallbackCopy(text, done);
}
function fallbackCopy(text, done){
  const ta = document.createElement("textarea");
  ta.value = text; document.body.appendChild(ta); ta.select();
  try { document.execCommand("copy"); } catch(e){}
  ta.remove(); done();
}

/* ---------- TAB 03: checks ---------- */
function checkLine(pass, what, vals, warn){
  const cls = pass ? "pass" : (warn ? "warn" : "fail");
  const mark = pass ? "✓ pass" : (warn ? "⚠ warning" : "✗ check failed");
  return '<div class="check"><span class="mark '+cls+'">'+mark+'</span><div class="what">'+what+(vals?'<div class="vals">'+vals+'</div>':'')+'</div></div>';
}
let sample = null; // {seed, ids:[], verdicts:{}}
function mulberry32(a){ return function(){ a|=0; a=a+0x6D2B79F5|0; let t=Math.imul(a^a>>>15,1|a); t=t+Math.imul(t^t>>>7,61|t)^t; return ((t^t>>>14)>>>0)/4294967296; }; }
function drawSample(list, seed){
  const rng = mulberry32(seed);
  const picks = [];
  const pool = list.length;
  if (!pool){ sample = null; return; }
  for (let i=0;i<Math.min(10,pool);i++){
    picks.push(pool === 1 ? 0 : Math.floor(rng()*pool));
  }
  const idx = [...new Set(picks)];
  while (idx.length < Math.min(10,pool)){
    const j = Math.floor(rng()*pool);
    if (!idx.includes(j)) idx.push(j);
  }
  sample = { seed, idx, verdicts:{} };
}
function renderChecks(list){
  const el = document.getElementById("panel-03");
  let h = '<h2 class="sec">How the app checks itself</h2>';
  // 1 record count
  const declared = Number(uhri.count);
  h += checkLine(N === declared, "Record count: rows in the file vs the declared count.", fmt(N)+" records vs declared "+fmt(declared)+".");
  // 2 partitions
  let ok = true, detail = [];
  ["mechanism","body","year"].forEach(f => {
    const m = {}; records.forEach(r => m[r[f]] = (m[r[f]]||0)+1);
    const s = Object.values(m).reduce((a,b)=>a+b,0);
    if (s !== N) ok = false;
    detail.push("per "+f+": "+fmt(s));
  });
  h += checkLine(ok, "Partitions: counts per mechanism, body and year each sum to the record count.", detail.join(" · ")+".");
  // 3 type partition
  const tm = {}; records.forEach(r => tm[r.type]=(tm[r.type]||0)+1);
  const ts = Object.values(tm).reduce((a,b)=>a+b,0);
  h += checkLine(ts === N, "Type partition: counts per type sum to the headline total.", Object.keys(tm).map(t=>fmt(tm[t])+" "+t).join(" · ")+".");
  // 4 chart vs table
  const stats = themeStats(list);
  const recomputed = {};
  list.forEach(r => r._themes.forEach(t => recomputed[t] = (recomputed[t]||0)+1));
  const chartOK = stats.slice(0,10).every(t => recomputed[t.theme] === t.n) && (stats.length===0 || stats[0].n <= list.length);
  h += checkLine(chartOK, "Chart against table: each FIG.01 bar equals a second, independent count of the same theme; the largest bar is not larger than the filtered count.", "top bar "+(stats[0]?stats[0].theme+" = "+stats[0].n:"none")+" vs "+fmt(list.length)+" filtered records.");
  // 5 links
  const badLinks = records.filter(r => {
    let u = r.doc_url || "";
    try { u = decodeURIComponent(u); } catch(e){}
    return !(u.startsWith("https://docs.un.org/") && u.toLowerCase().endsWith(r.symbol.toLowerCase()));
  });
  h += checkLine(badLinks.length === 0, "Links: every doc_url starts with https://docs.un.org/ and ends with its symbol.",
    badLinks.length ? badLinks.length+" fail: "+badLinks.slice(0,5).map(r=>esc(r.symbol)).join(", ")+(badLinks.length>5?" …":"") : "all "+fmt(N)+" pass.");
  // 6 paragraph numbers
  const perMech = {};
  records.forEach(r => { perMech[r.mechanism] = perMech[r.mechanism] || {t:0,p:0}; perMech[r.mechanism].t++; if (r._para) perMech[r.mechanism].p++; });
  const pdetail = Object.keys(perMech).map(m => m+": "+(100*perMech[m].p/perMech[m].t).toFixed(1)+"% ("+perMech[m].p+"/"+perMech[m].t+")").join(" · ");
  const uprPct = perMech["Universal Periodic Review"] ? 100*perMech["Universal Periodic Review"].p/perMech["Universal Periodic Review"].t : 100;
  h += checkLine(uprPct >= 100, "Paragraph numbers: share of records where a number was found at the start of the text, per mechanism. UPR is expected at 100%; a lower figure is a warning, not an error.", pdetail+".", uprPct < 100);
  // 7 states
  const uprRecs = records.filter(r=>r.mechanism==="Universal Periodic Review");
  const withState = uprRecs.filter(r=>r._states && r._states.some(s=>s!=="(State not found)"));
  const noState = uprRecs.filter(r=>!r._states || !r._states.some(s=>s!=="(State not found)"));
  h += checkLine(noState.length === 0, "States found: UPR records with at least one recommending State extracted, against all UPR records.",
    fmt(withState.length)+" of "+fmt(uprRecs.length)+" UPR records have a State"+(noState.length ? "; without one: "+noState.slice(0,6).map(r=>'<a href="'+esc(r.doc_url)+'" target="_blank" rel="noopener">'+esc(r.symbol)+'</a> para. '+esc(r._para||"—")).join(", ")+(noState.length>6?" …":"") : "")+".");
  // 8 duplicates and gaps
  const ids = distinct(records.map(r=>r.id));
  const texts = {}; let dupT = 0;
  records.forEach(r => { if (texts[r.text] !== undefined){ if (texts[r.text] === 0){ dupT++; texts[r.text] = 1; } } else texts[r.text] = 0; });
  const noTheme = records.filter(r=>!r._themes.length).length;
  const noSdg = records.filter(r=>!r._sdgs.length).length;
  const noAp = records.filter(r=>!r._ap.length).length;
  h += checkLine(ids.length === N, "Duplicates and gaps: distinct id equals the record count; duplicate texts and unlabelled records are counted, not hidden.",
    fmt(ids.length)+" distinct ids of "+fmt(N)+" · "+dupT+" duplicate text"+(dupT===1?"":"s")+" · not labelled: "+fmt(noTheme)+" no themes, "+fmt(noSdg)+" no SDGs, "+fmt(noAp)+" no affected persons.");
  // 9 random sample
  h += '<h2 class="sec">Random-sample label check</h2>'
     + '<p class="note" style="max-width:70ch;font-family:-apple-system,sans-serif;font-size:14px;letter-spacing:0">The UN’s theme labels are the weakest part of this data. Draw ten records from the current filter ('+fmt(list.length)+' records) and judge for yourself whether the labels fit the paragraph. This is your judgement of the UN’s labels; nothing is sent anywhere.</p>'
     + '<div style="display:flex;gap:10px;align-items:center;flex-wrap:wrap;margin:8px 0 14px">'
     + '<button class="btn" id="draw-btn">Check 10 at random</button>'
     + '<label class="fld" style="width:130px"><span class="hint">seed</span><input type="text" id="seed-input" value="1"></label>'
     + '<button class="btn" id="draw-seed-btn">Draw with this seed</button>'
     + '<span class="cnt" id="tally"></span></div><div id="sample-cards"></div>';
  el.innerHTML = h;
  const tallyEl = document.getElementById("tally");
  function updTally(){
    if (!sample) { tallyEl.textContent = ""; return; }
    const v = Object.values(sample.verdicts);
    const fit = v.filter(x=>x==="fit").length, no = v.filter(x=>x==="no").length, uns = v.filter(x=>x==="unsure").length;
    tallyEl.textContent = "Themes: "+fit+" fit, "+no+" don’t, "+uns+" unsure of "+v.length+" of "+sample.idx.length+" judged · seed "+sample.seed+" (your judgement, not the app’s)";
  }
  function renderCards(){
    const box = document.getElementById("sample-cards");
    if (!sample || !list.length){ box.innerHTML = '<p class="note">No records in the current filter.</p>'; updTally(); return; }
    box.innerHTML = sample.idx.map((i,k) => {
      const r = list[i];
      if (!r) return "";
      return '<div class="samplecard" data-k="'+k+'"><button aria-expanded="false">'
        + '<span class="mono" style="color:var(--accent)">CARD '+(k+1)+'</span>'
        + '<a href="'+esc(r.doc_url)+'" target="_blank" rel="noopener" onclick="event.stopPropagation()">'+esc(r.symbol)+'</a>'
        + '<span class="cnt">para. '+esc(r._para||"—")+' · '+esc(r.date)+'</span></button>'
        + '<div class="body" hidden><p class="fulltext">'+esc(r.text)+'</p>'
        + '<div class="labels">'+(r._themes.length ? r._themes.map(t=>'<span class="lchip">'+esc(t)+'</span>').join("") : '<span class="lchip">no themes (not labelled)</span>')+'</div>'
        + '<div class="verdicts" data-id="'+esc(r.id)+'">'
        + '<button class="btn v-btn" data-v="fit">Fits</button>'
        + '<button class="btn v-btn" data-v="no">Doesn’t fit</button>'
        + '<button class="btn v-btn" data-v="unsure">Unsure</button></div></div></div>';
    }).join("");
    box.querySelectorAll(".samplecard > button").forEach(b => {
      b.addEventListener("click", e => {
        if (e.target.closest("a")) return;
        const body = b.nextElementSibling;
        body.hidden = !body.hidden;
        b.setAttribute("aria-expanded", String(!body.hidden));
      });
    });
    box.querySelectorAll(".v-btn").forEach(vb => {
      vb.addEventListener("click", () => {
        const id = vb.closest(".verdicts").dataset.id;
        sample.verdicts[id] = vb.dataset.v;
        vb.closest(".verdicts").querySelectorAll(".v-btn").forEach(x=>x.classList.remove("sel"));
        vb.classList.add("sel");
        updTally();
      });
    });
    // open the first card
    const first = box.querySelector(".samplecard > button");
    if (first){ first.click(); }
    updTally();
  }
  document.getElementById("draw-btn").addEventListener("click", () => {
    const s = Math.floor(Math.random()*1e9);
    document.getElementById("seed-input").value = s;
    drawSample(list, s); renderCards();
  });
  document.getElementById("draw-seed-btn").addEventListener("click", () => {
    const s = parseInt(document.getElementById("seed-input").value, 10);
    drawSample(list, isNaN(s) ? 1 : s); renderCards();
  });
  if (sample) renderCards();
}

/* ---------- TAB 04 ---------- */
function renderMethod(list){
  const el = document.getElementById("panel-04");
  const stats = themeStats(list).slice(0,10);
  const docs = distinct(list.map(r=>r.symbol)).length;
  let h = '<h2 class="sec">How each number is computed</h2><div class="method">'
    + '<p>Every count is a loop over the records currently matching the filters — nothing is estimated and no model is called. The headline total is the number of matching records; the breakdown uses the UN’s own <em>type</em> values, spelled as in the data. Documents are distinct symbols; years are the minimum and maximum of <em>year</em>.</p>'
    + '<p>Filters combine with AND: exact match on mechanism, body and type, year between the two selects, SDG goal present in the record’s list, and every keyword word occurring as a literal substring of the text or symbol. Theme counts count each label once per record, so they sum to more than the record count; percentages are of records.</p>'
    + '<p>The paragraph number is the number at the start of the text (for example “71” or “144.43”); when there is none, the citation falls back to the symbol alone. The recommending State is extracted only from UPR records, from the parenthesised groups at the end of the text; the text itself is never altered.</p>'
    + '<p>Dates are the document’s date, not the date a recommendation was made or accepted. Keyword search is literal: “torture” does not find “ill-treatment”.</p>'
    + '</div>'
    + '<h2 class="sec">Take it with you</h2>'
    + '<p><button class="btn" id="csv-btn">Download CSV of the current filter</button> <span class="hint">'+fmt(list.length)+' rows · visible columns plus full text and labels · preceded by comment lines with country, source, filters and row count</span></p>'
    + '<p style="margin-top:14px"><button class="btn" id="sum-btn">Copy summary</button> <span class="hint">plain-text headline numbers and the ten themes, for pasting into notes</span></p>'
    + '<h2 class="sec">Source</h2>'
    + '<p class="method"><a href="'+esc(uhri.source_url)+'" target="_blank" rel="noopener">'+esc(uhri.source)+'</a> · '+esc(uhri.title||("Recommendations to "+country))+' · built '+esc(uhri.built)+' · '+fmt(N)+' records in the file, '+fmt(docs)+' documents in the current filter.</p>';
  el.innerHTML = h;
  document.getElementById("csv-btn").addEventListener("click", () => downloadCSV(list));
  document.getElementById("sum-btn").addEventListener("click", e => {
    const types = {}; list.forEach(r=>types[r.type]=(types[r.type]||0)+1);
    const years = list.map(r=>r.year);
    const txt = "UN human rights recommendations and observations: "+country+". "
      + fmt(list.length)+" records ("+Object.keys(types).map(t=>fmt(types[t])+" "+t).join(", ")+") from "+fmt(docs)+" documents"
      + (years.length ? ", "+Math.min(...years)+"–"+Math.max(...years)+"." : ".")
      + " Ten most frequent themes: "+stats.map(t=>t.theme+" ("+t.n+")").join("; ")+"."
      + " Source: "+uhri.source+", extracted "+uhri.built+". Counts computed in the UHRI dashboard; a record can carry several themes.";
    copyText(txt, e.target);
  });
}
function csvEscape(v){
  v = String(v ?? "");
  return /[",\n]/.test(v) ? '"' + v.replace(/"/g,'""') + '"' : v;
}
function downloadCSV(list){
  const lines = [];
  lines.push("# UN human rights recommendations and observations: " + country);
  lines.push("# Source: " + uhri.source + " <" + uhri.source_url + ">");
  lines.push("# Built: " + uhri.built);
  const fl = [];
  if (filt.kw) fl.push('keyword="'+filt.kw+'"');
  if (filt.mechanism) fl.push("mechanism="+filt.mechanism);
  if (filt.body) fl.push("body="+filt.body);
  if (filt.type) fl.push("type="+filt.type);
  if (filt.state) fl.push("state="+filt.state);
  if (filt.yFrom||filt.yTo) fl.push("years="+(filt.yFrom||"…")+"–"+(filt.yTo||"…"));
  if (filt.sdg) fl.push("sdg="+filt.sdg);
  if (filt.themes.size) fl.push("themes="+[...filt.themes].join(" | "));
  lines.push("# Filters applied: " + (fl.length ? fl.join("; ") : "none"));
  lines.push("# Rows: " + list.length);
  lines.push(["date","body","mechanism","type","symbol","doc_url","paragraph","recommending_states","first_line","themes","sdgs","sdg_targets","affected_persons","section","full_text"].join(","));
  sortedRows(list).forEach(r => {
    lines.push([
      r.date, r.body, r.mechanism, r.type, r.symbol, r.doc_url, r._para||"",
      (r._states ? r._states.filter(s=>s!=="(State not found)").join(" | ") : ""),
      firstLine(r.text), r._themes.join(" | "), r._sdgs.join(" | "), r._targets.join(" | "),
      r._ap.join(" | "), r.section||"", r.text
    ].map(csvEscape).join(","));
  });
  const blob = new Blob([lines.join("\r\n")], {type:"text/csv;charset=utf-8"});
  const a = document.createElement("a");
  a.href = URL.createObjectURL(blob);
  a.download = "uhri-" + country.toLowerCase().replace(/\s+/g,"-") + "-filtered.csv";
  document.body.appendChild(a); a.click();
  setTimeout(()=>{ URL.revokeObjectURL(a.href); a.remove(); }, 500);
}

/* ---------- render ---------- */
function render(){
  const list = filtered();
  // rail
  document.getElementById("match-n").textContent = fmt(list.length);
  const share = N ? Math.min(100, 100*list.length/N) : 0;
  document.getElementById("sharebar-fill").style.width = share.toFixed(1)+"%";
  document.getElementById("sharebar-note").textContent = share.toFixed(1)+"% of the file";
  document.getElementById("chips").innerHTML = chipsHTML();
  document.getElementById("chips").querySelectorAll("button[data-chip]").forEach(b => {
    b.addEventListener("click", () => {
      const k = b.dataset.chip;
      if (k === "kw") filt.kw = "";
      else if (k === "years"){ filt.yFrom = ""; filt.yTo = ""; }
      else if (k.startsWith("theme:")) filt.themes.delete(k.slice(6));
      else filt[k] = "";
      shown = 50; render();
    });
  });
  document.getElementById("clear-all").hidden = activeFilterCount() === 0;
  const rf = document.getElementById("rail-filters");
  if (tab === "01" || tab === "02"){
    if (!rf.innerHTML || rf.dataset.tab !== "full"){ rf.dataset.tab = "full"; rf.innerHTML = railHTML(); }
    else {
      // refresh selects in place without losing focus
      rf.innerHTML = railHTML();
    }
    wireRail();
  } else {
    rf.dataset.tab = "short"; rf.innerHTML = "";
  }
  document.getElementById("clear-all").onclick = () => {
    filt = { kw:"", mechanism:"", body:"", type:"", state:"", yFrom:"", yTo:"", sdg:"", themes:new Set() };
    shown = 50; render();
  };
  if (tab === "01") renderOverview(list);
  else if (tab === "02") renderRecords(list);
  else if (tab === "03") renderChecks(list);
  else renderMethod(list);
}
render();
</script>
</body>
</html>
```

Open the file, and the four tabs work straight away: 01 gives the at-a-glance tiles, the ranked theme chart (click a bar to filter) and the per-year timeline; 02 lists the paragraphs with expandable full text, UPR recommending States and copy-ready citations; 03 runs the self-checks and the seeded random-sample label check; 04 explains the method and exports a commented CSV or a copy-paste summary. All numbers are computed live from your file, so if the counts differ from the plan's, the app is right.