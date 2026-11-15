This app opens on the first article in the file and lists every drafting stage in date order, with added words in <ins> and removed words in <del>, and the votes taken since the stage before. The Overview tab ranks the stages by how much of the text changed. Punctuation, capitals and line-end hyphens are ignored when comparing, as you asked.

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>How a Covenant article changed</title>
<style>
:root{--paper:#f4f0e8;--ink:#1d1b18;--rule:#d9d2c3;--accent:#9b2335;--muted:#5b564c;--ins-bg:#d9ead3;--ins-fg:#1f4d2b;--del-bg:#f3dcd7;--del-fg:#7a1d2b}
*{box-sizing:border-box}
[hidden]{display:none!important}
html{background:var(--paper)}
body{margin:0;background:var(--paper);color:var(--ink);font:16px/1.55 system-ui,-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
.wrap{max-width:1080px;margin:0 auto;padding:20px 24px 48px}
.mono{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:12px;letter-spacing:.08em;text-transform:uppercase}
.muted{color:var(--muted)}
.serif{font-family:Georgia,"Times New Roman",serif}
a{color:var(--accent)}
:focus-visible{outline:3px solid var(--accent);outline-offset:2px}
header{border-bottom:1px solid var(--rule);padding-bottom:14px}
header .top{display:flex;justify-content:space-between;align-items:flex-end;gap:16px;flex-wrap:wrap}
h1{font:400 34px/1.15 Georgia,"Times New Roman",serif;margin:6px 0 6px}
.picker{display:flex;flex-direction:column;gap:4px}
select{font:16px system-ui,sans-serif;color:var(--ink);background:var(--paper);border:1px solid var(--ink);padding:8px 10px;min-width:260px;border-radius:0}
.meta{margin:0;color:var(--muted);font-size:14px}
[role=tablist]{display:flex;gap:4px;flex-wrap:wrap;border-bottom:1px solid var(--rule);margin:16px 0 22px}
[role=tab]{background:none;border:0;border-bottom:3px solid transparent;padding:10px 14px;cursor:pointer;color:var(--ink);font-family:ui-monospace,Menlo,Consolas,monospace;font-size:12px;letter-spacing:.08em;text-transform:uppercase}
[role=tab][aria-selected=true]{color:var(--accent);border-bottom-color:var(--accent);font-weight:700}
.bigs{display:flex;gap:40px;flex-wrap:wrap;margin:6px 0 10px}
.big .n{font:400 52px/1 Georgia,"Times New Roman",serif}
.big .l{display:block;margin-top:6px}
h2{font:400 22px/1.25 Georgia,"Times New Roman",serif;margin:26px 0 4px}
.how{margin:4px 0 14px;color:var(--muted);font-size:14px}
.bars{list-style:none;margin:0;padding:0}
.bars li{border-top:1px solid var(--rule)}
.bars li:last-child{border-bottom:1px solid var(--rule)}
.bar{display:grid;grid-template-columns:minmax(150px,280px) 1fr 140px;gap:14px;align-items:center;width:100%;background:none;border:0;padding:10px 4px;text-align:left;cursor:pointer;color:var(--ink);font:inherit}
.bar:hover{background:#ece6d8}
.bar .lab b{display:block;font-weight:600}
.track{height:16px;background:transparent}
.fill{height:100%;background:var(--accent);min-width:2px}
.bar .val{text-align:right;font-family:Georgia,serif;font-size:20px}
.bar .val small{display:block;font:12px ui-monospace,Menlo,Consolas,monospace;color:var(--muted)}
.stage{border-top:2px solid var(--ink);padding:14px 0 18px;margin-top:22px;scroll-margin-top:12px}
.stage:focus{outline:none}
.stage h3{font:400 22px/1.25 Georgia,"Times New Roman",serif;margin:4px 0 6px}
.chips{display:flex;gap:8px;flex-wrap:wrap;margin:6px 0 12px}
.chip{border:1px solid var(--rule);padding:2px 8px;font:12px ui-monospace,Menlo,Consolas,monospace;letter-spacing:.04em}
.chip.hot{border-color:var(--accent);color:var(--accent)}
.diff{font-size:17px;line-height:1.75;margin:0 0 12px;max-width:78ch}
ins{background:var(--ins-bg);color:var(--ins-fg);text-decoration:underline;text-decoration-thickness:1px;padding:0 2px}
del{background:var(--del-bg);color:var(--del-fg);text-decoration:line-through;padding:0 2px}
.legend{display:flex;gap:18px;flex-wrap:wrap;align-items:center;margin:0 0 6px}
details{border-top:1px solid var(--rule);padding:8px 0}
summary{cursor:pointer}
details pre{white-space:pre-wrap;font:14px/1.5 ui-monospace,Menlo,Consolas,monospace;margin:8px 0 0;max-width:90ch}
table{border-collapse:collapse;width:100%;margin:8px 0 4px;font-size:15px}
caption{text-align:left;padding:4px 0 6px;color:var(--muted)}
th,td{padding:7px 8px;border-top:1px solid var(--rule);vertical-align:top;text-align:left}
th{font:11px ui-monospace,Menlo,Consolas,monospace;letter-spacing:.08em;text-transform:uppercase;color:var(--muted);font-weight:400}
td.num,th.num{text-align:right;white-space:nowrap}
.res-adopted{font-weight:700}
.checks{list-style:none;padding:0;margin:0}
.checks li{display:grid;grid-template-columns:70px 1fr;gap:12px;border-top:1px solid var(--rule);padding:10px 0}
.checks li:last-child{border-bottom:1px solid var(--rule)}
.st-ok{color:#1f4d2b}.st-warn{color:var(--accent);font-weight:700}
.words{display:flex;flex-wrap:wrap;gap:6px;margin-top:6px}
button.act{background:var(--ink);color:var(--paper);border:0;padding:9px 16px;cursor:pointer;font:12px ui-monospace,Menlo,Consolas,monospace;letter-spacing:.08em;text-transform:uppercase}
textarea{width:100%;height:160px;font:12px/1.4 ui-monospace,Menlo,Consolas,monospace;background:#fbf9f4;border:1px solid var(--rule);color:var(--ink);margin-top:10px;padding:8px}
ul.plain{margin:6px 0;padding-left:20px}
.empty{padding:24px 0;color:var(--muted)}
@media (max-width:720px){.bar{grid-template-columns:1fr;gap:6px}.bar .val{text-align:left}h1{font-size:28px}}
</style>
</head>
<body>
<div class="wrap">
<header>
  <div class="mono muted" id="dataLabel">WORKSHOP_DATA.drafts</div>
  <div class="top">
    <h1>How a Covenant article changed while it was drafted</h1>
    <div class="picker">
      <label class="mono muted" for="artSel">Article <span style="text-transform:none;letter-spacing:0">(pick one)</span></label>
      <select id="artSel"></select>
    </div>
  </div>
  <p class="meta" id="metaLine"></p>
</header>

<div role="tablist" aria-label="Views" id="tabs">
  <button role="tab" id="tab-0" aria-controls="panel-0" aria-selected="true" tabindex="0">01 Overview</button>
  <button role="tab" id="tab-1" aria-controls="panel-1" aria-selected="false" tabindex="-1">02 Stages</button>
  <button role="tab" id="tab-2" aria-controls="panel-2" aria-selected="false" tabindex="-1">03 Can I trust this</button>
  <button role="tab" id="tab-3" aria-controls="panel-3" aria-selected="false" tabindex="-1">04 Method &amp; export</button>
</div>

<section role="tabpanel" id="panel-0" aria-labelledby="tab-0"></section>
<section role="tabpanel" id="panel-1" aria-labelledby="tab-1" hidden></section>
<section role="tabpanel" id="panel-2" aria-labelledby="tab-2" hidden></section>
<section role="tabpanel" id="panel-3" aria-labelledby="tab-3" hidden></section>
</div>

<script>
(function(){
"use strict";
var DATA = (window.WORKSHOP_DATA && window.WORKSHOP_DATA.drafts) || {};
var articles = Array.isArray(DATA.records) ? DATA.records : [];
var MONTHS = {jan:0,feb:1,mar:2,apr:3,may:4,jun:5,jul:6,aug:7,sep:8,oct:9,nov:10,dec:11};
var state = {art:0, tab:0};
var cache = {};
var $ = function(id){return document.getElementById(id);};

function esc(s){return String(s==null?"":s).replace(/[&<>"']/g,function(c){return {"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c];});}

/* ---------- dates ---------- */
function stageEnd(s){
  s = String(s||"").trim();
  var m = s.match(/^(\d{1,2})\s+([A-Za-z]+)\s+(\d{4})$/);
  if(m && MONTHS[m[2].slice(0,3).toLowerCase()] !== undefined) return Date.UTC(+m[3], MONTHS[m[2].slice(0,3).toLowerCase()], +m[1]);
  m = s.match(/^([A-Za-z]+)\s+(\d{4})$/);
  if(m && MONTHS[m[1].slice(0,3).toLowerCase()] !== undefined) return Date.UTC(+m[2], MONTHS[m[1].slice(0,3).toLowerCase()]+1, 0); /* last day of that month */
  return null;
}
function voteTime(s){
  var m = String(s||"").match(/^(\d{4})-(\d{2})-(\d{2})/);
  return m ? Date.UTC(+m[1], +m[2]-1, +m[3]) : null;
}
function yearOf(ms){return new Date(ms).getUTCFullYear();}

/* ---------- words and diff ---------- */
function keyOf(w){return w.toLowerCase().normalize("NFD").replace(/[^\p{L}\p{N}]/gu,"");}
function words(text){
  var t = String(text||"").replace(/(\p{L})-\s+(\p{L})/gu,"$1$2"); /* join words broken at a line end */
  return t.split(/\s+/).map(function(w){return {show:w, key:keyOf(w)};}).filter(function(w){return w.key;});
}
function diff(a,b){
  var n=a.length, m=b.length, ops=[], i, j;
  if((n+1)*(m+1) > 8000000){
    a.forEach(function(x){ops.push({t:"del",w:x.show});});
    b.forEach(function(x){ops.push({t:"ins",w:x.show});});
    return {ops:ops,lcs:0,approx:true};
  }
  var w=m+1, L=new Uint16Array((n+1)*(m+1));
  for(i=n-1;i>=0;i--) for(j=m-1;j>=0;j--)
    L[i*w+j] = a[i].key===b[j].key ? L[(i+1)*w+j+1]+1 : Math.max(L[(i+1)*w+j], L[i*w+j+1]);
  var dels=[], inss=[];
  function flush(){
    dels.forEach(function(x){ops.push({t:"del",w:x.show});});
    inss.forEach(function(x){ops.push({t:"ins",w:x.show});});
    dels=[]; inss=[];
  }
  i=0; j=0;
  while(i<n && j<m){
    if(a[i].key===b[j].key){flush(); ops.push({t:"eq",w:b[j].show}); i++; j++;}
    else if(L[(i+1)*w+j] >= L[i*w+j+1]){dels.push(a[i]); i++;}
    else {inss.push(b[j]); j++;}
  }
  while(i<n) dels.push(a[i++]);
  while(j<m) inss.push(b[j++]);
  flush();
  return {ops:ops, lcs:L[0], approx:false};
}
function opsHtml(ops){
  var out=[], cur=null, buf=[];
  function close(){
    if(!buf.length) return;
    var s = buf.map(esc).join(" ");
    out.push(cur==="ins" ? "<ins>"+s+"</ins>" : cur==="del" ? "<del>"+s+"</del>" : s);
    buf=[];
  }
  ops.forEach(function(o){ if(o.t!==cur){close(); cur=o.t;} buf.push(o.w); });
  close();
  return out.join(" ");
}
function plainHtml(ws){return ws.map(function(x){return esc(x.show);}).join(" ");}

/* ---------- analysis of one article ---------- */
function analyse(idx){
  if(cache[idx]) return cache[idx];
  var rec = articles[idx] || {};
  var raw = Array.isArray(rec.stages) ? rec.stages : [];
  var prevEnd = 0;
  var stages = raw.map(function(s,k){
    var e = stageEnd(s.date), undated = (e===null);
    if(undated) e = prevEnd; else prevEnd = e;
    return {orig:k, s:s, end:e, undated:undated, ws:words(s.text)};
  });
  var wasSorted = stages.every(function(x,k){return k===0 || stages[k-1].end <= x.end;});
  stages.sort(function(a,b){return a.end-b.end || a.orig-b.orig;});
  var votes = (Array.isArray(rec.votes) ? rec.votes : []).map(function(v){return {v:v, t:voteTime(v.date)};});
  var assigned = {}, unassigned = [];
  votes.forEach(function(x){
    if(x.t===null){unassigned.push({x:x,why:"no usable date"});return;}
    var placed=false;
    for(var i=0;i<stages.length;i++){
      var lo = i===0 ? -Infinity : stages[i-1].end;
      if(x.t > lo && x.t <= stages[i].end){(assigned[i]=assigned[i]||[]).push(x); placed=true; break;}
    }
    if(!placed) unassigned.push({x:x,why:"after the last stage"});
  });
  stages.forEach(function(st,i){
    st.no = i+1;
    st.votes = (assigned[i]||[]).sort(function(a,b){return a.t-b.t || String(a.v.meeting).localeCompare(String(b.v.meeting));}).map(function(x){return x.v;});
    if(i===0){
      st.prev=null; st.added=null; st.removed=null; st.share=null; st.html=plainHtml(st.ws);
    } else {
      var d = diff(stages[i-1].ws, st.ws), a=stages[i-1].ws.length, b=st.ws.length;
      st.prev = stages[i-1];
      st.added = b - d.lcs; st.removed = a - d.lcs;
      st.share = (a+b)>0 ? (st.added+st.removed)/(a+b) : 0;
      st.html = opsHtml(d.ops); st.approx = d.approx;
    }
  });
  var kept = null;
  if(stages.length>1){
    var dk = diff(stages[0].ws, stages[stages.length-1].ws);
    kept = {lcs:dk.lcs, of:stages[stages.length-1].ws.length};
  }
  var r = {rec:rec, stages:stages, wasSorted:wasSorted, unassigned:unassigned, totalVotes:votes.length, kept:kept};
  cache[idx]=r; return r;
}

/* ---------- helpers for display ---------- */
function pct(x){return Math.round(x*100)+"%";}
function link(sym){
  if(!sym) return '<span class="muted">no symbol</span>';
  return '<a href="'+esc(encodeURI("https://docs.un.org/en/"+sym))+'" target="_blank" rel="noopener">'+esc(sym)+'</a>';
}
function yearsRange(){
  var ys=[];
  articles.forEach(function(a){
    (a.stages||[]).forEach(function(s){var e=stageEnd(s.date); if(e!==null) ys.push(yearOf(e));});
    (a.votes||[]).forEach(function(v){var t=voteTime(v.date); if(t!==null) ys.push(yearOf(t));});
  });
  return ys.length ? Math.min.apply(null,ys)+"–"+Math.max.apply(null,ys) : "years not available";
}
function artName(a){return "Article "+esc(a.article)+" · "+esc(a.title||"");}

/* ---------- rendering ---------- */
function renderHeader(){
  $("dataLabel").textContent = "WORKSHOP_DATA.drafts · " + (DATA.title || "Drafts of ICCPR articles");
  var sel = $("artSel");
  sel.innerHTML = articles.map(function(a,i){return '<option value="'+i+'">Article '+esc(a.article)+' · '+esc(a.title||"")+'</option>';}).join("");
  sel.value = String(state.art);
  var r = articles.length ? analyse(state.art) : null;
  $("metaLine").textContent = "Source: " + (DATA.source || "not stated in the file") + " · n = " + articles.length + " articles in the file · years " + yearsRange() +
    (r ? " · this article: " + r.stages.length + " stages, " + r.totalVotes + " recorded votes" : "");
}

function renderOverview(r){
  var p = $("panel-0");
  if(!r.stages.length){p.innerHTML='<p class="empty">This article has no drafting stages in the file.</p>';return;}
  var ch = r.stages.filter(function(s){return s.share!==null;});
  var top = ch.slice().sort(function(a,b){return b.share-a.share || (b.added+b.removed)-(a.added+a.removed);})[0];
  var votesIn = r.stages.reduce(function(n,s){return n+s.votes.length;},0);
  var h = '<div class="bigs">';
  h += '<div class="big"><span class="n">'+r.stages.length+'</span><span class="l mono muted">stages, '+esc(r.stages[0].s.date)+' to '+esc(r.stages[r.stages.length-1].s.date)+'</span></div>';
  h += '<div class="big"><span class="n">'+votesIn+'</span><span class="l mono muted">votes between stages</span></div>';
  if(top) h += '<div class="big"><span class="n">'+pct(top.share)+'</span><span class="l mono muted">most changed: stage '+String(top.no).padStart(2,"0")+' · '+esc(top.s.date)+'</span></div>';
  h += '</div>';
  if(top) h += '<p class="how">Biggest rewrite: stage '+top.no+' ('+esc(top.s.symbol||"no symbol")+', '+esc(top.s.date)+') changed '+pct(top.share)+' of the words it shares with the stage before: '+top.added+' added, '+top.removed+' removed.</p>';
  if(r.kept) h += '<p class="how">Words of the adopted text that already stood, in the same order, in the first draft: '+r.kept.lcs+' of '+r.kept.of+' ('+pct(r.kept.of? r.kept.lcs/r.kept.of:0)+').</p>';
  h += '<h2>Which stages changed the text most</h2>';
  h += '<div class="mono muted">FIG.01 · ranked · click = go to that stage</div>';
  if(!ch.length){
    h += '<p class="empty">There is only one stage, so there is nothing to compare.</p>';
  } else {
    var ranked = ch.slice().sort(function(a,b){return b.share-a.share || (b.added+b.removed)-(a.added+a.removed);});
    var max = ranked[0].share || 1;
    h += '<ol class="bars" style="padding:0">';
    ranked.forEach(function(s){
      h += '<li><button class="bar" data-go="'+(s.no-1)+'" aria-label="Go to stage '+s.no+'">'+
        '<span class="lab"><b>'+String(s.no).padStart(2,"0")+' · '+esc(s.s.date)+'</b><span class="muted">'+esc(s.s.symbol||"no symbol")+'</span></span>'+
        '<span class="track"><span class="fill" style="display:block;width:'+Math.max(1,(s.share/max)*100)+'%"></span></span>'+
        '<span class="val">'+pct(s.share)+'<small>+'+s.added+' / −'+s.removed+' words</small></span></button></li>';
    });
    h += '</ol>';
  }
  h += '<p class="how">How this is computed: each stage is compared word by word with the stage before (punctuation, capitals and line-end hyphens ignored); share = (added + removed words) ÷ (words in both stages). The first stage has nothing before it, so it is not ranked. Exact counting, not an estimate.</p>';
  p.innerHTML = h;
}

function voteTable(st){
  if(!st.votes.length) return '<p class="muted" style="margin:6px 0">No recorded vote on this article '+(st.no===1?'up to this stage':'since the stage before')+'.</p>';
  var h = '<table><caption>Votes taken '+(st.no===1?'up to this stage':'since the previous stage')+' ('+st.votes.length+')</caption><thead><tr>'+
    '<th scope="col">Date</th><th scope="col">Meeting</th><th scope="col">Voted on</th><th scope="col">Result</th><th scope="col" class="num">Yes–No–Abst.</th><th scope="col">Proposed by</th></tr></thead><tbody>';
  st.votes.forEach(function(v){
    var nums = [v.yes,v.no,v.abstentions];
    var figs = nums.every(function(x){return x==null;}) ? '<span class="muted">not recorded</span>' : nums.map(function(x){return x==null?"–":x;}).join("–");
    var prop = Array.isArray(v.proposers)&&v.proposers.length ? v.proposers.map(esc).join(", ") : '<span class="muted">not stated</span>';
    h += '<tr><td>'+esc(v.date||"no date")+'</td><td>'+link(v.meeting)+'</td><td>'+esc(v.subject||"not stated")+'</td>'+
      '<td class="res-'+esc(String(v.outcome||"").toLowerCase())+'">'+esc(v.outcome||"not stated")+'</td><td class="num">'+figs+'</td><td>'+prop+'</td></tr>';
  });
  return h+'</tbody></table>';
}

function renderStages(r){
  var p = $("panel-1");
  if(!r.stages.length){p.innerHTML='<p class="empty">This article has no drafting stages in the file.</p>';return;}
  var top = null;
  r.stages.forEach(function(s){ if(s.share!==null && (!top || s.share>top.share)) top=s; });
  var h = '<div class="legend"><span class="mono muted">LEGEND</span><span><ins>added word</ins></span><span><del>removed word</del></span><span>plain = kept</span>'+
    '<span class="mono muted">punctuation, capitals and line-end hyphens ignored</span></div>';
  r.stages.forEach(function(st){
    h += '<article class="stage" id="stage-'+(st.no-1)+'" tabindex="-1">';
    h += '<div class="mono muted">Stage '+String(st.no).padStart(2,"0")+' of '+r.stages.length+' · '+esc(st.s.date||"no date")+(st.undated?' (date not readable)':'')+'</div>';
    h += '<h3>'+esc(st.s.stage||"Untitled stage")+'</h3>';
    h += '<div class="chips"><span class="chip">'+link(st.s.symbol)+'</span>'+
      (st.s.draft_article!=null?'<span class="chip">draft art. '+esc(st.s.draft_article)+'</span>':'')+
      (st.s.page!=null?'<span class="chip">p. '+esc(st.s.page)+'</span>':'');
    if(st.share===null) h += '<span class="chip">first draft: nothing to compare</span>';
    else h += '<span class="chip'+(st===top?' hot':'')+'">'+pct(st.share)+' changed · +'+st.added+' / −'+st.removed+' words'+(st===top?' · most changed':'')+'</span>';
    h += '</div>';
    if(!st.ws.length) h += '<p class="muted">No text for this stage in the file.</p>';
    else {
      if(st.share!==null) h += '<div class="mono muted" style="margin-bottom:4px">What changed since stage '+String(st.prev.no).padStart(2,"0")+' ('+esc(st.prev.s.date||"")+')'+(st.approx?' · text too long to align, shown as all removed + all added':'')+'</div>';
      h += '<p class="diff">'+st.html+'</p>';
    }
    h += voteTable(st);
    h += '<details><summary class="mono muted">Draft text exactly as OCR read it</summary><pre>'+esc(st.s.text||"")+'</pre></details>';
    h += '</article>';
  });
  p.innerHTML = h;
}

function renderChecks(r){
  var p = $("panel-2");
  if(!r.stages.length){p.innerHTML='<p class="empty">Nothing to check: no stages.</p>';return;}
  var items=[], st=r.stages;
  items.push({ok:r.wasSorted, t: r.wasSorted ? "Stages were already in date order in the file." : "Stages were not in date order in the file; the app re-sorted them by date."});
  var und = st.filter(function(s){return s.undated;}).length;
  items.push({ok:!und, t: und ? und+" stage(s) have a date the app could not read; they stay next to their neighbours." : "All "+st.length+" stage dates were read (a month alone counts as the last day of that month)."});
  var last = st[st.length-1];
  var adopted = /2200/.test(String(last.s.symbol||"")) || /adopt|covenant as/i.test(String(last.s.stage||""));
  items.push({ok:adopted, t: adopted ? "The last stage is the adopted Covenant text ("+esc(last.s.symbol||"")+")." : "The last stage does not look like the adopted text: check "+esc(last.s.symbol||"no symbol")+"."});
  var empty = st.filter(function(s){return !s.ws.length;}).length;
  items.push({ok:!empty, t: empty ? empty+" stage(s) have no text." : "Every stage has text."});
  var vIn = st.reduce(function(n,s){return n+s.votes.length;},0);
  items.push({ok:r.unassigned.length===0, t: vIn+" of "+r.totalVotes+" votes were placed between stages."+(r.unassigned.length ? " Not placed: "+r.unassigned.map(function(u){return esc(u.x.v.meeting||"?")+" ("+esc(u.x.v.date||"no date")+", "+u.why+")";}).join("; ")+".":"")});
  var noFig = 0; st.forEach(function(s){s.votes.forEach(function(v){ if(v.yes==null&&v.no==null&&v.abstentions==null) noFig++; });});
  items.push({ok:!noFig, t: noFig ? noFig+" vote(s) have no recorded figures; they are shown as “not recorded”, not as zero." : "Every placed vote has figures."});
  var sameDate = st.filter(function(s,i){return i>0 && s.end===st[i-1].end;}).length;
  items.push({ok:!sameDate, t: sameDate ? sameDate+" stage(s) share a date with the stage before; votes of that month are placed with the earlier stage." : "No two stages share a date."});
  /* suspicious words */
  var sus=[], seen={};
  st.forEach(function(s){ s.ws.forEach(function(w){
    if(/\p{Ll}\p{Lu}|\p{L}\d|\d\p{L}/u.test(w.show.replace(/^[^\p{L}\p{N}]+|[^\p{L}\p{N}]+$/gu,"")) && !seen[w.key+s.no]){seen[w.key+s.no]=1; sus.push({w:w.show,no:s.no});}
  });});
  var h = '<h2>The app’s own checks</h2><div class="mono muted">FIG.02 · deterministic checks on this article</div><ul class="checks">';
  items.forEach(function(i){h += '<li><span class="mono '+(i.ok?'st-ok':'st-warn')+'">'+(i.ok?'OK':'CHECK')+'</span><span>'+i.t+'</span></li>';});
  h += '<li><span class="mono '+(sus.length?'st-warn':'st-ok')+'">'+(sus.length?'CHECK':'OK')+'</span><span>Words with capitals or digits inside them, a typical sign of OCR misreads: '+(sus.length?sus.length+' found. They are counted as real changes below because the app cannot know the intended word.':'none found.')+
    (sus.length?'<span class="words">'+sus.slice(0,40).map(function(x){return '<span class="chip">'+esc(x.w)+' · stage '+x.no+'</span>';}).join("")+(sus.length>40?'<span class="chip">+'+(sus.length-40)+' more</span>':'')+'</span>':'')+'</span></li>';
  h += '</ul>';
  h += '<h2>What these checks cannot tell you</h2><ul class="plain"><li>A misread letter (for example a capital I read as l) shows up as one word removed and one added, even when the drafters changed nothing.</li><li>A few drafts carry footnote text; the app cannot tell footnotes from the article, so they count as words.</li><li>Votes are placed by date only; a vote in the same month as a stage is placed with that stage, because the stage’s text is dated by month.</li></ul>';
  p.innerHTML = h;
}

function csvCell(x){x=String(x==null?"":x); return /[",\n]/.test(x)?'"'+x.replace(/"/g,'""')+'"':x;}
function buildCsv(r){
  var rows=[["article","stage_no","date","symbol","words_before","words_this","added","removed","percent_changed","votes_since_previous_stage"]];
  r.stages.forEach(function(s,i){
    rows.push([r.rec.article,s.no,s.s.date,s.s.symbol,i?r.stages[i-1].ws.length:"",s.ws.length,s.added==null?"":s.added,s.removed==null?"":s.removed,s.share==null?"":Math.round(s.share*1000)/10,s.votes.length]);
  });
  return rows.map(function(row){return row.map(csvCell).join(",");}).join("\n");
}
function renderMethod(r){
  var p = $("panel-3");
  var h = '<h2>How the comparison is made</h2><ul class="plain">'+
    '<li><b>Order.</b> Stages are sorted by date. A month alone (“June 1952”) counts as the last day of that month.</li>'+
    '<li><b>Words.</b> Each draft is split into words. Words broken at a line end (“restric- tions”) are joined first. Two words are the same when they match after lower-casing and removing punctuation.</li>'+
    '<li><b>Changes.</b> The longest run of words the two drafts share, in order, is kept; every other word of the older draft is removed (<del>del</del>) and every other word of the newer one is added (<ins>ins</ins>).</li>'+
    '<li><b>Share changed.</b> (added + removed) ÷ (words in the older draft + words in the newer draft).</li>'+
    '<li><b>Votes.</b> A vote belongs to the first stage dated on or after it, and after the stage before. Votes after the last stage are listed on the checks tab.</li>'+
    '<li><b>Links.</b> The file has no document URLs for drafts or meetings; links are built from the symbol (docs.un.org) and may not open every record.</li></ul>';
  h += '<h2>Export</h2><div class="mono muted">FIG.03 · one row per stage of this article</div><p style="margin:10px 0"><button class="act" id="dl">Download CSV</button></p><textarea id="csv" readonly aria-label="CSV of stage changes">'+esc(buildCsv(r))+'</textarea>';
  p.innerHTML = h;
  $("dl").onclick = function(){
    try{
      var blob = new Blob([$("csv").value], {type:"text/csv"});
      var a = document.createElement("a");
      a.href = URL.createObjectURL(blob); a.download = "iccpr-article-"+r.rec.article+"-stages.csv";
      document.body.appendChild(a); a.click(); a.remove();
    }catch(e){ $("csv").focus(); $("csv").select(); }
  };
}

function renderAll(){
  if(!articles.length){
    ["panel-0","panel-1","panel-2","panel-3"].forEach(function(id){$(id).innerHTML='<p class="empty">No articles found in WORKSHOP_DATA.drafts. Attach the drafts file and reload.</p>';});
    $("metaLine").textContent="No data."; return;
  }
  renderHeader();
  var r = analyse(state.art);
  renderOverview(r); renderStages(r); renderChecks(r); renderMethod(r);
}

/* ---------- tabs ---------- */
function setTab(i, focus){
  state.tab = i;
  for(var k=0;k<4;k++){
    var t=$("tab-"+k), on=(k===i);
    t.setAttribute("aria-selected", on?"true":"false"); t.tabIndex = on?0:-1;
    $("panel-"+k).hidden = !on;
  }
  if(focus) $("tab-"+i).focus();
}
$("tabs").addEventListener("click", function(e){
  var t = e.target.closest("[role=tab]"); if(t) setTab(+t.id.split("-")[1]);
});
$("tabs").addEventListener("keydown", function(e){
  var i = state.tab, n=4, j=null;
  if(e.key==="ArrowRight") j=(i+1)%n;
  else if(e.key==="ArrowLeft") j=(i+n-1)%n;
  else if(e.key==="Home") j=0;
  else if(e.key==="End") j=n-1;
  if(j!==null){e.preventDefault(); setTab(j,true);}
});
$("panel-0").addEventListener("click", function(e){
  var b = e.target.closest("[data-go]"); if(!b) return;
  setTab(1);
  var el = $("stage-"+b.getAttribute("data-go"));
  if(el){el.scrollIntoView(); el.focus();}
});
$("artSel").addEventListener("change", function(e){
  state.art = +e.target.value; renderAll();
});

renderAll();
setTab(0);
})();
</script>
</body>
</html>
```
