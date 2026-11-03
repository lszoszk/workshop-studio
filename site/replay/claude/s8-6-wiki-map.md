I added tab 06 MAP: every page is a node coloured by its type and sized by the number of pages that link to it, with one curved line for each [[link]] and a layout the code computes the same way every time. Hover or focus a node to see its title and its links in and out; click it to highlight its neighbours and use "Open this page", and the orphans are listed and clickable under the map. That makes six tabs, one more than the usual five, and the rest of the app is unchanged.

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Research wiki: neurotechnology and justice</title>
<style>
:root{--paper:#f4f0e8;--ink:#1d1b18;--rule:#d9d2c3;--red:#9b2335;--mute:#5b564c;--ok:#1f6b3a;--warn:#7d4a00;--ins:#fbf0b5;--serif:Georgia,"Times New Roman",serif;--mono:ui-monospace,Menlo,Consolas,monospace}
*{box-sizing:border-box}
body{margin:0;background:var(--paper);color:var(--ink);font:16px/1.55 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif}
[hidden]{display:none!important}
.wrap{max-width:1200px;margin:0 auto;padding:0 20px}
a{color:var(--red)}
:focus-visible{outline:3px solid var(--red);outline-offset:2px}
.mono{font:11.5px/1.5 var(--mono);letter-spacing:.07em;text-transform:uppercase}
.mn{font:12px/1.5 var(--mono);color:var(--mute);margin:4px 0}
.mute{color:var(--mute)}
header.wrap{display:flex;justify-content:space-between;gap:24px;flex-wrap:wrap;padding-top:22px;padding-bottom:14px}
header h1{font:400 30px/1.15 var(--serif);margin:4px 0 8px;max-width:30ch}
header .src{margin:0;font-size:14px;max-width:70ch}
header .hr{text-align:right;max-width:430px}
header .hr p{margin:2px 0}
#tabwrap{border-top:1px solid var(--rule);border-bottom:1px solid var(--rule)}
[role=tablist]{display:flex;flex-wrap:wrap}
[role=tab]{background:none;border:0;border-bottom:3px solid transparent;font:12px var(--mono);letter-spacing:.08em;text-transform:uppercase;padding:13px 18px;color:var(--ink);cursor:pointer}
[role=tab][aria-selected=true]{color:var(--red);border-bottom-color:var(--red)}
.panel{padding:24px 0 40px}
.q{margin:0 0 14px;color:var(--mute)}
.btn{font:12px var(--mono);letter-spacing:.06em;text-transform:uppercase;border:1px solid var(--ink);background:transparent;color:var(--ink);padding:9px 14px;cursor:pointer;margin:2px 4px 2px 0}
.btn.pri{background:var(--red);border-color:var(--red);color:#fff}
.btn.sm{padding:3px 8px;font-size:11px}
.btn:disabled{opacity:.45;cursor:not-allowed}
.link{background:none;border:0;padding:0;color:var(--red);text-decoration:underline;cursor:pointer;font:inherit}
h2{font:400 26px/1.2 var(--serif);margin:6px 0 8px}
h3{font:400 20px/1.3 var(--serif);margin:22px 0 6px}
h4{font:700 16px/1.3 var(--serif);margin:16px 0 4px}
.fig{font:400 19px/1.3 var(--serif);margin:24px 0 6px}
.fig .mono{color:var(--red);margin-right:8px}
.big{font:400 52px/1.05 var(--serif);margin:8px 0}
.big small{font:12px var(--mono);letter-spacing:.07em;text-transform:uppercase;color:var(--mute)}
.pg{display:grid;grid-template-columns:320px minmax(0,900px);gap:36px}
@media(max-width:900px){.pg{grid-template-columns:1fr}header .hr{text-align:left}}
input[type=search],input[type=text],textarea{width:100%;font:16px system-ui,sans-serif;padding:8px 10px;border:1px solid var(--ink);background:#fbf9f4;color:var(--ink)}
label{display:block;font:11.5px var(--mono);letter-spacing:.07em;text-transform:uppercase;margin:10px 0 4px}
label.inl{display:inline;text-transform:none;letter-spacing:0;font:14px system-ui,sans-serif}
.grp{margin:16px 0 4px;font:11.5px var(--mono);letter-spacing:.08em;text-transform:uppercase;color:var(--mute);border-bottom:1px solid var(--rule)}
.li{display:block;padding:6px 8px;border-left:3px solid transparent;text-decoration:none;color:var(--ink);border-bottom:1px solid var(--rule)}
.li[aria-current=page]{border-left-color:var(--red);background:#ece6d8}
.li span{display:block;font:11.5px var(--mono);color:var(--mute)}
.tag{color:var(--red)!important;font-weight:700}
.badges{display:flex;flex-wrap:wrap;gap:6px;margin:6px 0}
.badge{font:11.5px var(--mono);letter-spacing:.05em;border:1px solid var(--rule);padding:2px 7px}
.md p,.md li{max-width:72ch}
.md h3{border-top:1px solid var(--rule);padding-top:12px}
.md .ins{background:var(--ins);border-left:3px solid #b8960b;padding:3px 10px;margin:8px 0}
.md .ctx{color:#6a655b}
.md pre{white-space:pre-wrap;font:13px var(--mono)}
.dangling{color:var(--red);border-bottom:1px dashed var(--red)}
.pin{display:inline-block;border:1px solid #bdb5a2;background:#fbf9f4;padding:0 4px;margin:0 1px;font-size:14px;line-height:1.5;vertical-align:baseline;max-width:100%}
.pin.struck .pinlab{text-decoration:line-through}
.pinlab{background:none;border:0;padding:0;color:var(--red);text-decoration:underline;cursor:pointer;font:inherit}
.pin .reg{font:11px var(--mono);margin:0 4px}
.vf{font:11px var(--mono);margin-right:4px}
.vf.ok{color:var(--ok)}.vf.no{color:var(--warn)}.vf.diff{color:var(--mute)}
.pinx{background:none;border:0;cursor:pointer;color:var(--ink);padding:0 3px;font-size:13px}
.pinbody{display:block;white-space:normal;max-width:62ch;margin:4px 0 6px;font-size:14px}
.pinbody q{display:block;font-style:italic;margin-bottom:4px}
.pinbody .pl{display:block;margin:2px 0;color:#3b372f}
.pinbody .warn{color:var(--warn)}
table{border-collapse:collapse;width:100%;font-size:15px}
caption{text-align:left;font:11.5px var(--mono);letter-spacing:.08em;text-transform:uppercase;padding:6px 0;color:var(--mute)}
th,td{border-bottom:1px solid var(--rule);padding:6px 8px;text-align:left;vertical-align:top}
th{font:11px var(--mono);letter-spacing:.08em;text-transform:uppercase}
.num{text-align:right;font-variant-numeric:tabular-nums}
.card{border-top:2px solid var(--ink);margin:24px 0;padding-top:10px}
.card .claim{font:700 18px/1.35 var(--serif);margin:0}
.verdict{font:400 44px/1.1 var(--serif);margin:8px 0;color:var(--red)}
.leanbar{height:14px;background:var(--rule);max-width:520px}
.leanbar i{display:block;height:100%;background:var(--red)}
.notice{background:#ebe5d6;border-left:3px solid var(--mute);padding:10px 14px;margin:0 0 14px;font-size:15px}
.chip{display:inline-block;border:1px solid var(--red);color:var(--red);padding:1px 8px;margin:2px 4px 2px 0;font:12px var(--mono)}
fieldset{border:1px solid var(--rule);padding:12px 16px;margin:14px 0}
legend{font:11.5px var(--mono);letter-spacing:.07em;text-transform:uppercase;padding:0 6px}
.steps{display:flex;flex-wrap:wrap;gap:6px 24px;list-style:none;padding:0;margin:8px 0 14px;font:12px var(--mono);text-transform:uppercase;letter-spacing:.06em;color:var(--mute)}
.steps .on{color:var(--red);border-bottom:2px solid var(--red)}
.runline{font:15px var(--serif);margin:6px 0}
.runline b{font:400 40px var(--serif);margin:0 8px 0 4px}
.pass{color:var(--ok);font-weight:700}.check{color:var(--red);font-weight:700}.na{color:var(--mute)}
details{border-bottom:1px solid var(--rule);padding:6px 0}
summary{cursor:pointer;font-weight:600}
.fail{border:1px solid var(--warn);padding:8px 14px;margin:14px 0}
.toast{position:fixed;left:16px;bottom:16px;background:var(--ink);color:#fff;font:12px var(--mono);padding:8px 12px;max-width:80vw}
.sec{border-top:1px solid var(--rule);padding-top:10px}
.ail{margin:0 0 6px}
pre.raw{white-space:pre-wrap;font:12px var(--mono);border:1px solid var(--rule);padding:8px;max-height:260px;overflow:auto}
footer.wrap{border-top:1px solid var(--rule);padding-top:12px;padding-bottom:30px}
footer p{margin:2px 0}
.mapbox{position:relative}
#mapsvg{display:block;width:100%;height:auto;border-top:1px solid var(--rule);border-bottom:1px solid var(--rule)}
#maptip{position:absolute;z-index:2;background:var(--ink);color:#fff;font:13px/1.4 system-ui,sans-serif;padding:6px 10px;max-width:260px;pointer-events:none}
.mapinfo{min-height:118px}
.mapname{font:400 24px/1.2 var(--serif);margin:0 0 2px}
.lg i{display:inline-block;width:12px;height:12px;border-radius:50%;margin:0 5px 0 14px;vertical-align:-1px}
.ed{fill:none;stroke:#8d8678;stroke-width:1;opacity:.35}
.sel .ed{opacity:.06}
.sel .ed.out{stroke:var(--red);stroke-width:1.8;opacity:.9}
.sel .ed.in{stroke:var(--ink);stroke-width:1.8;opacity:.85}
.nd{cursor:pointer;outline:none}
.nd circle{stroke:var(--paper);stroke-width:1.5}
.sel .nd{opacity:.25}
.sel .nd.nb,.sel .nd.cur{opacity:1}
.nd.cur circle{stroke:var(--red);stroke-width:3.5}
.nd:focus-visible circle{stroke:var(--red);stroke-width:4}
.lb{display:none;font:11px var(--mono);fill:var(--ink);paint-order:stroke;stroke:var(--paper);stroke-width:3px;pointer-events:none}
.nd.top .lb,.nd.show .lb{display:block}
</style>
</head>
<body>
<header class="wrap">
 <div>
  <p class="mono mute" style="margin:0">WIKI · neurotechnology and justice</p>
  <h1>Research wiki: neurotechnology in the administration of justice</h1>
  <p class="src" id="hline"></p>
 </div>
 <div class="hr">
  <p class="mn" id="strip" aria-live="polite"></p>
  <p class="mn">This page has no storage: changes live in it until you download them (tab 05)</p>
 </div>
</header>
<div id="tabwrap"><div class="wrap"><div role="tablist" id="tabs" aria-label="Wiki workspace"></div></div></div>
<main class="wrap">
 <section class="panel" role="tabpanel" id="p0" aria-labelledby="t0">
  <p class="q mono">What does the wiki say?</p>
  <div class="pg">
   <aside>
    <label for="flt">title, tag or slug</label>
    <input type="search" id="flt" autocomplete="off">
    <p class="big" aria-live="polite"><span id="fn">0</span> <small id="ftot"></small></p>
    <p class="mn">How this is computed: pages whose title, slug or a tag contains your text, counted by this page.</p>
    <div id="plist"></div>
   </aside>
   <article id="pview"></article>
  </div>
 </section>
 <section class="panel" role="tabpanel" id="p1" aria-labelledby="t1" hidden>
  <p class="q mono">What does the wiki answer, and is it worth filing?</p>
  <div class="notice" id="notice" aria-live="polite"></div>
  <label for="q">Your question</label>
  <textarea id="q" rows="3"></textarea>
  <p><button class="btn pri" id="askBtn" data-act="askgo">Ask the wiki</button><button class="btn" id="askStop" data-act="stop" hidden>Stop</button> <span class="mn" id="askProg" aria-live="polite"></span></p>
  <div id="askOut"></div>
 </section>
 <section class="panel" role="tabpanel" id="p2" aria-labelledby="t2" hidden>
  <p class="q mono">What would the waiting document change?</p>
  <div id="ingOut"></div>
 </section>
 <section class="panel" role="tabpanel" id="p3" aria-labelledby="t3" hidden>
  <p class="q mono">Can I trust this?</p>
  <div id="chkOut"></div>
 </section>
 <section class="panel" role="tabpanel" id="p4" aria-labelledby="t4" hidden>
  <p class="q mono">What has changed, where do the sources disagree, and how do I take it away?</p>
  <p><input type="checkbox" id="newest" checked> <label class="inl" for="newest">Log: newest first</label></p>
  <div id="recOut"></div>
 </section>
 <section class="panel" role="tabpanel" id="p5" aria-labelledby="t5" hidden>
  <p class="q mono">How are the pages connected?</p>
  <p class="mn" id="maplg"></p>
  <p class="mn">How this is computed: one line for each [[link]] in a page's body that points to another page (a link written twice in one page counts once); two pages that link to each other get two lines, bending opposite ways. Positions come from a fixed layout with no random start, so the map looks the same every time.</p>
  <div id="mapinfo" class="mapinfo" aria-live="polite"></div>
  <div class="mapbox"><svg id="mapsvg" viewBox="0 0 1000 640" role="group" aria-label="Map of the wiki: one node per page, one line per link"></svg><div id="maptip" role="tooltip" hidden></div></div>
  <p class="mn" id="mapsum"></p>
 </section>
</main>
<footer class="wrap"><p class="mn" id="foot"></p></footer>
<div class="toast" id="toast" aria-live="polite" hidden></div>
<script>
(function(){
'use strict';
const FENCE='\x60\x60\x60',INS='<!--ins-->',INE='<!--/ins-->';
const $=(s,r)=>(r||document).querySelector(s);
const esc=s=>String(s==null?'':s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const uniq=a=>[...new Set(a)];
const today=()=>new Date().toISOString().slice(0,10);
const fmtN=n=>Number(n).toLocaleString('en-GB');
const escRe=s=>s.replace(/[.*+?^${}()|[\]\\]/g,'\\$&');
const slugify=s=>String(s||'').normalize('NFKD').replace(/[̀-ͯ]/g,'').toLowerCase().replace(/[^a-z0-9]+/g,'-').replace(/^-+|-+$/g,'');
const REGN={a:'treaty law',b:'General Comments',c:'UN, agency and soft-law reports',d:'national human rights institution',e:'civil society',f:'scholarship'};
const REGS={a:'treaty law',b:'General Comment',c:'UN report',d:'NHRI',e:'civil society',f:'scholarship'};
const WGT={a:5,b:4,c:3,d:2,e:1,f:.5};
const PIN_RE=/\[([^\]]+)\]\(pin:([^#\s)]+)#p(\d+)(?: "([^"]*)")?\) ?(✓|⚠)/;
const INL_RE=new RegExp(PIN_RE.source+'|\\[\\[([^\\]|#]+)(?:[|#][^\\]]*)?\\]\\]|\\[([^\\]]+)\\]\\((https?:[^)\\s]+)\\)','g');
const WD=window.WORKSHOP_DATA||{};
const wiki=WD.wiki||{};
const pages=(wiki.pages||[]).map(p=>{const fm=Object.assign({links:[],sources:[],tags:[],register:[]},p.frontmatter||{});['links','sources','tags','register'].forEach(k=>{if(!Array.isArray(fm[k]))fm[k]=[];});return{slug:p.slug,type:p.type||fm.type||'',title:p.title||fm.title||p.slug,frontmatter:fm,body:String(p.body||'')};});
const docs=(WD.library&&WD.library.records)||[];
const docMap=new Map(docs.map(d=>[d.id,d]));
let indexMd=String(wiki.index||''),logMd=String(wiki.log||''),tensMd=String(wiki.tensions||'');
const orig=new Map(pages.map(p=>[p.slug,p.body]));
const S={calls:0,chars:0,passages:0},callLog=[],changes=[],sessionHeads=[],sessionTens=[];
const RUN={ask:null,ingest:null};
let P_MAP=new Map(),backl=new Map(),regCache=new Map(),vCache=new Map(),cur=null,ING=null,warn0=0;
if(!pages.length){document.body.innerHTML='<p style="padding:30px;font-family:sans-serif">No wiki data is attached. Drag the research wiki from "Your files" into the chat.</p>';return;}

/* ---------- normalising, parsing, verifying ---------- */
function normM(s,m){return String(s==null?'':s).normalize('NFKC').replace(/[“”„]/g,'"').replace(/[‘’]/g,"'").replace(/[–—]/g,'-').replace(/­/g,'').replace(/-\s+/g,m?'':'-').replace(/\s+/g,' ').trim();}
const norm=s=>normM(s,0);
function pn(x,m){x._n=x._n||[];if(x._n[m]==null)x._n[m]=normM(x.text,m);return x._n[m];}
function parsePins(body){const re=new RegExp(PIN_RE.source,'g');const a=[];let m;while((m=re.exec(body)))a.push({label:m[1],id:m[2],page:+m[3],quote:m[4]||'',mark:m[5],raw:m[0]});return a;}
function verify(p,o){o=o||{};const k=[p.id,p.page,p.label,p.quote,o.inbox||''].join('\u0001');if(vCache.has(k))return vCache.get(k);const r=verify0(p,o);vCache.set(k,r);return r;}
function verify0(p,o){
 const d=docMap.get(p.id);if(!d)return{ok:false,reason:'unknown document "'+p.id+'"'};
 if(d.status==='inbox'&&o.inbox!==p.id)return{ok:false,reason:'the document is still in the inbox, not in the wiki'};
 if(!p.quote)return{ok:false,reason:'the pin has no quote'};
 const cands=(d.passages||[]).filter(x=>x.page===p.page);
 if(!cands.length)return{ok:false,reason:'no passage starts on PDF page '+p.page};
 let bad=null;
 for(const x of cands){
  let hit=false;
  for(let m=0;m<2&&!hit;m++){
   const t=pn(x,m),fr=p.quote.split(/…|\.\.\./).map(s=>normM(s,m)).filter(Boolean);let pos=0;hit=fr.length>0;
   for(const f of fr){const i=t.indexOf(f,pos);if(i<0){hit=false;break;}pos=i+f.length;}
  }
  if(!hit)continue;
  const want=x.paragraph?'para. '+x.paragraph:'p. '+x.page_label;
  if(new RegExp(escRe(want)+'(?![0-9A-Za-z])').test(p.label))return{ok:true,passage:x};
  bad={reason:'label should contain "'+want+'"',passage:x};
 }
 return bad?Object.assign({ok:false},bad):{ok:false,reason:'the quote is not in any passage that starts on PDF page '+p.page};
}
const pinKey=p=>p.id+'|'+p.page+'|'+norm(p.quote);
function reindex(){
 P_MAP=new Map(pages.map(p=>[p.slug,p]));regCache.clear();vCache.clear();backl=new Map();
 for(const p of pages){p._links=uniq([...p.body.matchAll(/\[\[([^\]|#]+)/g)].map(m=>m[1].trim()));p._pins=parsePins(p.body);}
 for(const p of pages)for(const s of p._links){if(!backl.has(s))backl.set(s,new Set());backl.get(s).add(p.slug);}
 for(const p of pages)p._pins.forEach(x=>{x.v=verify(x);});
}
function regOf(id){
 if(regCache.has(id))return regCache.get(id);
 const same=(a,b)=>a.length===b.length&&a.every((x,i)=>x===b[i]);
 let sp=pages.find(p=>p.type==='source'&&same(p.frontmatter.sources,[id]))||pages.find(p=>p.frontmatter.status==='stub'&&(same(p.frontmatter.sources,[id])||p.slug===slugify(id)));
 const r=sp&&sp.frontmatter.register.length?sp.frontmatter.register.join(''):'?';regCache.set(id,r);return r;
}
const regLine=id=>{const r=regOf(id);return r==='?'?'(?) register unknown':r.split('').map(x=>'('+x+') '+(REGS[x]||'')).join(', ');};
function citeAs(d){
 const c={};for(const p of pages)for(const x of p._pins)if(x.id===d.id){const t=x.label.split(/, (?:para\.|p\.)/)[0];c[t]=(c[t]||0)+1;}
 const best=Object.entries(c).sort((a,b)=>b[1]-a[1])[0];
 return best?best[0]:(d.symbol||((d.author||'')+' '+(d.year||'')).trim());
}
const mkPin=(d,x,q)=>{const quote=String(q).replace(/"([^"]*)"/g,'“$1”').replace(/"/g,'”').trim();const label=citeAs(d)+', '+(x.paragraph?'para. '+x.paragraph:'p. '+x.page_label);return{label,id:d.id,page:x.page,quote,mark:'✓',raw:'['+label+'](pin:'+d.id+'#p'+x.page+' "'+quote+'") ✓'};};
function parseContested(t){
 const o={claim:'',verdict:'',note:'',pos:[]};
 for(const l of t.split('\n')){let m;
  if((m=l.match(/^claim:\s*(.*)$/)))o.claim=m[1];else if((m=l.match(/^verdict:\s*(.*)$/)))o.verdict=m[1].trim();else if((m=l.match(/^note:\s*(.*)$/)))o.note=m[1];
  else if((m=l.match(/^([+\-~])\s*(.*)$/))){const q=m[2].split(' | ');o.pos.push({sign:m[1],reg:(q[0]||'').trim().toLowerCase(),pin:q[1]||'',gloss:q[2]||'',page:(q[3]||'').trim()});}}
 return o;
}
function lean(pos){let t=0,s=0;for(const p of pos){const w=WGT[p.reg]||0;t+=w;s+=p.sign==='+'?w:p.sign==='~'?w/2:0;}return t?s/t:null;}
const parseTens=()=>tensMd.split(/^###\s+/m).slice(1).map((t,i)=>{const nl=t.indexOf('\n'),m=t.match(/card:\**\s*\[\[([^\]|#]+)/);return{i,head:(nl<0?t:t.slice(0,nl)).trim(),card:m?m[1].trim():null,body:nl<0?'':t.slice(nl+1)};});
const parseLog=()=>logMd.split(/^##\s+/m).slice(1).map(t=>{const nl=t.indexOf('\n');return{head:(nl<0?t:t.slice(0,nl)).trim(),body:nl<0?'':t.slice(nl+1).trim()};});
const hasCards=p=>p.body.includes(FENCE+'contested');
function plainFirst(md,n){n=n||170;let t=String(md||'').split('\n').filter(l=>l.trim()&&!/^#/.test(l)&&!l.startsWith('<!--'))[0]||'';const m=t.match(/\*\*One-liner\.\*\*\s*(.*)/);if(m)t=m[1];t=t.replace(new RegExp(PIN_RE.source,'g'),'').replace(/\[\[([^\]|#]+)\]\]/g,'$1').replace(/\[([^\]]+)\]\([^)]*\)/g,'$1').replace(/[*_]/g,'').replace(/\s+/g,' ').trim();return t.length>n?t.slice(0,n-1).replace(/\s+\S*$/,'')+'…':t;}
const stripIns=b=>b.replace(/^<!--\/?ins-->\n?/gm,'').replace(/\n{3,}/g,'\n\n');
const insPart=b=>{const o=[];b.replace(/<!--ins-->\n([\s\S]*?)\n<!--\/ins-->/g,(m,x)=>{o.push(x);return m;});return o.join('\n\n');};
function insertAt(body,after,md){
 const L=body.replace(/\s+$/,'').split('\n'),block=['',INS,md.trim(),INE,''];let note=null;
 if(after&&after!=='end'){
  const want=norm(String(after).replace(/^#+\s*/,'')).toLowerCase(),i=L.findIndex(l=>/^#{1,6}\s/.test(l)&&norm(l.replace(/^#+\s*/,'')).toLowerCase()===want);
  if(i>=0){const lv=L[i].match(/^#+/)[0].length;let e=i+1;while(e<L.length){const m=L[e].match(/^(#{1,6})\s/);if(m&&m[1].length<=lv)break;e++;}while(e>i+1&&!L[e-1].trim())e--;L.splice(e,0,...block);return{body:L.join('\n'),note};}
  note='heading "'+after+'" not found; added at the end of the page';
 }
 L.push(...block);return{body:L.join('\n'),note};
}

/* ---------- markdown rendering ---------- */
const fmt=t=>esc(t).replace(/\*\*(.+?)\*\*/g,'<strong>$1</strong>').replace(/(^|[\s(])\*(?!\s)(.+?)\*(?=[\s).,;:!?]|$)/g,'$1<em>$2</em>');
function inline(s,ctx){
 ctx=ctx||{};const re=new RegExp(INL_RE.source,'g');let out='',last=0,m;
 while((m=re.exec(s))){
  out+=fmt(s.slice(last,m.index));last=re.lastIndex;
  if(m[2])out+=pinChip({label:m[1],id:m[2],page:+m[3],quote:m[4]||'',mark:m[5]},ctx);
  else if(m[6]){const sl=m[6].trim();out+=P_MAP.has(sl)?'<a href="#'+esc(sl)+'">'+esc(P_MAP.get(sl).title)+'</a>':'<span class="dangling">'+esc(sl)+' (no page)</span>';}
  else out+='<a href="'+esc(m[8])+'" target="_blank" rel="noopener">'+fmt(m[7])+'</a>';
 }
 return out+fmt(s.slice(last));
}
function pinChip(p,ctx){
 const r=ctx.pinCheck?ctx.pinCheck(p):verify(p),d=docMap.get(p.id),reg=regOf(p.id),x=r.passage;
 let h='<span class="pin'+(r.struck?' struck':'')+'"><button type="button" class="pinlab" data-id="'+esc(p.id)+'" data-page="'+p.page+'" aria-label="Open '+esc(p.label)+' at PDF page '+p.page+'">'+esc(p.label)+'</button>';
 h+='<span class="reg" title="'+esc(REGN[reg]||'')+'">('+esc(reg)+')</span><span class="vf '+(r.ok?'ok':'no')+'">'+(r.ok?'✓ verified':'⚠ not found')+'</span>';
 if(r.note)h+='<span class="vf no">'+esc(r.note)+'</span>';
 if(r.ok?p.mark!=='✓':p.mark==='✓')h+='<span class="vf diff">page says '+esc(p.mark)+'</span>';
 h+='<button type="button" class="pinx" aria-expanded="false" aria-label="Show the quote for '+esc(p.label)+'">▾</button><span class="pinbody" hidden>';
 h+=p.quote?'<q>'+esc(p.quote)+'</q>':'<em>no quote in this pin</em>';
 h+='<span class="pl">Document: '+(d?esc((d.symbol||d.short_title)+' · '+d.kind+' · '+d.year+(d.status==='inbox'?' · inbox':'')):'unknown')+' · register '+esc(regLine(p.id))+'</span>';
 if(x)h+='<span class="pl">Passage: '+(x.paragraph?'para. '+esc(x.paragraph):'p. '+esc(x.page_label))+' (PDF page '+x.page+'): '+esc(x.text.slice(0,300))+(x.text.length>300?'…':'')+'</span>';
 if(!r.ok)h+='<span class="pl warn">Not verified: '+esc(r.reason||r.note||'')+'. Footnotes, tables and captions are not in the passages, so a pin cannot verify them.</span>';
 return h+'<button type="button" class="openpdf btn sm" data-id="'+esc(p.id)+'" data-page="'+p.page+'" aria-label="Open '+esc(d?d.symbol||d.short_title:p.id)+' at PDF page '+p.page+'">Open the PDF page</button></span></span>';
}
function contestedCard(txt,ctx){
 const c=parseContested(txt),L=lean(c.pos),te=ctx.slug?parseTens().find(e=>e.card===ctx.slug):null,SG={'+':'supports','-':'contests','~':'mixed'};
 let h='<section class="card"><p class="claim">'+inline(c.claim,ctx)+'</p><p class="verdict">'+esc((c.verdict||'no verdict').replace(/-/g,' '))+'</p><p>'+inline(c.note,ctx)+'</p>';
 if(te)h+='<p class="mn"><button class="link" data-act="gotens" data-arg="'+te.i+'">in the tensions register</button></p>';
 h+='<h4 class="fig"><span class="mono">FIG.01</span> Lean bar</h4>';
 h+=L==null?'<p class="mn">No weighted positions.</p>':'<div class="leanbar" role="img" aria-label="support '+Math.round(L*100)+' percent"><i style="width:'+Math.round(L*100)+'%"></i></div><p class="mn">descriptive: support '+Math.round(L*100)+'% of weighted positions, weights a 5 · b 4 · c 3 · d 2 · e 1 · f ½; the verdict is the answer</p>';
 h+='<table><caption>Positions on this claim</caption><thead><tr><th scope="col">Position</th><th scope="col">Register</th><th scope="col">Pin</th><th scope="col">Gloss</th><th scope="col">Page</th></tr></thead><tbody>';
 h+=c.pos.map(p=>'<tr><td>'+(SG[p.sign]||p.sign)+'</td><td>('+esc(p.reg)+') '+esc(REGS[p.reg]||'')+'</td><td>'+inline(p.pin,ctx)+'</td><td>'+inline(p.gloss,ctx)+'</td><td>'+inline(p.page,ctx)+'</td></tr>').join('');
 return h+'</tbody></table></section>';
}
function renderMd(md,ctx){
 ctx=ctx||{};const L=String(md||'').replace(/\r/g,'').split('\n'),out=[];let i=0,ins=false;
 const cl=()=>ctx.mark?(ins?' class="ins"':' class="ctx"'):'';
 const bul=/^\s*[-*]\s+/,num=/^\s*\d+[.)]\s+/;
 while(i<L.length){
  const ln=L[i];
  if(ln.trim()===INS){ins=true;i++;continue;}
  if(ln.trim()===INE){ins=false;i++;continue;}
  const f=ln.match(/^\x60\x60\x60(\w*)\s*$/);
  if(f){const buf=[];i++;while(i<L.length&&!/^\x60\x60\x60\s*$/.test(L[i])){buf.push(L[i]);i++;}i++;
   out.push(f[1]==='contested'?(ctx.mark?'<div'+cl()+'>':'<div>')+contestedCard(buf.join('\n'),ctx)+'</div>':'<pre'+cl()+'>'+esc(buf.join('\n'))+'</pre>');continue;}
  const hm=ln.match(/^(#{1,6})\s+(.*)$/);
  if(hm){const lv=Math.min(hm[1].length+2,6);out.push('<h'+lv+cl()+'>'+inline(hm[2],ctx)+'</h'+lv+'>');i++;continue;}
  if(bul.test(ln)||num.test(ln)){
   const ord=num.test(ln),re=ord?num:bul,items=[];
   while(i<L.length&&re.test(L[i])){let t=L[i].replace(re,'');i++;while(i<L.length&&/^\s{2,}\S/.test(L[i])&&!bul.test(L[i])&&!num.test(L[i])){t+=' '+L[i].trim();i++;}items.push(t);}
   out.push('<'+(ord?'ol':'ul')+cl()+'>'+items.map(t=>'<li>'+inline(t,ctx)+'</li>').join('')+'</'+(ord?'ol':'ul')+'>');continue;}
  if(!ln.trim()){i++;continue;}
  const buf=[ln];i++;
  while(i<L.length&&L[i].trim()&&!/^(#{1,6}\s|\x60\x60\x60|<!--)/.test(L[i])&&!bul.test(L[i])&&!num.test(L[i])){buf.push(L[i]);i++;}
  out.push('<p'+cl()+'>'+inline(buf.join(' '),ctx)+'</p>');
 }
 return out.join('\n');
}

/* ---------- header, tabs, helpers ---------- */
const TABS=['PAGES','ASK','INGEST','CHECK','RECORD','MAP'];
const tabLabel=i=>'0'+(i+1)+' '+TABS[i]+(((i===1&&RUN.ask)||(i===2&&RUN.ingest))?' · running':'');
let toastT=null;
function say(m){const t=$('#toast');t.textContent=m;t.hidden=false;clearTimeout(toastT);toastT=setTimeout(()=>{t.hidden=true;},4500);}
function buildTabs(){
 $('#tabs').innerHTML=TABS.map((n,i)=>'<button role="tab" id="t'+i+'" aria-controls="p'+i+'" aria-selected="'+(i===0)+'" tabindex="'+(i===0?0:-1)+'">'+tabLabel(i)+'</button>').join('');
 $('#tabs').addEventListener('keydown',e=>{
  const i=TABS.findIndex((_,k)=>$('#t'+k)===document.activeElement);if(i<0)return;
  const N=TABS.length,k={ArrowRight:(i+1)%N,ArrowLeft:(i+N-1)%N,Home:0,End:N-1}[e.key];if(k==null)return;e.preventDefault();selectTab(k,true);
 });
 $('#tabs').addEventListener('click',e=>{const b=e.target.closest('[role=tab]');if(b)selectTab(+b.id.slice(1),false);});
}
function selectTab(i,focus){TABS.forEach((_,k)=>{const t=$('#t'+k);t.setAttribute('aria-selected',k===i);t.tabIndex=k===i?0:-1;$('#p'+k).hidden=k!==i;});if(focus)$('#t'+i).focus();}
function updTabs(){TABS.forEach((_,k)=>{const t=$('#t'+k);if(t)t.textContent=tabLabel(k);});}
const allPins=()=>pages.flatMap(p=>p._pins);
function updHeader(){
 const t={};pages.forEach(p=>{t[p.type]=(t[p.type]||0)+1;});
 const nm=[['source','source','sources'],['concept','concept','concepts'],['entity','entity','entities'],['question','question','questions']];
 const parts=nm.map(([k,s,pl])=>(t[k]||0)+' '+((t[k]||0)===1?s:pl));
 Object.keys(t).filter(k=>!nm.some(n=>n[0]===k)).forEach(k=>parts.push(t[k]+' '+(k||'other')));
 const ap=allPins(),ok=ap.filter(x=>x.v.ok).length,inbox=docs.filter(d=>d.status==='inbox').length;
 $('#hline').textContent=pages.length+' pages ('+parts.join(', ')+') · '+fmtN(ap.length)+' pins, '+fmtN(ok)+' verified by this page · '+docs.length+' documents, '+inbox+' in the inbox · built '+(wiki.built||'date unknown');
 $('#strip').textContent='Changes this session: '+changes.length+' · Calls to the model: '+S.calls+' · Passages that left the browser: '+S.passages;
 $('#foot').textContent=(wiki.source||'research wiki')+' · built '+(wiki.built||'unknown')+' · Counting, matching and verification are done by this page\'s code; the model is called only when you press Ask, Ingest or a retry button.';
}
async function copyText(t){try{await navigator.clipboard.writeText(t);return true;}catch(e){const a=document.createElement('textarea');a.value=t;document.body.appendChild(a);a.select();let ok=false;try{ok=document.execCommand('copy');}catch(_){}a.remove();return ok;}}
function openSrc(id,page){if(window.studio&&studio.openSource)studio.openSource(id,page);else say('The PDF viewer is not available in this preview.');}
function startRun(k){const r={stopped:false};r.sig=new Promise(res=>{r.halt=()=>{r.stopped=true;res('\u0000stopped');};});RUN[k]=r;updTabs();return r;}
function endRun(k){RUN[k]=null;updTabs();}
const yamlOf=fm=>Object.entries(fm).map(([k,v])=>k+': '+(Array.isArray(v)?'['+v.map(x=>JSON.stringify(x)).join(', ')+']':JSON.stringify(v))).join('\n');
const pageMd=p=>'---\n'+yamlOf(p.frontmatter)+'\n---\n\n'+p.body;
function parseJSON(raw){
 const t=String(raw||'').trim(),tries=[t,t.replace(/^\x60\x60\x60(?:json)?\s*/i,'').replace(/\s*\x60\x60\x60$/,''),t.slice(t.indexOf('{'),t.lastIndexOf('}')+1)];
 for(const s of tries){try{const v=JSON.parse(s);if(v&&typeof v==='object')return v;}catch(e){}}return null;
}
const PRE='You are helping maintain a research wiki on neurotechnology in the administration of justice. A pin is written [label](pin:DOCUMENT_ID#pPDFPAGE "verbatim quote") ✓ . Quote only words that stand in the passages given; the code will check every quote against the library and discards anything that does not match. Copy pins exactly as given. Reply with JSON only.\n\n';
async function callModel(prompt,o){
 o=o||{};const E={label:o.label,chars:prompt.length,passages:o.passages||0,parsed:false,unknown:0};callLog.push(E);
 S.calls++;S.chars+=prompt.length;S.passages+=E.passages;updHeader();
 let res;
 try{
  if(!window.studio||!studio.ask)throw new Error('studio.ask is not available here');
  const p=studio.ask(prompt,{json:true});res=await(o.run?Promise.race([p,o.run.sig]):p);
 }catch(e){return{ok:false,raw:'',error:String(e&&e.message||e),E};}
 if(res==='\u0000stopped')return{ok:false,stopped:true,E};
 const raw=typeof res==='string'?res:JSON.stringify(res),data=(res&&typeof res==='object')?res:parseJSON(raw);
 if(!data)return{ok:false,raw,error:'The answer was not valid JSON.',E};
 E.parsed=true;return{ok:true,data,raw,E};
}
const errHTML=(e,act)=>'<div class="fail"><p><strong>'+esc(e.error)+'</strong> Nothing was filed.</p>'+(e.raw?'<pre class="raw" data-source="ai">'+esc(e.raw)+'</pre>':'')+'<button class="btn" data-act="'+act+'">Retry</button></div>';
function download(name,text,type){const u=URL.createObjectURL(new Blob([text],{type}));const a=document.createElement('a');a.href=u;a.download=name;document.body.appendChild(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(u),1500);}

/* ---------- tab 01 pages ---------- */
function renderList(){
 const q=$('#flt').value.trim().toLowerCase();
 const hit=pages.filter(p=>!q||(p.title+' '+p.slug+' '+p.frontmatter.tags.join(' ')).toLowerCase().includes(q));
 $('#fn').textContent=hit.length;$('#ftot').textContent='of '+pages.length+' pages';
 const types=uniq(['source','concept','entity','question',...pages.map(p=>p.type)]);
 $('#plist').innerHTML=types.map(t=>{
  const g=hit.filter(p=>p.type===t);if(!g.length)return'';
  return'<p class="grp">'+esc(t||'other')+' ('+g.length+')</p>'+g.map(p=>'<a class="li" href="#'+esc(p.slug)+'"'+(cur===p.slug?' aria-current="page"':'')+'>'+esc(p.title)+'<span>'+(p.frontmatter.register.join(' ')||'-')+' · '+p._pins.length+' pins'+(p.frontmatter.status==='stub'?' · <b class="tag">stub</b>':'')+'</span></a>').join('');
 }).join('')||'<p class="mn">No page matches.</p>';
}
function pageHTML(p){
 const fm=p.frontmatter,bodyL=new Set(p._links),from=[...(backl.get(p.slug)||[])].filter(s=>s!==p.slug);
 const lk=s=>P_MAP.has(s)?'<a href="#'+esc(s)+'">'+esc(P_MAP.get(s).title)+'</a>':'<span class="dangling">'+esc(s)+' (no page)</span>';
 let h='<p class="mn"><a href="#">← index</a></p><h2>'+esc(p.title)+'</h2><p class="badges"><span class="badge">'+esc(p.type)+'</span>'+fm.register.map(r=>'<span class="badge">('+esc(r)+') '+esc(REGN[r]||'')+'</span>').join('')+'<span class="badge">'+esc(fm.status||'no status')+'</span><span class="badge">updated '+esc(fm.updated||'?')+'</span>'+(changes.some(c=>c.slug===p.slug)?'<span class="badge" style="color:var(--red)">this session</span>':'')+'</p>';
 h+='<p class="mn">tags: '+(fm.tags.map(esc).join(' · ')||'none')+'</p><div class="md">'+renderMd(p.body.replace(/^#\s+[^\n]*\n+/,''),{slug:p.slug})+'</div>';
 h+='<h3 class="sec">Links out</h3><ul>'+(fm.links.map(s=>'<li>'+lk(s)+(bodyL.has(s)?'':' <span class="mn">frontmatter only</span>')+'</li>').join('')||'<li class="mn">none</li>')+'</ul>';
 h+='<h3>Linked from</h3><ul>'+(from.map(s=>'<li>'+lk(s)+'</li>').join('')||'<li class="mn">no page links here</li>')+'</ul>';
 h+='<h3>Sources</h3><ul>'+(fm.sources.map(id=>{const d=docMap.get(id);return'<li>'+(d?esc(d.short_title||d.title)+' · '+esc(d.kind)+' · '+esc(d.year)+' · <a href="'+esc(d.url)+'" target="_blank" rel="noopener">'+esc(d.symbol||d.url)+'</a>'+(d.status==='inbox'?' · <b class="tag">inbox</b>':''):esc(id)+' (not in the library)')+'</li>';}).join('')||'<li class="mn">none</li>')+'</ul>';
 return h+'<p><button class="btn" data-act="copymd" data-arg="'+esc(p.slug)+'">Copy page as markdown</button></p>';
}
function renderView(){
 const v=$('#pview');
 if(!cur){v.innerHTML='<h2>Index</h2><p class="mn">The catalog of every page. Pick a page on the left or follow a link.</p><div class="md">'+renderMd(indexMd,{})+'</div>';return;}
 const p=P_MAP.get(cur);
 v.innerHTML=p?pageHTML(p):'<p class="mn"><a href="#">← index</a></p><h2>No page "'+esc(cur)+'"</h2><p>The wiki has no page with this slug.</p>';
}
function route(){let h='';try{h=decodeURIComponent(location.hash.slice(1));}catch(e){h=location.hash.slice(1);}cur=h||null;if(h)selectTab(0);renderList();renderView();if(h)window.scrollTo(0,0);}

/* ---------- tab 02 ask ---------- */
const ask={stage:'idle',q:'',chosen:[],sentKeys:new Set(),answer:null,err:null,filing:false,pickOpen:false,fTitle:'',fTags:'',filed:null,prog:''};
const bodiesFor=sl=>sl.map(s=>'=== PAGE '+s+' ===\n'+P_MAP.get(s).body).join('\n\n');
const q1Prompt=q=>PRE+'Choose the wiki pages needed to answer the question. Below is the wiki index. Return JSON {"pages": [slug, ...]} with at most 5 slugs that appear in the index.\n\nQUESTION: '+q+'\n\nINDEX:\n'+indexMd;
const q2Prompt=(q,sl)=>PRE+'Answer the question using only the wiki pages below. Return JSON {"title": short title, "answer": markdown of at most 350 words, "cannot_answer": one or two sentences on what the library cannot answer}. Every claim in the answer carries a pin copied exactly from the pages below, and may link to the pages you used as [[slug]]. Name the register where it matters ((a) treaty law, (b) General Comments, (c) UN, agency and soft-law reports, (d) national human rights institution, (e) civil society, (f) scholarship), keep the document\'s own verb, and never present (c) to (f) as what the treaty requires.\n\nQUESTION: '+q+'\n\n'+bodiesFor(sl);
function renderAskTop(){
 const n=$('#notice'),b=$('#askBtn'),q=($('#q').value||'').trim(),busy=!!RUN.ask;
 if(ask.stage==='pick'&&ask.chosen.length){const pr=q2Prompt(ask.q,ask.chosen);n.innerHTML='Step 2 will send '+ask.chosen.length+' page'+(ask.chosen.length===1?'':'s')+', '+fmtN(pr.length)+' characters (page bodies, instructions and the question) to a language model; 0 library passages have left the browser.';b.textContent='Send '+ask.chosen.length+' page'+(ask.chosen.length===1?'':'s')+' and the question';}
 else{n.innerHTML='Step 1 will send the wiki index ('+fmtN(indexMd.length)+' characters) and your question ('+fmtN(q.length)+' characters) to a language model. No page body and no library passage is sent in this step.';b.textContent=ask.answer?'Ask again':'Ask the wiki';}
 b.disabled=busy;$('#askStop').hidden=!busy;$('#askProg').textContent=ask.prog;
}
function renderAskOut(){
 let h='';
 if(ask.err)h+=errHTML(ask.err,'askretry');
 if(ask.stage==='pick'){
  h+='<h3 class="fig"><span class="mono">STEP 1</span> Pages chosen by the model</h3><p data-source="ai">'+(ask.chosen.map(s=>'<span class="chip">'+esc(P_MAP.get(s).title)+'</span>').join('')||'<span class="mn">none chosen</span>')+'</p><p class="mn"><button class="link" data-act="pickopen" aria-expanded="'+ask.pickOpen+'">Change pages</button></p>';
  if(ask.pickOpen)h+='<fieldset><legend>Tick the pages to send (at most 5)</legend>'+pages.map(p=>'<div><input type="checkbox" name="pick" id="pk-'+esc(p.slug)+'" value="'+esc(p.slug)+'"'+(ask.chosen.includes(p.slug)?' checked':'')+'> <label class="inl" for="pk-'+esc(p.slug)+'">'+esc(p.title)+'</label></div>').join('')+'</fieldset>';
 }
 if(ask.answer)h+=answerHTML();
 $('#askOut').innerHTML=h;
}
function askPinCheck(p){const v=verify(p);if(!ask.sentKeys.has(pinKey(p)))return Object.assign({},v,{ok:false,struck:true,note:'not on the pages sent'});return v;}
function answerHTML(){
 const a=ask.answer,ctx={pinCheck:askPinCheck},pins=parsePins(a.answer),by={};let bad=0;
 pins.forEach(p=>{const r=askPinCheck(p);if(r.ok){const g=regOf(p.id);by[g]=(by[g]||0)+1;}else bad++;});
 let h='<h3 class="fig"><span class="mono">STEP 2</span> Answer</h3><div class="md" data-source="ai"><h3 style="border:0;margin-top:0">'+esc(a.title)+'</h3>'+renderMd(a.answer,ctx)+'<h4>What the library cannot answer</h4><p>'+esc(a.cannot||'The model gave no answer to this.')+'</p></div>';
 h+='<p class="mn">How this is computed: '+pins.length+' pins in the answer; verified by register: '+(Object.entries(by).map(([k,n])=>'('+k+') '+(REGS[k]||'?')+' '+n).join(' · ')||'none')+'; not verified or not on the pages sent: '+bad+'.</p>';
 h+='<p><button class="btn pri" data-act="filecard" aria-expanded="'+ask.filing+'">File as a question page</button></p>';
 if(ask.filing)h+='<fieldset><legend>File as a question page</legend><label for="fT">Title</label><input type="text" id="fT" value="'+esc(ask.fTitle)+'"><label for="fG">Tags, separated by commas</label><input type="text" id="fG" value="'+esc(ask.fTags)+'"><div id="fPrev"></div></fieldset>';
 return h;
}
function buildQuestion(){
 const a=ask.answer,title=(ask.fTitle||a.title).trim(),pins=parsePins(a.answer),bad=pins.filter(p=>!askPinCheck(p).ok).length;
 let slug=slugify(title).slice(0,60)||'question',k=slug,n=2;while(P_MAP.has(slug)){slug=k+'-'+n++;}
 const ids=uniq(pins.map(p=>p.id)),regs=uniq(ids.flatMap(id=>regOf(id).split('')).filter(x=>'abcdef'.includes(x))).sort();
 const links=uniq([...a.answer.matchAll(/\[\[([^\]|#]+)/g)].map(m=>m[1].trim())).filter(s=>P_MAP.has(s));
 const paras=a.answer.trim().split(/\n\s*\n/),body='# '+title+'\n\n**Short answer.** '+paras[0]+'\n\n## Reasoning\n\n'+(paras.length>1?paras.slice(1).join('\n\n'):a.answer.trim())+'\n\n## What the library cannot answer\n\n'+(a.cannot||'Not stated.')+'\n\n## Related\n\n'+(links.map(s=>'- [[' + s + ']]').join('\n')||'- none')+'\n';
 const fm={title,type:'question',tags:ask.fTags.split(',').map(s=>s.trim()).filter(Boolean),register:regs,status:'draft',updated:today(),links,sources:ids};
 return{page:{slug,type:'question',title,frontmatter:fm,body},bad,pins:pins.length};
}
function updFile(){
 const el=$('#fPrev');if(!el||!ask.answer)return;const b=buildQuestion(),fm=b.page.frontmatter;
 const why=b.pins===0?'the answer has no pins':b.bad?b.bad+' pin'+(b.bad===1?'':'s')+' in the answer do not verify':'';
 el.innerHTML='<p class="mn">preview · slug '+esc(b.page.slug)+' · type question · status draft · updated '+fm.updated+' · register '+esc(fm.register.join('')||'-')+' · links '+fm.links.length+' · sources '+fm.sources.length+'</p><div class="md" style="border:1px solid var(--rule);padding:6px 14px">'+renderMd(b.page.body,{pinCheck:askPinCheck})+'</div><p><button class="btn pri" data-act="filedo"'+(why?' disabled':'')+'>File this page</button><button class="btn" data-act="copyans">Copy answer</button>'+(why?' <span class="mn">File this page is disabled: '+esc(why)+'.</span>':'')+'</p>';
}
function idxUpsert(slug,type,line){
 const L=indexMd.split('\n'),k=L.findIndex(l=>/^\s*[-*]\s/.test(l)&&l.includes('[['+slug+']]'));
 if(k>=0){L[k]=line;indexMd=L.join('\n');return;}
 const name={source:'Sources',concept:'Concepts',entity:'Entities',question:'Questions'}[type]||'Other',h=L.findIndex(l=>/^#{1,4}\s/.test(l)&&l.toLowerCase().includes(name.toLowerCase()));
 if(h<0){indexMd=indexMd.replace(/\s*$/,'')+'\n\n## '+name+'\n\n'+line+'\n';return;}
 let e=h+1,last=h;while(e<L.length&&!/^#{1,4}\s/.test(L[e])){if(/^\s*[-*]\s/.test(L[e]))last=e;e++;}
 L.splice(last+1,0,line);indexMd=L.join('\n');
}
function idxCounts(){
 const t={};pages.forEach(p=>{t[p.type]=(t[p.type]||0)+1;});const ok=allPins().filter(x=>x.v.ok).length;
 let h=indexMd.slice(0,800);const rest=indexMd.slice(800);
 h=h.replace(/(\d[\d,]*)(\s+pins)/,(m,a,b)=>(a.includes(',')?fmtN(ok):ok)+b).replace(/(\d+)(\s+pages)/,(m,a,b)=>pages.length+b);
 [['source','sources?'],['concept','concepts?'],['entity','(?:entities|entity)'],['question','questions?']].forEach(([k,re])=>{h=h.replace(new RegExp('(\\d+)(\\s+'+re+'\\b)','i'),(m,a,b)=>(t[k]||0)+b);});
 indexMd=h+rest;
}
function appendLog(head,body){logMd=logMd.replace(/\s*$/,'')+'\n\n## '+head+'\n'+body+'\n';sessionHeads.push(head);}
async function askStep1(){
 const q=$('#q').value.trim();if(!q){ask.prog='Type a question first.';renderAskTop();return;}
 Object.assign(ask,{q,answer:null,filing:false,err:null,chosen:[],stage:'idle',pickOpen:false,prog:'Step 1: sending the index and the question…'});
 const run=startRun('ask');renderAskTop();renderAskOut();
 const r=await callModel(q1Prompt(q),{label:'Ask: choose pages',run});endRun('ask');
 if(r.stopped){ask.prog='Stopped.';renderAskTop();return;}
 if(!r.ok){ask.err={error:r.error,raw:r.raw,retry:1};ask.prog='';renderAskTop();renderAskOut();return;}
 const sl=(Array.isArray(r.data.pages)?r.data.pages:[]).map(String),keep=uniq(sl.filter(s=>P_MAP.has(s))).slice(0,5);
 r.E.unknown=sl.filter(s=>!P_MAP.has(s)).length;ask.chosen=keep;ask.stage='pick';
 ask.prog=keep.length?'The model chose '+keep.length+' page'+(keep.length===1?'':'s')+(r.E.unknown?' ('+r.E.unknown+' slug'+(r.E.unknown===1?'':'s')+' that do not exist dropped)':'')+'.':'The model chose no page that exists. Tick pages yourself under "Change pages".';
 updHeader();renderAskTop();renderAskOut();
}
async function askStep2(){
 if(!ask.chosen.length){ask.prog='Choose at least one page first.';renderAskTop();return;}
 ask.err=null;ask.prog='Step 2: sending '+ask.chosen.length+' pages and the question…';ask.sentKeys=new Set(ask.chosen.flatMap(s=>parsePins(P_MAP.get(s).body).map(pinKey)));
 const run=startRun('ask');renderAskTop();
 const r=await callModel(q2Prompt(ask.q,ask.chosen),{label:'Ask: answer',run});endRun('ask');
 if(r.stopped){ask.prog='Stopped.';renderAskTop();return;}
 if(!r.ok){ask.err={error:r.error,raw:r.raw,retry:2};ask.prog='';renderAskTop();renderAskOut();return;}
 const d=r.data,cn=d.cannot_answer;
 ask.answer={title:String(d.title||ask.q.slice(0,80)).trim(),answer:String(d.answer||'').trim(),cannot:Array.isArray(cn)?cn.join(' '):String(cn||'')};
 if(!ask.answer.answer){ask.answer=null;ask.err={error:'The answer was empty.',raw:r.raw,retry:2};}
 ask.stage='done';ask.fTitle=ask.answer?ask.answer.title:'';ask.fTags='';ask.prog='Answer received. Every pin below was checked by this page.';
 renderAskTop();renderAskOut();
}
function fileQuestion(){
 const b=buildQuestion();if(b.bad||!b.pins)return;const p=b.page,date=today(),n=p.frontmatter.sources.length;
 pages.push(p);reindex();
 idxUpsert(p.slug,'question','- [[' + p.slug + ']] — ' + plainFirst(p.body.replace(/^#[^\n]*\n+/,'').replace('**Short answer.**','')) + ' · (' + p.frontmatter.register.join('') + ') · ✓' + p._pins.filter(x=>x.v.ok).length);
 idxCounts();const head='['+date+'] ask | '+p.title;
 appendLog(head,'Filed [[' + p.slug + ']] as a draft question page from the pages '+ask.chosen.map(s=>'[['+s+']]').join(', ')+'. '+p._pins.length+' pins, all verified by the code, on '+n+' document'+(n===1?'':'s')+'.');
 changes.push({date,kind:'ask',slug:p.slug,change:'new',op:head});
 ask.filed=p.slug;ask.filing=false;ask.prog='Filed: '+p.title+'. It is a draft page in memory; download it on tab 05.';
 refreshAll();say('Filed as a question page.');
}

/* ---------- lint and checks ---------- */
function lint(){
 const R=[],row=(label,count,slugs,extra)=>R.push({label,count,slugs:uniq(slugs),extra:extra||''});
 const idx=uniq([...indexMd.matchAll(/\[\[([^\]|#]+)/g)].map(m=>m[1].trim())),tens=parseTens();
 let a=[];pages.forEach(p=>p._links.forEach(s=>{if(!P_MAP.has(s))a.push(p.slug);}));row('Dangling [[links]]',a.length,a);
 a=pages.filter(p=>![...(backl.get(p.slug)||[])].some(s=>s!==p.slug)).map(p=>p.slug);row('Orphan pages (no page links to them)',a.length,a);
 a=[];pages.forEach(p=>p._pins.forEach(x=>{if(!x.v.ok)a.push(p.slug);}));row('Pins the code could not verify',a.length,a);
 a=[];pages.forEach(p=>p._pins.forEach(x=>{if(!x.v.ok&&x.mark==='✓')a.push(p.slug);}));row('Pins marked ✓ that fail',a.length,a);
 a=pages.filter(p=>{const s=new Set(p.frontmatter.sources),q=new Set(p._pins.map(x=>x.id));return s.size!==q.size||[...s].some(x=>!q.has(x));}).map(p=>p.slug);row('`sources` differ from the documents pinned',a.length,a);
 a=pages.filter(p=>!p._pins.length).map(p=>p.slug);row('Pages with no pins',a.length,a);
 a=[];pages.forEach(p=>uniq([...p.frontmatter.links,...p._links]).forEach(s=>{const o=P_MAP.get(s);if(o&&o!==p&&!uniq([...o.frontmatter.links,...o._links]).includes(p.slug))a.push(p.slug);}));row('Links not reciprocated',a.length,a);
 a=pages.filter(p=>!idx.includes(p.slug)).map(p=>p.slug);row('Pages missing from the index',a.length,a);
 const nopage=idx.filter(s=>!P_MAP.has(s));row('Index lines without a page',nopage.length,[],nopage.join(', '));
 a=[];indexMd.split('\n').forEach(l=>{const m=l.match(/\[\[([^\]|#]+)\]\]/),n=l.match(/✓\s*(\d+)/);if(m&&n&&P_MAP.has(m[1].trim())&&P_MAP.get(m[1].trim())._pins.filter(x=>x.v.ok).length!==+n[1])a.push(m[1].trim());});row('Index ✓N differs from the computed count',a.length,a);
 const cards=new Set(tens.map(t=>t.card).filter(Boolean)),withC=pages.filter(hasCards).map(p=>p.slug);
 a=withC.filter(s=>!cards.has(s));row('Contested cards without a tensions entry',a.length,a);
 const rev=[...cards].filter(s=>!withC.includes(s));row('Tensions entries without a contested card',rev.length,rev.filter(s=>P_MAP.has(s)),rev.filter(s=>!P_MAP.has(s)).join(', '));
 a=pages.filter(p=>p.frontmatter.status==='stub').map(p=>p.slug);row('Stub pages',a.length,a);
 a=[];pages.forEach(p=>p._pins.forEach(x=>{const d=docMap.get(x.id);if(d&&d.status==='inbox')a.push(p.slug);}));row('Pins to a document still in the inbox',a.length,a);
 return R;
}
const slugLinks=(sl,max)=>{max=max||12;const s=sl.slice(0,max).map(x=>P_MAP.has(x)?'<a href="#'+esc(x)+'">'+esc(x)+'</a>':esc(x)).join(', ');return s+(sl.length>max?' +'+(sl.length-max)+' more':'');};
function selfChecks(){
 const L=lint(),g=l=>L.find(r=>r.label.startsWith(l)),C=[],add=(name,text,ok,slugs)=>C.push({name,text,ok,slugs:slugs||[]});
 const all=pages.flatMap(p=>p._pins.map(x=>({p,x}))),m0=(indexMd.match(/(\d[\d,]*) pins/)||[])[1],st=m0?+m0.replace(/,/g,''):null;
 const okN=all.filter(a=>a.x.v.ok).length,fc=all.filter(a=>!a.x.v.ok&&a.x.mark==='✓');
 add('Pins','found '+all.length+'; the index states '+(st==null?'no number':st)+'; verified '+okN+'; marked ✓ but failing '+fc.length,st===all.length&&!fc.length,fc.map(a=>a.p.slug));
 const lb=all.filter(a=>/^label/.test(a.x.v.reason||''));add('Labels','pins whose quote is found but whose label names the wrong paragraph or page: '+lb.length,!lb.length,lb.map(a=>a.p.slug));
 add('Structure','dangling links '+g('Dangling').count+'; orphans '+g('Orphan').count+'; `sources` differing from pinned documents '+g('`sources`').count+'; pages missing from the index '+g('Pages missing').count+'; index lines without a page '+g('Index lines').count+'; contested cards without a tensions entry '+g('Contested cards').count+', the reverse '+g('Tensions entries').count,[g('Dangling'),g('Orphan'),g('`sources`'),g('Pages missing'),g('Index lines'),g('Contested cards'),g('Tensions entries')].every(r=>!r.count),uniq(L.filter(r=>/Dangling|Orphan|sources|missing|Contested|Tensions/.test(r.label)).flatMap(r=>r.slugs)));
 const parsed=callLog.filter(c=>c.parsed).length,unk=callLog.reduce((n,c)=>n+(c.unknown||0),0);
 if(!callLog.length)add('Model answers','no call to the model yet',null);
 else add('Model answers','calls '+callLog.length+'; JSON parsed '+parsed+'; slugs that do not exist, dropped '+unk+(ING?'; takeaways returned '+ING.returned+' = verified '+ING.tk.length+' + could not verify '+ING.failed.length:''),parsed===callLog.length&&(!ING||ING.returned===ING.tk.length+ING.failed.length));
 if(!ING)add('Coverage','no ingest yet',null);
 else{const tot=ING.doc.passages.length;add('Coverage','passages sent '+ING.sent+' of '+tot+'; takeaways naming a passage that was not sent, dropped '+ING.dropped,ING.sent===tot);}
 const warn=all.filter(a=>a.x.mark==='⚠').length,chg=new Set(changes.map(c=>c.slug)),bad=all.filter(a=>chg.has(a.p.slug)&&!a.x.v.ok);
 add('Unverified','⚠ pins in the wiki: '+warn+' (at load: '+warn0+'); pins failing in changed pages: '+bad.length+(ING?'; could not verify '+ING.failed.length+' + verified '+ING.tk.length+' = returned '+ING.returned:''),warn===warn0&&!bad.length&&(!ING||ING.returned===ING.tk.length+ING.failed.length),bad.map(a=>a.p.slug));
 const diff=pages.filter(p=>orig.has(p.slug)&&orig.get(p.slug)!==p.body).map(p=>p.slug),und=diff.filter(s=>!chg.has(s));
 add('Approval','pages whose body differs from the loaded one: '+diff.length+'; of these without an approved card or filing: '+und.length,!und.length,und);
 if(ING&&ING.filed)add('Filing','pages re-parsed and re-verified: '+ING.filed.slugs.length+'; lint checks needing a look before '+ING.filed.before+', after '+ING.filed.after+'; last log entry: '+(parseLog().slice(-1)[0]||{head:'-'}).head,ING.filed.slugs.every(s=>P_MAP.has(s)&&P_MAP.get(s)._pins.every(x=>x.v.ok))&&!g('Index ✓N').count,ING.filed.slugs);
 else add('Filing','nothing filed from an ingest yet',null);
 const ops=uniq(changes.map(c=>c.op)).length;add('Session','changes listed '+changes.length+' in '+ops+' operation'+(ops===1?'':'s')+'; log entries added this session '+sessionHeads.length+'; the download holds '+exportObj().pages.length+' pages, the wiki has '+pages.length,ops===sessionHeads.length&&exportObj().pages.length===pages.length);
 return C;
}
function renderCheck(){
 const L=lint(),bad=L.filter(r=>r.count>0).length,ap=allPins(),ok=ap.filter(x=>x.v.ok).length;
 let h='<p class="big">'+fmtN(ok)+' <small>of '+fmtN(ap.length)+' pins verified by this page</small></p><p class="mono">'+bad+' lint check'+(bad===1?'':'s')+' need a look</p><p class="mn">How this is computed: each pin\'s quote is searched, after normalising quotes, dashes and spaces, in the passages of its document that start on its PDF page, and its label must name that passage.</p>';
 h+='<p><button class="btn pri" data-act="lint" id="lintBtn">'+(renderCheck.ran?'Re-run':'Lint now')+'</button> <span class="mn">Contradictions between pages are not checked by code: the schema\'s reading for contradictions is a person\'s job.</span></p>';
 h+='<table><caption><span class="mono" style="color:var(--red)">FIG.03</span> Lint: '+L.length+' checks</caption><thead><tr><th scope="col">Check</th><th scope="col" class="num">Count</th><th scope="col">Result</th><th scope="col">Pages concerned</th></tr></thead><tbody>'+L.map(r=>'<tr><td>'+esc(r.label)+'</td><td class="num">'+r.count+'</td><td class="'+(r.count?'check':'pass')+'">'+(r.count?r.count+' · check':'0 · pass')+'</td><td>'+slugLinks(r.slugs)+(r.extra?(r.slugs.length?'; ':'')+'no page: '+esc(r.extra):'')+'</td></tr>').join('')+'</tbody></table>';
 h+='<details open><summary>How the app checks itself</summary><ul>'+selfChecks().map(c=>'<li><strong>'+esc(c.name)+'.</strong> '+esc(c.text)+' · <span class="'+(c.ok==null?'na':c.ok?'pass':'check')+'">'+(c.ok==null?'not applicable yet':c.ok?'pass':'check')+'</span>'+(c.slugs.length?' · '+slugLinks(c.slugs):'')+'</li>').join('')+'</ul></details>';
 $('#chkOut').innerHTML=h;
}

/* ---------- tab 05 record ---------- */
function exportObj(){return{title:wiki.title,source:wiki.source,built:wiki.built,count:pages.length,schema:wiki.schema,pages:pages.map(p=>({slug:p.slug,type:p.type,title:p.title,frontmatter:p.frontmatter,body:p.body})),index:indexMd,log:logMd,tensions:tensMd,changes,library_status:Object.fromEntries(docs.map(d=>[d.id,d.status]))};}
function renderRecord(){
 const ent=parseLog(),list=$('#newest').checked?ent.slice().reverse():ent,tens=parseTens();
 let h='<h3 class="fig"><span class="mono">LOG</span> Operations, '+ent.length+' entries</h3>'+list.map(e=>'<details><summary>'+esc(e.head)+(sessionHeads.includes(e.head)?' <span class="chip">this session</span>':'')+'</summary><div class="md">'+renderMd(e.body,{})+'</div></details>').join('');
 h+='<h3 class="fig"><span class="mono">TENSIONS</span> Open disagreements, '+tens.length+' entries</h3>'+tens.map(e=>'<details id="tens-'+e.i+'"><summary>'+esc(e.head)+(sessionTens.includes(e.head)?' <span class="chip">this session</span>':'')+'</summary><div class="md">'+renderMd(e.body,{})+'</div>'+(e.card?'<p class="mn">card: '+(P_MAP.has(e.card)?'<a href="#'+esc(e.card)+'">'+esc(P_MAP.get(e.card).title)+'</a>':esc(e.card)+' (no page)')+'</p>':'')+'</details>').join('');
 h+='<h3>Method and source</h3><p class="mn">Counting, matching and verification are done by this page\'s code; each number has its "How this is computed" line. Data: '+esc(wiki.source||'research wiki')+', built '+esc(wiki.built||'unknown')+'.</p>';
 h+='<p><button class="btn pri" data-act="dljson">Download the wiki</button>'+(changes.length?'<button class="btn" data-act="dlmd">Download the changed pages (markdown)</button>':'')+'</p>';
 $('#recOut').innerHTML=h;
}

/* ---------- tab 03 ingest ---------- */
const chunk=(a,n)=>{const o=[];for(let i=0;i<a.length;i+=n)o.push(a.slice(i,i+n));return o;};
const paraLab=x=>x.paragraph?'para. '+x.paragraph:'p. '+x.page_label;
function newING(doc){
 const stub=pages.find(p=>p.frontmatter.status==='stub'&&(p.slug===slugify(doc.id)||p.slug===slugify(doc.symbol||'')))||pages.find(p=>p.frontmatter.status==='stub');
 return{doc,step:1,batches:chunk(doc.passages||[],25).map((ps,i)=>({i,passages:ps})),tk:[],failed:[],rows:[],dropped:0,returned:0,calls:0,sent:0,newSlugs:[],stub:stub?stub.slug:null,src:null,touched:[],drafts:{},changes:[],msg:'',err:null,filed:null,done1:false,run:null};
}
function nearest(q,page){
 const a=norm(q).split(' ');let best={run:0,passage:null};
 for(const x of ING.doc.passages.filter(x=>x.page===page)){
  const b=norm(x.text).split(' ');let run=0,prev=new Array(b.length+1).fill(0);
  for(let i=1;i<=a.length;i++){const c=new Array(b.length+1).fill(0);for(let j=1;j<=b.length;j++)if(a[i-1]===b[j-1]){c[j]=prev[j-1]+1;if(c[j]>run)run=c[j];}prev=c;}
  if(run>best.run)best={run,passage:x};
 }
 return best;
}
const vIng=p=>verify(p,{inbox:ING.doc.id});
const tkPrompt=(items,b,n)=>PRE+'DOCUMENT: '+ING.doc.title+' ('+citeAs(ING.doc)+', '+ING.doc.kind+', '+ING.doc.year+'). This is batch '+(b+1)+' of '+n+'. Return JSON {"takeaways": [{"claim": ..., "quote": ..., "passage": the passage id, "pages": [slug, ...]}]}, at most 10. Each quote is 8 to 40 words copied verbatim from that one passage. pages are slugs from the index that the claim bears on; propose a new lowercase-hyphenated slug only when no page fits (at most two in the whole ingest). Skip passages with nothing to take away.\n\nINDEX:\n'+indexMd+'\n\nPASSAGES (JSON):\n'+JSON.stringify(items);
async function ingStart(from){
 const run=startRun('ingest');ING.run=run;ING.step=2;ING.err=null;const n=ING.batches.length,tot=ING.doc.passages.length;
 for(let b=from||0;b<n;b++){
  if(run.stopped)break;const bt=ING.batches[b],items=bt.passages.map(x=>({id:x.id,page:x.page,paragraph:x.paragraph,text:x.text}));
  ING.msg='batch '+(b+1)+' of '+n+' · '+ING.sent+' of '+tot+' passages have left the browser; sending '+items.length+' more';renderIngest();
  ING.calls++;ING.sent+=items.length;
  const r=await callModel(tkPrompt(items,b,n),{label:'Ingest: batch '+(b+1),passages:items.length,run});
  if(r.stopped)break;
  if(!r.ok){ING.err={error:r.error,raw:r.raw,batch:b};ING.msg='';endRun('ingest');renderIngest();return;}
  const arr=Array.isArray(r.data.takeaways)?r.data.takeaways.slice(0,10):[];ING.returned+=arr.length;
  for(const t of arr){
   const pas=bt.passages.find(x=>x.id===String(t&&t.passage).trim());
   if(!pas){ING.dropped++;continue;}
   const quote=String(t.quote||'').trim(),pin=mkPin(ING.doc,pas,quote),v=vIng(pin);
   const pg=uniq((Array.isArray(t.pages)?t.pages:[]).map(String).filter(s=>/^[a-z0-9-]+$/.test(s))).filter(s=>{if(P_MAP.has(s)||ING.newSlugs.includes(s))return true;if(ING.newSlugs.length<2){ING.newSlugs.push(s);return true;}return false;});
   const row={claim:String(t.claim||'').trim(),quote,pas,pin,pages:pg,ok:v.ok,reason:v.reason};ING.rows.push(row);
   if(v.ok)ING.tk.push(row);else ING.failed.push(Object.assign({near:nearest(quote,pas.page)},row));
  }
  updHeader();renderIngest();
 }
 const stopped=run.stopped;endRun('ingest');ING.done1=true;
 ING.msg=(stopped?'Stopped; what has returned is kept. ':'')+ING.returned+' takeaways returned: '+ING.tk.length+' verified, '+ING.failed.length+' could not be verified'+(ING.dropped?', '+ING.dropped+' named a passage that was not sent (dropped)':'')+'.';
 renderIngest();
}
const srcPrompt=()=>PRE+'Write the source page for the document below. DOCUMENT: '+ING.doc.title+'; author '+(ING.doc.author||'unknown')+'; published '+ING.doc.published+'; '+ING.doc.pages+' pages; '+ING.doc.url+'. Cite as: '+citeAs(ING.doc)+'. Sections, in this order: Full cite, Register, One-liner, Key takeaways, How NOT to read this, Where it feeds the wiki, Related. Return JSON {"one_liner": ..., "body": markdown of at most 900 words, "touches": [{"slug": ..., "why": ...}]}. Use only the pins given below, copied exactly, one per claim.\n\nVERIFIED TAKEAWAYS (JSON):\n'+JSON.stringify(ING.tk.map(t=>({claim:t.claim,pin:t.pin.raw,passage:paraLab(t.pas)+', PDF page '+t.pas.page,pages:t.pages})))+'\n\nREGISTER of this document: ('+regOf(ING.doc.id)+')\nINDEX (existing slugs):\n'+indexMd;
function srcSlug(){const b=slugify(ING.doc.symbol||ING.doc.id);return!P_MAP.has(b)?b:!P_MAP.has(b+'-source')?b+'-source':b+'-'+Date.now().toString(36);}
async function ingDraftSource(){
 const run=startRun('ingest');ING.run=run;ING.err=null;ING.msg='Drafting the source page (1 call)…';ING.calls++;renderIngest();
 const r=await callModel(srcPrompt(),{label:'Ingest: source page',run});endRun('ingest');
 if(r.stopped){ING.msg='Stopped.';renderIngest();return;}
 const body=r.ok?String(r.data.body||'').trim():'';
 if(!r.ok||!body){ING.err={error:r.ok?'The draft had no body.':r.error,raw:r.raw,retry:'src'};ING.msg='';renderIngest();return;}
 ING.src={slug:srcSlug(),oneLiner:String(r.data.one_liner||'').trim(),body,touches:Array.isArray(r.data.touches)?r.data.touches:[]};
 const ok=s=>typeof s==='string'&&s!==ING.src.slug&&(P_MAP.has(s)||ING.newSlugs.includes(s)),out=new Map();
 ING.src.touches.forEach(t=>{const s=String((t&&t.slug)||t);if(ok(s)&&!out.has(s))out.set(s,String((t&&t.why)||''));});
 ING.tk.forEach(t=>t.pages.forEach(s=>{if(ok(s)&&!out.has(s))out.set(s,'takeaway');}));
 let list=[...out.entries()].filter(([s])=>s!==ING.stub).map(([slug,why])=>({slug,why}));
 if(ING.stub)list.unshift({slug:ING.stub,why:'stub: rewrite it with its checklist'});
 ING.touched=list.slice(0,12).map(t=>({slug:t.slug,why:t.why,isNew:!P_MAP.has(t.slug),isStub:t.slug===ING.stub}));
 ING.msg='Source page drafted. '+ING.touched.length+' pages would be touched.';renderIngest();
}
function pagePrompt(t){
 const rel=ING.tk.filter(x=>x.pages.includes(t.slug)),use=(t.isStub?ING.tk:(rel.length?rel:ING.tk.slice(0,5))).map(x=>({claim:x.claim,pin:x.pin.raw,passage:paraLab(x.pas)}));
 const head=PRE+'DOCUMENT: '+citeAs(ING.doc)+' ('+ING.doc.title+'). Why this page is touched: '+t.why+'.\n\nTAKEAWAYS WITH READY-MADE PINS (JSON):\n'+JSON.stringify(use)+'\n\n';
 if(t.isStub)return head+'The page below is a stub for this document. Rewrite it as a real entity page, working through the checklist in its body. Return JSON {"body": the complete new markdown body starting with "# title", at most 500 words}. Keep its existing pins if you keep their claims; add only the pins given above, copied exactly.\n\nPAGE '+t.slug+':\n'+P_MAP.get(t.slug).body;
 if(t.isNew)return head+'The page "'+t.slug+'" does not exist yet. Write it as a short concept page. Return JSON {"edits": [{"after": "end", "markdown": the complete page starting with "# title"}], "contested": null}, at most 300 words, only the pins given above, copied exactly.';
 return head+'Return JSON {"edits": [{"after": an existing heading of the page or "end", "markdown": ...}], "contested": null or a full contested block (claim:, verdict:, note:, then one line per position: sign, register letter, pin, gloss, [[slug]], separated by " | ") only where this document disagrees with the page}. At most 300 words in all; pins copied exactly from above.\n\nPAGE '+t.slug+':\n'+P_MAP.get(t.slug).body;
}
async function ingDraftPages(){
 const run=startRun('ingest');ING.run=run;ING.err=null;
 for(let i=0;i<ING.touched.length;i++){
  const t=ING.touched[i];if(ING.drafts[t.slug])continue;if(run.stopped)break;
  ING.msg='page '+(i+1)+' of '+ING.touched.length+': '+t.slug;ING.calls++;renderIngest();
  const r=await callModel(pagePrompt(t),{label:'Ingest: '+t.slug,run});
  if(r.stopped)break;
  if(!r.ok){ING.err={error:r.error,raw:r.raw,retry:'pages'};ING.msg='';endRun('ingest');renderIngest();return;}
  const d=r.data,old=P_MAP.get(t.slug),notes=[];let body,kind=t.isNew?'new':'edited',title=old?old.title:t.slug,type=old?old.type:'concept';
  if(t.isStub){body=String(d.body||'').trim();if(body)body=INS+'\n'+body+'\n'+INE;}
  else{
   const ed=Array.isArray(d.edits)?d.edits:[];body=old?old.body:'';let n=0;
   for(const e of ed){const md=String((e&&e.markdown)||'').trim();if(!md)continue;if(t.isNew){body=INS+'\n'+md+'\n'+INE;n++;continue;}const x=insertAt(body,e.after,md);body=x.body;if(x.note)notes.push(x.note);n++;}
   if(typeof d.contested==='string'&&/claim:/.test(d.contested)){let blk=d.contested.trim();if(!/^\x60\x60\x60/.test(blk))blk=FENCE+'contested\n'+blk+'\n'+FENCE;if(t.isNew)body=body.replace(INE,'\n'+blk+'\n'+INE);else{body=insertAt(body,'end',blk).body;}n++;}
   if(!n)body='';
  }
  if(!body){ING.drafts[t.slug]={none:true};continue;}
  if(t.isNew){const h=insPart(body).match(/^#\s+(.*)$/m);title=h?h[1].trim():t.slug;}
  ING.drafts[t.slug]={slug:t.slug,kind,title,type,body,notes,isStub:t.isStub,decision:null};
 }
 const stopped=run.stopped;endRun('ingest');ING.msg=stopped?'Stopped; the drafts that returned are kept.':'All page drafts returned.';renderIngest();
}
function mkChanges(){
 const out=[],s=ING.src,doc=ING.doc,reg=(ING.stub&&P_MAP.get(ING.stub).frontmatter.register)||[];
 const sb=/^#\s/.test(s.body)?s.body:'# '+citeAs(doc)+' — '+(doc.short_title||doc.title)+'\n\n'+s.body;
 out.push({slug:s.slug,kind:'new',title:(sb.match(/^#\s+(.*)$/m)||[0,s.slug])[1],type:'source',body:INS+'\n'+sb+'\n'+INE,notes:[],decision:null,fm:{type:'source',tags:uniq(['source',...ING.touched.map(t=>t.slug)]),register:reg.slice(),status:'draft',links:[],sources:[doc.id]}});
 ING.touched.forEach(t=>{const d=ING.drafts[t.slug];if(d&&!d.none)out.push(d);});
 return out;
}
function cardStats(c){
 const ip=insPart(c.body),pins=parsePins(ip),ok=pins.filter(p=>vIng(p).ok).length;
 return{paras:ip.split(/\n\s*\n/).filter(x=>x.trim()).length,ok,bad:pins.length-ok};
}
function ingFile(){
 const date=today(),doc=ING.doc,bc=lint().filter(r=>r.count>0).length,ap=ING.changes.filter(c=>c.decision==='approved'),rj=ING.changes.filter(c=>c.decision==='rejected');
 const apSet=new Set(ap.map(c=>c.slug)),srcOk=apSet.has(ING.src.slug),head='['+date+'] ingest | '+(doc.symbol||doc.short_title)+': '+doc.short_title;
 const dreg=regOf(doc.id).split('').filter(x=>'abcdef'.includes(x)),newTens=[];
 for(const c of ap){
  const body=stripIns(c.body).trim()+'\n',ids=uniq(parsePins(body).map(p=>p.id)),p=P_MAP.get(c.slug),old=p?p.frontmatter:c.fm;
  const fm=Object.assign({},old,{title:c.title,type:c.type,updated:date,register:uniq([...(old.register||[]),...(c.slug===ING.src.slug?[]:dreg)]),sources:uniq([...(old.sources||[]).filter(s=>ids.includes(s)),...ids])});
  if(c.isStub||c.kind==='new')fm.status='draft';
  const bl=uniq([...body.matchAll(/\[\[([^\]|#]+)/g)].map(m=>m[1].trim()));
  let links=uniq([...(old.links||[]),...bl.filter(s=>P_MAP.has(s)||apSet.has(s))]);
  if(c.slug===ING.src.slug)links=uniq([...bl.filter(s=>P_MAP.has(s)||apSet.has(s)),...ap.filter(x=>x.slug!==c.slug).map(x=>x.slug)]);else if(srcOk)links=uniq([...links,ING.src.slug]);
  fm.links=links.filter(s=>s!==c.slug);
  const oldBody=p?p.body:'';
  for(const m of body.matchAll(new RegExp(FENCE+'contested\\n([\\s\\S]*?)'+FENCE,'g'))){const k=parseContested(m[1]);if(!k.claim||oldBody.includes(k.claim))continue;
   const sm={contested:'open'},stt=/^leans/.test(k.verdict)?'leaning':/^settled/.test(k.verdict)?'settled':(sm[k.verdict]||'open');
   const ps=s=>k.pos.filter(x=>x.sign===s).map(x=>'('+x.reg+') '+((x.pin.match(/\[([^\]]+)\]/)||[0,''])[1])).join('; ')||'none';
   newTens.push('### '+(slugify(k.claim).slice(0,60)||'claim')+'\n- title: '+k.claim+'\n- status: '+stt+'\n- card: [['+c.slug+']]\n- poles: supports '+ps('+')+' · contests '+ps('-')+'\n- where: '+uniq(k.pos.map(x=>(x.pin.match(/\[([^\]]+)\]/)||[0,''])[1])).join('; '));}
  if(p){p.body=body;p.frontmatter=fm;}else pages.push({slug:c.slug,type:c.type,title:c.title,frontmatter:fm,body});
 }
 doc.status='ingested';reindex();
 for(const c of ap){
  const p=P_MAP.get(c.slug),n=p._pins.filter(x=>x.v.ok).length;
  if(c.kind==='new'||c.isStub){idxUpsert(c.slug,p.type,'- [[' + c.slug + ']] — ' + (c.slug===ING.src.slug&&ING.src.oneLiner?plainFirst(ING.src.oneLiner):plainFirst(p.body)) + ' · (' + p.frontmatter.register.join('') + ') · ✓' + n);}
  else{const L=indexMd.split('\n'),k=L.findIndex(l=>/^\s*[-*]\s/.test(l)&&l.includes('[['+c.slug+']]'));if(k>=0){L[k]=L[k].replace(/✓\s*\d+/,'✓'+n);indexMd=L.join('\n');}else idxUpsert(c.slug,p.type,'- [[' + c.slug + ']] — ' + plainFirst(p.body) + ' · (' + p.frontmatter.register.join('') + ') · ✓' + n);}
 }
 idxCounts();
 const pinned=pages.filter(p=>p.slug!==ING.src.slug&&p._pins.some(x=>x.id===doc.id)).map(p=>p.slug),tp=pages.reduce((n,p)=>n+p._pins.filter(x=>x.id===doc.id).length,0);
 appendLog(head,'Read '+ING.sent+' passages ('+citeAs(doc)+', register ('+regOf(doc.id)+')). Wrote [['+ING.src.slug+']]'+(srcOk?'':' (rejected)')+'. '+tp+' pins in all; besides its own page, pinned on '+pinned.length+' pages: '+(pinned.map(s=>'[['+s+']]').join(', ')||'none')+'. Rejected: '+(rj.map(c=>'[['+c.slug+']]').join(', ')||'none')+'.');
 if(newTens.length){tensMd=tensMd.replace(/\s*$/,'')+'\n\n'+newTens.join('\n\n')+'\n';newTens.forEach(t=>sessionTens.push(t.split('\n')[0].slice(4).trim()));}
 ap.forEach(c=>changes.push({date,kind:'ingest',slug:c.slug,change:c.kind,op:head}));
 ING.filed={date,slugs:ap.map(c=>c.slug),approved:ap.length,rejected:rj.length,before:bc,after:lint().filter(r=>r.count>0).length};
 refreshAll();say('Filed '+ap.length+' approved page'+(ap.length===1?'':'s')+'.');
}
const stepsHTML=()=>'<ol class="steps">'+['Scope','Takeaways','Drafts','Review and file'].map((n,i)=>'<li class="'+(ING.step===i+1?'on':'')+'"'+(ING.step===i+1?' aria-current="step"':'')+'>0'+(i+1)+' '+n+'</li>').join('')+'</ol>';
const runLine=()=>'<p class="runline" aria-live="polite">calls so far <b>'+ING.calls+'</b> · passages sent <b>'+ING.sent+'</b></p>'+(ING.msg?'<p class="mn" aria-live="polite">'+esc(ING.msg)+'</p>':'');
const stopBtn=()=>RUN.ingest?'<button class="btn" data-act="stop">Stop</button>':'';
function renderIngest(){
 const out=$('#ingOut'),inbox=docs.filter(d=>d.status==='inbox'),btns=inbox.map(d=>'<button class="btn pri" data-act="ingstart" data-arg="'+esc(d.id)+'">Ingest '+esc(d.symbol||d.short_title)+'</button>').join(' ');
 const intro='<p class="mn">Ingesting sends the document\'s passages to a language model in batches. Every change waits for your approval; nothing is written before.</p>';
 if(ING&&ING.filed){const f=ING.filed;out.innerHTML='<h2>Filed</h2><p class="big">'+f.approved+' <small>page'+(f.approved===1?'':'s')+' written, '+f.rejected+' rejected</small></p><p class="mn" aria-live="polite">Lint checks needing a look: '+f.before+' before, '+f.after+' after. The log, the index and the tensions register were updated; the pages are in memory until you download them on tab 05.</p>'+(inbox.length?intro+btns:'<p class="lead">Nothing waits in the inbox.</p>');return;}
 if(!ING){out.innerHTML=inbox.length?intro+'<p>'+btns+'</p>':'<p class="lead">Nothing waits in the inbox.</p>';return;}
 let h='<h2>Ingest '+esc(ING.doc.symbol||ING.doc.short_title)+'</h2>'+stepsHTML()+runLine();
 if(ING.err)h+=errHTML(ING.err,ING.err.batch!=null?'ingretry':ING.err.retry==='src'?'ingsrc':'ingpages');
 const tot=ING.doc.passages.length,n=ING.batches.length;
 if(ING.step===1){
  const chars=ING.doc.passages.reduce((a,x)=>a+x.text.length,0);
  h+='<p><strong>Scope: the whole document.</strong></p><p>All '+tot+' passages will be sent, in batches of 25 ('+n+' call'+(n===1?'':'s')+'), '+fmtN(chars)+' characters; nothing is held back. They leave the browser.</p>';
  h+='<table><caption>Batches</caption><thead><tr><th scope="col">Batch</th><th scope="col" class="num">Passages</th><th scope="col">Paragraphs</th><th scope="col">PDF pages</th></tr></thead><tbody>'+ING.batches.map(b=>{const pr=b.passages.map(x=>x.paragraph).filter(Boolean),pg=b.passages.map(x=>x.page);return'<tr><td>'+(b.i+1)+'</td><td class="num">'+b.passages.length+'</td><td>'+(pr.length?esc(pr[0]===pr[pr.length-1]?pr[0]:pr[0]+' to '+pr[pr.length-1]):'no paragraph numbers')+'</td><td>'+Math.min(...pg)+'–'+Math.max(...pg)+'</td></tr>';}).join('')+'</tbody></table><p><button class="btn pri" data-act="ingbegin">Start</button></p>';
 }else if(ING.step===2){
  h+=stopBtn();
  h+='<table><caption><span class="mono" style="color:var(--red)">FIG.02</span> Takeaways so far: '+ING.rows.length+' returned</caption><thead><tr><th scope="col">Claim</th><th scope="col">Quote</th><th scope="col">Passage</th><th scope="col">Pages it would touch</th><th scope="col">Check</th></tr></thead><tbody>'+(ING.rows.map(r=>'<tr><td data-source="ai">'+esc(r.claim)+'</td><td data-source="ai">“'+esc(r.quote)+'”</td><td>'+esc(paraLab(r.pas))+' · PDF p. '+r.pas.page+'</td><td data-source="ai">'+(r.pages.map(s=>'<span class="chip">'+esc(s)+'</span>').join('')||'<span class="mn">none</span>')+'</td><td class="'+(r.ok?'pass':'check')+'">'+(r.ok?'verified':'could not verify')+'</td></tr>').join('')||'<tr><td colspan="5" class="mn">Nothing has returned yet.</td></tr>')+'</tbody></table>';
  h+='<details class="fail" open><summary>Could not verify: '+ING.failed.length+'</summary><p class="mn">These claims are in no change card and in no later prompt.</p>'+ING.failed.map(f=>'<div><p data-source="ai">“'+esc(f.quote)+'” (claim: '+esc(f.claim)+')</p><p class="mn">named passage '+esc(f.pas.id)+' ('+esc(paraLab(f.pas))+', PDF p. '+f.pas.page+'); reason: '+esc(f.reason)+'. Nearest passage on that page: '+(f.near.passage?esc(paraLab(f.near.passage))+', longest shared run '+f.near.run+' words':'none')+'.</p><button class="btn sm openpdf" data-id="'+esc(ING.doc.id)+'" data-page="'+f.pas.page+'" aria-label="Open '+esc(ING.doc.symbol||ING.doc.short_title)+' at PDF page '+f.pas.page+'">Open the PDF page</button></div>').join('')+'</details>';
  if(ING.done1&&!RUN.ingest)h+=ING.tk.length?'<p><button class="btn pri" data-act="ingto3">Continue to the drafts</button></p>':'<p class="check">No takeaway verified, so there is nothing to draft.</p>';
 }else if(ING.step===3){
  h+=stopBtn();
  if(!ING.src)h+='<p>'+ING.tk.length+' verified takeaways will be sent to draft the source page.</p><p><button class="btn pri" data-act="ingsrc"'+(RUN.ingest?' disabled':'')+'>Draft the source page (1 call)</button></p>';
  else{
   const sc=ING.touched.length,left=ING.touched.filter(t=>!ING.drafts[t.slug]).length;
   h+='<details><summary>Source page draft (one-liner: '+esc(ING.src.oneLiner||'none')+')</summary><div class="md" data-source="ai">'+renderMd(ING.src.body,{pinCheck:vIng})+'</div></details>';
   h+='<p>Pages that would be touched: '+ING.touched.map(t=>'<span class="chip">'+esc(t.slug)+(t.isNew?' (new)':t.isStub?' (stub)':'')+'</span>').join('')+'</p>';
   h+=left?'<p><button class="btn pri" data-act="ingpages"'+(RUN.ingest?' disabled':'')+'>Draft the changes to '+sc+' pages ('+left+' call'+(left===1?'':'s')+')</button></p>':'<p><button class="btn pri" data-act="ingto4">Review the changes</button></p>';
  }
 }else{
  const cs=ING.changes,k=cs.findIndex(c=>!c.decision);
  if(k>=0){
   const c=cs[k],st=cardStats(c);
   h+='<fieldset><legend>Change '+(k+1)+' of '+cs.length+' · '+esc(c.title)+' ('+esc(c.type)+') · '+(c.kind==='new'?'new page':'edited')+'</legend><p class="mn">inserted paragraphs: '+st.paras+' · pins added: '+st.ok+' verified, '+st.bad+' not verified'+(c.notes&&c.notes.length?' · note: '+esc(c.notes.join('; ')):'')+'</p><div class="md" data-source="ai">'+renderMd(c.body,{mark:true,slug:c.slug,pinCheck:vIng})+'</div><p><button class="btn pri" data-act="approve"'+(st.bad?' disabled':'')+' aria-label="Approve change '+(k+1)+' of '+cs.length+': '+esc(c.slug)+'">Approve this page</button><button class="btn" data-act="reject" aria-label="Reject change '+(k+1)+' of '+cs.length+': '+esc(c.slug)+'">Reject this page</button>'+(st.bad?' <span class="mn">Approve is disabled: '+st.bad+' inserted pin'+(st.bad===1?'':'s')+' do not verify. Reject this page.</span>':'')+'</p></fieldset>';
  }else h+='<p class="runline">All '+cs.length+' changes decided: approved <b>'+cs.filter(c=>c.decision==='approved').length+'</b> · rejected <b>'+cs.filter(c=>c.decision==='rejected').length+'</b></p><p class="mn">Nothing in the wiki has changed yet.</p><p><button class="btn pri" data-act="ingfile">File the approved changes</button></p>';
  h+='<p class="mn">Decided so far: '+cs.map(c=>esc(c.slug)+' '+(c.decision||'waiting')).join(' · ')+'</p>';
 }
 out.innerHTML=h;
}

/* ---------- tab 06 map ---------- */
const MCOL={source:'#2a6f97',concept:'#996600',entity:'#2f7a4a',question:'#7a4a9a'},MCO='#6b665c',MW=1000,MH=640,MANC={source:[.2,.3],concept:[.72,.26],entity:[.4,.74],question:[.86,.74]};
const mapSel={slug:null};let MG=null;
const mcol=t=>MCOL[t]||MCO,mr1=v=>Math.round(v*10)/10;
function mapGraph(){
 const order=['source','concept','entity','question'],rank=t=>{const i=order.indexOf(t);return i<0?order.length:i;};
 const nodes=pages.slice().sort((a,b)=>rank(a.type)-rank(b.type)||(a.slug<b.slug?-1:a.slug>b.slug?1:0)).map(p=>({slug:p.slug,title:p.title,type:p.type,in:0,out:0,x:0,y:0,r:0}));
 const ix=new Map(nodes.map((n,i)=>[n.slug,i])),links=[];let loose=0;
 pages.forEach(p=>p._links.forEach(s=>{
  if(s===p.slug)return;
  if(!ix.has(s)){loose++;return;}
  const a=ix.get(p.slug),b=ix.get(s);links.push([a,b]);nodes[a].out++;nodes[b].in++;
 }));
 nodes.forEach(n=>{n.r=Math.min(5+3*Math.sqrt(n.in),24);});
 return{nodes,links,loose,ix};
}
/* Fruchterman-Reingold with a fixed start (each type on a ring round its own anchor) and a fixed number of steps: no random numbers, so the same data always gives the same map. */
function mapLayout(nodes,links){
 const n=nodes.length,anc=nd=>{const a=MANC[nd.type]||[.5,.5];return[a[0]*MW,a[1]*MH];},cnt={},idx={};
 nodes.forEach(nd=>{cnt[nd.type]=(cnt[nd.type]||0)+1;});
 nodes.forEach(nd=>{const a0=anc(nd),i=idx[nd.type]=(idx[nd.type]||0)+1,m=cnt[nd.type],rad=Math.min(40+m*6,150),ang=2*Math.PI*(i-1)/m;nd.x=a0[0]+rad*Math.cos(ang);nd.y=a0[1]+rad*Math.sin(ang);});
 const seen=new Set(),pairs=[];
 links.forEach(([a,b])=>{const k=a<b?a+'_'+b:b+'_'+a;if(!seen.has(k)){seen.add(k);pairs.push([a,b]);}});
 const k=Math.sqrt(MW*MH/Math.max(n,1))*.75,ITER=320,clamp=nd=>{nd.x=Math.max(40,Math.min(MW-40,nd.x));nd.y=Math.max(40,Math.min(MH-40,nd.y));};
 for(let it=0;it<ITER;it++){
  const t=(MW/12)*(1-it/ITER)+1,dx=new Array(n).fill(0),dy=new Array(n).fill(0);
  for(let i=0;i<n;i++)for(let j=i+1;j<n;j++){
   let vx=nodes[i].x-nodes[j].x,vy=nodes[i].y-nodes[j].y,d=Math.hypot(vx,vy);
   if(d<.01){vx=(i-j)*.01;vy=.01;d=Math.hypot(vx,vy);}
   const f=k*k/d;dx[i]+=vx/d*f;dy[i]+=vy/d*f;dx[j]-=vx/d*f;dy[j]-=vy/d*f;
  }
  for(const [a,b] of pairs){
   const vx=nodes[a].x-nodes[b].x,vy=nodes[a].y-nodes[b].y,d=Math.hypot(vx,vy)||.01,f=d*d/k;
   dx[a]-=vx/d*f;dy[a]-=vy/d*f;dx[b]+=vx/d*f;dy[b]+=vy/d*f;
  }
  for(let i=0;i<n;i++){
   const a0=anc(nodes[i]);dx[i]+=(a0[0]-nodes[i].x)*.5;dy[i]+=(a0[1]-nodes[i].y)*.5;
   const d=Math.hypot(dx[i],dy[i])||.01,m=Math.min(d,t);nodes[i].x+=dx[i]/d*m;nodes[i].y+=dy[i]/d*m;clamp(nodes[i]);
  }
 }
 for(let it=0;it<60;it++){
  let moved=false;
  for(let i=0;i<n;i++)for(let j=i+1;j<n;j++){
   let vx=nodes[j].x-nodes[i].x,vy=nodes[j].y-nodes[i].y,d=Math.hypot(vx,vy);const min=nodes[i].r+nodes[j].r+7;
   if(d>=min)continue;if(d<.01){vx=1;vy=0;d=1;}
   const m=(min-d)/2;nodes[i].x-=vx/d*m;nodes[i].y-=vy/d*m;nodes[j].x+=vx/d*m;nodes[j].y+=vy/d*m;moved=true;
  }
  if(!moved)break;
 }
 nodes.forEach(nd=>{clamp(nd);nd.x=mr1(nd.x);nd.y=mr1(nd.y);});
}
function mapEdge(a,b){
 const mx=(a.x+b.x)/2,my=(a.y+b.y)/2,vx=b.x-a.x,vy=b.y-a.y,d=Math.hypot(vx,vy)||1,o=Math.min(d*.12,26);
 return'M'+mr1(a.x)+' '+mr1(a.y)+' Q'+mr1(mx-vy/d*o)+' '+mr1(my+vx/d*o)+' '+mr1(b.x)+' '+mr1(b.y);
}
function renderMap(){
 MG=mapGraph();const nodes=MG.nodes,links=MG.links;mapLayout(nodes,links);
 if(mapSel.slug&&!P_MAP.has(mapSel.slug))mapSel.slug=null;
 const top=new Set(nodes.map((n,i)=>i).filter(i=>nodes[i].in>0).sort((a,b)=>nodes[b].in-nodes[a].in||a-b).slice(0,8));
 let h='';
 links.forEach(([a,b])=>{h+='<path class="ed" data-a="'+a+'" data-b="'+b+'" d="'+mapEdge(nodes[a],nodes[b])+'"/>';});
 nodes.forEach((n,i)=>{
  const t=n.title.length>30?n.title.slice(0,29)+'…':n.title,lx=Math.max(70,Math.min(MW-70,n.x)),ly=n.y+n.r+13>MH-4?n.y-n.r-6:n.y+n.r+13;
  h+='<g class="nd'+(top.has(i)?' top':'')+'" data-i="'+i+'" role="button" aria-pressed="false" tabindex="'+(i===0?0:-1)+'" aria-label="'+esc(n.title)+', '+esc(n.type||'page')+', '+n.in+' links in, '+n.out+' links out"><circle cx="'+n.x+'" cy="'+n.y+'" r="'+mr1(n.r)+'" fill="'+mcol(n.type)+'"/><text class="lb" x="'+mr1(lx)+'" y="'+mr1(ly)+'" text-anchor="middle">'+esc(t)+'</text></g>';
 });
 $('#mapsvg').innerHTML=h;
 const types=uniq(nodes.map(n=>n.type));
 $('#maplg').innerHTML='Colour = type: '+types.map(t=>'<span class="lg"><i style="background:'+mcol(t)+'"></i>'+esc(t||'other')+' ('+nodes.filter(n=>n.type===t).length+')</span>').join('')+' · size = number of pages that link to the page';
 const orph=nodes.filter(n=>n.in===0);
 $('#mapsum').innerHTML=nodes.length+' pages · '+links.length+' links · pages no other page links to (orphans): '+(orph.length?orph.map(n=>'<button class="link" data-act="mapsel" data-arg="'+esc(n.slug)+'">'+esc(n.title)+'</button>').join(', '):'none')+(MG.loose?' · '+MG.loose+' link'+(MG.loose===1?'':'s')+' to a slug with no page, not drawn':'');
 mapApply();
}
function mapApply(){
 if(!MG)return;
 const svg=$('#mapsvg'),s=mapSel.slug,si=s?MG.ix.get(s):-1,nb=new Set();
 if(si>=0)MG.links.forEach(([a,b])=>{if(a===si)nb.add(b);if(b===si)nb.add(a);});
 svg.classList.toggle('sel',si>=0);
 svg.querySelectorAll('.ed').forEach(e=>{const a=+e.dataset.a,b=+e.dataset.b;e.classList.toggle('out',si>=0&&a===si);e.classList.toggle('in',si>=0&&b===si);});
 svg.querySelectorAll('.nd').forEach(g=>{const i=+g.dataset.i;g.classList.toggle('cur',i===si);g.classList.toggle('nb',nb.has(i));g.classList.toggle('show',i===si||nb.has(i));g.setAttribute('aria-pressed',String(i===si));});
 const n=si>=0?MG.nodes[si]:null,nl=[...nb].map(i=>MG.nodes[i].title);
 $('#mapinfo').innerHTML=n?'<p class="mapname">'+esc(n.title)+'</p><p class="mn">'+esc(n.type||'page')+' · '+n.in+' link'+(n.in===1?'':'s')+' in · '+n.out+' link'+(n.out===1?'':'s')+' out · '+nb.size+' neighbouring page'+(nb.size===1?'':'s')+(nl.length?': '+nl.slice(0,12).map(esc).join('; ')+(nl.length>12?' and '+(nl.length-12)+' more':''):'')+'</p><p class="mn">Red lines: links out of this page · dark lines: links into it</p><p><button class="btn pri" data-act="mapopen" aria-label="Open this page: '+esc(n.title)+'">Open this page</button><button class="btn" data-act="mapclear">Clear</button></p>':'<p class="mn">Hover or focus a page to see its title and its links in and out. Click it to highlight the pages it links to and the pages that link to it.</p>';
}
function mapSelect(s){if(!P_MAP.has(s))return;mapSel.slug=s;mapApply();}
function mapTip(g){
 const tip=$('#maptip');
 if(!g||!MG){tip.hidden=true;return;}
 const n=MG.nodes[+g.dataset.i],k=$('#mapsvg').getBoundingClientRect().width/MW,w=$('#mapsvg').getBoundingClientRect().width;
 tip.innerHTML='<strong>'+esc(n.title)+'</strong><br>'+esc(n.type||'page')+' · '+n.in+' link'+(n.in===1?'':'s')+' in · '+n.out+' link'+(n.out===1?'':'s')+' out';
 const below=(n.y-n.r)*k<70;
 tip.style.left=Math.max(100,Math.min(w-100,n.x*k))+'px';tip.style.top=(below?(n.y+n.r)*k+8:(n.y-n.r)*k-8)+'px';tip.style.transform=below?'translate(-50%,0)':'translate(-50%,-100%)';tip.hidden=false;
}
function bindMap(){
 const svg=$('#mapsvg'),nodeOf=e=>(e.target.closest?e.target.closest('.nd'):null);
 svg.addEventListener('click',e=>{const g=nodeOf(e);if(g)mapSelect(MG.nodes[+g.dataset.i].slug);else ACT.mapclear(true);});
 svg.addEventListener('keydown',e=>{
  const g=nodeOf(e);if(!g)return;
  if(e.key==='Enter'||e.key===' '){e.preventDefault();mapSelect(MG.nodes[+g.dataset.i].slug);return;}
  const d={ArrowRight:1,ArrowDown:1,ArrowLeft:-1,ArrowUp:-1}[e.key];
  if(d){e.preventDefault();const gs=[...svg.querySelectorAll('.nd')];gs[(gs.indexOf(g)+d+gs.length)%gs.length].focus();}
 });
 svg.addEventListener('mouseover',e=>mapTip(nodeOf(e)));
 svg.addEventListener('mouseout',e=>{const g=nodeOf(e);if(g&&!g.contains(e.relatedTarget))mapTip(null);});
 svg.addEventListener('focusin',e=>{const g=nodeOf(e);if(!g)return;svg.querySelectorAll('.nd').forEach(x=>x.setAttribute('tabindex','-1'));g.setAttribute('tabindex','0');mapTip(g);});
 svg.addEventListener('focusout',()=>mapTip(null));
}

/* ---------- actions and events ---------- */
function refreshAll(){reindex();updHeader();renderList();renderView();renderAskTop();renderAskOut();renderIngest();renderCheck();renderRecord();renderMap();}
const ACT={
 askgo(){ask.stage==='pick'?askStep2():askStep1();},
 askretry(){ask.err&&ask.err.retry===2?askStep2():askStep1();},
 stop(){['ask','ingest'].forEach(k=>{if(RUN[k])RUN[k].halt();});say('Stopped. What has returned is kept.');},
 pickopen(){ask.pickOpen=!ask.pickOpen;renderAskOut();},
 filecard(){ask.filing=!ask.filing;renderAskOut();updFile();},
 filedo:fileQuestion,
 async copyans(){say(await copyText(ask.answer.answer)?'Answer copied.':'Copy failed.');},
 async copymd(s){const p=P_MAP.get(s);if(p)say(await copyText(pageMd(p))?'Page copied as markdown.':'Copy failed.');},
 gotens(i){selectTab(4);const d=$('#tens-'+i);if(d){d.open=true;d.scrollIntoView();$('summary',d).focus();}},
 lint(){renderCheck.ran=true;renderCheck();},
 dljson(){download('wiki-'+today()+'.json',JSON.stringify(exportObj(),null,1),'application/json');},
 dlmd(){const sl=uniq(changes.map(c=>c.slug)).filter(s=>P_MAP.has(s));download('wiki-changed-pages-'+today()+'.md',sl.map(s=>pageMd(P_MAP.get(s))).join('\n\n---\n\n'),'text/markdown');},
 ingstart(id){ING=newING(docMap.get(id));renderIngest();},
 ingbegin(){ingStart(0);},
 ingretry(){ingStart(ING.err.batch);},
 ingto3(){ING.step=3;ING.msg='';renderIngest();},
 ingsrc:ingDraftSource,
 ingpages:ingDraftPages,
 ingto4(){ING.changes=mkChanges();ING.step=4;ING.msg='';renderIngest();},
 approve(){const c=ING.changes.find(x=>!x.decision);if(c)c.decision='approved';renderIngest();},
 reject(){const c=ING.changes.find(x=>!x.decision);if(c)c.decision='rejected';renderIngest();},
 ingfile:ingFile,
 mapsel(s){mapSelect(s);$('#mapinfo').scrollIntoView({block:'nearest'});},
 mapopen(){const s=mapSel.slug;if(!s)return;const h=location.hash.slice(1);if(h===s||h===encodeURIComponent(s))route();else location.hash=s;},
 mapclear(bg){const old=mapSel.slug;mapSel.slug=null;mapApply();if(old&&!bg&&MG){const g=document.querySelector('#mapsvg .nd[data-i="'+MG.ix.get(old)+'"]');if(g)g.focus();}}
};
document.addEventListener('click',e=>{
 const t=e.target.closest('button');if(!t)return;
 if(t.classList.contains('pinlab')||t.classList.contains('openpdf')){openSrc(t.dataset.id,+t.dataset.page);return;}
 if(t.classList.contains('pinx')){const b=t.parentElement.querySelector('.pinbody'),o=b.hidden;b.hidden=!o;t.setAttribute('aria-expanded',o);t.textContent=o?'▴':'▾';return;}
 const a=t.dataset.act;if(a&&ACT[a])ACT[a](t.dataset.arg,t);
});
document.addEventListener('input',e=>{
 if(e.target.id==='flt')renderList();
 else if(e.target.id==='q')renderAskTop();
 else if(e.target.id==='fT'){ask.fTitle=e.target.value;updFile();}
 else if(e.target.id==='fG'){ask.fTags=e.target.value;updFile();}
});
document.addEventListener('change',e=>{
 if(e.target.id==='newest')renderRecord();
 else if(e.target.name==='pick'){
  const on=[...document.querySelectorAll('input[name=pick]:checked')].map(x=>x.value);
  if(on.length>5){e.target.checked=false;say('At most 5 pages.');return;}
  ask.chosen=pages.map(p=>p.slug).filter(s=>on.includes(s));renderAskTop();
 }
});
document.addEventListener('keydown',e=>{
 if(e.key==='Escape'&&(RUN.ask||RUN.ingest))ACT.stop();
 if(e.key==='Escape'&&mapSel.slug&&!$('#p5').hidden)ACT.mapclear();
 if(e.target.id==='q'&&e.key==='Enter'&&!e.shiftKey){e.preventDefault();if(!RUN.ask)askStep1();}
});
window.addEventListener('hashchange',route);

/* ---------- start ---------- */
reindex();warn0=allPins().filter(x=>x.mark==='⚠').length;
buildTabs();updHeader();renderAskTop();renderAskOut();renderIngest();renderCheck();renderRecord();bindMap();renderMap();route();
$('#t0').focus();
})();
</script>
</body>
</html>
```
