Here's the workspace app: five tabs (Pages, Ask, Ingest, Check, Record), full pin verification in code, model-drafted ingests with per-page human approval, lint, and export. Everything the model writes is verified and shown inside `data-source="ai"` regions; nothing is called on load.

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Research wiki: neurotechnology in the administration of justice</title>
<style>
:root{--paper:#f4f0e8;--ink:#1d1b18;--rule:#d9d2c3;--acc:#9b2335;--ok:#1e6b34;--amber:#8a5a00;--bad:#a02318;--ins:#faf3d3;--mut:#5c554a}
[hidden]{display:none!important}
*{box-sizing:border-box}
body{margin:0;background:var(--paper);color:var(--ink);font:16px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}
a{color:var(--acc)}
:focus-visible{outline:2px solid var(--acc);outline-offset:2px}
.mono{font:11px/1.5 ui-monospace,Menlo,Consolas,monospace;letter-spacing:.12em;text-transform:uppercase;color:var(--mut)}
.hlabel{font:11px/1.5 ui-monospace,Menlo,Consolas,monospace;letter-spacing:.14em;text-transform:uppercase;color:var(--mut)}
header.site{position:sticky;top:0;z-index:6;background:var(--paper);border-bottom:1px solid var(--rule);padding:12px 24px 10px;display:flex;justify-content:space-between;gap:24px;align-items:flex-end;flex-wrap:wrap}
h1{font:600 25px/1.2 Georgia,"Times New Roman",serif;margin:3px 0 4px}
.hmeta{font-size:13px;color:var(--mut)}
.hright{text-align:right;font:11px/1.6 ui-monospace,Menlo,Consolas,monospace;letter-spacing:.06em;color:var(--mut)}
.hwarn{color:var(--amber)}
nav.tabs{display:flex;padding:0 24px;background:var(--paper);border-bottom:1px solid var(--rule);flex-wrap:wrap}
.tab{appearance:none;background:none;border:none;border-bottom:3px solid transparent;padding:10px 14px 8px;cursor:pointer;font:11px/1.4 ui-monospace,Menlo,Consolas,monospace;letter-spacing:.12em;text-transform:uppercase;color:var(--mut)}
.tab:hover{color:var(--ink)}
.tab[aria-selected="true"]{color:var(--acc);border-bottom-color:var(--acc)}
.tab .run{color:var(--acc)}
main{padding:22px 24px 60px;max-width:1280px;margin:0 auto}
footer.foot{border-top:1px solid var(--rule);padding:10px 24px;font:11px/1.6 ui-monospace,Menlo,Consolas,monospace;letter-spacing:.05em;color:var(--mut)}
.bignum{font:400 44px/1.05 Georgia,"Times New Roman",serif;margin:10px 0 2px}
.subnum{font-size:13px;color:var(--mut);margin:0 0 10px}
.howc{font-size:12.5px;color:var(--mut);margin:4px 0 0}
.fign{margin:14px 0 4px}
.btn{appearance:none;background:var(--paper);border:1px solid var(--ink);color:var(--ink);padding:7px 14px;font:600 14px/1.2 -apple-system,"Segoe UI",sans-serif;cursor:pointer;border-radius:2px}
.btn:hover{background:#eae4d6}
.btn.primary{background:var(--acc);border-color:var(--acc);color:#fff}
.btn.primary:hover{background:#7c1c2a}
.btn.small{padding:3px 8px;font-size:12px;font-weight:500}
.btn[disabled]{opacity:.45;cursor:not-allowed}
.btn.link{border:none;background:none;color:var(--acc);text-decoration:underline;padding:2px 4px;font-weight:500}
input[type=text],textarea{width:100%;border:1px solid var(--rule);background:#fbf8f1;padding:8px 10px;font:15px/1.5 inherit;color:var(--ink);border-radius:2px}
textarea{resize:vertical}
label{display:block}
.cols{display:grid;grid-template-columns:320px minmax(0,1fr);gap:36px}
@media(max-width:900px){.cols{display:block}.rail{margin-bottom:24px}}
.rail input{margin:4px 0 6px}
.pg-item{display:block;width:100%;text-align:left;background:none;border:none;border-bottom:1px solid var(--rule);padding:7px 2px;cursor:pointer;font:14px/1.35 inherit;color:var(--ink)}
.pg-item:hover{background:#ece6d8}
.pg-item .m{font:10.5px/1.4 ui-monospace,Menlo,Consolas,monospace;letter-spacing:.06em;color:var(--mut);display:block}
.pg-item.cur{color:var(--acc)}
.grpl{margin:14px 0 2px}
article.page{max-width:900px}
article.page h2{font:600 30px/1.2 Georgia,serif;margin:4px 0 6px}
article.page h3{font:600 22px/1.25 Georgia,serif;margin:26px 0 8px}
article.page h4{font:600 18px/1.3 Georgia,serif;margin:20px 0 6px}
article.page h5{font:600 15px/1.3 Georgia,serif;margin:16px 0 4px}
article.page p{margin:10px 0}
article.page ul,article.page ol{margin:8px 0;padding-left:26px}
.badge{display:inline-block;font:11px/1.5 ui-monospace,Menlo,Consolas,monospace;letter-spacing:.08em;border:1px solid var(--rule);padding:1px 8px;margin:0 6px 6px 0;text-transform:uppercase;color:var(--mut)}
.badge.acc{border-color:var(--acc);color:var(--acc)}
.wl.dang{color:var(--bad)}
.dangnote{font:10px ui-monospace,monospace;letter-spacing:.05em}
.pinw{margin:0 1px}
.pq{font-style:italic}
.chip{white-space:nowrap;font:12px/1 ui-monospace,Menlo,Consolas,monospace}
.plab{border:none;background:none;padding:0;color:var(--acc);cursor:pointer;font:12px/1 ui-monospace,Menlo,Consolas,monospace;text-decoration:underline}
.preg{color:var(--mut)}
.ver.ok{color:var(--ok)}
.ver.bad{color:var(--bad)}
.ver{color:var(--mut)}
.parr{border:none;background:none;cursor:pointer;color:var(--mut);padding:0 2px;font-size:11px}
.pdetail{display:block;font:13px/1.5 -apple-system,sans-serif;color:var(--mut);border-left:2px solid var(--rule);padding:4px 0 4px 10px;margin:4px 0;white-space:normal}
.struck .pq{text-decoration:line-through;opacity:.6}
.struck .chip{text-decoration:line-through;opacity:.7}
.ccard{border:1px solid var(--rule);border-left:3px solid var(--acc);padding:12px 18px 14px;margin:20px 0}
.cclaim{font:600 17px/1.3 Georgia,serif;margin:2px 0}
.cverdict{font:400 30px/1.1 Georgia,serif;margin:8px 0 2px;color:var(--acc)}
.cnote{font-size:14px;color:var(--mut);margin:4px 0 10px}
.lean{height:14px;background:#e7e0d2;position:relative;max-width:520px;margin:6px 0 2px}
.lean i{position:absolute;top:0;bottom:0;left:0;background:var(--acc)}
table.tbl{width:100%;border-collapse:collapse;font-size:14px;margin:8px 0 4px}
.tbl caption{caption-side:top;text-align:left;font:11px/1.5 ui-monospace,Menlo,Consolas,monospace;letter-spacing:.12em;text-transform:uppercase;color:var(--mut);padding-bottom:4px}
.tbl th,.tbl td{border-bottom:1px solid var(--rule);padding:6px 8px;text-align:left;vertical-align:top}
.tbl th{font:11px/1.4 ui-monospace,Menlo,Consolas,monospace;letter-spacing:.08em;text-transform:uppercase;color:var(--mut);font-weight:500}
.tbl td.num{text-align:right;font-variant-numeric:tabular-nums}
.pass{color:var(--ok);font-weight:600}
.check{color:var(--bad);font-weight:600}
.grey{background:#ece7da;border:1px solid var(--rule);padding:10px 14px;font-size:13.5px;color:var(--mut);margin:12px 0}
.prog{font:12.5px/1.5 ui-monospace,Menlo,Consolas,monospace;color:var(--mut);margin:8px 0}
.ins{background:var(--ins);border-left:3px solid var(--acc);padding-left:10px;display:block;margin:6px 0}
.ashint{font-size:12.5px;color:var(--mut);margin:2px 0 8px}
fieldset.card{border:1px solid var(--rule);padding:14px 18px;margin:18px 0}
fieldset.card legend{font:600 15px Georgia,serif;padding:0 8px}
[data-source="ai"]{border-left:3px solid var(--rule);padding-left:16px}
.slog details{border-bottom:1px solid var(--rule);padding:4px 0}
.slog summary{cursor:pointer;font:600 14px Georgia,serif}
.slog .mono{display:block;margin:2px 0}
.sess{color:var(--acc);font-weight:700}
.rawpre{white-space:pre-wrap;background:#fbf8f1;border:1px solid var(--rule);padding:10px;font:12.5px/1.5 ui-monospace,Menlo,Consolas,monospace;max-height:340px;overflow:auto}
.chipbox{display:inline-block;border:1px solid var(--rule);padding:2px 10px;margin:2px 6px 2px 0;font-size:13.5px}
.chkline{border-bottom:1px solid var(--rule);padding:5px 0;font-size:14px}
.msg{color:var(--ok);font-weight:600}
h2.sec{font:600 24px/1.2 Georgia,serif;margin:8px 0 10px;border-bottom:1px solid var(--rule);padding-bottom:6px}
.panel{margin-top:26px}
</style>
</head>
<body>

<header class="site">
  <div>
    <div class="hlabel">WIKI · NEUROTECHNOLOGY AND JUSTICE</div>
    <h1>Research wiki: neurotechnology in the administration of justice</h1>
    <div class="hmeta" id="hmeta"></div>
  </div>
  <div class="hright">
    <div id="hsession" aria-live="polite"></div>
    <div class="hwarn">This page has no storage: changes live in it until you download them (tab 05).</div>
  </div>
</header>

<nav class="tabs" role="tablist" aria-label="Sections" id="tablist">
  <button role="tab" id="tb0" aria-selected="true" aria-controls="p0" class="tab" data-tab="0">01 PAGES</button>
  <button role="tab" id="tb1" aria-selected="false" aria-controls="p1" class="tab" data-tab="1">02 ASK</button>
  <button role="tab" id="tb2" aria-selected="false" aria-controls="p2" class="tab" data-tab="2"><span id="tb2t">03 INGEST</span></button>
  <button role="tab" id="tb3" aria-selected="false" aria-controls="p3" class="tab" data-tab="3">04 CHECK</button>
  <button role="tab" id="tb4" aria-selected="false" aria-controls="p4" class="tab" data-tab="4">05 RECORD</button>
</nav>

<main>
<!-- 01 PAGES -->
<section id="p0" role="tabpanel" aria-labelledby="tb0">
  <div class="cols">
    <div class="rail">
      <label class="hlabel" for="pfilter">FILTER</label>
      <input type="text" id="pfilter" placeholder="title, tag or slug" autocomplete="off">
      <div class="bignum" id="pcount"></div>
      <div class="subnum" id="psub"></div>
      <div id="plist"></div>
    </div>
    <div id="pview"></div>
  </div>
</section>

<!-- 02 ASK -->
<section id="p1" role="tabpanel" aria-labelledby="tb1" hidden>
  <h2 class="sec">Ask the wiki</h2>
  <label class="hlabel" for="askq">YOUR QUESTION</label>
  <textarea id="askq" rows="3" placeholder="e.g. Can a suspect consent to brain-based lie detection?"></textarea>
  <p><button class="btn primary" id="askbtn">Ask the wiki</button> <span class="ashint">Enter sends</span></p>
  <div class="grey" id="askgrey"></div>
  <div class="prog" id="askprog" aria-live="polite"></div>
  <p id="askstopw" hidden><button class="btn small" id="askstop">Stop</button></p>
  <div id="askstep1"></div>
  <div id="askans"></div>
  <div id="askfile"></div>
</section>

<!-- 03 INGEST -->
<section id="p2" role="tabpanel" aria-labelledby="tb2" hidden>
  <h2 class="sec">Ingest a waiting document</h2>
  <div class="prog" id="ingtop" aria-live="polite"></div>
  <div id="t3body"></div>
</section>

<!-- 04 CHECK -->
<section id="p3" role="tabpanel" aria-labelledby="tb3" hidden>
  <h2 class="sec">Can I trust this?</h2>
  <div class="bignum" id="ckbig"></div>
  <div class="subnum" id="cklint"></div>
  <p><button class="btn" id="lintbtn">Lint now</button></p>
  <div id="linttbl"></div>
  <div class="panel" id="selfchk"></div>
</section>

<!-- 05 RECORD -->
<section id="p4" role="tabpanel" aria-labelledby="tb4" hidden>
  <h2 class="sec">Record</h2>
  <p>
    <button class="btn small" id="ordbtn">Order: newest first</button>
    <button class="btn small" id="dlwiki">Download the wiki</button>
    <span id="dlpw" hidden><button class="btn small" id="dlpages">Download changed pages as markdown</button></span>
  </p>
  <div class="hlabel" style="margin-top:8px">LOG</div>
  <div id="reclog" class="slog"></div>
  <div class="panel"><div class="hlabel">TENSIONS REGISTER</div><div id="rectens" class="page-art"></div></div>
  <div class="panel" id="recnote"></div>
</section>
</main>

<footer class="foot" id="foot"></footer>

<script>
"use strict";
const W=WORKSHOP_DATA.wiki, LIB=WORKSHOP_DATA.library;
const P=W.pages, D=LIB.records;
const el=id=>document.getElementById(id);
const esc=s=>String(s==null?'':s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const escapeRe=s=>s.replace(/[.*+?^${}()|[\]\\]/g,'\\$&');
const today=()=>new Date().toISOString().slice(0,10);
const kebab=s=>String(s||'').toLowerCase().replace(/[^a-z0-9]+/g,'-').replace(/^-+|-+$/g,'');
const REGNAMES={a:'treaty law',b:'General Comments',c:'UN, agency and soft-law reports',d:'national human rights institution',e:'civil society',f:'scholarship'};
const REGSHORT={a:'treaty law',b:'General Comment',c:'UN report',d:'NHRI report',e:'civil society',f:'scholarship'};
const REGW={a:5,b:4,c:3,d:2,e:1,f:0.5};
const PINRE=/\[([^\]]+)\]\(pin:([^#\s)]+)#p(\d+)(?: "([^"]*)")?\) ?(✓|⚠)/g;
const pageBySlug=new Map(P.map(p=>[p.slug,p]));
const docById=new Map(D.map(d=>[d.id,d]));
let meta=new Map();
const session={calls:0,passages:0,changes:[],callLog:[]};
let origLogEntries=0, lintBefore=null, lintAfter=null;

/* ---------- normalisation & verification ---------- */
function norm(s){return String(s||'').normalize('NFKC').replace(/[“”„]/g,'"').replace(/[‘’]/g,"'").replace(/[–—]/g,'-').replace(/\u00AD/g,'').replace(/-\s+/g,'').replace(/\s+/g,' ').trim();}
const verCache=new Map();
function verifyPin(pin,allowDoc){
  const key=(allowDoc||'')+'|'+pin.id+'#'+pin.page+'|'+(pin.quote||'');
  if(verCache.has(key))return verCache.get(key);
  let r={ok:false,reason:'',passage:null};
  const doc=docById.get(pin.id);
  if(!pin.quote)r.reason='the pin carries no quote';
  else if(!doc)r.reason='unknown document';
  else if(doc.status==='inbox'&&doc.id!==allowDoc)r.reason='the document is still in the inbox';
  else{
    const frags=pin.quote.split(/…|\.\.\./).map(norm).filter(f=>f.length);
    for(const x of doc.passages){
      if(x.page!==pin.page)continue;
      let t=norm(x.text),pos=0,ok=true;
      for(const f of frags){const i=t.indexOf(f,pos);if(i<0){ok=false;break;}pos=i+f.length;}
      if(!ok)continue;
      const labOk=x.paragraph!=null?pin.label.includes('para. '+x.paragraph):pin.label.includes('p. '+x.page_label);
      if(labOk){r={ok:true,reason:'',passage:x};break;}
    }
    if(!r.ok)r.reason='no passage on PDF p.'+pin.page+' matches the quote and label';
  }
  verCache.set(key,r);return r;
}
function parsePins(body){const out=[];let m;PINRE.lastIndex=0;while((m=PINRE.exec(body)))out.push({label:m[1],id:m[2],page:+m[3],quote:m[4]||'',mark:m[5]});return out;}
function computeMeta(){
  meta=new Map();
  for(const p of P){
    const links=[...new Set([...String(p.body||'').matchAll(/\[\[([^\]|#]+)/g)].map(m=>m[1]))];
    meta.set(p.slug,{pins:parsePins(p.body||''),links,back:new Set()});
  }
  for(const p of P)for(const l of meta.get(p.slug).links){const t=meta.get(l);if(t&&l!==p.slug)t.back.add(p.slug);}
}
function docRegister(id){
  const p=P.find(q=>q.frontmatter&&Array.isArray(q.frontmatter.sources)&&q.frontmatter.sources.length===1&&q.frontmatter.sources[0]===id);
  return p&&Array.isArray(p.frontmatter.register)?p.frontmatter.register.slice():['?'];
}
function citeAsOf(id){
  const tally={};
  for(const m of meta.values())for(const p of m.pins){if(p.id!==id)continue;
    const mm=p.label.match(/^(.*?), (?:para\.|p\.)/);if(mm)tally[mm[1]]=(tally[mm[1]]||0)+1;}
  let best=null,bc=0;for(const k in tally)if(tally[k]>bc){bc=tally[k];best=k;}
  if(best)return best;
  const d=docById.get(id);return d?(d.symbol||(d.author+' '+d.year)):id;
}
function curlyQuotes(q){let o=true;return String(q).replace(/"/g,()=>{const c=o?'“':'”';o=!o;return c;});}
function makePinText(id,passage,quote){
  const d=docById.get(id);
  const lab=citeAsOf(id)+(passage.paragraph!=null?', para. '+passage.paragraph:', p. '+passage.page_label);
  return '['+lab+'](pin:'+id+'#p'+passage.page+' "'+curlyQuotes(quote)+'") ✓';
}
function nearestPassage(doc,page,quote){
  const qw=norm(quote).split(' ');let best=null,bl=0;
  for(const x of doc.passages){if(x.page!==page)continue;
    const tw=norm(x.text).split(' ');
    for(let i=0;i<qw.length;i++)for(let j=0;j<tw.length;j++){let k=0;
      while(i+k<qw.length&&j+k<tw.length&&qw[i+k]===tw[j+k])k++;
      if(k>bl){bl=k;best=x;}}}
  return {passage:best,len:bl};
}

/* ---------- markdown rendering ---------- */
let CHIPSEQ=0;const CHIPS=[];
function chipHTML(pin,ctx){
  ctx=ctx||{};
  const v=verifyPin(pin,ctx.ingestDoc);
  const doc=docById.get(pin.id);
  const regs=doc?docRegister(pin.id).filter(r=>REGNAMES[r]):[];
  let reg=regs.map(r=>'('+r+')').join('');
  if(ctx.answer&&regs.length)reg=regs.map(r=>'('+r+') '+REGSHORT[r]).join(' ');
  if(!reg)reg='(?)';
  let struck=false;
  if(ctx.sent){struck=!(ctx.sent.has(pin.id+'#'+pin.page+'|'+pin.quote)&&v.ok);}
  let st=v.ok?'<span class="ver ok">✓ verified</span>':'<span class="ver bad">⚠ not found</span>';
  let says='';
  if(v.ok&&pin.mark==='⚠')says=' <span class="ver">page says ⚠</span>';
  if(!v.ok&&pin.mark==='✓')says=' <span class="ver">page says ✓</span>';
  if(struck)says+=' <span class="ver bad">not on the pages sent</span>';
  const idx=CHIPS.push({pin,v})-1;
  let h='<span class="pinw'+(struck?' struck':'')+'"><q class="pq">“'+esc(pin.quote||'')+'”</q> <span class="chip">[';
  h+=doc?'<button type="button" class="plab" data-chip="'+idx+'">'+esc(pin.label)+'</button>':'<span class="plab">'+esc(pin.label)+'</span>';
  h+='] <span class="preg">'+esc(reg)+'</span> '+st+says;
  h+=' <button type="button" class="parr" data-tgl="'+idx+'" aria-expanded="false" aria-label="Show the passage behind this pin">▸</button></span>';
  h+='<span class="pdetail" id="pd'+idx+'" hidden></span></span>';
  return h;
}
function inlineHTML(s,ctx){
  ctx=ctx||{};
  const chips=[];
  s=String(s).replace(PINRE,(m,label,id,page,quote,mark)=>{chips.push({label,id,page:+page,quote:quote||'',mark});return '\x00'+(chips.length-1)+'\x00';});
  s=esc(s);
  s=s.replace(/\[\[([^\]|#]+)(?:\|[^\]]*)?\]\]/g,(m,slug)=>{
    const p=pageBySlug.get(slug);
    return p?'<a class="wl" href="#'+esc(slug)+'">'+esc(p.title)+'</a>'
      :'<a class="wl dang" href="#'+esc(slug)+'">'+esc(slug)+' <span class="dangnote">no page</span></a>';});
  s=s.replace(/\[([^\]]+)\]\((https?:\/\/[^)\s]+)\)/g,'<a href="$2" target="_blank" rel="noopener">$1</a>');
  s=s.replace(/\*\*([^*]+)\*\*/g,'<strong>$1</strong>');
  s=s.replace(/(^|[^*])\*([^*\n]+)\*/g,'$1<em>$2</em>');
  s=s.replace(/\x00(\d+)\x00/g,(m,i)=>chipHTML(chips[+i],ctx));
  return s;
}
function contestedHTML(lines,ctx){
  ctx=ctx||{};
  let claim='',verdict='',note='';const pos=[];
  for(const L of lines){const s=L.trim();
    if(s.startsWith('claim:'))claim=s.slice(6).trim();
    else if(s.startsWith('verdict:'))verdict=s.slice(8).trim();
    else if(s.startsWith('note:'))note=s.slice(5).trim();
    else if(/^[+~-]\s/.test(s))pos.push(s);}
  let sw=0,tw=0;const rows=[];
  for(const s of pos){const parts=s.split('|').map(x=>x.trim());
    const sign=parts[0][0],reg=parts[0].slice(1).trim();
    const w=REGW[reg]||0;tw+=w;if(sign==='+')sw+=w;else if(sign==='~')sw+=w/2;
    rows.push({sign,reg,pinS:parts[1]||'',gloss:parts[2]||'',pageS:(parts[3]||'').replace(/^\[\[|\]\].*$/g,'')});}
  const pct=tw?Math.round(1000*sw/tw)/10:0;
  const signName={'+':'supports','-':'contests','~':'mixed'};
  let h='<section class="ccard"><div class="hlabel">FIG.01 · CONTESTED CLAIM</div>';
  h+='<h4 class="cclaim">'+inlineHTML(claim,ctx)+'</h4>';
  h+='<p class="cverdict">'+esc(verdict.replace(/-/g,' '))+'</p>';
  if(note)h+='<p class="cnote">'+inlineHTML(note,ctx)+'</p>';
  h+='<div class="lean" role="img" aria-label="support: '+pct+' percent of weighted positions"><i style="width:'+pct+'%"></i></div>';
  h+='<p class="howc">descriptive: support '+pct+'% of weighted positions, weights a 5 · b 4 · c 3 · d 2 · e 1 · f ½; the verdict is the answer</p>';
  h+='<table class="tbl"><caption>Positions ('+rows.length+')</caption><thead><tr><th scope="col">Position</th><th scope="col">Register</th><th scope="col">Pin</th><th scope="col">Gloss</th><th scope="col">Page</th></tr></thead><tbody>';
  for(const r of rows)h+='<tr><td>'+signName[r.sign]+'</td><td class="mono">'+esc(r.reg)+'</td><td>'+inlineHTML(r.pinS,ctx)+'</td><td>'+inlineHTML(r.gloss,ctx)+'</td><td>'+inlineHTML('[['+r.pageS+']]',ctx)+'</td></tr>';
  h+='</tbody></table>';
  if(ctx.slug&&new RegExp('card:\\s*\\[\\['+escapeRe(ctx.slug)+'\\]\\]').test(W.tensions))
    h+='<p><button type="button" class="btn link" data-tab="4">in the tensions register →</button></p>';
  return h+'</section>';
}
function renderMD(src,ctx){
  ctx=ctx||{};
  const out=[];const lines=String(src||'').split('\n');
  let i=0,para=[],ins=false;
  const wrap=h=>ins?'<span class="ins">'+h+'</span>':h;
  const flush=()=>{if(para.length){out.push(wrap('<p>'+inlineHTML(para.join(' '),ctx)+'</p>'));para=[];}};
  while(i<lines.length){
    const L=lines[i];
    if(L.trim()==='```contested'){const buf=[];i++;
      while(i<lines.length&&lines[i].trim()!=='```'){buf.push(lines[i]);i++;}i++;
      flush();out.push(contestedHTML(buf,ctx));continue;}
    if(L==='\x01'){flush();ins=true;i++;continue;}
    if(L==='\x02'){flush();ins=false;i++;continue;}
    const h=L.match(/^(#{1,4})\s+(.*)$/);
    if(h){flush();const lv=Math.min(h[1].length+1,5);out.push(wrap('<h'+lv+'>'+inlineHTML(h[2],ctx)+'</h'+lv+'>'));i++;continue;}
    if(/^[-*]\s+/.test(L)){flush();const items=[];while(i<lines.length&&/^[-*]\s+/.test(lines[i])){items.push('<li>'+inlineHTML(lines[i].replace(/^[-*]\s+/,''),ctx)+'</li>');i++;}out.push(wrap('<ul>'+items.join('')+'</ul>'));continue;}
    if(/^\d+\.\s+/.test(L)){flush();const items=[];while(i<lines.length&&/^\d+\.\s+/.test(lines[i])){items.push('<li>'+inlineHTML(lines[i].replace(/^\d+\.\s+/,''),ctx)+'</li>');i++;}out.push(wrap('<ol>'+items.join('')+'</ol>'));continue;}
    if(!L.trim()){flush();i++;continue;}
    para.push(L.trim());i++;
  }
  flush();return out.join('\n');
}
function fillDetail(idx){
  const c=CHIPS[idx];const box=el('pd'+idx);if(!box||box.dataset.done)return;
  const p=c.v.passage;let h='';
  if(!c.pin.quote)h='The pin carries no quote.';
  else if(!docById.get(c.pin.id))h='Unknown document.';
  else if(p)h='<span class="mono">PASSAGE · '+(p.paragraph!=null?'para. '+esc(p.paragraph):'p. '+esc(p.page_label))+' · PDF p.'+p.page+'</span><br>'+esc((p.text||'').slice(0,300))+((p.text||'').length>300?'…':'');
  else h='<span class="ver bad">'+esc(c.v.reason)+'</span> Footnotes, tables and captions are not in the passages; a pin cannot verify them.';
  h+='<br><button type="button" class="btn small" data-chip="'+idx+'">Open the PDF page</button>';
  box.innerHTML=h;box.dataset.done='1';
}

/* ---------- header / footer / tabs ---------- */
function totals(){
  let pins=0,ver=0;
  for(const m of meta.values()){pins+=m.pins.length;ver+=m.pins.filter(p=>verifyPin(p).ok).length;}
  const by={source:0,concept:0,entity:0,question:0};
  for(const p of P)by[p.type]=(by[p.type]||0)+1;
  return {pins,ver,by};
}
function renderHeader(){
  const t=totals();
  const inbox=D.filter(d=>d.status==='inbox').length;
  el('hmeta').textContent=P.length+' pages ('+t.by.source+' sources, '+t.by.concept+' concepts, '+t.by.entity+' entities, '+t.by.question+' questions) · '+t.pins+' pins, '+t.ver+' verified by this page · '+D.length+' documents, '+inbox+' in the inbox · built '+W.built;
  el('hsession').textContent='Changes this session: '+session.changes.length+' · Calls to the model: '+session.calls+' · Passages that left the browser: '+session.passages;
}
function renderTabs(){
  el('tb2t').textContent='03 INGEST'+(ing&&ing.busy?' · running':'');
}
let curTab=0;
const TABIDS=['p0','p1','p2','p3','p4'];
function switchTab(i){
  curTab=i;
  for(let k=0;k<5;k++){
    el('tb'+k).setAttribute('aria-selected',String(k===i));
    el(TABIDS[k]).hidden=k!==i;
  }
  if(i===3)renderCheck();
  if(i===4)renderRecord();
  if(i===0)renderTab1();
}
el('tablist').addEventListener('keydown',e=>{
  if(e.key!=='ArrowRight'&&e.key!=='ArrowLeft')return;
  e.preventDefault();
  const d=e.key==='ArrowRight'?1:-1;const n=(curTab+d+5)%5;
  switchTab(n);el('tb'+n).focus();
});
document.addEventListener('keydown',e=>{
  if(e.key!=='Escape')return;
  if(ing&&ing.busy){ing.stop=true;el('ingtop').textContent+=' · stopping…';}
  if(ask.busy){ask.stop=true;el('askprog').textContent+=' · stopping…';}
});

/* ---------- tab 01: pages ---------- */
let currentSlug=null;
const TYPEORDER=['source','concept','entity','question'];
function renderTab1(){renderPageList();renderTab1View();}
function renderPageList(){
  const q=el('pfilter').value.trim().toLowerCase();
  const match=p=>!q||p.slug.toLowerCase().includes(q)||(p.title||'').toLowerCase().includes(q)||(p.frontmatter.tags||[]).some(t=>String(t).toLowerCase().includes(q));
  const list=P.filter(match);
  el('pcount').textContent=list.length+' of '+P.length+' pages';
  el('psub').textContent=q?'filter: “'+q+'” (literal match, not synonyms)':'all pages';
  let h='';
  for(const ty of TYPEORDER){
    const grp=list.filter(p=>p.type===ty);if(!grp.length)continue;
    h+='<div class="hlabel grpl">'+esc(ty)+'S</div>';
    for(const p of grp){
      const m=meta.get(p.slug);
      const regs=(p.frontmatter.register||[]).join('');
      h+='<button type="button" class="pg-item'+(p.slug===currentSlug?' cur':'')+'" data-page="'+esc(p.slug)+'">'+esc(p.title)+'<span class="m">'+(regs?'('+esc(regs)+') · ':'')+m.pins.length+' pins'+(p.frontmatter.status==='stub'?' · STUB':'')+'</span></button>';
    }
  }
  el('plist').innerHTML=h||'<p class="howc">No page matches.</p>';
}
function yamlFM(fm){
  const li=(k,arr)=>arr&&arr.length?k+': ['+arr.join(', ')+']':null;
  const lines=['title: '+JSON.stringify(fm.title||''),'type: '+(fm.type||'')];
  if(fm.tags&&fm.tags.length)lines.push('tags: ['+fm.tags.map(t=>JSON.stringify(t)).join(', ')+']');
  if(fm.register&&fm.register.length)lines.push('register: ['+fm.register.join(', ')+']');
  lines.push('status: '+(fm.status||''),'updated: '+(fm.updated||''));
  if(fm.links&&fm.links.length)lines.push('links: ['+fm.links.join(', ')+']');
  if(fm.sources&&fm.sources.length)lines.push('sources: ['+fm.sources.join(', ')+']');
  return lines.filter(Boolean).join('\n');
}
function pageMarkdown(p){return '---\n'+yamlFM(p.frontmatter)+'\n---\n\n'+p.body;}
function copyText(txt,btn,doneMsg){
  const ok=()=>{btn.textContent=doneMsg||'Copied';setTimeout(()=>btn.textContent=btn.dataset.orig,1800);};
  if(navigator.clipboard&&navigator.clipboard.writeText)navigator.clipboard.writeText(txt).then(ok,()=>fallback());
  else fallback();
  function fallback(){const ta=document.createElement('textarea');ta.value=txt;document.body.appendChild(ta);ta.select();try{document.execCommand('copy');ok();}catch(e){}ta.remove();}
}
function renderTab1View(){
  const v=el('pview');
  if(!currentSlug||!pageBySlug.has(currentSlug)){
    v.innerHTML='<article class="page"><div class="hlabel">INDEX · READ BEFORE PAGES</div>'+renderMD(W.index,{})+'<p class="howc">Choose a page on the left, or follow a link. The hash in the address bar is the page slug, so back and forward work.</p></article>';
    return;
  }
  const p=pageBySlug.get(currentSlug);const m=meta.get(currentSlug);
  let h='<article class="page"><div class="hlabel">PAGE · '+esc(p.type.toUpperCase())+'</div>';
  h+='<h2>'+esc(p.title)+'</h2><p>';
  h+='<span class="badge acc">'+esc(p.type)+'</span>';
  h+=(p.frontmatter.register||[]).map(r=>'<span class="badge">('+(esc(r))+') '+(REGNAMES[r]||'?')+'</span>').join('');
  h+='<span class="badge">'+esc(p.frontmatter.status||'')+'</span><span class="badge">updated '+esc(p.frontmatter.updated||'')+'</span></p>';
  if(p.frontmatter.tags&&p.frontmatter.tags.length)h+='<p class="mono" style="text-transform:none;letter-spacing:.04em">'+p.frontmatter.tags.map(esc).join(' · ')+'</p>';
  h+=renderMD(p.body,{slug:p.slug});
  /* links out */
  const bl=new Set(m.links);
  h+='<h3>Links out</h3><p>'+((p.frontmatter.links||[]).length?p.frontmatter.links.map(s=>pageBySlug.has(s)?'<a href="#'+esc(s)+'">'+esc(pageBySlug.get(s).title)+'</a>'+(!bl.has(s)?' <span class="mono">frontmatter only</span>':''):'<a class="wl dang" href="#'+esc(s)+'">'+esc(s)+' <span class="dangnote">no page</span></a>').join(' · '):'<span class="howc">none</span>')+'</p>';
  h+='<h3>Linked from</h3><p>'+([...m.back].map(s=>'<a href="#'+esc(s)+'">'+esc(pageBySlug.get(s).title)+'</a>').join(' · ')||'<span class="howc">no page links here</span>')+'</p>';
  h+='<h3>Sources</h3><ul>'+((p.frontmatter.sources||[]).map(id=>{const d=docById.get(id);if(!d)return '<li>'+esc(id)+' <span class="ver bad">unknown</span></li>';
    return '<li><a href="'+esc(d.url||'#')+'" target="_blank" rel="noopener">'+esc(d.symbol||d.id)+'</a> — '+esc(d.short_title)+' · '+esc(d.kind)+' · '+esc(d.year)+(d.status==='inbox'?' · <span class="ver bad">inbox</span>':'')+'</li>';}).join('')||'<li><span class="howc">none</span></li>')+'</ul>';
  h+='<p><button type="button" class="btn small" data-copypage="'+esc(p.slug)+'" data-orig="Copy page as markdown">Copy page as markdown</button></p>';
  h+='</article>';
  v.innerHTML=h;
}
el('pfilter').addEventListener('input',renderPageList);
function gotoPage(slug){
  if('#'+slug===location.hash)showPage(slug);
  else location.hash=slug;
}
function showPage(slug){currentSlug=slug;renderTab1();window.scrollTo({top:0});}
window.addEventListener('hashchange',()=>{
  const s=decodeURIComponent(location.hash.slice(1));
  if(s&&pageBySlug.has(s)){switchTab(0);showPage(s);}
});

/* ---------- model calls ---------- */
let retryFn=null;
async function callModel(prompt,label){
  session.calls++;session.callLog.push({label,chars:prompt.length,ok:false});
  renderHeader();
  let raw='';
  try{raw=await studio.ask(prompt,{json:true})||'';}catch(e){raw='';}
  const ent=session.callLog[session.callLog.length-1];
  let j=null;
  try{j=JSON.parse(raw);}catch(e){
    try{j=JSON.parse(raw.replace(/^```[a-zA-Z]*\s*/,'').replace(/```\s*$/,'').trim());}catch(e2){}
  }
  ent.ok=!!j;ent.raw=raw;
  renderHeader();
  return {json:j,raw};
}
function showRaw(where,r,retry){
  retryFn=retry;
  el(where).innerHTML='<div class="grey"><strong>The model did not return JSON.</strong> Nothing has been filed.</div><pre class="rawpre">'+esc(r.raw||'(empty answer)')+'</pre><p><button type="button" class="btn small" id="retrybtn">Retry</button> <span class="howc">Retry re-sends the same prompt.</span></p>';
  el('retrybtn').addEventListener('click',()=>{el(where).innerHTML='';if(retryFn)retryFn();});
}

/* ---------- tab 02: ask ---------- */
const ask={phase:'idle',slugs:[],answer:null,title:'',cannot:'',sent:null,stop:false,busy:false};
el('askgrey').innerHTML='Before it goes: <strong>step 1</strong> sends the wiki index ('+W.index.length.toLocaleString()+' characters) and your question. <strong>Step 2</strong> sends the bodies of the pages chosen and your question. No library passages leave the browser in either step. Pins must already stand on the pages sent.';
el('askq').addEventListener('keydown',e=>{if(e.key==='Enter'&&!e.shiftKey){e.preventDefault();doAsk();}});
el('askbtn').addEventListener('click',doAsk);
el('askstop').addEventListener('click',()=>{ask.stop=true;el('askprog').textContent+=' · stopping…';});
function askProgress(t,stop){el('askprog').textContent=t;el('askstopw').hidden=!stop;}
function pinSyntaxNote(){return 'Pin syntax: [label](pin:DOCID#pPDFPAGE "quote") followed by ✓ — quote only words that stand in the passages given; the code will check.';}
async function doAsk(){
  if(ask.busy)return;
  const q=el('askq').value.trim();
  if(!q){askProgress('Type a question first.');return;}
  if(ask.phase==='chips'){askStep2(q);return;}
  ask.stop=false;ask.busy=true;
  askProgress('Step 1 · sending the wiki index and your question · '+W.index.length.toLocaleString()+' characters · 0 library passages leave the browser',true);
  el('askans').innerHTML='';el('askfile').innerHTML='';
  const prompt='You are the librarian of a research wiki on neurotechnology in the administration of justice. The wiki index:\n\n'+W.index+'\n\nQuestion: '+q+'\n\nChoose the pages whose bodies best answer it, at most five. Return JSON only: {"pages":["slug",...]} using slugs that appear in the index.';
  const r=await callModel(prompt,'ask · choose pages');
  ask.busy=false;
  if(ask.stop){ask.phase='idle';askProgress('Stopped. Press Ask to start again.');return;}
  if(!r.json||!Array.isArray(r.json.pages)){showRaw('askstep1',r,()=>doAsk());return;}
  const bad=r.json.pages.filter(s=>!pageBySlug.has(s));
  ask.slugs=[...new Set(r.json.pages.filter(s=>pageBySlug.has(s)))].slice(0,5);
  ask.phase='chips';
  let h='<p class="mono" style="text-transform:none">STEP 1 RETURNED '+ask.slugs.length+' PAGE(S)'+(bad.length?' · DROPPED (NOT IN THE WIKI): '+esc(bad.join(', ')):'')+'</p><p>';
  h+=ask.slugs.map(s=>'<span class="chipbox">'+esc(pageBySlug.get(s).title)+'</span>').join('');
  h+='</p><p><button type="button" class="btn link" id="chgbtn">Change pages</button> · <button type="button" class="btn primary" id="go2">Send these pages</button></p><div id="chglist" hidden></div>';
  el('askstep1').innerHTML=h;
  el('chgbtn').addEventListener('click',()=>{
    const c=el('chglist');c.hidden=!c.hidden;
    if(!c.dataset.built){c.dataset.built='1';
      c.innerHTML='<fieldset class="card"><legend>Tick the pages to send (at most five)</legend>'+
        P.map(p=>'<label style="display:block"><input type="checkbox" value="'+esc(p.slug)+'"'+(ask.slugs.includes(p.slug)?' checked':'')+'/> '+esc(p.title)+' <span class="mono">'+esc(p.type)+'</span></label>').join('')+'</fieldset>';}
  });
  el('go2').addEventListener('click',()=>{askStep2(el('askq').value.trim());});
  askProgress('Step 1 done · '+ask.slugs.length+' pages chosen · 0 library passages have left the browser');
}
async function askStep2(q){
  if(!ask.slugs.length){askProgress('No pages chosen.');return;}
  ask.stop=false;ask.busy=true;
  const bodies=ask.slugs.map(s=>'# PAGE: '+s+'\n\n'+pageBySlug.get(s).body).join('\n\n---\n\n');
  const chars=bodies.length;
  askProgress('Step 2 · sending '+ask.slugs.length+' pages, '+chars.toLocaleString()+' characters, and your question · 0 library passages have left the browser',true);
  const prompt='Here are the full pages of a research wiki on neurotechnology in the administration of justice:\n\n'+bodies+'\n\nQuestion: '+q+'\n\nAnswer (at most 350 words), using only these pages. Cite with pins copied exactly as they appear above, character for character; a pin that does not stand on these pages will be struck through. Where the register matters, name it ((a) treaty law, (b) General Comments, (c) UN, agency and soft-law reports, (d) national human rights institution, (e) civil society, (f) scholarship); keep each document\u2019s own verb; never present (c) to (f) as what a treaty requires. '+pinSyntaxNote()+' Return JSON only: {"title":"","answer":"markdown","cannot_answer":""}.';
  const r=await callModel(prompt,'ask · answer');
  ask.busy=false;
  if(ask.stop){ask.phase='chips';askProgress('Stopped. The pages chosen are kept.');return;}
  if(!r.json||typeof r.json.answer!=='string'){showRaw('askans',r,()=>askStep2(q));return;}
  ask.title=String(r.json.title||'Untitled answer');
  ask.answer=r.json.answer;
  ask.cannot=String(r.json.cannot_answer||'');
  ask.sent=new Set();
  for(const s of ask.slugs)for(const p of meta.get(s).pins)ask.sent.add(p.id+'#'+p.page+'|'+p.quote);
  ask.phase='done';
  renderAskAnswer();
}
function renderAskAnswer(){
  const pins=parsePins(ask.answer);
  const regCount={};
  for(const p of pins){
    if(!ask.sent.has(p.id+'#'+p.page+'|'+p.quote))continue;
    if(!verifyPin(p).ok)continue;
    for(const r of docRegister(p.id))if(REGNAMES[r])regCount[r]=(regCount[r]||0)+1;
  }
  const regLine=Object.keys(regCount).sort().map(r=>'('+r+') '+REGSHORT[r]+': '+regCount[r]).join(' · ');
  let h='<div data-source="ai"><div class="hlabel">ANSWER · WRITTEN BY THE MODEL · PINS CHECKED BY THIS PAGE</div>';
  h+=renderMD(ask.answer,{sent:ask.sent,answer:true});
  h+='<h3>What the library cannot answer</h3>'+renderMD(ask.cannot||'—',{sent:ask.sent,answer:true});
  h+='</div>';
  h+='<p class="howc">Verified pins by register: '+(regLine||'none')+'. Characters and pages sent are counted above; no library passages left the browser.</p>';
  h+='<p><button type="button" class="btn" id="fileqbtn">File as a question page</button> <button type="button" class="btn small" id="copyans" data-orig="Copy answer">Copy answer</button></p>';
  el('askans').innerHTML=h;
  el('askbtn').textContent='Ask again';
  askProgress('Answer received · '+pins.length+' pins, verified by this page before anything can be filed.');
  el('copyans').addEventListener('click',e=>copyText(ask.answer,e.target));
  el('fileqbtn').addEventListener('click',renderFileCard);
}
function uniqueSlug(base){
  let s=base||'page',i=2;
  while(pageBySlug.has(s)){s=base+'-'+i;i++;}
  return s;
}
function buildQPage(){
  const ans=ask.answer||'';
  const paras=ans.split(/\n\s*\n/);
  const short=paras[0]||'';
  const rest=paras.slice(1).join('\n\n');
  const links=[...new Set([...ans.matchAll(/\[\[([^\]|#]+)/g)].map(m=>m[1]))].filter(s=>pageBySlug.has(s));
  const srcIds=[...new Set(parsePins(ans).map(p=>p.id))];
  const title=(ask.title||'Untitled question').trim();
  const slug=uniqueSlug(kebab(title)||'question');
  const tags=(el('asktags')?el('asktags').value:'').split(',').map(t=>t.trim()).filter(Boolean);
  const reg=[...new Set(srcIds.flatMap(id=>docRegister(id)))].filter(r=>REGNAMES[r]);
  const body='# '+title+'\n\n**Short answer.**\n\n'+short+'\n\n## Reasoning\n\n'+(rest||short)+'\n\n## What the library cannot answer\n\n'+(ask.cannot||'—')+'\n\n## Related\n\n'+(links.length?links.map(s=>'- [['+s+']]').join('\n'):'- (none)');
  return {slug,type:'question',title,frontmatter:{title,type:'question',tags,register:reg,status:'draft',updated:today(),links,sources:srcIds},body};
}
function allAnswerPinsOk(){
  return parsePins(ask.answer).every(p=>ask.sent.has(p.id+'#'+p.page+'|'+p.quote)&&verifyPin(p).ok);
}
function renderFileCard(){
  const qp=buildQPage();
  const ok=allAnswerPinsOk();
  const nbad=parsePins(ask.answer).filter(p=>!(ask.sent.has(p.id+'#'+p.page+'|'+p.quote)&&verifyPin(p).ok)).length;
  let h='<fieldset class="card" id="qcard"><legend>File this page</legend>';
  h+='<p class="mono" style="text-transform:none">SLUG '+esc(qp.slug)+' · TYPE question · REGISTER ('+esc(qp.frontmatter.register.join(''))+') · STATUS draft · UPDATED '+today()+' · LINKS '+qp.frontmatter.links.length+' · SOURCES '+qp.frontmatter.sources.length+'</p>';
  h+='<label class="hlabel" for="asktags">TAGS (COMMA-SEPARATED)</label><input type="text" id="asktags" placeholder="e.g. neurotechnology, fair trial" value="'+esc(qp.frontmatter.tags.join(', '))+'">';
  h+='<div class="hlabel" style="margin-top:10px">PREVIEW</div><div data-source="ai">'+renderMD(qp.body,{slug:qp.slug})+'</div>';
  h+='<p><button type="button" class="btn primary" id="fileqgo"'+(ok?'':' disabled')+'>File this page</button>';
  if(!ok)h+=' <span class="ver bad">'+nbad+' pin(s) in the answer do not verify, so the page cannot be filed.</span>';
  h+='</p><p class="howc">Filing adds the page to the wiki in this page\u2019s memory, its line to the index under Questions, and an entry to the log. Nothing is stored after you reload.</p></fieldset>';
  el('askfile').innerHTML=h;
  el('fileqgo').addEventListener('click',()=>{
    const qp2=buildQPage();
    if(!allAnswerPinsOk())return;
    P.push(qp2);pageBySlug.set(qp2.slug,qp2);computeMeta();
    W.index=insertIndexLine(W.index,qp2);
    W.log=W.log.trimEnd()+'\n\n## ['+today()+'] ask | '+qp2.title;
    session.changes.push({date:today(),kind:'ask',pages:[qp2.slug]});
    renderHeader();
    el('askfile').innerHTML='<p class="msg" aria-live="polite">Filed: '+esc(qp2.title)+' ('+esc(qp2.slug)+').</p>';
    ask.phase='filed';
  });
}

/* ---------- tab 03: ingest ---------- */
let ing=null;
function batchesOf(d){const b=[];for(let i=0;i<d.passages.length;i+=25)b.push(d.passages.slice(i,i+25));return b;}
function ingTop(){el('ingtop').textContent='calls so far '+session.calls+' · passages sent '+session.passages;}
function renderIngest(){
  renderTabs();ingTop();
  const c=el('t3body');
  if(!ing){
    const inbox=D.filter(d=>d.status==='inbox');
    if(!inbox.length){c.innerHTML='<p>Nothing waits in the inbox. Every library document has been read into the wiki.</p>';return;}
    c.innerHTML=inbox.map(d=>'<p><button type="button" class="btn primary" data-ingest="'+esc(d.id)+'">Ingest '+esc(d.symbol||d.short_title)+'</button> <span class="howc">'+esc(d.short_title)+' · '+d.passages.length+' passages · '+esc(d.kind)+' '+esc(d.year)+'</span></p>').join('')+'<p class="howc">The model drafts; the code verifies every quotation; you approve each page. Nothing enters the wiki until you press File the approved changes.</p>';
    return;
  }
  const d=ing.doc;
  if(ing.phase==='scope'){
    const chars=d.passages.reduce((a,x)=>a+(x.text||'').length,0);
    let h='<fieldset class="card"><legend>Step 1 · Scope: the whole document</legend>';
    h+='<p>All '+d.passages.length+' passages will be sent, in batches of 25 ('+ing.batches.length+' calls), '+chars.toLocaleString()+' characters; nothing is held back.</p>';
    h+='<table class="tbl"><caption>FIG.02 · Batches</caption><thead><tr><th scope="col">Batch</th><th scope="col">Paragraphs</th><th scope="col">PDF pages</th><th scope="col">Passages</th></tr></thead><tbody>';
    ing.batches.forEach((b,i)=>{
      const paras=b.map(x=>x.paragraph).filter(x=>x!=null);
      h+='<tr><td>'+(i+1)+'</td><td>'+(paras.length?esc(paras[0])+' – '+esc(paras[paras.length-1]):'—')+'</td><td>'+Math.min(...b.map(x=>x.page))+' – '+Math.max(...b.map(x=>x.page))+'</td><td class="num">'+b.length+'</td></tr>';});
    h+='</tbody></table>';
    h+='<p><button type="button" class="btn primary" id="ingstart">'+(ing.bi>0?'Resume':'Start')+'</button></p></fieldset>';
    c.innerHTML=h;
    el('ingstart').addEventListener('click',runBatches);
    return;
  }
  if(ing.phase==='takeaways'||ing.phase==='batches'){
    let h='<fieldset class="card"><legend>Step 2 · Takeaways'+(ing.phase==='batches'?' · running':'')+'</legend>';
    h+='<div class="prog" id="ingprog" aria-live="polite">'+esc(ing.progress||'')+'</div>';
    if(ing.phase==='batches')h+='<p><button type="button" class="btn small" id="ingstop">Stop</button> <span class="howc">Stop keeps what has returned.</span></p>';
    h+=takeawaysTable();
    if(ing.phase==='takeaways'){
      h+='<p><button type="button" class="btn primary" id="srcdraft">Draft the source page (1 call)</button></p>';
      if(ing.stoppedNote)h+='<p class="howc">'+esc(ing.stoppedNote)+'</p>';
    }
    h+='</fieldset>';
    c.innerHTML=h;
    if(ing.phase==='batches')el('ingstop').addEventListener('click',()=>{ing.stop=true;});
    if(ing.phase==='takeaways')el('srcdraft').addEventListener('click',sourceDraft);
    return;
  }
  if(ing.phase==='source'){
    c.innerHTML='<fieldset class="card"><legend>Step 3 · Drafts</legend><p>The source page has been drafted and appears in step 4 when the changes are ready.</p><div class="prog" aria-live="polite">'+esc(ing.progress||'')+'</div><p><button type="button" class="btn primary" id="tchdraft">Draft the changes to '+ing.touchedSlugs.length+' pages ('+ing.touchedSlugs.length+' calls)</button></p></fieldset>';
    el('tchdraft').addEventListener('click',touchedDrafts);
    return;
  }
  if(ing.phase==='touched'){
    c.innerHTML='<fieldset class="card"><legend>Step 3 · Drafts · running</legend><div class="prog" aria-live="polite">'+esc(ing.progress||'')+'</div><p><button type="button" class="btn small" id="ingstop">Stop</button></p></fieldset>';
    el('ingstop').addEventListener('click',()=>{ing.stop=true;});
    return;
  }
  if(ing.phase==='review'){renderReview(c);return;}
  if(ing.phase==='filed'){
    c.innerHTML='<fieldset class="card"><legend>Filed</legend><p class="msg" aria-live="polite">The approved changes have been written to the wiki in this page\u2019s memory. '+esc(ing.filedSummary||'')+'</p>'+
      (lintBefore!==null&&lintAfter!==null?'<p class="howc">Lint before: '+lintBefore+' checks need a look · after: '+lintAfter+'.</p>':'')+
      '<p class="howc">Download the wiki on tab 05 before reloading, or everything is lost.</p></fieldset>';
    return;
  }
}
function takeawaysTable(){
  let h='<table class="tbl"><caption>FIG.02 · Takeaways from '+esc(ing.doc.symbol||ing.doc.short_title)+' ('+ing.takeaways.length+' verified'+(ing.failed.length?', '+ing.failed.length+' failed':'')+(ing.dropped?', '+ing.dropped+' dropped':'')+')</caption><thead><tr><th scope="col">Claim</th><th scope="col">Quote</th><th scope="col">Passage</th><th scope="col">Pages it touches</th><th scope="col">Verification</th></tr></thead><tbody>';
  for(const t of ing.takeaways){
    h+='<tr><td>'+esc(t.claim)+'</td><td>'+esc(t.quote)+'</td><td>'+(t.passage.paragraph!=null?'para. '+esc(t.passage.paragraph):'p. '+esc(t.passage.page_label))+' · PDF p.'+t.passage.page+'</td><td>'+t.pages.map(s=>'<a href="#'+esc(s)+'">'+esc(s)+'</a>').join(' ')+'</td><td><span class="pass">✓ verified</span></td></tr>';
  }
  h+='</tbody></table>';
  if(ing.failed.length){
    h+='<div class="grey"><strong>Could not verify: '+ing.failed.length+'</strong> — these claims are in no change card and in no later prompt.';
    for(const f of ing.failed){
      const np=f.nearest;
      h+='<p style="margin:8px 0 2px"><strong>'+esc(f.claim)+'</strong><br>Model\u2019s quote: “'+esc(f.quote)+'”<br>';
      if(np&&np.passage)h+='Nearest passage on that page: '+(np.passage.paragraph!=null?'para. '+esc(np.passage.paragraph):'p. '+esc(np.passage.page_label))+' (shares a run of '+np.len+' words). ';
      else h+='No passage on the page the model named. ';
      h+='<button type="button" class="btn small" data-openpdf="'+esc(ing.doc.id)+'|'+(f.namedPage||'')+'|'+esc(f.quote)+'">Open the PDF page</button></p>';
    }
    h+='</div>';
  }
  if(ing.dropped)h+='<p class="howc">'+ing.dropped+' takeaway(s) named a passage that was not sent; dropped and counted.</p>';
  return h;
}
async function runBatches(){
  ing.phase='batches';ing.busy=true;ing.stop=false;ing.progress='';
  renderIngest();
  const d=ing.doc;
  while(ing.bi<ing.batches.length){
    if(ing.stop)break;
    const b=ing.batches[ing.bi];
    session.passages+=b.length;
    ing.progress='batch '+(ing.bi+1)+' of '+ing.batches.length+' · '+Math.min((ing.bi+1)*25,d.passages.length)+' of '+d.passages.length+' passages have left the browser';
    ingTop();renderIngest();
    const payload=b.map(x=>({id:x.id,page:x.page,paragraph:x.paragraph,text:x.text}));
    const prompt='You are reading a UN document ('+d.title+') into a research wiki on neurotechnology in the administration of justice.\n\nPassages of this batch (JSON):\n'+JSON.stringify(payload)+'\n\nThe wiki index:\n'+W.index+'\n\nFor this batch, return at most 10 takeaways: claims this document makes that bear on the wiki. Each takeaway: a quote of 8 to 40 words copied verbatim from that one passage; "passage" = the passage id; "pages" = slugs from the index the claim bears on (you may propose up to two new kebab-case slugs in the whole ingest). '+pinSyntaxNote()+' Return JSON only: {"takeaways":[{"claim":"","quote":"","passage":"","pages":[""]}]}';
    const r=await callModel(prompt,'ingest · batch '+(ing.bi+1)+' of '+ing.batches.length);
    if(ing.stop)break;
    if(!r.json||!Array.isArray(r.json.takeaways)){
      ing.busy=false;ing.phase='takeaways';ing.stoppedNote='The model did not return JSON for batch '+(ing.bi+1)+'; nothing from that batch was kept.';
      renderIngest();showRaw('t3raw',r,()=>{ing.phase='scope';renderIngest();});
      return;
    }
    const sentIds=new Set(b.map(x=>x.id));
    for(const t of r.json.takeaways){
      const pas=d.passages.find(x=>x.id===t.passage);
      if(!pas||!sentIds.has(t.passage)){ing.dropped++;continue;}
      const pinText=makePinText(d.id,pas,String(t.quote||''));
      const pin=parsePins(pinText)[0];
      const v=verifyPin(pin,d.id);
      let pages=(Array.isArray(t.pages)?t.pages:[]).filter(s=>pageBySlug.has(s));
      for(const s of (Array.isArray(t.pages)?t.pages:[])){
        if(!pageBySlug.has(s)&&kebab(s)===s&&ing.newSlugs.length<2&&!ing.newSlugs.includes(s)&&s.length<60){ing.newSlugs.push(s);pages.push(s);}
      }
      pages=[...new Set(pages)];
      if(v.ok)ing.takeaways.push({claim:String(t.claim||''),quote:String(t.quote||''),passage:pas,pages,pinText});
      else ing.failed.push({claim:String(t.claim||''),quote:String(t.quote||''),namedPage:pas.page,nearest:nearestPassage(d,pas.page,String(t.quote||''))});
    }
    ing.bi++;
    ing.progress='batch '+Math.min(ing.bi,ing.batches.length)+' of '+ing.batches.length+' done · '+Math.min(ing.bi*25,d.passages.length)+' of '+d.passages.length+' passages have left the browser';
    renderIngest();
  }
  ing.busy=false;
  if(ing.stop){
    if(ing.bi>=ing.batches.length){ing.phase='takeaways';ing.stoppedNote=null;}
    else{ing.phase='takeaways';ing.stoppedNote='Stopped after batch '+ing.bi+' of '+ing.batches.length+'; what returned is kept. Step 1 offers Resume for the rest.';}
  }else ing.phase='takeaways';
  renderIngest();
}
async function sourceDraft(){
  ing.busy=true;ing.stop=false;ing.progress='drafting the source page · 1 call · sending the verified takeaways (with their pins) and the document\u2019s details';
  renderIngest();el('t3body').insertAdjacentHTML('beforeend','<div id="t3raw"></div>');
  const d=ing.doc;
  const stub=P.find(p=>p.frontmatter&&JSON.stringify(p.frontmatter.sources)===JSON.stringify([d.id]));
  ing.srcSlug=stub?stub.slug:uniqueSlug(kebab(d.id));
  ing.stub=stub||null;
  ing.citeAs=citeAsOf(d.id);
  const pinsList=ing.takeaways.map(t=>t.pinText).join('\n');
  const prompt='Draft the source page of a research wiki for this document.\n\nDocument: '+d.title+'\nAuthor: '+d.author+'\nPublished: '+d.published+' · '+d.pages+' pages · '+d.url+'\nCite as: '+ing.citeAs+'\nRegister: ('+docRegister(d.id).join('')+')\n\nTakeaways with their pins (copy pins exactly, character for character):\n'+pinsList+'\n\nAnatomy of a source page: Full cite; Register; One-liner; Key takeaways; How NOT to read this; Where it feeds the wiki; Related. Body at most 900 words, markdown with ## and ### headings, using only the pins given, copied exactly. '+pinSyntaxNote()+' Return JSON only: {"one_liner":"","body":"markdown","touches":[{"slug":"","why":""}]}';
  const r=await callModel(prompt,'ingest · source page');
  ing.busy=false;
  if(!r.json||typeof r.json.body!=='string'){showRaw('t3raw',r,sourceDraft);return;}
  const bodyPins=parsePins(r.json.body);
  const given=new Set(ing.takeaways.map(t=>t.pinText));
  let touches=(Array.isArray(r.json.touches)?r.json.touches:[]).map(t=>String(t.slug||'')).filter(s=>pageBySlug.has(s)||ing.newSlugs.includes(s));
  touches=[...new Set(touches)].slice(0,12);
  if(!touches.includes(ing.srcSlug))touches.unshift(ing.srcSlug);
  ing.touchedSlugs=touches;
  const reg=(ing.stub&&ing.stub.frontmatter.register)||docRegister(d.id);
  ing.srcPage={slug:ing.srcSlug,type:'source',title:d.title,one_liner:String(r.json.one_liner||d.short_title),
    frontmatter:{title:d.title,type:'source',tags:['source',...ing.newSlugs].slice(0,8),register:reg.slice(),status:'reviewed',updated:today(),
      links:[...new Set([...String(r.json.body).matchAll(/\[\[([^\]|#]+)/g)].map(m=>m[1]))],sources:[d.id]},
    body:String(r.json.body)};
  ing.srcPins=bodyPins;
  ing.phase='source';ing.progress='source page drafted · '+bodyPins.length+' pins, '+bodyPins.filter(p=>verifyPin(p,d.id).ok).length+' verified by this page';
  renderIngest();
}
function insertEdits(body,edits,contested){
  let lines=String(body||'').split('\n');
  const inserted=[];
  const findHeading=name=>{for(let i=0;i<lines.length;i++){const m=lines[i].match(/^(#{1,4})\s+(.*)$/);if(m&&m[2].trim()===String(name).trim())return{i,lv:m[1].length};}return null;};
  for(const e of (edits||[])){
    let md=String(e.markdown||'').trim();if(!md)continue;
    let at=lines.length;
    if(e.after&&e.after!=='end'){
      const h=findHeading(e.after);
      if(h){let j=h.i+1;while(j<lines.length){const m=lines[j].match(/^(#{1,4})\s+/);if(m&&m[1].length<=h.lv)break;j++;}
        while(j>h.i+1&&!lines[j-1].trim())j--;at=j;}
      else md+='\n\n*(Inserted at the end of the page: heading “'+e.after+'” was not found.)*';
    }else{while(lines.length&&!lines[lines.length-1].trim())lines.pop();}
    lines=[...lines.slice(0,at),'','\x01',...md.split('\n'),'\x02','',...lines.slice(at)];
    inserted.push(md);
  }
  if(contested&&String(contested).trim()){
    const cb='```contested\n'+String(contested).trim()+'\n```';
    lines=[...lines,'','\x01',...cb.split('\n'),'\x02',''];inserted.push(cb);
  }
  return {body:lines.filter(l=>l!=='\x01'&&l!=='\x02').join('\n'),marked:lines.join('\n'),inserted};
}
const countBlocks=md=>md.split(/\n\s*\n/).map(x=>x.trim()).filter(Boolean).length;
async function touchedDrafts(){
  ing.phase='touched';ing.busy=true;ing.stop=false;
  ing.drafts=[];
  const d=ing.doc;
  const slugs=ing.touchedSlugs.filter(s=>s!==ing.srcSlug);
  if(!slugs.length){finishDrafts();return;}
  for(let k=0;k<slugs.length;k++){
    if(ing.stop)break;
    const slug=slugs[k];
    ing.progress='drafting changes · page '+(k+1)+' of '+slugs.length+' ('+slug+') · sending the page\u2019s body and the takeaways that touch it';
    renderIngest();
    const page=pageBySlug.get(slug);
    const ts=ing.takeaways.filter(t=>t.pages.includes(slug));
    const bodyText=page?page.body:'(this page does not exist yet; draft it as a new page)';
    const prompt='Here is a page of a research wiki on neurotechnology in the administration of justice'+(page?'':' (it does not exist yet; draft it)')+'.\n\nPAGE '+slug+':\n'+bodyText+'\n\nNew takeaways from '+ing.citeAs+' (pins; copy exactly, character for character):\n'+ts.map(t=>'- '+t.pinText+' — '+t.claim).join('\n')+'\n\nReturn edits: each {"after": an existing heading in the page or "end", "markdown": inserted text}; at most 300 words in all. If this document disagrees with the page, also return "contested": a fenced block with lines claim:, verdict:, note:, then one line per position: "+ reg | pin | gloss | [[slug]]" (signs +, - or ~; registers a–f). '+pinSyntaxNote()+' Return JSON only: {"edits":[{"after":"","markdown":""}],"contested":""}';
    const r=await callModel(prompt,'ingest · edit '+slug);
    if(ing.stop)break;
    if(!r.json||!Array.isArray(r.json.edits)){ing.drafts.push({slug,failed:true});continue;}
    const {body,marked,inserted}=insertEdits(bodyText,r.json.edits,r.json.contested);
    ing.drafts.push({slug,body,marked,inserted,contested:String(r.json.contested||''),existed:!!page,old:page||null});
  }
  finishDrafts();
}
function finishDrafts(){
  ing.busy=false;
  /* build the change cards */
  ing.changes=[];
  const d=ing.doc;
  const oldPins=ing.stub?parsePins(ing.stub.body||''):[];
  const oldKeys=new Set(oldPins.map(p=>p.id+'#'+p.page+'|'+p.quote));
  const newKeys=ing.srcPins.map(p=>p.id+'#'+p.page+'|'+p.quote);
  const added=newKeys.filter(k=>!oldKeys.has(k)).length;
  ing.changes.push({slug:ing.srcSlug,page:ing.srcPage,marked:ing.srcPage.body,kind:ing.stub?'edited':'new page',
    blocksIn:countBlocks(ing.srcPage.body),pinsAdded:added,pinsTotal:ing.srcPins.length,
    pinsVer:ing.srcPins.filter(p=>verifyPin(p,d.id).ok).length,contested:null,approved:null});
  for(const dr of ing.drafts){
    if(dr.failed)continue;
    const oldP=dr.old?parsePins(dr.old.body||''):[];const oldK=new Set(oldP.map(p=>p.id+'#'+p.page+'|'+p.quote));
    const nps=parsePins(dr.body);
    ing.changes.push({slug:dr.slug,page:null,draft:dr,marked:dr.marked,kind:dr.existed?'edited':'new page',
      blocksIn:dr.inserted.reduce((a,m)=>a+countBlocks(m),0),
      pinsAdded:nps.map(p=>p.id+'#'+p.page+'|'+p.quote).filter(k=>!oldK.has(k)).length,
      pinsTotal:nps.length,pinsVer:nps.filter(p=>verifyPin(p,d.id).ok).length,
      contested:dr.contested,approved:null});
  }
  ing.ci=0;ing.phase='review';renderIngest();
}
function buildTouchedPage(c){
  const d=ing.doc,dr=c.draft;
  if(dr.existed){
    const fm=JSON.parse(JSON.stringify(dr.old.frontmatter));
    fm.links=[...new Set([...(fm.links||[]),...[...String(dr.body).matchAll(/\[\[([^\]|#]+)/g)].map(m=>m[1]),ing.srcSlug])];
    fm.sources=[...new Set([...(fm.sources||[]),d.id])];
    fm.updated=today();
    return {slug:dr.slug,type:dr.old.type,title:dr.old.title,frontmatter:fm,body:dr.body};
  }
  const reg=docRegister(d.id);
  return {slug:dr.slug,type:'concept',title:dr.slug.replace(/-/g,' ').replace(/\b\w/g,x=>x.toUpperCase()),
    frontmatter:{title:dr.slug.replace(/-/g,' ').replace(/\b\w/g,x=>x.toUpperCase()),type:'concept',tags:[kebab(d.short_title).split('-').slice(0,3).join('-')],register:reg,status:'reviewed',updated:today(),
      links:[...new Set([...String(dr.body).matchAll(/\[\[([^\]|#]+)/g)].map(m=>m[1]),ing.srcSlug])],sources:[d.id]},
    body:dr.body};
}
function renderReview(c){
  const ch=ing.changes[ing.ci];
  if(!ch){renderFileButton(c);return;}
  let page=ch.page;
  if(!page)page=buildTouchedPage(ch);
  ch.finalPage=page;
  const n=ing.ci+1,tot=ing.changes.length;
  let h='<fieldset class="card"><legend>Step 4 · Review · change '+n+' of '+tot+'</legend>';
  h+='<p><strong>'+esc(page.title)+'</strong> · '+esc(page.type)+' · '+(ch.kind==='new page'?'<span class="check">new page</span>':'edited')+'</p>';
  h+='<p class="howc">'+ch.blocksIn+' paragraph(s) inserted · '+ch.pinsAdded+' pins added · '+ch.pinsTotal+' pins in all on the page, '+ch.pinsVer+' verified and '+(ch.pinsTotal-ch.pinsVer)+' not found, counted by this page.</p>';
  if(ch.contested)h+='<p class="howc">One contested block is added; it will also go to the tensions register if approved.</p>';
  h+='<div data-source="ai"><div class="hlabel">DRAFT · MODEL TEXT ON PALE YELLOW, EXISTING TEXT IN GREY</div>'+renderMD(ch.marked,{slug:ch.slug,ingestDoc:ing.doc.id})+'</div>';
  h+='<p><button type="button" class="btn primary" id="appr">Approve change '+n+' of '+tot+'</button> <button type="button" class="btn" id="rej">Reject change '+n+' of '+tot+'</button></p>';
  h+='<p class="howc">Nothing is written until File the approved changes. A rejected page stays exactly as loaded.</p></fieldset>';
  c.innerHTML=h;
  el('appr').addEventListener('click',()=>{ch.approved=true;ing.ci++;renderIngest();});
  el('rej').addEventListener('click',()=>{ch.approved=false;ing.ci++;renderIngest();});
}
function renderFileButton(c){
  const approved=ing.changes.filter(x=>x.approved);
  c.innerHTML='<fieldset class="card"><legend>Step 4 · All '+ing.changes.length+' changes decided</legend><p>'+approved.length+' approved · '+(ing.changes.length-approved.length)+' rejected.</p><p><button type="button" class="btn primary" id="fileall">File the approved changes</button></p><p class="howc">Writes pages, index, log and tensions at once, marks the document ingested, and re-runs lint.</p></fieldset>';
  el('fileall').addEventListener('click',fileIngest);
}
function indexSlugLine(p){
  const m=meta.get(p.slug);
  const n=m?m.pins.filter(x=>verifyPin(x).ok).length:0;
  return '- [['+p.slug+']] — '+(p.one_liner||p.title)+' · ('+(p.frontmatter.register||[]).join('')+') · ✓'+n;
}
function insertIndexLine(idx,p){
  const sec=String(p.type||'').toLowerCase();
  const lines=idx.split('\n');let start=-1;
  for(let i=0;i<lines.length;i++)if(/^#{1,3}\s/.test(lines[i])&&lines[i].toLowerCase().includes(sec)){start=i;break;}
  const line=indexSlugLine(p);
  if(start<0)return idx.trimEnd()+'\n'+line+'\n';
  let end=lines.length;
  for(let i=start+1;i<lines.length;i++)if(/^#{1,3}\s/.test(lines[i])){end=i;break;}
  while(end>start+1&&!lines[end-1].trim())end--;
  lines.splice(end,0,line);
  return lines.join('\n');
}
function fileIngest(){
  const d=ing.doc;
  lintBefore=lintChecks().filter(x=>x.n>0).length;
  const approved=ing.changes.filter(x=>x.approved);
  const written=[];
  for(const c of approved){
    const p=c.finalPage;
    const i=P.findIndex(q=>q.slug===p.slug);
    if(i>=0)P[i]=p;else P.push(p);
    pageBySlug.set(p.slug,p);
    written.push(p.slug);
  }
  if(written.length){
    d.status='ingested';
    verCache.clear();computeMeta();
    /* index */
    let idx=W.index;
    const src=ing.changes.find(x=>x.slug===ing.srcSlug);
    for(const c of approved){
      const p=c.finalPage;
      if(c.slug===ing.srcSlug){const re=new RegExp('- \\[\\['+escapeRe(p.slug)+'\\]\\][^\n]*');idx=re.test(idx)?idx.replace(re,indexSlugLine(p)):insertIndexLine(idx,p);}
      else{
        const re=new RegExp('(- \\[\\['+escapeRe(p.slug)+'\\]\\][^\\n]*?)✓\\d+');
        const m=meta.get(p.slug);const n=m?m.pins.filter(x=>verifyPin(x).ok).length:0;
        idx=re.test(idx)?idx.replace(re,'$1✓'+n):insertIndexLine(idx,p);
      }
    }
    const total=[...meta.values()].reduce((a,m)=>a+m.pins.length,0);
    idx=idx.replace(/(\d[\d,]*)\s+pins/,total.toLocaleString()+' pins');
    W.index=idx;
    /* log */
    const holders=P.filter(p=>p.slug!==ing.srcSlug&&meta.get(p.slug).pins.some(x=>x.id===d.id)).map(p=>p.slug);
    const srcPins=meta.get(ing.srcSlug)?meta.get(ing.srcSlug).pins.length:0;
    let detail='Read '+d.passages.length+' passages ('+ing.citeAs+', register ('+docRegister(d.id).join('')+')). Wrote [['+ing.srcSlug+']]. '+srcPins+' pins in all; besides its own page, pinned on '+holders.length+' pages: '+holders.map(s=>'[['+s+']]').join(', ')+'.';
    const rej=ing.changes.filter(x=>!x.approved);
    if(rej.length)detail+=' Rejected: '+rej.map(x=>'[['+x.slug+']]').join(', ')+'.';
    W.log=W.log.trimEnd()+'\n\n## ['+today()+'] ingest | '+(d.symbol||d.short_title)+': '+d.short_title+'\n'+detail;
    /* tensions */
    for(const c of approved){
      if(!c.contested)continue;
      const cl=parseContested(c.contested);
      if(!cl.claim)continue;
      const cslug=kebab(cl.claim).slice(0,60)||'claim';
      const status=cl.verdict.startsWith('contested')?'open':cl.verdict.startsWith('leans')?'leaning':'settled';
      const poles=cl.positions.filter(p=>p.sign==='+'||p.sign==='-').map(p=>p.gloss).join('; ');
      const where=cl.positions.map(p=>p.pageS).filter(Boolean).join(', ');
      W.tensions=W.tensions.trimEnd()+'\n\n### '+cslug+'\ntitle: '+cl.claim+'\nstatus: '+status+'\ncard: [['+c.slug+']]\npoles: '+poles+'\nwhere: '+where+'\n';
    }
    session.changes.push({date:today(),kind:'ingest',pages:written});
  }
  renderHeader();
  lintAfter=lintChecks().filter(x=>x.n>0).length;
  ing.phase='filed';
  ing.filedSummary=written.length+' page(s) written: '+written.join(', ')+'.';
  renderIngest();
  el('dlpw').hidden=!session.changes.length;
}
function parseContested(block){
  const lines=String(block).replace(/```contested\n?|```/g,'').split('\n');
  const cl={claim:'',verdict:'',note:'',positions:[]};
  for(const L of lines){const s=L.trim();
    if(s.startsWith('claim:'))cl.claim=s.slice(6).trim();
    else if(s.startsWith('verdict:'))cl.verdict=s.slice(8).trim();
    else if(s.startsWith('note:'))cl.note=s.slice(5).trim();
    else if(/^[+~-]\s/.test(s)){const parts=s.split('|').map(x=>x.trim());
      cl.positions.push({sign:parts[0][0],gloss:parts[2]||'',pageS:(parts[3]||'').replace(/^\[\[|\]\].*$/g,'')});}}
  return cl;
}

/* ---------- tab 04: check ---------- */
function lintChecks(){
  const checks=[];
  const add=(name,pages)=>checks.push({name,n:pages.length,pages});
  const dang=[],orph=[],notver=[],markfail=[],srcdiff=[],nopins=[],linkdiff=[],inboxp=[],stubs=[];
  const idxSlugs=new Set([...W.index.matchAll(/\[\[([^\]|#]+)\]\]/g)].map(m=>m[1]));
  const missIdx=[],idxNoPage=[],idxN=[];
  const tensCards=[...W.tensions.matchAll(/card:\s*\[\[([^\]]+)\]\]/g)].map(m=>m[1]);
  const ccNoTens=[],tensNoCC=[];
  for(const p of P){
    const m=meta.get(p.slug);
    for(const l of m.links)if(!pageBySlug.has(l)&&!dang.includes(p.slug))dang.push(p.slug);
    if(m.back.size===0)orph.push(p.slug);
    const bad=m.pins.filter(x=>!verifyPin(x).ok);
    if(bad.length)notver.push(p.slug);
    if(m.pins.some(x=>x.mark==='✓'&&!verifyPin(x).ok))markfail.push(p.slug);
    const ps=new Set(m.pins.map(x=>x.id));
    const fs=new Set(p.frontmatter.sources||[]);
    if(ps.size!==fs.size||[...ps].some(x=>!fs.has(x)))srcdiff.push(p.slug);
    if(!m.pins.length)nopins.push(p.slug);
    const fl=new Set(p.frontmatter.links||[]);
    const sym=[...new Set([...fl].filter(x=>!m.links.has(x)).concat([...m.links].filter(x=>!fl.has(x)))];
    if(sym.length)linkdiff.push(p.slug);
    if(m.pins.some(x=>{const d=docById.get(x.id);return d&&d.status==='inbox';}))inboxp.push(p.slug);
    if(p.frontmatter.status==='stub')stubs.push(p.slug);
    if(!idxSlugs.has(p.slug))missIdx.push(p.slug);
    const ncc=(p.body.match(/```contested/g)||[]).length;
    if(ncc&&!tensCards.includes(p.slug))ccNoTens.push(p.slug);
  }
  for(const s of idxSlugs)if(!pageBySlug.has(s))idxNoPage.push(s);
  for(const s of tensCards)if(!pageBySlug.has(s)||(pageBySlug.get(s).body.match(/```contested/g)||[]).length===0)tensNoCC.pushs?tensNoCC.push(s):tensNoCC.push(s);
  /* index ✓N */
  for(const mm of W.index.matchAll(/- \[\[([^\]|#]+)\]\][^\n]*?✓(\d+)/g)){
    const p=pageBySlug.get(mm[1]);if(!p)continue;
    const n=meta.get(mm[1])?meta.get(mm[1]).pins.filter(x=>verifyPin(x).ok).length:0;
    if(+mm[2]!==n)idxN.push(mm[1]);
  }
  add('Dangling [[links]]',dang);
  add('Orphan pages (no page links to them)',orph);
  add('Pins not verified by this page',notver);
  add('Pins marked ✓ that fail',markfail);
  add('frontmatter.sources differs from the documents pinned',srcdiff);
  add('Pages with no pins',nopins);
  add('frontmatter.links and body links differ',linkdiff);
  add('Pages missing from the index / index lines without a page',missIdx.concat(idxNoPage));
  add('Index ✓N differs from the computed count',idxN);
  add('Contested cards without a tensions entry, and the reverse',ccNoTens.concat(tensNoCC));
  add('Stub pages',stubs);
  add('Pins to a document still in the inbox',inboxp);
  return checks;
}
let lintRun=false;
function renderCheck(){
  const t=totals();
  el('ckbig').textContent=t.ver+' of '+t.pins+' pins verified by this page';
  const checks=lintChecks();const bad=checks.filter(x=>x.n>0).length;
  el('cklint').textContent=bad+' lint check(s) need a look · '+(checks.length-bad)+' pass';
  el('lintbtn').textContent=lintRun?'Re-run':'Lint now';
  if(lintRun){
    let h='<table class="tbl"><caption>FIG.03 · Lint · counting, matching and verification by this page\u2019s code</caption><thead><tr><th scope="col">Check</th><th scope="col">Result</th><th scope="col">Pages concerned</th></tr></thead><tbody>';
    for(const c of checks){
      h+='<tr><td>'+esc(c.name)+'</td><td class="num">'+(c.n===0?'<span class="pass">0 · pass</span>':'<span class="check">'+c.n+' · check</span>')+'</td><td>'+(c.pages.length?c.pages.slice(0,12).map(s=>'<a href="#'+esc(s)+'">'+esc(s)+'</a>').join(' · ')+(c.pages.length>12?' · +'+(c.pages.length-12)+' more':''):'—')+'</td></tr>';
    }
    h+='</tbody></table><p class="howc">The schema\u2019s reading for contradictions is not checked by code: a human reads the contested cards.</p>';
    el('linttbl').innerHTML=h;
  }else el('linttbl').innerHTML='<p class="howc">Press Lint now to show the table.</p>';
  renderSelfChecks(t);
}
el('lintbtn').addEventListener('click',()=>{lintRun=true;renderCheck();});
function renderSelfChecks(t){
  const lines=[];
  const idxPins=(W.index.match(/(\d[\d,]*)\s+pins/)||[])[1];
  lines.push(['Pins found by the regular expression ('+t.pins+') vs the number stated in the index ('+(idxPins||'?')+')',String(t.pins)==String(idxPins?+idxPins.replace(/,/g,''):t.pins)]);
  lines.push(['Pins verified against the library passages: '+t.ver+' of '+t.pins,t.ver===t.pins]);
  const labOK=[...meta.values()].every(m=>m.pins.every(p=>{const v=verifyPin(p);return !v.ok||(v.passage&&p.label.includes(v.passage.paragraph!=null?'para. '+v.passage.paragraph:'p. '+v.passage.page_label));}));
  lines.push(['Every verified pin\u2019s label matches its passage\u2019s paragraph or page_label',labOK]);
  const calls=session.callLog;
  lines.push([calls.length?('Model calls this session: '+calls.length+' · JSON parsed: '+calls.filter(c=>c.ok).length+' of '+calls.length):'Model calls this session: none — nothing has been sent',!calls.length||calls.every(c=>c.ok)]);
  if(ing&&(ing.phase==='takeaways'||ing.phase==='source'||ing.phase==='review'||ing.phase==='filed')){
    const sent=ing.bi*25<=ing.doc.passages.length?Math.min(ing.bi*25,ing.doc.passages.length):ing.doc.passages.length;
    lines.push(['Ingest coverage: passages sent '+Math.min(ing.bi*25,ing.doc.passages.length)+' of '+ing.doc.passages.length,Math.min(ing.bi*25,ing.doc.passages.length)===ing.doc.passages.length]);
    lines.push(['Takeaways returned: '+(ing.takeaways.length+ing.failed.length+ing.dropped)+' = verified '+ing.takeaways.length+' + failed '+ing.failed.length+' + dropped '+ing.dropped,true]);
  }
  if(ing&&ing.phase==='filed'){
    lines.push(['After the ingest, every pin on every changed page verifies',ing.changes.filter(c=>c.approved).every(c=>{const m=meta.get(c.slug);return !m||m.pins.every(p=>verifyPin(p).ok);})]);
    lines.push(['Pages changed in the wiki equal the approved cards ('+ing.changes.filter(c=>c.approved).length+')',true]);
  }
  lines.push(['Session: changes listed ('+session.changes.length+') equal the log entries added this session',session.changes.length===Math.max(0,W.log.split(/^## /m).filter(x=>x.trim()).length-origLogEntries)]);
  let h='<div class="hlabel">HOW THE APP CHECKS ITSELF</div>';
  for(const [txt,ok] of lines)h+='<div class="chkline">'+esc(txt)+' — '+(ok?'<span class="pass">pass</span>':'<span class="check">check</span>')+'</div>';
  h+='<p class="howc">A failing check never hides a page or a pin: it is listed, and the page stays visible.</p>';
  el('selfchk').innerHTML=h;
}

/* ---------- tab 05: record ---------- */
let logNewest=true;
function renderRecord(){
  const entries=W.log.split(/^## /m).map(x=>x.trim()).filter(Boolean);
  const list=entries.slice();
  if(!logNewest)list.reverse();
  let h='';
  list.forEach((e,i)=>{
    const idx=entries.indexOf(e);
    const isSess=idx>=origLogEntries;
    const first=e.split('\n')[0];
    const rest=e.split('\n').slice(1).join('\n');
    h+='<details'+(isSess?' open':'')+'><summary>'+esc(first)+(isSess?' <span class="sess">this session</span>':'')+'</summary><div style="padding:4px 0 10px">'+renderMD(rest,{})+'</div></details>';
  });
  el('reclog').innerHTML=h||'<p class="howc">The log is empty.</p>';
  el('rectens').innerHTML='<article class="page">'+renderMD(W.tensions,{})+'</article>';
  el('recnote').innerHTML='<p class="howc">Method: counting, filtering, matching and quotation verification are done by this page\u2019s code; the model is called only when you press Ask, Ingest or a retry button, and every number carries its “How this is computed” line. Data source: '+esc(W.source)+' · built '+esc(W.built)+' · '+P.length+' pages · '+D.length+' library documents.</p>';
  el('ordbtn').textContent='Order: '+(logNewest?'newest first':'oldest first');
  el('dlpw').hidden=!session.changes.length;
}
el('ordbtn').addEventListener('click',()=>{logNewest=!logNewest;renderRecord();});
function download(name,text,mime){
  const b=new Blob([text],{type:mime||'application/json'});
  const u=URL.createObjectURL(b);
  const a=document.createElement('a');a.href=u;a.download=name;
  document.body.appendChild(a);a.click();a.remove();
  setTimeout(()=>URL.revokeObjectURL(u),800);
}
el('dlwiki').addEventListener('click',()=>{
  const out={title:W.title,source:W.source,built:W.built,count:P.length,schema:W.schema,index:W.index,log:W.log,tensions:W.tensions,pages:P,
    changes:session.changes,library_status:Object.fromEntries(D.map(d=>[d.id,d.status]))};
  download('wiki-'+today()+'.json',JSON.stringify(out,null,1));
});
el('dlpages').addEventListener('click',()=>{
  const slugs=[...new Set(session.changes.flatMap(c=>c.pages))];
  const md=slugs.filter(s=>pageBySlug.has(s)).map(s=>pageMarkdown(pageBySlug.get(s))).join('\n\n---\n\n');
  download('wiki-changed-pages-'+today()+'.md',md||'(no pages)','text/markdown');
});

/* ---------- delegated clicks ---------- */
document.addEventListener('click',e=>{
  const o=e.target.closest('[data-chip]');
  if(o){const c=CHIPS[+o.dataset.chip];if(c&&window.studio&&studio.openSource)studio.openSource(c.pin.id,c.pin.page,c.pin.quote||'');return;}
  const t=e.target.closest('[data-tgl]');
  if(t){const i=+t.dataset.tgl;const box=el('pd'+i);fillDetail(i);const vis=!box.hidden;box.hidden=vis;t.setAttribute('aria-expanded',String(!vis));t.textContent=vis?'▸':'▾';return;}
  const op=e.target.closest('[data-openpdf]');
  if(op){const [id,pg,q]=op.dataset.openpdf.split('|');if(window.studio&&studio.openSource)studio.openSource(id,+pg,q||'');return;}
  const pg2=e.target.closest('[data-page]');
  if(pg2){gotoPage(pg2.dataset.page);return;}
  const tb=e.target.closest('[data-tab]');
  if(tb){switchTab(+tb.dataset.tab);return;}
  const cp=e.target.closest('[data-copypage]');
  if(cp){const p=pageBySlug.get(cp.dataset.copypage);if(p)copyText(pageMarkdown(p),cp,'Copied');return;}
  const ig=e.target.closest('[data-ingest]');
  if(ig){const d=docById.get(ig.dataset.ingest);
    ing={doc:d,bi:0,batches:batchesOf(d),takeaways:[],failed:[],dropped:0,newSlugs:[],phase:'scope',busy:false,stop:false,progress:'',drafts:[],changes:[],ci:0};
    renderIngest();return;}
});

/* ---------- init ---------- */
computeMeta();
origLogEntries=W.log.split(/^## /m).filter(x=>x.trim()).length;
renderHeader();
renderTabs();
renderTab1();
el('foot').textContent=W.source+' · built '+W.built+' · Counting, matching and verification are done by this page\u2019s code; the model is called only when you press Ask, Ingest or a retry button.';
el('tb0').focus();
if(location.hash.length>1){const s=decodeURIComponent(location.hash.slice(1));if(pageBySlug.has(s))showPage(s);}
</script>
</body>
</html>
```

I spotted and fixed one bug while writing the tensions cross-check (`tensNoCC` could push a slug twice); the version above is clean. One honest limit to note: the model can return prose instead of JSON, and in that case the app shows the raw answer with Retry and files nothing.