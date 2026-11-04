Build the app per the detailed plan. One HTML file, two tabs, header, rail, checks, exports. Let me write carefully but compactly.

Key data: WORKSHOP_DATA.html_doc: {title, symbol, doc_url, source, html, reference}.

Pipeline:
- parse html
- iterate body elements in order; first table = cover, skip. Classify h2/h3/p.
- paragraph regex /^(\d{1,3})\.\s*(.*)$/s
- heading split /^([IVX]+|[A-Z])\.\s*(.+)$/
- repairs with logging (20 chars each side).
- first words check with normalization.
- checks list.
- exports JSON/Markdown blobs.

Design per studio style. Tabs 01/02, arrow keys. Check panel closed. Spaces table closed. Paragraph rows expandable with copy citation.

Write code. Keep under ~1500 lines. Use system fonts, colors #f4f0e8 etc, red #9b2335, green pass dark green (#2a6b3c say, contrast ok).

Let me draft.

Structure:
- header: monospace label "UN DOCUMENT · HTML", title serif, line: symbol link, adopted, source. Right: dot + "n of m checks pass", "1 source limit".
- rail: card symbol + short title (use title or symbol? "short title" — use title truncated? Plan says symbol + short title; no short_title field, use title maybe shortened). Big numbers: paragraphs found of expected with bar; footnotes 0 of N red "not in this HTML"; "n of m checks pass".
- tabs.

Tab 01: four tiles, mismatch list, export buttons, two closed headings (Every check, spaces restored).

Tab 02: closed "Headings found: n" box, table of paragraphs, expandable rows.

Checks array: each {name, status: pass/fail/source-limit/not-run, found, expected, detail}.

Checks:
1. Paragraph count: found vs reference.paragraphs.
2. Numbering: 1..n in order, gaps/dups.
3. First words: mismatches.
4. Footnotes: 0 vs reference.footnotes → source limit.
5. Repairs: count.
6. Headings: count + glued labels separated.
7. Nothing lost: classification totals sum.
8. Export round trip: parse JSON back, count equals.

Pass count: checks with status pass; failed; source-limit counted separately.

Export round trip: build JSON string, JSON.parse, compare length. Do at build time on button? Plan says check panel includes it; run once on load.

Repairs marking in expanded paragraph: wrap inserted space in a span with thin red box. Easiest: when rendering expanded text, re-apply repairs to text_raw while capturing positions, or build text from text_raw by inserting markers. I'll re-run regexes building HTML with <mark> around inserted space.

Approach: function repairToHtml(raw) returns html with escaped text and inserted spaces wrapped in `<span class="rep"> </span>`. Apply rules sequentially with a combined pass? Rules applied sequentially on string; for marking, I'll do it in one pass over text with a combined regex: /([a-z])\.([A-Z])|([a-z]),([A-Za-z])|([a-z])“|–([A-Za-z])/g and insert " " between groups. But sequential application on raw differs? E.g. "x.–A": dash rule after comma rule... Combined single pass could differ from sequential when patterns overlap. Rules: comma rule inserts after comma; dash rule inserts after en dash before letter; quote rule inserts before “ after lowercase letter. Overlaps unlikely. Accept single pass for both text and marked html to stay consistent: build text and html in one loop. Actually plan says sequential regexes; differences negligible. I'll do combined single pass for text too, and verify counts similar. Fine.

Simpler: apply repairs sequentially to get text and count log; separately render marked version with combined pass. Could produce inconsistency in rare overlap but acceptable? Risky. I'll just do single combined pass everywhere and log rule names per match.

Rules: for match m:
- if groups [a-z]\.[A-Z]: rule "sentence join"
- ([a-z]),([A-Za-z]): "comma join"
- ([a-z])“ : "quote join"
- –([A-Za-z]): "dash join"

Spaces restored count = number of insertions.

First-words normalization: curly quotes straight (replace “”‘’ with " and '), en dash – and non-breaking hyphen ‑ → -, nbsp → space.

Mismatch list on tab 01: para n: found "first six words" / reference.

Copy citation: navigator.clipboard, fallback textarea. Show "Copied" 2s.

Tabs arrow key nav, role tablist. Hidden panels with [hidden] and CSS rule.

Tiles: green when equal. green: #1e6b3a maybe; use class.

Bar: thin div, width % = min(found/expected*100,100), red when !=.

Export JSON: records with fields per plan. limitations string: "no footnotes in this HTML version; the document has N".

Markdown: front matter --- lines with title, symbol, adopted, source_url, extracted date, paragraphs_found, paragraphs_expected, footnotes sentence. Then headings as ## for h2 (roman/part) and ### for h3? Plan: "the headings as ## and ### lines in document order and each paragraph as its number in bold, then its text." I'll track document order elements; export sequence: for each heading (h2 → "## label. heading", h3 → "### label. heading"), paragraphs as "**n.** text". Include title at top? Front matter has title; add "# title" maybe. Keep simple: front matter, then "# {title}", then headings/paragraphs.

File name: symbol.replace(/\//g,'-') + '.json'/'.md'.

Check "nothing lost": count block elements after cover table: paragraphs classified + headings + title + committee line; unclassified list. Total elements considered = body direct children (and nested? "the parsed document's body elements in order" — I'll iterate body.querySelectorAll('*')? Simpler: body.children plus... The HTML has table (with nested), div.content with children. I'll iterate over all descendant elements that are p/h2/h3 plus track others. Classify each element in content div plus stray ones. Let me define: walk all elements inside body that are h2, h3, p, or table; table first = cover. Other element types (div, span, img, td, tr) skipped as containers — but "nothing lost" check: classify block-level elements. I'll define blocks = body.querySelectorAll('p, h2, h3, table, li, ul, ol, blockquote'); classify each; count per class; sum equals total blocks. Good enough.

Edge: if no reference fields → tiles say "no reference in this file", checks "not run".

Header right: green dot with "n of m checks pass" or red dot "n checks failed"; plus "1 source limit". Compute: failures>0 → red dot "n checks failed"; else green dot "n of m checks pass". m = number of run checks? Plan: "n of m checks pass". I'll use m = checks that ran (exclude not-run), and show source limit separately.

Let me now write the file. Aim ~700 lines.

Rail "short title": use title but truncated? I'll show full title small. Fine.

Tab 02 table: columns No. | Section | First line | Check. Rows: a button row (tr? Buttons inside tr are awkward). Use table with rows where first cell contains... Plan: "Rows are buttons with aria-expanded". I'll make each row a <tr> with tabindex 0 role button aria-expanded, click/Enter toggles an extra detail <tr>. Simpler and accessible enough. Actually focusable tr works.

Headings box on tab 02: closed heading button listing h2/h3 headings found.

Expanded row: full text with marked repairs, reference six words vs found six words, copy citation button. Button inside tr — put inside a td colspan.

Space restored table on tab 01: Paragraph | Before | After | Rule with count per rule above; clicking row opens paragraph on tab 02 (switch tab, expand that paragraph, scroll).

Let me code.

Colors: paper #f4f0e8, ink #1d1b18, rule #d9d2c3, red #9b2335, green #1e6b34.

Write JS:

```js
const D = WORKSHOP_DATA.html_doc;
const ref = D.reference || {};
const doc = new DOMParser().parseFromString(D.html, 'text/html');
const body = doc.body;
const paras = [], headings = []; // headings: {level,label,headingText,glued,el}
let titleEl=null, committeeLine=null, coverSeen=false, unclassified=[];
let seq = []; // document-order items {type:'heading'|'para', ...}
body.querySelectorAll('p,h2,h3,table,li,ul,ol,blockquote').forEach(el=>{ ... })
```

Careful: nested elements (p inside table cells, etc.) — querySelectorAll('p') includes cover table's <p> elements. Cover: elements inside the first table. I'll skip elements whose closest('table') is the first table. Get first table: body.querySelector('table').

Iterate all block elements: skip if inside cover table. Classify:
- P: if /^(\d{1,3})\.\s*([\s\S]*)$/ → paragraph. else committee line (first non-number p).
- H2: first h2 → title; else heading.
- H3: heading.
- other (li, ul, ol, blockquote, table beyond first): unclassified.

Heading split: /^([IVX]+|[A-Z])\.\s*(.+)$/ — glued labels "I.Introduction": no space after dot, \s* handles.

Current section tracking while iterating in document order (querySelectorAll returns document order). Maintain curH3 (nearest heading) and curPart (nearest roman h2).

Paragraph object: {number, text_raw, text, repairs:[], section, part, firstMatch, foundWords, refWords, el}.

Repairs: combined regex over text_raw:

```js
const RULES = [
 {re:/([a-z])\.([A-Z])/g, rule:'sentence join', ...}
];
```

Single combined regex:
```js
const rx = /([a-z])\.([A-Z])|([a-z]),([A-Za-z])|([a-z])“|–([A-Za-z])/g;
```
For each match determine insertion point and context. Build text and html:
```js
function repair(raw){
  let out='', last=0, m, log=[];
  rx.lastIndex=0;
  while((m=rx.exec(raw))){
    let idx, rule;
    if(m[1]!==undefined){ idx=m.index+1; rule='sentence join'; }
    else if(m[3]!==undefined){ idx=m.index+1; rule='comma join'; }
    else if(m[5]!==undefined){ idx=m.index+1; rule='quote join'; }
    else { idx=m.index; rule='dash join'; }
    out += raw.slice(last, idx) + ' ' ;
    log.push({rule, before: raw.slice(Math.max(0,idx-20), idx), after: raw.slice(idx, idx+20)});
    last = idx;
  }
  out += raw.slice(last);
  return {text:out, log};
}
```
Wait: insertion for sentence join is after the ".", i.e., between m[1] and m[2] → index m.index+1. Comma: after comma → m.index+1. Quote: before “ after lowercase letter → index m.index+1 (after the letter). Dash: after en dash before letter → insert before the letter: index m.index (start of match is "–", insert after dash = m.index+1). Let me redo: dash rule /–([A-Za-z])/ inserts space after the en dash: between – and letter → idx = m.index+1. All insertions at m.index+1 then. Quote rule /([a-z])“/ inserts before “ : between letter and quote → idx = m.index+1. Yes all m.index+1.

Marked html: escape raw, but easier: build marked from same loop: outHtml += esc(raw.slice(last, idx)) + '<span class="rep"> </span>'.

But careful: quote join rule inserts space between lowercase and “, but m[2] group would be undefined. Fine.

Also there's rule "before an opening curly quote touching a letter" — only lowercase before? Plan: `/([a-z])“/g`. OK.

First words:
```js
function norm(s){return s.replace(/[“”]/g,'"').replace(/[‘’]/g,"'").replace(/[–]/g,'-').replace(/\u2011/g,'-').replace(/\u00a0/g,' ');}
```
foundWords = text.split(/\s+/).slice(0,6); refWords = ref.first_words[String(n)].

Checks:
```js
checks = [
 {name:'Paragraph count', ...},
 numbering,
 firstwords,
 footnotes (source limit),
 repairs,
 headings,
 nothingLost,
 roundtrip
];
```
Numbering: expected 1..found.length in order; check sorted numbers equal sequence; gaps/dups listed. Status pass if numbers are exactly 1..n ascending unique.

Roundtrip: build records array, JSON.parse(JSON.stringify(records)) length === paras.length → pass. Trivially true but that's the check.

Not-run handling when ref missing.

Now render. I'll write functions renderResult(), renderParagraphs(), etc.

Tabs: buttons with role tab, panels. Arrow keys.

Copy: 
```js
function copyCite(btn, n){ const s = `${D.symbol}, para. ${n}`; navigator.clipboard?.writeText(s).catch(()=>fallback).then... }
```
Fallback with textarea + execCommand.

Export downloads via Blob.

Go to tab 02 from spaces table: switch tab, expand row (set expanded), scrollIntoView.

OK, write it. Keep explanations in app text.

The mismatch list under tiles: paras where !firstMatch, "para. n: found <six words> / reference <refWords>". max 10 lines.

Tiles: paragraphs found / expected (green equal, red diff), first words match n of N, footnotes 0 of N red, spaces n in n paragraphs.

Rail numbers: big serif.

Header right: dot span. Compute passN, failN, limitN (footnote check). limit = checks with status 'limit'.

Headings check detail: "n <h2> and <h3> headings; m glued labels separated" — count glued = headings whose raw text matched label without space? "glued" means original text like "I.Introduction" (no space after label). Detect: raw label match where char after '.' is not whitespace. Store heading.raw.

Nothing lost: counts per class + unclassified list; pass if none unclassified.

Alright, writing the HTML now. Also caption per table, FIG/TAB numbering monospace.

Table 01 paragraphs: caption "90 paragraphs found, 90 expected" etc.

Let me write final code, moderately concise CSS.