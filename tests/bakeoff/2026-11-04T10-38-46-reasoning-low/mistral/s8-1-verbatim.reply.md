Here's the verbatim finder: it searches all 7,304 General Comment paragraphs in `WORKSHOP_DATA.gc` with a Boolean query parser (phrases, AND/OR/NOT, wildcards), normalises curly quotes/dashes/footnote marks so pasted text still matches, and builds paste-ready citations and quotations strictly from each record's fields — no model is called. Four tabs (overview chart, paged paragraphs, draft collection, self-checks), a filter rail, and a Chart.js bar chart of hits per committee.

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Verbatim finder · UN General Comments</title>
<style>
:root{
  --paper:#f4f0e8; --ink:#1d1b18; --rule:#d9d2c3; --red:#9b2335;
  --amber:#8a5a00; --green:#1e6b3a; --mark:#f3e6a2; --mut:#6b655a; --soft:#8a8578;
}
*{box-sizing:border-box}
[hidden]{display:none!important}
html{margin:0}
body{
  margin:0 auto; max-width:1180px; padding:0 22px 46px;
  background:var(--paper); color:var(--ink);
  font:16px/1.55 -apple-system,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif;
}
:focus-visible{outline:3px solid var(--red); outline-offset:2px}
a{color:var(--ink)}
button{font-family:inherit; cursor:pointer}
.sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}

/* header */
.top{padding:24px 0 12px; border-bottom:1px solid var(--rule); position:relative}
.kicker{font:11px/1 ui-monospace,Menlo,Consolas,monospace; letter-spacing:.2em; color:var(--red)}
h1{font-family:Georgia,"Times New Roman",serif; font-weight:400; font-size:30px; line-height:1.2; margin:10px 0 8px; max-width:62ch}
.dataline{font-size:13px; color:#4a463f; margin:0}
.checkstatus{position:absolute; right:0; top:26px; font:11px ui-monospace,Menlo,Consolas,monospace; letter-spacing:.08em; color:#4a463f}
.dot{display:inline-block; width:9px; height:9px; border-radius:50%; margin-right:6px; vertical-align:baseline}
.dot.g{background:var(--green)} .dot.r{background:var(--red)}

/* tabs */
.tabs{display:flex; gap:2px; border-bottom:1px solid var(--rule); margin-top:8px; overflow-x:auto}
.tabs [role=tab]{
  appearance:none; background:none; border:none; border-bottom:2px solid transparent;
  padding:11px 14px; font:12px ui-monospace,Menlo,Consolas,monospace; letter-spacing:.14em;
  color:var(--mut); white-space:nowrap;
}
.tabs [role=tab][aria-selected=true]{color:var(--red); border-bottom-color:var(--red)}
.tabs [role=tab]:hover{color:var(--ink)}

/* layout */
.layout{display:flex; gap:30px; align-items:flex-start; padding-top:20px}
.rail{width:302px; flex:0 0 302px; position:sticky; top:14px}
.main{flex:1; min-width:0}
@media (max-width:920px){
  .layout{flex-direction:column}
  .rail{width:100%; flex:none; position:static}
  .checkstatus{position:static; margin-top:8px}
}

/* rail */
.railhead{display:flex; justify-content:space-between; align-items:baseline; border-bottom:1px solid var(--rule); padding-bottom:7px; font:11px ui-monospace,Menlo,Consolas,monospace; letter-spacing:.2em; color:var(--mut)}
#clearall{background:none; border:none; color:var(--mut); text-decoration:underline; font:11px ui-monospace,Menlo,Consolas,monospace; letter-spacing:.06em; padding:0}
#clearall:hover{color:var(--red)}
.bignum{font-family:Georgia,"Times New Roman",serif; font-size:52px; line-height:1; margin-top:16px}
.biglabel{font:11px ui-monospace,Menlo,Consolas,monospace; letter-spacing:.12em; color:var(--mut); margin-top:5px}
.how{font-size:12px; color:var(--mut); margin:10px 0 0; border-top:1px dotted var(--rule); padding-top:7px}
.chips{display:flex; flex-wrap:wrap; gap:6px; margin-top:10px}
.chip{font:11px ui-monospace,Menlo,Consolas,monospace; border:1px solid var(--red); color:var(--red); background:none; padding:3px 8px; border-radius:2px}
.chip:hover{background:#efe7d6}

/* search */
.searchbox{margin-top:20px; border-top:1px solid var(--rule); padding-top:14px}
.searchbox label{display:block; font:11px ui-monospace,Menlo,Consolas,monospace; letter-spacing:.18em; color:var(--mut); margin-bottom:7px}
.qrow{display:flex; gap:6px}
#q{flex:1; min-width:0; padding:9px 10px; font:13px ui-monospace,Menlo,Consolas,monospace; background:#fffdf8; border:1px solid var(--rule); color:var(--ink)}
#searchbtn{padding:9px 14px; background:var(--ink); color:var(--paper); border:1px solid var(--ink); font:12px ui-monospace,Menlo,Consolas,monospace; letter-spacing:.1em}
#searchbtn:hover{background:var(--red); border-color:var(--red)}
.syntax{margin-top:8px; border:1px solid var(--rule); background:#fffdf8; padding:10px 12px; font-size:12.5px}
.syntax .sline{margin:3px 0; color:#4a463f}
.syntax b{font-family:ui-monospace,Menlo,Consolas,monospace; font-weight:600}
.exs{margin-top:8px; border-top:1px dotted var(--rule); padding-top:7px}
.ex{display:inline-block; background:none; border:none; padding:2px 4px; margin:2px 6px 2px 0; font:12px ui-monospace,Menlo,Consolas,monospace; color:var(--red); text-decoration:underline}
.echo{margin:9px 0 0; font-size:13px; min-height:1em}
.err{margin:6px 0 0; font-size:13px; color:var(--red)}
.hint{font-size:12px; color:var(--mut); margin:8px 0 0}

/* filter section */
.filtersec{margin-top:20px; border-top:1px solid var(--rule)}
.fhead{width:100%; display:flex; gap:9px; align-items:baseline; text-align:left; background:none; border:none; padding:12px 0 10px; font:12px ui-monospace,Menlo,Consolas,monospace; letter-spacing:.14em; color:var(--ink)}
.fhead .fnum{color:var(--red)}
.fhead .chev{margin-left:auto; color:var(--mut)}
.fhead[aria-expanded=true]{color:var(--red)}
.fbody{border-top:1px dotted var(--rule); padding:4px 0 18px}
.flabel{display:flex; justify-content:space-between; align-items:baseline; font:11px ui-monospace,Menlo,Consolas,monospace; letter-spacing:.16em; color:var(--mut); margin:14px 0 7px}
#allnone{background:none; border:none; color:var(--mut); text-decoration:underline; font:11px ui-monospace,Menlo,Consolas,monospace; padding:0}
#allnone:hover{color:var(--red)}
.ck{display:flex; align-items:baseline; gap:7px; font-size:13px; padding:2.5px 0; cursor:pointer}
.ck input{accent-color:var(--red); margin:0}
.ck .code{font:11px ui-monospace,Menlo,Consolas,monospace; color:var(--red)}
.ck .nm{color:#4a463f}
.ck .hits{font:11px ui-monospace,Menlo,Consolas,monospace; color:var(--soft); margin-left:auto}
.yrow{display:flex; gap:7px; align-items:center}
.yrow input{width:86px; padding:6px 8px; border:1px solid var(--rule); background:#fffdf8; font:13px ui-monospace,Menlo,Consolas,monospace; color:var(--ink)}
#docsel{width:100%; padding:7px; border:1px solid var(--rule); background:#fffdf8; font-size:13px; color:var(--ink)}

/* panels */
.ptitle{font-family:Georgia,"Times New Roman",serif; font-weight:400; font-size:22px; margin:26px 0 6px}
.figtitle{font-family:Georgia,"Times New Roman",serif; font-weight:400; font-size:22px; margin:0 0 4px}
.figno{font:11px ui-monospace,Menlo,Consolas,monospace; color:var(--red); letter-spacing:.16em; margin-right:12px; vertical-align:middle}
.figwrap{display:flex; gap:28px; align-items:flex-start; flex-wrap:wrap; margin-top:14px}
.chartbox{flex:1 1 340px; min-width:300px; position:relative}
.figtable{border-collapse:collapse; font-size:13px; flex:0 0 auto}
.figtable caption{text-align:left; font:11px ui-monospace,Menlo,Consolas,monospace; letter-spacing:.12em; color:var(--mut); padding-bottom:7px}
.figtable th,.figtable td{border-bottom:1px solid var(--rule); padding:4px 14px 4px 0; text-align:left; font-weight:400}
.figtable td.num,.figtable th.num{text-align:right; font-family:Georgia,serif}
.summary{font-size:15px; margin:0 0 10px}
.orderrow{display:flex; gap:10px; align-items:center; flex-wrap:wrap; margin-bottom:6px}
.orderrow label{font:11px ui-monospace,Menlo,Consolas,monospace; letter-spacing:.14em; color:var(--mut)}
#order{padding:6px 8px; border:1px solid var(--rule); background:#fffdf8; font-size:13px; color:var(--ink)}

/* result rows */
.row{border-bottom:1px solid var(--rule); padding:15px 0}
.rowh{margin:0; font-size:inherit; font-weight:inherit}
.rowhead{display:block; width:100%; text-align:left; background:none; border:none; padding:0; color:inherit; font:inherit}
.meta{display:flex; flex-wrap:wrap; gap:8px; align-items:baseline; font-size:13px}
.badge{font:11px ui-monospace,Menlo,Consolas,monospace; border:1px solid var(--soft); color:#4a463f; padding:1px 6px; letter-spacing:.06em}
.doc{color:#4a463f}
.sym{font:12px ui-monospace,Menlo,Consolas,monospace}
.pin{color:var(--red); font:12px ui-monospace,Menlo,Consolas,monospace}
.yr{color:var(--soft); font:12px ui-monospace,Menlo,Consolas,monospace}
.rtext{margin:9px 0 0; white-space:pre-wrap; font-size:15px}
mark{background:var(--mark); color:var(--ink); font-weight:700; padding:0 1px}
.marksline{font-size:12px; color:var(--soft); margin-top:7px}
.linkbtn{background:none; border:none; padding:0; color:var(--mut); text-decoration:underline; font-size:inherit}
.linkbtn:hover{color:var(--red)}
.note{font-size:12.5px; color:var(--amber); margin-top:7px}
.detail{margin-top:12px; border-top:1px dotted var(--rule); padding-top:12px}
.btns{display:flex; flex-wrap:wrap; gap:8px}
.btn{padding:7px 13px; border:1px solid var(--ink); background:none; color:var(--ink); font:12px ui-monospace,Menlo,Consolas,monospace; letter-spacing:.06em}
.btn:hover{background:#eae3d3}
.btn.primary{border-color:var(--red); color:var(--red)}
.btn.primary:hover{background:#f0e2e4}
.ctx{margin-top:10px; font-size:13px; color:var(--mut)}
.ctxblock{margin-top:8px; color:var(--mut); font-size:13.5px; white-space:pre-wrap; border-left:2px solid var(--rule); padding-left:12px}
#more{margin-top:18px}

/* draft */
.draftbtns{display:flex; gap:8px; flex-wrap:wrap; margin:12px 0 6px}
.ditem{border-bottom:1px solid var(--rule); padding:13px 0}
.dq{margin:0; white-space:pre-wrap; font-size:15px}
.dc{margin:5px 0 8px; font:12px ui-monospace,Menlo,Consolas,monospace; color:var(--red)}

/* checks */
.check{display:flex; gap:12px; padding:9px 0; border-bottom:1px dotted var(--rule); font-size:14px}
.check .st{flex:0 0 96px; font:11px ui-monospace,Menlo,Consolas,monospace; letter-spacing:.1em; padding-top:2px}
.st.pass{color:var(--green)} .st.fail{color:var(--red)}
.quirk{padding:9px 0; border-bottom:1px dotted var(--rule); font-size:14px}
.method{margin:8px 0 0; padding-left:20px; font-size:14px}
.method li{margin:7px 0}
.method code{font:12px ui-monospace,Menlo,Consolas,monospace; background:#fffdf8; border:1px solid var(--rule); padding:0 4px}

/* footer + copybox */
footer{margin-top:38px; border-top:1px solid var(--rule); padding-top:11px; display:flex; justify-content:space-between; gap:10px; flex-wrap:wrap; font:11px ui-monospace,Menlo,Consolas,monospace; letter-spacing:.05em; color:var(--mut)}
#copybox{position:fixed; left:16px; right:16px; bottom:16px; z-index:60; background:#fffdf8; border:1px solid var(--red); padding:12px 14px}
.cbhead{display:flex; justify-content:space-between; font:11px ui-monospace,Menlo,Consolas,monospace; letter-spacing:.1em; color:var(--red); margin-bottom:7px}
#cbtext{width:100%; height:96px; font:12px ui-monospace,Menlo,Consolas,monospace; border:1px solid var(--rule); background:#fff; color:var(--ink); padding:8px}
</style>
</head>
<body>

<header class="top">
  <div class="kicker">UN TREATY BODIES · GENERAL COMMENTS</div>
  <h1>Verbatim finder: General Comments and General Recommendations</h1>
  <p class="dataline"><span id="dataline"></span> · <span id="srcline"></span></p>
  <div class="checkstatus" id="checkstatus"></div>
</header>

<nav class="tabs" role="tablist" aria-label="Views">
  <button role="tab" id="tab-0" aria-controls="panel-0" aria-selected="true" type="button">01 OVERVIEW</button>
  <button role="tab" id="tab-1" aria-controls="panel-1" aria-selected="false" type="button" tabindex="-1">02 PARAGRAPHS</button>
  <button role="tab" id="tab-2" aria-controls="panel-2" aria-selected="false" type="button" tabindex="-1">03 DRAFT <span id="dcount">(0)</span></button>
  <button role="tab" id="tab-3" aria-controls="panel-3" aria-selected="false" type="button" tabindex="-1">04 CHECK &amp; METHOD <span class="dot r" id="tab4dot" hidden></span></button>
</nav>

<div class="layout">
  <aside class="rail" id="rail" aria-label="Filters">
    <div class="railhead"><span>FILTERS</span><button id="clearall" type="button">Clear all</button></div>
    <div class="bignum" id="bignum" aria-live="polite">0</div>
    <div class="biglabel" id="oftotal"></div>
    <p class="how">How this is computed: records whose normalised text matches the query and that pass the filters below; counted by this page's code, never estimated.</p>
    <div class="chips" id="chips"></div>

    <div class="searchbox">
      <label for="q">SEARCH THE PARAGRAPHS</label>
      <div class="qrow">
        <input id="q" type="text" autocomplete="off" spellcheck="false" placeholder='try "torture" NOT "death penalty"'>
        <button id="searchbtn" type="button">Search</button>
      </div>
      <div class="syntax" id="syntax" hidden>
        <div class="sline">a space or <b>AND</b> joins words · <b>OR</b> · <b>NOT</b> or a leading minus</div>
        <div class="sline"><b>"an exact phrase"</b> in double quotes</div>
        <div class="sline"><b>(</b> parentheses <b>)</b></div>
        <div class="sline">a star at the end of a word for any ending (<b>child*</b> finds children)</div>
        <div class="sline">operators in capitals; lower-case "or" is a word</div>
        <div class="sline exs">Try:
          <button type="button" class="ex" data-q="&quot;best interests&quot; AND child">"best interests" AND child</button>
          <button type="button" class="ex" data-q="(torture OR ill-treatment) NOT detention">(torture OR ill-treatment) NOT detention</button>
          <button type="button" class="ex" data-q="&quot;reasonable accommodation&quot;">"reasonable accommodation"</button>
        </div>
      </div>
      <p class="echo" id="echo" aria-live="polite"></p>
      <p class="err" id="qerr"></p>
      <p class="hint">Whole words, any case. Curly and straight quotes, apostrophes, dashes and hyphens count as the same, and footnote marks are skipped, so State's finds State’s and a phrase can cross a footnote.</p>
    </div>

    <div class="filtersec">
      <button class="fhead" id="fhead" type="button" aria-expanded="false" aria-controls="fbody">
        <span class="fnum">01</span> COMMITTEE, YEARS, DOCUMENT <span class="chev">▾</span>
      </button>
      <div class="fbody" id="fbody" hidden>
        <div class="fgroup">
          <div class="flabel"><span>COMMITTEE</span><button id="allnone" type="button">all / none</button></div>
          <div id="committees"></div>
        </div>
        <div class="fgroup">
          <div class="flabel"><span>YEARS</span></div>
          <div class="yrow"><input id="yfrom" type="number" step="1"> <span>–</span> <input id="yto" type="number" step="1"></div>
        </div>
        <div class="fgroup">
          <div class="flabel"><span>DOCUMENT</span></div>
          <select id="docsel"></select>
        </div>
      </div>
    </div>
  </aside>

  <main class="main">
    <section class="panel" role="tabpanel" id="panel-0" aria-labelledby="tab-0">
      <h2 class="figtitle"><span class="figno">FIG.01</span>Paragraphs per committee</h2>
      <p class="hint">click a bar = tick that committee alone</p>
      <div class="figwrap">
        <div class="chartbox" id="chartbox">
          <canvas id="fig1" role="img" aria-label="Bar chart of paragraphs per committee">Your browser cannot draw the chart; the table beside it lists the same numbers.</canvas>
        </div>
        <p id="nohits" class="hint" hidden>No paragraphs match — no bars to draw.</p>
        <table class="figtable">
          <caption>Paragraphs per committee — the same numbers as FIG.01</caption>
          <thead><tr><th scope="col">Committee</th><th scope="col" class="num">Paragraphs</th></tr></thead>
          <tbody id="figtbody"></tbody>
        </table>
      </div>
      <p class="how">How this is computed: one count per committee over the paragraphs that match the query and filters. Joint General Comments count under both committees, so the bars can add up to more than the hits.</p>
    </section>

    <section class="panel" role="tabpanel" id="panel-1" aria-labelledby="tab-1" hidden>
      <p class="summary" id="summary" aria-live="polite"></p>
      <div class="orderrow">
        <label for="order">ORDER</label>
        <select id="order">
          <option value="year">year, newest first</option>
          <option value="doc">document order</option>
          <option value="matches">most matches first</option>
        </select>
        <span class="hint" id="orderhint"></span>
      </div>
      <p class="hint">This page retrieves; it never writes. Every paragraph shown is a record of the file, as stored.</p>
      <div id="results"></div>
      <button id="more" class="btn" type="button" hidden>Show 25 more</button>
    </section>

    <section class="panel" role="tabpanel" id="panel-2" aria-labelledby="tab-2" hidden>
      <h2 class="ptitle">Your draft (<span id="dn">0</span> quotations)</h2>
      <p class="hint" id="storehint"></p>
      <div class="draftbtns">
        <button class="btn" id="copyall" type="button">Copy all</button>
        <button class="btn" id="dltxt" type="button">Download .txt</button>
        <button class="btn" id="dlcsv" type="button">Download .csv</button>
      </div>
      <div id="draftlist"></div>
    </section>

    <section class="panel" role="tabpanel" id="panel-3" aria-labelledby="tab-3" hidden>
      <h2 class="ptitle">How the app checks itself</h2>
      <p class="hint">Run after every search, over the paragraphs that match. A failed check marks rows; it never drops them.</p>
      <div id="checks"></div>
      <h2 class="ptitle">Known quirks of this file</h2>
      <p class="hint">Computed once at load, before any search.</p>
      <div id="quirks"></div>
      <h2 class="ptitle">How this is computed</h2>
      <div id="method"></div>
    </section>
  </main>
</div>

<footer>
  <span id="footline"></span>
  <span>Credits: Chart.js 4 (MIT licence) renders FIG.01.</span>
</footer>

<div id="live" class="sr" aria-live="polite"></div>
<div id="copybox" hidden>
  <div class="cbhead"><span>Clipboard refused — select and copy</span><button id="cbclose" class="linkbtn" type="button">close</button></div>
  <textarea id="cbtext" readonly></textarea>
</div>

<script>
(function(){
'use strict';
var GC = window.WORKSHOP_DATA.gc;
var R = GC.records;
var FN = /\[\[fn:\d+\]\]/g;

function esc(s){ return String(s==null?'':s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;'); }
function fmt(n){ return Number(n).toLocaleString('en-US'); }
function normText(s){
  return String(s).replace(FN,'')
    .replace(/[“”„]/g,'"')
    .replace(/[‘’‚]/g,"'")
    .replace(/[‐-―­]/g,'-')
    .replace(/\s+/g,' ')
    .toLowerCase().trim();
}
function escRe(s){ return s.replace(/[.*+?^${}()|[\]\\]/g,'\\$&'); }

/* ---------- query: tokenise, parse, evaluate ---------- */
function termRe(text){
  var words = text.split(/\s+/).filter(Boolean).map(function(w){
    var wc = w.charAt(w.length-1)==='*';
    var core = wc ? w.slice(0,-1) : w;
    return escRe(core) + (wc ? '\\w*' : '');
  });
  return new RegExp('(?<![\\p{L}\\p{N}])' + words.join('\\s+') + '(?![\\p{L}\\p{N}])', 'u');
}
function hiPat(text){
  var words = text.split(/\s+/).filter(Boolean).map(function(w){
    var wc = w.charAt(w.length-1)==='*';
    var core = wc ? w.slice(0,-1) : w;
    var p='';
    for(var i=0;i<core.length;i++){
      var ch=core.charAt(i);
      if(ch==='"') p+='["“”„]';
      else if(ch==="'") p+="['‘’‚]";
      else if(ch==='-') p+='[-‐-―­]';
      else p+=escRe(ch);
    }
    return p + (wc?'\\w*':'');
  });
  return words.join('(?:\\s|\\[\\[fn:\\d+\\]\\])+');
}
function hiRe(terms, global){
  var body = terms.map(function(t){
    return '(?<![\\p{L}\\p{N}])(?:'+hiPat(t.text)+')(?![\\p{L}\\p{N}])';
  }).join('|');
  return new RegExp(body, 'iu'+(global?'g':''));
}
function tokenize(q){
  var toks=[], i=0, n=q.length;
  while(i<n){
    var c=q.charAt(i);
    if(/\s/.test(c)){ i++; continue; }
    if(c==='('||c===')'){ toks.push({k:c}); i++; continue; }
    if(c==='"'||c==='“'||c==='”'||c==='„'){
      var j=i+1, buf='';
      while(j<n && q.charAt(j)!=='"' && q.charAt(j)!=='”'){ buf+=q.charAt(j); j++; }
      if(j>=n) throw new Error('unbalanced quote — a phrase needs a closing double quote');
      toks.push({k:'term', text:buf, phrase:true}); i=j+1; continue;
    }
    var j2=i;
    while(j2<n && !/[\s()"“”„]/.test(q.charAt(j2))) j2++;
    var w=q.slice(i,j2);
    if(w==='AND') toks.push({k:'AND'});
    else if(w==='OR') toks.push({k:'OR'});
    else if(w==='NOT') toks.push({k:'NOT'});
    else if(w.charAt(0)==='-' && w.length>1) toks.push({k:'NOT'},{k:'term',text:w.slice(1)});
    else toks.push({k:'term', text:w});
    i=j2;
  }
  return toks;
}
function makeTerm(tok){
  var raw = tok.text.replace(/\s+/g,' ').trim();
  var text = normText(tok.text);
  if(!text) throw new Error('empty phrase');
  return {t:'term', raw:raw, text:text, phrase:!!tok.phrase, re:termRe(text)};
}
function parse(toks){
  var p=0;
  function peek(){ return toks[p]; }
  function parseOr(){
    var left=parseAnd();
    while(peek() && peek().k==='OR'){ p++; var r=parseAnd(); left={t:'or',a:left,b:r}; }
    return left;
  }
  function parseAnd(){
    var left=parseNot();
    while(peek() && (peek().k==='AND'||peek().k==='NOT'||peek().k==='term'||peek().k==='(')){
      if(peek().k==='AND') p++;
      var r=parseNot();
      left={t:'and',a:left,b:r};
    }
    return left;
  }
  function parseNot(){
    if(peek() && peek().k==='NOT'){ p++; return {t:'not', a:parseNot()}; }
    return parsePrim();
  }
  function parsePrim(){
    var tk=peek();
    if(!tk) throw new Error('unexpected end of query');
    if(tk.k==='('){ p++; var e=parseOr(); if(!peek()||peek().k!==')') throw new Error('unbalanced parenthesis'); p++; return e; }
    if(tk.k==='term'){ p++; return makeTerm(tk); }
    throw new Error('unexpected "'+tk.k+'"');
  }
  var tree=parseOr();
  if(p<toks.length) throw new Error('unexpected "'+toks[p].k+'"');
  return tree;
}
function evalTree(n, s){
  if(n.t==='term') return n.re.test(s);
  if(n.t==='not') return !evalTree(n.a, s);
  if(n.t==='and') return evalTree(n.a,s) && evalTree(n.b,s);
  return evalTree(n.a,s) || evalTree(n.b,s);
}
function collectTerms(n, neg, out){
  if(n.t==='term'){ if(!neg) out.push(n); return; }
  if(n.t==='not'){ collectTerms(n.a, true, out); return; }
  collectTerms(n.a, neg, out); collectTerms(n.b, neg, out);
}
function countTerms(n){
  if(n.t==='term') return 1;
  if(n.t==='not') return countTerms(n.a);
  return countTerms(n.a)+countTerms(n.b);
}
function echoTree(n){
  if(n.t==='term'){
    if(n.phrase) return 'the phrase “'+n.raw+'”';
    if(n.text.charAt(n.text.length-1)==='*') return 'the word '+n.raw+' (any ending)';
    return 'the word '+n.raw;
  }
  if(n.t==='not') return 'without '+echoTree(n.a);
  if(n.t==='and') return echoTree(n.a)+' and '+echoTree(n.b);
  return echoTree(n.a)+' or '+echoTree(n.b);
}
function echoLine(){
  if(!state.tree) return '';
  if(state.tree.t==='not') return 'Paragraphs without '+echoTree(state.tree.a)+' — a NOT-only query matches everything that lacks these terms';
  return 'Paragraphs containing '+echoTree(state.tree);
}

/* ---------- precompute records once at load ---------- */
var symbolTitles=new Map();
R.forEach(function(r){
  var s=symbolTitles.get(r.symbol);
  if(!s){ s=new Set(); symbolTitles.set(r.symbol,s); }
  s.add(r.title);
});
var dupPin=new Map();
R.forEach(function(r){ var k=r.title+'|'+r.paragraph; dupPin.set(k,(dupPin.get(k)||0)+1); });

var FULL={
  'CAT':'Committee against Torture',
  'CAT-OP':'Subcommittee on Prevention of Torture (SPT)',
  'CCPR':'Human Rights Committee',
  'CED':'Committee on Enforced Disappearances',
  'CEDAW':'Committee on the Elimination of Discrimination against Women',
  'CERD':'Committee on the Elimination of Racial Discrimination',
  'CESCR':'Committee on Economic, Social and Cultural Rights',
  'CMW':'Committee on Migrant Workers',
  'CRC':'Committee on the Rights of the Child',
  'CRPD':'Committee on the Rights of Persons with Disabilities'
};
var SYMRE=/\b(CAT|CCPR|CED|CEDAW|CERD|CESCR|CMW|CRC|CRPD)\b/g;
function docName(t){ var m=String(t).match(/^(.*?)(?::|\son\b)/); return (m?m[1]:t).trim(); }

var recs=R.map(function(r){
  var text=String(r.text);
  var shown=text.replace(FN,'');
  var marks=(text.match(FN)||[]).length;
  var norm=normText(text);
  var lm=text.match(/^(\d{1,3})\.\s/);
  var leading=lm?parseInt(lm[1],10):null;
  var sm=text.match(/^\(([a-z]{1,4})\)/);
  var para=Number(r.paragraph);
  var pinpoint = sm ? 'subpara. ('+sm[1]+')' : (para===0 ? 'preamble' : 'para. '+r.paragraph);
  var codes=new Set();
  var found=String(r.symbol).match(SYMRE)||[];
  found.forEach(function(c){ codes.add(c); });
  if(/CAT\/OP/.test(r.symbol)) codes.add('CAT-OP');
  if(r.committee) codes.add(r.committee);
  var o={ r:r, shown:shown, marks:marks, norm:norm, leading:leading, sub:sm?sm[1]:null,
          pinpoint:pinpoint, committees:Array.from(codes), joint:found.length>1,
          shared:symbolTitles.get(r.symbol).size>1 };
  o.citation = o.shared
    ? (r.committee+', '+docName(r.title)+' ('+r.symbol+'), '+pinpoint)
    : (r.symbol+', '+pinpoint);
  var c=shown;
  if(o.leading!==null && o.leading===para) c=c.replace(/^\d{1,3}\.\s/,'');
  o.copied=c;
  o.quotation='“'+c+'” '+o.citation;
  return o;
});
var byId=new Map(recs.map(function(o){ return [o.r.id,o]; }));
var titleMap=new Map();
recs.forEach(function(o){
  var a=titleMap.get(o.r.title);
  if(!a){ a=[]; titleMap.set(o.r.title,a); }
  a.push(o);
});
titleMap.forEach(function(a){ a.sort(function(x,y){ return Number(x.r.paragraph)-Number(y.r.paragraph); }); });

var codeCounts=new Map();
recs.forEach(function(o){ o.committees.forEach(function(c){ codeCounts.set(c,(codeCounts.get(c)||0)+1); }); });
var allCodes=Array.from(codeCounts.keys()).sort(function(a,b){ return (codeCounts.get(b)-codeCounts.get(a)) || a.localeCompare(b); });
var years=R.map(function(r){ return Number(r.year)||0; });
var minYear=Math.min.apply(null,years), maxYear=Math.max.apply(null,years);
var titles=new Set(R.map(function(r){ return r.title; }));

var docList=[], seenT={};
recs.forEach(function(o){
  if(!seenT[o.r.title]){
    seenT[o.r.title]=1;
    docList.push({title:o.r.title, committee:o.r.committee||'', short:o.r.short_title||o.r.title, year:o.r.year});
  }
});
docList.sort(function(a,b){ return a.committee.localeCompare(b.committee) || String(a.short).localeCompare(String(b.short)); });
var docByTitle=new Map(docList.map(function(d){ return [d.title,d]; }));

/* ---------- state ---------- */
var storeOK=true;
try{ localStorage.setItem('__vgc','1'); localStorage.removeItem('__vgc'); }catch(e){ storeOK=false; }
function loadDraft(){
  try{
    var s=localStorage.getItem('verbatim-gc-draft');
    if(s){ var a=JSON.parse(s); if(Array.isArray(a)) return a; }
  }catch(e){}
  return [];
}
function saveDraft(){
  if(!storeOK) return;
  try{ localStorage.setItem('verbatim-gc-draft', JSON.stringify(state.draft)); }catch(e){ storeOK=false; }
}
var state={
  tree:null, error:null, query:'',
  ticked:new Set(allCodes),
  yFrom:minYear, yTo:maxYear, doc:'',
  order:'year', shown:25,
  hits:[], hi:null, hiTest:null, checks:[],
  rowState:new Map(),
  draft:loadDraft()
};
var perComm=new Map(), titleHits=new Map();

/* ---------- elements ---------- */
function $(id){ return document.getElementById(id); }
var qInput=$('q'), searchbtn=$('searchbtn'), syntaxEl=$('syntax'), echoEl=$('echo'), qerr=$('qerr'),
    bignum=$('bignum'), oftotal=$('oftotal'), chipsEl=$('chips'),
    fhead=$('fhead'), fbody=$('fbody'), committeesEl=$('committees'), allnoneBtn=$('allnone'),
    yfrom=$('yfrom'), yto=$('yto'), docsel=$('docsel'), clearallBtn=$('clearall'),
    rail=$('rail'), summaryEl=$('summary'), orderSel=$('order'), orderhint=$('orderhint'),
    resultsEl=$('results'), moreBtn=$('more'),
    dcount=$('dcount'), dn=$('dn'), draftList=$('draftlist'), storehint=$('storehint'),
    checksEl=$('checks'), statusEl=$('checkstatus'), tab4dot=$('tab4dot'),
    liveEl=$('live'), copybox=$('copybox'), cbtext=$('cbtext');
var panels=[0,1,2,3].map(function(i){ return $('panel-'+i); });
var tabs=Array.prototype.slice.call(document.querySelectorAll('.tabs [role=tab]'));
var orderText={
  year:'sorted by year, newest first, then by document and paragraph',
  doc:'sorted by document, then paragraph',
  matches:'sorted by most matches first, then year, document and paragraph'
};

/* ---------- filtering / matching ---------- */
function passes(o){
  var okC=false;
  for(var i=0;i<o.committees.length;i++) if(state.ticked.has(o.committees[i])){ okC=true; break; }
  if(!okC) return false;
  var y=Number(o.r.year)||0;
  if(y<state.yFrom || y>state.yTo) return false;
  if(state.doc && o.r.title!==state.doc) return false;
  return true;
}
function sortHits(){
  var h=state.hits;
  if(state.order==='doc'){
    h.sort(function(a,b){ return a.r.title.localeCompare(b.r.title) || (Number(a.r.paragraph)-Number(b.r.paragraph)); });
  } else if(state.order==='matches'){
    h.sort(function(a,b){
      return (titleHits.get(b.r.title)||0)-(titleHits.get(a.r.title)||0)
        || b.r.year-a.r.year || a.r.title.localeCompare(b.r.title)
        || (Number(a.r.paragraph)-Number(b.r.paragraph));
    });
  } else {
    h.sort(function(a,b){
      return b.r.year-a.r.year || a.r.title.localeCompare(b.r.title)
        || (Number(a.r.paragraph)-Number(b.r.paragraph));
    });
  }
}
function buildHi(){
  var pos=[];
  if(state.tree) collectTerms(state.tree,false,pos);
  state.hi = pos.length ? hiRe(pos,true) : null;
  state.hiTest = pos.length ? hiRe(pos,false) : null;
}
function run(){
  var hits=[];
  for(var i=0;i<recs.length;i++){
    var o=recs[i];
    if(!passes(o)) continue;
    if(state.tree && !evalTree(state.tree,o.norm)) continue;
    hits.push(o);
  }
  state.hits=hits;
  perComm.clear();
  hits.forEach(function(o){ o.committees.forEach(function(c){ perComm.set(c,(perComm.get(c)||0)+1); }); });
  titleHits.clear();
  hits.forEach(function(o){ titleHits.set(o.r.title,(titleHits.get(o.r.title)||0)+1); });
  sortHits();
  buildHi();
  renderRail(); renderChips(); renderCommittees(); renderOverview(); renderResults(); runChecks();
}

/* ---------- rendering: rail ---------- */
function renderRail(){
  bignum.textContent=fmt(state.hits.length);
  oftotal.textContent='matching paragraphs of '+fmt(R.length);
}
function renderChips(){
  var chips=[];
  if(state.ticked.size<allCodes.length) chips.push({k:'comm', label:'committees '+state.ticked.size+'/'+allCodes.length});
  if(state.yFrom>minYear || state.yTo<maxYear) chips.push({k:'years', label:'years '+state.yFrom+'–'+state.yTo});
  if(state.doc){ var d=docByTitle.get(state.doc); chips.push({k:'doc', label:'document: '+(d?d.short:state.doc)}); }
  chipsEl.innerHTML=chips.map(function(c){
    return '<button type="button" class="chip" data-chip="'+c.k+'" title="remove this filter">'+esc(c.label)+' ✕</button>';
  }).join('');
}
function renderCommittees(){
  committeesEl.innerHTML=allCodes.map(function(c){
    return '<label class="ck"><input type="checkbox" data-code="'+esc(c)+'"'+(state.ticked.has(c)?' checked':'')+'>'
      +'<span class="code">'+esc(c)+'</span><span class="nm">'+esc(FULL[c]||c)+'</span>'
      +'<span class="hits">['+fmt(perComm.get(c)||0)+']</span></label>';
  }).join('');
}
function syncYears(){ yfrom.value=state.yFrom; yto.value=state.yTo; }

/* ---------- rendering: FIG.01 ---------- */
var chart=null;
function renderOverview(){
  var data=Array.from(perComm.entries()).filter(function(e){ return e[1]>0; })
    .sort(function(a,b){ return b[1]-a[1]; });
  var labels=data.map(function(e){ return e[0]; }), vals=data.map(function(e){ return e[1]; });
  var box=$('chartbox'), cv=$('fig1');
  if(!data.length){
    box.hidden=true; $('nohits').hidden=false; $('figtbody').innerHTML='';
    cv.setAttribute('aria-label','No paragraphs match, so the chart is empty.');
    return;
  }
  box.hidden=false; $('nohits').hidden=true;
  box.style.height=Math.max(180, labels.length*30+70)+'px';
  cv.setAttribute('aria-label','Bar chart, paragraphs per committee: '+data.map(function(e){ return e[0]+' '+fmt(e[1]); }).join('; '));
  if(window.Chart){
    if(!chart){
      chart=new Chart(cv.getContext('2d'),{
        type:'bar',
        data:{labels:labels, datasets:[{data:vals, backgroundColor:'#9b2335', borderWidth:0, barPercentage:0.85, categoryPercentage:0.9}]},
        options:{
          indexAxis:'y', responsive:true, maintainAspectRatio:false,
          onClick:function(evt){
            var pts=chart.getElementsAtEventForMode(evt.nativeEvent||evt,'nearest',{intersect:true},true);
            if(pts && pts.length) tickAlone(chart.data.labels[pts[0].index]);
          },
          scales:{
            x:{beginAtZero:true, border:{color:'#d9d2c3'}, grid:{color:'#e6dfd0'},
               ticks:{color:'#1d1b18', maxTicksLimit:10, precision:0, font:{family:'ui-monospace, Menlo, Consolas, monospace', size:11}}},
            y:{grid:{display:false}, border:{display:false},
               ticks:{color:'#1d1b18', font:{family:'ui-monospace, Menlo, Consolas, monospace', size:11}}}
          },
          plugins:{
            legend:{display:false},
            tooltip:{callbacks:{label:function(c){ return ' '+fmt(c.parsed.x)+' paragraphs'; }}}
          }
        },
        plugins:[{ id:'vals', afterDatasetsDraw:function(ch){
          var meta=ch.getDatasetMeta(0), ctx=ch.ctx;
          ctx.save();
          ctx.fillStyle='#1d1b18'; ctx.font='12px ui-monospace, Menlo, Consolas, monospace';
          ctx.textAlign='left'; ctx.textBaseline='middle';
          meta.data.forEach(function(bar,i){ ctx.fillText(fmt(ch.data.datasets[0].data[i]), bar.x+6, bar.y); });
          ctx.restore();
        }}]
      });
    } else {
      chart.data.labels=labels;
      chart.data.datasets[0].data=vals;
      chart.update();
    }
  } else { box.hidden=true; }
  $('figtbody').innerHTML=data.map(function(e){
    return '<tr><th scope="row">'+esc(e[0])+'</th><td class="num">'+fmt(e[1])+'</td></tr>';
  }).join('');
}
function tickAlone(code){
  state.ticked=new Set([code]);
  renderCommittees(); state.shown=25; run();
}

/* ---------- rendering: results ---------- */
function getRowState(id){
  var s=state.rowState.get(id);
  if(!s){ s={open:false, full:false, stored:false, ctx:null}; state.rowState.set(id,s); }
  return s;
}
function cut700(t){ var c=t.slice(0,700); var sp=c.lastIndexOf(' '); if(sp>350) c=c.slice(0,sp); return c; }
function wordCount(t){ return t.split(/\s+/).filter(Boolean).length; }
function highlightHTML(t){
  if(!state.hi) return esc(t);
  state.hi.lastIndex=0;
  var out='', last=0, m;
  while((m=state.hi.exec(t))){
    if(m[0].length===0){ state.hi.lastIndex++; continue; }
    out+=esc(t.slice(last,m.index))+'<mark>'+esc(m[0])+'</mark>';
    last=m.index+m[0].length;
  }
  out+=esc(t.slice(last));
  return out;
}
function metaHTML(o){
  var badges=o.committees.map(function(c){ return '<span class="badge">'+esc(c)+'</span>'; }).join(' ');
  return '<span class="meta">'+badges+' <span class="doc">'+esc(o.r.short_title)+'</span>'
    +' · <span class="sym"><a href="'+esc(o.r.doc_url)+'" target="_blank" rel="noopener">'+esc(o.r.symbol)+'</a></span>'
    +' · <span class="pin">'+esc(o.pinpoint)+'</span>'
    +' · <span class="yr">'+esc(o.r.year)+'</span></span>';
}
function textHTML(o,st){
  var t = st.stored ? String(o.r.text) : o.shown;
  var html;
  if(st.full || t.length<=700) html=highlightHTML(t);
  else html=highlightHTML(cut700(t))+' … <button type="button" class="linkbtn" data-action="full">Show the full paragraph ('+fmt(wordCount(o.shown))+' words)</button>';
  return '<p class="rtext">'+html+'</p>';
}
function marksLineHTML(o,st){
  if(o.marks>0){
    return '<div class="marksline">'+o.marks+' footnote mark'+(o.marks>1?'s':'')+' removed · '
      +'<button type="button" class="linkbtn" data-action="stored">'+(st.stored?'show without marks':'show as stored')+'</button></div>';
  }
  return '<div class="marksline">no footnote marks in this paragraph</div>';
}
function notesHTML(o){
  var notes=[];
  if(o.leading!==null && o.leading!==Number(o.r.paragraph))
    notes.push('the text begins ‘'+o.leading+’.’ but the record is '+o.pinpoint+': check the document');
  if(o.sub) notes.push('a lettered sub-paragraph, numbered '+o.r.paragraph+' by the file');
  if(dupPin.get(o.r.title+'|'+o.r.paragraph)>1) notes.push('two records share this pinpoint');
  if(o.joint) notes.push('joint General Comment');
  return notes.length ? '<div class="note">'+notes.map(esc).join('<br>')+'</div>' : '';
}
function ctxHTML(o,dir){
  var arr=titleMap.get(o.r.title)||[], idx=-1;
  for(var i=0;i<arr.length;i++) if(arr[i].r.id===o.r.id){ idx=i; break; }
  var sib = dir==='prev' ? (idx>0?arr[idx-1]:null) : (idx>=0&&idx<arr.length-1?arr[idx+1]:null);
  if(!sib) return '<span class="hint">no '+(dir==='prev'?'previous':'next')+' paragraph in this document</span>';
  return '<span class="pin">'+esc(sib.pinpoint)+'</span> '+esc(sib.shown);
}
function detailHTML(o,st){
  return '<div class="btns">'
    +'<button type="button" class="btn" data-action="cite">Copy citation</button>'
    +'<button type="button" class="btn" data-action="quote">Copy quotation</button>'
    +'<button type="button" class="btn primary" data-action="draft">Add to draft</button>'
    +'</div>'
    +'<p class="hint">citation style: UN short form</p>'
    +'<div class="ctx">Context: <button type="button" class="linkbtn" data-action="ctxprev">previous</button> | <button type="button" class="linkbtn" data-action="ctxnext">next</button></div>'
    +'<div class="ctxblock"'+(st.ctx?'':' hidden')+'>'+(st.ctx?ctxHTML(o,st.ctx):'')+'</div>';
}
function buildRow(o){
  var st=getRowState(o.r.id);
  var art=document.createElement('article');
  art.className='row'; art.dataset.id=o.r.id;
  var h=document.createElement('h3'); h.className='rowh';
  var btn=document.createElement('button');
  btn.type='button'; btn.className='rowhead';
  btn.setAttribute('aria-expanded', st.open?'true':'false');
  btn.innerHTML=metaHTML(o);
  h.appendChild(btn); art.appendChild(h);
  var body=document.createElement('div'); body.className='rbody';
  body.innerHTML=textHTML(o,st)+marksLineHTML(o,st)+notesHTML(o);
  art.appendChild(body);
  var det=document.createElement('div'); det.className='detail';
  det.hidden=!st.open; det.innerHTML=detailHTML(o,st);
  art.appendChild(det);
  return art;
}
function refreshRow(art,o,st){
  art.querySelector('.rowhead').setAttribute('aria-expanded', st.open?'true':'false');
  art.querySelector('.rbody').innerHTML=textHTML(o,st)+marksLineHTML(o,st)+notesHTML(o);
  var det=art.querySelector('.detail');
  det.hidden=!st.open; det.innerHTML=detailHTML(o,st);
}
function renderResults(){
  var hits=state.hits, n=hits.length;
  var commSet=new Set();
  hits.forEach(function(o){ o.committees.forEach(function(c){ commSet.add(c); }); });
  var s;
  if(n){
    var ys=hits.map(function(o){ return Number(o.r.year)||0; });
    s=fmt(n)+' of '+fmt(R.length)+' paragraphs match · '+commSet.size+' committees · '+Math.min.apply(null,ys)+'–'+Math.max.apply(null,ys);
  } else s='0 of '+fmt(R.length)+' paragraphs match';
  if(!state.tree && !state.error) s+=' · no search words';
  summaryEl.textContent=s;
  orderhint.textContent=orderText[state.order];
  resultsEl.innerHTML='';
  var frag=document.createDocumentFragment();
  var upto=Math.min(state.shown,n);
  for(var i=0;i<upto;i++) frag.appendChild(buildRow(hits[i]));
  resultsEl.appendChild(frag);
  moreBtn.hidden = upto>=n;
  if(n>upto) moreBtn.textContent='Show 25 more ('+fmt(n-upto)+' left)';
  if(state.error){ qerr.textContent=state.error; echoEl.textContent=''; }
  else{
    qerr.textContent='';
    echoEl.textContent = state.tree ? echoLine() : 'no search words — every paragraph that passes the filters is listed, paged';
  }
}

/* ---------- checks ---------- */
function runChecks(){
  var hits=state.hits, cs=[];
  if(state.error){
    cs.push({name:'Query understood', ok:false, detail:'parse error — '+state.error+'. No results are shown.'});
  } else if(!state.tree){
    cs.push({name:'Query understood', ok:true, detail:'no search words — the empty query matches every paragraph that passes the filters'});
  } else {
    cs.push({name:'Query understood', ok:true, detail:countTerms(state.tree)+' term(s) — '+echoLine()});
  }
  var jointHits=hits.filter(function(o){ return o.committees.length>1; }).length;
  var sum=0; perComm.forEach(function(v){ sum+=v; });
  cs.push({name:'Totals', ok:sum===hits.length+jointHits,
    detail:'rows listed across all pages = '+fmt(hits.length)+' hits; the committees’ bracketed counts sum to '+fmt(sum)+' = '+fmt(hits.length)+' hits + '+fmt(jointHits)+' joint hits'});
  cs.push({name:'Chart total (FIG.01)', ok:sum===hits.length+jointHits,
    detail:'the bars sum to '+fmt(sum)+'; hits '+fmt(hits.length)+' + joint hits '+fmt(jointHits)});
  var pos=[]; if(state.tree) collectTerms(state.tree,false,pos);
  if(!pos.length){
    cs.push({name:'Highlight', ok:true, detail:'NOT-only query — no terms to highlight'});
  } else {
    var bad=hits.filter(function(o){ state.hiTest.lastIndex=0; return !state.hiTest.test(o.shown); });
    cs.push({name:'Highlight', ok:bad.length===0,
      detail: bad.length===0
        ? 'every one of the '+fmt(hits.length)+' hits shows at least one highlighted match'
        : fmt(bad.length)+' hit(s) matched in the normalised text but show no highlight: '+bad.slice(0,5).map(function(o){ return o.citation; }).join('; ')});
  }
  var q=state.query, straight=['"',"'",'-'].filter(function(c){ return q.indexOf(c)>=0; });
  if(straight.length){
    var onlyVar=0;
    hits.forEach(function(o){
      var t=String(o.r.text), hasS=false, hasV=false;
      straight.forEach(function(c){
        if(t.indexOf(c)>=0) hasS=true;
        if(c==='"' && /[“”„]/.test(t)) hasV=true;
        if(c==="'" && /[‘’‚]/.test(t)) hasV=true;
        if(c==='-' && /[‐-―­]/.test(t)) hasV=true;
      });
      if(hasV && !hasS) onlyVar++;
    });
    cs.push({name:'Normalisation', ok:true,
      detail:'the query contains a straight quote, apostrophe or hyphen; curly and dash forms were matched too — '+fmt(onlyVar)+' of '+fmt(hits.length)+' hits contain only the curly/dash forms'});
  } else {
    cs.push({name:'Normalisation', ok:true, detail:'the query contains no straight quote, apostrophe or hyphen'});
  }
  var mism=hits.filter(function(o){ return o.leading!==null && o.leading!==Number(o.r.paragraph); });
  var subs=hits.filter(function(o){ return !!o.sub; });
  var dups=hits.filter(function(o){ return dupPin.get(o.r.title+'|'+o.r.paragraph)>1; });
  cs.push({name:'Numbering', ok:true,
    detail: fmt(mism.length)+' leading-number mismatch(es) ('+(mism.slice(0,3).map(function(o){ return o.citation+' — text begins '+o.leading+'.'; }).join('; ')||'none')+'); '
      +fmt(dups.length)+' shared pinpoint(s); '+fmt(subs.length)+' lettered sub-paragraph(s) — each is flagged on its row'});
  var mbad=0;
  hits.forEach(function(o){
    var c=(String(o.r.text).match(/\[\[fn:/g)||[]).length;
    if(c!==o.marks || String(o.r.text).replace(FN,'')!==o.shown) mbad++;
  });
  cs.push({name:'Footnote marks', ok:mbad===0,
    detail:'for '+fmt(hits.length)+' hits, the marks removed equal the count of [[fn: in the stored text, and removing them reproduces the shown text exactly'+(mbad?'; '+mbad+' mismatch(es)':'')});
  var dbad=state.draft.filter(function(it){ var o=byId.get(it.id); return !o || o.r.text!==it.text_as_stored; });
  cs.push({name:'Draft', ok:dbad.length===0,
    detail: fmt(state.draft.length)+' draft item(s) re-checked against the stored text of their record'+(dbad.length?'; '+dbad.length+' differ(s)':'')});
  state.checks=cs;
  checksEl.innerHTML=cs.map(function(c){
    return '<div class="check"><span class="st '+(c.ok?'pass':'fail')+'">'+(c.ok?'pass':'check failed')+'</