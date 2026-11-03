I built the Verbatim finder on the General Comments file you attached: it searches paragraph by paragraph with AND, OR, NOT, exact phrases and endings, and shows each paragraph as stored with a citation built only from the record's fields. You can copy a citation or a quotation, collect quotations in a draft drawer and download them as .txt or .csv. The page checks its own counts, numbering, footnote marks and draft on screen, and no model is called.

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Verbatim finder: General Comments and General Recommendations</title>
<style>
:root{--accent:#1f6fb2;--ink:#17212b;--grey:#5b6672;--line:#d8dee6;--bg:#f5f7fa;--card:#fff;--green:#18723a;--red:#b42318;--amber:#8a5a00}
*{box-sizing:border-box}
[hidden]{display:none!important}
body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.5 system-ui,-apple-system,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif}
.wrap{max-width:1500px;margin:0 auto;padding:24px 20px 56px}
h1{font-size:1.8rem;line-height:1.25;margin:0 0 6px}
h2{font-size:1.2rem;margin:0 0 10px}
h3{font-size:1rem;margin:0}
a{color:var(--accent)}
.desc{margin:0 0 4px;color:var(--grey)}
.lead{margin:0 0 20px}
.grey{color:var(--grey)}
.small{font-size:.9rem}
.sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}
.layout{display:grid;grid-template-columns:minmax(0,1100px) 320px;gap:24px;justify-content:center;align-items:start}
@media(max-width:1000px){.layout{grid-template-columns:minmax(0,1fr)}}
.card{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:16px 18px;margin-bottom:16px}
details.card>summary{cursor:pointer;font-weight:700;font-size:1.1rem}
label{font-weight:600}
form label{display:block;margin-bottom:4px}
.qrow{display:flex;gap:8px}
input[type=text],input[type=number],select{font:inherit;padding:.5em .65em;border:1px solid #8a97a6;border-radius:6px;background:#fff;color:var(--ink)}
#q{flex:1;min-width:0}
.btn{font:inherit;padding:.4em .85em;border:1px solid var(--accent);background:#fff;color:var(--accent);border-radius:6px;cursor:pointer}
.btn.primary{background:var(--accent);color:#fff}
.btn:disabled{opacity:.6;cursor:default}
.btn.ex{margin:0 6px 6px 0;font-family:ui-monospace,Menlo,Consolas,monospace;font-size:.88rem}
.lnk{font:inherit;background:none;border:0;padding:0;color:var(--accent);text-decoration:underline;cursor:pointer}
.lnk:disabled{color:var(--grey);text-decoration:none;cursor:default}
:focus-visible{outline:3px solid var(--accent);outline-offset:2px}
.err{color:var(--red);font-weight:600;margin-top:8px}
.echo{margin-top:8px;font-weight:600}
.help{margin:10px 0 6px;padding-left:20px}
code{background:#eef2f6;padding:0 .3em;border-radius:3px;font-size:.92em}
fieldset{border:1px solid var(--line);border-radius:8px;margin:0 0 12px;padding:8px 12px}
legend{font-weight:700;padding:0 6px}
.coms{display:grid;grid-template-columns:repeat(auto-fill,minmax(310px,1fr));gap:2px 16px}
.cb{font-weight:400;display:block;padding:2px 0}
.cb input{margin-right:4px}
.frow{display:flex;flex-wrap:wrap;gap:12px 20px;align-items:end}
.frow input[type=number]{width:6.5em}
.frow select{max-width:100%}
.sumrow{display:flex;flex-wrap:wrap;gap:8px 20px;align-items:center;justify-content:space-between}
#summary{font-size:1.15rem;font-weight:700;margin:0}
.st{font-weight:700}
.st.pass{color:var(--green)}
.st.fail{color:var(--red)}
.st.note{color:var(--amber)}
#checks,#quirks{padding-left:20px;margin:8px 0}
#checks li,#quirks li{margin-bottom:6px}
.chartwrap{display:grid;grid-template-columns:minmax(0,1fr) 270px;gap:16px;align-items:start}
@media(max-width:760px){.chartwrap{grid-template-columns:minmax(0,1fr)}}
#chartbox{position:relative}
table{border-collapse:collapse;width:100%;font-size:.92rem}
th,td{border-bottom:1px solid var(--line);padding:3px 6px;text-align:left}
td.num,th.num{text-align:right}
.row{background:#fff;border:1px solid var(--line);border-radius:10px;padding:14px 16px;margin-bottom:12px}
.rowhead{display:flex;flex-wrap:wrap;align-items:baseline;gap:4px 8px}
.badge{display:inline-block;background:#e6f0f9;color:#124a78;border:1px solid #b9d3e8;border-radius:4px;padding:0 .45em;font-size:.85rem;font-weight:700;margin-right:2px}
.cite{margin-top:2px}
.txt{white-space:pre-wrap;overflow-wrap:anywhere;margin:8px 0}
mark{background:#fff3a3;color:#111;font-weight:700;padding:0 1px;border-radius:2px}
.note{background:#fff4d6;border-left:4px solid #e0a100;color:#5c3d00;padding:4px 10px;margin:6px 0;font-size:.92rem}
.ctx{border-left:3px solid #c3cbd4;padding-left:10px;margin:8px 0}
.acts{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin-top:10px}
.drawer{position:sticky;top:12px;max-height:calc(100vh - 24px);overflow:auto}
@media(max-width:1000px){.drawer{position:static;max-height:none}}
.ditems{padding-left:20px;margin:8px 0}
.ditems li{margin-bottom:12px}
.dq{white-space:pre-wrap;overflow-wrap:anywhere;max-height:11em;overflow:auto;font-size:.92rem}
.dc{font-weight:700;font-size:.92rem;margin:2px 0}
.dbtns{display:flex;flex-wrap:wrap;gap:8px;margin:8px 0}
.toast{position:fixed;left:16px;bottom:16px;max-width:min(680px,calc(100vw - 32px));background:#17212b;color:#fff;padding:12px 14px;border-radius:8px;box-shadow:0 4px 18px rgba(0,0,0,.35);z-index:20}
.toast .btn{margin-top:8px}
.sent{white-space:pre-wrap;overflow-wrap:anywhere;max-height:9em;overflow:auto;background:#0e151c;padding:6px 8px;border-radius:4px;margin-top:6px;font-size:.9rem}
.toast textarea{width:100%;font:inherit;margin-top:6px}
footer{margin-top:24px;color:var(--grey);font-size:.92rem}
.empty{color:var(--grey)}
</style>
</head>
<body>
<div class="wrap" id="app">
<header>
  <h1>Verbatim finder: General Comments and General Recommendations</h1>
  <p id="desc" class="desc"></p>
  <p class="lead">This page retrieves; it never writes. Every paragraph shown is a record of the file, as stored.</p>
</header>
<div class="layout">
<main>
  <section class="card" aria-labelledby="sh">
    <h2 id="sh">Search</h2>
    <form id="sform" role="search" autocomplete="off">
      <label for="q">Search the paragraphs</label>
      <div class="qrow"><input id="q" type="text" spellcheck="false"><button class="btn primary" type="submit">Search</button></div>
    </form>
    <div id="qerr" class="err" role="alert"></div>
    <div id="echo" class="echo" aria-live="polite"></div>
    <p class="small" style="margin:10px 0 4px">Examples, one click fills the box and searches:</p>
    <div id="examples"></div>
    <ul class="help small">
      <li>A space or <code>AND</code> joins words: both must be there.</li>
      <li><code>OR</code> accepts either; <code>NOT</code> or a leading minus (<code>-detention</code>) leaves out paragraphs with that word.</li>
      <li>Double quotes make an exact phrase: <code>"best interests"</code>.</li>
      <li>Parentheses group: <code>(torture OR ill-treatment) NOT detention</code>.</li>
      <li>A star at the end of a word means any ending: <code>child*</code> finds children.</li>
      <li>Operators must be in capitals; lower-case &ldquo;or&rdquo; is just a word.</li>
    </ul>
    <p class="grey small" style="margin:0">Whole words, any case. Curly and straight quotes, apostrophes, dashes and hyphens count as the same, and footnote marks are skipped, so State's finds State&rsquo;s and a phrase can cross a footnote.</p>
  </section>

  <section class="card" aria-labelledby="fh">
    <h2 id="fh">Filters</h2>
    <fieldset>
      <legend>Committee</legend>
      <div id="coms" class="coms"></div>
      <div style="margin-top:8px"><button type="button" class="btn" id="all">all</button> <button type="button" class="btn" id="none">none</button> <span class="grey small">The number in brackets is how many hits the committee has.</span></div>
    </fieldset>
    <div class="frow">
      <div><label for="yf">Year from</label><br><input type="number" id="yf"></div>
      <div><label for="yt">to</label><br><input type="number" id="yt"></div>
      <div><label for="doc">Document</label><br><select id="doc"></select></div>
    </div>
  </section>

  <section class="card" aria-labelledby="sumh">
    <h2 id="sumh" class="sr">Summary</h2>
    <div class="sumrow">
      <p id="summary" aria-live="polite"></p>
      <div><label for="sort">Order</label> <select id="sort">
        <option value="newest">Year, newest first</option>
        <option value="doc">Document order</option>
        <option value="matches">Most matches first</option>
      </select></div>
    </div>
    <p id="orderline" class="grey small" style="margin:4px 0 0"></p>
    <p class="small" style="margin:8px 0 0"><strong>How this is computed:</strong> a paragraph is a hit when its text (footnote marks left out) satisfies the query and it passes the committee, year and document filters. This page&rsquo;s code does the counting; nothing is estimated.</p>
  </section>

  <details class="card" id="checkspanel" open>
    <summary>Checks: the page checks its own work</summary>
    <p class="grey small" style="margin:6px 0 0">Each line compares two numbers or texts. A failed check marks rows; it never hides them.</p>
    <ul id="checks"></ul>
    <h3>Known quirks of this file (found when the page loaded, before any search)</h3>
    <ul id="quirks"></ul>
  </details>

  <section class="card" aria-labelledby="ch">
    <h2 id="ch">Hits per committee</h2>
    <div class="chartwrap">
      <div>
        <div id="chartbox"><canvas id="chart" role="img" aria-label="Hits per committee: loading">The numbers are in the table beside this chart.</canvas></div>
        <p id="chartnone" class="grey" hidden></p>
      </div>
      <table>
        <caption class="sr">Hits per committee</caption>
        <thead><tr><th scope="col">Code</th><th scope="col">Committee</th><th scope="col" class="num">Hits</th></tr></thead>
        <tbody id="ctb"></tbody>
        <tfoot><tr><th scope="row" colspan="2">Sum of the bars</th><td class="num" id="ctot"></td></tr></tfoot>
      </table>
    </div>
    <p class="small"><strong>How this is computed:</strong> one count per committee over the paragraphs that match the query and filters. Joint General Comments count under both committees, so the bars can add up to more than the hits. Click a bar to tick that committee alone; a lighter bar is a committee that is not ticked but shares a joint document with a ticked one.</p>
  </section>

  <section aria-labelledby="rh">
    <h2 id="rh">Paragraphs</h2>
    <p id="shownline" class="grey small" style="margin-top:0"></p>
    <p id="empty" class="empty" hidden></p>
    <div id="rows"></div>
    <div id="more" style="margin:12px 0" hidden><button type="button" class="btn primary" id="morebtn"></button></div>
  </section>
</main>

<aside id="drawer" class="card drawer" aria-labelledby="dtitle">
  <h2 id="dtitle">Your draft (0 quotations)</h2>
  <p class="grey small" id="dstore"></p>
  <ol id="ditems" class="ditems"></ol>
  <p id="dempty" class="grey small">Nothing yet. Use &ldquo;Add to draft&rdquo; on a paragraph.</p>
  <div class="dbtns">
    <button type="button" class="btn" id="dcopy">Copy all</button>
    <button type="button" class="btn" id="dtxt">Download .txt</button>
    <button type="button" class="btn" id="dcsv">Download .csv</button>
  </div>
  <p class="grey small">Each item is the quotation as copied, then its citation. The .csv has the stored text too, so you can compare.</p>
</aside>
</div>

<footer>
  <p id="foot"></p>
  <p>Counting, matching and sorting are done by this page&rsquo;s code; no model is called and nothing leaves the browser.</p>
  <p>Credits: charts drawn with Chart.js (MIT licence).</p>
</footer>
</div>

<div id="toast" class="toast" hidden>
  <div id="tlabel"></div>
  <div id="tsent" class="sent"></div>
  <div id="tfb" hidden><textarea id="tta" rows="4" readonly aria-label="Text to copy"></textarea><button type="button" class="btn" id="tsel">Select and copy</button></div>
  <button type="button" class="btn" id="tclose">Dismiss</button>
</div>
<div id="sr" class="sr" aria-live="polite"></div>

<script>
(function(){
'use strict';
const $=id=>document.getElementById(id);
const esc=s=>String(s==null?'':s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;').replace(/'/g,'&#39;');
const fmt=n=>Number(n).toLocaleString('en-US');
const safeUrl=u=>/^https?:\/\//i.test(String(u||''))?String(u):'';
const FN=/\[\[fn:\d+\]\]/g;
const GAP='(?:\\s|\\[\\[fn:\\d+\\]\\])+';
const LB='(?<![\\p{L}\\p{N}])';
const LA='(?![\\p{L}\\p{N}])';
const TAILW='[\\p{L}\\p{N}_]*';
const PAGE=25, CUT=700, KEY='verbatim-finder-draft-v1';
const CN={CAT:'Committee against Torture','CAT-OP':'Subcommittee on Prevention of Torture',CCPR:'Human Rights Committee',CED:'Committee on Enforced Disappearances',CEDAW:'Committee on the Elimination of Discrimination against Women',CERD:'Committee on the Elimination of Racial Discrimination',CESCR:'Committee on Economic, Social and Cultural Rights',CMW:'Committee on Migrant Workers',CRC:'Committee on the Rights of the Child',CRPD:'Committee on the Rights of Persons with Disabilities'};

const D=(window.WORKSHOP_DATA&&window.WORKSHOP_DATA.gc)||{};
const R=Array.isArray(D.records)?D.records:[];
if(!R.length){
  $('app').innerHTML='<h1>Verbatim finder</h1><p class="card">No General Comments were found in this page’s data (<code>WORKSHOP_DATA.gc</code>). Attach the file “General Comments, paragraph by paragraph” and ask for the app again.</p>';
  return;
}

/* ---------- text helpers ---------- */
function punct(s){
  return s.replace(/[“”„]/g,'"').replace(/[‘’‚]/g,"'").replace(/[–—­]/g,'-').replace(/\s+/g,' ');
}
function reEsc(s){return s.replace(/[.*+?^${}()|[\]\\\/]/g,'\\$&');}
function hlEsc(s){
  let o='';
  for(const ch of s){
    if(ch==="'") o+="['‘’‚]";
    else if(ch==='-') o+='[-–—­]';
    else if(ch==='"') o+='["“”„]';
    else o+=reEsc(ch);
  }
  return o;
}
function wordsOf(s){const t=s.trim();return t?t.split(/\s+/).length:0;}

/* ---------- load: one pass over the records ---------- */
const titleSyms=new Map();
R.forEach(r=>{
  const s=String(r.symbol||'');
  if(!titleSyms.has(s)) titleSyms.set(s,new Set());
  titleSyms.get(s).add(String(r.title||''));
});
const CODES=/\b(CAT|CCPR|CED|CEDAW|CERD|CESCR|CMW|CRC|CRPD)\b/g;

function markBad(r){
  const c=r.text.split('[[fn:').length-1;
  if(c!==r.marks) return true;
  const parts=r.text.split(FN), ms=r.text.match(FN)||[];
  let back=parts[0];
  for(let k=0;k<ms.length;k++) back+=ms[k]+parts[k+1];
  return back!==r.text||parts.join('')!==r.shown;
}

const recs=R.map((r,i)=>{
  const text=String(r.text==null?'':r.text);
  const symbol=String(r.symbol||'');
  const title=String(r.title||r.short_title||'');
  const committee=String(r.committee||'');
  const pn=typeof r.paragraph==='number'?r.paragraph:parseInt(r.paragraph,10);
  const paragraph=Number.isFinite(pn)?pn:null;
  const yn=typeof r.year==='number'?r.year:parseInt(r.year,10);
  const marks=(text.match(FN)||[]).length;
  const shown=text.replace(FN,'');
  const lm=/^(\d{1,3})\.\s/.exec(text);
  const leading=lm?parseInt(lm[1],10):null;
  const lt=/^\s*\(([a-z]{1,4})\)/.exec(text);
  let pin;
  if(paragraph===0) pin='preamble';
  else if(lt) pin='subpara. ('+lt[1]+')';
  else pin='para. '+(paragraph===null?'?':paragraph);
  const cs=new Set();
  for(const mm of symbol.matchAll(CODES)){
    let c=mm[1];
    if(c==='CAT'&&(/CAT\/OP/.test(symbol)||committee==='CAT-OP')) c='CAT-OP';
    cs.add(c);
  }
  if(committee) cs.add(committee);
  if(!cs.size) cs.add('unknown');
  const coms=[...cs];
  const symParts=symbol.split(/\s*(?:[–—]|,)\s*/).filter(Boolean);
  const joint=coms.length>1||symParts.length>1;
  const shared=(titleSyms.get(symbol)||new Set()).size>1;
  const docName=(title.split(/:| on /)[0]||'').trim()||title;
  const cite=(shared?committee+', '+docName+' ('+symbol+'), ':symbol+', ')+pin;
  const qtext=(leading!==null&&leading===paragraph?shown.replace(/^\d{1,3}\.\s+/,''):shown).trim();
  const rec={i,key:r.id!=null?String(r.id):'#'+i,text,symbol,title,short:String(r.short_title||title),committee,paragraph,year:Number.isFinite(yn)?yn:NaN,
    url:safeUrl(r.doc_url),marks,shown,leading,lettered:!!lt,pin,coms,joint,shared,cite,qtext,quote:'“'+qtext+'”',
    norm:punct(shown).toLowerCase().trim(),mc:0,raw:null,dup:false,pos:0,rank:0};
  rec.markBad=markBad(rec);
  return rec;
});

const citeCount=new Map();
recs.forEach(r=>{if(r.pin.startsWith('para.')) citeCount.set(r.cite,(citeCount.get(r.cite)||0)+1);});
recs.forEach(r=>{r.dup=r.pin.startsWith('para.')&&citeCount.get(r.cite)>1;});

const coll=new Intl.Collator('en',{numeric:true,sensitivity:'base'});
const titles=[...new Set(recs.map(r=>r.title))].sort(coll.compare);
const rank=new Map(titles.map((t,i)=>[t,i]));
const byTitle=new Map();
recs.forEach(r=>{
  r.rank=rank.get(r.title);
  if(!byTitle.has(r.title)) byTitle.set(r.title,[]);
  byTitle.get(r.title).push(r);
});
byTitle.forEach(a=>{a.sort((x,y)=>(x.paragraph-y.paragraph)||(x.i-y.i));a.forEach((r,k)=>{r.pos=k;});});
const byKey=new Map();
recs.forEach(r=>{if(!byKey.has(r.key)) byKey.set(r.key,r);});
const yrs=recs.map(r=>r.year).filter(Number.isFinite);
const minY=yrs.length?yrs.reduce((a,b)=>Math.min(a,b)):0;
const maxY=yrs.length?yrs.reduce((a,b)=>Math.max(a,b)):0;
const allCom=[...new Set(recs.flatMap(r=>r.coms))].sort();

/* ---------- state ---------- */
const state={q:'',tree:null,termList:[],terms:0,echo:'',error:'',hlRe:null,notOnly:false,matched:recs,
  sel:new Set(allCom),yf:minY,yt:maxY,doc:'',sort:'newest',shown:PAGE,hits:[],counts:{},chartData:[],
  stored:new Set(),expanded:new Set(),ctx:new Map()};
let chart=null;
let draft=[];
let storeOK=false;
try{
  localStorage.setItem(KEY+'-t','1');localStorage.removeItem(KEY+'-t');
  storeOK=true;
  const raw=localStorage.getItem(KEY);
  if(raw){const a=JSON.parse(raw);if(Array.isArray(a)) draft=a.filter(x=>x&&typeof x==='object'&&x.id!=null);}
}catch(e){storeOK=storeOK&&true;}
function saveDraft(){
  if(!storeOK) return;
  try{localStorage.setItem(KEY,JSON.stringify(draft));}catch(e){storeOK=false;}
}

/* ---------- query: tokens, parser, matching ---------- */
class QErr extends Error{}
function tokenize(q){
  q=punct(q);
  const toks=[];let i=0;const n=q.length;
  while(i<n){
    const c=q[i];
    if(/\s/.test(c)){i++;continue;}
    if(c==='('||c===')'){toks.push({t:c});i++;continue;}
    if(c==='"'){
      const j=q.indexOf('"',i+1);
      if(j<0) throw new QErr('Unbalanced quote: a phrase opened with a double quote is never closed.');
      const body=q.slice(i+1,j).trim();
      if(body) toks.push({t:'phrase',v:body});
      i=j+1;continue;
    }
    if(c==='-'&&i+1<n&&!/\s/.test(q[i+1])){toks.push({t:'NOT'});i++;continue;}
    let j=i;
    while(j<n&&!/[\s()"]/.test(q[j])) j++;
    const w=q.slice(i,j);
    i=j;
    if(w==='AND'||w==='OR'||w==='NOT') toks.push({t:w});
    else if(w!=='-'&&w.replace(/\*/g,'')!=='') toks.push({t:'word',v:w});
  }
  return toks;
}
function mkTerm(t){
  if(t.t==='phrase'){
    const ws=t.v.split(/\s+/).filter(Boolean);
    return {op:'term',kind:'phrase',v:t.v,star:false,
      re:new RegExp(LB+ws.map(w=>reEsc(w.toLowerCase())).join('\\s+')+LA,'u'),
      hl:LB+ws.map(hlEsc).join(GAP)+LA};
  }
  const star=/\*$/.test(t.v);
  const w=t.v.replace(/\*+$/,'');
  return {op:'term',kind:'word',v:w,star,
    re:new RegExp(LB+reEsc(w.toLowerCase())+(star?TAILW:'')+LA,'u'),
    hl:LB+hlEsc(w)+(star?TAILW:'')+LA};
}
function parse(toks){
  let p=0;const terms=[];
  const peek=()=>toks[p];
  const starts=t=>t&&(t.t==='word'||t.t==='phrase'||t.t==='('||t.t==='NOT');
  function parseOr(){
    let a=parseAnd();
    while(peek()&&peek().t==='OR'){p++;const b=parseAnd();a={op:'or',a,b};}
    return a;
  }
  function parseAnd(){
    let a=parseNot();
    for(;;){
      const t=peek();
      if(t&&t.t==='AND'){p++;const b=parseNot();a={op:'and',a,b};}
      else if(starts(t)){const b=parseNot();a={op:'and',a,b};}
      else break;
    }
    return a;
  }
  function parseNot(){
    const t=peek();
    if(t&&t.t==='NOT'){p++;return {op:'not',a:parseNot()};}
    return parseAtom();
  }
  function parseAtom(){
    const t=peek();
    if(!t) throw new QErr('The query ends where a word or phrase is expected.');
    if(t.t==='('){
      p++;
      const n=parseOr();
      if(!peek()||peek().t!==')') throw new QErr('Unbalanced parenthesis: a ( has no closing ).');
      p++;return n;
    }
    if(t.t===')') throw new QErr('Unbalanced parenthesis: a ) has no opening ( or the brackets are empty.');
    if(t.t==='word'||t.t==='phrase'){p++;const n=mkTerm(t);terms.push(n);return n;}
    throw new QErr('The operator '+t.t+' is missing a word or phrase next to it.');
  }
  const tree=parseOr();
  if(p<toks.length) throw new QErr('Unbalanced parenthesis: a ) has no opening (.');
  return {tree,terms};
}
function evalNode(n,s){
  switch(n.op){
    case 'term':return n.re.test(s);
    case 'not':return !evalNode(n.a,s);
    case 'and':return evalNode(n.a,s)&&evalNode(n.b,s);
    case 'or':return evalNode(n.a,s)||evalNode(n.b,s);
  }
  return false;
}
function echoOf(n){
  if(n.op==='term') return n.kind==='phrase'?'the phrase “'+n.v+'”':(n.star?'a word beginning with '+n.v:'the word '+n.v);
  if(n.op==='not') return 'not '+((n.a.op==='and'||n.a.op==='or')?'('+echoOf(n.a)+')':echoOf(n.a));
  const wrap=c=>((c.op==='and'||c.op==='or')&&c.op!==n.op)?'('+echoOf(c)+')':echoOf(c);
  return wrap(n.a)+(n.op==='and'?' and ':' or ')+wrap(n.b);
}
function collectHl(n,out){
  if(n.op==='term') out.push(n.hl);
  else if(n.op==='and'||n.op==='or'){collectHl(n.a,out);collectHl(n.b,out);}
}
function countMatches(s,re){
  re.lastIndex=0;
  let n=0,m;
  while((m=re.exec(s))!==null){if(!m[0]){re.lastIndex++;continue;}n++;}
  return n;
}
function hl(str){
  const re=state.hlRe;
  if(!re) return esc(str);
  re.lastIndex=0;
  let out='',last=0,m;
  while((m=re.exec(str))!==null){
    if(!m[0]){re.lastIndex++;continue;}
    out+=esc(str.slice(last,m.index))+'<mark>'+esc(m[0])+'</mark>';
    last=m.index+m[0].length;
  }
  return out+esc(str.slice(last));
}
function rawOf(r){return r.raw||(r.raw=r.shown.replace(/\s+/g,' ').toLowerCase().trim());}

function runSearch(){
  const q=$('q').value;
  state.q=q;state.error='';state.tree=null;state.hlRe=null;state.terms=0;state.termList=[];state.notOnly=false;
  if(q.trim()===''){
    state.matched=recs;
    state.echo='No search words: every paragraph that passes the filters is listed.';
  }else{
    try{
      const res=parse(tokenize(q));
      state.tree=res.tree;state.termList=res.terms;state.terms=res.terms.length;
      const parts=[];
      collectHl(res.tree,parts);
      state.notOnly=parts.length===0;
      state.hlRe=parts.length?new RegExp(parts.sort((a,b)=>b.length-a.length).join('|'),'giu'):null;
      state.echo=(state.notOnly?'Paragraphs for which: ':'Paragraphs containing ')+echoOf(res.tree)+'.'+(state.notOnly?' A query of only NOT terms matches every paragraph that lacks them.':'');
      state.matched=recs.filter(r=>evalNode(res.tree,r.norm));
    }catch(e){
      state.error=(e instanceof QErr)?e.message:'The query could not be turned into a search ('+e.message+').';
      state.tree=null;state.hlRe=null;state.matched=[];state.echo='';
    }
  }
  state.shown=PAGE;
  refresh();
}

/* ---------- hits ---------- */
function passes(r){
  if(!r.coms.some(c=>state.sel.has(c))) return false;
  if(state.yf>minY||state.yt<maxY){if(!(r.year>=state.yf&&r.year<=state.yt)) return false;}
  if(state.doc&&r.title!==state.doc) return false;
  return true;
}
function computeHits(){
  const list=state.matched.filter(passes);
  list.forEach(r=>{r.mc=state.hlRe?countMatches(r.shown,state.hlRe):0;});
  const base=(a,b)=>(b.year-a.year)||(a.rank-b.rank)||(a.paragraph-b.paragraph)||(a.i-b.i);
  const byDoc=(a,b)=>(a.rank-b.rank)||(a.paragraph-b.paragraph)||(a.i-b.i);
  const byMc=(a,b)=>(b.mc-a.mc)||base(a,b);
  list.sort(state.sort==='doc'?byDoc:state.sort==='matches'?byMc:base);
  const counts={};
  list.forEach(r=>{r.coms.forEach(c=>{counts[c]=(counts[c]||0)+1;});});
  state.hits=list;state.counts=counts;
}

/* ---------- rendering ---------- */
function refresh(){
  computeHits();
  document.querySelectorAll('[data-cnt]').forEach(e=>{e.textContent='('+fmt(state.counts[e.getAttribute('data-cnt')]||0)+')';});
  $('qerr').textContent=state.error;
  $('echo').textContent=state.error?'':state.echo;
  renderSummary();renderChart();renderResults();renderChecks();
}
function renderSummary(){
  const h=state.hits;
  const cs=new Set();let y0=Infinity,y1=-Infinity;
  h.forEach(r=>{r.coms.forEach(c=>cs.add(c));if(Number.isFinite(r.year)){y0=Math.min(y0,r.year);y1=Math.max(y1,r.year);}});
  let t;
  if(state.error) t='No results: the query could not be read.';
  else{
    t=fmt(h.length)+' of '+fmt(recs.length)+' paragraphs match'+(state.tree?'':' (no search words)');
    if(h.length) t+=' · '+cs.size+' committee'+(cs.size===1?'':'s')+(Number.isFinite(y0)?' · '+(y0===y1?y0:y0+'–'+y1):'');
  }
  $('summary').textContent=t;
  $('orderline').textContent={newest:'Sorted by year, newest first, then by document and paragraph.',doc:'Sorted by document, then by paragraph.',matches:'Sorted by number of matched words, most first, then by year, newest first.'}[state.sort];
}
function renderChart(){
  const entries=Object.keys(state.counts).map(c=>[c,state.counts[c]]).sort((a,b)=>(b[1]-a[1])||(a[0]<b[0]?-1:1));
  state.chartData=entries;
  const total=entries.reduce((s,e)=>s+e[1],0);
  $('chart').setAttribute('aria-label',entries.length?'Hits per committee, highest first: '+entries.map(e=>e[0]+' '+e[1]).join(', ')+'. The bars add up to '+total+'.':'Hits per committee: no hits.');
  $('ctb').innerHTML=entries.length?entries.map(e=>'<tr><th scope="row">'+esc(e[0])+'</th><td>'+esc(CN[e[0]]||'')+'</td><td class="num">'+fmt(e[1])+'</td></tr>').join(''):'<tr><td colspan="3">No hits</td></tr>';
  $('ctot').textContent=fmt(total);
  if(chart){chart.destroy();chart=null;}
  const ok=typeof window.Chart!=='undefined';
  $('chartbox').hidden=!entries.length||!ok;
  $('chartnone').hidden=entries.length>0&&ok;
  $('chartnone').textContent=entries.length?'The chart library did not load; the table has the same numbers.':'No hits, so there is nothing to chart.';
  if(!entries.length||!ok) return;
  $('chartbox').style.height=(64+entries.length*36)+'px';
  chart=new window.Chart($('chart'),{
    type:'bar',
    data:{labels:entries.map(e=>e[0]),datasets:[{data:entries.map(e=>e[1]),backgroundColor:entries.map(e=>state.sel.has(e[0])?'#1f6fb2':'#a9c9e3'),barPercentage:0.7,categoryPercentage:0.85}]},
    options:{
      indexAxis:'y',responsive:true,maintainAspectRatio:false,animation:false,
      layout:{padding:{right:48}},
      plugins:{legend:{display:false},tooltip:{callbacks:{label:c=>fmt(c.parsed.x)+' paragraphs'}}},
      scales:{
        x:{beginAtZero:true,ticks:{precision:0,maxTicksLimit:10,color:'#5b6672'},grid:{color:'#e3e8ee'},title:{display:true,text:'Paragraphs that match'}},
        y:{grid:{display:false},ticks:{color:'#17212b',font:{size:14}}}
      },
      onClick:(evt,els)=>{
        if(els&&els.length){
          state.sel=new Set([entries[els[0].index][0]]);
          syncChecks();state.shown=PAGE;refresh();
        }
      },
      onHover:(evt,els)=>{if(evt.native&&evt.native.target) evt.native.target.style.cursor=(els&&els.length)?'pointer':'default';}
    },
    plugins:[{id:'endLabels',afterDatasetsDraw(ch){
      const ctx=ch.ctx;
      ctx.save();ctx.fillStyle='#17212b';ctx.font='600 14px system-ui,sans-serif';ctx.textBaseline='middle';ctx.textAlign='left';
      ch.getDatasetMeta(0).data.forEach((bar,i)=>{ctx.fillText(fmt(ch.data.datasets[0].data[i]),bar.x+6,bar.y);});
      ctx.restore();
    }}]
  });
}
function renderResults(){
  $('rows').innerHTML='';
  const h=state.hits;
  const em=$('empty');
  if(state.error){em.hidden=false;em.textContent='Fix the query to see paragraphs. The message above says what is wrong.';}
  else if(!h.length){em.hidden=false;em.textContent='No paragraph matches this query with these filters. Check the committee, year and document filters, and remember that child finds only the whole word (type child* for children).';}
  else em.hidden=true;
  appendRows(0,Math.min(state.shown,h.length));
  updateMore();
}
function appendRows(a,b){$('rows').insertAdjacentHTML('beforeend',state.hits.slice(a,b).map(rowHTML).join(''));}
function updateMore(){
  const len=state.hits.length,rem=Math.max(0,len-state.shown);
  $('more').hidden=rem===0;
  $('morebtn').textContent='Show '+Math.min(PAGE,rem)+' more';
  $('shownline').textContent=len?'Showing '+fmt(Math.min(state.shown,len))+' of '+fmt(len)+' paragraphs.':'';
}
function rowHTML(r){
  const asSt=state.stored.has(r.i),full=state.expanded.has(r.i),cx=state.ctx.get(r.i)||{};
  const base=asSt?r.text:r.shown;
  let part=base,cut=false;
  if(!full&&base.length>CUT){
    let c=CUT;
    while(c>CUT-300&&!/\s/.test(base[c])) c--;
    if(!/\s/.test(base[c])) c=CUT;
    if(state.hlRe){
      state.hlRe.lastIndex=0;
      const m=state.hlRe.exec(base);
      state.hlRe.lastIndex=0;
      if(m&&m[0]&&m.index+m[0].length>c){
        c=m.index+m[0].length;
        while(c<base.length&&!/\s/.test(base[c])) c++;
      }
    }
    if(c<base.length){part=base.slice(0,c);cut=true;}
  }
  const list=byTitle.get(r.title)||[r];
  const prev=list[r.pos-1],next=list[r.pos+1];
  const ctxHTML=(o,lab)=>'<div class="ctx"><div class="grey small"><strong>'+lab+' · '+esc(o.pin)+'</strong></div><div class="txt grey">'+esc(o.shown)+'</div></div>';
  const notes=[];
  if(r.leading!==null&&r.leading!==r.paragraph) notes.push('the text begins ‘'+r.leading+'.’ but the record is '+r.pin+': check the document');
  if(r.lettered) notes.push('a lettered sub-paragraph, numbered '+r.paragraph+' by the file: check the letter in the document');
  if(r.dup) notes.push('two records share this pinpoint');
  if(r.joint) notes.push('joint General Comment');
  if(r.markBad) notes.push('check failed: putting the footnote marks back does not restore the stored text');
  if(state.hlRe&&r.mc===0) notes.push('matched, not highlighted');
  const inD=draft.some(d=>d.id===r.key);
  const link=r.url?'<a href="'+esc(r.url)+'" target="_blank" rel="noopener">'+esc(r.symbol)+'<span class="sr"> (opens in a new tab)</span></a>':esc(r.symbol);
  let fullBtn='';
  if(cut) fullBtn='<button type="button" class="lnk" data-act="full">Show the full paragraph ('+fmt(wordsOf(r.shown))+' words)</button>';
  else if(full&&base.length>CUT) fullBtn='<button type="button" class="lnk" data-act="full">Show less</button>';
  const marksLine=r.marks?'<div class="grey small">'+r.marks+' footnote mark'+(r.marks===1?'':'s')+(asSt?' shown, as stored':' removed')+' · <button type="button" class="lnk" data-act="stored">'+(asSt?'hide the marks':'show as stored')+'</button></div>':'';
  return '<article class="row" data-i="'+r.i+'" tabindex="-1" aria-labelledby="h'+r.i+'">'+
    '<div class="rowhead">'+r.coms.map(c=>'<span class="badge">'+esc(c)+'</span>').join('')+'<h3 id="h'+r.i+'">'+esc(r.short)+'</h3></div>'+
    '<div class="cite">'+link+' · <strong>'+esc(r.pin)+'</strong> · '+esc(Number.isFinite(r.year)?r.year:'year not stated')+'</div>'+
    notes.map(n=>'<div class="note">'+esc(n)+'</div>').join('')+
    (cx.p&&prev?ctxHTML(prev,'Previous record'):'')+
    '<div class="txt">'+hl(part)+(cut?'<span class="grey"> …</span>':'')+'</div>'+
    (cx.n&&next?ctxHTML(next,'Next record'):'')+
    (fullBtn?'<div class="small">'+fullBtn+'</div>':'')+
    marksLine+
    '<div class="grey small">Context: <button type="button" class="lnk" data-act="prev" aria-pressed="'+(!!cx.p)+'"'+(prev?'':' disabled')+'>previous</button> | <button type="button" class="lnk" data-act="next" aria-pressed="'+(!!cx.n)+'"'+(next?'':' disabled')+'>next</button></div>'+
    '<div class="acts"><button type="button" class="btn" data-act="cite">Copy citation</button><button type="button" class="btn" data-act="quote">Copy quotation</button><button type="button" class="btn" data-act="add"'+(inD?' disabled':'')+'>'+(inD?'In your draft':'Add to draft')+'</button><span class="grey small">UN short form</span></div>'+
    '</article>';
}
function updateRow(i,act){
  const old=$('rows').querySelector('article.row[data-i="'+i+'"]');
  if(!old) return;
  old.outerHTML=rowHTML(recs[i]);
  const nw=$('rows').querySelector('article.row[data-i="'+i+'"]');
  if(!nw) return;
  const b=act?nw.querySelector('button[data-act="'+act+'"]'):null;
  if(b&&!b.disabled) b.focus();else nw.focus();
}

/* ---------- checks ---------- */
function renderChecks(){
  const out=[],hits=state.hits;
  const add=(s,t)=>out.push('<li><span class="st '+s+'">'+({pass:'pass',fail:'check failed',note:'note'})[s]+'</span> '+t+'</li>');
  const pins=(rs,n)=>rs.slice(0,n).map(r=>esc(r.cite)).join('; ')+(rs.length>n?' and '+(rs.length-n)+' more':'');
  if(state.error) add('fail','<strong>Query understood.</strong> '+esc(state.error));
  else if(!state.tree) add('pass','<strong>Query understood.</strong> No search words (0 terms). Every paragraph that passes the filters is listed.');
  else add('pass','<strong>Query understood.</strong> '+esc(state.echo)+' ('+state.terms+' term'+(state.terms===1?'':'s')+').');

  const rendered=document.querySelectorAll('#rows article.row').length;
  const want=Math.min(state.shown,hits.length);
  const bsum=[...document.querySelectorAll('[data-cnt]')].reduce((s,e)=>s+(parseInt(e.textContent.replace(/\D/g,''),10)||0),0);
  const joint=hits.reduce((s,r)=>s+r.coms.length-1,0);
  add(rendered===want&&bsum===hits.length+joint?'pass':'fail','<strong>Totals.</strong> '+fmt(rendered)+' rows on screen and '+fmt(Math.max(0,hits.length-rendered))+' more behind “Show more” = '+fmt(hits.length)+' hits. The committee counts in brackets add up to '+fmt(bsum)+'; hits '+fmt(hits.length)+' + joint '+fmt(joint)+' = '+fmt(hits.length+joint)+'.');
  const bars=state.chartData.reduce((s,e)=>s+e[1],0);
  add(bars===hits.length+joint?'pass':'fail','<strong>Chart total.</strong> The bars add up to '+fmt(bars)+'; hits '+fmt(hits.length)+' + joint '+fmt(joint)+' = '+fmt(hits.length+joint)+'. (Joint = extra committees of joint General Comments.)');

  if(!state.hlRe) add('note','<strong>Highlight.</strong> Not applicable: '+(state.tree?'the query has only NOT terms, so there is nothing to mark.':'there are no search words.'));
  else{
    const miss=hits.filter(r=>r.mc===0);
    add(miss.length?'fail':'pass','<strong>Highlight.</strong> '+fmt(hits.length-miss.length)+' of '+fmt(hits.length)+' hits show at least one <mark>marked</mark> word.'+(miss.length?' Matched, not highlighted (still shown): '+pins(miss,8)+'.':''));
  }

  const nt=state.termList.filter(t=>/['-]/.test(t.v));
  if(nt.length){
    const only=hits.filter(r=>!evalNode(state.tree,rawOf(r)));
    add('note','<strong>Normalisation.</strong> The query holds a straight apostrophe or hyphen, so curly apostrophes and en or em dashes were matched too. '+fmt(only.length)+' of '+fmt(hits.length)+' hits contain only those forms'+(only.length?': '+pins(only,6):'')+'.');
  }else add('pass','<strong>Normalisation.</strong> The query holds no apostrophe or hyphen, so nothing was matched through normalisation.');

  const mm=hits.filter(r=>r.leading!==null&&r.leading!==r.paragraph);
  add(mm.length?'fail':'pass','<strong>Numbering: leading number.</strong> '+(mm.length?fmt(mm.length)+' hits begin with a number that differs from the record: '+mm.slice(0,6).map(r=>esc(r.cite)+' (text ‘'+r.leading+'.’, record '+r.paragraph+')').join('; ')+(mm.length>6?' and more':'')+'.':'Where a hit begins with its own number, it equals the record’s paragraph.'));
  const dd=hits.filter(r=>r.dup);
  add(dd.length?'fail':'pass','<strong>Numbering: shared pinpoints.</strong> '+(dd.length?fmt(dd.length)+' hits share a pinpoint with another record of the same document: '+pins(dd,6)+'.':'No hit shares its pinpoint with another record.'));
  const lt=hits.filter(r=>r.lettered);
  add(lt.length?'note':'pass','<strong>Numbering: lettered sub-paragraphs.</strong> '+(lt.length?fmt(lt.length)+' hits are lettered sub-paragraphs that the file numbers 1, 2, 3: '+pins(lt,6)+'.':'No hit is a lettered sub-paragraph.'));

  const mb=hits.filter(r=>r.markBad);
  add(mb.length?'fail':'pass','<strong>Footnote marks.</strong> '+(mb.length?'For '+fmt(mb.length)+' hits the marks removed differ from the count of [[fn: in the stored text, or putting them back does not restore it: '+pins(mb,6)+'.':'For all '+fmt(hits.length)+' hits the marks removed equal the count of [[fn: in the stored text, and putting them back restores the stored text exactly.'));

  if(!draft.length) add('note','<strong>Draft.</strong> Nothing in the draft yet, so nothing to compare.');
  else{
    const bad=draft.filter(d=>{const r=byKey.get(d.id);return !r||r.text!==d.text_as_stored;});
    add(bad.length?'fail':'pass','<strong>Draft.</strong> The stored text of each of the '+draft.length+' items was looked up again by its record id and compared with the saved copy. '+(bad.length?'Different or missing: '+bad.slice(0,6).map(d=>esc(d.citation)).join('; ')+'.':'All identical.'));
  }
  $('checks').innerHTML=out.join('');
}
function renderQuirks(){
  const L=[];
  const z=recs.filter(r=>r.paragraph===0);
  L.push(fmt(z.length)+' paragraphs have the number 0 (preambles); they are cited as “preamble”.'+(z.length?' Example: '+esc(z[0].cite)+'.':''));
  const sh=[...titleSyms].filter(e=>e[1].size>1).sort((a,b)=>b[1].size-a[1].size);
  L.push(fmt(sh.length)+' symbols hold more than one document, so their citation names the committee and the document.'+(sh.length?' Largest: '+esc(sh[0][0])+' ('+sh[0][1].size+' documents).':''));
  const jt=recs.filter(r=>r.joint);
  L.push(fmt(jt.length)+' records belong to joint General Comments (two symbols or two committees).'+(jt.length?' Example: '+esc(jt[0].symbol)+'.':''));
  const dp=[...citeCount].filter(e=>e[1]>1);
  L.push(fmt(dp.length)+' pinpoints occur on more than one record.'+(dp.length?' Example: '+esc(dp[0][0])+'.':''));
  const mm=recs.filter(r=>r.leading!==null&&r.leading!==r.paragraph);
  L.push(fmt(mm.length)+' records begin with a number that differs from their paragraph number.'+(mm.length?' Example: '+esc(mm[0].cite)+' (text begins ‘'+mm[0].leading+'.’).':''));
  const lt=recs.filter(r=>r.lettered);
  L.push(fmt(lt.length)+' records are lettered sub-paragraphs numbered by the file.'+(lt.length?' Example: '+esc(lt[0].cite)+' (file number '+lt[0].paragraph+').':''));
  const fm=recs.filter(r=>r.marks>0);
  L.push(fmt(fm.length)+' records carry footnote marks ('+fmt(fm.reduce((s,r)=>s+r.marks,0))+' marks in all); the page removes them for display and for matching.');
  $('quirks').innerHTML=L.map(t=>'<li>'+t+'</li>').join('');
}

/* ---------- copy, toast, draft ---------- */
function toast(label,str,fb){
  $('toast').hidden=false;
  $('tlabel').textContent=label;
  const s=$('tsent');
  s.textContent=str||'';
  s.hidden=!str||!!fb;
  $('tfb').hidden=!fb;
  if(fb){const ta=$('tta');ta.value=str;ta.focus();ta.select();}
  $('sr').textContent=label+(str?' '+str:'');
}
async function copyText(str,what){
  let ok=false;
  try{
    if(navigator.clipboard&&navigator.clipboard.writeText){await navigator.clipboard.writeText(str);ok=true;}
  }catch(e){ok=false;}
  if(ok) toast('Copied '+what+'. This exact text was sent to the clipboard:',str,false);
  else toast('The clipboard is blocked here. The text is in the box: press “Select and copy”.',str,true);
}
function download(name,mime,content){
  try{
    const blob=new Blob([content],{type:mime+';charset=utf-8'});
    const url=URL.createObjectURL(blob);
    const a=document.createElement('a');
    a.href=url;a.download=name;
    document.body.appendChild(a);a.click();a.remove();
    setTimeout(()=>URL.revokeObjectURL(url),2000);
    toast('Download started: '+name+' ('+draft.length+' item'+(draft.length===1?'':'s')+'). If nothing arrives, this window blocks downloads: use Copy all instead.','',false);
  }catch(e){toast('The download did not start. Use Copy all instead.','',false);}
}
const COLS=['citation','symbol','paragraph','pinpoint','committee','short_title','year','text_copied','text_as_stored','doc_url'];
function cell(v){return '"'+String(v==null?'':v).replace(/"/g,'""')+'"';}
function csvText(){
  return '﻿'+[COLS.map(cell).join(',')].concat(draft.map(d=>COLS.map(c=>cell(d[c])).join(','))).join('\r\n')+'\r\n';
}
function allText(){return draft.map(d=>d.quote+'\n'+d.citation).join('\n\n');}
function addDraft(r){
  if(draft.some(d=>d.id===r.key)){toast('Already in your draft:',r.cite,false);return;}
  draft.push({id:r.key,quote:r.quote,citation:r.cite,symbol:r.symbol,paragraph:r.paragraph,pinpoint:r.pin,committee:r.committee,short_title:r.short,year:r.year,text_copied:r.qtext,text_as_stored:r.text,doc_url:r.url});
  saveDraft();renderDraft();updateRow(r.i,'add');renderChecks();
  toast('Added to your draft:',r.cite,false);
}
function removeDraft(id){
  draft=draft.filter(d=>d.id!==id);
  saveDraft();renderDraft();
  const r=byKey.get(id);
  if(r&&$('rows').querySelector('article.row[data-i="'+r.i+'"]')) updateRow(r.i,null);
  renderChecks();
}
function renderDraft(){
  const n=draft.length;
  $('dtitle').textContent='Your draft ('+n+' quotation'+(n===1?'':'s')+')';
  $('dstore').textContent=storeOK?'Kept in this browser (localStorage), so it is still here after a reload.':'Kept in memory only: this window does not allow localStorage, so the draft is lost when the page closes. Download it before you leave.';
  $('dempty').hidden=n>0;
  ['dcopy','dtxt','dcsv'].forEach(id=>{$(id).disabled=n===0;});
  const ol=$('ditems');
  ol.innerHTML='';
  draft.forEach(d=>{
    const r=byKey.get(d.id);
    const li=document.createElement('li');
    const q=document.createElement('div');q.className='dq';q.textContent=d.quote;
    const c=document.createElement('div');c.className='dc';c.textContent=d.citation;
    li.append(q,c);
    if(!r||r.text!==d.text_as_stored){
      const w=document.createElement('div');w.className='note';
      w.textContent='check failed: the stored text of this record is not the text saved here';
      li.appendChild(w);
    }
    const rm=document.createElement('button');
    rm.type='button';rm.className='lnk';rm.textContent='Remove';
    rm.setAttribute('aria-label','Remove '+d.citation+' from the draft');
    rm.addEventListener('click',()=>removeDraft(d.id));
    li.appendChild(rm);
    ol.appendChild(li);
  });
}

/* ---------- filters and wiring ---------- */
function syncChecks(){$('coms').querySelectorAll('input').forEach(i=>{i.checked=state.sel.has(i.value);});}
function buildFilters(){
  const box=$('coms');
  allCom.forEach(c=>{
    const lab=document.createElement('label');lab.className='cb';
    const inp=document.createElement('input');inp.type='checkbox';inp.value=c;inp.checked=true;
    const a=document.createElement('strong');a.textContent=c;
    const b=document.createElement('span');b.className='grey';b.textContent=' '+(CN[c]||'');
    const n=document.createElement('span');n.setAttribute('data-cnt',c);
    lab.append(inp,a,b,' ',n);
    inp.addEventListener('change',()=>{
      state.sel=new Set([...box.querySelectorAll('input:checked')].map(i=>i.value));
      state.shown=PAGE;refresh();
    });
    box.appendChild(lab);
  });
  $('all').addEventListener('click',()=>{state.sel=new Set(allCom);syncChecks();state.shown=PAGE;refresh();});
  $('none').addEventListener('click',()=>{state.sel=new Set();syncChecks();state.shown=PAGE;refresh();});
  const yf=$('yf'),yt=$('yt');
  yf.min=yt.min=minY;yf.max=yt.max=maxY;yf.value=minY;yt.value=maxY;
  yf.addEventListener('change',()=>{const v=parseInt(yf.value,10);state.yf=Number.isFinite(v)?v:minY;if(!Number.isFinite(v)) yf.value=minY;state.shown=PAGE;refresh();});
  yt.addEventListener('change',()=>{const v=parseInt(yt.value,10);state.yt=Number.isFinite(v)?v:maxY;if(!Number.isFinite(v)) yt.value=maxY;state.shown=PAGE;refresh();});
  const sel=$('doc');
  const o0=document.createElement('option');o0.value='';o0.textContent='All documents ('+fmt(titles.length)+')';sel.appendChild(o0);
  const groups=new Map();
  recs.forEach(r=>{
    if(!groups.has(r.committee)) groups.set(r.committee,new Map());
    if(!groups.get(r.committee).has(r.title)) groups.get(r.committee).set(r.title,r.short);
  });
  [...groups.keys()].sort().forEach(c=>{
    const og=document.createElement('optgroup');
    og.label=(c||'unknown')+(CN[c]?' · '+CN[c]:'');
    [...groups.get(c)].sort((a,b)=>coll.compare(a[1],b[1])).forEach(e=>{
      const o=document.createElement('option');o.value=e[0];o.textContent=e[1];og.appendChild(o);
    });
    sel.appendChild(og);
  });
  sel.addEventListener('change',()=>{state.doc=sel.value;state.shown=PAGE;refresh();});
  $('sort').addEventListener('change',()=>{state.sort=$('sort').value;state.shown=PAGE;refresh();});
}
function buildHeader(){
  const nT=new Set(recs.map(r=>r.title)).size,nC=new Set(recs.map(r=>r.committee)).size;
  const su=safeUrl(D.source_url),sn=D.source||D.source_url||'not stated in the file';
  const src=su?'<a href="'+esc(su)+'" target="_blank" rel="noopener">'+esc(sn)+'</a>':esc(sn);
  $('desc').innerHTML=fmt(recs.length)+' paragraphs from '+fmt(nT)+' General Comments of '+nC+' committees, '+(yrs.length?minY+'–'+maxY:'years not stated')+'. Source: '+src+'.';
  $('foot').innerHTML='Source: '+src+'. Built: '+esc(D.built||'date not stated in the file')+'.';
  ['"best interests" AND child','(torture OR ill-treatment) NOT detention','"reasonable accommodation"'].forEach(q=>{
    const b=document.createElement('button');
    b.type='button';b.className='btn ex';b.textContent=q;
    b.addEventListener('click',()=>{$('q').value=q;runSearch();});
    $('examples').appendChild(b);
  });
}
function toggle(set,k){if(set.has(k)) set.delete(k);else set.add(k);}

$('sform').addEventListener('submit',e=>{e.preventDefault();runSearch();});
$('rows').addEventListener('click',e=>{
  const b=e.target.closest('button[data-act]');
  if(!b||b.disabled) return;
  const art=b.closest('article.row');
  const r=recs[parseInt(art.getAttribute('data-i'),10)];
  const act=b.getAttribute('data-act');
  if(act==='cite') copyText(r.cite,'citation');
  else if(act==='quote') copyText(r.quote+' '+r.cite,'quotation');
  else if(act==='add') addDraft(r);
  else{
    if(act==='stored') toggle(state.stored,r.i);
    else if(act==='full') toggle(state.expanded,r.i);
    else if(act==='prev'||act==='next'){
      const c=Object.assign({},state.ctx.get(r.i)),k=act==='prev'?'p':'n';
      c[k]=!c[k];state.ctx.set(r.i,c);
    }
    updateRow(r.i,act);
  }
});
$('morebtn').addEventListener('click',()=>{
  const a=Math.min(state.shown,state.hits.length);
  state.shown+=PAGE;
  appendRows(a,Math.min(state.shown,state.hits.length));
  updateMore();renderChecks();
  const first=$('rows').children[a];
  if(first) first.focus();
});
$('dcopy').addEventListener('click',()=>copyText(allText(),'all '+draft.length+' quotations'));
$('dtxt').addEventListener('click',()=>download('draft-quotations.txt','text/plain',allText()+'\n'));
$('dcsv').addEventListener('click',()=>download('draft-quotations.csv','text/csv',csvText()));
$('tclose').addEventListener('click',()=>{$('toast').hidden=true;});
$('tsel').addEventListener('click',()=>{
  const ta=$('tta');ta.focus();ta.select();
  let ok=false;
  try{ok=document.execCommand('copy');}catch(e){ok=false;}
  $('tlabel').textContent=ok?'Copied from the box.':'Selected: press Ctrl+C (Cmd+C on a Mac) to copy.';
});

buildHeader();
buildFilters();
renderQuirks();
renderDraft();
$('q').focus();
runSearch();
})();
</script>
</body>
</html>
```
