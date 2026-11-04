Built the four-tab UHRI dashboard on the attached file: overview with the theme chart and year timeline, the records table with in-place expansion and citation copying, the self-check panel with the seeded random label sample, and method + CSV export. Every number is computed in the browser from `WORKSHOP_DATA.uhri`, and the country is read from the data, never hard-coded.

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>UHRI dashboard</title>
<style>
:root{--paper:#f4f0e8;--ink:#1d1b18;--rule:#d9d2c3;--red:#9b2335;--muted:#57534a;}
*{box-sizing:border-box}
[hidden]{display:none!important}
html{margin:0}
body{margin:0;background:var(--paper);color:var(--ink);font:16px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;}
a{color:var(--ink);text-decoration:underline;text-decoration-color:var(--rule);text-underline-offset:2px}
a:hover{text-decoration-color:var(--red)}
:focus-visible{outline:3px solid var(--red);outline-offset:2px}
.wrap{max-width:1180px;margin:0 auto;padding:0 20px}
header{padding:30px 0 0}
.kicker{font:11px/1 ui-monospace,Menlo,Consolas,monospace;letter-spacing:.16em;text-transform:uppercase;color:var(--red)}
h1{font-family:Georgia,"Times New Roman",serif;font-weight:400;font-size:34px;line-height:1.18;margin:10px 0 8px;max-width:26em}
.meta{font:12px/1.7 ui-monospace,Menlo,Consolas,monospace;color:var(--muted);margin:0}
.tabs{display:flex;flex-wrap:wrap;gap:2px;border-bottom:1px solid var(--rule);margin-top:16px}
.tabs [role=tab]{font:12px/1 ui-monospace,Menlo,Consolas,monospace;letter-spacing:.12em;text-transform:uppercase;background:none;border:none;border-bottom:3px solid transparent;padding:12px 14px 11px;cursor:pointer;color:var(--muted)}
.tabs [role=tab]:hover{color:var(--ink)}
.tabs [role=tab][aria-selected=true]{color:var(--red);border-bottom-color:var(--red)}
.layout{display:grid;grid-template-columns:272px minmax(0,1fr);gap:40px;align-items:start;padding:24px 0 70px}
.rail{position:sticky;top:14px}
.railhead{display:flex;justify-content:space-between;align-items:baseline;font:11px/1 ui-monospace,Menlo,Consolas,monospace;letter-spacing:.16em;text-transform:uppercase;color:var(--muted)}
.mini{font:11px/1 ui-monospace,Menlo,Consolas,monospace;letter-spacing:.08em;text-transform:uppercase;background:none;border:none;color:var(--red);cursor:pointer;padding:2px 0;text-decoration:underline;text-underline-offset:2px}
.matchnum{font-family:Georgia,"Times New Roman",serif;font-size:54px;line-height:1;margin:12px 0 3px}
.matchsub{font:11px/1.5 ui-monospace,Menlo,Consolas,monospace;color:var(--muted)}
.sharebar{height:4px;background:var(--rule);margin:10px 0 12px}
.sharebar i{display:block;height:100%;background:var(--red);width:0}
.chips{display:flex;flex-wrap:wrap;gap:6px;margin:0 0 14px}
.chip{font:11px/1 ui-monospace,Menlo,Consolas,monospace;border:1px solid var(--red);color:var(--red);background:none;padding:5px 8px;cursor:pointer;border-radius:2px}
.chip:hover{background:rgba(155,35,53,.08)}
.acc{border-top:1px solid var(--rule)}
.accbtn{width:100%;display:flex;justify-content:space-between;align-items:center;background:none;border:none;border-bottom:1px solid var(--rule);padding:13px 2px;cursor:pointer;font:12px/1 ui-monospace,Menlo,Consolas,monospace;letter-spacing:.12em;text-transform:uppercase;color:var(--ink);text-align:left}
.accbtn .chev{color:var(--muted)}
.accbody{border-bottom:1px solid var(--rule);padding:12px 2px 16px}
.hint{font:11px/1.6 ui-monospace,Menlo,Consolas,monospace;color:var(--muted);margin:6px 0 0}
input[type=text],input[type=number],select{width:100%;background:#fffdf8;border:1px solid var(--rule);padding:8px 10px;font:14px/1.4 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;color:var(--ink);border-radius:0}
input:focus,select:focus{border-color:var(--red)}
label.f{display:block;font:10px/1 ui-monospace,Menlo,Consolas,monospace;letter-spacing:.12em;text-transform:uppercase;color:var(--muted);margin:14px 0 5px}
.accbody label.f:first-child{margin-top:0}
.sect{font:12px/1 ui-monospace,Menlo,Consolas,monospace;letter-spacing:.14em;text-transform:uppercase;color:var(--muted);margin:34px 0 10px}
.sect:first-child{margin-top:0}
.tiles{display:flex;flex-wrap:wrap;gap:40px}
.tile .big{font-family:Georgia,"Times New Roman",serif;font-size:48px;line-height:1}
.tile .sub{font-size:14px;margin-top:7px;max-width:38ch}
.how{font:11px/1.6 ui-monospace,Menlo,Consolas,monospace;color:var(--muted);margin-top:7px;max-width:42ch}
.mechtiles{display:flex;flex-wrap:wrap;gap:32px;margin-top:22px;padding-top:18px;border-top:1px solid var(--rule)}
.mech .mname{font:12px/1.4 ui-monospace,Menlo,Consolas,monospace;letter-spacing:.1em;text-transform:uppercase}
.mech .dot{display:inline-block;width:10px;height:10px;border-radius:50%;margin-right:8px}
.mech .mnum{font-family:Georgia,"Times New Roman",serif;font-size:34px;line-height:1;margin-top:8px}
.mech .msub{font-size:13px;color:var(--muted);margin-top:5px;max-width:32ch}
.linkbtn{background:none;border:none;padding:0;font:11px/1 ui-monospace,Menlo,Consolas,monospace;letter-spacing:.08em;text-transform:uppercase;color:var(--red);cursor:pointer;text-decoration:underline;text-underline-offset:2px;margin-top:7px}
.statesbox{margin-top:16px;border-top:1px solid var(--rule);padding-top:12px}
.statesbox h3{font-family:Georgia,"Times New Roman",serif;font-weight:400;font-size:19px;margin:0 0 8px}
.statesbox ol{margin:0;padding-left:22px;font-size:14px}
figure{margin:40px 0 0}
.figtitle{font-family:Georgia,"Times New Roman",serif;font-weight:400;font-size:22px;line-height:1.3;margin:0 0 5px;max-width:44em}
.figsrc{font:11px/1.6 ui-monospace,Menlo,Consolas,monospace;color:var(--muted);margin:0 0 14px;max-width:72em}
.chartbox{height:360px;position:relative}
.chartbox.small{height:320px}
.norecords{font-size:15px;color:var(--muted);padding:26px 0;border-top:1px solid var(--rule);border-bottom:1px solid var(--rule)}
table{width:100%;border-collapse:collapse;margin:12px 0 6px;font-size:15px}
caption{text-align:left;font:11px/1.6 ui-monospace,Menlo,Consolas,monospace;letter-spacing:.08em;text-transform:uppercase;color:var(--muted);padding:0 0 8px;border-bottom:1px solid var(--ink)}
th{font:11px/1.4 ui-monospace,Menlo,Consolas,monospace;letter-spacing:.1em;text-transform:uppercase;color:var(--muted);text-align:left;padding:9px 12px 9px 0;border-bottom:1px solid var(--ink);font-weight:400;vertical-align:bottom}
td{padding:9px 12px 9px 0;border-bottom:1px solid var(--rule);vertical-align:top}
th.num,td.num{text-align:right}
.thbtn{background:none;border:none;padding:0;font:inherit;letter-spacing:inherit;text-transform:inherit;color:inherit;cursor:pointer;text-decoration:underline;text-underline-offset:2px}
tbody tr.data{cursor:pointer}
tbody tr.data:hover td{background:rgba(155,35,53,.05)}
td.firstline{max-width:34em}
tr.detail td{background:#ede7d9;padding:18px 20px}
.paranum{font-family:Georgia,"Times New Roman",serif;font-size:30px;color:var(--red);margin-bottom:10px}
.fulltext{max-width:78ch;white-space:pre-wrap;margin:0 0 14px}
.labels div{margin:5px 0;font-size:14px}
.lbl{font:10px/1 ui-monospace,Menlo,Consolas,monospace;letter-spacing:.12em;text-transform:uppercase;color:var(--muted);margin-right:10px}
.missing{color:#8a8375;font-style:italic}
.tagchip{display:inline-block;border:1px solid var(--rule);padding:2px 8px;margin:2px 4px 2px 0;font-size:12.5px;border-radius:2px;background:#fffdf8}
mark{background:rgba(155,35,53,.22);color:inherit;padding:0 1px}
.rowactions{display:flex;align-items:center;gap:10px;margin-top:14px;flex-wrap:wrap}
.btn{font:12px/1 ui-monospace,Menlo,Consolas,monospace;letter-spacing:.1em;text-transform:uppercase;background:none;border:1px solid var(--rule);color:var(--ink);padding:9px 14px;cursor:pointer;border-radius:2px;text-decoration:none;display:inline-block}
.btn:hover{border-color:var(--ink)}
.btn.primary{border-color:var(--red);color:var(--red)}
.btn.primary:hover{background:rgba(155,35,53,.08)}
.btn[aria-pressed=true]{background:var(--red);border-color:var(--red);color:var(--paper)}
.copied{font:11px/1 ui-monospace,Menlo,Consolas,monospace;color:var(--red)}
.searchrow{margin-bottom:6px}
.searchrow input{font-size:16px}
.check{display:flex;gap:12px;padding:10px 0;border-bottom:1px solid var(--rule);font-size:14px}
.check .mark{font-family:ui-monospace,Menlo,Consolas,monospace;flex:none}
.check .what{font:11px/1.5 ui-monospace,Menlo,Consolas,monospace;letter-spacing:.1em;text-transform:uppercase;color:var(--muted)}
.check.fail .mark,.check.fail .failtxt{color:var(--red);font-weight:700}
.check.warn .mark{color:var(--red)}
.failures{font:12px/1.7 ui-monospace,Menlo,Consolas,monospace;color:var(--muted);word-break:break-all}
.samplectl{display:flex;align-items:flex-end;gap:14px;flex-wrap:wrap;margin:8px 0 14px}
.samplectl label.f{margin:0;display:flex;align-items:center;gap:8px}
.samplectl input{width:100px}
.tally{font:12px/1.6 ui-monospace,Menlo,Consolas,monospace;margin:0 0 10px}
.samplecard{border-bottom:1px solid var(--rule)}
.samplebtn{width:100%;display:flex;justify-content:space-between;gap:12px;text-align:left;background:none;border:none;padding:11px 2px;cursor:pointer;font:13px/1.4 ui-monospace,Menlo,Consolas,monospace;color:var(--ink)}
.samplebtn:hover{color:var(--red)}
.samplebody{padding:2px 2px 18px}
.verdicts{display:flex;gap:8px;margin-top:12px;flex-wrap:wrap}
.method{margin:0;padding-left:22px;max-width:74ch}
.method li{margin:0 0 10px}
.srcblock{font-size:14px;max-width:74ch}
footer{position:sticky;bottom:0;background:var(--paper);border-top:1px solid var(--rule);padding:9px 0 10px;font:11px/1.7 ui-monospace,Menlo,Consolas,monospace;color:var(--muted)}
footer a{color:inherit}
.credits{opacity:.85}
@media (max-width:920px){
  .layout{grid-template-columns:1fr;gap:20px}
  .rail{position:static}
  h1{font-size:27px}
}
</style>
</head>
<body>
<header class="wrap">
  <div class="kicker" id="kicker">UHRI</div>
  <h1 id="title"></h1>
  <p class="meta" id="meta"></p>
  <nav class="tabs" role="tablist" aria-label="Dashboard sections" id="tablist">
    <button role="tab" id="tab-0" aria-controls="panel-0" aria-selected="true">01 Overview</button>
    <button role="tab" id="tab-1" aria-controls="panel-1" aria-selected="false" tabindex="-1">02 Records</button>
    <button role="tab" id="tab-2" aria-controls="panel-2" aria-selected="false" tabindex="-1">03 Check</button>
    <button role="tab" id="tab-3" aria-controls="panel-3" aria-selected="false" tabindex="-1">04 Method &amp; export</button>
  </nav>
</header>
<div class="wrap layout">
  <aside class="rail" aria-label="Filters">
    <div class="railhead"><span>Filters</span><button class="mini" id="clearAll" type="button">Clear all</button></div>
    <div class="matchnum" id="matchNum" aria-live="polite">–</div>
    <div class="matchsub" id="matchSub"></div>
    <div class="sharebar" aria-hidden="true"><i id="shareFill"></i></div>
    <div class="chips" id="chips"></div>
    <div id="accWrap">
      <div class="acc">
        <button class="accbtn" type="button" data-acc="kw" aria-expanded="true" aria-controls="acc-kw"><span>01 Keyword</span><span class="chev" aria-hidden="true">▾</span></button>
        <div class="accbody" id="acc-kw">
          <input type="text" id="kw1" placeholder="e.g. torture" aria-label="Keyword search">
          <p class="hint">literal match, not synonyms · every word must appear in the text or symbol · applied 300 ms after typing</p>
        </div>
      </div>
      <div class="acc">
        <button class="accbtn" type="button" data-acc="mech" aria-expanded="false" aria-controls="acc-mech"><span>02 Mechanism, body, type</span><span class="chev" aria-hidden="true">▾</span></button>
        <div class="accbody" id="acc-mech" hidden>
          <label class="f" for="selMech">Mechanism</label>
          <select id="selMech"></select>
          <label class="f" for="selBody">Body or mandate</label>
          <select id="selBody"></select>
          <label class="f" for="selType">Type</label>
          <select id="selType"></select>
          <label class="f" for="selState">Recommending State (UPR only)</label>
          <select id="selState"></select>
        </div>
      </div>
      <div class="acc">
        <button class="accbtn" type="button" data-acc="yr" aria-expanded="false" aria-controls="acc-yr"><span>03 Years and SDG</span><span class="chev" aria-hidden="true">▾</span></button>
        <div class="accbody" id="acc-yr" hidden>
          <label class="f" for="selYf">Year from</label>
          <select id="selYf"></select>
          <label class="f" for="selYt">Year to</label>
          <select id="selYt"></select>
          <label class="f" for="selSdg">SDG</label>
          <select id="selSdg"></select>
        </div>
      </div>
    </div>
  </aside>
  <main>
    <section id="panel-0" role="tabpanel" aria-labelledby="tab-0">
      <div class="tiles" id="tiles"></div>
      <div class="mechtiles" id="mechTiles"></div>
      <div class="statesbox" id="statesBox" hidden></div>
      <figure>
        <figcaption>
          <p class="figtitle" id="fig1Title"></p>
          <p class="figsrc" id="fig1Src"></p>
        </figcaption>
        <div class="chartbox" id="fig1Box"><canvas id="chart1" aria-label="Bar chart of the ten most frequent themes"></canvas></div>
        <div class="norecords" id="fig1Empty" hidden>No records match the current filters.</div>
        <table id="fig1Table">
          <caption>FIG.01 data — the same ten rows as the chart</caption>
          <thead><tr><th>Theme</th><th class="num">Records</th><th class="num">% of filtered</th><th>Years</th></tr></thead>
          <tbody id="fig1Body"></tbody>
        </table>
        <p class="hint" id="fig1Note"></p>
      </figure>
      <figure>
        <figcaption>
          <p class="figtitle" id="fig2Title"></p>
          <p class="figsrc" id="fig2Src"></p>
        </figcaption>
        <div class="chartbox small" id="fig2Box"><canvas id="chart2" aria-label="Stacked bar chart of records per year by mechanism"></canvas></div>
        <div class="norecords" id="fig2Empty" hidden>No records match the current filters.</div>
      </figure>
    </section>
    <section id="panel-1" role="tabpanel" aria-labelledby="tab-1" hidden>
      <div class="searchrow">
        <input type="text" id="kw2" aria-label="Keyword search, same as the filter in the left rail">
        <p class="hint">literal match, not synonyms · same box as 01 Keyword in the filters</p>
      </div>
      <table id="recTable">
        <caption id="recCaption"></caption>
        <thead><tr>
          <th><button class="thbtn" type="button" id="dateSort">Date <span id="dateArrow" aria-hidden="true">↓ newest first</span></button></th>
          <th>Body</th><th>Symbol</th><th>Para.</th><th>First line</th><th>Recommending State</th>
        </tr></thead>
        <tbody id="recBody"></tbody>
      </table>
      <div class="norecords" id="recEmpty" hidden>No records match the current filters.</div>
      <p><button class="btn" type="button" id="showMore">Show 50 more</button></p>
    </section>
    <section id="panel-2" role="tabpanel" aria-labelledby="tab-2" hidden>
      <h2 class="sect">Check this dashboard — how the app checks itself</h2>
      <p class="hint">Each line compares two values computed in this page. Failures are shown in red, never hidden.</p>
      <div id="checkList"></div>
      <h2 class="sect">Random-sample label check</h2>
      <p class="hint">This is your judgement of the UN's labels; nothing is sent anywhere.</p>
      <div class="samplectl">
        <button class="btn primary" type="button" id="drawBtn">Check 10 at random</button>
        <label class="f" for="seedBox">Seed <input type="number" id="seedBox" value="1" min="0" step="1"></label>
        <button class="btn" type="button" id="drawSeed">Draw with this seed</button>
        <button class="btn" type="button" id="drawAgain">Draw again</button>
      </div>
      <p class="tally" id="tally"></p>
      <div id="sampleList"></div>
    </section>
    <section id="panel-3" role="tabpanel" aria-labelledby="tab-3" hidden>
      <h2 class="sect">How each number is computed</h2>
      <ol class="method">
        <li>Every number on this page is computed in your browser by looping over the records of the attached UHRI file. Nothing is estimated, and no model, server or network request is involved.</li>
        <li>The headline count is the number of records passing all filters; documents are the distinct <em>symbol</em> values; years are the minimum and maximum of <em>year</em> among those records.</li>
        <li>Filters combine with AND: every keyword word must appear literally in the text or the symbol; mechanism, body, type and recommending State match exactly; years are inclusive between the two selects; an SDG matches when its goal number is in the record's <em>sdgs</em> list; a theme matches when the record carries it.</li>
        <li>Paragraph numbers are read from the first number at the start of the text (for example “71.” or “144.43”); recommending States are read from the trailing parentheses of UPR records only, never from treaty-body texts.</li>
        <li>Theme counts count each theme once per record, so the ten bars add up to more than the record count; percentages are shares of the filtered records, not of labels.</li>
        <li>The CSV export contains exactly the filtered records, with the columns you see on the Records tab plus the full text and all labels, generated in the browser.</li>
      </ol>
      <h2 class="sect">Take it with you</h2>
      <p>
        <button class="btn primary" type="button" id="csvBtn">Download CSV of the current filter</button>
        <button class="btn" type="button" id="sumBtn">Copy summary</button>
        <span class="copied" id="sumCopied" hidden>Copied ✓</span>
      </p>
      <p class="hint">The CSV starts with comment lines (country, source, build date, filters, row count) and is generated in the browser with a Blob URL. Copy summary writes plain text to the clipboard — the only thing that leaves the page.</p>
      <h2 class="sect">Source</h2>
      <p class="srcblock" id="srcLine"></p>
    </section>
  </main>
</div>
<footer>
  <div class="wrap" id="footLine"></div>
  <div class="wrap credits">Credits: chart and table practice after UK Government Analysis Function guidance (data visualisation: charts; tables); citation form after Dag Hammarskjöld Library Ask DAG; data practice after the OHCHR guidance note A Human Rights-Based Approach to Data.</div>
</footer>
<script>
(function(){
"use strict";
var D = window.WORKSHOP_DATA.uhri;
var COUNTRY = D.country || "the participant country";
var SDG_NAMES = D.sdg_names || {};
var BUILT = D.built || "unknown";
var SOURCE = D.source || "OHCHR Universal Human Rights Index";
var SOURCE_URL = D.source_url || "";

/* ---------- helpers ---------- */
function $(s, el){ return (el || document).querySelector(s); }
function esc(s){ return String(s == null ? "" : s).replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;").replace(/"/g,"&quot;"); }
function fmt(n){ return Number(n).toLocaleString("en-GB"); }
function countBy(list, fn){ var o = {}; list.forEach(function(x){ var k = fn(x); o[k] = (o[k] || 0) + 1; }); return o; }
function mulberry32(a){ return function(){ a |= 0; a = a + 0x6D2B79F5 | 0; var t = Math.imul(a ^ a >>> 15, 1 | a); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; }
function copyText(t, done){
  if (navigator.clipboard && navigator.clipboard.writeText){ navigator.clipboard.writeText(t).then(done, function(){ fallbackCopy(t, done); }); }
  else fallbackCopy(t, done);
}
function fallbackCopy(t, done){
  var ta = document.createElement("textarea"); ta.value = t; ta.style.position = "fixed"; ta.style.opacity = "0";
  document.body.appendChild(ta); ta.select();
  try { document.execCommand("copy"); } catch(e){}
  document.body.removeChild(ta); done();
}

/* ---------- prepare records ---------- */
var RECS = D.records;
var byId = {};
RECS.forEach(function(r, i){
  r._i = i;
  var m = /^(\d{1,3}(?:\.\d{1,3})?)\.?\s/.exec(r.text || "");
  r._para = m ? m[1] : null;
  r._states = [];
  if (r.mechanism === "Universal Periodic Review"){
    var run = /((?:\s*\((?:[^()]|\([^()]*\))*\))+)\s*[;.]?\s*$/.exec(r.text || "");
    if (run){
      var groups = run[1].match(/\((?:[^()]|\([^()]*\))*\)/g) || [];
      var names = groups.map(function(g){ return g.slice(1, -1).trim(); });
      var bad = names.some(function(n){ return n.indexOf(",") !== -1 || n.length > 60; });
      r._states = bad ? ["State not found"] : names;
    }
  }
  var t = String(r.text || "");
  if (t.length <= 120) r._first = t;
  else { var c = t.slice(0, 120); var sp = c.lastIndexOf(" "); if (sp > 0) c = c.slice(0, sp); r._first = c + "…"; }
  byId[r.id] = r;
});
var YEARS = Array.from(new Set(RECS.map(function(r){ return r.year; }))).sort(function(a,b){ return a-b; });
var FILE_YMIN = YEARS[0], FILE_YMAX = YEARS[YEARS.length - 1];
var MECHS = Array.from(new Set(RECS.map(function(r){ return r.mechanism; })));
var MEC_COLORS = { "Universal Periodic Review": "#c2410c", "Treaty bodies": "#0f766e", "Special Procedures": "#7c3aed" };
var BY_MECH = countBy(RECS, function(r){ return r.mechanism; });
var BY_TYPE = countBy(RECS, function(r){ return r.type; });
var BY_STATE = {};
RECS.forEach(function(r){
  if (r.mechanism === "Universal Periodic Review"){
    r._states.forEach(function(s){ if (s !== "State not found") BY_STATE[s] = (BY_STATE[s] || 0) + 1; });
  }
});
var SDG_SET = new Set();
RECS.forEach(function(r){ (r.sdgs || []).forEach(function(g){ SDG_SET.add(g); }); });

/* ---------- state ---------- */
var state = {
  tab: 0, sortAsc: false, shown: 50, openAcc: "kw",
  filters: { keyword: "", mechanism: "all", body: "all", type: "all", state: "all", theme: "all", yf: FILE_YMIN, yt: FILE_YMAX, sdg: "all" },
  expanded: new Set(), showStates: false,
  sampleSeed: 1, sampleIds: null, sampleOpen: null, verdicts: {}
};

/* ---------- filtering ---------- */
function filtered(){
  var f = state.filters;
  var words = f.keyword.trim().toLowerCase().split(/\s+/).filter(Boolean);
  var yf = Number(f.yf), yt = Number(f.yt);
  if (yf > yt){ var t = yf; yf = yt; yt = t; }
  return RECS.filter(function(r){
    if (f.mechanism !== "all" && r.mechanism !== f.mechanism) return false;
    if (f.body !== "all" && r.body !== f.body) return false;
    if (f.type !== "all" && r.type !== f.type) return false;
    if (f.state !== "all" && r._states.indexOf(f.state) === -1) return false;
    if (f.theme !== "all" && (r.themes || []).indexOf(f.theme) === -1) return false;
    if (f.sdg !== "all" && (r.sdgs || []).indexOf(Number(f.sdg)) === -1) return false;
    if (r.year < yf || r.year > yt) return false;
    if (words.length){
      var hay = (r.text + " " + r.symbol).toLowerCase();
      for (var i = 0; i < words.length; i++){ if (hay.indexOf(words[i]) === -1) return false; }
    }
    return true;
  });
}
function themeStats(f){
  var m = {};
  f.forEach(function(r){
    (r.themes || []).forEach(function(t){
      var e = m[t] || (m[t] = { count: 0, ymin: r.year, ymax: r.year });
      e.count++; if (r.year < e.ymin) e.ymin = r.year; if (r.year > e.ymax) e.ymax = r.year;
    });
  });
  return Object.keys(m).map(function(t){ var e = m[t]; return { theme: t, count: e.count, ymin: e.ymin, ymax: e.ymax }; })
    .sort(function(a, b){ return b.count - a.count || a.theme.localeCompare(b.theme); });
}
function hi(text){
  var words = state.filters.keyword.trim().toLowerCase().split(/\s+/).filter(Boolean);
  if (!words.length) return esc(text);
  var rx = new RegExp("(" + words.map(function(w){ return w.replace(/[.*+?^${}()|[\]\\]/g, "\\$&"); }).join("|") + ")", "gi");
  return String(text).split(rx).map(function(p){
    if (!p) return "";
    var low = p.toLowerCase();
    return words.some(function(w){ return low.indexOf(w) !== -1; }) ? "<mark>" + esc(p) + "</mark>" : esc(p);
  }).join("");
}
function filterDesc(){
  var f = state.filters, parts = [];
  if (f.keyword.trim()) parts.push('keyword "' + f.keyword.trim() + '"');
  if (f.mechanism !== "all") parts.push("mechanism=" + f.mechanism);
  if (f.body !== "all") parts.push("body=" + f.body);
  if (f.type !== "all") parts.push("type=" + f.type);
  if (f.state !== "all") parts.push("state=" + f.state);
  if (f.theme !== "all") parts.push("theme=" + f.theme);
  if (Number(f.yf) !== FILE_YMIN || Number(f.yt) !== FILE_YMAX) parts.push("years " + f.yf + "–" + f.yt);
  if (f.sdg !== "all") parts.push("SDG " + f.sdg);
  return parts.length ? parts.join("; ") : "none (all records)";
}

/* ---------- rail ---------- */
function fillSelect(el, opts, cur){
  var sig = opts.map(function(o){ return String(o.v); }).join("\u0001");
  if (el.dataset.sig !== sig){
    el.dataset.sig = sig;
    el.innerHTML = opts.map(function(o){ return '<option value="' + esc(o.v) + '">' + esc(o.label) + "</option>"; }).join("");
  }
  if (cur != null && opts.some(function(o){ return String(o.v) === String(cur); })) el.value = String(cur);
  else el.value = String(opts[0].v);
  return el.value;
}
function renderRail(){
  var f = state.filters;
  var m = filtered().length, all = RECS.length;
  $("#matchNum").textContent = fmt(m);
  $("#matchSub").textContent = "matching records · of " + fmt(all) + " in the file";
  $("#shareFill").style.width = (all ? Math.max(0, 100 * m / all) : 0) + "%";
  var chips = [];
  if (f.keyword.trim()) chips.push({ k: "keyword", label: 'Keyword "' + f.keyword.trim() + '"' });
  if (f.mechanism !== "all") chips.push({ k: "mechanism", label: "Mechanism: " + f.mechanism });
  if (f.body !== "all") chips.push({ k: "body", label: "Body: " + f.body });
  if (f.type !== "all") chips.push({ k: "type", label: "Type: " + f.type });
  if (f.state !== "all") chips.push({ k: "state", label: "State: " + f.state });
  if (f.theme !== "all") chips.push({ k: "theme", label: "Theme: " + f.theme });
  if (Number(f.yf) !== FILE_YMIN || Number(f.yt) !== FILE_YMAX) chips.push({ k: "years", label: "Years: " + f.yf + "–" + f.yt });
  if (f.sdg !== "all") chips.push({ k: "sdg", label: "SDG: " + f.sdg });
  var cb = $("#chips"); cb.innerHTML = "";
  chips.forEach(function(c){
    var b = document.createElement("button"); b.type = "button"; b.className = "chip";
    b.textContent = c.label + "  ×"; b.setAttribute("aria-label", "Remove filter " + c.label);
    b.addEventListener("click", function(){ resetFilter(c.k); });
    cb.appendChild(b);
  });
  $("#accWrap").hidden = state.tab >= 2;
  Array.prototype.forEach.call(document.querySelectorAll(".accbtn"), function(btn){
    var open = state.openAcc === btn.dataset.acc;
    btn.setAttribute("aria-expanded", open ? "true" : "false");
    btn.querySelector(".chev").textContent = open ? "▴" : "▾";
    $("#acc-" + btn.dataset.acc).hidden = !open;
  });
  var mechOpts = [{ v: "all", label: "All mechanisms (" + fmt(all) + ")" }].concat(
    MECHS.map(function(m){ return { v: m, label: m + " (" + fmt(BY_MECH[m] || 0) + ")" }; }));
  f.mechanism = fillSelect($("#selMech"), mechOpts, f.mechanism);
  var scope = f.mechanism === "all" ? RECS : RECS.filter(function(r){ return r.mechanism === f.mechanism; });
  var scopeBody = countBy(scope, function(r){ return r.body; });
  var bodyOpts = [{ v: "all", label: "All bodies (" + fmt(scope.length) + ")" }].concat(
    Object.keys(scopeBody).sort().map(function(b){ return { v: b, label: b + " (" + fmt(scopeBody[b]) + ")" }; }));
  f.body = fillSelect($("#selBody"), bodyOpts, f.body);
  var typeOpts = [{ v: "all", label: "All types (" + fmt(all) + ")" }].concat(
    Object.keys(BY_TYPE).sort().map(function(t){ return { v: t, label: t + " (" + fmt(BY_TYPE[t]) + ")" }; }));
  f.type = fillSelect($("#selType"), typeOpts, f.type);
  var stateOpts = [{ v: "all", label: "All States" }].concat(
    Object.keys(BY_STATE).map(function(s){ return { s: s, c: BY_STATE[s] }; })
      .sort(function(a, b){ return b.c - a.c || a.s.localeCompare(b.s); })
      .map(function(o){ return { v: o.s, label: o.s + " (" + fmt(o.c) + ")" }; }));
  f.state = fillSelect($("#selState"), stateOpts, f.state);
  var yearOpts = YEARS.map(function(y){ return { v: y, label: String(y) }; });
  f.yf = Number(fillSelect($("#selYf"), yearOpts, f.yf));
  f.yt = Number(fillSelect($("#selYt"), yearOpts, f.yt));
  if (f.yf > f.yt){ var t = f.yf; f.yf = f.yt; f.yt = t; $("#selYf").value = String(f.yf); $("#selYt").value = String(f.yt); }
  var sdgOpts = [{ v: "all", label: "All SDGs" }].concat(
    Array.from(SDG_SET).sort(function(a, b){ return a - b; }).map(function(g){
      return { v: String(g), label: g + " — " + (SDG_NAMES[String(g)] || "SDG " + g) };
    }));
  f.sdg = fillSelect($("#selSdg"), sdgOpts, f.sdg);
}
function setFilter(k, v){ state.filters[k] = v; state.shown = 50; redrawSample(); render(); }
function resetFilter(k){
  var f = state.filters;
  if (k === "keyword"){ f.keyword = ""; $("#kw1").value = ""; $("#kw2").value = ""; }
  else if (k === "years"){ f.yf = FILE_YMIN; f.yt = FILE_YMAX; }
  else f[k] = "all";
  state.shown = 50; redrawSample(); render();
}

/* ---------- overview ---------- */
var chart1 = null, chart2 = null;
var barValuePlugin = {
  id: "barValue",
  afterDatasetsDraw: function(chart){
    var ctx = chart.ctx, meta = chart.getDatasetMeta(0);
    ctx.save();
    ctx.font = '12px ui-monospace, Menlo, Consolas, monospace';
    ctx.fillStyle = "#1d1b18"; ctx.textBaseline = "middle";
    meta.data.forEach(function(bar, i){
      ctx.fillText(fmt(chart.data.datasets[0].data[i]), bar.x + 6, bar.y);
    });
    ctx.restore();
  }
};
function renderOverview(){
  var f = filtered(), n = f.length;
  var byType = countBy(f, function(r){ return r.type; });
  var docs = new Set(f.map(function(r){ return r.symbol; })).size;
  var ys = f.map(function(r){ return r.year; });
  var ymin = ys.length ? Math.min.apply(null, ys) : null;
  var ymax = ys.length ? Math.max.apply(null, ys) : null;
  var tiles = $("#tiles"); tiles.innerHTML = "";
  function tile(big, sub, how){
    var d = document.createElement("div"); d.className = "tile";
    d.innerHTML = '<div class="big">' + big + '</div><div class="sub">' + sub + '</div><div class="how">' + how + "</div>";
    return d;
  }
  tiles.appendChild(tile(fmt(n),
    "records in the current filter — " + Object.keys(byType).map(function(t){ return esc(t) + " " + fmt(byType[t]); }).join(" · "),
    "How this is computed: count of records passing every filter, all types included; " + fmt(RECS.length) + " records in the file."));
  tiles.appendChild(tile(fmt(docs), "documents (distinct symbol)",
    "How this is computed: number of distinct symbol values among the filtered records."));
  tiles.appendChild(tile(n ? ymin + "–" + ymax : "—", "years covered (min–max of year)",
    "How this is computed: min and max of year among the filtered records; the file spans " + FILE_YMIN + "–" + FILE_YMAX + "."));
  var mt = $("#mechTiles"); mt.innerHTML = "";
  MECHS.forEach(function(m){
    var sub = f.filter(function(r){ return r.mechanism === m; });
    var mdocs = new Set(sub.map(function(r){ return r.symbol; })).size;
    var mys = sub.map(function(r){ return r.year; });
    var latest = mys.length ? Math.max.apply(null, mys) : "—";
    var share = n ? (100 * sub.length / n).toFixed(1) : "0.0";
    var d = document.createElement("div"); d.className = "mech";
    d.innerHTML = '<div class="mname"><span class="dot" style="background:' + (MEC_COLORS[m] || "#6b6459") + '"></span>' + esc(m) + "</div>"
      + '<div class="mnum">' + fmt(sub.length) + "</div>"
      + '<div class="msub">' + fmt(mdocs) + " documents · latest " + latest + " · " + share + "% of filtered</div>"
      + '<div class="how">How this is computed: filtered records with mechanism = ' + esc(m) + ".</div>"
      + (m === "Universal Periodic Review" ? '<button class="linkbtn" type="button" id="statesLink">' + (state.showStates ? "hide the States" : "see the States") + "</button>" : "");
    mt.appendChild(d);
  });
  var sb = $("#statesBox");
  if (state.showStates){
    var upr = f.filter(function(r){ return r.mechanism === "Universal Periodic Review"; });
    var sc = {};
    upr.forEach(function(r){ r._states.forEach(function(s){ if (s !== "State not found") sc[s] = (sc[s] || 0) + 1; }); });
    var top = Object.keys(sc).map(function(s){ return { s: s, c: sc[s] }; })
      .sort(function(a, b){ return b.c - a.c || a.s.localeCompare(b.s); }).slice(0, 10);
    sb.innerHTML = "<h3>Ten States that made most recommendations to " + esc(COUNTRY) + " · current filter</h3>"
      + (top.length
        ? "<ol>" + top.map(function(t){ return "<li>" + esc(t.s) + " — " + fmt(t.c) + " recommendations</li>"; }).join("") + "</ol>"
        : "<p class='hint'>No UPR records in the current filter.</p>")
      + "<p class='hint'>How this is computed: UPR records in the filter, each counted once per State named in its trailing parentheses. A count of recommendations, not of influence; two States can co-sponsor one line.</p>";
    sb.hidden = false;
  } else sb.hidden = true;
  /* FIG.01 */
  var top10 = themeStats(f).slice(0, 10);
  $("#fig1Title").textContent = "FIG.01 · Ten most frequent themes among " + fmt(n) + " filtered records";
  $("#fig1Src").textContent = "Source: UHRI records, current filter · click a bar to filter by that theme · a record can carry several themes, so counts add up to more than " + fmt(n);
  if (chart1){ chart1.destroy(); chart1 = null; }
  if (n === 0 || top10.length === 0){
    $("#fig1Box").hidden = true;
    $("#fig1Empty").hidden = false;
    $("#fig1Empty").textContent = n === 0 ? "No records match the current filters." : "None of the matching records carries a theme label.";
    $("#fig1Body").innerHTML = ""; $("#fig1Note").textContent = "";
  } else {
    $("#fig1Box").hidden = false; $("#fig1Empty").hidden = true;
    chart1 = new Chart($("#chart1").getContext("2d"), {
      type: "bar",
      data: {
        labels: top10.map(function(t){ return t.theme; }),
        datasets: [{ label: "records", data: top10.map(function(t){ return t.count; }), backgroundColor: "rgba(155,35,53,0.8)", borderWidth: 0, maxBarThickness: 34 }]
      },
      options: {
        indexAxis: "y", responsive: true, maintainAspectRatio: false,
        onClick: function(e, els){ if (els.length){ setFilter("theme", top10[els[0].index].theme); } },
        scales: {
          x: { beginAtZero: true, suggestedMax: Math.max.apply(null, top10.map(function(t){ return t.count; })) * 1.18 + 1,
               grid: { color: "#e7e0d2" }, border: { color: "#d9d2c3" },
               ticks: { font: { family: "ui-monospace, Menlo, Consolas, monospace", size: 11 } } },
          y: { grid: { display: false }, border: { color: "#d9d2c3" }, ticks: { font: { size: 13 } } }
        },
        plugins: { legend: { display: false }, tooltip: { callbacks: { label: function(c){ return " " + fmt(c.parsed.x) + " records"; } } } }
      },
      plugins: [barValuePlugin]
    });
    $("#fig1Body").innerHTML = top10.map(function(t){
      return "<tr><td>" + esc(t.theme) + "</td><td class='num'>" + fmt(t.count) + "</td><td class='num'>" + (100 * t.count / n).toFixed(1) + "%</td><td>" + t.ymin + "–" + t.ymax + "</td></tr>";
    }).join("");
    $("#fig1Note").textContent = "Percentages are of the " + fmt(n) + " filtered records, not of labels; ties are alphabetical. Years = first–last year of the filtered records carrying the theme.";
  }
  /* FIG.02 */
  $("#fig2Title").textContent = "FIG.02 · Records per year by mechanism · " + fmt(n) + " filtered records";
  $("#fig2Src").textContent = "Source: UHRI records, current filter · every year from " + FILE_YMIN + " to " + FILE_YMAX + " is shown, so empty years appear as gaps · dated by document";
  if (chart2){ chart2.destroy(); chart2 = null; }
  if (n === 0){
    $("#fig2Box").hidden = true; $("#fig2Empty").hidden = false;
  } else {
    $("#fig2Box").hidden = false; $("#fig2Empty").hidden = true;
    var yAll = []; for (var y = FILE_YMIN; y <= FILE_YMAX; y++) yAll.push(y);
    var datasets = MECHS.map(function(m){
      return { label: m, stack: "s", backgroundColor: MEC_COLORS[m] || "#6b6459",
        data: yAll.map(function(yy){ return f.filter(function(r){ return r.year === yy && r.mechanism === m; }).length; }) };
    });
    chart2 = new Chart($("#chart2").getContext("2d"), {
      type: "bar",
      data: { labels: yAll.map(String), datasets: datasets },
      options: {
        responsive: true, maintainAspectRatio: false,
        scales: {
          x: { stacked: true, grid: { display: false }, ticks: { font: { family: "ui-monospace, Menlo, Consolas, monospace", size: 11 } } },
          y: { stacked: true, beginAtZero: true, grid: { color: "#e7e0d2" }, ticks: { precision: 0, font: { family: "ui-monospace, Menlo, Consolas, monospace", size: 11 } } }
        },
        plugins: { legend: { position: "bottom", labels: { usePointStyle: true, pointStyle: "rect", font: { size: 12 } } } }
      }
    });
  }
}

/* ---------- records ---------- */
function stateCell(r){
  if (r.mechanism !== "Universal Periodic Review") return "—";
  return r._states.length ? esc(r._states.join(" · ")) : "State not found";
}
function labelsHtml(r){
  var h = '<div class="labels">';
  h += '<div><span class="lbl">Section</span>' + (r.section ? esc(r.section) : '<span class="missing">not labelled</span>') + "</div>";
  h += '<div><span class="lbl">Themes</span>' + ((r.themes && r.themes.length) ? r.themes.map(function(t){ return '<span class="tagchip">' + esc(t) + "</span>"; }).join("") : '<span class="missing">not labelled</span>') + "</div>";
  var sdgs = (r.sdgs || []).map(function(g){ return "SDG " + g + (SDG_NAMES[String(g)] ? ": " + SDG_NAMES[String(g)] : ""); }).join("; ");
  h += '<div><span class="lbl">SDGs</span>' + (sdgs || '<span class="missing">not labelled</span>') + "</div>";
  h += '<div><span class="lbl">SDG targets</span>' + ((r.sdg_targets && r.sdg_targets.length) ? esc(r.sdg_targets.join("; ")) : '<span class="missing">not labelled</span>') + "</div>";
  h += '<div><span class="lbl">Affected persons</span>' + ((r.affected_persons && r.affected_persons.length) ? esc(r.affected_persons.join("; ")) : '<span class="missing">not labelled</span>') + "</div>";
  return h + "</div>";
}
function detailHtml(r){
  return '<td colspan="6">'
    + '<div class="paranum">' + (r._para ? "para. " + esc(r._para) : "no paragraph number in this extract") + "</div>"
    + '<p class="fulltext">' + hi(r.text) + "</p>"
    + labelsHtml(r)
    + '<div class="rowactions"><button type="button" class="btn copybtn" data-id="' + esc(r.id) + '">'
    + (r._para ? "Copy citation" : "Copy citation (no paragraph number in this extract)")
    + '</button> <a class="btn" href="' + esc(r.doc_url) + '" target="_blank" rel="noopener">Open the UN document</a>'
    + ' <span class="copied" hidden>Copied ✓</span></div></td>';
}
function renderRecords(){
  var f = filtered();
  var sorted = f.slice().sort(function(a, b){
    var d = state.sortAsc ? String(a.date).localeCompare(String(b.date)) : String(b.date).localeCompare(String(a.date));
    if (d) return d;
    var b2 = String(a.body).localeCompare(String(b.body)); if (b2) return b2;
    var pa = a._para ? parseFloat(a._para) : Infinity, pb = b._para ? parseFloat(b._para) : Infinity;
    if (pa !== pb) return pa - pb;
    return a._i - b._i;
  });
  var shown = Math.min(state.shown, sorted.length);
  $("#recCaption").textContent = sorted.length
    ? "Showing " + fmt(shown) + " of " + fmt(sorted.length) + " matching records · " + (state.sortAsc ? "oldest" : "newest") + " first · click a row for the full paragraph"
    : "No records match the current filters.";
  $("#recEmpty").hidden = sorted.length > 0;
  $("#showMore").hidden = shown >= sorted.length;
  $("#kw2").placeholder = "Search " + fmt(sorted.length) + " records, e.g. torture";
  var tb = $("#recBody"); tb.innerHTML = "";
  var frag = document.createDocumentFragment();
  sorted.slice(0, shown).forEach(function(r){
    var tr = document.createElement("tr");
    tr.className = "data"; tr.tabIndex = 0; tr.dataset.id = r.id;
    tr.setAttribute("aria-expanded", state.expanded.has(r.id) ? "true" : "false");
    tr.innerHTML = "<td>" + esc(r.date) + "</td><td>" + esc(r.body) + "</td>"
      + "<td><a href='" + esc(r.doc_url) + "' target='_blank' rel='noopener'>" + esc(r.symbol) + "</a></td>"
      + "<td>" + (r._para ? esc(r._para) : "—") + "</td>"
      + "<td class='firstline'>" + hi(r._first) + "</td>"
      + "<td>" + stateCell(r) + "</td>";
    frag.appendChild(tr);
    var dt = document.createElement("tr");
    dt.className = "detail"; dt.dataset.id = r.id; dt.hidden = !state.expanded.has(r.id);
    dt.innerHTML = detailHtml(r);
    frag.appendChild(dt);
  });
  tb.appendChild(frag);
}
function toggleRow(id){
  if (state.expanded.has(id)) state.expanded.delete(id); else state.expanded.add(id);
  renderTab(1);
}

/* ---------- checks ---------- */
function runChecks(){
  var checks = [], n = RECS.length;
  checks.push({ name: "Record count", detail: "records.length = " + fmt(n) + " vs Number(count) = " + fmt(Number(D.count)), pass: n === Number(D.count) });
  function sum(o){ return Object.keys(o).map(function(k){ return o[k]; }).reduce(function(a, b){ return a + b; }, 0); }
  var bm = countBy(RECS, function(r){ return r.mechanism; });
  var bb = countBy(RECS, function(r){ return r.body; });
  var by = countBy(RECS, function(r){ return r.year; });
  checks.push({ name: "Partitions: mechanism, body, year", detail: "sums " + fmt(sum(bm)) + ", " + fmt(sum(bb)) + ", " + fmt(sum(by)) + " vs " + fmt(n) + " records", pass: sum(bm) === n && sum(bb) === n && sum(by) === n });
  var bt = countBy(RECS, function(r){ return r.type; });
  checks.push({ name: "Type partition", detail: "counts per type sum to " + fmt(sum(bt)) + " vs " + fmt(n), pass: sum(bt) === n });
  var f = filtered();
  var a = themeStats(f).slice(0, 10);
  var b = {};
  f.forEach(function(r){ (r.themes || []).forEach(function(t){ b[t] = (b[t] || 0) + 1; }); });
  var bTop = Object.keys(b).map(function(t){ return { theme: t, count: b[t] }; })
    .sort(function(x, y){ return y.count - x.count || x.theme.localeCompare(y.theme); }).slice(0, 10);
  var same = a.length === bTop.length && a.every(function(t, i){ return t.theme === bTop[i].theme && t.count === bTop[i].count; });
  var largest = a.length ? a[0].count : 0;
  checks.push({ name: "Chart against table (FIG.01)", detail: "top ten recomputed by a second loop: " + (same ? "identical" : "DIFFERENT") + "; largest bar " + fmt(largest) + " ≤ " + fmt(f.length) + " filtered records: " + (largest <= f.length ? "yes" : "no"), pass: same && largest <= f.length });
  var badLinks = RECS.filter(function(r){
    try {
      var u = decodeURIComponent(r.doc_url).toLowerCase();
      return !(String(r.doc_url).indexOf("https://docs.un.org/") === 0 && u.slice(-r.symbol.length) === r.symbol.toLowerCase());
    } catch(e){ return true; }
  });
  checks.push({ name: "Links", detail: fmt(n - badLinks.length) + " of " + fmt(n) + " doc_url values start with https://docs.un.org/ and end with the record's symbol (case-insensitive, decoded)", pass: badLinks.length === 0,
    list: badLinks.slice(0, 10).map(function(r){ return r.symbol + " → " + r.doc_url; }), more: Math.max(0, badLinks.length - 10) });
  var pm = {};
  RECS.forEach(function(r){ var m = r.mechanism; pm[m] = pm[m] || { tot: 0, found: 0 }; pm[m].tot++; if (r._para) pm[m].found++; });
  var upr = pm["Universal Periodic Review"];
  var uprWarn = !(upr && upr.found === upr.tot);
  checks.push({ name: "Paragraph numbers found", detail: Object.keys(pm).map(function(m){ var v = pm[m]; return m + ": " + v.found + "/" + v.tot + " (" + (100 * v.found / v.tot).toFixed(1) + "%)"; }).join(" · ") + (uprWarn ? " — UPR below 100%: warning, not an error" : ""), pass: true, warn: uprWarn });
  var uprRecs = RECS.filter(function(r){ return r.mechanism === "Universal Periodic Review"; });
  var noState = uprRecs.filter(function(r){ return !r._states.some(function(s){ return s !== "State not found"; }); });
  checks.push({ name: "Recommending States found (UPR)", detail: fmt(uprRecs.length - noState.length) + " of " + fmt(uprRecs.length) + " UPR records have at least one State in the trailing parentheses", pass: noState.length === 0,
    list: noState.slice(0, 10).map(function(r){ var t = String(r.text || ""); return r.symbol + " — trailing text: " + (t.length > 90 ? "…" + t.slice(-90) : t); }), more: Math.max(0, noState.length - 10) });
  var ids = new Set(RECS.map(function(r){ return r.id; }));
  var tc = countBy(RECS, function(r){ return r.text; });
  var dup = Object.keys(tc).filter(function(k){ return tc[k] > 1; }).length;
  var noTh = RECS.filter(function(r){ return !(r.themes || []).length; }).length;
  var noSdg = RECS.filter(function(r){ return !(r.sdgs || []).length; }).length;
  var noAp = RECS.filter(function(r){ return !(r.affected_persons || []).length; }).length;
  checks.push({ name: "Duplicates and gaps", detail: "distinct id " + fmt(ids.size) + " vs " + fmt(n) + " records; duplicate text values " + dup + "; not labelled — themes " + fmt(noTh) + ", sdgs " + fmt(noSdg) + ", affected persons " + fmt(noAp), pass: ids.size === n });
  return checks;
}
function renderChecks(){
  var list = $("#checkList"); list.innerHTML = "";
  runChecks().forEach(function(c){
    var div = document.createElement("div");
    div.className = "check" + (c.pass ? (c.warn ? " warn" : "") : " fail");
    var mark = c.pass ? (c.warn ? "⚠" : "✓") : "✗";
    var html = '<span class="mark">' + mark + '</span><span><span class="what">' + esc(c.name) + "</span> — " + esc(c.detail);
    if (!c.pass) html += ' <span class="failtxt">CHECK FAILED</span>';
    if (c.list && c.list.length) html += '<br><span class="failures">' + c.list.map(esc).join("<br>") + (c.more > 0 ? "<br>… and " + c.more + " more" : "") + "</span>";
    div.innerHTML = html + "</span>";
    list.appendChild(div);
  });
  renderSample();
}
function renderSample(){
  var box = $("#sampleList"); box.innerHTML = "";
  var tally = $("#tally");
  if (!state.sampleIds){ tally.textContent = ""; box.innerHTML = '<p class="hint">No sample drawn yet — press "Check 10 at random".</p>'; return; }
  var ids = state.sampleIds;
  var vs = ids.map(function(id){ return state.verdicts[state.sampleSeed + "|" + id]; });
  var fit = vs.filter(function(v){ return v === "fit"; }).length;
  var no = vs.filter(function(v){ return v === "no"; }).length;
  var un = vs.filter(function(v){ return v === "unsure"; }).length;
  tally.textContent = "Themes: " + fit + " fit · " + no + " don't fit · " + un + " unsure · " + (fit + no + un) + " of " + ids.length + " judged · seed " + state.sampleSeed + " · drawn from " + fmt(filtered().length) + " filtered records";
  ids.forEach(function(id){
    var r = byId[id]; if (!r) return;
    var open = state.sampleOpen === id;
    var card = document.createElement("div"); card.className = "samplecard";
    var btn = document.createElement("button"); btn.type = "button"; btn.className = "samplebtn";
    btn.setAttribute("aria-expanded", open ? "true" : "false");
    btn.innerHTML = "<span>" + esc(r.symbol) + " · para " + (r._para ? esc(r._para) : "—") + " · " + r.year + "</span><span>" + (open ? "–" : "+") + "</span>";
    btn.addEventListener("click", function(){ state.sampleOpen = open ? null : id; renderTab(2); });
    card.appendChild(btn);
    if (open){
      var v = state.verdicts[state.sampleSeed + "|" + id];
      var body = document.createElement("div"); body.className = "samplebody";
      body.innerHTML = '<p class="fulltext">' + esc(r.text) + "</p>"
        + '<div><span class="lbl">Themes as labelled by the UN</span> '
        + ((r.themes && r.themes.length) ? r.themes.map(function(t){ return '<span class="tagchip">' + esc(t) + "</span>"; }).join("") : '<span class="missing">not labelled</span>') + "</div>"
        + '<div class="verdicts">'
        + [["fit", "Fits"], ["no", "Doesn't fit"], ["unsure", "Unsure"]].map(function(kv){
            return '<button type="button" class="btn verdict" data-id="' + esc(id) + '" data-v="' + kv[0] + '" aria-pressed="' + (v === kv[0]) + '">' + kv[1] + "</button>";
          }).join(" ")
        + "</div>";
      card.appendChild(body);
    }
    box.appendChild(card);
  });
}
function drawSample(){
  var f = filtered();
  var rnd = mulberry32(state.sampleSeed >>> 0);
  var idx = f.map(function(_, i){ return i; });
  for (var i = idx.length - 1; i > 0; i--){ var j = Math.floor(rnd() * (i + 1)); var t = idx[i]; idx[i] = idx[j]; idx[j] = t; }
  state.sampleIds = idx.slice(0, Math.min(10, idx.length)).map(function(i){ return f[i].id; });
  state.sampleOpen = null;
  render();
}
function redrawSample(){
  if (!state.sampleIds) return;
  var f = filtered();
  var rnd = mulberry32(state.sampleSeed >>> 0);
  var idx = f.map(function(_, i){ return i; });
  for (var i = idx.length - 1; i > 0; i--){ var j = Math.floor(rnd() * (i + 1)); var t = idx[i]; idx[i] = idx[j]; idx[j] = t; }
  state.sampleIds = idx.slice(0, Math.min(10, idx.length)).map(function(i){ return f[i].id; });
  state.sampleOpen = null;
}

/* ---------- method & export ---------- */
function renderMethod(){
  $("#srcLine").innerHTML = "Source: <a href='" + esc(SOURCE_URL) + "' target='_blank' rel='noopener'>" + esc(SOURCE) + "</a> · built " + esc(BUILT)
    + " · " + fmt(RECS.length) + " records for " + esc(COUNTRY) + " · terms of use as stated on the source page. The file holds one country; no other country is compared.";
}
function csvCell(v){ v = String(v == null ? "" : v); return '"' + v.replace(/"/g, '""') + '"'; }
function downloadCSV(){
  var f = filtered();
  var lines = [];
  lines.push("# Country: " + COUNTRY);
  lines.push("# Source: " + SOURCE + " — " + SOURCE_URL);
  lines.push("# Built: " + BUILT);
  lines.push("# Filters: " + filterDesc());
  lines.push("# Rows: " + f.length + " of " + RECS.length + " records");
  lines.push(["Date","Body","Mechanism","Type","Symbol","Document URL","Paragraph","Recommending State(s)","Section","Themes","SDGs","SDG targets","Affected persons","Text"].map(csvCell).join(","));
  f.forEach(function(r){
    lines.push([r.date, r.body, r.mechanism, r.type, r.symbol, r.doc_url, r._para || "", r._states.join("; "), r.section || "", (r.themes || []).join("; "), (r.sdgs || []).join("; "), (r.sdg_targets || []).join("; "), (r.affected_persons || []).join("; "), r.text].map(csvCell).join(","));
  });
  var blob = new Blob([lines.join("\r\n")], { type: "text/csv;charset=utf-8" });
  var a = document.createElement("a");
  a.href = URL.createObjectURL(blob);
  a.download = "uhri-" + COUNTRY.toLowerCase().replace(/[^a-z0-9]+/g, "-") + "-recommendations.csv";
  document.body.appendChild(a); a.click();
  setTimeout(function(){ URL.revokeObjectURL(a.href); a.remove(); }, 500);
}
function summaryText(){
  var f = filtered(), n = f.length;
  if (!n) return COUNTRY + ": 0 records match the current filters (" + filterDesc() + "). Source: " + SOURCE + " (" + SOURCE_URL + "), built " + BUILT + ".";
  var byType = countBy(f, function(r){ return r.type; });
  var types = Object.keys(byType).map(function(t){ return t + " " + fmt(byType[t]); }).join(" · ");
  var docs = new Set(f.map(function(r){ return r.symbol; })).size;
  var ys = f.map(function(r){ return r.year; });
  var top = themeStats(f).slice(0, 10).map(function(t, i){ return (i + 1) + ") " + t.theme + " (" + fmt(t.count) + ")"; }).join(", ");
  return COUNTRY + ": " + fmt(n) + " UN recommendations and observations (" + types + ") from " + fmt(docs) + " documents, "
    + Math.min.apply(null, ys) + "–" + Math.max.apply(null, ys) + ", dated by document. Top themes among the " + fmt(n)
    + " filtered records: " + top + ". Source: " + SOURCE + " (" + SOURCE_URL + "), built " + BUILT + ". Filters: " + filterDesc() + ".";
}

/* ---------- tabs & render ---------- */
function renderTab(i){
  if (i === 0) renderOverview();
  else if (i === 1) renderRecords();
  else if (i === 2) renderChecks();
  else renderMethod();
}
function render(){ renderRail(); renderTab(state.tab); }
function switchTab(i){
  state.tab = i;
  for (var k = 0; k < 4; k++){
    $("#tab-" + k).setAttribute("aria-selected", k === i ? "true" : "false");
    $("#tab-" + k).tabIndex = k === i ? 0 : -1;
    $("#panel-" + k).hidden = k !== i;
  }
  if (i !== 0){ if (chart1){ chart1.destroy(); chart1 = null; } if (chart2){ chart2.destroy(); chart2 = null; } }
  renderRail(); renderTab(i);
}

/* ---------- init ---------- */
function bindKw(input){
  var t;
  input.addEventListener("input", function(){
    clearTimeout(t);
    t = setTimeout(function(){
      state.filters.keyword = input.value; state.shown = 50; redrawSample();
      var other = input.id === "kw1" ? $("#kw2") : $("#kw1");
      if (other && other.value !== input.value) other.value = input.value;
      render();
    }, 300);
  });
}
function init(){
  document.title = "UHRI · " + COUNTRY + " — UN recommendations dashboard";
  $("#kicker").textContent = "UHRI · " + COUNTRY.toUpperCase();
  $("#title").textContent = "UN human rights recommendations and observations: " + COUNTRY;
  var docs = new Set(RECS.map(function(r){ return r.symbol; })).size;
  $("#meta").innerHTML = "Source: <a href='" + esc(SOURCE_URL) + "' target='_blank' rel='noopener'>" + esc(SOURCE) + "</a> · "
    + fmt(RECS.length) + " records · " + fmt(docs) + " documents · " + FILE_YMIN + "–" + FILE_YMAX + " · built " + esc