This is a huge spec. I need to build a complete app in one HTML file, under ~1500 lines. Let me build the core faithfully but pragmatically. I'll structure carefully.

Key components:
- Load: parse pages, pins, backlinks, verify.
- Tabs 01-05 with hash routing.
- 01 PAGES: list + filter, index display, page render with pins, contested cards, links out/from, sources, copy markdown.
- 02 ASK: two calls, answer rendering, filing question page.
- 03 INGEST: 4-step flow.
- 04 CHECK: lint + checks panel.
- 05 RECORD: log, tensions, downloads.
- Header/footer with counters.

I'll write a compact but complete implementation. Let me plan the code structure:

```js
const W = WORKSHOP_DATA.wiki, LIB = WORKSHOP_DATA.library;
const P = W.pages, D = LIB.records;
slugMap, docMap.
norm(s), verifyPin(pin) -> {ok, reason, passage}.
parsePins(body), parseLinks(body).
state: session {changes:0, calls:0, chars:0, passagesSent:0, logAdded:[], changesList:[]}.
renderPageBody(body, opts) -> DOM, handling headings, bold, italic, lists, pins, links, contested blocks.
```

Markdown rendering: I'll write a simple renderer that processes blocks: headings (#, ##, ###), fenced ```contested blocks, lists (- / 1.), bold/italic inline, pins, [[links]], [text](url) plain links.

Pin chip: quoted text + chip with label button (openSource), register, verification words; expand arrow showing passage detail.

Contested card: claim heading, verdict large serif, note, lean bar, positions table.

For ask: prompts, studio.ask with json, parse, render answer inside data-source="ai". Pin regex to find pins in answer; accept if same id+page+quote exists in sent pages and verifies.

Ingest: batch passages, takeaway calls, verification, failed with nearest passage, source page call, touched page calls, review cards, approve/reject, file.

Lint: checks list.

Given size constraints I'll aim for maybe 1200-1400 lines. Let me write it.

Helper: mdInline(text) escaping HTML, handling **bold**, *italic*, [[slug]], [label](pin:...) ✓/⚠, [text](http...). Actually easier: render line-by-line, first escape HTML, then replace inline patterns. For pins I need to build chips with buttons — so inline replacement should produce HTML with placeholders. I'll do: for inline text, run a sequence of regex replacements to HTML. Since I escape first, quotes become &quot; etc. — careful: pin quotes contain `"` which after escaping becomes `&quot;`, and pin syntax `"([^"]*)"` won't match escaped text. Better approach: extract pins from the raw text first, replace with placeholder tokens, then escape the rest, then replace placeholders with chip HTML.

Plan for renderBody(body, ctx):
- Split into blocks: lines; detect fenced blocks starting with ```contested and ending ```.
- Within normal blocks: group consecutive list items; headings; else paragraphs (blank-line separated).
- For each text chunk: tokens = []; replace pins first (regex with quotes intact), then [[...]], then plain links [..](url), then escape remainder, then bold/italic on escaped text? Bold markers ** work fine after escaping. Apply bold/italic to escaped text — fine.

Chips need unique ids? I'll just generate HTML strings with data attributes and attach handlers after insertion via delegation. Use event delegation on document for .pin-label buttons (openSource), .pin-expand toggles, etc. That simplifies a lot. Pin data stored in data-* attributes (quote, id, page). Verification status computed at render time — I'll compute per pin and embed result.

verify(pin): find doc, find passages with page === pin.page; check label contains "para. "+paragraph or "p. "+page_label; check fragments in order in norm(passage.text). Return {ok, passage, reason}.

Register of document: find source page with sources exactly [id]; else stub with sources [id]; else "?".

CiteAs(doc): most frequent prefix before ", para." or ", p." in pins across wiki to that id; else symbol or author+year.

Lean bar: weights {a:5,b:4,c:3,d:2,e:1,f:0.5}.

Contested block parse: lines claim:, verdict:, note:, then position lines starting with + - ~.

Page render: header badges, tags, body, links out (mark frontmatter-only), linked from, sources list, copy markdown button.

Index render: render like a page — parse W.index markdown via renderBody? Index has [[slug]] links; my renderBody will linkify them (need to make [[slug]] clickable to open page). Yes — handle [[slug]] in renderBody generally: link with text = title of slug if exists else slug + "no page".

Ask flow:
- textarea + Ask button.
- Step 1: prompt with index + question → JSON {pages}. Show chips with Change pages link → checkboxes list.
- Step 2: bodies + question → JSON {title, answer, cannot_answer}. Render answer like a page but pins validated against sent pages.
- Filing card: build page object, preview, File button disabled until all pins verify.
- Stop button via Escape / abort flag.

askModel(prompt, meta): increments counters, aria-live progress, awaits studio.ask, parse JSON (try JSON.parse; strip fenced block; try again). Return parsed or throw {raw}.

Ingest flow: state machine with abort flag.
- Step 1 panel: batches table, Start.
- Run batches sequentially; takeaways accumulate (verified) + failed.
- Step 2 table + failed box.
- Step 3: two buttons sequentially: Draft source page, Draft changes.
- Step 4: change cards; approve/reject; File.

Building drafts:
- Source page call: prompt with takeaways pins, doc meta, anatomy; returns {one_liner, body, touches}. Code re-verifies pins in body, builds frontmatter, keep touches ≤12.
- New pins format: `[citeAs, para. N](pin:id#pP "quote") ✓` — build from takeaway: passage found by id.
- Touched page call: returns {edits:[{after, markdown}], contested}. Insert markdown at end of heading section. I'll implement insertAfterHeading(body, heading, markdown): find line matching `#`s heading text, insert before next heading of same-or-higher level or end.

Change card: page with inserted paragraphs highlighted. To track inserted paragraphs: when building the edited body, I know inserted chunks; for rendering diff I'll render the new body but wrap inserted chunks... simpler: render body normally, but mark inserted paragraphs by keeping a list of inserted raw strings; when rendering, compare paragraph raw text to inserted list and add class. I'll render with renderBody(body, {highlight: Set of raw paragraph strings}).

Tensions entry on file for new contested cards.

Lint checks: compute each; table rows with count + links.

05 RECORD: log render newest first with switch; tensions render; download buttons.

Hash routing: on load, if location.hash matches slug, open tab 01 with that page.

OK, let's also do the "How this is computed" lines. And checks panel on tab 04.

Let me now write the code. I'll be economical with comments. Aim ~1300 lines.

Key CSS: paper theme per system prompt.

Let me write it.

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
header, tabs, panels, footer
<script>...</script>
</body>
</html>
```

Tab panels: five sections. Let me draft the HTML skeleton:

Header: label, title, data line; right: counters strip.

Tabs: buttons role=tab.

Tab 01: two columns: aside (filter input, big number, page list grouped by type), main (index or page).

Tab 02: grey box, textarea, ask button, progress line, step1 chips, answer area, filing card.

Tab 03: inbox buttons / stepper with steps.

Tab 04: big number, lint button, table, checks panel.

Tab 05: switch, log, tensions, method note, download buttons.

JS core structures:

```js
const S = {calls:0, chars:0, passages:0, changes:0, approved:[], logAdded:[], newTensions:[], filedPages:[], stop:false, askAnswer:null};
```

Let me write render functions.

escapeHtml(s).

norm(s):
```js
function norm(s){return s.normalize('NFKC').replace(/[\u201C\u201D\u201E]/g,'"').replace(/[\u2018\u2019]/g,"'").replace(/[\u2013\u2014]/g,'-').replace(/\u00AD/g,'').replace(/- (?=[a-z])/g,'').replace(/\s+/g,' ').trim();}
```
Wait "a hyphen followed by whitespace → ''" — that would join "decision- making"→"decisionmaking" not "decision-making". Hmm spec says '"decision- making" = "decision-making"'. So hyphen+space → remove the space? No: replace(/-\s+/g,'-')? That gives "decision-making". But spec literally says "a hyphen followed by whitespace → ''" then claims result is "decision-making". Contradiction in spec; follow the intent: `-\s+` → `-`. Actually if we remove the hyphen and space: "decisionmaking". The stated example is "decision-making", so replace "- " with "" gives "decisionmaking"? No — "decision- making" with "- " removed = "decisionmaking". The example says decision-making. So the intended rule: remove the whitespace after a hyphen, i.e., `.replace(/- /g,'-')`. I'll do that.

verifyPin:
```js
function verifyPin(p){ // p: {label,id,page,quote,mark}
 const doc=docMap[p.id];
 if(!p.quote) return {ok:false,reason:'pin has no quote'};
 if(!doc) return {ok:false,reason:'unknown document'};
 if(doc.status==='inbox') return {ok:false,reason:'document still in the inbox'};
 const frags=(p.quote.split(/\u2026|\.\.\./)).map(norm).filter(Boolean);
 let best=null;
 for(const x of doc.passages){ if(x.page!==+p.page) continue;
   const t=norm(x.text); let pos=0,all=true;
   for(const f of frags){ const i=t.indexOf(f,pos); if(i<0){all=false;break;} pos=i+f.length; }
   const labelOk = x.paragraph!=null ? p.label.includes('para. '+x.paragraph) : p.label.includes('p. '+x.page_label);
   if(all&&labelOk) return {ok:true,passage:x,doc};
   if(all) best={ok:true,passage:x,doc,labelMismatch:true}; // quote found but label mismatch
 }
 return {ok:false,reason:'quote not found on PDF page '+p.page+(best?' (quote found but label does not match)':'')};
}
```
Hmm label mismatch should be not verified. I'll simplify: require both; if quote found but label mismatch, reason accordingly.

Pin parsing per page: cache on page object: page._pins, page._links, computed lazily.

Rendering body. I'll write:

```js
function inlineHTML(text,page,opts){
 // extract pins, wikilinks, plain links -> tokens
}
```

Implementation: use a combined regex approach with placeholders:

```js
function inlineHTML(raw,opts){
 let out=[];
 let s=raw;
 const toks=[];
 s=s.replace(PIN_RE,(m,label,id,page,quote,mark)=>{toks.push(pinChip({label,id,page:+page,quote,mark},opts));return '\u0001'+(toks.length-1)+'\u0001';});
 s=s.replace(/\[\[([^\]|#]+)(?:\|[^\]]*)?\]\]/g,(m,slug)=>{toks.push(wikiLink(slug));return '\u0001'+(toks.length-1)+'\u0001';});
 s=s.replace(/\[([^\]]+)\]\((https?:[^)\s]+)\)/g,(m,t,u)=>{toks.push(`<a href="${u}" target="_blank" rel="noopener">${esc(t)}</a>`);return '\u0001'+(toks.length-1)+'\u0001';});
 let h=esc(s);
 h=h.replace(/\*\*([^*]+)\*\*/g,'<strong>$1</strong>').replace(/\*([^*]+)\*/g,'<em>$1</em>');
 h=h.replace(/\u0001(\d+)\u0001/g,(m,i)=>toks[+i]);
 return h;
}
```

But pins contain quotes in label etc.; PIN_RE on raw works. Note pin regex needs the ✓/⚠ mark optional? Spec says mark always present. Keep as spec. But answers might have pins without mark? Prompt says pin syntax; I'll make mark optional `(?:\s*(✓|⚠))?`.

Problem: pin regex `\[([^\]]+)\]` label may contain ] ? No, [^\]]+. Quotes inside quote attr: `"([^"]*)"` — if quote contains straight " it breaks; code converts to curly when building new pins. Fine.

Block-level render:

```js
function renderBody(body,opts={}){
 const lines=body.split('\n');
 let html='',i=0;
 while(i<lines.length){
  const L=lines[i];
  if(/^```contested/.test(L)){ // collect until ```
   let j=i+1,buf=[]; while(j<lines.length&&!/^```/.test(lines[j])){buf.push(lines[j]);j++;}
   html+=contestedCard(buf.join('\n'),opts); i=j+1; continue;}
  const h=L.match(/^(#{1,3})\s+(.*)/);
  if(h){const lv=h[1].length+1; html+=`<h${lv}>${inlineHTML(h[2],opts)}</h${lv}>`;i++;continue;}
  if(/^\s*[-*]\s+/.test(L)){ let buf=[]; while(i<lines.length&&/^\s*[-*]\s+/.test(lines[i])){buf.push(lines[i].replace(/^\s*[-*]\s+/,''));i++;}
   html+='<ul>'+buf.map(x=>`<li>${inlineHTML(x,opts)}</li>`).join('')+'</ul>';continue;}
  if(/^\s*\d+\.\s+/.test(L)){ similar ol }
  if(!L.trim()){i++;continue;}
  // paragraph until blank
  let buf=[L];i++; while(i<lines.length&&lines[i].trim()&&!/^(#{1,3}\s|```|\s*[-*]\s|\s*\d+\.\s)/.test(lines[i])){buf.push(lines[i]);i++;}
  const rawP=buf.join(' ');
  const cls=opts.highlight&&opts.highlight.has(rawP)?' class="ins"':'';
  html+=`<p${cls}>${inlineHTML(rawP,opts)}</p>`;
 }
 return html;
}
```

Pin chip:
```js
function pinChip(p,opts){
 const v=verifyPin(p);
 const reg=docRegister(p.id);
 const ok=v.ok;
 // strike-through for ask answers when not on sent pages
 let cls='pinchip'+(ok?'':' bad')+(p._struck?' struck':'');
 ...
}
```
Chip content: `“quote”` then chip: label button (opens source), register letter, "✓ verified"/"⚠ not found", plus "page says ✓" if differs from mark. Expand arrow → passage paragraph/page_label + first 300 chars + Open PDF page button. Store pin JSON in data attr (escape).

Events: delegate clicks:
- .pin-open: read data → studio.openSource(id,page,quote)
- .pin-x: toggle next sibling detail
- .wikilink: open page
- tab buttons, filters, etc.

Contested card parse:
```js
function parseContested(buf){
 lines; claim/verdict/note by prefix 'claim:' etc.; positions lines matching /^([+~-])\s+(.+)$/ split ' | '.
}
```
Position line: `+ c | [pin](...) ✓ | gloss | [[slug]]`. Split on ' | ' — but the pin contains ' | '? Unlikely; label contains ", p. 34" no pipes. OK.

Lean: weights map; pos weight = w[reg]. support = sum('+')+0.5*sum('~'); total=sum all. pct.

Positions table: columns sign in words (supports/contests/mixed), register, pin chip, gloss, page link.

Contested in ask answers? Model answers use plain pins; fine.

wikiLink(slug): if slugMap has slug → `<a class="wikilink" data-slug>title</a>`; else red `<span class="dangling">slug</span> · no page`. Links should navigate to tab 01 page.

Page view (tab 01): function showPage(slug). List rendering with filter. Group by type in fixed order: source, concept, entity, question.

Header counts update function updateCounters().

Copy page as markdown: frontmatter as YAML + body → clipboard via navigator.clipboard fallback textarea.

ASK tab:

Prompt construction. Step1:
```
index + "\n\nQuestion: ..." + "\nReturn JSON {\"pages\":[\"slug\",...]} with at most five slugs from the index that bear on the question. Pin syntax: [label](pin:ID#pPAGE \"quote\") ✓ ..."
```
Hmm "Every prompt states the pin syntax and 'quote only words that stand in the passages given; the code will check'." Even for slugs step. Include a line.

Step 2: bodies + question → {title, answer, cannot_answer}. Prompt: answer ≤350 words; pins must already stand on the pages sent — "use only pins that appear verbatim in the pages below"; name register where it matters; keep document's own verb; never present (c)-(f) as treaty requirements.

Render answer: renderBody inside div data-source="ai", with opts.sentPages = set of "id#page|normquote"? Validation: pin accepted when same id+page and same quote exists in a sent page's body and verify true. I'll precompute set from sent pages' pins: key id+'#'+page+'|'+norm(quote). If not in set or !verify → struck with note "not on the pages sent".

Count line: verified pins by register: "a 2 · b 1 · c 4 ...".

Filing card: build page:
- slug: kebab from title, ensure unique (append -2).
- tags: user input (comma separated).
- register: from pinned docs.
- body: `# title\n\n**Short answer.** ...\n\n## Reasoning\n\n<answer>\n\n## What the library cannot answer\n\n<cannot>\n\n## Related\n\n- [[slug]]...` links from [[slugs]] in answer.

Actually "**Short answer.**" then what? Spec: body = "# title", "**Short answer.**", "## Reasoning" (the answer)... I'll put "**Short answer.**" followed by the first sentence? Simpler: put the title heading, then "**Short answer.**" then the answer text under "## Reasoning". I'll do: `# {title}\n\n**Short answer.**\n\n## Reasoning\n\n{answer}\n\n## What the library cannot answer\n\n{cannot}\n\n## Related\n\n{links bullets}`. Preview rendered. File button disabled until every pin verifies (with reason shown).

On file: push page, update index (add line under Questions... simpler: append line to index under a "Questions" heading if present, else append). Spec says "its line to the index under Questions". I'll try to insert after a line matching "## Questions" section; fallback append. Log: `## [today] ask | title`. Update counters, re-render, show "Filed" aria-live.

INGEST tab. State object ingest = {doc, step, batches, takeaways:[], failed:[], drafts:[], changes:[], decisions:[]}.

Step 1 panel with batches table (paragraph ranges, pdf pages), Start button.

Run batches: for each batch, prompt:
```
Passages: JSON [{id,page,paragraph,text}]
Index
Return JSON {takeaways:[{claim,quote,passage,pages}]} at most 10; quote 8-40 words copied verbatim from that one passage; pages = slugs from the index the claim bears on.
Pin syntax: ... quote only words that stand in the passages given; the code will check.
```
Progress line, Stop (abort flag). On each return: parse; for each takeaway: find passage by id among sent (coverage check); build pin: citeAs + ", para. N"/", p. label", quote with straight " → curly; verify. Keep pages to existing slugs; collect proposed new slugs (not existing) — keep at most two new slugs per ingest (across all). Failed go to failed[] with nearest passage.

Nearest passage: among passages on that page, longest run of consecutive normalised words shared with quote. Implement: words of quote; for each passage on page, for each start in quote words, extend match... simpler: longest common substring on word level via dynamic-ish: for each i in quote words, j in passage words count consecutive equal. O(n*m) fine for small.

Step 3: button "Draft the source page (1 call)" then "Draft the changes to n pages (n calls)".

Source page call prompt: verified takeaways pins (ready-made pin markdown), citeAs, doc title/author/published/pages/url, anatomy, return {one_liner, body, touches}. Code: re-verify pins in body (drop/flag non-verified? "The code re-verifies every pin in body" — mark them; I'll count and show; keep pins that verify, mark others not found—actually for a draft, pins that fail should be flagged. I'll keep them rendered as not found and count in card). Build page: type source, register from stub (register of stub page's frontmatter... "register from the stub" — stub page register letters), sources [id], links from body, tags from touched slugs. touches: keep to existing or allowed new slugs, at most 12, stub added if missing.

Touched page call per slug (from touches ∪ takeaway pages ∪ stub): prompt with page body, takeaways for that slug with pins, return {edits:[{after,markdown}], contested}. Insert each markdown at end of named heading's section; heading not found → end of page with a note. Re-verify pins; add link both ways in links; add id to sources.

Contested: parse block from string; if present, add to body (append at end) and record for tensions.

Change cards (step 4): for each changed/new page: fieldset with legend title+type, "new page"/"edited", counts of paragraphs inserted and pins added (verified and not), body rendered with highlight of inserted paragraphs. Buttons Approve/Reject, "change i of n". Sequential display: show one card at a time.

After last decision: "File the approved changes" button → apply: pages replaced/added with updated today; index updates: source line under Sources, stub line replaced, touched pages' N recomputed, first line rebuilt; log entry appended; tensions entries for new cards; doc.status='ingested' (in memory); lint re-run. Session changes count updated.

Index manipulation: index is markdown with lines. First line contains pins count — rebuild via regex replace `/\d[\d,]* pins/` with new count. Lines like `- [[slug]] — one-liner · (letters) · ✓N`. To update a page's line: find line starting `- [[slug]]`; replace or insert. New line format per spec.

Log entry text per spec: "## [date] ingest | symbol: short_title\n\nRead n passages (cite-as, register (x)). Wrote [[slug]]. N pins in all; besides its own page, pinned on k pages: [[…]]. Rejected: [[…]]." I'll follow.

Tensions entry: `### slug-of-claim` — slug from claim; title, status mapping, card: [[page]], poles and where from positions. I'll generate a reasonable block.

CHECK tab: big number verified pins/total, lint count. Lint table with checks per spec (~13 checks). "Lint now" runs (or auto on load? "Nothing is called on page load" refers to model; lint is code, fine to compute on load — but spec says button "Lint now" reads "Re-run" after first run, implying it runs on click. I'll compute on load too silently? The checks panel is "open by default, under the table" — panel of self-checks. I'll run lint on load and show results, button says "Re-run". Actually simpler and honest: run on load, label button "Re-run". Hmm spec: "One button, Lint now, which reads 'Re-run' after the first run." Ambiguous; running on load is fine.

Lint checks:
1. dangling links
2. orphans (no backlinks... orphan = page with no bodyLinks and no backlinks? Orphan = nothing links to it and it links nowhere? Standard: no other page links to it. Index links? I'll define: no page's bodyLinks or frontmatter.links contain it → orphan.)
3. pins not verified by code
4. pins marked ✓ that fail
5. sources ≠ pinned docs
6. pages with no pins
7. links not reciprocated (frontmatter.links not in body links? "links not reciprocated" — frontmatter.links vs bodyLinks differ, and body links not in frontmatter.links; spec earlier: "frontmatter.links and body links differ on 5 entries". Check: symmetric difference non-empty → count.)
8. pages missing from index / index lines without page
9. index ✓N differs from computed
10. contested cards without tensions entry and reverse
11. stub pages
12. pins to inbox document

Each row: name, count, "pass"/"check", pages as links.

Checks panel: pin count vs index statement, verified, labels, structure, model answers (populated during session), coverage, unverified, approval, filing, session. I'll render dynamically-ish: mostly static lines with computed values.

RECORD tab: log rendered: split on `## [` entries; render each collapsible (details/summary — but "nothing opens in a modal", details is fine). Newest first toggle. Tensions: split on `### ` entries; each card: title, status, card: [[page]] link. Method note, download buttons.

Download: JSON blob of wiki shape {title, source, built, count, pages, index, log, tensions, schema, changes, library_status}; save via a.download. Markdown of changed pages joined with `---`.

Hash routing: on load and on tab 01 page open, set location.hash = slug. hashchange listener.

Tab running marks: when ingest running, tab 03 label adds "· running" (aria-live on it? put aria-live on a hidden status). Keep simple: update tab text and a status span.

Keyboard: tablist arrow keys. Escape → stop running step (set S.stop=true).

OK, prompts must be strings; characters sent counter: add prompt.length. Passages sent: count passage objects in prompt (for ingest calls; ask = 0).

Let me now count clickables constraints — fine.

Time to write. I'll be disciplined; target ~1200 lines. Also add "How this is computed" lines near key numbers.

Also the Ask grey box: "states what each step will send before it goes" — static text describing both steps.

Filing register from pinned docs; count line under answer.

For the answer's pins validation: parse pins from answer text with PIN_RE (mark optional), key check.

Write now. Also `studio.ask` may not exist? It exists in environment. Guard anyway with try.

For openSource: `studio.openSource(id, page, quote)`.

Let me write the file.

Details on step counters: "Changes this session: n · Calls to the model: m · Passages that left the browser: k".

updateHeader() recalculates: pins verified by this page (recompute lazily — cache per page; after changes, invalidate).

I'll maintain a global verification cache Map pinKey → result, cleared when doc status changes (ingest affects inbox doc pins — inbox pins were unverified; after ingested they'd verify... but pins to A/HRC/57/61 stub: 0 pins to it per plan, fine; still clear cache after filing).

Now write.

For inserting markdown after heading:

```js
function insertAfterHeading(body, heading, md){
 const lines=body.split('\n');
 let idx=-1;
 for(let i=0;i<lines.length;i++){const m=lines[i].match(/^(#{1,3})\s+(.*)$/); if(m&&m[2].trim()===heading.trim()){idx=i;break;}}
 if(idx<0) return body+'\n\n'+md+'\n\n<!-- inserted at end: heading not found -->';
 const lvl=lines[idx].match(/^#+/)[0].length;
 let j=idx+1; while(j<lines.length&&!(lines[j].match(/^#{1,3}\s/)&&lines[j].match(/^#+/)[0].length<=lvl)) j++;
 return lines.slice(0,j).join('\n')+'\n'+md+'\n'+lines.slice(j).join('\n');
}
```

Track inserted paragraphs: collect md strings; when rendering diff, highlight paragraphs whose raw text matches any inserted md paragraph line. I'll normalize comparison: build Set of norm of each non-empty line of inserted mds; in renderBody, check set for norm(rawP).startsWith? Paragraphs may join lines. I'll compare norm(rawP) against set of norm of joined inserted paragraph blocks — hard. Simpler: highlight check via `highlight` set of norm-strings; when building the edited body I process each insertion separately and know its md; I'll precompute set of norm(md lines joined). Compare norm(rawP) === one of them, or rawP includes a marker... Use norm inclusion: if any inserted string h has norm(rawP)===norm(h) → highlight. Inserted md may contain heading or list; those won't highlight — acceptable-ish, but better: also highlight list items. Keep simple: highlight exact norm matches of inserted paragraph-ish chunks and list items. I'll compute highlight set as: for each inserted md, split into blocks, norm each block's text.

Actually simpler: since insertion happens at known point, I could wrap inserted content in markers in the body and strip them when filing. E.g. insert `\u0002md\u0003`. renderBody detects \u0002...\u0003 spans and wraps in class ins. Filing strips markers. That's clean! Do that.

So edited body stored with markers; on Approve/File, strip `\u0002` and `\u0003`. Render: escape first... markers survive escape (unicode control chars — esc won't touch). In inlineHTML after esc, replace `\u0002`→`<mark class="ins">`? But markers may span blocks. Handle in renderBody at line level: lines starting with \u0002 → open highlight until line containing \u0003. Implement: maintain flag; when splitting paragraphs, if text contains markers, split into segments... Simplest: in renderBody, before processing, I handle a line-based approach: if a line starts with '\u0002', set ins=true and strip; if line ends with '\u0003', close after. Paragraph class picks up flag. Lists/headings inside insertion: wrap with class too — I'll add class to ul/h tags when flag active. Good enough.

Contested block inside inserted md: lines within markers; my contested detection happens before... order: detect ```contested first; markers on surrounding lines fine.

OK. Writing final code now. Keep functions tight.

One more: page list item shows register letters and pin count, stub tagged.

Filter: matches title, tags, slug (lowercase includes).

Let me write everything out.

For the ASK "Change pages" — after step 1, chips of slugs + a "Change pages" link toggling a checkbox list of all pages. Then step 2 auto-runs after selection? Spec: step 1 shows chips; step 2 sends those pages. I'll auto-continue to step 2 after step 1 (with ability to change pages before? The Change pages link is shown with chips — then a "Send these pages" happens as part of step 2 automatically). I'll do: after step 1 returns, show chips + "Change pages" toggle; automatically proceed to step 2 with the returned pages; changing pages afterwards offers "Ask again"? Simpler: after step 1, show chips and a "Continue with these pages" button plus Change pages toggle... but clickable budget. Spec: "Step 2 sends those pages' bodies" — automatic. Change pages lets you tick others, and then... presumably re-run step 2. I'll add: when user changes selection via checkboxes, show a small "Send these pages" button that runs step 2. That stays within budget when open.

Actually to keep clickables ≤7: tabs(5)+Ask+File as a question page =7; the send-pages button appears transiently. Fine.

Escape key: global, sets S.stop=true.

Progress lines: aria-live polite.

Now the code. Also handle empty states.

Let me also remember: "Before the code block: at most three short sentences... After it: nothing."

Write it.