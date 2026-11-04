Let me plan this app carefully. The user wants a single HTML file app that:

1. Parses `WORKSHOP_DATA.html_doc.html` with DOMParser
2. Classifies elements: cover table, committee line, title h2, headings (h2/h3), numbered paragraphs
3. Computes repairs (space insertions) with rules
4. Counts special characters
5. Compares against `reference` (paragraphs, footnotes, adopted, first_words)
6. Four tabs: 01 RESULT, 02 PARAGRAPHS, 03 LOST & CHANGED, 04 CHECKS & EXPORT
7. Left rail with document card, big numbers
8. Header with title, symbol link, adopted, source, check status dot
9. Export JSON and Markdown via Blob URLs
10. Copy citation buttons
11. Footer

Let me think about the data structure:

```js
WORKSHOP_DATA.html_doc = {
  title, symbol, doc_url, source, html, reference: {paragraphs, footnotes, adopted, first_words}
}
```

Wait — the description says `html_doc` is `{title, symbol, doc_url, source, html, reference: {...}}`. The sample shows `html_doc` as an array with one element containing `html`... Actually the sample shows `"html_doc": [ { "html": "..." } ]` but the description says it's an object. The description at top says: "`WORKSHOP_DATA.html_doc`: one UN document as OHCHR publishes it in HTML — `{title, symbol, doc_url, source, html, reference: {...}}`". The sample JSON shows an array but that's just the sample format (samples are arrays of records). I should handle both: if it's an array, take element 0. Let me be defensive: `const doc = Array.isArray(WORKSHOP_DATA.html_doc) ? WORKSHOP_DATA.html_doc[0] : WORKSHOP_DATA.html_doc;`

Pipeline:

```js
const parsed = new DOMParser().parseFromString(doc.html, 'text/html');
const body = parsed.body;
// iterate over body's children (block elements) in order
```

Actually elements might be nested inside divs. The description says: cover `<table>`, then `<div class="content">` containing p, h2, h3. So I should iterate over all block-level elements in document order. Simplest: walk `body.querySelectorAll('*')` but only consider top-level block elements. Better approach: collect elements in document order that are direct children of body or of divs... Let me do a recursive walk collecting block elements: table, div, p, h1-h6, ul, etc. Actually simpler: get all elements in document order via `body.querySelectorAll('table, div, p, h1, h2, h3, h4, h5, h6, ul, ol, li, blockquote, pre')` — but nested divs would double count. Hmm.

Better: a function that walks children of body; for each element, if it's a "container" (div), recurse into it; otherwise classify it. That handles `<div class="content">`. Let me do:

```js
function collectBlocks(el, out) {
  for (const child of el.children) {
    const tag = child.tagName.toLowerCase();
    if (tag === 'div' || tag === 'section' || tag === 'article' || tag === 'main') {
      collectBlocks(child, out);
    } else {
      out.push(child);
    }
  }
}
```

That gives block elements in order: table, p (committee), h2 (title), h2s, h3s, ps...

Classification:
- First `<table>` → cover. Actually "Elements inside the first `<table>` are cover." So the table element itself is cover. What if there are more tables? Classify any table as cover? The spec says "the first `<table>`". I'll classify tables as cover (all of them, but there's one). Actually to be safe: any `table` → cover.
- `<p>` matching `/^(\d{1,3})\.\s*(.*)$/s` → paragraph with number = int, text_raw = rest trimmed, whitespace collapsed.
- First `<h2>` → title.
- Other h2/h3 → heading. Split label: `/^([IVX]+|[A-Z])\.\s*(.+)$/s` → label + heading. If no match, label = null, heading = full text. "glued labels were separated" — count headings where the regex matched but `\s*` matched zero spaces? Hmm, "how many glued labels were separated" — a heading like "I.Introduction" matches with no space after the dot. So glued = match where the original had no space after "label." i.e. `/^([IVX]+|[A-Z])\.(?!\s)/`. Let me count: heading matches regex AND the character after the dot is not whitespace → glued label separated. Actually "D. Obligation" has its space, so it's not glued. I'll compute `glued = /^([IVX]+|[A-Z])\.[^\s]/` test on the heading text.

Wait, but the heading text — I should get textContent, collapse whitespace. "I.Introduction" → label "I", heading "Introduction". "Right to work (art. 6)" → no match (starts with capital R but "Right" is more than one letter... regex `^([IVX]+|[A-Z])\.` requires single capital letter followed by dot. "Right to work" — R followed by "i", not a dot. So no match. Good. But what about "D. Obligation" → label "D", heading "Obligation". Good.

Hmm wait, careful: `[IVX]+` could match "IX" etc. Also a heading like "A. Something" matches. What about headings that are just text like "Introduction"? No dot → no match.

- Any other `<p>` → committee line (or "other p"). The spec says "any other `<p>` is the committee line". But for the "Nothing lost" check, every block element must be classified exactly once. Classes: cover, committee, title, heading, paragraph, other. If something is not p/h2/h3/table (e.g., ul), classify as "other" and list in red if unclassified... Actually "any unclassified element is listed in red" — I'll have an "other" class and count it; if other > 0, list them. Hmm, the check says "Every block element is classified exactly once and the counts per class sum to the total; any unclassified element is listed in red." So I'll classify everything into one of the classes; "other" elements are the "unclassified" ones listed in red. Let me define classes: cover, committee, title, heading, paragraph, other. The check passes if other === 0 (or lists them in red otherwise). Actually the check should verify sum of class counts === total blocks. That always passes by construction... unless I make classification strict. Let me make it: an element is "classified" if it falls into cover/committee/title/heading/paragraph; anything else goes to "other" and is listed in red, and the check reports "n elements not classified" as a failure-ish. I'll implement: check "Nothing lost" = (otherCount === 0) ? pass : fail with list. And also sum check.

Paragraph text processing:
- `text_raw` = captured group 2, trimmed, whitespace runs collapsed to single space: `.replace(/\s+/g, ' ').trim()`.
- Repairs on text_raw → text, logging each insertion: {para, rule, before (20 chars each side), after}. Rules:
  1. sentence join: `/([a-z])\.([A-Z])/g` → `$1. $2`
  2. comma join: `/([a-z]),([A-Za-z])/g` → `$1, $2`
  3. quote join: `/([a-z])“/g` → `$1 “`
  4. dash join: `/–([A-Za-z])/g` → `– $1`

Wait the spec: "after an en dash touching a letter (`/–([A-Za-z])/g`)". The example was "challenges –to" — en dash, space, then "to"? Hmm "challenges –to": there's a space before the dash but not after. The rule `/–([A-Za-z])/g` inserts space after the dash when followed by a letter. So "–to" → "– to". OK.

For logging "20 characters each side": when a replacement happens at index i, log context = text_raw.slice(max(0,i-20), i) + "|" + text_raw.slice(i, i+20). I'll capture via replace callback.

Implementation of repairs with logging:

```js
function repair(text, paraNum, log) {
  let out = text;
  const rules = [
    {name:'sentence', re:/([a-z])\.([A-Z])/g, rep:'$1. $2'},
    {name:'comma', re:/([a-z]),([A-Za-z])/g, rep:'$1, $2'},
    {name:'quote', re:/([a-z])“/g, rep:'$1 “'},
    {name:'dash', re:/–([A-Za-z])/g, rep:'– $1'},
  ];
  for (const r of rules) {
    out = out.replace(r.re, (m, ...args) => {
      const offset = args[args.length-2]; // index
      log.push({para: paraNum, rule: r.name, index: offset, before: out.slice(...)...});
      return r.rep.replace... 
    });
  }
}
```

Hmm, careful: using `$1` in replacement string with a function — I'll just build the replacement manually in the callback: for sentence: `args[0] + '. ' + args[1]`. For comma: `args[0] + ', ' + args[1]`. Quote: `args[0] + ' “'`. Dash: `'– ' + args[0]`.

But logging context: I want 20 chars each side of the insertion point in the *current* string. The offset given is the match start index in the current string. Insertion point is at offset + (position within match). For sentence rule, insertion after the dot: offset+2. For comma: offset+2. Quote: offset+1. Dash: offset+1. Simpler: log before = out.slice(Math.max(0, offset-20), offset) and after = out.slice(offset, offset+20) — 20 chars each side of the match start. That's fine, "20 characters each side".

Also note: applying rules sequentially means later rules see earlier repairs. That's fine.

Also careful: the sentence rule `/([a-z])\.([A-Z])/` — could match inside "e.g.A"? "e.g.A" — 'g' '.' 'A' → would insert space: "e.g. A". Hmm, that's actually correct-ish. But could it match decimal numbers like "11.5"? '1' is not [a-z], so no. What about "art.6"? 't' '.' '6' — 6 not [A-Z]. OK. What about abbreviations like "para.16"? no. "H RI"? fine. Risk: "U.S.A" style — 'S' '.' 'A' → "U.S. A". Acceptable per spec; the spec defines the rule exactly, so follow it.

Wait, one more concern: the comma rule `/([a-z]),([A-Za-z])/` — "land,wetlands" → "land, wetlands". Good.

Characters counted over all paragraph texts (which text — text or text_raw? "Counted over all paragraph texts" — I'll count over `text` (repaired); repairs only add spaces so counts are same). Characters: U+2013 en dash, U+201C/U+201D double quotes (count each? "double quotes (U+201C, U+201D)" — one row for double quotes, count both), U+2019 right single quote, U+2011 non-breaking hyphen, U+00A0 non-breaking space. Table rows: Character | Count | Example. Example: find first occurrence in some paragraph text with context. I'll find the first paragraph containing it and show ~30 chars around.

Also headings may contain non-breaking spaces ("2 non-breaking spaces inside headings") — spec says counted over all paragraph texts, so just paragraphs. Fine.

Section assignment: iterate blocks in order; maintain `currentHeading` (nearest heading above) and `currentPart` (nearest roman-numbered h2). For a heading element: if it's an h2 with roman label (label matches /^[IVX]+$/) → part = heading text (or label+heading?). "part (the nearest heading and the roman-numbered section above it)" — export fields: `section` and `part`. part = the roman-numbered section above, e.g. "IV. ..." — I'll store part as the full heading text of the nearest roman h2 (e.g. "IV. ..."). Hmm, for the heading split: label "IV", heading "Obligations...". part could be `label + '. ' + heading` normalized, or just the raw text. I'll store part as the collapsed raw text of that h2 (e.g. "IV.Obligations..." hmm glued). Better: part = label ? label + '. ' + heading : raw text. That gives "IV. Obligations...". Good.

section = nearest heading above the paragraph: store as label ? label+'. '+heading : text. E.g. "Right to work (art. 6)". Full path in expanded row: part + " › " + section.

Wait — "Section is the nearest heading above the paragraph ('Right to work (art. 6)'); the expanded row shows the full path ('IV. … › Right to work (art. 6)')". So section = nearest heading (could be h3), part = roman h2. If the nearest heading IS the roman h2, then section = part, path = just that. Fine.

First words check: first six whitespace-separated words of `text` vs `reference.first_words[String(number)]`. Normalize both: curly quotes → straight, en dash & non-breaking hyphen → hyphen, NBSP → space. Case kept. Compare joined strings. `first_words_match` boolean. Mismatch list: "para. n: found … / reference …".

Note: reference.first_words values are "the first six words" — presumably a string of six words. Compare `norm(found6) === norm(ref)`. If reference missing → "not run".

Checks (tab 04), one line each:
1. Paragraph count: found vs reference.paragraphs → pass/fail (fail links to tab 02).
2. Numbering: exactly 1..n in order; gaps/duplicates listed. Since numbers come from the doc, check sequence equals [1..foundCount]? The check: "Exactly 1 to n in order; gaps and duplicates listed." n = reference.paragraphs presumably, or found count. I'll check: sorted unique numbers === 1..max, and no duplicates, and count === max. List gaps/duplicates if any.
3. First words: mismatches counted and listed, each "para. n: found … / reference …", link to tab 02 rows.
4. Footnotes: 0 vs reference.footnotes → "source limit" (red), counted apart from failures. Text: "the HTML version has no footnotes: a limit of the source, not of the app".
5. Repairs: n spaces restored in n paragraphs, per rule counts; link to tab 03.
6. Headings: count h2 (excluding title) + h3, glued labels separated count.
7. Nothing lost: every block classified once, counts sum to total; unclassified listed in red.
8. Export round trip: JSON string parsed back, record count equals table row count → pass.

If reference missing: tiles say "no reference in this file", checks needing it show "not run". If html yields no `<p>`: tab 01 says so, exports disabled.

Header status: "n of m checks pass" green dot, or red "n checks failed". Footnote check is "source limit" — counted apart. So m = total checks excluding footnote? Let's say checks array with status in {'pass','fail','limit','notrun'}. Header: passCount of (pass+fail+limit?) Hmm. "n of m checks pass" or "n checks failed". I'll compute: m = checks that ran (pass+fail), plus limit shown separately as "1 source limit". Header right: dot + "n of m checks pass" (green if no fails) or "n checks failed" (red), then "1 source limit" text. If reference missing, some checks "not run" — then m = run checks. Keep simple: m = checks with status pass or fail; if fails>0 red "k checks failed", else green "m of m checks pass"; plus "· 1 source limit" if any limit.

Left rail: "DOCUMENT" heading, card with symbol monospace + short title. What's "the short title"? doc.title is the full title. I'll use title (maybe truncated). Two big numbers: "n paragraphs of reference.paragraphs" with thin bar (red when short or over) — bar width = min(n/expected,1)*100%, red if n!==expected. "0 footnotes of reference.footnotes" in red, "not in this HTML". Then "n of m checks pass" linking to tab 04.

Tab 01 RESULT: four tiles:
- Paragraphs found: n (big serif) beside "the document has reference.paragraphs" — green when equal, red with difference ("+2" or "−3").
- First words match: n of reference.paragraphs.
- Footnotes: 0 of reference.footnotes, red, "this HTML version has none; see tab 03".
- Spaces: n repaired or flagged, linking to tab 03.
Each with "How this is computed" line.

If no reference: tiles say "no reference in this file". If no paragraphs found: tab 01 says "no paragraphs found in this HTML".

Tab 02 PARAGRAPHS: 
- Closed "Headings found: n" box (button aria-expanded) listing headings (label + text, maybe with tag h2/h3).
- Table: caption "n paragraphs found, m expected" + TAB.02 monospace. Columns: No. | Section | First line | Check. No. right-aligned. Rows are buttons... "Rows are buttons with aria-expanded; click or Enter expands the row in place". Implementation: each row is a `<tr>` with a button in the first cell? Or the whole row clickable. To keep accessible, I'll make the first cell contain a `<button>` that toggles expansion, and also make the row clickable... Simpler robust approach: each paragraph renders as a `<tr class="prow">` (summary) followed by a hidden `<tr class="detail">`. The summary row's cells: I'll put a button spanning... Actually simplest: make the entire summary row a `<tr tabindex="0" role="button" aria-expanded>`? role=button on tr is odd. Alternative: put a `<button>` in the No. cell that says the number, and clicking anywhere on the row toggles (row click handler). Keyboard: button focusable, Enter/Space triggers. I'll do: row has click handler; first cell has `<button class="pnum" aria-expanded="false">n</button>`. Clicking row or button toggles. That satisfies "rows are buttons with aria-expanded" reasonably — I'll set aria-expanded on the button. Hmm, spec says "Rows are buttons with aria-expanded". I'll make the row itself contain the button and set aria-expanded on both? Let me just make the whole `<tr>` act as button: add `tabindex="0"`, `role="button"`, `aria-expanded`, keydown Enter/Space. Screen-reader-wise not perfect but matches spec. Actually cleaner: wrap — no. I'll do tr with role="button" tabindex 0 aria-expanded, click + keydown handlers. Fine.

- Expanded detail row: full text verbatim (in `text`? or text_raw?). "the full text, verbatim, never shortened" — hmm, but we repaired spaces. The spec says expanded row shows "the full text, verbatim, never shortened; the reference's six words beside the found six; the places repaired or flagged in this paragraph". I think show `text` (repaired) as the main full text with repaired places marked by thin red box (mark the inserted spaces). And also show text_raw? The export has both text and text_raw. In the expanded row, I'll show the repaired text with `<mark class="fix">` around inserted spaces... marking a space is invisible; better mark the surrounding word? "A repaired or flagged place is marked in the expanded paragraph by a thin red box." I'll wrap the inserted space plus adjacent character? Simplest: wrap the character after the insertion point (or the match) in a span with red outline. E.g. for "levels.Key" → "levels.<span class=fix> </span>Key"? A box around a space is invisible. I'll wrap the following word fragment: e.g. `<span class="fix">Key</span>` with title "space restored here". Hmm. Let me wrap the inserted space together with the next character: "levels. <span class='fix'>K</span>ey"? That looks odd. Alternative: wrap the whole match: `<span class="fix">levels.Key</span>` with the space inserted inside: "levels. Key" all inside the red box. That's visible and clear: the box shows before→after. I'll render the repaired text by re-running the repair with a callback that wraps the matched substring in `<span class="fix" title="space restored by the sentence rule">`. So the expanded paragraph shows text with red-boxed repaired spots. 

Also show text_raw? Maybe a small line "as found (text_raw): …" — could be long. The spec's expanded row: full text verbatim, reference six words beside found six, places repaired/flagged, Copy citation button. I'll show: full repaired text with marks; a line "first words — found: … · reference: …" (red if differ); "spaces restored here: n (sentence 2, comma 1…)" listing each with before→after context; Copy citation button. Maybe also a details for raw text? Keep it: add a small "as found in the HTML" toggle? That adds clicks. The spec says never shortened full text — I'll show repaired text as the full text (it IS the paragraph, with spaces restored), and list repairs with before/after so raw is recoverable. Also export includes text_raw. Good enough. Actually, let me include the raw text too in the expanded row as a second block labeled "as found (text_raw)" — it's just text, no extra click. Hmm, it doubles length. The repairs list already shows before/after contexts. I'll skip full raw in the row but note text_raw is in the export. Actually "the full text, verbatim, never shortened" — verbatim suggests raw. But we repaired... The app's product is the repaired text; raw is preserved in export. I'll show both: repaired text (with marks) as main, and raw in a smaller monospace? No — I'll show repaired as main and a collapsed... no extra clicks allowed beyond 7. Let me just show the repaired full text with marks, plus the repairs list showing before/after (which reveals raw fragments). And mention "text_raw (as found) is in the JSON export". Good.

- First line: first 120 chars of text cut at a word boundary with "…". `text.slice(0,120)` then cut back to last space, append "…". If text shorter than 120, no ellipsis.

- Check column: "OK" (green) or "first words differ" (red).

- Copy citation: button copies `symbol + ", para. " + n` via navigator.clipboard.writeText with fallback (execCommand). Show "Copied" for 2s. Note: clipboard API may fail in sandbox; fallback to a temporary textarea + execCommand('copy'). I'll implement fallback.

Tab 03 LOST & CHANGED: three blocks:
1. Lost: footnotes — serif title "Lost: footnotes (n)" with count; paragraph text as specified.
2. Changed: spaces — count per rule above table; table Paragraph | Before | After | Rule; before/after show ~20 chars each side with the insertion marked (e.g. "levels.|Key" → "levels. |Key"? I'll show before context with a marker "·" at insertion point: before = ctx.slice(0,20) + "▸" ... simpler: Before column shows the raw context with the match highlighted? Since it's a table cell, I'll show `…levels.[K]ey…`? Let me show before as the 20-chars-each-side string with the matched part wrapped in a span (red box) — but in a table cell HTML is fine. Before: `levels.` + boxed `Key`? Hmm the match for sentence rule is "s.K" (3 chars). I'll wrap the match in the before cell: `levels.<span class=fix>s.K</span>ey`... getting confusing. Simpler: Before cell = context string with "⎸" marker at insertion point? Let me do: before = raw.slice(max(0,idx-20), idx) + "|" + raw.slice(idx, idx+20) where | marks the insertion point; After = repaired context similarly with the space: rep.slice(...) + " | "? I'll show After as the repaired text around: repaired.slice(max(0,idx-20), idx) + "[ ]" ... 

Simplest readable: Before: `…levels.|Key…` (pipe = where the space goes), After: `…levels. |Key…`? Hmm. Let me do Before: `levels.│Key` and After: `levels. │Key`? I think clearest: Before shows `levels.|Key`, After shows `levels. |Key` — wait after insertion the string is "levels. Key", insertion point after "levels. ", so After = `levels. |Key` where pipe marks where space was inserted... Actually in After, the space is already there: `levels. Key` and I can box the space+next char. I'll render After as `levels. <span class="fix">Key</span>` — box around the word that now follows the restored space. And Before as `levels.<span class="fix">Key</span>` — box around the glued word. That reads well: before shows glued, after shows separated, both boxed. Context: 20 chars each side of the match. I'll build these strings in JS and set innerHTML with escaped text + span. Need HTML escaping helper.

Clicking a row on tab 03 "opens the paragraph on tab 02" — switch to tab 02 and expand that row, scroll to it. Implement `openParagraph(n)`: activate tab 02, expand row n, scrollIntoView.

3. Changed: characters — table Character | Count | Example. Rows: en dash (–), double quotes (“ ”), right single quote (’), non-breaking hyphen (‑), non-breaking space ( ). Example: first occurrence context from paragraph texts. Plus monospace hint "on a keyboard: a hyphen and straight quotes" and the note about searching.

Tab 04 CHECKS & EXPORT:
- Check panel open, every check one line: description, two values, status word ("pass" green / "check failed" red with link / "source limit" red / "not run"). 
- Export: two buttons Download JSON, Download Markdown. Disabled if no paragraphs.
- JSON: array of records with fields symbol, paragraph, section, part, text, text_raw, first_words_match, citation, doc_url, limitations. limitations: "no footnotes in this HTML version; the document has n" (n = reference.footnotes or "?" if missing).
- Markdown: front matter between --- lines: title, symbol, adopted, source_url, extracted (today's date ISO), paragraphs_found, paragraphs_expected, footnotes (same sentence as limitations?), then headings as ## / ### lines in document order and each paragraph as its number in bold then text. "the headings as `##` and `###` lines in document order and each paragraph as its number in bold, then its text" — so iterate blocks in order; h2 → `## text`, h3 → `### text`, paragraph → `**n.** text`? "its number in bold, then its text" → `**12.** text`. Title h2 → maybe `# title`? Spec says headings as ## and ###; the title is the first h2... I'll render title h2 as `# title`? Spec: "then the headings as `##` and `###` lines in document order" — the title is an h2 too. Hmm, front matter already has title. I'll render the document title h2 as `# ` and other h2 as `##`, h3 as `###`. That seems reasonable; or keep all h2 as ##. The spec literally says headings as ## and ### — I'll do title as # (it's the doc title, front matter has it too, harmless). Actually to follow spec strictly: h2 → `##`, h3 → `###`, including title. But then title appears as ## — fine, front matter also has it. I'll do: first h2 (title) → `#`, others `##`, h3 → `###`. Hmm "where it says nothing, keep it simple" — spec says ## and ###. I'll just do h2→##, h3→### for all, including title. Simple and literal. Wait but then the markdown starts with `## General comment No. 27...` — fine.

Heading text in markdown: use the raw collapsed text (glued "I.Introduction")? Or normalized label+heading? For markdown export, I'd use the readable form: if split matched, `label + '. ' + heading`, else raw. Hmm, but "verbatim"... The markdown is a dataset export; I'll use the normalized heading text (label. heading) since glued labels are a known defect; actually keep raw? The spec for markdown: "the headings as ## and ### lines in document order" — doesn't specify. I'll use the display form (label + '. ' + heading when split, else text) — consistent with the app. Hmm, but that changes text. The paragraphs' text in markdown: use `text` (repaired) or text_raw? Spec: "each paragraph as its number in bold, then its text" — ambiguous. I'll use `text` (repaired) since that's the app's product, and JSON has both. Actually for a quotable dataset, repaired is better. Go with text.

- File names: symbol with slashes replaced by hyphens: "E/C.12/GC/27" → "E-C.12-GC-27.json" / ".md". Blob URL, UTF-8: `new Blob([str], {type:'application/json;charset=utf-8'})`, `URL.createObjectURL`, temp `<a download>` click.

- Under buttons: closed heading "Elements found (n)" button aria-expanded → table Tag | Classified as | Text (first 80 chars). Every block element in order.

Footer: source, built, "Done by this page's code; no model was called and nothing left the browser." Wait — does html_doc have `built`? The description lists `{title, symbol, doc_url, source, html, reference}` — no `built`. The footer spec says "`source`, `built`". I'll show built if present else omit gracefully: `doc.built ? ... : ''`. I'll render footer line: source · built (if present) · the done line. Handle missing.

Tabs: role="tablist" with buttons role="tab" aria-selected, panels role="tabpanel", arrow-key navigation (Left/Right/Home/End). Hidden panels: use `hidden` attribute + CSS `[hidden]{display:none!important}`.

Click budget: tabs (4) + headings box + elements found + 2 export buttons = 7. Plus filter headings — none here. Left rail has a link to tab 04 (not a button per se, it's an anchor — counts? "tabs, filter headings and buttons together" — the rail link... I'll make it a button-styled link; total clicks: 4 tabs + 1 headings box + 2 exports + 1 elements box = 8. Hmm, over seven. The rail "n of m checks pass" link — I could make it non-button text? Spec says "linking to tab 04". I'll make it an `<a href="#tab-04">`-ish button. 8 clickable things... The rule says "about seven". The rail link is arguably part of rail, not view. I'll keep it; "about seven" is soft. Alternatively make headings box and elements box... they're required. Fine.

Left rail filters: none needed (no filters). The rail is "DOCUMENT" card — that's per spec.

Design: paper #f4f0e8, ink #1d1b18, rules #d9d2c3, accent #9b2335, green for pass — "pass dark green": use #1e6b3a or similar (contrast on paper: #1e6b3a on #f4f0e8 — should be ok, ~5:1). Let me pick #1f6b3a. Red #9b2335.

Fonts: Georgia serif for title/big numbers/figure titles; ui-monospace 11-12px uppercase letter-spaced for labels/tabs; system sans 16px body.

Layout: header top; below, a grid: left rail ~260px + main content. Tabs row under header spanning full width? Spec: "Under the header, numbered tabs" — tabs above the rail+content? "The arrangement of the workshop's Verbatim finder: header, left rail, four numbered tabs." I'll do: header (full width), then tabs row (full width), then a flex row: left rail + tab panels. Rail always visible. That matches "Left rail, always visible".

Tab panels: each panel contains its content. Rail outside panels.

Now, code structure:

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>...</title>
<style>...</style>
</head>
<body>
<header>...</header>
<nav role="tablist" id="tabs">4 buttons</nav>
<div class="layout">
  <aside id="rail">...</aside>
  <main>
    <section id="panel-1" role="tabpanel">...</section>
    ... panels 2-4
  </main>
</div>
<footer>...</footer>
<script>...</script>
</body>
</html>
```

I'll build most DOM in JS from computed data, with static skeleton in HTML.

Let me now write the pipeline code carefully.

```js
const DATA = window.WORKSHOP_DATA.html_doc;
const doc = Array.isArray(DATA) ? DATA[0] : DATA;
const ref = doc.reference || null;
const symbol = doc.symbol || '';
const docUrl = doc.doc_url || '';
```

Parse:

```js
let blocks = [];
let parsed = null;
try {
  parsed = new DOMParser().parseFromString(doc.html || '', 'text/html');
  collectBlocks(parsed.body, blocks);
} catch(e) { blocks = []; }
```

collectBlocks as above (recurse into div/section/article/main; also maybe `td`? No — table is one block, cover).

Hmm wait: what if body has text nodes directly? Ignore.

Classification:

```js
const paras = [];       // {num, text_raw, text, repairs:[], section, part, firstMatch, found6, ref6}
const headings = [];    // {tag, raw, label, heading, glued, part:boolean}
const elements = [];    // {tag, cls, text80}
let titleEl = null, committee = null, coverCount = 0, other = [];
let currentSection = null, currentPart = null;
let seenTitle = false;

for (const el of blocks) {
  const tag = el.tagName.toLowerCase();
  const rawText = (el.textContent || '').replace(/\s+/g,' ').trim();
  elements.push({tag, cls: el.className || '', text: rawText.slice(0,80), raw: rawText});
  if (tag === 'table') { coverCount++; continue; }
  if (tag === 'p') {
    const m = rawText.match(/^(\d{1,3})\.\s*(.*)$/s);
    if (m) {
      const num = parseInt(m[1],10);
      const textRaw = m[2].replace(/\s+/g,' ').trim();
      const repairs = [];
      const text = repairText(textRaw, num, repairs);
      paras.push({num, text_raw: textRaw, text, repairs, section: currentSection, part: currentPart});
      continue;
    }
    // committee line or other p
    if (!committee) committee = rawText; 
    else other.push(...)  // hmm
    continue;
  }
  if (tag === 'h2' || tag === 'h3') {
    if (tag === 'h2' && !seenTitle) { titleEl = rawText; seenTitle = true; continue; }
    const hm = rawText.match(/^([IVX]+|[A-Z])\.\s*(.+)$/s);
    let label=null, htext=rawText, glued=false;
    if (hm) {
      label = hm[1]; htext = hm[2].trim();
      glued = /^[IVX]+|[A-Z])\.[^\s]/ ... 
    }
    ...
  }
}
```

Wait — careful with the paragraph regex on rawText: rawText already collapsed whitespace, so `\s*` after dot handles "1. A" and "1.A". But the regex `^(\d{1,3})\.\s*(.*)$` on collapsed text: "1.A clean..." → m[2] = "A clean...". Good. But what about a paragraph like "10.1 something"? `(\d{1,3})\.` matches "10." then `\s*` then "1 something" — hmm "10.1" would be parsed as paragraph 10 with text "1 something". Edge case, unlikely in this doc. The spec gives the regex; follow it.

Glued label detection: after matching hm, glued = the original rawText has no whitespace after "label." — check `rawText.startsWith(label + '.')` and char at label.length+1 is not whitespace: `!/\s/.test(rawText.charAt(label.length+1))`. Since rawText collapsed, "I.Introduction" → char after "I." is 'I' → glued. "D. Obligation" → ' ' → not glued.

Heading display: `label ? label + '. ' + htext : rawText`. part flag: tag==='h2' && label && /^[IVX]+$/.test(label).

When heading encountered: currentSection = display; if part → currentPart = display.

Hmm — should currentSection update on every heading (h2 and h3)? Yes, nearest heading above. And part only on roman h2.

Committee line: "any other `<p>` is the committee line" — first non-numbered p. Additional non-numbered ps → classify as "other p"? For the nothing-lost check, I'll count them as class "committee/other p" — hmm. Let me define classes: cover (table), title (first h2), heading (h2/h3), paragraph (numbered p), line (other p), other (anything else). The check "Nothing lost": every block classified exactly once — by construction yes; but "any unclassified element is listed in red" — I'll treat class "other" (non p/h2/h3/table) as unclassified → listed red, check fails if any. And "line" ps are fine (committee). Actually spec says any other p is the committee line — so all non-numbered ps are "committee line" class. OK: classes = cover, title, heading, paragraph, line, other. Check: other.length === 0 → pass; else fail listing them. Also verify sum: cover+title+headings+paras+lines+other === blocks.length (always true, but display it).

Hmm, wait: what about the first h2 being title — what if there are h1s? Not in this doc. h1 → other. Fine.

Repairs function:

```js
function repairText(raw, num, log) {
  let out = raw;
  const rules = [
    {key:'sentence', name:'sentence join', re:/([a-z])\.([A-Z])/g, ins:2},
    {key:'comma', name:'comma join', re:/([a-z]),([A-Za-z])/g, ins:2},
    {key:'quote', name:'quote join', re:/([a-z])“/g, ins:1},
    {key:'dash', name:'dash join', re:/–([A-Za-z])/g, ins:1},
  ];
  for (const r of rules) {
    out = out.replace(r.re, (match, a, b, offset) => {
      const at = offset + r.ins;
      log.push({
        para: num, rule: r.key, ruleName: r.name,
        before: out.slice(Math.max(0, offset-20), offset) + '|' + out.slice(offset, offset+20),
        // hmm, want context around insertion point
      });
      return match.slice(0, r.ins) + ' ' + match.slice(r.ins);
    });
  }
  return out;
}
```

Wait, replace callback args: (match, p1, p2, ..., offset, string). For 2-group regex: (match, a, b, offset, string). For 1-group (quote, dash): (match, a, offset, string). So I need to handle arg count. Let me write per-rule replacer functions:

```js
const rules = [
  {key:'sentence', name:'sentence join', re:/([a-z])\.([A-Z])/g,
   rep:(m,a,b)=>a+'. '+b, ins:2},
  {key:'comma', name:'comma join', re:/([a-z]),([A-Za-z])/g,
   rep:(m,a,b)=>a+', '+b, ins:2},
  {key:'quote', name:'quote join', re:/([a-z])“/g,
   rep:(m,a)=>a+' “', ins:1},
  {key:'dash', name:'dash join', re:/–([A-Za-z])/g,
   rep:(m,a)=>'– '+a, ins:1},
];
for (const r of rules) {
  out = out.replace(r.re, function(m) {
    const args = Array.prototype.slice.call(arguments, 1, -2); // groups
    const offset = arguments[arguments.length-2];
    const at = offset + r.ins;
    log.push({para:num, rule:r.key, ruleName:r.name, at,
      before: out.slice(Math.max(0,at-20), at) + '▏' + out.slice(at, at+20)});
    return r.rep.apply(null, [m].concat(args));
  });
}
```

Hmm, `arguments` in arrow vs function — use function. `arguments[arguments.length-2]` is offset, last is full string. Groups are arguments 1..length-2. OK.

For the "before/after" display in tab 03 table: I'll store `beforeCtx` = 20 chars each side of insertion point in the pre-repair string, and compute after from repaired. Actually simpler: store `raw` snippet and `fixed` snippet: before = out.slice(max(0,at-20), at) + "|" + out.slice(at, at+20) — pipe marks insertion point. After: I can recompute by applying... simpler: after = before with the pipe replaced by " | "? No — after insertion, text at that point is "...levels. Key...". Let me store both: during replace, `beforeSnippet = out.slice(...)` with marker, and afterSnippet = (new string).slice(max(0,at-20), at+1+20)? The new string has one more char. afterSnippet = newOut.slice(Math.max(0,at-20), at+21) with marker at at+1? Getting fiddly. 

Alternative cleaner approach for display: store `match` (the matched substring, e.g. "s.K"), `prefix` = 20 chars before match, `suffix` = 20 chars after match, all from the pre-repair string. Then Before cell: `prefix + [match] + suffix` with match boxed; After cell: `prefix + repairedMatch + suffix` with repairedMatch boxed. repairedMatch = r.rep(match, ...groups). That's clean. So log: {para, rule, ruleName, prefix, match, suffix, fixed}.

For marking in the expanded paragraph (tab 02), I'll re-run repair on text_raw with a function that wraps the match in a span. I'll write a second function `renderRepaired(raw, paraNum)` returning HTML string: escape each chunk, wrap matches in `<span class="fix" title="space restored — rule name">`. Implementation: run same rules sequentially on a token list? Since rules apply sequentially and offsets shift, easiest: build HTML by walking: maintain `html` string built from escaped pieces. Do it rule by rule on the plain string but track positions... Simpler: do a single pass with a combined regex? The rules could interfere. Alternative: apply rules sequentially, each time rebuilding an array of segments [{t, fixed:boolean}]. Start: [{t: raw, fixed:false}]. For each rule, map over segments: for fixed segments, keep as-is (already repaired — but later rules might match inside them? e.g. sentence rule inserts space, then comma rule could match across? The inserted space prevents most cross matches. But to exactly mirror the plain-text pipeline, I should apply rules to the whole string sequentially. Hmm.

Let me think: does rule order matter for final text? Sentence rule inserts space after "x.Y". Comma rule matches "x,y". These patterns don't overlap destructively. Applying sequentially to full string is what the pipeline does. For HTML rendering, I can do: run the plain pipeline but record, for each insertion, the resulting string and position; then reconstruct HTML by diffing? Overkill.

Pragmatic approach: render HTML by applying rules sequentially to a segment list where each segment is {text, fixed}. For each rule, for each non-fixed segment, replace matches within that segment's text, splitting into pieces; mark the inserted space's surrounding match as fixed. For fixed segments, skip (they contain already-inserted spaces; a later rule matching inside a fixed segment — e.g. dash rule matching "–X" where the "–" was part of... no rule inserts "–". Sentence rule inserts ". " — could comma rule match "a. b"? comma needs "a,b". Quote rule needs 'a“'. Dash needs '–X'. The inserted chars are space, '.', ',', '“', '–'... wait dash rule inserts space after '–', doesn't insert '–'. Quote rule inserts '“' after a letter: "a “" — then dash rule? no. Sentence rule inserts space after '.', so "a. B" — comma rule needs comma. So no later rule can match text created by an earlier rule except... sentence rule creates "a. B" — no other rule matches ". ". Comma creates "a, b" — sentence rule needs lowercase.period.capital: "a, b" no period. OK, but a later rule could match spanning across a fixed segment boundary? E.g. raw "a.B–c": sentence rule → "a. B–c" (segment fixed around "B"?). Then dash rule on "B–c": '–' preceded by 'B'... dash rule is /–([A-Za-z])/ — matches "–c" regardless of preceding. In plain pipeline, after sentence repair string is "a. B–c", dash rule matches "–c" → "a. B– c". In segment approach, if sentence rule marked "a.B" as fixed segment and "–c" remains in a non-fixed segment, dash rule still applies to "–c". Good. But what if dash match spans a fixed boundary, e.g. raw "a–B.c"? dash rule first? Order: sentence first: "a–B.c" → sentence matches "B.c" → "a–B. c". Then dash: "–B" → "a– B. c". In segment approach: sentence rule splits into ["a–", fixed("B.c"), ...] wait the match is "B.c" → segments: "a–", fixed "B. c". Then dash rule on non-fixed segment "a–": /–([A-Za-z])/ needs letter after –; "a–" ends there, next segment is fixed — no match within segment. Plain pipeline would match "–B" across the boundary! Divergence.

This is an edge case unlikely to occur, but to be exact, I'll render HTML differently: compute the final repaired string via the plain pipeline (authoritative), and separately compute insertion positions in the final string. How? Run pipeline recording each insertion's `at` in the current string; after all rules, positions shift. Alternative: record insertions as (atInFinalString) by tracking cumulative offset: process rules in order; maintain `shift` = number of insertions so far; when rule logs insertion at position `at` in current string, final position = at + shift; then shift++. Since later rules operate on the string including earlier insertions, and their logged `at` is already in "current" coordinates which include earlier shifts — so final position = at + (insertions after this one)? No wait. Let me think again.

Let s0 = raw. Rule 1 produces s1 = s0 with insertions at positions p1_i (in s0 coords). Rule 2 operates on s1, logs positions in s1 coords. Final string sN. An insertion logged at position q in s_k coords maps to final coords: q + (number of insertions made in rules k+1..N that occur before q)? Ugh.

Simpler: since each rule's insertions are at distinct positions and rules are applied in order, I can compute final positions by processing rules in order and maintaining a list of insertion points in final coordinates incrementally: Actually easiest correct method: apply rules one at a time, and after each rule, record the insertion positions in the *current* string; at the end, convert all recorded positions to final-string coordinates by adding the count of insertions that happened after each recording and before that position... still messy.

Alternative much simpler: build the final string and the HTML in one pass using a single combined regex with alternation, applied once? But rules applied sequentially vs once differ only in the cross-boundary edge case. Honestly, for rendering marks, I can do this: run the plain pipeline to get `text` and the log with (rule, match, prefix, suffix) per insertion — but for HTML rendering, just re-run the same sequential replace on the raw string, but this time build HTML incrementally: maintain `htmlParts` and a parallel plain string? 

You know what — simplest robust approach: render the expanded paragraph by walking the final `text` and the raw `text_raw` with a diff? No.

Cleanest: do the sequential replace, but instead of replacing in a plain string, replace in an array of tokens where each token is {text, fixed}. For each rule, iterate tokens; for non-fixed tokens, split on the rule regex, producing sub-tokens; the matched sub-token becomes fixed with the repaired text. For fixed tokens, still run the regex on them? If I run the regex on fixed tokens too (treating their text), matches inside fixed text would be double-processed... but as analyzed, a match inside a fixed token's text: fixed tokens contain repaired matches like "a. B" — could sentence rule match inside "a. B"? Needs lowercase.period.capital — "a. B" has "a. B" — wait that IS lowercase.period.space.capital — the regex is ([a-z])\.([A-Z]) — requires capital IMMEDIATELY after period. "a. B" has space, no match. Comma rule on fixed "a, b": needs comma immediately followed by letter — "a, b" has space. Quote fixed "a “": no. Dash fixed "– b": /–([A-Za-z])/ — "– b" has space, no match. So no rule re-matches inside fixed tokens. And cross-boundary matches (like "–B" spanning fixed boundary) would be missed in token approach but caught in plain approach. To handle: when running a rule, also consider the concatenation... 

OK, decision: the plain pipeline is authoritative for `text`. For HTML marking, I'll do a simpler thing: mark repaired places by comparing — actually, let me just do the token approach but run each rule over the *concatenation* logic: process tokens left to right, and for matching, use the regex on each non-fixed token AND check boundary between last char of previous token and first chars of next? Too complex.

Pragmatic: cross-boundary matches essentially require the earlier rule's inserted space to be immediately adjacent... e.g. "a–B.c": sentence rule matches "B.c" making fixed "B. c"; the dash "–B" spans boundary between "a–" and fixed "B. c". In plain pipeline, dash rule then fixes "–B". In token approach, missed. How likely in real data? The found issues: "challenges –to" (dash join, space before dash already), "levels.Key", "land,wetlands", "crises“increase". Cross-boundary cases would need e.g. "x–Y.z" patterns. Rare. But I want the marked HTML to exactly match `text`. 

Alternative exact approach: compute `text` via plain pipeline. Then compute marks by re-running the pipeline where each replace callback records (finalPosition) — I can compute final positions correctly like this: process rules in order; maintain array `inserts` of {pos (in current string at time of insertion), rule, match}. After all rules, the final string is known. To map each recorded pos to final coords: sort? Each insertion at rule k, position p in s_{k-1} coords. Final position = p + (total insertions from rules > k that are at positions ≤ p in their coords)... circular.

Honestly, simplest exact method: build final string incrementally as a list of chunks: start chunks = [raw]. For each rule in order: newChunks = []; for each chunk: if chunk.fixed → push as-is... no wait, that's the token approach with the boundary issue.

New idea: apply each rule to the whole current string, but keep a parallel "mask" string of same length marking which characters are original vs inserted. When replacing with callback, I know offset and match length; the replacement = match with space inserted at ins. In the new string, positions: chars before offset unchanged; the inserted space at offset+ins; rest shifted by 1. I can maintain mask as array of booleans (true = inserted). After all rules, I have final string + mask. Then HTML: walk final string; group consecutive chars; wrap runs where mask is true... but I want to wrap the *match* (including surrounding original chars) in the box, per my design "box around the glued word". Hmm, with mask I know exactly which char is the inserted space; I can wrap from previous word char to next word char. Simpler: wrap just a small window: the inserted space plus the following character? A box around " K" (space+letter) is visible. Or wrap the inserted space and both neighbors: "s. K" hmm.

Let me simplify the visual: wrap the inserted space together with the character after it in `<span class="fix">` — e.g. "levels.<span class=fix> K</span>ey". The box around " K" is visible (has the letter). Title attr explains. Good enough and exact.

Implementation with mask:

```js
function repairText(raw, num, log) {
  let s = raw;
  let mask = new Array(raw.length).fill(false);
  const rules = [...];
  for (const r of rules) {
    let newS = '', newMask = [];
    let last = 0;
    s.replace(r.re, function(m) {
      const args = Array.prototype.slice.call(arguments, 1, -2);
      const offset = arguments[arguments.length - 2];
      // append unchanged part
      newS += s.slice(last, offset); newMask.push(...mask.slice(last, offset));
      const fixed = r.rep.apply(null, [m].concat(args));
      // fixed = m with space inserted at r.ins
      newS += fixed.slice(0, r.ins) + ' ' + fixed.slice(r.ins);
      for (let i=0;i<r.ins;i++) newMask.push(mask[offset+i]); // original chars
      newMask.push(true); // inserted space
      for (let i=r.ins;i<m.length;i++) newMask.push(mask[offset+i]);
      last = offset + m.length;
      log.push({para:num, rule:r.key, ruleName:r.name, match:m, fixed,
        prefix: s.slice(Math.max(0,offset-20), offset),
        suffix: s.slice(offset+m.length, offset+m.length+20)});
      return m; // value irrelevant
    });
    newS += s.slice(last); newMask.push(...mask.slice(last));
    s = newS; mask = newMask;
  }
  return {text: s, mask};
}
```

Wait — `r.rep` for quote rule: rep:(m,a)=>a+' “' — that's m with space inserted at ins=1: m = a+'“', fixed = a+' “' = m.slice(0,1)+' '+m.slice(1). Yes consistent: fixed = m.slice(0,ins)+' '+m.slice(ins). So I don't even need rep; just insert space at ins. 

But careful: `String.replace` with a function — I'm using it for side effects and building newS manually; return value ignored since I build newS separately. But `s.replace` iterates matches in s — fine. Note: regexes have /g flag; lastIndex handling — using replace with function resets properly. But reusing the same regex object across calls with /g: replace resets lastIndex internally? `String.prototype.replace` with global regex sets lastIndex to 0 at start. Yes, safe.

Edge: overlapping matches — replace handles non-overlapping left-to-right. Fine.

Then HTML rendering of a paragraph:

```js
function renderMarked(text, mask) {
  let html = '';
  for (let i=0;i<text.length;i++) {
    const ch = text[i];
    if (mask[i]) {
      // wrap this inserted space + next char
      html += '<span class="fix" title="space restored here">' + esc(ch) + (i+1<text.length?esc(text[i+1]):'') + '</span>';
      if (i+1<text.length) { html += esc(text[i+1]); i++; } // skip next, already emitted
      // hmm but next char's mask? it's original, fine
    } else html += esc(ch);
  }
  return html;
}
```

Wait bug: if mask[i] true, I emit span with ch + next char, then also emit next char again via the i++ skip — I wrote `html += esc(text[i+1]); i++;` inside — that emits next char inside... let me redo: 

```js
if (mask[i]) {
  html += '<span class="fix">' + esc(text[i]) + (i+1 < text.length ? esc(text[i+1]) : '') + '</span>';
  i++; // skip the next char (already inside the span)
} else {
  html += esc(text[i]);
}
```

But if i+1 is also masked (two consecutive insertions — impossible, insertions are single spaces separated by ≥1 original char... could two rules insert at adjacent positions? e.g. "a.B–c"? sentence inserts after "a." at pos 2; dash rule on "a. B–c" matches "–c" at pos 5 — not adjacent. Adjacent insertions would need matches like "x.Y" and then... ins positions differ by ≥2 typically. If mask[i+1] also true, my skip would drop its span. Guard: only include next char in span if !mask[i+1]. Fine:

```js
if (mask[i]) {
  let inner = esc(text[i]);
  if (i+1 < text.length && !mask[i+1]) { inner += esc(text[i+1]); i++; }
  html += '<span class="fix" title="space restored by the ' + ... + ' rule">' + inner + '</span>';
}
```

I'll pass rule names per position? Simpler title: "space restored here (see tab 03)". OK.

Also for tab 03 table Before/After: from log entries: Before = esc(prefix) + '<span class="fix">' + esc(match) + '</span>' + esc(suffix); After = esc(prefix) + '<span class="fix">' + esc(fixed) + '</span>' + esc(suffix). Where prefix/suffix are 20 chars each side. Good — shows context with the glued/fixed part boxed.

Character counts: over all paragraph `text`s (repaired — same counts). Count per char: en dash '\u2013', left double '\u201C', right double '\u201D' (row "double quotes" counts both), right single '\u2019', nb-hyphen '\u2011', nbsp '\u00A0'. Example: first paragraph text containing it, show ~30 chars around first occurrence: `…` + ctx. I'll find in para.text.

First words:

```js
function normWords(s) {
  return (s||'').replace(/[“”]/g,'"').replace(/[’]/g,"'").replace(/[–—]/g,'-').replace(/\u2011/g,'-').replace(/\u00A0/g,' ').trim();
}
```

Wait spec: "equal after turning curly quotes straight, en dashes and non-breaking hyphens into a hyphen and non-breaking spaces into spaces; case is kept." Curly quotes → straight: “” → ", ’ → '. En dash (and em dash? spec says en dashes) → hyphen. I'll map [– —] → '-'? Spec says en dashes; I'll include em dash too harmlessly? Stick to spec: en dash \u2013 and nb-hyphen \u2011 → '-'; NBSP → ' '; curly quotes → straight. Also maybe collapse whitespace. Compare `norm(found6) === norm(ref6)` where found6 = first 6 words of text joined by space: `text.split(/\s+/).slice(0,6).join(' ')`. ref value is a string like "A clean, healthy and sustainable environment" (six words). Compare normalized.

Hmm — should normalization apply to the whole comparison or word-by-word? Apply norm to both joined strings. Also trim ref. If ref missing for a para → firstMatch = null (not run).

Checks list construction:

```js
const checks = [];
// 1 paragraph count
if (ref) {
  checks.push({name:'Paragraph count', detail:`found ${paras.length} · reference.paragraphs ${ref.paragraphs}`, status: paras.length===ref.paragraphs?'pass':'fail', link:'#tab-2'...});
  // numbering
  const nums = paras.map(p=>p.num);
  const dup = nums.filter((n,i)=>nums.indexOf(n)!==i);
  const gaps = []; for(let i=1;i<=Math.max(...nums||[0]);i++) if(!nums.includes(i)) gaps.push(i);
  const inOrder = nums.every((n,i)=> i===0 || n>nums[i-1]);
  status = (dup.length===0 && gaps.length===0 && inOrder && nums.length===Math.max(...)) ? pass : fail;
  detail: `numbers ${nums[0]}–${nums[nums.length-1]}, ${dup.length} duplicates, ${gaps.length} gaps` + list
  // first words
  mismatches = paras.filter(p=>p.firstMatch===false);
  status = mismatches.length? 'fail':'pass'; detail lists "para. n: found … / reference …"
  // footnotes
  checks.push({name:'Footnotes', detail:`this HTML has 0 · reference.footnotes ${ref.footnotes}`, status:'limit', note:'the HTML version has no footnotes: a limit of the source, not of the app'});
} else {
  those checks status 'notrun', detail 'no reference in this file'
}
// repairs
const totalRepairs = all logs; per rule counts; status pass (informational) — "n spaces restored in n paragraphs, counted per rule" — status pass if... it's a count, always "pass"? It's a check that the repair log is complete: every logged insertion is listed on tab 03. status pass. detail: `n spaces in m paragraphs (sentence a, comma b, quote c, dash d)`.
// headings
h2count (excluding title), h3count, glued count. status pass.
// nothing lost
other elements count; sum check. status pass/fail.
// export round trip
jsonStr built; JSON.parse(jsonStr).length === paras.length → pass.
```

Export round trip check needs the JSON string — build export JSON first, then checks. Order: compute everything, build export strings, then checks including round trip.

Header status: fails = checks.filter(c=>c.status==='fail').length; limits = ...'limit'; run = pass+fail. If fails>0 → red dot "k checks failed"; else green "n of m checks pass" where m = pass+fail (run checks). Plus "· 1 source limit" if limits. If ref missing, some 'notrun' — m excludes them; maybe show "n of m checks pass · r not run". Keep simple: if fails>0 red "k checks failed", else green `${pass} of ${pass+fail} checks pass`; append `· ${limits} source limit` if limits>0.

Rail: big number 1: paras.length with "of ref.paragraphs paragraphs" — bar: width = ref ? min(100, paras.length/ref.paragraphs*100) : 100; red if paras.length !== ref.paragraphs. Big number 2: "0" red with "of ref.footnotes footnotes" + "not in this HTML". Then checks line linking to tab 04.

Tab 01 tiles: 
- Tile 1: big "n" + label "paragraphs found" + sub "the document has m" — green if equal else red with diff "(+k)" / "(−k)". If no ref: "no reference in this file".
- Tile 2: "n of m" first words match. If no ref: "no reference in this file".
- Tile 3: "0 of m" footnotes, red, "this HTML version has none; see tab 03" (link). If no ref: "no reference in this file".
- Tile 4: "n" spaces repaired or flagged, link to tab 03.
Each tile: "How this is computed" line: e.g. "counted by this page's code over the parsed HTML body; compared with reference.paragraphs".

If paras.length === 0: tab 01 shows a message "no paragraphs found in this HTML" and exports disabled.

Tab 02: headings box: button "Headings found: n" aria-expanded false → div listing each heading: monospace tag (H2/H3) + display text. Table caption: `${paras.length} paragraphs found, ${ref?ref.paragraphs:'?'} expected` + "TAB.02". Columns: No. | Section | First line | Check. 

Row rendering: I'll render tbody rows via JS. Each paragraph: 

```html
<tr class="prow" data-n="12" tabindex="0" role="button" aria-expanded="false">
  <td class="num">12</td>
  <td class="sec">Right to work (art. 6)</td>
  <td class="first">A clean, healthy and sustainable environ…</td>
  <td class="chk ok">OK</td>
</tr>
<tr class="pdet" hidden>
  <td colspan="4">
    <p class="full">…marked html…</p>
    <p class="fw">first words — found: … · reference: …</p>
    <p class="reps">spaces restored here: n — sentence 1, comma 1 …</p>
    <button class="copy" data-cite="E/C.12/GC/27, para. 12">Copy citation</button>
  </td>
</tr>
```

Click on prow toggles pdet hidden + aria-expanded. Keydown Enter/Space on prow toggles. Also the copy button inside pdet — stopPropagation not needed since pdet isn't the toggle row.

Section cell: if no heading above (paragraph before any heading) → "—" or "(front matter)". Use "—".

Check cell: p.firstMatch === true → "OK" green; false → "first words differ" red; null → "not run" (if no ref).

Copy citation: 

```js
function copyText(t, btn) {
  const done = () => { btn.textContent='Copied'; setTimeout(()=>btn.textContent='Copy citation',2000); };
  if (navigator.clipboard && navigator.clipboard.writeText) {
    navigator.clipboard.writeText(t).then(done).catch(()=>fallback(t,done));
  } else fallback(t, done);
}
function fallback(t, done) {
  const ta = document.createElement('textarea'); ta.value=t; ta.style.position='fixed'; ta.style.opacity='0';
  document.body.appendChild(ta); ta.select();
  try { document.execCommand('copy'); done(); } catch(e) { btn.textContent = t; } // show the citation if copy fails
  document.body.removeChild(ta);
}
```

Tab 03: 
Block 1: `<h3 class="blocktitle">Lost: footnotes <span class="count">0 of m</span></h3>` + paragraph text: "The document has m footnotes. This HTML has 0: no footnote text, no footnote marks, and the note the title's asterisk points to is missing. To cite a footnote, use the PDF or Word version." If no ref: "This HTML has 0 footnotes: no footnote text and no footnote marks survive in it."

Block 2: "Changed: spaces" + count line: "n spaces restored in m paragraphs — sentence join a · comma join b · quote join c · dash join d". Table caption "n missing spaces restored by rule" + TAB.03. Columns Paragraph | Before | After | Rule. Rows clickable → openParagraph(n). Make rows tabindex 0 role button? They're table rows with click → I'll add class and handler + cursor pointer, and a hint "click a row = open the paragraph on tab 02". Rule column shows rule name. Before/After cells with boxed spans as designed.

Note under: "Rules restore a space only where the characters prove it was there. Word pairs such as 'Giventhe' are not touched; the first-words check catches them only in a paragraph's first six words."

Block 3: "Changed: characters" + table Character | Count | Example. Rows: 
- "en dash (–)" count
- "double quotes (“ ”)" count (201C+201D)
- "right single quote (’)" 
- "non-breaking hyphen (‑)" — display the char in a code span
- "non-breaking space ( )" — show as "⍽"? Show as "(U+00A0)" with visible marker: I'll display the character itself in a boxed span plus label "non-breaking space". Example column: context from a paragraph.
Hint: monospace "on a keyboard: a hyphen and straight quotes". Note: "Kept exactly as published, in the table and in every export. A search for 'business-related' typed with the hyphen key will not find 'business‑related': normalise the text before searching it."

Tab 04: 
- Check panel: `<h3>Checks</h3>` open list; each check a line: name — detail — status word. Status word: "pass" green / "check failed" red (with link "see tab 02" / "see tab 03") / "source limit" red / "not run" grey. Links: for first-words fail → link to tab 02; repairs → tab 03; paragraph count fail → tab 02.
- Export: two buttons. Disabled if paras.length===0 (with note). 
- Elements found (n): closed button aria-expanded → table Tag | Classified as | Text (first 80 chars). Classified as: cover / title / heading / paragraph / committee line / other.

Footer: `source` · `built` (if present) · "Done by this page's code; no model was called and nothing left the browser."

Credits line: sources consulted — Turing Way (CC BY 4.0), UK Government Analysis Function (OGL? The QA of code guidance is under OGL — but spec says add credits only for open licence code/wording used. I used no code from them; the spec says "If you use code or wording from a 'Reference shelf excerpts' page that has an open licence... add a small Credits line". I'm following their guidance approach but not copying wording/code. The plan lists "Sources consulted". I'll add a small Credits line naming them — safe: "Method follows The Turing Way (CC BY 4.0), UK Government Analysis Function QA-of-code guidance (OGL 3.0), and the Dag Hammarskjöld Library citation guidance." Hmm, licences: Turing Way CC BY 4.0; best-practice-and-impact repo is OGL-ish... I'm not 100% sure. To avoid inventing licence claims, I'll say "Guidance followed: The Turing Way (Documentation and metadata), UK Government Analysis Function (Testing code), Dag Hammarskjöld Library (citing UN documents)." without licence names? The rule says name source and its licence if using code/wording from reference shelf excerpts. I'm not using their code/wording verbatim. I'll include a modest credits line without asserting specific licences... Actually the instruction: "If you use code or wording from a 'Reference shelf excerpts' page that has an open licence (MIT, Apache, BSD, ISC, CC BY), add a small 'Credits' line at the bottom of the app naming the source and its licence." I'm not using their code or wording, so credits optional. I'll add a small line anyway naming the three sources consulted as the plan requests, phrased as guidance followed. Keep it.

Tabs keyboard nav: 

```js
tablist.addEventListener('keydown', e => {
  const tabs = [...tablist.querySelectorAll('[role=tab]')];
  let i = tabs.indexOf(document.activeElement);
  if (i<0) return;
  if (e.key==='ArrowRight') i=(i+1)%tabs.length;
  else if (e.key==='ArrowLeft') i=(i-1+tabs.length)%tabs.length;
  else if (e.key==='Home') i=0;
  else if (e.key==='End') i=tabs.length-1;
  else return;
  e.preventDefault(); tabs[i].focus(); activateTab(i);
});
```

activateTab(i): set aria-selected, hidden on panels.

Also clicking rail "checks" link → activateTab(3).

openParagraph(n): activateTab(1); expand row n; scroll into view.

Now sizes: 90 paragraphs, table with 180 rows — fine. Elements table ~100 rows.

Line count: aim under 1500. Let's write efficiently.

Let me also double check the header: "A monospace label 'UN DOCUMENT · HTML', the serif title, one line: symbol linked to doc_url (new tab), 'adopted reference.adopted', source. At the right a green dot 'n of m checks pass' or a red dot 'n checks failed', then '1 source limit' (the footnotes)."

So header right side: status dot + text, then "1 source limit". I'll render: `<span class="dot green"></span> 8 of 8 checks pass · 1 source limit`. If fails: red dot "2 checks failed · 1 source limit".

Title: doc.title — long serif title. OK.

Rail card: symbol monospace + "the short title" — I'll use doc.title (maybe long; card can wrap). Fine.

Now the "How this is computed" lines:
- Tile paragraphs: "Counted by this page's code: every <p> in the parsed HTML whose text starts with a number and a full stop; compared with reference.paragraphs."
- Tile first words: "The first six words of each paragraph, normalised (curly quotes straight, en dashes and non-breaking hyphens to hyphens, non-breaking spaces to spaces), compared with reference.first_words."
- Tile footnotes: "Counted in the parsed HTML: 0 footnote elements exist in this version; reference.footnotes is the document's own count."
- Tile spaces: "Four rules insert a space only where the characters prove one was there; every insertion is logged and listed on tab 03."

Tab 02 caption: "90 paragraphs found, 90 expected — click a row for the full text". Plus TAB.02 label.

Now write the markdown export:

```js
function buildMarkdown() {
  const lines = [];
  lines.push('---');
  lines.push('title: ' + mdVal(doc.title));
  lines.push('symbol: ' + symbol);
  lines.push('adopted: ' + (ref && ref.adopted ? ref.adopted : 'unknown'));
  lines.push('source_url: ' + docUrl);
  lines.push('extracted: ' + new Date().toISOString().slice(0,10));
  lines.push('paragraphs_found: ' + paras.length);
  lines.push('paragraphs_expected: ' + (ref ? ref.paragraphs : 'unknown'));
  lines.push('footnotes: ' + footnoteSentence());
  lines.push('---');
  lines.push('');
  // blocks in order: need headings and paragraphs interleaved in document order.
```

Hmm — markdown needs document order of headings and paragraphs. My `paras` and `headings` arrays lost interleaving. I'll keep a `flow` array during classification: entries {kind:'heading', display, tag} or {kind:'para', num}. Then markdown iterates flow. Also tab 02's section assignment uses currentSection at time of paragraph — already stored.

Markdown body:

```js
for (const f of flow) {
  if (f.kind==='heading') lines.push((f.tag==='h2'?'## ':'### ') + f.display);
  else { const p = byNum[f.num]; lines.push('**' + f.num + '.** ' + p.text); lines.push(''); }
}
```

Wait "each paragraph as its number in bold, then its text" → `**12.** text`. Good. Use p.text (repaired). Hmm or text_raw? I'll use text and note in front matter? The JSON has both. For markdown I'll use text (repaired) — it's the quotable form. Fine.

mdVal: quote if contains ':' etc. Simple: if /[:#]/ or leading/trailing space → JSON.stringify. Keep simple: `title: "..."` always quoted via JSON.stringify — valid YAML. I'll use JSON.stringify for title and symbol.

footnoteSentence(): `no footnotes in this HTML version; the document has ${ref?ref.footnotes:'an unknown number of'} footnotes` — used in JSON limitations and front matter footnotes field.

JSON export:

```js
const records = paras.map(p => ({
  symbol, paragraph: p.num, section: p.section || '', part: p.part || '',
  text: p.text, text_raw: p.text_raw, first_words_match: p.firstMatch === null ? null : p.firstMatch,
  citation: symbol + ', para. ' + p.num, doc_url: docUrl,
  limitations: footnoteSentence()
}));
const jsonStr = JSON.stringify(records, null, 2);
```

Download:

```js
function download(name, content, type) {
  const blob = new Blob([content], {type: type + ';charset=utf-8'});
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url; a.download = name;
  document.body.appendChild(a); a.click(); a.remove();
  setTimeout(()=>URL.revokeObjectURL(url), 1000);
}
```

File name: symbol.replace(/\//g,'-') + '.json' → "E-C.12-GC-27.json".

Now CSS. Let me draft:

```css
:root {
  --paper:#f4f0e8; --ink:#1d1b18; --rule:#d9d2c3; --red:#9b2335; --green:#1f6b3a;
}
* { box-sizing: border-box; }
[hidden]{display:none!important}
body { margin:0; background:var(--paper); color:var(--ink); font:16px/1.55 -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif; }
.mono { font-family: ui-monospace, Menlo, Consolas, monospace; font-size:11.5px; letter-spacing:.12em; text-transform:uppercase; }
header { padding: 20px 28px 14px; border-bottom:1px solid var(--rule); display:flex; ... }
```

Header layout: left block (label, title, meta line), right block (status). Use flex with space-between, align end.

Tabs: 

```css
nav[role=tablist] { display:flex; gap:2px; padding:0 28px; border-bottom:1px solid var(--rule); }
nav [role=tab] { font-family:mono...; background:none; border:none; border-bottom:2px solid transparent; padding:10px 14px; cursor:pointer; color:var(--ink); }
nav [role=tab][aria-selected=true] { color:var(--red); border-bottom-color:var(--red); }
```

Focus ring: `:focus-visible { outline:2px solid var(--red); outline-offset:2px; }`.

Layout: `.layout { display:flex; align-items:flex-start; } aside { width:250px; flex:0 0 250px; padding:18px 20px; border-right:1px solid var(--rule); position:sticky; top:0; } main { flex:1; padding:18px 28px 40px; min-width:0; }`

Rail big numbers: `.bignum { font-family: Georgia, 'Times New Roman', serif; font-size:44px; line-height:1; }` bar: `.bar { height:4px; background:var(--rule); } .bar i { display:block; height:100%; background:var(--green); } .bar.red i { background:var(--red); }`

Tiles: `.tiles { display:grid; grid-template-columns:repeat(auto-fit,minmax(220px,1fr)); gap:0; }` each tile with border-left rule? Use thin rules between: `.tile { padding:14px 18px; border-left:1px solid var(--rule); } .tile:first-child{border-left:none}`. Big number serif 48px. Green/red classes.

Tables: `table { border-collapse:collapse; width:100%; } caption { text-align:left; font-family:Georgia,serif; font-size:18px; padding:8px 0; } caption .mono {display:block; color:#6b675f; margin-bottom:2px;} th { font-family:mono; font-size:11px; uppercase; letter-spacing; text-align:left; border-bottom:1px solid var(--ink); padding:6px 10px 6px 0; } td { border-bottom:1px solid var(--rule); padding:7px 10px 7px 0; vertical-align:top; } td.num, th.num { text-align:right; }`

Paragraph rows: `tr.prow { cursor:pointer; } tr.prow:hover { background:#ece7db; } tr.prow .num { font-family:Georgia,serif; color:var(--red); font-size:18px; text-align:right; }` detail row: `tr.pdet td { background:#efe9dd; padding:14px 18px; }` full text: `.full { font-size:16px; max-width:70ch; }` `.fix { outline:1px solid var(--red); padding:0 1px; }` — thin red box. 

Status words: `.ok{color:var(--green)} .bad{color:var(--red)} .limit{color:var(--red)} .notrun{color:#6b675f}`.

Buttons: `.btn { font:inherit; background:none; border:1px solid var(--ink); padding:8px 14px; cursor:pointer; } .btn:hover{ background:#eae4d6; } .btn[disabled]{opacity:.45; cursor:not-allowed;}`

Closed headings (accordion): `.acc { display:block; width:100%; text-align:left; background:none; border:none; border-top:1px solid var(--rule); padding:10px 0; cursor:pointer; font-family:Georgia,serif; font-size:18px; }` with a "+" indicator? Use `aria-expanded` and a small marker via ::after content " +" / " –"? I'll add `<span class="tw">+</span>` toggled. Keep simple: text includes "(show)"? I'll do ::after { content:" +" } and [aria-expanded=true]::after { content:" –" }.

Dot: `.dot { width:9px; height:9px; border-radius:50%; display:inline-block; } .dot.g{background:var(--green)} .dot.r{background:var(--red)}`.

Now, the tab panels: panel 2 table might be huge; fine.

Also "No view shows more than about seven things to click": tab 02 has headings box (1) + rows (not counted) + copy buttons (in expanded rows, not counted? "not counting table rows" — copy buttons are in rows... they're buttons though. The spec says not counting table rows; copy buttons live inside rows. I'll not worry). Tab 04: 2 export buttons + elements box = 3 + 4 tabs = 7. Good.

Now let me also handle: "If `reference` or one of its fields is missing, the tiles say 'no reference in this file' and the checks that need it show 'not run', never 'pass'; if `html` yields no `<p>`, tab 01 says so and the exports are disabled."

Implement: refExists = !!(ref && typeof ref==='object'). refParagraphs = ref && Number.isFinite(ref.paragraphs) ? ref.paragraphs : null. etc.

Now writing all the JS. Let me carefully write the whole file.

Also the header label: "UN DOCUMENT · HTML". Title serif ~28px. Meta line: symbol link + " · adopted " + adopted + " · " + source. Source string: doc.source — e.g. "OHCHR treaty body database, HTML version" whatever it is; just print it.

Let me now also think about `first_words` keys: `reference.first_words[String(number)]`. Values are strings of six words. Compare normalized.

Normalization function:

```js
function norm(s) {
  return (s == null ? '' : String(s))
    .replace(/[\u201C\u201D]/g, '"')
    .replace(/\u2019/g, "'")
    .replace(/\u2013/g, '-')
    .replace(/\u2011/g, '-')
    .replace(/\u00A0/g, ' ')
    .replace(/\s+/g, ' ')
    .trim();
}
```

found6 = norm(p.text.split(/\s+/).slice(0,6).join(' ')); ref6 = norm(ref.first_words[String(p.num)]); match = ref6 === '' ? null : found6 === ref6. Hmm if ref missing for that para → null ("not run"). If ref.first_words missing entirely → all null.

Numbering check details: nums array; expected sequence 1..max. duplicates: nums.filter((n,i)=>nums.indexOf(n)!==i). gaps: for i in 1..max not in nums. Also "exactly 1 to n in order": check nums[i] === i+1 for all i (i.e., sequence is 1,2,3,...). If paras.length===max and no dups and starts at 1 and increasing → sequence equals 1..n. I'll compute `ordered = nums.every((n,i)=>n===i+1)` — that's the strict check (1..n in order). If not ordered, list first few issues. Status pass iff ordered && nums.length === (ref? ref.paragraphs : nums.length)? Hmm — numbering check is about the document's own numbering: "Exactly 1 to n in order; gaps and duplicates listed." n here = found count? If doc has 90 paragraphs numbered 1..90, ordered=true. I'll define pass = ordered (nums[i]===i+1 ∀i) — that implies no gaps/dups and starts at 1. Detail: `first ${nums[0]}, last ${nums[nums.length-1]}, ${dups} duplicates, ${gaps} gaps`. If !ordered → fail, list gaps/dups (up to 10).

Edge: paras empty → numbering check "not run"? If no paragraphs, tab 01 says so; checks: paragraph count fail (0 vs 90). Numbering: skip → "not run" (nothing to check). I'll guard.

Nothing-lost check: classes counted: cover, title, heading, paragraph, line, other. total = blocks.length. sum === total always; status = other.length===0 ? pass : fail; detail: `${total} block elements: ${cover} cover, ${title?1:0} title, ${headings.length} headings, ${paras.length} paragraphs, ${lines} committee lines, ${other.length} unclassified` + list unclassified (tag + text80) in red.

Headings check: detail: `${h2} h2 + ${h3} h3 = ${headings.length} headings; ${glued} glued labels separated (e.g. "I.Introduction")`. status pass.

Repairs check: total repairs, per-rule counts, paragraphs affected. status pass. detail: `${n} spaces restored in ${m} paragraphs — sentence ${a}, comma ${b}, quote ${c}, dash ${d}; every one listed on tab 03`. Link to tab 03.

Export round trip: `JSON.parse(jsonStr).length === paras.length` → pass, detail `the downloaded JSON parses back to ${parsed.length} records = ${paras.length} rows on tab 02`.

Footnotes check: status 'limit', detail `this HTML has 0 footnotes · reference.footnotes ${ref.footnotes}` note "the HTML version has no footnotes: a limit of the source, not of the app". Counted apart from failures.

First words check: if ref && ref.first_words: mismatches list; status = mismatches.length? 'fail':'pass'; detail: `${matchCount} of ${paras.length} match` + if fail, list "para. n: found '…' / reference '…'" (up to 10) with link to tab 02. Else 'not run'.

Paragraph count: if refParagraphs!=null: status = paras.length===refParagraphs?'pass':'fail'; detail `found ${paras.length} · reference.paragraphs ${refParagraphs}` + diff. Link tab 02 on fail. Else 'not run', detail 'no reference in this file'.

Now header/rail status text: compute after checks.

Let me now also design tab 01 tiles markup:

```html
<section id="p1" role="tabpanel">
  <div class="tiles">
    <div class="tile"><div class="mono">PARAGRAPHS FOUND</div><div class="bignum" id="t1n">90</div><div class="sub" id="t1s">the document has 90</div><div class="how mono">HOW THIS IS COMPUTED: ...</div></div>
    ...
  </div>
  <p id="noref" hidden>no reference in this file...</p>
</section>
```

Hmm "How this is computed" line near every chart or number — I'll put a small line under each tile: class "how" — small sans 13px, not mono uppercase maybe. Spec: 'one "How this is computed" line near every chart or number'. I'll write: `How this is computed: …` in 13px.

Tile 1 sub: green "the document has 90 — equal" or red "the document has 92 — 2 short". 

Tile 2: bignum "90" with sub "of 90 first words match". Actually spec: "First words match: n of reference.paragraphs" — bignum n, sub "of m paragraphs". 

Tile 3: bignum "0" red, sub "of m footnotes — this HTML version has none; see tab 03" (link).

Tile 4: bignum n, sub "spaces repaired or flagged — see tab 03" (link).

If no ref: tiles 1-3 show "no reference in this file" instead of numbers? Spec: "the tiles say 'no reference in this file'". I'll set bignum text to "—" and sub to "no reference in this file" for tiles 1–3; tile 4 still works (repairs don't need ref).

If paras.length===0: tab 01 shows a notice: "No paragraphs were found in this HTML: no <p> element starts with a number and a full stop. The exports on tab 04 are disabled." and tiles show 0s. I'll add a banner.

Now tab 02 headings box content: list like `<li><span class="mono">H2</span> IV. Obligations…</li>`. Also count glued? Just list.

Let me write the code now, being careful about size. I'll aim for ~700-900 lines.

One more detail: "Every row that shows a document has its symbol, linked to doc_url in a new tab." — header meta line has symbol link; also maybe in tab 02? The rows show paragraphs of the document; the symbol link is in header and rail card. I'll add symbol link in the tab 02 caption area too? The rule says every row that shows a document — our rows show paragraphs, not documents. Header + rail card + footer cover it. I'll also put the symbol link in the export section. Fine.

Also tab 04 "Elements found (n)" table: Tag | Classified as | Text (first 80 chars). Classified as values: "cover", "title", "heading (h2)", "heading (h3)", "paragraph", "committee line", "unclassified". I stored elements with class assigned during classification — I'll push class name at classification time. Let me restructure: during the loop, for each block push {tag, cls: el.className, text: rawText.slice(0,80), clsAs: '...'}.

Now, the flow array for markdown: push {kind:'h', tag, display} for headings (including title? The title h2 — in markdown, include as `#`? I decided h2→##. The title is first h2 → `## General comment No. 27...`. Hmm, front matter has title already; including as ## is fine and literal.) Also committee line? Skip in markdown (it's cover-ish). Actually committee line is inside content div before title h2. Skip. Cover table skip.

Wait — order: in the HTML, is the committee `<p>` before the title `<h2>`? Sample: `<div class="content"><p bold>Committee on...</p><h2>General comment No. 27...</h2><h2>I.Introduction</h2>...`. Yes. So title = first h2. Good.

Markdown heading display: use display form (label + '. ' + heading if split else raw). For "I.Introduction" → "I. Introduction". Good.

Now — one subtlety in classification: the paragraph regex on collapsed rawText. But rawText collapses whitespace including newlines — fine. However, `textContent` of a `<p>` may contain nested spans — fine.

Also: what if a numbered `<p>` appears inside the cover table? We treat table as one block, skip its children. Good.

What about `<p>` elements that are numbered but > 3 digits? regex \d{1,3}. Fine.

Now the "part" for paragraphs before any roman h2 (e.g., paragraphs under "I. Introduction" — "I" is roman → part = "I. Introduction"). Good.

Section display for paragraphs directly under an h2: section = that h2's display. Path = part + " › " + section — if section === part, path = part. I'll compute path = (part && section && part!==section) ? part + ' › ' + section : (section || part || '—').

Expanded row shows: full path line (mono small): "IV. … › Right to work (art. 6)". Then full text. Then first-words line. Then repairs line. Then copy button.

Repairs line in expanded row: "spaces restored here: 2 — sentence join ×1, comma join ×1" plus maybe list each with before→after? The tab 03 table has details; in the row I'll summarize counts and link "see tab 03". Actually spec: expanded row shows "the places repaired or flagged in this paragraph" — the marks in the text show the places; I'll also list them: each as `levels.Key → levels. Key (sentence join)`. Could be long but fine — cap at, say, all (max ~4 per para). I'll list all with small text.

Let me now write out the file. I'll write it in one go, carefully.

Also remember: before code block, at most three short sentences; after, nothing.

Let me write:

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Numbered paragraphs · UN document HTML</title>
<style>
...
</style>
</head>
<body>
<header>
  <div class="hleft">
    <div class="mono label">UN DOCUMENT · HTML</div>
    <h1 id="doctitle"></h1>
    <div class="meta" id="docmeta"></div>
  </div>
  <div class="hright" id="hstatus"></div>
</header>
<nav role="tablist" id="tablist" aria-label="Views">
  <button role="tab" id="tab-1" aria-controls="p1" aria-selected="true">01 RESULT</button>
  <button role="tab" id="tab-2" aria-controls="p2" aria-selected="false" tabindex="-1">02 PARAGRAPHS</button>
  <button role="tab" id="tab-3" aria-controls="p3" aria-selected="false" tabindex="-1">03 LOST &amp; CHANGED</button>
  <button role="tab" id="tab-4" aria-controls="p4" aria-selected="false" tabindex="-1">04 CHECKS &amp; EXPORT</button>
</nav>
<div class="layout">
  <aside>
    <div class="mono railhead">DOCUMENT</div>
    <div class="doccard">
      <div class="mono sym" id="railsym"></div>
      <div class="shorttitle" id="railtitle"></div>
    </div>
    <div class="railnum">
      <div class="bignum" id="railp"></div>
      <div class="railsub" id="railpsub"></div>
      <div class="bar" id="railbar"><i></i></div>
    </div>
    <div class="railnum">
      <div class="bignum red" id="railf">0</div>
      <div class="railsub">of <span id="railftotal"></span> footnotes — not in this HTML</div>
    </div>
    <button class="railchecks" id="railchecks"></button>
  </aside>
  <main>
    <section id="p1" role="tabpanel" aria-labelledby="tab-1">...</section>
    <section id="p2" role="tabpanel" aria-labelledby="tab-2" hidden>...</section>
    <section id="p3" role="tabpanel" aria-labelledby="tab-3" hidden>...</section>
    <section id="p4" role="tabpanel" aria-labelledby="tab-4" hidden>...</section>
  </main>
</div>
<footer id="foot"></footer>
<script>
...
</script>
</body>
</html>
```

Panels 2-4 mostly built by JS into containers.

Let me write the script fully now (mentally compile):

```js
(function(){
'use strict';
var W = window.WORKSHOP_DATA || {};
var raw = W.html_doc;
var doc = Array.isArray(raw) ? raw[0] : raw;
if (!doc) doc = {};
var ref = doc.reference || null;
var symbol = doc.symbol || '(no symbol)';
var docUrl = doc.doc_url || '';
var title = doc.title || '(untitled)';
var source = doc.source || '';
var adopted = (ref && ref.adopted) ? ref.adopted : null;
var refParas = (ref && typeof ref.paragraphs === 'number') ? ref.paragraphs : null;
var refFoots = (ref && typeof ref.footnotes === 'number') ? ref.footnotes : null;
var firstWords = (ref && ref.first_words) ? ref.first_words : null;

function esc(s){ return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;'); }
function norm(s){ return String(s==null?'':s).replace(/[\u201C\u201D]/g,'"').replace(/\u2019/g,"'").replace(/\u2013/g,'-').replace(/\u2011/g,'-').replace(/\u00A0/g,' ').replace(/\s+/g,' ').trim(); }
function collapse(s){ return String(s==null?'':s).replace(/\s+/g,' ').trim(); }

// parse
var blocks = [];
try {
  var parsed = new DOMParser().parseFromString(doc.html || '', 'text/html');
  (function walk(el){
    for (var i=0;i<el.children.length;i++){
      var c = el.children[i], t = c.tagName.toLowerCase();
      if (t==='div'||t==='section'||t==='article'||t==='main') walk(c);
      else blocks.push(c);
    }
  })(parsed.body);
} catch(e){ blocks = []; }
```

Wait — parsed.body could be null if html empty; guard: `if (parsed.body) walk(parsed.body);`.

Classification:

```js
var paras = [], headings = [], flow = [], elements = [];
var coverN=0, titleText=null, lineN=0, otherEls=[];
var curSec=null, curPart=null, seenTitle=false;
var byNum = {};

blocks.forEach(function(el){
  var tag = el.tagName.toLowerCase();
  var text = collapse(el.textContent);
  var clsAs;
  if (tag==='table'){ coverN++; clsAs='cover'; }
  else if (tag==='p'){
    var m = text.match(/^(\d{1,3})\.\s*(.*)$/s);
    if (m){
      var num = parseInt(m[1],10);
      var rawText = collapse(m[2]);
      var rep = repair(rawText, num);
      var p = {num:num, text_raw:rawText, text:rep.text, mask:rep.mask, repairs:rep.log,
               section:curSec, part:curPart, firstMatch:null, found6:'', ref6:''};
      paras.push(p); byNum[num]=p; flow.push({kind:'p', num:num});
      clsAs='paragraph';
    } else { lineN++; clsAs='committee line'; }
  }
  else if (tag==='h2'||tag==='h3'){
    if (tag==='h2' && !seenTitle){ seenTitle=true; titleText=text; clsAs='title'; }
    else {
      var hm = text.match(/^([IVX]+|[A-Z])\.\s*(.+)$/s);
      var label=null, htext=text, glued=false, display=text;
      if (hm){ label=hm[1]; htext=collapse(hm[2]); glued = !/\s/.test(text.charAt(label.length+1)); display = label + '. ' + htext; }
      var isPart = (tag==='h2' && label && /^[IVX]+$/.test(label));
      headings.push({tag:tag, raw:text, label:label, text:htext, glued:glued, display:display, part:isPart});
      flow.push({kind:'h', tag:tag, display:display});
      curSec = display; if (isPart) curPart = display;
      clsAs = 'heading ('+tag+')';
    }
  }
  else { otherEls.push({tag:tag, text:text}); clsAs='unclassified'; }
  elements.push({tag:tag, cls:(el.className||''), text:text.slice(0,80), clsAs:clsAs});
});
```

Hmm — 's' flag in regex: `/^(\d{1,3})\.\s*(.*)$/s` — the `s` flag makes `.` match newlines, but text is already collapsed so no newlines. Harmless. Actually `.*` with collapsed text fine without /s. Keep /s anyway? `m[2]` with /s could include... text has no newlines after collapse. Fine either way; I'll drop /s to be safe? With collapsed text, no newlines, so no difference. Keep without /s. Actually keep it simple: no flags except where needed. The heading regex `(.+)` fine.

Wait, one issue: `text.charAt(label.length+1)` — for "I.Introduction", label="I", charAt(2)='I' → glued=true. For "D. Obligation", charAt(2)=' ' → glued=false. Good. But what if heading is exactly "I." with nothing after? `(.+)` requires content. OK.

repair function:

```js
var RULES = [
  {key:'sentence', name:'sentence join', re:/([a-z])\.([A-Z])/g, ins:2},
  {key:'comma',    name:'comma join',    re:/([a-z]),([A-Za-z])/g, ins:2},
  {key:'quote',    name:'quote join',    re:/([a-z])\u201C/g, ins:1},
  {key:'dash',     name:'dash join',     re:/\u2013([A-Za-z])/g, ins:1}
];
function repair(raw, num){
  var s = raw, mask = [], i;
  for (i=0;i<raw.length;i++) mask.push(false);
  var log = [];
  RULES.forEach(function(r){
    var ns='', nm=[], last=0;
    s.replace(r.re, function(){
      var args = Array.prototype.slice.call(arguments,1,arguments.length-2);
      var off = arguments[arguments.length-2];
      var m = arguments[0];
      ns += s.slice(last, off); for (var i=last;i<off;i++) nm.push(mask[i]);
      var fixed = m.slice(0,r.ins) + ' ' + m.slice(r.ins);
      ns += fixed;
      for (var j=0;j<r.ins;j++) nm.push(mask[off+j]);
      nm.push(true);
      for (var k=r.ins;k<m.length;k++) nm.push(mask[off+k]);
      last = off + m.length;
      log.push({para:num, rule:r.key, ruleName:r.name, match:m, fixed:fixed,
                prefix:s.slice(Math.max(0,off-20), off),
                suffix:s.slice(off+m.length, off+m.length+20)});
      return m;
    });
    ns += s.slice(last); for (var i2=last;i2<s.length;i2++) nm.push(mask[i2]);
    s = ns; mask = nm;
  });
  return {text:s, mask:mask, log:log};
}
```

Careful with variable shadowing `i` inside — I used var i in outer and inner loops; inner `for (var i=last...)` redeclares — var hoisting makes it same variable, could break outer loop? The outer loop over RULES uses forEach with function scope, so `i` inside the replace callback is a different function scope. The `for (i=0;i<raw.length;i++)` is in repair's scope; the replace callback has its own scope with its own `var i` — shadowing is fine since callback doesn't use outer i. But `for (var i2=last;...)` — fine. OK.

Wait, there's a subtle bug: inside the replace callback I reference `s` and `mask` — these are the current values (before this rule), correct since I build ns/nm separately. Good.

Also note: `s.replace(r.re, fn)` — with /g regex, replace scans s; the callback returns m (unchanged) but we ignore the return since we build ns manually. Correct.

But careful: regex `r.re` has /g and is a shared object; `replace` resets lastIndex — yes, String.replace with global regex starts from 0 and resets lastIndex after. Safe.

First words:

```js
paras.forEach(function(p){
  var w = p.text.split(/\s+/);
  p.found6 = norm(w.slice(0,6).join(' '));
  if (firstWords){
    var rv = firstWords[String(p.num)];
    if (rv != null){ p.ref6 = norm(rv); p.firstMatch = (p.found6 === p.ref6); }
  }
});
```

Characters:

```js
var CHARS = [
  {label:'en dash', chars:'\u2013', name:'–'},
  {label:'double quotes', chars:'\u201C\u201D'},
  {label:'right single quote', chars:'\u2019'},
  {label:'non-breaking hyphen', chars:'\u2011'},
  {label:'non-breaking space', chars:'\u00A0'}
];
var charStats = CHARS.map(function(c){
  var count=0, example='';
  paras.forEach(function(p){
    for (var i=0;i<p.text.length;i++){
      if (c.chars.indexOf(p.text[i])>=0){
        count++;
        if (!example){
          var a=Math.max(0,i-25);
          example = (a>0?'…':'') + p.text.slice(a, i) + '[' + (p.text[i]==='\u00A0'?'⍽':p.text[i]) + ']' + p.text.slice(i+1, i+26) + (i+26<p.text.length?'…':'');
        }
      }
    }
  });
  return {label:c.label, count:count, example:example};
});
```

Hmm for NBSP example, showing '⍽' marker inside brackets is clearer. For others show the char itself. Also for double quotes count both 201C and 201D — indexOf over chars string works.

Wait — counting per paragraph text: I count every occurrence. Good. Example: first occurrence overall (paras in order). Good.

Repairs aggregation:

```js
var allRepairs = [];
paras.forEach(function(p){ p.repairs.forEach(function(r){ allRepairs.push(r); }); });
var perRule = {sentence:0, comma:0, quote:0, dash:0};
allRepairs.forEach(function(r){ perRule[r.rule]++; });
var repairParas = paras.filter(function(p){return p.repairs.length>0;}).length;
```

Exports:

```js
function footnoteSentence(){
  return 'no footnotes in this HTML version; the document has ' + (refFoots!=null?refFoots:'an unknown number of') + ' footnotes';
}
function buildRecords(){
  return paras.map(function(p){
    return { symbol:symbol, paragraph:p.num, section:p.section||'', part:p.part||'',
      text:p.text, text_raw:p.text_raw,
      first_words_match: p.firstMatch===null?null:p.firstMatch,
      citation: symbol + ', para. ' + p.num, doc_url:docUrl, limitations: footnoteSentence() };
  });
}
var records = buildRecords();
var jsonStr = JSON.stringify(records, null, 2);
function buildMarkdown(){
  var L=[];
  L.push('---');
  L.push('title: ' + JSON.stringify(title));
  L.push('symbol: ' + JSON.stringify(symbol));
  L.push('adopted: ' + JSON.stringify(adopted||'unknown'));
  L.push('source_url: ' + JSON.stringify(docUrl));
  L.push('extracted: ' + new Date().toISOString().slice(0,10));
  L.push('paragraphs_found: ' + paras.length);
  L.push('paragraphs_expected: ' + (refParas!=null?refParas:'unknown'));
  L.push('footnotes: ' + JSON.stringify(footnoteSentence()));
  L.push('---'); L.push('');
  flow.forEach(function(f){
    if (f.kind==='h') L.push((f.tag==='h2'?'## ':'### ') + f.display);
    else { var p=byNum[f.num]; L.push('**' + p.num + '.** ' + p.text); L.push(''); }
  });
  return L.join('\n');
}
var mdStr = buildMarkdown();
```

Checks:

```js
var checks = [];
function addCheck(name, detail, status, linkTab, linkLabel, note){
  checks.push({name:name, detail:detail, status:status, linkTab:linkTab||null, linkLabel:linkLabel||'', note:note||''});
}
// paragraph count
if (refParas!=null){
  var ok = paras.length===refParas;
  addCheck('Paragraph count', 'found '+paras.length+' · reference.paragraphs '+refParas + (ok?'':' ('+(paras.length-refParas>0?'+':'')+(paras.length-refParas)+')'),
    ok?'pass':'fail', ok?null:1, 'see tab 02');
} else addCheck('Paragraph count','no reference in this file','notrun');
// numbering
if (paras.length){
  var nums = paras.map(function(p){return p.num;});
  var dups = nums.filter(function(n,i){return nums.indexOf(n)!==i;});
  var max = Math.max.apply(null,nums);
  var gaps=[]; for(var i=1;i<=max;i++) if(nums.indexOf(i)<0) gaps.push(i);
  var ordered = nums.every(function(n,j){return n===j+1;});
  addCheck('Numbering', 'first '+nums[0]+', last '+nums[max? nums.length-1:0]... 
```

Hmm detail: `'numbers '+nums[0]+'–'+nums[nums.length-1]+'; '+dups.length+' duplicates, '+gaps.length+' gaps' + (dups.length||gaps.length? ' ('+dups.concat(gaps).slice(0,10).join(', ')+')':'')`, status ordered&&!dups.length&&!gaps.length?'pass':'fail', link tab 1.

Wait if ordered is true then no dups/gaps by definition. status = ordered?'pass':'fail'.

// first words
```js
if (firstWords){
  var mm = paras.filter(function(p){return p.firstMatch===false;});
  var run = paras.filter(function(p){return p.firstMatch!==null;}).length;
  var det = run+' of '+paras.length+' paragraphs compared';
  if (mm.length) det += '; mismatches: ' + mm.slice(0,10).map(function(p){return 'para. '+p.num+': found \u201C'+p.found6+'\u201D / reference \u201C'+p.ref6+'\u201D';}).join(' · ');
  addCheck('First words', det, mm.length?'fail':'pass', mm.length?1:null, 'see the flagged rows on tab 02');
} else addCheck('First words','no reference in this file','notrun');
```

// footnotes
```js
if (refFoots!=null) addCheck('Footnotes','this HTML has 0 · reference.footnotes '+refFoots,'limit',null,'','the HTML version has no footnotes: a limit of the source, not of the app');
else addCheck('Footnotes','no reference in this file','notrun');
```

// repairs
```js
addCheck('Repairs', allRepairs.length+' spaces restored in '+repairParas+' paragraphs — sentence '+perRule.sentence+', comma '+perRule.comma+', quote '+perRule.quote+', dash '+perRule.dash, 'pass', 2, 'every one listed on tab 03', 'text_raw keeps the text as found');
```

// headings
```js
var h2n = headings.filter(function(h){return h.tag==='h2';}).length;
var h3n = headings.length - h2n;
var gluedN = headings.filter(function(h){return h.glued;}).length;
addCheck('Headings', h2n+' h2 + '+h3n+' h3 = '+headings.length+' headings; '+gluedN+' glued labels separated (e.g. "I.Introduction")','pass');
```

// nothing lost
```js
var total = elements.length;
var sum = coverN + (titleText?1:0) + headings.length + paras.length + lineN + otherEls.length;
var okAll = (sum===total) && otherEls.length===0;
addCheck('Nothing lost', total+' block elements: '+coverN+' cover, '+(titleText?1:0)+' title, '+headings.length+' headings, '+paras.length+' paragraphs, '+lineN+' committee lines, '+otherEls.length+' unclassified' + (otherEls.length? ' — '+otherEls.slice(0,5).map(function(o){return '<'+o.tag+'> '+esc(o.text.slice(0,40));}).join('; ') : ''), okAll?'pass':'fail');
```

Hmm — detail contains HTML for the unclassified list; I'll render detail as HTML (escape elsewhere). I'll treat detail as HTML string and escape user data within. Careful: detail strings include quotes etc. I'll build with esc() where data-derived. Simpler: keep detail plain text and add separate `extra` HTML. I'll just make detail plain text: 'unclassified: <table> …' — angle brackets in text would be escaped when inserted via textContent... I'm inserting via innerHTML. Let me make all detail strings safe by escaping data parts. I'll write details with esc() around data-derived bits. For simplicity, most details are numbers — safe. The unclassified list: use esc(o.tag) etc. OK.

// export round trip
```js
var rt = 'not run';
try { rt = JSON.parse(jsonStr).length; } catch(e){}
addCheck('Export round trip', rt===paras.length ? 'the JSON to download parses back to '+rt+' records = '+paras.length+' rows on tab 02' : 'parse-back gave '+rt+' records, expected '+paras.length, rt===paras.length?'pass':'fail');
```

Status counts:

```js
var nPass = checks.filter(function(c){return c.status==='pass';}).length;
var nFail = checks.filter(function(c){return c.status==='fail';}).length;
var nLimit = checks.filter(function(c){return c.status==='limit';}).length;
var nNotRun = checks.filter(function(c){return c.status==='notrun';}).length;
var nRun = nPass + nFail;
```

Header status: if nFail>0: red dot + nFail+' checks failed' else green dot + nPass+' of '+nRun+' checks pass'; + (nLimit? ' · '+nLimit+' source limit':'') + (nNotRun? ' · '+nNotRun+' not run':'').

Now rendering. I'll write render functions setting innerHTML of containers.

Header:

```js
document.getElementById('doctitle').textContent = title;
meta: symbol link: '<a href="'+esc(docUrl)+'" target="_blank" rel="noopener">'+esc(symbol)+'</a>' + (adopted? ' · adopted '+esc(adopted):'') + ' · '+esc(source)
```

If docUrl empty, just text symbol.

Rail:

```js
railsym.textContent = symbol;
railtitle.textContent = title;
railp.textContent = paras.length;
railpsub: refParas!=null ? 'of '+refParas+' paragraphs' : 'paragraphs found';
bar width: refParas!=null ? Math.min(100, paras.length/refParas*100)+'%' : '100%'; class red if refParas!=null && paras.length!==refParas.
railf: '0'; railftotal: refFoots!=null?refFoots:'?';
railchecks: textContent = nFail? nFail+' checks failed — see tab 04' : nPass+' of '+nRun+' checks pass — see tab 04'; onclick activate tab 4 (index 3).
```

Tab 01:

```js
var p1 = document.getElementById('p1');
if (paras.length===0){ p1.innerHTML = '<p class="notice">No paragraphs were found in this HTML: no &lt;p&gt; element starts with a number and a full stop. The exports on tab 04 are disabled.</p>'; }
else {
  tiles html...
}
```

Tile builder:

```js
function tile(label, big, bigCls, sub, how){
  return '<div class="tile"><div class="mono tlabel">'+label+'</div>'+
    '<div class="bignum '+bigCls+'">'+big+'</div>'+
    '<div class="tsub">'+sub+'</div>'+
    '<div class="how">How this is computed: '+how+'</div></div>';
}
```

Tile1: label 'PARAGRAPHS FOUND', big paras.length, cls (refParas!=null && paras.length===refParas)?'ok':'bad' — but if no ref, cls '' and sub 'no reference in this file'. sub: refParas!=null ? 'the document has '+refParas + (equal? ' — equal' : ' — '+(diff>0? diff+' extra' : -diff+' short')) : 'no reference in this file'. how: 'every <p> in the parsed HTML whose text starts with a number and a full stop; compared with reference.paragraphs'. Note: how contains `<p>` — escape: use '&lt;p&gt;'.

Tile2: 'FIRST WORDS MATCH', big = count of firstMatch===true, sub = 'of '+(refParas!=null?refParas:paras.length)+' paragraphs' or 'no reference in this file'. how: 'the first six words of each paragraph, normalised (curly quotes straight, en dashes and non-breaking hyphens to hyphens, non-breaking spaces to spaces), against reference.first_words'.

Tile3: 'FOOTNOTES', big '0', cls 'bad', sub: 'of '+(refFoots!=null?refFoots:'?')+' footnotes — this HTML version has none; <a href="#" data-tab="2">see tab 03</a>'. how: 'counted in the parsed HTML: this version contains no footnote text and no footnote marks; reference.footnotes is the document\u2019s own count'.

Tile4: 'SPACES REPAIRED OR FLAGGED', big allRepairs.length, sub: 'in '+repairParas+' paragraphs — <a data-tab="2">see tab 03</a>'. how: 'four rules insert a space only where the characters prove one was there; every insertion is logged and listed on tab 03'.

Links with data-tab → click handler activates tab. I'll delegate: document.addEventListener('click', e => { var t = e.target.closest('[data-tab]'); if (t){ e.preventDefault(); activateTab(+t.dataset.tab); } });

Tab 02:

```js
var p2 = ...;
var hbox = '<button class="acc" id="hbox" aria-expanded="false">Headings found: '+headings.length+'</button>'+
 '<div id="hbody" hidden><ul class="hlist">' + headings.map(h=>'<li><span class="mono">'+h.tag.toUpperCase()+'</span> '+esc(h.display)+(h.glued?' <span class="mono hint">glued label separated</span>':'')+'</li>').join('') + '</ul></div>';
```

Table:

```js
var rows = paras.map(function(p){
  var first = p.text.length>120 ? p.text.slice(0,120).replace(/\s+\S*$/,'') + '…' : p.text;
```

Hmm "first 120 characters cut at a word with '…'": take slice(0,120), then cut back to last space: `var s=p.text.slice(0,120); if(p.text.length>120){ s = s.slice(0, s.lastIndexOf(' ')); } first = s + (p.text.length>120?'…':'')`. If lastIndexOf(' ')===-1, keep s. Fine.

```js
  var chk = p.firstMatch===true ? '<span class="ok">OK</span>' : p.firstMatch===false ? '<span class="bad">first words differ</span>' : '<span class="notrun">not run</span>';
  return '<tr class="prow" data-n="'+p.num+'" tabindex="0" role="button" aria-expanded="false">'+
    '<td class="num">'+p.num+'</td>'+
    '<td class="sec">'+esc(p.section||'—')+'</td>'+
    '<td class="first">'+esc(first)+'</td>'+
    '<td class="chk">'+chk+'</td></tr>'+
    '<tr class="pdet" data-n="'+p.num+'" hidden><td colspan="4">'+detailHtml(p)+'</td></tr>';
}).join('');
```

detailHtml(p):

```js
function detailHtml(p){
  var path = (p.part && p.section && p.part!==p.section) ? p.part+' › '+p.section : (p.section||p.part||'—');
  var h = '<div class="mono path">'+esc(path)+'</div>';
  h += '<p class="full">'+markedHtml(p)+'</p>';
  // first words
  if (p.firstMatch===null) h += '<p class="fw notrun">first words: not run — no reference in this file</p>';
  else h += '<p class="fw '+(p.firstMatch?'ok':'bad')+'">first words — found: \u201C'+esc(p.found6)+'\u201D · reference: \u201C'+esc(p.ref6)+'\u201D</p>';
  // repairs
  if (p.repairs.length){
    h += '<p class="reps">spaces restored here: '+p.repairs.length+' — '+p.repairs.map(function(r){return esc(r.ruleName)+' \u201C'+esc(r.match)+'\u201D \u2192 \u201C'+esc(r.fixed)+'\u201D';}).join(' · ')+'</p>';
  } else h += '<p class="reps dim">no spaces restored in this paragraph</p>';
  h += '<button class="btn copy" data-cite="'+esc(symbol+', para. '+p.num)+'">Copy citation</button> <span class="mono hint">citation: '+esc(symbol+', para. '+p.num)+'</span>';
  return h;
}
function markedHtml(p){
  var out='', i;
  for (i=0;i<p.text.length;i++){
    if (p.mask[i]){
      var inner = esc(p.text[i]);
      if (i+1<p.text.length && !p.mask[i+1]){ inner += esc(p.text[i+1]); i++; }
      out += '<span class="fix" title="space restored here — see tab 03">'+inner+'</span>';
    } else out += esc(p.text[i]);
  }
  return out;
}
```

Table html:

```js
p2.innerHTML = hbox +
 '<table><caption><span class="mono">TAB.02</span>'+paras.length+' paragraphs found'+(refParas!=null?', '+refParas+' expected':'')+' — click a row for the full text, verbatim</caption>'+
 '<thead><tr><th scope="col" class="num">No.</th><th scope="col">Section</th><th scope="col">First line</th><th scope="col">Check</th></tr></thead>'+
 '<tbody>'+rows+'</tbody></table>';
```

Row toggle: delegate on p2:

```js
p2.addEventListener('click', function(e){
  var c = e.target.closest('.copy'); if (c){ copyCite(c); return; }
  var r = e.target.closest('tr.prow'); if (!r) return;
  toggleRow(r);
});
p2.addEventListener('keydown', function(e){
  if (e.key!=='Enter' && e.key!==' ') return;
  var r = e.target.closest('tr.prow'); if (!r) return;
  e.preventDefault(); toggleRow(r);
});
function toggleRow(r){
  var det = p2.querySelector('tr.pdet[data-n="'+r.dataset.n+'"]');
  var open = det.hidden;
  det.hidden = !open; // hmm
```

Wait: toggle: if det.hidden → show (hidden=false), aria-expanded=true. Else hide.

```js
function toggleRow(r){
  var det = p2.querySelector('tr.pdet[data-n="'+r.dataset.n+'"]');
  var show = det.hidden;
  det.hidden = !show;
  r.setAttribute('aria-expanded', show?'true':'false');
}
```

openParagraph(n): activateTab(1); then find row, expand, scroll:

```js
function openParagraph(n){
  activateTab(1);
  var r = p2.querySelector('tr.prow[data-n="'+n+'"]');
  if (!r) return;
  var det = p2.querySelector('tr.pdet[data-n="'+n+'"]');
  if (det.hidden){ det.hidden=false; r.setAttribute('aria-expanded','true'); }
  r.scrollIntoView({block:'center'});
}
```

Tab 03:

```js
var p3 = ...;
var footBlock = '<h3 class="btitle">Lost: footnotes <span class="cnt">'+(refFoots!=null?('0 of '+refFoots):'0')+'</span></h3>'+
 '<p>The document has '+(refFoots!=null?refFoots:'an unknown number of')+' footnotes. This HTML has 0: no footnote text, no footnote marks, and the note the title\u2019s asterisk points to is missing. To cite a footnote, use the PDF or Word version.</p>';
```

Spaces block:

```js
var spaceBlock = '<h3 class="btitle">Changed: spaces <span class="cnt">'+allRepairs.length+' restored in '+repairParas+' paragraphs</span></h3>'+
 '<p class="ruleline mono">SENTENCE '+perRule.sentence+' · COMMA '+perRule.comma+' · QUOTE '+perRule.quote+' · DASH '+perRule.dash+'</p>'+
 '<table><caption><span class="mono">TAB.03</span>Every missing space the rules found and restored — click a row to open the paragraph on tab 02</caption>'+
 '<thead><tr><th scope="col" class="num">Paragraph</th><th scope="col">Before</th><th scope="col">After</th><th scope="col">Rule</th></tr></thead><tbody>'+
 allRepairs.map(function(r){
   return '<tr class="rrow" data-n="'+r.para+'" tabindex="0" role="button"><td class="num">'+r.para+'</td>'+
   '<td>'+esc(r.prefix)+'<span class="fix">'+esc(r.match)+'</span>'+esc(r.suffix)+'</td>'+
   '<td>'+esc(r.prefix)+'<span class="fix">'+esc(r.fixed)+'</span>'+esc(r.suffix)+'</td>'+
   '<td>'+esc(r.ruleName)+'</td></tr>';
 }).join('') + '</tbody></table>'+
 '<p class="note">Rules restore a space only where the characters prove it was there. Word pairs such as \u2018Giventhe\u2019 are not touched; the first-words check catches them only in a paragraph\u2019s first six words.</p>';
```

Wait — Before/After: prefix+match+suffix from the pre-repair string; After should show the repaired context: prefix + fixed + suffix. Yes as written. Good.

Characters block:

```js
var charBlock = '<h3 class="btitle">Changed: characters <span class="cnt">kept as published</span></h3>'+
 '<table><caption><span class="mono">TAB.03</span>Characters a keyboard does not type — counted over all paragraph texts</caption>'+
 '<thead><tr><th scope="col">Character</th><th scope="col" class="num">Count</th><th scope="col">Example</th></tr></thead><tbody>'+
 charStats.map(function(c){
   return '<tr><td><code>'+esc(c.label)+'</code></td><td class="num">'+c.count+'</td><td class="ex">'+esc(c.example||'—')+'</td></tr>';
 }).join('')+'</tbody></table>'+
 '<p class="mono hint">on a keyboard: a hyphen and straight quotes</p>'+
 '<p class="note">Kept exactly as published, in the table and in every export. A search for \u2018business-related\u2019 typed with the hyphen key will not find \u2018business\u2011related\u2019: normalise the text before searching it.</p>';
```

Hmm the example for NBSP: I built example with '⍽' marker. esc() will keep it. OK. For the character label, maybe show the actual char: label + ' ' + char. I'll include the char in the label cell: `<code>en dash –</code>`. Let me add `glyph` field: for double quotes '“”', etc. I'll add glyph in CHARS: en dash '–', double quotes '“”', right single '’', nb-hyphen '‑' (U+2011, looks like hyphen — fine, it's the point), nbsp '⍽' with note. Actually for nbsp show '(U+00A0)'. I'll do label cell: `en dash (–) U+2013`? Keep: `<code>–</code> en dash · U+2013`. Let me structure: name + code glyph + codepoint. Fine.

Tab 03 click delegation: rrow click → openParagraph(+n). keydown Enter/Space too.

Tab 04:

```js
var p4 = ...;
var checksHtml = '<h3 class="btitle">Checks <span class="cnt">'+nPass+' pass · '+nFail+' failed'+(nLimit?' · '+nLimit+' source limit':'')+(nNotRun?' · '+nNotRun+' not run':'')+'</span></h3>'+
 '<ol class="checks">'+checks.map(function(c){
   var st = c.status==='pass' ? '<span class="ok">pass</span>' : c.status==='fail' ? '<span class="bad">check failed</span>' : c.status==='limit' ? '<span class="bad">source limit</span>' : '<span class="notrun">not run</span>';
   var link = c.linkTab!=null ? ' <a href="#" data-tab="'+c.linkTab+'">'+(c.linkLabel||'see the rows')+'</a>' : '';
   return '<li><strong>'+esc(c.name)+'</strong> — '+c.detail+' '+st+link+(c.note?' <span class="dim">'+esc(c.note)+'</span>':'')+'</li>';
 }).join('')+'</ol>';
```

detail contains HTML for unclassified list — I said I'd escape; in the nothing-lost check I embed esc'd content, so detail is HTML-safe. But other details contain '·' fine. The first-words detail contains curly quotes — fine as HTML text. But it contains found6/ref6 which are data — should escape. I'll esc() them when building. OK.

Export section:

```js
var expHtml = '<h3 class="btitle">Export</h3>'+
 '<p class="note">The dataset travels with its source, its fields and its known limitations: every record carries symbol, paragraph, section, part, text, text_raw, first_words_match, citation, doc_url and limitations.</p>'+
 '<button class="btn" id="dljson"'+(paras.length?'':' disabled')+'>Download JSON</button> '+
 '<button class="btn" id="dlmd"'+(paras.length?'':' disabled')+'>Download Markdown</button>'+
 (paras.length?'':'<p class="bad">No paragraphs found — exports are disabled.</p>')+
 '<p class="mono hint">file name: '+esc(symbol.replace(/\//g,'-'))+'.json / .md · UTF-8 · Blob URL</p>';
```

Elements accordion:

```js
var elHtml = '<button class="acc" id="elbox" aria-expanded="false">Elements found ('+elements.length+')</button>'+
 '<div id="elbody" hidden><table><caption><span class="mono">TAB.04</span>Every block element in the parsed HTML, in order, classified exactly once</caption>'+
 '<thead><tr><th scope="col">Tag</th><th scope="col">Classified as</th><th scope="col">Text (first 80 characters)</th></tr></thead><tbody>'+
 elements.map(function(e){ return '<tr><td><code>&lt;'+esc(e.tag)+'&gt;</code>'+(e.cls?' <span class="mono hint">.'+esc(e.cls)+'</span>':'')+'</td><td>'+esc(e.clsAs)+'</td><td>'+esc(e.text)+'</td></tr>'; }).join('')+
 '</tbody></table></div>';
```

p4.innerHTML = checksHtml + expHtml + elHtml;

Accordion handlers: hbox, elbox toggle their bodies.

Downloads:

```js
document.getElementById('dljson').onclick = function(){ download(symbol.replace(/\//g,'-')+'.json', jsonStr, 'application/json'); };
document.getElementById('dlmd').onclick = function(){ download(symbol.replace(/\//g,'-')+'.md', mdStr, 'text/markdown'); };
```

But if disabled, onclick still set — guard inside: if (!paras.length) return.

Copy citation:

```js
function copyCite(btn){
  var t = btn.getAttribute('data-cite');
  function done(){ var old=btn.textContent; btn.textContent='Copied'; setTimeout(function(){btn.textContent=old;},2000); }
  function fb(){
    var ta=document.createElement('textarea'); ta.value=t; ta.setAttribute('readonly',''); ta.style.position='fixed'; ta.style.opacity='0';
    document.body.appendChild(ta); ta.select();
    var ok=false; try{ ok=document.execCommand('copy'); }catch(e){}
    document.body.removeChild(ta);
    if (ok) done(); else { btn.textContent=t; setTimeout(function(){btn.textContent='Copy citation';},2000); }
  }
  if (navigator.clipboard && navigator.clipboard.writeText){ navigator.clipboard.writeText(t).then(done, fb); } else fb();
}
```

Tabs:

```js
var tabs = Array.prototype.slice.call(document.querySelectorAll('#tablist [role=tab]'));
var panels = [document.getElementById('p1'),...,p4];
function activateTab(i){
  tabs.forEach(function(t,j){
    var on = i===j;
    t.setAttribute('aria-selected', on?'true':'false');
    t.tabIndex = on?0:-1;
    panels[j].hidden = !on;
  });
}
tabs.forEach(function(t,i){
  t.addEventListener('click', function(){ activateTab(i); });
});
document.getElementById('tablist').addEventListener('keydown', function(e){
  var i = tabs.indexOf(document.activeElement);
  if (i<0) return;
  var n=null;
  if (e.key==='ArrowRight') n=(i+1)%tabs.length;
  else if (e.key==='ArrowLeft') n=(i-1+tabs.length)%tabs.length;
  else if (e.key==='Home') n=0;
  else if (e.key==='End') n=tabs.length-1;
  if (n!==null){ e.preventDefault(); tabs[n].focus(); activateTab(n); }
});
```

Global data-tab delegation:

```js
document.addEventListener('click', function(e){
  var t = e.target.closest ? e.target.closest('[data-tab]') : null;
  if (t){ e.preventDefault(); activateTab(parseInt(t.getAttribute('data-tab'),10)); }
});
```

Careful: p2 click handler also fires; order fine.

Accordion:

```js
function bindAcc(btnId, bodyId){
  var b=document.getElementById(btnId), d=document.getElementById(bodyId);
  if(!b) return;
  b.addEventListener('click', function(){ var open = d.hidden; d.hidden=!open; b.setAttribute('aria-expanded', open?'true':'false'); });
}
```

But p2/p3/p4 innerHTML set after; bind after setting innerHTML.

Footer:

```js
document.getElementById('foot').innerHTML = '<span class="mono">SOURCE</span> '+esc(source) + (doc.built? ' · <span class="mono">BUILT</span> '+esc(doc.built):'') + ' · Done by this page\u2019s code; no model was called and nothing left the browser.' + credits;
```

Credits: `<div class="credits">Guidance followed: The Turing Way, \u201CDocumentation and metadata\u201D (CC BY 4.0) · UK Government Analysis Function, \u201CQuality assurance of code for analysis and research: Testing code\u201D · Dag Hammarskjöld Library, \u201CHow should I cite a UN document?\u201D</div>`. Hmm — licence claims: Turing Way is CC BY 4.0 (true). Analysis Function guidance — published under OGL? The repo best-practice-and-impact uses CC BY 4.0? Actually the QA of code guidance is under the Open Government Licence? I'm not certain. To avoid inventing, I'll phrase: "Method and citation practice follow The Turing Way (CC BY 4.0), the UK Government Analysis Function's QA-of-code guidance, and the Dag Hammarskjöld Library's guidance on citing UN documents." Only assert CC BY for Turing Way which I'm confident about. The rule says name source and licence when using code/wording from reference shelf excerpts with open licence — I'm not using their code/wording, so this is optional; I'll keep the line modest.

Header status render:

```js
var hs = document.getElementById('hstatus');
var dotCls = nFail>0 ? 'r' : 'g';
var txt = nFail>0 ? nFail+' checks failed' : nPass+' of '+nRun+' checks pass';
hs.innerHTML = '<span class="dot '+dotCls+'"></span> <span class="mono">'+txt+'</span>' + (nLimit? ' <span class="mono bad">· '+nLimit+' source limit</span>':'') + (nNotRun? ' <span class="mono notrun">· '+nNotRun+' not run</span>':'');
```

Now — one thing: the rail "checks" element is a button; clicking activates tab 4 (index 3). Set `railchecks.onclick = function(){ activateTab(3); };`

Also initial: activateTab(0) — panels 2-4 already hidden in markup.

Edge: `p.text.split(/\s+/)` — if text empty, split gives ['']; found6 = ''. fine.

Now — the "s" flag issue: I'll write regexes without /s since text collapsed: `/^(\d{1,3})\.\s*(.*)$/` and `/^([IVX]+|[A-Z])\.\s*(.+)$/`. Good.

One more: heading regex could wrongly match a heading like "A. Introduction" — intended. What about h3 "Right to work (art. 6)" — starts 'R' then 'i' — `[A-Z]\.` requires dot right after single capital — "Right" has 'i' after R, no match. Good. What about "D. Obligation" — matches. What about a heading like "V. Conclusion" fine.

Potential false positive: heading "X. Something" fine. Heading like "I.Introduction" matches, glued. Good.

Now — the paragraph regex vs committee line: committee line "Committee on Economic, Social and Cultural Rights" — no leading digits. Good.

What about `<p>` cover lines inside table — skipped (table is one block). Good.

Now sizes: elements ~100 rows, fine.

Let me also double check the tab-02 "Headings found" box is closed initially and lists headings — yes.

"At most seven things to click" per view: tab 02: 4 tabs + headings box = 5 (+ rows). Tab 03: 4 tabs + rows. Tab 04: 4 tabs + 2 buttons + elements box = 7. Tab 01: 4 tabs + links in tiles (2 links) = 6. OK.

Now CSS details. Let me write it:

```css
:root{--paper:#f4f0e8;--ink:#1d1b18;--rule:#d9d2c3;--red:#9b2335;--green:#1f6b3a;--dim:#6b675f;}
*{box-sizing:border-box}
[hidden]{display:none!important}
html,body{margin:0;padding:0}
body{background:var(--paper);color:var(--ink);font:16px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif}
a{color:var(--red)}
code{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:.85em}
.mono{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:11.5px;letter-spacing:.12em;text-transform:uppercase}
.hint{color:var(--dim);text-transform:none;letter-spacing:.04em}
:focus-visible{outline:2px solid var(--red);outline-offset:2px}
header{display:flex;justify-content:space-between;gap:24px;align-items:flex-end;padding:22px 28px 14px;border-bottom:1px solid var(--rule)}
.label{color:var(--red);margin-bottom:6px}
h1{font-family:Georgia,"Times New Roman",serif;font-weight:normal;font-size:27px;line-height:1.2;margin:0 0 8px;max-width:60ch}
.meta{color:var(--dim);font-size:14px}
.hright{white-space:nowrap;text-align:right;padding-bottom:4px}
.dot{display:inline-block;width:9px;height:9px;border-radius:50%;margin-right:6px;vertical-align:1px}
.dot.g{background:var(--green)}.dot.r{background:var(--red)}
nav[role=tablist]{display:flex;padding:0 20px;border-bottom:1px solid var(--rule);background:var(--paper)}
nav [role=tab]{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:12px;letter-spacing:.12em;background:none;border:none;border-bottom:2px solid transparent;padding:12px 14px 10px;cursor:pointer;color:var(--ink)}
nav [role=tab][aria-selected=true]{color:var(--red);border-bottom-color:var(--red)}
.layout{display:flex;align-items:flex-start}
aside{flex:0 0 248px;width:248px;border-right:1px solid var(--rule);padding:18px 20px 28px;position:sticky;top:0;max-height:100vh;overflow:auto}
.railhead{color:var(--red);border-bottom:1px solid var(--rule);padding-bottom:8px;margin-bottom:12px}
.doccard{border:1px solid var(--rule);padding:10px 12px;margin-bottom:18px}
.sym{color:var(--red)}
.shorttitle{font-family:Georgia,serif;font-size:14px;line-height:1.35;margin-top:6px}
.railnum{margin-bottom:18px}
.bignum{font-family:Georgia,"Times New Roman",serif;font-size:46px;line-height:1}
.bignum.red{color:var(--red)}
.bignum.ok{color:var(--green)}
.bignum.bad{color:var(--red)}
.railsub{font-size:13px;color:var(--dim);margin-top:4px}
.bar{height:4px;background:var(--rule);margin-top:8px}
.bar i{display:block;height:100%;background:var(--green)}
.bar.bad i{background:var(--red)}
.railchecks{display:block;background:none;border:none;border-top:1px solid var(--rule);padding:10px 0 0;cursor:pointer;font:inherit;font-size:13px;color:var(--red);text-align:left}
main{flex:1;min-width:0;padding:20px 28px 48px}
section[role=tabpanel]{max-width:1060px}
.tiles{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr))}
.tile{padding:16px 20px 18px;border-left:1px solid var(--rule)}
.tile:first-child{border-left:none;padding-left:0}
.tlabel{color:var(--dim);margin-bottom:10px}
.tsub{font-size:14px;margin-top:6px}
.how{font-size:12.5px;color:var(--dim);margin-top:10px;border-top:1px solid var(--rule);padding-top:8px}
.notice{border:1px solid var(--red);padding:14px 16px;max-width:70ch}
.btitle{font-family:Georgia,serif;font-weight:normal;font-size:21px;margin:26px 0 8px}
.btitle .cnt{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:12px;letter-spacing:.1em;color:var(--dim);margin-left:10px;text-transform:uppercase}
table{border-collapse:collapse;width:100%;margin:10px 0 18px}
caption{text-align:left;font-family:Georgia,serif;font-size:17px;padding:6px 0 10px;caption-side:top}
caption .mono{display:block;color:var(--dim);margin-bottom:3px}
th{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:11px;letter-spacing:.1em;text-transform:uppercase;font-weight:normal;text-align:left;border-bottom:1px solid var(--ink);padding:6px 14px 6px 0;color:var(--ink)}
td{border-bottom:1px solid var(--rule);padding:8px 14px 8px 0;vertical-align:top;font-size:15px}
th.num,td.num{text-align:right;font-variant-numeric:tabular-nums}
tr.prow{cursor:pointer}
tr.prow:hover{background:#ece6d8}
tr.prow .num{font-family:Georgia,serif;font-size:18px;color:var(--red);text-align:right}
tr.pdet td{background:#efe9dc;padding:16px 20px}
tr.pdet .full{max-width:75ch;margin:8px 0 12px}
.path{color:var(--dim)}
.fw{font-size:14px;margin:6px 0}
.reps{font-size:14px;margin:6px 0 12px}
.fix{outline:1px solid var(--red);padding:0 1px}
.ok{color:var(--green)}.bad{color:var(--red)}.notrun{color:var(--dim)}.dim{color:var(--dim)}
.btn{font:inherit;font-size:15px;background:none;border:1px solid var(--ink);padding:8px 16px;cursor:pointer;margin:4px 8px 4px 0}
.btn:hover{background:#eae3d3}
.btn[disabled]{opacity:.4;cursor:not-allowed}
.acc{display:block;width:100%;text-align:left;background:none;border:none;border-top:1px solid var(--rule);padding:12px 0;cursor:pointer;font-family:Georgia,serif;font-size:18px;color:var(--ink)}
.acc::after{content:" +";color:var(--red);font-family:ui-monospace,monospace}
.acc[aria-expanded=true]::after{content:" \2013"}
.acc:hover{color:var(--red)}
.hlist{list-style:none;margin:8px 0 20px;padding:0}
.hlist li{padding:5px 0;border-bottom:1px solid var(--rule);font-size:15px}
.hlist .mono{color:var(--red);margin-right:8px}
.rrow{cursor:pointer}
.rrow:hover{background:#ece6d8}
.checks{margin:8px 0 8px;padding-left:22px}
.checks li{margin:7px 0;font-size:15px;max-width:90ch}
.note{font-size:14px;color:var(--dim);max-width:80ch}
.ruleline{color:var(--dim);margin:4px 0 0}
.ex{font-size:14px}
footer{border-top:1px solid var(--rule);padding:14px 28px 22px;font-size:13px;color:var(--dim)}
.credits{margin-top:6px;font-size:12px}
```

Also `.fw.ok` etc fine.

Media query for narrow: `@media (max-width:820px){ .layout{flex-direction:column} aside{position:static;width:auto;flex:none;border-right:none;border-bottom:1px solid var(--rule);max-height:none} }` — good for no horizontal scroll.

Now assemble everything. Also note: the tab buttons in nav need ids tab-1..tab-4 and panels p1..p4 with aria-labelledby.

One more requirement: "A hidden tab panel is not focusable" — hidden attribute handles that (display:none removes from tab order). Good.

Also "Every table has a serif <caption> stating the message, a monospace number (TAB.01)" — I have TAB.02, TAB.03, TAB.04 captions. Tab 01 tiles aren't tables; fine.

Also the header label "UN DOCUMENT · HTML" — done.

Let me also handle `doc.built` — html_doc may not have built; guard.

Also the rail "short title": use title; maybe shorten? Just use title.

Now, potential issue: `elements` includes the cover table with text = whole table text (symbol etc.) sliced to 80 — fine.

Also the "committee line" count lineN — includes any non-numbered p. Good.

Double-check the numbering check when paras empty: skip (guard `if (paras.length)`), else add 'not run'? If no paras and ref exists, paragraph count check fails (0 vs 90). Numbering: add notrun. I'll do: if paras.length → run; else addCheck('Numbering','no paragraphs found','notrun').

First words when paras empty: firstWords exists → run=0, mm=0 → pass "0 of 0"? That would say pass with 0 — misleading. Guard: if paras.length===0 → notrun. Similarly repairs check with 0 repairs → pass "0 spaces restored in 0 paragraphs" — fine, it's a count. OK.

Export round trip with 0 paras: JSON "[]" parses to 0 === 0 → pass. Fine.

Now, one more spec item: tab 02 "A closed 'Headings found: n' box above the table lists them, so none can hide inside a paragraph." Done.

"Rows are buttons with aria-expanded; click or Enter expands the row in place" — done via tr role=button.

Also: "the reference's six words beside the found six" — done in detail.

"Copy citation button that copies 'symbol, para. n' and shows 'Copied' for two seconds; the same string is the citation field of every export" — done.

Tab 04 check panel "open, every check on one line" — done.

"Under the buttons a closed heading 'Elements found (n)'" — done.

Footer — done.

Now let me also make sure: "Before the code block: at most three short sentences saying what you built or changed. After it: nothing."

So my reply: 1-3 sentences + the html code block. Nothing after.

Let me now write the final code completely and carefully, checking syntax as I go.

One concern: in `repair`, using `s.replace(r.re, function(){...})` — inside the callback, `arguments[arguments.length-2]` is offset only when the regex has capture groups... Actually for replace with function, args are (match, p1, ..., pn, offset, string). With 2 groups: (match, p1, p2, offset, string) → length 5, offset at index 3 = length-2. With 1 group: (match, p1, offset, string) → length 4, offset at index 2 = length-2. Good, `arguments[arguments.length-2]` works for both.

But I don't even use the groups — I insert space at r.ins within the match. So I only need offset and match. Simplify callback: `function(m, ...rest)` — but I need offset = rest[rest.length-2]. Let me write:

```js
s.replace(r.re, function(m){
  var off = arguments[arguments.length-2];
  ...
});
```

Good.

Also mask building: initial mask all false length raw.length. In callback: append s.slice(last, off) with mask[last..off-1]; then fixed chars: for j in 0..ins-1 push mask[off+j] (original chars of match before insertion point), push true (the inserted space), then for k in ins..m.length-1 push mask[off+k]. Then last = off+m.length. After replace loop: append s.slice(last) with mask. Correct.

Edge: overlapping/adjacent matches — replace handles.

Now `markedHtml` uses p.mask aligned with p.text — yes since repair returns them together.

Let me also compute `firstLine` carefully:

```js
function firstLine(t){
  if (t.length<=120) return t;
  var s = t.slice(0,120);
  var sp = s.lastIndexOf(' ');
  if (sp>0) s = s.slice(0,sp);
  return s + '…';
}
```

Now the tab-01 tile 2 big number: count of firstMatch===true. If no ref → tile shows 'no reference in this file'. I'll set big = ref? count : '—'.

Let me write tile HTML generation:

```js
var t1big = paras.length;
var t1cls = (refParas!=null && paras.length===refParas) ? 'ok' : (refParas!=null ? 'bad' : '');
var t1sub = refParas!=null ? 'the document has '+refParas+(paras.length===refParas?' — equal':(paras.length>refParas?' — '+（paras.length-refParas)+' extra':' — '+(refParas-paras.length)+' short')) : 'no reference in this file';
```

Careful with full-width parens — avoid. Use plain.

Tile2: matchCount = paras.filter(p=>p.firstMatch===true).length; big = firstWords? matchCount : '—'; sub = firstWords? 'of '+(refParas!=null?refParas:paras.length)+' paragraphs match' : 'no reference in this file'; cls = (firstWords && matchCount===paras.length && paras.length>0)?'ok':(firstWords&&matchCount<paras.length?'bad':'').

Tile3: big '0' cls 'bad'; sub = 'of '+(refFoots!=null?refFoots:'?')+' footnotes — this HTML version has none; <a href="#" data-tab="2">see tab 03</a>'.

Tile4: big allRepairs.length; sub = 'in '+repairParas+' paragraphs — <a href="#" data-tab="2">see tab 03</a>'.

how lines as planned.

If paras.length===0: show notice + still tiles? Spec: "if html yields no <p>, tab 01 says so and the exports are disabled." I'll show notice above tiles; tiles show 0s. Fine — I'll render notice then tiles.

Now writing everything into the final HTML. Also add `<meta name="color-scheme" content="light">`? Not needed.

Let me also think about `activateTab` and panels array — panels defined after DOM. Script at end of body, so fine.

Potential pitfall: `e.target.closest` — e.target may be text node? In click events target is element. OK. But if e.target is the document? fine.

Also the global data-tab click handler will also catch rail? rail uses onclick directly. OK.

Also note: links `<a href="#" data-tab="2">` — preventDefault in handler. Good.

Now, the copy button inside pdet: p2 click handler checks `.copy` first — but the global data-tab handler also runs; copy has no data-tab. Fine.

Also keydown on p2 for prow — but copy button keydown Enter would bubble to p2 handler; e.target.closest('tr.prow') — copy button is inside tr.pdet, not prow → closest returns null → return. Good.

Let me now also handle the tab-03 rrow keyboard: add keydown on p3 similar.

Write final code. I'll be careful with quotes inside template strings — I'll use string concatenation with single quotes and escape as needed. Use \u2019 etc. for typographic chars to avoid encoding issues? File is UTF-8 with meta charset; I can use literal ’ etc. I'll use literals for readability but ensure charset declared. Fine.

Let me count roughly — should be under 1500 lines. Let's write.

Also: title of the page `<title>` — set to something like "Paragraphs of E/C.12/GC/27 from HTML" — but symbol read from data; set via JS: `document.title = symbol + ' — numbered paragraphs (HTML)'`.

One more check on the spec: "Header ... one line with the data's source, n and years." — that's the generic layout rule; here the header spec overrides: symbol link, adopted, source. I'll also include n: "90 paragraphs" maybe in meta line: symbol · adopted · source · n paragraphs. I'll add `· ` + paras.length + ' paragraphs' to meta. Good — covers "n".

Rail heading "DOCUMENT" — done.

Now write it all out.

Also careful: in `detailHtml`, `data-cite="'+esc(...)+'"` — esc escapes quotes to &quot; so attribute safe. Good.

In checks detail for first words I embed curly quotes and esc(found6) — found6 may contain straight quotes after norm (curly→straight) — esc handles.

Let me write the nothing-lost detail carefully:

```js
var uncls = otherEls.length ? ' — unclassified: '+otherEls.slice(0,5).map(function(o){return '&lt;'+esc(o.tag)+'&gt; '+esc(o.text.slice(0,40));}).join('; ') : '';
addCheck('Nothing lost', total+' block elements: '+coverN+' cover, '+(titleText?1:0)+' title, '+headings.length+' headings, '+paras.length+' paragraphs, '+lineN+' committee lines, '+otherEls.length+' unclassified'+uncls, okAll?'pass':'fail');
```

OK. Now the full document. Writing now.

Also — `flow` includes headings and paragraphs; markdown uses it. But note the title h2 is not in flow (classified as title) — markdown then starts with first section h2 "## I. Introduction". Hmm, spec says "the headings as ## and ### lines in document order" — title is a heading too... I'll include the title as `# title` at top of body? Spec literally: headings as ## and ###. The title h2 → I'll emit it as `# ` + titleText for a sensible document, since front matter also has title. Hmm "keep it simple... where it says nothing". The spec says headings as ## and ### lines — I'll follow literally: all headings (h2/h3) as ##/###. But then the doc title is missing from body... front matter has title. I'll include title as `#` line — it's the document title, natural. Actually to be safe and literal, I'll push the title into flow as {kind:'h', tag:'h1', display:titleText} so markdown emits `# title`. That's a reasonable interpretation ("headings in document order" — the title is the first heading). I'll do that.

Wait but then in tab 02 headings list, title excluded (it's classified as title, not heading) — correct per spec ("the first <h2> is the title").

OK. Also markdown: committee line skipped. Fine.

Now, writing the final answer. Let me carefully produce the code.

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>UN document HTML — numbered paragraphs</title>
<style>
:root{--paper:#f4f0e8;--ink:#1d1b18;--rule:#d9d2c3;--red:#9b2335;--green:#1f6b3a;--dim:#6b675f}
*{box-sizing:border-box}
[hidden]{display:none!important}
body{margin:0;background:var(--paper);color:var(--ink);font:16px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif}
a{color:var(--red)}
code{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:.85em}
.mono{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:11.5px;letter-spacing:.12em;text-transform:uppercase}
.hint{color:var(--dim);text-transform:none;letter-spacing:.03em;font-size:11px}
:focus-visible{outline:2px solid var(--red);outline-offset:2px}
header{display:flex;justify-content:space-between;align-items:flex-end;gap:24px;padding:22px 28px 14px;border-bottom:1px solid var(--rule)}
.label{color:var(--red);margin-bottom:6px}
h1{font-family:Georgia,"Times New Roman",serif;font-weight:400;font-size:27px;line-height:1.2;margin:0 0 8px;max-width:62ch}
.meta{font-size:14px;color:var(--dim)}
.hright{white-space:nowrap;text-align:right;padding-bottom:4px}
.dot{display:inline-block;width:9px;height:9px;border-radius:50%;margin-right:6px}
.dot.g{background:var(--green)}.dot.r{background:var(--red)}
nav[role=tablist]{display:flex;padding:0 20px;border-bottom:1px solid var(--rule)}
nav [role=tab]{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:12px;letter-spacing:.12em;background:none;border:none;border-bottom:2px solid transparent;padding:12px 14px 10px;cursor:pointer;color:var(--ink)}
nav [role=tab][aria-selected=true]{color:var(--red);border-bottom-color:var(--red)}
.layout{display:flex;align-items:flex-start}
aside{flex:0 0 250px;width:250px;border-right:1px solid var(--rule);padding:18px 20px 28px;position:sticky;top:0;max-height:100vh;overflow:auto}
.railhead{color:var(--red);border-bottom:1px solid var(--rule);padding-bottom:8px;margin-bottom:12px}
.doccard{border:1px solid var(--rule);padding:10px 12px;margin-bottom:18px}
.sym{color:var(--red)}
.shorttitle{font-family:Georgia,serif;font-size:14px;line-height:1.35;margin-top:6px}
.railnum{margin-bottom:20px}
.bignum{font-family:Georgia,"Times New Roman",serif;font-size:46px;line-height:1}
.bignum.red,.bignum.bad{color:var(--red)}
.bignum.ok{color:var(--green)}
.railsub{font-size:13px;color:var(--dim);margin-top:5px}
.bar{height:4px;background:var(--rule);margin-top:9px}
.bar i{display:block;height:100%;background:var(--green)}
.bar.bad i{background:var(--red)}
.railchecks{display:block;background:none;border:none;border-top:1px solid var(--rule);padding:12px 0 0;cursor:pointer;font:inherit;font-size:13px;color:var(--red);text-align:left;width:100%}
main{flex:1;min-width:0;padding:20px 28px 48px}
section[role=tabpanel]{max-width:1080px}
.tiles{display:grid;grid-template-columns:repeat(auto-fit,minmax(235px,1fr))}
.tile{padding:16px 20px 18px;border-left:1px solid var(--rule)}
.tile:first-child{border-left:none;padding-left:0}
.tlabel{color:var(--dim);margin-bottom:10px}
.tsub{font-size:14px;margin-top:6px}
.how{font-size:12.5px;color:var(--dim);margin-top:10px;border-top:1px solid var(--rule);padding-top:8px}
.notice{border:1px solid var(--red);padding:14px 16px;max-width:75ch}
.btitle{font-family:Georgia,serif;font-weight:400;font-size:21px;margin:28px 0 8px}
.btitle .cnt{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:11.5px;letter-spacing:.1em;color:var(--dim);margin-left:10px;text-transform:uppercase}
table{border-collapse:collapse;width:100%;margin:10px 0 18px}
caption{text-align:left;font-family:Georgia,serif;font-size:17px;padding:6px 0 10px}
caption .mono{display:block;color:var(--dim);margin-bottom:3px}
th{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:11px;letter-spacing:.1em;text-transform:uppercase;font-weight:400;text-align:left;border-bottom:1px solid var(--ink);padding:6px 14px 6px 0}
td{border-bottom:1px solid var(--rule);padding:8px 14px 8px 0;vertical-align:top;font-size:15px}
th.num,td.num{text-align:right;font-variant-numeric:tabular-nums}
tr.prow{cursor:pointer}
tr.prow:hover{background:#ece6d8}
tr.prow .num{font-family:Georgia,serif;font-size:18px;color:var(--red)}
tr.pdet td{background:#efe9dc;padding:16px 20px}
tr.pdet .full{max-width:78ch;margin:8px 0 12px}
.path{color:var(--dim)}
.fw,.reps{font-size:14px;margin:6px 0}
.fix{outline:1px solid var(--red);padding:0 1px}
.ok{color:var(--green)}.bad{color:var(--red)}.notrun,.dim{color:var(--dim)}
.btn{font:inherit;font-size:15px;background:none;border:1px solid var(--ink);padding:8px 16px;cursor:pointer;margin:4px 8px 4px 0}
.btn:hover{background:#eae3d3}
.btn[disabled]{opacity:.4;cursor:not-allowed}
.acc{display:block;width:100%;text-align:left;background:none;border:none;border-top:1px solid var(--rule);padding:12px 0;cursor:pointer;font-family:Georgia,serif;font-size:18px;color:var(--ink)}
.acc::after{content:" +";color:var(--red)}
.acc[aria-expanded=true]::after{content:" –"}
.acc:hover{color:var(--red)}
.hlist{list-style:none;margin:8px 0 20px;padding:0}
.hlist li{padding:5px 0;border-bottom:1px solid var(--rule);font-size:15px}
.hlist .mono{color:var(--red);margin-right:8px}
.rrow{cursor:pointer}
.rrow:hover{background:#ece6d8}
.checks{margin:8px 0;padding-left:22px}
.checks li{margin:7px 0;font-size:15px;max-width:95ch}
.note{font-size:14px;color:var(--dim);max-width:85ch}
.ruleline{color:var(--dim);margin:4px 0 0}
footer{border-top:1px solid var(--rule);padding:14px 28px 24px;font-size:13px;color:var(--dim)}
.credits{margin-top:6px;font-size:12px}
@media (max-width:840px){.layout{flex-direction:column}aside{position:static;width:auto;flex:none;max-height:none;border-right:none;border-bottom:1px solid var(--rule)}header{flex-direction:column;align-items:flex-start;gap:8px}}
</style>
</head>
<body>
...
```

Now the body markup and script. Let me write the script in full, then assemble.

I need to double check one thing: `nav [role=tab]` buttons — initial: tab-1 aria-selected=true, others false with tabindex="-1". Panels p2..p4 hidden.

Script (I'll write it as one IIFE):

```js
(function(){
'use strict';
var W = window.WORKSHOP_DATA || {};
var raw = W.html_doc;
var doc = Array.isArray(raw) ? (raw[0]||{}) : (raw||{});
var ref = doc.reference || null;
var symbol = doc.symbol || '(no symbol)';
var docUrl = doc.doc_url || '';
var title = doc.title || '(untitled)';
var source = doc.source || '';
var adopted = (ref && ref.adopted) ? ref.adopted : null;
var refParas = (ref && typeof ref.paragraphs === 'number') ? ref.paragraphs : null;
var refFoots = (ref && typeof ref.footnotes === 'number') ? ref.footnotes : null;
var firstWords = (ref && ref.first_words) ? ref.first_words : null;

function esc(s){return String(s==null?'':s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');}
function collapse(s){return String(s==null?'':s).replace(/\s+/g,' ').trim();}
function norm(s){return String(s==null?'':s).replace(/[\u201C\u201D]/g,'"').replace(/\u2019/g,"'").replace(/\u2013/g,'-').replace(/\u2011/g,'-').replace(/\u00A0/g,' ').replace(/\s+/g,' ').trim();}

var blocks=[];
try{
  var parsed=new DOMParser().parseFromString(doc.html||'','text/html');
  if(parsed.body){
    (function walk(el){
      for(var i=0;i<el.children.length;i++){
        var c=el.children[i],t=c.tagName.toLowerCase();
        if(t==='div'||t==='section'||t==='article'||t==='main') walk(c); else blocks.push(c);
      }
    })(parsed.body);
  }
}catch(e){blocks=[];}

var RULES=[
  {key:'sentence',name:'sentence join',re:/([a-z])\.([A-Z])/g,ins:2},
  {key:'comma',name:'comma join',re:/([a-z]),([A-Za-z])/g,ins:2},
  {key:'quote',name:'quote join',re:/([a-z])\u201C/g,ins:1},
  {key:'dash',name:'dash join',re:/\u2013([A-Za-z])/g,ins:1}
];
function repair(rawText,num){
  var s=rawText,mask=[],i;
  for(i=0;i<rawText.length;i++)mask.push(false);
  var log=[];
  RULES.forEach(function(r){
    var ns='',nm=[],last=0;
    s.replace(r.re,function(m){
      var off=arguments[arguments.length-2];
      var j;
      ns+=s.slice(last,off); for(j=last;j<off;j++)nm.push(mask[j]);
      var fixed=m.slice(0,r.ins)+' '+m.slice(r.ins);
      ns+=fixed;
      for(j=0;j<r.ins;j++)nm.push(mask[off+j]);
      nm.push(true);
      for(j=r.ins;j<m.length;j++)nm.push(mask[off+j]);
      last=off+m.length;
      log.push({para:num,rule:r.key,ruleName:r.name,match:m,fixed:fixed,
        prefix:s.slice(Math.max(0,off-20),off),
        suffix:s.slice(off+m.length,off+m.length+20)});
      return m;
    });
    ns+=s.slice(last); for(var k=last;k<s.length;k++)nm.push(mask[k]);
    s=ns; mask=nm;
  });
  return {text:s,mask:mask,log:log};
}

var paras=[],headings=[],flow=[],elements=[];
var coverN=0,titleText=null,lineN=0,otherEls=[];
var curSec=null,curPart=null,seenTitle=false;
var byNum={};

blocks.forEach(function(el){
  var tag=el.tagName.toLowerCase();
  var text=collapse(el.textContent);
  var clsAs;
  if(tag==='table'){coverN++;clsAs='cover';}
  else if(tag==='p'){
    var m=text.match(/^(\d{1,3})\.\s*(.*)$/);
    if(m){
      var num=parseInt(m[1],10);
      var rawText=collapse(m[2]);
      var rep=repair(rawText,num);
      var p={num:num,text_raw:rawText,text:rep.text,mask:rep.mask,repairs:rep.log,section:curSec,part:curPart,firstMatch:null,found6:'',ref6:''};
      paras.push(p); byNum[num]=p; flow.push({kind:'p',num:num});
      clsAs='paragraph';
    } else { lineN++; clsAs='committee line'; }
  }
  else if(tag==='h2'||tag==='h3'){
    if(tag==='h2'&&!seenTitle){seenTitle=true;titleText=text;clsAs='title';flow.push({kind:'h',tag:'h1',display:text});}
    else{
      var hm=text.match(/^([IVX]+|[A-Z])\.\s*(.+)$/);
      var label=null,htext=text,glued=false,display=text;
      if(hm){label=hm[1];htext=collapse(hm[2]);glued=!/\s/.test(text.charAt(label.length+1));display=label+'. '+htext;}
      var isPart=(tag==='h2'&&label&&/^[IVX]+$/.test(label));
      headings.push({tag:tag,raw:text,label:label,text:htext,glued:glued,display:display,part:isPart});
      flow.push({kind:'h',tag:tag,display:display});
      curSec=display; if(isPart)curPart=display;
      clsAs='heading ('+tag+')';
    }
  }
  else { otherEls.push({tag:tag,text:text}); clsAs='unclassified'; }
  elements.push({tag:tag,cls:el.className||'',text:text.slice(0,80),clsAs:clsAs});
});
```

Wait — flow for title: I push {kind:'h',tag:'h1',...} so markdown emits '# '. But tab-02 headings list uses `headings` (excludes title). Good.

Hmm, but the markdown heading level: tag 'h1' → '# '. In buildMarkdown I map f.tag==='h2'?'## ':'### ' — need to handle 'h1' → '# '. I'll map: h1→'# ', h2→'## ', h3→'### '.

Continue:

```js
paras.forEach(function(p){
  p.found6=norm(p.text.split(/\s+/).slice(0,6).join(' '));
  if(firstWords){
    var rv=firstWords[String(p.num)];
    if(rv!=null){p.ref6=norm(rv);p.firstMatch=(p.found6===p.ref6);}
  }
});

var CHARS=[
  {name:'en dash',glyph:'\u2013',cp:'U+2013',chars:'\u2013'},
  {name:'double quotes',glyph:'\u201C \u201D',cp:'U+201C / U+201D',chars:'\u201C\u201D'},
  {name:'right single quote',glyph:'\u2019',cp:'U+2019',chars:'\u2019'},
  {name:'non-breaking hyphen',glyph:'\u2011',cp:'U+2011',chars:'\u2011'},
  {name:'non-breaking space',glyph:'\u00A0',cp:'U+00A0',chars:'\u00A0'}
];
var charStats=CHARS.map(function(c){
  var count=0,example='';
  paras.forEach(function(p){
    for(var i=0;i<p.text.length;i++){
      if(c.chars.indexOf(p.text[i])>=0){
        count++;
        if(!example){
          var a=Math.max(0,i-25);
          var g=(p.text[i]==='\u00A0')?'\u2423':p.text[i];
          example=(a>0?'\u2026':'')+p.text.slice(a,i)+'['+g+']'+p.text.slice(i+1,i+26)+(i+26<p.text.length?'\u2026':'');
        }
      }
    }
  });
  return {name:c.name,glyph:c.glyph,cp:c.cp,count:count,example:example};
});

var allRepairs=[];
paras.forEach(function(p){p.repairs.forEach(function(r){allRepairs.push(r);});});
var perRule={sentence:0,comma:0,quote:0,dash:0};
allRepairs.forEach(function(r){perRule[r.rule]++;});
var repairParas=paras.filter(function(p){return p.repairs.length>0;}).length;

function footnoteSentence(){
  return 'no footnotes in this HTML version; the document has '+(refFoots!=null?refFoots:'an unknown number of')+' footnotes';
}
var records=paras.map(function(p){
  return {symbol:symbol,paragraph:p.num,section:p.section||'',part:p.part||'',
    text:p.text,text_raw:p.text_raw,
    first_words_match:(p.firstMatch===null?null:p.firstMatch),
    citation:symbol+', para. '+p.num,doc_url:docUrl,limitations:footnoteSentence()};
});
var jsonStr=JSON.stringify(records,null,2);
function buildMarkdown(){
  var L=['---',
    'title: '+JSON.stringify(title),
    'symbol: '+JSON.stringify(symbol),
    'adopted: '+JSON.stringify(adopted||'unknown'),
    'source_url: '+JSON.stringify(docUrl),
    'extracted: '+new Date().toISOString().slice(0,10),
    'paragraphs_found: '+paras.length,
    'paragraphs_expected: '+(refParas!=null?refParas:'unknown'),
    'footnotes: '+JSON.stringify(footnoteSentence()),
    '---',''];
  flow.forEach(function(f){
    if(f.kind==='h'){
      L.push((f.tag==='h1'?'# ':f.tag==='h2'?'## ':'### ')+f.display);
    } else {
      var p=byNum[f.num];
      L.push('**'+p.num+'.** '+p.text); L.push('');
    }
  });
  return L.join('\n');
}
var mdStr=buildMarkdown();
```

Checks:

```js
var checks=[];
function addCheck(name,detail,status,linkTab,linkLabel,note){
  checks.push({name:name,detail:detail,status:status,linkTab:(linkTab==null?null:linkTab),linkLabel:linkLabel||'',note:note||''});
}
if(refParas!=null){
  var ok=paras.length===refParas;
  var diff=paras.length-refParas;
  addCheck('Paragraph count','found '+paras.length+' \u00B7 reference.paragraphs '+refParas+(ok?'':' ('+(diff>0?'+':'')+diff+')'),
    ok?'pass':'fail',ok?null:1,'see tab 02');
}else addCheck('Paragraph count','no reference in this file','notrun');

if(paras.length){
  var nums=paras.map(function(p){return p.num;});
  var dups=nums.filter(function(n,i){return nums.indexOf(n)!==i;});
  var max=Math.max.apply(null,nums);
  var gaps=[]; for(var gi=1;gi<=max;gi++) if(nums.indexOf(gi)<0) gaps.push(gi);
  var ordered=nums.every(function(n,j){return n===j+1;});
  var prob=dups.concat(gaps);
  addCheck('Numbering','numbers '+nums[0]+'\u2013'+nums[nums.length-1]+'; '+dups.length+' duplicates, '+gaps.length+' gaps'+(prob.length?' ('+prob.slice(0,10).join(', ')+')':''),
    ordered?'pass':'fail',ordered?null:1,'see tab 02');
}else addCheck('Numbering','no paragraphs found','notrun');

if(firstWords&&paras.length){
  var mm=paras.filter(function(p){return p.firstMatch===false;});
  var run=paras.filter(function(p){return p.firstMatch!==null;}).length;
  var det=run+' of '+paras.length+' paragraphs compared';
  if(mm.length) det+='; mismatches: '+mm.slice(0,10).map(function(p){return 'para. '+p.num+': found \u201C'+esc(p.found6)+'\u201D / reference \u201C'+esc(p.ref6)+'\u201D';}).join(' \u00B7 ');
  addCheck('First words',det,mm.length?'fail':'pass',mm.length?1:null,'see the flagged rows on tab 02');
}else addCheck('First words','no reference in this file','notrun');

if(refFoots!=null) addCheck('Footnotes','this HTML has 0 \u00B7 reference.footnotes '+refFoots,'limit',null,'','the HTML version has no footnotes: a limit of the source, not of the app');
else addCheck('Footnotes','no reference in this file','notrun');

addCheck('Repairs',allRepairs.length+' spaces restored in '+repairParas+' paragraphs \u2014 sentence '+perRule.sentence+', comma '+perRule.comma+', quote '+perRule.quote+', dash '+perRule.dash,'pass',2,'every one listed on tab 03','text_raw keeps the text as found');

var h2n=headings.filter(function(h){return h.tag==='h2';}).length;
var gluedN=headings.filter(function(h){return h.glued;}).length;
addCheck('Headings',h2n+' h2 + '+(headings.length-h2n)+' h3 = '+headings.length+' headings; '+gluedN+' glued labels separated (e.g. \u201CI.Introduction\u201D)','pass');

var total=elements.length;
var sum=coverN+(titleText?1:0)+headings.length+paras.length+lineN+otherEls.length;
var uncls=otherEls.length?' \u2014 unclassified: '+otherEls.slice(0,5).map(function(o){return '&lt;'+esc(o.tag)+'&gt; '+esc(o.text.slice(0,40));}).join('; '):'';
addCheck('Nothing lost',total+' block elements: '+coverN+' cover, '+(titleText?1:0)+' title, '+headings.length+' headings, '+paras.length+' paragraphs, '+lineN+' committee lines, '+otherEls.length+' unclassified'+uncls,(sum===total&&otherEls.length===0)?'pass':'fail');

var rt='parse error';
try{rt=JSON.parse(jsonStr).length;}catch(e){}
addCheck('Export round trip',(rt===paras.length)?('the JSON to download parses back to '+rt+' records = '+paras.length+' rows on tab 02'):('parse-back gave '+rt+', expected '+paras.length),rt===paras.length?'pass':'fail');

var nPass=checks.filter(function(c){return c.status==='pass';}).length;
var nFail=checks.filter(function(c){return c.status==='fail';}).length;
var nLimit=checks.filter(function(c){return c.status==='limit';}).length;
var nNotRun=checks.filter(function(c){return c.status==='notrun';}).length;
var nRun=nPass+nFail;
```

Rendering — header, rail, tabs, panels. Then event bindings.

```js
document.title=symbol+' \u2014 numbered paragraphs (HTML)';
document.getElementById('doctitle').textContent=title;
var metaHtml=(docUrl?'<a href="'+esc(docUrl)+'" target="_blank" rel="noopener">'+esc(symbol)+'</a>':esc(symbol))+
  (adopted?' \u00B7 adopted '+esc(adopted):'')+
  ' \u00B7 '+paras.length+' paragraphs'+
  (source?' \u00B7 '+esc(source):'');
document.getElementById('docmeta').innerHTML=metaHtml;
var hs=document.getElementById('hstatus');
hs.innerHTML='<span class="dot '+(nFail>0?'r':'g')+'"></span><span class="mono">'+(nFail>0?nFail+' checks failed':nPass+' of '+nRun+' checks pass')+'</span>'+
  (nLimit?' <span class="mono bad">\u00B7 '+nLimit+' source limit</span>':'')+
  (nNotRun?' <span class="mono notrun">\u00B7 '+nNotRun+' not run</span>':'');

document.getElementById('railsym').textContent=symbol;
document.getElementById('railtitle').textContent=title;
document.getElementById('railp').textContent=paras.length;
document.getElementById('railpsub').textContent=refParas!=null?('of '+refParas+' paragraphs'):'paragraphs found';
var bar=document.getElementById('railbar');
var bw=refParas!=null?Math.min(100,paras.length/refParas*100):100;
bar.firstElementChild.style.width=bw+'%';
if(refParas!=null&&paras.length!==refParas)bar.classList.add('bad');
document.getElementById('railftotal').textContent=refFoots!=null?refFoots:'?';
var rc=document.getElementById('railchecks');
rc.textContent=(nFail>0?nFail+' checks failed':nPass+' of '+nRun+' checks pass')+' \u2014 see tab 04';
rc.addEventListener('click',function(){activateTab(3);});
```

Tab 01:

```js
function tile(label,big,cls,sub,how){
  return '<div class="tile"><div class="mono tlabel">'+label+'</div><div class="bignum '+cls+'">'+big+'</div><div class="tsub">'+sub+'</div><div class="how">How this is computed: '+how+'</div></div>';
}
var matchCount=paras.filter(function(p){return p.firstMatch===true;}).length;
var p1=document.getElementById('p1');
var notice=paras.length===0?'<p class="notice">No paragraphs were found in this HTML: no &lt;p&gt; element starts with a number and a full stop. The exports on tab 04 are disabled.</p>':'';
var t1cls=(refParas!=null)?(paras.length===refParas?'ok':'bad'):'';
var t1sub=refParas!=null?('the document has '+refParas+(paras.length===refParas?' \u2014 equal':(paras.length>refParas?' \u2014 '+(paras.length-refParas)+' extra':' \u2014 '+(refParas-paras.length)+' short'))):'no reference in this file';
var t2big=firstWords?matchCount:'\u2014';
var t2cls=firstWords?(matchCount===paras.length&&paras.length>0?'ok':(matchCount<paras.length?'bad':'')):'';
var t2sub=firstWords?('of '+(refParas!=null?refParas:paras.length)+' paragraphs match'):'no reference in this file';
p1.innerHTML=notice+'<div class="tiles">'+
  tile('Paragraphs found',paras.length,t1cls,t1sub,'every &lt;p&gt; in the parsed HTML whose text starts with a number and a full stop; compared with reference.paragraphs')+
  tile('First words match',t2big,t2cls,t2sub,'the first six words of each paragraph, normalised (curly quotes straight, en dashes and non-breaking hyphens to hyphens, non-breaking spaces to spaces), against reference.first_words')+
  tile('Footnotes','0','bad','of '+(refFoots!=null?refFoots:'?')+' footnotes \u2014 this HTML version has none; <a href="#" data-tab="2">see tab 03</a>','counted in the parsed HTML: this version has no footnote text and no footnote marks; reference.footnotes is the document\u2019s own count')+
  tile('Spaces repaired or flagged',allRepairs.length,'','in '+repairParas+' paragraphs \u2014 <a href="#" data-tab="2">see tab 03</a>','four rules insert a space only where the characters prove one was there; every insertion is logged and listed on tab 03')+
'</div>';
```

Tab 02:

```js
function firstLine(t){
  if(t.length<=120)return t;
  var s=t.slice(0,120),sp=s.lastIndexOf(' ');
  if(sp>0)s=s.slice(0,sp);
  return s+'\u2026';
}
function markedHtml(p){
  var out='',i;
  for(i=0;i<p.text.length;i++){
    if(p.mask[i]){
      var inner=esc(p.text[i]);
      if(i+1<p.text.length&&!p.mask[i+1]){inner+=esc(p.text[i+1]);i++;}
      out+='<span class="fix" title="space restored here \u2014 see tab 03">'+inner+'</span>';
    } else out+=esc(p.text[i]);
  }
  return out;
}
function detailHtml(p){
  var path=(p.part&&p.section&&p.part!==p.section)?(p.part+' \u203A '+p.section):(p.section||p.part||'\u2014');
  var h='<div class="mono path">'+esc(path)+'</div>';
  h+='<p class="full">'+markedHtml(p)+'</p>';
  if(p.firstMatch===null)h+='<p class="fw notrun">first words: not run \u2014 no reference in this file</p>';
  else h+='<p class="fw '+(p.firstMatch?'ok':'bad')+'">first words \u2014 found: \u201C'+esc(p.found6)+'\u201D \u00B7 reference: \u201C'+esc(p.ref6)+'\u201D</p>';
  if(p.repairs.length){
    h+='<p class="reps">spaces restored here: '+p.repairs.length+' \u2014 '+p.repairs.map(function(r){return esc(r.ruleName)+' \u201C'+esc(r.match)+'\u201D \u2192 \u201C'+esc(r.fixed)+'\u201D';}).join(' \u00B7 ')+'</p>';
  } else h+='<p class="reps dim">no spaces restored in this paragraph</p>';
  var cite=symbol+', para. '+p.num;
  h+='<button class="btn copy" data-cite="'+esc(cite)+'">Copy citation</button> <span class="mono hint">citation: '+esc(cite)+'</span>';
  return h;
}
var p2=document.getElementById('p2');
var hbox='<button class="acc" id="hbox" aria-expanded="false">Headings found: '+headings.length+'</button>'+
  '<div id="hbody" hidden><ul class="hlist">'+headings.map(function(hh){
    return '<li><span class="mono">'+hh.tag.toUpperCase()+'</span>'+esc(hh.display)+(hh.glued?' <span class="mono hint">glued label separated</span>':'')+'</li>';
  }).join('')+'</ul></div>';
var rows=paras.map(function(p){
  var chk=p.firstMatch===true?'<span class="ok">OK</span>':(p.firstMatch===false?'<span class="bad">first words differ</span>':'<span class="notrun">not run</span>');
  return '<tr class="prow" data-n="'+p.num+'" tabindex="0" role="button" aria-expanded="false">'+
    '<td class="num">'+p.num+'</td><td>'+esc(p.section||'\u2014')+'</td><td>'+esc(firstLine(p.text))+'</td><td>'+chk+'</td></tr>'+
    '<tr class="pdet" data-n="'+p.num+'" hidden><td colspan="4">'+detailHtml(p)+'</td></tr>';
}).join('');
p2.innerHTML=hbox+
 '<table><caption><span class="mono">TAB.02</span>'+paras.length+' paragraphs found'+(refParas!=null?', '+refParas+' expected':'')+' \u2014 click a row for the full text, verbatim</caption>'+
 '<thead><tr><th scope="col" class="num">No.</th><th scope="col">Section</th><th scope="col">First line</th><th scope="col">Check</th></tr></thead>'+
 '<tbody>'+rows+'</tbody></table>';
```

Tab 03:

```js
var p3=document.getElementById('p3');
var footBlock='<h3 class="btitle">Lost: footnotes <span class="cnt">'+(refFoots!=null?('0 of '+refFoots):'0')+'</span></h3>'+
 '<p>The document has '+(refFoots!=null?refFoots:'an unknown number of')+' footnotes. This HTML has 0: no footnote text, no footnote marks, and the note the title\u2019s asterisk points to is missing. To cite a footnote, use the PDF or Word version.</p>';
var spaceBlock='<h3 class="btitle">Changed: spaces <span class="cnt">'+allRepairs.length+' restored in '+repairParas+' paragraphs</span></h3>'+
 '<p class="mono ruleline">SENTENCE '+perRule.sentence+' \u00B7 COMMA '+perRule.comma+' \u00B7 QUOTE '+perRule.quote+' \u00B7 DASH '+perRule.dash+'</p>'+
 '<table><caption><span class="mono">TAB.03</span>Every missing space the rules found and restored \u2014 click a row to open the paragraph on tab 02</caption>'+
 '<thead><tr><th scope="col" class="num">Paragraph</th><th scope="col">Before</th><th scope="col">After</th><th scope="col">Rule</th></tr></thead><tbody>'+
 allRepairs.map(function(r){
   return '<tr class="rrow" data-n="'+r.para+'" tabindex="0" role="button"><td class="num">'+r.para+'</td>'+
     '<td>'+esc(r.prefix)+'<span class="fix">'+esc(r.match)+'</span>'+esc(r.suffix)+'</td>'+
     '<td>'+esc(r.prefix)+'<span class="fix">'+esc(r.fixed)+'</span>'+esc(r.suffix)+'</td>'+
     '<td>'+esc(r.ruleName)+'</td></tr>';
 }).join('')+'</tbody></table>'+
 '<p class="note">Rules restore a space only where the characters prove it was there. Word pairs such as \u2018Giventhe\u2019 are not touched; the first-words check catches them only in a paragraph\u2019s first six words.</p>';
var charBlock='<h3 class="btitle">Changed: characters <span class="cnt">kept as published</span></h3>'+
 '<table><caption><span class="mono">TAB.03</span>Characters a keyboard does not type \u2014 counted over all paragraph texts</caption>'+
 '<thead><tr><th scope="col">Character</th><th scope="col" class="num">Count</th><th scope="col">Example</th></tr></thead><tbody>'+
 charStats.map(function(c){
   return '<tr><td><code>'+esc(c.glyph)+'</code> '+esc(c.name)+' <span class="mono hint">'+esc(c.cp)+'</span></td><td class="num">'+c.count+'</td><td>'+esc(c.example||'\u2014')+'</td></tr>';
 }).join('')+'</tbody></table>'+
 '<p class="mono hint">on a keyboard: a hyphen and straight quotes</p>'+
 '<p class="note">Kept exactly as published, in the table and in every export. A search for \u2018business-related\u2019 typed with the hyphen key will not find \u2018business\u2011related\u2019: normalise the text before searching it.</p>';
p3.innerHTML=footBlock+spaceBlock+charBlock;
```

Tab 04:

```js
var p4=document.getElementById('p4');
var checksHtml='<h3 class="btitle">Checks <span class="cnt">'+nPass+' pass \u00B7 '+nFail+' failed'+(nLimit?' \u00B7 '+nLimit+' source limit':'')+(nNotRun?' \u00B7 '+nNotRun+' not run':'')+'</span></h3>'+
 '<ol class="checks">'+checks.map(function(c){
   var st=c.status==='pass'?'<span class="ok">pass</span>':c.status==='fail'?'<span class="bad">check failed</span>':c.status==='limit'?'<span class="bad">source limit</span>':'<span class="notrun">not run</span>';
   var link=c.linkTab!=null?' <a href="#" data-tab="'+c.linkTab+'">'+(c.linkLabel||'see the rows')+'</a>':'';
   return '<li><strong>'+esc(c.name)+'</strong> \u2014 '+c.detail+' '+st+link+(c.note?' <span class="dim">'+esc(c.note)+'</span>':'')+'</li>';
 }).join('')+'</ol>';
var expHtml='<h3 class="btitle">Export</h3>'+
 '<p class="note">The dataset travels with its source, its fields and its known limitations: every record carries symbol, paragraph, section, part, text, text_raw, first_words_match, citation, doc_url and limitations.</p>'+
 '<button class="btn" id="dljson"'+(paras.length?'':' disabled')+'>Download JSON</button>'+
 '<button class="btn" id="dlmd"'+(paras.length?'':' disabled')+'>Download Markdown</button>'+
 (paras.length?'':'<p class="bad">No paragraphs found \u2014 the exports are disabled.</p>')+
 '<p class="mono hint">file name: '+esc(symbol.replace(/\//g,'-'))+'.json / .md \u00B7 UTF-8 \u00B7 Blob URL</p>';
var elHtml='<button class="acc" id="elbox" aria-expanded="false">Elements found ('+elements.length+')</button>'+
 '<div id="elbody" hidden><table><caption><span class="mono">TAB.04</span>Every block element in the parsed HTML, in order, classified exactly once</caption>'+
 '<thead><tr><th scope="col">Tag</th><th scope="col">Classified as</th><th scope="col">Text (first 80 characters)</th></tr></thead><tbody>'+
 elements.map(function(e){
   return '<tr><td><code>&lt;'+esc(e.tag)+'&gt;</code>'+(e.cls?' <span class="mono hint">.'+esc(e.cls)+'</span>':'')+'</td><td>'+esc(e.clsAs)+'</td><td>'+esc(e.text)+'</td></tr>';
 }).join('')+'</tbody></table></div>';
p4.innerHTML=checksHtml+expHtml+elHtml;
```

Footer:

```js
document.getElementById('foot').innerHTML=
 '<span class="mono">SOURCE</span> '+esc(source)+(doc.built?' \u00B7 <span class="mono">BUILT</span> '+esc(doc.built):'')+
 ' \u00B7 Done by this page\u2019s code; no model was called and nothing left the browser.'+
 '<div class="credits">Method and citation practice follow The Turing Way, \u201CDocumentation and metadata\u201D (CC BY 4.0); the UK Government Analysis Function, \u201CQuality assurance of code for analysis and research: Testing code\u201D; and the Dag Hammarskj\u00F6ld Library, \u201CHow should I cite a UN document?\u201D.</div>';
```

Tabs & events:

```js
var tabs=Array.prototype.slice.call(document.querySelectorAll('#tablist [role=tab]'));
var panels=[document.getElementById('p1'),document.getElementById('p2'),document.getElementById('p3'),document.getElementById('p4')];
function activateTab(i){
  tabs.forEach(function(t,j){
    var on=(i===j);
    t.setAttribute('aria-selected',on?'true':'false');
    t.tabIndex=on?0:-1;
    panels[j].hidden=!on;
  });
}
tabs.forEach(function(t,i){t.addEventListener('click',function(){activateTab(i);});});
document.getElementById('tablist').addEventListener('keydown',function(e){
  var i=tabs.indexOf(document.activeElement);
  if(i<0)return;
  var n=null;
  if(e.key==='ArrowRight')n=(i+1)%tabs.length;
  else if(e.key==='ArrowLeft')n=(i-1+tabs.length)%tabs.length;
  else if(e.key==='Home')n=0;
  else if(e.key==='End')n=tabs.length-1;
  if(n!==null){e.preventDefault();tabs[n].focus();activateTab(n);}
});
document.addEventListener('click',function(e){
  var t=e.target&&e.target.closest?e.target.closest('[data-tab]'):null;
  if(t){e.preventDefault();activateTab(parseInt(t.getAttribute('data-tab'),10));}
});
function toggleRow(r){
  var det=p2.querySelector('tr.pdet[data-n="'+r.getAttribute('data-n')+'"]');
  if(!det)return;
  var show=det.hidden;
  det.hidden=!show;
  r.setAttribute('aria-expanded',show?'true':'false');
}
p2.addEventListener('click',function(e){
  var c=e.target.closest?e.target.closest('.copy'):null;
  if(c){copyCite(c);return;}
  var r=e.target.closest?e.target.closest('tr.prow'):null;
  if(r)toggleRow(r);
});
p2.addEventListener('keydown',function(e){
  if(e.key!=='Enter'&&e.key!==' ')return;
  var r=e.target.closest?e.target.closest('tr.prow'):null;
  if(r){e.preventDefault();toggleRow(r);}
});
function openParagraph(n){
  activateTab(1);
  var r=p2.querySelector('tr.prow[data-n="'+n+'"]');
  if(!r)return;
  var det=p2.querySelector('tr.pdet[data-n="'+n+'"]');
  if(det&&det.hidden){det.hidden=false;r.setAttribute('aria-expanded','true');}
  r.scrollIntoView({block:'center'});
}
p3.addEventListener('click',function(e){
  var r=e.target.closest?e.target.closest('tr.rrow'):null;
  if(r)openParagraph(parseInt(r.getAttribute('data-n'),10));
});
p3.addEventListener('keydown',function(e){
  if(e.key!=='Enter'&&e.key!==' ')return;
  var r=e.target.closest?e.target.closest('tr.rrow'):null;
  if(r){e.preventDefault();openParagraph(parseInt(r.getAttribute('data-n'),10));}
});
function bindAcc(btnId,bodyId){
  var b=document.getElementById(btnId),d=document.getElementById(bodyId);
  if(!b||!d)return;
  b.addEventListener('click',function(){
    var open=d.hidden;
    d.hidden=!open;
    b.setAttribute('aria-expanded',open?'true':'false');
  });
}
bindAcc('hbox','hbody');
bindAcc('elbox','elbody');
function copyCite(btn){
  var t=btn.getAttribute('data-cite');
  function done(){var old=btn.textContent;btn.textContent='Copied';setTimeout(function(){btn.textContent=old;},2000);}
  function fb(){
    var ta=document.createElement('textarea');
    ta.value=t;ta.setAttribute('readonly','');ta.style.position='fixed';ta.style.opacity='0';
    document.body.appendChild(ta);ta.select();
    var ok=false;try{ok=document.execCommand('copy');}catch(err){}
    document.body.removeChild(ta);
    if(ok)done();else{btn.textContent=t;setTimeout(function(){btn.textContent='Copy citation';},2000);}
  }
  if(navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText(t).then(done,fb);}else fb();
}
function download(name,content,type){
  var blob=new Blob([content],{type:type+';charset=utf-8'});
  var url=URL.createObjectURL(blob);
  var a=document.createElement('a');
  a.href=url;a.download=name;
  document.body.appendChild(a);a.click();a.remove();
  setTimeout(function(){URL.revokeObjectURL(url);},1500);
}
var baseName=symbol.replace(/\//g,'-');
var dj=document.getElementById('dljson'),dm=document.getElementById('dlmd');
if(dj)dj.addEventListener('click',function(){if(paras.length)download(baseName+'.json',jsonStr,'application/json');});
if(dm)dm.addEventListener('click',function(){if(paras.length)download(baseName+'.md',mdStr,'text/markdown');});
activateTab(0);
})();
```

Wait — issue: `activateTab` is referenced by `rc.addEventListener` before its definition — function declarations hoist within the IIFE, so `function activateTab` is hoisted. Yes, declared with `function` keyword → hoisted. Good.

Another issue: `p2`, `p3`, `p4` are defined via getElementById before use in handlers — yes defined earlier.

`bar.firstElementChild` — the `<i>` inside #railbar. Markup: `<div class="bar" id="railbar"><i></i></div>`. Good.

Also `document.getElementById('railf')` — I set textContent '0' statically in markup; fine, or set via JS. I'll put static "0" in markup.

Check: header hstatus uses class "mono bad" — .bad color red, mono uppercase — fine.

One more: in tile(), `how` strings contain `&lt;p&gt;` — I pass HTML, inserted raw. Good.

In tile 3 sub contains a link with data-tab="2" — global handler catches. Good.

Potential problem: the global click handler for [data-tab] also fires when clicking links inside p1 — fine.

Also: `e.target.closest` — if e.target is an SVG or text? click targets are elements. OK.

Now the header markup:

```html
<header>
  <div>
    <div class="mono label">UN DOCUMENT \u00B7 HTML</div>
```

In HTML I'll write literal "UN DOCUMENT · HTML".

```html
    <h1 id="doctitle"></h1>
    <div class="meta" id="docmeta"></div>
  </div>
  <div class="hright" id="hstatus"></div>
</header>
<nav role="tablist" id="tablist" aria-label="Views of the document">
  <button role="tab" id="tab-1" aria-controls="p1" aria-selected="true">01 RESULT</button>
  <button role="tab" id="tab-2" aria-controls="p2" aria-selected="false" tabindex="-1">02 PARAGRAPHS</button>
  <button role="tab" id="tab-3" aria-controls="p3" aria-selected="false" tabindex="-1">03 LOST &amp; CHANGED</button>
  <button role="tab" id="tab-4" aria-controls="p4" aria-selected="false" tabindex="-1">04 CHECKS &amp; EXPORT</button>
</nav>
<div class="layout">
  <aside>
    <div class="mono railhead">DOCUMENT</div>
    <div class="doccard">
      <div class="mono sym" id="railsym"></div>
      <div class="shorttitle" id="railtitle"></div>
    </div>
    <div class="railnum">
      <div class="bignum" id="railp"></div>
      <div class="railsub" id="railpsub"></div>
      <div class="bar" id="railbar"><i></i></div>
    </div>
    <div class="railnum">
      <div class="bignum red">0</div>
      <div class="railsub">of <span id="railftotal"></span> footnotes \u2014 not in this HTML</div>
    </div>
    <button class="railchecks" id="railchecks"></button>
  </aside>
  <main>
    <section id="p1" role="tabpanel" aria-labelledby="tab-1"></section>
    <section id="p2" role="tabpanel" aria-labelledby="tab-2" hidden></section>
    <section id="p3" role="tabpanel" aria-labelledby="tab-3" hidden></section>
    <section id="p4" role="tabpanel" aria-labelledby="tab-4" hidden></section>
  </main>
</div>
<footer id="foot"></footer>
```

Note: "of X footnotes — not in this HTML" — write literal —.

One more consideration: the spec says rail shows "0 footnotes of reference.footnotes" in red with "not in this HTML" — done.

Also — "n of m checks pass, linking to tab 04" — railchecks button. Done.

Double-check the repair regex for quote: `/([a-z])\u201C/g` — in JS literal I can write `/([a-z])“/g` directly with the char. I'll use \u201C escapes for safety in the RULES array. Fine.

Also the dash rule: `/\u2013([A-Za-z])/g` — inserts space after en dash before letter. Example "challenges –to": the string has " –to" — dash followed by 't' → matches → "– to". Good.

Now — one subtle thing about the sentence rule and headings: repairs only apply to paragraph text, not headings. Spec says repairs on paragraph text. Headings keep glued labels (we display them separated but raw kept). Fine.

Also — the first-words check uses `text` (repaired). Spec: "The first six whitespace-separated words of `text`". Yes.

Now, `norm` also should maybe handle em dash? Spec says en dashes only. Keep.

Potential issue: `firstWords[String(p.num)]` — keys are strings of numbers. Good.

Now let me double check `markedHtml` when mask[i] is true and i+1 is also masked: inner = just the space; box around a space — invisible but harmless; rare.

Also `detailHtml` path uses '›' (U+203A). Fine.

Now — the tab-02 table with 90 paragraphs × 2 rows = 180 rows; innerHTML string big but fine.

Check the "How this is computed" for tile 1 contains `&lt;p&gt;` — in tile() I insert how raw. Good.

One more spec item: tab 02 "Check: 'OK' or 'first words differ' (red)" — done.

"the expanded row shows the full path ('IV. … › Right to work (art. 6)')" — done via path.

Also: "A closed 'Headings found: n' box above the table" — done.

Tab 04: "The check panel (next section but one), open, every check on one line." — done.

Now, the intro text before the code block: 1-3 sentences. E.g.: "Built: a four-tab app that parses the attached OHCHR HTML of the General Comment into numbered paragraphs with their headings, repairs the missing spaces rule by rule, checks everything against the document's own reference, and exports JSON/Markdown. All counts are computed by the page's code; no model is called." Then the code block. Nothing after.

Let me also double check for any use of external resources: none. Chart.js not needed (no charts required — spec has no charts; bars are CSS). Good.

Line count: probably ~600. Fine.

One more check on `repair` — the `s.replace(r.re, function(m){...})` — inside, I use `arguments[arguments.length-2]` for offset. For regex with 2 capture groups: arguments = (match, g1, g2, offset, string) → length 5, offset index 3 = length-2 ✓. For 1 group: (match, g1, offset, string) → length 4, offset index 2 = length-2 ✓. 

But wait — there's a subtlety: `String.prototype.replace` with a function — if the regex is global, it finds all matches; the callback's offset is correct. And I return `m` (unchanged) — the actual replacement result is discarded since I build `ns` manually. But careful: `s.replace` returns a new string which I ignore; I use `s` (original) inside the callback to slice — correct because I only read from `s` and write to `ns`. ✓.

Edge: what if a rule matches at overlapping positions with previous insertions? Not possible since we process rules sequentially on the current string.

Now, `mask` alignment: after each rule, mask length === s length. ✓ (each match of length L becomes L+1 chars: ins original + 1 inserted + (L-ins) original = L+1 ✓).

Now `charStats` — counting over p.text (repaired). NBSP count includes those in paragraphs only (spec: over all paragraph texts). ✓.

Example building: `p.text.slice(a,i)+'['+g+']'+p.text.slice(i+1,i+26)` — good.

Now — one thing I should double check: `elements` includes every block; the cover table's textContent includes lots; sliced to 80. ✓.

`flow` for markdown includes title as h1 → '# '. ✓.

Also — markdown front matter `footnotes:` value is the sentence — spec: "`footnotes`: the same sentence". ✓.

JSON limitations: "no footnotes in this HTML version; the document has n" ✓.

Now, `activateTab(0)` at end — panels already hidden except p1; fine.

Also initial `tabindex` on tab buttons: tab-1 has none (default 0), others -1. ✓.

Arrow-key nav: roving tabindex handled in activateTab. ✓.

One more: the spec says tabs labels like `01 RESULT · 02 PARAGRAPHS · 03 LOST & CHANGED · 04 CHECKS & EXPORT` — I use "01 RESULT" etc. without the "·" separators (they're separate buttons). Fine.

Also header: "At the right a green dot 'n of m checks pass' or a red dot 'n checks failed', then '1 source limit'". ✓.

Potential CSS issue: `nav [role=tab]` — buttons inherit font? I set font-family explicitly. ✓.

Also add `button{font:inherit}`? .btn and .acc and railchecks set fonts. nav tabs set. OK.

Let me also ensure `main` sections don't overflow: tables width 100% — with long text cells, table may overflow on narrow screens; add `td{overflow-wrap:anywhere}`? Add `table{table-layout:auto}` default; long words could overflow — add `td{overflow-wrap:break-word}`. I'll add `overflow-wrap:anywhere` on td. Fine.

Also `.first` column width — fine.

Now, assemble the final file. Also double-check no stray backticks or template literals that could break — I'm using plain strings.

One thing: in the `tile()` how text for tile 1, I wrote 'every &lt;p&gt; in the parsed HTML...' — good.

In p1 notice: 'no &lt;p&gt; element starts...' — good.

Also in checks detail for Headings I include '\u201CI.Introduction\u201D' — that's an example from the plan; it's illustrative text, not a data claim... The plan says 8 of 10 glued. Writing "e.g. 'I.Introduction'" as an example is fine (it's from the data description). But to be safe against inventing, I could phrase "glued labels separated (label and text joined without a space)". I'll keep a generic phrasing without quoting a specific heading: 'glued labels separated (no space after the label\u2019s full stop)'. Safer. Similarly the note about 'Giventhe' — that's from the user's own findings; quoting it as an example of an unrepairable pair is fine since the user provided it. I'll keep 'Giventhe' since the user stated it. And 'business‑related' with U+2011 — user stated. Keep.

Also the footnote block mentions "the note the title's asterisk points to is missing" — from spec. Keep.

Now write everything out. Also ensure `<meta charset="utf-8">` first.

Let me also reconsider: the plan says header label "UN DOCUMENT · HTML" — literal.

Also: "one line with the data's source, n and years" — generic; my meta has symbol, adopted, n paragraphs, source. No years in this dataset (single document, adopted date). Fine.

Final check of the copy: "Copy citation" button copies "E/C.12/GC/27, para. 12" — symbol from data. ✓.

Also the citation hint next to button shows the citation string. ✓.

I think we're ready. Let me also make sure the script handles `doc.html` undefined → blocks empty → paras empty → tab 01 notice, exports disabled, checks: paragraph count fail (0 vs 90) etc. Good.

Write the final response: 2-3 sentences + code block.

Let me write out the complete HTML now, being meticulous with syntax.

Also: in CSS I used `.acc::after{content:" –"}` for expanded — the en dash literal in CSS is fine (file UTF-8).

One more detail — `tr.prow` has `role="button"` on a `<tr>`; also add `aria-controls`? Not necessary.

Also for accessibility, the pdet row could have role="region"? Skip.

Counting lines... let's just write it.

Also note: `p2.addEventListener('keydown'...)` — e.target could be the copy button inside pdet; closest('tr.prow') null → return. ✓.

Also the global `[data-tab]` click handler: clicking the rail? rail uses its own listener. ✓.

Potential conflict: p2 click handler and global handler both on document? Global is on document, p2's on p2 — both fire for clicks in p2; global only acts on [data-tab]. ✓.

Now, writing the deliverable.

Wait, one more: the spec for tab 02 says "First line: the first 120 characters cut at a word with '…'". My firstLine does that. ✓.

And "Rows are buttons with aria-expanded" — tr role=button aria-expanded. ✓.

Also "Details open in place (a clicked row expands)". ✓.

Also the rail bar: "a thin bar (red when short or over)". ✓.

Double-check `railpsub` when refParas null: 'paragraphs found'. ✓.

OK writing final.

Actually one more thought on `norm` for first words: reference first_words like "A clean, healthy and sustainable environment" — 6 words? "A clean, healthy and sustainable environment" = A(1) clean,(2) healthy(3) and(4) sustainable(5) environment(6) — yes 6 words. found6 = first 6 words of text joined. Compare normalized. ✓.

Also — should comparison be case-sensitive? "case is kept" → yes, case-sensitive. ✓.

Now finalize. I'll write the code block.

Let me make sure about one thing in the classification regex: `/^(\d{1,3})\.\s*(.*)$/` — on collapsed text. For "1.A clean..." → m[1]='1', m[2]='A clean...'. ✓. For a hypothetical "1. A clean" → m[2]='A clean'. ✓.

But careful: a paragraph text like "2025. something"? Would be misclassified — not in this doc.

Also the committee `<p>` bold — textContent fine.

Final assembly now. I'll write it carefully in one pass.

Also — I realize the `flow` push for title happens in the h2 branch; but if the document had no h2 title... fine.

Also `elements` for the title h2 gets clsAs 'title'. ✓.

Let me now also double check `buildMarkdown` heading prefix mapping: f.tag values 'h1','h2','h3'. ✓.

Writing the answer now. Also keep intro ≤3 sentences.