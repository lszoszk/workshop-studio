Here's the complete dashboard: four tabs (overview, records, self-checks, method & export) over `WORKSHOP_DATA.uhri`, with the filter rail, seeded label sampling, CSV export and every number computed by loops in the browser — nothing estimated, nothing sent anywhere except a clipboard write.

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>UHRI dashboard</title>
<style>
:root{--paper:#f4f0e8;--ink:#1d1b18;--rule:#d9d2c3;--red:#9b2335;--mut:#5b564c;--mono:ui-monospace,Menlo,Consolas,monospace}
*{box-sizing:border-box}
[hidden]{display:none!important}
html,body{margin:0;padding:0}
body{background:var(--paper);color:var(--ink);font:16px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
a{color:var(--ink)}
:focus-visible{outline:2px solid var(--red);outline-offset:2px}
header{padding:22px 30px 16px;border-bottom:1px solid var(--rule)}
.kicker{font:11px/1 var(--mono);letter-spacing:.16em;text-transform:uppercase;color:var(--red)}
h1{font-family:Georgia,"Times New Roman",serif;font-weight:400;font-size:34px;line-height:1.15;margin:10px 0 8px;max-width:920px}
.meta{margin:0;font-size:13px;color:var(--mut)}
.layout{display:flex;align-items:flex-start}
aside#rail{width:262px;flex:0 0 262px;border-right:1px solid var(--rule);padding:18px 20px 30px;position:sticky;top:0;max-height:100vh;overflow:auto}
.rail-h{display:flex;justify-content:space-between;align-items:baseline}
.lbl{font:11px var(--mono);letter-spacing:.16em;color:var(--red)}
#clearAll{background:none;border:none;font:11px var(--mono);color:var(--mut);cursor:pointer;text-decoration:underline;padding:0}
.bignum{font-family:Georgia,serif;font-size:54px;line-height:1;margin:12px 0 2px}
.of{font:11px var(--mono);color:var(--mut)}
.sharebar{height:4px;background:var(--rule);margin:10px 0 4px}
.sharebar i{display:block;height:100%;background:var(--red);width:0}
.chips{display:flex;flex-wrap:wrap;gap:4px;margin:8px 0 6px;min-height:4px}
.chip{font:11px var(--mono);background:#fbf8f1;border:1px solid var(--rule);border-radius:11px;padding:2px 8px;cursor:pointer;color:var(--ink)}
.chip b{color:var(--red);font-weight:400}
.acc-btn{width:100%;display:flex;justify-content:space-between;align-items:center;background:none;border:none;border-top:1px solid var(--rule);padding:11px 0 9px;font:12px var(--mono);letter-spacing:.1em;color:var(--ink);cursor:pointer;text-align:left}
.acc-btn .n{color:var(--red);margin-right:6px}
.acc-btn .arr{color:var(--mut)}
.acc-panel{padding:2px 0 14px}
.acc-panel input[type=search]{width:100%;padding:6px 8px;border:1px solid var(--rule);background:#fbf8f1;font:14px inherit;color:var(--ink)}
.hint{font:11px var(--mono);color:var(--mut);margin-top:5px;line-height:1.5}
.how{font:11px var(--mono);color:var(--mut);margin-top:8px;line-height:1.5}
.rail-min .acc,.rail-min .how{display:none}
.fl{display:block;font:11px var(--mono);letter-spacing:.08em;text-transform:uppercase;color:var(--mut);margin:10px 0 3px}
.fl select{display:block;width:100%;margin-top:3px;padding:5px 6px;border:1px solid var(--rule);background:#fbf8f1;font:13px -apple-system,"Segoe UI",Roboto,sans-serif;color:var(--ink)}
.yrow{display:flex;gap:8px}.yrow .fl{flex:1}
main{flex:1;min-width:0;padding:18px 30px 50px}
.tabs{display:flex;gap:4px;border-bottom:1px solid var(--rule);margin-bottom:20px;flex-wrap:wrap}
.tab{background:none;border:none;border-bottom:2px solid transparent;padding:9px 13px;font:12px var(--mono);letter-spacing:.1em;text-transform:uppercase;color:var(--mut);cursor:pointer}
.tab[aria-selected="true"]{color:var(--red);border-bottom-color:var(--red)}
.tiles{display:flex;flex-wrap:wrap;border-top:1px solid var(--rule);border-bottom:1px solid var(--rule);margin-bottom:8px}
.tile{padding:16px 26px 14px 0;margin-right:26px;border-right:1px solid var(--rule);min-width:180px}
.tile:last-child{border-right:none}
.num{font-family:Georgia,serif;font-size:46px;line-height:1}
.cap{font:11px var(--mono);letter-spacing:.12em;text-transform:uppercase;color:var(--mut);margin-top:6px}
.sub{font-size:13px;color:var(--mut);margin-top:3px}
.dot{display:inline-block;width:9px;height:9px;border-radius:50%;margin-right:6px}
.linkbtn{background:none;border:none;font:11px var(--mono);color:var(--red);text-decoration:underline;cursor:pointer;padding:0;margin-top:6px}
.stateslist{margin:6px 0;padding-left:20px;font-size:14px}
.fig{margin:30px 0 10px;max-width:880px}
.figno{font:11px var(--mono);letter-spacing:.16em;color:var(--red)}
.figtitle{font-family:Georgia,serif;font-weight:400;font-size:21px;margin:6px 0 12px}
.chartwrap{position:relative}
.src{font:11px var(--mono);color:var(--mut);margin-top:10px;line-height:1.5}
.nomatch{font:13px var(--mono);color:var(--mut);padding:18px 0}
table{border-collapse:collapse;width:100%;font-size:14px;margin-top:6px}
caption{text-align:left;font:11px var(--mono);color:var(--mut);padding:8px 0 4px}
th{font:11px var(--mono);letter-spacing:.08em;text-transform:uppercase;text-align:left;border-bottom:1px solid var(--ink);padding:6px 10px 6px 0}
td{border-bottom:1px solid var(--rule);padding:7px 10px 7px 0;vertical-align:top}
th.num,td.num{text-align:right;padding-right:0}
.thbtn{background:none;border:none;font:inherit;letter-spacing:inherit;text-transform:inherit;color:inherit;cursor:pointer;padding:0}
tbody tr.data{cursor:pointer}
tbody tr.data:hover{background:#ece5d5}
tr.detail td{background:#efe9db;padding:16px 20px}
.para-big{font-family:Georgia,serif;font-size:42px;color:var(--red);line-height:1;margin-bottom:8px}
.fulltext{max-width:780px;margin:0 0 10px;white-space:pre-wrap}
.labels{font-size:13px;max-width:780px}
.labels .ll{font:10px var(--mono);letter-spacing:.12em;color:var(--red);margin-right:6px}
.labels>div{margin:3px 0}
.missing{color:var(--mut);font-style:italic}
mark{background:#f0d9a0;padding:0 1px}
.btn{display:inline-block;background:none;border:1px solid var(--ink);color:var(--ink);font:12px var(--mono);padding:7px 14px;cursor:pointer;text-decoration:none;margin:4px 8px 4px 0}
.btn:hover{background:#e9e2d1}
.btnrow{margin-top:10px}
.searchrow{display:flex;align-items:baseline;gap:12px;margin-bottom:8px;flex-wrap:wrap}
.searchrow input{flex:1;min-width:260px;padding:8px 10px;border:1px solid var(--rule);background:#fbf8f1;font:15px inherit;color:var(--ink)}
.ptitle{font-family:Georgia,serif;font-weight:400;font-size:22px;margin:26px 0 6px}
.checkline{display:flex;gap:14px;align-items:baseline;padding:8px 0;border-bottom:1px solid var(--rule);font-size:14px}
.cname{font:11px var(--mono);letter-spacing:.08em;text-transform:uppercase;white-space:nowrap;min-width:150px}
.cdetail{flex:1;color:var(--mut);word-break:break-word}
.st{font:11px var(--mono);white-space:nowrap}
.st.pass{color:#0f766e}.st.warn{color:#b45309}.st.fail{color:var(--red)}
.sample-controls{display:flex;align-items:center;gap:10px;flex-wrap:wrap;margin:10px 0}
.seedlbl{margin:0}
.seedlbl input{width:90px;padding:5px 6px;border:1px solid var(--rule);background:#fbf8f1;font:13px var(--mono)}
.tally{font:12px var(--mono);border-top:1px solid var(--rule);border-bottom:1px solid var(--rule);padding:8px 0;margin:8px 0 4px;line-height:1.6}
.card{border-bottom:1px solid var(--rule)}
.card-btn{width:100%;text-align:left;background:none;border:none;padding:9px 0;font:13px var(--mono);cursor:pointer;color:var(--ink)}
.card-btn .arr{color:var(--red);margin-right:6px}
.card-panel{border-left:2px solid var(--red);padding:2px 0 14px 16px;margin:0 0 12px}
.themechips{display:flex;flex-wrap:wrap;gap:4px;margin:8px 0}
.themechips span{font:11px var(--mono);border:1px solid var(--rule);border-radius:10px;padding:2px 8px;background:#fbf8f1}
.vbtns{display:flex;gap:6px}
.vbtn{background:none;border:1px solid var(--rule);font:11px var(--mono);padding:5px 12px;cursor:pointer;color:var(--ink)}
.vbtn.on{background:var(--red);border-color:var(--red);color:#fff}
.method{max-width:780px;padding-left:20px}
.method li{margin:7px 0}
.mono{font-family:var(--mono);font-size:13px}
.credits{font:11px var(--mono);color:var(--mut);max-width:780px;line-height:1.6}
footer{border-top:1px solid var(--rule);padding:12px 30px;font:11px var(--mono);color:var(--mut)}
@media (max-width:900px){.layout{flex-direction:column}aside#rail{width:100%;flex:none;position:static;max-height:none;border-right:none;border-bottom:1px solid var(--rule)}main{padding:14px 18px 40px}header{padding:16px 18px 12px}}
</style>
</head>
<body>
<header>
  <div class="kicker" id="kicker"></div>
  <h1 id="title"></h1>
  <p class="meta" id="meta"></p>
</header>
<div class="layout">
  <aside id="rail" aria-label="Filters">
    <div class="rail-h"><span class="lbl">FILTERS</span><button type="button" id="clearAll">Clear all</button></div>
    <div class="bignum" id="matchNum" aria-live="polite">–</div>
    <div class="of" id="ofNum"></div>
    <div class="sharebar" aria-hidden="true"><i id="shareFill"></i></div>
    <div class="chips" id="chips"></div>
    <div class="acc" id="accWrap">
      <button type="button" class="acc-btn" data-acc="0" aria-expanded="false" aria-controls="accp0"><span><span class="n">01</span>KEYWORD</span><span class="arr">▾</span></button>
      <div class="acc-panel" id="accp0" hidden>
        <input type="search" id="kw1" placeholder="e.g. torture" aria-label="Keyword filter">
        <div class="hint">literal match, not synonyms · every word must appear in the text or symbol · applied 300 ms after typing</div>
      </div>
      <button type="button" class="acc-btn" data-acc="1" aria-expanded="false" aria-controls="accp1"><span><span class="n">02</span>MECHANISM · BODY · TYPE</span><span class="arr">▾</span></button>
      <div class="acc-panel" id="accp1" hidden>
        <label class="fl">Mechanism<select id="fMech"></select></label>
        <label class="fl">Body / mandate<select id="fBody"></select></label>
        <label class="fl">Type<select id="fType"></select></label>
        <label class="fl">Recommending State (UPR)<select id="fState"></select></label>
      </div>
      <button type="button" class="acc-btn" data-acc="2" aria-expanded="false" aria-controls="accp2"><span><span class="n">03</span>YEARS &amp; SDG</span><span class="arr">▾</span></button>
      <div class="acc-panel" id="accp2" hidden>
        <div class="yrow">
          <label class="fl">Year from<select id="fY0"></select></label>
          <label class="fl">to<select id="fY1"></select></label>
        </div>
        <label class="fl">SDG<select id="fSdg"></select></label>
      </div>
    </div>
    <div class="how">How this is computed: records passing every filter above, combined with AND.</div>
  </aside>
  <main>
    <div class="tabs" role="tablist" aria-label="Dashboard sections" id="tablist">
      <button type="button" class="tab" role="tab" id="tab0" aria-controls="panel0" aria-selected="true">01 Overview</button>
      <button type="button" class="tab" role="tab" id="tab1" aria-controls="panel1" aria-selected="false" tabindex="-1">02 Records</button>
      <button type="button" class="tab" role="tab" id="tab2" aria-controls="panel2" aria-selected="false" tabindex="-1">03 Check</button>
      <button type="button" class="tab" role="tab" id="tab3" aria-controls="panel3" aria-selected="false" tabindex="-1">04 Method &amp; export</button>
    </div>

    <section id="panel0" role="tabpanel" aria-labelledby="tab0">
      <div class="tiles" id="tiles"></div>
      <div class="fig">
        <div class="figno">FIG.01</div>
        <h3 class="figtitle" id="fig1title"></h3>
        <div class="chartwrap" id="fig1wrap" style="height:340px"><canvas id="fig1"></canvas></div>
        <div class="nomatch" id="fig1none" hidden>No records match the current filters.</div>
        <table id="fig1tab"></table>
        <div class="how" id="fig1how"></div>
        <div class="src" id="fig1src"></div>
      </div>
      <div class="fig">
        <div class="figno">FIG.02</div>
        <h3 class="figtitle" id="fig2title"></h3>
        <div class="chartwrap" style="height:300px"><canvas id="fig2"></canvas></div>
        <div class="how" id="fig2how"></div>
        <div class="src" id="fig2src"></div>
      </div>
    </section>

    <section id="panel1" role="tabpanel" aria-labelledby="tab1" hidden>
      <div class="searchrow">
        <input type="search" id="kw2" placeholder="Search the filtered records, e.g. torture" aria-label="Search records">
        <span class="hint">same box as 01 Keyword · literal match, not synonyms</span>
      </div>
      <table id="rectab">
        <caption id="reccap"></caption>
        <thead><tr>
          <th scope="col"><button type="button" class="thbtn" id="thDate">Date ▾</button></th>
          <th scope="col">Body</th>
          <th scope="col">Symbol</th>
          <th scope="col">Para.</th>
          <th scope="col">First line</th>
          <th scope="col">Recommending State</th>
        </tr></thead>
        <tbody id="recbody"></tbody>
      </table>
      <button type="button" class="btn" id="moreBtn">Show 50 more</button>
    </section>

    <section id="panel2" role="tabpanel" aria-labelledby="tab2" hidden>
      <h2 class="ptitle">How the app checks itself</h2>
      <p class="hint">Each line compares two values computed by separate loops over the file. Nothing is hidden; a red line is a failed check.</p>
      <div id="checks"></div>
      <h2 class="ptitle">Check the UN's labels on a random sample</h2>
      <p class="hint">Ten records drawn from the current filter with a seeded generator, so a colleague can draw the same ten. This is your judgement of the UN's labels; nothing is sent anywhere.</p>
      <div class="sample-controls">
        <button type="button" class="btn" id="drawBtn">Check 10 at random</button>
        <button type="button" class="btn" id="drawAgain">Draw again</button>
        <label class="fl seedlbl">seed <input type="number" id="seedBox" value="1" min="1"></label>
        <button type="button" class="btn" id="drawSeed">Draw with this seed</button>
      </div>
      <div class="tally" id="tally"></div>
      <div id="cards"></div>
    </section>

    <section id="panel3" role="tabpanel" aria-labelledby="tab3" hidden>
      <h2 class="ptitle">How this was made</h2>
      <ol class="method">
        <li>Every number on this page is computed by loops over the records in the attached file (<span class="mono">WORKSHOP_DATA.uhri</span>); nothing is estimated and no language model is called.</li>
        <li>The headline count is the number of records passing the filters in the left rail; documents are distinct <span class="mono">symbol</span> values; years are the minimum and maximum of <span class="mono">year</span>, which is the document's date, not the date a recommendation was made or accepted.</li>
        <li>Filters combine with AND: mechanism, body, type and recommending State match the field exactly; years are inclusive between the two selects; an SDG matches when the record lists that goal; the keyword requires every typed word to appear literally in the text or the symbol — "torture" will not find "ill-treatment".</li>
        <li>Paragraph numbers are read from the start of each text with a fixed pattern ("71." or "144.43"); recommending States are read only from the parentheses at the end of UPR texts, and a group with a comma or over 60 characters is rejected as "State not found".</li>
        <li>Theme counts count each theme of each record once, so they add up to more than the record count; the app never removes, renames or re-labels a UN label — the year range per theme and the random sample let you judge them.</li>
        <li>The CSV export is generated in your browser from the filtered rows, with the full text and all labels; the only thing that can leave this page is the clipboard write when you press a Copy button.</li>
      </ol>
      <h2 class="ptitle">Take it with you</h2>
      <div class="btnrow">
        <button type="button" class="btn" id="csvBtn">Download CSV of the current filter</button>
        <button type="button" class="btn" id="sumBtn">Copy summary</button>
      </div>
      <div class="hint" id="exportNote"></div>
      <h2 class="ptitle">Source</h2>
      <p class="src" id="srcBlock"></p>
      <p class="credits">Credits: data — OHCHR Universal Human Rights Index (UHRI). Design guidance — UK Government Analysis Function, "Data visualisation: charts" and "Data visualisation: tables" (Open Government Licence v3.0). Citation practice — UN Dag Hammarskjöld Library, Ask DAG. Data approach — OHCHR, "A Human Rights-Based Approach to Data".</p>
    </section>
  </main>
</div>
<footer id="foot"></footer>

<script>
(function(){
"use strict";
var U=window.WORKSHOP_DATA.uhri;
var records=U.records||[];
var country=U.country||"the country";
var sdgNames=U.sdg_names||{};
var N=records.length;
var MONO='ui-monospace, Menlo, Consolas, monospace';
var MEC_COLORS={"Universal Periodic Review":"#c2410c","Treaty bodies":"#0f766e","Special Procedures":"#7c3aed"};
var PARA_RE=/^(\d{1,3}(?:\.\d{1,3})?)\.?\s/;
var STATE_RUN_RE=/((?:\s*\((?:[^()]|\([^()]*\))*\))+)\s*[;.]?\s*$/;
var STATE_GROUP_RE=/\((?:[^()]|\([^()]*\))*\)/g;

function esc(s){return String(s==null?"":s).replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;").replace(/"/g,"&quot;");}
function escRe(s){return s.replace(/[.*+?^${}()|[\]\\]/g,"\\$&");}
function fmt(n){return Number(n).toLocaleString("en-US");}
function $(id){return document.getElementById(id);}

var yearsAll=records.map(function(r){return r.year;}).filter(function(y){return typeof y==="number";});
var Y0=yearsAll.length?Math.min.apply(null,yearsAll):null;
var Y1=yearsAll.length?Math.max.apply(null,yearsAll):null;
var docCount=Object.keys(records.reduce(function(m,r){m[r.symbol]=1;return m;},{})).length;

records.forEach(function(r,i){
  r._i=i;
  var m=String(r.text||"").match(PARA_RE);
  r._para=m?m[1]:null;
  r._paraNum=m?parseFloat(m[1]):Infinity;
  r._hay=(String(r.text||"")+" "+String(r.symbol||"")).toLowerCase();
  r._states=null;
  if(r.mechanism==="Universal Periodic Review"){
    var run=String(r.text||"").match(STATE_RUN_RE);
    var out=[];
    if(run){
      var groups=run[1].match(STATE_GROUP_RE)||[];
      var bad=false;
      for(var g=0;g<groups.length;g++){
        var name=groups[g].slice(1,-1).trim();
        if(name.indexOf(",")>-1||name.length>60){bad=true;break;}
        out.push(name);
      }
      if(bad) out=["State not found"];
    }
    r._states=out;
  }
});

/* ---------- filters ---------- */
var F={keyword:"",mechanism:"all",body:"all",type:"all",state:"all",themes:new Set(),y0:Y0,y1:Y1,sdg:"all"};
var filtered=records.slice();
var themeTop=[];

function matches(r,skip){
  if(skip!=="mechanism"&&F.mechanism!=="all"&&r.mechanism!==F.mechanism) return false;
  if(skip!=="body"&&F.body!=="all"&&r.body!==F.body) return false;
  if(skip!=="type"&&F.type!=="all"&&r.type!==F.type) return false;
  if(skip!=="state"&&F.state!=="all"&&!(r._states&&r._states.indexOf(F.state)>-1)) return false;
  if(skip!=="theme"){for(var t of F.themes){if(!r.themes||r.themes.indexOf(t)<0)return false;}}
  if(skip!=="year"&&Y0!=null){if(typeof r.year!=="number"||r.year<F.y0||r.year>F.y1)return false;}
  if(skip!=="sdg"&&F.sdg!=="all"&&!(r.sdgs&&r.sdgs.map(Number).indexOf(Number(F.sdg))>-1)) return false;
  if(skip!=="keyword"&&F.keyword){
    var ws=F.keyword.toLowerCase().split(/\s+/).filter(Boolean);
    for(var w=0;w<ws.length;w++){if(r._hay.indexOf(ws[w])<0)return false;}
  }
  return true;
}

function chipList(){
  var c=[];
  if(F.keyword)c.push({k:"keyword",label:"Keyword: \u201C"+F.keyword+"\u201D"});
  if(F.mechanism!=="all")c.push({k:"mechanism",label:"Mechanism: "+F.mechanism});
  if(F.body!=="all")c.push({k:"body",label:"Body: "+F.body});
  if(F.type!=="all")c.push({k:"type",label:"Type: "+F.type});
  if(F.state!=="all")c.push({k:"state",label:"State: "+F.state});
  F.themes.forEach(function(t){c.push({k:"theme:"+t,label:"Theme: "+t});});
  if(Y0!=null&&(F.y0!==Y0||F.y1!==Y1))c.push({k:"years",label:"Years: "+F.y0+"\u2013"+F.y1});
  if(F.sdg!=="all")c.push({k:"sdg",label:"SDG: "+F.sdg+(sdgNames[String(F.sdg)]?" "+sdgNames[String(F.sdg)]:"")});
  return c;
}

/* ---------- rail ---------- */
function renderRail(){
  $("matchNum").textContent=fmt(filtered.length);
  $("ofNum").textContent="of "+fmt(N)+" in the file";
  $("shareFill").style.width=(N?filtered.length/N*100:0)+"%";
  var h="";
  chipList().forEach(function(ch){
    h+='<button type="button" class="chip" data-k="'+esc(ch.k)+'" title="remove this filter">'+esc(ch.label)+' <b>\u00D7</b></button>';
  });
  $("chips").innerHTML=h;
  fillStateOptions();
}

function fillMechOptions(){
  var counts={};records.forEach(function(r){counts[r.mechanism]=(counts[r.mechanism]||0)+1;});
  var o='<option value="all">all ('+fmt(N)+')</option>';
  Object.keys(counts).sort().forEach(function(m){o+='<option value="'+esc(m)+'">'+esc(m)+' ('+fmt(counts[m])+')</option>';});
  $("fMech").innerHTML=o;
}
function fillBodyOptions(){
  var src=F.mechanism==="all"?records:records.filter(function(r){return r.mechanism===F.mechanism;});
  var counts={};src.forEach(function(r){counts[r.body]=(counts[r.body]||0)+1;});
  var o='<option value="all">all bodies</option>';
  Object.keys(counts).sort(function(a,b){return counts[b]-counts[a]||a.localeCompare(b);}).forEach(function(b){
    o+='<option value="'+esc(b)+'">'+esc(b)+' ('+fmt(counts[b])+')</option>';
  });
  $("fBody").innerHTML=o;
  if(F.body!=="all"&&!counts[F.body])F.body="all";
  $("fBody").value=F.body;
}
function fillTypeOptions(){
  var counts={};records.forEach(function(r){counts[r.type]=(counts[r.type]||0)+1;});
  var o='<option value="all">all types</option>';
  Object.keys(counts).sort(function(a,b){return counts[b]-counts[a]||a.localeCompare(b);}).forEach(function(t){
    o+='<option value="'+esc(t)+'">'+esc(t)+' ('+fmt(counts[t])+')</option>';
  });
  $("fType").innerHTML=o;$("fType").value=F.type;
}
function fillStateOptions(){
  var src=records.filter(function(r){return matches(r,"state");});
  var counts={};
  src.forEach(function(r){if(r._states)r._states.forEach(function(s){if(s!=="State not found")counts[s]=(counts[s]||0)+1;});});
  var o='<option value="all">all States</option>';
  Object.keys(counts).sort(function(a,b){return counts[b]-counts[a]||a.localeCompare(b);}).forEach(function(s){
    o+='<option value="'+esc(s)+'">'+esc(s)+' ('+fmt(counts[s])+')</option>';
  });
  $("fState").innerHTML=o;
  if(F.state!=="all"&&counts[F.state])$("fState").value=F.state;else F.state="all";
}
function fillYearOptions(){
  if(Y0==null){$("fY0").innerHTML="";$("fY1").innerHTML="";return;}
  var ys=[],seen={};records.forEach(function(r){if(typeof r.year==="number"&&!seen[r.year]){seen[r.year]=1;ys.push(r.year);}});
  ys.sort(function(a,b){return a-b;});
  var o0="",o1="";
  ys.forEach(function(y){o0+='<option value="'+y+'">'+y+'</option>';o1+='<option value="'+y+'">'+y+'</option>';});
  $("fY0").innerHTML=o0;$("fY1").innerHTML=o1;
  $("fY0").value=String(F.y0);$("fY1").value=String(F.y1);
}
function fillSdgOptions(){
  var goals={};records.forEach(function(r){(r.sdgs||[]).forEach(function(g){goals[Number(g)]=1;});});
  var o='<option value="all">all SDGs</option>';
  Object.keys(goals).map(Number).sort(function(a,b){return a-b;}).forEach(function(g){
    var nm=sdgNames[String(g)]||"";
    o+='<option value="'+g+'">SDG '+g+(nm?" \u2014 "+esc(nm):"")+'</option>';
  });
  $("fSdg").innerHTML=o;$("fSdg").value=F.sdg==="all"?"all":String(F.sdg);
}

/* ---------- text helpers ---------- */
function highlight(text){
  var raw=String(text==null?"":text);
  var words=F.keyword.toLowerCase().split(/\s+/).filter(Boolean);
  if(!words.length)return esc(raw);
  var re=new RegExp("("+words.map(escRe).join("|")+")","gi");
  return raw.split(re).map(function(p,i){return i%2===1?"<mark>"+esc(p)+"</mark>":esc(p);}).join("");
}
function firstLine(t){
  t=String(t==null?"":t);
  if(t.length<=120)return t;
  var cut=t.slice(0,120),sp=cut.lastIndexOf(" ");
  if(sp>40)cut=cut.slice(0,sp);
  return cut+"\u2026";
}
function labelsHtml(r){
  var h="";
  if(r.section)h+="<div><span class='ll'>SECTION</span>"+esc(r.section)+"</div>";
  h+="<div><span class='ll'>THEMES</span>"+((r.themes&&r.themes.length)?r.themes.map(esc).join(" \u00B7 "):'<span class="missing">not labelled</span>')+"</div>";
  var sdgs=(r.sdgs||[]).map(function(g){return esc(String(g)+(sdgNames[String(g)]?" "+sdgNames[String(g)]:""));}).join(" \u00B7 ");
  h+="<div><span class='ll'>SDGS</span>"+(sdgs||'<span class="missing">not labelled</span>')+"</div>";
  if(r.sdg_targets&&r.sdg_targets.length)h+="<div><span class='ll'>SDG TARGETS</span>"+r.sdg_targets.map(esc).join(" \u00B7 ")+"</div>";
  h+="<div><span class='ll'>AFFECTED PERSONS</span>"+((r.affected_persons&&r.affected_persons.length)?r.affected_persons.map(esc).join(" \u00B7 "):'<span class="missing">not labelled</span>')+"</div>";
  return h;
}
function copyText(t,done){
  if(navigator.clipboard&&navigator.clipboard.writeText){
    navigator.clipboard.writeText(t).then(function(){done(true);},function(){fallbackCopy(t,done);});
  }else fallbackCopy(t,done);
}
function fallbackCopy(t,done){
  var ta=document.createElement("textarea");ta.value=t;ta.style.position="fixed";ta.style.opacity="0";
  document.body.appendChild(ta);ta.select();var ok=false;
  try{ok=document.execCommand("copy");}catch(e){}
  ta.remove();done(ok);
}

/* ---------- tabs ---------- */
var tabIdx=0;
var tabBtns=Array.prototype.slice.call(document.querySelectorAll(".tab"));
function setTab(i,focus){
  tabIdx=i;
  tabBtns.forEach(function(b,j){
    b.setAttribute("aria-selected",j===i?"true":"false");
    b.tabIndex=j===i?0:-1;
    $("panel"+j).hidden=j!==i;
  });
  $("rail").classList.toggle("rail-min",i>=2);
  if(focus)tabBtns[i].focus();
  renderActive();
}
tabBtns.forEach(function(b,i){
  b.addEventListener("click",function(){setTab(i,false);});
  b.addEventListener("keydown",function(e){
    if(e.key==="ArrowRight"){setTab((i+1)%4,true);e.preventDefault();}
    else if(e.key==="ArrowLeft"){setTab((i+3)%4,true);e.preventDefault();}
    else if(e.key==="Home"){setTab(0,true);e.preventDefault();}
    else if(e.key==="End"){setTab(3,true);e.preventDefault();}
  });
});

/* ---------- overview ---------- */
function topThemes(list,k){
  var m={};
  list.forEach(function(r){
    (r.themes||[]).forEach(function(t){
      if(!m[t])m[t]={theme:t,count:0,y0:r.year,y1:r.year};
      m[t].count++;
      if(typeof r.year==="number"){if(r.year<m[t].y0)m[t].y0=r.year;if(r.year>m[t].y1)m[t].y1=r.year;}
    });
  });
  return Object.keys(m).map(function(k){return m[k];}).sort(function(a,b){
    return b.count-a.count||a.theme.localeCompare(b.theme);
  }).slice(0,k);
}
function topStates(list,k){
  var m={};
  list.forEach(function(r){if(r._states)r._states.forEach(function(s){if(s!=="State not found")m[s]=(m[s]||0)+1;});});
  return Object.keys(m).map(function(s){return {state:s,count:m[s]};}).sort(function(a,b){
    return b.count-a.count||a.state.localeCompare(b.state);
  }).slice(0,k);
}

var chart1=null,chart2=null;
var endLabels={id:"endLabels",afterDatasetsDraw:function(chart){
  var meta=chart.getDatasetMeta(0);if(!meta||!meta.data)return;
  var ctx=chart.ctx;ctx.save();
  ctx.font="11px "+MONO;ctx.fillStyle="#1d1b18";ctx.textBaseline="middle";
  meta.data.forEach(function(bar,i){
    ctx.fillText(fmt(chart.data.datasets[0].data[i]),bar.x+6,bar.y);
  });
  ctx.restore();
}};

function ensureCharts(){
  if(chart1||!window.Chart)return;
  chart1=new Chart($("fig1"),{
    type:"bar",
    data:{labels:[],datasets:[{data:[],backgroundColor:"rgba(155,35,53,0.8)",borderWidth:0,maxBarThickness:26}]},
    options:{
      indexAxis:"y",responsive:true,maintainAspectRatio:false,
      onClick:function(e,els){
        if(els.length){
          var t=themeTop[els[0].index];
          if(t&&!F.themes.has(t.theme)){F.themes.add(t.theme);applyFilters();}
        }
      },
      plugins:{legend:{display:false},tooltip:{callbacks:{label:function(c){return " "+fmt(c.parsed.x)+" records";}}}},
      scales:{
        x:{beginAtZero:true,grid:{color:"#e4ddcd"},ticks:{font:{family:MONO,size:11}}},
        y:{grid:{display:false},ticks:{font:{family:MONO,size:11}}}
      }
    },
    plugins:[endLabels]
  });
  var mechs=Object.keys(MEC_COLORS).filter(function(m){return records.some(function(r){return r.mechanism===m;});});
  records.forEach(function(r){if(mechs.indexOf(r.mechanism)<0)mechs.push(r.mechanism);});
  chart2=new Chart($("fig2"),{
    type:"bar",
    data:{labels:[],datasets:mechs.map(function(m){return {label:m,data:[],backgroundColor:MEC_COLORS[m]||"#6b6459"};})},
    options:{
      responsive:true,maintainAspectRatio:false,
      plugins:{legend:{position:"top",labels:{usePointStyle:true,boxWidth:8,font:{family:MONO,size:11}}}},
      scales:{
        x:{stacked:true,grid:{display:false},ticks:{font:{family:MONO,size:11}}},
        y:{stacked:true,beginAtZero:true,grid:{color:"#e4ddcd"},ticks:{font:{family:MONO,size:11}}}
      }
    }
  });
}
function updateCharts(){
  if(!chart1)return;
  chart1.data.labels=themeTop.map(function(t){return t.theme;});
  chart1.data.datasets[0].data=themeTop.map(function(t){return t.count;});
  chart1.update();
  var yrs=[];for(var y=Y0;y<=Y1;y++)yrs.push(String(y));
  var fbyM={};
  filtered.forEach(function(r){(fbyM[r.mechanism]=fbyM[r.mechanism]||{})[r.year]=(fbyM[r.mechanism][r.year]||0)+1;});
  chart2.data.labels=yrs;
  chart2.data.datasets.forEach(function(ds){
    ds.data=yrs.map(function(ys){return (fbyM[ds.label]&&fbyM[ds.label][Number(ys)])||0;});
  });
  chart2.update();
}

function renderOverview(){
  var tc={};filtered.forEach(function(r){tc[r.type]=(tc[r.type]||0)+1;});
  var tb=Object.keys(tc).sort(function(a,b){return tc[b]-tc[a]||a.localeCompare(b);}).map(function(t){return fmt(tc[t])+" "+t;}).join(" \u00B7 ");
  var docsF=Object.keys(filtered.reduce(function(m,r){m[r.symbol]=1;return m;},{})).length;
  var fy=filtered.map(function(r){return r.year;}).filter(function(y){return typeof y==="number";});
  var fy0=fy.length?Math.min.apply(null,fy):null,fy1=fy.length?Math.max.apply(null,fy):null;
  var mechCounts={};records.forEach(function(r){mechCounts[r.mechanism]=(mechCounts[r.mechanism]||0)+1;});
  var mechs=Object.keys(mechCounts).sort(function(a,b){return mechCounts[b]-mechCounts[a]||a.localeCompare(b);});
  var tiles='';
  tiles+='<div class="tile"><div class="num">'+fmt(filtered.length)+'</div><div class="cap">records in view</div><div class="sub">'+(tb?esc(tb):"\u2014")+' \u00B7 of '+fmt(N)+' in the file</div><div class="how">How this is computed: count of records passing the left-rail filters; each record counted once and split by the UN\u2019s own type label.</div></div>';
  tiles+='<div class="tile"><div class="num">'+fmt(docsF)+'</div><div class="cap">documents</div><div class="sub">distinct symbols</div><div class="how">How this is computed: number of distinct symbol values among the filtered records.</div></div>';
  tiles+='<div class="tile"><div class="num">'+(fy0?fy0+"\u2013"+fy1:"\u2014")+'</div><div class="cap">years</div><div class="sub">dated by document</div><div class="how">How this is computed: minimum and maximum of the year field among the filtered records.</div></div>';
  mechs.forEach(function(m){
    var sub=filtered.filter(function(r){return r.mechanism===m;});
    var d=Object.keys(sub.reduce(function(mm,r){mm[r.symbol]=1;return mm;},{})).length;
    var ly=sub.length?Math.max.apply(null,sub.map(function(r){return r.year;})):"\u2014";
    var share=filtered.length?Math.round(100*sub.length/filtered.length):0;
    var dot='<i class="dot" style="background:'+(MEC_COLORS[m]||"#6b6459")+'"></i>';
    var extra=m==="Universal Periodic Review"?'<br><button type="button" class="linkbtn" id="statesToggle" aria-expanded="false">see the States</button><div id="statesBox" hidden></div>':'';
    tiles+='<div class="tile"><div class="cap">'+dot+esc(m)+'</div><div class="num">'+fmt(sub.length)+'</div><div class="sub">'+fmt(d)+' documents \u00B7 latest '+ly+' \u00B7 '+share+'% of filtered</div><div class="how">How this is computed: filtered records with mechanism = \u201C'+esc(m)+'\u201D; share = count \u00F7 '+fmt(filtered.length)+'.</div>'+extra+'</div>';
  });
  $("tiles").innerHTML=tiles;

  $("fig1title").textContent=filtered.length?("Ten most frequent themes among "+fmt(filtered.length)+" filtered records"):"No records match the current filters";
  $("fig1wrap").hidden=!themeTop.length;
  $("fig1none").hidden=!!themeTop.length;
  if(themeTop.length){
    $("fig1tab").innerHTML='<caption>The same ten themes as the bars above</caption><thead><tr><th scope="col">Theme</th><th scope="col" class="num">Records</th><th scope="col" class="num">% of filtered</th><th scope="col">Years</th></tr></thead><tbody>'+
      themeTop.map(function(t){
        return "<tr><td>"+esc(t.theme)+"</td><td class='num'>"+fmt(t.count)+"</td><td class='num'>"+(filtered.length?(100*t.count/filtered.length).toFixed(1):"0.0")+"%</td><td>"+t.y0+"\u2013"+t.y1+"</td></tr>";
      }).join("")+"</tbody>";
    $("fig1how").textContent="How this is computed: each theme of each filtered record counts once, so the bars add up to more than "+fmt(filtered.length)+"; ties are alphabetical. Click a bar to filter by that theme.";
  }else{
    $("fig1tab").innerHTML="";
    $("fig1how").textContent="How this is computed: each theme of each filtered record counts once; no records match, so there is nothing to count.";
  }
  $("fig1src").textContent="Source: WORKSHOP_DATA.uhri, themes field of "+fmt(filtered.length)+" filtered records (of "+fmt(N)+").";
  ensureCharts();
  updateCharts();
  $("fig2title").textContent="Records per year by mechanism \u2014 "+fmt(filtered.length)+" filtered records, "+Y0+"\u2013"+Y1;
  $("fig2how").textContent="How this is computed: records per year and per mechanism in the filtered set; every year from "+Y0+" to "+Y1+" appears, so empty years show as gaps.";
  $("fig2src").textContent="Source: WORKSHOP_DATA.uhri, year and mechanism fields of "+fmt(filtered.length)+" filtered records.";
}

$("tiles").addEventListener("click",function(e){
  if(e.target.id!=="statesToggle")return;
  var box=$("statesBox"),open=!box.hidden;
  box.hidden=open;e.target.setAttribute("aria-expanded",String(!open));
  if(!open){
    var upr=filtered.filter(function(r){return r.mechanism==="Universal Periodic Review";});
    var ts=topStates(upr,10);
    box.innerHTML='<div class="cap" style="margin:8px 0 2px">Ten States that made most recommendations to '+esc(country)+' \u2014 counts over the '+fmt(upr.length)+' UPR records in view</div>'+
      (ts.length?"<ol class='stateslist'>"+ts.map(function(s){return "<li>"+esc(s.state)+" \u2014 "+fmt(s.count)+"</li>";}).join("")+"</ol>":'<div class="hint">No States found in the current filter.</div>')+
      '<div class="how">How this is computed: parentheses at the end of each UPR text; a record counts once per State, so two States can co-sponsor one line.</div>';
  }
});

/* ---------- records tab ---------- */
var visible=50,sortAsc=false,expanded={};
function renderRecords(){
  var rows=filtered.slice().sort(function(a,b){
    var c=sortAsc?String(a.date||"").localeCompare(String(b.date||"")):String(b.date||"").localeCompare(String(a.date||""));
    if(c)return c;
    c=String(a.body||"").localeCompare(String(b.body||""));if(c)return c;
    c=a._paraNum-b._paraNum;if(c)return c;
    return a._i-b._i;
  });
  var shown=rows.slice(0,visible);
  $("reccap").textContent=fmt(shown.length)+" of "+fmt(rows.length)+" matching records shown \u00B7 "+(sortAsc?"oldest first":"newest first")+" \u00B7 click Date to reverse";
  $("thDate").textContent="Date "+(sortAsc?"\u25B4":"\u25BE");
  var h="";
  shown.forEach(function(r){
    var st=r._states?(r._states.length?r._states.join(", "):"State not found"):"\u2014";
    h+='<tr class="data" data-id="'+esc(r.id)+'" tabindex="0" aria-expanded="'+(expanded[r.id]?"true":"false")+'">'
      +"<td>"+esc(r.date||"")+"</td><td>"+esc(r.body||"")+"</td>"
      +'<td><a href="'+esc(r.doc_url||"#")+'" target="_blank" rel="noopener">'+esc(r.symbol||"")+'</a></td>'
      +"<td>"+(r._para?esc(r._para):"\u2013")+"</td>"
      +"<td>"+highlight(firstLine(r.text))+"</td>"
      +"<td>"+esc(st)+"</td></tr>";
    if(expanded[r.id]){
      h+='<tr class="detail" data-id="'+esc(r.id)+'"><td colspan="6">'
        +'<div class="para-big">'+(r._para?esc(r._para):"\u2013")+'</div>'
        +'<p class="fulltext">'+highlight(r.text)+'</p>'
        +'<div class="labels">'+labelsHtml(r)+'</div>'
        +'<div class="btnrow"><button type="button" class="btn copybtn" data-id="'+esc(r.id)+'">'+(r._para?"Copy citation":"Copy citation (no paragraph number in this extract)")+'</button>'
        +'<a class="btn" href="'+esc(r.doc_url||"#")+'" target="_blank" rel="noopener">Open the UN document</a></div>'
        +'</td></tr>';
    }
  });
  if(!shown.length)h='<tr><td colspan="6" class="nomatch">No records match the current filters.</td></tr>';
  $("recbody").innerHTML=h;
  $("moreBtn").hidden=shown.length>=rows.length;
}
function toggleRow(id){if(expanded[id])delete expanded[id];else expanded[id]=1;renderRecords();}
$("recbody").addEventListener("click",function(e){
  var cp=e.target.closest(".copybtn");
  if(cp){
    var id=cp.getAttribute("data-id");
    var r=records.filter(function(x){return x.id===id;})[0];
    if(r){
      var cite=r._para?r.symbol+", para. "+r._para:r.symbol;
      copyText(cite,function(ok){
        if(ok){var old=cp.textContent;cp.textContent="Copied \u2713";setTimeout(function(){cp.textContent=old;},2000);}
      });
    }
    return;
  }
  if(e.target.closest("a"))return;
  var tr=e.target.closest("tr.data");
  if(tr)toggleRow(tr.getAttribute("data-id"));
});
$("recbody").addEventListener("keydown",function(e){
  if((e.key==="Enter"||e.key===" ")&&e.target.classList&&e.target.classList.contains("data")){
    e.preventDefault();toggleRow(e.target.getAttribute("data-id"));
  }
});
$("thDate").addEventListener("click",function(){sortAsc=!sortAsc;renderRecords();});
$("moreBtn").addEventListener("click",function(){visible+=50;renderRecords();});

/* ---------- checks tab ---------- */
var checkResults=[];
function runChecks(){
  var res=[];
  var cntRaw=U.count,cnt=Number(U.count);
  res.push({name:"Record count",detail:"records.length = "+fmt(N)+" \u00B7 the file's own count field = "+esc(String(cntRaw))+" (as a number: "+cnt+")",status:N===cnt?"pass":"fail"});
  function sumBy(fn){var m={};records.forEach(function(r){var k=fn(r);m[k]=(m[k]||0)+1;});return Object.keys(m).reduce(function(a,k){return a+m[k];},0);}
  var sm=sumBy(function(r){return r.mechanism;}),sb=sumBy(function(r){return r.body;}),sy=sumBy(function(r){return r.year;});
  res.push({name:"Partitions",detail:"counts per mechanism sum to "+fmt(sm)+", per body to "+fmt(sb)+", per year to "+fmt(sy)+" \u2014 each should equal "+fmt(N),status:(sm===N&&sb===N&&sy===N)?"pass":"fail"});
  var st=sumBy(function(r){return r.type;});
  res.push({name:"Type partition",detail:"counts per type sum to "+fmt(st)+" against the headline "+fmt(N),status:st===N?"pass":"fail"});
  var alt={};filtered.forEach(function(r){(r.themes||[]).forEach(function(t){alt[t]=(alt[t]||0)+1;});});
  var altTop=Object.keys(alt).map(function(k){return [k,alt[k]];}).sort(function(a,b){return b[1]-a[1]||a[0].localeCompare(b[0]);}).slice(0,10);
  var ok4=themeTop.length===altTop.length;
  if(ok4)for(var i=0;i<themeTop.length;i++){if(themeTop[i].theme!==altTop[i][0]||themeTop[i].count!==altTop[i][1]){ok4=false;break;}}
  var largest=themeTop.length?themeTop[0].count:0;
  ok4=ok4&&largest<=filtered.length;
  res.push({name:"Chart against table",detail:"each FIG.01 bar recomputed by a second loop over the "+fmt(filtered.length)+" filtered records matches the ten table rows; largest bar "+fmt(largest)+" \u2264 "+fmt(filtered.length),status:ok4?"pass":"fail"});
  var bad=[];
  records.forEach(function(r){
    var ok=/^https:\/\/docs\.un\.org\//i.test(String(r.doc_url||""));
    if(ok){
      var u=String(r.doc_url),s=String(r.symbol);
      try{u=decodeURIComponent(u);}catch(e){}
      try{s=decodeURIComponent(s);}catch(e){}
      ok=s.length>0&&u.toLowerCase().lastIndexOf(s.toLowerCase())===u.length-s.length;
    }
    if(!ok)bad.push(r.symbol);
  });
  res.push({name:"Links",detail:bad.length?("records whose doc_url does not start with https://docs.un.org/ or does not end with its symbol: "+bad.slice(0,6).join(", ")+(bad.length>6?" (+"+(bad.length-6)+" more)":"")):("all "+fmt(N)+" doc_url values start with https://docs.un.org/ and end with their symbol (case-insensitive, decoded)"),status:bad.length?"fail":"pass"});
  var pm={};
  records.forEach(function(r){var m=r.mechanism;pm[m]=pm[m]||{t:0,p:0};pm[m].t++;if(r._para)pm[m].p++;});
  var det6=Object.keys(pm).map(function(m){return m+": "+Math.round(100*pm[m].p/pm[m].t)+"% with a number";}).join(" \u00B7 ");
  var upr=pm["Universal Periodic Review"];
  var warn6=upr&&upr.p<upr.t;
  res.push({name:"Paragraph numbers",detail:det6,status:warn6?"warn":"pass",note:warn6?"UPR below 100% \u2014 a warning, not an error":""});
  var uprRecs=records.filter(function(r){return r.mechanism==="Universal Periodic Review";});
  var noState=uprRecs.filter(function(r){return !r._states||!r._states.length||r._states[0]==="State not found";});
  res.push({name:"States found",detail:fmt(uprRecs.length-noState.length)+" of "+fmt(uprRecs.length)+" UPR records have at least one State"+(noState.length?" \u2014 without one: "+noState.slice(0,6).map(function(r){return r.symbol+" (\u201C\u2026"+String(r.text||"").slice(-50)+"\u201D)";}).join("; ")+(noState.length>6?" (+"+(noState.length-6)+" more)":""):"") ,status:noState.length?"warn":"pass"});
  var ids={};records.forEach(function(r){ids[r.id]=1;});
  var idc=Object.keys(ids).length;
  var tm={};records.forEach(function(r){var t=String(r.text||"");tm[t]=(tm[t]||0)+1;});
  var dups=Object.keys(tm).filter(function(t){return tm[t]>1;});
  var extra=0;dups.forEach(function(t){extra+=tm[t]-1;});
  var noTh=records.filter(function(r){return !r.themes||!r.themes.length;}).length;
  var noSdg=records.filter(function(r){return !r.sdgs||!r.sdgs.length;}).length;
  var noAp=records.filter(function(r){return !r.affected_persons||!r.affected_persons.length;}).length;
  res.push({name:"Duplicates and gaps",detail:"distinct id = "+fmt(idc)+" of "+fmt(N)+" \u00B7 duplicate texts: "+dups.length+" texts appear more than once ("+fmt(extra)+" extra records) \u00B7 not labelled: "+fmt(noTh)+" without themes, "+fmt(noSdg)+" without SDGs, "+fmt(noAp)+" without affected persons",status:idc!==N?"fail":(dups.length?"warn":"pass")});
  checkResults=res;
}
function renderChecks(){
  $("checks").innerHTML=checkResults.map(function(c){
    var mark=c.status==="pass?"\u2713 pass":c.status==="warn"?"\u26A0 warning":"\u2717 check failed";
    return '<div class="checkline"><span class="cname">'+esc(c.name)+'</span><span class="cdetail">'+esc(c.detail)+(c.note?" "+esc(c.note):"")+'</span><span class="st '+c.status+'">'+mark+'</span></div>';
  }).join("");
}

/* ---------- random sample ---------- */
var sampleSeed=1,sampleRecs=[],verdicts={},sampleDrawn=false,openCard=null;
function mulberry32(a){return function(){a|=0;a=a+0x6D2B79F5|0;var t=Math.imul(a^a>>>15,1|a);t=t+Math.imul(t^t>>>7,61|t)^t;return ((t^t>>>14)>>>0)/4294967296;};}
function drawSample(seed){
  sampleSeed=(seed>>>0)||1;
  var rng=mulberry32(sampleSeed);
  var n=filtered.length,k=Math.min(10,n);
  var idx={},list=[];
  while(list.length<k){var j=Math.floor(rng()*n);if(!idx[j]){idx[j]=1;list.push(filtered[j]);}}
  sampleRecs=list;verdicts={};openCard=null;
  renderSample();
}
function renderSample(){
  var f=0,d=0,u=0;
  sampleRecs.forEach(function(r){var v=verdicts[r.id];if(v==="fit")f++;else if(v==="dont")d++;else if(v==="unsure")u++;});
  $("tally").textContent="Themes: "+f+" fit \u00B7 "+d+" don't fit \u00B7 "+u+" unsure of "+sampleRecs.length+" judged \u00B7 seed "+sampleSeed+" \u2014 your judgement of the UN's labels; nothing is sent anywhere.";
  $("cards").innerHTML=sampleRecs.map(function(r){
    var open=openCard===r.id,v=verdicts[r.id]||"";
    return '<div class="card">'
      +'<button type="button" class="card-btn" data-id="'+esc(r.id)+'" aria-expanded="'+open+'"><span class="arr">'+(open?"\u25BE":"\u25B8")+'</span>'+esc(r.symbol)+' \u00B7 para '+(r._para?esc(r._para):"\u2013")+'</button>'
      +'<div class="card-panel"'+(open?"":" hidden")+'>'
      +'<p class="fulltext">'+esc(r.text)+'</p>'
      +'<div class="themechips">'+(r.themes&&r.themes.length?r.themes.map(function(t){return "<span>"+esc(t)+"</span>";}).join(""):'<span class="missing">not labelled</span>')+'</div>'
      +'<div class="vbtns">'
      +'<button type="button" class="vbtn'+(v==="fit"?" on":"")+'" data-id="'+esc(r.id)+'" data-v="fit">Fits</button>'
      +'<button type="button" class="vbtn'+(v==="dont"?" on":"")+'" data-id="'+esc(r.id)+'" data-v="dont">Doesn\'t fit</button>'
      +'<button type="button" class="vbtn'+(v==="unsure"?" on":"")+'" data-id="'+esc(r.id)+'" data-v="unsure">Unsure</button>'
      +'</div>'
      +'<div class="btnrow"><a class="btn" href="'+esc(r.doc_url||"#")+'" target="_blank" rel="noopener">Open the UN document</a></div>'
      +'</div></div>';
  }).join("");
}
$("cards").addEventListener("click",function(e){
  var vb=e.target.closest(".vbtn");
  if(vb){verdicts[vb.getAttribute("data-id")]=vb.getAttribute("data-v");renderSample();return;}
  var cb=e.target.closest(".card-btn");
  if(cb){var id=cb.getAttribute("data-id");openCard=(openCard===id?null:id);renderSample();}
});
$("drawBtn").addEventListener("click",function(){drawSample(Number($("seedBox").value)||1);});
$("drawAgain").addEventListener("click",function(){var s=Math.floor(Math.random()*100000)+1;$("seedBox").value=s;drawSample(s);});
$("drawSeed").addEventListener("click",function(){drawSample(Number($("seedBox").value)||1);});

/* ---------- method & export ---------- */
function renderMethod(){
  $("srcBlock").innerHTML="Data: <a href='"+esc(U.source_url||"#")+"' target='_blank' rel='noopener'>"+esc(U.source||"OHCHR Universal Human Rights Index")+"</a> \u00B7 "+fmt(N)+" records \u00B7 "+docCount+" documents \u00B7 "+Y0+"\u2013"+Y1+" \u00B7 built "+esc(U.built||"")+" \u00B7 dated by document.";
}
function csvEsc(v){v=String(v==null?"":v);return /[",\n]/.test(v)?'"'+v.replace(/"/g,'""')+'"':v;}
function buildCSV(){
  var lines=[];
  lines.push("# Country: "+country);
  lines.push("# Source: "+(U.source||"")+" \u2014 "+(U.source_url||""));
  lines.push("# Built: "+(U.built||""));
  var cl=chipList();
  lines.push("# Filters: "+(cl.length?cl.map(function(c){return c.label;}).join("; "):"none"));
  lines.push("# Rows: "+filtered.length+" of "+N);
  lines.push(["Date","Body","Mechanism","Type","Symbol","Document URL","Paragraph","Recommending State(s)","Section","Themes","SDGs","SDG targets","Affected persons","Text"].map(csvEsc).join(","));
  filtered.forEach(function(r){
    lines.push([r.date,r.body,r.mechanism,r.type,r.symbol,r.doc_url,r._para||"",(r._states?r._states.join("; "):""),r.section||"",(r.themes||[]).join("; "),(r.sdgs||[]).join("; "),(r.sdg_targets||[]).join("; "),(r.affected_persons||[]).join("; "),r.text||""].map(csvEsc).join(","));
  });
  return lines.join("\n");
}
function summaryText(){
  var tc={};filtered.forEach(function(r){tc[r.type]=(tc[r.type]||0)+1;});
  var tb=Object.keys(tc).sort(function(a,b){return tc[b]-tc[a];}).map(function(t){return fmt(tc[t])+" "+t;}).join(", ");
  var th=themeTop.length?themeTop:topThemes(filtered,10);
  var cl=chipList();
  return "UN human rights recommendations and observations: "+country+" \u2014 "+fmt(filtered.length)+" of "+fmt(N)+" records from "+docCount+" documents ("+Y0+"\u2013"+Y1+"), "+tb+". Top themes: "+th.map(function(t,i){return (i+1)+". "+t.theme+" ("+fmt(t.count)+")";}).join("; ")+". Source: "+(U.source||"OHCHR UHRI")+" (built "+(U.built||"")+"). Filters: "+(cl.length?cl.map(function(c){return c.label;}).join("; "):"none")+".";
}
$("csvBtn").addEventListener("click",function(){
  var blob=new Blob([buildCSV()],{type:"text/csv;charset=utf-8"});
  var a=document.createElement("a");
  a.href=URL.createObjectURL(blob);
  a.download="uhri-"+String(country).toLowerCase().replace(/[^a-z0-9]+/g,"-").replace(/^-+|-+$/g,"")+"-filtered.csv";
  document.body.appendChild(a);a.click();a.remove();
  setTimeout(function(){URL.revokeObjectURL(a.href);},2000);
  $("exportNote").textContent="CSV downloaded: "+fmt(filtered.length)+" rows of "+fmt(N)+", with the full text and labels, generated in your browser. Nothing was sent anywhere.";
});
$("sumBtn").addEventListener("click",function(){
  copyText(summaryText(),function(ok){
    $("exportNote").textContent=ok?"Summary copied to the clipboard \u2014 the only thing that left this page.":"Copy failed; please copy manually.";
  });
});

/* ---------- rail events ---------- */
document.querySelectorAll(".acc-btn").forEach(function(b){
  b.addEventListener("click",function(){
    var i=b.getAttribute("data-acc"),wasOpen=b.getAttribute("aria-expanded")==="true";
    document.querySelectorAll(".acc-btn").forEach(function(x){x.setAttribute("aria-expanded","false");});
    document.querySelectorAll(".acc-panel").forEach(function(x){x.hidden=true;});
    if(!wasOpen){b.setAttribute("aria-expanded","true");$("accp"+i).hidden=false;}
  });
});
var kwT=null;
function onKw(v){
  clearTimeout(kwT);
  kwT=setTimeout(function(){
    F.keyword=v.trim();
    if($("kw1").value!==v)$("kw1").value=v;
    if($("kw2").value!==v)$("kw2").value=v;
    applyFilters();
  },300);
}
$("kw1").addEventListener("input",function(){onKw(this.value);});
$("kw2").addEventListener("input",function(){onKw(this.value);});
$("fMech").addEventListener("change",function(){F.mechanism=this.value;F.body="all";fillBodyOptions();applyFilters();});
$("fBody").addEventListener("change",function(){F.body=this.value;applyFilters();});
$("fType").addEventListener("change",function(){F.type=this.value;applyFilters();});
$("fState").addEventListener("change",function(){F.state=this.value;applyFilters();});
$("fSdg").addEventListener("change",function(){F.sdg=this.value;applyFilters();});
function onYear(){
  var a=Number($("fY0").value),b=Number($("fY1").value);
  if(a>b){var t=a;a=b;b=t;$("fY0").value=String(a);$("fY1").value=String(b);}
  F.y0=a;F.y1=b;applyFilters();
}
$("fY0").addEventListener("change",onYear);
$("fY1").addEventListener("change",onYear);
$("chips").addEventListener("click",function(e){
  var b=e.target.closest(".chip");if(!b)return;
  var k=b.getAttribute("data-k");
  if(k==="keyword"){F.keyword="";$("kw1").value="";$("kw2").value="";}
  else if(k==="mechanism"){F.mechanism="all";fillMechOptions();F.body="all";fillBodyOptions();}
  else if(k==="body"){F.body="all";fillBodyOptions();}
  else if(k==="type"){F.type="all";fillTypeOptions();}
  else if(k==="state"){F.state="all";}
  else if(k==="years"){F.y0=Y0;F.y1=Y1;fillYearOptions();}
  else if(k==="sdg"){F.sdg="all";fillSdgOptions();}
  else if(k.indexOf("theme:")===0){F.themes.delete(k.slice(6));}
  applyFilters();
});
$("clearAll").addEventListener("click",function(){
  F.keyword="";F.mechanism="all";F.body="all";F.type="all";F.state="all";F.themes.clear();F.y0=Y0;F.y1=Y1;F.sdg="all";
  $("kw1").value="";$("kw2").value="";
  fillMechOptions();fillBodyOptions();fillTypeOptions();fillYearOptions();fillSdgOptions();fillStateOptions();
  applyFilters();
});

/* ---------- render pipeline ---------- */
function renderActive(){
  if(tabIdx===0)renderOverview();
  else if(tabIdx===1)renderRecords();
  else if(tabIdx===2){renderChecks();if(!sampleDrawn){sampleDrawn=true;drawSample(Number($("seedBox").value)||1);}else renderSample();}
  else renderMethod();
}
function applyFilters(){
  filtered=records.filter(function(r){return matches(r);});
  themeTop=topThemes(filtered,10);
  visible=50;
  runChecks();
  renderRail();
  renderActive();
}

/* ---------- init ---------- */
$("kicker").textContent="UHRI \u00B7 "+String(country).toUpperCase();
$("title").textContent="UN human rights recommendations and observations: "+country;
$("meta").innerHTML='<a href="'+esc(U.source_url||"#")+'" target="_blank" rel="noopener">'+esc(U.source||"source")+'</a> \u00B7 '+fmt(N)+' records \u00B7 '+docCount+' documents \u00B7 '+Y0+'\u2013'+Y1+' \u00B7 built '+esc(U.built||"")+' \u00B7 dated by document';
$("foot").innerHTML='Built on OHCHR UHRI data \u00B7 '+fmt(N)+' records \u00B7 <a href="'+esc(U.source_url||"#")+'" target="_blank" rel="noopener">'+esc(U.source||"source")+'</a>';
document.title="UHRI \u00B7 "+country+" \u2014 UN recommendations dashboard";
fillMechOptions();fillBodyOptions();fillTypeOptions();fillYearOptions();fillSdgOptions();fillStateOptions();
themeTop=topThemes(records,10);
runChecks();
setTab(0,false);
})();
</script>
</body>
</html>
```