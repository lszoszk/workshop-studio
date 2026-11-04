I built the verbatim finder on the General Comments file, following your plan: the four tabs, the Boolean search and the citation copy. The draft collector and the self-checks are in as well. I haven't run it against the full file, so the first thing to look at is tab 04: its checks run on your data and show a red dot if any fail.

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Verbatim finder: General Comments and General Recommendations</title>
<style>
:root{--bg:#f4f0e8;--ink:#1d1b18;--rule:#d9d2c3;--red:#9b2335;--mut:#5c564c;--ok:#1e6b3a;--amber:#7a4e00;--amberbg:#f8ecc9;--serif:Georgia,"Times New Roman",serif;--mono:ui-monospace,Menlo,Consolas,monospace}
*{box-sizing:border-box}
[hidden]{display:none!important}
body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.5 system-ui,-apple-system,"Segoe UI",Roboto,Arial,sans-serif}
.wrap{max-width:1200px;margin:0 auto;padding:0 20px}
a{color:var(--red)}
:focus-visible{outline:3px solid var(--red);outline-offset:2px}
.lab{font:11px/1.4 var(--mono);text-transform:uppercase;letter-spacing:.09em;color:var(--mut)}
.hint{font:12px/1.5 var(--mono);color:var(--mut);margin:6px 0}
h1{font:400 clamp(24px,3.2vw,34px)/1.15 var(--serif);margin:4px 0 6px}
.top{border-bottom:1px solid var(--rule);padding-top:16px}
.toprow{display:flex;justify-content:space-between;gap:16px;align-items:flex-start;flex-wrap:wrap}
.sub{margin:0 0 12px;font-size:14px;color:var(--mut)}
.health{font:12px var(--mono);white-space:nowrap;padding-top:6px}
.dot{display:inline-block;width:10px;height:10px;border-radius:50%;margin-right:6px;vertical-align:baseline}
.dot.ok{background:var(--ok)}.dot.bad{background:#c0182f}
.tabs{display:flex;gap:4px;flex-wrap:wrap}
.tabs button{background:none;border:0;border-bottom:3px solid transparent;padding:10px 14px;font:12px var(--mono);letter-spacing:.08em;text-transform:uppercase;color:var(--ink);cursor:pointer}
.tabs button[aria-selected="true"]{color:var(--red);border-bottom-color:var(--red);font-weight:700}
.layout{display:grid;grid-template-columns:310px minmax(0,1fr);gap:32px;padding-top:20px;padding-bottom:30px}
.layout.norail{grid-template-columns:minmax(0,1fr)}
#rail{border-right:1px solid var(--rule);padding-right:22px}
.railhead{display:flex;justify-content:space-between;align-items:baseline}
.bignum{font:400 56px/1 var(--serif);color:var(--ink);margin-top:10px}
.bigsub{font:14px var(--mono);color:var(--mut)}
.bigsub b{font:400 16px var(--serif);color:var(--ink)}
.chips{display:flex;flex-wrap:wrap;gap:6px;margin:10px 0 0}
.chip{border:1px solid var(--red);color:var(--red);background:transparent;border-radius:14px;padding:2px 10px;font:12px var(--mono);cursor:pointer}
.sbox{display:flex;gap:6px;margin-top:4px}
.sbox input{flex:1;min-width:0;font:inherit;padding:8px;border:1px solid var(--ink);background:#fff;color:var(--ink)}
.btn{border:1px solid var(--ink);background:transparent;color:var(--ink);padding:6px 12px;font:12px var(--mono);text-transform:uppercase;letter-spacing:.06em;cursor:pointer}
.btn:hover{background:#e9e3d6}
.btn.pri{background:var(--red);border-color:var(--red);color:#fff}
.btn:disabled{opacity:.45;cursor:default}
.link{background:none;border:0;color:var(--red);text-decoration:underline;padding:0;font:inherit;cursor:pointer}
.link.m{font:12px var(--mono)}
.syn{border:1px solid var(--rule);background:#fbf9f4;padding:8px 10px;margin-top:6px;font-size:14px}
.syn ul{margin:4px 0 8px;padding-left:18px}
.syn li{margin:2px 0}
.syn .ex{list-style:none;padding:0;margin:4px 0 0}
.syn .ex li{font:13px var(--mono);padding:5px 6px;border:1px solid var(--rule);margin:4px 0;cursor:pointer;background:#fff}
.syn .ex li:hover,.syn .ex li:focus{border-color:var(--red);outline:none;box-shadow:inset 3px 0 0 var(--red)}
.echo{font-size:14px;margin:6px 0;min-height:1em}
.err{color:#a1081f;font-size:14px;margin:6px 0;font-weight:600}
.facet{border-top:1px solid var(--rule);margin-top:14px;padding-top:6px}
.fh{margin:0;font-size:16px}
.fh button{width:100%;text-align:left;background:none;border:0;padding:8px 0;font:inherit;font-weight:600;cursor:pointer;color:var(--ink)}
.fh button[aria-expanded="true"]{color:var(--red)}
.fh .num{font:12px var(--mono);margin-right:8px;color:var(--red)}
fieldset{border:0;padding:0;margin:0 0 12px}
.cb{display:flex;gap:8px;align-items:flex-start;font-size:14px;margin:3px 0;line-height:1.3}
.cb input{accent-color:var(--red);margin-top:3px}
.cnt{font:12px var(--mono);color:var(--red)}
.yrs{display:flex;gap:10px;align-items:center;flex-wrap:wrap;margin:8px 0 12px}
.yrs input{width:84px;font:inherit;padding:4px;border:1px solid var(--ink);background:#fff}
select{font:inherit;padding:6px;border:1px solid var(--ink);background:#fff;color:var(--ink);max-width:100%}
.fig .figlab{font:11px var(--mono);letter-spacing:.09em;color:var(--red)}
.figt{font:400 24px var(--serif);margin:2px 0 4px}
.figrow{display:flex;gap:28px;flex-wrap:wrap;align-items:flex-start;margin-top:10px}
.chartwrap{flex:1 1 380px;min-width:280px;position:relative}
table{border-collapse:collapse;font-size:14px}
caption{text-align:left;font:11px var(--mono);letter-spacing:.08em;text-transform:uppercase;color:var(--mut);padding-bottom:4px}
th,td{padding:5px 10px;border-bottom:1px solid var(--rule);text-align:left;vertical-align:top}
th{font:11px var(--mono);text-transform:uppercase;letter-spacing:.06em;color:var(--mut)}
td.n,th.n{text-align:right;font-variant-numeric:tabular-nums}
.how{font:12px var(--mono);color:var(--mut);margin-top:12px;border-top:1px solid var(--rule);padding-top:8px}
.sum{font:400 22px/1.3 var(--serif);margin:0 0 6px}
.orderrow{display:flex;gap:10px;align-items:center;flex-wrap:wrap;margin-bottom:4px}
.row{border-top:1px solid var(--rule);padding:12px 0}
.rh{margin:0;font-size:16px}
.rt{background:none;border:0;padding:0;font:inherit;font-weight:600;text-align:left;cursor:pointer;color:var(--ink)}
.rt:hover span{text-decoration:underline}
.badge{font:11px var(--mono);border:1px solid var(--ink);padding:1px 6px;letter-spacing:.06em;margin-right:4px;display:inline-block;font-weight:400}
.meta{font:12px var(--mono);color:var(--mut);margin:3px 0 6px}
.pin{color:var(--red);font-weight:700}
.txt{white-space:pre-wrap;margin:4px 0;overflow-wrap:anywhere}
mark{background:#fff2a8;color:var(--ink);font-weight:700;padding:0 1px}
.fnl{font:12px var(--mono);color:var(--mut);margin:2px 0}
.note{background:var(--amberbg);color:var(--amber);font-size:13px;padding:3px 8px;margin:4px 0;border-left:3px solid #c98a00}
.row.open{background:#efe9dc;margin:0 -10px;padding:12px 10px}
.acts{display:flex;gap:8px;flex-wrap:wrap;align-items:center;margin:10px 0 4px}
.ctx{background:#e6dfd0;color:#3d3830;padding:6px 10px;margin:6px 0;font-size:15px}
.st{font:700 12px var(--mono);text-transform:uppercase;padding:1px 6px;border:1px solid}
.st.ok{color:var(--ok)}.st.bad{color:#a1081f}
#checks{padding-left:0;list-style:none}
#checks>li{border-top:1px solid var(--rule);padding:8px 0}
.ex2{font:12px var(--mono);color:var(--mut);margin:4px 0 0;padding-left:18px}
.dq{list-style:none;padding:0}
.dq>li{border-top:1px solid var(--rule);padding:10px 0}
.dq .cit{font:13px var(--mono);color:var(--red);font-weight:700}
footer{border-top:1px solid var(--rule);padding:12px 0 28px;font:11px/1.6 var(--mono);color:var(--mut)}
#cbox{position:fixed;right:14px;bottom:14px;max-width:min(520px,calc(100vw - 28px));max-height:40vh;overflow:auto;background:#fff;border:1px solid var(--ink);padding:10px;z-index:20;font-size:14px}
#cbox pre{white-space:pre-wrap;margin:6px 0;font:13px var(--mono)}
#cbox textarea{width:100%;height:90px;font:13px var(--mono)}
.sr{position:absolute;left:-9999px;width:1px;height:1px;overflow:hidden}
.empty{padding:18px 0;color:var(--mut)}
@media(max-width:860px){.layout{grid-template-columns:1fr}#rail{border-right:0;padding-right:0;border-bottom:1px solid var(--rule);padding-bottom:16px}}
</style>
</head>
<body>
<header class="top"><div class="wrap">
  <div class="toprow">
    <div>
      <div class="lab">UN TREATY BODIES · GENERAL COMMENTS</div>
      <h1>Verbatim finder: General Comments and General Recommendations</h1>
      <p class="sub" id="srcline"></p>
    </div>
    <div class="health" id="health" role="status"></div>
  </div>
  <div class="tabs" role="tablist" aria-label="Views" id="tabs">
    <button role="tab" id="tab1" aria-controls="p1" aria-selected="true" data-tab="1">01 OVERVIEW</button>
    <button role="tab" id="tab2" aria-controls="p2" aria-selected="false" tabindex="-1" data-tab="2">02 PARAGRAPHS</button>
    <button role="tab" id="tab3" aria-controls="p3" aria-selected="false" tabindex="-1" data-tab="3">03 DRAFT (0)</button>
    <button role="tab" id="tab4" aria-controls="p4" aria-selected="false" tabindex="-1" data-tab="4">04 CHECK &amp; METHOD</button>
  </div>
</div></header>

<div class="wrap layout" id="layout">
  <aside id="rail" aria-label="Filters">
    <div class="railhead"><span class="lab">FILTERS</span><button class="link m" id="clearAll">Clear all</button></div>
    <div aria-live="polite"><div class="bignum" id="bigN">0</div><div class="bigsub"><b>matching paragraphs</b> · <span id="bigOf"></span></div></div>
    <div class="chips" id="chips"></div>
    <div style="margin-top:16px" id="swrap">
      <label for="q" class="lab">SEARCH THE TEXT</label>
      <div class="sbox">
        <input id="q" type="text" role="combobox" aria-expanded="false" aria-haspopup="listbox" aria-controls="exlist" aria-autocomplete="none" autocomplete="off" spellcheck="false" aria-describedby="qhelp qecho qerr">
        <button class="btn pri" id="go" type="button">Search</button>
      </div>
      <div class="syn" id="syn" hidden>
        <ul>
          <li>A space or <b>AND</b> joins words: all must appear.</li>
          <li><b>OR</b> accepts either word.</li>
          <li><b>NOT</b>, or a minus sign in front, leaves a word out.</li>
          <li>Put an <b>“exact phrase”</b> in double quotes.</li>
          <li>Parentheses group parts together.</li>
          <li>A star ends a word openly: child* finds children.</li>
          <li>Operators need capitals; lower-case “or” is just a word.</li>
        </ul>
        <span class="lab">TRY ONE (click = run)</span>
        <ul class="ex" id="exlist" role="listbox" aria-label="Example searches">
          <li role="option" tabindex="-1" data-q="&quot;best interests&quot; AND child">"best interests" AND child</li>
          <li role="option" tabindex="-1" data-q="(torture OR ill-treatment) NOT detention">(torture OR ill-treatment) NOT detention</li>
          <li role="option" tabindex="-1" data-q="&quot;reasonable accommodation&quot;">"reasonable accommodation"</li>
        </ul>
      </div>
      <p class="hint" id="qhelp">Whole words, any case. Curly and straight quotes, apostrophes, dashes and hyphens count as the same, and footnote marks are skipped, so State's finds State’s and a phrase can cross a footnote.</p>
      <p class="echo" id="qecho" aria-live="polite"></p>
      <p class="err" id="qerr" role="alert" hidden></p>
    </div>
    <div class="facet">
      <h2 class="fh"><button type="button" id="fbtn" aria-expanded="false" aria-controls="fbody"><span class="num">01</span>Committee, years, document</button></h2>
      <div id="fbody" hidden>
        <fieldset><legend class="lab">COMMITTEE · <button class="link m" type="button" id="cAll">all</button> / <button class="link m" type="button" id="cNone">none</button></legend>
          <div id="clist"></div></fieldset>
        <div class="yrs"><span class="lab">YEARS</span>
          <label>from <input id="yf" type="number"></label><label>to <input id="yt" type="number"></label></div>
        <label class="lab" for="dsel">DOCUMENT</label><br>
        <select id="dsel"></select>
      </div>
    </div>
  </aside>

  <main>
    <section id="p1" role="tabpanel" aria-labelledby="tab1">
      <div class="fig">
        <div class="figlab">FIG.01</div>
        <h2 class="figt">Paragraphs per committee</h2>
        <p id="ovsum" style="margin:2px 0 4px"></p>
        <p class="hint">click a bar = tick that committee alone · grey bars = committees not ticked</p>
        <div class="figrow">
          <div class="chartwrap" id="cwrap"><canvas id="cv" role="img" aria-label="Paragraphs per committee">Paragraphs per committee: see the table beside this chart.</canvas></div>
          <table id="ctab"></table>
        </div>
        <p class="hint">Joint General Comments count under both committees, so the bars can add up to more than the hits.</p>
        <p class="how">How this is computed: one count per committee over the paragraphs that match the query and filters.</p>
      </div>
    </section>

    <section id="p2" role="tabpanel" aria-labelledby="tab2" hidden>
      <p class="sum" id="psum" aria-live="polite"></p>
      <div class="orderrow"><span id="pord" class="hint" style="margin:0"></span>
        <label for="ord" class="lab">ORDER</label>
        <select id="ord"><option value="new">newest first</option><option value="doc">document order</option><option value="most">most matches first</option></select></div>
      <p class="hint">This page retrieves; it never writes. Every paragraph shown is a record of the file, as stored.</p>
      <div id="plist"></div>
      <p><button class="btn" id="more" type="button">Show 25 more</button></p>
    </section>

    <section id="p3" role="tabpanel" aria-labelledby="tab3" hidden>
      <h2 class="figt" id="dhead">Your draft (0 quotations)</h2>
      <div class="acts">
        <button class="btn pri" id="dCopy" type="button">Copy all</button>
        <button class="btn" id="dTxt" type="button">Download .txt</button>
        <button class="btn" id="dCsv" type="button">Download .csv</button>
      </div>
      <p class="hint" id="dstore"></p>
      <p class="hint" id="dmsg" aria-live="polite"></p>
      <ol class="dq" id="dlist"></ol>
    </section>

    <section id="p4" role="tabpanel" aria-labelledby="tab4" hidden>
      <h2 class="figt">Checks the app runs on itself</h2>
      <p class="hint">Each line compares two numbers or two texts. A failed check marks rows; it never drops them.</p>
      <ol id="checks"></ol>
      <h2 class="figt" style="margin-top:26px">Known quirks of this file</h2>
      <div id="quirks"></div>
      <h2 class="figt" style="margin-top:26px">How this is computed</h2>
      <div id="method"></div>
    </section>
  </main>
</div>

<footer><div class="wrap">
  <div id="foot1"></div>
  <div>Counting, matching and sorting are done by this page's code; no model is called and nothing leaves the browser.</div>
  <div>Credits: charts drawn with Chart.js (MIT licence).</div>
</div></footer>

<div id="cbox" hidden>
  <div id="cmsg" class="lab"></div>
  <pre id="cstr"></pre>
  <textarea id="cta" readonly hidden aria-label="Text to copy"></textarea>
  <div class="acts"><button class="btn" id="csel" type="button" hidden>Select and copy</button><button class="btn" id="cclose" type="button">Close</button></div>
</div>
<div class="sr" id="live" aria-live="polite"></div>

<script>
(function(){
'use strict';
const $=id=>document.getElementById(id);
const esc=s=>String(s==null?'':s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const fmt=n=>Number(n).toLocaleString('en-GB');
const FN=/\[\[fn:\d+\]\]/g;
const safeUrl=u=>/^https?:\/\//i.test(u||'')?u:'';
const D=window.WORKSHOP_DATA||{};
const GC=D.gc||{};
const R=Array.isArray(GC.records)?GC.records:[];
if(!R.length){document.body.innerHTML='<p style="padding:24px;font-family:Georgia,serif">The General Comments file is not attached to this conversation. Drag it from “Your files” into the chat.</p>';return;}

/* ---------- names, normalising ---------- */
const NAMES={CAT:'Committee against Torture','CAT-OP':'Subcommittee on Prevention of Torture',CCPR:'Human Rights Committee',CED:'Committee on Enforced Disappearances',CEDAW:'Committee on the Elimination of Discrimination against Women',CERD:'Committee on the Elimination of Racial Discrimination',CESCR:'Committee on Economic, Social and Cultural Rights',CMW:'Committee on Migrant Workers',CRC:'Committee on the Rights of the Child',CRPD:'Committee on the Rights of Persons with Disabilities'};
const collator=new Intl.Collator('en',{numeric:true});
function normText(s){return String(s).replace(/[\u201c\u201d\u201e]/g,'"').replace(/[\u2018\u2019\u201a]/g,"'").replace(/[\u2013\u2014\u00ad]/g,'-').replace(/\s+/g,' ').trim().toLowerCase();}
function strip(text){const marks=[];let clean='',last=0,m;const re=/\[\[fn:\d+\]\]/g;while((m=re.exec(text))){clean+=text.slice(last,m.index);marks.push({at:clean.length,s:m[0]});last=m.index+m[0].length;}clean+=text.slice(last);return{clean,marks};}
function rebuild(clean,marks){let out='',last=0;for(const k of marks){out+=clean.slice(last,k.at)+k.s;last=k.at;}return out+clean.slice(last);}
function docName(t){const m=/^(.*?)(:| on )/.exec(t);return(m?m[1]:t).trim();}

/* ---------- load: one pass over the records ---------- */
const CODE=/\b(CAT-OP|CAT|CCPR|CED|CEDAW|CERD|CESCR|CMW|CRC|CRPD)\b/g;
const recs=R.map((r,i)=>{
  const text=String(r.text==null?'':r.text),cl=text.replace(FN,'');
  const lm=/^(\d{1,3})\.\s/.exec(text),lab=/^\(([a-z]{1,4})\)/.exec(cl.trim());
  const sym=String(r.symbol||''),title=String(r.title||''),para=Number(r.paragraph);
  const cs=[];const add=c=>{if(c&&cs.indexOf(c)<0)cs.push(c);};
  add(r.committee);(sym.replace(/CAT\/OP/g,'CAT-OP').match(CODE)||[]).forEach(add);
  return{i,key:r.id!=null?String(r.id):'i'+i,symbol:sym,title,short:String(r.short_title||title),committee:String(r.committee||''),year:Number(r.year),para,text,clean:cl,norm:normText(cl),
    marks:(text.match(FN)||[]).length,leading:lm?+lm[1]:null,lettered:lab?lab[1]:null,
    pin:lab?'subpara. ('+lab[1]+')':(para===0?'preamble':'para. '+(isNaN(para)?'?':para)),
    cs,url:String(r.doc_url||''),words:cl.split(/\s+/).filter(Boolean).length,shared:false,dup:1,joint:cs.length>1,cite:'',qtext:'',quote:'',tpos:0};
});
const symTitles=new Map(),dupMap=new Map(),byTitle=new Map(),byKey=new Map();
recs.forEach(r=>{
  if(!symTitles.has(r.symbol))symTitles.set(r.symbol,new Set());symTitles.get(r.symbol).add(r.title);
  const k=r.title+'|'+r.para+'|'+(r.lettered||'');dupMap.set(k,(dupMap.get(k)||0)+1);
  if(!byTitle.has(r.title))byTitle.set(r.title,[]);r.tpos=byTitle.get(r.title).length;byTitle.get(r.title).push(r);
  byKey.set(r.key,r);
});
recs.forEach(r=>{
  r.shared=symTitles.get(r.symbol).size>1;
  r.dup=dupMap.get(r.title+'|'+r.para+'|'+(r.lettered||''));
  r.cite=r.shared?(r.committee+', '+docName(r.title)+' ('+r.symbol+'), '+r.pin):(r.symbol+', '+r.pin);
  r.qtext=((r.leading!==null&&r.leading===r.para)?r.clean.replace(/^\d{1,3}\.\s+/,''):r.clean).trim();
  r.quote='\u201c'+r.qtext+'\u201d '+r.cite;
});
const total=recs.length;
const titles=new Set(recs.map(r=>r.title));
const cc={};recs.forEach(r=>r.cs.forEach(c=>cc[c]=(cc[c]||0)+1));
const codes=Object.keys(cc).sort((a,b)=>cc[b]-cc[a]||a.localeCompare(b));
const yrs=recs.map(r=>r.year).filter(y=>!isNaN(y));
const yMin=yrs.length?Math.min.apply(null,yrs):0,yMax=yrs.length?Math.max.apply(null,yrs):0;

/* ---------- query parser ---------- */
const QUOTES='"\u201c\u201d\u201e';
const B1='(?<![\\p{L}\\p{N}])',B2='(?![\\p{L}\\p{N}])',GAP='(?:\\s|\\[\\[fn:\\d+\\]\\])+';
const esc2=s=>s.replace(/[.*+?^${}()|[\]\\]/g,'\\$&');
function hchar(c){if(c==="'")return"['\u2018\u2019\u201a]";if(c==='"')return'["\u201c\u201d\u201e]';if(c==='-')return'[\\-\u2013\u2014\u00ad]';return esc2(c);}
function mkTerm(kind,raw,star){
  const n=normText(raw);if(!n)return null;
  const words=n.split(' ');
  const k=(kind==='phrase'&&words.length>1)?'phrase':'word';
  const body=k==='phrase'?words.map(esc2).join('\\s+'):esc2(words[0])+(star?'[\\p{L}\\p{N}]*':'');
  const hb=k==='phrase'?words.map(w=>Array.from(w).map(hchar).join('')).join(GAP):Array.from(words[0]).map(hchar).join('')+(star?'[\\p{L}\\p{N}]*':'');
  return{k:'term',kind:k,raw:kind==='phrase'?n:raw.replace(/\*+$/,''),n,words,star:!!star&&k==='word',body,hb,re:new RegExp(B1+'(?:'+body+')'+B2,'u')};
}
function parseQuery(q){
  const toks=[];let i=0;const n=q.length;
  while(i<n){
    const c=q[i];
    if(/\s/.test(c)){i++;continue;}
    if(c==='('||c===')'){toks.push({t:c});i++;continue;}
    if(QUOTES.indexOf(c)>=0){let j=i+1;while(j<n&&QUOTES.indexOf(q[j])<0)j++;
      if(j>=n)return{error:'A double quote is not closed. Close the exact phrase with a second double quote.'};
      toks.push({t:'phrase',v:q.slice(i+1,j)});i=j+1;continue;}
    if(c==='-'&&i+1<n&&!/\s/.test(q[i+1])){toks.push({t:'NOT'});i++;continue;}
    if(c==='-'){i++;continue;}
    let j=i;while(j<n&&!/[\s()]/.test(q[j])&&QUOTES.indexOf(q[j])<0)j++;
    const w=q.slice(i,j);i=j;
    if(w==='AND'||w==='OR'||w==='NOT')toks.push({t:w});
    else{const v=w.replace(/\*+$/,'');if(v)toks.push({t:'word',v,star:/\*$/.test(w)});}
  }
  if(!toks.length)return{error:'Type a word or an “exact phrase”.'};
  let p=0;const peek=()=>toks[p];
  function primary(){
    const t=toks[p];
    if(!t)throw new Error('The query ends where a word or phrase should come next.');
    if(t.t==='('){p++;const e=orE();if(!toks[p]||toks[p].t!==')')throw new Error('A parenthesis is not closed.');p++;return e;}
    if(t.t===')')throw new Error('A closing parenthesis has no opening one, or the parentheses are empty.');
    if(t.t==='word'||t.t==='phrase'){p++;const term=mkTerm(t.t,t.v,t.star);if(!term)throw new Error('An empty phrase cannot be searched.');return term;}
    throw new Error(t.t+' needs a word or phrase beside it.');
  }
  function notE(){const t=peek();if(t&&t.t==='NOT'){p++;return{k:'not',item:notE()};}return primary();}
  function andE(){const items=[notE()];for(;;){const t=peek();if(!t||t.t==='OR'||t.t===')')break;if(t.t==='AND')p++;items.push(notE());}return items.length===1?items[0]:{k:'and',items};}
  function orE(){const items=[andE()];while(peek()&&peek().t==='OR'){p++;items.push(andE());}return items.length===1?items[0]:{k:'or',items};}
  let tree;
  try{tree=orE();if(p<toks.length){if(toks[p].t===')')throw new Error('A closing parenthesis has no opening one.');throw new Error('The query is not complete near “'+toks[p].t+'”.');}}
  catch(e){return{error:e.message};}
  const terms=[],pos=[];
  (function walk(nd,neg){if(nd.k==='term'){terms.push(nd);if(!neg)pos.push(nd);}else if(nd.k==='not')walk(nd.item,!neg);else nd.items.forEach(x=>walk(x,neg));})(tree,false);
  const notOnly=pos.length===0&&terms.length>0;
  const dT=t=>t.kind==='phrase'?'the phrase \u201c'+t.raw+'\u201d':(t.star?'a word starting with '+t.raw:'the word '+t.raw);
  const dsc=(nd,wrapOr)=>{
    if(nd.k==='term')return dT(nd);
    if(nd.k==='not')return 'not '+dsc(nd.item,true);
    if(nd.k==='and')return nd.items.map(x=>dsc(x,true)).join(' and ');
    const s=nd.items.map(x=>dsc(x,false)).join(' or ');return wrapOr?'('+s+')':s;
  };
  const d=dsc(tree,false);
  const echo=notOnly?'Paragraphs that satisfy: '+d+'. Only exclusions, so every other paragraph matches and nothing can be highlighted.':'Paragraphs containing '+d;
  const bodies=pos.map(t=>t.hb).sort((a,b)=>b.length-a.length);
  const hre=bodies.length?new RegExp(B1+'(?:'+bodies.join('|')+')'+B2,'giu'):null;
  return{tree,echo,terms,pos,notOnly,hre};
}
function ev(nd,s){
  if(nd.k==='term')return nd.re.test(s);
  if(nd.k==='not')return!ev(nd.item,s);
  if(nd.k==='and')return nd.items.every(x=>ev(x,s));
  return nd.items.some(x=>ev(x,s));
}
function countMatches(re,txt){let c=0,m;re.lastIndex=0;while((m=re.exec(txt))){if(m[0]==='')re.lastIndex++;else c++;}return c;}
function hlc(txt){
  const re=S.parsed&&S.parsed.hre;if(!re)return{html:esc(txt),n:0};
  re.lastIndex=0;let out='',last=0,m,n=0;
  while((m=re.exec(txt))){if(m[0]===''){re.lastIndex++;continue;}out+=esc(txt.slice(last,m.index))+'<mark>'+esc(m[0])+'</mark>';last=m.index+m[0].length;n++;}
  return{html:out+esc(txt.slice(last)),n};
}

/* ---------- state ---------- */
const S={q:'',tab:1,ticked:new Set(codes),from:yMin,to:yMax,doc:'',order:'new',visible:25,rendered:0,open:new Set(),full:new Set(),stored:new Set(),ctx:{},
  parsed:{empty:true},base:[],hits:[],counts:{},sorted:null,sortedFor:'',checks:null,draft:[],chartRows:[]};
const KEY='gc-verbatim-draft-v1';let storeOK=false;
try{localStorage.setItem('__t','1');localStorage.removeItem('__t');storeOK=true;}catch(e){storeOK=false;}
if(storeOK){try{const d=JSON.parse(localStorage.getItem(KEY)||'[]');if(Array.isArray(d))S.draft=d.filter(x=>x&&x.id);}catch(e){}}
function saveDraft(){if(storeOK){try{localStorage.setItem(KEY,JSON.stringify(S.draft));}catch(e){storeOK=false;}}S.checks=null;}

function compute(){
  const q=S.q.trim();
  S.parsed=q?parseQuery(q):{empty:true};
  const P=S.parsed,base=[];
  if(!P.error){for(const r of recs){
    if(r.year<S.from||r.year>S.to)continue;
    if(S.doc&&r.title!==S.doc)continue;
    if(P.tree&&!ev(P.tree,r.norm))continue;
    base.push(r);}}
  S.base=base;S.hits=base.filter(r=>r.cs.some(c=>S.ticked.has(c)));
  S.counts={};codes.forEach(c=>S.counts[c]=0);base.forEach(r=>r.cs.forEach(c=>S.counts[c]=(S.counts[c]||0)+1));
  S.sorted=null;S.visible=25;S.checks=null;
}
const cmpNew=(a,b)=>(b.year-a.year)||collator.compare(a.title,b.title)||(a.para-b.para)||(a.i-b.i);
const cmpDoc=(a,b)=>collator.compare(a.title,b.title)||(a.para-b.para)||(a.i-b.i);
function getSorted(){
  if(S.sorted&&S.sortedFor===S.order)return S.sorted;
  const a=S.hits.slice();
  if(S.order==='doc')a.sort(cmpDoc);
  else if(S.order==='most'){const hre=S.parsed.hre,mc=new Map();if(hre)a.forEach(r=>mc.set(r.i,countMatches(hre,r.clean)));a.sort((x,y)=>((mc.get(y.i)||0)-(mc.get(x.i)||0))||cmpNew(x,y));}
  else a.sort(cmpNew);
  S.sorted=a;S.sortedFor=S.order;return a;
}

/* ---------- notes, badges, rows ---------- */
function noteFor(r){
  const n=[];
  if(r.leading!==null&&r.leading!==r.para)n.push('the text begins \u2018'+r.leading+'.\u2019 but the record is '+r.pin+': check the document');
  if(r.lettered)n.push('a lettered sub-paragraph, numbered '+r.para+' by the file: verify in the document');
  if(r.dup>1)n.push((r.dup===2?'two':r.dup)+' records share this pinpoint');
  if(r.joint)n.push('joint General Comment');
  return n;
}
const badges=r=>r.cs.map(c=>'<span class="badge">'+esc(c)+'</span>').join('');
const symLink=r=>{const u=safeUrl(r.url);return u?'<a href="'+esc(u)+'" target="_blank" rel="noopener">'+esc(r.symbol)+'</a>':esc(r.symbol);};
function cutText(s){
  let c=s.slice(0,700);const sp=Math.max(c.lastIndexOf(' '),c.lastIndexOf('\n'));if(sp>400)c=c.slice(0,sp);
  const lb=c.lastIndexOf('[[');if(lb>c.lastIndexOf(']]')&&lb>=0)c=c.slice(0,lb);
  return c.replace(/\s+$/,'')+' \u2026';
}
function inDraft(r){return S.draft.some(d=>d.id===r.key);}
function rowHTML(r){
  const open=S.open.has(r.i),st=S.stored.has(r.i),full=S.full.has(r.i);
  const shown=st?r.text:r.clean;
  let disp=shown,cutOn=false;
  if(shown.length>700&&!full){disp=cutText(shown);cutOn=true;}
  const h=hlc(disp);
  const further=cutOn&&S.parsed.hre&&h.n===0&&countMatches(S.parsed.hre,shown)>0;
  const cx=S.ctx[r.i]||{p:false,n:false};
  const ctxBlock=dir=>{
    const arr=byTitle.get(r.title),o=arr[r.tpos+dir];
    return'<div class="ctx"><span class="pin">'+(o?esc(o.pin):'')+'</span> <span class="lab">'+(dir<0?'previous':'next')+' paragraph of this document</span>'+(o?'<p class="txt">'+esc(o.clean)+'</p>':'<p class="hint">There is no '+(dir<0?'previous':'next')+' paragraph in this document.</p>')+'</div>';
  };
  let s='<article class="row'+(open?' open':'')+'" data-i="'+r.i+'">';
  s+='<h3 class="rh"><button type="button" class="rt" data-act="toggle" aria-expanded="'+open+'">'+badges(r)+'<span>'+esc(r.short)+'</span></button></h3>';
  s+='<p class="meta">'+symLink(r)+' · <span class="pin">'+esc(r.pin)+'</span> · '+esc(isNaN(r.year)?'year ?':r.year)+'</p>';
  if(open&&cx.p)s+=ctxBlock(-1);
  s+='<p class="txt">'+h.html+'</p>';
  if(cutOn)s+='<p class="fnl"><button type="button" class="link m" data-act="full">Show the full paragraph ('+fmt(r.words)+' words)</button>'+(further?' · the match is further down':'')+'</p>';
  else if(full&&shown.length>700)s+='<p class="fnl"><button type="button" class="link m" data-act="full">Show less</button></p>';
  if(r.marks>0)s+='<p class="fnl">'+(st?'Shown as stored, '+r.marks+' footnote mark'+(r.marks>1?'s':'')+' kept · ':r.marks+' footnote mark'+(r.marks>1?'s':'')+' removed · ')+'<button type="button" class="link m" data-act="stored">'+(st?'show as read in print':'show as stored')+'</button></p>';
  if(open&&cx.n)s+=ctxBlock(1);
  noteFor(r).forEach(t=>{s+='<div class="note">'+esc(t.charAt(0).toUpperCase()+t.slice(1))+'</div>';});
  if(open){
    s+='<div class="acts"><button type="button" class="btn" data-act="cite">Copy citation</button><button type="button" class="btn" data-act="quote">Copy quotation</button><button type="button" class="btn" data-act="add">'+(inDraft(r)?'Remove from draft':'Add to draft')+'</button>'
      +'<span class="lab">Context: <button type="button" class="link m" data-act="prev" aria-pressed="'+!!cx.p+'">previous</button> | <button type="button" class="link m" data-act="next" aria-pressed="'+!!cx.n+'">next</button></span></div>';
    s+='<p class="hint">Citation: <b>'+esc(r.cite)+'</b> · style: UN short form · built only from this record\u2019s fields</p>';
  }
  return s+'</article>';
}

/* ---------- copy ---------- */
async function copyText(s){
  let ok=false;
  try{await navigator.clipboard.writeText(s);ok=true;}catch(e){ok=false;}
  $('cbox').hidden=false;$('cstr').textContent=s;
  $('cmsg').textContent=ok?'Copied to the clipboard. Exact text sent:':'The browser refused clipboard access. Select the text below and copy it with Ctrl+C:';
  $('cta').hidden=ok;$('csel').hidden=ok;if(!ok){$('cta').value=s;$('cstr').hidden=true;}else $('cstr').hidden=false;
  $('live').textContent=(ok?'Copied: ':'Not copied, select and copy: ')+s;
}
$('csel').onclick=()=>{const t=$('cta');t.focus();t.select();try{document.execCommand('copy');}catch(e){}};
$('cclose').onclick=()=>{$('cbox').hidden=true;};

/* ---------- draft ---------- */
function toggleDraft(r){
  const k=S.draft.findIndex(d=>d.id===r.key);
  if(k>=0)S.draft.splice(k,1);
  else S.draft.push({id:r.key,citation:r.cite,quote:'\u201c'+r.qtext+'\u201d',text_copied:r.qtext,text_as_stored:r.text});
  saveDraft();tabLabels();updateHealth();
}
function draftAll(){return S.draft.map(d=>d.quote+'\n'+d.citation).join('\n\n');}
function csvCell(v){return'"'+String(v==null?'':v).replace(/"/g,'""')+'"';}
function draftCsv(){
  const head=['citation','symbol','paragraph','pinpoint','committee','short_title','year','text_copied','text_as_stored','doc_url'];
  const rows=S.draft.map(d=>{const r=byKey.get(d.id)||{};return[d.citation,r.symbol,r.para,r.pin,r.committee,r.short,r.year,d.text_copied,d.text_as_stored,r.url];});
  return'\uFEFF'+[head].concat(rows).map(a=>a.map(csvCell).join(',')).join('\r\n');
}
function download(name,mime,content){
  try{const u=URL.createObjectURL(new Blob([content],{type:mime}));const a=document.createElement('a');a.href=u;a.download=name;document.body.appendChild(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(u),2000);$('dmsg').textContent='Download started: '+name+'. If nothing arrives, this preview blocks downloads: use Copy all.';}
  catch(e){$('dmsg').textContent='The download was blocked here. Use Copy all instead.';}
}
function renderDraft(){
  const n=S.draft.length;
  $('dhead').textContent='Your draft ('+n+' quotation'+(n===1?'':'s')+')';
  $('dstore').textContent=storeOK?'Kept in this browser (localStorage), so it survives a reload. Citations are built from the record fields, nothing is invented.':'Kept in memory only: it disappears when you close this page, because localStorage is not allowed here. Download or copy before leaving.';
  ['dCopy','dTxt','dCsv'].forEach(id=>$(id).disabled=!n);
  const bad=new Set(draftBad().map(d=>d.id));
  $('dlist').innerHTML=n?S.draft.map(d=>{const r=byKey.get(d.id);
    return'<li><p class="txt">'+esc(d.quote)+'</p><p class="cit">'+esc(d.citation)+'</p>'
    +(r?'<p class="meta">'+symLink(r)+' · '+esc(r.short)+' · '+esc(r.year)+'</p>':'')
    +(bad.has(d.id)?'<div class="note">The stored text of this record no longer equals the text saved in the draft: check it before you cite.</div>':'')
    +'<button type="button" class="btn" data-rm="'+esc(d.id)+'">Remove</button></li>';}).join(''):'<li class="empty">Nothing collected yet. Open a paragraph on tab 02 and press “Add to draft”.</li>';
}
function draftBad(){return S.draft.filter(d=>{const r=byKey.get(d.id);return!r||r.text!==d.text_as_stored;});}

/* ---------- checks ---------- */
function buildChecks(){
  const out=[],P=S.parsed,H=S.hits;
  const add=(name,ok,detail,extra)=>out.push({name,ok,detail,extra:extra||[]});
  if(P.error)add('Query understood',false,P.error);
  else if(P.empty)add('Query understood',true,'No search words: every paragraph that passes the filters is listed.');
  else add('Query understood',true,P.echo+' · '+P.terms.length+' term'+(P.terms.length===1?'':'s'));
  const sorted=getSorted();let rows=0;for(let k=0;k<sorted.length;k+=25)rows+=sorted.slice(k,k+25).length;
  const uniq=new Set(sorted.map(r=>r.i)).size;
  let extraJ=0;H.forEach(r=>{extraJ+=r.cs.filter(c=>S.ticked.has(c)).length-1;});
  const expect=H.length+extraJ;
  let bracket=0;document.querySelectorAll('#clist input').forEach(cb=>{if(cb.checked){const sp=cb.parentNode.querySelector('.cnt');bracket+=Number(sp.dataset.n)||0;}});
  add('Totals',rows===H.length&&uniq===H.length&&bracket===expect,'Rows across pages of 25: '+fmt(rows)+' · hits: '+fmt(H.length)+' · distinct rows: '+fmt(uniq)+' · committee counts in brackets add up to '+fmt(bracket)+' (hits '+fmt(H.length)+' + joint extras '+fmt(extraJ)+' = '+fmt(expect)+').');
  const cr=chartRowsNow();const bars=cr.filter(x=>x.on).reduce((a,x)=>a+x.n,0);
  add('Chart total',bars===expect,'The ticked bars add up to '+fmt(bars)+'; hits '+fmt(H.length)+' + joint hits counted twice '+fmt(extraJ)+' = '+fmt(expect)+'.');
  if(P.hre&&!P.notOnly){
    const miss=H.filter(r=>{P.hre.lastIndex=0;return!P.hre.test(r.clean);});
    add('Highlight',miss.length===0,miss.length?miss.length+' hit(s) matched but show no highlight (still listed): ':'Every one of the '+fmt(H.length)+' hits shows at least one highlighted match.',miss.slice(0,6).map(r=>r.cite));
  }else add('Highlight',true,P.notOnly?'The query holds only exclusions, so no highlight is expected.':'No search words, nothing to highlight.');
  const punct=(P.pos||[]).filter(t=>/['"\-]/.test(t.n));
  if(punct.length){
    const re=new RegExp(B1+'(?:'+punct.map(t=>t.body).join('|')+')'+B2,'iu');
    const only=H.filter(r=>!re.test(r.clean)).length;
    add('Normalisation',true,'The words typed hold a straight quote, apostrophe or hyphen, so curly quotes and en or em dashes were matched too. '+fmt(only)+' of '+fmt(H.length)+' hits contain only those forms.');
  }else add('Normalisation',true,'No straight quote, apostrophe or hyphen in the words typed, so no extra forms were needed.');
  const lead=H.filter(r=>r.leading!==null&&r.leading!==r.para),dups=H.filter(r=>r.dup>1),lets=H.filter(r=>r.lettered);
  const unflagged=lead.concat(dups,lets).filter(r=>!noteFor(r).length);
  add('Numbering',unflagged.length===0,fmt(lead.length)+' hit(s) with a leading number that differs from the record · '+fmt(dups.length)+' sharing a pinpoint · '+fmt(lets.length)+' lettered sub-paragraphs. Each carries an amber note on its row; none is corrected.',
    lead.slice(0,4).map(r=>r.cite+': text begins \u2018'+r.leading+'.\u2019, record says '+r.para).concat(dups.slice(0,3).map(r=>r.cite+': '+r.dup+' records'),lets.slice(0,3).map(r=>r.cite+': file number '+r.para)));
  const mb=H.filter(r=>{const s=strip(r.text);return s.marks.length!==r.marks||s.clean!==r.clean||rebuild(s.clean,s.marks)!==r.text||(r.text.split('[[fn:').length-1)!==r.marks;});
  const nm=H.reduce((a,r)=>a+r.marks,0);
  add('Marks',mb.length===0,'Footnote marks removed from the hits: '+fmt(nm)+'; each equals the count of “[[fn:” in the stored text, and putting them back gives the stored text exactly'+(mb.length?' (not so for '+mb.length+' hit(s))':'')+'.',mb.slice(0,6).map(r=>r.cite));
  const db=draftBad();
  add('Draft',db.length===0,S.draft.length?S.draft.length+' item(s): the stored text of each record was looked up again and compared with the saved text'+(db.length?'; '+db.length+' differ':'; all equal')+'.':'The draft is empty, nothing to compare.',db.slice(0,6).map(d=>d.citation));
  return out;
}
function getChecks(){if(!S.checks)S.checks=buildChecks();return S.checks;}
function updateHealth(){
  const ch=getChecks(),bad=ch.filter(c=>!c.ok).length,good=ch.length-bad;
  $('health').innerHTML='<span class="dot '+(bad?'bad':'ok')+'"></span>'+(bad?bad+' check'+(bad>1?'s':'')+' failed':good+' checks pass');
  $('tab4').innerHTML='04 CHECK &amp; METHOD'+(bad?' <span class="dot bad" style="margin:0 0 0 4px"></span>':'');
}
function tabLabels(){$('tab3').textContent='03 DRAFT ('+S.draft.length+')';}

/* ---------- rail ---------- */
function updateRail(){
  const P=S.parsed;
  $('bigN').textContent=fmt(S.hits.length);$('bigOf').textContent='of '+fmt(total);
  $('qecho').textContent=P.error?'':(P.echo||'');
  const er=$('qerr');er.hidden=!P.error;er.textContent=P.error||'';$('q').setAttribute('aria-invalid',P.error?'true':'false');
  const ch=[];
  if(S.ticked.size!==codes.length)ch.push(['c',S.ticked.size===0?'No committee ticked':'Committee: '+(S.ticked.size>3?S.ticked.size+' of '+codes.length:[...S.ticked].join(', '))]);
  if(S.from!==yMin||S.to!==yMax)ch.push(['y','Years '+S.from+'\u2013'+S.to]);
  if(S.doc){const r=byTitle.get(S.doc)[0];ch.push(['d','Document: '+r.short]);}
  $('chips').innerHTML=ch.map(c=>'<button type="button" class="chip" data-chip="'+c[0]+'" aria-label="Remove filter: '+esc(c[1])+'">'+esc(c[1])+' \u00d7</button>').join('');
  document.querySelectorAll('#clist input').forEach(cb=>{
    cb.checked=S.ticked.has(cb.value);const sp=cb.parentNode.querySelector('.cnt');
    const n=S.counts[cb.value]||0;sp.dataset.n=n;sp.textContent=' ['+fmt(n)+']';sp.hidden=!S.q.trim()||!!P.error;});
  $('yf').value=S.from;$('yt').value=S.to;$('dsel').value=S.doc;
}

/* ---------- overview ---------- */
let chart=null;
function chartRowsNow(){return codes.map(c=>({code:c,n:S.counts[c]||0,on:S.ticked.has(c)})).sort((a,b)=>b.n-a.n||a.code.localeCompare(b.code));}
const valueLabels={id:'valueLabels',afterDatasetsDraw(ch){const ctx=ch.ctx,meta=ch.getDatasetMeta(0);ctx.save();ctx.fillStyle='#1d1b18';ctx.font='12px ui-monospace,Menlo,Consolas,monospace';ctx.textBaseline='middle';meta.data.forEach((b,i)=>ctx.fillText(fmt(ch.data.datasets[0].data[i]),b.x+6,b.y));ctx.restore();}};
function tickOnly(code){if(S.ticked.size===1&&S.ticked.has(code))S.ticked=new Set(codes);else S.ticked=new Set([code]);compute();render();}
function renderOverview(){
  const rows=chartRowsNow();S.chartRows=rows;
  const H=S.hits.length;
  $('ovsum').textContent=H?('Most paragraphs: '+rows[0].code+' ('+fmt(rows[0].n)+') of '+fmt(H)+' matching.'):'No paragraph matches the query and filters.';
  $('cv').setAttribute('aria-label','Paragraphs per committee: '+rows.map(r=>r.code+' '+r.n).join(', ')+'.');
  $('cwrap').style.height=(rows.length*34+56)+'px';
  $('ctab').innerHTML='<caption>Paragraphs per committee (same numbers as the chart)</caption><thead><tr><th scope="col">Committee</th><th scope="col">Name</th><th scope="col" class="n">Paragraphs</th></tr></thead><tbody>'+rows.map(r=>'<tr><td><b>'+esc(r.code)+'</b></td><td>'+esc(NAMES[r.code]||'')+(r.on?'':' <span class="hint">(not ticked)</span>')+'</td><td class="n">'+fmt(r.n)+'</td></tr>').join('')+'</tbody>';
  if(!window.Chart)return;
  const labels=rows.map(r=>r.code),data=rows.map(r=>r.n),cols=rows.map(r=>r.on?'#9b2335':'#cdbfa9');
  if(!chart){
    chart=new Chart($('cv'),{type:'bar',data:{labels,datasets:[{data,backgroundColor:cols,barPercentage:.7,categoryPercentage:.85}]},plugins:[valueLabels],
      options:{indexAxis:'y',animation:false,responsive:true,maintainAspectRatio:false,layout:{padding:{right:56}},
        plugins:{legend:{display:false},tooltip:{callbacks:{label:c=>fmt(c.parsed.x)+' paragraphs'}}},
        scales:{x:{beginAtZero:true,grid:{color:'#e6e0d2'},ticks:{maxTicksLimit:8,precision:0,color:'#5c564c'}},y:{grid:{display:false},ticks:{autoSkip:false,color:'#1d1b18',font:{family:'ui-monospace,Menlo,Consolas,monospace',size:12}}}},
        onClick:(e,els)=>{if(els.length)tickOnly(S.chartRows[els[0].index].code);},
        onHover:(e,els)=>{if(e.native&&e.native.target)e.native.target.style.cursor=els.length?'pointer':'default';}}});
  }else{chart.data.labels=labels;chart.data.datasets[0].data=data;chart.data.datasets[0].backgroundColor=cols;chart.update('none');}
}

/* ---------- paragraphs ---------- */
const ORDERTXT={new:'sorted by year, newest first, then by document and paragraph',doc:'in document order: by document title, then paragraph',most:'most matches first, then newest first'};
function renderParas(){
  const H=S.hits,P=S.parsed;
  const comm=new Set();H.forEach(r=>r.cs.forEach(c=>comm.add(c)));
  const ys=H.map(r=>r.year).filter(y=>!isNaN(y));
  let s=fmt(H.length)+' of '+fmt(total)+' paragraphs match';
  if(H.length)s+=' \u00b7 '+comm.size+' committee'+(comm.size===1?'':'s')+' \u00b7 '+Math.min.apply(null,ys)+'\u2013'+Math.max.apply(null,ys);
  if(P.empty)s+=' \u00b7 no search words';
  $('psum').textContent=s;
  $('pord').textContent=ORDERTXT[S.order]+(S.order==='most'&&!S.parsed.hre?' (no highlighted words, so all tie)':'');
  const list=getSorted();
  $('plist').innerHTML=list.length?list.slice(0,S.visible).map(rowHTML).join(''):'<p class="empty">'+(P.error?esc(P.error):'No paragraph matches. Try fewer words, or end a word with a star (child* finds children).')+'</p>';
  S.rendered=Math.min(S.visible,list.length);updateMore();
}
function updateMore(){const left=S.hits.length-S.rendered;$('more').hidden=left<=0;$('more').textContent='Show '+Math.min(25,left)+' more ('+fmt(left)+' left)';}
$('more').onclick=()=>{
  const list=getSorted(),from=S.rendered;S.visible=from+25;
  $('plist').insertAdjacentHTML('beforeend',list.slice(from,S.visible).map(rowHTML).join(''));
  S.rendered=Math.min(S.visible,list.length);updateMore();
};
function refreshRow(r,focus){
  const el=$('plist').querySelector('[data-i="'+r.i+'"]');if(!el)return;
  el.outerHTML=rowHTML(r);
  if(focus){const b=$('plist').querySelector('[data-i="'+r.i+'"] [data-act="'+focus+'"]');if(b)b.focus();}
}
function doAct(act,r,fromBtn){
  if(act==='toggle'){S.open.has(r.i)?S.open.delete(r.i):S.open.add(r.i);refreshRow(r,fromBtn?'toggle':null);}
  else if(act==='cite')copyText(r.cite);
  else if(act==='quote')copyText(r.quote);
  else if(act==='add'){toggleDraft(r);refreshRow(r,'add');}
  else if(act==='prev'||act==='next'){const c=S.ctx[r.i]||(S.ctx[r.i]={p:false,n:false});const k=act==='prev'?'p':'n';c[k]=!c[k];refreshRow(r,act);}
  else if(act==='full'){S.full.has(r.i)?S.full.delete(r.i):S.full.add(r.i);refreshRow(r,'full');}
  else if(act==='stored'){S.stored.has(r.i)?S.stored.delete(r.i):S.stored.add(r.i);refreshRow(r,'stored');}
}
$('plist').addEventListener('click',e=>{
  const art=e.target.closest('article.row');if(!art||e.target.closest('a'))return;
  const r=recs[+art.dataset.i],b=e.target.closest('[data-act]');
  if(b){doAct(b.dataset.act,r,true);return;}
  if(e.target.closest('.ctx')||String(window.getSelection()).length)return;
  doAct('toggle',r,false);
});
$('ord').onchange=e=>{S.order=e.target.value;S.sorted=null;S.visible=25;renderParas();};

/* ---------- check & method tab ---------- */
function renderCheck(){
  $('checks').innerHTML=getChecks().map(c=>'<li><span class="st '+(c.ok?'ok':'bad')+'">'+(c.ok?'pass':'check failed')+'</span> <strong>'+esc(c.name)+'.</strong> '+esc(c.detail)+(c.extra.length?'<ul class="ex2">'+c.extra.map(x=>'<li>'+esc(x)+'</li>').join('')+'</ul>':'')+'</li>').join('');
}
function buildStatic(){
  const q=[];
  const pre=recs.filter(r=>r.para===0);
  q.push(['Preambles filed as paragraph 0 (cited as \u201cpreamble\u201d, never \u201cpara. 0\u201d)',pre.length,pre[0]?pre[0].cite:'\u2014']);
  const sh=[...symTitles.entries()].filter(e=>e[1].size>1);
  q.push(['Symbols that hold more than one General Comment (the citation then carries committee and document number)',sh.length,sh[0]?sh[0][0]+' ('+sh[0][1].size+' documents)':'\u2014']);
  const jt=new Set(recs.filter(r=>r.joint).map(r=>r.symbol));
  q.push(['Joint General Comments (two committees in one symbol)',jt.size,[...jt][0]||'\u2014']);
  const dg=[...dupMap.entries()].filter(e=>e[1]>1);
  const dr=dg[0]?recs.find(r=>r.title+'|'+r.para+'|'+(r.lettered||'')===dg[0][0]):null;
  q.push(['Pinpoints that occur more than once in one document',dg.length,dr?dr.cite:'\u2014']);
  const lm=recs.filter(r=>r.leading!==null&&r.leading!==r.para);
  q.push(['Texts whose own number differs from the record\u2019s paragraph',lm.length,lm[0]?lm[0].cite+' (text begins \u2018'+lm[0].leading+'.\u2019)':'\u2014']);
  const lt=recs.filter(r=>r.lettered);
  q.push(['Lettered sub-paragraphs numbered by the file',lt.length,lt[0]?lt[0].cite+' (file number '+lt[0].para+')':'\u2014']);
  const fm=recs.filter(r=>r.marks>0);
  q.push(['Paragraphs with footnote marks written [[fn:N]]',fm.length,fm[0]?fm[0].cite+' ('+fm.reduce((a,r)=>a+r.marks,0)+' marks in all)':'\u2014']);
  $('quirks').innerHTML='<table><caption>Computed from the file when this page loaded</caption><thead><tr><th scope="col">Quirk</th><th scope="col" class="n">Count</th><th scope="col">Example</th></tr></thead><tbody>'+q.map(x=>'<tr><td>'+esc(x[0])+'</td><td class="n">'+fmt(x[1])+'</td><td>'+esc(x[2])+'</td></tr>').join('')+'</tbody></table>'
    +'<p class="hint">Older General Comments may be replaced by later ones (for example Human Rights Committee GC 36 replaced GC 6 and 14). The file has no \u201creplaced\u201d field, so the year is shown on every row.</p>';
  $('method').innerHTML='<ul>'
   +'<li><b>Matching.</b> Your query becomes a tree (NOT first, then AND, then OR; parentheses override). Each paragraph\u2019s text, with footnote marks removed, curly quotes and dashes unified and lower-cased, is tested against it. Whole words only: child does not find children, child* does.</li>'
   +'<li><b>Hits</b> are the paragraphs that match and pass the committee, year and document filters. A joint General Comment counts under each of its committees in the chart.</li>'
   +'<li><b>Shown and copied text</b> is the stored text minus the footnote marks. The leading number (\u201c12. \u201d) is left out of the copied quotation only when it equals the record\u2019s paragraph.</li>'
   +'<li><b>Citation</b> is symbol + pinpoint (UN short form). Preambles read \u201cpreamble\u201d, lettered records \u201csubpara. (b)\u201d. When a symbol holds several documents, committee and document number come first. Nothing is invented: every part comes from a field of the record.</li>'
   +'<li><b>Order</b> is year descending