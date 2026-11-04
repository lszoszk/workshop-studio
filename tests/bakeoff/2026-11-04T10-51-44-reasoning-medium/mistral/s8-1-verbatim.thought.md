Let me plan this app carefully. The user wants a complete HTML app for searching General Comments paragraphs. I need to build one complete HTML file, under ~1500 lines, using WORKSHOP_DATA.gc.

Key features:
- Header: monospace label, serif title, one line with source, n, years; checks pass/fail indicator.
- Left rail with filters (always visible except Draft tab): big count, search box with syntax help dropdown, examples, query echo, committee checkboxes with hits, years from/to, document select, chips.
- Tabs: 01 Overview (chart FIG.01), 02 Paragraphs (results, paging, highlight, expand, copy citation/quotation, add to draft, context), 03 Draft (list, copy all, download txt/csv), 04 Check & method.
- Checks panel computed at load and after search.
- Footer with source, built, credits (Chart.js MIT).

Let me write the code carefully.

Data: WORKSHOP_DATA.gc = {title, source, source_url?, built, count, records}. Wait — the description says gc has {title, source, count, records}. Does it have source_url and built? The uhri has source_url and built. For gc, described fields: `{title, source, count, records: [...]}`. Hmm, header says "one line with the data's source, n and years" and "`source` linked to `source_url`". The gc description doesn't list source_url or built explicitly, but the plan says link source to source_url and footer shows source and built. I'll read them defensively: `D.source_url || ''`, `D.built || ''`. If missing, just show source text without link. Actually plan says "`source` linked to `source_url`" — I'll do `D.source_url ? <a> : text`.

Records fields: id, symbol, paragraph (int), committee, year, title, short_title, doc_url, text, cited_articles.

Precompute per record at load:
- norm: normalized text
- marks: count of [[fn:N]]
- shown: text with fn marks removed
- leading: match ^(\d{1,3})\.\s on text
- pinpoint: "para. N" / "preamble" / "subpara. (x)"
- lettered: text starts with ^\(([a-z]{1,4})\)
- citation
- shared: symbol maps to >1 distinct title
- joint: symbol contains two committee codes? Plan: "joint" — symbol with two symbols (en dash or comma). Detect via regex of committee codes in symbol finding ≥2 distinct codes. Actually "A record's committees" = codes found in symbol plus committee field. Joint = more than one code in symbol? The plan says joint General Comment (two symbols in one symbol). I'll compute codesInSymbol; joint = codesInSymbol.length > 1. Hmm but "CAT-OP" — regex `\b(CAT|CCPR|CED|CEDAW|CERD|CESCR|CMW|CRC|CRPD)\b` with "CAT-OP" for CAT/OP. Note CEDAW contains... "CEDAW" — \bCED\b would match inside "CEDAW"? \b between D and A? No — \b is between word and non-word char; D and A are both word chars, so no boundary. Good. But "CED" appears in "CEDAW"? CEDAW = C-E-D-A-W; \bCED\b requires boundary after D, but A follows, word char, so no match. Good. CAT in "CAT-OP": \bCAT\b — after T is "-", non-word, so boundary exists → matches CAT. Plan says "CAT-OP" for CAT/OP, so committee code for CAT/OP symbol... The committee field is "CAT-OP" per the data notes ("CAT-OP is the Subcommittee on Prevention of Torture"). Hmm, actually the note says 10 committee codes, CAT-OP is one. So committee field may be "CAT-OP". The regex for codes in symbol: I'll use a regex that finds CAT-OP first: /\b(CAT-OP|CAT|CCPR|CED|CEDAW|CERD|CESCR|CMW|CRC|CRPD)\b/g. Order matters: CAT-OP before CAT.

Committee full names: need a map. 10 codes: CAT, CAT-OP, CCPR, CED, CEDAW, CERD, CESCR, CMW, CRC, CRPD. Full names:
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

But I shouldn't hard-code the list of committees — read from data (distinct committee values). Full names: I can provide a map but fall back to the code itself if unknown. That's fine — names are a lookup table, not data facts. Actually "never hard-code counts, countries, years or names" — names of committees... hmm. The instruction says read field values from data, never hard-code counts/countries/years/names. Committee full names aren't in the data though. Safer: display the code, and if I have a known expansion use it. I think providing expansions for standard treaty body codes is acceptable knowledge, but to be safe I could just show the code plus expansion from a map with fallback. I'll include the map with fallback to code. That's reasonable.

Query parser:
Tokens: quoted phrase (straight or curly double quotes “ ” " ), parens, AND/OR/NOT capitals, leading `-` as NOT, word = run of non-space chars with optional trailing `*`.

Grammar: expr := orExpr; orExpr := andExpr (OR andExpr)*; andExpr := notExpr (AND? notExpr)* — adjacent terms joined by AND (implicit); notExpr := NOT notExpr | `-` notExpr | primary; primary := `(` expr `)` | term.

Term: {type:'word', value, wildcard} or {type:'phrase', words:[...]}.

Echo: build English description. E.g. phrase “best interests” AND word child → "Paragraphs containing the phrase “best interests” and the word child". For OR: "…or…". NOT: "without the word X". NOT-only query: "Paragraphs that do not contain …" and matches everything lacking terms.

Normalization function:
```js
function norm(s){
  return s
    .replace(/\[\[fn:\d+\]\]/g, ' ')
    .replace(/[“”„]/g, '"')
    .replace(/[‘’‚]/g, "'")
    .replace(/[–—­]/g, '-')   // en dash, em dash, soft hyphen
    .replace(/\u00a0/g, ' ')
    .replace(/\s+/g, ' ')
    .toLowerCase();
}
```
Wait — plan says fn marks removed (replaced with... "removed"). For norm, removing vs replacing with space: "212 between two words of a sentence, so the string 'Education For All. By virtue' does not exist" — meaning if you remove the mark entirely, "Education For All[[fn:5]]. By virtue" → "Education For All. By virtue"? Hmm, actually the mark sits between words: "Education For All[[fn:5]] By virtue" → removing gives "Education For All By virtue" — the sentence exists. The example says the string "Education For All. By virtue" does not exist although the sentence does — because there's a period? Whatever. I'll replace fn marks with a space in norm (safer for word boundaries) — actually plan says "removed". If mark is between two words with no spaces: "word1[[fn:1]]word2" → removing gives "word1word2" merged. Replacing with space splits them. Hmm. For matching purposes, replacing with space is safer. But plan explicitly: "`norm`, once per record at load = `text` with `[[fn:N]]` removed". I'll follow: remove (replace with ''). But then "All[[fn]]. By" → "All. By" fine. "word1[[fn]]word2" → merged — edge case, acceptable. Actually for highlight, the gap regex handles `(?:\s|\[\[fn:\d+\]\])+`. For norm matching, if I remove marks, a phrase spanning a mark would need the words adjacent without space — phrase regex joins words with `\s+`, requiring at least one space. If mark removed leaves no space, phrase won't match. To be safe, replace with a space in norm. The plan's intent is that footnote marks are skipped. I'll replace with ' ' in norm — this makes "a phrase can cross a footnote" work. For shown text, remove entirely (as it reads in print — actually in print the footnote mark appears as a superscript number; "shown with the footnote marks removed, as it reads in print" — hmm, removing entirely could join words. But plan says shown = text with every [[fn:N]] removed. I'll follow plan: replace with '' for shown. Wait but then "All[[fn:5]]. By virtue" → "All. By virtue" fine. And "word1[[fn]]word2" → "word1word2". Rare. Follow the plan literally: shown = text.replace(/\[\[fn:\d+\]\]/g, ''). marks = count.

Hmm, but for norm, plan says removed too. But then phrase crossing footnote: "Education For All[[fn:5]] By virtue" — phrase "Education For All By virtue" → words joined by \s+ → "education\s+for\s+all\s+by\s+virtue" — in norm with mark removed: "education for all by virtue"? Only if there was a space after the mark. If text is "All[[fn:5]]By" → "allby". Edge case. I'll use replace with ' ' in norm to be robust; it still satisfies "footnote marks are skipped". Actually wait — replacing with space then collapsing whitespace gives same result as removing when surrounded by spaces. Only differs when mark is glued between word chars, where space is better. Go with space in norm.

Term regex over norm:
```js
function termRegex(t){
  let core = t.words.map(escapeRe).join('\\s+');
  if (t.wildcard) core = core.replace(/\*$/,'') ... 
}
```
Better: for word with trailing `*`: escape the word without the star, then append `\w*`? Plan: "trailing `*` → `\w*`". So `child*` → `child\w*`. Boundaries: `(?<![\p{L}\p{N}])` before and `(?![\p{L}\p{N}])` after, flag u. But with wildcard, the trailing boundary should not apply after `\w*` (since \w* can match zero, boundary after would fail when word is exactly "child" followed by non-word... actually `(?![\p{L}\p{N}])` after `child\w*` — if text is "children", `child\w*` matches "children", then boundary check: next char after "children" — fine. If text is "child", `child\w*` matches "child" (\w* matches empty), then `(?![\p{L}\p{N}])` — next char must not be letter/number. OK. But regex backtracking: `child\w*` on "childish" matches "childish" fully. On "child" followed by "s" — "childs"? matches "childs". Fine. But problem: on "childcare", `child\w*` matches "childcare", boundary ok — so child* finds childcare. That's intended ("any ending").

Hmm, but with wildcard, should the trailing lookahead be there? "child*" should match "child" itself too. `child\w*(?![\p{L}\p{N}])` on "child." → matches "child", next char "." not letter → ok. On "children" → \w* consumes "ren", next char boundary ok. Good. Keep both boundaries always.

For phrase: words joined by `\s+`, wrapped in same boundaries.

Word tokenization of query: after normalization of the query? Plan: "The query is normalised the same way". So normalize query string first (curly quotes → straight, dashes → hyphen, lowercase, collapse whitespace) — but careful: normalizing the query would turn curly quotes into straight, which is what we want for phrase detection. But it also lowercases — fine since matching is case-insensitive anyway (norm is lowercase, regex built from normalized query). But the echo should show the original query terms? Echo shows phrase “best interests” — I can keep original casing for display by tokenizing the original but normalizing each token. Simpler: tokenize original query (detect curly quotes as phrase delimiters), then normalize each token's content for matching, keep raw for echo.

Tokenizer on raw query:
- skip whitespace
- if char is `"` or `“` or `”`: read until matching close quote (straight `"` or curly `”`/`“`?) — phrase in double quotes straight or curly. Read until next `"` or `”`. If none → error "unbalanced quote".
- `(` `)` tokens
- otherwise read run of non-space, non-paren chars. Then check: if token === 'AND'/'OR'/'NOT' (capitals) → operator. If starts with '-' and length>1 → NOT + rest as word. Else word; trailing `*` → wildcard.

Wait: a word run could include quotes? "any other run of non-space characters" — I'll stop word at quote chars too, to be safe. Actually simpler: read run of chars not in whitespace, parens, or quote chars.

Parser with precedence NOT > AND > OR, implicit AND between adjacent primaries.

```js
function parse(q){
  const toks = tokenize(q);
  let pos = 0;
  function peek(){ return toks[pos]; }
  function parseOr(){
    let left = parseAnd();
    while (peek() && peek().type==='OR'){ pos++; const right = parseAnd(); left = {type:'or', args:[left,right]}; }
    return left;
  }
  function parseAnd(){
    let left = parseNot();
    while (peek() && (peek().type==='AND' || isTermStart(peek()))){
      if (peek().type==='AND') pos++;
      const right = parseNot();
      left = {type:'and', args:[left,right]};
    }
    return left;
  }
  function parseNot(){
    const t = peek();
    if (t && t.type==='NOT'){ pos++; return {type:'not', arg: parseNot()}; }
    if (t && t.type==='NOTWORD'){ pos++; return {type:'not', arg: t.term}; }
    return parsePrimary();
  }
  function parsePrimary(){
    const t = peek();
    if (!t) throw {msg:'unexpected end of query'};
    if (t.type==='LPAREN'){ pos++; const e = parseOr(); if(!peek()||peek().type!=='RPAREN') throw {msg:'unbalanced parenthesis'}; pos++; return e; }
    if (t.type==='TERM'){ pos++; return t.term; }
    throw {msg:'unexpected "'+t.raw+'"'}; // e.g. RPAREN or OR at start
  }
  const tree = parseOr();
  if (pos < toks.length) throw {msg:'unexpected "'+toks[pos].raw+'"'}; // e.g. stray RPAREN
  return tree;
}
```
isTermStart: type TERM, NOT, NOTWORD, LPAREN.

Empty query → tree = null → matches all.

Evaluate tree over norm:
```js
function evalTree(node, norm){
  switch(node.type){
    case 'word': return node.re.test(norm);
    case 'phrase': return node.re.test(norm);
    case 'and': return node.args.every(a=>evalTree(a,norm));
    case 'or': return node.args.some(a=>evalTree(a,norm));
    case 'not': return !evalTree(node.arg,norm);
  }
}
```
Build regexes at parse time: for each term, compile regex from normalized words.

Term regex builder:
```js
function buildTerm(words, wildcard){
  let core = words.map(w=>escapeRe(w)).join('\\s+');
  if (wildcard) core = core + '\\w*'; // hmm, wildcard applies to last word
  return new RegExp('(?<![\\p{L}\\p{N}])' + core + '(?![\\p{L}\\p{N}])', 'u');
}
```
Wait wildcard: word "child*" → words = ["child"], wildcard → core = "child\\w*". For phrase with trailing star? Plan says "a star at the end of a word" — phrases probably don't have wildcards; if a phrase token ends with `*`, treat... I'll only apply wildcard to single-word terms; if phrase ends with *, strip it and ignore or apply to last word. I'll apply to last word: words[last] += '\\w*'. Simpler: handle in tokenizer — word token with trailing * → wildcard flag.

Hmm, careful: `(?![\p{L}\p{N}])` after `child\w*` — on "child" at end of string, lookahead succeeds (no char). Good.

But there's a subtlety: with wildcard, `child\w*` then `(?![\p{L}\p{N}])` — regex will try to match maximal \w* then check boundary; if fails, backtrack \w* shorter — but then next char is a letter, boundary fails... eventually \w* = empty, next char after "child" is a letter → fail. So "child*" won't match "childhood"? Wait "childhood": `child\w*` greedy matches "childhood", then boundary: end or non-letter → ok. It matches. "child*" matching "childish" — yes intended. OK.

Escape: escapeRe = s => s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'). Note hyphen doesn't need escaping outside char class.

Normalization of query tokens: apply same normChar function per word (lowercase, curly→straight, dashes→hyphen). But norm also collapses whitespace — words are single tokens so fine. Also fn marks won't appear in query.

Echo builder:
```js
function echo(node){
  if(!node) return 'no search words';
  switch(node.type){
    case 'word': return node.wildcard ? 'the word '+node.display+'*' : 'the word '+node.display;
    case 'phrase': return 'the phrase “'+node.display+'”';
    case 'and': return node.args.map(echo).join(' and ');
    case 'or': return node.args.map(echo).join(' or ');
    case 'not': return 'without '+echo(node.arg);
  }
}
```
Plan example: "Paragraphs containing the phrase “best interests” and the word child". So prefix "Paragraphs containing " + echo. For NOT-only: "Paragraphs that do not contain …". Detect NOT-only: tree is not-node at top with no positive terms. I'll compute hasPositive = tree contains any word/phrase not under a not. If !hasPositive && tree: echo = "Paragraphs not containing " + echo of inner... Let me just: if top-level is 'not' and no positive terms anywhere → "Paragraphs that do not contain " + echoInner. Simpler: full echo = "Paragraphs containing " + echo(tree) but for not-only, echo(tree) = "without X" → "Paragraphs containing without X" is awkward. I'll special-case: if no positive terms, "Paragraphs that do not contain " + echo(positive parts). Let me write: collect positive terms list; if tree exists and positives empty → "Paragraphs that do not contain " + echo(tree.arg...) hmm tree could be and of nots. I'll do: if positives.length===0 → "Paragraphs without " + echoAll(tree) where echoAll for not gives the inner. Actually simplest: echoNot(tree) returns description of what's excluded. I'll implement: 

```js
function describe(node){
  // returns {pos: [...], neg: [...]}
}
```
Overkill. Keep simple: echo string as above; if no positive terms, prefix "Paragraphs that do not contain " and for the not nodes echo as just the inner term. I'll write echo with a flag. Fine, minor.

Highlight: build a regex over the shown text (raw, with fn marks still present? Plan: "The same terms become a second regular expression over the shown text, where a quote or apostrophe matches its straight and curly forms, a hyphen matches hyphen, en and em dash, and a gap between phrase words matches `(?:\s|\[\[fn:\d+\]\])+`"). So highlight regex operates on the raw text (with fn marks), and gaps can include fn marks. Then matches wrapped in <mark> after HTML-escaping. So process: escape HTML of shown text? But shown text has fn marks removed... wait — highlight over "the shown text" — shown text = text with fn removed. But gap regex includes `[[fn:...]]` — contradiction? If shown text has marks removed, gaps can't include them. Hmm. I think highlight should run on the raw text (with marks), then when rendering, remove marks from inside... Actually plan: "Every matched word or phrase is wrapped in <mark>... The text is shown with the footnote marks removed". And gap matches `(?:\s|\[\[fn:\d+\]\])+` — so highlight runs on raw text including marks, and then the marks are removed from the final HTML (marks inside or outside <mark>). Approach: run highlight regex on raw text, produce HTML with <mark> tags, then strip `[[fn:N]]` from the resulting HTML string (they'd only appear as plain text between marks or inside). Since fn marks contain `[` `]` `:` digits — HTML-escaping doesn't affect them. So: html = escapeHtml(raw); then apply highlight by replacing matches in the escaped string? The regex needs to match against escaped text — escaping changes `"` to `&quot;` etc., breaking quote matching. Better: run regex on raw text, collect match ranges, then build HTML by escaping segments and wrapping matched segments in <mark>. Then remove fn marks from all segments. 

Implementation:
```js
function highlight(raw, terms){
  // terms: array of {re} regexes over raw text
  const combined = new RegExp(terms.map(t=>'('+t.source+')').join('|'), 'gu');
  ...
}
```
Build per-term raw regex: for each word (normalized? no — raw matching should be case-insensitive and quote/dash flexible). Plan: "a quote or apostrophe matches its straight and curly forms, a hyphen matches hyphen, en and em dash". So build char-class replacements: when escaping a word for the raw regex, replace `"` → `["“”„]`, `'` → `[''‚']`, `-` → `[-–—]`. And case-insensitive flag `i` (plus `u`). Gap between phrase words: `(?:\s|\[\[fn:\d+\]\])+`. Boundaries: for raw text, use `(?<![\p{L}\p{N}])` and `(?![\p{L}\p{N}])` too (works on raw). 

So rawTermRegex(words, wildcard):
```js
function rawEscape(w){
  return w.split('').map(c=>{
    if (c==='"') return '["“”„]';
    if (c==="'") return "[''‚']";
    if (c==='-') return '[-–—]';
    return escapeRe(c);
  }).join('');
}
```
But words are normalized (lowercase, straight quotes) — since we match with flag `i`, case doesn't matter. Normalized words have straight quotes/hyphens, which we expand to classes. Good.

Combined regex with alternation; use `g` and `u` and `i` flags. Then iterate matches over raw text, build HTML.

Note: NOT terms never highlighted — only positive terms (word/phrase nodes not under a `not`). Collect positive terms from tree.

Also "a hit matched in norm but without a highlight is listed as 'matched, not highlighted'" — check: after rendering, if row has no <mark> and query has positive terms → note in checks.

Filters:
- committees: set of ticked codes (all ticked initially). Record passes if any of record.committees intersects ticked.
- years: from/to inputs, preset min/max. Pass if year >= from && year <= to.
- document: select of short_title grouped by committee (optgroup). Blank = all. Pass if record.short_title === selected (or blank).

Wait — document select by short_title; multiple records share short_title (same GC). Filter by short_title equality. But different committees could share short_title? Unlikely; group by committee in optgroups, value = short_title. Fine. Hmm, but two different documents could have same short_title? Use title as value instead? short_title is the display; use `title` as value to be unique. Display short_title. I'll use title as value, label short_title.

Chips: active filters shown as removable chips under big number: e.g. "Committee: CERD ×", "Years: 1990–2023 ×" (only when narrowed from min/max), "Document: … ×". Clear all resets.

Hits = records matching tree + filters.

Hits per committee: for each hit, for each committee in record.committees, count++. Chart bars = per committee over hits. Note about joint.

Order: default year desc, title asc, paragraph asc. Select options: "Year, newest first" (default), "Document order" (title asc, paragraph asc, year?), "Most matches first" — hmm "most matches first" for a single query doesn't quite make sense... The plan says "a select beside it offers document order and most matches first". "Most matches first" — maybe sort by number of matched terms descending? I'll implement: score = number of positive terms that match the record; sort by score desc, then year desc. That's a reasonable interpretation. Label: "most matches first".

Paging: 25 per page, "Show 25 more" button.

Row rendering:
- header line: committee badge(s) (all committees of record? plan: "committee badge and short_title" — show record.committee badge; for joint show both badges), short_title, symbol link (doc_url, target _blank), pinpoint in red, year.
- text: shown text (fn removed), highlighted, truncated to 700 chars at word boundary if longer, with "Show the full paragraph (N words)" toggle.
- grey line: "3 footnote marks removed · show as stored" — link toggles to raw text.
- amber notes: leading mismatch ("the text begins '45.' but the record is para. 41: check the document"), lettered subpara, shared pinpoint, joint.
- click row → expand: buttons Copy citation, Copy quotation, Add to draft; Context: previous | next links.

Pinpoint: paragraph 0 → "preamble"; lettered (text starts with ^\(([a-z]{1,4})\)) → "subpara. (b)"; else "para. N".

Wait — lettered sub-paragraphs: "22 records are lettered sub-paragraphs ('(a) To take note…') that the file numbers 1, 2, 3". So paragraph is 1,2,3 but text starts with "(a)". Pinpoint "subpara. (b)". Detect: /^\(([a-z]{1,4})\)/ on text.

Citation: if shared (symbol has >1 title): `committee + ", " + docName + " (" + symbol + "), " + pinpoint` where docName = title up to first colon or " on ". E.g. "CERD, General Recommendation No. 29 (A/57/18), para. 3". Else `symbol + ", " + pinpoint`.

Copy quotation: shown text in quotation marks + " " + citation. Which quotes — curly or straight? Use curly “ ” to match document style? Plan: "copies the shown text in quotation marks". I'll use “ ”. Leading number dropped when leading === paragraph: "When leading equals paragraph, the copied quotation drops the '12. ' at the start". So copyText = shown (or raw?) — "the shown text" — with fn marks removed. And drop leading "N. " if leading == paragraph. Hmm: "the copied quotation drops the '12. ' at the start (the citation carries the number); the shown text keeps it."

So quotation = shownText, minus leading number if matches, wrapped in “”, plus " " + citation.

Add to draft: store {id, citation, quotation, symbol, paragraph, pinpoint, committee, short_title, year, text_copied, text_as_stored, doc_url}. text_copied = the quotation text (without quotes? plan CSV has text_copied and text_as_stored — text_copied = shown text possibly with leading dropped, text_as_stored = raw text). Draft persists in localStorage if available else memory.

Draft tab: list items with quotation as copied (with quotes + citation), remove button. Copy all: items joined: quotation + "\n" + citation + "\n\n". Download .txt: same as copy all. Download .csv: header citation,symbol,paragraph,pinpoint,committee,short_title,year,text_copied,text_as_stored,doc_url; UTF-8 BOM; fields double-quoted (escape " as ""). Use Blob + URL.createObjectURL + a.click(). That's allowed (no network).

Tab name carries count: "03 DRAFT (4)" — update on add/remove.

Checks (tab 04), computed at load and re-run after each search:
1. Query understood: echo + term count; parse error shown here.
2. Totals: rows listed across pages == hits; checkbox bracketed counts sum == hits + jointHits.
3. Chart total: bars sum == hits + jointHits, both shown.
4. Highlight: every hit has ≥1 <mark> unless NOT-only; list "matched, not highlighted".
5. Normalisation: if query has straight quote/apostrophe/hyphen, say curly/dash forms matched too and how many hits contain only those forms. Hmm — "how many hits contain only those forms": hits where the match in raw text uses curly/dash forms. Simplify: count hits whose raw text contains curly quote/apostrophe/en-dash AND norm matched... I'll compute: hits where raw contains any of [“”‘’–—] and the term regex matched only via those forms — hard. Simplify: report number of hits whose raw text contains curly quotes/apostrophes/dashes (i.e., where normalisation mattered). I'll phrase: "n hits contain curly quotes, apostrophes or dashes that normalisation folded". Good enough, honest.
6. Numbering: hits with leading != paragraph (both numbers); hits sharing pinpoint with another record of same title; lettered subparas.
7. Marks: for every hit, marks removed == count of [[fn: in stored text, and reinserting gives stored text exactly. Reinserting: shown.replace... can't reinsert exactly (positions lost). Instead check: stored.replace(fnRegex,'') === shown. That verifies. And marks count === (stored.match(/\[\[fn:/g)||[]).length.
8. Draft: for each draft item, look up record by id, compare text_as_stored; difference marks item.

Known quirks at load: paragraph 0 count + example; shared symbols count + example; joint count + example; duplicated pinpoints (same title+paragraph appearing >1) count + example; leading mismatches count + example.

Header checks indicator: run checks at load (with empty query) — count pass/fail; green dot "n checks pass" or red "n checks failed" + red dot on tab 04.

Layout: header, then tabs row, then main area: left rail (filters) + content. On Draft tab, hide left rail ("always visible except on the Draft tab").

Tabs: role="tablist", buttons role="tab" aria-selected, arrow-key navigation (left/right). Panels role="tabpanel".

Clickable count constraints — fine.

Chart: Chart.js bar, indexAxis 'y', data = committees sorted desc by count, backgroundColor '#9b2335', categoryPercentage/barPercentage to make gaps narrower than bar (e.g. barPercentage 0.9? gap narrower than bar → barThickness relative... use categoryPercentage: 0.8, barPercentage: 0.9). Value labels at end of bar: use plugin afterDatasetsDraw to draw values, or use tooltip + table. Plan: "the value at the end of each bar" — implement custom plugin drawing fillText at bar end. Axis from zero: beginAtZero: true. Gridlines: at most ten light gridlines — maxTicksLimit: 10. Click on bar = tick that committee alone: chart onClick → get elements at event → set committee filter to only that committee, update checkboxes, re-render.

Canvas role="img" aria-label with numbers; fallback content inside canvas; table beside with same numbers.

Chart only on Overview tab; render when tab shown (and on data change). Chart.js preloaded.

Search behavior: search box focus on load; while empty and focused, show syntax dropdown with 3 examples as buttons (fill + run); closes when typing starts. Enter or Search button runs. After search, echo line under box: "Paragraphs containing the phrase “best interests” and the word child". Unbalanced quote/paren → message, no results (keep previous? "shows a message and no results" — set hits to [] and show error).

Also note line under box: "Whole words, any case. Curly and straight quotes... footnote marks are skipped, so State's finds State’s and a phrase can cross a footnote."

Committee checkboxes: after a search, show hits in brackets. "all / none" links. All ticked initially.

Years: two number inputs from/to preset to min/max of data.

Now sizes: 7,304 records — precompute at load is fine.

Rendering results: 25 per page with "Show 25 more". Each row an <article>. Row click toggles open (but clicks on buttons/links inside shouldn't toggle — stopPropagation).

Context: previous/next paragraph of same title: find records with same title, sort by paragraph, find index of current, show ±1 inline in grey with pinpoint. Implement as expanding a context div within the open row.

Let me now think about the "shared pinpoint" check: two records share this pinpoint — same title and same paragraph (and not lettered?). Compute map key title+'|'+paragraph → count>1.

Leading mismatch: leading (from ^(\d{1,3})\.\s) != null && parseInt(leading) !== paragraph. Note: 5 records where number differs. Also lettered subparas have leading null (text starts with "(a)") — separate note.

Amber notes on rows:
- leading mismatch: "the text begins ‘45.’ but the record is para. 41: check the document"
- lettered: "a lettered sub-paragraph, numbered 2 by the file"
- shared pinpoint: "two records share this pinpoint"
- joint: "joint General Comment"

Now the header line: "`records.length` paragraphs from n General Comments (distinct title) of k committees, year min–max", source linked. E.g. "7,304 paragraphs from 188 General Comments of 10 committees, 1972–2026 · source: ...".

Checks indicator at right of header.

Footer: source and built; "Counting, matching and sorting are done by this page's code; no model is called." Credits: "Chart.js 4 (MIT)".

Let me now also handle: "An empty query with filters lists every paragraph that passes them, paged, and the summary says 'no search words'."

Summary line tab 02: "279 of 7,304 paragraphs match · 8 committees · 1990–2023" (committees among hits, years min–max among hits) + "no search words" if no query. Then order line: "sorted by year, newest first, then by document and paragraph" + select.

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
<nav role="tablist" id="tabs">4 buttons</nav>
<main>
  <aside id="rail">filters</aside>
  <section id="panels">
    <div id="tab-overview" role="tabpanel">fig01 + table</div>
    <div id="tab-paragraphs" role="tabpanel">summary + order + results</div>
    <div id="tab-draft" role="tabpanel">draft</div>
    <div id="tab-checks" role="tabpanel">checks</div>
  </section>
</main>
<footer>...</footer>
<script>...</script>
</body>
</html>
```

CSS: paper #f4f0e8, ink #1d1b18, rules #d9d2c3, accent #9b2335. Fonts: Georgia serif for title/numbers; ui-monospace for labels; system sans 16px body.

Layout: main { display:flex } rail width ~300px, content flex 1. On draft tab, rail hidden. Responsive: maybe media query stack — keep simple, min-width handling: "Works on a laptop screen without horizontal scrolling" — flex with rail 280px fixed, content min-width 0.

Tabs: numbered "01 OVERVIEW · 02 PARAGRAPHS · 03 DRAFT (n) · 04 CHECK & METHOD". Monospace uppercase, letter-spacing. Active: red + underline.

Let me write the JS carefully.

```js
const D = window.WORKSHOP_DATA.gc;
const R = D.records;
const $ = s => document.querySelector(s);
const esc = s => String(s).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
```

Normalization:
```js
const FN = /\[\[fn:\d+\]\]/g;
function normText(s){
  return s.replace(FN,' ')
    .replace(/[“”„]/g,'"').replace(/[‘’‚]/g,"'")
    .replace(/[–—­]/g,'-')
    .replace(/\u00a0/g,' ')
    .replace(/\s+/g,' ')
    .toLowerCase().trim();
}
```
Wait — soft hyphen \u00ad. Include in dash class: /[–—­]/ — careful writing the literal soft hyphen in code; use \u00ad escape: /[\u2013\u2014\u00ad]/g.

Precompute per record:
```js
const byId = {};
R.forEach(r=>{
  const shown = r.text.replace(FN,'');
  const marks = (r.text.match(/\[\[fn:/g)||[]).length;
  const norm = normText(r.text);
  const leadM = r.text.match(/^(\d{1,3})\.\s/);
  const letterM = r.text.match(/^\(([a-z]{1,4})\)/);
  const codes = [...new Set([...(r.symbol.match(/CAT-OP|CAT|CCPR|CED|CEDAW|CERD|CESCR|CMW|CRC|CRPD/g)||[]), r.committee])];
  ...
});
```
Hmm the symbol regex: need word boundaries. Use /(CAT-OP|CAT|CCPR|CED|CEDAW|CERD|CESCR|CMW|CRC|CRPD)\b/g — but "CED" in "CEDAW": with \b after CED — "CEDAW" has A after D, no boundary, so CED won't match inside CEDAW. But alternation order: regex tries CAT-OP first at each position. In "CEDAW/C/GC/27": at position 0, tries CAT-OP no, CAT no, CCPR no, CED — matches "CED" then \b required — next char 'A' is word char → \b fails → backtrack, try CEDAW → matches, \b after W (next '/') ok. Good. But wait, does the regex engine try CED before CEDAW? Alternation order in my list: I listed CED before CEDAW. At pos 0 of "CEDAW": CED matches chars 0-2, then \b between 'D' and 'A'? Both word chars → no boundary → fail. Then CEDAW tried → success. Good. Also "CAT-OP" vs "CAT": in symbol "CAT/OP/..." — hmm, would symbol be "CAT/OP/..."? The committee code is "CAT-OP". Symbol might be like "CAT/C/..." for CAT. For SPT, symbol maybe "CAT/OP/..."? Then regex CAT-OP wouldn't match "CAT/OP" (slash not hyphen). Plan says: codes found in symbol (`\b(CAT|...)\b`, "CAT-OP" for `CAT/OP`). So map "CAT/OP" → "CAT-OP". I'll do: match /(CAT\/OP|CAT|CCPR|...)\b/g then replace 'CAT/OP' with 'CAT-OP'. Let me write:

```js
const CODE_RE = /(CAT\/OP|CAT|CCPR|CEDAW|CED|CERD|CESCR|CMW|CRC|CRPD)\b/g;
function codesOf(r){
  const found = (r.symbol.match(CODE_RE)||[]).map(c=>c==='CAT/OP'?'CAT-OP':c);
  return [...new Set([...found, r.committee])];
}
```
Order alternation: put longer first (CAT/OP, CEDAW before CED). With \b, CED inside CEDAW fails anyway, but safer to order longest first.

Joint: found codes in symbol length > 1 (two symbols in one symbol field). Actually joint = symbol contains 2 committee codes. E.g. "CMW/C/GC/7–CERD/C/GC/38" → CMW, CERD → joint. Compute joint = (r.symbol.match(CODE_RE)||[]).length > 1.

Shared: symbolToTitles map: symbol → set of titles. shared = titles.size > 1.

Pinpoint:
```js
function pinpoint(r){
  if (r.paragraph === 0) return 'preamble';
  const m = r.text.match(/^\(([a-z]{1,4})\)/);
  if (m) return 'subpara. ('+m[1]+')';
  return 'para. ' + r.paragraph;
}
```

Citation:
```js
function docName(title){ 
  let t = title.split(':')[0];
  const on = t.split(/\s+on\s+/)[0]; // "up to the first colon or ' on '"
  return on.trim();
}
function citation(r){
  const pin = pinpoint(r);
  if (sharedSymbols.has(r.symbol)) {
    return r.committee + ', ' + docName(r.title) + ' (' + r.symbol + '), ' + pin;
  }
  return r.symbol + ', ' + pin;
}
```

Quotation text:
```js
function quoteText(r){
  let t = r._shown;
  const m = r.text.match(/^(\d{1,3})\.\s/);
  if (m && parseInt(m[1],10) === r.paragraph) t = t.replace(/^\d{1,3}\.\s/,'');
  return '“' + t + '” ' + citation(r);
}
```
Hmm — "copies the shown text in quotation marks, a space, the citation". Shown text = fn removed. Leading dropped if matches. OK.

Wait, should the quotation use shown (fn removed) or stored? "Copy quotation copies the shown text in quotation marks" — shown. OK.

Query parsing. Tokenizer:

```js
function tokenize(q){
  const toks=[]; let i=0;
  while(i<q.length){
    const c=q[i];
    if(/\s/.test(c)){i++;continue;}
    if(c==='('){toks.push({type:'LP',raw:c});i++;continue;}
    if(c===')'){toks.push({type:'RP',raw:c});i++;continue;}
    if(c==='"'||c==='“'||c==='”'){
      const close = (c==='"')?'"':'”';
      let j=q.indexOf(close, i+1);
      // also allow straight close for curly open? keep simple: curly open closes with ” or "
      if(j<0){ // try the other
        j = q.indexOf(c==='"'?'”':'"', i+1);
        if(j<0) throw {msg:'unbalanced quote: no closing quote after “'+q.slice(i+1,i+30)+'…'};
      }
      const inner = q.slice(i+1,j);
      toks.push({type:'PHRASE', raw:q.slice(i,j+1), inner});
      i=j+1; continue;
    }
    // word: run of non-space, non-paren, non-quote
    let j=i;
    while(j<q.length && !/[\s()"“”]/.test(q[j])) j++;
    let w = q.slice(i,j);
    if(w==='AND'||w==='OR'||w==='NOT'){toks.push({type:w,raw:w});i=j;continue;}
    if(w.startsWith('-') && w.length>1){ 
      let rest=w.slice(1);
      toks.push({type:'NOTW', raw:w, word:rest});
      i=j; continue;
    }
    toks.push({type:'WORD', raw:w, word:w});
    i=j;
  }
  return toks;
}
```
Hmm — a word could contain a quote mid-word like `don't` — apostrophe is fine (not a double quote). Double quote inside a word run: I stop at double quotes, so `say"hello` becomes word `say` then phrase... edge case, fine.

Wait: `-` alone (just a minus)? w.length>1 required, else it's a word "-". Fine.

Also NOTW with trailing star: rest may end with '*'.

Parser as sketched. Build term nodes:

```js
function makeTerm(word, display){
  // normalize word
  const w = normWord(word); // lowercase, curly→straight, dashes→hyphen
  const wildcard = w.endsWith('*');
  const core = wildcard ? w.slice(0,-1) : w;
  const words = core.split('-').length... 
```
Hmm — phrase words: a phrase token's inner split on whitespace → words. Each word normalized. For a single word term, words=[w]. Wildcard: trailing `*` on the word (or last word of phrase).

normWord: 
```js
function normWord(s){
  return s.replace(/[“”„]/g,'"').replace(/[‘’‚]/g,"'").replace(/[\u2013\u2014\u00ad]/g,'-').toLowerCase();
}
```
(No whitespace collapse needed per word; but phrase inner may have multiple spaces — split(/\s+/).)

Term node:
```js
{
  kind:'term', words:[...], wildcard:bool, display: original,
  re: new RegExp('(?<![\\p{L}\\p{N}])'+words.map(escRe).join('\\s+')+(wildcard?'\\w*':'')+'(?![\\p{L}\\p{N}])','u'),
  rawRe: raw regex for highlight
}
```
Wait wildcard placement: `child*` → core 'child' + '\\w*'. For phrase ending with `*`? e.g. `"best interests"*` — weird; I'll strip trailing * from phrase inner and treat as wildcard on last word: words[last] handled by appending '\\w*' after join. So: core = words.map(escRe).join('\\s+') + (wildcard?'\\w*':''). Good.

escRe = s=>s.replace(/[.*+?^${}()|[\]\\]/g,'\\$&');

Raw (highlight) regex per term:
```js
function rawTermRe(words, wildcard){
  const parts = words.map(w=>w.split('').map(rawChar).join(''));
  let core = parts.join('(?:\\s|\\[\\[fn:\\d+\\]\\])+');
  if(wildcard) core += '\\w*';
  return new RegExp('(?<![\\p{L}\\p{N}])'+core+'(?![\\p{L}\\p{N}])','giu');
}
function rawChar(c){
  if(c==='"') return '["“”„]';
  if(c==="'") return "['‘’‚']";
  if(c==='-') return '[-\\u2013\\u2014\\u00ad]';
  return escRe(c);
}
```
Note: words here are normalized (lowercase, straight quotes/hyphens) — with flag i, case ok.

Hmm — one issue: raw regex boundaries `(?<![\p{L}\p{N}])` — for wildcard `child\w*` the trailing `(?![\p{L}\p{N}])` as discussed. OK.

Combined highlight: collect all positive term rawRes, combine: new RegExp(terms.map(t=>'('+t.source+')').join('|'), 'giu'). Then walk matches on raw text, build HTML:

```js
function renderText(r, terms){
  const raw = r.text;
  if(!terms.length) return esc(raw).replace(FN,''); // no highlight
  const re = new RegExp(terms.map(t=>'('+t.source+')').join('|'),'giu');
  let out='', last=0, m;
  while((m=re.exec(raw))){
    out += esc(raw.slice(last,m.index)).replace(FN,'');
    out += '<mark>'+esc(m[0]).replace(FN,'')+'</mark>';
    last = m.index + m[0].length;
    if(m[0].length===0) re.lastIndex++;
  }
  out += esc(raw.slice(last)).replace(FN,'');
  return out;
}
```
Wait — FN is a global regex with lastIndex state; using .replace with /g is fine (replace resets). But using FN in multiple places with .test would be buggy; I only use replace/match — match with /g doesn't carry lastIndex issues? String.match with /g returns all matches, doesn't use lastIndex persistently (it resets). Actually String.prototype.match with global regex ignores lastIndex and resets it. replace also resets. Safe. But to be extra safe, define FN as a function or non-global for test. I'll use separate constants: FN_G = /\[\[fn:\d+\]\]/g for replace/match, and count via match.

Hmm, one subtlety: highlight match could span a fn mark (phrase gap includes fn marks) — then m[0] contains `[[fn:5]]` and we strip it inside <mark>. Good — "a phrase can cross a footnote" and highlight shows the phrase with the mark removed. 

Truncation: if shown length > 700 → show first 700 cut at word: 
```js
function truncate(s){ if(s.length<=700) return s; let cut=s.slice(0,700); cut=cut.replace(/\s+\S*$/,'') ... }
```
Better: cut at last space within first 700: `const idx = s.slice(0,701).lastIndexOf(' ')` hmm. Do: `let t=s.slice(0,700); const sp=t.lastIndexOf(' '); if(sp>400) t=t.slice(0,sp);` then append ' …'. But highlight complicates truncation — truncating HTML is messy. Approach: decide truncation on the shown text length; if long, render highlighted HTML of full text but wrap the tail in a hidden span? Simpler: render full highlighted HTML, then if long, split: take the shown plain length 700 → find position in raw text... complicated with marks.

Alternative: build the highlighted HTML for the full text, and separately compute a cut point in the raw text at ~700 chars of shown text. Since fn marks are removed in display, mapping is annoying. Pragmatic approach: if r._shown.length > 700, render only the first N chars of raw such that shown length ≈700: iterate raw, accumulate shown length (raw chars minus fn marks), stop at 700 shown chars at a word boundary. Then highlight within that prefix. Implement:

```js
function shownPrefix(raw, limit){
  let shownLen=0, i=0;
  const re=/\[\[fn:\d+\]\]|\S+/g; // hmm
}
```
Simpler: walk raw with a regex that matches either a fn mark or a single char:
```js
function cutRaw(raw, limit){
  let count=0, i=0;
  const tok=/\[\[fn:\d+\]\]|./gsu;
  let m, end=0;
  while((m=tok.exec(raw))){
    if(m[0].startsWith('[[fn:')) continue; // doesn't count
    count++;
    if(count>limit){ 
      // cut at last word boundary before this
      return raw.slice(0, end);
    }
    end = tok.lastIndex;
  }
  return raw;
}
```
Hmm, word boundary: cut at last space in the shown prefix. Let me do: take raw up to the point where shown count reaches limit, then trim back to last whitespace in raw (fn marks adjacent... fine). Then append '…'. Then highlight that prefix. The "Show the full paragraph (N words)" button re-renders full. Word count: shown.split(/\s+/).length.

Actually simpler and robust: if shown.length > 700: display = highlight(cutRaw(raw,700)) + ' …' + button. cutRaw: find raw index where shown-length hits 700, then back off to last whitespace:

```js
function cutRaw(raw, limit){
  let count=0, idx=0, lastSpace=-1;
  const re=/\[\[fn:\d+\]\]|[\s\S]/gu;
  let m;
  while((m=re.exec(raw))){
    const ch=m[0];
    if(ch.length>1) continue; // fn mark
    if(/\s/.test(ch)) lastSpace=idx;
    count++; idx+=ch.length;
    if(count>=limit){
      return raw.slice(0, lastSpace>0?lastSpace:idx);
    }
  }
  return raw;
}
```
Good enough.

Row structure:

```html
<article class="row" data-id>
  <button class="rowhead" aria-expanded>
    <span class="badge">CEDAW</span> <span class="stitle">GC27 …</span>
    <a class="sym" href=doc_url target=_blank rel=noopener>symbol</a>
    <span class="pin">para. 18</span> <span class="yr">2025</span>
  </button>
  <div class="body">
    <p class="text">…highlighted…</p>
    <p class="marks">3 footnote marks removed · <button>show as stored</button></p>
    <p class="note amber">…</p>
    <div class="actions"> (when open)
      <button>Copy citation</button><button>Copy quotation</button><button>Add to draft</button>
      <span>Context: <button>previous</button> | <button>next</button></span>
    </div>
    <div class="ctx"></div>
  </div>
</article>
```
Plan: "A click on a row opens it in place, with three buttons and a 'Context: previous | next' link." So the row click toggles open; when open, show actions. The text is always visible? "Each row: committee badge and short_title; symbol linked...; the text is shown..." — text always shown; click opens actions. I'll make the whole row header clickable to toggle actions; text always visible.

Hmm, but "Details open in place (a clicked row expands)". I'll show text always (it's the point of the app), and clicking the row toggles the action bar + context. Fine.

Copy functions:
```js
async function copyText(str, msgEl){
  try{ await navigator.clipboard.writeText(str); live('Copied: '+str); }
  catch(e){
    // fallback box
    show fallback with textarea/selectable
    live('Clipboard refused — select and copy from the box');
  }
}
```
Fallback: a fixed div with a <textarea readonly> containing text, visible. I'll implement a modal-ish box.

aria-live messages: one #live region.

Draft:
```js
let draft = loadDraft(); // localStorage 'gc_draft_v1' or []
function saveDraft(){ try{ localStorage.setItem(...); storageOK=true }catch(e){ storageOK=false } }
```
Hint: "kept in localStorage when allowed, in memory otherwise" — detect by trying set/remove test at load.

Draft item: {id, citation, quotation, symbol, paragraph, pinpoint, committee, short_title, year, text_copied, text_as_stored, doc_url}. text_copied = the copied quotation text without surrounding quotes? CSV fields: text_copied, text_as_stored. I'll set text_copied = shown text (leading dropped if matched, fn removed) — i.e., the quotation content; text_as_stored = r.text raw. quotation field = “...” + citation for display/copy-all.

Downloads:
```js
function download(name, content, mime){
  const blob = new Blob([content], {type:mime+''});
  const a=document.createElement('a'); a.href=URL.createObjectURL(blob); a.download=name; a.click(); setTimeout(()=>URL.revokeObjectURL(a.href),1000);
}
```
CSV: BOM '\uFEFF' + header + rows, each field wrapped in double quotes with internal " doubled.

TXT: items.map(it=>it.quotation).join('\n\n')? Plan: "Copy all (quotation, new line, citation, blank line between items)". quotation already includes citation... "each with its quotation as copied, its citation" — quotation as copied = “text” citation. Copy all = for each item: quotation + "\n" + citation + "\n\n"? That duplicates citation. Hmm: "Copy all (quotation, new line, citation, blank line between items)" — I'll do: `“text”\ncitation\n\n` per item. Since quotation-as-copied already is “text” citation on one line, copy-all format: quotation line, then citation line, blank line. I'll store item.quote (with quotes, no citation) and item.citation; display shows quote + citation; copy all = quote + '\n' + citation + '\n\n'. And "Copy quotation" copies quote + ' ' + citation. OK.

Checks implementation. Run after load and after each search/render:

```js
function runChecks(){
  const results=[];
  // 1 query
  if(parseError) results.push({ok:false, label:'Query understood', detail: parseError.msg + ' — no results shown'});
  else results.push({ok:true, label:'Query understood', detail: (query? echoStr+' · '+nTerms+' term(s)' : 'no search words · listing all paragraphs that pass the filters')});
  // 2 totals
  const listed = renderedCount; // rows rendered across pages
  results.push({ok: listed===hits.length, label:'Totals', detail:`rows listed across pages ${listed} = hits ${hits.length}`});
  // checkbox sum
  const sum = committeeHitCounts sum; const jointExtra = hits with committees.length>1 counted extra: sum === hits.length + hits.filter(h=>h._committees.length>1).length
  // 3 chart total
  barsSum === hits + jointHits, both shown
  // 4 highlight
  hits without mark (when positive terms exist): list ids/pinpoints; ok if none
  // 5 normalisation
  if query contains straight " ' - : count hits whose raw text contains curly/dash forms; informational pass
  // 6 numbering
  list mismatches etc. ok:true (informational) — but "pass"/"check failed": numbering issues are data quirks, not app failures. I'll mark ok:true with detail listing counts, or ok:false if... The plan: "Hits whose leading number differs... with both numbers" — these are listed; the check is that the app detected them. I'll mark pass when the app's detection matches a recount. Simpler: these lines are informational; mark "pass" if the listed counts equal recomputed counts (trivially true). Hmm. Let me make each check genuinely verify something:
  - Numbering: verify that for each hit, pinpoint string matches the rule recomputed from fields → pass.
  - Marks: for each hit: shown === text.replace(FN,'') and marks === count → pass/fail with pinpoints.
  - Draft: compare stored text → pass/fail.
}
```
Header indicator: n checks pass / failed. Red dot on tab 04 when failures.

Known quirks at load (before any search), computed over all R:
- paragraph 0: count + example symbol
- shared symbols: count of symbols with >1 title + example
- joint: count + example
- duplicated pinpoints: pairs (title,paragraph) with >1 record + example
- leading mismatches: count + example

Now committee full names map:
```js
const COMMITTEE_NAMES = {
  'CAT':'Committee against Torture',
  'CAT-OP':'Subcommittee on Prevention of Torture',
  'CCPR':'Human Rights Committee',
  'CED':'Committee on Enforced Disappearances',
  'CEDAW':'Committee on the Elimination of Discrimination against Women',
  'CERD':'Committee on the Elimination of Racial Discrimination',
  'CESCR':'Committee on Economic, Social and Cultural Rights',
  'CMW':'Committee on Migrant Workers',
  'CRC':'Committee on the Rights of the Child',
  'CRPD':'Committee on the Rights of Persons with Disabilities'
};
```
Fallback: code.

Chart click: 
```js
options: { onClick(e){ const pts = chart.getElementsAtEventForMode(e,'nearest',{intersect:true},true); if(pts.length){ const label = chart.data.labels[pts[0].index]; setOnlyCommittee(label); } } }
```
setOnlyCommittee: tick only that committee, re-render.

Value labels at end of bar: plugin:
```js
const valueLabels = { id:'valueLabels', afterDatasetsDraw(chart){ const {ctx}=chart; ctx.save(); ctx.font='12px ui-monospace, monospace'; ctx.fillStyle='#1d1b18'; chart.data.datasets[0].data.forEach((v,i)=>{ const meta=chart.getDatasetMeta(0); const x=meta.data[i].x; const y=meta.data[i].y; ctx.fillText(String(v), x+6, y+4); }); ctx.restore(); } };
```
Register locally when creating chart (plugins: [valueLabels]).

Chart config:
```js
new Chart(ctx, { type:'bar', data:{labels, datasets:[{data, backgroundColor:'#9b2335', borderWidth:0, categoryPercentage:0.85, barPercentage:0.9}]}, options:{ indexAxis:'y', responsive:true, maintainAspectRatio:false, scales:{ x:{ beginAtZero:true, maxTicksLimit:10, grid:{color:'#d9d2c3'}, ticks:{color:'#1d1b18', font:{family:'ui-monospace, monospace', size:11}} }, y:{ grid:{display:false}, ticks:{color:'#1d1b18', font:{family:'ui-monospace,monospace', size:12}} } }, plugins:{ legend:{display:false}, tooltip:{ callbacks:{ label: c=>' '+c.parsed.x+' paragraphs' } } }, onClick: ... }, plugins:[valueLabels] });
```
Canvas height: set container height = committees*28+40 px.

aria-label on canvas: "Bar chart. Paragraphs per committee: CRC 2091, ..." Build string.

Table beside chart: same numbers, caption "FIG.01 data".

Tabs keyboard: arrow left/right moves focus & activates.

Search dropdown: div under input, shown when input empty && focused. Contains syntax list + 3 example buttons. On input (typing) → hide. On focus with empty → show. Examples: `"best interests" AND child`, `(torture OR ill-treatment) NOT detention`, `"reasonable accommodation"`.

Search execution:
```js
function runSearch(){
  const q = input.value;
  parseError=null; tree=null; terms=[];
  if(q.trim()){
    try{ const toks=tokenize(q); tree=parse(toks); terms=collectPositive(tree); echoStr=describe(tree); }
    catch(e){ parseError=e; }
  }
  applyFilters(); // recompute hits, render all tabs
}
```
applyFilters: compute hits = R.filter(r => (!tree || evalTree(tree, r._norm)) && committeeOK(r) && yearOK(r) && docOK(r)). Then sort, render overview chart, results (reset page count), summary, checkbox hit counts, chips, checks.

Committee hit counts: for each committee code (all distinct committees in data), count hits where r._committees includes code. Display in brackets after search (i.e., when query non-empty? "after a search, its hits in brackets" — I'll show always after any runSearch, including empty query? "after a search" — show when a search has been run; I'll show always once runSearch executed at least once; simpler: always show counts in brackets — but plan says after a search. I'll show them whenever hits computed and a search was run; initial load also runs applyFilters... I'll just always show counts — harmless and informative. Hmm, plan explicitly: "a checkbox per code with its full name and, after a search, its hits in brackets". I'll show brackets only after user has run a search (flag searched=true). Fine.

Chips: under big number, active filters: if committees narrowed (not all ticked) → chip "Committees: n of k ×"; if years narrowed → "Years: from–to ×"; if doc selected → chip with short_title ×. Clicking × removes that filter.

Clear all: reset query? "Headed 'FILTERS', with 'Clear all'" — clears filters (committees all, years min/max, doc blank). I'll also clear search? Keep search; clear all = filters only. Hmm, ambiguous; I'll clear filters and keep the query. Actually "Clear all" in a FILTERS header — filters only. OK.

Order select: options: 'year' (Year, newest first — default), 'doc' (Document order), 'match' (Most matches first). Comparator:
- year: (b.year-a.year) || a.title.localeCompare(b.title) || a.paragraph-b.paragraph
- doc: a.title.localeCompare(b.title) || a.paragraph-b.paragraph || b.year-a.year
- match: score desc (score = number of positive terms matching r._norm), then year desc...

Summary line: `${hits.length} of ${R.length} paragraphs match · ${k} committees · ${minYear}–${maxYear}` + (query? '' : ' · no search words'). aria-live.

Order line: "sorted by year, newest first, then by document and paragraph" changes with select.

Rendering results: container #results; render first `pageSize` (25) rows; "Show 25 more" button increments. Rebuild on each applyFilters (pageSize reset to 25). Each row built via DOM creation or template strings? Use template strings with esc() — careful with event handlers; use event delegation on #results: click on [data-action] buttons.

Row open state: track openIds set; re-render preserves? Simpler: re-render on paging only appends. I'll keep a `shown` count and render rows incrementally: renderRows() renders rows[0..shown). On applyFilters, shown=25, clear container, render. "Show 25 more": shown+=25, render appended rows. Row open state stored in a Set by id, applied during render.

Context: when open and user clicks previous/next: find same-title records sorted by paragraph; locate current index; render neighbor into .ctx div: grey text with pinpoint + highlighted? Just plain grey text (esc) with pinpoint label and symbol link. "Context opens paragraph −1 or +1 of the same title inline, in grey, with its own pinpoint". Implement: ctx div shows "para. 17 (previous): text…" grey. Clicking again toggles? I'll render both prev and next when either clicked? Plan: "Context: previous | next" links — clicking previous shows prev paragraph; clicking next shows next. I'll show the requested one, replacing content.

Add to draft: push item, save, update tab label, live message. If already in draft (same id) → message "already in draft".

Draft tab render: list; each item: blockquote with quotation (as copied: “text” citation), remove button. Buttons: Copy all, Download .txt, Download .csv. Hint about storage.

Checks tab: 
- Section "How the app checks itself" (open): list of check lines.
- "Known quirks of this file": computed at load.
- "How this is computed": short method description.

Method text: describe normalization, parser, matching, citation building, checks. A few lines.

Footer: `source` and `built` + sentence + Credits line: "Chart.js 4, MIT licence — chart rendering." Also maybe note syntax inspired by Wikipedia Help:Searching (CC BY-SA) — "the help text is written fresh, since that page is CC BY-SA" — so no credit needed, but I could mention "syntax inspired by Wikipedia's search help (CC BY-SA); text written fresh." The rules say add Credits line if code/wording from open-licence shelf excerpts is reused. I'm not copying wording; Chart.js is used (MIT) — credit that. I'll add: "Credits: Chart.js 4 (MIT) for FIG.01. Search syntax follows the conventions of Wikipedia Help:Searching (CC BY-SA 4.0); the help text here is written fresh."

Now, header checks indicator: run checks at load (empty query) → e.g. all pass → green dot "8 checks pass". Update after each search.

Let me also handle: "A failed check marks rows; it never drops them." — e.g. numbering check failure marks rows (amber note already). Fine — the amber notes cover it; I'll also add class to rows when relevant checks fail? Keep simple: amber notes already on rows; checks panel lists them.

Highlight check: "Every hit shows at least one <mark> unless the query is NOT-only; a hit matched in norm but without a highlight is listed as 'matched, not highlighted' and still shown." Implement: after computing hits, for each hit, test combined raw regex on r.text; if no match and positive terms exist → add to list. Note: could happen when norm matched via fn-removal joining? e.g. phrase across fn mark where raw gap regex handles it... or when norm's space-replacement of fn marks created adjacency that raw regex handles via gap alternation — should mostly align. Edge: norm replaces fn with space; raw gap `(?:\s|fn)+` requires at least one — if fn mark glued between words with no spaces: raw "word1[[fn:2]]word2", norm "word1 word2" — phrase "word1 word2" matches norm; raw regex gap `(?:\s|fn)+` matches "[[fn:2]]" → matches raw too. Good. Reverse edge: norm removes... fine.

Normalisation check: "When the query holds a straight quote, apostrophe or hyphen, the panel says the curly and dash forms were matched too, and how many hits contain only those forms." Implement: if /["'-]/ in normalized query terms... check raw query for straight " ' -; then count hits whose raw text contains [“”‘’–—] (curly/dash forms) — say "n of the hits contain curly quotes, apostrophes or dashes that were folded to match". Mark pass (informational). I'll phrase as pass with detail.

Now the "committees" of a record for filter: any of r._committees ticked. Chart: count per committee over hits: for each hit, for each c in r._committees → counts[c]++.

Joint hits extra = hits.filter(h=>h._committees.length>1).length — wait, joint is about symbol having 2 codes; _committees includes committee field too. A record with symbol "CMW/C/GC/7–CERD/C/GC/38" and committee "CMW" → codes [CMW, CERD] → length 2 → counts under both. The "joint hits" extra = hits where symbol codes > 1. I'll compute symbolCodes separately: r._symCodes. jointExtra = hits.filter(h=>h._symCodes.length>1).length. Chart note says joint GCs count under both committees.

Checkbox sum check: sum of per-committee counts === hits.length + jointExtra.

Now years filter: from/to inputs type=number, preset min/max. On change → applyFilters.

Document select: optgroups by committee: for each distinct committee (sorted), optgroup label = code, options = distinct titles of that committee... wait, group by committee — records of that committee. Use r.committee for grouping (the record's own committee field). Value = title, label = short_title. Blank option "All documents".

Hmm — but a joint GC record has one committee field; appears under that committee's group. Fine.

Now let me think about performance: 7304 records, evalTree per record per search — fine. Rendering 25 rows — fine. Precompute at load: norm for 7304 records — fine.

localStorage draft load: parse JSON, validate ids exist.

Edge: doc_url could be empty? gc records all have doc_url presumably. Link: if doc_url falsy, show symbol without link. I'll guard.

Now write CSS. Keep it clean:

```css
:root{ --paper:#f4f0e8; --ink:#1d1b18; --rule:#d9d2c3; --red:#9b2335; --amber:#8a5a00; --green:#1e6b3a; --markbg:#f6e9a8; }
*{box-sizing:border-box}
body{margin:0;background:var(--paper);color:var(--ink);font:16px/1.5 -apple-system,'Segoe UI',Roboto,Helvetica,Arial,sans-serif}
.mono{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:11px;letter-spacing:.12em;text-transform:uppercase}
header{padding:20px 28px 12px;border-bottom:1px solid var(--rule)}
...
```

Focus ring: `:focus-visible{outline:3px solid var(--red); outline-offset:2px}`.

Tabs:
```css
#tabs{display:flex;gap:4px;padding:0 28px;border-bottom:1px solid var(--rule);position:sticky;top:0;background:var(--paper)}
#tabs button{...mono...;padding:12px 14px;background:none;border:none;border-bottom:3px solid transparent;cursor:pointer;color:var(--ink)}
#tabs button[aria-selected="true"]{color:var(--red);border-bottom-color:var(--red)}
```

Main: `main{display:flex;align-items:flex-start}` rail: `width:300px;flex:0 0 300px;padding:20px 20px 20px 28px;border-right:1px solid var(--rule);position:sticky;top:49px;max-height:calc(100vh - 49px);overflow:auto`. Content: `flex:1;min-width:0;padding:20px 28px`.

Big number: `.bignum{font-family:Georgia,serif;font-size:48px;line-height:1}`.

Filter headings: numbered headings closed until clicked — only one filter heading here ("01 Committee, years, document") containing all three filter groups. Button with aria-expanded toggles a div.

Checkboxes list: max-height with scroll.

Chips: small removable.

mark: `mark{background:#f3e6a2;color:#1d1b18;font-weight:700;padding:0 1px}`.

Rows: `article.row{border-bottom:1px solid var(--rule);padding:14px 0}` rowhead as a full-width button? I'll make the row header a clickable div with role="button" tabindex? Simpler: a <button class="rowhead"> containing spans (no links inside? symbol link must be clickable — nested interactive elements inside button is invalid). Alternative: row header is a div with click handler; symbol link inside with stopPropagation. Keyboard: make the rowhead have tabindex=0 role=button aria-expanded, keydown Enter/Space toggles. OK.

Actually simpler: each row has a small "open" toggle button (chevron "Open ▸") plus clicking anywhere on header. I'll do: header div with class rowhead, tabindex 0, role button; inside, the symbol <a> with click stopPropagation.

Actions bar: three buttons + context links.

Amber notes: `.note{color:var(--amber)}` with "▲" maybe. Keep text.

Checks: `.pass{color:var(--green)} .fail{color:var(--red)}`.

Draft items: blockquote style with left red border? "share bars" red — use border-left:3px solid var(--red).

Now, the tab count label: `03 DRAFT (4)` — update textContent of tab 3: `03 DRAFT${draft.length? ' ('+draft.length+')':''}`.

Search dropdown positioning: wrap input in relative div; dropdown absolute below.

Let me now also handle "While the box is empty and has focus, a short list opens under it" — focus event: if input.value==='' show; input event: hide; blur: hide (with small timeout so example clicks register — use mousedown on examples).

Examples as <button type=button> — on mousedown (before blur) set value and run.

Now the echo line: `#echo` under the box: after search: "Paragraphs containing the phrase “best interests” and the word child". If parse error: red message "Unbalanced quote — no results. Fix the query." and hits=[].

NOT-only echo: "Paragraphs that do not contain the word torture" etc.

describe(tree):
```js
function describe(n){
  if(!n) return '';
  switch(n.type){
    case 'term': return n.wildcard? 'the word '+n.display+'*' : (n.words.length>1? 'the phrase “'+n.display+'”' : 'the word '+n.display);
    case 'and': return n.args.map(describe).join(' and ');
    case 'or': return n.args.map(describe).join(' or ');
    case 'not': return 'without '+describe(n.arg);
  }
}
```
Echo: if tree && !hasPositive(tree): 'Paragraphs that do not contain '+describeNot... Let me: hasPositive = tree contains term not under not. If !hasPositive: echo = 'Paragraphs that do not contain ' + describeInner(tree) where describeInner for not returns describe(arg), for and joins... I'll write:

```js
function positives(n){ let c=0; (function w(x){ if(!x)return; if(x.type==='term')c++; else if(x.type==='not') w(x.arg); else x.args.forEach(w); })(n); return c; }
```
If positives===0 && tree: echo = 'Paragraphs that do not contain ' + describeNeg(tree) where describeNeg(not)=describe(arg), and→join(' and '), or→join(' or '). Else echo='Paragraphs containing '+describe(tree).

Term count for check: count term nodes total.

Now evalTree with term.re on r._norm.

collectPositive(tree): list of term nodes not under not.

Score for 'match' order: terms.filter(t=>t.re.test(r._norm)).length.

Now checks details:

```js
function runChecks(){
  const out=[];
  const q=input.value.trim();
  // 1
  if(parseError) out.push({ok:false, t:'Query understood', d: parseError.msg+' — no results are shown until the query is fixed.'});
  else out.push({ok:true, t:'Query understood', d: q? ('“'+q+'” → '+echoStr+' · '+termCount+' term(s)') : 'no search words — every paragraph that passes the filters is listed'});
  // 2 totals
  const jointExtra = hits.filter(h=>h._symCodes.length>1).length;
  const cbSum = Object.values(committeeCounts).reduce((a,b)=>a+b,0);
  out.push({ok: renderedRows===hits.length && cbSum===hits.length+jointExtra, t:'Totals', d:`rows listed across pages ${renderedRows} = hits ${hits.length}; committee counts sum to ${cbSum} = ${hits.length} hits + ${jointExtra} joint`});
  // 3 chart
  const barSum = ... same as cbSum; out.push({ok: barSum===hits.length+jointExtra, t:'Chart total (FIG.01)', d:`bars sum to ${barSum} = ${hits.length} hits + ${jointExtra} joint hits (joint General Comments count under both committees)`});
  // 4 highlight
  const noMark = hits.filter(h=> posTerms.length && !combinedRaw.test(h.text));
```
careful: combinedRaw with /g and .test mutates lastIndex — create fresh regex each test or reset lastIndex. I'll create function makeRawCombined() returning new regex; or set lastIndex=0 before test. Use `re.lastIndex=0; re.test(...)`.

```js
  if(posTerms.length===0) out.push({ok:true,t:'Highlight',d:'NOT-only query — nothing is highlighted by design'});
  else if(noMark.length===0) out.push({ok:true,t:'Highlight',d:`all ${hits.length} hits show at least one <mark>`});
  else out.push({ok:false,t:'Highlight',d:`${noMark.length} hit(s) matched in the normalised text but got no <mark>: `+noMark.slice(0,5).map(h=>h.symbol+', '+pinpoint(h)).join('; ')+' — still shown'});
  // 5 normalisation
  if(/["'\-]/.test(q)){ const curly = hits.filter(h=>/[“”‘’–—]/.test(h.text)).length; out.push({ok:true,t:'Normalisation',d:`the query holds a straight quote, apostrophe or hyphen; curly quotes, apostrophes and en/em dashes were folded to match — ${curly} of ${hits.length} hits contain those forms`}); }
  else out.push({ok:true,t:'Normalisation',d:'query holds no quote, apostrophe or hyphen; normalisation still applied to every record at load'});
  // 6 numbering
  const mism = hits.filter(h=>h._lead!=null && h._lead!==h.paragraph);
  const dup = hits.filter(h=>h._dupPin);
  const lettered = hits.filter(h=>h._letter);
  out.push({ok:true,t:'Numbering',d:`${mism.length} leading-number mismatch(es) ${mism.slice(0,3).map(h=>`"${h._leadText}" vs para. ${h.paragraph} (${h.symbol})`).join('; ')}; ${dup.length} duplicated pinpoint(s); ${lettered.length} lettered sub-paragraph(s) — all flagged on their rows, none dropped`});
  // 7 marks
  let bad=0, badEx=[];
  hits.forEach(h=>{ if(h._shown !== h.text.replace(FNG,'') || h._marks !== (h.text.match(FNC)||[]).length){bad++; if(badEx.length<3) badEx.push(h.symbol+', '+pinpoint(h));} });
  out.push({ok:bad===0,t:'Footnote marks',d: bad? `${bad} hit(s) failed: ${badEx.join('; ')}` : `for all ${hits.length} hits, removing [[fn:N]] gives the shown text exactly and the removed count matches (${hits.reduce((a,h)=>a+h._marks,0)} marks in total)`});
  // 8 draft
  let dbad=0, dex=[];
  draft.forEach(it=>{ const r=byId[it.id]; if(!r || r.text!==it.text_as_stored){dbad++; dex.push(it.citation);} });
  out.push({ok:dbad===0,t:'Draft',d: dbad? `${dbad} draft item(s) differ from the stored text: ${dex.join('; ')}` : `all ${draft.length} draft item(s) match the stored text of their record`});
  return out;
}
```
renderedRows = number of rows currently rendered (shown count capped by hits length). Since paging renders all eventually but initially 25 — "Rows listed across pages equal the hits" — hmm, with paging, only 25 shown initially. The check should compare total listed across pages... I'll interpret: rendered rows (shown) ≤ hits and shown+remaining... Let me define: rows listed across pages = hits.length when all pages shown; but check runs at render time with shown=25. To make check meaningful: verify that shown rows correspond to first `shown` of sorted hits — trivially true. Better: check that hits.length === count of records passing filter recomputed independently? I'll do: recompute hits via a second independent pass (filter function) and compare lengths. That's a real check: `hits2 = R.filter(pass)` where pass re-evaluates — same code though. Alternative: verify sorted order is correct and no duplicates: check that the rendered list has no duplicate ids and length min(shown,hits). I'll do: ok = (new Set(renderedIds).size===renderedIds.length) && renderedIds.length===Math.min(shown,hits.length). Detail: "rows listed across pages: X shown of Y hits, no duplicates". Good enough and honest.

Header indicator: after runChecks, count ok → "n checks pass" green or "n checks failed" red; tab 04 gets red dot class when failures.

Known quirks at load (over all R):
```js
quirks = [
 {t:'Preambles (paragraph 0)', n: R.filter(r=>r.paragraph===0).length, ex: example symbol},
 {t:'Symbols shared by several General Comments', n: sharedSymbols.size, ex: ...},
 {t:'Joint General Comments (two symbols in one field)', n: R.filter(r=>r._symCodes.length>1).length ... } // distinct symbols? count records or symbols — I'll count distinct symbols
 {t:'Duplicated pinpoints (same document and paragraph)', n: dupPinKeys.size, ex},
 {t:'Leading number differs from the paragraph field', n: ..., ex}
]
```

Now, "How this is computed" section on tab 04: short paragraphs:
- Load: one pass over records; per record the normalised text, shown text, footnote-mark count, leading number, pinpoint, citation, committees.
- Normalisation: fn marks skipped; curly/straight quotes and apostrophes, en/em dashes, hyphens and non-breaking spaces folded; lower case. The query is normalised the same way.
- Query: tokens… precedence NOT > AND > OR, parentheses; adjacent terms AND; trailing * wildcard; whole words with letter/number boundaries, so "state" also matches "non-State".
- Matching: Boolean tree evaluated over the normalised text of every record; filters (committee, years, document) applied after; sorting by year desc, title, paragraph.
- Citation and quotation are assembled only from the record's fields (symbol, paragraph, title, committee, doc_url); nothing is generated; no model is called and nothing leaves the browser.

Now — the header line: `${R.length.toLocaleString('en-US')} paragraphs from ${titleSet.size} General Comments (distinct title) of ${committeeSet.size} committees, ${minYear}–${maxYear}` + source link. Source: D.source, D.source_url. built: D.built.

Wait — does gc have source_url/built? Description lists {title, source, count, records}. The plan says link source to source_url and footer shows built. I'll guard: `D.source_url ? <a href> : span`. And built may be undefined → show if present. To be safe: `const srcUrl = D.source_url || (D.source && D.source.match(/https?:\/\/\S+/)||[])[0]`. Hmm, overengineering. Just: if D.source_url exists link it; else plain text. Footer: show D.built if present.

Actually the plan explicitly says "`source` linked to `source_url`" — so presumably gc has source_url. I'll use it with fallback.

Now the tab labels: "01 OVERVIEW", "02 PARAGRAPHS", "03 DRAFT", "04 CHECK & METHOD".

Let me now also handle the "search box has focus on load" — input.focus() at end. But that opens the dropdown — fine, it's designed for that.

Arrow-key navigation on tablist:
```js
tabsEl.addEventListener('keydown', e=>{
  if(e.key==='ArrowRight'||e.key==='ArrowLeft'){ e.preventDefault(); const i=[...tabs].indexOf(document.activeElement); const n=(i+(e.key==='ArrowRight'?1:-1)+tabs.length)%tabs.length; tabs[n].focus(); activateTab(tabs[n]); }
});
```

Tab activation: show panel, hide others; on draft tab hide rail; on overview ensure chart rendered (render chart when data changes and tab active; also render lazily when tab first shown).

Chart re-render: destroy previous chart, create new. Keep reference.

Now, "Show 25 more" button: below results; hidden when shown>=hits.length.

Let me write row rendering function:

```js
function rowHTML(r){
  const notes=[];
  if(r._lead!=null && r._lead!==r.paragraph) notes.push(`the text begins ‘${r._leadText}’ but the record is ${pinpoint(r)}: check the document`);
  if(r._letter) notes.push(`a lettered sub-paragraph, numbered ${r.paragraph} by the file`);
  if(r._dupPin) notes.push('two records share this pinpoint');
  if(r._symCodes.length>1) notes.push('joint General Comment');
  ...
}
```
_leadText = the matched "45." string.

Row:
```html
<article class="row" data-id="${r.id}">
  <div class="rowhead" role="button" tabindex="0" aria-expanded="false">
    <span class="badges">${badges}</span>
    <span class="stitle">${esc(r.short_title)}</span>
    <span class="symlink">${r.doc_url?`<a href="${esc(r.doc_url)}" target="_blank" rel="noopener">${esc(r.symbol)}</a>`:esc(r.symbol)}</span>
    <span class="pin">${pinpoint(r)}</span>
    <span class="yr">${r.year}</span>
  </div>
  <div class="rtext">${textHTML}</div>
  <div class="rmarks">${r._marks} footnote mark(s) removed · <button class="linkbtn" data-act="stored">show as stored</button></div>
  ${notes.map(n=>`<div class="rnote">⚠ ${n}</div>`).join('')}
  <div class="actions" hidden>
    <button data-act="cite">Copy citation</button>
    <button data-act="quote">Copy quotation</button>
    <button data-act="draft">Add to draft</button>
    <span class="ctxlink">Context: <button class="linkbtn" data-act="prev">previous</button> | <button class="linkbtn" data-act="next">next</button></span>
  </div>
  <div class="ctx" hidden></div>
</article>
```
Wait — "show as stored" swaps the text: toggle between shown and raw. Store both; on click, replace .rtext content. Since re-render happens on filter change, keep per-row state in a map? Simpler: on click, toggle: if currently shown → set to esc(raw) (no highlight) and label "show as printed"; else re-render highlighted. I'll store flag on element dataset.

Text truncation: if r._shown.length>700 → truncated view with button "Show the full paragraph (N words)". Toggle similar.

Combine: .rtext contains either truncated-highlight + button, or full highlight. And stored toggle overrides. Manage via dataset.mode: 'short'|'full'|'stored'. Render text accordingly:

```js
function textHTML(r){
  const mode = rowMode[r.id]||'short';
  if(mode==='stored') return esc(r.text);
  const long = r._shown.length>700;
  if(mode==='short' && long){
    const cut = cutRaw(r.text, 700);
    return highlightHTML(cut, posTerms) + ' … <button class="linkbtn" data-act="full">Show the full paragraph ('+wordCount(r._shown)+' words)</button>';
  }
  return highlightHTML(r.text, posTerms);
}
```
Hmm — button inside .rtext; the rowhead click toggles actions; clicks on buttons inside rtext shouldn't toggle — I'll attach toggle only to .rowhead, so fine. But data-act delegation on #results handles all buttons.

Wait: highlightHTML on cut prefix — cut at 700 shown chars; highlight regex over the cut raw. Fine.

Also "white-space: pre-wrap keeps stored line breaks" — .rtext{white-space:pre-wrap}.

Actions toggle: click on .rowhead → toggle .actions hidden + aria-expanded. Also Enter/Space on rowhead.

Delegation:
```js
resultsEl.addEventListener('click', e=>{
  const btn = e.target.closest('[data-act]'); 
  const head = e.target.closest('.rowhead');
  if(btn){ const row=btn.closest('.row'); const r=byId[row.dataset.id]; const act=btn.dataset.act;
    if(act==='cite') copyText(citation(r));
    else if(act==='quote') copyText(quoteStr(r));
    else if(act==='draft') addToDraft(r);
    else if(act==='full'){ rowMode[r.id]='full'; refreshRowText(row,r); }
    else if(act==='stored'){ toggle stored }
    else if(act==='prev'||act==='next') showContext(row,r,act);
    e.stopPropagation(); return;
  }
  if(head && !e.target.closest('a')){ toggle actions }
});
```
Also keydown Enter/Space on rowhead.

Symbol link click: it's inside rowhead; e.target.closest('a') guard prevents toggle; link opens new tab naturally.

refreshRowText: re-render .rtext innerHTML via textHTML(r). For 'stored' toggle: dataset.stored flag.

Simplify: keep rowState = {mode:'short'|'full'|'stored'} per id in a Map.

Context: 
```js
function showContext(row, r, dir){
  const same = R.filter(x=>x.title===r.title).sort((a,b)=>a.paragraph-b.paragraph);
  const i = same.findIndex(x=>x.id===r.id);
  const nb = same[i+(dir==='prev'?-1:1)];
  const ctx=row.querySelector('.ctx');
  if(!nb){ ctx.hidden=false; ctx.innerHTML='<span class="grey">No '+(dir==='prev'?'previous':'next')+' paragraph in this document.</span>'; return; }
  ctx.hidden=false;
  ctx.innerHTML = `<div class="grey"><span class="pin">${pinpoint(nb)}</span> ${esc(nb._shown)}</div>`;
}
```
Maybe highlight too — keep plain grey.

Copy fallback box: 
```html
<div id="copybox" hidden><p class="mono">CLIPBOARD REFUSED — SELECT AND COPY</p><textarea id="copyarea" readonly rows="6"></textarea></div>
```
Fixed position bottom. On failure: fill, show, live message. On successful copy: hide.

live(msg): #live textContent = msg (aria-live polite). Show exact string sent: "Copied: CCPR/C/GC/37, para. 12".

Draft tab:
```html
<h2>Your draft (n quotations)</h2>
<div id="draftlist">…</div>
<div class="draftbtns"><button id="copyall">Copy all</button><button id="dlTxt">Download .txt</button><button id="dlCsv">Download .csv</button></div>
<p class="hint">Kept in localStorage when the browser allows it, otherwise in memory only for this session.</p>
```
Empty state: "Nothing collected yet — open a paragraph on tab 02 and choose “Add to draft”."

Item:
```html
<blockquote class="dq"><p>“text” citation</p><button data-remove="id">Remove</button></blockquote>
```

CSV escaping:
```js
const csvField = s => '"'+String(s??'').replace(/"/g,'""')+'"';
```

Download names: 'gc-quotations.txt' / 'gc-quotations.csv'.

Now the Overview tab: 
```html
<h2 class="figtitle">FIG.01 Paragraphs per committee</h2>
<p class="hint">click a bar = tick that committee alone · joint General Comments count under both committees, so the bars can add up to more than the hits</p>
<div class="chartwrap"><canvas id="chart" role="img" aria-label="...">fallback text</canvas></div>
<table class="figtable"><caption>FIG.01 data: paragraphs per committee among the matching paragraphs</caption>...</table>
<p class="how">How this is computed: one count per committee over the paragraphs that match the query and filters.</p>
```

Layout chart + table side by side (flex).

Now — "No view shows more than about seven things to click" — overview: 4 tabs + search + 1 filter heading = 6. OK.

Rail structure:
```html
<aside id="rail">
  <div class="railhead mono">FILTERS <button id="clearall" class="linkbtn">Clear all</button></div>
  <div class="bignum" id="bignum" aria-live="polite">7,304</div>
  <div class="of">matching paragraphs of 7,304</div>
  <div id="chips"></div>
  <div class="searchwrap">
    <label class="mono" for="q">SEARCH THE PARAGRAPHS</label>
    <input id="q" type="text" autocomplete="off" spellcheck="false">
    <button id="go">Search</button>
    <div id="syntax" hidden>…syntax + examples…</div>
  </div>
  <p id="querynorm" class="hint">Whole words, any case. Curly and straight quotes, apostrophes, dashes and hyphens count as the same, and footnote marks are skipped, so State's finds State’s and a phrase can cross a footnote.</p>
  <p id="echo" aria-live="polite"></p>
  <div class="fgroup">
    <button class="fhead" aria-expanded="false"><span class="mono">01 COMMITTEE, YEARS, DOCUMENT</span> <span>▸</span></button>
    <div class="fbody" hidden>
      <div class="fsub mono">COMMITTEE <button id="allc">all</button>/<button id="nonec">none</button></div>
      <div id="committees"></div>
      <div class="fsub mono">YEARS</div>
      <div class="years"><input id="yfrom" type="number"> – <input id="yto" type="number"></div>
      <div class="fsub mono">DOCUMENT</div>
      <select id="docsel"><option value="">All documents</option>…</select>
    </div>
  </div>
</aside>
```
Hmm — "one numbered heading, closed until clicked: 01 Committee, years, document" — a single collapsible containing all three. Good, that's what I have.

Wait, clickable count on paragraphs tab: 4 tabs + search box + 1 filter heading + order select + show more = 8. Plan says 8. OK.

Search button next to input — plan says "a labelled input and a 'Search' button". Put them on one row.

Syntax dropdown content:
```
a space or AND joins words · OR · NOT or a leading minus · "an exact phrase" in double quotes · parentheses · a star at the end of a word for any ending (child* finds children) · operators in capitals; lower-case "or" is a word
Examples: [ "best interests" AND child ] [ (torture OR ill-treatment) NOT detention ] [ "reasonable accommodation" ]
```

Now the header:
```html
<header>
  <div class="mono">UN TREATY BODIES · GENERAL COMMENTS</div>
  <h1>Verbatim finder: General Comments and General Recommendations</h1>
  <p class="meta" id="meta">…</p>
  <div class="checks" id="checkdot"><span class="dot"></span><span id="checktxt"></span></div>
</header>
```
Layout: flex with checks at right.

Meta: `${fmt(R.length)} paragraphs from ${titles} General Comments (distinct title) of ${comms} committees, ${minY}–${maxY} · <a href=source_url>source</a>`.

Hmm "n General Comments (distinct title)" — 188 distinct titles but 159 symbols; some titles repeat? "159 distinct symbol, 188 distinct title" — titles more than symbols because shared symbols hold multiple GCs. So "188 General Comments (distinct title)". OK.

Now write everything. Also remember: `[hidden]{display:none!important}` rule.

Chart.js usage: window.Chart. Guard if missing? It's preloaded; assume present.

One more detail: "the canvas has role="img" and an aria-label stating the numbers, and a small table with the same numbers beside it" — update aria-label on each render.

Chart container height: set style height = (labels.length*26+60)+'px'.

Let me also handle window resize — Chart.js responsive handles it.

Now, about `count` top-level being string "7304" — use R.length.

Potential pitfall: `paragraph` could be 0 → pinpoint 'preamble'. Also paragraph might be string? Description says int. Guard with ==.

Let me now also compute dupPin: map key = title+'|'+paragraph → count; _dupPin = count>1. But lettered subparas share paragraph numbers 1,2,3 within same title — they'd be flagged as dup pinpoints too. Plan says "two records share this pinpoint" note and check lists "hits that share a pinpoint with another record of the same title". Lettered ones have distinct pinpoints ("subpara. (a)") though same paragraph field. Hmm — dup by (title, paragraph) would flag lettered ones as sharing. The plan's quirk list mentions both separately. For the note "two records share this pinpoint" — I'll compute dup by pinpoint string (title+pinpoint) so lettered subparas (different pinpoints) don't trigger it, but the real duplicated pinpoints (CEDAW/C/GC/27 para. 9 twice) do. Use key = title+'|'+pinpoint(r).

Leading mismatch: _lead = parseInt of leading match; mismatch when _lead !== paragraph. Note text uses the raw leading text e.g. "45." — store _leadText = m[0] trimmed? m[0] like "45. " — display ‘45.’. I'll store m[1] and display m[1]+'.'.

Also 3 records in CCPR/C/21/Rev.1/Add.5 numbered 3.1, 3.2 — leading regex ^(\d{1,3})\.\s won't match "3.1." — so no leading, no mismatch note. Fine.

Now the "shared" citation prefix: docName = title up to first colon or " on ". E.g. "General Recommendation No. 29: ..." → "General Recommendation No. 29". Implementation:
```js
function docName(t){ let s=t.split(':')[0]; const i=s.lastIndexOf(' on '); if(i>0) s=s.slice(0,i); return s.trim(); }
```
Hmm "up to the first colon or ' on '" — split at first occurrence of either. Do: find min index of ':' and ' on '. 
```js
function docName(t){ const c=t.indexOf(':'); const o=t.indexOf(' on '); let i=c; if(o>-1 && (i<0||o<i)) i=o; return (i<0?t:t.slice(0,i)).trim(); }
```

Citation for shared: `CERD, General Recommendation No. 29 (A/57/18), para. 3`. Good.

Now, quoteStr(r): 
```js
function quoteStr(r){
  let t=r._shown;
  if(r._lead!=null && r._lead===r.paragraph) t=t.replace(/^\d{1,3}\.\s/,'');
  return '“'+t+'” '+citation(r);
}
```
Wait — shown text starts with "12. The Committee…" — dropping leading "12. " — but only when leading equals paragraph. Note: _shown has fn removed; leading regex on _shown same as text (fn marks unlikely at start). Use r.text match but apply to _shown — fine.

Hmm, should the quotation include the leading number when it matches? Plan says drop it. OK.

Draft item text_copied: the t above (shown, leading dropped). text_as_stored: r.text.

Copy citation: citation(r). Note grey: "UN short form" — add small note next to button? Plan: 'A grey note names the style, "UN short form"'. I'll put a static grey note in the actions bar: `<span class="grey">citation style: UN short form</span>`.

Now let me count lines and write the final file. Aim ~900-1100 lines. Let me write it.

Also remember: before code block, at most three short sentences; after, nothing.

Let me write the HTML now, carefully and completely.

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Verbatim finder — General Comments, paragraph by paragraph</title>
<style>
:root{
  --paper:#f4f0e8; --ink:#1d1b18; --rule:#d9d2c3; --red:#9b2335;
  --amber:#8a5a00; --green:#1e6b3a; --mark:#f3e6a2; --grey:#6f6a60;
}
*{box-sizing:border-box}
[hidden]{display:none!important}
html,body{margin:0;padding:0}
body{background:var(--paper);color:var(--ink);font:16px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
.mono{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:11px;letter-spacing:.14em;text-transform:uppercase}
a{color:var(--red)}
button{font:inherit;color:inherit;background:none;border:none;cursor:pointer;padding:0}
button:hover{text-decoration:underline}
:focus-visible{outline:3px solid var(--red);outline-offset:2px}
header{display:flex;justify-content:space-between;gap:24px;align-items:flex-end;padding:22px 28px 14px;border-bottom:1px solid var(--rule)}
header .kicker{color:var(--red);margin-bottom:6px}
h1{font-family:Georgia,"Times New Roman",serif;font-weight:400;font-size:30px;line-height:1.15;margin:0 0 8px;max-width:60ch}
.meta{margin:0;color:var(--grey);font-size:13px}
.checks{white-space:nowrap;text-align:right;font-family:ui-monospace,Menlo,Consolas,monospace;font-size:11px;letter-spacing:.1em;text-transform:uppercase;padding-bottom:4px}
.dot{display:inline-block;width:10px;height:10px;border-radius:50%;margin-right:6px;vertical-align:baseline}
.dot.ok{background:var(--green)} .dot.bad{background:var(--red)}
#tabs{display:flex;gap:2px;padding:0 28px;border-bottom:1px solid var(--rule);position:sticky;top:0;background:var(--paper);z-index:5}
#tabs button{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:11px;letter-spacing:.14em;text-transform:uppercase;padding:13px 14px 11px;border-bottom:3px solid transparent;color:var(--ink)}
#tabs button[aria-selected="true"]{color:var(--red);border-bottom-color:var(--red)}
#tabs button .tabdot{color:var(--red)}
main{display:flex;align-items:flex-start}
#rail{flex:0 0 308px;width:308px;padding:20px 18px 28px 28px;border-right:1px solid var(--rule);position:sticky;top:44px;max-height:calc(100vh - 44px);overflow:auto}
#content{flex:1;min-width:0;padding:22px 28px 40px}
...
</style>
```

Hmm sticky top for tabs: tabs height ~ 40px; rail top should match tabs bottom. Tabs sticky top:0; rail top: 41px approx. I'll compute roughly; fine.

Continue CSS:

```css
.railhead{display:flex;justify-content:space-between;align-items:center;color:var(--grey);margin-bottom:10px}
.linkbtn{color:var(--red);text-decoration:underline;font-size:inherit}
.bignum{font-family:Georgia,serif;font-size:52px;line-height:1;margin:2px 0 2px}
.of{color:var(--grey);font-size:13px;margin-bottom:8px}
#chips{display:flex;flex-wrap:wrap;gap:6px;margin:6px 0 12px}
.chip{font-family:ui-monospace,monospace;font-size:10px;letter-spacing:.08em;text-transform:uppercase;border:1px solid var(--red);color:var(--red);padding:3px 6px;border-radius:2px;background:none}
.chip:hover{text-decoration:underline}
.searchwrap{position:relative;margin:10px 0 6px}
#q{width:100%;padding:8px 10px;font:inherit;border:1px solid var(--rule);background:#fff;color:var(--ink)}
#go{margin-top:6px;border:1px solid var(--ink);padding:6px 14px}
#go:hover{background:var(--ink);color:var(--paper);text-decoration:none}
#syntax{position:absolute;z-index:20;top:100%;left:0;right:0;background:#fff;border:1px solid var(--rule);padding:12px 14px;font-size:13px;line-height:1.5;box-shadow:0 2px 0 rgba(0,0,0,.04)}
#syntax ul{margin:0 0 8px;padding-left:18px}
#syntax .ex{display:block;margin:4px 0;text-align:left;font-family:ui-monospace,monospace;font-size:12px;color:var(--red);text-decoration:underline}
.hint{font-size:12.5px;color:var(--grey);line-height:1.5}
#echo{font-size:13px;margin:8px 0 0;min-height:1em}
#echo.err{color:var(--red)}
.fgroup{margin-top:16px;border-top:1px solid var(--rule)}
.fhead{width:100%;display:flex;justify-content:space-between;align-items:center;padding:12px 0;color:var(--ink)}
.fhead .mono{color:var(--ink)}
.fhead[aria-expanded="true"] .mono{color:var(--red)}
.fbody{padding:2px 0 14px}
.fsub{color:var(--grey);margin:12px 0 6px;display:flex;gap:8px;align-items:center}
.fsub button{color:var(--red);text-decoration:underline;font-size:10px}
#committees{max-height:220px;overflow:auto;border-top:1px solid var(--rule)}
#committees label{display:flex;gap:8px;align-items:baseline;padding:5px 2px;border-bottom:1px solid var(--rule);font-size:13.5px;cursor:pointer}
#committees input{accent-color:var(--red)}
#committees .cnt{color:var(--grey);font-family:ui-monospace,monospace;font-size:11px}
.years{display:flex;gap:8px;align-items:center}
.years input{width:90px;padding:5px 8px;border:1px solid var(--rule);font:inherit;background:#fff}
#docsel{width:100%;padding:6px 8px;border:1px solid var(--rule);font:inherit;background:#fff}
```

Content/tabs CSS:

```css
.panel{padding-top:6px}
h2.fig{font-family:Georgia,serif;font-weight:400;font-size:22px;margin:0 0 4px}
.figwrap{display:flex;gap:28px;align-items:flex-start;flex-wrap:wrap;margin-top:10px}
.chartbox{flex:1 1 420px;min-width:0}
.chartbox .canvaswrap{position:relative}
table.figtable{border-collapse:collapse;font-size:13.5px;flex:0 0 240px}
.figtable caption{text-align:left;font-family:ui-monospace,monospace;font-size:10px;letter-spacing:.12em;text-transform:uppercase;color:var(--grey);padding-bottom:6px}
.figtable th,.figtable td{border-bottom:1px solid var(--rule);padding:4px 10px 4px 0;text-align:left}
.figtable td.num,.figtable th.num{text-align:right;font-variant-numeric:tabular-nums}
.how{font-size:12.5px;color:var(--grey);border-top:1px solid var(--rule);margin-top:18px;padding-top:8px;max-width:70ch}
.summary{font-size:15px;margin:0 0 4px}
.orderline{display:flex;gap:10px;align-items:center;flex-wrap:wrap;color:var(--grey);font-size:13px;margin-bottom:14px}
.orderline select{padding:4px 8px;border:1px solid var(--rule);font:inherit;background:#fff}
article.row{border-bottom:1px solid var(--rule);padding:14px 0 12px}
.rowhead{display:flex;flex-wrap:wrap;gap:6px 12px;align-items:baseline;cursor:pointer}
.badge{font-family:ui-monospace,monospace;font-size:10px;letter-spacing:.1em;border:1px solid var(--ink);padding:2px 6px;text-transform:uppercase}
.stitle{font-size:13.5px;color:var(--grey)}
.symlink a{font-family:ui-monospace,monospace;font-size:12px}
.pin{font-family:ui-monospace,monospace;font-size:12px;color:var(--red)}
.yr{color:var(--grey);font-size:13px}
.rtext{margin:8px 0 4px;white-space:pre-wrap;font-size:15px;max-width:88ch}
.rmarks{font-size:12px;color:var(--grey)}
.rnote{font-size:12.5px;color:var(--amber);margin-top:4px}
.actions{display:flex;gap:10px;align-items:center;flex-wrap:wrap;margin-top:10px;padding-top:8px;border-top:1px dashed var(--rule)}
.actions button{border:1px solid var(--ink);padding:5px 12px;font-size:13.5px}
.actions button:hover{background:var(--ink);color:var(--paper);text-decoration:none}
.ctxlink{font-size:13px;color:var(--grey)}
.ctx{margin-top:8px;padding:8px 12px;border-left:3px solid var(--rule);color:var(--grey);font-size:14px;white-space:pre-wrap;max-width:88ch}
.ctx .pin{color:var(--grey)}
mark{background:var(--mark);color:var(--ink);font-weight:700;padding:0 1px}
#more{margin:18px 0;border:1px solid var(--ink);padding:8px 18px}
#more:hover{background:var(--ink);color:var(--paper)}
```

Draft & checks CSS:

```css
.dq{border-left:3px solid var(--red);margin:0 0 16px;padding:4px 0 4px 16px;max-width:88ch}
.dq p{margin:0 0 6px;white-space:pre-wrap}
.dq button{font-size:12.5px;color:var(--red);text-decoration:underline}
.draftbtns{display:flex;gap:10px;flex-wrap:wrap;margin:6px 0 12px}
.draftbtns button{border:1px solid var(--ink);padding:7px 16px}
.draftbtns button:hover{background:var(--ink);color:var(--paper)}
.checkline{display:flex;gap:10px;padding:7px 0;border-bottom:1px solid var(--rule);font-size:14px}
.checkline .st{font-family:ui-monospace,monospace;font-size:10px;letter-spacing:.1em;text-transform:uppercase;flex:0 0 110px;padding-top:3px}
.pass{color:var(--green)} .fail{color:var(--red)}
h3.sec{font-family:Georgia,serif;font-weight:400;font-size:19px;margin:26px 0 8px}
.quirk{padding:6px 0;border-bottom:1px solid var(--rule);font-size:14px}
.quirk .n{font-family:Georgia,serif;font-size:18px;margin-right:8px}
.method p{max-width:78ch;font-size:14.5px}
footer{border-top:1px solid var(--rule);padding:12px 28px 20px;font-family:ui-monospace,monospace;font-size:10.5px;letter-spacing:.1em;text-transform:uppercase;color:var(--grey);line-height:1.8}
#live{position:fixed;left:0;right:0;bottom:0;background:var(--ink);color:var(--paper);padding:8px 28px;font-size:13px;z-index:50}
#copybox{position:fixed;right:16px;bottom:44px;width:min(560px,90vw);background:#fff;border:1px solid var(--ink);padding:12px;z-index:60}
#copybox textarea{width:100%;font:13px/1.4 ui-monospace,monospace}
@media (max-width:900px){ main{flex-direction:column} #rail{position:static;width:auto;flex:none;max-height:none;border-right:none;border-bottom:1px solid var(--rule)} }
```

Now the body HTML and script. Let me write the script fully.

```js
(function(){
"use strict";
const D = window.WORKSHOP_DATA.gc;
const R = D.records;
const $ = s => document.querySelector(s);
const $$ = s => [...document.querySelectorAll(s)];
const esc = s => String(s).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const fmt = n => n.toLocaleString('en-US');
const FNG = /\[\[fn:\d+\]\]/g;
const FNC = /\[\[fn:/g;

const COMMITTEE_NAMES = {...};

function normText(s){
  return s.replace(FNG,' ')
    .replace(/[\u201c\u201d\u201e]/g,'"')
    .replace(/[\u2018\u2019\u201a]/g,"'")
    .replace(/[\u2013\u2014\u00ad]/g,'-')
    .replace(/\u00a0/g,' ')
    .replace(/\s+/g,' ')
    .toLowerCase().trim();
}
const escRe = s => s.replace(/[.*+?^${}()|[\]\\]/g,'\\$&');

// ---- precompute ----
const symbolTitles = new Map();
R.forEach(r=>{ if(!symbolTitles.has(r.symbol)) symbolTitles.set(r.symbol,new Set()); symbolTitles.get(r.symbol).add(r.title); });
const sharedSymbols = new Set([...symbolTitles].filter(([s,t])=>t.size>1).map(([s])=>s));
const pinCount = new Map();
R.forEach(r=>{ const k=r.title+'|'+pinpointOf(r); pinCount.set(k,(pinCount.get(k)||0)+1); });
```
Wait pinpointOf needs r fields; define function first:

```js
function pinpointOf(r){
  if(r.paragraph===0) return 'preamble';
  const m = String(r.text).match(/^\(([a-z]{1,4})\)/);
  if(m) return 'subpara. ('+m[1]+')';
  return 'para. '+r.paragraph;
}
```
But pinCount uses pinpointOf before records precomputed — fine, it only uses r.text/r.paragraph.

CODE_RE:
```js
const CODE_RE = /(CAT\/OP|CAT|CCPR|CEDAW|CED|CERD|CESCR|CMW|CRC|CRPD)\b/g;
```
Hmm \b after CEDAW: "CEDAW/C/GC/27" — CEDAW then '/' → boundary ok. But alternation order: at "CEDAW", tries CAT/OP no, CAT no, CCPR no, CEDAW yes. Good. At "CED/C/GC/..." CED matches. But careful: in "CEDAW", if CEDAW listed after CED, CED would match "CED" then \b fails (A follows) → engine tries next alternative CEDAW → ok. Either order works due to \b. Keep longest-first anyway.

```js
function symCodes(r){
  const found = (String(r.symbol).match(CODE_RE)||[]).map(c=>c==='CAT/OP'?'CAT-OP':c);
  return [...new Set(found)];
}
```

Precompute loop:
```js
const byId = {};
R.forEach(r=>{
  const text = String(r.text||'');
  const shown = text.replace(FNG,'');
  const marks = (text.match(FNC)||[]).length;
  const norm = normText(text);
  const leadM = text.match(/^(\d{1,3})\.\s/);
  const letterM = text.match(/^\(([a-z]{1,4})\)/);
  const sc = symCodes(r);
  const committees = [...new Set([...sc, r.committee])];
  const rec = {
    r, id:r.id, text, shown, marks, norm,
    lead: leadM? parseInt(leadM[1],10): null,
    leadText: leadM? leadM[1]+'.' : null,
    letter: letterM? letterM[1] : null,
    symCodes: sc, committees,
    joint: sc.length>1,
    shared: sharedSymbols.has(r.symbol),
    pin: pinpointOf(r),
    dupPin: false
  };
  rec.pinKey = r.title+'|'+rec.pin;
  rec.citation = rec.shared
    ? r.committee+', '+docName(r.title)+' ('+r.symbol+'), '+rec.pin
    : r.symbol+', '+rec.pin;
  byId[r.id]=rec;
});
R.forEach(r=>{ const rec=byId[r.id]; rec.dupPin = (pinCount.get(rec.pinKey)||0)>1; });
```
Hmm — I set dupPin after; but pinCount computed with pinpointOf on raw records — same result. OK. Actually simpler: compute pinCount in first loop after rec creation. Let me restructure: first loop creates recs and fills pinCount; second loop sets dupPin. Fine as written but pinCount built from raw r — same. I'll build pinCount in the first loop using rec.pin.

docName:
```js
function docName(t){
  const c = t.indexOf(':'); const o = t.indexOf(' on ');
  let i = c;
  if(o>-1 && (i<0 || o<i)) i=o;
  return (i<0?t:t.slice(0,i)).trim();
}
```

Totals:
```js
const titles = new Set(R.map(r=>r.title));
const comms = [...new Set(R.map(r=>r.committee))].sort();
const years = R.map(r=>r.year);
const minY = Math.min(...years), maxY = Math.max(...years);
```
Math.min over 7304 — fine.

Query parser:

```js
function tokenize(q){
  const toks=[]; let i=0;
  while(i<q.length){
    const c=q[i];
    if(/\s/.test(c)){i++;continue;}
    if(c==='('){toks.push({t:'LP',raw:c});i++;continue;}
    if(c===')'){toks.push({t:'RP',raw:c});i++;continue;}
    if(c==='"'||c==='\u201c'||c==='\u201d'){
      let j = q.indexOf(c==='"'?'"':'\u201d', i+1);
      if(j<0 && c!=='"') j = q.indexOf('"', i+1);
      if(j<0) throw {msg:'Unbalanced quote: the phrase starting at “'+q.slice(i+1,i+25)+'… has no closing quote.'};
      toks.push({t:'PHRASE', raw:q.slice(i,j+1), inner:q.slice(i+1,j)});
      i=j+1; continue;
    }
    let j=i;
    while(j<q.length && !/[\s()\u201c\u201d"]/.test(q[j])) j++;
    const w=q.slice(i,j);
    if(w==='AND'||w==='OR'||w==='NOT'){toks.push({t:w,raw:w});i=j;continue;}
    if(w.length>1 && w[0]==='-'){toks.push({t:'NOTW',raw:w,word:w.slice(1)});i=j;continue;}
    toks.push({t:'WORD',raw:w,word:w});
    i=j;
  }
  return toks;
}
```
Edge: word run stops at quotes — `don"t` splits; acceptable.

normWord:
```js
function normWord(s){
  return s.replace(/[\u201c\u201d\u201e]/g,'"').replace(/[\u2018\u2019\u201a]/g,"'")
    .replace(/[\u2013\u2014\u00ad]/g,'-').toLowerCase();
}
```

makeTerm:
```js
function makeTerm(rawWord, isPhrase){
  let w = normWord(rawWord);
  const wildcard = w.endsWith('*');
  if(wildcard) w = w.slice(0,-1);
  const words = w.split(/\s+/).filter(Boolean);
  if(!words.length) throw {msg:'Empty term in the query.'};
  const display = rawWord;
  const core = words.map(escRe).join('\\s+') + (wildcard?'\\w*':'');
  const re = new RegExp('(?<![\\p{L}\\p{N}])'+core+'(?![\\p{L}\\p{N}])','u');
  // raw highlight regex
  const rawParts = words.map(wd=>wd.split('').map(rawChar).join(''));
  const rawCore = rawParts.join('(?:\\s|\\[\\[fn:\\d+\\]\\])+') + (wildcard?'\\w*':'');
  const rawRe = new RegExp('(?<![\\p{L}\\p{N}])'+rawCore+'(?![\\p{L}\\p{N}])','giu');
  return {type:'term', words, wildcard, display, isPhrase, re, rawRe};
}
function rawChar(c){
  if(c==='"') return '["\u201c\u201d\u201e]';
  if(c==="'") return "['\u2018\u2019\u201a]";
  if(c==='-') return '[-\u2013\u2014\u00ad]';
  return escRe(c);
}
```

Parser:
```js
function parseQuery(q){
  const toks = tokenize(q);
  let pos=0;
  const peek=()=>toks[pos];
  function isTermStart(t){ return t && (t.t==='WORD'||t.t==='PHRASE'||t.t==='NOTW'||t.t==='NOT'||t.t==='LP'); }
  function parseOr(){
    let left=parseAnd();
    while(peek()&&peek().t==='OR'){pos++; left={type:'or',args:[left,parseAnd()]};}
    return left;
  }
  function parseAnd(){
    let left=parseNot();
    while(peek()&&(peek().t==='AND'||isTermStart(peek()))){
      if(peek().t==='AND') pos++;
      left={type:'and',args:[left,parseNot()]};
    }
    return left;
  }
  function parseNot(){
    const t=peek();
    if(t&&t.t==='NOT'){pos++; return {type:'not',arg:parseNot()};}
    if(t&&t.t==='NOTW'){pos++; return {type:'not',arg:makeTerm(t.word,false)};}
    return parsePrimary();
  }
  function parsePrimary(){
    const t=peek();
    if(!t) throw {msg:'The query ends where a term or ) was expected.'};
    if(t.t==='LP'){pos++; const e=parseOr(); if(!peek()||peek().t!=='RP') throw {msg:'Unbalanced parenthesis: ( has no matching )'}; pos++; return e;}
    if(t.t==='WORD'){pos++; return makeTerm(t.word,false);}
    if(t.t==='PHRASE'){pos++; return makeTerm(t.inner,true);}
    throw {msg:'Unexpected "'+t.raw+'" in the query.'};
  }
  if(!toks.length) return null;
  const tree=parseOr();
  if(pos<toks.length) throw {msg:'Unexpected "'+toks[pos].raw+'" — check the parentheses.'};
  return tree;
}
```
Wait: parseAnd loop condition — after parseNot, if next is 'OR' we stop (good), if 'RP' stop, if 'AND' or term start continue. But NOT/NOTW as start of parseNot handled. However isTermStart includes 'NOT' — in parseAnd loop, if peek is NOT, we call parseNot which consumes it. Good.

Issue: `parseAnd` while condition `peek().t==='AND'||isTermStart(peek())` — isTermStart includes LP; `(` after term → implicit AND with parenthesized group. Good.

evalTree:
```js
function evalTree(n, norm){
  if(n.type==='term') return n.re.test(norm);
  if(n.type==='and') return n.args.every(a=>evalTree(a,norm));
  if(n.type==='or') return n.args.some(a=>evalTree(a,norm));
  if(n.type==='not') return !evalTree(n.arg,norm);
  return true;
}
```

collectTerms (positive only):
```js
function collectPos(n, out){
  if(!n) return;
  if(n.type==='term'){ out.push(n); return; }
  if(n.type==='not') return;
  n.args.forEach(a=>collectPos(a,out));
}
function countTerms(n){ let c=0; (function w(x){ if(!x)return; if(x.type==='term')c++; else if(x.type==='not')w(x.arg); else x.args.forEach(w); })(n); return c; }
```

describe:
```js
function describe(n){
  if(n.type==='term') return n.isPhrase? 'the phrase \u201c'+n.display+'\u201d' : 'the word '+n.display+(n.wildcard?'*':'');
  if(n.type==='and') return n.args.map(describe).join(' and ');
  if(n.type==='or') return n.args.map(describe).join(' or ');
  if(n.type==='not') return 'without '+describe(n.arg);
}
function hasPos(n){ let c=0; (function w(x){ if(!x)return; if(x.type==='term')c++; else if(x.type==='not')return; else x.args.forEach(w); })(n); return c>0; }
```

State:
```js
let tree=null, parseError=null, posTerms=[], echoStr='', termCount=0;
let hits=[], committeeCounts={}, shown=25, order='year';
let ticked = new Set(comms);
let yFrom=minY, yTo=maxY, docSel='';
let searched=false;
const rowState = new Map(); // id -> 'short'|'full'|'stored'
let openRows = new Set();
```

applyFilters:
```js
function applyFilters(){
  const q = $('#q').value;
  parseError=null; tree=null; posTerms=[]; echoStr=''; termCount=0;
  if(q.trim()){
    try{
      tree = parseQuery(q);
      if(tree){ posTerms=[]; collectPos(tree,posTerms); termCount=countTerms(tree); echoStr=describe(tree); }
    }catch(e){ parseError=e; }
  }
  const yf = parseInt($('#yfrom').value,10), yt = parseInt($('#yto').value,10);
  yFrom = isNaN(yf)?minY:yf; yTo = isNaN(yt)?maxY:yt;
  docSel = $('#docsel').value;
  hits = [];
  committeeCounts = {}; comms.forEach(c=>committeeCounts[c]=0);
  for(const rec of Object.values(byId)){
    if(tree && !evalTree(tree, rec.norm)) continue;
    if(tree===null && parseError) continue; // error → no results
    if(!rec.committees.some(c=>ticked.has(c))) continue;
    if(rec.r.year < yFrom || rec.r.year > yTo) continue;
    if(docSel && rec.r.title!==docSel) continue;
    hits.push(rec);
    rec.committees.forEach(c=>{ if(committeeCounts[c]!=null) committeeCounts[c]++; });
  }
  if(parseError) hits=[];
  sortHits();
  shown=25;
  renderAll();
}
```
Hmm — when parseError, hits=[] and echo shows error. Also "shows a message and no results". OK. But careful: `if(tree && !eval...)` — when parseError, tree null → would list all; so explicitly clear. Handled.

Wait also: when parseError, committeeCounts all zero — fine.

sortHits:
```js
function sortHits(){
  const score = rec => posTerms.reduce((a,t)=>a+(t.re.test(rec.norm)?1:0),0);
  if(order==='year') hits.sort((a,b)=> (b.r.year-a.r.year) || String(a.r.title).localeCompare(b.r.title) || (a.r.paragraph-b.r.paragraph));
  else if(order==='doc') hits.sort((a,b)=> String(a.r.title).localeCompare(b.r.title) || (a.r.paragraph-b.r.paragraph) || (b.r.year-a.r.year));
  else hits.sort((a,b)=> score(b)-score(a) || (b.r.year-a.r.year) || String(a.r.title).localeCompare(b.r.title) || (a.r.paragraph-b.r.paragraph));
}
```
Note: rec.r.paragraph — I stored r in rec.r. OK.

renderAll: update bignum, chips, echo, committee checkbox counts, summary, results, chart, checks, tab label.

```js
function renderAll(){
  $('#bignum').textContent = fmt(hits.length);
  $('#of').textContent = 'matching paragraphs of '+fmt(R.length);
  renderChips();
  renderEcho();
  renderCommCounts();
  renderSummary();
  renderResults();
  renderChart();
  renderChecks();
}
```

renderEcho:
```js
function renderEcho(){
  const el=$('#echo');
  if(parseError){ el.textContent=''; el.classList.add('err'); el.textContent=parseError.msg+' — no results until the query is fixed.'; return; }
  el.classList.remove('err');
  if(!tree){ el.textContent = searched? 'No search words — every paragraph that passes the filters is listed.' : ''; return; }
  const pos = hasPos(tree);
  el.textContent = pos? 'Paragraphs containing '+echoStr+'.' : 'Paragraphs that do not contain '+describeNeg(tree)+'.';
}
function describeNeg(n){
  if(n.type==='not') return describe(n.arg);
  if(n.type==='and') return n.args.map(describeNeg).join(' and ');
  if(n.type==='or') return n.args.map(describeNeg).join(' or ');
  return describe(n);
}
```

renderChips:
```js
function renderChips(){
  const box=$('#chips'); box.innerHTML='';
  const chips=[];
  if(ticked.size!==comms.length) chips.push({label:'Committees: '+ticked.size+' of '+comms.length, fn:()=>{ comms.forEach(c=>ticked.add(c)); }});
  if(yFrom!==minY||yTo!==maxY) chips.push({label:'Years: '+yFrom+'–'+yTo, fn:()=>{ $('#yfrom').value=minY; $('#yto').value=maxY; }});
  if(docSel) chips.push({label:'Document: '+shortOf(docSel), fn:()=>{ $('#docsel').value=''; }});
  chips.forEach(ch=>{
    const b=document.createElement('button'); b.className='chip'; b.type='button';
    b.textContent=ch.label+' ×';
    b.title='remove this filter';
    b.onclick=()=>{ ch.fn(); applyFilters(); };
    box.appendChild(b);
  });
}
function shortOf(title){ const r=R.find(x=>x.title===title); return r? r.short_title : title; }
```

renderCommCounts: update each label's .cnt span: searched? ` (${committeeCounts[c]})` : ''. Also checkbox checked state = ticked.has(c).

Committee list built once:
```js
function buildCommitteeList(){
  const box=$('#committees'); box.innerHTML='';
  comms.forEach(c=>{
    const lab=document.createElement('label');
    const cb=document.createElement('input'); cb.type='checkbox'; cb.checked=true;
    cb.addEventListener('change',()=>{ if(cb.checked) ticked.add(c); else ticked.delete(c); applyFilters(); });
    const name=document.createElement('span'); name.textContent=(COMMITTEE_NAMES[c]||c);
    const cnt=document.createElement('span'); cnt.className='cnt'; cnt.dataset.c=c;
    lab.append(cb,name,cnt); box.appendChild(lab);
  });
}
```
Hmm label text: code + full name + count. I'll show `CERD — Committee on the Elimination of Racial Discrimination [12]`. Put code in a mono span. Let me: `<span class="mono" style="...">CERD</span> name <span class=cnt>`. Fine.

all/none buttons: set all checkboxes checked & ticked = all/none, applyFilters.

renderCommCounts:
```js
function renderCommCounts(){
  $$('#committees .cnt').forEach(el=>{
    const c=el.dataset.c;
    el.textContent = searched? ' ['+fmt(committeeCounts[c]||0)+']' : '';
  });
  $$('#committees input').forEach(cb=>{ /* sync checked */ });
}
```
Need mapping cb→c: store dataset.c on cb too.

renderSummary:
```js
function renderSummary(){
  const el=$('#summary');
  if(!hits.length){ el.textContent = parseError? '' : '0 of '+fmt(R.length)+' paragraphs match.'; }
  else{
    const cs=[...new Set(hits.flatMap(h=>h.committees))];
    const ys=hits.map(h=>h.r.year);
    el.textContent = fmt(hits.length)+' of '+fmt(R.length)+' paragraphs match · '+cs.length+' committees · '+Math.min(...ys)+'–'+Math.max(...ys)+(tree?'':' · no search words');
  }
  el.setAttribute('aria-live','polite');
  const ord=$('#orderline .desc');
  ord.textContent = order==='year'? 'sorted by year, newest first, then by document and paragraph' : order==='doc'? 'sorted by document, then paragraph' : 'sorted by most matched terms first, then year, newest first';
}
```

renderResults:
```js
function renderResults(){
  const box=$('#results'); box.innerHTML='';
  const n=Math.min(shown,hits.length);
  for(let i=0;i<n;i++) box.appendChild(rowEl(hits[i]));
  const more=$('#more');
  if(shown<hits.length){ more.hidden=false; more.textContent='Show 25 more ('+fmt(Math.min(25,hits.length-shown))+' of '+fmt(hits.length-shown)+' remaining)'; }
  else more.hidden=true;
}
```
Hmm "Show 25 more" — label 'Show 25 more'. I'll keep simple: 'Show 25 more' plus remaining count in summary? Keep 'Show 25 more'.

rowEl(rec): build DOM via createElement or innerHTML template. I'll use innerHTML on article then attach. Since handlers are delegated, innerHTML fine.

```js
function rowEl(rec){
  const r=rec.r;
  const art=document.createElement('article');
  art.className='row'; art.dataset.id=rec.id;
  const badges = rec.committees.map(c=>'<span class="badge">'+esc(c)+'</span>').join(' ');
  const sym = r.doc_url? '<a href="'+esc(r.doc_url)+'" target="_blank" rel="noopener">'+esc(r.symbol)+'</a>' : esc(r.symbol);
  const notes=[];
  if(rec.lead!=null && rec.lead!==r.paragraph) notes.push('the text begins \u2018'+rec.leadText+'\u2019 but the record is '+rec.pin+': check the document');
  if(rec.letter) notes.push('a lettered sub-paragraph, numbered '+r.paragraph+' by the file');
  if(rec.dupPin) notes.push('two records share this pinpoint');
  if(rec.joint) notes.push('joint General Comment');
  art.innerHTML =
    '<div class="rowhead" role="button" tabindex="0" aria-expanded="'+(openRows.has(rec.id))+'">'+
      '<span class="badges">'+badges+'</span>'+
      '<span class="stitle">'+esc(r.short_title||'')+'</span>'+
      '<span class="symlink">'+sym+'</span>'+
      '<span class="pin">'+esc(rec.pin)+'</span>'+
      '<span class="yr">'+r.year+'</span>'+
    '</div>'+
    '<div class="rtext">'+textHTML(rec)+'</div>'+
    (rec.marks? '<div class="rmarks">'+rec.marks+' footnote mark'+(rec.marks>1?'s':'')+' removed · <button type="button" class="linkbtn" data-act="stored">show as stored</button></div>' : '')+
    notes.map(n=>'<div class="rnote">\u26a0 '+esc(n)+'</div>').join('')+
    '<div class="actions"'+(openRows.has(rec.id)?'':' hidden')+'>'+
      '<button type="button" data-act="cite">Copy citation</button>'+
      '<button type="button" data-act="quote">Copy quotation</button>'+
      '<button type="button" data-act="draft">Add to draft</button>'+
      '<span class="ctxlink">Context: <button type="button" class="linkbtn" data-act="prev">previous</button> | <button type="button" class="linkbtn" data-act="next">next</button></span>'+
      '<span class="grey">citation style: UN short form</span>'+
    '</div>'+
    '<div class="ctx" hidden></div>';
  return art;
}
```
.grey class: color grey small.

textHTML(rec):
```js
function textHTML(rec){
  const mode = rowState.get(rec.id)||'short';
  if(mode==='stored') return esc(rec.text);
  const long = rec.shown.length>700;
  if(mode==='short' && long){
    const cut = cutRaw(rec.text,700);
    return highlightHTML(cut)+' \u2026 <button type="button" class="linkbtn" data-act="full">Show the full paragraph ('+wordCount(rec.shown)+' words)</button>';
  }
  return highlightHTML(rec.text);
}
function wordCount(s){ return s.split(/\s+/).filter(Boolean).length; }
function cutRaw(raw, limit){
  let count=0, idx=0, lastSpace=-1;
  const re=/\[\[fn:\d+\]\]|[\s\S]/gu;
  let m;
  while((m=re.exec(raw))){
    if(m[0].length>1) continue;
    if(/\s/.test(m[0])) lastSpace=idx;
    count++; idx+=m[0].length;
    if(count>=limit) return raw.slice(0, lastSpace>0?lastSpace:idx);
  }
  return raw;
}
function highlightHTML(raw){
  if(!posTerms.length) return esc(raw).replace(FNG,'');
  const re=new RegExp(posTerms.map(t=>'('+t.rawRe.source+')').join('|'),'giu');
  let out='', last=0, m;
  while((m=re.exec(raw))){
    out+=esc(raw.slice(last,m.index)).replace(FNG,'');
    out+='<mark>'+esc(m[0]).replace(FNG,'')+'</mark>';
    last=m.index+m[0].length;
    if(!m[0].length) re.lastIndex++;
  }
  out+=esc(raw.slice(last)).replace(FNG,'');
  return out;
}
```
Note: rawRe already has flags giu; embedding .source into new RegExp with 'giu' — fine.

Delegation on #results:
```js
$('#results').addEventListener('click', e=>{
  const btn=e.target.closest('[data-act]');
  if(btn){
    const art=btn.closest('.row'); const rec=byId[art.dataset.id];
    const act=btn.dataset.act;
    if(act==='cite') copyText(rec.citation);
    else if(act==='quote') copyText(quoteStr(rec));
    else if(act==='draft') addToDraft(rec);
    else if(act==='full'){ rowState.set(rec.id,'full'); art.querySelector('.rtext').innerHTML=textHTML(rec); }
    else if(act==='stored'){ const cur=rowState.get(rec.id)||'short'; rowState.set(rec.id, cur==='stored'?'short':'stored'); art.querySelector('.rtext').innerHTML=textHTML(rec); btn.textContent = cur==='stored'?'show as stored':'show as printed'; }
    else if(act==='prev'||act==='next') showContext(art,rec,act);
    e.stopPropagation();
    return;
  }
  const head=e.target.closest('.rowhead');
  if(head && !e.target.closest('a')){
    const art=head.closest('.row'); const id=art.dataset.id;
    if(openRows.has(id)){ openRows.delete(id); } else openRows.add(id);
    head.setAttribute('aria-expanded', openRows.has(id));
    art.querySelector('.actions').hidden=!openRows.has(id);
  }
});
$('#results').addEventListener('keydown', e=>{
  if((e.key==='Enter'||e.key===' ') && e.target.classList.contains('rowhead')){ e.preventDefault(); e.target.click(); }
});
```
Hmm e.target.click() on rowhead triggers click handler — but the click handler checks e.target.closest('a') — target is rowhead, fine.

Wait — 'stored' toggle button label: initial "show as stored"; after switching to stored, label should become "show as printed". My code sets btn.textContent based on cur — if cur was 'stored' (meaning currently stored), new mode 'short', label 'show as stored'? Let me redo: cur = current mode; new mode = cur==='stored' ? 'short' : 'stored'; label = newMode==='stored' ? 'show as printed' : 'show as stored'. Fix in code.

showContext:
```js
function showContext(art, rec, dir){
  const same = R.filter(x=>x.title===rec.r.title).sort((a,b)=>(a.paragraph-b.paragraph));
  const i = same.findIndex(x=>x.id===rec.id);
  const nb = same[i+(dir==='prev'?-1:1)];
  const ctx=art.querySelector('.ctx');
  ctx.hidden=false;
  if(!nb){ ctx.innerHTML='<span>No '+(dir==='prev'?'previous':'next')+' paragraph in this document.</span>'; return; }
  const nrec=byId[nb.id];
  ctx.innerHTML='<span class="pin">'+esc(nrec.pin)+'</span> '+esc(nrec.shown);
}
```

copyText:
```js
async function copyText(str){
  try{
    await navigator.clipboard.writeText(str);
    live('Copied: '+str);
  }catch(err){
    const box=$('#copybox'); $('#copyarea').value=str; box.hidden=false;
    live('Clipboard refused — the text is in the box below; select and copy it.');
  }
}
function live(msg){ const el=$('#live'); el.textContent=msg; }
```
#live always visible? It's a status bar at bottom — always present but empty. Fine, aria-live polite.

quoteStr:
```js
function quoteStr(rec){
  let t=rec.shown;
  if(rec.lead!=null && rec.lead===rec.r.paragraph) t=t.replace(/^\d{1,3}\.\s/,'');
  return '\u201c'+t+'\u201d '+rec.citation;
}
```

Draft:
```js
let draft=[];
let storageOK=false;
try{ localStorage.setItem('__gc_t','1'); localStorage.removeItem('__gc_t'); storageOK=true; }catch(e){ storageOK=false; }
function loadDraft(){
  if(!storageOK) return [];
  try{ const a=JSON.parse(localStorage.getItem('gc_draft_v1')||'[]'); return Array.isArray(a)?a:[]; }catch(e){ return []; }
}
function saveDraft(){ if(storageOK){ try{ localStorage.setItem('gc_draft_v1', JSON.stringify(draft)); }catch(e){} } }
function addToDraft(rec){
  if(draft.some(d=>d.id===rec.id)){ live('Already in the draft: '+rec.citation); return; }
  let t=rec.shown;
  if(rec.lead!=null && rec.lead===rec.r.paragraph) t=t.replace(/^\d{1,3}\.\s/,'');
  draft.push({ id:rec.id, citation:rec.citation, quotation:'\u201c'+t+'\u201d '+rec.citation, quote:'\u201c'+t+'\u201d',
    symbol:rec.r.symbol, paragraph:rec.r.paragraph, pinpoint:rec.pin, committee:rec.r.committee,
    short_title:rec.r.short_title, year:rec.r.year, text_copied:t, text_as_stored:rec.text, doc_url:rec.r.doc_url||'' });
  saveDraft(); renderDraft(); live('Added to draft: '+rec.citation);
}
function renderDraft(){
  $('#tab-draft-btn').textContent = '03 DRAFT'+(draft.length?' ('+draft.length+')':'');
  const box=$('#draftlist'); box.innerHTML='';
  if(!draft.length){ box.innerHTML='<p class="hint">Nothing collected yet. On tab 02, open a paragraph and choose \u201cAdd to draft\u201d.</p>'; return; }
  draft.forEach((d,i)=>{
    const bq=document.createElement('blockquote'); bq.className='dq';
    bq.innerHTML='<p>'+esc(d.quotation)+'</p>';
    const rm=document.createElement('button'); rm.type='button'; rm.textContent='Remove';
    rm.onclick=()=>{ draft.splice(i,1); saveDraft(); renderDraft(); live('Removed: '+d.citation); };
    bq.appendChild(rm); box.appendChild(bq);
  });
}
```
Tab button label: I need stable reference; give the draft tab button an id and a span for label. Simpler: set textContent fully: '03 DRAFT (4)'. But mono uppercase via CSS text-transform — fine.

Copy all:
```js
$('#copyall').onclick=()=>{ copyText(draft.map(d=>d.quote+'\n'+d.citation).join('\n\n')); };
```
Downloads:
```js
function download(name, content, mime){
  const blob=new Blob([content],{type:mime});
  const a=document.createElement('a'); a.href=URL.createObjectURL(blob); a.download=name;
  document.body.appendChild(a); a.click(); a.remove();
  setTimeout(()=>URL.revokeObjectURL(a.href),2000);
}
$('#dlTxt').onclick=()=>{ download('gc-quotations.txt', draft.map(d=>d.quote+'\n'+d.citation).join('\n\n')+'\n', 'text/plain;charset=utf-8'); live('Downloaded gc-quotations.txt ('+draft.length+' quotations)'); };
$('#dlCsv').onclick=()=>{
  const head=['citation','symbol','paragraph','pinpoint','committee','short_title','year','text_copied','text_as_stored','doc_url'];
  const rows=draft.map(d=>[d.citation,d.symbol,d.paragraph,d.pinpoint,d.committee,d.short_title,d.year,d.text_copied,d.text_as_stored,d.doc_url].map(f=>'"'+String(f==null?'':f).replace(/"/g,'""')+'"').join(','));
  download('gc-quotations.csv','\uFEFF'+head.join(',')+','+'\n'+rows.join('\n')+'\n','text/csv;charset=utf-8');
  live('Downloaded gc-quotations.csv ('+draft.length+' rows)');
};
```
Head join: head.map(f=>'"'+f+'"').join(','). Fix.

Chart:
```js
let chart=null;
function renderChart(){
  const labels = Object.keys(committeeCounts).sort((a,b)=>committeeCounts[b]-committeeCounts[a] || a.localeCompare(b));
  const data = labels.map(l=>committeeCounts[l]);
  const canvas=$('#chart');
  const aria = 'Bar chart, paragraphs per committee among the '+hits.length+' matching paragraphs: '+labels.map((l,i)=>l+' '+data[i]).join(', ')+'.';
  canvas.setAttribute('aria-label', aria);
  const wrap=canvas.parentElement;
  wrap.style.height=(labels.length*26+56)+'px';
  if(chart) chart.destroy();
  chart=new Chart(canvas.getContext('2d'),{
    type:'bar',
    data:{labels, datasets:[{data, backgroundColor:'#9b2335', borderWidth:0, categoryPercentage:0.85, barPercentage:0.9}]},
    options:{
      indexAxis:'y', responsive:true, maintainAspectRatio:false,
      onClick(e){
        const pts=chart.getElementsAtEventForMode(e,'nearest',{intersect:true},true);
        if(pts.length){ const l=chart.data.labels[pts[0].index]; tickOnly(l); }
      },
      scales:{
        x:{beginAtZero:true, maxTicksLimit:10, grid:{color:'#d9d2c3'}, ticks:{color:'#1d1b18', font:{family:'ui-monospace,Menlo,Consolas,monospace', size:11}, precision:0}},
        y:{grid:{display:false}, ticks:{color:'#1d1b18', font:{family:'ui-monospace,Menlo,Consolas,monospace', size:12}}}
      },
      plugins:{legend:{display:false}, tooltip:{callbacks:{label:c=>' '+c.parsed.x+' paragraphs'}}}
    },
    plugins:[{ id:'vals', afterDatasetsDraw(ch){
      const {ctx}=ch; ctx.save();
      ctx.font='11px ui-monospace, Menlo, Consolas, monospace'; ctx.fillStyle='#1d1b18';
      ch.data.datasets[0].data.forEach((v,i)=>{
        const m=ch.getDatasetMeta(0).data[i]; if(!m) return;
        ctx.fillText(fmt(v), m.x+6, m.y+4);
      });
      ctx.restore();
    }}]
  });
  // table
  const tb=$('#figtable tbody'); tb.innerHTML='';
  labels.forEach((l,i)=>{
    const tr=document.createElement('tr');
    tr.innerHTML='<td>'+esc(l)+'</td><td class="num">'+fmt(data[i])+'</td>';
    tb.appendChild(tr);
  });
}
function tickOnly(c){
  ticked=new Set([c]);
  $$('#committees input').forEach(cb=>{ cb.checked = cb.dataset.c===c; });
  applyFilters();
}
```
Note: chart only meaningful on overview tab; render anyway (canvas hidden in other tab — Chart.js with responsive in hidden container may size 0; when tab shown, need chart.resize(). I'll call chart.resize() when activating overview tab. Or render chart only when overview active, and re-render on activation. Simpler: in activateTab, if overview and chart → chart.resize(). Also initial render happens while overview is the active tab (default), fine.

Checks:
```js
function renderChecks(){
  const box=$('#checklist'); box.innerHTML='';
  const out=[];
  // 1 query
  if(parseError) out.push({ok:false,t:'Query understood',d:parseError.msg+' — no results are shown until the query is fixed.'});
  else if(tree) out.push({ok:true,t:'Query understood',d:'\u201c'+$('#q').value+'\u201d \u2192 '+echoStr+' \u00b7 '+termCount+' term(s)'});
  else out.push({ok:true,t:'Query understood',d:'no search words \u2014 every paragraph that passes the filters is listed'});
  // 2 totals
  const jointExtra=hits.filter(h=>h.joint).length;
  const cbSum=Object.values(committeeCounts).reduce((a,b)=>a+b,0);
  const rendered=Math.min(shown,hits.length);
  const ids=new Set(hits.slice(0,rendered).map(h=>h.id));
  out.push({ok: rendered===hits.length? true : ids.size===rendered, t:'Totals', d:'rows listed across pages: '+rendered+' of '+hits.length+' hits, no duplicates; committee checkbox counts sum to '+fmt(cbSum)+' = '+fmt(hits.length)+' hits + '+jointExtra+' joint'});
```
Hmm that ok logic is weird. Let me make it: ok = (ids.size===rendered) && (cbSum===hits.length+jointExtra). Detail as above. Good.

```js
  // 3 chart
  out.push({ok: cbSum===hits.length+jointExtra, t:'Chart total (FIG.01)', d:'the bars sum to '+fmt(cbSum)+' = '+fmt(hits.length)+' hits + '+jointExtra+' joint hits (joint General Comments count under both committees)'});
  // 4 highlight
  if(!posTerms.length) out.push({ok:true,t:'Highlight',d:'NOT-only query \u2014 nothing is highlighted, by design'});
  else{
    const re=new RegExp(posTerms.map(t=>'('+t.rawRe.source+')').join('|'),'giu');
    const noMark=hits.filter(h=>{ re.lastIndex=0; return !re.test(h.text); });
    out.push(noMark.length? {ok:false,t:'Highlight',d:noMark.length+' hit(s) matched in the normalised text but show no <mark>: '+noMark.slice(0,5).map(h=>h.citation).join('; ')+' \u2014 still shown'} : {ok:true,t:'Highlight',d:'all '+fmt(hits.length)+' hits show at least one <mark>'});
  }
  // 5 normalisation
  const q=$('#q').value;
  if(/["'\-]/.test(q)){
    const curly=hits.filter(h=>/[\u201c\u201d\u2018\u2019\u2013\u2014]/.test(h.text)).length;
    out.push({ok:true,t:'Normalisation',d:'the query holds a straight quote, apostrophe or hyphen; curly quotes, apostrophes and en/em dashes were folded to match \u2014 '+curly+' of '+fmt(hits.length)+' hits contain those forms'});
  } else out.push({ok:true,t:'Normalisation',d:'no quote, apostrophe or hyphen in the query; normalisation was still applied to every record at load'});
  // 6 numbering
  const mism=hits.filter(h=>h.lead!=null && h.lead!==h.r.paragraph);
  const dup=hits.filter(h=>h.dupPin);
  const lett=hits.filter(h=>h.letter);
  out.push({ok:true,t:'Numbering',d: mism.length+' leading-number mismatch(es) '+mism.slice(0,3).map(h=>'\u2018'+h.leadText+'\u2019 vs '+h.pin+' ('+h.r.symbol+')').join('; ')+'; '+dup.length+' duplicated pinpoint(s); '+lett.length+' lettered sub-paragraph(s) \u2014 flagged on their rows, none dropped'});
  // 7 marks
  let bad=0, ex=[];
  hits.forEach(h=>{ if(h.shown!==h.text.replace(FNG,'') || h.marks!==(h.text.match(FNC)||[]).length){ bad++; if(ex.length<3) ex.push(h.citation); } });
  out.push(bad? {ok:false,t:'Footnote marks',d:bad+' hit(s) failed the mark check: '+ex.join('; ')} : {ok:true,t:'Footnote marks',d:'for all '+fmt(hits.length)+' hits, removing [[fn:N]] reproduces the shown text exactly; '+fmt(hits.reduce((a,h)=>a+h.marks,0))+' marks removed in total'});
  // 8 draft
  let dbad=0, dex=[];
  draft.forEach(d=>{ const rec=byId[d.id]; if(!rec || rec.text!==d.text_as_stored){ dbad++; dex.push(d.citation); } });
  out.push(dbad? {ok:false,t:'Draft',d:dbad+' draft item(s) differ from the stored text: '+dex.join('; ')} : {ok:true,t:'Draft',d:'all '+draft.length+' draft item(s) match the stored text of their record'});
  // render
  out.forEach(c=>{
    const div=document.createElement('div'); div.className='checkline';
    div.innerHTML='<span class="st '+(c.ok?'pass':'fail')+'">'+(c.ok?'pass':'check failed')+'</span><span><strong>'+esc(c.t)+'.</strong> '+esc(c.d)+'</span>';
    box.appendChild(div);
  });
  const fails=out.filter(c=>!c.ok).length;
  const dot=$('#checkdot .dot'); dot.className='dot '+(fails?'bad':'ok');
  $('#checktxt').textContent = fails? fails+' checks failed' : out.length+' checks pass';
  $('#tab-checks-btn').classList.toggle('hasfail', fails>0);
}
```
.tabdot on tab 04: `<span class="tabdot" hidden>●</span>` shown when fails. I'll add span in tab 04 button, toggle hidden.

Known quirks:
```js
function renderQuirks(){
  const box=$('#quirks'); box.innerHTML='';
  const q0=R.filter(r=>r.paragraph===0);
  const shared=[...sharedSymbols];
  const jointSyms=[...new Set(R.filter(r=>symCodes(r).length>1).map(r=>r.symbol))];
  const dupKeys=[...pinCount].filter(([k,v])=>v>1);
  const mism=R.filter(r=>{ const m=String(r.text).match(/^(\d{1,3})\.\s/); return m && parseInt(m[1],10)!==r.paragraph; });
  const items=[
    ['Preambles cited as \u201cpreamble\u201d (paragraph 0)', q0.length, q0.length? q0[0].symbol : ''],
    ['Symbols shared by several General Comments', shared.length, shared.length? shared[0] : ''],
    ['Joint General Comments (two symbols in one field)', jointSyms.length, jointSyms.length? jointSyms[0] : ''],
    ['Duplicated pinpoints (same document and paragraph)', dupKeys.length, dupKeys.length? dupKeys[0][0].split('|')[0]+', '+dupKeys[0][0].split('|')[1] : ''],
    ['Leading number differs from the paragraph field', mism.length, mism.length? mism[0].symbol+', text begins \u2018'+String(mism[0].text).match(/^(\d{1,3})\./)[1]+'.\u2019, record is para. '+mism[0].paragraph : '']
  ];
  items.forEach(([t,n,ex])=>{
    const div=document.createElement('div'); div.className='quirk';
    div.innerHTML='<span class="n">'+fmt(n)+'</span>'+esc(t)+(ex?' \u2014 e.g. '+esc(ex):'');
    box.appendChild(div);
  });
}
```
pinCount keyed by title+'|'+pin — example display: title is long; use symbol? key has title not symbol. I'll store example as the first record's citation. Let me build dup examples from records: map key→first rec. Simpler: compute in precompute: dupExamples map key→citation. I'll do that.

Method section: static HTML.

Tabs:
```js
const TABS=[['overview','01 OVERVIEW'],['paragraphs','02 PARAGRAPHS'],['draft','03 DRAFT'],['checks','04 CHECK & METHOD']];
function activateTab(name){
  $$('#tabs button').forEach(b=>{
    const on=b.dataset.tab===name;
    b.setAttribute('aria-selected', on?'true':'false');
    $('#panel-'+b.dataset.tab).hidden=!on;
  });
  $('#rail').hidden = (name==='draft');
  if(name==='overview' && chart) chart.resize();
}
```
Panels: `<div id="panel-overview" role="tabpanel" ...>`.

Tab buttons HTML:
```html
<nav id="tabs" role="tablist" aria-label="Views">
  <button role="tab" id="tab-overview-btn" data-tab="overview" aria-selected="true" aria-controls="panel-overview">01 Overview</button>
  <button role="tab" id="tab-paragraphs-btn" data-tab="paragraphs" aria-selected="false" aria-controls="panel-paragraphs">02 Paragraphs</button>
  <button role="tab" id="tab-draft-btn" data-tab="draft" aria-selected="false" aria-controls="panel-draft">03 Draft</button>
  <button role="tab" id="tab-checks-btn" data-tab="checks" aria-selected="false" aria-controls="panel-checks">04 Check &amp; method <span class="tabdot" hidden>●</span></button>
</nav>
```
CSS uppercase transforms. tabdot red.

Tab click + arrow keys:
```js
$('#tabs').addEventListener('click', e=>{ const b=e.target.closest('button[data-tab]'); if(b) activateTab(b.dataset.tab); });
$('#tabs').addEventListener('keydown', e=>{
  if(e.key!=='ArrowRight'&&e.key!=='ArrowLeft') return;
  const btns=$$('#tabs button'); const i=btns.indexOf(document.activeElement);
  if(i<0) return; e.preventDefault();
  const n=(i+(e.key==='ArrowRight'?1:-1)+btns.length)%btns.length;
  btns[n].focus(); activateTab(btns[n].dataset.tab);
});
```

Search wiring:
```js
$('#go').addEventListener('click', ()=>{ searched=true; $('#syntax').hidden=true; applyFilters(); });
$('#q').addEventListener('keydown', e=>{ if(e.key==='Enter'){ searched=true; $('#syntax').hidden=true; applyFilters(); } });
$('#q').addEventListener('focus', ()=>{ if(!$('#q').value) $('#syntax').hidden=false; });
$('#q').addEventListener('input', ()=>{ $('#syntax').hidden=true; });
$('#q').addEventListener('blur', ()=>{ setTimeout(()=>{ $('#syntax').hidden=true; },150); });
$$('#syntax .ex').forEach(b=> b.addEventListener('mousedown', e=>{ e.preventDefault(); $('#q').value=b.dataset.q; searched=true; $('#syntax').hidden=true; applyFilters(); }));
```
Examples as buttons with data-q.

Years inputs:
```js
$('#yfrom').addEventListener('change', ()=>applyFilters());
$('#yto').addEventListener('change', ()=>applyFilters());
```
Set values at init: minY, maxY.

Doc select build:
```js
function buildDocSelect(){
  const sel=$('#docsel');
  sel.innerHTML='<option value="">All documents</option>';
  const byComm={};
  R.forEach(r=>{ (byComm[r.committee]=byComm[r.committee]||new Map()).set(r.title, r.short_title); });
  comms.forEach(c=>{
    const g=document.createElement('optgroup'); g.label=c+' — '+(COMMITTEE_NAMES[c]||c);
    const m=byComm[c]; if(!m) return;
    [...m.keys()].sort().forEach(t=>{
      const o=document.createElement('option'); o.value=t; o.textContent=m.get(t)||t; g.appendChild(o);
    });
    sel.appendChild(g);
  });
  sel.addEventListener('change', ()=>applyFilters());
}
```

Clear all:
```js
$('#clearall').addEventListener('click', ()=>{
  ticked=new Set(comms);
  $$('#committees input').forEach(cb=>cb.checked=true);
  $('#yfrom').value=minY; $('#yto').value=maxY; $('#docsel').value='';
  applyFilters();
});
```

Filter heading toggle:
```js
$('#fhead').addEventListener('click', ()=>{
  const open=$('#fhead').getAttribute('aria-expanded')==='true';
  $('#fhead').setAttribute('aria-expanded', String(!open));
  $('#fbody').hidden=open;
});
```

Order select:
```js
$('#order').addEventListener('change', ()=>{ order=$('#order').value; sortHits(); shown=25; renderResults(); renderSummary(); renderChecks(); });
```
Hmm renderChecks uses shown — fine. But renderResults resets openRows? openRows persists across re-render (Set) — rows re-created with actions visible if in openRows. rowState persists too. OK.

"Show more":
```js
$('#more').addEventListener('click', ()=>{
  shown+=25;
  const box=$('#results');
  const start=box.children.length;
  for(let i=start;i<Math.min(shown,hits.length);i++) box.appendChild(rowEl(hits[i]));
  if(shown>=hits.length) $('#more').hidden=true; else $('#more').hidden=false;
  renderChecks();
});
```

Init:
```js
buildCommitteeList(); buildDocSelect();
$('#yfrom').value=minY; $('#yto').value=maxY;
renderQuirks();
draft=loadDraft(); renderDraft();
applyFilters();
$('#q').focus();
```
applyFilters calls renderAll which includes renderChart — chart on overview (default active). Good.

Header meta:
```js
$('#meta').innerHTML = fmt(R.length)+' paragraphs from '+titles.size+' General Comments (distinct title) of '+comms.length+' committees, '+minY+'\u2013'+maxY+' \u00b7 '+(D.source_url? '<a href="'+esc(D.source_url)+'" target="_blank" rel="noopener">'+esc(D.source||'source')+'</a>' : esc(D.source||''));
```
Footer:
```js
$('#foot').innerHTML = esc(D.source||'')+(D.built? ' \u00b7 built '+esc(D.built):'')+' \u00b7 counting, matching and sorting are done by this page\u2019s code; no model is called and nothing leaves the browser.<br>Credits: Chart.js 4 (MIT) renders FIG.01. Search syntax follows the conventions of Wikipedia \u201cHelp:Searching\u201d (CC BY-SA 4.0); the help text here is written fresh.';
```

Wait — footer should be static-ish; I'll build in JS since source/built from data. Or put spans. JS fine.

Overview panel HTML:
```html
<div id="panel-overview" class="panel" role="tabpanel" aria-labelledby="tab-overview-btn">
  <h2 class="fig">FIG.01 Paragraphs per committee</h2>
  <p class="hint">click a bar = tick that committee alone \u00b7 joint General Comments count under both committees, so the bars can add up to more than the hits</p>
  <div class="figwrap">
    <div class="chartbox"><div class="canvaswrap"><canvas id="chart" role="img" aria-label="Bar chart of paragraphs per committee">Your browser cannot draw the chart; the table beside it lists the same numbers.</canvas></div></div>
    <table class="figtable" id="figtable">
      <caption>FIG.01 data — matching paragraphs per committee</caption>
      <thead><tr><th scope="col">Committee</th><th scope="col" class="num">Paragraphs</th></tr></thead>
      <tbody></tbody>
    </table>
  </div>
  <p class="how">How this is computed: one count per committee over the paragraphs that match the query and filters; a record with two committees (a joint General Comment) is counted under both.</p>
</div>
```

Paragraphs panel:
```html
<div id="panel-paragraphs" class="panel" role="tabpanel" aria-labelledby="tab-paragraphs-btn" hidden>
  <p class="summary" id="summary" aria-live="polite"></p>
  <div class="orderline">
    <span class="desc" id="orderdesc"></span>
    <label class="mono" for="order">ORDER</label>
    <select id="order">
      <option value="year">Year, newest first</option>
      <option value="doc">Document order</option>
      <option value="match">Most matches first</option>
    </select>
  </div>
  <p class="hint">This page retrieves; it never writes. Every paragraph shown is a record of the file, as stored.</p>
  <div id="results"></div>
  <button id="more" type="button">Show 25 more</button>
</div>
```

Draft panel:
```html
<div id="panel-draft" class="panel" role="tabpanel" aria-labelledby="tab-draft-btn" hidden>
  <h2 class="fig">Your draft (<span id="dcount">0</span> quotations)</h2>
  <div class="draftbtns">
    <button id="copyall" type="button">Copy all</button>
    <button id="dlTxt" type="button">Download .txt</button>
    <button id="dlCsv" type="button">Download .csv</button>
  </div>
  <p class="hint">Kept in localStorage when the browser allows it, in memory otherwise (this session only). Copy all = quotation, new line, citation, blank line between items.</p>
  <div id="draftlist"></div>
</div>
```
dcount update in renderDraft.

Checks panel:
```html
<div id="panel-checks" class="panel" role="tabpanel" aria-labelledby="tab-checks-btn" hidden>
  <h3 class="sec">How the app checks itself</h3>
  <p class="hint">Re-run after every search. A failed check marks rows; it never drops them.</p>
  <div id="checklist"></div>
  <h3 class="sec">Known quirks of this file</h3>
  <p class="hint">Computed at load, before any search.</p>
  <div id="quirks"></div>
  <h3 class="sec">How this is computed</h3>
  <div class="method">
    <p><strong>Load.</strong> One pass over all records. Per record: the normalised text, the shown text (footnote marks removed), the mark count, the leading number, the pinpoint, the citation, and the committees found in the symbol plus the committee field.</p>
    <p><strong>Normalisation.</strong> <code>[[fn:N]]</code> marks are skipped; curly and straight quotes and apostrophes, en/em dashes, hyphens and non-breaking spaces are folded to one form; everything is lower-cased. The query is normalised the same way, so curly quotes pasted from Word still match.</p>
    <p><strong>Query.</strong> Tokens: a phrase in double quotes (straight or curly), parentheses, AND / OR / NOT in capitals, a leading minus as NOT, any other run of characters as a word with an optional trailing star. Adjacent terms are joined by AND; precedence NOT, then AND, then OR; parentheses override. A word becomes a regular expression over the normalised text with letter/number boundaries, so \u201cstate\u201d also matches \u201cnon-State\u201d; a star allows any ending (<code>child*</code> finds <em>children</em>).</p>
    <p><strong>Matching.</strong> The Boolean tree is evaluated over the normalised text of every record; the committee, year and document filters are applied after. Sorting: year descending, then title, then paragraph (the select swaps the comparator; the hit set does not change).</p>
    <p><strong>Citation and quotation.</strong> Assembled only from the record's own fields — symbol, paragraph, title, committee, doc_url — never invented. Preambles are cited as \u201cpreamble\u201d, lettered sub-paragraphs as \u201csubpara. (b)\u201d, shared symbols carry the committee and the document's name first. When the text begins with its own number and that number equals the paragraph field, the copied quotation drops the leading \u201c12. \u201d because the citation carries it; the shown text keeps it.</p>
    <p><strong>Honesty.</strong> This page retrieves; it never generates. No model is called and nothing leaves the browser. Counting, filtering, sorting and matching are done by this page's code, deterministically.</p>
  </div>
</div>
```
code styling: `code{font-family:ui-monospace,monospace;font-size:13px;background:#ece7db;padding:0 3px}`.

Rail HTML:
```html
<aside id="rail" aria-label="Filters">
  <div class="railhead"><span class="mono">Filters</span><button id="clearall" type="button" class="linkbtn">Clear all</button></div>
  <div class="bignum" id="bignum" aria-live="polite">0</div>
  <div class="of" id="of"></div>
  <div id="chips"></div>
  <div class="searchwrap">
    <label class="mono" for="q" style="display:block;margin-bottom:6px">Search the paragraphs</label>
    <input id="q" type="text" autocomplete="off" spellcheck="false" aria-describedby="querynorm">
    <button id="go" type="button">Search</button>
    <div id="syntax" hidden>
      <ul>
        <li>a space or <b>AND</b> joins words; <b>OR</b>; <b>NOT</b> or a leading minus</li>
        <li>\u201can exact phrase\u201d in double quotes; parentheses; a star at the end of a word for any ending (<code>child*</code> finds <em>children</em>)</li>
        <li>operators in capitals — lower-case \u201cor\u201d is a word</li>
      </ul>
      <button type="button" class="ex" data-q='"best interests" AND child'>\u201cbest interests\u201d AND child</button>
      <button type="button" class="ex" data-q='(torture OR ill-treatment) NOT detention'>(torture OR ill-treatment) NOT detention</button>
      <button type="button" class="ex" data-q='"reasonable accommodation'>\u201creasonable accommodation\u201d</button>
    </div>
  </div>
  <p class="hint" id="querynorm">Whole words, any case. Curly and straight quotes, apostrophes, dashes and hyphens count as the same, and footnote marks are skipped, so State's finds State\u2019s and a phrase can cross a footnote.</p>
  <p id="echo" aria-live="polite"></p>
  <div class="fgroup">
    <button type="button" class="fhead" id="fhead" aria-expanded="false" aria-controls="fbody">
      <span class="mono">01 Committee, years, document</span><span aria-hidden="true">\u25b8</span>
    </button>
    <div class="fbody" id="fbody" hidden>
      <div class="fsub mono">Committee <button type="button" id="allc">all</button> / <button type="button" id="nonec">none</button></div>
      <div id="committees"></div>
      <div class="fsub mono">Years</div>
      <div class="years"><input id="yfrom" type="number" aria-label="from year"> \u2013 <input id="yto" type="number" aria-label="to year"></div>
      <div class="fsub mono">Document</div>
      <select id="docsel"></select>
    </div>
  </div>
</aside>
```
Note: in HTML I must write actual characters or entities — I'll write literal curly quotes in the file (UTF-8). Fine.

all/none:
```js
$('#allc').onclick=()=>{ ticked=new Set(comms); $$('#committees input').forEach(cb=>cb.checked=true); applyFilters(); };
$('#nonec').onclick=()=>{ ticked=new Set(); $$('#committees input').forEach(cb=>cb.checked=false); applyFilters(); };
```

Committee label content: `<input type=checkbox data-c=CERD checked><span class="ccode mono">CERD</span><span class="cname">Committee on…</span><span class="cnt" data-c=CERD></span>`. CSS: #committees .ccode{flex:0 0 52px}.

Now — one concern: applyFilters reads $('#q').value etc. Fine.

Also initial applyFilters: searched=false → echo empty, counts no brackets. Good.

renderCommCounts must also sync checkbox checked with ticked (after tickOnly/clearall we set manually; but applyFilters→renderCommCounts can sync): 
```js
$$('#committees input').forEach(cb=>{ cb.checked=ticked.has(cb.dataset.c); });
```

Now the header checks element:
```html
<div class="checks"><span class="dot ok" id="checkdot"></span><span id="checktxt">…</span></div>
```
I referenced $('#checkdot .dot') — adjust: give dot id="checkdot". 

Also tab 04 red dot: `#tab-checks-btn .tabdot` toggle hidden = fails===0.

Edge: `hits.flatMap` — fine modern browsers.

One more: the plan says results summary "279 of 7,304 paragraphs match · 8 committees · 1990–2023" — committees among hits: count distinct committees across hits (using rec.committees). OK.

Also "then the order: 'sorted by year, newest first, then by document and paragraph'; a select beside it" — done.

Potential issue: Chart.js v4 `getElementsAtEventForMode` exists. OK.

Canvas fallback content: text inside <canvas> shows only if canvas unsupported. Good.

Now — the "search box has focus on load" plus syntax dropdown opens. Good.

Let me also double check the highlight combined regex: posTerms rawRe sources contain groups? rawCore has non-capturing groups only — `(?:...)`. escRe escapes parens in words. So wrapping in '('+source+')' is safe.

One subtlety: rawRe flags 'giu' — when embedding source into new RegExp with 'giu', fine.

Another: term.re (norm) built with flag 'u' only — norm is lowercase; query words normalized lowercase. Case-insensitive not needed. But wait — norm lowercases, and words lowercased — ok.

Wildcard in norm regex: `child\w*` with 'u' flag — \w fine.

Boundaries with lookbehind `(?<![\p{L}\p{N}])` — supported in modern browsers. OK.

Now the cutRaw regex `/\[\[fn:\d+\]\]|[\s\S]/gu` — alternation order: fn mark first. Good.

Also — "Paragraphs up to 700 characters are shown whole" — shown length ≤700 → full. My condition: long = shown.length>700. Good.

Let me also handle doc_url empty in row: guard done.

Now assemble everything. Also add `#live` div and `#copybox` at end of body.

Also the "grey" class: `.grey{color:var(--grey);font-size:12px}`.

Let me also make sure the tab buttons have type="button".

Potential CSS conflict: `#tabs button` styles vs `.chip` etc. fine.

Let me now also handle: when parseError, renderResults shows empty + maybe message. I'll add: if parseError, results box shows a red line. In renderResults: if(parseError){ box.innerHTML='<p class="rnote">'+esc(parseError.msg)+'</p>'; more.hidden=true; return; }

Also summary when parseError: '0 results — fix the query.' I'll set summary text accordingly.

Also bignum shows 0. OK.

Now, the checks "Totals" when parseError: hits=[] → cbSum=0=0+0 ok. Fine.

Write final HTML. Also include `<meta name="color-scheme" content="light">`? Not needed.

Let me be careful with template literals inside the script containing `</` sequences? No `</script>` inside strings. The innerHTML strings contain `</span>` etc — fine, only `</script>` is problematic.

Also careful: in rowEl innerHTML I use string concatenation with quotes — fine.

One more plan item: "After every copy an aria-live message shows the exact string sent." — live('Copied: '+str) does that.

"Copy uses navigator.clipboard.writeText; if refused, the text goes into a selectable box with 'Select and copy'." — copybox has label "CLIPBOARD REFUSED — SELECT AND COPY" and textarea. Add a close button? Add small "Close" button. OK.

Draft CSV header: `head.map(f=>'"'+f+'"').join(',')`.

Also plan: Draft tab clickable count 7 — fine.

Now, about `renderChart` being called when overview hidden (e.g., after search while on paragraphs tab): Chart.js creating chart in hidden canvas (display:none via [hidden]) — width 0. When switching to overview, activateTab calls chart.resize() — but if canvas was display:none at creation, chart may have 0 size; resize after unhide should fix since responsive. To be safer: in activateTab, if overview: renderChart() again (rebuild). Rebuilding each activation is cheap (≤10 bars). I'll call renderChart() on overview activation instead of resize. But renderChart is also called in renderAll — double render fine (destroy first).

Actually careful: renderAll→renderChart while overview hidden creates chart with 0 size; then activateTab('overview')→renderChart() rebuilds with correct size. OK.

Also initial load: overview visible → fine.

Let me now also compute `titles` set and `comms` — comms from r.committee distinct sorted.

Edge: committee field might be like "CAT-OP" — included in COMMITTEE_NAMES.

Now write out the whole file. I'll aim for clarity and completeness. Let me also double-check the parser handles `"best interests" AND child`: tokens PHRASE, AND, WORD → parseOr→parseAnd: parseNot→primary PHRASE; loop: peek AND → consume, parseNot→WORD → and. Good. `(torture OR ill-treatment) NOT detention`: LP → parseOr inside: WORD torture, OR, WORD ill-treatment → or; RP; back in parseAnd: peek NOT → isTermStart true → parseNot consumes NOT → not(detention) → and. Good. `-torture`: NOTW. `child*`: WORD with word 'child*' → makeTerm strips star → wildcard. Good. Lowercase 'or': WORD 'or' → term matching word "or". Good.

Echo for phrase: display = raw inner (original case) — 'the phrase “best interests”'. Good.

One thing: makeTerm for NOTW passes rawWord without the minus; display shows without minus — echo "without the word torture". Good.

Empty query: tree=null → all pass filters. searched flag: after user clicks Search with empty box — searched=true, echo "No search words — ...". Good.

Now — "While the box is empty and has focus, a short list opens under it" — implemented.

Also plan: "it closes when typing starts" — input event hides. Good.

Let me write the final answer now. Before the code block: 2-3 short sentences describing what I built.

Also check: "Every row that shows a document has its symbol, linked to doc_url in a new tab." — done in rowhead.

Let me make sure I don't exceed ~1500 lines — should be around 800-900.

One more detail: the plan says the rail is hidden on Draft tab — `$('#rail').hidden = name==='draft'`. With [hidden]{display:none!important} rule. Good.

Also add `aria-live="polite"` to #live.

Writing the code now. I'll be meticulous about matching IDs between HTML and JS.

IDs: meta, checkdot, checktxt, tabs, rail, bignum, of, chips, q, go, syntax, querynorm, echo, fhead, fbody, committees, allc, nonec, yfrom, yto, docsel, clearall, panel-overview/paragraphs/draft/checks, chart, figtable (tbody), summary, orderdesc, order, results, more, dcount, draftlist, copyall, dlTxt, dlCsv, checklist, quirks, live, copybox, copyarea, copyclose.

Tab buttons: data-tab attributes; ids tab-overview-btn etc. For draft label update: `$('#tab-draft-btn').firstChild.textContent`? Simpler: wrap label in span: `<span class="tlabel">03 Draft</span>` and update span. I'll do: tab-draft-btn contains `<span id="draftlabel">03 Draft</span>`. Update `$('#draftlabel').textContent='03 Draft'+(n?' ('+n+')':'')`. CSS uppercase handles caps.

Checks tab dot: `<span class="tabdot" id="checktabdot" hidden>●</span>`.

Now, in renderChecks I referenced $('#tab-checks-btn') — use $('#checktabdot').hidden = fails===0.

Also header checktxt initial before first applyFilters — applyFilters runs at init, so fine.

Let me also handle `renderSummary` when parseError: summary = 'Fix the query — no results.' and orderdesc still set.

Also in applyFilters, when parseError, we should still render chips etc. Fine.

Potential bug: in applyFilters I compute yFrom/yTo from inputs each time; chips compare to minY/maxY. Good.

docSel compare: `if(docSel && rec.r.title!==docSel) continue;` — docSel is title value. Good.

Now write it all.

For the syntax dropdown examples, data-q attributes contain double quotes — in HTML attribute use single quotes: data-q='"best interests" AND child'. Good.

Also the `#syntax` positioning: .searchwrap relative; #syntax absolute top:100% — but the Search button is below input inside searchwrap, so dropdown overlaps button. Put dropdown after button; top:100% of searchwrap → below button. Fine.

Let me also ensure the input row: input full width, button below. OK.

Final check on "How this is computed" line near chart — present.

Also plan wants on tab 02: "one monospace hint: 'This page retrieves; it never writes...'" — present as .hint with mono? Make it class "hint mono"? mono is uppercase 11px — the sentence would be uppercase, ugly. Plan says "one monospace hint" — I'll use a smaller mono-styled line but not uppercase: create class .hintmono {font-family:ui-monospace...; font-size:11px; letter-spacing:.08em; text-transform:none; color:var(--grey)}. Use for that line and maybe others. Actually simpler: keep .hint for readability; but plan explicitly says monospace hint. I'll add .mono2 class (monospace, 11px, no uppercase). Use for that line and the "click a bar" hint? The chart hint can stay .hint. I'll use mono2 for the retrieves line.

OK, writing final output now.

Also — the footer must include source and built; if D.built undefined, skip gracefully.

Let me write the complete file.

Additional check — `renderResults` uses `rowEl` which uses `openRows` and `rowState`; after applyFilters, openRows may contain ids not in hits — harmless.

In rowEl, actions hidden attr: `'<div class="actions"'+(openRows.has(rec.id)?'':' hidden')+'>'`.

Delegation keydown: e.target may be the rowhead div. OK.

Also stop rowhead toggle when clicking the "show as stored"/"full" buttons — those are in .rtext, not rowhead, so no conflict.

But clicking symbol link inside rowhead: guard `!e.target.closest('a')`. Good.

Now — one more consideration about performance of evalTree over 7304 records with regex tests: each term regex test on ~500-char strings — fast enough.

Writing now. I'll count roughly: CSS ~200 lines, HTML ~120, JS ~450. Good.

For the intro text before code: "I built the verbatim finder on WORKSHOP_DATA.gc: Boolean + phrase search over all paragraphs, four tabs (overview chart, paged results with highlight and copy-ready citations, a draft collector, and self-checks), filters in the left rail. Everything is computed in the page from the records; no model is called." — 2 sentences. Good.