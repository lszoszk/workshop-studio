```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Research wiki: neurotechnology in the administration of justice</title>
<style>
:root{--paper:#f4f0e8;--ink:#1d1b18;--rule:#d9d2c3;--red:#9b2335;--green:#1e6b34;--amber:#8a5a00;--serif:Georgia,"Times New Roman",serif;--mono:ui-monospace,Menlo,Consolas,monospace;--sans:-apple-system,"Segoe UI",Roboto,sans-serif}
*{box-sizing:border-box}
[hidden]{display:none!important}
body{margin:0;background:var(--paper);color:var(--ink);font:16px/1.55 var(--sans)}
a{color:var(--red)}
a:focus,button:focus,input:focus,summary:focus{outline:2px solid var(--red);outline-offset:2px}
header{display:flex;justify-content:space-between;align-items:flex-end;gap:2rem;padding:1.1rem 1.4rem .9rem;border-bottom:1px solid var(--rule)}
.kicker{font:11px/1 var(--mono);letter-spacing:.14em;text-transform:uppercase;color:#6b6355}
h1{font:400 1.7rem/1.2 var(--serif);margin:.3rem 0 .25rem}
.dataline{font:12px/1.4 var(--mono);color:#6b6355}
.hdright{text-align:right;font:11px/1.5 var(--mono);color:#6b6355;max-width:24rem}
[role="tablist"]{display:flex;gap:0;flex-wrap:wrap;border-bottom:1px solid var(--rule);padding:0 1.4rem}
[role="tab"]{font:12px var(--mono);letter-spacing:.08em;background:none;border:none;border-bottom:3px solid transparent;padding:.7rem 1rem .55rem;color:var(--ink);cursor:pointer}
[role="tab"][aria-selected="true"]{color:var(--red);border-bottom-color:var(--red)}
[role="tab"] .run{color:var(--red)}
main{padding:1.3rem 1.4rem 3rem;max-width:1280px}
.panel{display:flex;gap:2rem;align-items:flex-start}
.rail{width:320px;flex:none;position:sticky;top:0}
.rail input{width:100%;padding:.45rem .5rem;font:14px var(--sans);border:1px solid var(--rule);background:#fbf8f2}
.bignum{font:400 3rem var(--serif);margin:.4rem 0 .1rem}
.hint{font:11px var(--mono);color:#6b6355;display:block;margin:.15rem 0 .5rem}
.grouplab{font:11px var(--mono);letter-spacing:.12em;text-transform:uppercase;color:#6b6355;margin:.9rem 0 .25rem;border-top:1px solid var(--rule);padding-top:.5rem}
.plist button{display:block;width:100%;text-align:left;background:none;border:none;border-left:3px solid transparent;padding:.35rem .5rem;cursor:pointer;font:14px var(--sans)}
.plist button:hover{background:#ece6d9}
.plist button.on{border-left-color:var(--red);background:#ece6d9}
.plist .meta{font:10px var(--mono);color:#6b6355}
.stubtag{color:var(--amber)}
.textcol{flex:1;max-width:900px;min-width:0}
.pagebody{font:16px/1.6 var(--sans)}
.pagebody h2,.pagebody h3,.pagebody h4{font:400 1.25rem/1.3 var(--serif);margin:1.4rem 0 .4rem}
.pagebody h3{font-size:1.1rem}.pagebody h4{font-size:1rem}
.badges{font:11px var(--mono);letter-spacing:.06em;color:#6b6355;margin:.3rem 0 .9rem}
.badges b{font-weight:400;color:var(--ink);border:1px solid var(--rule);padding:.1rem .4rem;margin-right:.3rem}
blockquote.cite,.pinwrap{margin:0}
.pinquote{font-style:italic}
.pinchip{display:inline-flex;flex-wrap:wrap;gap:.35rem;align-items:baseline;border:1px solid var(--rule);background:#fbf8f2;padding:.05rem .45rem;margin:0 .15rem;font:11px var(--mono);vertical-align:baseline}
.pinchip .lbl{background:none;border:none;color:var(--red);cursor:pointer;font:11px var(--mono);padding:0}
.pinchip .lbl:hover{text-decoration:underline}
.pinchip .ok{color:var(--green)}.pinchip .bad{color:var(--amber)}
.pindetail{display:block;font:12px var(--sans);color:#4c463d;margin:.2rem 0 .6rem .2rem;border-left:3px solid var(--rule);padding-left:.6rem}
.pindetail button{font:11px var(--mono)}
.struck{text-decoration:line-through}
.noteflag{color:var(--amber);font:11px var(--mono)}
.dangling{color:var(--red)}
.wikilink{cursor:pointer}
mark.ins, .ins{background:#f6ecc8;box-shadow:inset 3px 0 0 var(--amber);padding-left:.5rem}
.grey{color:#8c8578}
table{border-collapse:collapse;width:100%;margin:.6rem 0 1rem;font:14px var(--sans)}
caption{caption-side:top;text-align:left;font:11px var(--mono);letter-spacing:.1em;color:#6b6355;padding-bottom:.3rem;text-transform:uppercase}
th,td{border-top:1px solid var(--rule);padding:.35rem .5rem;text-align:left;vertical-align:top}
th{font:11px var(--mono);letter-spacing:.08em;text-transform:uppercase;color:#6b6355)
}
td.num,th.num{text-align:right;font-variant-numeric:tabular-nums}
fieldset{border:1px solid var(--rule);padding:1rem 1.2rem;margin:1rem 0;background:#fbf8f2}
legend{font:11px var(--mono);letter-spacing:.1em;text-transform:uppercase;padding:0 .4rem}
button.act{font:12px var(--mono);letter-spacing:.05em;background:var(--ink);color:var(--paper);border:none;padding:.55rem 1.1rem;cursor:pointer}
button.act:disabled{background:#a99f8d;cursor:not-allowed}
button.quiet{font:11px var(--mono);background:none;border:1px solid var(--rule);padding:.3rem .7rem;cursor:pointer}
.progress{font:12px var(--mono);color:var(--red);min-height:1.3em}
[aria-live]{outline:none}
.verdict{font:400 1.9rem var(--serif);margin:.2rem 0}
.leanbar{height:14px;background:#e5ddcc;position:relative;max-width:420px;margin:.4rem 0}
.leanbar i{position:absolute;left:0;top:0;bottom:0;background:var(--red)}
.figno{font:11px var(--mono);letter-spacing:.12em;color:#6b6355;text-transform:uppercase}
textarea{width:100%;min-height:5rem;font:15px var(--sans);border:1px solid var(--rule);background:#fbf8f2;padding:.5rem}
.greybox{background:#eae4d6;border:1px solid var(--rule);padding:.7rem .9rem;font:13px var(--sans);margin:.8rem 0}
[data-source="ai"]{border-left:3px solid var(--rule);padding-left:1rem}
details{border-top:1px solid var(--rule);padding:.4rem 0}
summary{cursor:pointer;font:14px var(--mono)}
.session{font:10px var(--mono);color:var(--red);border:1px solid var(--red);padding:0 .3rem}
footer{border-top:1px solid var(--rule);padding:.7rem 1.4rem;font:11px var(--mono);color:#6b6355}
.chips{display:flex;flex-wrap:wrap;gap:.4rem;margin:.4rem 0}
.chip{border:1px solid var(--rule);background:#fbf8f2;padding:.15rem .55rem;font:12px var(--mono)}
.chip.on{border-color:var(--red);color:var(--red)}
.step{border:1px solid var(--rule);background:#fbf8f2;padding:.9rem 1.1rem;margin:.8rem 0}
.step h3{margin:.1rem 0 .4rem;font:400 1.05rem var(--serif)}
.lint-pass{color:var(--green);font:11px var(--mono)}.lint-check{color:var(--red);font:11px var(--mono)}
@media(max-width:900px){.panel{flex-direction:column}.rail{width:100%;position:static}}
</style>
</head>
<body>

<header>
  <div>
    <div class="kicker">WIKI · neurotechnology and justice</div>
    <h1>Research wiki: neurotechnology in the administration of justice</h1>
    <div class="dataline" id="hd-dataline"></div>
  </div>
  <div class="hdright">
    <div id="hd-session" aria-live="polite"></div>
    <div>This page has no storage: changes live in it until you download them (tab 05).</div>
  </div>
</header>

<div role="tablist" aria-label="Wiki tabs" id="tabs">
  <button role="tab" id="tab-1" aria-selected="true" aria-controls="p1">01 PAGES</button>
  <button role="tab" id="tab-2" aria-selected="false" aria-controls="p2">02 ASK</button>
  <button role="tab" id="tab-3" aria-selected="false" aria-controls="p3">03 INGEST</button>
  <button role="tab" id="tab-4" aria-selected="false" aria-controls="p4">04 CHECK</button>
  <button role="tab" id="tab-5" aria-selected="false" aria-controls="p5">05 RECORD</button>
</div>

<main>
  <!-- 01 PAGES -->
  <section id="p1" role="tabpanel" aria-labelledby="tab-1" class="panel">
    <div class="rail">
      <label for="pgfilter" class="kicker">Filter</label>
      <input id="pgfilter" placeholder="title, tag or slug" autocomplete="off">
      <div class="bignum" id="pgcount"></div>
      <span class="hint">pages matching the filter · click a page to read it</span>
      <div id="pglist" class="plist"></div>
    </div>
    <div class="textcol" id="pgmain" aria-live="polite"></div>
  </section>

  <!-- 02 ASK -->
  <section id="p2" role="tabpanel" aria-labelledby="tab-2" hidden class="textcol" style="max-width:900px">
    <div class="greybox" id="ask-grey">
      Step 1 sends the wiki index and your question to the model. Step 2 sends the bodies of the pages it picks, and the question.
      Every prompt states the pin syntax and that only words standing in the passages given may be quoted; this page's code checks every quote afterwards. Nothing is sent until you press the button.
    </div>
    <label for="askq" class="kicker">Question</label>
    <textarea id="askq" placeholder="e.g. Can a suspect consent to brain-based lie detection?"></textarea>
    <div style="margin:.5rem 0;display:flex;gap:.6rem;align-items:center">
      <button class="act" id="askbtn">Ask the wiki</button>
      <button class="quiet" id="askstop" hidden>Stop</button>
      <span class="progress" id="askprog" aria-live="polite"></span>
    </div>
    <div id="askout" aria-live="polite"></div>
  </section>

  <!-- 03 INGEST -->
  <section id="p3" role="tabpanel" aria-labelledby="tab-3" hidden class="textcol" style="max-width:1000px">
    <div id="ingmain" aria-live="polite"></div>
  </section>

  <!-- 04 CHECK -->
  <section id="p4" role="tabpanel" aria-labelledby="tab-4" hidden>
    <div class="bignum" id="ck-big"></div>
    <span class="hint">pins verified by this page's code against the library passages · <span id="ck-lintn"></span></span>
    <div id="ck-top"></div>
    <div style="margin:.7rem 0"><button class="act" id="lintbtn">Lint now</button></div>
    <div id="lintout"></div>
  </section>

  <!-- 05 RECORD -->
  <section id="p5" role="tabpanel" aria-labelledby="tab-5" hidden class="textcol" style="max-width:900px">
    <div style="display:flex;gap:.6rem;align-items:center;margin-bottom:.6rem">
      <button class="quiet" id="logorder">Order: newest first</button>
      <button class="act" id="dlwiki">Download the wiki</button>
      <button class="act" id="dlpages" hidden>Download changed pages</button>
    </div>
    <div class="figno">LOG</div>
    <div id="logout"></div>
    <div class="figno" style="margin-top:1.4rem">TENSIONS REGISTER</div>
    <div id="tensout" class="pagebody"></div>
    <div class="greybox" style="margin-top:1.4rem">
      <p><strong>Method.</strong> Counting, matching and verification are done by this page's code: pins are matched against library passages after normalising quotes, dashes and hyphenation; every number above carries its “How this is computed” line. The model is called only when you press Ask, Ingest or a retry button.</p>
      <p id="rec-src"></p>
    </div>
  </section>
</main>

<footer id="ft"></footer>

<script>
"use strict";
const W = WORKSHOP_DATA.wiki, LIB = WORKSHOP_DATA.library;
const P = W.pages, D = LIB.records;
const slugMap = new Map(P.map(p=>[p.slug,p]));
const docMap = new Map(D.map(d=>[d.id,d]));
const PIN_RE = /\[([^\]]+)\]\(pin:([^#\s)]+)#p(\d+)(?: "([^"]*)")?\)\s?(✓|⚠)?/g;
const LINK_RE = /\[\[([^\]|#]+)(?:\|[^\]]*)?\]\]/g;
const REG_NAMES = {a:"treaty law",b:"General Comments",c:"UN, agency and soft-law reports",d:"national human rights institution",e:"civil society",f:"scholarship"};
const REG_W = {a:5,b:4,c:3,d:2,e:1,f:0.5};
const esc = s => String(s).replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
const today = () => new Date().toISOString().slice(0,10);

const S = {calls:0,chars:0,passages:0,changes:0,stop:false,logAdded:[],changedPages:[],newTensions:[],approved:0};

/* ---------- normalisation & verification ---------- */
function norm(s){return String(s).normalize("NFKC")
 .replace(/[\u201C\u201D\u201E]/g,'"').replace(/[\u2018\u2019]/g,"'")
 .replace(/[\u2013\u2014]/g,"-").replace(/\u00AD/g,"")
 .replace(/- /g,"-").replace(/\s+/g," ").trim();}

const vCache = new Map();
function parsePins(body){const out=[];let m;const re=new RegExp(PIN_RE);while((m=re.exec(body)))out.push({label:m[1],id:m[2],page:+m[3],quote:m[4]||"",mark:m[5]||""});return out;}
function pagePins(p){if(!p._pins)p._pins=parsePins(p.body);return p._pins;}
function bodyLinks(body){const out=[];let m;const re=new RegExp(LINK_RE);while((m=re.exec(body)))out.push(m[1]);return out;}
function pageBodyLinks(p){if(!p._bl)p._bl=bodyLinks(p.body);return p._bl;}

function verifyPin(p){
  const key = p.id+"#"+p.page+"|"+norm(p.quote);
  if(vCache.has(key))return vCache.get(key);
  let r;
  const doc = docMap.get(p.id);
  if(!p.quote) r={ok:false,reason:"pin has no quote"};
  else if(!doc) r={ok:false,reason:"unknown document "+p.id};
  else if(doc.status==="inbox") r={ok:false,reason:doc.id+" is still in the inbox (not read into the wiki)"};
  else{
    const frags=p.quote.split(/\u2026|\.\.\./).map(norm).filter(Boolean);
    let quoteHit=null;
    for(const x of doc.passages){
      if(x.page!==p.page)continue;
      const t=norm(x.text);let pos=0,all=true;
      for(const f of frags){const i=t.indexOf(f,pos);if(i<0){all=false;break;}pos=i+f.length;}
      if(all){quoteHit=x;
        const labelOk = x.paragraph!=null ? p.label.includes("para. "+x.paragraph) : p.label.includes("p. "+x.page_label);
        if(labelOk){r={ok:true,passage:x,doc};break;}
      }
    }
    if(!r) r = quoteHit ? {ok:false,reason:"quote found on PDF page "+p.page+" but the label does not match that passage"}
                        : {ok:false,reason:"quote not found on PDF page "+p.page+" of "+p.id};
  }
  vCache.set(key,r);return r;
}
function docRegister(id){
  for(const p of P){if(p.frontmatter&&p.frontmatter.sources&&p.frontmatter.sources.length===1&&p.frontmatter.sources[0]===id)return p.frontmatter.register||["?"];}
  return ["?"];
}
function citeAs(doc){
  const counts=new Map();
  for(const p of P)for(const pin of pagePins(p)){
    if(pin.id!==doc.id)continue;
    const m=pin.label.match(/^(.*?), (?:para\.|p\.) /);
    if(m)counts.set(m[1],(counts.get(m[1])||0)+1);
  }
  let best=null,bn=0;for(const[k,v]of counts)if(v>bn){bn=v;best=k;}
  return best||doc.symbol||(doc.author+" "+doc.year);
}
function makePin(doc,x,quote){
  const q = quote.replace(/"/g,"\u201C").replace(/(?<=\u201C[^"]*)"/,"\u201D");
  const lbl = x.paragraph!=null ? citeAs(doc)+", para. "+x.paragraph : citeAs(doc)+", p. "+x.page_label;
  return "["+lbl+"](pin:"+doc.id+"#p"+x.page+" \u201C"+q.replace(/\u201C|\u201D/g,'"')+"\u201D) \u2713".replace("\u201C",'"').replace("\u201D",'"');
}
function pinMarkdown(doc,x,quote){
  const q=quote.replace(/"/g,"\u201D");
  const lbl = x.paragraph!=null ? citeAs(doc)+", para. "+x.paragraph : citeAs(doc)+", p. "+x.page_label;
  return "["+lbl+"](pin:"+doc.id+"#p"+x.page+' "'+q+'") \u2713';
}

/* ---------- counters / header ---------- */
function totals(){
  let pins=0,ver=0;const byType={};
  for(const p of P){byType[p.type]=(byType[p.type]||0)+1;for(const pin of pagePins(p)){pins++;if(verifyPin(pin).ok)ver++;}}
  return{pins,ver,byType,inbox:D.filter(d=>d.status==="inbox").length};
}
function updateHeader(){
  const t=totals();
  document.getElementById("hd-dataline").textContent =
    P.length+" pages ("+(t.byType.source||0)+" sources, "+(t.byType.concept||0)+" concepts, "+(t.byType.entity||0)+" entities, "+(t.byType.question||0)+" questions) · "
    +t.pins+" pins, "+t.ver+" verified by this page · "+D.length+" documents, "+t.inbox+" in the inbox · built "+W.built;
  document.getElementById("hd-session").textContent =
    "Changes this session: "+S.changes+" · Calls to the model: "+S.calls+" · Passages that left the browser: "+S.passages;
  document.getElementById("ft").textContent = W.source+" · built "+W.built+" · Counting, matching and verification are done by this page's code; the model is called only when you press Ask, Ingest or a retry button.";
  document.getElementById("rec-src").textContent = "Data source: "+W.source+" · "+P.length+" pages · "+D.length+" library documents.";
}

/* ---------- rendering: pins, links, body ---------- */
function pinChip(p,opts){
  opts=opts||{};
  const v=verifyPin(p);
  const regs=docRegister(p.id).join("");
  const regName=REG_NAMES[docRegister(p.id)[0]]||"";
  let note="";
  if(p.mark&&((p.mark==="\u2713")!==v.ok))note=' <span class="noteflag">page says '+(p.mark==="\u2713"?"✓":"⚠")+"</span>";
  const struck=opts.sentSet&&!(opts.sentSet.has(p.id+"#"+p.page+"|"+norm(p.quote))&&v.ok);
  const chip =
    '<span class="pinchip'+(struck?" struck":"")+'">'
    +'<button type="button" class="lbl pin-open" data-id="'+esc(p.id)+'" data-page="'+p.page+'" data-quote="'+esc(p.quote)+'">'+esc(p.label)+"</button>"
    +' <span class="'+(v.ok?"ok":"bad")+'">'+(v.ok?"✓ verified":"⚠ not found")+"</span>"
    +(regs&&regs!=="?"?' <span title="'+esc(regName)+'">'+esc(regs)+"</span>":"")
    +(opts.regName?' <span>'+esc(opts.regName)+"</span>":"")
    +(struck?' <span class="noteflag">not on the pages sent</span>':"")
    +note
    +' <button type="button" class="quiet pin-x" aria-expanded="false" aria-label="Show the passage behind this pin">▾</button></span>';
  const det='<span class="pindetail" hidden>'
    +(v.ok?("Passage "+(v.passage.paragraph!=null?"para. "+v.passage.paragraph:"p. "+v.passage.page_label)+" · PDF page "+v.passage.page+" · "+esc(v.passage.text.slice(0,300))+(v.passage.text.length>300?"…":"")):esc(v.reason||"not verified")
      +". Footnotes, tables and captions are not in the passages; a pin cannot verify them.")
    +' <button type="button" class="quiet pin-open" data-id="'+esc(p.id)+'" data-page="'+p.page+'" data-quote="'+esc(p.quote)+'">Open the PDF page</button></span>';
  return '<span class="pinwrap"><span class="pinquote">\u201C'+esc(p.quote)+"\u201D</span> "+chip+det+"</span>";
}
function wikiLink(slug){
  const t=slugMap.get(slug);
  if(t)return '<a class="wikilink" data-slug="'+esc(slug)+'" tabindex="0">'+esc(t.title)+"</a>";
  return '<span class="dangling">'+esc(slug)+"</span> <span class=\"noteflag\">no page</span>";
}
function inlineHTML(raw,opts){
  const toks=[];let s=String(raw);
  s=s.replace(new RegExp(PIN_RE),(m,label,id,page,quote,mark)=>{toks.push(pinChip({label,id,page:+page,quote:quote||"",mark:mark||""},opts));return "\u0001"+(toks.length-1)+"\u0001";});
  s=s.replace(new RegExp(LINK_RE),(m,slug)=>{toks.push(wikiLink(slug));return "\u0001"+(toks.length-1)+"\u0001";});
  s=s.replace(/\[([^\]]+)\]\((https?:[^)\s]+)\)/g,(m,t,u)=>{toks.push('<a href="'+esc(u)+'" target="_blank" rel="noopener">'+esc(t)+"</a>");return "\u0001"+(toks.length-1)+"\u0001";});
  let h=esc(s).replace(/\*\*([^*]+)\*\*/g,"<strong>$1</strong>").replace(/\*([^*]+)\*/g,"<em>$1</em>");
  h=h.replace(/\u0001(\d+)\u0001/g,(m,i)=>toks[+i]);
  return h;
}
function parseContested(buf){
  const c={claim:"",verdict:"",note:"",positions:[]};
  for(const line of buf.split("\n")){
    if(/^claim:/.test(line))c.claim=line.slice(6).trim();
    else if(/^verdict:/.test(line))c.verdict=line.slice(8).trim();
    else if(/^note:/.test(line))c.note=line.slice(5).trim();
    else{const m=line.match(/^([+~-])\s+(.+)$/);if(m)c.positions.push({sign:m[1],parts:m[2].split(" | ")});}
  }
  return c;
}
function lean(c){
  let sup=0,tot=0;
  for(const p of c.positions){const w=REG_W[p.parts[1]?p.parts[1].trim():"f"]||0.5;tot+=w;if(p.sign==="+")sup+=w;else if(p.sign==="~")sup+=w/2;}
  return tot?Math.round(100*sup/tot):0;
}
function contestedCard(buf,opts){
  const c=parseContested(buf);
  const pct=lean(c);
  let pos="";
  for(const p of c.positions){
    const sign=p.sign==="+"?"supports":p.sign==="-"?"contests":"mixed";
    const pinTxt=p.parts[2]||"";
    const pinM=pinTxt.match(new RegExp(PIN_RE));
    const pin=pinM?pinChip({label:pinM[1],id:pinM[2],page:+pinM[3],quote:pinM[4]||"",mark:pinM[5]||""},opts):esc(pinTxt);
    const slug=(p.parts[4]||"").replace(/\[\[|\]\]/g,"").trim();
    pos+="<tr><td>"+sign+"</td><td>"+esc(p.parts[1]||"")+"</td><td>"+pin+"</td><td>"+esc(p.parts[3]||"")+"</td><td>"+(slug?wikiLink(slug):"")+"</td></tr>";
  }
  const tensLink = tensionsHasCard(opts.slug) ? ' · <a class="wikilink" data-goto-tab="5">in the tensions register</a>' : "";
  return '<div class="step"><div class="figno">FIG.01 · contested claim</div><h3>'+esc(c.claim)+"</h3>"
   +'<div class="verdict">'+esc(c.verdict)+"</div>"
   +(c.note?"<p>"+esc(c.note)+"</p>":"")
   +'<div class="figno">lean bar · descriptive: support '+pct+"% of weighted positions · weights a 5 · b 4 · c 3 · d 2 · e 1 · f ½ · the verdict is the answer</div>"
   +'<div class="leanbar" role="img" aria-label="support '+pct+' percent of weighted positions"><i style="width:'+pct+'%"></i></div>'
   +'<table><caption>positions · sign · register · pin · gloss · page</caption><thead><tr><th>Sign</th><th>Reg.</th><th>Pin</th><th>Gloss</th><th>Page</th></tr></thead><tbody>'+pos+"</tbody></table>"
   +'<span class="hint">How this is computed: (Σ weight of “+” + ½ Σ weight of “~”) ÷ Σ weight of all positions'+tensLink+"</span></div>";
}
function renderBody(body,opts){
  opts=opts||{};
  const lines=String(body).split("\n");let html="",i=0,ins=false;
  const openIns=()=>ins?' class="ins"':""; 
  while(i<lines.length){
    let L=lines[i];
    if(L.startsWith("\u0002")){ins=true;L=L.slice(1);}
    let closeAfter=false;
    if(L.endsWith("\u0003")){closeAfter=true;L=L.slice(0,-1);}
    if(/^```contested/.test(L)){
      let j=i+1,buf=[];while(j<lines.length&&!/^```/.test(lines[j])){buf.push(lines[j]);j++;}
      html+=contestedCard(buf.join("\n"),opts);i=j+1;continue;
    }
    const h=L.match(/^(#{1,3})\s+(.*)/);
    if(h){html+="<h"+(+h[1].length+1)+openIns()+">"+inlineHTML(h[2],opts)+"</h"+(+h[1].length+1)+">";i++;if(closeAfter)ins=false;continue;}
    if(/^\s*[-*]\s+/.test(L)){const buf=[];while(i<lines.length&&/^\s*[-*]\s+/.test(lines[i])){buf.push(lines[i].replace(/^\s*[-*]\s+/,"").replace(/^\u0002|\u0003$/g,""));i++;}
      html+="<ul"+openIns()+">"+buf.map(x=>"<li>"+inlineHTML(x,opts)+"</li>").join("")+"</ul>";if(closeAfter)ins=false;continue;}
    if(/^\s*\d+\.\s+/.test(L)){const buf=[];while(i<lines.length&&/^\s*\d+\.\s+/.test(lines[i])){buf.push(lines[i].replace(/^\s*\d+\.\s+/,"").replace(/^\u0002|\u0003$/g,""));i++;}
      html+="<ol"+openIns()+">"+buf.map(x=>"<li>"+inlineHTML(x,opts)+"</li>").join("")+"</ol>";if(closeAfter)ins=false;continue;}
    if(!L.trim()){i++;continue;}
    const buf=[L];i++;
    while(i<lines.length&&lines[i].trim()&&!/^(#{1,3}\s|```|\s*[-*]\s|\s*\d+\.\s)/.test(lines[i])){buf.push(lines[i]);i++;}
    html+="<p"+openIns()+">"+inlineHTML(buf.join(" "),opts)+"</p>";
    if(closeAfter)ins=false;
  }
  return html;
}

/* ---------- tabs ---------- */
const tabs=[...document.querySelectorAll('[role="tab"]')];
function setTab(n){
  tabs.forEach((t,i)=>{t.setAttribute("aria-selected",i===n-1?"true":"false");document.getElementById("p"+(i+1)).hidden=i!==n-1;});
  if(n===5)renderRecord();
  if(n===4)renderCheck();
}
tabs.forEach((t,i)=>{t.addEventListener("click",()=>setTab(i+1));
  t.addEventListener("keydown",e=>{
    if(e.key==="ArrowRight"){tabs[(i+1)%5].focus();tabs[(i+1)%5].click();}
    if(e.key==="ArrowLeft"){tabs[(i+4)%5].focus();tabs[(i+4)%5].click();}
  });});
document.addEventListener("keydown",e=>{if(e.key==="Escape")S.stop=true;});

/* ---------- 01 PAGES ---------- */
let currentSlug=null;
function renderList(){
  const q=document.getElementById("pgfilter").value.trim().toLowerCase();
  const groups=[["source","SOURCES"],["concept","CONCEPTS"],["entity","ENTITIES"],["question","QUESTIONS"]];
  const backlinks=backlinkMap();
  let html="",n=0;
  for(const[type,lab]of groups){
    const ps=P.filter(p=>p.type===type&&(!q||p.title.toLowerCase().includes(q)||(p.slug||"").toLowerCase().includes(q)||(p.frontmatter.tags||[]).join(" ").toLowerCase().includes(q)));
    if(!ps.length)continue;
    html+='<div class="grouplab">'+lab+"</div>";
    for(const p of ps){n++;
      const pins=pagePins(p).length;
      html+='<button type="button" data-slug="'+esc(p.slug)+'" class="'+(p.slug===currentSlug?"on":"")+'">'+esc(p.title)
       +' <span class="meta">'+((p.frontmatter.register||[]).join("")||"?")+" · "+pins+" pins"+(p.frontmatter.status==="stub"?' · <span class="stubtag">stub</span>':"")+" · ←"+(backlinks.get(p.slug)||0)+"</span></button>";
    }
  }
  document.getElementById("pglist").innerHTML=html;
  document.getElementById("pgcount").textContent=n+" of "+P.length+" pages";
}
function backlinkMap(){
  const m=new Map();
  for(const p of P)for(const s of pageBodyLinks(p))m.set(s,(m.get(s)||0)+1);
  return m;
}
function showIndex(){
  currentSlug=null;renderList();
  document.getElementById("pgmain").innerHTML='<div class="figno">INDEX</div><div class="pagebody">'+renderBody(W.index,{})+'</div><span class="hint">How this is computed: the index markdown from the data, rendered like a page; pin counts on it are the marks written there, not recomputed.</span>';
}
function showPage(slug){
  const p=slugMap.get(slug);if(!p)return;
  currentSlug=slug;renderList();
  history.replaceState(null,"","#"+slug);
  const fm=p.frontmatter||{};
  const backlinks=P.filter(x=>pageBodyLinks(x).includes(slug));
  const pins=pagePins(p),ver=pins.filter(x=>verifyPin(x).ok).length;
  let h='<div class="figno">PAGE · '+esc(slug)+'</div><h2 style="font:400 1.8rem var(--serif);margin:.2rem 0">'+esc(p.title)+"</h2>";
  h+='<div class="badges"><b>'+esc(p.type)+"</b><b>"+((fm.register||[]).join("")||"?")+" "+(fm.register||[]).map(r=>REG_NAMES[r]).filter(Boolean).join(", ")+"</b><b>"+esc(fm.status||"?")+"</b><b>updated "+esc(fm.updated||"?")+"</b></div>";
  if((fm.tags||[]).length)h+='<div class="badges">tags: '+esc(fm.tags.join(" · "))+"</div>";
  h+='<div class="pagebody">'+renderBody(p.body,{slug})+"</div>";
  h+='<span class="hint">How this is computed: pins found in the body by the pin regular expression; '+ver+" of "+pins.length+" verified by this page's code.</span>";
  h+='<h3>Links out</h3><p>'+((fm.links||[]).length?fm.links.map(s=>wikiLink(s)+(pageBodyLinks(p).includes(s)?"":' <span class="noteflag">frontmatter only</span>')).join(" · "):"none")+"</p>";
  h+='<h3>Linked from</h3><p>'+(backlinks.length?backlinks.map(b=>wikiLink(b.slug)).join(" · "):"none")+"</p>";
  h+='<h3>Sources</h3><ul>'+(fm.sources||[]).map(id=>{const d=docMap.get(id);if(!d)return "<li>"+esc(id)+"</li>";
    return '<li><a href="'+esc(d.url||"")+'" target="_blank" rel="noopener">'+esc(d.symbol||d.id)+"</a> · "+esc(d.short_title)+" · "+esc(d.kind)+" · "+d.year+(d.status==="inbox"?' · <span class="noteflag">inbox</span>':"")+"</li>";}).join("")||"<li>none</li>")+"</ul>";
  h+='<div style="margin:.8rem 0"><button type="button" class="quiet" id="copymd">Copy page as markdown</button></div>';
  document.getElementById("pgmain").innerHTML=h;
  document.getElementById("copymd").onclick=()=>{
    const yml="---\ntitle: "+JSON.stringify(p.title)+"\ntype: "+p.type+"\ntags: "+JSON.stringify(fm.tags||[])+"\nregister: "+JSON.stringify(fm.register||[])+"\nstatus: "+(fm.status||"")+"\nupdated: "+(fm.updated||"")+"\nlinks: "+JSON.stringify(fm.links||[])+"\nsources: "+JSON.stringify(fm.sources||[])+"\n---\n\n";
    copyText(yml+p.body);
  };
}
function copyText(t){
  if(navigator.clipboard&&navigator.clipboard.writeText)navigator.clipboard.writeText(t).catch(()=>fallbackCopy(t));
  else fallbackCopy(t);
}
function fallbackCopy(t){const ta=document.createElement("textarea");ta.value=t;document.body.appendChild(ta);ta.select();try{document.execCommand("copy");}catch(e){}ta.remove();}
document.getElementById("pgfilter").addEventListener("input",renderList);

/* delegated events */
document.addEventListener("click",e=>{
  const open=e.target.closest(".pin-open");
  if(open){studio.openSource(open.dataset.id,+open.dataset.page,open.dataset.quote);return;}
  const x=e.target.closest(".pin-x");
  if(x){const d=x.closest(".pinwrap").querySelector(".pindetail");d.hidden=!d.hidden;x.setAttribute("aria-expanded",String(!d.hidden));return;}
  const wl=e.target.closest(".wikilink");
  if(wl&&wl.dataset.slug){setTab(1);showPage(wl.dataset.slug);return;}
  if(e.target.closest('[data-goto-tab="5"]')){setTab(5);return;}
  const pb=e.target.closest(".plist button");
  if(pb){showPage(pb.dataset.slug);return;}
});
document.addEventListener("keydown",e=>{if(e.key==="Enter"&&e.target.classList&&e.target.classList.contains("wikilink")&&e.target.dataset.slug){setTab(1);showPage(e.target.dataset.slug);}});

/* ---------- model calls ---------- */
async function askModel(prompt,passageCount,progEl){
  S.calls++;S.chars+=prompt.length;S.passages+=passageCount;updateHeader();
  progEl.textContent="Sending "+prompt.length.toLocaleString()+" characters"+(passageCount?" · "+passageCount+" passages":"")+" to the model…";
  let raw;
  try{raw=await studio.ask(prompt,{json:true});}
  catch(err){throw{raw:String(err&&err.message||err),error:true};}
  try{return JSON.parse(raw);}catch(e){}
  const stripped=(raw.match(/```(?:json)?\s*([\s\S]*?)```/)||[])[1];
  if(stripped){try{return JSON.parse(stripped);}catch(e){}}
  throw{raw};
}
const PIN_RULE = ' Pin syntax: [Label, para. N](pin:DOCID#pPDFPAGE "verbatim quote") \u2713. Quote only words that stand in the passages given; the code will check.';

/* ---------- 02 ASK ---------- */
const askQ=document.getElementById("askq"),askBtn=document.getElementById("askbtn"),askStop=document.getElementById("askstop"),askProg=document.getElementById("askprog"),askOut=document.getElementById("askout");
let askState=null;
askBtn.addEventListener("click",runAsk);
askStop.addEventListener("click",()=>S.stop=true);
async function runAsk(){
  const q=askQ.value.trim();if(!q){askProg.textContent="Type a question first.";return;}
  S.stop=false;askStop.hidden=false;askBtn.disabled=true;
  askState={q,pages:[],answer:null};
  try{
    askProg.textContent="Step 1: sending the index ("+W.index.length.toLocaleString()+" characters) and your question; 0 library passages leave the browser.";
    const r1=await askModel("You are asked a question about a research wiki. Here is the wiki index:\n\n"+W.index+"\n\nQuestion: "+q+"\n\nReturn JSON {\"pages\":[\"slug\",...]}, at most five slugs from the index that bear on the question."+PIN_RULE,0,askProg);
    if(S.stop){askProg.textContent="Stopped.";return;}
    if(!r1||!Array.isArray(r1.pages))throw{raw:JSON.stringify(r1)};
    const exist=r1.pages.filter(s=>slugMap.has(s));
    const missing=r1.pages.filter(s=>!slugMap.has(s));
    askState.pages=exist.slice(0,5);
    askProg.textContent="Step 1 done: "+askState.pages.length+" pages chosen"+(missing.length?" · slugs that do not exist (dropped): "+missing.join(", "):"")+". Step 2: sending their bodies; 0 library passages leave the browser.";
    renderAskChips();
    if(!askState.pages.length){askOut.innerHTML='<p class="noteflag">No existing pages were chosen for this question.</p>';return;}
    const bodies=askState.pages.map(s=>"--- PAGE "+s+" ---\n"+slugMap.get(s).body).join("\n\n");
    const chars=W.index.length+bodies.length+q.length;
    askProg.textContent="Step 2: "+askState.pages.length+" pages, "+chars.toLocaleString()+" characters; 0 library passages have left the browser.";
    const r2=await askModel("You answer a question using ONLY the wiki pages below. Pages:\n\n"+bodies+"\n\nQuestion: "+q+"\n\nRules: answer in at most 350 words; use pins only where the same pin already stands in the pages given, copied exactly (same document id, PDF page and quote); name the register where it matters (e.g. \u201C(c) UN report\u201D); keep each document's own verb; never present (c) to (f) documents as what the treaty requires. Return JSON {\"title\":\"...\",\"answer\":\"markdown\",\"cannot_answer\":\"what the library cannot answer\"}."+PIN_RULE,0,askProg);
    if(S.stop){askProg.textContent="Stopped.";return;}
    if(!r2||typeof r2.answer!=="string")throw{raw:JSON.stringify(r2)};
    askState.answer=r2;renderAnswer();
  }catch(err){
    askOut.innerHTML='<div class="greybox"><p class="noteflag">The model\u2019s answer could not be parsed. Nothing was filed.</p><pre style="white-space:pre-wrap;font:12px var(--mono)">'+esc(err.raw||"")+'</pre><button type="button" class="quiet" id="askretry">Retry</button></div>';
    document.getElementById("askretry").onclick=runAsk;
  }finally{askStop.hidden=true;askBtn.disabled=false;askBtn.textContent="Ask again";}
}
function renderAskChips(){
  let h='<p class="kicker">PAGES CHOSEN</p><div class="chips">'+askState.pages.map(s=>'<span class="chip on">'+esc(slugMap.get(s).title)+"</span>").join("")+'</div><button type="button" class="quiet" id="chgpages">Change pages</button><div id="chglist" hidden></div>';
  askOut.innerHTML=h;
  document.getElementById("chgpages").onclick=()=>{
    const d=document.getElementById("chglist");d.hidden=!d.hidden;
    if(!d.innerHTML){
      d.innerHTML=P.map(p=>'<label style="display:block"><input type="checkbox" value="'+esc(p.slug)+'"'+(askState.pages.includes(p.slug)?" checked":"")+"> "+esc(p.title)+"</label>").join("")+'<button type="button" class="quiet" id="sendpages">Send these pages (1 call)</button>';
      document.getElementById("sendpages").onclick=async()=>{
        askState.pages=[...d.querySelectorAll("input:checked")].map(i=>i.value).slice(0,5);
        d.hidden=true;renderAskChips();S.stop=false;askStop.hidden=false;
        try{
          const bodies=askState.pages.map(s=>"--- PAGE "+s+" ---\n"+slugMap.get(s).body).join("\n\n");
          askProg.textContent="Step 2 (pages changed): "+askState.pages.length+" pages, "+bodies.length.toLocaleString()+" characters; 0 library passages have left the browser.";
          const r2=await askModel("You answer a question using ONLY the wiki pages below. Pages:\n\n"+bodies+"\n\nQuestion: "+askState.q+"\n\nRules: answer in at most 350 words; use pins only where the same pin already stands in the pages given, copied exactly; name the register where it matters; keep each document's own verb; never present (c) to (f) documents as what the treaty requires. Return JSON {\"title\":\"...\",\"answer\":\"markdown\",\"cannot_answer\":\"...\"}."+PIN_RULE,0,askProg);
          if(typeof r2.answer==="string"){askState.answer=r2;renderAnswer();}
        }catch(err){askProg.textContent="Failed; press the button again to retry.";}
        askStop.hidden=true;
      };
    }
  };
}
function sentPinSet(pages){
  const set=new Set();
  for(const s of pages)for(const pin of pagePins(slugMap.get(s)))set.add(pin.id+"#"+pin.page+"|"+norm(pin.quote));
  return set;
}
function renderAnswer(){
  const a=askState.answer;
  const sentSet=sentPinSet(askState.pages);
  const pins=parsePins(a.answer);
  const verByReg={};
  for(const pin of pins){const v=verifyPin(pin);if(v.ok&&sentSet.has(pin.id+"#"+pin.page+"|"+norm(pin.quote))){const r=docRegister(pin.id)[0];verByReg[r]=(verByReg[r]||0)+1;}}
  let h='<div class="figno">ANSWER · model output, checked by this page</div><div data-source="ai"><h2 style="font:400 1.5rem var(--serif)">'+esc(a.title||"Answer")+'</h2><div class="pagebody">'+renderBody(a.answer,{sentSet})+"</div>";
  if(a.cannot_answer)h+='<h3>What the library cannot answer</h3><p>'+esc(a.cannot_answer)+"</p>";
  h+="</div>";
  h+='<p class="hint">Verified pins by register: '+(Object.keys(verByReg).length?Object.keys(verByReg).sort().map(k=>k+" "+verByReg[k]).join(" · "):"none")+" · struck-through pins are not on the pages sent.</p>";
  h+='<div style="margin:.6rem 0"><button type="button" class="act" id="fileq">File as a question page</button> <button type="button" class="quiet" id="copyans">Copy answer</button></div><div id="filecard" hidden></div>';
  askOut.innerHTML=h;
  document.getElementById("copyans").onclick=()=>copyText((a.title||"")+"\n\n"+a.answer+"\n\nCannot answer: "+(a.cannot_answer||""));
  document.getElementById("fileq").onclick=renderFileCard;
}
function renderFileCard(){
  const card=document.getElementById("filecard");card.hidden=false;
  const a=askState.answer;
  let base=a.title.toLowerCase().replace(/[^a-z0-9]+/g,"-").replace(/^-|-$/g,"")||"question";
  let slug=base,i=2;while(slugMap.has(slug))slug=base+"-"+(i++);
  const pins=parsePins(a.answer);
  const allVer=pins.every(p=>verifyPin(p).ok);
  const sentSet=sentPinSet(askState.pages);
  const onSent=pins.every(p=>sentSet.has(p.id+"#"+p.page+"|"+norm(p.quote))&&verifyPin(p).ok);
  const regs=[...new Set(pins.flatMap(p=>docRegister(p.id)))].sort();
  const links=[...new Set(bodyLinks(a.answer))].filter(s=>slugMap.has(s));
  const srcs=[...new Set(pins.map(p=>p.id))];
  const body="# "+(a.title||"Question")+"\n\n**Short answer.**\n\n## Reasoning\n\n"+a.answer+"\n\n## What the library cannot answer\n\n"+(a.cannot_answer||"—")+"\n\n## Related\n\n"+(links.map(l=>"- [["+l+"]]").join("\n")||"- (none)");
  const page={slug,type:"question",title:a.title||slug,frontmatter:{title:a.title||slug,type:"question",tags:[],register:regs,status:"draft",updated:today(),links,sources:srcs},body,_draft:true};
  card.innerHTML='<fieldset><legend>File as a question page · preview</legend>'
   +'<label class="kicker">Tags (comma-separated)</label><input id="qtags" style="width:100%;padding:.4rem;border:1px solid var(--rule)" placeholder="e.g. neurotechnology, fair-trial">'
   +'<div class="pagebody" style="margin-top:.7rem">'+renderBody(body,{})+"</div>"
   +'<span class="hint">Slug: '+slug+" · register "+(regs.join("")||"?")+" · links "+links.length+" · sources "+srcs.length+"</span>"
   +'<div style="margin:.5rem 0"><button type="button" class="act" id="dofile"'+(onSent?"":" disabled")+">File this page</button>"
   +(onSent?"":' <span class="noteflag">Disabled: '+(allVer?"some pins are not on the pages sent.":"not every pin in the answer verifies.")+"</span>")+"</div></fieldset>";
  document.getElementById("qtags").oninput=e=>{page.frontmatter.tags=e.target.value.split(",").map(t=>t.trim()).filter(Boolean);};
  document.getElementById("dofile").onclick=()=>{
    P.push(page);slugMap.set(page.slug,page);
    page._pins=null;page._bl=null;
    const line="- [["+page.slug+"]] — "+(a.title||"")+" · ("+(regs.join("")||"?")+") · \u2713"+pins.filter(p=>verifyPin(p).ok).length;
    W.index=insertIndexLine(W.index,page.slug,line,"Questions");
    const entry="## ["+today()+"] ask | "+(a.title||page.slug);
    W.log+=(W.log.endsWith("\n")?"":"\n")+"\n"+entry+"\n";
    S.logAdded.push(entry);S.changes++;S.changedPages.push(page.slug);
    updateHeader();vCacheClearPage(page);
    card.innerHTML='<p class="lint-pass" role="status">Filed: '+esc(page.title)+" ("+esc(page.slug)+"). The page now stands in the wiki for this session; download it on tab 05.</p>";
  };
}
function vCacheClearPage(p){for(const pin of pagePins(p))vCache.delete(pin.id+"#"+pin.page+"|"+norm(pin.quote));}
function insertIndexLine(index,slug,line,section){
  const lines=index.split("\n");
  const at=lines.findIndex(l=>l.includes("[["+slug+"]]"));
  if(at>=0){lines[at]=line;return lines.join("\n");}
  let ins=-1;
  for(let i=0;i<lines.length;i++){if(/^##\s/.test(lines[i])&&lines[i].slice(2).trim().toLowerCase().startsWith((section||"").toLowerCase())){let j=i+1;while(j<lines.length&&!/^##\s/.test(lines[j]))j++;ins=j;} }
  if(ins<0)ins=lines.length;
  lines.splice(ins,0,line);return lines.join("\n");
}

/* ---------- 03 INGEST ---------- */
const ingMain=document.getElementById("ingmain");
let ing=null;
function renderIngestStart(){
  const inbox=D.filter(d=>d.status==="inbox");
  ing=null;
  if(!inbox.length){ingMain.innerHTML='<p class="hint">Nothing waits in the inbox. Every library document is ingested.</p>';return;}
  ingMain.innerHTML='<p class="kicker">INBOX</p>'+inbox.map(d=>'<p><button type="button" class="act" data-doc="'+esc(d.id)+'">Ingest '+esc(d.symbol||d.short_title)+"</button> <span class=\"hint\">"+esc(d.short_title)+" · "+d.passages.length+" passages · "+esc(d.kind)+" · "+d.year+"</span></p>").join("");
  ingMain.querySelectorAll("button[data-doc]").forEach(b=>b.onclick=()=>openIngest(b.dataset.doc));
}
function openIngest(id){
  const doc=docMap.get(id);
  ing={doc,step:1,batches:[],takeaways:[],failed:[],newSlugs:[],drafts:null,changes:[],cursor:0,decided:[],tensions:[]};
  const n=Math.ceil(doc.passages.length/25);
  let rows="";
  for(let b=0;b<n;b++){
    const batch=doc.passages.slice(b*25,(b+1)*25);
    ing.batches.push(batch);
    const paras=batch.filter(x=>x.paragraph!=null).map(x=>x.paragraph);
    rows+="<tr><td>"+(b+1)+"</td><td>"+(paras.length?esc(paras[0])+" – "+esc(paras[paras.length-1]):"—")+"</td><td>"+batch[0].page+" – "+batch[batch.length-1].page+"</td><td class='num'>"+batch.length+"</td></tr>";
  }
  const chars=doc.passages.reduce((s,x)=>s+x.text.length,0);
  ingMain.innerHTML='<h2 style="font:400 1.5rem var(--serif)">Ingest '+esc(doc.symbol||doc.short_title)+'</h2>'
   +'<p class="hint">Scope: the whole document. All '+doc.passages.length+' passages will be sent, in batches of 25 ('+n+" calls), "+chars.toLocaleString()+" characters; nothing is held back.</p>"
   +'<div class="progress" id="ingprog" aria-live="polite">calls so far 0 · passages sent 0</div>'
   +'<table><caption>FIG.02 · batches</caption><thead><tr><th>Batch</th><th>Paragraphs</th><th>PDF pages</th><th class="num">Passages</th></tr></thead><tbody>'+rows+"</tbody></table>"
   +'<button type="button" class="act" id="ingstart">Start</button> <button type="button" class="quiet" id="ingstop" hidden>Stop</button><div id="ingbody"></div>';
  document.getElementById("ingstart").onclick=runBatches;
  document.getElementById("ingstop").onclick=()=>S.stop=true;
  setTabRun(3,true);
}
function ingProg(extra){
  const el=document.getElementById("ingprog");
  if(el)el.textContent="calls so far "+S.calls+" · passages sent "+S.passages+(extra?" · "+extra:"");
}
async function runBatches(){
  S.stop=false;document.getElementById("ingstart").hidden=true;document.getElementById("ingstop").hidden=false;
  const doc=ing.doc;let b=0;
  for(const batch of ing.batches){
    if(S.stop){ingProg("stopped");break;}
    ingProg("batch "+(b+1)+" of "+ing.batches.length+" · "+(b*25)+" of "+doc.passages.length+" passages have left the browser");
    const payload=batch.map(x=>({id:x.id,page:x.page,paragraph:x.paragraph,text:x.text}));
    try{
      const r=await askModel("You read passages of "+doc.title+" ("+doc.author+", "+doc.published+"), a document being ingested into a research wiki on neurotechnology in the administration of justice. Passages (JSON):\n"+JSON.stringify(payload)+"\n\nThe wiki index:\n"+W.index+"\n\nReturn JSON {\"takeaways\":[{\"claim\":\"...\",\"quote\":\"8 to 40 words copied verbatim from that one passage\",\"passage\":\"the passage id\",\"pages\":[slugs from the index the claim bears on]}]}, at most 10 takeaways."+PIN_RULE,batch.length,ingProgEl());
      if(r&&Array.isArray(r.takeaways)){
        for(const t of r.takeaways){
          const x=batch.find(p=>p.id===t.passage)||doc.passages.find(p=>p.id===t.passage);
          if(!x){ing.failed.push({claim:t.claim,quote:t.quote,passageId:t.passage,reason:"names a passage that was not sent (dropped)"});continue;}
          const pin={label:(x.paragraph!=null?citeAs(doc)+", para. "+x.paragraph:citeAs(doc)+", p. "+x.page_label),id:doc.id,page:x.page,quote:t.quote||"",mark:"\u2713"};
          const v=verifyPin(pin);
          let pages=(t.pages||[]).filter(s=>slugMap.has(s));
          for(const s of (t.pages||[]))if(!slugMap.has(s)&&!ing.newSlugs.includes(s)&&ing.newSlugs.length<2)ing.newSlugs.push(s);
          if(v.ok)ing.takeaways.push({claim:t.clause||t.claim,claim:t.claim,quote:t.quote,x,pin,pages});
          else ing.failed.push({claim:t.claim,quote:t.quote,x,reason:v.reason,nearest:nearestPassage(doc,x,t.quote)});
        }
      }
    }catch(err){
      ingMain.querySelector("#ingbody").insertAdjacentHTML("beforeend",'<div class="greybox"><p class="noteflag">Batch '+(b+1)+' could not be parsed.</p><pre style="white-space:pre-wrap;font:12px var(--mono)">'+esc(err.raw||"")+'</pre><button type="button" class="quiet" data-retrybatch="'+b+'">Retry</button></div>');
    }
    b++;
    renderTakeaways();
  }
  document.getElementById("ingstop").hidden=true;
  ingProg("step 1 done");
  setTabRun(3,false);
  renderStep3();
}
function ingProgEl(){return document.getElementById("ingprog");}
function nearestPassage(doc,x,quote){
  const qw=norm(quote).split(" ");let best=null,bl=0;
  for(const p of doc.passages){
    if(p.page!==x.page)continue;
    const tw=norm(p.text).split(" ");
    for(let i=0;i<qw.length;i++)for(let j=0;j<tw.length;j++){
      let k=0;while(i+k<qw.length&&j+k<tw.length&&qw[i+k]===tw[j+k])k++;
      if(k>bl){bl=k;best=p;}
    }
  }
  return best?{p:best,len:bl}:null;
}
function renderTakeaways(){
  let el=document.getElementById("tk");
  if(!el){document.getElementById("ingbody").insertAdjacentHTML("beforeend",'<div class="figno" style="margin-top:.8rem">FIG.03 · takeaways</div><div id="tk"></div>');el=document.getElementById("tk");}
  let h='<table><caption>verified takeaways · claim · quote · passage · pages</caption><tbody>'
   +ing.takeaways.map(t=>"<tr><td>"+esc(t.claim)+"</td><td>"+esc(t.quote)+"</td><td>para. "+esc(t.x.paragraph!=null?t.x.paragraph:"—")+" · PDF p."+t.x.page+"</td><td>"+t.pages.map(s=>'<span class="chip">'+esc(slugMap.get(s)?slugMap.get(s).title:s)+"</span>").join(" ")+"</td></tr>").join("")
   +"</tbody></table>";
  if(ing.failed.length){
    h+='<fieldset><legend>Could not verify: '+ing.failed.length+"</legend>"
     +ing.failed.map(f=>"<p><strong>"+esc(f.claim)+"</strong> <span class=\"noteflag\">"+esc(f.reason)+"</span><br>Model\u2019s quote: \u201C"+esc(f.quote)+"\u201D"
      +(f.nearest?"<br>Nearest passage on that page: "+(f.nearest.p.paragraph!=null?"para. "+esc(f.nearest.p.paragraph):"PDF p."+f.nearest.p.page)+" ("+f.nearest.len+" consecutive words in common) <button type=\"button\" class=\"quiet pin-open\" data-id=\""+esc(ing.doc.id)+'" data-page="'+f.x.page+'" data-quote="'+esc(f.quote||"")+'">Open the PDF page</button>':"")
      +"</p>").join("")+'<span class="hint">These claims are in no change card and in no later prompt.</span></fieldset>';
  }
  h+='<span class="hint">How this is computed: each quote is matched, after normalisation, against the passage the model named; failed quotes keep the nearest passage on that page by longest run of consecutive normalised words.</span>';
  el.innerHTML=h;
}
function renderStep3(){
  const touched=new Set();
  for(const t of ing.takeaways)for(const s of t.pages)touched.add(s);
  for(const s of ing.newSlugs)touched.add(s);
  touched.add("a-hrc-57-61");
  document.getElementById("ingbody").insertAdjacentHTML("beforeend",
    '<div class="step"><h3>Step 3 · drafts</h3><p><button type="button" class="act" id="draftsrc">Draft the source page (1 call)</button></p><div id="srcdraft"></div><p id="touchedbtn" hidden><button type="button" class="act" id="drafttouch">Draft the changes to '+touched.size+" pages ("+touched.size+" calls)</button></p><div id="touchdraft"></div></div>");
  document.getElementById("draftsrc").onclick=draftSource;
}
async function draftSource(){
  S.stop=false;const btn=document.getElementById("draftsrc");btn.disabled=true;
  const doc=ing.doc,ca=citeAs(doc);
  const tk=ing.takeaways.map(t=>({claim:t.claim,pin:pinMarkdown(doc,t.x,t.quote)}));
  const anatomy="Full cite, Register, One-liner, Key takeaways, How NOT to read this, Where it feeds the wiki, Related";
  try{
    const r=await askModel("Draft the source wiki page for "+doc.title+" ("+doc.author+", "+doc.published+", "+doc.pages+" pages, "+doc.url+"), cited as \u201C"+ca+"\u201D. Use ONLY these verified takeaways with their ready-made pins, copied exactly:\n"+JSON.stringify(tk)+"\n\nFollow the source-page anatomy: "+anatomy+". Return JSON {\"one_liner\":\"...\",\"body\":\"markdown, at most 900 words, only the pins given, copied exactly\",\"touches\":[{\"slug\":\"existing wiki slug\",\"why\":\"...\"}]}."+PIN_RULE,0,ingProgEl());
    const body=String(r.body||"");
    const pins=parsePins(body);
    const ver=pins.filter(p=>verifyPin(p).ok).length;
    const stub=slugMap.get("a-hrc-57-61");
    const regs=stub&&stub.frontmatter.register||["c"];
    let touches=(r.touches||[]).map(t=>t.slug).filter(s=>slugMap.has(s)||ing.newSlugs.includes(s));
    touches=[...new Set(touches)];touches.push("a-hrc-57-61");touches=touches.slice(0,12);
    const links=[...new Set(bodyLinks(body))].filter(s=>slugMap.has(s)||ing.newSlugs.includes(s));
    const page={slug:"a-hrc-57-61",type:"source",title:doc.title,frontmatter:{title:doc.title,type:"source",tags:touches,register:regs,status:"draft",updated:today(),links,sources:[doc.id]},body:"\u0002"+body+"\u0003",isNew:false,edited:true};
    ing.sourceDraft=page;ing.sourcePins=pins;ing.sourceVer=ver;
    document.getElementById("srcdraft").innerHTML='<p class="hint">Draft received: '+pins.length+" pins, "+ver+" verified, "+(pins.length-ver)+' not found (shown in the review step).</p>';
    document.getElementById("touchedbtn").hidden=false;
    document.getElementById("drafttouch").dataset.slugs=JSON.stringify(touches);
    document.getElementById("drafttouch").onclick=draftTouched;
  }catch(err){
    btn.disabled=false;
    document.getElementById("srcdraft").innerHTML='<div class="greybox"><p class="noteflag">Could not parse the draft.</p><pre style="white-space:pre-wrap;font:12px var(--mono)">'+esc(err.raw||"")+'</pre><button type="button" class="quiet" id="srcretry">Retry</button></div>';
    document.getElementById("srcretry").onclick=draftSource;
  }
}
async function draftTouched(){
  S.stop=false;const btn=document.getElementById("drafttouch");btn.disabled=true;
  const slugs=JSON.parse(btn.dataset.slugs);
  ing.changes=[{page:ing.sourceDraft,kind:"new page"=== "new page"?"new page":"edited",pins:ing.sourcePins,ins:1}];
  ing.changes=[];
  const srcChange={page:ing.sourceDraft,kind:"new page",pins:ing.sourcePins,inserted:1};
  let i=0;
  for(const slug of slugs){
    if(S.stop)break;
    i++;ingProg("touched page "+i+" of "+slugs.length+" · "+slug);
    const tks=ing.takeaways.filter(t=>t.pages.includes(slug));
    const p=slugMap.get(slug);
    if(!p&&ing.newSlugs.includes(slug)){
      const np={slug,type:"concept",title:slug.replace(/-/g," "),frontmatter:{title:slug.replace(/-/g," "),type:"concept",tags:[],register:["c"],status:"draft",updated:today(),links:[],sources:[]},body:"\u0002# "+slug.replace(/-/g," ")+"\u0003",isNew:true};
      slugMap.set(slug,np);P.push(np);
      ing.changes.push({page:np,kind:"new page",pins:[],inserted:1});
      continue;
    }
    if(!p)continue;
    try{
      const r=await askModel("You edit one page of a research wiki to take account of a newly ingested document, "+ing.doc.title+". The page "+p.slug+":\n\n"+p.body+"\n\nThe new document's takeaways that bear on this page (with their ready-made pins, copied exactly):\n"+JSON.stringify(tks.map(t=>({claim:t.claim,pin:pinMarkdown(ing.doc,t.x,t.quote)})))+"\n\nReturn JSON {\"edits\":[{\"after\":\"an existing heading on the page, or 'end'\",\"markdown\":\"...\"}],\"contested\":\"a full fenced ```contested block, only where this document disagrees with the page, else empty\"}. At most 300 words in all; pins copied exactly."+PIN_RULE,0,ingProgEl());
      let body=p.body;
      const md=(r.edits||[]).map(e=>String(e.markdown||"")).filter(Boolean);
      for(const e of (r.edits||[])){
        if(!e.markdown)continue;
        body=insertAfterHeading(body,String(e.after||"end"),"\u0002"+e.markdown+"\u0003");
      }
      if(r.contested&&/```contested/.test(r.contested)){
        body+="\n\n"+r.contested;
        ing.tensions.push({slug:slug,block:r.contested});
      }
      const fm=JSON.parse(JSON.stringify(p.frontmatter));
      fm.sources=[...new Set([...(fm.sources||[]),ing.doc.id])];
      fm.links=[...new Set([...(fm.links||[]),...bodyLinks(body),"a-hrc-57-61"])].filter(s=>slugMap.has(s)||ing.newSlugs.includes(s));
      fm.updated=today();
      const np=Object.assign({},p,{body,frontmatter:fm,_pins:null,_bl:null});
      const pins=parsePins(body);
      const oldPinKeys=new Set(pagePins(p).map(x=>x.id+"#"+x.page+"|"+norm(x.quote)));
      const newPins=pins.filter(x=>!oldPinKeys.has(x.id+"#"+x.page+"|"+norm(x.quote)));
      ing.changes.push({page:np,kind:"edited",pins:newPins,inserted:md.length,orig:p});
    }catch(err){
      ing.changes.push({page:p,kind:"edited",pins:[],inserted:0,error:err.raw});
    }
  }
  ing.changes.unshift(srcChange);
  document.getElementById("touchdraft").innerHTML='<p class="hint">Drafts received: '+ing.changes.length+" change cards. Step 4 below.</p>";
  ingProg("step 3 done");
  renderReview();
}
function insertAfterHeading(body,heading,md){
  const lines=body.split("\n");let idx=-1;
  for(let i=0;i<lines.length;i++){const m=lines[i].match(/^(#{1,3})\s+(.*)$/);if(m&&m[2].trim()===String(heading).trim()){idx=i;break;}}
  if(idx<0||String(heading).trim()==="end")return body+"\n\n"+md+"\n<!-- inserted at end"+(idx<0?" (heading not found)":"")+" -->";
  const lvl=lines[idx].match(/^#+/)[0].length;
  let j=idx+1;while(j<lines.length){const m=lines[j].match(/^(#{1,3})\s/);if(m&&m[1].length<=lvl)break;j++;}
  return lines.slice(0,j).join("\n")+"\n"+md+"\n"+lines.slice(j).join("\n");
}
function renderReview(){
  ing.cursor=0;
  document.getElementById("ingbody").insertAdjacentHTML("beforeend",'<div class="step"><h3>Step 4 · review and file</h3><div id="rev"></div><div id="revfile"></div></div>');
  showChange();
}
function showChange(){
  const rev=document.getElementById("rev");
  const c=ing.changes[ing.cursor];
  if(!c){finishReview();return;}
  const ver=c.pins.filter(p=>verifyPin(p).ok).length;
  rev.innerHTML='<fieldset><legend>change '+(ing.cursor+1)+" of "+ing.changes.length+" · "+esc(c.page.title)+" · "+esc(c.page.type)+" · "+c.kind+"</legend>"
   +'<p class="hint">'+c.inserted+" paragraph"+(c.inserted===1?"":"s")+" inserted · "+c.pins.length+" pins added ("+ver+" verified, "+(c.pins.length-ver)+" not)</p>"
   +(c.error?'<pre style="white-space:pre-wrap;font:12px var(--mono)">'+esc(c.error)+"</pre>":"")
   +'<div class="pagebody">'+renderBody(c.page.body,{slug:c.page.slug})+"</div>"
   +'<span class="hint">Inserted paragraphs on pale yellow; the rest grey is the page as loaded.</span>'
   +'<div style="margin:.6rem 0"><button type="button" class="act" id="appr">Approve change '+(ing.cursor+1)+" of "+ing.changes.length+'</button> <button type="button" class="quiet" id="rej">Reject this page</button></div></fieldset>';
  document.getElementById("appr").onclick=()=>{c.approved=true;ing.cursor++;showChange();};
  document.getElementById("rej").onclick=()=>{c.approved=false;ing.cursor++;showChange();};
}
function finishReview(){
  const approved=ing.changes.filter(c=>c.approved);
  document.getElementById("revfile").innerHTML='<p><button type="button" class="act" id="fileall">File the approved changes ('+approved.length+' of '+ing.changes.length+")</button></p>";
  document.getElementById("fileall").onclick=()=>{
    const doc=ing.doc,ca=citeAs(doc),regs=docRegister(doc.id)[0];
    const written=[];
    for(const c of ing.changes){
      if(!c.approved)continue;
      const idx=P.findIndex(p=>p.slug===c.page.slug);
      const clean=Object.assign({},c.page,{body:c.page.body.replace(/\u0002|\u0003/g,""),_pins:null,_bl:null});
      clean.frontmatter.updated=today();
      if(idx>=0)P[idx]=clean;else P.push(clean);
      slugMap.set(clean.slug,clean);
      written.push(clean.slug);
      S.changedPages.push(clean.slug);
    }
    if(!written.includes("a-hrc-57-61")){}else{}
    // index
    const stubLine="- [[a-hrc-57-61]] — "+doc.title+" · ("+regs+") · \u2713"+(ing.sourceVer||0);
    W.index=insertIndexLine(W.index,"a-hrc-57-61",stubLine,"Sources");
    for(const c of ing.changes){
      if(!c.approved)continue;
      const pins=pagePins(slugMap.get(c.page.slug));
      const ver=pins.filter(p=>verifyPin(p).ok).length;
      const t=totals();W.index=W.index.replace(/(\d[\d,]*) pins/,t.pins+" pins");
      const re=new RegExp("- \\[\\["+c.page.slug+"\\]\\][^\\n]*");
      const line="- [["+c.page.slug+"]] — "+c.page.title+" · ("+((c.page.frontmatter.register||[]).join("")||"?")+") · \u2713"+ver;
      if(re.test(W.index))W.index=W.index.replace(re,line);else W.index=insertIndexLine(W.index,c.page.slug,line,c.page.type+"s");
    }
    const t=totals();W.index=W.index.replace(/(\d[\d,]*) pins/,t.pins+" pins");
    // doc status
    doc.status="ingested";vCache.clear();
    // log
    const rejected=ing.changes.filter(c=>!c.approved).map(c=>c.page.slug);
    let k=0;const pinners=[];
    for(const p of P){if(written.includes(p.slug))continue;if(pagePins(p).some(x=>x.id===doc.id)){k++;pinners.push("[["+p.slug+"]]");}}
    const entry="## ["+today()+"] ingest | "+(doc.symbol||doc.short_title)+": "+doc.short_title+"\nRead "+doc.passages.length+" passages ("+ca+", register ("+regs+")). Wrote [[a-hrc-57-61]]. "+(ing.sourceVer||0)+" pins in all; besides its own page, pinned on "+k+" pages: "+pinners.join(", ")+". Rejected: "+(rejected.length?rejected.map(s=>"[["+s+"]]").join(", "):"none")+".";
    W.log+=(W.log.endsWith("\n")?"":"\n")+"\n"+entry;
    S.logAdded.push(entry);S.changes++;
    // tensions
    for(const tn of ing.tensions){
      const c=parseContested(tn.block.replace(/```contested\n?|```/g,""));
      const tslug=c.claim.toLowerCase().replace(/[^a-z0-9]+/g,"-").replace(/^-|-$/g,"").slice(0,60);
      const status=/^contested/.test(c.verdict)?"open":/^leans/.test(c.verdict)?"leaning":"settled";
      const poles=[...new Set(c.positions.map(p=>p.parts[1]))].join(", ");
      W.tensions+="\n### "+tslug+"\n"+c.claim+"\nstatus: "+status+"\ncard: [["+tn.slug+"]]\npoles: "+poles+"\nwhere: "+c.positions.map(p=>(p.parts[4]||"").replace(/\[\[|\]\]/g,"")).join(", ")+"\n";
      S.newTensions.push(tslug);
    }
    ing=null;updateHeader();
    document.getElementById("revfile").innerHTML='<p class="lint-pass" role="status">Filed. '+written.length+" page(s) written: "+written.map(s=>"[["+s+"]]").join(", ")+". The document is now marked ingested in this session; Lint re-runs on tab 04; download on tab 05.</p>";
    renderCheck();
  };
}
function setTabRun(n,on){
  const t=document.getElementById("tab-"+n);
  t.innerHTML=on?'0'+n+' INGEST · <span class="run" aria-live="polite">running</span>':"0"+n+" INGEST";
}

/* ---------- 04 CHECK ---------- */
function tensionsEntries(){
  return (W.tensions.match(/^### .*$/gm)||[]).map(l=>l.slice(4).trim());
}
function tensionsHasCard(slug){
  if(!slug)return false;
  return W.tensions.includes("card: [[")+slug+"]]";
}
function runLint(){
  const back=backlinkMap();
  const checks=[];
  const add=(name,pages,note)=>checks.push({name,pages:pages,note});
  // dangling
  const dang=[];for(const p of P)for(const s of pageBodyLinks(p))if(!slugMap.has(s))dang.push(p.slug+" → "+s);
  add("dangling links",dang);
  // orphans
  const orph=P.filter(p=>!(back.get(p.slug)>0)&&pageBodyLinks(p).length===0).map(p=>p.slug);
  add("orphan pages",orph);
  // pins not verified
  const unv=[],badmark=[];
  for(const p of P)for(const pin of pagePins(p)){const v=verifyPin(pin);if(!v.ok)unv.push(p.slug+" ("+pin.label+")");if(pin.mark==="\u2713"&&!v.ok)badmark.push(p.slug);}
  add("pins not verified by the code",unv);
  add("pins marked ✓ that fail",badmark);
  // sources vs pinned
  const src=[];
  for(const p of P){const pinned=[...new Set(pagePins(p).map(x=>x.id))];const s=p.frontmatter.sources||[];if(JSON.stringify([...s].sort())!==JSON.stringify(pinned.sort()))src.push(p.slug);}
  add("`sources` differ from the documents pinned",src);
  add("pages with no pins",P.filter(p=>pagePins(p).length===0).map(p=>p.slug));
  const recip=[];
  for(const p of P){const bl=new Set(pageBodyLinks(p));const fl=new Set(p.frontmatter.links||[]);for(const s of fl)if(!bl.has(s)){recip.push(p.slug);break;}for(const s of bl)if(!fl.has(s)){if(!recip.includes(p.slug))recip.push(p.slug);break;}}
  add("`links` not reciprocated (frontmatter vs body)",recip);
  const idxSlugs=[...W.index.matchAll(/\[\[([^\]|#]+)/g)].map(m=>m[1]);
  add("pages missing from the index",P.filter(p=>!idxSlugs.includes(p.slug)).map(p=>p.slug));
  add("index lines without a page",idxSlugs.filter(s=>!slugMap.has(s)));
  const idxN=[];
  for(const m of W.index.matchAll(/- \[\[([^\]|#]+)\]\][^\n]*\u2713(\d+)/g)){
    const p=slugMap.get(m[1]);if(!p)continue;
    const ver=pagePins(p).filter(x=>verifyPin(x).ok).length;
    if(+m[2]!==ver)idxN.push(m[1]+" (index "+m[2]+", computed "+ver+")");
  }
  add("index ✓N differs from the computed count",idxN);
  const bodyCards=new Set();
  for(const p of P){const re=/```contested/g;let m;while((m=re.exec(p.body)))bodyCards.add(p.slug);}
  const tensCards=tensionsEntries();
  const cardsNoTens=[...bodyCards].filter(s=>!tensCards.some(t=>W.tensions.includes("card: [["+s+"]]")));
  const tensNoCard=tensCards.filter(t=>{const seg=W.tensions.split("### "+t)[1]||"";const card=(seg.match(/card: \[\[([^\]]+)\]\]/)||[])[1];return !card||!bodyCards.has(card);});
  add("contested cards without a tensions entry",cardsNoTens);
  add("tensions entries without a card",tensNoCard);
  add("stub pages",P.filter(p=>p.frontmatter.status==="stub").map(p=>p.slug));
  const inboxPins=[];
  for(const p of P)for(const pin of pagePins(p))if(docMap.get(pin.id)&&docMap.get(pin.id).status==="inbox")inboxPins.push(p.slug);
  add("pins to a document still in the inbox",inboxPins);
  return checks;
}
function renderCheck(){
  const t=totals();
  document.getElementById("ck-big").textContent=t.ver+" of "+t.pins;
  const checks=runLint();
  const n=checks.filter(c=>c.pages.length).length;
  document.getElementById("ck-lintn").textContent=n+" lint checks need a look";
  let h='<table><caption>FIG.04 · lint · '+checks.length+" checks · counting and matching by this page's code</caption><thead><tr><th>Check</th><th class=\"num\">Count</th><th>Result</th><th>Pages</th></tr></thead><tbody>";
  for(const c of checks){
    h+="<tr><td>"+esc(c.name)+"</td><td class=\"num\">"+c.pages.length+"</td><td>"+(c.pages.length?'<span class="lint-check">check</span>':'<span class="lint-pass">pass</span>')+"</td><td>"+c.pages.slice(0,12).map(x=>{const slug=x.split(" ")[0].replace("→","").trim();return slugMap.has(slug)?wikiLink(slug):esc(x);}).join(" · ")+(c.pages.length>12?" …":"")+"</td></tr>";
  }
  h+="</tbody></table>";
  h+='<span class="hint">The schema\u2019s reading for contradictions is not done by code: contested claims are read by a person on the page.</span>';
  document.getElementById("lintout").innerHTML=h;
  document.getElementById("ck-top").innerHTML='<div class="greybox"><strong>How the app checks itself.</strong> Pins found by the regular expression are compared with the number stated in the first line of the index ('+t.pins+" found here). Every pin is verified against the library passages after normalisation; labels must match the passage's paragraph or printed page. Structure: dangling links, orphans, sources vs pinned documents, index coverage, contested cards vs the tensions register. Model answers: JSON parsed, slugs checked, takeaways returned = verified + failed. Coverage: passages sent equal the document's passages. Unverified: after an ingest the ⚠ count must be unchanged and every pin in a changed page verifies. Approval: pages changed equal approved cards; the log lists approved and rejected slugs. Filing: index line counts equal computed pins; Lint re-runs before and after. Session: changes equal log entries added; the download's page count equals "+P.length+".</div>";
  document.getElementById("lintbtn").textContent="Re-run";
}
document.getElementById("lintbtn").onclick=renderCheck;

/* ---------- 05 RECORD ---------- */
let logNewest=true;
function renderRecord(){
  const entries=(W.log.match(/^## \[.*$/gm)||[]);
  const blocks=[];let rest=W.log;
  for(const e of entries){const i=rest.indexOf(e);const head=rest.slice(0,i);rest=rest.slice(i);const j=rest.indexOf("\n## [",1);const blk=j<0?rest:rest.slice(0,j);blocks.push({head:e,block:blk});rest=j<0?"":rest.slice(j);if(head.trim())blocks[blocks.length-1].pre=head;}
  const ordered=logNewest?blocks.slice().reverse():blocks;
  let h="";
  for(const b of ordered){
    const sess=S.logAdded.some(e=>e.split("\n")[0]===b.head);
    h+="<details"+(sess?" open":"")+"><summary>"+esc(b.head)+(sess?' <span class="session">this session</span>':"")+"</summary><div class=\"pagebody\">"+renderBody(b.block.replace(b.head,"").trim(),{})+"</div></details>";
  }
  document.getElementById("logout").innerHTML=h||"<p class='hint'>The log is empty.</p>";
  // tensions
  const tens=W.tensions.split(/(?=^### )/m).filter(s=>s.trim());
  let th=tens.map(t=>{
    const title=(t.match(/^### (.*)$/m)||[])[1]||"";
    const card=(t.match(/card: \[\[([^\]]+)\]\]/)||[])[1];
    return "<div class=\"step\"><h3>"+esc(title)+"</h3><div class=\"pagebody\">"+renderBody(t.replace(/^### .*$/m,"").trim(),{})+"</div>"+(card?wikiLink(card):"")+"</div>";
  }).join("");
  document.getElementById("tensout").innerHTML=th||"<p class='hint'>No tensions recorded.</p>";
  document.getElementById("dlpages").hidden=!S.changedPages.length;
}
document.getElementById("logorder").onclick=e=>{logNewest=!logNewest;e.target.textContent="Order: "+(logNewest?"newest first":"oldest first");renderRecord();};
document.getElementById("dlwiki").onclick=()=>{
  const out={title:W.title,source:W.source,built:W.built,count:P.length,pages:P,index:W.index,log:W.log,tensions:W.tensions,schema:W.schema,
    changes:S.changedPages.map(s=>({slug:s,date:today()})),library_status:Object.fromEntries(D.map(d=>[d.id,d.status]))};
  saveFile("wiki-"+today()+".json",JSON.stringify(out,null,2),"application/json");
};
document.getElementById("dlpages").onclick=()=>{
  const md=S.changedPages.map(s=>{const p=slugMap.get(s);return "---\nslug: "+s+"\n---\n\n"+p.body;}).join("\n\n---\n\n");
  saveFile("wiki-changed-pages-"+today()+".md",md,"text/markdown");
};
function saveFile(name,content,type){
  const b=new Blob([content],{type});const a=document.createElement("a");
  a.href=URL.createObjectURL(b);a.download=name;document.body.appendChild(a);a.click();
  setTimeout(()=>{URL.revokeObjectURL(a.href);a.remove();},0);
}

/* ---------- init ---------- */
renderIngestStart();
showIndex();
renderCheck();
updateHeader();
tabs[0].focus();
if(location.hash){const s=location.hash.slice(1);if(slugMap.has(s))showPage(s);}
window.addEventListener("hashchange",()=>{const s=location.hash.slice(1);if(slugMap.has(s)){setTab(1);showPage(s);}});
</script>
</body>
</html>
```