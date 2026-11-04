Let me plan this app carefully. The user wants a single HTML file app that parses `WORKSHOP_DATA.html_doc` (E/C.12/GC/27 HTML), extracts numbered paragraphs, checks against reference, shows lost/changed things, and exports JSON/Markdown.

Key requirements:
- Header: monospace label "UN DOCUMENT · HTML", serif title, one line with symbol linked to doc_url, "adopted reference.adopted", source. Right side: green dot "n of m checks pass" or red dot "n checks failed", then "1 source limit".
- Left rail: "DOCUMENT" heading, card with symbol + short title, big numbers "n paragraphs of reference.paragraphs" with thin bar, "0 footnotes of reference.footnotes" in red "not in this HTML", "n of m checks pass" linking to tab 04.
- Tabs: 01 RESULT · 02 PARAGRAPHS · 03 LOST & CHANGED · 04 CHECKS & EXPORT, role="tablist", arrow keys.
- Tab 01: four tiles with big serif numbers + "How this is computed" lines.
- Tab 02: table of paragraphs: No. | Section | First line | Check. Closed "Headings found: n" box above. Rows expand in place with full text, reference six words vs found six, repairs flagged, Copy citation button.
- Tab 03: three blocks: Lost footnotes, Changed spaces (table Paragraph | Before | After | Rule), Changed characters (Character | Count | Example).
- Tab 04: check panel (one line per check), Export buttons (Download JSON, Download Markdown), closed "Elements found (n)" heading with table Tag | Classified as | Text.
- Footer: source, built, "Done by this page's code; no model was called and nothing left the browser."

Pipeline:
- Parse html with DOMParser.
- Classify: elements inside first `<table>` = cover. After it: `<p>` matching `/^(\d{1,3})\.\s*(.*)$/s` = paragraph; first `<h2>` = title; other h2/h3 = headings split by `/^([IVX]+|[A-Z])\.\s*(.+)$/`; other `<p>` = committee line.
- text_raw = text after number+full stop, trimmed, whitespace collapsed.
- Repairs on text: `/([a-z])\.([A-Z])/g` → "$1. $2"; `/([a-z]),([A-Za-z])/g` → "$1, $2"; `/([a-z])“/g` → "$1 “"; `/–([A-Za-z])/g` → "– $1". Log each insertion with paragraph, rule, 20 chars each side.
- Characters counted over all paragraph texts (text after repair? "Counted over all paragraph texts" — I'll count over text_raw or text; repairs don't touch those chars, so same). En dash U+2013, curly double quotes U+201C/U+201D, right single quote U+2019, non-breaking hyphen U+2011, non-breaking space U+00A0.
- Section = nearest heading above; part = nearest roman-numbered h2.
- First words: first six whitespace-separated words of `text` vs reference.first_words[String(number)], normalized (curly quotes→straight, en dash & nb-hyphen → hyphen, nbsp → space), case kept.
- Citation = symbol + ", para. " + number.
- Checks: paragraph count, numbering (1..n in order), first words, footnotes (source limit), repairs, headings, nothing lost (every block element classified exactly once, counts sum to total), export round trip.

Edge cases: missing reference → "no reference in this file", checks "not run"; no `<p>` → tab 01 says so, exports disabled.

Design: warm off-white #f4f0e8, ink #1d1b18, rules #d9d2c3, accent #9b2335, green for pass (dark green, e.g. #1e6b3a). Serif Georgia for title/big numbers, monospace labels, sans 16px body. Left rail narrow. Tabs numbered. Max ~7 clickable things per view — tabs (4) + filter headings... In tab 02: tabs 4 + "Headings found" button + rows (rows don't count). Tab 03: tabs + nothing else? The blocks are static. Tab 04: tabs + 2 export buttons + "Elements found" button = 7. OK.

Credits line at bottom for the three sources consulted (Turing Way CC BY, UK Gov Analysis Function OGL, DAG library). The plan lists sources consulted; Turing Way is CC BY 4.0, Analysis Function is OGL 3.0. I'll add a small Credits line.

Layout: header top, then a flex row: left rail (~260px) + main content with tabs. Footer at bottom.

Let me think about the structure of the HTML:

```
<header> label, title, meta line, status dot
<div class="layout">
  <aside class="rail"> DOCUMENT card, numbers, checks link
  <main>
    <div role="tablist"> 4 buttons
    <section id="tab-01"> tiles
    <section id="tab-02"> headings box + table
    <section id="tab-03"> three blocks
    <section id="tab-04"> checks + export + elements
  </main>
</div>
<footer>
```

Tab switching: buttons with role="tab", panels role="tabpanel", arrow key navigation (Left/Right/Home/End), hidden attribute on panels, `[hidden]{display:none!important}`.

Classification details: "Elements inside the first `<table>` are cover." So iterate over body's children (block elements). Actually the html string starts with `<body>...` — DOMParser will parse it; the body element contains the table and div.content. I'll take `doc.body` and iterate `body.children` — but the content is inside `<div class="content">`. Hmm: "the pipeline runs once on load, over the parsed document's `body` elements in order." The structure: body > table (cover), body > div.content > (p committee, h2 title, h2s, h3s, ps). So I should walk all block-level elements in document order: I'll use `body.querySelectorAll('table, div, p, h2, h3')`? Better: walk recursively collecting block elements in order: table, div, p, h2, h3. For the div, it's a container — classify as "container" and recurse into it. Elements inside the first table are cover.

Simpler approach: get all elements in document order via `body.querySelectorAll('*')` and filter to block tags: TABLE, DIV, P, H2, H3. Classification:
- If element is inside the first table (or is the table) → cover.
- DIV → container (recurse naturally since we iterate all in order).
- P matching paragraph regex → paragraph.
- First H2 → title.
- Other H2/H3 → heading.
- Other P → committee line (or "other paragraph").

"Nothing lost" check: every block element classified exactly once and counts per class sum to total. So I'll classify each block element into one class: cover, container, title, heading, paragraph, committee/other. Sum = total block elements.

Wait — elements inside the table: the table itself plus its descendants (tr, td, p, span...). "Elements inside the first `<table>` are cover." I'll count block elements only (table, div, p, h2, h3) — spans aren't block. Inside table there are `<p>` elements (the "United Nations", symbol, etc.). Those are cover. So: for each block element in document order, if it's the first table or has the first table as ancestor → cover.

Heading split: `/^([IVX]+|[A-Z])\.\s*(.+)$/` — "I.Introduction" → label "I", heading "Introduction". "D. Obligation" → label "D", heading "Obligation". If no match, label = null, heading = full text. Note: title h2 ends in " *" — the title is the first h2, classified as title, not heading.

Roman-numbered h2 for `part`: heading whose label matches /^[IVX]+$/.

Section path: nearest heading above the paragraph; expanded row shows full path: part label + heading, e.g. "IV. … › Right to work (art. 6)". I'll build path as the chain of headings from the roman h2 down to the nearest heading. Actually "the full path ('IV. … › Right to work (art. 6)')" — I'll show part label + " › " + nearest heading text (with label if lettered). Maybe show all intermediate headings: e.g. "IV. Economic, social and cultural rights obligations › D. Obligation to respect › Right to work (art. 6)". I'll build the full chain of headings since the last roman h2. That's nicer. Keep it simple: chain of heading labels+texts since last roman heading, joined with " › ".

Repairs logging: for each rule, replace with callback logging {para, rule, before: 20 chars each side of match in text_raw, after}. Rules:
1. sentence: `/([a-z])\.([A-Z])/g` → "$1. $2"
2. comma: `/([a-z]),([A-Za-z])/g` → "$1, $2"
3. quote: `/([a-z])“/g` → "$1 “"
4. dash: `/–([A-Za-z])/g` → "– $1"

Apply sequentially to text_raw to get text. Log context from the current string at time of replacement (20 chars each side).

Careful: applying sentence rule first might create new matches for others? E.g. "levels.Key" → "levels. Key" — then comma rule etc. Fine. Order as given.

Note: the dash rule `/–([A-Za-z])/g` — "challenges –to" has space before dash, letter after: "–to" → "– to". Good.

First words comparison: normalize both sides: replace U+2018/U+2019 → ', U+201C/U+201D → ", U+2013/U+2011 → -, U+00A0 → space. Then split on whitespace, take first 6, join with space, compare. Case kept.

Hmm, "the first six whitespace-separated words of `text`" — text is repaired; repairs only add spaces, could split a word? E.g. if first six words include a repaired join... The reference first_words presumably come from the clean document. The plan says compare first six words of `text` (repaired) against reference. OK, follow the plan.

Checks list (tab 04), each one line: name, what was compared, two values, verdict:
1. Paragraph count: found n vs reference.paragraphs → pass/fail.
2. Numbering: sequence 1..n in order; gaps/duplicates listed → pass/fail.
3. First words: n mismatches listed → pass if 0 else fail with link to tab 02 rows.
4. Footnotes: 0 vs reference.footnotes → "source limit" (red), counted apart from failures.
5. Repairs: n spaces in n paragraphs, per rule → pass (informational; it's a count, "pass" meaning logged completely). I'll mark as pass with counts.
6. Headings: count h2/h3, glued labels separated → pass.
7. Nothing lost: classified counts sum to total block elements → pass/fail, unclassified listed.
8. Export round trip: JSON parsed back, record count equals table rows → pass. This runs when building export (on load, build the JSON string, parse it, compare). Run on load.

Status in header: "n of m checks pass" green dot, or "n checks failed" red dot, plus "1 source limit". m = total checks excluding the source-limit one? The footnotes check is "counted apart from failures". So m = checks that can pass/fail (7 of 8), source limit shown separately. If reference missing: checks needing it show "not run".

Rail: "n paragraphs of reference.paragraphs" big serif with thin bar (red when short or over — bar width = min(n/ref,1)*100%, red if n≠ref, green if equal). "0 footnotes of reference.footnotes" red "not in this HTML". "n of m checks pass" link to tab 04.

Tab 01 tiles:
- Paragraphs found: n (big) beside "the document has reference.paragraphs" — green when equal, red with difference (e.g. "−2" or "+1").
- First words match: n of reference.paragraphs.
- Footnotes: 0 of reference.footnotes, red, "this HTML version has none; see tab 03".
- Spaces: n repaired or flagged, link to tab 03.
Each with "How this is computed" line.

Tab 02: closed "Headings found: n" box (button aria-expanded) listing headings (maybe as a compact list: label + text). Then table with caption "n paragraphs found, m expected" + TAB.02 monospace. Columns: No. | Section | First line | Check. No. right-aligned. Rows are buttons — a row that's a button: I'll make the `<tr>` clickable? Better: each row's first cell contains a button, or make the whole row a button via role. Simplest accessible approach: each `<tr>` has a `<button>` in the No. cell that toggles expansion, with aria-expanded, and the row click also toggles. Actually plan says "Rows are buttons with aria-expanded". I'll make the entire row content wrapped: use a button inside the row spanning... Hmm. Practical approach: `<tr class="prow" tabindex="0" role="button" aria-expanded="false">`? role=button on tr is odd. Alternative: put a button in the first cell ("12") that expands; also clicking anywhere on row triggers. I'll do: each row has a button in the No. cell (the number, styled), aria-expanded controls a following detail row (`<tr class="detail">` with colspan). Clicking the row also toggles. Keyboard: button handles Enter/Space natively. That satisfies "rows are buttons with aria-expanded" reasonably — I'll put aria-expanded on the button and make row click delegate to button.

Detail row content: full text verbatim (text_raw? "the full text, verbatim, never shortened" — show `text` (repaired) with repaired places marked by thin red box, and maybe also raw? Plan: "the full text, verbatim, never shortened; the reference's six words beside the found six; the places repaired or flagged in this paragraph; and a Copy citation button". I'll show the repaired text with `<mark class="repair">` spans around inserted spaces? Marking an inserted space: wrap the boundary — e.g. "levels.<span class=repair> </span>Key"? A thin red box around the inserted space. I can reconstruct: when logging repairs I know positions; simpler: render text and for each repair, wrap the inserted space character in a span with class "repair" (border). To do that, I'll build the repaired text by segments: apply rules with a function that records match index and length, then build HTML with spans. Let me implement: 

```js
function repair(text){
  const logs=[];
  let out=text;
  const rules=[
    {name:'sentence', re:/([a-z])\.([A-Z])/g, rep:(m,a,b)=>a+'. '+b},
    {name:'comma', re:/([a-z]),([A-Za-z])/g, rep:(m,a,b)=>a+', '+b},
    {name:'quote', re:/([a-z])“/g, rep:(m,a)=>a+' “'},
    {name:'dash', re:/–([A-Za-z])/g, rep:(m,a)=>'– '+a},
  ];
  ...
}
```

But sequential application changes indices. Easier: apply each rule to the current string with replace callback that logs context (20 chars each side from the current string) and returns replacement; collect logs. Then to mark in display, I can re-run and build segments: do it in one pass per rule, building output array. Let me write a function that applies all rules in order, producing final string plus a list of {indexInFinal, rule, context}. Since later rules operate on the string after earlier rules, indices shift. Alternative: build final string incrementally with a "pieces" array where each piece is {text, repair:boolean}. Apply rule 1 to the whole raw string via replace with callback — but replace gives me matches in the pre-rule string; I can build pieces by walking matches. Simpler approach: process the string char by char? Overkill.

Pragmatic: apply rules sequentially with logging (context from current string). For display marking, do a second pass: take text_raw, apply rules one at a time, and for each rule, use `String.replace` with a callback that appends to an HTML string, wrapping the inserted space in `<span class="repair"> </span>`. Since I apply rules in the same order to the same starting string, the result equals `text`. So:

```js
function repairHTML(raw){
  let s = raw, logs=[];
  const rules = [...];
  for(const r of rules){
    s = s.replace(r.re, (...args)=>{
      const m = args[0];
      // context: 20 chars each side in the string before this rule? Use current s before replacement — tricky inside replace.
    });
  }
}
```

Inside replace callback I don't have easy access to the pre-replacement string positions... Actually I do: capture `const before = s` before calling replace; within callback, `before.indexOf(m)`? Matches could repeat. Use the offset argument: replace callback receives (match, p1, p2, ..., offset, string). The `string` argument is the original string being replaced (i.e., s before this rule). So offset and string give me context: `string.slice(Math.max(0,offset-20), offset)` and `string.slice(offset+m.length, offset+m.length+20)`. 

So:

```js
function applyRules(raw){
  let s = raw; const logs=[];
  const rules=[
    {key:'sentence', label:'sentence join', re:/([a-z])\.([A-Z])/g, fix:(m,a,b)=>a+'. '+b, ins:'. '},
    ...
  ];
  for(const r of rules){
    s = s.replace(r.re, (m, ...rest)=>{
      const offset = rest[rest.length-2], str = rest[rest.length-1];
      const ctxBefore = str.slice(Math.max(0,offset-20), offset);
      const ctxAfter = str.slice(offset+m.length, offset+m.length+20);
      logs.push({rule:r.key, before:ctxBefore, after:ctxAfter, match:m});
      return r.fix(m, ...);
    });
  }
  return {text:s, logs};
}
```

Wait, fix needs the capture groups: callback args are (match, p1, p2, ..., offset, string). So `r.fix` can be `(m, ...groups)` where groups excludes offset/string. Let me just define fix functions taking (m, g1, g2) and call with the first groups. For rules with one group: (m, g1). I'll handle generically: `const groups = rest.slice(0, rest.length-2); return r.fix(m, ...groups);`

For HTML marking, do the same but wrap the inserted space: fix returns e.g. `a+'.<span class="repair"> </span>'+b`. But then the resulting string contains HTML, and subsequent rules operate on it — regexes could match inside the span markup? E.g. comma rule `([a-z]),([A-Za-z])` — the span markup contains `class="repair"` — could `="` match? comma rule needs letter-comma-letter; markup has no commas. Sentence rule needs lowercase-period-uppercase: markup `class="repair">` — no period. Quote rule `([a-z])“` — no curly quote in markup. Dash rule `–([A-Za-z])` — no en dash in markup. Safe-ish, but fragile. Cleaner: build marked HTML in a separate pass using logs with final indices. 

Alternative simpler approach: compute `text` and logs via sequential replace (plain). Then for display, recompute marked HTML by applying rules to raw with HTML-wrapped insertions, in the same order — since insertions only add a space (plus span tags), and rules match on letters/punct adjacent... the span tags sit between the repaired chars, e.g. "levels.<span…> </span>Key" — subsequent rules see "…span> Key"? The dash rule `–([A-Za-z])`: after sentence repair we have "levels. <span> </span>Key" — no issue. But could a later rule match across the span boundary and insert another space inside? E.g. comma rule on "a,<span> </span>B"? That would only happen if raw had "a,B" — but then sentence rule wouldn't have fired... Actually raw "a.B" fires sentence rule; raw "a,B" fires comma rule. They're different chars, no overlap. Quote rule fires on `“` preceded by letter; dash on `–` followed by letter. None of these chars appear in my span markup. And the inserted space inside span: could a later rule match `([a-z])“` where the letter is inside markup? Markup letters: c,l,a,s,s,r,e,p,a,i,r — e.g. `class="repair"` contains `="` — quote rule needs `“` (curly) — markup uses straight quotes. OK safe. But to be extra safe, I'll do the marked-HTML pass on the plain repaired string? No — indices.

Simplest robust approach: single pass producing both. Apply rules sequentially to a plain string, logging matches with their offset in the *current* string. Then, to build marked HTML, I can reconstruct by applying rules to raw again but this time building output manually with a scanner:

Actually, easiest correct method: process rules one at a time on a plain string, but record for each log the match and the rule; then build the marked HTML by walking the final text? No.

Alternative: build marked HTML directly with a manual loop per rule using `re.exec` on the current plain string, constructing a new string with spans, and tracking logs. Since I construct the new string myself, I know exactly where insertions go:

```js
function applyRule(s, rule){
  const logs=[]; let out=''; let last=0; rule.re.lastIndex=0;
  let m;
  while((m=rule.re.exec(s))){
    const ins = rule.insert; // e.g. '. ' with space marked
    out += s.slice(last, m.index) + rule.pre(m) + '<span class="repair">'+rule.spaceChar+'</span>' + rule.post(m);
    logs.push({rule:rule.key, match:m[0], before:s.slice(Math.max(0,m.index-20), m.index), after:s.slice(m.index+m[0].length, m.index+m[0].length+20)});
    last = m.index + m[0].length;
    rule.re.lastIndex = m.index + m[0].length; // avoid infinite loop on zero-length; matches are non-empty
  }
  out += s.slice(last);
  return {out, logs};
}
```

Hmm but the replacement changes length; since I rebuild from the original s each rule and set lastIndex manually, it's fine. But wait — the replacement text differs in length from the match (adds one space + span tags). Since I'm building `out` from slices of the original `s` and only inserting at match boundaries, and I set `re.lastIndex = m.index + m[0].length` to continue scanning the original s — correct.

But there's subtlety: rule fix like sentence: match "s.K" (3 chars) replaced by "s. K" — in marked version: pre = m[0].slice(0,?) ... Let me define per rule: given match m with groups, the replacement is groups joined with the inserted space at a known position. Simpler: define replacement as function returning array of segments where one segment is the marked space:

- sentence: match = a + '.' + b → segments: [a+'.', SPACE, b]
- comma: [a+',', SPACE, b]
- quote: [a, SPACE, '“']  (space before the quote)
- dash: ['–', SPACE, b]

So each rule: `parts(m)` returns array of strings, one of which is the inserted space (mark with index). I'll define:

```js
const RULES=[
 {key:'sentence', label:'sentence join (full stop)', re:/([a-z])\.([A-Z])/g, parts:m=>[m[1]+'.', ' ', m[2]]},
 {key:'comma', label:'comma join', re:/([a-z]),([A-Za-z])/g, parts:m=>[m[1]+',', ' ', m[2]]},
 {key:'quote', label:'quote join', re:/([a-z])“/g, parts:m=>[m[1], ' ', '“']},
 {key:'dash', label:'dash join', re:/–([A-Za-z])/g, parts:m=>['–', ' ', m[1]]},
];
```

Then applyRule builds out with `<span class="repair"> </span>` for the ' ' part. And plain text = parts joined. I'll run applyRule twice? No — run once producing marked HTML, and derive plain text by stripping tags? Or run the plain version for `text` and marked version for display. Since both apply the same rules to the same raw in the same order, results are consistent. I'll write one function that returns {text, html, logs} by building both simultaneously: out_text += parts.join(''), out_html += parts with ' ' wrapped. 

```js
function applyRule(s, rule, logs){
  let outT='', outH='', last=0;
  rule.re.lastIndex=0; let m;
  while((m=rule.re.exec(s))!==null){
    const parts=rule.parts(m);
    outT += s.slice(last,m.index) + parts.join('');
    outH += esc(s.slice(last,m.index)) + parts.map(p=>p===' '?'<span class="repair"> </span>':esc(p)).join('');
    logs.push({rule:rule.key,label:rule.label,match:m[0],before:s.slice(Math.max(0,m.index-20),m.index),after:s.slice(m.index+m[0].length,m.index+m[0].length+20)});
    last=m.index+m[0].length;
    rule.re.lastIndex=last;
    if(m[0].length===0) rule.re.lastIndex++;
  }
  outT+=s.slice(last); outH+=esc(s.slice(last));
  return {text:outT, html:outH};
}
```

Wait — issue: after inserting a space, could the same rule match again overlapping? E.g. "a.B.C" — regex `([a-z])\.([A-Z])` matches "a.B" at 0, lastIndex=3, then continues from index 3: ".C" — needs [a-z] before '.', at index 2 is 'B'... exec from lastIndex 3: string "a.B.C", from index 3: ".C" no match (needs lowercase before period). Hmm "B.C" would need to start at index 2 but lastIndex=3 skips it. With global regex and replace, "a.B.C" → replace scans: match at 0 ("a.B"), continues from 3, no more. So "a.B.C" → "a. B.C"? Actually replace with /g: after match at 0-3, lastIndex=3, remaining ".C" no match. Result "a. B.C". My manual loop replicates that. Fine — consistent with the spec's replace semantics.

But careful: my manual loop sets `rule.re.lastIndex = last` where last = m.index + m[0].length — same as replace semantics. Good.

One more subtlety: the spec says apply rules in order to text_raw producing text. My sequential application does that. But note the quote rule inserts space *before* the quote: "crises“increase" → "crises “increase". parts: [m[1], ' ', '“'] — yes.

Dash rule: "challenges –to" — the match is "–t" (dash + letter), parts ['–',' ', 't'] → "– t". The space before the dash in original remains. Good.

Escaping: esc() for HTML display of text (escape &, <, >). The text may contain quotes etc. — fine.

Also `text_raw`: text after number and full stop, trimmed, whitespace runs collapsed to one space. Note: collapsing whitespace would turn U+00A0 into regular space? "runs of whitespace collapsed to one space" — \s in JS regex matches U+00A0? Yes, \s matches \u00a0 in JavaScript. Hmm, but the character count includes non-breaking space counted over paragraph texts — if text_raw collapses \s (including nbsp) to a space, then nbsp count would be 0. The plan says count non-breaking space over "all paragraph texts" and the data has "2 non-breaking spaces inside headings" — inside headings, not paragraphs! So paragraph texts may have 0 nbsp. But to be safe, collapse only regular whitespace `[ \t\n\r\f\v]+` (not \s) so nbsp survives in text_raw? The plan says "runs of whitespace collapsed to one space". If I use /\s+/g, nbsp becomes space and the nbsp count in paragraphs would be 0 — but the character table should still show the row (count 0? or count from headings?). The plan: "Characters. Counted over all paragraph texts". And the example says 2 nbsp inside headings. So counting over paragraph texts gives nbsp count possibly 0. Hmm, but then the table row "non-breaking space | 0 | …" — example would be empty. Maybe count over all texts (paragraphs + headings)? The plan explicitly says paragraph texts. But the found data says 2 nbsp in headings. To make the table useful, I'll count over paragraph texts AND heading texts, and label the table "Counted over paragraph and heading texts". Hmm — deviating from plan. Let me re-read: "**Characters.** Counted over all paragraph texts: en dash (U+2013), double quotes (U+201C, U+201D), right single quote (U+2019), non-breaking hyphen (U+2011), non-breaking space (U+00A0); `text` keeps them as published."

I'll count over paragraph texts as specified, but also include headings in the count so the nbsp row isn't empty... Risky to deviate. Actually the "What I found" says "2 non-breaking spaces inside headings" — so if I count only paragraphs, nbsp = 0, and the example column would have nothing. The plan's tab 03 says "one row each for the en dash, the double quotes, the right single quote, the non-breaking hyphen and the non-breaking space". I'll count over all extracted texts (paragraphs and headings) and say so in the "How this is computed" line: "counted over every paragraph and heading text". That's honest and matches the found data. Actually, let me count over paragraph texts primarily but the hint line can say "paragraph and heading texts". I'll do: counts over paragraphs + headings combined, labeled clearly. Hmm, but "How this is computed" honesty matters more than exact adherence. I'll count over all block texts (paragraphs, headings, title) — no wait, keep it to paragraphs + headings. Fine.

For whitespace collapse in text_raw: use `/[ \t\n\r\f\v\u00a0]+/g`? If I collapse nbsp to space, nbsp count = 0 everywhere. The found data says nbsp exists in headings — headings aren't collapsed (only paragraph text_raw is processed). Heading text I'll keep raw (trimmed). So nbsp survives in headings. For paragraphs, if any nbsp existed, collapsing with \s would remove it. The found data says nbsp only in headings, so either way paragraph count is 0. I'll collapse with `/\s+/g` per plan ("runs of whitespace"), and count characters over paragraph texts (post-collapse) + heading texts (raw trimmed). The nbsp row will show count from headings (2). Example: show the heading text snippet containing it. Good.

Hmm wait, but "text keeps them as published" — for paragraphs, if nbsp were present it'd be collapsed... The found data says none in paragraphs, so no conflict. I'll note in code comment. Actually, to be safe and honest, I'll collapse only ASCII whitespace plus newlines: `/[^\S\u00a0]+/g` — this collapses all whitespace EXCEPT nbsp, preserving nbsp as published. That satisfies "keeps them as published" better. "runs of whitespace collapsed to one space" — nbsp is arguably not "whitespace" to collapse for typography. I'll use `/[^\S\u00a0]+/g → ' '`. And count nbsp over paragraph texts then — would be 0 per found data, plus headings 2. I'll count over paragraphs + headings. Decision made.

First words: "first six whitespace-separated words of `text`" — split on /\s+/ (nbsp counts as whitespace for splitting? If nbsp preserved, splitting on \s+ splits on nbsp too since \s includes \u00a0). Fine.

Normalization for comparison: curly quotes → straight, en dash and nb-hyphen → '-', nbsp → ' '. Apply to both found and reference words.

Now the reference: `WORKSHOP_DATA.html_doc` shape: `{title, symbol, doc_url, source, html, reference: {...}}`. Wait — the preview shows `html_doc` as an array with one object? The sample shows `"html_doc": [ { "html": ... } ]` — hmm, the sample JSON shows html_doc as an array containing one object with only `html`. But the description says `WORKSHOP_DATA.html_doc`: `{title, symbol, doc_url, source, html, reference: {...}}`. The sample is truncated/omitted fields. The description at top says: "`WORKSHOP_DATA.html_doc`: one UN document as OHCHR publishes it in HTML — `{title, symbol, doc_url, source, html, reference: {...}}`". I'll code defensively: `const D = Array.isArray(WORKSHOP_DATA.html_doc) ? WORKSHOP_DATA.html_doc[0] : WORKSHOP_DATA.html_doc;` and handle missing fields. Similarly reference may be missing.

Also `built` — footer needs `source`, `built`. The description mentions title, symbol, doc_url, source, html, reference — no `built` listed for html_doc. Footer: "`source`, `built`". I'll show `D.built` if present else omit or show source only. I'll write: source line, and built if present. Defensive: `D.built ? ' · built ' + D.built : ''`.

Short title for the rail card: derive from title — e.g. "General comment No. 27 (2025) on …" — I'll just show the title (maybe truncated) or a short version: take title up to first colon? The title is "General comment No. 27 (2025) on economic, social and cultural rights and the environmental dimension of sustainable development *". Short title: I'll use "General comment No. 27 (2025)" — derive via regex `/^(General comment No\. \d+[^:]*)/`? Simpler: show full title in the card, small. The rail card: symbol in monospace + short title. I'll compute short title as title split at " on " first part? Eh — I'll just show the title text, styled small; it wraps. Or derive: `title.replace(/\s*\*$/, '')` and truncate to ~80 chars with ellipsis. Fine.

Export JSON: array of records with fields: symbol, paragraph (number), section, part, text, text_raw, first_words_match, citation, doc_url, limitations. `paragraph` — its number (int? "its number" — I'll use the integer). `section` = nearest heading (text, maybe with label), `part` = nearest roman h2 (label + heading). limitations: "no footnotes in this HTML version; the document has n".

Export Markdown: front matter between --- lines: title, symbol, adopted, source_url, extracted (today's date), paragraphs_found, paragraphs_expected, footnotes (the same sentence — "0 of 141: this HTML version has no footnotes"? "the same sentence" refers to the footnotes tile sentence: "this HTML version has none; see tab 03"? I'll use: `footnotes: "0 of 141 — this HTML version has no footnotes"`). Then headings as ## and ### lines in document order and each paragraph as its number in bold then text. So markdown body: iterate document order; h2 (non-title) → `## label. heading` (or just heading text); h3 → `### ...`; paragraph → `**n.** text`. Title h2 → maybe `# title`? Plan says "the headings as ## and ### lines" — the title is the first h2; I'll render title as `# title` (it's the document title, in front matter too). Hmm, "then the headings as `##` and `###` lines in document order and each paragraph as its number in bold, then its text". I'll render: title h2 as `#`, other h2 as `##`, h3 as `###`. Reasonable.

File names: symbol with slashes → hyphens: "E/C.12/GC/27" → "E-C.12-GC-27.json" / ".md". Blob URL, UTF-8, download attribute.

Export round trip check: build JSON string, JSON.parse it, compare length to paragraph count. Run on load.

Copy citation: navigator.clipboard.writeText with fallback (execCommand). Show "Copied" for 2s. Clipboard API may fail in sandbox — fallback to a temporary textarea + execCommand('copy'). I'll try clipboard, catch, fallback.

Tabs: 4 buttons, role="tablist", each button role="tab" aria-selected, panels role="tabpanel" aria-labelledby, hidden attr. Arrow keys: Left/Right/Home/End move focus and activate (I'll activate on arrow — common pattern; or focus only then activate on Enter. I'll do roving tabindex with activation on arrow press for simplicity, plus click). "a hidden tab panel is not focusable" — hidden attribute handles that.

Left rail "n of m checks pass" links to tab 04 — clicking should switch to tab 04. I'll make it a button styled as link that activates tab 04.

Clicking a repair row on tab 03 "opens the paragraph on tab 02": switch to tab 02, expand that row, scroll to it. I'll implement: activate tab 02, expand row, scrollIntoView.

Check panel lines: each check one line: name — compared values — verdict word ("pass" green / "check failed" red with link / "source limit" red / "not run"). Link to rows concerned: for first-words fail, link "tab 02" (and maybe list para numbers). I'll include the para numbers in the line.

Header status: compute pass/fail counts. Checks array with status: 'pass' | 'fail' | 'limit' | 'notrun'. m = checks with status pass/fail (i.e., run and not limit)? "n of m checks pass" — m should be total runnable checks. If reference missing, checks needing it are 'notrun' — then m excludes them? I'll define m = checks that ran (pass+fail), n = passes. Header: if fails>0 → red dot "n checks failed" (n = fail count) else green dot "n of m checks pass". Plus "1 source limit" (the footnotes check) — if reference missing, footnotes check is notrun, so "0 source limits"? Plan says header shows "1 source limit" (the footnotes). I'll show source-limit count dynamically: `${limitCount} source limit${s}`. With reference present, footnotes check = limit → "1 source limit". Good.

Rail bar: thin bar under "n paragraphs of reference.paragraphs": width = min(n, ref)/ref * 100%, color green if equal else red.

Tab 01 tiles: 4 tiles in a grid (2x2 on narrow). Each: monospace label (FIG.01 etc.? plan says tiles with big serif numbers and "How this is computed" line each). Labels: "PARAGRAPHS FOUND", "FIRST WORDS MATCH", "FOOTNOTES", "SPACES REPAIRED". Big number + beside text. Colors: green when equal/pass, red for footnotes and differences.

Tile 1: big "n" beside "the document has m" — green when equal, red with difference ("+x"/"−x").
Tile 2: "n of m" first words match.
Tile 3: "0 of m" red, "this HTML version has none; see tab 03" (link to tab 03).
Tile 4: "n" spaces repaired or flagged, link to tab 03.

How-this-computed lines: e.g. "Counted by this page's code: every `<p>` in the HTML whose text starts with a number and a full stop." etc.

Tab 02 table: caption "n paragraphs found, m expected" + "TAB.02" monospace. Columns: No. (right-aligned), Section, First line, Check. First line: first 120 chars cut at word + "…". Check: "OK" (green) or "first words differ" (red).

Headings box: closed button "Headings found: n" aria-expanded; when open, list all headings in order: label + text (monospace label). Count n = h2 (non-title) + h3.

Expanded row detail: full text (marked HTML with repair spans), then a small comparison: "found: … / reference: …" six words each, then repairs list for this paragraph ("sentence join: '…levels. Key…'"), then Copy citation button.

Tab 03 blocks:
1. "Lost: footnotes" — serif title + count (reference.footnotes). Text as specified.
2. "Changed: spaces" — count per rule above the table; table Paragraph | Before | After | Rule. Before/After: 20 chars each side context — I'll show `before + '[' + match + ']' + after`? Plan: "the inserted space marked". I'll show Before as context with match highlighted? Simpler: Before column = `…${before}${match}${after}…` and After = same with space inserted at match: `…${before}${inserted}${after}…` where inserted = match with space. And mark the inserted space — in the After cell, wrap the inserted space in red. I'll construct: afterStr = before + matchWithSpace + after, and in HTML wrap the space. Let me store in log: before, match, after, and rule label. Render Before: `…before` + match + `after…` (plain, maybe match in bold). After: before + match-with-space + after, with the inserted space in `<span class="ins"> </span>` (red box). Clicking row → open paragraph on tab 02.
   Count per rule above table: "sentence join: n · comma join: n · quote join: n · dash join: n" as small lines or one line. Plan: "the count per rule above it". I'll put a line above the table: "sentence join n · comma join n · quote join n · dash join n".
   Then the note about Giventhe etc.
3. "Changed: characters" — table Character | Count | Example. Rows: en dash –, double quotes “ ”, right single quote ’, non-breaking hyphen ‑, non-breaking space (nbsp). Example: first occurrence context (e.g. word containing it) from texts. Hint: "on a keyboard: a hyphen and straight quotes". Then the note about searching.

Character counting: over paragraph texts (text, post-repair — repairs don't affect these chars) and heading texts. I'll count over `text` of paragraphs + heading texts + title? Just paragraphs + headings. Example: find first context: search in the source string for the char, take ~12 chars each side. For nbsp, show "·" marker? I'll show the example with the char visible; for nbsp show `word·word` using a visible marker? Better: show example text with the char replaced by a visible representation in the Example column? Plan says "Example" — I'll show surrounding text with the character itself; for nbsp I'll render it as `⍽`? Hmm, keep simple: example = snippet with the char, and for nbsp use "·" substitution in display with a note. Actually simplest: example snippet where nbsp shown as "·" (middle dot) — but that changes the char... The hint line explains. I'll show snippet with the actual char but for nbsp wrap in span with visible background? I'll just show the snippet; monospace font renders nbsp as blank — confusing. I'll display nbsp as `␣`? Let me use: for the nbsp row, example shows the two words joined by a highlighted "·" and the hint says the document uses U+00A0. I'll implement: example text with the target char replaced by `<span class="char-mark">·</span>` for nbsp only, and for others show the char itself highlighted. Actually uniform: highlight the char itself in each example with a span (red underline?) — for nbsp, replace with '·' in the display copy only. Fine.

Tab 04: check panel open — every check one line. Then Export heading + two buttons. Then closed "Elements found (n)" button with table Tag | Classified as | Text (first 80 chars). Elements table: every block element in order: tag (lowercase), class (cover/container/title/heading/paragraph/committee), text first 80 chars.

"At most seven things to click" per view: tab 04 has 4 tabs + 2 export buttons + 1 elements heading = 7. Tab 02: 4 tabs + 1 headings box = 5 (+rows). Tab 03: 4 tabs (+ rows in spaces table — rows don't count per spec "not counting table rows"). OK.

Footer: source, built, "Done by this page's code; no model was called and nothing left the browser." Plus Credits line for the three sources (Turing Way CC BY 4.0, UK Analysis Function OGL 3.0, DAG Library). The instruction: "If you use code or wording from a 'Reference shelf excerpts' page that has an open licence... add a small Credits line". These are sources consulted, not code. The plan lists them under "Sources consulted". I'll add a small credits line naming them with licences — harmless and appropriate.

Now, code size: keep under 1500 lines. Let's write it.

Data access:

```js
const RAW = window.WORKSHOP_DATA && window.WORKSHOP_DATA.html_doc;
const D = Array.isArray(RAW) ? RAW[0] : RAW;
const html = D && D.html ? D.html : '';
const REF = (D && D.reference) || null;
const SYMBOL = D && D.symbol ? D.symbol : '(no symbol)';
const TITLE = D && D.title ? D.title : '(untitled)';
const DOC_URL = D && D.doc_url ? D.doc_url : '';
const SOURCE = D && D.source ? D.source : '';
```

Parse:

```js
const doc = new DOMParser().parseFromString(html, 'text/html');
const body = doc.body;
```

Block elements in order: `body.querySelectorAll('table, div, p, h2, h3')` — but nested: div contains p/h2/h3; querySelectorAll returns document order including nested. The table contains p's. So:

```js
const blocks = Array.from(body.querySelectorAll('table, div, p, h2, h3'));
const firstTable = body.querySelector('table');
```

Classify each block:
```js
function isInTable(el){ return firstTable && (el===firstTable || firstTable.contains(el)); }
```

For each block:
- if isInTable → class 'cover'
- tag 'div' → 'container'
- tag 'p': text = el.textContent; match `/^(\d{1,3})\.\s*(.*)$/s` → paragraph {num: parseInt, raw: m[2]}; else 'committee' (or 'other text')
- tag 'h2': if first h2 encountered → 'title'; else 'heading'
- tag 'h3' → 'heading'

Heading split: `/^([IVX]+|[A-Z])\.\s*(.+)$/s` on trimmed text → {label, heading} else {label:null, heading:text}.

Wait: "I.Introduction" — regex `^([IVX]+|[A-Z])\.\s*(.+)$` — "I.Introduction": [IVX]+ matches "I", then ".", then "Introduction". Good. "D. Obligation": [A-Z] matches "D", ".", \s* eats space, "Obligation". Good. But careful: a heading like "Right to work (art. 6)" (h3, plain) — no match → label null. But what about h3 lettered like "A. Something"? matches with [A-Z]. Good. Edge: "IV. ..." — [IVX]+ greedy matches "IV". Good. Potential false positive: heading "A.1..."? Not in data.

Hmm, one issue: `[IVX]+` could match a word like "IX" in "IX.something" — fine.

Also the title h2 ends with " *" — title text kept as-is; I'll strip trailing " *" for display? Keep as published; maybe trim. I'll display title with the asterisk (as published) — plan says title as h2 ending in " *". Keep it.

Paragraph processing:
```js
text_raw = m[2].replace(/[^\S\u00a0]+/g,' ').trim();
```
Wait order: trim then collapse, or collapse then trim — same result. But careful: `\s` in the paragraph regex `\s*` after the number — "1.A clean" → m[2]="A clean...". Good.

Hmm — the regex `/^(\d{1,3})\.\s*(.*)$/s` on textContent: textContent of `<p>1.A clean…</p>` is "1.A clean…". Good. But what if the `<p>` contains nested elements? textContent handles.

Also: could a committee `<p>` accidentally match? Committee line "Committee on Economic, Social and Cultural Rights" — no leading digits. Cover p's are inside table → cover. Good.

Section tracking: iterate blocks in order; maintain `currentHeadings` stack? For each paragraph, section = nearest heading above (last heading seen), part = nearest roman h2 (last h2 whose label matches /^[IVX]+$/). Path: maintain array of headings since last roman h2; on roman h2, reset path to [that heading]; on other heading, push. Paragraph's path = current path. Section display: last heading's full text (label + '. ' + heading if label else heading). Part: roman heading's label + '. ' + heading.

Wait — "part (the nearest heading and the roman-numbered section above it)" for export: `section` = nearest heading, `part` = roman-numbered section above. So export record: section = nearest heading text (e.g. "Right to work (art. 6)"), part = e.g. "IV. ...". I'll store section as the display string of nearest heading (with label if present: "D. Obligation to respect"), part as roman h2 display ("IV. ..."). 

First words:
```js
function norm(s){ return s.replace(/[\u2018\u2019]/g,"'").replace(/[\u201C\u201D]/g,'"').replace(/[\u2013\u2011]/g,'-').replace(/\u00A0/g,' '); }
function firstSix(t){ return norm(t).split(/\s+/).filter(Boolean).slice(0,6).join(' '); }
```
Compare firstSix(text) with norm(REF.first_words[String(num)]) — reference first_words are already clean presumably, but normalize anyway. first_words_match boolean. If REF missing or key missing → null → check "not run"; display "no reference".

Repairs: as designed. logs per paragraph: para num, rule key/label, before, match, after.

Characters: count over paragraph `text` + heading texts (raw trimmed) — I'll count over `text` (repaired) for paragraphs and heading text for headings. Actually simpler: count over text_raw? Repairs only insert spaces; the special chars unaffected. Use `text`. Also include title text? Plan says paragraph texts; I'll do paragraphs + headings and label it. Let me define `allTexts = paragraphs.map(p=>p.text).concat(headings.map(h=>h.text))`. Counts:
- en dash \u2013
- double quotes \u201C and \u201D (count both, one row "double quotes “ ”")
- right single quote \u2019
- non-breaking hyphen \u2011
- non-breaking space \u00A0

Example: for each char, find first index in any text, snippet ±14 chars, with the char highlighted.

Checks:

```js
checks = [];
// 1 paragraph count
if(REF){ found vs REF.paragraphs → pass/fail } else notrun
// 2 numbering: nums sorted equals 1..n? Actually "Exactly 1 to n in order" — check nums[i] === i+1. gaps/duplicates listed.
pass if all in order 1..n (n = found count). If REF present maybe compare to REF.paragraphs too — the count check covers that. Numbering check: sequence is 1..foundN consecutive. List gaps/duplicates if any.
// 3 first words: mismatches list; needs REF. pass if 0 mismatches (and REF present). fail with "para. n: found … / reference …" — maybe cap list at, say, all (6 expected). Link to tab 02.
// 4 footnotes: 0 vs REF.footnotes → 'limit' (source limit). If no REF → notrun.
// 5 repairs: count spaces restored, per rule → pass (informational): "n spaces restored in n paragraphs; every one listed on tab 03; text_raw unchanged". status pass.
// 6 headings: count h2/h3, glued labels separated (headings where label was glued, i.e. original had no space after label? "how many glued labels were separated" — heading text matched the split regex with \s* — glued means no space: check original text matches /^([IVX]+|[A-Z])\./ without space. I'll count headings where label matched and the char after '.' was not a space.) → pass.
// 7 nothing lost: classified counts sum to blocks.length; unclassified list → pass/fail.
// 8 export round trip: JSON.parse(exportJSON).length === paragraphs.length → pass. (Build export JSON on load.)
```

If no paragraphs at all (html yields no p): tab 01 says "no paragraphs found in this HTML" and exports disabled.

Status counts: pass = checks.filter(c=>c.status==='pass').length; fail = ...'fail'; limit = 'limit'; m = pass+fail (run checks). Header: fail>0 ? red "n checks failed" : green `${pass} of ${m} checks pass`; plus `${limit} source limit` (red text) if limit>0.

Hmm "n of m checks pass" where m includes limit? Plan: "a green dot 'n of m checks pass' or a red dot 'n checks failed', then '1 source limit'". I'll set m = pass+fail (excluding limit and notrun). With all passing: "8 of 8"? There are 8 checks, one is limit → 7 of 7 pass + "1 source limit". Good.

Rail: "n of m checks pass" link → tab 04. If fails: "n checks failed" red.

Now rendering. I'll build DOM via template strings + innerHTML for static parts, and create rows with createElement or innerHTML strings. Use esc() everywhere for data text.

Layout CSS:

```css
:root{ --paper:#f4f0e8; --ink:#1d1b18; --rule:#d9d2c3; --red:#9b2335; --green:#1e6b3a; }
body{ background:var(--paper); color:var(--ink); font:16px/1.55 -apple-system,'Segoe UI',Roboto,Helvetica,Arial,sans-serif; margin:0; }
header{ padding:20px 28px 14px; border-bottom:1px solid var(--rule); }
...
.layout{ display:flex; gap:0; align-items:flex-start; }
aside{ width:250px; flex:0 0 250px; border-right:1px solid var(--rule); padding:18px 20px; position:sticky; top:0; }
main{ flex:1; min-width:0; padding:18px 28px 40px; }
```

Header content:
```html
<div class="kicker">UN DOCUMENT · HTML</div>
<h1 class="serif">TITLE</h1>
<div class="meta"><a href=doc_url target=_blank>SYMBOL</a> · adopted DATE · SOURCE <span class="status">…</span></div>
```
Status at right: use flex with margin-left:auto.

Tabs:
```html
<div class="tabs" role="tablist" aria-label="Views">
  <button role="tab" id="tabbtn-1" aria-controls="panel-1" aria-selected="true">01 RESULT</button>
  ...
</div>
```
Tab names: "01 RESULT", "02 PARAGRAPHS", "03 LOST & CHANGED", "04 CHECKS & EXPORT". Monospace uppercase letter-spaced. Active: red color + red underline (border-bottom 2px red).

Panels: `<section role="tabpanel" id="panel-1" aria-labelledby="tabbtn-1">`.

Tab switching JS:
```js
const tabs=[...document.querySelectorAll('[role="tab"]')];
function selectTab(i){ tabs.forEach((t,j)=>{ const on=i===j; t.setAttribute('aria-selected',on); t.tabIndex=on?0:-1; document.getElementById(t.getAttribute('aria-controls')).hidden=!on; }); }
tabs.forEach((t,i)=>{ t.addEventListener('click',()=>selectTab(i)); t.addEventListener('keydown',e=>{ let n=null; if(e.key==='ArrowRight')n=(i+1)%tabs.length; if(e.key==='ArrowLeft')n=(i-1+tabs.length)%tabs.length; if(e.key==='Home')n=0; if(e.key==='End')n=tabs.length-1; if(n!==null){e.preventDefault(); tabs[n].focus(); selectTab(n);} }); });
```

Rail:
```html
<aside>
 <div class="rail-h">DOCUMENT</div>
 <div class="doc-card"><div class="mono">E/C.12/GC/27</div><div class="doc-title">General comment No. 27 (2025) …</div></div>
 <div class="big"><span id="rail-n">90</span> <span class="of">paragraphs of 90</span></div>
 <div class="bar"><div class="bar-fill"></div></div>
 <div class="big red">0 <span class="of">footnotes of 141</span></div>
 <div class="note red">not in this HTML</div>
 <button class="linklike" id="rail-checks">7 of 7 checks pass</button>
</aside>
```

Plan: two big serif numbers: "n paragraphs of reference.paragraphs" with thin bar; "0 footnotes of reference.footnotes" in red, "not in this HTML". Then "n of m checks pass" linking to tab 04.

Tab 01 tiles:
```html
<div class="tiles">
 <div class="tile"><div class="t-label">PARAGRAPHS FOUND</div><div class="t-num serif">90</div><div class="t-beside">the document has 90</div><div class="how">How this is computed: …</div></div>
 ...
</div>
```
Tile 1: big n, beside "the document has m" — green if equal else red with diff. Tile 2: "n of m" big? Big number "n of m"? I'll make big "n" with beside "of m first words match". Tile 3: big "0" red, beside "of m footnotes — this HTML version has none; see tab 03" (link). Tile 4: big "n" beside "spaces repaired or flagged — see tab 03" (link).

How lines:
- T1: "Every `<p>` in the HTML whose text begins with a number and a full stop, counted by this page's code."
- T2: "First six words of each paragraph, compared with the document's reference after normalising quotes, dashes and non-breaking characters."
- T3: "The HTML contains no footnote elements; the reference counts the footnotes of the PDF and Word versions."
- T4: "Spaces inserted by the four repair rules on tab 03; the text as found is kept in `text_raw`."

Tab 02:
```html
<button class="fold" aria-expanded="false" id="headings-fold">Headings found: 30</button>
<div id="headings-list" hidden>…list…</div>
<table>
 <caption><span class="tabno">TAB.02</span> 90 paragraphs found, 90 expected</caption>
 <thead><tr><th scope="col" class="num">No.</th><th scope="col">Section</th><th scope="col">First line</th><th scope="col">Check</th></tr></thead>
 <tbody> rows… </tbody>
</table>
```

Row:
```html
<tr class="prow" data-para="12">
 <td class="num"><button class="pbtn" aria-expanded="false" aria-controls="detail-12">12</button></td>
 <td class="sec">Right to work (art. 6)</td>
 <td class="first">…</td>
 <td class="chk ok">OK</td>
</tr>
<tr class="detail" id="detail-12" hidden><td colspan="4">…</td></tr>
```

Row click: clicking anywhere on prow toggles. I'll add listener on tbody: if e.target.closest('.prow') and not on detail → toggle. Button handles keyboard.

Detail content:
```html
<div class="path mono">IV. … › D. … › Right to work (art. 6)</div>
<p class="full">marked html</p>
<div class="fw"><span class="mono">FIRST WORDS</span> found: "…" · reference: "…" </div>
<div class="repairs">…list…</div>
<button class="copy" data-cite="E/C.12/GC/27, para. 12">Copy citation</button>
```

Copy: on click, copy, set text "Copied", revert after 2000ms.

Tab 03:
Block 1:
```html
<section class="block">
 <h2 class="serif">Lost: footnotes <span class="count">141</span></h2>
 <p>The document has 141 footnotes. This HTML has 0: no footnote text, no footnote marks, and the note the title's asterisk points to is missing. To cite a footnote, use the PDF or Word version.</p>
</section>
```
Block 2:
```html
<h2 class="serif">Changed: spaces <span class="count">35</span></h2>
<div class="rule-counts mono">sentence join 23 · comma join 8 · quote join 2 · dash join 2</div>
<table> caption TAB.03 "35 missing spaces restored by rule" ; cols Paragraph | Before | After | Rule
 rows clickable → open para on tab 02
</table>
<p class="note">Rules restore a space only where the characters prove it was there. Word pairs such as “Giventhe” are not touched; the first-words check catches them only in a paragraph's first six words.</p>
```
Wait — "Giventhe" — I shouldn't hard-code; the plan itself uses it as example wording. It says: 'Word pairs such as 'Giventhe' are not touched'. Since the plan explicitly gives this wording, I can use it, but better to derive from data? The plan's sentence is given; but data may differ. Safer: generic wording: "Word pairs a rule cannot see (two words glued with no punctuation) are not touched; the first-words check catches them only when they fall in a paragraph's first six words." That avoids inventing. But the plan literally says include that sentence with 'Giventhe'. Hmm — "Never invent records, statistics, or quotes" — 'Giventhe' is from the user's own plan describing their file. I could detect glued word pairs? Hard. I'll use the plan's sentence but make it data-driven-ish: I can search for a known pattern? Simplest: use generic wording without the specific token: "Word pairs no rule can see (for example two words glued together with no punctuation between them) are not touched; …". That's faithful and safe.

Block 3:
```html
<h2 class="serif">Changed: characters</h2>
<table> Character | Count | Example
 rows: en dash –, double quotes “ ”, right single quote ’, non-breaking hyphen ‑, non-breaking space (U+00A0)
</table>
<div class="mono hint">on a keyboard: a hyphen and straight quotes</div>
<p class="note">Kept exactly as published, in the table and in every export. A search for "business-related" typed with the hyphen key will not find "business‑related": normalise the text before searching it.</p>
```
Again "business-related" is from the plan; I'll make it generic: "A search typed with the hyphen key will not find a non-breaking hyphen, and straight quotes will not find curly ones: normalise the text before searching it." Safer.

Tab 04:
```html
<h2 class="serif">Checks</h2>
<div class="checks"> one line per check </div>
<h2 class="serif">Export</h2>
<button id="dl-json">Download JSON</button> <button id="dl-md">Download Markdown</button>
<button class="fold" aria-expanded="false">Elements found (n)</button>
<div hidden><table> Tag | Classified as | Text (first 80 characters) </table></div>
```

Check line format: `<div class="check"><span class="cname">Paragraph count</span> found 90 · reference 90 <span class="pass">pass</span></div>`. Fail: red "check failed" + link "see tab 02" + details. Limit: red "source limit" + note.

Export JSON record:
```js
{ symbol, paragraph: num, section, part, text, text_raw, first_words_match, citation, doc_url, limitations }
```
limitations: `no footnotes in this HTML version; the document has ${REF?REF.footnotes:'?'} footnotes` — if no REF: "no footnotes in this HTML version". 

Markdown:
```
---
title: ...
symbol: ...
adopted: ...
source_url: ...
extracted: 2026-… (today)
paragraphs_found: n
paragraphs_expected: m
footnotes: "0 of 141 — this HTML version has no footnotes"
---
# title
## I. Introduction
**1.** text
...
```
Headings in document order: I need to interleave headings and paragraphs in document order — I have blocks order; I'll build an ordered list of items (heading or paragraph) during classification. Title h2 → `#`. Other h2 → `##`, h3 → `###`. Heading line: label ? `${label}. ${heading}` : heading. Paragraph: `**${num}.** ${text}`.

Wait plan: "each paragraph as its number in bold, then its text" — `**12.** text`. Good.

Download:
```js
function download(name, content, type){ const blob=new Blob([content],{type}); const url=URL.createObjectURL(blob); const a=document.createElement('a'); a.href=url; a.download=name; document.body.appendChild(a); a.click(); a.remove(); setTimeout(()=>URL.revokeObjectURL(url),1000); }
```
Filename: symbol.replace(/\//g,'-') + '.json'.

Export round trip check: `JSON.parse(jsonStr).length === paragraphs.length`.

Edge: no reference → tiles say "no reference in this file"; checks needing REF → "not run". No paragraphs → tab 01 message + disable export buttons (disabled attr + title).

Now the "Elements found (n)" table: Tag | Classified as | Text (first 80 chars). For each block: tag = el.tagName.toLowerCase(), class = classification, text = el.textContent collapsed, slice 0..80 + '…' if longer.

Classification classes: cover, container, title, heading, paragraph, text (committee/other p). "Nothing lost" check: every block classified exactly once — since my classifier assigns exactly one class to each, sum always equals; but I'll still compute and if any 'unclassified' (shouldn't happen) list. To make the check meaningful, I'll classify with a function that returns null for unknown tags — but I only select known tags. I'll include all block-ish elements: querySelectorAll('table,div,p,h2,h3,ul,ol,li,blockquote,pre')? The doc may have only table/div/p/h2/h3. I'll query a broader set and classify unknown as 'unclassified' → check fails if any. Let me query `'table, div, p, h1, h2, h3, h4, ul, ol, li, blockquote, pre, section, article'` — anything not matching known patterns → 'unclassified'. Good, makes check real.

Hmm wait: div is container; but what if there are nested divs? Fine, each is container.

Also note: the first table's descendant p's — querySelectorAll includes them; isInTable check handles.

One more: the paragraph regex on textContent — cover p's like "E/C.12/GC/27" don't match. "6 November 2025" — starts with digit! "6 November 2025" → `^(\d{1,3})\.` requires a full stop after digits — "6 November" has no dot after 6 → no match. Good. But it's inside table → cover anyway.

Committee line: the bold `<p>` "Committee on Economic, Social and Cultural Rights" → class 'text' (committee). 

Now heading glued labels: count headings where label matched AND the original text has no space after the label's dot: check `/^([IVX]+|[A-Z])\.[^\s]/`. I'll compute gluedCount.

Also "Headings found: n" on tab 02 — n = headings count (h2 non-title + h3). List them in order with label.

Section for paragraph rows: display nearest heading: label ? `${label}. ${heading}` : heading. Path for detail: join path items similarly with " › ".

Part: nearest roman h2 display.

Now let me also handle: paragraph numbers as int; citation uses the number as found (e.g. "12"). reference.first_words keys are strings.

Numbering check: nums in order should be 1..N where N = paragraphs found? "Exactly 1 to n in order; gaps and duplicates listed." I'll check nums[i] === i+1 for all i; if not, list the anomalies (expected i+1, found nums[i]). Also duplicates: if nums has duplicates. I'll compute: expected sequence 1..nums.length; mismatches listed (cap 10).

First words check details: for each para, if REF && REF.first_words && key exists: compare; mismatch list entries "para. n: found “…” / reference “…”". If REF missing → notrun. If key missing for a para → count as mismatch? I'll treat missing key as "no reference entry" — count separately, mark check fail? Plan: "Mismatches counted and listed". If reference lacks the key, I'll list as "para. n: no reference entry". Keep simple: mismatch if key missing or differs.

Now write the HTML. Also focus ring: `:focus-visible{ outline:2px solid var(--red); outline-offset:2px; }`.

Fonts: serif Georgia; mono ui-monospace etc.

Big numbers: 40–56px serif.

Let me now also handle the header status dot: `<span class="dot green"></span>` circle 8px.

Let me think about "How this is computed" line near every chart or number — tiles have them; rail numbers: add small mono hints? Rail: under big numbers maybe tiny hint. Keep minimal.

Table captions: serif, message + TAB.0x mono. E.g. `<caption><span class="tabno">TAB.02</span><span class="serif">90 paragraphs found, 90 expected</span></caption>`.

Numbers right-aligned: `.num, th.num { text-align:right; }`.

Repair mark CSS: `.repair{ box-shadow: inset 0 0 0 1px var(--red); }` thin red box around the space — a space with inset box shows a small red rectangle. Good: "marked in the expanded paragraph by a thin red box".

Inserted space in tab 03 After cell: `.ins{ box-shadow: inset 0 0 0 1px var(--red); }`.

Now sizes: keep code tidy. Let me draft the full file.

Also: "Every row that shows a document has its symbol, linked to doc_url" — header has symbol link; tab 02 rows: the citation includes symbol; maybe add symbol link in detail row. I'll add in detail: "symbol ↗" link. Good.

Footer: `source` · built · done-line. Credits line: "Sources consulted: The Turing Way, Documentation and metadata (CC BY 4.0) · UK Government Analysis Function, Quality assurance of code (Open Government Licence v3.0) · Dag Hammarskjöld Library, Ask DAG: citing a UN document."

Let me now write the code.

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Paragraphs out of a UN document — HTML</title>
<style>
...
</style>
</head>
<body>
<header>...</header>
<div class="layout">
 <aside id="rail">...</aside>
 <main>
  <div class="tabs" role="tablist">...</div>
  <section id="panel-1" role="tabpanel" aria-labelledby="tab-1">...</section>
  ...
 </main>
</div>
<footer>...</footer>
<script>
...
</script>
</body>
</html>
```

I'll render most content via JS into containers to keep HTML skeleton small.

Let me write the JS pipeline carefully.

```js
(function(){
"use strict";
const WD = window.WORKSHOP_DATA || {};
const raw = WD.html_doc;
const D = Array.isArray(raw) ? (raw[0]||{}) : (raw||{});
const html = typeof D.html === 'string' ? D.html : '';
const REF = (D && typeof D.reference === 'object' && D.reference) ? D.reference : null;
const SYMBOL = D.symbol || '(no symbol in this file)';
const TITLE = D.title || '(untitled document)';
const DOC_URL = D.doc_url || '';
const SOURCE = D.source || '';
const BUILT = D.built || '';

const esc = s => String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
const collapse = s => String(s).replace(/[^\S\u00A0]+/g,' ').trim();

let doc=null, body=null;
try { doc = new DOMParser().parseFromString(html, 'text/html'); body = doc.body; } catch(e){ body=null; }
```

If !body or !html → show "no HTML" message.

Blocks:

```js
const TAGS = 'table,div,p,h1,h2,h3,h4,h5,h6,ul,ol,li,blockquote,pre,section,article,header,footer,nav';
const blocks = body ? Array.from(body.querySelectorAll(TAGS)) : [];
const firstTable = body ? body.querySelector('table') : null;
```

Classify:

```js
const items = []; // ordered: {kind:'heading'|'paragraph', ...}
const elements = []; // every block: {tag, cls, text}
const paragraphs = [];
const headings = [];
let titleEl = null;
let curPath = [];   // headings since last roman h2
let curPart = '';
let curSection = '';

const PARA_RE = /^(\d{1,3})\.\s*([\s\S]*)$/;
const HEAD_RE = /^([IVX]+|[A-Z])\.\s*([\s\S]+)$/;

blocks.forEach(el=>{
  const tag = el.tagName.toLowerCase();
  const text = collapse(el.textContent);
  let cls, rec=null;
  const inTable = firstTable && (el===firstTable || firstTable.contains(el));
  if(inTable){ cls='cover'; }
  else if(tag==='div'||tag==='section'||tag==='article'){ cls='container'; }
  else if(tag==='p'){
    const m = text.match(PARA_RE);
    if(m){ cls='paragraph'; rec={num:parseInt(m[1],10), raw:m[2]}; }
    else { cls='text'; }
  }
  else if(tag==='h1'||tag==='h2'||tag==='h3'||tag==='h4'||tag==='h5'||tag==='h6'){
    if(!titleEl && (tag==='h2'||tag==='h1')){ cls='title'; titleEl=el; }
    else {
      cls='heading';
      const m = text.match(HEAD_RE);
      let label=null, head=text, glued=false;
      if(m){ label=m[1]; head=m[2]; glued = new RegExp('^'+label.replace(/[.*+?^${}()|[\]\\]/g,'\\$&')+'\\.[^\\s]').test(text); }
      rec={tag, label, heading:head, text, glued};
      headings.push(rec);
      const roman = label && /^[IVX]+$/.test(label);
      if(tag==='h2' && roman){ curPath=[rec]; curPart = label+'. '+head; }
      else if(tag==='h2' && label){ curPath=[rec]; curPart = label+'. '+head; } // hmm
      else { curPath.push(rec); }
      ...
    }
  }
  else { cls='unclassified'; }
  ...
});
```

Wait — part = nearest roman-numbered h2. What about lettered h2? The found data: 6 roman h2, 24 h3 (4 lettered, 20 plain). So h2 are all roman. But defensively: part = nearest h2 whose label is roman; if an h2 has a letter label, it's still a section divider? Plan: "part = the nearest roman-numbered `<h2>`". I'll set: on any h2 heading, if label is roman → curPart = display, curPath=[rec]; if h2 without roman label → curPart unchanged? Hmm, safer: on h2, reset curPath=[rec]; if roman label, also set curPart. On h3, push to curPath. Section = last heading in curPath (or last heading overall). Let me maintain `lastHeading` separately: every heading updates lastHeading=rec. Section = lastHeading display. Path = curPath (headings since last h2). Part = curPart (last roman h2 display, '' if none).

Display of heading: `disp = label ? label+'. '+heading : heading`.

Paragraph record:
```js
rec = {num, raw, text_raw: collapse(m[2]), section: lastHeading?disp(lastHeading):'', part: curPart, path: curPath.slice()};
```
Wait text_raw: m[2] already collapsed? I collapsed text first then matched — collapse removed newlines. m[2] from collapsed text is fine; then trim. Actually collapse already trims. But the regex `\s*` after `\.` — with collapsed text, "1.A clean" → m[2]="A clean…". Good. text_raw = m[2] (already collapsed+trimmed). But careful: collapse preserves nbsp; fine.

Hmm — one subtlety: collapse uses `[^\S\u00A0]+` which collapses \n etc. but not nbsp. Good.

Then repairs:

```js
const RULES=[
 {key:'sentence', label:'sentence join', re:/([a-z])\.([A-Z])/g, parts:m=>[m[1]+'.',' ',m[2]]},
 {key:'comma', label:'comma join', re:/([a-z]),([A-Za-z])/g, parts:m=>[m[1]+',',' ',m[2]]},
 {key:'quote', label:'quote join', re:/([a-z])\u201C/g, parts:m=>[m[1],' ','\u201C']},
 {key:'dash', label:'dash join', re:/\u2013([A-Za-z])/g, parts:m=>['\u2013',' ',m[1]]},
];
function repairAll(rawText){
  let text=rawText, htmlOut='', logs=[];
  for(const r of RULES){
    let outT='', outH='', last=0;
    r.re.lastIndex=0;
    let m;
    while((m=r.re.exec(text))!==null){
      const parts=r.parts(m);
      const before=text.slice(Math.max(0,m.index-20), m.index);
      const after=text.slice(m.index+m[0].length, m.index+m[0].length+20);
      logs.push({rule:r.key,label:r.label,match:m[0],before,after});
      outT += text.slice(last,m.index)+parts.join('');
      outH += esc(text.slice(last,m.index))+parts.map(p=>p===' '?'<span class="repair"> </span>':esc(p)).join('');
      last=m.index+m[0].length;
      r.re.lastIndex=last;
      if(m[0].length===0) r.re.lastIndex++;
    }
    outT+=text.slice(last); outH+=esc(text.slice(last));
    text=outT; htmlOut+=outH;
  }
  return {text, html:htmlOut, logs};
}
```

Wait bug: htmlOut accumulates across rules but `text` is reassigned each rule; outH built from current text — but I append outH to htmlOut each rule; however outH for rule 2 is built from text after rule 1 — correct, since repairs compound. But htmlOut for rule1 + rule2: rule2's outH includes esc of rule1's repaired text (plain, since text is plain) — yes text is always plain; htmlOut accumulates marked segments. But careful: rule2's outH escapes the whole current text including parts already... no — text is plain (outT), so htmlOut = marked rule1 output + marked rule2 output built from plain text. But rule2's outH includes the entire text again (from last=0), so htmlOut would double-count! Bug: I should not accumulate htmlOut across rules; instead build html only in the final pass, or track: after each rule, htmlOut should be rebuilt from the new text. Simplest: run the loop twice — once for text+logs (plain), once for html (marked), applying same rules to rawText. Since deterministic, same result. Or: build html incrementally by converting: after computing final text and logs... logs don't have final indices.

Cleaner: single pass but maintain both text and html in parallel per rule, where html is rebuilt each rule from the new text? That loses previous marks. 

Alternative: do it in one pass over rules where I keep `text` plain and also `segs` = array of {t, marked} segments... complex.

Easiest: two passes. Pass A: plain, collect logs. Pass B: marked HTML only (no logs). Both apply RULES in order to rawText. Deterministic → identical. Implement `applyRules(raw, wantHtml)` returning {text, html, logs} where in pass B logs ignored. Actually just one function with flag; call twice. Fine — cheap (90 paragraphs).

Actually simpler: one function that returns text and logs; and a second function `markHTML(raw)` that applies rules producing html with spans (same logic, building only outH). I'll write generic:

```js
function runRules(raw, withHtml){
  let text=raw; const logs=[]; let html='';
  for(const r of RULES){
    let outT='', outH='', last=0; r.re.lastIndex=0; let m;
    while((m=r.re.exec(text))!==null){
      const parts=r.parts(m);
      logs.push({rule:r.key,label:r.label,match:m[0],before:text.slice(Math.max(0,m.index-20),m.index),after:text.slice(m.index+m[0].length,m.index+m[0].length+20)});
      outT+=text.slice(last,m.index)+parts.join('');
      if(withHtml) outH+=esc(text.slice(last,m.index))+parts.map(p=>p===' '?'<span class="repair"> </span>':esc(p)).join('');
      last=m.index+m[0].length; r.re.lastIndex=last;
    }
    outT+=text.slice(last);
    if(withHtml){ outH+=esc(text.slice(last)); html=outH; }
    text=outT;
  }
  return {text, html, logs};
}
```

Wait — in pass with html, `html=outH` after each rule — outH is built from current text (which includes previous repairs as plain text) with new marks. After final rule, html = fully marked. But intermediate: after rule1, html=outH(rule1). After rule2, outH is built from text after rule1 — includes rule1's inserted spaces as plain ' ' (not marked!). Bug: rule2's outH escapes text.slice which contains rule1's inserted space unmarked.

Fix: maintain html incrementally alongside text: keep `html` as marked version of current text. When applying a rule to text, I need to apply the same transformation to html — but html has span tags whose positions shift. Ugh.

Better approach: build marked html in ONE pass over rules where I carry both text and html in sync by processing rule matches on text and mapping to html via segment list. Alternative much simpler: apply all rules in one combined pass? The rules are independent patterns; I could run a single combined regex pass on the raw text: `([a-z])\.([A-Z])|([a-z]),([A-Za-z])|([a-z])“|–([A-Za-z])` with alternation, replacing each match with marked insertion. But order matters per plan (sentence first, etc.) — with alternation, at each position the first alternative that matches wins; scanning left to right. Would results differ from sequential? Sequential: rule1 fixes all "a.B", then rule2 sees the modified text — could rule2 match something created by rule1? Rule1 inserts a space: "a. B" — rule2 needs letter-comma-letter; no comma introduced. Rule3 needs letter+“; rule1 doesn't create that. Rule4 needs –+letter; rule1 doesn't create. Conversely, could rule1's fix destroy a rule2 match? Rule2 match "a,B" — rule1 needs "a.B" — different. They don't overlap since each match consumes distinct punctuation (., comma, “, –). One overlap: "a.B" where... no. What about "x.–Y"? dash rule matches "–Y"; sentence rule needs [a-z].[A-Z] — "x.–Y" has "x." then "–" not [A-Z]. No overlap. So a single combined pass with alternation in the plan's priority order gives identical results to sequential application. 

Combined regex: `/([a-z])\.([A-Z])|([a-z]),([A-Za-z])|([a-z])“|–([A-Za-z])/g`. In callback, determine which alternative matched by checking groups. Replacement parts:
- alt1: [g1+'.', ' ', g2]
- alt2: [g3+',', ' ', g4]
- alt3: [g5, ' ', '“']
- alt4: ['–', ' ', g6]

Then one pass builds text and html simultaneously, with logs. 

But wait — is sequential vs combined truly identical? Consider "a.B,C": sequential rule1: "a. B,C" → rule2: "a. B, C". Combined: scan: at index0 alt1 matches "a.B" → replace, lastIndex=3; from index 3: ",C" — alt2 needs [a-z] before comma; at index 2 is 'B' but lastIndex=3 skips... combined regex exec from lastIndex=3: remaining ",C" no match at 3; but regex engine tries index 3,4... ",C" — alt2 `([a-z]),` needs lowercase before comma — position 3 is ','; no. So combined gives "a. B,C" — rule2 doesn't fire! Sequential gives "a. B, C". Difference! Because sequential rule2 runs on the whole string fresh, matching "B,C" at index 2.

Hmm. So combined single-pass differs from sequential in edge cases. Does such a case exist in data? "levels.Key" style — a sentence join immediately followed by comma join like "a.B,C" — possible? The found data: 23 sentence joins, 8 comma joins. Could overlap. To be exactly per plan (sequential), I need sequential application.

OK, do sequential properly with parallel text/html. Approach: maintain `text` (plain) and build html at the END from text + logs? Logs have before/match/after contexts from intermediate strings — not final indices.

Alternative: maintain segments. Represent current content as array of segments {t: string, marked: bool}. Applying a rule: scan the plain concatenation? Indices get messy.

Simplest robust: run sequential passes for text+logs (plain). Then, for html, run sequential passes again but on a "marked" string where I apply rules to the plain text and simultaneously produce html by re-running with a trick: since each rule's matches are known (from pass A logs per rule, in order), I can reconstruct: for each rule in order, take current plain text, and I know the matches (from logs of that rule) with their indices in that rule's input string. Build html by walking matches: outH += esc(text.slice(last, m.index)) + marked parts. And text = outT. The key: in pass A, for each rule, record matches with index in the input string of that rule. Then pass B replays: for rule i, input text_i (same as pass A), matches known → build html_i. So store per-rule match lists: `ruleMatches[i] = [{index, match, parts}]`. Then:

```js
function process(raw){
  let text=raw; const allLogs=[]; const ruleMatches=[];
  RULES.forEach((r,ri)=>{
    const ms=[]; r.re.lastIndex=0; let m;
    while((m=r.re.exec(text))!==null){
      ms.push({index:m.index, match:m[0], parts:r.parts(m)});
      allLogs.push({rule:r.key,label:r.label,match:m[0],before:text.slice(Math.max(0,m.index-20),m.index),after:text.slice(m.index+m[0].length,m.index+m[0].length+20)});
      r.re.lastIndex=m.index+m[0].length;
    }
    ruleMatches.push(ms);
    text = text.replace(r.re, (...a)=>{ const g=a.slice(1,-2); return r.partsFromGroups? ... });
  });
}
```

Hmm, replace with function needs parts from groups: parts functions take m (match array). I can do `text.replace(r.re, (...args)=>{ const m=args.slice(0,-2); m.index=args[args.length-2]; ... return r.parts(m).join(''); })`. Wait args = [match, g1, g2, ..., offset, string]. So m = [args[0], ...groups]; set m.index = offset. parts(m) uses m[1], m[2] — works if I construct array properly: `const m=[args[0]].concat(args.slice(1,-2)); m.index=args[args.length-2];` Then parts(m) works since parts access m[1], m[2]. 

Then html replay:
```js
let html=''; let cur=raw;
ruleMatches.forEach((ms,ri)=>{
  const r=RULES[ri];
  let outH='', last=0;
  for(const mm of ms){
    outH+=esc(cur.slice(last,mm.index))+mm.parts.map(p=>p===' '?'<span class="repair"> </span>':esc(p)).join('');
    last=mm.index+mm.match.length;
  }
  outH+=esc(cur.slice(last));
  html=outH; cur = cur.replace(r.re, (...args)=>{const m=[args[0]].concat(args.slice(1,-2)); return r.parts(m).join('');});
});
```
Wait but `cur` after replace must equal the text after rule ri — yes. And html built from cur before replacement with marks at match positions — correct. But note: ruleMatches[ri] indices refer to the text at start of rule ri — which is `cur` at that point in replay. ✓.

Hmm, but there's a subtlety with `r.re.lastIndex` reuse between the match-collection loop and replace — replace resets lastIndex internally? String.replace with /g regex starts from 0 and resets lastIndex after. Actually replace ignores/resets lastIndex. To be safe set r.re.lastIndex=0 before each use. Since RULES reused across paragraphs, always reset. In the collection loop I set lastIndex manually. OK.

Actually simpler: I can avoid the double bookkeeping by collecting matches AND building text in the same loop (as in my earlier applyRule), storing per-rule match lists; then replay only for html. Let me write:

```js
function processParagraph(raw){
  let text=raw; const logs=[]; const perRule=[];
  RULES.forEach(r=>{
    const ms=[]; let out=''; let last=0;
    r.re.lastIndex=0; let m;
    while((m=r.re.exec(text))!==null){
      const parts=r.parts(m);
      ms.push({index:m.index, match:m[0], parts});
      logs.push({rule:r.key,label:r.label,match:m[0],
        before:text.slice(Math.max(0,m.index-20),m.index),
        after:text.slice(m.index+m[0].length, m.index+m[0].length+20)});
      out+=text.slice(last,m.index)+parts.join('');
      last=m.index+m[0].length;
      r.re.lastIndex=last;
      if(m[0].length===0) r.re.lastIndex++;
    }
    out+=text.slice(last);
    text=out;
    perRule.push(ms);
  });
  // replay for html
  let cur=raw, html='';
  perRule.forEach((ms,ri)=>{
    const r=RULES[ri];
    let outH='', last=0;
    for(const mm of ms){
      outH+=esc(cur.slice(last,mm.index))+mm.parts.map(p=>p===' '?'<span class="repair"> </span>':esc(p)).join('');
      last=mm.index+mm.match.length;
    }
    outH+=esc(cur.slice(last));
    html=outH;
    let outT='', l2=0;
    for(const mm of ms){ outT+=cur.slice(l2,mm.index)+mm.parts.join(''); l2=mm.index+mm.match.length; }
    outT+=cur.slice(l2);
    cur=outT;
  });
  return {text, html, logs};
}
```

This is fine. Note: `r.parts(m)` — m from exec is an array with index; parts uses m[1], m[2] — works.

Edge: zero-length matches impossible here (all patterns consume ≥2 chars).

Now per paragraph: `const pr = processParagraph(p.text_raw); p.text=pr.text; p.html=pr.html; p.logs=pr.logs;`

First words:
```js
function normW(s){ return String(s).replace(/[\u2018\u2019]/g,"'").replace(/[\u201C\u201D]/g,'"').replace(/[\u2013\u2011]/g,'-').replace(/\u00A0/g,' '); }
function firstSix(t){ const w=normW(t).split(/\s+/).filter(Boolean); return w.slice(0,6).join(' '); }
p.first6 = firstSix(p.text);
const refKey = REF && REF.first_words ? String(p.num) : null;
const ref6 = (REF && REF.first_words && REF.first_words[String(p.num)]!=null) ? firstSix(REF.first_words[String(p.num)]) : null;
p.ref6 = ref6;
p.fwMatch = (ref6===null) ? null : (p.first6===ref6);
```

Characters:
```js
const CHARS=[
 {name:'en dash', ch:'\u2013', disp:'–'},
 {name:'double quotes', chs:['\u201C','\u201D'], disp:'“ ”'},
 {name:'right single quote', ch:'\u2019', disp:'’'},
 {name:'non-breaking hyphen', ch:'\u2011', disp:'‑'},
 {name:'non-breaking space', ch:'\u00A0', disp:'⍽'}, // display marker
];
```
Count over paragraph texts + heading texts + title text? I'll use paragraphs' text and headings' text. Build `charCorpus = paragraphs.map(p=>p.text).join('\n') + '\n' + headings.map(h=>h.text).join('\n')`. For each char count occurrences. Example: find first occurrence in corpus, snippet ±16 chars with the char highlighted (for nbsp, replace displayed char with '·' inside a mark span). Implementation: 

```js
function charRow(ch, disp){
  let count=0, idx=-1, src='';
  for(const t of corpusTexts){ let i=t.indexOf(ch); ... }
```
Simpler: count via split: `(t.split(ch).length-1)`. For multiple chars (quotes) sum. Example: find in first text containing it.

```js
function findExample(ch){
  for(const t of corpusTexts){ const i=t.indexOf(ch); if(i>=0) return {text:t, i}; }
  return null;
}
```
Snippet: `t.slice(Math.max(0,i-16), i) + '⟦'+disp+'⟧' + t.slice(i+ch.length, i+ch.length+16)` — with escaping and the char highlighted: I'll render `esc(before) + '<span class="chmark">'+esc(dispFor(ch))+'</span>' + esc(after)` where for nbsp dispFor = '·' (visible) — but then it's not the actual char... The hint says "on a keyboard: a hyphen and straight quotes". For nbsp I'll show '·' and label the row "non-breaking space (U+00A0)". For others show the actual char. OK.

Checks construction:

```js
const checks=[];
function addCheck(name, detail, status, link){ checks.push({name, detail, status, link}); }
```

1. Paragraph count: needs REF? "Found against reference.paragraphs" — if REF missing → notrun. status pass if equal.
2. Numbering: always runnable. nums in order 1..N. detail: "found 1–90 in order" or list gaps/dups.
3. First words: needs REF. mismatch list.
4. Footnotes: needs REF → status 'limit', detail "0 in this HTML · reference counts 141 in the PDF and Word versions — the HTML version has no footnotes: a limit of the source, not of the app". If no REF → notrun.
5. Repairs: always. "n spaces restored in n paragraphs (sentence n, comma n, quote n, dash n); every one listed on tab 03; text_raw keeps the text as found". status pass.
6. Headings: "n headings (x h2, y h3); z glued labels separated". pass.
7. Nothing lost: classified counts sum === blocks.length; unclassified listed. pass/fail.
8. Export round trip: build JSON, parse, compare length. pass/fail. (Run even without REF — export works without REF.)

If no paragraphs: tab 01 shows "no paragraphs found" message; exports disabled.

Status counts: pass/fail/limit/notrun.

Header status: 
```js
const npass=..., nfail=..., nlimit=...;
const m=npass+nfail;
statusHtml = nfail>0 ? `<span class="dot red"></span>${nfail} check${s} failed` : `<span class="dot green"></span>${npass} of ${m} checks pass`;
plus ` · <span class="red">${nlimit} source limit${s}</span>` if nlimit>0.
```

Rail: big numbers; bar width: REF? Math.min(n/REF.paragraphs,1)*100 : 100%; class red if n!==REF.paragraphs.

Now rendering functions. I'll write render code with template literals and innerHTML, then attach event listeners via delegation.

Tab 02 rows: build html string:

```js
rowsHtml = paragraphs.map((p,i)=>{
  const ok = p.fwMatch===true, bad = p.fwMatch===false;
  const chk = p.fwMatch===null ? '<span class="muted">no reference</span>' : ok ? '<span class="pass">OK</span>' : '<span class="fail">first words differ</span>';
  const first = esc(firstLine(p.text));
  return `<tr class="prow" data-i="${i}">
    <td class="num"><button class="pbtn" aria-expanded="false" aria-controls="det-${i}">${p.num}</button></td>
    <td class="sec">${esc(p.section)}</td>
    <td class="first">${first}</td>
    <td>${chk}</td></tr>
   <tr class="det" id="det-${i}" hidden><td colspan="4">${detailHtml(p,i)}</td></tr>`;
}).join('');
```

firstLine: first 120 chars cut at word + '…':
```js
function firstLine(t){ if(t.length<=120) return t; let cut=t.slice(0,120); const sp=cut.lastIndexOf(' '); if(sp>60) cut=cut.slice(0,sp); return cut+' …'; }
```

detailHtml:
```js
function detailHtml(p,i){
  const path = p.path.length? p.path.map(h=>esc(dispH(h))).join(' › ') : '(no heading above)';
  const fw = p.fwMatch===null ? '<span class="muted">no reference in this file</span>'
    : `<span class="mono">FOUND</span> “${esc(p.first6)}” · <span class="mono">REFERENCE</span> “${esc(p.ref6)}”`;
  const reps = p.logs.length ? `<div class="reps"><span class="mono">REPAIRED HERE</span><ul>${p.logs.map(l=>`<li>${esc(l.label)}: …${esc(l.before)}<b>${esc(l.match)}</b>${esc(l.after)}…</li>`).join('')}</ul></div>` : '<div class="reps muted">no space repaired in this paragraph</div>';
  return `<div class="path mono">${path}</div>
   <p class="full">${p.html}</p>
   <div class="fwline">${fw}</div>
   ${reps}
   <div class="cite-row"><button class="copy" data-cite="${esc(p.citation)}">Copy citation</button> <span class="mono">${esc(p.citation)}</span> ${DOC_URL?`<a href="${esc(DOC_URL)}" target="_blank" rel="noopener">${esc(SYMBOL)} ↗</a>`:''}</div>`;
}
```

citation = `${SYMBOL}, para. ${p.num}`.

Toggle: 
```js
tbody.addEventListener('click', e=>{
  const btn = e.target.closest('.pbtn'); const row = e.target.closest('.prow');
  if(row){ const i=row.dataset.i; toggleRow(i); }
});
function toggleRow(i){ const btn=..., det=...; const open = det.hidden; det.hidden=!open... }
```
Set aria-expanded on button, hidden on det. Also row click anywhere (except copy button inside det — det is separate row so fine).

Copy buttons: delegate on document: `e.target.closest('.copy')` → clipboard.

```js
function copyText(t, btn){
  const done=()=>{ const old=btn.textContent; btn.textContent='Copied'; btn.classList.add('copied'); setTimeout(()=>{btn.textContent=old; btn.classList.remove('copied');},2000); };
  if(navigator.clipboard && navigator.clipboard.writeText){ navigator.clipboard.writeText(t).then(done, ()=>fallback(t,done)); } else fallback(t,done);
}
function fallback(t,done){ const ta=document.createElement('textarea'); ta.value=t; ta.style.position='fixed'; ta.style.opacity='0'; document.body.appendChild(ta); ta.select(); try{document.execCommand('copy'); done();}catch(e){} ta.remove(); }
```

Tab 03 spaces table rows: click → openPara(num): selectTab(1) (index of tab 02), expand row with that num, scroll.

```js
function openPara(num){
  selectTab(1);
  const i = paragraphs.findIndex(p=>p.num===num);
  if(i>=0){ setRow(i,true); document.getElementById('det-'+i).scrollIntoView({block:'center'}); }
}
```

Spaces table row html:
```js
`<tr class="srow" data-num="${p.num}" title="open on tab 02">
  <td class="num">${p.num}</td>
  <td class="mono before">…${esc(l.before)}<b>${esc(l.match)}</b>${esc(l.after)}…</td>
  <td class="mono after">…${esc(l.before)}${esc(l.match).replace(...)}...`
```
For After with inserted space marked: I need match-with-space. Compute from rule: inserted position within match. Store in log: `afterMatch` = match with space inserted (plain), and for html mark the space. Let me store in log: `parts` (array) — then After cell = before + parts joined with the ' ' wrapped: `parts.map(p=>p===' '?'<span class="ins"> </span>':esc(p)).join('')`. And Before = before + `<b>`+esc(match)+`</b>` + after. I'll add `parts` to log entries. In processParagraph logs push parts too.

Rule column: l.label.

Rule counts line: count per rule key.

Characters table: as designed.

Tab 04 checks render:
```js
checks.map(c=>{
  const verdict = c.status==='pass' ? '<span class="pass">pass</span>'
    : c.status==='fail' ? `<span class="fail">check failed</span> ${c.link?`<a href="#" data-tab="${c.link.tab}">${esc(c.link.label)}</a>`:''}`
    : c.status==='limit' ? '<span class="fail">source limit</span>'
    : '<span class="muted">not run</span>';
  return `<div class="check"><span class="cname">${esc(c.name)}</span> <span class="cdetail">${c.detail}</span> ${verdict}</div>`;
})
```
detail may contain HTML (links) — I'll build detail as HTML string carefully with esc on data.

Check details:
1. `found ${n} · reference ${REF.paragraphs}` — pass/fail.
2. numbering: `sequence ${nums.join(', ')}`? too long. detail: `expected 1–${n} in order · found ${ok?'1–'+n+' in order': anomalies}`. anomalies: list like "para. position 5: expected 5, found 7" cap 8.
3. first words: `${mismatch} of ${n} mismatch` + list `para. 13: found “…” / reference “…”` cap 6 + link tab 02.
4. footnotes limit: `0 in this HTML · ${REF.footnotes} in the PDF and Word versions — the HTML version has no footnotes: a limit of the source, not of the app`.
5. repairs: `${total} spaces in ${parasWith} paragraphs · sentence ${a}, comma ${b}, quote ${c}, dash ${d} · all listed on tab 03 · text_raw unchanged` + link tab 03.
6. headings: `${h2} h2 + ${h3} h3 = ${headings.length} · ${glued} glued labels separated`.
7. nothing lost: `cover ${c} + container ${c} + title 1 + headings ${h} + paragraphs ${p} + text ${t} = ${blocks.length} of ${blocks.length} block elements` pass; else list unclassified.
8. export round trip: `JSON parsed back: ${parsed.length} records = ${paragraphs.length} rows` pass.

Links in checks: data-tab attr → click switches tab. I'll add delegation: `a[data-tab]` click → preventDefault, selectTab(+tab).

Elements table (tab 04): rows for each block: tag, cls, text 80 chars.

Export JSON:
```js
const exportRecords = paragraphs.map(p=>({
  symbol: SYMBOL,
  paragraph: p.num,
  section: p.section,
  part: p.part,
  text: p.text,
  text_raw: p.text_raw,
  first_words_match: p.fwMatch===null? null : p.fwMatch,
  citation: p.citation,
  doc_url: DOC_URL,
  limitations: 'no footnotes in this HTML version' + (REF&&REF.footnotes!=null?` ; the document has ${REF.footnotes} footnotes`:'')
}));
const jsonStr = JSON.stringify(exportRecords, null, 2);
```

Markdown:
```js
function buildMarkdown(){
  const today = new Date().toISOString().slice(0,10);
  const fm = ['---', `title: ${yaml(TITLE)}`, `symbol: ${SYMBOL}`, `adopted: ${REF&&REF.adopted?REF.adopted:''}`, `source_url: ${DOC_URL}`, `extracted: ${today}`, `paragraphs_found: ${paragraphs.length}`, `paragraphs_expected: ${REF&&REF.paragraphs!=null?REF.paragraphs:''}`, `footnotes: "0 of ${REF&&REF.footnotes!=null?REF.footnotes:'?'} — this HTML version has no footnotes"`, '---'].join('\n');
  let body='';
  // ordered items: I need document order of headings & paragraphs. I stored items order? Let me keep an `ordered` array during classification: push {type:'heading',rec} or {type:'paragraph',rec}.
  for(const it of ordered){
    if(it.type==='heading'){ const h=it.rec; const line = h.label? `${h.label}. ${h.heading}` : h.heading; body += (h.tag==='h2'?'## ':'### ')+line+'\n\n'; }
    else { const p=it.rec; body += `**${p.num}.** ${p.text}\n\n`; }
  }
  return fm+'\n# '+TITLE.replace(/\s*\*$/,'')+'\n\n'+body;
}
```
yaml(): quote if contains ':' — simple: wrap in double quotes escaping quotes: `JSON.stringify(TITLE)` gives quoted string — valid YAML double-quoted. Use that.

Title heading: `# title` — plan says headings as ## and ###; title as # is fine (it's the doc title). Actually plan: "then the headings as `##` and `###` lines in document order and each paragraph as its number in bold". The title h2 — I'll render as `#`. Acceptable.

Downloads:
```js
dlJson.onclick = ()=> download(SYMBOL.replace(/\//g,'-')+'.json', jsonStr, 'application/json');
dlMd.onclick = ()=> download(SYMBOL.replace(/\//g,'-')+'.md', mdStr, 'text/markdown');
```
Disable if no paragraphs: `btn.disabled = paragraphs.length===0`.

Round-trip check: `try{ const back=JSON.parse(jsonStr); ok = back.length===paragraphs.length; }catch(e){ ok=false; }` — run only if paragraphs.length>0? If 0, jsonStr='[]', parse length 0 === 0 → pass. Fine, but if no html at all, skip → notrun.

Now header/rail/tab01 rendering with REF possibly missing:
- If !REF: tiles: "no reference in this file" — tile values: paragraphs found n (beside "no reference in this file"), first words "not run", footnotes "not run", spaces n. Checks needing REF → notrun.

Tab 01 when no paragraphs: show a message block "This HTML yielded no numbered paragraphs." and disable exports.

Now CSS. Let me write it:

```css
*{box-sizing:border-box}
[hidden]{display:none!important}
html,body{margin:0}
body{background:#f4f0e8;color:#1d1b18;font:16px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
.serif{font-family:Georgia,"Times New Roman",serif}
.mono{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:11.5px;letter-spacing:.08em;text-transform:uppercase}
a{color:#9b2335}
header{padding:22px 30px 16px;border-bottom:1px solid #d9d2c3}
.kicker{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:11.5px;letter-spacing:.14em;color:#9b2335}
h1{font-family:Georgia,"Times New Roman",serif;font-weight:400;font-size:30px;line-height:1.2;margin:8px 0 10px;max-width:60ch}
.meta{display:flex;flex-wrap:wrap;gap:8px 18px;align-items:baseline;font-size:14px;color:#4a463f}
.meta .sym{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:12.5px}
.status{margin-left:auto;display:flex;align-items:center;gap:8px;font-family:ui-monospace,Menlo,Consolas,monospace;font-size:11.5px;letter-spacing:.06em}
.dot{width:9px;height:9px;border-radius:50%;display:inline-block}
.dot.green{background:#1e6b3a}.dot.red{background:#9b2335}
.green{color:#1e6b3a}.red{color:#9b2335}.fail{color:#9b2335;font-weight:600}.pass{color:#1e6b3a;font-weight:600}.muted{color:#8a8378}
.layout{display:flex;align-items:flex-start}
aside{flex:0 0 264px;border-right:1px solid #d9d2c3;padding:20px 22px;position:sticky;top:0;max-height:100vh;overflow:auto}
main{flex:1;min-width:0;padding:20px 30px 60px}
.rail-h{...mono label with border-bottom}
.doc-card{border:1px solid #d9d2c3;padding:10px 12px;margin:12px 0 18px}
.big{font-family:Georgia,serif;font-size:44px;line-height:1.05;margin-top:14px}
.big .of{font-size:16px;font-family:...sans;color:#4a463f}
.bar{height:3px;background:#d9d2c3;margin:6px 0 2px}
.bar i{display:block;height:100%;background:#1e6b3a}
.bar i.bad{background:#9b2335}
.note{font-size:13px;margin:2px 0 0}
.linklike{background:none;border:none;padding:0;color:#9b2335;cursor:pointer;font:inherit;text-decoration:underline;font-size:14px;margin-top:16px}
.tabs{display:flex;gap:2px;border-bottom:1px solid #d9d2c3;margin-bottom:20px;flex-wrap:wrap}
.tabs [role="tab"]{background:none;border:none;border-bottom:2px solid transparent;padding:10px 14px 8px;cursor:pointer;font-family:ui-monospace,Menlo,Consolas,monospace;font-size:11.5px;letter-spacing:.1em;color:#4a463f}
.tabs [role="tab"][aria-selected="true"]{color:#9b2335;border-bottom-color:#9b2335}
:focus-visible{outline:2px solid #9b2335;outline-offset:2px}
.tiles{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:1px;background:#d9d2c3;border:1px solid #d9d2c3}
.tile{background:#f4f0e8;padding:16px 18px}
.t-label{mono}
.t-num{font-family:Georgia,serif;font-size:52px;line-height:1;margin:8px 0 4px}
.t-beside{font-size:14px;color:#4a463f}
.how{font-size:12.5px;color:#6b655b;margin-top:10px;border-top:1px solid #d9d2c3;padding-top:8px}
table{border-collapse:collapse;width:100%;margin:10px 0 22px}
caption{text-align:left;font-family:Georgia,serif;font-size:19px;padding:6px 0 10px}
caption .tabno{font-family:ui-monospace...;font-size:11px;color:#9b2335;letter-spacing:.12em;display:block;margin-bottom:4px}
th{font-family:ui-monospace...;font-size:11px;letter-spacing:.1em;text-transform:uppercase;font-weight:400;color:#4a463f;text-align:left;border-bottom:1px solid #1d1b18;padding:6px 10px 6px 0}
td{border-bottom:1px solid #d9d2c3;padding:8px 10px 8px 0;vertical-align:top;font-size:15px}
th.num,td.num{text-align:right;font-variant-numeric:tabular-nums}
.prow{cursor:pointer}
.prow:hover td{background:#ece6d9}
.pbtn{background:none;border:none;font:inherit;font-weight:600;color:#9b2335;cursor:pointer;padding:0 4px;font-variant-numeric:tabular-nums}
.det td{background:#efe9dc;padding:14px 18px}
.full{font-size:15.5px;max-width:75ch}
.repair{box-shadow:inset 0 0 0 1px #9b2335}
.ins{box-shadow:inset 0 0 0 1px #9b2335}
.fold{background:none;border:none;border-bottom:1px solid #d9d2c3;width:100%;text-align:left;padding:10px 2px;cursor:pointer;font-family:Georgia,serif;font-size:18px;color:#1d1b18}
.fold .cnt{color:#9b2335}
.block h2{font-family:Georgia,serif;font-weight:400;font-size:24px;margin:26px 0 8px}
.block h2 .count{color:#9b2335;font-size:20px;margin-left:8px}
.check{display:flex;gap:10px;flex-wrap:wrap;padding:9px 0;border-bottom:1px solid #d9d2c3;font-size:14.5px}
.cname{font-family:ui-monospace...;font-size:11.5px;letter-spacing:.08em;text-transform:uppercase;min-width:150px;padding-top:2px}
.btn{background:#1d1b18;color:#f4f0e8;border:none;padding:10px 16px;cursor:pointer;font:inherit;font-size:14.5px;margin-right:10px}
.btn:disabled{opacity:.4;cursor:not-allowed}
footer{border-top:1px solid #d9d2c3;padding:14px 30px 26px;font-size:13px;color:#4a463f}
footer .credits{margin-top:6px;font-size:12px;color:#8a8378}
.srow{cursor:pointer}
.srow:hover td{background:#ece6d9}
.before,.after{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:12px;letter-spacing:0;text-transform:none;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;max-width:340px}
```

Hmm .mono class sets uppercase — for before/after cells I don't want uppercase. I'll use a separate class `.code` without uppercase. Let me define `.code{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:12px}` and `.mono` for labels (uppercase). 

Path line in detail: `.path{color:#6b655b;margin-bottom:8px}` using .code.

Headings list (tab 02 fold): list of headings: `<div class="hlist"><span class="code">I.</span> Introduction</div>` etc.

Now, the "How this is computed" for rail numbers — plan says one line near every chart or number; rail big numbers get small hints: under paragraphs number: mono hint "counted from the HTML's <p> elements"; under footnotes: "not in this HTML". OK.

Also tab 01 tile 1 "beside the document has reference.paragraphs (green when equal, red with the difference)". diff = n - ref; show `+x`/`−x` red.

Let me also handle `REF.adopted` in header meta: "adopted 6 November 2025"? reference.adopted — value unknown format; display as-is: `adopted ${REF.adopted}`. If missing, omit.

Header meta line: symbol link, "adopted …", source. Source might be long; fine.

Now assemble everything. Also the tab-01 "Spaces: n repaired or flagged, linking to tab 03" — make the beside text a link `a[data-tab="2"]`.

Links with data-tab: delegation:
```js
document.addEventListener('click', e=>{
  const a=e.target.closest('[data-tab]');
  if(a){ e.preventDefault(); selectTab(parseInt(a.dataset.tab,10)); }
  const c=e.target.closest('.copy'); if(c){ copyText(c.dataset.cite, c); }
  const s=e.target.closest('.srow'); if(s){ openPara(parseInt(s.dataset.num,10)); }
});
```
Careful: .pbtn click also bubbles to document — handle prow toggle in tbody listener; but the document-level handler for [data-tab] etc. fine. Also clicking copy inside det row — det rows aren't .prow so no toggle. But clicking .pbtn triggers both tbody handler (toggle) — good; ensure not double-toggle: tbody listener on click checks closest('.prow') — the button is inside prow → toggle once. OK.

Keyboard on rows: button handles Enter/Space natively → click event → toggle. Good.

Arrow-key tab nav implemented.

Rail checks link: `<button class="linklike" data-tab="3">7 of 7 checks pass</button>`.

Now, "Headings found: n" fold on tab 02: button.fold with aria-expanded, controls div hidden.

Elements fold on tab 04 similarly.

Let me now also compute `ordered` during classification: push {type:'heading'|'paragraph', rec}. Title not included (or include as title for markdown `#`). I'll include title in ordered as {type:'title'}.

Edge: paragraphs before any heading → section '' → display '(no heading above)'.

Now write final counts for checks:

```js
// numbering
let numOk=true; const anomalies=[];
paragraphs.forEach((p,i)=>{ if(p.num!==i+1){ numOk=false; anomalies.push(`position ${i+1}: expected ${i+1}, found ${p.num}`); } });
const dups = paragraphs.map(p=>p.num).filter((n,i,a)=>a.indexOf(n)!==i);
```
detail: numOk ? `1–${paragraphs.length} in order, no gaps or duplicates` : anomalies.slice(0,8).join('; ') + (dups.length?`; duplicate numbers: ${[...new Set(dups)].join(', ')}`:'').

First words mismatches:
```js
const fwMismatch = paragraphs.filter(p=>p.fwMatch===false);
const fwNoRef = paragraphs.filter(p=>p.fwMatch===null);
```
If !REF or !REF.first_words → check notrun. Else pass if fwMismatch.length===0 && fwNoRef.length===0? If some keys missing → treat as fail with note. detail: `${fwMismatch.length} of ${paragraphs.length} differ` + list.

List entries: `para. ${p.num}: found “${p.first6}” / reference “${p.ref6}”` — cap 6, plus "…".

Nothing lost:
```js
const clsCounts={}; elements.forEach(e=>clsCounts[e.cls]=(clsCounts[e.cls]||0)+1);
const sum = Object.values(clsCounts).reduce((a,b)=>a+b,0);
const unclassified = elements.filter(e=>e.cls==='unclassified');
status = (sum===elements.length && unclassified.length===0) ? 'pass':'fail';
```
Since every element gets a class, unclassified only if tag not handled — my classifier: tags in TAGS list; p→paragraph/text; h1-h6→title/heading; table/div/section/article→cover/container; ul/ol/li/blockquote/pre/header/footer/nav → 'unclassified'. Good.

Headings check: h2count = headings.filter(h=>h.tag==='h2').length etc. glued = headings.filter(h=>h.glued).length.

Repairs check: total logs, per rule counts, paragraphs with logs count.

Export round trip: as above.

Footnotes check: status 'limit' if REF&&REF.footnotes!=null else 'notrun'. detail: `0 in this HTML · ${REF.footnotes} in the PDF and Word versions — the HTML version has no footnotes: a limit of the source, not of the app`.

Paragraph count check: REF? compare : notrun.

Now tab 01 tiles with no REF: 
- T1: big n, beside "no reference in this file" (muted).
- T2: big "—", beside "no reference in this file".
- T3: big "0", beside "no reference in this file" — hmm footnotes tile: "0 of reference.footnotes" — without REF: "0 footnotes in this HTML · no reference in this file". Keep red? The red is because HTML lacks them — still true: 0 footnotes found in HTML. I'll show big 0 red with beside "in this HTML; no reference in this file".
- T4: n spaces.

If no paragraphs at all: tab 01 shows a paragraph "This HTML yielded no numbered paragraphs — nothing to show on tabs 02–04, exports disabled." plus tiles? I'll show message and still tiles with 0s. Simpler: if paragraphs.length===0, tab01 innerHTML = message; exports disabled; other tabs show "no paragraphs". I'll guard rendering.

Now header status when checks not run (no REF): m = pass+fail; if m===0 → status "checks not run". Handle.

Let me now write out the whole file. I'll be careful with template literals inside the script — fine.

One more detail: `dispH(h)` = h.label ? `${h.label}. ${h.heading}` : h.heading.

Section for row: p.section = lastHeading display at time of paragraph. Path: curPath — but curPath resets on h2; includes the h2 itself. For a paragraph right after h2 "IV. X", path = [IV. X]. Detail path shows "IV. X". For paragraph under h3: path = [IV. X, D. Y, Right to work]. Display joined " › ". Good.

part: curPart = roman h2 display; if none yet, ''.

Export `section` and `part`: section = p.section (nearest heading display), part = p.part.

Markdown heading lines: use dispH.

Also add to detail: doc symbol link — done.

Character corpus: include title text too? Plan says paragraph texts; I decided paragraphs + headings. I'll also include title? The nbsp are in headings. Keep paragraphs+headings, and the how-line says "counted over every paragraph and heading text in this file".

Wait, actually let me reconsider: plan says "Counted over all paragraph texts". The found data says 2 nbsp inside headings — if I count only paragraphs, nbsp row = 0 with no example. The plan's tab 03 wants a row for nbsp with an example. So counting paragraphs+headings is the sensible reading ("all paragraph texts" loosely = all extracted texts). I'll count over paragraphs + headings + title and say "every paragraph, heading and title text". Hmm, title has the asterisk... fine, include title too? The title is an h2 classified as title — its text includes " *". I'll include headings only (not title) — nbsp are in headings per found data. Label: "counted over every paragraph and heading text". Good.

Example for nbsp: snippet with '·' marker.

Let me write charRow rendering:

```js
const corpus = paragraphs.map(p=>p.text).concat(headings.map(h=>h.text));
function countCh(ch){ let n=0; for(const t of corpus) n += t.split(ch).length-1; return n; }
function exampleFor(ch, dispCh){
  for(const t of corpus){ const i=t.indexOf(ch); if(i>=0){ const b=t.slice(Math.max(0,i-18),i), a=t.slice(i+ch.length,i+ch.length+18); return esc(b)+'<span class="chmark">'+esc(dispCh)+'</span>'+esc(a); } }
  return '<span class="muted">none found</span>';
}
```
For double quotes (two chars), count both, example for U+201C. dispCh for nbsp: '·' with note. Actually to be precise, for nbsp row I'll display the marker '·' and the row label "non-breaking space (U+00A0)". For others dispCh = the char itself.

chmark CSS: `.chmark{box-shadow:inset 0 0 0 1px #9b2335;padding:0 1px}`.

Rows:
```js
const charRows=[
 ['en dash (U+2013)','\u2013','–'],
 ['double quotes (U+201C / U+201D)',['\u201C','\u201D'],'“'],
 ['right single quote (U+2019)','\u2019','’'],
 ['non-breaking hyphen (U+2011)','\u2011','‑'],
 ['non-breaking space (U+00A0)','\u00A0','·'],
];
```
count for array: sum.

Now the spaces table: gather all logs across paragraphs: `allLogs = []` with p.num attached. Sort by paragraph order (they're already in order). Rule counts.

Row html:
```js
`<tr class="srow" data-num="${l.num}" title="open para. ${l.num} on tab 02">
 <td class="num">${l.num}</td>
 <td class="code before">…${esc(l.before)}<b>${esc(l.match)}</b>${esc(l.after)}…</td>
 <td class="code after">…${esc(l.before)}${l.parts.map(p=>p===' '?'<span class="ins"> </span>':esc(p)).join('')}${esc(l.after)}…</td>
 <td>${esc(l.label)}</td></tr>`
```
Need parts in log — add.

Hmm wait: in the After cell, `l.before` + parts + `l.after` — but parts joined = match with space; before/after are context from the string at rule time — consistent. Good.

Now the fold for headings list on tab 02:

```js
headingsList.innerHTML = headings.map(h=>`<div class="hitem"><span class="code lbl">${esc(h.label? h.label+'.':'')}</span> ${esc(h.heading)}</div>`).join('');
```

Fold toggle generic:
```js
document.querySelectorAll('.fold').forEach(b=>{
  b.addEventListener('click',()=>{ const t=document.getElementById(b.getAttribute('aria-controls')); const open=t.hidden; t.hidden=!open; b.setAttribute('aria-expanded',String(open)); });
});
```

Now header build:

```js
document.getElementById('kicker').textContent='UN DOCUMENT · HTML';
h1.textContent = TITLE;
meta: `<a class="sym" href="${DOC_URL}" target="_blank" rel="noopener">${SYMBOL}</a> <span>adopted ${REF&&REF.adopted?esc(REF.adopted):'—'}</span> <span>${esc(SOURCE)}</span>` + status span.
```
If DOC_URL empty, no link: just span.

Rail:
```js
railDoc: `<div class="code sym">${esc(SYMBOL)}</div><div class="doc-title">${esc(shortTitle)}</div>`
shortTitle: TITLE stripped of trailing ' *', maybe truncated 90 chars.
big1: `<div class="big">${paragraphs.length} <span class="of">paragraphs of ${REF&&REF.paragraphs!=null?REF.paragraphs:'?'}</span></div><div class="bar"><i style="width:${w}%" class="${bad?'bad':''}"></i></div><div class="note code">counted from the HTML's &lt;p&gt; elements</div>`
big2: `<div class="big red">0 <span class="of">footnotes of ${REF&&REF.footnotes!=null?REF.footnotes:'?'}</span></div><div class="note red">not in this HTML</div>`
checks link: `<button class="linklike" data-tab="3">${statusText}</button>`
```

statusText: fail>0 ? `${nfail} checks failed` : `${npass} of ${m} checks pass` (or 'checks not run').

Tab 01 tiles html:

```js
const diff = REF&&REF.paragraphs!=null ? paragraphs.length-REF.paragraphs : null;
tile1: num=paragraphs.length; beside: REF? `the document has ${REF.paragraphs}` + (diff===0? green ' — equal' : red ` (${diff>0?'+':''}${diff})`) : 'no reference in this file';
tile2: num = REF&&REF.first_words? `${fwOk} of ${paragraphs.length}`... big number should be a number: use fwOk count; beside `of ${REF.paragraphs} paragraphs match the reference's first six words` — hmm plan: "First words match: n of reference.paragraphs". big: `${fwMatchCount} of ${REF.paragraphs}`? Big number as "n of m" string in serif — fine, font-size maybe smaller. I'll put big = fwMatchCount, beside = `of ${REF.paragraphs} paragraphs match on the first six words` (red if < ref).
tile3: big 0 red, beside `of ${REF.footnotes} footnotes — this HTML version has none; <a data-tab="2">see tab 03</a>`.
tile4: big totalRepairs, beside `spaces repaired or flagged — <a data-tab="2">see tab 03</a>`.
```

How lines as planned.

Tab 02 caption: `${paragraphs.length} paragraphs found, ${REF?REF.paragraphs:'?'} expected`.

OK. Also "How this is computed" near tab02 caption? The caption states message; add small mono line under caption? I'll add a `.how` line above table: "One row per <p> whose text starts with a number and a full stop; click a row for the full text." Good.

Now write everything. Also remember: no external loads. Chart.js not needed (no charts). 

Footer:
```js
footer.innerHTML = `${esc(SOURCE)}${BUILT? ' · built '+esc(BUILT):''} · Done by this page's code; no model was called and nothing left the browser.
<div class="credits">Sources consulted: The Turing Way, “Documentation and metadata” (CC BY 4.0) · UK Government Analysis Function, “Quality assurance of code for analysis and research: Testing code” (Open Government Licence v3.0) · Dag Hammarskjöld Library, “Ask DAG: how should I cite a UN document?”</div>`;
```

Now, potential pitfall: `body.querySelectorAll(TAGS)` — TAGS includes 'header','footer','nav' etc. The parsed doc body contains table + div.content. Fine.

Also the html string starts with `<body>` — DOMParser with 'text/html' will handle; doc.body exists.

Another pitfall: paragraph regex on collapsed text — collapse first: `const text = collapse(el.textContent)`. For `<p>1.A clean…</p>`, textContent = "1.A clean…". match → num 1, raw "A clean…". But wait — collapse preserves nbsp; if a paragraph starts "1.\u00A0A clean"? \s* in regex — \s matches nbsp in JS? Yes \s includes \u00A0. So `\.\s*` eats nbsp too. Fine.

Hmm, one thing: `collapse` uses `[^\S\u00A0]+` — this collapses all whitespace except nbsp. But `\s` in PARA_RE `\s*` matches nbsp — so "1.\u00A0Text" → raw "Text". OK.

Numbering: nums might not be 1..90 if some p's are cover etc. Fine.

Let me also double check heading regex against "I.Introduction": text collapsed = "I.Introduction". HEAD_RE = /^([IVX]+|[A-Z])\.\s*([\s\S]+)$/ — "I" matches [IVX]+, ".", \s* matches empty, "Introduction". label "I", heading "Introduction". glued check: /^I\.[^\s]/ on "I.Introduction" → true. Good. "D. Obligation": label "D", heading "Obligation", glued false (space after dot). Good.

But careful: a plain h3 like "Right to work (art. 6)" — HEAD_RE: `^([IVX]+|[A-Z])\.` — "R" then "ight..." — needs `\.` right after the single char — "Right" → after "R" comes "i", not "." → no match. Good. But what about a heading like "A. Something" (lettered h3) → matches, label "A". Good. What about "X.509..."? Not present.

Edge: heading "I.Introduction" — but what if heading text is like "V.1. Something"? [IVX]+ matches "V", then ".", then "1. Something" as heading. Fine.

Potential false positive: h3 "A.1 Introduction"? label "A", heading "1 Introduction". OK.

Now — one concern: the first h2 is the title. But what if there are h2s before div.content? No. titleEl set on first h1/h2 encountered outside table. Good.

Also: elements inside table include `<p>` — classified cover before the p-check. Order of conditions: inTable first. ✓.

Now the "Elements found (n)" table: n = elements.length (all block elements incl. cover). Rows: tag, cls, text 80.

Let me now also make sure at most ~7 clickable per view: tab04: 4 tabs + 2 buttons + 1 fold = 7 ✓. tab02: 4 tabs + 1 fold = 5 ✓ (rows excluded). tab03: 4 tabs + rows ✓. tab01: 4 tabs + 2 links (tiles 3,4) = 6 ✓.

Time to write the final code. I'll aim for clean, complete implementation.

Also the intro text before code block: at most three short sentences. After code block: nothing.

Let me write the script fully now, mentally compiling.

```js
(function(){
"use strict";
var WD = window.WORKSHOP_DATA || {};
var raw = WD.html_doc;
var D = Array.isArray(raw) ? (raw[0] || {}) : (raw || {});
var html = typeof D.html === 'string' ? D.html : '';
var REF = (D && D.reference && typeof D.reference === 'object') ? D.reference : null;
var SYMBOL = D.symbol || '(no symbol in this file)';
var TITLE = D.title || '(untitled document)';
var DOC_URL = D.doc_url || '';
var SOURCE = D.source || 'source not stated in this file';
var BUILT = D.built || '';

function esc(s){ return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;'); }
function collapse(s){ return String(s).replace(/[^\S\u00A0]+/g,' ').trim(); }

var body = null;
if(html){ try { body = new DOMParser().parseFromString(html,'text/html').body; } catch(e){ body=null; } }

var TAGS='table,div,p,h1,h2,h3,h4,h5,h6,ul,ol,li,blockquote,pre,section,article';
var blocks = body ? Array.prototype.slice.call(body.querySelectorAll(TAGS)) : [];
var firstTable = body ? body.querySelector('table') : null;

var PARA_RE=/^(\d{1,3})\.\s*([\s\S]*)$/;
var HEAD_RE=/^([IVX]+|[A-Z])\.\s*([\s\S]+)$/;

var elements=[], paragraphs=[], headings=[], ordered=[];
var titleSeen=false, lastHeading=null, curPath=[], curPart='';

function dispH(h){ return h.label ? h.label+'. '+h.heading : h.heading; }

blocks.forEach(function(el){
  var tag=el.tagName.toLowerCase();
  var text=collapse(el.textContent);
  var inTable = firstTable && (el===firstTable || firstTable.contains(el));
  var cls, rec=null;
  if(inTable){ cls='cover'; }
  else if(tag==='div'||tag==='section'||tag==='article'){ cls='container'; }
  else if(tag==='p'){
    var m=text.match(PARA_RE);
    if(m){ cls='paragraph'; rec={num:parseInt(m[1],10), text_raw:m[2].trim(), section: lastHeading?dispH(lastHeading):'', part:curPart, path:curPath.slice()}; paragraphs.push(rec); ordered.push({type:'paragraph',rec:rec}); }
    else cls='text';
  }
  else if(/^h[1-6]$/.test(tag)){
    if(!titleSeen && (tag==='h1'||tag==='h2')){ cls='title'; titleSeen=true; ordered.push({type:'title',text:text}); }
    else {
      cls='heading';
      var hm=text.match(HEAD_RE), label=null, head=text, glued=false;
      if(hm){ label=hm[1]; head=hm[2]; glued = new RegExp('^'+label.replace(/[.*+?^${}()|[\]\\]/g,'\\$&')+'\\.[^\\s]').test(text); }
      rec={tag:tag,label:label,heading:head,text:text,glued:glued};
      headings.push(rec); ordered.push({type:'heading',rec:rec});
      lastHeading=rec;
      if(tag==='h2'){ curPath=[rec]; if(label && /^[IVX]+$/.test(label)) curPart=dispH(rec); }
      else curPath.push(rec);
    }
  }
  else cls='unclassified';
  elements.push({tag:tag, cls:cls, text:text});
});
```

Wait: text_raw = m[2] — but text was collapsed already; m[2] from collapsed text; trim again fine. But note: collapse preserves nbsp; if paragraph begins "1.\u00A0A" the `\s*` eats nbsp. OK.

Hmm — one issue: `m[2].trim()` — collapse already trimmed the whole text; m[2] may have leading space if "1. Text" — `\s*` consumes it. Fine.

Repairs:

```js
var RULES=[
 {key:'sentence',label:'sentence join',re:/([a-z])\.([A-Z])/g,parts:function(m){return [m[1]+'.',' ',m[2]];}},
 {key:'comma',label:'comma join',re:/([a-z]),([A-Za-z])/g,parts:function(m){return [m[1]+',',' ',m[2]];}},
 {key:'quote',label:'quote join',re:/([a-z])\u201C/g,parts:function(m){return [m[1],' ','\u201C'];}},
 {key:'dash',label:'dash join',re:/\u2013([A-Za-z])/g,parts:function(m){return ['\u2013',' ',m[1]];}}
];

function processParagraph(rawText){
  var text=rawText, logs=[], perRule=[];
  RULES.forEach(function(r){
    var ms=[], out='', last=0; r.re.lastIndex=0; var m;
    while((m=r.re.exec(text))!==null){
      var parts=r.parts(m);
      ms.push({index:m.index, match:m[0], parts:parts});
      logs.push({rule:r.key, label:r.label, match:m[0], parts:parts,
        before:text.slice(Math.max(0,m.index-20),m.index),
        after:text.slice(m.index+m[0].length, m.index+m[0].length+20)});
      out+=text.slice(last,m.index)+parts.join('');
      last=m.index+m[0].length;
      r.re.lastIndex=last;
      if(m[0].length===0) r.re.lastIndex++;
    }
    out+=text.slice(last);
    text=out;
    perRule.push(ms);
  });
  var cur=rawText, htmlOut='';
  perRule.forEach(function(ms,ri){
    var r=RULES[ri], outH='', last=0, outT='', l2=0;
    ms.forEach(function(mm){
      outH+=esc(cur.slice(last,mm.index))+mm.parts.map(function(p){return p===' '?'<span class="repair"> </span>':esc(p);}).join('');
      outT+=cur.slice(l2,mm.index)+mm.parts.join('');
      last=mm.index+mm.match.length; l2=last;
    });
    outH+=esc(cur.slice(last)); outT+=cur.slice(l2);
    htmlOut=outH; cur=outT;
  });
  return {text:text, html:htmlOut, logs:logs};
}
```

Then:
```js
paragraphs.forEach(function(p){
  var pr=processParagraph(p.text_raw);
  p.text=pr.text; p.html=pr.html; p.logs=pr.logs;
  p.citation=SYMBOL+', para. '+p.num;
});
```

First words:
```js
function normW(s){ return String(s).replace(/[\u2018\u2019]/g,"'").replace(/[\u201C\u201D]/g,'"').replace(/[\u2013\u2011]/g,'-').replace(/\u00A0/g,' '); }
function firstSix(t){ return normW(t).split(/\s+/).filter(Boolean).slice(0,6).join(' '); }
paragraphs.forEach(function(p){
  p.first6=firstSix(p.text);
  if(REF && REF.first_words && REF.first_words[String(p.num)]!=null){ p.ref6=firstSix(REF.first_words[String(p.num)]); p.fwMatch=(p.first6===p.ref6); }
  else { p.ref6=null; p.fwMatch=null; }
});
```

Characters:
```js
var corpus = paragraphs.map(function(p){return p.text;}).concat(headings.map(function(h){return h.text;}));
function countCh(ch){ var n=0; corpus.forEach(function(t){ n+=t.split(ch).length-1; }); return n; }
function exampleFor(ch, disp){
  for(var i=0;i<corpus.length;i++){ var t=corpus[i], idx=t.indexOf(ch);
    if(idx>=0){ var b=t.slice(Math.max(0,idx-18),idx), a=t.slice(idx+ch.length, idx+ch.length+18);
      return esc(b)+'<span class="chmark">'+esc(disp)+'</span>'+esc(a); } }
  return '<span class="muted">none found</span>';
}
```

Checks:
```js
var checks=[];
function addCheck(name, detailHtml, status, link){ checks.push({name:name, detail:detailHtml, status:status, link:link||null}); }

var n=paragraphs.length;
// 1
if(REF && REF.paragraphs!=null){ addCheck('Paragraph count', 'found '+n+' · reference '+REF.paragraphs, n===REF.paragraphs?'pass':'fail'); }
else addCheck('Paragraph count','found '+n+' · no reference in this file','notrun');
// 2 numbering
var numOk=true, anomalies=[];
paragraphs.forEach(function(p,i){ if(p.num!==i+1){ numOk=false; anomalies.push('position '+(i+1)+': expected '+(i+1)+', found '+p.num); } });
var seen={}, dups=[];
paragraphs.forEach(function(p){ if(seen[p.num]) dups.push(p.num); seen[p.num]=1; });
var numDetail = numOk ? '1–'+n+' in order, no gaps, no duplicates' : (anomalies.slice(0,8).join('; ')+(dups.length?'; duplicate numbers: '+dups.join(', '):''));
addCheck('Numbering', esc(numDetail), numOk?'pass':'fail');
// 3 first words
if(REF && REF.first_words){
  var mm=paragraphs.filter(function(p){return p.fwMatch===false;});
  var nr=paragraphs.filter(function(p){return p.fwMatch===null;});
  var det=(mm.length+nr.length)+' of '+n+' differ';
  var list=mm.slice(0,6).map(function(p){return 'para. '+p.num+': found \u201C'+p.first6+'\u201D / reference \u201C'+(p.ref6||'—')+'\u201D';});
  if(nr.length) list.push(nr.length+' paragraphs have no reference entry');
  if(list.length) det+=' — '+list.join('; ');
  addCheck('First words', esc(det), (mm.length===0&&nr.length===0)?'pass':'fail', {tab:1,label:'see tab 02'});
} else addCheck('First words','no reference in this file','notrun');
// 4 footnotes
if(REF && REF.footnotes!=null){ addCheck('Footnotes','0 in this HTML · '+REF.footnotes+' in the PDF and Word versions — the HTML version has no footnotes: a limit of the source, not of the app','limit'); }
else addCheck('Footnotes','no reference in this file','notrun');
// 5 repairs
var allLogs=[]; paragraphs.forEach(function(p){ p.logs.forEach(function(l){ allLogs.push({num:p.num, rule:l.rule, label:l.label, match:l.match, parts:l.parts, before:l.before, after:l.after}); }); });
var perRuleCount={}; allLogs.forEach(function(l){ perRuleCount[l.rule]=(perRuleCount[l.rule]||0)+1; });
var parasWithRepairs = paragraphs.filter(function(p){return p.logs.length>0;}).length;
addCheck('Repairs', allLogs.length+' spaces restored in '+parasWithRepairs+' paragraphs · sentence '+(perRuleCount.sentence||0)+', comma '+(perRuleCount.comma||0)+', quote '+(perRuleCount.quote||0)+', dash '+(perRuleCount.dash||0)+' · every one listed on tab 03 · text_raw keeps the text as found','pass',{tab:2,label:'see tab 03'});
// 6 headings
var h2c=headings.filter(function(h){return h.tag==='h2';}).length, h3c=headings.length-h2c;
var glued=headings.filter(function(h){return h.glued;}).length;
addCheck('Headings', h2c+' h2 + '+h3c+' h3 = '+headings.length+' headings · '+glued+' glued labels separated','pass');
// 7 nothing lost
var clsCounts={}; elements.forEach(function(e){ clsCounts[e.cls]=(clsCounts[e.cls]||0)+1; });
var sum=0; for(var k in clsCounts) sum+=clsCounts[k];
var uncl=elements.filter(function(e){return e.cls==='unclassified';});
var det7 = Object.keys(clsCounts).map(function(k){return k+' '+clsCounts[k];}).join(' + ')+' = '+sum+' of '+elements.length+' block elements';
if(uncl.length) det7 += ' — unclassified: '+uncl.slice(0,5).map(function(e){return e.tag;}).join(', ');
addCheck('Nothing lost', esc(det7), (sum===elements.length && uncl.length===0)?'pass':'fail');
// 8 export round trip
var jsonStr = buildJson();
var rtOk=false, rtDetail='not run';
if(n>0 || true){ try{ var back=JSON.parse(jsonStr); rtOk=(back.length===n); rtDetail='JSON parsed back: '+back.length+' records = '+n+' rows on tab 02'; }catch(e){ rtDetail='JSON parse failed: '+e.message; } }
addCheck('Export round trip', esc(rtDetail), rtOk?'pass':'fail');
```

Hmm — buildJson needs paragraphs with all fields; define before checks. Also if no html at all (body null), n=0, jsonStr='[]', round trip 0=0 pass. But tab01 should say no paragraphs. OK.

Status counts:
```js
var npass=checks.filter(c=>c.status==='pass').length, nfail=..., nlimit=..., nnotrun=...;
var m=npass+nfail;
var statusText = nfail>0 ? nfail+' check'+(nfail>1?'s':'')+' failed' : (m>0 ? npass+' of '+m+' checks pass' : 'checks not run');
```

buildJson:
```js
function buildJson(){
  var recs=paragraphs.map(function(p){
    return { symbol:SYMBOL, paragraph:p.num, section:p.section, part:p.part, text:p.text, text_raw:p.text_raw,
      first_words_match:(p.fwMatch===null?null:p.fwMatch), citation:p.citation, doc_url:DOC_URL,
      limitations:'no footnotes in this HTML version'+(REF&&REF.footnotes!=null?'; the document has '+REF.footnotes+' footnotes':'') };
  });
  return JSON.stringify(recs,null,2);
}
```

buildMarkdown:
```js
function buildMarkdown(){
  var today=new Date().toISOString().slice(0,10);
  var fn=REF&&REF.footnotes!=null?REF.footnotes:'?';
  var fm=['---','title: '+JSON.stringify(TITLE),'symbol: '+JSON.stringify(SYMBOL),
    'adopted: '+(REF&&REF.adopted?JSON.stringify(String(REF.adopted)):'""'),
    'source_url: '+JSON.stringify(DOC_URL),'extracted: '+today,
    'paragraphs_found: '+n,'paragraphs_expected: '+(REF&&REF.paragraphs!=null?REF.paragraphs:'null'),
    'footnotes: '+JSON.stringify('0 of '+fn+' — this HTML version has no footnotes'),'---'].join('\n');
  var out=fm+'\n\n# '+TITLE.replace(/\s*\*$/,'')+'\n\n';
  ordered.forEach(function(it){
    if(it.type==='title') return;
    if(it.type==='heading'){ var h=it.rec; out+=(h.tag==='h2'?'## ':'### ')+dispH(h)+'\n\n'; }
    else { var p=it.rec; out+='**'+p.num+'.** '+p.text+'\n\n'; }
  });
  return out;
}
```

Rendering — I'll write render() that fills containers. Let me define the static HTML skeleton with empty containers and ids:

```html
<header>
 <div class="kicker" id="kicker">UN DOCUMENT · HTML</div>
 <h1 id="doc-title"></h1>
 <div class="meta">
   <span id="meta-sym"></span><span id="meta-adopted"></span><span id="meta-source"></span>
   <span class="status" id="meta-status"></span>
 </div>
</header>
<div class="layout">
 <aside id="rail"></aside>
 <main>
  <div class="tabs" role="tablist" aria-label="Views">
    <button role="tab" id="tab-0" aria-controls="panel-0" aria-selected="true">01 RESULT</button>
    <button role="tab" id="tab-1" aria-controls="panel-1" aria-selected="false" tabindex="-1">02 PARAGRAPHS</button>
    <button role="tab" id="tab-2" aria-controls="panel-2" aria-selected="false" tabindex="-1">03 LOST &amp; CHANGED</button>
    <button role="tab" id="tab-3" aria-controls="panel-3" aria-selected="false" tabindex="-1">04 CHECKS &amp; EXPORT</button>
  </div>
  <section id="panel-0" role="tabpanel" aria-labelledby="tab-0"></section>
  <section id="panel-1" role="tabpanel" aria-labelledby="tab-1" hidden></section>
  <section id="panel-2" role="tabpanel" aria-labelledby="tab-2" hidden></section>
  <section id="panel-3" role="tabpanel" aria-labelledby="tab-3" hidden></section>
 </main>
</div>
<footer id="foot"></footer>
```

Render functions fill panels. Let me write them.

renderHeader:
```js
document.getElementById('doc-title').textContent=TITLE;
var symHtml = DOC_URL ? '<a class="sym" href="'+esc(DOC_URL)+'" target="_blank" rel="noopener">'+esc(SYMBOL)+' ↗</a>' : '<span class="sym">'+esc(SYMBOL)+'</span>';
meta-sym.innerHTML=symHtml;
meta-adopted.textContent = 'adopted '+(REF&&REF.adopted?REF.adopted:'not stated');
meta-source.textContent = SOURCE;
meta-status.innerHTML = (nfail>0?'<span class="dot red"></span><span class="red">'+statusText+'</span>':'<span class="dot green"></span><span class="green">'+statusText+'</span>') + (nlimit>0?' · <span class="red">'+nlimit+' source limit'+(nlimit>1?'s':'')+'</span>':'');
```

renderRail:
```js
var shortTitle = TITLE.replace(/\s*\*$/,'');
if(shortTitle.length>110) shortTitle=shortTitle.slice(0,107)+'…';
var refP = REF&&REF.paragraphs!=null?REF.paragraphs:null;
var refF = REF&&REF.footnotes!=null?REF.footnotes:null;
var w = refP? Math.min(100, Math.round(n/refP*100)) : 100;
var bad = refP!=null && n!==refP;
rail.innerHTML =
 '<div class="rail-h code">DOCUMENT</div>'+
 '<div class="doc-card"><div class="code sym">'+esc(SYMBOL)+'</div><div class="doc-title">'+esc(shortTitle)+'</div></div>'+
 '<div class="big">'+n+' <span class="of">paragraphs of '+(refP!=null?refP:'?')+'</span></div>'+
 '<div class="bar"><i style="width:'+w+'%" class="'+(bad?'bad':'')+'"></i></div>'+
 '<div class="note code">counted from the HTML\u2019s &lt;p&gt; elements</div>'+
 '<div class="big red">0 <span class="of">footnotes of '+(refF!=null?refF:'?')+'</span></div>'+
 '<div class="note red">not in this HTML</div>'+
 '<button class="linklike" data-tab="3">'+esc(statusText)+' → tab 04</button>';
```

Hmm the rail-h uses .code (mono). Fine.

renderPanel0 (RESULT):
```js
if(!body || n===0){
  panel0.innerHTML='<p class="empty">This HTML yielded no numbered paragraphs, so there is nothing to list on tabs 02–04 and the exports are disabled.</p>';
} else {
  tiles...
}
```
Tiles:
```js
var diff = refP!=null ? n-refP : null;
var fwOk = paragraphs.filter(p=>p.fwMatch===true).length;
var tile1beside = refP!=null ? 'the document has '+refP+(diff===0?' <span class="pass">— equal</span>':' <span class="fail">('+(diff>0?'+':'')+diff+')</span>') : 'no reference in this file';
var tile2beside = (REF&&REF.first_words) ? 'of '+refP+' paragraphs match on the first six words'+(fwOk===refP?' <span class="pass">— all</span>':' <span class="fail">— '+(refP-fwOk)+' differ</span>') : 'no reference in this file';
...
panel0.innerHTML =
 '<div class="tiles">'+
 tile('PARAGRAPHS FOUND', String(n), tile1beside, 'How this is computed: every &lt;p&gt; in the HTML whose text begins with a number and a full stop, counted by this page\u2019s code.')+
 tile('FIRST WORDS MATCH', (REF&&REF.first_words)? String(fwOk):'—', tile2beside, 'How this is computed: the first six words of each paragraph, compared with the document\u2019s reference after normalising quotes, dashes and non-breaking characters; case is kept.')+
 tile('FOOTNOTES', '0', 'of '+(refF!=null?refF:'?')+' footnotes — this HTML version has none; <a href="#" data-tab="2">see tab 03</a>', 'How this is computed: the HTML contains no footnote elements; the reference counts the footnotes of the PDF and Word versions.', true)+
 tile('SPACES REPAIRED', String(allLogs.length), 'spaces restored or flagged by the four rules — <a href="#" data-tab="2">see tab 03</a>', 'How this is computed: a space is inserted only where the characters prove one was there; the text as found is kept in text_raw.', false)+
 '</div>';
function tile(label,num,beside,how,red){ return '<div class="tile"><div class="t-label code">'+esc(label)+'</div><div class="t-num'+(red?' red':'')+'">'+esc(num)+'</div><div class="t-beside">'+beside+'</div><div class="how">'+how+'</div></div>'; }
```
Note tile() defined before use — function declaration hoisted if declared with function keyword inside render scope. I'll structure carefully.

renderPanel1 (PARAGRAPHS):
```js
var headFold = '<button class="fold" aria-expanded="false" aria-controls="headings-box" id="headings-fold">Headings found: <span class="cnt">'+headings.length+'</span></button>'+
 '<div id="headings-box" hidden>'+ headings.map(h=>'<div class="hitem"><span class="code lbl">'+(h.label?esc(h.label+'.'):'')+'</span> '+esc(h.heading)+'</div>').join('') +'</div>';
var rows = paragraphs.map(function(p,i){
  var chk = p.fwMatch===null ? '<span class="muted">no reference</span>' : (p.fwMatch? '<span class="pass">OK</span>' : '<span class="fail">first words differ</span>');
  return '<tr class="prow" data-i="'+i+'"><td class="num"><button class="pbtn" aria-expanded="false" aria-controls="det-'+i+'">'+p.num+'</button></td>'+
   '<td class="sec">'+esc(p.section||'(no heading above)')+'</td>'+
   '<td class="first">'+esc(firstLine(p.text))+'</td>'+
   '<td>'+chk+'</td></tr>'+
   '<tr class="det" id="det-'+i+'" hidden><td colspan="4">'+detailHtml(p,i)+'</td></tr>';
}).join('');
panel1.innerHTML = headFold +
 '<p class="how">One row per paragraph; click a row (or its number) for the full text, the check and the citation.</p>'+
 '<table><caption><span class="tabno">TAB.02</span>'+n+' paragraphs found, '+(refP!=null?refP:'?')+' expected</caption>'+
 '<thead><tr><th scope="col" class="num">No.</th><th scope="col">Section</th><th scope="col">First line</th><th scope="col">Check</th></tr></thead>'+
 '<tbody id="ptbody">'+rows+'</tbody></table>';
```

detailHtml as sketched. firstLine:
```js
function firstLine(t){ if(t.length<=120) return t; var c=t.slice(0,120); var sp=c.lastIndexOf(' '); if(sp>60)c=c.slice(0,sp); return c+' …'; }
```

renderPanel2 (LOST & CHANGED):
```js
var ruleLine = ['sentence','comma','quote','dash'].map(k=>k+' join '+(perRuleCount[k]||0)).join(' · ');
var srows = allLogs.map(l=>'<tr class="srow" data-num="'+l.num+'" title="open para. '+l.num+' on tab 02"><td class="num">'+l.num+'</td>'+
 '<td class="code before">…'+esc(l.before)+'<b>'+esc(l.match)+'</b>'+esc(l.after)+'…</td>'+
 '<td class="code after">…'+esc(l.before)+l.parts.map(p=>p===' '?'<span class="ins"> </span>':esc(p)).join('')+esc(l.after)+'…</td>'+
 '<td>'+esc(l.label)+'</td></tr>').join('');
var charRows = [
 ['en dash (U+2013)','\u2013','–'],
 ['double quotes (U+201C, U+201D)',['\u201C','\u201D'],'“'],
 ['right single quote (U+2019)','\u2019','’'],
 ['non-breaking hyphen (U+2011)','\u2011','‑'],
 ['non-breaking space (U+00A0)','\u00A0','·']
].map(r=>{
  var ch = Array.isArray(r[1])? r[1][0] : r[1];
  var cnt = Array.isArray(r[1])? r[1].reduce((a,c)=>a+countCh(c),0) : countCh(ch);
  return '<tr><td>'+esc(r[0])+'</td><td class="num">'+cnt+'</td><td class="code ex">'+exampleFor(ch, r[2])+'</td></tr>';
}).join('');
panel2.innerHTML =
 '<section class="block"><h2>Lost: footnotes <span class="count">'+(refF!=null?refF:'?')+'</span></h2>'+
 '<p>The document has '+(refF!=null?refF:'an unknown number of')+' footnotes. This HTML has 0: no footnote text, no footnote marks, and the note the title\u2019s asterisk points to is missing. To cite a footnote, use the PDF or Word version.</p></section>'+
 '<section class="block"><h2>Changed: spaces <span class="count">'+allLogs.length+'</span></h2>'+
 '<div class="code ruleline">'+esc(ruleLine)+'</div>'+
 '<table><caption><span class="tabno">TAB.03</span>'+allLogs.length+' missing spaces restored by rule — click a row to open the paragraph on tab 02</caption>'+
 '<thead><tr><th scope="col" class="num">Paragraph</th><th scope="col">Before</th><th scope="col">After</th><th scope="col">Rule</th></tr></thead>'+
 '<tbody>'+srows+'</tbody></table>'+
 '<p class="note">Rules restore a space only where the characters prove it was there. Word pairs no rule can see — two words glued together with no punctuation between them — are not touched; the first-words check catches them only when they fall in a paragraph\u2019s first six words.</p></section>'+
 '<section class="block"><h2>Changed: characters</h2>'+
 '<table><caption><span class="tabno">TAB.04</span>special characters kept exactly as published, counted over every paragraph and heading text</caption>'+
 '<thead><tr><th scope="col">Character</th><th scope="col" class="num">Count</th><th scope="col">Example</th></tr></thead>'+
 '<tbody>'+charRows+'</tbody></table>'+
 '<div class="code hint">on a keyboard: a hyphen and straight quotes</div>'+
 '<p class="note">Kept exactly as published, in the tables and in every export. A search typed with the hyphen key will not find a non-breaking hyphen, and straight quotes will not find curly ones: normalise the text before searching it.</p></section>';
```

Wait — caption TAB numbers: tab 03 is panel index 2; I used TAB.03/TAB.04 for the two tables in tab 03 — maybe FIG numbering instead. Plan says figure numbers `FIG.01`. I'll use FIG.01.. for tables: tab02 table FIG.01, spaces table FIG.02, chars FIG.03, elements FIG.04. And tab captions "TAB.02" per plan ("a monospace number (TAB.01)"). Plan: "Every table has a serif <caption> stating the message ..., a monospace number (TAB.01)". So caption includes TAB.0x. I'll use TAB.02 for paragraphs table (it's on tab 02), TAB.03 for spaces, TAB.03b? Just use TAB.03 for both tab-03 tables? Use FIG for within-tab: I'll put `<span class="tabno">TAB.02 · FIG.01</span>`? Overkill. Keep: paragraphs table caption "TAB.02", spaces "TAB.03 · FIG.01", chars "TAB.03 · FIG.02", elements "TAB.04 · FIG.01". Fine.

renderPanel3 (CHECKS & EXPORT):
```js
var checkHtml = checks.map(function(c){
  var v;
  if(c.status==='pass') v='<span class="pass">pass</span>';
  else if(c.status==='fail') v='<span class="fail">check failed</span>'+(c.link?' <a href="#" data-tab="'+c.link.tab+'">'+esc(c.link.label)+'</a>':'');
  else if(c.status==='limit') v='<span class="fail">source limit</span>';
  else v='<span class="muted">not run</span>';
  return '<div class="check"><span class="cname code">'+esc(c.name)+'</span><span class="cdetail">'+c.detail+'</span><span class="cverdict">'+v+'</span></div>';
}).join('');
var elRows = elements.map(function(e){
  var t=e.text.length>80? e.text.slice(0,80)+' …' : e.text;
  return '<tr><td class="code">'+esc(e.tag)+'</td><td>'+esc(e.cls)+'</td><td>'+esc(t)+'</td></tr>';
}).join('');
panel3.innerHTML =
 '<h2 class="ph">Checks</h2><div class="checks">'+checkHtml+'</div>'+
 '<h2 class="ph">Export</h2>'+
 '<button class="btn" id="dl-json"'+(n===0?' disabled':'')+'>Download JSON</button>'+
 '<button class="btn" id="dl-md"'+(n===0?' disabled':'')+'>Download Markdown</button>'+
 '<p class="how">The JSON is an array of records with symbol, paragraph, section, part, text, text_raw, first_words_match, citation, doc_url and limitations. The Markdown opens with front matter (title, symbol, adopted, source_url, extracted, paragraphs_found, paragraphs_expected, footnotes), then the headings and each paragraph as its number in bold. File names use the symbol with slashes replaced by hyphens.</p>'+
 '<button class="fold" aria-expanded="false" aria-controls="elements-box">Elements found ('+elements.length+')</button>'+
 '<div id="elements-box" hidden><table><caption><span class="tabno">TAB.04 · FIG.01</span>every block element in the HTML, classified exactly once</caption>'+
 '<thead><tr><th scope="col">Tag</th><th scope="col">Classified as</th><th scope="col">Text (first 80 characters)</th></tr></thead>'+
 '<tbody>'+elRows+'</tbody></table></div>';
```

Note: check detail for repairs contains "tab 03" text — I put link separately. The detail strings I built contain plain text; I esc() them in addCheck? I passed raw strings with '·' fine; but they contain no HTML except where intended. In addCheck I stored detail as given; for check 5 detail includes 'tab 03' plain — fine. For check 3 detail esc'd. Mixed — I'll esc all details at addCheck time except where I intentionally include HTML. Simpler: store detail as plain text, esc at render, and put link separately. Check 5's detail mentions tab 03 — link param {tab:2,label:'see tab 03'}. OK adjust: addCheck('Repairs', plainDetail, 'pass', {tab:2,label:'see tab 03'}).

Then render: `'<span class="cdetail">'+esc(c.detail)+'</span>'`.

Downloads:
```js
document.getElementById('dl-json').addEventListener('click',function(){ download(SYMBOL.replace(/\//g,'-')+'.json', jsonStr, 'application/json;charset=utf-8'); });
document.getElementById('dl-md').addEventListener('click',function(){ download(SYMBOL.replace(/\//g,'-')+'.md', buildMarkdown(), 'text/markdown;charset=utf-8'); });
function download(name, content, type){
  var blob=new Blob([content],{type:type});
  var url=URL.createObjectURL(blob);
  var a=document.createElement('a'); a.href=url; a.download=name; document.body.appendChild(a); a.click(); a.remove();
  setTimeout(function(){ URL.revokeObjectURL(url); }, 2000);
}
```

Row toggling:
```js
var ptbody=document.getElementById('ptbody');
ptbody.addEventListener('click',function(e){
  var row=e.target.closest('.prow'); if(!row) return;
  setRow(row.dataset.i, undefined);
});
function setRow(i, force){
  var det=document.getElementById('det-'+i);
  var btn=ptbody.querySelector('.prow[data-i="'+i+'"] .pbtn');
  var open = force!==undefined? force : det.hidden;
  det.hidden=!open; btn.setAttribute('aria-expanded',String(open));
}
```
Wait: `det.hidden` currently true means closed; open = det.hidden (true→open). If force given use it. `var open = (force!==undefined)? force : det.hidden;` then det.hidden=!open. ✓.

openPara(num): find index; selectTab(1); setRow(i,true); scroll.

Global click delegation for [data-tab], .copy, .srow:
```js
document.addEventListener('click',function(e){
  var t=e.target;
  var dt=t.closest('[data-tab]');
  if(dt){ e.preventDefault(); selectTab(parseInt(dt.getAttribute('data-tab'),10)); return; }
  var cp=t.closest('.copy');
  if(cp){ copyText(cp.getAttribute('data-cite'), cp); return; }
  var sr=t.closest('.srow');
  if(sr){ openPara(parseInt(sr.getAttribute('data-num'),10)); }
});
```
Careful: .pbtn clicks bubble to document — no data-tab/copy/srow match, fine. But prow click handled by ptbody listener; also document listener runs — no conflict.

But wait: the rail linklike button has data-tab="3" — handled. Tile links data-tab="2" — handled.

selectTab:
```js
var tabs=Array.prototype.slice.call(document.querySelectorAll('[role="tab"]'));
function selectTab(i){
  tabs.forEach(function(t,j){
    var on=(i===j);
    t.setAttribute('aria-selected',String(on));
    t.tabIndex=on?0:-1;
    document.getElementById(t.getAttribute('aria-controls')).hidden=!on;
  });
}
tabs.forEach(function(t,i){
  t.addEventListener('click',function(){ selectTab(i); });
  t.addEventListener('keydown',function(e){
    var n=null;
    if(e.key==='ArrowRight') n=(i+1)%tabs.length;
    else if(e.key==='ArrowLeft') n=(i-1+tabs.length)%tabs.length;
    else if(e.key==='Home') n=0;
    else if(e.key==='End') n=tabs.length-1;
    if(n!==null){ e.preventDefault(); tabs[n].focus(); selectTab(n); }
  });
});
```

Folds:
```js
document.querySelectorAll('.fold').forEach(function(b){
  b.addEventListener('click',function(){
    var box=document.getElementById(b.getAttribute('aria-controls'));
    var open=box.hidden;
    box.hidden=!open;
    b.setAttribute('aria-expanded',String(open));
  });
});
```
Note: folds are rendered dynamically, so attach after rendering. I'll render everything first, then bind.

copyText as sketched.

Footer:
```js
document.getElementById('foot').innerHTML = esc(SOURCE)+(BUILT?' · built '+esc(BUILT):'')+'<br>Done by this page\u2019s code; no model was called and nothing left the browser.'+
 '<div class="credits">Sources consulted: The Turing Way, \u201CDocumentation and metadata\u201D (CC BY 4.0) · UK Government Analysis Function, \u201CQuality assurance of code for analysis and research: Testing code\u201D (Open Government Licence v3.0) · Dag Hammarskjöld Library, \u201CAsk DAG: how should I cite a UN document?\u201D</div>';
```

Order of operations in script: compute everything, render panels, then bind events (folds, downloads, delegation, tabs). Since panels rendered before binding folds — yes.

One catch: `selectTab` referenced by openPara before definition — function declaration hoisted. Use function declarations.

Also `jsonStr` used in checks (round trip) — define buildJson before checks; buildJson uses paragraphs (with text etc.) — fine after processing.

Edge: body null (no html) → blocks empty, paragraphs empty. Panels: panel0 shows empty message; panel1: headings fold with 0 + table with 0 rows — caption "0 paragraphs found". Guard: if n===0, panel1 shows message too. I'll add guards: if n===0, panel1.innerHTML = '<p class="empty">No numbered paragraphs found in this HTML.</p>'; panel2 still shows footnotes block (0 footnotes) and empty tables — fine, or message. Keep tables with 0 rows; captions say 0. OK but srows empty — fine.

Also disable exports when n===0 — done via disabled attr.

Now CSS details — write final:

```css
*{box-sizing:border-box}
[hidden]{display:none!important}
html{margin:0}
body{margin:0;background:#f4f0e8;color:#1d1b18;font:16px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
a{color:#9b2335}
code,.code{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:12px}
.code{letter-spacing:.02em}
header{padding:22px 30px 16px;border-bottom:1px solid #d9d2c3}
.kicker{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:11.5px;letter-spacing:.16em;color:#9b2335}
h1{font-family:Georgia,"Times New Roman",serif;font-weight:400;font-size:29px;line-height:1.22;margin:8px 0 10px;max-width:62ch}
.meta{display:flex;flex-wrap:wrap;gap:6px 20px;align-items:baseline;font-size:14px;color:#4a463f}
.meta .sym{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:12.5px}
.status{margin-left:auto;font-family:ui-monospace,Menlo,Consolas,monospace;font-size:11.5px;letter-spacing:.05em;display:flex;align-items:center;gap:7px}
.dot{width:9px;height:9px;border-radius:50%;display:inline-block;flex:none}
.dot.green{background:#1e6b3a}.dot.red{background:#9b2335}
.green{color:#1e6b3a}.red{color:#9b2335}
.pass{color:#1e6b3a;font-weight:600}.fail{color:#9b2335;font-weight:600}.muted{color:#8a8378}
.layout{display:flex;align-items:flex-start}
aside{flex:0 0 268px;border-right:1px solid #d9d2c3;padding:20px 22px 30px;position:sticky;top:0;max-height:100vh;overflow:auto}
main{flex:1;min-width:0;padding:20px 30px 60px}
.rail-h{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:11.5px;letter-spacing:.16em;color:#4a463f;border-bottom:1px solid #d9d2c3;padding-bottom:8px}
.doc-card{border:1px solid #d9d2c3;padding:10px 12px;margin:14px 0 6px}
.doc-card .sym{color:#9b2335;font-size:12.5px}
.doc-title{font-size:13.5px;color:#4a463f;margin-top:4px;line-height:1.4}
.big{font-family:Georgia,"Times New Roman",serif;font-size:46px;line-height:1.05;margin-top:18px}
.big .of{font-family:-apple-system,...;font-size:15px;color:#4a463f}
```
Hmm .big .of should be sans 15px — set explicitly: `.big .of{font-family:inherit... }` — inherit would be serif. Set `.big .of{font-size:15px;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;color:#4a463f}`.

```css
.bar{height:3px;background:#d9d2c3;margin:8px 0 4px}
.bar i{display:block;height:100%;background:#1e6b3a}
.bar i.bad{background:#9b2335}
.note{font-size:12.5px;margin:2px 0 0;color:#6b655b}
.note.red{color:#9b2335}
.linklike{background:none;border:none;padding:0;margin-top:20px;color:#9b2335;cursor:pointer;font:inherit;font-size:14px;text-decoration:underline;text-underline-offset:3px}
.tabs{display:flex;flex-wrap:wrap;border-bottom:1px solid #d9d2c3;margin-bottom:22px}
.tabs [role="tab"]{background:none;border:none;border-bottom:2px solid transparent;margin-bottom:-1px;padding:10px 14px 9px;cursor:pointer;font-family:ui-monospace,Menlo,Consolas,monospace;font-size:11.5px;letter-spacing:.1em;color:#4a463f}
.tabs [role="tab"]:hover{color:#1d1b18}
.tabs [role="tab"][aria-selected="true"]{color:#9b2335;border-bottom-color:#9b2335}
:focus-visible{outline:2px solid #9b2335;outline-offset:2px}
.tiles{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:1px;background:#d9d2c3;border:1px solid #d9d2c3}
.tile{background:#f4f0e8;padding:16px 18px 14px}
.t-label{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:11px;letter-spacing:.14em;color:#4a463f}
.t-num{font-family:Georgia,"Times New Roman",serif;font-size:54px;line-height:1;margin:10px 0 6px}
.t-beside{font-size:14px;color:#4a463f}
.how{font-size:12.5px;color:#6b655b;margin-top:12px;border-top:1px solid #d9d2c3;padding-top:8px;line-height:1.45}
table{border-collapse:collapse;width:100%;margin:8px 0 24px}
caption{text-align:left;font-family:Georgia,"Times New Roman",serif;font-size:19px;line-height:1.3;padding:4px 0 10px;max-width:70ch}
.tabno{display:block;font-family:ui-monospace,Menlo,Consolas,monospace;font-size:11px;letter-spacing:.14em;color:#9b2335;margin-bottom:5px}
th{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:10.5px;letter-spacing:.12em;text-transform:uppercase;font-weight:400;color:#4a463f;text-align:left;border-bottom:1px solid #1d1b18;padding:6px 12px 6px 0}
td{border-bottom:1px solid #d9d2c3;padding:8px 12px 8px 0;vertical-align:top;font-size:15px}
th.num,td.num{text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap}
.prow{cursor:pointer}
.prow:hover td{background:#ece5d6}
.pbtn{background:none;border:none;padding:0 2px;font:inherit;font-weight:600;color:#9b2335;cursor:pointer;font-variant-numeric:tabular-nums}
.det td{background:#efe9db;padding:14px 18px 16px}
.sec{max-width:220px}
.first{max-width:420px;color:#3d3a34}
.path{color:#6b655b;margin-bottom:10px}
.full{max-width:78ch;margin:0 0 12px;font-size:15.5px}
.repair{box-shadow:inset 0 0 0 1px #9b2335}
.ins{box-shadow:inset 0 0 0 1px #9b2335}
.chmark{box-shadow:inset 0 0 0 1px #9b2335;padding:0 1px}
.fwline{font-size:13.5px;color:#4a463f;margin-bottom:10px}
.reps{font-size:13px;color:#4a463f;margin-bottom:12px}
.reps ul{margin:6px 0 0;padding-left:18px}
.cite-row{display:flex;align-items:center;gap:12px;flex-wrap:wrap}
.copy{background:none;border:1px solid #9b2335;color:#9b2335;padding:6px 12px;cursor:pointer;font:inherit;font-size:13.5px}
.copy.copied{background:#9b2335;color:#f4f0e8}
.fold{display:block;background:none;border:none;border-bottom:1px solid #d9d2c3;width:100%;text-align:left;padding:12px 2px;cursor:pointer;font-family:Georgia,"Times New Roman",serif;font-size:19px;color:#1d1b18}
.fold .cnt{color:#9b2335}
#headings-box,#elements-box{border:1px solid #d9d2c3;border-top:none;padding:10px 16px;margin-bottom:22px}
.hitem{padding:3px 0;font-size:14.5px;border-bottom:1px dotted #d9d2c3}
.hitem .lbl{color:#9b2335;display:inline-block;min-width:34px}
.block h2{font-family:Georgia,"Times New Roman",serif;font-weight:400;font-size:25px;margin:30px 0 10px}
.block h2 .count{color:#9b2335}
.ruleline{color:#4a463f;margin:0 0 6px}
.srow{cursor:pointer}
.srow:hover td{background:#ece5d6}
.before,.after{max-width:360px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;font-size:11.5px}
.ex{font-size:12px}
.hint{color:#6b655b;margin:2px 0 8px}
.ph{font-family:Georgia,"Times New Roman",serif;font-weight:400;font-size:25px;margin:26px 0 10px}
.check{display:flex;gap:14px;flex-wrap:wrap;padding:10px 0;border-bottom:1px solid #d9d2c3;font-size:14.5px;align-items:baseline}
.cname{min-width:160px;color:#4a463f;letter-spacing:.1em;font-size:11px;text-transform:uppercase}
.cdetail{flex:1;min-width:260px}
.cverdict{white-space:nowrap}
.btn{background:#1d1b18;color:#f4f0e8;border:none;padding:11px 18px;cursor:pointer;font:inherit;font-size:14.5px;margin:0 10px 10px 0}
.btn:hover{background:#000}
.btn:disabled{opacity:.35;cursor:not-allowed}
.empty{font-size:17px;max-width:60ch;padding:20px 0}
footer{border-top:1px solid #d9d2c3;padding:16px 30px 30px;font-size:13.5px;color:#4a463f}
.credits{margin-top:8px;font-size:12px;color:#8a8378;max-width:90ch}
@media (max-width:900px){ .layout{flex-direction:column} aside{position:static;max-height:none;width:100%;flex:none;border-right:none;border-bottom:1px solid #d9d2c3} }
```

Also `.big.red` — red color for the 0 footnotes number: `.big.red{color:#9b2335}`.

Now, one more check on plan details I might have missed:

- "At the right a green dot 'n of m checks pass' or a red dot 'n checks failed', then '1 source limit' (the footnotes)." ✓ header status.
- Rail: "Then 'n of m checks pass', linking to tab 04." ✓.
- Tab 01 tile 1: "Paragraphs found: n beside the document has reference.paragraphs (green when equal, red with the difference)" ✓.
- Tab 02: "A closed 'Headings found: n' box above the table lists them" ✓.
- Expanded row: "the full text, verbatim, never shortened; the reference's six words beside the found six; the places repaired or flagged in this paragraph; and a Copy citation button that copies 'symbol, para. n' and shows 'Copied' for two seconds; the same string is the citation field of every export." ✓.
- Tab 03 blocks ✓. "clicking a row opens the paragraph on tab 02" ✓.
- Tab 04: check panel open, every check one line ✓; Export two buttons ✓; JSON fields ✓; Markdown front matter ✓; file names ✓; closed "Elements found (n)" ✓.
- Footer ✓.
- Checks list ✓ (8 checks).
- Edge cases ✓.

One more: "Rows are buttons with aria-expanded" — my pbtn has aria-expanded ✓; row click also toggles. Good enough.

"Details open in place (a clicked row expands)" ✓.

Header label: "UN DOCUMENT · HTML" ✓.

Also plan: tab 02 "Check: 'OK' or 'first words differ' (red)" ✓.

Now — the intro sentences before the code block (max 3 short sentences): "I built the paragraph extractor for the attached CESCR General Comment No. 27 HTML: it parses the HTML, finds the 90 numbered paragraphs under their headings, checks them against the document's reference, lists what the HTML lost (the footnotes) and changed (missing spaces, special characters), and exports JSON or Markdown. Everything is computed on load by the page's own code — no model was called."

Wait — don't hard-code "90" in my message? The rule says never hard-code counts in the app; my prose can mention what the plan said but safer to avoid specific numbers: "finds the numbered paragraphs under their headings…". Keep generic.

Now let me also double-check the `parts` for quote rule: match "s“" (letter + curly open quote). parts [m[1], ' ', '“'] → "s “". ✓. But what about closing quote joins like `”word`? Plan only lists opening. Fine.

Dash rule: match "–t" → "– t". But what about "word–word" (dash between letters, no spaces)? Plan: "after an en dash touching a letter (/–([A-Za-z])/g)" — only after. "challenges –to" has space before. OK.

Sentence rule `([a-z])\.([A-Z])` — could match inside abbreviations like "e.g.Example"? Would insert space — per plan, that's the rule. Fine.

One risk: sentence rule could match across a repaired boundary? Sequential — fine.

Also: could the sentence rule match something in a number like "art. 6"? "art. 6" — after '.' is space, not [A-Z]. "art.6"? would match "t.6"? No — [A-Z] uppercase only; "6" not. OK. What about "No.27"? "o.2" no. Fine.

Now, `firstSix` on `p.text` — text after repairs. Reference first_words presumably from clean text. Repairs in first six words would help match. OK.

Potential issue: REF.first_words keys — "keyed by the paragraph number as a string". ✓ String(p.num).

Now write detailHtml fully:

```js
function detailHtml(p,i){
  var path = p.path.length ? p.path.map(function(h){return esc(dispH(h));}).join(' \u203A ') : '(no heading above)';
  var fw = p.fwMatch===null ? '<span class="muted">no reference in this file</span>'
    : '<span class="code">FOUND</span> \u201C'+esc(p.first6)+'\u201D &nbsp;\u00B7&nbsp; <span class="code">REFERENCE</span> \u201C'+esc(p.ref6)+'\u201D';
  var reps = p.logs.length
    ? '<div class="reps"><span class="code">REPAIRED HERE</span><ul>'+p.logs.map(function(l){
        return '<li>'+esc(l.label)+': \u2026'+esc(l.before)+'<b>'+esc(l.match)+'</b>'+esc(l.after)+'\u2026</li>';
      }).join('')+'</ul></div>'
    : '<div class="reps muted">no space repaired in this paragraph</div>';
  var link = DOC_URL ? ' <a href="'+esc(DOC_URL)+'" target="_blank" rel="noopener">'+esc(SYMBOL)+' \u2197</a>' : '';
  return '<div class="path code">'+path+'</div>'+
    '<p class="full">'+p.html+'</p>'+
    '<div class="fwline">'+fw+'</div>'+
    reps+
    '<div class="cite-row"><button class="copy" data-cite="'+esc(p.citation)+'">Copy citation</button><span class="code">'+esc(p.citation)+'</span>'+link+'</div>';
}
```

Note: p.html contains esc'd text with repair spans — safe.

Now, "the places repaired or flagged in this paragraph" — logs show before/match/after. ✓.

Let me also make sure the tab-02 table's Section column shows nearest heading — p.section set at classification. ✓.

Potential issue: `p.path` — I set path at classification time as curPath.slice() — but curPath at that moment includes headings up to current. ✓. But note: for paragraphs before any h2, path empty.

`part` — curPart at classification. ✓.

Now assemble the final document. Also add `<meta name="color-scheme" content="light">`? Not needed.

Let me also handle the case where `WORKSHOP_DATA.html_doc` is missing entirely: D={}, html='' → body null → blocks [] → n=0 → panel0 empty message; header shows title '(untitled document)'. Acceptable.

Also — the sample shows html_doc possibly as array; handled.

Double-check the round-trip check when n===0: jsonStr='[]' → back.length 0 === 0 → pass. But if body null, maybe 'notrun' better; keep pass, harmless. Actually if no html at all, exports disabled; check says pass 0=0 — slightly odd but fine. I'll make it: if(!body){ status 'notrun', detail 'no HTML in this file' }.

Let me now also think about `elements` text for the elements table: e.text is collapsed textContent — for the table element, textContent includes all cover text concatenated — fine, first 80 chars.

One more plan item: tab 04 "The check panel (next section but one), open, every check on one line." ✓.

"Under the buttons a closed heading 'Elements found (n)'" ✓.

Also plan: header "one line with the data's source, n and years" — that's the generic workshop header spec; here the plan overrides: symbol link, adopted, source. I'll also include n: "n paragraphs" maybe in meta. I'll add `<span>90 paragraphs in this HTML</span>`? The rail covers it. I'll add to meta: `${n} paragraphs · ${refF} footnotes in the PDF/Word versions`? Keep meta as plan says: symbol, adopted, source. Add n: I'll include "n paragraphs extracted" in meta line. Fine.

Now, writing everything out. Also ensure no `fetch`, no external. Chart.js unused — fine.

Let me write the complete final HTML now, carefully, keeping it under ~1500 lines (it'll be ~600).

One more consideration on the `while((m=r.re.exec(text))!==null)` loop with manual lastIndex: after a match, I set `r.re.lastIndex=last` where last=m.index+m[0].length — this equals what exec would set anyway (since match non-empty). The zero-length guard unnecessary but harmless. Actually there's a subtle bug: I set `r.re.lastIndex=last` inside loop after using m — exec already advanced lastIndex to m.index+m[0].length; setting again same. Fine. But if a match is zero-length (impossible here), guard prevents infinite loop. Keep.

Also in the replay loop, `cur` must be the text at the start of rule ri — I update cur after each rule using the same ms. ✓.

Let me also verify: in processParagraph, `perRule.push(ms)` after building out — ms collected on the pre-rule text. ✓.

Now the copy fallback: `document.execCommand` deprecated but works. Fine.

Writing final answer now. Also remember: after the code block, nothing. Before: ≤3 sentences.

Let me write out the code in full.

Additional detail — `selectTab` initial: panel 0 visible, others hidden in markup. ✓.

`openPara`:
```js
function openPara(num){
  var i=-1;
  for(var j=0;j<paragraphs.length;j++){ if(paragraphs[j].num===num){ i=j; break; } }
  if(i<0) return;
  selectTab(1);
  setRow(i,true);
  var det=document.getElementById('det-'+i);
  if(det) det.scrollIntoView({block:'center'});
}
```

setRow defined:
```js
function setRow(i,force){
  var det=document.getElementById('det-'+i);
  var btn=document.querySelector('.prow[data-i="'+i+'"] .pbtn');
  if(!det||!btn) return;
  var open=(force!==undefined)?force:det.hidden;
  det.hidden=!open;
  btn.setAttribute('aria-expanded',String(open));
}
```

ptbody click:
```js
var ptbody=document.getElementById('ptbody');
if(ptbody){ ptbody.addEventListener('click',function(e){ var row=e.target.closest('.prow'); if(row) setRow(row.getAttribute('data-i')); }); }
```

Note: clicking the pbtn triggers click → bubbles to tr → ptbody handler toggles once. ✓ (button click doesn't double-fire since only one handler).

Folds binding after render:
```js
Array.prototype.forEach.call(document.querySelectorAll('.fold'),function(b){
  b.addEventListener('click',function(){
    var box=document.getElementById(b.getAttribute('aria-controls'));
    if(!box) return;
    var open=box.hidden;
    box.hidden=!open;
    b.setAttribute('aria-expanded',String(open));
  });
});
```

Downloads binding after render.

Global delegation for data-tab/copy/srow.

OK — also the tile function: define before use.

Let me finalize the panel0 render:

```js
function renderPanel0(){
  var p0=document.getElementById('panel-0');
  if(!body || paragraphs.length===0){
    p0.innerHTML='<p class="empty">This HTML yielded no numbered paragraphs, so tabs 02\u201304 have nothing to list and the exports are disabled.</p>';
    return;
  }
  var refP=(REF&&REF.paragraphs!=null)?REF.paragraphs:null;
  var refF=(REF&&REF.footnotes!=null)?REF.footnotes:null;
  var diff=refP!=null?paragraphs.length-refP:null;
  var fwOk=paragraphs.filter(function(p){return p.fwMatch===true;}).length;
  var hasFw=!!(REF&&REF.first_words);
  function tile(label,num,beside,how,red){
    return '<div class="tile"><div class="t-label">'+esc(label)+'</div>'+
      '<div class="t-num'+(red?' red':'')+'">'+esc(num)+'</div>'+
      '<div class="t-beside">'+beside+'</div>'+
      '<div class="how">'+how+'</div></div>';
  }
  var b1 = refP!=null
    ? 'the document has '+refP+(diff===0?' <span class="pass">\u2014 equal</span>':' <span class="fail">('+(diff>0?'+':'')+diff+')</span>')
    : 'no reference in this file';
  var b2 = hasFw
    ? 'of '+refP+' paragraphs match on the first six words'+(fwOk===refP?' <span class="pass">\u2014 all</span>':' <span class="fail">\u2014 '+(refP-fwOk)+' differ</span>')
    : 'no reference in this file';
  var b3 = 'of '+(refF!=null?refF:'?')+' footnotes \u2014 this HTML version has none; <a href="#" data-tab="2">see tab 03</a>';
  var b4 = 'spaces restored or flagged by the four rules \u2014 <a href="#" data-tab="2">see tab 03</a>';
  p0.innerHTML='<div class="tiles">'+
    tile('PARAGRAPHS FOUND',String(paragraphs.length),b1,'How this is computed: every &lt;p&gt; in the HTML whose text begins with a number and a full stop, counted by this page\u2019s code.')+
    tile('FIRST WORDS MATCH',hasFw?String(fwOk):'\u2014',b2,'How this is computed: the first six words of each paragraph, compared with the document\u2019s reference after normalising quotes, dashes and non-breaking characters; case is kept.')+
    tile('FOOTNOTES','0',b3,'How this is computed: the HTML contains no footnote elements; the reference counts the footnotes of the PDF and Word versions.',true)+
    tile('SPACES REPAIRED',String(allLogs.length),b4,'How this is computed: a space is inserted only where the characters prove one was there; the text as found is kept in text_raw.')+
    '</div>';
}
```

Note: tile labels use .t-label with uppercase via CSS text-transform? I set letter-spacing; add text-transform:uppercase in .t-label. The label text already uppercase.

OK. Also panel1 guard when n===0.

Now finalize everything into the answer. Also double-check: "no view shows more than about seven things to click" — tab01: 4 tabs + 2 links = 6 ✓.

Also the plan wants tab names exactly: `01 RESULT · 02 PARAGRAPHS · 03 LOST & CHANGED · 04 CHECKS & EXPORT` — I'll use "01 RESULT", "02 PARAGRAPHS", "03 LOST & CHANGED", "04 CHECKS & EXPORT" (the · is separator in plan). Fine.

Write it all out now. I'll be careful with quotes inside template strings — I'm using string concatenation with single quotes and escaping. In the JS I'll use single-quoted strings with \u2019 etc. for typographic chars to avoid encoding issues — actually UTF-8 charset is declared, so literal ’ etc. are fine. I'll use literals sparingly; safer to use \u escapes in JS strings for special chars. In HTML text nodes I can use literal characters since charset utf-8. I'll use literals like ’ — fine.

Let me write the final file.

Also one more: the plan says tab 02 table columns "No. | Section | First line | Check" ✓.

And "Headings found: n" box lists them "so none can hide inside a paragraph" ✓.

Final check on line count — fine.

Write the answer.