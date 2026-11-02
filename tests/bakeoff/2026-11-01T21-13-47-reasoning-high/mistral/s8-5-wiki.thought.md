Let me plan this app. It's a research wiki over WORKSHOP_DATA.un_library (9 General Comments, each with paragraphs). Features:

- Sidebar with concept pages: proportionality, legal capacity, surveillance, non-State actors, reasonable accommodation, access to information, deprivation of liberty. User can add a concept by typing a term.
- Concept page: grouped by document, every paragraph that uses the term (case-insensitive substring match on text), verbatim, with symbol, paragraph number, and a link "¶ 12 · p. 5" calling studio.openSource(symbol, page).
- Related concepts: other concepts found in the same paragraphs, as links.
- "Draft a summary" button: sends page's paragraphs (max 12) to studio.ask, asks for three sentences each ending with citation like (CCPR/C/GC/37, para. 40). Mark summary with data-source="ai", say how many paragraphs sent and that they left the browser. Show progress, allow stop? The instructions say batch at most 25 records per call, show progress, let user stop. Here max 12 paragraphs in one call — fine. Show "sending N paragraphs to the model…" and a stop button maybe. Since it's a single call, a simple "cancel" flag. I'll implement a stop button that sets a flag; after await resolves, if cancelled, don't render. Also render AI values in elements with data-source="ai".
- Never call studio.ask on page load — only on button click. Good.

Design: clean, sidebar left, main content right. Hash routing so concept links work (#/concept/proportionality). Custom concepts stored in memory (and maybe localStorage? Sandbox offline — localStorage should work, but keep it simple; in-memory is fine, maybe persist in localStorage guarded by try/catch).

Matching: term matching should be case-insensitive; for multi-word terms like "non-State actors" maybe also match "non-state actors" — normalize hyphens/case. I'll normalize text: lowercase, replace non-alphanumeric with space? That could break "non-State". Simple approach: lowercase both, and also try replacing "-" with " " variants. I'll do a normalized match: lowercase, collapse whitespace, and compare with term normalized similarly; also match term with hyphens replaced by space against text with hyphens replaced by space. Keep it simple: normalize by lowercasing and replacing [-–—] with space, collapse spaces. That handles "non-State actors" vs "non-state actors" vs "non state actors".

Concept page shows grouped by document: for each doc (in library order), paragraphs containing term. Each paragraph row: symbol link (doc_url), "¶ N · p. P" button calling studio.openSource(symbol, page), verbatim text (maybe in a <details> or just shown; requirement says keep full text available click to expand — here show verbatim; could show full text directly since paragraphs are short-ish, but rule says "Keep the full text of a paragraph available (click to expand)". I'll show first ~200 chars with expand toggle, or use <details>. Simpler: show full text in a blockquote-ish; but rule says click to expand. Use a <details> with summary showing ¶ number and first line? The link "¶ 12 · p. 5" must be visible. I'll render: header line with symbol link + "¶ 12 · p. 5" button, then text in a collapsible <details open?> — maybe collapsed by default with "show text". Actually for a wiki, showing text directly is nicer; but rule: "Keep the full text of a paragraph available (click to expand); never paraphrase it." I'll use <details> with summary "¶ 12 · p. 5 — show paragraph text" plus separate openSource link. Hmm, requirement: 'a link "¶ 12 · p. 5" that opens the PDF at that page with studio.openSource(symbol, page)'. So the link text is "¶ 12 · p. 5". I'll make that an <a href="#" onclick> calling openSource, plus doc symbol link to doc_url. Text in <details> expanded? I'll make details open by default for the first few? Keep simple: <details open> maybe too long. I'll do details closed with summary "Paragraph text (verbatim)". Actually simpler and compliant: show the text in a <details> element; summary contains the ¶ link. Let me structure:

```
<div class="para">
  <div class="para-head">
    <a class="sym" href=doc_url target=_blank>CCPR/C/GC/37</a>
    <a class="pg" href="#" data-symbol data-page>¶ 40 · p. 12</a>
  </div>
  <details><summary>Show verbatim text</summary><p>text</p></details>
</div>
```

Hmm, but "shows every paragraph that uses the term, verbatim" — maybe show text directly. The global rule says click to expand. I'll use details with open attribute? If many paragraphs, page long. I'll leave details closed but summary shows first ~80 chars? Summary can't easily contain the ¶ link then. I'll do: head line with symbol + ¶ link, then details (closed) "verbatim text". That satisfies both. Actually to make the page useful at a glance, maybe open the details for paragraphs — but rule explicitly says click to expand. Keep closed.

Related concepts: for the current concept's matched paragraphs, find which other concepts (from the concept list, including custom) appear in those paragraphs; list as links to their pages. Exclude the current concept itself.

Summary button: gather matched paragraphs (all, but send at most 12 — take first 12 across documents), build prompt: "Below are N verbatim paragraphs from UN General Comments... Write exactly three sentences summarizing... Each sentence must end with a citation in the form (SYMBOL, para. N) referring to the paragraph(s) it rests on. Paragraphs: ..." Then await studio.ask(prompt, {json:true})? The user said "sends ... with await studio.ask(prompt), asking for three sentences". Could ask for JSON: {"sentences": [...]} with json:true, parse, survive invalid JSON (fallback: show raw text). I'll ask for JSON with sentences array, each sentence ending with citation. Render each sentence in <li data-source="ai">. Show note: "AI summary — N paragraphs sent to the model (they left your browser)." Also a stop button: set cancelled flag; while awaiting show spinner "Waiting for the model… (N paragraphs sent)" and a Cancel button; after resolve, if cancelled show "cancelled". Since single call, that's adequate "let the user stop".

Also must say on screen how many records sent and that they left the browser — do that when sending.

Sidebar: list of concepts as links; input + "Add" button to add a concept term. Concepts stored in array; default seven. Custom concepts added go to list (persist via localStorage try/catch). Active concept highlighted. Home page: overview — list documents with counts, maybe. Start page could be first concept or an intro. I'll make a home view describing the wiki, listing the nine documents with paragraph counts and links to... maybe each document page? Not required. Keep home simple: intro + concept list + documents list. Clicking a concept shows its page.

Routing: use location.hash like #/c/<encoded term>. On hashchange render. Default route: home or first concept. I'll default to home.

Counts: show "n paragraphs in m documents" for the concept, with "How this is computed" note: "Case-insensitive search for 'term' (hyphens treated as spaces) across all N paragraphs of the 9 General Comments in WORKSHOP_DATA.un_library."

Data reading: WORKSHOP_DATA.un_library.records — array of docs with symbol, title, short_title, committee, year, doc_url, pages, paragraphs[{id, paragraph, page, text, cited_articles}]. Handle missing fields gracefully.

studio.openSource(symbol, page) — call on click of ¶ link; prevent default. Guard if studio.openSource undefined? It's provided. Wrap in try/catch and fallback window.open(doc_url)? Just call it.

Chart not needed. No Chart.js needed.

Line budget ~ under 700 lines. Fine.

Let me write the HTML.

Key JS:

```js
const LIB = (window.WORKSHOP_DATA && window.WORKSHOP_DATA.un_library) || {records: []};
const docs = LIB.records || [];
const allParas = []; docs.forEach(d => (d.paragraphs||[]).forEach(p => allParas.push({doc:d, ...p})));
```

normalize(s): String(s||'').toLowerCase().replace(/[\u2010-\u2015-]/g,' ')... careful: replace hyphen-like chars with space, then collapse whitespace: .replace(/[^a-z0-9]+/g,' ').trim(). Then term normalized similarly; match if normText.includes(normTerm). For single-word terms fine.

Concepts: default list; load custom from localStorage 'wiki-concepts' try/catch; save on add. Validate term non-empty, not duplicate (case-insensitive).

renderConcept(term): find matches: allParas.filter(p => norm(p.text).includes(norm(term))). Group by doc preserving doc order. For each doc group: heading with symbol link + short_title + committee/year; paragraphs list. Related concepts: for each other concept c (all concepts except current), if any matched para text includes norm(c) → include. Render as links.

Summary: collect matched paras (flattened, doc order), slice(0,12). Build prompt with numbered paragraphs: `[SYMBOL, para. N, p. P] text`. Ask: "You are given N verbatim paragraphs... Return JSON: {"sentences": ["...", "...", "..."]} with exactly three sentences; each sentence must end with a citation like (CCPR/C/GC/37, para. 40) naming the paragraph(s) it rests on. Do not invent content." Call studio.ask(prompt, {json:true}). Parse JSON; if fail, treat raw as text split into sentences? Fallback: display raw string in ai element. Render sentences as list items each with data-source="ai". Note element: `AI-generated summary — ${n} paragraphs were sent to the model and left your browser.` also with data-source="ai"? The note about count is our own; the summary content is AI. Put data-source="ai" on the summary container. The "how many sent" note can be plain but I'll also mark container.

Progress/stop: on click, disable button, show status "Sending 12 paragraphs to the model… (they have left your browser)" with Cancel button. cancelled flag; await; if cancelled → status "Cancelled — no summary shown." else render.

Escape HTML when injecting text — use textContent via createElement or escape function. I'll build DOM with helper el(tag, cls, text) using textContent to avoid injection.

Sidebar: nav list; input form. Also "Home" link.

Header: title "General Comments Research Wiki", description line: source — "Nine General Comments from the UN library (WORKSHOP_DATA.un_library), N paragraphs, years X–Y" computed from data. Compute min/max year, total paragraphs.

How-this-is-computed note near concept results.

Let me also handle empty matches: "No paragraph uses the term 'x'." plus note.

Hash routing: `#/c/` + encodeURIComponent(term). On add concept, navigate to it.

Write code now. Keep CSS clean: sidebar fixed width 260px, main flexible, accent #1f6fb2, background #f7f9fb, base 16px.

Paragraph row styling: card with border-left accent.

Details/summary styling.

Let me draft the full file.

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>General Comments Research Wiki</title>
<style> ... </style>
</head>
<body>
<header>...</header>
<div class="layout">
  <aside>
    <nav id="conceptNav"></nav>
    <form id="addForm"><input id="addInput" placeholder="Add a concept…"><button>Add</button></form>
    <p class="hint">Concepts are matched case-insensitively; hyphens count as spaces.</p>
  </aside>
  <main id="main"></main>
</div>
<script> ... </script>
</body>
</html>
```

JS details:

```js
const DATA = window.WORKSHOP_DATA || {};
const LIB = DATA.un_library || {};
const docs = Array.isArray(LIB.records) ? LIB.records : [];
const paras = [];
docs.forEach(d => (d.paragraphs||[]).forEach(p => paras.push({doc:d, para:p})));

const DEFAULT_CONCEPTS = ["proportionality","legal capacity","surveillance","non-State actors","reasonable accommodation","access to information","deprivation of liberty"];
let concepts = DEFAULT_CONCEPTS.slice();
try { const saved = JSON.parse(localStorage.getItem('gcwiki.concepts')||'[]'); if(Array.isArray(saved)) saved.forEach(c=>{ if(typeof c==='string' && c.trim() && !concepts.some(x=>x.toLowerCase()===c.toLowerCase())) concepts.push(c.trim()); }); } catch(e){}

function norm(s){ return String(s==null?'':s).toLowerCase().replace(/[^a-z0-9]+/g,' ').trim(); }
function usesTerm(text, term){ const n=norm(text), t=norm(term); return t.length>0 && n.indexOf(t) !== -1; }
```

Wait: norm replaces non-alphanumeric with space — "non-State" → "non state". Term "non-State actors" → "non state actors". Text "non-State actors" → "non state actors". Match. Good. But substring matching across collapsed text: "deprivation of liberty" fine.

Edge: term with apostrophes fine.

el helper:

```js
function el(tag, cls, text){ const e=document.createElement(tag); if(cls) e.className=cls; if(text!=null) e.textContent=text; return e; }
```

renderNav(active): nav with Home link + concepts.

Route:

```js
function route(){
  const h = location.hash || '';
  const m = h.match(/^#\/c\/(.*)$/);
  if(m){ renderConcept(decodeURIComponent(m[1])); } else { renderHome(); }
}
window.addEventListener('hashchange', route);
```

renderHome: intro, stats (docs count, paragraphs count, years range), list of documents (symbol link, short_title, committee, year, paragraph count, pages), and concept list explanation.

renderConcept(term):
- main.innerHTML='' then build.
- h1: term (capitalize? keep as typed).
- meta line: "X paragraphs in Y of 9 documents match “term”." + how computed note: "Computed by a case-insensitive text search for “term” (hyphens treated as spaces) over all N paragraphs of the nine General Comments in the library. Counts are exact, not estimated."
- If none: message.
- Group: iterate docs in order; for each, matched = paras of doc using term; if any, section: header with symbol link (doc_url, target _blank), short_title, committee · year; then paragraph cards.
- Paragraph card: head: span "¶ N" + link "¶ N · p. P" (the required link text "¶ 12 · p. 5") — requirement: 'a link "¶ 12 · p. 5" that opens the PDF'. So the link text should be exactly "¶ 12 · p. 5". I'll make the link text `¶ ${p.paragraph} · p. ${p.page}` with href="#" and click → openSource. Also symbol link to doc_url. Then details with verbatim text; summary "Verbatim text". Maybe also cited_articles chips if present.
- Related concepts: compute set; render "Related concepts:" links `#/c/...`.
- Summary section: button "Draft a summary", status area, output area.

openSource handler: delegate clicks on document for `a[data-open]`:

```js
document.addEventListener('click', e=>{
  const a = e.target.closest('a[data-open]');
  if(a){ e.preventDefault(); const sym=a.getAttribute('data-symbol'), pg=a.getAttribute('data-page');
    try{ if(window.studio && studio.openSource) studio.openSource(sym, parseInt(pg,10)); }catch(err){}
  }
});
```

Summary logic:

```js
let cancel=false;
async function draftSummary(term, matches){
  const btn=..., status=..., out=...;
  const selected = matches.slice(0,12);
  const n = selected.length;
  btn.disabled=true; out.innerHTML='';
  status.textContent = `Sending ${n} paragraph${n===1?'':'s'} to the model — they have left your browser. Waiting for an answer…`;
  cancel=false; show cancel button...
```

Simpler: a cancel button element in status area; onclick sets cancel=true and status text "Cancelling…". After await:

```js
  const lines = selected.map((m,i)=>`[${i+1}] ${m.doc.symbol}, para. ${m.para.paragraph} (p. ${m.para.page}): ${m.para.text}`);
  const prompt = `Below are ${n} verbatim paragraphs from UN human rights treaty-body General Comments, all of which use the concept “${term}”.\n\n${lines.join('\n\n')}\n\nWrite exactly three sentences that summarize what these paragraphs say about “${term}”. Each sentence must end with a citation in parentheses naming the paragraph it rests on, in the form (SYMBOL, para. N), e.g. (CCPR/C/GC/37, para. 40). Use only what the paragraphs say; do not invent content. Reply as JSON only: {"sentences": ["sentence one (SYMBOL, para. N)", "sentence two (SYMBOL, para. N)", "sentence three (SYMBOL, para. N)"]}`;
  let answer;
  try{ answer = await studio.ask(prompt, {json:true}); }catch(err){ ... }
  if(cancel){ status.textContent='Cancelled — no summary was added.'; btn.disabled=false; return; }
  parse JSON: let sentences=null; try{ const j=JSON.parse(answer); if(j && Array.isArray(j.sentences)) sentences=j.sentences.map(String); }catch(e){}
  render: out: note el: `AI-written summary — ${n} paragraphs were sent to the model (they left your browser).` with data-source="ai" on the list; if sentences, ol of li data-source="ai"; else fallback: single p data-source="ai" with raw answer text.
  status.textContent = `Done — ${n} paragraphs sent.`;
  btn.disabled=false;
```

Note: "Render every value that came from studio.ask inside an element with the attribute data-source="ai"." So each sentence li gets data-source="ai". The count note is ours, fine either way; I'll put data-source="ai" on the container div of the summary output to be safe, plus each li.

Also "say on screen: how many records, and that they left the browser" — status does that at send time. Good.

Add concept form:

```js
form.onsubmit = e=>{ e.preventDefault(); const v=input.value.trim(); if(!v) return; if(!concepts.some(c=>c.toLowerCase()===v.toLowerCase())){ concepts.push(v); try{localStorage.setItem('gcwiki.concepts', JSON.stringify(concepts.slice(DEFAULT_CONCEPTS.length)));}catch(err){} } location.hash = '#/c/'+encodeURIComponent(v); input.value=''; };
```

Hmm storing only custom ones: store concepts beyond defaults. Fine.

renderNav after add — route() calls renderConcept which calls renderNav(activeTerm).

Sidebar nav: Home link `#/` plus each concept link `#/c/...`, class active if matches.

Also show count badge per concept in sidebar? Nice: compute matches count per concept — could be expensive but 9 docs, maybe ~1000 paragraphs total; fine. I'll compute counts lazily and cache. Let's compute counts for all concepts once (paras maybe ~800; 7+ concepts × 800 includes — trivial). Show small count next to each concept. Good touch.

Header description: `Source: ${LIB.source || 'UN library of nine General Comments'} — ${docs.length} documents, ${paras.length} paragraphs, ${minYear}–${maxYear}. Loaded from WORKSHOP_DATA.un_library.` Compute years from docs' year field, handle missing.

Now CSS. Layout: 

```css
*{box-sizing:border-box}
body{margin:0;font:16px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;background:#f6f8fa;color:#1c2733}
header{background:#fff;border-bottom:1px solid #e3e9ef;padding:18px 28px}
header h1{margin:0 0 4px;font-size:22px;color:#123a5c}
header p{margin:0;color:#4a5b6b;max-width:70em}
.layout{display:flex;min-height:calc(100vh - 90px)}
aside{width:270px;flex:0 0 270px;background:#fff;border-right:1px solid #e3e9ef;padding:18px 16px;position:sticky;top:0;align-self:flex-start;height:100vh;overflow:auto}
main{flex:1;padding:24px 32px;max-width:960px}
```

Sidebar nav links: block, padding, border-radius, active accent background #e8f1f9 color #1f6fb2.

Concept page: h1 term; .meta; .how note small; doc sections h2 with symbol link; para cards.

.para{background:#fff;border:1px solid #e3e9ef;border-left:4px solid #1f6fb2;border-radius:6px;padding:10px 14px;margin:10px 0}
.para-head{display:flex;gap:12px;align-items:baseline;flex-wrap:wrap}
a.pg{color:#1f6fb2;font-weight:600;text-decoration:none} hover underline.
details{margin-top:6px} summary{cursor:pointer;color:#1f6fb2}
.para-text{white-space:pre-wrap;background:#f6f8fa;padding:10px;border-radius:4px;margin:8px 0 0}

Related: .rel a chips.

Summary: button styles; .ai-note; ol li.

Status area with cancel button.

Buttons: .btn{background:#1f6fb2;color:#fff;border:0;border-radius:6px;padding:8px 14px;font-size:15px;cursor:pointer} disabled opacity.

Input: padding 8px, border, radius.

Home: doc list table-ish: each doc row card with symbol link, title, committee/year, "N paragraphs · M pages".

Also "How this is computed" near top of concept page and home.

Now write everything carefully. Also handle docs with missing paragraphs array. Handle p.page missing → show "p. ?" — use p.page ?? '—'. The link text format "¶ 12 · p. 5": `¶ ${p.paragraph} · p. ${p.page}`.

Cited articles: show as small chips if present.

Related concepts computation: for current term's matched paragraphs (all matches), for each concept c != term (compare normalized), if any match para uses c → related. Sort alphabetically? Keep sidebar order. I'll keep concepts order.

Also on concept page, maybe show which documents matched count.

Edge: term added that matches nothing → show empty message.

Let me now write the final file, aiming ~450 lines.

One more: "start with: proportionality, ..." — default concepts list as given. Good.

Title: "General Comments Research Wiki". Description: source line.

Write code:

```js
(function(){
"use strict";
const DATA = window.WORKSHOP_DATA || {};
const LIB = DATA.un_library || {};
const docs = Array.isArray(LIB.records) ? LIB.records : [];
const paras = [];
docs.forEach(function(d){ (Array.isArray(d.paragraphs)?d.paragraphs:[]).forEach(function(p){ paras.push({doc:d, para:p}); }); });
const years = docs.map(d=>d.year).filter(y=>typeof y==='number');
const yMin = years.length?Math.min.apply(null,years):null;
const yMax = years.length?Math.max.apply(null,years):null;

const DEFAULT_CONCEPTS = [...];
let concepts = DEFAULT_CONCEPTS.slice();
try{ ... }catch(e){}

const norm = s => String(s==null?'':s).toLowerCase().replace(/[^a-z0-9]+/g,' ').trim();
const uses = (text, term) => { const t=norm(term); return t && norm(text).indexOf(t)!==-1; };
const matchesFor = term => paras.filter(m => uses(m.para.text, term));
const countCache = {};
function countFor(term){ const k=norm(term); if(!(k in countCache)) countCache[k]=matchesFor(term).length; return countCache[k]; }
```

el helper, esc not needed with textContent.

renderNav(active):

```js
function renderNav(active){
  const nav = document.getElementById('conceptNav');
  nav.innerHTML='';
  const home = el('a','nav-link'+(active?'':' active'),'🏠 Home'); home.href='#/';
  nav.appendChild(home);
  const h = el('div','nav-head','Concepts'); nav.appendChild(h);
  concepts.forEach(c=>{
    const a = el('a','nav-link'+(norm(c)===norm(active)?' active':''), c + ' ');
    const b = el('span','count', String(countFor(c)));
    a.appendChild(b);
    a.href = '#/c/'+encodeURIComponent(c);
    nav.appendChild(a);
  });
}
```

Home link active when no active. Fine.

renderHome:

```js
function renderHome(){
  renderNav('');
  const main = document.getElementById('main'); main.innerHTML='';
  main.appendChild(el('h1',null,'General Comments research wiki'));
  const p = el('p','lede', `A small wiki over the ${docs.length} General Comments in the UN library (${LIB.source||'WORKSHOP_DATA.un_library'}): ${paras.length} numbered paragraphs, ${yMin!=null?yMin+'–'+yMax:'years unknown'}. Pick a concept in the sidebar, or add your own term.`);
  main.appendChild(p);
  const how = el('p','how','How this is computed: every number on this page is a deterministic count over the paragraphs loaded in WORKSHOP_DATA.un_library — no estimates, no sampling.');
  main.appendChild(how);
  const h = el('h2',null,'Documents in the library'); main.appendChild(h);
  docs.forEach(d=>{
    const card = el('div','doc-card');
    const head = el('div','doc-head');
    const a = el('a','sym', d.symbol||'(no symbol)'); a.href=d.doc_url||'#'; a.target='_blank'; a.rel='noopener';
    head.appendChild(a);
    head.appendChild(el('span','doc-title', (d.short_title||d.title||'')));
    card.appendChild(head);
    card.appendChild(el('p','doc-meta', [d.committee, d.year, (d.paragraphs||[]).length+' paragraphs', (d.pages!=null? d.pages+' PDF pages':'')].filter(Boolean).join(' · ')));
    main.appendChild(card);
  });
  main.appendChild(el('h2',null,'Concepts'));
  main.appendChild(el('p',null,'Each concept page lists, grouped by document, every paragraph that uses the term, verbatim, with a link that opens the PDF at the right page. Start with: '+concepts.slice(0,DEFAULT_CONCEPTS.length).join(', ')+'.'));
}
```

renderConcept(term):

```js
function renderConcept(term){
  renderNav(term);
  const main = document.getElementById('main'); main.innerHTML='';
  const matches = matchesFor(term);
  main.appendChild(el('h1',null,'Concept: '+term));
  const docsHit = []; matches.forEach(m=>{ if(docsHit.indexOf(m.doc)===-1) docsHit.push(m.doc); });
  main.appendChild(el('p','lede', `${matches.length} paragraph${matches.length===1?'':'s'} in ${docsHit.length} of ${docs.length} documents use “${term}”.`));
  main.appendChild(el('p','how', `How this is computed: a case-insensitive text search for “${term}” (hyphens and other punctuation count as spaces) over all ${paras.length} paragraphs of the ${docs.length} General Comments in WORKSHOP_DATA.un_library. The count is exact, not estimated. Paragraph texts are verbatim — expand each card to read them.`));
  if(!matches.length){ main.appendChild(el('p','empty',`No paragraph in the library uses the term “${term}”. Try another wording (for example “non-state actors” without the capital, or “accommodation”).`)); return; }
  // group by doc
  docs.forEach(d=>{
    const ms = matches.filter(m=>m.doc===d);
    if(!ms.length) return;
    const sec = el('section','doc-sec');
    const h2 = el('h2',null,'');
    const a = el('a','sym', d.symbol||'(no symbol)'); a.href=d.doc_url||'#'; a.target='_blank'; a.rel='noopener';
    h2.appendChild(a);
    h2.appendChild(document.createTextNode(' — '+(d.short_title||d.title||'')));
    sec.appendChild(h2);
    sec.appendChild(el('p','doc-meta', [d.committee, d.year, ms.length+' matching paragraph'+(ms.length===1?'':'s')].filter(Boolean).join(' · ')));
    ms.forEach(m=> sec.appendChild(paraCard(m)));
    main.appendChild(sec);
  });
  // related concepts
  const related = concepts.filter(c=>norm(c)!==norm(term) && matches.some(m=>uses(m.para.text,c)));
  if(related.length){
    const box = el('div','rel-box');
    box.appendChild(el('strong',null,'Related concepts (found in the same paragraphs): '));
    related.forEach((c,i)=>{ if(i) box.appendChild(document.createTextNode(' · '));
      const a=el('a',null,c); a.href='#/c/'+encodeURIComponent(c); box.appendChild(a); });
    main.appendChild(box);
  }
  // summary
  main.appendChild(summarySection(term, matches));
}
```

paraCard(m):

```js
function paraCard(m){
  const p = m.para, d = m.doc;
  const card = el('div','para');
  const head = el('div','para-head');
  const sym = el('a','sym', d.symbol||'(no symbol)'); sym.href=d.doc_url||'#'; sym.target='_blank'; sym.rel='noopener';
  head.appendChild(sym);
  const pg = el('a','pg','¶ '+(p.paragraph!=null?p.paragraph:'?')+' · p. '+(p.page!=null?p.page:'?'));
  pg.href='#'; pg.setAttribute('data-open','1'); pg.setAttribute('data-symbol', d.symbol||''); pg.setAttribute('data-page', String(p.page||''));
  pg.title='Open the PDF at this page';
  head.appendChild(pg);
  card.appendChild(head);
  const det = el('details',null);
  det.appendChild(el('summary',null,'Verbatim text of ¶ '+(p.paragraph!=null?p.paragraph:'?')));
  const t = el('p','para-text', p.text||'(no text)');
  det.appendChild(t);
  card.appendChild(det);
  if(Array.isArray(p.cited_articles)&&p.cited_articles.length){
    const chips = el('div','chips');
    p.cited_articles.forEach(c=> chips.appendChild(el('span','chip',c)));
    card.appendChild(chips);
  }
  return card;
}
```

summarySection(term, matches):

```js
function summarySection(term, matches){
  const sec = el('section','summary-sec');
  sec.appendChild(el('h2',null,'Draft a summary (AI)'));
  sec.appendChild(el('p','how','The button below sends at most 12 of this page’s paragraphs — verbatim, with their symbols and paragraph numbers — to a language model via studio.ask, and asks for three sentences, each ending with the paragraph it rests on. The model’s answer is marked as AI-written. Nothing is sent until you click.'));
  const row = el('div','sum-row');
  const btn = el('button','btn','Draft a summary');
  const cancelBtn = el('button','btn ghost','Stop');
  cancelBtn.style.display='none';
  const status = el('p','status','');
  row.appendChild(btn); row.appendChild(cancelBtn);
  sec.appendChild(row); sec.appendChild(status);
  const out = el('div','ai-out'); sec.appendChild(out);
  let cancelled=false;
  btn.addEventListener('click', async ()=>{
    const selected = matches.slice(0,12);
    const n = selected.length;
    btn.disabled=true; cancelBtn.style.display=''; cancelled=false;
    out.innerHTML='';
    status.textContent = `Sending ${n} paragraph${n===1?'':'s'} to the model — they have left your browser. Waiting for the answer…`;
    cancelBtn.onclick = ()=>{ cancelled=true; status.textContent='Stopping… the answer will be discarded.'; };
    const lines = selected.map((m,i)=>`[${i+1}] ${m.doc.symbol}, para. ${m.para.paragraph} (p. ${m.para.page}): ${m.para.text}`);
    const prompt = `Below are ${n} verbatim paragraphs from UN human rights treaty-body General Comments. All of them use the concept “${term}”.\n\n${lines.join('\n\n')}\n\nTask: write exactly three sentences summarizing what these paragraphs say about “${term}”. Each sentence must end with a citation in parentheses naming the paragraph it rests on, in the form (SYMBOL, para. N) — for example (CCPR/C/GC/37, para. 40). Use only what the paragraphs say; do not invent facts, quotes or paragraph numbers. Reply with JSON only, no other text: {"sentences": ["...", "...", "..."]}`;
    let answer='';
    try{ answer = await studio.ask(prompt, {json:true}); }
    catch(err){ answer=''; status.textContent='The model call failed: '+err; }
    btn.disabled=false; cancelBtn.style.display='none';
    if(cancelled){ status.textContent='Stopped — no summary was added.'; return; }
    if(!answer){ if(!status.textContent) status.textContent='No answer from the model.'; return; }
    let sentences=null;
    try{ const j=JSON.parse(answer); if(j&&Array.isArray(j.sentences)) sentences=j.sentences.map(s=>String(s)); }catch(e){ sentences=null; }
    out.innerHTML='';
    const note = el('p','ai-note', `AI-written summary — ${n} paragraph${n===1?'':'s'} were sent to the model and left your browser. Sentences below come from the model, not from the documents.`);
    out.appendChild(note);
    const box = el('div','ai-box'); box.setAttribute('data-source','ai');
    if(sentences && sentences.length){
      const ol = el('ol','ai-list');
      sentences.slice(0,3).forEach(s=>{ const li=el('li',null,s); li.setAttribute('data-source','ai'); ol.appendChild(li); });
      box.appendChild(ol);
    } else {
      const p = el('p','ai-raw', answer); p.setAttribute('data-source','ai'); box.appendChild(p);
    }
    out.appendChild(box);
    status.textContent = `Done — ${n} paragraph${n===1?'':'s'} sent to the model.`;
  });
  return sec;
}
```

Note: if matches.length > 12, mention "first 12". The note says at most 12 sent; if matches>12, say "the first 12 of X". Adjust: `const sent = Math.min(12, matches.length)` and note text uses n and total matches.length.

Click delegation for data-open:

```js
document.addEventListener('click', function(e){
  const a = e.target.closest ? e.target.closest('a[data-open]') : null;
  if(!a) return;
  e.preventDefault();
  const sym=a.getAttribute('data-symbol'), pg=parseInt(a.getAttribute('data-page'),10);
  try{ if(window.studio && typeof studio.openSource==='function'){ studio.openSource(sym, pg); } }catch(err){}
});
```

Add form wiring, route, init.

Also guard: if studio undefined at click time for ask — wrap in try (done).

CSS write out. Also `.nav-head`, `.count`, `.chip`, `.rel-box`, `.summary-sec`, `.ai-box`, `.ai-note`, `.btn.ghost`, `.status`, `.empty`, `.lede`, `.how`, `.doc-card`, `.doc-head`, `.doc-title`, `.doc-meta`, `.doc-sec h2`, `.sym`, `.pg`.

Responsive: on narrow screens sidebar stacks? "Works on a laptop screen without horizontal scrolling" — flex with fixed sidebar fine. Add media query to stack under 800px.

Now assemble final answer: 1–3 short sentences before code, then the html block, nothing after.

Let me write the complete file now, mindful of length.

Also home link in nav: use text "Home" without emoji maybe; fine with "⌂ Home"? Keep "Home".

Double-check requirement: "A concept page shows, grouped by document, every paragraph that uses the term, verbatim, with the symbol, the paragraph number and a link '¶ 12 · p. 5'". Our card shows symbol link, ¶ link with page, and verbatim text in details. Good.

"Under it, list the related concepts: the other concepts found in the same paragraphs, as links." Done.

"Add a button 'Draft a summary' that sends the page's paragraphs (at most 12)..." Done.

"Mark the summary as written by AI, and say how many paragraphs were sent." Done.

Sidebar lists concept pages; add concept by typing a term. Done.

Write it.