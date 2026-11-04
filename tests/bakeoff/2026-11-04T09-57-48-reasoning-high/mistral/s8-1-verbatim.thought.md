Let me plan this app carefully. The user wants a complete HTML app for searching General Comments verbatim. I need to build one complete HTML file, under ~1500 lines, using window.WORKSHOP_DATA.gc, Chart.js preloaded.

Key features:
- Header with label, title, source line, checks pass/fail indicator
- Left rail filters: big count, search box with syntax help + examples, committee checkboxes with hits, year range, document select, chips
- Tabs: 01 Overview (chart FIG.01), 02 Paragraphs (results list, 25/page, highlight, copy citation/quotation, add to draft, context), 03 Draft (collected quotes, copy all, download txt/csv), 04 Check & method (self-checks, quirks, method)
- Query parser: Boolean with AND/OR/NOT, quotes phrases, parens, trailing *, leading -, implicit AND, precedence NOT > AND > OR
- Normalization: remove [[fn:N]], curly→straight quotes, dashes→hyphen, whitespace→space, lowercase
- Term matching with regex over norm with unicode boundaries
- Highlight over shown text with flexible quote/dash/fn matching
- Citations: symbol + pinpoint; shared symbols get committee + doc name prefix
- Checks panel
- localStorage for draft with memory fallback
- Clipboard with fallback

Let me write the code carefully.

Data: WORKSHOP_DATA.gc = {title, source, source_url?, built, count, records}. Wait — the description says gc has {title, source, count, records}. Does it have source_url and built? The uhri has source_url and built. The gc description: `{title, source, count, records: [...]}`. Hmm, header says "source linked to source_url" and footer "source and built". I should handle missing gracefully: use `gc.source_url` if present, else just source text; `gc.built` if present. I'll write defensively: `const SRC = D.source || ''`, `const SRC_URL = D.source_url || ''`, `const BUILT = D.built || ''`.

Records fields: id, symbol, paragraph, committee, year, title, short_title, doc_url, text, cited_articles.

Precompute per record:
- norm: normalized text
- marks: count of [[fn:N]]
- shown: text with fn marks removed
- leading: match ^(\d{1,3})\.\s on text
- pinpoint: paragraph===0 → "preamble"; text starts with ^\(([a-z]{1,4})\) → "subpara. (b)"; else "para. N"
- lettered: boolean
- citation: if shared symbol (symbol maps to >1 title) → `${committee}, ${docName} (${symbol}), ${pinpoint}` else `${symbol}, ${pinpoint}`. docName = title up to first colon or " on ". Hmm "title up to the first colon or ' on '". E.g. "General Comment No. 01: Implementation of article 3..." → "General Comment No. 01". For "General Recommendation No. 34: Racial discrimination..." → "General Recommendation No. 34". Take min index of ":" and " on " whichever comes first.
- shared: symbolToTitles count > 1
- joint: symbol contains two committee codes (en dash or comma) — detect via regex finding 2+ codes in symbol
- committees: codes found in symbol via regex \b(CAT|CCPR|CED|CEDAW|CERD|CESCR|CMW|CRC|CRPD)\b plus "CAT-OP" for CAT/OP, plus committee field. Note CEDAW and CED both? CED is Committee on Enforced Disappearance. CEDAW is the women's committee. The regex includes both CED and CEDAW — \bCED\b won't match inside CEDAW because \b after D... "CEDAW" — \bCED\b requires boundary after D, but next char is A (word char), so no match. Good. CAT-OP: symbol like "CAT/OP/..." — \bCAT\b would match CAT in "CAT/OP" since "/" is a boundary. So need to handle: if symbol contains "CAT/OP", use "CAT-OP" instead of "CAT". I'll do: find all matches of /(CAT\/OP|CAT|CCPR|CEDAW|CED|CERD|CESCR|CMW|CRC|CRPD)\b/g... careful ordering: CAT/OP before CAT. Actually simpler: replace "CAT/OP" with "CAT-OP" in a copy, then regex \b(CAT-OP|CCPR|CEDAW|CED|CERD|CESCR|CMW|CRC|CRPD)\b. Hmm \b with hyphen: "CAT-OP" — \bCAT-OP\b: boundary before C ok, after P ok. But \b between T and -? The regex \b(CAT-OP|...)\b matches the whole "CAT-OP" as a token since - is non-word... Actually \b is between word and non-word. In "CAT-OP", positions: C-A-T are word chars, "-" non-word, O-P word. \bCAT-OP\b would try to match "CAT-OP" literally: \b before C (start or after non-word) ok; then literal "CAT-OP"; then \b after P ok. Yes it matches the full string including hyphen. Good.

Committee full names: I need a map. 10 committee codes: CAT, CCPR, CED, CEDAW, CERD, CESCR, CMW, CRC, CRPD, CAT-OP. Full names:
- CAT: Committee against Torture
- CAT-OP: Subcommittee on Prevention of Torture (SPT)
- CCPR: Human Rights Committee
- CED: Committee on Enforced Disappearances
- CEDAW: Committee on the Elimination of Discrimination against Women
- CERD: Committee on the Elimination of Racial Discrimination
- CESCR: Committee on Economic, Social and Cultural Rights
- CMW: Committee on Migrant Workers
- CRC: Committee on the Rights of the Child
- CRPD: Committee on the Rights of Persons with Disabilities

I'll include a map with fallback to the code itself if unknown.

Query parser:
Tokens: scan string. Handle curly quotes “ ” as phrase delimiters too. Tokens: '(' ')' 'AND' 'OR' 'NOT' (capitals only), '-' prefix as NOT, quoted phrase, word (run of non-space, non-paren chars?) — words can contain hyphens etc. Let's tokenize: iterate chars; skip whitespace; if char is '(' or ')' → token; if '"' or '“' or '”'... phrase: opening quote (straight " or curly “), read until matching closing (straight " or curly ”), if none → error "unbalanced quote". If starts with '-' followed by non-space → NOT token then continue with rest as term? A leading minus as NOT: "-torture" → NOT word torture. I'll treat '-' at start of a term as NOT operator applied to the following term. Simpler: when encountering '-', emit NOT token, continue. Then word: run of chars until whitespace or paren or quote. Word may end with '*'.

Grammar: expr := orExpr; orExpr := andExpr (OR andExpr)*; andExpr := notExpr (AND? notExpr)* — implicit AND when next token is a term/NOT/'(' ; notExpr := NOT notExpr | primary; primary := '(' expr ')' | term.

Term: {type:'word', value, wildcard} or {type:'phrase', words:[...]}.

Echo: build English: phrase → `the phrase “...”`, word → `the word child` (with * → `words ending in child`), NOT → `without ...`, AND → "and", OR → "or". Compose recursively. For NOT-only query: echo says "Paragraphs without ...".

Matching: build regex per term over norm. Word: escape regex chars, trailing * → `\w*` appended... spec: "the word escaped, trailing * → \w*, boundaries (?<![\p{L}\p{N}]) before and (?![\p{L}\p{N}]) after, flag u". So pattern = `(?<![\p{L}\p{N}])` + escaped (+ `\w*` if wildcard) + `(?![\p{L}\p{N}])`, flags 'u'. Note: with wildcard, the trailing boundary after \w* — `(?<![\p{L}\p{N}])abc\w*(?![\p{L}\p{N}])` — the negative lookahead after \w* means the match must end at a non-letter... \w* is greedy but backtracks; effectively matches "abc" followed by word chars then a boundary. Fine.

Hyphen is a boundary: since lookbehind/lookahead only exclude letters/numbers, "-" is not in \p{L}\p{N}, so "state" matches in "non-State" (norm lowercases, hyphen stays). Good.

Phrase: words joined by `\s+` inside same boundaries: `(?<![\p{L}\p{N}])w1\s+w2(?![\p{L}\p{N}])`. But norm has fn marks removed and whitespace collapsed, so \s+ works.

Evaluate tree over record.norm with regex test.

Highlight: over shown text (fn marks removed? Spec: "The same terms become a second regular expression over the shown text" — shown text = text with fn removed. But then "a gap between phrase words matches (?:\s|\[\[fn:\d+\]\])+" — that's for when highlighting the stored text? Hmm. The shown text has marks removed, so gap is just \s+. But the spec says the highlight regex allows fn marks in gaps — that applies when showing "as stored". I'll build the highlight regex to allow `(?:\s|\[\[fn:\d+\]\])+` between phrase words, and apply it to whichever text is displayed (shown or stored). Also quotes/apostrophes/hyphens match variants: in the pattern, replace escaped `"` with `["“”„]`, `'` with `['‘’‚]`, `-` with `[-–—]`... careful: escaping then replacing. I'll build a helper that converts a term's literal into a char-class-friendly pattern: for each char, if it's a quote/apostrophe/dash, emit class; else escape.

Also case-insensitive: norm is lowercase but shown text is original case. Highlight regex needs flag 'iu' (case-insensitive + unicode). Use 'iu'.

Highlight function: escape HTML first, then wrap matches in <mark>. But careful: escaping changes characters (& → &amp;) which could break matching. Better: run regex over raw text, collect match ranges, then build HTML by escaping segments between ranges. That's safer. I'll do that: find all matches with a global regex combining all positive terms (OR), sort, merge, then construct HTML.

Combined highlight regex: for each positive term (words and phrases, not NOT), build pattern; join with '|'; flags 'giu'. Then iterate matches over raw shown text.

Wait — phrase gap `(?:\s|\[\[fn:\d+\]\])+` — in shown text fn removed so just whitespace; in stored text fn marks present. Since I apply to whichever is displayed, include the fn alternative. But when applied to shown text, `[[fn:...]]` won't appear, fine.

Also single word terms with wildcard: `child\*` → pattern `child\w*` with boundaries.

NOT terms never highlighted.

Now filters:
- committees ticked set (all ticked initially). Record passes if any of record.committees in ticked set. Joint records count under both.
- year range: from/to inputs preset to min/max.
- document select: short_title grouped by committee (optgroup label = committee code or full name). Blank = all. Filter: record.short_title === selected.

Chips: show active filters as removable chips: e.g. "Committee: CRC" (only when not all ticked — maybe show "Committees: 3 of 10" chip? Spec: "A narrowed filter shows as a small removable chip under the big number." I'll show chips: if committee filter narrowed → chip "committees: n of k" with × to reset all; if year narrowed → "years: 1990–2023" ×; if document selected → chip with short_title ×. Also maybe query chip? Query has its own echo line. Keep chips for the three filters.

Search flow: on search, parse query → tree or error. Compute hits = records where (tree ? eval : true) && filters. Update count, committee hit counts in brackets, chart, results, checks.

Committee hit counts: for each committee code, count hits whose committees include it. Shown in brackets after search.

Chart FIG.01: horizontal bars per committee ranked by value over hits. Use Chart.js bar with indexAxis 'y'. Data labels at end of bar — Chart.js doesn't have built-in datalabels plugin (not loaded). I'll draw values via a custom plugin or just put value in the label? Spec: "the value at the end of each bar". I can write a tiny inline plugin that draws the value text after each bar. That's allowed (inline JS). Or simpler: use the category labels to include the value? "horizontal labels" — labels on y axis are committee names. I'll add a small plugin `afterDraw` that renders values at bar ends. Keep it simple.

Click a bar = tick that committee alone: chart onClick → get index → committee → set ticked = {that one} → re-filter (without re-running search? The chart is over hits of current query; clicking sets committee filter to that one and re-renders). I'll implement: onClick sets committee filter to only that committee and re-applies.

aria-label on canvas stating numbers: build string "CRC 2091, CEDAW 1500, ..." — could be long with 10 committees; fine.

Fallback table beside chart with same numbers.

Results tab: summary line aria-live: "279 of 7,304 paragraphs match · 8 committees · 1990–2023" (committees = distinct committees among hits? "8 committees" — distinct committee codes among hits; years min–max of hits). Order select: "year, newest first" (default) / "document order" / "most matches first"? Spec: "a select beside it offers document order and most matches first". Hmm "most matches first" — matches of what? Maybe records with most highlighted terms? I'll interpret: sort by number of matched terms descending. Actually simpler interpretation: order options: (1) year desc, title, paragraph asc (default); (2) document order (title asc, paragraph asc); (3) most matches first = by count of highlighted matches descending. I'll implement that.

Pagination: 25 per page, "Show 25 more" button appends.

Row rendering: article with heading (committee badge + short_title), symbol link, pinpoint, year. Text shown with marks removed; grey line "3 footnote marks removed · show as stored" toggle. Highlight marks. Long paragraphs >700 chars: show first 700 cut at word + "Show the full paragraph (N words)". white-space: pre-wrap.

Amber notes: leading mismatch ("the text begins '45.' but the record is para. 41: check the document"), lettered subpara, shared pinpoint (two records same title+paragraph), joint GC.

Click row → expand in place: buttons Copy citation, Copy quotation, Add to draft; Context: previous | next links (paragraph ±1 of same title). Context opens inline grey with pinpoint.

Copy citation: if shared symbol: `${committee}, ${docName} (${symbol}), ${pinpoint}` else `${symbol}, ${pinpoint}`. Wait spec earlier: "CERD, General Recommendation No. 29 (A/57/18), para. 3" — committee code or full name? Example uses "CERD". Use committee code. docName = title up to first colon or " on ".

Copy quotation: shown text in quotation marks + space + citation. But leading number: "When leading equals paragraph, the copied quotation drops the '12. ' at the start". So copied quotation text = shown text with leading "N. " stripped if leading===paragraph. Use curly quotes? "in quotation marks" — I'll use “ ” curly quotes. Hmm, or straight? Data uses curly mostly. I'll use “...”.

Add to draft: push {id, citation, quotation, text_copied, text_as_stored, symbol, paragraph, pinpoint, committee, short_title, year, doc_url} to draft array; persist to localStorage if available else memory; update tab label "03 DRAFT (n)".

Draft tab: list items with quotation as copied, citation, remove button. Copy all: items joined: quotation + "\n" + citation + "\n\n". Download .txt: same content as file. Download .csv: header citation,symbol,paragraph,pinpoint,committee,short_title,year,text_copied,text_as_stored,doc_url; fields double-quoted, escape quotes by doubling; UTF-8 BOM. Use Blob + URL.createObjectURL + a.click(). That's fine offline.

Check tab: run checks after each search (and at load with empty query):
1. Query understood: echo + term count, or parse error.
2. Totals: rows listed across pages equal hits (renderedCount === hits.length); checkbox bracketed counts sum = hits + jointHits (joint hits = hits counted multiple times due to multi-committee records: sum over committees of counts − hits.length).
3. Chart total: bars sum = hits + joint extra, both shown.
4. Highlight: every hit has ≥1 mark unless NOT-only query; list "matched, not highlighted" ones.
5. Normalisation: if query contains straight quote/apostrophe/hyphen, say curly/dash forms matched too and how many hits contain only those forms. Compute: hits whose shown text contains curly variant but not the straight form of the query term? Simplify: count hits where norm matched but shown text doesn't contain the literal straight query string... I'll do: for each query char in ['"', "'", '-'], if present in raw query, count hits whose shown text includes the curly counterpart (“ ” ’ –) — report "n hits use the curly/dash form".
6. Numbering: hits with leading≠paragraph (both numbers), hits sharing pinpoint within same title, lettered subparas.
7. Marks: for every hit, marks removed count equals count of '[[fn:' in stored text, and reinserting... "putting them back gives the stored text exactly" — since we only removed via regex, trivially true; check: shown === text.replace(regex,'') and marks === count. Verify per hit.
8. Draft: for each draft item, look up record by id, compare text_as_stored.

Each check line: description, values, "pass" green or "check failed" red. Header dot: n checks pass / n checks failed; red dot on tab 04 if any failed.

Known quirks (computed at load, shown before search): paragraph 0 count + example; shared symbols count + example; joint docs count + example; duplicated pinpoints count + example; leading mismatches count + example.

Header line: "`records.length` paragraphs from n General Comments (distinct title) of k committees, year min–max", source linked.

Left rail hidden on Draft tab ("always visible except on the Draft tab"). So layout: rail + main; when draft tab active, hide rail (add class). Keep header always.

Search box focus on load. Example list: while box empty and focused, show list with syntax + 3 examples as buttons; closes when typing starts. Arrow keys navigate examples — make them buttons in a list; simple approach: a div with buttons, arrow up/down moves focus. Enter in input searches.

Syntax text: "a space or AND joins words; OR; NOT or a leading minus; "an exact phrase" in double quotes; parentheses; a star at the end of a word for any ending (child* finds children); operators in capitals, lower-case "or" is a word".

Under box: "Whole words, any case. Curly and straight quotes, apostrophes, dashes and hyphens count as the same, and footnote marks are skipped, so State's finds State’s and a phrase can cross a footnote."

After search: echo line: "Paragraphs containing the phrase “best interests” and the word child".

Error: unbalanced quote/paren → message, no results (hits = []? or keep previous? "shows a message and no results" — set hits empty, show error).

Empty query with filters: lists all passing filters, summary says "no search words".

Now design/CSS: paper #f4f0e8, ink #1d1b18, rules #d9d2c3, accent #9b2335. Fonts: Georgia serif for title/big numbers; ui-monospace for labels; system sans 16px body.

Layout: header top; below, flex: aside (rail, ~260px) + main (tabs content). Tabs as role=tablist with buttons, arrow-key navigation. Tab panels.

Tabs: 01 OVERVIEW, 02 PARAGRAPHS, 03 DRAFT, 04 CHECK & METHOD. Tab 03 label includes count: "03 DRAFT (4)" — update dynamically.

Clickable count constraints — fine.

Chart: Chart.js bar. Colors: bars accent red #9b2335. Gridlines light #d9d2c3, max 10 ticks. Value labels at end via plugin.

Let me now think about the "committees" per record and chart: chart shows one bar per committee over hits, counting joint under both. If a committee has 0 hits, still show bar with 0? "one bar per committee, ranked by value" — over hits; committees with zero... I'll include all 10 committees that appear in data, ranked, including zeros (bar length 0). Or only committees with hits? Ranked by value; including zeros is fine and shows "8 committees" in summary separately. I'll include all committees present in the full dataset.

Document select: optgroups by committee (full name), options value=short_title, label=short_title. But short_title may repeat across committees? Possibly; group by committee so value could be committee + '|' + short_title. I'll use value = committee + ' :: ' + short_title and filter record.committee === that committee && short_title matches. Hmm but joint GCs have one committee field. Use record.committee for grouping. Fine.

Actually simpler: option value = short_title; duplicates unlikely but possible; filter by short_title only. Spec says "a select of short_title grouped by committee". I'll group by committee and match on short_title (and committee if provided). I'll do value=`${committee}||${short_title}`.

Year inputs: number inputs from/to.

Now the checks header dot: compute after each render: passCount/failCount. Green dot + "n checks pass" or red + "n checks failed". Also red dot on tab 04 label when failures.

Let me think about performance: 7,304 records, normalization at load — fine. Search: evaluate tree per record with regexes — build regexes once per query, test 7,304 strings — fine.

Highlight per rendered row only (25 per page + expanded) — fine.

Now write the code. Structure:

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Verbatim finder: General Comments</title>
<style>...</style>
</head>
<body>
<header>...</header>
<div class="layout">
  <aside id="rail">...</aside>
  <main>
    <div role="tablist" id="tabs">4 buttons</div>
    <section id="panel-overview">...</section>
    <section id="panel-paragraphs">...</section>
    <section id="panel-draft">...</section>
    <section id="panel-check">...</section>
  </main>
</div>
<footer>...</footer>
<script>...</script>
</body>
</html>
```

CSS details: 

```css
:root{--paper:#f4f0e8;--ink:#1d1b18;--rule:#d9d2c3;--red:#9b2335;--green:#2e6b3e;--amber:#8a5a00;}
*{box-sizing:border-box}
body{margin:0;background:var(--paper);color:var(--ink);font:16px/1.5 -apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
```

Header: padding, label monospace uppercase letter-spacing, h1 serif ~34px, meta line small.

Tabs: monospace uppercase buttons with bottom border; active red.

Rail: width 280px, border-right thin rule. Big number serif 48px.

Filter heading: button with aria-expanded, numbered "01 COMMITTEE, YEARS, DOCUMENT" — spec says one numbered heading "01 Committee, years, document" containing all three filter groups. OK: one collapsible section containing committee checkboxes, years, document select.

Checkbox list: each label with input checkbox + code + full name + hits bracket span.

Chips: small spans with × button.

Main panels: padding.

Results rows: article with border-top rule; heading row; text pre-wrap.

mark: background pale yellow #f6e9a8? "pale yellow, dark text, bold". Use background:#f3e5a0; color:#1d1b18; font-weight:700.

Amber note: color #8a5a00.

Buttons: monospace small, border 1px rule, background transparent; hover.

Focus ring: outline 2px solid var(--red).

Now JS. Let me write it carefully.

```js
const D = window.WORKSHOP_DATA.gc;
const R = D.records;
const FN = /\[\[fn:\d+\]\]/g;
const COMMITTEE_NAMES = {CAT:"Committee against Torture","CAT-OP":"Subcommittee on Prevention of Torture (CAT/OP)",CCPR:"Human Rights Committee",CED:"Committee on Enforced Disappearances",CEDAW:"Committee on the Elimination of Discrimination against Women",CERD:"Committee on the Elimination of Racial Discrimination",CESCR:"Committee on Economic, Social and Cultural Rights",CMW:"Committee on Migrant Workers",CRC:"Committee on the Rights of the Child",CRPD:"Committee on the Rights of Persons with Disabilities"};
```

Normalization function:

```js
function normalize(s){
  return s.replace(/\[\[fn:\d+\]\]/g,'')
    .replace(/[“”„]/g,'"').replace(/[‘’‚]/g,"'")
    .replace(/[–—­]/g,'-')   // en dash, em dash, soft hyphen
    .replace(/\s+/g,' ')      // includes nbsp? \s in JS matches \u00a0? Yes, \s matches \u00a0 in JS.
    .toLowerCase();
}
```

JS \s matches \u00A0 (yes, \s includes \u00a0). Good. Soft hyphen \u00ad included in dash class — spec says "en dash, em dash and soft hyphen → '-'". OK.

Record precompute:

```js
const byId = {};
R.forEach(r=>{
  const shown = r.text.replace(FN,'');
  const marks = (r.text.match(/\[\[fn:/g)||[]).length;
  const leading = (r.text.match(/^(\d{1,3})\.\s/)||[null,null])[1];
  const lettered = (r.text.match(/^\(([a-z]{1,4})\)/)||[null,null])[1];
  ...
});
```

Wait lettered: text starts with "(a) To take note…" — but leading number check first: "22 records are lettered sub-paragraphs ('(a) To take note…') that the file numbers 1, 2, 3". So text starts with "(a)". pinpoint: if paragraph===0 → "preamble"; else if lettered → `subpara. (${lettered})`; else "para. "+paragraph. Order: check lettered before paragraph? A lettered subpara has paragraph 1,2,3 (nonzero), so check paragraph===0 first, then lettered, then para. But could a preamble start with "(a)"? Unlikely. Fine.

committees of record:

```js
function committeesOf(r){
  const s = r.symbol.replace(/CAT\/OP/g,'CAT-OP');
  const found = s.match(/\b(CAT-OP|CCPR|CEDAW|CED|CERD|CESCR|CMW|CRC|CRPD|CAT)\b/g) || [];
  const set = new Set(found);
  set.add(r.committee);
  return [...set];
}
```

Order in alternation: put CAT-OP before CAT so "CAT-OP" (after replacement) matches fully; also plain "CAT" in "CAT/C/GC/..." matches. But careful: after replacing CAT/OP→CAT-OP, a symbol "CAT/OP/CAT/..." hmm unlikely. Also \bCAT\b in "CAT-OP"? After replacement the string has "CAT-OP"; regex alternation tries CAT-OP first at that position — matches "CAT-OP" fully. Good. But also "CAT" alone elsewhere matches. Edge: symbol "CAT/C/GC/..." → matches CAT. Good.

Hmm wait: \b(CAT-OP|...)\b — in "CAT-OP", at position 0, \b ok, alternation: "CAT-OP" matches chars 0-5, then \b after P (end or non-word) ok. 

shared symbols: map symbol → set of titles:

```js
const symTitles = {};
R.forEach(r=>{(symTitles[r.symbol]=symTitles[r.symbol]||new Set()).add(r.title)});
const shared = r => symTitles[r.symbol].size > 1;
```

joint: committeesOf(r).length > 1? Spec: "Three joint General Comments carry two symbols in one symbol". Detect: symbol contains two committee codes → committees from symbol length ≥2. I'll define joint = (codes found in symbol).length >= 2.

docName: title up to first ':' or ' on ':

```js
function docName(t){
  const i1 = t.indexOf(':'), i2 = t.indexOf(' on ');
  let i = -1;
  if(i1>=0 && i2>=0) i=Math.min(i1,i2); else i = i1>=0?i1:i2;
  return i>0 ? t.slice(0,i) : t;
}
```

citation:

```js
function citation(r){
  const pin = r._pinpoint;
  if(r._shared) return `${r.committee}, ${docName(r.title)} (${r.symbol}), ${pin}`;
  return `${r.symbol}, ${pin}`;
}
```

Query parser:

```js
function tokenize(q){
  const toks=[]; let i=0;
  while(i<q.length){
    const c=q[i];
    if(/\s/.test(c)){i++;continue;}
    if(c==='('||c===')'){toks.push({t:c});i++;continue;}
    if(c==='“'||c==='”'||c==='"'){
      const close = (c==='“')?'”':'"';
      // accept either closing
      let j=q.indexOf... 
    }
    ...
  }
}
```

Simpler: for quote char (any of " “ ”), find closing quote of any of " ” ” starting after i. Let me: `const rest=q.slice(i+1); const m=rest.match(/["”]/);` if none → throw {msg:'Unbalanced quote: no closing " .'} phrase = rest.slice(0,m.index). i = i+1+m.index+1. Phrase token {t:'PHRASE', value:phrase}.

If c==='-': toks.push({t:'NOT'}); i++; continue. (leading minus as NOT; even mid-word hyphen? "non-State" contains hyphen mid-word — if I treat every '-' as NOT, "non-State" breaks! Spec says "a leading minus" — only at start of a term. So: treat '-' as NOT only if at start of a token (i.e., previous token is operator/start/'(' ). Track: if previous emitted token is undefined, '(', 'AND','OR','NOT' → '-' is NOT operator; else it's part of word. Implement with a flag `atTermStart`.

Word: read run until whitespace, paren, or quote char. But hyphen inside word ok. Also trailing '*' kept in value, wildcard flag.

Uppercase check: word === 'AND'/'OR'/'NOT' exactly (capitals) → operator. Lowercase 'or' is a word.

Parser:

```js
function parse(q){
  const toks=tokenize(q);
  let pos=0;
  function peek(){return toks[pos];}
  function parseOr(){
    let left=parseAnd();
    while(peek()&&peek().t==='OR'){pos++;const right=parseAnd();left={t:'OR',a:left,b:right};}
    return left;
  }
  function parseAnd(){
    let left=parseNot();
    while(peek()&&(peek().t==='AND'||isTermStart(peek()))){
      if(peek().t==='AND')pos++;
      const right=parseNot();
      left={t:'AND',a:left,b:right};
    }
    return left;
  }
  function parseNot(){
    if(peek()&&peek().t==='NOT'){pos++;return {t:'NOT',a:parseNot()};}
    return parsePrimary();
  }
  function parsePrimary(){
    const tk=peek();
    if(!tk) throw {msg:'Unexpected end of query.'};
    if(tk.t==='('){pos++;const e=parseOr();if(!peek()||peek().t!==')')throw{msg:'Unbalanced parenthesis: missing ) .'}pos++;return e;}
    if(tk.t===')')throw{msg:'Unbalanced parenthesis: unexpected ) .'};
    if(tk.t==='PHRASE'){pos++;return {t:'PHRASE',value:tk.value};}
    if(tk.t==='WORD'){pos++;return {t:'WORD',value:tk.value,wild:tk.value.endsWith('*')&&tk.value.length>1};}
    throw {msg:'Unexpected "'+tk.t+'" in query.'};
  }
  const tree=parseOr();
  if(pos<toks.length) throw {msg:'Unbalanced parenthesis: unexpected "'+toks[pos].t+'" .'};
  return tree;
}
function isTermStart(tk){return tk.t==='WORD'||tk.t==='PHRASE'||tk.t==='NOT';}
```

Hmm parseAnd loop: after parseNot, if next is AND consume, else if term-start (WORD/PHRASE/NOT) implicit AND. But NOT after a term without AND: "torture NOT detention" → implicit AND then NOT — parseNot handles NOT. OK.

Edge: empty query → tree null → match all.

Echo builder:

```js
function echo(tree){
  if(!tree) return 'no search words';
  switch(tree.t){
    case 'WORD': return tree.wild? `words ending in “${tree.value.replace(/\*$/,'')}”` : `the word ${tree.value}`;
    case 'PHRASE': return `the phrase “${tree.value}”`;
    case 'NOT': return `without ${echo(tree.a)}`;
    case 'AND': return `${echo(tree.a)} and ${echo(tree.b)}`;
    case 'OR': return `${echo(tree.a)} or ${echo(tree.b)}`;
  }
}
```

Full echo line: "Paragraphs containing " + echo + "." For NOT-only: "Paragraphs without X." Detect: tree.t==='NOT' → "Paragraphs without ...". I'll handle: if root is NOT → `Paragraphs without ${echo(tree.a)}.` else `Paragraphs containing ${echo(tree)}.`

Term regex over norm:

```js
function escRe(s){return s.replace(/[.*+?^${}()|[\]\\]/g,'\\$&');}
function termRegexNorm(term){
  if(term.t==='PHRASE'){
    const words=term.value.split(/\s+/).filter(Boolean).map(w=>escRe(w)).join('\\s+');
    return new RegExp(`(?<![\\p{L}\\p{N}])${words}(?![\\p{L}\\p{N}])`,'u');
  }
  let w=escRe(term.value.replace(/\*$/,''));
  if(term.wild) w+='\\w*';
  return new RegExp(`(?<![\\p{L}\\p{N}])${w}(?![\\p{L}\\p{N}])`,'u');
}
```

Wait: phrase words may contain regex chars — escaped. But phrase words in norm are normalized (lowercase, straight quotes). The query phrase should be normalized too before building regex: normalize the phrase value with same normalize() (minus fn removal — harmless). I'll normalize query terms at tokenize time: phrase value → normalize(value); word → normalize(word). But echo should show original? Echo with normalized is fine-ish; better keep original for echo. I'll store both: value (original) for echo, and norm value for regex. Simpler: normalize in termRegexNorm: `const v = normalize(term.value)`. normalize lowercases and converts quotes — good for matching norm. For echo use original.

Hmm but normalize also collapses whitespace — fine for phrases.

Collect positive terms for highlight:

```js
function collectTerms(tree, out){ // positive only
  if(!tree)return;
  if(tree.t==='NOT')return;
  if(tree.t==='WORD'||tree.t==='PHRASE'){out.push(tree);return;}
  collectTerms(tree.a,out);collectTerms(tree.b,out);
}
```

Evaluate:

```js
function evalTree(tree,norm){
  if(!tree)return true;
  switch(tree.t){
    case 'WORD':case 'PHRASE':return termRegexNorm(tree).test(norm);
    case 'NOT':return !evalTree(tree.a,norm);
    case 'AND':return evalTree(tree.a,norm)&&evalTree(tree.b,norm);
    case 'OR':return evalTree(tree.a,norm)||evalTree(tree.b,norm);
  }
}
```

Cache regex per term: attach `tree._re` lazily.

Highlight regex over shown/stored text:

```js
function flexChar(ch){
  if(ch==='"'||ch==='“'||ch==='”'||ch==='„') return '["“”„]';
  if(ch==="'"||ch==='‘'||ch==='’'||ch==='‚') return "['‘’‚]";
  if(ch==='-'||ch==='–'||ch==='—'||ch==='­') return '[-–—­]';
  return escRe(ch);
}
function termPatternShown(term){
  const raw = term.value; // original
  let body='';
  if(term.t==='PHRASE'){
    const parts=raw.split(/\s+/).filter(Boolean).map(w=>[...w].map(flexChar).join(''));
    body=parts.join('(?:\\s|\\[\\[fn:\\d+\\]\\])+');
  } else {
    let w=[...raw.replace(/\*$/,'')].map(flexChar).join('');
    if(term.wild) w+='\\w*';
    body=w;
  }
  return `(?<![\\p{L}\\p{N}])${body}(?![\\p{L}\\p{N}])`;
}
```

Hmm — the boundary lookbehind on shown text: shown text has original case; flag 'iu' handles case. But lookbehind `(?<![\p{L}\p{N}])` with 'u' flag fine.

Wait, issue: phrase gap in shown text: fn marks removed, whitespace collapsed? No — shown text keeps original whitespace (line breaks, nbsp). `\s` matches nbsp and line breaks in JS. Good. In stored text, fn marks present → gap alternative includes them. Good.

But careful: `[...w]` spreads by code points — good for accented chars.

Combined highlight regex: `new RegExp(patterns.join('|'),'giu')`. Then:

```js
function highlightHTML(text, terms){
  if(!terms.length) return escHtml(text);
  const re=new RegExp(terms.map(termPatternShown).join('|'),'giu');
  let out='',last=0,m;
  while((m=re.exec(text))){
    if(m[0].length===0){re.lastIndex++;continue;}
    out+=escHtml(text.slice(last,m.index))+'<mark>'+escHtml(m[0])+'</mark>';
    last=m.index+m[0].length;
  }
  out+=escHtml(text.slice(last));
  return out;
}
```

escHtml: & < >.

Note: overlapping matches — regex exec handles non-overlapping leftmost; fine.

Now state:

```js
const state={tree:null, query:'', error:null, hits:[], committees:new Set(all codes), yearFrom:minYear, yearTo:maxYear, doc:'', order:'year', shown:25, draft:[]};
```

allCommittees: distinct codes across records (from committeesOf). For checkbox list, use sorted list of codes present in data.

applyFilters(r): committees: r._committees.some(c=>state.committees.has(c)); year: r.year>=from && <=to; doc: !state.doc || (r.committee+'||'+r.short_title)===state.doc.

runSearch(): parse query; if error → state.error, hits=[]; else hits = R.filter(r=>evalTree(tree,r._norm)&&passFilters(r)). Then update everything: count, chips, committee counts, chart, results (reset shown=25), checks, header dot.

Committee hit counts: for each code in allCommittees: count hits with _committees includes code.

Chart data: committees sorted by count desc (all committees in data, including 0). Build chart once, update data on search.

Chart click: onClick → element index → committee → state.committees = new Set([code]); sync checkboxes; re-run filter only (keep query): I'll just call applyAll() which re-filters hits without re-parsing (or re-run search — cheap enough; but re-running search resets shown=25, fine). Simpler: clicking bar sets committee filter and calls refresh() which recomputes hits from current tree+filters. I'll structure: `computeHits()` uses state.tree; `runSearch()` sets tree from input then computeHits+render. Bar click: set committees, computeHits+render.

Rendering results: function renderResults() builds rows for hits.slice(0,state.shown). Each row article:

```
<article class="row" data-id>
  <header>badge committee(s) + short_title ... </header>
  <div class="meta"><a href=doc_url target=_blank rel=noopener>symbol</a> · <span class="pin">para. 18</span> · 2011</div>
  <p class="text">highlighted</p>
  <div class="marks">3 footnote marks removed · <button>show as stored</button></div>
  <div class="notes">amber notes</div>
  <div class="actions"> (visible when open) Copy citation / Copy quotation / Add to draft / Context: previous | next </div>
  <div class="context"></div>
</article>
```

Row click toggles open (but clicks on buttons/links inside shouldn't toggle — stopPropagation on buttons). I'll attach click on row header area to toggle.

Pinpoint display: "para. 18" in red accent per design ("pinpoints in red").

Long text: if shown.length>700 → cut at last space before 700 → + "… " + button "Show the full paragraph (N words)". N words = shown.split(/\s+/).length. Toggle full.

Marks line: if marks>0: "n footnote marks removed · show as stored" button toggles between shown and stored text (stored highlighted too, with fn marks visible). When stored shown, label "show as printed (marks removed)".

Copy citation: citation(r). Copy quotation: `“${copyText}” ${citation}` where copyText = shown with leading "N. " removed if leading===paragraph (leading is string; compare Number(leading)===r.paragraph). Note: leading regex on r.text (stored). If leading matches and equals paragraph → strip from shown: shown.replace(/^\d{1,3}\.\s/,''). 

Copy function:

```js
async function copyText(t, msg){
  try{ await navigator.clipboard.writeText(t); live(msg||('Copied: '+t)); }
  catch(e){ show fallback box with text selectable; live('Clipboard refused — select and copy from the box.'); }
}
```

Fallback: a fixed div with textarea, shown when needed.

aria-live region: #live.

Draft:

```js
function loadDraft(){ try{ const s=localStorage.getItem('gc-draft'); if(s){state.draft=JSON.parse(s);} state.store='localStorage'; }catch(e){ state.store='memory'; } }
function saveDraft(){ if(state.store==='localStorage'){ try{localStorage.setItem('gc-draft',JSON.stringify(state.draft));}catch(e){state.store='memory';} } }
```

Draft item: {id, citation, quotation, symbol, paragraph, pinpoint, committee, short_title, year, text_copied, text_as_stored, doc_url}.

Add to draft: build from record; check duplicates by id? Allow duplicates? I'll skip if same id already present (note "already in draft"). Fine.

Draft tab render: heading "Your draft (n quotations)", list; each item: quotation paragraph (as copied, in quotes), citation line, remove button. Buttons: Copy all, Download .txt, Download .csv. Hint: "Kept in localStorage when allowed, in memory otherwise." — dynamic: state.store.

Copy all format: items.map(i=>i.quotation+'\n'+i.citation).join('\n\n').

CSV: header + rows; quote all fields, double internal quotes; BOM '\uFEFF'. Blob type 'text/csv;charset=utf-8'.

Download: 

```js
function download(name, content, type){
  const blob=new Blob([content],{type});
  const a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download=name;document.body.appendChild(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(a.href),1000);
}
```

Checks: function runChecks() returns array of {label, detail, pass}. Render into panel 04. Also quirks computed at load.

Check details:

1. Query understood: `Query: “${state.query}” → ${echo} · ${nTerms} term(s)` pass unless error (error → fail with message). nTerms = count of WORD/PHRASE in tree.
2. Totals: rendered rows count === hits.length (we render all via paging — "rows listed across pages equal the hits": state.shown may be < hits; check: min(shown,hits) rendered... I'll check renderedCount===Math.min(state.shown,hits.length) and note "25 of 279 shown, all counted". Hmm spec: "Rows listed across pages equal the hits" — meaning when all pages shown. I'll compute: sum of committee bracket counts === hits.length + jointExtra; and rendered === hits.length when shown>=hits.length else rendered===shown. I'll phrase: "rows rendered (${rendered}) + rows on later pages (${hits.length-rendered}) = ${hits.length} hits" pass if rendered+rest===hits.length (trivially true) — better: verify hits.length === R.filter(...).length recomputed? That's the same computation. I'll do: recompute hits independently with a second pass (simple loop) and compare lengths. OK: `const recount = R.filter(r=>match&&filters).length; pass = recount===hits.length`. And bracket sum check: sum(committeeCounts) === hits.length + jointExtra where jointExtra = hits with >1 committees counted extra. Compute jointExtra = hits.reduce((s,h)=>s+h._committees.length-1,0). pass if sum===hits.length+jointExtra.
3. Chart total: chart data sum === same.
4. Highlight: for each hit, count marks in its rendered highlight — but we only render 25. Check over all hits: compute highlight on shown text and count `<mark>` occurrences? That's expensive for 7k records × long texts... Only when hits reasonable. Alternative: check via regex: does combined highlight regex match shown text? For NOT-only query skip. For each hit, test re.test(shown) — 7k regex tests fine. Collect hits where matched in norm but highlight regex fails → "matched, not highlighted" list (cap display at 10). pass if none.
5. Normalisation: if query has straight " ' -: count hits whose shown text contains curly counterpart but not the straight char... Simplify: for each of `"`,`'`,`-` present in raw query: count hits where shown includes the curly/dash variant. Report line. pass = true (informational) — but checks should be pass/fail; make it pass with info. I'll mark pass always with detail.
6. Numbering: list hits with leading && Number(leading)!==paragraph (both numbers); hits sharing (title,paragraph) with another record; lettered hits. pass = informational? These are quirks, not failures. Spec: checks panel lines "pass" or "check failed". Numbering check: pass if no mismatches? But mismatches exist in data (5 records) — they'd show as "check failed"? Spec says "A failed check marks rows; it never drops them." Hmm — the numbering check is meant to surface them. I'll make it: pass if 0 mismatches, else "check failed" listing them (with pinpoints). Since data has 5, it will show failed — that's honest and intended ("the row shows both"). Actually re-reading: "Numbering. Hits whose leading number differs from paragraph, with both numbers; hits that share a pinpoint...; hits that are lettered sub-paragraphs." It's a check that reports these; I'll mark it "check failed" when any exist (they're flagged on rows too). Hmm, but then header shows failures at load with empty query... The quirks panel already lists them. Maybe numbering check should be "pass" when the app correctly displayed both numbers on rows? I'll define: pass if every hit with mismatch is flagged in the row (we do flag) — i.e., check that our flagging covers all: count mismatches in hits vs count flagged. That's circular. Simpler and honest: report counts; pass = true if the app shows both numbers (which it does by construction)... I'll make it informational "pass" with counts, and the amber notes on rows carry the warning. Actually spec explicitly wants "check failed" possible. Let me make numbering check: fail if any hit has leading mismatch (listing them) — since these are real data quirks the user must verify, "check failed" with pinpoints is appropriate and matches "A failed check marks rows". But at load with empty query, all 5 mismatch records are hits → header red. That's fine and honest — the file has quirks. Hmm, but "n checks pass" green dot expectation... The spec says header shows green "n checks pass" or red "n checks failed". With quirks present it'd be red. I think that's acceptable and truthful. But maybe softer: numbering check passes when every mismatch is flagged on its row (which we guarantee), and lists them as "flagged". I'll go with: pass if flagged count === mismatch count (always true) — no. 

Decision: Numbering check = "pass" when no mismatches among hits; "check failed" when mismatches exist, listing pinpoints — because the reader must check the document. This matches "with the pinpoints concerned". The header will show some failures at load due to file quirks; the quirks panel explains. Actually wait — that makes the header permanently red, which seems off for "n checks pass". Let me reconsider: maybe treat numbering as informational pass with counts listed (the check is "did we detect and flag them" → pass). The spec's check list is about the app verifying itself. "Numbering. Hits whose leading number differs..." — the check verifies the app surfaces them. I'll implement: pass if every mismatch/duplicate/lettered hit is flagged in its row; detail lists counts and examples. That keeps header green normally, and fails only on real app bugs. I think that's the right reading: checks verify the app's own behavior. Similarly marks check: verify shown===text.replace and marks count — pass/fail real. Highlight check: fail if matched-not-highlighted exist. Totals: fail if mismatch. Query: fail on parse error. Draft: fail if stored text differs.

OK good — header green normally.

7. Marks: for each hit: marks === count of '[[fn:' in text AND shown === text.replace(FN,''). pass if all.
8. Draft: for each item, byId[item.id].text === item.text_as_stored. pass if all.

Quirks at load (over all R): paragraph===0 count + example symbol/para; shared symbols count + example; joint count + example; duplicated pinpoints (same title+paragraph appearing >1) count + example; leading mismatches count + example.

Header dot: after runChecks, passCount/failCount → update #checkdot.

Tab 04 red dot: add span in tab label when failures.

Now the Overview tab: FIG.01 chart + table. "Nothing else on this tab." Table beside chart: two-column layout: canvas left, table right (or below). I'll do flex: chart 60%, table 40%.

Chart config:

```js
const ctx=document.getElementById('fig1');
chart=new Chart(ctx,{type:'bar',data:{labels, datasets:[{data, backgroundColor:'#9b2335', borderWidth:0}]},options:{indexAxis:'y', responsive:true, maintainAspectRatio:false, onClick:..., plugins:{legend:{display:false}, tooltip:{...}}, scales:{x:{beginAtZero:true, grid:{color:'#d9d2c3', maxTicksLimit:10}, ticks:{...}}, y:{grid:{display:false}, ticks:{...}}}} , plugins:[valueLabels]});
```

valueLabels plugin:

```js
const valueLabels={id:'valueLabels', afterDatasetsDraw(c){ const {ctx}=c; const meta=c.getDatasetMeta(0); ctx.save(); ctx.font='12px ui-monospace, Menlo, monospace'; ctx.fillStyle='#1d1b18'; meta.data.forEach((bar,i)=>{ const v=c.data.datasets[0].data[i]; const x=bar.x + 4? ... }) }}
```

For horizontal bar (indexAxis y), bar.x is the right edge (value position), bar.y center. Draw text at bar.x+4, bar.y, baseline middle. If value 0, draw at x=0+4. Use `bar.x` — for horizontal bars, in Chart.js 4, `bar.x` is the end (value axis) coordinate? For indexAxis:'y', the base is at x of 0 value, and bar.x is the pixel of the value end. Actually element properties: for horizontal bar, `bar.x` = end, `bar.base` = start. I'll use `Math.max(bar.x, bar.base)+4`.

Canvas height: set container height = committees*28+40 px.

aria-label: set on canvas: `Paragraphs per committee: CRC 2091, CEDAW 1800, ...` update on chart update. Also fallback content inside canvas element + visible table.

Table: `<table><caption>FIG.01 data</caption><thead>Committee, Paragraphs</thead>...`.

Click bar → tick that committee alone: 

```js
onClick(e,els){ if(els.length){ const i=els[0].index; const code=chart.data.labels[i]; setCommittees(new Set([code])); } }
```

setCommittees updates checkboxes + state + recompute.

Now the rail HTML:

```html
<aside id="rail">
  <div class="rail-head"><span class="lbl">FILTERS</span><button id="clearAll">Clear all</button></div>
  <div class="bigcount"><span id="hitCount">7,304</span><div class="of">matching paragraphs<br>of 7,304</div></div>
  <div id="chips"></div>
  <div class="search">
    <label for="q">SEARCH THE PARAGRAPHS</label>
    <div class="qwrap">
      <input id="q" type="text" autocomplete="off" spellcheck="false" placeholder='e.g. "best interests" AND child'>
      <button id="go">Search</button>
    </div>
    <div id="syntax" hidden> ... syntax text + examples ... </div>
    <div class="hint">Whole words, any case. Curly and straight quotes, apostrophes, dashes and hyphens count as the same, and footnote marks are skipped, so State's finds State’s and a phrase can cross a footnote.</div>
    <div id="echo" class="echo"></div>
    <div id="qerror" class="err"></div>
  </div>
  <div class="fgroup">
    <button id="fhead" aria-expanded="false"><span>01</span> COMMITTEE, YEARS, DOCUMENT</button>
    <div id="fbody" hidden>
      <div class="allnone"><button id="allC">all</button>/<button id="noneC">none</button></div>
      <div id="clist"></div>
      <div class="years"><label>from <input id="yFrom" type="number"></label><label>to <input id="yTo" type="number"></label></div>
      <label class="doclbl">Document <select id="docSel"><option value="">all documents</option>...</select></label>
    </div>
  </div>
</aside>
```

Wait — clickable count: "4 tabs, search box, 1 filter heading = 6". The all/none buttons and year inputs are inside the closed heading, so not counted until opened. OK.

Syntax dropdown: shown when input empty && focused. Contains syntax paragraph + 3 example buttons. Arrow keys: I'll make examples a list of buttons; keydown on input: ArrowDown moves focus to first example, then between them; Enter on example runs it. Implement: examples array of buttons; on input keydown ArrowDown → focus examples[0]; on each example keydown ArrowDown/ArrowUp navigate. Esc closes. Typing (input event) hides if value non-empty.

Examples: `"best interests" AND child`, `(torture OR ill-treatment) NOT detention`, `"reasonable accommodation"`. Clicking fills input and runs search.

Search trigger: Enter in input or Search button click.

Now tabs behavior: buttons with role="tab", panels role="tabpanel". Arrow keys left/right move between tabs and activate. Rail hidden on draft tab: `document.body.classList.toggle('nodraft', tab==='draft')` with CSS `.nodraft #rail{display:none}`. Hmm but "Left rail (always visible except on the Draft tab)" — yes hide on draft.

Tab labels: "01 OVERVIEW", "02 PARAGRAPHS", "03 DRAFT (n)" — update count span, "04 CHECK & METHOD" with failure dot span.

Order select in paragraphs tab: options: "year, newest first" (value year), "document order" (doc), "most matches first" (matches). Comparator:

- year: year desc, then title asc (localeCompare), then paragraph asc.
- doc: title asc, paragraph asc, year desc.
- matches: count of highlight matches desc, then year desc. Compute match count per hit: run combined regex over shown, count. Cache per hit per query: store r._mcount.

Summary line: `${hits.length} of ${R.length} paragraphs match · ${distinct committees among hits} committees · ${minYear}–${maxYear}` or "no search words" when query empty: "no search words · 7,304 of 7,304 paragraphs pass the filters · ...". Spec: "An empty query with filters lists every paragraph that passes them, paged, and the summary says 'no search words'." So summary: if no query: "no search words · N of 7,304 paragraphs pass the filters · k committees · y1–y2". Else "N of 7,304 paragraphs match · k committees · y1–y2". Then order line: "sorted by year, newest first, then by document and paragraph" etc.

Context: previous/next of same title: find records with same title, sort by paragraph, find index of current, prev/next. Render inline grey block with pinpoint + text (highlighted? plain grey). Include its own symbol link? Keep simple: pinpoint + text. "Context opens paragraph −1 or +1 of the same title inline, in grey, with its own pinpoint". I'll render both prev and next as two small blocks when clicked ("previous | next" links). Clicking "previous" shows prev block; "next" shows next.

Now header:

```html
<header>
  <div class="kicker">UN TREATY BODIES · GENERAL COMMENTS</div>
  <h1>Verbatim finder: General Comments and General Recommendations</h1>
  <div class="meta"><span id="metaLine"></span> · <a id="srcLink">source</a> <span id="checkdot"></span></div>
</header>
```

metaLine: `${R.length.toLocaleString('en-US')} paragraphs from ${titles} General Comments (distinct title) of ${committees} committees, ${minYear}–${maxYear}`. Spec: "records.length paragraphs from n General Comments (distinct title) of k committees, year min–max". n = distinct title count (188), k = distinct committee count (10). Source linked to source_url if present.

checkdot: `<span class="dot green"></span> 8 checks pass` or red.

Footer: `${source} · built ${built}` + "Counting, matching and sorting are done by this page's code; no model is called." + Credits line: "Chart.js (MIT) for FIG.01." Spec: "A Credits line if shelf code is reused (Chart.js, MIT)." Chart.js is preloaded — include "Credits: charting by Chart.js 4 (MIT licence)." Also maybe cite the consulted sources? The plan lists sources consulted; the app could include a small "Method follows" line on tab 04. I'll add on tab 04 a short "Method & sources" list with the four consulted references (Ask DAG citation guidance, Wikipedia Help:Searching syntax, Chart.js accessibility, UK GAF chart formatting). That's nice for credibility. Keep brief.

Now, sizes: this will be a long file. Let me aim ~900-1100 lines. Must be complete and correct. Let me write it now, carefully, keeping all IDs consistent.

Let me define CSS classes:

- .kicker (monospace label)
- h1 serif
- .meta small
- .dot (green/red circle)
- .layout {display:flex; align-items:flex-start}
- #rail {width:300px; flex:0 0 300px; border-right:1px solid var(--rule); padding:...; position:sticky? top:0} — sticky nice.
- main {flex:1; padding:...; min-width:0}
- .tabs {display:flex; gap:...; border-bottom:1px solid var(--rule)}
- .tab {monospace uppercase, padding, border-bottom 2px transparent} .tab[aria-selected=true]{color:var(--red); border-color:var(--red)}
- .big {font-family:serif; font-size:52px}
- .chip {monospace small, border, red text when active? chips removable: × button}
- .row {border-top:1px solid var(--rule); padding}
- .badge {monospace outlined}
- .pin {color:var(--red); monospace}
- mark
- .note {color:var(--amber)}
- .grey {color:#6b675f}
- buttons .btn
- table styles
- .figtitle {serif italic? "FIG.01 Paragraphs per committee" — figure number monospace + title serif}
- [hidden]{display:none!important}
- :focus-visible {outline:2px solid var(--red); outline-offset:2px}

Chart container: #fig1wrap {height: set via JS}.

Now write JS fully. Let me be careful with details:

- `R.length` count; top-level count is string "7304" — use R.length.
- years min/max: compute.
- distinct titles: new Set(R.map(r=>r.title)).size.
- distinct committees: from committeesOf union — but "k committees" probably distinct `committee` field values (10). Use distinct r.committee. For checkbox list use codes from committeesOf union (includes CAT-OP). Hmm committee field for SPT records is "CAT-OP" per description ("CAT-OP is the Subcommittee on Prevention of Torture"). So distinct committee field = 10 codes. Use that for list; committeesOf adds symbol-derived codes which should be subset. I'll build checkbox list from distinct r.committee values sorted.

- docSel optgroups: group by committee (r.committee), option value `${r.committee}||${r.short_title}`, label short_title. Sort options by short_title within group. Distinct (committee, short_title) pairs.

- Year inputs: min/max preset.

Chips: 
- if committees.size < allCodes.size → chip `committees: ${size} of ${all}` × resets to all.
- if yearFrom>min||yearTo<max → chip `years ${from}–${to}` ×.
- if doc → chip `document: ${short_title}` ×.
- maybe query chip? skip.

Clear all: reset committees all, years min/max, doc '', query ''? "Clear all" in FILTERS header — clears filters (and maybe query). I'll clear filters only, keep query? Safer: clear filters and query, re-run. I'll clear filters + query and run.

Hmm, "Clear all" next to FILTERS heading — clears filters. I'll also clear the search box since it's in the rail; fine.

Committee checkbox change: update state.committees, recompute (without resetting query), update chips, counts, chart, results, checks. Also year inputs change → recompute. Doc select change → recompute.

Recompute function `refresh()` = computeHits + renderAll (count, chips, clist brackets, chart, results, checks, header). runSearch = parse input → set tree/error → state.shown=25 → refresh.

renderResults: build HTML string for hits.slice(0,shown). Use event delegation on results container for clicks: buttons with data-action and data-id; row header click toggles open.

Row open state: track openId; re-render on toggle (simple: re-render results). Context: store ctxFor id.

Let me write renderRow(r):

```js
function rowHTML(r){
  const open = state.openId===r.id;
  const notes=[];
  if(r._leading && Number(r._leading)!==r.paragraph) notes.push(`the text begins ‘${r._leading}’ but the record is para. ${r.paragraph}: check the document`);
  if(r._lettered) notes.push(`a lettered sub-paragraph, numbered ${r.paragraph} by the file`);
  if(r._dupPin) notes.push('two records share this pinpoint');
  if(r._joint) notes.push('joint General Comment');
  ...
}
```

_dupPin: computed at load: group by title+'|'+paragraph, size>1.

Text display: 

```js
function displayText(r){
  const full = state.fullId===r.id;
  const stored = state.storedId===r.id;
  const raw = stored? r.text : r._shown;
  const hl = highlightHTML(raw, state.hlTerms);
  if(!full && r._shown.length>700){
    const cut = r._shown.slice(0,700);
    const sp = cut.lastIndexOf(' ');
    const words = r._shown.split(/\s+/).length;
    return hl.slice? ...
  }
}
```

Problem: highlighting then cutting could cut inside a <mark>. Better: cut raw text first, then highlight the cut portion. But highlight regex over cut text: matches near the cut boundary fine. So:

```js
let raw = stored? r.text : r._shown;
let truncated=false;
if(!full && raw.length>700){ const cut=raw.slice(0,700); const sp=cut.lastIndexOf(' '); raw = (sp>400? cut.slice(0,sp): cut) + ' …'; truncated=true; }
const html = highlightHTML(raw, state.hlTerms);
```

Word count for label: r._shown.split(/\s+/).length.

Marks line: if r._marks>0: `${r._marks} footnote mark(s) removed · <button data-act="stored">show as stored</button>` else nothing (or "no footnote marks"). Toggle storedId.

Actions (when open): three buttons + context links:

```html
<div class="actions">
 <button data-act="cite">Copy citation</button>
 <button data-act="quote">Copy quotation</button>
 <button data-act="draft">Add to draft</button>
 <span class="ctx">Context: <button data-act="prev">previous</button> | <button data-act="next">next</button></span>
</div>
<div class="ctxbox" id="ctx-${r.id}"></div>
```

Context render: find same-title records sorted by paragraph; prev = largest paragraph < r.paragraph (or index-1); next similarly. Render: `<div class="ctxitem"><span class="pin">para. 17</span> text…</div>`. Grey. Include symbol? same title so same symbol mostly. Keep pinpoint + text (plain, maybe highlighted). I'll highlight too.

Copy citation text: citation(r). Note under buttons: `<div class="grey">Citation style: UN short form — parts stored separately, formatted on copy.</div>` Spec: "A grey note names the style, 'UN short form'." Put once in the open row or in tab intro. I'll put in each open row small grey line: "citation style: UN short form".

Copy quotation: `“${copyBody}” ${citation(r)}` where copyBody = shown with leading number stripped if leading===paragraph:

```js
function copyBody(r){
  let t=r._shown;
  if(r._leading && Number(r._leading)===r.paragraph) t=t.replace(/^\d{1,3}\.\s/,'');
  return t;
}
```

Add to draft: item = {id, citation, quotation, symbol, paragraph, pinpoint, committee, short_title, year, text_copied: copyBody(r), text_as_stored: r.text, doc_url}. quotation = `“${copyBody}” ${citation}`. Check duplicate id → live "already in your draft". saveDraft, update tab count, render draft if on draft tab.

Draft tab render:

```html
<h2>Your draft (<span id="dcount"></span> quotations)</h2>
<div id="draftList">items…</div>
<div class="btns"><button id="copyAll">Copy all</button><button id="dlTxt">Download .txt</button><button id="dlCsv">Download .csv</button></div>
<p class="hint">Kept in localStorage when your browser allows it; otherwise in this page's memory only.</p>
```

Item: `<div class="ditem"><p class="dq">quotation</p><p class="dc">citation · <button data-remove=id>remove</button></p></div>`.

Copy all: items.map(i=>`${i.quotation}\n${i.citation}`).join('\n\n').

TXT download: same as copy all, filename 'gc-quotations.txt'.

CSV: header: citation,symbol,paragraph,pinpoint,committee,short_title,year,text_copied,text_as_stored,doc_url. Row: fields quoted: `"` + String(v).replace(/"/g,'""') + `"`. Join with ','. BOM prefix.

Checks panel render: list of check lines: `<div class="check pass|fail"><span class="tag">pass</span> label — detail</div>`.

Quirks: `<ul>` items with counts + example.

Method section on tab 04: short paragraphs describing normalization, parser, matching, highlight, citation, copy — "How this is computed" in short form. Plus sources consulted list.

Header check dot update: after checks: `${pass} checks pass` green or `${fail} checks failed` red; tab 04 gets red dot span if fail>0.

Now, initial load: build everything, run with empty query (tree=null → all records pass filters) → hits = all 7304. That's fine; results paged 25. Chart over all. Checks run at load. Search box focus.

Performance: highlight check over 7304 hits at load — each regex test on texts up to ~7k chars... total maybe 7304 × avg 500 chars = 3.6M chars regex — fine.

Marks check over all hits: string ops — fine.

Numbering check: fine.

One concern: evalTree with regex per term per record — build regexes once per query (cache on tree nodes). Implement `getRe(tree)` memo: if tree._re return; compute for WORD/PHRASE.

NOT-only query: tree.t==='NOT' at root → highlight terms empty → no marks; check 4 skipped ("unless the query is NOT-only").

Echo for NOT-only: "Paragraphs without X." Also nested NOT fine.

Now the "hits per committee" brackets: after search, each checkbox label shows `[n]` — update spans. Before any search (initial load counts as a run with empty query) — spec says "after a search, its hits in brackets". Initial load: I'll show brackets too (it's a run). Fine — or only after user searches. I'll show always after first refresh; harmless. Actually spec: "a checkbox per code with its full name and, after a search, its hits in brackets". I'll show brackets once a search has been run (state.searched flag). Initial: no brackets. OK.

Chart note about joint: under FIG.01: "Joint General Comments count under both committees, so the bars can add up to more than the hits." Show when jointExtra>0.

"How this is computed" line under chart: "one count per committee over the paragraphs that match the query and filters."

Hint: "click a bar = tick that committee alone".

Now write the whole file. I'll be methodical. Also remember: no external loads; Chart.js via window.Chart.

Tab keyboard nav: keydown on tablist: ArrowRight/ArrowLeft → move focus & select.

Let me also handle `prefers-reduced-motion`? No animations anyway.

Let me now also double check pinpoint for paragraph 0: "preamble". Citation: "CEDAW/C/GC/1, preamble". Good.

Shared symbol example: A/48/18 holds seven GCs → citation "CERD, General Recommendation No. 29 (A/57/18), para. 3" style: `${committee}, ${docName(title)} (${symbol}), ${pinpoint}`. docName("General Recommendation No. 29: ...") → "General Recommendation No. 29". Good.

Edge: title without colon or " on " → whole title.

Now, the summary "8 committees" — distinct r.committee among hits.

Order select options:
- value "year": "sorted by year, newest first, then by document and paragraph"
- value "doc": "sorted by document, then paragraph"
- value "match": "sorted by most matches first"

Summary line includes order text. Spec: summary line then "the order: 'sorted by year, newest first, then by document and paragraph'; a select beside it offers document order and most matches first."

Implement comparators:

```js
const orders={
 year:(a,b)=> b.year-a.year || a.title.localeCompare(b.title) || a.paragraph-b.paragraph,
 doc:(a,b)=> a.title.localeCompare(b.title) || a.paragraph-b.paragraph || b.year-a.year,
 match:(a,b)=> (b._mc||0)-(a._mc||0) || b.year-a.year
};
```

_mc computed in refresh when order==='match' or always: count matches of combined highlight regex over shown. Compute for all hits each refresh — 7304 regex counts, ok. I'll compute always (cheap enough) so switching order is instant.

Actually computing _mc for all hits each refresh: combined regex global exec over each shown text — fine.

Now writing HTML skeleton with panels:

Panel overview:
```html
<section id="p-overview" role="tabpanel">
  <div class="fighead"><span class="figno">FIG.01</span> <h2 class="figtitle">Paragraphs per committee</h2></div>
  <p class="hint">click a bar = tick that committee alone · How this is computed: one count per committee over the paragraphs that match the query and filters.</p>
  <div class="figrow">
    <div class="chartwrap"><canvas id="fig1" role="img" aria-label="...">Fallback: see the table beside this chart.</canvas></div>
    <table class="figtable" id="fig1table"><caption>FIG.01 — paragraphs per committee (same numbers as the chart)</caption>...</table>
  </div>
  <p class="hint" id="jointNote" hidden>Joint General Comments count under both committees, so the bars can add up to more than the hits.</p>
</section>
```

Panel paragraphs:
```html
<section id="p-paragraphs" role="tabpanel" hidden>
  <div class="sumrow"><p id="summary" aria-live="polite"></p><label class="orderlbl">order <select id="orderSel">...</select></label></div>
  <p class="hint">This page retrieves; it never writes. Every paragraph shown is a record of the file, as stored.</p>
  <div id="results"></div>
  <button id="more" class="btn">Show 25 more</button>
</section>
```

Panel draft, panel check.

Rail as above.

Footer.

Live region: `<div id="live" aria-live="polite" class="sr"></div>` — sr class visually hidden but readable. Also copied message should be visible? "After every copy an aria-live message shows the exact string sent." aria-live region can be visually hidden; but better show a small toast line. I'll make #live a small visible line in header area? Put it fixed bottom-left small monospace. I'll make it visible small text under header (a status line). Simple: `<div id="live" aria-live="polite"></div>` styled small monospace, in header meta area or fixed. I'll place a status bar at top of main? Put it in header right side. I'll add `<div id="live" class="livemsg" aria-live="polite"></div>` in header.

Clipboard fallback box: `<div id="clipfallback" hidden><p>Clipboard refused — select and copy:</p><textarea id="cliptext" rows="4"></textarea></div>` fixed bottom.

Now write everything. Also remember `[hidden]{display:none!important}`.

Let me carefully write the JS in one pass mentally, then output.

Potential pitfalls:
- `normalize` on query word with `*`: normalize keeps `*`? normalize doesn't remove `*`; escRe escapes it; we strip trailing `*` before escaping via replace(/\*$/,''). But normalize lowercases — fine.
- Word token chars: read until whitespace/paren/quote. Quotes inside word? e.g. `State's` — apostrophe is part of word (not a quote delimiter since only " “ ” are delimiters). Good: `State's` tokenizes as word `State's`, normalized to `state's`, regex matches `state's` with flex apostrophe in highlight. In norm, apostrophe normalized to straight `'`. Good.
- Phrase with curly quotes pasted: opening “ closing ” handled.
- Unbalanced: throw error with message; display in #qerror; hits=[]; echo cleared; checks show parse error as failed check.

- The `-` NOT detection: track last token type. Implement in tokenizer:

```js
let prev=null;
while(i<q.length){
  const c=q[i];
  if(/\s/.test(c)){i++;continue;}
  if(c==='('||c===')'){toks.push({t:c});prev=toks[toks.length-1];i++;continue;}
  if(c==='"'||c==='“'||c==='”'){
    const rest=q.slice(i+1);
    const m=rest.search(/["”]/);
    if(m<0) throw new QError('Unbalanced quote — no closing " was found.');
    toks.push({t:'PHRASE',value:rest.slice(0,m)});
    i=i+1+m+1; prev=toks[toks.length-1]; continue;
  }
  if(c==='-' && (!prev || prev.t==='('||prev.t==='AND'||prev.t==='OR'||prev.t==='NOT')){
    toks.push({t:'NOT'}); prev={t:'NOT'}; i++; continue;
  }
  // word
  let j=i;
  while(j<q.length && !/[\s()"“”]/.test(q[j])) j++;
  const w=q.slice(i,j);
  if(w==='AND'||w==='OR'||w==='NOT'){toks.push({t:w});prev={t:w};}
  else {toks.push({t:'WORD',value:w});prev={t:'WORD'};}
  i=j;
}
```

Wait: a word could be empty if c is a quote handled above; if c is '-' not at term start, it's included in word (loop includes '-'). Good. If c is something like '*' alone → word '*' → wild with empty stem → pattern `\w*` with boundaries — matches any word. Edge, acceptable.

Hmm: `prev` for '-' check: after a WORD, '-' is part of next word? e.g. "torture -detention": after WORD torture, space, then '-' with prev=WORD → treated as part of word "-detention"? The word loop starts at '-', reads "-detention" as word including leading '-'. Then term value "-detention" — regex escRe includes '-'... boundary lookbehind before '-'? Pattern `(?<![\p{L}\p{N}])-detention(?!...)` — lookbehind before '-' checks char before '-', which is space → ok, matches "-detention" literally including hyphen. Hmm that wouldn't match "detention" alone. Spec says "a leading minus" as NOT — typically "-detention" at term start. With space before, prev is WORD (torture) so my rule treats '-' as part of word → wrong. Better rule: '-' is NOT operator when at start of a token, i.e., when previous char is whitespace/start/operator/'('. Track `termStart` boolean: true at beginning, after whitespace, after '(', after operators. Let me track: `let termStart=true;` set true after whitespace and after pushing '(' or operator tokens; false after WORD/PHRASE/')'. Then `if(c==='-' && termStart)` → NOT. That handles "torture -detention" correctly (after space, termStart=true → NOT). And "non-State": '-' mid-word, termStart=false → part of word. 

- Parser implicit AND: in parseAnd loop condition: peek is AND → consume; else if peek is WORD/PHRASE/NOT → implicit AND. But NOT as start of parseAnd's first element handled by parseNot. After a term, "NOT" token: e.g. "a NOT b" → parseAnd: left=a; peek NOT → implicit AND → parseNot consumes NOT b. Good.

- parsePrimary for WORD: wild = /\*$/.test(value) && value.length>1.

- Empty phrase `""` → value '' → phrase with no words → regex `(?<!..) (?!..)` matches everywhere — bad. Guard: if phrase value trim empty → throw QError('Empty phrase "" in query.'). Also word empty can't happen.

- Query with only operators e.g. "AND" → parsePrimary sees AND token → throw 'Unexpected "AND"'. Good.

Echo for wild: `words ending in “child”`.

Now evalTree caching:

```js
function reOf(node){
  if(node._re) return node._re;
  if(node.t==='WORD'||node.t==='PHRASE'){
    node._re=termRegexNorm(node);
  }
  return node._re;
}
```

termRegexNorm uses normalize(term.value):

```js
function termRegexNorm(node){
  const v=normalize(node.t==='PHRASE'?node.value:node.value.replace(/\*$/,''));
  let body;
  if(node.t==='PHRASE'){
    const parts=v.split(/\s+/).filter(Boolean).map(escRe);
    if(!parts.length) throw new QError('Empty phrase in query.');
    body=parts.join('\\s+');
  } else {
    body=escRe(v);
    if(node.wild) body+='\\w*';
  }
  return new RegExp('(?<![\\p{L}\\p{N}])'+body+'(?![\\p{L}\\p{N}])','u');
}
```

Note: normalize on phrase collapses whitespace — good.

Highlight terms: collect positive terms; if root NOT-only (tree.t==='NOT') → hlTerms=[] (spec: NOT terms never highlighted; a NOT-only query → no highlights). Actually collectTerms skips NOT subtrees entirely, so "a NOT b" highlights only a. Root NOT → collectTerms returns [] since it returns on NOT. Good — matches "unless the query is NOT-only".

hlRegex built in refresh: `state.hlRe = terms.length? new RegExp(terms.map(termPatternShown).join('|'),'giu') : null`.

termPatternShown uses original value (not normalized) with flexChar per char — handles curly in query too since flexChar maps curly to class. But normalize for matching? Shown text has original case; regex 'i' flag handles case. Curly in query maps to class covering all. Good. But phrase split on whitespace of original — fine.

One catch: flexChar for chars like `(` in word? Words can't contain parens (tokenizer splits). Phrase values can contain parens? Phrase is delimited by quotes, so parens inside quotes are literal — flexChar escapes them via escRe. Good.

Highlight function as above with escHtml segments.

_mc: count matches: 

```js
function countMatches(r){ if(!state.hlRe) return 0; state.hlRe.lastIndex=0; let n=0,m; const t=r._shown; while((m=state.hlRe.exec(t))){n++; if(m[0]==='')state.hlRe.lastIndex++;} return n; }
```

Careful: global regex with lastIndex shared — reset each use. OK.

Check 4 (highlight): for each hit: matched = evalTree true (by construction); highlighted = state.hlRe? state.hlRe.test(r._shown): (tree&&tree.t!=='NOT'). If tree && tree.t!=='NOT' && hlRe && !hlRe.test(shown) → list. Note hlRe.test with 'g' flag advances lastIndex — reset before each test. Use a non-global clone for testing: build `state.hlReTest = new RegExp(same source,'iu')`. Simpler: build two regexes.

Now checks implementation:

```js
function runChecks(){
  const checks=[];
  // 1 query
  if(state.error) checks.push({pass:false, label:'Query understood', detail:`parse error: ${state.error}`});
  else checks.push({pass:true, label:'Query understood', detail:`“${state.query||'(empty)'}” → ${echoText()} · ${termCount()} term(s)`});
  // 2 totals
  const recount = R.reduce((n,r)=>n+((!state.tree||evalTree(state.tree,r._norm))&&passFilters(r)?1:0),0);
  const jointExtra = state.hits.reduce((s,h)=>s+(h._committees.length-1),0);
  const bracketSum = Object.values(state.comCounts).reduce((a,b)=>a+b,0);
  checks.push({pass: recount===state.hits.length && bracketSum===state.hits.length+jointExtra, label:'Totals', detail:`recount ${recount} = hits ${state.hits.length}; committee brackets sum ${bracketSum} = hits ${state.hits.length} + ${jointExtra} joint`});
  // 3 chart total
  const chartSum = chart? chart.data.datasets[0].data.reduce((a,b)=>a+b,0):0;
  checks.push({pass: chartSum===state.hits.length+jointExtra, label:'Chart total', detail:`bars sum ${chartSum} = hits ${state.hits.length} + ${jointExtra} joint (both shown)`});
  // 4 highlight
  ...
  // 5 normalisation
  ...
  // 6 numbering
  const mism = state.hits.filter(r=>r._leading&&Number(r._leading)!==r.paragraph);
  const dups = state.hits.filter(r=>r._dupPin);
  const lett = state.hits.filter(r=>r._lettered);
  checks.push({pass: mism.every(r=>flagged...) — I'll just pass:true with detail listing counts and examples (flagged on rows). Hmm decide: pass true, detail: `${mism.length} leading-number mismatches (both numbers shown on the row), ${dups.length} shared pinpoints, ${lett.length} lettered sub-paragraphs — each flagged on its row`. pass: true. But if we want fail when unflagged... we always flag. pass:true.
  // 7 marks
  let bad=0; state.hits.forEach(r=>{ const c=(r.text.match(/\[\[fn:/g)||[]).length; if(c!==r._marks || r._shown!==r.text.replace(FN,'')) bad++; });
  checks.push({pass:bad===0, label:'Footnote marks', detail:`for ${state.hits.length} hits, marks removed = count of [[fn: in the stored text and re-adding gives the stored text exactly; ${bad} mismatches`});
  // 8 draft
  let dbad=0; state.draft.forEach(d=>{ const r=byId[d.id]; if(!r||r.text!==d.text_as_stored) dbad++; });
  checks.push({pass:dbad===0, label:'Draft', detail:`${state.draft.length} items; each stored text re-looked-up by id and compared; ${dbad} differences`});
  return checks;
}
```

Check 5 normalisation: 

```js
const raw=state.query; let det=[];
for(const [straight,curly] of [['"','“”'],["'","‘’"],['-','–—']]){
  if(raw.includes(straight)){
    const n=state.hits.filter(r=>r._shown.includes(curly[0])||r._shown.includes(curly[1])).length;
    det.push(`query holds “${straight}”; ${n} hits contain the curly/dash form`);
  }
}
checks.push({pass:true,label:'Normalisation',detail: det.length? det.join(' · ') : 'query holds no straight quote, apostrophe or hyphen'});
```

Check 4:

```js
let notHl=[];
if(state.tree && state.tree.t!=='NOT' && state.hlReTest){
  for(const h of state.hits){ state.hlReTest.lastIndex=0; if(!state.hlReTest.test(h._shown)) notHl.push(h); }
}
checks.push({pass:notHl.length===0, label:'Highlight', detail: state.tree&&state.tree.t!=='NOT' ? `every one of ${state.hits.length} hits shows at least one <mark>; ${notHl.length} matched but not highlighted${notHl.length?': '+notHl.slice(0,5).map(r=>r.symbol+', '+r._pinpoint).join('; '):''}` : 'NOT-only query: nothing is highlighted, as intended'});
```

Quirks at load:

```js
function quirks(){
  const p0=R.filter(r=>r.paragraph===0);
  const sharedSyms=Object.entries(symTitles).filter(([s,t])=>t.size>1);
  const joint=R.filter(r=>r._joint);
  const pinGroups={}; R.forEach(r=>{const k=r.title+'|'+r.paragraph;(pinGroups[k]=pinGroups[k]||[]).push(r)});
  const dups=Object.values(pinGroups).filter(g=>g.length>1);
  const mism=R.filter(r=>r._leading&&Number(r._leading)!==r.paragraph);
  return [...each with count + example (symbol, pinpoint)...];
}
```

Render as list: "preambles cited as 'preamble' (paragraph 0): 33 — e.g. CEDAW/C/GC/1, preamble" etc.

Now header meta: 

```js
metaLine.textContent = `${R.length.toLocaleString('en-US')} paragraphs from ${titleSet.size} General Comments (distinct title) of ${commSet.size} committees, ${minY}–${maxY}`;
```

Source link: if D.source_url → `<a href="${D.source_url}">${D.source}</a>` else text. Footer: `${D.source}${D.built? ' · built '+D.built:''}` + sentence + credits.

Now the tab switching:

```js
const tabs=[...document.querySelectorAll('.tab')];
function selectTab(id){ tabs.forEach(t=>{const on=t.dataset.tab===id; t.setAttribute('aria-selected',on); document.getElementById('p-'+t.dataset.tab).hidden=!on;}); document.body.classList.toggle('on-draft', id==='draft'); if(id==='draft') renderDraft(); }
```

Arrow keys on tablist.

Rail hidden on draft: CSS `body.on-draft #rail{display:none}`.

Search events:

```js
q.addEventListener('keydown',e=>{ if(e.key==='Enter'){runSearch();} if(e.key==='ArrowDown'&&!q.value){e.preventDefault(); focus first example;} });
q.addEventListener('input',()=>{ if(q.value) hideSyntax(); });
q.addEventListener('focus',()=>{ if(!q.value) showSyntax(); });
q.addEventListener('blur',()=>{ setTimeout(hideSyntax,150); }); // allow example click
```

Examples: buttons with data-q; click → q.value=..., runSearch(). Keydown on examples for arrows: I'll implement roving: examples container keydown ArrowDown/Up moves focus.

Syntax content:

```html
<div class="syntax">
  <p><b>Syntax.</b> A space or AND joins words; OR; NOT or a leading minus; “an exact phrase” in double quotes; parentheses; a star at the end of a word for any ending (child* finds children). Operators in capitals — lower-case “or” is a word.</p>
  <p class="exlbl">Try:</p>
  <button class="ex" data-q='"best interests" AND child'>"best interests" AND child</button>
  <button class="ex" data-q='(torture OR ill-treatment) NOT detention'>(torture OR ill-treatment) NOT detention</button>
  <button class="ex" data-q='"reasonable accommodation"'>"reasonable accommodation"</button>
</div>
```

Hint under box (always visible): the normalization hint.

Echo line after search: `#echo` textContent = state.error? '' : (tree? (root NOT? `Paragraphs without ${echo(tree.a)}.` : `Paragraphs containing ${echo(tree)}.`) : 'No search words — the filters alone decide.');

Hmm spec: "After a search, a line echoes the query as understood: 'Paragraphs containing the phrase “best interests” and the word child'." Good.

Error: `#qerror` shows message, results cleared.

runSearch:

```js
function runSearch(){
  state.searched=true; state.shown=25; state.openId=null; state.fullId=null; state.storedId=null; state.ctxId=null;
  const q=qInput.value.trim();
  state.query=q;
  if(!q){ state.tree=null; state.error=null; }
  else { try{ state.tree=parse(q); state.error=null; }catch(e){ state.tree=null; state.error=e.message||String(e); } }
  refresh();
}
```

refresh():

```js
function refresh(){
  // hits
  state.hits = state.error? [] : R.filter(r=> (!state.tree || evalTree(state.tree,r._norm)) && passFilters(r));
  // committee counts
  state.comCounts={}; allCodes.forEach(c=>state.comCounts[c]=0);
  state.hits.forEach(h=>h._committees.forEach(c=>{ if(c in state.comCounts) state.comCounts[c]++; }));
  // highlight regexes
  const terms=[]; collectTerms(state.tree,terms); state.hlTerms=terms;
  state.hlRe = terms.length? new RegExp(terms.map(termPatternShown).join('|'),'giu') : null;
  state.hlReTest = terms.length? new RegExp(terms.map(termPatternShown).join('|'),'iu') : null;
  state.hits.forEach(h=>{ h._mc = state.hlRe? countMatches(h._shown):0; });
  // sort
  const cmp=orders[state.order]; state.hits.sort(cmp);
  renderRail(); renderChart(); renderResults(); renderChecks(); updateHeaderDot();
}
```

Wait — sorting hits in place mutates; fine.

But note: hits sorted by 'match' uses _mc computed — ok.

renderRail: hitCount text = hits.length.toLocaleString + " matching paragraphs" + "of 7,304". Spec: big number "279 matching paragraphs" of "7,304". I'll do big number + small "matching paragraphs · of 7,304". aria-live on the count container.

Chips render. Checkbox brackets: if state.searched → `[${comCounts[c]}]`.

renderChart: labels = allCodes sorted by count desc (then alpha); data counts. Update chart.data, aria-label, table, jointNote hidden toggle. If chart not yet created, create.

Chart creation after DOM ready; allCodes known at load.

renderResults: summary, rows, more button visibility.

renderChecks: run checks, render lines, quirks (static, rendered once), update header dot + tab04 dot.

Also update draft tab count label: `03 DRAFT (${n})` — I'll have span inside tab 03: `<button class="tab" data-tab="draft">03 DRAFT <span id="dtab">(0)</span></button>` — update text: if n>0 show `(n)` else ''. Spec: tab name carries count "03 DRAFT (4)". I'll always show (n).

Now row interactions via delegation:

```js
resultsEl.addEventListener('click', e=>{
  const btn=e.target.closest('button[data-act]');
  const rowHead=e.target.closest('.rowhead');
  if(btn){
    const id=btn.closest('.row').dataset.id; const r=byId[id];
    const act=btn.dataset.act;
    if(act==='cite') copyText(citation(r), 'Copied citation: '+citation(r));
    else if(act==='quote'){ const t='“'+copyBody(r)+'” '+citation(r); copyText(t,'Copied quotation: '+t); }
    else if(act==='draft') addToDraft(r);
    else if(act==='stored'){ state.storedId = state.storedId===id? null:id; renderResults(); }
    else if(act==='full'){ state.fullId=id; renderResults(); }
    else if(act==='prev'||act==='next'){ showContext(r, act); }
    e.stopPropagation();
    return;
  }
  if(rowHead){ state.openId = state.openId===rowHead.closest('.row').dataset.id? null: rowHead.closest('.row').dataset.id; renderResults(); }
});
```

Hmm re-render on every toggle loses scroll? Acceptable.

"Show 25 more": state.shown+=25; renderResults().

Context: showContext(r, which): find same title records sorted by paragraph; idx; target = which==='prev'? idx-1: idx+1; if out of range → live 'no previous paragraph in this document'. Render into `#ctx-${r.id}` — but renderResults wipes it. Instead store state.ctx={id, which} and render inside row when open. I'll do: state.ctxId=id, state.ctxWhich=which; renderResults(); then the row renders ctx box. Simpler: in rowHTML, if state.ctxId===r.id → include context block. Clicking prev/next sets and re-renders.

Context block:

```js
function ctxHTML(r){
  if(state.ctxId!==r.id) return '';
  const same=R.filter(x=>x.title===r.title).sort((a,b)=>a.paragraph-b.paragraph);
  const i=same.findIndex(x=>x.id===r.id);
  const t=same[i+(state.ctxWhich==='prev'?-1:1)];
  if(!t) return '<div class="ctxbox grey">no '+state.ctxWhich+' paragraph in this document</div>';
  return `<div class="ctxbox"><div class="grey">context · <span class="pin">${t._pinpoint}</span> · ${t.year}</div><p class="ctxt">${highlightHTML(t._shown,state.hlTerms)}</p></div>`;
}
```

copyText:

```js
async function copyText(t,msg){
  try{ await navigator.clipboard.writeText(t); live(msg); }
  catch(e){
    clipFallback.hidden=false; clipText.value=t; clipText.focus(); clipText.select();
    live('Clipboard refused — the text is in the box below; select and copy it.');
  }
}
function live(m){ liveEl.textContent=m; }
```

Draft:

```js
function addToDraft(r){
  if(state.draft.some(d=>d.id===r.id)){ live('Already in your draft: '+citation(r)); return; }
  const c=citation(r);
  const item={id:r.id, citation:c, quotation:'“'+copyBody(r)+'” '+c, symbol:r.symbol, paragraph:r.paragraph, pinpoint:r._pinpoint, committee:r.committee, short_title:r.short_title, year:r.year, text_copied:copyBody(r), text_as_stored:r.text, doc_url:r.doc_url};
  state.draft.push(item); saveDraft(); updateDraftTab(); if(currentTab==='draft') renderDraft();
  live('Added to draft: '+c);
}
```

renderDraft: list items; remove buttons delegation.

Downloads:

```js
function csvCell(v){ return '"'+String(v==null?'':v).replace(/"/g,'""')+'"'; }
function draftCSV(){
  const head=['citation','symbol','paragraph','pinpoint','committee','short_title','year','text_copied','text_as_stored','doc_url'];
  const rows=state.draft.map(d=>head.map(k=>csvCell(d[k])).join(','));
  return '\uFEFF'+[head.map(csvCell).join(','),...rows].join('\r\n');
}
```

TXT: copyAll text.

Now the chart plugin for value labels:

```js
const valLabels={id:'vallabels', afterDatasetsDraw(chart){
  const meta=chart.getDatasetMeta(0); const ctx=chart.ctx;
  ctx.save(); ctx.font='12px ui-monospace, Menlo, Consolas, monospace'; ctx.fillStyle='#1d1b18'; ctx.textBaseline='middle';
  meta.data.forEach((bar,i)=>{
    const v=chart.data.datasets[0].data[i];
    const x=Math.max(bar.x,bar.base)+5;
    ctx.fillText(String(v), x, bar.y);
  });
  ctx.restore();
}};
```

For indexAxis 'y', bar.x is the value-end pixel? In Chart.js 4 horizontal bar element: properties x (end), y (center), base (start), width/height. Yes for horizontal, `x` is where value ends. Good.

Chart options:

```js
options:{
  indexAxis:'y',
  responsive:true, maintainAspectRatio:false,
  onClick(evt,els){ if(els&&els.length){ const code=chart.data.labels[els[0].index]; setCommitteesOnly(code); } },
  plugins:{ legend:{display:false}, tooltip:{callbacks:{label:(c)=>' '+c.parsed.x+' paragraphs'} } },
  scales:{
    x:{ beginAtZero:true, grid:{color:'#d9d2c3'}, ticks:{color:'#1d1b18', maxTicksLimit:10, precision:0}, border:{color:'#d9d2c3'} },
    y:{ grid:{display:false}, ticks:{color:'#1d1b18', font:{family:'ui-monospace, Menlo, Consolas, monospace', size:12}}, border:{display:false} }
  }
}
```

Container height: set style height = allCodes.length*30+60 px.

aria-label update: `fig1.setAttribute('aria-label', 'Paragraphs per committee: '+labels.map((l,i)=>l+' '+data[i]).join(', '))`.

Table: rebuild tbody.

setCommitteesOnly(code): state.committees=new Set([code]); sync checkboxes; refresh(). Note: refresh keeps query — good ("click a bar = tick that committee alone").

Checkbox sync: clist inputs checked = state.committees.has(code).

all/none buttons.

Year inputs: on change → state.yearFrom=+yFrom.value etc; clamp; refresh.

Doc select: on change → state.doc=value; refresh.

Chips: render function; chip × buttons: data-chip type; click → reset that filter; refresh.

Clear all: reset committees all, years, doc, query input '', runSearch().

Now passFilters:

```js
function passFilters(r){
  if(!r._committees.some(c=>state.committees.has(c))) return false;
  if(r.year<state.yearFrom||r.year>state.yearTo) return false;
  if(state.doc && (r.committee+'||'+r.short_title)!==state.doc) return false;
  return true;
}
```

Initial state: committees = all codes; yearFrom=minY; yearTo=maxY; doc=''.

allCodes: distinct r.committee sorted. But committeesOf may add codes not in committee field? e.g. symbol "CAT/OP/..." with committee "CAT-OP" — same. Joint "CMW/C/GC/7–CERD/C/GC/38" committee maybe "CMW/CERD"? Description says "one committee". Hmm — joint GC has one `committee` field but two symbols. committeesOf extracts both codes from symbol → record counts under both. The checkbox list from distinct committee field might miss CERD if no record has committee==='CERD'... but CERD surely has its own GCs. To be safe, build allCodes from union of committeesOf over all records. That includes CAT-OP etc. Use that for checkboxes and chart. And "k committees" in header = distinct committee field (10). Fine.

Wait — committeesOf regex on symbol "CMW/C/GC/7–CERD/C/GC/38": matches CMW and CERD. Good. On "CRC/C/GC/23, CMW/C/GC/4": CRC, CMW. Good.

But careful: symbol "A/48/18" has no codes → committees = [committee field]. Good.

Also CEDAW vs CED: symbol "CEDAW/C/GC/..." → regex alternation has CEDAW before CED? Order in my alternation: (CAT-OP|CCPR|CEDAW|CED|CERD|CESCR|CMW|CRC|CRPD|CAT). At position of "CEDAW", tries CAT-OP no, CCPR no, CEDAW yes → matches CEDAW. Good. "CED/C/GC/..." → CEDAW no (CED then A? "CED/" — CEDAW requires A after CED; next is '/', so CEDAW fails, CED matches). Good.

Now the header check dot: 

```js
function updateHeaderDot(){
  const res=lastChecks; const pass=res.filter(c=>c.pass).length, fail=res.length-pass;
  dotEl.innerHTML = fail? `<span class="dot red"></span> ${fail} of ${res.length} checks failed` : `<span class="dot green"></span> ${pass} checks pass`;
  tab04dot.hidden = fail===0; // red dot on tab 04
}
```

Spec: green dot "n checks pass" or red "n checks failed" (and a red dot on tab 04). I'll show red dot on tab 04 when fail>0.

Now sizes: fine.

Let me also handle `doc_url` empty? gc records all have doc_url presumably. Link only if present: if r.doc_url → link else plain symbol text.

Row heading: badges for each committee in r._committees (usually 1; joint shows both badges). Plus short_title. 

Row meta line: symbol link · pinpoint (red) · year. Also type? gc has no type. OK.

Let me now also compute _pinpoint etc. in precompute loop:

```js
R.forEach(r=>{
  r._shown=r.text.replace(FN,'');
  r._marks=(r.text.match(/\[\[fn:/g)||[]).length;
  r._norm=normalize(r.text);
  const lm=r.text.match(/^(\d{1,3})\.\s/); r._leading=lm?lm[1]:null;
  const am=r.text.match(/^\(([a-z]{1,4})\)/); r._lettered=am?am[1]:null;
  r._pinpoint = r.paragraph===0 ? 'preamble' : (r._lettered? 'subpara. ('+r._lettered+')' : 'para. '+r.paragraph);
  r._committees=committeesOf(r);
  r._joint = (r.symbol.match(/CAT\/OP|CCPR|CEDAW|CED|CERD|CESCR|CMW|CRC|CRPD|CAT/g)||[]).length>=2;
  r._shared = symTitles[r.symbol].size>1;
  byId[r.id]=r;
});
```

Wait _joint: count codes in symbol; but "CAT/OP" contains CAT — the match list for "CAT/OP/C/..." would give ['CAT/OP','CAT']? The regex alternation CAT/OP first: at "CAT/OP", matches "CAT/OP" (consumes through P), so no separate CAT. Good. But symbol "CAT/C/GC/1" → ['CAT']. Good. Joint detection: codes in symbol ≥2. But careful: a symbol like "CRC/C/GC/23, CMW/C/GC/4" → 2 → joint. Good.

_dupPin: after loop, group by title|paragraph.

Also note: paragraph 0 preamble — pinpoint 'preamble'; lettered check before paragraph? If paragraph===0 AND lettered? unlikely; order: paragraph===0 → preamble first. Spec: "preamble when paragraph is 0; subpara. (b) when text starts with a lettered label". OK.

Citation function uses r._shared, r._pinpoint, docName(r.title).

Now, "the document's number" for shared: docName gives "General Recommendation No. 29". Good.

Now writing the final HTML. Also include `<meta name="color-scheme" content="light">`? optional.

Let me make sure the search input has label. And focus on load: `qInput.focus()` at end — but syntax dropdown shows on focus when empty. Good.

Edge: `state.order` default 'year'.

Order select change → state.order=value; refresh() (re-sort; keep shown? reset shown=25? keep shown). I'll keep shown.

More button: hidden when shown>=hits.length.

Summary line: 

```js
const comms=new Set(state.hits.map(h=>h.committee)).size;
const ys=state.hits.map(h=>h.year); const y1=Math.min(...ys), y2=Math.max(...ys);
```

Careful with empty hits: guard. If hits empty: "0 of 7,304 paragraphs match". 

Summary text: 
- if !state.query && !state.error: `no search words · ${n} of ${R.length} paragraphs pass the filters · ${comms} committees · ${y1}–${y2}`
- else: `${n} of ${R.length} paragraphs match · ${comms} committees · ${y1}–${y2}`
Then order line separate: `sorted by ...` — I'll append: ` · sorted by ${orderText}`. Spec has them as separate lines; I'll put order text in the select label area: `<label>order <select>…</select></label>` and a line "sorted by year, newest first, then by document and paragraph" as part of summary second sentence. I'll render summary as one <p> with two sentences.

orderText map: year: 'year, newest first, then by document and paragraph'; doc: 'document, then paragraph'; match: 'most matches first'.

Now the "How this is computed" lines: under chart (done), under big number? Add near results: the retrieval hint (done). 

Tab 04 content:

```html
<section id="p-check" role="tabpanel" hidden>
  <h2>How the app checks itself</h2>
  <p class="hint">Each line compares two computations done by this page. A failed check marks rows; it never drops them.</p>
  <div id="checks"></div>
  <h2>Known quirks of this file</h2>
  <p class="hint">Computed at load, before any search.</p>
  <ul id="quirks"></ul>
  <h2>How this is computed</h2>
  <div class="method"> ... short paragraphs ... </div>
  <h2>Sources consulted</h2>
  <ul class="srcs">4 items</ul>
</section>
```

Method text: normalization, parser, matching, highlight, citation, copy — short.

Now let me count clickable things roughly — fine.

One more: "the search box has focus on load" — call qInput.focus() after init.

Also `aria-live` on hitCount container, summary, live.

Let me write the CSS fully:

```css
:root{--paper:#f4f0e8;--ink:#1d1b18;--rule:#d9d2c3;--red:#9b2335;--green:#2e6b3e;--amber:#8a5a00;--grey:#6f6a60;--mark:#f2e39b;}
*{box-sizing:border-box}
[hidden]{display:none!important}
html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--paper);color:var(--ink);font:16px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
a{color:var(--red)}
:focus-visible{outline:2px solid var(--red);outline-offset:2px}
header{padding:22px 28px 14px;border-bottom:1px solid var(--rule)}
.kicker{font:11px/1 ui-monospace,Menlo,Consolas,monospace;letter-spacing:.14em;text-transform:uppercase;color:var(--grey)}
h1{font-family:Georgia,"Times New Roman",serif;font-weight:400;font-size:32px;margin:8px 0 6px;max-width:900px}
.meta{font-size:13px;color:var(--grey);display:flex;flex-wrap:wrap;gap:8px;align-items:center}
.dot{display:inline-block;width:9px;height:9px;border-radius:50%;margin-right:5px;vertical-align:baseline}
.dot.green{background:var(--green)} .dot.red{background:var(--red)}
#live{font:11px/1.4 ui-monospace,Menlo,Consolas,monospace;color:var(--red);min-height:14px;margin-top:4px;max-width:900px}
.layout{display:flex;align-items:flex-start}
#rail{flex:0 0 300px;width:300px;border-right:1px solid var(--rule);padding:18px 20px 40px;position:sticky;top:0;max-height:100vh;overflow:auto}
body.on-draft #rail{display:none}
main{flex:1;min-width:0;padding:18px 28px 60px}
.tabs{display:flex;gap:4px;border-bottom:1px solid var(--rule);flex-wrap:wrap}
.tab{font:12px/1 ui-monospace,Menlo,Consolas,monospace;letter-spacing:.1em;text-transform:uppercase;background:none;border:none;border-bottom:2px solid transparent;padding:10px 12px;cursor:pointer;color:var(--ink)}
.tab[aria-selected="true"]{color:var(--red);border-bottom-color:var(--red)}
.tab .tdot{color:var(--red)}
section{padding-top:18px}
h2{font-family:Georgia,serif;font-weight:400;font-size:22px;margin:18px 0 8px}
...
```

Rail internals:

```css
.railhead{display:flex;justify-content:space-between;align-items:baseline}
.lbl{font:11px/1 ui-monospace,...;letter-spacing:.14em;color:var(--grey)}
button.link{background:none;border:none;color:var(--red);font:11px ui-monospace;cursor:pointer;text-decoration:underline}
.big{font-family:Georgia,serif;font-size:52px;line-height:1;margin:14px 0 2px}
.bigsub{font:11px ui-monospace;color:var(--grey);letter-spacing:.08em}
#chips{display:flex;flex-wrap:wrap;gap:6px;margin:10px 0}
.chip{font:11px ui-monospace;border:1px solid var(--red);color:var(--red);padding:3px 6px;display:inline-flex;gap:6px;align-items:center}
.chip button{background:none;border:none;color:var(--red);cursor:pointer;font:11px ui-monospace;padding:0}
.search label{...}
.qwrap{display:flex;gap:6px;margin:6px 0}
#q{flex:1;min-width:0;font:14px ui-monospace,Menlo,Consolas,monospace;padding:8px;border:1px solid var(--rule);background:#fff;color:var(--ink)}
#go{...btn}
.btn{font:12px ui-monospace;letter-spacing:.06em;border:1px solid var(--ink);background:none;color:var(--ink);padding:7px 12px;cursor:pointer}
.btn:hover{border-color:var(--red);color:var(--red)}
.hint{font:11.5px/1.5 ui-monospace,Menlo,Consolas,monospace;color:var(--grey);margin:6px 0}
.echo{font:12px ui-monospace;color:var(--ink);margin:8px 0 0}
.err{font:12px ui-monospace;color:var(--red);margin:6px 0}
.syntax{border:1px solid var(--rule);background:#efe9dd;padding:10px;margin-top:6px}
.syntax p{font:12px/1.5 ui-monospace;margin:0 0 8px}
.ex{display:block;width:100%;text-align:left;background:none;border:none;border-top:1px solid var(--rule);font:12px ui-monospace;color:var(--red);padding:6px 2px;cursor:pointer}
.fhead{width:100%;display:flex;gap:8px;align-items:baseline;background:none;border:none;border-top:1px solid var(--rule);padding:12px 0 6px;cursor:pointer;font:12px ui-monospace;letter-spacing:.1em;color:var(--ink);text-transform:uppercase}
.fhead .n{color:var(--red)}
#fbody{padding:4px 0 10px}
.clist{display:flex;flex-direction:column;gap:2px;max-height:260px;overflow:auto}
.clist label{display:flex;gap:7px;align-items:baseline;font-size:13px;cursor:pointer;padding:2px 0}
.clist input{accent-color:var(--red)}
.clist .code{font:11px ui-monospace;min-width:52px}
.clist .hits{color:var(--red);font:11px ui-monospace}
.allnone{display:flex;gap:8px;margin:2px 0 8px}
.allnone button{...link style}
.years{display:flex;gap:10px;margin:10px 0}
.years input{width:70px;font:13px ui-monospace;padding:4px;border:1px solid var(--rule);background:#fff}
.doclbl{display:block;font:11px ui-monospace;letter-spacing:.1em;color:var(--grey);margin-top:8px}
#docSel{width:100%;font:13px sans-serif;padding:5px;border:1px solid var(--rule);background:#fff;margin-top:4px}
```

Results:

```css
.sumrow{display:flex;flex-wrap:wrap;gap:14px;align-items:baseline;justify-content:space-between}
#summary{font-size:15px;margin:0}
.orderlbl{font:11px ui-monospace;color:var(--grey)}
#orderSel{font:12px ui-monospace;padding:4px;border:1px solid var(--rule);background:#fff}
.row{border-top:1px solid var(--rule);padding:14px 0 12px}
.row:first-child{border-top:none}
.rowhead{cursor:pointer;display:flex;flex-wrap:wrap;gap:8px;align-items:baseline}
.badge{font:10.5px ui-monospace;letter-spacing:.06em;border:1px solid var(--ink);padding:2px 6px;color:var(--ink)}
.rowtitle{font-family:Georgia,serif;font-size:16px}
.meta{font:12px ui-monospace;color:var(--grey);margin:6px 0;display:flex;flex-wrap:wrap;gap:10px}
.meta a{color:var(--red);text-decoration:none;border-bottom:1px solid var(--rule)}
.pin{color:var(--red)}
.rtext{white-space:pre-wrap;margin:8px 0 4px;font-size:15px}
mark{background:var(--mark);color:var(--ink);font-weight:700;padding:0 1px}
.marksline{font:11px ui-monospace;color:var(--grey)}
.marksline button{...link}
.note{font:12px ui-monospace;color:var(--amber);margin:4px 0}
.actions{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin-top:8px}
.actions .btn{padding:5px 10px;font-size:11px}
.ctx{font:11px ui-monospace;color:var(--grey)}
.ctx button{link style}
.ctxbox{margin-top:8px;border-left:2px solid var(--rule);padding-left:12px;color:var(--grey)}
.ctxt{white-space:pre-wrap;font-size:14px}
.styleNote{font:11px ui-monospace;color:var(--grey);margin-top:6px}
#more{margin:14px 0}
```

Draft:

```css
.ditem{border-top:1px solid var(--rule);padding:12px 0}
.dq{font-family:Georgia,serif;font-size:16px;margin:0 0 4px;white-space:pre-wrap}
.dc{font:12px ui-monospace;color:var(--grey)}
.dc button{link}
.btnrow{display:flex;gap:8px;flex-wrap:wrap;margin:14px 0}
```

Checks:

```css
.check{display:flex;gap:10px;padding:8px 0;border-top:1px solid var(--rule);font-size:14px}
.check .tag{font:11px ui-monospace;flex:0 0 110px}
.check.pass .tag{color:var(--green)} .check.fail .tag{color:var(--red)}
.check .det{color:var(--grey);font-size:13px}
#quirks li{font-size:14px;margin:4px 0}
```

Fig:

```css
.fighead{display:flex;gap:10px;align-items:baseline}
.figno{font:12px ui-monospace;color:var(--red);letter-spacing:.1em}
.figtitle{font-family:Georgia,serif;font-size:20px;margin:0}
.figrow{display:flex;gap:24px;align-items:flex-start;flex-wrap:wrap;margin-top:10px}
.chartwrap{flex:1 1 420px;min-width:300px}
#fig1wrap{position:relative}
table.figtable{border-collapse:collapse;font-size:13px;flex:0 1 260px}
.figtable caption{text-align:left;font:11px ui-monospace;color:var(--grey);padding-bottom:6px}
.figtable th,.figtable td{border-bottom:1px solid var(--rule);padding:4px 10px 4px 0;text-align:left}
.figtable td.num,.figtable th.num{text-align:right}
```

Footer:

```css
footer{border-top:1px solid var(--rule);padding:12px 28px;font:11px/1.6 ui-monospace;color:var(--grey)}
```

Clipboard fallback:

```css
#clipfallback{position:fixed;left:12px;bottom:12px;right:12px;background:var(--paper);border:1px solid var(--red);padding:10px;z-index:9}
#clipfallback textarea{width:100%;font:12px ui-monospace}
```

OK. Now assemble the JS in order:

1. Data + constants + precompute
2. Helpers (escHtml, escRe, normalize, committeesOf, docName, citation, copyBody)
3. Query tokenizer/parser/echo/termRegexNorm/evalTree/collectTerms/termPatternShown/highlightHTML/countMatches
4. State
5. DOM refs
6. Build rail (checkbox list, doc select, years)
7. Chart init
8. refresh + render functions
9. Events
10. Init: quirks render, runSearch (empty), focus.

Careful: chart init needs container sized; create once with allCodes labels (counts computed in refresh). I'll create chart after first hits computed: in refresh, if !chart create with current data else update.

Let me handle `renderChart`:

```js
function renderChart(){
  const entries=allCodes.map(c=>[c,state.comCounts[c]||0]).sort((a,b)=>b[1]-a[1]||a[0].localeCompare(b[0]));
  const labels=entries.map(e=>e[0]), data=entries.map(e=>e[1]);
  const alabel='Paragraphs per committee: '+entries.map(e=>e[0]+' '+e[1]).join(', ');
  fig1.setAttribute('aria-label',alabel);
  if(!chart){
    chartWrap.style.height=(labels.length*30+50)+'px';
    chart=new Chart(fig1.getContext('2d'),{type:'bar',data:{labels,datasets:[{label:'paragraphs',data,backgroundColor:'#9b2335'}]},options:{...},plugins:[valLabels]});
  } else {
    chart.data.labels=labels; chart.data.datasets[0].data=data; chart.update();
  }
  // table
  figTable.innerHTML='<caption>FIG.01 — same numbers as the chart</caption><thead><tr><th scope="col">Committee</th><th scope="col" class="num">Paragraphs</th></tr></thead><tbody>'+entries.map(e=>`<tr><td>${escHtml(e[0])}</td><td class="num">${e[1].toLocaleString('en-US')}</td></tr>`).join('')+'</tbody>';
  jointNote.hidden = !(state.hits.reduce((s,h)=>s+(h._committees.length-1),0)>0);
}
```

Note: chart onClick uses labels index — after update fine.

Hmm: chart height fixed at creation based on labels length (constant allCodes) — fine.

renderRail:

```js
function renderRail(){
  hitCount.textContent=state.hits.length.toLocaleString('en-US');
  hitWrap.setAttribute('aria-label', state.hits.length+' matching paragraphs of '+R.length);
  // chips
  let chips='';
  if(state.committees.size<allCodes.length) chips+=chip('committees', `committees: ${state.committees.size} of ${allCodes.length}`,'c');
  if(state.yearFrom>minY||state.yearTo<maxY) chips+=chip('years',`years ${state.yearFrom}–${state.yearTo}`,'y');
  if(state.doc) chips+=chip('doc',`document: ${state.doc.split('||')[1]}`,'d');
  chipsEl.innerHTML=chips;
  // checkbox brackets
  document.querySelectorAll('#clist input').forEach(cb=>{
    const c=cb.value; const s=cb.parentElement.querySelector('.hits');
    s.textContent = state.searched? ` [${state.comCounts[c]||0}]` : '';
  });
}
```

chip html: `<span class="chip">${label}<button data-chip="${type}" aria-label="remove filter">×</button></span>`.

Chips delegation on chipsEl.

renderResults:

```js
function renderResults(){
  const n=state.hits.length;
  const comms=new Set(state.hits.map(h=>h.committee)).size;
  let s;
  if(n===0){ s = state.error? '' : '0 paragraphs pass.'; }
  else {
    const ys=state.hits.map(h=>h.year);
    const y1=Math.min(...ys), y2=Math.max(...ys);
    s = (state.query&&!state.error) ? `${n.toLocaleString('en-US')} of ${R.length.toLocaleString('en-US')} paragraphs match · ${comms} committees · ${y1}–${y2}` : `no search words · ${n.toLocaleString('en-US')} of ${R.length.toLocaleString('en-US')} paragraphs pass the filters · ${comms} committees · ${y1}–${y2}`;
  }
  if(state.error) s='';
  summaryEl.innerHTML = escHtml(s) + (s? ` <span class="hint" style="display:inline">· sorted by ${orderText[state.order]}</span>`:'');
  ...
}
```

Hmm keep simpler: summary textContent = s; separate span for order. Let me structure: `<p id="summary" aria-live="polite"></p>` set textContent = s + (s? ' · sorted by '+orderText[state.order] : ''). Fine.

Rows:

```js
const slice=state.hits.slice(0,state.shown);
resultsEl.innerHTML=slice.map(rowHTML).join('');
moreBtn.hidden = state.shown>=n;
moreBtn.textContent=`Show 25 more (${Math.min(25,n-state.shown)} of ${n-state.shown} left)` — simpler: 'Show 25 more';
```

rowHTML(r):

```js
function rowHTML(r){
  const open=state.openId===r.id;
  const badges=r._committees.map(c=>`<span class="badge">${escHtml(c)}</span>`).join(' ');
  const sym = r.doc_url? `<a href="${escHtml(r.doc_url)}" target="_blank" rel="noopener">${escHtml(r.symbol)}</a>` : escHtml(r.symbol);
  const notes=[];
  if(r._leading&&Number(r._leading)!==r.paragraph) notes.push(`the text begins ‘${r._leading}’ but the record is para. ${r.paragraph}: check the document`);
  if(r._lettered) notes.push(`a lettered sub-paragraph, numbered ${r.paragraph} by the file`);
  if(r._dupPin) notes.push('two records share this pinpoint');
  if(r._joint) notes.push('joint General Comment');
  // text
  const stored=state.storedId===r.id;
  const full=state.fullId===r.id;
  let raw=stored?r.text:r._shown;
  let trunc=false;
  if(!full&&raw.length>700){ const cut=raw.slice(0,700); const sp=cut.lastIndexOf(' '); raw=(sp>400?cut.slice(0,sp):cut)+' …'; trunc=true; }
  const words=r._shown.split(/\s+/).length;
  const textHtml=highlightHTML(raw,state.hlTerms);
  const marksLine = r._marks>0 ? `<div class="marksline">${r._marks} footnote mark${r._marks>1?'s':''} removed · <button data-act="stored">${stored?'show as printed (marks removed)':'show as stored'}</button></div>` : '';
  const fullLine = trunc? `<div class="marksline"><button data-act="full">Show the full paragraph (${words.toLocaleString('en-US')} words)</button></div>` : (state.fullId===r.id? `<div class="marksline"><button data-act="full">Show less</button></div>`:'');
  const actions = open? `
    <div class="actions">
      <button class="btn" data-act="cite">Copy citation</button>
      <button class="btn" data-act="quote">Copy quotation</button>
      <button class="btn" data-act="draft">Add to draft</button>
      <span class="ctx">Context: <button data-act="prev">previous</button> | <button data-act="next">next</button></span>
    </div>
    <div class="styleNote">citation style: UN short form — symbol and pinpoint stored separately, formatted on copy</div>
    ${ctxHTML(r)}` : '';
  return `<article class="row" data-id="${escHtml(r.id)}">
    <div class="rowhead">${badges}<span class="rowtitle">${escHtml(r.short_title)}</span></div>
    <div class="meta"><span>${sym}</span><span class="pin">${escHtml(r._pinpoint)}</span><span>${r.year}</span></div>
    <p class="rtext">${textHtml}</p>
    ${marksLine}${fullLine}
    ${notes.map(n=>`<div class="note">⚠ ${escHtml(n)}</div>`).join('')}
    ${actions}
  </article>`;
}
```

Wait: rowhead click toggles open — but rowhead contains only badges+title; clicking text shouldn't toggle? Spec: "A click on a row opens it in place". I'll make whole article header area clickable: put click handler on `.row` but ignore clicks on buttons/links/mark? Clicking text to select would toggle — annoying. I'll attach toggle to `.rowhead` and `.meta` — wrap them in a `.rowtop` div with cursor pointer. Let me add `<div class="rowtop">` containing rowhead+meta. Click on rowtop toggles.

Also amber note marker: use "▲" or just text. Use "note:" prefix. I'll use `⚠` fine.

ctxHTML as designed; also include symbol link? skip.

Now events wiring. Also `#more` click.

Order select change: state.order=val; refresh().

Wait refresh() re-sorts hits — but hits array was filtered fresh each refresh, ok.

Also when filters change (checkbox etc.) → refresh() without resetting shown? Keep shown reset to 25 for consistency: I'll reset shown=25 in refresh? But "Show 25 more" calls refresh? No — more button just increases shown and calls renderResults only. Let me separate: refresh(full=true) resets shown. Filter changes call refresh() (reset shown=25). More button: state.shown+=25; renderResults(); renderChecks()? Checks reference rendered count... check 2 uses recount vs hits — independent of shown. Fine, more button only renderResults.

Actually simpler: refresh() always resets shown=25 except when called from more-button path. I'll have renderAll(resetShown).

Let me define:

```js
function applyAll(reset=true){ if(reset){state.shown=25;state.openId=null;state.fullId=null;state.storedId=null;state.ctxId=null;} computeAndRender(); }
```

runSearch → applyAll(true). Filter changes → applyAll(true). More → state.shown+=25; renderResults(); (checks unaffected).

computeAndRender: hits, comCounts, hl regexes, _mc, sort, renderRail, renderChart, renderResults, renderChecks, updateHeaderDot.

renderChecks also updates header dot.

Init: build static DOM (checkboxes, doc select, years), render quirks, applyAll(true) with empty query (searched=false initially → brackets hidden until first search; but applyAll at load sets searched? runSearch sets searched=true. At load I'll call applyAll without setting searched → brackets hidden. Then user search sets searched. But filter changes before search — brackets still hidden until a search. Fine.)

Hmm but initial hits = all records (tree null) — chart shows full distribution. Good.

Draft tab count update: `dtab.textContent='('+state.draft.length+')'`.

renderDraft:

```js
function renderDraft(){
  dcount.textContent=state.draft.length;
  if(!state.draft.length){ draftList.innerHTML='<p class="hint">Nothing collected yet. Open 02 PARAGRAPHS, click a row, and choose “Add to draft”.</p>'; return; }
  draftList.innerHTML=state.draft.map((d,i)=>`<div class="ditem"><p class="dq">${escHtml(d.quotation)}</p><p class="dc">${escHtml(d.citation)} · <button data-rm="${i}">remove</button></p></div>`).join('');
}
```

Remove delegation.

copyAll:

```js
function draftText(){ return state.draft.map(d=>d.quotation+'\n'+d.citation).join('\n\n'); }
```

copyAll click → copyText(draftText(), 'Copied all '+state.draft.length+' quotations to the clipboard.'). If empty → live 'draft is empty'.

Downloads: download('gc-quotations.txt', '\uFEFF'+draftText(), 'text/plain;charset=utf-8'); csv: download('gc-quotations.csv', draftCSV(), 'text/csv;charset=utf-8').

Now the checks render:

```js
function renderChecks(){
  const checks=runChecks(); lastChecks=checks;
  checksEl.innerHTML=checks.map(c=>`<div class="check ${c.pass?'pass':'fail'}"><span class="tag">${c.pass?'pass':'check failed'}</span><span><b>${escHtml(c.label)}.</b> <span class="det">${escHtml(c.detail)}</span></span></div>`).join('');
  const pass=checks.filter(c=>c.pass).length, fail=checks.length-pass;
  dotEl.innerHTML = fail? `<span class="dot red"></span>${fail} of ${checks.length} checks failed` : `<span class="dot green"></span>${pass} checks pass`;
  t04dot.hidden = fail===0;
}
```

Quirks render once:

```js
function renderQuirks(){
  const items=[
    ['preambles (paragraph 0), cited as “preamble”', p0.length, p0[0]&&`${p0[0].symbol}, preamble`],
    ['symbols shared by several General Comments (citation adds committee and number)', sharedSyms.length, sharedSyms[0]&&sharedSyms[0][0]],
    ['joint General Comments (two symbols in one record)', joint.length, joint[0]&&joint[0].symbol],
    ['pinpoints shared by two records of the same document', dups.length, dups[0]&&`${dups[0][0].symbol}, ${dups[0][0]._pinpoint}`],
    ['texts whose leading number differs from the paragraph field', mism.length, mism[0]&&`${mism[0].symbol}, text begins ‘${mism[0]._leading}’, record is para. ${mism[0].paragraph}`]
  ];
  quirksEl.innerHTML=items.map(i=>`<li><b>${i[1]}</b> ${escHtml(i[0])} — e.g. ${escHtml(i[2]||'—')}</li>`).join('');
}
```

Now method text (tab 04):

```html
<div class="method">
<p><b>Normalised text.</b> Each stored paragraph is normalised once at load: footnote marks [[fn:N]] removed; curly quotes and apostrophes → straight; en/em dashes and soft hyphens → "-"; all whitespace (including non-breaking spaces and line breaks) → one space; lower-cased. The query is normalised the same way, so curly quotes pasted from Word still match.</p>
<p><b>Query.</b> Tokens: "phrase" (straight or curly quotes), ( ), AND OR NOT in capitals, a leading - as NOT, any other run of characters as a word with an optional trailing *. Adjacent terms are AND. Precedence NOT &gt; AND &gt; OR; parentheses override. The parser returns a tree and an English echo, or the error shown in the box.</p>
<p><b>Matching.</b> A word becomes a regular expression over the normalised text with letter/number boundaries, so “state” also matches “non-State”; a trailing * allows any ending; a phrase is its words joined by whitespace. A record matches when the tree is true. Whole words only: child does not find children — type child*.</p>
<p><b>Highlight.</b> The same positive terms become one regular expression over the shown text, where quotes, apostrophes and dashes match their straight and curly forms and a gap between phrase words may contain footnote marks; matches are wrapped in mark. NOT terms are never highlighted.</p>
<p><b>Citation and copy.</b> Citation = symbol + pinpoint (“para. N”, “preamble”, “subpara. (b)”); when a symbol is shared by several General Comments, the committee and the document's name come first and the symbol goes in parentheses. Copy uses the clipboard API with a selectable fallback. Nothing is generated: every character shown or copied comes from a record of the file.</p>
</div>
```

Sources consulted list:

```html
<ul class="srcs">
<li>Dag Hammarskjöld Library, Ask DAG: how should I cite a UN document? — ask.un.org/faq/401380 (citation parts stored separately, pinpoint always, style named)</li>
<li>Wikipedia, Help:Searching — phrase in quotes, leading hyphen exclusion, capital OR, trailing star (syntax written fresh for this app)</li>
<li>Chart.js docs, Accessibility of canvas charts — role="img", aria-label with the numbers, fallback table (Chart.js 4, MIT)</li>
<li>UK Government Analysis Function, Data visualisation: charts — bar gaps, ≤10 gridlines, horizontal labels</li>
</ul>
```

Footer credits: "Credits: charting by Chart.js 4 (MIT licence)."

Now — one more detail: "the top-level count is the string '7304'" — use R.length everywhere. Header uses R.length.

Also the header meta: "records.length paragraphs from n General Comments (distinct title) of k committees, year min–max". n=distinct title (188), k=distinct committee (10).

Let me now also handle the case where `D.source_url` missing — guard.

Also `D.built` may be missing — guard.

Time to write the final output. I must keep under ~1500 lines. Let me write compactly but readable.

Also double-check: tab buttons need `role="tab"`, tablist `role="tablist"`, panels `role="tabpanel"` + aria-labelledby. Arrow-key nav:

```js
tablist.addEventListener('keydown',e=>{
  if(e.key!=='ArrowRight'&&e.key!=='ArrowLeft')return;
  const i=tabs.indexOf(document.activeElement); if(i<0)return;
  e.preventDefault();
  const j=(i+(e.key==='ArrowRight'?1:tabs.length-1))%tabs.length;
  tabs[j].focus(); selectTab(tabs[j].dataset.tab);
});
```

selectTab also called on click.

currentTab variable to know if draft render needed.

One more: the syntax dropdown arrow-key navigation: examples are buttons; when input focused and empty, ArrowDown focuses first .ex; within .ex keydown ArrowDown/Up moves among them; Enter triggers click (native button behavior). Esc hides. Implement:

```js
qInput.addEventListener('keydown',e=>{
  if(e.key==='Enter'){e.preventDefault();runSearch();}
  else if(e.key==='ArrowDown'&&!qInput.value){e.preventDefault();const ex=document.querySelector('.ex');if(ex)ex.focus();}
  else if(e.key==='Escape'){syntaxEl.hidden=true;}
});
syntaxEl.addEventListener('keydown',e=>{
  if(e.key==='ArrowDown'||e.key==='ArrowUp'){
    const exs=[...syntaxEl.querySelectorAll('.ex')]; const i=exs.indexOf(document.activeElement);
    if(i>=0){e.preventDefault(); const j=(i+(e.key==='ArrowDown'?1:exs.length-1))%exs.length; exs[j].focus();}
  } else if(e.key==='Escape'){syntaxEl.hidden=true;qInput.focus();}
});
document.querySelectorAll('.ex').forEach(b=>b.addEventListener('click',()=>{qInput.value=b.dataset.q;runSearch();}));
qInput.addEventListener('input',()=>{ if(qInput.value) syntaxEl.hidden=true; });
qInput.addEventListener('focus',()=>{ if(!qInput.value) syntaxEl.hidden=false; });
qInput.addEventListener('blur',()=>{ setTimeout(()=>{ if(!syntaxEl.contains(document.activeElement)) syntaxEl.hidden=true; },120); });
```

OK. Now write everything out. Also ensure `escHtml` for attribute values (quotes): escape `"` too.

escHtml:

```js
const escHtml=s=>String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
```

escRe:

```js
const escRe=s=>s.replace(/[.*+?^${}()|[\]\\]/g,'\\$&');
```

normalize:

```js
function normalize(s){
  return String(s)
    .replace(/\[\[fn:\d+\]\]/g,'')
    .replace(/[“”„]/g,'"')
    .replace(/[‘’‚]/g,"'")
    .replace(/[–—­]/g,'-')
    .replace(/\s+/g,' ')
    .toLowerCase();
}
```

Note: \s+ → ' ' also trims? No, leading/trailing become single space; fine for matching (boundaries handle).

Hmm: normalize removes fn marks — for query too (harmless).

termPatternShown — build from original term value:

```js
function flexChar(ch){
  if(ch==='"'||ch==='“'||ch==='”'||ch==='„')return '["“”„]';
  if(ch==="'"||ch==='‘'||ch==='’'||ch==='‚')return "['‘’‚]";
  if(ch==='-'||ch==='–'||ch==='—'||ch==='­')return '[-–—­]';
  return escRe(ch);
}
function termPatternShown(t){
  if(t.t==='PHRASE'){
    const parts=t.value.split(/\s+/).filter(Boolean).map(w=>[...w].map(flexChar).join(''));
    return '(?<![\\p{L}\\p{N}])'+parts.join('(?:\\s|\\[\\[fn:\\d+\\]\\])+')+'(?![\\p{L}\\p{N}])';
  }
  let w=[...t.value.replace(/\*$/,'')].map(flexChar).join('');
  if(t.wild)w+='\\w*';
  return '(?<![\\p{L}\\p{N}])'+w+'(?![\\p{L}\\p{N}])';
}
```

Edge: phrase empty → parts empty → pattern with empty join → matches boundary-only. Guard in parser: throw on empty phrase.

highlightHTML as designed.

countMatches:

```js
function countMatches(text){
  if(!state.hlRe)return 0;
  state.hlRe.lastIndex=0; let n=0,m;
  while((m=state.hlRe.exec(text))){ n++; if(!m[0])state.hlRe.lastIndex++; }
  return n;
}
```

evalTree with memo:

```js
function evalTree(t,norm){
  if(!t)return true;
  if(t.t==='WORD'||t.t==='PHRASE'){ if(!t._re)t._re=termRegexNorm(t); return t._re.test(norm); }
  if(t.t==='NOT')return !evalTree(t.a,norm);
  if(t.t==='AND')return evalTree(t.a,norm)&&evalTree(t.b,norm);
  return evalTree(t.a,norm)||evalTree(t.b,norm);
}
```

termRegexNorm:

```js
function termRegexNorm(t){
  const v=normalize(t.value);
  if(t.t==='PHRASE'){
    const parts=v.split(/\s+/).filter(Boolean).map(escRe);
    if(!parts.length)throw new QError('Empty phrase in the query.');
    return new RegExp('(?<![\\p{L}\\p{N}])'+parts.join('\\s+')+'(?![\\p{L}\\p{N}])','u');
  }
  let w=escRe(v.replace(/\*$/,''));
  if(t.wild)w+='\\w*';
  return new RegExp('(?<![\\p{L}\\p{N}])'+w+'(?![\\p{L}\\p{N}])','u');
}
```

QError class: `class QError extends Error{}` — catch and use e.message.

Parser as designed with termStart flag.

Echo:

```js
function echo(t){
  if(t.t==='WORD')return t.wild?`words ending in “${t.value.replace(/\*$/,'')}”`:`the word ${t.value}`;
  if(t.t==='PHRASE')return `the phrase “${t.value}”`;
  if(t.t==='NOT')return `without ${echo(t.a)}`;
  if(t.t==='AND')return `${echo(t.a)} and ${echo(t.b)}`;
  return `${echo(t.a)} or ${echo(t.b)}`;
}
function echoLine(){
  if(!state.tree)return 'No search words — the filters alone decide.';
  if(state.tree.t==='NOT')return `Paragraphs without ${echo(state.tree.a)}.`;
  return `Paragraphs containing ${echo(state.tree)}.`;
}
function termCount(t){ if(!t)return 0; if(t.t==='WORD'||t.t==='PHRASE')return 1; if(t.t==='NOT')return termCount(t.a); return termCount(t.a)+termCount(t.b); }
```

collectTerms:

```js
function collectTerms(t,out){
  if(!t||t.t==='NOT')return;
  if(t.t==='WORD'||t.t==='PHRASE'){out.push(t);return;}
  collectTerms(t.a,out);collectTerms(t.b,out);
}
```

Now DOM building for clist:

```js
allCodes.forEach(c=>{
  const lab=document.createElement('label');
  lab.innerHTML=`<input type="checkbox" value="${escHtml(c)}" checked> <span class="code">${escHtml(c)}</span> <span class="cname">${escHtml(COMMITTEE_NAMES[c]||c)}</span> <span class="hits"></span>`;
  clist.appendChild(lab);
});
clist.addEventListener('change',e=>{
  if(e.target.matches('input[type=checkbox]')){
    const set=new Set([...clist.querySelectorAll('input:checked')].map(i=>i.value));
    state.committees=set; applyAll();
  }
});
```

all/none:

```js
allC.onclick=()=>{clist.querySelectorAll('input').forEach(i=>i.checked=true);state.committees=new Set(allCodes);applyAll();};
noneC.onclick=()=>{clist.querySelectorAll('input').forEach(i=>i.checked=false);state.committees=new Set();applyAll();};
```

Empty committees set → hits 0 — fine.

Doc select build:

```js
const groups={};
R.forEach(r=>{(groups[r.committee]=groups[r.committee]||new Set()).add(r.short_title);});
Object.keys(groups).sort().forEach(c=>{
  const og=document.createElement('optgroup'); og.label=c+' — '+(COMMITTEE_NAMES[c]||c);
  [...groups[c]].sort().forEach(st=>{
    const o=document.createElement('option'); o.value=c+'||'+st; o.textContent=st; og.appendChild(o);
  });
  docSel.appendChild(og);
});
```

Years inputs: yFrom.value=minY etc; change → clamp & applyAll.

Chips delegation:

```js
chipsEl.addEventListener('click',e=>{
  const b=e.target.closest('button[data-chip]'); if(!b)return;
  const k=b.dataset.chip;
  if(k==='c'){state.committees=new Set(allCodes);clist.querySelectorAll('input').forEach(i=>i.checked=true);}
  if(k==='y'){state.yearFrom=minY;state.yearTo=maxY;yFrom.value=minY;yTo.value=maxY;}
  if(k==='d'){state.doc='';docSel.value='';}
  applyAll();
});
```

Clear all:

```js
clearAll.onclick=()=>{ qInput.value=''; state.searched=false; ... reset filters ...; applyAll(); };
```

Hmm runSearch sets searched=true; clearAll: set query '', tree null, error null, searched=false, filters reset, applyAll.

Bar click → setCommitteesOnly:

```js
function setCommitteesOnly(code){
  state.committees=new Set([code]);
  clist.querySelectorAll('input').forEach(i=>i.checked=(i.value===code));
  applyAll();
}
```

Chart onClick uses chart variable — define options.onClick referencing `chart` (closure, chart assigned after; use function referencing window-level let chart — fine since onClick fires later).

Now header dot element in meta: `<span id="checkdot"></span>`.

Tab 04 label: `04 CHECK & METHOD <span class="tdot" id="t04dot" hidden>●</span>`.

Draft tab: `03 DRAFT <span id="dtab">(0)</span>`.

Now assemble final HTML. Also add `<noscript>` note? optional, skip.

Let me also make sure the "02 PARAGRAPHS" tab default selected is overview (01). selectTab('overview') at init.

Also initial focus: qInput.focus() — but that triggers focus handler showing syntax. Good.

Potential issue: `position:sticky` rail with max-height 100vh overflow auto — ok.

Let me also compute minY/maxY:

```js
const years=R.map(r=>r.year); const minY=Math.min(...years), maxY=Math.max(...years);
```

7304 spread into Math.min — spread of 7304 args is fine (limit ~65k). OK.

titleSet/committeeSet:

```js
const titleSet=new Set(R.map(r=>r.title));
const commSet=new Set(R.map(r=>r.committee));
```

allCodes from committeesOf union:

```js
const allCodes=[...new Set(R.flatMap(r=>r._committees))].sort();
```

But _committees computed in precompute loop — order: precompute first, then allCodes.

symTitles built in same loop before _shared assignment — need two passes: first pass build symTitles, second pass per-record fields. I'll do:

```js
const symTitles={};
R.forEach(r=>{(symTitles[r.symbol]=symTitles[r.symbol]||new Set()).add(r.title);});
R.forEach(r=>{ ...precompute... });
```

_dupPin after:

```js
const pinMap={};
R.forEach(r=>{const k=r.title+'|'+r.paragraph;(pinMap[k]=pinMap[k]||[]).push(r);});
R.forEach(r=>{r._dupPin=(pinMap[r.title+'|'+r.paragraph].length)>1;});
```

Now writing final answer. Intro: at most three short sentences before code block. Then the html block. Nothing after.

Let me write the complete file now, being careful about syntax errors. I'll write it in full.

Also: the results container delegation — note buttons inside rowtop? rowtop has no buttons. Links in meta (symbol) — clicking link inside rowtop would also toggle; stopPropagation on link clicks: add handler: resultsEl.addEventListener('click', e=>{ if(e.target.closest('a'))return; ... }).

Also mark clicks — fine.

One more: "Show 25 more" — after renderResults, keep scroll (innerHTML replace keeps scroll position roughly). OK.

Also add `lang="en"`.

Let me write out the code.

Also careful: in rowHTML template literals inside the main script — fine.

For the chart aria fallback content inside canvas: `<canvas ...>Fallback text: the table beside this chart lists the same numbers.</canvas>`.

Chart.js requires canvas parent with height — I set #fig1wrap height via style.

Let me now also handle `state.order` select id orderSel with three options.

Writing now. I'll aim for clean, complete code.

One more check — the spec for tab 02 summary: "279 of 7,304 paragraphs match · 8 committees · 1990–2023". My format matches.

Also "the order: 'sorted by year, newest first, then by document and paragraph'; a select beside it offers document order and most matches first" — my orderText for 'year' is exactly that phrase. Good.

Also rail big number: "279 matching paragraphs" with "of 7,304" — I'll render big number + sub "matching paragraphs · of 7,304".

Also the search label: "SEARCH THE PARAGRAPHS" monospace.

Also hint under search box always visible (the normalization hint). And echo line. And error line.

Now, writing the final file. I'll count roughly — it'll be ~700-800 lines. Good.

Also remember: no code after the block; before block ≤3 sentences.

Let me write the JS init sequence at end of body:

```js
buildRail(); buildDocSel(); renderQuirks(); selectTab('overview'); applyAll(false); qInput.focus();
```

applyAll(reset) — at init reset=false fine (state.shown=25 default).

Wait applyAll signature: function applyAll(reset=true). Init call applyAll(true) fine.

Also `state.searched=false` initially.

In renderRail, brackets only when state.searched.

Also echo line: set in runSearch/applyAll: echoEl.textContent = state.error? '' : echoLine(); qerror.textContent = state.error||''.

Put that in computeAndRender.

Edge: parse error → hits=[] → summary '0 paragraphs pass.'? Spec: "An unbalanced quote or parenthesis shows a message and no results." So results empty + error message. Summary: I'll set summary to '' when error, and qerror shows message. Checks: query check fails with parse error. Good.

Now finalize CSV/TXT filenames: 'general-comments-quotations.txt' / '.csv'.

Also `download` uses a.click() — fine offline.

localStorage key 'gc-verbatim-draft'.

Also on load, loadDraft before first render of draft tab count.

Write it.

For the value labels plugin, ensure it doesn't crash when chart has 0 data — fine.

Also chart tooltip: keep default but format: callbacks label: c=>` ${c.parsed.x.toLocaleString('en-US')} paragraphs`.

Let me write everything now carefully.

Also one subtlety: `highlightHTML` when state.hlTerms empty → return escHtml(text). Good.

In check 4, when tree exists and root not NOT: use state.hlReTest (non-global). Build in computeAndRender:

```js
const pats=state.hlTerms.map(termPatternShown);
state.hlRe=pats.length?new RegExp(pats.join('|'),'giu'):null;
state.hlReTest=pats.length?new RegExp(pats.join('|'),'iu'):null;
```

Check 4 uses hlReTest.test(h._shown) — non-global, no lastIndex issue.

_mc uses hlRe global — reset lastIndex each call. OK.

Now — writing the response.

Also the intro sentences: "Built the verbatim finder on WORKSHOP_DATA.gc: Boolean/phrase search over all paragraphs, four tabs (overview chart, paged results with highlight and copy, draft collection, self-checks), filters in the left rail. Everything is computed in the page; no model is called." That's 2 sentences. Good.

Let me write the code.

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Verbatim finder — General Comments, paragraph by paragraph</title>
<style>
...
</style>
</head>
<body>
<header>
  <div class="kicker">UN Treaty Bodies · General Comments</div>
  <h1>Verbatim finder: General Comments and General Recommendations</h1>
  <div class="meta"><span id="metaLine"></span><span id="checkdot"></span></div>
  <div id="live" aria-live="polite"></div>
</header>
<div class="layout">
  <aside id="rail" aria-label="Filters">
    <div class="railhead"><span class="lbl">FILTERS</span><button class="link" id="clearAll">Clear all</button></div>
    <div id="hitWrap" aria-live="polite"><div class="big" id="hitCount">–</div><div class="bigsub">matching paragraphs · of <span id="totalCount"></span></div></div>
    <div id="chips"></div>
    <div class="search">
      <label class="lbl" for="q">SEARCH THE PARAGRAPHS</label>
      <div class="qwrap"><input id="q" type="text" autocomplete="off" spellcheck="false" placeholder='“best interests” AND child'><button class="btn" id="go">Search</button></div>
      <div class="syntax" id="syntax" hidden>
        <p><b>Syntax.</b> A space or AND joins words; OR; NOT or a leading minus; “an exact phrase” in double quotes; parentheses; a star at the end of a word for any ending (child* finds children). Operators in capitals — lower-case “or” is a word.</p>
        <button class="ex" data-q='"best interests" AND child'>“best interests” AND child</button>
        <button class="ex" data-q='(torture OR ill-treatment) NOT detention'>(torture OR ill-treatment) NOT detention</button>
        <button class="ex" data-q='"reasonable accommodation"'>“reasonable accommodation”</button>
      </div>
      <p class="hint">Whole words, any case. Curly and straight quotes, apostrophes, dashes and hyphens count as the same, and footnote marks are skipped, so State's finds State’s and a phrase can cross a footnote.</p>
      <div class="echo" id="echo"></div>
      <div class="err" id="qerror"></div>
    </div>
    <button class="fhead" id="fhead" aria-expanded="false" aria-controls="fbody"><span class="n">01</span> Committee, years, document</button>
    <div id="fbody" hidden>
      <div class="allnone"><button class="link" id="allC">all</button><button class="link" id="noneC">none</button></div>
      <div class="clist" id="clist"></div>
      <div class="years"><label>from <input id="yFrom" type="number" step="1"></label><label>to <input id="yTo" type="number" step="1"></label></div>
      <label class="doclbl" for="docSel">DOCUMENT</label>
      <select id="docSel"><option value="">all documents</option></select>
    </div>
  </aside>
  <main>
    <div class="tabs" role="tablist" aria-label="Views" id="tablist">
      <button class="tab" role="tab" data-tab="overview" aria-selected="true" id="t-overview">01 Overview</button>
      <button class="tab" role="tab" data-tab="paragraphs" aria-selected="false" id="t-paragraphs">02 Paragraphs</button>
      <button class="tab" role="tab" data-tab="draft" aria-selected="false" id="t-draft">03 Draft <span id="dtab">(0)</span></button>
      <button class="tab" role="tab" data-tab="check" aria-selected="false" id="t-check">04 Check &amp; method <span class="tdot" id="t04dot" hidden>●</span></button>
    </div>
    <section id="p-overview" role="tabpanel" aria-labelledby="t-overview">
      <div class="fighead"><span class="figno">FIG.01</span><h2 class="figtitle">Paragraphs per committee</h2></div>
      <p class="hint">click a bar = tick that committee alone · How this is computed: one count per committee over the paragraphs that match the query and filters.</p>
      <div class="figrow">
        <div class="chartwrap"><div id="fig1wrap"><canvas id="fig1" role="img" aria-label="Paragraphs per committee">Fallback: the table beside this chart lists the same numbers.</canvas></div></div>
        <table class="figtable" id="fig1table"></table>
      </div>
      <p class="hint" id="jointNote" hidden>Joint General Comments count under both committees, so the bars can add up to more than the hits.</p>
    </section>
    <section id="p-paragraphs" role="tabpanel" aria-labelledby="t-paragraphs" hidden>
      <div class="sumrow">
        <p id="summary" aria-live="polite"></p>
        <label class="orderlbl" for="orderSel">order <select id="orderSel">
          <option value="year">year, newest first</option>
          <option value="doc">document order</option>
          <option value="match">most matches first</option>
        </select></label>
      </div>
      <p class="hint">This page retrieves; it never writes. Every paragraph shown is a record of the file, as stored.</p>
      <div id="results"></div>
      <button class="btn" id="more">Show 25 more</button>
    </section>
    <section id="p-draft" role="tabpanel" aria-labelledby="t-draft" hidden>
      <h2>Your draft (<span id="dcount">0</span> quotations)</h2>
      <div id="draftList"></div>
      <div class="btnrow">
        <button class="btn" id="copyAll">Copy all</button>
        <button class="btn" id="dlTxt">Download .txt</button>
        <button class="btn" id="dlCsv">Download .csv</button>
      </div>
      <p class="hint" id="storeHint">Kept in localStorage when your browser allows it; otherwise in this page's memory only.</p>
    </section>
    <section id="p-check" role="tabpanel" aria-labelledby="t-check" hidden>
      <h2>How the app checks itself</h2>
      <p class="hint">Each line compares two computations done by this page. A failed check marks rows; it never drops them.</p>
      <div id="checks"></div>
      <h2>Known quirks of this file</h2>
      <p class="hint">Computed at load, before any search.</p>
      <ul id="quirks"></ul>
      <h2>How this is computed</h2>
      <div class="method">…</div>
      <h2>Sources consulted</h2>
      <ul class="srcs">…</ul>
    </section>
  </main>
</div>
<footer>
  <div id="footLine"></div>
  <div>Counting, matching and sorting are done by this page's code; no model is called. Credits: charting by Chart.js 4 (MIT licence).</div>
</footer>
<div id="clipfallback" hidden><p class="hint">Clipboard refused — select and copy from this box:</p><textarea id="cliptext" rows="5"></textarea></div>
<script>
...
</script>
</body>
</html>
```

Now the script. Writing it fully and carefully:

```js
(function(){
"use strict";
const D=window.WORKSHOP_DATA.gc;
const R=D.records;
const FN=/\[\[fn:\d+\]\]/g;
const COMMITTEE_NAMES={...};
const $=id=>document.getElementById(id);
const escHtml=s=>String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
const escRe=s=>s.replace(/[.*+?^${}()|[\]\\]/g,'\\$&');
function normalize(s){...}
class QError extends Error{}
... etc
```

I'll now produce the final long code. Let me be extra careful with template literals and quotes inside the HTML strings (e.g. data-q attributes with double quotes inside — I used curly quotes in examples so attribute quoting with double quotes is safe: data-q='"best interests" AND child' uses straight double quotes inside a double-quoted attribute — that breaks! Use single-quoted attribute: data-q='"best interests" AND child' — attribute delimited by single quotes containing double quotes — valid HTML. I wrote data-q='"best interests" AND child' above — yes single-quoted. And the button text uses curly quotes. Good. Third example data-q='"reasonable accommodation"' single-quoted. Good.

In JS, examples read via b.dataset.q — fine.

Now, writing everything. Also note the `.ex` buttons inside #syntax — the syntax div is inside .search after qwrap.

Also the fhead toggle:

```js
fhead.addEventListener('click',()=>{const open=fbody.hidden; fbody.hidden=!open; fhead.setAttribute('aria-expanded',String(open));});
```

Initially closed (hidden). Spec: "one open at a time" — only one heading, fine.

Let me also handle window resize for chart — Chart.js responsive handles.

Alright, compose the final answer. I'll write the code block now, mentally compiling as I go.

Careful with one thing: in `rowHTML`, nested template literals with `${...}` — fine.

In `renderChecks`, `runChecks` uses `chart` — defined. Also uses `state.comCounts`.

Also `updateHeaderDot` merged into renderChecks.

Also `applyAll` calls `computeAndRender` which calls renderChecks → updates dot. Good.

Also initial `selectTab('overview')` before applyAll so panels correct.

Also `more` button handler: `state.shown+=25; renderResults();`.

Also orderSel change: `state.order=orderSel.value; applyAll(false);` — keep shown? applyAll(false) doesn't reset shown. But hits recomputed & sorted; renderResults uses shown. OK use applyAll(false).

Filter changes: applyAll(true) (reset paging).

runSearch: state.searched=true; parse; applyAll(true).

Let me also ensure `renderResults` handles state.error: resultsEl.innerHTML=''; moreBtn.hidden=true; summary=''.

Also when error, echo empty, qerror message.

Write final code now. Also include `totalCount` set to R.length formatted.

For the meta line: 

```js
metaLine.textContent=`${R.length.toLocaleString('en-US')} paragraphs from ${titleSet.size} General Comments (distinct title) of ${commSet.size} committees, ${minY}–${maxY} · source: `;
```

and source link appended: I'll build with innerHTML:

```js
const srcTxt=D.source||'source';
metaLine.innerHTML=`${R.length.toLocaleString('en-US')} paragraphs from ${titleSet.size} General Comments (distinct title) of ${commSet.size} committees, ${minY}–${maxY} · ${D.source_url?`<a href="${escHtml(D.source_url)}" target="_blank" rel="noopener">${escHtml(srcTxt)}</a>`:escHtml(srcTxt)}`;
```

Footer:

```js
footLine.textContent=`${D.source||''}${D.built?' · built '+D.built:''}`;
```

OK. Also storeHint update: `storeHint.textContent='Kept in '+ (state.store==='localStorage'?'localStorage (this browser)':'this page's memory only') +' — nothing leaves the browser.';` careful apostrophe in string — use double quotes or escape.

Now produce. Also double-check the parser handles "(torture OR ill-treatment) NOT detention": tokens: ( WORD(torture) OR WORD(ill-treatment) ) NOT WORD(detention). parseOr→parseAnd→parseNot→parsePrimary '(' → parseOr inside → torture OR ill-treatment → ')' consumed → back in parseAnd: peek NOT → implicit AND → parseNot → NOT detention. Tree: AND(OR(...), NOT(detention)). Good.

Echo: "the word torture or the word ill-treatment and without the word detention" — hmm echo of AND(OR(a,b),NOT(c)) = `${echo(OR)} and ${echo(NOT)}` = "the word torture or the word ill-treatment and without the word detention" — ambiguous English but acceptable. Could add parentheses in echo for OR inside AND: if child is OR and parent AND → wrap in "( )". I'll add: in AND case, if t.b.t==='OR' wrap echo(t.b) in parentheses; similarly for a. Minor polish:

```js
if(t.t==='AND'){const a=echo(t.a),b=echo(t.b);return `${t.a.t==='OR'?'('+a+')':a} and ${t.b.t==='OR'?'('+b+')':b}`;}
```

Good.

Now finalize. Also `termCount` for check 1.

Also note: `state.hlTerms` used by rowHTML via highlightHTML(raw, state.hlTerms) — highlightHTML builds regex each call from terms; for 25 rows fine, but building regex per row is wasteful; pass prebuilt? highlightHTML(text, terms) builds `new RegExp(terms.map(termPatternShown).join('|'),'giu')` each call — 25× per render, fine.

But ctxHTML also uses it. OK.

Edge: terms empty → escHtml only.

Let me also make sure `highlightHTML` handles the 'giu' regex with lookbehind — supported in modern browsers with 'u' flag. Fine.

Now write out. Also add small CSS for .method p, .srcs.

Also `.link` button style:

```css
button.link{background:none;border:none;padding:0;color:var(--red);font:11px ui-monospace,Menlo,Consolas,monospace;cursor:pointer;text-decoration:underline}
```

.marksline button and .ctx button also use class? I'll give them class="link" too in generated HTML.

In rowHTML actions: `<button class="link" data-act="stored">` etc.

OK writing final.

One more consideration: performance of applyAll at load with 7304 records: evalTree skipped (tree null), passFilters cheap, _mc: hlRe null → 0. Sort 7304 — fine. renderResults 25 rows. Checks: recount loop 7304 with passFilters — fine; marks check 7304 string ops — fine; highlight check skipped (tree null). Good.

After a search, evalTree per record with regex — 7304 × few regex tests — fine.

Let me write it all now. Final output structure: 2-3 intro sentences, then ```html block. Nothing after.