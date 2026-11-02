Let me plan this app carefully.

Data: WORKSHOP_DATA.library with 9 documents, each with passages. Concepts: mental privacy, freedom of thought, self-incrimination, lie detection (also "deception detection", "brain fingerprinting"), consent, neural data, data solidarity, proportionality.

Requirements:

1. Sidebar: concept pages with passage counts. Below, "Add a concept": input, Enter adds.
2. Page heading: concept + terms that find it.
3. Table "Passages by kind of document": one row per kind + total.
4. Passages grouped by document in library order. Group heading: short_title, kind, year, symbol linked to url. Each passage: citation link calling studio.openSource(id, page), section if any, text folded after three lines.
5. "Related concepts": other concepts found in same passages, as links.
6. "Draft a summary" button: sends at most first 12 passages with await studio.ask(prompt); answer in box labelled "Written by AI. N passages were sent to the model and left the browser". Answer inside data-source="ai".

Rules:
- Passage uses concept when text contains one of terms, case-insensitive, ignoring line breaks. So normalize text: lowercase, replace line breaks with space (maybe collapse whitespace). Terms list per concept.
- Text shown character for character; fold hides, never shortens. So use CSS line-clamp: 3 lines, with a "show more" toggle that removes clamp. Character for character — don't truncate with ellipsis in the data; CSS clamp hides visually but text is full in DOM. That satisfies "fold hides, never shortens". Add a toggle button "Show full text"/"Fold".
- Citation: symbol + ", para. " + paragraph when paragraph set; otherwise author, year, printed page: e.g. "Szoszkiewicz & Yuste 2025, p. 3471". Journal articles cited by surnames: "Szoszkiewicz & Yuste" (two authors → "A & B"), "Prainsack et al." for three or more. Other documents by author as written. So for journal articles, parse author field: split on " and " or ","? Authors like "Łukasz Szoszkiewicz and Rafael Yuste" → surnames "Szoszkiewicz & Yuste". "Prainsack et al." — author probably "E. Prainsack and others" or similar; need to handle: take first author's surname + " et al." if more than 2 authors. Let me write a function: split author on " and " or ", " — hmm. Safer: split on /\s+and\s+|,/. Take surnames (last word of each name). If 2 authors → "A & B"; if ≥3 → "First et al."; if 1 → surname. For non-journal: author as written (e.g. "UN Secretary-General").

Actually for journal articles: "Szoszkiewicz & Yuste 2025, p. 3471" — year and page_label. For documents with symbol and paragraph: "A/81/351, para. 1". What about symbol but paragraph null? Rule says: symbol + ", para. " + paragraph when paragraph is set; otherwise author, year, printed page. So if symbol exists but paragraph null → author, year, p. page_label. Fine.

- openSource gets page (numeric PDF page), never page_label. Link calls studio.openSource(docId, page). Note: passage id is like "A/81/351#1" — the doc id is the part before "#", or we can track doc id when grouping. Use doc.id.

- Prompt: lists passages with citations, asks for three sentences each ending with citation it rests on; model may rest only on sent passages. Answer in data-source="ai" element. Label: "Written by AI. N passages were sent to the model and left the browser". Never on page load. Show progress? It's a single call with ≤12 passages, so just a "working..." state and maybe stop? "let the user stop" — for a single call it's fine to just show "Drafting…". I could add a cancel via AbortController but studio.ask doesn't support signal presumably. Keep simple: disable button while running, show "Asking the model…".

- No symbol → show author (in group heading). No section → omitted. No passages → "No passage uses this term", no button.

- Related concepts: other concepts (from the full concept list, including added ones? "other concepts found in the same passages" — I'd include all concepts in the sidebar list except current, that match at least one of the currently displayed passages). As links (clicking switches concept).

- Sidebar counts: passage counts per concept (total across all docs).

- Table: rows per kind among matching passages, plus total row. Kinds present in data: UN report, UN agency paper, Civil-society submission, National human rights institution report, Journal article, General Comment. Only show kinds that have ≥1 matching passage? "one row per kind, and a total" — I'd show kinds present in the filtered set (rows add up to total — test 1 says "the table rows add up to its total; the Journal article row is not zero"). If we show all kinds including zero rows, rows still add up. But cleaner: show only kinds with count > 0? Test says rows add up to total — either way works. I'll show all kinds present in the library? Hmm, if a kind has zero for the concept, showing 0 rows is fine and adds up. But simpler and cleaner: show kinds that appear in the filtered passages, sorted by count desc, plus total. Actually to be safe with "rows add up to total", showing only nonzero rows guarantees it. But showing zero rows also adds up. I'll show all kinds present in the whole library with their counts (0 allowed) — that gives context. Hmm, but then "one row per kind" — ambiguous. I'll show kinds present in filtered results only, plus total; that's cleanest and always adds up. Actually let me show all kinds from the library with counts (including 0) — no wait. Test: "the table rows add up to its total; the Journal article row is not zero." Either approach passes. I'll go with kinds present in the filtered set, sorted descending, then Total row. Hmm, but a diplomat might want to see zero rows... Keep simple: only kinds with ≥1 passage in this concept. Fine.

- Grouped by document in library order: iterate library records in order, include only docs having ≥1 matching passage.

- Heading: concept name + terms that find it. E.g. "Lie detection — found by: "lie detection", "deception detection", "brain fingerprinting"".

- Default page: first concept (mental privacy) on load.

- Add a concept: input + Enter → adds concept with that single term, navigates to it. Lost on reload (fine, in-memory).

- Search matching: normalize text: text.toLowerCase().replace(/\s+/g, ' ') — "ignoring case and line breaks". Terms also normalized similarly. Check includes.

- Fold after three lines: CSS -webkit-line-clamp: 3 on a <p> with class folded; toggle button per passage "More"/"Less". Ensure full text in DOM.

- Every row showing a document has symbol linked to doc_url — group heading: symbol linked to url (record.url). If no symbol, show author. The spec: "Group heading: short_title, kind, year, symbol linked to url" and "No symbol → show author". So heading shows short_title, kind, year, and symbol (link to url) or author if no symbol.

- Citation link: <a href="#" onclick> calling studio.openSource(docId, page); prevent default. Should also maybe be a real link? It calls studio.openSource which opens PDF next to app. Use a button-styled link or anchor with role. Use <a href="javascript:void(0)">? Better: <a href="#" data-...> with click handler preventDefault. Fine.

- Title/description at top: "Research wiki — neurotechnology in the administration of justice", source line: WORKSHOP_DATA.library.title, source, count (9 documents), years range. Compute years from records min–max.

- "How this is computed" note near table and counts: e.g. "A passage counts when its text contains one of the terms (case and line breaks ignored). n = X passages in Y documents."

- Design: clean, accent #1f6fb2, light background, system fonts, 16px base, sidebar layout with flex, no horizontal scroll.

- Under 700 lines. Single HTML file.

- studio.ask prompt: build with citations + texts of first 12 passages. Prompt: "Below are N passages from documents about neurotechnology and the administration of justice, each with a citation. Write exactly three sentences summarizing what they say about [concept]. Each sentence must end with the citation of the passage(s) it rests on, in parentheses. Use only these passages. Passages: ..." Then parse answer as string (ask with json:false? The spec: `await studio.ask(prompt, {json: true})` returns answer as string; parse yourself when asked for JSON. We don't need JSON — just ask without json option? The signature shows {json:true} optional. I'll call `await studio.ask(prompt)` — returns string. Safer: call with no options. Render answer inside element with data-source="ai". Maybe convert newlines to paragraphs. Label: "Written by AI. N passages were sent to the model and left the browser." Also show "N passages sent" — the label includes N.

Also show on screen how many records sent and that they left the browser — the label does that. Also maybe a note before sending? The label after is enough, but rule says "When the app sends text to the model, say so on screen: how many records, and that they left the browser." The label covers it. I'll also show a status line while running: "Sending 12 passages to the model (they leave the browser)…".

- Handle studio.ask errors: try/catch, show error message.

- Related concepts: for the current concept's matching passages, find other concepts (from all concepts incl. added) that match any of those passages; list as links with counts maybe. "as links" — clicking navigates. Show concept name and count of shared passages.

- Sidebar: list of concepts with counts (count = passages matching across whole library). Clicking sets current concept. Active state highlighted. "Add a concept" input below.

Concept definitions:
```js
const BASE_CONCEPTS = [
  {name: "Mental privacy", terms: ["mental privacy"]},
  {name: "Freedom of thought", terms: ["freedom of thought"]},
  {name: "Self-incrimination", terms: ["self-incrimination", "self incrimination"]},
  ...
];
```
Wait — spec says: "lie detection also 'deception detection', 'brain fingerprinting'". Only lie detection has extra terms specified. Others: single term presumably. But "self-incrimination" — text might say "self-incrimination" only. Keep single terms except lie detection. Hmm, should I add variants for others? Spec: "Page heading: the concept and the terms that find it (lie detection also 'deception detection', 'brain fingerprinting')". So only lie detection has aliases. Keep others single-term to follow spec exactly. But "No synonyms: 'consent' finds 'consented', not 'agreement'" — meaning substring matching: "consent" matches "consented" because includes. Good, includes() handles that.

Concepts list:
- mental privacy → ["mental privacy"]
- freedom of thought → ["freedom of thought"]
- self-incrimination → ["self-incrimination"] — hmm, text may use "self-incrimination" with hyphen; also "privilege against self-incrimination". includes("self-incrimination") catches. Maybe also "self incrimination" without hyphen? Spec doesn't say. Keep just the hyphenated? Risky if data uses non-hyphenated. The spec says "where it says nothing, keep it simple" — single term. But to be safe for matching quality... The test only checks lie detection alias. I'll keep single terms as specified, except lie detection with its three terms. Actually, hmm — "self-incrimination" might appear as "self-incrimination" consistently in UN docs. Fine.

- lie detection → ["lie detection", "deception detection", "brain fingerprinting"]
- consent → ["consent"]
- neural data → ["neural data"]
- data solidarity → ["data solidarity"]
- proportionality → ["proportionality"]

Test 3: "Open 'lie detection': one passage contains 'deception detection' but not 'lie detection'." So matching must be per-term includes — yes.

Normalization: lowercase + replace line breaks. "ignoring case and line breaks" — I'll do `t.toLowerCase().replace(/[\r\n]+/g, " ")` then also collapse multiple spaces? "ignoring line breaks" — replacing \n with space suffices; but if text has "lie\ndetection", replacing with space gives "lie detection" — good. If "lie  detection" double space... collapse whitespace to single space to be safe: `.replace(/\s+/g," ")`. Terms normalized the same.

Citation function:
```js
function surname(name){ const parts = name.trim().split(/\s+/); return parts[parts.length-1]; }
function citeAuthor(author, kind){
  if(kind === "Journal article"){
    const names = author.split(/\s+and\s+|,|;/).map(s=>s.trim()).filter(Boolean);
    if(names.length >= 3) return surname(names[0]) + " et al.";
    if(names.length === 2) return surname(names[0]) + " & " + surname(names[1]);
    return surname(names[0]);
  }
  return author;
}
```
Careful: "Łukasz Szoszkiewicz and Rafael Yuste" → split on " and " → ["Łukasz Szoszkiewicz","Rafael Yuste"] → "Szoszkiewicz & Yuste". Good. Prainsack et al. author might be "E. Prainsack, ..." with commas — splitting on comma could break "Prainsack, E." style. Hmm. If author is "Prainsack, E., et al." splitting on comma gives ["Prainsack","E.","et al."] → 3 names → "Prainsack et al." — actually works by accident. If "Barbara Prainsack and others" → " and " split → ["Barbara Prainsack","others"] → 2 → "Prainsack & others" — bad. Let me handle "others"/"et al." in author string: if author matches /et al|and others|others/i, return surname(first) + " et al.". Let me write:

```js
function citeAuthor(author, kind){
  if(kind !== "Journal article") return author;
  const a = author.trim();
  if(/et al|others/i.test(a)){
    const first = a.split(/\s+and\s+|,|;/)[0].trim();
    return surname(first) + " et al.";
  }
  const names = a.split(/\s+and\s+/).map(s=>s.trim()).filter(Boolean);
  ...
}
```
Hmm "and others" contains " and " → split gives ["Barbara Prainsack","others"] → check /others/ first. OK my order handles it: test /et al\.?|others/ first. But "others" could appear... fine.

Actually simpler robust approach: split on /\s+and\s+|,|;/ then filter out tokens like "et al.", "others". If remaining ≥3 → first surname + " et al."; if 2 → "A & B"; if 1 → surname. Let me do:

```js
function journalCite(author){
  let names = author.split(/\s+and\s+|,|;/).map(s=>s.trim()).filter(s=>s && !/^(et al\.?|others?)$/i.test(s));
  if(!names.length) return author;
  if(names.length >= 3) return surname(names[0]) + " et al.";
  if(names.length === 2) return surname(names[0]) + " & " + surname(names[1]);
  return surname(names[0]);
}
```
"Łukasz Szoszkiewicz and Rafael Yuste" → 2 → "Szoszkiewicz & Yuste". Good.

Citation for passage:
```js
function citation(doc, p){
  if(doc.symbol && p.paragraph != null && p.paragraph !== "") return doc.symbol + ", para. " + p.paragraph;
  const a = (doc.kind === "Journal article") ? journalCite(doc.author) : doc.author;
  return a + " " + doc.year + ", p. " + p.page_label;
}
```
Wait spec: "Citation: symbol + ', para. ' + paragraph when paragraph is set; otherwise author, year and printed page". So condition is paragraph set (symbol presumably present for those). If symbol set but paragraph null → author/year/page. My condition: paragraph set → symbol + para. Else author-year-page. But what if symbol null and paragraph set? Unlikely. Use: `if(p.paragraph != null && p.paragraph !== "")` → symbol + ", para. " + paragraph (symbol should exist; if not, fall back). I'll do: if paragraph set and symbol → symbol form; else author form.

Group heading: short_title (maybe link to url too? spec: "symbol linked to url"). Heading: `<a href=url target=_blank>symbol</a>` or author if no symbol; plus kind, year, short_title. Also maybe passage count for the doc.

Passage row: citation link (openSource), section (if any) as a label, text folded. Layout: 
```
[ citation link ]  [section]
text (clamped 3 lines) [Show more]
```

Fold: 
```css
.ptext{display:-webkit-box;-webkit-box-orient:vertical;-webkit-line-clamp:3;overflow:hidden;}
.ptext.open{-webkit-line-clamp:unset;display:block;}
```
Toggle button per passage.

Table: kinds of matching passages. Build counts by kind. Rows sorted by count desc then name. Total row.

Related concepts: for each other concept, count passages among current matching set that match it. Show those with count>0 as links "name (n)".

Summary button: visible only if passages exist. On click: take first 12 passages (in display order — grouped by document in library order; "first 12 passages on the page" = display order). Build prompt:

```
You are helping human rights professionals. Below are {n} passages from {docs} documents about neurotechnology and the administration of justice, each with its citation. Write exactly three sentences that summarize what these passages say about "{concept}". Each sentence must end with the citation of the passage it rests on, in parentheses, using only the citations given. Do not use any other source.

Passages:
1. [citation] text...
```

Then `const ans = await studio.ask(prompt);` render into div data-source="ai", splitting on newlines into paragraphs. Label above: `Written by AI. ${n} passages were sent to the model and left the browser.` The label element itself — should the label be inside data-source="ai"? Rule: "Render every value that came from studio.ask inside an element with data-source='ai'". The label is our own text, not from model — but the answer must be inside data-source="ai". I'll put the answer in `<div data-source="ai">` and the label as a separate heading (not AI-generated). Actually spec: "the answer appears in a box labelled 'Written by AI. N passages were sent...'". So box has label + answer; answer inside data-source="ai". I'll make the whole box contain a label div and an answer div with data-source="ai". Safe: put data-source="ai" on the answer container.

Progress: while awaiting, show "Sending N passages to the model — they leave the browser…" and disable button. try/catch → show error text (not in ai box).

studio.openSource(id, page): id = doc.id (e.g. "A/81/351"), page = p.page. Wrap in try/catch? Just call. Citation link: `<a href="#" class="cite">` with click handler `studio.openSource(docId, p.page); return false;`.

Sidebar counts: for each concept, count passages across all docs matching. Show name + count badge.

Add concept: form with input; on submit, term = value.trim(); if empty ignore; if concept name already exists (case-insensitive), just navigate; else push {name: term, terms:[term]} — name capitalized? Use term as name. Navigate to it. Clear input.

Heading: h1 concept name; below: "Found by the terms: "lie detection", "deception detection", "brain fingerprinting"" — list terms in quotes. Plus a "How this is computed" note: "A passage is counted when its full text contains one of these terms, ignoring case and line breaks. Matching is by substring: 'consent' also finds 'consented'."

Top header: title "Neurotechnology & justice — research wiki", description: `${library.title} — ${library.source}; ${library.count} documents, ${totalPassages} passages, ${minYear}–${maxYear}.` Compute from data.

Layout: 
```
header
main: flex; aside (sidebar, ~260px); section (content)
```
Responsive: on narrow, sidebar stacks on top (media query). No horizontal scroll: use max-width 100%, box-sizing border-box.

Colors: background #f5f7fa, panels white, accent #1f6fb2, text #1a1a1a.

Fonts: system stack.

Now line count: aim under 700 lines. Fine.

Edge: empty library? Handle gracefully (counts zero). Missing fields: guard with || "".

Let me also make sure "Every row that shows a document has its symbol, linked to doc_url" — group headings have symbol link to record.url. If no symbol, show author (and maybe link url anyway? spec says no symbol → show author; I'll show author as plain text, but could still link url... keep author plain, but maybe link to url if present — spec says show author; I'll show author text and if url exists make the short_title link? Keep simple: symbol linked if present, else author plain).

Passage citation link also should maybe have title attribute "Open the PDF at this page".

Related concepts links: `<a href="#" data-concept="...">`.

Also the sidebar "concept pages" — clicking navigates (render). Use hash? Could use location.hash for deep-linking; simple: just render, optionally set hash. I'll use hash so back button works-ish? Keep simple: render on click, update location.hash without scroll (history.replaceState). Optional. I'll set hash and on load read hash to pick initial concept. Nice touch, low cost.

Let me now think about the "terms that find it" display: e.g. for lie detection: `Terms: "lie detection", "deception detection", "brain fingerprinting"`. For others single term.

Table note: "How this is computed: each of the n passages whose text contains a term (case and line breaks ignored) is counted once under its document's kind."

Now write the code.

Structure:

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Neurotechnology & justice — research wiki</title>
<style>...</style>
</head>
<body>
<header>
  <h1>...</h1>
  <p class="desc" id="desc"></p>
</header>
<div class="layout">
  <aside>
    <h2>Concepts</h2>
    <ul id="conceptList"></ul>
    <form id="addForm"><label for="addInput">Add a concept</label><input id="addInput" placeholder="type a term, press Enter"></form>
    <p class="note">Added concepts are kept only in this session.</p>
  </aside>
  <main id="main"></main>
</div>
<script>
const LIB = window.WORKSHOP_DATA.library;
...
</script>
</body>
</html>
```

JS:

```js
const LIB = window.WORKSHOP_DATA.library || {records:[]};
const docs = LIB.records || [];
const BASE = [
 {name:"Mental privacy", terms:["mental privacy"]},
 {name:"Freedom of thought", terms:["freedom of thought"]},
 {name:"Self-incrimination", terms:["self-incrimination"]},
 {name:"Lie detection", terms:["lie detection","deception detection","brain fingerprinting"]},
 {name:"Consent", terms:["consent"]},
 {name:"Neural data", terms:["neural data"]},
 {name:"Data solidarity", terms:["data solidarity"]},
 {name:"Proportionality", terms:["proportionality"]},
];
let concepts = BASE.map(c=>({...c}));
let current = concepts[0].name;

const norm = s => (s||"").toLowerCase().replace(/\s+/g," ").trim();
function matches(text, terms){ const t = norm(text); return terms.some(term => t.includes(norm(term))); }
function passagesFor(concept){ // returns [{doc, p}]
  const out=[];
  for(const d of docs) for(const p of (d.passages||[])) if(matches(p.text, concept.terms)) out.push({doc:d, p:p});
  return out;
}
```

Citation:
```js
function surname(n){ const parts=(n||"").trim().split(/\s+/); return parts[parts.length-1]||n; }
function citeAuthor(doc){
  if(doc.kind === "Journal article"){
    const names=(doc.author||"").split(/\s+and\s+|,|;/).map(s=>s.trim()).filter(s=>s && !/^(et al\.?|others?)$/i.test(s));
    if(names.length>=3) return surname(names[0])+" et al.";
    if(names.length===2) return surname(names[0])+" & "+surname(names[1]);
    if(names.length===1) return surname(names[0]);
  }
  return doc.author || "";
}
function citation(doc,p){
  if(p.paragraph !== null && p.paragraph !== undefined && p.paragraph !== "" && doc.symbol)
    return doc.symbol + ", para. " + p.paragraph;
  return citeAuthor(doc) + " " + (doc.year||"") + ", p. " + (p.page_label||p.page);
}
```

Render functions:

renderSidebar(): list items with name + count; click → select(name).

select(name): current=name; update hash; renderSidebar (active class); renderMain().

renderMain():
- concept = find; items = passagesFor(concept)
- h1 concept.name
- terms line
- note how computed
- if items.length===0: p "No passage uses this term." and return (no table? spec: "no passages → 'No passage uses this term', no button". Table with total 0? Probably show message only; I'll show the message and skip table/button. Actually maybe still show table with zeros? Simpler: message only.)
- table by kind: counts; rows sorted; total.
- groups: iterate docs in order; for each doc, matching passages; if any, render group.
- related concepts.
- summary button + output box.

Group rendering:
```js
for(const d of docs){
  const ps=(d.passages||[]).filter(p=>matches(p.text,concept.terms));
  if(!ps.length) continue;
  // heading
}
```

Passage element:
```html
<div class="passage">
  <div class="pmeta"><a class="cite" href="#">A/81/351, para. 2</a> <span class="sec">I. Introduction</span></div>
  <p class="ptext folded">text</p>
  <button class="foldbtn">Show full text</button>
</div>
```
Fold button only if text long enough? Always show; if short, clamp does nothing and button toggles class — fine, but button "Show full text" on a 1-line text is odd. Could hide button if text fits in 3 lines — hard to know; estimate by characters? Just always show toggle; harmless. Or check `p.text.length > 300`? Eh — keep always, label toggles "Fold" / "Show full text". Fine.

Text character-for-character: put text via textContent (create elements with DOM APIs or use innerHTML with escaping). I'll build DOM with createElement and textContent to avoid HTML injection issues. That's more verbose but safe. Alternatively escape function and innerHTML. I'll use a helper `el(tag, cls, text)`.

Summary:
```js
async function draft(){
  const items = currentItems.slice(0,12);
  const n = items.length;
  status: "Sending n passages to the model — they leave the browser…"
  const lines = items.map((it,i)=>`${i+1}. ${citation(it.doc,it.p)}\n${it.p.text}`);
  const prompt = `...`;
  try{
    const ans = await studio.ask(prompt);
    answerBox: label + <div data-source="ai"> paragraphs from ans split /\n+/ 
  }catch(e){ show error }
}
```
Prompt text:
```
You are assisting human rights professionals (diplomats, NGOs, NHRIs, UN staff). Below are ${n} verbatim passages from documents about neurotechnology and the administration of justice, each with its citation.

Write exactly three sentences summarising what these passages say about "${concept.name}". Each sentence must end with the citation of the passage it rests on, in parentheses, and you may only use the passages below.

Passages:
${lines.join("\n\n")}
```

Label: `Written by AI. ${n} passages were sent to the model and left the browser.` — put label as box heading (not data-source), answer inside data-source="ai". Hmm, rule: "Render every value that came from studio.ask inside an element with the attribute data-source='ai'." The label contains n which we know — fine outside. But to be extra safe I could put data-source="ai" on the whole box including label? The label is not from the model. I'll put data-source="ai" on the answer div only. Actually the spec for this app says: "the answer sits inside data-source='ai'". Good.

Also "show progress": single call; show status text while awaiting. "let the user stop" — single call, can't abort easily; I'll note it's one request. Fine.

studio may be undefined in some contexts? It's provided. Guard: `if(typeof studio==="undefined")` show error.

Hash handling: on load, read location.hash like "#concept=Lie%20detection"? Simpler: `#` + encodeURIComponent(name). On select, history.replaceState(null,"", "#"+encodeURIComponent(name)). On load, decode and find concept; fallback first.

Now CSS:

```css
*{box-sizing:border-box}
body{margin:0;font:16px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;background:#f4f6f9;color:#17202a;}
header{background:#fff;border-bottom:1px solid #dde3ea;padding:20px 28px;}
header h1{margin:0 0 6px;font-size:24px;color:#1f6fb2;}
.desc{margin:0;color:#4a5568;max-width:70em;}
.layout{display:flex;gap:24px;padding:24px 28px;align-items:flex-start;max-width:1200px;}
aside{width:250px;flex:0 0 250px;background:#fff;border:1px solid #dde3ea;border-radius:8px;padding:16px;position:sticky;top:16px;}
aside h2{font-size:15px;text-transform:uppercase;letter-spacing:.06em;color:#4a5568;margin:0 0 10px;}
#conceptList{list-style:none;margin:0 0 14px;padding:0;}
#conceptList li{margin:0;}
#conceptList button{all:unset-ish...}
```
I'll style concept buttons: display:flex;justify-content:space-between;width:100%;padding:7px 10px;border-radius:6px;cursor:pointer;color:#17202a; hover background #eaf2fa; active: background #1f6fb2 color #fff.

Count badge: background #e3ecf5; border-radius:10px; padding:0 8px; font-size:13px.

main{flex:1;min-width:0;}
.panel{background:#fff;border:1px solid #dde3ea;border-radius:8px;padding:20px 24px;margin-bottom:20px;}
h2 in main: font-size:19px;color:#1f6fb2.
table{border-collapse:collapse;width:100%;} th,td{text-align:left;padding:8px 10px;border-bottom:1px solid #e4e9f0;} th{color:#4a5568;font-weight:600;} td.num,th.num{text-align:right;} tr.total td{font-weight:700;border-top:2px solid #1f6fb2;}
.note{font-size:13.5px;color:#5a6b7d;background:#eef4fa;border-left:3px solid #1f6fb2;padding:8px 12px;border-radius:0 6px 6px 0;margin:10px 0 0;}
.docgroup{border:1px solid #dde3ea;border-radius:8px;margin-bottom:16px;overflow:hidden;}
.dochead{background:#eef4fa;padding:10px 16px;display:flex;flex-wrap:wrap;gap:6px 14px;align-items:baseline;}
.dochead .t{font-weight:700;}
.dochead a{color:#1f6fb2;}
.passage{padding:12px 16px;border-top:1px solid #e4e9f0;}
.pmeta{display:flex;gap:10px;flex-wrap:wrap;align-items:baseline;margin-bottom:4px;}
.cite{color:#1f6fb2;font-weight:600;text-decoration:none;} .cite:hover{text-decoration:underline;}
.sec{font-size:13.5px;color:#5a6b7d;font-style:italic;}
.ptext{margin:4px 0 6px;white-space:pre-wrap;} 
```
Wait — "text shown character for character" — white-space:pre-wrap preserves line breaks as in source. Good, use pre-wrap. Fold with line-clamp: with pre-wrap and -webkit-box... line-clamp works with display:-webkit-box. Combine: `.ptext{display:-webkit-box;-webkit-box-orient:vertical;-webkit-line-clamp:3;overflow:hidden;white-space:pre-wrap;}` and `.ptext.open{display:block;-webkit-line-clamp:unset;}`. Should work in modern browsers.

foldbtn: small button, accent outline.

Related: `.rel a{display:inline-block;margin:4px 8px 4px 0;padding:4px 10px;background:#eef4fa;border-radius:14px;color:#1f6fb2;text-decoration:none;}`

Summary box: `.aibox{border:1px solid #1f6fb2;border-radius:8px;background:#f7fbff;padding:14px 16px;} .aibox .label{font-weight:700;color:#1f6fb2;font-size:14px;margin-bottom:8px;} [data-source="ai"] p{margin:0 0 8px;}`

Button: `.btn{background:#1f6fb2;color:#fff;border:none;border-radius:6px;padding:9px 16px;font-size:15px;cursor:pointer;} .btn:disabled{opacity:.6;cursor:default;}`

Add form: input full width, padding 8px, border, radius.

Media query max-width 860px: layout column; aside width auto, position static.

Now counts in sidebar: passagesFor(concept).length — computed each render; fine (data small: ~900 passages total; 8 concepts × 900 × terms — trivial).

Related concepts: for current items (doc,p list), for each other concept count items where matches(p.text, other.terms). Show if >0.

Terms display: concept.terms.map(t=>`"${t}"`).join(", ").

Header desc: `${LIB.title} — ${LIB.source}. ${docs.length} documents, ${totalPassages} passages, ${years}.` years: min/max of doc.year. If missing, omit.

Also note under heading: "How this is computed: a passage is listed when its full text contains one of the terms above, ignoring case and line breaks (substring match, so “consent” also finds “consented”). n = X passages in Y documents."

Table note: "Each passage is counted once, under the kind of its document."

Now the "Draft a summary" button placement: after passages, before related? Spec order: 3 table, 4 passages, 5 related, 6 button. I'll put button + output after related concepts, or right after passages. Order in spec lists related (5) then button (6). I'll follow: table, passages, related, summary. Actually button maybe more useful near top... follow spec order.

Test 4: "three sentences, each ending with a citation also on the page" — that's model behavior; prompt enforces. Label says how many sent.

Now write everything carefully. Also ensure no external loads. Chart.js not needed.

One more detail: "Every row that shows a document has its symbol, linked to doc_url" — in our app, documents shown as group headings; symbol linked to `url` (record.url). Also maybe table rows are kinds not documents. OK.

Citation link click: `studio.openSource(doc.id, p.page)`. doc.id like "A/81/351". Good.

Also add title attr: "Open the PDF at the page where this paragraph starts".

Edge: p.paragraph could be "50 (c)" string — fine, string concat.

Let me also handle "no passages → no button": in renderMain, if items empty, show message, no table? I'll still show heading + terms + note + message. Skip table, groups, related, button.

Write the final HTML now. Keep it tidy, ~450 lines.

Prompt construction detail: include citations and full texts. Cap 12.

Let me write:

```js
function buildPrompt(concept, items){
  const n = items.length;
  const lines = items.map((it,i)=> (i+1)+". "+citation(it.doc,it.p)+"\n"+it.p.text).join("\n\n");
  return [
   "You are assisting human rights professionals (diplomats, NGO, NHRI and UN staff).",
   "Below are "+n+" verbatim passages from documents about neurotechnology and the administration of justice, each with its citation.",
   "",
   "Task: write exactly three sentences that summarise what these passages say about \""+concept.name+"\".",
   "Each sentence must end with the citation of the passage it rests on, in parentheses. Use only the passages below; do not invent anything.",
   "",
   "Passages:",
   lines
  ].join("\n");
}
```

Draft handler:

```js
let drafting=false;
async function onDraft(){
  if(drafting) return;
  const concept = getCurrent();
  const items = currentItems.slice(0,12);
  const n = items.length;
  const status = document.getElementById("sumStatus");
  const out = document.getElementById("sumOut");
  out.innerHTML=""; 
  status.textContent = "Sending "+n+" passages to the model — they leave the browser…";
  btn.disabled=true; drafting=true;
  try{
    const ans = await studio.ask(buildPrompt(concept, items));
    status.textContent="";
    const label = el("p","ailabel","Written by AI. "+n+" passage"+(n===1?"":"s")+" were sent to the model and left the browser.");
    const body = el("div","aibody"); body.setAttribute("data-source","ai");
    String(ans||"").split(/\n+/).map(s=>s.trim()).filter(Boolean).forEach(s=>{ const p=document.createElement("p"); p.textContent=s; body.appendChild(p); });
    out.appendChild(label); out.appendChild(body);
  }catch(err){
    status.textContent = "The model could not be reached: "+(err && err.message ? err.message : err);
  } finally { btn.disabled=false; drafting=false; }
}
```

Hmm — label inside out; answer in data-source div. Good.

Render main with DOM building. Let me write helper:

```js
function el(tag, cls, text){ const e=document.createElement(tag); if(cls) e.className=cls; if(text!==undefined) e.textContent=text; return e; }
```

renderMain:

```js
function renderMain(){
  const concept = concepts.find(c=>c.name===current) || concepts[0];
  current = concept.name;
  const main = document.getElementById("main"); main.innerHTML="";
  const items = passagesFor(concept); currentItems = items;

  const h = el("h2","pagetitle", concept.name); main.appendChild(h);
  const terms = el("p","terms","Found by the terms: " + concept.terms.map(t=>"\u201C"+t+"\u201D").join(", "));
  main.appendChild(terms);
  const docsHit = new Set(items.map(it=>it.doc.id));
  const note = el("p","note","How this is computed: a passage is listed when its full text contains one of the terms above, ignoring case and line breaks (substring match, so \u201Cconsent\u201D also finds \u201Cconsented\u201D). n = "+items.length+" passage"+(items.length===1?"":"s")+" in "+docsHit.size+" document"+(docsHit.size===1?"":"s")+".");
  main.appendChild(note);

  if(!items.length){ main.appendChild(el("p","empty","No passage uses this term.")); return; }

  // table
  const panel = el("section","panel"); panel.appendChild(el("h3","paneltitle","Passages by kind of document"));
  const kindCount = {};
  items.forEach(it=>{ const k=it.doc.kind||"Other"; kindCount[k]=(kindCount[k]||0)+1; });
  const rows = Object.entries(kindCount).sort((a,b)=>b[1]-a[1] || a[0].localeCompare(b[0]));
  const table = el("table");
  thead: Kind | Passages
  rows.forEach(([k,c])=>{ tr: td k, td.num c });
  total row: "Total", items.length
  panel.appendChild(table);
  panel.appendChild(el("p","note","Each passage is counted once, under the kind of its document."));
  main.appendChild(panel);

  // groups
  const gwrap = el("section","panel"); gwrap.appendChild(el("h3","paneltitle","Passages, grouped by document"));
  for(const d of docs){
    const ps = (d.passages||[]).filter(p=>matches(p.text, concept.terms));
    if(!ps.length) continue;
    const g = el("div","docgroup");
    const head = el("div","dochead");
    head.appendChild(el("span","t", d.short_title || d.title || d.id));
    head.appendChild(el("span","k", d.kind||""));
    head.appendChild(el("span","y", String(d.year||"")));
    if(d.symbol){ const a=el("a","sym", d.symbol); a.href=d.url||"#"; a.target="_blank"; a.rel="noopener"; head.appendChild(a); }
    else head.appendChild(el("span","sym", d.author||""));
    head.appendChild(el("span","k", ps.length+" passage"+(ps.length===1?"":"s")));
    g.appendChild(head);
    ps.forEach(p=>{
      const row = el("div","passage");
      const meta = el("div","pmeta");
      const cite = el("a","cite", citation(d,p));
      cite.href="#"; cite.title="Open the PDF at the page where this paragraph starts";
      cite.addEventListener("click", ev=>{ ev.preventDefault(); try{ studio.openSource(d.id, p.page); }catch(e){} });
      meta.appendChild(cite);
      if(p.section) meta.appendChild(el("span","sec", p.section));
      row.appendChild(meta);
      const t = el("p","ptext", p.text);
      row.appendChild(t);
      const b = el("button","foldbtn","Show full text");
      b.addEventListener("click", ()=>{ const open=t.classList.toggle("open"); b.textContent = open ? "Fold" : "Show full text"; });
      row.appendChild(b);
      g.appendChild(row);
    });
    gwrap.appendChild(g);
  }
  main.appendChild(gwrap);

  // related
  const rel = el("section","panel");
  rel.appendChild(el("h3","paneltitle","Related concepts"));
  const relWrap = el("div","rellinks");
  let any=false;
  for(const c of concepts){
    if(c.name===concept.name) continue;
    const ccount = items.filter(it=>matches(it.p.text, c.terms)).length;
    if(ccount>0){ any=true;
      const a=el("a","rel", c.name+" ("+ccount+")");
      a.href="#"+encodeURIComponent(c.name);
      a.addEventListener("click",ev=>{ev.preventDefault(); select(c.name);});
      relWrap.appendChild(a);
    }
  }
  if(!any) relWrap.appendChild(el("span","note-inline","No other concept appears in these passages."));
  rel.appendChild(relWrap);
  rel.appendChild(el("p","note","A concept is related when at least one of the passages above also contains its term(s)."));
  main.appendChild(rel);

  // summary
  const sum = el("section","panel");
  sum.appendChild(el("h3","paneltitle","Draft a summary"));
  const btn = el("button","btn","Draft a summary");
  const status = el("p","status","");
  const out = el("div","sumout");
  btn.addEventListener("click", ()=>onDraft(btn,status,out,concept,items));
  sum.appendChild(btn); sum.appendChild(status); sum.appendChild(out);
  sum.appendChild(el("p","note","At most the first 12 passages on this page are sent, with their citations, to a language model. The model may only use what it is sent."));
  main.appendChild(sum);
}
```

Wait — onDraft needs concept & items; pass them. Also currentItems global not needed then.

Sidebar render:

```js
function renderSidebar(){
  const ul = document.getElementById("conceptList"); ul.innerHTML="";
  for(const c of concepts){
    const li = document.createElement("li");
    const b = el("button","concept"+(c.name===current?" active":""), "");
    const nm = el("span","cname", c.name);
    const ct = el("span","ccount", String(passagesFor(c).length));
    b.appendChild(nm); b.appendChild(ct);
    b.addEventListener("click", ()=>select(c.name));
    li.appendChild(b); ul.appendChild(li);
  }
}
function select(name){
  current = name;
  try{ history.replaceState(null,"","#"+encodeURIComponent(name)); }catch(e){}
  renderSidebar(); renderMain();
}
```

Add form:

```js
document.getElementById("addForm").addEventListener("submit", ev=>{
  ev.preventDefault();
  const inp = document.getElementById("addInput");
  const term = inp.value.trim();
  if(!term) return;
  const exists = concepts.find(c=>c.name.toLowerCase()===term.toLowerCase());
  if(exists) select(exists.name);
  else { concepts.push({name: term, terms:[term]}); select(term); }
  inp.value="";
});
```

Init:

```js
(function(){
  const hash = decodeURIComponent((location.hash||"").replace(/^#/,""));
  if(hash && concepts.some(c=>c.name===hash)) current = hash;
  // header desc
  const totalP = docs.reduce((s,d)=>s+(d.passages||[]).length,0);
  const years = docs.map(d=>d.year).filter(y=>y!=null);
  const yr = years.length ? Math.min(...years)+"–"+Math.max(...years) : "";
  document.getElementById("desc").textContent = (LIB.title||"Research library")+" — "+(LIB.source||"")+". "+docs.length+" documents, "+totalP+" passages"+(yr?", "+yr:"")+".";
  document.getElementById("addForm")... 
  renderSidebar(); renderMain();
})();
```

Header title: "Neurotechnology and the administration of justice — research wiki". Static title fine.

onDraft signature: I'll define `async function onDraft(btn,status,out,concept,items)`.

Also guard `typeof studio === "undefined"` in onDraft and openSource click: show message.

Check test 1: mental privacy — table rows sum to total: yes since rows are exactly the kind counts of items, total = items.length. Journal article row non-zero: Szoszkiewicz-Yuste article is about mental privacy — yes, its passages contain "mental privacy". Good.

Test 2: citation link calls studio.openSource("A/81/351", 2) etc. Good.

Test 3: lie detection — "deception detection" passage included via alias. Good.

Test 4: prompt asks 3 sentences ending with citations; label shows n. Good.

One more: "Page heading: the concept and the terms that find it". Done.

"Sidebar: the concept pages with passage counts" — done.

Fold: "the text folded after three lines" — line-clamp 3. Good.

Also ensure `white-space:pre-wrap` on ptext so character-for-character incl. line breaks; clamp still works.

Potential issue: -webkit-line-clamp with pre-wrap — works in Chrome/Safari/Firefox (Firefox supports -webkit-line-clamp). OK.

Now, the note about "How this is computed" near every chart or number — we have notes near table and heading counts and sidebar? Sidebar counts: add a small note in sidebar: "Counts: passages whose text contains the concept's term(s), case and line breaks ignored." Good.

Line count check — should be well under 700.

Also: "no passages → 'No passage uses this term', no button" — handled.

"no symbol → show author" in group heading — handled. Also citation falls back to author/year/page when paragraph null even if symbol exists — per rule.

Also for General Comment docs (CCPR/C/GC/32 etc.), symbol exists, paragraph set → "CCPR/C/GC/32, para. 12". Good.

Write final answer: 1–3 short sentences before code block, then the html block, nothing after.

Let me now write the complete file carefully.

Also add `<meta name="color-scheme" content="light">`? Not needed.

CSS details for concept button active: `.concept.active{background:#1f6fb2;color:#fff;} .concept.active .ccount{background:rgba(255,255,255,.25);color:#fff;}`

Buttons reset: `button{font:inherit;}`.

Let me write it.

Also the "terms" line and heading: h2 pagetitle font-size 22px color #17202a maybe; accent for h3 paneltitle.

Empty state: also maybe still show table? Spec says message, no button. I'll show just message.

One subtlety: "sends at most the first 12 passages on the page" — display order = grouped by document in library order, passages in original order within doc. My items from passagesFor iterate docs in order and passages in order — same order. Good.

Also progress: status text while awaiting. Good.

Now write out. I'll be careful with quotes in JS strings (use \u201C etc. or plain quotes). Use plain double quotes inside single-quoted JS strings carefully.

Final code:

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Neurotechnology &amp; justice — research wiki</title>
<style>
  * { box-sizing: border-box; }
  html, body { margin: 0; padding: 0; }
  body {
    font: 16px/1.55 -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    background: #f4f6f9; color: #17202a;
  }
  header { background: #fff; border-bottom: 1px solid #dde3ea; padding: 20px 28px; }
  header h1 { margin: 0 0 6px; font-size: 24px; color: #1f6fb2; }
  .desc { margin: 0; color: #4a5568; max-width: 75em; }
  .layout { display: flex; gap: 24px; align-items: flex-start; padding: 24px 28px; max-width: 1240px; }
  aside { flex: 0 0 260px; width: 260px; background: #fff; border: 1px solid #dde3ea; border-radius: 8px; padding: 16px; position: sticky; top: 16px; }
  aside h2 { margin: 0 0 10px; font-size: 14px; text-transform: uppercase; letter-spacing: .06em; color: #4a5568; }
  #conceptList { list-style: none; margin: 0 0 16px; padding: 0; }
  .concept { display: flex; justify-content: space-between; align-items: center; gap: 8px; width: 100%; padding: 7px 10px; border: 0; border-radius: 6px; background: transparent; color: #17202a; cursor: pointer; text-align: left; font: inherit; }
  .concept:hover { background: #eaf2fa; }
  .concept.active { background: #1f6fb2; color: #fff; }
  .ccount { background: #e3ecf5; color: #17202a; border-radius: 999px; padding: 1px 9px; font-size: 13px; white-space: nowrap; }
  .concept.active .ccount { background: rgba(255,255,255,.28); color: #fff; }
  .side-note { font-size: 13px; color: #5a6b7d; margin: 10px 0 0; }
  #addForm label { display: block; font-size: 14px; font-weight: 600; margin-bottom: 6px; color: #17202a; }
  #addInput { width: 100%; padding: 8px 10px; border: 1px solid #c3cedb; border-radius: 6px; font: inherit; }
  #addInput:focus { outline: 2px solid #1f6fb2; outline-offset: 1px; }
  main { flex: 1; min-width: 0; }
  .pagetitle { margin: 0 0 4px; font-size: 24px; color: #17202a; }
  .terms { margin: 0 0 10px; color: #4a5568; }
  .panel { background: #fff; border: 1px solid #dde3ea; border-radius: 8px; padding: 18px 22px; margin: 0 0 20px; }
  .paneltitle { margin: 0 0 12px; font-size: 19px; color: #1f6fb2; }
  .note { font-size: 13.5px; color: #4a5568; background: #eef4fa; border-left: 3px solid #1f6fb2; padding: 8px 12px; border-radius: 0 6px 6px 0; margin: 12px 0 0; }
  table { border-collapse: collapse; width: 100%; }
  th, td { text-align: left; padding: 8px 10px; border-bottom: 1px solid #e4e9f0; }
  th { color: #4a5568; font-weight: 600; }
  th.num, td.num { text-align: right; }
  tr.total td { font-weight: 700; border-top: 2px solid #1f6fb2; border-bottom: 0; }
  .docgroup { border: 1px solid #dde3ea; border-radius: 8px; margin: 0 0 14px; overflow: hidden; }
  .dochead { background: #eef4fa; padding: 10px 16px; display: flex; flex-wrap: wrap; gap: 4px 14px; align-items: baseline; }
  .dochead .t { font-weight: 700; }
  .dochead .k, .dochead .y { color: #4a5568; font-size: 14px; }
  .dochead a.sym { color: #1f6fb2; font-weight: 600; text-decoration: none; }
  .dochead a.sym:hover { text-decoration: underline; }
  .dochead .sym { font-weight: 600; }
  .passage { padding: 12px 16px; border-top: 1px solid #e4e9f0; }
  .pmeta { display: flex; flex-wrap: wrap; gap: 4px 12px; align-items: baseline; margin-bottom: 2px; }
  a.cite { color: #1f6fb2; font-weight: 600; text-decoration: none; }
  a.cite:hover { text-decoration: underline; }
  .sec { font-size: 13.5px; color: #5a6b7d; font-style: italic; }
  .ptext { margin: 4px 0 6px; white-space: pre-wrap; display: -webkit-box; -webkit-box-orient: vertical; -webkit-line-clamp: 3; overflow: hidden; }
  .ptext.open { display: block; -webkit-line-clamp: unset; }
  .foldbtn { background: none; border: 1px solid #1f6fb2; color: #1f6fb2; border-radius: 6px; padding: 3px 10px; font-size: 13px; cursor: pointer; }
  .foldbtn:hover { background: #eaf2fa; }
  .rellinks a { display: inline-block; margin: 0 8px 8px 0; padding: 5px 12px; background: #eef4fa; border-radius: 999px; color: #1f6fb2; text-decoration: none; }
  .rellinks a:hover { background: #dce9f6; }
  .btn { background: #1f6fb2; color: #fff; border: 0; border-radius: 6px; padding: 9px 16px; font: inherit; font-size: 15px; cursor: pointer; }
  .btn:hover { background: #185a94; }
  .btn:disabled { opacity: .55; cursor: default; }
  .status { color: #4a5568; font-size: 14px; margin: 10px 0 0; }
  .sumout { margin-top: 12px; }
  .ailabel { font-weight: 700; color: #1f6fb2; font-size: 14px; margin: 0 0 8px; }
  .aibox { border: 1px solid #1f6fb2; background: #f7fbff; border-radius: 8px; padding: 12px 16px; }
  .aibox p { margin: 0 0 8px; }
  .aibox p:last-child { margin-bottom: 0; }
  .empty { background: #fff; border: 1px solid #dde3ea; border-radius: 8px; padding: 18px 22px; color: #4a5568; }
  @media (max-width: 880px) {
    .layout { flex-direction: column; }
    aside { position: static; width: 100%; flex: none; }
  }
</style>
</head>
<body>
<header>
  <h1>Neurotechnology and the administration of justice — research wiki</h1>
  <p class="desc" id="desc"></p>
</header>
<div class="layout">
  <aside>
    <h2>Concepts</h2>
    <ul id="conceptList"></ul>
    <form id="addForm">
      <label for="addInput">Add a concept</label>
      <input id="addInput" type="text" placeholder="type a term, press Enter" autocomplete="off">
    </form>
    <p class="side-note">Counts: passages whose full text contains the concept's term(s), ignoring case and line breaks. Added concepts last only until reload.</p>
  </aside>
  <main id="main"></main>
</div>
<script>
...
</script>
</body>
</html>
```

JS full:

```js
(function(){
"use strict";
var LIB = window.WORKSHOP_DATA && window.WORKSHOP_DATA.library ? window.WORKSHOP_DATA.library : {records:[]};
var docs = LIB.records || [];
var BASE = [
  {name:"Mental privacy", terms:["mental privacy"]},
  {name:"Freedom of thought", terms:["freedom of thought"]},
  {name:"Self-incrimination", terms:["self-incrimination"]},
  {name:"Lie detection", terms:["lie detection","deception detection","brain fingerprinting"]},
  {name:"Consent", terms:["consent"]},
  {name:"Neural data", terms:["neural data"]},
  {name:"Data solidarity", terms:["data solidarity"]},
  {name:"Proportionality", terms:["proportionality"]}
];
var concepts = BASE.map(function(c){ return {name:c.name, terms:c.terms.slice()}; });
var current = concepts[0].name;

function el(tag, cls, text){ var e=document.createElement(tag); if(cls) e.className=cls; if(text!==undefined && text!==null) e.textContent=String(text); return e; }
function norm(s){ return (s||"").toLowerCase().replace(/\s+/g," ").trim(); }
function matches(text, terms){ var t=norm(text); for(var i=0;i<terms.length;i++){ if(t.indexOf(norm(terms[i]))!==-1) return true; } return false; }
function passagesFor(concept){
  var out=[];
  docs.forEach(function(d){ (d.passages||[]).forEach(function(p){ if(matches(p.text, concept.terms)) out.push({doc:d, p:p}); }); });
  return out;
}
function surname(n){ var parts=(n||"").trim().split(/\s+/); return parts[parts.length-1]||n; }
function citeAuthor(doc){
  if(doc.kind==="Journal article"){
    var names=(doc.author||"").split(/\s+and\s+|,|;/).map(function(s){return s.trim();}).filter(function(s){ return s && !/^(et al\.?|others?)$/i.test(s); });
    if(names.length>=3) return surname(names[0])+" et al.";
    if(names.length===2) return surname(names[0])+" & "+surname(names[1]);
    if(names.length===1) return surname(names[0]);
  }
  return doc.author||"";
}
function citation(doc,p){
  if(p.paragraph!==null && p.paragraph!==undefined && p.paragraph!=="" && doc.symbol) return doc.symbol+", para. "+p.paragraph;
  return citeAuthor(doc)+" "+(doc.year||"")+", p. "+(p.page_label||p.page);
}
```

Hmm — "self-incrimination": should I also match "self incrimination"? Spec says keep simple where nothing said. Keep single.

Wait, one concern: "freedom of thought" — GC22 title contains "freedom of thought, conscience and religion" — passages will match. Good.

renderSidebar, select, renderMain, onDraft, init as planned.

onDraft:

```js
var drafting=false;
function onDraft(btn,status,out,concept,items){
  if(drafting) return;
  var n=Math.min(12, items.length);
  var sent=items.slice(0,n);
  status.textContent="Sending "+n+" passage"+(n===1?"":"s")+" to the model — they leave the browser…";
  btn.disabled=true; drafting=true;
  var lines=sent.map(function(it,i){ return (i+1)+". "+citation(it.doc,it.p)+"\n"+it.p.text; }).join("\n\n");
  var prompt=[
    "You are assisting human rights professionals (diplomats, NGO, NHRI and UN staff).",
    "Below are "+n+" verbatim passages from documents about neurotechnology and the administration of justice, each with its citation.",
    "",
    "Task: write exactly three sentences that summarise what these passages say about \""+concept.name+"\".",
    "Each sentence must end with the citation of the passage it rests on, in parentheses. Use only the passages below; do not invent anything.",
    "",
    "Passages:",
    lines
  ].join("\n");
  var done=function(){ btn.disabled=false; drafting=false; };
  if(typeof studio==="undefined" || !studio.ask){ status.textContent="The model is not available in this session."; done(); return; }
  studio.ask(prompt).then(function(ans){
    status.textContent="";
    out.innerHTML="";
    out.appendChild(el("p","ailabel","Written by AI. "+n+" passage"+(n===1?"":"s")+" were sent to the model and left the browser."));
    var box=el("div","aibox"); box.setAttribute("data-source","ai");
    String(ans||"").split(/\n+/).map(function(s){return s.trim();}).filter(Boolean).forEach(function(s){ box.appendChild(el("p",null,s)); });
    out.appendChild(box);
    done();
  }).catch(function(err){
    status.textContent="The model could not be reached: "+((err && err.message)||err);
    done();
  });
}
```

Note: studio.ask(prompt) — spec says `await studio.ask(prompt, {json:true})`; without json it returns string presumably. Call `studio.ask(prompt)` — fine.

renderMain as planned. Also in renderMain, after building, if items empty show empty message.

Init: header desc, hash, listeners, render.

Also the sidebar note about counts. Good.

Double-check "Table 'Passages by kind of document': one row per kind, and a total." — I show only kinds present. Hmm, "one row per kind" could mean per kind in the library. If a kind has 0 for the concept, showing it with 0 still "adds up". Which is better for test 1? Both pass. But consider: if I show all 6 kinds always, rows add to total too. I'll show only kinds with ≥1 — cleaner. Actually wait, re-read: "Table 'Passages by kind of document': one row per kind, and a total." Ambiguous; nonzero-only is safe and clean. Keep.

Also group heading includes passage count — extra info, fine.

Citation link for passages in docs without symbol (journal articles): "Szoszkiewicz & Yuste 2025, p. 3469" — link still calls openSource(doc.id, page). Good.

Now assemble final. Also ensure the h1/desc: desc computed: LIB.title e.g. "Research library on neurotechnology in the administration of justice (PDFs)"? The data says title: "a research library on neurotechnology in the administration of justice (PDF)". source field exists. Use them.

Years: docs have year. Compute min–max.

Edge: LIB.count is 9 documents — use docs.length (same). Use LIB.count if present else docs.length. I'll use docs.length.

Write final response: short intro (≤3 sentences) + code block. Nothing after.

Let me count roughly lines — fine.

One more check on fold: "the text folded after three lines" — line-clamp:3. "text is shown character for character; the fold hides, never shortens" — full text in DOM, clamp only visually hides. Good.

Related concepts as links — done, with counts.

"Add a concept: type a term, press Enter" — form submit on Enter. Good.

Also make sure clicking sidebar concept updates hash and re-renders; initial load reads hash.

Potential pitfall: `history.replaceState` with hash — fine offline.

Also add `rel="noopener"` on external links.

Now finalize the code text. Also careful: in JS strings I use typographic quotes “ ” via unicode escapes or literal — literal is fine in UTF-8.

Write it.