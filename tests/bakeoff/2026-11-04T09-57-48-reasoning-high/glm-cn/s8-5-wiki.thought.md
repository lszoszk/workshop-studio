This is a huge spec. I need to build a complete single-file HTML app implementing the plan: five tabs (PAGES, ASK, INGEST, CHECK, RECORD), pin verification, markdown rendering, contested cards, lean bar, lint, ingest stepper with studio.ask, download. Must stay under ~1500 lines. That's tight for this feature set. I need to be economical while covering the essentials.

Let me plan the architecture:

**Data**: `W = WORKSHOP_DATA.wiki`, `LIB = WORKSHOP_DATA.library`. Compute at load: pages, pinMap per page, backlinks, docMap, registerOfDoc, citeAs map, verified counts.

**Core functions**:
- `norm(s)`: NFKC, quotes, dashes, hyphen+space removal, whitespace collapse.
- `parsePins(body)`: regex.
- `verifyPin(pin)`: find passage in doc with page, check fragments in order in norm(text), and label check. Return {ok, reason, passage}.
- `mdRender(body, opts)`: render markdown subset: headings #/##/###, bold, italic, bullets, numbered lists, [[slug]] links, plain links, pins → chips, contested fenced blocks → cards. For pins, need to handle the pin regex in the inline pass. Simplest: a line-based renderer; for each line, first extract pins into placeholders, then process inline markdown (bold, italic, links, wikilinks), then replace placeholders with chip HTML.

Pins display: show quote in quotation marks + chip (label button → studio.openSource, register letter, verified status words). Expandable detail via details/summary or a toggle. Use `<button>` for label; an arrow toggle for the detail. To keep clickables manageable — the spec says clickables counted are tabs/filter/buttons, not links in page text or pins. So it's fine.

**Contested card**: parse the fenced ```contested block: claim:, verdict:, note:, position lines. Lean bar: horizontal stacked bar (support red? accent). Actually lean = weighted support fraction. Show bar with percentage, label "descriptive...". Positions table with caption.

**Tab 01 PAGES**: left rail (filter box, big count, page list grouped by type), main column: index rendered (or page). location.hash = slug.

**Tab 02 ASK**: textarea, Ask button, two calls to studio.ask. Step 1: index + question → {pages}. Show chips with Change pages link (checkbox list). Step 2: bodies + question → {title, answer, cannot_answer}. Render answer with pins verified against sent pages. File as question page card: preview, disabled until all pins verify, File button, Copy answer.

**Tab 03 INGEST**: inbox documents list, Ingest button per doc. Stepper: step 1 scope (batches table, Start), step 2 takeaways (grows per batch, failed box), step 3 drafts (source page call + touched page calls), step 4 review (change cards, approve/reject, file). This is the biggest part. Need session counters, stop buttons, progress lines.

**Tab 04 CHECK**: big verified number, lint table (many checks), checks panel, Lint now button.

**Tab 05 RECORD**: log rendered newest first with switch, tensions register, method note, download buttons.

**Header**: as specified.

Session state: changes count, calls count, passages count.

Stop mechanism: a flag `stopRequested`; check between awaits.

studio.ask wrapper: `callModel(prompt)` — show chars, count calls, parse JSON with fallback strip fenced.

Given 1500-line budget, I must write compactly but readably. Let me estimate: CSS ~150 lines, HTML skeleton ~80, JS ~900-1000. Doable if I'm disciplined.

Let me write helper: `esc(s)` HTML escape.

Markdown renderer plan:

```js
function inline(s, ctx){ // ctx: {chips: []} for pins
  // handle pins first: replace with \x00i\x00 placeholder
  s = s.replace(PINRE, (m,label,id,page,quote,mark)=>{ ctx.chips.push({label,id,page:+page,quote,mark}); return '\x00'+(ctx.chips.length-1)+'\x00';});
  s = esc(s);
  s = s.replace(/\[\[([^\]]+)\]\]/g, (m,slug)=> wikiPage slugs has slug? `<a href="#slug" class="wl">`+title+`</a>` : `<span class="wl dangling">…</span>`);
  plain links: \[([^\]]+)\]\((https?:[^)]+)\)
  bold **x**, italic *x* — careful. Do bold first then italic with non-greedy.
  s = s.replace(/\x00(\d+)\x00/g, chip html)
}
```

Italic with single `*` could conflict with bold; do bold `\*\*(.+?)\*\*` → `<strong>`, then `\*(.+?)\*` → `<em>`. Acceptable.

Block-level: split body by lines; detect fenced blocks ```contested ... ``` ; headings `^#{1,3} `; bullets `^- `; numbered `^\d+\. `; else paragraph (accumulate until blank). Contested block: collect lines until closing ```.

Chip HTML:
```js
function chipHtml(pin){
  const v = verifyPin(pin); const doc = docMap[pin.id];
  const reg = docRegister(pin.id);
  // structure: <span class="pin"> "quote" <span class="pinchip"><button class="pinlabel" onclick openSource>label</button> <span class="reg">(c)</span> <span class="ver ok/bad">✓ verified</span> [page says] <button class="pinx" aria-expanded>▸</button></span><span hidden class="pindetail">…</span></span>
}
```
Detail: passage paragraph/page_label + first 300 chars + "Open the PDF page" button. Toggle via button click.

To avoid inline onclick complexity, I'll use event delegation on document for clicks on `[data-open]`, `[data-toggle]`, etc.

Pins: label button → studio.openSource(id, page, quote). Detail "Open the PDF page" also.

Verification result cache: `pinVer = new Map` keyed by id+page+quote.

`verifyPin(pin)`:
```js
const doc = docMap[pin.id]; if(!pin.quote) reason 'no quote'; if(!doc) 'unknown document';
if(doc.status==='inbox') 'document is in the inbox';
const frags = pin.quote.split(/\s*\.\.\.\s*|\s*\.\.\.\.\s*/) hmm split on "…" or "..." → pin.quote.split(/…|\.\.\./)
find passages of doc with page===pin.page; for each: t=norm(x.text); pos=0; all frags found in order (indexOf from pos). Then label check: if x.paragraph set → label.includes('para. '+x.paragraph) else label.includes('p. '+x.page_label). If text matches but label doesn't, keep searching other passages? Spec: verified when a passage exists such that fragments found AND label contains. So iterate passages, return first satisfying both. If none, not verified; keep reason.
```
Return {ok, passage (the matching one), reason}.

For the "nearest passage" for failed takeaways: passage on that page sharing longest run of consecutive normalized words. Implement `longestRun(quoteWords, textWords)` — O(n*m) could be heavy; use a simple approach with a map from word→indices. Passages are maybe 500 words, quotes 8-40 words. Simple DP fine.

**Register of document**: find source page with frontmatter.sources exactly [id] → its register; else stub page (the entity page with sources [id]? spec says "else of the stub page with that sources"). I'll implement: pages with sources length 1 containing id, take register; fallback '?'. For A/HRC/57/61, the stub a-hrc-57-61 has sources maybe [id]? It said stub has 11 pins all to other documents and is an entity page. Its frontmatter.sources might be ["A/HRC/57/61"]. The register of that page. OK, general rule covers it.

Register names: {a:'treaty law', b:'General Comments', c:'UN, agency and soft-law reports', d:'national human rights institution', e:'civil society', f:'scholarship'}. Weights {a:5,b:4,c:3,d:2,e:1,f:0.5}.

**citeAs(docId)**: most frequent text before ", para." or ", p." in existing pin labels to it; fallback symbol or author+year. Collect from all pages' pins.

**Index rendering** (tab 01 default view): render markdown of `wiki.index` like a page (no pins expected there, but wikilinks work).

**Lint checks** list:
1. dangling links
2. orphans (no backlinks and no bodyLinks? orphan = page with no backlinks; a page with no links in and no links out? Spec: "orphans 0" — page not linked from any other page presumably). I'll define orphan = no other page's bodyLinks include it.
3. pins not verified by code
4. pins marked ✓ that fail
5. sources ≠ pinned documents
6. pages with no pins
7. links not reciprocated (frontmatter.links vs body links differ)
8. pages missing from index / index lines without a page
9. index ✓N differing from computed
10. contested cards without tensions entry and reverse
11. stub pages
12. pins to inbox documents

Each check: {name, pages[], count}. Rendered as table rows "n · check" or "0 · pass".

Parsing index for `[[slug]]` and `✓N`: regex over index lines.

Tensions `card:` entries: `/card:\s*\[\[([^\]]+)\]\]/g`.

**Tab 02 details**:

Ask flow:
- textarea + Ask the wiki button.
- Step 1 prompt: index + question, ask for JSON {pages:[slug]}. Show progress line with Stop. On result: chips of slugs (up to 5, existing), "Change pages" link toggles a checkbox list of all pages. Then button "Ask the wiki" becomes... Spec: after step 1, proceed to step 2. I think flow: Ask → step1 → show chips + "Continue" or automatically step 2? Spec: "Step 1 sends the index and the question; the model returns up to five slugs, shown as chips with a Change pages link that lets you tick others. Step 2 sends those pages' bodies, announced as...". The button reads "Ask again" once there's an answer. So after step 1, need a way to trigger step 2 — probably a "Continue" button or the same button. I'll add a "Send these pages" button after chips shown. Clickables budget: 5 tabs + Ask + File as question page = 7 (8 with card open). Hmm, "Change pages" link + continue... The spec counts: "Ask the wiki, File as a question page = 7 (8 once the filing card is open)". So Change pages is a link (not counted?). I'll make Change pages a link-style button, and Continue as part of it. Simpler: after step 1, show chips and a "Change pages" link; a "Send these pages" button. I'll accept slight extra.

Actually, to keep to plan: the main button "Ask the wiki" could do step 1 then step 2 automatically (with a pause for Change pages?). The spec says chips shown with Change pages link, implying a pause. I'll do: step 1 → chips + "Change pages" link + main button now reads "Send these pages" (same button repurposed). Then step 2 → answer. Then button reads "Ask again". That keeps one button. 

- Step 2 prompt: bodies of chosen pages + question → {title, answer, cannot_answer}, answer ≤350 words. Render answer like a page inside data-source="ai". Pins in answer: accepted when same pin:id#pPAGE with same quote exists in a sent page's body and verify true; else struck through ("not on the pages sent"). Render: I can render answer with the same markdown renderer but with a "sentPins" set for validation. Pin chip in answer: register letter + name.

- Count line: verified pins by register.
- "File as a question page" button → opens card in place: preview (slug kebab unique, type question, tags input, register from pinned docs, status draft, updated today, links from [[slugs]] in answer, sources from pins; body built). "File this page" disabled until all pins verify, with reason. On file: add to pages, recompute, add index line under Questions, log entry `## [date] ask | title`. Message "Filed" aria-live.
- Copy answer button.

**Tab 03 ingest** details:

State machine per ingest session:
```js
ing = {doc, takeaways:[], failed:[], batches, batchIdx, results per batch, sourceDraft, touchedDrafts: [{slug, body, contested}], changes: [{slug, page(before/after), kind, approved}], phase}
```

- Inbox list: buttons "Ingest <symbol>".
- Step 1 scope panel: passages count, batches n = ceil(25), chars; table of batches (paragraph ranges, PDF pages). Start button.
- Run batches sequentially: prompt per batch: passages as {id,page,paragraph,text} + index + instruction → {takeaways:[{claim, quote, passage, pages}]}. Progress line "batch 2 of 4 · 50 of 100 passages have left the browser", Stop keeps returned.
- Step 2 table grows: claim, quote, passage (para & PDF page), pages chips, verification words. Failed box: "Could not verify: n" with model quote, nearest passage + run length, Open PDF page button.
- Step 3: "Draft the source page (1 call)" button → source page call. Then "Draft the changes to n pages (n calls)" button → per touched page call with progress + Stop. Stub always among them; its checklist sent along (send stub body which contains the checklist).
- Step 4: change cards (fieldset/legend): title, type, "new page"/"edited", counts of paragraphs inserted and pins added; page rendered with inserted paragraphs pale yellow. Approve/Reject buttons, "change 3 of 9" line. After last decision: "File the approved changes" button → apply: pages replaced/added, updated today, index updated, log appended, tensions updated, doc.status='ingested', lint re-run.

Rendering diffs: for edited pages, model returns edits [{after, markdown}] and contested. Code inserts markdown at end of heading's section. Track inserted paragraphs: I'll render the new body with markers. Simpler: during insertion, wrap inserted markdown in a marker like `<!--ins-->...<!--/ins-->`? But then the page body contains markers... Spec says inserted paragraphs on pale yellow. I can keep a parallel structure: build new body with inserted segments tracked in a list of the inserted strings; then when rendering the change card, render body and highlight paragraphs equal to inserted ones. Since inserted markdown becomes its own lines, I can mark lines. Approach: maintain `insRanges` — when constructing new body, insert `\x01` before inserted text and `\x02` after; keep the final body clean by stripping, but for rendering keep a version with markers. I'll store `marked` body and render with markers → wrap paragraph in span.ins. Strip markers for the real body.

Paragraph inserted count: count block-level elements in inserted markdown (headings/bullets/paragraphs). Approximate: count non-empty lines after splitting? I'll count blocks: split markdown into blocks by blank lines, count. Simple.

Pins added: pins in new body not in old body (count total, and verified/not verified in words).

New page cards: takeaways with new slugs (at most two new slugs per ingest become "new page" cards). New page body: hmm, for new slugs proposed by takeaways — the spec: "pages = slugs from the index the claim bears on ... plus at most two new slugs per ingest, which become 'new page' cards". How are new page bodies drafted? Probably via the touched-page call? Touched page call sends "the page's body" — for a new slug there is no body. Hmm. Maybe new page cards are drafted as part of... The spec doesn't detail new-page drafting. I'll handle: new slugs get touched-page calls too, with an empty body and instruction to create; treat as "new page" card. But spec says "Draft the changes to n pages (n calls)" where n = touched pages (existing slugs + up to 2 new). I'll include new slugs in touched calls with body "(new page)" instruction. The code then builds frontmatter for new pages: type "concept"? I'll set type "concept", register from doc register, sources [id], links from body. Fine.

Actually simpler and safer: allow new slugs in `pages` lists; include them in touched set; for the call, body = "" and prompt says this page does not exist yet, draft it. On return, edits with after 'end'. Card labeled "new page". Frontmatter built by code.

**Index line** update: "- [[slug]] — one-liner · (letters) · ✓N". For the source page, line under Sources section of index; replace stub's line; recompute N for touched pages; rebuild first line from counts. The index first line contains "/(\d[\d,]*) pins/" — rebuild: replace the pins number with new total. I'll do: `index = index.replace(/(\d[\d,]*) pins/, totalPins+' pins')` after changes. And counts of pages if stated — keep simple: only replace pins count.

Where in index: find "Sources" section heading (## Sources?) — I'll find the stub's line `- [[a-hrc-57-61]]...` and replace it; if source page line placement: replace stub line with new line. Touched pages' lines: replace `✓N` in their lines. Implement `updateIndexLine(slug, newline)` finds `/- \[\[slug\]\][^\n]*/`.

One-liner for source page: from model's one_liner.

**Log entry**: `## [today] ingest | symbol: short_title` + detail line as specified.

**Tensions entry** for new contested blocks: `### <slug-of-claim>` etc. slug-of-claim: kebab of claim. status mapping. poles/where from positions: poles = the +/- glosses? I'll write: poles: joined glosses of + and −; where: pages. Keep simple.

**Tab 05**: log rendered newest first, collapsible (details/summary per entry — but details elements fine). Switch flips order (button). Tensions register rendered as markdown with card: links opening page on tab 01. Entries added this session tagged "this session" in red. Download wiki JSON (with changes, library_status), second button (changed pages as markdown) once there are changes.

**Session tracking**: `session = {changes: [], calls: 0, passages: 0, logAdded: []}`. Header counters update via `renderHeader()`.

**Hash routing**: `location.hash = slug` → open page on tab 01. On hashchange, if hash is a slug, show tab 01 and that page. Tabs: also maybe hashes like `#tab-04`? Keep: hash = slug only.

**Tab labels with running mark**: when ingest running and user switches tab, tab 03 reads "03 INGEST · running". Manage via `updateTabLabels()`.

**Escape stops** running step: keydown Escape → stopRequested = true.

**aria-live** on progress lines and counters.

OK. Also "Copy page as markdown" button on tab 01: frontmatter as YAML + body. Use navigator.clipboard, fallback textarea select. Show "Copied".

Now write the code. I'll aim for compactness. Let me draft the CSS.

Design: paper #f4f0e8, ink #1d1b18, rules #d9d2c3, accent #9b2335. Serif Georgia. Mono labels. Tabs numbered. Focus ring red.

Let me now write the whole file mentally, section by section.

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Research wiki: neurotechnology in the administration of justice</title>
<style>
:root{--paper:#f4f0e8;--ink:#1d1b18;--rule:#d9d2c3;--acc:#9b2335;--ok:#1e6b34;--warn:#8a5a00;--bad:#a02318;}
[hidden]{display:none!important}
*{box-sizing:border-box}
body{margin:0;background:var(--paper);color:var(--ink);font:16px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}
...
```

Colors: verified green #1e6b34 (contrast on paper: dark green fine), amber #8a5a00, red for check #a02318 or accent. Pale yellow for inserted: #faf3d3.

Focus: `:focus-visible{outline:2px solid var(--acc);outline-offset:2px}`.

Layout: header sticky? "always visible" — I'll make it sticky top with paper bg. Tabs under header.

Grid for tab 01: `.cols{display:grid;grid-template-columns:320px 1fr;gap:32px}` collapse below 900px.

Now JS structure:

```js
const W = WORKSHOP_DATA.wiki, LIB = WORKSHOP_DATA.library;
const P = W.pages, D = LIB.records;
const pageBySlug = new Map(P.map(p=>[p.slug,p]));
const docById = new Map(D.map(d=>[d.id,d]));
const REGNAMES={a:'treaty law',b:'General Comments',c:'UN, agency and soft-law reports',d:'national human rights institution',e:'civil society',f:'scholarship'};
const REGW={a:5,b:4,c:3,d:2,e:1,f:0.5};
```

Per page compute: pins (parsed), bodyLinks, backlinks. Store in `meta = new Map(slug → {pins, links, back:Set})`.

norm:
```js
function norm(s){return s.normalize('NFKC').replace(/[“”„]/g,'"').replace(/[‘’]/g,"'").replace(/[–—]/g,'-').replace(/\u00AD/g,'').replace(/- /g,'').replace(/\s+/g,' ').trim();}
```
Wait: "a hyphen followed by whitespace → ''" — "decision- making" → "decisionmaking"? Spec says ("decision- making" = "decision-making"). Hmm: removing the hyphen+space gives "decisionmaking" which ≠ "decision-making". To make them equal, the passage side also normalizes: passage "decision-\nmaking" → norm → "decision- making"→ hyphen+space removed → "decisionmaking"; and pin quote "decision-making" → norm → "decision-making" (hyphen not followed by space stays). Those don't match! Unless we also remove hyphens entirely... The spec's norm: "a hyphen followed by whitespace → ''". So passage "decision- making" → "decisionmaking"; quote "decision-making" → "decision-making". Mismatch. Unless the pin quote would also be normalized the same way — pin quote "decision- making" → "decisionmaking". Both sides normalized the same, so both become "decisionmaking" when they have "- ". The equality "decision- making" = "decision-making" in spec is loose. Since both sides get the same norm, a pin quoting "decision-making" against a passage "decision- making" would fail. But spec claims 707 verify. Probably PDF hyphenation: passage has "decision-\nmaking" and pin quote uses "decision-making"? Then mismatch... unless norm removes hyphen before whitespace on both, and pin quote "decision-making" has no whitespace after hyphen so stays. Risky. Alternative interpretation: replace /-\s+/ with '' on passage and also treat "decision-making" vs "decisionmaking" — to be safe, I could additionally remove hyphens when comparing? That would over-match ("decision-making" vs "decision making"). Hmm.

The data description said "a hyphen followed by a space in 6" passages. The verification must handle those. Safest: in norm, replace `/-\s*/` ... Let me think: to make "decision- making" equal "decision-making", transform both by removing "- " (hyphen+whitespace) → "decisionmaking" vs "decision-making". Still differ. To make them equal you'd need to remove hyphens entirely in both: "decisionmaking" = "decisionmaking". ✓. But then "e-mail" vs "email" match — fine, low risk.

But the spec explicitly says `a hyphen followed by whitespace → ""`. If I apply exactly that to both sides: passage "decision- making"→"decisionmaking"; pin quote likely also written as "decision- making" (copied from passage with hyphen+newline→"- "?) Actually when the wiki was written, quotes were copied from passages; if passage text has "decision-\nmaking" (hyphen then newline), the quote in the pin might have "decision- making" or "decisionmaking" or "decision-making". The pin quotes are stored with the same source, so likely "decision-\nmaking" collapsed... In JSON the passage text contains "decision-\nmaking"? Then norm: /\s+/→' ' first? Order matters: spec order: soft hyphen removed; hyphen+whitespace→''; runs of whitespace→one space. So "-\n" → "-" + whitespace → removed → "decisionmaking". And the pin quote, if it contains "decision-making" (typed with plain hyphen), → stays "decision-making". Mismatch unless the pin quote also has the hyphen-space form.

Given uncertainty, the safest is: compare with a canonical form where hyphens adjacent to whitespace are removed AND also allow matching where one side has "- " and other has "-"? Overkill. I'll follow the spec exactly; if some pins fail, the lint shows them — acceptable? The user says "The 707 pins of the file I examined all verify by this rule." So follow the spec rule exactly. Trust it. OK: norm = NFKC, curly quotes → straight, dashes → "-", soft hyphen removed, then `replace(/- /g,'')`? "hyphen followed by whitespace" — use `/-\s/g,''`? If hyphen followed by newline: after NFKC, replace [–—]→'-', then /-\s+/→''. I'll use `replace(/-\s+/g,'')`. Then whitespace collapse, trim.

Hmm wait, that removes "- " anywhere, e.g., "dash - like" becomes "dashlike". Both sides same, fine.

PIN regex:
```js
const PINRE=/\[([^\]]+)\]\(pin:([^#\s)]+)#p(\d+)(?: "([^"]*)")?\) ?(✓|⚠)/g;
```

parsePins(body): collect matches with index.

verifyPin:
```js
const verCache=new Map();
function verifyPin(pin){
 const key=pin.id+'#'+pin.page+'|'+pin.quote;
 if(verCache.has(key))return verCache.get(key);
 let r={ok:false,reason:'',passage:null};
 const doc=docById.get(pin.id);
 if(!pin.quote){r.reason='the pin carries no quote';}
 else if(!doc){r.reason='unknown document '+pin.id;}
 else if(doc.status==='inbox'){r.reason='the document is still in the inbox';}
 else{
  const frags=pin.quote.split(/…|\.\.\./).map(norm).filter(f=>f.length);
  outer: for(const x of doc.passages){ if(x.page!==pin.page)continue;
   let t=norm(x.text),pos=0,ok=true;
   for(const f of frags){const i=t.indexOf(f,pos); if(i<0){ok=false;break;} pos=i+f.length;}
   if(!ok)continue;
   const labOk = x.paragraph!=null? pin.label.includes('para. '+x.paragraph) : pin.label.includes('p. '+x.page_label);
   if(labOk){r={ok:true,reason:'',passage:x};break outer;}
  }
  if(!r.ok)r.reason='no passage on PDF p.'+pin.page+' matches the quote and label';
 }
 verCache.set(key,r);return r;
}
```
Note: paragraph is a string like "32" or "50 (c)". 'para. '+x.paragraph works.

Edge: multiple passages on same page; label check may match a different one — fine.

docRegister(id): find page with sources exactly [id] → frontmatter.register (array); return array. Spec: register of document = register of source page whose sources is exactly [id]; else stub page with that sources; else "?". Same thing basically. Return array of letters or ['?'].

citeAs(id): tally prefixes of pin labels to id: label.match(/^(.*?), (?:para\.|p\.)/) take group 1; most frequent; fallback symbol or author+' '+year.

Rendering markdown:

```js
function renderMD(src, opts={}){
 // opts: {sentPins:Set of "id#page|quote" for ask-tab validation, struck handling}
}
```

Blocks: split into lines. Handle fenced: if line.trim()==='```contested' start collecting until line '```'. Headings: /^(#{1,4})\s+(.*)/. Lists: /^[-*]\s+/ and /^\d+\.\s+/. Paragraphs accumulate.

For each text line, inline processing:

```js
function inlineHTML(s,ctx){
 const chips=[];
 s=s.replace(PINRE,(m,label,id,page,quote,mark)=>{chips.push({label,id,page:+page,quote,mark});return '\x00'+(chips.length-1)+'\x00';});
 s=esc(s);
 s=s.replace(/\[\[([^\]|#]+)(?:\|[^\]]*)?\]\]/g,(m,slug)=>{
   const p=pageBySlug.get(slug);
   return p?`<a class="wl" href="#${esc(slug)}">${esc(p.title)}</a>`:`<a class="wl dang" href="#${esc(slug)}">${esc(slug)} <span class="dangnote">no page</span></a>`;
 });
 s=s.replace(/\[([^\]]+)\]\((https?:\/\/[^)\s]+)\)/g,'<a href="$2" target="_blank" rel="noopener">$1</a>');
 s=s.replace(/\*\*([^*]+)\*\*/g,'<strong>$1</strong>');
 s=s.replace(/(^|[^*])\*([^*]+)\*/g,'$1<em>$2</em>');
 s=s.replace(/\x00(\d+)\x00/g,(m,i)=>chipHTML(chips[+i],ctx));
 return s;
}
```

Careful: esc before replacements; the pin placeholders use \x00 so they survive esc. Wikilink pipe variant not needed but harmless.

chipHTML(pin, ctx):
```js
function chipHTML(pin,ctx){
 const doc=docById.get(pin.id);
 const v=ctx&&ctx.validate? ctxValidate... 
```
For ask answers: pin accepted if sentPins has id#page and same quote and verify ok; else render struck-through with "not on the pages sent". I'll pass ctx={answer:true, sent:Set}. In chipHTML:

```js
const v=verifyPin(pin);
let statusHtml, struck=false;
if(ctx&&ctx.sent){ struck=!(ctx.sent.has(pin.id+'#'+pin.page+'|'+pin.quote)&&v.ok); }
status = v.ok? '<span class="ver ok">✓ verified</span>' : '<span class="ver bad">⚠ not found</span>';
if(v.ok===false && pin.mark==='✓') add '<span class="ver">page says ✓</span>'
if(v.ok===true && pin.mark==='⚠') add 'page says ⚠'
```
Mark mismatch: show "page says ✓"/"page says ⚠" when differs.

Chip markup:
```html
<span class="pinw"><q class="pq">“quote”</q> <span class="chip">[<button class="plab" data-open="id|page|quote">label</button>] <span class="preg">(c)</span> status [page says] <button class="parr" data-pin="n" aria-expanded="false">▸</button></span><span class="pdetail" hidden>…</span></span>
```
Quotes display: wrap in “ ” (curly) for display. Details content: computed lazily on toggle: passage paragraph/page_label, first 300 chars, Open the PDF page button.

Simplify: build detail content at render time (we have v.passage when ok). For failed, show reason.

```html
<button class="plab" data-open>label</button> — opens studio.openSource(id,page,quote)
```
data-open value: JSON-ish `data-id data-page` and quote in data-q. Use attributes data-id, data-pg, data-q.

Toggle arrow: button with data-toggle on the wrapper id. Give each chip unique index via a global counter; store pin data in a global array `CHIPDB`. `<button data-chip="17" aria-expanded="false">▸</button>` and detail `<span id="cd17" hidden>`. Delegated click toggles.

For answer pins (struck): `<span class="pinw struck">` with note "not on the pages sent".

Contested block rendering:

```js
function contestedHTML(lines){
 let claim='',verdict='',note='',pos=[];
 for(const L of lines){
  if(L.startsWith('claim:'))claim=L.slice(6).trim();
  else if(L.startsWith('verdict:'))verdict=L.slice(8).trim();
  else if(L.startsWith('note:'))note=L.slice(5).trim();
  else if(/^[+~-]\s/.test(L)) pos.push(L);
 }
 // lean
 let sw=0,tw=0;
 const rows=pos.map(L=>{const [sign,reg,pinS,gloss,pageS]=L.split('|').map(x=>x.trim());
  const w=REGW[reg]||0; tw+=w; if(sign==='+')sw+=w; else if(sign==='~')sw+=w/2;
  ...});
 const pct=tw?Math.round(100*sw/tw):0;
```
Position line format: `~ c | [pin](pin:...) ✓ | gloss | [[slug]]`. Splitting on '|' breaks the pin? Pin contains `pin:id#p12 "quote"` — no pipe inside. Label could contain '|' unlikely. But the markdown link `[label](pin:...)` contains no pipes. OK. But gloss may contain pipes? Unlikely. Split with limit: split into 5 parts max: `L.split('|')` then rejoin extra parts into gloss? I'll split all and if length>5, join middle extras into gloss. Keep simple: parts = L.split('|').map(trim); sign=parts[0][0]; reg=parts[0].slice(2).trim(); Actually format: `+ c | pin | gloss | [[slug]]` — sign and register in first segment before first pipe. So parts[0]='+ c'. sign=parts[0][0], reg=parts[0].slice(1).trim(). Then pin part, gloss, page.

Verdict in words: verdicts like "leans-support" → display "leans support". Just replace '-' with ' '.

Lean bar: div with a filled portion width pct%, accent red for support. FIG label. Caption text with formula.

Positions table: caption "Positions", columns: sign in words (supports/contests/mixed), register, pin chip, gloss, page link.

Tensions link: check if tensions has `### ... card: [[thisslug]]`. In page render, contested cards get link "in the tensions register" that goes to tab 05. Implement: check W.tensions includes `[[slug]]` within a card line near... simpler: regex /card:\s*\[\[slug\]\]/.

**Page rendering (tab 01)**:

```js
function showPage(slug){ currentSlug=slug; render badges, body, links sections, copy button }
```

Badges: type, register letters with names, status, updated; tags.

Links out: frontmatter.links, mark "frontmatter only" when not in bodyLinks. Linked from: backlinks. Sources: frontmatter.sources with doc info.

Copy page as markdown: build YAML frontmatter from frontmatter object.

**Index view**: renderMD(W.index).

**Filter**: input filters list by title/tag/slug substring (lowercase). List grouped by type with group labels. Each item: title, register letters, pin count, "stub" tag.

**Tabs**: buttons with role=tab, arrow keys. `switchTab(i)`.

Hash routing: on load and hashchange: if hash matches a slug, switchTab(0) and showPage. When user clicks a page, set location.hash = slug (which triggers hashchange → showPage; guard to avoid loops).

**ASK implementation**:

```js
let ask={q:'',phase:'idle',slugs:[],answer:null,title:'',cannot:'',calls:0,stop:false};
```

callModel(prompt, label):
```js
async function callModel(prompt){
 session.calls++; renderHeader();
 const t0=Date.now();
 let raw=await studio.ask(prompt,{json:true});
 session... 
 let txt=raw||'';
 let j=null;
 try{j=JSON.parse(txt)}catch(e){ try{ j=JSON.parse(txt.replace(/^```[a-z]*\n?/,'').replace(/```\s*$/,'')) }catch(e2){} }
 return {json:j, raw:txt};
}
```
Spec: parse once more after stripping a fenced code block. OK.

Progress line with Stop: while awaiting, show "Calling the model · n characters sent …" plus Stop button setting stopFlag. Since we can't cancel the promise, Stop just prevents further processing. Fine.

Ask step 1 prompt:

```
You maintain a research wiki... INDEX: <index> QUESTION: ... Return JSON {"pages":["slug",...]} at most five slugs that exist in the index.
```

Step 2 prompt: bodies + question + instructions about pins: "Pins must be copied exactly from the pages given... name the register... Return JSON {title, answer, cannot_answer}".

Rendering the answer: renderMD(answer, {sent:Set}) inside `<div data-source="ai">`.

sent set built from chosen pages' pins: key id+'#'+page+'|'+quote.

Register count line: for verified accepted pins count by register letter.

File as question page:
- slug: kebab from title; ensure unique (append -2).
- tags: text input.
- register: union of pinned docs' registers.
- body built per spec.
- File button disabled until all pins verify (i.e., every pin in answer accepted & verified). Reason shown.
- On file: create page object {slug, type:'question', title, frontmatter:{...}, body}; push to P (array — but P is const referencing W.pages; push works). Update meta maps (recompute for new page). Add index line under Questions: find "## Questions" heading in index, insert after. Log: append `## [today] ask | title`. session.changes.push. Mark "Filed".

**INGEST implementation**:

```js
let ing=null; // {docId, passages, batches, bi, takeaways, failed, dropped, srcDraft, touched, changes, phase, stop}
```

Render function `renderIngest()` re-renders tab 03 content based on phase. Since tables grow, I'll re-render the panel each time (simplest).

Phases: 'pick' (inbox buttons), 'scope', 'batches' (running/done), 'takeaways' (after batches; shows table + failed; then step 3 buttons), 'source' (draft source page pending/done), 'touched' (running/done), 'review' (cards), 'filed'.

Buttons per phase as spec.

Takeaway call prompt per batch:

```
Passages (JSON): [{id,page,paragraph,text}...] — from batch
Index: ...
Task: identify at most 10 takeaways... quote 8–40 words copied verbatim from that one passage... pages = slugs from the index the claim bears on, may include up to two new slugs (kebab-case).
Pin syntax: [label](pin:ID#pPAGE "quote") ✓ — quote only words that stand in the passages given; the code will check.
Return JSON {"takeaways":[{"claim":..., "quote":..., "passage": id, "pages":[slug...]}]}
```

session.passages += batch length before/after? "passages sent k" — add batch size when sent. Also "Passages that left the browser" in header = session.passages. For ask, 0.

After each batch returns: for each takeaway: find passage by id among sent batch (coverage check: if passage id not in batch → dropped, counted). Build pin: label = citeAs + ', para. ' + paragraph (or ', p. ' + page_label); pin text `[label](pin:id#pPAGE "quote")` with quote's straight " made curly: replace /"..."? Spec: straight double quotes inside the quote become “ ” first. So quote.replace(/^"|"$/g?) Hmm: "straight double quotes inside the quote become “ ” first". The quote may contain " characters (from norm? no — raw). I'll do: q = quote; if it contains '"', replace pairs: simplest `q.replace(/"([^"]*)"/g,'“$1”')` and any remaining '"' → '”'. Actually simpler: replace all `"` with `”`? That breaks matching? The pin regex looks for `"([^"]*)"` so inner straight quotes break parsing. Converting all inner straight quotes to curly keeps regex valid. Order: escape the whole thing: take quote, replace /"/g with '”'? Opening vs closing doesn't matter for display much. But spec: become “ ”. I'll do: first quote char after start... Just do `q.replace(/"/g,'“')`? Display would show “ everywhere. Better pair-wise: replace /"(?=\w)/ opening... Overkill. I'll do: `q = q.replace(/"/g,'”')`... hmm shows wrong direction for opening. Use a small function: alternate. 

```js
function curlyQuotes(q){let o=true;return q.replace(/"/g,()=>{const c=o?'“':'”';o=!o;return c;});}
```
Good enough. But wait — the passages themselves contain curly quotes (120 passages), so model quotes copied verbatim will already have curly quotes. Straight quotes appear only if model converts. OK.

Then verify the built pin via verifyPin — but the document is in the inbox! verifyPin returns not-verified for inbox docs. Hmm. The takeaways are quotes from the inbox document, and pins to it can't verify per the rule "a document whose status is inbox is not verified". But then no takeaway would verify and ingest dies. Wait — the verification rule for inbox: that's for wiki pins (pins to inbox docs are untrustworthy because... hmm, actually the passages ARE in library). Let me re-read: "A pin with no quote, an unknown id, or a document whose status is 'inbox' is not verified, with the reason kept for the chip." And lint: "pins to a document still in the inbox" is a check. And "Unverified: After an ingest the count of ⚠ pins in the wiki is unchanged (0...) and every pin in a changed page verifies".

But during ingest, takeaways quote the inbox document, and the source page draft will contain pins to it. If those pins are "not verified" because inbox, the change cards would show ⚠... Contradiction. Resolution: during ingest, verify quotes against passages regardless of status (the text check), but the lint flags pins to inbox docs as a check until filed; once filed, status becomes "ingested" and the check passes. So verifyPin should have a mode: for the wiki lint/chips, inbox → not verified with reason; for ingest-time checks... but the change cards show pins as chips which call verifyPin...

Hmm. The spec says change cards show "pins added (verified and not, in words)". And "every pin in a changed page verifies" after ingest. So during ingest, pins to the inbox doc must verify (against its passages). I think the cleanest: verifyPin checks the text always; the inbox reason applies only... Let me re-read the edge: "pins to a document still in the inbox" lint check exists because the wiki (as loaded) shouldn't pin to inbox docs (they haven't been read). After filing, status → ingested, so pins verify.

But the chip for a pin to an inbox doc in the loaded wiki: not verified, reason "document is still in the inbox". So verifyPin(pin, {allowInbox:false}) default; ingest code uses allowInbox:true (doc is being ingested). But change-card chips render via renderMD → verifyPin default → would show ⚠... The change cards need to show pins verifying. I'll add a global flag or pass ctx into renderMD with allowInbox doc id. During ingest rendering, ctx.ingestDoc = docId; verifyPin checks `doc.status==='inbox' && doc.id!==ctxDoc`. Hmm but cache. I'll implement verifyPin(pin, allowInboxId) where allowInboxId permits that specific doc; cache key includes it. During change-card rendering, pass ctx {ingestDoc:id}. Also "File the approved changes" sets doc status to 'ingested' and clears... cache would still hold inbox-failed results for other... only that doc was inbox; after status change, cached entries for it keyed without allow flag remain "not verified". I'll clear verCache for that doc on filing, or just clear whole cache on filing. Fine.

Also the lint check "pins to a document still in the inbox" — after filing status is ingested so passes.

Takeaway verification: use verifyPin(pin, docId) with allowInbox=docId.

Failed takeaways: nearest passage on that page: implement longestRun.

```js
function nearestPassage(doc,page,quote){
 const qw=norm(quote).split(' ');let best=null,bl=0;
 for(const x of doc.passages){if(x.page!==page)continue;
  const tw=norm(x.text).split(' ');
  // longest common consecutive run
  for(let i=0;i<qw.length;i++){for(let j=0;j<tw.length;j++){let k=0;while(i+k<qw.length&&j+k<tw.length&&qw[i+k]===tw[j+k])k++;if(k>bl){bl=k;best=x;}}}
 }
 return {passage:best,len:bl};
}
```
O(q*t) fine.

Source page call prompt: verified takeaways with pins, cite-as, doc title/author/published/pages/url, anatomy, return JSON {one_liner, body, touches:[{slug,why}]}, body ≤900 words, only pins given, copied exactly.

The code re-verifies every pin in body (pins parsed from body; each must be among given pins? Spec: "re-verifies every pin in body" — verifyPin each; also pins not among given? I'll verify and also flag pins not in the given set as unverified? Keep: verify each; those failing are counted; card shows counts. Maybe also strip? No—show as ⚠.)

Frontmatter built by code: type 'source', register from stub (stub page register — find page with sources exactly [docId]... the stub a-hrc-57-61; its frontmatter.register), sources [id], links from body links, tags from touched slugs (plus maybe 'source'). status: keep 'reviewed'? The new source page — spec doesn't say; I'll use 'reviewed'... hmm, model-drafted. Use 'draft'? The filed wiki pages are 'reviewed'/'stub'. Since a person approves, I'll set status 'reviewed' after approval? Keep 'draft'? Spec for question pages says status 'draft'. For source page I'll use 'reviewed' — no wait, safer 'draft'? The lint "stub pages" check only flags stubs. I'll set 'reviewed' since approved by a person. Hmm, actually let me set status 'reviewed' — approved. Fine.

touches: keep to existing or allowed new slugs, at most 12, stub added if missing.

Touched page call: page body + takeaways for that slug with pins + instructions; return JSON {edits:[{after, markdown}], contested}. Insert markdown at end of heading's section. Implementation:

```js
function insertEdits(body, edits){
 // build list of heading positions: lines starting with #
 let lines=body.split('\n');
 for(const e of edits){
   const md=(e.after==='end'?'':null)...
 }
}
```
Approach: process edits in order; for each, find heading line matching `after` (exact heading text or startsWith?), then find the end of its section (next heading of same or higher level, or EOF); insert markdown lines there. Track inserted ranges for highlighting: return {body: newBody, marked: newBodyWithMarkers}. I'll build with markers \x01 ... \x02 around inserted blocks, keep `marked` version; strip for real.

Heading match: strip leading #'s and trim; compare case-insensitive? Exact after normalize spaces. If not found → append at end with a note "*(inserted at the end; heading “X” not found)*" — spec: "at the end of the page, with a note".

Contested: if returned and non-empty, append fenced block to body (marked as inserted).

New page (new slug): body starts empty; edits applied to ''; after 'end' → whole body. kind 'new page'.

Also update links both ways and sources: frontmatter.links add slug of source page & other; body links computed; sources add docId. Since code builds final page object at file time, do: for each touched page: newBody; frontmatter.links = union(old links, bodyLinks(newBody), [srcSlug]); sources = union(old, [docId]); updated today. For new pages: type 'concept', title from slug (title-case), register [docRegister letter], sources [docId], links bodyLinks, status 'reviewed', tags [kebab of doc short_title]? Fine.

Change card content: page rendered with inserted paragraphs highlighted. Rendering: renderMD(markedBody) — my renderer must handle \x01/\x02 markers: treat them as toggling a class on the block. Implement: in block loop, a line starting with \x01 sets insFlag... markers wrap inserted markdown which may span multiple blocks (heading + paragraphs). Simplest: put marker at line starts? I'll handle: when a line === '\x01' → ins=true; '\x02' → ins=false; wrap each block's HTML in `<span class="ins">` when ins true. Markers on their own lines. When building, I insert `\n\x01\n` + md + `\n\x02\n`.

Paragraph inserted count: count blocks in inserted markdowns.

Pins added: pins in new body not in old body (compare id+page+quote). Report "n pins added (m verified, k not verified, in words)": I'll phrase "12 pins added, 12 verified by this page, 0 not found".

Review UI: cards in sequence; show one at a time with "change 3 of 9". Approve/Reject buttons labeled "Approve change 3 of 9: slug-title". After last decision → "File the approved changes" button. On file: apply everything as spec (pages replaced/added, index, log, tensions, status, lint re-run, session.changes). Show "Filed" message; lint before/after counts? The checks panel says "Lint re-run and its before and after counts shown side by side" — I'll show a line with before/after "n · check" totals.

Log entry text per spec: "## [date] ingest | symbol: short_title" then detail line: "Read n passages (cite-as, register (x)). Wrote [[slug]]. N pins in all; besides its own page, pinned on k pages: [[…]]. Rejected: [[…]]."

Tensions entry: for each new contested block added:
```
### <kebab-of-claim>
title: <claim>
status: open|leaning|settled
card: [[page-slug]]
poles: <glosses of + and − positions>
where: <page slugs>
```
status: contested→open; leans-*→leaning; settled-*→settled.

Index updates: replace stub line with source page line under Sources; recompute ✓N on touched pages' lines; rebuild first line pins count. Implementation:
- `updateIndex()`: 
  - total pins recount → replace /(\d[\d,]*) pins/ in first line? The first line of index — I'll just do global replace of the pins number via regex on the whole index? Risky. Use: find first match of /(\d[\d,]*)\s+pins/ and replace.
  - For each changed page: find line `- [[slug]]` → replace `✓\d+` with new count; if line missing, insert under section by type (Sources/Concepts/Entities/Questions). Section detection: find `## <Type>s` heading... index structure unknown; sample not given. I'll search for a heading line matching the type name (case-insensitive, plural) and insert after the last line of that section; fallback append at end.
  - For source page: replace the stub's line (line containing `[[a-hrc-57-61]]`... i.e., the old slug) with new line. Actually the source page uses the same slug as the stub? The stub is `a-hrc-57-61` (entity page). The new source page — same slug? Spec: "the stub `a-hrc-57-61` is always among them, rewritten with its ten-item checklist sent along" — so the stub page is edited (rewritten) into... hmm, but also "Draft the source page (1 call) ... the draft appears as a change card" and "the stub's [line] is replaced" in index. And frontmatter register "from the stub". So: the source page might be a new page with slug a-hrc-57-61? The stub slug for A/HRC/57/61 document would naturally be the same slug used for source pages (other source pages presumably have slugs like `a-81-351`). The stub is an entity page with slug a-hrc-57-61. So the source page = same slug, replacing the stub: "new page or edited"? Since slug exists, it's an edit of the stub — kind 'edited', "rewritten". I'll build the source page with slug = stub slug if a stub exists (page whose sources==[docId] and type!=='source'), else kebab of id. Actually docRegister finds "the stub page with that sources". Let me: stubPage = page with sources exactly [docId] and (type==='entity' || status==='stub'). srcSlug = stubPage?stubPage.slug:kebab(docId). The source page change is an edit of the stub (replaces it entirely: new body, new frontmatter with type 'source'). Card kind: 'edited' (page existed). Fine — spec says "the stub's [index line] is replaced", consistent with same slug.

Hmm but then "Wrote [[slug]]" in log — the source page slug. OK.

Registration for source page: "register from the stub" — stub's frontmatter.register.

**Coverage checks** displayed in the checks panel (tab 04) — the self-checks panel lists pass/check lines. I'll implement a `selfChecks()` function producing lines for: pins found vs index stated; verified count; labels; structure (dangling, orphans, sources match, index coverage, contested vs tensions); model answers (per call: JSON parsed, slugs exist, takeaways add up); coverage (passages sent = passages.length; takeaways' passage ids among sent); unverified; approval; filing; session. Many are session-dependent; before any model call they show "not run yet"? The panel says pass/check with values. I'll compute what's computable and for model-dependent ones show "— · not run this session". Keep it as a list of one-line checks with values.

Lint checks (the table): computed by `runLint()` returning array {name, n, pages:[slugs], pass}. Rendered with FIG.03 caption. "n · check" or "0 · pass" with page links.

Let me enumerate lint implementations:
1. Dangling links: slugs in bodyLinks not in pageBySlug.
2. Orphans: pages with no backlinks.
3. Pins not verified: pins where verifyPin false.
4. Pins marked ✓ that fail.
5. sources ≠ pinned documents: set difference of frontmatter.sources vs set of pin ids.
6. Pages with no pins.
7. links not reciprocated: frontmatter.links vs bodyLinks differ (symmetric difference).
8. Pages missing from index / index lines without page: index slugs vs pages.
9. index ✓N differs: parse each index line's ✓N vs computed verified pins for that slug.
10. Contested cards vs tensions card: entries: pages with contested blocks whose slug not in tensions card list; and tensions cards without a page. Combine two counts? Spec lists as one check "contested cards without a tensions entry and the reverse". I'll show count = mismatches both ways.
11. Stub pages.
12. Pins to inbox documents.

Render each row: name, count ("0 · pass" green / "n · check" red), pages as links.

**Tab 05**: 
- log: split on /^## /m. Entries: `## [date] op | subject` + body. Render newest first (default). Switch button toggles. Each entry collapsible: use <details open?> — collapsible via details/summary. Entries added this session: compare against original log length — track `origLog = W.log` and session-appended entries stored separately; mark.
- tensions: render as markdown-ish: I'll render via renderMD (handles ### headings, links). card: links `[[slug]]` will render as page links → open tab 01. Good, automatic.
- method note + source line.
- Download wiki: JSON blob {title, source, built, count, schema, index, log, tensions, pages, changes, library_status}. count = pages.length.
- Download changed pages (markdown) — appears once session.changes.length.

**Header**: as spec. session counters update.

**Footer**: one line.

**Tab running mark**: when ingest running (awaiting a call), tab 03 label appends "· running", aria-live region announces.

Escape key: set global stopFlag; each running loop checks.

Alright, also `studio.openSource(id, page, quote)` — guard existence.

Now, counts: I need to keep code tight. Let me now write it all out. I'll be pragmatic about minor spec details to fit budget, but keep all major features.

One more: "location.hash = slug opens a page on tab 01, so back and forward work." Implement hashchange listener.

Tabs arrow keys: keydown on tablist: ArrowRight/Left move focus & activate.

Let me write the file now.

CSS plan (compact):

```css
:root{--paper:#f4f0e8;--ink:#1d1b18;--rule:#d9d2c3;--acc:#9b2335;--ok:#1e6b34;--amber:#8a5a00;--ins:#faf3d3}
[hidden]{display:none!important}
html{scroll-behavior:smooth}
body{margin:0;background:var(--paper);color:var(--ink);font:16px/1.55 ui-sans-serif,-apple-system,"Segoe UI",sans-serif}
a{color:var(--acc)}
:focus-visible{outline:2px solid var(--acc);outline-offset:2px}
.mono{font:11px/1.4 ui-monospace,Menlo,Consolas,monospace;letter-spacing:.12em;text-transform:uppercase}
header.site{position:sticky;top:0;z-index:5;background:var(--paper);border-bottom:1px solid var(--rule);padding:14px 24px 10px;display:flex;justify-content:space-between;gap:24px;align-items:flex-end}
.hlabel{...mono, color #6b6357}
h1{font:600 26px/1.2 Georgia,"Times New Roman",serif;margin:2px 0 4px}
.hmeta{font-size:13px;color:#5c554a}
.hright{text-align:right;font-size:11px;color:#5c554a;mono...}
.tabs{display:flex;gap:0;border-bottom:1px solid var(--rule);padding:0 24px;background:var(--paper)}
.tab{appearance:none;background:none;border:none;border-bottom:3px solid transparent;padding:10px 14px 8px;cursor:pointer;font:11px mono;letter-spacing:.1em;color:#5c554a}
.tab[aria-selected="true"]{color:var(--acc);border-bottom-color:var(--acc)}
main{padding:24px;max-width:1280px;margin:0 auto}
```

Big numbers: `.big{font:400 44px/1 Georgia,serif}`.

Two columns tab01: `.cols{display:grid;grid-template-columns:320px minmax(0,1fr);gap:36px}@media(max-width:900px){.cols{display:block}}`.

Page list items: `.plist button{display:block;width:100%;text-align:left;background:none;border:none;border-bottom:1px solid var(--rule);padding:7px 2px;cursor:pointer;font-size:14px}`.

Chips: `.chip{white-space:nowrap}` careful with wrap; pins inline with quotes. `.pinw{}` `.pq{font-style:italic}` maybe. Chips: small monospace.

Tables: `.tbl{width:100%;border-collapse:collapse;font-size:14px} .tbl th,.tbl td{border-bottom:1px solid var(--rule);padding:6px 8px;text-align:left;vertical-align:top} .tbl caption{caption-side:top;text-align:left;...mono}`.

Contested card: `.ccard{border:1px solid var(--rule);border-left:3px solid var(--acc);padding:14px 18px;margin:18px 0}`.

Lean bar: `.lean{height:14px;background:#e7e0d2;position:relative} .lean i{position:absolute;inset:0 auto 0 0;background:var(--acc)}`.

Insert highlight: `.ins{background:var(--ins);border-left:3px solid var(--acc);padding-left:8px;display:block}` — applied per block.

OK. Now writing the JS carefully. Key sizes: I'll write it as one big script with sections. Let me now compose the final file. I'll write ~1300 lines.

Some detailed decisions while writing:

`esc = s=>s.replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]))`.

Block renderer:

```js
function renderMD(src,ctx){
 ctx=ctx||{};
 const out=[];const lines=String(src||'').split('\n');
 let i=0,para=[],ins=false;
 const flush=()=>{if(para.length){out.push(wrapIns('<p>'+inlineHTML(para.join(' '),ctx)+'</p>'));para=[];}};
 const wrapIns=h=>ins?'<span class="ins">'+h+'</span>':h;
 while(i<lines.length){
  const L=lines[i];
  if(L.trim()==='```contested'){let buf=[];i++;while(i<lines.length&&lines[i].trim()!=='```'){buf.push(lines[i]);i++;}i++;flush();out.push(contestedHTML(buf,ctx));continue;}
  if(L==='\x01'){flush();ins=true;i++;continue;}
  if(L==='\x02'){flush();ins=false;i++;continue;}
  const h=L.match(/^(#{1,4})\s+(.*)$/);
  if(h){flush();const lv=h[1].length;out.push(wrapIns('<h'+(lv+1)+'>'+inlineHTML(h[2],ctx)+'</h'+(lv+1)+'>'));i++;continue;}
  ... bullets, numbered
  if(!L.trim()){flush();i++;continue;}
  para.push(L.trim());i++;
 }
 flush();
 return out.join('\n');
}
```
Wait — wrapIns wraps each block; marker lines toggle ins. Since \x01 on its own line. Good. Headings level: body uses # (title) — render as h2? Page title shown separately; body's own `# title` heading → I'll render # as h2, ## as h3, ### as h4. Slight shift ok.

Bullets: collect consecutive `- ` lines into `<ul>`. Numbered `^\d+\.\s+` into `<ol>`.

inlineHTML with pins — note: pin regex is global; using replace with function and resetting lastIndex? `String.replace` with /g resets internally, fine.

chipHTML:

```js
let CHIPSEQ=0;const CHIPS=[];
function chipHTML(pin,ctx){
 const v=verifyPin(pin,ctx&&ctx.ingestDoc);
 const doc=docById.get(pin.id);
 const regs=doc?docRegister(pin.id):[];
 const reg=regs.filter(r=>REGNAMES[r]).map(r=>'('+r+')').join('')||'(?';
 let struck=false;
 if(ctx&&ctx.sent){struck=!(ctx.sent.has(pin.id+'#'+pin.page+'|'+pin.quote)&&v.ok);}
 let st;
 if(v.ok)st='<span class="ver ok">✓ verified</span>';
 else st='<span class="ver bad">⚠ not found</span>';
 let says='';
 if(v.ok&&pin.mark==='⚠')says=' <span class="ver">page says ⚠</span>';
 if(!v.ok&&pin.mark==='✓')says=' <span class="ver">page says ✓</span>';
 const idx=CHIPS.push({pin,v})-1;
 const q=pin.quote?esc(pin.quote):'';
 const label=esc(pin.label||pin.id);
 let html='<span class="pinw'+(struck?' struck':'')+'">“'+q+'” ';
 html+='<span class="chip">['+(doc?'<button type="button" class="plab" data-chip="'+idx+'">'+label+'</button>':'<span class="plab">'+label+'</span>')+'] ';
 html+='<span class="preg">'+reg+'</span> '+st+says;
 html+=' <button type="button" class="parr" data-tgl="'+idx+'" aria-expanded="false">▸</button></span>';
 html+='<span class="pdetail" id="pd'+idx+'" hidden></span></span>';
 return html;
}
```
For answer pins, register with name: "(c) UN report" — spec: answer chips carry register letter and name. I'll include name in ctx.answer mode: reg name appended. Let me add: if(ctx&&ctx.sent) reg display = '(c) UN, agency and soft-law reports'? Too long inline. Spec: "Each pin chip carries its document's register letter and name ("(c) UN report")". Names short: I'll add short names: {c:'UN report', d:'NHRI report', e:'civil society', f:'scholarship', a:'treaty law', b:'General Comment'}. Use short names in answer mode.

Struck pins also get note "not on the pages sent": `<span class="ver bad">not on the pages sent</span>`.

Detail fill (on toggle):

```js
function fillDetail(idx){const c=CHIPS[idx];const el=document.getElementById('pd'+idx);if(el.dataset.done)return;
 const p=c.v.passage;
 let h='';
 if(!c.pin.quote)h='The pin carries no quote.';
 else if(!docById.get(c.pin.id))h='Unknown document.';
 else{
  const d=docById.get(c.pin.id);
  if(p)h='<span class="mono">PASSAGE</span> '+(p.paragraph!=null?'para. '+esc(p.paragraph):'p. '+esc(p.page_label))+' · PDF p.'+p.page+'<br>'+esc((p.text||'').slice(0,300))+(p.text&&p.text.length>300?'…':'');
  else h='<span class="ver bad">'+esc(c.v.reason)+'</span> — footnotes, tables and captions are not in the passages; a pin cannot verify them.';
  h+='<br><button type="button" class="btn small" data-chip="'+idx+'">Open the PDF page</button>';
 }
 el.innerHTML=h;el.dataset.done='1';}
```
data-chip on both label and open button → openSource.

Delegated clicks:

```js
document.addEventListener('click',e=>{
 const o=e.target.closest('[data-chip]');
 if(o){const c=CHIPS[+o.dataset.chip];if(c&&window.studio&&studio.openSource)studio.openSource(c.pin.id,c.pin.page,c.pin.quote||'');return;}
 const t=e.target.closest('[data-tgl]');
 if(t){const i=+t.dataset.tgl;const el=document.getElementById('pd'+i);fillDetail(i);const vis=!el.hidden;el.hidden=vis;t.setAttribute('aria-expanded',String(!vis));t.textContent=vis?'▸':'▾';return;}
});
```

Contested HTML:

```js
function contestedHTML(lines,ctx){
 let claim='',verdict='',note='';const pos=[];
 for(const L of lines){const s=L.trim();
  if(s.startsWith('claim:'))claim=s.slice(6).trim();
  else if(s.startsWith('verdict:'))verdict=s.slice(8).trim();
  else if(s.startsWith('note:'))note=s.slice(5).trim();
  else if(/^[+~-]\s/.test(s))pos.push(s);}
 let sw=0,tw=0;const rows=[];
 for(const s of pos){const parts=s.split('|').map(x=>x.trim());
  const sign=parts[0][0],reg=parts[0].slice(1).trim();
  const w=REGW[reg]||0;tw+=w;if(sign==='+')sw+=w;else if(sign==='~')sw+=w/2;
  const pinS=parts[1]||'',gloss=parts[2]||'',pageS=(parts[3]||'').replace(/^\[\[|\]\]$/g,'');
  rows.push({sign,reg,pinS,gloss,pageS});}
 const pct=tw?Math.round(1000*sw/tw)/10:0;
 const signName={'+':'supports','-':'contests','~':'mixed'};
 let h='<section class="ccard"><div class="mono fign">CONTESTED CLAIM</div>';
 h+='<h4 class="cclaim">'+inlineHTML(claim,ctx)+'</h4>';
 h+='<p class="cverdict">'+esc(verdict.replace(/-/g,' '))+'</p>';
 if(note)h+='<p class="cnote">'+inlineHTML(note,ctx)+'</p>';
 h+='<div class="mono fign">FIG · LEAN, DESCRIPTIVE</div><div class="lean" role="img" aria-label="support '+pct+'% of weighted positions"><i style="width:'+pct+'%"></i></div>';
 h+='<p class="howc">descriptive: support '+pct+'% of weighted positions, weights a 5 · b 4 · c 3 · d 2 · e 1 · f ½; the verdict is the answer</p>';
 h+='<table class="tbl"><caption>Positions ('+rows.length+')</caption><thead><tr><th scope="col">Position</th><th scope="col">Register</th><th scope="col">Pin</th><th scope="col">Gloss</th><th scope="col">Page</th></tr></thead><tbody>';
 for(const r of rows){
  h+='<tr><td>'+signName[r.sign]+'</td><td class="mono">'+esc(r.reg)+'</td><td>'+inlineHTML(r.pinS,ctx)+'</td><td>'+inlineHTML(r.gloss,ctx)+'</td><td>'+inlineHTML('[['+r.pageS+']]',ctx)+'</td></tr>';}
 h+='</tbody></table>';
 // tensions link if page context
 if(ctx&&ctx.slug){const re=new RegExp('card:\\s*\\[\\['+escapeRe(ctx.slug)+'\\]\\]');if(re.test(W.tensions))h+='<p><a href="#" data-goto-tab="4">in the tensions register →</a></p>';}
 h+='</section>';
 return h;
}
```
Pin in position lines: `[A/81/351, para. 16](pin:... ) ✓` — inlineHTML handles pins. ✓

escapeRe helper.

data-goto-tab delegated click → switchTab.

Page view (tab 01 main):

```js
function pageView(slug){
 const p=pageBySlug.get(slug);const m=meta.get(slug);
 let h='<article class="page">';
 h+='<div class="mono fign">PAGE · '+esc(p.type.toUpperCase())+'</div>';
 h+='<h2 class="ptitle">'+esc(p.title)+'</h2>';
 badges: type, register letters+names, status, updated; tags
 h+=renderMD(p.body,{slug});
 // links out / linked from / sources
 ...
 copy button
}
```

Badges: `<span class="badge">type</span>` etc.

Links out: m.links (frontmatter.links) each → link; if not in bodyLinks set → append `<span class="mono">frontmatter only</span>`.
Linked from: iterate meta, back sets.
Sources: for each id in frontmatter.sources: doc short_title, kind, year, url link, 'inbox' mark.

Copy button: `data-copy-page="slug"`.

Copy markdown:
```js
function pageMarkdown(p){return '---\n'+yaml(p.frontmatter)+'---\n\n'+p.body;}
function yaml(fm){ lines for title,type,tags(list),register(list),status,updated,links(list),sources(list) }
```

Index view: `<article class="page"><div class="mono fign">INDEX</div>` + renderMD(W.index).

Tab 01 render: list + view. Filter input `oninput` → renderPageList().

Now ASK tab rendering & logic. DOM: static in HTML with containers; JS fills.

```html
<section id="tab1" role="tabpanel">... etc
```

I'll create the tab panels in HTML statically and fill via JS.

ASK flow code:

```js
const ask={phase:'idle',slugs:[],answer:null,title:'',cannot:'',sent:null,stop:false,busy:false};
async function doAsk(){
 if(ask.busy)return;
 const q=el('askq').value.trim();if(!q){note...;return;}
 if(ask.phase==='chips'){return askStep2();}
 ask.phase='step1';ask.busy=true;ask.stop=false;
 setAskProgress('Step 1 · sending the index and your question · '+W.index.length+' characters · 0 library passages leave the browser',true);
 const prompt1=askPrompt1(q);
 const r=await callModel(prompt1);
 ask.busy=false;
 if(ask.stop){ask.phase='idle';setAskProgress('stopped',false);return;}
 if(!r.json||!Array.isArray(r.json.pages)){showRaw(r,'ask');return;}
 ask.slugs=[...new Set(r.json.pages.filter(s=>pageBySlug.has(s)))].slice(0,5);
 ask.phase='chips';renderAsk();
}
```

callModel increments counters and handles stop? Stop only prevents continuing. The Stop button sets ask.stop=true; since we can't abort studio.ask, when it resolves we discard. Acceptable.

renderAsk(): shows chips (slugs) + "Change pages" link + checkbox list (hidden until clicked) + button label "Send these pages". Progress line shows counts.

askStep2():
```js
const bodies=ask.slugs.map(s=>'# PAGE '+s+'\n'+pageBySlug.get(s).body).join('\n\n');
announce: 'Step 2 · sending n pages, X characters; 0 library passages have left the browser'
prompt2 with instructions; callModel; parse {title,answer,cannot_answer}
build sent set from chosen pages' pins
ask.answer=...; render answer inside data-source="ai"
```

Answer rendering: `renderMD(ask.answer,{sent:ask.sent,answer:true})`. Pins in answer that exist in sent pages with same quote & verify → normal chip with register name; others struck.

Register count line: iterate pins parsed from answer, count those accepted&verified by register letter of doc.

File card: build preview:

```js
function buildQuestionPage(){
 const title=ask.title; slug=uniqueSlug(kebab(title));
 tags from input
 register: union of docRegister over pinned docs
 links: bodyLinks of answer
 sources: pin ids
 body='# '+title+'\n\n**Short answer.**\n\n'+? 
```
Spec: body = "# title", "**Short answer.**", "## Reasoning" (the answer), "## What the library cannot answer", "## Related". So:

```
# Title

**Short answer.**

<answer>? 
```
Hmm "**Short answer.**" then what text? Probably the answer's first part? The answer is the whole text. I think: Short answer section holds the answer (≤350 words) and Reasoning... wait "## Reasoning (the answer)". So Short answer is maybe empty or the title...? Reading again: body = "# title", "**Short answer.**", "## Reasoning" (the answer), "## What the library cannot answer", "## Related". So Short answer is a label with... perhaps the model's answer is short. I'll put the answer under "**Short answer.**" AND also under Reasoning? That duplicates. Interpretation: "**Short answer.**" followed by the answer text, then "## Reasoning" ... no. Alternative: the answer from the model goes under Reasoning; Short answer left for... Hmm. Maybe intended: **Short answer.** = the answer text (it's ≤350 words, short), then ## What the library cannot answer, ## Related. And "## Reasoning (the answer)" means the answer goes under a Reasoning heading. I'll do:

```
# Title

**Short answer.**

## Reasoning

<answer>

## What the library cannot answer

<cannot>

## Related

- [[slug]]...
```
That matches the listed order exactly with the answer under Reasoning. Short answer section empty-ish is odd but faithful to the list. Hmm, that leaves "**Short answer.**" dangling. Maybe better: put the first sentence of the answer as the short answer? That's inventing. I'll put the answer's first paragraph under Short answer... no — duplicating text. Decision: "**Short answer.**" followed by the answer text, and "## Reasoning" omitted? The spec explicitly lists both. I'll keep both: Short answer holds the answer's first paragraph (deterministic split on first blank line), Reasoning holds the full answer. That's a reasonable reading and deterministic. Hmm, but duplication of first paragraph... Acceptable; note in preview. Actually simplest faithful: Short answer = answer text; Reasoning heading contains "See Short answer above."? No.

Let me just do: Short answer. → first paragraph of answer; ## Reasoning → full answer. Fine.

File this page: disabled until every pin verifies (accepted & verified). Add page, index line under Questions, log entry, session.changes, recompute meta, message "Filed" aria-live.

uniqueSlug(base): if exists append -2, -3...

kebab(s): lowercase, non-alnum→'-', collapse, trim.

**Ingest code** — the biggest. Let me write it.

```js
let ing=null;
function renderIngest(){
 const c=el('t3body');
 if(!ing){
  const inbox=D.filter(d=>d.status==='inbox');
  if(!inbox.length){c.innerHTML='<p>Nothing waits in the inbox.</p>';return;}
  c.innerHTML=inbox.map(d=>`<p><button class="btn" data-ingest="${esc(d.id)}">Ingest ${esc(d.symbol||d.short_title)}</button> <span class="howc">${esc(d.short_title)}, ${d.passages.length} passages</span></p>`).join('');
  return;
 }
 ... phases
}
```

Start ingest:
```js
function startIngest(id){const d=docById.get(id);ing={doc:d,bi:0,takeaways:[],failed:[],dropped:0,batches:batchAll(d),phase:'scope',src:null,touched:null,changes:[],ci:0,stop:false,busy:false,newSlugs:[]};renderIngest();}
function batchAll(d){const b=[];for(let i=0;i<d.passages.length;i+=25)b.push(d.passages.slice(i,i+25));return b;}
```

Scope panel: text + batches table (paragraph range & pdf pages per batch) + Start button (data-ingstart).

Run batches:
```js
async function runBatches(){
 ing.phase='batches';ing.busy=true;ing.stop=false;
 for(;ing.bi<ing.batches.length;ing.bi++){
  if(ing.stop)break;
  const b=ing.batches[ing.bi];
  ing.progress='batch '+(ing.bi+1)+' of '+ing.batches.length+' · '+Math.min((ing.bi+1)*25,doc.passages.length)... 
```
Progress: "batch 2 of 4 · 50 of 100 passages have left the browser". passages sent so far = sum of batches processed (including current when sent). Set session.passages += b.length when sending.

Prompt: passages JSON {id,page,paragraph,text}, index, instructions. Parse {takeaways:[...]}. For each takeaway: passage lookup in batch set; if not found → dropped++ (and count). Build pin (with curlyQuotes), verify with allowInbox=doc.id. If ok → takeaways.push({claim,quote,pin,pinText,passage, pages: filtered slugs + allowed new slugs}). Else failed.push({claim,quote,passage: model's passage id, nearest: nearestPassage(...)}).

New slugs allowance: collect proposed slugs not in pageBySlug; keep at most 2 across whole ingest (ing.newSlugs). Others dropped from pages list (and noted? keep simple: dropped silently from pages but counted in checks "slugs that do not exist listed").

After loop: ing.phase='takeaways' (step 2 done). renderIngest shows takeaways table + failed box + step-3 buttons.

Takeaways table columns: claim, quote, passage (para/PDF p), pages (chips), verification. FIG.02.

Failed box: "Could not verify: n" each with model quote, nearest passage (para, run length), Open PDF page button (data-openpdf with id/page/quote=quote).

Step 3 buttons: "Draft the source page (1 call)" → sourceDraft(); then "Draft the changes to n pages (n calls)" → touchedDrafts().

sourceDraft():
```js
const pinsList=ing.takeaways.map(t=>t.pinText).join('\n');
prompt = cite-as, doc meta, anatomy, pins, "return JSON {one_liner, body, touches:[{slug,why}]}, body at most 900 words, only the pins given, copied exactly. Pin syntax: ... quote only words that stand in the passages given; the code will check."
```
On return: parse pins in body, verify each (allowInbox). touches filtered: existing slugs or ing.newSlugs, max 12, stub added if missing (stub slug). Determine srcSlug: stub page (sources==[id]) → slug; else kebab(id). Build source page object:

```js
const stub=pagesWithSources([id]).find(p=>p.slug===... ) 
```
Find: `P.find(p=>arrayEq(p.frontmatter.sources,[id]))` — that gives stub (entity) or source page. srcSlug = that? For A/HRC/57/61 the stub a-hrc-57-61. But careful: the source page should have the "source-like" slug. Other source pages have slugs like `a-81-351` (kebab of id lowercased). kebab('A/HRC/57/61') = 'a-hrc-57-61'. Same as stub. 

srcPage = {slug:srcSlug, type:'source', title: doc.title (or short_title?), frontmatter:{title:doc.title,type:'source',tags:[...touched slugs? plus 'source'],register:stubRegister,status:'reviewed',updated:today,links:bodyLinks,body sources:[id]}, body: model body, one_liner}
```
Change card: kind = stub existed ? 'edited' (rewritten) : 'new page'.

touchedDrafts(): slugs = union of takeaways' pages (existing) + newSlugs + stub, minus srcSlug (src handled separately), dedupe. For each slug, one call:

```js
const page = pageBySlug.get(slug);
const bodyText = page? page.body : '(this page does not exist yet; draft it)';
const ts = takeaways with pages including slug;
prompt: body, takeaways with pins, instructions, return {edits:[{after,markdown}], contested}
```
Apply edits via insertEdits; collect contested block (string). Store draft {slug, body(new), marked, contested, existed, oldPage}.

Then phase 'review': build changes array:
- source page change {slug:srcSlug, page:newSrcPage, old:stubPageOrNull, kind}
- each touched draft change.
Count paragraphs inserted & pins added.

Review UI: one card at a time (ing.ci). Card: fieldset/legend, title+type, kind, counts, rendered marked body with ctx.ingestDoc=id, Approve/Reject buttons ("Approve change 3 of 9"), line "change 3 of 9". After all decided → "File the approved changes" button.

Approve: changes[ci].approved=true; reject: approved=false, note in log. ci++; renderIngest.

fileIngest():
```js
const approved=ing.changes.filter(c=>c.approved);
for(const c of approved){ apply page: if existed → replace in P (P is array; find index by slug, replace); else push. update meta.}
doc.status='ingested' (in memory)
updateIndexFor(changes)
log entry
tensions additions
session.changes.push({date,kind:'ingest',pages:...})
clear verCache? recompute meta & counts
ing.phase='filed'; renderIngest(); renderHeader(); runLint();
lintBefore/After display.
```

Page objects: build frontmatter for touched pages: copy old frontmatter, update links (union old links, bodyLinks new, [srcSlug]), sources union [docId], updated today. For new pages: build fresh.

Insert edits function:

```js
function insertEdits(body,edits,contested){
 let lines=(body||'').split('\n');
 const inserted=[];
 const findHeading=(name)=>{
  for(let i=0;i<lines.length;i++){const m=lines[i].match(/^(#{1,4})\s+(.*)$/);
   if(m&&m[2].trim()===name.trim())return {i,lv:m[1].length};}
  return null;};
 for(const e of edits||[]){
  let md=(e.markdown||'').trim();if(!md)continue;
  let at=lines.length,note='';
  if(e.after&&e.after!=='end'){const h=findHeading(e.after);
   if(h){let j=h.i+1;while(j<lines.length){const m=lines[j].match(/^(#{1,4})\s+/);if(m&&m[1].length<=h.lv)break;j++;}
    // skip blank lines at section end
    while(j>h.i+1&&lines[j-1].trim()==='')j--;
    at=j;}
   else{note='\n*(Inserted at the end of the page: heading “'+e.after+'” was not found.)*';md=md+note;}}
  else{ // end
   while(lines.length&&!lines[lines.length-1].trim())lines.pop();}
  const block=['','\x01',...md.split('\n'),'\x02',''];
  lines=[...lines.slice(0,at),...block,...lines.slice(at)];
  inserted.push(md);
 }
 if(contested&&contested.trim()){const cb='```contested\n'+contested.trim()+'\n```';lines=lines.concat(['','\x01',...cb.split('\n'),'\x02','']);inserted.push(cb);}
 return {body:lines.join('\n').replace(/\x01\n?|\x02\n?/g,m=>m), marked:lines.join('\n'), inserted};
}
```
Wait body should have markers stripped: `lines.join('\n')` then remove marker lines: `.split('\n').filter(l=>l!=='\x01'&&l!=='\x02').join('\n')`. Simpler.

Hmm, findHeading operates on `lines` which mutates as we insert — fine.

Edge: insert at 'end': pop trailing blanks then push at end.

Count blocks in inserted markdown:
```js
function countBlocks(md){return md.split(/\n\s*\n/).map(x=>x.trim()).filter(Boolean).length;}
```

Pins added: parse pins of new body, minus old body pins (key set).

Index update:
```js
function indexSlugLine(p){const m=meta.get(p.slug);const n=m?m.pins.filter(x=>verifyPin(x).ok).length:0;
 const regs=(p.frontmatter.register||[]).join('');
 const one=p.one_liner||p.frontmatter.title;
 return '- [['+p.slug+']] — '+one+' · ('+regs+') · ✓'+n;}
```
One-liner for source page from model. For others keep existing line's one-liner: when recomputing ✓N for touched pages, just regex-replace `✓\d+` in existing line. For the source page, replace the stub's line entirely with new line. Insert if no line: find section by type.

```js
function updateIndexFile(changed,srcPage){
 let idx=W.index;
 // replace stub line / add source line
 const srcLine=indexSlugLine(srcPage);
 const re=new RegExp('- \\[\\['+escapeRe(srcPage.slug)+'\\]\\][^\\n]*');
 if(re.test(idx))idx=idx.replace(re,srcLine);
 else idx=insertIndexLine(idx,srcPage);
 for(const c of changed){ if(c.page.slug===srcPage.slug)continue;
  const r2=new RegExp('(- \\[\\['+escapeRe(c.page.slug)+'\\]\\][^\\n]*?)✓\\d+');
  const m=meta.get(c.page.slug);const n=m?countVer(m):0;
  if(r2.test(idx))idx=idx.replace(r2,'$1✓'+n);
  else idx=insertIndexLine(idx,c.page);
 }
 // first line pins count
 const total=[...meta.values()].reduce((a,m)=>a+m.pins.length,0);
 idx=idx.replace(/(\d[\d,]*)\s+pins/,total.toLocaleString()+' pins');
 W.index=idx;
}
```
insertIndexLine: find heading matching type plural (`## Sources`, `## Concepts` etc — case-insensitive contains). Insert after last non-empty line of that section; else append.

```js
function insertIndexLine(idx,p){
 const sec=(p.type||'').toLowerCase();
 const lines=idx.split('\n');let start=-1;
 for(let i=0;i<lines.length;i++){if(/^#{1,3}\s/.test(lines[i])&&lines[i].toLowerCase().includes(sec)){start=i;break;}}
 if(start<0){return idx+'\n'+indexSlugLine(p)+'\n';}
 let end=lines.length;
 for(let i=start+1;i<lines.length;i++){if(/^#{1,3}\s/.test(lines[i])){end=i;break;}}
 while(end>start+1&&lines[end-1].trim()==='')end--;
 lines.splice(end,0,indexSlugLine(p));
 return lines.join('\n');}
```

Log entry:
```js
const cite=ing.citeAs; const reg=docRegister(id).join('');
let detail='Read '+d.passages.length+' passages ('+cite+', register ('+reg+')). Wrote [['+srcSlug+']]. '+srcPins+' pins in all; besides its own page, pinned on '+k+' pages: '+slugs.map(s=>'[['+s+']]').join(', ')+'.';
const rej=ing.changes.filter(c=>!c.approved);
if(rej.length)detail+=' Rejected: '+rej.map(c=>'[['+c.page.slug+']]').join(', ')+'.';
W.log+='\n\n## ['+today()+'] ingest | '+symbol+': '+short_title+'\n'+detail;
sessionLogCount++
```
k = number of other pages pinning docId after filing: count pages (excluding src) whose pins include id.

Tensions addition: for each change with contested (the raw contested string from that page's draft): parse claim/verdict; entry:

```js
function tensionsEntry(contestedRaw,pageSlug){
 parse claim, verdict, positions...
 const cslug=kebab(claim).slice(0,60);
 const status=verdict.startsWith('contested')?'open':verdict.startsWith('leans')?'leaning':'settled';
 poles: glosses of + and - positions joined '; '
 where: position page slugs
 return '### '+cslug+'\ntitle: '+claim+'\nstatus: '+status+'\ncard: [['+pageSlug+']]\npoles: '+poles+'\nwhere: '+where+'\n';
}
W.tensions = W.tensions.trimEnd()+'\n\n'+entry;
```

Now CHECK tab:

```js
function runLint(){
 const checks=[];
 // helper add(name, pages[])
 dangling: map over meta: bodyLinks not in pageBySlug → pages
 orphans: pages with back.size===0
 pinsNotVerified: pages with any pin failing (allowInbox none)
 markedFail: pins mark ✓ failing
 sourcesDiff
 noPins
 linksDiff: symmetric diff frontmatter.links vs bodyLinks
 indexCov: pages missing from index + index slugs without pages (two lists, combined count)
 indexN: lines where ✓N ≠ computed
 contestedMismatch: pages with contested blocks whose slug not in tensionsCards; tensionsCards without contested block on that page
 stubs
 inboxPins: pages with pins to inbox docs
 store lint=checks; render
}
```

Index slugs: `[...W.index.matchAll(/\[\[([^\]|#]+)\]\]/g)]`.
Tensions cards: `[...W.tensions.matchAll(/card:\s*\[\[([^\]]+)\]\]/g)]`.
Contested blocks per page: count occurrences of '```contested' in body.

Checks panel (self-checks): function selfChecks() returns lines:
- "Pins found by the regular expression: 707 · index states 707 — pass/check"
- "Pins verified: 707 of 707"
- "Labels match passage paragraph or page_label: n/n"
- structure lines (reuse lint values)
- model answers: per session call: "call 1 JSON parsed: pass" etc. Track session.callLog=[{label,ok,chars}]. Show latest few or summary: "calls this session: m, JSON parsed: k of m".
- coverage (ingest): passages sent vs total; takeaways returned = verified + failed (+dropped).
- unverified after ingest: ⚠ count before/after.
- approval: pages changed equal approved cards; log lists them.
- session: changes listed equal log entries added this session.

Render as list with pass/check words. For not-run items show "not run yet". I'll compute what's available.

Big number: verified pins / total pins; "n lint checks need a look" = checks with count>0 (after run; before run show "run Lint now").

Lint now button → runLint() (first time auto? Spec says one button Lint now, reads Re-run after first run. So not auto; big number shows pins verified (computed at load regardless) and lint line "n lint checks need a look" — before first run maybe "—". I'll run lint lazily on first visit? Spec: "At the top one big serif number, 'n of n pins verified by this page', and 'n lint checks need a look'." I'll compute lint on load silently (cheap) but the table shows after pressing Lint now? Hmm "One button, Lint now, which reads 'Re-run' after the first run" implies table appears after press. I'll auto-run on load anyway to show the count, and show the table after button press. Simplest: run lint at load, show table, button "Re-run". But spec wants button gating... "Each reads '0 · pass' or 'n · check'" — table exists. I'll show table after first run and auto-run on first tab visit. Actually just run at load and display; button says "Re-run". Slight deviation, acceptable? The spec explicitly says button Lint now → "Re-run" after first run, implying the first run is user-triggered. I'll display the count "n lint checks need a look" from a load-time computation, table hidden until Lint now. Fine — I'll run computation at load (for the count) but reveal table on button.

RECORD tab:

```js
let logNewest=true;
function renderRecord(){
 entries = W.log.split(/^## /m).filter(x=>x.trim())
 each: first line "[date] op | subject", rest body.
 html: details/summary; session entries marked.
 order per switch.
 tensions: renderMD(W.tensions) inside .page
 buttons: Download the wiki; Download changed pages (if session.changes.length)
 method note, source line
}
```
Session log entries: count original entries at load: origLogEntries = split count. Entries beyond that → "this session".

Downloads:
```js
function download(name,text,type){const b=new Blob([text],{type});const u=URL.createObjectURL(b);const a=document.createElement('a');a.href=u;a.download=name;document.body.appendChild(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(u),500);}
```
Wiki JSON: {title:W.title,source:W.source,built:W.built,count:P.length,schema:W.schema,index:W.index,log:W.log,tensions:W.tensions,pages:P,changes:session.changes.map(...),library_status:Object.fromEntries(D.map(d=>[d.id,d.status]))}.

Changed pages markdown: session changed slugs → pages with '---' separators (pageMarkdown).

Header render: counts from computed data. "n pins, n verified by this page", documents & inbox, built. Right: session counters.

Now tab labels & running: `setTabRunning(true)` → tab3 text '03 INGEST · running' with aria-live polite? Put an aria-live span. I'll implement updateTabs().

Hash routing:
```js
window.addEventListener('hashchange',()=>{const s=decodeURIComponent(location.hash.slice(1));if(s&&pageBySlug.has(s)){switchTab(0);currentSlug=s;renderTab1View();}});
```
And when clicking a page in list or wikilink: set location.hash (guard: if same, call directly).

Wikilinks in renderMD are `<a href="#slug">` — default behavior changes hash → hashchange handles. But if hash already equals (same page click), nothing—fine. Also need to ensure hashchange switches to tab 01 — yes as above. But careful: when user is on tab 01 and clicks link, fine.

Tab switching: `switchTab(i)` sets aria-selected, hidden on panels, focus? Only on keyboard nav.

Arrow keys on tablist:
```js
tabsEl.addEventListener('keydown',e=>{if(e.key==='ArrowRight'||e.key==='ArrowLeft'){e.preventDefault();const d=e.key==='ArrowRight'?1:-1;const n=(cur+d+5)%5;switchTab(n);tabs[n].focus();}});
```

Escape: document keydown → if ing&&ing.busy ing.stop=true; if ask.busy ask.stop=true; update progress note "stopping…".

Now let me also handle `renderTab1View()`: main column: currentSlug? pageView : indexView.

meta computation:
```js
function computeMeta(){
 meta=new Map();
 for(const p of P){const pins=parsePins(p.body);const links=[...new Set([...p.body.matchAll(/\[\[([^\]|#]+)/g)].map(m=>m[1]))];
  meta.set(p.slug,{pins,links});}
 // backlinks
 for(const m of meta.values())m.back=new Set();
 for(const p of P)for(const l of meta.get(p.slug).links){const t=meta.get(l);if(t&&l!==p.slug)t.back.add(p.slug);}
}
```
Call after any filing too.

OK, prompts. Write them carefully but compactly.

Common suffix: `Pin syntax: [label](pin:DOCID#pPDFPAGE "quote") ✓ — quote only words that stand in the passages given; the code will check. Return JSON only.`

askPrompt1:
```
You are the librarian of a research wiki on neurotechnology in the administration of justice. Here is the wiki index:

<index>

Question: <q>

Choose the pages (at most five) whose bodies best answer it. Return JSON only: {"pages":["slug", ...]} using slugs that appear in the index.
```

askPrompt2:
```
Here are the full pages:

<bodies>

Question: <q>

Write the answer (at most 350 words) using only these pages. Cite with pins copied exactly as they appear above, character for character. Where the register matters, name it ((a) treaty law, (b) General Comments, (c) UN reports, (d) NHRI, (e) civil society, (f) scholarship); keep each document's own verb; never present (c)–(f) as what a treaty requires. Pin syntax: [label](pin:ID#pPAGE "quote") ✓ — quote only words that stand in the passages given; the code will check. Return JSON only: {"title":"...","answer":"markdown","cannot_answer":"what the library cannot answer"}.
```

Takeaway prompt:
```
You are reading a UN document into a research wiki. Passages (JSON): [...]
Wiki index: <index>
For this batch, return at most 10 takeaways: claims this document makes that bear on the wiki. Each: quote of 8 to 40 words copied verbatim from that one passage; passage = the passage id; pages = slugs from the index the claim bears on (you may propose up to two new kebab-case slugs in the whole ingest). Pin syntax: ... Return JSON only: {"takeaways":[{"claim":"","quote":"","passage":"","pages":[]}]}
```

Source page prompt:
```
Draft the source page for <doc title, author, published, pages, url>. Cite as: <cite-as>. Takeaways with their pins (copy pins exactly):
<pins>
Anatomy: Full cite; Register; One-liner; Key takeaways; How NOT to read this; Where it feeds the wiki; Related. Body at most 900 words, markdown, headings ## and ###, only the pins given, copied exactly. Pin syntax... Return JSON only: {"one_liner":"","body":"markdown","touches":[{"slug":"","why":""}]}
```

Touched prompt:
```
Here is the wiki page <slug>:
<body or "(new page)">
New takeaways from <cite-as> (pins; copy exactly):
<takeaways>
Return edits: each {after: an existing heading in the page or "end", markdown: at most 300 words in all}. If this document disagrees with the page, also return "contested": a fenced block (claim:, verdict:, note:, then lines "+ reg | pin | gloss | [[slug]]"). Pin syntax... Return JSON only: {"edits":[{"after":"","markdown":""}],"contested":""}
```

callModel:

```js
async function callModel(prompt,label){
 session.calls++;session.callLog.push({label,chars:prompt.length,ok:false});
 renderHeader();
 announce(promptAnnouncement(label,prompt));
 let raw='';
 try{raw=await studio.ask(prompt,{json:true})||'';}catch(e){raw='';}
 const ent=session.callLog[session.callLog.length-1];
 let j=null;
 try{j=JSON.parse(raw);}catch(e){try{j=JSON.parse(raw.replace(/^```[a-zA-Z]*\s*/,'').replace(/```\s*$/,'').trim());}catch(e2){}}
 ent.ok=!!j;ent.raw=raw;
 renderHeader();
 return {json:j,raw};
}
```

Announcement: "sent to the model: <label>, N characters; passages in it: k" — for takeaway calls, passages count = batch length, and session.passages += that. I'll pass passages count param.

showRaw: display raw in a pre inside the relevant tab with a Retry button that re-runs the same call (store last call fn). Implement `retryFn` global; Retry button calls it.

OK — also "The answer comes as one text" etc.

Time to actually write the final HTML. I'll try to keep it organized and commented lightly. Let me write it fully now, watching length (~1400 lines).

Also remember: header right strip, footer line, focus on first tab on load.

Let me write out the code.

Additional detail — tab 02 "A grey box above states what each step will send before it goes." I'll include a static grey box: "Step 1 sends the wiki index and your question. Step 2 sends the bodies of the chosen pages and your question. No library passages leave the browser in either step."

Ask clickables: textarea, Ask button, Change pages (link), File as question page, File this page, Copy answer. OK.

Now the ingest "calls so far m · passages sent k" running line at stepper top, updated.

Write everything. For event delegation, I'll use one document click handler with data- attributes:
- data-page (go to page)
- data-tab (go to tab)
- data-copy-page
- data-ingest, data-ingstart, data-ingbatch? (start batches = same as ingstart)
- data-srcdraft, data-tchdraft
- data-approve, data-reject, data-file
- data-openpdf (id,page,quote)
- data-ask (main button), data-changepages, data-fileq, data-copyans, data-retry
- data-lint
- data-order (log switch)
- data-dlwiki, data-dlpages
- data-goto (page link alt) — wikilinks use href="#slug" natively.

For ask main button: id askbtn, click → doAsk.

Question tags input: id asktags.

Let me now write. I'll number figure labels: FIG.01 lean bar, FIG.02 takeaways table, FIG.03 lint table.

Also spec: header counts "n pins, n verified by this page". Compute totalPins, totalVerified.

Edge: verifyPin cache with allowInbox param — key includes allow.

```js
function verifyPin(pin,allowDoc){
 const key=(allowDoc||'')+'|'+pin.id+'#'+pin.page+'|'+(pin.quote||'');
 ...cache
}
```

Also pins parsed need mark etc.

parsePins:
```js
function parsePins(body){const out=[];let m;PINRE.lastIndex=0;while((m=PINRE.exec(body))){out.push({label:m[1],id:m[2],page:+m[3],quote:m[4]||'',mark:m[5]});}return out;}
```

Note: PINRE has capture groups (label,id,page,quote,mark) — matches spec.

Counting pins for header: sum over meta.

Let me write the HTML body skeleton:

```html
<header class="site">
 <div>
  <div class="mono hlabel">WIKI · NEUROTECHNOLOGY AND JUSTICE</div>
  <h1>Research wiki: neurotechnology in the administration of justice</h1>
  <div class="hmeta" id="hmeta"></div>
 </div>
 <div class="hright">
  <div id="hsession" aria-live="polite"></div>
  <div class="hwarn">This page has no storage: changes live in it until you download them (tab 05).</div>
 </div>
</header>
<nav class="tabs" role="tablist" aria-label="Sections" id="tablist">
 <button role="tab" id="tab0" aria-selected="true" aria-controls="p0" class="tab">01 PAGES</button>
 ... 02 ASK, 03 INGEST, 04 CHECK, 05 RECORD
</nav>
<main>
 <section id="p0" role="tabpanel" aria-labelledby="tab0">
   <div class="cols">
    <div class="rail">
     <label class="mono" for="pfilter">FILTER</label>
     <input id="pfilter" placeholder="title, tag or slug">
     <div class="bignum" id="pcount"></div>
     <div id="plist"></div>
    </div>
    <div id="pview"></div>
   </div>
 </section>
 <section id="p1" role="tabpanel" aria-labelledby="tab1" hidden> ... ask UI ... </section>
 <section id="p2" ... hidden><div id="t3body"></div></section>
 <section id="p3" hidden> check </section>
 <section id="p4" hidden> record </section>
</main>
<footer class="foot mono" id="foot"></footer>
```

Ask UI static:
```html
<div class="askbox">
 <label for="askq" class="mono">QUESTION</label>
 <textarea id="askq" rows="3"></textarea>
 <button id="askbtn" class="btn primary">Ask the wiki</button>
 <div class="grey">Before it goes: step 1 sends the wiki index and your question (n characters). Step 2 sends the bodies of the pages chosen and your question. No library passages leave the browser in either step.</div>
 <div id="askprog" class="prog" aria-live="polite"></div>
 <div id="askstopwrap" hidden><button class="btn" id="askstop">Stop</button></div>
 <div id="askstep1"></div>
 <div id="askans"></div>
 <div id="askfile"></div>
</div>
```

Check:
```html
<div class="checktop"><div class="bignum" id="ckbig"></div><p id="cklint" class="howc"></p><button class="btn" data-lint id="lintbtn">Lint now</button></div>
<div id="linttbl"></div>
<div id="selfchk"></div>
```

Record:
```html
<div class="recbar"><button class="btn" data-order id="ordbtn">Newest first</button><button class="btn" data-dlwiki>Download the wiki</button><span id="dlpwrap" hidden><button class="btn" data-dlpages>Download changed pages</button></span></div>
<div id="reclog"></div>
<div id="rectens"></div>
<div id="recnote"></div>
```

OK, writing final now. I must be careful about size; let me be terse but complete. I'll write the JS in one <script> at end.

One more subtlety: `switchTab` should re-render target tab content each time (record, check).

Progress lines & running tab mark: `setRunning(on)` toggles tab3 label.

Let me handle "A running step goes on when you change tab; its tab then reads '03 INGEST · running'." — i.e., if ingest is busy and user is elsewhere, tab label shows running. Implement in renderTabs: tab3 text = '03 INGEST' + (ing&&ing.busy?' · running':''). Update on busy changes. Also aria-live? Add sr-only live region maybe; skip, put aria-live on progress lines.

Counting characters for announcements: prompt.length.

Ask filing preview: render the built page (renderMD of body) + frontmatter summary + tags input + File this page (disabled w/ reason) + Copy answer.

Build question body:

```js
function buildQPage(){
 const ans=ask.answer||'';const paras=ans.split(/\n\s*\n/);
 const short=paras[0]||'';
 const rest=paras.slice(1).join('\n\n');
 const links=[...new Set([...ans.matchAll(/\[\[([^\]|#]+)/g)].map(m=>m[1]))].filter(s=>pageBySlug.has(s));
 const srcIds=[...new Set(parsePins(ans).map(p=>p.id))];
 const title=(ask.title||'Untitled question').trim();
 const slug=uniqueSlug(kebab(title)||'question');
 const body='# '+title+'\n\n**Short answer.**\n\n'+short+'\n\n## Reasoning\n\n'+(rest||short)+'\n\n## What the library cannot answer\n\n'+(ask.cannot||'—')+'\n\n## Related\n\n'+(links.length?links.map(s=>'- [['+s+']]').join('\n'):'- (none)');
 const tags=(el('asktags').value.split(',').map(t=>t.trim()).filter(Boolean));
 const reg=[...new Set(srcIds.flatMap(id=>docRegister(id)))].filter(r=>REGNAMES[r]);
 return {slug,type:'question',title,frontmatter:{title,type:'question',tags,register:reg,status:'draft',updated:today(),links,sources:srcIds},body};
}
```
Hmm if answer is one paragraph, rest empty → Reasoning duplicates short. Acceptable-ish. Alternatively Reasoning = full answer always and Short answer = first paragraph. Duplication exists either way. Fine.

File: 
```js
P.push(qp);computeMeta();W.index=insertIndexLine(W.index,qp);W.log+='\n\n## ['+today()+'] ask | '+qp.title;session.changes.push({date:today(),kind:'ask',pages:[qp.slug]});renderHeader();message('Filed: '+qp.title);
```

All pins verify check: parsePins(ans).every(p=>accepted) where accepted = sent has key && verifyPin ok. Show reason when disabled.

Copy answer: navigator.clipboard.writeText(ask.answer). Fallback: create textarea. I'll write copyText helper with fallback.

Now — writing final output. Also credits line? I used wording from plan only; reference shelf excerpts not used. No credits needed. Maybe the A11Y checklist inspired but that's not a code/wording source; skip.

Let me count roughly as I write and stay tight.

Also careful: PINRE used with .exec loop and also .replace — both fine with /g as long as I reset lastIndex before exec loops (replace resets? replace with /g starts from 0 regardless? Actually String.replace with global regex ignores lastIndex and resets it to 0 after. But my exec loop sets lastIndex; subsequent replace calls start at 0 anyway? No — replace with global regex sets lastIndex to 0 before starting. Yes, replace resets. But to be safe, reset lastIndex=0 before exec loops.)

Now, tab 01 list rendering with groups in fixed type order: source, concept, entity, question.

Item: `<button data-page="slug">` title `· pins n · (regs)` + 'stub' mark.

Filter: match title, tags, slug lowercase includes query.

renderTab1View for main column.

Let me also compute "n of 40 pages" big number = filtered count.

Alright. Also the `howc` class = "How this is computed" small line.

Time to write the answer. I'll write the code in a compact but readable style. Given the size, comments minimal.

For ingest takeaways table pages chips: `<a href="#slug">` links (not buttons) fine.

Change card rendering with marked body: renderMD(marked,{slug,ingestDoc:id}).

Approve buttons: `data-approve` label "Approve change 3 of 9: title". Use aria-labelled via text.

File the approved changes button: data-file.

Also after filing: phase 'filed' shows summary + lint before/after. Keep lintBefore stored before applying (from last run or load-computed), lintAfter after.

session.changes entries for download: {date, kind, pages:[slugs]}.

Edge: ingest "no second ingest of same document": after filed, doc status 'ingested' so it leaves inbox list. Good. Also while ing is active, hide inbox buttons (ing set → stepper shown).

Stop behavior in runBatches: check ing.stop before each batch; after loop if stopped, phase stays 'takeaways' with note "stopped after batch k of n; kept what returned". If not all batches done and stopped — allow resume? Spec: "Stop keeps what has returned." I'll allow "Start" again to resume remaining batches (bi persists). The Start button in scope/table phase: label "Resume" if partial. Fine.

Takeaways dropped: takeaway.passage id not in the batch sent → drop, count. Show in checks.

Also coverage check: passages sent total vs doc.passages.length.

Now writing. (Also `el = id=>document.getElementById(id)`.)

Announce function for model calls: update a global live region? Each tab has its own progress line; for ingest: `ingprog` line inside stepper. I'll pass an announcer callback to callModel? Simpler: callModel returns; the caller sets progress before/after. But announcement of what left: I'll set progress text before calling.

session.passages incremented by caller (batches). Ask: 0.

Header: "Changes this session: n · Calls to the model: m · Passages that left the browser: k".

Let me write everything now, final.

Also `today()` = new Date().toISOString().slice(0,10).

Let me make sure verifyPin label check uses paragraph as stored (string) — 'para. '+x.paragraph. x.paragraph may be "5 (a)". label like "A/HRC/57/61, para. 5 (a)". includes works.

One more: chips for pins in position lines of contested blocks — they're pins to documents; fine.

`docRegister(id)`:
```js
function docRegister(id){
 const p=P.find(p=>p.frontmatter&&Array.isArray(p.frontmatter.sources)&&p.frontmatter.sources.length===1&&p.frontmatter.sources[0]===id);
 return p&&p.frontmatter.register?p.frontmatter.register.slice():['?'];}
```
Hmm "the source page whose sources is exactly [that id], else of the stub page" — both covered by the same find (first match). Good enough.

citeAs:
```js
function citeAs(id){
 const tally={};let n=0;
 for(const m of meta.values())for(const p of m.pins){if(p.id!==id)continue;n++;
  const mm=p.label.match(/^(.*?), (?:para\.|p\.)/);if(mm){tally[mm[1]]=(tally[mm[1]]||0)+1;}}
 if(n){let best=null,bc=0;for(const k in tally)if(tally[k]>bc){bc=tally[k];best=k;}if(best)return best;}
 const d=docById.get(id);return d?(d.symbol||(d.author+' '+d.year)):id;}
```

OK writing final file now. I'll aim for clarity and completeness. Let me go.

For the ingest stepper top line: "calls so far m · passages sent k" — session.calls & session.passages.

Also progress line aria-live.

Final check on clickables counts — acceptable.

Writing now, carefully, once.