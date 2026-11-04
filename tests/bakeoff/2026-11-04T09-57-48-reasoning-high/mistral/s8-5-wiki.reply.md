Here is the complete workspace: five tabs (pages, ask, ingest, check, record), every pin re-verified in code against the library passages, model calls only on button press with announced sizes, and all session changes kept in memory until download.

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Research wiki · neurotechnology and justice</title>
<style>
:root{--paper:#f4f0e8;--ink:#1d1b18;--rule:#d9d2c3;--red:#9b2335;--green:#2e6b3e;--amber:#8a5a00;--grey:#6b675f}
*{box-sizing:border-box}
[hidden]{display:none!important}
body{background:var(--paper);color:var(--ink);font:16px/1.55 -apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;margin:0;padding:0 22px 60px}
.serif{font-family:Georgia,"Times New Roman",serif}
.mono{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:11.5px;letter-spacing:.08em;text-transform:uppercase}
.quiet{color:var(--grey)}
.bad{color:var(--red)} .ok{color:var(--green)} .warn{color:var(--amber)}
header{display:flex;justify-content:space-between;gap:24px;flex-wrap:wrap;padding:18px 0 12px;border-bottom:1px solid var(--rule)}
.kicker{color:var(--red)}
nh1,h1.title{font-family:Georgia,"Times New Roman",serif;font-size:29px;font-weight:normal;margin:6px 0 8px;max-width:760px}
#hdr-line{text-transform:none;letter-spacing:.02em;color:var(--ink)}
#hdr-session{text-align:right}
#hdr-note{text-align:right;color:var(--grey);margin-top:4px;max-width:340px}
nav[role=tablist]{display:flex;gap:2px;flex-wrap:wrap;border-bottom:1px solid var(--rule);margin:14px 0 22px}
nav[role=tablist] button{background:none;border:none;border-bottom:2px solid transparent;padding:9px 13px;cursor:pointer;color:var(--ink);font-family:ui-monospace,Menlo,Consolas,monospace;font-size:12px;letter-spacing:.08em}
nav[role=tablist] button[aria-selected=true]{color:var(--red);border-bottom-color:var(--red)}
:focus-visible{outline:2px solid var(--red);outline-offset:2px}
.cols{display:grid;grid-template-columns:320px minmax(0,1fr);gap:34px}
@media(max-width:900px){.cols{grid-template-columns:1fr}}
.rail input{width:100%}
.bignum{font-size:46px;line-height:1.05;margin:12px 0 2px}
.group{margin:16px 0 4px;color:var(--grey);border-bottom:1px solid var(--rule);padding-bottom:3px}
.pitem{display:block;width:100%;text-align:left;background:none;border:none;border-left:2px solid transparent;padding:6px 9px;cursor:pointer;font:inherit;color:var(--ink)}
.pitem:hover{background:#ece6d8}
.pitem.active{border-left-color:var(--red);background:#ece6d8}
.pitem .pt{display:block}
.pitem .meta{color:var(--grey)}
.main{max-width:900px;min-width:0}
h2.serif{font-size:27px;font-weight:normal;margin:0 0 6px}
.badges{color:var(--grey);margin:2px 0 8px}
.tag{display:inline-block;border:1px solid var(--rule);border-radius:11px;padding:0 9px;font-family:ui-monospace,Menlo,Consolas,monospace;font-size:11px;margin:2px 4px 2px 0;color:var(--grey);text-transform:none;letter-spacing:.03em}
.tag.red{color:var(--red);border-color:var(--red)}
.body h3{font-size:19px;margin:22px 0 6px}
.body h4{font-size:16.5px;margin:16px 0 4px}
.body p{margin:8px 0}
.body ul,.body ol{margin:8px 0;padding-left:24px}
.body li{margin:3px 0}
.pin{white-space:normal}
.pq{font-style:italic}
.chip{display:inline-block;border:1px solid var(--rule);border-radius:12px;background:#fff;padding:1px 9px;font-family:ui-monospace,Menlo,Consolas,monospace;font-size:11px;cursor:pointer;margin:1px 2px;vertical-align:middle;color:var(--ink)}
.chip:hover{border-color:var(--red);color:var(--red)}
.reg{color:var(--grey)}
.v{font-size:13px}
.v.ok{color:var(--green)} .v.warn{color:var(--amber)} .v.bad{color:var(--red)}
.pin.struck .pq,.pin.struck .chip{text-decoration:line-through}
.pdetail{display:block;border-left:2px solid var(--rule);background:#efe9db;padding:6px 12px;margin:5px 0}
.pdetail p{margin:4px 0;font-size:14.5px}
.contested{border:1px solid var(--rule);background:#efe9db;padding:14px 18px;margin:18px 0}
.verdict{font-size:34px;color:var(--red);margin:2px 0 6px}
.lean{height:10px;background:#e0dac6;margin:6px 0 12px}
.leanfill{height:100%;background:var(--red)}
.fig{color:var(--grey);margin:8px 0 2px}
table{border-collapse:collapse;width:100%;margin:10px 0;font-size:14.5px}
caption{text-align:left;font-family:ui-monospace,Menlo,Consolas,monospace;font-size:11.5px;letter-spacing:.08em;text-transform:uppercase;color:var(--grey);padding:4px 0}
th,td{border-bottom:1px solid var(--rule);padding:6px 9px;text-align:left;vertical-align:top}
th{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:11px;letter-spacing:.06em;text-transform:uppercase;color:var(--grey);font-weight:normal}
.btn{border:1px solid var(--ink);background:none;color:var(--ink);padding:7px 15px;cursor:pointer;font:inherit;border-radius:2px;margin:3px 4px 3px 0}
.btn.primary{background:var(--red);border-color:var(--red);color:#fff}
.btn:disabled{opacity:.45;cursor:not-allowed}
.greybox{background:#e9e3d4;border:1px solid var(--rule);padding:10px 15px;margin:12px 0;font-size:14.5px}
.progress{color:var(--red);font-family:ui-monospace,Menlo,Consolas,monospace;font-size:12px;min-height:1.3em;margin:8px 0}
fieldset.card{border:1px solid var(--rule);margin:16px 0;padding:12px 18px}
legend{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:12px;letter-spacing:.06em;text-transform:uppercase;padding:0 8px}
.ins{background:#fdf3c9;border-left:3px solid #dfc25a;padding:2px 9px}
.diff .rest{color:var(--grey)}
.ai{border:1px dashed var(--red);padding:6px 20px;margin:14px 0}
.rawbox pre{white-space:pre-wrap;background:#efe9db;padding:10px;max-height:280px;overflow:auto;font-size:13px}
pre.raw{background:#efe9db;padding:10px;overflow:auto;font-size:13px}
textarea,input[type=text],input[type=search]{border:1px solid var(--rule);background:#fff;padding:7px 9px;font:inherit;width:100%}
.field{margin:12px 0}
label{display:block;font-family:ui-monospace,Menlo,Consolas,monospace;font-size:11.5px;letter-spacing:.08em;text-transform:uppercase;color:var(--grey);margin-bottom:4px}
label.inline{display:inline;text-transform:none;letter-spacing:0;font-family:inherit;color:var(--ink)}
details.logentry{margin:7px 0;border-bottom:1px solid var(--rule);padding-bottom:7px}
details.logentry summary{cursor:pointer}
.wikilink{color:var(--red)}
.src{margin:5px 0}
footer{border-top:1px solid var(--rule);margin-top:34px;padding-top:10px;color:var(--grey)}
.hint{color:var(--grey);margin:2px 0 10px}
</style>
</head>
<body>
<header>
  <div>
    <div class="mono kicker">WIKI · neurotechnology and justice</div>
    <h1 class="title">Research wiki: neurotechnology in the administration of justice</h1>
    <div id="hdr-line" class="mono"></div>
  </div>
  <div>
    <div id="hdr-session" class="mono"></div>
    <div id="hdr-note" class="mono">This page has no storage: changes live in it until you download them (tab 05)</div>
  </div>
</header>

<nav role="tablist" aria-label="Sections" id="tabs">
  <button role="tab" id="tab-pages" aria-controls="panel-pages" aria-selected="true" data-tab="pages">01 PAGES</button>
  <button role="tab" id="tab-ask" aria-controls="panel-ask" aria-selected="false" tabindex="-1" data-tab="ask">02 ASK</button>
  <button role="tab" id="tab-ingest" aria-controls="panel-ingest" aria-selected="false" tabindex="-1" data-tab="ingest">03 INGEST<span id="run-mark" aria-live="polite"></span></button>
  <button role="tab" id="tab-check" aria-controls="panel-check" aria-selected="false" tabindex="-1" data-tab="check">04 CHECK</button>
  <button role="tab" id="tab-record" aria-controls="panel-record" aria-selected="false" tabindex="-1" data-tab="record">05 RECORD</button>
</nav>

<main>
  <section role="tabpanel" id="panel-pages" aria-labelledby="tab-pages">
    <div class="cols">
      <aside class="rail">
        <label for="page-filter">Filter: title, tag or slug</label>
        <input id="page-filter" type="search" placeholder="title, tag or slug" autocomplete="off">
        <div class="bignum serif" id="page-count"></div>
        <div class="mono hint">literal match, not synonyms · click a page to open it</div>
        <div id="page-list"></div>
      </aside>
      <div class="main" id="page-main"></div>
    </div>
  </section>

  <section role="tabpanel" id="panel-ask" aria-labelledby="tab-ask" hidden>
    <div class="greybox" id="ask-announce"></div>
    <div class="field">
      <label for="ask-q">Your question about the wiki</label>
      <textarea id="ask-q" rows="3" placeholder="e.g. What do the documents say about consent to brain-based lie detection in custody?"></textarea>
    </div>
    <button class="btn primary" id="ask-btn">Ask the wiki</button>
    <button class="btn" id="ask-stop" hidden>Stop</button>
    <div class="progress" id="ask-progress" aria-live="polite"></div>
    <div id="ask-out"></div>
  </section>

  <section role="tabpanel" id="panel-ingest" aria-labelledby="tab-ingest" hidden>
    <div id="ingest-home"></div>
    <div class="progress" id="ingest-run" aria-live="polite"></div>
    <button class="btn" id="ingest-stop" hidden>Stop (Escape also stops)</button>
    <div id="ingest-work"></div>
  </section>

  <section role="tabpanel" id="panel-check" aria-labelledby="tab-check" hidden>
    <div class="bignum serif" id="check-num"></div>
    <div class="mono hint">how this is computed: every pin in every page is re-checked against the library passages by this page's code</div>
    <div class="mono" id="check-sub" style="margin:6px 0 14px"></div>
    <button class="btn primary" id="lint-btn">Lint now</button>
    <table id="lint-table">
      <caption>FIG.03 · Lint checks — each reads 0 · pass or n · check</caption>
      <thead><tr><th scope="col">Check</th><th scope="col">Result</th><th scope="col">Pages concerned</th></tr></thead>
      <tbody id="lint-body"></tbody>
    </table>
    <details open>
      <summary class="mono">How this app checks itself</summary>
      <div id="selfcheck-list" style="margin-top:8px"></div>
    </details>
  </section>

  <section role="tabpanel" id="panel-record" aria-labelledby="tab-record" hidden>
    <label class="inline" style="display:inline-block"><input type="checkbox" id="log-order" checked> newest first</label>
    <h3 class="serif" style="font-size:21px;margin:14px 0 6px">Log</h3>
    <div id="log-view"></div>
    <h3 class="serif" style="font-size:21px;margin:20px 0 6px">Tensions register</h3>
    <div id="tensions-view" class="body"></div>
    <p class="hint mono" style="margin-top:18px">Counting, matching and verification are done by this page's code; each number above has its "how this is computed" line. The model is called only when you press Ask, Ingest or a retry button.</p>
    <p class="mono" id="rec-source"></p>
    <button class="btn primary" id="dl-wiki">Download the wiki (JSON)</button>
    <button class="btn" id="dl-changed" hidden>Download changed pages (markdown)</button>
  </section>
</main>

<footer class="mono" id="foot"></footer>

<script>
'use strict';
/* ---------- data ---------- */
const W = WORKSHOP_DATA.wiki, L = WORKSHOP_DATA.library;
const P = W.pages, D = L.records;
const bySlug = {}, byId = {};
P.forEach(p => bySlug[p.slug] = p);
D.forEach(d => byId[d.id] = d);

const PIN_SRC = '\\[([^\\]]+)\\]\\(pin:([^#\\s)]+)#p(\\d+)(?: "([^"]*)")?\\) ?(✓|⚠)';
const pinRe = () => new RegExp(PIN_SRC, 'g');
const REG_NAMES = {a:'treaty law', b:'General Comments', c:'UN, agency and soft-law reports', d:'national human rights institution', e:'civil society', f:'scholarship'};
const REG_W = {a:5, b:4, c:3, d:2, e:1, f:0.5};
const session = {changes:0, calls:0, passages:0, changedSlugs:[], logAdded:0};
let stopFlag = false, currentSlug = null;

function esc(s){return String(s==null?'':s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');}
function norm(s){if(s==null)return '';s=String(s).normalize('NFKC');s=s.replace(/[“”„]/g,'"').replace(/[‘’]/g,"'").replace(/[–—]/g,'-').replace(/\u00AD/g,'');s=s.replace(/-\s+/g,'-').replace(/\s+/g,' ').trim();return s;}
function kebab(s){return String(s).toLowerCase().replace(/[^a-z0-9]+/g,'-').replace(/^-+|-+$/g,'');}
function today(){const d=new Date();return d.getFullYear()+'-'+String(d.getMonth()+1).padStart(2,'0')+'-'+String(d.getDate()).padStart(2,'0');}
function chunk(a,n){const r=[];for(let i=0;i<a.length;i+=n)r.push(a.slice(i,i+n));return r;}

/* ---------- verification ---------- */
function verifyPin(pin){
  const doc = byId[pin.id];
  if(!doc) return {ok:false, reason:'unknown document'};
  if(doc.status === 'inbox') return {ok:false, reason:'document still in the inbox'};
  if(!pin.quote) return {ok:false, reason:'no quote'};
  const frags = pin.quote.split(/…|\.\.\./).map(norm).filter(f => f.length);
  if(!frags.length) return {ok:false, reason:'no quote'};
  for(const x of doc.passages){
    if(x.page !== pin.page) continue;
    const t = norm(x.text);
    let pos = 0, ok = true;
    for(const f of frags){
      const i = t.indexOf(f, pos);
      if(i < 0){ ok = false; break; }
      pos = i + f.length;
    }
    if(!ok) continue;
    const labelOk = x.paragraph != null ? pin.label.includes('para. ' + x.paragraph) : pin.label.includes('p. ' + x.page_label);
    if(!labelOk) continue;
    return {ok:true, passage:x};
  }
  return {ok:false, reason:'quote not found on that PDF page'};
}
P.forEach(p => {
  p._links = [...p.body.matchAll(/\[\[([^\]|#]+)\]\]/g)].map(m => m[1]);
  p._pins = [...p.body.matchAll(pinRe())].map(m => ({label:m[1], id:m[2], page:+m[3], quote:m[4]||'', mark:m[5], raw:m[0]}));
  p._pins.forEach(pn => pn._v = verifyPin(pn));
});
function recompute(p){
  p._links = [...p.body.matchAll(/\[\[([^\]|#]+)\]\]/g)].map(m => m[1]);
  p._pins = [...p.body.matchAll(pinRe())].map(m => ({label:m[1], id:m[2], page:+m[3], quote:m[4]||'', mark:m[5], raw:m[0]}));
  p._pins.forEach(pn => pn._v = verifyPin(pn));
}
const backlinks = {};
P.forEach(p => p._links.forEach(s => {(backlinks[s] = backlinks[s] || []).push(p.slug);}));

function docRegister(id){
  const src = P.find(p => p.type === 'source' && p.frontmatter.sources && p.frontmatter.sources.length === 1 && p.frontmatter.sources[0] === id);
  if(src) return (src.frontmatter.register || []).join('');
  const stub = P.find(p => p.frontmatter.status === 'stub' && p.frontmatter.sources && p.frontmatter.sources.length === 1 && p.frontmatter.sources[0] === id);
  if(stub) return (stub.frontmatter.register || []).join('');
  return '?';
}
function citeAs(id){
  const labels = [];
  P.forEach(p => p._pins.forEach(pn => {
    if(pn.id === id){ const m = pn.label.match(/^(.*?), (?:para\.|p\.)/); if(m) labels.push(m[1]); }
  }));
  if(labels.length){
    const c = {}; labels.forEach(l => c[l] = (c[l]||0)+1);
    return Object.entries(c).sort((a,b) => b[1]-a[1])[0][0];
  }
  const d = byId[id];
  return d.symbol || (d.author + ' ' + d.year);
}
function newPin(id, passage, quote){
  const q = String(quote || '').replace(/"/g, '”');
  const ca = citeAs(id);
  const loc = passage.paragraph != null ? 'para. ' + passage.paragraph : 'p. ' + passage.page_label;
  return '[' + ca + ', ' + loc + '](pin:' + id + '#p' + passage.page + ' "' + q + '") ✓';
}
function totalPins(){return P.reduce((a,p) => a + p._pins.length, 0);}
function verifiedPins(){return P.reduce((a,p) => a + p._pins.filter(x => x._v.ok).length, 0);}
function inboxDocs(){return D.filter(d => d.status === 'inbox');}

/* ---------- markdown rendering ---------- */
const CHIP_REG = [];
function pinChip(pin, ctx){
  ctx = ctx || {};
  const v = pin._v || verifyPin(pin);
  const reg = docRegister(pin.id);
  const idx = CHIP_REG.length; CHIP_REG.push({pin, v});
  const struck = ctx.sentRaws && !ctx.sentRaws.has(pin.raw);
  let status;
  if(struck) status = '<span class="v bad">not on the pages sent</span>';
  else status = '<span class="v ' + (v.ok ? 'ok' : 'warn') + '">' + (v.ok ? '✓ verified' : '⚠ not found')
    + (pin.mark === '✓' && !v.ok ? ' · page says ✓' : '') + (pin.mark === '⚠' && v.ok ? ' · page says ⚠' : '') + '</span>';
  let detail;
  if(v.ok && v.passage){
    const x = v.passage;
    detail = '<div class="pdetail" hidden><div class="mono">' + (x.paragraph != null ? 'para. ' + esc(x.paragraph) : 'p. ' + esc(x.page_label)) + ' · PDF page ' + x.page + '</div><p>' + esc(x.text.slice(0,300)) + (x.text.length > 300 ? '…' : '') + '</p><button class="chip" data-chip="' + idx + '">Open the PDF page</button></div>';
  } else {
    detail = '<div class="pdetail" hidden><p class="warn">' + esc(v.reason) + '. Footnotes, tables and captions are not in the passages, so a pin cannot verify them.</p><button class="chip" data-chip="' + idx + '">Open the PDF page anyway</button></div>';
  }
  return '<span class="pin' + (struck ? ' struck' : '') + '"><span class="pq">“' + esc(pin.quote) + '”</span> '
    + '<button class="chip" data-chip="' + idx + '" title="Open the source PDF at page ' + pin.page + ' with this quote marked">' + esc(pin.label) + '</button> '
    + '<span class="reg mono" title="' + esc(REG_NAMES[reg] || '') + '">(' + esc(reg) + ')</span> ' + status
    + ' <button class="chip more" data-more="' + idx + '" aria-expanded="false" aria-label="show the passage behind this pin">▸</button>' + detail + '</span>';
}
function wikiLink(slug){
  if(bySlug[slug]) return '<a href="#' + encodeURIComponent(slug) + '" class="wikilink" data-page="' + esc(slug) + '">' + esc(bySlug[slug].title) + '</a>';
  return '<span class="bad">[[' + esc(slug) + ']] no page</span>';
}
function inline(s, ctx){
  const tokens = [];
  const stash = h => { tokens.push(h); return '\u0000' + (tokens.length - 1) + '\u0000'; };
  s = s.replace(pinRe(), (m,l,id,pg,q,mk) => stash(pinChip({label:l, id:id, page:+pg, quote:q||'', mark:mk, raw:m}, ctx)));
  s = s.replace(/\[\[([^\]|#]+)\]\]/g, (m,sl) => stash(wikiLink(sl)));
  s = s.replace(/\[([^\]]+)\]\((https?:\/\/[^\)\s]+)\)/g, (m,t,u) => stash('<a href="' + esc(u) + '" target="_blank" rel="noopener">' + esc(t) + '</a>'));
  s = esc(s);
  s = s.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
  s = s.replace(/\*([^*]+)\*/g, '<em>$1</em>');
  s = s.replace(/\u0000(\d+)\u0000/g, (m,i) => tokens[+i]);
  return s;
}
function parseContested(text){
  const out = {positions:[]};
  text.split('\n').forEach(l => {
    if(l.startsWith('claim:')) out.claim = l.slice(6).trim();
    else if(l.startsWith('verdict:')) out.verdict = l.slice(8).trim();
    else if(l.startsWith('note:')) out.note = l.slice(5).trim();
    else if(/^[+~\-]\s*\|/.test(l)){
      const parts = l.split(' | ').map(s => s.trim());
      out.positions.push({sign:parts[0], register:parts[1], pinRaw:parts[2], gloss:parts[3], page:parts[4]});
    }
  });
  return out;
}
function renderContested(text, ctx){
  const c = parseContested(text);
  let num = 0, den = 0;
  c.positions.forEach(p => { const w = REG_W[p.register] || 0; den += w; if(p.sign === '+') num += w; else if(p.sign === '~') num += w/2; });
  const pct = den ? Math.round(100 * num / den) : 0;
  const signWords = {'+':'supports', '-':'contests', '~':'mixed'};
  const rows = c.positions.map(p => {
    const pm = p.pinRaw.match(new RegExp(PIN_SRC));
    const chip = pm ? pinChip({label:pm[1], id:pm[2], page:+pm[3], quote:pm[4]||'', mark:pm[5], raw:p.pinRaw}, ctx) : esc(p.pinRaw);
    const pg = (p.page || '').match(/\[\[([^\]]+)\]\]/);
    return '<tr><td>' + (signWords[p.sign] || esc(p.sign)) + '</td><td class="mono">(' + esc(p.register) + ')</td><td>' + chip + '</td><td>' + esc(p.gloss || '') + '</td><td>' + (pg ? wikiLink(pg[1]) : '') + '</td></tr>';
  }).join('');
  const inTensions = ctx && ctx.slug && W.tensions.includes('card: [[' + ctx.slug + ']]');
  return '<div class="contested"><h4 class="serif" style="margin:0 0 4px">' + esc(c.claim || 'Contested claim') + '</h4>'
    + '<div class="verdict serif">' + esc((c.verdict || '').replace(/-/g, ' ')) + '</div>'
    + '<p>' + esc(c.note || '') + '</p>'
    + '<div class="mono fig">FIG.01 · lean bar — descriptive: support ' + pct + '% of weighted positions · weights a 5 · b 4 · c 3 · d 2 · e 1 · f ½ · the verdict is the answer</div>'
    + '<div class="lean"><div class="leanfill" style="width:' + pct + '%"></div></div>'
    + '<table><caption>Positions in this contested block</caption><thead><tr><th scope="col">Sign</th><th scope="col">Register</th><th scope="col">Pin</th><th scope="col">Gloss</th><th scope="col">Page</th></tr></thead><tbody>' + rows + '</tbody></table>'
    + (inTensions ? '<button class="chip" data-goto="record">in the tensions register (tab 05)</button>' : '') + '</div>';
}
function renderMD(body, ctx){
  ctx = ctx || {};
  const ins = ctx.ins || null;
  const lines = String(body == null ? '' : body).split('\n');
  const out = []; let para = []; let listTag = null;
  const clsOf = ls => ins ? (ls.every(l => ins.has(l)) ? ' class="ins"' : ' class="rest"') : '';
  function flushPara(){ if(para.length){ out.push('<p' + clsOf(para) + '>' + inline(para.join(' '), ctx) + '</p>'); para = []; } }
  let i = 0;
  while(i < lines.length){
    const l = lines[i];
    if(/^\s*```/.test(l)){
      flushPara(); if(listTag){ out.push('</' + listTag + '>'); listTag = null; }
      const fence = l.trim().slice(3); const buf = []; i++;
      while(i < lines.length && !/^\s*```/.test(lines[i])){ buf.push(lines[i]); i++; }
      i++;
      if(fence === 'contested') out.push(renderContested(buf.join('\n'), ctx));
      else out.push('<pre class="raw">' + esc(buf.join('\n')) + '</pre>');
      continue;
    }
    const h = l.match(/^(#{1,3})\s+(.*)$/);
    if(h){ flushPara(); if(listTag){ out.push('</' + listTag + '>'); listTag = null; }
      const lv = h[1].length; out.push('<h' + (lv+1) + clsOf([l]) + '>' + inline(h[2], ctx) + '</h' + (lv+1) + '>'); i++; continue; }
    if(/^\s*$/.test(l)){ flushPara(); if(listTag){ out.push('</' + listTag + '>'); listTag = null; } i++; continue; }
    const li = l.match(/^\s*[-*]\s+(.*)$/), ni = l.match(/^\s*\d+\.\s+(.*)$/);
    if(li || ni){
      flushPara();
      const tag = li ? 'ul' : 'ol';
      if(listTag && listTag !== tag) out.push('</' + listTag + '>');
      if(listTag !== tag){ out.push('<' + tag + '>'); listTag = tag; }
      out.push('<li' + clsOf([l]) + '>' + inline((li || ni)[1], ctx) + '</li>'); i++; continue;
    }
    if(listTag){ out.push('</' + listTag + '>'); listTag = null; }
    para.push(l.trim()); i++;
  }
  flushPara(); if(listTag) out.push('</' + listTag + '>');
  return out.join('\n');
}

/* ---------- header, tabs, routing ---------- */
function updateHeader(){
  const types = {}; P.forEach(p => types[p.type] = (types[p.type]||0)+1);
  document.getElementById('hdr-line').textContent =
    P.length + ' pages (' + (types.source||0) + ' sources, ' + (types.concept||0) + ' concepts, ' + (types.entity||0) + ' entities, ' + (types.question||0) + ' questions) · '
    + totalPins() + ' pins, ' + verifiedPins() + ' verified by this page · ' + D.length + ' documents, ' + inboxDocs().length + ' in the inbox · built ' + W.built;
  document.getElementById('hdr-session').textContent =
    'Changes this session: ' + session.changes + ' · Calls to the model: ' + session.calls + ' · Passages that left the browser: ' + session.passages;
}
const TAB_IDS = ['pages','ask','ingest','check','record'];
function showTab(id){
  TAB_IDS.forEach(t => {
    const b = document.getElementById('tab-' + t);
    b.setAttribute('aria-selected', t === id ? 'true' : 'false');
    b.tabIndex = t === id ? 0 : -1;
    document.getElementById('panel-' + t).hidden = t !== id;
  });
  if(id === 'pages'){ if(currentSlug) renderPage(currentSlug); else renderIndex(); }
  if(id === 'ingest') renderIngestHome();
  if(id === 'check') renderCheck();
  if(id === 'record') renderRecord();
}
document.querySelectorAll('#tabs button').forEach(b => {
  b.addEventListener('click', () => showTab(b.dataset.tab));
  b.addEventListener('keydown', e => {
    const arr = [...document.querySelectorAll('#tabs button')];
    let i = arr.indexOf(b);
    if(e.key === 'ArrowRight') i = (i+1) % arr.length;
    else if(e.key === 'ArrowLeft') i = (i-1+arr.length) % arr.length;
    else if(e.key === 'Home') i = 0;
    else if(e.key === 'End') i = arr.length - 1;
    else return;
    e.preventDefault(); arr[i].focus(); showTab(arr[i].dataset.tab);
  });
});
function onHash(){
  const s = decodeURIComponent(location.hash.slice(1));
  if(bySlug[s]){ showTab('pages'); if(currentSlug !== s) selectPage(s); else renderPage(s); }
}
window.addEventListener('hashchange', onHash);
document.addEventListener('keydown', e => { if(e.key === 'Escape') stopFlag = true; });

/* ---------- tab 01: pages ---------- */
function renderList(){
  const q = (document.getElementById('page-filter').value || '').toLowerCase();
  const items = P.filter(p => !q || (p.title + ' ' + p.slug + ' ' + (p.frontmatter.tags || []).join(' ')).toLowerCase().includes(q));
  document.getElementById('page-count').textContent = items.length + ' of ' + P.length + ' pages';
  const order = ['source','concept','entity','question'];
  const labels = {source:'SOURCES', concept:'CONCEPTS', entity:'ENTITIES', question:'QUESTIONS'};
  let html = '';
  order.forEach(t => {
    const g = items.filter(p => p.type === t);
    if(!g.length) return;
    html += '<div class="mono group">' + labels[t] + '</div>';
    html += g.map(p => '<button class="pitem' + (p.slug === currentSlug ? ' active' : '') + '" data-page="' + esc(p.slug) + '"><span class="pt">' + esc(p.title) + '</span><span class="mono meta">' + (p.frontmatter.register || []).join('') + ' · ' + p._pins.length + ' pins' + (p.frontmatter.status === 'stub' ? ' · stub' : '') + '</span></button>').join('');
  });
  document.getElementById('page-list').innerHTML = html || '<p class="quiet">no pages match</p>';
}
function renderIndex(){
  document.getElementById('page-main').innerHTML =
    '<h2 class="serif">Index</h2><div class="mono hint">the catalog, one line per page · click a line to open the page</div><div class="body">' + renderMD(W.index, {}) + '</div>';
}
function pageMarkdown(p){
  const fm = p.frontmatter;
  const y = Object.keys(fm).map(k => { const v = fm[k]; return k + ': ' + (Array.isArray(v) ? v.join(', ') : v); }).join('\n');
  return '---\n' + y + '\n---\n\n' + p.body + '\n';
}
function renderPage(slug){
  const p = bySlug[slug]; if(!p) return;
  const fm = p.frontmatter;
  let body = p.body;
  const fh = body.match(/^#\s+(.+)$/m);
  if(fh && fh[1].trim() === p.title) body = body.replace(/^#\s+.+\n?/, '');
  const badges = [fm.type].concat((fm.register || []).map(r => '(' + r + ') ' + (REG_NAMES[r] || r)), [fm.status, 'updated ' + fm.updated]).join(' · ');
  const tags = (fm.tags || []).map(t => '<span class="tag">#' + esc(t) + '</span>').join(' ');
  const linksOut = (fm.links || []).map(l => bySlug[l]
    ? '<button class="chip" data-page="' + esc(l) + '">' + esc(bySlug[l].title) + '</button>' + (p._links.includes(l) ? '' : ' <span class="tag">frontmatter only</span>')
    : '<span class="bad">' + esc(l) + ' (no page)</span>').join(' ') || '<span class="quiet">none</span>';
  const linkedFrom = (backlinks[slug] || []).map(s => '<button class="chip" data-page="' + esc(s) + '">' + esc(bySlug[s].title) + '</button>').join(' ') || '<span class="quiet">none</span>';
  const sources = (fm.sources || []).map(id => {
    const d = byId[id];
    if(!d) return '<div class="src bad">' + esc(id) + ' (not in the library)</div>';
    return '<div class="src"><a href="' + esc(d.url) + '" target="_blank" rel="noopener">' + esc(d.symbol || 'no symbol') + '</a> · ' + esc(d.short_title || d.title) + ' · ' + esc(d.kind) + ' · ' + d.year + (d.status === 'inbox' ? ' · <span class="tag red">inbox</span>' : '') + ' · (' + esc(docRegister(id)) + ')</div>';
  }).join('') || '<span class="quiet">none</span>';
  document.getElementById('page-main').innerHTML =
    '<h2 class="serif">' + esc(p.title) + '</h2>'
    + '<div class="mono badges">' + esc(badges) + '</div>'
    + '<div>' + tags + '</div>'
    + '<div class="body">' + renderMD(body, {slug: slug}) + '</div>'
    + '<h3 class="serif" style="font-size:19px">Links out</h3><div>' + linksOut + '</div>'
    + '<h3 class="serif" style="font-size:19px">Linked from</h3><div>' + linkedFrom + '</div>'
    + '<h3 class="serif" style="font-size:19px">Sources</h3><div>' + sources + '</div>'
    + '<button class="btn" data-copy="' + esc(slug) + '" style="margin-top:14px">Copy page as markdown</button>';
}
function selectPage(slug){
  currentSlug = slug;
  renderList(); renderPage(slug);
  const target = '#' + encodeURIComponent(slug);
  if(location.hash !== target) location.hash = target;
}
document.getElementById('page-filter').addEventListener('input', renderList);

/* ---------- model calls ---------- */
async function askModel(prompt, opts){
  opts = opts || {};
  session.calls++; session.passages += (opts.passages || 0);
  updateHeader();
  let raw;
  try { raw = await studio.ask(prompt, {json: true}); }
  catch(e){ return {parsed:null, raw:'studio.ask failed: ' + e}; }
  let parsed = null;
  try { parsed = JSON.parse(raw); }
  catch(e){
    try { parsed = JSON.parse(String(raw).replace(/^```[a-zA-Z]*\s*/, '').replace(/```\s*$/, '').trim()); } catch(e2){ parsed = null; }
  }
  return {parsed, raw};
}
function rawBox(raw, retryFn){
  return '<div class="rawbox"><p class="mono bad">the model did not return JSON — raw answer shown, nothing was filed</p><pre>' + esc(raw) + '</pre><button class="btn" data-retry>Retry</button></div>';
}
function copyText(t){
  const fb = () => { const ta = document.createElement('textarea'); ta.value = t; document.body.appendChild(ta); ta.select(); try{document.execCommand('copy');}catch(e){} ta.remove(); };
  if(navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(t).catch(fb); else fb();
}

/* ---------- tab 02: ask ---------- */
const ask = {slugs:[], sent:[], answer:null};
function askAnnounce(){
  document.getElementById('ask-announce').textContent =
    'What leaves the browser when you press Ask: step 1 sends the index (' + W.index.length.toLocaleString() + ' characters) and your question; step 2 sends the bodies of the pages chosen (their character count is shown before sending) and your question. No library passages are sent in Ask.';
}
async function runAsk(){
  const q = document.getElementById('ask-q').value.trim();
  if(!q) return;
  const btn = document.getElementById('ask-btn'), out = document.getElementById('ask-out'), prog = document.getElementById('ask-progress');
  btn.disabled = true; btn.textContent = 'Ask again';
  document.getElementById('ask-stop').hidden = false; stopFlag = false;
  out.innerHTML = '';
  prog.textContent = 'Step 1 of 2 · sending the index (' + W.index.length.toLocaleString() + ' characters) and your question…';
  const p1 = 'You route a question to pages of a research wiki.\n\nINDEX:\n' + W.index + '\n\nQUESTION: ' + q + '\n\nReturn JSON only: {"pages": ["slug", ...]} — up to 5 slugs from the index that answer the question.';
  const r1 = await askModel(p1, {});
  if(!r1.parsed){ out.innerHTML = rawBox(r1.raw, runAsk); prog.textContent = ''; document.getElementById('ask-stop').hidden = true; btn.disabled = false; return; }
  ask.slugs = (r1.parsed.pages || []).filter(s => bySlug[s]).slice(0, 5);
  if(!ask.slugs.length) ask.slugs = P.slice(0, 5).map(p => p.slug);
  await runStep2(q, prog, out);
}
async function runStep2(q, prog, out){
  stopFlag = false;
  const bodies = ask.slugs.map(s => '=== ' + s + ' ===\n' + bySlug[s].body).join('\n\n');
  const chars = bodies.length + q.length;
  prog.textContent = 'Step 2 of 2 · sending ' + ask.slugs.length + ' pages, ' + chars.toLocaleString() + ' characters; 0 library passages have left the browser…';
  const p2 = 'You answer a question from pages of a research wiki. PIN SYNTAX: [label](pin:id#pPAGE "quote") ✓ — quote only words that stand in the pages given; the code will check every quotation. Name the register where it matters ((a) treaty law … (f) scholarship); keep each document\'s own verb; never present (c)–(f) as what a treaty requires.\n\nPAGES:\n' + bodies + '\n\nQUESTION: ' + q + '\n\nReturn JSON only: {"title": "short title", "answer": "markdown, at most 350 words, pins in the syntax above", "cannot_answer": "what the library cannot answer"}';
  const r2 = await askModel(p2, {});
  prog.textContent = ''; document.getElementById('ask-stop').hidden = true; document.getElementById('ask-btn').disabled = false;
  if(stopFlag) return;
  if(!r2.parsed){ out.innerHTML = rawBox(r2.raw, () => runStep2(q, prog, out)); return; }
  ask.answer = r2.parsed; ask.sent = [...ask.slugs];
  renderAnswer(out);
}
function renderAnswer(out){
  const a = ask.answer;
  const sentRaws = new Set();
  ask.sent.forEach(s => bySlug[s]._pins.forEach(pn => sentRaws.add(pn.raw)));
  const pins = [...String(a.answer || '').matchAll(pinRe())].map(m => ({label:m[1], id:m[2], page:+m[3], quote:m[4]||'', mark:m[5], raw:m[0]}));
  pins.forEach(pn => pn._v = verifyPin(pn));
  const accepted = pins.filter(pn => sentRaws.has(pn.raw) && pn._v.ok);
  const rc = {}; accepted.forEach(pn => { const r = docRegister(pn.id); rc[r] = (rc[r]||0)+1; });
  const regLine = Object.keys(REG_W).map(r => '(' + r + ') ' + (rc[r]||0)).join(' · ');
  out.innerHTML =
    '<div style="margin:10px 0">' + ask.slugs.map(s => '<button class="chip" data-page="' + esc(s) + '">' + esc(bySlug[s].title) + '</button>').join(' ')
    + ' <button class="chip" id="change-pages">Change pages</button></div>'
    + '<div id="page-picker" hidden></div>'
    + '<div class="ai" data-source="ai"><h3 class="serif">' + esc(a.title || 'Answer') + '</h3>'
    + '<div class="body">' + renderMD(a.answer || '', {sentRaws}) + '</div>'
    + '<p><strong>What the library cannot answer:</strong> ' + esc(a.cannot_answer || '—') + '</p>'
    + '<p class="mono">verified pins by register: ' + regLine + '</p></div>'
    + '<button class="btn" id="file-q">File as a question page</button>'
    + '<div id="file-card" hidden></div>';
  document.getElementById('change-pages').onclick = togglePicker;
  document.getElementById('file-q').onclick = showFileCard;
}
function togglePicker(){
  const pk = document.getElementById('page-picker');
  if(pk.hidden){
    pk.innerHTML = '<fieldset class="card"><legend>Choose the pages sent in step 2 (up to 5)</legend>'
      + P.map(p => '<label class="inline"><input type="checkbox" value="' + esc(p.slug) + '"' + (ask.slugs.includes(p.slug) ? ' checked' : '') + '> ' + esc(p.title) + '</label>').join('<br>')
      + '<br><button class="btn" id="picker-go">Send these pages</button></fieldset>';
    pk.hidden = false;
    document.getElementById('picker-go').onclick = () => {
      ask.slugs = [...pk.querySelectorAll('input:checked')].map(i => i.value).slice(0, 5);
      pk.hidden = true;
      runStep2(document.getElementById('ask-q').value.trim(), document.getElementById('ask-progress'), document.getElementById('ask-out'));
    };
  } else pk.hidden = true;
}
function showFileCard(){
  const card = document.getElementById('file-card');
  if(!card.hidden){ card.hidden = true; return; }
  const a = ask.answer, title = a.title || 'Question';
  let base = kebab(title) || 'question', slug = base, n = 2;
  while(bySlug[slug]) slug = base + '-' + (n++);
  const pins = [...String(a.answer || '').matchAll(pinRe())].map(m => ({label:m[1], id:m[2], page:+m[3], quote:m[4]||'', mark:m[5], raw:m[0]}));
  pins.forEach(pn => pn._v = verifyPin(pn));
  const sentRaws = new Set(); ask.sent.forEach(s => bySlug[s]._pins.forEach(pn => sentRaws.add(pn.raw)));
  const allOk = pins.length > 0 && pins.every(pn => pn._v.ok && sentRaws.has(pn.raw));
  const sources = [...new Set(pins.map(p => p.id))];
  const register = [...new Set(sources.map(docRegister))].filter(r => r !== '?');
  const links = [...new Set([...String(a.answer || '').matchAll(/\[\[([^\]|#]+)\]\]/g)].map(m => m[1]).filter(s => bySlug[s]))];
  const first = (String(a.answer || '').split(/(?<=[.!?])\s/)[0] || '').slice(0, 300);
  const body = '# ' + title + '\n\n**Short answer.** ' + first + '\n\n## Reasoning\n\n' + (a.answer || '') + '\n\n## What the library cannot answer\n\n' + (a.cannot_answer || '—') + '\n\n## Related\n\n' + (links.map(l => '[[' + l + ']]').join(', ') || '—');
  card.innerHTML = '<fieldset class="card"><legend>File as a question page</legend>'
    + '<div class="mono">slug ' + esc(slug) + ' · type question · status draft · updated ' + today() + ' · register (' + register.join(' ') + ') · ' + sources.length + ' sources</div>'
    + '<div class="field"><label for="fq-tags">Tags (comma separated)</label><input id="fq-tags" type="text" value="question, draft"></div>'
    + '<div class="ai" data-source="ai"><div class="body">' + renderMD(body, {}) + '</div></div>'
    + '<button class="btn primary" id="fq-file"' + (allOk ? '' : ' disabled') + '>File this page</button> '
    + (allOk ? '' : '<span class="mono bad">disabled until every pin in the answer verifies</span> ')
    + '<button class="btn" id="fq-copy">Copy answer</button>'
    + '<div class="mono" id="fq-msg" aria-live="polite"></div></fieldset>';
  card.hidden = false;
  document.getElementById('fq-copy').onclick = () => { copyText(a.answer || ''); document.getElementById('fq-msg').textContent = 'answer copied'; };
  document.getElementById('fq-file').onclick = () => {
    const tags = document.getElementById('fq-tags').value.split(',').map(s => s.trim()).filter(Boolean);
    const p = {slug, type:'question', title, frontmatter:{title, type:'question', tags, register, status:'draft', updated:today(), links, sources}, body};
    P.push(p); bySlug[slug] = p; recompute(p);
    updateIndexLine(slug);
    W.log += '\n\n## [' + today() + '] ask | ' + title;
    session.logAdded++; session.changes++; session.changedSlugs.push(slug);
    updateHeader(); renderList();
    document.getElementById('fq-msg').textContent = 'Filed as [[' + slug + ']] — open it on tab 01.';
  };
}
document.getElementById('ask-btn').onclick = runAsk;
document.getElementById('ask-stop').onclick = () => { stopFlag = true; };

/* ---------- tab 03: ingest ---------- */
const ing = {doc:null, batches:[], takeaways:[], failed:[], dropped:0, changes:[], touched:[]};
function prog(m){ document.getElementById('ingest-run').textContent = m; }
function markRunning(on){ document.getElementById('run-mark').textContent = on ? ' · running' : ''; }
function renderIngestHome(){
  const home = document.getElementById('ingest-home');
  const docs = inboxDocs();
  if(!docs.length){ home.innerHTML = '<p class="quiet">Nothing waits in the inbox.</p>'; return; }
  home.innerHTML = '<p>Documents in the library but not yet read into the wiki:</p>'
    + docs.map(d => '<button class="btn primary" data-ingest="' + esc(d.id) + '">Ingest ' + esc(d.symbol || d.short_title) + '</button>').join(' ');
}
function startIngest(id){
  const doc = byId[id];
  ing.doc = doc; ing.takeaways = []; ing.failed = []; ing.dropped = 0; ing.changes = []; ing.touched = [];
  ing.batches = chunk(doc.passages, 25);
  const chars = doc.passages.reduce((a,x) => a + x.text.length, 0);
  const calls = ing.batches.length;
  document.getElementById('ingest-work').innerHTML =
    '<h3 class="serif" style="font-size:21px">Step 1 · Scope: the whole document</h3>'
    + '<p>All ' + doc.passages.length + ' passages will be sent, in batches of 25 (' + calls + ' calls), ' + chars.toLocaleString() + ' characters; nothing is held back.</p>'
    + '<table><caption>FIG.01 · Batches</caption><thead><tr><th scope="col">Batch</th><th scope="col">Paragraphs</th><th scope="col">PDF pages</th></tr></thead><tbody>'
    + ing.batches.map((b,i) => {
        const ps = b.map(x => x.paragraph || ('p.' + x.page_label));
        const pgs = [...new Set(b.map(x => x.page))];
        return '<tr><td>' + (i+1) + ' of ' + calls + '</td><td>' + esc(ps[0]) + ' – ' + esc(ps[ps.length-1]) + '</td><td>' + pgs.join(', ') + '</td></tr>';
      }).join('') + '</tbody></table>'
    + '<button class="btn primary" id="ingest-start">Start</button>';
  document.getElementById('ingest-start').onclick = runBatches;
  markRunning(true);
}
function nearest(doc, page, quote){
  const qw = norm(quote).split(' ').filter(Boolean);
  let best = null, bestRun = 0;
  for(const x of doc.passages){
    if(x.page !== page) continue;
    const xw = norm(x.text).split(' ');
    let max = 0;
    for(let i = 0; i < qw.length; i++) for(let j = 0; j < xw.length; j++){
      let k = 0; while(i+k < qw.length && j+k < xw.length && qw[i+k] === xw[j+k]) k++;
      if(k > max) max = k;
    }
    if(max > bestRun){ bestRun = max; best = x; }
  }
  return best ? {passage:best, run:bestRun} : null;
}
async function runBatches(){
  stopFlag = false;
  document.getElementById('ingest-stop').hidden = false;
  const doc = ing.doc;
  for(let i = 0; i < ing.batches.length; i++){
    if(stopFlag) break;
    const b = ing.batches[i];
    prog('batch ' + (i+1) + ' of ' + ing.batches.length + ' · ' + Math.min((i+1)*25, doc.passages.length) + ' of ' + doc.passages.length + ' passages have left the browser');
    const payload = b.map(x => ({id:x.id, page:x.page, paragraph:x.paragraph, text:x.text}));
    const prompt = 'You read one batch of a document into a research wiki. PIN SYNTAX: [label](pin:id#pPAGE "quote") ✓ — quote only words that stand in the passages given; the code will check every quotation.\n\nPASSAGES (JSON):\n' + JSON.stringify(payload) + '\n\nINDEX OF THE WIKI:\n' + W.index + '\n\nReturn JSON only: {"takeaways": [{"claim": "one sentence", "quote": "8 to 40 words copied verbatim from ONE passage above", "passage": "the id of that passage", "pages": ["slugs from the index this claim bears on"]}]}, at most 10 takeaways.';
    const r = await askModel(prompt, {passages: b.length});
    if(!r.parsed){
      document.getElementById('ingest-work').insertAdjacentHTML('beforeend', rawBox(r.raw, runBatches));
      break;
    }
    const tas = (r.parsed && r.parsed.takeaways) || [];
    for(const t of tas){
      const passage = doc.passages.find(x => x.id === t.passage);
      if(!passage){ ing.dropped++; continue; }
      const pinStr = newPin(doc.id, passage, t.quote || '');
      const m = pinStr.match(pinRe());
      const pin = {label:m[1], id:m[2], page:+m[3], quote:m[4]||'', mark:m[5], raw:pinStr};
      pin._v = verifyPin(pin);
      const pages = (t.pages || []).filter(s => bySlug[s]);
      const rec = {claim:t.claim || '', quote:t.quote || '', passage, pages, pin, ok:pin._v.ok};
      if(pin._v.ok) ing.takeaways.push(rec);
      else { rec.nearest = nearest(doc, passage.page, t.quote || ''); ing.failed.push(rec); }
    }
  }
  document.getElementById('ingest-stop').hidden = true;
  prog(''); markRunning(false);
  showStep2();
}
function showStep2(){
  const work = document.getElementById('ingest-work');
  const rows = ing.takeaways.map(t =>
    '<tr><td>' + esc(t.claim) + '</td><td class="pq">“' + esc(t.quote) + '”</td><td class="mono">' + (t.passage.paragraph != null ? 'para. ' + esc(t.passage.paragraph) : 'p. ' + esc(t.passage.page_label)) + ' · PDF p. ' + t.passage.page + '</td><td>' + t.pages.map(s => '<button class="chip" data-page="' + esc(s) + '">' + esc(bySlug[s] ? bySlug[s].title : s) + '</button>').join(' ') + '</td><td class="ok">✓ verified</td></tr>').join('');
  const failed = ing.failed.map(f => {
    const ci = CHIP_REG.length; CHIP_REG.push({pin:{id:ing.doc.id, page:f.passage.page, quote:f.quote}});
    return '<div style="margin:8px 0"><p><strong>Claim:</strong> ' + esc(f.claim) + '</p><p class="pq">“' + esc(f.quote) + '”</p><p class="mono">model named ' + esc(f.passage.id) + ' · nearest passage on PDF page ' + f.passage.page + ' shares ' + (f.nearest ? f.nearest.run : 0) + ' consecutive words</p><button class="chip" data-chip="' + ci + '">Open the PDF page</button></div>';
  }).join('');
  work.innerHTML =
    '<h3 class="serif" style="font-size:21px">Step 2 · Takeaways (' + ing.takeaways.length + ' verified, ' + ing.failed.length + ' could not verify' + (ing.dropped ? ', ' + ing.dropped + ' dropped (passage not sent)' : '') + ')</h3>'
    + '<table><caption>FIG.02 · Takeaways returned by the model, verified by this page</caption><thead><tr><th scope="col">Claim</th><th scope="col">Quote</th><th scope="col">Passage</th><th scope="col">Pages it would touch</th><th scope="col">Verification</th></tr></thead><tbody>' + (rows || '<tr><td colspan="5" class="quiet">none</td></tr>') + '</tbody></table>'
    + '<div class="greybox"' + (ing.failed.length ? '' : ' hidden') + '><strong>Could not verify: ' + ing.failed.length + '</strong> — these claims are in no change card and in no later prompt.' + failed + '</div>'
    + '<h3 class="serif" style="font-size:21px">Step 3 · Drafts</h3>'
    + '<button class="btn primary" id="draft-source">Draft the source page (1 call)</button>'
    + '<div id="draft-out"></div>';
  document.getElementById('draft-source').onclick = draftSource;
}
async function draftSource(){
  stopFlag = false; markRunning(true);
  const doc = ing.doc;
  const verified = ing.takeaways;
  const prompt = 'Draft the SOURCE PAGE of this document for the research wiki. PIN SYNTAX: [label](pin:id#pPAGE "quote") ✓ — copy the pins below EXACTLY; the code re-verifies every quotation.\n\nDOCUMENT: ' + doc.title + ' — ' + (doc.author || '') + ', ' + doc.published + ', ' + doc.pages + ' PDF pages, ' + doc.url + '\nCITE-AS for pins: ' + citeAs(doc.id) + '\n\nVERIFIED TAKEAWAYS WITH PINS:\n' + verified.map(t => '- ' + t.claim + '\n  ' + t.pin.raw).join('\n') + '\n\nA source page has: Full cite, Register, One-liner, Key takeaways, How NOT to read this, Where it feeds the wiki, Related.\n\nReturn JSON only: {"one_liner": "...", "body": "markdown, at most 900 words, only the pins given, copied exactly", "touches": [{"slug": "...", "why": "..."}]}';
  prog('drafting the source page · 1 call · ' + prompt.length.toLocaleString() + ' characters');
  const r = await askModel(prompt, {});
  prog(''); markRunning(false);
  if(!r.parsed){ document.getElementById('draft-out').innerHTML = rawBox(r.raw, draftSource); return; }
  const slug = kebab(doc.id);
  const stub = bySlug[slug] && bySlug[slug].frontmatter.sources && bySlug[slug].frontmatter.sources[0] === doc.id ? bySlug[slug] : null;
  const body = '# ' + (doc.short_title || doc.title) + '\n\n' + (r.parsed.body || '');
  const links = [...body.matchAll(/\[\[([^\]|#]+)\]\]/g)].map(m => m[1]).filter(s => bySlug[s]);
  const page = {slug, type:'source', title:doc.short_title || doc.title,
    frontmatter:{title:doc.short_title || doc.title, type:'source', tags:[], register:stub ? stub.frontmatter.register : ['c'], status:'draft', updated:today(), links, sources:[doc.id]}, body};
  ing.changes.push({slug, kind:stub ? 'edited' : 'new', page, newBody:body, oldBody:stub ? stub.body : null, contested:null, stub:!!stub});
  const touched = [...new Set([].concat((r.parsed.touches || []).map(t => t.slug).filter(s => bySlug[s]), ing.takeaways.flatMap(t => t.pages)))];
  if(stub && !touched.includes(stub.slug)) touched.push(stub.slug);
  ing.touched = touched.filter(s => s !== slug).slice(0, 12);
  document.getElementById('draft-out').innerHTML =
    '<p class="mono">source page drafted (' + (stub ? 'replaces the stub [[' + stub.slug + ']]' : 'new page [[' + slug + ']]') + ') · ' + ing.touched.length + ' pages would be touched</p>'
    + '<button class="btn primary" id="draft-touched">Draft the changes to ' + ing.touched.length + ' pages (' + ing.touched.length + ' calls)</button>';
  document.getElementById('draft-touched').onclick = runTouched;
}
function insertAfterHeading(body, after, md){
  if(!after || after === 'end') return body.replace(/\s*$/, '') + '\n\n' + md + '\n';
  const lines = body.split('\n');
  const idx = lines.findIndex(l => l.trim() === after || l.trim().replace(/^#+\s*/, '') === after);
  if(idx < 0) return body.replace(/\s*$/, '') + '\n\n<!-- inserted at end: heading not found: ' + esc(after) + ' -->\n' + md + '\n';
  const lv = (lines[idx].match(/^#+/) || ['#'])[0].length;
  let end = lines.length;
  for(let i = idx+1; i < lines.length; i++){ const m = lines[i].match(/^(#+)\s/); if(m && m[1].length <= lv){ end = i; break; } }
  lines.splice(end, 0, md);
  return lines.join('\n');
}
async function runTouched(){
  stopFlag = false; markRunning(true);
  document.getElementById('ingest-stop').hidden = false;
  for(const slug of ing.touched){
    if(stopFlag) break;
    const page = bySlug[slug]; if(!page) continue;
    const rel = ing.takeaways.filter(t => t.pages.includes(slug));
    const prompt = 'You edit one page of a research wiki with new verified evidence. PIN SYNTAX: [label](pin:id#pPAGE "quote") ✓ — copy pins EXACTLY; the code re-verifies every quotation.\n\nPAGE [[' + slug + ']]:\n' + page.body + '\n\nNEW EVIDENCE:\n' + (rel.map(t => '- ' + t.claim + '\n  ' + t.pin.raw).join('\n') || '(none)') + '\n\nReturn JSON only: {"edits": [{"after": "an existing heading of the page, or \"end\"", "markdown": "..."}], "contested": "a full contested block only if this document disagrees with the page, otherwise null"}. At most 300 words across all edits.';
    prog('drafting changes to ' + slug + ' · ' + prompt.length.toLocaleString() + ' characters');
    const r = await askModel(prompt, {});
    if(!r.parsed){ document.getElementById('ingest-work').insertAdjacentHTML('beforeend', rawBox(r.raw, runTouched)); break; }
    let newBody = page.body;
    for(const e of (r.parsed.edits || [])) newBody = insertAfterHeading(newBody, e.after, e.markdown || '');
    let contested = r.parsed.contested || null;
    if(contested) newBody += '\n\n```contested\n' + String(contested).replace(/^```contested\n?/, '').replace(/```\s*$/, '') + '\n```\n';
    ing.changes.push({slug, kind:'edited', newBody, oldBody:page.body, contested});
  }
  document.getElementById('ingest-stop').hidden = true;
  prog(''); markRunning(false);
  showReview();
}
function showReview(){
  const work = document.getElementById('ingest-work');
  work.innerHTML = '<h3 class="serif" style="font-size:21px">Step 4 · Review and file</h3>'
    + '<p class="mono hint">nothing is written until Approve is pressed · a rejected page stays exactly as loaded</p>'
    + '<div id="cards"></div>'
    + '<button class="btn primary" id="file-changes" disabled>File the approved changes</button>'
    + '<div class="mono" id="file-out" aria-live="polite" style="margin-top:10px"></div>';
  const cards = document.getElementById('cards');
  ing.changes.forEach((c, i) => {
    const newBody = c.newBody || c.page.body;
    const oldLines = c.oldBody ? c.oldBody.split('\n') : [];
    const oldSet = {}; oldLines.forEach(l => oldSet[l] = (oldSet[l]||0)+1);
    const ins = new Set();
    newBody.split('\n').forEach(l => { if(oldSet[l] > 0) oldSet[l]--; else ins.add(l); });
    const pins = [...newBody.matchAll(pinRe())].map(m => ({label:m[1], id:m[2], page:+m[3], quote:m[4]||'', mark:m[5], raw:m[0]}));
    pins.forEach(pn => pn._v = verifyPin(pn));
    const okN = pins.filter(p => p._v.ok).length;
    const title = c.page ? c.page.title : (bySlug[c.slug] ? bySlug[c.slug].title : c.slug);
    const fs = document.createElement('fieldset');
    fs.className = 'card';
    fs.innerHTML = '<legend>Change ' + (i+1) + ' of ' + ing.changes.length + ' · ' + esc(title) + ' (' + (c.kind === 'new' ? 'new page' : 'edited') + (c.stub ? ', replaces the stub' : '') + ')</legend>'
      + '<div class="mono">' + ins.size + ' lines inserted · ' + pins.length + ' pins added: ' + okN + ' verified, ' + (pins.length - okN) + ' not verified</div>'
      + '<div class="diff body" style="margin:10px 0">' + renderMD(newBody, {ins}) + '</div>'
      + '<button class="btn" data-approve="' + i + '">Approve change ' + (i+1) + ' of ' + ing.changes.length + '</button>'
      + '<button class="btn" data-reject="' + i + '">Reject change ' + (i+1) + ' of ' + ing.changes.length + '</button>'
      + '<div class="mono" id="dec-' + i + '" aria-live="polite"></div>';
    cards.appendChild(fs);
  });
  document.getElementById('file-changes').onclick = fileIngest;
}
function decide(i, val){
  ing.changes[i].decision = val;
  document.getElementById('dec-' + i).textContent = val === 'approve' ? 'approved — will be written when you file' : 'rejected — stays exactly as loaded, noted in the log';
  document.getElementById('file-changes').disabled = !ing.changes.every(c => c.decision);
}
function updateIndexLine(slug){
  const p = bySlug[slug];
  const n = p._pins.filter(x => x._v.ok).length;
  const regs = (p.frontmatter.register || []).join('');
  const line = '- [[' + slug + ']] — ' + (p.frontmatter.title || p.title) + ' · (' + regs + ') · ✓' + n;
  const lines = W.index.split('\n');
  const i = lines.findIndex(l => l.includes('[[' + slug + ']]'));
  if(i >= 0){ lines[i] = line; W.index = lines.join('\n'); }
  else W.index = W.index.replace(/\s*$/, '') + '\n' + line + '\n';
}
function fileIngest(){
  const approved = ing.changes.filter(c => c.decision === 'approve');
  const rejected = ing.changes.filter(c => c.decision === 'reject');
  approved.forEach(c => {
    const body = c.newBody || c.page.body;
    if(c.kind === 'new' || !bySlug[c.slug]){
      const p = c.page; P.push(p); bySlug[p.slug] = p; recompute(p);
    } else {
      const p = bySlug[c.slug];
      p.body = body; p.frontmatter.updated = today();
      if(!p.frontmatter.sources.includes(ing.doc.id)) p.frontmatter.sources.push(ing.doc.id);
      recompute(p);
    }
    session.changedSlugs.push(c.slug);
    updateIndexLine(c.slug);
  });
  const sym = ing.doc.symbol || (ing.doc.author + ' ' + ing.doc.year);
  W.log += '\n\n## [' + today() + '] ingest | ' + sym + ': ' + (ing.doc.short_title || ing.doc.title)
    + '\n\nRead ' + ing.doc.passages.length + ' passages (' + citeAs(ing.doc.id) + ', register (' + docRegister(ing.doc.id) + ')). Approved: ' + (approved.map(c => '[[' + c.slug + ']]').join(', ') || 'none') + '. Rejected: ' + (rejected.map(c => '[[' + c.slug + ']]').join(', ') || 'none') + '.';
  session.logAdded++;
  approved.forEach(c => {
    if(c.contested){
      W.tensions += '\n\n### ' + kebab(c.slug) + '-claim\ntitle: contested claim on [[' + c.slug + ']]\nstatus: open\ncard: [[' + c.slug + ']]\n';
    }
  });
  ing.doc.status = 'ingested';
  session.changes += approved.length;
  updateHeader(); renderList(); renderIngestHome();
  document.getElementById('file-out').textContent = 'Filed ' + approved.length + ' change(s) (' + rejected.length + ' rejected). The document is now ingested; Lint re-runs on tab 04.';
}

/* ---------- tab 04: check ---------- */
function lint(){
  const res = [];
  const push = (name, items) => res.push({name, n:items.length, items});
  let d = []; P.forEach(p => p._links.forEach(s => { if(!bySlug[s]) d.push({page:p.slug, ref:s}); }));
  push('Dangling [[links]]', d);
  let o = []; P.forEach(p => { if(!(backlinks[p.slug] || []).length) o.push({page:p.slug}); });
  push('Orphan pages (nothing links to them)', o);
  let nv = []; P.forEach(p => p._pins.forEach(pn => { if(!pn._v.ok) nv.push({page:p.slug, ref:pn.raw.slice(0,70)}); }));
  push('Pins not verified by this page', nv);
  let f = []; P.forEach(p => p._pins.forEach(pn => { if(pn.mark === '✓' && !pn._v.ok) f.push({page:p.slug}); }));
  push('Pins marked ✓ that fail verification', f);
  let s = []; P.forEach(p => {
    const a = [...new Set(p._pins.map(x => x.id))].sort().join(',');
    const b = (p.frontmatter.sources || []).slice().sort().join(',');
    if(a !== b) s.push({page:p.slug, ref:'sources [' + b + '] vs pinned [' + a + ']'});
  });
  push('frontmatter.sources differ from pinned documents', s);
  let np = []; P.forEach(p => { if(!p._pins.length) np.push({page:p.slug}); });
  push('Pages with no pins', np);
  let r = []; P.forEach(p => (p.frontmatter.links || []).forEach(l => { const t = bySlug[l]; if(t && !(t.frontmatter.links || []).includes(p.slug)) r.push({page:p.slug, ref:l}); }));
  push('frontmatter.links not reciprocated', r);
  const idxSlugs = [...W.index.matchAll(/\[\[([^\]]+)\]\]/g)].map(m => m[1]);
  let ic = []; P.forEach(p => { if(!idxSlugs.includes(p.slug)) ic.push({page:p.slug, ref:'missing from index'}); });
  idxSlugs.forEach(s => { if(!bySlug[s]) ic.push({page:s, ref:'index line without a page'}); });
  push('Index and pages disagree', ic);
  let im = []; W.index.split('\n').forEach(l => {
    const m = l.match(/\[\[([^\]]+)\]\][^\n]*✓\s?(\d+)/);
    if(m && bySlug[m[1]]){ const n = bySlug[m[1]]._pins.filter(x => x._v.ok).length; if(+m[2] !== n) im.push({page:m[1], ref:'index says ✓' + m[2] + ', computed ' + n}); }
  });
  push('Index ✓N differs from the computed count', im);
  const tens = [...W.tensions.matchAll(/card:\s*\[\[([^\]]+)\]\]/g)].map(m => m[1]);
  const withC = P.filter(p => (p.body.match(/```contested/g) || []).length).map(p => p.slug);
  let cc = [];
  withC.forEach(s => { if(!tens.includes(s)) cc.push({page:s, ref:'contested card without a tensions entry'}); });
  tens.forEach(s => { if(!withC.includes(s)) cc.push({page:s, ref:'tensions entry without a contested card'}); });
  push('Contested cards and tensions entries disagree', cc);
  let st = []; P.forEach(p => { if(p.frontmatter.status === 'stub') st.push({page:p.slug}); });
  push('Stub pages', st);
  let ib = []; P.forEach(p => p._pins.forEach(pn => { const d = byId[pn.id]; if(d && d.status === 'inbox') ib.push({page:p.slug, ref:pn.id}); }));
  push('Pins to a document still in the inbox', ib);
  return res;
}
function renderCheck(){
  document.getElementById('check-num').textContent = verifiedPins() + ' of ' + totalPins() + ' pins verified by this page';
  const res = lint();
  const need = res.filter(c => c.n > 0).length;
  document.getElementById('check-sub').textContent = need + ' lint checks need a look';
  document.getElementById('lint-body').innerHTML = res.map(c =>
    '<tr><td>' + esc(c.name) + '</td><td class="' + (c.n ? 'bad' : 'ok') + '">' + (c.n === 0 ? '0 · pass' : c.n + ' · check') + '</td><td>'
    + c.items.slice(0, 12).map(it => it.page ? '<button class="chip" data-page="' + esc(it.page) + '">' + esc(it.page) + (it.ref ? ' · ' + esc(it.ref) : '') + '</button>' : esc(it.ref || '')).join(' ')
    + (c.items.length > 12 ? ' …' : '') + '</td></tr>').join('');
  const idxM = W.index.match(/(\d[\d,]*) pins/);
  const stated = idxM ? +idxM[1].replace(/,/g, '') : null;
  const found = totalPins(), ver = verifiedPins();
  const dangling = res[0].n, orphans = res[1].n, srcBad = res[4].n;
  document.getElementById('selfcheck-list').innerHTML =
    '<p>· Pins found by the regular expression: ' + found + ' · the index states ' + (stated == null ? 'no number' : stated) + ' · <span class="' + (found === stated ? 'ok' : 'bad') + '">' + (found === stated ? 'pass' : 'check') + '</span></p>'
    + '<p>· Verified by this page\'s code: ' + ver + ' of ' + found + ' · every verified pin\'s label matches its passage\'s paragraph or page label</p>'
    + '<p>· Structure: dangling links ' + dangling + ' · orphans ' + orphans + ' · sources equal pinned documents on every page: ' + (srcBad ? '<span class="bad">check</span>' : '<span class="ok">pass</span>') + '</p>'
    + '<p>· Session: log entries added this session ' + session.logAdded + ' · changes this session ' + session.changes + ' · a failing check never hides a page or a pin</p>'
    + '<p>· The schema\'s reading for contradictions is named here and is not done by code.</p>';
}
document.getElementById('lint-btn').onclick = () => {
  renderCheck();
  document.getElementById('lint-btn').textContent = 'Re-run';
};

/* ---------- tab 05: record ---------- */
const origLogCount = W.log.split(/(?=^## )/m).filter(s => s.trim()).length;
function renderRecord(){
  const entries = W.log.split(/(?=^## )/m).filter(s => s.trim()).map((t, i) => ({t, session:i >= origLogCount}));
  const list = document.getElementById('log-order').checked ? [...entries].reverse() : entries;
  document.getElementById('log-view').innerHTML = list.map(e => {
    const m = e.t.match(/^## \[[^\]]+\] [^\n]*/);
    const head = m ? m[0].slice(3) : 'entry';
    const rest = e.t.slice(m ? m[0].length : 0);
    return '<details class="logentry"><summary><span class="mono">' + esc(head) + '</span>' + (e.session ? ' <span class="tag red">this session</span>' : '') + '</summary><div class="body">' + renderMD(rest, {}) + '</div></details>';
  }).join('');
  document.getElementById('tensions-view').innerHTML = renderMD(W.tensions, {});
  document.getElementById('rec-source').textContent = 'Source: ' + W.source + ' · built ' + W.built;
  document.getElementById('dl-changed').hidden = session.changedSlugs.length === 0;
}
document.getElementById('log-order').addEventListener('change', renderRecord);
function dl(name, text, type){
  const b = new Blob([text], {type: type || 'application/json'});
  const a = document.createElement('a');
  a.href = URL.createObjectURL(b); a.download = name;
  document.body.appendChild(a); a.click();
  setTimeout(() => { URL.revokeObjectURL(a.href); a.remove(); }, 500);
}
document.getElementById('dl-wiki').onclick = () => {
  const data = {title:W.title, source:W.source, built:W.built, count:P.length, schema:W.schema,
    pages:P.map(p => ({slug:p.slug, type:p.type, title:p.title, frontmatter:p.frontmatter, body:p.body})),
    index:W.index, log:W.log, tensions:W.tensions,
    changes:session.changedSlugs.map(s => ({slug:s, date:today(), kind:'approved'})),
    library_status:D.map(d => ({id:d.id, status:d.status}))};
  dl('wiki-' + today() + '.json', JSON.stringify(data, null, 2));
};
document.getElementById('dl-changed').onclick = () => {
  const seen = new Set();
  const md = session.changedSlugs.filter(s => { if(seen.has(s) || !bySlug[s]) return false; seen.add(s); return true; })
    .map(s => pageMarkdown(bySlug[s])).join('\n\n---\n\n');
  dl('wiki-changed-' + today() + '.md', md, 'text/markdown');
};

/* ---------- global click delegation ---------- */
document.addEventListener('click', e => {
  const t = e.target.closest('[data-page]');
  if(t){ e.preventDefault(); showTab('pages'); selectPage(t.dataset.page); return; }
  const c = e.target.closest('[data-chip]');
  if(c){ const r = CHIP_REG[+c.dataset.chip]; if(r && r.pin) studio.openSource(r.pin.id, r.pin.page, r.pin.quote); return; }
  const m = e.target.closest('[data-more]');
  if(m){ const d = m.parentElement.querySelector('.pdetail'); if(d){ d.hidden = !d.hidden; m.setAttribute('aria-expanded', String(!d.hidden)); } return; }
  const g = e.target.closest('[data-goto]');
  if(g){ showTab(g.dataset.goto); return; }
  const cp = e.target.closest('[data-copy]');
  if(cp){ copyText(pageMarkdown(bySlug[cp.dataset.copy])); cp.textContent = 'Copied'; setTimeout(() => cp.textContent = 'Copy page as markdown', 1500); return; }
  const ig = e.target.closest('[data-ingest]');
  if(ig){ startIngest(ig.dataset.ingest); return; }
  const ap = e.target.closest('[data-approve]');
  if(ap){ decide(+ap.dataset.approve, 'approve'); return; }
  const rj = e.target.closest('[data-reject]');
  if(rj){ decide(+rj.dataset.reject, 'reject'); return; }
  const rt = e.target.closest('[data-retry]');
  if(rt){ const box = rt.closest('.rawbox'); if(box) box.remove(); return; }
});
document.getElementById('ingest-stop').onclick = () => { stopFlag = true; };

/* ---------- init ---------- */
document.getElementById('foot').textContent = W.source + ' · built ' + W.built + ' · Counting, matching and verification are done by this page\'s code; the model is called only when you press Ask, Ingest or a retry button.';
updateHeader();
askAnnounce();
renderList();
renderIngestHome();
renderCheck();
renderRecord();
document.getElementById('tab-pages').focus();
const h0 = decodeURIComponent(location.hash.slice(1));
showTab('pages');
if(bySlug[h0]) selectPage(h0); else renderIndex();
</script>
</body>
</html>
```