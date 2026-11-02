I built a two-State vote comparator for the Human Rights Council dataset: pick any two States that appear in at least one roll call, see how many recorded votes they share and how often they agree, a stacked year-by-year chart with a counts table, a filter for resolutions/amendments/both, and a list of every vote where they differed (symbol linked to the UN document, both votes shown, plus a ⚠ warning whenever the official totals don't match the roll call).

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Comparing two States' votes at the Human Rights Council</title>
<style>
:root{
  --accent:#1f6fb2; --accent-dark:#175a91;
  --ink:#1d2733; --muted:#5c6b7a; --bg:#f4f6f9; --line:#dce3ec;
  --warn-bg:#fdf4e3; --warn-line:#e6c37c; --warn-ink:#7a5a10;
}
*{box-sizing:border-box}
html,body{margin:0;padding:0}
body{background:var(--bg);color:var(--ink);font:16px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif}
.wrap{max-width:1040px;margin:0 auto;padding:0 20px}
header.top{background:#fff;border-bottom:1px solid var(--line);padding:20px 0 18px}
.kicker{color:var(--accent);font-size:.78rem;font-weight:700;letter-spacing:.1em;text-transform:uppercase;margin:0 0 4px}
h1{font-size:1.4rem;margin:0 0 6px;line-height:1.25}
.dataline{margin:0;color:var(--muted);font-size:.92rem}
main{padding:6px 0 30px}
.card{background:#fff;border:1px solid var(--line);border-radius:10px;padding:18px 20px;margin:16px 0}
h2{font-size:1.08rem;margin:0 0 4px}
h3{font-size:.95rem;margin:14px 0 8px}
.note{font-size:.85rem;color:var(--muted);margin:8px 0 0}
.note strong{color:#41505f}
.controls{display:flex;flex-wrap:wrap;gap:14px;align-items:flex-end}
.field{display:flex;flex-direction:column;gap:4px}
.field>label{font-size:.8rem;font-weight:700;color:var(--muted);text-transform:uppercase;letter-spacing:.05em}
select{font:inherit;padding:8px 10px;border:1px solid var(--line);border-radius:7px;background:#fff;min-width:230px;max-width:100%;color:var(--ink)}
select:focus{outline:2px solid var(--accent);outline-offset:1px}
button{font:inherit;cursor:pointer}
#swap{padding:8px 12px;border:1px solid var(--line);border-radius:7px;background:#fff;color:var(--accent);font-weight:700}
#swap:hover{background:#eef4fa}
.seg-group{display:flex;border:1px solid var(--line);border-radius:7px;overflow:hidden;background:#fff}
.seg{padding:8px 14px;border:0;border-right:1px solid var(--line);background:#fff;color:var(--ink)}
.seg:last-child{border-right:0}
.seg.active{background:var(--accent);color:#fff;font-weight:600}
.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));gap:14px;margin-top:16px}
.stat{background:#fff;border:1px solid var(--line);border-radius:10px;padding:14px 16px}
.stat .num{font-size:1.9rem;font-weight:700;color:var(--accent);line-height:1.1}
.stat .pct{font-size:1rem;color:var(--muted);font-weight:600}
.stat .lbl{margin-top:4px;font-size:.9rem;color:var(--muted)}
.chart-wrap{position:relative;height:320px;margin-top:12px}
table{width:100%;border-collapse:collapse;margin-top:6px;font-size:.92rem}
th,td{padding:6px 10px;border-bottom:1px solid var(--line);text-align:right}
th:first-child,td:first-child{text-align:left}
th{color:var(--muted);font-size:.76rem;text-transform:uppercase;letter-spacing:.05em;font-weight:700}
tr.tot td{font-weight:700;border-top:2px solid var(--line)}
.vote{border:1px solid var(--line);border-radius:9px;padding:12px 14px;margin:10px 0;background:#fff}
.vote-head{display:flex;flex-wrap:wrap;gap:10px;align-items:baseline}
.sym{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;font-size:.85rem;color:var(--accent);font-weight:600;text-decoration:none}
a.sym:hover{text-decoration:underline}
.badge{font-size:.72rem;font-weight:700;text-transform:uppercase;letter-spacing:.05em;background:#e8f1f9;color:var(--accent-dark);border-radius:999px;padding:2px 9px}
.date{color:var(--muted);font-size:.85rem}
.meta{color:var(--muted);font-size:.82rem}
.vote-title{font-weight:600;margin:6px 0 8px}
.votes-line{display:flex;flex-wrap:wrap;gap:8px;align-items:center;font-size:.9rem}
.vs{color:var(--muted);font-size:.82rem}
.chip{display:inline-block;padding:2px 11px;border-radius:999px;font-weight:600;font-size:.85rem;border:1px solid}
.vY{color:#1e7b34;background:#edf7ef;border-color:#bfe0c8}
.vN{color:#b3261e;background:#fdecea;border-color:#f2c4c0}
.vA,.vOther{color:#54626f;background:#f1f4f8;border-color:#d6dee7}
.warn{margin-top:9px;font-size:.83rem;background:var(--warn-bg);border:1px solid var(--warn-line);color:var(--warn-ink);padding:6px 10px;border-radius:7px}
.empty{border:1px dashed var(--line);background:#fbfcfe;color:var(--muted);border-radius:9px;padding:14px 16px;margin-top:10px}
.reclink{font-size:.8rem;color:var(--accent)}
footer{border-top:1px solid var(--line);background:#fff;padding:14px 0 24px;color:var(--muted);font-size:.85rem}
</style>
</head>
<body>
<header class="top"><div class="wrap">
  <p class="kicker">Human Rights Council · recorded votes</p>
  <h1>Comparing how two States vote at the Human Rights Council</h1>
  <p class="dataline" id="dataLine"></p>
</div></header>
<main><div class="wrap">
  <div class="empty" id="fewStates" style="display:none">Fewer than two States appear in the roll calls of this dataset, so a two-State comparison cannot be shown.</div>

  <section class="card" id="controls">
    <div class="controls">
      <div class="field"><label for="stateA">State A</label><select id="stateA"></select></div>
      <div class="field"><button id="swap" title="Swap State A and State B" aria-label="Swap the two States">⇄ swap</button></div>
      <div class="field"><label for="stateB">State B</label><select id="stateB"></select></div>
      <div class="field"><label id="kindLabel">Vote type</label>
        <div class="seg-group" role="group" aria-labelledby="kindLabel">
          <button class="seg active" data-kind="all">Both</button>
          <button class="seg" data-kind="resolution">Resolutions</button>
          <button class="seg" data-kind="amendment">Amendments</button>
        </div>
      </div>
    </div>
  </section>

  <section id="summary" aria-live="polite">
    <div class="stats">
      <div class="stat"><div class="num" id="statCommon">–</div><div class="lbl">recorded votes both States took part in</div></div>
      <div class="stat"><div class="num" id="statSame">–</div><div class="lbl">voted the same way</div></div>
      <div class="stat"><div class="num" id="statDiff">–</div><div class="lbl">voted differently</div></div>
    </div>
    <p class="note" id="summaryNote"></p>
  </section>

  <section class="card" id="chartCard">
    <h2>Timeline by year</h2>
    <div class="chart-wrap" id="chartWrap"><canvas id="yearChart"></canvas></div>
    <div class="empty" id="chartEmpty" style="display:none">No votes with a year in the current filter, so no timeline can be drawn.</div>
    <p class="note">How this is computed: each bar is one year of recorded votes in the current filter; the segments count only the votes where both selected States appear in the roll call, split by whether their vote codes matched. Roll-call entries are used here, not the official totals. Votes without a year are not charted.</p>
    <div id="yearTableWrap" style="display:none">
      <h3>Year-by-year counts</h3>
      <table>
        <thead><tr><th>Year</th><th>Both took part</th><th>Same</th><th>Differ</th><th>% same</th></tr></thead>
        <tbody id="yearTableBody"></tbody>
      </table>
    </div>
  </section>

  <section class="card" id="diffCard">
    <h2 id="diffHeading">Votes where they differed</h2>
    <p class="note">How this is computed: every recorded vote in the current filter where the two selected States have different vote codes in the roll call, most recent first. The symbol links to the UN document (or, if none is recorded, to the OHCHR record page) in a new tab. A ⚠ warning marks rows where the official totals (yes / no / abstain) do not match the roll call counted from the record.</p>
    <div id="diffList"></div>
  </section>
</div></main>
<footer><div class="wrap">All counts, filters and charts on this page are computed in your browser from the loaded dataset — nothing is estimated and no data leaves this page.</div></footer>

<script>
(function(){
"use strict";
var W = window.WORKSHOP_DATA || {};
var HRC = W.hrc || {};
var records = Array.isArray(HRC.records) ? HRC.records : [];
var countries = (HRC.countries && typeof HRC.countries === "object") ? HRC.countries : {};
var voteCodes = (HRC.vote_codes && typeof HRC.vote_codes === "object") ? HRC.vote_codes : {};
function $(id){ return document.getElementById(id); }
function esc(s){ return String(s==null?"":s).replace(/[&<>"']/g, function(c){ return {"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]; }); }
function codeLabel(c){ return voteCodes[c] ? String(voteCodes[c]) : String(c); }
function num(v){ if(typeof v==="number" && isFinite(v)) return v; if(v===null||v===undefined||v==="") return null; var n=Number(v); return isNaN(n)?null:n; }
function yearOf(r){ return num(r && r.year); }
function nameOf(iso){ return countries[iso] || iso; }

/* States that were Council members in at least one recorded vote */
var memberSet = {};
records.forEach(function(r){
  if(r && r.votes && typeof r.votes==="object"){ Object.keys(r.votes).forEach(function(k){ memberSet[k]=true; }); }
});
var stateOptions = Object.keys(memberSet).map(function(iso){ return {iso:iso, name:nameOf(iso)}; })
  .sort(function(a,b){ return a.name.localeCompare(b.name, undefined, {sensitivity:"base"}) || a.iso.localeCompare(b.iso); });

var state = {
  a: stateOptions.length>0 ? stateOptions[0].iso : "",
  b: stateOptions.length>1 ? stateOptions[1].iso : "",
  kind: "all"
};
var KIND_LABEL = { all:"all recorded votes (resolutions and amendments)", resolution:"resolutions only", amendment:"amendments only" };

function kindMatches(r, kind){
  if(kind==="all") return true;
  return String((r && r.kind) || "").toLowerCase() === kind;
}
function rollCall(r){
  var c = {Y:0,N:0,A:0,other:0};
  if(r && r.votes && typeof r.votes==="object"){
    Object.keys(r.votes).forEach(function(k){ var v=r.votes[k]; if(v==="Y"||v==="N"||v==="A") c[v]++; else c.other++; });
  }
  return c;
}
function totalsMismatch(r){
  var y=num(r.yes), n=num(r.no), a=num(r.abstain);
  if(y===null||n===null||a===null) return null;
  var rc=rollCall(r);
  if(rc.Y===y && rc.N===n && rc.A===a && rc.other===0) return null;
  return {official:{Y:y,N:n,A:a}, roll:rc};
}
function chipClass(c){ return (c==="Y"||c==="N"||c==="A") ? "v"+c : "vOther"; }
function docLink(r){
  var d = r.doc_url ? String(r.doc_url).trim() : "";
  var rec = r.record_url ? String(r.record_url).trim() : "";
  return {doc:d, rec:rec, url: d || rec};
}

var chart = null;

function render(){
  var aName = nameOf(state.a), bName = nameOf(state.b);
  var filtered = records.filter(function(r){ return kindMatches(r, state.kind); });
  var common = [];
  filtered.forEach(function(r){
    var va = r.votes ? r.votes[state.a] : undefined;
    var vb = r.votes ? r.votes[state.b] : undefined;
    if(va!==undefined && va!==null && va!=="" && vb!==undefined && vb!==null && vb!==""){
      common.push({r:r, va:va, vb:vb, same: va===vb});
    }
  });
  var differ = common.filter(function(x){ return !x.same; });
  var sameCount = common.length - differ.length;
  var pctSame = common.length ? Math.round(sameCount/common.length*100) : null;
  var pctDiff = common.length ? Math.round(differ.length/common.length*100) : null;

  $("statCommon").textContent = common.length;
  $("statSame").innerHTML = sameCount + (pctSame!==null ? ' <span class="pct">('+pctSame+'%)</span>' : "");
  $("statDiff").innerHTML = differ.length + (pctDiff!==null ? ' <span class="pct">('+pctDiff+'%)</span>' : "");

  var extra = "";
  if(state.a && state.a===state.b) extra += " Note: both selectors are set to <strong>"+esc(aName)+"</strong>, so every common vote counts as \u201Csame\u201D.";
  if(common.length===0) extra += " In the current filter these two States never both appear in the same roll call.";
  $("summaryNote").innerHTML = "How this is computed: from the <strong>"+filtered.length+"</strong> recorded votes in the current filter ("+KIND_LABEL[state.kind]+"), a vote is counted only if both <strong>"+esc(aName)+"</strong> and <strong>"+esc(bName)+"</strong> have an entry in its roll call. \u201CSame\u201D means an identical vote code ("+["Y","N","A"].map(codeLabel).join(" / ")+"). Counts are exact, not estimated." + extra;

  renderChart(filtered, common);
  renderYearTable(common);
  renderDiffer(differ, common.length, aName, bName);
}

function renderChart(filtered, common){
  var yearSet = {};
  filtered.forEach(function(r){ var y=yearOf(r); if(y!==null) yearSet[y]=true; });
  var years = Object.keys(yearSet).map(Number).sort(function(a,b){ return a-b; });
  var perYear = {};
  years.forEach(function(y){ perYear[y]={same:0,differ:0}; });
  common.forEach(function(x){
    var y=yearOf(x.r);
    if(y!==null && perYear[y]){ if(x.same) perYear[y].same++; else perYear[y].differ++; }
  });
  var wrap = $("chartWrap");
  if(!years.length){
    if(chart){ chart.destroy(); chart=null; }
    wrap.style.display="none";
    $("chartEmpty").style.display="block";
    return;
  }
  $("chartEmpty").style.display="none";
  wrap.style.display="block";
  if(chart) chart.destroy();
  chart = new Chart($("yearChart").getContext("2d"), {
    type:"bar",
    data:{ labels: years.map(String),
      datasets:[
        {label:"Voted the same", data: years.map(function(y){ return perYear[y].same; }), backgroundColor:"#1f6fb2"},
        {label:"Voted differently", data: years.map(function(y){ return perYear[y].differ; }), backgroundColor:"#d64541"}
      ]},
    options:{ responsive:true, maintainAspectRatio:false,
      plugins:{ legend:{position:"bottom"},
        tooltip:{ callbacks:{ label:function(ctx){ return " "+ctx.dataset.label+": "+ctx.parsed.y+" vote"+(ctx.parsed.y===1?"":"s"); } } } },
      scales:{ x:{stacked:true, title:{display:true, text:"Year"}},
               y:{stacked:true, beginAtZero:true, ticks:{precision:0}, title:{display:true, text:"Recorded votes both took part in"}} } }
  });
}

function renderYearTable(common){
  var perYear = {};
  common.forEach(function(x){
    var y=yearOf(x.r); if(y===null) return;
    if(!perYear[y]) perYear[y]={same:0,differ:0};
    if(x.same) perYear[y].same++; else perYear[y].differ++;
  });
  var years = Object.keys(perYear).map(Number).sort(function(a,b){ return a-b; });
  if(!years.length){ $("yearTableWrap").style.display="none"; return; }
  $("yearTableWrap").style.display="block";
  var html="", totB=0, totS=0;
  years.forEach(function(y){
    var b=perYear[y].same+perYear[y].differ, s=perYear[y].same;
    totB+=b; totS+=s;
    html += "<tr><td>"+y+"</td><td>"+b+"</td><td>"+s+"</td><td>"+(b-s)+"</td><td>"+(b? Math.round(s/b*100)+"%":"\u2014")+"</td></tr>";
  });
  html += "<tr class='tot'><td>Total</td><td>"+totB+"</td><td>"+totS+"</td><td>"+(totB-totS)+"</td><td>"+(totB? Math.round(totS/totB*100)+"%":"\u2014")+"</td></tr>";
  $("yearTableBody").innerHTML = html;
}

function renderDiffer(differ, commonCount, aName, bName){
  $("diffHeading").textContent = "Votes where they differed \u2014 " + differ.length + " of " + commonCount + " common votes";
  var list = $("diffList");
  if(!differ.length){
    list.innerHTML = '<div class="empty">No recorded votes in the current filter where the two States voted differently.</div>';
    return;
  }
  var sorted = differ.slice().sort(function(x,y){
    var da=String(x.r.date||""), db=String(y.r.date||"");
    if(da!==db) return da<db ? 1 : -1; /* most recent first */
    return String(x.r.symbol||"").localeCompare(String(y.r.symbol||""));
  });
  var html="";
  sorted.forEach(function(x){
    var r=x.r, link=docLink(r);
    var sym = esc(r.symbol || r.id || "(no symbol)");
    var symHtml = link.url ? '<a class="sym" href="'+esc(link.url)+'" target="_blank" rel="noopener noreferrer">'+sym+'</a>' : '<span class="sym">'+sym+'</span>';
    var recLink = (link.doc && link.rec) ? ' \u00B7 <a class="reclink" href="'+esc(link.rec)+'" target="_blank" rel="noopener noreferrer">OHCHR record page</a>' : "";
    var kind = String(r.kind||"vote");
    var badge = '<span class="badge">'+esc(kind.charAt(0).toUpperCase()+kind.slice(1))+'</span>';
    var metaBits=[];
    if(r.session) metaBits.push(esc(r.session));
    if(r.agenda_item) metaBits.push(esc(r.agenda_item));
    var meta = metaBits.length ? ' <span class="meta">'+metaBits.join(" \u00B7 ")+'</span>' : "";
    var mm = totalsMismatch(r), warn="";
    if(mm){
      warn = '<div class="warn">\u26A0 Official totals ('+codeLabel("Y")+" "+mm.official.Y+", "+codeLabel("N")+" "+mm.official.N+", "+codeLabel("A")+" "+mm.official.A+') do not match the roll call counted from the record ('+codeLabel("Y")+" "+mm.roll.Y+", "+codeLabel("N")+" "+mm.roll.N+", "+codeLabel("A")+" "+mm.roll.A+(mm.roll.other?", other "+mm.roll.other:"")+').</div>';
    }
    html += '<div class="vote">'
      + '<div class="vote-head">'+symHtml+badge+'<span class="date">'+esc(r.date||"date unknown")+'</span>'+meta+'</div>'
      + '<div class="vote-title">'+esc(r.title||"(untitled)")+'</div>'
      + '<div class="votes-line"><span class="chip '+chipClass(x.va)+'">'+esc(aName)+': '+esc(codeLabel(x.va))+'</span>'
      + '<span class="vs">vs</span>'
      + '<span class="chip '+chipClass(x.vb)+'">'+esc(bName)+': '+esc(codeLabel(x.vb))+'</span>'+recLink+'</div>'
      + warn
      + '</div>';
  });
  list.innerHTML = html;
}

function fillSelect(sel){
  sel.innerHTML="";
  stateOptions.forEach(function(o){
    var opt=document.createElement("option");
    opt.value=o.iso;
    opt.textContent=o.name+" ("+o.iso+")";
    sel.appendChild(opt);
  });
}

function init(){
  var yearsAll = records.map(yearOf).filter(function(y){ return y!==null; });
  var minY = yearsAll.length ? Math.min.apply(null, yearsAll) : null;
  var maxY = yearsAll.length ? Math.max.apply(null, yearsAll) : null;
  var src = HRC.title ? String(HRC.title) : "Human Rights Council recorded votes";
  $("dataLine").textContent = "Source: " + src + " \u2014 " + records.length + " recorded votes" +
    (minY!==null ? ", "+minY+"\u2013"+maxY : "") + ", " + stateOptions.length +
    " States appear as Council members in at least one roll call. All figures below are computed from this dataset in your browser.";

  if(stateOptions.length < 2){
    ["controls","summary","chartCard","diffCard"].forEach(function(id){ $(id).style.display="none"; });
    $("fewStates").style.display="block";
    return;
  }
  $("fewStates").style.display="none";
  fillSelect($("stateA")); fillSelect($("stateB"));
  $("stateA").value = state.a; $("stateB").value = state.b;

  $("stateA").addEventListener("change", function(e){ state.a=e.target.value; render(); });
  $("stateB").addEventListener("change", function(e){ state.b=e.target.value; render(); });
  $("swap").addEventListener("click", function(){
    var t=$("stateA").value;
    $("stateA").value=$("stateB").value;
    $("stateB").value=t;
    state.a=$("stateA").value; state.b=$("stateB").value;
    render();
  });
  Array.prototype.forEach.call(document.querySelectorAll(".seg"), function(btn){
    btn.addEventListener("click", function(){
      Array.prototype.forEach.call(document.querySelectorAll(".seg"), function(b){ b.classList.remove("active"); });
      btn.classList.add("active");
      state.kind = btn.getAttribute("data-kind");
      render();
    });
  });
  render();
}
init();
})();
</script>
</body>
</html>
```