I built the research wiki workspace in five tabs: Pages, Ask, Ingest, Check and Record. Every quotation is re-checked by the page's own code against the library passages. Nothing goes to the model until you press Ask or Ingest, and nothing enters the wiki until a person approves it.

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Research wiki: neurotechnology in the administration of justice</title>
<style>
:root{--bg:#f4f0e8;--ink:#1d1b18;--mute:#5c574d;--rule:#d9d2c3;--red:#9b2335;--grn:#1f6b3a;--amb:#8a5a00;--ins:#fbf0b8;--serif:Georgia,"Times New Roman",serif;--mono:ui-monospace,Menlo,Consolas,monospace}
*{box-sizing:border-box}
html{background:var(--bg)}
body{margin:0;color:var(--ink);background:var(--bg);font:16px/1.55 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif}
a{color:var(--red)}
:focus-visible{outline:3px solid var(--red);outline-offset:2px}
button,input,textarea{font:inherit;color:inherit}
.lab,.mono{font:11.5px/1.4 var(--mono);letter-spacing:.08em;text-transform:uppercase}
.hint{font:12px/1.45 var(--mono);color:var(--mute)}
.top{display:flex;gap:24px;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;padding:20px 28px 14px;border-bottom:1px solid var(--rule)}
h1{font:400 30px/1.15 var(--serif);margin:4px 0 6px}
.strip{text-align:right;font:11.5px/1.5 var(--mono);color:var(--mute);max-width:430px}
[role=tablist]{display:flex;flex-wrap:wrap;gap:0 4px;padding:0 28px;border-bottom:1px solid var(--rule)}
.tab{background:none;border:0;border-bottom:3px solid transparent;padding:12px 14px 9px;font:12px var(--mono);letter-spacing:.08em;text-transform:uppercase;cursor:pointer}
.tab.on{color:var(--red);border-bottom-color:var(--red)}
main{padding:20px 28px 36px;max-width:1280px}
[role=tabpanel][hidden]{display:none}
h2.q{font:400 24px/1.25 var(--serif);margin:0 0 14px}
h2.ptitle{font:400 30px/1.2 var(--serif);margin:4px 0 8px}
.body h2{font:400 26px/1.2 var(--serif);margin:22px 0 8px}
.body h3,h3.s{font:400 21px/1.25 var(--serif);margin:22px 0 6px;border-top:1px solid var(--rule);padding-top:12px}
.body h4,.body h5{font:italic 400 18px/1.3 var(--serif);margin:16px 0 4px}
.cols{display:grid;grid-template-columns:320px minmax(0,1fr);gap:32px}
.cols>aside{position:sticky;top:8px;align-self:start;max-height:calc(100vh - 16px);overflow:auto;padding-right:8px}
.cols>div{max-width:900px}
@media(max-width:900px){.cols{grid-template-columns:1fr}.cols>aside{position:static;max-height:none}.top,main{padding-left:14px;padding-right:14px}[role=tablist]{padding:0 6px}.strip{text-align:left}}
.big{font:400 48px/1 var(--serif)}
.grp{font:11.5px var(--mono);letter-spacing:.08em;text-transform:uppercase;color:var(--mute);margin:16px 0 4px;border-bottom:1px solid var(--rule)}
ul.plist{list-style:none;margin:0;padding:0}
ul.plist li{padding:5px 0;border-bottom:1px solid var(--rule)}
ul.plist a{display:block}
ul.plist a[aria-current]{font-weight:700}
.stubtag{color:var(--red)}
input[type=search],input[type=text],textarea{width:100%;border:1px solid var(--ink);background:#fffdf8;padding:8px 10px;border-radius:2px}
textarea{resize:vertical}
.btn{border:1px solid var(--ink);background:transparent;padding:8px 14px;cursor:pointer;border-radius:2px}
.btn.pri{background:var(--red);border-color:var(--red);color:#fff}
.btn:disabled{opacity:.55;cursor:not-allowed}
.lnk{background:none;border:0;padding:0;color:var(--red);text-decoration:underline;cursor:pointer}
.grey{border-left:3px solid var(--rule);background:#ece7db;padding:8px 12px;margin:0 0 12px;font:12.5px/1.5 var(--mono)}
.badge{display:inline-block;border:1px solid var(--rule);padding:0 6px;margin:0 4px 4px 0;font:11.5px var(--mono)}
table{border-collapse:collapse;width:100%;margin:10px 0;font-size:15px}
caption{text-align:left;font:italic 18px var(--serif);padding:6px 0}
th{font:11.5px var(--mono);letter-spacing:.06em;text-transform:uppercase;text-align:left;border-bottom:2px solid var(--ink);padding:6px 8px 6px 0;vertical-align:bottom}
td{border-bottom:1px solid var(--rule);padding:6px 8px 6px 0;vertical-align:top}
td.n,th.n{text-align:right}
.pin{display:inline-flex;flex-wrap:wrap;align-items:baseline;gap:4px;border:1px solid var(--rule);border-radius:3px;padding:0 4px;margin:0 1px;background:#fbf8f1;font-size:14px;max-width:100%}
.pin.no{border-color:var(--amb)}
.pl{background:none;border:0;padding:0;color:var(--red);text-decoration:underline;cursor:pointer;font-size:14px;text-align:left}
.rg,.vw{font:11px var(--mono)}
.pin.ok .vw{color:var(--grn)}
.pin.no .vw{color:var(--amb)}
.px{border:0;background:none;cursor:pointer;padding:0 3px}
.pd{flex-basis:100%;display:block;font-size:13px;border-top:1px solid var(--rule);padding:4px 0}
.pd[hidden]{display:none}
.dangle{color:var(--red);font:12px var(--mono)}
.con{border:1px solid var(--rule);border-left:4px solid var(--red);padding:10px 14px;margin:14px 0;background:#faf7f0}
.con h4{font:400 19px/1.35 var(--serif);margin:4px 0}
.verdict{font:400 34px/1.1 var(--serif);margin:6px 0}
.bar{height:10px;background:var(--rule);margin:4px 0;max-width:420px}
.bar i{display:block;height:100%;background:var(--red)}
.ins{background:var(--ins);border-left:4px solid var(--amb);padding:2px 10px;margin:6px 0}
.dim{color:var(--mute)}
.dim .ins{color:var(--ink)}
.st{display:inline-block;min-width:54px;font:11.5px var(--mono);text-transform:uppercase;letter-spacing:.06em}
.st.ok{color:var(--grn)}
.st.no{color:var(--red);font-weight:700}
.st.na{color:var(--mute)}
.tag{font:11px var(--mono);color:var(--red);text-transform:uppercase;letter-spacing:.06em;margin-left:6px}
.err{border:1px solid var(--red);padding:10px 14px;margin:10px 0}
pre{white-space:pre-wrap;word-break:break-word;font:12px/1.4 var(--mono);background:#ece7db;padding:8px;max-height:220px;overflow:auto}
fieldset.chg{border:1px solid var(--ink);padding:10px 16px 14px;margin:10px 0}
legend{font:italic 19px var(--serif);padding:0 6px}
.prev{max-height:60vh;overflow:auto;border-top:1px solid var(--rule);margin:8px 0;padding-top:6px}
.steps{list-style:none;display:flex;flex-wrap:wrap;gap:6px 22px;margin:0 0 12px;padding:0;font:11.5px var(--mono);letter-spacing:.08em;color:var(--mute)}
.steps li.on{color:var(--red);border-bottom:2px solid var(--red)}
.nums{display:flex;gap:40px;margin:6px 0 10px}
.inb{display:flex;gap:16px;align-items:center;justify-content:space-between;border-top:1px solid var(--rule);border-bottom:1px solid var(--rule);padding:10px 0;margin:10px 0}
details{margin:6px 0}
summary{cursor:pointer}
.chips{display:flex;flex-wrap:wrap;gap:6px;margin:6px 0}
.chip{border:1px solid var(--rule);padding:1px 8px;border-radius:10px;font-size:14px;background:#fbf8f1}
.row2{display:flex;gap:10px;align-items:center;flex-wrap:wrap;margin:10px 0}
footer{border-top:1px solid var(--rule);padding:12px 28px 24px}
</style>
</head>
<body>
<header class="top">
 <div>
  <div class="lab">WIKI · neurotechnology and justice</div>
  <h1>Research wiki: neurotechnology in the administration of justice</h1>
  <p class="hint" id="hline"></p>
 </div>
 <div class="strip"><div id="strip" aria-live="polite"></div><div>This page has no storage: changes live in it until you download them (tab 05)</div></div>
</header>
<div id="tabs" role="tablist" aria-label="Workspace"></div>
<main>
 <section id="p1" role="tabpanel" aria-labelledby="t1">
  <div class="cols">
   <aside>
    <label for="flt" class="lab">title, tag or slug</label>
    <input id="flt" type="search" autocomplete="off">
    <div id="cnt" style="margin:12px 0 4px"></div>
    <div id="plist"></div>
   </aside>
   <div id="pview"></div>
  </div>
 </section>
 <section id="p2" role="tabpanel" aria-labelledby="t2" hidden>
  <h2 class="q">What does the wiki answer, and is it worth filing?</h2>
  <div class="grey" id="askNote"></div>
  <label for="askQ" class="lab">Your question</label>
  <textarea id="askQ" rows="3"></textarea>
  <div class="row2"><button id="askBtn" class="btn pri" data-act="ask" type="button">Ask the wiki</button><button id="askStop" class="btn" data-act="ask-stop" type="button" hidden>Stop</button><span id="askProg" class="hint" aria-live="polite"></span></div>
  <div id="askOut"></div>
 </section>
 <section id="p3" role="tabpanel" aria-labelledby="t3" hidden>
  <h2 class="q">What would the waiting document change?</h2>
  <div id="ingOut"></div>
 </section>
 <section id="p4" role="tabpanel" aria-labelledby="t4" hidden>
  <h2 class="q">Can I trust this?</h2>
  <div id="chkOut"></div>
 </section>
 <section id="p5" role="tabpanel" aria-labelledby="t5" hidden>
  <h2 class="q">What has changed, where do the sources disagree, and how do I take it away?</h2>
  <div id="recOut"></div>
 </section>
</main>
<footer class="hint" id="foot"></footer>
<script>
(function(){
'use strict';
const WD=window.WORKSHOP_DATA||{}, WK=WD.wiki||{}, LIBR=(WD.library&&WD.library.records)||[];
const FENCE='`'.repeat(3);
const PIN_SRC='\\[([^\\]]+)\\]\\(pin:([^#\\s)]+)#p(\\d+)(?: "([^"]*)")?\\) ?(✓|⚠)';
const PIN_LOOSE=PIN_SRC.replace('(✓|⚠)','(✓|⚠)?');
const REGN={a:'treaty law',b:'General Comments',c:'UN, agency and soft-law reports',d:'national human rights institution',e:'civil society',f:'scholarship'};
const REGS={a:'treaty law',b:'General Comment',c:'UN report',d:'NHRI report',e:'civil society',f:'scholarship'};
const WT={a:5,b:4,c:3,d:2,e:1,f:.5};
const SEC={source:'Sources',concept:'Concepts',entity:'Entities',question:'Questions'};
const BASE=['01 PAGES','02 ASK','03 INGEST','04 CHECK','05 RECORD'];
const $=(s,r)=>(r||document).querySelector(s);
const esc=s=>String(s==null?'':s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const rx=s=>s.replace(/[.*+?^${}()|[\]\\]/g,'\\$&');
const nf=n=>Number(n).toLocaleString('en-GB');
const uniq=a=>[...new Set(a)];
const sum=(a,f)=>a.reduce((x,y)=>x+f(y),0);
const today=()=>{const d=new Date();return d.getFullYear()+'-'+String(d.getMonth()+1).padStart(2,'0')+'-'+String(d.getDate()).padStart(2,'0');};
const slugify=s=>String(s||'').toLowerCase().normalize('NFKD').replace(/[̀-ͯ]/g,'').replace(/[^a-z0-9]+/g,'-').replace(/^-+|-+$/g,'').slice(0,70);
const norm=s=>String(s==null?'':s).normalize('NFKC').replace(/­/g,'').replace(/-\s+/g,'').replace(/[“”„]/g,'"').replace(/[‘’]/g,"'").replace(/[–—]/g,'-').replace(/\s+/g,' ').trim();
const tryJ=s=>{try{return JSON.parse(s);}catch(e){return undefined;}};
const humanise=s=>{s=String(s).replace(/-/g,' ');return s.charAt(0).toUpperCase()+s.slice(1);};
const cleanMk=s=>String(s).replace(/^<<(?:ins|end)>>\n?/gm,'').replace(/\n{3,}/g,'\n\n');

let pages=[],bySlug={},docs={},orig={},index=WK.index||'',log=WK.log||'',tensions=WK.tensions||'';
let curPage='',curTab=0,loadedWarn=0,lintRan=false,lastFiling=null,logNewest=true,ing=null;
const S={calls:0,chars:0,passages:0,changes:[],filings:0,logAdded:new Set(),tensAdded:new Set(),callLog:[],approved:new Set()};
const running={2:false,3:false};
const pinReg=[];
const ask={q:'',stage:'idle',chosen:[],changing:false,answer:null,run:null,prog:'',err:null,file:null,filed:null,fTitle:'',fTags:''};

/* ---------- parsing and verification ---------- */
function parsePins(body){const re=new RegExp(PIN_SRC,'g'),o=[];let m;while((m=re.exec(body)))o.push({label:m[1],id:m[2],page:+m[3],quote:m[4]||'',mark:m[5]});return o;}
function conBlocks(body){const re=new RegExp(FENCE+'contested[ \\t]*\\n([\\s\\S]*?)\\n'+FENCE,'g'),o=[];let m;while((m=re.exec(body)))o.push(m[1]);return o;}
function frags(q){return String(q).split(/…|\.\.\./).map(norm).filter(Boolean);}
function inText(text,q){const fr=frags(q);if(!fr.length)return false;const t=norm(text);let pos=0;for(const f of fr){const k=t.indexOf(f,pos);if(k<0)return false;pos=k+f.length;}return true;}
function verify(pin,allow){
  const d=docs[pin.id];
  if(!d)return {ok:false,why:'no document '+pin.id+' in the library'};
  if(d.status==='inbox'&&allow!==pin.id)return {ok:false,why:'the document is in the inbox: not yet read into the wiki'};
  if(!pin.quote)return {ok:false,why:'the pin has no quote'};
  const fr=frags(pin.quote);if(!fr.length)return {ok:false,why:'the quote is empty'};
  const cands=(d.passages||[]).filter(x=>x.page===pin.page);
  if(!cands.length)return {ok:false,why:'no passage of '+pin.id+' starts on PDF page '+pin.page+' (footnotes, tables and captions are not in the passages)'};
  let bad=null;
  for(const x of cands){
    const t=x._n||(x._n=norm(x.text));let pos=0,ok=true;
    for(const f of fr){const k=t.indexOf(f,pos);if(k<0){ok=false;break;}pos=k+f.length;}
    if(!ok)continue;
    const want=x.paragraph?'para. '+x.paragraph:'p. '+x.page_label;
    if(new RegExp(rx(want)+'(?![\\w])').test(pin.label))return {ok:true,passage:x};
    bad={ok:false,labelBad:true,why:'quote found, but the label should say "'+want+'"',passage:x};
  }
  return bad||{ok:false,why:'quote not found in a passage that starts on PDF page '+pin.page};
}
function rebuild(){
  bySlug={};pages.forEach(p=>{bySlug[p.slug]=p;});
  pages.forEach(p=>{p._links=[...p.body.matchAll(/\[\[([^\]|#]+)/g)].map(m=>m[1].trim());p._pins=parsePins(p.body);p._v=p._pins.map(x=>verify(x));p._con=conBlocks(p.body);p._back=[];});
  pages.forEach(p=>uniq(p._links).forEach(l=>{if(bySlug[l]&&l!==p.slug)bySlug[l]._back.push(p.slug);}));
}
function vcount(p){return p._v.filter(v=>v.ok).length;}
function citeAs(d){
  const c={};pages.forEach(p=>p._pins.forEach(x=>{if(x.id===d.id){const m=x.label.match(/^(.*?), (?:para\.|p\.) /);if(m)c[m[1]]=(c[m[1]]||0)+1;}}));
  const b=Object.entries(c).sort((x,y)=>y[1]-x[1])[0];
  return b?b[0]:(d.symbol||((d.author||'')+' '+d.year));
}
function docReg(id){
  const d=docs[id];
  let p=pages.find(x=>x.type==='source'&&(x.frontmatter.sources||[]).length===1&&x.frontmatter.sources[0]===id);
  if(!p&&d)p=pages.find(x=>x.frontmatter.status==='stub'&&((x.frontmatter.sources||[]).includes(id)||x.slug===slugify(d.symbol||d.id)));
  return (p&&p.frontmatter.register)||[];
}
const regTxt=id=>{const r=docReg(id);return r.length?'('+r.join('')+')':'(?)';};
function mkPin(d,ps,quote){
  const q=quote.replace(/\s+/g,' ').replace(/"([^"]*)"/g,'“$1”').replace(/"/g,'”');
  return '['+citeAs(d)+(ps.paragraph?', para. '+ps.paragraph:', p. '+ps.page_label)+'](pin:'+d.id+'#p'+ps.page+' "'+q+'") ✓';
}
function fixPins(text,id){
  let ok=0,removed=0;const keep=[];
  let out=String(text).replace(new RegExp(PIN_LOOSE,'g'),(m,label,did,pg,quote)=>{
    const v=verify({label,id:did,page:+pg,quote:quote||''},id);
    if(v.ok){ok++;return '\u0001'+(keep.push('['+label+'](pin:'+did+'#p'+pg+' "'+quote+'") ✓')-1)+'\u0002';}
    removed++;return label+' (pin removed: not verified)';
  });
  out=out.replace(/\[([^\]]+)\]\(pin:[^)]*\)/g,(m,l)=>{removed++;return l+' (pin removed: malformed)';});
  out=out.replace(/\u0001(\d+)\u0002/g,(m,i)=>keep[+i]);
  return {text:out,ok,removed};
}

/* ---------- markdown ---------- */
function inline(s,ctx){
  const re=new RegExp(PIN_SRC+'|\\[\\[([^\\]|#]+)(?:[|#][^\\]]*)?\\]\\]|\\[([^\\]]+)\\]\\((https?:\\/\\/[^)\\s]+)\\)|\\*\\*(.+?)\\*\\*|\\*([^*\\s][^*]*?)\\*','g');
  let o='',last=0,m;
  while((m=re.exec(s))){
    o+=esc(s.slice(last,m.index));
    if(m[1]!==undefined)o+=pinChip({label:m[1],id:m[2],page:+m[3],quote:m[4]||'',mark:m[5]},ctx);
    else if(m[6]!==undefined)o+=wlink(m[6].trim());
    else if(m[7]!==undefined)o+='<a href="'+esc(m[8])+'" target="_blank" rel="noopener">'+esc(m[7])+'</a>';
    else if(m[9]!==undefined)o+='<strong>'+inline(m[9],ctx)+'</strong>';
    else o+='<em>'+esc(m[10])+'</em>';
    last=re.lastIndex;
  }
  return o+esc(s.slice(last));
}
function wlink(s){const p=bySlug[s];if(!p)return '<span class="dangle">[['+esc(s)+']] · no page</span>';return '<a href="#'+esc(s)+'" data-act="open-page" data-slug="'+esc(s)+'">'+esc(p.title)+'</a>';}
function pinChip(pin,ctx){
  const key=pin.id+'#p'+pin.page+'|'+norm(pin.quote);
  if(ctx&&ctx.allowed&&!ctx.allowed.has(key))return '<span class="pin no"><s>'+esc(pin.label)+'</s> <span class="vw">not on the pages sent</span></span>';
  const v=verify(pin,ctx&&ctx.allow),d=docs[pin.id];
  const i=pinReg.push({id:pin.id,page:pin.page,quote:pin.quote})-1;
  const diff=(pin.mark==='✓'&&!v.ok)?'page says ✓':(pin.mark==='⚠'&&v.ok)?'page says ⚠':'';
  const det=(pin.quote?'“'+esc(pin.quote)+'”':'<i>no quote</i>')+'<br>'+(v.passage?'Passage: '+(v.passage.paragraph?'para. '+esc(v.passage.paragraph):'p. '+esc(v.passage.page_label))+' · '+esc(v.passage.text.slice(0,300))+(v.passage.text.length>300?'…':''):'Not verified: '+esc(v.why))+'<br><button type="button" class="lnk" data-act="pin-open" data-pin="'+i+'" aria-label="Open '+esc(d?d.symbol||d.short_title:pin.id)+' at PDF page '+pin.page+'">Open the PDF page</button>';
  return '<span class="pin '+(v.ok?'ok':'no')+'"><button type="button" class="pl" data-act="pin-open" data-pin="'+i+'" aria-label="Open '+esc(pin.label)+' at PDF page '+pin.page+'">'+esc(pin.label)+'</button><span class="rg" title="register">'+regTxt(pin.id)+'</span><span class="vw">'+(v.ok?'✓ verified':'⚠ not found')+'</span>'+(diff?'<span class="vw">'+diff+'</span>':'')+'<button type="button" class="px" data-act="pin-toggle" aria-expanded="false" aria-label="Show the quote for '+esc(pin.label)+'">▾</button><span class="pd" hidden>'+det+'</span></span>';
}
function md(src,ctx){
  const L=String(src||'').replace(/\r/g,'').split('\n'),out=[],fenceRe=new RegExp('^'+FENCE+'(\\w*)\\s*$');
  let para=[],list=null,i=0;
  const fp=()=>{if(para.length){out.push('<p>'+inline(para.join(' '),ctx)+'</p>');para=[];}};
  const fl=()=>{if(list){out.push('<'+list.t+'>'+list.it.map(x=>'<li>'+inline(x,ctx)+'</li>').join('')+'</'+list.t+'>');list=null;}};
  while(i<L.length){
    const ln=L[i];let m;
    if((m=ln.match(fenceRe))){fp();fl();const buf=[];i++;while(i<L.length&&!fenceRe.test(L[i]))buf.push(L[i++]);i++;out.push(m[1]==='contested'?conCard(buf.join('\n'),ctx):'<pre>'+esc(buf.join('\n'))+'</pre>');continue;}
    if(ln==='<<ins>>'){fp();fl();out.push('<div class="ins" data-source="ai">');i++;continue;}
    if(ln==='<<end>>'){fp();fl();out.push('</div>');i++;continue;}
    if((m=ln.match(/^(#{1,4})\s+(.*)$/))){fp();fl();const n=m[1].length+1;out.push('<h'+n+'>'+inline(m[2],ctx)+'</h'+n+'>');i++;continue;}
    if((m=ln.match(/^\s*([-*]|\d+[.)])\s+(.*)$/))){fp();const t=/\d/.test(m[1])?'ol':'ul';if(list&&list.t!==t)fl();if(!list)list={t,it:[]};list.it.push(m[2]);i++;continue;}
    if(!ln.trim()){fp();fl();i++;continue;}
    if(list&&/^\s+\S/.test(ln)){list.it[list.it.length-1]+=' '+ln.trim();i++;continue;}
    fl();para.push(ln.trim());i++;
  }
  fp();fl();return out.join('\n');
}
function parseCon(txt){
  const o={claim:'',verdict:'',note:'',pos:[]};
  String(txt).split('\n').forEach(l=>{let m;
    if((m=l.match(/^claim:\s*(.*)$/)))o.claim=m[1];
    else if((m=l.match(/^verdict:\s*(.*)$/)))o.verdict=m[1].trim();
    else if((m=l.match(/^note:\s*(.*)$/)))o.note=m[1];
    else if((m=l.match(/^([+\-~])\s+(.*)$/))){const f=m[2].split(' | ');o.pos.push({sign:m[1],reg:(f[0]||'').trim().toLowerCase(),pin:f[1]||'',gloss:f[2]||'',page:f[3]||''});}
  });
  return o;
}
function conCard(txt,ctx){
  const c=parseCon(txt);let tot=0,sup=0;
  c.pos.forEach(x=>{const w=WT[x.reg]||0;tot+=w;sup+=x.sign==='+'?w:x.sign==='~'?w/2:0;});
  const pct=tot?Math.round(100*sup/tot):null,words={'+':'supports','-':'contests','~':'mixed'};
  const tn=ctx&&ctx.slug?tensEntries().items.find(x=>x.card===ctx.slug):null;
  return '<section class="con"><div class="lab">FIG.01 · contested claim</div><h4>'+inline(c.claim,ctx)+'</h4><div class="verdict">'+esc(c.verdict.replace(/-/g,' ')||'no verdict')+'</div><p>'+inline(c.note,ctx)+'</p>'
   +'<div class="hint">descriptive: support '+(pct==null?'n/a':pct+'%')+' of weighted positions, weights a 5 · b 4 · c 3 · d 2 · e 1 · f ½; the verdict is the answer</div>'
   +'<div class="bar" role="img" aria-label="Descriptive lean: '+(pct==null?'n/a':pct+' percent')+' support"><i style="width:'+(pct||0)+'%"></i></div>'
   +'<div class="hint">How this is computed: (weight of + positions + ½ weight of ~ positions) ÷ weight of all positions.</div>'
   +'<table><caption>Positions on this claim</caption><thead><tr><th scope="col">Position</th><th scope="col">Register</th><th scope="col">Pin</th><th scope="col">Gloss</th><th scope="col">Page</th></tr></thead><tbody>'
   +c.pos.map(x=>'<tr><td>'+words[x.sign]+'</td><td class="mono">('+esc(x.reg)+') '+esc(REGS[x.reg]||'')+'</td><td>'+inline(x.pin,ctx)+'</td><td>'+inline(x.gloss,ctx)+'</td><td>'+inline(x.page,ctx)+'</td></tr>').join('')+'</tbody></table>'
   +(tn?'<a href="#" data-act="open-tens" data-head="'+esc(tn.head)+'">in the tensions register</a>':'')+'</section>';
}
function tensEntries(){
  const parts=tensions.split(/^### /m),intro=parts.shift();
  return {intro,items:parts.map(t=>{const nl=t.indexOf('\n'),head=(nl<0?t:t.slice(0,nl)).trim(),body=nl<0?'':t.slice(nl+1),m=body.match(/card:[^\n]*?\[\[([^\]|#]+)/);return {head,body,card:m?m[1].trim():null};})};
}
function logEntries(){
  const parts=log.split(/^## /m);parts.shift();
  return parts.map(t=>{const nl=t.indexOf('\n'),h=(nl<0?t:t.slice(0,nl)).trim();return {head:'## '+h,title:h,body:nl<0?'':t.slice(nl+1)};});
}

/* ---------- lint and self-checks ---------- */
function lintAll(){
  const idxSlugs=[...index.matchAll(/^\s*[-*]\s*\[\[([^\]|#]+)\]\]/gm)].map(m=>m[1].trim()),idxN={};
  index.split('\n').forEach(l=>{const m=l.match(/^\s*[-*]\s*\[\[([^\]|#]+)\]\][^\n]*✓\s*(\d+)/);if(m)idxN[m[1].trim()]=+m[2];});
  const te=tensEntries().items.filter(x=>x.card),C=[],add=(id,name,items)=>C.push({id,name,items});
  add('dang','Dangling links ([[slug]] with no page)',pages.flatMap(p=>uniq(p._links).filter(l=>!bySlug[l]).map(l=>({slug:p.slug,note:'[['+l+']]'}))));
  add('orph','Orphan pages (no other page links to them)',pages.filter(p=>!p._back.length).map(p=>({slug:p.slug})));
  add('unv','Pins not verified by this page',pages.flatMap(p=>p._pins.map((x,i)=>p._v[i].ok?null:{slug:p.slug,note:x.label+': '+p._v[i].why}).filter(Boolean)));
  add('lie','Pins marked ✓ that fail',pages.flatMap(p=>p._pins.map((x,i)=>(x.mark==='✓'&&!p._v[i].ok)?{slug:p.slug,note:x.label}:null).filter(Boolean)));
  add('src','Pages whose sources differ from the documents pinned',pages.filter(p=>{const a=uniq(p.frontmatter.sources||[]).sort().join('|'),b=uniq(p._pins.map(x=>x.id)).sort().join('|');return a!==b;}).map(p=>({slug:p.slug})));
  add('nop','Pages with no pins',pages.filter(p=>!p._pins.length).map(p=>({slug:p.slug})));
  add('rec','Links not reciprocated (A lists B, B does not list A)',pages.flatMap(p=>(p.frontmatter.links||[]).filter(l=>bySlug[l]&&!(bySlug[l].frontmatter.links||[]).includes(p.slug)).map(l=>({slug:p.slug,note:'→ '+l}))));
  add('idx','Pages missing from the index, and index lines without a page',[...pages.filter(p=>!idxSlugs.includes(p.slug)).map(p=>({slug:p.slug,note:'not in the index'})),...idxSlugs.filter(s=>!bySlug[s]).map(s=>({slug:s,note:'index line without a page'}))]);
  add('idn','Index ✓N that differs from the computed count',pages.filter(p=>p.slug in idxN&&idxN[p.slug]!==vcount(p)).map(p=>({slug:p.slug,note:'index '+idxN[p.slug]+', computed '+vcount(p)})));
  add('ten','Contested cards without a tensions entry, and the reverse',[...pages.filter(p=>p._con.length&&!te.some(x=>x.card===p.slug)).map(p=>({slug:p.slug,note:'no tensions entry'})),...te.filter(x=>!bySlug[x.card]||!bySlug[x.card]._con.length).map(x=>({slug:x.card,note:'tensions entry without a card'}))]);
  add('stub','Stub pages',pages.filter(p=>p.frontmatter.status==='stub').map(p=>({slug:p.slug})));
  add('inb','Pins to a document still in the inbox',pages.flatMap(p=>p._pins.filter(x=>docs[x.id]&&docs[x.id].status==='inbox').map(x=>({slug:p.slug,note:x.label}))));
  return C;
}
const needLook=()=>lintAll().filter(c=>c.items.length).length;
function slugLinks(items,max){
  const u=uniq(items.map(x=>x.slug)),sh=u.slice(0,max||12);
  return sh.map(s=>bySlug[s]?'<a href="#'+esc(s)+'" data-act="open-page" data-slug="'+esc(s)+'">'+esc(s)+'</a>':esc(s)).join(', ')+(u.length>sh.length?' … and '+(u.length-sh.length)+' more':'');
}
function selfChecks(){
  const R=[],L=Object.fromEntries(lintAll().map(c=>[c.id,c])),pins=sum(pages,p=>p._pins.length),ver=sum(pages,vcount);
  const m=index.split('\n').slice(0,8).join('\n').match(/(\d[\d,]*) pins/),stated=m?+m[1].replace(/,/g,''):null;
  const ck=(g,t,ok,items)=>R.push({g,t,ok,items:items||[]});
  ck('Pins','Pins found by the regular expression ('+nf(pins)+') against the number stated in the index ('+(stated==null?'none stated':nf(stated))+')',stated===pins);
  ck('Pins','Verified by this page ('+nf(ver)+') against found ('+nf(pins)+'); ✓ marks that fail: '+L.lie.items.length,ver===pins&&!L.lie.items.length,L.lie.items);
  const lb=sum(pages,p=>p._v.filter(v=>v.labelBad).length);
  ck('Labels','Pins whose quote is found but whose label does not match the passage’s paragraph or page label: '+lb,lb===0);
  ck('Structure','Dangling links '+L.dang.items.length+'; orphan pages '+L.orph.items.length,!L.dang.items.length&&!L.orph.items.length,[...L.dang.items,...L.orph.items]);
  ck('Structure','sources equal the pinned documents on '+(pages.length-L.src.items.length)+' of '+pages.length+' pages',!L.src.items.length,L.src.items);
  ck('Structure','Every page in the index and every index [[slug]] a page: '+L.idx.items.length+' differences',!L.idx.items.length,L.idx.items);
  ck('Structure','Contested cards ('+sum(pages,p=>p._con.length)+') against tensions card: entries ('+tensEntries().items.filter(x=>x.card).length+'): '+L.ten.items.length+' differences',!L.ten.items.length,L.ten.items);
  if(!S.callLog.length)ck('Model answers','No call to the model yet',null);
  S.callLog.forEach((c,i)=>ck('Model answers','Call '+(i+1)+' ('+c.kind+'): '+(c.parsed?'JSON parsed':'JSON not parsed')+'; slugs not in the wiki: '+((c.bad||[]).length)+(c.returned!=null?'; returned '+c.returned+' = verified '+c.ver+' + could not verify '+c.fail+' + dropped '+c.drop:''),c.parsed&&(c.returned==null||c.returned===c.ver+c.fail+c.drop)));
  if(!ing)ck('Coverage','No ingest started',null);
  else{const n=ing.doc.passages.length,done=ing.next>=ing.batches.length;ck('Coverage','Passages sent ('+ing.sent+') against passages.length ('+n+')'+(done?'':' — the run is not complete')+'; takeaways naming a passage that was not sent: dropped and counted ('+ing.dropped+')',done?ing.sent===n:null);}
  const warn=sum(pages,p=>p._pins.filter(x=>x.mark==='⚠').length);
  const changed=pages.filter(p=>!(p.slug in orig)||orig[p.slug]!==p.body),badCh=sum(changed,p=>p._v.filter(v=>!v.ok).length);
  ck('Unverified','⚠ pins in the wiki now: '+warn+' (at load: '+loadedWarn+'); pins in changed pages that do not verify: '+badCh,warn===loadedWarn&&badCh===0);
  if(ing&&ing.tk.length){const v=ing.tk.filter(t=>t.ok).length,f=ing.tk.length-v;ck('Unverified','Could not verify ('+f+') plus verified takeaways ('+v+') equal takeaways returned ('+ing.tkRet+') less those dropped ('+ing.dropped+')',f+v===ing.tkRet-ing.dropped);}
  const una=changed.filter(p=>!S.approved.has(p.slug));
  ck('Approval','Pages changed in the wiki ('+changed.length+') against approved changes ('+S.approved.size+'); changed without an approved card: '+una.length,!una.length&&changed.length===S.approved.size,una.map(p=>({slug:p.slug})));
  if(!S.filings)ck('Filing','Nothing filed yet',null);
  else{
    const lastLog=logEntries().slice(-1)[0],names=lastFiling?lastFiling.slugs:[];
    const miss=names.filter(s=>!(lastLog&&lastLog.body.includes('[['+s+']]'))&&!(lastLog&&lastLog.title.includes(s)));
    const idxBad=lintAll().find(c=>c.id==='idn').items;
    ck('Filing','Changed pages re-parsed and re-verified (pins that fail: '+badCh+'); index counts equal the pages’ verified pins ('+idxBad.length+' differences); last log entry names '+(names.length-miss.length)+' of '+names.length+' changed pages',badCh===0&&!idxBad.length&&!miss.length);
    if(lastFiling)ck('Filing','Lint checks needing a look: before '+lastFiling.before+', after '+lastFiling.after+' (side by side)',lastFiling.after<=lastFiling.before);
  }
  ck('Session','Log entries added this session ('+S.logAdded.size+') against filings made ('+S.filings+'); a download would hold '+pages.length+' pages (pages.length '+pages.length+')',S.logAdded.size===S.filings);
  return R;
}

/* ---------- rendering: header, tabs, pages ---------- */
function setRunning(k,b){running[k]=b;const s=$('#t'+k+' .run');if(s)s.textContent=b?' · running':'';}
function renderStrip(){$('#strip').textContent='Changes this session: '+S.changes.length+' · Calls to the model: '+S.calls+' · Passages that left the browser: '+S.passages;}
function renderHead(){
  const c={};pages.forEach(p=>{c[p.type]=(c[p.type]||0)+1;});
  const inbox=Object.values(docs).filter(d=>d.status==='inbox').length;
  $('#hline').textContent=pages.length+' pages ('+(c.source||0)+' sources, '+(c.concept||0)+' concepts, '+(c.entity||0)+' entities, '+(c.question||0)+' questions) · '+nf(sum(pages,p=>p._pins.length))+' pins, '+nf(sum(pages,vcount))+' verified by this page · '+LIBR.length+' documents, '+inbox+' in the inbox · built '+(WK.built||'unknown');
  renderStrip();
}
function showTab(i,focus){
  curTab=i;const tabs=document.querySelectorAll('.tab');
  tabs.forEach((b,k)=>{const on=k===i;b.setAttribute('aria-selected',String(on));b.tabIndex=on?0:-1;b.classList.toggle('on',on);$('#p'+(k+1)).hidden=!on;});
  if(focus)tabs[i].focus();
  if(i===3)renderCheck();
  if(i===4)renderRecord();
}
function openPage(slug){
  curPage=bySlug[slug]?slug:'';
  try{if(decodeURIComponent(location.hash.slice(1))!==curPage)location.hash=curPage;}catch(e){}
  showTab(0);renderList();renderPageView();window.scrollTo(0,0);
}
function openTens(head){showTab(4);const el=document.getElementById('tens-'+slugify(head));if(el){el.scrollIntoView();el.querySelector('summary').focus();el.open=true;}}
function renderList(){
  const q=($('#flt').value||'').trim().toLowerCase();
  const f=pages.filter(p=>!q||(p.title+' '+p.slug+' '+(p.frontmatter.tags||[]).join(' ')).toLowerCase().includes(q));
  $('#cnt').innerHTML='<span class="big">'+f.length+'</span> <span class="hint">of '+pages.length+' pages</span>';
  const order=['source','concept','entity','question'].concat(uniq(pages.map(p=>p.type)).filter(t=>!SEC[t]));
  let h='';
  order.forEach(t=>{const g=f.filter(p=>p.type===t);if(!g.length)return;
    h+='<div class="grp">'+esc(t)+' ('+g.length+')</div><ul class="plist">'+g.map(p=>'<li><a href="#'+esc(p.slug)+'" data-act="open-page" data-slug="'+esc(p.slug)+'"'+(p.slug===curPage?' aria-current="page"':'')+'>'+esc(p.title)+'</a><span class="hint">('+esc((p.frontmatter.register||[]).join(''))+') · '+p._pins.length+' pins'+(p.frontmatter.status==='stub'?' · <b class="stubtag">stub</b>':'')+'</span></li>').join('')+'</ul>';});
  $('#plist').innerHTML=h||'<p class="hint">No page matches.</p>';
}
function pageMarkdown(p){return '---\n'+Object.keys(p.frontmatter).map(k=>k+': '+JSON.stringify(p.frontmatter[k])).join('\n')+'\n---\n\n'+p.body;}
function renderPageView(){
  const el=$('#pview');
  if(!curPage||!bySlug[curPage]){el.innerHTML='<div class="lab">INDEX · what does the wiki say?</div><h2 class="ptitle">Index</h2><div class="body">'+md(index,{})+'</div><p class="hint">How this is computed: the index is the wiki’s own text. Pins counted here and in the header are found by this page’s code, not read from the index. Choose a page on the left.</p>';return;}
  const p=bySlug[curPage],fm=p.frontmatter,ctx={slug:p.slug},bl=p._links;
  const body=p.body.replace(/^#\s+.*\n+/,'');
  const out=uniq(fm.links||[]),src=fm.sources||[];
  el.innerHTML='<article><div class="lab"><a href="#" data-act="open-page" data-slug="">Index</a> · PAGE · '+esc(p.slug)+'</div><h2 class="ptitle">'+esc(p.title)+'</h2>'
   +'<div><span class="badge">'+esc(p.type)+'</span>'+(fm.register||[]).map(l=>'<span class="badge">('+esc(l)+') '+esc(REGN[l]||'')+'</span>').join('')+'<span class="badge">status: '+esc(fm.status||'?')+'</span><span class="badge">updated '+esc(fm.updated||'?')+'</span></div>'
   +'<div class="hint">tags: '+esc((fm.tags||[]).join(', ')||'none')+'</div>'
   +'<div class="body">'+md(body,ctx)+'</div>'
   +'<p class="hint">How this is computed: '+p._pins.length+' pins found in this body by regular expression; '+vcount(p)+' verified = the quote (fragments in order) stands in a passage of that document starting on that PDF page, and the label names its paragraph or page label.</p>'
   +'<h3 class="s">Links out</h3>'+(out.length?'<ul>'+out.map(s=>'<li>'+wlink(s)+(bl.includes(s)?'':' <span class="hint">frontmatter only</span>')+'</li>').join('')+'</ul>':'<p class="hint">none</p>')
   +'<h3 class="s">Linked from</h3>'+(p._back.length?'<ul>'+p._back.map(s=>'<li>'+wlink(s)+'</li>').join('')+'</ul>':'<p class="hint">no page links here</p>')
   +'<h3 class="s">Sources</h3>'+(src.length?'<ul>'+src.map(id=>{const d=docs[id];return d?'<li><a href="'+esc(d.url)+'" target="_blank" rel="noopener">'+esc(d.short_title||d.title)+'</a> <span class="hint">'+esc(d.kind)+' · '+esc(d.year)+(d.status==='inbox'?' · inbox':'')+'</span></li>':'<li>'+esc(id)+' <span class="hint">not in the library</span></li>';}).join('')+'</ul>':'<p class="hint">none</p>')
   +'<p><button type="button" class="btn" data-act="copy-page">Copy page as markdown</button></p></article>';
}

/* ---------- model calls ---------- */
async function callModel(prompt,nPass,kind){
  S.calls++;S.chars+=prompt.length;S.passages+=nPass;renderStrip();
  const rec={kind,parsed:false};S.callLog.push(rec);
  let raw;
  try{if(!(window.studio&&typeof studio.ask==='function'))throw new Error('studio.ask is not available in this preview');raw=await studio.ask(prompt,{json:true});}
  catch(e){return {ok:false,raw:'',error:String(e&&e.message||e),rec};}
  let d;
  if(raw&&typeof raw==='object'){d=raw;raw=JSON.stringify(raw);}
  else{raw=String(raw==null?'':raw);d=tryJ(raw);
    if(d===undefined){const m=raw.match(new RegExp(FENCE+'(?:json)?\\s*([\\s\\S]*?)'+FENCE));if(m)d=tryJ(m[1]);}
    if(d===undefined){const a=raw.indexOf('{'),b=raw.lastIndexOf('}');if(a>=0&&b>a)d=tryJ(raw.slice(a,b+1));}}
  if(d===undefined||d===null||typeof d!=='object')return {ok:false,raw,rec};
  rec.parsed=true;return {ok:true,data:d,raw,rec};
}
const PINRULE='Pin syntax: [label](pin:ID#pPAGE "verbatim quote") ✓. Quote only words that stand in the passages given; the code will check every quotation, and a pin that does not verify is removed.';
const REGRULE='Registers: (a) treaty law, (b) General Comments, (c) UN, agency and soft-law reports, (d) national human rights institution, (e) civil society, (f) scholarship. Name the register where it matters, keep the document’s own verb ("notes", "recommends", "proposes"), and never present (c) to (f) as what the treaty requires.';
function errHtml(e,act){return '<div class="err" role="alert"><p>The model’s answer could not be used'+(e.why?': '+esc(e.why):'')+'. Nothing was filed.</p><pre data-source="ai">'+esc(e.raw||'(no answer)')+'</pre><button type="button" class="btn" data-act="'+act+'">Retry</button></div>';}

/* ---------- tab 02: ask ---------- */
function pinKey(p){return p.id+'#p'+p.page+'|'+norm(p.quote);}
function askEval(){
  const a=ask.answer,pins=parsePins(a.answer);let good=0,bad=0;const reg={};
  pins.forEach(p=>{if(a.allowed.has(pinKey(p))&&verify(p).ok){good++;const r=(docReg(p.id)[0]||'?');reg[r]=(reg[r]||0)+1;}else bad++;});
  return {pins,good,bad,reg};
}
function buildQ(){
  const a=ask.answer,title=(ask.fTitle||a.title||'Untitled question').trim();
  const base=slugify(title)||'question';let slug=base,n=2;while(bySlug[slug])slug=base+'-'+n++;
  const pins=parsePins(a.answer),text=a.answer.trim(),first=text.split(/\n\s*\n/)[0];
  const links=uniq([...text.matchAll(/\[\[([^\]|#]+)/g)].map(m=>m[1].trim())).filter(s=>bySlug[s]);
  const sources=uniq(pins.map(p=>p.id)),reg=uniq(sources.flatMap(id=>docReg(id))).sort();
  const tags=(ask.fTags||'').split(',').map(s=>s.trim()).filter(Boolean);
  const body='# '+title+'\n\n**Short answer.** '+first+'\n\n## Reasoning\n\n'+text+'\n\n## What the library cannot answer\n\n'+(a.cannot||'Nothing was flagged.')+'\n\n## Related\n\n'+(links.map(s=>'- [['+s+']]').join('\n')||'- (no page linked)')+'\n';
  const ev=askEval(),reasons=[];
  if(!ev.pins.length)reasons.push('the answer has no pins');
  if(ev.bad)reasons.push(ev.bad+' pin(s) are struck through or do not verify');
  return {slug,title,first,body,links,sources,reg,tags,ev,reasons,fileable:!reasons.length,
    page:{slug,type:'question',title,body,frontmatter:{title,type:'question',tags,register:reg,status:'draft',updated:today(),links,sources}}};
}
function plain(s){return String(s).replace(new RegExp(PIN_LOOSE,'g'),'').replace(/\[\[([^\]|#]+)\]\]/g,'$1').replace(/[*_]/g,'').replace(/\s+/g,' ').trim();}
function renderAsk(){
  const a=ask,run=!!a.run;
  const k=a.chosen.length,ch=sum(a.chosen,s=>bySlug[s]?bySlug[s].body.length:0);
  $('#askNote').textContent=a.stage==='chosen'?'Step 2 will send '+k+' pages, '+nf(ch)+' characters, and your question. 0 library passages will leave the browser.'
   :a.stage==='s2'?k+' pages, '+nf(ch)+' characters; 0 library passages have left the browser.'
   :'Step 1 sends the wiki’s index ('+nf(index.length)+' characters) and your question to a language model. Step 2 then sends the bodies of up to 5 pages it names, announced here first. No library passages are sent. Nothing is sent until you press the button.';
  const b=$('#askBtn');b.textContent=a.stage==='chosen'?'Send these '+k+' pages':a.answer?'Ask again':'Ask the wiki';b.disabled=run;
  $('#askStop').hidden=!run;$('#askProg').textContent=a.prog||'';
  let h='';
  if(a.err)h+=errHtml(a.err,a.err.retry==='ask2'?'ask-retry2':'ask-retry1');
  if((a.chosen.length||a.changing)&&(a.stage==='chosen'||a.stage==='s2'||a.answer||a.changing)){
    h+='<div data-source="ai"><div class="lab">Pages chosen by the model</div><div class="chips">'+a.chosen.map(s=>'<span class="chip">'+wlink(s)+'</span>').join('')+'</div></div>';
    if(!run)h+='<button type="button" class="lnk" data-act="ask-change">Change pages</button>';
    if(a.changing)h+='<fieldset><legend>Tick up to 5 pages</legend>'+pages.map(p=>'<label style="display:block"><input type="checkbox" data-pick="'+esc(p.slug)+'"'+(a.chosen.includes(p.slug)?' checked':'')+'> '+esc(p.title)+'</label>').join('')+'</fieldset>';
  }
  if(a.answer){
    const A=a.answer,ev=askEval();
    h+='<article data-source="ai" style="border-top:1px solid var(--rule);margin-top:14px"><div class="lab">ANSWER · written by the model, every pin checked by this page</div><h3 class="s">'+esc(A.title||'Answer')+'</h3><div class="body">'+md(A.answer,{allowed:A.allowed})+'</div><h4>What the library cannot answer</h4><p>'+esc(A.cannot||'Nothing was flagged.')+'</p></article>';
    h+='<p class="hint">Verified pins by register: '+(Object.keys(ev.reg).sort().map(r=>'('+r+') '+(REGS[r]||'?')+' '+ev.reg[r]).join(' · ')||'none')+' · struck through or failing: '+ev.bad+'</p>';
    h+='<div class="row2"><button type="button" class="btn" data-act="ask-file-open" aria-expanded="'+!!a.file+'">File as a question page</button></div>';
    if(a.file)h+='<fieldset class="chg"><legend>File as a question page</legend><label for="fT" class="lab">Title</label><input id="fT" type="text" value="'+esc(a.fTitle||A.title)+'"><label for="fG" class="lab">Tags (comma-separated)</label><input id="fG" type="text" value="'+esc(a.fTags)+'"><div id="fPrev"></div></fieldset>';
  }
  if(a.filed)h+='<p aria-live="polite"><b>Filed.</b> The page is now in the wiki: '+wlink(a.filed)+'. The index and the log were updated.</p>';
  $('#askOut').innerHTML=h;
  if(a.file)updFile();
}
function updFile(){
  const q=buildQ(),el=$('#fPrev');if(!el)return;
  el.innerHTML='<p class="hint">Preview of the page the code will build. slug: '+esc(q.slug)+' · type: question · register: ('+esc(q.reg.join(''))+') · status: draft · updated '+today()+' · links: '+q.links.length+' · sources: '+esc(q.sources.join(', '))+'</p><div class="prev" data-source="ai">'+md(q.body,{allowed:ask.answer.allowed})+'</div>'
   +'<div class="row2"><button type="button" class="btn pri" data-act="ask-file"'+(q.fileable?'':' disabled')+'>File this page</button><button type="button" class="btn" data-act="ask-copy">Copy answer</button><span class="hint">'+(q.fileable?'Every pin verifies.':'Disabled: '+esc(q.reasons.join('; '))+'.')+'</span></div>';
}
async function askStep1(){
  const q=($('#askQ').value||'').trim();ask.q=q;
  if(!q){ask.prog='Type a question first.';renderAsk();return;}
  const run={stop:false};ask.run=run;ask.stage='s1';ask.answer=null;ask.file=null;ask.filed=null;ask.err=null;ask.changing=false;ask.chosen=[];
  ask.prog='Step 1 of 2 · sending the index ('+nf(index.length)+' characters) and your question…';setRunning(2,true);renderAsk();
  const prompt='You help with a research wiki on neurotechnology in the administration of justice. Below are the wiki’s index (one line per page) and a question. Choose up to 5 pages whose bodies are most likely to answer it. Return JSON {"pages": ["slug", ...]} using only slugs that appear in the index.\n\nINDEX\n'+index+'\n\nQUESTION\n'+q;
  const r=await callModel(prompt,0,'ask, step 1');
  if(run.stop)return;
  ask.run=null;setRunning(2,false);
  if(!r.ok){ask.stage='err';ask.err={raw:r.raw||r.error,retry:'ask1'};ask.prog='';return renderAsk();}
  const names=uniq((Array.isArray(r.data.pages)?r.data.pages:[]).map(s=>String(s).replace(/^\[\[|\]\]$/g,'').trim())),good=names.filter(s=>bySlug[s]).slice(0,5);
  r.rec.bad=names.filter(s=>!bySlug[s]);
  if(!good.length){ask.stage='err';ask.err={raw:r.raw,retry:'ask1',why:'it named no page that exists in the index'};ask.prog='';return renderAsk();}
  ask.chosen=good;ask.stage='chosen';ask.prog='Step 1 done · '+good.length+' pages chosen'+(r.rec.bad.length?' · '+r.rec.bad.length+' unknown slug(s) dropped':'')+'.';renderAsk();
}
async function askStep2(){
  const sent=ask.chosen.map(s=>bySlug[s]).filter(Boolean),ch=sum(sent,p=>p.body.length);
  const run={stop:false};ask.run=run;ask.stage='s2';ask.err=null;ask.changing=false;
  ask.prog='Step 2 of 2 · sending '+sent.length+' pages, '+nf(ch)+' characters; 0 library passages have left the browser.';setRunning(2,true);renderAsk();
  const prompt='You answer one question from a research wiki on neurotechnology in the administration of justice, using ONLY the wiki pages below.\n'+PINRULE+' Copy pins exactly as they stand on the pages; do not write a pin that is not on them.\n'+REGRULE+'\nAnswer in at most 350 words of markdown; you may link pages as [[slug]]. If the pages cannot answer part of the question, say so in cannot_answer instead of guessing.\nReturn JSON {"title": "a short title for the question", "answer": "...", "cannot_answer": "..."}.\n\nQUESTION\n'+ask.q+'\n\n'+sent.map(p=>'=== PAGE '+p.slug+' ('+(p.frontmatter.register||[]).join('')+') ===\n'+p.body).join('\n\n');
  const r=await callModel(prompt,0,'ask, step 2');
  if(run.stop)return;
  ask.run=null;setRunning(2,false);
  if(!r.ok||typeof r.data.answer!=='string'||!r.data.answer.trim()){ask.stage='chosen';ask.err={raw:r.raw||r.error,retry:'ask2',why:r.ok?'it returned no answer text':''};ask.prog='';return renderAsk();}
  const allowed=new Set();sent.forEach(p=>parsePins(p.body).forEach(x=>allowed.add(pinKey(x))));
  ask.answer={title:String(r.data.title||'').trim(),answer:r.data.answer,cannot:String(r.data.cannot_answer||'').trim(),allowed};
  r.rec.bad=uniq([...r.data.answer.matchAll(/\[\[([^\]|#]+)/g)].map(m=>m[1].trim())).filter(s=>!bySlug[s]);
  ask.stage='done';ask.fTitle='';ask.fTags='';ask.prog='Done. '+parsePins(r.data.answer).length+' pins in the answer, each checked by this page.';renderAsk();
}
function addIndexLine(section,line){
  const L=index.split('\n'),re=new RegExp(rx(section),'i');
  const h=L.findIndex(l=>/^#{1,4}\s/.test(l)&&re.test(l));
  if(h<0){L.push('','## '+section,line);}
  else{let j=h+1,last=h;while(j<L.length&&!/^#{1,4}\s/.test(L[j])){if(L[j].trim())last=j;j++;}L.splice(last+1,0,line);}
  index=L.join('\n');
}
function setIndexLine(slug,line){const re=new RegExp('^\\s*[-*]\\s*\\[\\['+rx(slug)+'\\]\\]');index=index.split('\n').map(l=>re.test(l)?line:l).join('\n');}
function setIndexN(slug,n){const re=new RegExp('^\\s*[-*]\\s*\\[\\['+rx(slug)+'\\]\\]');index=index.split('\n').map(l=>re.test(l)?l.replace(/✓\s*\d+/,'✓'+n):l).join('\n');}
function fixIndexHead(){
  const L=index.split('\n'),n=sum(pages,p=>p._pins.length);
  for(let i=0;i<Math.min(L.length,8);i++)if(/(\d[\d,]*) pins/.test(L[i])){L[i]=L[i].replace(/(\d[\d,]*) pins/,nf(n)+' pins').replace(/(\d+) pages/,pages.length+' pages');break;}
  index=L.join('\n');
}
function fileQuestion(){
  const q=buildQ();if(!q.fileable)return;
  const t=today(),before=needLook();
  pages.push(q.page);rebuild();
  const p=bySlug[q.slug],n=vcount(p);
  addIndexLine('Questions','- [['+q.slug+']] — '+(plain(q.first).slice(0,140)||q.title)+' · ('+q.reg.join('')+') · ✓'+n);fixIndexHead();
  const head='## ['+t+'] ask | '+q.title;
  log=log.replace(/\s+$/,'')+'\n\n'+head+'\n\nQuestion: "'+ask.q.replace(/"/g,'”')+'". Filed as [['+q.slug+']] from '+ask.chosen.length+' pages ('+ask.chosen.map(s=>'[['+s+']]').join(', ')+'). '+n+' pins, all verified.\n';
  S.logAdded.add(head);S.changes.push({date:t,kind:'ask',slug:q.slug,how:'new page'});S.approved.add(q.slug);S.filings++;
  lintRan=true;lastFiling={before,after:needLook(),slugs:[q.slug]};
  ask.filed=q.slug;ask.file=null;renderAll();
}

/* ---------- tab 03: ingest ---------- */
const inboxDocs=()=>Object.values(docs).filter(d=>d.status==='inbox');
function openIngest(id){
  const d=docs[id],ps=d.passages||[],B=[];
  for(let i=0;i<ps.length;i+=25){const ch=ps.slice(i,i+25),nums=ch.map(p=>p.paragraph).filter(Boolean),pg=ch.map(p=>p.page),lo=Math.min(...pg),hi=Math.max(...pg);
    B.push({n:B.length+1,passages:ch,para:nums.length?nums[0]+(nums.length>1?' – '+nums[nums.length-1]:''):'none numbered',pp:lo+(hi>lo?' – '+hi:''),chars:sum(ch,p=>p.text.length),state:'todo'});}
  ing={doc:d,stage:1,batches:B,next:0,sent:0,tk:[],tkRet:0,dropped:0,run:null,prog:'',err:null,src:null,srcSlug:'',touchesRaw:[],touched:null,drafted:0,cards:[],i:0,dec:{},newOK:new Set(),filed:null,c0:S.calls,p0:S.passages,skipped:[]};
  renderIngest();
}
function takePrompt(g,b){
  const d=g.doc;
  return 'You are reading a document that is waiting to be added to a research wiki on neurotechnology in the administration of justice.\nDOCUMENT: '+d.title+' ('+citeAs(d)+', '+d.year+'), register '+regTxt(d.id)+'.\nBelow are (1) the wiki’s index and (2) a batch of passages from the document as JSON {id, page, paragraph, text}.\nReturn JSON {"takeaways":[{"claim":"...","quote":"...","passage":"<passage id>","pages":["slug"]}]}.\n- At most 10 takeaways; keep only claims that bear on the administration of justice (evidence, torture and ill-treatment, fair trial, self-incrimination, recommendations); skip the rest.\n- claim: one sentence saying what the document says, with its own verb; do not turn a report’s statement into law.\n- quote: 8 to 40 words copied verbatim from that one passage. Quote only words that stand in the passages given; the code will check every quotation.\n- passage: the id of the passage the quote comes from.\n- pages: slugs from the index that the claim bears on.\n\nINDEX\n'+index+'\n\nPASSAGES\n'+JSON.stringify(b.passages.map(p=>({id:p.id,page:p.page,paragraph:p.paragraph,text:p.text})));
}
function lcsRun(a,b){let best=0;const prev=new Array(b.length+1).fill(0);for(let i=1;i<=a.length;i++){let diag=0;for(let j=1;j<=b.length;j++){const t=prev[j];prev[j]=a[i-1]===b[j-1]?diag+1:0;if(prev[j]>best)best=prev[j];diag=t;}}return best;}
function nearest(doc,ps,quote){
  const qw=norm(quote).toLowerCase().split(' ');let best=null;
  doc.passages.filter(x=>x.page===ps.page).forEach(x=>{const r=lcsRun(qw,norm(x.text).toLowerCase().split(' '));if(!best||r>best.run)best={p:x,run:r};});
  return best||{p:ps,run:0};
}
function procBatch(g,b,data){
  const arr=Array.isArray(data.takeaways)?data.takeaways:[],rows=arr.slice(0,10);let ver=0,fail=0,drop=arr.length-rows.length;const bad=[];
  g.tkRet+=arr.length;
  rows.forEach(t=>{
    const claim=String(t&&t.claim||'').trim(),quote=String(t&&t.quote||'').replace(/\s+/g,' ').trim(),pid=String(t&&t.passage||'').trim(),tail=pid.replace(/^.*#/,'');
    const ps=b.passages.find(p=>p.id===pid)||(/^\d+$/.test(tail)?b.passages.find(p=>p.id===g.doc.id+'#'+tail):null);
    if(!ps||!claim||!quote){drop++;return;}
    const slugs=[];
    (Array.isArray(t.pages)?t.pages:[]).forEach(s=>{s=String(s).replace(/^\[\[|\]\]$/g,'').trim();
      if(bySlug[s])slugs.push(s);
      else if(/^[a-z0-9][a-z0-9-]*$/.test(s)&&(g.newOK.has(s)||g.newOK.size<2)){g.newOK.add(s);slugs.push(s);}
      else bad.push(s);});
    const e={claim,quote,ps,slugs:uniq(slugs),ok:inText(ps.text,quote),batch:b.n};
    if(e.ok){e.pin=mkPin(g.doc,ps,quote);if(!verify(parsePins(e.pin)[0],g.doc.id).ok)e.ok=false;}
    if(e.ok)ver++;else{e.near=nearest(g.doc,ps,quote);fail++;}
    g.tk.push(e);
  });
  g.dropped+=drop;
  return {returned:arr.length,ver,fail,drop,bad};
}
async function runBatches(){
  const g=ing;g.stage=2;g.err=null;const run={stop:false};g.run=run;setRunning(3,true);renderIngest();
  while(g.next<g.batches.length&&!run.stop){
    const b=g.batches[g.next];b.state='running';
    g.prog='batch '+b.n+' of '+g.batches.length+' · '+(g.sent+b.passages.length)+' of '+g.doc.passages.length+' passages have left the browser';
    g.sent+=b.passages.length;renderIngest();
    const r=await callModel(takePrompt(g,b),b.passages.length,'takeaways, batch '+b.n+' of '+g.batches.length);
    if(run.stop)return;
    if(!r.ok){g.sent-=b.passages.length;b.state='failed';g.err={raw:r.raw||r.error,retry:'batch'};break;}
    Object.assign(r.rec,procBatch(g,b,r.data));b.state='done';g.next++;
  }
  g.run=null;setRunning(3,false);
  g.prog=g.err?'':(g.next>=g.batches.length?'All '+g.batches.length+' batches have returned.':'');
  renderIngest();
}
function stopIngest(){
  const g=ing;if(!g||!g.run)return;g.run.stop=true;g.run=null;setRunning(3,false);
  if(g.stage===2){const b=g.batches[g.next];if(b&&b.state==='running'){b.state='todo';g.sent-=b.passages.length;}}
  g.prog='Stopped. What has returned is kept.';renderIngest();
}
function stopAsk(){
  if(!ask.run)return;ask.run.stop=true;ask.run=null;setRunning(2,false);
  ask.stage=ask.chosen.length&&ask.stage==='s2'?'chosen':ask.stage==='s1'?'idle':ask.stage;ask.prog='Stopped.';renderAsk();
}
function blocks(t){return String(t).split(/\n\s*\n/).filter(s=>s.trim()).length;}
function insertAfter(body,after,text){
  const blk=['','<<ins>>',text,'<<end>>',''],want=String(after).replace(/^#+\s*/,'').trim().toLowerCase();
  const atEnd=note=>({body:body.replace(/\s+$/,'')+'\n'+blk.join('\n'),note});
  if(!want||want==='end')return atEnd('');
  const L=body.split('\n');let h=-1,lvl=0;
  for(let pass=0;pass<2&&h<0;pass++)for(let i=0;i<L.length;i++){const m=L[i].match(/^(#{1,4})\s+(.*)$/);if(m&&(pass?m[2].toLowerCase().includes(want):m[2].trim().toLowerCase()===want)){h=i;lvl=m[1].length;break;}}
  if(h<0)return atEnd('Heading "'+after+'" was not found: the text is placed at the end of the page.');
  let j=h+1;while(j<L.length){const m=L[j].match(/^(#{1,4})\s/);if(m&&m[1].length<=lvl)break;j++;}
  L.splice(j,0,...blk);return {body:L.join('\n'),note:''};
}
function cleanCon(raw,id){
  if(!raw||typeof raw!=='string')return null;
  let s=raw.trim();const m=s.match(new RegExp(FENCE+'(?:contested)?[ \\t]*\\n([\\s\\S]*?)\\n?'+FENCE));if(m)s=m[1];s=s.trim();
  if(!/^claim:/m.test(s)||!/^verdict:/m.test(s)||!/^[+\-~]\s/m.test(s))return null;
  return fixPins(s,id);
}
function srcPrompt(g,vt){
  const d=g.doc;
  return 'You write the source page for a document being added to a research wiki on neurotechnology in the administration of justice.\nDOCUMENT: '+d.title+'; author: '+d.author+'; published: '+d.published+'; '+d.pages+' PDF pages; url: '+d.url+'; cite as: '+citeAs(d)+'; register '+regTxt(d.id)+'.\n'+PINRULE+' Use only the pins listed below, copied exactly.\n'+REGRULE+'\nPage anatomy, as ## headings in this order: Full cite, Register, One-liner, Key takeaways, How NOT to read this, Where it feeds the wiki, Related. Link wiki pages as [[slug]].\nReturn JSON {"one_liner":"...","body":"markdown, at most 900 words","touches":[{"slug":"...","why":"..."}]}.\n\nVERIFIED TAKEAWAYS\n'+vt.map((t,i)=>(i+1)+'. '+t.claim+'\n   pin: '+t.pin+'\n   pages: '+t.slugs.join(', ')).join('\n')+'\n\nINDEX\n'+index;
}
async function draftSource(){
  const g=ing,vt=g.tk.filter(t=>t.ok),d=g.doc;g.err=null;const run={stop:false};g.run=run;g.prog='Drafting the source page (1 call)…';setRunning(3,true);renderIngest();
  const r=await callModel(srcPrompt(g,vt),0,'source page');
  if(run.stop)return;
  g.run=null;setRunning(3,false);
  if(!r.ok||typeof r.data.body!=='string'){g.err={raw:r.raw||r.error,retry:'src',why:r.ok?'it returned no page body':''};g.prog='';return renderIngest();}
  const f=fixPins(r.data.body,d.id),base=slugify(d.symbol||d.short_title||d.id)||'source';let slug=base;if(bySlug[slug])slug=base+'-source';let n=2;while(bySlug[slug])slug=base+'-source-'+n++;
  g.srcSlug=slug;g.touchesRaw=Array.isArray(r.data.touches)?r.data.touches.slice(0,12):[];
  const links=uniq([...f.text.matchAll(/\[\[([^\]|#]+)/g)].map(m=>m[1].trim())).filter(s=>bySlug[s]);
  const title=(d.short_title||d.title)+' ('+citeAs(d)+')',one=String(r.data.one_liner||'').trim();
  const fm={title,type:'source',tags:uniq(g.touchesRaw.map(x=>String(x&&x.slug||'')).filter(s=>bySlug[s])).slice(0,8),register:docReg(d.id).slice(),status:'draft',updated:today(),links,sources:[d.id]};
  const bodyTxt=/^#\s/.test(f.text.trim())?f.text.trim():'# '+title+'\n\n'+f.text.trim();
  g.src={slug,title,type:'source',kind:'new',role:'source',stub:false,after:'<<ins>>\n'+bodyTxt+'\n<<end>>\n',paras:blocks(bodyTxt),ok:f.ok,removed:f.removed,notes:[],oneLiner:one,con:null,fm};
  g.cards=[g.src];g.touched=planTouched(g);g.drafted=0;g.prog='';renderIngest();
}
function planTouched(g){
  const vt=g.tk.filter(t=>t.ok),map={};
  vt.forEach(t=>t.slugs.forEach(s=>{(map[s]=map[s]||[]).push(t);}));
  g.touchesRaw.forEach(x=>{const s=String(x&&x.slug||'').trim();if(!s||s===g.srcSlug)return;
    if(bySlug[s]||g.newOK.has(s)){map[s]=map[s]||[];}
    else if(/^[a-z0-9][a-z0-9-]*$/.test(s)&&g.newOK.size<2){g.newOK.add(s);map[s]=[];}});
  const stub=pages.find(p=>p.frontmatter.status==='stub'&&(p.slug===slugify(g.doc.symbol||g.doc.id)||(p.frontmatter.sources||[]).includes(g.doc.id)))||pages.find(p=>p.frontmatter.status==='stub');
  const sl=stub?stub.slug:null;
  const rest=Object.keys(map).filter(s=>s!==sl).sort((a,b)=>map[b].length-map[a].length).slice(0,sl?11:12);
  return (sl?[sl]:[]).concat(rest).map(s=>({slug:s,isNew:!bySlug[s],stub:s===sl,mode:(!bySlug[s]||s===sl)?'body':'edits',tks:s===sl?vt:map[s]}));
}
function touchPrompt(g,t){
  const d=g.doc,p=bySlug[t.slug],tl=t.tks.map((x,i)=>(i+1)+'. '+x.claim+'\n   pin: '+x.pin).join('\n')||'(none: use the document’s title and register only)';
  let h='You are updating a research wiki on neurotechnology in the administration of justice after reading a new document: '+d.title+' ('+citeAs(d)+', '+d.year+', register '+regTxt(d.id)+').\n'+PINRULE+' Use only the pins listed below, copied exactly.\n'+REGRULE+'\n\n';
  if(t.mode==='edits')h+='PAGE '+t.slug+' (current body)\n'+p.body+'\n\nNEW TAKEAWAYS BEARING ON THIS PAGE\n'+tl+'\n\nReturn JSON {"edits":[{"after":"<an existing heading of this page, or end>","markdown":"..."}],"contested":null}. At most 300 words in all. "contested" is a full block (lines claim:, verdict:, note:, then one line per position: + or - or ~, a register letter, a pin, a gloss and a [[slug]], separated by " | ") only where this document disagrees with the page; otherwise null.';
  else if(t.stub)h+='STUB PAGE '+t.slug+' (current body, with the checklist of what the ingest should check)\n'+p.body+'\n\nTAKEAWAYS FROM THE DOCUMENT\n'+tl+'\n\nRewrite this page as a proper entity page for the document: answer each checklist item the document addresses, say plainly which items it does not address, keep every existing pin that still applies (copied exactly) and use the pins above. Return JSON {"one_liner":"...","body":"markdown starting with # title, at most 600 words"}.';
  else h+='NEW PAGE '+t.slug+'\n\nTAKEAWAYS\n'+tl+'\n\nWrite a new wiki page with this slug. Return JSON {"title":"...","type":"concept or entity","one_liner":"...","body":"markdown starting with # title, at most 400 words"}.';
  return h;
}
function buildCard(g,t,data){
  const p=bySlug[t.slug],id=g.doc.id,notes=[];let ok=0,removed=0,paras=0,after,con=null;
  const one=String(data.one_liner||'').trim();
  if(t.mode==='edits'){
    after=p.body;let words=0;
    (Array.isArray(data.edits)?data.edits:[]).forEach(e=>{
      const m0=String(e&&e.markdown||'').trim();if(!m0)return;
      words+=m0.split(/\s+/).length;if(words>400){notes.push('An edit beyond the word limit was dropped.');return;}
      const f=fixPins(m0,id);ok+=f.ok;removed+=f.removed;paras+=blocks(f.text);
      const r=insertAfter(after,String(e.after||'end'),f.text);after=r.body;if(r.note)notes.push(r.note);});
    const c=cleanCon(data.contested,id);
    if(c){ok+=c.ok;removed+=c.removed;con=c.text;paras+=1;
      const blockTxt=FENCE+'contested\n'+c.text+'\n'+FENCE;
      after=after.replace(/\s+$/,'')+'\n\n<<ins>>\n'+(/^#{1,4}\s.*contested/im.test(after)?'':'## Contested claims\n\n')+blockTxt+'\n<<end>>\n';}
    if(!paras)return null;
    return {slug:t.slug,title:p.title,type:p.type,kind:'edited',stub:false,after,paras,ok,removed,notes,oneLiner:one,con};
  }
  const f=fixPins(String(data.body||''),id);ok=f.ok;removed=f.removed;
  if(!f.text.trim())return null;
  const title=p?p.title:String(data.title||'').trim()||humanise(t.slug),type=p?p.type:(data.type==='entity'?'entity':'concept');
  const bt=/^#\s/.test(f.text.trim())?f.text.trim():'# '+title+'\n\n'+f.text.trim();
  const fm=p?null:{title,type,tags:[],register:docReg(id).slice(),status:'draft',updated:today(),links:[],sources:[id]};
  return {slug:t.slug,title,type,kind:p?'edited':'new',stub:!!t.stub,after:'<<ins>>\n'+bt+'\n<<end>>\n',paras:blocks(bt),ok,removed,notes,oneLiner:one,con:null,fm};
}
async function draftPages(){
  const g=ing;g.err=null;const run={stop:false};g.run=run;setRunning(3,true);
  for(let k=g.drafted;k<g.touched.length&&!run.stop;k++){
    const t=g.touched[k];g.prog='page '+(k+1)+' of '+g.touched.length+': '+t.slug;renderIngest();
    const r=await callModel(touchPrompt(g,t),0,'page '+(k+1)+' of '+g.touched.length+' ('+t.slug+')');
    if(run.stop)return;
    if(!r.ok){g.err={raw:r.raw||r.error,retry:'pages'};break;}
    const c=buildCard(g,t,r.data);if(c)g.cards.push(c);else g.skipped.push(t.slug);
    g.drafted=k+1;
  }
  g.run=null;setRunning(3,false);g.prog=g.err?'':(g.drafted>=g.touched.length?'All page drafts have returned.':'');renderIngest();
}
function decide(v){const g=ing,c=g.cards[g.i];if(!c)return;g.dec[c.slug]=v;g.i++;renderIngest();}
function secOf(t){return SEC[t]||'Other';}
function fileIngest(){
  const g=ing,d=g.doc,t=today(),before=needLook();
  const ap=g.cards.filter(c=>g.dec[c.slug]==='approve'),rj=g.cards.filter(c=>g.dec[c.slug]==='reject');
  if(!ap.length)return;
  const cite=citeAs(d),srcCard=ap.find(c=>c.role==='source');
  d.status='ingested';
  ap.forEach(c=>{
    const cl=cleanMk(c.after);let p=bySlug[c.slug];
    if(p){p.body=cl;if(c.stub)p.frontmatter.status='draft';}
    else{p={slug:c.slug,type:c.type,title:c.title,frontmatter:c.fm,body:cl};pages.push(p);bySlug[p.slug]=p;}
  });
  rebuild();
  ap.forEach(c=>{
    const p=bySlug[c.slug],fm=p.frontmatter,ids=uniq(p._pins.map(x=>x.id));
    fm.updated=t;fm.sources=uniq((fm.sources||[]).filter(s=>ids.includes(s)).concat(ids));
    fm.links=uniq((fm.links||[]).concat(p._links.filter(s=>bySlug[s]&&s!==p.slug)));
    if(srcCard)fm.links=uniq(fm.links.concat(c.role==='source'?ap.filter(x=>x!==c).map(x=>x.slug):[srcCard.slug]));
  });
  rebuild();
  ap.forEach(c=>{
    const p=bySlug[c.slug],n=vcount(p),line='- [['+p.slug+']] — '+(c.oneLiner||p.title)+' · ('+(p.frontmatter.register||[]).join('')+') · ✓'+n;
    if(c.kind==='new')addIndexLine(secOf(p.type),line);else if(c.stub)setIndexLine(p.slug,line);else setIndexN(p.slug,n);
  });
  fixIndexHead();
  const pinsAll=sum(pages,p=>p._pins.filter(x=>x.id===d.id).length),srcSlug=srcCard?srcCard.slug:'';
  const others=pages.filter(p=>p.slug!==srcSlug&&p._pins.some(x=>x.id===d.id)).map(p=>'[['+p.slug+']]');
  const head='## ['+t+'] ingest | '+(d.symbol?d.symbol+': ':'')+d.short_title;
  const bodyTxt='Read '+g.sent+' passages ('+cite+', register '+regTxt(d.id)+'). Wrote '+(srcCard?'[['+srcCard.slug+']]':'no source page')+'. '+pinsAll+' pins in all; besides its own page, pinned on '+others.length+' pages: '+(others.join(', ')||'none')+'. Rejected: '+(rj.map(c=>'[['+c.slug+']]').join(', ')||'none')+'.';
  log=log.replace(/\s+$/,'')+'\n\n'+head+'\n\n'+bodyTxt+'\n';S.logAdded.add(head);
  ap.forEach(c=>{
    if(!c.con)return;
    const cc=parseCon(c.con),slug=slugify(cc.claim).slice(0,60)||c.slug+'-claim',st=/^leans-/.test(cc.verdict)?'leaning':/^settled-/.test(cc.verdict)?'settled':'open';
    const gl=sg=>cc.pos.filter(x=>x.sign===sg).map(x=>x.gloss.trim()).join('; ')||'none';
    tensions=tensions.replace(/\s+$/,'')+'\n\n### '+slug+'\n\n- title: '+cc.claim+'\n- status: '+st+'\n- card: [['+c.slug+']]\n- poles: '+gl('+')+' — against: '+gl('-')+'\n- where: '+cc.pos.map(x=>(x.pin.match(/^\[([^\]]+)\]/)||[])[1]||'').filter(Boolean).join('; ')+'\n';
    S.tensAdded.add('### '+slug);
  });
  ap.forEach(c=>{S.changes.push({date:t,kind:'ingest',slug:c.slug,how:c.kind==='new'?'new page':'edited'});S.approved.add(c.slug);});
  S.filings++;lintRan=true;
  const after=needLook();lastFiling={before,after,slugs:ap.map(c=>c.slug)};
  g.filed={ap:ap.length,rj:rj.length,before,after,head,bodyTxt};
  renderAll();
}
function renderIngest(){
  const el=$('#ingOut'),g=ing;let h='';
  const inboxList=()=>{const ds=inboxDocs();return ds.length?ds.map(d=>'<div class="inb"><div><b>'+esc(d.short_title||d.title)+'</b><div class="hint">'+esc(d.symbol||d.author||'')+' · '+esc(d.kind)+' · '+esc(d.year)+' · '+(d.passages||[]).length+' passages · '+esc(d.pages)+' PDF pages · status: inbox</div></div><button type="button" class="btn pri" data-act="ing-open" data-id="'+esc(d.id)+'">Ingest '+esc(d.symbol||d.short_title)+'</button></div>').join(''):'<p>Nothing waits in the inbox.</p>';};
  if(!g){el.innerHTML='<div class="grey">Pressing the button opens a four-step plan. Nothing leaves the browser until you press Start, and every step says what it sends.</div>'+inboxList();return;}
  const steps=['01 SCOPE','02 TAKEAWAYS','03 DRAFTS','04 REVIEW AND FILE'];
  h+='<ol class="steps" aria-label="Steps">'+steps.map((s,i)=>'<li'+(g.stage===i+1?' class="on" aria-current="step"':'')+'>'+s+'</li>').join('')+'</ol>';
  h+='<div class="nums"><div><span class="big">'+(S.calls-g.c0)+'</span><div class="hint">calls so far</div></div><div><span class="big">'+(S.passages-g.p0)+'</span><div class="hint">passages sent</div></div></div><div class="hint" aria-live="polite">calls so far '+(S.calls-g.c0)+' · passages sent '+(S.passages-g.p0)+(g.prog?' · '+esc(g.prog):'')+'</div>';
  if(g.run)h+='<div class="row2"><button type="button" class="btn" data-act="ing-stop">Stop</button><span class="hint">Escape also stops. What has returned is kept.</span></div>';
  if(g.err)h+=errHtml(g.err,'ing-retry');
  const vt=g.tk.filter(t=>t.ok),n=g.doc.passages.length;
  if(g.stage===1){
    h+='<h3 class="s">Scope: the whole document</h3><p>All '+n+' passages will be sent, in batches of 25 ('+g.batches.length+' calls), '+nf(sum(g.batches,b=>b.chars))+' characters; nothing is held back.</p>'
     +'<table><caption>Batches</caption><thead><tr><th scope="col">Batch</th><th scope="col">Paragraphs</th><th scope="col">PDF pages</th><th scope="col" class="n">Passages</th><th scope="col" class="n">Characters</th></tr></thead><tbody>'+g.batches.map(b=>'<tr><td>'+b.n+'</td><td>'+esc(b.para)+'</td><td>'+esc(b.pp)+'</td><td class="n">'+b.passages.length+'</td><td class="n">'+nf(b.chars)+'</td></tr>').join('')+'</tbody></table>'
     +'<p><button type="button" class="btn pri" data-act="ing-start">Start</button> <span class="hint">sends '+g.batches.length+' calls, one after another, with the wiki’s index in each</span></p>';
  }else if(g.stage===2){
    h+='<h3 class="s">Takeaways</h3><table><caption>FIG.02 Takeaways from '+esc(g.doc.symbol||g.doc.short_title)+': '+vt.length+' verified of '+g.tk.length+'</caption><thead><tr><th scope="col">Claim</th><th scope="col">Quote</th><th scope="col">Passage</th><th scope="col">Pages it would touch</th><th scope="col">Verification</th></tr></thead><tbody>'
     +(g.tk.length?g.tk.map(t=>'<tr><td data-source="ai">'+esc(t.claim)+'</td><td data-source="ai">“'+esc(t.quote)+'”</td><td>'+(t.ps.paragraph?'para. '+esc(t.ps.paragraph)+' · ':'')+'PDF p. '+t.ps.page+'</td><td data-source="ai">'+(t.slugs.map(s=>'<span class="chip">'+esc(s)+(bySlug[s]?'':' (new)')+'</span>').join(' ')||'—')+'</td><td>'+(t.ok?'<span class="st ok">verified</span>':'<span class="st no">not verified</span>')+'</td></tr>').join(''):'<tr><td colspan="5" class="hint">No takeaway yet.</td></tr>')+'</tbody></table>'
     +'<p class="hint">How this is computed: each quote must stand in the passage the model named; the code builds the pin and runs the same check as everywhere else. '+g.dropped+' takeaways were dropped (no passage sent, or over 10 in a batch).</p>';
    const fl=g.tk.map((t,i)=>({t,i})).filter(x=>!x.t.ok);
    h+='<details'+(fl.length?' open':'')+'><summary><b>Could not verify: '+fl.length+'</b></summary>'+(fl.length?fl.map(({t,i})=>'<div class="err"><p data-source="ai"><b>'+esc(t.claim)+'</b><br>Model’s quote: “'+esc(t.quote)+'”</p><p class="hint">Passage named: '+(t.ps.paragraph?'para. '+esc(t.ps.paragraph)+', ':'')+'PDF p. '+t.ps.page+' · nearest passage on that page: '+(t.near.p.paragraph?'para. '+esc(t.near.p.paragraph):'p. '+esc(t.near.p.page_label))+', sharing a run of '+t.near.run+' words</p><button type="button" class="btn" data-act="ing-open-tk" data-i="'+i+'" aria-label="Open '+esc(g.doc.symbol||g.doc.short_title)+' at PDF page '+t.ps.page+'">Open the PDF page</button></div>').join(''):'<p class="hint">None so far. These claims would be in no change card and in no later prompt.</p>')+'</details>';
    if(!g.run){
      const left=g.batches.length-g.next;
      h+='<div class="row2">'+(left?'<button type="button" class="btn'+(vt.length?'':' pri')+'" data-act="ing-start">Run the remaining '+left+' batches</button>':'')+(vt.length?'<button type="button" class="btn pri" data-act="ing-go3">Go to the drafts</button>':'<span class="hint">No verified takeaway yet, so there is nothing to draft.</span>')+'</div>';
    }
  }else if(g.stage===3){
    h+='<h3 class="s">Drafts</h3>';
    if(!g.src){
      const ch=sum(vt,t=>t.claim.length+t.pin.length)+index.length;
      h+='<div class="grey">Sends '+vt.length+' verified takeaways (claims and pins, no passages) and the index: about '+nf(ch)+' characters, 1 call.</div>'+(g.run?'':'<button type="button" class="btn pri" data-act="ing-src">Draft the source page (1 call)</button>');
    }else{
      const c=g.src;
      h+='<p>Source page drafted: <b data-source="ai">'+esc(c.title)+'</b> <span class="hint">('+esc(c.slug)+') · '+c.paras+' paragraphs · pins: '+c.ok+' verified, '+c.removed+' removed because they did not verify</span></p><p data-source="ai">'+esc(c.oneLiner)+'</p>';
      if(g.drafted<g.touched.length&&!g.run){
        const left=g.touched.length-g.drafted;
        h+='<div class="grey">Pages to touch ('+g.touched.length+'): '+g.touched.map(t=>esc(t.slug)+(t.isNew?' (new)':'')+(t.stub?' (stub, rewritten)':'')).join(', ')+'. Each call sends the page’s body and the takeaways that bear on it; no passages.</div><button type="button" class="btn pri" data-act="ing-pages">'+(g.drafted?'Draft the remaining '+left+' pages':'Draft the changes to '+g.touched.length+' pages ('+g.touched.length+' calls)')+'</button>';
      }
      if(g.drafted>0&&!g.run)h+=' <button type="button" class="btn'+(g.drafted>=g.touched.length?' pri':'')+'" data-act="ing-review">Review the changes ('+g.cards.length+' pages)</button>';
      if(g.skipped.length)h+='<p class="hint">No change proposed for: '+esc(g.skipped.join(', '))+'.</p>';
    }
  }else{
    const c=g.cards[g.i],tot=g.cards.length;
    h+='<h3 class="s">Review and file</h3>';
    if(g.filed){
      h+='<div role="status"><p><b>Filed.</b> '+g.filed.ap+' pages written, '+g.filed.rj+' rejected. The index, the log and the tensions register were updated.</p><div class="nums"><div><span class="big">'+g.filed.before+'</span><div class="hint">lint checks needing a look, before</div></div><div><span class="big">'+g.filed.after+'</span><div class="hint">after (tab 04 shows which)</div></div></div><p class="hint">Log entry: '+esc(g.filed.head)+'</p></div>';
    }else if(c){
      h+='<fieldset class="chg"><legend>Change '+(g.i+1)+' of '+tot+' · '+esc(c.title)+' · '+esc(c.type)+'</legend><p class="mono">'+(c.kind==='new'?'new page':'edited')+' · '+c.paras+' paragraphs inserted · pins added: '+c.ok+' verified, '+c.removed+' removed because they did not verify</p>'
       +(c.notes.length?'<p class="hint">'+c.notes.map(esc).join(' ')+'</p>':'')+'<div class="prev dim">'+md(c.after,{allow:g.doc.id,slug:c.slug})+'</div>'
       +'<div class="row2"><button type="button" class="btn pri" data-act="ing-approve" aria-label="Approve change '+(g.i+1)+' of '+tot+': '+esc(c.title)+'">Approve this page</button><button type="button" class="btn" data-act="ing-reject" aria-label="Reject change '+(g.i+1)+' of '+tot+': '+esc(c.title)+'">Reject this page</button><span class="hint">change '+(g.i+1)+' of '+tot+' · nothing is written until you file</span></div></fieldset>';
    }else{
      const ap=g.cards.filter(x=>g.dec[x.slug]==='approve').length;
      h+='<p>'+tot+' decisions made: '+ap+' approved, '+(tot-ap)+' rejected. A rejected page stays exactly as loaded.</p><button type="button" class="btn pri" data-act="ing-file"'+(ap?'':' disabled')+'>File the approved changes</button>'+(ap?'':' <span class="hint">Disabled: no page was approved.</span>');
    }
  }
  if(g.filed)h+=inboxList();
  el.innerHTML=h;
}

/* ---------- tabs 04 and 05 ---------- */
function renderCheck(){
  const C=lintAll(),pins=sum(pages,p=>p._pins.length),ver=sum(pages,vcount),need=C.filter(c=>c.items.length).length;
  let h='<div><span class="big" aria-live="polite">'+nf(ver)+'</span> <span>of '+nf(pins)+' pins verified by this page</span></div><p><b>'+need+' lint checks need a look.</b> <span class="hint">How this is computed: a pin verifies when its quote stands in a passage of that document starting on that PDF page and the label names the paragraph or page label.</span></p>';
  h+='<table><caption>FIG.03 Lint checks on the wiki</caption><thead><tr><th scope="col">Check</th><th scope="col" class="n">Result</th><th scope="col">Pages concerned</th></tr></thead><tbody>'
   +C.map(c=>'<tr><td>'+esc(c.name)+'</td><td class="n"><span class="st '+(c.items.length?'no':'ok')+'">'+c.items.length+' · '+(c.items.length?'check':'pass')+'</span></td><td>'+(c.items.length?slugLinks(c.items):'—')+'</td></tr>').join('')+'</tbody></table>';
  h+='<p><button type="button" class="btn pri" data-act="lint">'+(lintRan?'Re-run':'Lint now')+'</button> <span class="hint">Contradictions between pages (the schema’s reading lint) are not checked by this page’s code.</span></p>';
  const R=selfChecks(),groups=uniq(R.map(r=>r.g));
  h+='<details open><summary><b>How the app checks itself</b></summary>'+groups.map(g=>'<h4 class="lab" style="margin:12px 0 2px">'+esc(g)+'</h4><ul style="list-style:none;padding:0;margin:0">'+R.filter(r=>r.g===g).map(r=>'<li style="padding:3px 0;border-bottom:1px solid var(--rule)"><span class="st '+(r.ok===null?'na':r.ok?'ok':'no')+'">'+(r.ok===null?'n/a':r.ok?'pass':'check')+'</span> '+esc(r.t)+(r.items.length?' · '+slugLinks(r.items,8):'')+'</li>').join('')+'</ul>').join('')+'</details>';
  $('#chkOut').innerHTML=h;
}
function renderRecord(){
  const ents=logEntries();if(logNewest)ents.reverse();
  const te=tensEntries();
  let h='<div class="row2"><span class="lab">LOG</span><button type="button" class="btn" data-act="log-order" aria-pressed="'+logNewest+'">'+(logNewest?'Newest first':'Oldest first')+'</button><span class="hint">click = switch order</span></div>';
  h+=ents.map(e=>'<details><summary>'+esc(e.title)+(S.logAdded.has(e.head)?'<span class="tag">this session</span>':'')+'</summary><div class="body">'+md(e.body,{})+'</div></details>').join('')||'<p class="hint">The log is empty.</p>';
  h+='<h3 class="s">Where the sources disagree: the tensions register</h3>'+(te.intro.trim()?'<div class="body">'+md(te.intro,{})+'</div>':'')
   +te.items.map(x=>'<details id="tens-'+slugify(x.head)+'"><summary>'+esc(x.head)+(S.tensAdded.has('### '+x.head)?'<span class="tag">this session</span>':'')+'</summary><div class="body">'+md(x.body,{})+'</div></details>').join('');
  h+='<h3 class="s">Method</h3><p class="hint">Counting, matching and verification are done by this page’s code; each number has its “How this is computed” line. Source: '+esc(WK.source||'the attached wiki')+' · built '+esc(WK.built||'unknown')+' · library: '+esc((WD.library&&WD.library.source)||'the attached library')+'.</p>';
  h+='<div class="row2"><button type="button" class="btn pri" data-act="download">Download the wiki</button>'+(S.changes.length?'<button type="button" class="btn" data-act="download-md">Download the changed pages (markdown)</button>':'')+'<span id="dlMsg" class="hint" aria-live="polite"></span></div>';
  $('#recOut').innerHTML=h;
}
function download(name,text,type){
  try{const a=document.createElement('a');a.href=URL.createObjectURL(new Blob([text],{type}));a.download=name;document.body.appendChild(a);a.click();setTimeout(()=>{URL.revokeObjectURL(a.href);a.remove();},500);}
  catch(e){const m=$('#dlMsg');if(m)m.textContent='Download is not available here: '+e.message;}
}
function copyBtn(b,text){
  const old=b.textContent,done=ok=>{b.textContent=ok?'Copied':'Copy is not available here';setTimeout(()=>{b.textContent=old;},1600);};
  const fb=()=>{try{const a=document.createElement('textarea');a.value=text;a.style.cssText='position:fixed;opacity:0';document.body.appendChild(a);a.select();const ok=document.execCommand('copy');a.remove();return ok;}catch(e){return false;}};
  if(navigator.clipboard&&navigator.clipboard.writeText)navigator.clipboard.writeText(text).then(()=>done(true),()=>done(fb()));else done(fb());
}
function renderAll(){renderHead();renderList();renderPageView();renderAsk();renderIngest();renderCheck();renderRecord();}

/* ---------- events ---------- */
function openPin(i){const p=pinReg[i];if(!p)return;try{if(window.studio&&typeof studio.openSource==='function')studio.openSource(p.id,p.page,p.quote);}catch(e){}}
document.addEventListener('click',e=>{
  const b=e.target.closest('[data-act]');if(!b)return;const a=b.dataset.act;
  const F={
   'open-page':()=>{e.preventDefault();openPage(b.dataset.slug);},
   'open-tens':()=>{e.preventDefault();openTens(b.dataset.head);},
   'pin-open':()=>openPin(+b.dataset.pin),
   'pin-toggle':()=>{const d=b.parentElement.querySelector('.pd');d.hidden=!d.hidden;b.setAttribute('aria-expanded',String(!d.hidden));b.textContent=d.hidden?'▾':'▴';},
   'copy-page':()=>copyBtn(b,pageMarkdown(bySlug[curPage])),
   'ask':()=>ask.stage==='chosen'?askStep2():askStep1(),
   'ask-stop':stopAsk,
   'ask-retry1':askStep1,'ask-retry2':askStep2,
   'ask-change':()=>{ask.changing=!ask.changing;renderAsk();},
   'ask-file-open':()=>{ask.file=!ask.file;renderAsk();},
   'ask-file':fileQuestion,
   'ask-copy':()=>copyBtn(b,ask.answer.answer),
   'ing-open':()=>openIngest(b.dataset.id),
   'ing-start':runBatches,'ing-stop':stopIngest,
   'ing-go3':()=>{ing.stage=3;renderIngest();},
   'ing-src':draftSource,'ing-pages':draftPages,
   'ing-review':()=>{ing.stage=4;ing.i=0;renderIngest();},
   'ing-approve':()=>decide('approve'),'ing-reject':()=>decide('reject'),
   'ing-file':fileIngest,
   'ing-retry':()=>{const r=ing.err&&ing.err.retry;if(r==='batch')runBatches();else if(r==='src')draftSource();else draftPages();},
   'ing-open-tk':()=>{const t=ing.tk[+b.dataset.i];try{if(window.studio&&studio.openSource)studio.openSource(ing.doc.id,t.ps.page,t.near.p.text.split(' ').slice(0,12).join(' '));}catch(err){}},
   'lint':()=>{lintRan=true;renderCheck();},
   'log-order':()=>{logNewest=!logNewest;renderRecord();},
   'download':()=>download('wiki-'+today()+'.json',JSON.stringify({title:WK.title,source:WK.source,built:WK.built,count:pages.length,schema:WK.schema,pages:pages.map(p=>({slug:p.slug,type:p.type,title:p.title,frontmatter:p.frontmatter,body:p.body})),index,log,tensions,changes:S.changes,library_status:Object.fromEntries(Object.values(docs).map(d=>[d.id,d.status]))},null,1),'application/json'),
   'download-md':()=>download('changed-pages-'+today()+'.md',pages.filter(p=>S.approved.has(p.slug)).map(pageMarkdown).join('\n\n'),'text/markdown')
  };
  if(F[a])F[a]();
});
document.addEventListener('input',e=>{
  if(e.target.id==='flt')renderList();
  else if(e.target.id==='fT'||e.target.id==='fG'){ask.fTitle=$('#fT').value;ask.fTags=$('#fG').value;updFile();}
});
document.addEventListener('change',e=>{
  const s=e.target.dataset&&e.target.dataset.pick;if(!s)return;
  let c=ask.chosen.filter(x=>x!==s);if(e.target.checked)c.push(s);
  if(c.length>5){e.target.checked=false;return;}
  ask.chosen=c;ask.answer=null;ask.file=null;ask.err=null;ask.stage=c.length?'chosen':'idle';ask.prog=c.length?'Pages changed by you. Press the button to send them.':'';renderAsk();
});
document.addEventListener('keydown',e=>{
  if(e.key==='Escape'){if(ask.run)stopAsk();if(ing&&ing.run)stopIngest();}
  if(e.target.id==='askQ'&&e.key==='Enter'&&!e.shiftKey){e.preventDefault();if(!ask.run)(ask.stage==='chosen'?askStep2:askStep1)();}
});
window.addEventListener('hashchange',()=>{let s='';try{s=decodeURIComponent(location.hash.slice(1));}catch(e){}if(s!==curPage){curPage=bySlug[s]?s:'';showTab(0);renderList();renderPageView();}});

/* ---------- start ---------- */
(function init(){
  pages=(WK.pages||[]).map(p=>({slug:p.slug,type:p.type,title:p.title,frontmatter:JSON.parse(JSON.stringify(p.frontmatter||{})),body:p.body||''}));
  pages.forEach(p=>{orig[p.slug]=p.body;});
  LIBR.forEach(d=>{docs[d.id]=Object.assign({},d);});
  rebuild();loadedWarn=sum(pages,p=>p._pins.filter(x=>x.mark==='⚠').length);
  const tl=$('#tabs');
  tl.innerHTML=BASE.map((t,i)=>'<button type="button" class="tab" role="tab" id="t'+(i+1)+'" aria-controls="p'+(i+1)+'" data-tab="'+i+'">'+t+'<span class="run" aria-live="polite"></span></button>').join('');
  tl.querySelectorAll('.tab').forEach((b,i)=>{
    b.addEventListener('click',()=>showTab(i));
    b.addEventListener('keydown',e=>{const n=BASE.length;let k=null;if(e.key==='ArrowRight')k=(i+1)%n;else if(e.key==='ArrowLeft')k=(i+n-1)%n;else if(e.key==='Home')k=0;else if(e.key==='End')k=n-1;if(k!==null){e.preventDefault();showTab(k,true);}});
  });
  $('#foot').textContent=(WK.source||'')+' · built '+(WK.built||'unknown')+' · Counting, matching and verification are done by this page’s code; the model is called only when you press Ask, Ingest or a retry button.';
  if(!pages.length){$('#pview').innerHTML='<p>No wiki is attached to this conversation. Drag the wiki file from “Your files” into the chat.</p>';}
  try{const s=decodeURIComponent(location.hash.slice(1));if(bySlug[s])curPage=s;}catch(e){}
  renderAll();showTab(0,true);
})();
})();
</script>
</body>
</html>
```
