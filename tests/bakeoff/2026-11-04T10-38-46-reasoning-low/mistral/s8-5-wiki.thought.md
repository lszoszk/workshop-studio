This is a huge task. The user wants a full app: a research wiki workspace with 5 tabs, pin verification, model calls via studio.ask, ingest stepper, lint, record/download. I need to write one complete HTML file, under ~1500 lines, offline, using window.WORKSHOP_DATA.wiki and .library, Chart.js available but maybe not needed (lean bar could be a simple div bar, not Chart.js — simpler).

Let me plan the architecture carefully but keep code manageable. This will be a large file. I must aim for completeness but within line budget. Let me design.

Key data structures:
- W = WORKSHOP_DATA.wiki; L = WORKSHOP_DATA.library.
- P = W.pages; D = L.records.
- maps: bySlug, byId.
- Per page precompute: bodyLinks, pins (regex), backlinks.
- norm(s) normalization.
- verify(pin) function.
- citeAs per document.
- registerOfDoc(id): find source page with sources exactly [id], else stub page with sources [id], else "?".

State: session counters {changes, calls, passages}, current tab, current page slug, ask state, ingest state, lint results, changes list.

Rendering: I'll build DOM with helper functions (el(tag, attrs, children)).

Markdown rendering for page bodies: need headings (#, ##, ###), bold **, italic *, bullets (- and numbered), [[slug]] links, pins, plain links [text](url), fenced ```contested blocks, paragraphs. Write a small renderer:

- Split body into lines; handle fenced blocks (```contested ... ```) → contested card; other fenced → pre.
- Headings: /^#{1,3} /.
- Lists: consecutive lines starting with "- " or "N. ".
- Paragraphs: other non-empty lines; inline render: pins first (regex global), then [[slug]], then [text](url), then **bold**, *italic*.

Inline rendering approach: tokenize with a combined regex for pins, wiki links, md links, bold, italic. Simpler: process pins first by splitting on pin regex, then within text segments process [[...]], [..](..), **..**, *..*.

Pin chip: a span containing the quote in quotation marks (rendered inline as part of sentence), then a chip button with label; clicking calls studio.openSource(id, page, quote). Chip shows register letter, verification status ("✓ verified" green / "⚠ not found" amber), and if page mark differs, "page says ✓/⚠". Expandable arrow: shows passage paragraph/page_label and first 300 chars + "Open the PDF page" button.

Wait — spec: "the app shows the quote itself, in quotation marks, where the pin stands, and after it a small chip: the label as a button". So inline: quote text then chip. Good.

Contested card: parse block lines: claim:, verdict:, note:, then position lines "+ | ..." split " | " into sign, register, pin, gloss, page-link. Lean bar: div with width %, labelled. Positions table with caption.

Tabs: role=tablist, buttons with role=tab, arrow key navigation, aria-selected. location.hash = slug opens page on tab 01.

Tab 01 PAGES: left rail 320px with filter input + big count + grouped list (by type: source, concept, entity, question). Main column: index rendered as a page when no page chosen, else the page. Page view: title, badges, tags, body rendered, Links out / Linked from / Sources sections, Copy page as markdown button.

Tab 02 ASK: textarea + label, Ask button, grey info box describing what will be sent, progress line + Stop, results: step1 chips of slugs with "Change pages" toggle, step2 answer in data-source="ai", pins verified, cannot_answer, count line by register, "File as a question page" button opening filing card with preview, tags input, File this page / Copy answer buttons.

Model calls: function askModel(prompt, opts) — increments calls counter, computes chars and passages in prompt (count passage objects? we can count occurrences of passage ids... simpler: we pass passages count explicitly). Show prompt size on screen. Parse JSON: try JSON.parse, else strip ```json fences. On failure show raw + Retry.

Tab 03 INGEST: list inbox docs with Ingest button. Stepper with 4 steps. Step 1: scope panel, table of batches, Start button; runs batches sequentially with progress + Stop. Step 2: takeaways table grows; failed box. Step 3: draft source page button, then draft changes to n pages (one call each). Step 4: review cards with Approve/Reject; then File the approved changes button.

This is a lot. I need to implement all of it but keep code tight. Given 1500-line limit, I'll write compact but readable code. Realistically this will be ~1300-1500 lines. Let me be efficient: use helper `h()` for element creation, template strings for HTML where safe (escape user/model text!). Important: escape HTML in all rendered text (model output especially). I'll write esc() and build DOM mostly via createElement to avoid injection; but for markdown rendering, building strings with esc() is fine.

Let me decide: render markdown to HTML string with escaping, then set innerHTML. Pins become chips with data attributes; attach event delegation on document for clicks on .pin-chip etc.

Event delegation: one click handler on document checking closest('[data-action]').

Actions: tab switching, page select, filter, copy page, pin chip open, pin expand, ask flow buttons, ingest buttons, approve/reject, file, lint, download, log toggle, tensions card links, change-pages toggles, stop buttons, retry.

Given complexity, I'll write functions per flow.

Let me now think about verify():

```js
function norm(s){
  return (s||'').normalize('NFKC')
    .replace(/[“”„]/g,'"').replace(/[‘’]/g,"'")
    .replace(/[–—]/g,'-')
    .replace(/\u00AD/g,'')
    .replace(/-\s+/g,'')
    .replace(/\s+/g,' ').trim();
}
```

Wait: "a hyphen followed by whitespace → ''" — replace(/-\s/g,'')? "decision- making" → "decisionmaking"? Hmm, "decision- making" = "decision-making" per spec. So hyphen followed by whitespace removed along with... "decision- making" → remove "- " → "decisionmaking"? That's not "decision-making". Actually removing the hyphen and the space gives "decisionmaking" — but they say equals "decision-making". Hmm: "decision- making" normalized: hyphen followed by whitespace → "" means remove the hyphen (and the whitespace collapses later). "decision- making" → "decision making"? No: removing "-" gives "decision making", then whitespace runs → one space → "decision making". And "decision-making" stays "decision-making". Those aren't equal. Unless they mean remove hyphen+space: "decision- making" → "decisionmaking" vs "decision-making" → "decision-making". Still not equal. Hmm, maybe they intend hyphen followed by whitespace → "-" (i.e., join). "decision- making" → "decision-making". Yes! Replace /-\s+/ with "-" gives "decision-making". That matches the stated equality. So: .replace(/-\s+/g,'-'). Good.

verify(pin): pin = {label, id, page, quote, mark}. 
- if !quote → false reason "no quote".
- doc = byId[id]; if !doc → false "unknown document".
- if doc.status === 'inbox' → false "document still in the inbox".
- find passage x with x.page === page. If none → false.
- fragments = quote.split(/…|\.\.\./); search in norm(x.text) sequentially.
- label check: if x.paragraph != null → label must contain "para. " + x.paragraph; else label contains "p. " + x.page_label.

Note: label like "A/81/351, para. 16". Contains check fine.

Cite-as: for each doc, collect labels of pins to it, take text before ", para." or ", p." — most frequent. Implement: for pins with id, label.split(/, (?:para|p)\./)[0]. Count. Fallback symbol or author+year.

Register of doc: find page with type 'source' (or any) whose frontmatter.sources deep-equals [id]; else stub page (status 'stub') with sources [id]; else '?'. Spec: "the register of the source page whose sources is exactly [that id], else of the stub page with that sources". Implement: pages.find(p => p.frontmatter.sources.length===1 && p.frontmatter.sources[0]===id && p.type==='source') || pages.find(p => sources==[id] && status==='stub') || any with sources [id]. Return its register array joined, or '?'.

Register names: a treaty law, b General Comments, c UN/agency/soft-law reports, d NHRI, e civil society, f scholarship.

Lint checks (tab 04): compute list:
1. pins found vs index stated count.
2. verified vs found.
3. ✓ marks that fail.
4. dangling links.
5. orphans.
6. sources differ from pinned docs.
7. pages with no pins.
8. links not reciprocated (frontmatter.links vs body links differ — spec says "links not reciprocated"; I'll check frontmatter.links entries not in bodyLinks and body links not in frontmatter.links? The data says they differ on 5 entries; check: links in frontmatter not reciprocated in body? I'll report pages where frontmatter.links set ≠ bodyLinks set).
9. pages missing from index / index lines without page.
10. index ✓N differs from computed.
11. contested cards vs tensions card: entries.
12. stub pages.
13. pins to inbox documents.

Each: {name, count, pages, pass}.

Index parsing: index lines like "- [[slug]] — one-liner · (letters) · ✓N". Parse with regex /- \[\[([^\]]+)\]\].*?✓([\d,]+)/.

Tensions parsing: entries starting "### "; card: [[slug]].

Contested blocks in pages: find fenced ```contested blocks; claim slug for tensions entry: "slug-of-claim" — for matching contested cards to tensions entries, match card: [[page]] where page is the page containing the block.

Now the ASK flow:

State ask = {question, step, slugs, answer, ...}.

Call 1 prompt: index + question → ask for JSON {pages:[slugs]}. Parse, filter to existing, max 5. Show chips; "Change pages" reveals checkboxes of all pages (maybe grouped) to tick others.

Call 2 prompt: bodies of chosen pages + question + instructions (pin syntax, register naming, ≤350 words) → JSON {title, answer, cannot_answer}. Render answer as markdown (with pins) inside data-source="ai". Verify each pin in answer: accepted if same pin:id#pPAGE with same quote exists in a sent page's body AND verify true; else struck through with "not on the pages sent". Count verified pins by register.

File as question page: build page object preview; tags input; File this page disabled until all pins verify; adds to pages, index line, log entry; session changes++.

INGEST flow: This is the biggest. State ingest = {docId, step, batches, batchResults, takeaways, failed, drafts: {source, touched: {slug: card}}, decisions: {}, filed}.

Step 1: compute batches (chunks of 25). Table of batches with paragraph ranges and PDF pages. Start button: for each batch, call model with passages as {id,page,paragraph,text} + index + instructions → {takeaways:[...]}. Progress line "batch 2 of 4 · 50 of 100 passages have left the browser". Stop button sets flag. Passages counter += batch size each call. Calls counter++.

For each takeaway: find passage by id (takeaway.passage is passage id like "A/HRC/57/61#12"? The model returns "passage" — we sent passages with id field; model returns passage id). Build pin: citeAs + ", para. X" or ", p. label" + pin syntax with quote (escape straight quotes to curly). verify. If pass → takeaways list with pin; else failed list with nearest passage computed (longest common consecutive word run between norm(quote) and each passage on that page). Keep pages slugs filtered to existing + allow up to 2 new slugs per ingest.

Step 2 table grows as batches return: claim, quote, passage (paragraph + PDF page), pages chips, verification.

Step 3: "Draft the source page (1 call)": prompt with verified takeaways + pins, doc metadata, schema anatomy → {one_liner, body, touches}. Re-verify pins in body. Build frontmatter. Change card: new page (or edit of stub? The stub a-hrc-57-61 exists as entity page; spec says "the stub a-hrc-57-61 is always among them, rewritten" — the source page draft is a new source page; the stub gets edited among touched pages). Then "Draft the changes to n pages (n calls)": for each touched slug (existing pages + new slugs + stub), call with page body + relevant takeaways → {edits:[{after, markdown}], contested}. Insert markdown at end of named heading section; re-verify pins; update links/sources. Produce change card with new body.

Step 4: review each change card: show page with inserted paragraphs highlighted pale yellow, rest grey; pins as chips; counts of paragraphs inserted and pins added (verified/not); Approve/Reject buttons; "change 3 of 9". After all decisions, "File the approved changes" writes: replace/add pages, updated today, index updated, log entry, tensions entry for new contested, doc status → ingested, lint re-run, changes counter.

Highlighting inserted paragraphs: mark inserted markdown blocks. When inserting, wrap inserted segments with a marker? For display, I can diff: compare old body lines vs new body lines; lines present in new but not old → inserted. Simple approach: split both into lines, mark lines in new not in old (by set). Good enough.

Given the enormity, I'll implement it as completely as I can but keep each part compact.

Tab 05 RECORD: log rendered newest first with switch; each entry collapsible (<details>); tensions register rendered, card: links open page on tab 01; method note; Download the wiki button (JSON blob); if changes, second button markdown of changed pages.

Header counters: changes, calls, passages — update via renderCounters().

Footer line.

Hash routing: on load, if location.hash matches a slug, open tab 01 with that page. When selecting a page, set location.hash = slug. Listen hashchange.

Escape key stops running step: set stopFlag.

aria-live regions: progress lines.

OK, line budget: this will be tight. Let me write it now, aiming ~1400 lines. I'll write dense code.

Let me draft the HTML skeleton:

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Research wiki: neurotechnology in the administration of justice</title>
<style> ... </style>
</head>
<body>
<header> ... </header>
<nav role="tablist" id="tabs"> 5 buttons </nav>
<main>
 <section id="tab-01" role="tabpanel">...</section>
 ... etc
</main>
<footer>...</footer>
<script> ... </script>
</body>
</html>
```

CSS: paper #f4f0e8, ink #1d1b18, rules #d9d2c3, accent #9b2335. Fonts as specified. [hidden]{display:none!important}. Focus ring red. Chips, cards, tables, lean bar, pale yellow inserted (#fbf3d0-ish with left border), grey rest.

Now JS. Let me write it carefully.

```js
const W = WORKSHOP_DATA.wiki, L = WORKSHOP_DATA.library;
const P = W.pages, D = L.records;
const bySlug = {}, byId = {};
P.forEach(p=>bySlug[p.slug]=p); D.forEach(d=>byId[d.id]=d);
const REG_NAMES = {a:'treaty law',b:'General Comments',c:'UN, agency and soft-law reports',d:'national human rights institution',e:'civil society',f:'scholarship'};
const REG_W = {a:5,b:4,c:3,d:2,e:1,f:0.5};
const PIN_RE = /\[([^\]]+)\]\(pin:([^#\s)]+)#p(\d+)(?: "([^"]*)")?\) ?(✓|⚠)/g;
const LINK_RE = /\[\[([^\]|#]+)\]\]/g;
```

Precompute per page:

```js
P.forEach(p=>{
  p._links = [...p.body.matchAll(LINK_RE)].map(m=>m[1]);
  p._pins = [...p.body.matchAll(PIN_RE)].map(m=>({label:m[1],id:m[2],page:+m[3],quote:m[4]||'',mark:m[5],raw:m[0]}));
});
const backlinks = {}; P.forEach(p=>p._links.forEach(s=>{(backlinks[s]=backlinks[s]||[]).push(p.slug)}));
```

norm, verify:

```js
function norm(s){return (s??'').normalize('NFKC').replace(/[“”„]/g,'"').replace(/[‘’]/g,"'").replace(/[–—]/g,'-').replace(/\u00AD/g,'').replace(/-\s+/g,'-').replace(/\s+/g,' ').trim();}
function verify(pin){
  if(!pin.quote) return {ok:false,reason:'no quote in the pin'};
  const d = byId[pin.id];
  if(!d) return {ok:false,reason:'unknown document'};
  if(d.status==='inbox') return {ok:false,reason:'document is still in the inbox'};
  const x = d.passages.find(p=>p.page===pin.page);
  if(!x) return {ok:false,reason:'no passage starts on PDF page '+pin.page};
  const frags = pin.quote.split(/…|\.\.\./).map(norm).filter(Boolean);
  const t = norm(x.text); let pos=0;
  for(const f of frags){ const i = t.indexOf(f,pos); if(i<0) return {ok:false,reason:'quote not found on that page'}; pos=i+f.length; }
  if(x.paragraph!=null){ if(!pin.label.includes('para. '+x.paragraph)) return {ok:false,reason:'label does not match paragraph '+x.paragraph}; }
  else { if(!pin.label.includes('p. '+x.page_label)) return {ok:false,reason:'label does not match page '+x.page_label}; }
  return {ok:true,passage:x};
}
```

citeAs:

```js
const citeAs = {};
D.forEach(d=>{
  const counts={};
  P.forEach(p=>p._pins.forEach(pin=>{ if(pin.id===d.id){ const base=pin.label.split(/, (?:para|p)\./)[0]; counts[base]=(counts[base]||0)+1; }}));
  const best=Object.entries(counts).sort((a,b)=>b[1]-a[1])[0];
  citeAs[d.id]= best?best[0] : (d.symbol || (d.author+' '+d.year));
});
```

registerOfDoc:

```js
function registerOfDoc(id){
  const src = P.find(p=>p.type==='source' && p.frontmatter.sources.length===1 && p.frontmatter.sources[0]===id);
  const pg = src || P.find(p=>p.frontmatter.status==='stub' && p.frontmatter.sources.length===1 && p.frontmatter.sources[0]===id) || P.find(p=>p.frontmatter.sources.length===1&&p.frontmatter.sources[0]===id);
  return pg ? (pg.frontmatter.register||[]).join('') : '?';
}
```

newPin(docId, passage, quote):

```js
function escQuote(q){return q.replace(/"/g,'”');} // straight double quotes become curly
function makePin(id,x,quote){
  const label = citeAs[id]+(x.paragraph!=null? ', para. '+x.paragraph : ', p. '+x.page_label);
  return '['+label+'](pin:'+id+'#p'+x.page+' "'+escQuote(quote)+'") ✓';
}
```

Wait: escQuote should turn `"` into “ or ” — spec: "straight double quotes inside the quote become “ ” first". Replace with “” pair? Just replace each `"` with `”`? I'll replace with '”'. Fine.

Session state:

```js
const S = { changes:0, calls:0, passages:0, tab:'01', page:null, stop:false, changesList:[], lint:null, ask:{}, ingest:{} };
```

Counters render into header.

Model call wrapper:

```js
async function askModel(prompt, {passages=0, label=''} = {}){
  S.calls++; S.passages+=passages; renderCounters();
  // show size
  let raw;
  try{ raw = await studio.ask(prompt,{json:true}); }
  catch(e){ return {error:String(e), raw:''}; }
  let txt = raw.trim();
  let json=null;
  try{ json=JSON.parse(txt); }catch(e){
    const m = txt.match(/```(?:json)?\s*([\s\S]*?)```/);
    if(m){ try{ json=JSON.parse(m[1]); }catch(e2){} }
  }
  return {raw:txt, json};
}
```

Prompt builders include pin syntax note and "quote only words that stand in the passages given; the code will check".

Markdown renderer. Let me write renderMd(body, opts) returning HTML string. Handle:

- Split into lines. Iterate; fenced blocks: line starts with ``` → collect until closing ```; if info string 'contested' → renderContested(block); else <pre>.
- Headings: /^(#{1,3})\s+(.*)$/.
- Lists: lines starting '- ' → ul; /^\d+\.\s/ → ol. Group consecutive.
- Blank line separates paragraphs.
- Else paragraph <p> with inline().

inline(text): must handle pins, [[links]], [text](url), **bold**, *italic*. Order: pins first (they contain brackets and parens that would confuse link regex). Approach: use one combined regex:

```js
const INLINE_RE = /\[([^\]]+)\]\(pin:([^#\s)]+)#p(\d+)(?: "([^"]*)")?\) ?(✓|⚠)|\[\[([^\]|#]+)\]\]|\[([^\]]+)\]\(([^)\s]+)\)|(\*\*[^*]+\*\*)|(\*[^*]+\*)/g;
```

Replace with callback building HTML. For pin: quote in quotes + chip. Chip HTML:

```html
<span class="pin"><span class="pin-quote">“QUOTE”</span><button class="chip pin-chip" data-action="pin" data-id data-page data-quote data-label data-mark>LABEL</button><button class="chip pin-more" data-action="pinmore">▸</button><span class="pin-verdict ok">✓ verified</span> ...</span>
```

Hmm, spec: chip contains label as button that opens PDF; register letter; verification words; expand arrow shows passage preview + Open PDF page. Let me structure:

```html
<span class="pin">
  <span class="pin-quote">“…”</span>
  <span class="chip pin-chip" data-action="pin-open" ...>label</span>
  <span class="chip reg">c</span>
  <span class="verdict ok">✓ verified</span>
  <button class="chip pin-toggle" data-action="pin-toggle" aria-expanded="false">details</button>
  <span class="pin-detail" hidden> paragraph/page_label, first 300 chars, <button data-action="pin-open">Open the PDF page</button></span>
</span>
```

Verification computed at render time via verify(pin). If pin.mark differs from computed ok, add "page says ✓/⚠".

For AI answers, pins may not verify — same rendering, verdict shows not found, and if pin not on sent pages, wrap in <s> with note. I'll pass opts {ai:true, sentPins:Set of "id#p|quote"}.

Contested card render:

```js
function parseContested(block){
  const lines = block.split('\n');
  const o={positions:[]};
  for(const ln of lines){
    if(ln.startsWith('claim:')) o.claim=ln.slice(6).trim();
    else if(ln.startsWith('verdict:')) o.verdict=ln.slice(8).trim();
    else if(ln.startsWith('note:')) o.note=ln.slice(5).trim();
    else if(/^[+~\-]\s*\|/.test(ln)){
      const parts=ln.split('|').map(s=>s.trim());
      o.positions.push({sign:parts[0], register:parts[1], pin:parts[2], gloss:parts[3], page:parts[4]});
    }
  }
  return o;
}
```

Position pin is itself a pin markdown `[label](pin:...) ✓` — render inline within table cell.

Lean: weights; support% = (Σ+ + 0.5Σ~) / Σall.

Verdict words: map 'leans-contest'→'leans contest', etc. Just replace '-' with ' '.

Tensions register parse: split on /^### /m; each entry has card: [[slug]].

Index parse: lines with [[slug]] and ✓N.

Now tab 01 rendering:

```js
function renderTab01(){
  const list = filtered pages grouped by type order [source, concept, entity, question];
  ...
}
```

Filter input: matches title, tags, slug (lowercase includes).

Page view renderPage(slug): builds HTML: title h2, badges, tags, body via renderMd, then sections Links out / Linked from / Sources, copy button.

Sources section: for each id in frontmatter.sources: doc = byId[id]; show short_title, kind, year, url link, "inbox" tag if status inbox.

Copy page as markdown: frontmatter YAML:

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

Clipboard: navigator.clipboard.writeText — offline sandbox, clipboard may fail; wrap try/catch, fallback show in a textarea? Just try/catch and alert-ish message line. I'll attempt clipboard and show "copied" note; on failure select a temp textarea. Keep simple: try clipboard, catch → prompt? No prompt. Show the markdown in a <details> maybe. I'll do: try clipboard; on failure, put text into a temporary textarea and execCommand('copy'). Fine.

Tab switching: show/hide sections, update tab classes, aria-selected, and "running" mark for ingest tab when running.

Hash: function openPage(slug){ S.tab='01'; S.page=slug; location.hash=slug; renderAll(); } On hashchange: if slug exists → openPage without re-setting hash (guard).

Tab 02 ASK:

Elements: label + textarea#ask-q, button#ask-btn "Ask the wiki", grey box #ask-info describing steps, progress div aria-live, stop button, results container.

Flow:

```js
async function runAsk(){
  const q = askQ.value.trim(); if(!q) return;
  askBtn disabled; 
  info: "Step 1 will send: the index (n chars) and your question (n chars). No library passages leave the browser."
  const r1 = await askModel(indexPrompt(q), {});
  if(!r1.json || !r1.json.pages) → show raw + Retry.
  slugs = r1.json.pages.filter(s=>bySlug[s]).slice(0,5);
  show chips + "Change pages" link toggling a checkbox list of all pages (checked = chosen).
  info: "Step 2 will send: 5 pages, N characters; 0 library passages have left the browser."
  const r2 = await askModel(bodyPrompt(chosen, q));
  render answer.
}
```

Answer rendering: renderMd(answer, {ai:true, sentPins}) inside div data-source="ai". sentPins = set of pin raw strings from sent pages' bodies. For each pin in answer: key = id+'#p'+page+'|'+quote; if !sentPins.has(key) → struck through + "not on the pages sent". Verify via verify(). Count by register over verified pins.

File as question page: button opens card: preview (title input? spec: slug from title — title from r2.json.title; slug kebab unique), tags input, preview of body structure, File this page (disabled until all pins verify — check every pin in answer verifies AND is on sent pages), Copy answer.

File: build page object:

```js
const slug = uniqueSlug(kebab(title));
const page = {slug, type:'question', title, frontmatter:{title,type:'question',tags,register: registers of pinned docs, status:'draft', updated: today, links: slugs in answer, sources: pinned doc ids}, body: built};
P.push(page); bySlug[slug]=page; recompute _links/_pins; index line appended under Questions; log entry; S.changes++; S.changesList.push(...); renderAll; message "Filed".
```

Body built:

```
# title

**Short answer.** ...? 
```

Spec: body = "# title", "**Short answer.**", "## Reasoning" (the answer), "## What the library cannot answer", "## Related". Short answer — maybe first sentence of answer or the title... I'll use a short answer = answer's first sentence? Simpler: "**Short answer.** See Reasoning below; filed from an Ask answer." Hmm, better: use cannot_answer? I'll put the answer's first line/sentence as short answer. Actually simplest: "**Short answer.** " + first sentence of answer. OK.

Tab 03 INGEST:

```js
function inboxDocs(){ return D.filter(d=>d.status==='inbox'); }
```

Render: for each inbox doc a button "Ingest A/HRC/57/61". Clicking starts ingest state for that doc and shows stepper.

Stepper HTML: steps list with running line "calls so far m · passages sent k" (uses S counters). Step panels:

Step 1 panel: text "All 100 passages will be sent, in batches of 25 (4 calls), 61,737 characters; nothing is held back." Table of batches: batch #, paragraph range (first–last paragraph or passage ids), PDF pages range. Start button.

runBatches: for each batch i: if S.stop break; progress "batch i of n · X of 100 passages have left the browser"; prompt:

```
You are ingesting <cite-as> (<doc title>) into a research wiki. Index:
<index>
Passages (verbatim, from the PDF):
JSON array of {id,page,paragraph,section,text}
Return JSON {takeaways:[{claim, quote, passage, pages}]}, at most 10. quote 8 to 40 words copied verbatim from that one passage (passage = its id). pages = slugs from the index the claim bears on.
Pin syntax: [label](pin:id#pPAGE "quote") ✓ — quote only words that stand in the passages given; the code will check.
```

passages count = batch.length. Parse json; for each takeaway: find passage by id among batch (if not among sent → drop & count); build pin via makePin; verify; if ok → takeaway {claim, quote, passage, pages (filtered to existing slugs + newSlug allowance), pin, verified:true}; else failed.push({claim, quote, passageId, nearest}).

Nearest passage: among doc.passages with page === pin page? Spec: "the nearest passage on that page" — passage on that page sharing longest run of consecutive normalised words with the quote. Compute: for each passage x on that page, compute longest common substring of words? "longest run of consecutive normalised words" — longest common contiguous word sequence between norm(quote) words and norm(x.text) words. Implement simple: words arrays, find max run. O(n*m) fine for small.

Step 2 panel: table FIG.01 takeaways: claim, quote, passage (para + PDF page), pages chips, verification words. Box "Could not verify: n" listing failed with Open PDF page button (studio.openSource(id,page,quote)).

Step 3: button "Draft the source page (1 call)" → prompt with verified takeaways (claim + pin), cite-as, doc metadata, schema anatomy list → {one_liner, body, touches}. Re-verify pins in body (parse with PIN_RE, verify each; count verified/not). Build frontmatter: type source, register from stub, sources [id], links from body links, tags from touched slugs. Card: new page. Then button "Draft the changes to n pages (n calls)": touched = union of takeaway pages (existing) + new slugs (max 2) + stub slug if doc has stub. For each slug: prompt page body + takeaways whose pages include slug → {edits:[{after,markdown}], contested}. Insert each markdown at end of section of heading `after` (find heading line in body, insert after that section i.e., before next heading of same or higher level, or at end); if heading not found → append at end with note. Re-verify pins in new body. Update links both ways + sources add doc id. Card: edited page with inserted paragraphs count and pins added.

Insertion function:

```js
function insertAfterHeading(body, heading, md){
  const lines = body.split('\n');
  const idx = lines.findIndex(l=>l.replace(/^#+\s*/,'').trim().toLowerCase()===heading.replace(/^#+\s*/,'').trim().toLowerCase());
  if(idx<0) return {body: body + '\n\n' + md + '\n\n<!-- inserted at end: heading not found: '+heading+' -->', inserted:[md]};
  // find end of section: next line starting with # (any level) after idx
  let end = lines.length;
  for(let i=idx+1;i<lines.length;i++){ if(/^#{1,6}\s/.test(lines[i])){ end=i; break; } }
  const inserted = md;
  lines.splice(end,0,'',md,'');
  return {body: lines.join('\n'), inserted:[md]};
}
```

Hmm heading match: `after` is "an existing heading or 'end'". Match by text ignoring #'s.

Step 4: review cards. Each change card: fieldset/legend, title+type, "new page"/"edited", counts (paragraphs inserted = inserted markdown blocks count; pins added = pins in new body not in old body, verified/not counts in words), rendered page with inserted paragraphs highlighted. Implementation of highlight: when rendering a change card, pass opts {highlight: set of inserted md strings}; in renderMd paragraph rendering, if paragraph text (raw line group) is in highlight set → class "inserted", else class "dimmed"? Spec: "every inserted paragraph on a pale yellow background and the rest in grey". So in change card rendering, non-inserted content gets grey. I'll pass opts.cls to renderMd: wrap each block element with class. Simpler: render normally, then post-process: for change cards, add class to container 'diff' and mark inserted blocks. I'll implement renderMd(body, opts) where opts.markInserted = array of strings; when emitting a <p>/<li>/heading, check if its raw source is included in any inserted string → add class 'ins', else 'old'. Approximate: check if inserted.some(m=>m.includes(rawLine)). Good enough.

Approve/Reject: decisions[slug]='approved'/'rejected'; line "change i of n"; after all → enable "File the approved changes".

File: for each approved change: if new page → push to P, bySlug; else replace page body/frontmatter (keep slug, set updated today, merge links/sources). Update index: rebuild? Spec gives index line format; simplest: regenerate index lines for changed pages: replace existing line for slug or insert under type group; recompute first line counts. I'll implement updateIndex(): rebuild the whole index from pages? The index has a first line with counts and group structure. Safer: rebuild index entirely from pages in a canonical format matching: first line "- N pages (n sources, ...) · N pins" hmm I don't know exact original format. Let me just do targeted updates: for each changed page, if a line `- [[slug]]` exists, replace it with new line (recompute ✓N); else insert after the last line of its type group (or before end). And update the first line's pin count. To find first line: index.split('\n')[0] contains "pins" — replace the number via regex /(\d[\d,]*) pins/ with new total. Also page counts if new page added. I'll do regex replace on first line for pins count and pages count if present. Keep it simple and note "How this is computed".

Log entry: append "## [today] ingest | symbol: short_title\n\n" + body text per spec: "Read n passages (cite-as, register (x)). Wrote [[slug]]. N pins in all; besides its own page, pinned on k pages: [[…]]. Rejected: [[…]]."

Tensions entry for new contested card: append ### entry.

Doc status: byId[id].status='ingested' (in memory).

Lint re-run: run lint, show before/after.

S.changes++ per filed ingest? "Changes this session: n" — count filed pages + filed question pages. I'll increment per approved change filed and per question page filed.

Tab 04 CHECK: big number "n of n pins verified by this page", "n lint checks need a look", Lint now button, table of checks with caption, each row: check name, count, "0 · pass" or "n · check", pages links. Checks panel (static explanation list) open by default.

Lint computation function computeLint() returns array of {name, count, pass, pages:[slugs], detail}.

Checks:
1. Pins found vs index stated: stated = parse first line /(\d[\d,]*) pins/; found = total pins; pass if equal.
2. Verified pins: count not verified → pages.
3. ✓ marks that fail: pins with mark ✓ but !verify.ok.
4. Dangling links: bodyLinks not in bySlug.
5. Orphans: pages not linked from any body and not... orphan = no backlinks. (All pages have backlinks per data, but compute.)
6. sources differ from pinned docs: set(frontmatter.sources) vs set(pin ids).
7. Pages with no pins.
8. links not reciprocated: frontmatter.links vs bodyLinks symmetric difference.
9. Index structure: pages missing from index; index slugs without page.
10. Index ✓N differs from computed verified count per page.
11. Contested cards vs tensions card: entries: pages with contested blocks whose slug not in tensions card list, and reverse.
12. Stub pages (status stub).
13. Pins to inbox documents.

Tab 05 RECORD: log newest first (checkbox switch), entries as <details> with summary "## [date] op | subject" — parse log entries by /^## /m; summary = the heading line; content = rest rendered as markdown (simple). Tensions register rendered: entries with card: [[slug]] link (data-action open-page). Method note + source line. Download buttons.

Download JSON: Blob of {pages, index, log, tensions, schema, count, changes, library_status} → a.download = 'wiki-'+date+'.json'.

Changed pages markdown: pages in S.changesList → file with --- separators.

OK. Also "running" mark on tab 03 while ingest running: set S.ingest.running true; tab label "03 INGEST · running".

Escape key: S.stop=true.

aria-live: progress elements get aria-live="polite".

Focus first tab on load.

Now, clickables count: fine.

Let me also handle "Change pages" in ask: a button toggling a panel with checkboxes for all 40 pages; chosen set; then re-run step 2? Spec: "shown as chips with a Change pages link that lets you tick others" — after changing, presumably re-run call 2 with new set. I'll make "Apply pages" re-run step 2.

Time to write the code. I'll aim for clarity and compactness. Let me write the full file now.

Also note: studio.openSource(id, page, quote) — call for every pin chip click and "Open the PDF page".

Let me write CSS:

```css
:root{--paper:#f4f0e8;--ink:#1d1b18;--rule:#d9d2c3;--red:#9b2335;--green:#2e6b3f;--amber:#9a6a00;--grey:#6b675f;}
*{box-sizing:border-box}
[hidden]{display:none!important}
body{margin:0;background:var(--paper);color:var(--ink);font:16px/1.55 -apple-system,'Segoe UI',Roboto,Helvetica,Arial,sans-serif}
.mono{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:11.5px;letter-spacing:.08em;text-transform:uppercase}
header{padding:18px 24px 10px;border-bottom:1px solid var(--rule)}
...
```

Serif: Georgia,'Times New Roman',serif.

Tabs: buttons mono uppercase, active red with underline.

Layout tab01: display:flex; aside width 320px; main flex 1 max-width 900px.

Chips: border 1px solid rule, radius 999px, padding 1px 8px, mono 11px, background transparent; hover border red.

Verdict colors: .ok{color:var(--green)} .warn{color:var(--amber)} .bad{color:var(--red)}.

Inserted: background:#f7ecc9;border-left:3px solid var(--red); .old{color:#8a857a} within .diff context.

Lean bar: .lean{height:10px;background:var(--rule)} .lean>div{height:100%;background:var(--red)}.

Tables: width 100%, border-collapse, th mono small, td border-top rule, numbers right.

Focus: :focus-visible{outline:3px solid var(--red);outline-offset:2px}.

Buttons: .btn{border:1px solid var(--ink);background:transparent;padding:6px 12px;font:inherit;cursor:pointer} .btn.primary{background:var(--red);color:#fff;border-color:var(--red)}.

Now writing everything. I'll be careful with escaping: esc(s) for HTML.

renderMd implementation:

```js
function esc(s){return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');}
const INLINE_RE = /\[([^\]]+)\]\(pin:([^#\s)]+)#p(\d+)(?: "([^"]*)")?\) ?(✓|⚠)|\[\[([^\]|#]+)\]\]|\[([^\]]+)\]\(([^\s)]+)\)|(\*\*[^*]+\*\*)|(\*[^*\n]+\*)/g;
function inline(s, opts){
  return s.replace(INLINE_RE,(m,label,id,page,quote,mark,wslug,lt,lu,bold,ital)=>{
    if(label!==undefined){ return pinHtml({label,id,page:+page,quote:quote||'',mark},opts); }
    if(wslug!==undefined){ const t=bySlug[wslug]; return t? '<a href="#'+esc(wslug)+'" data-action="open-page" data-slug="'+esc(wslug)+'">'+esc(wslug)+'</a>' : '<span class="bad">'+esc(wslug)+' (no page)</span>'; }
    if(lt!==undefined){ return '<a href="'+esc(lu)+'" target="_blank" rel="noopener">'+esc(lt)+'</a>'; }
    if(bold) return '<strong>'+esc(bold.slice(2,-2))+'</strong>';
    if(ital) return '<em>'+esc(ital.slice(1,-1))+'</em>';
    return m;
  });
}
```

Careful: bold regex `\*\*[^*]+\*\*` — text may contain multiple; fine.

pinHtml(pin, opts):

```js
function pinHtml(pin, opts){
  const v = verify(pin);
  const reg = registerOfDoc(pin.id);
  const doc = byId[pin.id];
  const sent = opts && opts.sentPins ? opts.sentPins.has(pin.id+'#p'+pin.page+'|'+pin.quote) : true;
  const key = pin.id+'#p'+pin.page+'|'+pin.quote;
  let cls='pin', note='';
  if(opts&&opts.ai){ if(!sent){ cls+=' struck'; note=' <span class="bad">not on the pages sent</span>'; } }
  const markNote = (pin.mark==='✓')!==v.ok ? ' <span class="warn">page says '+pin.mark+'</span>' : '';
  const verdict = v.ok ? '<span class="ok">✓ verified</span>' : '<span class="warn">⚠ not found'+(v.reason?' — '+esc(v.reason):'')+'</span>';
  const detail = v.ok ? esc('para. '+v.passage.paragraph ?? ...) ...
}
```

Detail content: passage paragraph or page_label + first 300 chars of text + Open PDF page button.

```js
  const det = v.ok ? (v.passage.paragraph!=null? 'para. '+esc(v.passage.paragraph) : 'p. '+esc(v.passage.page_label)) + ' · ' + esc(v.passage.text.slice(0,300)) + (v.passage.text.length>300?'…':'') : esc(v.reason||'');
  return '<span class="'+cls+'"><span class="pin-quote">“'+esc(pin.quote)+'”</span> '+
    '<button class="chip" data-action="pin-open" data-id="'+esc(pin.id)+'" data-page="'+pin.page+'" data-quote="'+esc(pin.quote)+'" title="Open the PDF at this page with the quote marked">'+esc(pin.label)+'</button> '+
    '<span class="chip reg" title="register">'+esc(reg)+'</span> '+verdict+markNote+note+' '+
    '<button class="chip" data-action="pin-toggle" aria-expanded="false">details</button>'+
    '<span class="pin-detail" hidden>'+det+' <button class="chip" data-action="pin-open" data-id="'+esc(pin.id)+'" data-page="'+pin.page+'" data-quote="'+esc(pin.quote)+'">Open the PDF page</button></span></span>';
```

Note: quote in data-quote attribute — esc handles quotes. Good.

renderMd:

```js
function renderMd(body, opts){
  opts=opts||{};
  const lines = body.split('\n');
  let html='', i=0, para=[];
  const flush=()=>{ if(para.length){ html+='<p>'+inline(para.join(' '),opts)+'</p>'; para=[]; } };
  const isIns = raw => opts.inserted && opts.inserted.some(m=>m.includes(raw));
  while(i<lines.length){
    const ln=lines[i];
    if(ln.trim().startsWith('```')){
      flush();
      const info=ln.trim().slice(3);
      const buf=[]; i++;
      while(i<lines.length && !lines[i].trim().startsWith('```')){ buf.push(lines[i]); i++; }
      i++;
      if(info==='contested') html+=contestedHtml(buf.join('\n'), opts);
      else html+='<pre>'+esc(buf.join('\n'))+'</pre>';
      continue;
    }
    const h=ln.match(/^(#{1,6})\s+(.*)$/);
    if(h){ flush(); const lvl=Math.min(h[1].length+1,6); const cls=isIns(ln)?' class="ins"':' class="old"'; html+='<h'+lvl+cls+'>'+inline(h[2],opts)+'</h'+lvl+'>'; i++; continue; }
    if(/^\s*-\s+/.test(ln)){ flush(); let ul=''; while(i<lines.length && /^\s*-\s+/.test(lines[i])){ const it=lines[i].replace(/^\s*-\s+/,''); ul+='<li'+(isIns(it)?' class="ins"':' class="old"')+'>'+inline(it,opts)+'</li>'; i++; } html+='<ul>'+ul+'</ul>'; continue; }
    if(/^\s*\d+\.\s+/.test(ln)){ flush(); let ol=''; while(i<lines.length && /^\s*\d+\.\s+/.test(lines[i])){ const it=lines[i].replace(/^\s*\d+\.\s+/,''); ol+='<li'+(isIns(it)?' class="ins"':' class="old"')+'>'+inline(it,opts)+'</li>'; i++; } html+='<ol>'+ol+'</ol>'; continue; }
    if(ln.trim()===''){ flush(); i++; continue; }
    para.push(ln.trim()); i++;
  }
  flush();
  return html;
}
```

Hmm the class="old" on everything when opts.inserted set — only in diff view. When opts.inserted undefined, no class. Adjust: cls = opts.inserted ? (isIns? ' class="ins"' : ' class="old"') : ''. Let me handle via helper.

contestedHtml(block, opts):

```js
function contestedHtml(block, opts){
  const c = parseContested(block);
  const verdict = c.verdict.replace(/-/g,' ');
  let wsum=0, wsup=0;
  c.positions.forEach(p=>{ const w=REG_W[p.register]??0; wsum+=w; if(p.sign==='+') wsup+=w; else if(p.sign==='~') wsup+=w/2; });
  const pct = wsum? Math.round(100*wsup/wsum) : 0;
  let rows = c.positions.map(p=>'<tr><td>'+(p.sign==='+'?'supports':p.sign==='-'?'contests':'mixed')+'</td><td class="mono">'+esc(p.register)+'</td><td>'+inline(p.pin,opts)+'</td><td>'+esc(p.gloss)+'</td><td>'+(p.page?inline(p.page,opts):'')+'</td></tr>').join('');
  // tensions link
  const inTensions = tensionsCards.has(currentPageSlug) — hmm need page slug; pass opts.pageSlug.
  ...
  return '<section class="contested"><h3>'+esc(c.claim)+'</h3>'+
   '<p class="verdict">'+esc(verdict)+'</p>'+
   (c.note?'<p>'+esc(c.note)+'</p>':'')+
   '<div class="lean-wrap"><div class="mono fig">FIG.01 · lean bar — descriptive: support '+pct+'% of weighted positions (weights a 5 · b 4 · c 3 · d 2 · e 1 · f ½); the verdict is the answer</div>'+
   '<div class="lean"><div style="width:'+pct+'%"></div></div></div>'+
   '<table><caption>Positions in this contested block</caption><thead><tr><th scope="col">sign</th><th scope="col">register</th><th scope="col">pin</th><th scope="col">gloss</th><th scope="col">page</th></tr></thead><tbody>'+rows+'</tbody></table>'+
   (tensionLink)+'</section>';
}
```

tensionsCards: set of slugs named in tensions `card: [[slug]]`.

Now the main render functions. Given size, I'll render tabs lazily: renderTab01() on tab switch/page change; others rendered on switch too (cheap enough) or once.

Let me now write the whole thing. I'll try to keep it organized. Also header:

```html
<header>
 <div class="mono">WIKI · neurotechnology and justice</div>
 <h1>Research wiki: neurotechnology in the administration of justice</h1>
 <div class="meta" id="hdr-meta"></div>
 <div class="hdr-right">
   <div class="mono" id="hdr-counters"></div>
   <div class="mono dim">This page has no storage: changes live in it until you download them (tab 05)</div>
 </div>
</header>
```

Meta line: `${P.length} pages (${n} sources, ...) · ${totalPins} pins, ${verified} verified by this page · ${D.length} documents, ${inbox} in the inbox · built ${W.built}`.

Counters: `Changes this session: n · Calls to the model: m · Passages that left the browser: k`.

Footer: `${W.source} · built ${W.built} · Counting, matching and verification are done by this page's code; the model is called only when you press Ask, Ingest or a retry button.`

Now write JS flows in detail.

Ask flow code:

```js
const ask = {q:'', step:0, slugs:[], all:[], answer:null, raw:null, err:null, sentPins:new Set(), regCounts:{}, filing:false, tags:''};
```

Elements in tab 02 static HTML with ids; JS wires.

runAsk:

```js
async function runAsk(){
  const q = $('#ask-q').value.trim(); if(!q||ask.running) return;
  ask.running=true; S.stop=false; askBtn().disabled=true; askBtn().textContent='Asking…';
  const info=$('#ask-info'), prog=$('#ask-prog');
  info.textContent='Step 1 will send: the index ('+W.index.length+' characters) and your question ('+q.length+' characters). No library passages leave the browser.';
  prog.textContent='Step 1 of 2: choosing pages…'; $('#ask-stop').hidden=false;
  const p1 = 'You are the librarian of a research wiki on neurotechnology in the administration of justice.\nIndex (one line per page):\n'+W.index+'\n\nQuestion: '+q+'\n\nReturn JSON only: {\"pages\": [\"slug\", ...]} — up to five slugs from the index above whose pages answer the question.';
  const r1 = await askModel(p1,{});
  if(S.stop){...}
  if(!r1.json||!Array.isArray(r1.json.pages)){ show raw + retry; return; }
  ask.slugs = r1.json.pages.filter(s=>bySlug[s]).slice(0,5);
  renderAskStep1();
  // step 2
  const bodies = ask.slugs.map(s=>'## '+s+'\n'+bySlug[s].body).join('\n\n');
  info.textContent='Step 2 will send: '+ask.slugs.length+' pages, '+(bodies.length+q.length)+' characters; 0 library passages have left the browser.';
  prog.textContent='Step 2 of 2: drafting the answer…';
  const p2 = '...pin syntax instructions...\nPages:\n'+bodies+'\n\nQuestion: '+q+'\n\nReturn JSON only: {"title": "...", "answer": "markdown, at most 350 words, every claim pinned with [label](pin:id#pPAGE "quote") ✓ using only pins that already stand on the pages above, copied exactly", "cannot_answer": "what the library cannot answer"}';
  const r2 = await askModel(p2,{});
  ...
  ask.answer=r2.json; ask.sentPins = new Set(all pins of sent pages raw keys);
  renderAskAnswer();
}
```

sentPins: for each sent page, for each pin: key id#p|quote.

renderAskAnswer: container data-source="ai", render title h3, answer renderMd(answer,{ai:true,sentPins}), cannot_answer section, regCounts line: "Verified pins by register: (a) 0 · (b) 2 · (c) 5 …" computed over answer pins where verify ok and sent. File button.

Filing card: preview: slug (kebab of title, unique), type question, status draft, updated today, tags input, register computed, links, sources; body preview in <details> maybe; buttons File this page (disabled until all answer pins verify+sent) and Copy answer.

File:

```js
function fileQuestion(){
  const a=ask.answer; const title=a.title||'Question';
  const slug=uniqueSlug(kebab(title));
  const links=[...a.answer.matchAll(LINK_RE)].map(m=>m[1]).filter(s=>bySlug[s]);
  const pins=[...a.answer.matchAll(PIN_RE)].map(...);
  const sources=[...new Set(pins.map(p=>p.id))];
  const register=[...new Set(pins.map(p=>registerOfDoc(p.id)))].filter(r=>r!=='?');
  const body='# '+title+'\n\n**Short answer.** '+firstSentence(a.answer)+'\n\n## Reasoning\n\n'+a.answer+'\n\n## What the library cannot answer\n\n'+(a.cannot_answer||'—')+'\n\n## Related\n\n'+(links.map(s=>'[[['+s+']]]').join(', ')||'—');
  const page={slug,type:'question',title,frontmatter:{title,type:'question',tags:ask.tags.split(',').map(t=>t.trim()).filter(Boolean),register,status:'draft',updated:today(),links,sources},body};
  P.push(page); bySlug[slug]=page; page._links=...; page._pins=...;
  W.index += '\n- [['+slug+']] — '+oneLiner+' · ('+register.join('')+') · ✓'+verifiedCount;
  W.log += '\n## ['+today()+'] ask | '+title+'\n\nFiled from an Ask answer; '+pins.length+' pins, all verified.\n';
  S.changes++; S.changesList.push(slug);
  renderAll(); message.
}
```

Ingest flow — the most complex. Let me define:

```js
const ing = {docId:null, running:false, step:0, batches:[], results:[], takeaways:[], failed:[], dropped:0, newSlugs:[], sourceDraft:null, touchedDrafts:{}, order:[], decisions:{}, filed:false};
```

renderTab03: if no ing.docId → list inbox docs with buttons + "Nothing waits in the inbox" if empty. Else stepper.

Stepper HTML built by renderIngest(): shows steps 1-4 with states; only current step's panel expanded (others collapsed summaries). Running line at top: "calls so far m · passages sent k" (S.calls/S.passages — but "so far" within ingest; I'll track ing.calls0=S.calls at start and show S.calls-ing.calls0).

Step 1 panel: scope text + batches table + Start button (if not started) or progress.

Start:

```js
async function startBatches(){
  ing.running=true; S.stop=false; markTabRunning();
  for(let i=0;i<ing.batches.length;i++){
    if(S.stop) break;
    prog('batch '+(i+1)+' of '+ing.batches.length+' · '+((i)*25)+' of '+doc.passages.length+' passages have left the browser');
    const b=ing.batches[i];
    const passagesJson = JSON.stringify(b.map(p=>({id:p.id,page:p.page,paragraph:p.paragraph,section:p.section,text:p.text})));
    const prompt = 'Ingest ... batches ... Passages (verbatim): '+passagesJson+' ... Return JSON {takeaways:[{claim,quote,passage,pages}]} at most 10; quote 8–40 words copied verbatim from that one passage; passage = the passage id; pages = slugs from the index. Pin syntax: [label](pin:id#pPAGE "quote") ✓ — quote only words that stand in the passages given; the code will check.';
    const r = await askModel(prompt,{passages:b.length});
    if(!r.json||!Array.isArray(r.json.takeaways)){ show raw + retry (store pending batch); continue/break; }
    for(const t of r.json.takeaways){
      const passage = b.find(p=>p.id===t.passage);
      if(!passage){ ing.dropped++; continue; }
      const pinStr = makePin(ing.docId, passage, t.quote||'');
      const pin = parsePin(pinStr);
      const v = verify(pin);
      const pages = (t.pages||[]).filter(s=>bySlug[s]||allowNew(s));
      if(v.ok) ing.takeaways.push({claim:t.claim, quote:t.quote, passage, pin:pinStr, pages, v});
      else ing.failed.push({claim:t.claim, quote:t.quote, passage, pin:pinStr, reason:v.reason, nearest:nearestPassage(doc, pin.page, t.quote)});
    }
    renderIngest();
  }
  ing.running=false; markTabRunning(); prog('Step 1 done: '+ing.takeaways.length+' takeaways verified, '+ing.failed.length+' could not be verified'+(S.stop?', stopped early':''));
  enable step 3 button.
}
```

allowNew(s): if bySlug[s] return true; if ing.newSlugs.length<2 && !ing.newSlugs.includes(s) { ing.newSlugs.push(s); return true;} return false.

nearestPassage(doc, page, quote): among doc.passages.filter(p=>p.page===page), compute longest common consecutive word run with norm(quote); return {passage, run}.

```js
function commonRun(a,b){ const A=norm(a).split(' '), B=norm(b).split(' '); let best=0; for(let i=0;i<A.length;i++){ for(let j=0;j<B.length;j++){ let k=0; while(i+k<A.length&&j+k<B.length&&A[i+k]===B[j+k]) k++; if(k>best)best=k; } } return best; }
```

O(n²·k) — passages ~ up to maybe 100 words, fine.

Step 2 panel: table of takeaways (FIG.01) + failed box.

Step 3: 

```js
async function draftSource(){
  const doc=byId[ing.docId];
  const tks = ing.takeaways.map(t=>({claim:t.claim, pin:t.pin}));
  const prompt = 'Draft the source page for ... Full cite: '+doc.symbol||author...+' ... Register: ... One-liner, Key takeaways, How NOT to read this, Where it feeds the wiki, Related ... Verified takeaways with ready-made pins (copy pins exactly): '+JSON.stringify(tks)+' ... Return JSON {one_liner, body, touches:[{slug,why}]} body at most 900 words, only the pins given, copied exactly. Pin syntax: ...';
  const r = await askModel(prompt,{});
  parse; re-verify pins in r.json.body: pins=[...body.matchAll(PIN_RE)]; verified count.
  ing.sourceDraft = {title: doc.short_title||doc.title, body: r.json.body, one_liner, touches: filtered (existing or newSlugs or stub), pins, verified, notVerified};
  build frontmatter: type source, register from stub page (a-hrc-57-61's register) — registerOfDoc already handles stub; sources [docId]; links from body; tags from touched slugs.
  renderIngest();
}
```

Touched pages for step 3b: union of takeaways' pages (existing slugs) + ing.newSlugs + stub slug (page whose sources==[docId] and status stub). Dedupe. For each slug: draftTouched(slug).

```js
async function draftTouched(slug){
  const page=bySlug[slug];
  const tks = ing.takeaways.filter(t=>t.pages.includes(slug));
  const prompt='Page [[slug]] body:\n'+page.body+'\n\nNew verified takeaways from '+citeAs+' (pins ready-made, copy exactly): '+JSON.stringify(tks.map(t=>({claim:t.claim,pin:t.pin})))+'\n\nReturn JSON {edits:[{after, markdown}], contested} — each after an existing heading of the page or "end"; at most 300 words in all; pins copied exactly; contested a full ```contested block only where this document disagrees with the page. Pin syntax: ...';
  const r=await askModel(prompt,{});
  let body=page.body, inserted=[];
  for(const e of (r.json.edits||[])){ const res=insertAfterHeading(body, e.after, e.markdown); body=res.body; inserted.push(e.markdown); }
  let contested = r.json.contested||null;
  if(contested) body+='\n\n'+contested+'\n';
  // update links/sources
  const fm={...page.frontmatter};
  fm.links=[...new Set([...(fm.links||[]), ...bodyLinksOf(body)])];
  fm.sources=[...new Set([...(fm.sources||[]), ing.docId])];
  // re-verify pins
  const pins=[...body.matchAll(PIN_RE)].map(m=>({...}));
  const verified=pins.filter(p=>verify(p).ok).length;
  const oldPins=new Set(page._pins.map(p=>p.id+'#p'+p.page+'|'+p.quote));
  const added=pins.filter(p=>!oldPins.has(...));
  ing.touchedDrafts[slug]={page, body, frontmatter:fm, inserted, contested, pins, verified, added, addedVerified};
  ing.order.push(slug);
}
```

Run sequentially with progress + stop.

Step 4: review cards in order: sourceDraft (new page) first, then touched drafts. Each card: fieldset legend "Change i of n — slug"; title/type; "new page"/"edited"; "paragraphs inserted: k · pins added: j (verified v, not verified u)"; rendered body with opts.inserted=inserted (diff view); pins as chips (renderMd handles); Approve/Reject buttons.

After all decided → "File the approved changes" button.

fileIngest():

```js
function fileIngest(){
  const doc=byId[ing.docId];
  const approved=[];
  if(ing.sourceDraft && ing.decisions.__source==='approved'){
    const slug=uniqueSlug(kebab(doc.short_title||doc.title));
    const page={slug,type:'source',title:doc.title,frontmatter:{...built},body:ing.sourceDraft.body};
    P.push(page); bySlug[slug]=page; recompute; approved.push(slug);
    // replace stub index line? The stub line stays; source line added under Sources.
  }
  for(const slug of ing.order){ if(ing.decisions[slug]==='approved'){ const d=ing.touchedDrafts[slug]; bySlug[slug].body=d.body; bySlug[slug].frontmatter=d.frontmatter; bySlug[slug].frontmatter.updated=today(); recompute(bySlug[slug]); approved.push(slug);} }
  // index updates
  updateIndexFor(approved, ing.sourceDraft? [newSlug]:[]);
  // log
  W.log+='\n## ['+today()+'] ingest | '+(doc.symbol||doc.id)+': '+(doc.short_title||doc.title)+'\n\nRead '+doc.passages.length+' passages ('+citeAs[doc.id]+', register ('+registerOfDoc(doc.id)+')). Wrote [[...]]. ... Rejected: [[...]].\n';
  // tensions for new contested
  for each approved touched draft with contested: append tensions entry.
  doc.status='ingested';
  S.changes+=approved.length; S.changesList.push(...approved);
  ing.filed=true; runLint(); renderAll();
}
```

updateIndexFor: for each changed slug: compute line '- [[slug]] — one-liner · (letters) · ✓N'; if index has line with [[slug]] replace; else insert. For new source page insert under Sources group — I don't know group layout; I'll insert after the last line containing a source page... simpler: append at end of index? Spec says "the source page's line goes under Sources". I'll find index lines; group detection: index likely has headings like "## Sources"? Unknown. I'll do: find first line matching /- \[\[([^\]]+)\]\]/ whose slug is a source page; insert after the last consecutive such line. Fallback append at end. Also update first line pin count: replace /(\d[\d,]*) pins/ with new total verified? The index states total pins (707). New total = total pins after changes. And pages count if new page: replace /(\d+) pages/ if present.

OK. Lint:

```js
function computeLint(){
  const checks=[];
  const totalPins=P.reduce((n,p)=>n+p._pins.length,0);
  const verified=P.reduce((n,p)=>n+p._pins.filter(pn=>verify(pn).ok).length,0);
  const stated=(W.index.match(/(\d[\d,]*) pins/)||[])[1];
  checks.push({name:'Pins found vs the index line', count: totalPins, pass: String(totalPins)===String(stated).replace(/,/g,''), detail: stated+' stated', pages:[]});
  ...
}
```

I'll write each check.

Check "index ✓N differs": parse index lines /- \[\[([^\]]+)\]\][^\n]*✓([\d,]+)/; compare with page verified count.

Contested vs tensions: pages with contested blocks: detect via /```contested/ in body; tensions cards: parse tensions for /card: \[\[([^\]]+)\]\]/g. Check both directions.

Now tab 05:

```js
function renderTab05(){
  log entries: W.log.split(/(?=^## )/m).filter(Boolean); newest first toggle.
  each: <details><summary>heading line</summary><div>renderMd(rest)</div></details>; entries added this session (S.sessionLog entries) get red "this session" tag.
  tensions: split on /(?=^### )/m; render each: heading, card link button data-action open-page.
  method note, source line.
  Download buttons.
}
```

Session log entries: track S.logAdded = array of heading strings.

Download:

```js
function download(name, text, type){
  const blob=new Blob([text],{type:type||'application/json'});
  const a=document.createElement('a'); a.href=URL.createObjectURL(blob); a.download=name; document.body.appendChild(a); a.click(); setTimeout(()=>{URL.revokeObjectURL(a.href);a.remove();},500);
}
```

JSON: JSON.stringify({title:W.title, source:W.source, built:W.built, count:P.length, schema:W.schema, pages:P, index:W.index, log:W.log, tensions:W.tensions, changes:S.changesList.map(...), library_status: D.map(d=>({id:d.id,status:d.status}))}, null, 2).

Markdown of changed pages: S.changesList slugs → frontmatter YAML + body joined with '\n\n---\n\n'.

Event delegation:

```js
document.addEventListener('click', e=>{
  const t=e.target.closest('[data-action]');
  if(!t) return;
  const a=t.dataset.action;
  if(a==='tab'){ switchTab(t.dataset.tab); }
  else if(a==='open-page'){ openPage(t.dataset.slug); }
  else if(a==='pin-open'){ studio.openSource(t.dataset.id, +t.dataset.page, t.dataset.quote); }
  else if(a==='pin-toggle'){ const d=t.parentElement.querySelector('.pin-detail'); const open=d.hidden; d.hidden=!open; t.setAttribute('aria-expanded',String(open)); t.textContent=open?'hide':'details'; }
  ...
});
```

Keyboard: tablist arrow keys:

```js
tabsEl.addEventListener('keydown', e=>{
  const idx=[...tabsEl.querySelectorAll('[role=tab]')].indexOf(document.activeElement);
  if(e.key==='ArrowRight'){...focus & activate next} etc.
});
```

Escape: document keydown Escape → S.stop=true.

Hash: window.addEventListener('hashchange', ...) → if bySlug[hash.slice(1)] openPage.

Now sizes: this is going to be long. Let me just write it, trying to be economical. I'll skip some niceties if needed but keep all required features. Target ≤1500 lines.

Let me write the final code now, carefully.

Also note: "Before the code block: at most three short sentences saying what you built. After it: nothing."

One more detail: tab 01 default main shows index rendered like a page. Index rendered via renderMd(W.index).

Page list groups: types order: source, concept, entity, question with mono labels "SOURCES", "CONCEPTS", "ENTITIES", "QUESTIONS". Each item: button with title + register letters + pin count; stub tag.

Filter: input event → renderTab01 list only.

Big number "n of 40 pages" serif.

Copy page as markdown button in page view.

Let me now also handle "running" tab label: tab 03 button text updated when ing.running.

Write today(): new Date().toISOString().slice(0,10).

kebab: s.toLowerCase().replace(/[^a-z0-9]+/g,'-').replace(/^-|-$/g,'').

uniqueSlug: while bySlug[s] s+='-2' etc.

firstSentence: split on /(?<=[.!?])\s/ — lookbehind may be OK in modern browsers; safer: match /^(.{20,200?[.!?])(\s|$)/. I'll do simple: const m=a.match(/^.{10,300}?[.!?](\s|$)/s); return m?m[0].trim():a.slice(0,200).

Now, prompt for ask step 2 must include register naming instruction: "name the register where it matters ((c) UN report, (b) General Comment…); keep the document's own verb; never present (c)–(f) as what the treaty requires."

Alright — also the grey box "states what each step will send before it goes" — I update #ask-info before each call. Good.

Progress + Stop: #ask-stop button sets S.stop=true; flows check S.stop between calls.

Parse failure: show raw in <pre data-source="ai"> with Retry button that re-sends same prompt — store last prompt & rerun function.

I'll implement askModel returning {json, raw, error}; flows handle.

Let me now write out the entire HTML. I'll count roughly as I go and keep functions tight.

Also remember: no external loads. Chart.js not needed.

Let me write:

```html
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
.serif{font-family:Georgia,"Times New Roman",serif}
header{display:flex;justify-content:space-between;gap:24px;align-items:flex-end;padding:16px 24px 12px;border-bottom:1px solid var(--rule);flex-wrap:wrap}
header h1{font-family:Georgia,"Times New Roman",serif;font-weight:400;font-size:26px;margin:4px 0 6px}
.meta{color:var(--grey);font-size:13.5px}
.hdr-right{text-align:right;color:var(--grey)}
.dim{color:var(--grey)}
a{color:var(--red)}
button{font:inherit;color:inherit}
:focus-visible{outline:3px solid var(--red);outline-offset:2px}
nav[role=tablist]{display:flex;gap:2px;padding:0 24px;border-bottom:1px solid var(--rule);flex-wrap:wrap}
nav[role=tablist] [role=tab]{background:none;border:none;border-bottom:3px solid transparent;padding:10px 14px;cursor:pointer;font-family:ui-monospace,Menlo,Consolas,monospace;font-size:12px;letter-spacing:.09em;text-transform:uppercase;color:var(--grey)}
nav[role=tablist] [role=tab][aria-selected=true]{color:var(--red);border-bottom-color:var(--red)}
nav[role=tablist] [role=tab] .run{color:var(--red)}
main{padding:20px 24px 40px;max-width:1280px}
section[role=tabpanel]{padding-top:8px}
h2{font-family:Georgia,serif;font-weight:400;font-size:24px;margin:0 0 10px}
h3{font-family:Georgia,serif;font-weight:400;font-size:19px;margin:22px 0 8px}
h4{font-size:16px;margin:16px 0 6px}
.bignum{font-family:Georgia,serif;font-size:52px;line-height:1.05}
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
.verdict{font-family:Georgia,serif;font-size:30px;margin:2px 0 6px}
.lean{height:10px;background:var(--rule);margin:6px 0 12px;max-width:420px}
.lean>div{height:100%;background:var(--red)}
.fig{color:var(--grey);margin:8px 0 2px}
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
.old{color:var(--grey)}
.diff .old{color:#8d887e}
.note{color:var(--grey);font-size:13.5px}
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
...
```

Now body HTML:

```html
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
  <section role="tabpanel" id="panel-02" aria-labelledby="tabbtn-02" hidden></section>
  <section role="tabpanel" id="panel-03" aria-labelledby="tabbtn-03" hidden></section>
  <section role="tabpanel" id="panel-04" aria-labelledby="tabbtn-04" hidden></section>
  <section role="tabpanel" id="panel-05" aria-labelledby="tabbtn-05" hidden></section>
</main>
<footer class="mono" id="foot"></footer>
<script>
...
</script>
</body>
</html>
```

Tab 02 static content — I'll build it in JS to keep HTML small, or static HTML. I'll do static HTML for form controls:

```html
<section role="tabpanel" id="panel-02" ...>
  <h2>What does the wiki answer, and is it worth filing?</h2>
  <label for="ask-q">Your question</label>
  <textarea id="ask-q" placeholder="Ask the wiki…"></textarea>
  <div style="margin:10px 0"><button class="btn primary" id="ask-btn" data-action="ask">Ask the wiki</button>
  <button class="btn" id="ask-stop" data-action="stop" hidden>Stop</button></div>
  <div class="greybox" id="ask-info">Step 1 will send the index and your question; step 2 the chosen pages' bodies. Nothing leaves the browser until you press Ask the wiki.</div>
  <div class="progress" id="ask-prog" aria-live="polite"></div>
  <div id="ask-out"></div>
</section>
```

Tab 03, 04, 05 containers filled by JS.

Now the script. Let me write it fully.

```js
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
function esc(s){return String(s??'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');}
function today(){return new Date().toISOString().slice(0,10);}
function kebab(s){return String(s).toLowerCase().replace(/[^a-z0-9]+/g,'-').replace(/^-+|-+$/g,'')||'page';}
function uniqueSlug(base){let s=base,n=2;while(bySlug[s])s=base+'-'+(n++);return s;}
```

Precompute:

```js
function prep(p){ p._links=[...p.body.matchAll(WLINK_RE)].map(m=>m[1]); p._pins=[...p.body.matchAll(PIN_RE)].map(m=>({label:m[1],id:m[2],page:+m[3],quote:m[4]||'',mark:m[5]})); }
P.forEach(prep);
const backlinks={}; P.forEach(p=>p._links.forEach(s=>{(backlinks[s]=backlinks[s]||[]).push(p.slug);}));
```

norm/verify/citeAs/registerOfDoc/makePin as planned.

Session:

```js
const S={tab:'01',page:null,changes:0,calls:0,passages:0,stop:false,changesList:[],logAdded:[],lintBefore:null};
```

renderCounters, renderHeader.

Tabs:

```js
const TABS=['01','02','03','04','05'];
function switchTab(t){ S.tab=t; TABS.forEach(x=>{ const b=$('#tabbtn-'+x); b.setAttribute('aria-selected',String(x===t)); $('#panel-'+x).hidden=x!==t; }); if(t==='01')render01(); if(t==='02')render02(); if(t==='03')render03(); if(t==='04')render04(); if(t==='05')render05(); }
```

render01:

```js
let filterQ='';
function render01(){
  const panel=$('#panel-01');
  const q=filterQ.toLowerCase();
  const shown=P.filter(p=>!q||p.slug.includes(q)||p.title.toLowerCase().includes(q)||(p.frontmatter.tags||[]).some(t=>t.toLowerCase().includes(q)));
  const types=[['source','Sources'],['concept','Concepts'],['entity','Entities'],['question','Questions']];
  let list='';
  types.forEach(([ty,label])=>{
    const g=shown.filter(p=>p.type===ty);
    if(!g.length)return;
    list+='<div class="mono grouplabel">'+label+'</div><div class="pagelist">';
    g.forEach(p=>{
      const pins=p._pins.length, stub=p.frontmatter.status==='stub';
      list+='<button data-action="open-page" data-slug="'+esc(p.slug)+'" class="'+(S.page===p.slug?'sel':'')+'"><span class="cnt">'+pins+' pins · '+(p.frontmatter.register||[]).join('')+'</span>'+esc(p.title)+(stub?' <span class="badge stub">stub</span>':'')+'</button>';
    });
    list+='</div>';
  });
  const main = S.page&&bySlug[S.page] ? pageHtml(bySlug[S.page]) : '<h2>The index</h2><div class="note">Every page in one line; click a page on the left. How this is computed: the index below is the wiki\'s own catalog, rendered as a page.</div>'+renderMd(W.index,{});
  panel.innerHTML='<div class="layout"><aside class="rail"><label for="pg-filter">title, tag or slug</label><input type="text" id="pg-filter" value="'+esc(filterQ)+'"><div class="bignum" id="pg-count">'+shown.length+' of '+P.length+'</div><div class="mono dim" style="margin-bottom:6px">pages</div>'+list+'</aside><div class="content">'+main+'</div></div>';
  $('#pg-filter').addEventListener('input',e=>{filterQ=e.target.value;render01();});
}
```

Wait — re-rendering on each input resets focus. Better: only re-render the list, not the input. I'll restructure: render01 builds static shell once; list re-render function updates #pg-list and #pg-count. Let me do that: render01() builds shell if not built; updateList() updates list. Simpler: keep input listener that calls updateList() only.

pageHtml(p):

```js
function pageHtml(p){
  const fm=p.frontmatter;
  let badges='<span class="badge">'+esc(p.type)+'</span>';
  (fm.register||[]).forEach(r=>badges+='<span class="badge" title="'+esc(REG_NAMES[r]||r)+'">'+esc(r)+' · '+esc(REG_NAMES[r]||'?')+'</span>');
  badges+='<span class="badge">'+esc(fm.status||'')+'</span><span class="badge">updated '+esc(fm.updated||'')+'</span>';
  const tags=(fm.tags||[]).map(t=>'<span class="tag">#'+esc(t)+'</span>').join('');
  let out='<h2>'+esc(p.title)+'</h2><div>'+badges+'</div><div style="margin:6px 0">'+tags+'</div>';
  out+='<div class="body">'+renderMd(p.body,{pageSlug:p.slug})+'</div>';
  // links out / linked from / sources
  const bodySet=new Set(p._links);
  out+='<h3>Links out</h3><div>'+(fm.links||[]).map(s=>bodySet.has(s)?linkSlug(s):linkSlug(s)+' <span class="warn">frontmatter only</span>').join(' · ')+'</div>';
  out+='<h3>Linked from</h3><div>'+((backlinks[p.slug]||[]).map(linkSlug).join(' · ')||'<span class="dim">no page links here</span>')+'</div>';
  out+='<h3>Sources</h3><div>';
  (fm.sources||[]).forEach(id=>{ const d=byId[id]; if(!d){out+='<div>'+esc(id)+' <span class="bad">not in the library</span></div>';return;} out+='<div>· <a href="'+esc(d.url)+'" target="_blank" rel="noopener">'+esc(d.short_title||d.title)+'</a> — '+esc(d.kind)+', '+esc(d.year)+(d.status==='inbox'?' <span class="badge stub">inbox</span>':'')+'</div>'; });
  out+='</div>';
  out+='<div style="margin:14px 0"><button class="btn" data-action="copy-page" data-slug="'+esc(p.slug)+'">Copy page as markdown</button></div>';
  return out;
}
function linkSlug(s){ return bySlug[s]? '<a href="#'+esc(s)+'" data-action="open-page" data-slug="'+esc(s)+'">'+esc(s)+'</a>' : '<span class="bad">'+esc(s)+' (no page)</span>'; }
```

copy-page handler: build markdown, clipboard.

renderMd with opts.pageSlug for contested tensions link.

contestedHtml needs pageSlug: tensions link "in the tensions register (tab 05)" when a ### entry names this page in card:. Compute tensionsCards set once (and update after ingest adds entries — recompute lazily each render: parseTensions()).

parseTensions: 

```js
function tensionsEntries(){ return W.tensions.split(/(?=^### )/m).filter(s=>s.trim()); }
function tensionsCards(){ const s=new Set(); tensionsEntries().forEach(e=>{ const m=e.match(/card:\s*\[\[([^\]]+)\]\]/); if(m)s.add(m[1]); }); return s; }
```

Index parse:

```js
function indexLines(){ return W.index.split('\n').filter(l=>/^- \[\[/.test(l)); }
```

Ask flow — write render02 to set up static (already static in HTML) and wire via delegation; runAsk as planned.

Let me write ask functions concretely:

```js
const ask={running:false,slugs:[],answer:null,raw:null,badJson:false,sentPins:new Set(),regLine:'',filing:false,tags:'',lastPrompt:null,lastRun:null};
function askBtn(){return $('#ask-btn');}
async function runAsk(){
  const q=$('#ask-q').value.trim(); if(!q||ask.running)return;
  ask.running=true; S.stop=false; askBtn().disabled=true; const old=askBtn().textContent; askBtn().textContent='Asking…';
  $('#ask-stop').hidden=false; $('#ask-out').innerHTML='';
  const info=$('#ask-info'), prog=$('#ask-prog');
  try{
    info.textContent='Step 1 will send: the index ('+W.index.length+' characters) and your question ('+q.length+' characters). No library passages leave the browser.';
    prog.textContent='Step 1 of 2 · choosing pages…';
    const p1='You route questions in a research wiki on neurotechnology in the administration of justice.\n\nIndex (one line per page):\n'+W.index+'\n\nQuestion: '+q+'\n\nReturn JSON only: {"pages":["slug",…]} — up to five slugs from the index above.';
    ask.lastPrompt=p1; ask.lastRun=()=>runAskFrom(q,1);
    const r1=await askModel(p1,{});
    if(S.stop){prog.textContent='Stopped.';return;}
    if(!r1.json||!Array.isArray(r1.json.pages)){ askFail(r1,'Step 1 did not return JSON.'); return; }
    ask.slugs=r1.json.pages.filter(s=>bySlug[s]).slice(0,5);
    renderAskStep1(q);
    await runAskStep2(q);
  } finally { ask.running=false; askBtn().disabled=false; askBtn().textContent=ask.answer?'Ask again':'Ask the wiki'; $('#ask-stop').hidden=true; }
}
```

Hmm retry semantics: "a parse failure shows the raw answer with Retry" — Retry re-sends the same prompt. I'll implement askFail(r,msg): show pre with raw + Retry button data-action="ask-retry" storing ask.lastPrompt and a continuation. To keep simple: Retry re-runs the whole runAsk with same question (re-sends step1 then step2). Acceptable: "Retry re-sends the same prompt". I'll store lastPrompt and a function; retry button calls it. Simplify: retry re-executes runAsk() (same question still in box). Fine.

runAskStep2(q):

```js
async function runAskStep2(q){
  const info=$('#ask-info'), prog=$('#ask-prog');
  const bodies=ask.slugs.map(s=>'## '+s+' — '+bySlug[s].title+'\n\n'+bySlug[s].body).join('\n\n---\n\n');
  const chars=bodies.length+q.length;
  info.textContent='Step 2 will send: '+ask.slugs.length+' pages, '+chars+' characters; 0 library passages have left the browser. The answer must pin every claim to a pin that already stands on those pages.';
  prog.textContent='Step 2 of 2 · drafting the answer…';
  const p2='You answer from a research wiki on neurotechnology in the administration of justice. Pages:\n\n'+bodies+'\n\nQuestion: '+q+'\n\nReturn JSON only: {"title":"…","answer":"markdown, at most 350 words","cannot_answer":"what the library cannot answer"}. In the answer, pin every claim with [label](pin:id#pPAGE "quote") ✓ using only pins that already stand on the pages above, copied exactly — quote only words that stand in the passages given; the code will check. Name the register where it matters ((a) treaty law, (b) General Comment, (c) UN report, (d) NHRI, (e) civil society, (f) scholarship); keep each document\'s own verb; never present (c)–(f) as what the treaty requires.';
  const r2=await askModel(p2,{});
  if(S.stop){prog.textContent='Stopped.';return;}
  if(!r2.json||typeof r2.json.answer!=='string'){ askFail(r2,'Step 2 did not return JSON.'); return; }
  ask.answer=r2.json;
  ask.sentPins=new Set();
  ask.slugs.forEach(s=>bySlug[s]._pins.forEach(pn=>ask.sentPins.add(pn.id+'#p'+pn.page+'|'+pn.quote)));
  renderAskAnswer();
}
```

renderAskStep1: chips of slugs + "Change pages" button toggling panel with checkboxes (all pages, checked if in ask.slugs) + "Apply pages" button → sets ask.slugs from checked (max 5? allow any) and calls runAskStep2 again.

renderAskAnswer:

```js
function renderAskAnswer(){
  const a=ask.answer; const out=$('#ask-out');
  const pins=[...a.answer.matchAll(PIN_RE)].map(m=>({label:m[1],id:m[2],page:+m[3],quote:m[4]||'',mark:m[5]}));
  const ver=pins.filter(p=>verify(p).ok && ask.sentPins.has(p.id+'#p'+p.page+'|'+p.quote));
  const regs={}; ver.forEach(p=>{const r=registerOfDoc(p.id); regs[r]=(regs[r]||0)+1;});
  ask.regLine=Object.keys(REG_W).map(r=>'('+r+') '+(regs[r]||0)).join(' · ');
  let html='<div data-source="ai"><h3>'+esc(a.title||'Answer')+'</h3><div class="body">'+renderMd(a.answer,{ai:true,sentPins:ask.sentPins})+'</div>';
  html+='<h4>What the library cannot answer</h4><p>'+esc(a.cannot_answer||'—')+'</p>';
  html+='<div class="note">Verified pins by register: '+esc(ask.regLine)+' · computed by this page from the pins above.</div></div>';
  html+='<div style="margin:12px 0"><button class="btn" data-action="ask-file-open">File as a question page</button></div>';
  html+='<div id="ask-file"></div>';
  out.innerHTML=html;
}
```

ask-file-open: render filing card into #ask-file:

```js
function renderFiling(){
  const a=ask.answer; const title=a.title||'Question';
  const slug=uniqueSlug(kebab(title));
  const pins=[...a.answer.matchAll(PIN_RE)].map(...);
  const allOk=pins.length>0 && pins.every(p=>verify(p).ok && ask.sentPins.has(...));
  const links=[...new Set([...a.answer.matchAll(WLINK_RE)].map(m=>m[1]).filter(s=>bySlug[s]))];
  const sources=[...new Set(pins.map(p=>p.id))];
  const register=[...new Set(pins.map(p=>registerOfDoc(p.id)))].filter(r=>r&&r!=='?');
  const body=buildQuestionBody(title,a,links);
  preview html: dl of slug/type/status/updated/register/links/sources + tags input + body preview in details + buttons File this page (disabled unless allOk, with reason) and Copy answer.
}
```

File handler: as planned; also S.logAdded.push('## ['+today()+'] ask | '+title).

Ingest rendering — render03:

```js
const ing={docId:null,running:false,started:false,batches:[],takeaways:[],failed:[],dropped:0,newSlugs:[],sourceDraft:null,order:[],drafts:{},decisions:{},filed:false,calls0:0,progEl:null};
function inboxDocs(){return D.filter(d=>d.status==='inbox');}
function render03(){
  const panel=$('#panel-03');
  if(!ing.docId){
    const docs=inboxDocs();
    let h='<h2>What would the waiting document change?</h2>';
    if(!docs.length){ h+='<p class="note">Nothing waits in the inbox.</p>'; }
    else { h+='<p>One document waits in the inbox. Ingesting sends all its passages to the model in batches, verifies every quote the code can check, and nothing is written until you approve each change.</p>';
      docs.forEach(d=>{ h+='<div style="margin:10px 0"><button class="btn primary" data-action="ingest-start" data-id="'+esc(d.id)+'">Ingest '+esc(d.symbol||d.short_title||d.id)+'</button> <span class="note">'+esc(d.short_title||d.title)+' · '+d.passages.length+' passages</span></div>'; }); }
    panel.innerHTML=h; return;
  }
  const doc=byId[ing.docId];
  ...stepper...
}
```

Stepper HTML:

```js
let h='<h2>Ingest '+esc(doc.symbol||doc.id)+' — '+esc(doc.short_title||doc.title)+'</h2>';
h+='<div class="progress" aria-live="polite" id="ing-prog">'+(ing.progText||'ready')+' · calls so far '+(S.calls-ing.calls0)+' · passages sent '+(S.passages-ing.pass0)+'</div>';
h+='<button class="btn" data-action="stop" '+(ing.running?'':'hidden')+'>Stop</button>';
steps...
```

Track ing.pass0 too.

Step 1 panel:

```js
h+='<div class="step"><h3>Step 1 · Scope</h3>';
if(!ing.started){
  const n=doc.passages.length, calls=Math.ceil(n/25);
  h+='<p>All '+n+' passages will be sent, in batches of 25 ('+calls+' calls), '+doc.passages.reduce((s,p)=>s+p.text.length,0)+' characters; nothing is held back.</p>';
  h+='<table><caption>FIG.01 · Batches</caption><thead><tr><th>batch</th><th>paragraphs</th><th>PDF pages</th><th class="num">passages</th></tr></thead><tbody>';
  ing.batches.forEach((b,i)=>{ h+='<tr><td>'+(i+1)+'</td><td>'+esc(b[0].paragraph||'?')+'–'+esc(b[b.length-1].paragraph||'?')+'</td><td>'+b[0].page+'–'+b[b.length-1].page+'</td><td class="num">'+b.length+'</td></tr>'; });
  h+='</tbody></table>';
  h+='<button class="btn primary" data-action="ingest-run">Start</button>';
} else { h+='<p class="note">Batches run one after another; Stop keeps what has returned.</p>'; }
h+='</div>';
```

Step 2 panel: table of takeaways + failed box (shown when started).

Step 3 panel: buttons.

Step 4 panel: cards + file button.

I'll render steps 2–4 always but with content depending on state (empty notes). To keep clickable count low, fine.

ingest-start handler:

```js
ing.docId=id; ing.calls0=S.calls; ing.pass0=S.passages;
const doc=byId[id]; ing.batches=[]; for(let i=0;i<doc.passages.length;i+=25) ing.batches.push(doc.passages.slice(i,i+25));
render03();
```

ingest-run: startBatches().

renderIngest = render03 basically; I'll just call render03() after each batch (rebuilds panel; progress text stored in ing.progText).

But rebuilding during run loses scroll — acceptable.

Careful: render03 rebuild while awaiting — the Start button replaced by progress. OK.

Step 3 handlers: ingest-draft-source, ingest-draft-touched.

Touched slugs computation:

```js
function touchedSlugs(){
  const set=new Set();
  ing.takeaways.forEach(t=>t.pages.forEach(s=>{ if(bySlug[s]) set.add(s); }));
  ing.newSlugs.forEach(s=>set.add(s));
  const stub=P.find(p=>p.frontmatter.status==='stub'&&p.frontmatter.sources.includes(ing.docId));
  if(stub) set.add(stub.slug);
  if(ing.sourceDraft) (ing.sourceDraft.touches||[]).forEach(t=>{ if(bySlug[t.slug]||ing.newSlugs.includes(t.slug)) set.add(t.slug); });
  return [...set];
}
```

Hmm new slugs from takeaways pages: allowNew adds to ing.newSlugs when model proposes. Also sourceDraft touches may add. Keep as above.

draftTouched for each slug in touchedSlugs() sequentially with progress; store in ing.drafts[slug]; ing.order.

Step 4: cards list = [sourceDraft as '__new__'] + ing.order. Render each as fieldset with Approve/Reject (data-action approve/reject with data-key). decisions[key]. When all keys decided → show File button.

Change card render:

```js
function changeCard(key, i, n){
  const isNew = key==='__new__';
  const d = isNew? ing.sourceDraft : ing.drafts[key];
  const page = isNew? null : bySlug[key];
  const title = isNew? d.title : page.title;
  const type = isNew? 'source' : page.type;
  const pins=[...d.body.matchAll(PIN_RE)].map(m=>({label:m[1],id:m[2],page:+m[3],quote:m[4]||'',mark:m[5]}));
  const ver=pins.filter(p=>verify(p).ok).length;
  const oldKeys = page? new Set(page._pins.map(p=>p.id+'#p'+p.page+'|'+p.quote)) : new Set();
  const added=pins.filter(p=>!oldKeys.has(p.id+'#p'+p.page+'|'+p.quote));
  const addedVer=added.filter(p=>verify(p).ok).length;
  const dec=ing.decisions[key];
  let h='<fieldset class="card"><legend>Change '+i+' of '+n+' · '+esc(key==='__new__'?d.slug:key)+'</legend>';
  h+='<div>'+esc(title)+' · '+esc(type)+' · '+(isNew?'new page':'edited')+' · paragraphs inserted: '+(d.inserted?d.inserted.length:0)+' · pins added: '+added.length+' (verified '+addedVer+', not verified '+(added.length-addedVer)+')</div>';
  h+='<div class="diff body" style="margin:10px 0">'+renderMd(d.body,{inserted:d.inserted||[]})+'</div>';
  h+='<div>';
  h+='<button class="btn primary" data-action="approve" data-key="'+esc(key)+'" '+(dec?'disabled':'')+'>Approve change '+i+' of '+n+'</button> ';
  h+='<button class="btn" data-action="reject" data-key="'+esc(key)+'" '+(dec?'disabled':'')+'>Reject change '+i+' of '+n+'</button> ';
  h+='<span class="note">'+(dec?('decision: '+dec):'nothing is written until you approve')+'</span></div></fieldset>';
  return h;
}
```

Note: for edited pages, d.body includes whole new body; inserted marks highlight. For new page, inserted = [whole body]? Then everything yellow — spec says inserted paragraphs pale yellow and rest grey; for a new page all is inserted. Set inserted=[d.body] for new page. OK.

approve/reject handlers set decisions, S.stop not needed; re-render; if all decided show file button (render03 includes it when complete).

fileIngest as planned.

Lint — render04:

```js
function computeLint(){
  const checks=[];
  const add=(name,count,pass,pages,detail)=>checks.push({name,count,pass,pages:pages||[],detail:detail||''});
  const totalPins=P.reduce((n,p)=>n+p._pins.length,0);
  const verPins=P.reduce((n,p)=>n+p._pins.filter(pn=>verify(pn).ok).length,0);
  const stated=(W.index.match(/(\d[\d,]*) pins/)||[,'?'])[1].replace(/,/g,'');
  add('Pins found by the regular expression vs the index line', totalPins, String(totalPins)===stated, [], 'index says '+stated);
  const notVer=P.filter(p=>p._pins.some(pn=>!verify(pn).ok));
  add('Pins not verified by this page', P.reduce((n,p)=>n+p._pins.filter(pn=>!verify(pn).ok).length,0), notVer.length===0, notVer.map(p=>p.slug));
  const badMark=P.filter(p=>p._pins.some(pn=>pn.mark==='✓'&&!verify(pn).ok));
  add('Pins marked ✓ that fail verification', badMark.reduce((n,p)=>n+p._pins.filter(pn=>pn.mark==='✓'&&!verify(pn).ok).length,0), badMark.length===0, badMark.map(p=>p.slug));
  const dangling=P.filter(p=>p._links.some(s=>!bySlug[s]));
  add('Dangling [[links]]', dangling.reduce((n,p)=>n+p._links.filter(s=>!bySlug[s]).length,0), dangling.length===0, dangling.map(p=>p.slug));
  const orphans=P.filter(p=>!(backlinks[p.slug]||[]).length);
  add('Orphan pages (nothing links to them)', orphans.length, orphans.length===0, orphans.map(p=>p.slug));
  const srcDiff=P.filter(p=>{ const a=new Set(p.frontmatter.sources||[]), b=new Set(p._pins.map(pn=>pn.id)); return a.size!==b.size||[...a].some(x=>!b.has(x)); });
  add('frontmatter.sources differ from the pinned documents', srcDiff.length, srcDiff.length===0, srcDiff.map(p=>p.slug));
  const noPins=P.filter(p=>p._pins.length===0);
  add('Pages with no pins', noPins.length, noPins.length===0, noPins.map(p=>p.slug));
  const nonRecip=P.filter(p=>{ const a=new Set(p.frontmatter.links||[]), b=new Set(p._links); return a.size!==b.size||[...a].some(x=>!b.has(x)); });
  add('frontmatter.links not reciprocated in the body', nonRecip.length, nonRecip.length===0, nonRecip.map(p=>p.slug));
  const idxSlugs=new Set(indexLines().map(l=>l.match(/\[\[([^\]]+)\]\]/)[1]));
  const missingIdx=P.filter(p=>!idxSlugs.has(p.slug));
  const ghostIdx=[...idxSlugs].filter(s=>!bySlug[s]);
  add('Pages missing from the index / index lines without a page', missingIdx.length+ghostIdx.length, missingIdx.length===0&&ghostIdx.length===0, [...missingIdx.map(p=>p.slug),...ghostIdx]);
  const idxCount={}; indexLines().forEach(l=>{ const m=l.match(/\[\[([^\]]+)\]\]/), c=l.match(/✓([\d,]+)/); if(m&&c) idxCount[m[1]]=+c[1].replace(/,/g,''); });
  const wrongN=P.filter(p=>idxCount[p.slug]!==undefined&&idxCount[p.slug]!==p._pins.filter(pn=>verify(pn).ok).length);
  add('Index ✓N differs from the computed verified count', wrongN.length, wrongN.length===0, wrongN.map(p=>p.slug));
  const cards=new Set(P.filter(p=>/```contested/.test(p.body)).map(p=>p.slug));
  const tcards=tensionsCards();
  const c1=[...cards].filter(s=>!tcards.has(s)), c2=[...tcards].filter(s=>!cards.has(s));
  add('Contested cards without a tensions entry / reverse', c1.length+c2.length, c1.length===0&&c2.length===0, [...c1,...c2]);
  const stubs=P.filter(p=>p.frontmatter.status==='stub');
  add('Stub pages', stubs.length, false, stubs.map(p=>p.slug), 'a stub waits for its ingest');
  const inboxPins=P.filter(p=>p._pins.some(pn=>byId[pn.id]&&byId[pn.id].status==='inbox'));
  add('Pins to a document still in the inbox', inboxPins.reduce((n,p)=>n+p._pins.filter(pn=>byId[pn.id]&&byId[pn.id].status==='inbox').length,0), inboxPins.length===0, inboxPins.map(p=>p.slug));
  return {checks, totalPins, verPins};
}
```

render04:

```js
function render04(){
  const panel=$('#panel-04');
  const L=computeLint(); S.lint=L;
  const need=L.checks.filter(c=>!c.pass).length;
  let h='<h2>Can I trust this?</h2>';
  h+='<div class="bignum">'+L.verPins+' of '+L.totalPins+'</div><div class="note">pins verified by this page · '+need+' lint checks need a look · How this is computed: every pin in every page is re-checked against WORKSHOP_DATA.library by the code on this page.</div>';
  h+='<div style="margin:12px 0"><button class="btn primary" data-action="lint">Lint now</button></div>';
  h+='<table><caption>FIG.02 · Lint checks — counting, matching and verification are done by this page\'s code</caption><thead><tr><th scope="col">check</th><th scope="col" class="num">count</th><th scope="col">result</th><th scope="col">pages</th></tr></thead><tbody>';
  L.checks.forEach(c=>{ h+='<tr><td>'+esc(c.name)+(c.detail?' <span class="dim">('+esc(c.detail)+')</span>':'')+'</td><td class="num">'+c.count+'</td><td class="'+(c.pass?'ok':'bad')+'">'+(c.pass?'0 · pass':c.count+' · check')+'</td><td>'+(c.pages.map(s=>bySlug[s]?linkSlug(s):esc(s)).join(', ')||'—')+'</td></tr>'; });
  h+='</tbody></table>';
  h+='<details open><summary>How this app checks itself</summary><div class="note"><ul>';
  h+='<li>Pins: found by the regular expression against the number stated in the first line of the index; each verified against a passage of the pinned document on that PDF page, fragments joined by "…" checked in order after normalising whitespace, quotes, dashes and hyphenation; capitals are kept.</li>';
  h+='<li>Labels: every verified pin\'s label must contain "para. N" or "p. label" of its passage.</li>';
  h+='<li>Structure: dangling links, orphans, sources vs pinned documents, index coverage, contested cards vs the tensions register.</li>';
  h+='<li>Contradictions between pages are named in the schema but are not linted by code — that reading stays with a person.</li></ul></div></details>';
  panel.innerHTML=h;
}
```

Lint button: re-run render04 with message "Re-run" — button text changes after first run; store S.linted=true.

render05:

```js
let logNewestFirst=true;
function render05(){
  const panel=$('#panel-05');
  const entries=W.log.split(/(?=^## )/m).filter(s=>s.trim());
  if(logNewestFirst) entries.reverse();
  let h='<h2>What has changed, where do the sources disagree, and how do I take it away?</h2>';
  h+='<div style="margin:8px 0"><button class="btn" data-action="log-order">Order: '+(logNewestFirst?'newest first':'oldest first')+'</button></div>';
  h+='<h3>Log</h3>';
  entries.forEach(e=>{
    const head=e.split('\n')[0];
    const sess=S.logAdded.some(s=>head.includes(s.slice(3)));
    h+='<details'+(sess?' open':'')+'><summary>'+esc(head)+(sess?'<span class="session-tag">this session</span>':'')+'</summary><div class="body">'+renderMd(e.split('\n').slice(1).join('\n'))+'</div></details>';
  });
  h+='<h3>Tensions register</h3>';
  tensionsEntries().forEach(e=>{
    const head=e.split('\n')[0];
    const m=e.match(/card:\s*\[\[([^\]]+)\]\]/);
    h+='<details><summary>'+esc(head)+(m?' · card: '+linkSlug(m[1]):'')+'</summary><div class="body">'+renderMd(e.split('\n').slice(1).join('\n'))+'</div></details>';
  });
  h+='<h3>Method</h3><p class="note">Counting, filtering, sorting, matching and pin verification are done by this page\'s code, deterministically; every number above has its "How this is computed" line. The model is called only when you press Ask, Ingest or a retry button, and each call announces what leaves the browser. Data: '+esc(W.source)+' · built '+esc(W.built)+' · '+D.length+' library documents.</p>';
  h+='<div style="margin:14px 0"><button class="btn primary" data-action="download-json">Download the wiki</button> '+(S.changesList.length?'<button class="btn" data-action="download-md">Download the changed pages (markdown)</button>':'')+'</div>';
  panel.innerHTML=h;
}
```

Header render:

```js
function renderHeader(){
  const byType={}; P.forEach(p=>byType[p.type]=(byType[p.type]||0)+1);
  const totalPins=P.reduce((n,p)=>n+p._pins.length,0);
  const ver=P.reduce((n,p)=>n+p._pins.filter(pn=>verify(pn).ok).length,0);
  const inbox=D.filter(d=>d.status==='inbox').length;
  $('#hdr-meta').textContent=P.length+' pages ('+(byType.source||0)+' sources, '+(byType.concept||0)+' concepts, '+(byType.entity||0)+' entities, '+(byType.question||0)+' questions) · '+totalPins+' pins, '+ver+' verified by this page · '+D.length+' documents, '+inbox+' in the inbox · built '+W.built;
  renderCounters();
}
function renderCounters(){ $('#hdr-counters').textContent='Changes this session: '+S.changes+' · Calls to the model: '+S.calls+' · Passages that left the browser: '+S.passages; }
$('#foot').textContent=W.source+' · built '+W.built+' · Counting, matching and verification are done by this page\'s code; the model is called only when you press Ask, Ingest or a retry button.';
```

askModel:

```js
async function askModel(prompt,opts){
  opts=opts||{};
  S.calls++; S.passages+=opts.passages||0; renderCounters();
  let raw='';
  try{ raw=await studio.ask(prompt,{json:true}); }
  catch(e){ return {error:String(e),raw:'',json:null}; }
  const txt=String(raw).trim();
  let json=null;
  try{ json=JSON.parse(txt); }
  catch(e){ const m=txt.match(/```(?:json)?\s*([\s\S]*?)```/); if(m){ try{json=JSON.parse(m[1]);}catch(e2){} } }
  return {raw:txt,json,error:null};
}
```

Delegation handler — big switch:

```js
document.addEventListener('click',e=>{
  const t=e.target.closest('[data-action]'); if(!t)return;
  const a=t.dataset.action;
  if(a==='tab') switchTab(t.dataset.tab);
  else if(a==='open-page'){ openPage(t.dataset.slug); }
  else if(a==='pin-open'){ studio.openSource(t.dataset.id,+t.dataset.page,t.dataset.quote); }
  else if(a==='pin-toggle'){ const pin=t.closest('.pin'); const d=pin.querySelector('.pin-detail'); d.hidden=!d.hidden; t.setAttribute('aria-expanded',String(!d.hidden)); }
  else if(a==='copy-page'){ copyPage(t.dataset.slug); }
  else if(a==='ask'){ runAsk(); }
  else if(a==='ask-retry'){ runAsk(); }
  else if(a==='ask-stop'||a==='stop'){ S.stop=true; }
  else if(a==='ask-pages-toggle'){ $('#ask-pages').hidden=!$('#ask-pages').hidden; }
  else if(a==='ask-pages-apply'){ const sel=[...document.querySelectorAll('#ask-pages input:checked')].map(i=>i.value); if(sel.length) ask.slugs=sel.slice(0,8); runAskStep2($('#ask-q').value.trim()); }
  else if(a==='ask-file-open'){ renderFiling(); }
  else if(a==='ask-file'){ fileQuestion(); }
  else if(a==='ask-copy'){ copyText(ask.answer.answer); }
  else if(a==='ingest-start'){ startIngest(t.dataset.id); }
  else if(a==='ingest-run'){ startBatches(); }
  else if(a==='ingest-draft-source'){ draftSource(); }
  else if(a==='ingest-draft-touched'){ draftAllTouched(); }
  else if(a==='approve'){ ing.decisions[t.dataset.key]='approved'; render03(); }
  else if(a==='reject'){ ing.decisions[t.dataset.key]='rejected'; render03(); }
  else if(a==='ingest-file'){ fileIngest(); }
  else if(a==='lint'){ S.linted=true; render04(); }
  else if(a==='log-order'){ logNewestFirst=!logNewestFirst; render05(); }
  else if(a==='download-json'){ downloadJson(); }
  else if(a==='download-md'){ downloadMd(); }
});
```

openPage:

```js
function openPage(slug){ if(!bySlug[slug])return; S.page=slug; S.tab='01'; if(location.hash!=='#'+slug) location.hash=slug; switchTab('01'); }
window.addEventListener('hashchange',()=>{ const s=location.hash.slice(1); if(s&&bySlug[s]&&s!==S.page){ S.page=s; switchTab('01'); } });
```

switchTab calls render01 etc. — but switchTab('01') re-renders; fine.

Tablist keyboard:

```js
$('#tabs').addEventListener('keydown',e=>{
  if(!['ArrowRight','ArrowLeft','Home','End'].includes(e.key))return;
  const tabs=[...$('#tabs').querySelectorAll('[role=tab]')];
  let i=tabs.indexOf(document.activeElement); if(i<0)return;
  e.preventDefault();
  if(e.key==='ArrowRight')i=(i+1)%tabs.length; else if(e.key==='ArrowLeft')i=(i-1+tabs.length)%tabs.length; else if(e.key==='Home')i=0; else i=tabs.length-1;
  tabs[i].focus(); tabs[i].click();
});
document.addEventListener('keydown',e=>{ if(e.key==='Escape') S.stop=true; });
```

Init:

```js
renderHeader();
const h0=location.hash.slice(1); if(h0&&bySlug[h0]) S.page=h0;
switchTab('01');
$('#tabbtn-01').focus();
```

Wait switchTab renders all tabs? I'll make switchTab render only the target tab. render02: mostly static; but need to reset? Keep static; render02() can be a no-op or restore previous output — I'll keep ask-out persistent (don't clear on tab switch). So render02 = no-op. render03/04/05 render on switch.

Now the ingest functions in full:

```js
function startIngest(id){
  ing.docId=id; ing.calls0=S.calls; ing.pass0=S.passages;
  const doc=byId[id]; ing.batches=[];
  for(let i=0;i<doc.passages.length;i+=25) ing.batches.push(doc.passages.slice(i,i+25));
  ing.progText='ready · scope set';
  render03();
}
function setProg(t){ ing.progText=t; const el=$('#ing-prog'); if(el) el.textContent=t+' · calls so far '+(S.calls-ing.calls0)+' · passages sent '+(S.passages-ing.pass0); }
async function startBatches(){
  if(ing.running)return;
  ing.running=true; ing.started=true; S.stop=false; markRunning();
  const doc=byId[ing.docId];
  for(let i=0;i<ing.batches.length;i++){
    if(S.stop) break;
    setProg('batch '+(i+1)+' of '+ing.batches.length+' · '+(i*25)+' of '+doc.passages.length+' passages have left the browser');
    const b=ing.batches[i];
    const pj=JSON.stringify(b.map(p=>({id:p.id,page:p.page,paragraph:p.paragraph,section:p.section,text:p.text})));
    const prompt='You are ingesting '+citeAs[ing.docId]+' ('+(doc.symbol||doc.author+' '+doc.year)+', '+doc.title+') into a research wiki on neurotechnology in the administration of justice.\n\nIndex (one line per page):\n'+W.index+'\n\nPassages, verbatim from the PDF (JSON array):\n'+pj+'\n\nReturn JSON only: {"takeaways":[{"claim":"…","quote":"8–40 words copied verbatim from that one passage","passage":"the passage id","pages":["slugs from the index the claim bears on"]}]}, at most 10 takeaways. Pin syntax: [label](pin:id#pPAGE "quote") ✓ — quote only words that stand in the passages given; the code will check.';
    const r=await askModel(prompt,{passages:b.length});
    if(S.stop) break;
    if(!r.json||!Array.isArray(r.json.takeaways)){ ing.progText='batch '+(i+1)+' did not return JSON — raw answer kept below; press Start again to retry'; ing.raw=r.raw; render03(); continue; }
    for(const t of r.json.takeaways){
      const passage=b.find(p=>p.id===t.passage);
      if(!passage){ ing.dropped++; continue; }
      const pinStr=makePin(ing.docId,passage,t.quote||'');
      const pin=parsePinStr(pinStr);
      const v=verify(pin);
      const pages=(Array.isArray(t.pages)?t.pages:[]).filter(s=>allowNew(s));
      if(v.ok) ing.takeaways.push({claim:t.claim,quote:t.quote,passage,pin:pinStr,pages});
      else ing.failed.push({claim:t.claim,quote:t.quote,passage,pin:pinStr,reason:v.reason,nearest:nearestPassage(doc,pin.page,t.quote||'')});
    }
    render03();
  }
  ing.running=false; markRunning();
  setProg('step 1 done · '+ing.takeaways.length+' takeaways verified · '+ing.failed.length+' could not be verified'+(S.stop?' · stopped early':''));
  render03();
}
```

parsePinStr: use PIN_RE on string: `const m=pinStr.match(new RegExp(PIN_RE.source))` — PIN_RE has /g; create fresh: `pinStr.match(/\[([^\]]+)\]\(pin:([^#\s)]+)#p(\d+)(?: "([^"]*)")?\) ?(✓|⚠)/)`.

allowNew:

```js
function allowNew(s){ if(bySlug[s])return true; if(ing.newSlugs.length<2&&!ing.newSlugs.includes(s)){ ing.newSlugs.push(s); return true; } return false; }
```

nearestPassage:

```js
function nearestPassage(doc,page,quote){
  let best=null,bestRun=0;
  doc.passages.filter(p=>p.page===page).forEach(p=>{ const r=commonRun(quote,p.text); if(r>bestRun){bestRun=r;best=p;} });
  return best?{passage:best,run:bestRun}:null;
}
```

draftSource:

```js
async function draftSource(){
  if(ing.running)return; ing.running=true; S.stop=false; markRunning();
  const doc=byId[ing.docId];
  setProg('drafting the source page · 1 call');
  const tks=ing.takeaways.map(t=>({claim:t.claim,pin:t.pin}));
  const stub=P.find(p=>p.frontmatter.status==='stub'&&p.frontmatter.sources.includes(ing.docId));
  const prompt='Draft the source page for a new library document in a research wiki on neurotechnology in the administration of justice.\n\nFull cite: '+(doc.symbol||doc.author+' '+doc.year)+' — '+doc.title+' ('+doc.kind+', '+doc.published+', '+doc.url+', '+doc.pages+' PDF pages). Register: '+(stub?(stub.frontmatter.register||[]).join(''):'?')+' ('+((stub&&stub.frontmatter.register||[]).map(r=>REG_NAMES[r]).join(', '))+').\n\nVerified takeaways with ready-made pins (copy the pins exactly, character for character):\n'+JSON.stringify(tks)+'\n\nThe schema\'s source-page anatomy: Full cite · Register · One-liner · Key takeaways · How NOT to read this · Where it feeds the wiki · Related.\n\nReturn JSON only: {"one_liner":"…","body":"markdown, at most 900 words, only the pins given, copied exactly","touches":[{"slug":"…","why":"…"}]}, at most 12 touches, slugs from the index or new slugs. Pin syntax: [label](pin:id#pPAGE "quote") ✓ — quote only words that stand in the passages given; the code will check.';
  const r=await askModel(prompt,{});
  ing.running=false; markRunning();
  if(!r.json||typeof r.json.body!=='string'){ ing.progText='source-page draft did not return JSON'; ing.raw=r.raw; render03(); return; }
  const body=r.json.body;
  const pins=[...body.matchAll(PIN_RE)].map(m=>({label:m[1],id:m[2],page:+m[3],quote:m[4]||'',mark:m[5]}));
  const ver=pins.filter(p=>verify(p).ok).length;
  const slug=uniqueSlug(kebab(doc.short_title||doc.title));
  const links=[...new Set([...body.matchAll(WLINK_RE)].map(m=>m[1]))];
  const touches=(Array.isArray(r.json.touches)?r.json.touches:[]).map(t=>t.slug).filter(s=>bySlug[s]||allowNew(s)).slice(0,12);
  if(stub&&!touches.includes(stub.slug)) touches.push(stub.slug);
  ing.sourceDraft={slug,title:doc.title,one_liner:r.json.one_liner||'',body,inserted:[body],pins,ver,notVer:pins.length-ver,touches,
    frontmatter:{title:doc.title,type:'source',tags:touches.slice(0,8),register:stub?(stub.frontmatter.register||[]):[],status:'reviewed',updated:today(),links,sources:[ing.docId]}};
  setProg('source page drafted · '+pins.length+' pins, '+ver+' verified, '+(pins.length-ver)+' not verified');
  render03();
}
```

draftAllTouched:

```js
async function draftAllTouched(){
  if(ing.running)return; ing.running=true; S.stop=false; markRunning();
  const slugs=touchedSlugs();
  for(let i=0;i<slugs.length;i++){
    if(S.stop)break;
    const slug=slugs[i];
    setProg('drafting changes to page '+(i+1)+' of '+slugs.length+' ('+slug+')');
    const page=bySlug[slug]||null;
    const tks=ing.takeaways.filter(t=>t.pages.includes(slug)).map(t=>({claim:t.claim,pin:t.pin}));
    const base=page?('Existing page [['+slug+']] — '+page.title+'\n\nBody:\n'+page.body+'\n\n'):('New page to create: '+slug+'\n\n');
    const prompt=base+'New verified takeaways from '+citeAs[ing.docId]+' (pins ready-made, copy exactly):\n'+JSON.stringify(tks)+'\n\nReturn JSON only: {"edits":[{"after":"an existing heading of the page, or \"end\"","markdown":"at most 300 words in all across edits, pins copied exactly"}],"contested":"a full ```contested block only where this document disagrees with the page, else null"}. Pin syntax: [label](pin:id#pPAGE "quote") ✓ — quote only words that stand in the passages given; the code will check.';
    const r=await askModel(prompt,{});
    if(!r.json||!Array.isArray(r.json.edits)){ ing.progText='draft for '+slug+' did not return JSON'; ing.raw=r.raw; render03(); continue; }
    let body=page?page.body:'# '+slug+'\n';
    const inserted=[];
    for(const e of r.json.edits){ if(!e||typeof e.markdown!=='string')continue; const res=insertAfterHeading(body,e.after||'end',e.markdown); body=res.body; inserted.push(e.markdown); }
    if(r.json.contested&&typeof r.json.contested==='string'){ body+='\n\n'+r.json.contested.replace(/^```|```$/g,'')+'\n'; }
    const fm=page?{...page.frontmatter}:{title:slug,type:'concept',tags:[],register:[],status:'draft',updated:today(),links:[],sources:[]};
    fm.links=[...new Set([...(fm.links||[]),...([...body.matchAll(WLINK_RE)].map(m=>m[1]))])];
    fm.sources=[...new Set([...(fm.sources||[]),ing.docId])];
    fm.updated=today();
    const pins=[...body.matchAll(PIN_RE)].map(m=>({label:m[1],id:m[2],page:+m[3],quote:m[4]||'',mark:m[5]}));
    const oldKeys=page?new Set(page._pins.map(p=>p.id+'#p'+p.page+'|'+p.quote)):new Set();
    const added=pins.filter(p=>!oldKeys.has(p.id+'#p'+p.page+'|'+p.quote));
    ing.drafts[slug]={body,frontmatter:fm,inserted,pins,added,addedVer:added.filter(p=>verify(p).ok).length,contested:!!r.json.contested};
    if(!ing.order.includes(slug)) ing.order.push(slug);
    render03();
  }
  ing.running=false; markRunning();
  setProg('drafts done · '+ing.order.length+' pages touched');
  render03();
}
```

fileIngest:

```js
function fileIngest(){
  const doc=byId[ing.docId];
  const approved=[], rejected=[];
  if(ing.sourceDraft&&ing.decisions.__new__==='approved'){
    const slug=ing.sourceDraft.slug;
    const page={slug,type:'source',title:ing.sourceDraft.title,frontmatter:ing.sourceDraft.frontmatter,body:ing.sourceDraft.body};
    P.push(page); bySlug[slug]=page; prep(page); approved.push(slug);
  }
  ing.order.forEach(slug=>{ if(ing.decisions[slug]==='approved'){ const d=ing.drafts[slug], p=bySlug[slug]; p.body=d.body; p.frontmatter=d.frontmatter; prep(p); approved.push(slug); } else if(ing.decisions[slug]==='rejected') rejected.push(slug); });
  // index
  const totalPins=P.reduce((n,p)=>n+p._pins.length,0);
  W.index=W.index.replace(/(\d[\d,]*) pins/, totalPins.toLocaleString('en-US')+' pins');
  approved.forEach(slug=>upsertIndexLine(slug));
  if(ing.sourceDraft&&ing.decisions.__new__==='approved') upsertIndexLine(ing.sourceDraft.slug);
  // log
  const cite=citeAs[ing.docId], reg=registerOfDoc(ing.docId);
  const pinnedOn=P.filter(p=>p.slug!==ing.sourceDraft?.slug&&p._pins.some(pn=>pn.id===ing.docId)).map(p=>p.slug);
  const logEntry='## ['+today()+'] ingest | '+(doc.symbol||ing.docId)+': '+(doc.short_title||doc.title)+'\n\nRead '+doc.passages.length+' passages ('+cite+', register ('+reg+')). '+(approved.length?'Wrote '+approved.map(s=>'[['+s+']]').join(', ')+'.':'Nothing approved.')+' '+totalPins+' pins in all; besides its own page, pinned on '+pinnedOn.length+' pages: '+pinnedOn.map(s=>'[['+s+']]').join(', ')+'. Rejected: '+(rejected.length?rejected.map(s=>'[['+s+']]').join(', '):'none')+'.';
  W.log+='\n'+logEntry+'\n'; S.logAdded.push(logEntry.split('\n')[0]);
  // tensions for new contested cards
  ing.order.forEach(slug=>{ const d=ing.drafts[slug]; if(d&&d.contested&&ing.decisions[slug]==='approved'){ W.tensions+='\n### '+kebab(slug)+'-contested\n\nstatus: open\ncard: [['+slug+']]\n\n'; } });
  doc.status='ingested';
  S.changes+=approved.length; approved.forEach(s=>S.changesList.push(s));
  ing.filed=true; ing.progText='filed · lint re-run below';
  S.lint=computeLint();
  renderHeader(); render03();
}
```

upsertIndexLine:

```js
function upsertIndexLine(slug){
  const p=bySlug[slug]; if(!p)return;
  const n=p._pins.filter(pn=>verify(pn).ok).length;
  const line='- [['+slug+']] — '+(p.frontmatter.title||p.title).slice(0,80)+' · ('+(p.frontmatter.register||[]).join('')+') · ✓'+n;
  const re=new RegExp('- \\[\\['+slug.replace(/[.*+?^${}()|[\]\\]/g,'\\$&')+'\\]\\][^\\n]*');
  if(re.test(W.index)) W.index=W.index.replace(re,line);
  else W.index+='\n'+line;
}
```

markRunning: update tab 03 label:

```js
function markRunning(){ const b=$('#tabbtn-03'); b.innerHTML='03 Ingest'+(ing.running?' <span class="run" aria-live="polite">· running</span>':''); }
```

render03 full:

```js
function render03(){
  const panel=$('#panel-03');
  if(!ing.docId){ ...as above...; return; }
  const doc=byId[ing.docId];
  let h='<h2>Ingest '+esc(doc.symbol||doc.id)+'</h2><div class="note">'+esc(doc.short_title||doc.title)+' · '+doc.kind+' · '+doc.passages.length+' passages · status: '+doc.status+'</div>';
  h+='<div class="progress" id="ing-prog" aria-live="polite">'+esc(ing.progText||'ready')+' · calls so far '+(S.calls-ing.calls0)+' · passages sent '+(S.passages-ing.pass0)+'</div>';
  if(ing.running) h+='<button class="btn" data-action="stop">Stop</button>';
  // step 1
  h+='<div class="step"><h3>01 · Scope</h3>';
  if(!ing.started){
    const n=doc.passages.length, calls=Math.ceil(n/25), chars=doc.passages.reduce((s,p)=>s+p.text.length,0);
    h+='<p>All '+n+' passages will be sent, in batches of 25 ('+calls+' calls), '+chars.toLocaleString('en-US')+' characters; nothing is held back.</p>';
    h+='<table><caption>FIG.01 · Batches — every passage is sent exactly once</caption><thead><tr><th scope="col">batch</th><th scope="col">paragraphs</th><th scope="col">PDF pages</th><th scope="col" class="num">passages</th></tr></thead><tbody>';
    ing.batches.forEach((b,i)=>{ h+='<tr><td>'+(i+1)+'</td><td>'+esc(String(b[0].paragraph??'—'))+' – '+esc(String(b[b.length-1].paragraph??'—'))+'</td><td>'+b[0].page+'–'+b[b.length-1].page+'</td><td class="num">'+b.length+'</td></tr>'; });
    h+='</tbody></table><button class="btn primary" data-action="ingest-run">Start</button>';
  } else {
    h+='<p class="note">Batches run one after another; Stop keeps what has returned. Passages sent so far: '+(S.passages-ing.pass0)+' of '+doc.passages.length+'.</p>';
  }
  h+='</div>';
  // step 2
  h+='<div class="step"><h3>02 · Takeaways</h3>';
  if(ing.takeaways.length||ing.failed.length){
    h+='<table><caption>FIG.02 · Takeaways — each quote re-verified by this page against the library</caption><thead><tr><th scope="col">claim</th><th scope="col">quote</th><th scope="col">passage</th><th scope="col">pages</th><th scope="col">verification</th></tr></thead><tbody>';
    ing.takeaways.forEach(t=>{ h+='<tr><td>'+esc(t.claim)+'</td><td class="pin-quote">“'+esc(t.quote)+'”</td><td>'+esc(t.passage.paragraph!=null?'para. '+t.passage.paragraph:'p. '+t.passage.page_label)+' · PDF p. '+t.passage.page+'</td><td>'+t.pages.map(esc).join(', ')+'</td><td class="ok">✓ verified</td></tr>'; });
    h+='</tbody></table>';
    if(ing.failed.length){
      h+='<div class="card"><strong class="warn">Could not verify: '+ing.failed.length+'</strong><ul>';
      ing.failed.forEach(f=>{ h+='<li>'+esc(f.claim)+' — quote “'+esc(f.quote)+'” ('+esc(f.reason||'')+')'+(f.nearest?' · nearest passage on that page: para. '+(f.nearest.passage.paragraph??f.nearest.passage.page_label)+', shared run '+f.nearest.run+' words':'')+' <button class="chip" data-action="pin-open" data-id="'+esc(ing.docId)+'" data-page="'+f.passage.page+'" data-quote="'+esc(f.quote)+'">Open the PDF page</button></li>'; });
      h+='</ul><p class="note">These claims are in no change card and in no later prompt.</p></div>';
    }
  } else h+='<p class="note">No takeaways yet — run step 01.</p>';
  h+='</div>';
  // step 3
  h+='<div class="step"><h3>03 · Drafts</h3>';
  if(ing.takeaways.length){
    h+='<div style="margin:6px 0"><button class="btn" data-action="ingest-draft-source" '+(ing.running?'disabled':'')+'>Draft the source page (1 call)</button></div>';
    if(ing.sourceDraft){
      const ts=touchedSlugs();
      h+='<p class="note">Source page drafted: '+ing.sourceDraft.pins.length+' pins, '+ing.sourceDraft.ver+' verified, '+ing.sourceDraft.notVer+' not verified. Touches: '+ts.map(esc).join(', ')+'.</p>';
      h+='<div style="margin:6px 0"><button class="btn" data-action="ingest-draft-touched" '+(ing.running?'disabled':'')+'>Draft the changes to '+ts.length+' pages ('+ts.length+' calls)</button></div>';
    }
  } else h+='<p class="note">Waiting on step 02.</p>';
  if(ing.raw) h+='<details><summary>Raw model answer (parse failure)</summary><pre data-source="ai">'+esc(ing.raw)+'</pre></details>';
  h+='</div>';
  // step 4
  h+='<div class="step"><h3>04 · Review and file</h3>';
  const keys=[...(ing.sourceDraft?['__new__']:[]),...ing.order];
  if(keys.length){
    const decided=keys.filter(k=>ing.decisions[k]).length;
    h+='<p class="note">change '+decided+' of '+keys.length+' decided · nothing is written until Approve is pressed</p>';
    keys.forEach((k,i)=>{ h+=changeCard(k,i+1,keys.length); });
    if(decided===keys.length&&!ing.filed) h+='<button class="btn primary" data-action="ingest-file">File the approved changes</button>';
    if(ing.filed) h+='<p class="ok">Filed. The document is now ingested; lint re-run on tab 04.</p>';
  } else h+='<p class="note">No drafts yet.</p>';
  h+='</div>';
  panel.innerHTML=h;
}
```

changeCard as above.

Ask step1 render:

```js
function renderAskStep1(q){
  const out=$('#ask-out');
  let h='<div class="note">Step 1 chose these pages:</div><div>';
  ask.slugs.forEach(s=>{ h+='<span class="chip" style="cursor:default">'+esc(s)+'</span> '; });
  h+='<button class="btn" data-action="ask-pages-toggle">Change pages</button></div>';
  h+='<div id="ask-pages" hidden><p class="note">Tick the pages to send in step 2 (the model sees only these bodies):</p>';
  P.forEach(p=>{ h+='<label style="text-transform:none;letter-spacing:0;font-family:inherit"><input type="checkbox" value="'+esc(p.slug)+'" '+(ask.slugs.includes(p.slug)?'checked':'')+'> '+esc(p.title)+' <span class="dim">('+p.type+')</span></label>'; });
  h+='<button class="btn" data-action="ask-pages-apply">Apply pages and ask</button></div>';
  h+='<div class="progress" id="ask-prog" aria-live="polite"></div><div id="ask-answer"></div>';
  out.innerHTML=h;
}
```

Hmm — #ask-prog exists in static HTML; duplicating id. I'll restructure: static panel has #ask-out only; progress inside. Let me put prog inside ask-out flow. Simplify: static HTML has #ask-info, #ask-prog, #ask-out. renderAskStep1 writes into #ask-out only (chips + change pages). runAskStep2 writes answer into #ask-out too (append). Let me make renderAskAnswer write into #ask-out replacing? Keep: after step2, out.innerHTML = step1 chips + answer. I'll just have renderAskStep1 store html prefix. Simpler: runAskStep2 sets $('#ask-out').innerHTML = chipsHtml + answerHtml. I'll factor chipsHtml().

Filing card:

```js
function renderFiling(){
  const a=ask.answer; if(!a)return;
  const title=a.title||'Question';
  const slug=uniqueSlug(kebab(title));
  const pins=[...a.answer.matchAll(PIN_RE)].map(m=>({label:m[1],id:m[2],page:+m[3],quote:m[4]||'',mark:m[5]}));
  const allOk=pins.length>0&&pins.every(p=>verify(p).ok&&ask.sentPins.has(p.id+'#p'+p.page+'|'+p.quote));
  const links=[...new Set([...a.answer.matchAll(WLINK_RE)].map(m=>m[1]).filter(s=>bySlug[s]))];
  const sources=[...new Set(pins.map(p=>p.id))];
  const register=[...new Set(pins.map(p=>registerOfDoc(p.id)))].filter(r=>r&&r!=='?');
  const body=buildQuestionBody(title,a,links);
  let h='<div class="card"><strong>File as a question page</strong><div class="note">The code builds this page; the model wrote only the answer above.</div>';
  h+='<table><tbody>';
  h+='<tr><th scope="row">slug</th><td class="mono">'+esc(slug)+'</td></tr>';
  h+='<tr><th scope="row">type / status</th><td>question / draft · updated '+today()+'</td></tr>';
  h+='<tr><th scope="row">register</th><td>'+esc(register.join('')||'?')+'</td></tr>';
  h+='<tr><th scope="row">links</th><td>'+links.map(esc).join(', ')+'</td></tr>';
  h+='<tr><th scope="row">sources</th><td>'+sources.map(esc).join(', ')+'</td></tr>';
  h+='</tbody></table>';
  h+='<label for="ask-tags">tags (comma-separated)</label><input type="text" id="ask-tags" value="'+esc(ask.tags)+'">';
  h+='<details><summary>Preview the body the code builds</summary><pre>'+esc(body)+'</pre></details>';
  h+='<div style="margin:10px 0"><button class="btn primary" data-action="ask-file" '+(allOk?'':'disabled')+'>File this page</button> <button class="btn" data-action="ask-copy">Copy answer</button> <span class="note">'+(allOk?'every pin in the answer verifies and stands on the pages sent':'disabled until every pin in the answer verifies and stands on the pages sent ('+pins.filter(p=>!(verify(p).ok&&ask.sentPins.has(p.id+'#p'+p.page+'|'+p.quote))).length+' do not)')+'</span></div></div>';
  $('#ask-file').innerHTML=h;
  $('#ask-tags').addEventListener('input',e=>ask.tags=e.target.value);
}
```

buildQuestionBody:

```js
function buildQuestionBody(title,a,links){
  const m=a.answer.match(/^.{10,400}?[.!?](?:\s|$)/s);
  const short=m?m[0].trim():a.answer.slice(0,200);
  return '# '+title+'\n\n**Short answer.** '+short+'\n\n## Reasoning\n\n'+a.answer+'\n\n## What the library cannot answer\n\n'+(a.cannot_answer||'—')+'\n\n## Related\n\n'+(links.length?links.map(s=>'[['+s+']]').join(', '):'—');
}
```

fileQuestion:

```js
function fileQuestion(){
  const a=ask.answer; if(!a)return;
  const title=a.title||'Question';
  const slug=uniqueSlug(kebab(title));
  const pins=[...a.answer.matchAll(PIN_RE)].map(m=>({label:m[1],id:m[2],page:+m[3],quote:m[4]||'',mark:m[5]}));
  const links=[...new Set([...a.answer.matchAll(WLINK_RE)].map(m=>m[1]).filter(s=>bySlug[s]))];
  const sources=[...new Set(pins.map(p=>p.id))];
  const register=[...new Set(pins.map(p=>registerOfDoc(p.id)))].filter(r=>r&&r!=='?');
  const body=buildQuestionBody(title,a,links);
  const page={slug,type:'question',title,frontmatter:{title,type:'question',tags:(ask.tags||'').split(',').map(s=>s.trim()).filter(Boolean),register,status:'draft',updated:today(),links,sources},body};
  P.push(page); bySlug[slug]=page; prep(page);
  const n=page._pins.filter(pn=>verify(pn).ok).length;
  W.index+='\n- [['+slug+']] — '+title.slice(0,80)+' · ('+register.join('')+') · ✓'+n;
  const head='## ['+today()+'] ask | '+title;
  W.log+='\n'+head+'\n\nFiled from an Ask answer: '+page._pins.length+' pins, all verified by this page.\n';
  S.logAdded.push(head);
  S.changes++; S.changesList.push(slug);
  renderHeader(); render01();
  const el=$('#ask-file'); if(el) el.innerHTML='<p class="ok" aria-live="polite">Filed as [['+slug+']] — see tab 01. Download it on tab 05.</p>';
}
```

copyPage / copyText:

```js
function fmYaml(fm){ return '---\n'+Object.entries(fm).map(([k,v])=>k+': '+(Array.isArray(v)?'['+v.join(', ')+']':v)).join('\n')+'\n---\n'; }
function copyPage(slug){ const p=bySlug[slug]; copyText(fmYaml(p.frontmatter)+p.body); }
function copyText(t){ if(navigator.clipboard&&navigator.clipboard.writeText){ navigator.clipboard.writeText(t).then(()=>flash('Copied.'),()=>fallbackCopy(t)); } else fallbackCopy(t); }
function fallbackCopy(t){ const ta=document.createElement('textarea'); ta.value=t; document.body.appendChild(ta); ta.select(); try{document.execCommand('copy'); flash('Copied.');}catch(e){ flash('Copy failed — select and copy manually.'); } ta.remove(); }
function flash(msg){ const el=$('#hdr-counters'); const old=el.textContent; el.textContent=msg+' · '+old; setTimeout(renderCounters,1500); }
```

Downloads:

```js
function downloadJson(){
  const data={title:W.title,source:W.source,built:W.built,count:P.length,schema:W.schema,pages:P,index:W.index,log:W.log,tensions:W.tensions,changes:S.changesList,library_status:D.map(d=>({id:d.id,status:d.status}))};
  download('wiki-'+today()+'.json',JSON.stringify(data,null,2),'application/json');
}
function downloadMd(){
  const parts=S.changesList.map(slug=>{ const p=bySlug[slug]; return fmYaml(p.frontmatter)+p.body; });
  download('wiki-changed-'+today()+'.md',parts.join('\n\n---\n\n'),'text/markdown');
}
function download(name,text,type){ const b=new Blob([text],{type:type}); const a=document.createElement('a'); a.href=URL.createObjectURL(b); a.download=name; document.body.appendChild(a); a.click(); setTimeout(()=>{URL.revokeObjectURL(a.href); a.remove();},400); }
```

insertAfterHeading as planned.

makePin:

```js
function makePin(id,x,quote){
  const label=citeAs[id]+(x.paragraph!=null?', para. '+x.paragraph:', p. '+x.page_label);
  return '['+label+'](pin:'+id+'#p'+x.page+' "'+String(quote).replace(/"/g,'”')+'") ✓';
}
```

contestedHtml with tensions link:

```js
function contestedHtml(block,opts){
  const c=parseContested(block);
  const verdict=(c.verdict||'').replace(/-/g,' ');
  let wsum=0,wsup=0;
  (c.positions||[]).forEach(p=>{ const w=REG_W[p.register]??0; wsum+=w; if(p.sign==='+')wsup+=w; else if(p.sign==='~')wsup+=w/2; });
  const pct=wsum?Math.round(100*wsup/wsum):0;
  let rows=(c.positions||[]).map(p=>'<tr><td>'+(p.sign==='+'?'supports':p.sign==='-'?'contests':'mixed')+'</td><td class="mono">'+esc(p.register)+'</td><td>'+inline(p.pin||'',opts)+'</td><td>'+esc(p.gloss||'')+'</td><td>'+(p.page?inline(p.page,opts):'')+'</td></tr>').join('');
  const inT=opts&&opts.pageSlug&&tensionsCards().has(opts.pageSlug);
  return '<section class="contested"><h3>'+esc(c.claim||'Contested claim')+'</h3>'+
    '<p class="verdict">'+esc(verdict)+'</p>'+
    (c.note?'<p>'+esc(c.note)+'</p>':'')+
    '<div class="mono fig">FIG.01 · lean bar — descriptive: support '+pct+'% of weighted positions (weights a 5 · b 4 · c 3 · d 2 · e 1 · f ½); the verdict is the answer</div>'+
    '<div class="lean"><div style="width:'+pct+'%"></div></div>'+
    '<table><caption>Positions in this contested block</caption><thead><tr><th scope="col">sign</th><th scope="col">register</th><th scope="col">pin</th><th scope="col">gloss</th><th scope="col">page</th></tr></thead><tbody>'+rows+'</tbody></table>'+
    (inT?'<p class="note">Also <a href="#" data-action="tab" data-tab="05">in the tensions register (tab 05)</a>.</p>':'')+
    '</section>';
}
```

Note data-action="tab" on an <a href="#"> — click handler preventDefault? The handler doesn't preventDefault; href="#" would jump. Use button styled as link or add e.preventDefault() when a==='tab' and tag is A. I'll add: if(a==='tab'){ e.preventDefault(); switchTab(...) }.

renderMd opts.inserted handling for class ins/old: implement helper in renderMd:

```js
const mark = raw => !opts.inserted ? '' : (opts.inserted.some(m=>m.includes(raw)) ? ' class="ins"' : ' class="old"');
```

Apply to p, li, headings.

Also inline() needs opts passed through — yes.

One catch: PIN_RE with /g used with matchAll — fine; but reusing same regex object across matchAll calls: matchAll requires /g and doesn't mutate lastIndex? Actually String.prototype.matchAll clones the regex internally? No — matchAll uses the regex's lastIndex? Per spec, matchAll creates a new RegExp with same flags, so safe. Yes, matchAll internally constructs a new regex. OK.

verify uses pin.quote; for pins parsed from model output, quote may contain ” already — norm keeps capitals, curly quotes normalized to ". Good.

Edge: pin label check "para. 5 (a)" — label contains 'para. 5 (a)' if passage.paragraph==='5 (a)'. includes('para. 5 (a)') works.

Now the ASK step-2 "Change pages" — after apply, runAskStep2 re-sends. Fine.

Also "once there is an answer the same button reads 'Ask again'" — handled in finally.

Stop button in ask: data-action="ask-stop" → S.stop=true. In runAsk I check S.stop after calls. Also generic 'stop' for ingest.

render02: no-op (static). But switchTab('02') calls render02 — define as empty.

Also initial: switchTab('01') renders. Focus first tab.

Potential issue: render01 re-binds filter input each render — I'll structure render01 to build shell once and update list via updatePageList(). Let me write:

```js
function render01(){
  const panel=$('#panel-01');
  if(!panel.dataset.built){
    panel.innerHTML='<div class="layout"><aside class="rail"><label for="pg-filter">title, tag or slug</label><input type="text" id="pg-filter"><div class="bignum" id="pg-count"></div><div class="mono dim">pages · click = open</div><div id="pg-list"></div></aside><div class="content" id="pg-main"></div></div>';
    panel.dataset.built='1';
    $('#pg-filter').addEventListener('input',e=>{ filterQ=e.target.value; updatePageList(); });
  }
  updatePageList();
  $('#pg-main').innerHTML = S.page&&bySlug[S.page]? pageHtml(bySlug[S.page]) : indexHtml();
}
```

updatePageList computes shown and fills #pg-list and #pg-count.

indexHtml: '<h2>The index</h2><p class="note">…</p>'+renderMd(W.index,{}).

OK. Also pageHtml body wrapper class "body".

Now line count — likely ~1100-1300. Acceptable.

One more requirement: "Every row that shows a document has its symbol, linked to doc_url" — Sources section links short_title to url; add symbol: show doc.symbol linked. I'll include symbol in the source line: `<a href=url>symbol</a> short_title — kind, year`.

Also header right counters aria-live.

Also "A running step goes on when you change tab; its tab then reads '03 INGEST · running'" — markRunning handles.

Also tab 02 grey box initial text — set in HTML.

Also "Enter sends" — textarea keydown Enter (without shift) triggers ask:

```js
document.addEventListener('keydown',e=>{ if(e.key==='Enter'&&e.target.id==='ask-q'&&!e.shiftKey){ e.preventDefault(); runAsk(); } if(e.key==='Escape') S.stop=true; });
```

Now write everything out. Also careful: in template building I use string concat; ensure escaping of quotes in data attributes (esc handles ").

In pinHtml, data-quote attribute: esc(pin.quote) — good.

Let me also compute verified count for header once at load (707 pins × verify — each verify does norm of passage text; passages up to 652; fine).

Performance: verify called many times (render each page). Cache: pin._v = verify result memoized per pin object. Since pins are per-page objects created once in prep, memoize: in verify, attach pin._v. But pins created fresh in various places (answer pins). Add cache via WeakMap? Simple: in verify, if(pin._v) return pin._v; pin._v=result. But pin objects from matchAll in render are fresh each render — memoize on the string key instead: global Map vcache key=id|page|quote|label. Do that.

```js
const vcache=new Map();
function verify(pin){
  const key=pin.id+'|'+pin.page+'|'+pin.quote+'|'+pin.label;
  if(vcache.has(key))return vcache.get(key);
  ... compute res ...
  vcache.set(key,res); return res;
}
```

Good.

Now write final answer. Intro: 2-3 sentences. Then the html block. Nothing after.

Let me write the code in full now, being careful about syntax.

Also note: `renderMd` for log entries etc. uses inline which references opts — fine.

For the tab-02 static HTML, include grey box, prog, out, stop.

Writing render03 step 2 table: quote column may be long — fine.

Also add "How this is computed" lines near charts/numbers: tab01 big number has note; tab04 bignum note; lean bar labelled; takeaways table caption; lint table caption. Good.

Double-check clickables per view ≤7: tab01: 5 tabs + filter + copy = 7. OK.

Let me also make sure `hidden` attribute CSS rule included: `[hidden]{display:none!important}` — yes.

Now produce final code. I'll write it carefully in one pass.

One concern: in renderMd, headings regex allows up to 6 #; body uses ###. lvl = min(len+1,6) so h1→h2 etc. Fine.

In inline(), the pin branch: first alternative captures label etc. But note the regex alternation order: pin pattern first — good since it also starts with '['.

Bold `\*\*[^*]+\*\*` — labels inside pins contain no **. OK.

Italic `\*[^*\n]+\*` — could match across "a * b"? rare; fine.

Also plain links `[text](url)` — third alternative. But pin pattern also matches `[label](pin:...)` — first alternative wins. Wiki links second. Good.

In contested positions, p.pin is like `[A/81/351, para. 16](pin:...) ✓` — inline handles.

parseContested: position lines start with '+', '-', '~' followed by ' | '. My regex /^[+~\-]\s*\|/ — line is "+ c | [pin] ✓ | gloss | [[slug]]". Split on '|' gives ['+ c ', ' [pin] ✓ ', ' gloss ', ' [[slug]]']. parts[0]='+ c' — sign should be first char. I'll parse: sign=parts[0].trim()[0], register=parts[0].trim().slice(1).trim(). Let me handle: const head=parts[0].trim(); sign=head[0]; register=head.slice(1).trim().

OK, writing now. Also `esc` on undefined → ''.

For the ingest "Start" retry after parse failure: my loop `continue`s after storing raw; user presses Start again — but ing.started=true so Start button hidden. I'll show a "Retry batches" button when ing.raw set and not running: data-action="ingest-run" label "Retry". In render03 step1 else-branch: if ing.raw && !ing.running show retry button. And clear ing.raw at start of startBatches.

Also stop during ask: ask-stop sets S.stop; runAsk checks after each await.

Finally, initial focus: after switchTab('01'), call $('#tabbtn-01').focus().

Let me now also handle `switchTab` rendering: 

```js
function switchTab(t){
  S.tab=t;
  TABS.forEach(x=>{ $('#tabbtn-'+x).setAttribute('aria-selected',String(x===t)); $('#panel-'+x).hidden=(x!==t); });
  if(t==='01')render01(); else if(t==='03')render03(); else if(t==='04')render04(); else if(t==='05')render05();
}
```

render04 each time recomputes lint — fine (fast enough? 707 verifies cached; ok).

Write it all. Also add small "Credits" line? Sources consulted include external pages but no code copied with open licence requirement — the instruction says add Credits only if using code/wording from reference shelf excerpts with open licence. We didn't copy code. Skip.

Let me finalize the HTML now. I'll write ~compact.

Also: header meta uses "n pins, n verified by this page" — computed.

Potential pitfall: `W.index.match(/(\d[\d,]*) pins/)` — index first line states "707 pins". OK.

Time to write the final response.