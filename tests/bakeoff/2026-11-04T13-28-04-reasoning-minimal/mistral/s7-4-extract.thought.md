Let me plan this app carefully. The user wants a single HTML file app that:

1. Parses `WORKSHOP_DATA.html_doc.html` with DOMParser
2. Classifies elements: cover table, committee line `<p>`, title `<h2>`, headings `<h2>`/`<h3>`, numbered paragraphs `<p>`
3. Computes repairs (space insertions) with rules
4. Counts special characters
5. Compares against `reference` (paragraphs, footnotes, adopted, first_words)
6. Four tabs: 01 RESULT, 02 PARAGRAPHS, 03 LOST & CHANGED, 04 CHECKS & EXPORT
7. Left rail with document card and big numbers
8. Header with title, symbol link, adopted, source, check status dot
9. Footer
10. Exports: JSON and Markdown downloads via Blob
11. Copy citation buttons
12. Keyboard accessible tabs with arrow keys, aria-expanded rows

Data shape: `WORKSHOP_DATA.html_doc` is `{title, symbol, doc_url, source, html, reference: {paragraphs, footnotes, adopted, first_words}}`. Wait — the sample shows `html_doc` as an array with one object, but the description says `WORKSHOP_DATA.html_doc`: one UN document as `{title, symbol, doc_url, source, html, reference}`. The sample JSON shows `"html_doc": [ { "html": ... } ]` — an array. Hmm. The description says "The same shape as..." for pdf_text_2 which is also shown as array. Actually the preview shows arrays but the description says objects. To be safe, handle both: `const D = Array.isArray(WORKSHOP_DATA.html_doc) ? WORKSHOP_DATA.html_doc[0] : WORKSHOP_DATA.html_doc;`. Also `built` — footer mentions `built` but html_doc description doesn't list `built`. The footer says "`source`, `built`". I'll handle missing built gracefully ("built" may be undefined — show if present). Actually the description of html_doc fields: `{title, symbol, doc_url, source, html, reference: {...}}` — no `built`. I'll show source and, if present, built; otherwise just source. Better: show `source` and if `D.built` exists show it. The plan says footer: `source`, `built`, and the done line. I'll render built only if present, else omit gracefully. Hmm, but plan says footer always visible with source, built. I'll do: `source` + (built ? ` · built ${built}` : ''). Safe.

Also `reference` may be missing — handle "no reference in this file".

Let me write the pipeline:

```js
const doc = new DOMParser().parseFromString(D.html, 'text/html');
const body = doc.body;
```

Classification: iterate over body's children (block elements). The first `<table>` is cover. Then elements in order. For each element:
- tag TABLE → cover (first one; any table → cover)
- tag P: text = el.textContent. Match `/^(\d{1,3})\.\s*(.*)$/s` → paragraph with number parseInt, raw text = group 2. Else → committee line (or "other p").
- tag H2: first h2 → title; subsequent h2 → heading, try split `/^([IVX]+|[A-Z])\.\s*(.+)$/s` into label + heading. Note "I.Introduction" glued — regex `^([IVX]+|[A-Z])\.\s*(.+)$` with `\s*` handles glued. But careful: a heading like "Right to work (art. 6)" (h3, plain, no label) doesn't match → label null, heading = full text.
- tag H3 → heading similarly.
- anything else → unclassified.

Wait: the title h2 ends in " *" — the first h2 is the title. But what if there are multiple h2 before content? Plan says "the first `<h2>` is the title". OK.

Also headings: "6 roman-numbered `<h2>`, 24 `<h3>` (4 lettered, 20 plain)". The split regex: `/^([IVX]+|[A-Z])\.\s*(.+)$/s`. For "I.Introduction" → label "I", heading "Introduction". For "D. Obligation" → label "D", heading "Obligation". For "Right to work (art. 6)" → no match (starts with capital R followed by lowercase... "R" then "ight" — regex `[A-Z]\.` requires a period after single letter; "Right" has no period after R, so no match). Good. But careful: a heading like "A. Something" matches with label "A". What about roman "IV." — `[IVX]+` matches "IV". Good. Edge: heading text might be "I.Introduction" — matches.

Hmm, but what about h2 title "General comment No. 27 (2025) on ... *" — it's the first h2, classified as title regardless.

Paragraph regex: `/^(\d{1,3})\.\s*(.*)$/s` on the p's textContent. But textContent of "1.A clean..." — the p contains "1.A clean, healthy..." so textContent starts "1.A clean". Match: number "1", then `\.\s*` consumes ".", then rest. Good. But careful: a committee line like "Committee on Economic, Social and Cultural Rights" doesn't start with digits. Good. But what about a paragraph p that contains nested elements? textContent handles.

Wait — potential issue: the number might be inside the p as text "1." with no space. The regex `^(\d{1,3})\.` — for "1.A clean" → matches "1" + ".". Good. For "109.243 Strengthen..." (not in this doc). Fine.

But there's a subtlety: what if a `<p>` starts with digits but isn't a paragraph, e.g., a date "6 November 2025"? In the cover table, dates are inside the table, so they're cover. After the table, the committee line is a p. In this document, after the table: bold p (committee), h2 title, h2 "I.Introduction", then p "1....". So OK. But to be safe, plan says exactly this classification. Also `\d{1,3}` — "6 November 2025" would match "6" then require "." — "6 November" has no period after 6, so no match. Good.

Section tracking: maintain `currentH2` (roman part) and `currentHeading` (nearest heading). For each paragraph, section = nearest heading above (could be h2 or h3), part = nearest roman-numbered h2. "Roman-numbered h2" — an h2 whose label matches `[IVX]+`. The title h2 is not a heading. So part = last h2 with roman label. If none yet, part = null.

Full path for expanded row: "IV. … › Right to work (art. 6)" — part label + heading + " › " + section heading. I'll build path = [partLabel, sectionLabel?]. Actually plan: "the expanded row shows the full path ('IV. … › Right to work (art. 6)')". So path = part (roman h2, e.g. "IV. ...") + " › " + section. I'll show part as its label+heading maybe truncated. Let me store for each heading: `label` (e.g. "IV" or "D" or null), `heading` (text after label), `full` (original text). Path: if part exists, part.full (or label + ". " + heading) then " › " then section.full. Keep simple: use the original heading text.

Repairs on text_raw:
- sentence join: `/([a-z])\.([A-Z])/g` → "$1. $2"
- comma join: `/([a-z]),([A-Za-z])/g` → "$1, $2"
- quote join: `/([a-z])“/g` → "$1 “"
- dash join: `/–([A-Za-z])/g` → "– $1"

Each insertion logged: {para, rule, before: 20 chars each side of the match, after}. Log with context: take text_raw, find match index, context = raw.slice(max(0,i-20), i) + "[" + matched + "]" + raw.slice(i+match.length, i+match.length+20). Simpler: store the matched substring and surrounding 20 chars from text_raw.

Rules named: "sentence join", "comma join", "quote join", "dash join". Counts per rule.

Note: applying rules sequentially — apply to text_raw progressively, logging each insertion. Since insertions change indices, easiest: run each rule with replace callback on the current string, collecting logs with context from the string at time of replacement. Use a function:

```js
function applyRule(str, re, ruleName, paraNo, logs) {
  return str.replace(re, (m, ...args) => {
    const idx = args[args.length-2]; // offset
    logs.push({para: paraNo, rule: ruleName, match: m, before: str.slice(Math.max(0,idx-20), idx), after: str.slice(idx+m.length, idx+m.length+20)});
    return m.replace(...) // insertion
  });
}
```

For sentence: replacement "$1. $2" — but in callback, return args[0]+". "+args[1]. For comma: args[0]+", "+args[1]. Quote: args[0]+" “". Dash: "– "+args[1].

Order: apply sentence, comma, quote, dash in sequence to text_raw → text.

Characters counted over all paragraph texts (text, after repair — plan says "Counted over all paragraph texts"; I'll count over `text`): en dash U+2013, “ U+201C, ” U+201D, ’ U+2019, ‑ U+2011, NBSP U+00A0. Table rows: Character | Count | Example. Example: find first occurrence in some paragraph text with context. For quotes, show both “ and ” maybe as one row "double quotes “ ”" — plan says "the double quotes" as one row. I'll do rows: en dash –, double quotes “ ” (count both), right single quote ’, non-breaking hyphen ‑, non-breaking space (nbsp). Count for double quotes = count of “ + count of ”.

First words: first six whitespace-separated words of `text` vs `reference.first_words[String(number)]`. Normalize both: curly quotes → straight, en dash and U+2011 → "-", NBSP → " ". Case kept. Compare joined by space. Note: first_words values like "A clean, healthy and sustainable environment" — six words. Split on whitespace. The found text's first six words: e.g. "A clean, healthy and sustainable environment" — after normalization. Compare strings equal.

Hmm — but repairs might affect first words (e.g., para 13 "Giventhe..." — first words differ). The check uses `text` (repaired). Plan: "The first six whitespace-separated words of `text` against reference.first_words". Yes, use repaired text.

Checks list (tab 04):
1. Paragraph count: found vs reference.paragraphs → pass/fail.
2. Numbering: exactly 1..n in order; gaps/duplicates listed.
3. First words: mismatches listed "para. n: found … / reference …".
4. Footnotes: 0 vs reference.footnotes → "source limit" (red), counted apart from failures.
5. Repairs: n spaces restored in n paragraphs, per rule counts.
6. Headings: count h2/h3, glued labels separated count.
7. Nothing lost: every block element classified exactly once; counts per class sum to total; unclassified listed red.
8. Export round trip: JSON parsed back, record count equals table's. This runs when? "The JSON to download is parsed back; its record count equals the table's." I can run it on load by building the JSON string, parsing it, comparing length. Do it at pipeline time.

Check status in header: "n of m checks pass" green dot, or red "n checks failed". Footnote check is "source limit" — counted apart from failures. So m = checks excluding footnote? Plan: header shows "n of m checks pass" or "n checks failed", then "1 source limit". So m = total checks minus the source-limit one(s). I'll compute: passes, failures, sourceLimits. Header: if failures>0 red dot "X checks failed" else green dot "n of m checks pass"; then "· 1 source limit" (if any). Rail: "n of m checks pass" linking to tab 04.

If reference missing: tiles say "no reference in this file", checks needing it show "not run".

Tabs: role="tablist", buttons role="tab" aria-selected, panels role="tabpanel". Arrow key navigation: left/right (and up/down) move between tabs, Home/End. Clicking a tab shows its panel, hides others (hidden attribute + CSS `[hidden]{display:none!important}`).

Left rail: always visible. "DOCUMENT" heading, card with symbol monospace + short title (title maybe long — use title, it's fine, or shorten). Two big serif numbers: "n paragraphs of reference.paragraphs" with thin bar (red when short or over) — bar width = min(n/expected,1)*100%, red if n!==expected. "0 footnotes of reference.footnotes" in red "not in this HTML". Then "n of m checks pass" link to tab 04.

Tab 01 RESULT: four tiles:
- Paragraphs found: n (big serif) beside "the document has reference.paragraphs" — green when equal, red with difference (e.g. "+2" or "−3").
- First words match: n of reference.paragraphs.
- Footnotes: 0 of reference.footnotes, red, "this HTML version has none; see tab 03".
- Spaces: n repaired or flagged, link to tab 03.
Each tile has "How this is computed" line.

If no reference: tiles say "no reference in this file". If html yields no p: tab 01 says so and exports disabled.

Tab 02 PARAGRAPHS: closed "Headings found: n" box (button aria-expanded) listing headings above the table. Table: caption "n paragraphs found, m expected", monospace "TAB.02"? Plan says every table has serif caption stating message + monospace number (TAB.01). Hmm "a monospace number (`TAB.01`)" — I'll add a small monospace label like "TAB.02 · PARAGRAPHS" near caption. Columns: No. | Section | First line | Check. Rows are buttons with aria-expanded — implement as table rows where the row itself is clickable? "Rows are buttons with aria-expanded" — I'll make each row a `<tr>` containing a `<button>` spanning? Simpler accessible approach: each row is a `<tr tabindex="0" role="button" aria-expanded>`? The plan says rows are buttons. I'll make the first cell contain a button? Hmm. Common pattern: make the whole row a button-like: use `<tr>` with a `<button class="rowbtn">` inside first cell covering... Actually simplest robust: each paragraph row is a `<tr>` whose cells contain a single `<button>` in the No. cell? That's awkward for layout.

Alternative: render as a list of `<div role="button">`? But plan says table with caption, th scope. I can do: table with tbody where each `<tr>` has `tabindex="0"`, `role="button"`, `aria-expanded`, and keydown Enter/Space toggles. That satisfies "rows are buttons with aria-expanded" in spirit. But role="button" on tr breaks table semantics for screen readers... For this workshop, acceptable. Alternatively put a real `<button>` inside the first `<td>` that says the number, and the whole row clickable via JS on the tr. I'll do: tr with class, containing td with button (the number, aria-expanded controls the detail row), plus click handler on tr. Actually cleanest: each paragraph = two rows: main row (clickable, contains button in first cell with aria-expanded + aria-controls pointing to detail row id) and a hidden detail row (`<tr class="detail" hidden>`). The button in the No. cell: `<button aria-expanded="false" aria-controls="d-12">12</button>`. Clicking anywhere on the main row triggers the button. Keyboard: button is focusable, Enter/Space works natively. Good.

Detail row content: full text verbatim (in a `<td colspan=4>`), with repaired places marked by thin red box — I'll wrap repaired spots in `<mark class="repair">`. To do that, I need to know positions in `text`. Since repairs were applied via replace, I can rebuild: when applying rules, record match positions... but positions shift after each insertion. Simpler: after computing text, re-run the rules on text_raw and build HTML by walking: apply rules one at a time, and for marking, I can compute the final text and also produce a marked-up version by processing sequentially: maintain `html` string built from text_raw where each replacement inserts `<mark> </mark>`? Hmm.

Approach: build marked text by applying rules with a function that returns both new string and segments. Let me do: start with segments = [text_raw]. For each rule, for each segment that is plain text, apply regex replace with callback that splits segment into [before, MATCH_MARKED, after] where MATCH_MARKED = match with inserted space wrapped: e.g. for sentence rule match "s.K" → `s.<mark class="rep"> </mark>K`? The inserted space marked: "the inserted space marked". So render as `levels.<mark> </mark>Key`. I'll construct: for sentence: g1 + "." + `<mark class="rep"> </mark>` + g2. For comma: g1 + "," + mark + g2. Quote: g1 + `<mark class="rep"> </mark>` + "“". Dash: "–" + mark + g1.

Implementation: represent text as array of parts (strings and marked-space objects). Simpler: build an HTML string incrementally. Start `html = escapeHtml(text_raw)`. For each rule, apply regex on the *plain* text but we need to map to html... messy because escaping.

Alternative simpler: do replacements on plain text while recording, for each insertion, the character index in the *final* text where the space was inserted. Since rules applied sequentially, I can track: maintain `text` and a list of insertion positions in current text. When a rule replaces at index i with match m and replacement r (which is m with a space inserted at position k within m), the inserted space ends up at final position i+k. But subsequent rules shift positions. I can adjust: keep sorted list of inserted positions; when a later rule inserts at index j, all recorded positions >= j shift by +1 (the inserted space adds 1 char). Actually replacement changes length: r.length - m.length = 1 (one space inserted). So after each replacement at index i, positions >= i+? Let me just recompute: after all rules, re-run all rules on text_raw in the same order, but this time build the marked HTML directly using a segment list:

```js
let segs = [esc(text_raw)]; // but rules need to match across... 
```

Rules match within text; matches won't span across previous insertions? They could in theory but practically fine. Hmm, risk: after inserting a space, a new pattern could form? E.g. "a.B" → "a. B" — no new matches created by inserting spaces (patterns require no space). Inserting a space can only destroy matches, not create them (all patterns require adjacent chars without space). But the regex runs on the whole string at once per rule, so within one rule pass, replacements are non-overlapping and computed on the original string of that pass. So: process rule by rule; for each rule, run `String.replace` with callback on the current plain text, and simultaneously build marked html? The issue: html escaping.

Cleaner: keep an array `parts` of {text, marked:boolean}. Initially [{text: text_raw, marked:false}]. For each rule: iterate parts; for unmarked parts, run regex with callback using offset relative to that part; split the part into before/match/after, where match becomes {text: replacement, marked: true} — but the replacement includes original chars plus inserted space; I want only the space marked. So split match into sub-parts: e.g. sentence match "s.K" → [{text:"s."},{text:" ",marked:true},{text:"K"}]. For comma "a,B" → "a," + " " + "B". Quote "a“" → "a" + " " + "“". Dash "–a" → "–" + " " + "a".

For marked parts, skip (don't re-match inside marks — fine since marks are single spaces).

Then final text = parts.map(p=>p.text).join(""), and markedHtml = parts.map(p => p.marked ? `<mark class="rep">${esc(p.text)}</mark>` : esc(p.text)).join("").

But wait — the plan says text = text_raw with rules applied via simple regex replaces. My segment approach yields the same result as sequential regex replace per rule (since within a rule, replace processes left-to-right on the current string, and my per-part processing is equivalent as long as matches don't span part boundaries — they can't span a marked space since patterns need adjacency... actually a pattern could span from an unmarked part into... no, parts are contiguous; a match could theoretically start in one unmarked part and... all unmarked parts are contiguous chunks of original text separated by marked spaces; a pattern requiring adjacency can't cross a space. But patterns like `/([a-z])\.([A-Z])/` require no space between, so can't cross a marked space. However, could a match span two unmarked parts that are adjacent (i.e., a previous rule split them)? Previous rule insertions create marked parts between, so unmarked parts are separated by marked parts. Except the very first rule: one part. So fine. Also, could a match within one unmarked part be affected by... no. Equivalent. 

Also logging: for each insertion, log {para, rule, match, contextBefore, contextAfter} from the part's text at that moment. Context: 20 chars each side within the part (or the whole current text — part is fine, but for display "20 characters each side" — I'll take from the joined plain text at that point; simpler: from the part text, pad). I'll compute context from the current full plain text: before = plain.slice(max(0,idx-20), idx), after = plain.slice(idx+m.length, idx+m.length+20). To get idx in full text, track offset of part within full text. Manageable: maintain offset as I iterate parts.

Actually simpler: do it in two passes. Pass 1: compute text via plain sequential replaces, logging matches with context from the string at that time (using replace callback offset — the offset given is relative to the string being replaced in that pass, which is the current full text). That gives logs. Pass 2: build marked html via segment approach (no logging needed). Both passes apply identical rules in identical order → same result. 

For pass 1 logging with replace callback: `str.replace(re, (m, g1, g2, offset) => {...})` — for regex with 2 groups, callback args: (match, p1, p2, offset, string). Return replacement. Log: {rule, match: m, before: str.slice(Math.max(0,offset-20), offset), after: str.slice(offset+m.length, offset+m.length+20)}. Good.

Pass 2 segments: as described.

Rule definitions:
```js
const RULES = [
 {name:"sentence join", re:/([a-z])\.([A-Z])/g, rep:(a,b)=>a+". "+b, mark:(m)=>...},
 ...
];
```
For marking in pass 2, I need to know where the space goes within the match. Define per rule a function that given match returns array of [text, marked] pieces:
- sentence: m = a+"."+b → [[a+".",false],[" ",true],[b,false]]
- comma: a+","+b → [[a+",",false],[" ",true],[b,false]]
- quote: a+"“" → [[a,false],[" ",true],["“",false]]
- dash: "–"+a → [["–",false],[" ",true],[a,false]]

In pass 2, for each unmarked part, use `part.text.replace(re, (m, ...gs) => { const offset = gs[gs.length-2]; ... })` but replace returns a string, losing segmentation. Instead, manually loop with `re.exec` on the part text:

```js
function applyRuleMarked(parts, rule) {
  const out = [];
  for (const p of parts) {
    if (p.marked) { out.push(p); continue; }
    let last = 0; let m; rule.re.lastIndex = 0;
    while ((m = rule.re.exec(p.text)) !== null) {
      const pieces = rule.pieces(m);
      out.push({text: p.text.slice(last, m.index), marked:false});
      for (const [t, mk] of pieces) out.push({text:t, marked:mk});
      last = m.index + m[0].length;
      if (m[0].length === 0) rule.re.lastIndex++; // safety
    }
    out.push({text: p.text.slice(last), marked:false});
  }
  return out;
}
```

And pass 1:
```js
function applyRulePlain(str, rule, paraNo, logs) {
  return str.replace(rule.re, (m, ...rest) => {
    const offset = rest[rest.length-2];
    logs.push({para: paraNo, rule: rule.name, match: m, before: str.slice(Math.max(0,offset-20), offset), after: str.slice(offset+m.length, offset+m.length+20)});
    return rule.rep(...rest.slice(0, -2));
  });
}
```

Careful: `rest` = [g1, g2, offset, string] for 2-group regex. rep takes (g1,g2). OK.

Note: regexes with /g and .replace — fine. But reusing a /g regex across calls with exec needs lastIndex reset — I reset in the marked loop. For replace, lastIndex is handled internally. OK.

Edge: quote rule `/([a-z])“/g` — one group. comma `/([a-z]),([A-Za-z])/g`. dash `/–([A-Za-z])/g`.

Order matters: plan lists sentence, comma, quote, dash. Apply in that order.

Hmm wait, one subtlety: sentence rule `([a-z])\.([A-Z])` — could match inside something like "art. 6)"? "art. 6" — after "." is space, no match. "levels.Key" matches. But also could match abbreviations like "e.g.Something" — that's the point. But also could match "No.27"? "o.2" — 2 is not [A-Z]. Fine. What about "U.S.A"? "U.S" — U is not [a-z]. Fine.

Comma rule `([a-z]),([A-Za-z])` — "land,wetlands" → matches. But also "e.g,foo". Fine.

Now, first-words check normalization:
```js
function norm(s){ return s.replace(/[“”]/g,'"').replace(/[’]/g,"'").replace(/[–—]/g,'-').replace(/[\u2011]/g,'-').replace(/\u00A0/g,' '); }
```
Plan: "turning curly quotes straight, en dashes and non-breaking hyphens into a hyphen and non-breaking spaces into spaces". Curly quotes → straight (both double and single? "curly quotes straight" — I'll do “”→" and ’→'). En dash → hyphen, U+2011 → hyphen, NBSP → space. Case kept.

first six words: `text.split(/\s+/).slice(0,6).join(' ')` vs `norm(reference.first_words[String(n)])`. Compare norm(found) === norm(ref). Note reference first_words might have different spacing; normalize whitespace too: `.trim().replace(/\s+/g,' ')`.

Numbering check: found numbers array; expected 1..found.length? Plan: "Exactly 1 to n in order; gaps and duplicates listed." n = reference.paragraphs if available else found count. I'll check: numbers sorted equal [1..max] and no duplicates. List gaps/duplicates. Compare against reference.paragraphs count in check 1.

Nothing lost check: total block elements = cover tables + committee p + title h2 + headings + paragraphs + unclassified. Sum of classes === total, unclassified count 0 (list them if any).

Headings check: count h2 (excluding title) + h3; glued labels separated = headings where original text had no space after label period (i.e., matched regex with `\s*` consuming zero spaces). I can detect: if match and the char after "." in original is not whitespace → glued. Count those.

Export JSON: array of records with fields: symbol, paragraph (number), section, part, text, text_raw, first_words_match, citation, doc_url, limitations. limitations: "no footnotes in this HTML version; the document has n" (n = reference.footnotes or "?" if no reference). Build JSON string; round-trip check: JSON.parse(json).length === paragraphs.length.

Export Markdown: front matter between --- lines: title, symbol, adopted, source_url, extracted (today's date YYYY-MM-DD), paragraphs_found, paragraphs_expected, footnotes sentence. Then headings as ## and ### lines in document order and each paragraph as its number in bold then text. "the headings as `##` and `###` lines in document order and each paragraph as its number in bold, then its text". So iterate elements in document order: h2 (non-title) → `## label. heading` (or full text), h3 → `### ...`, paragraph → `**n.** text`. Title h2 → maybe `# title`? Plan says headings as ## and ### — the title h2 is the document title, already in front matter; I'll emit it as `# title`? Plan doesn't say; keep simple: skip the title h2 in body (it's in front matter) or emit as `#`. I'll emit `# title` — hmm "then the headings as ## and ### lines" — the title is an h2 too. To follow plan literally, all non-title headings: h2→##, h3→###. I'll skip the title h2 (it's the doc title in front matter). Actually safer to include everything in document order: title h2 as `#`? The plan: "then the headings as `##` and `###` lines in document order and each paragraph as its number in bold, then its text." I'll treat the first h2 (title) as `#` line — reasonable. Hmm, but plan says headings as ## and ###. The title is classified as title, not heading. I'll emit `# {title}` for it. Fine.

Markdown paragraph: `**12.** text` — text is the repaired text? Or raw? "each paragraph as its number in bold, then its text" — I'll use repaired `text` (the app's output). Hmm, verbatim... The JSON has both text and text_raw. For markdown, use `text` (repaired) — it's the app's result. I'll use text.

File names: symbol with slashes replaced by hyphens: `E-C.12-GC-27.json` / `.md`. Blob URL, UTF-8: `new Blob([str], {type:'application/json;charset=utf-8'})`, `URL.createObjectURL`, temp `<a download>` click.

Copy citation: navigator.clipboard.writeText with fallback (execCommand). Show "Copied" for 2s. Clipboard may fail in sandbox — fallback: create textarea, select, document.execCommand('copy'). Wrap in try/catch; if fails, still show citation text? I'll attempt clipboard, fallback textarea; show "Copied" or on failure select the text... keep simple: try clipboard API, catch → fallback; if both fail, show "Press Ctrl+C" — I'll just show "Copied" optimistically after attempting, or show the citation in a prompt? Keep: attempt, then set button text "Copied" for 2s regardless (best effort), maybe. Better to be honest: if copy fails, show "Copy failed — select manually". I'll implement fallback and set text accordingly.

Tab 03 LOST & CHANGED: three blocks:
1. Lost: footnotes — serif title "Lost: footnotes (n)" with count; paragraph text as specified.
2. Changed: spaces — table Paragraph | Before | After | Rule; count per rule above it (e.g., "sentence join: 23 · comma join: 8 · ..."). Before/After: show context with the match highlighted — e.g. Before: `…levels.Key…` After: `…levels. Key…` with inserted space marked (in After, wrap the space in mark). Clicking a row opens the paragraph on tab 02: switch to tab 02 and expand that row, scroll to it.
3. Changed: characters — table Character | Count | Example. Hint line. Note line.

"Before | After" — I'll show before = before+match+after (from log), after = before + repaired match + after. Mark inserted space in after with `<mark>`.

Tab 04: check panel open, every check one line: what was compared, two values, pass (green) / check failed (red, link to rows) / source limit (red). Then Export with two buttons. Then closed "Elements found (n)" heading (button aria-expanded) with table Tag | Classified as | Text (first 80 chars) — every block element in order.

"At most seven things to click" per view — tab 04 has: 2 export buttons + 1 elements heading = 3. Tab 02: headings box + rows (rows not counted). Tab 03: rows clickable. Fine.

Header right: green/red dot + "n of m checks pass" or "n checks failed", then "1 source limit". 

Footer: source, built (if present), done line.

Now the "How this is computed" lines: near every chart/number. Tiles each get one.

Design: warm off-white #f4f0e8, ink #1d1b18, rules #d9d2c3, accent #9b2335, green for pass — "dark green" e.g. #1e6b3a. Serif Georgia for title/big numbers/figure titles; monospace labels 11-12px uppercase letter-spaced; sans 16px body.

Layout: header top; below, a grid: left rail (~260px) + main area with tabs. Tabs row under header. Rail always visible.

Let me now think about the header line: monospace label "UN DOCUMENT · HTML", serif title (h1), one line: symbol linked to doc_url (new tab, target=_blank rel=noopener), "adopted {reference.adopted}", source. Right side: status dot + text + "1 source limit".

Rail: "DOCUMENT" monospace heading; card: symbol monospace, short title (I'll use title, maybe truncated via CSS). Big numbers: paragraphs "n" big serif with "of m" small, thin bar underneath (div with inner width %). Footnotes "0" big serif red with "of m" and "not in this HTML" note. Then checks line "n of m checks pass" as link (button styled as link) → go to tab 04.

If no reference: rail numbers show "n paragraphs" without "of m"? Plan: tiles say "no reference in this file". Rail: I'll show n paragraphs (no expected), footnotes "0" with "not in this HTML" (reference.footnotes unknown → "the document has footnotes not counted here"? If no reference, say "0 footnotes in this HTML"). Handle gracefully.

Tabs implementation:

```html
<div class="tabs" role="tablist" aria-label="Views">
  <button role="tab" id="tab-1" aria-controls="panel-1" aria-selected="true">01 RESULT</button>
  ...
</div>
```

Panels: `<section role="tabpanel" id="panel-1" aria-labelledby="tab-1">`. Hidden panels get `hidden` attribute. Arrow keys: on keydown in tablist, ArrowRight/ArrowDown → next, ArrowLeft/ArrowUp → prev, Home/End. Move focus and activate (activation on focus, simple).

Tab labels: `01 RESULT · 02 PARAGRAPHS · 03 LOST & CHANGED · 04 CHECKS & EXPORT` — as separate buttons: "01 RESULT", "02 PARAGRAPHS", "03 LOST & CHANGED", "04 CHECKS & EXPORT".

Now details of tab 02 table:

Columns: No. | Section | First line | Check. First line: first 120 chars cut at a word with "…": 
```js
function firstLine(t){ if(t.length<=120) return t; let cut=t.slice(0,120); cut=cut.slice(0, cut.lastIndexOf(' ')); return cut+' …'; }
```
Hmm "cut at a word with '…'" — append "…". I'll use "…" (single ellipsis char) or "..."? Plan writes "…". Use "…".

Check column: "OK" (green) or "first words differ" (red). If no reference: "no reference".

Detail row: full text with marks, then "Reference first words: …" vs "Found: …" when differ, then repairs in this paragraph listed ("sentence join at '…levels.Key…'"), then Copy citation button.

Section column: nearest heading full text (e.g. "Right to work (art. 6)"). Might be long — CSS ellipsis with title attr.

Headings box: closed by default? "A closed 'Headings found: n' box above the table lists them" — closed until clicked (button aria-expanded). List: each heading with its level (H2/H3) and text, maybe with the paragraph numbers under it? Keep simple: list of headings in order with label. I'll show "IV. Introduction" style: if label, `label. heading` else full text; prefix with H2/H3 monospace.

Tab 03 spaces table: rows from logs. Before cell: `…{before}<b>{match}</b>{after}…` — but need escaping. I'll render before/match/after as text with match in a span. After cell: before + match-with-inserted-space-marked + after. To build "after" from match: apply the rule's replacement to the match: e.g. sentence: match "s.K" → "s. K" with the space marked. I can compute: pieces = rule.pieces(match) → join text = repaired match; html = pieces with marked space wrapped. So After cell = esc(before) + repairedMatchHtml + esc(after). Before cell = esc(before) + `<span class="m">` + esc(match) + `</span>` + esc(after). Add ellipses if truncated (before/after are 20 chars, may be cut mid-word — fine, add "…" when before doesn't start at 0 / after doesn't reach end; simpler: always wrap with "…" if length==20). I'll add … when before.length===20 and after.length===20.

Clicking a row: go to tab 02, expand that paragraph's detail, scroll into view, maybe flash. Implement `openParagraph(n)`.

Rule counts above table: "sentence join: n · comma join: n · quote join: n · dash join: n" as monospace line.

Characters table: rows:
- En dash – (U+2013): count, example (context from a paragraph)
- Double quotes “ ” (U+201C/201D): count total, example
- Right single quote ’ (U+2019): count, example
- Non-breaking hyphen ‑ (U+2011): count, example
- Non-breaking space (U+00A0): count, example

Example: find first paragraph text containing char, show ~20 chars context. For NBSP example, show with visible marker? Example cell: `…business‑related…` — the nbsp example would be invisible; I'll render example with the special char wrapped in a span with dotted underline, and for NBSP show "⍽"? Better: show context with the char highlighted via `<mark class="ch">` and add a note. For NBSP, replace displayed char with "␣"? That changes verbatim... it's an example display, fine to highlight. I'll wrap the char in `<span class="hl">` with background. For NBSP the span shows a visible space — add CSS `.hl{background:#e8d9a8}` hmm accent is red-only... "Other colours only where a category needs one." Highlight can be a thin underline. I'll use `border-bottom:1px solid` + background subtle. Keep simple: `<mark class="ch">` with background #ead9c2? Let me just use a light red tint background rgba(155,35,53,.12). OK.

Counting over "all paragraph texts" — I'll count over `text` (repaired). Note repairs insert regular spaces, don't affect these chars.

Checks panel lines (tab 04), each: name, compared values, status:
1. Paragraph count — "found n · reference m" — pass/fail.
2. Numbering — "1–n in order, no gaps or duplicates" or list issues — pass/fail.
3. First words — "n of m match; mismatches: para. 13, …" — fail if any mismatch (link to tab 02 rows). If no reference: "not run".
4. Footnotes — "0 in this HTML · reference m" — source limit.
5. Repairs — "n spaces restored in n paragraphs (sentence a, comma b, quote c, dash d); text_raw keeps the text as found" — pass (informational). Status "pass"? It's a count, not pass/fail — I'll mark "pass" with the counts, or "recorded". Plan: every check one line with pass/check failed/source limit. Repairs check: pass when every repair is listed on tab 03 (they are). I'll say pass.
6. Headings — "n headings (x h2, y h3), z glued labels separated" — pass.
7. Nothing lost — "n block elements classified: cover a, committee b, title c, headings d, paragraphs e, unclassified f" — pass if f===0 and sum===total.
8. Export round trip — "JSON parsed back: n records = n rows in tab 02" — pass.

If reference missing: checks 1,3,4 show "not run" (footnotes: "source limit"? Without reference we don't know footnotes count — plan says if reference missing, checks that need it show "not run". Footnote check needs reference → "not run". But we know HTML has 0 footnotes... the check compares 0 vs reference.footnotes; without reference → "not run". OK.)

Header status: passes / total (excluding source-limit and not-run?). Plan: "n of m checks pass" or "n checks failed", then "1 source limit". I'll compute m = checks that ran (pass+fail), sourceLimits counted separately. If failures>0 → red "X checks failed" else green "n of m checks pass". Then "· 1 source limit" if any.

Rail "n of m checks pass" link → tab 04.

Now, "no model was called" footer line: "Done by this page's code; no model was called and nothing left the browser."

Credits line: sources consulted — The Turing Way (CC BY 4.0), UK Government Analysis Function QA of code (Open Government Licence? The best-practice-and-impact repo is OGL v3 — actually it's under Open Government Licence). Dag Hammarskjöld Library Ask DAG — not a code licence. The rule: "If you use code or wording from a 'Reference shelf excerpts' page that has an open licence (MIT, Apache, BSD, ISC, CC BY), add a small 'Credits' line". The Turing Way is CC BY 4.0. I'll add: "Credits: methods follow The Turing Way, 'Documentation and metadata' (CC BY 4.0); UK Government Analysis Function, 'Quality assurance of code for analysis and research: Testing code' (Open Government Licence v3.0); citation format per Dag Hammarskjöld Library, Ask DAG." Good.

Now sizes: keep under 1500 lines. Let's write carefully.

Let me also handle: `WORKSHOP_DATA.html_doc` might be array (per sample) or object. Normalize.

Also `reference.first_words` keyed by string paragraph number.

Edge: html yields no `<p>` → tab 01 says so, exports disabled.

Let me draft the HTML structure:

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>…</title>
<style>…</style>
</head>
<body>
<header>
  <div class="kicker">UN DOCUMENT · HTML</div>
  <h1 id="docTitle"></h1>
  <p class="meta"><a id="symLink"></a> · adopted <span id="adopted"></span> · <span id="srcLine"></span>
    <span class="status" id="statusRight"></span>
  </p>
</header>
<div class="layout">
  <aside class="rail">…</aside>
  <main>
    <div class="tabs" role="tablist">…4 buttons…</div>
    <section id="panel-1" role="tabpanel">…tiles…</section>
    <section id="panel-2" role="tabpanel" hidden>…</section>
    <section id="panel-3" role="tabpanel" hidden>…</section>
    <section id="panel-4" role="tabpanel" hidden>…</section>
  </main>
</div>
<footer>…</footer>
<script>…</script>
</body>
</html>
```

Header status on the right: put in meta line with float/flex. I'll make header a flex? Keep simple: meta line contains left part and a right-floated status span.

CSS plan:

```css
:root{--paper:#f4f0e8;--ink:#1d1b18;--rule:#d9d2c3;--red:#9b2335;--green:#1e6b3a;}
*{box-sizing:border-box}
[hidden]{display:none!important}
body{margin:0;background:var(--paper);color:var(--ink);font:16px/1.55 -apple-system,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif;padding:0 28px 40px}
.mono{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:11.5px;letter-spacing:.12em;text-transform:uppercase}
header{border-bottom:1px solid var(--rule);padding:22px 0 14px}
h1{font-family:Georgia,"Times New Roman",serif;font-weight:400;font-size:30px;margin:6px 0 8px;line-height:1.2}
a{color:var(--red)}
...
.layout{display:grid;grid-template-columns:250px 1fr;gap:32px;align-items:start}
.rail{position:sticky;top:16px;border-right:1px solid var(--rule);padding:18px 18px 18px 0}
```

Tabs:
```css
.tabs{display:flex;gap:4px;border-bottom:1px solid var(--rule);margin-top:18px}
.tabs [role=tab]{background:none;border:none;border-bottom:2px solid transparent;padding:10px 14px;cursor:pointer;font-family:ui-monospace,...;font-size:11.5px;letter-spacing:.12em;color:var(--ink)}
.tabs [role=tab][aria-selected=true]{color:var(--red);border-bottom-color:var(--red)}
:focus-visible{outline:2px solid var(--red);outline-offset:2px}
```

Tiles:
```css
.tiles{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:0 28px;margin-top:20px}
.tile{border-top:1px solid var(--rule);padding:14px 0}
.bignum{font-family:Georgia,serif;font-size:52px;line-height:1}
```

Tables:
```css
table{border-collapse:collapse;width:100%;margin:10px 0 24px}
caption{font-family:Georgia,serif;font-size:19px;text-align:left;padding:6px 0;caption-side:top}
th{font-family:mono small; text-align:left;border-bottom:1px solid var(--ink);...}
td{border-bottom:1px solid var(--rule);padding:8px 10px;vertical-align:top}
td.num,th.num{text-align:right}
```

Rows as buttons: main row `tr.prow{cursor:pointer}` with td containing button for number. Detail row `tr.drow td{background:...}` maybe subtle.

mark.rep: `background:transparent;border:1px solid var(--red);padding:0 1px` — "thin red box". mark.ch similar.

Chips: not needed (no filters here — rail has no filters; plan's rail is document card, not filters. The general layout rule about filters applies "if the app has any" — this app has none. Fine.)

Now the JS. Let me write it fully.

```js
(function(){
"use strict";
const W = window.WORKSHOP_DATA || {};
let D = W.html_doc;
if (Array.isArray(D)) D = D[0] || {};
const REF = D.reference || null;
const SYMBOL = D.symbol || "";
const DOC_URL = D.doc_url || "";
const TITLE = D.title || "(untitled)";
const SOURCE = D.source || "";
const BUILT = D.built || "";

// parse
let root = null;
try { root = new DOMParser().parseFromString(D.html || "", "text/html"); } catch(e){ root = null; }
const body = root ? root.body : null;

const RULES = [
 {name:"sentence join", re:/([a-z])\.([A-Z])/g, rep:(a,b)=>a+". "+b, pieces:m=>[[m[1]+".",0],[" ",1],[m[2],0]]},
 {name:"comma join", re:/([a-z]),([A-Za-z])/g, rep:(a,b)=>a+", "+b, pieces:m=>[[m[1]+",",0],[" ",1],[m[2],0]]},
 {name:"quote join", re:/([a-z])“/g, rep:(a)=>a+" “", pieces:m=>[[m[1],0],[" ",1],["“",0]]},
 {name:"dash join", re:/–([A-Za-z])/g, rep:(a)=>"– "+a, pieces:m=>[["–",0],[" ",1],[m[1],0]]}
];
```

Wait — pieces uses match groups; in exec, m[1], m[2] are groups. Good.

Pipeline:

```js
const elements = []; // {tag, cls, text, kind, ...}
const paragraphs = []; // {num, raw, text, parts, section, part, path, firstMatch, repairs:[]}
const headings = []; // {level, label, heading, full, glued}
let coverCount=0, committee=null, titleEl=null, unclassified=[];
let curPart=null, curSection=null;

if (body) {
  for (const el of body.children) {
    const tag = el.tagName;
    const text = (el.textContent||"").replace(/\s+/g," ").trim();
    if (tag === "TABLE") { coverCount++; elements.push({tag, cls:el.className||"", text, kind:"cover"}); continue; }
    if (tag === "P") {
      const m = text.match(/^(\d{1,3})\.\s*(.*)$/s);
      if (m) {
        const num = parseInt(m[1],10);
        const raw = m[2].trim().replace(/\s+/g," ");
        // repairs pass 1 (plain + logs)
        const logs = [];
        let text = raw;
        for (const r of RULES) text = applyPlain(text, r, num, logs);
        // pass 2 marked parts
        let parts = [{t:raw, mk:false}];
        for (const r of RULES) parts = applyMarked(parts, r);
        const p = {num, raw, text, parts, logs, section: curSection, part: curPart,
                   firstMatch: null, firstFound: null};
        paragraphs.push(p);
        elements.push({tag, cls:el.className||"", text: raw.slice(0,80), kind:"paragraph", num});
      } else {
        if (!committee) committee = text;
        elements.push({tag, cls:el.className||"", text: text.slice(0,80), kind:"committee"});
      }
      continue;
    }
    if (tag === "H2" || tag === "H3") {
      if (tag === "H2" && !titleEl) { titleEl = text; elements.push({tag, cls:"", text:text.slice(0,80), kind:"title"}); continue; }
      const hm = text.match(/^([IVX]+|[A-Z])\.\s*(.+)$/s);
      let label=null, heading=text, glued=false;
      if (hm) { label=hm[1]; heading=hm[2].trim(); glued = !/\s/.test(text.slice(label.length+1, label.length+2)); }
      // glued: char right after "." is not whitespace
      const h = {level:tag, label, heading, full:text, glued};
      headings.push(h);
      if (tag==="H2" && label && /^[IVX]+$/.test(label)) curPart = h;
      curSection = h;
      elements.push({tag, cls:el.className||"", text:text.slice(0,80), kind:"heading"});
      continue;
    }
    unclassified.push({tag, text});
    elements.push({tag, cls:el.className||"", text:text.slice(0,80), kind:"unclassified"});
  }
}
```

Hmm glued detection: text like "I.Introduction" — label "I", after "." comes "I" (not whitespace) → glued. "D. Obligation" — after "." is " " → not glued. Compute: `const afterDot = text.charAt(label.length+1); glued = afterDot !== "" && !/\s/.test(afterDot);` Good.

Wait, but the regex `^([IVX]+|[A-Z])\.\s*(.+)$` on "I.Introduction": `[IVX]+` greedy matches "I", then `\.` matches ".", `\s*` matches "", `(.+)` = "Introduction". Good. On "IV. Foo": label "IV". On "Right to work (art. 6)": starts "R" then "ight" — `[A-Z]\.` needs "." right after R — "Ri" no. `[IVX]+` — "R" not in IVX. So no match → plain heading. Good. But careful: heading "A. Something" — label "A". And what about h2 like "II. General remarks"? fine.

Edge: what if a heading is like "X. Something" where X roman — fine.

But wait: what about h3 lettered "D. Obligation" — label "D" matches `[A-Z]`. Good.

applyPlain:

```js
function applyPlain(str, rule, num, logs){
  return str.replace(rule.re, function(m){
    const args = Array.prototype.slice.call(arguments,1);
    const offset = args[args.length-2];
    logs.push({para:num, rule:rule.name, match:m,
      before:str.slice(Math.max(0,offset-20),offset),
      after:str.slice(offset+m.length, offset+m.length+20)});
    return rule.rep.apply(null, args.slice(0,-2));
  });
}
```

applyMarked:

```js
function applyMarked(parts, rule){
  const out=[];
  for (const p of parts){
    if (p.mk){ out.push(p); continue; }
    let last=0, m; rule.re.lastIndex=0;
    while((m=rule.re.exec(p.t))!==null){
      out.push({t:p.t.slice(last,m.index), mk:false});
      const pieces = rule.pieces(m);
      for (const pc of pieces) out.push({t:pc[0], mk:!!pc[1]});
      last = m.index + m[0].length;
      if (m[0].length===0) rule.re.lastIndex++;
    }
    out.push({t:p.t.slice(last), mk:false});
  }
  return out;
}
```

Note: rule.re with /g used in exec loop — reset lastIndex before each part. Done.

Then text from parts: `p.text = p.parts.map(x=>x.t).join("")` — but I computed text in pass 1; they should be identical. I'll set text from parts to guarantee consistency: after pass 2, `p.text = parts.map(...).join("")`. And pass-1 text used only for logs... Actually simpler: compute parts first, then text = join, and logs from pass 1. Both passes identical. I'll just derive text from parts and keep pass 1 for logs. Or skip pass 1 and derive logs in pass 2 (I have m.index within part; context from part text). Let me merge: do pass 2 only, and log there with context from the part text (before = p.t.slice(max(0,m.index-20), m.index), after = p.t.slice(m.index+m[0].length, ...+20)). The context might be limited to part boundaries but parts are large (whole raw initially), fine. Merge into one pass. 

But careful: rule.rep no longer needed. pieces gives both. OK:

```js
function buildParagraph(num, raw){
  const logs=[]; let parts=[{t:raw,mk:false}];
  for (const r of RULES){
    const out=[];
    for (const p of parts){
      if(p.mk){out.push(p);continue;}
      let last=0,m; r.re.lastIndex=0;
      while((m=r.re.exec(p.t))!==null){
        out.push({t:p.t.slice(last,m.index),mk:false});
        const pcs=r.pieces(m);
        for(const pc of pcs) out.push({t:pc[0],mk:!!pc[1]});
        logs.push({para:num, rule:r.name, match:m[0],
          before:p.t.slice(Math.max(0,m.index-20),m.index),
          after:p.t.slice(m.index+m[0].length, m.index+m[0].length+20)});
        last=m.index+m[0].length;
        if(m[0].length===0) r.re.lastIndex++;
      }
      out.push({t:p.t.slice(last),mk:false});
    }
    parts=out;
  }
  const text=parts.map(p=>p.t).join("");
  return {num, raw, text, parts, logs};
}
```

Wait — logging inside the while: but if a part is marked (single space), skip. Also note: within one part, exec finds non-overlapping matches left to right — same as replace. Good.

Hmm, one issue: the logs' before/after context is from the part text at that rule stage, which equals the full text at that stage restricted to the part — since parts partition the text, context may be cut at part boundaries. Acceptable ("20 characters each side" — approximately; I'll note nothing). Fine.

First words:

```js
function normWords(s){
  return (s||"").replace(/[“”]/g,'"').replace(/[‘’]/g,"'").replace(/[–—]/g,"-").replace(/\u2011/g,"-").replace(/\u00A0/g," ").trim().replace(/\s+/g," ");
}
function firstSix(s){ return normWords(s).split(" ").slice(0,6).join(" "); }
```

Hmm: normWords then split — but first six words of text: split raw text on whitespace then normalize each? Plan: "The first six whitespace-separated words of `text` against reference.first_words: equal after turning curly quotes straight...". So take first six words of text (split on /\s+/), join, then normalize both sides and compare. If I normalize first then split, NBSP becomes space and could merge/split words differently. E.g. text "a\u00A0b c..." — first six whitespace-separated words: does \s match \u00A0 in JS? Yes, \s includes \u00A0. So split on /\s+/ treats NBSP as separator already. So: `text.split(/\s+/).filter(Boolean).slice(0,6).join(" ")` then normWords both. Let me do:

```js
function firstSix(s){ const w=(s||"").split(/\s+/).filter(Boolean).slice(0,6).join(" "); return normWords(w); }
```

Compare firstSix(p.text) === firstSix(REF.first_words[String(p.num)]).

Characters count over all paragraph texts:

```js
const CHARS=[
 {name:"En dash", ch:"–", code:"U+2013"},
 {name:"Double quotes", chs:["“","”"], code:"U+201C / U+201D"},
 {name:"Right single quote", ch:"’", code:"U+2019"},
 {name:"Non-breaking hyphen", ch:"‑", code:"U+2011"},
 {name:"Non-breaking space", ch:"\u00A0", code:"U+00A0"}
];
```
Count over concatenated text of all paragraphs. Example: find first paragraph containing, context 20 chars each side with char highlighted.

Checks computation:

```js
const checks=[]; // {name, detail, status: 'pass'|'fail'|'limit'|'notrun', link}
```

1. Paragraph count: if REF: found=paragraphs.length, expected=REF.paragraphs; status pass if equal else fail; detail "found n · reference m". else notrun "no reference in this file".
2. Numbering: nums = paragraphs.map(p=>p.num); issues: duplicates and gaps relative to 1..max. If REF, also compare max vs REF.paragraphs? Plan: "Exactly 1 to n in order" — n here likely reference.paragraphs or found count. I'll check sequence equals [1..paragraphs.length] (i.e., sorted, no gaps/dups within found) AND if REF, found count equals REF.paragraphs (that's check 1). Numbering check: expected sequence 1..(REF? REF.paragraphs : paragraphs.length); compare. List gaps/duplicates. status pass/fail. If no paragraphs → fail? If REF missing → notrun? Numbering doesn't need REF if we check 1..found.length. I'll run it regardless: expected = REF? REF.paragraphs : paragraphs.length.
3. First words: if REF && REF.first_words: mismatches list; status pass if 0 else fail with "para. n: found '…' / reference '…'". else notrun.
4. Footnotes: if REF: status 'limit', detail "0 in this HTML · reference has m — the HTML version has no footnotes: a limit of the source, not of the app". else notrun.
5. Repairs: total logs count, per-rule counts, paragraphs affected; status pass; detail.
6. Headings: h2count (non-title), h3count, glued count; pass.
7. Nothing lost: total elements = elements.length; classified = cover+committee+title+headings+paragraphs+unclassified... unclassified are "classified as unclassified" — check: every element has a kind; sum of kinds === total; unclassified.length===0 → pass else fail listing them.
8. Export round trip: build JSON string, parse, length === paragraphs.length → pass. Run at load.

Export JSON record:

```js
function recordFor(p){
  return {
    symbol: SYMBOL,
    paragraph: p.num,
    section: p.section ? p.section.full : "",
    part: p.part ? p.part.full : "",
    text: p.text,
    text_raw: p.raw,
    first_words_match: p.firstMatch,
    citation: SYMBOL + ", para. " + p.num,
    doc_url: DOC_URL,
    limitations: "no footnotes in this HTML version; the document has " + (REF? REF.footnotes : "an unknown number of") + " footnotes"
  };
}
```

Plan: limitations ("no footnotes in this HTML version; the document has n"). If no REF: "no footnotes in this HTML version". Fine.

Markdown:

```js
function buildMarkdown(){
  const today = new Date().toISOString().slice(0,10);
  const lines=[];
  lines.push("---");
  lines.push("title: " + mdEscape(TITLE));
  lines.push("symbol: " + SYMBOL);
  lines.push("adopted: " + (REF? REF.adopted : ""));
  lines.push("source_url: " + DOC_URL);
  lines.push("extracted: " + today);
  lines.push("paragraphs_found: " + paragraphs.length);
  lines.push("paragraphs_expected: " + (REF? REF.paragraphs : ""));
  lines.push("footnotes: no footnotes in this HTML version" + (REF? "; the document has " + REF.footnotes : ""));
  lines.push("---");
  // body in document order: need ordered stream of headings & paragraphs
  ...
}
```

For document order, I should keep an ordered list of items: during pipeline, push {type:'heading'|'paragraph', ref} into `stream`. Then markdown iterates stream: heading h2 → "## " + full, h3 → "### " + full, paragraph → "\n**" + num + ".** " + text. Title → "# " + titleEl at top? I'll add "# " + TITLE after front matter. Plan didn't mention; harmless and useful. Actually plan says "then the headings as ## and ### lines in document order and each paragraph as its number in bold, then its text" — I'll include title as `#` line; it's the document title. OK.

mdEscape: minimal — just output raw (titles may contain colons; YAML-ish front matter — quote values: `title: "..."` with quotes escaped). I'll wrap in double quotes and escape backslashes/quotes.

Download:

```js
function download(name, text, mime){
  const blob = new Blob([text], {type: mime+";charset=utf-8"});
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href=url; a.download=name; document.body.appendChild(a); a.click();
  setTimeout(()=>{URL.revokeObjectURL(url); a.remove();}, 500);
}
```

File name: SYMBOL.replace(/\//g,"-") + ".json" / ".md".

Copy citation:

```js
function copyText(t, btn){
  const done = ok => { btn.textContent = ok? "Copied":"Select & copy"; setTimeout(()=>btn.textContent="Copy citation",2000); };
  if (navigator.clipboard && navigator.clipboard.writeText) {
    navigator.clipboard.writeText(t).then(()=>done(true), ()=>{fallback();});
  } else fallback();
  function fallback(){
    try{
      const ta=document.createElement("textarea"); ta.value=t; ta.style.position="fixed"; ta.style.opacity="0";
      document.body.appendChild(ta); ta.select();
      const ok=document.execCommand("copy"); ta.remove(); done(ok);
    }catch(e){ done(false); }
  }
}
```

Tab switching:

```js
const tabs=[...document.querySelectorAll('[role=tab]')];
function selectTab(i, focus){
  tabs.forEach((t,j)=>{
    const on = i===j;
    t.setAttribute("aria-selected", on?"true":"false");
    t.tabIndex = on?0:-1;
    const panel=document.getElementById(t.getAttribute("aria-controls"));
    if(on){ panel.hidden=false; } else { panel.hidden=true; }
  });
  if(focus) tabs[i].focus();
}
tabs.forEach((t,i)=>{
  t.addEventListener("click",()=>selectTab(i,false));
  t.addEventListener("keydown",e=>{
    let n=null;
    if(e.key==="ArrowRight"||e.key==="ArrowDown") n=(i+1)%tabs.length;
    else if(e.key==="ArrowLeft"||e.key==="ArrowUp") n=(i-1+tabs.length)%tabs.length;
    else if(e.key==="Home") n=0; else if(e.key==="End") n=tabs.length-1;
    if(n!==null){ e.preventDefault(); selectTab(n,true); }
  });
});
```

Roving tabindex: set tabIndex in selectTab. Initially tab 0 selected.

openParagraph(n): selectTab(1,false); find row button for para n, set expanded, show detail, scrollIntoView.

Row rendering (tab 02): build via DOM creation or innerHTML with escaping. I'll build with template strings + esc().

```js
function esc(s){return String(s).replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;").replace(/"/g,"&quot;");}
```

Table body:

```js
tbody.innerHTML = paragraphs.map(p=>{
  const ok = p.firstMatch===null ? "" : (p.firstMatch? '<span class="pass">OK</span>' : '<span class="fail">first words differ</span>');
  const fl = firstLine(p.text);
  return `<tr class="prow" data-num="${p.num}">
    <td class="num"><button class="rowbtn" aria-expanded="false" aria-controls="det-${p.num}" data-num="${p.num}">${p.num}</button></td>
    <td class="sec" title="${esc(p.section?p.section.full:'')}">${esc(p.section?p.section.full:'—')}</td>
    <td class="fl">${esc(fl)}</td>
    <td>${ok}</td>
  </tr>
  <tr class="drow" id="det-${p.num}" hidden><td colspan="4">…detail…</td></tr>`;
}).join("");
```

Detail content:

```js
const marked = p.parts.map(pt=> pt.mk? `<mark class="rep">${esc(pt.t)}</mark>` : esc(pt.t)).join("");
let det = `<div class="fulltext">${marked}</div>`;
if (REF && REF.first_words){
  if(!p.firstMatch) det += `<p class="cmp"><span class="fail">first words differ</span> — found “${esc(p.firstFound)}” · reference “${esc(firstSix(REF.first_words[String(p.num)]))}”</p>`;
  else det += `<p class="cmp pass">first six words match the reference</p>`;
}
if(p.logs.length){ det += `<p class="mono">repairs in this paragraph: ${p.logs.map(l=>esc(l.rule)).join(", ")}</p>`; }
det += `<p class="path mono">path: ${esc(pathOf(p))}</p>`;
det += `<button class="copybtn" data-cite="${esc(p.citation)}">Copy citation</button> <span class="mono cite">${esc(p.citation)}</span>`;
```

pathOf: part.full + " › " + section.full (if both), else whichever.

Event delegation: tbody click on .rowbtn or .prow → toggle. Toggle: btn aria-expanded, det row hidden toggle.

```js
tbody.addEventListener("click", e=>{
  const btn = e.target.closest(".rowbtn");
  if(!btn) return;
  const tr = btn.closest("tr"); const det = document.getElementById(btn.getAttribute("aria-controls"));
  const open = btn.getAttribute("aria-expanded")==="true";
  btn.setAttribute("aria-expanded", String(!open));
  det.hidden = open;
});
```

Also clicking anywhere on prow triggers btn: add `tr.addEventListener`? With delegation: if e.target.closest(".prow") && !btn → btn = row.querySelector(".rowbtn"); btn.click(). I'll handle: 

```js
tbody.addEventListener("click", e=>{
  const row = e.target.closest("tr.prow");
  if(!row) return;
  const btn = row.querySelector(".rowbtn");
  btn.click();
});
```
And btn click handled by same listener? btn is inside prow, so closest("tr.prow") catches it too — but then btn.click() would recurse. Use: if target is the button itself, handle toggle; else find button and toggle directly. Simpler:

```js
tbody.addEventListener("click", e=>{
  const row = e.target.closest("tr.prow"); if(!row) return;
  const btn = row.querySelector(".rowbtn");
  const det = document.getElementById(btn.getAttribute("aria-controls"));
  const open = btn.getAttribute("aria-expanded")==="true";
  btn.setAttribute("aria-expanded", String(!open));
  det.hidden = open;
});
```
Clicking button bubbles to tbody → handled once. Good. Copy buttons are in detail rows, not prow — fine.

Tab 03 spaces table rows clickable: `tr.srow data-num` → click → openParagraph(num).

```js
spBody.addEventListener("click", e=>{
  const tr=e.target.closest("tr.srow"); if(!tr) return;
  openParagraph(parseInt(tr.dataset.num,10));
});
```

openParagraph:

```js
function openParagraph(n){
  selectTab(1,false);
  const btn=document.querySelector(`.rowbtn[data-num="${n}"]`);
  if(!btn) return;
  const det=document.getElementById(btn.getAttribute("aria-controls"));
  btn.setAttribute("aria-expanded","true"); det.hidden=false;
  btn.closest("tr").scrollIntoView({block:"center"});
}
```

Headings box (tab 02): button aria-expanded toggles a div listing headings:

```html
<button class="boxbtn" aria-expanded="false" aria-controls="headingsBox">Headings found: n</button>
<div id="headingsBox" hidden><ol>…</ol></div>
```

Each heading li: `<span class="mono">H2</span> IV. Introduction` — display full text; if label, show `label. heading`? full already contains it. Show full.

Elements found box (tab 04): button "Elements found (n)" aria-expanded, table Tag | Classified as | Text (first 80 chars). Rows from elements array.

Checks panel (tab 04): list of lines:

```html
<ul class="checks">
 <li><span class="pass">pass</span> Paragraph count — found 90 · reference 90</li>
 <li><span class="fail">check failed</span> First words — 6 of 90 differ: para. 13 … (<a href="#" data-tab="1">see tab 02</a>)</li>
 <li><span class="limit">source limit</span> Footnotes — 0 in this HTML · reference 141 …</li>
</ul>
```

Links to tab 02: `<button class="linkbtn" data-goto="1">tab 02</button>` — handle clicks: any [data-goto] → selectTab(n,true).

Header status: compute passes/fails/limits/notrun. m = pass+fail (checks that ran). If fail>0: red dot + `${fail} check${s} failed`; else green dot + `${pass} of ${m} checks pass`. Then `· ${limits} source limit` (red text) if limits>0. If no reference and nothing ran: "checks not run".

Rail: 
```html
<aside class="rail">
 <div class="mono railhead">Document</div>
 <div class="doccard">
   <div class="mono sym">E/C.12/GC/27</div>
   <div class="doctitle">General comment No. 27 (2025) …</div>
 </div>
 <div class="railnum"><span class="bignum" id="railP">90</span> <span class="of">of 90 paragraphs</span><div class="bar"><div class="barfill" id="railBar"></div></div></div>
 <div class="railnum"><span class="bignum red" id="railF">0</span> <span class="of">of 141 footnotes</span><div class="note red">not in this HTML</div></div>
 <button class="linkbtn mono" data-goto="3">n of m checks pass</button>
</aside>
```

Bar: width = min(100, n/expected*100)%; red if n!==expected else ink/green? "thin bar (red when short or over)" — fill color red when mismatch, else ink (#1d1b18) or green. I'll use ink when equal, red otherwise. Hmm green reserved for pass words; bar fill: use var(--ink) when equal, red when not.

Tab 01 tiles:

```html
<div class="tiles">
 <div class="tile"><div class="mono">Paragraphs found</div><div class="bignum" id="tP">90</div><div class="of">the document has 90</div><p class="how">How this is computed: every <code>&lt;p&gt;</code> whose text starts “n.” in the parsed HTML, counted once.</p></div>
 ...
</div>
```

Tile 1: big n, beside "the document has m" — green when equal, red with difference ("+2"/"−3"). If no REF: "no reference in this file".
Tile 2: "First words match: n of m" — big number n, "of m". If no REF: "no reference in this file".
Tile 3: "Footnotes: 0 of m" red, "this HTML version has none; see tab 03" (link data-goto=2). If no REF: "0 footnotes in this HTML".
Tile 4: "Spaces: n repaired or flagged" link to tab 03. How line: rules listed.

If no paragraphs found: tab 01 shows a message "The HTML yielded no numbered paragraphs" and exports disabled (buttons disabled attribute).

Export buttons disabled when paragraphs.length===0.

Now header meta line: `symbol` linked: `<a href=DOC_URL target=_blank rel="noopener">E/C.12/GC/27</a> · adopted 6 November 2025? ` — reference.adopted value unknown; just print REF.adopted. · source. Right: status.

Footer: `SOURCE` + (BUILT? " · built "+BUILT) + " · Done by this page's code; no model was called and nothing left the browser." Plus credits line.

Wait — does html_doc have `built`? Description doesn't list it. I'll include if present.

Also title of the page `<title>`: SYMBOL + " paragraphs".

Now, "TAB.01" monospace numbers on tables: I'll add a `<div class="mono fig">TAB.02 · PARAGRAPHS</div>` above each table.

Let me also double check the paragraph regex against text with newlines: I collapse whitespace in text first: `text = el.textContent.replace(/\s+/g," ").trim()`. Then match `/^(\d{1,3})\.(.*)$/` — after collapsing, `\s*` unnecessary but keep `/^(\d{1,3})\.\s*(.*)$/`. Note: "1.A clean" → m[2]="A clean...". Good. But careful: a p like "6 November 2025" — inside table, not iterated (we iterate body.children; table is one child). Good.

But wait: what about `<div class="content">` — body.children includes the table and the div.content! The sample HTML: `<body><table>…</table><div class="content">…</div></body>`. So body.children = [table, div]. I must iterate recursively into divs, or iterate all block elements in document order. Plan says "over the parsed document's body elements in order" — but the content is inside div.content. I'll flatten: walk all descendants, collecting block-level elements (P, H1-H6, TABLE, DIV?) in document order. Better: collect elements matching 'p, h1, h2, h3, h4, h5, h6, table, ul, ol, div' — but div.content itself would be an element. Hmm.

Approach: iterate `body.querySelectorAll("*")` and pick block elements: P, H2, H3, H1, H4..., TABLE. Skip elements nested inside a table (cover). Since table is cover, skip its descendants. Implementation:

```js
const blocks=[];
(function walk(node){
  for(const el of node.children){
    const tag=el.tagName;
    if(tag==="TABLE"){ blocks.push(el); continue; } // don't descend
    if(/^H[1-6]$/.test(tag) || tag==="P"){ blocks.push(el); continue; }
    walk(el); // divs etc.
  }
})(body);
```

This gives table, then p (committee), h2 title, h2, p, p... in order. 

But "Nothing lost: every block element is classified exactly once" — with this walk, divs are traversed not classified. The elements table (tab 04) lists "every block element in order" — the blocks list. Divs aren't listed; acceptable? Plan says "every block element in order, Tag | Classified as | Text". I'll list the blocks I classify (table, p, h2, h3). Divs are containers. To be safe, I could include divs as "container (traversed)" — nah, keep blocks = table/p/h*. The check "counts per class sum to the total" uses blocks.length. Fine.

Hmm, but what if there are other elements like `<ul>`? walk descends into them but their `<li>` children aren't collected... li is block-ish. Add LI to the collected set? If a li exists it'd be unclassified. I'll collect P, H1-H6, TABLE, LI, BLOCKQUOTE, PRE as blocks; others traversed. Unclassified ones get listed. Good.

Now classification of H1/H4-H6: treat like headings (any H* except first H2 as title). Plan only mentions h2/h3; I'll treat H1/H4+ as headings too (level recorded). Title = first H2 specifically per plan; if no H2, first heading is title? Plan says first h2 is title. Keep: first H2 → title; other headings → headings.

Wait, actually in this doc the title is an h2 and there are 6 more h2s. Good.

Now section/part assignment: curSection updates on every heading (h2/h3). curPart updates only on h2 with roman label. But what if part h2 has no roman label (plain h2)? Then part stays previous. Fine.

Edge: paragraphs before any heading → section null → display "—".

Now firstLine: first 120 chars cut at word:

```js
function firstLine(t){
  if(t.length<=120) return t;
  let cut=t.slice(0,120);
  const sp=cut.lastIndexOf(" ");
  if(sp>0) cut=cut.slice(0,sp);
  return cut+"…";
}
```

Now counts for tab 03 rule line: per rule counts from all logs.

Characters examples: 

```js
function charExample(allText, test){
  const i = allText.search(test); // test regex
  if(i<0) return null;
  const ch = allText.slice(i).match(test)[0];
  ...
}
```
Simpler per char: find index via indexOf for single chars; for quotes pair, find first of either. Build example: context 18 chars each side, highlight the char(s). For NBSP, highlight shows blank — add title attr. I'll render example as: esc(before) + `<mark class="ch">` + esc(displayChar) + `</mark>` + esc(after), where for NBSP displayChar = "␣"? That misrepresents. I'll keep the actual char in the mark and add CSS `.ch{background:rgba(155,35,53,.15); outline:1px dotted var(--red)}` so NBSP is visible as a highlighted gap. Good.

allText = paragraphs.map(p=>p.text).join("\n").

Counts: en dash count = (allText.match(/–/g)||[]).length; double quotes = “ + ” counts; ’ ; ‑ ; \u00A0.

Now checks details:

Check 3 first words: for each p, if REF && REF.first_words: ref = REF.first_words[String(p.num)]; if ref undefined → mismatch? If reference lacks that key, treat as "no reference entry" — count as not checked. I'll only compare when ref exists; p.firstMatch = (firstSix(p.text) === firstSix(ref)). If ref missing, firstMatch = null → display "no reference entry"? Keep simple: if ref missing, firstMatch=null and check column shows "—". Mismatch list for check line: paras where firstMatch===false.

Check 2 numbering: 
```js
const nums = paragraphs.map(p=>p.num);
const dups = nums.filter((n,i)=>nums.indexOf(n)!==i);
const expected = REF? REF.paragraphs : (paragraphs.length||0);
let gaps=[]; 
if(paragraphs.length){
  const max=Math.max(...nums);
  for(let k=1;k<=max;k++) if(!nums.includes(k)) gaps.push(k);
}
const okNum = dups.length===0 && gaps.length===0 && nums.length===expected && nums.every((n,i)=>n===i+1);
```
Hmm "exactly 1 to n in order" — nums[i]===i+1 covers order+gaps. dups covered. Also nums.length===expected ties to reference. I'll compute okNum = nums.length===expected && nums.every((n,i)=>n===i+1). Detail: "found 1–90 in order" or list "gaps: …; duplicates: …; count 88 vs 90".

Check 7 nothing lost: kinds count: cover, committee, title, heading, paragraph, unclassified. total=blocks.length. ok = unclassified.length===0 && sum===total (trivially true) — the real check: every block got a kind (always true by construction) — so check is: unclassified.length===0. Detail: "n block elements: 1 cover, 1 committee line, 1 title, 30 headings, 90 paragraphs, 0 unclassified". pass if 0 unclassified.

Check 8 export round trip: jsonStr = JSON.stringify(records); parsed = JSON.parse(jsonStr); ok = parsed.length===paragraphs.length. Run at load; detail "JSON parsed back: n records = n rows on tab 02".

Check 5 repairs: total logs; per rule; distinct paragraphs. status pass. detail: "n spaces restored in m paragraphs (sentence join a · comma join b · quote join c · dash join d); text_raw keeps the text as found".

Check 6 headings: h2 = headings.filter(h=>h.level==="H2").length etc; glued = headings.filter(h=>h.glued).length. pass.

Check 1: pass/fail. Check 4: limit.

Header/rail status: passes = checks.filter(c=>c.status==="pass").length; fails; limits; notrun. m = passes+fails. If m===0 → "checks not run". Else if fails>0 → red "X checks failed" else green "P of M checks pass". Plus "· L source limit" if L>0 (red). Plan: 'then "1 source limit"'. I'll show `${limits} source limit${s}`.

Rail link text: same "n of m checks pass" (or "checks: see tab 04" if not run). data-goto=3.

Now tab 01 tiles when REF missing: tile1: big n + "no reference in this file"; tile2: "no reference in this file"; tile3: "0" red + "footnotes in this HTML — no reference to compare"; tile4 normal.

If paragraphs.length===0: tab 01 shows a notice "The parsed HTML yielded no numbered paragraphs — exports are disabled." and tiles show zeros; export buttons disabled.

Now write the CSS more concretely. Also responsive: grid collapses to single column under 900px.

Focus ring: `:focus-visible{outline:2px solid var(--red); outline-offset:2px}`.

Buttons: `.linkbtn{background:none;border:none;color:var(--red);cursor:pointer;text-decoration:underline;font:inherit;padding:0}`.

Row buttons: `.rowbtn{background:none;border:none;font:inherit;font-family:Georgia,serif;font-size:18px;color:var(--red);cursor:pointer;padding:2px 6px}` — paragraph numbers in red serif per design ("Red accent on ... the paragraph numbers").

Detail row: `tr.drow td{background:#efe9dd;border-bottom:2px solid var(--rule)}` maybe. Full text: `.fulltext{font-size:16px;max-width:70ch}`.

mark.rep: `background:transparent;border:1px solid var(--red);border-radius:2px;padding:0 1px;` — thin red box around inserted space. A space with border box — visible. Good.

mark.ch: `background:rgba(155,35,53,.14);outline:1px dotted var(--red);`.

pass: `.pass{color:var(--green);font-weight:600}` fail: `.fail{color:var(--red);font-weight:600}` limit: `.limit{color:var(--red);font-weight:600}` — plan says "source limit" in red. Words as well as colours: text literally "pass", "check failed", "source limit".

Dot: `.dot{display:inline-block;width:9px;height:9px;border-radius:50%;margin-right:6px}` `.dot.ok{background:var(--green)}` `.dot.bad{background:var(--red)}`.

Big numbers: `.bignum{font-family:Georgia,serif;font-size:52px;line-height:1;font-weight:400}`.

Rail bar: `.bar{height:3px;background:var(--rule);margin-top:6px}.barfill{height:100%;background:var(--ink)}.barfill.bad{background:var(--red)}`.

Tabs styling as above. Panels: `main{min-width:0}`.

Table: caption serif 19px; th mono 11px uppercase letter-spacing, border-bottom 1px solid ink; td border-bottom rule; padding 8px 10px; `.num{text-align:right;font-variant-numeric:tabular-nums}`.

Section cell: max-width with ellipsis: `.sec{max-width:220px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}`.

First line cell: max-width 46ch.

OK, also "How this is computed" lines: `.how{font-size:13px;color:#5a554b;margin:8px 0 0}` — hint color must keep contrast ≥4.5: #5a554b on #f4f0e8 — contrast? #5a554b is darkish gray-brown, should be ~7:1. Fine.

Mono hints: `.hint{font-family:mono;font-size:11.5px;letter-spacing:.08em;color:#5a554b;text-transform:uppercase}` — plan says short monospace hints next to what they explain. For lowercase hints like "click = filter" — I'll not uppercase everything; use a `.mono` class without uppercase for inline hints, and `.kicker` uppercase for labels. Let me define `.mono{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:11.5px;letter-spacing:.1em}` and `.up{text-transform:uppercase}`.

Now assemble everything. Also the "Elements found" table: Tag | Classified as | Text (first 80 chars). Text: I stored text.slice(0,80) at classification — but for paragraphs I stored raw.slice(0,80). Fine.

Classified as values: "cover", "committee line", "title", "heading (H2)" etc., "paragraph 12", "unclassified".

Let me now also handle the tab-03 "Lost: footnotes" block text exactly-ish: "The document has {m} footnotes. This HTML has 0: no footnote text, no footnote marks, and the note the title's asterisk points to is missing. To cite a footnote, use the PDF or Word version." If no REF: "This HTML has 0 footnotes: no footnote text and no footnote marks." 

Changed: spaces intro: count per rule line + table. Note under: "Rules restore a space only where the characters prove it was there. Word pairs such as 'Giventhe' are not touched; the first-words check catches them only in a paragraph's first six words." — the plan literally mentions 'Giventhe' as an example from data; but I shouldn't hard-code data specifics... it's a generic example of the phenomenon; the plan says to include that sentence. It references a real word pair from the data. Since plan explicitly says to write it, include as written (it's illustrative). Hmm, "never hard-code counts, countries, years or names" — 'Giventhe' is a word pair example, plan instructs it. I'll keep the sentence but maybe generalize: "Word pairs such as a missing space inside a word are not touched; the first-words check catches them only in a paragraph's first six words." Safer to follow plan wording though. The plan explicitly quotes the sentence; I'll use it as given — it's from their own analysis. Actually to be safe against data differences, I'll phrase: "Word pairs the rules cannot prove (for example a missing space inside a word) are not touched; the first-words check catches them only in a paragraph's first six words." That's faithful and data-independent. Good.

Changed: characters note: "Kept exactly as published, in the table and in every export. A search for 'business-related' typed with the hyphen key will not find 'business‑related': normalise the text before searching it." — again data-specific example; generalize: "Kept exactly as published, in the table and in every export. A search typed with the keyboard hyphen will not find a non-breaking hyphen, nor straight quotes a curly one: normalise the text before searching it." Good.

Monospace hint next to characters table: "on a keyboard: a hyphen and straight quotes".

Now tab 04 layout: "The check panel, open, every check on one line. Then Export." So:

```html
<section id="panel-4">
  <h2 class="sectitle">Checks</h2>
  <ul class="checks" id="checkList"></ul>
  <h2 class="sectitle">Export</h2>
  <p class="hint">…</p>
  <button id="dlJson">Download JSON</button> <button id="dlMd">Download Markdown</button>
  <p class="how">JSON: one record per paragraph with symbol, paragraph, section, part, text, text_raw, first_words_match, citation, doc_url, limitations. Markdown: front matter + headings + paragraphs. File name: symbol with slashes as hyphens.</p>
  <button class="boxbtn" aria-expanded="false" aria-controls="elemBox">Elements found (n)</button>
  <div id="elemBox" hidden><table>…</table></div>
</section>
```

Buttons styled: `.btn{border:1px solid var(--ink);background:transparent;padding:10px 16px;font:inherit;cursor:pointer}` hover bg. Disabled: opacity .4.

Check line format: `<li><span class="tag pass">pass</span> <strong>Paragraph count</strong> — found 90 · reference 90</li>`. Fail with link: `… (<button class="linkbtn" data-goto="1">tab 02</button>)`.

data-goto handler: document.addEventListener('click', e=>{const g=e.target.closest('[data-goto]'); if(g){selectTab(parseInt(g.dataset.goto,10),true);}});

Now, one more requirement: "Every row that shows a document has its symbol, linked to doc_url in a new tab." Tab 02 rows show paragraphs of the document — the header has the symbol link; also each detail row shows citation with symbol. I'll add in detail row: `<a href=DOC_URL target=_blank>E/C.12/GC/27</a>, para. n`. And in tab 02 caption maybe. Good enough: header link + detail link.

Also "Keep the full text of a paragraph available (click to expand)" — done.

Now let me also compute rail "n paragraphs of m": if REF: `${paragraphs.length} of ${REF.paragraphs}` else just paragraphs.length. Bar width: if REF: min(100, len/REF.paragraphs*100). 

Footnotes rail: "0 of {REF.footnotes}" red + "not in this HTML". If no REF: "0 footnotes in this HTML".

Now, header right status: I'll place `<span class="status">` at end of meta line, floated right via flex: make `.meta{display:flex;justify-content:space-between;gap:16px;flex-wrap:wrap}` with left span and right span.

Let me now write the whole file. I'll be careful with quotes inside template literals in JS (the text contains curly quotes — fine in JS strings).

One concern: `el.textContent` for the title h2 includes " *" at end — fine.

Also the committee line: bold p "Committee on Economic, Social and Cultural Rights" — classified committee. In elements table: "committee line".

Also cover table text: textContent of table includes all cover text collapsed — first 80 chars for the table. Fine.

Let me write markdown builder with stream: during pipeline, push to `stream` array: {type:'heading', h} or {type:'paragraph', p}. Title pushed as {type:'title'}.

Markdown:

```js
function buildMarkdown(){
  const d=new Date(); const today=d.getFullYear()+"-"+String(d.getMonth()+1).padStart(2,"0")+"-"+String(d.getDate()).padStart(2,"0");
  const q=s=>'"'+String(s).replace(/\\/g,"\\\\").replace(/"/g,'\\"')+'"';
  const L=[];
  L.push("---");
  L.push("title: "+q(TITLE));
  L.push("symbol: "+q(SYMBOL));
  L.push("adopted: "+q(REF? String(REF.adopted):""));
  L.push("source_url: "+q(DOC_URL));
  L.push("extracted: "+today);
  L.push("paragraphs_found: "+paragraphs.length);
  L.push("paragraphs_expected: "+(REF? REF.paragraphs : "unknown"));
  L.push("footnotes: "+q("no footnotes in this HTML version"+(REF? "; the document has "+REF.footnotes+" footnotes":"")));
  L.push("---");
  L.push("");
  L.push("# "+TITLE);
  L.push("");
  for(const it of stream){
    if(it.type==="heading"){
      const h=it.h;
      L.push((h.level==="H2"?"## ":"### ")+h.full);
      L.push("");
    } else if(it.type==="paragraph"){
      const p=it.p;
      L.push("**"+p.num+".** "+p.text);
      L.push("");
    }
  }
  return L.join("\n");
}
```

JSON:

```js
function buildJSON(){ return JSON.stringify(paragraphs.map(recordFor), null, 2); }
```

Round-trip check at load: `JSON.parse(buildJSON()).length === paragraphs.length` (guard try/catch).

Now, the "citation" field: SYMBOL + ", para. " + num.

Copy button per detail row: data-cite attr; delegation on tbody for .copybtn:

```js
tbody.addEventListener("click", e=>{
  const cb=e.target.closest(".copybtn");
  if(cb){ copyText(cb.dataset.cite, cb); return; }
  const row=e.target.closest("tr.prow"); ...
});
```

Order: check copybtn first (it's in drow, not prow, so no conflict anyway).

Now tab 03 spaces table: columns Paragraph | Before | After | Rule. num right-aligned. Before: `…` + esc(before) + `<span class="m">` + esc(match) + `</span>` + esc(after) + `…`. After: esc(before) + repairedMatchHtml + esc(after) + "…". repairedMatchHtml from rule pieces: find rule by name. I'll store rule name in log and keep RULES map by name:

```js
const ruleByName={}; RULES.forEach(r=>ruleByName[r.name]=r);
function repairedMatchHtml(log){
  const r=ruleByName[log.rule];
  // recompute pieces from match: need groups — re-exec
  r.re.lastIndex=0; const m=r.re.exec(log.match);
  return r.pieces(m).map(pc=> pc[1]? `<mark class="rep">${esc(pc[0])}</mark>` : esc(pc[0])).join("");
}
```

Careful: exec on log.match with /g regex — reset lastIndex. Since match is a fresh string, fine.

Ellipsis: add "…" prefix if before.length===20, suffix if after.length===20.

Rule counts line above table: `sentence join: 23 · comma join: 8 · quote join: 2 · dash join: 2 — 35 spaces in 24 paragraphs` computed.

Characters table rows with counts and examples.

Now the headings box content: `<ol class="hlist">` items: `<li><span class="mono">H2</span> ${esc(h.full)}</li>`.

Elements table: rows: `<tr><td class="mono">TABLE</td><td>cover</td><td>${esc(text)}</td></tr>` etc. Kind labels: cover→"cover", committee→"committee line", title→"title", heading→"heading (H2)", paragraph→"paragraph "+num, unclassified→"unclassified".

Now header: 

```html
<header>
 <div class="mono up kicker">UN document · HTML</div>
 <h1 id="hTitle"></h1>
 <div class="meta">
   <span class="metaline"><a id="hSym" target="_blank" rel="noopener"></a><span id="hAdopted"></span><span id="hSource"></span></span>
   <span class="status" id="hStatus"></span>
 </div>
</header>
```

Set text via JS: hSym.textContent=SYMBOL; hSym.href=DOC_URL; hAdopted.textContent = REF? " · adopted "+REF.adopted : ""; hSource.textContent=" · "+SOURCE.

Status: `<span class="dot ok"></span>90 of 90 checks pass` etc. Build via innerHTML with spans.

Rail:

```html
<aside class="rail">
  <div class="mono up railhead">Document</div>
  <div class="doccard">
    <div class="mono sym" id="rSym"></div>
    <div class="doctitle" id="rTitle"></div>
  </div>
  <div class="railblock">
    <div><span class="bignum" id="rP"></span> <span class="of" id="rPof"></span></div>
    <div class="bar"><div class="barfill" id="rBar"></div></div>
  </div>
  <div class="railblock">
    <div><span class="bignum red" id="rF">0</span> <span class="of" id="rFof"></span></div>
    <div class="note red">not in this HTML</div>
  </div>
  <button class="linkbtn mono up" data-goto="3" id="rChecks"></button>
</aside>
```

doctitle: short title — use TITLE but CSS line-clamp 3.

OK. Also add `<div class="mono up fig">TAB.01 · RESULT</div>` etc. above each panel content? Plan: tables have monospace figure numbers. I'll add fig labels above tables and tiles sections.

Now, potential pitfall: paragraphs' `text` used for firstLine and display; `raw` for text_raw. Detail shows marked full text (repaired). Also show raw? Plan: expanded row shows "the full text, verbatim, never shortened" — the repaired text with marks is the app's text; raw available in export. I'll show the marked text (which is verbatim + marked insertions) and note "text_raw in the export holds the text exactly as found". Good.

Let me now also make sure: "A closed 'Headings found: n' box above the table lists them, so none can hide inside a paragraph." — implemented.

Time to write the final code. I'll aim for clean, complete, ~700-900 lines.

Also remember: before code block, at most three short sentences saying what I built. After: nothing.

Let me write CSS fully:

```css
:root{--paper:#f4f0e8;--ink:#1d1b18;--rule:#d9d2c3;--red:#9b2335;--green:#1e6b3a;--dim:#5c564a}
*{box-sizing:border-box}
[hidden]{display:none!important}
html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--paper);color:var(--ink);font:16px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif;padding:0 28px 48px}
.mono{font-family:ui-monospace,Menlo,Consolas,"Liberation Mono",monospace;font-size:11.5px;letter-spacing:.1em}
.up{text-transform:uppercase}
a{color:var(--red)}
button{font:inherit;color:inherit}
:focus-visible{outline:2px solid var(--red);outline-offset:2px}
header{border-bottom:1px solid var(--rule);padding:24px 0 16px}
.kicker{color:var(--dim)}
h1{font-family:Georgia,"Times New Roman",serif;font-weight:400;font-size:clamp(24px,3.4vw,34px);line-height:1.2;margin:8px 0 10px;max-width:60ch}
.meta{display:flex;justify-content:space-between;align-items:baseline;gap:18px;flex-wrap:wrap;font-size:14px;color:var(--dim)}
.meta a{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:12.5px;letter-spacing:.06em}
.status{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:11.5px;letter-spacing:.08em;text-transform:uppercase;white-space:nowrap}
.dot{display:inline-block;width:9px;height:9px;border-radius:50%;margin-right:7px;vertical-align:1px}
.dot.ok{background:var(--green)} .dot.bad{background:var(--red)}
.layout{display:grid;grid-template-columns:240px minmax(0,1fr);gap:36px;align-items:start}
.rail{position:sticky;top:20px;border-right:1px solid var(--rule);padding:20px 20px 20px 0}
.railhead{color:var(--dim);border-bottom:1px solid var(--rule);padding-bottom:8px;margin-bottom:14px}
.doccard{border:1px solid var(--rule);padding:12px 14px;margin-bottom:22px}
.sym{color:var(--red)}
.doctitle{font-family:Georgia,serif;font-size:15px;line-height:1.35;margin-top:6px}
.railblock{margin-bottom:22px}
.bignum{font-family:Georgia,"Times New Roman",serif;font-size:50px;line-height:1;font-weight:400}
.bignum.red{color:var(--red)}
.of{font-size:13px;color:var(--dim);margin-left:6px}
.bar{height:3px;background:var(--rule);margin-top:8px}
.barfill{height:100%;background:var(--ink)}
.barfill.bad{background:var(--red)}
.note{font-size:12.5px;margin-top:6px}
.red{color:var(--red)}
.green{color:var(--green)}
.pass{color:var(--green);font-weight:600}
.fail{color:var(--red);font-weight:600}
.limit{color:var(--red);font-weight:600}
.tabs{display:flex;flex-wrap:wrap;gap:2px;border-bottom:1px solid var(--rule);margin-top:22px}
.tabs [role=tab]{appearance:none;background:none;border:none;border-bottom:2px solid transparent;margin-bottom:-1px;padding:10px 14px 9px;cursor:pointer;font-family:ui-monospace,Menlo,Consolas,monospace;font-size:11.5px;letter-spacing:.12em;text-transform:uppercase;color:var(--ink)}
.tabs [role=tab]:hover{color:var(--red)}
.tabs [role=tab][aria-selected=true]{color:var(--red);border-bottom-color:var(--red)}
main{min-width:0;padding-top:6px}
.panel{padding-top:18px}
.fig{color:var(--dim);margin:18px 0 4px}
.sectitle{font-family:Georgia,serif;font-weight:400;font-size:22px;margin:26px 0 6px}
.tiles{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:0 30px;margin-top:8px}
.tile{border-top:1px solid var(--rule);padding:14px 0 18px}
.tile .lbl{color:var(--dim)}
.tile .bignum{font-size:54px}
.tile .sub{font-size:14px;margin-top:4px}
.how{font-size:13px;color:var(--dim);margin:10px 0 0;max-width:52ch}
table{border-collapse:collapse;width:100%;margin:8px 0 26px}
caption{caption-side:top;text-align:left;font-family:Georgia,serif;font-size:19px;padding:4px 0 8px}
th{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:11px;letter-spacing:.1em;text-transform:uppercase;font-weight:400;text-align:left;border-bottom:1px solid var(--ink);padding:6px 10px 6px 0}
td{border-bottom:1px solid var(--rule);padding:8px 14px 8px 0;vertical-align:top}
th.num,td.num{text-align:right;padding-right:0}
td.sec{max-width:230px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
td.fl{max-width:52ch}
tr.prow{cursor:pointer}
tr.prow:hover td{background:rgba(155,35,53,.05)}
.rowbtn{appearance:none;background:none;border:none;cursor:pointer;font-family:Georgia,serif;font-size:19px;color:var(--red);padding:2px 8px 2px 0;min-width:34px;text-align:right}
tr.drow td{background:#efe9dc;padding:14px 18px}
.fulltext{max-width:75ch}
mark.rep{background:transparent;border:1px solid var(--red);border-radius:2px;padding:0 1px}
mark.ch{background:rgba(155,35,53,.14);outline:1px dotted var(--red)}
.cmp{font-size:14px;margin:10px 0 0}
.path{margin:10px 0 0;color:var(--dim)}
.copybtn,.btn{appearance:none;background:transparent;border:1px solid var(--ink);padding:8px 14px;cursor:pointer;font-size:14px}
.copybtn:hover,.btn:hover{background:rgba(29,27,24,.06)}
.btn[disabled]{opacity:.4;cursor:not-allowed}
.linkbtn{appearance:none;background:none;border:none;padding:0;color:var(--red);cursor:pointer;text-decoration:underline;font:inherit}
.boxbtn{appearance:none;background:none;border:none;border-top:1px solid var(--rule);width:100%;text-align:left;padding:12px 0;cursor:pointer;font-family:Georgia,serif;font-size:18px}
.boxbtn::after{content:" +";color:var(--red);font-family:ui-monospace,monospace}
.boxbtn[aria-expanded=true]::after{content:" –"}
.hlist{margin:8px 0 20px;padding-left:22px;font-size:15px}
.hlist li{margin:3px 0}
.checks{list-style:none;margin:8px 0 0;padding:0}
.checks li{border-bottom:1px solid var(--rule);padding:9px 0;font-size:15px}
.checks .tag{display:inline-block;min-width:110px;font-family:ui-monospace,Menlo,Consolas,monospace;font-size:11px;letter-spacing:.1em;text-transform:uppercase;margin-right:10px}
.hint{color:var(--dim)}
.exportbtns{display:flex;gap:12px;flex-wrap:wrap;margin:10px 0 6px}
footer{border-top:1px solid var(--rule);margin-top:34px;padding-top:14px;font-size:13px;color:var(--dim)}
.credits{font-size:12px;color:var(--dim);margin-top:6px}
.srow{cursor:pointer}
.srow:hover td{background:rgba(155,35,53,.05)}
.m{font-weight:600}
@media (max-width:900px){.layout{grid-template-columns:1fr}.rail{position:static;border-right:none;border-bottom:1px solid var(--rule);padding-bottom:16px}}
```

Hmm `.checks .tag` colors: pass/fail/limit classes on the span.

Now JS full write-up. Also note: `body.children` walk — implement walk collecting blocks.

Also careful: `el.textContent` for p includes possible nested spans — fine.

One more: the paragraph regex on collapsed text: `/^(\d{1,3})\.(.*)$/` — after collapse, "1.A clean" → m[2] = "A clean…". But `\s*` after `\.` — collapsed text has single spaces; "1. A clean" → m[2]=" A clean" → trim. Use `/^(\d{1,3})\.\s*(.*)$/`.

Edge: what if a p is like "12." only — m[2]="" — paragraph with empty text; fine.

Now compute everything and render. Let me write the render functions.

Also: tab 01 tile 4 "Spaces: n repaired or flagged" — n = total logs. Link to tab 03 (data-goto=2).

Tile 2: first words match count: if REF&&REF.first_words: count of p.firstMatch===true among those with ref entry; "of reference.paragraphs". If no ref: "no reference in this file".

Tile 1: paragraphs.length; sub: REF? "the document has "+REF.paragraphs + (equal? green "match" : red diff) : "no reference in this file". Diff: (len-exp) with sign.

Tile 3: "0" red big; sub "of "+REF.footnotes+" — this HTML version has none; see tab 03" with link. If no REF: "footnotes in this HTML: 0".

How lines:
- tile1: "How this is computed: every <p> in the parsed HTML whose text begins with a number and a full stop, counted once, in document order."
- tile2: "How this is computed: the first six words of each paragraph, compared with reference.first_words after curly quotes, en dashes, non-breaking hyphens and non-breaking spaces are normalised; case is kept."
- tile3: "How this is computed: footnote text and footnote marks are absent from this HTML; the count is 0 by inspection of the parsed elements, the reference says the document has m."
- tile4: "How this is computed: four rules insert a space only where the characters prove one was there (sentence, comma, quote and dash joins); every insertion is listed on tab 03 and text_raw keeps the text as found."

Tab 02 caption: `${paragraphs.length} paragraphs found${REF? ", "+REF.paragraphs+" expected":""}`.

Now write checks list rendering:

```js
function renderChecks(){
  const ul=document.getElementById("checkList");
  ul.innerHTML = checks.map(c=>{
    const cls = c.status==="pass"?"pass": c.status==="fail"?"fail": c.status==="limit"?"limit":"hint";
    const word = c.status==="pass"?"pass": c.status==="fail"?"check failed": c.status==="limit"?"source limit":"not run";
    return `<li><span class="tag ${cls}">${word}</span><strong>${esc(c.name)}</strong> — ${c.detail}${c.link?` (<button class="linkbtn" data-goto="${c.link}">tab 0${c.link+1}</button>)`:""}</li>`;
  }).join("");
}
```

c.detail contains HTML (I'll build with esc where needed).

Check details:
1. name "Paragraph count", detail: `found ${n} · reference ${m}` (or "no reference in this file" → notrun).
2. "Numbering", detail: ok? `1–${n} in order, no gaps or duplicates` : `gaps: ${gaps.join(", ")}; duplicates: ${dups.join(", ")}; count ${n} vs ${expected}`.
3. "First words", detail: `${matchCount} of ${checked} match` + mismatches `para. 13: found "…" / reference "…"` (truncate). link 1 (tab 02 index 1 → "tab 02"). data-goto uses 0-based index: tab 02 is index 1. Label "tab 02". I'll store link as {tab:1,label:"tab 02"}.
4. "Footnotes", limit: `0 in this HTML · the document has ${m} — the HTML version has no footnotes: a limit of the source, not of the app`.
5. "Repairs", pass: `${total} spaces restored in ${paraCount} paragraphs — sentence join ${a}, comma join ${b}, quote join ${c}, dash join ${d}; every one is listed on tab 03 and text_raw keeps the text as found` + link tab 03 (index 2).
6. "Headings", pass: `${h2} h2 + ${h3} h3 = ${total} headings; ${glued} glued labels separated`.
7. "Nothing lost", pass/fail: `${total} block elements: ${cover} cover, ${committee?1:0} committee line, ${title?1:0} title, ${headings.length} headings, ${paragraphs.length} paragraphs, ${unclassified.length} unclassified`.
8. "Export round trip", pass: `the JSON to download parses back to ${parsed.length} records = ${paragraphs.length} rows on tab 02`.

If paragraphs.length===0: checks 1..: found 0 vs m → fail; numbering: expected m, found 0 → fail "count 0 vs m". Fine.

Header status & rail: as computed.

Now, "1 source limit" — plan shows literally "1 source limit" text after status. I'll render `${limits} source limit${limits===1?"":"s"}` in red within status span.

Now write everything. Also add `lang="en"`.

Potential large innerHTML for tab 02 with 90 paragraphs × 2 rows — fine.

Also the "Headings found" box button text: `Headings found: ${headings.length}`.

Elements box button: `Elements found (${blocks.length})`.

Let me make sure the tab key handling: buttons natively focusable; roving tabindex set initially: tab0 tabIndex 0 others -1 — set in HTML (tabindex="-1" on tabs 2-4) and selectTab updates.

Also panels need `aria-labelledby` and `tabindex="0"`? Panels: add tabindex="0" so they're focusable? Not required. Keep role=tabpanel + aria-labelledby; hidden attr on inactive.

Write the copy for tab 03 blocks:

Block 1:
```html
<h2 class="sectitle">Lost: footnotes <span class="count">(${REF?REF.footnotes:0})</span></h2>
<p>The document has <strong>${m} footnotes</strong>. This HTML has <strong class="red">0</strong>: no footnote text, no footnote marks, and the note the title's asterisk points to is missing. To cite a footnote, use the PDF or Word version.</p>
```
If no REF: "This HTML has 0 footnotes: no footnote text and no footnote marks are present in the parsed elements."

Block 2:
```html
<h2 class="sectitle">Changed: spaces <span class="count">(${total})</span></h2>
<p class="mono hint">sentence join: a · comma join: b · quote join: c · dash join: d — click a row to open the paragraph on tab 02</p>
<table>…</table>
<p class="how">Rules restore a space only where the characters prove it was there. Word pairs the rules cannot prove (a missing space inside a word) are not touched; the first-words check catches them only in a paragraph's first six words.</p>
```

Block 3:
```html
<h2 class="sectitle">Changed: characters</h2>
<p class="mono hint">kept as published · on a keyboard: a hyphen and straight quotes</p>
<table>Character | Count | Example</table>
<p class="how">Kept exactly as published, in the table and in every export. A search typed with the keyboard hyphen will not find a non-breaking hyphen, nor straight quotes a curly one: normalise the text before searching it.</p>
```

Character names: "En dash – (U+2013)", "Double quotes “ ” (U+201C, U+201D)", "Right single quote ’ (U+2019)", "Non-breaking hyphen ‑ (U+2011)", "Non-breaking space (U+00A0)".

Example: context with mark.ch around the char(s). For double quotes, find first “ or ”.

```js
function exampleFor(pred){
  for(const p of paragraphs){
    const t=p.text; 
    for(let i=0;i<t.length;i++){
      if(pred(t[i])){
        const b=t.slice(Math.max(0,i-18),i), a=t.slice(i+1,i+19);
        return {b,a,ch:t[i]};
      }
    }
  }
  return null;
}
```
For double quotes pred = c=>c==="“"||c==="”". For NBSP pred c==="\u00A0". Render: esc(b)+`<mark class="ch">${esc(ch)}</mark>`+esc(a). For NBSP the mark shows blank space with outline — visible. Add "…" if truncated.

Count function per char.

Now the elements table (tab 04): Tag | Classified as | Text (first 80 characters). 

```js
elemBody.innerHTML = blocks.map(b=>`<tr><td class="mono">${b.tag}</td><td>${esc(b.kindLabel)}</td><td>${esc(b.text)}</td></tr>`).join("");
```

Store kindLabel at classification.

Now assemble the script order:
1. normalize D
2. parse & pipeline
3. compute first words, chars, checks
4. render header, rail, tabs content
5. wire events

Also guard: if !D.html → show message. If body null.

Let me also handle `reference.first_words` keys: String(num).

Edge: REF.first_words may be missing → treat as no first_words.

Write `p.firstMatch`: if REF && REF.first_words && REF.first_words[String(p.num)] !== undefined → boolean; else null.

Check column display: if firstMatch===null → "" (or "no ref"); true → pass OK; false → fail.

Now let me write the final HTML. I'll write it in one go, carefully.

Also the intro text before code: 1-3 sentences. E.g. "I built the paragraph extractor for E/C.12/GC/27's HTML: it parses the attached document, finds the numbered paragraphs under their headings, repairs provable missing spaces, checks everything against the reference, and offers JSON/Markdown exports across four tabs." — but don't hard-code symbol; say "the attached document". Keep generic: "Built: a four-tab app that turns the attached UN document's HTML into numbered paragraphs with their headings, repairs only provable missing spaces, checks the result against the document's reference, and exports JSON/Markdown."

Now writing code. Let me be careful about template literal nesting: I'll use template literals with ${} — inside them, avoid backticks. Fine.

One more detail: `selectTab` should also update `location.hash`? Not needed.

Also initial: selectTab(0,false) after render.

Let me write the pipeline code concretely:

```js
const W = window.WORKSHOP_DATA || {};
let D = W.html_doc;
if (Array.isArray(D)) D = D[0] || {};
const REF = (D && D.reference) || null;
const FW = (REF && REF.first_words) || null;
const SYMBOL = D.symbol || "";
const DOC_URL = D.doc_url || "";
const TITLE = D.title || "UN document (HTML)";
const SOURCE = D.source || "";
const BUILT = D.built || "";

let doc=null;
try{ doc = new DOMParser().parseFromString(String(D.html||""), "text/html"); }catch(e){ doc=null; }

const RULES=[ ... ];

const blocks=[]; const paragraphs=[]; const headings=[]; const stream=[]; const unclassified=[];
let coverCount=0, committeeText=null, titleText=null;
let curPart=null, curSection=null;

function classify(){
  if(!doc || !doc.body) return;
  (function walk(node){
    for(const el of node.children){
      const tag=el.tagName;
      if(tag==="TABLE"){ blocks.push(mkBlock(el,"cover","cover")); coverCount++; continue; }
      if(tag==="P"){
        const text=el.textContent.replace(/\s+/g," ").trim();
        const m=text.match(/^(\d{1,3})\.\s*(.*)$/);
        if(m){
          const p=buildParagraph(parseInt(m[1],10), m[2].trim());
          p.section=curSection; p.part=curPart;
          p.citation=SYMBOL+", para. "+p.num;
          paragraphs.push(p); stream.push({type:"paragraph",p});
          blocks.push(mkBlock(el,"paragraph","paragraph "+p.num, p.raw.slice(0,80)));
        } else {
          if(committeeText===null) committeeText=text;
          blocks.push(mkBlock(el,"committee","committee line", text.slice(0,80)));
        }
        continue;
      }
      if(/^H[1-6]$/.test(tag)){
        const text=el.textContent.replace(/\s+/g," ").trim();
        if(tag==="H2" && titleText===null){ titleText=text; blocks.push(mkBlock(el,"title","title",text.slice(0,80))); continue; }
        const hm=text.match(/^([IVX]+|[A-Z])\.\s*(.+)$/);
        let label=null, heading=text, glued=false;
        if(hm){ label=hm[1]; heading=hm[2].trim(); const after=text.charAt(label.length+1); glued = after!=="" && !/\s/.test(after); }
        const h={level:tag,label,heading,full:text,glued};
        headings.push(h); stream.push({type:"heading",h});
        if(tag==="H2" && label && /^[IVX]+$/.test(label)) curPart=h;
        curSection=h;
        blocks.push(mkBlock(el,"heading","heading ("+tag+")",text.slice(0,80)));
        continue;
      }
      if(tag==="LI"||tag==="BLOCKQUOTE"||tag==="PRE"){
        const text=el.textContent.replace(/\s+/g," ").trim();
        unclassified.push({tag,text});
        blocks.push(mkBlock(el,"unclassified","unclassified",text.slice(0,80)));
        continue;
      }
      walk(el);
    }
  })(doc.body);
}
function mkBlock(el,kind,label,text){ return {tag:el.tagName, kind, label, text}; }
```

Wait — mkBlock for paragraph: text should be first 80 chars of raw. OK.

buildParagraph as designed; also compute firstMatch later.

Note: `blocks.push(mkBlock(el,"cover","cover"))` — text undefined; set text: el.textContent collapsed slice 80. Let me give mkBlock a text param default "".

First words:

```js
function normW(s){ return String(s).replace(/[“”]/g,'"').replace(/[‘’]/g,"'").replace(/[–—]/g,"-").replace(/\u2011/g,"-").replace(/\u00A0/g," ").replace(/\s+/g," ").trim(); }
function firstSix(s){ return normW(String(s).split(/\s+/).filter(Boolean).slice(0,6).join(" ")); }
paragraphs.forEach(p=>{
  if(FW && FW[String(p.num)]!==undefined){ p.firstFound=firstSix(p.text); p.firstRef=firstSix(FW[String(p.num)]); p.firstMatch = p.firstFound===p.firstRef; }
  else { p.firstMatch=null; }
});
```

Chars:

```js
const allText = paragraphs.map(p=>p.text).join("\n");
const CHARS=[
 {name:'En dash –', code:"U+2013", pred:c=>c==="\u2013"},
 {name:'Double quotes “ ”', code:"U+201C / U+201D", pred:c=>c==="\u201C"||c==="\u201D"},
 {name:'Right single quote ’', code:"U+2019", pred:c=>c==="\u2019"},
 {name:'Non-breaking hyphen ‑', code:"U+2011", pred:c=>c==="\u2011"},
 {name:'Non-breaking space', code:"U+00A0", pred:c=>c==="\u00A0"}
];
CHARS.forEach(c=>{ c.count=[...allText].filter(c.pred).length; c.ex=exampleFor(c.pred); });
```

exampleFor returns {b, ch, a, cutB, cutA}.

Checks:

```js
const checks=[];
const nP=paragraphs.length;
const expP = REF? REF.paragraphs : null;
// 1
if(REF && typeof REF.paragraphs==="number") checks.push({name:"Paragraph count", status: nP===REF.paragraphs?"pass":"fail", detail:`found ${nP} · reference ${REF.paragraphs}`});
else checks.push({name:"Paragraph count", status:"notrun", detail:"no reference in this file"});
// 2 numbering
const nums=paragraphs.map(p=>p.num);
const dups=nums.filter((n,i)=>nums.indexOf(n)!==i);
const expected = expP!==null? expP : nP;
const gaps=[]; if(nums.length){const mx=Math.max.apply(null,nums); const set=new Set(nums); for(let k=1;k<=mx;k++) if(!set.has(k)) gaps.push(k);}
const inOrder = nums.every((n,i)=>n===i+1);
const okNum = dups.length===0 && gaps.length===0 && inOrder && nP===expected;
checks.push({name:"Numbering", status: okNum?"pass":"fail", detail: okNum? `1–${nP} in order, no gaps or duplicates` : `count ${nP} vs ${expected}`+(gaps.length?` · gaps: ${gaps.join(", ")}`:"")+(dups.length?` · duplicates: ${[...new Set(dups)].join(", ")}`:"")});
// 3 first words
if(FW){
  const checked=paragraphs.filter(p=>p.firstMatch!==null);
  const bad=checked.filter(p=>!p.firstMatch);
  const det = `${checked.filter(p=>p.firstMatch).length} of ${checked.length} match` + (bad.length? "; differ: "+bad.map(p=>`para. ${p.num} (found “${p.firstFound}” / reference “${p.firstRef}”)`).join("; ") : "");
  checks.push({name:"First words", status: bad.length?"fail":"pass", detail: det, link:{tab:1,label:"tab 02"}});
} else checks.push({name:"First words", status:"notrun", detail:"no reference in this file"});
// 4 footnotes
if(REF && typeof REF.footnotes==="number") checks.push({name:"Footnotes", status:"limit", detail:`0 in this HTML · the document has ${REF.footnotes} — the HTML version has no footnotes: a limit of the source, not of the app`});
else checks.push({name:"Footnotes", status:"notrun", detail:"no reference in this file"});
// 5 repairs
const logs=[]; paragraphs.forEach(p=>p.logs.forEach(l=>logs.push(l)));
const perRule={}; RULES.forEach(r=>perRule[r.name]=0); logs.forEach(l=>perRule[l.rule]++);
const repParas=new Set(logs.map(l=>l.para)).size;
checks.push({name:"Repairs", status:"pass", detail:`${logs.length} spaces restored in ${repParas} paragraphs — ${RULES.map(r=>r.name+" "+perRule[r.name]).join(", ")}; every one is listed on tab 03 and text_raw keeps the text as found`, link:{tab:2,label:"tab 03"}});
// 6 headings
const h2=headings.filter(h=>h.level==="H2").length, h3=headings.filter(h=>h.level==="H3").length;
const glued=headings.filter(h=>h.glued).length;
checks.push({name:"Headings", status:"pass", detail:`${h2} h2 + ${h3} h3 = ${headings.length} headings; ${glued} glued labels separated`});
// 7 nothing lost
const kindCounts={}; blocks.forEach(b=>kindCounts[b.kind]=(kindCounts[b.kind]||0)+1);
const sum=Object.values(kindCounts).reduce((a,b)=>a+b,0);
const okLost = unclassified.length===0 && sum===blocks.length;
checks.push({name:"Nothing lost", status: okLost?"pass":"fail", detail:`${blocks.length} block elements: ${Object.entries(kindCounts).map(([k,v])=>v+" "+k).join(", ")}${unclassified.length?"; unclassified: "+unclassified.map(u=>u.tag).join(", "):""}`});
// 8 export round trip
let rtOk=false, rtN=0;
try{ const js=buildJSON(); rtN=JSON.parse(js).length; rtOk = rtN===nP; }catch(e){ rtOk=false; }
checks.push({name:"Export round trip", status: rtOk?"pass":"fail", detail:`the JSON to download parses back to ${rtN} records = ${nP} rows on tab 02`});
```

Status counts:

```js
const nPass=checks.filter(c=>c.status==="pass").length;
const nFail=checks.filter(c=>c.status==="fail").length;
const nLimit=checks.filter(c=>c.status==="limit").length;
const nRun=nPass+nFail;
```

Header status html:

```js
let st;
if(nRun===0) st=`<span class="dot bad"></span>checks not run`;
else if(nFail>0) st=`<span class="dot bad"></span>${nFail} check${nFail>1?"s":""} failed`;
else st=`<span class="dot ok"></span>${nPass} of ${nRun} checks pass`;
if(nLimit>0) st+=` <span class="fail">· ${nLimit} source limit${nLimit>1?"s":""}</span>`;
```

Rail checks link text: nRun? `${nPass} of ${nRun} checks pass` : "checks: not run".

Rendering tab 02 detail: build once.

Also "Copy citation" copies p.citation.

Now exports wiring:

```js
document.getElementById("dlJson").addEventListener("click",()=>{ if(!paragraphs.length) return; download(SYMBOL.replace(/\//g,"-")+".json", buildJSON(), "application/json"); });
```

Disabled attr set if !paragraphs.length.

Markdown build as above.

Now, one thing: `buildJSON` used in check 8 before definition — define functions before checks. Order in script: helpers, pipeline, buildJSON/buildMarkdown defs, checks, render, events.

Also `recordFor` uses REF for limitations.

Let me now also render tab 01 tiles:

```js
function renderTiles(){
  const t=document.getElementById("tiles");
  const diff = expP!==null? nP-expP : null;
  const pSub = expP!==null
    ? (diff===0? `<span class="pass">the document has ${expP} — match</span>` : `<span class="fail">the document has ${expP} — ${diff>0?"+":"−"}${Math.abs(diff)}</span>`)
    : `<span class="hint">no reference in this file</span>`;
  const fwCount = paragraphs.filter(p=>p.firstMatch===true).length;
  const fwChecked = paragraphs.filter(p=>p.firstMatch!==null).length;
  const fwSub = FW? `${fwCount} of ${expP} match` : "no reference in this file";
  const fSub = REF&&typeof REF.footnotes==="number"? `of ${REF.footnotes} — this HTML version has none; <button class="linkbtn" data-goto="2">tab 03</button>` : "in this HTML — no reference to compare";
  t.innerHTML = `
   <div class="tile"><div class="mono up lbl">Paragraphs found</div><div class="bignum">${nP}</div><div class="sub">${pSub}</div><p class="how">How this is computed: every &lt;p&gt; in the parsed HTML whose text begins with a number and a full stop, counted once, in document order.</p></div>
   <div class="tile"><div class="mono up lbl">First words match</div><div class="bignum">${FW?fwCount:0}</div><div class="sub">${esc(fwSub)}</div><p class="how">How this is computed: the first six words of each paragraph against reference.first_words, compared after curly quotes, en dashes, non-breaking hyphens and non-breaking spaces are normalised; case is kept.</p></div>
   <div class="tile"><div class="mono up lbl">Footnotes</div><div class="bignum red">0</div><div class="sub red">${fSub}</div><p class="how">How this is computed: no footnote text or footnote mark survives in this HTML; the count is 0 by inspection of the parsed elements.</p></div>
   <div class="tile"><div class="mono up lbl">Spaces repaired or flagged</div><div class="bignum">${logs.length}</div><div class="sub"><button class="linkbtn" data-goto="2">see tab 03</button></div><p class="how">How this is computed: four rules insert a space only where the characters prove one was there (sentence, comma, quote and dash joins); text_raw keeps the text as found.</p></div>`;
  if(nP===0){ t.innerHTML = `<p class="fail">The parsed HTML yielded no numbered paragraphs — the exports are disabled.</p>` + t.innerHTML; }
}
```

Hmm if nP===0 prepend notice. OK.

Tab 02 render:

```js
function renderParagraphs(){
  document.getElementById("hBoxBtn").textContent = "Headings found: "+headings.length;
  document.getElementById("hList").innerHTML = headings.map(h=>`<li><span class="mono">${h.level}</span> ${esc(h.full)}</li>`).join("");
  const cap=document.getElementById("pCap");
  cap.textContent = `${nP} paragraphs found${expP!==null?", "+expP+" expected":""}`;
  const tb=document.getElementById("pBody");
  tb.innerHTML = paragraphs.map(p=>{
    const chk = p.firstMatch===null? "" : p.firstMatch? `<span class="pass">OK</span>` : `<span class="fail">first words differ</span>`;
    const sec = p.section? p.section.full : "—";
    return `<tr class="prow"><td class="num"><button class="rowbtn" aria-expanded="false" aria-controls="det-${p.num}" data-num="${p.num}">${p.num}</button></td><td class="sec" title="${esc(sec)}">${esc(sec)}</td><td class="fl">${esc(firstLine(p.text))}</td><td>${chk}</td></tr>`+
    `<tr class="drow" id="det-${p.num}" hidden><td colspan="4">${detailHtml(p)}</td></tr>`;
  }).join("");
}
function detailHtml(p){
  const marked=p.parts.map(pt=>pt.mk?`<mark class="rep">${esc(pt.t)}</mark>`:esc(pt.t)).join("");
  let h=`<div class="fulltext">${marked}</div>`;
  if(p.firstMatch===false) h+=`<p class="cmp"><span class="fail">first words differ</span> — found “${esc(p.firstFound)}” · reference “${esc(p.firstRef)}”</p>`;
  else if(p.firstMatch===true) h+=`<p class="cmp pass">first six words match the reference</p>`;
  if(p.logs.length) h+=`<p class="mono hint">repairs here: ${esc(p.logs.map(l=>l.rule).join(", "))}</p>`;
  const path = [p.part?p.part.full:null, p.section?p.section.full:null].filter(Boolean).join(" › ");
  if(path) h+=`<p class="path mono">path: ${esc(path)}</p>`;
  h+=`<p class="cmp"><a href="${DOC_URL}" target="_blank" rel="noopener">${esc(SYMBOL)}</a>, para. ${p.num} &nbsp;<button class="copybtn" data-cite="${esc(p.citation)}">Copy citation</button> <span class="mono hint" id="cp-${p.num}"></span></p>`;
  return h;
}
```

Copy feedback: change button text to "Copied" 2s.

Tab 03 render:

```js
function renderLost(){
  // footnotes block
  const fb=document.getElementById("fnText");
  fb.innerHTML = REF&&typeof REF.footnotes==="number"
    ? `The document has <strong>${REF.footnotes} footnotes</strong>. This HTML has <strong class="red">0</strong>: no footnote text, no footnote marks, and the note the title's asterisk points to is missing. To cite a footnote, use the PDF or Word version.`
    : `This HTML has <strong class="red">0 footnotes</strong>: no footnote text and no footnote marks are present in the parsed elements.`;
  // spaces
  document.getElementById("ruleLine").textContent = RULES.map(r=>r.name+": "+perRule[r.name]).join(" · ")+" — "+logs.length+" spaces in "+repParas+" paragraphs · click a row = open the paragraph on tab 02";
  document.getElementById("sBody").innerHTML = logs.map((l,i)=>{
    const r=ruleByName[l.rule]; r.re.lastIndex=0; const m=r.re.exec(l.match);
    const repHtml=r.pieces(m).map(pc=>pc[1]?`<mark class="rep">${esc(pc[0])}</mark>`:esc(pc[0])).join("");
    const b=l.before, a=l.after;
    return `<tr class="srow" data-num="${l.para}"><td class="num">${l.para}</td><td>${b.length===20?"…":""}${esc(b)}<span class="m">${esc(l.match)}</span>${esc(a)}${a.length===20?"…":""}</td><td>${b.length===20?"…":""}${esc(b)}${repHtml}${esc(a)}${a.length===20?"…":""}</td><td>${esc(l.rule)}</td></tr>`;
  }).join("");
  // characters
  document.getElementById("cBody").innerHTML = CHARS.map(c=>{
    const ex = c.ex? `${c.ex.cutB?"…":""}${esc(c.ex.b)}<mark class="ch">${esc(c.ex.ch)}</mark>${esc(c.ex.a)}${c.ex.cutA?"…":""}` : "—";
    return `<tr><td>${esc(c.name)} <span class="mono hint">${c.code}</span></td><td class="num">${c.count}</td><td>${ex}</td></tr>`;
  }).join("");
}
```

exampleFor:

```js
function exampleFor(pred){
  for(const p of paragraphs){
    const t=p.text;
    for(let i=0;i<t.length;i++){
      if(pred(t[i])){
        return {b:t.slice(Math.max(0,i-18),i), ch:t[i], a:t.slice(i+1,i+19), cutB:i-18>0, cutA:i+19<t.length};
      }
    }
  }
  return null;
}
```

Tab 04 render: checks list + elements table + export buttons.

```js
function renderChecksPanel(){
  document.getElementById("checkList").innerHTML = checks.map(c=>{
    const cls=c.status==="pass"?"pass":c.status==="fail"?"fail":c.status==="limit"?"limit":"hint";
    const word=c.status==="pass"?"pass":c.status==="fail"?"check failed":c.status==="limit"?"source limit":"not run";
    const link=c.link?` (<button class="linkbtn" data-goto="${c.link.tab}">${c.link.label}</button>)`:"";
    return `<li><span class="tag ${cls}">${word}</span><strong>${esc(c.name)}</strong> — ${c.detail}${link}</li>`;
  }).join("");
  document.getElementById("eBtn").textContent="Elements found ("+blocks.length+")";
  document.getElementById("eBody").innerHTML=blocks.map(b=>`<tr><td class="mono">${b.tag}</td><td>${esc(b.label)}</td><td>${esc(b.text||"")}</td></tr>`).join("");
}
```

c.detail may contain HTML (buttons) — I built details with esc where needed; the footnote detail has plain text; first words detail includes quotes — esc them. In check 3 detail I used “ ” chars — fine as literal. But p.firstFound may contain < ? esc. I'll esc firstFound/firstRef in detail.

Rail render:

```js
document.getElementById("rSym").textContent=SYMBOL;
document.getElementById("rTitle").textContent=TITLE;
document.getElementById("rP").textContent=nP;
document.getElementById("rPof").textContent= expP!==null? "of "+expP+" paragraphs" : "paragraphs";
const bar=document.getElementById("rBar");
if(expP!==null){ bar.style.width=Math.min(100, nP/expP*100)+"%"; bar.classList.toggle("bad", nP!==expP); } else { bar.style.width="100%"; }
document.getElementById("rFof").textContent= REF&&typeof REF.footnotes==="number"? "of "+REF.footnotes+" footnotes" : "footnotes in this HTML";
document.getElementById("rChecks").textContent= nRun? `${nPass} of ${nRun} checks pass` : "checks not run";
```

Header:

```js
document.getElementById("hTitle").textContent=TITLE;
const a=document.getElementById("hSym"); a.textContent=SYMBOL; if(DOC_URL) a.href=DOC_URL; else a.removeAttribute("href");
document.getElementById("hAdopted").textContent= REF&&REF.adopted? " · adopted "+REF.adopted : "";
document.getElementById("hSource").textContent= SOURCE? " · "+SOURCE : "";
document.getElementById("hStatus").innerHTML=st;
```

Footer:

```js
document.getElementById("fLine").textContent = (SOURCE? SOURCE+" · ":"") + (BUILT? "built "+BUILT+" · ":"") + "Done by this page's code; no model was called and nothing left the browser.";
```

Credits line static in HTML.

Events: tabs, data-goto delegation, tbody delegation, box buttons (hBoxBtn, eBtn) toggle, downloads, copy.

Box toggle:

```js
function wireBox(btnId, boxId){ const b=document.getElementById(btnId), x=document.getElementById(boxId); b.addEventListener("click",()=>{ const open=b.getAttribute("aria-expanded")==="true"; b.setAttribute("aria-expanded",String(!open)); x.hidden=open; }); }
```

data-goto delegation:

```js
document.addEventListener("click",e=>{
  const g=e.target.closest("[data-goto]");
  if(g){ selectTab(parseInt(g.getAttribute("data-goto"),10), true); }
});
```

tbody delegation as planned.

Downloads:

```js
const base=SYMBOL.replace(/\//g,"-")||"document";
dlJson.onclick=()=>{ if(!nP)return; download(base+".json", buildJSON(), "application/json"); };
dlMd.onclick=()=>{ if(!nP)return; download(base+".md", buildMarkdown(), "text/markdown"); };
if(!nP){ dlJson.disabled=true; dlMd.disabled=true; }
```

copyText as planned; on copy button click set text "Copied" then revert.

Now, one more check on the regex `/^([IVX]+|[A-Z])\.\s*(.+)$/` — for heading "I.Introduction": `[IVX]+` matches "I"; but greedy `[IVX]+` on "IV.Introduction" matches "IV". On "X. Foo" fine. On a heading like "A. B. C"? label "A", heading "B. C". fine.

But careful: heading text "D. Obligation" — after collapse "D. Obligation". label "D", after=text.charAt(2)=" " → not glued. Good.

What about h2 "I.Introduction" — charAt(2)="I" → glued. Good.

Potential false positive: heading "Right to work (art. 6)" — no match as analyzed. But what about "A.1 something"? label "A", heading "1 something" — fine.

Edge: heading like "IV. Foo" where `[IVX]+` could match "I" then require "." but next is "V" → backtrack; regex engine will try `[IVX]+`="IV" then "." matches. Good.

Now the title h2: "General comment No. 27 (2025) on ... sustainable development *" — first H2 → title. Good.

Also note: the walk starts at doc.body; body.children = [table, div.content]. table → cover block. div → walk into it: children = [p (committee), h2 (title), h2, p, p, ...]. 

Now, `mkBlock` for cover: text = collapsed textContent slice 80.

Let me also compute `perRule` before renderLost — computed in checks section; order: pipeline → first words → chars → logs/perRule → checks → render. Fine.

Also `ruleByName`.

Now, one subtlety with `String.prototype.replace` and my pieces approach: the pieces functions use match groups m[1], m[2]. For quote rule (1 group): pieces m=>[[m[1],0],[" ",1],["“",0]]. For dash: m=>[["–",0],[" ",1],[m[1],0]]. Good.

Also in renderLost I re-exec the rule on l.match to get groups — but l.match for quote rule is like "a“" — exec gives m[1]="a". pieces → [["a",0],[" ",1],["“",0]] → html "a<mark> </mark>“". Good.

Now, the tab labels: "01 RESULT", "02 PARAGRAPHS", "03 LOST & CHANGED", "04 CHECKS & EXPORT". In HTML with &amp;.

Panels ids: panel-1..4; tabs aria-controls.

Also add `role="tablist"` on container with aria-label "Views of the document".

Let me also include the "FIG/TAB" monospace labels: above tiles: `<div class="mono up fig">TAB.01 · Result</div>`; above paragraphs table: `TAB.02 · Paragraphs`; tab 03 blocks have sectitles; add fig `TAB.03 · Lost & changed`; tab 04: `TAB.04 · Checks & export`.

Table captions: paragraphs table caption id pCap; spaces table caption: `${logs.length} missing spaces restored by rule`; characters caption: "Characters kept as published"; elements caption: "Every block element, in document order".

Now — the header status: also plan wants "1 source limit" text; included.

Also plan: rail "n of m checks pass, linking to tab 04" — button data-goto="3". Good.

Let me now also double-check the "at most seven things to click" per view: tab 02: headings box button + rows (rows not counted) → 1 + tab bar 4. Fine.

Now write final file. Also include `<meta name="color-scheme" content="light">`? Not necessary.

Potential issue: `el.textContent` on the cover table includes lots; fine.

Also: paragraphs table might be big; fine.

Let me write out the complete document now, mentally checking syntax.

Also: in detailHtml, `id="cp-${p.num}"` unused — drop.

copyText:

```js
function copyText(t, btn){
  const revert=()=>{ const old=btn.dataset.label||"Copy citation"; btn.textContent=old; };
  btn.dataset.label=btn.dataset.label||btn.textContent;
  const ok=()=>{ btn.textContent="Copied"; setTimeout(revert,2000); };
  const fail=()=>{ btn.textContent="Select & copy"; setTimeout(revert,2000); };
  const fb=()=>{
    try{
      const ta=document.createElement("textarea");
      ta.value=t; ta.setAttribute("readonly",""); ta.style.position="fixed"; ta.style.opacity="0";
      document.body.appendChild(ta); ta.select();
      const good=document.execCommand("copy"); ta.remove(); good?ok():fail();
    }catch(e){ fail(); }
  };
  if(navigator.clipboard && navigator.clipboard.writeText){ navigator.clipboard.writeText(t).then(ok, fb); } else fb();
}
```

tbody click handler:

```js
document.getElementById("pBody").addEventListener("click", e=>{
  const cb=e.target.closest(".copybtn");
  if(cb){ copyText(cb.getAttribute("data-cite"), cb); return; }
  const row=e.target.closest("tr.prow");
  if(!row) return;
  const btn=row.querySelector(".rowbtn");
  const det=document.getElementById(btn.getAttribute("aria-controls"));
  const open=btn.getAttribute("aria-expanded")==="true";
  btn.setAttribute("aria-expanded", String(!open));
  det.hidden=open;
});
```

sBody click:

```js
document.getElementById("sBody").addEventListener("click", e=>{
  const tr=e.target.closest("tr.srow");
  if(tr) openParagraph(parseInt(tr.getAttribute("data-num"),10));
});
```

openParagraph as planned; also after selectTab(1) need panel visible — selectTab handles.

Tabs HTML:

```html
<div class="tabs" role="tablist" aria-label="Views">
  <button role="tab" id="tab-0" aria-controls="panel-0" aria-selected="true" tabindex="0">01 Result</button>
  <button role="tab" id="tab-1" aria-controls="panel-1" aria-selected="false" tabindex="-1">02 Paragraphs</button>
  <button role="tab" id="tab-2" aria-controls="panel-2" aria-selected="false" tabindex="-1">03 Lost &amp; changed</button>
  <button role="tab" id="tab-3" aria-controls="panel-3" aria-selected="false" tabindex="-1">04 Checks &amp; export</button>
</div>
```

Panels:

```html
<section class="panel" role="tabpanel" id="panel-0" aria-labelledby="tab-0">…</section>
<section class="panel" role="tabpanel" id="panel-1" aria-labelledby="tab-1" hidden>…</section>
...
```

selectTab uses index.

Now finalize tab 03 markup:

```html
<section class="panel" role="tabpanel" id="panel-2" aria-labelledby="tab-2" hidden>
  <div class="mono up fig">TAB.03 · Lost &amp; changed</div>
  <h2 class="sectitle">Lost: footnotes</h2>
  <p id="fnText"></p>
  <h2 class="sectitle">Changed: spaces</h2>
  <p class="mono hint" id="ruleLine"></p>
  <table>
    <caption id="sCap"></caption>
    <thead><tr><th scope="col" class="num">Paragraph</th><th scope="col">Before</th><th scope="col">After</th><th scope="col">Rule</th></tr></thead>
    <tbody id="sBody"></tbody>
  </table>
  <p class="how">Rules restore a space only where the characters prove it was there. Word pairs the rules cannot prove (a missing space inside a word) are not touched; the first-words check catches them only in a paragraph's first six words.</p>
  <h2 class="sectitle">Changed: characters</h2>
  <p class="mono hint">kept exactly as published · on a keyboard: a hyphen and straight quotes</p>
  <table>
    <caption>Characters kept as published, counted over all paragraph texts</caption>
    <thead><tr><th scope="col">Character</th><th scope="col" class="num">Count</th><th scope="col">Example</th></tr></thead>
    <tbody id="cBody"></tbody>
  </table>
  <p class="how">Kept exactly as published, in the table and in every export. A search typed with the keyboard hyphen will not find a non-breaking hyphen, nor straight quotes a curly one: normalise the text before searching it.</p>
</section>
```

sCap: `${logs.length} missing spaces, restored by rule — the inserted space is boxed`.

Tab 04 markup:

```html
<section class="panel" role="tabpanel" id="panel-3" aria-labelledby="tab-3" hidden>
  <div class="mono up fig">TAB.04 · Checks &amp; export</div>
  <h2 class="sectitle">Checks</h2>
  <ul class="checks" id="checkList"></ul>
  <h2 class="sectitle">Export</h2>
  <div class="exportbtns">
    <button class="btn" id="dlJson">Download JSON</button>
    <button class="btn" id="dlMd">Download Markdown</button>
  </div>
  <p class="how">JSON: one record per paragraph — symbol, paragraph, section, part, text, text_raw, first_words_match, citation, doc_url, limitations. Markdown: front matter (title, symbol, adopted, source_url, extracted, paragraphs_found, paragraphs_expected, footnotes), then headings and paragraphs in document order. File name: the symbol with slashes as hyphens; UTF-8.</p>
  <button class="boxbtn" id="eBtn" aria-expanded="false" aria-controls="eBox">Elements found</button>
  <div id="eBox" hidden>
    <table>
      <caption>Every block element in the parsed HTML, in document order</caption>
      <thead><tr><th scope="col">Tag</th><th scope="col">Classified as</th><th scope="col">Text (first 80 characters)</th></tr></thead>
      <tbody id="eBody"></tbody>
    </table>
  </div>
</section>
```

Tab 02 markup:

```html
<section class="panel" role="tabpanel" id="panel-1" aria-labelledby="tab-1" hidden>
  <div class="mono up fig">TAB.02 · Paragraphs</div>
  <button class="boxbtn" id="hBoxBtn" aria-expanded="false" aria-controls="hBox">Headings found</button>
  <div id="hBox" hidden><ol class="hlist" id="hList"></ol></div>
  <table>
    <caption id="pCap"></caption>
    <thead><tr><th scope="col" class="num">No.</th><th scope="col">Section</th><th scope="col">First line</th><th scope="col">Check</th></tr></thead>
    <tbody id="pBody"></tbody>
  </table>
  <p class="how">Click a row = expand it in place: full text verbatim (repaired spaces boxed), the reference's first six words, the repairs in that paragraph, and a copy-citation button. The citation is “symbol, para. n”.</p>
</section>
```

Tab 01:

```html
<section class="panel" role="tabpanel" id="panel-0" aria-labelledby="tab-0">
  <div class="mono up fig">TAB.01 · Result</div>
  <div class="tiles" id="tiles"></div>
</section>
```

Rail & header & footer as planned.

Now, careful with JS string containing `</` inside script? No `</script>` sequences in strings — my template strings contain `</tr>` etc. — that's fine, only `</script>` is problematic. Avoid.

Also `&` in tab labels — use `&amp;` in HTML.

One more: the plan says header line: "symbol linked to doc_url (new tab), 'adopted reference.adopted', source". Done.

Also "At the right a green dot 'n of m checks pass' or a red dot 'n checks failed', then '1 source limit'". Done.

Now, `firstLine` uses p.text (repaired). OK.

Let me also make sure `buildJSON` defined before checks use it — I'll define functions with function declarations (hoisted) so order doesn't matter much. Use function declarations for buildJSON, buildMarkdown, recordFor.

recordFor:

```js
function recordFor(p){
  return {
    symbol: SYMBOL,
    paragraph: p.num,
    section: p.section? p.section.full : "",
    part: p.part? p.part.full : "",
    text: p.text,
    text_raw: p.raw,
    first_words_match: p.firstMatch,
    citation: p.citation,
    doc_url: DOC_URL,
    limitations: "no footnotes in this HTML version" + (REF && typeof REF.footnotes==="number"? "; the document has "+REF.footnotes+" footnotes" : "")
  };
}
```

Plan: limitations ("no footnotes in this HTML version; the document has n"). Good.

Now write it all. Also double-check `walk` handles `doc.body` null.

Also: `blocks` for cover: mkBlock(el,"cover","cover", collapsed text slice 80).

Let me write mkBlock:

```js
function mkBlock(el, kind, label, text){
  return {tag: el.tagName, kind: kind, label: label, text: text||""};
}
```

For cover: `blocks.push(mkBlock(el,"cover","cover", el.textContent.replace(/\s+/g," ").trim().slice(0,80)));`

For committee: label "committee line". For title: "title". heading: "heading ("+tag+")". paragraph: "paragraph "+num. unclassified: "unclassified".

Check 7 kindCounts uses b.kind — labels differ; use kind. Good.

Now, also ensure `stream` includes title? For markdown I add "# TITLE" manually. OK.

Potential issue: `paragraphs` empty → Math.max.apply(null, []) = -Infinity; guarded by nums.length check.

Also `firstLine` on empty text returns "".

Now, the intro sentence before the code block (max 3 sentences), and nothing after.

Let me also double check the RULES regexes against sample text: "levels.Key" → sentence rule: ([a-z])\.([A-Z]) matches "s.K" → "s. K". Good. "land,wetlands" → comma: "d,w" → "d, w". Good. "crises“increase" → quote: "s“" → "s “". Good. "challenges –to" → dash: "–t" → "– t". Good.

Note the dash rule `/–([A-Za-z])/g` — en dash only, not em dash. Plan says en dash. OK.

One more consideration: the sentence rule could match across "art. 6)"? "art. 6" — after "." is space → no. "No. 27" no. But "e.g.Example"? would match — intended.

Also careful: sentence rule might match inside "U.S.A"? "U.S" — U not lowercase. "i.e.Foo" → "i.e. Foo" — fine.

Now, the check "First words" detail could be long with 6 mismatches — fine.

Also plan: "A failed check never hides a result" — we show everything regardless. Good.

Now write the final answer. Estimate lines ~850. Let me write it.

Also remember `[hidden]{display:none!important}` in CSS.

Also the `.tag` width for "check failed" — min-width 110px ok.

Also add `td .mono` sizing fine.

Let me write the script in a single IIFE.

One more detail: `selectTab` should also move focus? Only when keyboard nav. Clicking sets selection without focus change (focus stays on clicked button anyway).

Also initial call selectTab(0,false) to sync (panels 1-3 already hidden in markup; fine).

Write download():

```js
function download(name, text, mime){
  const blob=new Blob([text],{type:mime+";charset=utf-8"});
  const url=URL.createObjectURL(blob);
  const a=document.createElement("a");
  a.href=url; a.download=name;
  document.body.appendChild(a); a.click(); a.remove();
  setTimeout(()=>URL.revokeObjectURL(url),800);
}
```

OK. Also `buildMarkdown` uses stream; ensure stream built.

Also the h1 title: TITLE from data.

Edge: if D.html missing → doc null → paragraphs empty → tab 01 notice; header still shows title/symbol. Fine.

Now compose. I'll write carefully to avoid syntax errors.

For the checks detail of first words, escaping: `found “${esc(p.firstFound)}” / reference “${esc(p.firstRef)}”`.

Also in check 3, `checked.length` may be < nP if some keys missing; detail says "x of y match" where y=checked.length; plan says "n of reference.paragraphs". I'll show `${matchCount} of ${expP}` plus mismatch list. Let me use: `${fwCount} of ${expP} match` where fwCount counts firstMatch===true. And mismatches listed. Good.

Also tile 2 uses fwCount of expP.

Now, writing everything out.

Also: the plan wants tab 02 "Check" column values "OK" or "first words differ" — done.

Also "Rows are buttons with aria-expanded" — our rowbtn has aria-expanded; row click works. Good enough.

Final check on grid: `.layout` with rail sticky. Header full width. Footer full width.

Also add `main` wrapper around tabs+panels inside layout's second column.

Let me write the code now, final.

Additional small thing: `document.getElementById("hBoxBtn")` textContent set in renderParagraphs: "Headings found: n".

Also wire hBoxBtn/eBtn toggles.

Also the "fig" labels: TAB.01 etc.

Also add `title` element: `<title>` + SYMBOL.

Alright, compose the final response: 2-3 intro sentences, then the html code block, nothing after.

Let me now write out the entire HTML meticulously.

Regarding the `.checks .tag` for "not run" — class "hint" color dim. Fine.

Also in renderTiles, when FW null, tile2 bignum 0 and sub "no reference in this file" — plan says tiles say "no reference in this file". OK.

Also when expP null, tile1 sub "no reference in this file".

Writing the script — I'll be careful with the `walk` function and `for...of` over `node.children` (HTMLCollection is iterable in modern browsers). OK.

Also `el.tagName` for SVG? none.

Let me also handle `D.html` being non-string (array sample had html string). String(D.html||"").

Now produce final output.

One more thought on `normW`: also normalize multiple spaces — done via replace(/\s+/g," ").trim().

firstSix: split on /\s+/ — note \s in JS includes \u00A0, so NBSP splits words — matches "whitespace-separated". Good.

Also compare: firstSix(p.text) vs firstSix(FW[...]) — both normalized. Case kept. Good.

Now the code.

Also: careful that in template literals inside renderParagraphs I use `${esc(...)}` — esc defined. And `firstLine` defined.

Also `detailHtml` uses p.parts — ensure buildParagraph returns parts.

Let me finalize buildParagraph:

```js
function buildParagraph(num, raw){
  const logs=[];
  let parts=[{t:raw, mk:false}];
  for(const r of RULES){
    const out=[];
    for(const p of parts){
      if(p.mk){ out.push(p); continue; }
      let last=0, m; r.re.lastIndex=0;
      while((m=r.re.exec(p.t))!==null){
        out.push({t:p.t.slice(last,m.index), mk:false});
        const pcs=r.pieces(m);
        for(const pc of pcs) out.push({t:pc[0], mk:pc[1]===1});
        logs.push({para:num, rule:r.name, match:m[0],
          before:p.t.slice(Math.max(0,m.index-20), m.index),
          after:p.t.slice(m.index+m[0].length, m.index+m[0].length+20)});
        last=m.index+m[0].length;
        if(m[0].length===0) r.re.lastIndex++;
      }
      out.push({t:p.t.slice(last), mk:false});
    }
    parts=out;
  }
  const text=parts.map(p=>p.t).join("");
  return {num:num, raw:raw, text:text, parts:parts, logs:logs, section:null, part:null, citation:"", firstMatch:null};
}
```

RULES pieces use m groups:

```js
const RULES=[
 {name:"sentence join", re:/([a-z])\.([A-Z])/g, pieces:m=>[[m[1]+".",0],[" ",1],[m[2],0]]},
 {name:"comma join", re:/([a-z]),([A-Za-z])/g, pieces:m=>[[m[1]+",",0],[" ",1],[m[2],0]]},
 {name:"quote join", re:/([a-z])“/g, pieces:m=>[[m[1],0],[" ",1],["“",0]]},
 {name:"dash join", re:/–([A-Za-z])/g, pieces:m=>[["–",0],[" ",1],[m[1],0]]}
];
```

Good.

Now full write-up. Also note: in renderLost, re-exec rule on l.match: `r.re.lastIndex=0; const m=r.re.exec(l.match);` — l.match is the matched substring; exec returns match with groups. Good.

Also `ruleByName` map.

Also careful: `perRule` computed from logs.

Also `repParas`.

Now the final answer. Also keep intro ≤3 sentences.

Let me count clickable things on tab 04: 2 export buttons + elements box = 3 (+4 tabs). OK.

Also ensure the app explains itself: how lines present. Good.

Write it.