Let me plan this app carefully. The user wants a single HTML file app that parses `WORKSHOP_DATA.html_doc` (E/C.12/GC/27 HTML), extracts numbered paragraphs, checks against reference, and provides tabs.

Key requirements:
- Header: monospace label "UN DOCUMENT · HTML", serif title, one line with symbol linked to doc_url, "adopted reference.adopted", source. Right: green/red dot "n of m checks pass", "1 source limit".
- Left rail: "DOCUMENT" heading, card with symbol + short title, big numbers "n paragraphs of reference.paragraphs" with thin bar, "0 footnotes of reference.footnotes" in red, "n of m checks pass" linking to tab 04.
- Tabs: 01 RESULT · 02 PARAGRAPHS · 03 LOST & CHANGED · 04 CHECKS & EXPORT, role="tablist" with arrow-key navigation.
- Tab 01: four tiles with big serif numbers + "How this is computed" lines.
- Tab 02: table of paragraphs: No. | Section | First line | Check. Closed "Headings found: n" box. Rows expand in place with full text, reference six words vs found six, repaired places marked, Copy citation button.
- Tab 03: three blocks: Lost footnotes, Changed spaces (table Paragraph | Before | After | Rule), Changed characters (Character | Count | Example).
- Tab 04: check panel (one line per check), Export buttons (JSON, Markdown), closed "Elements found (n)" heading with table Tag | Classified as | Text.
- Footer: source, built, "Done by this page's code; no model was called and nothing left the browser."

Pipeline:
- Parse html with DOMParser.
- Classify: elements inside first `<table>` = cover. After it: `<p>` matching `/^(\d{1,3})\.\s*(.*)$/s` = paragraph; first `<h2>` = title; other h2/h3 = headings split by `/^([IVX]+|[A-Z])\.\s*(.+)$/`; other `<p>` = committee line.
- text_raw = text after number+full stop, trimmed, whitespace collapsed.
- Repairs: text = text_raw with space inserted:
  - `/([a-z])\.([A-Z])/g` → "$1. $2" (sentence join)
  - `/([a-z]),([A-Za-z])/g` → "$1, $2" (comma join)
  - `/([a-z])“/g` → "$1 “" (quote join)
  - `/–([A-Za-z])/g` → "– $1" (dash join)
  Each insertion logged with paragraph, rule, 20 chars each side.
- Characters counted over all paragraph texts: U+2013, U+201C, U+201D, U+2019, U+2011, U+00A0. text keeps them.
- Section = nearest heading above; part = nearest roman-numbered h2.
- First words: first six whitespace-separated words of text vs reference.first_words[String(number)], normalized (curly quotes → straight, en dash and U+2011 → hyphen, U+00A0 → space), case kept.
- Citation = symbol + ", para. " + number.
- Checks: paragraph count, numbering (1..n in order), first words, footnotes (source limit), repairs, headings, nothing lost (every block element classified exactly once, counts sum to total), export round trip.

Edge cases: missing reference → "no reference in this file", checks "not run"; no `<p>` → tab 01 says so, exports disabled.

Design: paper #f4f0e8, ink #1d1b18, rules #d9d2c3, accent #9b2335, green for pass (dark green, e.g. #1e6b3a). Serif Georgia for title/big numbers, monospace labels, sans 16px body. [hidden]{display:none!important}. Focus ring red. No external resources. Chart.js not needed here (no charts required — bars are thin divs).

Credits line: sources consulted — The Turing Way (CC BY), UK Government Analysis Function (OGL? The QA of code guidance is under OGL — actually best-practice-and-impact repo is CC BY 4.0? The guidance says "Quality assurance of code for analysis and research" — UK Government Analysis Function guidance is licensed under Open Government Licence? Hmm. The Turing Way is CC BY 4.0. Dag Hammarskjöld Library Ask DAG — UN content, generally public domain-ish but not explicitly licensed. The instruction says: "If you use code or wording from a 'Reference shelf excerpts' page that has an open licence (MIT, Apache, BSD, ISC, CC BY), add a small 'Credits' line". The Turing Way is CC BY 4.0 — I'll credit it. The others I'm not certain of licence; I'll credit The Turing Way CC BY 4.0 and mention the others as consulted without claiming licence, or just credit Turing Way. Safer: "Credits: method follows The Turing Way, 'Documentation and metadata' (CC BY 4.0); check design follows UK Government Analysis Function, 'Testing code'; citation format follows Dag Hammarskjöld Library, Ask DAG." That names sources; only claim CC BY for Turing Way.

Layout: header + left rail + tabs. Left rail narrow (~260px), main content right. On laptop no horizontal scroll.

Let me think about structure:

```
<body>
  <header> label, title, meta line, status dot </header>
  <div class="layout">
    <aside class="rail"> DOCUMENT card, big numbers, checks link </aside>
    <main>
      <div role="tablist"> 4 tabs </div>
      <section id="tab-01" role="tabpanel"> tiles </section>
      <section id="tab-02" role="tabpanel"> headings box + table </section>
      <section id="tab-03" role="tabpanel"> three blocks </section>
      <section id="tab-04" role="tabpanel"> checks + export + elements </section>
    </main>
  </div>
  <footer> source, built, no-model line, credits </footer>
</body>
```

Tab behavior: click switches; arrow keys left/right move; hidden panels get `hidden` attribute; also set `aria-selected`, `tabindex`. Hidden tab panel not focusable — using `hidden` attribute handles that.

Data model in JS:

```js
const D = window.WORKSHOP_DATA.html_doc;
const ref = D.reference || null;
const doc = new DOMParser().parseFromString(D.html, 'text/html');
```

Classification: iterate `doc.body.children` (block elements in order). Actually "over the parsed document's body elements in order" — I'll iterate over body's element children. But the table contains nested elements; "Elements inside the first `<table>` are cover" — classify the table itself as cover (one element). The "nothing lost" check: "Every block element is classified exactly once and the counts per class sum to the total". I'll classify top-level children of body: table → cover; p → paragraph/committee; h2 → title/heading; h3 → heading. But what about other tags (div.content wraps everything?). In the sample, html is `<body><table>...</table><div class="content">...</div></body>`. Hmm — the sample shows a `<div class="content">` wrapping the rest. So top-level children: table, div.content. The div contains the p's and h2s. So I should iterate recursively but treat the table's descendants as cover. Better approach: walk all elements in document order (body.querySelectorAll('*')), but skip descendants of the first table. Classify each element: if it's inside first table → cover (but count once? "every block element classified exactly once" — I'll count the table and its descendants all as cover? Simpler: classify each element not inside the table; the table itself is one "cover" element. For the "Elements found" table on tab 04, list every block element in order: Tag | Classified as | Text (first 80 chars). I'll list top-level-ish block elements: for the table, one row; for elements inside div.content, each row. Let me define: collect elements via a walk: start at body children; if element is the first table → push as cover, don't descend; else push element, and descend into it if it has element children that are block-level (div). Actually simplest: get all elements in document order excluding those inside the first table: 

```js
const all = [...doc.body.querySelectorAll('*')].filter(el => !el.closest('table'));
```

But that includes inline elements inside p (span etc.). "every block element" — filter to block-level tags: P, H1-H6, DIV, TABLE, UL, OL, LI, etc. I'll use a set: ['P','H1','H2','H3','H4','H5','H6','DIV','TABLE','UL','OL','LI','BLOCKQUOTE','SECTION','ARTICLE','PRE']. The div.content would be one row classified as "container". Then classification of paragraphs: among these block elements (excluding table descendants), a P matching the number regex → paragraph; first H2 → title; other H2/H3 → heading; other P → committee/other.

Wait — the div.content is a block element; classify as "container". Counts per class: cover (1 table), container (1 div), title (1 h2), headings (h2+h3 count), paragraphs (90), committee (1 p). Sum = total block elements. Good.

But careful: if there's no wrapping div (other files), body children directly. The walk handles both.

Paragraph extraction: for a P classified as paragraph, match `/^(\d{1,3})\.\s*(.*)$/s` on its textContent. Note textContent of "1.A clean..." gives "1.A clean...". Number = parseInt. text_raw = group 2, trimmed, collapse whitespace: `.replace(/\s+/g,' ').trim()`.

Hmm, but collapsing whitespace with \s+ — non-breaking space U+00A0 is matched by \s in JS regex? Yes, \s includes U+00A0 in JavaScript. But the spec says text keeps U+00A0 as published... "runs of whitespace collapsed to one space" — if \s+ collapses U+00A0 runs to a normal space, that would change characters. The character count says non-breaking space counted over paragraph texts and "text keeps them as published". Hmm, conflict: collapsing whitespace would remove U+00A0. The plan says "2 non-breaking spaces inside headings" — inside headings, not paragraphs. So in paragraphs maybe no U+00A0. To be safe: collapse only ASCII whitespace `[ \t\n\r\f\v]+` → ' ', and trim. That preserves U+00A0. I'll use `.replace(/[ \t\n\r]+/g,' ').trim()` — trim() removes U+00A0 too at edges... trim removes \s including U+00A0. Edge case unlikely; but to be careful use replace on ASCII whitespace and trim via replace of ASCII whitespace at ends. Fine.

Repairs: apply rules to text_raw sequentially, logging each insertion. Rules:
1. sentence: `/([a-z])\.([A-Z])/g` → '$1. $2'
2. comma: `/([a-z]),([A-Za-z])/g` → '$1, $2'
3. quote: `/([a-z])“/g` → '$1 “'
4. dash: `/–([A-Za-z])/g` → '– $1'

Log: {para, rule, before: 20 chars each side of match, after}. For logging, during replace use a function to capture context: the 20 chars before match start and 20 after match end in the original string.

Order matters: apply sentence first, then comma, quote, dash. Each rule applied to result of previous. Log each insertion with rule name and context from the string at time of that rule.

Character counts: over all paragraph `text` values (after repair): count U+2013, U+201C, U+201D, U+2019, U+2011, U+00A0. Note U+201C and U+201D both counted as "double quotes" — the plan says "double quotes (U+201C, U+201D)" as one row presumably, count = sum. Rows: en dash, double quotes, right single quote, non-breaking hyphen, non-breaking space. Example: find first paragraph containing it, show ~30 chars around.

First words: `text.split(/\s+/).slice(0,6).join(' ')` — but \s includes U+00A0; for first-words comparison we normalize anyway. Normalization function: replace U+2018/U+2019 → ', U+201C/U+201D → ", U+2013/U+2014/U+2011 → '-', U+00A0 → ' '. Compare normalized found vs normalized reference. Case kept.

Reference first_words keyed by string number. If ref missing or key missing → check "not run" or mismatch? If reference missing entirely: tiles say "no reference in this file", checks "not run". If key missing for a paragraph, treat as mismatch? Better: mark as "no reference" for that para — but simpler: if ref missing → not run; if key missing → count as mismatch with "reference has no entry". I'll handle: if ref && ref.first_words && key exists → compare; else if ref exists but no key → mismatch listed as "no reference entry". Keep simple.

Checks list (tab 04), each: name, what compared, values, status: pass / fail / source limit / not run:
1. Paragraph count: found vs ref.paragraphs.
2. Numbering: sequence 1..n in order; gaps/duplicates listed.
3. First words: mismatches listed "para. n: found … / reference …".
4. Footnotes: 0 vs ref.footnotes → "source limit" (counted apart from failures).
5. Repairs: n spaces restored in n paragraphs, per rule counts.
6. Headings: count h2/h3, glued labels separated count.
7. Nothing lost: every block element classified once; counts sum to total; unclassified listed.
8. Export round trip: parse downloaded JSON, record count equals table rows. This runs when? "The JSON to download is parsed back; its record count equals the table's." I can run it at build time: construct the JSON string, JSON.parse it, compare length to paragraphs.length. Do it in pipeline once.

Status dot in header: "n of m checks pass" green if all non-source-limit checks pass, red if any fail; plus "1 source limit" always (footnotes). If ref missing, checks "not run" — dot maybe neutral. Keep: failures count > 0 → red "n checks failed"; else green "n of m checks pass". m = total checks run (excluding source limit? or including?). I'll say m = checks that ran (pass+fail), source limits counted separately: "1 source limit".

Tab 01 tiles:
- Paragraphs found: n (big) beside "the document has ref.paragraphs" — green when equal, red with difference (e.g. "−2" or "+3").
- First words match: n of ref.paragraphs.
- Footnotes: 0 of ref.footnotes, red, "this HTML version has none; see tab 03".
- Spaces: n repaired or flagged, link to tab 03.
Each tile has "How this is computed" line.

If no reference: tiles say "no reference in this file". If no paragraphs: tab 01 says "no paragraphs found in this HTML" and exports disabled.

Tab 02: closed "Headings found: n" box (button aria-expanded) listing headings (label + heading text, maybe with tag). Table with caption "n paragraphs found, m expected" + "TAB.02". Columns: No. | Section | First line | Check. No. right-aligned, red accent. Section = nearest heading's heading text (or label?). Plan: "Section is the nearest heading above the paragraph ('Right to work (art. 6)')". So use the heading text after label split; if no match, full text. Expanded row shows full path: part › section, e.g. "IV. … › Right to work (art. 6)". Full path: nearest roman h2 label+heading, then nearest heading. I'll show "part label. part heading › section heading".

Row expansion: I'll implement table rows where clicking the row (a button inside first cell? or whole row clickable) toggles a detail row below. Accessibility: "Rows are buttons with aria-expanded". I'll make each row a `<tr>` containing a `<button class="rowbtn" aria-expanded="false">` spanning... Simpler: make the first cell contain a button with the number, aria-expanded, and clicking anywhere on row toggles. To keep "rows are buttons", I'll put a button in the No. cell that covers... Hmm, plan says "Rows are buttons with aria-expanded; click or Enter expands the row in place". I'll make the whole `<tr>` clickable via a button in the first cell styled to fill, plus row click handler. Actually cleanest: each data row is a `<tr class="prow">` with a `<button>` in the first `<td>` (the number), aria-expanded, aria-controls pointing to detail row id. Also add click handler on the tr. Keyboard: button handles Enter/Space natively. Good enough.

Detail row: full text verbatim (in `text`? or `text_raw`?). "the full text, verbatim, never shortened" — show `text` (repaired) with repaired places marked by thin red box, and maybe also raw? The plan: "the expanded row shows the full text, verbatim, never shortened; the reference's six words beside the found six; the places repaired or flagged in this paragraph; and a Copy citation button". I'll show the repaired text with `<mark class="fix">` around inserted spaces... marking an inserted space is tricky — I can wrap the boundary: e.g. "levels.<span class=fix> </span>Key"? A thin red box around the space. I'll render text with repaired positions wrapped in a span with red outline. To do that, during repair I know match indices; I can build the display text by splicing spans. Let me implement repair to also produce segments: array of {t: string, fix: bool}. When inserting a space, the inserted space becomes a fix segment. Then render: escape HTML, wrap fix segments in `<span class="fix"> </span>` (the space itself inside the box). Also show text_raw below in a smaller "as found in the HTML" line? The plan says text_raw is an export field; showing it helps honesty. I'll include a small line "as found (raw): …" maybe only if different. Keep: if repairs>0 for the para, show raw too. Actually simpler: always show full repaired text with marks; plus a line "raw text differs in n places — see tab 03". Hmm, plan says expanded row shows "the places repaired or flagged in this paragraph" — I'll list them: rule + context (before → after). And show reference six words vs found six. And Copy citation button.

First line column: first 120 chars of text cut at word boundary + "…".

Check column: "OK" green or "first words differ" red.

Tab 03:
- Block 1 "Lost: footnotes" with count ref.footnotes: paragraph text as specified.
- Block 2 "Changed: spaces": count per rule above table; table Paragraph | Before | After | Rule. Before/After: 20 chars each side with inserted space marked — I'll show before context and after context, with the inserted space shown as "·" or marked. E.g. Before: "…levels.Key…" After: "…levels. Key…". Clicking a row opens the paragraph on tab 02 (switch tab and expand that row, scroll to it).
- Note text about Giventhe etc.
- Block 3 "Changed: characters": table Character | Count | Example. Rows: en dash –, double quotes “ ”, right single quote ’, non-breaking hyphen ‑, non-breaking space (nbsp). Hint monospace. Note text about search.

Tab 04:
- Check panel: "every check on one line" — a list/table: Check | Compared | Result. Status words colored.
- Export: two buttons Download JSON, Download Markdown. Disabled if no paragraphs.
- JSON: array of records with fields symbol, paragraph, section, part, text, text_raw, first_words_match, citation, doc_url, limitations.
  - part: "the nearest heading and the roman-numbered section above it" — part field = roman section, section = nearest heading. I'll set section = nearest heading full display (label + heading?), part = roman h2 display. Let me define heading display: if split matched, display = label + ". " + heading? e.g. "D. Obligation" or "Right to work (art. 6)" for plain h3 (no label match → label null, heading = full text). For section field I'll use the heading text (after label if split, else full). For part: roman h2 → its heading text; maybe include label "IV. ...". I'll make part = `${label}. ${heading}` trimmed for roman h2, e.g. "IV. ...". Hmm the h2 text is like "IV.Sustainable..."? Sample: "I.Introduction" glued. Split regex `/^([IVX]+|[A-Z])\.\s*(.+)$/` on "I.Introduction" → label "I", heading "Introduction". Display part: "I. Introduction". Section for h3 "Right to work (art. 6)" — no label match (starts with "R" capital... wait regex `[A-Z]\.` requires a letter followed by period; "Right to work (art. 6)" — "R" then "ight" — no period after R, so no match; good, heading = full text). But careful: h3 like "D. Obligation" matches with label "D". And something like "A. Something" matches. But a plain heading like "Annex" wouldn't match. Edge: heading "B.1 something"? Not our concern.
  
  Actually wait: the split regex on h2 "I.Introduction": `^([IVX]+|[A-Z])\.\s*(.+)$` — "I" matches [IVX]+, then ".", then "Introduction". Good. But what about a title h2? First h2 is title, excluded. What about h2 like "IV. ..."? fine.
  
  Hmm, one risk: a plain h3 like "Freedom of opinion" — "F" then "reedom" — no dot, no match. Good. But "A. " lettered h3s match. OK.

- Markdown export: front matter between --- lines: title, symbol, adopted, source_url, extracted (today's date), paragraphs_found, paragraphs_expected, footnotes (sentence). Then headings as ## / ### lines in document order and each paragraph as its number in bold then text. So I need to reconstruct document order of headings and paragraphs interleaved. I'll keep an ordered list of items (headings and paragraphs) during classification. Markdown: for h2 (non-title) → `## label. heading` or `## text`; h3 → `### ...`; paragraph → `**n.** text`. Title h2 → maybe `# title`? Plan says "then the headings as ## and ### lines in document order and each paragraph as its number in bold, then its text". The title h2 — I'll emit as `# title` (it's the document title; front matter has title too). Hmm "the headings as ## and ###" — the title h2 could be `#`. I'll do: title h2 → `#`, other h2 → `##`, h3 → `###`. Reasonable.

- File names: symbol with slashes → hyphens, e.g. "E-C.12-GC-27.json" / ".md". Blob URL, UTF-8, download attribute, click.

- Closed "Elements found (n)" heading (button aria-expanded) with table Tag | Classified as | Text (first 80 chars). Rows = block elements in order.

Footer: source, built, no-model line, credits.

Left rail details: "DOCUMENT" heading; card with symbol monospace + short title. Short title — html_doc has `title` only (no short_title). The rail says "the short title" — I'll derive: title is long ("General comment No. 27 (2025) on economic, social and cultural rights and the environmental dimension of sustainable development"). Short title could be "General comment No. 27 (2025)". I can derive by cutting at " on " — hmm, risky to hardcode. I could just show the full title in the card, smaller. Or derive short = title up to first " on " if present. I'll do: `title.split(' on ')[0]` if it contains ' on ' else title. That gives "General comment No. 27 (2025)". Reasonable, computed not hardcoded.

Big numbers on rail: "n paragraphs of ref.paragraphs" with thin bar (red when short or over) — bar width = n/ref*100% capped 100%, red if n≠ref. "0 footnotes of ref.footnotes" in red "not in this HTML". Then "n of m checks pass" link to tab 04.

Header right: dot + "n of m checks pass" or "n checks failed", then "1 source limit".

Now checks computation details:

Check 1 Paragraph count: found = paragraphs.length, expected = ref?.paragraphs. pass if equal.
Check 2 Numbering: expected sequence 1..found? "Exactly 1 to n in order; gaps and duplicates listed." n = ref.paragraphs if present else found. I'll check that paragraph numbers are exactly 1..max in order without gaps/dupes: iterate, expected counter 1; if numbers[i] !== i+1 → record gap/duplicate. Compare against ref.paragraphs too? The check: "Numbering. Exactly 1 to n in order". I'll check numbers form 1..N contiguous in order (N = found count), and list any deviations. Pass if contiguous.
Check 3 First words: mismatches list.
Check 4 Footnotes: 0 vs ref.footnotes → source limit.
Check 5 Repairs: count insertions, per rule, in how many paragraphs.
Check 6 Headings: h2 count (excluding title), h3 count, glued labels separated (headings where label regex matched and original had no space after dot? "how many glued labels were separated" — count headings where text matched `/^([IVX]+|[A-Z])\./` without space, i.e. `.\S`). I'll count headings whose raw text matches `/^([IVX]+|[A-Z])\.[^\s]/`.
Check 7 Nothing lost: block elements total, classified counts sum, unclassified list (elements classified as "unclassified" — e.g. a div that's not container? I'll classify div as container; any other block tag → "other/unclassified" listed). Let me define classes: cover (table), container (div), title (first h2), heading (h2/h3), paragraph (p with number), other-p (p without number → "committee/other line"). Every block element gets a class; unclassified = none by construction unless tag not in block set — but then it's not counted at all. To make the check meaningful: total block elements counted; each assigned exactly one class; sum of class counts === total; list any element whose class is "unclassified" (I'll assign "unclassified" to block tags that aren't p/h2/h3/table/div, e.g. ul/li). Pass if sum matches and no unclassified.
Check 8 Export round trip: build JSON string, parse, length === paragraphs.length.

m for header: checks that ran = pass + fail (source limit counted separately, "not run" excluded). If ref missing: checks needing ref → "not run"; dot shows... I'll show "checks not run" neutral? Keep simple: if no failures and some pass → green "n of m checks pass"; if failures → red; if none ran → grey "no checks run". Plus "1 source limit" when footnotes check is source limit (always, if ref present). If ref missing, footnotes check "not run" and no source limit label? The header says "1 source limit" — I'll show it when the footnotes check is source-limit status.

Now the "Spaces: n repaired or flagged" tile — n = total insertions. "repaired or flagged" — all insertions are repairs; flagged = first-words mismatches? I'll say n = spaces restored (repairs), link to tab 03.

Tab switching function: `showTab(i)` sets hidden on panels, aria-selected, tabindex, moves focus? Arrow keys: on tablist keydown, ArrowRight/Left moves and activates (focus + select). Home/End too maybe. Keep simple: left/right.

"Clicking a row [on tab 03] opens the paragraph on tab 02": function openParagraph(n): showTab(1), expand row n, scrollIntoView.

Copy citation: navigator.clipboard.writeText with fallback (execCommand). Show "Copied" for 2s. Clipboard may fail in sandbox — fallback: create textarea, select, document.execCommand('copy'). Wrap in try.

Exports disabled when no paragraphs: set disabled attribute + title.

Now sizes: 90 paragraphs, table with 90 rows + detail rows. Fine. Keep under 1500 lines.

Let me now think about the repair logging with context. Implementation:

```js
function repair(textRaw, paraNum, log) {
  let text = textRaw;
  const segments = [{t: text, fix:false}]; // hmm, building segments across sequential rules is complex
```

Simpler: run rules sequentially on a plain string, logging each insertion with before/after context strings (20 chars each side from the current string). For display marking in the expanded row, I can re-run and build HTML: process rules one at a time, each time producing new string and marking inserted spaces. Approach: maintain `html` string built from escaped text with markers. Alternative simpler approach: after computing final `text` and knowing insertion positions... positions shift across rules.

Alternative: build segments incrementally. Start segments = [{t: textRaw, fix:false}]. For each rule, scan segments: for each non-fix segment, apply regex with a replacer that splits the segment into [before, insertedSpace(fix), after]. Since rules only insert a space at match point, I can process each segment independently:

```js
function applyRule(segments, regex, ruleName, paraNum, log) {
  const out = [];
  for (const seg of segments) {
    if (seg.fix) { out.push(seg); continue; }
    let last = 0, m;
    regex.lastIndex = 0;
    let buf = '';
    while ((m = regex.exec(seg.t))) {
      buf += seg.t.slice(last, m.index);
      const inserted = m[0].length === ... 
```

Hmm, replacement: for sentence rule `/([a-z])\.([A-Z])/g` → "$1. $2": the inserted char is a space between m[0][1] (the '.') and m[0][2]. Actually m[0] = "a.K" (3 chars), replacement "a. K". The inserted space goes after index 1 within the match. General: I can compute replacement string via m[0].replace(regex, '$1. $2')? Easier: use a replacer function that returns the replacement, then find where the space is inserted: replacement length = m[0].length + 1, and the inserted space position = index of the space in replacement. For our rules, replacement = m[0] with a space inserted at a known spot. Let me just define rules as objects with regex and a function that returns {pre, ins, post} split of the match:

- sentence: match "a.K" → pre "a.", ins " ", post "K". Using capture groups: pre = m[1]+'.', ins=' ', post=m[2]. But regex `/([a-z])\.([A-Z])/` — m[1] is the lowercase, then literal '.', m[2] uppercase. pre = m[1] + '.', post = m[2].
- comma: `/([a-z]),([A-Za-z])/` → pre = m[1]+',', post = m[2].
- quote: `/([a-z])“/` → pre = m[1], post = '“'. ins ' ' between.
- dash: `/–([A-Za-z])/` → pre = '–', post = m[1].

So each rule: {name, re, split: m => [pre, post]}. Then insertion of ' ' between pre and post.

```js
function applyRule(segments, rule, paraNum, log) {
  const out = [];
  for (const seg of segments) {
    if (seg.fix) { out.push(seg); continue; }
    let last = 0, m, found = false;
    rule.re.lastIndex = 0;
    while ((m = rule.re.exec(seg.t)) !== null) {
      const [pre, post] = rule.split(m);
      const before = seg.t.slice(Math.max(0, m.index - 20), m.index);
      const after = seg.t.slice(m.index + m[0].length, m.index + m[0].length + 20);
      out.push({t: seg.t.slice(last, m.index) + pre, fix:false});
      out.push({t: ' ', fix:true});
      out.push({t: post, fix:false});
      log.push({para: paraNum, rule: rule.name, before: before + m[0] + after, after: before + pre + ' ' + post + after});
      last = m.index + m[0].length;
      found = true;
      if (m[0].length === 0) rule.re.lastIndex++; // safety
    }
    out.push({t: seg.t.slice(last), fix:false});
  }
  return out;
}
```

Wait — logging before/after: "20 characters each side". before context = 20 chars before match, after = 20 chars after match. I'll store `before: ctxBefore + m[0] + ctxAfter` and `after: ctxBefore + pre + ' ' + post + ctxAfter`. In tab 03 table, Before column shows the before string with the joined part, After shows with space; the inserted space marked — I can wrap in the after cell: show `after` with the space replaced by a marked span. Simpler: in the table, Before cell = before string, After cell = after string where I insert a `<span class="fix">·</span>`? The plan: "the inserted space marked". I'll render After as HTML with the inserted space wrapped in a red-boxed span containing the space (visible as a small box). I'll construct: afterHtml = escape(ctxBefore) + escape(pre) + '<span class="fix"> </span>' + escape(post) + escape(ctxAfter). And Before = escape(ctxBefore + m[0] + ctxAfter). Good — I'll store structured log entries: {para, rule, ctxBefore, match, pre, post, ctxAfter}.

Then text = segments.map(s=>s.t).join(''). textHtml = segments.map(s => s.fix ? `<span class="fix">${escape(s.t)}</span>` : escape(s.t)).join('').

Note: applying rules sequentially — after sentence rule inserts spaces, comma rule runs on new segments; fix segments skipped (they're just spaces, won't match anyway since rules need letter on both sides... a fix space between letters: comma rule `/([a-z]),([A-Za-z])/` needs comma; fine. Dash rule `/–([A-Za-z])/` — if a fix space follows the dash? e.g. "challenges –to": dash rule matches "–t" → inserts space → "– to". Then no further. OK. But careful: sentence rule on "levels.Key" inserts space; then could comma rule match across? No.

One subtlety: quote rule `/([a-z])“/g` — pre = m[1], post = '“'. Replacement "$1 “". Good.

Also note: the sentence rule could wrongly fire on abbreviations like "art. 6"? "art. 6" has space already. "e.g." followed by capital? "e.g.States"? Unlikely. The plan says rules only where characters prove it; fine, follow the plan.

Character counts over all paragraph texts (the repaired `text`). Count each char. Examples: find first occurrence in any paragraph text, show context 30 chars.

First words: `const words = text.split(/[\s\u00A0]+/).filter(Boolean).slice(0,6).join(' ')` — hmm \s already includes \u00A0 in JS. Use split(/\s+/). Normalize both sides: 

```js
function norm(s){return s.replace(/[\u2018\u2019]/g,"'").replace(/[\u201C\u201D]/g,'"').replace(/[\u2013\u2014\u2011]/g,'-').replace(/\u00A0/g,' ');}
```

Compare norm(foundSix) === norm(refSix). Case kept (no lowercasing).

reference.first_words keys are strings of paragraph numbers.

Now headings tracking: maintain `currentPart` (roman h2) and `currentSection` (nearest heading) as we walk block elements in document order. Also ordered items list for markdown: push {type:'h2'|'h3'|'p', ...}.

Walk: 

```js
const blockTags = new Set(['P','H1','H2','H3','H4','H5','H6','DIV','TABLE','UL','OL','LI','BLOCKQUOTE','PRE','SECTION','ARTICLE','FIGURE','HR']);
const firstTable = doc.body.querySelector('table');
const els = [];
(function walk(node){
  for (const el of node.children) {
    if (firstTable && (el === firstTable || firstTable.contains(el))) {
      if (el === firstTable) els.push({el, cls:'cover'});
      continue; // don't descend into table
    }
    if (!blockTags.has(el.tagName)) continue; // skip inline
    els.push({el});
    if (el.children.length) walk(el);
  }
})(doc.body);
```

Hmm but this pushes div.content AND its children — both block elements. That's fine: div.content classified as "container". But wait, if el is a P containing a span, we push P and don't descend into inline (span not in blockTags, skipped). Good. But if a DIV contains P's, we push div then descend. Good.

But careful: `firstTable.contains(el)` — el is a child of body; if el is inside table we skip; but we never descend into table so children of table never visited. The check `el === firstTable` handles the table itself. Actually since we don't descend into the table, only the table element itself is visited at top level. But what if table is nested in a div? Then walking div's children hits the table. Handle: in walk, if el === firstTable → push cover, continue (no descend). Also if firstTable.contains(el) → skip (shouldn't happen since we don't descend). Fine.

Classification per element (after collecting):

```js
let titleSeen = false;
for (const item of els) {
  const el = item.el, tag = el.tagName;
  const txt = cleanText(el.textContent); // collapse ASCII whitespace, trim
  if (item.cls === 'cover') { item.cls = 'cover'; continue; }
  if (tag === 'TABLE') { item.cls = 'cover'; continue; }
  if (tag === 'DIV' || tag === 'SECTION' || tag === 'ARTICLE') { item.cls = 'container'; continue; }
  if (tag === 'H2') {
    if (!titleSeen) { titleSeen = true; item.cls = 'title'; item.text = txt; continue; }
    item.cls = 'heading'; ...
  }
  if (tag === 'H3' || tag === 'H4'...) heading
  if (tag === 'P') {
    const m = txt.match(/^(\d{1,3})\.\s*(.*)$/s);
    if (m) paragraph else 'line' (committee/other)
  }
  else item.cls = 'unclassified';
}
```

Wait — the paragraph regex on the P's full text: "1.A clean..." matches with number 1, rest "A clean...". But careful: a committee line like "Committee on Economic, Social and Cultural Rights" doesn't start with digits. Good. But what about a P that starts with a number but isn't a paragraph, e.g. a date "6 November 2025"? `/^(\d{1,3})\.\s*(.*)$/` requires a full stop after the number — "6 November" has no dot. "6. November"? unlikely. OK per plan.

Hmm — one issue: the cover table contains `<p>` elements (symbol, dates). We skip them (cover). Good — that's why "elements inside the first table are cover".

Paragraph processing: number = parseInt(m[1],10); raw = m[2] collapsed/trimmed. Note: the regex `\s*` after dot — for "1.A clean", m[2] = "A clean...". For "1. A clean", m[2] = "A clean...". Good.

Heading split: `const hm = txt.match(/^([IVX]+|[A-Z])\.\s*(.+)$/s)`. If match: label = hm[1], heading = hm[2], glued = /^\S/ test on char after dot: check `txt.slice(label.length+1).startsWith(' ')`? glued if `txt[label.length+1] !== ' '` — i.e. `/^([IVX]+|[A-Z])\.[^\s]/`. I'll compute glued = new RegExp('^'+label+'\\.[^\\s]').test(txt). Display: label + '. ' + heading.

Section tracking: when heading encountered, set currentSection = display heading (label? For section column, plan example "Right to work (art. 6)" — a plain h3 without label. For lettered h3 "D. Obligation", section display... I'll use heading text (without label) for section, and full path in expanded row: partDisplay + ' › ' + sectionDisplay where partDisplay = roman h2 display "IV. ...". Hmm, but if section is a lettered h3 under a roman h2, path = "IV. Foo › D. Obligation"? I'll include label in section display when present: sectionDisplay = label ? label + '. ' + heading : heading. And partDisplay similarly. Path = partDisplay + ' › ' + sectionDisplay (if different).

Roman h2 detection: label matches /^[IVX]+$/ → it's a part; set currentPart. Lettered h2 ([A-Z]) — is it a part? Plan: "part = the nearest roman-numbered <h2>". So only [IVX]+ h2 sets part. Lettered h2 is just a heading (section). OK.

Markdown export: iterate ordered items: for each element in els order, if cls heading: h2→'## ', h3→'### ' + display; title → '# ' + text; paragraph → '\n**' + n + '.** ' + text + '\n'. Use repaired text (text). Plan: "each paragraph as its number in bold, then its text" — use text (repaired). I'll use text.

JSON export record:
```js
{
  symbol: D.symbol,
  paragraph: p.num,
  section: p.section,      // nearest heading display
  part: p.part,            // nearest roman h2 display
  text: p.text,
  text_raw: p.raw,
  first_words_match: p.fwMatch (bool or null),
  citation: p.citation,
  doc_url: D.doc_url,
  limitations: "no footnotes in this HTML version; the document has " + ref.footnotes
}
```

If ref missing, limitations = "no footnotes in this HTML version" (without count) — handle.

Front matter markdown:
```
---
title: ...
symbol: ...
adopted: ...
source_url: D.doc_url
extracted: YYYY-MM-DD
paragraphs_found: n
paragraphs_expected: m
footnotes: "This HTML version has 0 footnotes; the document has N."
---
```

File names: symbol.replace(/\//g,'-') + '.json' / '.md'.

Download function:
```js
function download(name, content, type){
  const blob = new Blob([content], {type: type + ';charset=utf-8'});
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url; a.download = name; document.body.appendChild(a); a.click();
  setTimeout(()=>{URL.revokeObjectURL(url); a.remove();}, 100);
}
```

Export round trip check: `const jsonStr = buildJSON(); let rt = null; try { rt = JSON.parse(jsonStr).length === paragraphs.length; } catch(e){ rt = false; }`.

Now checks array structure: {name, detail, status: 'pass'|'fail'|'limit'|'notrun', link?} where link = tab index to jump. Render one line each: name — detail — status word.

Header dot: failures = checks.filter(c=>c.status==='fail').length; passes = ...'pass'; limits = ...'limit'. If failures>0: red dot, text `${failures} check${s} failed`; else if passes>0: green `${passes} of ${passes+failures} checks pass`; else grey "checks not run". Plus if limits>0: "· 1 source limit" (or `${limits} source limits`).

Rail similar.

Now tab 01 tiles:
- Tile 1: big n, side text "paragraphs found" / "the document has m" — green if equal else red with diff (n-m, show "+x"/"−x"). How computed: "Counted by this page's code: <p> elements whose text starts with a number and a full stop, in document order."
- Tile 2: "n of m" first words match. How: "First six words of each paragraph, compared with reference.first_words after normalising quotes, dashes and non-breaking spaces."
- Tile 3: "0 of m" footnotes red. How: "This HTML version contains no footnote text or marks; the count is a limit of the source, not of the app."
- Tile 4: "n" spaces repaired. How: "Four rules insert a space only where the characters prove one was there; every insertion is listed on tab 03."

If no ref: tiles show "no reference in this file" instead of m values. If no paragraphs: message "No numbered paragraphs were found in this HTML." and exports disabled.

Tab 02 headings box: closed button "Headings found: n" aria-expanded; when open, list of headings: display text + tag (H2/H3) + glued marker. 

Table: caption "n paragraphs found, m expected" + TAB.02 monospace. Columns: No. (right), Section, First line, Check. First line: `text.length>120 ? text.slice(0,120).replace(/\s+\S*$/,'') + '…' : text` — cut at word: take slice(0,120), then cut back to last space: `s.slice(0, s.lastIndexOf(' '))` + '…'. Handle.

Detail row content:
- Full path line: "IV. … › Right to work (art. 6)" monospace small.
- Full text paragraph with fix marks.
- If fw mismatch: "first words differ — found: "…" / reference: "…"". If match: "first words match the reference: "…"". Show both: found six vs reference six.
- Repairs in this paragraph: list "sentence join: "…levels.Key…" → "…levels. Key…"".
- Copy citation button + status span.

Row ids: `prow-${num}`, detail `pdetail-${num}`.

Tab 03 spaces table: caption "n spaces restored in m paragraphs" + TAB.03. Columns Paragraph | Before | After | Rule. Paragraph cell is a button/link "para. n" that opens tab 02 row. Rule names: "sentence join", "comma join", "quote join", "dash join". Count per rule above table: small line "sentence join: a · comma join: b · quote join: c · dash join: d".

Characters table: Character | Count | Example. Character shown as the actual char + name: "– en dash (U+2013)", "“ ” double quotes (U+201C/D)", "’ right single quote (U+2019)", "‑ non-breaking hyphen (U+2011)", "⍽ non-breaking space (U+00A0)" — for nbsp show "·" maybe. I'll show name + codepoint + the char in a code element. Example: 30 chars of context from first paragraph containing it, with the char highlighted (wrap in span). Count right-aligned.

Tab 04 checks panel: open by default ("The check panel, open, every check on one line"). Render as a list: each line: status word (colored) + check name + detail. E.g. "pass — Paragraph count: 90 found, 90 expected." "source limit — Footnotes: 0 in this HTML, 141 in the document; the HTML version has no footnotes: a limit of the source, not of the app." "check failed — First words: 6 differ: para. 13: found … / reference … (rows flagged on tab 02)." with link "tab 02".

Export buttons + note "The JSON file is parsed back on build; its record count equals the table's (check 8)." Maybe not needed on screen; the check line covers it.

Elements found: closed button "Elements found (n)" aria-expanded → table Tag | Classified as | Text (first 80 chars).

Footer: `source`, `built` — html_doc has source; built? The data description for html_doc: `{title, symbol, doc_url, source, html, reference}` — no `built` field mentioned. Footer says "source, built". I'll show source and built if present: `D.built` may be undefined → show "built: not stated in this file"? Hmm. The sample data description doesn't list built for html_doc. I'll render footer: source line, and if D.built exists show it, else omit gracefully: `Footer: D.source + (D.built ? ' · built ' + D.built : '') + ' · Done by this page's code; no model was called and nothing left the browser.'` Plus credits line.

Wait — the header line: "one line with the data's source, n and years" per general layout; but this plan specifies header: symbol linked, "adopted reference.adopted", source. Follow the plan.

Also general rule: "Every row that shows a document has its symbol, linked to doc_url" — header covers it; maybe also in rail card link symbol. I'll link symbol in header and rail.

Now CSS. Layout:

```css
:root{--paper:#f4f0e8;--ink:#1d1b18;--rule:#d9d2c3;--red:#9b2335;--green:#1e6b3a;}
*{box-sizing:border-box}
[hidden]{display:none!important}
body{margin:0;background:var(--paper);color:var(--ink);font:16px/1.5 -apple-system,'Segoe UI',Roboto,Helvetica,Arial,sans-serif;}
```

Header: padding, border-bottom 1px rule. Label monospace uppercase letter-spacing. Title serif 28-32px. Meta line small.

Layout: `.layout{display:flex;gap:0;max-width:1200px;margin:0 auto;}` rail width 250px border-right; main flex:1 padding.

Tabs: `.tabs{display:flex;gap:2px;border-bottom:1px solid var(--rule)}` buttons monospace uppercase 12px letter-spacing, padding, border-bottom 2px transparent; active: color red, border-bottom red. role=tablist.

Tiles: grid 2x2 (or 4 across on wide). `.tiles{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:1px;background:var(--rule)}` each tile background paper padding. Big number serif 48px.

Tables: width 100%, border-collapse collapse; caption serif italic? caption text-align left, serif, padding. th monospace 11px uppercase letter-spacing, border-bottom 1px rule; td border-bottom 1px rule, padding 8px. Numbers right-aligned: `.num{text-align:right;font-variant-numeric:tabular-nums}`.

Row buttons: `.prow{cursor:pointer}` hover background slightly darker (#ece6d8). Detail row: background #efe9dc maybe; td colspan 4.

Fix mark: `.fix{outline:1px solid var(--red);outline-offset:1px;}` — thin red box around the space. Maybe background rgba red 0.08.

Chips/links: red for links? Links: color inherit with underline; accent for interactive. Keep links underlined ink; active tab red.

Focus: `:focus-visible{outline:2px solid var(--red);outline-offset:2px}`.

Buttons: `.btn{font:inherit;background:none;border:1px solid var(--ink);padding:6px 14px;cursor:pointer;border-radius:2px}` hover background ink color paper? Keep calm: border rule, hover border ink. Download buttons maybe solid ink. Keep simple: border 1px solid var(--ink).

Status dot: `.dot{display:inline-block;width:9px;height:9px;border-radius:50%;background:var(--green)}` red variant.

Bar in rail: `.bar{height:4px;background:var(--rule);position:relative}.bar>i{display:block;height:100%;background:var(--green)}.bar.bad>i{background:var(--red)}` width %.

Now, "No view shows more than about seven things to click" — tabs (4) + on tab 02: headings box button (1) + rows (not counted) = 5. Tab 03: rows clickable (not counted as they're table rows). Tab 04: 2 export buttons + elements heading = 3 + 4 tabs = 7. OK.

Left rail always visible with the big numbers — fine.

Now write the JS pipeline carefully.

```js
const D = window.WORKSHOP_DATA && window.WORKSHOP_DATA.html_doc;
```

If D missing → show error message. Handle gracefully.

```js
const ref = (D && D.reference) || null;
const symbol = D.symbol || '';
const docUrl = D.doc_url || '';
let parsed = null;
try { parsed = new DOMParser().parseFromString(D.html || '', 'text/html'); } catch(e){}
```

cleanText: `s.replace(/[ \t\n\r\f\v]+/g,' ').replace(/^ | $/g,'')` — trim ASCII only. Actually also trim leading/trailing: use `.replace(/^[ \t\n\r\f\v]+|[ \t\n\r\f\v]+$/g,'')`.

Block walk as above.

Classification & paragraph building:

```js
const els = []; // {el, tag, cls, text}
const firstTable = parsed ? parsed.body.querySelector('table') : null;
(function walk(node){
  if(!node) return;
  for (const el of Array.from(node.children)) {
    if (firstTable && el === firstTable) { els.push({el, cls:'cover'}); continue; }
    if (firstTable && firstTable.contains(el)) continue;
    const tag = el.tagName;
    if (!BLOCK.has(tag)) continue;
    els.push({el});
    if (el.children.length) walk(el);
  }
})(parsed ? parsed.body : null);
```

Hmm: `firstTable.contains(el)` — if el is a descendant of table we skip; but we never walk into table so this only matters if table nested elsewhere. Fine.

Wait, there's a subtle bug: if the first table is nested inside a div, walk(div) iterates children including table → handled by `el === firstTable`. Good.

Classify:

```js
let titleSeen = false;
const paragraphs = [];
const headings = [];
const items = []; // ordered for markdown: {kind:'title'|'h2'|'h3'|'p', ...}
let curPart = '', curSection = '';
const classCounts = {};
let unclassified = [];

for (const it of els) {
  const el = it.el, tag = el.tagName;
  const txt = clean(el.textContent || '');
  it.text = txt;
  if (it.cls === 'cover') { it.cls = 'cover'; }
  else if (tag === 'TABLE') it.cls = 'cover';
  else if (tag === 'DIV' || tag === 'SECTION' || tag === 'ARTICLE' || tag === 'MAIN') it.cls = 'container';
  else if (tag === 'H2') {
    if (!titleSeen) { titleSeen = true; it.cls = 'title'; items.push({kind:'title', text: txt}); }
    else {
      it.cls = 'heading';
      const h = splitHeading(txt);
      headings.push({tag:'H2', ...h});
      items.push({kind:'h2', ...h});
      if (h.label && /^[IVX]+$/.test(h.label)) curPart = h.display;
      curSection = h.display;
    }
  }
  else if (/^H[3-6]$/.test(tag)) {
    it.cls = 'heading';
    const h = splitHeading(txt);
    headings.push({tag, ...h});
    items.push({kind:'h3', ...h});
    curSection = h.display;
  }
  else if (tag === 'P') {
    const m = txt.match(/^(\d{1,3})\.\s*([\s\S]*)$/);
    if (m) {
      it.cls = 'paragraph';
      const num = parseInt(m[1], 10);
      const raw = clean(m[2]);
      const p = buildParagraph(num, raw, curPart, curSection);
      paragraphs.push(p);
      items.push({kind:'p', p});
    } else {
      it.cls = 'line';
    }
  }
  else it.cls = 'unclassified';
  classCounts[it.cls] = (classCounts[it.cls]||0)+1;
  if (it.cls === 'unclassified') unclassified.push(it);
}
```

splitHeading:

```js
function splitHeading(txt){
  const m = txt.match(/^([IVX]+|[A-Z])\.\s*([\s\S]+)$/);
  if (m) {
    const glued = new RegExp('^' + m[1].replace(/[.*+?^${}()|[\]\\]/g,'\\$&') + '\\.[^\\s]').test(txt);
    return {label: m[1], heading: clean(m[2]), display: m[1] + '. ' + clean(m[2]), glued};
  }
  return {label: null, heading: txt, display: txt, glued: false};
}
```

buildParagraph:

```js
function buildParagraph(num, raw, part, section){
  const log = [];
  let segs = [{t: raw, fix:false}];
  for (const rule of RULES) segs = applyRule(segs, rule, num, log);
  const text = segs.map(s=>s.t).join('');
  const html = segs.map(s=> s.fix ? '<span class="fix">'+esc(s.t)+'</span>' : esc(s.t)).join('');
  // first words
  let fw = null, fwFound = '', fwRef = '';
  const words = text.split(/\s+/).filter(Boolean).slice(0,6).join(' ');
  fwFound = words;
  if (ref && ref.first_words) {
    const key = String(num);
    if (Object.prototype.hasOwnProperty.call(ref.first_words, key)) {
      fwRef = ref.first_words[key];
      fw = norm(words) === norm(fwRef);
    } else { fw = null; fwRef = '(no reference entry)'; }
  }
  return {num, raw, text, html, log, part, section, fw, fwFound, fwRef, citation: symbol + ', para. ' + num};
}
```

RULES:

```js
const RULES = [
  {name:'sentence join', re:/([a-z])\.([A-Z])/g, split:m=>[m[1]+'.', m[2]]},
  {name:'comma join', re:/([a-z]),([A-Za-z])/g, split:m=>[m[1]+',', m[2]]},
  {name:'quote join', re:/([a-z])\u201C/g, split:m=>[m[1], '\u201C']},
  {name:'dash join', re:/\u2013([A-Za-z])/g, split:m=>['\u2013', m[1]]},
];
```

applyRule as sketched. Log entries: {para, rule, ctxBefore, match, pre, post, ctxAfter}.

Character counts:

```js
const CHARS = [
  {name:'en dash', cp:'U+2013', ch:'\u2013'},
  {name:'double quotes', cp:'U+201C / U+201D', chs:['\u201C','\u201D']},
  {name:'right single quote', cp:'U+2019', ch:'\u2019'},
  {name:'non-breaking hyphen', cp:'U+2011', ch:'\u2011'},
  {name:'non-breaking space', cp:'U+00A0', ch:'\u00A0'},
];
```

Count over paragraphs' text joined. Example: find index in some paragraph, context.

Checks:

```js
const checks = [];
// 1 paragraph count
if (ref && typeof ref.paragraphs === 'number') {
  checks.push({name:'Paragraph count', detail: paragraphs.length + ' found, ' + ref.paragraphs + ' expected', status: paragraphs.length === ref.paragraphs ? 'pass':'fail', tab: paragraphs.length!==ref.paragraphs?1:null});
} else checks.push({name:'Paragraph count', detail:'no reference in this file', status:'notrun'});
```

Hmm if ref missing, all ref-dependent checks 'notrun'. Numbering check doesn't need ref: check numbers are 1..N contiguous:

```js
let numOk = true; const numProblems = [];
paragraphs.forEach((p,i)=>{ if (p.num !== i+1) { numOk=false; numProblems.push('para. position '+(i+1)+' has number '+p.num); } });
```

Wait "Exactly 1 to n in order" — n here = found count? If ref says 90 and we found 90 numbered 1..90, fine. If found 88 numbered 1..88, numbering check passes (contiguous) but count check fails. I think numbering check = contiguous 1..N in order. Also duplicates: if numbers repeat, positions mismatch → captured. Good.

First words check: mismatches = paragraphs.filter(p=>p.fw===false). If ref missing → notrun. detail: `${mismatches.length} differ` + list "para. n: found "…" / reference "…"". Status pass if 0 mismatches (and ref present), fail otherwise, link tab 02 (index 1).

Footnotes: if ref && typeof ref.footnotes==='number': status 'limit', detail `0 in this HTML, ${ref.footnotes} in the document — the HTML version has no footnotes: a limit of the source, not of the app`. Else notrun.

Repairs: total insertions = sum log lengths; per rule counts; paragraphs affected count. status pass (informational) — it's a count, always "pass"? The plan lists it as a check: "n spaces restored in n paragraphs, counted per rule; every one is listed on tab 03". Status: pass (it ran). I'll mark 'pass' with detail.

Headings: h2 count (non-title), h3 count, glued count. pass.

Nothing lost: total = els.length; sum of classCounts values === total (always true by construction) — the real check: unclassified.length === 0 and every element has a class. Since I assign a class to every block element, sum always equals total; the meaningful part is unclassified list. status pass if unclassified empty else fail with list. detail: `${total} block elements, all classified (${classCounts breakdown})`.

Export round trip: build JSON string now, parse, compare length. status pass/fail.

Now render everything. I'll write render functions building HTML strings and setting innerHTML, with esc() for all data-derived text.

Tab 02 rows: for each paragraph:

```html
<tr class="prow" id="prow-N" data-n="N">
  <td class="num"><button class="rowbtn" aria-expanded="false" aria-controls="pdetail-N">N</button></td>
  <td>section</td>
  <td class="firstline">…</td>
  <td>OK / first words differ</td>
</tr>
<tr class="pdetail" id="pdetail-N" hidden><td colspan="4">...</td></tr>
```

Row click: attach one delegated listener on tbody: if closest('.prow') and not clicking the copy button → toggle. Button click also toggles (button inside row; row handler catches it). Careful: copy button inside detail row — detail row is separate tr, so no conflict.

Toggle: `btn.setAttribute('aria-expanded', open)`, detail.hidden = !open.

Detail content:

```html
<div class="path">IV. … › Right to work (art. 6)</div>
<p class="fulltext">html</p>
<p class="fw">first words: found "…" · reference "…" — match/differ</p>
<ul class="fixes">... or "no spaces repaired in this paragraph"</ul>
<button class="copybtn" data-cite="...">Copy citation</button> <span class="copied" hidden>Copied</span>
```

Copy handler: delegated on document: click .copybtn → copy text, show sibling .copied for 2s.

Tab 03 spaces table rows: log entries sorted by paragraph then order. Paragraph cell: `<button class="linkbtn" data-open-para="N">para. N</button>`. Click → openParagraph(N): showTab(1); expand row; scroll.

Characters table: rows with count and example (context with char wrapped in `<span class="ch">`).

Tab 04: checks list; export buttons; elements box.

Elements table: for each els item: Tag (lowercase), Classified as, Text first 80 chars (+ '…' if longer).

Header status: computed.

Rail: 

```
DOCUMENT (monospace label)
[card: symbol (mono, linked) / short title]
n  paragraphs of m   (big serif n, small "paragraphs of m")
[bar]
0  footnotes of m — not in this HTML (red)
n of m checks pass → (link to tab 04)
```

Plan: 'Two big serif numbers: "n paragraphs of reference.paragraphs" with a thin bar (red when short or over); "0 footnotes of reference.footnotes" in red, "not in this HTML". Then "n of m checks pass", linking to tab 04.' So big number n with caption "paragraphs of m". I'll render: `<div class="bignum">90</div><div class="bigcap">paragraphs of 90 expected</div><div class="bar">...` then `<div class="bignum red">0</div><div class="bigcap red">footnotes of 141 — not in this HTML</div>` then checks link.

If ref missing: "n paragraphs" / "no reference in this file".

Tabs markup:

```html
<div class="tabs" role="tablist" aria-label="Sections">
  <button role="tab" id="tab-0" aria-controls="panel-0" aria-selected="true">01 RESULT</button>
  ...
</div>
<section role="tabpanel" id="panel-0" aria-labelledby="tab-0">...</section>
```

Arrow keys on tablist: keydown handler; ArrowRight → next (wrap), ArrowLeft → prev; Home/End. Activate: click() or set selection + focus.

showTab(i): loop panels/tabs set hidden/aria-selected/tabindex.

Also "click = filter" hints — not needed here.

"How this is computed" line near every chart or number — tiles have it; rail numbers maybe small hint too. I'll add small mono hints.

Now, the "Spaces: n repaired or flagged" tile links to tab 03 — make the tile number a button/link that showTab(2). Similarly footnotes tile links to tab 03.

Edge: no paragraphs → tab 01 shows message; exports disabled (buttons disabled attr); tab 02 table shows "no paragraphs found". Handle.

Also handle D missing entirely: body shows a message.

Let me also double check the paragraph regex against committee line: "Committee on Economic, Social and Cultural Rights" — no leading digit. Cover table skipped. Title h2 "General comment No. 27 (2025) on ... *" — first h2 → title. Good.

One more: the h2 title ends with " *" — asterisk. In markdown export, title as `# ... *`. Fine.

Potential issue: `els` includes the div.content as 'container' — in "Elements found" table that's a row: div | container | text first 80. Fine.

Also the walk pushes elements in document order — but note: I push the element then descend, so parent before children. Good for "in order".

Wait, there's an issue with walk: `for (const el of node.children)` — children of body: table, div. div pushed, then walk(div) pushes its children (p, h2, ...). Good.

But inline elements inside p (like span in table only) — skipped since not block. But what about `<b>` inside p? Not block, skipped. Good.

Now the numbering regex on P text: what if a paragraph's textContent includes the number glued "1.A clean..." — match `/^(\d{1,3})\.\s*([\s\S]*)$/` — "1." then "A clean...". m[2] = "A clean...". Good. But what about "10.Something"? \d{1,3} matches "10". Good.

Hmm — careful: a P like "6 November 2025" (in cover table — skipped anyway). OK.

First-words normalization: also normalize multiple spaces? words joined with single space already.

Now the JSON export build:

```js
function buildJSON(){
  const recs = paragraphs.map(p => ({
    symbol: symbol,
    paragraph: p.num,
    section: p.section,
    part: p.part,
    text: p.text,
    text_raw: p.raw,
    first_words_match: p.fw,
    citation: p.citation,
    doc_url: docUrl,
    limitations: ref && typeof ref.footnotes==='number'
      ? 'no footnotes in this HTML version; the document has ' + ref.footnotes
      : 'no footnotes in this HTML version'
  }));
  return JSON.stringify(recs, null, 2);
}
```

Markdown:

```js
function buildMD(){
  const today = new Date().toISOString().slice(0,10);
  const lines = ['---'];
  lines.push('title: ' + mdEscape(D.title)); // quotes? just raw; if contains ':' problematic — keep simple, wrap in quotes
  ...
}
```

Front matter values with quotes: `title: "..."` — escape double quotes. I'll wrap string values in double quotes and escape `"` as `\"`. Numbers raw.

footnotes sentence: `This HTML version has 0 footnotes; the document has N.` or without N.

Body: iterate items: title → `# ` + text; h2 → `## ` + display; h3 → `### ` + display; p → `` `**${num}.** ${text}` `` — text may contain newlines? No, collapsed. But may contain markdown chars — fine, verbatim.

Blank lines between.

File name: `symbol.replace(/[^\w.-]+/g,'-')`? Plan: "the symbol with slashes replaced by hyphens" → `symbol.replace(/\//g,'-')`. "E/C.12/GC/27" → "E-C.12-GC-27.json". Good.

Now the header meta line: `symbol` linked to doc_url (new tab, target=_blank rel=noopener), "adopted " + ref.adopted, source. E.g. `<a href="...">E/C.12/GC/27</a> · adopted 6 November 2025 · OHCHR treaty body database (HTML)`. ref.adopted — sample says reference has `adopted`. Use `ref && ref.adopted ? 'adopted ' + ref.adopted : ''`.

Right side: dot + text + "1 source limit".

Let me now also compute "Spaces: n repaired or flagged" — n = total log entries. "flagged" might include first-words mismatches; I'll keep n = repairs count and the tile says "spaces repaired (tab 03)".

Now write the whole HTML. I'll be careful with escaping in template literals inside the script — the script is inline in HTML; avoid `</script>` sequences in strings. I'll use string concat where needed. Also avoid `<!--`. Fine.

Let me think about the CSS more concretely for a polished look:

```css
body{margin:0;background:#f4f0e8;color:#1d1b18;font:16px/1.55 system-ui,...}
header.top{padding:20px 28px 16px;border-bottom:1px solid #d9d2c3;display:flex;justify-content:space-between;gap:24px;align-items:flex-start;flex-wrap:wrap}
.kicker{font:11px/1.4 ui-monospace,Menlo,Consolas,monospace;letter-spacing:.14em;text-transform:uppercase;color:#6b6558}
h1{font-family:Georgia,'Times New Roman',serif;font-weight:400;font-size:30px;line-height:1.2;margin:6px 0 8px;max-width:60ch}
.meta{font-size:14px;color:#4a463d}
.meta a{color:inherit}
.status{text-align:right;font:12px ui-monospace,...;white-space:nowrap}
```

Layout:

```css
.layout{display:flex;max-width:1240px;margin:0 auto;align-items:stretch}
aside.rail{width:264px;flex:none;border-right:1px solid #d9d2c3;padding:20px 20px 28px}
main{flex:1;min-width:0;padding:20px 28px 40px}
```

Rail card: border 1px rule, padding 12px, background #efe9dc? Plan says thin rules instead of boxes... "a card with symbol in monospace and the short title" — I'll use a top rule + padding, no box: border-top 2px solid ink? Keep: `.doccard{border:1px solid #d9d2c3;padding:12px 14px}` — a card is fine, subtle. Actually "thin rules instead of boxes and shadows" — I'll use border 1px solid var(--rule), no shadow. OK.

Big numbers: `.bignum{font-family:Georgia,serif;font-size:52px;line-height:1}` caption mono 11px uppercase.

Tabs:

```css
.tabs{display:flex;gap:4px;border-bottom:1px solid #d9d2c3;flex-wrap:wrap}
.tabs [role=tab]{font:12px ui-monospace,...;letter-spacing:.12em;padding:10px 14px;background:none;border:none;border-bottom:2px solid transparent;cursor:pointer;color:#6b6558}
.tabs [role=tab][aria-selected=true]{color:#9b2335;border-bottom-color:#9b2335}
```

Panels: `section[role=tabpanel]{padding-top:20px}`.

Tiles:

```css
.tiles{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:1px;background:#d9d2c3;border:1px solid #d9d2c3}
.tile{background:#f4f0e8;padding:16px 18px}
.tile .n{font-family:Georgia,serif;font-size:48px;line-height:1.05}
.tile .cap{font:11px mono uppercase;letter-spacing:.12em;color:#6b6558;margin-top:2px}
.tile .how{font-size:12.5px;color:#4a463d;margin-top:10px;border-top:1px solid #d9d2c3;padding-top:8px}
```

Green/red text classes: `.ok{color:#1e6b3a}.bad{color:#9b2335}`.

Tables:

```css
table{width:100%;border-collapse:collapse;margin:10px 0 24px}
caption{caption-side:top;text-align:left;font-family:Georgia,serif;font-size:18px;padding:6px 0}
caption .tno{font:11px mono;letter-spacing:.12em;color:#6b6558;display:block;margin-bottom:2px}
th{font:11px mono uppercase;letter-spacing:.1em;text-align:left;color:#6b6558;border-bottom:1px solid #1d1b18;padding:6px 10px 6px 0;font-weight:400}
td{padding:8px 10px 8px 0;border-bottom:1px solid #d9d2c3;vertical-align:top}
td.num,th.num{text-align:right}
```

Row button: `.rowbtn{font:inherit;background:none;border:none;cursor:pointer;color:#9b2335;font-weight:600;padding:0;text-align:right;width:100%}` hmm number in red per plan ("Red accent on ... the paragraph numbers"). Yes paragraph numbers red.

prow hover: `tr.prow:hover{background:#ece5d6}` cursor pointer.

Detail row: `tr.pdetail td{background:#efe9db;padding:14px 18px}`.

fix span: `.fix{box-shadow:inset 0 0 0 1px #9b2335; background:rgba(155,35,53,.08); padding:0 1px;}` — thin red box. Use outline to avoid layout shift: `outline:1px solid #9b2335; outline-offset:1px;`.

Buttons: `.btn{font:13px ui-monospace...;letter-spacing:.08em;text-transform:uppercase;border:1px solid #1d1b18;background:none;padding:8px 16px;cursor:pointer}` hover: background #1d1b18 color #f4f0e8. Disabled: opacity .4 cursor default.

linkbtn (inline text button): `.linkbtn{background:none;border:none;padding:0;font:inherit;color:#9b2335;cursor:pointer;text-decoration:underline}`.

Closed headings (details toggles): `.toggle{...}` similar to tab style: mono uppercase with count, aria-expanded, with a "+" indicator? Use `▸`/`▾`? Keep text: "HEADINGS FOUND: 30" with aria-expanded; add `::after` content based on aria-expanded: `[aria-expanded=false]::after{content:" +"}` `[aria-expanded=true]::after{content:" –"}`. Nice.

Check panel: list of lines: `.check{display:flex;gap:10px;padding:8px 0;border-bottom:1px solid #d9d2c3;font-size:14.5px}` status word mono uppercase colored width fixed.

Footer: border-top, mono small, padding.

Now, the tab-03 "clicking a row opens the paragraph on tab 02" — implement openPara(n).

Also tile links: spaces tile → tab 03 (index 2), footnotes tile → tab 03.

Let me now also handle "If reference or one of its fields is missing, the tiles say 'no reference in this file' and the checks that need it show 'not run'". Implemented.

"If html yields no <p>, tab 01 says so and the exports are disabled." Implemented: if paragraphs.length===0 → tab01 message + disable buttons.

Now let me write out the code fully. I need to be careful about size — probably ~700-900 lines. Fine.

Let me draft the script structure:

```js
(function(){
'use strict';
var D = (window.WORKSHOP_DATA && window.WORKSHOP_DATA.html_doc) || null;
... 
})();
```

I'll use modern JS (const/let, arrow) — fine.

esc function:

```js
function esc(s){return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');}
```

Now full render. I'll build the static skeleton in HTML with containers, then JS fills:

- #kicker, #title, #meta, #status
- rail: #railcard, #railnums
- tabs static (4 buttons), panels: #panel-0..3 with inner containers filled by JS.

Let me write the code.

```js
const BLOCK = new Set(['P','H1','H2','H3','H4','H5','H6','DIV','TABLE','UL','OL','LI','BLOCKQUOTE','PRE','SECTION','ARTICLE','MAIN','FIGURE','ASIDE','HEADER','FOOTER','HR','DL','DT','DD','ADDRESS','FORM','FIELDSET']);
```

Hmm HEADER inside body? The html string is just body content; fine.

Wait — careful: if the parsed body has a `<header>`? Not in this doc. OK.

One concern: `doc.body.querySelector('table')` — the first table. In sample, body > table. Good.

Now, the walk pushes `el` for block tags; but note the div.content contains h2/p — walk descends. But also: what if there are nested divs? handled.

Edge: `parsed.body` might be null if html empty → guard.

Now compute everything, then render.

Rendering tab 02 table: 90 rows; each row's firstline computed. Detail rows built lazily? Build all upfront is fine (90 details with full text ~ maybe 100KB HTML — fine).

Actually to keep DOM lighter, build detail content lazily on first expand. Simpler: build all; 90 paragraphs × ~250 words ≈ 160KB text — acceptable. But innerHTML with all details might be heavy-ish; still fine. I'll build lazily to be safe: detail row exists with empty td; on first open, fill. Let me do lazy: store p objects; on toggle open, if not filled, fill innerHTML of td.

Delegated events:

```js
tbody.addEventListener('click', function(e){
  const copy = e.target.closest('.copybtn');
  if (copy) { doCopy(copy); return; }
  const row = e.target.closest('tr.prow');
  if (row) toggleRow(row);
});
```

toggleRow(row): const n = row.dataset.n; const btn = row.querySelector('.rowbtn'); const det = document.getElementById('pdetail-'+n); const open = btn.getAttribute('aria-expanded')==='true'; btn.setAttribute('aria-expanded', String(!open)); det.hidden = open; if(!open && !det.dataset.filled){ fillDetail(det, n); det.dataset.filled='1'; }

Keyboard: button handles Enter/Space natively (click). Row click via mouse. Good.

Copy:

```js
function doCopy(btn){
  const cite = btn.getAttribute('data-cite');
  const done = function(){ const s = btn.parentElement.querySelector('.copied'); if(s){ s.hidden=false; setTimeout(function(){s.hidden=true;},2000);} };
  if (navigator.clipboard && navigator.clipboard.writeText) { navigator.clipboard.writeText(cite).then(done, function(){ fallbackCopy(cite); done(); }); }
  else { fallbackCopy(cite); done(); }
}
function fallbackCopy(t){ const ta=document.createElement('textarea'); ta.value=t; ta.style.position='fixed'; ta.style.opacity='0'; document.body.appendChild(ta); ta.select(); try{document.execCommand('copy');}catch(e){} ta.remove(); }
```

Tabs:

```js
const tabs = Array.from(document.querySelectorAll('[role=tab]'));
const panels = tabs.map(t=>document.getElementById(t.getAttribute('aria-controls')));
function showTab(i, focus){
  tabs.forEach((t,j)=>{ const on = i===j; t.setAttribute('aria-selected', String(on)); t.tabIndex = on?0:-1; panels[j].hidden = !on; });
  if (focus) tabs[i].focus();
}
tabs.forEach((t,i)=>{
  t.addEventListener('click', function(){ showTab(i,false); });
  t.addEventListener('keydown', function(e){
    let j = null;
    if (e.key==='ArrowRight') j=(i+1)%tabs.length;
    else if (e.key==='ArrowLeft') j=(i-1+tabs.length)%tabs.length;
    else if (e.key==='Home') j=0;
    else if (e.key==='End') j=tabs.length-1;
    if (j!==null){ e.preventDefault(); showTab(j,true); }
  });
});
```

openPara(n): showTab(1,false); then find row, expand, fill, scrollIntoView({block:'center'}).

Tab 03 log rows: build from all paragraphs' logs in order (paragraphs in order, logs in order). Each entry: para, rule, ctxBefore, match, pre, post, ctxAfter.

Before cell: esc(ctxBefore + match + ctxAfter); After cell: esc(ctxBefore+pre) + '<span class="fix"> </span>' + esc(post+ctxAfter).

Rule counts line: counts per rule name.

Characters: compute counts over allText = paragraphs.map(p=>p.text).join('\n'). For each char spec, count occurrences (for double quotes sum of both). Example: find first paragraph containing, idx = p.text.indexOf(ch), ctx = p.text.slice(max(0,idx-25), idx) + span + slice(idx+1, idx+26). Build HTML.

Checks render into #checks.

Elements table into #elements.

Export buttons wired.

Header/rail render.

Now, "n of m checks pass" in header and rail: compute passes/fails/limits/notrun among checks. m = pass+fail. Text: failures? `${failures} check${failures>1?'s':''} failed` red : (passes>0 ? `${passes} of ${passes+failures} checks pass` green : 'checks not run'). Plus limits: ` · ${limits} source limit${limits>1?'s':''}`.

Rail checks link: `<button class="linkbtn" data-goto="3">n of m checks pass</button>` — handle clicks on [data-goto].

Also tiles with links: spaces tile number wrapped in button data-goto="2"; footnotes tile data-goto="2".

Global click handler for [data-goto]: showTab(parseInt).

Now tab 01 tiles content:

Tile 1: 
```
<div class="n ok">90</div>
<div class="cap">paragraphs found · the document has 90</div>
<div class="how">How this is computed: ...</div>
```
If mismatch: n red, cap "paragraphs found · the document has 92 (difference −2)". diff = found - expected; show sign.

Tile 2: `<div class="n">84 of 90</div>` cap "first words match the reference". If ref missing: n "—" cap "no reference in this file".

Tile 3: `<div class="n bad">0 of 141</div>` cap "footnotes in this HTML — see tab 03" (button). how: "This HTML version has no footnote text and no footnote marks; the count is a limit of the source, not of the app."

Tile 4: `<div class="n">35</div>` cap "spaces repaired — listed on tab 03" (button). how: "Four rules insert a space only where the characters prove one was there; text_raw keeps the text as found."

If no ref: tiles 1-3 say "no reference in this file" in cap; tile 4 still works (repairs don't need ref). Tile 1: n = found, cap "paragraphs found · no reference in this file".

If paragraphs empty: panel-0 shows a message div: "No numbered paragraphs were found in this HTML." plus tiles maybe hidden. I'll show message and still show tiles with 0s? Plan: "tab 01 says so and the exports are disabled". I'll show a notice line above tiles and tiles with zeros; exports disabled.

Tab 02 headings box: button.toggle aria-expanded=false aria-controls="headingsbox" text `HEADINGS FOUND: ${headings.length}`; box hidden with list: each heading: `<li><span class="mono">H2</span> IV. Introduction ${glued?'<span class="bad">glued label</span>':''}</li>`. Hmm keep simple: display text + tag. Also note title h2 counted separately? "Headings found: n" — count h2(non-title)+h3. I'll also mention title separately in elements table.

Table caption: `${paragraphs.length} paragraphs found, ${ref?ref.paragraphs:'?'} expected` + TAB.02.

Columns: No. | Section | First line | Check. Section cell: esc(p.section || '—'). Check cell: p.fw===false ? '<span class="bad">first words differ</span>' : (p.fw===true ? '<span class="ok">OK</span>' : 'no reference').

Detail fill:

```js
function fillDetail(det, n){
  const p = byNum[n];
  const path = (p.part ? p.part + ' › ' : '') + (p.section || '—');
  let h = '<div class="path mono">' + esc(path) + '</div>';
  h += '<p class="full">' + p.html + '</p>';
  // first words
  if (p.fw === true) h += '<p class="fwline"><span class="ok">first words match</span> the reference: “' + esc(p.fwFound) + '”</p>';
  else if (p.fw === false) h += '<p class="fwline"><span class="bad">first words differ</span> — found “' + esc(p.fwFound) + '” / reference “' + esc(p.fwRef) + '”</p>';
  else h += '<p class="fwline">no reference entry for this paragraph</p>';
  // repairs
  if (p.log.length) {
    h += '<ul class="fixlist">';
    for (const l of p.log) h += '<li>' + esc(l.rule) + ': “' + esc(l.ctxBefore + l.match + l.ctxAfter) + '” → “' + esc(l.ctxBefore + l.pre + ' ' + l.post + l.ctxAfter) + '”</li>';
    h += '</ul>';
  } else h += '<p class="fwline">no spaces repaired in this paragraph; the raw text is shown above.</p>';
  h += '<p class="citeRow"><button class="btn copybtn" data-cite="' + esc(p.citation) + '">Copy citation</button> <span class="copied mono" hidden>Copied</span> <span class="mono cite">' + esc(p.citation) + '</span></p>';
  det.firstElementChild.innerHTML = h;
}
```

Wait — the full text shown should be the repaired text with marks (p.html). Also maybe show raw when different: add line "as found in the HTML (raw): ..." if log.length. I'll add: if log.length, add `<details>`? Keep simple: add a line with raw text in smaller font: `<p class="raw">as found: “…”</p>`. Hmm might be long. The plan says text_raw is in export; expanded row shows "the places repaired or flagged in this paragraph" — the fixlist covers it. I'll skip raw in the row to avoid clutter, but the fixlist shows before/after contexts. Actually showing raw full text could help "verbatim" — but the repaired text IS what they'd quote; raw is as-found. The plan: "the full text, verbatim, never shortened" — I'll show repaired text (marked). Good enough; plus fixlist.

Hmm, actually maybe show raw too when repairs exist, in a smaller muted line, since honesty matters: "text_raw (as found in the HTML) differs in n places". I'll include a collapsed raw line only when log.length: `<p class="rawline">as found in the HTML: ` + esc(p.raw) + `</p>` — could be 253 words; acceptable inside expanded row. I'll include it; it's the verbatim source. OK include.

Tab 03 blocks:

Block 1:
```html
<h3 class="blocktitle">Lost: footnotes <span class="count">141</span></h3>
<p>The document has 141 footnotes. This HTML has 0: no footnote text, no footnote marks, and the note the title's asterisk points to is missing. To cite a footnote, use the PDF or Word version.</p>
```
Count = ref.footnotes or '—'. If no ref: "no reference in this file".

Block 2:
```html
<h3>Changed: spaces <span class="count">35</span></h3>
<p class="mono hint">sentence join: 23 · comma join: 8 · quote join: 2 · dash join: 2 — click a row to open the paragraph on tab 02</p>
<table>... Paragraph | Before | After | Rule ...</table>
<p>Rules restore a space only where the characters prove it was there. Word pairs such as “Giventhe” are not touched; the first-words check catches them only in a paragraph's first six words.</p>
```

Block 3:
```html
<h3>Changed: characters</h3>
<p class="mono hint">on a keyboard: a hyphen and straight quotes</p>
<table>Character | Count | Example</table>
<p>Kept exactly as published, in the table and in every export. A search for “business-related” typed with the hyphen key will not find “business‑related”: normalise the text before searching it.</p>
```

Note: in that sentence, use the actual U+2011 char in "business‑related" — I'll write it with the literal char. In my code I can use '\u2011' via JS or literal. I'll write literal in HTML — risky to type; better generate via JS or use &nbsp;? I'll construct that sentence in JS with '\u2011'. Or just write "business-related" with the actual char — I can include the unicode char directly in the file. I'll use JS string with \u2011 to be safe. Actually simpler: put the note text in HTML with a placeholder and replace? I'll just build tab 03 content in JS entirely, using '\u2011' escapes. Hmm, mixing. Let me build all dynamic panels in JS anyway (they depend on data), so I can use escapes freely.

Actually the static HTML will have empty containers; JS fills panels 0-3, header, rail, footer bits. That's cleanest.

Tab 04:

```html
<h3 class="blocktitle">Checks</h3>
<div id="checks"></div>
<h3 class="blocktitle">Export</h3>
<p class="hint mono">the JSON is parsed back on build; its record count equals the table's (check above)</p>
<button id="dljson" class="btn">Download JSON</button> <button id="dlmd" class="btn">Download Markdown</button>
<p class="mono small">files: E-C.12-GC-27.json · E-C.12-GC-27.md — UTF-8, Blob download</p>
<button class="toggle" aria-expanded="false" aria-controls="elsbox">ELEMENTS FOUND: n</button>
<div id="elsbox" hidden><table>Tag | Classified as | Text (first 80 characters)</table></div>
```

Check line format: `<div class="check"><span class="st ok">pass</span><span class="cname">Paragraph count</span><span class="cdetail">90 found, 90 expected</span></div>` with optional link button "tab 02".

Status words: pass (green), check failed (red), source limit (red), not run (grey).

Now header status dot: `<span class="dot ok"></span> 8 of 8 checks pass · 1 source limit`.

Rail: 

```html
<div class="railhead mono">DOCUMENT</div>
<div class="doccard">
  <div class="mono sym"><a href=doc_url>E/C.12/GC/27</a></div>
  <div class="short">General comment No. 27 (2025)</div>
</div>
<div class="bignum">90</div>
<div class="bigcap mono">paragraphs of 90 expected</div>
<div class="bar"><i style="width:100%"></i></div>
<div class="bignum bad">0</div>
<div class="bigcap mono bad">footnotes of 141 — not in this HTML</div>
<button class="linkbtn" data-goto="3">8 of 8 checks pass</button>
```

Bar: width = min(100, found/expected*100)%; class bad if found!==expected.

Short title derivation: `D.title.split(/\s+on\s+/)[0]` — "General comment No. 27 (2025) on economic..." → "General comment No. 27 (2025)". If no ' on ', full title. Good.

Footer: `<footer>source · built · Done by this page's code; no model was called and nothing left the browser. Credits: ...</footer>`. built: D.built may not exist — I'll write `D.built ? ' · built ' + D.built : ''`. Hmm the plan footer says "source, built" — html_doc description doesn't include built but maybe it does in real data. I'll conditionally include.

Credits line: "Credits: method after The Turing Way, “Documentation and metadata” (CC BY 4.0); check design after UK Government Analysis Function, “Quality assurance of code for analysis and research: Testing code”; citation format after Dag Hammarskjöld Library, Ask DAG."

Now — one more detail: "Every row that shows a document has its symbol, linked to doc_url in a new tab." Header + rail card link. Good.

Let me also add the "How this is computed" for rail numbers? Plan doesn't require; tiles have it. Add small hint on rail: "counted by this page's code" maybe. Keep minimal.

Now write everything. Also remember: `[hidden]{display:none!important}` in CSS.

Potential pitfall: setting innerHTML with p.html containing spans — fine.

Another pitfall: `text.split(/\s+/)` — \s matches \u00A0, so nbsp splits words — fine for first words.

norm function also should collapse? Compare norm(found) vs norm(ref) — both are 6-word strings joined with single space; ref may have different spacing? ref first_words like "A clean, healthy and sustainable environment" — normal. OK.

Let me also handle `ref.first_words` values possibly containing curly quotes — norm handles.

Now, the numbering check detail: list problems like "position 5 has number 7 (gap/duplicate)". I'll produce: if numbers not contiguous: `numbers run ${first}–${last} with gaps/duplicates: position i → number n`. Keep simple: list up to all mismatches: "para. at position i is numbered n".

Also check "Paragraph count" link to tab 02 when fail.

Export round trip check: build JSON string once at startup (store), parse, compare. Also store for download.

Now, about performance: fine.

Let me now also decide tab labels: `01 RESULT`, `02 PARAGRAPHS`, `03 LOST & CHANGED`, `04 CHECKS & EXPORT`. Use `&amp;` in HTML.

Write the final file. I'll aim for clean, complete code.

One more consideration: the plan says tab 02 has "A closed 'Headings found: n' box above the table". Implement as toggle button + hidden div with list.

Also "Details open in place (a clicked row expands)" — done via detail row.

Let me write the HTML now.

Also: title of app in header — serif `title` from D.title.

Header label: "UN DOCUMENT · HTML".

Let me write:

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Paragraphs of a UN General Comment — HTML extraction</title>
<style> ... </style>
</head>
<body>
<header class="top">
  <div class="hleft">
    <div class="kicker" id="kicker">UN DOCUMENT · HTML</div>
    <h1 id="doctitle"></h1>
    <div class="meta" id="docmeta"></div>
  </div>
  <div class="status" id="status"></div>
</header>
<div class="layout">
  <aside class="rail" id="rail"></aside>
  <main>
    <div class="tabs" role="tablist" aria-label="App sections">
      <button role="tab" id="tab-0" aria-controls="panel-0" aria-selected="true">01 RESULT</button>
      <button role="tab" id="tab-1" aria-controls="panel-1" aria-selected="false" tabindex="-1">02 PARAGRAPHS</button>
      <button role="tab" id="tab-2" aria-controls="panel-2" aria-selected="false" tabindex="-1">03 LOST &amp; CHANGED</button>
      <button role="tab" id="tab-3" aria-controls="panel-3" aria-selected="false" tabindex="-1">04 CHECKS &amp; EXPORT</button>
    </div>
    <section role="tabpanel" id="panel-0" aria-labelledby="tab-0"></section>
    <section role="tabpanel" id="panel-1" aria-labelledby="tab-1" hidden></section>
    <section role="tabpanel" id="panel-2" aria-labelledby="tab-2" hidden></section>
    <section role="tabpanel" id="panel-3" aria-labelledby="tab-3" hidden></section>
  </main>
</div>
<footer id="foot"></footer>
<script> ... </script>
</body>
</html>
```

CSS details — write carefully.

Now the script. Let me write it fully in my head/draft:

```js
(function(){
'use strict';
var D = (window.WORKSHOP_DATA && window.WORKSHOP_DATA.html_doc) || null;

function esc(s){return String(s==null?'':s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');}
function clean(s){return String(s==null?'':s).replace(/[ \t\n\r\f\v]+/g,' ').replace(/^ | $/g,'');}
function norm(s){return String(s).replace(/[\u2018\u2019]/g,"'").replace(/[\u201C\u201D]/g,'"').replace(/[\u2013\u2014\u2011]/g,'-').replace(/\u00A0/g,' ');}

if(!D){ document.body.innerHTML = '<p style="padding:24px">No WORKSHOP_DATA.html_doc in this page.</p>'; return; }

var ref = D.reference || null;
var symbol = D.symbol || '';
var docUrl = D.doc_url || '';
var source = D.source || '';

var parsed = null;
try { parsed = new DOMParser().parseFromString(D.html || '', 'text/html'); } catch(e) { parsed = null; }
var body = parsed ? parsed.body : null;

var BLOCK = {'P':1,'H1':1,'H2':1,'H3':1,'H4':1,'H5':1,'H6':1,'DIV':1,'TABLE':1,'UL':1,'OL':1,'LI':1,'BLOCKQUOTE':1,'PRE':1,'SECTION':1,'ARTICLE':1,'MAIN':1,'FIGURE':1,'ASIDE':1,'DL':1,'DT':1,'DD':1,'FORM':1,'FIELDSET':1,'ADDRESS':1,'HR':1};
var firstTable = body ? body.querySelector('table') : null;
var els = [];
(function walk(node){
  if(!node) return;
  var kids = node.children;
  for(var i=0;i<kids.length;i++){
    var el = kids[i];
    if(firstTable && el===firstTable){ els.push({el:el, cls:'cover'}); continue; }
    if(firstTable && firstTable.contains(el)) continue;
    if(!BLOCK[el.tagName]) continue;
    els.push({el:el});
    if(el.children.length) walk(el);
  }
})(body);
```

Wait: `firstTable.contains(el)` — el is a direct child being examined; if firstTable is an ancestor of el (e.g. table nested in div), contains works. But if el IS firstTable handled above. OK.

Hmm, but there's a subtle issue: if firstTable is nested inside a div, when we walk the div's children we hit the table → push cover, don't descend. Good.

Classification:

```js
function splitHeading(txt){
  var m = txt.match(/^([IVX]+|[A-Z])\.\s*([\s\S]+)$/);
  if(m){
    var escLabel = m[1].replace(/[.*+?^${}()|[\]\\]/g,'\\$&');
    var glued = new RegExp('^'+escLabel+'\\.[^\\s]').test(txt);
    return {label:m[1], heading:clean(m[2]), display:m[1]+'. '+clean(m[2]), glued:glued};
  }
  return {label:null, heading:txt, display:txt, glued:false};
}

var RULES = [
  {name:'sentence join', re:/([a-z])\.([A-Z])/g, split:function(m){return [m[1]+'.', m[2]];}},
  {name:'comma join', re:/([a-z]),([A-Za-z])/g, split:function(m){return [m[1]+',', m[2]];}},
  {name:'quote join', re:/([a-z])\u201C/g, split:function(m){return [m[1],'\u201C'];}},
  {name:'dash join', re:/\u2013([A-Za-z])/g, split:function(m){return ['\u2013', m[1]];}}
];

function applyRule(segs, rule, paraNum, log){
  var out = [];
  for(var s=0;s<segs.length;s++){
    var seg = segs[s];
    if(seg.fix){ out.push(seg); continue; }
    var t = seg.t, last = 0, m;
    rule.re.lastIndex = 0;
    while((m = rule.re.exec(t)) !== null){
      var parts = rule.split(m);
      var ctxB = t.slice(Math.max(0, m.index-20), m.index);
      var ctxA = t.slice(m.index + m[0].length, m.index + m[0].length + 20);
      out.push({t: t.slice(last, m.index) + parts[0], fix:false});
      out.push({t:' ', fix:true});
      out.push({t: parts[1], fix:false});
      log.push({para:paraNum, rule:rule.name, ctxBefore:ctxB, match:m[0], pre:parts[0], post:parts[1], ctxAfter:ctxA});
      last = m.index + m[0].length;
      if(m[0].length===0) rule.re.lastIndex++;
    }
    out.push({t: t.slice(last), fix:false});
  }
  return out;
}
```

Wait — bug: after pushing segments for a match, subsequent matches in the same segment: `last` updated; the trailing push uses t.slice(last). But the pushed pieces include parts[1] which is part of the match — correct. However, the regex continues scanning the ORIGINAL t (exec on t), so overlapping matches fine. But note: after inserting a space, could the same rule match again across the inserted space? E.g. sentence rule on "a.B.C"? "a.B" matches → "a. B", then exec continues from index after "a.B" in original t → ".C" — needs [a-z] before '.', the char before '.' in original is 'B' (uppercase) — no match. Fine.

But one issue: comma rule `/([a-z]),([A-Za-z])/g` on "land,wetlands" → "land, wetlands". Good.

Quote rule: "crises“increase" → m[1]='s', post='“' → "crises “increase". Good.

Dash: "challenges –to" → '–' + 't' → "– to". Good.

Paragraph build:

```js
var paragraphs = [], headings = [], items = [], classCounts = {}, unclassified = [];
var curPart = '', curSection = '', titleSeen = false;

function buildParagraph(num, raw, part, section){
  var log = [];
  var segs = [{t:raw, fix:false}];
  for(var r=0;r<RULES.length;r++) segs = applyRule(segs, RULES[r], num, log);
  var text = segs.map(function(s){return s.t;}).join('');
  var html = segs.map(function(s){return s.fix ? '<span class="fix">'+esc(s.t)+'</span>' : esc(s.t);}).join('');
  var words = text.split(/\s+/).filter(Boolean).slice(0,6).join(' ');
  var fw = null, fwRef = '';
  if(ref && ref.first_words){
    var key = String(num);
    if(Object.prototype.hasOwnProperty.call(ref.first_words, key)){
      fwRef = ref.first_words[key];
      fw = norm(words) === norm(fwRef);
    }
  }
  return {num:num, raw:raw, text:text, html:html, log:log, part:part, section:section,
          fw:fw, fwFound:words, fwRef:fwRef, citation: symbol + ', para. ' + num};
}

for(var i=0;i<els.length;i++){
  var it = els[i], el = it.el, tag = el.tagName;
  var txt = clean(el.textContent || '');
  it.text = txt;
  if(it.cls === 'cover'){ /* stays cover */ }
  else if(tag === 'TABLE') it.cls = 'cover';
  else if(tag==='DIV'||tag==='SECTION'||tag==='ARTICLE'||tag==='MAIN'||tag==='ASIDE'||tag==='FIGURE') it.cls = 'container';
  else if(tag === 'H2'){
    if(!titleSeen){ titleSeen = true; it.cls = 'title'; items.push({kind:'title', text:txt}); }
    else {
      it.cls = 'heading';
      var h = splitHeading(txt);
      h.tag = 'H2';
      headings.push(h);
      items.push({kind:'h2', h:h});
      if(h.label && /^[IVX]+$/.test(h.label)) curPart = h.display;
      curSection = h.display;
    }
  }
  else if(/^H[3-6]$/.test(tag)){
    it.cls = 'heading';
    var h2 = splitHeading(txt); h2.tag = tag;
    headings.push(h2);
    items.push({kind:'h3', h:h2});
    curSection = h2.display;
  }
  else if(tag === 'P'){
    var m = txt.match(/^(\d{1,3})\.\s*([\s\S]*)$/);
    if(m){
      it.cls = 'paragraph';
      var p = buildParagraph(parseInt(m[1],10), clean(m[2]), curPart, curSection);
      paragraphs.push(p);
      items.push({kind:'p', p:p});
    } else it.cls = 'line';
  }
  else it.cls = 'unclassified';
  classCounts[it.cls] = (classCounts[it.cls]||0)+1;
  if(it.cls==='unclassified') unclassified.push(it);
}
```

Wait — issue: the paragraph regex on a P like "1.A clean..." — but what about the committee bold p "Committee on Economic, Social and Cultural Rights"? no leading digit → 'line'. Good.

Hmm — but careful: the title h2 is inside div.content; the first h2 encountered in els order is the title. Good.

Character counts:

```js
var allText = paragraphs.map(function(p){return p.text;}).join('\n');
var CHARS = [
  {name:'en dash', cp:'U+2013', ch:'\u2013'},
  {name:'double quotes', cp:'U+201C / U+201D', chs:['\u201C','\u201D']},
  {name:'right single quote', cp:'U+2019', ch:'\u2019'},
  {name:'non-breaking hyphen', cp:'U+2011', ch:'\u2011'},
  {name:'non-breaking space', cp:'U+00A0', ch:'\u00A0'}
];
CHARS.forEach(function(c){
  var list = c.chs || [c.ch];
  c.count = 0; c.example = '';
  for(var i=0;i<paragraphs.length && !c.example;i++){
    var t = paragraphs[i].text;
    for(var k=0;k<list.length;k++){
      var idx = t.indexOf(list[k]);
      while(idx !== -1){
        c.count++;
        if(!c.example){
          var b = t.slice(Math.max(0,idx-25), idx);
          var a = t.slice(idx+1, idx+26);
          c.example = esc(b) + '<span class="ch">'+esc(list[k])+'</span>' + esc(a);
          c.examplePara = paragraphs[i].num;
        }
        idx = t.indexOf(list[k], idx+1);
      }
    }
  }
});
```

Hmm — count should count all occurrences across all paragraphs, but example from first found. The loop above breaks example search after first but continues counting? The `!c.example` guard only stops example capture; counting continues for all paragraphs since loop condition `i<paragraphs.length && !c.example` — oops, that stops the whole loop once example found. Fix: separate loops:

```js
CHARS.forEach(function(c){
  var list = c.chs || [c.ch];
  c.count = 0; c.example = '';
  for(var i=0;i<paragraphs.length;i++){
    var t = paragraphs[i].text;
    for(var k=0;k<list.length;k++){
      var idx = t.indexOf(list[k]);
      while(idx !== -1){
        c.count++;
        if(!c.example){
          var b = t.slice(Math.max(0,idx-25), idx);
          var a = t.slice(idx+1, idx+26);
          c.example = esc(b) + '<span class="ch">'+esc(list[k])+'</span>' + esc(a);
        }
        idx = t.indexOf(list[k], idx+1);
      }
    }
  }
});
```

For nbsp example, the char is invisible — show as `<span class="ch">⍽</span>`? Better: for nbsp display '·' in the highlight: I'll special-case: display char = ch === '\u00A0' ? '·' : ch. And in the Character column show name + cp + code with actual char (nbsp in code element renders as space — show '␣'? I'll show the char plus name; for nbsp use '⍽' symbol? Keep: `<code> </code>` looks empty. I'll render character cell as: name (e.g. "non-breaking space") + mono cp + `<code>` + (ch==='\u00A0'?'⍽':ch) + `</code>`. Hmm ⍽ is "squared n"? There's '␣' (U+2423 open box) commonly used for space. I'll use '␣' for nbsp and '·' maybe. Use '␣'. For non-breaking hyphen U+2011 the char itself is visible-ish (looks like hyphen) — fine, plus name clarifies.

Repairs totals:

```js
var allLogs = [];
paragraphs.forEach(function(p){ p.log.forEach(function(l){ allLogs.push(l); }); });
var ruleCounts = {};
allLogs.forEach(function(l){ ruleCounts[l.rule] = (ruleCounts[l.rule]||0)+1; });
var repairParas = paragraphs.filter(function(p){return p.log.length>0;}).length;
```

First words mismatches:

```js
var fwMismatch = paragraphs.filter(function(p){return p.fw===false;});
```

Checks:

```js
var checks = [];
function addCheck(name, detail, status, tabIdx){ checks.push({name:name, detail:detail, status:status, tab:tabIdx==null?null:tabIdx}); }

if(ref && typeof ref.paragraphs==='number'){
  addCheck('Paragraph count', paragraphs.length + ' found, ' + ref.paragraphs + ' expected', paragraphs.length===ref.paragraphs?'pass':'fail', 1);
} else addCheck('Paragraph count', 'no reference in this file', 'notrun');

var numProblems = [];
paragraphs.forEach(function(p,i){ if(p.num !== i+1) numProblems.push('position '+(i+1)+' is numbered '+p.num); });
addCheck('Numbering', numProblems.length ? 'not 1–n in order: '+numProblems.join('; ') : 'numbers run 1–'+paragraphs.length+' in order, no gaps or duplicates', numProblems.length?'fail':'pass', numProblems.length?1:null);

if(ref && ref.first_words){
  addCheck('First words', fwMismatch.length===0 ? 'all '+paragraphs.length+' paragraphs match reference.first_words' : fwMismatch.length+' differ: '+fwMismatch.map(function(p){return 'para. '+p.num+' found \u201C'+p.fwFound+'\u201D / reference \u201C'+p.fwRef+'\u201D';}).join('; '), fwMismatch.length?'fail':'pass', fwMismatch.length?1:null);
} else addCheck('First words', 'no reference in this file', 'notrun');

if(ref && typeof ref.footnotes==='number'){
  addCheck('Footnotes', '0 in this HTML, '+ref.footnotes+' in the document \u2014 the HTML version has no footnotes: a limit of the source, not of the app', 'limit');
} else addCheck('Footnotes', 'no reference in this file', 'notrun');

addCheck('Repairs', allLogs.length+' spaces restored in '+repairParas+' paragraphs ('+RULES.map(function(r){return r.name+': '+(ruleCounts[r.name]||0);}).join(', ')+'); every one is listed on tab 03 and text_raw keeps the text as found', 'pass', 2);

var h2n = headings.filter(function(h){return h.tag==='H2';}).length;
var h3n = headings.length - h2n;
var gluedN = headings.filter(function(h){return h.glued;}).length;
addCheck('Headings', (h2n+h3n)+' headings found ('+h2n+' H2, '+h3n+' H3), '+gluedN+' glued labels separated', 'pass', 1);

var totalEls = els.length;
var sum = 0; for(var k in classCounts) sum += classCounts[k];
var breakdown = Object.keys(classCounts).sort().map(function(k){return k+': '+classCounts[k];}).join(', ');
addCheck('Nothing lost', totalEls+' block elements, all classified exactly once ('+breakdown+')'+(unclassified.length?'; UNCLASSIFIED: '+unclassified.map(function(u){return u.el.tagName;}).join(', '):''), (sum===totalEls && unclassified.length===0)?'pass':'fail');
```

Export round trip:

```js
var jsonStr = buildJSON();
var rtOk = false, rtDetail = '';
try { rtOk = JSON.parse(jsonStr).length === paragraphs.length; rtDetail = 'JSON parsed back: '+JSON.parse(jsonStr).length+' records = '+paragraphs.length+' table rows'; }
catch(e){ rtDetail = 'JSON parse failed: '+e.message; }
addCheck('Export round trip', rtDetail, rtOk?'pass':'fail');
```

buildJSON defined before checks. Order: define buildJSON/buildMD before checks.

Status summary:

```js
var nPass = checks.filter(c=>c.status==='pass').length;
var nFail = checks.filter(c=>c.status==='fail').length;
var nLimit = checks.filter(c=>c.status==='limit').length;
var nNotRun = checks.filter(c=>c.status==='notrun').length;
var m = nPass + nFail;
var statusText, statusCls;
if(nFail>0){ statusText = nFail+' check'+(nFail>1?'s':'')+' failed'; statusCls='bad'; }
else if(nPass>0){ statusText = nPass+' of '+m+' checks pass'; statusCls='ok'; }
else { statusText = 'checks not run'; statusCls=''; }
if(nLimit>0) statusText += ' · '+nLimit+' source limit'+(nLimit>1?'s':'');
```

Rendering functions... then wire events.

Render header:

```js
document.getElementById('doctitle').textContent = D.title || '(untitled)';
var meta = '';
if(symbol){ meta += '<a href="'+esc(docUrl)+'" target="_blank" rel="noopener">'+esc(symbol)+'</a>'; }
if(ref && ref.adopted) meta += (meta?' · ':'') + 'adopted ' + esc(ref.adopted);
if(source) meta += (meta?' · ':'') + esc(source);
document.getElementById('docmeta').innerHTML = meta;
document.getElementById('status').innerHTML = '<span class="dot '+statusCls+'"></span> '+esc(statusText);
```

dot class: ok → green, bad → red, '' → grey. CSS: `.dot{...background:#8a8375}.dot.ok{background:#1e6b3a}.dot.bad{background:#9b2335}`.

Rail:

```js
var shortTitle = (D.title||'').split(/\s+on\s+/)[0] || D.title || '';
var rail = '';
rail += '<div class="railhead">DOCUMENT</div>';
rail += '<div class="doccard"><div class="sym"><a href="'+esc(docUrl)+'" target="_blank" rel="noopener">'+esc(symbol)+'</a></div><div class="short">'+esc(shortTitle)+'</div></div>';
var exp = (ref && typeof ref.paragraphs==='number') ? ref.paragraphs : null;
rail += '<div class="bignum'+(exp!=null && paragraphs.length!==exp?' bad':'')+'">'+paragraphs.length+'</div>';
rail += '<div class="bigcap">paragraphs'+(exp!=null?' of '+exp+' expected':'')+'</div>';
if(exp!=null){
  var pct = Math.max(0, Math.min(100, Math.round(paragraphs.length/exp*100)));
  rail += '<div class="bar'+(paragraphs.length!==exp?' bad':'')+'"><i style="width:'+pct+'%"></i></div>';
}
var fexp = (ref && typeof ref.footnotes==='number') ? ref.footnotes : null;
rail += '<div class="bignum bad">0</div>';
rail += '<div class="bigcap bad">footnotes'+(fexp!=null?' of '+fexp:'')+' — not in this HTML</div>';
rail += '<button class="linkbtn" data-goto="3">'+esc(nFail>0? nFail+' checks failed' : (nPass>0? nPass+' of '+m+' checks pass':'checks not run'))+'</button>';
rail += '<p class="railnote">counted by this page\u2019s code over the parsed HTML</p>';
document.getElementById('rail').innerHTML = rail;
```

Panel 0 (tiles):

```js
var p0 = '';
if(paragraphs.length===0) p0 += '<p class="notice">No numbered paragraphs were found in this HTML: no &lt;p&gt; starts with a number and a full stop. The exports on tab 04 are disabled.</p>';
p0 += '<div class="tiles">';
// tile 1
var t1cap, t1cls='';
if(exp!=null){
  var diff = paragraphs.length - exp;
  t1cap = 'paragraphs found · the document has '+exp+(diff!==0?' (difference '+(diff>0?'+':'')+diff+')':'');
  t1cls = diff===0?'ok':'bad';
} else { t1cap = 'paragraphs found · no reference in this file'; }
p0 += '<div class="tile"><div class="n '+t1cls+'">'+paragraphs.length+'</div><div class="cap">'+esc(t1cap)+'</div><div class="how">How this is computed: &lt;p&gt; elements whose text starts with a number and a full stop, counted in document order by this page\u2019s code.</div></div>';
// tile 2
if(ref && ref.first_words){
  var fwTotal = paragraphs.length, fwOk = paragraphs.filter(p=>p.fw===true).length;
  p0 += '<div class="tile"><div class="n">'+fwOk+' of '+fwTotal+'</div><div class="cap">first words match the reference</div><div class="how">How this is computed: the first six words of each paragraph against reference.first_words, after normalising curly quotes, dashes and non-breaking spaces; case is kept.</div></div>';
} else {
  p0 += '<div class="tile"><div class="n">—</div><div class="cap">no reference in this file</div><div class="how">The reference yardstick is missing, so this check is not run — never reported as pass.</div></div>';
}
// tile 3
if(fexp!=null){
  p0 += '<div class="tile"><div class="n bad">0 of '+fexp+'</div><div class="cap"><button class="linkbtn" data-goto="2">footnotes in this HTML — see tab 03</button></div><div class="how">How this is computed: this HTML version contains no footnote text and no footnote marks; the count is a limit of the source, not of the app.</div></div>';
} else {
  p0 += '<div class="tile"><div class="n bad">0</div><div class="cap">footnotes in this HTML · no reference in this file</div><div class="how">This HTML version contains no footnote text and no footnote marks.</div></div>';
}
// tile 4
p0 += '<div class="tile"><div class="n">'+allLogs.length+'</div><div class="cap"><button class="linkbtn" data-goto="2">spaces repaired — listed on tab 03</button></div><div class="how">How this is computed: four rules insert a space only where the characters prove one was there; every insertion is logged and text_raw keeps the text as found.</div></div>';
p0 += '</div>';
document.getElementById('panel-0').innerHTML = p0;
```

Panel 1 (paragraphs):

```js
var p1 = '';
p1 += '<button class="toggle" aria-expanded="false" aria-controls="hbox">HEADINGS FOUND: '+headings.length+'</button>';
p1 += '<div id="hbox" hidden><ul class="hlist">';
headings.forEach(function(h){
  p1 += '<li><span class="htag">'+h.tag+'</span> '+esc(h.display)+(h.glued?' <span class="bad mono">glued label separated</span>':'')+'</li>';
});
p1 += '</ul><p class="hint">The first &lt;h2&gt; is the document title; every other heading is listed here so none can hide inside a paragraph.</p></div>';
p1 += '<table><caption><span class="tno">TAB.02</span>'+paragraphs.length+' paragraphs found'+(exp!=null?', '+exp+' expected':'')+'</caption>';
p1 += '<thead><tr><th class="num" scope="col">No.</th><th scope="col">Section</th><th scope="col">First line</th><th scope="col">Check</th></tr></thead><tbody id="ptbody">';
paragraphs.forEach(function(p){
  var fl = p.text.length>120 ? p.text.slice(0,120).replace(/\s+\S*$/,'')+'…' : p.text;
  p1 += '<tr class="prow" data-n="'+p.num+'"><td class="num"><button class="rowbtn" aria-expanded="false" aria-controls="pdetail-'+p.num+'">'+p.num+'</button></td><td>'+esc(p.section||'—')+'</td><td class="fl">'+esc(fl)+'</td><td>'+(p.fw===false?'<span class="bad">first words differ</span>':(p.fw===true?'<span class="ok">OK</span>':'<span class="mut">no reference</span>'))+'</td></tr>';
  p1 += '<tr class="pdetail" id="pdetail-'+p.num+'" hidden><td colspan="4"></td></tr>';
});
p1 += '</tbody></table>';
document.getElementById('panel-1').innerHTML = p1;
```

Wait: firstline cut — `p.text.slice(0,120).replace(/\s+\S*$/,'')` removes trailing partial word; if no space in slice, replace does nothing → could cut mid-word; add fallback: if result length < 100 maybe fine. Acceptable. Actually if the slice has no space, `\s+\S*$` won't match, leaving a mid-word cut. Add: if no match, keep slice + '…'. It's fine either way; I'll do: `var s = p.text.slice(0,120); var cut = s.replace(/\s+\S*$/,' '); fl = (cut.trim().length < s.length ? cut.trim() : s) + '…'` — hmm overcomplicating. Simple: `var s=p.text.slice(0,120); var sp=s.lastIndexOf(' '); fl=(sp>60? s.slice(0,sp) : s)+'…';` Good.

Panel 2 (lost & changed):

```js
var p2 = '';
// block 1
p2 += '<h3 class="btitle">Lost: footnotes <span class="cnt">'+(fexp!=null?fexp:'—')+'</span></h3>';
p2 += '<p>The document has '+(fexp!=null?fexp:'an unknown number of')+' footnotes. This HTML has 0: no footnote text, no footnote marks, and the note the title\u2019s asterisk points to is missing. To cite a footnote, use the PDF or Word version.</p>';
// block 2
p2 += '<h3 class="btitle">Changed: spaces <span class="cnt">'+allLogs.length+'</span></h3>';
p2 += '<p class="hint">'+RULES.map(function(r){return esc(r.name)+': '+(ruleCounts[r.name]||0);}).join(' · ')+' — click a row to open the paragraph on tab 02</p>';
p2 += '<table><caption><span class="tno">TAB.03</span>'+allLogs.length+' spaces restored in '+repairParas+' paragraphs</caption>';
p2 += '<thead><tr><th scope="col">Paragraph</th><th scope="col">Before</th><th scope="col">After</th><th scope="col">Rule</th></tr></thead><tbody>';
allLogs.forEach(function(l){
  p2 += '<tr><td><button class="linkbtn" data-openpara="'+l.para+'">para. '+l.para+'</button></td><td class="mono-ish">'+esc(l.ctxBefore+l.match+l.ctxAfter)+'</td><td>'+esc(l.ctxBefore+l.pre)+'<span class="fix"> </span>'+esc(l.post+l.ctxAfter)+'</td><td>'+esc(l.rule)+'</td></tr>';
});
p2 += '</tbody></table>';
p2 += '<p>Rules restore a space only where the characters prove it was there. Word pairs such as \u201CGiventhe\u201D are not touched; the first-words check catches them only in a paragraph\u2019s first six words.</p>';
// block 3
p2 += '<h3 class="btitle">Changed: characters</h3>';
p2 += '<p class="hint">on a keyboard: a hyphen and straight quotes</p>';
p2 += '<table><caption><span class="tno">TAB.03</span>characters kept exactly as published, counted over all paragraph texts</caption>';
p2 += '<thead><tr><th scope="col">Character</th><th class="num" scope="col">Count</th><th scope="col">Example</th></tr></thead><tbody>';
CHARS.forEach(function(c){
  var disp = (c.ch==='\u00A0') ? '\u2423' : (c.chs? '\u201C\u201D' : c.ch);
  p2 += '<tr><td>'+esc(c.name)+' <span class="mono cp">'+esc(c.cp)+'</span> <code>'+esc(disp)+'</code></td><td class="num">'+c.count+'</td><td class="ex">'+c.example+'</td></tr>';
});
p2 += '</tbody></table>';
p2 += '<p>Kept exactly as published, in the table and in every export. A search for \u201Cbusiness-related\u201D typed with the hyphen key will not find \u201Cbusiness\u2011related\u201D: normalise the text before searching it.</p>';
document.getElementById('panel-2').innerHTML = p2;
```

Panel 3 (checks & export):

```js
var p3 = '';
p3 += '<h3 class="btitle">Checks — every check on one line</h3>';
p3 += '<div class="checks">';
checks.forEach(function(c){
  var st = c.status==='pass' ? '<span class="st ok">pass</span>' : c.status==='fail' ? '<span class="st bad">check failed</span>' : c.status==='limit' ? '<span class="st bad">source limit</span>' : '<span class="st mut">not run</span>';
  p3 += '<div class="check">'+st+'<span class="cname">'+esc(c.name)+'</span><span class="cdetail">'+esc(c.detail)+(c.tab!=null?' <button class="linkbtn" data-goto="'+c.tab+'">tab 0'+(c.tab+1)+'</button>':'')+'</span></div>';
});
p3 += '</div>';
p3 += '<h3 class="btitle">Export</h3>';
p3 += '<p><button class="btn" id="dljson"'+(paragraphs.length===0?' disabled':'')+'>Download JSON</button> <button class="btn" id="dlmd"'+(paragraphs.length===0?' disabled':'')+'>Download Markdown</button></p>';
p3 += '<p class="hint">files: '+esc(fileBase)+'.json and '+esc(fileBase)+'.md — UTF-8, downloaded as a Blob; the JSON is parsed back on build and its record count equals the table\u2019s (check above).</p>';
p3 += '<button class="toggle" aria-expanded="false" aria-controls="elsbox">ELEMENTS FOUND: '+els.length+'</button>';
p3 += '<div id="elsbox" hidden><table><caption><span class="tno">TAB.04</span>every block element in document order, classified exactly once</caption>';
p3 += '<thead><tr><th scope="col">Tag</th><th scope="col">Classified as</th><th scope="col">Text (first 80 characters)</th></tr></thead><tbody>';
els.forEach(function(it){
  var t = it.text || '';
  var short = t.length>80 ? t.slice(0,80)+'…' : t;
  p3 += '<tr><td class="mono">&lt;'+it.el.tagName.toLowerCase()+'&gt;</td><td>'+esc(it.cls)+'</td><td>'+esc(short)+'</td></tr>';
});
p3 += '</tbody></table></div>';
document.getElementById('panel-3').innerHTML = p3;
```

fileBase = symbol.replace(/\//g,'-').

buildJSON / buildMD:

```js
function buildJSON(){
  var recs = paragraphs.map(function(p){
    return {
      symbol: symbol,
      paragraph: p.num,
      section: p.section,
      part: p.part,
      text: p.text,
      text_raw: p.raw,
      first_words_match: p.fw,
      citation: p.citation,
      doc_url: docUrl,
      limitations: (ref && typeof ref.footnotes==='number') ? 'no footnotes in this HTML version; the document has '+ref.footnotes : 'no footnotes in this HTML version'
    };
  });
  return JSON.stringify(recs, null, 2);
}
function mdVal(s){ return '"' + String(s).replace(/\\/g,'\\\\').replace(/"/g,'\\"') + '"'; }
function buildMD(){
  var today = new Date().toISOString().slice(0,10);
  var L = [];
  L.push('---');
  L.push('title: '+mdVal(D.title||''));
  L.push('symbol: '+mdVal(symbol));
  if(ref && ref.adopted) L.push('adopted: '+mdVal(ref.adopted));
  L.push('source_url: '+mdVal(docUrl));
  L.push('extracted: '+today);
  L.push('paragraphs_found: '+paragraphs.length);
  L.push('paragraphs_expected: '+(exp!=null?exp:'null'));
  L.push('footnotes: '+mdVal('This HTML version has 0 footnotes'+(fexp!=null?'; the document has '+fexp:'')+'.'));
  L.push('---');
  L.push('');
  items.forEach(function(it){
    if(it.kind==='title'){ L.push('# '+it.text); L.push(''); }
    else if(it.kind==='h2'){ L.push('## '+it.h.display); L.push(''); }
    else if(it.kind==='h3'){ L.push('### '+it.h.display); L.push(''); }
    else if(it.kind==='p'){ L.push('**'+it.p.num+'.** '+it.p.text); L.push(''); }
  });
  return L.join('\n');
}
```

Note: `exp` and `fexp` are defined in rail section — I need them defined before buildMD used in checks (export round trip uses buildJSON only). Order in script: compute exp/fexp early. Let me define `var exp = ...; var fexp = ...;` right after ref.

Downloads:

```js
document.getElementById('dljson').addEventListener('click', function(){
  download(fileBase+'.json', buildJSON(), 'application/json');
});
document.getElementById('dlmd').addEventListener('click', function(){
  download(fileBase+'.md', buildMD(), 'text/markdown');
});
function download(name, content, type){
  var blob = new Blob([content], {type: type+';charset=utf-8'});
  var url = URL.createObjectURL(blob);
  var a = document.createElement('a');
  a.href = url; a.download = name;
  document.body.appendChild(a); a.click();
  setTimeout(function(){ URL.revokeObjectURL(url); a.remove(); }, 200);
}
```

Toggles (generic):

```js
document.addEventListener('click', function(e){
  var tg = e.target.closest('.toggle');
  if(tg){
    var box = document.getElementById(tg.getAttribute('aria-controls'));
    var open = tg.getAttribute('aria-expanded')==='true';
    tg.setAttribute('aria-expanded', String(!open));
    if(box) box.hidden = open;
    return;
  }
  var g = e.target.closest('[data-goto]');
  if(g){ showTab(parseInt(g.getAttribute('data-goto'),10), false); return; }
  var op = e.target.closest('[data-openpara]');
  if(op){ openPara(parseInt(op.getAttribute('data-openpara'),10)); return; }
  var cp = e.target.closest('.copybtn');
  if(cp){ doCopy(cp); return; }
  var row = e.target.closest('tr.prow');
  if(row){ toggleRow(row); }
});
```

Careful: copybtn is inside detail row (tr.pdetail), not prow — fine. But the row click handler: clicking the rowbtn inside prow triggers both row handler (closest tr.prow) — fine, single toggle. But also the button click might bubble... only one handler. OK.

But wait: data-goto buttons inside panels — handled. The toggle for headings box is in panel-1. OK.

toggleRow:

```js
function toggleRow(row){
  var n = row.getAttribute('data-n');
  var btn = row.querySelector('.rowbtn');
  var det = document.getElementById('pdetail-'+n);
  var open = btn.getAttribute('aria-expanded')==='true';
  btn.setAttribute('aria-expanded', String(!open));
  det.hidden = open;
  if(!open && !det.getAttribute('data-filled')){
    fillDetail(det, n);
    det.setAttribute('data-filled','1');
  }
}
function openPara(n){
  showTab(1, false);
  var row = document.querySelector('tr.prow[data-n="'+n+'"]');
  if(!row) return;
  var btn = row.querySelector('.rowbtn');
  if(btn.getAttribute('aria-expanded')!=='true') toggleRow(row);
  row.scrollIntoView({block:'center'});
}
```

fillDetail as sketched. byNum map: `var byNum = {}; paragraphs.forEach(p=>byNum[p.num]=p);`

doCopy as sketched.

Tabs wiring as sketched.

Footer:

```js
var foot = esc(source||'');
if(D.built) foot += ' · built ' + esc(D.built);
foot += ' · Done by this page\u2019s code; no model was called and nothing left the browser.';
document.getElementById('foot').innerHTML = '<div>'+foot+'</div><div class="credits">Credits: export metadata after The Turing Way, \u201CDocumentation and metadata\u201D (CC BY 4.0); check design after UK Government Analysis Function, \u201CQuality assurance of code for analysis and research: Testing code\u201D; citation format after Dag Hammarskj\u00F6ld Library, Ask DAG.</div>';
```

Hmm — the footer source: D.source. Also header meta includes source. Fine.

Now CSS full:

```css
:root{--paper:#f4f0e8;--ink:#1d1b18;--rule:#d9d2c3;--red:#9b2335;--green:#1e6b3a;--mut:#6b6558;}
*{box-sizing:border-box}
[hidden]{display:none!important}
html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--paper);color:var(--ink);font:16px/1.55 system-ui,-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
.mono,.kicker,.cap,.hint,.tno,.htag,.cp,.st,.cname,.sym,.railhead,.bigcap,.toggle,.tabs [role=tab],.btn,.linkbtn{font-family:ui-monospace,Menlo,Consolas,"Liberation Mono",monospace}
a{color:inherit}
:focus-visible{outline:2px solid var(--red);outline-offset:2px}
header.top{display:flex;justify-content:space-between;gap:24px;flex-wrap:wrap;padding:22px 30px 16px;border-bottom:1px solid var(--rule);max-width:1280px;margin:0 auto}
.kicker{font-size:11px;letter-spacing:.16em;text-transform:uppercase;color:var(--mut)}
h1{font-family:Georgia,"Times New Roman",serif;font-weight:400;font-size:29px;line-height:1.22;margin:8px 0 8px;max-width:62ch}
.meta{font-size:14px;color:#45413a}
.status{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:12px;letter-spacing:.06em;white-space:nowrap;padding-top:6px}
.dot{display:inline-block;width:9px;height:9px;border-radius:50%;background:#8a8375;margin-right:6px;vertical-align:1px}
.dot.ok{background:var(--green)}.dot.bad{background:var(--red)}
.layout{display:flex;max-width:1280px;margin:0 auto;align-items:stretch}
aside.rail{width:270px;flex:none;border-right:1px solid var(--rule);padding:22px 22px 32px}
main{flex:1;min-width:0;padding:18px 30px 48px}
.railhead{font-size:11px;letter-spacing:.16em;color:var(--mut);margin-bottom:10px}
.doccard{border:1px solid var(--rule);padding:12px 14px;margin-bottom:26px}
.sym{font-size:12px;letter-spacing:.04em}
.sym a{text-decoration:none;border-bottom:1px solid var(--rule)}
.short{font-size:13.5px;margin-top:6px;color:#45413a}
.bignum{font-family:Georgia,"Times New Roman",serif;font-size:54px;line-height:1;margin-top:18px}
.bignum.bad{color:var(--red)}
.bigcap{font-size:11px;letter-spacing:.1em;text-transform:uppercase;color:var(--mut);margin-top:4px}
.bigcap.bad{color:var(--red)}
.bar{height:4px;background:var(--rule);margin-top:8px}
.bar i{display:block;height:100%;background:var(--green)}
.bar.bad i{background:var(--red)}
.railnote{font-size:12px;color:var(--mut);margin-top:22px}
.linkbtn{background:none;border:none;padding:0;font-size:inherit;color:var(--red);cursor:pointer;text-decoration:underline;text-underline-offset:2px}
.tabs{display:flex;gap:2px;border-bottom:1px solid var(--rule);flex-wrap:wrap}
.tabs [role=tab]{font-size:12px;letter-spacing:.12em;padding:10px 14px 9px;background:none;border:none;border-bottom:2px solid transparent;cursor:pointer;color:var(--mut)}
.tabs [role=tab]:hover{color:var(--ink)}
.tabs [role=tab][aria-selected=true]{color:var(--red);border-bottom-color:var(--red)}
section[role=tabpanel]{padding-top:22px}
.tiles{display:grid;grid-template-columns:repeat(auto-fit,minmax(235px,1fr));gap:1px;background:var(--rule);border:1px solid var(--rule)}
.tile{background:var(--paper);padding:16px 18px 14px}
.tile .n{font-family:Georgia,"Times New Roman",serif;font-size:46px;line-height:1.05}
.tile .n.ok{color:var(--green)}.tile .n.bad{color:var(--red)}
.cap{font-size:11px;letter-spacing:.1em;text-transform:uppercase;color:var(--mut);margin-top:4px}
.how{font-size:12.5px;line-height:1.45;color:#45413a;margin-top:10px;border-top:1px solid var(--rule);padding-top:8px}
.notice{border:1px solid var(--red);color:var(--red);padding:10px 14px;margin-bottom:16px;font-size:14.5px}
.btitle{font-family:Georgia,"Times New Roman",serif;font-weight:400;font-size:21px;margin:26px 0 8px}
.btitle .cnt{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:13px;color:var(--red);margin-left:8px;letter-spacing:.06em}
.hint{font-size:11.5px;letter-spacing:.04em;color:var(--mut);margin:4px 0 10px}
table{width:100%;border-collapse:collapse;margin:8px 0 26px}
caption{caption-side:top;text-align:left;font-family:Georgia,"Times New Roman",serif;font-size:18px;padding:4px 0 8px}
.tno{display:block;font-family:ui-monospace,Menlo,Consolas,monospace;font-size:11px;letter-spacing:.14em;color:var(--mut);margin-bottom:2px}
th{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:11px;letter-spacing:.1em;text-transform:uppercase;font-weight:400;text-align:left;color:var(--mut);border-bottom:1px solid var(--ink);padding:6px 12px 6px 0}
td{padding:8px 12px 8px 0;border-bottom:1px solid var(--rule);vertical-align:top;font-size:15px}
th.num,td.num{text-align:right;font-variant-numeric:tabular-nums}
tr.prow{cursor:pointer}
tr.prow:hover{background:#ece5d5}
.rowbtn{background:none;border:none;padding:0;font:inherit;font-weight:600;color:var(--red);cursor:pointer;text-align:right;width:100%}
tr.pdetail td{background:#efe9da;padding:14px 18px}
.fl{color:#45413a}
.ok{color:var(--green)}.bad{color:var(--red)}.mut{color:var(--mut)}
.fix{outline:1px solid var(--red);outline-offset:1px;background:rgba(155,35,53,.07)}
.ch{outline:1px solid var(--red);outline-offset:1px;background:rgba(155,35,53,.07)}
.path{font-size:11.5px;letter-spacing:.08em;text-transform:uppercase;color:var(--mut);margin-bottom:8px}
.full{margin:0 0 10px;font-size:15.5px}
.fwline{font-size:13.5px;margin:6px 0}
.fixlist{margin:6px 0 10px;padding-left:18px;font-size:13.5px}
.rawline{font-size:13px;color:var(--mut);border-top:1px solid var(--rule);padding-top:8px;margin-top:10px}
.citeRow{margin-top:12px;display:flex;gap:10px;align-items:center;flex-wrap:wrap}
.cite{font-size:12px;color:var(--mut)}
.copied{font-size:11px;letter-spacing:.1em;text-transform:uppercase;color:var(--green)}
.btn{font-size:12px;letter-spacing:.1em;text-transform:uppercase;border:1px solid var(--ink);background:none;color:var(--ink);padding:9px 16px;cursor:pointer}
.btn:hover:not(:disabled){background:var(--ink);color:var(--paper)}
.btn:disabled{opacity:.4;cursor:default}
.toggle{display:block;background:none;border:none;border-bottom:1px solid var(--rule);width:100%;text-align:left;font-size:12px;letter-spacing:.12em;text-transform:uppercase;color:var(--ink);padding:10px 0;cursor:pointer;margin-top:18px}
.toggle::after{content:" +";color:var(--red)}
.toggle[aria-expanded=true]::after{content:" \2013";color:var(--red)}
.hlist{margin:10px 0 18px;padding-left:0;list-style:none}
.hlist li{padding:5px 0;border-bottom:1px solid var(--rule);font-size:14.5px}
.htag{font-size:10.5px;letter-spacing:.1em;color:var(--mut);border:1px solid var(--rule);padding:1px 5px;margin-right:8px}
.checks{border-top:1px solid var(--rule)}
.check{display:flex;gap:12px;align-items:baseline;padding:9px 0;border-bottom:1px solid var(--rule);font-size:14.5px}
.st{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:11px;letter-spacing:.1em;text-transform:uppercase;flex:none;width:96px}
.cname{font-weight:600;flex:none}
.cdetail{color:#45413a}
.ex{font-size:13.5px}
code{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:13px;background:#ece5d5;padding:0 3px}
.cp{font-size:10.5px;color:var(--mut);margin:0 4px}
footer{border-top:1px solid var(--rule);max-width:1280px;margin:0 auto;padding:16px 30px 30px;font-size:13px;color:#45413a}
.credits{font-size:11.5px;color:var(--mut);margin-top:6px}
@media (max-width:900px){.layout{flex-direction:column}aside.rail{width:auto;border-right:none;border-bottom:1px solid var(--rule)}}
```

Wait: `.mono` class defined in group selector but I use classes like `cp`, `st` etc. — I listed them in the font-family group. Also `.hint` uses mono? I set `.hint` font-size but family — add to group. Let me just define a utility: `.mono{font-family:ui-monospace,...}` and add mono class where needed, plus explicit families for kicker etc. Simplify: define

```css
.kicker,.cap,.hint,.tno,.htag,.cp,.st,.cname,.sym,.railhead,.bigcap,.toggle,.tabs [role=tab],.btn,.status,.path,.copied,.cite,.rowbtn? 
```

rowbtn should be sans bold red — keep sans. Let me finalize in code.

Also `.mono-ish` I used in tab03 before cell — replace with a class `.ctx{font-size:13px}` maybe with mono? Before/After contexts in mono 12.5px could be nice: class "ctx". I'll add `.ctx{font-family:ui-monospace,...;font-size:12.5px}`.

Now, one thing: tab labels contain `&` → `03 LOST &amp; CHANGED`.

Also the plan wants tab names like `01 RESULT · 02 PARAGRAPHS · ...` — I'll use "01 RESULT" etc. with the number and name; fine.

Check "at most five tabs" — 4. Good.

Now assemble the script in order:

1. helpers, D, ref, symbol, docUrl, source, exp, fexp
2. parse, walk, classify, paragraphs, headings, items, classCounts
3. CHARS counts
4. logs, ruleCounts
5. fwMismatch
6. buildJSON, buildMD (need items, paragraphs, exp, fexp, fileBase)
7. checks (uses buildJSON)
8. status summary
9. render header, rail, panels
10. events (tabs, delegated clicks, downloads)
11. footer

fileBase = symbol.replace(/\//g,'-').

One more: the plan says header right shows "n of m checks pass" or "n checks failed", then "1 source limit". My statusText includes limits appended — good.

Also rail "n of m checks pass, linking to tab 04" — done via data-goto=3.

Potential issue: `e.target.closest` — e.target may be a text node? In click events target is element. OK. But if e.target is not an Element (e.g., document)? closest exists on Element; clicks always target elements. Fine. Guard: `var t = e.target instanceof Element ? e.target : null; if(!t) return;`.

Also the rowbtn click: clicking button inside prow → closest('tr.prow') found → toggleRow. But also button default behavior fine.

But careful: clicking copybtn inside pdetail — pdetail is a tr but not .prow, so row handler won't fire; copybtn handled earlier. Order in handler: toggle, data-goto, data-openpara, copybtn, prow. The copybtn check must come before prow check — it does, and pdetail isn't prow anyway.

Also clicking linkbtn data-goto inside a check line — fine.

Now fillDetail:

```js
function fillDetail(det, n){
  var p = byNum[n];
  if(!p) return;
  var path = (p.part ? p.part + ' \u203A ' : '') + (p.section || '(no heading above)');
  var h = '<div class="path">'+esc(path)+'</div>';
  h += '<p class="full">'+p.html+'</p>';
  if(p.fw===true) h += '<p class="fwline"><span class="ok">first words match</span> the reference: \u201C'+esc(p.fwFound)+'\u201D</p>';
  else if(p.fw===false) h += '<p class="fwline"><span class="bad">first words differ</span> — found \u201C'+esc(p.fwFound)+'\u201D / reference \u201C'+esc(p.fwRef)+'\u201D</p>';
  else h += '<p class="fwline mut">no reference entry for this paragraph</p>';
  if(p.log.length){
    h += '<ul class="fixlist">';
    p.log.forEach(function(l){
      h += '<li>'+esc(l.rule)+': \u201C'+esc(l.ctxBefore+l.match+l.ctxAfter)+'\u201D \u2192 \u201C'+esc(l.ctxBefore+l.pre+' '+l.post+l.ctxAfter)+'\u201D</li>';
    });
    h += '</ul>';
    h += '<p class="rawline">as found in the HTML (text_raw): '+esc(p.raw)+'</p>';
  } else {
    h += '<p class="fwline mut">no spaces repaired in this paragraph</p>';
  }
  h += '<p class="citeRow"><button class="btn copybtn" data-cite="'+esc(p.citation)+'">Copy citation</button><span class="copied" hidden>Copied</span><span class="cite">'+esc(p.citation)+'</span></p>';
  det.firstElementChild.innerHTML = h;
}
```

doCopy:

```js
function doCopy(btn){
  var cite = btn.getAttribute('data-cite');
  var row = btn.closest('.citeRow');
  var done = function(){ var s = row ? row.querySelector('.copied') : null; if(s){ s.hidden=false; setTimeout(function(){ s.hidden=true; }, 2000); } };
  var fallback = function(){ var ta=document.createElement('textarea'); ta.value=cite; ta.setAttribute('readonly',''); ta.style.position='fixed'; ta.style.opacity='0'; document.body.appendChild(ta); ta.select(); try{ document.execCommand('copy'); }catch(err){} document.body.removeChild(ta); };
  if(navigator.clipboard && navigator.clipboard.writeText){ navigator.clipboard.writeText(cite).then(done, function(){ fallback(); done(); }); }
  else { fallback(); done(); }
}
```

Tabs:

```js
var tabs = Array.prototype.slice.call(document.querySelectorAll('.tabs [role=tab]'));
var panels = tabs.map(function(t){ return document.getElementById(t.getAttribute('aria-controls')); });
function showTab(i, focus){
  tabs.forEach(function(t,j){
    var on = (i===j);
    t.setAttribute('aria-selected', on?'true':'false');
    t.tabIndex = on?0:-1;
    panels[j].hidden = !on;
  });
  if(focus) tabs[i].focus();
}
tabs.forEach(function(t,i){
  t.addEventListener('click', function(){ showTab(i,false); });
  t.addEventListener('keydown', function(e){
    var j=null;
    if(e.key==='ArrowRight') j=(i+1)%tabs.length;
    else if(e.key==='ArrowLeft') j=(i-1+tabs.length)%tabs.length;
    else if(e.key==='Home') j=0;
    else if(e.key==='End') j=tabs.length-1;
    if(j!==null){ e.preventDefault(); showTab(j,true); }
  });
});
```

Note: panels[j].hidden — panels are sections; initial hidden attribute set in HTML for 1..3.

Edge: if D missing → early return before wiring; but the early return replaces body — fine.

Also handle `body` null (html empty): els empty, paragraphs empty → tab01 notice, exports disabled. Good.

Now double-check the classification of the sample: body children: table (cover), div.content (container) → walk div: children: p (bold committee) → 'line'; h2 (title) → 'title'; h2 "I.Introduction" → heading, label I, glued (I. followed by 'I' non-space) → glued true; curPart = "I. Introduction"; h3s...; 90 p's → paragraphs. 

Wait — the h2 title: "General comment No. 27 (2025) on economic, social and cultural rights andthe environmental dimension of sustainable development *" — first h2 → title. Good.

But hold on: is the committee `<p>` before the title h2 inside div.content? Sample: `<div class="content"><p style="font-weight:bold...">Committee on...</p><h2>General comment...</h2><h2>I.Introduction</h2><p>1.A clean...` Yes.

Paragraph regex on "1.A clean, healthy..." → num 1, raw "A clean, healthy...". 

First words: "A clean, healthy and sustainable environment" vs ref "A clean, healthy and sustainable environment" → match. 

Repairs: sentence joins etc. computed.

One more check — the plan's repair rule for sentence: `/([a-z])\.([A-Z])/g` → "$1. $2". My split: pre = m[1]+'.', post = m[2], inserted ' ' between → "a. K". Correct.

Comma: `/([a-z]),([A-Za-z])/g` → "$1, $2" → pre=m[1]+',', post=m[2]. Correct.

Quote: `/([a-z])“/g` → "$1 “" → pre=m[1], post='“'. Correct.

Dash: `/–([A-Za-z])/g` → "– $1" → pre='–', post=m[1]. Correct.

Now — one subtlety: applying sentence rule first may create "word. Word" where comma rule then... no interference.

But: could the sentence rule fire inside something like "art. 6"? "art. 6" — after '.' is space, no match (needs [A-Z] immediately). "e.g.States"? would fire — per plan, rules are as given. OK.

Now the "Elements found" table: els includes table (cover), div (container), p (line), h2 (title), h2/h3 (heading), p (paragraph). Total = 1+1+1+1+30+90 = 124 for the sample (6 roman h2 + 24 h3 = 30 headings). classCounts: cover 1, container 1, line 1, title 1, heading 30, paragraph 90 → sum 124 = total. Pass.

Check "Headings": h2n = 6, h3n = 24, glued = count of headings with glued label (8 of 10 per plan... whatever, computed).

Now — the plan says tab 02's closed box is "Headings found: n" — I use headings.length (30). Good.

Markdown export: items include title, h2s, h3s, ps in order. Good.

JSON round trip: buildJSON called before checks — define buildJSON before checks. Yes.

Now, "limitations" field: "no footnotes in this HTML version; the document has n". Good.

Also plan: JSON record field `part` = "the nearest heading and the roman-numbered section above it" — hmm, re-read: "`section` and `part` (the nearest heading and the roman-numbered section above it)". So section = nearest heading, part = roman section. My p.section = nearest heading display, p.part = roman h2 display. Good.

Now header: also include "n and years"? The general layout says header has source, n and years — but this plan's header spec: symbol link, adopted, source. I'll also add "n paragraphs" maybe in meta: `· 90 paragraphs in this HTML`. Nice touch: meta += ' · ' + paragraphs.length + ' paragraphs in this HTML'. OK.

Let me also make sure the app says on screen what's missing when data can't answer — covered by source limit and no-reference handling.

Now, writing the final answer: brief intro (≤3 sentences) before the code block, then the single html code block, nothing after.

Let me now write the complete file carefully, watching for JS syntax errors.

Also: careful with template literals vs string concat — I'll use string concat with single quotes and escape properly. In HTML inline script, avoid the sequence `</script>` — none of my strings contain it. Avoid `<!--`. OK.

One risk: in strings I use unicode escapes like \u201C — fine.

Also `String.prototype.closest` on e.target — ensure e.target is Element: `if(!(e.target instanceof Element)) return;`.

Let me write out the code now, mentally compiling.

Also note: `panels[j].hidden = !on;` — panels are the section elements; hidden attribute works with our CSS rule.

Initial HTML: panel-0 visible, others hidden. Tabs: tab-0 aria-selected true, others false tabindex -1.

Let me also compute `fwOk` etc. properly.

Also — the tile 2 when ref exists but paragraphs empty: "0 of 0" — fine.

Write buildMD's `paragraphs_expected: null` when no ref — mdVal not needed for number; I push raw. If exp null → 'null'. OK.

Now, one more detail from plan: tab 04 "The check panel (next section but one), open, every check on one line." — checks rendered as lines. Good.

"Under the buttons a closed heading 'Elements found (n)'" — done.

"At most seven things to click" — tab 04: 4 tabs + 2 buttons + 1 toggle = 7. OK.

Also the plan mentions header right: green dot "n of m checks pass" or red "n checks failed", then "1 source limit". Done.

Now write it all. I'll be meticulous with quotes in JS strings containing apostrophes — use \u2019 or escape. I'll use double-quoted JS strings where text has apostrophes, or use \u2019. To keep simple, I'll write user-facing strings with typographic apostrophes (\u2019) inside single-quoted strings — safe since ' vs ’ differ.

Let me write the final code.

Also — `clean()` uses `/^ | $/g` to trim single spaces at ends after collapsing — but collapse turns runs into single space, so ends have at most one space; the regex removes it. But multiple? collapse ensures single. OK. Actually also trim leading: after collapse, leading run → single space → removed by `^ `. Good.

One more: `el.textContent` for the table includes all cover text — fine, cover row shows first 80 chars.

Potential issue: `walk` uses `node.children` — HTMLCollection; converting with Array.from or index loop. I'll use index loop.

Also `firstTable.contains(el)` — when el is a top-level child not in table, contains false. OK.

Edge: what if there is no table? firstTable null → all elements walked. Fine.

Now, the checks: "Numbering" — if paragraphs empty, numbers run 1–0... detail: paragraphs.length? 'numbers run 1–'+n : 'no paragraphs found'. status pass if no problems. Fine.

Let me also add to check 1 link tab 02 on fail — done (tab index 1).

Check 3 (first words) link tab 1 on fail. Check 5 repairs link tab 2. Check 6 headings link tab 1? Plan doesn't require links; I'll add tab links where useful: repairs → tab 03 (index 2), first words → tab 02 (index 1), paragraph count fail → tab 02.

Now writing everything out. Also remember meta line in header: symbol link + adopted + source + paragraphs count.

Let me also handle `D.title` missing → '(untitled)'.

Time to write the final response. Intro: 2-3 sentences: "Built the paragraph extractor for WORKSHOP_DATA.html_doc: it parses the OHCHR HTML, classifies every block element, repairs provable missing spaces, checks the result against reference, and exports JSON/Markdown — all in one offline page." Then code block.

Let me carefully write the script now in full.

```js
(function(){
'use strict';
var D = (window.WORKSHOP_DATA && window.WORKSHOP_DATA.html_doc) || null;
if(!D){ document.body.innerHTML = '<p style="padding:28px;font-family:Georgia,serif">No WORKSHOP_DATA.html_doc was found on this page.</p>'; return; }

function esc(s){ return String(s==null?'':s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;'); }
function clean(s){ return String(s==null?'':s).replace(/[ \t\n\r\f\v]+/g,' ').replace(/^ /,'').replace(/ $/,''); }
function norm(s){ return String(s).replace(/[\u2018\u2019]/g,"'").replace(/[\u201C\u201D]/g,'"').replace(/[\u2013\u2014\u2011]/g,'-').replace(/\u00A0/g,' '); }

var ref = D.reference || null;
var symbol = D.symbol || '';
var docUrl = D.doc_url || '';
var source = D.source || '';
var exp = (ref && typeof ref.paragraphs==='number') ? ref.paragraphs : null;
var fexp = (ref && typeof ref.footnotes==='number') ? ref.footnotes : null;
var fileBase = symbol.replace(/\//g,'-') || 'document';

var parsed=null;
try{ parsed = new DOMParser().parseFromString(D.html||'','text/html'); }catch(e){ parsed=null; }
var bodyEl = parsed ? parsed.body : null;

var BLOCK = {P:1,H1:1,H2:1,H3:1,H4:1,H5:1,H6:1,DIV:1,TABLE:1,UL:1,OL:1,LI:1,BLOCKQUOTE:1,PRE:1,SECTION:1,ARTICLE:1,MAIN:1,ASIDE:1,FIGURE:1,DL:1,DT:1,DD:1,FORM:1,FIELDSET:1,ADDRESS:1,HR:1};
var firstTable = bodyEl ? bodyEl.querySelector('table') : null;
var els = [];
(function walk(node){
  if(!node) return;
  var kids = node.children;
  for(var i=0;i<kids.length;i++){
    var el = kids[i];
    if(firstTable && el===firstTable){ els.push({el:el, cls:'cover'}); continue; }
    if(firstTable && firstTable.contains(el)) continue;
    if(!BLOCK[el.tagName]) continue;
    els.push({el:el});
    if(el.children.length) walk(el);
  }
})(bodyEl);
```

Then splitHeading, RULES, applyRule, buildParagraph, classification loop, CHARS, logs, checks, renders, events.

I need to double check one thing in applyRule: `rule.re` has /g flag and is shared across paragraphs — I reset lastIndex=0 before each while loop. Since I use exec in a while loop until null, lastIndex resets to 0 after null? Actually after exec returns null, lastIndex is reset to 0 automatically. But I set it anyway. Good.

Also in applyRule, segments from previous rules include fix segments (single space) — skipped. But non-fix segments adjacent: after processing, out contains pieces; the final `out.push({t: t.slice(last), fix:false})` — if last===0 and no matches, pushes whole t. Good.

One bug: if a match occurs, I push `t.slice(last, m.index)+parts[0]` — but if last > m.index? Can't happen since exec finds non-overlapping matches in order.

Now classification loop — also need `items` for markdown and `byNum`.

Then CHARS.

Then:

```js
var allLogs=[]; paragraphs.forEach(function(p){ p.log.forEach(function(l){ allLogs.push(l); }); });
var ruleCounts={}; allLogs.forEach(function(l){ ruleCounts[l.rule]=(ruleCounts[l.rule]||0)+1; });
var repairParas = paragraphs.filter(function(p){ return p.log.length>0; }).length;
var fwMismatch = paragraphs.filter(function(p){ return p.fw===false; });
```

buildJSON/buildMD, checks, status, render, events.

For rendering panels I use innerHTML with concatenated strings — careful with quotes.

Let me also compute h2n/h3n/gluedN.

Now — writing panel 1 table: 90 rows each with a detail row → 180 tr elements; fine.

Also add to panel-1 a hint line: "click a row = expand in place · click = copy citation". Add small hint above table: `<p class="hint">click a row to expand it in place; the expanded row carries the full text, the first-words check, the repaired places and a copy-citation button</p>`.

OK. Also the plan: "First line: the first 120 characters cut at a word with '…'". Done.

Now finalize the checks details text.

Check 'Nothing lost': breakdown string.

Let me now also think: should the 'Repairs' check status ever be fail? It's informational; pass. Fine.

Write footer.

Also — accessibility: tab panels hidden → not focusable (hidden attr). Good.

Let me now also double-check the header status when ref missing: checks: paragraph count notrun, numbering pass (if paragraphs found), first words notrun, footnotes notrun, repairs pass, headings pass, nothing lost pass, round trip pass → nPass=5, m=5 → "5 of 5 checks pass · 0 source limits"? nLimit=0 so no limit text. Header shows green "5 of 5 checks pass". Hmm but plan says when ref missing, checks that need it show "not run" — done. OK.

Now, writing the response. The code will be long (~800 lines). Let me write it.

Actually one more consideration on `clean()` — I use it on textContent which includes newlines from HTML formatting; collapse handles. Good.

Also for `it.text` of cover table — includes "United Nations E/C.12/GC/27 ..." fine.

Also: the paragraph regex uses txt (cleaned). "1.A clean..." → match. But what if a paragraph number has trailing content like "1." only? fine.

Potential issue: `txt.match(/^(\d{1,3})\.\s*([\s\S]*)$/)` — for a line like "6 November 2025" no dot → no match. For "2025." unlikely. OK.

Now — the h2 title detection: `titleSeen` — but what if the first h2 appears after some paragraphs? In this doc it's before. Per plan "the first <h2> is the title". OK.

Let me write the markdown heading for title: `# ` + title text (includes trailing " *"). Fine.

Also in buildMD, paragraph text may contain characters like `*` — verbatim, fine.

Now write final HTML. I'll write CSS compactly but complete.

Also add `lang="en"`, title.

One more: the plan says tabs labels like `01 RESULT · 02 PARAGRAPHS · 03 LOST & CHANGED · 04 CHECKS & EXPORT` — I'll label buttons "01 RESULT", "02 PARAGRAPHS", "03 LOST & CHANGED", "04 CHECKS & EXPORT".

Also add `aria-label` on tablist.

Also: "A hidden tab panel is not focusable" — hidden handles.

Also the rail "n of m checks pass" link — data-goto="3".

Also add small hint under tabs? Not needed.

Let me make sure the delegated click handler doesn't conflict with tab buttons (they have their own listeners; the delegated handler checks .toggle/[data-goto]/... — tab buttons don't match those, and aren't inside tr.prow. Fine.)

Also the rowbtn inside prow: clicking triggers delegated handler → closest('tr.prow') → toggleRow. Also button's own click does nothing else. Good. But note: the delegated handler runs on document; the tab buttons' own listeners also run — no conflict.

Edge: clicking on the detail row's copy button — handled by copybtn branch before prow branch (pdetail not prow anyway).

Now — writing fillDetail's fixlist arrow: use '\u2192'.

Also in panel 2 Before/After cells: I want the inserted space visible in After: `esc(l.ctxBefore+l.pre)+'<span class="fix"> </span>'+esc(l.post+l.ctxAfter)`. Good.

Also add class "ctx" to before/after tds.

Now, finally, ensure no `</script>` inside strings — my strings contain `&lt;p&gt;` etc. in HTML strings — fine, they're escaped for display; the literal sequence "</script>" doesn't appear. In JS strings I have `'&lt;'+tag+'&gt;'` — fine.

Wait, in panel-3 elements table I wrote `'&lt;'+it.el.tagName.toLowerCase()+'&gt;'` — good.

Also in tile how text: `&lt;p&gt; elements...` — good.

Let me now also compute the header meta: 

```js
var metaParts = [];
if(symbol) metaParts.push('<a href="'+esc(docUrl)+'" target="_blank" rel="noopener">'+esc(symbol)+'</a>');
if(ref && ref.adopted) metaParts.push('adopted '+esc(ref.adopted));
metaParts.push(paragraphs.length+' paragraphs in this HTML');
if(source) metaParts.push(esc(source));
document.getElementById('docmeta').innerHTML = metaParts.join(' · ');
```

Good.

Now assemble. Also I should double check `showTab` initial: panels[0] visible.

Also: after rendering panels via innerHTML, the toggle buttons inside panels work via delegation. The dljson/dlmd listeners attached after render. Good.

Let me write the complete final code now, and count roughly — it's fine.

One more thought on the "Spaces: n repaired or flagged" tile — plan says "repaired or flagged". I'll cap: "spaces repaired — every one listed on tab 03". Good.

Also tab 01 tile 1 "beside the document has reference.paragraphs (green when equal, red with the difference)" — my cap includes difference. Good.

Writing now. I'll produce the final answer with a short intro then the code block.

Let me write the JS in full, carefully:

```js
(function(){
'use strict';
var D = (window.WORKSHOP_DATA && window.WORKSHOP_DATA.html_doc) || null;
if(!D){ document.body.innerHTML = '<p style="padding:28px">No WORKSHOP_DATA.html_doc was found on this page.</p>'; return; }

function esc(s){ return String(s==null?'':s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;'); }
function clean(s){ return String(s==null?'':s).replace(/[ \t\n\r\f\v]+/g,' ').replace(/^ /,'').replace(/ $/,''); }
function norm(s){ return String(s).replace(/[\u2018\u2019]/g,"'").replace(/[\u201C\u201D]/g,'"').replace(/[\u2013\u2014\u2011]/g,'-').replace(/\u00A0/g,' '); }

var ref = D.reference || null;
var symbol = D.symbol || '';
var docUrl = D.doc_url || '';
var source = D.source || '';
var exp = (ref && typeof ref.paragraphs === 'number') ? ref.paragraphs : null;
var fexp = (ref && typeof ref.footnotes === 'number') ? ref.footnotes : null;
var fileBase = symbol.replace(/\//g,'-') || 'document';

var parsed = null;
try { parsed = new DOMParser().parseFromString(D.html || '', 'text/html'); } catch(e) { parsed = null; }
var bodyEl = parsed ? parsed.body : null;

var BLOCK = {P:1,H1:1,H2:1,H3:1,H4:1,H5:1,H6:1,DIV:1,TABLE:1,UL:1,OL:1,LI:1,BLOCKQUOTE:1,PRE:1,SECTION:1,ARTICLE:1,MAIN:1,ASIDE:1,FIGURE:1,DL:1,DT:1,DD:1,FORM:1,FIELDSET:1,ADDRESS:1,HR:1};
var firstTable = bodyEl ? bodyEl.querySelector('table') : null;
var els = [];
(function walk(node){
  if(!node) return;
  var kids = node.children;
  for(var i=0;i<kids.length;i++){
    var el = kids[i];
    if(firstTable && el === firstTable){ els.push({el:el, cls:'cover'}); continue; }
    if(firstTable && firstTable.contains(el)) continue;
    if(!BLOCK[el.tagName]) continue;
    els.push({el:el});
    if(el.children.length) walk(el);
  }
})(bodyEl);

function splitHeading(txt){
  var m = txt.match(/^([IVX]+|[A-Z])\.\s*([\s\S]+)$/);
  if(m){
    var escL = m[1].replace(/[.*+?^${}()|[\]\\]/g,'\\$&');
    var glued = new RegExp('^'+escL+'\\.[^\\s]').test(txt);
    return {label:m[1], heading:clean(m[2]), display:m[1]+'. '+clean(m[2]), glued:glued};
  }
  return {label:null, heading:txt, display:txt, glued:false};
}

var RULES = [
  {name:'sentence join', re:/([a-z])\.([A-Z])/g, split:function(m){ return [m[1]+'.', m[2]]; }},
  {name:'comma join',    re:/([a-z]),([A-Za-z])/g, split:function(m){ return [m[1]+',', m[2]]; }},
  {name:'quote join',    re:/([a-z])\u201C/g,      split:function(m){ return [m[1], '\u201C']; }},
  {name:'dash join',     re:/\u2013([A-Za-z])/g,   split:function(m){ return ['\u2013', m[1]]; }}
];

function applyRule(segs, rule, paraNum, log){
  var out = [];
  for(var s=0;s<segs.length;s++){
    var seg = segs[s];
    if(seg.fix){ out.push(seg); continue; }
    var t = seg.t, last = 0, m;
    rule.re.lastIndex = 0;
    while((m = rule.re.exec(t)) !== null){
      var parts = rule.split(m);
      var ctxB = t.slice(Math.max(0, m.index-20), m.index);
      var ctxA = t.slice(m.index + m[0].length, m.index + m[0].length + 20);
      out.push({t: t.slice(last, m.index) + parts[0], fix:false});
      out.push({t:' ', fix:true});
      out.push({t: parts[1], fix:false});
      log.push({para:paraNum, rule:rule.name, ctxBefore:ctxB, match:m[0], pre:parts[0], post:parts[1], ctxAfter:ctxA});
      last = m.index + m[0].length;
      if(m[0].length === 0) rule.re.lastIndex++;
    }
    out.push({t: t.slice(last), fix:false});
  }
  return out;
}

var paragraphs = [], headings = [], items = [], classCounts = {}, unclassified = [];
var curPart = '', curSection = '', titleSeen = false;

function buildParagraph(num, raw, part, section){
  var log = [];
  var segs = [{t:raw, fix:false}];
  for(var r=0;r<RULES.length;r++) segs = applyRule(segs, RULES[r], num, log);
  var text = segs.map(function(s){ return s.t; }).join('');
  var html = segs.map(function(s){ return s.fix ? '<span class="fix">'+esc(s.t)+'</span>' : esc(s.t); }).join('');
  var words = text.split(/\s+/).filter(Boolean).slice(0,6).join(' ');
  var fw = null, fwRef = '';
  if(ref && ref.first_words){
    var key = String(num);
    if(Object.prototype.hasOwnProperty.call(ref.first_words, key)){
      fwRef = ref.first_words[key];
      fw = (norm(words) === norm(fwRef));
    }
  }
  return {num:num, raw:raw, text:text, html:html, log:log, part:part, section:section,
          fw:fw, fwFound:words, fwRef:fwRef, citation: symbol + ', para. ' + num};
}

for(var i=0;i<els.length;i++){
  var it = els[i], el = it.el, tag = el.tagName;
  var txt = clean(el.textContent || '');
  it.text = txt;
  if(it.cls === 'cover'){ /* cover */ }
  else if(tag === 'TABLE') it.cls = 'cover';
  else if(tag==='DIV'||tag==='SECTION'||tag==='ARTICLE'||tag==='MAIN'||tag==='ASIDE'||tag==='FIGURE') it.cls = 'container';
  else if(tag === 'H2'){
    if(!titleSeen){ titleSeen = true; it.cls = 'title'; items.push({kind:'title', text:txt}); }
    else {
      it.cls = 'heading';
      var h = splitHeading(txt); h.tag = 'H2';
      headings.push(h); items.push({kind:'h2', h:h});
      if(h.label && /^[IVX]+$/.test(h.label)) curPart = h.display;
      curSection = h.display;
    }
  }
  else if(/^H[3-6]$/.test(tag)){
    it.cls = 'heading';
    var h2 = splitHeading(txt); h2.tag = tag;
    headings.push(h2); items.push({kind:'h3', h:h2});
    curSection = h2.display;
  }
  else if(tag === 'P'){
    var m = txt.match(/^(\d{1,3})\.\s*([\s\S]*)$/);
    if(m){
      it.cls = 'paragraph';
      var p = buildParagraph(parseInt(m[1],10), clean(m[2]), curPart, curSection);
      paragraphs.push(p); items.push({kind:'p', p:p});
    } else it.cls = 'line';
  }
  else it.cls = 'unclassified';
  classCounts[it.cls] = (classCounts[it.cls]||0)+1;
  if(it.cls === 'unclassified') unclassified.push(it);
}

var byNum = {};
paragraphs.forEach(function(p){ byNum[p.num] = p; });

var CHARS = [
  {name:'en dash', cp:'U+2013', ch:'\u2013'},
  {name:'double quotes', cp:'U+201C / U+201D', chs:['\u201C','\u201D']},
  {name:'right single quote', cp:'U+2019', ch:'\u2019'},
  {name:'non-breaking hyphen', cp:'U+2011', ch:'\u2011'},
  {name:'non-breaking space', cp:'U+00A0', ch:'\u00A0'}
];
CHARS.forEach(function(c){
  var list = c.chs || [c.ch];
  c.count = 0; c.example = '';
  for(var i=0;i<paragraphs.length;i++){
    var t = paragraphs[i].text;
    for(var k=0;k<list.length;k++){
      var idx = t.indexOf(list[k]);
      while(idx !== -1){
        c.count++;
        if(!c.example){
          var b = t.slice(Math.max(0, idx-25), idx);
          var a = t.slice(idx+1, idx+26);
          c.example = esc(b) + '<span class="ch">'+esc(list[k]==='\u00A0' ? '\u2423' : list[k])+'</span>' + esc(a);
        }
        idx = t.indexOf(list[k], idx+1);
      }
    }
  }
});

var allLogs = [];
paragraphs.forEach(function(p){ p.log.forEach(function(l){ allLogs.push(l); }); });
var ruleCounts = {};
allLogs.forEach(function(l){ ruleCounts[l.rule] = (ruleCounts[l.rule]||0)+1; });
var repairParas = paragraphs.filter(function(p){ return p.log.length>0; }).length;
var fwMismatch = paragraphs.filter(function(p){ return p.fw===false; });

function buildJSON(){
  var recs = paragraphs.map(function(p){
    return {
      symbol: symbol,
      paragraph: p.num,
      section: p.section,
      part: p.part,
      text: p.text,
      text_raw: p.raw,
      first_words_match: p.fw,
      citation: p.citation,
      doc_url: docUrl,
      limitations: (fexp!=null) ? ('no footnotes in this HTML version; the document has '+fexp) : 'no footnotes in this HTML version'
    };
  });
  return JSON.stringify(recs, null, 2);
}
function mdVal(s){ return '"'+String(s).replace(/\\/g,'\\\\').replace(/"/g,'\\"')+'"'; }
function buildMD(){
  var today = new Date().toISOString().slice(0,10);
  var L = ['---'];
  L.push('title: '+mdVal(D.title||''));
  L.push('symbol: '+mdVal(symbol));
  if(ref && ref.adopted) L.push('adopted: '+mdVal(ref.adopted));
  L.push('source_url: '+mdVal(docUrl));
  L.push('extracted: '+today);
  L.push('paragraphs_found: '+paragraphs.length);
  L.push('paragraphs_expected: '+(exp!=null ? exp : 'null'));
  L.push('footnotes: '+mdVal('This HTML version has 0 footnotes'+(fexp!=null ? '; the document has '+fexp : '')+'.'));
  L.push('---','');
  items.forEach(function(it){
    if(it.kind==='title'){ L.push('# '+it.text, ''); }
    else if(it.kind==='h2'){ L.push('## '+it.h.display, ''); }
    else if(it.kind==='h3'){ L.push('### '+it.h.display, ''); }
    else if(it.kind==='p'){ L.push('**'+it.p.num+'.** '+it.p.text, ''); }
  });
  return L.join('\n');
}

var checks = [];
function addCheck(name, detail, status, tab){ checks.push({name:name, detail:detail, status:status, tab:(tab==null?null:tab)}); }

if(exp!=null) addCheck('Paragraph count', paragraphs.length+' found, '+exp+' expected', paragraphs.length===exp?'pass':'fail', 1);
else addCheck('Paragraph count', 'no reference in this file', 'notrun');

var numProblems = [];
paragraphs.forEach(function(p,i){ if(p.num !== i+1) numProblems.push('position '+(i+1)+' is numbered '+p.num); });
addCheck('Numbering', numProblems.length ? ('not 1\u2013n in order: '+numProblems.join('; ')) : ('numbers run 1\u2013'+paragraphs.length+' in order, no gaps or duplicates'), numProblems.length?'fail':'pass', numProblems.length?1:null);

if(ref && ref.first_words){
  addCheck('First words', fwMismatch.length===0 ? ('all '+paragraphs.length+' paragraphs match reference.first_words') : (fwMismatch.length+' differ: '+fwMismatch.map(function(p){ return 'para. '+p.num+' found \u201C'+p.fwFound+'\u201D / reference \u201C'+p.fwRef+'\u201D'; }).join('; ')), fwMismatch.length?'fail':'pass', fwMismatch.length?1:null);
} else addCheck('First words', 'no reference in this file', 'notrun');

if(fexp!=null) addCheck('Footnotes', '0 in this HTML, '+fexp+' in the document \u2014 the HTML version has no footnotes: a limit of the source, not of the app', 'limit');
else addCheck('Footnotes', 'no reference in this file', 'notrun');

addCheck('Repairs', allLogs.length+' spaces restored in '+repairParas+' paragraphs ('+RULES.map(function(r){ return r.name+': '+(ruleCounts[r.name]||0); }).join(', ')+'); every one is listed on tab 03 and text_raw keeps the text as found', 'pass', 2);

var h2n = headings.filter(function(h){ return h.tag==='H2'; }).length;
var gluedN = headings.filter(function(h){ return h.glued; }).length;
addCheck('Headings', (headings.length)+' headings found ('+h2n+' H2, '+(headings.length-h2n)+' H3), '+gluedN+' glued labels separated', 'pass', 1);

var totalEls = els.length, sum = 0, k;
for(k in classCounts) sum += classCounts[k];
var breakdown = Object.keys(classCounts).sort().map(function(kk){ return kk+': '+classCounts[kk]; }).join(', ');
addCheck('Nothing lost', totalEls+' block elements, all classified exactly once ('+breakdown+')'+(unclassified.length ? '; UNCLASSIFIED: '+unclassified.map(function(u){ return u.el.tagName; }).join(', ') : ''), (sum===totalEls && unclassified.length===0)?'pass':'fail');

var jsonStr = buildJSON();
var rtOk = false, rtDetail = '';
try { var parsed2 = JSON.parse(jsonStr); rtOk = (parsed2.length === paragraphs.length); rtDetail = 'JSON parsed back on build: '+parsed2.length+' records = '+paragraphs.length+' table rows'; }
catch(e){ rtDetail = 'JSON parse failed: '+e.message; }
addCheck('Export round trip', rtDetail, rtOk?'pass':'fail');

var nPass=0,nFail=0,nLimit=0,nNotRun=0;
checks.forEach(function(c){ if(c.status==='pass')nPass++; else if(c.status==='fail')nFail++; else if(c.status==='limit')nLimit++; else nNotRun++; });
var m = nPass+nFail;
var statusText, statusCls;
if(nFail>0){ statusText = nFail+' check'+(nFail>1?'s':'')+' failed'; statusCls='bad'; }
else if(nPass>0){ statusText = nPass+' of '+m+' checks pass'; statusCls='ok'; }
else { statusText = 'checks not run'; statusCls=''; }
if(nLimit>0) statusText += ' \u00B7 '+nLimit+' source limit'+(nLimit>1?'s':'');
var railStatus = nFail>0 ? (nFail+' checks failed') : (nPass>0 ? (nPass+' of '+m+' checks pass') : 'checks not run');
```

Then rendering. OK, now write render code (as planned above). Then events.

I think this is solid. Let me also make sure `panels` variable name doesn't clash. Fine.

Also note: in the delegated click handler, `e.target.closest` — need Element check.

Final check on plan item: "the same string is the `citation` field of every export" — yes.

"File names: the symbol with slashes replaced by hyphens" — fileBase. Good.

Now write the whole document. Also include `<meta name="viewport">`.

Also — the intro before code: max 3 short sentences. Then code block. Nothing after.

Let me write the CSS fully now (final):

I'll include responsive tweak. Also ensure `main` min-width 0 to avoid overflow with long words — add `overflow-wrap:break-word` on body maybe. Add `td, .full {overflow-wrap:break-word}`.

Also table on narrow screens: allow horizontal scroll? "Works on a laptop screen without horizontal scrolling" — laptop fine. Add `main{overflow-x:auto}`? Better keep tables fitting: first line column flexible. OK.

Write it.

One more detail: the plan says tab 02 table columns "No. | Section | First line | Check" — done. And "the expanded row shows the full path ('IV. … › Right to work (art. 6)')" — my path uses '\u203A' (›). Good.

Also "A closed 'Headings found: n' box above the table lists them" — done.

Also plan: header right "then '1 source limit' (the footnotes)" — done via statusText.

Also footer: "source, built, and 'Done by this page's code; no model was called and nothing left the browser.'" — done.

Also credits line at bottom — done in footer.

Now produce final answer.