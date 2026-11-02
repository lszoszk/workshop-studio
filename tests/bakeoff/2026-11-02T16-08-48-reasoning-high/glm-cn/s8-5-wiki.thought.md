Let me build this app carefully.

Requirements:
1. Sidebar with 8 predefined concepts (each with base term + synonyms where specified: lie detection also "deception detection", "brain fingerprinting"), showing passage counts. Plus "Add a concept" input.
2. Page heading: concept name and the terms that find it.
3. Table "Passages by kind of document": rows per kind, total.
4. Passages grouped by document, in library order. Group heading: short_title, kind, year, symbol linked to url (or author if no symbol). Each passage: citation as link calling studio.openSource(id, page), section if any, text folded after three lines (click to expand).
5. "Related concepts": other concepts found in same passages, as links.
6. Button "Draft a summary": sends first 12 passages, uses studio.ask, answer in box labeled "Written by AI. N passages were sent to the model and left the browser", inside data-source="ai".

Rules:
- Match: text contains term, case-insensitive, line breaks ignored. I'll normalize text: lowercase, replace whitespace/newlines with space. Terms too.
- Show text character for character; fold via CSS (max-height + overflow hidden, click to expand).
- Citation: symbol + ", para. " + paragraph when paragraph set; otherwise author, year, p. page_label. Journal articles cited by surnames: "Szoszkiewicz & Yuste" (two authors), "Prainsack et al." (3+). Other docs by author as written. So for journal articles I need to derive surnames from author field. Author fields: "Łukasz Szoszkiewicz and Rafael Yuste" → "Szoszkiewicz & Yuste". "Prainsack et al."? Let me check: author "Barbara Prainsack, ... " — actually sample shows "Prainsack-et-al-2022" record but not its author field. The doc description says journal: Prainsack-et-al-2022 (Journal article, 2022: Data solidarity, The Lancet Digital Health). Author probably "Barbara Prainsack and Nikolaus Forgó and..." Hmm. I'll write a surname extractor: split author on " and ", ",", ";", also handle "et al." If 1 surname → that; 2 → "X & Y"; 3+ → first + " et al.". But the spec explicitly says: "Szoszkiewicz & Yuste"; "Prainsack et al." for three or more. So compute surnames generically: for each author name part, take last word as surname. Split on " and " and commas. But careful: "UN Secretary-General" is not a journal article. Only journal articles get surname treatment; others use author as written.

For Prainsack: author might be "Barbara Prainsack, Nikolaus Forgó, Alena Buyx" or similar. Extracting surnames: split on " and " / "," gives three names → "Prainsack et al.". Good.

Edge: name "Łukasz Szoszkiewicz" → surname "Szoszkiewicz". Fine.

- openSource gets page (PDF page), never page_label.
- No symbol → show author in group heading. In citation too: "no symbol → show author" — wait, the citation rule: "symbol + ', para. ' + paragraph when paragraph is set; otherwise author, year and printed page". So journal articles have symbol null, paragraph null → author-year-page citation with surname form. What if a doc has no symbol but has paragraph? Then citation rule says: when paragraph is set, use symbol + para. But no symbol... The library docs: journal articles have paragraph null. Others have symbols. I'll handle: if symbol and paragraph → "symbol, para. N". Else → authorCitation + " " + year + ", p. " + page_label. If no symbol but paragraph set, fall back to author form with para? Keep simple: if symbol exists and paragraph != null → symbol para form; if symbol exists and paragraph null → maybe symbol + ", p." + page_label? Spec says "otherwise author, year and printed page". I'll follow spec exactly.

- Empty state: "No passage uses this term", no button.

Concepts list:
- mental privacy: ["mental privacy"]
- freedom of thought: ["freedom of thought"]
- self-incrimination: ["self-incrimination"] — also "self incrimination"? Spec says no synonyms; keep term as given. Hyphenated term. Maybe include "self-incrimination" only.
- lie detection: ["lie detection", "deception detection", "brain fingerprinting"]
- consent: ["consent"]
- neural data: ["neural data"]
- data solidarity: ["data solidarity"]
- proportionality: ["proportionality"]

Added concepts via input: term = the typed term (single term). Press Enter adds.

Related concepts: for current concept, look at its passages; other concepts (from full list including added) whose terms also appear in any of those passages. Show as links.

Draft summary: first 12 passages on the page (in the order displayed — grouped by document, library order). Prompt lists passages with citations and asks for three sentences each ending with the citation it rests on. Show label. data-source="ai" on the answer box. Let user stop? The studio rules say show progress and let user stop — the plan says "where it says nothing, keep it simple". The general system rules say: batch (max 25 per call — 12 is fine), show progress, let user stop. I'll disable button and show "Contacting model…" text; a Stop button maybe. Keep simple: button becomes disabled with "Asking the model…". Maybe add a stop via AbortController-ish — studio.ask doesn't support abort presumably. Keep simple: progress text. Actually rules say "let the user stop" — but plan says keep simple where nothing specified. I'll add a simple stop isn't possible without abort support. I'll just show progress. Hmm, to be safe, I could implement a "Cancel" that sets a flag ignoring the result. That's cheap. Let me add that.

Fold after three lines: CSS line-clamp with -webkit-line-clamp: 3, click to expand toggles class. line-clamp hides but doesn't shorten text — good. Use `-webkit-line-clamp` and standard `line-clamp`. Click on passage text toggles.

Layout: sidebar left (~260px), main content right. Responsive-ish but laptop screen fine.

Table: rows per kind present in the matched passages? Or all kinds? "one row per kind, and a total" — I'll show kinds that appear among matched passages, or all kinds in library with counts (some zero)? Test says "the table rows add up to its total" — either works. "the Journal article row is not zero" — implies Journal article row exists. I'll show all kinds present in the library (so the table is stable), with counts, total row. Actually simpler and informative: all kinds in library order of first appearance. Rows add to total of matched passages. Good.

Related concepts: exclude current concept. Link clicking navigates.

Sidebar counts: passage counts per concept (computed over whole library).

Header: title "Neurotechnology & Justice — Concept Wiki" or similar, one-line description: source title, n documents, years range.

Document order: library order (records array order). Group passages by document, in library order — even documents with zero passages for the concept are skipped (only show documents with matching passages).

Group heading: short_title, kind, year, symbol linked to url. If no symbol → author (linked to url presumably). Spec: "symbol linked to url" and "No symbol → show author". I'll link whatever is shown.

Passage citation link: <a href="#" onclick="studio.openSource(id, page)">citation</a>. Prevent default. Note id here is document id? "studio.openSource(id, page) opens that document's PDF at that PDF page" — id is the document id (e.g. "A/81/351"). The passage has id like "A/81/351#1". Document id = passage.id.split("#")[0]? Safer to carry doc record. I'll group by doc, so I have doc.id.

Citation for journal: "Szoszkiewicz & Yuste 2025, p. 3471". Format: surnameCite + " " + year + ", p. " + page_label.

Author surname extraction:
```js
function journalCite(doc){
  const parts = doc.author.split(/,| and |;/).map(s=>s.trim()).filter(Boolean);
  const surnames = parts.map(p => p.split(/\s+/).pop());
  if (surnames.length === 0) return doc.author;
  if (surnames.length === 1) return surnames[0];
  if (surnames.length === 2) return surnames[0] + " & " + surnames[1];
  return surnames[0] + " et al.";
}
```
"Łukasz Szoszkiewicz and Rafael Yuste" → ["Łukasz Szoszkiewicz", "Rafael Yuste"] → "Szoszkiewicz & Yuste". Prainsack author maybe "Barbara Prainsack, Nikolaus Forgó and Alena Buyx" → three → "Prainsack et al.". Good. Edge: "et al." already in author? Unlikely.

Matching function:
```js
const norm = s => s.toLowerCase().replace(/\s+/g, " ");
function passageUses(passage, terms){
  const t = norm(passage.text);
  return terms.some(term => t.includes(norm(term)));
}
```

Concepts state: array of {name, terms}. Default list plus user-added.

Rendering: re-render main content when concept selected; re-render sidebar when concept added.

Related concepts computation: for each other concept, check if any passage in current set matches its terms.

Summary prompt:
```
You are helping diplomats and human rights staff research neurotechnology and justice.
Below are N passages from UN and academic documents on the concept "X".
Write exactly three sentences summarizing what these passages say about "X".
Each sentence must end with the citation (in parentheses) of the passage it rests on.
Use only the passages below.

[1] Citation: "text"
...
```
Parse answer as plain text (not JSON). studio.ask(prompt) without json option.

Label: "Written by AI. N passages were sent to the model and left the browser." N = number actually sent (min(12, count)).

Fold: click anywhere on the text toggles. Add cursor pointer and a small hint "click to expand". Use class .folded with line-clamp 3.

Styling: system font, #1f6fb2 accent, light bg, 16px base.

Empty passages: "No passage uses this term" and no Draft button. Also table? Show table with zeros probably fine, and related concepts none. Keep heading + message.

Also description line: `${lib.title}, ${lib.count} documents`. Years: compute min/max from records. Fine.

Let me also handle: "Add a concept" input: Enter adds concept with term = typed value; select it. Duplicate name — just add anyway or ignore; keep simple, if name exists just select it.

Line count: keep under 700. Should be ~450.

Escape HTML for text display (character for character). Use textContent where possible, or escape function.

Let me write the code.

Structure:
```html
<!doctype html>
<html>
<head><meta charset="utf-8"><title>...</title><style>...</style></head>
<body>
<header>...</header>
<div class="layout">
  <nav id="sidebar"></nav>
  <main id="page"></main>
</div>
<script>...</script>
</body>
</html>
```

JS:

```js
const lib = WORKSHOP_DATA.library;
const docs = lib.records;

const norm = s => (s||"").toLowerCase().replace(/\s+/g," ");
const uses = (p, terms) => terms.some(t => norm(p.text).includes(norm(t)));

let concepts = [
 {name:"Mental privacy", terms:["mental privacy"]},
 ...
];
```
Concept names: display capitalized. Sidebar shows "Mental privacy (n)". Heading shows concept and terms.

Default concepts with names: mental privacy, freedom of thought, self-incrimination, lie detection (terms: lie detection, deception detection, brain fingerprinting), consent, neural data, data solidarity, proportionality.

State: current = concept name or null. On load show... first concept? Or a welcome? Plan doesn't say. I'll show first concept selected by default (mental privacy). That's reasonable and not an AI call.

Render functions:

renderSidebar():
- list of concepts with count of passages (computed via getPassages(concept).length)
- "Add a concept" input.

getPassages(concept): flatten docs, filter passages with uses(). Return array of {doc, p}.

renderPage(concept):
- h2: concept name; subtitle: 'Found by the terms: "…", "…"'.
- table by kind: kinds from all docs (unique, library order). Counts per kind from matched. Total row.
- related concepts: other concepts sharing ≥1 passage.
- groups: for each doc in library order with ≥1 matched passage: heading + passages.
- passage item: citation link (openSource), section badge, folded text.
- Draft button (if passages > 0).

Citation function:
```js
function citation(doc, p){
  if (doc.symbol && p.paragraph != null && p.paragraph !== "") return doc.symbol + ", para. " + p.paragraph;
  const who = doc.kind === "Journal article" ? journalCite(doc) : (doc.author || doc.short_title);
  return who + " " + doc.year + ", p. " + p.page_label;
}
```

Group heading: if doc.symbol → link text symbol to url; else link author. Also short_title, kind, year displayed.

openSource call:
```js
a.href = "#"; a.onclick = e => { e.preventDefault(); studio.openSource(doc.id, p.page); };
```

Summary:
```js
async function draftSummary(){
  const list = currentPassages.slice(0,12);
  ...
  const prompt = `...${list.map((it,i)=>`[${i+1}] ${citation(it.doc,it.p)}: ${it.p.text}`).join("\n\n")}...`;
  const btn disable; show status; cancel flag.
  try { const ans = await studio.ask(prompt); if(!cancelled) show; } catch(e){ show error }
}
```

The answer box: label + div data-source="ai".

Add "Stop" button while waiting: sets cancelled=true, resets button. Fine.

Fold CSS:
```css
.ptext.folded{display:-webkit-box;-webkit-line-clamp:3;-webkit-box-orient:vertical;overflow:hidden;line-clamp:3;cursor:pointer}
```
Click toggles.

Also "How this is computed" note near table: "A passage counts when its text contains any of the terms …, ignoring case and line breaks. n = N matching passages out of M in the library."

Write everything. Escape function:
```js
const esc = s => s.replace(/[&<>"']/g, c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
```

Build DOM with template strings mostly, but attach event handlers after via querySelector or inline onclick with data attributes. I'll use event delegation: container onclick checks target closest things.

Let me draft the full HTML.

Also heading description at top: "Source: {lib.title} — {lib.count} documents, {minYear}–{maxYear}. Every quote links to its page in the original PDF."

Sidebar item: name + count.

For added concept terms: [typed term]. If typed "mental privacy" duplicate — check name collision case-insensitively; if exists select it.

Table: "Passages by kind of document". Columns: Kind of document, Passages. Rows per kind in library; total. Note: "Rows add up to the total of matching passages; a passage can appear under only its own document's kind."

Related concepts section: "Related concepts" — other concepts found in the same passages. Links (buttons) switching concept. If none: omit or "None found." I'll show "None of the other concepts appears in these passages." Keep simple: only show section if there are related ones? Spec item 5 says show related concepts as links. If empty, show a line saying none. I'll show section always with fallback text.

Now citation link styling: accent color, dotted underline maybe.

The summary prompt text:

```
You are helping diplomats and human rights staff study the concept "X" in neurotechnology and the administration of justice.

Below are N passages quoted from UN documents, national human rights institution reports and journal articles. Write exactly three sentences summarizing what these passages say about "X". Each sentence must end with the citation of the passage it rests on, in the form (Citation). Rely only on the passages below; do not add outside knowledge.

Passages:

[1] (citation): text
...

Answer with the three sentences only.
```

Label under/above box: "Written by AI. N passages were sent to the model and left the browser." Put label above the box. The box (div data-source="ai") contains the answer.

Progress: "Contacting the model — N passages were sent and left the browser…" with Stop button.

Now write it. Aim ~480 lines.

One more detail: "Each passage: its citation as a link calling studio.openSource(id, page)". The passage text folded after three lines — click text to expand. Also maybe show a small "more" indicator. I'll add title attribute.

Group heading format: 
```
<h3>short_title</h3>
<div class="docmeta">Kind · Year · <a>symbol</a></div>
```

Passage count per group maybe "(n passages)".

Sidebar "Add a concept": label + input, placeholder "Type a term and press Enter".

Edge: input Enter with empty value — ignore.

Let me write the final code.

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Neurotechnology &amp; Justice — Concept Wiki</title>
<style>
:root{--accent:#1f6fb2;}
*{box-sizing:border-box;}
body{margin:0;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;font-size:16px;line-height:1.55;background:#f6f8fa;color:#1c2733;}
header.site{background:#fff;border-bottom:1px solid #dde4ea;padding:22px 28px;}
...
</style>
</head>
<body>
<header class="site">
  <h1>...</h1>
  <p class="sub" id="subtitle"></p>
</header>
<div class="layout">
  <nav class="side" id="sidebar"></nav>
  <main class="main" id="page"></main>
</div>
<script>
...
</script>
</body>
</html>
```

CSS details: layout display flex; side width 280px, background #fff, border-right; main flex 1, padding 26px 32px; max-width overall maybe 1200px centered. Keep full width fine.

Table: border-collapse, th background #eef3f7, borders #dde4ea, td padding 8px 12px. Total row bold.

Passage item: border-left 3px accent? Keep clean: each passage a block with citation line, section tag, text.

Related concept links: pill buttons.

Write JS:

```js
(function(){
const lib = WORKSHOP_DATA.library;
const docs = lib.records || [];

const DEFAULT_CONCEPTS = [
 ["Mental privacy", ["mental privacy"]],
 ["Freedom of thought", ["freedom of thought"]],
 ["Self-incrimination", ["self-incrimination"]],
 ["Lie detection", ["lie detection","deception detection","brain fingerprinting"]],
 ["Consent", ["consent"]],
 ["Neural data", ["neural data"]],
 ["Data solidarity", ["data solidarity"]],
 ["Proportionality", ["proportionality"]],
].map(([name,terms])=>({name,terms}));

let concepts = DEFAULT_CONCEPTS.slice();
let current = concepts.length ? concepts[0].name : null;
let cancelFlag = false;

const esc = ...
const norm = ...
const uses = ...
function passagesFor(concept){ const out=[]; docs.forEach(d=>(d.passages||[]).forEach(p=>{ if(uses(p,concept.terms)) out.push({doc:d,p}); })); return out; }
function conceptByName(n){ return concepts.find(c=>c.name.toLowerCase()===n.toLowerCase()); }

function journalCite(doc){...}
function citation(doc,p){...}

function renderSidebar(){...}
function renderPage(){...}
```

renderPage builds html string with data attributes for handlers, then binds.

Passage html:
```js
`<div class="passage" data-doc="${esc(d.id)}" data-page="${p.page}">
  <div class="pcite"><a href="#" class="srclink" data-doc="..." data-page="...">${esc(citation)}</a></div>
  ${p.section?`<div class="psec">${esc(p.section)}</div>`:""}
  <div class="ptext folded">${esc(p.text)}</div>
</div>`
```

Event delegation on #page:
- click .srclink → openSource
- click .ptext → toggle folded
- click .relbtn → set current, render
- click #draftBtn → draftSummary
- click #stopBtn → cancel

Draft summary:

```js
async function draftSummary(){
  const c = conceptByName(current); if(!c) return;
  const list = passagesFor(c).slice(0,12);
  if(!list.length) return;
  const prompt =
`You are helping diplomats and human rights staff study the concept "${c.name}" in neurotechnology and the administration of justice.

Below are ${list.length} passages quoted from UN and other documents. Write exactly three sentences summarising what these passages say about "${c.name}". Each sentence must end with the citation, in parentheses, of the passage it rests on. Use only the passages below: do not rely on anything else.

` + list.map((it,i)=>`[${i+1}] ${citation(it.doc,it.p)}: ${it.p.text}`).join("\n\n");
  cancelFlag=false;
  // update status area, disable button
  try{
    const ans = await studio.ask(prompt);
    if(cancelFlag){ resetStatus(); return; }
    showAnswer(ans, list.length);
  }catch(e){
    show error
  }
}
```

Status area html inside page: 
```html
<div class="aiwrap" id="aiwrap">
  <button id="draftBtn" class="btn">Draft a summary</button>
  <div id="aistatus"></div>
</div>
```

showAnswer: 
```html
<p class="ailabel">Written by AI. ${n} passages were sent to the model and left the browser.</p>
<div class="aibox" data-source="ai">...</div>
```
Plus keep draft button to redo.

Total passages in library for subtitle: sum of passages.

Kinds for table: unique from docs in order.

Related: 
```js
const related = concepts.filter(o=>o!==c).filter(o=>passagesFor(o).some(...)) 
```
More efficient: compute set of passage ids in current set, then for each other concept check any passage in that set uses it.

```js
const curSet = new Set(cur.map(it=>it.p.id));
const related = concepts.filter(o=>o.name.toLowerCase()!==c.name.toLowerCase())
  .filter(o=> docs.some(d=>(d.passages||[]).some(p=>curSet.has(p.id)&&uses(p,o.terms))));
```

Heading terms: `Terms that find this concept: "lie detection", "deception detection", "brain fingerprinting"`. For single term concepts just show it.

Note near table: "How this is computed: a passage counts when its text contains any of the terms above, ignoring case and line breaks; n of N passages in the library match."

Group heading: `<h3>${short_title}</h3><p class="dmeta">${kind} · ${year} · <a href=url target=_blank>symbol or author</a> · n passages</p>`.

Empty: `<p class="empty">No passage uses this term.</p>` and no draft button. Table still shown with zeros? Plan says table then passages. If no passages, table all zeros, total 0 — fine, or maybe skip table too? "No passages → 'No passage uses this term', no button." I'll still show the table (all zeros) — actually simpler to show heading, terms, table, message. Fine.

Sidebar counts computed each render.

Add concept:
```js
input.addEventListener("keydown", e=>{
  if(e.key==="Enter"){
    const v=e.target.value.trim(); if(!v) return;
    let ex=conceptByName(v);
    if(!ex){ concepts.push({name:v, terms:[v]}); ex=concepts[concepts.length-1]; }
    current=ex.name; renderSidebar(); renderPage(); input focus? sidebar rerendered so refocus.
  }
});
```
After re-render sidebar, focus the new input.

Name display: keep typed casing as name.

Fine. Let me also make sure "the first 12 passages on the page" = display order = library order grouping — passagesFor iterates docs in order, so order matches page. Good.

Now the "How this is computed" for the AI box: label covers it.

Write final file. Count lines ~ 420. 

One more: header subtitle: `${lib.title} — ${lib.count} documents, ${minY}–${maxY}. Every passage links to its page in the original PDF.` If count docs with year. Handle single year.

Let me write it out.