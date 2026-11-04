I built the verbatim finder on the attached General Comments, following your plan tab by tab. It searches with Boolean operators, phrases and a trailing star. It shows each paragraph as stored and copies a citation built only from the record's fields. A draft tab collects quotations. No model is called and nothing leaves the browser. Downloads and the clipboard may be blocked in this sandbox; if so, the app shows the exact text in a box to select and copy.

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Verbatim finder: General Comments and General Recommendations</title>
<style>
*{box-sizing:border-box}
body{margin:0;background:#f4f0e8;color:#1d1b18;font:16px/1.5 system-ui,-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
[hidden]{display:none!important}
a{color:#9b2335}
button,input,select,textarea{font:inherit;color:inherit}
button{cursor:pointer}
:focus-visible{outline:3px solid #9b2335;outline-offset:2px}
.mono,.lbl,.hint,.btn,.tab{font-family:ui-monospace,Menlo,Consolas,monospace}
.lbl{font-size:12px;letter-spacing:.08em;text-transform:uppercase;color:#5e5850}
.hint{font-size:12px;line-height:1.45;color:#5e5850;margin:4px 0}
.serif,h1,h2,.num{font-family:Georgia,"Times New Roman",serif}
header.top{padding:16px 28px 0;border-bottom:1px solid #d9d2c3}
.titlerow{display:flex;justify-content:space-between;align-items:flex-start;gap:16px;flex-wrap:wrap}
h1{font-size:28px;line-height:1.2;margin:4px 0 6px;font-weight:700}
.sub{margin:0 0 12px;font-size:14px;color:#3b3731}
.status{font:12px ui-monospace,Menlo,Consolas,monospace;display:flex;align-items:center;gap:6px;padding-top:8px}
.dot{display:inline-block;width:10px;height:10px;border-radius:50%;background:#1f6b3a}
.dot.bad{background:#b3261e}
[role=tablist]{display:flex;gap:4px;flex-wrap:wrap}
.tab{background:none;border:0;border-bottom:3px solid transparent;padding:10px 14px;font-size:12px;letter-spacing:.08em;text-transform:uppercase;color:#3b3731}
.tab[aria-selected=true]{color:#9b2335;border-bottom-color:#9b2335;font-weight:700}
.tab .dot{width:8px;height:8px;margin-left:6px}
.layout{display:grid;grid-template-columns:310px minmax(0,1fr)}
.layout.nr{grid-template-columns:minmax(0,1fr)}
.rail{padding:16px 20px;border-right:1px solid #d9d2c3;min-width:0}
main{padding:18px 28px 40px;min-width:0}
.railhead{display:flex;justify-content:space-between;align-items:baseline}
.lnk{background:none;border:0;padding:0;color:#9b2335;text-decoration:underline;font-size:13px}
.bignum{margin:10px 0 6px;border-bottom:1px solid #d9d2c3;padding-bottom:10px}
.num{font-size:52px;line-height:1;color:#1d1b18;display:block}
.bignum .of{font-size:13px;color:#5e5850}
.chips{display:flex;flex-wrap:wrap;gap:6px;margin:8px 0}
.chip{border:1px solid #9b2335;color:#9b2335;background:none;border-radius:14px;padding:1px 10px;font-size:13px}
.qrow{display:flex;gap:6px;margin-top:4px}
.qrow input{flex:1;min-width:0;padding:8px;border:1px solid #1d1b18;background:#fffdf8}
.btn{border:1px solid #1d1b18;background:transparent;padding:7px 12px;font-size:12px;letter-spacing:.05em;text-transform:uppercase}
.btn.pri{background:#9b2335;border-color:#9b2335;color:#fff}
.qhelp{border:1px solid #d9d2c3;background:#fffdf8;padding:8px 10px;margin-top:4px;font-size:14px}
.qhelp ul{margin:4px 0 8px;padding-left:18px}
.qhelp li{margin:2px 0}
.ex{display:block;width:100%;text-align:left;background:none;border:0;border-top:1px solid #e6e0d2;padding:6px 2px;font:13px ui-monospace,Menlo,Consolas,monospace}
.ex:hover,.ex:focus{background:#efe9db}
#echo{font-size:14px;margin:6px 0;min-height:1px}
#qerr{color:#b3261e;font-size:14px;margin:6px 0}
.fh{margin:14px 0 0;border-top:1px solid #d9d2c3;font-size:12px}
.fh button{width:100%;text-align:left;background:none;border:0;padding:10px 0;font:12px ui-monospace,Menlo,Consolas,monospace;letter-spacing:.08em;text-transform:uppercase}
.fh button::after{content:"+";float:right}
.fh button[aria-expanded=true]::after{content:"–"}
.fh button[aria-expanded=true]{color:#9b2335;font-weight:700}
#fp label.cb{display:flex;gap:6px;align-items:baseline;font-size:14px;padding:2px 0}
#fp input[type=checkbox]{accent-color:#9b2335}
#fp .cn{color:#5e5850;font-size:12px}
#fp .yr{display:flex;gap:8px;align-items:center;margin:4px 0}
#fp input[type=number]{width:84px;padding:5px;border:1px solid #1d1b18;background:#fffdf8}
#fp select{width:100%;padding:6px;border:1px solid #1d1b18;background:#fffdf8;font-size:14px}
#fp .sec{margin:12px 0 4px}
h2{font-size:22px;margin:0 0 4px;font-weight:700}
.sumline{font:20px/1.3 Georgia,"Times New Roman",serif;margin:0 0 4px}
.orderrow{display:flex;gap:10px;align-items:center;flex-wrap:wrap;margin:4px 0}
.orderrow select{padding:5px;border:1px solid #1d1b18;background:#fffdf8}
.fig{display:flex;gap:28px;flex-wrap:wrap;align-items:flex-start;margin-top:10px}
.figchart{flex:1 1 380px;min-width:300px;position:relative}
table{border-collapse:collapse;font-size:15px}
caption{text-align:left;font:12px ui-monospace,Menlo,Consolas,monospace;color:#5e5850;padding-bottom:4px}
th,td{padding:4px 10px;border-bottom:1px solid #d9d2c3;text-align:left;vertical-align:top}
th{font:12px ui-monospace,Menlo,Consolas,monospace;text-transform:uppercase;letter-spacing:.05em;color:#5e5850}
td.r,th.r{text-align:right}
.row{border-top:1px solid #d9d2c3;padding:12px 0;cursor:pointer}
.row.open{background:#efe9db;padding:12px 10px;cursor:default}
.row h3{margin:0;font-size:16px}
.rt{background:none;border:0;padding:0;text-align:left;font-weight:600;cursor:pointer}
.badge{display:inline-block;border:1px solid #1d1b18;padding:0 6px;margin-right:6px;font:11px ui-monospace,Menlo,Consolas,monospace;font-weight:400;letter-spacing:.04em}
.meta{font-size:14px;margin:2px 0}
.pin{color:#9b2335;font:700 13px ui-monospace,Menlo,Consolas,monospace}
.txt{white-space:pre-wrap;max-width:80ch;margin:6px 0}
mark{background:#fbe9a6;color:#1d1b18;font-weight:700;padding:0 1px}
.fnl{font-size:13px;color:#5e5850;margin:2px 0}
.note{font-size:14px;color:#8a5a00;margin:3px 0}
.detail{border-top:1px dashed #b9b09b;margin-top:8px;padding-top:8px}
.btns{display:flex;gap:8px;flex-wrap:wrap}
.ctx{color:#5e5850;border-left:3px solid #cfc7b4;padding-left:10px;margin:8px 0}
.empty{color:#3b3731;border-top:1px solid #d9d2c3;padding-top:12px}
ul.chk{list-style:none;padding:0;margin:0}
ul.chk li{border-top:1px solid #d9d2c3;padding:8px 0;font-size:15px}
.ok{color:#1f6b3a;font:700 12px ui-monospace,Menlo,Consolas,monospace;text-transform:uppercase;margin-right:6px}
.fail{color:#b3261e;font:700 12px ui-monospace,Menlo,Consolas,monospace;text-transform:uppercase;margin-right:6px}
ul.plain{padding-left:18px;margin:6px 0}
ul.plain li{margin:4px 0;font-size:15px}
.dr{border-top:1px solid #d9d2c3;padding:10px 0;list-style:none}
.dr blockquote{margin:0;white-space:pre-wrap;max-width:80ch;font-family:Georgia,serif}
.dr p{margin:4px 0}
ul.drl{padding:0;margin:12px 0}
footer{border-top:1px solid #d9d2c3;padding:12px 28px 90px;font:11px/1.5 ui-monospace,Menlo,Consolas,monospace;color:#5e5850}
#copied{position:fixed;left:0;right:0;bottom:0;background:#fffdf8;border-top:3px solid #9b2335;padding:8px 28px;max-height:38vh;overflow:auto;font-size:14px;z-index:5}
#copied pre{white-space:pre-wrap;margin:4px 0;font:13px ui-monospace,Menlo,Consolas,monospace}
#copied textarea{width:100%;height:90px;font:13px ui-monospace,Menlo,Consolas,monospace}
.sr{position:absolute;left:-9999px}
@media(max-width:860px){.layout{grid-template-columns:1fr}.rail{border-right:0;border-bottom:1px solid #d9d2c3}main{padding:16px}header.top{padding:14px 16px 0}}
</style>
</head>
<body>
<header class="top">
  <div class="lbl">UN TREATY BODIES · GENERAL COMMENTS</div>
  <div class="titlerow">
    <h1>Verbatim finder: General Comments and General Recommendations</h1>
    <div id="status" class="status" aria-live="polite"></div>
  </div>
  <p class="sub" id="sub"></p>
  <div role="tablist" aria-label="Views">
    <button class="tab" role="tab" id="t0" aria-controls="p0">01 Overview</button>
    <button class="tab" role="tab" id="t1" aria-controls="p1">02 Paragraphs</button>
    <button class="tab" role="tab" id="t2" aria-controls="p2">03 Draft (0)</button>
    <button class="tab" role="tab" id="t3" aria-controls="p3">04 Check &amp; method<span class="dot" id="t3dot" hidden></span></button>
  </div>
</header>

<div class="layout" id="layout">
  <aside class="rail" id="rail" aria-label="Filters">
    <div class="railhead"><span class="lbl">Filters</span><button class="lnk" id="clear">Clear all</button></div>
    <div class="bignum" aria-live="polite"><span class="num" id="bn">0</span><span>matching paragraphs</span><div class="of">of <span id="bt"></span></div></div>
    <div class="chips" id="chips"></div>
    <label for="q" class="lbl">Search</label>
    <div class="qrow"><input id="q" type="text" autocomplete="off" spellcheck="false" aria-describedby="qnote" aria-controls="qhelp" placeholder='e.g. "best interests" AND child*'><button class="btn pri" id="go">Search</button></div>
    <div class="qhelp" id="qhelp" hidden></div>
    <p class="hint" id="qnote">Whole words, any case. Curly and straight quotes, apostrophes, dashes and hyphens count as the same, and footnote marks are skipped, so State's finds State’s and a phrase can cross a footnote.</p>
    <p id="echo" aria-live="polite"></p>
    <p id="qerr" role="alert" hidden></p>
    <h2 class="fh"><button id="fb" aria-expanded="false" aria-controls="fp">01 Committee, years, document</button></h2>
    <div id="fp" hidden>
      <div class="sec"><span class="lbl">Committee</span> <button class="lnk" id="call">all</button> / <button class="lnk" id="cnone">none</button></div>
      <div id="clist"></div>
      <div class="sec"><span class="lbl">Years</span></div>
      <div class="yr"><label for="yf" class="hint">from</label><input type="number" id="yf"><label for="yt" class="hint">to</label><input type="number" id="yt"></div>
      <div class="sec"><label for="doc" class="lbl">Document</label></div>
      <select id="doc"><option value="">All documents</option></select>
    </div>
  </aside>

  <main>
    <section id="p0" role="tabpanel" aria-labelledby="t0">
      <div class="lbl">Which committees say this?</div>
      <h2>FIG.01 Paragraphs per committee</h2>
      <p class="hint">click a bar = tick that committee alone</p>
      <div class="fig">
        <div class="figchart">
          <div id="chartwrap"><canvas id="chart" role="img" aria-label="Paragraphs per committee">Paragraphs per committee: see the table beside this chart.</canvas></div>
          <p id="nochart" class="empty" hidden>No paragraph matches, so there is nothing to chart.</p>
        </div>
        <table id="ctable"><caption>Paragraphs per committee (same numbers as the chart)</caption><thead><tr><th scope="col">Committee</th><th scope="col">Name</th><th scope="col" class="r">Paragraphs</th></tr></thead><tbody></tbody></table>
      </div>
      <p class="hint" id="ctot"></p>
      <p class="hint">How this is computed: one count per committee over the paragraphs that match the query and filters. Joint General Comments count under both committees, so the bars can add up to more than the hits.</p>
    </section>

    <section id="p1" role="tabpanel" aria-labelledby="t1" hidden>
      <div class="lbl">What exactly does it say?</div>
      <p class="sumline" id="sum" aria-live="polite"></p>
      <div class="orderrow"><span class="hint" id="ordtxt"></span><label class="lbl" for="ord">Order</label>
        <select id="ord"><option value="year">Year, newest first</option><option value="doc">Document order</option><option value="match">Most matches first</option></select></div>
      <p class="hint">This page retrieves; it never writes. Every paragraph shown is a record of the file, as stored.</p>
      <div id="results"></div>
      <p><button class="btn" id="more" hidden>Show 25 more</button></p>
    </section>

    <section id="p2" role="tabpanel" aria-labelledby="t2" hidden>
      <div class="lbl">What have I collected?</div>
      <h2 id="dtitle">Your draft (0 quotations)</h2>
      <div class="btns"><button class="btn pri" id="dcopy">Copy all</button><button class="btn" id="dtxt">Download .txt</button><button class="btn" id="dcsv">Download .csv</button></div>
      <p class="hint" id="dstore"></p>
      <ul class="drl" id="dlist"></ul>
    </section>

    <section id="p3" role="tabpanel" aria-labelledby="t3" hidden>
      <div class="lbl">Can I trust this?</div>
      <h2>Checks on the current search</h2>
      <p class="hint">A failed check marks rows; it never drops them. The checks re-run after every search, filter, page and draft change.</p>
      <ul class="chk" id="checks"></ul>
      <h2 style="margin-top:24px">Known quirks of this file</h2>
      <p class="hint">Computed when the page loaded, before any search.</p>
      <ul class="plain" id="quirks"></ul>
      <h2 style="margin-top:24px">How this is computed</h2>
      <ul class="plain">
        <li>Matching is done by this page's code over each paragraph with footnote marks removed, curly quotes and dashes made plain, whitespace collapsed and letters lower-cased. The query is treated the same way.</li>
        <li>Words match whole words only. A hyphen is a boundary, so “state” finds “non-State”. A star at the end of a word matches any ending. A phrase is its words in order, separated only by spaces.</li>
        <li>NOT binds tightest, then AND (a space also means AND), then OR; brackets override.</li>
        <li>Hits are the paragraphs that match the query and pass the committee, year and document filters. A joint General Comment counts under each of its committees.</li>
        <li>Citation = symbol + pinpoint, built only from the record's fields (“para. N”, “preamble” for paragraph 0, “subpara. (b)” for lettered sub-paragraphs). When one symbol holds several documents, the committee and the document's name come first. Style: UN short form. No symbol, number or link is ever invented.</li>
        <li>The copied quotation is the shown text (footnote marks removed). The “12. ” at the start is dropped only when it equals the record's paragraph number.</li>
        <li>Older General Comments may have been replaced by later ones; the file does not say which, so the year is on every row.</li>
      </ul>
    </section>
  </main>
</div>

<div id="copied" aria-live="polite" hidden></div>
<footer id="foot"></footer>

<script>
(function(){
"use strict";
var D=window.WORKSHOP_DATA||{}, GC=D.gc||{}, R=Array.isArray(GC.records)?GC.records:[];
function $(s){return document.querySelector(s)}
function esc(s){return String(s==null?'':s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;')}
function fmt(n){return Number(n).toLocaleString('en-US')}
function rx(s){return s.replace(/[.*+?^${}()|[\]\\]/g,'\\$&')}
var NAMES={'CAT':'Committee against Torture','CAT-OP':'Subcommittee on Prevention of Torture','CCPR':'Human Rights Committee','CED':'Committee on Enforced Disappearances','CEDAW':'Committee on the Elimination of Discrimination against Women','CERD':'Committee on the Elimination of Racial Discrimination','CESCR':'Committee on Economic, Social and Cultural Rights','CMW':'Committee on Migrant Workers','CRC':'Committee on the Rights of the Child','CRPD':'Committee on the Rights of Persons with Disabilities'};
function cname(c){return NAMES[c]||c}

if(!R.length){
  $('main').innerHTML='<p class="empty">The General Comments file is empty or was not attached, so there is nothing to search. Drag it from “Your files” into the chat.</p>';
  return;
}

/* ---------- load: precompute once ---------- */
var FN=/\[\[fn:\d+\]\]/g;
var CODE=/\b(CAT-OP|CAT|CCPR|CEDAW|CED|CERD|CESCR|CMW|CRC|CRPD)\b/g;
function norm(s){return String(s).replace(FN,'').replace(/[“”„]/g,'"').replace(/[‘’‚]/g,"'").replace(/[–—\u00ad]/g,'-').replace(/\s+/g,' ').toLowerCase()}
function docName(t){var a=t.indexOf(':'),b=t.indexOf(' on '),c=[a,b].filter(function(x){return x>0});return c.length?t.slice(0,Math.min.apply(null,c)).trim():t}
var titleSets=new Map();
R.forEach(function(r){var s=String(r.symbol||'');if(!titleSets.has(s))titleSets.set(s,new Set());titleSets.get(s).add(r.title)});
var uniqTitles=Array.from(new Set(R.map(function(r){return String(r.title||'')}))).sort(function(a,b){return a.localeCompare(b)});
var titleRank=new Map();uniqTitles.forEach(function(t,i){titleRank.set(t,i)});
var pinCount=new Map(),byId=new Map(),byTP=new Map();
var recs=R.map(function(r,i){
  var o=Object.assign({},r);
  var text=typeof r.text==='string'?r.text:'';
  o.text=text;o._i=i;o.title=String(r.title||'');o.symbol=String(r.symbol||'');o.year=+r.year||0;o.paragraph=+r.paragraph||0;
  o._tr=titleRank.get(o.title);
  o.norm=norm(text);o.shown=text.replace(FN,'');o.marks=(text.match(FN)||[]).length;
  var lm=text.match(/^(\d{1,3})\.\s/);o.leading=lm?+lm[1]:null;
  var le=text.match(/^\(([a-z]{1,4})\)/);o.letter=le?le[1]:null;
  o.mismatch=o.leading!==null&&o.leading!==o.paragraph;
  o.pinpoint=o.paragraph===0?'preamble':(o.letter?'subpara. ('+o.letter+')':'para. '+o.paragraph);
  var sym=o.symbol.replace(/CAT\/OP/g,'CAT-OP');
  var codes=Array.from(new Set(sym.match(CODE)||[]));
  o.joint=codes.length>1;
  o.cm=Array.from(new Set((o.committee?[o.committee]:[]).concat(codes)));if(!o.cm.length)o.cm=['?'];
  o.shared=(titleSets.get(o.symbol)||new Set()).size>1;
  o.citation=o.shared?(o.committee+', '+docName(o.title)+' ('+o.symbol+'), '+o.pinpoint):(o.symbol+', '+o.pinpoint);
  o.copyText=(o.leading!==null&&o.leading===o.paragraph?o.shown.replace(/^\d{1,3}\.\s+/,''):o.shown).trim();
  o.words=o.shown.trim().split(/\s+/).length;
  o.pk=o.title+'|'+o.pinpoint;pinCount.set(o.pk,(pinCount.get(o.pk)||0)+1);
  byId.set(o.id,o);
  var k=o.title+'|'+o.paragraph,ex=byTP.get(k);if(!ex||(ex.letter&&!o.letter))byTP.set(k,o);
  return o;
});
recs.forEach(function(o){o.dup=pinCount.get(o.pk)});
var N=recs.length;
var DOCMAP=new Map();recs.forEach(function(r){if(!DOCMAP.has(r.title))DOCMAP.set(r.title,{title:r.title,short:r.short_title||r.title,committee:r.committee||r.cm[0],year:r.year})});
var DOCS=Array.from(DOCMAP.values()).sort(function(a,b){return a.committee.localeCompare(b.committee)||a.year-b.year||a.short.localeCompare(b.short)});
var ALL=Array.from(new Set(recs.reduce(function(a,r){return a.concat(r.cm)},[]))).sort();
var YMIN=Math.min.apply(null,recs.map(function(r){return r.year})),YMAX=Math.max.apply(null,recs.map(function(r){return r.year}));
var NCOMM=new Set(recs.map(function(r){return r.committee})).size;
var PAGE=25,CUT=700;

/* ---------- state ---------- */
var KEY='gc-verbatim-finder-draft-v1',store=null;
try{localStorage.setItem('__t','1');localStorage.removeItem('__t');store=localStorage}catch(e){store=null}
function loadDraft(){try{if(store){var v=JSON.parse(store.getItem(KEY)||'[]');if(Array.isArray(v))return v}}catch(e){}return[]}
function saveDraft(){try{if(store)store.setItem(KEY,JSON.stringify(S.draft))}catch(e){store=null;renderDraft()}}
var S={q:'',parsed:{empty:true,terms:0,echo:'no search words'},hi:null,qHits:recs,base:recs,hits:recs,bcount:new Map(),
  ticked:new Set(ALL),yf:YMIN,yt:YMAX,doc:'',order:'year',shownN:0,tab:0,
  open:new Set(),full:new Set(),stored:new Set(),ctx:new Set(),draft:loadDraft()};

/* ---------- query parser ---------- */
function isQ(c){return c==='"'||c==='“'||c==='”'||c==='„'}
function tokenize(q){
  var T=[],i=0,n=q.length;
  while(i<n){
    var c=q[i];
    if(/\s/.test(c)){i++;continue}
    if(c==='('||c===')'){T.push({t:c});i++;continue}
    if(isQ(c)){var j=i+1;while(j<n&&!isQ(q[j]))j++;if(j>=n)return{error:'Unbalanced quote: the phrase opened with '+c+' has no closing double quote.'};T.push({t:'phrase',v:q.slice(i+1,j)});i=j+1;continue}
    if(c==='-'&&i+1<n&&!/\s/.test(q[i+1])){T.push({t:'NOT'});i++;continue}
    var k=i;while(k<n&&!/\s/.test(q[k])&&q[k]!=='('&&q[k]!==')'&&!isQ(q[k]))k++;
    var w=q.slice(i,k);
    if(w==='AND'||w==='OR'||w==='NOT')T.push({t:w});else T.push({t:'word',v:w});
    i=k;
  }
  return T;
}
var B1='(?<![\\p{L}\\p{N}])',B2='(?![\\p{L}\\p{N}])',GAP='(?:\\s|\\[\\[fn:\\d+\\]\\])+';
function hiWord(w){return Array.from(w).map(function(ch){if(ch==="'")return "['’‘ʼ]";if(ch==='"')return '["“”„]';if(ch==='-')return '[-–—\\u00ad]';return rx(ch)}).join('')}
function mkTerm(kind,words,wild,raw,text){
  var W=wild?'[\\p{L}\\p{N}]*':'';
  return{t:'term',kind:kind,wild:wild,text:text,
    re:new RegExp(B1+words.map(rx).join('\\s+')+W+B2,'u'),
    sre:new RegExp(B1+raw.map(rx).join('\\s+')+W+B2,'iu'),
    hi:B1+words.map(hiWord).join(GAP)+W+B2};
}
function desc(n){
  if(n.t==='term')return n.kind==='phrase'?'the phrase “'+n.text+'”':(n.wild?'a word beginning with '+n.text:'the word '+n.text);
  if(n.t==='not')return 'not '+(n.x.t==='term'?desc(n.x):'('+desc(n.x)+')');
  var wr=function(x){return x.t==='or'&&n.t==='and'?'('+desc(x)+')':desc(x)};
  return wr(n.l)+(n.t==='and'?' and ':' or ')+wr(n.r);
}
function posTerms(n,neg,out){
  if(n.t==='term'){if(!neg)out.push(n)}
  else if(n.t==='not')posTerms(n.x,!neg,out);
  else{posTerms(n.l,neg,out);posTerms(n.r,neg,out)}
}
function parseQuery(q){
  q=q.trim();
  if(!q)return{empty:true,terms:0,echo:'no search words',pos:[]};
  var tk=tokenize(q);if(tk.error)return{error:tk.error};
  var p=0,nterm=0;
  function fail(m){throw new Error(m)}
  function primary(){
    var t=tk[p];
    if(!t)fail('The query ends where a word, a phrase or a bracket was expected.');
    if(t.t==='('){p++;if(tk[p]&&tk[p].t===')')fail('Empty brackets.');var e=orE();if(!tk[p]||tk[p].t!==')')fail('Unbalanced parenthesis: a “(” has no closing “)”.');p++;return e}
    if(t.t==='word'||t.t==='phrase'){p++;nterm++;return term(t)}
    if(t.t===')')fail('Unbalanced parenthesis: a “)” has no opening “(”.');
    fail('“'+t.t+'” needs a word or phrase on both sides.');
  }
  function term(t){
    if(t.t==='phrase'){
      var ws=t.v.trim().split(/\s+/).filter(Boolean);if(!ws.length)fail('Empty phrase: put words between the quotes.');
      return mkTerm('phrase',ws.map(norm),false,ws.map(function(w){return w.toLowerCase()}),ws.join(' '));
    }
    var v=t.v,wild=false;
    if(/\*+$/.test(v)){wild=true;v=v.replace(/\*+$/,'')}
    if(!v)fail('A star must follow some letters, for example child*.');
    return mkTerm('word',[norm(v)],wild,[v.toLowerCase()],v+(wild?'*':''));
  }
  function notE(){if(tk[p]&&tk[p].t==='NOT'){p++;return{t:'not',x:notE()}}return primary()}
  function andE(){
    var l=notE();
    while(tk[p]&&['word','phrase','(','NOT','AND'].indexOf(tk[p].t)>=0){if(tk[p].t==='AND')p++;var r=notE();l={t:'and',l:l,r:r}}
    return l;
  }
  function orE(){var l=andE();while(tk[p]&&tk[p].t==='OR'){p++;var r=andE();l={t:'or',l:l,r:r}}return l}
  try{
    var tree=orE();
    if(p<tk.length)fail(tk[p].t===')'?'Unbalanced parenthesis: a “)” has no opening “(”.':'The query could not be read after “'+tk[p].t+'”.');
    var pos=[];posTerms(tree,false,pos);
    var echo='Paragraphs '+(tree.t==='not'?'not containing '+desc(tree.x):'containing '+desc(tree));
    if(!pos.length)echo+=' (a NOT-only query: every paragraph that lacks these terms)';
    return{tree:tree,terms:nterm,pos:pos,echo:echo,notOnly:!pos.length};
  }catch(e){return{error:e.message}}
}
function ev(n,r,strict){
  switch(n.t){
    case 'term':return strict?n.sre.test(r.shown):n.re.test(r.norm);
    case 'not':return !ev(n.x,r,strict);
    case 'and':return ev(n.l,r,strict)&&ev(n.r,r,strict);
    default:return ev(n.l,r,strict)||ev(n.r,r,strict);
  }
}
function highlight(text){
  if(!S.hi)return esc(text);
  var re=S.hi,out='',last=0,m;re.lastIndex=0;
  while((m=re.exec(text))){if(m[0]===''){re.lastIndex++;continue}out+=esc(text.slice(last,m.index))+'<mark>'+esc(m[0])+'</mark>';last=m.index+m[0].length}
  return out+esc(text.slice(last));
}
function countHi(text){
  if(!S.hi)return 0;
  var re=S.hi,c=0,m;re.lastIndex=0;
  while((m=re.exec(text))){if(m[0]===''){re.lastIndex++;continue}c++}
  return c;
}

/* ---------- run + filter ---------- */
function run(){
  S.parsed=parseQuery(S.q);
  S.hi=null;
  if(S.parsed.pos&&S.parsed.pos.length){
    var src=Array.from(new Set(S.parsed.pos.map(function(t){return t.hi}))).sort(function(a,b){return b.length-a.length});
    try{S.hi=new RegExp(src.join('|'),'giu')}catch(e){S.hi=null}
  }
  if(S.parsed.error)S.qHits=[];
  else if(!S.parsed.tree)S.qHits=recs;
  else S.qHits=recs.filter(function(r){return ev(S.parsed.tree,r,false)});
}
function cmpYear(a,b){return b.year-a.year||a._tr-b._tr||a.paragraph-b.paragraph||a._i-b._i}
function cmpDoc(a,b){return a.year-b.year||a._tr-b._tr||a.paragraph-b.paragraph||a._i-b._i}
function refilter(){
  var dt=S.doc===''?null:DOCS[S.doc].title;
  S.base=S.qHits.filter(function(r){return r.year>=S.yf&&r.year<=S.yt&&(dt===null||r.title===dt)});
  S.bcount=new Map();S.base.forEach(function(r){r.cm.forEach(function(c){S.bcount.set(c,(S.bcount.get(c)||0)+1)})});
  S.hits=S.base.filter(function(r){return r.cm.some(function(c){return S.ticked.has(c)})});
  if(S.order==='doc')S.hits.sort(cmpDoc);
  else if(S.order==='match'){S.hits.forEach(function(r){r._mc=countHi(r.shown)});S.hits.sort(function(a,b){return b._mc-a._mc||cmpYear(a,b)})}
  else S.hits.sort(cmpYear);
  renderAll();
}

/* ---------- rail ---------- */
function buildRail(){
  $('#bt').textContent=fmt(N);
  var cl=$('#clist');
  cl.innerHTML=ALL.map(function(c){return '<label class="cb"><input type="checkbox" value="'+esc(c)+'" checked><span><b class="mono">'+esc(c)+'</b> <span class="cn">'+esc(c==='?'?'unknown':cname(c))+' <span data-n="'+esc(c)+'"></span></span></span></label>'}).join('');
  cl.addEventListener('change',function(e){
    var cb=e.target;if(cb.type!=='checkbox')return;
    if(cb.checked)S.ticked.add(cb.value);else S.ticked.delete(cb.value);
    refilter();
  });
  $('#call').onclick=function(){S.ticked=new Set(ALL);syncBoxes();refilter()};
  $('#cnone').onclick=function(){S.ticked=new Set();syncBoxes();refilter()};
  $('#yf').value=YMIN;$('#yt').value=YMAX;$('#yf').min=$('#yt').min=YMIN;$('#yf').max=$('#yt').max=YMAX;
  $('#yf').onchange=function(){var v=parseInt(this.value,10);S.yf=isNaN(v)?YMIN:v;this.value=S.yf;refilter()};
  $('#yt').onchange=function(){var v=parseInt(this.value,10);S.yt=isNaN(v)?YMAX:v;this.value=S.yt;refilter()};
  var sel=$('#doc'),grp=null,gc=null;
  DOCS.forEach(function(d,i){
    if(d.committee!==gc){gc=d.committee;grp=document.createElement('optgroup');grp.label=gc+' · '+cname(gc);sel.appendChild(grp)}
    var o=document.createElement('option');o.value=i;o.textContent=d.short+' ('+d.year+')';grp.appendChild(o);
  });
  sel.onchange=function(){S.doc=this.value===''?'':+this.value;refilter()};
  $('#fb').onclick=function(){var open=this.getAttribute('aria-expanded')==='true';this.setAttribute('aria-expanded',!open);$('#fp').hidden=open};
  $('#chips').addEventListener('click',function(e){
    var b=e.target.closest('[data-chip]');if(!b)return;
    var k=b.dataset.chip;
    if(k==='c'){S.ticked=new Set(ALL);syncBoxes()}
    if(k==='y'){S.yf=YMIN;S.yt=YMAX;$('#yf').value=YMIN;$('#yt').value=YMAX}
    if(k==='d'){S.doc='';$('#doc').value=''}
    refilter();
  });
  $('#clear').onclick=function(){
    S.q='';$('#q').value='';S.ticked=new Set(ALL);S.yf=YMIN;S.yt=YMAX;S.doc='';
    $('#yf').value=YMIN;$('#yt').value=YMAX;$('#doc').value='';syncBoxes();run();refilter();
  };
}
function syncBoxes(){document.querySelectorAll('#clist input').forEach(function(cb){cb.checked=S.ticked.has(cb.value)})}
function renderRail(){
  $('#bn').textContent=fmt(S.hits.length);
  var ch=[];
  if(S.ticked.size<ALL.length)ch.push(['c','Committees: '+(S.ticked.size?Array.from(S.ticked).sort().join(', '):'none')]);
  if(S.yf!==YMIN||S.yt!==YMAX)ch.push(['y','Years '+S.yf+'–'+S.yt]);
  if(S.doc!=='')ch.push(['d','Document: '+DOCS[S.doc].short]);
  $('#chips').innerHTML=ch.map(function(c){return '<button class="chip" data-chip="'+c[0]+'" aria-label="Remove filter: '+esc(c[1])+'">'+esc(c[1])+' ×</button>'}).join('');
  var er=$('#qerr');
  if(S.parsed.error){er.hidden=false;er.textContent=S.parsed.error;$('#echo').textContent=''}
  else{er.hidden=true;$('#echo').textContent=S.parsed.empty?'':S.parsed.echo}
  document.querySelectorAll('#clist [data-n]').forEach(function(s){s.textContent='('+fmt(S.bcount.get(s.dataset.n)||0)+')'});
}

/* ---------- search box + help ---------- */
var EXAMPLES=['"best interests" AND child','(torture OR ill-treatment) NOT detention','"reasonable accommodation"'];
function buildHelp(){
  $('#qhelp').innerHTML='<p class="lbl">Syntax</p><ul>'+
   '<li>A space or <b>AND</b> joins words.</li><li><b>OR</b> accepts either.</li>'+
   '<li><b>NOT</b> or a leading minus leaves a word out.</li><li>Put an exact phrase in double quotes.</li>'+
   '<li>Parentheses group terms.</li><li>A star at the end of a word means any ending (child* finds children).</li>'+
   '<li>Operators are in capitals; lower-case “or” is a word.</li></ul><p class="lbl">Examples (select = run)</p>'+
   EXAMPLES.map(function(x){return '<button class="ex" type="button" data-q="'+esc(x)+'">'+esc(x)+'</button>'}).join('');
  var h=$('#qhelp'),q=$('#q');
  h.addEventListener('mousedown',function(e){e.preventDefault()});
  h.addEventListener('click',function(e){var b=e.target.closest('.ex');if(!b)return;q.value=b.dataset.q;doSearch();q.focus()});
  h.addEventListener('keydown',function(e){
    var ex=Array.from(h.querySelectorAll('.ex')),i=ex.indexOf(document.activeElement);
    if(e.key==='ArrowDown'){e.preventDefault();ex[Math.min(i+1,ex.length-1)].focus()}
    else if(e.key==='ArrowUp'){e.preventDefault();if(i<=0)q.focus();else ex[i-1].focus()}
    else if(e.key==='Escape'){h.hidden=true;q.focus()}
  });
  q.addEventListener('focus',function(){if(!q.value)h.hidden=false});
  q.addEventListener('input',function(){h.hidden=!!q.value});
  q.addEventListener('keydown',function(e){
    if(e.key==='Enter'){doSearch()}
    else if(e.key==='ArrowDown'){h.hidden=false;var f=h.querySelector('.ex');if(f){e.preventDefault();f.focus()}}
    else if(e.key==='Escape'){h.hidden=true}
  });
  $('#qhelp').parentNode.addEventListener('focusout',function(e){if(!e.relatedTarget||!(h.contains(e.relatedTarget)||e.relatedTarget===q))h.hidden=true});
  $('#go').onclick=doSearch;
}
function doSearch(){S.q=$('#q').value;$('#qhelp').hidden=true;run();refilter()}

/* ---------- rows ---------- */
function notesOf(r){
  var n=[];
  if(r.mismatch)n.push('the text begins ‘'+r.leading+'.’ but the record is para. '+r.paragraph+': check the document');
  if(r.letter)n.push('a lettered sub-paragraph, numbered '+r.paragraph+' by the file: verify the label in the document');
  if(r.dup>1)n.push(r.dup===2?'two records share this pinpoint':r.dup+' records share this pinpoint');
  if(r.joint)n.push('joint General Comment');
  return n;
}
function ctxHTML(r,dir){
  if(!S.ctx.has(r.id+':'+dir))return '';
  var q=byTP.get(r.title+'|'+(r.paragraph+(dir==='next'?1:-1)));
  if(!q)return '<div class="ctx">There is no '+dir+' paragraph in this document.</div>';
  return '<div class="ctx"><div class="mono hint">'+(dir==='next'?'NEXT':'PREVIOUS')+' · <span class="pin">'+esc(q.pinpoint)+'</span> · '+esc(q.symbol)+'</div><div class="txt">'+esc(q.shown)+'</div></div>';
}
function rowHTML(r){
  var open=S.open.has(r.id),st=S.stored.has(r.id),fu=S.full.has(r.id);
  var t=st?r.text:r.shown,long=t.length>CUT,disp=t;
  if(long&&!fu){
    disp=t.slice(0,CUT);
    if(!/\s/.test(t[CUT]||' ')){var k=disp.search(/\s\S*$/);if(k>300)disp=disp.slice(0,k)}
    disp=disp.replace(/\[\[[^\]]*$/,'').replace(/\s+$/,'')+' …';
  }
  var badges=r.cm.map(function(c){return '<span class="badge">'+esc(c)+'</span>'}).join('');
  var sym=r.doc_url?'<a href="'+esc(r.doc_url)+'" target="_blank" rel="noopener">'+esc(r.symbol)+'</a>':esc(r.symbol);
  var more=long?'<button class="lnk" data-act="full">'+(fu?'Show less':'Show the full paragraph ('+fmt(r.words)+' words)')+'</button>':'';
  var fn='';
  if(r.marks>0)fn='<div class="fnl">'+(st?'Showing the text as stored, with '+r.marks+' footnote mark'+(r.marks>1?'s':'')+' · ':r.marks+' footnote mark'+(r.marks>1?'s':'')+' removed · ')+'<button class="lnk" data-act="stored">'+(st?'show as printed':'show as stored')+'</button></div>';
  var notes=notesOf(r).map(function(n){return '<div class="note">Note: '+esc(n)+'.</div>'}).join('');
  var inDraft=S.draft.some(function(d){return d.id===r.id});
  var detail=open?'<div class="detail"><div class="btns"><button class="btn pri" data-act="copycite">Copy citation</button><button class="btn" data-act="copyquote">Copy quotation</button><button class="btn" data-act="add">'+(inDraft?'In your draft ✓':'Add to draft')+'</button></div>'+
    '<p class="hint">Citation style: UN short form · built from the record’s fields: <b>'+esc(r.citation)+'</b></p>'+
    '<p class="hint">Context: <button class="lnk" data-act="prev">previous</button> | <button class="lnk" data-act="next">next</button></p>'+ctxHTML(r,'prev')+ctxHTML(r,'next')+'</div>':'';
  return '<article class="row'+(open?' open':'')+'" data-id="'+esc(r.id)+'"><h3><button class="rt" data-act="toggle" aria-expanded="'+open+'">'+badges+'<span>'+esc(r.short_title||r.title)+'</span></button></h3>'+
    '<div class="meta">'+sym+' · <span class="pin">'+esc(r.pinpoint)+'</span> · '+esc(r.year)+'</div>'+
    '<div class="txt">'+highlight(disp)+'</div>'+more+fn+notes+detail+'</article>';
}
function renderResults(){
  var el=$('#results');
  S.shownN=Math.min(PAGE,S.hits.length);
  if(!S.hits.length){
    el.innerHTML='<p class="empty">'+(S.parsed.error?'The query could not be read: '+esc(S.parsed.error):'No paragraph matches. Check the spelling, try a star for endings (child*), or clear the filters.')+'</p>';
  }else el.innerHTML=S.hits.slice(0,S.shownN).map(rowHTML).join('');
  updateMore();
}
function updateMore(){
  var left=S.hits.length-S.shownN,b=$('#more');
  b.hidden=left<=0;b.textContent='Show '+Math.min(PAGE,left)+' more ('+fmt(left)+' left)';
}
function redraw(id,act){
  var old=$('#results').querySelector('article[data-id="'+CSS.escape(id)+'"]');if(!old)return;
  var t=document.createElement('div');t.innerHTML=rowHTML(byId.get(id));
  var nw=t.firstElementChild;old.replaceWith(nw);
  if(act){var b=nw.querySelector('[data-act="'+act+'"]');if(b)b.focus({preventScroll:true})}
}
function bindResults(){
  $('#more').onclick=function(){
    var from=S.shownN;S.shownN=Math.min(S.shownN+PAGE,S.hits.length);
    $('#results').insertAdjacentHTML('beforeend',S.hits.slice(from,S.shownN).map(rowHTML).join(''));
    updateMore();renderChecks();
  };
  $('#results').addEventListener('click',function(e){
    var art=e.target.closest('article');if(!art)return;
    var id=art.dataset.id,r=byId.get(id),b=e.target.closest('[data-act]'),act=b&&b.dataset.act;
    if(!b){
      if(e.target.closest('a,.detail,mark')&&e.target.closest('a,.detail'))return;
      if(String(window.getSelection&&window.getSelection()))return;
      act='toggle';
    }
    if(act==='toggle'){if(S.open.has(id))S.open.delete(id);else S.open.add(id);redraw(id,'toggle')}
    else if(act==='stored'){if(S.stored.has(id))S.stored.delete(id);else S.stored.add(id);redraw(id,'stored')}
    else if(act==='full'){if(S.full.has(id))S.full.delete(id);else S.full.add(id);redraw(id,'full')}
    else if(act==='copycite')copyText(r.citation,'Citation');
    else if(act==='copyquote')copyText('“'+r.copyText+'” '+r.citation,'Quotation');
    else if(act==='add'){addDraft(r);redraw(id,'add')}
    else if(act==='prev'||act==='next'){var k=id+':'+act;if(S.ctx.has(k))S.ctx.delete(k);else S.ctx.add(k);redraw(id,act)}
  });
}

/* ---------- summary, overview ---------- */
var ORD={year:'sorted by year, newest first, then by document and paragraph',doc:'sorted by year, oldest first, then by document and paragraph',match:'sorted by number of matches in the paragraph, then by year, newest first'};
function renderSummary(){
  var H=S.hits,cms=new Set(),y0=1e9,y1=-1e9;
  H.forEach(function(r){r.cm.forEach(function(c){cms.add(c)});if(r.year<y0)y0=r.year;if(r.year>y1)y1=r.year});
  var s=fmt(H.length)+' of '+fmt(N)+' paragraphs match'+(S.parsed.empty?' · no search words':'');
  if(H.length)s+=' · '+cms.size+' committee'+(cms.size===1?'':'s')+' · '+y0+'–'+y1;
  $('#sum').textContent=s;
  $('#ordtxt').textContent=ORD[S.order]+(S.order==='match'&&!S.hi?' (no search words, so all equal)':'');
}
function chartData(){
  var m=new Map();S.hits.forEach(function(r){r.cm.forEach(function(c){m.set(c,(m.get(c)||0)+1)})});
  return Array.from(m).sort(function(a,b){return b[1]-a[1]||a[0].localeCompare(b[0])});
}
var chart=null;
var valueLabels={id:'valueLabels',afterDatasetsDraw:function(c){
  var ctx=c.ctx;ctx.save();ctx.font='13px ui-monospace,Menlo,Consolas,monospace';ctx.fillStyle='#1d1b18';ctx.textBaseline='middle';
  c.getDatasetMeta(0).data.forEach(function(b,i){ctx.fillText(fmt(c.data.datasets[0].data[i]),b.x+6,b.y)});ctx.restore()}};
function renderOverview(){
  var cd=chartData(),sum=cd.reduce(function(a,d){return a+d[1]},0),extra=S.hits.reduce(function(a,r){return a+r.cm.length-1},0);
  $('#ctable tbody').innerHTML=cd.map(function(d){return '<tr><td><b class="mono">'+esc(d[0])+'</b></td><td>'+esc(d[0]==='?'?'unknown':cname(d[0]))+'</td><td class="r">'+fmt(d[1])+'</td></tr>'}).join('')||'<tr><td colspan="3">No paragraph matches.</td></tr>';
  $('#ctot').textContent='Bars add up to '+fmt(sum)+' = '+fmt(S.hits.length)+' hits + '+fmt(extra)+' extra counts for joint General Comments.';
  $('#chart').setAttribute('aria-label','Paragraphs per committee: '+(cd.map(function(d){return d[0]+' '+fmt(d[1])}).join('; ')||'none'));
  S.cd=cd;
  if(S.tab===0)renderChart();
}
function renderChart(){
  if(chart){chart.destroy();chart=null}
  var cd=S.cd||[];
  $('#chartwrap').hidden=!cd.length||!window.Chart;$('#nochart').hidden=!!cd.length;
  if(!cd.length||!window.Chart)return;
  $('#chartwrap').style.height=Math.max(170,cd.length*42+60)+'px';
  chart=new Chart($('#chart'),{type:'bar',
    data:{labels:cd.map(function(d){return d[0]}),datasets:[{data:cd.map(function(d){return d[1]}),backgroundColor:'#9b2335',barPercentage:.8,categoryPercentage:.85}]},
    options:{indexAxis:'y',responsive:true,maintainAspectRatio:false,animation:false,layout:{padding:{right:60}},
      plugins:{legend:{display:false}},
      scales:{x:{beginAtZero:true,ticks:{maxTicksLimit:6},grid:{color:'#e8e2d4'}},y:{grid:{display:false},ticks:{font:{family:'ui-monospace,Menlo,Consolas,monospace',size:12}}}},
      onClick:function(e,els){if(els.length){S.ticked=new Set([cd[els[0].index][0]]);syncBoxes();refilter()}},
      onHover:function(e,els){if(e.native&&e.native.target)e.native.target.style.cursor=els.length?'pointer':'default'}},
    plugins:[valueLabels]});
}

/* ---------- copy, draft ---------- */
function say(html){var b=$('#copied');b.hidden=false;b.innerHTML=html+' <button class="lnk" id="chide">Hide</button>';$('#chide').onclick=function(){b.hidden=true}}
function copyText(s,label){
  function ok(){say('<div class="hint">'+esc(label)+' copied. Exactly this text was sent:</div><pre>'+esc(s)+'</pre>')}
  function fb(){
    say('<div>The browser did not allow copying. Select the text and copy it (Ctrl+C or ⌘C).</div><textarea id="cta" readonly></textarea> <button class="btn" id="csel">Select and copy</button>');
    var ta=$('#cta');ta.value=s;ta.focus();ta.select();
    $('#csel').onclick=function(){ta.focus();ta.select();try{document.execCommand('copy')}catch(e){}};
  }
  try{if(navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText(s).then(ok,fb);return}}catch(e){}
  fb();
}
function addDraft(r){
  if(S.draft.some(function(d){return d.id===r.id})){say('<div class="hint">Already in your draft: '+esc(r.citation)+'</div>');return}
  S.draft.push({id:r.id,citation:r.citation,quotation:'“'+r.copyText+'”',symbol:r.symbol,paragraph:r.paragraph,pinpoint:r.pinpoint,committee:r.committee,short_title:r.short_title||r.title,year:r.year,text_copied:r.copyText,text_as_stored:r.text,doc_url:r.doc_url||''});
  saveDraft();renderDraft();renderChecks();
  say('<div class="hint">Added to your draft: '+esc(r.citation)+'</div>');
}
function draftBad(){return S.draft.filter(function(it){var r=byId.get(it.id);return !r||r.text!==it.text_as_stored})}
function renderDraft(){
  var n=S.draft.length,bad=new Set(draftBad().map(function(i){return i.id}));
  $('#t2').firstChild.textContent='03 Draft ('+n+')';
  $('#dtitle').textContent='Your draft ('+n+' quotation'+(n===1?'':'s')+')';
  $('#dstore').textContent=(store?'Kept in this browser (localStorage), so it stays after a reload.':'localStorage is not available here: the draft is kept in memory and is lost when the page closes or reloads.')+' If downloads are blocked, use Copy all.';
  ['dcopy','dtxt','dcsv'].forEach(function(i){$('#'+i).disabled=!n});
  $('#dlist').innerHTML=n?S.draft.map(function(it,i){
    return '<li class="dr"><blockquote>'+esc(it.quotation)+'</blockquote><p><span class="pin">'+esc(it.citation)+'</span> · '+(it.doc_url?'<a href="'+esc(it.doc_url)+'" target="_blank" rel="noopener">open document</a> · ':'')+esc(it.short_title)+', '+esc(it.year)+
    ' · <button class="lnk" data-rm="'+i+'">Remove</button></p>'+(bad.has(it.id)?'<p class="note">Note: the stored text of this record differs from the text saved here: check it against the document.</p>':'')+'</li>';
  }).join(''):'<li class="empty">Nothing collected yet. Open a paragraph on tab 02 and press “Add to draft”.</li>';
}
function draftTxt(){return S.draft.map(function(it){return it.quotation+'\n'+it.citation}).join('\n\n')}
function draftCsv(){
  var cols=['citation','symbol','paragraph','pinpoint','committee','short_title','year','text_copied','text_as_stored','doc_url'];
  var q=function(v){return '"'+String(v==null?'':v).replace(/"/g,'""')+'"'};
  return '\uFEFF'+[cols.map(q).join(',')].concat(S.draft.map(function(it){return cols.map(function(c){return q(it[c])}).join(',')})).join('\r\n');
}
function download(name,mime,content){
  var u=URL.createObjectURL(new Blob([content],{type:mime})),a=document.createElement('a');
  a.href=u;a.download=name;document.body.appendChild(a);a.click();a.remove();setTimeout(function(){URL.revokeObjectURL(u)},2000);
}
function bindDraft(){
  $('#dcopy').onclick=function(){copyText(draftTxt(),'Draft ('+S.draft.length+' quotations)')};
  $('#dtxt').onclick=function(){download('draft-quotations.txt','text/plain;charset=utf-8',draftTxt())};
  $('#dcsv').onclick=function(){download('draft-quotations.csv','text/csv;charset=utf-8',draftCsv())};
  $('#dlist').addEventListener('click',function(e){
    var b=e.target.closest('[data-rm]');if(!b)return;
    S.draft.splice(+b.dataset.rm,1);saveDraft();renderDraft();renderChecks();
    if(S.open.size)document.querySelectorAll('#results .row.open').forEach(function(a){redraw(a.dataset.id)});
  });
}

/* ---------- checks ---------- */
function plist(a,n){n=n||6;return a.slice(0,n).map(function(r){return r.citation}).join('; ')+(a.length>n?' … and '+(a.length-n)+' more':'')}
function computeChecks(){
  var C=[],H=S.hits,P=S.parsed;
  if(P.error)C.push({n:'Query understood',ok:false,d:P.error});
  else C.push({n:'Query understood',ok:true,d:P.empty?'No search words: every paragraph that passes the filters is listed.':P.echo+' · '+P.terms+' term'+(P.terms===1?'':'s')+'.'});
  var listed=document.querySelectorAll('#results article').length,sumB=0;S.bcount.forEach(function(v){sumB+=v});
  var exB=S.base.reduce(function(a,r){return a+r.cm.length-1},0);
  C.push({n:'Totals',ok:listed===Math.min(S.shownN,H.length)&&sumB===S.base.length+exB,d:listed+' rows listed + '+(H.length-listed)+' behind “Show more” = '+H.length+' hits. Committee counts add up to '+sumB+' = '+S.base.length+' paragraphs before the committee filter + '+exB+' joint.'});
  var cs=(S.cd||[]).reduce(function(a,d){return a+d[1]},0),ex=H.reduce(function(a,r){return a+r.cm.length-1},0);
  C.push({n:'Chart total',ok:cs===H.length+ex,d:'Bars add up to '+cs+'; hits '+H.length+' + joint extras '+ex+' = '+(H.length+ex)+'.'});
  var noHl=[];
  if(S.hi)H.forEach(function(r){if(countHi(r.shown)===0)noHl.push(r)});
  C.push({n:'Highlight',ok:!noHl.length,d:!S.hi?(P.empty?'No search words: nothing to highlight.':P.notOnly?'NOT-only query: nothing to highlight.':'Nothing to highlight.'):(noHl.length?'Matched, not highlighted ('+noHl.length+'; still shown): '+plist(noHl):'All '+H.length+' hits show at least one highlighted word.')});
  var nd='No straight quote, apostrophe or hyphen in the query, so no normalisation was needed.';
  if(P.tree&&/['"\-]/.test(S.q)){
    var only=H.filter(function(r){return !ev(P.tree,r,true)}).length;
    nd='The query has straight quotes, apostrophes or hyphens; curly quotes and dash forms were matched too. '+only+' hit'+(only===1?' contains':'s contain')+' only those other forms (not a letter-for-letter match).';
  }
  C.push({n:'Normalisation',ok:true,d:nd});
  var mm=H.filter(function(r){return r.mismatch}),dp=H.filter(function(r){return r.dup>1}),lt=H.filter(function(r){return r.letter});
  C.push({n:'Numbering',ok:!mm.length&&!dp.length,d:(mm.length?mm.length+' with a leading number that differs from the paragraph: '+mm.slice(0,5).map(function(r){return r.citation+' (text says '+r.leading+')'}).join('; ')+(mm.length>5?' …':'')+'. ':'No leading-number mismatches. ')+(dp.length?dp.length+' share a pinpoint with another record: '+plist(dp,5)+'. ':'No shared pinpoints. ')+(lt.length?lt.length+' lettered sub-paragraph'+(lt.length>1?'s':'')+' (verify the label): '+plist(lt,4)+'.':'No lettered sub-paragraphs.')});
  var bm=[];
  H.forEach(function(r){
    var c=(r.text.match(/\[\[fn:/g)||[]).length,parts=r.text.split(FN),ms=r.text.match(FN)||[],b=parts[0];
    ms.forEach(function(m,i){b+=m+parts[i+1]});
    if(c!==r.marks||ms.length!==r.marks||b!==r.text)bm.push(r);
  });
  C.push({n:'Footnote marks',ok:!bm.length,d:bm.length?'Mismatch in: '+plist(bm):'For all '+H.length+' hits the marks removed equal the marks stored, and putting them back gives the stored text exactly.'});
  var bd=draftBad();
  C.push({n:'Draft',ok:!bd.length,d:S.draft.length?(bd.length?bd.length+' item(s) differ from the stored record: '+bd.map(function(i){return i.citation}).join('; '):'All '+S.draft.length+' item(s) match the stored text of their records.'):'No items in the draft yet.'});
  return C;
}
function renderChecks(){
  var C=computeChecks(),bad=C.filter(function(c){return !c.ok}).length;
  $('#checks').innerHTML=C.map(function(c){return '<li><span class="'+(c.ok?'ok':'fail')+'">'+(c.ok?'pass':'check failed')+'</span><b>'+esc(c.n)+'.</b> '+esc(c.d)+'</li>'}).join('');
  $('#status').innerHTML='<span class="dot'+(bad?' bad':'')+'"></span><span>'+(bad?bad+' check'+(bad>1?'s':'')+' failed':(C.length-bad)+' checks pass')+'</span>';
  $('#t3dot').hidden=!bad;$('#t3dot').className='dot bad';
}
function quirks(){
  var L=[],eg=function(r){return r?' e.g. '+r.citation+' ('+(r.short_title||r.title)+')':''};
  var p0=recs.filter(function(r){return r.paragraph===0});
  L.push('<b>'+fmt(p0.length)+'</b> records have paragraph 0: preambles, cited as “preamble”, never “para. 0”.'+eg(p0[0]));
  var sh=Array.from(titleSets).filter(function(e){return e[1].size>1}).sort(function(a,b){return b[1].size-a[1].size});
  L.push('<b>'+sh.length+'</b> symbols are shared by several documents'+(sh.length?' (the largest, '+esc(sh[0][0])+', holds '+sh[0][1].size+')':'')+': their citations carry the committee and the document’s name.');
  var jt=recs.filter(function(r){return r.joint});
  L.push('<b>'+new Set(jt.map(function(r){return r.title})).size+'</b> joint General Comments ('+fmt(jt.length)+' records) carry two symbols in one field and count under both committees.'+eg(jt[0]));
  var dk=new Set();recs.forEach(function(r){if(r.dup>1)dk.add(r.pk)});
  var dr=recs.filter(function(r){return r.dup>1});
  L.push('<b>'+dk.size+'</b> pinpoints occur more than once within one document.'+eg(dr[0]));
  var mm=recs.filter(function(r){return r.mismatch});
  L.push('<b>'+mm.length+'</b> records start with a number that differs from their paragraph number; they are never corrected.'+(mm[0]?' e.g. text begins ‘'+mm[0].leading+'.’, record is para. '+mm[0].paragraph+' of '+esc(mm[0].symbol):''));
  var lt=recs.filter(function(r){return r.letter});
  L.push('<b>'+lt.length+'</b> records are lettered sub-paragraphs that the file numbers 1, 2, 3…; cited as “subpara. (b)”.'+eg(lt[0]));
  var fm=recs.filter(function(r){return r.marks>0});
  L.push('<b>'+fmt(fm.length)+'</b> paragraphs carry footnote marks ('+fmt(recs.reduce(function(a,r){return a+r.marks},0))+' in all), removed on screen and in copies.');
  $('#quirks').innerHTML=L.map(function(l){return '<li>'+l.replace(/e\.g\. ([^(]+)\(/,function(m,a){return 'e.g. '+esc(a)+'('}).replace(/\(([^)]*)\)\.?$/,function(m){return m})+'</li>'}).join('');
}

/* ---------- tabs ---------- */
var tabs=[0,1,2,3].map(function(i){return $('#t'+i)}),panels=[0,1,2,3].map(function(i){return $('#p'+i)});
function setTab(i,focus){
  S.tab=i;
  tabs.forEach(function(b,k){b.setAttribute('aria-selected',k===i);b.tabIndex=k===i?0:-1;panels[k].hidden=k!==i});
  $('#layout').classList.toggle('nr',i===2);$('#rail').hidden=i===2;
  if(i===0)renderChart();
  if(focus)tabs[i].focus();
}
tabs.forEach(function(b,i){
  b.onclick=function(){setTab(i)};
  b.addEventListener('keydown',function(e){
    var k=e.key,j=null;
    if(k==='ArrowRight')j=(i+1)%4;else if(k==='ArrowLeft')j=(i+3)%4;else if(k==='Home')j=0;else if(k==='End')j=3;
    if(j!==null){e.preventDefault();setTab(j,true)}
  });
});

function renderAll(){renderRail();renderSummary();renderResults();renderOverview();renderDraft();renderChecks()}

/* ---------- start ---------- */
(function(){
  var src=GC.source||'',url=GC.source_url||(/^https?:\/\//.test(src)?src:'');
  var link=url?'<a href="'+esc(url)+'" target="_blank" rel="noopener">'+esc(src||url)+'</a>':esc(src||'UN treaty bodies');
  $('#sub').innerHTML=fmt(N)+' paragraphs from '+fmt(DOCS.length)+' General Comments of '+NCOMM+' committees, '+YMIN+'–'+YMAX+'. Source: '+link+'.';
  $('#foot').textContent='Source: '+(src||'General Comments file')+(GC.built?' · built '+GC.built:'')+'. Counting, matching and sorting are done by this page’s code; no model is called. Credits: charts drawn with Chart.js (MIT licence).';
  buildRail();buildHelp();bindResults();bindDraft();quirks();
  setTab(0);
  run();refilter();
  $('#q').focus();
})();
})();
</script>
</body>
</html>
```