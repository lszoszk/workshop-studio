I built the full five-tab workspace: pages with verified pins and contested cards, Ask with two announced model calls and filing, the four-step ingest with per-claim verification and approve/reject review, the lint tab, and the record/download tab — all counting and verification done by the page's own code.

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Research wiki · neurotechnology and justice</title>
<style>
:root{--paper:#f4f0e8;--ink:#1d1b18;--rule:#d9d2c3;--red:#9b2335;--green:#1a7f37;--amber:#9a6700;--grey:#6f6a60;--yellow:#fbf0c4}
*{box-sizing:border-box}
[hidden]{display:none!important}
body{margin:0;background:var(--paper);color:var(--ink);font:16px/1.55 -apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;padding:0 20px 56px}
.mono{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:11.5px;letter-spacing:.08em;text-transform:uppercase}
.serif{font-family:Georgia,"Times New Roman",serif}
a{color:var(--red)}
button{font:inherit;cursor:pointer;color:inherit}
:focus-visible{outline:3px solid var(--red);outline-offset:2px}
header.top{display:flex;justify-content:space-between;gap:24px;align-items:flex-end;flex-wrap:wrap;border-bottom:1px solid var(--rule);padding:16px 0 12px}
.kicker{color:var(--red)}
nh1{}
h1.title{font-family:Georgia,serif;font-weight:normal;font-size:29px;margin:2px 0 4px}
.dataline{color:var(--grey);font-size:14px}
.counters{text-align:right;color:var(--grey)}
.counters .warnline{color:var(--ink)}
nav.tabs{display:flex;gap:2px;border-bottom:1px solid var(--rule);margin-bottom:18px;flex-wrap:wrap}
nav.tabs [role=tab]{border:none;background:none;padding:10px 14px;font-family:ui-monospace,Menlo,Consolas,monospace;font-size:12px;letter-spacing:.1em;color:var(--grey);border-bottom:2px solid transparent}
nav.tabs [role=tab][aria-selected=true]{color:var(--red);border-bottom-color:var(--red)}
.runmark{color:var(--red)}
.cols{display:flex;gap:24px;align-items:flex-start}
.rail{width:320px;flex:none;border-right:1px solid var(--rule);padding-right:16px}
.main{flex:1;max-width:900px;min-width:0}
@media(max-width:900px){.cols{flex-direction:column}.rail{width:100%;border-right:none;border-bottom:1px solid var(--rule);padding:0 0 12px}}
.bignum{font-family:Georgia,serif;font-size:44px;line-height:1.1;margin:8px 0 2px}
.hint{color:var(--grey);text-transform:none;letter-spacing:.03em;margin-bottom:10px}
.grouplabel{color:var(--grey);border-bottom:1px solid var(--rule);padding:10px 0 4px;margin-top:8px}
.pagelink{display:block;width:100%;text-align:left;background:none;border:none;border-top:1px solid var(--rule);padding:6px 2px}
.pagelink:hover .ptitle{color:var(--red)}
.ptitle{display:block}
.meta{color:var(--grey);font-family:ui-monospace,Menlo,Consolas,monospace;font-size:11px;letter-spacing:.05em}
input[type=text],input[type=search],textarea{width:100%;border:1px solid var(--rule);background:#fffdf8;padding:8px;font:inherit;color:var(--ink);border-radius:2px}
textarea{min-height:110px}
label{display:block;font-family:ui-monospace,Menlo,Consolas,monospace;font-size:11.5px;letter-spacing:.08em;text-transform:uppercase;color:var(--grey);margin:12px 0 4px}
.btn{border:1px solid var(--ink);background:transparent;padding:6px 12px;font-family:ui-monospace,Menlo,Consolas,monospace;font-size:11.5px;letter-spacing:.08em;text-transform:uppercase;border-radius:2px;margin:4px 6px 4px 0}
.btn:hover{border-color:var(--red);color:var(--red)}
.btn.primary{background:var(--red);border-color:var(--red);color:#fff}
.btn.primary:hover{color:#fff;opacity:.9}
.btn:disabled{opacity:.45;cursor:not-allowed}
.btn.small{padding:2px 8px;font-size:10.5px}
.card{border:1px solid var(--rule);border-radius:2px;padding:14px 16px;margin:14px 0;background:#faf7f0}
fieldset.card{font:inherit}
legend{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:11.5px;letter-spacing:.08em;text-transform:uppercase;color:var(--red);padding:0 6px}
.ok{color:var(--green)} .warn{color:var(--amber)} .bad{color:var(--red)} .pass{color:var(--green)}
.pinquote{font-family:Georgia,serif}
.chip{display:inline-flex;align-items:center;gap:4px;border:1px solid var(--rule);border-radius:999px;padding:0 6px;margin:0 3px;vertical-align:middle;background:#fffdf8;white-space:nowrap}
.chipbtn{border:none;background:none;font-family:ui-monospace,Menlo,Consolas,monospace;font-size:11px;color:var(--red);text-decoration:underline;padding:2px}
.reg{color:var(--ink);border-left:1px solid var(--rule);padding-left:5px}
.expbtn{border:none;background:none;font-size:11px;padding:0 2px;color:var(--grey)}
.pindetail{display:block;border-left:2px solid var(--rule);margin:4px 0 10px 14px;padding:4px 12px;font-size:14px}
.struck{text-decoration:line-through;opacity:.7}
.contested{border-left:4px solid var(--red)}
.verdict{font-size:34px;color:var(--red);margin:2px 0 8px}
.leanbar{height:10px;background:var(--rule);margin:6px 0 12px;max-width:520px}
.leanbar div{height:100%;background:var(--red)}
.fig{color:var(--grey);margin:10px 0 4px}
table{width:100%;border-collapse:collapse;margin:10px 0}
caption{text-align:left;padding:4px 0;color:var(--grey);font-family:ui-monospace,Menlo,Consolas,monospace;font-size:11px;letter-spacing:.08em;text-transform:uppercase}
th{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:11px;text-transform:uppercase;letter-spacing:.08em;text-align:left;border-bottom:1px solid var(--ink);padding:4px 10px 4px 0}
td{border-top:1px solid var(--rule);padding:6px 10px 6px 0;vertical-align:top}
td.num,th.num{text-align:right}
.ins{background:var(--yellow);border-left:3px solid var(--red);padding-left:8px}
.dim{color:var(--grey)}
.tag{border:1px solid var(--rule);border-radius:999px;padding:0 8px;margin:0 4px 0 0;color:var(--grey)}
.badges{margin:6px 0}
.tags{margin:4px 0 12px}
.pagebody h1{font-family:Georgia,serif;font-weight:normal;font-size:26px;margin:18px 0 6px}
.pagebody h2{font-family:Georgia,serif;font-weight:normal;font-size:21px;margin:16px 0 6px;border-bottom:1px solid var(--rule);padding-bottom:3px}
.pagebody h3{font-family:Georgia,serif;font-weight:normal;font-size:17px;margin:14px 0 4px}
.pagebody ul,.pagebody ol{margin:6px 0;padding-left:24px}
.pagebody p{margin:8px 0}
pre{background:#ece7db;padding:10px;overflow:auto;font-size:12.5px}
.sendnote{background:#e9e3d6;border:1px solid var(--rule);padding:10px 12px;margin:10px 0;color:var(--ink)}
.progress{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:12px;color:var(--red);margin:8px 0;min-height:1.2em}
.sess{color:var(--red);border:1px solid var(--red);border-radius:999px;padding:0 6px;font-size:10px}
details{margin:8px 0}
summary{cursor:pointer;font-family:ui-monospace,Menlo,Consolas,monospace;font-size:11.5px;letter-spacing:.08em;text-transform:uppercase;color:var(--grey)}
footer{border-top:1px solid var(--rule);margin-top:28px;padding-top:10px;color:var(--grey);font-family:ui-monospace,Menlo,Consolas,monospace;font-size:11px;letter-spacing:.05em}
[data-source=ai]{border:1px dashed var(--red);padding:4px 14px 10px;margin:10px 0;background:#faf5ee}
.aitag{color:var(--red)}
</style>
</head>
<body>
<header class="top">
  <div>
    <div class="mono kicker">WIKI · neurotechnology and justice</div>
    <h1 class="title">Research wiki: neurotechnology in the administration of justice</h1>
    <div class="dataline" id="dataline"></div>
  </div>
  <div class="counters mono">
    <div>Changes this session: <span id="cChanges">0</span> · Calls to the model: <span id="cCalls">0</span> · Passages that left the browser: <span id="cPass">0</span></div>
    <div class="warnline">This page has no storage: changes live in it until you download them (tab 05)</div>
  </div>
</header>
<nav class="tabs" role="tablist" aria-label="App sections" id="tablist">
  <button role="tab" id="tabbtn-pages" aria-controls="tab-pages" aria-selected="true" data-tab="pages">01 PAGES</button>
  <button role="tab" id="tabbtn-ask" aria-controls="tab-ask" aria-selected="false" data-tab="ask" tabindex="-1">02 ASK</button>
  <button role="tab" id="tabbtn-ingest" aria-controls="tab-ingest" aria-selected="false" data-tab="ingest" tabindex="-1">03 INGEST <span class="runmark" aria-live="polite" id="runmark"></span></button>
  <button role="tab" id="tabbtn-check" aria-controls="tab-check" aria-selected="false" data-tab="check" tabindex="-1">04 CHECK</button>
  <button role="tab" id="tabbtn-record" aria-controls="tab-record" aria-selected="false" data-tab="record" tabindex="-1">05 RECORD</button>
</nav>
<main>
  <section id="tab-pages" role="tabpanel" aria-labelledby="tabbtn-pages">
    <div class="cols">
      <aside class="rail">
        <label for="pagefilter">title, tag or slug</label>
        <input type="search" id="pagefilter" placeholder="filter pages">
        <div class="bignum" id="pagecount"></div>
        <div class="mono hint">computed by this page's code · click a page to open it</div>
        <div id="pagelist"></div>
      </aside>
      <div class="main" id="pageview"></div>
    </div>
  </section>
  <section id="tab-ask" role="tabpanel" aria-labelledby="tabbtn-ask" hidden>
    <div class="sendnote" id="sendnote">Nothing has been sent yet. Step 1 will send the index and your question; step 2 will send the chosen pages' bodies and your question. No library passages leave the browser in either step.</div>
    <label for="qinput">Ask the wiki</label>
    <textarea id="qinput" placeholder="e.g. Can a suspect consent to brain-based lie detection?"></textarea>
    <button class="btn primary" id="askbtn">Ask the wiki</button>
    <div class="progress" id="askprog" aria-live="polite"></div>
    <div id="askresult"></div>
  </section>
  <section id="tab-ingest" role="tabpanel" aria-labelledby="tabbtn-ingest" hidden>
    <div id="ingestHome"></div>
    <div id="ingestRun" hidden>
      <div class="mono" style="color:var(--grey)">calls so far <span id="ingCalls">0</span> · passages sent <span id="ingPass">0</span></div>
      <div class="progress" id="ingProg" aria-live="polite"></div>
      <div id="ingestSteps"></div>
    </div>
  </section>
  <section id="tab-check" role="tabpanel" aria-labelledby="tabbtn-check" hidden>
    <div class="bignum" id="checkBig"></div>
    <div class="mono hint">computed by this page's code from WORKSHOP_DATA.wiki and .library · a failing check never hides a page or a pin</div>
    <div id="checkNeed" style="font-size:18px;margin:6px 0 14px"></div>
    <button class="btn" id="lintBtn">Lint now</button>
    <table id="lintTable"><caption>FIG.01 · lint checks — count · pass / check, with the pages concerned</caption><thead><tr><th scope="col">check</th><th scope="col">result</th><th scope="col">pages</th></tr></thead><tbody></tbody></table>
    <details open id="checksPanel"><summary>How the app checks itself</summary><div id="checksList"></div></details>
  </section>
  <section id="tab-record" role="tabpanel" aria-labelledby="tabbtn-record" hidden>
    <label for="orderSwitch" style="display:inline-block"><input type="checkbox" id="orderSwitch" checked> newest first</label>
    <div id="logView"></div>
    <h2 class="serif">Tensions register</h2>
    <div class="pagebody" id="tensionsView"></div>
    <h2 class="serif">Method and taking it away</h2>
    <p>Counting, filtering, matching and pin verification are done by this page's code, deterministically; every number above has its "how this is computed" line. The model is called only when you press Ask, Ingest or a retry button, and what leaves the browser is announced first. The library is read-only; the index is read before pages; the log is append-only.</p>
    <p class="mono" id="srcLine"></p>
    <button class="btn primary" id="dlWiki">Download the wiki (JSON)</button>
    <button class="btn" id="dlChanged" hidden>Download changed pages (markdown)</button>
  </section>
</main>
<footer id="foot"></footer>
<script>
"use strict";
/* ---------- data ---------- */
const W = window.WORKSHOP_DATA.wiki, L = window.WORKSHOP_DATA.library;
const P = W.pages, D = L.records;
const bySlug = {}, byId = {};
P.forEach(p => bySlug[p.slug] = p); D.forEach(d => byId[d.id] = d);
const PIN_SRC = String.raw`\[([^\]]+)\]\(pin:([^#\s)]+)#p(\d+)(?: "([^"]*)")?\) ?(✓|⚠)`;
const pinsOf = s => [...s.matchAll(new RegExp(PIN_SRC, "g"))].map(m => ({label:m[1], id:m[2], page:+m[3], quote:m[4]||null, mark:m[5], raw:m[0]}));
const REGNAMES = {a:"treaty law", b:"General Comments", c:"UN, agency and soft-law reports", d:"national human rights institution", e:"civil society", f:"scholarship"};
const W8 = {a:5, b:4, c:3, d:2, e:1, f:0.5};
const esc = s => String(s).replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;").replace(/"/g,"&quot;");
const today = new Date().toISOString().slice(0,10);
const kebab = s => String(s).toLowerCase().replace(/[^a-z0-9]+/g,"-").replace(/^-+|-+$/g,"");
function norm(s){ return String(s).normalize("NFKC").replace(/[“”„]/g,'"').replace(/[‘’]/g,"'").replace(/[–—]/g,"-").replace(/\u00ad/g,"").replace(/-\s+/g,"").replace(/\s+/g," ").trim(); }
function parsePage(p){
  p._links = [...p.body.matchAll(/\[\[([^\]|#]+)/g)].map(m => m[1]);
  p._pins = pinsOf(p.body);
  p._contested = (p.body.match(/```contested/g) || []).length;
}
P.forEach(parsePage);
let backlinks = {};
function recomputeBacklinks(){ backlinks = {}; P.forEach(p => p._links.forEach(s => { (backlinks[s] = backlinks[s] || []).push(p.slug); })); }
recomputeBacklinks();
/* ---------- verification ---------- */
function verify(pin){
  const d = byId[pin.id];
  if(!d) return {ok:false, reason:"unknown document"};
  if(!pin.quote) return {ok:false, reason:"the pin carries no quote"};
  if(d.status === "inbox") return {ok:false, reason:"the document is still in the inbox"};
  const frags = pin.quote.split(/…|\.\.\./).map(norm).filter(Boolean);
  for(const x of d.passages.filter(x => x.page === pin.page)){
    const t = norm(x.text); let pos = 0, ok = true;
    for(const f of frags){ const i = t.indexOf(f, pos); if(i < 0){ ok = false; break; } pos = i + f.length; }
    if(!ok) continue;
    const want = x.paragraph ? "para. " + x.paragraph : "p. " + x.page_label;
    if(!pin.label.includes(want)) continue;
    return {ok:true, passage:x};
  }
  return {ok:false, reason:"quote not found on that PDF page"};
}
function docRegister(id){
  const src = P.find(p => p.type === "source" && (p.frontmatter.sources||[]).length === 1 && p.frontmatter.sources[0] === id);
  if(src) return src.frontmatter.register || ["?"];
  const stub = P.find(p => p.frontmatter.status === "stub" && (p.frontmatter.sources||[])[0] === id);
  if(stub) return stub.frontmatter.register || ["?"];
  return ["?"];
}
function citeAs(id){
  const d = byId[id]; if(!d) return id;
  const counts = {};
  P.forEach(p => p._pins.forEach(pin => { if(pin.id === id){ const m = pin.label.match(/^(.*?), (?:para\.|p\.)/); if(m) counts[m[1]] = (counts[m[1]]||0)+1; } }));
  let best = null, bc = 0; for(const k in counts) if(counts[k] > bc){ bc = counts[k]; best = k; }
  return best || d.symbol || ((d.author||"") + " " + (d.year||""));
}
function makePin(id, x, quote){
  let q = String(quote||""), open = true;
  q = q.replace(/"/g, () => { const c = open ? "“" : "”"; open = !open; return c; });
  const loc = x.paragraph ? "para. " + x.paragraph : "p. " + x.page_label;
  const str = `[${citeAs(id)}, ${loc}](pin:${id}#p${x.page} "${q}") ✓`;
  return {str, pin:{label:citeAs(id)+", "+loc, id, page:x.page, quote:q, mark:"✓"}};
}
/* ---------- session counters ---------- */
const S = {changes:0, calls:0, passages:0};
const sessionLogStart = W.log.length;
const sessionChanges = [];
function renderHeader(){
  document.getElementById("cChanges").textContent = S.changes;
  document.getElementById("cCalls").textContent = S.calls;
  document.getElementById("cPass").textContent = S.passages;
  const types = {}; P.forEach(p => types[p.type] = (types[p.type]||0)+1);
  const pins = P.reduce((n,p) => n + p._pins.length, 0);
  const ver = P.reduce((n,p) => n + p._pins.filter(x => verify(x).ok).length, 0);
  const inbox = D.filter(d => d.status === "inbox").length;
  document.getElementById("dataline").textContent =
    `${P.length} pages (${types.source||0} sources, ${types.concept||0} concepts, ${types.entity||0} entities, ${types.question||0} questions) · ${pins} pins, ${ver} verified by this page · ${D.length} documents, ${inbox} in the inbox · built ${W.built}`;
}
/* ---------- model calls ---------- */
let STOP = false;
async function callModel(prompt, passages){
  S.calls++; S.passages += (passages||[]).length; renderHeader();
  let raw;
  try{ raw = await studio.ask(prompt, {json:true}); }
  catch(err){ return {error:String(err), raw:"", json:null, chars:prompt.length}; }
  const txt = String(raw).trim(); let json = null;
  try{ json = JSON.parse(txt); }catch(e){
    const m = txt.match(/```(?:json)?\s*([\s\S]*?)```/);
    if(m){ try{ json = JSON.parse(m[1]); }catch(e2){} }
  }
  return {raw:txt, json, chars:prompt.length, passages:(passages||[]).length};
}
/* ---------- markdown rendering ---------- */
function linkHtml(slug){
  if(bySlug[slug]) return `<a href="#${esc(slug)}" data-slug="${esc(slug)}">${esc(slug)}</a>`;
  return `<a href="#${esc(slug)}" data-slug="${esc(slug)}" class="bad" title="no page">${esc(slug)} (no page)</a>`;
}
function inlineSeg(s){
  let h = esc(s);
  h = h.replace(/\[\[([^\]|#]+)\]\]/g, (m,sl) => linkHtml(sl));
  h = h.replace(/\[([^\]]+)\]\((https?:\/\/[^\s)]+)\)/g, (m,t,u) => `<a href="${u}" target="_blank" rel="noopener">${t}</a>`);
  h = h.replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>");
  h = h.replace(/\*([^*]+)\*/g, "<em>$1</em>");
  return h;
}
function pinHtml(pin, ctx){
  ctx = ctx || {};
  const v = verify(pin);
  const d = byId[pin.id];
  const reg = d ? docRegister(pin.id) : ["?"];
  const regTitle = reg.map(r => r + " " + (REGNAMES[r]||"?")).join(", ");
  let st = v.ok ? `<span class="ok">✓ verified</span>` : `<span class="warn">⚠ not found — ${esc(v.reason)}</span>`;
  let diff = "";
  if(pin.mark === "✓" && !v.ok) diff = ` · <span class="warn">page says ✓</span>`;
  if(pin.mark === "⚠" && v.ok) diff = ` · page says ⚠`;
  let answerNote = "", struck = "";
  if(ctx.answerSet){
    const key = pin.id + "#p" + pin.page + "|" + (pin.quote||"");
    if(!ctx.answerSet.has(key) || !v.ok){ answerNote = ` · <span class="bad">not on the pages sent</span>`; struck = " struck"; }
  }
  const q = ctx.compact ? "" : (pin.quote ? `<span class="pinquote">“${esc(pin.quote)}”</span> ` : `<span class="warn">(pin has no quote)</span> `);
  const btn = `<button class="chipbtn" data-openpin data-id="${esc(pin.id)}" data-page="${pin.page}" data-quote="${esc(pin.quote||"")}" title="Open the PDF at this page with the quote marked">${esc(pin.label)}</button>`;
  let det;
  if(v.ok){
    const x = v.passage;
    det = `<span class="pindetail" hidden><span class="mono">${x.paragraph ? "para. "+esc(x.paragraph) : "p. "+esc(x.page_label)} · PDF p. ${x.page}${x.section ? " · " + esc(x.section) : ""}</span><br>${esc(x.text.slice(0,300))}${x.text.length > 300 ? "…" : ""}<br><button class="btn small" data-openpin data-id="${esc(pin.id)}" data-page="${pin.page}" data-quote="${esc(pin.quote||"")}">Open the PDF page</button></span>`;
  } else {
    det = `<span class="pindetail" hidden><span class="warn">The code could not verify these words: ${esc(v.reason)}. Footnotes, tables and captions are not in the passages, so a pin cannot verify them.</span></span>`;
  }
  return `<span class="pin${struck}">${q}<span class="chip">${btn}<span class="reg mono" title="${esc(regTitle)}">${esc(reg.join(""))}</span>${st}${diff}${answerNote}<button class="expbtn" aria-expanded="false" title="show the passage">▸</button></span>${det}</span>`;
}
function inlineWithPins(s, ctx){
  const re = new RegExp(PIN_SRC, "g"); let out = "", last = 0, m;
  while((m = re.exec(s))){
    out += inlineSeg(s.slice(last, m.index));
    out += pinHtml({label:m[1], id:m[2], page:+m[3], quote:m[4]||null, mark:m[5]}, ctx);
    last = m.index + m[0].length;
  }
  return out + inlineSeg(s.slice(last));
}
function parseContested(buf){
  const o = {positions:[]};
  for(const line of buf){
    if(line.startsWith("claim:")) o.claim = line.slice(6).trim();
    else if(line.startsWith("verdict:")) o.verdict = line.slice(8).trim();
    else if(line.startsWith("note:")) o.note = line.slice(5).trim();
    else if(/^[+~\-] /.test(line)){
      const parts = line.slice(2).split(" | ");
      o.positions.push({sign:line[0], register:(parts[1]||"").trim(), pinRaw:(parts[2]||"").trim(), gloss:(parts[3]||"").trim(), page:(parts[4]||"").trim()});
    }
  }
  return o;
}
function leanOf(o){
  let sup = 0, tot = 0;
  for(const p of o.positions){ const w = W8[p.register] || 0; tot += w; if(p.sign === "+") sup += w; else if(p.sign === "~") sup += w/2; }
  return tot ? sup/tot : 0;
}
function contestedHtml(o, ctx){
  const pct = Math.round(leanOf(o)*100);
  const rows = o.positions.map(p => {
    const pin = pinsOf(p.pinRaw)[0] || {label:p.pinRaw, id:"", page:0, quote:null, mark:"?"};
    const signWord = p.sign === "+" ? "supports" : p.sign === "-" ? "contests" : "mixed";
    const ps = (p.page||"").match(/\[\[([^\]|#]+)\]\]/);
    return `<tr><td>${signWord} (${esc(p.sign)})</td><td class="mono">${esc(p.register||"?")}</td><td>${pinHtml(pin,{compact:true})}</td><td>${esc(p.gloss||"")}</td><td>${ps ? `<a href="#${esc(ps[1])}" data-slug="${esc(ps[1])}">${esc(ps[1])}</a>` : ""}</td></tr>`;
  }).join("");
  const inTensions = ctx && ctx.pageSlug ? W.tensions.includes("card: [[" + ctx.pageSlug + "]]") : false;
  return `<div class="contested card"><div class="mono fig">contested claim</div><h3>${esc(o.claim||"")}</h3>
  <div class="verdict serif">${esc((o.verdict||"").replace(/-/g," "))}</div><p>${esc(o.note||"")}</p>
  <div class="mono fig">FIG.01 · lean bar — descriptive: support ${pct}% of weighted positions · weights a 5 · b 4 · c 3 · d 2 · e 1 · f ½ · the verdict is the answer</div>
  <div class="leanbar" role="img" aria-label="support ${pct}% of weighted positions"><div style="width:${pct}%"></div></div>
  <table><caption>positions — sign · register · pin · gloss · page</caption><thead><tr><th scope="col">sign</th><th scope="col">register</th><th scope="col">pin</th><th scope="col">gloss</th><th scope="col">page</th></tr></thead><tbody>${rows}</tbody></table>
  ${inTensions ? `<p class="mono"><a href="#" data-goto="record">in the tensions register (tab 05)</a></p>` : ""}</div>`;
}
function renderBody(body, ctx){
  ctx = ctx || {};
  const lines = String(body).split("\n");
  let out = "", list = null, para = [], insFlag = false, i = 0;
  const blk = (tag, inner) => {
    const cls = ctx.card ? (insFlag ? ' class="ins"' : ' class="dim"') : "";
    return `<${tag}${cls}>${inner}</${tag}>`;
  };
  const flushPara = () => { if(para.length){ out += blk("p", inlineWithPins(para.join(" "), ctx)); para = []; } };
  const closeList = () => { if(list){ out += `</${list}>`; list = null; } };
  while(i < lines.length){
    const ln = lines[i];
    if(ln.trim() === "<!--INS-->"){ flushPara(); closeList(); insFlag = true; i++; continue; }
    if(ln.trim() === "<!--/INS-->"){ flushPara(); closeList(); insFlag = false; i++; continue; }
    if(ln.trim().startsWith("```")){
      flushPara(); closeList();
      const fence = ln.trim(); const buf = []; i++;
      while(i < lines.length && !lines[i].trim().startsWith("```")){ buf.push(lines[i]); i++; }
      i++;
      out += fence.includes("contested") ? contestedHtml(parseContested(buf), ctx) : `<pre>${esc(buf.join("\n"))}</pre>`;
      continue;
    }
    let m;
    if(m = ln.match(/^###\s+(.*)/)){ flushPara(); closeList(); out += blk("h3", inlineWithPins(m[1], ctx)); }
    else if(m = ln.match(/^##\s+(.*)/)){ flushPara(); closeList(); out += blk("h2", inlineWithPins(m[1], ctx)); }
    else if(m = ln.match(/^#\s+(.*)/)){ flushPara(); closeList(); out += blk("h1", inlineWithPins(m[1], ctx)); }
    else if(m = ln.match(/^\s*-\s+(.*)/)){ flushPara(); if(list !== "ul"){ closeList(); out += "<ul>"; list = "ul"; } out += blk("li", inlineWithPins(m[1], ctx)); }
    else if(m = ln.match(/^\s*\d+\.\s+(.*)/)){ flushPara(); if(list !== "ol"){ closeList(); out += "<ol>"; list = "ol"; } out += blk("li", inlineWithPins(m[1], ctx)); }
    else if(!ln.trim()){ flushPara(); closeList(); }
    else { closeList(); para.push(ln); }
    i++;
  }
  flushPara(); closeList();
  return out;
}
/* ---------- tabs ---------- */
const tabButtons = [...document.querySelectorAll("[role=tab]")];
function showTab(name){
  tabButtons.forEach(b => {
    const on = b.dataset.tab === name;
    b.setAttribute("aria-selected", String(on)); b.tabIndex = on ? 0 : -1;
    document.getElementById("tab-" + b.dataset.tab).hidden = !on;
  });
}
tabButtons.forEach((b, i) => {
  b.addEventListener("click", () => { showTab(b.dataset.tab); b.focus(); });
  b.addEventListener("keydown", e => {
    if(e.key === "ArrowRight" || e.key === "ArrowLeft"){
      e.preventDefault();
      const n = tabButtons[(i + (e.key === "ArrowRight" ? 1 : tabButtons.length - 1)) % tabButtons.length];
      showTab(n.dataset.tab); n.focus();
    }
  });
});
document.addEventListener("keydown", e => { if(e.key === "Escape") STOP = true; });
/* ---------- tab 01: pages ---------- */
const pageview = document.getElementById("pageview");
const pagelist = document.getElementById("pagelist");
const pagefilter = document.getElementById("pagefilter");
function renderPageList(){
  const f = pagefilter.value.trim().toLowerCase();
  const groups = [["source","SOURCES"],["concept","CONCEPTS"],["entity","ENTITIES"],["question","QUESTIONS"]];
  let n = 0, html = "";
  for(const [t, label] of groups){
    const items = P.filter(p => p.type === t && (!f || (p.title + " " + p.slug + " " + (p.frontmatter.tags||[]).join(" ")).toLowerCase().includes(f)));
    if(!items.length) continue;
    n += items.length;
    html += `<div class="grouplabel mono">${label}</div>`;
    for(const p of items){
      const pins = p._pins.length;
      html += `<button class="pagelink" data-openpage="${esc(p.slug)}"><span class="ptitle">${esc(p.title)}</span><span class="meta">${esc((p.frontmatter.register||[]).join(""))} · ${pins} pins${p.frontmatter.status === "stub" ? ' · <span class="warn">stub</span>' : ""}</span></button>`;
    }
  }
  document.getElementById("pagecount").textContent = `${n} of ${P.length} pages`;
  pagelist.innerHTML = html || `<p class="meta">no pages match</p>`;
}
function pageMarkdown(p){
  const fm = p.frontmatter;
  const y = ["title: " + JSON.stringify(p.title), "type: " + fm.type, "tags: [" + (fm.tags||[]).map(t => JSON.stringify(t)).join(", ") + "]",
    "register: [" + (fm.register||[]).join(", ") + "]", "status: " + (fm.status||""), "updated: " + (fm.updated||""),
    "links: [" + (fm.links||[]).join(", ") + "]", "sources: [" + (fm.sources||[]).join(", ") + "]"].join("\n");
  return "---\n" + y + "\n---\n\n" + p.body;
}
function pageHtml(p){
  const fm = p.frontmatter;
  const reg = (fm.register||[]).map(r => `<span class="mono reg" title="${esc(r + " " + (REGNAMES[r]||""))}">${esc(r)}</span>`).join(" ");
  const ver = p._pins.filter(x => verify(x).ok).length;
  const linksOut = (fm.links||[]).map(s => bySlug[s]
    ? `<a href="#${esc(s)}" data-slug="${esc(s)}">${esc(bySlug[s].title)}</a>`
    : `<span class="bad">${esc(s)} (no page)</span>`).join(", ") || "none";
  const fmOnly = (fm.links||[]).filter(s => !p._links.includes(s)).map(s => `<span class="mono">frontmatter only: ${esc(s)}</span>`).join(" ");
  const linkedFrom = (backlinks[p.slug]||[]).map(s => `<a href="#${esc(s)}" data-slug="${esc(s)}">${esc(bySlug[s].title)}</a>`).join(", ") || "none";
  const sources = (fm.sources||[]).map(id => {
    const d = byId[id];
    return d ? `<div>${esc(d.short_title || d.title)} · ${esc(d.kind)} · ${d.year} · <a href="${esc(d.url)}" target="_blank" rel="noopener">document</a>${d.status === "inbox" ? ' · <span class="warn mono">inbox</span>' : ""}</div>`
             : `<div class="bad">${esc(id)} (not in the library)</div>`;
  }).join("") || "<p>none</p>";
  return `<h1 class="serif" style="font-size:30px;font-weight:normal">${esc(p.title)}</h1>
  <div class="badges mono">${esc(p.type)} · ${reg} · ${esc(fm.status||"")} · updated ${esc(fm.updated||"")} · ${p._pins.length} pins (${ver} verified by this page)</div>
  <div class="tags mono">${(fm.tags||[]).map(t => `<span class="tag">#${esc(t)}</span>`).join(" ")}</div>
  <div class="pagebody">${renderBody(p.body, {pageSlug:p.slug})}</div>
  <h2 class="serif">Links out</h2><p>${linksOut}</p>${fmOnly ? `<p>${fmOnly}</p>` : ""}
  <h2 class="serif">Linked from</h2><p>${linkedFrom}</p>
  <h2 class="serif">Sources</h2>${sources}
  <p><button class="btn" id="copyPage">Copy page as markdown</button></p>
  <details id="copyBox" hidden><summary>markdown (frontmatter as YAML, then the body)</summary><textarea readonly rows="16">${esc(pageMarkdown(p))}</textarea></details>`;
}
function renderIndexView(){
  pageview.innerHTML = `<h1 class="serif" style="font-size:30px;font-weight:normal">Index</h1>
  <div class="mono hint">rendered from wiki.index · ${P.length} pages · pin counts recomputed by this page's code</div>
  <div class="pagebody">${renderBody(W.index, {})}</div>`;
}
function showPage(slug){
  const p = bySlug[slug]; if(!p) return;
  showTab("pages");
  pageview.innerHTML = pageHtml(p);
  pageview.scrollTop = 0;
}
pagefilter.addEventListener("input", renderPageList);
pagelist.addEventListener("click", e => {
  const b = e.target.closest("[data-openpage]");
  if(b) location.hash = b.dataset.openpage;
});
pageview.addEventListener("click", e => {
  if(e.target.closest("#copyPage")){
    const box = document.getElementById("copyBox");
    box.hidden = !box.hidden;
    const ta = box.querySelector("textarea");
    ta.focus(); ta.select();
    try{ document.execCommand("copy"); }catch(err){}
  }
});
/* ---------- tab 02: ask ---------- */
const qInput = document.getElementById("qinput"), askBtn = document.getElementById("askbtn"),
      askProg = document.getElementById("askprog"), askResult = document.getElementById("askresult"),
      sendNote = document.getElementById("sendnote");
const ask = {phase:0, slugs:[], sentSet:null, answer:null, title:"", cannot:"", apins:[], allVer:false, regCounts:{}};
function setProg(el, msg){ el.textContent = msg; }
function showRaw(el, r, prompt){
  el.innerHTML = `The model's answer was not valid JSON (${esc(r.error || "parse failure")}). Nothing is filed.<br>
  <button class="btn small" id="retryBtn">Retry (sends the same prompt again)</button>
  <details><summary>raw answer</summary><pre>${esc(r.raw)}</pre></details>`;
  el.querySelector("#retryBtn").onclick = () => callModel(prompt, []).then(r2 => { if(r2.json){ el.textContent = ""; } showRaw(el, r2, prompt); });
}
askBtn.addEventListener("click", async () => {
  const q = qInput.value.trim();
  if(!q){ qInput.focus(); return; }
  askBtn.disabled = true; STOP = false;
  try{
    if(ask.phase === 0){
      ask.answer = null; askResult.innerHTML = "";
      sendNote.textContent = `Step 1 will send: the index (${W.index.length.toLocaleString()} characters) and your question (${q.length} characters). No library passages leave the browser.`;
      setProg(askProg, "Step 1 of 2 · sending the index and the question…");
      const p1 = `You route questions to pages of a research wiki.\nINDEX:\n${W.index}\n\nQUESTION:\n${q}\n\nReturn JSON only: {"pages":["slug",...]} — at most 5 slugs that exist in the index.`;
      const r = await callModel(p1, []);
      if(STOP){ setProg(askProg, "stopped"); return; }
      if(!r.json || !Array.isArray(r.json.pages)){ setProg(askProg, ""); showRaw(askProg, r, p1); return; }
      const dropped = r.json.pages.filter(s => !bySlug[s]);
      ask.slugs = r.json.pages.filter(s => bySlug[s]).slice(0, 5);
      setProg(askProg, `Step 1 done · ${ask.slugs.length} pages chosen${dropped.length ? " · dropped (not in the wiki): " + dropped.join(", ") : ""}`);
      renderSlugChips();
      askBtn.textContent = `Send ${ask.slugs.length} pages to step 2`;
      ask.phase = 1;
    } else {
      await runStep2(q);
      askBtn.textContent = "Ask again"; ask.phase = 0;
    }
  } finally { askBtn.disabled = false; }
});
function renderSlugChips(){
  const chips = ask.slugs.map(s => `<span class="chip"><a href="#${esc(s)}" data-slug="${esc(s)}">${esc(s)}</a></span>`).join(" ");
  askResult.innerHTML = `<p>${chips} <a href="#" id="changePages">Change pages</a></p>
  <div id="pickBox" hidden><p class="mono">tick up to 5 pages</p>${P.map(p => `<label style="text-transform:none;letter-spacing:0;font-family:inherit"><input type="checkbox" value="${esc(p.slug)}" ${ask.slugs.includes(p.slug) ? "checked" : ""}> ${esc(p.title)}</label>`).join("")}</div>`;
  document.getElementById("changePages").onclick = e => { e.preventDefault(); const b = document.getElementById("pickBox"); b.hidden = !b.hidden; };
}
async function runStep2(q){
  const picked = [...document.querySelectorAll("#pickBox input:checked")].map(i => i.value);
  const slugs = (picked.length ? picked : ask.slugs).filter(s => bySlug[s]).slice(0, 5);
  ask.slugs = slugs;
  const bodies = slugs.map(s => `PAGE ${s}:\\n${bySlug[s].body}`).join("\\n\\n---\\n\\n");
  sendNote.textContent = `Step 2 will send: ${slugs.length} pages, ${bodies.length.toLocaleString()} characters, and your question; 0 library passages have left the browser.`;
  setProg(askProg, `Step 2 of 2 · sending ${slugs.length} pages, ${bodies.length.toLocaleString()} characters…`);
  const p2 = `You answer from the pages of a research wiki. Cite every claim with a pin that already stands on one of the pages sent.\nPAGES:\n${bodies}\n\nQUESTION:\n${q}\n\nReturn JSON only: {"title":"...","answer":"...","cannot_answer":"..."}. Answer at most 350 words. Pin syntax: [label](pin:id#pPAGE "quote") ✓ — use the same id, PDF page and quote as a pin on the pages sent; quote only words that stand in the pages given; the code will check. Name the register where it matters — (a) treaty law, (b) General Comments, (c) UN/agency/soft-law reports, (d) national human rights institution, (e) civil society, (f) scholarship; keep each document's own verb; never present (c)–(f) as what the treaty requires.`;
  const r = await callModel(p2, []);
  if(STOP){ setProg(askProg, "stopped"); return; }
  if(!r.json || typeof r.json.answer !== "string"){ setProg(askProg, ""); showRaw(askProg, r, p2); return; }
  ask.title = r.json.title || "Untitled answer";
  ask.answer = r.json.answer; ask.cannot = r.json.cannot_answer || "";
  ask.sentSet = new Set();
  for(const s of slugs) for(const pin of pinsOf(bySlug[s].body)) ask.sentSet.add(pin.id + "#p" + pin.page + "|" + (pin.quote||""));
  ask.apins = pinsOf(ask.answer);
  ask.allVer = ask.apins.length > 0; ask.regCounts = {};
  for(const pin of ask.apins){
    const key = pin.id + "#p" + pin.page + "|" + (pin.quote||"");
    if(ask.sentSet.has(key) && verify(pin).ok){ const g = docRegister(pin.id)[0] || "?"; ask.regCounts[g] = (ask.regCounts[g]||0)+1; }
    else ask.allVer = false;
  }
  renderAnswer();
  setProg(askProg, `Step 2 done · ${r.chars.toLocaleString()} characters sent in this call`);
}
function renderAnswer(){
  const verCount = Object.values(ask.regCounts).reduce((a,b) => a+b, 0);
  const regLine = "abcdef".split("").map(l => `${l} ${ask.regCounts[l]||0}`).join(" · ");
  askResult.innerHTML = `
  <div class="mono aitag">model answer — every pin re-checked by this page's code · ${ask.apins.length} pins, ${verCount} verified</div>
  <div data-source="ai">
    <h2 class="serif" style="font-weight:normal">${esc(ask.title)}</h2>
    <div class="pagebody">${renderBody(ask.answer, {answerSet:ask.sentSet})}</div>
    <h3 class="serif">What the library cannot answer</h3>
    <div class="pagebody">${renderBody(ask.cannot || "—", {})}</div>
  </div>
  <p class="mono">verified pins by register: ${regLine}</p>
  <button class="btn" id="fileAsk">File as a question page</button>
  <div id="fileCard"></div>`;
  document.getElementById("fileAsk").onclick = renderFileCard;
}
function uniqueSlug(base){ let s = base || "page", n = 2; while(bySlug[s]) s = base + "-" + (n++); return s; }
function renderFileCard(){
  const slug = uniqueSlug(kebab(ask.title || "question"));
  const links = [...new Set([...ask.answer.matchAll(/\[\[([^\]|#]+)\]\]/g)].map(m => m[1]))];
  const sources = [...new Set(ask.apins.map(p => p.id))];
  const reg = [...new Set(ask.apins.flatMap(p => docRegister(p.id)))];
  const first = (ask.answer.match(/^[^.!?]*[.!?]/) || [ask.answer.slice(0,120)])[0];
  const body = `# ${ask.title}\\n\\n**Short answer.** ${first}\\n\\n## Reasoning\\n\\n${ask.answer}\\n\\n## What the library cannot answer\\n\\n${ask.cannot || "—"}\\n\\n## Related\\n\\n${links.map(s => "[[" + s + "]]").join(" ") || "none"}`;
  const card = document.getElementById("fileCard");
  card.innerHTML = `<fieldset class="card"><legend>file as a question page</legend>
  <p class="mono">slug <code>${esc(slug)}</code> · type question · status draft · updated ${today} · register ${esc(reg.join("") || "?")} · sources ${esc(sources.join(", ") || "none")} · links ${esc(links.join(", ") || "none")}</p>
  <label for="askTags">tags (comma-separated)</label><input type="text" id="askTags">
  <details open><summary>preview of the page the code builds</summary><div class="pagebody">${renderBody(body, {})}</div></details>
  <button class="btn primary" id="doFile" ${ask.allVer ? "" : "disabled"}>File this page</button>
  ${ask.allVer ? "" : `<span class="warn mono">disabled: ${ask.apins.length === 0 ? "the answer has no pins to verify" : "some pins in the answer do not verify"}</span>`}
  <button class="btn" id="copyAns">Copy answer</button>
  <div class="mono" aria-live="polite" id="filedMsg"></div></fieldset>`;
  document.getElementById("doFile").onclick = () => {
    const page = {slug, type:"question", title:ask.title, frontmatter:{title:ask.title, type:"question", tags:(document.getElementById("askTags").value.split(",").map(s => s.trim()).filter(Boolean)), register:reg, status:"draft", updated:today, links, sources}, body};
    P.push(page); bySlug[slug] = page; parsePage(page); recomputeBacklinks();
    const ver = page._pins.filter(x => verify(x).ok).length;
    W.index += `\\n- [[${slug}]] — ${first.replace(/\\n/g," ")} · (${reg.join("")}) · ✓${ver}`;
    W.log += `\\n\\n## [${today}] ask | ${ask.title}\\n\\nFiled from an Ask answer; ${page._pins.length} pins, ${ver} verified by this page's code.`;
    S.changes++; sessionChanges.push({date:today, kind:"ask", slug});
    renderHeader(); renderPageList(); renderCheck();
    document.getElementById("filedMsg").textContent = `Filed as [[${slug}]] — this session`;
  };
  document.getElementById("copyAns").onclick = () => {
    card.insertAdjacentHTML("beforeend", `<details open><summary>answer markdown</summary><textarea readonly rows="12">${esc(ask.answer)}</textarea></details>`);
  };
}
/* ---------- tab 03: ingest ---------- */
const ingestHome = document.getElementById("ingestHome"), ingestRun = document.getElementById("ingestRun"),
      ingestSteps = document.getElementById("ingestSteps"), ingProg = document.getElementById("ingProg");
let ing = null;
function setRunning(on){ document.getElementById("runmark").textContent = on ? "· running" : ""; }
function renderIngestHome(){
  const inbox = D.filter(d => d.status === "inbox");
  ingestHome.innerHTML = inbox.length
    ? `<p>Documents waiting in the inbox:</p>` + inbox.map(d => `<button class="btn primary" data-ingest="${esc(d.id)}">Ingest ${esc(d.symbol || d.short_title)}</button>`).join("")
    : `<p>Nothing waits in the inbox.</p>`;
}
ingestHome.addEventListener("click", e => {
  const b = e.target.closest("[data-ingest]");
  if(b) startIngest(byId[b.dataset.ingest]);
});
function startIngest(doc){
  const batches = [];
  for(let i = 0; i < doc.passages.length; i += 25) batches.push(doc.passages.slice(i, i+25));
  ing = {doc, batches, ti:0, takeaways:[], failed:[], sentIds:new Set(), changes:[], newSlugs:[], ci:0, stop:false, dropped:0, newContested:[], lintBefore:computeLint()};
  STOP = false; setRunning(true);
  ingestHome.hidden = true; ingestRun.hidden = false;
  const chars = doc.passages.reduce((n,x) => n + x.text.length, 0);
  ingestSteps.innerHTML = `<div class="card"><h2 class="serif" style="font-weight:normal">Step 1 · Scope: the whole document</h2>
  <p>All ${doc.passages.length} passages will be sent, in batches of 25 (${batches.length} calls), ${chars.toLocaleString()} characters; nothing is held back.</p>
  <table><caption>FIG.01 · batches — every passage is sent exactly once</caption><thead><tr><th scope="col">batch</th><th scope="col">paragraphs</th><th scope="col">PDF pages</th><th scope="col" class="num">passages</th></tr></thead><tbody>
  ${batches.map((b,i) => `<tr><td>${i+1}</td><td>${esc(String(b[0].paragraph || b[0].page_label))} – ${esc(String(b[b.length-1].paragraph || b[b.length-1].page_label))}</td><td>${b[0].page}–${b[b.length-1].page}</td><td class="num">${b.length}</td></tr>`).join("")}</tbody></table>
  <button class="btn primary" id="ingStart">Start</button> <button class="btn" id="ingStop" hidden>Stop</button>
  <div id="ingTables"></div><div id="ingStep3"></div><div id="ingReview"></div></div>`;
  document.getElementById("ingStop").onclick = () => { STOP = true; };
  document.getElementById("ingStart").onclick = runBatches;
}
function ingStatus(msg){
  document.getElementById("ingCalls").textContent = S.calls;
  document.getElementById("ingPass").textContent = S.passages;
  setProg(ingProg, msg);
}
function nearestPassage(doc, page, quote){
  const qw = norm(quote).split(" ").filter(Boolean);
  let best = null, bestLen = 0;
  for(const x of doc.passages.filter(x => x.page === page)){
    const tw = norm(x.text).split(" ");
    for(let i = 0; i < qw.length; i++) for(let j = 0; j < tw.length; j++){
      let L = 0;
      while(i+L < qw.length && j+L < tw.length && qw[i+L] === tw[j+L]) L++;
      if(L > bestLen){ bestLen = L; best = x; }
    }
  }
  return {passage:best, run:bestLen};
}
function processTakeaway(t){
  const doc = ing.doc;
  const passage = doc.passages.find(x => x.id === t.passage);
  if(!passage || !ing.sentIds.has(passage.id)){ ing.dropped++; return; }
  const mk = makePin(doc.id, passage, t.quote || "");
  const v = verify(mk.pin);
  const pages = (t.pages || []).filter(s => bySlug[s]);
  for(const s of (t.pages || [])) if(!bySlug[s] && ing.newSlugs.length < 2 && !ing.newSlugs.includes(s)) ing.newSlugs.push(s);
  if(v.ok) ing.takeaways.push({claim:t.claim || "", quote:t.quote || "", passage, pages, pinStr:mk.str});
  else ing.failed.push({claim:t.claim || "", quote:t.quote || "", passage, nearest:nearestPassage(doc, passage.page, t.quote || "")});
}
function renderTakeawayTables(){
  const tt = document.getElementById("ingTables");
  const rows = ing.takeaways.map(t => `<tr><td>${esc(t.claim)}</td><td class="pinquote">“${esc(t.quote)}”</td><td class="mono">${esc(t.passage.paragraph ? "para. "+t.passage.paragraph : "p. "+t.passage.page_label)} · PDF p. ${t.passage.page}</td><td>${t.pages.map(s => `<a href="#${esc(s)}" data-slug="${esc(s)}">${esc(s)}</a>`).join(", ")}</td><td class="ok">✓ verified</td></tr>`).join("");
  const fails = ing.failed.map(f => `<div class="card" style="border-left:3px solid var(--amber)"><p class="pinquote">“${esc(f.quote)}”</p><p class="mono">named passage: ${esc(f.passage.paragraph ? "para. "+f.passage.paragraph : "p. "+f.passage.page_label)} · PDF p. ${f.passage.page}${f.nearest.passage ? ` · nearest passage on that page: ${esc(f.nearest.passage.paragraph ? "para. "+f.nearest.passage.paragraph : "p. "+f.nearest.passage.page_label)} (${f.nearest.run} consecutive words match)` : ""}</p><button class="btn small" data-openpin data-id="${esc(ing.doc.id)}" data-page="${f.passage.page}" data-quote="${esc(f.quote)}">Open the PDF page</button></div>`).join("");
  tt.innerHTML = `<h2 class="serif" style="font-weight:normal">Step 2 · Takeaways</h2>
  <table><caption>FIG.02 · verified takeaways — claim · quote · passage · pages · verification</caption><thead><tr><th scope="col">claim</th><th scope="col">quote</th><th scope="col">passage</th><th scope="col">pages it would touch</th><th scope="col">verification</th></tr></thead><tbody>${rows || `<tr><td colspan="5">none yet</td></tr>`}</tbody></table>
  <div class="card"><strong>Could not verify: ${ing.failed.length}</strong> ${ing.failed.length ? `<p class="mono">these claims are in no change card and in no later prompt</p>${fails}` : ""}</div>`;
}
async function runBatches(){
  document.getElementById("ingStop").hidden = false;
  for(let i = ing.ti; i < ing.batches.length; i++){
    if(STOP) break;
    const b = ing.batches[i];
    b.forEach(x => ing.sentIds.add(x.id));
    ingStatus(`batch ${i+1} of ${ing.batches.length} · ${ing.sentIds.size} of ${ing.doc.passages.length} passages have left the browser`);
    const prompt = `You are reading one document into a research wiki. Every claim must be pinned to a passage with a verbatim quote.\nPassages (JSON, sent now: ${b.length} passages): ${JSON.stringify(b.map(x => ({id:x.id, page:x.page, paragraph:x.paragraph, text:x.text})))}\nIndex of the wiki: ${W.index}\nReturn JSON only: {"takeaways":[{"claim":"...","quote":"8-40 words copied verbatim from ONE passage","passage":"passage id","pages":["slug from the index"]}]} — at most 10 takeaways. Pin syntax: [label](pin:id#pPAGE "quote") ✓. Quote only words that stand in the passages given; the code will check.`;
    const r = await callModel(prompt, b);
    if(r.json && Array.isArray(r.json.takeaways)) r.json.takeaways.forEach(processTakeaway);
    renderTakeawayTables();
  }
  document.getElementById("ingStop").hidden = true;
  ingStatus(`Step 1 done · ${ing.takeaways.length} verified, ${ing.failed.length} could not verify, ${ing.dropped} dropped (passage not sent)`);
  renderStep3();
}
function renderStep3(){
  const stub = P.find(p => p.frontmatter.status === "stub" && (p.frontmatter.sources||[])[0] === ing.doc.id);
  const touched = [...new Set(ing.takeaways.flatMap(t => t.pages))].filter(s => bySlug[s]);
  if(stub && !touched.includes(stub.slug)) touched.push(stub.slug);
  ing.touched = touched;
  document.getElementById("ingStep3").innerHTML = `<h2 class="serif" style="font-weight:normal">Step 3 · Drafts</h2>
  <button class="btn primary" id="draftSrc">Draft the source page (1 call)</button>
  <button class="btn" id="draftTouched" disabled>Draft the changes to ${touched.length} pages (${touched.length} calls)</button>
  <div id="draftProg" class="progress" aria-live="polite"></div><div id="draftOut"></div>`;
  document.getElementById("draftSrc").onclick = draftSource;
  document.getElementById("draftTouched").onclick = draftTouched;
}
async function draftSource(){
  const doc = ing.doc;
  const tks = ing.takeaways.map(t => ({claim:t.claim, pin:t.pinStr}));
  const stub = P.find(p => p.frontmatter.status === "stub" && (p.frontmatter.sources||[])[0] === doc.id);
  const prompt = `Draft the source page for this document in the research wiki.\nDocument: ${JSON.stringify({title:doc.title, author:doc.author, published:doc.published, pages:doc.pages, url:doc.url, symbol:doc.symbol})}\nCite-as: ${citeAs(doc.id)}\nVerified takeaways with ready-made pins: ${JSON.stringify(tks)}\nSource-page anatomy: Full cite, Register, One-liner, Key takeaways, How NOT to read this, Where it feeds the wiki, Related.\nReturn JSON only: {"one_liner":"...","body":"...","touches":[{"slug":"...","why":"..."}]} — body at most 900 words, only the pins given, copied exactly. Pin syntax: [label](pin:id#pPAGE "quote") ✓; quote only words that stand in the passages given; the code will check.`;
  ingStatus("Drafting the source page (1 call)…");
  const r = await callModel(prompt, []);
  const dp = document.getElementById("draftProg");
  if(!r.json || typeof r.json.body !== "string"){ showRaw(dp, r, prompt); return; }
  const body = r.json.body;
  const pins = pinsOf(body);
  const ver = pins.filter(x => verify(x).ok).length;
  let slug = kebab(doc.symbol || doc.id) || kebab(doc.id);
  if(bySlug[slug]) slug += "-source";
  const links = [...new Set([...body.matchAll(/\[\[([^\]|#]+)/g)].map(m => m[1]))];
  const page = {slug, type:"source", title:doc.title, frontmatter:{title:doc.title, type:"source", tags:(r.json.touches||[]).map(t => t.slug), register:stub ? stub.frontmatter.register : docRegister(doc.id), status:"draft", updated:today, links, sources:[doc.id]}, body};
  parsePage(page);
  ing.sourceSlug = slug;
  ing.changes.push({kind:"new", slug, page, inserted:[body], pinAdded:pins.length, ver, notVer:pins.length - ver, approved:null});
  dp.textContent = `Source page drafted: ${pins.length} pins, ${ver} verified, ${pins.length - ver} not verified.`;
  document.getElementById("draftTouched").disabled = false;
}
async function draftTouched(){
  const doc = ing.doc;
  const dp = document.getElementById("draftProg");
  document.getElementById("ingStop").hidden = false;
  for(const slug of ing.touched){
    if(STOP) break;
    const page = bySlug[slug];
    const tks = ing.takeaways.filter(t => t.pages.includes(slug)).map(t => ({claim:t.claim, pin:t.pinStr}));
    ingStatus(`Drafting changes to ${slug} (${ing.changes.filter(c => c.kind === "edit").length + 1} of ${ing.touched.length})…`);
    const prompt = `Edit one page of a research wiki with new evidence from a document.\nPage body:\n${page.body}\nVerified takeaways for this page, with ready-made pins: ${JSON.stringify(tks)}\nReturn JSON only: {"edits":[{"after":"existing heading text or 'end'","markdown":"..."}],"contested":"optional full contested block"} — at most 300 words in all; pins copied exactly. Pin syntax: [label](pin:id#pPAGE "quote") ✓; quote only words that stand in the passages given; the code will check. Add a contested block only where this document disagrees with the page.`;
    const r = await callModel(prompt, []);
    if(!r.json || !Array.isArray(r.json.edits)){ showRaw(dp, r, prompt); continue; }
    const res = applyEdits(page.body, r.json.edits);
    let body = res.body, inserted = res.inserted;
    if(r.json.contested){ body += "\\n\\n```contested\\n" + r.json.contested + "\\n```\\n"; ing.newContested.push({page:slug, block:r.json.contested}); }
    const fm = {...page.frontmatter, links:[...new Set([...(page.frontmatter.links||[]), ing.sourceSlug])], sources:[...new Set([...(page.frontmatter.sources||[]), doc.id])], updated:today};
    const newPage = {slug, type:page.type, title:page.title, frontmatter:fm, body};
    parsePage(newPage);
    const pins = newPage._pins, oldPins = page._pins.length;
    const ver = pins.filter(x => verify(x).ok).length;
    ing.changes.push({kind:"edit", slug, page:newPage, inserted, pinAdded:pins.length - oldPins, ver:ver - page._pins.filter(x => verify(x).ok).length, notVer:(pins.length - ver) - (oldPins - page._pins.filter(x => verify(x).ok).length), approved:null});
  }
  for(const s of ing.newSlugs){
    const tks = ing.takeaways.filter(t => (t.pages||[]).includes(s));
    const body = `# ${s}\\n\\n${tks.map(t => t.claim + " " + t.pinStr).join("\\n\\n")}`;
    const page = {slug:s, type:"concept", title:s, frontmatter:{title:s, type:"concept", tags:[], register:docRegister(doc.id), status:"draft", updated:today, links:[], sources:[doc.id]}, body};
    parsePage(page);
    ing.changes.push({kind:"new", slug:s, page, inserted:[body], pinAdded:page._pins.length, ver:page._pins.filter(x => verify(x).ok).length, notVer:0, approved:null});
  }
  document.getElementById("ingStop").hidden = true;
  ingStatus(`Step 3 done · ${ing.changes.length} change cards to review`);
  showReview();
}
function applyEdits(body, edits){
  let out = body; const inserted = [];
  for(const e of (edits || [])){
    const md = e.markdown || ""; if(!md) continue;
    inserted.push(md);
    if(!e.after || e.after === "end"){ out += "\\n\\n" + md + "\\n"; continue; }
    const lines = out.split("\\n");
    let idx = -1;
    for(let i = 0; i < lines.length; i++){ const m = lines[i].match(/^(#{1,3})\\s+(.*)$/); if(m && m[2].trim().toLowerCase() === String(e.after).trim().toLowerCase()){ idx = i; break; } }
    if(idx < 0){ out += "\\n\\n" + md + "\\n<!-- heading not found: " + String(e.after).replace(/-->/g,"") + " -->\\n"; continue; }
    const lvl = lines[idx].match(/^(#{1,3})/)[1].length;
    let j = idx + 1;
    while(j < lines.length){ const m = lines[j].match(/^(#{1,3})\\s/); if(m && m[1].length <= lvl) break; j++; }
    lines.splice(j, 0, "", md);
    out = lines.join("\\n");
  }
  return {body:out, inserted};
}
function showReview(){
  ing.ci = 0;
  renderReviewCard();
}
function renderReviewCard(){
  const rv = document.getElementById("ingReview");
  const n = ing.changes.length;
  if(ing.ci >= n){ 
    rv.innerHTML = `<div class="card"><h2 class="serif" style="font-weight:normal">Step 4 · File</h2>
    <p>${ing.changes.filter(c => c.approved).length} of ${n} changes approved, ${ing.changes.filter(c => !c.approved).length} rejected. Nothing has been written to the wiki yet.</p>
    <button class="btn primary" id="fileChanges">File the approved changes</button></div>`;
    document.getElementById("fileChanges").onclick = fileChanges;
    return;
  }
  const c = ing.changes[ing.ci];
  let disp = c.page.body;
  for(const md of c.inserted) disp = disp.split(md).join("<!--INS-->\\n" + md + "\\n<!--/INS-->");
  rv.innerHTML = `<fieldset class="card"><legend>${esc(c.page.title)} (${esc(c.page.type)}) — ${c.kind === "new" ? "new page" : "edited"} · change ${ing.ci+1} of ${n}</legend>
  <p class="mono">${c.inserted.length} paragraph(s) inserted · ${c.pinAdded} pin(s) added — ${c.ver} verified, ${c.notVer} not verified (in words, counted by this page's code)</p>
  <div class="pagebody">${renderBody(disp, {card:true, pageSlug:c.slug})}</div>
  <button class="btn primary" id="approveBtn">Approve change ${ing.ci+1} of ${n}</button>
  <button class="btn" id="rejectBtn">Reject change ${ing.ci+1} of ${n}</button>
  <div class="mono" aria-live="polite" id="revMsg"></div></fieldset>`;
  document.getElementById("approveBtn").onclick = () => { c.approved = true; ing.ci++; renderReviewCard(); };
  document.getElementById("rejectBtn").onclick = () => { c.approved = false; ing.ci++; renderReviewCard(); };
}
function updateIndexLine(slug){
  const p = bySlug[slug];
  const ver = p._pins.filter(x => verify(x).ok).length;
  W.index = W.index.split("\\n").map(l => l.includes("[[" + slug + "]]") ? l.replace(/✓\\d+/, "✓" + ver) : l).join("\\n");
}
function fileChanges(){
  const approved = ing.changes.filter(c => c.approved);
  const rejected = ing.changes.filter(c => !c.approved);
  for(const c of approved){
    if(c.kind === "new"){
      if(!bySlug[c.slug]){ P.push(c.page); bySlug[c.slug] = c.page; }
      else { const i = P.findIndex(p => p.slug === c.slug); P[i] = c.page; bySlug[c.slug] = c.page; }
      parsePage(c.page);
      const ver = c.page._pins.filter(x => verify(x).ok).length;
      W.index += `\\n- [[${c.slug}]] — ${kebab(c.page.title).slice(0,60)} · (${(c.page.frontmatter.register||[]).join("")}) · ✓${ver}`;
    } else {
      const i = P.findIndex(p => p.slug === c.slug);
      if(i >= 0) P[i] = c.page;
      bySlug[c.slug] = c.page; parsePage(c.page); updateIndexLine(c.slug);
    }
    c.page.frontmatter.updated = today;
  }
  byId[ing.doc.id].status = "ingested";
  W.log += `\\n\\n## [${today}] ingest | ${ing.doc.symbol || ing.doc.id}: ${ing.doc.short_title || ing.doc.title}\\n\\nRead ${ing.doc.passages.length} passages (${citeAs(ing.doc.id)}, register ${(docRegister(ing.doc.id).join(""))}). Approved: ${approved.map(c => "[[" + c.slug + "]]").join(", ") || "none"}. Rejected: ${rejected.map(c => "[[" + c.slug + "]]").join(", ") || "none"}.`;
  for(const nc of ing.newContested){
    W.tensions += `\\n\\n### ${kebab(nc.block.split("\\n").find(l => l.startsWith("claim:")) || "contested claim").slice(6)} \\nstatus: open\\ncard: [[${nc.page}]]\\n\\n${nc.block}\\n`;
  }
  W.count = P.length;
  S.changes += approved.length;
  sessionChanges.push({date:today, kind:"ingest", slug:ing.doc.id, approved:approved.map(c => c.slug), rejected:rejected.map(c => c.slug)});
  const after = computeLint();
  const before = ing.lintBefore;
  setRunning(false);
  ingestRun.hidden = true; ingestHome.hidden = false;
  renderHeader(); renderPageList(); renderCheck(); renderIngestHome(); renderRecord();
  alert(`Filed ${approved.length} change(s). Lint before: ${before.filter(c => !c.pass).length} checks need a look; after: ${after.filter(c => !c.pass).length}. The document is now marked ingested (in memory only — download on tab 05 to keep it).`);
}
/* ---------- tab 04: check ---------- */
function computeLint(){
  const checks = [];
  const add = (name, count, pass, pages, desc) => checks.push({name, count, pass, pages, desc});
  const allPins = P.flatMap(p => p._pins.map(x => ({p:p.slug, pin:x})));
  const ver = allPins.filter(o => verify(o.pin).ok);
  const statedM = W.index.match(/(\\d[\\d,]*) pins/);
  const stated = statedM ? +statedM[1].replace(/,/g,"") : null;
  add("Pins found vs the index's stated number", stated === null ? allPins.length : Math.abs(stated - allPins.length), stated === allPins.length, [], `index says ${stated}, code found ${allPins.length}`);
  const unver = allPins.filter(o => !verify(o.pin).ok);
  add("Pins not verified by this page's code", unver.length, unver.length === 0, [...new Set(unver.map(o => o.p))], `${ver.length} of ${allPins.length} verified`);
  const failMarked = allPins.filter(o => o.pin.mark === "✓" && !verify(o.pin).ok);
  add("Pins marked ✓ that fail verification", failMarked.length, failMarked.length === 0, [...new Set(failMarked.map(o => o.p))], "the page's own mark vs the code");
  const dangling = P.flatMap(p => p._links.filter(s => !bySlug[s]).map(s => p.slug));
  add("Dangling [[links]]", dangling.length, dangling.length === 0, [...new Set(dangling)], "links to slugs with no page");
  const orphans = P.filter(p => !(backlinks[p.slug] || []).length).map(p => p.slug);
  add("Orphan pages (nothing links to them)", orphans.length, orphans.length === 0, orphans, "");
  const srcMis = P.filter(p => [...new Set(p._pins.map(x => x.id))].sort().join(",") !== (p.frontmatter.sources||[]).slice().sort().join(",")).map(p => p.slug);
  add("frontmatter.sources differ from the pinned documents", srcMis.length, srcMis.length === 0, srcMis, "sources must equal the set of pinned documents");
  const noPins = P.filter(p => p._pins.length === 0).map(p => p.slug);
  add("Pages with no pins", noPins.length, noPins.length === 0, noPins, "");
  const nonRecip = [...new Set(P.flatMap(p => (p.frontmatter.links||[]).filter(s => bySlug[s] && !bySlug[s]._links.includes(p.slug)).map(() => p.slug)))];
  add("frontmatter.links not reciprocated in the body", nonRecip.length, nonRecip.length === 0, nonRecip, "");
  const indexSlugs = [...W.index.matchAll(/\\[\\[([^\\]|#]+)\\]\\]/g)].map(m => m[1]);
  const missIdx = P.filter(p => !indexSlugs.includes(p.slug)).map(p => p.slug);
  const idxNoPage = indexSlugs.filter(s => !bySlug[s]);
  add("Pages missing from the index / index lines without a page", missIdx.length + idxNoPage.length, missIdx.length + idxNoPage.length === 0, missIdx, "");
  const idxCount = [];
  for(const m of W.index.matchAll(/\\[\\[([^\\]|#]+)\\]\\][^\\n]*?✓(\\d+)/g)){
    const p = bySlug[m[1]];
    if(p && p._pins.filter(x => verify(x).ok).length !== +m[2]) idxCount.push(p.slug);
  }
  add("Index ✓N differs from the computed count", idxCount.length, idxCount.length === 0, idxCount, "");
  const cards = P.filter(p => p._contested > 0).map(p => p.slug);
  const tens = [...W.tensions.matchAll(/card:\\s*\\[\\[([^\\]|#]+)\\]\\]/g)].map(m => m[1]);
  const cDiff = cards.filter(s => !tens.includes(s)).concat(tens.filter(s => !cards.includes(s)));
  add("Contested cards without a tensions entry, and the reverse", cDiff.length, cDiff.length === 0, cDiff, "");
  const stubs = P.filter(p => p.frontmatter.status === "stub").map(p => p.slug);
  add("Stub pages (waiting for their ingest)", stubs.length, false, stubs, "a stub is expected until its document is ingested");
  const inboxPins = allPins.filter(o => byId[o.pin.id] && byId[o.pin.id].status === "inbox");
  add("Pins to a document still in the inbox", inboxPins.length, inboxPins.length === 0, [...new Set(inboxPins.map(o => o.p))], "");
  return checks;
}
function renderCheck(){
  const allPins = P.flatMap(p => p._pins);
  const ver = allPins.filter(x => verify(x).ok).length;
  document.getElementById("checkBig").textContent = `${ver} of ${allPins.length} pins verified by this page`;
  const checks = computeLint();
  document.getElementById("checkNeed").innerHTML = `<span class="${checks.filter(c => !c.pass).length ? "bad" : "pass"}">${checks.filter(c => !c.pass).length} lint checks need a look</span>`;
  document.querySelector("#lintTable tbody").innerHTML = checks.map(c =>
    `<tr><td>${esc(c.name)}</td><td class="${c.pass ? "pass" : "bad"}">${c.count} · ${c.pass ? "pass" : "check"}</td><td>${c.pages.length ? c.pages.map(s => `<a href="#${esc(s)}" data-slug="${esc(s)}">${esc(s)}</a>`).join(", ") : "—"}</td></tr>`).join("");
  document.getElementById("checksList").innerHTML = checks.map(c =>
    `<p><span class="${c.pass ? "pass" : "bad"} mono">${c.pass ? "pass" : "check"}</span> — ${esc(c.name)}: ${esc(c.desc || (c.count + " found"))}${c.pages.length ? " · pages: " + esc(c.pages.join(", ")) : ""}</p>`).join("") +
    `<p class="mono">the schema's reading for contradictions is named here but not done by code: no model call lints contradictions.</p>`;
  document.getElementById("lintBtn").textContent = "Re-run";
}
document.getElementById("lintBtn").addEventListener("click", renderCheck);
/* ---------- tab 05: record ---------- */
const orderSwitch = document.getElementById("orderSwitch");
function renderRecord(){
  const entries = W.log.split(/(?=^## )/m).filter(s => s.trim());
  const list = orderSwitch.checked ? entries.slice().reverse() : entries;
  document.getElementById("logView").innerHTML = `<h2 class="serif" style="font-weight:normal">Log</h2>` + list.map(e => {
    const m = e.match(/^## \\[([^\\]]+)\\] (\\w+) \\| ([^\\n]*)/);
    const session = W.log.indexOf(e) >= sessionLogStart;
    const rest = e.replace(/^## [^\\n]*\\n/, "");
    return `<details><summary>${m ? esc(m[1] + " · " + m[2] + " · " + m[3]) : esc(e.slice(0,60))} ${session ? '<span class="sess">this session</span>' : ""}</summary><div class="pagebody">${renderBody(rest, {})}</div></details>`;
  }).join("");
  document.getElementById("tensionsView").innerHTML = renderBody(W.tensions, {});
  document.getElementById("srcLine").textContent = "source: " + W.source + " · built " + W.built + " · library: " + L.source;
  document.getElementById("dlChanged").hidden = S.changes === 0;
}
orderSwitch.addEventListener("change", renderRecord);
function download(name, text, type){
  const blob = new Blob([text], {type});
  const a = document.createElement("a");
  a.href = URL.createObjectURL(blob); a.download = name;
  document.body.appendChild(a); a.click(); a.remove();
  setTimeout(() => URL.revokeObjectURL(a.href), 1000);
}
document.getElementById("dlWiki").addEventListener("click", () => {
  const out = {title:W.title, source:W.source, built:W.built, count:P.length, schema:W.schema, index:W.index, log:W.log, tensions:W.tensions,
    pages:P.map(p => ({slug:p.slug, type:p.type, title:p.title, frontmatter:p.frontmatter, body:p.body})),
    changes:sessionChanges, library_status:D.map(d => ({id:d.id, status:d.status}))};
  download("wiki-" + today + ".json", JSON.stringify(out, null, 2), "application/json");
});
document.getElementById("dlChanged").addEventListener("click", () => {
  const slugs = [...new Set(sessionChanges.flatMap(c => c.kind === "ingest" ? (c.approved || []) : [c.slug]))];
  const text = slugs.map(s => { const p = bySlug[s]; return p ? pageMarkdown(p) : "# " + s + " (not found)"; }).join("\\n\\n---\\n\\n");
  download("wiki-changed-" + today + ".md", text, "text/markdown");
});
/* ---------- global events ---------- */
document.addEventListener("click", e => {
  const op = e.target.closest("[data-openpin]");
  if(op){ e.preventDefault(); studio.openSource(op.dataset.id, +op.dataset.page, op.dataset.quote); return; }
  const ex = e.target.closest(".expbtn");
  if(ex){
    const d = ex.closest(".pin").querySelector(".pindetail");
    const hid = d.hidden; d.hidden = !hid;
    ex.setAttribute("aria-expanded", String(!hid)); ex.textContent = hid ? "▾" : "▸";
    return;
  }
  const sl = e.target.closest("a[data-slug]");
  if(sl){ e.preventDefault(); location.hash = sl.dataset.slug; return; }
  const gt = e.target.closest("[data-goto]");
  if(gt){ e.preventDefault(); showTab(gt.dataset.goto); }
});
window.addEventListener("hashchange", () => {
  const s = location.hash.slice(1);
  if(bySlug[s]) showPage(s);
});
/* ---------- init ---------- */
document.getElementById("foot").textContent = W.source + " · built " + W.built + " · Counting, matching and verification are done by this page's code; the model is called only when you press Ask, Ingest or a retry button. Credits: method after Karpathy's \"LLM Wiki\"; UK Government Analysis Function QA guidance (OGL 3.0); A11Y Project checklist (CC BY 4.0).";
renderHeader(); renderPageList(); renderIndexView(); renderCheck(); renderRecord(); renderIngestHome();
showTab("pages");
document.getElementById("tabbtn-pages").focus();
if(location.hash){ const s = location.hash.slice(1); if(bySlug[s]) showPage(s); }
</script>
</body>
</html>
```