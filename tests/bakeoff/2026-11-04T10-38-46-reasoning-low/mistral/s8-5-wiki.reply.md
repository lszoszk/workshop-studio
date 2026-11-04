I built the full five-tab wiki workspace: page reader with verified pin chips and contested cards, the Ask flow with announced model calls and filing, the four-step ingest stepper with per-change approval, the lint panel, and the record/download tab — all verification done by the page's own code against the library.html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Research wiki workspace · neurotechnology and justice</title>
<style>
:root{--paper:#f4f0e8;--ink:#1d1b18;--rule:#d9d2c3;--red:#9b2335;--green:#2f6b40;--amber:#8f6400;--grey:#77726a;--yellow:#f6e9c4}
*{box-sizing:border-box}
[hidden]{display:none!important}
html,body{margin:0}
body{background:var(--paper);color:var(--ink);font:16px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
.mono{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:11.5px;letter-spacing:.09em;text-transform:uppercase}
header{display:flex;justify-content:space-between;gap:24px;align-items:flex-end;padding:16px 24px 12px;border-bottom:1px solid var(--rule);flex-wrap:wrap}
header h1{font-family:Georgia,"Times New Roman",serif;font-weight:400;font-size:26px;margin:4px 0 6px}
.meta{color:var(--grey);font-size:13.5px}
.hdr-right{text-align:right;color:var(--grey)}
.dim{color:var(--grey)} .note{color:var(--grey);font-size:13.5px}
a{color:var(--red)}
button{font:inherit;color:inherit}
:focus-visible{outline:3px solid var(--red);outline-offset:2px}
nav[role=tablist]{display:flex;gap:2px;padding:0 24px;border-bottom:1px solid var(--rule);flex-wrap:wrap}
nav[role=tablist] [role=tab]{background:none;border:none;border-bottom:3px solid transparent;padding:10px 14px;cursor:pointer;font-family:ui-monospace,Menlo,Consolas,monospace;font-size:12px;letter-spacing:.09em;text-transform:uppercase;color:var(--grey)}
nav[role=tablist] [role=tab][aria-selected=true]{color:var(--red);border-bottom-color:var(--red)}
nav[role=tablist] .run{color:var(--red)}
main{padding:20px 24px 48px;max-width:1300px}
h2{font-family:Georgia,"Times New Roman",serif;font-weight:400;font-size:24px;margin:0 0 10px}
h3{font-family:Georgia,"Times New Roman",serif;font-weight:400;font-size:19px;margin:22px 0 8px}
h4{font-size:16px;margin:16px 0 6px}
.bignum{font-family:Georgia,"Times New Roman",serif;font-size:52px;line-height:1.05}
.btn{border:1px solid var(--ink);background:transparent;padding:6px 14px;cursor:pointer;border-radius:2px}
.btn:hover{border-color:var(--red);color:var(--red)}
.btn.primary{background:var(--red);border-color:var(--red);color:#fff}
.btn.primary:hover{color:#fff;opacity:.9}
.btn[disabled]{opacity:.45;cursor:not-allowed}
.chip{display:inline-block;border:1px solid var(--rule);border-radius:999px;padding:0 8px;margin:1px 2px;font-family:ui-monospace,Menlo,Consolas,monospace;font-size:11px;letter-spacing:.04em;background:transparent;cursor:pointer;vertical-align:middle}
.chip:hover{border-color:var(--red);color:var(--red)}
.chip.reg{cursor:default;color:var(--grey)}
.pin-quote{font-style:italic}
.pin .pin-detail{display:block;border-left:2px solid var(--rule);margin:4px 0 8px 18px;padding:4px 10px;color:var(--grey);font-size:14px}
.pin.struck .pin-quote,.pin.struck .chip{text-decoration:line-through}
.ok{color:var(--green)} .warn{color:var(--amber)} .bad{color:var(--red)}
table{border-collapse:collapse;width:100%;margin:10px 0;font-size:14.5px}
caption{text-align:left;font-family:ui-monospace,Menlo,Consolas,monospace;font-size:11.5px;letter-spacing:.09em;text-transform:uppercase;color:var(--grey);padding:4px 0}
th{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:11px;letter-spacing:.08em;text-transform:uppercase;text-align:left;color:var(--grey);font-weight:400;border-bottom:1px solid var(--ink);padding:4px 8px 4px 0}
td{border-bottom:1px solid var(--rule);padding:6px 8px 6px 0;vertical-align:top}
td.num,th.num{text-align:right;font-variant-numeric:tabular-nums}
.contested{border:1px solid var(--rule);border-left:3px solid var(--red);padding:12px 16px;margin:16px 0}
.verdict{font-family:Georgia,"Times New Roman",serif;font-size:30px;margin:2px 0 6px}
.lean{height:10px;background:var(--rule);margin:6px 0 12px;max-width:420px}
.lean>div{height:100%;background:var(--red)}
.fig{color:var(--grey);margin:8px 0 2px;font-family:ui-monospace,Menlo,Consolas,monospace;font-size:11.5px;letter-spacing:.09em;text-transform:uppercase}
.layout{display:flex;gap:28px;align-items:flex-start}
.rail{width:320px;flex:none}
.content{flex:1;max-width:900px;min-width:0}
@media(max-width:900px){.layout{flex-direction:column}.rail{width:100%}}
input[type=text],textarea{width:100%;border:1px solid var(--rule);background:#fff;padding:8px 10px;font:inherit;color:var(--ink)}
textarea{min-height:110px}
label{display:block;font-family:ui-monospace,Menlo,Consolas,monospace;font-size:11.5px;letter-spacing:.09em;text-transform:uppercase;color:var(--grey);margin:12px 0 4px}
.badge{display:inline-block;border:1px solid var(--rule);border-radius:2px;padding:1px 7px;margin:0 4px 4px 0;font-family:ui-monospace,Menlo,Consolas,monospace;font-size:11px;letter-spacing:.05em}
.badge.stub{border-color:var(--red);color:var(--red)}
.tag{color:var(--grey);font-size:13px;margin-right:8px}
.pagelist button{display:block;width:100%;text-align:left;background:none;border:none;border-bottom:1px solid var(--rule);padding:7px 4px;cursor:pointer;font:inherit}
.pagelist button:hover{color:var(--red)}
.pagelist button.sel{color:var(--red);border-left:3px solid var(--red);padding-left:8px}
.pagelist .cnt{float:right;color:var(--grey);font-family:ui-monospace,Menlo,Consolas,monospace;font-size:11px}
.grouplabel{color:var(--grey);margin:14px 0 4px}
.card{border:1px solid var(--rule);padding:14px 18px;margin:14px 0}
fieldset.card{border:1px solid var(--ink)}
legend{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:12px;letter-spacing:.08em;text-transform:uppercase;padding:0 8px}
pre{background:#ece7db;padding:10px;overflow:auto;font-size:13px}
.ins{background:var(--yellow);border-left:3px solid var(--red);padding-left:8px}
.diff .old{color:#8d887e}
.progress{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:12px;color:var(--red);margin:8px 0}
.greybox{border:1px dashed var(--rule);background:#efe9dd;padding:10px 14px;color:var(--grey);font-size:14px;margin:10px 0}
footer{border-top:1px solid var(--rule);padding:10px 24px;color:var(--grey)}
details{margin:6px 0;border-bottom:1px solid var(--rule)}
summary{cursor:pointer;padding:6px 0;font-family:ui-monospace,Menlo,Consolas,monospace;font-size:12px;letter-spacing:.06em}
.session-tag{color:var(--red);border:1px solid var(--red);border-radius:999px;padding:0 7px;font-size:10.5px;margin-left:8px}
.step{border:1px solid var(--rule);margin:12px 0;padding:12px 16px}
.step h3{margin-top:0}
</style>
</head>
<body>
<header>
  <div>
    <div class="mono">WIKI · neurotechnology and justice</div>
    <h1>Research wiki: neurotechnology in the administration of justice</h1>
    <div class="meta" id="hdr-meta"></div>
  </div>
  <div class="hdr-right">
    <div class="mono" id="hdr-counters" aria-live="polite"></div>
    <div class="mono dim">This page has no storage: changes live in it until you download them (tab 05)</div>
  </div>
</header>
<nav role="tablist" id="tabs" aria-label="App sections">
  <button role="tab" id="tabbtn-01" data-action="tab" data-tab="01" aria-selected="true" aria-controls="panel-01">01 Pages</button>
  <button role="tab" id="tabbtn-02" data-action="tab" data-tab="02" aria-selected="false" aria-controls="panel-02">02 Ask</button>
  <button role="tab" id="tabbtn-03" data-action="tab" data-tab="03" aria-selected="false" aria-controls="panel-03">03 Ingest</button>
  <button role="tab" id="tabbtn-04" data-action="tab" data-tab="04" aria-selected="false" aria-controls="panel-04">04 Check</button>
  <button role="tab" id="tabbtn-05" data-action="tab" data-tab="05" aria-selected="false" aria-controls="panel-05">05 Record</button>
</nav>
<main>
  <section role="tabpanel" id="panel-01" aria-labelledby="tabbtn-01"></section>
  <section role="tabpanel" id="panel-02" aria-labelledby="tabbtn-02" hidden>
    <h2>What does the wiki answer, and is it worth filing?</h2>
    <label for="ask-q">Your question</label>
    <textarea id="ask-q" placeholder="Ask the wiki… (Enter sends)"></textarea>
    <div style="margin:10px 0">
      <button class="btn primary" id="ask-btn" data-action="ask">Ask the wiki</button>
      <button class="btn" data-action="ask-stop" hidden>Stop</button>
    </div>
    <div class="greybox" id="ask-info">Step 1 will send the index and your question; step 2 the chosen pages' bodies. Nothing leaves the browser until you press Ask the wiki.</div>
    <div class="progress" id="ask-prog" aria-live="polite"></div>
    <div id="ask-out"></div>
  </section>
  <section role="tabpanel" id="panel-03" aria-labelledby="tabbtn-03" hidden></section>
  <section role="tabpanel" id="panel-04" aria-labelledby="tabbtn-04" hidden></section>
  <section role="tabpanel" id="panel-05" aria-labelledby="tabbtn-05" hidden></section>
</main>
<footer class="mono" id="foot"></footer>
<script>
'use strict';
const W=WORKSHOP_DATA.wiki, L=WORKSHOP_DATA.library;
const P=W.pages, D=L.records;
const bySlug={}, byId={};
P.forEach(p=>bySlug[p.slug]=p); D.forEach(d=>byId[d.id]=d);
const REG_NAMES={a:'treaty law',b:'General Comments',c:'UN, agency and soft-law reports',d:'national human rights institution',e:'civil society',f:'scholarship'};
const REG_W={a:5,b:4,c:3,d:2,e:1,f:0.5};
const PIN_RE=/\[([^\]]+)\]\(pin:([^#\s)]+)#p(\d+)(?: "([^"]*)")?\) ?(✓|⚠)/g;
const WLINK_RE=/\[\[([^\]|#]+)\]\]/g;
const $=s=>document.querySelector(s);
const esc=s=>String(s??'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
const today=()=>new Date().toISOString().slice(0,10);
const kebab=s=>String(s).toLowerCase().replace(/[^a-z0-9]+/g,'-').replace(/^-+|-+$/g,'')||'page';
function uniqueSlug(base){let s=base,n=2;while(bySlug[s])s=base+'-'+(n++);return s;}
function prep(p){p._links=[...p.body.matchAll(WLINK_RE)].map(m=>m[1]);p._pins=[...p.body.matchAll(PIN_RE)].map(m=>({label:m[1],id:m[2],page:+m[3],quote:m[4]||'',mark:m[5]}));}
P.forEach(prep);
const backlinks={};P.forEach(p=>p._links.forEach(s=>{(backlinks[s]=backlinks[s]||[]).push(p.slug);}));
function norm(s){return String(s??'').normalize('NFKC').replace(/[“”„]/g,'"').replace(/[‘’]/g,"'").replace(/[–—]/g,'-').replace(/\u00AD/g,'').replace(/-\s+/g,'-').replace(/\s+/g,' ').trim();}
const vcache=new Map();
function verify(pin){
  const key=pin.id+'|'+pin.page+'|'+pin.quote+'|'+pin.label;
  if(vcache.has(key))return vcache.get(key);
  let res;
  if(!pin.quote)res={ok:false,reason:'no quote in the pin'};
  else{const d=byId[pin.id];
    if(!d)res={ok:false,reason:'unknown document'};
    else if(d.status==='inbox')res={ok:false,reason:'document is still in the inbox'};
    else{const x=d.passages.find(p=>p.page===pin.page);
      if(!x)res={ok:false,reason:'no passage starts on PDF page '+pin.page};
      else{const frags=pin.quote.split(/…|\.\.\./).map(norm).filter(Boolean);const t=norm(x.text);let pos=0,ok=true;
        for(const f of frags){const i=t.indexOf(f,pos);if(i<0){ok=false;break;}pos=i+f.length;}
        if(!ok)res={ok:false,reason:'quote not found on that page',passage:x};
        else if(x.paragraph!=null&&!pin.label.includes('para. '+x.paragraph))res={ok:false,reason:'label does not match paragraph '+x.paragraph,passage:x};
        else if(x.paragraph==null&&!pin.label.includes('p. '+x.page_label))res={ok:false,reason:'label does not match page '+x.page_label,passage:x};
        else res={ok:true,passage:x};
      }}}
  vcache.set(key,res);return res;
}
const citeAs={};
D.forEach(d=>{const counts={};
  P.forEach(p=>p._pins.forEach(pn=>{if(pn.id===d.id){const b=pn.label.split(/, (?:para|p)\./)[0];counts[b]=(counts[b]||0)+1;}}));
  const best=Object.entries(counts).sort((a,b)=>b[1]-a[1])[0];
  citeAs[d.id]=best?best[0]:(d.symbol||(d.author+' '+d.year));});
function registerOfDoc(id){
  const src=P.find(p=>p.type==='source'&&p.frontmatter.sources.length===1&&p.frontmatter.sources[0]===id);
  const pg=src||P.find(p=>p.frontmatter.status==='stub'&&p.frontmatter.sources.length===1&&p.frontmatter.sources[0]===id)||P.find(p=>p.frontmatter.sources.length===1&&p.frontmatter.sources[0]===id);
  return pg?(pg.frontmatter.register||[]).join(''):'?';
}
function makePin(id,x,quote){
  const label=citeAs[id]+(x.paragraph!=null?', para. '+x.paragraph:', p. '+x.page_label);
  return '['+label+'](pin:'+id+'#p'+x.page+' "'+String(quote).replace(/"/g,'”')+'") ✓';
}
const S={tab:'01',page:null,changes:0,calls:0,passages:0,stop:false,changesList:[],logAdded:[],linted:false};
function renderCounters(){$('#hdr-counters').textContent='Changes this session: '+S.changes+' · Calls to the model: '+S.calls+' · Passages that left the browser: '+S.passages;}
function renderHeader(){
  const bt={};P.forEach(p=>bt[p.type]=(bt[p.type]||0)+1);
  const tp=P.reduce((n,p)=>n+p._pins.length,0), vp=P.reduce((n,p)=>n+p._pins.filter(pn=>verify(pn).ok).length,0);
  const inbox=D.filter(d=>d.status==='inbox').length;
  $('#hdr-meta').textContent=P.length+' pages ('+(bt.source||0)+' sources, '+(bt.concept||0)+' concepts, '+(bt.entity||0)+' entities, '+(bt.question||0)+' questions) · '+tp+' pins, '+vp+' verified by this page · '+D.length+' documents, '+inbox+' in the inbox · built '+W.built;
  renderCounters();
}
$('#foot').textContent=W.source+' · built '+W.built+' · Counting, matching and verification are done by this page\u2019s code; the model is called only when you press Ask, Ingest or a retry button.';
async function askModel(prompt,opts){
  opts=opts||{};S.calls++;S.passages+=opts.passages||0;renderCounters();
  let raw='';
  try{raw=await studio.ask(prompt,{json:true});}catch(e){return{error:String(e),raw:'',json:null};}
  const txt=String(raw).trim();let json=null;
  try{json=JSON.parse(txt);}catch(e){const m=txt.match(/```(?:json)?\s*([\s\S]*?)```/);if(m){try{json=JSON.parse(m[1]);}catch(e2){}}}
  return{raw:txt,json,error:json?null:'not JSON'};
}
const INLINE_RE=/\[([^\]]+)\]\(pin:([^#\s)]+)#p(\d+)(?: "([^"]*)")?\) ?(✓|⚠)|\[\[([^\]|#]+)\]\]|\[([^\]]+)\]\(([^\s)]+)\)|(\*\*[^*]+?\*\*)|(\*[^*\n]+?\*)/g;
function pinHtml(pin,opts){
  const v=verify(pin),reg=registerOfDoc(pin.id);
  const sent=!(opts&&opts.ai&&opts.sentPins)||opts.sentPins.has(pin.id+'#p'+pin.page+'|'+pin.quote);
  const markNote=(pin.mark==='✓')!==v.ok?' <span class="warn">page says '+pin.mark+'</span>':'';
  const verdict=v.ok?'<span class="ok">✓ verified</span>':'<span class="warn">⚠ not found'+(v.reason?' — '+esc(v.reason):'')+'</span>';
  const struck=(opts&&opts.ai&&!sent)?' struck':'';
  const notSent=(opts&&opts.ai&&!sent)?' <span class="bad">not on the pages sent</span>':'';
  const det=v.ok?((v.passage.paragraph!=null?'para. '+esc(v.passage.paragraph):'p. '+esc(v.passage.page_label))+' · '+esc(v.passage.text.slice(0,300))+(v.passage.text.length>300?'…':'')):esc(v.reason||'');
  return '<span class="pin'+struck+'"><span class="pin-quote">“'+esc(pin.quote)+'”</span> '+
    '<button class="chip" data-action="pin-open" data-id="'+esc(pin.id)+'" data-page="'+pin.page+'" data-quote="'+esc(pin.quote)+'" title="Open the PDF at this page with the quote marked">'+esc(pin.label)+'</button> '+
    '<span class="chip reg" title="register of the pinned document">'+esc(reg)+'</span> '+verdict+markNote+notSent+' '+
    '<button class="chip" data-action="pin-toggle" aria-expanded="false">details</button>'+
    '<span class="pin-detail" hidden>'+det+' <button class="chip" data-action="pin-open" data-id="'+esc(pin.id)+'" data-page="'+pin.page+'" data-quote="'+esc(pin.quote)+'">Open the PDF page</button></span></span>';
}
function inline(s,opts){
  return String(s).replace(INLINE_RE,(m,label,id,page,quote,mark,wslug,lt,lu,bold,ital)=>{
    if(label!==undefined)return pinHtml({label,id,page:+page,quote:quote||'',mark},opts);
    if(wslug!==undefined)return bySlug[wslug]?'<a href="#'+esc(wslug)+'" data-action="open-page" data-slug="'+esc(wslug)+'">'+esc(wslug)+'</a>':'<span class="bad">'+esc(wslug)+' (no page)</span>';
    if(lt!==undefined)return '<a href="'+esc(lu)+'" target="_blank" rel="noopener">'+esc(lt)+'</a>';
    if(bold)return '<strong>'+esc(bold.slice(2,-2))+'</strong>';
    if(ital)return '<em>'+esc(ital.slice(1,-1))+'</em>';
    return m;
  });
}
function parseContested(block){
  const o={positions:[]};
  block.split('\n').forEach(ln=>{
    if(ln.startsWith('claim:'))o.claim=ln.slice(6).trim();
    else if(ln.startsWith('verdict:'))o.verdict=ln.slice(8).trim();
    else if(ln.startsWith('note:'))o.note=ln.slice(5).trim();
    else if(/^[+~\-]\s*\|/.test(ln)){const parts=ln.split('|').map(x=>x.trim());const head=parts[0];o.positions.push({sign:head[0],register:head.slice(1).trim(),pin:parts[1]||'',gloss:parts[2]||'',page:parts[3]||''});}
  });
  return o;
}
function tensionsEntries(){return W.tensions.split(/(?=^### )/m).filter(s=>s.trim());}
function tensionsCards(){const s=new Set();tensionsEntries().forEach(e=>{const m=e.match(/card:\s*\[\[([^\]]+)\]\]/);if(m)s.add(m[1]);});return s;}
function contestedHtml(block,opts){
  const c=parseContested(block),verdict=(c.verdict||'').replace(/-/g,' ');
  let wsum=0,wsup=0;
  c.positions.forEach(p=>{const w=REG_W[p.register]??0;wsum+=w;if(p.sign==='+')wsup+=w;else if(p.sign==='~')wsup+=w/2;});
  const pct=wsum?Math.round(100*wsup/wsum):0;
  const rows=c.positions.map(p=>'<tr><td>'+(p.sign==='+'?'supports':p.sign==='-'?'contests':'mixed')+'</td><td class="mono">'+esc(p.register)+'</td><td>'+inline(p.pin,opts)+'</td><td>'+esc(p.gloss)+'</td><td>'+(p.page?inline(p.page,opts):'')+'</td></tr>').join('');
  const inT=opts&&opts.pageSlug&&tensionsCards().has(opts.pageSlug);
  return '<section class="contested"><h3>'+esc(c.claim||'Contested claim')+'</h3><p class="verdict">'+esc(verdict)+'</p>'+
    (c.note?'<p>'+esc(c.note)+'</p>':'')+
    '<div class="fig">FIG.01 · lean bar — descriptive: support '+pct+'% of weighted positions (weights a 5 · b 4 · c 3 · d 2 · e 1 · f ½); the verdict is the answer</div>'+
    '<div class="lean"><div style="width:'+pct+'%"></div></div>'+
    '<table><caption>Positions in this contested block</caption><thead><tr><th scope="col">sign</th><th scope="col">register</th><th scope="col">pin</th><th scope="col">gloss</th><th scope="col">page</th></tr></thead><tbody>'+rows+'</tbody></table>'+
    (inT?'<p class="note">Also <button class="btn" data-action="tab" data-tab="05" style="padding:0;border:none;text-decoration:underline">in the tensions register (tab 05)</button>.</p>':'')+'</section>';
}
function renderMd(body,opts){
  opts=opts||{};
  const mark=raw=>!opts.inserted?'':(opts.inserted.some(m=>m.includes(raw))?' class="ins"':' class="old"');
  const lines=String(body).split('\n');let html='',i=0,para=[];
  const flush=()=>{if(para.length){html+='<p'+mark(para.join(' '))+'>'+inline(para.join(' '),opts)+'</p>';para=[];}};
  while(i<lines.length){
    const ln=lines[i];
    if(ln.trim().startsWith('```')){
      flush();const info=ln.trim().slice(3);const buf=[];i++;
      while(i<lines.length&&!lines[i].trim().startsWith('```')){buf.push(lines[i]);i++;}
      i++;
      html+=info==='contested'?contestedHtml(buf.join('\n'),opts):'<pre>'+esc(buf.join('\n'))+'</pre>';
      continue;
    }
    const h=ln.match(/^(#{1,6})\s+(.*)$/);
    if(h){flush();const lvl=Math.min(h[1].length+1,6);html+='<h'+lvl+mark(ln)+'>'+inline(h[2],opts)+'</h'+lvl+'>';i++;continue;}
    if(/^\s*-\s+/.test(ln)){flush();let ul='';while(i<lines.length&&/^\s*-\s+/.test(lines[i])){const it=lines[i].replace(/^\s*-\s+/,'');ul+='<li'+mark(it)+'>'+inline(it,opts)+'</li>';i++;}html+='<ul>'+ul+'</ul>';continue;}
    if(/^\s*\d+\.\s+/.test(ln)){flush();let ol='';while(i<lines.length&&/^\s*\d+\.\s+/.test(lines[i])){const it=lines[i].replace(/^\s*\d+\.\s+/,'');ol+='<li'+mark(it)+'>'+inline(it,opts)+'</li>';i++;}html+='<ol>'+ol+'</ol>';continue;}
    if(ln.trim()===''){flush();i++;continue;}
    para.push(ln.trim());i++;
  }
  flush();return html;
}
function linkSlug(s){return bySlug[s]?'<a href="#'+esc(s)+'" data-action="open-page" data-slug="'+esc(s)+'">'+esc(s)+'</a>':'<span class="bad">'+esc(s)+' (no page)</span>';}
const TABS=['01','02','03','04','05'];
function switchTab(t){
  S.tab=t;
  TABS.forEach(x=>{$('#tabbtn-'+x).setAttribute('aria-selected',String(x===t));$('#panel-'+x).hidden=(x!==t);});
  if(t==='01')render01();else if(t==='03')render03();else if(t==='04')render04();else if(t==='05')render05();
}
function openPage(slug){if(!bySlug[slug])return;S.page=slug;if(location.hash!=='#'+slug)location.hash=slug;switchTab('01');}
window.addEventListener('hashchange',()=>{const s=location.hash.slice(1);if(s&&bySlug[s]&&s!==S.page){S.page=s;switchTab('01');}});
let filterQ='';
function render01(){
  const panel=$('#panel-01');
  if(!panel.dataset.built){
    panel.innerHTML='<div class="layout"><aside class="rail"><label for="pg-filter">title, tag or slug</label><input type="text" id="pg-filter"><div class="bignum" id="pg-count"></div><div class="mono dim" style="margin-bottom:6px">pages · click = open</div><div id="pg-list"></div></aside><div class="content" id="pg-main"></div></div>';
    panel.dataset.built='1';
    $('#pg-filter').addEventListener('input',e=>{filterQ=e.target.value;updatePageList();});
  }
  updatePageList();
  $('#pg-main').innerHTML=S.page&&bySlug[S.page]?pageHtml(bySlug[S.page]):'<h2>The index</h2><p class="note">The wiki\u2019s own catalog, rendered as a page. Click a page on the left. How this is computed: the index is the wiki\u2019s first line plus one line per page.</p>'+renderMd(W.index,{}).replace(/<h([2-6])>/g,'<h$1>');
}
function updatePageList(){
  const q=filterQ.toLowerCase();
  const shown=P.filter(p=>!q||p.slug.includes(q)||p.title.toLowerCase().includes(q)||(p.frontmatter.tags||[]).some(t=>t.toLowerCase().includes(q)));
  $('#pg-count').textContent=shown.length+' of '+P.length;
  const types=[['source','Sources'],['concept','Concepts'],['entity','Entities'],['question','Questions']];
  let list='';
  types.forEach(([ty,label])=>{
    const g=shown.filter(p=>p.type===ty);if(!g.length)return;
    list+='<div class="mono grouplabel">'+label+'</div><div class="pagelist">';
    g.forEach(p=>{const stub=p.frontmatter.status==='stub';
      list+='<button data-action="open-page" data-slug="'+esc(p.slug)+'" class="'+(S.page===p.slug?'sel':'')+'"><span class="cnt">'+p._pins.length+' pins · '+(p.frontmatter.register||[]).join('')+'</span>'+esc(p.title)+(stub?' <span class="badge stub">stub</span>':'')+'</button>';});
    list+='</div>';
  });
  $('#pg-list').innerHTML=list||'<p class="note">No page matches.</p>';
}
function pageHtml(p){
  const fm=p.frontmatter;
  let badges='<span class="badge">'+esc(p.type)+'</span>';
  (fm.register||[]).forEach(r=>badges+='<span class="badge" title="'+esc(REG_NAMES[r]||r)+'">'+esc(r)+' · '+esc(REG_NAMES[r]||'?')+'</span>');
  badges+='<span class="badge">'+esc(fm.status||'')+'</span><span class="badge">updated '+esc(fm.updated||'')+'</span>';
  const tags=(fm.tags||[]).map(t=>'<span class="tag">#'+esc(t)+'</span>').join('');
  let out='<h2>'+esc(p.title)+'</h2><div>'+badges+'</div><div style="margin:6px 0">'+tags+'</div>';
  out+='<div class="body">'+renderMd(p.body,{pageSlug:p.slug})+'</div>';
  const bodySet=new Set(p._links);
  out+='<h3>Links out</h3><div>'+((fm.links||[]).map(s=>linkSlug(s)+(bodySet.has(s)?'':' <span class="warn">frontmatter only</span>')).join(' · ')||'<span class="dim">none</span>')+'</div>';
  out+='<h3>Linked from</h3><div>'+(((backlinks[p.slug]||[]).map(linkSlug).join(' · '))||'<span class="dim">no page links here</span>')+'</div>';
  out+='<h3>Sources</h3><div>';
  (fm.sources||[]).forEach(id=>{const d=byId[id];
    if(!d){out+='<div>'+esc(id)+' <span class="bad">not in the library</span></div>';return;}
    out+='<div>· <a href="'+esc(d.url)+'" target="_blank" rel="noopener">'+esc(d.symbol||d.id)+'</a> '+esc(d.short_title||d.title)+' — '+esc(d.kind)+', '+esc(d.year)+(d.status==='inbox'?' <span class="badge stub">inbox</span>':'')+'</div>';});
  out+='</div>';
  out+='<div style="margin:14px 0"><button class="btn" data-action="copy-page" data-slug="'+esc(p.slug)+'">Copy page as markdown</button></div>';
  return out;
}
const ask={running:false,slugs:[],answer:null,raw:null,sentPins:new Set(),tags:''};
async function runAsk(){
  const q=$('#ask-q').value.trim();if(!q||ask.running)return;
  ask.running=true;S.stop=false;const b=$('#ask-btn');b.disabled=true;b.textContent='Asking…';
  $('#ask-stop').hidden=false;$('#ask-out').innerHTML='';
  const info=$('#ask-info'),prog=$('#ask-prog');
  try{
    info.textContent='Step 1 will send: the index ('+W.index.length+' characters) and your question ('+q.length+' characters). No library passages leave the browser.';
    prog.textContent='Step 1 of 2 · choosing pages…';
    const p1='You route questions in a research wiki on neurotechnology in the administration of justice.\n\nIndex (one line per page):\n'+W.index+'\n\nQuestion: '+q+'\n\nReturn JSON only: {"pages":["slug",…]} — up to five slugs from the index above whose pages answer the question.';
    const r1=await askModel(p1,{});if(S.stop){prog.textContent='Stopped.';return;}
    if(!r1.json||!Array.isArray(r1.json.pages)){askFail(r1,'Step 1 did not return JSON.');return;}
    ask.slugs=r1.json.pages.filter(s=>bySlug[s]).slice(0,5);
    renderAskStep1();
    await runAskStep2(q);
  }finally{ask.running=false;b.disabled=false;b.textContent=ask.answer?'Ask again':'Ask the wiki';$('#ask-stop').hidden=true;}
}
function askFail(r,msg){
  $('#ask-prog').textContent=msg;
  $('#ask-out').innerHTML='<div class="card"><strong class="warn">'+esc(msg)+'</strong><pre data-source="ai">'+esc(r.raw||r.error||'')+'</pre><button class="btn" data-action="ask-retry">Retry</button></div>';
}
function chipsHtml(){
  let h='<div class="note">Step 1 chose these pages:</div><div>';
  ask.slugs.forEach(s=>h+='<span class="chip" style="cursor:default">'+esc(s)+'</span> ');
  h+='<button class="btn" data-action="ask-pages-toggle">Change pages</button></div>';
  h+='<div id="ask-pages" hidden><p class="note">Tick the pages to send in step 2 (the model sees only these bodies):</p>';
  P.forEach(p=>{h+='<label style="text-transform:none;letter-spacing:0;font-family:inherit;font-size:14px"><input type="checkbox" value="'+esc(p.slug)+'" '+(ask.slugs.includes(p.slug)?'checked':'')+'> '+esc(p.title)+' <span class="dim">('+p.type+')</span></label>';});
  h+='<button class="btn" data-action="ask-pages-apply">Apply pages and ask</button></div>';
  return h;
}
function renderAskStep1(){$('#ask-out').innerHTML=chipsHtml()+'<div class="progress" id="ask-prog2" aria-live="polite"></div>';}
async function runAskStep2(q){
  if(!q||ask.running&&ask.answer)return;
  const info=$('#ask-info'),prog=$('#ask-prog');
  const bodies=ask.slugs.map(s=>'## '+s+' — '+bySlug[s].title+'\n\n'+bySlug[s].body).join('\n\n---\\n\n');
  info.textContent='Step 2 will send: '+ask.slugs.length+' pages, '+(bodies.length+q.length).toLocaleString('en-US')+' characters; 0 library passages have left the browser. The answer must pin every claim to a pin that already stands on those pages.';
  prog.textContent='Step 2 of 2 · drafting the answer…';
  const p2='You answer from a research wiki on neurotechnology in the administration of justice. Pages:\n\n'+bodies+'\n\nQuestion: '+q+'\n\nReturn JSON only: {"title":"…","answer":"markdown, at most 350 words","cannot_answer":"what the library cannot answer"}. In the answer, pin every claim with [label](pin:id#pPAGE "quote") ✓ using only pins that already stand on the pages above, copied exactly — quote only words that stand in the passages given; the code will check. Name the register where it matters ((a) treaty law, (b) General Comment, (c) UN report, (d) NHRI, (e) civil society, (f) scholarship); keep each document\u2019s own verb; never present (c)–(f) as what the treaty requires.';
  const r2=await askModel(p2,{});if(S.stop){prog.textContent='Stopped.';return;}
  if(!r2.json||typeof r2.json.answer!=='string'){askFail(r2,'Step 2 did not return JSON.');return;}
  ask.answer=r2.json;ask.sentPins=new Set();
  ask.slugs.forEach(s=>bySlug[s]._pins.forEach(pn=>ask.sentPins.add(pn.id+'#p'+pn.page+'|'+pn.quote)));
  renderAskAnswer();
}
function renderAskAnswer(){
  const a=ask.answer;
  const pins=[...a.answer.matchAll(PIN_RE)].map(m=>({label:m[1],id:m[2],page:+m[3],quote:m[4]||'',mark:m[5]}));
  const ver=pins.filter(p=>verify(p).ok&&ask.sentPins.has(p.id+'#p'+p.page+'|'+p.quote));
  const regs={};ver.forEach(p=>{const r=registerOfDoc(p.id);regs[r]=(regs[r]||0)+1;});
  const regLine=Object.keys(REG_W).map(r=>'('+r+') '+(regs[r]||0)).join(' · ');
  let html=chipsHtml();
  html+='<div data-source="ai"><h3>'+esc(a.title||'Answer')+'</h3><div class="body">'+renderMd(a.answer,{ai:true,sentPins:ask.sentPins})+'</div>'+
    '<h4>What the library cannot answer</h4><p>'+esc(a.cannot_answer||'—')+'</p>'+
    '<div class="note">Verified pins by register: '+esc(regLine)+' · computed by this page from the pins above.</div></div>';
  html+='<div style="margin:12px 0"><button class="btn" data-action="ask-file-open">File as a question page</button></div><div id="ask-file"></div>';
  $('#ask-out').innerHTML=html;
}
function buildQuestionBody(title,a,links){
  const m=a.answer.match(/^.{10,400}?[.!?](?:\s|$)/s);
  const short=m?m[0].trim():a.answer.slice(0,200);
  return '# '+title+'\n\n**Short answer.** '+short+'\n\n## Reasoning\n\n'+a.answer+'\n\n## What the library cannot answer\n\n'+(a.cannot_answer||'—')+'\n\n## Related\n\n'+(links.length?links.map(s=>'[['+s+']]').join(', '):'—');
}
function renderFiling(){
  const a=ask.answer;if(!a)return;
  const title=a.title||'Question',slug=uniqueSlug(kebab(title));
  const pins=[...a.answer.matchAll(PIN_RE)].map(m=>({label:m[1],id:m[2],page:+m[3],quote:m[4]||'',mark:m[5]}));
  const allOk=pins.length>0&&pins.every(p=>verify(p).ok&&ask.sentPins.has(p.id+'#p'+p.page+'|'+p.quote));
  const links=[...new Set([...a.answer.matchAll(WLINK_RE)].map(m=>m[1]).filter(s=>bySlug[s]))];
  const sources=[...new Set(pins.map(p=>p.id))];
  const register=[...new Set(pins.map(p=>registerOfDoc(p.id)))].filter(r=>r&&r!=='?');
  const body=buildQuestionBody(title,a,links);
  let h='<div class="card"><strong>File as a question page</strong><div class="note">The code builds this page; the model wrote only the answer above.</div><table><tbody>'+
    '<tr><th scope="row">slug</th><td class="mono">'+esc(slug)+'</td></tr>'+
    '<tr><th scope="row">type / status</th><td>question / draft · updated '+today()+'</td></tr>'+
    '<tr><th scope="row">register</th><td>'+esc(register.join('')||'?')+'</td></tr>'+
    '<tr><th scope="row">links</th><td>'+(links.map(esc).join(', ')||'—')+'</td></tr>'+
    '<tr><th scope="row">sources</th><td>'+(sources.map(esc).join(', ')||'—')+'</td></tr></tbody></table>'+
    '<label for="ask-tags">tags (comma-separated)</label><input type="text" id="ask-tags" value="'+esc(ask.tags)+'">'+
    '<details><summary>Preview the body the code builds</summary><pre>'+esc(body)+'</pre></details>'+
    '<div style="margin:10px 0"><button class="btn primary" data-action="ask-file" '+(allOk?'':'disabled')+'>File this page</button> <button class="btn" data-action="ask-copy">Copy answer</button> <span class="note">'+(allOk?'every pin in the answer verifies and stands on the pages sent':'disabled until every pin verifies and stands on the pages sent ('+pins.filter(p=>!(verify(p).ok&&ask.sentPins.has(p.id+'#p'+p.page+'|'+p.quote))).length+' do not)')+'</span></div></div>';
  $('#ask-file').innerHTML=h;
  $('#ask-tags').addEventListener('input',e=>ask.tags=e.target.value);
}
function fileQuestion(){
  const a=ask.answer;if(!a)return;
  const title=a.title||'Question',slug=uniqueSlug(kebab(title));
  const pins=[...a.answer.matchAll(PIN_RE)].map(m=>({label:m[1],id:m[2],page:+m[3],quote:m[4]||'',mark:m[5]}));
  const links=[...new Set([...a.answer.matchAll(WLINK_RE)].map(m=>m[1]).filter(s=>bySlug[s]))];
  const sources=[...new Set(pins.map(p=>p.id))];
  const register=[...new Set(pins.map(p=>registerOfDoc(p.id)))].filter(r=>r&&r!=='?');
  const page={slug,type:'question',title,frontmatter:{title,type:'question',tags:(ask.tags||'').split(',').map(s=>s.trim()).filter(Boolean),register,status:'draft',updated:today(),links,sources},body:buildQuestionBody(title,a,links)};
  P.push(page);bySlug[slug]=page;prep(page);
  const n=page._pins.filter(pn=>verify(pn).ok).length;
  W.index+='\n- [['+slug+']] — '+title.slice(0,80)+' · ('+register.join('')+') · ✓'+n;
  const head='## ['+today()+'] ask | '+title;
  W.log+='\n'+head+'\n\nFiled from an Ask answer: '+page._pins.length+' pins, all verified by this page.\n';
  S.logAdded.push(head);S.changes++;S.changesList.push(slug);
  renderHeader();render01();
  const el=$('#ask-file');if(el)el.innerHTML='<p class="ok" aria-live="polite">Filed as [['+slug+']] — open it on tab 01; download it on tab 05.</p>';
}
const ing={docId:null,running:false,started:false,batches:[],takeaways:[],failed:[],dropped:0,newSlugs:[],sourceDraft:null,order:[],drafts:{},decisions:{},filed:false,calls0:0,pass0:0,progText:'',raw:null};
function markRunning(){const b=$('#tabbtn-03');b.innerHTML='03 Ingest'+(ing.running?' <span class="run" aria-live="polite">· running</span>':'');}
function setProg(t){ing.progText=t;const el=$('#ing-prog');if(el)el.textContent=t+' · calls so far '+(S.calls-ing.calls0)+' · passages sent '+(S.passages-ing.pass0);}
function startIngest(id){
  ing.docId=id;ing.calls0=S.calls;ing.pass0=S.passages;
  const doc=byId[id];ing.batches=[];
  for(let i=0;i<doc.passages.length;i+=25)ing.batches.push(doc.passages.slice(i,i+25));
  ing.progText='ready · scope set';render03();
}
function allowNew(s){if(bySlug[s])return true;if(ing.newSlugs.length<2&&!ing.newSlugs.includes(s)){ing.newSlugs.push(s);return true;}return false;}
function commonRun(a,b){const A=norm(a).split(' '),B=norm(b).split(' ');let best=0;for(let i=0;i<A.length;i++)for(let j=0;j<B.length;j++){let k=0;while(i+k<A.length&&j+k<B.length&&A[i+k]===B[j+k])k++;if(k>best)best=k;}return best;}
function nearestPassage(doc,page,quote){
  let best=null,br=0;
  doc.passages.filter(p=>p.page===page).forEach(p=>{const r=commonRun(quote,p.text);if(r>br){br=r;best=p;}});
  return best?{passage:best,run:br}:null;
}
function parsePinStr(s){const m=s.match(/\[([^\]]+)\]\(pin:([^#\s)]+)#p(\d+)(?: "([^"]*)")?\) ?(✓|⚠)/);return m?{label:m[1],id:m[2],page:+m[3],quote:m[4]||'',mark:m[5]}:null;}
async function startBatches(){
  if(ing.running)return;
  ing.running=true;ing.started=true;ing.raw=null;S.stop=false;markRunning();render03();
  const doc=byId[ing.docId];
  for(let i=0;i<ing.batches.length;i++){
    if(S.stop)break;
    setProg('batch '+(i+1)+' of '+ing.batches.length+' · '+(i*25)+' of '+doc.passages.length+' passages have left the browser');
    const b=ing.batches[i];
    const pj=JSON.stringify(b.map(p=>({id:p.id,page:p.page,paragraph:p.paragraph,section:p.section,text:p.text})));
    const prompt='You are ingesting '+citeAs[ing.docId]+' ('+(doc.symbol||doc.author+' '+doc.year)+', '+doc.title+') into a research wiki on neurotechnology in the administration of justice.\n\nIndex (one line per page):\n'+W.index+'\n\nPassages, verbatim from the PDF (JSON array):\n'+pj+'\n\nReturn JSON only: {"takeaways":[{"claim":"…","quote":"8–40 words copied verbatim from that one passage","passage":"the passage id","pages":["slugs from the index the claim bears on"]}]}, at most 10 takeaways. Pin syntax: [label](pin:id#pPAGE "quote") ✓ — quote only words that stand in the passages given; the code will check.';
    const r=await askModel(prompt,{passages:b.length});
    if(S.stop)break;
    if(!r.json||!Array.isArray(r.json.takeaways)){ing.raw=r.raw;ing.progText='batch '+(i+1)+' did not return JSON — raw answer kept in step 03; press Retry';render03();continue;}
    for(const t of r.json.takeaways){
      const passage=b.find(p=>p.id===t.passage);
      if(!passage){ing.dropped++;continue;}
      const pinStr=makePin(ing.docId,passage,t.quote||''),pin=parsePinStr(pinStr),v=verify(pin);
      const pages=(Array.isArray(t.pages)?t.pages:[]).filter(s=>allowNew(s));
      if(v.ok)ing.takeaways.push({claim:t.claim,quote:t.quote,passage,pin:pinStr,pages});
      else ing.failed.push({claim:t.claim,quote:t.quote,passage,pin:pinStr,reason:v.reason,nearest:nearestPassage(doc,pin.page,t.quote||'')});
    }
    render03();
  }
  ing.running=false;markRunning();
  setProg('step 1 done · '+ing.takeaways.length+' takeaways verified · '+ing.failed.length+' could not be verified'+(S.stop?' · stopped early':''));
  render03();
}
function touchedSlugs(){
  const set=new Set();
  ing.takeaways.forEach(t=>t.pages.forEach(s=>{if(bySlug[s])set.add(s);}));
  ing.newSlugs.forEach(s=>set.add(s));
  const stub=P.find(p=>p.frontmatter.status==='stub'&&p.frontmatter.sources.includes(ing.docId));
  if(stub)set.add(stub.slug);
  if(ing.sourceDraft)(ing.sourceDraft.touches||[]).forEach(s=>{if(bySlug[s]||ing.newSlugs.includes(s))set.add(s);});
  return [...set];
}
async function draftSource(){
  if(ing.running)return;ing.running=true;S.stop=false;markRunning();
  const doc=byId[ing.docId];
  setProg('drafting the source page · 1 call');render03();
  const tks=ing.takeaways.map(t=>({claim:t.claim,pin:t.pin}));
  const stub=P.find(p=>p.frontmatter.status==='stub'&&p.frontmatter.sources.includes(ing.docId));
  const reg=stub?(stub.frontmatter.register||[]):[];
  const prompt='Draft the source page for a new library document in a research wiki on neurotechnology in the administration of justice.\n\nFull cite: '+(doc.symbol||doc.author+' '+doc.year)+' — '+doc.title+' ('+doc.kind+', '+doc.published+', '+doc.url+', '+doc.pages+' PDF pages). Register: '+reg.join('')+' ('+reg.map(r=>REG_NAMES[r]).join(', ')+').\n\nVerified takeaways with ready-made pins (copy the pins exactly, character for character):\n'+JSON.stringify(tks)+'\n\nThe schema\u2019s source-page anatomy: Full cite · Register · One-liner · Key takeaways · How NOT to read this · Where it feeds the wiki · Related.\n\nReturn JSON only: {"one_liner":"…","body":"markdown, at most 900 words, only the pins given, copied exactly","touches":[{"slug":"…","why":"…"}]}, at most 12 touches, slugs from the index or new slugs. Pin syntax: [label](pin:id#pPAGE "quote") ✓ — quote only words that stand in the passages given; the code will check.';
  const r=await askModel(prompt,{});
  ing.running=false;markRunning();
  if(!r.json||typeof r.json.body!=='string'){ing.raw=r.raw;ing.progText='source-page draft did not return JSON';render03();return;}
  const body=r.json.body;
  const pins=[...body.matchAll(PIN_RE)].map(m=>({label:m[1],id:m[2],page:+m[3],quote:m[4]||'',mark:m[5]}));
  const ver=pins.filter(p=>verify(p).ok).length;
  const slug=uniqueSlug(kebab(doc.short_title||doc.title));
  const links=[...new Set([...body.matchAll(WLINK_RE)].map(m=>m[1]))];
  const touches=(Array.isArray(r.json.touches)?r.json.touches:[]).map(t=>t.slug).filter(s=>bySlug[s]||allowNew(s)).slice(0,12);
  if(stub&&!touches.includes(stub.slug))touches.push(stub.slug);
  ing.sourceDraft={slug,title:doc.title,one_liner:r.json.one_liner||'',body,inserted:[body],pins,ver,notVer:pins.length-ver,touches,
    frontmatter:{title:doc.title,type:'source',tags:touches.slice(0,8),register:reg,status:'reviewed',updated:today(),links,sources:[ing.docId]}};
  setProg('source page drafted · '+pins.length+' pins, '+ver+' verified, '+(pins.length-ver)+' not verified');
  render03();
}
function insertAfterHeading(body,heading,md){
  const lines=body.split('\n');
  const target=String(heading).replace(/^#+\s*/,'').trim().toLowerCase();
  const idx=lines.findIndex(l=>l.replace(/^#+\s*/,'').trim().toLowerCase()===target);
  if(idx<0||target==='end')return{body:body.replace(/\s*$/,'')+'\\n\\n'+md+'\\n',inserted:[md]};
  let end=lines.length;
  for(let i=idx+1;i<lines.length;i++)if(/^#{1,6}\s/.test(lines[i])){end=i;break;}
  lines.splice(end,0,'',md,'');
  return{body:lines.join('\\n'),inserted:[md]};
}
async function draftAllTouched(){
  if(ing.running)return;ing.running=true;S.stop=false;markRunning();
  const slugs=touchedSlugs();
  for(let i=0;i<slugs.length;i++){
    if(S.stop)break;
    const slug=slugs[i];
    setProg('drafting changes to page '+(i+1)+' of '+slugs.length+' ('+slug+')');render03();
    const page=bySlug[slug]||null;
    const tks=ing.takeaways.filter(t=>t.pages.includes(slug)).map(t=>({claim:t.claim,pin:t.pin}));
    const base=page?('Existing page [['+slug+']] — '+page.title+'\\n\\nBody:\\n'+page.body+'\\n\\n'):('New page to create: '+slug+'\\n\\n');
    const prompt=base+'New verified takeaways from '+citeAs[ing.docId]+' (pins ready-made, copy exactly):\\n'+JSON.stringify(tks)+'\\n\\nReturn JSON only: {"edits":[{"after":"an existing heading of the page, or \\"end\\"","markdown":"at most 300 words in all across edits, pins copied exactly"}],"contested":"a full contested block only where this document disagrees with the page, else null"}. Pin syntax: [label](pin:id#pPAGE "quote") ✓ — quote only words that stand in the passages given; the code will check.';
    const r=await askModel(prompt,{});
    if(!r.json||!Array.isArray(r.json.edits)){ing.raw=r.raw;ing.progText='draft for '+slug+' did not return JSON';render03();continue;}
    let body=page?page.body:'# '+slug+'\\n';
    const inserted=[];
    for(const e of r.json.edits){if(!e||typeof e.markdown!=='string')continue;const res=insertAfterHeading(body,e.after||'end',e.markdown);body=res.body;inserted.push(e.markdown);}
    if(r.json.contested&&typeof r.json.contested==='string')body+='\\n\\n'+r.json.contested.replace(/^```\\w*\\s*|```$/g,'')+'\\n';
    const fm=page?{...page.frontmatter}:{title:slug,type:'concept',tags:[],register:[],status:'draft',updated:today(),links:[],sources:[]};
    fm.links=[...new Set([...(fm.links||[]),...([...body.matchAll(WLINK_RE)].map(m=>m[1]))])];
    fm.sources=[...new Set([...(fm.sources||[]),ing.docId])];
    fm.updated=today();
    const pins=[...body.matchAll(PIN_RE)].map(m=>({label:m[1],id:m[2],page:+m[3],quote:m[4]||'',mark:m[5]}));
    const oldKeys=page?new Set(page._pins.map(p=>p.id+'#p'+p.page+'|'+p.quote)):new Set();
    const added=pins.filter(p=>!oldKeys.has(p.id+'#p'+p.page+'|'+p.quote));
    ing.drafts[slug]={body,frontmatter:fm,inserted,pins,added,addedVer:added.filter(p=>verify(p).ok).length,contested:!!r.json.contested};
    if(!ing.order.includes(slug))ing.order.push(slug);
    render03();
  }
  ing.running=false;markRunning();
  setProg('drafts done · '+ing.order.length+' pages touched');
  render03();
}
function changeCard(key,i,n){
  const isNew=key==='__new__';
  const d=isNew?ing.sourceDraft:ing.drafts[key];
  const page=isNew?null:bySlug[key];
  if(!d)return'';
  const title=isNew?d.title:page.title,type=isNew?'source':page.type;
  const pins=[...d.body.matchAll(PIN_RE)].map(m=>({label:m[1],id:m[2],page:+m[3],quote:m[4]||'',mark:m[5]}));
  const oldKeys=page?new Set(page._pins.map(p=>p.id+'#p'+p.page+'|'+p.quote)):new Set();
  const added=pins.filter(p=>!oldKeys.has(p.id+'#p'+p.page+'|'+p.quote));
  const addedVer=added.filter(p=>verify(p).ok).length;
  const dec=ing.decisions[key];
  let h='<fieldset class="card"><legend>Change '+i+' of '+n+' · '+esc(isNew?d.slug:key)+'</legend>';
  h+='<div>'+esc(title)+' · '+esc(type)+' · '+(isNew?'new page':'edited')+' · paragraphs inserted: '+(d.inserted?d.inserted.length:0)+' · pins added: '+added.length+' (verified '+addedVer+', not verified '+(added.length-addedVer)+')</div>';
  h+='<div class="diff body" style="margin:10px 0">'+renderMd(d.body,{inserted:d.inserted||[]})+'</div>';
  h+='<div><button class="btn primary" data-action="approve" data-key="'+esc(key)+'" '+(dec?'disabled':'')+'>Approve change '+i+' of '+n+'</button> '+
    '<button class="btn" data-action="reject" data-key="'+esc(key)+'" '+(dec?'disabled':'')+'>Reject change '+i+' of '+n+'</button> '+
    '<span class="note">'+(dec?('decision: '+dec):'nothing is written until you approve')+'</span></div></fieldset>';
  return h;
}
function upsertIndexLine(slug){
  const p=bySlug[slug];if(!p)return;
  const n=p._pins.filter(pn=>verify(pn).ok).length;
  const line='- [['+slug+']] — '+(p.frontmatter.title||p.title).slice(0,80)+' · ('+(p.frontmatter.register||[]).join('')+') · ✓'+n;
  const re=new RegExp('- \\[\\['+slug.replace(/[.*+?^${}()|[\]\\]/g,'\\$&')+'\\]\\][^\\n]*');
  W.index=re.test(W.index)?W.index.replace(re,line):W.index.replace(/\\s*$/,''')+'\\n'+line;
}
function fileIngest(){
  const doc=byId[ing.docId],approved=[],rejected=[];
  if(ing.sourceDraft&&ing.decisions.__new__==='approved'){
    const slug=ing.sourceDraft.slug;
    const page={slug,type:'source',title:ing.sourceDraft.title,frontmatter:ing.sourceDraft.frontmatter,body:ing.sourceDraft.body};
    P.push(page);bySlug[slug]=page;prep(page);approved.push(slug);
  }
  ing.order.forEach(slug=>{
    if(ing.decisions[slug]==='approved'){const d=ing.drafts[slug],p=bySlug[slug];p.body=d.body;p.frontmatter=d.frontmatter;prep(p);approved.push(slug);}
    else if(ing.decisions[slug]==='rejected')rejected.push(slug);
  });
  const totalPins=P.reduce((n,p)=>n+p._pins.length,0);
  W.index=W.index.replace(/(\\d[\\d,]*) pins/,totalPins.toLocaleString('en-US')+' pins');
  approved.forEach(upsertIndexLine);
  const cite=citeAs[ing.docId],reg=registerOfDoc(ing.docId);
  const pinnedOn=P.filter(p=>approved.includes(p.slug)?false:p._pins.some(pn=>pn.id===ing.docId)).map(p=>p.slug);
  const head='## ['+today()+'] ingest | '+(doc.symbol||ing.docId)+': '+(doc.short_title||doc.title);
  W.log+='\\n'+head+'\\n\\nRead '+doc.passages.length+' passages ('+cite+', register ('+reg+')). '+(approved.length?'Wrote '+approved.map(s=>'[['+s+']]').join(', ')+'.':'Nothing approved.')+' '+totalPins+' pins in all; besides its own page, pinned on '+pinnedOn.length+' pages: '+(pinnedOn.map(s=>'[['+s+']]').join(', ')||'none')+'. Rejected: '+(rejected.length?rejected.map(s=>'[['+s+']]').join(', '):'none')+'.\\n';
  S.logAdded.push(head);
  ing.order.forEach(slug=>{const d=ing.drafts[slug];if(d&&d.contested&&ing.decisions[slug]==='approved')W.tensions+='\\n### '+kebab(slug)+'-contested\\n\\nstatus: open\\ncard: [['+slug+']]\\n\\n';});
  doc.status='ingested';
  S.changes+=approved.length;approved.forEach(s=>S.changesList.push(s));
  ing.filed=true;ing.progText='filed · lint re-run on tab 04';
  renderHeader();render03();
}
function render03(){
  const panel=$('#panel-03');
  if(!ing.docId){
    const docs=D.filter(d=>d.status==='inbox');
    let h='<h2>What would the waiting document change?</h2>';
    if(!docs.length)h+='<p class="note">Nothing waits in the inbox.</p>';
    else{docs.forEach(d=>{h+='<div style="margin:10px 0"><button class="btn primary" data-action="ingest-start" data-id="'+esc(d.id)+'">Ingest '+esc(d.symbol||d.short_title||d.id)+'</button> <span class="note">'+esc(d.short_title||d.title)+' · '+d.passages.length+' passages · '+esc(d.kind)+'</span></div>';});
      h+='<p class="note">Ingesting sends all passages to the model in batches of 25, verifies every quote the code can check, and writes nothing until you approve each change.</p>';}
    panel.innerHTML=h;return;
  }
  const doc=byId[ing.docId];
  let h='<h2>Ingest '+esc(doc.symbol||doc.id)+'</h2><div class="note">'+esc(doc.short_title||doc.title)+' · '+esc(doc.kind)+' · '+doc.passages.length+' passages · status: '+doc.status+'</div>';
  h+='<div class="progress" id="ing-prog" aria-live="polite">'+esc(ing.progText||'ready')+' · calls so far '+(S.calls-ing.calls0)+' · passages sent '+(S.passages-ing.pass0)+'</div>';
  if(ing.running)h+='<button class="btn" data-action="stop">Stop</button>';
  h+='<div class="step"><h3>01 · Scope</h3>';
  if(!ing.started){
    const n=doc.passages.length,calls=Math.ceil(n/25),chars=doc.passages.reduce((s,p)=>s+p.text.length,0);
    h+='<p>All '+n+' passages will be sent, in batches of 25 ('+calls+' calls), '+chars.toLocaleString('en-US')+' characters; nothing is held back.</p>';
    h+='<table><caption>FIG.01 · Batches — every passage is sent exactly once</caption><thead><tr><th scope="col">batch</th><th scope="col">paragraphs</th><th scope="col">PDF pages</th><th scope="col" class="num">passages</th></tr></thead><tbody>';
    ing.batches.forEach((b,i)=>{h+='<tr><td>'+(i+1)+'</td><td>'+esc(String(b[0].paragraph??'—'))+' – '+esc(String(b[b.length-1].paragraph??'—'))+'</td><td>'+b[0].page+'–'+b[b.length-1].page+'</td><td class="num">'+b.length+'</td></tr>';});
    h+='</tbody></table><button class="btn primary" data-action="ingest-run">Start</button>';
  }else{
    h+='<p class="note">Batches run one after another; Stop keeps what has returned. Passages sent so far: '+(S.passages-ing.pass0)+' of '+doc.passages.length+'.</p>';
    if(ing.raw&&!ing.running)h+='<button class="btn" data-action="ingest-run">Retry</button>';
  }
  h+='</div>';
  h+='<div class="step"><h3>02 · Takeaways</h3>';
  if(ing.takeaways.length||ing.failed.length){
    h+='<table><caption>FIG.02 · Takeaways — each quote re-verified by this page against the library</caption><thead><tr><th scope="col">claim</th><th scope="col">quote</th><th scope="col">passage</th><th scope="col">pages</th><th scope="col">verification</th></tr></thead><tbody>';
    ing.takeaways.forEach(t=>{h+='<tr><td>'+esc(t.claim)+'</td><td class="pin-quote">“'+esc(t.quote)+'”</td><td>'+esc(t.passage.paragraph!=null?'para. '+t.passage.paragraph:'p. '+t.passage.page_label)+' · PDF p. '+t.passage.page+'</td><td>'+t.pages.map(esc).join(', ')+'</td><td class="ok">✓ verified</td></tr>';});
    h+='</tbody></table>';
    if(ing.failed.length){
      h+='<div class="card"><strong class="warn">Could not verify: '+ing.failed.length+'</strong><ul>';
      ing.failed.forEach(f=>{h+='<li>'+esc(f.claim)+' — quote “'+esc(f.quote)+'” ('+esc(f.reason||'')+')'+(f.nearest?' · nearest passage on that page: '+(f.nearest.passage.paragraph!=null?'para. '+esc(f.nearest.passage.paragraph):'p. '+esc(f.nearest.passage.page_label))+', shared run '+f.nearest.run+' words':'')+' <button class="chip" data-action="pin-open" data-id="'+esc(ing.docId)+'" data-page="'+f.passage.page+'" data-quote="'+esc(f.quote)+'">Open the PDF page</button></li>';});
      h+='</ul><p class="note">These claims are in no change card and in no later prompt.</p></div>';
    }
  }else h+='<p class="note">No takeaways yet — run step 01.</p>';
  h+='</div>';
  h+='<div class="step"><h3>03 · Drafts</h3>';
  if(ing.takeaways.length){
    h+='<div style="margin:6px 0"><button class="btn" data-action="ingest-draft-source" '+(ing.running?'disabled':'')+'>Draft the source page (1 call)</button></div>';
    if(ing.sourceDraft){
      const ts=touchedSlugs();
      h+='<p class="note">Source page drafted: '+ing.sourceDraft.pins.length+' pins, '+ing.sourceDraft.ver+' verified, '+ing.sourceDraft.notVer+' not verified. Touches: '+ts.map(esc).join(', ')+'.</p>';
      h+='<div style="margin:6px 0"><button class="btn" data-action="ingest-draft-touched" '+(ing.running?'disabled':'')+'>Draft the changes to '+ts.length+' pages ('+ts.length+' calls)</button></div>';
    }
  }else h+='<p class="note">Waiting on step 02.</p>';
  if(ing.raw)h+='<details><summary>Raw model answer (parse failure)</summary><pre data-source="ai">'+esc(ing.raw)+'</pre></details>';
  h+='</div>';
  h+='<div class="step"><h3>04 · Review and file</h3>';
  const keys=[...(ing.sourceDraft?['__new__']:[]),...ing.order];
  if(keys.length){
    const decided=keys.filter(k=>ing.decisions[k]).length;
    h+='<p class="note">change '+decided+' of '+keys.length+' decided · nothing is written until Approve is pressed</p>';
    keys.forEach((k,i)=>{h+=changeCard(k,i+1,keys.length);});
    if(decided===keys.length&&!ing.filed)h+='<button class="btn primary" data-action="ingest-file">File the approved changes</button>';
    if(ing.filed)h+='<p class="ok">Filed. The document is now ingested; lint re-run on tab 04.</p>';
  }else h+='<p class="note">No drafts yet.</p>';
  h+='</div>';
  panel.innerHTML=h;
}
function indexLines(){return W.index.split('\\n').filter(l=>/^- \\[\\[/.test(l));}
function computeLint(){
  const checks=[];
  const add=(name,count,pass,pages,detail)=>checks.push({name,count,pass,pages:pages||[],detail:detail||''});
  const totalPins=P.reduce((n,p)=>n+p._pins.length,0);
  const verPins=P.reduce((n,p)=>n+p._pins.filter(pn=>verify(pn).ok).length,0);
  const stated=(W.index.match(/(\\d[\\d,]*) pins/)||[,'?'])[1].replace(/,/g,'');
  add('Pins found by the regular expression vs the index line',totalPins,String(totalPins)===stated,[],'index says '+stated);
  const notVer=P.filter(p=>p._pins.some(pn=>!verify(pn).ok));
  add('Pins not verified by this page',notVer.reduce((n,p)=>n+p._pins.filter(pn=>!verify(pn).ok).length,0),notVer.length===0,notVer.map(p=>p.slug));
  const badMark=P.filter(p=>p._pins.some(pn=>pn.mark==='✓'&&!verify(pn).ok));
  add('Pins marked ✓ that fail verification',badMark.reduce((n,p)=>n+p._pins.filter(pn=>pn.mark==='✓'&&!verify(pn).ok).length,0),badMark.length===0,badMark.map(p=>p.slug));
  const dangling=P.filter(p=>p._links.some(s=>!bySlug[s]));
  add('Dangling [[links]]',dangling.reduce((n,p)=>n+p._links.filter(s=>!bySlug[s]).length,0),dangling.length===0,dangling.map(p=>p.slug));
  const orphans=P.filter(p=>!(backlinks[p.slug]||[]).length);
  add('Orphan pages (nothing links to them)',orphans.length,orphans.length===0,orphans.map(p=>p.slug));
  const srcDiff=P.filter(p=>{const a=new Set(p.frontmatter.sources||[]),b=new Set(p._pins.map(pn=>pn.id));return a.size!==b.size||[...a].some(x=>!b.has(x));});
  add('frontmatter.sources differ from the pinned documents',srcDiff.length,srcDiff.length===0,srcDiff.map(p=>p.slug));
  const noPins=P.filter(p=>p._pins.length===0);
  add('Pages with no pins',noPins.length,noPins.length===0,noPins.map(p=>p.slug));
  const nonRecip=P.filter(p=>{const a=new Set(p.frontmatter.links||[]),b=new Set(p._links);return a.size!==b.size||[...a].some(x=>!b.has(x));});
  add('frontmatter.links not reciprocated in the body',nonRecip.length,nonRecip.length===0,nonRecip.map(p=>p.slug));
  const idxSlugs=new Set(indexLines().map(l=>l.match(/\\[\\[([^\\]]+)\\]\\]/)[1]));
  const missingIdx=P.filter(p=>!idxSlugs.has(p.slug)),ghost=[...idxSlugs].filter(s=>!bySlug[s]);
  add('Pages missing from the index / index lines without a page',missingIdx.length+ghost.length,missingIdx.length===0&&ghost.length===0,[...missingIdx.map(p=>p.slug),...ghost]);
  const idxCount={};indexLines().forEach(l=>{const m=l.match(/\\[\\[([^\\]]+)\\]\\]/),c=l.match(/✓([\\d,]+)/);if(m&&c)idxCount[m[1]]=+c[1].replace(/,/g,'');});
  const wrongN=P.filter(p=>idxCount[p.slug]!==undefined&&idxCount[p.slug]!==p._pins.filter(pn=>verify(pn).ok).length);
  add('Index ✓N differs from the computed verified count',wrongN.length,wrongN.length===0,wrongN.map(p=>p.slug));
  const cards=new Set(P.filter(p=>/```contested/.test(p.body)).map(p=>p.slug)),tc=tensionsCards();
  const c1=[...cards].filter(s=>!tc.has(s)),c2=[...tc].filter(s=>!cards.has(s));
  add('Contested cards without a tensions entry / reverse',c1.length+c2.length,c1.length===0&&c2.length===0,[...c1,...c2]);
  const stubs=P.filter(p=>p.frontmatter.status==='stub');
  add('Stub pages',stubs.length,false,stubs.map(p=>p.slug),'a stub waits for its ingest');
  const inboxPins=P.filter(p=>p._pins.some(pn=>byId[pn.id]&&byId[pn.id].status==='inbox'));
  add('Pins to a document still in the inbox',inboxPins.reduce((n,p)=>n+p._pins.filter(pn=>byId[pn.id]&&byId[pn.id].status==='inbox').length,0),inboxPins.length===0,inboxPins.map(p=>p.slug));
  return{checks,totalPins,verPins};
}
function render04(){
  const L=computeLint(),need=L.checks.filter(c=>!c.pass).length;
  let h='<h2>Can I trust this?</h2>';
  h+='<div class="bignum">'+L.verPins+' of '+L.totalPins+'</div>';
  h+='<div class="note">pins verified by this page · '+need+' lint checks need a look · How this is computed: every pin in every page is re-checked against WORKSHOP_DATA.library by the code on this page.</div>';
  h+='<div style="margin:12px 0"><button class="btn primary" data-action="lint">'+(S.linted?'Re-run lint':'Lint now')+'</button></div>';
  h+='<table><caption>FIG.03 · Lint checks — counting, matching and verification are done by this page\\u2019s code</caption><thead><tr><th scope="col">check</th><th scope="col" class="num">count</th><th scope="col">result</th><th scope="col">pages</th></tr></thead><tbody>';
  L.checks.forEach(c=>{h+='<tr><td>'+esc(c.name)+(c.detail?' <span class="dim">('+esc(c.detail)+')</span>':'')+'</td><td class="num">'+c.count+'</td><td class="'+(c.pass?'ok':'bad')+'">'+(c.pass?'0 · pass':c.count+' · check')+'</td><td>'+(c.pages.map(s=>bySlug[s]?linkSlug(s):esc(s)).join(', ')||'—')+'</td></tr>';});
  h+='</tbody></table>';
  h+='<details open><summary>How this app checks itself</summary><div class="note"><ul>'+
    '<li>Pins: found by the regular expression against the number stated in the first line of the index; each verified against a passage of the pinned document on that PDF page, fragments joined by "…" checked in order after normalising whitespace, quotes, dashes and hyphenation; capitals are kept.</li>'+
    '<li>Labels: every verified pin\\u2019s label must contain "para. N" or "p. label" of its passage.</li>'+
    '<li>Structure: dangling links, orphans, sources vs pinned documents, index coverage and ✓N, contested cards vs the tensions register, stubs, pins to inbox documents.</li>'+
    '<li>Contradictions between pages are named in the schema but are not linted by code — that reading stays with a person.</li>'+
    '<li>A failing check never hides a page or a pin.</li></ul></div></details>';
  $('#panel-04').innerHTML=h;
}
let logNewestFirst=true;
function render05(){
  const entries=W.log.split(/(?=^## )/m).filter(s=>s.trim());
  if(logNewestFirst)entries.reverse();
  let h='<h2>What has changed, where do the sources disagree, and how do I take it away?</h2>';
  h+='<div style="margin:8px 0"><button class="btn" data-action="log-order">Order: '+(logNewestFirst?'newest first':'oldest first')+'</button></div>';
  h+='<h3>Log</h3>';
  entries.forEach(e=>{
    const head=e.split('\\n')[0],sess=S.logAdded.some(s=>head.includes(s.slice(3)));
    h+='<details'+(sess?' open':'')+'><summary>'+esc(head)+(sess?'<span class="session-tag">this session</span>':'')+'</summary><div class="body">'+renderMd(e.split('\\n').slice(1).join('\\n'))+'</div></details>';
  });
  h+='<h3>Tensions register</h3>';
  tensionsEntries().forEach(e=>{
    const head=e.split('\\n')[0],m=e.match(/card:\\s*\\[\\[([^\\]]+)\\]\\]/);
    h+='<details><summary>'+esc(head)+(m?' · card: '+linkSlug(m[1]):'')+'</summary><div class="body">'+renderMd(e.split('\\n').slice(1).join('\\n'))+'</div></details>';
  });
  h+='<h3>Method</h3><p class="note">Counting, filtering, sorting, matching and pin verification are done by this page\\u2019s code, deterministically; every number above has its "How this is computed" line. The model is called only when you press Ask, Ingest or a retry button, and each call announces what leaves the browser. Data: '+esc(W.source)+' · built '+esc(W.built)+' · '+D.length+' library documents.</p>';
  h+='<div style="margin:14px 0"><button class="btn primary" data-action="download-json">Download the wiki</button> '+(S.changesList.length?'<button class="btn" data-action="download-md">Download the changed pages (markdown)</button>':'')+'</div>';
  $('#panel-05').innerHTML=h;
}
function fmYaml(fm){return '---\\n'+Object.entries(fm).map(([k,v])=>k+': '+(Array.isArray(v)?'['+v.join(', ')+']':v)).join('\\n')+'\\n---\\n';}
function copyText(t){
  const done=()=>flash('Copied.');
  if(navigator.clipboard&&navigator.clipboard.writeText)navigator.clipboard.writeText(t).then(done,()=>fallbackCopy(t,done));else fallbackCopy(t,done);
}
function fallbackCopy(t,done){const ta=document.createElement('textarea');ta.value=t;document.body.appendChild(ta);ta.select();try{document.execCommand('copy');done();}catch(e){flash('Copy failed.');}ta.remove();}
function flash(msg){const el=$('#hdr-counters');el.textContent=msg+' · '+el.textContent;setTimeout(renderCounters,1500);}
function copyPage(slug){const p=bySlug[slug];if(p)copyText(fmYaml(p.frontmatter)+p.body);}
function download(name,text,type){const b=new Blob([text],{type:type||'application/json'});const a=document.createElement('a');a.href=URL.createObjectURL(b);a.download=name;document.body.appendChild(a);a.click();setTimeout(()=>{URL.revokeObjectURL(a.href);a.remove();},400);}
function downloadJson(){
  const data={title:W.title,source:W.source,built:W.built,count:P.length,schema:W.schema,pages:P,index:W.index,log:W.log,tensions:W.tensions,changes:S.changesList,library_status:D.map(d=>({id:d.id,status:d.status}))};
  download('wiki-'+today()+'.json',JSON.stringify(data,null,2));
}
function downloadMd(){
  download('wiki-changed-'+today()+'.md',S.changesList.map(slug=>{const p=bySlug[slug];return fmYaml(p.frontmatter)+p.body;}).join('\\n\\n---\\n\\n'),'text/markdown');
}
document.addEventListener('click',e=>{
  const t=e.target.closest('[data-action]');if(!t)return;
  const a=t.dataset.action;
  if(a==='tab'){e.preventDefault();switchTab(t.dataset.tab);}
  else if(a==='open-page')openPage(t.dataset.slug);
  else if(a==='pin-open')studio.openSource(t.dataset.id,+t.dataset.page,t.dataset.quote);
  else if(a==='pin-toggle'){const d=t.closest('.pin').querySelector('.pin-detail');d.hidden=!d.hidden;t.setAttribute('aria-expanded',String(!d.hidden));}
  else if(a==='copy-page')copyPage(t.dataset.slug);
  else if(a==='ask')runAsk();
  else if(a==='ask-retry')runAsk();
  else if(a==='ask-stop'||a==='stop')S.stop=true;
  else if(a==='ask-pages-toggle'){const p=$('#ask-pages');p.hidden=!p.hidden;}
  else if(a==='ask-pages-apply'){const sel=[...document.querySelectorAll('#ask-pages input:checked')].map(i=>i.value);if(sel.length){ask.slugs=sel.slice(0,8);}runAskStep2($('#ask-q').value.trim());}
  else if(a==='ask-file-open')renderFiling();
  else if(a==='ask-file')fileQuestion();
  else if(a==='ask-copy')copyText(ask.answer?ask.answer.answer:'');
  else if(a==='ingest-start')startIngest(t.dataset.id);
  else if(a==='ingest-run')startBatches();
  else if(a==='ingest-draft-source')draftSource();
  else if(a==='ingest-draft-touched')draftAllTouched();
  else if(a==='approve'){ing.decisions[t.dataset.key]='approved';render03();}
  else if(a==='reject'){ing.decisions[t.dataset.key]='rejected';render03();}
  else if(a==='ingest-file')fileIngest();
  else if(a==='lint'){S.linted=true;render04();}
  else if(a==='log-order'){logNewestFirst=!logNewestFirst;render05();}
  else if(a==='download-json')downloadJson();
  else if(a==='download-md')downloadMd();
});
document.addEventListener('keydown',e=>{
  if(e.key==='Enter'&&e.target.id==='ask-q'&&!e.shiftKey){e.preventDefault();runAsk();}
  if(e.key==='Escape')S.stop=true;
});
$('#tabs').addEventListener('keydown',e=>{
  if(!['ArrowRight','ArrowLeft','Home','End'].includes(e.key))return;
  const tabs=[...$('#tabs').querySelectorAll('[role=tab]')];
  let i=tabs.indexOf(document.activeElement);if(i<0)return;
  e.preventDefault();
  if(e.key==='ArrowRight')i=(i+1)%tabs.length;else if(e.key==='ArrowLeft')i=(i-1+tabs.length)%tabs.length;else if(e.key==='Home')i=0;else i=tabs.length-1;
  tabs[i].focus();tabs[i].click();
});
renderHeader();
const h0=location.hash.slice(1);if(h0&&bySlug[h0])S.page=h0;
switchTab('01');
$('#tabbtn-01').focus();
</script>
</body>
</html>
```