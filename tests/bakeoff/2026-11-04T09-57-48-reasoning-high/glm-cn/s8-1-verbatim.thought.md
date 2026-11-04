Let me build this app carefully. It's a complex verbatim finder for General Comments. Let me plan the structure:

- Single HTML file, offline, Chart.js 4 preloaded as window.Chart.
- Data: WORKSHOP_DATA.gc = {title, source, count, records}.
- Four tabs: 01 Overview, 02 Paragraphs, 03 Draft (n), 04 Check & method.
- Header always visible with label, title, one line with stats, checks status at right.
- Left rail with filters (except on Draft tab).
- Search box with syntax help when empty and focused, examples.
- Query parser with Boolean operators, phrases, wildcards, parentheses.
- Normalisation for matching; highlight regex over shown text.
- Results list with rows, expandable, context, copy citation, copy quotation, add to draft.
- Draft tab with localStorage, copy all, download txt/csv.
- Checks tab with self-checks and known quirks.
- Footer.

Design: warm off-white #f4f0e8, near-black #1d1b18, thin rules #d9d2c3, red accent #9b2335. Serif for title/big numbers, monospace labels, sans body.

Let me write the code carefully.

Key implementation details:

1. Load: R = WORKSHOP_DATA.gc.records. Precompute per record:
   - norm: normalised text (footnote marks removed, curly → straight quotes/apostrophes, dashes → "-", whitespace → single space, lowercase)
   - marks: count of [[fn:N]]
   - leading: match ^(\d{1,3})\.\s on text
   - pinpoint
   - citation
   - shared: symbol holds more than one title
   - joint: two symbols in one symbol
   - committees: codes found in symbol + committee

2. Committees regex: /\b(CAT|CCPR|CED|CEDAW|CERD|CESCR|CMW|CRC|CRPD)\b/g on symbol, plus "CAT-OP" for CAT/OP. Note \b(CAT)\b would match "CAT-OP"? \b between T and -? "CAT-OP": after "CAT" comes "-", which is a non-word char, so \bCAT\b matches within "CAT-OP". Hmm, but the plan says codes found via that regex plus committee. The committee field is e.g. "CAT-OP". So committees = set of codes from symbol regex + committee field. Actually wait — the plan says: "A record's committees = the codes found in symbol (\b(CAT|...)\b, "CAT-OP" for CAT/OP) plus committee". So if symbol is "CAT/OP/... " hmm. Actually simpler: committees set = codes matched in symbol ∪ {committee}. The committee field is one of 10 codes: CRC, CEDAW, ... CAT-OP. So a CAT/OP record has committee "CAT-OP". Symbols like "CAT/C/... " give "CAT". Should CAT-OP appear as "CAT" too? The regex \b(CAT)\b on "CAT/OP/..." — "CAT" followed by "/" is a word boundary, so yes it matches "CAT". Hmm, that means a CAT/OP symbol record gets committees {CAT, CAT-OP}. That may be intended or not. Actually for the chart, we count by each record's committee (the field). The plan says "Hits per committee = one count per committee over the hits, by each record's committee" then "A record's committees = the codes found in symbol ... plus committee; the filter keeps a record if any is ticked, and the chart adds it to each of its committees' bars." Hmm, that seems to say chart uses committees set. But "CAT-OP" — the regex \b(CAT|...)\b — would "CAT" match in "CAT-OP"? The committee field is "CAT-OP" as a string; the regex over symbol... Let me not overthink. I'll compute committees as: matched codes in symbol (using the regex, which for "CAT/OP/..." yields "CAT"), plus the committee field value. For committee "CAT-OP", should I also add "CAT"? The plan says joint GCs count under both committees. For CAT-OP, it's a distinct committee (Subcommittee on Prevention of Torture). I'll just use the committee field plus symbol-matched codes. If committee is "CAT-OP" and symbol is "CAT/OP/...", regex gives "CAT" — hmm, that would add CAT to a Subcommittee record. Wait, does \bCAT\b match in "CAT/OP"? Yes: C-A-T followed by / is a boundary. Hmm. But actually is that wrong? The Subcommittee's symbols are like "CAT/OP/...". Hmm, matching "CAT" there could be seen as correct (it's the CAT-related machinery) or incorrect. The plan explicitly says the regex finds codes in symbol. I'll follow it but exclude "CAT" match when symbol starts with "CAT/OP"? The plan says '"CAT-OP" for CAT/OP' — meaning the code "CAT-OP" is used for CAT/OP symbols. So I think the intent: if symbol contains "CAT/OP", the code is "CAT-OP" (and not "CAT"). Let me implement: first check for CAT/OP → add "CAT-OP"; else run the regex over symbol. Plus always add committee field.

Committee full names:
- CAT: Committee against Torture
- CCPR: Human Rights Committee
- CED: Committee on the Elimination of Racial Discrimination... wait no, CED is Committee on Enforced Disappearances; CERD is racial discrimination. CED = Committee on Enforced Disappearances.
- CEDAW: Committee on the Elimination of Discrimination against Women
- CERD: Committee on the Elimination of Racial Discrimination
- CESCR: Committee on Economic, Social and Cultural Rights
- CMW: Committee on Migrant Workers... (Committee on the Protection of the Rights of All Migrant Workers and Members of Their Families)
- CRC: Committee on the Rights of the Child
- CRPD: Committee on the Rights of Persons with Disabilities
- CAT-OP: Subcommittee on Prevention of Torture (as given in the plan)

3. Search: parse query into a tree. Tokens:
   - quoted phrase: "..." (straight or curly quotes “ ”)
   - ( and )
   - AND, OR, NOT in capitals
   - leading - as NOT
   - word: run of non-space chars, trailing * allowed

Parser: precedence NOT > AND > OR; adjacent terms joined by AND. Parentheses override.

Implementation: tokenize, then recursive descent:
   - parseOr: parseAnd (OR parseAnd)*
   - parseAnd: parseNot ((AND)? parseNot)* — adjacent terms joined by AND, meaning if next token is not OR, NOT (operator), ')' or end, treat as AND.
   - parseNot: NOT? or -? then parsePrimary
   - parsePrimary: '(' parseOr ')' | phrase | word

Careful: '-' as leading minus only when at start of a word token (token starts with '-' and has more chars). A standalone hyphen word... treat as word.

Echo: build English description:
   - word → "the word X" (or "any word ending X" for star)
   - phrase → "the phrase “X”"
   - AND → "A and B"
   - OR → "A or B"
   - NOT → "not X" — hmm, "Paragraphs containing ... " Let me build echo like "Paragraphs containing the phrase “best interests” and the word child". NOT-only query matches everything that lacks the terms, echo says so.

Term match: word → regex over norm: escaped, trailing * → \w*, boundaries (?<![\p{L}\p{N}]) and (?![\p{L}\p{N}]), flag u. Hyphen is a boundary. Phrase: words joined by \s+ inside same boundaries. Note the phrase words themselves get normalised first (lowercase, quote normalisation).

Wait: the word may contain characters that need escaping. Also, the word itself could contain a hyphen: "ill-treatment" — in norm, hyphens stay as "-"? Normalisation: en dash, em dash, soft hyphen → "-". So "ill-treatment" stays "ill-treatment". In the regex, boundaries (?<![\p{L}\p{N}]) before and (?![\p{L}\p{N}]) after. So "ill-treatment" matches literally. But if the document has "ill–treatment" (en dash), norm converted to "-", so it matches. Good.

But wait, "A hyphen is a boundary, so 'state' finds 'non-State'": norm of "non-State" → "non-state". Regex for "state": (?<![\p{L}\p{N}])state(?![\p{L}\p{N}]) — in "non-state", before "state" is "-" which is not a letter/number → lookbehind passes. Good.

Phrase joined by \s+: phrase "best interests" → (?<![\p{L}\p{N}])best\s+interests(?![\p{L}\p{N}]). But what if phrase words contain hyphens? Fine.

Hmm, one subtlety: phrase regex over norm uses \s+ between words, but norm has all whitespace collapsed to single spaces, so fine.

4. Highlight: second regex over the shown text (text with footnote marks removed, but line breaks etc. kept). Quote/apostrophe matches straight and curly forms; hyphen matches hyphen, en dash, em dash; gap between phrase words matches (?:\s|\[\[fn:\d+\]\])+ — wait, but highlight is applied to shown text where footnote marks are removed... Hmm. The plan says: "The same terms become a second regular expression over the shown text, where a quote or apostrophe matches its straight and curly forms, a hyphen matches hyphen, en and em dash, and a gap between phrase words matches (?:\s|\[\[fn:\d+\]\])+". But shown text has footnote marks removed... unless the user clicked "show as stored". I'll build the highlight regex to handle both: gaps match (?:\s|\[\[fn:\d+\]\])+, so it works on stored text too. And quotes: [“”"] etc.

So highlight term regex:
- word chars escaped; quote chars in the word → [“”„"] class; apostrophe → [‘’‚']; hyphen → [-–—]; trailing * → \w*.
- boundaries same as before but case-insensitive: since shown text keeps case, add flag 'giu'? Hmm, boundaries (?<![\p{L}\p{N}]) with 'i' flag... fine. But lower-case word "child" should match "Child". Use flag 'giu'. Hmm but \w* with u flag fine.

Wait, but a word may contain uppercase — the query is normalised to lowercase for matching norm, but for highlight we keep the original query word and match case-insensitively. Good.

Actually, careful: escaping. Let me write a function hlPattern(word):
   - for each char: if char is '"' → '[“”"]'; if "'" → '[‘’\']'; if '-' → '[-–—]'; if '*' at end → '\\w*'; else escape.
   Actually '*' only trailing. Let me handle: strip trailing '*', build pattern, append '\\w*'.

For phrase: words joined by '(?:\\s|\\[\\[fn:\\d+\\]\\])+'.

Combine all positive terms into one regex with alternation for efficiency: (term1|term2|...). NOT terms excluded.

Collect terms: walk the tree, gather phrase and word nodes not under a NOT. Need to track NOT context: when descending into NOT branch, mark terms as negative (don't highlight).

5. Filters: committee checkboxes (all ticked by default), year from/to, document select. Joint GC appears when either committee ticked (naturally, since filter keeps record if any of its committees is ticked — a joint record has committees {CMW, CERD} say, so it passes if CMW or CERD ticked). Show both badges on the row.

Filter chips: committee ticks (when not all ticked — show as chip? The plan: "A narrowed filter shows as a small removable chip under the big number." So when committees are a proper subset, show a chip like "CRC, CEDAW (2 of 10)" removable → resets to all. Year chip when narrowed. Document chip when set.

Hmm, removable chips: click × to remove. Let me implement chips as small buttons with "×".

6. Hits: records matching query tree AND filters. Empty query → all pass (then filters apply). Summary says "no search words".

7. Overview tab: FIG.01 horizontal bar chart, one bar per committee, ranked, value at end of bar, axis from zero. Canvas role="img" aria-label with numbers, fallback content, small table beside. Click a bar = tick that committee alone. "How this is computed" line.

Chart: Chart.js bar, indexAxis 'y'. Value at end: use datalabels? No plugin — Chart.js 4 doesn't have datalabels preloaded. I can draw values via a custom plugin (afterDatasetsDraw) — that's inline code, fine. Or put values in ticks... Simpler: custom inline plugin to draw the value at the end of each bar. That's allowed (my own code).

Colors: one colour — the red accent #9b2335 for bars.

At most 10 committees (we have 10), light gridlines: keep x grid light, no y grid. Gaps narrower than a bar: barPercentage/categoryPercentage tweak.

Click on bar: use onClick handler on chart, get element index, map to committee, tick that committee alone in the filter, re-render.

aria-label: "Paragraphs per committee: CRC 2091, ..." stating numbers. Fallback content inside canvas element.

8. Paragraphs tab: summary line aria-live, order select, hint, results 25 per page, "Show 25 more". Rows as <article> with heading. Each row: committee badge(s), short_title, symbol linked, pinpoint (red), year. Text shown with footnote marks removed, marks highlighted; "N footnote marks removed · show as stored" link swaps. Long paragraphs: first 700 chars cut at word + "Show the full paragraph (1,287 words)" — word count. Amber notes for numbering quirks. Click row (or a button?) opens in place with three buttons + Context link. 

"Clickable: ... rows expand" — a click on a row opens it in place. So the row itself is clickable (maybe via a button for a11y — make the row header a button, or the whole article clickable with keyboard support). Let me make each row an <article> with an <h3> heading containing a <button> that toggles expansion. Clicking the article body also toggles? Plan says "A click on a row opens it in place". I'll make the whole article clickable (except links/buttons inside), toggling expansion, and also provide keyboard: the heading button.

Expanded row: three buttons (Copy citation, Copy quotation, Add to draft) and "Context: previous | next" link. Context opens paragraph −1/+1 of same title inline in grey with its own pinpoint.

Copy citation: builds citation string. When symbol shared by several titles: "CERD, General Recommendation No. 29 (A/57/18), para. 3" — committee + ", " + document's name (title up to first colon or " on ") + " (" + symbol + "), " + pinpoint. Document's name: title up to first colon or " on ". E.g. title "General Recommendation No. 29 (2002): Article 1, paragraph 1 of the Convention" → up to colon → "General Recommendation No. 29 (2002)". Hmm the example says "General Recommendation No. 29 (A/57/18)" — without year? "the document's name (title up to the first colon or ' on ')". So title up to first colon. If title is "General Recommendation No. 29 (2002)..." Hmm. Whatever the actual title is, we take up to colon or " on ". I'll implement exactly that.

Grey note names the style: "UN short form".

Copy quotation: shown text in quotation marks + " " + citation. Which quotation — "the shown text": text with footnote marks removed, and leading number dropped when leading == paragraph. The full text (not truncated). Use curly quotes for the quotation marks? "copies the shown text in quotation marks" — I'll use straight double quotes... Actually for a submission, curly might be nicer, but the plan says quotation marks. I'll use straight double quotes "..." Hmm, but the text contains curly quotes inside. Either is fine; I'll use straight double quotes. Hmm, actually let me use curly “ ” for elegance? The plan doesn't specify. Keep it simple: straight double quotes. Wait — if the text itself contains double quotes (curly “ ”), wrapping in straight " is fine.

Add to draft: pushes {id, citation, quotation text, symbol, paragraph, pinpoint, committee, short_title, year, text_as_stored (the stored text), doc_url}. Dedupe? Plan doesn't say; allow duplicates? I'll dedupe by id — hmm, "collects quotations for the draft" — adding the same paragraph twice is silly. I'll skip if already present, with a live message "already in the draft". That's reasonable.

9. Draft tab: "Your draft (n quotations)", each with quotation, citation, remove button. Tab name carries count "03 DRAFT (4)". "Copy all" (quotation, new line, citation, blank line between items). Download .txt (same as copy all content? probably the same text) and .csv with columns citation, symbol, paragraph, pinpoint, committee, short_title, year, text_copied, text_as_stored, doc_url; UTF-8 BOM, fields double-quoted. localStorage when allowed, in memory otherwise; hint says where kept.

Download: create Blob, URL.createObjectURL, a.download. That works offline (no network).

localStorage: wrap in try/catch. Test availability at load.

10. Check & method tab: checks panel, one line each, pass green / check failed red:
- Query understood: echo + term count; parse errors.
- Totals: rows listed across pages equal hits; checkbox bracketed counts sum to hits plus joint hits.
- Chart total: bars sum to hits + joint hits, both shown.
- Highlight: every hit shows at least one <mark> unless NOT-only; matched-but-not-highlighted listed.
- Normalisation: when query holds straight quote/apostrophe/hyphen, say curly forms matched too, and how many hits contain only those forms. "hits contain only those forms" — count of hits where the term matched only via curly/dash variants, i.e., where the straight form wouldn't match the stored text? Hmm. Let me interpret: hits where the raw stored text does not contain the straight form but the normalised match succeeded — i.e., matched via curly/dash equivalence. I'll compute: for each positive term, hits whose stored text (lowercased, footnote marks intact) doesn't contain the literal term string but norm matches. Simpler: count hits where the straight-form regex (over raw text) fails but the normalised match succeeds. I can approximate: for each hit, check if the highlight regex matched... Actually let me compute: terms with straight quote/apostrophe/hyphen in them; hits where the literal term (as typed, case-insensitive) is not found in the stored text. That's "contain only those forms". Good enough and deterministic.
- Numbering: hits with leading number differing from paragraph; hits sharing pinpoint with another record of same title; lettered sub-paragraphs.
- Marks: for every hit, marks removed equal count of [[fn: in stored text, and reinserting gives stored text exactly. Reinserting — the shown text is text.replace(/\[\[fn:\d+\]\]/g,'') — removing them can't be reinserted positionally. "putting them back gives the stored text exactly" — hmm, that check would be: text.replace(regex, '') with marks counted... Actually the real check: removing all [[fn:N]] and counting matches — count of /\[\[fn:\d+\]\]/g equals count of '[[fn:' occurrences in text. And maybe verify that text.indexOf('[[fn:') count == marks. The "putting them back" is odd; I'll implement: marks == (text.match(/\[\[fn:/g)||[]).length, and no other '[[fn' malformed patterns (i.e., every occurrence of '[[fn:' is a well-formed mark). And re-check: shownText with marks removed... "putting them back gives the stored text exactly" can't literally be done. I'll do: stored text === shown text with... no. Let me just check: count of [[fn: occurrences equals marks, and each is well-formed. That's the meaningful check. I'll word the line accordingly: "For every hit, footnote marks removed = marks counted, every '[[fn:' well-formed". Pass/fail.

Actually, I could implement a genuine round-trip: replace each [[fn:N]] with a placeholder like \u0000 + i + \u0000... no, that changes nothing. Skip; word it honestly.

- Draft: for every item, look up stored text of record with that id, compare with item's text_as_stored; difference marks the item (red note on draft item).
- Known quirks (computed at load, shown before any search): records with paragraph 0, symbols shared by several documents, joint documents, duplicated pinpoints, leading-number mismatches, each with count and example.

Header right: green dot + "n checks pass" or red dot + "n checks failed" (and red dot on tab 04). So I need a global checks status. Compute checks; some depend on current query. The header shows overall: if any check failed → red. Checks count: number of check lines. Let me compute the checks whenever state changes (query/filters/render) and update header. Some checks like "Totals: rows listed across pages equal hits" — I render max 25 + "show more"; rows listed = number actually rendered. Hmm, that check is about pagination consistency: rows rendered + hidden = hits. I'll count rendered rows + remaining count. Let me implement: renderedCount + notRendered (computed) == hits.

Simplify: checks list computed in a function updateChecks() called after each render:
1. Query understood: echo, terms n. Pass if no parse error.
2. Totals: rendered rows + pending == hits; committee bracketed counts sum == hits + jointHits.
3. Chart total: bars sum == hits + jointHits (chart only on overview; compute regardless).
4. Highlight: all hits have ≥1 mark unless NOT-only; list matched-not-highlighted.
5. Normalisation (conditional).
6. Numbering quirks among hits.
7. Marks round-trip among hits.
8. Draft integrity.

Header: count of passes/fails. If any fail → "n checks failed" red + tab 04 red dot. Else "n checks pass" green.

Hmm "n checks pass" — n = number of passing checks. OK.

11. Footer: source, built; "Counting, matching and sorting are done by this page's code; no model is called." Credits: Chart.js MIT — the app uses Chart.js (preloaded). "A Credits line if shelf code is reused (Chart.js, MIT)." I'll add "Built with Chart.js 4 (MIT licence)."

Also data source line in header: source linked to source_url. WORKSHOP_DATA.gc has title, source, count, records — does it have source_url? The description says {title, source, count, records}. No source_url mentioned. The header plan says "source linked to source_url". I'll handle missing source_url gracefully (no link). Also `built` not mentioned for gc — the footer plan says "source and built". gc has no built field per description. Handle missing: show source only. Let me guard: const src = D.source || ''; const url = D.source_url || ''; const built = D.built || ''.

12. Tabs: role="tablist", arrow-key navigation. Numbered tabs: "01 OVERVIEW · 02 PARAGRAPHS · 03 DRAFT (n) · 04 CHECK & METHOD". At most five tabs — four here. Follow Hicks: left rail hidden on Draft tab (plan says "always visible except on the Draft tab"). Hmm, what about Check tab? Rail visible. OK.

Actually wait — plan says left rail always visible except Draft. On Overview, rail is useful (filters feed the chart). Fine.

Layout: header top; below: a row with left rail (narrow) + main content (tabs + panels). Actually tabs should be above content, and rail beside content. Let me structure:

<header> ... </header>
<div class="layout">
  <aside class="rail" (hidden on draft tab)> filters </aside>
  <main>
    <nav tabs>
    <section panels>
  </main>
</div>
<footer>

13. Search box in rail: labelled input + Search button; Enter searches. While empty and focused, list opens under it with syntax help + three example options that fill and run. Closes when typing starts. One line under the box about normalisation. After search, echo line. Unbalanced quote/parenthesis → message, no results.

Search semantics: the input holds the raw query; clicking Search (or Enter) parses and applies. Typing doesn't auto-search (examples "fill and run"). So state.query applied on demand. If input changed but not searched... keep last applied query. Fine.

Syntax list content (in the app's own words, per plan):
- a space or AND joins words
- OR
- NOT or a leading minus
- "an exact phrase" in double quotes
- parentheses
- a star at the end of a word for any ending (child* finds children)
- operators in capitals, lower-case "or" is a word

Three examples as options (buttons) that fill and run: `"best interests" AND child`, `(torture OR ill-treatment) NOT detention`, `"reasonable accommodation"`.

The list opens when box empty and has focus; closes when typing starts. Implement with focus/blur/input handlers; use mousedown on examples to run before blur.

14. Committee checkbox labels: code + full name + hits in brackets after a search. "all / none" links. Joint GC handling: appears when either committee ticked and shows both badges (on rows). Chart note: "Joint General Comments count under both committees, so the bars can add up to more than the hits".

Hmm wait — committee list for checkboxes: the distinct committee codes from records' committees sets. Order: maybe by total paragraphs descending, or fixed order. I'll order by total record count descending.

Years: from/to number inputs preset to min/max.

Document: select of short_title grouped by committee (optgroup), blank option "All documents". Values: title (since short_title may repeat? unlikely; use title as value, display short_title). Grouped by committee — but a joint GC has one committee field. Group under its committee field.

Document filter: record.title === selected.

15. Ordering: default year desc, then title, then paragraph asc. Select options: "year, newest first" (default), "document order" (title asc, paragraph asc), "most matches first" (count of highlight matches in norm desc, tie by default order). "most matches first" — number of term matches; compute via regex counts over norm. I'll count matches of the combined positive-term regex over norm.

16. Marks on rows: "3 footnote marks removed · show as stored" — only when marks > 0. Toggle swaps shown text (re-render row with stored text, highlighting still applied — highlight regex handles [[fn:]] in gaps; but marks inside... a footnote mark between words of a phrase is handled; a footnote mark inside a highlighted word? Not possible since marks sit between words mostly, but 212 are between two words of a sentence — that's exactly the gap case. If a mark is adjacent to a term (e.g., "word[[fn:1]]"), the term boundary lookarounds (?<![\p{L}\p{N}]) pass since [ is not a letter. Highlight regex over stored text: term boundaries fine. OK.)

Row expansion: clicking row toggles open. When open, show three buttons + context link. Context: previous/next paragraph of same title (paragraph field ±1? or adjacent records by paragraph sort within same title). Use records with same title sorted by paragraph; find index; show prev/next. The plan: "opens paragraph −1 or +1 of the same title inline". I'll find record with same title and paragraph === p−1 / p+1; if not found, disable. Actually adjacent records might have non-consecutive numbering (lettered subparas). Safer: sort same-title records by paragraph (and list order), find neighbours by position. I'll do positional neighbours in the sorted-by-paragraph list of that title, skipping... hmm, duplicates. Positional is fine: prev = the record before in paragraph-sorted order.

Context shown inline in grey with its own pinpoint; maybe also a copy? Plan says just shown, grey, with pinpoint. Keep simple: text (footnote marks removed? "in grey, with its own pinpoint, for a chapeau that ends in a colon" — show as stored or cleaned? I'll show cleaned (marks removed) — simpler reading; actually to be verbatim-safe show the stored text? The purpose is reading context. I'll show marks-removed with note if any. Keep simple: show text with marks removed, pre-wrap.)

17. Truncation: ≤700 chars shown whole; longer show first 700 cut at word boundary + button "Show the full paragraph (1,287 words)". Word count = text.split(/\s+/).length. After expanding, full text shown. When "show as stored" also — states: {truncated, full} × {clean, stored}. Manage per-row state in a Map keyed by id.

Highlight application: I need to highlight within the possibly truncated text. Truncation happens on the shown text (clean or stored). Highlight after truncation: first 700 chars may cut mid-highlight... The highlight regex applied to the truncated string — a phrase spanning the cut won't highlight; fine. But careful: truncation "cut at a word" — find last space before 700, cut there, add "…". Then apply highlight to that string. When full shown, apply to full.

Escaping: HTML-escape the text first, then apply highlight regex on the escaped string? Problem: escaping changes characters (& → &amp;) and regex indices. Better: run regex on raw string, split into segments, escape each segment, wrap marks. Implement highlightText(str) → builds HTML: iterate matches of combined regex, escape between-parts, wrap matched parts in <mark>.

But wait — the highlight regex must work on text with HTML-escapable chars; regex operates on raw string, fine.

Also `white-space: pre-wrap` to keep line breaks.

18. Amber notes on rows:
- "the text begins ‘45.’ but the record is para. 41: check the document" (leading differs from paragraph)
- "a lettered sub-paragraph, numbered 2 by the file" (text starts with ^(?\([a-z]{1,4}\)))
- "two records share this pinpoint" (same title + same paragraph appears twice)
- "joint General Comment" (two symbols in one symbol)

19. Pinpoint: "para. N"; "preamble" if paragraph 0; "subpara. (b)" if text starts with lettered label. Note paragraph 0 + lettered? subpara check on text. Order: if lettered label → subpara; else if paragraph === 0 → preamble; else "para. N".

Hmm wait — 22 lettered sub-paragraphs "that the file numbers 1, 2, 3". So text starts with "(a) To take note…". Pinpoint "subpara. (a)".

20. Citation: symbol + ", " + pinpoint. Shared symbol → committee + ", " + docName + " (" + symbol + "), " + pinpoint, where docName = title up to first colon or " on " (whichever comes first).

21. Copy: navigator.clipboard.writeText; fallback: selectable box with "Select and copy". After every copy, aria-live message shows the exact string sent. I'll show the message with the copied string (maybe truncated for long ones — "shows the exact string sent" — for a 1287-word quotation that's huge. Hmm. "an aria-live message shows the exact string sent". I'll show it in a visually small area, truncated visually with CSS? aria-live would read the whole thing... I'll show the exact string but cap display... The plan says exact string. Let me show it in a box, max-height with scroll. Fine.

22. NOT-only query: matches everything lacking terms; echo says so; highlight check skips.

23. Empty query with filters: lists everything passing filters, paged; summary says "no search words".

24. Checks details:

- Query understood: "Query understood: Paragraphs containing the phrase “best interests” and the word child · 2 terms" — pass. Parse error: "Query not understood: unbalanced quote" — fail.

- Totals: "Rows listed (25 shown + 254 more) = 279 hits" pass. "Committee counts sum to 281 = 279 hits + 2 joint" pass.

- Chart total: same numbers.

- Highlight: "Every hit shows at least one highlighted word (279 of 279)" pass; else list matched-not-highlightened ids.

- Normalisation: only when query contains straight ', ", or -: "The query holds a straight apostrophe; curly forms (’) were matched too; 3 hits contain only the curly form."

- Numbering: among hits: leading mismatches (with both numbers), shared pinpoints, lettered subparas — report counts; is this a pass/fail or informational? The plan lists it under checks with "pass" or "check failed". These numbering quirks are data quirks, not app failures... but the plan says each check is one line with pass/fail. Hmm: "Numbering. Hits whose leading number differs from paragraph, with both numbers; hits that share a pinpoint...; hits that are lettered sub-paragraphs." These are reported; do they fail? I think these are informational — the check is "numbering quirks identified and flagged on rows" → always pass, with details. Hmm. But "A failed check marks rows; it never drops them." So a numbering mismatch — is that a "check failed"? The data quirk exists regardless. I think the check passes when the app successfully identified them (they're shown on rows). I'll mark: "Numbering: 3 hits flagged (1 leading-number mismatch, 1 shared pinpoint, 1 lettered sub-paragraph) — shown on the rows" pass. If there are none: "no numbering quirks among hits" pass.

Hmm, but maybe mismatches should be "check failed"? The check is about the app's own consistency, not the data. Data quirks aren't app failures. I'll treat as pass with details. Actually, let me reconsider: the plan for header says "n checks pass" / "n checks failed". The genuinely failing conditions: parse error, totals mismatch, chart mismatch, highlight missing, marks round-trip failure, draft text changed. Numbering/normalisation are informational passes. OK.

- Marks: "Footnote marks: removed 5, counted 5, every [[fn: well-formed across 279 hits" pass/fail.

- Draft: "Draft: 4 items, all match the stored text of their records" pass; else "1 item differs from the stored text" fail, and mark the item red in Draft tab.

Known quirks of this file (computed at load, before any search):
- records with paragraph 0: count + example
- symbols shared by several documents: count + example
- joint documents: count + example
- duplicated pinpoints: count + example
- leading-number mismatches: count + example
Also maybe lettered subparas count. The plan lists: "records with paragraph 0, symbols shared by several documents, joint documents, duplicated pinpoints, leading-number mismatches, each with its count and an example." I'll add lettered sub-paragraphs too? It says "each with its count and an example" for the listed five. I'll include the five listed plus maybe lettered. Keep the five.

25. "How this is computed" section in tab 04: short form of the computation section.

26. Accessibility: search box focus on load; example list opens with arrow keys (make examples focusable buttons; when list open, ArrowDown moves focus into it); rows are <article>s with heading; count/summary/copied message aria-live polite; chart click duplicated by checkboxes.

Arrow-key tab navigation: standard roving implementation: keydown on tablist for ArrowLeft/Right, Home/End.

27. Now — data checks on `count`: top-level count is string "7304"; use records.length. Header line: "`records.length` paragraphs from n General Comments (distinct title) of k committees, year min–max".

Let me now also handle: `D.title` for gc is like "General Comments, paragraph by paragraph"? The header has its own title per plan. The data line: "7,304 paragraphs from 159 General Comments of 10 committees, 1972–2026" — computed.

28. Line count: keep under ~1,500 lines. This is a big app; I'll write compactly but readably. Aim ~1,200 lines.

Let me think about the query parser more concretely.

Tokenizer:
```
function tokenize(q){
  const toks=[]; let i=0;
  while(i<q.length){
    const c=q[i];
    if(/\s/.test(c)){i++;continue;}
    if(c==='('||c===')'){toks.push({t:c});i++;continue;}
    if(c==='"'||c==='“'||c==='”'){
      // find closing quote
      let j=i+1, buf='';
      while(j<q.length && !('"“”'.includes(q[j]))){buf+=q[j];j++;}
      if(j>=q.length) return {error:'unbalanced quote'};
      toks.push({t:'phrase', v:buf}); i=j+1; continue;
    }
    // word: run of non-space, non-paren chars; may start with '-'
    let j=i, buf='';
    while(j<q.length && !/[\s()]/.test(q[j]) && !'"“”'.includes(q[j])){buf+=q[j];j++;}
    if(buf==='AND'||buf==='OR'||buf==='NOT'){toks.push({t:buf});}
    else if(buf==='-'... 
```
Hmm, a leading minus: "-" alone? If buf starts with '-' and length>1 → {t:'NOT'} + word rest? Or token {t:'word', v:buf, neg:true}. Let me push NOT token then word token of buf.slice(1). If buf is just '-', treat as word '-'? Weird; treat as NOT with nothing → error "NOT with no term". I'll handle in parser.

Also a word could contain quotes? No — quotes start a phrase. A word ends at whitespace, paren, or quote.

Parser (recursive descent over tokens):
```
pos=0;
function parseOr(){
  let left=parseAnd();
  while(tok && tok.t==='OR'){pos++; left={k:'OR',l:left,r:parseAnd()};}
  return left;
}
function parseAnd(){
  let left=parseNot();
  while(true){
    const tk=toks[pos];
    if(!tk) break;
    if(tk.t==='OR'||tk.t===')') break;
    if(tk.t==='AND'){pos++;}
    // next is a term or NOT or '('
    left={k:'AND',l:left,r:parseNot()};
  }
  return left;
}
function parseNot(){
  let neg=false;
  while(toks[pos] && (toks[pos].t==='NOT')){pos++;neg=!neg;}
  if(neg) return {k:'NOT', v:parsePrimary()};
  return parsePrimary();
}
```
Hmm, careful with AND loop: after parseNot, if next token is AND consume it and parse next; if next is a term/NOT/'(' → implicit AND; if OR/')'/end → stop. But if next is AND and then nothing/or → error. Handle gracefully.

parsePrimary:
```
function parsePrimary(){
  const tk=toks[pos];
  if(!tk) return {error...}
  if(tk.t==='('){pos++; const n=parseOr(); if(toks[pos]&&toks[pos].t===')'){pos++;return n;} return error 'unbalanced parenthesis';}
  if(tk.t===')') error 'unexpected )';
  if(tk.t==='phrase'){pos++; return {k:'phrase', v:tk.v};}
  if(tk.t==='AND'||tk.t==='OR'||tk.t==='NOT') error 'operator without term';
  // word
  pos++; return {k:'word', v:tk.v};
}
```

Errors as thrown object {msg}; catch and show.

Matching:
```
function buildMatcher(node){
  switch(node.k){
    case 'word': {const re=wordRe(node.v); return s=>re.test(s);}
    case 'phrase': {const re=phraseRe(node.v); return s=>re.test(s);}
    case 'AND': return s=>buildMatcher... 
```
Better: compile once → function. Compile each node recursively into predicate.

wordRe(w): strip trailing '*', normWord = normaliseString(w) (lowercase, curly→straight, dashes→'-'), escape, trailing \w* if star. Pattern: `(?<![\\p{L}\\p{N}])` + body + `(?![\\p{L}\\p{N}])`, flags 'u'.

Wait — normalising the word: whitespace inside a word can't happen (tokenised by space). NBSP in query → normalised to space... but word tokens are split on /\s/ — NBSP is \s? Yes, \s includes NBSP in JS. OK good.

But careful: normalise collapses whitespace to single space — for a single word irrelevant.

phraseRe(p): split into words on whitespace, normalise each, join with \\s+.

Echo builder:
```
function echo(node){
  switch(node.k){
    case 'word': return node.v.endsWith('*') ? `any word ending “${node.v}”` : `the word ${node.v}`;
    case 'phrase': return `the phrase “${normPhrase}”`;
    case 'AND': return `${echo(l)} and ${echo(r)}`;
    case 'OR': return `${echo(l)} or ${echo(r)}`;
    case 'NOT': return `paragraphs not containing ${echo(v)}`;
  }
}
```
Top-level echo: "Paragraphs containing X". If root is NOT: "Paragraphs not containing X" (the NOT-only case: matches everything lacking). If root NOT: echo = "Every paragraph except those containing X"? Plan: "a NOT-only query matches everything that lacks the terms, and the echo says so". So echo(root NOT) = `Paragraphs containing ${echo(l)}... ` hmm. Let me special-case: if root.k==='NOT', echo = "Paragraphs that do not contain " + echo(child). And for NOT nested in AND: "(not " + echo + ")"? E.g. `A NOT B` parses as A AND (NOT B) → echo "the word a and paragraphs not containing the word b". Let me phrase NOT-child as "not " + echo(child): "the word a and not the word b". And root NOT: "not the word b" → full line: "Paragraphs matching: not the word b — that is, every paragraph that lacks it." Simpler: I'll produce "Paragraphs containing: ..." list-style. Let me define:

echoNode:
- word: `the word “child”` (or `any word ending “child”` with star... plan example: "a star at the end of a word for any ending (child* finds children)")
- phrase: `the phrase “best interests”`
- AND: `${l} and ${r}`
- OR: `${l} or ${r}`
- NOT: `not ${child}`

Top: if root.k==='NOT': line = `Paragraphs that lack: ${echo(child)}` hmm the plan's example: "Paragraphs containing the phrase “best interests” and the word child". So top prefix "Paragraphs containing ". For root NOT: "Paragraphs not containing the word detention". Good enough — echo says the query matches everything lacking. I'll add for root NOT: append " (every paragraph that lacks these terms)". Fine.

Term collection for highlight: walk tree; terms under an odd number of NOTs are excluded.

```
function collectTerms(node, neg, out){
  if(node.k==='word'||node.k==='phrase'){ if(!neg) out.push(node); }
  else if(node.k==='NOT') collectTerms(node.v, !neg, out);
  else { collectTerms(node.l,neg,out); collectTerms(node.r,neg,out); }
}
```

Highlight regex from terms:
```
function hlRe(terms){
  const alts = terms.map(t=>{
    if(t.k==='word') return wordHlPattern(t.v);
    return phraseHlPattern(t.v);
  });
  return new RegExp('(?:'+alts.join('|')+')','giu');
}
```
wordHlPattern(w): strip trailing '*'; map chars:
- '"' → '[“”"]'
- "'" → '[‘’\\']'
- '-' → '[-–—]'
- '*' handled
- else escape
append '\\w*' if star.
Boundaries: `(?<![\\p{L}\\p{N}])` ... `(?![\\p{L}\\p{N}])`.

phraseHlPattern(p): words = p.trim().split(/\s+/); each word → char-class pattern (no star? plan: star at end of a word — could allow in phrase words too; trailing * in phrase word → \w*. I'll support it). Join with `(?:\\s|\\[\\[fn:\\d+\\]\\])+`.

Hmm — one catch: highlight runs on text where the leading number "12. " exists; fine.

Another catch: the 'u' flag with escaped chars — escape function must escape regex specials: /[.*+?^${}()|[\]\\]/g → '\\$&'. Hyphen outside char class is literal — but I map '-' to class anyway.

Wait, in wordHlPattern, a '-' in the query word maps to '[-–—]' — good. But what about other punctuation like '.' or ','? escaped literal. Good.

Combined highlight regex with 'giu' — case-insensitive since shown text keeps case while query is normalised lowercase.

Edge: term with star: child* → pattern child\w* with boundaries. \w includes underscore and ASCII alphanumerics only (with u flag, \w still ASCII). "any ending" — fine for children.

Hmm, but accented letters: \w doesn't match é. "children" fine. OK.

Now norm function:
```
function normText(s){
  return s.replace(/\[\[fn:\d+\]\]/g,'')
    .replace(/[“”„]/g,'"').replace(/[‘’‚]/g,"'")
    .replace(/[–—‑]/g,'-')  // en, em, soft hyphen
    .replace(/\s+/g,' ')   // includes NBSP? \s matches NBSP yes
    .toLowerCase();
}
```
Wait order: remove footnote marks first, then collapse whitespace (removing marks may leave double spaces). Also lower case last. Also NBSP → \s handles. Good. Soft hyphen \u00AD. Also maybe non-breaking hyphen \u2011 — plan mentions "hyphenation" in the wiki context; here plan says "en dash, em dash and soft hyphen → '-'". I'll include \u2011 too? Plan for this app says: "en dash, em dash and soft hyphen → '-'; non-breaking space and all other whitespace → one space". I'll follow exactly, adding \u2011 harmless... no, follow plan exactly: [–—‑] = \u2013 \u2014 \u00AD.

For the query normalisation, same function but footnote removal irrelevant.

Note: lowercasing — use toLowerCase(). Fine.

Norm must be computed once per record at load: 7,304 records — fine.

Committees:
```
function recCommittees(rec){
  const s=new Set();
  const sym=rec.symbol||'';
  if(/CAT\/OP/.test(sym)) s.add('CAT-OP');
  else {
    const m=sym.match(/\b(CAT|CCPR|CED|CEDAW|CERD|CESCR|CMW|CRC|CRPD)\b/g);
    if(m) m.forEach(c=>s.add(c));
  }
  if(rec.committee) s.add(rec.committee);
  return s;
}
```
Wait — what if symbol has both CAT/OP and something else? Unlikely. Also joint symbols like "CMW/C/GC/7–CERD/C/GC/38": \b(CMW)\b matches, \b(CERD)\b matches. Good. "CRC/C/GC/23, CMW/C/GC/4": both match. 

Hmm wait, but "CAT/OP" check: what about Subcommittee symbols like "CAT/OP/... "? Yes. But also, does \b(CAT)\b in "CAT/OP/..." — if I check CAT\/OP first and add CAT-OP, should I also run regex excluding CAT? The else branch means: if CAT/OP present, only CAT-OP added from symbol. Then committee field also added ("CAT-OP"). Good.

Joint: symbol contains two symbols — detect: count of committee codes in symbol ≥ 2, or presence of '–' or ', ' joining two symbol-like parts. Plan: `joint` = two symbols in one symbol. I'll compute: matches of the code regex (or CAT-OP) in symbol, count ≥2 → joint. "CMW/C/GC/7–CERD/C/GC/38": CMW, CERD → 2. "CRC/C/GC/23, CMW/C/GC/4": CRC, CMW → 2. Good. But careful: "CCPR/C/21/Rev.1/Add.4" — only CCPR. "CAT/C/..." only CAT. OK.

Hmm, wait: does \b(CED)\b match inside "CEDAW"? \bCED\b — in "CEDAW", after D comes A (word char), so no boundary → no match. Good. CERD in CERD? fine. CRC in "CRC"? fine. But "CRC" inside "CRC/C/GC/23, CMW/C/GC/4" both match. 

But careful: \b(CAT)\b matches "CAT" in "CAT/OP/..." too — handled by the if/else.

Hmm, another subtlety: \b(CESCR)\b — in symbol "E/..."? CESCR symbols are like "E/C.12/..."! The committee field says CESCR but symbol starts with E. So code regex on symbol finds nothing → committees = {committee field} = {CESCR}. Fine. Same for CED? CED symbols might be "C/CED/..." hmm. Whatever — committee field saves us.

Shared symbol: group records by symbol; symbol with >1 distinct title → shared. Precompute map symbol → set of titles; also for citation, need the doc's name; for shared symbol, the record's own title (each record has title).

Duplicated pinpoints: group by title+':'+paragraph; count>1 → dup flag.

Leading: m = text.match(/^(\d{1,3})\.\s/).

Lettered subpara: /^\(([a-z]{1,4})\)/.

Pinpoint:
```
function makePinpoint(rec){
  const m=(rec.text||'').match(/^\(([a-z]{1,4})\)/);
  if(m) return 'subpara. ('+m[1]+')';
  if(rec.paragraph===0) return 'preamble';
  return 'para. '+rec.paragraph;
}
```
Hmm, but subpara detection: what if paragraph 0 and lettered? Lettered wins per plan order? Plan: "Pinpoint: 'para. ' + paragraph; 'preamble' when paragraph is 0; 'subpara. (b)' when text starts with a lettered label". Ambiguous ordering; lettered check first seems right.

Citation:
```
function makeCitation(rec){
  const pin=rec._pin;
  if(rec._shared){
    const name=docName(rec.title);
    return `${rec.committee}, ${name} (${rec.symbol}), ${pin}`;
  }
  return `${rec.symbol}, ${pin}`;
}
function docName(t){
  const iC=t.indexOf(':'); const iO=t.indexOf(' on ');
  let i=Infinity;
  if(iC>-1) i=Math.min(i,iC);
  if(iO>-1) i=Math.min(i,iO);
  return i===Infinity? t : t.slice(0,i).trim();
}
```
Hmm "title up to the first colon or ' on '" — first occurrence of either. OK.

Quotation (copied): shown text = clean text (marks removed); if leading == paragraph, drop the leading "12. ". So:
```
function quotationText(rec){
  let t=(rec.text||'').replace(/\[\[fn:\d+\]\]/g,'');
  if(rec._leading!=null && rec._leading===rec.paragraph){
    t=t.replace(/^\d{1,3}\.\s+/,'');
  }
  return t;
}
```
Copy quotation = `"${quotation}" ${citation}`.

Now the shown text on rows keeps the leading number.

Filters state:
```
state = {
  query: null (parsed tree) or {error}, rawQuery,
  committees: Set (ticked) — default all,
  yearFrom, yearTo,
  docTitle: '' (all),
  order: 'year',
  shown: 25,
  openRows: Set of ids,
  rowModes: Map id -> {stored:bool, full:bool},
  contextShown: Map id -> 'prev'|'next' (or both?) — "Context: previous | next" link opens one inline. I'll allow toggling each.
  draft: [],
}
```

Hits computation:
```
function computeHits(){
  return R.filter(rec=>{
    if(state.q && state.q.tree){ if(!state.q.match(rec._norm)) return false; }
    // committees
    const cs=rec._committees;
    let any=false; for(const c of cs) if(ticked.has(c)){any=true;break;}
    if(!any) return false;
    if(rec.year<state.yearFrom||rec.year>state.yearTo) return false;
    if(state.docTitle && rec.title!==state.docTitle) return false;
    return true;
  });
}
```

Re-render on any state change. Rendering approach: full re-render of active panel; rail counts update too. Keep it straightforward: render() updates rail numbers, chips, tab panels (only active one fully; but draft count in tab label always). Chart re-created on overview render (destroy previous).

Performance: 7,304 records; filtering per keystroke? Search only on button/Enter, so fine. Committee checkbox change → recompute hits: 7,304 predicate calls with regex tests — fine.

But committee bracket counts "after a search": count per committee over hits — but hits depend on ticked committees... circular. The bracketed count per committee should be: over the query-matched + non-committee-filtered set? Hmm. "Committee: a checkbox per code with its full name and, after a search, its hits in brackets". I think brackets show query hits per committee ignoring committee ticks (but applying other filters?). To keep it simple and consistent with the check ("the checkboxes' bracketed counts sum to the hits plus joint hits"): bracketed count = query+year+doc filtered, per committee (each record counted under each of its committees). Sum over committees = queryHits + jointExtra where jointExtra = records with 2 committees counted twice. And "hits plus joint hits": hits = filtered set... hmm if some committees unticked, hits < queryHits. The check says "the checkboxes' bracketed counts sum to the hits plus joint hits". If brackets counted over query-matched (pre-committee-filter), sum = queryHits + joints, not hits + joints when committees narrowed. 

Let me re-read: "Totals. Rows listed across pages equal the hits; the checkboxes' bracketed counts sum to the hits plus joint hits." For this to hold, bracketed counts must be over the hits (post-filter). But then a ticked-only subset... if I narrow to CRC only, other committees' brackets show 0? That's weird but consistent. Hmm, but then the brackets are useless for deciding what to tick.

Alternative interpretation: brackets show counts over the set matching query + year + doc (ignoring committee filter) — the natural "hits per committee" for browsing. Then sum = thatSet + joints. The check then compares against that set, not hits. The plan's check says "sum to the hits plus joint hits". 

Hmm. Wait — maybe the intended design: the committee filter's bracketed counts are over the current hits (with committee filter applied). If all ticked (default), hits = queryHits, and sum = hits + joints. The check presumably runs in the common case... but checks should always hold.

Let me think about what's most useful and still checkable: brackets = count over query+year+doc matched records by committee (committee filter NOT applied). Then define Q = that set (call it "query-matched before committee filter"). Check line: "Committee brackets sum to Q + joints". But the plan's check literally says "the checkboxes' bracketed counts sum to the hits plus joint hits". If brackets were over hits, then when I untick CRC, CRC bracket → 0 and others recount... sum = hits + joints still holds actually! Because each hit record contributes to each of its committees' brackets (and ticked committees include at least one of its committees... no wait — a record passes if ANY of its committees is ticked; its bracket contribution goes to ALL its committees, including unticked ones. So sum over all committees' brackets = Σ_hits (num committees of rec) = hits + jointHits (where jointHits = hits with 2 committees). Yes! If brackets count hits per committee (post-filter), sum = hits + Σ(extra committees) = hits + jointHits. The check holds always.

But is it useful? When I untick CRC, the CRC bracket shows... records that are joint with a ticked committee? A pure-CRC record fails the filter, so contributes 0 to CRC bracket. So CRC bracket drops. Hmm — that's actually informative in a weird way but bad for browsing.

Alternative: brackets over pre-committee-filter set. Then check would need "sum = preSet + joints". The plan says hits. I'll follow the plan: brackets over current hits, counted per committee. Hmm wait, but then the default state (all ticked, empty query) → brackets = totals per committee. Good. After a search with all ticked → query hits per committee. Good. If user unticks → brackets reflect the filtered set. It's self-consistent and the check holds. But honestly for usability, pre-filter counts are better for choosing committees...

Hmm, let me reconsider. "Committee: a checkbox per code with its full name and, after a search, its hits in brackets; all ticked". The phrase "its hits" — the hits. OK, brackets over hits. But there's a subtle issue: with all ticked (the common case), it's the same as pre-filter. I'll go with hits-based brackets per plan. Hmm, wait — actually, one more consideration: "the chart adds it to each of its committees' bars" — chart bars are over hits per committee, same as brackets. Consistent. And "Chart total. The bars sum to the hits plus joint hits, both shown." Great — consistent: bars = brackets = per-committee counts over hits. Sum = hits + jointHits. 

So: hitsPerCommittee: for each hit, for each c in rec._committees → count[c]++.

Wait, but does a joint record's committee set include both CMW and CERD? Symbol "CMW/C/GC/7–CERD/C/GC/38" → regex finds CMW, CERD → yes. And committee field is one of them (say CMW). Good.

But hold on: chart "one bar per committee" — 10 committees. And the checkbox list order. I'll order committees by total paragraphs desc.

Hmm wait, one more issue: the plan says "Hits per committee = one count per committee over the hits, by each record's committee:" (then the committees definition). So yes, per-committee over hits via committees set.

Now jointHits (for the check): number of hit records whose committees set size ≥2 (specifically, extra = Σ(|cs|-1) over hits). I'll compute extras = Σ(|cs|−1). Bars sum = hits + extras. Display: "bars sum to 281 = 279 hits + 2 double-counted joint records".

Also chart note: "Joint General Comments count under both committees, so the bars can add up to more than the hits".

Now the chart click: "click a bar = tick that committee alone". Implement chart onClick → get index → committee → set ticked = {that committee} → update.

Rail structure:
```
FILTERS  [Clear all]
  279        (big serif, aria-live)
  matching paragraphs
  of 7,304
  [chips...]
  SEARCH
  [label][input][Search button]
  (syntax dropdown)
  normalisation line
  echo line / error
  01 COMMITTEE, YEARS, DOCUMENT  (button, aria-expanded)
    Committee: checkboxes, all/none
    Years: from – to
    Document: select
```
One numbered heading, closed until clicked, one open at a time — only one heading here. Default closed? "each closed until clicked" — so closed by default. Hmm, but filters are the main interaction... The plan explicitly designed it: one numbered heading "01 Committee, years, document", closed until clicked. OK, follow it. Big number and search always visible.

Chips: committee (when subset), years (when narrowed), document (when set). Removable.

"Clear all" — clears query and filters (reset committees to all, years to min/max, doc to all, query empty, input empty).

Tabs: also need tab 03 label to carry draft count: "03 DRAFT (4)". Update on draft changes.

Now the rows rendering. Each row:
```
<article class="row" data-id>
  <h3 class="row-head">
    <button class="row-toggle" aria-expanded>
      <span class="badge">CRC</span> <span class="badge">CMW</span>
      <span class="row-doc">GC 23...</span>
      <a href=doc_url target=_blank>symbol</a>
      <span class="pin">para. 18</span> <span class="yr">2017</span>
    </button>
  </h3>
  <p class="row-text">...highlighted text...</p>
  <p class="row-sub">3 footnote marks removed · <button>show as stored</button></p>
  <button>Show the full paragraph (1,287 words)</button>
  <p class="note amber">...</p>
  (expanded:)
  <div class="row-actions">
    <button>Copy citation</button> <button>Copy quotation</button> <button>Add to draft</button>
    <span class="ctx">Context: <button>previous</button> | <button>next</button></span>
    <span class="style-note">UN short form</span>
  </div>
  <div class="context" hidden>...</div>
</article>
```

Click on row toggles open: attach click handler on article; ignore clicks on buttons/links (closest('a,button')). Keyboard: the h3 button toggles.

Wait, "A click on a row opens it in place" — clicking toggles open/close. And the truncation/footnote toggles are separate buttons inside (their clicks shouldn't toggle the row — handled by closest check).

Copy feedback: an aria-live region in main; message "Copied: CCPR/C/GC/37, para. 12" showing exact string. For long quotations, show truncated? "shows the exact string sent" — I'll show exact but cap the visible box with CSS (max-height, overflow auto). aria-live polite will announce it (long, but per plan).

Fallback copy: if clipboard writeText rejects → show a box (textarea/div selectable) with the text and "Select and copy" note. Place near the live region — a single fallback area that appears with the text selected? Use a textarea + select() and message "Clipboard refused — select and copy:". 

Now check panel structure — a list of lines:
```
<ul class="checks">
  <li class="pass|fail"> <span class="mark">pass</span> description </li>
```
"pass" in green or "check failed" in red — as words too (colour + word).

Header right: `<span class="dot green"></span> n checks pass` or red. Compute after each updateChecks.

Also "a red dot on tab 04" when failed.

Known quirks (at load):
- paragraph 0 records: count + example ("CEDAW/C/GC/... preamble")
- shared symbols: count symbols (or records?) + example symbol
- joint documents: count + example
- duplicated pinpoints: count + example
- leading-number mismatches: count + example (both numbers)

Show as list with counts and examples, with links? Keep simple: count + example text with symbol.

"How this is computed" short form in tab 04: a few lines summarising: norm, query parse, term match, highlight, hits, order, citation, copy.

Footer: source + built; "Counting, matching and sorting are done by this page's code; no model is called." + Credits: "Chart.js 4 (MIT licence)".

Wait — does gc data have `built`? Not per spec ({title, source, count, records}). I'll conditionally show.

Now let me also handle the summary line on tab 02: "279 of 7,304 paragraphs match · 8 committees · 1990–2023" — committees = distinct committees among hits; years min–max among hits. If empty query: "no search words" mention: e.g. "7,304 of 7,304 paragraphs match (no search words) · 10 committees · 1972–2026".

Order line: "sorted by year, newest first, then by document and paragraph" + select with options: "year, newest first" / "document order" / "most matches first".

Hint: "This page retrieves; it never writes. Every paragraph shown is a record of the file, as stored."

Pagination: show 25, "Show 25 more" button (shows 25 more each click). Hidden when all shown. Also maybe "showing 25 of 279".

Now the check "Totals: rows listed across pages equal the hits": rowsRendered + remaining = hits. remaining = max(0, hits.length - state.shown) — but "rows listed" = min(shown, hits.length). Check: min(shown,hits) + (hits - min) == hits — trivially true... unless rendering bug. It's a self-check; fine, it verifies the DOM row count actually. Let me count actual DOM articles and compare: renderedRows = document.querySelectorAll('#panel-records .row').length; expected = min(shown, hits.length). Plus the "Show 25 more" button shows remaining count. Check: renderedRows == min(shown, hits). Good, that's a real DOM check.

Committee brackets check: sum of bracket values (computed) == hits + extras.

Chart bars check: same numbers as brackets (bars built from same data) — check bars sum == hits + extras; show both.

Highlight check: for each hit, does highlight regex match the shown text (clean)? Since clean text vs norm: norm is lowercased clean (plus normalisations). The highlight regex is more permissive (curly variants), so it should match whenever the match regex matches... except: norm removes footnote marks and collapses whitespace; highlight gap pattern (?:\s|\[\[fn:\d+\]\])+ handles phrase gaps across marks and line breaks. But what about a phrase gap across a footnote mark AND curly quotes inside words — handled. Edge: a word match where the stored text has a soft hyphen inside? E.g., query "non-State" vs text "non‐State" (U+2010 hyphen)? norm maps only –, —, soft hyphen. U+2010 not mapped... rare; skip.

Another edge: mark adjacent changes boundary: word "education" with text "education[[fn:1]]" — lookbehind/ahead: [ not letter → matches. In norm, mark removed → "education " fine. In highlight over clean text (marks removed) also fine. Over stored text (with marks) also fine. 

Real edge where highlight fails but match succeeds: phrase spanning a footnote mark where the clean text has been... no, gap pattern covers \s and marks. Hmm — what if the phrase gap in norm came from collapsed multiple whitespace including line break — clean text has "\n" which is \s → covered.

What if the word has a straight apostrophe in query, text has curly — hl pattern covers. If word ends with '*' → \w* — covered.

So the highlight check should always pass; it's a genuine self-check anyway. Implement by testing hlRe against clean text for each hit; collect failures.

Normalisation check: query holds straight quote/apostrophe/hyphen (in any positive term) → line: "The query holds a straight apostrophe (’) — curly forms were matched too; N hits match only through the curly form." Compute N: hits where for at least one such term, the literal straight form isn't in raw text but match succeeded. Simpler: count hits where hlRe... hmm. Let me implement: straightChars = positive terms containing "'" or '"' or '-'. For each hit, "only those forms" = the match regex (which normalises) succeeds but a strict regex (no variant mapping, case-insensitive, footnote-aware) fails. Building the strict regex: same boundaries but literal chars, over raw lowercased text? Approximation: for each hit, check if rawText.toLowerCase() contains any straight variant... this is getting complicated. 

Simpler honest approach: count hits where the stored text does not contain the straight form of the term (case-insensitive literal substring, whitespace-flexible?) but norm matches. I'll do: for each term with straight ', ", or -: build a "strict" regex like the match regex but without normalising the text (apply to raw text lowercased, marks kept). If strict fails but normalised match succeeds → hit relies on curly/dash forms. Count those hits. That's deterministic and honest. Implement strictRe: word/phrase pattern with literal chars, flags 'giu' applied to rec.text (raw). Phrase gaps: (?:\s|\[\[fn:\d+\]\])+? In raw text the phrase could span marks... keep same gap pattern. OK.

Hmm, this is getting heavy. Simplify: normalisation line reports: "The query holds a straight apostrophe; curly and dash forms count as the same (see the line under the search box). N of the hits match only through a curly or dash form." Compute N via: for each hit, if !strictAny.test(text) → N++. Where strictAny = alternation of strict term regexes. I'll implement it as: reuse hlPattern machinery but with strict char mapping (identity). Fine, ~10 lines.

Actually — simpler still and still honest: N = hits where the combined highlight regex matched only via variant classes... no way to know which alternative. Go with strict regex approach.

Hmm, wait. Actually let me simplify further: the strict check applies per straight-char term: strictRe over rec.text. If none of the straight-char terms strictly match → but overall match true (could be via other terms!). Ugh — AND semantics: hit may match term A (plain) and term B (straight-apostrophe, only curly form present). Then "hit contains only curly form of B" is true and meaningful. So: N = hits where (some straight-char term's normalised match true) AND (that term's strict match false). I'll compute per-term: normalisedMatched(term) && !strictMatched(term). For counting, evaluate per hit per straight-term. Need per-term matchers — I have them in the tree; I can compile each term separately. OK, doable: compile term list with both normalised and strict matchers.

Let me structure code:

```
// per-term compiled: {kind:'word'|'phrase', raw, normRe, strictRe, hlPattern}
```
Build from collectTerms. Tree matching uses normRe per term (compile once, cache).

OK. Now, marks check: for each hit: marks == (text.match(/\[\[fn:/g)||[]).length && text.replace(/\[\[fn:\d+\]\]/g,'') removes exactly marks occurrences — the replace count: (text.match(/\[\[fn:\d+\]\]/g)||[]).length === marks && count of '[[fn:' === marks. Fail → list ids.

Draft check: for each draft item, find record by id; if !rec → "record no longer found" fail; else rec.text === item.text_as_stored? Compare. Difference marks item (red note in draft list).

Now, overview tab layout: FIG.01 title (serif), figure number label, chart canvas (role img, aria-label, fallback content), small table beside, hint "click a bar = tick that committee alone", how-computed line, chart note about joints.

Chart config:
```
new Chart(ctx, {
  type:'bar',
  data:{labels, datasets:[{data, backgroundColor:'#9b2335', ...}]},
  options:{
    indexAxis:'y',
    responsive:true, maintainAspectRatio:false,
    onClick: (e, els)=>{...},
    scales:{
      x:{beginAtZero:true, grid:{color:'#e6dfd0', maxTicksLimit:10}, ticks:{font:{family:'mono...'},color:'#1d1b18'}},
      y:{grid:{display:false}, ticks:{font:{...}}}
    },
    plugins:{legend:{display:false}, tooltip:{enabled:true}}
  },
  plugins:[valuePlugin]
});
```
valuePlugin: afterDatasetsDraw: draw value text at end of each bar: ctx.save(); font mono 12; fillStyle '#1d1b18'; for each bar: x=meta.data[i].x+6, y=base... textAlign 'left', baseline 'middle', fillText(value).

Container height: 10 bars × ~40px = 400px; set style height on wrapper.

aria-label on canvas: "Paragraphs per committee: CRC 2,091; ...". Canvas content fallback: text inside canvas element.

Note: canvas element with role="img" and aria-label; put fallback text as canvas innerText (not rendered but available). OK.

Also "a small table with the same numbers beside it" — table with committee, paragraphs. With caption? "Tables: <caption>, <th scope="col">". Add caption "FIG.01 Paragraphs per committee — table". Numbers right-aligned.

Layout: chart left (flex 1), table right (narrow). On narrow screens wrap.

Now — bar chart with 10 committees; ranked by value desc.

Also committees with 0 hits: show or hide? One bar per committee — include zeros? Ranked, zeros at bottom. I'll include all committees that exist in data (10), showing 0 where none. Fine.

Now the tab list with arrow keys:
```
tablist keydown: ArrowRight/Left/Home/End → move focus & activate (I'll activate on focus? Standard: activation on focus or on click; use click-activation plus arrows move focus and activate — simpler: arrows activate).
```
Implement: each tab button role="tab", aria-selected, aria-controls panel; panels role="tabpanel".

Left rail hidden on draft tab: when tab 03 active, aside hidden. Use [hidden] + CSS rule.

Search input focus on load: input.focus() — but only if not reduced-motion... just do it. Hmm, focusing input on load might open the syntax dropdown (empty + focus → opens). That's per spec: "While the box is empty and has focus, a short list opens under it". On load with focus, the list opens — that's actually per spec. OK. Hmm, it might be slightly annoying but it teaches syntax. Follow the plan.

The list closes when typing starts (input event with value → close).

Examples as options: buttons (role="option"? it's a listbox-ish; simpler: buttons in a div, arrow keys move between them). "the example list opens with the arrow keys" — pressing ArrowDown in the input moves focus to first example. Implement keydown on input: ArrowDown → focus first example button; example buttons handle ArrowUp/Down to move between, ArrowUp from first → back to input; Escape closes. Enter on example → fill and run.

Run example: set input value, close list, parse, apply, render.

Now — search application flow:
```
function runSearch(){
  const raw=input.value.trim();
  state.rawQuery=raw;
  if(!raw){ state.q=null; ... } 
  else { try{ tree=parse(raw); state.q={tree, echo, terms}; } catch(e){ state.q={error:e.msg}; } }
  state.shown=25; update();
}
```
Error: message shown, no results — hits = [] when q.error. Echo line shows error in red.

Update flow:
```
function update(){
  hits = computeHits();
  orderHits();
  updateRail();  // big number, chips, brackets, doc select counts?, year inputs
  renderTabs();  // active panel
  updateChecks(); // header status + tab04 panel content (render even if not active? build data; render panel when active — but checks status in header always)
}
```
I'll render the active panel each time; checks computed as data (list of {ok, text}) each update; header updated; tab 04 panel rendered from stored list when shown.

Draft: array of items; persist to localStorage (key 'gc-verbatim-draft') try/catch; memory fallback flag. Load at start.

Draft tab render: list items: quotation (blockquote), citation, remove button. If item differs from stored text → red note "the stored text of this record has changed since it was added" — wait, the check compares item.text_as_stored with current record text; records are static in-session, but across sessions data could change. Mark if differs.

Copy all: items.map(i => `"${i.text_copied}"\n${i.citation}`).join('\n\n')? Plan: "quotation, new line, citation, blank line between items". So each item: quotation text (already includes quotes? "copies the shown text in quotation marks" — the item's quotation as copied. I'll store text_copied (without quotes) and build `"..."` at copy time consistently. Copy all: `"${text}"\n${citation}` joined by '\n\n'.

Download .txt: same content as copy all? Plan: "Download .txt" and "Download .csv" — txt presumably the draft text. Yes.

CSV: columns citation, symbol, paragraph, pinpoint, committee, short_title, year, text_copied, text_as_stored, doc_url. UTF-8 BOM \uFEFF. Fields double-quoted, escape " as "". Rows joined \r\n.

Download: Blob + a.click(). URL.revokeObjectURL after.

localStorage: save on draft change (if allowed). Note: text_as_stored can be large; 7,304... draft items only, fine. Quota errors caught → switch to memory mode with note.

Now the rail "Clear all" resets everything including query.

Chips: 
- committee chip when ticked != all: "Committees: CRC, CEDAW (2 of 10) ×"
- year chip when narrowed: "Years 1990–2023 ×"
- doc chip: "Document: GC 23 … ×"
Click × removes that filter (reset dimension). Chip is a button with the text and ×.

Big number: hits.length formatted with thousands separator (toLocaleString('en-US')). "matching paragraphs" / "of 7,304".

Committee checkbox labels: `<label><input type=checkbox> CRC Committee on the Rights of the Child [2091]</label>`. With brackets showing hits per committee. "all / none" small links (buttons).

Years: two number inputs.

Document select: optgroups per committee, options short_title, value title. Only documents... all 188 titles? That's a long select but fine (it's a dropdown). Blank "All documents (188)". Hmm, value: title strings can be long; fine. Should the doc list reflect other filters? Keep static (all docs), simpler and predictable. Actually plan doesn't say; static.

Wait — grouped by committee: which committee for grouping? rec.committee field. Build map from records: committee → set of titles (with a representative short_title). Joint GCs have one committee field. OK.

Now let me think about the "echo" line: "After a search, a line echoes the query as understood: 'Paragraphs containing the phrase “best interests” and the word child'." Show in rail under search box. Also term count maybe in checks.

NOT-only detection: root.k === 'NOT' → notOnly = true. Echo: "Paragraphs not containing the word detention — every paragraph that lacks it". Highlight check: skip when notOnly. Also when notOnly, no marks shown (terms are negative). collectTerms with neg tracking handles: terms under NOT excluded → empty list → no highlight.

Empty query: echo line hidden or "no search words".

Summary line tab 02: `${hits.length} of ${R.length} paragraphs match · ${nCommittees} committees · ${minY}–${maxY}` + (no search words note when query empty). Wait plan: "An empty query with filters lists every paragraph that passes them, paged, and the summary says 'no search words'." So append "· no search words" when q empty. If q.error: "0 of N paragraphs match · search not understood".

Ordering:
- year: (b.year - a.year) || a.title.localeCompare(b.title) || (a.paragraph - b.paragraph)
- doc: a.title.localeCompare(b.title) || a.paragraph - b.paragraph
- matches: matchCount(b) - matchCount(a) || year order

matchCount: count of positive-term matches over norm: combined norm regex with 'gu' and count matches — but combined regex of terms; count = (norm.match(combined)||[]).length. For empty query → 0. Compute lazily per hit when order==='matches'.

Wait, phrase terms combined — a phrase match counts as 1. Fine.

Row rendering details:

Shown text: mode.stored ? rec.text : clean(rec.text). Then truncation: if !mode.full && text.length > 700 → cut at last space ≤ 700 (searching in [600..700]?) — "first 700 cut at a word": take slice(0,700), then cut at last whitespace: `s.slice(0,700).replace(/\s+\S*$/,'')` and append '…'. Hmm ensure not empty. Then "Show the full paragraph (N words)" button. N words = full text word count.

Highlight: apply hlRe to the displayed string (truncated or full). But hlRe over stored text handles [[fn:]] gaps. Over clean text fine too.

Careful: the ellipsis '…' after highlight — fine.

Footnote line: if marks>0 && !mode.stored: `${marks} footnote mark(s) removed · ` + button "show as stored". If mode.stored: button "show as in print (marks removed)". Hmm plan says the link "swaps in the stored text character for character" — toggle. Label when stored: "show as stored" was the label to switch TO stored; to switch back: "hide the footnote marks" / "show as in print". I'll use: clean mode: "3 footnote marks removed · show as stored"; stored mode: "showing the stored text · remove footnote marks".

Wait, careful reading: "a grey line under it says '3 footnote marks removed · show as stored', and that link swaps in the stored text character for character". Yes.

Amber notes (only when applicable):
- leading mismatch: `the text begins “${leading}.” but the record is para. ${paragraph}: check the document`
- lettered: `a lettered sub-paragraph, numbered ${paragraph} by the file`
- dup pinpoint: `two records share this pinpoint`
- joint: `joint General Comment`

Expanded actions:
- Copy citation → copy(citation)
- Copy quotation → copy('"' + quotationText + '" ' + citation)
- Add to draft
- Context: previous | next
- style note: "UN short form" grey note next to citation button area.

Context inline: grey block with pinpoint + text (marks removed), for prev and/or next. "Context: previous | next" link opens paragraph −1 or +1 inline. I'll make each a toggle button; when active shows that paragraph inline. Both could be shown. Keep: clicking "previous" toggles showing prev; "next" toggles next.

Context record: same title, adjacent in paragraph-sorted list. Precompute per title: sorted array; map id → {prev, next}.

Now the copy function:
```
async function copyText(str){
  try{ await navigator.clipboard.writeText(str); copiedMsg(str, true); }
  catch(e){ fallbackBox(str); }
}
```
navigator.clipboard may be undefined (non-secure context) → catch via typeof check.

copiedMsg: live region: "Copied: " + exact string. Show in a status area (fixed at bottom of main? or near top of panel). I'll put a status strip under the tabs (in main), aria-live=polite, showing the message; visually a bordered... thin-ruled area. For long strings, CSS max-height 6em overflow auto.

Fallback: show textarea with str, selected, message "Clipboard refused — select and copy:".

Now checks data structure:
```
function computeChecks(){
  const list=[];
  // 1 query understood
  // 2 totals: rows + brackets
  // 3 chart total
  // 4 highlight
  // 5 normalisation (conditional presence — only add when applicable; hmm "n checks pass" count varies; fine)
  // 6 numbering
  // 7 marks
  // 8 draft
  return list; // {ok:bool, html}
}
```
Header: fails = list.filter(!ok).length; passes = rest. If fails>0: red dot + `${fails} check${s} failed`... plan: "a green dot and 'n checks pass', or a red dot and 'n checks failed'". So when fails: show red + fails count (maybe also passes?). I'll show `${fails} of ${list.length} checks failed`? Plan literally "n checks failed". I'll show "n checks failed" when any fail, else "n checks pass". Good.

Tab 04 content: checks list (each line), then "Known quirks of this file", then "How this is computed" short form.

Let me now also handle the case hits.length===0 on tab 02: message "No paragraphs match." Fine.

Number formatting: fmt = n=>n.toLocaleString('en-US').

Now, CSS. Studio look:
- body: background #f4f0e8, color #1d1b18, font 16px system sans.
- .serif: Georgia etc.
- .mono: ui-monospace... 11-12px uppercase letter-spacing.
- rules: border-top 1px solid #d9d2c3.
- accent #9b2335.
- focus ring: outline 2px solid #9b2335, offset 2.
- [hidden]{display:none!important}
- layout: header, .layout{display:flex}, aside width ~280px, main flex 1, padding.
- tabs: buttons row, mono, active red underline/border.
- rail: sticky? Not necessary.
- big number: 44px serif.
- chips: small bordered mono buttons.
- marks: <mark> background #f5e6a8? Pale yellow, dark text, bold: background:#f7ecc4; color:#1d1b18; font-weight:700.
- badges: outlined mono labels: border 1px solid #d9d2c3... one colour: border-color #1d1b18? "plain outlined monospace labels, one colour" — border #b9ab8f maybe. Keep border: 1px solid #a99e86; color inherit.
- amber notes: color #8a5a00; background transparent; maybe left border amber. Amber colour with contrast: #7a4d00 on #f4f0e8 — contrast? #7a4d00 vs #f4f0e8: should be ≥4.5. Let me use #7a4d00 (dark amber). Also word "amber" conveyed by text content anyway.
- green pass: #1e6b34 (dark green, good contrast).
- red fail: #9b2335.
- pinpoints red: #9b2335, mono.
- rows: article with border-top rule; padding.
- buttons: plain, mono small, border 1px solid #1d1b18 or subtle; hover invert? Keep quiet: border 1px solid #8b8271; background transparent; cursor pointer.
- table: th bottom rule, numbers right aligned, td padding.
- chart container height ~ 10*40+60.

Header layout: flex; left: label + title + source line; right: checks status.

Footer: mono small, top rule.

Responsive: @media max-width 900px: rail becomes full width above main (flex-wrap). OK.

Now, arrow-key on tablist; roving tabindex.

Let me think about how render is organized to avoid clobbering focus: full re-render on updates replaces DOM — focus lost if focus inside panel (e.g., clicking a checkbox re-renders rail → focus lost from checkbox?). To preserve, I can re-focus the element by id/key after render, or do fine-grained updates. Simplest: after re-render, restore focus/scroll: record document.activeElement's id or data-key before replacing, then refocus. And preserve scroll position. Let me implement a small helper: capture activeElement id + selection; after render, find same id, focus, restore selection.

Rail re-renders on: search, filter changes. Checkbox click → update → rail rebuilt → refocus the checkbox by id (`cb-CRC`). Input focus: search input is re-rendered? If I re-render the whole rail each update, the search input would be rebuilt and focus lost while typing... but search only applies on Enter/button, and typing only closes dropdown. Focus in input: re-render triggered by checkbox clicks, not typing. But input value: keep state.rawQueryInput and set value on render. Careful: re-render on "Search" click: input re-created — refocus it. OK, my refocus helper handles this.

Alternatively, keep static rail DOM and update pieces. That's cleaner: build rail once; update numbers/brackets/chips via targeted updates. Let me do that:
- big number element updated.
- chips container rebuilt (small).
- bracket spans updated (keep references).
- echo line updated.
- error line.
- doc/year/committee inputs static (values changed by user or clear-all).
- "Clear all" resets input values too.

Yes — build rail once, targeted updates. Main panels re-rendered per update (fine, focus in panels: clicking row buttons triggers update? Copy buttons don't change state → no re-render. Add to draft → draft count changes → tab label updates (targeted) and if draft tab active re-render; row can stay. "Show 25 more" → re-render records panel; button disappears anyway. Row expand toggles → re-render panel (focus was on row toggle button → restore by data-id). OK, refocus helper still useful. Let me implement focus restore: before render, note activeElement's [data-ref] attribute; after render, querySelector same [data-ref] and focus. I'll add data-ref to interactive elements: row toggles (`row-<id>`), show-more button, order select, row buttons. Hmm, that's a lot of bookkeeping. Alternative: for row expansion, do targeted DOM updates instead of full re-render... 

Simpler approach: expansion toggling via class toggling + building the expanded content lazily:
- Rows built once per records render; expansion handled by re-building just that article (replaceWith) and refocusing its toggle button.

Let me structure records rendering:
```
function renderRecords(){
  const container=el('#rec-list'); container.innerHTML='';
  const page=hits.slice(0,state.shown);
  page.forEach(rec=>container.appendChild(buildRow(rec)));
  // show more button
}
function buildRow(rec){ ... returns article; toggle handler replaces article with rebuild (buildRow(rec) again, reading current mode) ... }
```
Row-internal state (mode, context) stored in state maps keyed by id, so rebuild is deterministic. Buttons inside row: event delegation or per-row listeners — per-row listeners fine.

Order select changes → full renderRecords.

OK. For "Show 25 more": state.shown += 25; renderRecords; focus back to the button? Button gone/repositioned; acceptable, or keep focus on it if still present. I'll try refocus by data-ref.

Focus restore helper: 
```
function keepFocus(fn){
  const a=document.activeElement; const ref=a&&a.dataset? a.dataset.ref:null; const pos=a&&a.selectionStart;
  fn();
  if(ref){const n=document.querySelector(`[data-ref="${CSS.escape(ref)}"]`); if(n){n.focus(); try{if(pos!=null)n.setSelectionRange(pos,pos)}catch(e){}}}
}
```
Use for renderRecords etc. Add data-ref to order select, show-more, row toggles. Minor.

Now the syntax dropdown behaviour:
- input#q, on focus: if value==='' → open list.
- on input: if value → close; else keep open? "it closes when typing starts" — close on input event with non-empty value; if user deletes back to empty... keep closed until re-focus. I'll close on any input.
- examples: mousedown → preventDefault (keep focus), fill+run.
- Escape closes.
- ArrowDown from input → focus first example.

Examples list content:
```
How to search:
· a space or AND joins words
· OR, NOT, or a leading - to exclude
· "an exact phrase" in double quotes
· parentheses group
· a star at the end of a word matches any ending (child* finds children)
· operators in capitals — lower-case "or" is a word

Try:
"best interests" AND child
(torture OR ill-treatment) NOT detention
"reasonable accommodation"
```

Under-box line (always visible under input):
"Whole words, any case. Curly and straight quotes, apostrophes, dashes and hyphens count as the same, and footnote marks are skipped, so State's finds State’s and a phrase can cross a footnote."

Now committee full names:
```
const CMTY={
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
CMW full name is long; use "Committee on Migrant Workers" (short). OK.

These are facts about the treaty bodies — well-known, safe.

Now the checks panel — "open" by default on tab 04. Fine, it's the tab content.

Header line: "7,304 paragraphs from 159 General Comments of 10 committees, 1972–2026" — with source linked. Note: title says distinct `title` counts "General Comments" — 188 distinct titles but "159 distinct symbol"... plan: "n General Comments (distinct title) of k committees". Use distinct titles count, distinct committees count (from committee field? or committees sets? Use distinct committee field values + symbol codes... I'll use union of all committees sets — that gives 10 including CAT-OP).

Hmm wait, "of k committees" — union over records of _committees. That's 10. Good.

Edge: data may differ from described (7,304 etc.) — all computed.

Now write "How this is computed" short form (tab 04):
- Matching: text normalised (footnote marks removed; curly quotes, apostrophes and dashes as their straight forms; one space; lower case); the query the same way; whole words, star endings.
- Hits: Boolean tree true AND committee/year/document filters pass.
- Order: year desc, document, paragraph — or as chosen.
- Citation: symbol + pinpoint from the record's fields; shared symbols prefixed with committee and document name; style: UN short form (Dag Hammarskjöld Library).
- Quotation: stored text, footnote marks removed, leading number dropped when it matches the record's paragraph.
- Counting done by this page; no model called.

Known quirks list items with counts and examples.

Now — one more detail from plan: tab 02 hint "This page retrieves; it never writes..." — include.

Also plan: "Every matched word or phrase is wrapped in <mark> (bold, pale yellow, dark text)."

Also the header checks status is computed... when? updateChecks after each update. But checks referencing DOM rows (totals check) require records panel rendered — only when tab 02 active. If another tab active, rows check... The check "Rows listed across pages equal the hits" — when tab 02 not active, no rows listed. Hmm. I'll compute this check only when records panel is in DOM; otherwise state it as counts: "Rows listed (25) + remaining (254) = 279 hits" computed arithmetically from state. That always holds. To make it a real check, verify DOM when present: rendered = container ? container.children.length (rows) : min(shown, hits). I'll do that.

Let me also double check the "bracketed counts sum" when q.error: hits=0, brackets 0, sum 0 = 0+0 ✓.

Now, potential subtle issue: committee checkboxes "all ticked" default. The Set of ticked codes — initialize to all codes found. Committee list order: by total records desc (over R, counting per committee via _committees? or via committee field?). I'll count via _committees union (each record counts once per committee) — matches bars when no filter. Order bars and checkboxes the same way.

Hmm, wait: with default all-ticked, hits=R (empty query), bars = per-committee counts over R via _committees — CRC 2,091 per the file description. Good.

Now the document select: options = all distinct titles grouped by committee field. 188 options. Fine. Value = title (string). Use index? title strings contain quotes — as option value attribute fine. I'll use title as value directly.

But wait — should the doc select only show documents passing other filters? Keep all, simpler.

Chip for doc: "GC 23 …" — show short_title truncated.

Now "Clear all" button in rail header.

Draft persistence: localStorage key. On load: try parse. Items: {id, citation, symbol, paragraph, pinpoint, committee, short_title, year, text_copied, text_as_stored, doc_url}.

text_copied = quotation text WITHOUT surrounding quotes (so CSV has it clean); copy-time adds quotes. Plan CSV column 'text_copied' — the shown text copied. I'll store without quote marks; quotation copy adds "…". Copy all: `"${text_copied}"\n${citation}`.

Hmm wait — "Copy quotation copies the shown text in quotation marks, a space, the citation": `"text" citation` — same line: `"…" CCPR/C/GC/37, para. 12`. Yes with space.

Draft item display: quotation in quotes + citation.

Now, "Add to draft" when already there: live message "Already in the draft." plus maybe still switch? Keep message.

Tab label: `03 DRAFT (n)`.

Draft tab content when empty: "Your draft is empty. Add quotations from the Paragraphs tab." Plus hint about storage: "Kept in this browser's localStorage when allowed; in memory otherwise." Determine mode: try localStorage set/get test at load.

Now, code size: Let me estimate. This will be ~1,100-1,400 lines. Acceptable (under 1,500).

Let me now also design HTML skeleton:

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Verbatim finder: General Comments and General Recommendations</title>
<style> ... </style>
</head>
<body>
<header class="site-head">
  <div class="head-left">
    <p class="mono label">UN TREATY BODIES · GENERAL COMMENTS</p>
    <h1>Verbatim finder: <span>General Comments and General Recommendations</span></h1>
    <p class="mono source-line" id="head-line">…</p>
  </div>
  <div class="head-right mono" id="head-checks"></div>
</header>
<div class="layout">
  <aside class="rail" id="rail">
    <div class="rail-head mono">FILTERS <button id="clear-all">Clear all</button></div>
    <div class="bignum-wrap">
      <p class="bignum" id="big-num" aria-live="polite">7,304</p>
      <p class="bigsub">matching paragraphs</p>
      <p class="mono of">of 7,304</p>
    </div>
    <div id="chips" class="chips"></div>
    <div class="search">
      <label class="mono" for="q">SEARCH</label>
      <div class="search-row">
        <input id="q" type="text" autocomplete="off" spellcheck="false" placeholder='e.g. "best interests" AND child*'>
        <button id="q-go">Search</button>
      </div>
      <div id="syntax" class="syntax mono" hidden> ... </div>
      <p class="normline mono">Whole words, any case. ...</p>
      <p class="echo" id="echo" aria-live="polite"></p>
    </div>
    <div class="acc">
      <button class="acc-btn mono" id="acc-btn" aria-expanded="false" aria-controls="acc-panel">
        <span class="num">01</span> COMMITTEE, YEARS, DOCUMENT
      </button>
      <div class="acc-panel" id="acc-panel" hidden>
        <fieldset> committee checkboxes + all/none </fieldset>
        <fieldset> years </fieldset>
        <fieldset> doc select </fieldset>
      </div>
    </div>
  </aside>
  <main class="main">
    <div class="tabs mono" role="tablist" aria-label="Sections">
      <button role="tab" id="tab-1" aria-controls="panel-1" aria-selected="true">01 OVERVIEW</button>
      <button role="tab" id="tab-2" ...>02 PARAGRAPHS</button>
      <button role="tab" id="tab-3" ...>03 DRAFT (<span id="draft-n">0</span>)</button>
      <button role="tab" id="tab-4" ...>04 CHECK &amp; METHOD <span class="dot" id="tab4-dot" hidden></span></button>
    </div>
    <p class="copystatus mono" id="copystatus" aria-live="polite"></p>
    <div id="fallback-copy" class="fallback" hidden>
      <p class="mono">Clipboard refused — select and copy:</p>
      <textarea id="fallback-text" readonly></textarea>
    </div>
    <section role="tabpanel" id="panel-1"> ... FIG.01 ... </section>
    <section role="tabpanel" id="panel-2" hidden> summary, order, list </section>
    <section role="tabpanel" id="panel-3" hidden> draft </section>
    <section role="tabpanel" id="panel-4" hidden> checks, quirks, method </section>
  </main>
</div>
<footer class="mono" id="foot"> ... </footer>
<script> ... </script>
</body>
</html>
```

Panels 1's chart: canvas inside; chart instance destroyed/recreated on updates when panel visible.

Wait — Chart.js needs canvas in DOM & visible to size properly. Overview is default tab. When switching to overview, re-render chart. I'll (re)build chart whenever panel-1 becomes active or update() runs while active.

Let me write the tab switching:
```
function setTab(i){ state.tab=i; tabs update aria-selected; panels hidden; rail hidden if tab 3; if(i===1) buildChart(); if(i===4) renderChecksPanel(); if(i===2) renderRecords(); if(i===3) renderDraft(); }
```
And update() also refreshes active panel.

Default tab: 1 (Overview).

Now, checks panel content is stored in state.checks (computed each update); render on tab open. Also header line updated.

Known quirks computed once at load (static): stored in `quirks` array of strings (with counts/examples).

Now implement everything in JS carefully.

Let me draft the JS:

```js
(function(){
'use strict';
const D=window.WORKSHOP_DATA&&window.WORKSHOP_DATA.gc;
if(!D||!D.records){document.getElementById('head-line').textContent='No data loaded.';return;}
const R=D.records;
const $=s=>document.querySelector(s);
const fmt=n=>n.toLocaleString('en-US');
const esc=s=>String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');

// ---- precompute
const FN_RE=/\[\[fn:\d+\]\]/g;
function normText(s){
  return s.replace(FN_RE,'')
    .replace(/[\u201C\u201D\u201E]/g,'"')
    .replace(/[\u2018\u2019\u201A]/g,"'")
    .replace(/[\u2013\u2014\u00AD]/g,'-')
    .replace(/\s+/g,' ')
    .toLowerCase();
}
```
Wait — order issue: FN_RE is a global regex reused with .replace — global regexes with replace reset lastIndex? String.replace with /g resets? Actually String.prototype.replace with a global regex resets lastIndex to 0 after completion... It sets lastIndex during but ends at 0? Per spec, replace with global flag sets lastIndex to 0 before starting. Yes, RegExp.prototype[Symbol.replace] sets lastIndex=0 when global. Safe.

But normText also used for query. Also test with .test on global regexes — I avoid .test on global regexes (or reset). For matchers I create non-global regexes.

```
const CMTY_FULL={...};
const CODE_RE=/\b(CAT|CCPR|CED|CEDAW|CERD|CESCR|CMW|CRC|CRPD)\b/g;
function recCommittees(sym, committee){
  const s=new Set();
  if(sym && /CAT\/OP/.test(sym)) s.add('CAT-OP');
  else if(sym){const m=sym.match(CODE_RE); if(m) for(const c of m) s.add(c);}
  if(committee) s.add(committee);
  return s;
}
```
Note: CODE_RE is global; .match with global returns all matches, safe.

Hmm: "CAT/OP" check — but also the committee field might be "CAT-OP" while symbol "CAT/OP/..." — both add CAT-OP. But should a CAT/OP record ALSO count under CAT? I decided no (else branch). Hmm wait — but actually, what about symbols like "CAT/C/..."? \bCAT\b matches → CAT. Fine.

Per record:
```
R.forEach(r=>{
  r._norm=normText(r.text||'');
  r._marks=(r.text||'').match(/\[\[fn:\d+\]\]/g)||[]).length;  // careful syntax
  const lm=(r.text||'').match(/^(\d{1,3})\.\s/);
  r._leading=lm?parseInt(lm[1],10):null;
  r._committees=recCommittees(r.symbol,r.committee);
  r._joint=r._committees.size>=2 || /–/.test(r.symbol||'') && ... 
```
Hmm — joint detection. "Three joint General Comments carry two symbols in one symbol". committees.size>=2 happens exactly for these (symbol with two codes). But wait — could a record have committee field CESCR and symbol "E/C.12/..." → committees={CESCR}, size 1. Joint ones: symbol "CMW/C/GC/7–CERD/C/GC/38" → codes {CMW,CERD} + committee (one of them) → size 2. But also — could there be a symbol containing two codes that's NOT joint? E.g., "CRC/C/GC/23, CMW/C/GC/4" is joint. I think committees.size>=2 is the joint test. Hmm, but wait: what about CAT/OP records where I add only CAT-OP? size 1. OK: r._joint = [...r._committees].length>=2? But careful: is committee field ever different from symbol codes for non-joint? E.g., symbol "A/53/44" (CAT GC1) with committee "CAT" — codes from symbol: CAT; plus committee CAT → {CAT}. Good. Symbol "A/HRC/..."? not in gc. CED symbol "C/CED/..."? committee CED → {CED}.

Hmm — but CESCR early GCs: symbol "E/C.12/..." committee CESCR → {CESCR}. Good.

But here's a risk: some symbol might contain e.g. "CRC" and committee "CRC" → 1. What about "CCPR/C/21/Rev.1/Add.4" hmm wait, what about symbols containing 'CED' inside 'CEDAW'? \b prevents. OK.

But one more: the joint "CMW/C/GC/7–CERD/C/GC/38" — en dash between. Also possible committee field might be "CMW" or "CERD" or something like "CMW/CERD"? The plan says "but one committee". So _committees = {CMW, CERD} + committee field (one of them, or maybe written differently). If committee field were e.g. "CMW-CERD"... unlikely. I'll also guard: if committees.size>=2 → joint.

Wait, actually careful: what if committee field = "CAT-OP" and symbol = "CAT/OP/SC/..."? My else-branch adds only CAT-OP; committee adds CAT-OP; size 1, not joint. 

Hmm, but one more subtle thing: is it possible that a symbol matches a code AND committee is a different code, making size 2 but not joint? E.g., SPT documents published under CAT symbol with committee "CAT-OP" — handled. I'll accept the heuristic.

```
  r._pin=pinpoint(r);
  r._shared=false; // set below
  r._dup=false;
  r._sub=r._lettered? ... 
```
Let me store: r._lettered = match of /^\(([a-z]{1,4})\)/ → label.
r._pin: as described.

Shared symbols:
```
const symTitles=new Map();
R.forEach(r=>{ if(!symTitles.has(r.symbol)) symTitles.set(r.symbol,new Set()); symTitles.get(r.symbol).add(r.title); });
R.forEach(r=>{ r._shared=symTitles.get(r.symbol).size>1; r._citation=citation(r); });
```
citation uses _shared and _pin — compute after.

Dup pinpoints:
```
const pinKeys=new Map();
R.forEach(r=>{const k=r.title+'||'+r.paragraph; pinKeys.set(k,(pinKeys.get(k)||0)+1);});
R.forEach(r=>{ r._dup=pinKeys.get(r.title+'||'+r.paragraph)>1; });
```
Hmm — "Two pinpoints occur twice (CEDAW/C/GC/27 para. 9; the joint GR 31/GC 18 para. 31)." Same title+paragraph → the joint one: title is one per record... The joint record's title — probably the same title for both para-31 records? The plan says "hits that share a pinpoint with another record of the same title". OK my key is title+paragraph. Good.

Context neighbours:
```
const byTitle=new Map();
R.forEach(r=>{ if(!byTitle.has(r.title)) byTitle.set(r.title,[]); byTitle.get(r.title).push(r); });
byTitle.forEach(a=>a.sort((x,y)=>x.paragraph-y.paragraph));
const ctx=new Map();
byTitle.forEach(a=>{ a.forEach((r,i)=>ctx.set(r.id,{prev:a[i-1]||null,next:a[i+1]||null})); });
```

Years min/max:
```
const years=R.map(r=>r.year); const YMIN=Math.min(...years); const YMAX=Math.max(...years);
```
Math.min with 7304 args — spread might be OK (limit ~65k). Fine. Or reduce. Use reduce to be safe.

Distinct titles, committees:
```
const titles=new Set(R.map(r=>r.title));
const allCodes=new Set(); R.forEach(r=>r._committees.forEach(c=>allCodes.add(c)));
```

Committee order by count over R via _committees:
```
const cCounts={}; R.forEach(r=>r._committees.forEach(c=>cCounts[c]=(cCounts[c]||0)+1));
const CORDER=Object.keys(cCounts).sort((a,b)=>cCounts[b]-cCounts[a]);
```

Quirks at load:
```
const quirks=[];
const p0=R.filter(r=>r.paragraph===0);
if(p0.length) quirks.push(`${fmt(p0.length)} records are preambles (paragraph 0), cited as “preamble” — e.g. ${p0[0].symbol}.`);
const sharedSyms=[...symTitles].filter(([s,t])=>t.size>1);
if(sharedSyms.length) quirks.push(`${sharedSyms.length} symbols hold more than one General Comment (e.g. ${sharedSyms[0][0]}, ${sharedSyms[0][1].size} titles); citations name the document.`);
const jointRecs=R.filter(r=>r._joint);
if(jointRecs.length) quirks.push(`${fmt(jointRecs.length)} paragraphs belong to joint General Comments with two symbols (e.g. ${jointRecs[0].symbol}); they count under both committees.`);
const dupRecs=R.filter(r=>r._dup);
if(dupRecs.length) quirks.push(`${fmt(dupRecs.length)} records share their pinpoint with another record of the same document (e.g. ${dupRecs[0].symbol}, para. ${dupRecs[0].paragraph}); the row is flagged.`);
const leadMis=R.filter(r=>r._leading!=null&&r._leading!==r.paragraph);
if(leadMis.length) quirks.push(`${fmt(leadMis.length)} records whose text begins with a number that differs from the record’s paragraph (e.g. ${leadMis[0].symbol}: text begins “${leadMis[0]._leading}.”, record para. ${leadMis[0].paragraph}); both are shown, nothing corrected.`);
const subRecs=R.filter(r=>r._lettered);
if(subRecs.length) quirks.push(...)
```
Plan lists five quirks (p0, shared, joint, dup, leading). I'll include lettered too? The plan: "records with paragraph 0, symbols shared by several documents, joint documents, duplicated pinpoints, leading-number mismatches, each with its count and an example." I'll stick to the five listed... adding lettered is harmless but plan says "where it says nothing, keep it simple" — stick to five.

Query parsing:

```js
function tokenize(q){
  const toks=[];let i=0;
  const OPEN='"\u201C\u201D';
  while(i<q.length){
    const c=q[i];
    if(/\s/.test(c)){i++;continue;}
    if(c==='('||c===')'){toks.push({t:c});i++;continue;}
    if(OPEN.indexOf(c)>-1){
      let j=i+1,b='';
      while(j<q.length&&OPEN.indexOf(q[j])<0){b+=q[j];j++;}
      if(j>=q.length)throw{msg:'unbalanced quote — a closing double quote is missing'};
      if(!b.trim())throw{msg:'empty phrase — put words between the quotes'};
      toks.push({t:'P',v:b});i=j+1;continue;
    }
    let j=i,b='';
    while(j<q.length&&(!/[\s()]/.test(q[j]))&&OPEN.indexOf(q[j])<0){b+=q[j];j++;}
    if(!b){i++;continue;}
    if(b==='AND'||b==='OR'||b==='NOT'){toks.push({t:b});}
    else if(b.length>1&&b[0]==='-'){toks.push({t:'NOT'});toks.push({t:'W',v:b.slice(1)});}
    else if(b==='-'){throw{msg:'a lone “-” — put the word to exclude after it'};}
    else toks.push({t:'W',v:b});
    i=j;
  }
  return toks;
}
```
Hmm — a word could contain '-' not at start, e.g., "ill-treatment" — fine, it's just a word. Also a word token could start with '-' where '-' is a hyphenated... " -something". OK.

Wait — what about '-' at start of a phrase-word inside quotes? Phrases captured raw; words inside phrase handled by phrase logic.

Parser:

```js
function parse(q){
  const toks=tokenize(q);
  if(!toks.length)throw{msg:'empty query'};
  let p=0;
  function peek(){return toks[p];}
  function parseOr(){
    let l=parseAnd();
    while(peek()&&peek().t==='OR'){p++;const r=parseAnd();l={k:'OR',l,r};}
    return l;
  }
  function parseAnd(){
    let l=parseNot();
    while(true){
      const t=peek();
      if(!t||t.t==='OR'||t.t===')')break;
      if(t.t==='AND'){p++;const n=peek();if(!n||n.t===')'||n.t==='OR')throw{msg:'AND with no following term'};}
      const r=parseNot();l={k:'AND',l,r};
    }
    return l;
  }
  function parseNot(){
    let neg=false;
    while(peek()&&peek().t==='NOT'){p++;neg=!neg;}
    const v=parsePrim();
    return neg?{k:'NOT',v}:v;
  }
  function parsePrim(){
    const t=peek();
    if(!t)throw{msg:'a term is missing (operator or parenthesis with nothing after it)'};
    if(t.t==='('){p++;const n=parseOr();const c=peek();if(!c||c.t!==')')throw{msg:'unbalanced parenthesis — a “)” is missing'};p++;return n;}
    if(t.t===')')throw{msg:'unexpected “)”'};
    if(t.t==='AND'||t.t==='OR')throw{msg:t.t+' with no term before it'};
    if(t.t==='NOT')throw{msg:'NOT with no term'}; // handled in parseNot; unreachable
    p++;
    return t.t==='P'?{k:'PH',v:t.v}:{k:'WD',v:t.v};
  }
  const tree=parseOr();
  if(p<toks.length)throw{msg:'unexpected “)”'};
  return tree;
}
```
Hmm, NOT with no term: parseNot loop consumes NOT tokens then parsePrim throws 'a term is missing'. Fine.

Wait, in parseAnd: if next token is AND consume and parse next; but if next token is ')' or end after AND → error. Also if next is a term → implicit AND. But careful: if next token is 'NOT' → implicit AND with NOT-term — parseNot handles. Good. If next is '(' → parseNot→parsePrim handles '('. Good. If next is 'AND' handled. If next is 'OR' → break (handled by while condition). Wait, after consuming AND, if next is OR → error thrown (AND then OR). OK.

Edge: query "NOT" alone → parseNot: neg=true, parsePrim: no token → throw 'a term is missing'. Good.

Edge: '-word' at start: tokenize gives NOT, W(word) → parseNot → NOT(word). Root NOT → notOnly.

Now matching compile:

```js
function escRe(s){return s.replace(/[.*+?^${}()|[\]\\]/g,'\\$&');}
function normWord(w){return normText(w);}
const B0='(?<![\\p{L}\\p{N}])', B1='(?![\\p{L}\\p{N}])';
function wordBody(w,hl){ // w raw word possibly with trailing *
  let star=false;
  if(w.endsWith('*')){star=true;w=w.slice(0,-1);}
  let out='';
  for(const ch of w){
    if(hl){
      if(ch==='"'){out+='[\u201C\u201D"]';continue;}
      if(ch==="'"){out+='[\u2018\u2019\']';continue;}
      if(ch==='-'){out+='[-\u2013\u2014]';continue;}
    }
    out+=escRe(ch);
  }
  if(star)out+='\\w*';
  return out;
}
```
Hmm wait: for the norm match (hl=false), the word itself is normalised first (curly→straight, lowercased). Actually simpler: build match regex from normText(word) with hl=false; build highlight regex from raw word with hl=true (case-insensitive flag). But the raw word may contain uppercase — 'i' flag handles.

Wait, subtle: normText of word collapses whitespace — words have none. normText lowercases and normalises quotes — so match regex body uses normalised chars (straight, hyphen). For highlight, map each char of the raw word to variant classes. But raw word might have curly quotes — map anyway (class includes them). Fine.

But careful with '*': normText doesn't remove '*'. trailing '*' detected before.

```
function termMatcher(node){ // returns {test(s)->bool, re}
  if(node.k==='WD'){
    const re=new RegExp(B0+wordBody(normText(node.v),false)+B1,'u');
    return s=>re.test(s);
  }
  // PH
  const words=node.v.trim().split(/\s+/).map(w=>normText(w));
  const re=new RegExp(B0+words.map(w=>wordBody(w,false)).join('\\s+')+B1,'u');
  return s=>re.test(s);
}
```
Wait — phrase words: can a phrase word end with '*'? "an exact phrase" — star support optional; wordBody handles trailing * anyway if present. Fine.

Compile tree to predicate with caching per node (WeakMap or attach _fn):

```js
function compile(node){
  switch(node.k){
    case 'WD':case 'PH':{ if(!node._fn) node._fn=termMatcher(node); return node._fn;}
    case 'AND':{const l=compile(node.l),r=compile(node.r);return s=>l(s)&&r(s);}
    case 'OR':{const l=compile(node.l),r=compile(node.r);return s=>l(s)||r(s);}
    case 'NOT':{const v=compile(node.v);return s=>!v(s);}
  }
}
```

Echo:
```js
function echoNode(n){
  switch(n.k){
    case 'WD':return n.v.endsWith('*')?('any word ending “'+n.v.slice(0,-1)+'”'):('the word “'+n.v+'”');
    case 'PH':return 'the phrase “'+n.v.trim()+'”';
    case 'AND':return echoNode(n.l)+' and '+echoNode(n.r);
    case 'OR':return echoNode(n.l)+' or '+echoNode(n.r);
    case 'NOT':return 'not '+echoNode(n.v);
  }
}
function echoLine(tree){
  if(tree.k==='NOT')return 'Paragraphs not containing '+echoNode(tree.v)+' — that is, every paragraph that lacks these terms.';
  return 'Paragraphs containing '+echoNode(tree);
}
```
Plan example: "Paragraphs containing the phrase “best interests” and the word child" — without quotes around child in their example, but quotes are clearer. Fine.

Terms collection:
```js
function collectTerms(n,neg,out){
  if(!n)return;
  if(n.k==='WD'||n.k==='PH'){if(!neg)out.push(n);return;}
  if(n.k==='NOT'){collectTerms(n.v,!neg,out);return;}
  collectTerms(n.l,neg,out);collectTerms(n.r,neg,out);
}
```
Count terms: number of WD/PH nodes total (for "the number of terms" in check). Count all terms incl. under NOT: walk all.

Highlight regex:
```js
function buildHlRe(terms){
  if(!terms.length)return null;
  const alts=terms.map(t=>{
    if(t.k==='WD')return wordBody(t.v,true); // raw word, variant classes
    const ws=t.v.trim().split(/\s+/);
    return ws.map(w=>wordBody(w,true)).join('(?:\\s|\\[\\[fn:\\d+\\]\\])+');
  });
  return new RegExp('(?:'+alts.join('|')+')','giu');
}
```
Wait — wordBody with hl=true on raw word: trailing star handled inside. But raw word chars like '.' escaped. Good. Note: word boundaries — should the highlight regex also have boundaries? Yes: "The same terms become a second regular expression" with same boundary semantics. Add B0/B1 around each alternative:
alt = B0+body+B1 for words; phrases: B0+joined+B1.

Hmm — but B0/B1 with lookbehind on each alt is fine.

One concern: 'giu' flags with \w* and \s — fine. Lookbehind supported in modern browsers (sandbox presumably Chromium). OK.

Highlight function:
```js
function highlightInto(str,re){
  if(!re)return esc(str);
  re.lastIndex=0;
  let out='',last=0,m;
  while((m=re.exec(str))){
    out+=esc(str.slice(last,m.index))+'<mark>'+esc(m[0])+'</mark>';
    last=m.index+m[0].length;
    if(m[0].length===0)re.lastIndex++;
  }
  return out+esc(str.slice(last));
}
```
Global regex exec loop with lastIndex — since I reuse re across rows, reset lastIndex at start. Zero-length matches guarded.

Now state:

```js
const state={
  tab:1,
  rawQ:'',
  q:null, // {tree,echo,terms,notOnly,err}
  ticked:new Set(CORDER),
  yFrom:YMIN, yTo:YMAX,
  doc:'',
  order:'year',
  shown:25,
  open:new Set(), // open row ids
  mode:new Map(), // id -> {stored:bool,full:bool}
  ctx:new Set(), // ids with context open (store 'id:prev'/'id:next')
  draft:[],
  storage:'memory'
};
```

computeHits:
```js
function computeHits(){
  if(state.q&&state.q.err)return [];
  const pred=state.q?compile(state.q.tree):null;
  const t=state.ticked;
  return R.filter(r=>{
    if(pred&&!pred(r._norm))return false;
    let ok=false;
    for(const c of r._committees){if(t.has(c)){ok=true;break;}}
    if(!ok)return false;
    if(r.year<state.yFrom||r.year>state.yTo)return false;
    if(state.doc&&r.title!==state.doc)return false;
    return true;
  });
}
```

Order:
```js
function orderHits(hits){
  const byYear=(a,b)=>(b.year-a.year)||a.title.localeCompare(b.title)||((a.paragraph||0)-(b.paragraph||0));
  if(state.order==='doc')return hits.slice().sort((a,b)=>a.title.localeCompare(b.title)||((a.paragraph||0)-(b.paragraph||0)));
  if(state.order==='matches'&&state.q&&state.q.termsReNorm){
    const re=state.q.termsReNorm; // global combined over norm
    const cnt=r=>{re.lastIndex=0;const m=r._norm.match(re);return m?m.length:0;};
    return hits.slice().sort((a,b)=>cnt(b)-cnt(a)||byYear(a,b));
  }
  return hits.slice().sort(byYear);
}
```
termsReNorm: combined norm regex (global) built from terms: alts of wordBody(norm,false) joined. Build when q set.

Per-committee counts over hits:
```js
function countsByCommittee(hits){
  const c={};CORDER.forEach(k=>c[k]=0);
  let extra=0;
  hits.forEach(r=>{r._committees.forEach(k=>{if(c[k]!=null)c[k]++;});extra+=r._committees.size-1;});
  return {c,extra};
}
```
Hmm extra counts committees beyond first — for joint (size 2) extra=1. But what if some record has committees size 2 not joint (shouldn't happen)? Fine.

Wait — but extra should only count committees that are in CORDER (all are). If a record's committee set has codes not in CORDER (impossible, CORDER built from all). OK.

Update pipeline:

```js
let hits=[],ordered=[];
function update(){
  hits=computeHits();
  ordered=orderHits(hits);
  updateRail();
  renderPanel();
  runChecks();
}
```
renderPanel renders the active tab panel.

updateRail: big number, of, chips, brackets, echo, error.

Brackets: spans per committee: `#cnt-CRC`.

Echo area: if state.q null: if rawQ empty → hide. If q.err → red error text. Else echo line.

Chips:
- committees: if ticked.size!==CORDER.length → chip label `Committees: ${list} (${ticked.size} of ${CORDER.length})`, remove → tick all.
- years: if yFrom>YMIN||yTo<YMAX → `Years ${yFrom}–${yTo}`, remove → reset.
- doc: if doc → `Document: ${short_title}`, remove → ''.

renderPanel switch:
- 1: buildChart + table + notes (update numbers).
- 2: renderRecords.
- 3: renderDraft.
- 4: renderChecks.

Panel 1 content (static skeleton in HTML, dynamic numbers): I'll build it in HTML with ids: fig table body, chart canvas, aria-label, computed line, chart total line.

Chart building:
```js
let chart=null;
function buildChart(){
  const {c,extra}=countsByCommittee(hits);
  const labels=CORDER.slice().sort((a,b)=>c[b]-c[a]); // ranked
  const data=labels.map(k=>c[k]);
  // aria label
  const cv=$('#chart');
  cv.setAttribute('aria-label','Paragraphs per committee: '+labels.map((l,i)=>l+' '+fmt(data[i])).join('; ')+'.');
  if(chart){chart.destroy();chart=null;}
  chart=new Chart(cv.getContext('2d'),{...});
  // table
  tbody rows...
  $('#chart-note-total').textContent=...
}
```
Chart onClick:
```js
onClick:(e,els)=>{
  if(!els.length)return;
  const idx=els[0].index;
  const c=labels[idx];
  state.ticked=new Set([c]);
  update();
}
```
labels captured in closure — rebuild chart each update anyway.

Value plugin:
```js
const valuePlugin={id:'valueAtEnd',afterDatasetsDraw(chart){
  const {ctx}=chart;const meta=chart.getDatasetMeta(0);
  ctx.save();ctx.font='12px ui-monospace, Menlo, Consolas, monospace';ctx.fillStyle='#1d1b18';ctx.textAlign='left';ctx.textBaseline='middle';
  meta.data.forEach((bar,i)=>{
    const v=chart.data.datasets[0].data[i];
    ctx.fillText(fmt(v),bar.x+6,bar.y);
  });
  ctx.restore();
}};
```

Chart options: x max maybe add padding so labels fit: suggestedMax = max*1.12.

Scales:
```
x:{beginAtZero:true,grid:{color:'#e7e0d1'},ticks:{maxTicksLimit:10,font:{family:'ui-monospace, Menlo, Consolas, monospace',size:11},color:'#4a453d'}}
y:{grid:{display:false},ticks:{font:{family:...},color:'#1d1b18'}}
```
barThickness or categoryPercentage: "gaps narrower than a bar": barPercentage:0.85, categoryPercentage:0.9.

Chart container: position relative, height: labels.length*44+40 px? Set style.height dynamically: (labels.length*44+50)+'px'.

renderRecords:

```js
function renderRecords(){
  const listEl=$('#rec-list');
  // summary
  const cs=new Set();hits.forEach(r=>r._committees.forEach(c=>cs.add(c)));
  let y1=null,y2=null;hits.forEach(r=>{y1=y1===null?r.year:Math.min(y1,r.year);y2=y2===null?r.year:Math.max(y2,r.year);});
  let sum;
  if(state.q&&state.q.err)sum=`Search not understood — ${state.q.err}. Nothing is listed.`;
  else{
    sum=`${fmt(hits.length)} of ${fmt(R.length)} paragraphs match`;
    if(!state.q)sum+=' (no search words)';
    if(hits.length)sum+=` · ${cs.size} committees · ${y1}–${y2}`;
  }
  $('#rec-summary').textContent=sum;
  // order line + select value
  ...
  listEl.innerHTML='';
  const page=ordered.slice(0,state.shown);
  page.forEach(r=>listEl.appendChild(buildRow(r)));
  // more button
  const more=$('#rec-more');
  if(ordered.length>state.shown){more.hidden=false;more.textContent=`Show 25 more (${fmt(ordered.length-state.shown)} remaining)`;}
  else more.hidden=true;
}
```

buildRow(rec):
```js
function buildRow(r){
  const art=document.createElement('article');
  art.className='row';art.dataset.id=r.id;
  const m=state.mode.get(r.id)||{stored:false,full:false};
  const open=state.open.has(r.id);
  // badges
  const badges=[...r._committees].map(c=>`<span class="badge">${esc(c)}</span>`).join(' ');
  ...
}
```
Full construction with innerHTML then attach listeners via delegation on list container? Delegation once on #rec-list: click handler:
- find closest('button,a,input,label') — if a/button with own handler... Let me use delegation with data-act attributes:
  - row toggle: click on article not on [data-act] or a → toggle open.
  - buttons: data-act="cite"|"quote"|"draft"|"stored"|"full"|"ctx-prev"|"ctx-next".
  
Delegation on listEl:
```js
listEl.addEventListener('click',e=>{
  const b=e.target.closest('[data-act]');
  if(b){const art=b.closest('article.row');const r=byId.get(art.dataset.id);doAct(b.dataset.act,r,b);return;}
  if(e.target.closest('a'))return;
  const art=e.target.closest('article.row');
  if(art){toggleOpen(art.dataset.id);}
});
```
But the h3 button toggle — make the heading button data-act="open"? Then clicking heading triggers doAct('open') → toggle. And clicking elsewhere in article also toggles. But then clicks on the text (p) toggle too — plan: "A click on a row opens it in place". OK.

Hmm — clicking the truncation button ("Show the full paragraph") has data-act="full" — handled separately, doesn't toggle. Good.

doAct:
```js
function doAct(act,r){
  switch(act){
    case 'open':toggleOpen(r.id);break;
    case 'stored':{const m=mode(r);m.stored=!m.stored;rerow(r);break;}
    case 'full':{mode(r).full=true;rerow(r);break;}
    case 'cite':copyText(r._citation);break;
    case 'quote':copyText('"'+quotationText(r)+'" '+r._citation);break;
    case 'draft':addToDraft(r);break;
    case 'ctx-prev':case 'ctx-next':{const k=r.id+':'+act.slice(4);if(state.ctx.has(k))state.ctx.delete(k);else state.ctx.add(k);rerow(r);break;}
  }
}
function rerow(r){const art=listEl.querySelector(`[data-id="${CSS.escape(r.id)}"]`);if(art)art.replaceWith(buildRow(r));}
```
toggleOpen: if open delete else add; rerow.

Note: mode(r) helper: get-or-create.

Row HTML content (build with template string):

```js
function buildRow(r){
  const m=getMode(r.id);
  const shownText=m.stored?(r.text||''):(r.text||'').replace(/\[\[fn:\d+\]\]/g,'');
  let display=shownText, cut=false;
  if(!m.full&&shownText.length>700){
    display=shownText.slice(0,700);
    const sp=display.lastIndexOf(' ');
    if(sp>400)display=display.slice(0,sp);
    cut=true;
  }
  const hl=state.q&&!state.q.err?state.q.hlRe:null;
  const html=highlightInto(display+(cut?' …':''),hl);
  // word count
  const wc=(shownText.match(/\S+/g)||[]).length;
  ...
}
```
Hmm wait — cut text + ' …' appended then highlight — ellipsis outside highlight fine. But appending '…' before highlight could merge with a trailing mark... fine.

Hmm, one issue: if cut at 700 and the highlight regex is a phrase that spans the cut — no mark. Acceptable.

Wait, also: the "Show the full paragraph (1,287 words)" — word count of full text. `wc` computed on shownText (full when m.full). For the button label use full-text word count: compute on r.text.

Row structure:

```html
<article class="row" data-id>
 <h3 class="row-h">
   <button class="row-toggle" data-act="open" data-ref="row-<id>" aria-expanded="false|true">
     [badges] <span class="doc">short_title</span>
   </button>
   <span class="meta mono">
     <a href="doc_url" target="_blank" rel="noopener">symbol</a>
     <span class="pin">para. 18</span> <span class="yr">2017</span>
   </span>
 </h3>
 <p class="row-text">…html…</p>
 <p class="row-sub mono">…marks line… …full button…</p>
 <p class="note">…amber notes…</p>
 <div class="row-actions" (only if open)>
   <button data-act="cite">Copy citation</button>
   <button data-act="quote">Copy quotation</button>
   <button data-act="draft">Add to draft</button>
   <span class="ctx mono">Context: <button data-act="ctx-prev">previous</button> | <button data-act="ctx-next">next</button></span>
   <span class="stylenote mono">citation style: UN short form</span>
 </div>
 <div class="ctxblocks">(prev/next content)</div>
</article>
```

Hmm, heading structure: h3 > button containing badges+doc; meta span inside h3 after button. OK.

Marks line: if r._marks>0:
- clean mode: `${r._marks} footnote mark${s} removed · <button data-act="stored" class="linkish">show as stored</button>`
- stored mode: `showing the stored text · <button data-act="stored">remove the footnote marks</button>`

Full button: if cut: `<button data-act="full">Show the full paragraph (${fmt(wc)} words)</button>`.

Amber notes (concatenate):
```js
const notes=[];
if(r._leading!=null&&r._leading!==r.paragraph)notes.push(`the text begins “${r._leading}.” but the record is para. ${r.paragraph}: check the document`);
if(r._lettered)notes.push(`a lettered sub-paragraph, numbered ${r.paragraph} by the file`);
if(r._dup)notes.push('two records share this pinpoint');
if(r._joint)notes.push('joint General Comment');
```
r._lettered store the label letter.

Context blocks: for 'prev'/'next' if in state.ctx: find ctx record, render:
```html
<blockquote class="ctxblock">
 <span class="pin mono">para. 17</span> text (marks removed, escaped, pre-wrap)
</blockquote>
```
Context record text: show marks-removed, escaped (no highlight? plan doesn't say highlight; keep plain grey). Escaped.

Also context availability: if no prev, the button hidden or disabled. ctxMap has prev/next possibly null.

Draft:

```js
function addToDraft(r){
  if(state.draft.some(d=>d.id===r.id)){copyStatus('Already in the draft: '+r._citation);return;}
  state.draft.push({id:r.id,citation:r._citation,symbol:r.symbol,paragraph:r.paragraph,pinpoint:r._pin,committee:r.committee,short_title:r.short_title,year:r.year,text_copied:quotationText(r),text_as_stored:r.text,doc_url:r.doc_url});
  saveDraft();
  $('#draft-n').textContent=state.draft.length;
  // update tab label handled via span
  copyStatus('Added to the draft: '+r._citation);
  if(state.tab===3)renderDraft();
}
```
Tab label: "03 DRAFT (4)" — the span #draft-n inside tab button text.

saveDraft: try localStorage.setItem(key,JSON.stringify(state.draft)) catch → storage='memory'.

Load: try parse; test storage availability:
```js
let storageMode='memory';
try{localStorage.setItem('__t','1');localStorage.removeItem('__t');storageMode='local';}catch(e){}
```

Draft tab render:
```js
function renderDraft(){
  const el=$('#draft-list');
  $('#draft-title').textContent=`Your draft (${state.draft.length} quotation${state.draft.length===1?'':'s'})`;
  if(!state.draft.length){el.innerHTML='<p class="empty">Empty. Open a paragraph on the Paragraphs tab and choose “Add to draft”.</p>';}
  else el.innerHTML=state.draft.map((d,i)=>{
    const bad=draftBad(d); // record missing or text differs
    return `<article class="ditem">
      <blockquote>“${esc(d.text_copied)}”</blockquote>
      <p class="mono"><span class="pin">${esc(d.citation)}</span> <button data-i="${i}" data-act="rm">remove</button>${bad?' <span class="note-red">…</span>':''}</p>
    </article>`;}).join('');
  $('#draft-buttons').hidden=!state.draft.length;
  $('#draft-hint').textContent=`Kept in ${storageMode==='local'?"this browser’s localStorage":"memory only (this browser refused localStorage)"} — nothing leaves the browser.`;
}
```
Draft bad: find record by id; if !rec → 'the record is no longer in the file'; else if rec.text!==d.text_as_stored → 'the stored text of this record differs from the copy in this draft — re-add it if in doubt'.

Delegation for remove on draft list.

Copy all: 
```js
function draftText(){return state.draft.map(d=>'"'+d.text_copied+'"\n'+d.citation).join('\n\n');}
```

Downloads:
```js
function download(name,content,type){
  const b=new Blob([content],{type});
  const u=URL.createObjectURL(b);
  const a=document.createElement('a');a.href=u;a.download=name;document.body.appendChild(a);a.click();a.remove();
  setTimeout(()=>URL.revokeObjectURL(u),1000);
}
```
CSV:
```js
function csv(){
  const cols=['citation','symbol','paragraph','pinpoint','committee','short_title','year','text_copied','text_as_stored','doc_url'];
  const q=v=>'"'+String(v==null?'':v).replace(/"/g,'""')+'"';
  const rows=state.draft.map(d=>cols.map(c=>q(d[c])).join(','));
  return '\uFEFF'+cols.map(q).join(',')+'\r\n'+rows.join('\r\n');
}
```

Copy status area: `#copystatus` — show "Copied: <exact string>" — set textContent; keep max-height. Also the fallback box.

```js
function copyText(str){
  const done=()=>{copyStatusEl.textContent='Copied: '+str;};
  if(navigator.clipboard&&navigator.clipboard.writeText){
    navigator.clipboard.writeText(str).then(done,()=>fallback(str));
  }else fallback(str);
}
function fallback(str){
  $('#fallback-copy').hidden=false;
  const t=$('#fallback-text');t.value=str;t.focus();t.select();
  copyStatusEl.textContent='The clipboard was refused — the text is in the box below; select and copy.';
}
```
Hmm — showing the exact string in aria-live for long quotes: per plan, fine.

Maybe cap display: "Copied: " + (str.length>300? str.slice(0,300)+'… ('+str.length+' characters)': str) — but plan says exact string. The fallback shows exact. For the live message I'll show exact but CSS-limited. OK.

Checks:

```js
function runChecks(){
  const L=[];
  // 1 Query
  if(!state.q)L.push({ok:true,html:'Query: no search words — filters only.'});
  else if(state.q.err)L.push({ok:false,html:'Query not understood: '+esc(state.q.err)});
  else L.push({ok:true,html:'Query understood: '+esc(state.q.echo)+' · '+state.q.termCount+' term'+(s)});
  // 2 totals
  const rendered=($('#panel-2').hidden?Math.min(state.shown,hits.length):$('#rec-list').querySelectorAll('article.row').length);
  const okT=rendered===Math.min(state.shown,ordered.length)&&rendered+Math.max(0,ordered.length-rendered)===ordered.length;
  L.push({ok:okT,html:`Totals: ${fmt(rendered)} rows listed + ${fmt(Math.max(0,ordered.length-rendered))} not yet listed = ${fmt(ordered.length)} hits.`});
  const {c,extra}=countsByCommittee(hits);
  const sumBr=Object.values(c).reduce((a,b)=>a+b,0);
  L.push({ok:sumBr===hits.length+extra,html:`Committee brackets sum to ${fmt(sumBr)} = ${fmt(hits.length)} hits + ${fmt(extra)} double-counted (joint) records.`});
  // 3 chart
  L.push({ok:sumBr===hits.length+extra,html:`FIG.01 bars sum to ${fmt(sumBr)} = ${fmt(hits.length)} hits + ${fmt(extra)} joint.`});
```
Hmm, checks 2's brackets and 3 chart are same numbers — chart check could verify chart data sum from the actual chart instance. If chart built: chart.data.datasets[0].data sum. Else same as brackets. Let me: if chart instance exists, sum its data; compare. Good, more genuine.

```js
  // 4 highlight
  if(state.q&&!state.q.err&&!state.q.notOnly){
    const miss=hits.filter(r=>{const t=(r.text||'').replace(/\[\[fn:\d+\]\]/g,'');return !state.q.hlRe.test(t);});
```
careful: hlRe is global — .test advances lastIndex! Use a fresh non-global test or reset. I'll create hlRe as global for exec loop; for .test usage reset lastIndex=0 before and after. Or make a separate non-global check regex with same source, flags 'iu'. Let me store both: hlRe (giu) and hlTest (iu). Simpler: hlTest = new RegExp(hlRe.source,'iu').

Hmm wait — case-insensitivity needed for test since raw text keeps case. Yes 'iu'.

```js
    if(miss.length)L.push({ok:false,html:`Highlight: ${miss.length} hit${...} matched in the normalised text but show no highlight (${list symbols/pinpoints}); they are still listed.`});
    else L.push({ok:true,html:`Highlight: every one of the ${fmt(hits.length)} hits shows at least one highlighted word.`});
  } else if(state.q&&state.q.notOnly){
    L.push({ok:true,html:'Highlight: the query excludes terms only (NOT), so nothing is highlighted.'});
  } else {
    L.push({ok:true,html:'Highlight: no search words, nothing to highlight.'});
  }
```
miss list: cap at 5 examples: `${r.symbol}, ${r._pin}`.

```js
  // 5 normalisation
  if(state.q&&!state.q.err&&state.q.straightTerms&&state.q.straightTerms.length){
    // count hits matching only via variant
    let n=0;
    hits.forEach(r=>{
      const only=state.q.straightTerms.some(t=>t.normTest(r._norm)&&!t.strictTest(r.text||''));
      if(only)n++;
    });
    const chars=[...new Set(state.q.straightTerms.flatMap(t=>t.chars))].join(', ');
    L.push({ok:true,html:`Normalisation: the query holds straight ${chars}; curly and dash forms count as the same, and ${fmt(n)} hit${n===1?'':'s'} matched only through a curly or dash form.`});
  }
```
straightTerms: positive terms whose raw contains ', ", or -'. For each: normTest (the term matcher over norm), strictTest: regex over raw text: build with hl=false body but... strict means literal chars as typed (normalised casing? query lowercased vs text case → use 'iu' flags), over raw text with marks intact. Body: wordBody(normText(v),false) with flags 'iu', gaps for phrases: (?:\s|\[\[fn:\d+\]\])+? In raw text, phrase words separated by newline etc — \s covers; marks: keep pattern same. OK.

Hmm wait — strict with 'iu' over raw text: raw text may have curly quotes which won't match straight query char → strict fails → counted as variant-only. Correct semantics.

But subtle: strict body from normText(v): normText lowercases and maps curly→straight in the QUERY — if user typed curly apostrophe in query, it becomes straight in body → strict fails always → variant-only count inflated. But this check only applies when query holds straight chars... the term may hold both? Edge case, acceptable. Actually let me build strict body from raw v with escRe only (no mapping, no lowercase — 'i' flag handles case): wordBodyStrict(v): star support, escRe each char. Fine.

```js
  // 6 numbering
  const lm=hits.filter(r=>r._leading!=null&&r._leading!==r.paragraph);
  const dp=hits.filter(r=>r._dup);
  const sb=hits.filter(r=>r._lettered);
  const nq=lm.length+dp.length+sb.length;
  let txt='Numbering: ';
  const parts=[];
  if(lm.length)parts.push(`${lm.length} leading-number mismatch${...} (e.g. ${lm[0].symbol}: “${lm[0]._leading}.” vs para. ${lm[0].paragraph})`);
  if(dp.length)parts.push(`${dp.length} shared pinpoint${...}`);
  if(sb.length)parts.push(`${sb.length} lettered sub-paragraph${...}`);
  L.push({ok:true,html:'Numbering: '+(parts.length?parts.join('; ')+'. Each is flagged on its row.':'no numbering quirks among the hits.')});
```
Wait — should numbering be a pass always? I earlier decided informational pass. Hmm, but actually think again: "A failed check marks rows; it never drops them." — the amber notes mark rows regardless. So numbering check passing while notes show is coherent: the check verifies identification. OK. Hmm, but one could argue leading mismatch = "check failed" highlighting data issue... I'll keep pass-with-details; the amber notes carry the warning. Actually wait — let me reconsider once more. The plan says: "**Numbering.** Hits whose leading number differs from `paragraph`, with both numbers; hits that share a pinpoint with another record of the same `title`; hits that are lettered sub-paragraphs." It just lists what to show. And the preamble: "Each check is one line: what was compared, the values, 'pass' in green or 'check failed' in red with the pinpoints concerned." So numbering line shows values (counts, examples). Whether pass/fail... The values being non-zero doesn't mean the app failed. Pass. OK.

```js
  // 7 marks
  let bad=[];
  hits.forEach(r=>{
    const t=r.text||'';
    const well=(t.match(/\[\[fn:\d+\]\]/g)||[]).length;
    const opens=(t.match(/\[\[fn:/g)||[]).length;
    if(well!==r._marks||opens!==well)bad.push(r);
  });
  L.push({ok:!bad.length,html:bad.length?`Footnote marks: ${bad.length} hit${...} where the marks removed do not round-trip (${examples})`:`Footnote marks: for all ${fmt(hits.length)} hits, marks removed = marks counted and every “[[fn:” is well-formed.`});
```
Hmm "putting them back gives the stored text exactly" — can't do; wording: I'll say "removal is exact: nothing else is changed". Actually I CAN verify more: clean = t.replace(/\[\[fn:\d+\]\]/g,''); verify that inserting back... no. Another verifiable property: t.split(mark) pieces joined equal clean — trivially true. The meaningful check: well-formedness + counts. I'll word: "for every hit, the footnote marks removed equal the marks counted, and each “[[fn:” is a well-formed mark". Good.

```js
  // 8 draft
  if(!state.draft.length)L.push({ok:true,html:'Draft: empty.'});
  else{
    const bad2=state.draft.filter(d=>{const r=byId.get(d.id);return !r||r.text!==d.text_as_stored;});
    L.push({ok:!bad2.length,html:bad2.length?`Draft: ${bad2.length} of ${state.draft.length} items no longer match the stored text of their records (${bad2[0].citation}); the item is marked.`:`Draft: all ${state.draft.length} items match the stored text of their records.`});
  }
  state.checks=L;
  const fails=L.filter(x=>!x.ok).length;
  const hc=$('#head-checks');
  if(fails){hc.innerHTML='<span class="dot red"></span>'+fails+' check'+(fails===1?'':'s')+' failed';$('#tab4-dot').hidden=false;}
  else{hc.innerHTML='<span class="dot green"></span>'+L.length+' checks pass';$('#tab4-dot').hidden=true;}
  if(state.tab===4)renderChecksPanel();
}
```
Hmm wait — when fails>0, should header also show passes? Plan: "a green dot and 'n checks pass', or a red dot and 'n checks failed'". So just fails count when any. OK.

Hmm, also the tab 04 red dot: plan "(and a red dot on tab 04)". #tab4-dot red dot span in tab 4 label.

byId map: `const byId=new Map(R.map(r=>[r.id,r]));`

renderChecksPanel:
```js
function renderChecksPanel(){
  $('#checks-list').innerHTML=state.checks.map(c=>`<li class="${c.ok?'pass':'fail'}"><span class="res">${c.ok?'pass':'check failed'}</span> ${c.html}</li>`).join('');
}
```
Known quirks + method static sections in HTML (quirks injected at load).

Now the rail interactive wiring:

Search:
```js
const qInput=$('#q'), syn=$('#syntax');
qInput.addEventListener('focus',()=>{if(!qInput.value)syn.hidden=false;});
qInput.addEventListener('input',()=>{syn.hidden=true;});
qInput.addEventListener('blur',()=>{setTimeout(()=>{syn.hidden=true;},150);});
```
Hmm — blur closing: examples use mousedown preventDefault to avoid blur. Simpler: don't close on blur; close on input or Escape or after running. But clicking elsewhere leaves it open... use blur with timeout and mousedown preventDefault on syntax buttons. And clicking a syntax example button: mousedown preventDefault → no blur; click → run. OK. Actually focus moving to example button (we allow focus via keyboard arrows) — blur fires; timeout hides list while focus is on button inside it... Guard: in blur timeout, check if activeElement is inside syn → don't hide.

```js
qInput.addEventListener('keydown',e=>{
  if(e.key==='ArrowDown'&&!syn.hidden){const b=syn.querySelector('button.ex');if(b){e.preventDefault();b.focus();}}
  if(e.key==='Escape'){syn.hidden=true;}
  if(e.key==='Enter'){e.preventDefault();runSearch();}
});
syn.addEventListener('keydown',e=>{
  const btns=[...syn.querySelectorAll('button.ex')];
  const i=btns.indexOf(document.activeElement);
  if(e.key==='ArrowDown'&&i<btns.length-1){e.preventDefault();btns[i+1].focus();}
  if(e.key==='ArrowUp'){e.preventDefault();if(i>0)btns[i-1].focus();else qInput.focus();}
  if(e.key==='Escape')qInput.focus();
});
```
Example click: qInput.value=ex; runSearch(); syn.hidden=true; qInput.focus().

runSearch:
```js
function runSearch(){
  const raw=qInput.value.trim();
  state.rawQ=raw;
  if(!raw){state.q=null;}
  else{
    try{
      const tree=parse(raw);
      const terms=[];collectTerms(tree,false,terms);
      state.q={tree,echo:echoLine(tree),terms,notOnly:tree.k==='NOT',
        termCount:countTerms(tree),
        hlRe:terms.length?buildHlRe(terms):null,
        termsReNorm:terms.length?buildNormRe(terms):null,
        straightTerms:buildStraight(terms),
        err:null};
    }catch(e){state.q={err:e.msg||'could not parse the query'};}
  }
  state.shown=25;
  update();
}
```
countTerms: walk all WD/PH nodes.
buildNormRe: combined global: alts=terms.map(t=>t.k==='WD'?B0+wordBody(normText(t.v),false)+B1:B0+words.join('\\s+')+B1) — wait phrases over norm: words joined \\s+. flags 'gu'.

buildStraight(terms): for each term whose raw v contains ' or " or -: 
```js
function buildStraight(terms){
  const out=[];
  terms.forEach(t=>{
    const raw=t.k==='WD'?t.v:t.v;
    if(!/['"-]/.test(raw))return;
    const chars=[...raw].filter(c=>c==='\''||c==='"'||c==='-');
    let body;
    if(t.k==='WD')body=B0+wordBodyStrict(t.v)+B1;
    else body=B0+t.v.trim().split(/\s+/).map(w=>wordBodyStrict(w)).join('(?:\\s|\\[\\[fn:\\d+\\]\\])+')+B1;
    const strict=new RegExp(body,'iu');
    const normT=termMatcher(t); // over norm
    out.push({normTest:normT,strictTest:s=>strict.test(s),chars});
  });
  return out;
}
```
wordBodyStrict(w): star strip, escRe each char (no mapping).

Wait — termMatcher(t) needs t.k 'WD'/'PH' — my parse nodes use k:'WD'/'PH'. Adjust termMatcher to those keys. And buildHlRe too.

Non-global strict regex .test — no lastIndex issue. normT non-global 'u' — fine.

Echo line element: `#echo`. Update in updateRail:
```js
const echoEl=$('#echo');
if(!state.q){echoEl.textContent=state.rawQ?'':'';echoEl.hidden=true;}
else if(state.q.err){echoEl.hidden=false;echoEl.textContent='Not understood: '+state.q.err;echoEl.className='echo err';}
else{echoEl.hidden=false;echoEl.textContent=state.q.echo;echoEl.className='echo';}
```
Note: state.q stays until new search; typing in input doesn't clear it. If user clears input and hits Search → q=null. Good.

Committee checkboxes: build at init:
```js
const cbsBox=$('#cbs');
CORDER.forEach(c=>{
  const id='cb-'+c;
  const lb=document.createElement('label');
  lb.className='cb';
  lb.innerHTML=`<input type="checkbox" id="${id}" checked><span class="code">${c}</span> <span class="cname">${CMTY_FULL[c]||c}</span> <span class="cnt mono" id="cnt-${c}"></span>`;
  cbsBox.appendChild(lb);
});
cbsBox.addEventListener('change',e=>{ if(e.target.matches('input')){ sync ticks from all inputs; update(); }});
```
syncTicks: read all checkboxes; if none ticked → keep... "all / none" links: "none" ticks none → hits 0. Allowed? Sure, shows 0. Hmm — filter with none ticked → 0 matches; fine, big number 0. OK.

all/none buttons:
```js
$('#cb-all').onclick=()=>{setAll(true)};
$('#cb-none').onclick=()=>{setAll(false)};
```
setAll: set inputs checked; state.ticked accordingly; update().

Year inputs:
```js
$('#yfrom').value=YMIN; ...
change: parse ints, clamp, if from>to swap? or set to min/max on invalid. Keep simple: if invalid/empty → defaults; clamp to [YMIN,YMAX]; if from>to, swap.
```

Doc select:
```js
build optgroups: map committee(field) → sorted titles; option value=title, text=short_title.
change: state.doc=value; update();
```
Note: doc select applies immediately on change (filters). Fine.

Accordion: 
```js
const accBtn=$('#acc-btn'),accPanel=$('#acc-panel');
accBtn.onclick=()=>{const open=accBtn.getAttribute('aria-expanded')==='true';accBtn.setAttribute('aria-expanded',String(!open));accPanel.hidden=open;};
```
Default closed. Hmm — should it be open by default? "each closed until clicked". Closed.

Tabs:
```js
const tabs=[...document.querySelectorAll('[role="tab"]')];
tabs.forEach((t,i)=>{
  t.addEventListener('click',()=>setTab(i+1));
  t.addEventListener('keydown',e=>{
    let j=null;
    if(e.key==='ArrowRight')j=(i+1)%tabs.length;
    if(e.key==='ArrowLeft')j=(i-1+tabs.length)%tabs.length;
    if(e.key==='Home')j=0;
    if(e.key==='End')j=tabs.length-1;
    if(j!=null){e.preventDefault();tabs[j].focus();setTab(j+1);}
  });
});
function setTab(n){
  state.tab=n;
  tabs.forEach((t,i)=>{t.setAttribute('aria-selected',String(i===n-1));t.tabIndex=i===n-1?0:-1;});
  for(let k=1;k<=4;k++)$('#panel-'+k).hidden=k!==n;
  $('#rail').hidden=n===3;
  if(n===1){buildChart();}
  if(n===4)renderChecksPanel();
  if(n===2)renderRecords();
  if(n===3)renderDraft();
}
```
tabIndex roving.

update() → renderPanel():
```js
function renderPanel(){
  if(state.tab===1)buildChart();
  else if(state.tab===2)renderRecords();
  else if(state.tab===3)renderDraft();
  // tab4 rendered by runChecks when active
}
```
runChecks called after renderPanel — renders tab4 panel if active. Order in update(): renderPanel(); runChecks(). Good.

updateRail():
```js
function updateRail(){
  $('#big-num').textContent=fmt(hits.length);
  $('#of').textContent='of '+fmt(R.length);
  // brackets
  const {c}=countsByCommittee(hits);
  CORDER.forEach(k=>{$('#cnt-'+k).textContent=c[k]?'['+fmt(c[k])+']':'';});
  // chips
  const chips=[];
  if(state.ticked.size!==CORDER.length){
    const names=CORDER.filter(k=>state.ticked.has(k)).join(', ');
    chips.push({label:`Committees: ${names} (${state.ticked.size} of ${CORDER.length})`,remove:()=>setAll(true)});
  }
  if(state.yFrom!==YMIN||state.yTo!==YMAX)chips.push({label:`Years ${state.yFrom}–${state.yTo}`,remove:()=>{state.yFrom=YMIN;state.yTo=YMAX;$('#yfrom').value=YMIN;$('#yto').value=YMAX;}});
  if(state.doc)chips.push({label:'Document: '+docShort(state.doc),remove:()=>{state.doc='';$('#docsel').value='';}});
  const box=$('#chips');box.innerHTML='';
  chips.forEach(ch=>{const b=document.createElement('button');b.className='chip mono';b.innerHTML=esc(ch.label)+' <span aria-hidden="true">×</span>';b.onclick=()=>{ch.remove();update();};box.appendChild(b);});
  // echo
  ...
}
```
docShort: find a record with that title → short_title.

setAll(v): set state.ticked and checkbox DOM, then caller calls update. Let me make setAll do update itself? In chip remove I call ch.remove() then update() — remove fns only mutate state+DOM. OK.

Note: setAll used by all/none buttons too:
```js
function setAll(v){CORDER.forEach(k=>{const cb=$('#cb-'+k);cb.checked=v;});state.ticked=v?new Set(CORDER):new Set();}
$('#cb-all').addEventListener('click',()=>{setAll(true);update();});
```
And checkbox change:
```js
cbsBox.addEventListener('change',()=>{
  const t=new Set();CORDER.forEach(k=>{if($('#cb-'+k).checked)t.add(k);});
  state.ticked=t;update();
});
```

Clear all:
```js
$('#clear-all').addEventListener('click',()=>{
  qInput.value='';state.rawQ='';state.q=null;
  setAll(true);
  state.yFrom=YMIN;state.yTo=YMAX;$('#yfrom').value=YMIN;$('#yto').value=YMAX;
  state.doc='';$('#docsel').value='';
  state.shown=25;
  update();
});
```
Should clear-all also close rows? Rows re-render on records tab (modes stay but that's per-row display pref — fine).

Show more:
```js
$('#rec-more').addEventListener('click',()=>{state.shown+=25;renderRecords();runChecks();});
```
Focus restore: keepFocus wrapper. Add data-ref="more" to button; wrap renderRecords call. Eh — I'll implement keepFocus and use it in the few update triggers (order select change, show more, checkbox changes?). Checkbox change re-renders rail numbers only (not rail DOM rebuild), so focus retained naturally. Good — since rail DOM is static, focus is safe. Only main panel re-renders. So keepFocus matters for: order select (data-ref), show-more (data-ref), row buttons after rerow (row rerow replaces article; the clicked button inside — after rerow, focus lost; restore to row toggle or same act button? e.g., clicking "show as stored" → rerow → focus gone. Restore: data-ref on act buttons: `act-stored-<id>` etc. Let me add data-ref to each data-act button as `${act}-${id}` and in rerow, after replace, try focus `[data-ref="${act}-${id}"]`... but 'full' button disappears after expansion (no longer cut). Then focus the row toggle. Implementation: in doAct, after rerow, attempt focus matching data-ref, else row toggle.

Let me implement:
```js
function rerow(r,ref){
  const art=$('#rec-list').querySelector(`article.row[data-id="${CSS.escape(r.id)}"]`);
  if(!art)return;
  art.replaceWith(buildRow(r));
  if(ref){const n=$('#rec-list').querySelector(`[data-ref="${CSS.escape(ref)}"]`);if(n){n.focus();return;}}
  const t=$('#rec-list').querySelector(`[data-ref="open-${CSS.escape(r.id)}"]`);if(t)t.focus();
}
```
And doAct passes ref = act+'-'+r.id.

For 'cite'/'quote'/'draft' no rerow needed (no state change except draft count → tab label span textContent only). Good.

Order select: 
```js
$('#order-sel').addEventListener('change',e=>{state.order=e.target.value;keepFocus(()=>{renderRecords();runChecks();});});
```
keepFocus helper with data-ref="order-sel" on select — it's static DOM in panel 2 header... wait, is the records panel header static? I'll build panel-2 header statically in HTML (summary line, order select, hint) and only re-render #rec-list and #rec-more. Then focus retained automatically; no keepFocus needed. renderRecords updates summary text, order label text. 

But summary line is aria-live — fine.

Panel 2 static skeleton:
```html
<section id="panel-2" role="tabpanel" aria-labelledby="tab-2" hidden>
  <p id="rec-summary" class="rec-summary serif" aria-live="polite"></p>
  <p class="orderline mono">sorted by <span id="order-desc">year, newest first, then by document and paragraph</span>
    <label class="mono">order: <select id="order-sel" data-ref="order-sel">
      <option value="year">year, newest first</option>
      <option value="doc">document order</option>
      <option value="matches">most matches first</option>
    </select></label></p>
  <p class="hint mono">This page retrieves; it never writes. Every paragraph shown is a record of the file, as stored.</p>
  <div id="rec-list"></div>
  <button id="rec-more" class="more" data-ref="more" hidden></button>
</section>
```
order-desc text per selection: year → "year, newest first, then by document and paragraph"; doc → "document, then paragraph"; matches → "number of matched terms, most first".

Show more: state.shown+=25; renderRecords(); runChecks(); — focus: button may still exist (re-rendered? No! #rec-more is static, only text/hidden updated). Focus retained. 

rec-list rebuilt only when renderRecords called — on update() (filters/search/tab). Fine.

Panel 1 static skeleton:
```html
<section id="panel-1" role="tabpanel" aria-labelledby="tab-1">
  <div class="fig">
    <p class="mono figno">FIG.01</p>
    <h2 class="serif figtitle">Paragraphs per committee</h2>
    <div class="fig-flex">
      <div class="chart-wrap" id="chart-wrap" style="height:480px">
        <canvas id="chart" role="img"><span id="chart-fallback">Chart of paragraphs per committee; the table gives the same numbers.</span></canvas>
      </div>
      <table class="figtable">
        <caption class="mono">FIG.01 — table</caption>
        <thead><tr><th scope="col">Committee</th><th scope="col" class="num">Paragraphs</th></tr></thead>
        <tbody id="chart-tbody"></tbody>
      </table>
    </div>
    <p class="hint mono">click a bar = tick that committee alone</p>
    <p class="compute mono">How this is computed: one count per committee over the paragraphs that match the query and filters. Joint General Comments count under both committees, so the bars can add up to more than the hits.</p>
    <p class="mono" id="chart-total"></p>
  </div>
</section>
```
chart-total: "Bars sum to 281 = 279 hits + 2 joint records." Maybe put in compute line area. OK.

buildChart updates tbody, aria-label, chart instance, chart-wrap height.

Panel 3:
```html
<section id="panel-3" role="tabpanel" aria-labelledby="tab-3" hidden>
  <h2 class="serif" id="draft-title">Your draft (0 quotations)</h2>
  <p id="draft-hint" class="hint mono"></p>
  <div id="draft-buttons" hidden>
    <button id="copy-all">Copy all</button>
    <button id="dl-txt">Download .txt</button>
    <button id="dl-csv">Download .csv</button>
  </div>
  <div id="draft-list"></div>
</section>
```

Panel 4:
```html
<section id="panel-4" role="tabpanel" aria-labelledby="tab-4" hidden>
  <h2 class="serif">Can I trust this?</h2>
  <p class="hint mono">The app checks itself after every search and filter change. A failed check marks rows; it never drops them.</p>
  <ul id="checks-list" class="checks"></ul>
  <h3 class="serif">Known quirks of this file</h3>
  <p class="hint mono">Computed at load, before any search.</p>
  <ul id="quirks-list" class="quirks"></ul>
  <h3 class="serif">How this is computed</h3>
  <ul class="quirks">
    <li>Matching: ... </li>
    ...
  </ul>
</section>
```

Footer:
```html
<footer class="mono site-foot">
  <span id="foot-src"></span> · Counting, matching and sorting are done by this page’s code; no model is called. · Built with Chart.js 4 (MIT licence).
</footer>
```

Header line: `${fmt(R.length)} paragraphs from ${fmt(titles.size)} General Comments of ${allCodes.size} committees, ${YMIN}–${YMAX}` + source link.

foot-src: `${D.source}` + (D.built? ', built '+D.built : '').

Now — remaining details:

quotationText:
```js
function quotationText(r){
  let t=(r.text||'').replace(/\[\[fn:\d+\]\]/g,'');
  if(r._leading!=null&&r._leading===r.paragraph)t=t.replace(/^\d{1,3}\.\s+/,'');
  return t.trim();
}
```
Hmm trim? "the shown text" — shown text isn't trimmed... trailing whitespace trim is harmless. Keep .trim()? If stored text has trailing spaces, citation paste cleaner. I'll keep trim.

Pinpoint function:
```js
function pinpoint(r){
  const m=(r.text||'').match(/^\(([a-z]{1,4})\)/);
  if(m){r._lettered=m[1];return 'subpara. ('+m[1]+')';}
  if(!r.paragraph)return 'preamble';
  return 'para. '+r.paragraph;
}
```
paragraph 0 → 'preamble'. Note plan: "22 records are lettered sub-paragraphs" — some may also be para 0? lettered check first per my order.

Hmm wait — the lettered regex on raw text: "^\(([a-z]{1,4})\)" e.g. "(a) To take note…". But could a normal paragraph start with "(3)"? digits — [a-z] only, ok. Could text start with "(see ...)"? "see" is 3 letters — would match as lettered "(see)"! Hmm. Risky? Actual subparas are (a)-(z) or (ii) etc. "(see" unlikely at very start. The plan specifies `^\(([a-z]{1,4})\)`. Follow plan.

Citation:
```js
function citation(r){
  if(r._shared){
    return r.committee+', '+docName(r.title)+' ('+r.symbol+'), '+r._pin;
  }
  return r.symbol+', '+r._pin;
}
```

Now buildRow full:

```js
function buildRow(r){
  const m=getMode(r.id);
  const open=state.open.has(r.id);
  const raw=r.text||'';
  const clean=raw.replace(/\[\[fn:\d+\]\]/g,'');
  const base=m.stored?raw:clean;
  let display=base,cut=false;
  if(!m.full&&base.length>700){
    display=base.slice(0,700);
    const sp=display.lastIndexOf(' ');
    if(sp>300)display=display.slice(0,sp);
    cut=true;
  }
  const shown=display+(cut?' …':'');
  const hl=state.q&&!state.q.err&&state.q.hlRe?state.q.hlRe:null;
  const textHtml=highlightInto(shown,hl);
  const wc=(raw.match(/\S+/g)||[]).length;
  const badges=[...r._committees].map(c=>'<span class="badge">'+esc(c)+'</span>').join(' ');
  const notes=[];
  if(r._leading!=null&&r._leading!==r.paragraph)notes.push('the text begins “'+r._leading+'.” but the record is para. '+r.paragraph+': check the document');
  if(r._lettered)notes.push('a lettered sub-paragraph, numbered '+r.paragraph+' by the file');
  if(r._dup)notes.push('two records share this pinpoint');
  if(r._joint)notes.push('joint General Comment');
  const cm=r._marks? (m.stored?
      '<span>showing the stored text, character for character</span> · <button class="linkish" data-act="stored" data-ref="stored-'+esc(r.id)+'">remove the footnote marks</button>'
      : fmt(r._marks)+' footnote mark'+(r._marks===1?'':'s')+' removed · <button class="linkish" data-act="stored" data-ref="stored-'+esc(r.id)+'">show as stored</button>') : '';
  const fullBtn=cut?'<button class="linkish" data-act="full" data-ref="full-'+esc(r.id)+'">Show the full paragraph ('+fmt(wc)+' words)</button>':'';
  // context blocks
  let ctxHtml='';
  ['prev','next'].forEach(side=>{
    if(state.ctx.has(r.id+':'+side)){
      const c=ctxMap.get(r.id)&&ctxMap.get(r.id)[side];
      if(c)ctxHtml+='<blockquote class="ctxblock"><span class="pin mono">'+esc(c._pin)+'</span> '+esc((c.text||'').replace(/\[\[fn:\d+\]\]/g,''))+'</blockquote>';
    }
  });
  const prevOk=ctxMap.get(r.id)&&ctxMap.get(r.id).prev;
  const nextOk=ctxMap.get(r.id)&&ctxMap.get(r.id).next;
  const art=document.createElement('article');
  art.className='row'+(open?' open':'');
  art.dataset.id=r.id;
  art.innerHTML=
   '<h3 class="row-h"><button class="row-toggle" data-act="open" data-ref="open-'+esc(r.id)+'" aria-expanded="'+open+'">'+badges+' <span class="doc">'+esc(r.short_title||r.title)+'</span></button>'+
   '<span class="meta mono"><a href="'+esc(r.doc_url||'')+'" target="_blank" rel="noopener">'+esc(r.symbol)+'</a> · <span class="pin">'+esc(r._pin)+'</span> · '+esc(String(r.year))+'</span></h3>'+
   '<p class="row-text">'+textHtml+'</p>'+
   (cm||fullBtn?'<p class="row-sub mono">'+[cm,fullBtn].filter(Boolean).join(' · ')+'</p>':'')+
   (notes.length?'<p class="ambernote">'+notes.map(n=>esc(n)).join(' · ')+'</p>':'')+
   (open?('<div class="row-actions">'+
     '<button data-act="cite" data-ref="cite-'+esc(r.id)+'">Copy citation</button> '+
     '<button data-act="quote" data-ref="quote-'+esc(r.id)+'">Copy quotation</button> '+
     '<button data-act="draft" data-ref="draft-'+esc(r.id)+'">Add to draft</button>'+
     '<span class="ctx mono">Context: '+(prevOk?'<button class="linkish" data-act="ctx-prev" data-ref="ctx-prev-'+esc(r.id)+'">previous</button>':'<span class="dim">previous</span>')+' | '+(nextOk?'<button class="linkish" data-act="ctx-next" data-ref="ctx-next-'+esc(r.id)+'">next</button>':'<span class="dim">next</span>')+'</span>'+
     '<span class="stylenote mono">citation style: UN short form</span></div>'):'')+
   ctxHtml;
  return art;
}
```
Wait — doc_url could be empty? Fields say all filled except cited_articles. Guard with href fallback: if no doc_url, render symbol without link. Plan: "Every row that shows a document has its symbol, linked to doc_url". Handle empty: if !doc_url → plain span. Let me add that.

Hmm — data-ref values contain record ids like "a-53-44-0001" — CSS.escape fine in selector; attribute values fine.

Note the mark: cm string when stored mode says "showing the stored text, character for character" — plus button to go back.

toggleOpen:
```js
function toggleOpen(id){if(state.open.has(id))state.open.delete(id);else state.open.add(id);const r=byId.get(id);rerow(r,'open-'+id);}
```
Hmm rerow focuses ref 'open-id' — the toggle button. Good.

doAct:
```js
function doAct(act,r){
  switch(act){
    case 'open':toggleOpen(r.id);break;
    case 'stored':{const m=getMode(r.id);m.stored=!m.stored;rerow(r,'stored-'+r.id);break;}
    case 'full':{getMode(r.id).full=true;rerow(r,'open-'+r.id);break;}
    case 'cite':copyText(r._citation);break;
    case 'quote':copyText('"'+quotationText(r)+'" '+r._citation);break;
    case 'draft':addToDraft(r);break;
    case 'ctx-prev':case 'ctx-next':{
      const k=r.id+':'+act.slice(4);
      if(state.ctx.has(k))state.ctx.delete(k);else state.ctx.add(k);
      rerow(r,act+'-'+r.id);break;}
  }
}
```

getMode:
```js
function getMode(id){let m=state.mode.get(id);if(!m){m={stored:false,full:false};state.mode.set(id,m);}return m;}
```

Now — one thing: rerow uses querySelector with data-id — ids may contain quotes? ids like "a-53-44-0001" — safe. Use CSS.escape anyway.

Init sequence:
```js
// header
$('#head-line').innerHTML= ... link ...
// quirks list
// committee checkboxes, doc select, years
// tabs wiring, rail wiring, records delegation, draft wiring
// load draft
// update();
qInput.focus(); // opens syntax list (empty+focus)
```
Focus on load: qInput.focus() triggers focus handler → syntax shown. Per plan. OK.

Hmm — wait, `syn.hidden=false` on focus: on load focus fires focus event? Programmatic .focus() fires focus event, yes.

update() initial: hits=R (empty query, all ticked). Overview chart with totals. 

Draft buttons wiring:
```js
$('#copy-all').addEventListener('click',()=>copyText(draftText()));
$('#dl-txt').addEventListener('click',()=>download('verbatim-draft.txt',draftText(),'text/plain;charset=utf-8'));
$('#dl-csv').addEventListener('click',()=>download('verbatim-draft.csv',csvString(),'text/csv;charset=utf-8'));
$('#draft-list').addEventListener('click',e=>{
  const b=e.target.closest('[data-act="rm"]');
  if(!b)return;
  const i=+b.dataset.i;state.draft.splice(i,1);saveDraft();
  $('#draft-n').textContent=state.draft.length;
  renderDraft();runChecks();
});
```
runChecks to update draft check + header. Good.

saveDraft:
```js
function saveDraft(){
  if(storageMode==='local'){try{localStorage.setItem(KEY,JSON.stringify(state.draft));}catch(e){storageMode='memory';}}
}
```
And update draft hint if rendered.

Now — chart total line and check. buildChart stores lastChartSum & labels/data on state for checks: I'll compute counts in runChecks independently (countsByCommittee(hits)) — chart check: if chart && state.tab===1: sum chart data. Else arithmetic. Let me just do: chartSum = chart? chart.data.datasets[0].data.reduce(...) : arithmetic sum. Both compared to hits+extra.

Now — panel 1 table + aria-label: numbers same.

Table rows:
```js
$('#chart-tbody').innerHTML=labels.map((l,i)=>'<tr><th scope="row">'+esc(l)+'</th><td class="num">'+fmt(data[i])+'</td></tr>').join('');
```
th scope=row for committee names.

Wait — plan says table with same numbers beside chart; with caption and th scope=col. Done.

aria-label: 'Paragraphs per committee, matching paragraphs per committee: CRC 2091; ...'. Compose: labels.map((l,i)=>`${CMTY_FULL[l]||l} (${l}): ${fmt(data[i])}`).join('; '). Full names better for screen readers. OK.

Chart height: labels.length*(bar ~36px + gap) — set wrap height = labels.length*46+30.

Now, one more check: "Totals: rows listed across pages equal the hits" — implemented.

Also — check 2 wording combines two things (rows + brackets) as separate lines? Plan: "Totals. Rows listed across pages equal the hits; the checkboxes' bracketed counts sum to the hits plus joint hits." Could be one line or two. I'll make two lines for clarity: "Totals (rows)" and "Totals (committees)". Then chart separate. That's fine — check count n in header varies (8-9 lines). OK.

Edge: hits=0 → summary "0 of 7,304 paragraphs match"; committees/years omitted; rec-list empty; add "No paragraphs match." message? renderRecords: if !ordered.length show `<p class="empty">No paragraphs match.</p>`. Good.

Now the search input placeholder — keep short: `e.g. "best interests" AND child*`.

Syntax dropdown content:
```html
<div id="syntax" class="syntax" hidden>
  <p class="mono syn-head">HOW TO SEARCH</p>
  <ul class="syn-list">
    <li>a space or AND joins words</li>
    <li>OR, NOT, or a leading - excludes or offers a choice</li>
    ...
  </ul>
</div>
```
Per plan wording:
- a space or AND joins words
- OR
- NOT or a leading minus
- "an exact phrase" in double quotes
- parentheses
- a star at the end of a word for any ending (child* finds children)
- operators in capitals, lower-case "or" is a word

Examples buttons class "ex".

Let me write:
```html
<ul>
 <li>a space or AND joins words</li>
 <li>OR offers a choice</li>
 <li>NOT, or a leading -, excludes</li>
 <li>“an exact phrase” in double quotes</li>
 <li>parentheses group</li>
 <li>a star at the end of a word finds any ending (child* finds children)</li>
 <li>operators in capitals; lower-case “or” is a word</li>
</ul>
<p class="mono">TRY:</p>
<button class="ex">"best interests" AND child</button>
<button class="ex">(torture OR ill-treatment) NOT detention</button>
<button class="ex">"reasonable accommodation"</button>
```

Styling the syntax list: bordered top rule, small.

Now CSS. Let me write it:

```css
[hidden]{display:none!important}
*{box-sizing:border-box}
html,body{margin:0;padding:0}
body{background:#f4f0e8;color:#1d1b18;font:16px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
a{color:#9b2335}
a:focus,button:focus,input:focus,select:focus,textarea:focus,[tabindex]:focus{outline:2px solid #9b2335;outline-offset:2px}
.mono{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:11.5px;letter-spacing:.08em;text-transform:uppercase}
```
Hmm — uppercase transform on mono labels; but some mono content (echo, hints) shouldn't be all caps... The studio spec: "small uppercase letter-spaced monospace ... for labels, tab names and figure numbers". Hints are short monospace hints — plan says "Short monospace hints" — not necessarily uppercase. I'll define .mono without transform, and .mono.up or apply uppercase selectively. Simpler: .mono class = monospace 11.5px letter-spacing .06em; uppercase where wanted via additional class or element-specific. Let me use `.lab` for uppercase labels and `.mono` plain small monospace. I'll define:

```css
.mono{font-family:ui-monospace,Menlo,Consolas,"Courier New",monospace;font-size:12px;letter-spacing:.04em}
.lab{font-family:...;font-size:11px;letter-spacing:.12em;text-transform:uppercase}
```
Use .lab for tab names, section labels, figure numbers, header label; .mono for hints, echoes, meta (mixed case).

serif: `font-family:Georgia,"Times New Roman",serif`.

Layout:
```css
.site-head{display:flex;justify-content:space-between;align-items:flex-end;gap:24px;padding:20px 28px 14px;border-bottom:1px solid #d9d2c3}
.site-head h1{font-family:Georgia,...;font-size:26px;font-weight:700;margin:6px 0 4px;line-height:1.2}
.layout{display:flex;align-items:stretch;min-height:60vh}
.rail{width:300px;flex:0 0 300px;border-right:1px solid #d9d2c3;padding:18px 20px 30px}
.main{flex:1;min-width:0;padding:18px 28px 40px}
```
Responsive @media (max-width:880px){.layout{flex-direction:column}.rail{width:auto;flex:none;border-right:none;border-bottom:1px solid #d9d2c3}}

Tabs:
```css
.tabs{display:flex;gap:0;border-bottom:1px solid #d9d2c3;margin-bottom:18px}
.tab{font-family:mono...;font-size:11px;letter-spacing:.12em;text-transform:uppercase;background:none;border:none;border-bottom:2px solid transparent;padding:10px 14px;cursor:pointer;color:#1d1b18}
.tab[aria-selected="true"]{color:#9b2335;border-bottom-color:#9b2335}
```

Rail bits:
```css
.rail-head{display:flex;justify-content:space-between;align-items:center;...}
#clear-all{...linkish}
.bignum{font-family:Georgia;font-size:46px;line-height:1;margin:14px 0 0}
.bigsub{...}
.of{color:#6f675a}
.chips{display:flex;flex-wrap:wrap;gap:6px;margin:10px 0}
.chip{border:1px solid #9b2335;color:#9b2335;background:#fff8;padding:2px 8px;border-radius:10px;cursor:pointer;font-size:10.5px}
```
chip font mono small; text-transform none? Chip labels like "Committees: CRC" — keep as-is (mixed case ok, or lowercase?). I'll not uppercase.

Search:
```css
.search{margin-top:16px;border-top:1px solid #d9d2c3;padding-top:14px}
#q{width:100%;padding:7px 8px;border:1px solid #b7ac97;background:#fffdf8;font:inherit}
#q-go{...button}
.syntax{border:1px solid #d9d2c3;background:#fbf8f1;padding:10px 12px;margin-top:6px}
.syntax ul{margin:6px 0;padding-left:18px;font-size:13px;line-height:1.5}
.syntax .ex{display:block;width:100%;text-align:left;margin:4px 0;padding:4px 8px;border:1px solid #d9d2c3;background:#fff;cursor:pointer;font:12px mono}
.normline{font-size:11px;color:#5d5648;line-height:1.5;margin:8px 0 0}
.echo{font-size:13px;margin:10px 0 0;color:#1d1b18;border-left:2px solid #9b2335;padding-left:8px}
.echo.err{color:#9b2335;border-left-color:#9b2335;font-weight:600}
```
Hmm .echo.err red — fine.

Accordion:
```css
.acc{margin-top:18px;border-top:1px solid #d9d2c3}
.acc-btn{width:100%;text-align:left;background:none;border:none;padding:12px 0 10px;cursor:pointer;font:11px mono uppercase ls;color:#1d1b18;display:flex;gap:8px}
.acc-btn .num{color:#9b2335}
fieldset{border:none;margin:0 0 14px;padding:0}
legend / .fhead {mono label}
.cb{display:block;margin:3px 0;font-size:13px}
.cb .code{font-family:mono;font-weight:700}
.cb .cnt{color:#6f675a}
```

Rows:
```css
.row{border-top:1px solid #d9d2c3;padding:12px 0 14px;cursor:pointer}
.row:first-child{border-top:none}
.row-h{margin:0 0 6px;font-size:15px;display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap;align-items:baseline}
.row-toggle{background:none;border:none;padding:0;cursor:pointer;text-align:left;font:inherit;font-family:inherit}
.badge{display:inline-block;border:1px solid #a2977e;font-family:mono;font-size:10px;letter-spacing:.06em;padding:0 5px;margin-right:4px;border-radius:2px}
.row-h .doc{font-style:italic}
.meta{font-size:11px;color:#5d5648}
.pin{color:#9b2335;font-weight:600}
.row-text{white-space:pre-wrap;margin:6px 0 4px;font-size:15.5px;line-height:1.6;cursor:pointer}
mark{background:#f3e6ad;color:#1d1b18;font-weight:700;padding:0 1px}
.row-sub{font-size:11px;color:#6f675a;margin:2px 0}
.linkish{background:none;border:none;padding:0;color:#5d5648;text-decoration:underline;cursor:pointer;font:inherit}
.row-sub .linkish{font-size:11px}
.ambernote{color:#7a4d00;font-size:13px;margin:6px 0 0}
.row-actions{margin-top:10px;display:flex;gap:10px;flex-wrap:wrap;align-items:center}
.row-actions>button{border:1px solid #8b8271;background:#fffdf8;padding:5px 10px;cursor:pointer;font:12px mono}
.stylenote{color:#6f675a;margin-left:auto}
.ctxblock{margin:10px 0 0;border-left:2px solid #b7ac97;padding:2px 0 2px 12px;color:#5d5648;white-space:pre-wrap;font-size:14px}
.ctxblock .pin{display:block;margin-bottom:2px}
.dim{color:#a99e86}
.more{display:block;margin:16px auto;padding:8px 18px;border:1px solid #8b8271;background:#fffdf8;cursor:pointer;font:12px mono}
```

Buttons general: ok.

Checks:
```css
.checks{list-style:none;padding:0;margin:0}
.checks li{border-top:1px solid #d9d2c3;padding:8px 0;font-size:14px}
.checks .res{font-weight:700}
.checks li.pass .res{color:#1e6b34}
.checks li.fail .res{color:#9b2335}
.checks li.fail{color:#1d1b18}
.quirks{padding-left:20px;font-size:14px;line-height:1.6}
.dot{display:inline-block;width:9px;height:9px;border-radius:50%;margin-right:6px}
.dot.green{background:#1e6b34}
.dot.red{background:#9b2335}
```

Copy status:
```css
.copystatus{min-height:18px;font-size:11.5px;color:#1e6b34;margin:0 0 10px;white-space:pre-wrap;max-height:5.5em;overflow:auto}
.fallback{border:1px solid #9b2335;padding:10px;margin-bottom:14px}
.fallback textarea{width:100%;height:110px;font:12px mono;white-space:pre-wrap}
```
copystatus color green? It shows "Copied: ..." — keep neutral #1e6b34 or ink. Use ink. Fine, I'll use color #1e6b34 for copied confirmation… The exact string is the content; keep ink color. I'll keep neutral.

Draft:
```css
.ditem{border-top:1px solid #d9d2c3;padding:10px 0}
.ditem blockquote{margin:0 0 4px;white-space:pre-wrap;font-size:15px}
.note-red{color:#9b2335;font-size:12px}
```

Fig:
```css
.figno{color:#9b2335;margin:0 0 2px}
.figtitle{font-family:Georgia;font-size:22px;margin:0 0 14px;font-weight:700}
.fig-flex{display:flex;gap:28px;align-items:flex-start;flex-wrap:wrap}
.chart-wrap{position:relative;flex:1 1 420px;min-width:320px}
.figtable{border-collapse:collapse;flex:0 0 auto;min-width:220px}
.figtable caption{text-align:left;color:#6f675a;padding-bottom:6px}
.figtable th,.figtable td{border-top:1px solid #d9d2c3;padding:4px 10px;text-align:left;font-size:13px}
.figtable td.num,.figtable th.num{text-align:right}
.hint{color:#6f675a;font-size:11.5px}
.compute{color:#6f675a;font-size:11.5px;max-width:70ch}
```

Header checks:
```css
.head-right{text-align:right;color:#1e6b34... set dynamically}
#head-checks.fail{color:#9b2335}
```

Footer:
```css
.site-foot{border-top:1px solid #d9d2c3;padding:12px 28px;color:#6f675a;font-size:11px}
```

Summary line:
```css
.rec-summary{font-family:Georgia;font-size:21px;margin:0 0 4px}
.orderline{...}
```

OK. Now — a11y: h1 in header; panels use h2; row headings h3. Fine.

Also `lang="en"`.

Potential pitfall: `Math.min(...years)` with 7,304 — fine but use reduce.

Another: CORDER from Object.keys(cCounts) — but cCounts keys added via r._committees.forEach — all codes present. Good.

Edge: wordBody loop `for(const ch of w)` — handles surrogate pairs fine.

Lookbehind in regex — supported in modern Chromium/Firefox/Safari 16.4+. OK.

The 'u' flag with escaped chars — escRe escapes properly. But careful: with 'u' flag, unnecessary escapes like \- or \/ are errors? In unicode mode, IdentityEscape only allows SyntaxCharacters and "/". escRe escapes .*+?^${}()|[]\ — all syntax chars — OK. '-' not escaped (fine, literal outside class). Curly quote chars in classes fine.

But wait — wordBody hl=true builds classes like [\u201C\u201D"] — fine. And the escaped chars from escRe — for e.g. '(' → '\\(' — allowed in u mode. Good.

One more: in buildHlRe, phrase gap `(?:\\s|\\[\\[fn:\\d+\\]\\])+` — \[ \] \d fine.

Another subtlety: highlightInto uses global regex with exec; the regex may match zero-length? Bodies always have ≥1 char. OK.

Potential catastrophic case: query with many terms OR'd — fine.

Performance: compile caching via node._fn — nodes are plain objects; fine.

orderHits 'matches' with cnt per comparison — O(n log n) with regex per compare; cache counts in Map first. I'll precompute a Map id→count.

Let me also handle `state.q.termsReNorm` for matches counting:
```js
function buildNormRe(terms){
  const alts=terms.map(t=>t.k==='WD'?B0+wordBody(normText(t.v),false)+B1:B0+normText(t.v).trim().split(/\s+/).map(w=>wordBody(w,false)).join('\\s+')+B1);
  return new RegExp('(?:'+alts.join('|')+')','gu');
}
```
Careful — normText(t.v) for phrase then split — normText collapses spaces. For WD, wordBody(normText(v)) — if v had '*' trailing, normText keeps it; wordBody strips. OK.

Hmm wait, order issue in wordBody: strip star BEFORE normalising? normText doesn't affect '*'. fine.

countTerms:
```js
function countTerms(n){if(!n)return 0;if(n.k==='WD'||n.k==='PH')return 1;return countTerms(n.l)+countTerms(n.r)+countTerms(n.v);}
```
Careful: NOT has .v; AND/OR have .l,.r. countTerms(n.v) for NOT: add. Let me: 
```js
function countTerms(n){if(!n)return 0;if(n.k==='WD'||n.k==='PH')return 1;if(n.k==='NOT')return countTerms(n.v);return countTerms(n.l)+countTerms(n.r);}
```

Now — committee "joint" appearing under both tick filters: the filter keeps record if ANY ticked — done.

Chart note about joints — in compute line. Also maybe an extra line when extra>0: `#chart-total`: `Bars sum to X = Y hits + Z joint records.` Show always.

Now — the records summary "8 committees" — distinct committees among hits via _committees union.

Also the tab-02 summary line should be aria-live — yes.

Now — one more plan requirement: header line "one line with the data's source, n and years" — includes link to source_url if present. gc fields: title, source, count, records — no source_url/built guaranteed. I'll link source to D.source_url when present.

Wait, the top-level gc might have more fields in reality. Guard everything.

Also — plan says the small monospace label "UN TREATY BODIES · GENERAL COMMENTS" and title "Verbatim finder: General Comments and General Recommendations". Good.

Draft tab label: "03 DRAFT (<span id=draft-n>0</span>)" — but .lab uppercase transform makes it "03 DRAFT (4)" anyway.

Now — write the "How this is computed" list (tab 4):
```html
<ul class="quirks">
<li><strong>Matching.</strong> Each paragraph is normalised once at load: footnote marks ([[fn:N]]) removed, curly quotes and apostrophes as their straight forms, en and em dashes as hyphens, all whitespace one space, lower case. The query is normalised the same way, so text pasted from Word still matches. Words match whole (child does not find children; type child*), any case.</li>
<li><strong>Hits.</strong> A paragraph is a hit when the Boolean tree is true over its normalised text and it passes the committee, year and document filters. Counting, filtering and sorting are done by this page's code; nothing is estimated.</li>
<li><strong>Highlight.</strong> The same terms, matched again over the text as shown, where quotes, apostrophes and dashes match their curly and straight forms and a phrase may cross a footnote mark. Terms after NOT are never highlighted.</li>
<li><strong>Order.</strong> Year, newest first, then document, then paragraph — or the order chosen on the Paragraphs tab. The hit set does not change.</li>
<li><strong>Citation.</strong> The record's symbol and pinpoint only: "para. N", "preamble" for paragraph 0, "subpara. (x)" for lettered sub-paragraphs. When a symbol holds more than one General Comment, the committee and the document's name come first (Dag Hammarskjöld Library short form). No symbol is invented.</li>
<li><strong>Quotation.</strong> The stored text with footnote marks removed; the leading number is dropped only when it equals the record's paragraph (the citation carries it). The full text is always copied, never the on-screen cut.</li>
<li><strong>Draft.</strong> Kept in this browser (localStorage when allowed, memory otherwise). Downloads are built from the collected fields; nothing leaves the browser and no model is called.</li>
</ul>
```
Wait "Dag Hammarskjöld Library short form" — style named "UN short form" on rows; in method I can say 'UN short form (symbol + pinpoint)'. Keep.

Now quirks list at load — done above.

One more consideration: the plan says tab 04 shows checks panel "open". Fine.

Also: "Clickable: 6" tab 4 — ok.

Now let me also double-check the records tab clickables count — fine.

Potential issue: clicking on row text toggles open — also selecting text to copy manually triggers click after selection? Mouse click after drag-selection fires click; users selecting text might accidentally toggle. Acceptable; also they can use buttons. Hmm, maybe restrict toggle to the heading button + rest of article except .row-text? Plan: "A click on a row opens it in place". Keep whole row but ignore clicks when a selection exists: `if(window.getSelection&&String(window.getSelection()))return;`. Nice touch, add.

Also the "show as stored" and "full" buttons are inside p.row-sub — inside article; they have data-act so handled before toggle. Links (symbol) handled. Good.

Now — draft storage: KEY='gc-verbatim-finder-draft'.

Load draft:
```js
try{const s=localStorage.getItem(KEY);if(s){const a=JSON.parse(s);if(Array.isArray(a))state.draft=a;}}catch(e){}
```
Only if storageMode local... getItem may throw — caught.

Also validate items have id etc. Light validation: filter items with id and citation. OK.

After load: $('#draft-n').textContent=state.draft.length.

Now, big consideration — RE-RENDER of records panel on update(): state.open/mode/ctx persist — good.

Also when query changes, previous marks/highlights recompute — buildRow uses state.q.hlRe. Good.

Order select label update:
```js
const ORDER_DESC={year:'year, newest first, then by document and paragraph',doc:'document order, then paragraph',matches:'most matched terms first'};
```

Now — "Show 25 more" button label with remaining count. Also maybe "showing X of Y"? The button covers it.

Empty hits message.

Now, header line HTML:
```js
$('#head-line').innerHTML=fmt(R.length)+' paragraphs from '+fmt(titles.size)+' General Comments of '+allCodes.size+' committees, '+YMIN+'–'+YMAX+(D.source?(' · '+((D.source_url&&isUrl)?('<a href="'+esc(D.source_url)+'" target="_blank" rel="noopener">'+esc(D.source)+'</a>'):esc(D.source))):'');
```
Hmm source_url might not exist; check typeof.

Footer: `${esc(D.source||'')} ${D.built? ' · built '+esc(String(D.built)) : ''} · Counting, matching and sorting are done by this page’s code; no model is called. · Chart.js 4 (MIT licence).`

Hmm — is Credits needed? "If you use code or wording from a Reference shelf excerpts page that has an open licence... add Credits". Chart.js is preloaded, not from reference shelf — but the plan's footer spec explicitly says "A Credits line if shelf code is reused (Chart.js, MIT)". I'll include "Built with Chart.js (MIT licence)."

Now — one more spec item: "the canvas has role='img' and an aria-label stating the numbers, and a small table with the same numbers beside it". Done.

"axis from zero" — beginAtZero. "ranked by value" — sort labels desc. "the value at the end of the bar" — plugin. "at most ten light gridlines" — maxTicksLimit:10. "gaps narrower than a bar" — categoryPercentage .9, barPercentage .85.

Now — think about Chart.js responsiveness: canvas inside .chart-wrap with position:relative and set height. Chart maintainAspectRatio:false with wrapper height. Wrapper height set dynamically: `${labels.length*46+40}px`.

One catch: when panel-1 hidden and buildChart called... I only call buildChart when tab 1 active. update() calls renderPanel → if tab===1 buildChart. Good. When switching to tab 1 → buildChart. But the check "chart total" uses chart instance if exists — when tab 1 inactive, arithmetic. Fine.

Wait — there's an ordering problem in update(): renderPanel() (buildChart) then runChecks() reads chart — good.

Now — the syntax dropdown: it's inside rail; z-index above? It's in normal flow (pushes content). Fine.

Let me also handle "Enter searches" — done in keydown.

Also — clicking "Search" button: runSearch. 

Search button id q-go, label "Search".

Also — input 'input' event hides syntax; but what if user clears text — syntax reopens only on focus. OK.

Now — potential XSS via query echo: echoLine contains user text; I set textContent — safe. Notes etc. escaped.

Record text into HTML — escaped via esc in highlightInto. Good.

data-ref attribute values escaped with esc() for quotes — ids are safe anyway.

Now — one thing about `.row{cursor:pointer}` — the whole article clickable. Add title? no.

Accessibility of row toggle button: aria-expanded. Good.

The records list container: `<div id="rec-list" role="list"?` — articles with headings fine without list role. Keep plain div.

Live regions: #big-num aria-live polite (in rail), #rec-summary aria-live, #copystatus aria-live. Good.

Now — write the doc select build:
```js
const docsel=$('#docsel');
const byCmt=new Map();
R.forEach(r=>{if(!byCmt.has(r.committee))byCmt.set(r.committee,[]);const a=byCmt.get(r.committee);if(!a.some(x=>x.title===r.title))a.push(r);});
[...byCmt.keys()].sort().forEach(c=>{
  const og=document.createElement('optgroup');og.label=c;
  byCmt.get(c).sort((a,b)=>a.short_title.localeCompare(b.short_title)).forEach(r=>{
    const o=document.createElement('option');o.value=r.title;o.textContent=r.short_title;og.appendChild(o);
  });
  docsel.appendChild(og);
});
```
Hmm committee keys sort: alphabetical fine. Also the blank option first: `<option value="">All documents (N)</option>` — N=titles.size.

docsel change:
```js
docsel.addEventListener('change',()=>{state.doc=docsel.value;state.shown=25;update();});
```
Focus: select is in rail (static DOM) — retained. 

Year inputs change:
```js
function yearsFromInputs(){
  let a=parseInt($('#yfrom').value,10);let b=parseInt($('#yto').value,10);
  if(!isNaN(a))a=Math.max(YMIN,Math.min(YMAX,a));else a=YMIN;
  if(!isNaN(b))b=Math.max(YMIN,Math.min(YMAX,b));else b=YMAX;
  if(a>b){const t=a;a=b;b=t;}
  state.yFrom=a;state.yTo=b;$('#yfrom').value=a;$('#yto').value=b;
  update();
}
```
Hmm — swapping while typing is odd (change fires on blur/enter). Acceptable.

Wait: if a>b I swap and rewrite inputs — maybe better to just set both to the valid pair without swap: if a>b, swap. OK.

Now — update() calls orderHits which needs state.q.termsReNorm — present.

hits variable module-level; runChecks uses hits & ordered.

Also — "Clear all" resets shown/open? Keep open rows. Fine.

Let me now also decide tab names: "01 OVERVIEW", "02 PARAGRAPHS", "03 DRAFT (n)", "04 CHECK & METHOD". aria-label "Sections". Panel titles via aria-labelledby.

Roving tabindex init: tab1 tabIndex 0, others -1.

One more: role="tablist" arrow nav implemented.

Also `qInput.focus()` at end of init — inside try? If iframe sandbox... fine.

Now — the fallback textarea and copystatus are placed between tabs and panels; visible only when used. copystatus always in DOM (min-height reserved). fallback hidden until needed; hide it when? Next successful copy could hide: in copyText success: $('#fallback-copy').hidden=true. OK.

Now let me also double check `highlightInto` with regex that has lookbehind — exec fine.

Wait — one bug risk: hlRe built with 'giu'; using .exec loop resets lastIndex manually (re.lastIndex=0 at start). Between rows, lastIndex persists after last exec returning null → reset to 0 automatically when exec returns null. But if a row's loop ends because exec returned null, lastIndex=0. If loop completes normally (last=...), lastIndex at 0 after final null. Safe to reset at function start anyway. Done.

hlTest (non-global 'iu') — .test no lastIndex issue.

Now — checks: highlight check uses hlTest on clean text. But when notOnly — skip. When q err — skip (no hits anyway).

Edge: query like `child* OR -child` — whatever.

Now — "Normalisation" check presence condition: state.q.straightTerms.length. Also require hits>0? If 0 hits, line: "...and 0 hits matched only through a curly or dash form." Keep, fine.

Hmm — one more thing about strictTest for phrases: raw text may contain line breaks between phrase words — \s covers; and footnote marks in gap — included; but strict should ALSO fail when mark sits INSIDE gap? The normalised match treats marks as removed (whitespace). Strict with (?:\s|\[\[fn:\d+\]\])+ gap also bridges marks — so a phrase crossing a footnote isn't "variant-only". Fine — the normalisation note is about quotes/dashes anyway.

Now, a subtle correctness issue with strictTest word boundaries: wordBodyStrict lacks B0/B1? I add B0/B1 around. Yes: body=B0+wordBodyStrict(v)+B1.

Now — implement wordBodyStrict:
```js
function wordBodyStrict(w){
  let star=false;if(w.endsWith('*')){star=true;w=w.slice(0,-1);}
  let out='';for(const ch of w){out+=escRe(ch);}
  return star?out+'\\w*':out;
}
```

And wordBody(w,hl):
```js
function wordBody(w,hl){
  let star=false;if(w.endsWith('*')){star=true;w=w.slice(0,-1);}
  let out='';
  for(const ch of w){
    if(hl){
      if(ch==='"'){out+='[\u201C\u201D"]';continue;}
      if(ch==="'"){out+='[\u2018\u2019\']';continue;}
      if(ch==='-'){out+='[-\u2013\u2014]';continue;}
    }
    out+=escRe(ch);
  }
  return star?out+'\\w*':out;
}
```
Wait — for norm matching (hl=false), w should already be normText'd (so curly in query → straight). wordBody(normText(v),false). For hl=true, use raw v.

Hmm — but wait: for the norm match, if query word contains an en dash, normText converts to '-', and text norm has '-' too. Good.

Now — `termMatcher`:
```js
function termMatcher(t){
  if(t.k==='WD')return mkWord(normText(t.v));
  return mkPhrase(normText(t.v));
}
function mkWord(nw){const re=new RegExp(B0+wordBody(nw,false)+B1,'u');return s=>re.test(s);}
function mkPhrase(np){const re=new RegExp(B0+np.trim().split(/\s+/).map(w=>wordBody(w,false)).join('\\s+')+B1,'u');return s=>re.test(s);}
```
Wait — for phrase, split AFTER normText collapses whitespace. But normText of the phrase also lowercases. But splitting: normText returns single-spaced; split(/\s+/). OK. But careful: phrase words with '*' — wordBody handles.

BUT: subtle — mkWord on normText(t.v): if t.v contains '(' etc — tokeniser prevents (words can't contain parens). Phrases can contain parens! e.g. "general comment (2000)" hmm — a phrase "reason No. 5 (2003)". escRe escapes parens. Good.

Another subtle: normText on phrase converts internal quotes — but phrase content came from between quotes; internal curly quotes → straight — matches text norm. Good.

Now compile() caches node._fn — nodes reused across searches? Each search builds new tree. Fine.

NOT-only: tree.k==='NOT'. Also `(NOT a)` → root NOT. `-a` → NOT. But `a AND -b` root AND — notOnly false, terms=[a]. Good.

Now — the plan's check 1 "Query understood. The English echo and the number of terms". Include both.

Also: when rawQ non-empty but q null? Can't happen (runSearch sets q for non-empty; err otherwise). rawQ tracked for... nothing much. Skip rawQ.

Now — Draft tab render note about counts of check: runChecks triggers renderChecksPanel only if tab 4 active; and updates header always. When on draft tab and item removed — header updates. Good.

Now — potential problem: `update()` re-renders active panel; when on tab 2, renderRecords rebuilds rec-list — open rows preserved via state. Focus: clicking a committee checkbox (in rail) — focus stays in rail. Good. Typing search + Enter — focus in input (rail). Good. So focus issues only for panel-local actions (handled by rerow refs; order select static; show more static).

Wait — order select is inside panel-2 static header; renderRecords doesn't touch it. 

Now — countsByCommittee called multiple times per update (rail + chart + checks) — cheap enough; or compute once in update() and store. I'll compute once: `state.cc=countsByCommittee(hits)` in update; runChecks reuses. buildChart uses too. updateRail uses.

Let me now also think: does Chart exist? window.Chart preloaded. Guard if missing: if(!window.Chart) show table only + message. Add small guard.

Now, word count line: "Show the full paragraph (1,287 words)" — wc from raw text.

One more plan item: rows show committee badge AND short_title; the symbol link; pinpoint; year. Done.

"An amber note sits on the row when needed" — done.

Tab 2 hint — done.

Now — special case: `state.q` err → hits=[]; big number 0; echo error; summary "Search not understood…". checks: query line fail. Fine.

Also empty query and no filters: hits=R; summary "7,304 of 7,304 paragraphs match (no search words) · 10 committees · 1972–2026".

Now — one more possible gotcha: records with year as string? Spec says int. Coerce: r.year maybe number. Use as-is; sorting with minus works for numbers. If strings, minus gives NaN... trust spec. I'll coerce once: r._year=+r.year||0? Hmm, that could break display. Trust the spec (int).

paragraph: int per spec.

OK — also `r.paragraph||0` in sorts — paragraph 0 valid; use (r.paragraph||0) fine (0→0).

For pinpoint 'preamble' when paragraph===0 — `if(!r.paragraph)` catches 0 and undefined. Good.

Now, writing the checks list items with esc() where user/data text included.

Let me write the full "Known quirks" injection at load:
```js
$('#quirks-list').innerHTML=quirks.map(q=>'<li>'+q+'</li>').join('');
```
quirks strings built with esc on symbols.

Alright — also the plan says the rail's big number aria-live — set attribute in HTML.

One more requirement: "Works on a laptop screen without horizontal scrolling." — flex layouts, wrap. Chart width flexible.

"Readable at projector distance, contrast at least 4.5:1" — check greys: #6f675a on #f4f0e8 — contrast? #6f675a is medium grey-brown; roughly L ~0.16? Let me estimate: rgb(111,103,90) → relative luminance ≈ 0.147; bg #f4f0e8 ≈ 0.87. Contrast = (0.87+0.05)/(0.147+0.05) ≈ 4.7. OK borderline pass. Use #5d5648 for hints (darker): rgb(93,86,72) lum ≈ 0.105 → contrast ≈ 5.9. I'll use #5d5648 for secondary text and #6f675a sparingly (big "of" text ok since large? keep #5d5648 mostly). Let me set hints #5d5648.

Amber #7a4d00: rgb(122,77,0) lum≈0.096 → 6.2. Good. Green #1e6b34: rgb(30,107,52) lum≈0.116→5.6. Good. Red #9b2335: lum? rgb(155,35,53): ≈0.09 → 6.3. Good. Dim #a99e86 — only for disabled "previous/next" placeholders — low contrast; disabled controls are exempt-ish, but let me use #7d7462 with note. Eh, keep .dim #867c68 (decorative). Fine.

mark: background #f3e6ad with #1d1b18 text — high contrast. Good.

Now — let me also add `.tab .dot` small red dot in tab 4: `<span class="dot red" id="tab4-dot" hidden></span>` inline-block.

Now, an important detail — tab buttons contain span#draft-n; with uppercase transform fine.

Let me now also handle: rail hidden on draft tab — but tabs are in main; when rail hidden, layout fine.

Also — the accordion default closed; but on first load user may not find filters. The plan wants it closed. OK.

Let me also make sure the search "runs" initial: q empty; hits all.

Init call order:
```js
buildRail(); // committees, docsel, years defaults
wireTabs(); wireSearch(); wireRecords(); wireDraft(); loadDraft();
update();
qInput.focus();
```

update() → updateRail needs #cnt spans — exist after buildRail. Good.

Now — one more thought on `renderRecords` when panel hidden (tab 1 active): don't render; when switching to tab 2, setTab calls renderRecords. But renderRecords reads hits — fine.

Also runChecks DOM-row count: only when panel-2 visible. Else arithmetic min(shown, len). Good.

Edge: state.shown persists across searches? runSearch resets to 25. Filter changes (committee/year/doc) — also reset shown? Sensible: reset to 25 on any filter change. Let me reset state.shown=25 in those handlers. Hmm — but then "show 25 more" lost on filter change — that's fine/expected.

Actually simpler: reset in update()? No — show-more calls renderRecords directly, not update. runSearch and filter handlers reset. OK.

Now — write everything. Also add `<noscript>` note? Eh.

Let me make sure I don't exceed line budget — I'll write compact CSS.

One more detail: "Copied" message: "Copied: CCPR/C/GC/37, para. 12". For fallback: message + box. The aria-live shows exact string sent — in fallback case the exact string is in the textarea. Fine.

Also copyStatus element id 'copystatus'.

Let me write the highlightInto with the ellipsis: display+(cut?' …':'') then highlight — the ellipsis char '…' appended after; if a phrase matches up to end... fine.

Also — the "…" should be styled maybe. Fine.

Word cut: `display=base.slice(0,700); const sp=display.lastIndexOf(' '); if(sp>300)display=display.slice(0,sp);` — if no space after 300, keep 700 hard cut (mid-word acceptable rare). OK.

Now — records summary years: if hits non-empty compute min/max.

Also "8 committees" — count distinct committees across hits.

Now — think about `docShort(title)`:
```js
function docShort(title){const r=R.find(x=>x.title===title);return r?(r.short_title||r.title):title;}
```
R.find over 7304 — fine (rare).

Chip for doc label: 'Document: '+short (may be long; CSS max-width + ellipsis? white-space normal fine).

Now — implement `keepFocus`? I decided not needed. Skip.

One more a11y: accordion button aria-controls. Fine.

Also the "all / none" — small buttons in committee fieldset.

Let me write HTML for the accordion panel:

```html
<div class="acc-panel" id="acc-panel" hidden>
  <div class="fgroup">
    <p class="lab">Committee</p>
    <p class="mono small"><button class="linkish" id="cb-all">all</button> / <button class="linkish" id="cb-none">none</button></p>
    <div id="cbs"></div>
  </div>
  <div class="fgroup">
    <p class="lab">Years</p>
    <p class="mono small"><input type="number" id="yfrom" class="yr"> – <input type="number" id="yto" class="yr"></p>
  </div>
  <div class="fgroup">
    <p class="lab">Document</p>
    <select id="docsel"></select>
  </div>
</div>
```

The joint note about chart is on overview; also maybe under committee fieldset: "A joint General Comment appears when either committee is ticked and shows both badges." Add as small hint. Good.

Now — writing the final code. Let me also compute `state.cc` in update.

Let me write out the entire file now, carefully.

Also — one more thought about `esc` for attribute values in innerHTML strings (doc_url). esc handles quotes. Good.

For `data-ref="open-${r.id}"` — r.id safe chars.

Potential issue: `CSS.escape` may not exist in old browsers — assume modern.

Let me also double-check the parseAnd loop for query like `a b`:
tokens: W a, W b. parseOr→parseAnd→parseNot→parsePrim(W a). loop: peek W b → not OR/')' → not AND → r=parseNot→parsePrim(b) → AND node. loop: no more → return. Good.

Query `a OR b`: parseAnd→a; loop: peek OR → break; parseOr sees OR → p++, parseAnd→b → OR node. Good.

`NOT a b`: parseNot consumes NOT, prim a → NOT(a). parseAnd loop: peek W b → implicit AND with parseNot(b). Result: (NOT a) AND b. Good.

`-a OR b`: tokens NOT, W a, OR, W b: parseNot→NOT(a); loop peek OR break; parseOr: OR → b. → OR(NOT a, b). Good.

`(torture OR ill-treatment) NOT detention`: tokens: ( W W OR W-ill-treatment ) NOT W. parsePrim '(' → parseOr inside → torture OR ill-treatment; ')' consumed. parseAnd loop: peek NOT → not OR/')' → r=parseNot → NOT(detention) → AND. 

Echo: "the word “torture” or the word “ill-treatment” and not the word “detention”". Precedence in echo string without parens could mislead, but fine.

Phrase with star: `"best interest*"` — phrase words with star; wordBody adds \w*. OK.

Now — potential issue: word token containing quotes like `don't` (apostrophe inside word): tokenizer: apostrophe not in OPEN set (only double quotes), so `don't` is one word. Good — apostrophes are word chars here.

Word containing double quote mid-word: `say"hello` — the `"` starts a phrase token, so word ends before it. Edge acceptable.

Now — highlightInto boundary issue: hlRe has B0/B1 lookbehind/lookahead per alternative. Combined with 'g' flag — fine.

Hmm — one thing: hlRe alternatives combine word and phrase patterns; a word like "a" (single letter) with boundaries — matches standalone "a". fine.

Now — Chart.js accessibility doc: fallback content inside canvas. Note: Chart.js will draw over it. OK.

Now — write the code. I'll aim for clarity with comments minimal.

Also — plan says rail big number "279 matching paragraphs" with "of 7,304". Implement.

One more plan line: left rail "Headed 'FILTERS', with 'Clear all'." Done.

Also — "One big serif number ... (`aria-live`)". Done.

Let me also reconsider the tab count label: "The tab name carries the count: '03 DRAFT (4)'." Done via span.

Draft title: "Your draft (n quotations)".

Now — writing time. Let me carefully produce the file.

Additional check — the `#q` label: `<label class="lab" for="q">Search</label>`.

Syntax panel — put TRY buttons with type="button" (default in button). All buttons default type="button"? In HTML default is "submit" only inside forms; no forms here. Fine.

Now, edge: `wordBody` for hl on raw word that includes '*' — stripped before char loop. Yes.

Edge: term raw word could be just '*' → after strip, empty body with \w* → matches every word boundary... B0\w*B1 matches single letters etc. Whatever.

Empty phrase check in tokenizer: throws. Good.

Now — `runSearch` when input empty → q=null, update. Good.

Also — after runSearch, keep focus in input: input is static rail DOM — retained.

Wait — one problem: `syn.hidden=true` after running example, and qInput.focus().

Now — checks "Query understood" when q null: "Query: no search words — filters only." pass.

Hmm — the plan's checks list includes "Query understood" always. OK.

Now — counts: how many checks: query, totals-rows, totals-committees, chart, highlight, [normalisation], numbering, marks, draft = 8-9. Header "9 checks pass". Good.

Now — implement `renderChecksPanel` with sections; quirks static; method static.

Also plan: tab 4 "Below, 'How this is computed': the next section in short form." Done.

Let me now also double check countsByCommittee extra: joint record committees {CMW,CERD} size2 → extra+1. But also — CAT/OP: my recCommittees for symbol "CAT/OP/..." adds only CAT-OP (size could be 1 with committee CAT-OP). But what if committee field is "CAT" while symbol "CAT/OP/..."? Then committees={CAT-OP,CAT} size2 → marked joint wrongly! Hmm. Does that happen? The plan says committee codes: "10 committee codes (CRC 2,091 … CED 56; CAT-OP is the Subcommittee...)". So committee field for SPT records is "CAT-OP". And symbol "CAT/OP/...". So my else-branch: sym has CAT/OP → add CAT-OP; committee CAT-OP → {CAT-OP}. size1. Good.

But wait — SPT general comments symbols: actual SPT documents are "CAT/OP/...". OK.

Hmm, but one more: are there records with committee "CAT-OP" but symbol without CAT/OP? Then committees={CAT-OP} only. Fine.

And joint: symbol with two codes. But ALSO — what about committee field for joint records: e.g. "CMW/C/GC/7–CERD/C/GC/38" with committee maybe "CMW" — codes {CMW,CERD} ∪ {CMW} = {CMW,CERD}. size2 → joint. 

But here's a subtle issue for the chart note "Joint General Comments count under both committees" — with committees {CMW,CERD}, ticks: record passes if CMW or CERD ticked. Bars: counted under both. Brackets show both. Matches plan.

Edge risk: a record whose symbol legitimately contains two codes but is NOT joint — I can't think of one in gc data (e.g., a GC published in a joint session...). Accept.

Hmm — wait, actually there's a real case: "CRC/C/GC/23, CMW/C/GC/4" hmm that IS joint. And "CMW/C/GC/7–CERD/C/GC/38" hmm wait actually I should double check the en dash forms: plan says en dash "–". My CODE_RE with \b works around it: "GC/7–CERD" — between "7" and "–" ... \b(CERD)\b: before C is "–" (non-word) → boundary. Good.

Now — one more consideration on `_joint` detection: I use committees.size>=2. But suppose symbol "A/48/18" (annual report) with committee "CERD" → {CERD}. fine.

Now — potential issue: `\b(CRC)\b` matching "CRC" inside "CRC/C/GC/23, CMW/C/GC/4" — yes both.

OK. Also — CED symbols: "C/CED/..."? \b(CED)\b: "C/CED/" — before CED is "/", boundary; after D is "/" → match. Good.

Now — write it all.

Actually — one more thing: the header "n General Comments (distinct title)" — 188 distinct titles but 159 distinct symbols; plan header: "`records.length` paragraphs from n General Comments (distinct `title`) of k committees, `year` min–max". So n = distinct titles = 188? Hmm the plan's data notes say "A symbol is not a document: 159 distinct symbol, 188 distinct title." and header uses distinct title. OK — "7,304 paragraphs from 188 General Comments of 10 committees, 1972–2026". Follow plan.

Also — hmm, distinct title 188 > symbols 159 because HRI/GEN pages etc. Fine.

Let me also prepare `isSafeUrl`: only link http(s). D.source_url if begins with http. Simple check.

Now writing the final HTML. I'll be careful with the details. Also keep IDs consistent.

Also: CSS for `.small{font-size:11px}`.

Order line layout: "sorted by year, newest first... | order: [select]". 

Let me write the summary line example format check: "279 of 7,304 paragraphs match · 8 committees · 1990–2023". Good.

Now — one more: the rec-summary is serif per plan? "A summary line (aria-live)" — big-ish. I'll make it serif 20px. Good.

Also — panel-2 needs the list max width ~ 75ch for readability: .main content width; rows text max-width: 78ch. OK.

Draft CSV/txt filenames: 'general-comments-draft.txt' / '.csv'.

Now, code the checks examples capping: `ex(list, n=3)`.

Now — writing. Also remember `[hidden]{display:none!important}`.

Also — Chart defaults font family: set Chart.defaults? I'll set in options per scale ticks and plugin font. Also tooltip font whatever.

Chart onClick: need access to labels — define inside buildChart closure.

Potential problem: Chart requires canvas parent with position relative for responsive sizing. .chart-wrap{position:relative}. Good.

Let me write valuePlugin with chartArg.

Also — bar color: '#9b2335'. Hover color slightly darker? Keep same; set hoverBackgroundColor '#7c1c2a'.

Border radius 0. barPercentage .82, categoryPercentage .92 — gaps narrower than bars? barPercentage .82 means bar occupies 82% of category slot... with categoryPercentage .92 → bar width = .82*.92 of slot ≈ .75, gap .25 → gap narrower than bar. Good.

x grid color '#e7e0d1' (light), border (axis line) color '#d9d2c3'.

Ticks callback to format numbers with commas? Values up to ~2091 — fmt. Use callback: v=>fmt(v).

suggestedMax: max*1.15 to leave room for end labels.

Now — the aria-label must state numbers — done.

Also chart title? The fig title is HTML above. plugins.title display false.

Tooltips default fine; maybe disable to keep quiet? Keep enabled (helpful). Set tooltip callbacks label: ctx=>fmt(ctx.parsed.x). Fine.

Now — final structure of script. Let me write it in one IIFE.

Also — 'use strict'.

Let me also remember: `D.count` is string "7304" — we use R.length. Good.

Potential large innerHTML for rec-list: 25 rows with up to 700 chars each — fine.

Let me write the checks line HTML carefully with escaping.

One more: `#head-checks` styling: mono, with dot span. Set class ok/fail for color.

Alright — also handle the situation `window.Chart` missing: buildChart guards: if(!window.Chart){canvas replaced by message; table still shows numbers.}

Write it:

```js
function buildChart(){
  const labels=CORDER.slice().sort((a,b)=>state.cc.c[b]-state.cc.c[a]);
  const data=labels.map(k=>state.cc.c[k]);
  const wrap=$('#chart-wrap');
  wrap.style.height=Math.max(220,labels.length*46+36)+'px';
  $('#chart-tbody').innerHTML=labels.map((l,i)=>'<tr><th scope="row">'+esc(l)+'</th><td class="num">'+fmt(data[i])+'</td></tr>').join('');
  const cv=$('#chart');
  cv.setAttribute('aria-label','Bar chart, paragraphs per committee: '+labels.map((l,i)=>(CMTY_FULL[l]||l)+' '+fmt(data[i])).join('; ')+'.');
  $('#chart-total').textContent='Bars sum to '+fmt(data.reduce((a,b)=>a+b,0))+' = '+fmt(hits.length)+' hits + '+fmt(state.cc.extra)+' double-counted joint records.';
  if(!window.Chart){cv.getContext('2d').clearRect... just skip; return;}
  if(chart){chart.destroy();}
  chart=new Chart(cv,{...});
}
```
Note: canvas fallback text inside — Chart.js uses canvas content? It reads font attrs; inner text ignored. Fine.

Careful: creating Chart on a canvas that already has a chart → destroy first (done).

x-axis ticks maxTicksLimit 10.

Now — writing final answer. Pre-code text: at most three short sentences describing what I built. Then the single html block. Nothing after.

Let me now write out the whole thing mentally-checked line by line.

Regarding the doc select label widths: rail 300px; select width 100%.

Also inputs number width 80px.

CSS for .yr{width:76px;padding:4px 6px;border:1px solid #b7ac97;background:#fffdf8;font:inherit}

Let me write the syntax list markup with the plan's wording (fresh words, fine).

Potential issue: uppercase transform on .lab applied to tab buttons — tab text contains "&" fine.

Draft tab label: `03 DRAFT (<span id="draft-n">0</span>)` — inside uppercase transform, numbers unaffected.

Now — a tricky bit: `#tab4-dot` inside tab button: `<span class="dot red" id="tab4-dot" hidden></span>` — hidden attr with [hidden] rule — display:none important. Good.

Also — plan: header right shows checks status — `#head-checks` `<span class="dot ...">` + text. Implement innerHTML with span.

Let me also compute `state.cc` before updateRail uses it: in update(): hits=...; state.cc=countsByCommittee(hits); ordered=...; updateRail(); renderPanel(); runChecks();

Wait — orderHits needs termsReNorm only. fine.

renderPanel: tab1 → buildChart (uses state.cc, hits). tab2 → renderRecords (uses ordered, hits). tab3 → renderDraft. tab4 → nothing (runChecks renders).

runChecks after renderPanel. In runChecks, chart check: if(chart){sum=chart.data.datasets[0].data.reduce(...)} else arithmetic.

Hmm — chart.data.datasets[0].data are numbers. Good.

Now — let me also ensure the "rows listed" check reads DOM only when panel-2 visible: `!$('#panel-2').hidden`.

Write runChecks:

```js
function runChecks(){
  const L=[];
  const q=state.q;
  if(!q)L.push({ok:true,html:'Query understood: no search words — filters only.'});
  else if(q.err)L.push({ok:false,html:'Query not understood: '+esc(q.err)+'.'});
  else L.push({ok:true,html:'Query understood: '+esc(q.echo)+' · '+q.termCount+' term'+(q.termCount===1?'':'s')+'.'});
  const vis=!$('#panel-2').hidden;
  const listed=vis?$('#rec-list').querySelectorAll('article.row').length:Math.min(state.shown,ordered.length);
  const rest=Math.max(0,ordered.length-listed);
  L.push({ok:listed+rest===hits.length&&listed<=hits.length,html:'Totals: '+fmt(listed)+' rows listed + '+fmt(rest)+' waiting = '+fmt(hits.length)+' hits.'});
  const sumBr=CORDER.reduce((a,k)=>a+state.cc.c[k],0);
  L.push({ok:sumBr===hits.length+state.cc.extra,html:'Committee brackets sum to '+fmt(sumBr)+' = '+fmt(hits.length)+' hits + '+fmt(state.cc.extra)+' joint double-count.'});
  const chartSum=chart?chart.data.datasets[0].data.reduce((a,b)=>a+b,0):sumBr;
  L.push({ok:chartSum===hits.length+state.cc.extra,html:'FIG.01 bars sum to '+fmt(chartSum)+' = '+fmt(hits.length)+' hits + '+fmt(state.cc.extra)+' joint.'});
  ...
```
Hmm the rows check: listed + rest === hits.length — rest computed as max(0, ordered.length - listed) → always equals. Trivial pass unless DOM mismatch (listed > min(shown,len) would make rest 0 and sum ≠ len → fail). Actually if DOM has fewer rows than expected (bug), rest = len - listed, sum = len — still passes! Let me compute expected=Math.min(state.shown,ordered.length) and ok = listed===expected. Better:
```js
const expected=Math.min(state.shown,ordered.length);
L.push({ok:listed===expected&&listed+Math.max(0,ordered.length-expected)===ordered.length, ...});
```
Second clause trivial; keep first. Fine.

Highlight:
```js
  if(q&&!q.err){
    if(q.notOnly)L.push({ok:true,html:'Highlight: the query only excludes terms (NOT), so nothing is highlighted.'});
    else if(!q.hlRe)L.push({ok:true,html:'Highlight: no positive terms to highlight.'});
    else{
      const miss=hits.filter(r=>!q.hlTest.test((r.text||'').replace(/\[\[fn:\d+\]\]/g,'')));
      L.push(miss.length?{ok:false,html:'Highlight: '+miss.length+' hit'+(miss.length===1?'':'s')+' matched the normalised text but show no highlight ('+exList(miss)+'); still listed.'}:{ok:true,html:'Highlight: each of the '+fmt(hits.length)+' hits shows at least one highlighted word.'});
    }
  } else L.push({ok:true,html:'Highlight: no search words, nothing to highlight.'});
```
q.hlTest built alongside hlRe: `q.hlTest = q.hlRe? new RegExp(q.hlRe.source,'iu'):null`.

Normalisation:
```js
  if(q&&!q.err&&q.straightTerms.length){
    let n=0;
    hits.forEach(r=>{if(q.straightTerms.some(t=>t.normTest(r._norm)&&!t.strictTest(r.text||'')))n++;});
    const chars=[...new Set(q.straightTerms.reduce((a,t)=>a.concat(t.chars),[]))].join(' and ');
    L.push({ok:true,html:'Normalisation: the query holds a straight '+chars+'; curly and dash forms were matched too, and '+fmt(n)+' hit'+(n===1?' matches':'s match')+' only through a curly or dash form.'});
  }
```

Numbering:
```js
  const lm=hits.filter(r=>r._leading!=null&&r._leading!==r.paragraph);
  const dp=hits.filter(r=>r._dup);
  const sb=hits.filter(r=>r._lettered);
  const parts=[];
  if(lm.length)parts.push(fmt(lm.length)+' leading-number mismatch'+pl(lm)+' (e.g. '+esc(lm[0].symbol)+': text begins “'+lm[0]._leading+'.”, record para. '+lm[0].paragraph+')');
  if(dp.length)parts.push(fmt(dp.length)+' shared pinpoint'+pl(dp)+' (e.g. '+esc(dp[0].symbol)+', '+esc(dp[0]._pin)+')');
  if(sb.length)parts.push(fmt(sb.length)+' lettered sub-paragraph'+pl(sb));
  L.push({ok:true,html:'Numbering: '+(parts.length?parts.join('; ')+'. Each is flagged on its row.':'no numbering quirks among the hits.')});
```
pl(n)=n.length===1?'':'s'.

Marks:
```js
  const mb=hits.filter(r=>{const t=r.text||'';const well=(t.match(/\[\[fn:\d+\]\]/g)||[]).length;const opens=(t.match(/\[\[fn:/g)||[]).length;return well!==r._marks||opens!==well;});
  L.push(mb.length?{ok:false,html:'Footnote marks: '+mb.length+' hit'+pl2+' where the marks do not round-trip ('+exList(mb)+').'}:{ok:true,html:'Footnote marks: for all '+fmt(hits.length)+' hits, marks removed = marks counted and every “[[fn:” is a well-formed mark.'});
```

Draft:
```js
  if(!state.draft.length)L.push({ok:true,html:'Draft: empty.'});
  else{
    const bad=state.draft.filter(d=>{const r=byId.get(d.id);return !r||r.text!==d.text_as_stored;});
    L.push(bad.length?{ok:false,html:'Draft: '+bad.length+' of '+state.draft.length+' item'+pl(bad)+' no longer match the stored text of their records (first: '+esc(bad[0].citation)+'); the item is marked.'}:{ok:true,html:'Draft: all '+state.draft.length+' item'+(state.draft.length===1?'':'s')+' match the stored text of their records.'});
  }
```

exList(rs)=rs.slice(0,3).map(r=>esc(r.symbol)+', '+esc(r._pin)).join('; ')+(rs.length>3?'; …':'').

Header:
```js
  const fails=L.filter(x=>!x.ok).length;
  const hc=$('#head-checks');
  hc.className='mono head-checks '+(fails?'fail':'ok');
  hc.innerHTML=fails?'<span class="dot red"></span>'+fails+' check'+(fails===1?'':'s')+' failed':'<span class="dot green"></span>'+L.length+' checks pass';
  $('#tab4-dot').hidden=!fails;
  state.checks=L;
  if(state.tab===4)renderChecksPanel();
```

Good. renderChecksPanel:
```js
function renderChecksPanel(){
  $('#checks-list').innerHTML=state.checks.map(c=>'<li class="'+(c.ok?'pass':'fail')+'"><span class="res">'+(c.ok?'pass':'check failed')+'</span> — '+c.html+'</li>').join('');
}
```

Now init quirks list etc.

One more: the plan wants "Known quirks of this file" BEFORE any search — it's static, computed at load. Done.

Also tab4 heading order: checks panel first (open), quirks, method.

Let me also include in tab4 a line about what citations are built from: covered in method.

Now — the draft hint: "Kept in localStorage when allowed, in memory otherwise" — plan says hint on draft tab. Done via renderDraft.

Draft buttons area and list.

Now, potential issue: `renderDraft` called by renderPanel when tab 3; also by addToDraft/remove when on other tabs — guard: only if panel visible or just always (cheap). Always fine.

Also `#draft-n` update on add/remove.

Now — wiring records delegation once at init:
```js
$('#rec-list').addEventListener('click',onRecClick);
```

onRecClick:
```js
function onRecClick(e){
  const b=e.target.closest('[data-act]');
  if(b){const art=b.closest('article.row');if(!art)return;const r=byId.get(art.dataset.id);if(r)doAct(b.dataset.act,r);return;}
  if(e.target.closest('a'))return;
  if(window.getSelection&&String(window.getSelection()))return;
  const art=e.target.closest('article.row');
  if(art){const r=byId.get(art.dataset.id);if(r)toggleOpen(r.id);}
}
```

doAct implemented above.

Now — 'quote' copy: `'"'+quotationText(r)+'" '+r._citation`. quotation marks: straight ". OK.

addToDraft — also update tab label + runChecks (header draft check) — but runChecks uses DOM for rows check (panel2 may be hidden → arithmetic). Fine. Also if tab2 active, no re-render needed (row unchanged) — but maybe mark button as added? Keep simple: status message.

Now — saveDraft and storageMode.

Downloads — `download()`.

CSV column 'paragraph' numeric.

Now — write header/footer init.

Also — `qInput.setAttribute('aria-label'...)` via label element. Done with <label for>.

I think I'm ready to write. Length estimate: HTML ~150 lines, CSS ~230, JS ~700. Total ~1,100. Good.

One more check — the plan: "Under it the search: a labelled input and a 'Search' button; Enter searches." and syntax list behaviour. Done.

"While the box is empty and has focus, a short list opens under it" — focus handler: `if(!qInput.value)syn.hidden=false`. On load focus → opens. Good.

"it closes when typing starts" — input handler: syn.hidden=true (on any input). Good.

Examples "fill and run".

Also — plan: "One line under the box: 'Whole words, any case. …'" — the normline. Done.

"After a search, a line echoes the query as understood" — echo. Done.

"An unbalanced quote or parenthesis shows a message and no results." — echo.err + hits=[]. Done.

Committee checkbox "with its full name and, after a search, its hits in brackets" — brackets show always (even empty query they show totals — "after a search" per plan; showing totals always is fine and matches "all ticked" default where brackets = totals). OK.

Now — one more thought about aria: the tablist needs aria-label. Panels aria-labelledby. Done.

Also — "the count, the summary line and the 'Copied' message are aria-live='polite'". Done.

Search input focused on load. Done.

Let me also double-check highlightInto's handling when hl null (no query): returns esc(str). Good.

One more potential issue: highlight regex could match the leading number "12." if query is "12"? wordBody("12") → B0 12 B1 — "12." in "12. The Committee" — before "1" is start (boundary ok), after "2" is "." (boundary) → match. Fine, legit.

Now — write the final document.

Small detail: `.row-text` click also toggles (part of article). Also `user-select` allowed.

For the `more` button hidden default.

Also renderRecords should set `#order-desc` and select value: `$('#order-sel').value=state.order` (static element, set on change anyway; but set for safety).

Also note — plan: order select "offers document order and most matches first" plus default. 3 options.

Edge: 'matches' order with no query → fallback to year. Implement: if order==='matches' && (!state.q||state.q.err||!state.q.termsReNorm) → year sort.

Now, counts for 'matches': 
```js
if(state.order==='matches'&&state.q&&state.q.termsReNorm){
  const re=state.q.termsReNorm;const cnt=new Map();
  hits.forEach(r=>{re.lastIndex=0;const m=r._norm.match(re);cnt.set(r.id,m?m.length:0);});
  return hits.slice().sort((a,b)=>(cnt.get(b.id)||0)-(cnt.get(a.id)||0)||byYear(a,b));
}
```
Note: String.match with global regex — safe.

Alright. Also — `byYear` uses localeCompare on title — fine.

Now — write!

Actually one more: `esc` also for `_pin` etc — done inline.

And the header source link: 
```js
let srcHtml='';
if(D.source){srcHtml=D.source_url&&/^https?:/.test(D.source_url)?'<a href="'+esc(D.source_url)+'" target="_blank" rel="noopener">'+esc(D.source)+'</a>':esc(D.source);}
$('#head-line').innerHTML=fmt(R.length)+' paragraphs from '+fmt(titlesSet.size)+' General Comments of '+allCodes.size+' committees, '+YMIN+'–'+YMAX+(srcHtml?' · '+srcHtml:'');
```

Footer:
```js
$('#foot-src').textContent=(D.source||'')+(D.built?', built '+D.built:'');
```
Hmm — source appears in header too; footer per plan: "`source` and `built`". OK.

The footer static text: 'Counting, matching and sorting are done by this page’s code; no model is called. Built with Chart.js (MIT licence).'

Now — also think: does `WORKSHOP_DATA.gc` include `built`? Unknown; guard.

Writing the CSS `.head-checks.ok{color:#1e6b34}` `.fail{color:#9b2335}`.

OK also — accessibility: contrast of #9b2335 on #f4f0e8 ≈ 6+.

Let me also give `.rec-summary` id and aria-live.

Time to write the final output. I'll write carefully and completely.

Also — remember: NO network calls. Chart via window.Chart only.

One more consideration: `state.mode`/`open`/`ctx` grow — fine.

Also, `renderRecords` sets `#rec-more`:
```js
const more=$('#rec-more');
if(ordered.length>state.shown){more.hidden=false;more.textContent='Show 25 more ('+fmt(ordered.length-state.shown)+' of '+fmt(ordered.length)+' not yet listed)';}
else more.hidden=true;
```
Plan label: "Show 25 more". With remaining count. OK.

Empty list message:
```js
if(!ordered.length)listEl.innerHTML='<p class="empty">No paragraphs match. Widen the filters or clear the search.</p>';
```

Also when q err — summary explains.

Let me write buildRow's doc link:
```js
const symHtml=r.doc_url? '<a href="'+esc(r.doc_url)+'" target="_blank" rel="noopener">'+esc(r.symbol)+'</a>':'<span>'+esc(r.symbol)+'</span>';
```

Also `.meta` separators: ' · '.

Final check of the copy citation note: "A grey note names the style, 'UN short form'." — in row-actions: `<span class="stylenote mono">citation style: UN short form</span>`. Done.

Also plan: "Copy citation copies 'CCPR/C/GC/37, para. 12'; when the symbol is shared ... 'CERD, General Recommendation No. 29 (A/57/18), para. 3'." — implemented via _shared.

Hmm — docName: title up to first colon or " on ". Example title likely "General Recommendation No. 29 (2002): Article 1, paragraph 1 of the Convention" hmm that would give "General Recommendation No. 29 (2002)". The plan's example shows "General Recommendation No. 29 (A/57/18)" — no year. Maybe their actual title is "General Recommendation No. 29 on Article 1, paragraph 1, of the Convention" → " on " cut → "General Recommendation No. 29". Then citation: "CERD, General Recommendation No. 29 (A/57/18), para. 3". Matches plan example! Good, my docName handles both.

Edge: title containing " on " early, e.g. "General Comment No. 32 on Article 14..." → cut at " on " → "General Comment No. 32". Fine.

Now — also one thing: `citation` for shared uses r.committee — the code. Good.

Let me also ensure `_pin` set before `citation` — order in precompute: _pin then _shared then _citation. I'll do two passes.

Also `_lettered` set inside pinpoint — fine (called in pass 1).

Writing everything now. Also — micro: `pl` helper.

One more consideration on `normline` text — exactly per plan: "Whole words, any case. Curly and straight quotes, apostrophes, dashes and hyphens count as the same, and footnote marks are skipped, so State's finds State’s and a phrase can cross a footnote."

Include curly apostrophe in the text — fine.

Let me also add `<meta name="color-scheme" content="light">`? Optional, skip... actually add to avoid dark-mode form controls: fine, add.

Now write. I'll number nothing; just produce.

Also — one subtle thing in the tab keydown: activate on arrow — includes focus() then setTab. OK.

The tab buttons: type="button".

Also — initial tabIndex setup in HTML: tab1 tabindex 0? Default all focusable; set tabindex="-1" on others via JS init. I'll do in JS.

Potential final issue — `qInput.focus()` on load might scroll — fine.

Also — plan says hint next to search: label "SEARCH". Done.

Also — big number area: "279 matching paragraphs" then "of 7,304". Implement:
```html
<p class="bignum" id="big-num" aria-live="polite">0</p>
<p class="bigsub">matching paragraphs</p>
<p class="mono ofsub" id="of">of 0</p>
```

Chips container after.

OK writing final.

Wait — one more requirement I should double check: "Every tab reads the same filtered set." Yes — hits computed once globally.

"Filters in a narrow left rail... one big number of matching records on top, then numbered headings (01 KEYWORD, 02 YEARS)…" — the plan for THIS app overrides: search then one numbered heading "01 Committee, years, document". Follow the app plan.

Also — the app plan says search sits under the big number, then numbered heading. Yes.

Also — "Active filters show as small removable chips." Done.

Final: write the code.

Let me also handle a corner: user types query with only spaces → runSearch: raw='' → q=null. Good.

And the "Search" button click: runSearch.

Let me draft the JS section in full now (mentally compile):

Potential bug: in tokenize, the word loop condition `while(j<q.length&&(!/[\s()]/.test(q[j]))&&OPEN.indexOf(q[j])<0)` — creating regex per char is slow-ish but queries are short. fine.

In parsePrim for token 'P' with v — build node {k:'PH',v}.

collectTerms pushes nodes (k WD/PH).

buildHlRe(terms):
```js
function buildHlRe(terms){
  const alts=terms.map(t=>{
    if(t.k==='WD')return B0+wordBody(t.v,true)+B1;
    return B0+t.v.trim().split(/\s+/).map(w=>wordBody(w,true)).join('(?:\\s|\\[\\[fn:\\d+\\]\\])+')+B1;
  });
  return new RegExp('(?:'+alts.join('|')+')','giu');
}
```
Hmm — for WD hl, t.v raw (not normalised) — uppercase handled by 'i'. Curly in query handled by class. Good.

But WAIT — subtle: for WD norm-match, I used normText(t.v). For hl I use raw t.v. If t.v = "State's" — hl pattern: S t a t e [’'] s — matches "State's" and "State’s". Good.

buildNormRe similar with normText.

Now — `q.straightTerms` — build:
```js
function buildStraight(terms){
  const out=[];
  terms.forEach(t=>{
    if(!/['"\u2018\u2019\u201C\u201D-]/.test(t.v))return;
    const chars=[];for(const ch of t.v){if(ch==='"'||ch==="'"||ch==='-')chars.push(ch);}
    let body;
    if(t.k==='WD')body=B0+wordBodyStrict(t.v)+B1;
    else body=B0+t.v.trim().split(/\s+/).map(w=>wordBodyStrict(w)).join('(?:\\s|\\[\\[fn:\\d+\\]\\])+')+B1;
    out.push({normTest:termMatcher(t),strictTest:s=>new RegExp... 
```
Precompile: const re=new RegExp(body,'iu'); {normTest, strictTest:s=>re.test(s), chars:[...new Set(chars)]}.

Note — if the query uses a CURLY apostrophe, normText maps to straight in matcher; strict body from raw has curly char (escaped literal) — strict would fail on straight text... but the check only fires when straight chars present. If mixed... edge, ignore.

Now — `termMatcher(t)` uses normText(t.v) internally. t reused — fine.

One more possible gotcha: terms collected include SAME node objects as tree — compile caches _fn on them; termMatcher separately compiles — fine.

OK — also `q.echo` built via echoLine(tree).

`q.termCount`.

Alright, final write-out. I'll be disciplined about matching ids.

For the initial render, `update()` runs with tab=1 → buildChart. Good.

Let me also not forget `Chart.defaults` font — set per-chart.

Writing the response now. Pre-code: 2-3 sentences.

Also the file must start with <!doctype html>.

Count lines roughly as I write to stay under 1500.

One more small thing: the plan says the rail is headed "FILTERS" with "Clear all" — done.

And "One big serif number" — 46px Georgia.

Also plan: pinpoints red — .pin color #9b2335 — used in rows and draft.

Also — `.badge` outlined mono one colour — done.

In draft items, citation as .pin.

Also — remove button in draft: linkish "remove".

OK — also the `empty` class style.

Also — `.checks li.fail` maybe add red left border? Keep simple.

Final: write.

Ah wait — one more important thing: `renderRecords` is called by setTab(2) and update(). But `#rec-summary` aria-live updates. fine.

And when state.q.err, renderRecords: ordered=[] → "No paragraphs match." plus summary error text. Good.

Also — `hits` used in runChecks; when q err, hits=[] — checks consistent.

One more: `countsByCommittee` returns c with all CORDER keys (0 default) — bars show 0 for committees with no hits — chart with zero bars fine; table shows 0.

Edge: all-zero chart (no hits) — bars empty, axis 0..1. fine.

Now writing for real.

Also `#rec-list` container and `.more` button — ensure `more` outside list.

double-check: `renderPanel` for tab 4 — nothing; runChecks will render if tab4. In update() order: renderPanel(); runChecks(); — good.

But setTab(4) after update: renderChecksPanel called in setTab. state.checks exists (from last runChecks). If never ran? update() runs at init. Good.

Let me also ensure `state.cc` exists before buildChart in init update. Yes.

Write now. Also include `lang="en"`, `<meta charset>`.

Also careful: in HTML, the syntax examples contain quotes: `<button class="ex">"best interests" AND child</button>` — fine in HTML.

The normline contains "State's finds State’s" — fine.

In JS strings with curly quotes — file is UTF-8. OK.

Now — write the answer.

Let me write the complete code.

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="color-scheme" content="light">
<title>Verbatim finder — General Comments and General Recommendations</title>
<style>
[hidden]{display:none!important}
*{box-sizing:border-box}
body{margin:0;background:#f4f0e8;color:#1d1b18;font:16px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
a{color:#9b2335}
a:focus,button:focus,input:focus,select:focus,textarea:focus{outline:2px solid #9b2335;outline-offset:2px}
.mono{font-family:ui-monospace,Menlo,Consolas,"Courier New",monospace;font-size:12px;letter-spacing:.04em}
.lab{font-family:ui-monospace,Menlo,Consolas,"Courier New",monospace;font-size:11px;letter-spacing:.14em;text-transform:uppercase}
.serif{font-family:Georgia,"Times New Roman",serif}
...
```

I'll write it all out in the answer. Let me be careful about a few JS details as I write:

- `const listEl` reference cached.
- In `buildRow`, `state.ctx` keys `id:prev`.

For ctxMap: `const ctxMap=new Map(); byTitleArr.forEach(...)` storing {prev,next}.

Let me also store byTitle sorted arrays.

Alright — also, in the row-sub line, join cm and fullBtn with ' · '.

One more UI nicety: `.row.open` maybe left border red? Keep subtle: border-left 2px solid #9b2335, padding-left 10px when open. Nice. But changes layout width — acceptable.

Now writing final. Also remember to include `role="img"` on canvas and fallback content.

Also — the chart hint "click a bar = tick that committee alone" — below chart.

Also — the compute line: "How this is computed: one count per committee over the paragraphs that match the query and filters." plus joint note. Two lines ok.

Final answer structure: 2-3 sentences, then code block, nothing after.

Let me write the whole JS carefully now in final form (I'll compose directly in the answer).

One more check on `doAct` 'full': after setting full, the "Show the full paragraph" button disappears; focus restore to 'open-id' (toggle). Good.

'ctx-prev' toggling: rerow(r, 'ctx-prev-'+r.id) — button still exists → refocus. Good.

Also when context opened, ensure the ctxblock appears — in buildRow reading state.ctx. Good.

Edge: ctx for records where prev/next missing — buttons replaced by dim spans.

Also — `#rec-list` may be re-rendered by renderRecords on filter change — open/ctx/mode preserved.

Write it.

For `download` ensure Blob type with charset.

CSV: also wrap header.

Draft `text_as_stored`: r.text.

Also — remove draft item uses index — after splice, render. Fine.

`renderDraft` bad-item note:
```js
function draftBadNote(d){
  const r=byId.get(d.id);
  if(!r)return 'the record is no longer in the file';
  if(r.text!==d.text_as_stored)return 'the stored text of this record differs from the copy kept in this draft';
  return null;
}
```

OK. Compose now. Also — remember the fallback textarea select on show.

Also — `copyStatusEl` = $('#copystatus'); set textContent.

Also on successful copy hide fallback box.

Now, final code. (Writing with care; ~950 lines total hopefully.)

Let me also double check `tokenize` handles a query that is only `"phrase` (unbalanced): throws with message. runSearch catches → q.err. Good.

`parse(')')` → parsePrim sees ')' → 'unexpected “)”'. Actually parseOr→parseAnd→parseNot→parsePrim: t=')' → throw. Good.

`parse('a)')` → after a, parseAnd loop breaks at ')'; parseOr returns; leftover ')' → throw 'unexpected “)”'. Good.

Now — committee label in optgroup: label=c code. Good.

Also add to committee fieldset a small hint about joint: "A joint General Comment appears when either of its committees is ticked, and shows both badges." — small mono. Good.

Ready. Also — make sure I define `pl` helper used in checks.

Also — for the `Numbering` check I want pl for arrays: `const pl=a=>a.length===1?'':'s';`.

Let me also make sure the `echo` for star uses the raw with star trimmed: `any word ending “child”` — plan: "(child* finds children)". OK.

Write the answer now.

Line-count vigilance: I'll keep CSS compact.

One more consideration: `.row-toggle` inherits font — set `font:inherit` won't keep italic span; spans inside carry own styles. fine.

In row heading, short_title italic serif? Use .doc {font-style:italic}. fine.

Also `h3.row-h{font-size:15px;font-weight:600}`.

OK — go.

Also — small: `#q` and button in a flex row.

And the `Search` button style: like other buttons.

Final!