I built the Verbatim finder on your General Comments file, in four tabs: overview chart, paragraphs, draft and check & method. Search takes AND, OR, NOT, "exact phrases", parentheses and word* endings, and every citation and quotation is built only from the record's own fields. Nothing is generated and nothing leaves the browser.

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Verbatim finder: General Comments</title>
<style>
:root{--bg:#f4f0e8;--ink:#1d1b18;--rule:#d9d2c3;--red:#9b2335;--grey:#5a554c;--green:#1f6b3a;--mono:ui-monospace,Menlo,Consolas,monospace;--serif:Georgia,"Times New Roman",serif}
*{box-sizing:border-box}
[hidden]{display:none!important}
body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.5 system-ui,-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;padding-bottom:64px}
a{color:var(--red)}
:focus-visible{outline:3px solid var(--red);outline-offset:2px}
.mono{font-family:var(--mono);font-size:12px;letter-spacing:.06em;text-transform:uppercase}
.mono2{font-family:var(--mono);font-size:12px;letter-spacing:.03em}
.wrap{max-width:1280px;margin:0 auto;padding:0 20px}
.top{padding-top:18px}
.top .lab{color:var(--grey)}
.hrow{display:flex;justify-content:space-between;align-items:flex-start;gap:16px;flex-wrap:wrap}
h1{font:400 30px/1.15 var(--serif);margin:4px 0 6px}
.sub{margin:0 0 12px;color:var(--grey);font-size:15px}
.status{white-space:nowrap;padding-top:8px}
.dot{display:inline-block;width:10px;height:10px;border-radius:50%;margin-right:6px;background:var(--green)}
.dot.bad{background:var(--red)}
.ok{color:var(--green)}
.bad{color:var(--red)}
.sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)}
[role=tablist]{display:flex;gap:4px;border-bottom:1px solid var(--rule);flex-wrap:wrap}
[role=tab]{font:12px var(--mono);letter-spacing:.08em;text-transform:uppercase;background:none;border:0;border-bottom:3px solid transparent;padding:12px 14px;color:var(--grey);cursor:pointer}
[role=tab][aria-selected=true]{color:var(--red);border-bottom-color:var(--red);font-weight:700}
.shell{display:grid;grid-template-columns:300px minmax(0,1fr);gap:36px;padding-top:20px;align-items:start}
.shell.norail{grid-template-columns:minmax(0,1fr)}
.rail{position:sticky;top:8px;max-height:calc(100vh - 76px);overflow:auto;border-right:1px solid var(--rule);padding:0 20px 12px 0}
.railhead{display:flex;justify-content:space-between;align-items:baseline}
.bignum .n{font:400 52px/1 var(--serif)}
.bignum .t{font:400 20px var(--serif)}
.of{color:var(--grey);font-size:14px;margin-bottom:8px}
.chips{display:flex;flex-wrap:wrap;gap:6px;margin:6px 0 12px}
.chip{font:12px var(--mono);background:none;border:1px solid var(--red);color:var(--red);padding:2px 8px;cursor:pointer;border-radius:12px}
.lbl{display:block;color:var(--grey);margin:12px 0 4px}
input[type=text],input[type=number],select{font:16px system-ui,sans-serif;padding:8px;border:1px solid var(--ink);background:#fffdf8;color:var(--ink);width:100%}
.searchrow{display:flex;gap:8px;margin-top:8px}
.searchwrap{position:relative}
.help{position:absolute;left:0;right:0;top:100%;background:#fffdf8;border:1px solid var(--ink);padding:10px 12px;z-index:5;font-size:14px;box-shadow:none}
.help ul{margin:0 0 8px;padding-left:18px}
.help li{margin:2px 0}
.help [role=listbox]{list-style:none;padding:0;margin:6px 0 0}
.help [role=option]{display:block;width:100%;text-align:left;font:13px var(--mono);background:none;border:1px solid var(--rule);padding:6px 8px;margin:4px 0;cursor:pointer;color:var(--ink)}
.help [role=option]:hover{border-color:var(--red)}
.btn{font:13px var(--mono);letter-spacing:.04em;background:var(--ink);color:var(--bg);border:1px solid var(--ink);padding:8px 14px;cursor:pointer}
.btn.ghost{background:transparent;color:var(--ink)}
.lnk{background:none;border:0;padding:0;color:var(--red);text-decoration:underline;cursor:pointer;font:inherit}
.note{font-size:14px;color:var(--grey);margin:8px 0}
.echo{font-size:14px;margin:8px 0}
.err{color:var(--red);font-weight:600}
.fh{margin:16px 0 0;border-top:1px solid var(--rule);font:inherit}
.fh button{width:100%;display:flex;gap:10px;text-align:left;background:none;border:0;padding:10px 0;font:13px var(--mono);letter-spacing:.06em;text-transform:uppercase;cursor:pointer;color:var(--ink)}
.fh .num{color:var(--red);font-weight:700}
.fbody{padding-bottom:8px}
.cb{display:flex;gap:8px;align-items:baseline;padding:3px 0;font-size:14px}
.cb input{flex:none;accent-color:var(--red)}
.cb .cname{flex:1;color:var(--grey);font-size:13px}
.cc{color:var(--red);font-weight:700}
.yrs{display:flex;gap:10px}
.yrs label{flex:1}
.badge{font:11px var(--mono);letter-spacing:.06em;border:1px solid var(--ink);padding:1px 6px;text-transform:uppercase;white-space:nowrap}
h2.h2,h3.fig,h2.fig{font:400 24px/1.2 var(--serif);margin:0 0 10px}
h3.fig{font-size:20px;margin-top:28px}
.fig .mono{color:var(--red);margin-right:8px}
.hint{color:var(--grey);margin:6px 0}
.how{font-size:14px;color:var(--grey);margin:10px 0}
.figrow{display:grid;grid-template-columns:minmax(0,1.3fr) minmax(0,1fr);gap:28px;align-items:start}
.chartbox{position:relative;min-height:140px}
table{border-collapse:collapse;width:100%}
caption{text-align:left;font:12px var(--mono);letter-spacing:.06em;text-transform:uppercase;color:var(--grey);padding-bottom:6px}
th,td{border-bottom:1px solid var(--rule);padding:6px 8px;text-align:left;font-size:15px}
th{font:12px var(--mono);letter-spacing:.06em;text-transform:uppercase;color:var(--grey)}
.num{text-align:right;font-variant-numeric:tabular-nums}
.sumline{font:400 20px/1.3 var(--serif);margin:0 0 4px}
.orderrow{display:flex;gap:10px;align-items:center;flex-wrap:wrap;margin:4px 0 8px}
.orderrow select{width:auto}
.row{border-top:1px solid var(--rule);padding:14px 0;cursor:pointer}
.row.open{background:#ece5d6;cursor:auto;padding:14px 12px;margin:0 -12px}
.rh{margin:0;font:600 16px/1.35 system-ui,sans-serif}
.rowbtn{display:flex;flex-wrap:wrap;gap:8px;align-items:baseline;background:none;border:0;padding:0;font:inherit;color:inherit;text-align:left;cursor:pointer}
.meta{margin:4px 0 0;color:var(--grey)}
.pin{color:var(--red);font-weight:700}
.txt{margin:8px 0 4px;white-space:pre-wrap;max-width:80ch}
mark{background:#fff2a8;color:#1d1b18;font-weight:700;padding:0 1px}
.sub2{font-size:14px;color:var(--grey);margin:2px 0}
.amber{margin:6px 0 0;background:#f8e7c0;color:#5c3a00;border-left:4px solid #b97a00;padding:4px 10px;font-size:14px}
.ctx{color:var(--grey);border-left:3px solid var(--rule);padding-left:10px;margin:8px 0;white-space:pre-wrap;font-size:15px;max-width:80ch}
.ctx .lab{display:block}
.actions{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin-top:10px}
.copied{font-size:14px;margin:6px 0 0}
.sent{display:block;white-space:pre-wrap;max-height:9em;overflow:auto;border:1px solid var(--rule);background:#fffdf8;padding:6px 8px;margin-top:4px;font-size:14px}
textarea.fb{width:100%;height:6em;font:14px var(--mono);margin:6px 0}
.checks,.quirks{list-style:none;margin:0;padding:0}
.checks li,.quirks li{display:flex;gap:14px;border-top:1px solid var(--rule);padding:8px 0;font-size:15px}
.st{flex:none;width:96px;font:700 12px var(--mono);letter-spacing:.06em;text-transform:uppercase}
.quirks .qn{flex:none;width:64px;font:400 22px var(--serif);text-align:right}
ol.how2{padding-left:20px;max-width:90ch}
ol.how2 li{margin:6px 0}
.dli{border-top:1px solid var(--rule);padding:12px 0}
.dli .q{margin:0 0 4px;white-space:pre-wrap;max-width:80ch}
.bar{display:flex;flex-wrap:wrap;gap:8px;margin:10px 0}
.empty{color:var(--grey);padding:20px 0}
footer{position:fixed;left:0;right:0;bottom:0;background:var(--bg);border-top:1px solid var(--rule);padding:8px 20px;font:11px/1.4 var(--mono);letter-spacing:.04em;color:var(--grey)}
@media(max-width:860px){.shell{grid-template-columns:1fr}.rail{position:static;max-height:none;border-right:0;border-bottom:1px solid var(--rule);padding:0 0 16px}.figrow{grid-template-columns:1fr}h1{font-size:24px}}
</style>
</head>
<body>
<div class="wrap">
<header class="top">
  <div class="mono lab">UN TREATY BODIES · GENERAL COMMENTS</div>
  <div class="hrow">
    <h1>Verbatim finder: General Comments and General Recommendations</h1>
    <div id="status" class="status mono" aria-live="polite"></div>
  </div>
  <p id="sub" class="sub"></p>
</header>
<div role="tablist" id="tabs" aria-label="Views">
  <button role="tab" id="t0" aria-controls="p0" aria-selected="true"><span class="tl">01 OVERVIEW</span></button>
  <button role="tab" id="t1" aria-controls="p1" aria-selected="false" tabindex="-1"><span class="tl">02 PARAGRAPHS</span></button>
  <button role="tab" id="t2" aria-controls="p2" aria-selected="false" tabindex="-1"><span class="tl">03 DRAFT (0)</span></button>
  <button role="tab" id="t3" aria-controls="p3" aria-selected="false" tabindex="-1"><span class="tl">04 CHECK &amp; METHOD</span> <span class="dot bad" id="tdot" hidden></span><span class="sr" id="tsr" hidden>(a check failed)</span></button>
</div>
<div class="shell" id="shell">
  <aside class="rail" id="rail" aria-label="Filters">
    <div class="railhead"><span class="mono">FILTERS</span><button class="lnk mono2" id="clear" hidden>Clear all</button></div>
    <div id="big" class="bignum" aria-live="polite"><span class="n" id="bign">0</span> <span class="t">matching paragraphs</span></div>
    <div class="of" id="bigof"></div>
    <div class="chips" id="chips"></div>
    <form id="sf" autocomplete="off">
      <label class="lbl mono" for="q">Search the paragraphs</label>
      <div class="searchwrap" id="sw">
        <input type="text" id="q" spellcheck="false" aria-describedby="qnote">
        <div class="help" id="help" role="group" aria-label="Search syntax" hidden>
          <ul>
            <li>a space or <b>AND</b> joins words</li>
            <li><b>OR</b> accepts either word</li>
            <li><b>NOT</b> or a leading minus leaves a word out</li>
            <li>"an exact phrase" goes in double quotes</li>
            <li>parentheses group: (a OR b) c</li>
            <li>a star ends a word: child* finds children</li>
            <li>operators in capitals; lower-case "or" is a word</li>
          </ul>
          <div class="mono2">Examples (arrow keys, Enter)</div>
          <ul role="listbox" aria-label="Examples">
            <li role="presentation"><button type="button" role="option" data-ex='"best interests" AND child'>"best interests" AND child</button></li>
            <li role="presentation"><button type="button" role="option" data-ex="(torture OR ill-treatment) NOT detention">(torture OR ill-treatment) NOT detention</button></li>
            <li role="presentation"><button type="button" role="option" data-ex='"reasonable accommodation"'>"reasonable accommodation"</button></li>
          </ul>
        </div>
      </div>
      <div class="searchrow"><button class="btn" type="submit">Search</button></div>
    </form>
    <p class="note" id="qnote">Whole words, any case. Curly and straight quotes, apostrophes, dashes and hyphens count as the same, and footnote marks are skipped, so State's finds State’s and a phrase can cross a footnote.</p>
    <p class="echo" id="echo" aria-live="polite"></p>
    <h2 class="fh"><button type="button" id="fbtn" aria-expanded="false" aria-controls="fbody"><span class="num">01</span> Committee, years, document</button></h2>
    <div class="fbody" id="fbody" hidden>
      <div class="mono2" style="margin:6px 0">Committee <button type="button" class="lnk" id="call">all</button> / <button type="button" class="lnk" id="cnone">none</button></div>
      <div id="cmlist"></div>
      <div class="yrs">
        <label class="mono lbl">From<input type="number" id="y0"></label>
        <label class="mono lbl">To<input type="number" id="y1"></label>
      </div>
      <p class="err mono2" id="yerr" hidden>From is after To: nothing can match.</p>
      <label class="mono lbl" for="doc">Document</label>
      <select id="doc"><option value="">All documents</option></select>
    </div>
  </aside>
  <main id="main">
    <section role="tabpanel" id="p0" aria-labelledby="t0">
      <h2 class="fig"><span class="mono">FIG.01</span>Paragraphs per committee</h2>
      <div id="fig1"></div>
      <p class="hint mono">click a bar = tick that committee alone</p>
      <p class="how"><b class="mono">How this is computed</b> One count per committee over the paragraphs that match the query and filters.</p>
      <p class="how">Joint General Comments count under both committees, so the bars can add up to more than the hits.</p>
    </section>
    <section role="tabpanel" id="p1" aria-labelledby="t1" hidden>
      <p class="sumline" id="psum" aria-live="polite"></p>
      <div class="orderrow"><span class="hint mono2" id="pord"></span>
        <label class="mono" for="ord">Order</label>
        <select id="ord"><option value="year">Newest year first</option><option value="doc">Document order</option><option value="matches">Most matches first</option></select>
      </div>
      <p class="hint mono">This page retrieves; it never writes. Every paragraph shown is a record of the file, as stored.</p>
      <div id="rows"></div>
      <div id="more"></div>
    </section>
    <section role="tabpanel" id="p2" aria-labelledby="t2" hidden><div id="draft"></div></section>
    <section role="tabpanel" id="p3" aria-labelledby="t3" hidden><div id="chk"></div></section>
  </main>
</div>
</div>
<footer id="foot"></footer>
<script>
(function(){
'use strict';
var WD=window.WORKSHOP_DATA||{},GC=WD.gc||{},R=Array.isArray(GC.records)?GC.records:[];
var $=function(s,e){return (e||document).querySelector(s);};
var esc=function(s){return String(s==null?'':s).replace(/[&<>"']/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c];});};
var fmt=function(n){return Number(n).toLocaleString('en-GB');};
var NAMES={CAT:'Committee against Torture','CAT-OP':'Subcommittee on Prevention of Torture',CCPR:'Human Rights Committee',CED:'Committee on Enforced Disappearances',CEDAW:'Committee on the Elimination of Discrimination against Women',CERD:'Committee on the Elimination of Racial Discrimination',CESCR:'Committee on Economic, Social and Cultural Rights',CMW:'Committee on Migrant Workers',CRC:'Committee on the Rights of the Child',CRPD:'Committee on the Rights of Persons with Disabilities'};
var FNG=/\[\[fn:\d+\]\]/g,CODE=/\b(CAT|CCPR|CED|CEDAW|CERD|CESCR|CMW|CRC|CRPD)\b/g;
var B1='(?<![\\p{L}\\p{N}])',B2='(?![\\p{L}\\p{N}])',WCH='[\\p{L}\\p{N}]*',GAP='(?:\\s|\\[\\[fn:\\d+\\]\\])+';
var SYN=/[.*+?^${}()|[\]\\\/]/;

function qNorm(s){return String(s).replace(/[“”„‟]/g,'"').replace(/[‘’‚‛]/g,"'").replace(/[–—­]/g,'-').replace(/\s+/g,' ').trim();}
function normText(s){return qNorm(String(s).replace(FNG,'')).toLowerCase();}
function symCodes(sym){var out=[],s=String(sym||'');if(/\bCAT\/OP\b/.test(s)){out.push('CAT-OP');s=s.replace(/\bCAT\/OP\b/g,' ');}
  var m,re=new RegExp(CODE.source,'g');while((m=re.exec(s))){if(out.indexOf(m[1])<0)out.push(m[1]);}return out;}
function docName(t){t=String(t||'');var k=t.length,a=t.indexOf(':'),b=t.indexOf(' on ');if(a>0)k=Math.min(k,a);if(b>0)k=Math.min(k,b);return t.slice(0,k).trim();}

/* ---------- load: everything computed once from the records ---------- */
var symTitles=new Map();
R.forEach(function(r){var k=String(r.symbol||'');if(!symTitles.has(k))symTitles.set(k,new Set());symTitles.get(k).add(String(r.title||''));});
var D=R.map(function(r,i){
  var text=typeof r.text==='string'?r.text:'',shown=text.replace(FNG,''),marks=(text.match(FNG)||[]).length;
  var lm=/^(\d{1,3})\.\s/.exec(text),lt=/^\(([a-z]{1,4})\)/.exec(text),para=Number(r.paragraph);
  var sym=String(r.symbol||''),title=String(r.title||''),com=String(r.committee||'?'),cs=[com];
  symCodes(sym).forEach(function(c){if(cs.indexOf(c)<0)cs.push(c);});
  var lead=lm?+lm[1]:null;
  var pin=!isFinite(para)?'paragraph not numbered':para===0?'preamble':lt?'subpara. ('+lt[1]+')':'para. '+para;
  var shared=symTitles.get(sym).size>1,st=String(r.short_title||title);
  var cit=shared?com+', '+(docName(title)||st)+' ('+sym+'), '+pin:sym+', '+pin;
  return {i:i,r:r,id:String(r.id==null?'':r.id),text:text,shown:shown,marks:marks,norm:normText(text),lead:lead,para:para,
    lettered:(isFinite(para)&&para!==0&&lt)?lt[1]:null,pin:pin,shared:shared,cit:cit,
    copied:(lead!==null&&lead===para)?shown.replace(/^\d{1,3}\.\s+/,''):shown,
    title:title,st:st,sym:sym,com:com,committees:cs,joint:cs.length>1,year:Number(r.year),
    mismatch:lead!==null&&lead!==para,dupeN:1};
});
var dupMap=new Map();
D.forEach(function(d){if(d.para>0&&!d.lettered){var k=d.title+'|'+d.para;dupMap.set(k,(dupMap.get(k)||0)+1);}});
D.forEach(function(d){if(d.para>0&&!d.lettered)d.dupeN=dupMap.get(d.title+'|'+d.para);});
var grp=new Map(),byId=new Map();
D.forEach(function(d){if(!grp.has(d.title))grp.set(d.title,[]);grp.get(d.title).push(d);if(!byId.has(d.id))byId.set(d.id,d);});
grp.forEach(function(a){a.forEach(function(d,k){d.g=a;d.gk=k;});});
var ys=D.map(function(d){return d.year;}).filter(isFinite);
var YMIN=ys.length?ys.reduce(function(a,b){return Math.min(a,b);}):0,YMAX=ys.length?ys.reduce(function(a,b){return Math.max(a,b);}):0;
var ALL=Array.from(new Set([].concat.apply([],D.map(function(d){return d.committees;})))).sort();
var NTITLES=grp.size,NCOM=new Set(R.map(function(r){return r.committee;})).size;

/* ---------- state ---------- */
var S={tab:0,qApplied:'',parsed:null,err:null,echo:'',terms:[],cm:new Set(ALL),y0:YMIN,y1:YMAX,doc:'',order:'year',shown:25,open:-1,
  stored:new Set(),full:new Set(),ctx:new Map(),draft:[],hits:[],sorted:[],bars:[],cnt:{},extra:0,checks:[],noHl:new Set(),draftBad:new Set(),store:'memory'};
var HLg=null,HLt=null,chart=null;
var rail=$('#rail'),qi=$('#q'),help=$('#help'),y0El=$('#y0'),y1El=$('#y1');

/* ---------- header, footer ---------- */
var src=GC.source?(GC.source_url||/^https?:/.test(String(GC.source))?'<a href="'+esc(GC.source_url||GC.source)+'" target="_blank" rel="noopener">'+esc(GC.source)+'</a>':esc(GC.source)):'source not given';
$('#sub').innerHTML=R.length?fmt(R.length)+' paragraphs from '+fmt(NTITLES)+' General Comments of '+NCOM+' committees, '+YMIN+'–'+YMAX+'. Source: '+src+'.':'No records loaded.';
$('#foot').innerHTML='Source: '+src+(GC.built?' · built '+esc(GC.built):'')+' · Counting, matching and sorting are done by this page’s code; no model is called. · Credits: charts drawn with Chart.js (MIT licence).';
if(!R.length){$('#shell').innerHTML='<p class="empty">No General Comments were attached. Drag “General Comments, paragraph by paragraph” from Your files into the chat.</p>';return;}

/* ---------- query parser ---------- */
function mkTerm(t){
  var raw=t.raw,star=false;
  if(!t.phrase&&/\*$/.test(raw)){star=true;raw=raw.replace(/\*+$/,'');}
  var body=normText(raw);
  if(!body)throw new Error('A star needs letters before it.');
  var words=body.split(' ');
  var rx=words.map(function(w){return Array.from(w).map(function(c){return SYN.test(c)?'\\'+c:c;}).join('');}).join('\\s+')+(star?WCH:'');
  var hl=words.map(function(w){return Array.from(w).map(function(c){
    return c==="'"?"['\\u2018\\u2019\\u201A\\u201B]":c==='"'?'["\\u201C\\u201D\\u201E\\u201F]':c==='-'?'[-\\u2013\\u2014\\u00AD]':SYN.test(c)?'\\'+c:c;}).join('');}).join(GAP)+(star?WCH:'');
  return {t:'term',phrase:!!t.phrase,raw:raw,star:star,re:new RegExp(B1+rx+B2,'u'),hl:B1+hl+B2};
}
function parseQuery(q){
  var s=qNorm(q),tk=[],i=0,c,j,w;
  while(i<s.length){
    c=s[i];
    if(c===' '){i++;continue;}
    if(c==='('||c===')'){tk.push({k:c});i++;continue;}
    if(c==='"'){j=s.indexOf('"',i+1);if(j<0)throw new Error('A quotation mark is not closed. Add the closing " or remove it.');
      w=s.slice(i+1,j).trim();if(!w)throw new Error('A pair of quotation marks has nothing inside.');tk.push({k:'t',phrase:true,raw:w});i=j+1;continue;}
    if(c==='-'&&i+1<s.length&&s[i+1]!==' '){tk.push({k:'NOT'});i++;continue;}
    j=i;while(j<s.length&&' ()"'.indexOf(s[j])<0)j++;
    w=s.slice(i,j);i=j;
    if(w==='AND'||w==='OR'||w==='NOT')tk.push({k:w});else if(w!=='-')tk.push({k:'t',phrase:false,raw:w});
  }
  if(!tk.length)return {tree:null,terms:[],echo:''};
  var p=0,terms=[];
  var peek=function(){return tk[p];};
  var starts=function(t){return !!t&&(t.k==='t'||t.k==='('||t.k==='NOT');};
  function orE(){var a=andE();while(peek()&&peek().k==='OR'){p++;if(!starts(peek()))throw new Error('OR needs a word or phrase after it.');a={t:'or',l:a,r:andE()};}return a;}
  function andE(){var a=notE();for(;;){var t=peek();
    if(t&&t.k==='AND'){p++;if(!starts(peek()))throw new Error('AND needs a word or phrase after it.');a={t:'and',l:a,r:notE()};}
    else if(starts(t)){a={t:'and',l:a,r:notE()};}else break;}return a;}
  function notE(){var t=peek();if(t&&t.k==='NOT'){p++;if(!starts(peek()))throw new Error('NOT needs a word or phrase after it.');return {t:'not',x:notE()};}return prim();}
  function prim(){var t=tk[p++];
    if(!t)throw new Error('The search ends too early. A word or phrase is missing.');
    if(t.k==='('){if(peek()&&peek().k===')')throw new Error('A pair of parentheses has nothing inside.');
      var e=orE();if(!peek()||peek().k!==')')throw new Error('A parenthesis is not closed. Add the closing ) or remove the (.');p++;return e;}
    if(t.k==='t'){var n=mkTerm(t);terms.push(n);return n;}
    if(t.k===')')throw new Error('A closing parenthesis ) has no opening one.');
    throw new Error(t.k+' needs a word or phrase before it.');}
  var tree=orE();
  if(p<tk.length)throw new Error('A closing parenthesis ) has no opening one.');
  function desc(n){
    if(n.t==='term')return n.phrase?'the phrase “'+esc(n.raw)+'”':n.star?'a word starting with '+esc(n.raw):'the word '+esc(n.raw);
    var par=function(x,pt){return (x.t==='and'||x.t==='or')&&x.t!==pt?'('+desc(x)+')':desc(x);};
    if(n.t==='and')return par(n.l,'and')+' and '+par(n.r,'and');
    if(n.t==='or')return par(n.l,'or')+' or '+par(n.r,'or');
    return 'not '+par(n.x,'not');
  }
  var echo=tree.t==='not'?'Paragraphs that do not contain '+desc(tree.x)+'. A search of excluded words only matches everything without them.':'Paragraphs containing '+desc(tree);
  return {tree:tree,terms:terms,echo:echo};
}
function ev(n,s){switch(n.t){case 'term':return n.re.test(s);case 'and':return ev(n.l,s)&&ev(n.r,s);case 'or':return ev(n.l,s)||ev(n.r,s);default:return !ev(n.x,s);}}
function buildHL(tree){
  var out=[];HLg=HLt=null;
  if(!tree)return;
  (function w(n,neg){if(n.t==='term'){if(!neg)out.push(n);}else if(n.t==='not')w(n.x,!neg);else{w(n.l,neg);w(n.r,neg);}})(tree,false);
  if(!out.length)return;
  var s='(?:'+out.slice().sort(function(a,b){return b.hl.length-a.hl.length;}).map(function(n){return n.hl;}).join('|')+')';
  HLg=new RegExp(s,'giu');HLt=new RegExp(s,'iu');
}
function hlHTML(t){
  if(!HLg)return esc(t);
  var o='',last=0,m;HLg.lastIndex=0;
  while((m=HLg.exec(t))){if(!m[0]){HLg.lastIndex++;continue;}o+=esc(t.slice(last,m.index))+'<mark>'+esc(m[0])+'</mark>';last=m.index+m[0].length;}
  return o+esc(t.slice(last));
}
function countHL(t){if(!HLg)return 0;var n=0,m;HLg.lastIndex=0;while((m=HLg.exec(t))){n++;if(!m[0])HLg.lastIndex++;}return n;}

function runSearch(q){
  S.qApplied=qNorm(q);S.parsed=null;S.err=null;S.echo='';S.terms=[];
  if(S.qApplied){try{var r=parseQuery(S.qApplied);S.parsed=r.tree;S.echo=r.echo;S.terms=r.terms;}catch(e){S.err=e.message;}}
  buildHL(S.parsed);S.shown=25;S.open=-1;update();
}

/* ---------- compute ---------- */
function passes(d){
  var ok=false,k;for(k=0;k<d.committees.length;k++){if(S.cm.has(d.committees[k])){ok=true;break;}}
  if(!ok)return false;
  if(isFinite(d.year)){if(d.year<S.y0||d.year>S.y1)return false;}else if(S.y0!==YMIN||S.y1!==YMAX)return false;
  return !S.doc||d.title===S.doc;
}
function sortHits(){
  var byYear=function(a,b){return (b.year-a.year)||(a.title<b.title?-1:a.title>b.title?1:0)||(a.para-b.para)||(a.i-b.i);};
  var byDoc=function(a,b){return (a.title<b.title?-1:a.title>b.title?1:0)||(a.para-b.para)||(a.i-b.i);};
  if(S.order==='doc')S.hits.sort(byDoc);
  else if(S.order==='matches'){S.hits.forEach(function(d){d.m=countHL(d.shown);});S.hits.sort(function(a,b){return (b.m-a.m)||byYear(a,b);});}
  else S.hits.sort(byYear);
  S.sorted=S.hits;
}
function compute(){
  var hits=[];
  if(!S.err){D.forEach(function(d){if(!passes(d))return;if(S.parsed&&!ev(S.parsed,d.norm))return;hits.push(d);});}
  S.hits=hits;
  var cnt={},extra=0;
  hits.forEach(function(d){d.committees.forEach(function(c){cnt[c]=(cnt[c]||0)+1;});extra+=d.committees.length-1;});
  S.cnt=cnt;S.extra=extra;
  S.bars=ALL.filter(function(c){return cnt[c]||S.cm.has(c);}).map(function(c){return {code:c,n:cnt[c]||0};}).sort(function(a,b){return b.n-a.n||(a.code<b.code?-1:1);});
  sortHits();
}

/* ---------- self-checks ---------- */
function runChecks(){
  var C=[],hits=S.hits,n=hits.length,i;
  S.noHl=new Set();
  var nt=S.terms.length;
  C.push({n:'Query understood',ok:!S.err,d:S.err?'The search was not run: '+esc(S.err):!S.qApplied?'No search words; the filters alone select the paragraphs.':S.echo+' ('+nt+' term'+(nt===1?'':'s')+').'});
  var per=25,pages=Math.ceil(n/per),listed=0;for(i=0;i<pages;i++)listed+=Math.min(per,n-i*per);
  var uniq=new Set(S.sorted.map(function(d){return d.i;})).size,br=0,cc=rail.querySelectorAll('.cc'),shownBr=!!S.qApplied&&!S.err;
  if(shownBr)cc.forEach(function(e){br+=parseInt(e.textContent.replace(/\D/g,''),10)||0;});else Object.keys(S.cnt).forEach(function(k){br+=S.cnt[k];});
  C.push({n:'Totals',ok:listed===n&&S.sorted.length===n&&uniq===n&&br===n+S.extra,d:fmt(listed)+' rows across '+pages+' page'+(pages===1?'':'s')+' of 25 = '+fmt(n)+' hits; committee counts sum to '+fmt(br)+' = '+fmt(n)+' hits + '+fmt(S.extra)+' joint hits.'});
  var bs=S.bars.reduce(function(a,b){return a+b.n;},0);
  C.push({n:'Chart total',ok:bs===n+S.extra,d:'The bars sum to '+fmt(bs)+'; hits '+fmt(n)+' + joint hits '+fmt(S.extra)+' = '+fmt(n+S.extra)+'.'});
  if(!HLt)C.push({n:'Highlight',ok:true,d:S.qApplied&&!S.err?'The search holds only excluded words, so there is nothing to highlight.':'No search words, nothing to highlight.'});
  else{var miss=hits.filter(function(d){return !HLt.test(d.shown);});miss.forEach(function(d){S.noHl.add(d.i);});
    C.push({n:'Highlight',ok:!miss.length,d:miss.length?miss.length+' hits matched but are not highlighted (still shown): '+esc(miss.slice(0,5).map(function(d){return d.sym+', '+d.pin;}).join('; '))+(miss.length>5?' and more':'')+'.':'All '+fmt(n)+' hits show at least one highlighted match.'});}
  var raws=S.terms.map(function(t){return t.raw;}).join(' '),hasAp=/'/.test(raws),hasHy=/-/.test(raws);
  if(S.parsed&&(hasAp||hasHy)){var only=hits.filter(function(d){return !ev(S.parsed,d.shown.replace(/\s+/g,' ').toLowerCase());}).length;
    C.push({n:'Normalisation',ok:true,d:'The search has '+(hasAp?'an apostrophe':'')+(hasAp&&hasHy?' and ':'')+(hasHy?'a hyphen':'')+'; curly apostrophes and en or em dashes were matched too. '+fmt(only)+' of '+fmt(n)+' hits contain only those forms.'});}
  else C.push({n:'Normalisation',ok:true,d:'No apostrophe or hyphen in the search terms, so no forms were equated. Curly quotes, dashes and non-breaking spaces are normalised in every search.'});
  var mm=hits.filter(function(d){return d.mismatch;}),dp=hits.filter(function(d){return d.dupeN>1;}),lt=hits.filter(function(d){return d.lettered;});
  C.push({n:'Numbering',ok:true,d:mm.length+' hits whose leading number differs from the record'+(mm.length?' ('+esc(mm.slice(0,3).map(function(d){return d.sym+': begins '+d.lead+', record para. '+d.para;}).join('; '))+(mm.length>3?' and more':'')+')':'')+'; '+dp.length+' that share a pinpoint with another record of the same document'+(dp.length?' ('+esc(dp.slice(0,3).map(function(d){return d.sym+', '+d.pin;}).join('; '))+(dp.length>3?' and more':'')+')':'')+'; '+lt.length+' lettered sub-paragraphs. Flagged rows carry an amber note; nothing is corrected.'});
  var badM=[];
  hits.forEach(function(d){var seg=d.text.split(/(\[\[fn:\d+\]\])/),sh='',pos=[],k;
    for(k=0;k<seg.length;k++){if(k%2)pos.push([sh.length,seg[k]]);else sh+=seg[k];}
    var back=sh,add=0;pos.forEach(function(p){back=back.slice(0,p[0]+add)+p[1]+back.slice(p[0]+add);add+=p[1].length;});
    if(sh!==d.shown||back!==d.text||pos.length!==d.marks||pos.length!==d.text.split('[[fn:').length-1)badM.push(d);});
  C.push({n:'Marks',ok:!badM.length,d:badM.length?badM.length+' hits where the removed footnote marks do not add up: '+esc(badM.slice(0,5).map(function(d){return d.sym+', '+d.pin;}).join('; '))+'.':'For all '+fmt(n)+' hits the marks removed equal the marks in the stored text, and putting them back gives the stored text exactly.'});
  var bad=new Set();S.draft.forEach(function(x){var d=byId.get(x.id);if(!d||d.text!==x.text_as_stored)bad.add(x.id);});S.draftBad=bad;
  C.push({n:'Draft',ok:!bad.size,d:S.draft.length?S.draft.length+' quotation'+(S.draft.length===1?'':'s')+' compared with the stored text of the record with the same id: '+(bad.size?bad.size+' differ ('+esc(Array.from(bad).join(', '))+').':'all identical.'):'Nothing in the draft yet.'});
  return C;
}
function refreshChecks(){S.checks=runChecks();renderStatus();}
function renderStatus(){
  var f=S.checks.filter(function(c){return !c.ok;}).length;
  $('#status').innerHTML=f?'<span class="dot bad"></span><span class="bad">'+f+' check'+(f>1?'s':'')+' failed</span>':'<span class="dot"></span><span class="ok">'+S.checks.length+' checks pass</span>';
  $('#tdot').hidden=$('#tsr').hidden=!f;
}

/* ---------- known quirks (computed at load) ---------- */
var QUIRKS=(function(){
  var q=[],z=D.filter(function(d){return d.para===0;}),sh=[],jt=new Set(),dups=[],mm=D.filter(function(d){return d.mismatch;}),lt=D.filter(function(d){return d.lettered;});
  symTitles.forEach(function(v,k){if(v.size>1)sh.push([k,v.size]);});
  D.forEach(function(d){if(d.joint)jt.add(d.sym);});
  dupMap.forEach(function(v,k){if(v>1)dups.push(k);});
  sh.sort(function(a,b){return b[1]-a[1];});
  q.push([z.length,'records with paragraph 0 (preambles, cited as “preamble”)',z[0]?z[0].sym+', '+z[0].st:'']);
  q.push([sh.length,'symbols that hold more than one document (the citation then names the committee and the document)',sh[0]?sh[0][0]+' holds '+sh[0][1]+' documents':'']);
  q.push([jt.size,'joint General Comments (two committees under one symbol)',jt.size?Array.from(jt)[0]:'']);
  q.push([dups.length,'pinpoints that occur more than once in the same document',dups[0]?dups[0].replace('|',', para. '):'']);
  q.push([mm.length,'records whose text begins with a number that differs from paragraph',mm[0]?mm[0].sym+': begins ‘'+mm[0].lead+'.’, record para. '+mm[0].para:'']);
  q.push([lt.length,'lettered sub-paragraphs numbered by the file (cited as “subpara.”; verify in the document)',lt[0]?lt[0].sym+', '+lt[0].pin+' (file para. '+lt[0].para+')':'']);
  var dupIds=D.length-byId.size;
  q.push([dupIds,'records sharing an id with another record',dupIds?'ids are used to find draft items again':'none']);
  q.push([typeof GC.count==='string'?1:0,'top-level count given as text','count is “'+GC.count+'”; the app uses records.length = '+fmt(R.length)]);
  return q;
})();

/* ---------- rail ---------- */
function buildRail(){
  $('#cmlist').innerHTML=ALL.map(function(c){return '<label class="cb"><input type="checkbox" data-code="'+esc(c)+'"><span class="badge">'+esc(c)+'</span><span class="cname">'+esc(NAMES[c]||'')+'</span><span class="cc mono2"></span></label>';}).join('');
  y0El.min=y1El.min=YMIN;y0El.max=y1El.max=YMAX;y0El.value=YMIN;y1El.value=YMAX;
  var g=new Map();
  D.forEach(function(d){var c=d.committees[0];if(!g.has(c))g.set(c,new Map());g.get(c).set(d.title,d.st);});
  var sel=$('#doc');
  Array.from(g.keys()).sort().forEach(function(c){var og=document.createElement('optgroup');og.label=c+(NAMES[c]?' – '+NAMES[c]:'');
    Array.from(g.get(c).entries()).sort(function(a,b){return a[1]<b[1]?-1:a[1]>b[1]?1:0;}).forEach(function(e){var o=document.createElement('option');o.value=e[0];o.textContent=e[1];og.appendChild(o);});
    sel.appendChild(og);});
}
function renderRail(){
  $('#bign').textContent=fmt(S.hits.length);$('#bigof').textContent='of '+fmt(D.length);
  var showCnt=!!S.qApplied&&!S.err;
  rail.querySelectorAll('input[data-code]').forEach(function(cb){cb.checked=S.cm.has(cb.dataset.code);cb.parentNode.querySelector('.cc').textContent=showCnt?'['+fmt(S.cnt[cb.dataset.code]||0)+']':'';});
  var ch=[];
  if(S.qApplied)ch.push(['q','Search: '+S.qApplied]);
  if(S.cm.size!==ALL.length)ch.push(['cm','Committees: '+(S.cm.size?Array.from(S.cm).sort().join(', '):'none')]);
  if(S.y0!==YMIN||S.y1!==YMAX)ch.push(['y','Years: '+S.y0+'–'+S.y1]);
  if(S.doc){var d0=grp.get(S.doc);ch.push(['doc','Document: '+(d0?d0[0].st:S.doc)]);}
  $('#chips').innerHTML=ch.map(function(c){return '<button type="button" class="chip" data-chip="'+c[0]+'" aria-label="Remove filter: '+esc(c[1])+'">'+esc(c[1])+' ×</button>';}).join('');
  $('#clear').hidden=!ch.length;
  $('#echo').innerHTML=S.err?'<span class="err" role="alert">'+esc(S.err)+' No search was run.</span>':S.echo;
  $('#yerr').hidden=S.y0<=S.y1;
}
function syncControls(){y0El.value=S.y0;y1El.value=S.y1;$('#doc').value=S.doc;}

/* ---------- panels ---------- */
function renderActive(){[renderOverview,renderParagraphs,renderDraft,renderCheck][S.tab]();}
function renderTabs(){$('#t2 .tl').textContent='03 DRAFT ('+S.draft.length+')';}
function renderOverview(){
  var box=$('#fig1'),bars=S.bars;
  if(chart){chart.destroy();chart=null;}
  if(!S.hits.length){box.innerHTML='<p class="empty">'+(S.err?'The search could not run. See the message under the search box.':'No paragraph matches this search and these filters.')+'</p>';return;}
  var aria='Paragraphs per committee: '+bars.map(function(b){return b.code+' '+fmt(b.n);}).join(', ')+'.';
  var tbl='<table><caption>Same numbers as the chart</caption><thead><tr><th scope="col">Committee</th><th scope="col" class="num">Paragraphs</th></tr></thead><tbody>'+
    bars.map(function(b){return '<tr><th scope="row"><span class="badge">'+esc(b.code)+'</span> <span style="font:400 14px system-ui;text-transform:none;letter-spacing:0;color:var(--grey)">'+esc(NAMES[b.code]||'')+'</span></th><td class="num">'+fmt(b.n)+'</td></tr>';}).join('')+'</tbody></table>';
  box.innerHTML='<div class="figrow"><div class="chartbox" style="height:'+Math.max(140,bars.length*34+50)+'px"><canvas id="cv" role="img" aria-label="'+esc(aria)+'"><p>'+esc(aria)+'</p></canvas></div>'+tbl+'</div>';
  if(!window.Chart)return;
  var F='ui-monospace,Menlo,Consolas,monospace';
  chart=new Chart($('#cv'),{type:'bar',data:{labels:bars.map(function(b){return b.code;}),datasets:[{data:bars.map(function(b){return b.n;}),backgroundColor:'#9b2335',barPercentage:.7,categoryPercentage:.85}]},
    options:{indexAxis:'y',responsive:true,maintainAspectRatio:false,animation:false,layout:{padding:{right:52}},
      plugins:{legend:{display:false}},
      scales:{x:{beginAtZero:true,grid:{color:'#e6dfd0'},ticks:{maxTicksLimit:8,color:'#5a554c',font:{size:13}}},y:{grid:{display:false},ticks:{color:'#1d1b18',font:{family:F,size:13}}}},
      onClick:function(ev,els){if(!els.length)return;var code=bars[els[0].index].code;setTimeout(function(){S.cm=new Set([code]);S.shown=25;update();},0);},
      onHover:function(ev,els){ev.native.target.style.cursor=els.length?'pointer':'default';}},
    plugins:[{id:'vals',afterDatasetsDraw:function(c){var x=c.ctx;x.save();x.fillStyle='#1d1b18';x.font='13px '+F;x.textBaseline='middle';
      c.getDatasetMeta(0).data.forEach(function(b,k){x.fillText(fmt(c.data.datasets[0].data[k]),b.x+6,b.y);});x.restore();}}]});
}
function summary(){
  var n=S.hits.length,cm=new Set(),a=1e9,b=-1e9;
  S.hits.forEach(function(d){d.committees.forEach(function(c){cm.add(c);});if(isFinite(d.year)){a=Math.min(a,d.year);b=Math.max(b,d.year);}});
  if(S.err)return 'The search could not run, so no paragraphs are shown.';
  var tail=n?' · '+cm.size+' committee'+(cm.size===1?'':'s')+' · '+a+'–'+b:'';
  return S.qApplied?fmt(n)+' of '+fmt(D.length)+' paragraphs match'+tail:fmt(n)+' of '+fmt(D.length)+' paragraphs shown · no search words'+tail.replace(/^ ·/,' ·');
}
function renderParagraphs(){
  $('#psum').textContent=summary();
  $('#pord').textContent=S.order==='doc'?'sorted by document, then paragraph':S.order==='matches'?'sorted by number of matched words, most first, then year':'sorted by year, newest first, then by document and paragraph';
  $('#ord').value=S.order;renderRows();
}
function clip(t){
  if(t.length<=700)return {t:t,cut:false};
  var end=700,m;
  if(HLg){HLg.lastIndex=0;m=HLg.exec(t);if(m&&m[0]&&m.index+m[0].length>700)end=m.index+m[0].length;}
  if(end>=t.length)return {t:t,cut:false};
  var k;
  if(end===700){var sub=t.slice(0,700);k=Math.max(sub.lastIndexOf(' '),sub.lastIndexOf('\n'),sub.lastIndexOf(' '));if(k<1)k=700;}
  else{var mm=/\s/.exec(t.slice(end));k=mm?end+mm.index:t.length;}
  return k>=t.length?{t:t,cut:false}:{t:t.slice(0,k),cut:true};
}
function notes(d){
  var a=[];
  if(d.mismatch)a.push('the text begins ‘'+d.lead+'.’ but the record is para. '+d.para+': check the document');
  if(d.lettered)a.push('a lettered sub-paragraph, numbered '+d.para+' by the file: check the document before citing');
  if(d.dupeN>1)a.push((d.dupeN===2?'two':d.dupeN)+' records share this pinpoint');
  if(d.joint)a.push('joint General Comment');
  if(S.noHl.has(d.i))a.push('matched, not highlighted');
  return a;
}
function rowHTML(d){
  var open=S.open===d.i,stored=S.stored.has(d.i),base=stored?d.text:d.shown,t=base,cut=false;
  if(!S.full.has(d.i)){var c=clip(base);t=c.t;cut=c.cut;}
  var words=d.shown.trim()?d.shown.trim().split(/\s+/).length:0;
  var link=d.r.doc_url?'<a href="'+esc(d.r.doc_url)+'" target="_blank" rel="noopener">'+esc(d.sym)+'</a>':esc(d.sym);
  var cx=S.ctx.get(d.i)||{};
  var nb=function(k){var x=d.g[d.gk+k];return x?'<p class="ctx"><span class="lab mono2">'+(k<0?'previous':'next')+' · '+esc(x.pin)+'</span>'+esc(x.shown)+'</p>':'<p class="ctx mono2">No '+(k<0?'previous':'next')+' paragraph in this document.</p>';};
  var h='<article class="row'+(open?' open':'')+'" data-i="'+d.i+'" aria-labelledby="h'+d.i+'">';
  h+='<h3 class="rh" id="h'+d.i+'"><button type="button" class="rowbtn" data-act="toggle" aria-expanded="'+open+'">'+d.committees.map(function(c){return '<span class="badge">'+esc(c)+'</span>';}).join('')+'<span>'+esc(d.st)+'</span></button></h3>';
  h+='<p class="meta mono2">'+link+' · <span class="pin">'+esc(d.pin)+'</span> · '+(isFinite(d.year)?d.year:'year not given')+'</p>';
  if(open&&cx.p)h+=nb(-1);
  h+='<p class="txt">'+hlHTML(t)+(cut?'…':'')+'</p>';
  if(cut)h+='<p class="sub2"><button type="button" class="lnk" data-act="full">Show the full paragraph ('+fmt(words)+' words)</button></p>';
  if(open&&cx.n)h+=nb(1);
  if(d.marks)h+='<p class="sub2">'+(stored?'Shown as stored, with '+d.marks+' footnote mark'+(d.marks>1?'s':'')+' · <button type="button" class="lnk" data-act="stored">hide the footnote marks</button>':d.marks+' footnote mark'+(d.marks>1?'s':'')+' removed · <button type="button" class="lnk" data-act="stored">show as stored</button>')+'</p>';
  notes(d).forEach(function(x){h+='<p class="amber">'+esc(x)+'</p>';});
  if(open){
    h+='<div class="actions"><button type="button" class="btn" data-act="cite">Copy citation</button><button type="button" class="btn" data-act="quote">Copy quotation</button><button type="button" class="btn ghost" data-act="add">Add to draft</button>';
    h+='<span class="mono2">Context: <button type="button" class="lnk" data-act="prev">previous</button> | <button type="button" class="lnk" data-act="next">next</button></span></div>';
    h+='<p class="sub2">Citation style: UN short form, built from this record’s fields only: <b>'+esc(d.cit)+'</b></p><div class="copied" role="status" aria-live="polite"></div>';
  }
  return h+'</article>';
}
function renderRows(focusFrom){
  var n=S.sorted.length,list=S.sorted.slice(0,S.shown);
  $('#rows').innerHTML=list.length?list.map(rowHTML).join(''):'<p class="empty">'+(S.err?esc(S.err):'No paragraph matches. Try fewer words, a star ending (child*), or clear a filter.')+'</p>';
  $('#more').innerHTML=S.shown<n?'<p style="margin:16px 0"><button type="button" class="btn" id="morebtn">Show 25 more</button> <span class="mono2">showing '+fmt(list.length)+' of '+fmt(n)+'</span></p>':'';
  if(focusFrom!=null){var a=$('#rows').querySelectorAll('article')[focusFrom];if(a)a.querySelector('button').focus();}
}
function refreshRow(i,act){
  var a=$('#rows article[data-i="'+i+'"]');if(!a)return;
  a.outerHTML=rowHTML(D[i]);
  if(act){var b=$('#rows article[data-i="'+i+'"] [data-act="'+act+'"]');if(b)b.focus();}
}

/* ---------- copy, draft ---------- */
function copyText(str,msg){
  var done=function(){msg.innerHTML='Copied to the clipboard:<span class="sent"></span>';msg.querySelector('.sent').textContent=str;};
  var fail=function(){msg.innerHTML='The clipboard is blocked here. Select the text below and press Ctrl+C (Cmd+C on a Mac).<textarea class="fb" readonly aria-label="Text to copy"></textarea><button type="button" class="btn ghost">Select and copy</button>';
    var ta=msg.querySelector('textarea');ta.value=str;ta.focus();ta.select();
    msg.querySelector('button').onclick=function(){ta.focus();ta.select();try{document.execCommand('copy');}catch(e){}};};
  try{if(navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText(str).then(done,fail);return;}}catch(e){}
  fail();
}
var KEY='gc-verbatim-finder-draft-v1';
function loadDraft(){try{var s=localStorage.getItem(KEY);if(s){var a=JSON.parse(s);if(Array.isArray(a))S.draft=a.filter(function(x){return x&&typeof x.id==='string'&&typeof x.citation==='string';});}localStorage.setItem(KEY+'-t','1');localStorage.removeItem(KEY+'-t');S.store='localStorage';}catch(e){S.store='memory';}}
function saveDraft(){try{localStorage.setItem(KEY,JSON.stringify(S.draft));S.store='localStorage';}catch(e){S.store='memory';}}
var quoteOf=function(d){return '“'+d.copied+'”';};
function addDraft(d,msg){
  if(S.draft.some(function(x){return x.id===d.id;})){msg.textContent='Already in your draft.';return;}
  S.draft.push({id:d.id,quotation:quoteOf(d),citation:d.cit,symbol:d.sym,paragraph:d.r.paragraph,pinpoint:d.pin,committee:d.com,short_title:d.st,year:d.r.year,text_copied:d.copied,text_as_stored:d.text,doc_url:d.r.doc_url||''});
  saveDraft();refreshChecks();renderTabs();msg.textContent='Added to your draft ('+S.draft.length+').';
}
var allText=function(){return S.draft.map(function(x){return x.quotation+'\n'+x.citation;}).join('\n\n');};
function csvText(){
  var cols=['citation','symbol','paragraph','pinpoint','committee','short_title','year','text_copied','text_as_stored','doc_url'];
  var q=function(v){return '"'+String(v==null?'':v).replace(/"/g,'""')+'"';};
  return '﻿'+[cols.map(q).join(',')].concat(S.draft.map(function(x){return cols.map(function(c){return q(x[c]);}).join(',');})).join('\r\n');
}
function download(name,type,content,msg){
  try{var u=URL.createObjectURL(new Blob([content],{type:type})),a=document.createElement('a');a.href=u;a.download=name;document.body.appendChild(a);a.click();a.remove();setTimeout(function(){URL.revokeObjectURL(u);},3000);
    msg.textContent='Prepared '+name+'. If nothing was saved, use Copy all instead.';}
  catch(e){msg.textContent='Downloads are blocked here. Use Copy all instead.';}
}
function renderDraft(){
  var n=S.draft.length,h='<h2 class="h2">Your draft ('+n+' quotation'+(n===1?'':'s')+')</h2>';
  h+='<p class="hint mono">'+(S.store==='localStorage'?'Kept in this browser (localStorage), so it survives a reload.':'localStorage is not available here: the draft is kept in memory and is lost when you reload. Download it before you leave.')+'</p>';
  if(!n)h+='<p class="empty">Nothing collected yet. On tab 02, open a paragraph and press “Add to draft”.</p>';
  else{
    h+='<div class="bar"><button type="button" class="btn" data-d="copyall">Copy all</button><button type="button" class="btn ghost" data-d="txt">Download .txt</button><button type="button" class="btn ghost" data-d="csv">Download .csv</button></div><div class="copied" id="dmsg" role="status" aria-live="polite"></div>';
    S.draft.forEach(function(x,k){
      h+='<div class="dli"><p class="q">'+esc(x.quotation)+'</p><p class="sub2"><span class="pin">'+esc(x.citation)+'</span> · '+(x.doc_url?'<a href="'+esc(x.doc_url)+'" target="_blank" rel="noopener">'+esc(x.symbol)+'</a>':esc(x.symbol))+' · '+esc(x.year)+'</p>';
      if(S.draftBad.has(x.id))h+='<p class="amber">The stored text of this record differs from the text saved here, or the record is not in this file: check the document.</p>';
      h+='<button type="button" class="lnk" data-d="rm" data-k="'+k+'">Remove</button></div>';
    });
  }
  $('#draft').innerHTML=h;
}
function renderCheck(){
  $('#chk').innerHTML='<h2 class="h2">Can I trust this?</h2><p class="hint mono">The app can only return paragraphs that exist, with their real symbol and paragraph number. Citations and quotations are built from those fields, never written.</p>'+
  '<h3 class="fig"><span class="mono">CHECKS</span>How the app checks itself</h3><ul class="checks">'+S.checks.map(function(c){return '<li><span class="st '+(c.ok?'ok':'bad')+'">'+(c.ok?'pass':'check failed')+'</span><div><b>'+esc(c.n)+'.</b> '+c.d+'</div></li>';}).join('')+'</ul>'+
  '<h3 class="fig"><span class="mono">QUIRKS</span>Known quirks of this file</h3><p class="hint mono">Counted at load, before any search</p><ul class="quirks">'+QUIRKS.map(function(q){return '<li><span class="qn">'+fmt(q[0])+'</span><div>'+esc(q[1])+(q[2]?'<br><span class="mono2" style="color:var(--grey)">e.g. '+esc(q[2])+'</span>':'')+'</div></li>';}).join('')+'</ul>'+
  '<h3 class="fig"><span class="mono">METHOD</span>How this is computed</h3><ol class="how2">'+
  '<li>Everything is read from <b>'+fmt(R.length)+'</b> records of the attached file when the page opens. Nothing is sent anywhere and no model is called.</li>'+
  '<li>For matching, the text loses its footnote marks; curly quotes become straight, en and em dashes and soft hyphens become a hyphen, every space and line break becomes one space, and case is ignored. Your search is treated the same way.</li>'+
  '<li>A space or AND joins terms; NOT binds first, then AND, then OR; parentheses override. A word matches whole words only (a hyphen is a boundary, so “state” finds “non-State”); a star at the end allows any ending.</li>'+
  '<li>Hits are the paragraphs that satisfy the query and pass the committee, years and document filters. A record counts under every committee found in its symbol and its committee field.</li>'+
  '<li>The text shown and copied is the stored text without footnote marks; the leading “12.” is dropped from a copied quotation only when it equals the record’s paragraph number.</li>'+
  '<li>Citation = symbol, pinpoint: “para. N”, “preamble” for paragraph 0, “subpara. (b)” for lettered sub-paragraphs. When a symbol holds several documents, the committee and the document come first and the symbol goes in parentheses.</li>'+
  '<li>Order: year, newest first, then document, then paragraph. Older General Comments may have been replaced by later ones; the file has no such field, so the year is on every row.</li></ol>';
}

/* ---------- tabs and events ---------- */
var tabs=[0,1,2,3].map(function(k){return $('#t'+k);}),panels=[0,1,2,3].map(function(k){return $('#p'+k);});
function setTab(i,focus){
  S.tab=i;
  tabs.forEach(function(t,k){t.setAttribute('aria-selected',k===i);t.tabIndex=k===i?0:-1;});
  panels.forEach(function(p,k){p.hidden=k!==i;});
  $('#shell').classList.toggle('norail',i===2);rail.hidden=i===2;
  renderActive();if(focus)tabs[i].focus();
}
function update(){compute();renderRail();refreshChecks();renderActive();}
tabs.forEach(function(t,k){t.addEventListener('click',function(){setTab(k);});});
$('#tabs').addEventListener('keydown',function(e){var i=S.tab;
  if(e.key==='ArrowRight')i=(i+1)%4;else if(e.key==='ArrowLeft')i=(i+3)%4;else if(e.key==='Home')i=0;else if(e.key==='End')i=3;else return;
  e.preventDefault();setTab(i,true);});
$('#sf').addEventListener('submit',function(e){e.preventDefault();help.hidden=true;runSearch(qi.value);});
qi.addEventListener('focus',function(){if(!qi.value)help.hidden=false;});
qi.addEventListener('input',function(){help.hidden=!!qi.value;});
qi.addEventListener('keydown',function(e){
  if(e.key==='ArrowDown'&&!qi.value){e.preventDefault();help.hidden=false;help.querySelector('button').focus();}
  else if(e.key==='Escape')help.hidden=true;});
help.addEventListener('mousedown',function(e){e.preventDefault();});
help.addEventListener('keydown',function(e){
  var bs=Array.from(help.querySelectorAll('button')),k=bs.indexOf(document.activeElement);
  if(e.key==='ArrowDown'){e.preventDefault();bs[Math.min(k+1,bs.length-1)].focus();}
  else if(e.key==='ArrowUp'){e.preventDefault();if(k<=0)qi.focus();else bs[k-1].focus();}
  else if(e.key==='Escape'){help.hidden=true;qi.focus();}});
help.addEventListener('click',function(e){var b=e.target.closest('[data-ex]');if(!b)return;qi.value=b.dataset.ex;help.hidden=true;qi.focus();runSearch(qi.value);});
$('#sw').addEventListener('focusout',function(e){if(!$('#sw').contains(e.relatedTarget))help.hidden=true;});
$('#fbtn').addEventListener('click',function(){var o=$('#fbtn').getAttribute('aria-expanded')!=='true';$('#fbtn').setAttribute('aria-expanded',o);$('#fbody').hidden=!o;});
$('#cmlist').addEventListener('change',function(e){var cb=e.target.closest('input[data-code]');if(!cb)return;cb.checked?S.cm.add(cb.dataset.code):S.cm.delete(cb.dataset.code);S.shown=25;update();});
$('#call').addEventListener('click',function(){S.cm=new Set(ALL);S.shown=25;update();});
$('#cnone').addEventListener('click',function(){S.cm=new Set();S.shown=25;update();});
function readYears(){var a=parseInt(y0El.value,10),b=parseInt(y1El.value,10);S.y0=isFinite(a)?a:YMIN;S.y1=isFinite(b)?b:YMAX;S.shown=25;update();}
y0El.addEventListener('change',readYears);y1El.addEventListener('change',readYears);
$('#doc').addEventListener('change',function(){S.doc=$('#doc').value;S.shown=25;update();});
$('#ord').addEventListener('change',function(){S.order=$('#ord').value;S.shown=25;S.open=-1;sortHits();renderParagraphs();});
function clearAll(){S.cm=new Set(ALL);S.y0=YMIN;S.y1=YMAX;S.doc='';qi.value='';syncControls();runSearch('');}
$('#clear').addEventListener('click',clearAll);
$('#chips').addEventListener('click',function(e){var b=e.target.closest('[data-chip]');if(!b)return;var k=b.dataset.chip;
  if(k==='q'){qi.value='';runSearch('');return;}
  if(k==='cm')S.cm=new Set(ALL);else if(k==='y'){S.y0=YMIN;S.y1=YMAX;}else S.doc='';
  syncControls();S.shown=25;update();});
$('#more').addEventListener('click',function(e){if(e.target.id!=='morebtn')return;var old=S.shown;S.shown+=25;renderRows(old);});
$('#rows').addEventListener('click',function(e){
  var art=e.target.closest('article.row');if(!art)return;
  var i=+art.dataset.i,d=D[i],b=e.target.closest('[data-act]'),msg=art.querySelector('.copied');
  if(!b){if(e.target.closest('a,button,textarea')||String(window.getSelection())||S.open===i)return;var p=S.open;S.open=i;if(p>=0)refreshRow(p);refreshRow(i);return;}
  var a=b.dataset.act;
  if(a==='toggle'){var pv=S.open;S.open=pv===i?-1:i;if(pv>=0&&pv!==i)refreshRow(pv);refreshRow(i,'toggle');}
  else if(a==='cite')copyText(d.cit,msg);
  else if(a==='quote')copyText(quoteOf(d)+' '+d.cit,msg);
  else if(a==='add')addDraft(d,msg);
  else if(a==='stored'){S.stored.has(i)?S.stored.delete(i):S.stored.add(i);refreshRow(i,'stored');}
  else if(a==='full'){S.full.add(i);refreshRow(i);}
  else if(a==='prev'||a==='next'){var c=S.ctx.get(i)||{},key=a==='prev'?'p':'n';c[key]=!c[key];S.ctx.set(i,c);refreshRow(i,a);}
});
$('#draft').addEventListener('click',function(e){
  var b=e.target.closest('[data-d]');if(!b)return;var a=b.dataset.d,msg=$('#dmsg');
  if(a==='copyall')copyText(allText(),msg);
  else if(a==='txt')download('draft-quotations.txt','text/plain;charset=utf-8','﻿'+allText(),msg);
  else if(a==='csv')download('draft-quotations.csv','text/csv;charset=utf-8',csvText(),msg);
  else if(a==='rm'){S.draft.splice(+b.dataset.k,1);saveDraft();refreshChecks();renderTabs();renderDraft();}
});

loadDraft();buildRail();renderTabs();setTab(0);update();qi.focus();
})();
</script>
</body>
</html>
```
