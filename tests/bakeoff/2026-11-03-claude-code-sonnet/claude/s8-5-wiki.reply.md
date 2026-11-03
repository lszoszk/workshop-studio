I built the research wiki workspace as one page: read and navigate every page, ask the wiki, ingest the waiting report with a person approving each page, and lint. This page's code verifies every quotation against the library, and the model is called only when you press Ask, Ingest or a retry button. Changes live in the page until you download them.

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Research wiki: neurotechnology in the administration of justice</title>
<style>
:root{--ac:#1f6fb2;--bg:#f5f7f9;--tx:#1c2733;--mut:#485364;--bd:#7d8a99;--ok:#14633a;--bad:#a1232b;--wn:#7a4a00;--wnb:#fff0c9;--ins:#fff7c4;--ln:#d5dce3}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--tx);font:16px/1.55 system-ui,-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
a{color:#17609c}
a:focus-visible,button:focus-visible,input:focus-visible,textarea:focus-visible,summary:focus-visible{outline:3px solid #0b4f87;outline-offset:2px}
.skip{position:absolute;left:-999px}.skip:focus{left:8px;top:8px;background:#fff;padding:6px;z-index:9}
.top{background:#fff;border-bottom:1px solid var(--ln);padding:14px 24px}
h1{font-size:1.45rem;margin:0 0 4px;color:#123a5c}
h2{font-size:1.3rem;margin:.2em 0 .4em;color:#123a5c}h3{font-size:1.1rem;margin:1em 0 .3em}h4{font-size:1rem;margin:.8em 0 .3em}
.sub{margin:2px 0;color:var(--mut)}.strip{margin:6px 0}.note{color:var(--mut);font-size:.92rem;margin:.4em 0}
.warn{color:var(--wn);background:var(--wnb);padding:2px 8px;border-radius:4px;font-size:.92rem}
button{font:inherit;padding:5px 12px;border:1px solid var(--ac);background:#fff;color:#0f4f85;border-radius:6px;cursor:pointer}
button.primary{background:var(--ac);color:#fff}button:disabled{opacity:.55;cursor:not-allowed}
.checks{margin:0;padding:8px 24px;background:#eef3f8;border-bottom:1px solid var(--ln)}.checks summary{cursor:pointer;font-weight:600}
.chk{margin:6px 0;padding-left:20px;font-size:.93rem}.chk li{margin:3px 0}
.pass{color:var(--ok);font-weight:700}.fail{color:var(--bad);font-weight:700}.na{color:var(--mut);font-weight:700}
.layout{display:grid;grid-template-columns:320px minmax(0,900px);gap:24px;padding:16px 24px;align-items:start}
.side{background:#fff;border:1px solid var(--ln);border-radius:8px;padding:12px;position:sticky;top:8px;max-height:calc(100vh - 16px);overflow:auto}
.tabs{display:flex;flex-wrap:wrap;gap:4px;margin-bottom:8px}.tabs button[aria-pressed="true"]{background:var(--ac);color:#fff}
.side input[type=search]{width:100%;font:inherit;padding:6px 8px;border:1px solid var(--bd);border-radius:6px}
.lt{font-size:.85rem;text-transform:uppercase;letter-spacing:.04em;color:var(--mut);margin:12px 0 4px}
.pl-list{list-style:none;margin:0;padding:0}.pl-list li{padding:3px 0;border-bottom:1px solid #eef1f4}.meta{display:block;font-size:.82rem;color:var(--mut)}
.acts{margin-top:12px;border-top:1px solid var(--ln);padding-top:10px;display:grid;gap:6px}.acts button{text-align:left}
main{background:#fff;border:1px solid var(--ln);border-radius:8px;padding:16px 22px;min-width:0}
.badge{display:inline-block;border:1px solid var(--bd);border-radius:10px;padding:0 8px;font-size:.84rem;background:#f1f4f7;margin:1px 2px}
.warnb{background:var(--wnb);color:var(--wn);border-color:var(--wn)}.ses{background:#dff1e6;color:var(--ok);border-color:var(--ok)}
.pin{display:inline-block;border:1px solid var(--bd);border-radius:12px;padding:0 8px;background:#fff;margin:1px 2px;font-size:.92rem}
.pin .pl{border:0;padding:0;background:none;color:#17609c;text-decoration:underline}
.pin.struck .pl{text-decoration:line-through}.rg{color:var(--mut);font-size:.85rem}
.vok{color:var(--ok);font-weight:700;font-size:.85rem}.vbad{color:var(--wn);font-weight:700;font-size:.85rem}.says{font-size:.8rem;color:var(--mut)}
.pin .ex{border:0;padding:0 4px;background:none}.pd{display:block;margin:4px 0;padding:6px 8px;background:#f4f6f8;border-left:3px solid var(--ac);font-size:.9rem}.pd[hidden]{display:none}
.dang{color:var(--bad)}.wl{font-weight:500}
.cc{border:1px solid var(--bd);border-radius:8px;padding:10px 14px;margin:12px 0;background:#fbfcfd}
.verd{font-size:1.5rem;font-weight:700;margin:4px 0;text-transform:capitalize;color:#123a5c}
.bar{height:12px;background:#e2e8ee;border:1px solid var(--bd);border-radius:6px;overflow:hidden}.bar span{display:block;height:100%;background:var(--ac)}
table{border-collapse:collapse;width:100%;font-size:.92rem;margin:8px 0}caption{text-align:left;font-weight:600;padding:4px 0}
th,td{border:1px solid var(--ln);padding:5px 8px;text-align:left;vertical-align:top}th{background:#f1f4f7}
.ins{background:var(--ins);border-left:4px solid #b38f00;padding:2px 10px;margin:6px 0;color:var(--tx)}
.review{color:#555}.review .ins{color:#111}
fieldset.chg,fieldset.pick{border:1px solid var(--bd);border-radius:8px;margin:10px 0}legend{font-weight:700;padding:0 6px}
.chk1{display:block;padding:2px 0}label{font-weight:600;display:block;margin:8px 0 3px}.chk1{font-weight:400}
textarea,input[type=text]{width:100%;font:inherit;padding:6px 8px;border:1px solid var(--bd);border-radius:6px}
.gray{background:#e9edf1;border:1px solid var(--ln);border-radius:6px;padding:8px 10px;margin:8px 0}
.failbox{border:2px solid var(--bad);border-radius:6px;padding:8px 12px;margin:8px 0;background:#fff3f3}
pre{white-space:pre-wrap;background:#f4f6f8;padding:8px;border-radius:6px;max-height:240px;overflow:auto}
.steps{display:flex;gap:8px;list-style:none;padding:0;flex-wrap:wrap}.steps li{padding:3px 10px;border:1px solid var(--bd);border-radius:14px;font-size:.9rem}.steps li.cur{background:var(--ac);color:#fff;border-color:var(--ac)}
.line{font-weight:600;color:var(--mut)}.prog{color:var(--mut);min-height:1.4em}
blockquote{margin:6px 0;padding-left:12px;border-left:3px solid var(--ln);color:var(--mut)}
footer{padding:14px 24px;color:var(--mut);font-size:.9rem}
@media (max-width:900px){.layout{grid-template-columns:1fr;padding:12px}.side{position:static;max-height:none}}
</style>
</head>
<body>
<a class="skip" href="#main">Skip to the main column</a>
<header class="top">
<h1>Research wiki: neurotechnology in the administration of justice</h1>
<p class="sub" id="sub"></p>
<p class="strip" id="status" aria-live="polite"></p>
<p class="strip"><button type="button" class="primary" data-act="dl-json">Download the wiki</button> <button type="button" data-act="dl-md">Download changed pages (markdown)</button> <span class="warn">This page has no storage: changes live in it until you download them.</span></p>
<p class="strip" id="flash" aria-live="polite"></p>
</header>
<details class="checks" open><summary>Checks panel: what this page compared against itself</summary><div id="checks-body"></div></details>
<div class="layout">
<aside class="side" aria-label="Wiki navigation">
<div class="tabs" role="group" aria-label="Views of the wiki">
<button type="button" data-view="page" aria-pressed="true">Pages</button>
<button type="button" data-view="log" aria-pressed="false">Log</button>
<button type="button" data-view="tensions" aria-pressed="false">Tensions</button>
<button type="button" data-view="lint" aria-pressed="false">Lint</button>
</div>
<label for="flt">Filter pages (title, tag or slug)</label>
<input id="flt" type="search" autocomplete="off">
<div id="plist"></div>
<div class="acts">
<button type="button" data-view="ask">Ask the wiki</button>
<div id="ingbtns"></div>
<button type="button" data-act="lint-now">Lint now</button>
</div>
</aside>
<main id="main" tabindex="-1">
<section id="v-page"></section>
<section id="v-log" hidden></section>
<section id="v-tensions" hidden></section>
<section id="v-lint" hidden></section>
<section id="v-ask" hidden>
<h2>Ask the wiki</h2>
<p class="note">How this works: step 1 sends the wiki index and your question so the model can name up to five pages; step 2 sends those pages and your question. The answer is checked by this page: every pin must stand on the pages sent and verify against the library.</p>
<label for="ask-q">Your question</label>
<textarea id="ask-q" rows="3"></textarea>
<div class="gray" id="ask-send" aria-live="polite"></div>
<p><button type="button" class="primary" id="ask-go" data-act="ask-go">Ask the wiki</button> <button type="button" id="ask-stop" data-act="stop" hidden>Stop</button></p>
<p class="prog" id="ask-progress" aria-live="polite"></p>
<div id="ask-fail"></div>
<div id="ask-pages"></div>
<div id="ask-answer"></div>
</section>
<section id="v-ingest" hidden>
<div id="ing-body"></div>
<p class="prog" id="ing-progress" aria-live="polite"></p>
<div id="ing-fail"></div>
</section>
</main>
</div>
<footer id="foot"></footer>
<script>
(function(){
'use strict';
const WD=window.WORKSHOP_DATA||{},WIKI=WD.wiki||{},LIB=WD.library||{};
const REGN={a:'treaty law',b:'General Comments',c:'UN, agency and soft-law reports',d:'national human rights institution',e:'civil society',f:'scholarship'};
const WT={a:5,b:4,c:3,d:2,e:1,f:0.5};
const PIN_RE=/\[([^\]]+)\]\(pin:([^#\s)]+)#p(\d+)(?: "([^"]*)")?\) ?(✓|⚠)/g;
const INLSRC=PIN_RE.source+'|\\[\\[([^\\]|#]+)(?:[|#][^\\]]*)?\\]\\]|\\[([^\\]]+)\\]\\((https?:[^)\\s]+)\\)|\\*\\*([^*]+)\\*\\*|\\*([^*\\s][^*]*)\\*|`([^`]+)`';
const FENCE='`'.repeat(3);
const $=id=>document.getElementById(id);
const esc=s=>String(s==null?'':s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const today=new Date().toISOString().slice(0,10);
const fmt=n=>Number(n).toLocaleString('en-US');
const uniq=a=>[...new Set(a)];
const slugify=s=>String(s).toLowerCase().replace(/[^a-z0-9]+/g,'-').replace(/^-+|-+$/g,'');
const reEsc=s=>String(s).replace(/[.*+?^${}()|[\]\\]/g,'\\$&');
const titleOf=s=>s.replace(/-/g,' ').replace(/^./,c=>c.toUpperCase());
function norm(s){return String(s==null?'':s).normalize('NFKC').replace(/[“”„]/g,'"').replace(/[‘’]/g,"'").replace(/[–—]/g,'-').replace(/\u00ad/g,'').replace(/-\s+/g,'').replace(/\s+/g,' ').trim();}

/* ---------- state ---------- */
let pages=(WIKI.pages||[]).map(p=>({slug:p.slug,type:p.type,title:p.title||(p.frontmatter&&p.frontmatter.title)||p.slug,frontmatter:JSON.parse(JSON.stringify(p.frontmatter||{})),body:String(p.body||'')}));
let indexTxt=String(WIKI.index||''),logTxt=String(WIKI.log||''),tensTxt=String(WIKI.tensions||'');
const docs=LIB.records||[];
const docById={};docs.forEach(d=>{docById[d.id]=d;});
const loaded={};pages.forEach(p=>{loaded[p.slug]=p.body;});
let bySlug={},back={},regCache={},ingestingId=null,baseWarn=0;
const vcache=new Map();
const S={calls:0,passages:0,chars:0,ops:[],sessLog:new Set(),sessTens:new Set(),modelLog:[],view:'page',cur:null,order:'new',lastFiling:null,pending:null};
const A={q:'',step:0,chosen:[],keys:null,ans:null,run:null,busy:false,filed:false,changing:false,tags:''};
const ing={doc:null,batches:[],step:1,running:false,run:null,items:[],failed:[],returned:0,verified:0,dropped:0,sent:new Set(),newSlugs:new Set(),src:null,jobs:[],changes:[],rv:0,filed:false};

/* ---------- parsing and verification ---------- */
function pinOf(m){return {label:m[1],id:m[2],page:+m[3],quote:m[4]||'',mark:m[5],raw:m[0]};}
function parsePins(body){return [...String(body).matchAll(PIN_RE)].map(pinOf);}
function analyze(p){
  p.bodyLinks=uniq([...p.body.matchAll(/\[\[([^\]|#]+)/g)].map(m=>m[1].trim()));
  p.pins=parsePins(p.body);
  p.frontmatter.links=p.frontmatter.links||[];p.frontmatter.sources=p.frontmatter.sources||[];
  p.frontmatter.tags=p.frontmatter.tags||[];p.frontmatter.register=p.frontmatter.register||[];
}
function reindex(){
  pages.forEach(analyze);bySlug={};pages.forEach(p=>{bySlug[p.slug]=p;});back={};regCache={};vcache.clear();
  pages.forEach(p=>p.bodyLinks.forEach(t=>{if(t!==p.slug){(back[t]=back[t]||new Set()).add(p.slug);}}));
}
function pOK(label,p){
  const tok=(p.paragraph!=null&&p.paragraph!=='')?'para\\.\\s*'+reEsc(String(p.paragraph)):'p\\.\\s*'+reEsc(String(p.page_label==null?'':p.page_label));
  return new RegExp('(?:^|[\\s,(;])'+tok+'(?![0-9A-Za-z])').test(label);
}
function verify(pin){
  const d=docById[pin.id];
  const key=[pin.id,pin.page,pin.quote,pin.label,d?d.status:'',ingestingId].join('\u0001');
  if(vcache.has(key))return vcache.get(key);
  const r=verifyRaw(pin,d);vcache.set(key,r);return r;
}
function verifyRaw(pin,d){
  if(!d)return {ok:false,quoteOk:false,reason:'the document is not in the library'};
  if(d.status==='inbox'&&d.id!==ingestingId)return {ok:false,quoteOk:false,reason:'the document is still in the inbox, not read into the wiki'};
  if(!pin.quote)return {ok:false,quoteOk:false,reason:'the pin has no quote'};
  const fr=pin.quote.split(/…|\.\.\./).map(norm).filter(Boolean);
  if(!fr.length)return {ok:false,quoteOk:false,reason:'the pin has no quote'};
  const cands=(d.passages||[]).filter(p=>p.page===pin.page);
  if(!cands.length)return {ok:false,quoteOk:false,reason:'no passage of this document starts on PDF page '+pin.page};
  let qOnly=null;
  for(const p of cands){
    const t=p._n||(p._n=norm(p.text));let pos=0,ok=true;
    for(const f of fr){const i=t.indexOf(f,pos);if(i<0){ok=false;break;}pos=i+f.length;}
    if(!ok)continue;
    if(pOK(pin.label,p))return {ok:true,quoteOk:true,labelOk:true,passage:p};
    if(!qOnly)qOnly=p;
  }
  if(qOnly)return {ok:false,quoteOk:true,labelOk:false,passage:qOnly,reason:'the quote is there, but the label does not match the passage’s paragraph or page number'};
  return {ok:false,quoteOk:false,reason:'the quote is not in any passage that starts on PDF page '+pin.page};
}
function fixMarks(s){return String(s).replace(PIN_RE,(m,l,id,pg,q)=>{const ok=verify({label:l,id:id,page:+pg,quote:q||'',mark:'',raw:m}).ok;return m.slice(0,-1)+(ok?'✓':'⚠');});}
function docReg(id){
  if(id in regCache)return regCache[id];
  const src=pages.find(p=>p.type==='source'&&p.frontmatter.sources.length===1&&p.frontmatter.sources[0]===id);
  const stub=pages.find(p=>p.frontmatter.status==='stub'&&(p.frontmatter.sources.join('|')===id||p.slug===slugify(id)));
  const pg=src||stub;const r=pg?pg.frontmatter.register.join(''):'';
  return (regCache[id]=r||'?');
}
function citeAs(d){
  const cnt={};
  pages.forEach(p=>p.pins.forEach(x=>{if(x.id===d.id){const k=x.label.replace(/,\s*(?:para|p)\..*$/,'');cnt[k]=(cnt[k]||0)+1;}}));
  const ks=Object.keys(cnt).sort((a,b)=>cnt[b]-cnt[a]);
  return ks[0]||d.symbol||((d.author||'')+' '+(d.year||'')).trim();
}
function curly(q){return q.replace(/"([^"]*)"/g,'“$1”').replace(/"/g,'”');}
function newPin(d,ps,q){
  const lab=citeAs(d)+((ps.paragraph!=null&&ps.paragraph!=='')?', para. '+ps.paragraph:', p. '+ps.page_label);
  return '['+lab+'](pin:'+d.id+'#p'+ps.page+' "'+curly(q.trim())+'") ✓';
}
function nearest(d,page,quote){
  const q=norm(quote).split(' ');let best=null,bl=0;
  (d.passages||[]).filter(p=>p.page===page).forEach(p=>{
    const t=(p._n||(p._n=norm(p.text))).split(' ');let L=0;const prev=new Array(t.length+1).fill(0);
    for(let i=1;i<=q.length;i++){let diag=0;for(let j=1;j<=t.length;j++){const tmp=prev[j];prev[j]=(q[i-1]===t[j-1])?diag+1:0;if(prev[j]>L)L=prev[j];diag=tmp;}}
    if(L>bl){bl=L;best=p;}
  });
  return {p:best,run:bl};
}
function indexEntries(){
  return indexTxt.split('\n').map(l=>{const m=l.match(/^\s*[-*]\s*\[\[([^\]|#]+)\]\]/);if(!m)return null;const n=l.match(/✓\s*(\d+)/);return {slug:m[1].trim(),line:l,n:n?+n[1]:null};}).filter(Boolean);
}
function tensParts(){
  const parts=tensTxt.split(/^### /m);const pre=parts.shift()||'';
  return {pre:pre,entries:parts.map(t=>{const nl=t.indexOf('\n');const key=(nl<0?t:t.slice(0,nl)).trim();const cm=t.match(/card:\s*(?:\[\[)?([a-z0-9][a-z0-9-]*)/i);return {key:key,text:t,rest:nl<0?'':t.slice(nl+1),card:cm?cm[1]:null};})};
}
function parseContested(b){
  const c={claim:'',verdict:'',note:'',pos:[]};
  b.split('\n').forEach(l=>{
    const t=l.trim();let m;
    if((m=t.match(/^claim:\s*(.*)$/i)))c.claim=m[1];
    else if((m=t.match(/^verdict:\s*(.*)$/i)))c.verdict=m[1];
    else if((m=t.match(/^note:\s*(.*)$/i)))c.note=m[1];
    else if(/^[+\-~](\s|$)/.test(t)){
      const pr=t.split(' | ').map(x=>x.trim());const sg=pr[0][0];let rg=pr[0].slice(1).trim().toLowerCase();const rest=pr.slice(1);
      if(!rg&&rest.length>=4)rg=rest.shift().toLowerCase();
      c.pos.push({sign:sg,reg:rg?rg[0]:'?',pin:rest[0]||'',gloss:rest[1]||'',page:rest[2]||''});
    }
  });
  return c;
}
function lean(c){let s=0,tot=0;c.pos.forEach(p=>{const w=WT[p.reg]||0;tot+=w;s+=p.sign==='+'?w:(p.sign==='~'?w/2:0);});return tot?Math.round(100*s/tot):null;}
function plain(s){return String(s).replace(PIN_RE,'$1').replace(/\[\[([^\]|#]+)[^\]]*\]\]/g,'$1').replace(/\[([^\]]+)\]\([^)]*\)/g,'$1').replace(/[*_`]/g,'').replace(/\s+/g,' ').trim();}
function oneLiner(p){const m=p.body.match(/\*\*One-liner\.\*\*\s*([^\n]+)/);return plain(m?m[1]:(p.body.split('\n').find(l=>l.trim()&&!/^#/.test(l))||p.title)).slice(0,160);}
function parseJSON(raw){
  const s=String(raw==null?'':raw);
  try{return JSON.parse(s);}catch(e){}
  const m=s.match(/`{3}(?:json)?\s*([\s\S]*?)`{3}/);
  if(m){try{return JSON.parse(m[1]);}catch(e){}}
  const a=s.indexOf('{'),b=s.lastIndexOf('}');
  if(a>=0&&b>a){try{return JSON.parse(s.slice(a,b+1));}catch(e){}}
  return null;
}

/* ---------- markdown ---------- */
function wlink(s){
  s=String(s).trim();const p=bySlug[s];
  return p?'<a class="wl" href="#'+esc(s)+'" data-go="'+esc(s)+'">'+esc(p.title)+'</a>':'<span class="dang">'+esc(s)+' <small>(no page)</small></span>';
}
function pinChip(pin,o){
  o=o||{};const v=verify(pin),d=docById[pin.id],rg=docReg(pin.id);
  const acc=o.accept?o.accept(pin):true,bad=acc!==true;
  let h='<span class="pin'+(bad?' struck':'')+'">';
  h+='<button type="button" class="pl" data-open="'+esc(pin.id)+'" data-page="'+pin.page+'" aria-label="Open '+esc(pin.id)+' at PDF page '+pin.page+' ('+esc(pin.label)+')">'+esc(pin.label)+'</button> ';
  h+='<span class="rg" title="'+esc(REGN[rg]||'register unknown')+'">('+esc(rg)+(o.longReg&&d?' '+esc(d.kind):'')+')</span> ';
  h+=v.ok?'<span class="vok">✓ verified</span>':'<span class="vbad">⚠ not found</span>';
  if(bad)h+=' <span class="vbad">'+esc(acc)+'</span>';
  if(pin.mark==='✓'&&!v.ok)h+=' <span class="says">page says ✓</span>';
  if(pin.mark==='⚠'&&v.ok)h+=' <span class="says">page says ⚠</span>';
  h+=' <button type="button" class="ex" data-exp="1" aria-expanded="false" aria-label="Show the quote and passage for '+esc(pin.label)+'">▸</button>';
  let dt='<q>'+esc(pin.quote||'(no quote)')+'</q>';
  if(v.passage){
    const p=v.passage,t=String(p.text||'');
    dt+='<br><small>Passage: '+((p.paragraph!=null&&p.paragraph!=='')?'para. '+esc(p.paragraph):'p. '+esc(p.page_label))+' · PDF page '+esc(p.page)+'</small><br>'+esc(t.slice(0,300))+(t.length>300?'…':'');
  }
  if(!v.ok)dt+='<br><strong>Not verified:</strong> '+esc(v.reason||'')+'. Footnotes, tables and captions are not in the passages, so a pin cannot verify them.';
  dt+='<br><button type="button" data-open="'+esc(pin.id)+'" data-page="'+pin.page+'" aria-label="Open the PDF page for '+esc(pin.label)+'">Open the PDF page</button>';
  return h+'<span class="pd" hidden>'+dt+'</span></span>';
}
function inline(s,o){
  s=String(s==null?'':s);const re=new RegExp(INLSRC,'g');let out='',last=0,m;
  while((m=re.exec(s))){
    out+=esc(s.slice(last,m.index));last=m.index+m[0].length;
    if(m[1]!==undefined)out+=pinChip(pinOf(m),o);
    else if(m[6]!==undefined)out+=wlink(m[6]);
    else if(m[7]!==undefined)out+='<a href="'+esc(m[8])+'" target="_blank" rel="noopener noreferrer">'+esc(m[7])+'</a>';
    else if(m[9]!==undefined)out+='<strong>'+inline(m[9],o)+'</strong>';
    else if(m[10]!==undefined)out+='<em>'+inline(m[10],o)+'</em>';
    else out+='<code>'+esc(m[11])+'</code>';
  }
  return out+esc(s.slice(last));
}
function card(b,o){
  const c=parseContested(b),pc=lean(c),sn={'+':'supports','-':'contests','~':'mixed'};
  const tc=o&&o.slug&&tensParts().entries.some(e=>e.card===o.slug);
  let h='<section class="cc" aria-label="Contested claim"><h3>'+inline(c.claim,o)+'</h3><p class="verd">'+esc((c.verdict||'no verdict').replace(/-/g,' '))+'</p><p>'+inline(c.note,o)+'</p>';
  if(pc!==null)h+='<div class="bar" role="img" aria-label="Descriptive lean: support '+pc+'% of weighted positions"><span style="width:'+pc+'%"></span></div><p class="note">descriptive: support '+pc+'% of weighted positions, weights a 5 · b 4 · c 3 · d 2 · e 1 · f ½; the verdict is the answer</p>';
  h+='<table><caption>Positions on this claim</caption><thead><tr><th scope="col">Position</th><th scope="col">Register</th><th scope="col">Pin</th><th scope="col">What it says</th><th scope="col">Page</th></tr></thead><tbody>';
  c.pos.forEach(p=>{h+='<tr><td>'+(sn[p.sign]||'?')+'</td><td>('+esc(p.reg)+') '+esc(REGN[p.reg]||'')+'</td><td>'+inline(p.pin,o)+'</td><td>'+inline(p.gloss,o)+'</td><td>'+inline(p.page,o)+'</td></tr>';});
  h+='</tbody></table>';
  if(tc)h+='<p><a href="#" data-view="tensions">in the tensions register</a></p>';
  return h+'</section>';
}
function md(src,o){
  o=o||{};const L=String(src==null?'':src).replace(/\r/g,'').split('\n');
  let h='',para=[],list=null,i=0;
  const fp=()=>{if(para.length){h+='<p>'+inline(para.join(' '),o)+'</p>';para=[];}};
  const fl=()=>{if(list){h+='<'+list.t+'>'+list.it.map(x=>'<li>'+inline(x,o)+'</li>').join('')+'</'+list.t+'>';list=null;}};
  while(i<L.length){
    const ln=L[i];let m;
    if(ln==='\u0001INS'){fp();fl();h+='<div class="ins">';i++;continue;}
    if(ln==='\u0001END'){fp();fl();h+='</div>';i++;continue;}
    if((m=ln.match(/^`{3,}\s*(\w*)\s*$/))){
      fp();fl();const buf=[];i++;
      while(i<L.length&&!/^`{3,}\s*$/.test(L[i])){buf.push(L[i]);i++;}
      i++;h+=m[1]==='contested'?card(buf.join('\n'),o):'<pre>'+esc(buf.join('\n'))+'</pre>';continue;
    }
    if((m=ln.match(/^(#{1,6})\s+(.*)$/))){fp();fl();const lv=Math.min(6,m[1].length+1);h+='<h'+lv+'>'+inline(m[2],o)+'</h'+lv+'>';i++;continue;}
    if((m=ln.match(/^\s*[-*]\s+(.*)$/))){fp();if(!list||list.t!=='ul'){fl();list={t:'ul',it:[]};}list.it.push(m[1]);i++;continue;}
    if((m=ln.match(/^\s*\d+[.)]\s+(.*)$/))){fp();if(!list||list.t!=='ol'){fl();list={t:'ol',it:[]};}list.it.push(m[1]);i++;continue;}
    if(/^\s*$/.test(ln)){fp();fl();i++;continue;}
    if(list&&/^\s+\S/.test(ln)){list.it[list.it.length-1]+=' '+ln.trim();i++;continue;}
    if(/^>\s?/.test(ln)){fp();fl();h+='<blockquote>'+inline(ln.replace(/^>\s?/,''),o)+'</blockquote>';i++;continue;}
    fl();para.push(ln.trim());i++;
  }
  fp();fl();return h;
}

/* ---------- small helpers ---------- */
function flash(m){$('flash').textContent=m;}
function renderStatus(){
  const n=S.ops.reduce((a,o)=>a+o.pages.length,0);
  $('status').textContent='Changes this session: '+n+' · Calls to the model: '+S.calls+' · Passages that left the browser: '+S.passages;
}
function yaml(fm){
  const q=v=>JSON.stringify(String(v==null?'':v)),arr=a=>'['+(a||[]).map(q).join(', ')+']';
  return '---\ntitle: '+q(fm.title)+'\ntype: '+q(fm.type)+'\ntags: '+arr(fm.tags)+'\nregister: '+arr(fm.register)+'\nstatus: '+q(fm.status)+'\nupdated: '+q(fm.updated)+'\nlinks: '+arr(fm.links)+'\nsources: '+arr(fm.sources)+'\n---\n';
}
function copyText(txt,done){
  const fb=()=>{const ta=document.createElement('textarea');ta.value=txt;ta.setAttribute('readonly','');ta.style.position='fixed';ta.style.opacity='0';document.body.appendChild(ta);ta.select();let ok=false;try{ok=document.execCommand('copy');}catch(e){}ta.remove();flash(ok?done:'Copy was blocked here; select the text and copy it by hand.');};
  if(navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText(txt).then(()=>flash(done),fb);}else{fb();}
}
function save(name,txt,type){
  try{const a=document.createElement('a');a.href=URL.createObjectURL(new Blob([txt],{type:type+';charset=utf-8'}));a.download=name;document.body.appendChild(a);a.click();setTimeout(()=>{URL.revokeObjectURL(a.href);a.remove();},500);flash('Saved '+name+'.');}
  catch(e){flash('The download did not start here: '+(e.message||e));}
}
function changedSlugs(){return pages.filter(p=>!(p.slug in loaded)||loaded[p.slug]!==p.body).map(p=>p.slug);}
function dlJSON(){
  const out={title:WIKI.title,source:WIKI.source,built:WIKI.built,count:pages.length,schema:WIKI.schema,
    pages:pages.map(p=>({slug:p.slug,type:p.type,title:p.title,frontmatter:p.frontmatter,body:p.body})),
    index:indexTxt,log:logTxt,tensions:tensTxt,changes:S.ops,library_status:Object.fromEntries(docs.map(d=>[d.id,d.status]))};
  save('wiki-'+today+'.json',JSON.stringify(out,null,1),'application/json');
}
function dlMd(){
  const ch=changedSlugs();if(!ch.length){flash('No page has changed in this session.');return;}
  save('wiki-changed-pages-'+today+'.md',ch.map(s=>yaml(bySlug[s].frontmatter)+bySlug[s].body).join('\n\n---\n\n'),'text/markdown');
}
function indexInsert(re,line,title){
  const L=indexTxt.split('\n'),hi=L.findIndex(l=>re.test(l));
  if(hi<0){L.push('','## '+title,line);}
  else{let at=L.length;for(let j=hi+1;j<L.length;j++){if(/^#{1,6}\s/.test(L[j])){at=j;break;}}while(at>hi+1&&L[at-1].trim()==='')at--;L.splice(at,0,line);}
  indexTxt=L.join('\n');
}
function rebuildIndexHead(){
  const L=indexTxt.split('\n'),i=L.findIndex(l=>/\d[\d,]*\s+pins/.test(l));if(i<0)return;
  const n=pages.reduce((a,p)=>a+p.pins.length,0);
  L[i]=L[i].replace(/(\d[\d,]*)(\s+pins)/,(m,a,b)=>n+b).replace(/(\d[\d,]*)(\s+pages)/,(m,a,b)=>pages.length+b);
  indexTxt=L.join('\n');
}
function lineFor(slug,one){
  const p=bySlug[slug];
  return '- [['+slug+']] — '+(one||oneLiner(p))+' · ('+p.frontmatter.register.join('')+') · ✓'+p.pins.filter(x=>verify(x).ok).length;
}
function addLog(op,subject,body){
  const e='## ['+today+'] '+op+' | '+subject+'\n'+body;
  logTxt=logTxt.replace(/\s*$/,'')+'\n\n'+e+'\n';S.sessLog.add(e.trim());
}

/* ---------- model calls ---------- */
async function askJSON(prompt,nPass,zone,label,run){
  for(;;){
    if(run&&run.stop)return null;
    S.calls++;S.chars+=prompt.length;S.passages+=nPass;renderStatus();
    zone.innerHTML='<p class="note">'+esc(label)+': sent '+fmt(prompt.length)+' characters and '+nPass+' library passage'+(nPass===1?'':'s')+' to the language model; waiting for the answer…</p>';
    let raw='',err=null;
    try{raw=await studio.ask(prompt,{json:true});if(typeof raw!=='string')raw=JSON.stringify(raw);}catch(e){err=e;}
    const data=err?null:parseJSON(raw);
    const entry={label:label,parsed:!!data&&typeof data==='object',retried:false,badSlugs:[]};
    S.modelLog.push(entry);
    if(entry.parsed){zone.innerHTML='';return data;}
    const choice=await new Promise(res=>{
      S.pending=res;
      zone.innerHTML='<div class="failbox" role="alert"><p><strong>'+esc(label)+': the answer could not be read as JSON'+(err?' ('+esc(err.message||err)+')':'')+'.</strong> Nothing was changed. Raw answer:</p><pre data-source="ai">'+esc(raw||'(empty)')+'</pre><p><button type="button" class="rt">Retry '+esc(label)+'</button> <button type="button" class="gu">Give up</button></p></div>';
      zone.querySelector('.rt').onclick=()=>res('retry');zone.querySelector('.gu').onclick=()=>res('stop');
    });
    S.pending=null;
    if(choice==='retry'){entry.retried=true;continue;}
    zone.innerHTML='';return null;
  }
}
function stopAll(){
  if(A.run)A.run.stop=true;if(ing.run)ing.run.stop=true;
  if(S.pending)S.pending('stop');
  flash('Stopping: what has already returned is kept.');
}

/* ---------- lint ---------- */
function runLint(){
  const sl=new Set(pages.map(p=>p.slug)),O=[],ix=indexEntries(),ixs=new Set(ix.map(e=>e.slug));
  const add=(id,label,how,items)=>O.push({id:id,label:label,how:how,items:items,n:items.length});
  const pv=[];pages.forEach(p=>p.pins.forEach(x=>pv.push({p:p,x:x,v:verify(x)})));
  const it=(p,t)=>({s:p.slug,t:t});
  add('dangling','Dangling links','A [[slug]] in a body with no page of that slug.',pages.flatMap(p=>p.bodyLinks.filter(t=>!sl.has(t)).map(t=>it(p,p.slug+' → '+t))));
  add('orphans','Orphan pages','A page that no other page links to in its body.',pages.filter(p=>!(back[p.slug]&&back[p.slug].size)).map(p=>it(p,p.title)));
  add('unver','Pins not verified by the code','Quote not found in a passage that starts on the cited PDF page, or the label does not match.',pv.filter(a=>!a.v.ok).map(a=>it(a.p,a.p.slug+': '+a.x.label)));
  add('markfail','Pins marked ✓ that fail','The page says ✓ and the code does not confirm it.',pv.filter(a=>a.x.mark==='✓'&&!a.v.ok).map(a=>it(a.p,a.p.slug+': '+a.x.label)));
  add('src','Sources differing from the documents pinned','frontmatter.sources against the document ids found in the pins.',pages.filter(p=>uniq(p.pins.map(x=>x.id)).sort().join('|')!==uniq(p.frontmatter.sources).sort().join('|')).map(p=>it(p,p.title)));
  add('nopins','Pages with no pins','A page whose body holds no pin at all.',pages.filter(p=>!p.pins.length).map(p=>it(p,p.title)));
  const rec=[];pages.forEach(p=>p.frontmatter.links.forEach(l=>{const q=bySlug[l];if(q&&!q.frontmatter.links.includes(p.slug))rec.push(it(p,p.slug+' → '+l));}));
  add('recip','Links not reciprocated','frontmatter.links of A names B, but B does not name A.',rec);
  add('idx','Pages missing from the index, or index lines without a page','Compared by slug.',pages.filter(p=>!ixs.has(p.slug)).map(p=>it(p,p.slug+' (not in the index)')).concat(ix.filter(e=>!sl.has(e.slug)).map(e=>({s:null,t:e.slug+' (index line, no page)'}))));
  const ixn=ix.filter(e=>e.n!=null&&sl.has(e.slug)&&e.n!==bySlug[e.slug].pins.filter(x=>verify(x).ok).length).map(e=>it(bySlug[e.slug],e.slug+': index says ✓'+e.n+', computed ✓'+bySlug[e.slug].pins.filter(x=>verify(x).ok).length));
  const st=indexTxt.match(/(\d[\d,]*) pins/);
  if(st&&+st[1].replace(/,/g,'')!==pv.length)ixn.push({s:null,t:'index head states '+st[1]+' pins, found '+pv.length});
  add('idxn','Index ✓N differing from the computed count','✓N on an index line against the verified pins counted on that page.',ixn);
  const cardPages=pages.filter(p=>/^`{3}contested/m.test(p.body)).map(p=>p.slug),te=tensParts().entries;
  add('card','Contested cards without a tensions entry, and the reverse','Pages with a contested block against the card: lines of the tensions register.',
    cardPages.filter(s=>!te.some(e=>e.card===s)).map(s=>({s:s,t:s+': card, no tensions entry'})).concat(te.filter(e=>!cardPages.includes(e.card)).map(e=>({s:sl.has(e.card)?e.card:null,t:e.key+': entry, no contested card'}))));
  add('stub','Stub pages','Pages whose status is “stub”.',pages.filter(p=>p.frontmatter.status==='stub').map(p=>it(p,p.title)));
  add('inbox','Pins to a document still in the inbox','The cited document has status “inbox”.',pv.filter(a=>docById[a.x.id]&&docById[a.x.id].status==='inbox').map(a=>it(a.p,a.p.slug+': '+a.x.label)));
  return O;
}
function countLint(){const o={};runLint().forEach(r=>{o[r.id]=r.n;});return o;}
function itemsHtml(items){
  if(!items.length)return '–';
  return items.slice(0,12).map(i=>i.s?'<a href="#'+esc(i.s)+'" data-go="'+esc(i.s)+'">'+esc(i.t)+'</a>':esc(i.t)).join('<br>')+(items.length>12?'<br>… and '+(items.length-12)+' more':'');
}
function baTable(){
  const F=S.lastFiling;if(!F)return '';
  return '<table><caption>Lint before and after the last filing, side by side</caption><thead><tr><th scope="col">Check</th><th scope="col">Before</th><th scope="col">After</th></tr></thead><tbody>'+runLint().map(r=>'<tr><th scope="row">'+esc(r.label)+'</th><td>'+(F.before[r.id]==null?'–':F.before[r.id])+'</td><td>'+(F.after[r.id]==null?'–':F.after[r.id])+'</td></tr>').join('')+'</tbody></table>';
}
function renderLint(){
  const L=runLint();
  let h='<h2>Lint</h2><p class="note">How this is computed: each check below is counted by this page’s code from the pages, the index, the tensions register and the library; “0 · pass” means nothing was found. Nothing here is a model’s judgement.</p><p><button type="button" data-act="lint-rerun">Re-run lint</button></p>';
  h+='<table><caption>Lint checks on the wiki as it stands now</caption><thead><tr><th scope="col">Check</th><th scope="col">Result</th><th scope="col">Pages concerned</th></tr></thead><tbody>';
  L.forEach(r=>{h+='<tr><th scope="row">'+esc(r.label)+'<br><small>'+esc(r.how)+'</small></th><td class="'+(r.n?'fail':'pass')+'">'+r.n+' · '+(r.n?'check':'pass')+'</td><td>'+itemsHtml(r.items)+'</td></tr>';});
  h+='</tbody></table><p class="note">The schema’s reading for contradictions (do two pages say opposite things about the same point?) is not done by code. It needs a person or a model, and this page does not run it.</p>'+baTable();
  $('v-lint').innerHTML=h;
}

/* ---------- checks panel ---------- */
function computeChecks(){
  const C=[],ck=(name,text,ok,pg)=>C.push({name:name,text:text,ok:ok,pg:pg||[]});
  const all=[];pages.forEach(p=>p.pins.forEach(x=>all.push({p:p,x:x,v:verify(x)})));
  const sm=indexTxt.match(/(\d[\d,]*) pins/),st=sm?+sm[1].replace(/,/g,''):null;
  ck('Pins found','Found by the regular expression: '+all.length+'; the index states '+(st==null?'no number':st)+'.',st!=null&&st===all.length);
  const nv=all.filter(a=>!a.v.ok),mf=all.filter(a=>a.x.mark==='✓'&&!a.v.ok);
  ck('Pins verified','Verified by this page: '+(all.length-nv.length)+' of '+all.length+'; marked ✓ but failing: '+mf.length+'.',nv.length===0&&mf.length===0,uniq(nv.map(a=>a.p.slug)));
  const lab=all.filter(a=>a.v.quoteOk&&!a.v.labelOk);
  ck('Labels','Pins whose quote was found but whose label differs from the passage’s paragraph or page number: '+lab.length+' of '+all.filter(a=>a.v.quoteOk).length+'.',lab.length===0,uniq(lab.map(a=>a.p.slug)));
  const L=runLint(),g=id=>L.find(x=>x.id===id);
  ck('Structure: links','Dangling links '+g('dangling').n+'; orphan pages '+g('orphans').n+'.',g('dangling').n===0&&g('orphans').n===0,uniq(g('dangling').items.concat(g('orphans').items).map(i=>i.s)));
  ck('Structure: sources','Pages whose sources differ from the documents pinned: '+g('src').n+'.',g('src').n===0,g('src').items.map(i=>i.s));
  ck('Structure: index','Pages missing from the index or index lines without a page: '+g('idx').n+'.',g('idx').n===0,g('idx').items.map(i=>i.s).filter(Boolean));
  ck('Structure: cards','Contested cards without a tensions entry, or the reverse: '+g('card').n+'.',g('card').n===0,g('card').items.map(i=>i.s).filter(Boolean));
  const ml=S.modelLog;
  if(!ml.length)ck('Model answers','No call to the model yet.',null);
  else{
    const unp=ml.filter(m=>!m.parsed&&!m.retried).length,bad=uniq(ml.flatMap(m=>m.badSlugs)),tk=ml.filter(m=>m.kind==='takeaways');
    const R=tk.reduce((a,m)=>a+(m.returned||0),0),V=tk.reduce((a,m)=>a+(m.verified||0),0),F=tk.reduce((a,m)=>a+(m.failed||0),0),D=tk.reduce((a,m)=>a+(m.dropped||0),0);
    ck('Model answers','Calls '+ml.length+'; answers not read as JSON: '+unp+'; slugs that do not exist, dropped: '+(bad.length?bad.join(', '):'none')+'; takeaways returned '+R+' = verified '+V+' + could not verify '+F+' + dropped '+D+'.',unp===0&&R===V+F+D);
  }
  if(!ing.doc||!ing.sent.size)ck('Coverage','No ingest has sent passages yet.',null);
  else ck('Coverage','Passages sent: '+ing.sent.size+' of '+ing.doc.passages.length+'; takeaways naming a passage that was not sent, dropped: '+ing.dropped+'.',ing.sent.size===ing.doc.passages.length);
  const warn=all.filter(a=>a.x.mark==='⚠').length,chs=changedSlugs();
  const chBad=pages.filter(p=>chs.includes(p.slug)).reduce((a,p)=>a+p.pins.filter(x=>!verify(x).ok).length,0);
  ck('Unverified','⚠ pins in the wiki: '+warn+' (at load: '+baseWarn+'); pins in changed pages that do not verify: '+chBad+'; takeaways returned '+ing.returned+' = verified '+ing.verified+' + could not verify '+ing.failed.length+' + dropped '+ing.dropped+'.',warn===baseWarn&&chBad===0&&ing.returned===ing.verified+ing.failed.length+ing.dropped,chs.filter(s=>bySlug[s]&&bySlug[s].pins.some(x=>!verify(x).ok)));
  const appr=uniq(S.ops.flatMap(o=>o.pages)),same=chs.length===appr.length&&chs.every(s=>appr.includes(s));
  const logOk=S.ops.filter(o=>o.kind==='ingest').every(o=>{const e=logTxt.split(/^(?=## \[)/m).find(x=>S.sessLog.has(x.trim())&&x.indexOf('| '+o.subject)>=0);return !!e&&o.pages.every(s=>e.includes('[['+s+']]'))&&o.rejected.every(s=>e.includes('[['+s+']]'));});
  ck('Approval','Pages changed in the wiki: '+chs.length+'; pages named by approved cards: '+appr.length+'; log entries list approved and rejected pages by slug: '+(logOk?'yes':'no')+'.',same&&logOk,chs);
  if(!S.lastFiling)ck('Filing','Nothing has been filed yet.',null);
  else{
    const F=S.lastFiling,ie=indexEntries();
    const bad=F.pages.filter(s=>{const p=bySlug[s];if(!p)return true;const re=parsePins(p.body);if(re.some(x=>!verify(x).ok))return true;const e=ie.find(x=>x.slug===s);return !!(e&&e.n!=null&&e.n!==re.length);});
    const last=logTxt.split(/^(?=## \[)/m).pop();
    const named=F.pages.every(s=>last.includes('[['+s+']]'));
    const fb=Object.values(F.before).filter(n=>n>0).length,fa=Object.values(F.after).filter(n=>n>0).length;
    ck('Filing','Pages re-parsed and re-verified: '+F.pages.length+', with a problem: '+bad.length+'; the last log entry names every page changed: '+(named?'yes':'no')+'; lint checks failing before '+fb+', after '+fa+' (side by side in the Lint tab).',bad.length===0&&named,bad);
  }
  ck('Session','Filings listed: '+S.ops.length+'; log entries added this session: '+S.sessLog.size+'; the download would hold '+pages.length+' pages (pages in the wiki: '+pages.length+').',S.ops.length===S.sessLog.size);
  return C;
}
function renderChecks(){
  const C=computeChecks();
  $('checks-body').innerHTML='<ul class="chk">'+C.map(c=>'<li><strong>'+esc(c.name)+'.</strong> '+esc(c.text)+' <span class="'+(c.ok===null?'na':(c.ok?'pass':'fail'))+'">'+(c.ok===null?'not run yet':(c.ok?'pass':'check'))+'</span>'+(c.pg.length?' '+c.pg.slice(0,8).map(s=>'<a href="#'+esc(s)+'" data-go="'+esc(s)+'">'+esc(s)+'</a>').join(', ')+(c.pg.length>8?' …':''):'')+'</li>').join('')+'</ul><p class="note">How this is computed: every line is counted from the data by this page’s code when anything changes. A failing check never hides a page or a pin.</p>';
}

/* ---------- views ---------- */
function setView(v){
  S.view=v;
  ['page','log','tensions','lint','ask','ingest'].forEach(x=>{$('v-'+x).hidden=(x!==v);});
  document.querySelectorAll('.tabs [data-view]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.view===v)));
  if(v==='page')renderPage();if(v==='log')renderLog();if(v==='tensions')renderTens();if(v==='lint')renderLint();if(v==='ask')askAnnounce();if(v==='ingest')renderIngest();
}
function go(slug){
  if(!bySlug[slug])return;
  S.cur=slug;setView('page');renderSidebar();
  try{if(location.hash!=='#'+slug)location.hash=slug;}catch(e){}
  try{window.scrollTo(0,0);}catch(e){}
}
function renderHeader(){
  const c={};pages.forEach(p=>{c[p.type]=(c[p.type]||0)+1;});
  let pins=0,ver=0;pages.forEach(p=>p.pins.forEach(x=>{pins++;if(verify(x).ok)ver++;}));
  const inbox=docs.filter(d=>d.status==='inbox').length;
  $('sub').textContent=pages.length+' pages ('+(c.source||0)+' sources, '+(c.concept||0)+' concepts, '+(c.entity||0)+' entities, '+(c.question||0)+' questions) · '+fmt(pins)+' pins, '+fmt(ver)+' verified by this page · '+docs.length+' documents, '+inbox+' in the inbox · built '+(WIKI.built||'unknown');
  renderStatus();
}
function renderSidebar(){
  const f=($('flt').value||'').trim().toLowerCase(),order=['source','concept','entity','question'];
  let h='';
  uniq(order.concat(pages.map(p=>p.type))).forEach(t=>{
    const list=pages.filter(p=>p.type===t&&(!f||p.title.toLowerCase().includes(f)||p.slug.toLowerCase().includes(f)||p.frontmatter.tags.some(x=>String(x).toLowerCase().includes(f))));
    if(!list.length)return;
    h+='<h3 class="lt">'+esc(t)+' ('+list.length+')</h3><ul class="pl-list">'+list.map(p=>'<li><a href="#'+esc(p.slug)+'" data-go="'+esc(p.slug)+'"'+(p.slug===S.cur&&S.view==='page'?' aria-current="page"':'')+'>'+esc(p.title)+'</a>'+(p.frontmatter.status==='stub'?' <span class="badge warnb">stub</span>':'')+'<span class="meta">('+esc(p.frontmatter.register.join(''))+') · '+p.pins.length+' pins</span></li>').join('')+'</ul>';
  });
  $('plist').innerHTML=h||'<p class="note">No page matches the filter.</p>';
}
function renderIngButtons(){
  const ib=docs.filter(d=>d.status==='inbox');
  $('ingbtns').innerHTML=ib.length?ib.map(d=>'<button type="button" data-act="ing-pick" data-id="'+esc(d.id)+'">Ingest '+esc(d.symbol||d.short_title||d.id)+'</button>').join(''):'<p class="note">No document is waiting in the inbox.</p>';
}
function renderPage(){
  const el=$('v-page'),p=bySlug[S.cur];
  if(!p){el.innerHTML='<p>No page selected. Choose one from the list.</p>';return;}
  const fm=p.frontmatter,first=p.body.split('\n')[0],body=/^#\s/.test(first)?p.body.split('\n').slice(1).join('\n'):p.body;
  const vp=p.pins.filter(x=>verify(x).ok).length,bl=new Set(p.bodyLinks);
  const regs=fm.register.map(r=>'<span class="badge">('+esc(r)+') '+esc(REGN[r]||'')+'</span>').join(' ');
  const out=fm.links.map(s=>'<li>'+wlink(s)+(bl.has(s)?'':' <span class="badge">frontmatter only</span>')+'</li>').join('');
  const inb=[...(back[p.slug]||[])].sort().map(s=>'<li>'+wlink(s)+'</li>').join('');
  const src=fm.sources.map(id=>{const d=docById[id];return '<li>'+(d?esc(d.short_title||d.title)+' · '+esc(d.kind)+' · '+esc(d.year)+' · <a href="'+esc(d.url)+'" target="_blank" rel="noopener noreferrer">'+esc(d.symbol||id)+'</a>'+(d.status==='inbox'?' <span class="badge warnb">inbox</span>':''):esc(id)+' <span class="badge warnb">not in the library</span>')+'</li>';}).join('');
  el.innerHTML='<article><h2>'+esc(p.title)+'</h2><p><span class="badge">'+esc(p.type)+'</span> '+regs+' <span class="badge'+(fm.status==='stub'?' warnb':'')+'">status: '+esc(fm.status||'?')+'</span> <span class="badge">updated '+esc(fm.updated||'?')+'</span></p>'+
    '<p>'+fm.tags.map(t=>'<span class="badge">#'+esc(t)+'</span>').join(' ')+'</p>'+
    '<p class="note">'+p.pins.length+' pins on this page, '+vp+' verified by this page. How this is computed: each quote is searched, fragment by fragment in order, in the passages of the cited document that start on the cited PDF page, and the label must match that passage’s paragraph or printed page number.</p>'+
    '<div class="body">'+md(body,{slug:p.slug})+'</div>'+
    '<h3>Links out</h3>'+(out?'<ul>'+out+'</ul>':'<p class="note">None.</p>')+
    '<h3>Linked from</h3>'+(inb?'<ul>'+inb+'</ul>':'<p class="note">No page links here in its body.</p>')+
    '<h3>Sources</h3>'+(src?'<ul>'+src+'</ul>':'<p class="note">None.</p>')+
    '<p><button type="button" data-act="copy-page">Copy page as markdown</button></p></article>';
}
function renderLog(){
  const parts=logTxt.split(/^(?=## \[)/m);
  const pre=(parts.length&&!parts[0].startsWith('## ['))?parts.shift():'';
  let ents=parts;if(S.order==='new')ents=ents.slice().reverse();
  let h='<h2>Log</h2><p class="note">How this is computed: the log is append-only; entries are read from the wiki’s log text and ordered by their position in it. Entries added in this session carry a tag.</p><p><button type="button" data-act="log-flip">Show '+(S.order==='new'?'oldest first':'newest first')+'</button> <span class="note">Now: '+(S.order==='new'?'newest first':'oldest first')+'</span></p>';
  if(pre.trim())h+=md(pre);
  h+=ents.map((e,i)=>{const nl=e.indexOf('\n'),head=(nl<0?e:e.slice(0,nl)).replace(/^##\s*/,''),rest=nl<0?'':e.slice(nl+1);return '<details'+(i===0?' open':'')+'><summary>'+esc(head)+(S.sessLog.has(e.trim())?' <span class="badge ses">this session</span>':'')+'</summary><div>'+md(rest)+'</div></details>';}).join('');
  $('v-log').innerHTML=h;
}
function renderTens(){
  const t=tensParts();
  let h='<h2>Tensions register</h2><p class="note">How this is computed: the register is the wiki’s own text; each entry’s card: link opens the page that holds the contested block.</p>';
  if(t.pre.trim())h+=md(t.pre);
  h+=t.entries.map(e=>'<details open><summary>'+esc(e.key)+(S.sessTens.has(e.key)?' <span class="badge ses">this session</span>':'')+'</summary><div>'+md(e.rest.replace(/([^\n])\n(?=[A-Za-z_]+:)/g,'$1\n\n'))+'</div></details>').join('');
  $('v-tensions').innerHTML=h;
}

/* ---------- ask the wiki ---------- */
const pk=x=>x.id+'#p'+x.page+'|'+norm(x.quote);
const ackFn=x=>{if(!A.keys||!A.keys.has(pk(x)))return 'not on the pages sent';return verify(x).ok?true:'not verified by the code';};
function askAnnounce(){
  const q=($('ask-q').value||'').trim();let m;
  if(A.step===0)m='Step 1 will send the wiki index ('+fmt(indexTxt.length)+' characters) and your question ('+fmt(q.length)+' characters) to a language model, outside this browser. 0 library passages will leave the browser.';
  else if(A.step===1){const ch=A.chosen.map(s=>bySlug[s]).filter(Boolean),c=ch.reduce((a,p)=>a+p.body.length,0)+q.length;m='Step 2 will send '+ch.length+' page'+(ch.length===1?'':'s')+' and your question, '+fmt(c)+' characters; 0 library passages have left the browser.';}
  else m='Both steps are done. 0 library passages have left the browser.';
  $('ask-send').textContent=m;
}
function askBusy(on){A.busy=on;$('ask-go').disabled=on;$('ask-stop').hidden=!on;}
async function askStep1(){
  const q=$('ask-q').value.trim();
  if(!q){flash('Type a question first.');return;}
  if(A.busy)return;
  A.q=q;A.step=0;A.ans=null;A.filed=false;A.changing=false;A.chosen=[];$('ask-answer').innerHTML='';$('ask-pages').innerHTML='';
  const run=A.run={stop:false};askBusy(true);
  $('ask-progress').textContent='Step 1 of 2: asking which pages hold the answer…';
  const prompt='You are helping to answer a question from a research wiki. Below is the wiki index, one line per page. Choose the pages most likely to hold the answer, at most 5. Return JSON only: {"pages": ["slug", ...]} with slugs written exactly as in the index.\n\nQUESTION: '+q+'\n\nINDEX:\n'+indexTxt;
  const data=await askJSON(prompt,0,$('ask-fail'),'Ask, step 1',run);
  askBusy(false);
  if(!data){$('ask-progress').textContent='Step 1 stopped. Nothing was filed.';renderChecks();return;}
  const ml=S.modelLog[S.modelLog.length-1],ch=[];
  (Array.isArray(data.pages)?data.pages:[]).forEach(s=>{s=String(s).trim();if(bySlug[s]){if(!ch.includes(s))ch.push(s);}else{ml.badSlugs.push(s);}});
  A.chosen=ch.slice(0,5);A.step=1;
  $('ask-progress').textContent='Step 1 of 2 done: '+A.chosen.length+' page'+(A.chosen.length===1?'':'s')+' chosen.';
  renderAskPages();askAnnounce();renderChecks();
}
function renderAskPages(){
  const el=$('ask-pages');
  if(A.step<1){el.innerHTML='';return;}
  let h='<h3>Pages chosen by the model</h3><p data-source="ai">'+(A.chosen.length?A.chosen.map(s=>wlink(s)).join(' · '):'The model named no page that exists.')+'</p><p><button type="button" data-act="ask-change" aria-expanded="'+(A.changing?'true':'false')+'">Change pages</button></p>';
  if(A.changing)h+='<fieldset class="pick"><legend>Tick up to 5 pages to send in step 2</legend>'+pages.map(p=>'<label class="chk1"><input type="checkbox" data-pick="'+esc(p.slug)+'"'+(A.chosen.includes(p.slug)?' checked':'')+'> '+esc(p.title)+' <small>('+esc(p.type)+')</small></label>').join('')+'</fieldset>';
  if(A.step===1)h+='<p><button type="button" class="primary" data-act="ask-step2"'+(A.busy?' disabled':'')+'>Send these pages and the question (step 2)</button></p>';
  el.innerHTML=h;
}
async function askStep2(){
  if(A.busy||!A.chosen.length){if(!A.chosen.length)flash('Choose at least one page.');return;}
  const ch=A.chosen.map(s=>bySlug[s]).filter(Boolean),run=A.run={stop:false};askBusy(true);
  $('ask-progress').textContent='Step 2 of 2: answering from '+ch.length+' page'+(ch.length===1?'':'s')+'…';
  const prompt='Answer the question using only the wiki pages below. Every claim carries a pin copied exactly from these pages, in this syntax: [label](pin:DOC#pPAGE "verbatim quote") ✓ . Quote only words that stand in the passages given; the code will check every pin. Name the register where it matters (a treaty law, b General Comments, c UN, agency and soft-law reports, d national human rights institution, e civil society, f scholarship). Keep the document’s own verb (“the report records”, “the AHRC reads”). Never present (c) to (f) as what the treaty requires. At most 350 words. Say in cannot_answer what the pages cannot answer. Return JSON only: {"title": "...", "answer": "markdown with pins", "cannot_answer": "..."}.\n\nQUESTION: '+A.q+'\n\nPAGES:\n'+ch.map(p=>'### ['+p.slug+'] '+p.title+'\n'+p.body).join('\n\n');
  const data=await askJSON(prompt,0,$('ask-fail'),'Ask, step 2',run);
  askBusy(false);
  if(!data){$('ask-progress').textContent='Step 2 stopped. Nothing was filed.';renderAskPages();renderChecks();return;}
  A.ans={title:String(data.title||'Untitled answer').trim(),answer:String(data.answer||''),cannot:String(data.cannot_answer||'')};
  A.keys=new Set();ch.forEach(p=>p.pins.forEach(x=>A.keys.add(pk(x))));
  A.step=2;$('ask-progress').textContent='Both steps done.';
  renderAskPages();renderAnswer();askAnnounce();renderChecks();
}
function questionReason(){
  if(!A.ans)return 'there is no answer yet';
  if(!parsePins(A.ans.answer).length)return 'the answer holds no pin';
  const bad=parsePins(A.ans.answer+'\n'+A.ans.cannot).filter(x=>ackFn(x)!==true);
  return bad.length?bad.length+' pin'+(bad.length===1?'':'s')+' in the answer do not verify or are not on the pages sent':'';
}
function buildQuestion(){
  const a=A.ans,txt=a.answer+'\n'+a.cannot,ids=uniq(parsePins(txt).map(x=>x.id));
  const base=slugify(a.title)||'question';let slug=base;for(let n=2;bySlug[slug];n++)slug=base+'-'+n;
  const regs=uniq(ids.flatMap(id=>docReg(id).split('').filter(c=>c!=='?'))).sort();
  const links=uniq([...txt.matchAll(/\[\[([^\]|#]+)/g)].map(m=>m[1].trim()).filter(s=>bySlug[s]));
  const rel=uniq(links.concat(A.chosen));
  const tags=A.tags.split(',').map(x=>x.trim()).filter(Boolean);
  const first=a.answer.split(/\n\s*\n/)[0];
  const body='# '+a.title+'\n\n**Short answer.** '+first+'\n\n## Reasoning\n\n'+a.answer+'\n\n## What the library cannot answer\n\n'+(a.cannot||'Nothing was flagged.')+'\n\n## Related\n\n'+(rel.length?rel.map(s=>'- [['+s+']]').join('\n'):'- (no related page)')+'\n';
  return {slug:slug,first:first,body:body,fm:{title:a.title,type:'question',tags:tags,register:regs,status:'draft',updated:today,links:links,sources:ids}};
}
function renderAnswer(){
  const a=A.ans,el=$('ask-answer');
  if(!a){el.innerHTML='';return;}
  const opt={accept:ackFn,longReg:true},pins=parsePins(a.answer),good=pins.filter(x=>ackFn(x)===true),by={};
  good.forEach(x=>{const r=docReg(x.id);by[r]=(by[r]||0)+1;});
  const q=buildQuestion(),why=questionReason();
  el.innerHTML='<h3>Answer</h3><div data-source="ai"><h4>'+esc(a.title)+'</h4>'+md(a.answer,opt)+'</div>'+
    '<p class="note">'+good.length+' of '+pins.length+' pins in the answer stand on the pages sent and are verified by this page. By register: '+(Object.keys(by).sort().map(r=>'('+esc(r)+') '+by[r]).join(' · ')||'none')+'. How this is computed: each pin is looked up on the pages sent, then checked against the library by this page’s code.</p>'+
    '<h4>What the library cannot answer</h4><div data-source="ai">'+(a.cannot?md(a.cannot,opt):'<p>The model flagged nothing.</p>')+'</div>'+
    '<section class="cc"><h3>File as a question page: preview</h3><p class="note">Built by this page’s code from the answer above; nothing is written until you press the button.</p>'+
    '<ul><li>slug: '+esc(q.slug)+'</li><li>type: question · status: draft · updated: '+today+'</li><li>register: '+esc(q.fm.register.join(', ')||'none')+'</li><li>links: '+esc(q.fm.links.join(', ')||'none')+'</li><li>sources: '+esc(q.fm.sources.join(', ')||'none')+'</li></ul>'+
    '<label for="ask-tags">Tags (comma separated)</label><input type="text" id="ask-tags" value="'+esc(A.tags)+'"'+(A.filed?' disabled':'')+'>'+
    '<p><button type="button" class="primary" data-act="ask-file" aria-describedby="ask-why"'+((why||A.filed)?' disabled':'')+'>File this page</button> <button type="button" data-act="ask-copy">Copy answer</button> <button type="button" data-act="ask-again">Ask again</button></p>'+
    '<p id="ask-why" class="note" aria-live="polite">'+(A.filed?'Filed. The new question page is in the page list.':(why?'File this page is disabled: '+esc(why)+'.':'Every pin in the answer verifies, so this page can be filed.'))+'</p></section>';
}
function fileQuestion(){
  if(!A.ans||A.filed||questionReason())return;
  const q=buildQuestion();
  q.fm.tags=A.tags.split(',').map(x=>x.trim()).filter(Boolean);
  pages.push({slug:q.slug,type:'question',title:A.ans.title,frontmatter:q.fm,body:q.body});
  reindex();
  indexInsert(/^#+\s*Questions?/i,lineFor(q.slug,plain(q.first).slice(0,160)),'Questions');
  rebuildIndexHead();
  addLog('ask',A.ans.title,'Filed as [['+q.slug+']] from a question asked in the workspace; '+bySlug[q.slug].pins.length+' pins, all verified by this page.');
  S.ops.push({kind:'ask',date:today,subject:A.ans.title,pages:[q.slug],rejected:[]});
  A.filed=true;refresh();renderAnswer();flash('Filed question page '+q.slug+'.');
  $('ask-why').textContent='Filed as '+q.slug+'.';
}

/* ---------- ingest ---------- */
function ingReset(){
  Object.assign(ing,{doc:null,batches:[],step:1,running:false,run:null,items:[],failed:[],returned:0,verified:0,dropped:0,sent:new Set(),newSlugs:new Set(),src:null,jobs:[],changes:[],rv:0,filed:false});
  ingestingId=null;vcache.clear();
}
function ingSelect(id){
  if(ing.running)return;
  const d=docById[id];if(!d||d.status!=='inbox')return;
  if(!(ing.doc&&ing.doc.id===id)){
    ingReset();ing.doc=d;ingestingId=id;
    const ps=d.passages||[];
    for(let i=0;i<ps.length;i+=25)ing.batches.push({n:ing.batches.length+1,passages:ps.slice(i,i+25),status:'waiting'});
  }
  setView('ingest');
}
const pRange=ps=>{const q=ps.map(p=>p.paragraph).filter(x=>x!=null&&x!=='');return q.length?(q[0]===q[q.length-1]?String(q[0]):q[0]+' to '+q[q.length-1]):'no paragraph numbers';};
function batchTable(){
  return '<table><caption>Batches of 25 passages, in file order</caption><thead><tr><th scope="col">Batch</th><th scope="col">Passages</th><th scope="col">Paragraphs</th><th scope="col">PDF pages</th><th scope="col">State</th></tr></thead><tbody>'+ing.batches.map(b=>{const pg=b.passages.map(p=>p.page);return '<tr><td>'+b.n+'</td><td>'+b.passages.length+'</td><td>'+esc(pRange(b.passages))+'</td><td>'+Math.min(...pg)+' to '+Math.max(...pg)+'</td><td>'+esc(b.status)+'</td></tr>';}).join('')+'</tbody></table>';
}
function stubFor(d){return pages.find(p=>p.frontmatter.status==='stub'&&(p.slug===slugify(d.id)||p.title.indexOf(d.id)>=0))||null;}
function takeawayPrompt(b){
  const ps=b.passages.map(p=>({id:p.id,page:p.page,paragraph:p.paragraph,text:p.text}));
  return 'You are reading one batch of passages of a document into a research wiki. The wiki index follows, one line per page.\n\nReturn JSON only: {"takeaways":[{"claim":"...","quote":"...","passage":"<id of the passage>","pages":["slug"]}]}. At most 10 takeaways. Each quote is 8 to 40 words copied verbatim from that one passage. "pages" are slugs from the index that the claim bears on; you may propose at most two new slugs for the whole document. Quote only words that stand in the passages given; the code will check every quote. Pins in this wiki look like [label](pin:DOC#pPAGE "verbatim quote") ✓ . Say what the document says, in its own verbs; do not turn a report into what the treaty requires.\n\nDOCUMENT: '+ing.doc.title+' ('+(ing.doc.symbol||ing.doc.author)+', '+ing.doc.year+')\n\nINDEX:\n'+indexTxt+'\n\nPASSAGES:\n'+JSON.stringify(ps);
}
function procTake(b,data){
  const ml=S.modelLog[S.modelLog.length-1],d=ing.doc;ml.kind='takeaways';
  const arr=(Array.isArray(data.takeaways)?data.takeaways:[]).slice(0,10);
  ml.returned=arr.length;ml.verified=0;ml.failed=0;ml.dropped=0;
  arr.forEach(t=>{
    t=t||{};const ps=b.passages.find(p=>p.id===String(t.passage||'').trim());
    if(!ps){ml.dropped++;ing.dropped++;return;}
    const quote=String(t.quote||'').replace(/\s+/g,' ').trim(),pin=newPin(d,ps,quote);
    const px=parsePins(pin)[0]||{label:'',id:d.id,page:ps.page,quote:quote,mark:'✓'};
    const v=verify(px),pg=[];
    (Array.isArray(t.pages)?t.pages:[]).forEach(s=>{
      s=String(s).trim();if(!s||pg.includes(s))return;
      if(bySlug[s]||ing.newSlugs.has(s))pg.push(s);
      else if(/^[a-z0-9][a-z0-9-]*$/.test(s)&&ing.newSlugs.size<2){ing.newSlugs.add(s);pg.push(s);}
      else ml.badSlugs.push(s);
    });
    const row={claim:String(t.claim||''),quote:px.quote,passage:ps,pin:pin,pages:pg,ok:v.ok,reason:v.reason,batch:b.n};
    if(v.ok){ml.verified++;ing.verified++;}
    else{ml.failed++;row.near=nearest(d,ps.page,quote);ing.failed.push(row);}
    ing.items.push(row);
  });
  ing.returned+=ml.returned;
}
async function ingStart(){
  if(ing.running||!ing.doc)return;
  const run=ing.run={stop:false};ing.running=true;ing.step=2;renderIngest();
  for(const b of ing.batches){
    if(b.status==='done')continue;if(run.stop)break;
    b.status='running';b.passages.forEach(p=>ing.sent.add(p.id));
    $('ing-progress').textContent='batch '+b.n+' of '+ing.batches.length+' · '+ing.sent.size+' of '+ing.doc.passages.length+' passages have left the browser';
    renderIngest();
    const data=await askJSON(takeawayPrompt(b),b.passages.length,$('ing-fail'),'Takeaways, batch '+b.n,run);
    if(!data){b.status=run.stop?'stopped':'failed';break;}
    procTake(b,data);b.status='done';
    renderIngest();renderChecks();
  }
  ing.running=false;ing.run=null;
  $('ing-progress').textContent='Takeaways: '+ing.batches.filter(b=>b.status==='done').length+' of '+ing.batches.length+' batches done · '+ing.sent.size+' of '+ing.doc.passages.length+' passages have left the browser.';
  renderIngest();renderChecks();
}
function stepScope(d){
  const ps=d.passages||[],n=ps.length,k=Math.ceil(n/25),c=ps.reduce((a,p)=>a+String(p.text||'').length,0);
  return '<h3>Step 1. Scope: the whole document</h3><div class="gray">All '+n+' passages will be sent, in batches of 25 ('+k+' call'+(k===1?'':'s')+'), '+fmt(c)+' characters; nothing is held back. They leave the browser and go to a language model. Nothing is sent until you press Start.</div>'+batchTable()+'<p><button type="button" class="primary" data-act="ing-start"'+(n?'':' disabled')+'>Start: send '+k+' batch'+(k===1?'':'es')+'</button></p><p class="note">How this is computed: batches are the passages in file order, cut every 25; calls = the number of passages ÷ 25, rounded up; every passage is sent exactly once.</p>';
}
function stepTake(d){
  const left=ing.batches.filter(b=>b.status!=='done').length;
  let h='<h3>Step 2. Takeaways</h3>'+batchTable();
  h+='<p>'+(ing.running?'<button type="button" data-act="stop">Stop (keeps what has returned)</button>':((left?'<button type="button" class="primary" data-act="ing-start">Resume: '+left+' batch'+(left===1?'':'es')+' left</button> ':'')+(ing.verified?'<button type="button" class="primary" data-act="ing-to" data-step="3">Go to the drafts (step 3)</button>':'')))+'</p>';
  h+='<p class="note">Takeaways returned '+ing.returned+': verified '+ing.verified+', could not verify '+ing.failed.length+', dropped (passage not sent) '+ing.dropped+'. How this is computed: for each takeaway the code finds the passage by id, builds the pin and runs the same check as everywhere else.</p>';
  if(ing.items.length){
    h+='<table><caption>Takeaways returned so far</caption><thead><tr><th scope="col">Claim</th><th scope="col">Quote</th><th scope="col">Passage</th><th scope="col">Pages it would touch</th><th scope="col">Verification</th></tr></thead><tbody>'+ing.items.map(t=>'<tr><td data-source="ai">'+esc(t.claim)+'</td><td data-source="ai"><q>'+esc(t.quote)+'</q></td><td>'+((t.passage.paragraph!=null&&t.passage.paragraph!=='')?'para. '+esc(t.passage.paragraph):'p. '+esc(t.passage.page_label))+' · PDF page '+t.passage.page+'</td><td>'+(t.pages.map(s=>bySlug[s]?'<a href="#'+esc(s)+'" data-go="'+esc(s)+'">'+esc(s)+'</a>':'<span class="badge">new page: '+esc(s)+'</span>').join(' ')||'none')+'</td><td class="'+(t.ok?'pass':'fail')+'">'+(t.ok?'✓ verified':'⚠ not verified (listed below)')+'</td></tr>').join('')+'</tbody></table>';
  }
  h+='<section class="cc"><h3>Could not verify: '+ing.failed.length+'</h3>'+(ing.failed.length?'<p class="note">These claims are in no change card and in no later prompt.</p>':'<p class="note">None so far.</p>')+ing.failed.map(t=>{
    const n=t.near&&t.near.p;
    return '<div><p><strong data-source="ai">'+esc(t.claim)+'</strong><br>Model’s quote: <q data-source="ai">'+esc(t.quote)+'</q><br>Passage the model named: '+((t.passage.paragraph!=null&&t.passage.paragraph!=='')?'para. '+esc(t.passage.paragraph):'p. '+esc(t.passage.page_label))+' (PDF page '+t.passage.page+')<br>Nearest passage on that page: '+(n?((n.paragraph!=null&&n.paragraph!=='')?'para. '+esc(n.paragraph):'p. '+esc(n.page_label))+', longest shared run '+t.near.run+' word'+(t.near.run===1?'':'s')+': '+esc(String(n.text).slice(0,300))+'…':'none')+'</p><button type="button" data-open="'+esc(d.id)+'" data-page="'+t.passage.page+'" aria-label="Open '+esc(d.id)+' at PDF page '+t.passage.page+'">Open the PDF page</button></div>';
  }).join('')+'</section>';
  return h;
}
function sourcePrompt(ok,cite,rg){
  const d=ing.doc;
  return 'You are writing the source page for a document newly read into a research wiki. Use only the verified takeaways below. Each carries a ready-made pin; copy pins exactly and use no other pin.\n\nDOCUMENT: '+d.title+' | author: '+(d.author||'n/a')+' | published: '+(d.published||d.year)+' | pages: '+d.pages+' | url: '+d.url+'\nCITE AS: '+cite+' | REGISTER: ('+(rg.join('')||'?')+')\nANATOMY of a source page, as headings: Full cite, Register, One-liner, Key takeaways, How NOT to read this, Where it feeds the wiki, Related. Link pages as [[slug]] using slugs from the index'+(ing.newSlugs.size?' or these new slugs: '+[...ing.newSlugs].join(', '):'')+'.\n\nINDEX:\n'+indexTxt+'\n\nTAKEAWAYS:\n'+JSON.stringify(ok.map(t=>({claim:t.claim,pin:t.pin,pages:t.pages})))+'\n\nReturn JSON only: {"one_liner":"...","body":"markdown","touches":[{"slug":"...","why":"..."}]}. Body at most 900 words, only the pins given, copied exactly. Quote only words that stand in the passages given; the code will check.';
}
async function ingDraftSource(){
  if(ing.running||ing.src||!ing.verified)return;
  const d=ing.doc,ok=ing.items.filter(t=>t.ok),stub=stubFor(d),rg=stub?stub.frontmatter.register.slice():[],cite=citeAs(d);
  const run=ing.run={stop:false};ing.running=true;renderIngest();
  $('ing-progress').textContent='Drafting the source page (1 call)…';
  const data=await askJSON(sourcePrompt(ok,cite,rg),0,$('ing-fail'),'Source page',run);
  ing.running=false;ing.run=null;
  if(!data){renderIngest();return;}
  const ml=S.modelLog[S.modelLog.length-1];ml.kind='source';
  const base=slugify(d.id);let slug=base;if(bySlug[slug])slug=base+'-source';for(let n=2;bySlug[slug];n++)slug=base+'-source-'+n;
  const title=(d.symbol?d.symbol+': ':'')+(d.short_title||d.title);
  let body=fixMarks(String(data.body||'')).trim();if(!/^#\s/.test(body))body='# '+title+'\n\n'+body;
  const touches=[];
  (Array.isArray(data.touches)?data.touches:[]).forEach(t=>{
    const s=String((t&&t.slug)||'').trim();if(!s||touches.some(x=>x.slug===s))return;
    if(bySlug[s]||ing.newSlugs.has(s))touches.push({slug:s,why:String((t&&t.why)||'')});else ml.badSlugs.push(s);
  });
  if(stub&&!touches.some(x=>x.slug===stub.slug))touches.unshift({slug:stub.slug,why:'the stub for this report, with its checklist'});
  const kept=touches.slice(0,12);
  if(stub&&!kept.some(x=>x.slug===stub.slug)){kept.pop();kept.unshift({slug:stub.slug,why:'the stub for this report, with its checklist'});}
  const miss=kept.filter(t=>body.indexOf('[['+t.slug+']]')<0);
  if(miss.length)body+='\n\n## Pages this feeds\n\n'+miss.map(t=>'- [['+t.slug+']]'+(t.why?' — '+t.why:'')).join('\n')+'\n';
  const sp=parsePins(body);
  ing.src={slug:slug,title:title,one:String(data.one_liner||'').trim(),touches:kept,stub:stub,change:{slug:slug,title:title,type:'source',kind:'new',isSource:true,one:String(data.one_liner||'').trim()||null,body:body,marked:'\u0001INS\n'+body+'\n\u0001END',paras:body.split(/\n\s*\n/).filter(s=>s.trim()).length,pinOk:sp.filter(x=>verify(x).ok).length,pinBad:sp.filter(x=>!verify(x).ok).length,notes:ml.badSlugs.length?['Slugs not in the wiki were dropped: '+ml.badSlugs.join(', ')]:[],tags:kept.map(t=>t.slug),register:rg,contested:[],decision:null}};
  ing.jobs=kept.map(t=>({slug:t.slug,why:t.why,status:'waiting',change:null}));
  $('ing-progress').textContent='Source page drafted.';
  renderIngest();renderChecks();
}
function touchPrompt(j){
  const ex=bySlug[j.slug],tk=ing.items.filter(t=>t.ok&&t.pages.includes(j.slug)),stub=ex&&ex.frontmatter.status==='stub';
  return 'You are adding what a newly read document says to one page of a research wiki.\n\n'+(ex?'PAGE ['+j.slug+'], current body:\n'+ex.body+'\n\n':'PAGE ['+j.slug+'] does not exist yet. Write its content as edits with "after": "end".\n\n')+(stub?'This page is a stub. Its checklist says what the ingest should check. Answer each checklist item you can, from the takeaways only, and say plainly which you cannot.\n\n':'')+'WHY THIS PAGE IS TOUCHED: '+j.why+'\n\nTAKEAWAYS, each with its ready-made pin:\n'+JSON.stringify(tk.map(t=>({claim:t.claim,pin:t.pin})))+'\n\nReturn JSON only: {"edits":[{"after":"<an existing heading of the page, or end>","markdown":"..."}],"contested":"..."}. At most '+(stub?600:300)+' words in all. Copy pins exactly as given; quote only words that stand in the passages given; the code will check. Keep the document’s own verbs; never present a report as what the treaty requires. "contested" is a full block (lines claim:, verdict:, note:, then one line per position: sign + or - or ~, register letter | pin | gloss | [[slug]]) only where this document disagrees with the page; otherwise an empty string.';
}
function insertAfter(body,after,mdText,marked){
  const ins=marked?'\u0001INS\n'+mdText.trim()+'\n\u0001END':mdText.trim(),lines=body.split('\n');
  let at=lines.length,note=null;
  if(after&&String(after).toLowerCase()!=='end'){
    const want=norm(String(after).replace(/^#+\s*/,'')).toLowerCase();let hi=-1,lvl=0;
    for(let i=0;i<lines.length&&hi<0;i++){const m=lines[i].match(/^(#{1,6})\s+(.*)$/);if(m&&norm(m[2]).toLowerCase()===want){hi=i;lvl=m[1].length;}}
    if(hi<0)note='Heading “'+after+'” was not found: the text was inserted at the end of the page.';
    else{for(let j=hi+1;j<lines.length;j++){const m=lines[j].match(/^(#{1,6})\s/);if(m&&m[1].length<=lvl){at=j;break;}}}
  }
  lines.splice(at,0,'',ins,'');
  return {body:lines.join('\n'),note:note};
}
function makeChange(j,data){
  const ex=bySlug[j.slug],stub=!!(ex&&ex.frontmatter.status==='stub');
  const edits=(Array.isArray(data.edits)?data.edits:[]).map(e=>({after:String((e&&e.after)||'end'),md:fixMarks(String((e&&e.markdown)||'').trim())})).filter(e=>e.md);
  if(stub)edits.push({after:'end',md:'Source page: [['+ing.src.slug+']].'});
  let cont=String(data.contested||'').trim();const contested=[];
  if(cont){
    if(!/^`{3}/.test(cont))cont=FENCE+'contested\n'+cont+'\n'+FENCE;
    cont=fixMarks(cont);edits.push({after:'end',md:cont});
    contested.push(cont.replace(/^`{3}\w*\n/,'').replace(/\n`{3}\s*$/,''));
  }
  const title=ex?ex.title:titleOf(j.slug);
  let plainB=ex?ex.body:'# '+title+'\n',markedB=plainB;const notes=[];
  edits.forEach(e=>{const a=insertAfter(plainB,e.after,e.md,false),b=insertAfter(markedB,e.after,e.md,true);plainB=a.body;markedB=b.body;if(a.note&&!notes.includes(a.note))notes.push(a.note);});
  const ins=edits.map(e=>e.md),ps=parsePins(ins.join('\n'));
  j.change={slug:j.slug,title:title,type:ex?ex.type:'concept',kind:ex?'edited':'new',isSource:false,wasStub:stub,body:plainB,marked:markedB,paras:ins.join('\n\n').split(/\n\s*\n/).filter(s=>s.trim()).length,pinOk:ps.filter(x=>verify(x).ok).length,pinBad:ps.filter(x=>!verify(x).ok).length,notes:notes,tags:[],register:[],contested:contested,one:plain(ins[0]||'').slice(0,160),decision:null};
}
async function ingDraftPages(){
  if(ing.running||!ing.src)return;
  const run=ing.run={stop:false};ing.running=true;renderIngest();
  for(const j of ing.jobs){
    if(j.status==='done')continue;if(run.stop)break;
    j.status='running';
    $('ing-progress').textContent='Drafting '+j.slug+': '+(ing.jobs.filter(x=>x.status==='done').length+1)+' of '+ing.jobs.length+' pages…';
    renderIngest();
    const data=await askJSON(touchPrompt(j),0,$('ing-fail'),'Page '+j.slug,run);
    if(!data){j.status=run.stop?'stopped':'failed';break;}
    S.modelLog[S.modelLog.length-1].kind='page';
    makeChange(j,data);j.status='done';renderIngest();renderChecks();
  }
  ing.running=false;ing.run=null;
  $('ing-progress').textContent=ing.jobs.filter(j=>j.status==='done').length+' of '+ing.jobs.length+' page drafts done.';
  renderIngest();
}
function stepDraft(d){
  let h='<h3>Step 3. Drafts</h3>';
  if(!ing.src){
    return h+'<div class="gray">'+ing.verified+' verified takeaways will be sent (claims and ready-made pins; no passage text). The model writes a draft; nothing enters the wiki before you approve it.</div><p><button type="button" class="primary" data-act="ing-src"'+((ing.running||!ing.verified)?' disabled':'')+'>Draft the source page (1 call)</button></p>';
  }
  const left=ing.jobs.filter(j=>j.status!=='done').length;
  h+='<p>Source page drafted: <strong data-source="ai">'+esc(ing.src.title)+'</strong> (slug '+esc(ing.src.slug)+'). It names '+ing.src.touches.length+' page'+(ing.src.touches.length===1?'':'s')+' to change; the stub is always among them.</p>';
  h+='<table><caption>Pages to be changed</caption><thead><tr><th scope="col">Page</th><th scope="col">Why</th><th scope="col">State</th></tr></thead><tbody>'+ing.jobs.map(j=>'<tr><td>'+esc(j.slug)+(bySlug[j.slug]?'':' <span class="badge">new page</span>')+'</td><td data-source="ai">'+esc(j.why)+'</td><td>'+esc(j.status)+'</td></tr>').join('')+'</tbody></table>';
  h+='<p>'+(ing.running?'<button type="button" data-act="stop">Stop (keeps what has returned)</button>':(left?'<button type="button" class="primary" data-act="ing-pages">'+(left===ing.jobs.length?'Draft the changes to '+left+' page'+(left===1?'':'s')+' ('+left+' call'+(left===1?'':'s')+')':'Resume: '+left+' page'+(left===1?'':'s')+' left')+'</button> ':'')+(ing.jobs.some(j=>j.change)?'<button type="button" class="primary" data-act="ing-review">Review the changes (step 4)</button>':''))+'</p>';
  return h;
}
function renderReview(){
  const ch=ing.changes;
  if(ing.filed){
    return '<h3>Step 4. Filed</h3><p class="pass" aria-live="polite">The approved changes are written. '+ch.filter(c=>c.decision==='approved').length+' page(s) filed, '+ch.filter(c=>c.decision==='rejected').length+' rejected and left exactly as loaded.</p>'+baTable()+'<p><button type="button" class="primary" data-act="dl-json">Download the wiki</button></p>';
  }
  if(!ch.length)return '<h3>Step 4. Review and file</h3><p>No drafts to review yet.</p>';
  let h='<h3>Step 4. Review and file</h3>';
  if(ing.rv<ch.length){
    const c=ch[ing.rv],n=ing.rv+1;
    h+='<p class="line" aria-live="polite">change '+n+' of '+ch.length+'</p><fieldset class="chg"><legend>Change '+n+' of '+ch.length+': '+esc(c.title)+' ('+esc(c.type)+')</legend>'+
      '<p><span class="badge">'+(c.kind==='new'?'new page':'edited')+'</span> '+c.paras+' paragraph'+(c.paras===1?'':'s')+' inserted · pins added: '+c.pinOk+' verified, '+c.pinBad+' not verified'+(c.decision?' · your decision: <strong>'+c.decision+'</strong>':'')+'</p>'+
      (c.pinBad?'<p class="warn">Some pins in this draft did not verify. They are shown as not found and marked ⚠.</p>':'')+(c.notes.length?'<p class="warn">'+c.notes.map(esc).join(' ')+'</p>':'')+
      '<div class="review" data-source="ai">'+md(c.marked,{slug:c.slug})+'</div>'+
      '<p>'+(ing.rv>0?'<button type="button" data-act="ing-jump" data-i="'+(ing.rv-1)+'">Previous change</button> ':'')+'<button type="button" class="primary" data-act="ing-approve" aria-label="Approve change '+n+' of '+ch.length+': '+esc(c.title)+'">Approve this page</button> <button type="button" data-act="ing-reject" aria-label="Reject change '+n+' of '+ch.length+': '+esc(c.title)+'">Reject this page</button></p></fieldset>';
  }
  const und=ch.filter(c=>!c.decision).length,ap=ch.filter(c=>c.decision==='approved').length;
  h+='<h4>Decisions so far</h4><ul>'+ch.map((c,i)=>'<li>'+esc(c.title)+': '+(c.decision||'undecided')+' <button type="button" data-act="ing-jump" data-i="'+i+'" aria-label="Go to change '+(i+1)+' of '+ch.length+': '+esc(c.title)+'">Go to change '+(i+1)+'</button></li>').join('')+'</ul>';
  h+='<p><button type="button" class="primary" data-act="ing-file"'+((und||!ap)?' disabled':'')+'>File the approved changes ('+ap+')</button> <span class="note">'+(und?und+' change'+(und===1?'':'s')+' still undecided. Nothing is written until every change has a decision and you press the button.':(!ap?'Nothing is approved, so there is nothing to file.':'Approved pages are written at once; rejected pages stay exactly as loaded.'))+'</span></p>';
  return h;
}
function renderIngest(){
  const el=$('ing-body'),d=ing.doc;
  let h='<h2>Ingest a waiting document</h2>';
  if(!d){
    el.innerHTML=h+(docs.some(x=>x.status==='inbox')?'<p>Use an “Ingest” button under the page list. Nothing is sent until you press Start.</p>':'<p>No document is waiting in the inbox, so there is nothing to ingest.</p>');
    return;
  }
  const names=['Scope','Takeaways','Drafts','Review and file'];
  h+='<p class="note">Ingesting <strong>'+esc(d.symbol||d.short_title)+'</strong> ('+esc(d.short_title||d.title)+', '+esc(d.kind)+', '+esc(d.year)+'). A language model drafts, this page verifies every quotation, and you approve each page before anything is written.</p>';
  h+='<ol class="steps" aria-label="Ingest steps">'+names.map((n,i)=>'<li'+(ing.step===i+1?' class="cur" aria-current="step"':'')+'>'+(i+1)+'. '+n+'</li>').join('')+'</ol>';
  h+='<p class="line" aria-live="polite">calls so far '+S.calls+' · passages sent '+S.passages+'</p>';
  h+=ing.step===1?stepScope(d):(ing.step===2?stepTake(d):(ing.step===3?stepDraft(d):renderReview()));
  if(!ing.filed)h+='<p><button type="button" data-act="ing-reset"'+(ing.running?' disabled':'')+'>Start over with this document</button></p>';
  el.innerHTML=h;
}
function finalFm(c,srcSlug,apSlugs){
  const old=c.kind==='new'?{title:c.title,type:c.type,tags:c.tags||[],register:c.register||[],links:[],sources:[],status:'draft'}:JSON.parse(JSON.stringify(bySlug[c.slug].frontmatter));
  old.links=old.links||[];old.sources=old.sources||[];old.register=old.register||[];
  const ids=uniq(parsePins(c.body).map(x=>x.id));
  let links=old.links.concat([...c.body.matchAll(/\[\[([^\]|#]+)/g)].map(m=>m[1].trim()));
  if(c.isSource)links=links.concat(apSlugs.filter(s=>s!==c.slug));else if(srcSlug)links.push(srcSlug);
  old.links=uniq(links).filter(s=>s!==c.slug&&bySlug[s]);
  old.sources=uniq(old.sources.concat(ids));
  old.register=uniq(old.register.concat(ids.flatMap(id=>docReg(id).split('').filter(x=>x!=='?')))).sort();
  if(c.kind==='new'||old.status==='stub')old.status='draft';
  old.updated=today;return old;
}
function fileIngest(){
  const ch=ing.changes,ap=ch.filter(c=>c.decision==='approved'),rj=ch.filter(c=>c.decision==='rejected'),d=ing.doc;
  if(!ap.length||ch.some(c=>!c.decision)||ing.filed)return;
  const before=countLint(),srcAp=ap.find(c=>c.isSource),apSlugs=ap.map(c=>c.slug);
  ap.forEach(c=>{
    if(c.kind==='new')pages.push({slug:c.slug,type:c.type,title:c.title,frontmatter:{title:c.title,type:c.type,tags:c.tags||[],register:c.register||[],links:[],sources:c.isSource?[d.id]:[],status:'draft',updated:today},body:c.body});
    else bySlug[c.slug].body=c.body;
  });
  d.status='ingested';ingestingId=null;reindex();
  ap.forEach(c=>{bySlug[c.slug].frontmatter=finalFm(c,srcAp?srcAp.slug:null,apSlugs);});
  reindex();
  ap.forEach(c=>{
    const p=bySlug[c.slug],has=indexEntries().find(e=>e.slug===c.slug),n=p.pins.filter(x=>verify(x).ok).length;
    if(c.kind==='new')indexInsert(c.isSource?/^#+\s*Sources?/i:/^#+\s*Concepts?/i,lineFor(c.slug,c.one||null),c.isSource?'Sources':'Concepts');
    else if(has&&c.wasStub)indexTxt=indexTxt.split('\n').map(l=>l===has.line?lineFor(c.slug,null):l).join('\n');
    else if(has)indexTxt=indexTxt.split('\n').map(l=>l===has.line?(/✓\s*\d+/.test(l)?l.replace(/✓\s*\d+/,'✓'+n):l+' · ✓'+n):l).join('\n');
    else indexInsert(new RegExp('^#+\\s*'+(p.type==='entity'?'Entit':p.type==='question'?'Question':'Concept')),lineFor(c.slug,null),titleOf(p.type)+'s');
  });
  rebuildIndexHead();
  ap.forEach(c=>(c.contested||[]).forEach(b=>{
    const cc=parseContested(b),key=slugify(cc.claim.split(/\s+/).slice(0,8).join(' '))||('claim-'+c.slug);
    const stt=/^leans/.test(cc.verdict)?'leaning':(/^settled/.test(cc.verdict)?'settled':'open');
    const pole=sg=>cc.pos.filter(p=>p.sign===sg).map(p=>p.gloss).join('; ')||'none';
    tensTxt=tensTxt.replace(/\s*$/,'')+'\n\n### '+key+'\ntitle: '+cc.claim+'\nstatus: '+stt+'\ncard: [['+c.slug+']]\npoles: supports: '+pole('+')+' / contests: '+pole('-')+' / mixed: '+pole('~')+'\nwhere: '+cc.pos.map(p=>(parsePins(p.pin)[0]||{}).label).filter(Boolean).join('; ')+'\n';
    S.sessTens.add(key);
  }));
  const pinsAll=pages.reduce((a,p)=>a+p.pins.filter(x=>x.id===d.id&&verify(x).ok).length,0);
  const onPages=pages.filter(p=>p.pins.some(x=>x.id===d.id)&&!(srcAp&&p.slug===srcAp.slug)).map(p=>p.slug);
  const subject=(d.symbol||d.id)+': '+(d.short_title||d.title);
  addLog('ingest',subject,'Read '+d.passages.length+' passages ('+citeAs(d)+', register ('+docReg(d.id)+')). '+(srcAp?'Wrote [['+srcAp.slug+']]. ':'No source page was filed. ')+pinsAll+' pins in all; besides its own page, pinned on '+onPages.length+' pages: '+(onPages.map(s=>'[['+s+']]').join(', ')||'none')+'. Approved: '+apSlugs.map(s=>'[['+s+']]').join(', ')+'. Rejected: '+(rj.length?rj.map(c=>'[['+c.slug+']]').join(', '):'none')+'.');
  S.ops.push({kind:'ingest',date:today,subject:subject,pages:apSlugs,rejected:rj.map(c=>c.slug)});
  S.lastFiling={pages:apSlugs,before:before,after:countLint()};
  ing.filed=true;ing.step=4;
  refresh();renderIngest();renderIngButtons();flash('Filed '+ap.length+' page'+(ap.length===1?'':'s')+' from '+(d.symbol||d.id)+'.');
}
function decide(v){
  const c=ing.changes[ing.rv];if(!c)return;
  c.decision=v;ing.rv=(ing.rv<ing.changes.length-1)?ing.rv+1:ing.changes.length;
  renderIngest();renderChecks();
}

/* ---------- events ---------- */
function openSrc(id,page){
  if(window.studio&&typeof studio.openSource==='function')studio.openSource(id,page);
  else flash('The source viewer is not available here.');
}
const ACT={
  'dl-json':dlJSON,'dl-md':dlMd,
  'lint-now':()=>{setView('lint');},
  'lint-rerun':()=>{renderLint();renderChecks();flash('Lint re-run.');},
  'log-flip':()=>{S.order=S.order==='new'?'old':'new';renderLog();},
  'copy-page':()=>{const p=bySlug[S.cur];if(p)copyText(yaml(p.frontmatter)+p.body,'Page copied as markdown.');},
  'ask-go':askStep1,'ask-step2':askStep2,
  'ask-change':()=>{A.changing=!A.changing;renderAskPages();},
  'ask-again':()=>{A.step=0;A.ans=null;A.chosen=[];A.changing=false;A.filed=false;$('ask-answer').innerHTML='';$('ask-pages').innerHTML='';$('ask-progress').textContent='';askAnnounce();$('ask-q').focus();},
  'ask-file':fileQuestion,
  'ask-copy':()=>{if(A.ans)copyText(A.ans.title+'\n\n'+A.ans.answer+'\n\nWhat the library cannot answer: '+A.ans.cannot,'Answer copied.');},
  'stop':stopAll,
  'ing-pick':t=>ingSelect(t.dataset.id),
  'ing-start':ingStart,
  'ing-to':t=>{ing.step=+t.dataset.step;renderIngest();},
  'ing-src':ingDraftSource,'ing-pages':ingDraftPages,
  'ing-review':()=>{ing.changes=[ing.src.change].concat(ing.jobs.filter(j=>j.change).map(j=>j.change));ing.step=4;ing.rv=0;renderIngest();},
  'ing-approve':()=>decide('approved'),'ing-reject':()=>decide('rejected'),
  'ing-jump':t=>{ing.rv=+t.dataset.i;renderIngest();},
  'ing-file':fileIngest,
  'ing-reset':()=>{if(!ing.running){ingReset();renderIngest();renderIngButtons();renderChecks();}}
};
document.addEventListener('click',function(e){
  const t=e.target.closest?e.target.closest('[data-open],[data-exp],[data-go],[data-view],[data-act]'):null;
  if(!t)return;
  if(t.dataset.go){e.preventDefault();go(t.dataset.go);return;}
  if(t.dataset.open){openSrc(t.dataset.open,+t.dataset.page);return;}
  if(t.dataset.exp){const pd=t.parentElement.querySelector('.pd');if(pd){pd.hidden=!pd.hidden;t.setAttribute('aria-expanded',String(!pd.hidden));}return;}
  if(t.dataset.view){e.preventDefault();setView(t.dataset.view);return;}
  if(t.dataset.act&&ACT[t.dataset.act])ACT[t.dataset.act](t,e);
});
document.addEventListener('change',function(e){
  const t=e.target;
  if(t.matches&&t.matches('[data-pick]')){
    const s=t.dataset.pick;
    if(t.checked){if(A.chosen.length>=5){t.checked=false;flash('At most 5 pages can be sent.');return;}A.chosen.push(s);}
    else A.chosen=A.chosen.filter(x=>x!==s);
    askAnnounce();
  }
});
document.addEventListener('input',function(e){if(e.target.id==='ask-tags')A.tags=e.target.value;});
document.addEventListener('keydown',function(e){if(e.key==='Escape'&&(A.busy||ing.running||S.pending))stopAll();});
$('ask-q').addEventListener('keydown',function(e){if(e.key==='Enter'&&!e.shiftKey){e.preventDefault();askStep1();}});
$('ask-q').addEventListener('input',askAnnounce);
$('flt').addEventListener('input',renderSidebar);
window.addEventListener('hashchange',function(){const s=decodeURIComponent(location.hash.slice(1));if(bySlug[s]&&(s!==S.cur||S.view!=='page'))go(s);});
function refresh(){
  renderHeader();renderSidebar();
  if(S.view==='page')renderPage();if(S.view==='log')renderLog();if(S.view==='tensions')renderTens();if(S.view==='lint')renderLint();
  renderChecks();
}

/* ---------- start ---------- */
if(!pages.length){
  $('v-page').innerHTML='<p class="warn">No wiki is attached to this app, so there is nothing to show. Attach the research wiki and the library from “Your files”.</p>';
  $('sub').textContent='No data.';
}else{
  reindex();
  baseWarn=pages.reduce((a,p)=>a+p.pins.filter(x=>x.mark==='⚠').length,0);
  const h=decodeURIComponent((location.hash||'').slice(1));
  S.cur=bySlug[h]?h:pages[0].slug;
  $('foot').textContent='Source: '+(WIKI.source||'the attached research wiki')+' · built '+(WIKI.built||'unknown')+'. Counting, matching and verification are done by this page’s code; the model is called only when you press Ask, Ingest or a retry button.';
  renderIngButtons();renderHeader();renderSidebar();setView('page');renderChecks();askAnnounce();
  $('flt').focus();
}
})();
</script>
</body>
</html>
```
