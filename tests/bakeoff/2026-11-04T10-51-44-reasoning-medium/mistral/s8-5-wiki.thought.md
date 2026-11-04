This is a huge task. The user wants a complete HTML app implementing a research wiki workspace with 5 tabs. I need to build one complete HTML file, under ~1500 lines, offline, using window.WORKSHOP_DATA.wiki and .library, Chart.js available but maybe not needed much.

Let me plan the architecture carefully but keep it manageable. This is a very large spec. I need to write a single HTML file with inline CSS/JS. Let me design:

Data structures:
- P = WORKSHOP_DATA.wiki.pages
- D = WORKSHOP_DATA.library.records
- maps: bySlug, byId
- per page: bodyLinks, pins (regex), backlinks
- norm(s) normalization
- verify(pin) function
- register of document: find source page whose sources == [id], else stub page, else "?"
- citeAs per document

Session state: changes count, calls count, passagesSent count.

Tabs: 01 PAGES, 02 ASK, 03 INGEST, 04 CHECK, 05 RECORD. role=tablist, arrow keys, hash routing for page slugs on tab 01.

Tab 01: left rail 320px with filter input + "n of 40 pages" big number + list grouped by type. Main column: index rendered by default, or a page. Page rendering: title, badges, tags, body rendered markdown (headings, bold, italic, lists, paragraphs, [[links]], pins as chips with quote inline, contested cards). Below: Links out, Linked from, Sources, Copy page as markdown button.

Pin rendering: quote in quotation marks inline, then chip button with label → studio.openSource(id, page, quote); register letter; verification status words; if differs from page mark, note. Expandable arrow showing passage paragraph/page_label + first 300 chars + "Open the PDF page".

Contested cards: claim heading, verdict large serif, note, lean bar (FIG.01) with formula label, positions table with caption.

Tab 02 ASK: textarea + button. Grey box stating what will be sent. Step 1: index + question → {pages:[slugs]}. Show chips with "Change pages" to tick others. Step 2: bodies + question → {title, answer, cannot_answer}. Render answer in data-source="ai", pins verified, struck-through if not on sent pages. Count verified pins by register. "File as a question page" button opens filing card with File this page / Copy answer. File disabled until all pins verify.

Tab 03 INGEST: buttons for inbox documents. Stepper 4 steps. Step 1 scope with batches table + Start. Step 2 takeaways table growing, failed box. Step 3 drafts: source page call, then touched pages calls. Step 4 review cards with Approve/Reject, then File the approved changes.

Tab 04 CHECK: big number verified pins, lint table with Lint now button, checks panel.

Tab 05 RECORD: log newest first with switch, tensions register, method note, Download the wiki (JSON blob), download changed pages markdown.

Footer: source, built, note.

This is enormous. I must keep under 1500 lines. I'll write compact but complete code. Let me be pragmatic: implement all tabs functionally but with reasonably compact code. Some deep features (full ingest pipeline with model calls) need to be implemented since user asked. I'll implement them as specified but concisely.

Let me think about the markdown renderer. Need to handle: headings # ## ###, bold **, italic *, bullets -, numbered lists, [[slug]] links, pins, plain links [text](url), fenced ```contested blocks, paragraphs. I'll write a renderer that processes the body line by line, detecting fenced blocks first.

Pin regex: `/\[([^\]]+)\]\(pin:([^#\s)]+)#p(\d+)(?: "([^"]*)")?\) ?(✓|⚠)/g`

For rendering pins inline within text: I'll do a tokenizing approach — split text by pin regex, render text segments with inline formatting (bold, italic, links, [[slugs]]), and pins as quote + chip.

Inline formatting: apply to text segments: escape HTML first, then replace [[slug]] → link, [text](url) → link, **bold**, *italic*. Careful ordering: do links first (they contain brackets), then bold, then italic. Actually pins already extracted. For [[slug]] inside link text? Unlikely. Keep simple.

Contested block parsing: lines claim:, verdict:, note:, then position lines starting with +, -, ~. Split on " | " into sign, register, pin, gloss, page-link. The pin part is like `[A/81/351, para. 16](pin:A/81/351#p6 "...") ✓` — parse with pin regex.

Lean: weights a5 b4 c3 d2 e1 f0.5; lean = (sum(+) + 0.5*sum(~)) / sum(all).

Verification: norm function per spec. verify(pin): find passages of doc with x.page === page; quote split on /…|\.\.\./ into fragments; each fragment found in norm(x.text) in order, searching from end of previous; label check: if x.paragraph set, label contains "para. " + x.paragraph; else "p. " + x.page_label. Pin with no quote, unknown id, or inbox doc → not verified with reason.

Wait — spec says "A pin with no quote, an unknown id, or a document whose status is 'inbox' is not verified". But A/HRC/57/61 is inbox and has 0 pins, fine. But stub page a-hrc-57-61 has 11 pins all to other documents. OK.

Hmm, but wait: if document status is inbox, pins to it are not verified. A/HRC/57/61 has 0 pins so fine.

Register of document: source page whose sources is exactly [id]; else stub page with that sources; else "?". Source pages have type "source". Stub: a-hrc-57-61 is entity type with status "stub" and sources [A/HRC/57/61] presumably.

Cite-as: most frequent text before ", para." or ", p." in existing pins' labels to that doc; else symbol or author+year.

Now the model calls: `await studio.ask(prompt, {json:true})`. Wrap in callModel(prompt, {passages}) that updates counters, shows size, parses JSON (strip fenced block), on failure returns raw with retry.

Session counters in header: changes, calls, passages sent.

Hash routing: location.hash = slug → open tab 01 with that page. Listen to hashchange.

Tabs with arrow-key navigation: keydown on tablist, ArrowLeft/Right moves focus and activates.

Let me now think about line budget. 1500 lines max. I'll aim for ~1200-1400 lines. Write compact JS (short helper names but readable enough). CSS ~150 lines. HTML skeleton ~80 lines. JS ~900-1000 lines. Tight but doable. I need to be efficient — maybe simplify some sub-features while keeping the core: all five tabs functional, pins verified, contested cards, ask flow, ingest flow (4 steps with model calls), lint, record/download.

Let me draft the code.

Structure:

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Research wiki: neurotechnology in the administration of justice</title>
<style>...</style>
</head>
<body>
<header>...</header>
<nav role="tablist" id="tabs">5 buttons</nav>
<main>
 <section id="tab-pages">...</section>
 <section id="tab-ask">...</section>
 <section id="tab-ingest">...</section>
 <section id="tab-check">...</section>
 <section id="tab-record">...</section>
</main>
<footer>...</footer>
<script>...</script>
</body>
</html>
```

CSS: paper #f4f0e8, ink #1d1b18, rules #d9d2c3, accent #9b2335. Fonts: Georgia serif for title/numbers, ui-monospace for labels, system sans 16px body. [hidden]{display:none!important}. Focus ring red. Chips, cards, tables, tabs styling. Pale yellow inserted #fdf3d0-ish with left border. Green #1a7f37, amber #9a6700, red #9b2335 for states.

JS plan:

```js
const W = window.WORKSHOP_DATA.wiki, L = window.WORKSHOP_DATA.library;
const P = W.pages, D = L.records;
const bySlug = {}, byId = {};
P.forEach(p=>bySlug[p.slug]=p); D.forEach(d=>byId[d.id]=d);
const PIN_RE = /\[([^\]]+)\]\(pin:([^#\s)]+)#p(\d+)(?: "([^"]*)")?\) ?(✓|⚠)/g;
const LINK_RE = /\[\[([^\]|#]+)/g;
function norm(s){...}
function esc(s){...}
// per-page parse
P.forEach(p=>{
  p._links = [...p.body.matchAll(/\[\[([^\]|#]+)/g)].map(m=>m[1]);
  p._pins = [...p.body.matchAll(PIN_RE)].map(m=>({label:m[1],id:m[2],page:+m[3],quote:m[4]||null,mark:m[5],raw:m[0]}));
});
const backlinks = {}; P.forEach(p=>p._links.forEach(s=>{(backlinks[s]=backlinks[s]||[]).push(p.slug)}));
```

verify(pin): returns {ok, reason, passage}.

```js
function verify(pin){
  const d = byId[pin.id];
  if(!d) return {ok:false, reason:"unknown document"};
  if(!pin.quote) return {ok:false, reason:"no quote in the pin"};
  if(d.status==="inbox") return {ok:false, reason:"document still in the inbox"};
  const frags = pin.quote.split(/…|\.\.\./).map(s=>norm(s)).filter(s=>s.length);
  const cands = d.passages.filter(x=>x.page===pin.page);
  for(const x of cands){
    const t = norm(x.text); let pos=0, ok=true;
    for(const f of frags){ const i=t.indexOf(f,pos); if(i<0){ok=false;break;} pos=i+f.length; }
    if(!ok) continue;
    const want = x.paragraph ? "para. "+x.paragraph : "p. "+x.page_label;
    if(!pin.label.includes(want)) continue;
    return {ok:true, passage:x};
  }
  return {ok:false, reason:"quote not found on that PDF page"};
}
```

Wait: label check — spec: "the label contains 'para. ' + x.paragraph when x.paragraph is set, otherwise 'p. ' + x.page_label". So label must contain that. OK as above.

Register of doc:

```js
function docRegister(id){
  const src = P.find(p=>p.type==="source" && p.frontmatter.sources && p.frontmatter.sources.length===1 && p.frontmatter.sources[0]===id);
  if(src) return src.frontmatter.register;
  const stub = P.find(p=>p.frontmatter.status==="stub" && p.frontmatter.sources && p.frontmatter.sources[0]===id);
  if(stub) return stub.frontmatter.register;
  return ["?"];
}
```

Hmm register is a list. Return list.

citeAs:

```js
function citeAs(id){
  const d=byId[id]; if(!d) return id;
  const counts={};
  P.forEach(p=>p._pins.forEach(pin=>{ if(pin.id===id){ const m=pin.label.match(/^(.*?), (?:para\.|p\.)/); if(m){counts[m[1]]=(counts[m[1]]||0)+1;} }}));
  let best=null,bc=0; for(const k in counts) if(counts[k]>bc){bc=counts[k];best=k;}
  if(best) return best;
  return d.symbol || (d.author+" "+d.year);
}
```

newPin(docId, passage, quote): build pin string with curly quotes for straight quotes:

```js
function makePin(id, x, quote){
  const q = quote.replace(/"/g, m => ...); // straight " → “ ” alternating? spec: "straight double quotes inside the quote become “ ” first". Simple: replace " with “ ... but closing? Just replace all with ” ? Hmm. Simplest: replace /"/g with "”"? That would make opening quotes closing. The regex just needs no straight quotes. I'll alternate: first " → “, subsequent → ”. Actually simpler: replace each " with “ if even index else ”. Fine.
  const loc = x.paragraph ? "para. "+x.paragraph : "p. "+x.page_label;
  return `[${citeAs(id)}, ${loc}](pin:${id}#p${x.page} "${q}") ✓`;
}
```

Markdown renderer. I'll write renderBody(body, opts) returning HTML string. Process:

```js
function renderBody(body, opts={}){
  const lines = body.split("\n");
  let html="", inFence=false, fenceBuf=[], listType=null;
  ...
}
```

Handle fenced ```contested blocks: collect and render contested card. Other fences: render as pre.

Line handling:
- /^### / → h3, ## → h2, # → h1
- /^- / → li in ul
- /^\d+\. / → li in ol
- blank → close lists, paragraph break
- else paragraph: accumulate consecutive lines into one <p> with inline().

inline(text): escape, then pins (replace pin matches with pinChip HTML), then [[slug]] links, then [text](url) links, then **bold**, *italic*. Order: pins first (they contain [..](..) which would be mangled by link regex). So: split by PIN_RE and process segments: for text segments apply esc + links + bold/italic; for pin matches insert chip.

Actually careful: escaping then regex on escaped text — quotes become &quot;? esc replaces & < > and maybe ". If I escape " to &quot; then pin regex won't match (pins contain "). So extract pins BEFORE escaping: split raw text by pin regex using a manual loop with lastIndex.

```js
function inlineSeg(s){ // s has no pins
  let h = esc(s);
  h = h.replace(/\[\[([^\]|#]+)\]\]/g, (m,slug)=> linkHtml(slug));
  h = h.replace(/\[([^\]]+)\]\((https?:\/\/[^\s)]+)\)/g, (m,t,u)=>`<a href="${u}" target="_blank" rel="noopener">${t}</a>`);
  h = h.replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>");
  h = h.replace(/\*([^*]+)\*/g, "<em>$1</em>");
  return h;
}
function inlineWithPins(s, ctx){
  let out="", last=0; PIN_RE.lastIndex=0; let m;
  while((m=PIN_RE.exec(s))){
    out += inlineSeg(s.slice(last, m.index));
    out += pinHtml({label:m[1],id:m[2],page:+m[3],quote:m[4]||null,mark:m[5]}, ctx);
    last = m.index + m[0].length;
  }
  out += inlineSeg(s.slice(last));
  return out;
}
```

Note PIN_RE has /g and is shared — reset lastIndex each use. Careful with concurrent use; fine since synchronous.

linkHtml(slug): if bySlug[slug] → `<a href="#${slug}" data-slug="${slug}">${esc(slug title? or slug)}</a>`. Spec: "[[slug]] as a link to that page (a dangling one in red, 'no page')". Show the slug text? Probably show the slug or the linked page's title. I'll show the slug in monospace; dangling: red with title "no page". Clicking sets location.hash = slug and switches to tab 01.

pinHtml(pin, ctx): 
```js
function pinHtml(pin, ctx){
  const v = verify(pin);
  const d = byId[pin.id];
  const reg = d ? docRegister(pin.id) : ["?"];
  const regStr = reg.join("");
  let status;
  if(v.ok) status = `<span class="ok">✓ verified</span>`;
  else status = `<span class="warn">⚠ not found — ${esc(v.reason)}</span>`;
  let diff = "";
  if(v.ok && pin.mark!=="✓") diff = ` · page says ${pin.mark}`;
  if(!v.ok && pin.mark==="✓") diff = ` · page says ✓`;
  const quote = pin.quote ? `<span class="pinquote">“${esc(pin.quote)}”</span>` : `<span class="warn">(no quote)</span>`;
  // expandable details
  const det = v.ok ? passagePreview(v.passage) : "";
  return `${quote} <span class="chip"><button class="chipbtn" data-pin ...>${esc(pin.label)}</button> <span class="reg">${regStr}</span> ${status}${diff} <button class="expand" aria-expanded="false">▸</button></span><span class="pindetail" hidden>${det}</span>`;
}
```

Chip button click → studio.openSource(pin.id, pin.page, pin.quote). Expand toggles detail: passage paragraph/page_label, first 300 chars of text, "Open the PDF page" button.

Contested card render:

```js
function contestedHtml(block){
  parse lines: claim:, verdict:, note:, positions.
  positions: lines starting with +,-,~ ; split " | " → [sign, register, pinStr, gloss, pageLink]
  pinStr parse with PIN_RE (single match).
  lean compute.
  verdict words: map "leans-contest"→"leans contest", etc.
  HTML: card with h3 claim, big serif verdict, note, FIG.01 lean bar (div bar with width %), formula label, table with caption, rows: sign in words (supports/contests/mixed), register letter, pin chip (small), gloss, page link.
  tensions link: find tensions entry with card: [[page]] — check W.tensions contains "card: [[slug]]"? The card is on page slug; tensions entry names this page in `card:`. So search W.tensions for `card: [[${pageSlug}]]`. But contestedHtml doesn't know page slug — pass ctx.pageSlug.
}
```

Lean bar: use a div with inner width %, accent red. Label: "FIG.01 · descriptive: support n% of weighted positions · weights a 5 · b 4 · c 3 · d 2 · e 1 · f ½ — the verdict is the answer".

Tab 01 layout:

```html
<section id="tab-pages">
 <div class="cols">
  <aside class="rail">
    <label for="pagefilter">title, tag or slug</label>
    <input id="pagefilter" type="search">
    <div class="bignum" id="pagecount">40 of 40 pages</div>
    <div id="pagelist"></div>
  </aside>
  <div class="main" id="pageview"></div>
 </div>
</section>
```

Page list grouped by type: order source, concept, entity, question. Group labels monospace uppercase. Each item: button with title, register letters, pin count, "stub" tag if status stub. Click → showPage(slug), location.hash=slug.

Filter: matches title, slug, tags (frontmatter.tags). Big number "n of 40 pages".

Default main: render index (W.index) as a page-like view: title "Index", body = W.index rendered.

showPage(slug): build HTML: h1 title; badges: type, register letters with names, status, updated; tags chips; body rendered; then Links out / Linked from / Sources sections; Copy page as markdown button.

Register names: a treaty law, b General Comments, c UN, agency and soft-law reports, d national human rights institution, e civil society, f scholarship.

Copy page as markdown: frontmatter YAML + body. Use navigator.clipboard? Offline sandbox — clipboard may fail; fallback: select textarea. I'll do: create temp textarea, copy, show "copied" message; fallback show the markdown in a details block. Simpler: put markdown into a <textarea readonly> in a details. Actually simplest robust: use a temporary textarea + document.execCommand('copy') fallback, and always also show in a collapsible <details> with the text. I'll do details with textarea.

Tab 02 ASK:

```html
<section id="tab-ask" hidden>
 <p class="hint">What leaves the browser: ...</p>
 <label for="q">Ask the wiki</label>
 <textarea id="q"></textarea>
 <button id="askbtn">Ask the wiki</button>
 <div id="askprogress" aria-live="polite"></div>
 <div id="askresult"></div>
</section>
```

Flow:
- grey box: "Step 1 will send: the index (n chars) and your question. Step 2 will send: the bodies of the chosen pages (n chars) and your question. No library passages leave the browser."
- On Ask: call1: prompt = index + question, ask JSON {pages:[...]}. Show chips of chosen slugs + "Change pages" link → shows checkboxes of all pages to tick (up to 5). Then call2 automatically? Spec: step 2 sends those pages' bodies. I'll run call1, show chips with Change pages, then a "Continue" happens automatically after user confirms? Simpler: after call1, show chips + Change pages link; then automatically proceed to call2 (with the chosen set). But user may want to change pages before call2. I'll add: after call1, show chips and a small form with checkboxes (pre-ticked) and button "Send these pages" — but clickable budget: 5 tabs + Ask + File = 7; the change-pages is a link that reveals checkboxes, then "Send" button appears... that adds clicks. Spec says clickables: 5 tabs, Ask the wiki, File as a question page = 7 (8 once filing card open). The Change pages link is inside the answer area... Hmm "not counting table rows or links inside a page's text". The Change pages link is arguably part of the flow. I'll keep it: after call1, show chips + "Change pages" link; clicking toggles a checkbox list with a "Use these pages" button; default flow: after call1 completes, automatically run call2 with the model's pages. If user clicks Change pages before... race. Simpler: run call1, display chips + Change pages; then a button "Ask with these pages" appears? That's an extra click. Alternatively: call1 → show chips + change link + automatically proceed after render (setTimeout 0? no—user can't intervene). 

Let me re-read: "Step 1 sends the index and the question; the model returns up to five slugs, shown as chips with a Change pages link that lets you tick others. Step 2 sends those pages' bodies..." So step 2 presumably runs after, with the (possibly changed) pages. I'll implement: after call1, render chips + "Change pages" link; when clicked, show checkbox list of all pages (chosen ticked) and a "Send these pages" button; ALSO auto-proceed: I'll just have step 2 run when the user presses "Ask the wiki" again? No — button reads "Ask again" once there's an answer.

Pragmatic: after call1, show chips and Change pages; then automatically start call2 with current selection after a short delay? No animations/delays that hold results... I'll make it explicit but minimal: after call1, the chips row includes the Change pages link, and directly below a button "Send these pages to step 2" — hmm that's 8 clickables. The spec's count of 7 doesn't count the change-pages controls strictly ("links inside a page's text" excluded; these aren't page text). I'll not over-worry; keep ≤ ~8. Implementation: call1 → render chips + change link + auto-run call2 immediately with model's slugs; if user clicked change pages... they can't before call2 starts. Alternative: don't auto-run; show "Continue to step 2" button. I'll do: after call1, render chips + Change pages link + button "Send to step 2". When Change pages clicked, checkboxes appear with "Send to step 2" still working with ticked set. That's clean and user-controlled. Clickables: 5 tabs + Ask + Continue + File = 8. Slightly over but acceptable ("about seven"). Actually I can merge: the "Change pages" link toggles checkboxes, and the main button becomes "Send these pages" after call1. So: Ask the wiki → (call1) → button now reads "Send n pages" → click → call2 → answer shown, button reads "Ask again". Change pages link beside chips. That's 5 tabs + Ask/Send + Change pages + File = 8. Fine, "about seven".

- call2: prompt includes bodies of chosen pages + question + instructions (pin syntax, register naming, ≤350 words, JSON {title, answer, cannot_answer}). Parse. Render answer inside data-source="ai": renderBody-like with pins verified; pins not on sent pages or failing verify → struck through with "not on the pages sent". cannot_answer section. Count line: verified pins by register: "verified pins by register: a 0 · b 2 · c 5 ...".
- "File as a question page" button → opens filing card (fieldset) previewing built page: slug kebab from title unique, type question, tags input, register from pinned docs, status draft, updated today, links from [[slugs]] in answer, sources from pins; body template. "File this page" disabled until every pin in answer verifies (and answer has ≥1 pin? spec: "Disabled, with the reason, until every pin in the answer verifies" — if zero pins, all verify trivially; but reason should say if no pins... I'll disable when any pin fails; if zero pins, disable with reason "the answer has no pins to verify"). File: add page to P, bySlug, index line under Questions, log entry "## [date] ask | title". Update counters, header "changes". Show "Filed" message aria-live.

Progress line + Stop button per step: implement a runStep helper with a stop flag; Escape stops. studio.ask is a single await per call though — Stop can only prevent subsequent calls. For ask there's one call per step, so Stop matters for ingest batches. I'll implement stop flag checked between calls; Escape sets it.

Tab 03 INGEST:

Inbox docs: D.filter(d=>d.status==="inbox"). For each, button "Ingest {symbol or short_title}". If none: "Nothing waits in the inbox".

On click: show stepper UI: 4 steps with running line "calls so far m · passages sent k". Step 1 panel: "Scope: the whole document." text: "All N passages will be sent, in batches of 25 (n calls), c characters; nothing is held back." Table of batches: batch #, paragraph range, PDF pages. Start button.

Start: for each batch: callModel with takeaway prompt (batch passages as {id,page,paragraph,text}, index, instructions). Progress "batch 2 of 4 · 50 of 100 passages have left the browser". Stop button. After each batch: parse takeaways, verify each: find passage by id (takeaway.passage is passage id like "A/HRC/57/61#12"? The prompt says passage field — model returns passage id; code finds passage by id among sent). Build pin via makePin, verify. Table grows: claim, quote, passage (paragraph + PDF page), pages chips, verification words. Failed → failed[] box "Could not verify: n" with quote, named passage, nearest passage (longest common consecutive word run) + Open PDF page button.

Step 2 panel appears after step 1 done (or interleaved). Then Step 3: "Draft the source page (1 call)" button → source page call with verified takeaways + pins + doc metadata + schema anatomy → JSON {one_liner, body, touches}. Re-verify pins in body. Build frontmatter. Change card (new page). Then "Draft the changes to n pages (n calls)" → per touched slug call → {edits:[{after, markdown}], contested} → insert markdown at end of named heading section; re-verify; update links/sources. Change cards (edited).

Step 4: review: each change card: fieldset, legend page title + type + new/edited, counts (paragraphs inserted, pins added verified/not in words), page shown with inserted paragraphs highlighted pale yellow, rest grey, pins as chips. Buttons "Approve this page" / "Reject this page", line "change 3 of 9". After last: "File the approved changes" button → writes: pages replaced/added, updated today, index updated, log entry, tensions entry if new contested, doc status "ingested", lint re-run, counters.

This is a LOT. I'll implement it in a streamlined way: changes stored as {slug, kind:'new'|'edit', page (new object), insertedParas: [strings], approved:null}. For edit: apply edits to a copy of body at draft time (so card shows final text with inserted paragraphs marked). Marking inserted paragraphs: when inserting markdown, wrap inserted block in a marker? I'll track inserted markdown strings and when rendering the card, highlight paragraphs whose text is in inserted set. Simpler: wrap inserted markdown in `<mark class="ins">`? But body is markdown; rendering pipeline could detect a sentinel. I'll insert with a sentinel comment `<!--ins-->` before inserted markdown, and renderer adds class to following block. Simpler: keep inserted list; when rendering card body, split into blocks and check if block (normalized) is in inserted set → wrap in div.ins. Good enough.

Given the enormity, I'll implement ingest with real model calls per spec but keep code tight.

Tab 04 CHECK:

Big number: "n of n pins verified by this page" (computed at load; recompute after changes). "n lint checks need a look". Lint table: caption "Lint checks", rows: each check name, count, "0 · pass" or "n · check", pages concerned as links. Button "Lint now" → "Re-run". Checks panel below (open by default): the "How the app checks itself" one-liners — I'll render a static-ish list computed live: pins found vs index stated, verified vs found, ✓-that-fail listed, dangling links, orphans, sources mismatch, no-pin pages, links not reciprocated, index coverage, index ✓N mismatch, contested vs tensions, stubs, inbox pins, session checks. Each with pass/check.

Lint checks list per spec:
1. dangling links
2. orphans
3. pins not verified by code
4. pins marked ✓ that fail
5. sources differ from pinned documents
6. pages with no pins
7. links not reciprocated (frontmatter.links vs body links? "links not reciprocated" — pages in frontmatter.links that don't link back? I'll check: for each page, links in frontmatter that don't appear in bodyLinks AND bodyLinks not in frontmatter — spec earlier said they differ on 5 entries; the check "links not reciprocated": frontmatter.links entries whose page doesn't have this slug in bodyLinks.)
8. pages missing from index / index lines without page
9. index ✓N differs from computed
10. contested cards without tensions entry and reverse
11. stub pages
12. pins to inbox document

Tab 05 RECORD:

Log rendered newest first with switch (checkbox "newest first"). Each entry `## [date] op | subject` collapsible (<details>). Tensions register: render W.tensions markdown; each `###` entry with `card: [[slug]]` link → opens page on tab 01. Entries added this session tagged "this session" (red). Method note + source line. Buttons: "Download the wiki" (JSON blob), and if changes>0 "Download changed pages (markdown)".

Download JSON: Blob of {pages, index, log, tensions, schema, count, changes, library_status} → a.download = `wiki-${date}.json`.

Header: left label "WIKI · neurotechnology and justice", title serif, one line: "40 pages (9 sources, 14 concepts, 14 entities, 3 questions) · 707 pins, 707 verified by this page · 10 documents, 1 in the inbox · built 2026-…". Right: "Changes this session: 0 · Calls to the model: 0 · Passages that left the browser: 0" + "This page has no storage: changes live in it until you download them (tab 05)".

Footer: W.source, W.built + "Counting, matching and verification are done by this page's code; the model is called only when you press Ask, Ingest or a retry button."

Credits line: sources consulted — Karpathy LLM Wiki gist (MIT? gist... it's a gist, license unclear — actually Karpathy gists are typically... not stated. The instructions say add credits only for open-licence reference shelf excerpts. The sources list includes GitHub links; UK Gov guidance is OGL, A11Y Project is CC BY... I'll add a small Credits line: "Method notes: Karpathy, 'LLM Wiki'; UK Government Analysis Function QA guidance (OGL 3.0); A11Y Project checklist (CC BY 4.0)." That's safe.

Now, sizes: this will be long. Let me write carefully and compactly. I'll aim for ~1300 lines. Let me start writing.

Key helper: el creation via innerHTML strings mostly.

Let me define CSS classes:
- body: background #f4f0e8; color #1d1b18; font 16px system sans.
- .mono: ui-monospace 11-12px uppercase letter-spacing.
- header layout flex.
- .tabs: buttons row, border-bottom rule; active tab red with underline.
- .bignum: Georgia 44px.
- .rail: width 320px, border-right rule.
- .chip: inline-flex border 1px #d9d2c3 radius 999px padding 1px 8px, monospace 11px.
- .chipbtn: button inside chip, accent on hover.
- .pinquote: serif italic? Quote in quotation marks — I'll style serif.
- .pindetail: block, small, border-left.
- .ok green #1a7f37, .warn amber #9a6700, .bad red #9b2335, .pass green.
- table: full width, caption monospace, th uppercase small, td border-top rule, numbers right.
- .card: border 1px rule, padding, margin.
- .contested: card with left border accent.
- .verdict: Georgia 34px.
- .leanbar: height 10px background rule; inner accent width %.
- .ins: background #fbf0c8? pale yellow #fdf6d8 with left border accent.
- .grey: color #6b675f for non-inserted in change cards.
- [hidden]{display:none!important}
- :focus-visible outline 3px solid #9b2335.
- .btn: monospace uppercase small, border 1px ink, background transparent; hover accent.
- .btn.primary: accent background? Keep accent border/text.
- details/summary styling.
- .ai box: border dashed? data-source="ai" elements get a subtle marker: I'll add `[data-source="ai"]` outline? Add a small "AI" tag via CSS ::before? Use `.ai-tag`. I'll wrap answer in div data-source="ai" and add a monospace label "model answer — check every pin".

Tab switching: buttons with role=tab, aria-selected, panels role=tabpanel. Arrow keys. location.hash handling: on load and hashchange, if hash matches a slug, activate tab 01 and show page.

Running step: when ingest running, tab 03 label gets "· running" and aria-live.

Session counters: S = {changes:0, calls:0, passages:0}; updateHeader().

callModel(prompt, passageObjs): 
```js
async function callModel(prompt, passages){
  S.calls++; S.passages += passages? passages.length:0; updateHeader();
  const chars = prompt.length; // show
  const raw = await studio.ask(prompt, {json:true});
  let txt = raw.trim();
  let json = null;
  try { json = JSON.parse(txt); } catch(e){
    const m = txt.match(/```(?:json)?\s*([\s\S]*?)```/);
    if(m){ try{ json = JSON.parse(m[1]); }catch(e2){} }
  }
  return {raw: txt, json, chars};
}
```
Show prompt size on screen: I'll include in progress line: "call m · n characters · k passages sent".

Now Ask implementation details:

```js
let askState = {step:0, slugs:[], sentPages:[], answer:null};
async function runAsk(){
  const q = qInput.value.trim(); if(!q) return;
  ...
  // step 1
  progress("Step 1 of 2 · sending the index (n chars) and your question…");
  const p1 = `You are the research wiki... INDEX:\n${W.index}\n\nQUESTION: ${q}\n\nReturn JSON only: {"pages": ["slug", ...]} — at most 5 slugs from the index.`;
  const r1 = await callModel(p1, []);
  if(!r1.json || !Array.isArray(r1.json.pages)) → show raw + Retry.
  slugs = r1.json.pages.filter(s=>bySlug[s]).slice(0,5); dropped listed.
  render chips + Change pages link + button "Send these pages".
}
async function runAsk2(){
  const bodies = slugs.map(s=>bySlug[s].body).join("\n\n---\n\n");
  progress(`Step 2 of 2 · sending ${slugs.length} pages, ${chars} characters; 0 library passages have left the browser…`);
  const p2 = `...pages... question... Return JSON {"title":..., "answer":..., "cannot_answer":...}. Answer at most 350 words. Use pins in this syntax: [label](pin:id#pPAGE "quote") ✓ — quote only words that stand in the pages given; the code will check. Name the register where it matters ((a) treaty law … (f) scholarship); keep each document's own verb; never present (c)–(f) as what the treaty requires.`;
  const r2 = await callModel(p2, []);
  parse; render answer in data-source="ai" with pin checking: pin accepted when same pin:id#pPAGE with same quote exists in a sent page's body AND verify true; else struck through "not on the pages sent".
}
```

For answer pin checking: collect all pins from sent pages' bodies into a set keyed by `${id}#p${page}|${quote}`. In answer rendering, pass ctx {answerCheck: set}. pinHtml with ctx.answerCheck: if pin not in set or !verify → class struck + note.

Count line: verified pins by register over answer's pins.

Filing: build page object:
```js
function buildQuestionPage(title, answer, cannot){
  slug = kebab(title); ensure unique (append -2...);
  tags from input;
  pins in answer → sources = unique ids; register = union of doc registers;
  links = bodyLinks of answer;
  body = `# ${title}\n\n**Short answer.** ...\n\n## Reasoning\n\n${answer}\n\n## What the library cannot answer\n\n${cannot}\n\n## Related\n\n...`;
}
```
Spec body: "# title", "**Short answer.**", "## Reasoning" (the answer), "## What the library cannot answer", "## Related". Short answer — maybe first sentence of answer or title-based; I'll use the answer's first paragraph as short answer? Spec lists "**Short answer.**" as a line — I'll put a one-line short answer = title? Hmm. I'll put the first sentence of the answer. Fine.

File: P.push(page); bySlug[slug]=page; recompute _links/_pins; index += line under Questions — index is markdown; I'll append `\n- [[slug]] — ${short} · (${reg}) · ✓${n}` at end (Questions section presumably last; I'll just append at end and note). Log: W.log += `\n## [${today}] ask | ${title}\n`. S.changes++; updateHeader; show "Filed" aria-live; re-lint counts.

Ingest implementation:

```js
let ing = null; // {doc, batches, takeaways:[], failed:[], changes:[], step, stop:false}
function startIngest(doc){ ... render stepper ... }
```

Step 1: batches = chunk(doc.passages, 25). Table: batch i, paragraph range (first.paragraph–last.paragraph or pages), PDF pages range. Start button → loop batches with stop flag; progress line; per batch call:

prompt: `You read a UN document into a research wiki. Passages (JSON): ${JSON.stringify(batch.map(x=>({id:x.id,page:x.page,paragraph:x.paragraph,text:x.text})))}. Index: ${W.index}. Return JSON {"takeaways":[{"claim","quote","passage","pages":[slugs]}]} — at most 10; quote 8–40 words copied verbatim from that one passage; pages = slugs from the index the claim bears on. Pin syntax: [label](pin:id#pPAGE "quote") ✓; quote only words that stand in the passages given; the code will check.`

For each takeaway: find passage by id in doc.passages (must be in sent set — track sentIds; if not sent, drop & count). Build pin = makePin(id, passage, quote). v = verify(pinObj). If ok → takeaways.push({claim, quote, passage, pages: filtered slugs, pin, verified:true}); else failed.push({claim, quote, passageNamed, nearest, pin}).

Nearest passage: passage on same page as named passage with longest run of consecutive normalized words shared with quote. Implement: words of norm(quote); for each passage on that page, compute longest common consecutive run length; pick max.

Step 2 table grows after each batch (render rows). Failed box with "Could not verify: n".

Step 3: after all batches: button "Draft the source page (1 call)": prompt with verified takeaways (claim + pin), citeAs, doc metadata, schema anatomy list, instructions. Parse {one_liner, body, touches}. Re-verify every pin in body (extract with PIN_RE, verify each; count verified/not). Build page object: frontmatter {title: doc.title, type:"source", tags: from touched slugs?, register: from stub, status:"draft", updated: today, links: bodyLinks of body, sources:[doc.id]}; body. Change card kind "new". touches kept to existing slugs + up to 2 new slugs (new slugs become "new page" cards? spec: "plus at most two new slugs per ingest, which become 'new page' cards" — hmm, new slugs in takeaways' pages become new page cards. I'll collect newSlugs from takeaways (not existing) up to 2; they get draft cards too? That complicates. Spec step 3: "Draft the changes to n pages (n calls)" runs one call per touched page. Touched = existing pages named in takeaways + stub. New slugs (≤2) become "new page" cards — I'll create simple new-page cards from takeaways naming them (a card with the takeaways as body). Keep simple: for each new slug, card kind "new" with body built from its takeaways.

Then "Draft the changes to n pages (n calls)": for each touched existing slug: prompt with page body + relevant takeaways with pins + instructions → {edits:[{after, markdown}], contested}. Apply: insert markdown at end of section of heading `after` (find heading line, find next heading of same-or-higher level, insert before it; if 'end' or not found → append at end with note). Track inserted markdown strings. Re-verify pins in new body. Update links (add slug both ways? "adds the link both ways in links and the document id to sources") — modify frontmatter.links to include source page slug and source page links include this slug; sources add doc.id. Change card kind "edit" with new page object (body replaced, frontmatter updated), inserted list.

Contested from touched call: if contested block returned, add to page body appended as fenced block, and record for tensions entry at filing.

Step 4: review cards sequentially? Spec: "Each change is one page: a card..." with "change 3 of 9" — show all cards in a list, each with Approve/Reject buttons; or one at a time. "change 3 of 9" suggests sequential. I'll show them one at a time: current card index, "change i of n", Approve/Reject; after decision move to next; after last, "File the approved changes" button. Simpler and matches "change 3 of 9".

Card rendering: fieldset, legend "title (type) — new page/edited", counts line: "n paragraphs inserted · n pins added (n verified, n not verified, in words)", body rendered with inserted paragraphs highlighted (class ins) and rest grey (class dim). Pins as chips. Buttons: `Approve change i of n` / `Reject change i of n`.

File: for each approved change: if new → P.push, bySlug, index line under Sources; if edit → replace page in P (bySlug[slug] = newPage; also update P array element). Set updated today. Doc status = "ingested". Log entry: `## [today] ingest | symbol: short_title` + details line. Tensions: for new contested cards append entry. S.changes += approved count. Re-run lint, show before/after. Update header. Mark tab running off.

That's the plan. Now tab 04 lint function:

```js
function runLint(){
  const checks = [];
  // pins found vs index stated
  const stated = (W.index.match(/(\d[\d,]*) pins/)||[])[1];
  const found = P.reduce((n,p)=>n+p._pins.length,0);
  checks.push({name:"Pins found vs index", a:stated, b:found, pass: +stated.replace(/,/g,"")===found, pages:[]});
  const verified = P.reduce((n,p)=>n+p._pins.filter(x=>verify(x).ok).length,0);
  ...
}
```

Each check: {label, detail, count, pass, pages:[slugs]}. Render table rows: name, count/status "0 · pass" or "n · check", pages links.

Checks list (12 as spec). Also checks panel with one-line descriptions and live values.

Big number: `${verified} of ${found} pins verified by this page`; `n lint checks need a look` = checks.filter(!pass).length.

Tab 05: log entries: split W.log on /^## /m → entries. Render newest first (default) with switch checkbox. Each entry in <details><summary>[date] op | subject</summary>body</details>. Session-added entries get red "this session" tag — track sessionLogStart = W.log.length at load; entries beyond that are session. Tensions: render markdown; make `card: [[slug]]` links clickable → I'll post-process rendered HTML replacing links with data-slug. Simpler: render tensions with renderBody then attach click handler on container for a[data-slug].

Download wiki JSON:
```js
function downloadWiki(){
  const out = {title:W.title, source:W.source, built:W.built, count:P.length, schema:W.schema, index:W.index, log:W.log, tensions:W.tensions, pages:P.map(p=>({slug:p.slug,type:p.type,title:p.title,frontmatter:p.frontmatter,body:p.body})), changes:sessionChanges, library_status: D.map(d=>({id:d.id,status:d.status}))};
  const blob = new Blob([JSON.stringify(out,null,2)],{type:"application/json"});
  const a=document.createElement("a"); a.href=URL.createObjectURL(blob); a.download=`wiki-${todayStr()}.json`; a.click(); URL.revokeObjectURL...
}
```

Changed pages markdown: sessionChanges entries {date, kind, slug} → file with `---\nslug...` separators: each page as `---\nfrontmatter yaml\n---\n\nbody`? Spec: "saves the changed pages as one markdown file with --- separators". I'll do per page: `# slug\n\n---\n` + yaml frontmatter + body, separated by `\n\n---\n\n`.

OK. Also "How this is computed" lines near charts/numbers: add small mono hints: under big numbers "computed by this page's code from WORKSHOP_DATA".

Now write the code. I must be disciplined about length. Let me write it.

Also keyboard: tabs arrow navigation; Escape stops running step (set stopFlag). Focus first tab on load.

Hash: on load, if location.hash.slice(1) in bySlug → show tab 01 page. hashchange listener.

Let me now write the whole file mentally and produce it. I'll write JS with reasonably short but clear code. Given the size, I'll be terse in comments.

Some details:

norm:
```js
function norm(s){
  return s.normalize("NFKC")
    .replace(/[“”„]/g,'"').replace(/[‘’]/g,"'")
    .replace(/[–—]/g,"-")
    .replace(/\u00ad/g,"")
    .replace(/-\s+/g,"")
    .replace(/\s+/g," ").trim();
}
```

esc:
```js
const esc = s => String(s).replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;").replace(/"/g,"&quot;");
```

Register names:
```js
const REGNAMES = {a:"treaty law", b:"General Comments", c:"UN, agency and soft-law reports", d:"national human rights institution", e:"civil society", f:"scholarship"};
```

docRegister returns array; display letters joined + title attr names.

Page list rendering:
```js
function renderPageList(){
  const f = filter.value.toLowerCase();
  const groups = [["source","SOURCES"],["concept","CONCEPTS"],["entity","ENTITIES"],["question","QUESTIONS"]];
  let n=0, html="";
  for(const [t,label] of groups){
    const items = P.filter(p=>p.type===t && match(p,f));
    if(!items.length) continue;
    n+=items.length;
    html += `<div class="grouplabel mono">${label}</div>`;
    for(const p of items){
      const pins = p._pins.length, ver = p._pins.filter(x=>verify(x).ok).length;
      html += `<button class="pagelink" data-slug="${p.slug}"><span class="ptitle">${esc(p.title)}</span> <span class="mono meta">${(p.frontmatter.register||[]).join("")} · ${pins} pins${p.frontmatter.status==="stub"?' · <span class="warn">stub</span>":""}</span></button>`;
    }
  }
  pagecount.textContent = `${n} of ${P.length} pages`;
  pagelist.innerHTML = html;
}
```

match(p,f): title, slug, tags joined includes f.

showPage(slug): builds main HTML. Include badges, tags, body, links out (frontmatter.links with "frontmatter only" if not in bodyLinks), linked from (backlinks), sources (frontmatter.sources → doc info), copy button.

Sources section: for each id in frontmatter.sources: doc = byId[id]; show short_title, kind, year, url link, "inbox" tag if status inbox.

Copy markdown: build string:
```
---
title: ...
type: ...
tags: [...]
register: [...]
status: ...
updated: ...
links: [...]
sources: [...]
---
body
```
Show in details>textarea.

Index default view: title "Index", body W.index rendered, plus note.

Now contested parsing:

```js
function parseContested(buf){ // array of lines inside fence
  const o={positions:[]};
  for(const line of buf){
    if(line.startsWith("claim:")) o.claim=line.slice(6).trim();
    else if(line.startsWith("verdict:")) o.verdict=line.slice(8).trim();
    else if(line.startsWith("note:")) o.note=line.slice(5).trim();
    else if(/^[+~-] /.test(line)){
      const parts=line.slice(2).split(" | ");
      o.positions.push({sign:line[0], register:parts[1]?.trim(), pinRaw:parts[2]?.trim(), gloss:parts[3]?.trim(), page:parts[4]?.trim()});
    }
  }
  return o;
}
```

Position pin: parse with PIN_RE on pinRaw (reset lastIndex). page like `[[slug]]` → extract slug.

Lean:
```js
const W8={a:5,b:4,c:3,d:2,e:1,f:0.5};
function lean(o){ let sup=0,tot=0; for(const p of o.positions){ const w=W8[p.register]||0; tot+=w; if(p.sign==="+")sup+=w; else if(p.sign==="~")sup+=w/2; } return tot? sup/tot:0; }
```

Verdict words: replace "-" with " ".

Contested HTML with table:
```html
<div class="contested card">
 <div class="mono fig">CONTESTED CLAIM</div>
 <h3>claim</h3>
 <div class="verdict">leans contest</div>
 <p>note</p>
 <div class="mono fig">FIG.01 · lean bar — descriptive: support 42% of weighted positions · weights a 5 · b 4 · c 3 · d 2 · e 1 · f ½ · the verdict is the answer</div>
 <div class="leanbar"><div style="width:42%"></div></div>
 <table><caption>positions</caption>...rows: sign words, register, pin chip, gloss, page link</table>
 link to tensions register if entry exists
</div>
```

Renderer main loop:

```js
function renderBody(body, ctx={}){
  const lines = body.split("\n");
  let out="", list=null, para=[];
  const flushPara=()=>{ if(para.length){ out+=`<p>${inlineWithPins(para.join(" "),ctx)}</p>`; para=[]; } };
  const closeList=()=>{ if(list){ out+=`</${list}>`; list=null; } };
  let i=0;
  while(i<lines.length){
    const ln=lines[i];
    if(ln.trim().startsWith("```")){
      flushPara(); closeList();
      const fence=ln.trim();
      const buf=[]; i++;
      while(i<lines.length && !lines[i].trim().startsWith("```")){ buf.push(lines[i]); i++; }
      i++; // skip closing
      if(fence.includes("contested")) out+=contestedHtml(parseContested(buf), ctx);
      else out+=`<pre class="mono">${esc(buf.join("\n"))}</pre>`;
      continue;
    }
    if(/^###\s/.test(ln)){ flushPara(); closeList(); out+=`<h3>${inlineWithPins(ln.replace(/^###\s/,""),ctx)}</h3>`; }
    else if(/^##\s/.test(ln)){ ... h2 }
    else if(/^#\s/.test(ln)){ ... h1 }
    else if(/^\s*-\s/.test(ln)){ flushPara(); if(list!=="ul"){closeList(); out+="<ul>"; list="ul";} out+=`<li>${inlineWithPins(ln.replace(/^\s*-\s/,""),ctx)}</li>`; }
    else if(/^\s*\d+\.\s/.test(ln)){ ... ol }
    else if(!ln.trim()){ flushPara(); closeList(); }
    else { closeList(); para.push(ln); }
    i++;
  }
  flushPara(); closeList();
  return out;
}
```

pinHtml with ctx options: ctx.answerSet (for ask), ctx.highlight (set of inserted normalized blocks) handled at block level instead.

For change cards, I'll render body via renderBody then post-process? Highlighting inserted paragraphs: easier to pre-mark: before rendering card body, wrap inserted markdown blocks with a marker line `<!--INS-->` and in renderer, when a paragraph/heading starts after an INS marker, add class. Simpler approach: render normally, then in the card, split output? Hmm. Alternative: render card body with a modified renderer where I check each block: I'll implement renderBody with ctx.insSet (array of normalized block strings); when emitting a block (p, li, h), compute its plain text? Complicated. 

Simplest: in the edit application, wrap inserted markdown in HTML comment sentinels: body2 = body with `<!--INS-->\n${markdown}\n<!--/INS-->` inserted. Renderer: when line is `<!--INS-->`, set flag ins=true; subsequent blocks get class "ins"; `<!--/INS-->` clears. And for the card, non-ins blocks get class "dim". I'll add ctx.cardMode to add dim to non-ins blocks. Implement: in renderer, track insFlag; when emitting block-level element, wrap: if ctx.cardMode: class = insFlag? "ins":"dim". Apply to p, li, h1-3. Good.

pinHtml:

```js
function pinHtml(pin, ctx={}){
  const v = verify(pin);
  const d = byId[pin.id];
  const reg = d ? docRegister(pin.id) : ["?"];
  const regTitle = reg.map(r=>`${r} ${REGNAMES[r]||"?"}`).join(", ");
  let st;
  if(v.ok) st=`<span class="ok">✓ verified</span>`;
  else st=`<span class="warn">⚠ not found — ${esc(v.reason)}</span>`;
  let diff="";
  if(pin.mark==="✓" && !v.ok) diff=` · <span class="warn">page says ✓</span>`;
  if(pin.mark==="⚠" && v.ok) diff=` · page says ⚠`;
  let answerNote="";
  if(ctx.answerSet){
    const key = pin.id+"#p"+pin.page+"|"+(pin.quote||"");
    if(!ctx.answerSet.has(key) || !v.ok) answerNote=` · <span class="bad">not on the pages sent</span>`;
  }
  const q = pin.quote ? `<span class="pinquote">“${esc(pin.quote)}”</span> ` : `<span class="warn">(pin has no quote)</span> `;
  const btn = `<button class="chipbtn" data-openpin data-id="${esc(pin.id)}" data-page="${pin.page}" data-quote="${esc(pin.quote||"")}" title="Open the PDF at this page with the quote marked">${esc(pin.label)}</button>`;
  let det="";
  if(v.ok){
    const x=v.passage;
    det=`<div class="pindetail" hidden><div class="mono">${x.paragraph?("para. "+esc(x.paragraph)):"p. "+esc(x.page_label)} · PDF p. ${x.page}${x.section?" · "+esc(x.section):""}</div><p>${esc(x.text.slice(0,300))}${x.text.length>300?"…":""}</p><button class="btn small" data-openpin data-id="${esc(pin.id)}" data-page="${pin.page}" data-quote="${esc(pin.quote||"")}">Open the PDF page</button></div>`;
  } else {
    det=`<div class="pindetail" hidden><p class="warn">The code could not find these words: ${esc(v.reason)}. Footnotes, tables and captions are not in the passages, so a pin cannot verify them.</p></div>`;
  }
  const struck = answerNote? " struck":"";
  return `<span class="pin${struck}">${q}<span class="chip">${btn}<span class="reg mono" title="${esc(regTitle)}">${esc(reg.join(""))}</span>${st}${diff}${answerNote}<button class="expbtn" aria-expanded="false" title="show the passage">▸</button></span>${det}</span>`;
}
```

Event delegation on document for [data-openpin] click → studio.openSource(id, page, quote); for .expbtn → toggle next .pindetail hidden + aria-expanded.

Note: data-quote attribute with quotes — esc handles " → &quot;. Good.

Now the ASK tab code, INGEST code... Let me also handle "running" tab mark: function setRunning(on) → tab03 button text append " · running" with aria-live span.

Progress lines: div aria-live="polite".

Stop: global stopFlag; Escape key sets it; each loop checks.

Now let me count clickables roughly per tab — fine.

Time to write the final file. I'll write it now, being careful with syntax. Given the scale, I'll keep functions compact.

Also note: "Before the code block: at most three short sentences saying what you built. After it: nothing."

Let me write the HTML now.

Some care: template literals inside the big template literals — I'll use string concatenation carefully. I'll write JS with regular functions and template literals; nested backticks not allowed, so use them only at one level.

For the ingest prompts, include pin syntax instructions.

Let me define todayStr(): new Date().toISOString().slice(0,10).

kebab: title.toLowerCase().replace(/[^a-z0-9]+/g,"-").replace(/^-|-$/g,"").

Index line format: `- [[slug]] — one-liner · (letters) · ✓N`.

For ask filing: index append: W.index += `\n- [[${slug}]] — ${short} · (${reg}) · ✓${verCount}`.

Log entry: W.log += `\n\n## [${today}] ask | ${title}\n\nFiled from an Ask answer; ${n} pins, all verified: ...` Keep simple.

Now, the checks panel on tab 04: "How the app checks itself" — a <details open> with list of one-line checks and live values. I'll render the same checks array with descriptions.

Let me write lint checks concretely:

```js
function computeLint(){
  const checks=[];
  const add=(name, count, pass, pages, desc)=>checks.push({name,count,pass,pages,desc});
  const allPins = P.flatMap(p=>p._pins.map(x=>({p:p.slug,pin:x})));
  const ver = allPins.filter(o=>verify(o.pin).ok);
  const statedM = W.index.match(/(\d[\d,]*) pins/);
  const stated = statedM? +statedM[1].replace(/,/g,"") : null;
  add("Pins found vs the index's stated number", stated===null?allPins.length:Math.abs(stated-allPins.length), stated===allPins.length, [], `index says ${stated}, code found ${allPins.length}`);
  add("Pins verified by this page's code", allPins.length-ver.length, ver.length===allPins.length, [...new Set(allPins.filter(o=>!verify(o.pin).ok).map(o=>o.p.slug))], `${ver.length} of ${allPins.length} verified`);
  const failMarked = allPins.filter(o=>o.pin.mark==="✓" && !verify(o.pin).ok);
  add("Pins marked ✓ that fail verification", failMarked.length, failMarked.length===0, [...new Set(failMarked.map(o=>o.p.slug))], "the page's own mark vs the code");
  // dangling
  const dangling = P.flatMap(p=>p._links.filter(s=>!bySlug[s]).map(s=>({p:p.slug,s})));
  add("Dangling [[links]]", dangling.length, dangling.length===0, [...new Set(dangling.map(o=>o.p))], "links to slugs with no page");
  // orphans
  const orphans = P.filter(p=>!backlinks[p.slug] && p.type!=="source" ? ... )
```

Hmm orphan = page with no backlinks? Spec earlier: "no orphan page". Orphan = no other page links to it. But source pages might have none... In the data there are none. I'll define orphan = no backlinks. 

  // sources vs pinned
```js
  const srcMismatch = P.filter(p=>{ const pinned=[...new Set(p._pins.map(x=>x.id))].sort().join(","); const src=(p.frontmatter.sources||[]).slice().sort().join(","); return pinned!==src; });
  add("frontmatter.sources differ from pinned documents", srcMismatch.length, srcMismatch.length===0, srcMismatch.map(p=>p.slug), "sources equal the set of pinned documents");
  // no pins
  const noPins = P.filter(p=>p._pins.length===0);
  add("Pages with no pins", noPins.length, noPins.length===0, noPins.map(p=>p.slug), "");
  // links not reciprocated
  const nonRecip = P.flatMap(p=>(p.frontmatter.links||[]).filter(s=>bySlug[s] && !bySlug[s]._links.includes(p.slug)).map(s=>p.slug));
  add("frontmatter.links not reciprocated in the body", [...new Set(nonRecip)].length, nonRecip.length===0, [...new Set(nonRecip)], "");
  // index coverage
  const indexSlugs=[...W.index.matchAll(/\[\[([^\]|#]+)\]\]/g)].map(m=>m[1]);
  const missingFromIndex = P.filter(p=>!indexSlugs.includes(p.slug)).map(p=>p.slug);
  const indexNoPage = indexSlugs.filter(s=>!bySlug[s]);
  add("Pages missing from the index / index lines without a page", missingFromIndex.length+indexNoPage.length, missingFromIndex.length+indexNoPage.length===0, missingFromIndex, "");
  // index ✓N mismatch
  const idxCount = [];
  for(const m of W.index.matchAll(/\[\[([^\]|#]+)\]\][^\n]*✓(\d+)/g)){ const p=bySlug[m[1]]; if(p){ const v=p._pins.filter(x=>verify(x).ok).length; if(v!==+m[2]) idxCount.push(p.slug); } }
  add("Index ✓N differs from the computed count", idxCount.length, idxCount.length===0, idxCount, "");
  // contested vs tensions
  const cards = P.flatMap(p=>contestedSlugs(p)); // pages with contested blocks
  const tensCards = [...W.tensions.matchAll(/card:\s*\[\[([^\]|#]+)\]\]/g)].map(m=>m[1]);
  const c1 = cards.filter(s=>!tensCards.includes(s)), c2 = tensCards.filter(s=>!cards.includes(s));
  add("Contested cards without a tensions entry and the reverse", c1.length+c2.length, c1.length+c2.length===0, c1, "");
  // stubs
  const stubs = P.filter(p=>p.frontmatter.status==="stub").map(p=>p.slug);
  add("Stub pages", stubs.length, false, stubs, "a stub waits for its ingest"); // pass=false always? "0 · pass" — stub count 1 → "1 · check". pass = stubs.length===0? but data has 1 stub → check. OK.
  // inbox pins
  const inboxPins = allPins.filter(o=>byId[o.pin.id] && byId[o.pin.id].status==="inbox");
  add("Pins to a document still in the inbox", inboxPins.length, inboxPins.length===0, [...new Set(inboxPins.map(o=>o.p.slug))], "");
  return checks;
}
```

contestedSlugs(p): count fenced contested blocks in p.body — I'll precompute p._contested = number of ```contested blocks.

OK. Now writing everything. Also "Lint now" button triggers computeLint + render; initial render at load too (big numbers at top computed at load).

Given constraints, let me now produce the final answer. I'll write the code in one go, mindful of correctness.

For the ingest stepper UI structure:

```html
<section id="tab-ingest" hidden>
  <div id="ingestHome"></div>
  <div id="ingestRun" hidden>
    <div class="mono" id="ingestStatus" aria-live="polite"></div>
    <div id="ingestSteps"></div>
  </div>
</section>
```

ingestHome: for each inbox doc a button; else "Nothing waits in the inbox".

startIngest(doc): ing = {doc, batches, ti:0, takeaways:[], failed:[], sentIds:new Set(), changes:[], step:1, stop:false, newSlugs:[]}; render step1 panel: scope text, batches table, Start button.

runBatches(): async loop; for each batch: if ing.stop break; progress; prompt; callModel(prompt, batch) — passages sent = batch.length (callModel adds passages count). Parse takeaways; process; render takeaways table (append rows). After loop: show step2 summary (failed box) + step3 buttons.

Process takeaway:
```js
function processTakeaway(t, doc){
  const passage = doc.passages.find(x=>x.id===t.passage);
  if(!passage || !ing.sentIds.has(passage.id)) { ing.dropped=(ing.dropped||0)+1; return; }
  const pinStr = makePin(doc.id, passage, t.quote||"");
  const m = pinStr.match(PIN_RE); // build pin obj
  const pin = {label:m[1], id:m[2], page:+m[3], quote:m[4], mark:"✓"};
  const v = verify(pin);
  const pages = (t.pages||[]).filter(s=>bySlug[s]);
  const newS = (t.pages||[]).filter(s=>!bySlug[s]);
  for(const s of newS) if(ing.newSlugs.length<2 && !ing.newSlugs.includes(s)) ing.newSlugs.push(s);
  if(v.ok) ing.takeaways.push({claim:t.claim, quote:t.quote, passage, pages, pin, pinStr});
  else ing.failed.push({claim:t.claim, quote:t.quote, passage, pin, nearest: nearestPassage(doc, passage.page, t.quote||"")});
}
```

makePin returns string; to verify I need pin object — I'll have makePin return {str, pin}.

nearestPassage(doc, page, quote): 
```js
function nearestPassage(doc, page, quote){
  const qw = norm(quote).split(" ");
  let best=null, bestLen=0;
  for(const x of doc.passages.filter(x=>x.page===page)){
    const tw = norm(x.text).split(" ");
    // longest run of consecutive qw words present in tw in order
    let len=0;
    for(let i=0;i<qw.length;i++){
      // find qw[i..] consecutive in tw
    }
    // simpler: longest common substring of words
  }
}
```
Simpler: compute longest common contiguous word sequence between qw and tw via DP-lite: for each start in qw, extend while qw[i+k] appears... I'll do straightforward: best run = max over i,j of length L such that qw[i..i+L-1] equals tw[j..j+L-1]. O(n*m*L) fine for short quotes. Implement with simple loops.

Step 3 source page draft:

```js
async function draftSource(){
  const tks = ing.takeaways.map(t=>({claim:t.claim, pin:t.pinStr}));
  const prompt = `Draft the source page for this document in the research wiki.\nDocument: ${JSON.stringify({title:doc.title, author:doc.author, published:doc.published, pages:doc.pages, url:doc.url, symbol:doc.symbol})}\nCite-as: ${citeAs(doc.id)}\nVerified takeaways with ready-made pins: ${JSON.stringify(tks)}\nSource-page anatomy: Full cite, Register, One-liner, Key takeaways, How NOT to read this, Where it feeds the wiki, Related.\nReturn JSON {"one_liner":..., "body":..., "touches":[{"slug","why"}]} — body at most 900 words, only the pins given, copied exactly. Pin syntax: [label](pin:id#pPAGE "quote") ✓; quote only words that stand in the passages given; the code will check.`;
  const r = await callModel(prompt, []);
  ...
  const body = r.json.body;
  // re-verify pins
  const pins = [...body.matchAll(PIN_RE)].map(...);
  const verCount = pins.filter(verify ok).length;
  const page = {slug: doc.id→ slug? source page slug: use doc id kebab? The stub slug is "a-hrc-57-61". Source page slug for A/HRC/57/61 would be "a-hrc-57-61"? The stub exists with that slug. Hmm — the stub is an entity page for the inbox document; the ingest rewrites the stub? Spec: "the stub a-hrc-57-61 is always among them, rewritten with its ten-item checklist sent along" — so the stub gets edited, and the source page is new with slug maybe derived from doc id. I'll use slug = kebab(doc.symbol || doc.id) e.g. "a-hrc-57-61"... that collides with stub. Use doc.id.toLowerCase() → "a/hrc/57/61" → kebab "a-hrc-57-61" — collision. I'll make source slug = kebab(doc.id)+"-source"? Hmm. Actually maybe the stub IS meant to become... The stub is type entity; source page type source. I'll create source page slug = kebab(doc.symbol||doc.id) and if taken, append "-src". Fine: "a-hrc-57-61-src"? Eh. Let me just use slug = kebab((doc.symbol||doc.id)) and if exists, slug+"-source". OK.
  frontmatter: {title: doc.title, type:"source", tags: touched slugs, register: register of stub (docRegister), status:"draft", updated: today, links: bodyLinks(body), sources:[doc.id]}
  ing.changes.push({kind:"new", slug, page, inserted:[body], verCount, notVer: pins.length-verCount, doc});
}
```

Touched pages draft:
```js
async function draftTouched(){
  const stubSlug = stub for doc (page with status stub & sources [doc.id]);
  const touched = [...new Set(ing.takeaways.flatMap(t=>t.pages))].filter(s=>bySlug[s]);
  if(stubSlug && !touched.includes(stubSlug)) touched.push(stubSlug);
  for(const slug of touched){ if stop break; prompt with page body + takeaways for slug + (stub? checklist) ; r=callModel; apply edits; ing.changes.push({kind:"edit", slug, page:newPage, inserted, ...}); }
  // new slugs cards
  for(const s of ing.newSlugs){ build simple new page from takeaways naming s }
  showReview();
}
```

Apply edits:
```js
function applyEdits(body, edits){
  let out = body; const inserted=[];
  for(const e of edits||[]){
    const md = e.markdown||"";
    inserted.push(md);
    if(!e.after || e.after==="end"){ out += "\n\n"+md+"\n"; continue; }
    const lines = out.split("\n");
    // find heading line matching e.after (## or ### etc, text equal)
    let idx=-1;
    for(let i=0;i<lines.length;i++){ const m=lines[i].match(/^(#{1,3})\s+(.*)$/); if(m && m[2].trim().toLowerCase()===String(e.after).trim().toLowerCase()){ idx=i; break; } }
    if(idx<0){ out += "\n\n<!-- heading not found: "+esc? no, raw -->"+md+"\n"; continue; }
    // find next heading of level <= current
    const lvl = lines[idx].match(/^(#{1,3})/)[1].length;
    let j=idx+1;
    while(j<lines.length){ const m=lines[j].match(/^(#{1,3})\s/); if(m && m[1].length<=lvl) break; j++; }
    lines.splice(j,0,"",md);
    out = lines.join("\n");
  }
  return {body:out, inserted};
}
```

Then newPage = {...old, body:newBody, frontmatter:{...fm, links: union(fm.links, [sourceSlug]), sources: union(fm.sources,[doc.id])}, updated: today}. Re-verify pins in newBody: count.

Contested: if r.json.contested, append fenced block to body: "```contested\n"+contested+"\n```" and record ing.newContested.push({page:slug, block}).

Review:
```js
function showReview(){
  ing.step=4; render review area: current index ci=0; renderCard();
}
function renderCard(){
  const c = ing.changes[ing.ci];
  card html: fieldset legend `${c.page.title} (${c.page.type}) — ${c.kind==="new"?"new page":"edited"}`; counts: `${c.inserted.length} paragraphs inserted · ${c.pinAdded} pins added (${c.ver} verified, ${c.notVer} not verified)`; body rendered with cardMode and ins markers. To mark inserted: I'll wrap inserted md with sentinels when building body for display: displayBody = body with each inserted md preceded by "<!--INS-->" and followed by "<!--/INS-->". Since inserted strings are exact substrings, I can do body.split(md).join sentinel-wrapped. Renderer handles <!--INS--> lines.
  buttons Approve/Reject with labels `Approve change ${ci+1} of ${n}`.
}
```

Renderer INS handling: lines equal "<!--INS-->" → insFlag=true; "<!--/INS-->" → insFlag=false. When emitting block in cardMode: wrap with class. I'll implement in the block emitters: `const cls = ctx.card? (insFlag?"ins":"dim") : ""`.

Approve: c.approved=true; ci++; if ci<changes.length renderCard else show File button. Reject: c.approved=false; note; next.

File:
```js
function fileChanges(){
  const approved = ing.changes.filter(c=>c.approved);
  for(const c of approved){
    if(c.kind==="new"){ P.push(c.page); bySlug[c.slug]=c.page; parsePage(c.page); W.index += `\n- [[${c.slug}]] — ${esc? no, raw one-liner} · (${reg}) · ✓${ver}`; }
    else { const i=P.findIndex(p=>p.slug===c.slug); P[i]=c.page; bySlug[c.slug]=c.page; parsePage(c.page); /* recompute index line ✓N */ updateIndexLine(c.slug); }
    c.page.frontmatter.updated = today;
  }
  byId[ing.doc.id].status="ingested";
  W.log += `\n\n## [${today}] ingest | ${ing.doc.symbol||ing.doc.id}: ${ing.doc.short_title}\n\nRead ${ing.doc.passages.length} passages. Approved: ${approved.map(c=>c.slug).join(", ")||"none"}. Rejected: ${ing.changes.filter(c=>!c.approved).map(c=>c.slug).join(", ")||"none"}.`;
  for(const nc of ing.newContested||[]) W.tensions += `\n\n### ${kebab(nc.title||"claim")}\nstatus: open\ncard: [[${nc.page}]]\n...`;
  S.changes += approved.length; updateHeader();
  // re-lint
  const before = ing.lintBefore, after = computeLint(); show side by side.
  renderIngestHome(); // doc no longer inbox
}
```

updateIndexLine(slug): replace the line in W.index containing [[slug]] with recomputed line. Implement: split lines, find line with `[[${slug}]]`, rebuild `- [[slug]] — one-liner · (letters) · ✓N` — need one-liner: keep existing text between `]] — ` and ` · (`. I'll regex replace ✓N only: line.replace(/✓\d+/,"✓"+n). Good, simpler.

parsePage(p): sets _links, _pins, _contested.

OK also "running" mark and counters during ingest: update ingStatus text "calls so far m · passages sent k" — read from S.

Now ASK tab details — the "grey box above states what each step will send before it goes": a div .sendnote updated per step.

Let me now also handle "Change pages": after call1, render chips; link toggles a div with checkboxes for all pages (label = title), checked if in slugs; "Send these pages" is the main button which now reads `Send ${n} pages to step 2`. On click, slugs = ticked ∩ existing, max 5.

Answer rendering: 
```js
const sentSet = new Set();
for(const s of slugs) for(const m of bySlug[s].body.matchAll(PIN_RE)) sentSet.add(m[2]+"#p"+m[3]+"|"+(m[4]||""));
```
Render answer with ctx {answerSet: sentSet}. Then count verified by register:
```js
const apins=[...answer.matchAll(PIN_RE)].map(...);
const byReg={}; let allVer=true;
for(const pin of apins){ const ok = sentSet.has(key) && verify(pin).ok; if(!ok) allVer=false; else { const r=docRegister(pin.id)[0]||"?"; byReg[r]=(byReg[r]||0)+1; } }
```
Count line: "verified pins by register: a 0 · b 1 · c 4 · d 0 · e 0 · f 0 (n of m pins in the answer verified)".

File card: fieldset with preview: slug (editable? no—computed, shown), tags input, register shown, status draft, links, sources, body preview (rendered). Buttons "File this page" (disabled until allVer && apins.length>0, with reason text) and "Copy answer".

File this page: build page, push, index line, log entry, S.changes++, message aria-live "Filed as [[slug]]".

Copy answer: put answer markdown in details textarea.

Alright — also tab 05 tensions rendering: render W.tensions via renderBody; card links: in renderBody, [[slug]] links already become a[data-slug]; clicking handled globally: document click on a[data-slug] → e.preventDefault(); location.hash = slug; showTab('pages'); showPage(slug).

Global click handler:
```js
document.addEventListener("click", e=>{
  const op = e.target.closest("[data-openpin]");
  if(op){ studio.openSource(op.dataset.id, +op.dataset.page, op.dataset.quote); return; }
  const ex = e.target.closest(".expbtn");
  if(ex){ const d=ex.closest(".pin").querySelector(".pindetail"); const hid=d.hidden; d.hidden=!hid; ex.setAttribute("aria-expanded", String(!hid)); ex.textContent = hid?"▾":"▸"; return; }
  const sl = e.target.closest("a[data-slug]");
  if(sl){ e.preventDefault(); location.hash = sl.dataset.slug; }
  ...
});
```

showPage also called from hashchange: if hash slug exists → activate pages tab + showPage.

Tabs:
```js
const TABS=[["pages","01 PAGES"],["ask","02 ASK"],["ingest","03 INGEST"],["check","04 CHECK"],["record","05 RECORD"]];
```
Tab buttons in HTML static; JS wires.

Arrow keys on tablist: keydown ArrowRight/Left → focus & activate next/prev.

Escape: stopFlag=true.

Now header counts at load: compute pins total & verified, inbox count, built. 

Let me write the final code. I'll try to keep it tight. Also remember: no external anything; Chart.js not needed (lean bar is a div).

One more: "FIG.01" labels on lean bar, takeaways table, lint table — add mono fig labels.

Also the app must explain itself: add "How this is computed" mono hints near big numbers.

Let me write it all out now. I'll be careful with quotes inside template strings (use backticks in JS; inside them avoid backticks). In HTML attributes with data-quote I use esc() which escapes quotes — good.

Potential pitfall: PIN_RE with /g used with .matchAll — matchAll requires /g and doesn't mutate lastIndex? Actually matchAll internally clones? String.prototype.matchAll uses the regex's lastIndex? It creates a clone internally (per spec it uses a new RegExp with same flags? It actually uses the original's lastIndex as start). To be safe, I'll create fresh regex via new RegExp(PIN_SRC,"g") in a helper pinsOf(str). Define PIN_SRC string.

```js
const PIN_SRC = String.raw`\[([^\]]+)\]\(pin:([^#\s)]+)#p(\d+)(?: "([^"]*)")?\) ?(✓|⚠)`;
const pinsOf = s => [...s.matchAll(new RegExp(PIN_SRC,"g"))].map(m=>({label:m[1],id:m[2],page:+m[3],quote:m[4]||null,mark:m[5],raw:m[0]}));
```

Use pinsOf everywhere.

inlineWithPins: manual loop with regex exec on fresh regex.

Now write. Also ensure `hidden` attribute CSS rule.

Let me draft the entire file:

I'll now write it, estimating ~1100-1300 lines. Go.

For the ingest batches table: columns: batch, passages (ids range or paragraph range), PDF pages. paragraph range: first.paragraph+"–"+last.paragraph (may be null → use page labels). I'll show `para ${first.paragraph||first.page_label} – ${last.paragraph||last.page_label}` and `PDF p. ${first.page}–${last.page}`.

Takeaways table columns: claim, quote, passage (para + PDF p.), pages chips, verification ("✓ verified" / "⚠ not found").

Failed box: list each: quote, passage named (para/page), nearest passage (para/page + run length), Open PDF page button (data-openpin with nearest passage page and quote).

OK writing now. Also step 3 buttons appear after step 1 completes: "Draft the source page (1 call)" then after that "Draft the changes to n pages (n calls)". Spec has both in step 3; I'll show both buttons, source first then touched (touched needs source slug for links — fine, sequential awaits on click; or one button runs both? Spec: two separate buttons). I'll render both; touched button disabled until source drafted.

Review after touched drafts done.

Also "the stub a-hrc-57-61 is always among them, rewritten with its ten-item checklist sent along" — the stub body contains a ten-item list; I'll just send the stub body as-is (it contains the checklist). Fine.

Edge: doc with symbol null → button label short_title.

Let me also compute "c characters" for scope: sum of passage text lengths.

Alright, final code writing time. I'll write it as one continuous block, then review for syntax errors mentally.

Also add Credits line at bottom of app (footer area): "Method notes after Karpathy's LLM Wiki; QA guidance: UK Government Analysis Function (OGL 3.0); A11Y Project checklist (CC BY 4.0)."

Let me write:

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
html,body{margin:0;padding:0}
body{background:var(--paper);color:var(--ink);font:16px/1.55 -apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;padding:0 20px 60px}
.mono{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:11.5px;letter-spacing:.08em;text-transform:uppercase}
.serif{font-family:Georgia,"Times New Roman",serif}
a{color:var(--red)}
button{font:inherit;cursor:pointer}
:focus-visible{outline:3px solid var(--red);outline-offset:2px}
header.top{display:flex;justify-content:space-between;gap:24px;align-items:flex-end;border-bottom:1px solid var(--rule);padding:18px 0 12px;flex-wrap:wrap}
...
</style>
```

I'll write all CSS then HTML then JS. Let me be thorough but efficient. Time to produce output. I'll write the code now in final form.

For tab buttons: 
```html
<nav class="tabs" role="tablist" aria-label="App sections">
 <button role="tab" id="tabbtn-pages" aria-controls="tab-pages" aria-selected="true" data-tab="pages">01 PAGES</button>
 ...
</nav>
```
Running mark: `<span class="runmark" aria-live="polite"></span>` inside ingest tab button.

Panels: `<section id="tab-pages" role="tabpanel" aria-labelledby="tabbtn-pages">` etc.

Main JS sections:
1. data + helpers
2. header/counters
3. tabs + hash
4. renderers (inline, pin, contested, body)
5. tab 01
6. tab 02
7. tab 03
8. tab 04
9. tab 05
10. global events, init

Write it.

Careful: in renderBody, headings may contain pins? unlikely but inlineWithPins handles.

For lists inside contested? no.

Also plain links regex must not clash with pin syntax — pins extracted first in inlineWithPins, so remaining [..](..) are plain links. But [[slug]] also matches [..](..)? No, [[slug]] has no (..). Order: replace [[..]] first, then [t](url). But pin already removed. However plain link regex `\[([^\]]+)\]\((https?...)` could match inside `[[slug]]`? `[[slug]]` — the regex would match `[slug]` starting at second `[`? `\[([^\]]+)\]\(` requires `](` after — `[[slug]]` has `]]` not `](`. Safe.

Bold regex on escaped text: `**text**` fine.

Now the ASK prompt texts — include register names and pin syntax.

Let me also make sure I announce what leaves the browser: the sendnote div text before each call, plus progress line includes chars.

Write final. I'll now compose the entire document text. (Being careful: total under ~1500 lines.)

For ingest step panels, I'll build DOM via innerHTML strings into #ingestSteps.

Let me define ingest render functions:

```js
function renderIngestHome(){
  const inbox = D.filter(d=>d.status==="inbox");
  home.innerHTML = inbox.length? inbox.map(d=>`<button class="btn" data-ingest="${esc(d.id)}">${esc(d.symbol? "Ingest "+d.symbol : "Ingest "+d.short_title)}</button>`).join(" ") : `<p>Nothing waits in the inbox.</p>`;
}
```

Click data-ingest → startIngest(byId[id]).

startIngest renders stepper:
```js
function startIngest(doc){
  const batches=[]; for(let i=0;i<doc.passages.length;i+=25) batches.push(doc.passages.slice(i,i+25));
  ing={doc,batches,ti:0,takeaways:[],failed:[],sentIds:new Set(),changes:[],newSlugs:[],ci:0,stop:false,step:1,dropped:0,newContested:[],lintBefore:computeLint()};
  setRunning(true);
  const chars = doc.passages.reduce((n,x)=>n+x.text.length,0);
  steps.innerHTML = `
   <div class="mono" aria-live="polite" id="ingProg"></div>
   <div class="card"><h2 class="serif">Step 1 · Scope: the whole document</h2>
   <p>All ${doc.passages.length} passages will be sent, in batches of 25 (${batches.length} calls), ${chars.toLocaleString()} characters; nothing is held back.</p>
   <table><caption class="mono">FIG.01 · batches — every passage is sent exactly once</caption><thead><tr><th scope="col">batch</th><th scope="col">paragraphs</th><th scope="col">PDF pages</th><th scope="col">passages</th></tr></thead><tbody>
   ${batches.map((b,i)=>`<tr><td>${i+1}</td><td>${esc(b[0].paragraph||b[0].page_label)} – ${esc(b[b.length-1].paragraph||b[b.length-1].page_label)}</td><td>${b[0].page}–${b[b.length-1].page}</td><td>${b.length}</td></tr>`).join("")}
   </tbody></table>
   <button class="btn primary" id="ingStart">Start</button> <button class="btn" id="ingStop" hidden>Stop</button>
   <div id="ingTakeaways"></div><div id="ingFailed"></div><div id="ingStep3"></div><div id="ingReview"></div></div>`;
  ...
}
```

runBatches async; per batch build prompt; call; process; render tables incrementally.

Takeaway prompt:
```js
const prompt = `You are reading one document into a research wiki. Every claim must be pinned to a passage with a verbatim quote.\nPassages (JSON, sent now: ${b.length} passages): ${JSON.stringify(b.map(x=>({id:x.id,page:x.page,paragraph:x.paragraph,text:x.text})))}\nIndex of the wiki: ${W.index}\nReturn JSON only: {"takeaways":[{"claim":"...","quote":"8-40 words copied verbatim from ONE passage","passage":"passage id","pages":["slug from the index"]}]} — at most 10 takeaways. Pin syntax: [label](pin:id#pPAGE "quote") ✓. Quote only words that stand in the passages given; the code will check.`;
```

Process and render.

After batches: render failed box + step3:
```js
step3.innerHTML = `<h2>Step 2 · Takeaways</h2> ... <h2>Step 3 · Drafts</h2>
 <button id="draftSrc" class="btn primary">Draft the source page (1 call)</button>
 <button id="draftTouched" class="btn" disabled>Draft the changes to n pages (n calls)</button>`;
```

draftSrc: as planned; push change; enable draftTouched with count = touched.length.

draftTouched: loop; then showReview.

showReview: render card at ing.ci.

renderReviewCard: as planned with sentinels. To wrap inserted: 
```js
let disp = c.page.body;
for(const md of c.inserted){ disp = disp.split(md).join("<!--INS-->\n"+md+"\n<!--/INS-->"); }
```
Renderer: handle lines "<!--INS-->" and "<!--/INS-->" setting ins flag; in cardMode wrap blocks with class.

I'll add ctx.card flag; block emitters: `blk(tag, inner)` helper:
```js
const blk=(tag,inner)=>{ const cls = ctx.card ? (insFlag?' class="ins"':' class="dim"') : ""; return `<${tag}${cls}>${inner}</${tag}>`; };
```

Pins inside dim blocks still render normally.

Approve/Reject handlers; after last → file button.

fileChanges as planned; also update tab01 list (re-render), header, lint display, setRunning(false), renderIngestHome, and show summary "Filed n changes; lint before/after".

Also update W.count? W.count is pages count — update to P.length.

OK, and tab 04 render:

```js
function renderCheck(){
  const allPins = P.flatMap(p=>p._pins);
  const ver = allPins.filter(x=>verify(x).ok).length;
  bigNum.textContent = `${ver} of ${allPins.length} pins verified by this page`;
  const checks = computeLint();
  needLook.textContent = `${checks.filter(c=>!c.pass).length} lint checks need a look`;
  render table rows: name | `${count} · ${pass?"pass":"check"}` | pages links
  checks panel details with desc lines.
}
```

Lint now button → renderCheck() again (button text "Re-run").

Tab 05:

```js
function renderRecord(){
  const entries = W.log.split(/(?=^## )/m).filter(s=>s.trim());
  const newestFirst = orderSwitch.checked;
  const list = newestFirst? entries.slice().reverse() : entries;
  logEl.innerHTML = list.map(e=>{
    const m = e.match(/^## \[([^\]]+)\] (\w+) \| (.*)/);
    const session = W.log.indexOf(e) >= sessionLogStart; // hmm indexOf on substring; better: track count of entries at load: sessionEntries = entries.length - initialLogEntries
    ...
  }).join("");
}
```

Simpler: initialLogLen = W.log.length at load; an entry is "this session" if its position in W.log >= initialLogLen. Compute via indexOf(e) — entries are unique enough. I'll compute idx = W.log.indexOf(e); session = idx >= sessionLogStart.

Each entry: `<details><summary class="mono">[date] op | subject ${session?'<span class="sess">this session</span>':""}</summary><div class="logbody">${renderBody(rest)}</div></details>`.

Tensions: `<div id="tensionsView">${renderBody(W.tensions)}</div>` — card links clickable via global handler.

Buttons: Download the wiki; Download changed pages (markdown) shown when S.changes>0.

Method note + source line.

Footer static in HTML with spans filled by JS: wiki.source, wiki.built.

Header right counters: spans #cChanges #cCalls #cPassages.

OK — also "How this is computed" hints: add `<div class="mono hint">computed by this page's code from WORKSHOP_DATA.wiki / .library</div>` under big numbers.

Now, finally write everything. Let me produce the answer. I'll write the intro sentence(s) then the code block.

Let me carefully write the JS to avoid bugs:

- verify uses byId; docRegister uses P.find — after filing new pages, recompute fine.
- parsePage(p) sets _links, _pins, _contested count: (p.body.match(/```contested/g)||[]).length.

- backlinks recompute function: recomputeBacklinks().

Init:
```js
P.forEach(parsePage); recomputeBacklinks(); renderHeader(); renderPageList(); renderIndexView(); renderCheck(); renderRecord(); renderIngestHome(); wireTabs(); 
if(location.hash){ const s=location.hash.slice(1); if(bySlug[s]) showPage(s); }
```

showPage(slug): set active tab pages; pageview.innerHTML = pageHtml(bySlug[slug]); window.scrollTo? fine.

pageHtml(p):
```js
function pageHtml(p){
  const fm=p.frontmatter;
  const reg=(fm.register||[]).map(r=>`<span class="mono reg" title="${r} ${REGNAMES[r]||""}">${r}</span>`).join(" ");
  const pins=p._pins.length, ver=p._pins.filter(x=>verify(x).ok).length;
  const linksOut=(fm.links||[]).map(s=> bySlug[s]? `<a href="#${esc(s)}" data-slug="${esc(s)}">${esc(bySlug[s].title)}</a>` : `<span class="bad">${esc(s)} (no page)</span>` + (p._links.includes(s)?"":" <span class='mono'>frontmatter only</span>")).join(", ");
  const linkedFrom=(backlinks[p.slug]||[]).map(s=>`<a href="#${esc(s)}" data-slug="${esc(s)}">${esc(bySlug[s].title)}</a>`).join(", ")||"none";
  const sources=(fm.sources||[]).map(id=>{ const d=byId[id]; return d? `<div>${esc(d.short_title||d.title)} · ${esc(d.kind)} · ${d.year} · <a href="${esc(d.url)}" target="_blank" rel="noopener">document</a>${d.status==="inbox"?' · <span class="warn mono">inbox</span>':""}</div>` : `<div class="bad">${esc(id)} (not in the library)</div>`; }).join("");
  return `<h1 class="serif">${esc(p.title)}</h1>
  <div class="badges mono">${esc(p.type)} · ${reg} · ${esc(fm.status||"")} · updated ${esc(fm.updated||"")} · ${pins} pins (${ver} verified)</div>
  <div class="tags mono">${(fm.tags||[]).map(t=>`<span class="tag">#${esc(t)}</span>`).join(" ")}</div>
  <div class="pagebody">${renderBody(p.body,{})}</div>
  <h2 class="serif">Links out</h2><p>${linksOut||"none"}</p>
  <h2 class="serif">Linked from</h2><p>${linkedFrom}</p>
  <h2 class="serif">Sources</h2>${sources||"<p>none</p>"}
  <button class="btn" id="copyPage">Copy page as markdown</button>
  <details id="copyBox" hidden><summary class="mono">markdown</summary><textarea readonly rows="14" style="width:100%">${esc(pageMarkdown(p))}</textarea></details>`;
}
```

pageMarkdown(p): yaml frontmatter + body.

Index view:
```js
function renderIndexView(){
  pageview.innerHTML = `<h1 class="serif">Index</h1><div class="mono hint">rendered from wiki.index · ${P.length} pages</div><div class="pagebody">${renderBody(W.index,{})}</div>`;
}
```

Filter input event → renderPageList.

pagelink click (delegate on pagelist) → location.hash = slug.

OK, writing the final output now. I'll keep comments minimal to save lines. Let me go.

One more consideration: the answer area in tab 02 must be inside data-source="ai". I'll wrap: `<div data-source="ai">...rendered answer...</div>` plus a mono tag "model answer — every pin re-checked by this page's code".

Also "What the library cannot answer" section from cannot_answer.

Also struck-through pins: in pinHtml when ctx.answerSet and not accepted → wrap pin span class "struck" and note. Implement: answerNote computed; if not accepted, add class.

Let me finalize pinHtml signature: pinHtml(pin, ctx) where ctx={answerSet?:Set, card?:bool}.

In renderBody, ctx passed through.

Now writing. Also ensure `studio` guard: typeof studio !== "undefined" — but spec says studio.ask exists when asked. I'll call directly but wrap in try/catch to show error.

callModel:
```js
async function callModel(prompt, passages){
  S.calls++; S.passages += (passages||[]).length; renderHeader();
  let raw;
  try{ raw = await studio.ask(prompt, {json:true}); }
  catch(err){ return {error:String(err), raw:"", json:null, chars:prompt.length}; }
  const txt = String(raw).trim();
  let json=null;
  try{ json=JSON.parse(txt); }catch(e){
    const m=txt.match(/```(?:json)?\s*([\s\S]*?)```/);
    if(m){ try{ json=JSON.parse(m[1]); }catch(e2){} }
  }
  return {raw:txt, json, chars:prompt.length, passages:(passages||[]).length};
}
```

Progress helper: setProg(el, msg).

Stop: global `let STOP=false;` Escape → STOP=true; loops check `if(STOP) break;` and reset STOP=false at start of each run.

Ask flow code:

```js
const ask = {slugs:[], sentSet:null, answer:null, title:null, cannot:null, allVer:false, regCounts:{}};
askBtn.onclick = async ()=>{
  const q = qInput.value.trim(); if(!q){ qInput.focus(); return; }
  askBtn.disabled=true;
  try{
    if(!ask.answer){
      sendNote.textContent = `Step 1 will send: the index (${W.index.length.toLocaleString()} characters) and your question (${q.length} characters). No library passages leave the browser.`;
      setProg(askProg, `Step 1 of 2 · sending the index and the question…`);
      const p1 = `You route questions to pages of a research wiki.\nINDEX:\n${W.index}\n\nQUESTION:\n${q}\n\nReturn JSON only: {"pages":["slug",...]} — at most 5 slugs that exist in the index.`;
      const r = await callModel(p1, []);
      if(STOP){...}
      if(!r.json || !Array.isArray(r.json.pages)){ showRaw(askProg, r, p1); return; }
      const dropped = r.json.pages.filter(s=>!bySlug[s]);
      ask.slugs = r.json.pages.filter(s=>bySlug[s]).slice(0,5);
      renderSlugChips(dropped);
      askBtn.textContent = `Send ${ask.slugs.length} pages to step 2`;
      askBtn.dataset.phase="2";
    } else { askBtn.dataset.phase="0"; ask.answer=null; ... } // "Ask again" resets
  } finally { askBtn.disabled=false; }
};
```

Hmm, phases: initial phase "1". After answer shown, button reads "Ask again" and clicking resets and runs step 1 again. Let me manage with ask.phase variable instead of dataset.

Phase 2 click: gather ticked checkboxes if change list open else ask.slugs; run call2.

```js
async function runStep2(){
  const slugs = currentSlugs();
  const bodies = slugs.map(s=>`PAGE ${s}:\n${bySlug[s].body}`).join("\n\n---\n\n");
  sendNote.textContent = `Step 2 will send: ${slugs.length} pages, ${(bodies.length).toLocaleString()} characters, and your question; 0 library passages have left the browser.`;
  setProg(askProg, `Step 2 of 2 · sending ${slugs.length} pages, ${bodies.length.toLocaleString()} characters…`);
  const p2 = `You answer from the pages of a research wiki. Cite every claim with a pin.\nPAGES:\n${bodies}\n\nQUESTION:\n${q}\n\nReturn JSON only: {"title":"...","answer":"...","cannot_answer":"..."}. Answer at most 350 words. Pin syntax: [label](pin:id#pPAGE "quote") ✓ — the pin must already stand on one of the pages sent, with the same quote; quote only words that stand in the pages given; the code will check. Name the register where it matters — (a) treaty law, (b) General Comments, (c) UN/agency/soft-law reports, (d) national human rights institution, (e) civil society, (f) scholarship; keep each document's own verb; never present (c)–(f) as what the treaty requires.`;
  const r = await callModel(p2, []);
  if(!r.json || typeof r.json.answer!=="string"){ showRaw(...); return; }
  ask.title=r.json.title||"Untitled"; ask.answer=r.json.answer; ask.cannot=r.json.cannot_answer||"";
  ask.sentSet = new Set();
  for(const s of slugs) for(const pin of pinsOf(bySlug[s].body)) ask.sentSet.add(pin.id+"#p"+pin.page+"|"+(pin.quote||""));
  renderAnswer();
  askBtn.textContent="Ask again"; ask.phase=0;
}
```

renderAnswer: builds HTML into askResult:
```js
const apins = pinsOf(ask.answer);
let allVer = apins.length>0;
const regCounts={};
for(const pin of apins){ const key=...; const ok = ask.sentSet.has(key) && verify(pin).ok; if(!ok) allVer=false; else { const r=(docRegister(pin.id)[0]||"?"); regCounts[r]=(regCounts[r]||0)+1; } }
ask.allVer=allVer; ask.regCounts=regCounts; ask.apins=apins;
const regLine = "abcdef".split("").map(l=>`${l} ${regCounts[l]||0}`).join(" · ");
askResult.innerHTML = `<div class="mono">model answer — every pin re-checked by this page's code · ${apins.length} pins, ${Object.values(regCounts).reduce((a,b)=>a+b,0)} verified</div>
 <div data-source="ai"><h2 class="serif">${esc(ask.title)}</h2><div class="pagebody">${renderBody(ask.answer,{answerSet:ask.sentSet})}</div>
 <h3 class="serif">What the library cannot answer</h3><div class="pagebody">${renderBody(ask.cannot,{})}</div></div>
 <div class="mono">verified pins by register: ${regLine}</div>
 <button class="btn" id="fileAsk">File as a question page</button>
 <div id="fileCard"></div>`;
```

fileAsk click → render filing card:
```js
function renderFileCard(){
  const slug = uniqueSlug(kebab(ask.title||"question"));
  const links=[...new Set(pinsOf? no—links from answer: [...ask.answer.matchAll(/\[\[([^\]|#]+)\]\]/g)].map(m=>m[1]))];
  const sources=[...new Set(ask.apins.map(p=>p.id))];
  const reg=[...new Set(ask.apins.flatMap(p=>docRegister(p.id)))];
  const body = `# ${ask.title}\n\n**Short answer.** ${firstSentence(ask.answer)}\n\n## Reasoning\n\n${ask.answer}\n\n## What the library cannot answer\n\n${ask.cannot}\n\n## Related\n\n${links.map(s=>`[[${s}]]`).join(" ")||"none"}`;
  fileCard.innerHTML = `<fieldset class="card"><legend class="mono">file as a question page</legend>
   <p>slug <code>${esc(slug)}</code> · type question · status draft · updated ${today} · register ${(reg.join(""))||"?"} · sources ${sources.map(esc).join(", ")||"none"} · links ${links.map(esc).join(", ")||"none"}</p>
   <label for="askTags">tags (comma-separated)</label><input id="askTags" type="text">
   <details open><summary class="mono">preview</summary><div class="pagebody">${renderBody(body,{})}</div></details>
   <button class="btn primary" id="doFile" ${ask.allVer? "":"disabled"}>File this page</button> ${ask.allVer? "":`<span class="warn">disabled: ${ask.apins.length===0?"the answer has no pins to verify":"some pins in the answer do not verify"}</span>`}
   <button class="btn" id="copyAns">Copy answer</button>
   <div class="mono" aria-live="polite" id="filedMsg"></div></fieldset>`;
}
```

doFile: build page obj, push, parsePage, backlinks, index line, log, S.changes++, renderHeader, renderPageList, filedMsg "Filed as [[slug]] — this session", re-render check counts maybe.

uniqueSlug: while bySlug[s] s+="-2" etc.

firstSentence: ask.answer.split(/(?<=[.!?])\s/)[0] — lookbehind ok in modern browsers; safer: match /^[^.!?]*[.!?]/.

OK. Now tab 03 remaining functions and tab 04/05. I think I have the full picture. Let me write the final file. I'll aim for clarity over brevity in a few spots but keep total manageable.

Also note: after filing/ingest, tab01 list and check should refresh — call renderPageList() and renderCheck() where relevant.

Let me write out everything now. Final answer format: 1-3 sentences, then html code block, nothing after.

Writing the code (finally):

I need to double check contestedHtml positions table: pin chip small — reuse pinHtml with ctx {} but compact? pinHtml includes quote inline which in table cell would be long. For the table, spec says "pin chip" — I'll render a compact chip: button label + reg + status, without the quote (quote is in the card? The claim positions table: "sign in words, register, pin chip, gloss, page link"). I'll make pinChipSmall(pin): chip with label button, reg, ✓/⚠, expandable detail. Reuse pinHtml but with ctx.compact to skip the quote span. Add ctx.compact.

contestedHtml(block, ctx):
```js
function contestedHtml(o, ctx){
  const pct = Math.round(lean(o)*100);
  const rows = o.positions.map(p=>{
    const pin = pinsOf(p.pinRaw)[0] || {label:p.pinRaw,id:"",page:0,quote:null,mark:"?"};
    const signWord = p.sign==="+"?"supports":p.sign==="-"?"contests":"mixed";
    const pageSlug = (p.page||"").match(/\[\[([^\]|#]+)\]\]/);
    return `<tr><td>${signWord} (${p.sign})</td><td class="mono">${esc(p.register||"?")}</td><td>${pinHtml(pin,{compact:true})}</td><td>${esc(p.gloss||"")}</td><td>${pageSlug?`<a href="#${esc(pageSlug[1])}" data-slug="${esc(pageSlug[1])}">${esc(pageSlug[1])}</a>`:""}</td></tr>`;
  }).join("");
  const inTensions = W.tensions.includes(`card: [[${ctx.pageSlug}]]`);
  return `<div class="contested card">
   <div class="mono fig">contested claim</div>
   <h3>${esc(o.claim||"")}</h3>
   <div class="verdict serif">${esc((o.verdict||"").replace(/-/g," "))}</div>
   <p>${esc(o.note||"")}</p>
   <div class="mono fig">FIG.01 · lean bar — descriptive: support ${pct}% of weighted positions · weights a 5 · b 4 · c 3 · d 2 · e 1 · f ½ · the verdict is the answer</div>
   <div class="leanbar" role="img" aria-label="support ${pct}% of weighted positions"><div style="width:${pct}%"></div></div>
   <table><caption class="mono">positions — sign · register · pin · gloss · page</caption><thead><tr><th scope="col">sign</th><th scope="col">register</th><th scope="col">pin</th><th scope="col">gloss</th><th scope="col">page</th></tr></thead><tbody>${rows}</tbody></table>
   ${inTensions?`<p class="mono"><a href="#" data-goto="record">in the tensions register (tab 05)</a></p>`:""}
  </div>`;
}
```

data-goto handler: switch tab.

renderBody needs ctx.pageSlug for contested — pass ctx through.

OK writing final now for real. I'll produce the document.

Also add `.struck{text-decoration:line-through; opacity:.75}`.

Also `.pinquote{font-family:Georgia,serif}`.

Also `.ins{background:var(--yellow);border-left:3px solid var(--red);padding-left:8px}` `.dim{color:var(--grey)}`.

Also `.leanbar{height:10px;background:var(--rule);margin:6px 0 12px} .leanbar div{height:100%;background:var(--red)}`.

Also `.verdict{font-size:34px;color:var(--red);margin:4px 0 8px}`.

Also `.chip{display:inline-flex;align-items:center;gap:4px;border:1px solid var(--rule);border-radius:999px;padding:0 6px;margin:0 2px;vertical-align:middle;background:#fff8? keep paper}`. chipbtn: `border:none;background:none;font-family:mono;font-size:11px;color:var(--red);text-decoration:underline;padding:2px 2px`.

expbtn: small borderless.

pindetail: `display:block;border-left:2px solid var(--rule);margin:4px 0 8px 12px;padding:4px 10px;font-size:14px`.

Tables: `table{width:100%;border-collapse:collapse;margin:10px 0} caption{text-align:left;padding:4px 0;color:var(--grey)} th{font-family:mono;font-size:11px;text-transform:uppercase;letter-spacing:.08em;text-align:left;border-bottom:1px solid var(--ink);padding:4px 8px 4px 0} td{border-top:1px solid var(--rule);padding:6px 8px 6px 0;vertical-align:top} td.num{text-align:right}`.

Buttons `.btn{border:1px solid var(--ink);background:transparent;padding:6px 12px;font-family:mono;font-size:11.5px;letter-spacing:.08em;text-transform:uppercase;border-radius:2px} .btn:hover{border-color:var(--red);color:var(--red)} .btn.primary{background:var(--red);border-color:var(--red);color:#fff} .btn:disabled{opacity:.45;cursor:not-allowed}`.

Tabs: `.tabs{display:flex;gap:2px;border-bottom:1px solid var(--rule);margin:0 0 18px} .tabs [role=tab]{border:none;background:none;padding:10px 14px;font-family:mono;font-size:12px;letter-spacing:.1em;color:var(--grey);border-bottom:2px solid transparent} .tabs [role=tab][aria-selected=true]{color:var(--red);border-bottom-color:var(--red)}`.

Header: `.top{...} .kicker{...} h1.title{font-family:Georgia;font-size:30px;margin:2px 0 4px;font-weight:normal} .dataline{...} .counters{text-align:right}`.

Rail: `.cols{display:flex;gap:24px;align-items:flex-start} .rail{width:320px;flex:none;border-right:1px solid var(--rule);padding-right:16px} .main{flex:1;max-width:900px;min-width:0} @media(max-width:900px){.cols{flex-direction:column}.rail{width:100%;border-right:none;border-bottom:1px solid var(--rule);padding-bottom:12px}}`.

pagelink: `display:block;width:100%;text-align:left;background:none;border:none;border-top:1px solid var(--rule);padding:6px 2px` hover color red. `.ptitle{display:block}` `.meta{color:var(--grey)}`.

bignum: `font-family:Georgia;font-size:44px;margin:8px 0`.

OK. Compose now. Also remember footer + credits.

Given the massive scope, some simplifications are acceptable as long as everything asked works. Let me write.

For the "checks panel" on tab 04, I'll render computeLint() rows into both the table and a details panel with desc + values.

Final: write answer.