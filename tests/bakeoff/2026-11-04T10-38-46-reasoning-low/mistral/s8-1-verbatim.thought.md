Let me plan this app carefully. The user wants a "Verbatim finder" app over `WORKSHOP_DATA.gc`. Four tabs: 01 Overview, 02 Paragraphs, 03 Draft, 04 Check & method. Left rail with filters (search box, committee checkboxes, years, document select). Header with checks status. Footer.

Key implementation details:

1. Load data: `R = WORKSHOP_DATA.gc.records`. Compute per record at load: norm, marks, leading, pinpoint, citation, shared, joint, committees.

2. Normalisation function: remove `[[fn:N]]`, map curly quotes to straight, en/em dash and soft hyphen to "-", all whitespace (incl. nbsp, line breaks) to single space, lowercase.

3. Query parser: tokens — quoted phrases (straight or curly double quotes), parens, AND/OR/NOT capitals, leading `-` as NOT, words with optional trailing `*`. Adjacent = AND. Precedence NOT > AND > OR. Return tree + English echo + error.

4. Term match: word → regex over norm with boundaries `(?<![\p{L}\p{N}])` and `(?![\p{L}\p{N}])`, flag u, trailing `*` → `\w*`. Phrase: words joined by `\s+`. Hyphen is a boundary (since norm has "-" which is not \p{L}\p{N}, the lookarounds naturally treat hyphen as boundary — good, "state" finds "non-State" because "-" before "state" is not a letter/number).

Wait — but the word itself may contain a hyphen after normalisation, e.g. "non-state" → "non-state". The regex escapes the word; hyphen inside is fine. Boundaries: `(?<![\p{L}\p{N}])non\-state(?![\p{L}\p{N}])`. In "non-state", preceded by space — ok. Good.

5. Highlight: second regex over shown text (text with fn marks removed). Quote/apostrophe matches straight+curly forms; hyphen matches -, –, —; gap between phrase words matches `(?:\s|\[\[fn:\d+\]\])+` — but wait, shown text has fn marks removed already... Actually the spec says shown text = text with fn removed. But highlight regex should handle gaps matching `(?:\s|\[\[fn:\d+\]\])+` — that applies if we highlight over the stored text? Hmm. The spec: "The same terms become a second regular expression over the shown text, where ... a gap between phrase words matches `(?:\s|\[\[fn:\d+\]\])+`". Since shown text has marks removed, the gap would just be whitespace. But to be safe, build the highlight regex to allow fn marks in gaps anyway (harmless). Actually simpler: highlight over the shown (marks-removed) text, but allow the gap pattern to include fn marks just in case. I'll highlight over shown text.

For highlight, each character class: `"` → `["“”„]`, `'` → `['‘’‚]`, `-` → `[-–—]` plus soft hyphen `\u00AD`. Escape regex specials otherwise. Word boundaries for highlight: use lookarounds with `\p{L}\p{N}` too? The shown text isn't lowercased; use flag `iu`. Boundaries same.

Actually careful: highlight regex over shown text — the shown text retains curly quotes etc. The term's normalised form has straight quotes; when building the highlight pattern from the term, map each char: if it's `"` include class, etc. Also case-insensitive flag `iu`.

6. Filters: committee checkboxes (10 codes with full names), years from/to, document select grouped by committee (optgroup). Chips for active filters.

Committee full names: need a mapping. Codes: CAT, CCPR, CED, CEDAW, CERD, CESCR, CMW, CRC, CRPD, CAT-OP. Full names:
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

But I should derive codes from data, not hard-code? The spec says read field values from data, never hard-code counts/countries/years/names. Committee codes — the regex given in the plan lists them explicitly, so using that regex is fine. Full names: I can map known codes; if an unknown code appears, fall back to the code itself. That's safe.

A record's committees: codes found in symbol via regex `\b(CAT|CCPR|CED|CEDAW|CERD|CESCR|CMW|CRC|CRPD)\b` plus "CAT-OP" for `CAT/OP`, plus `committee` field. Note: "CAT" regex would also match inside "CAT-OP"? `\bCAT\b` — in "CAT-OP", after CAT comes "-", which is a non-word char, so `\b` matches. Hmm, `\b(CAT|...)\b` on "CAT/OP/CAT/10" — "CAT" followed by "/" is a boundary, so CAT matches. And CAT-OP: symbol like "CAT/OP/..." — the plan says "CAT-OP" for `CAT/OP`. So check if symbol contains "CAT/OP" → add "CAT-OP". Also plain CAT. Fine.

Joint: symbol contains two committee codes (or en dash / comma with two symbols). Compute: codes found in symbol; if more than one distinct code → joint. Actually "CMW/C/GC/7–CERD/C/GC/38" has CMW and CERD → joint. "CRC/C/GC/23, CMW/C/GC/4" → CRC and CMW. Good.

7. Pinpoint: "para. N" / "preamble" (paragraph 0) / "subpara. (b)" when text starts with `^\(([a-z]{1,4})\)`. Order: check lettered first? A record with paragraph 0 and lettered? Preambles of early CEDAW/CERD GRs have paragraph 0 — do they start with "(a)"? Possibly. Plan lists pinpoint rules; I'll check subpara first, then preamble, then para. Actually plan order: "para. " + paragraph; "preamble" when 0; "subpara. (b)" when lettered. Hmm ambiguous. I'll do: if lettered label → subpara; else if paragraph===0 → preamble; else para. N. Wait but the plan says pinpoint: "para. " + paragraph; "preamble" when paragraph is 0; "subpara. (b)" when text starts with lettered. If paragraph 0 AND lettered... unlikely. I'll prioritize lettered? Actually a lettered sub-para numbered 1,2,3 by the file has paragraph 1-3, so no conflict. Preamble para 0 probably doesn't start with "(a)". Either order fine. I'll do subpara check first.

Hmm, wait: "22 records are lettered sub-paragraphs ("(a) To take note…") that the file numbers 1, 2, 3" — so paragraph is 1,2,3 and text starts with "(a)". Pinpoint "subpara. (b)". Good.

8. Citation: symbol + ", " + pinpoint. If shared (symbol holds >1 title): `committee + ", " + docName + " (" + symbol + "), " + pinpoint` where docName = title up to first colon or " on ". E.g. "CERD, General Recommendation No. 29 (A/57/18), para. 3". Title like "General Recommendation No. 29: ..." → up to first colon. Some titles may have " on " — e.g. "General comment No. 27 (2025) on economic..." Hmm, "up to the first colon or ' on '". I'll take whichever comes first.

9. Leading number: `^(\d{1,3})\.\s` on text. If leading === paragraph → copied quotation drops the "N. " prefix. If differs → amber note, nothing dropped.

10. Copy quotation: shown text (marks removed) in quotation marks + space + citation. If leading matches, drop leading "N. " from the copied quotation. Use curly quotes? "in quotation marks" — I'll use “ ” curly since data uses curly. Fine.

11. Draft: stored in localStorage if allowed else memory. Items: {id, citation, quotation (as copied), symbol, paragraph, pinpoint, committee, short_title, year, text_copied, text_as_stored, doc_url}. Tab name "03 DRAFT (n)". Buttons: remove per item, Copy all, Download .txt, Download .csv (BOM, quoted fields).

CSV fields: citation, symbol, paragraph, pinpoint, committee, short_title, year, text_copied, text_as_stored, doc_url.

12. Checks (tab 04):
- Query understood: echo + term count; parse error shown.
- Totals: rows listed across pages equal hits; checkbox bracketed counts sum = hits + joint hits.
- Chart total: bars sum = hits + joint hits.
- Highlight: every hit has ≥1 mark unless NOT-only query; list "matched, not highlighted".
- Normalisation: if query has straight quote/apostrophe/hyphen, say curly/dash forms matched too and how many hits contain only those forms.
- Numbering: hits with leading≠paragraph (both numbers); hits sharing pinpoint with another record of same title; lettered sub-paragraphs.
- Marks: for every hit, marks removed == count of `[[fn:` in stored text, and reinserting gives stored text exactly. Reinserting: replace removed marks... hmm, "putting them back gives the stored text exactly" — since we only removed `\[\[fn:\d+\]\]`, we can verify by checking that stored text with marks removed equals shown text — trivially true. Better check: count of `[[fn:` occurrences in text equals marks, and `text.replace(/\[\[fn:\d+\]\]/g,'')` === shown. That's the check. I'll compute shown = text.replace(...), marks = (text.match(/\[\[fn:\d+\]\]/g)||[]).length, and check shown === text with marks removed (trivially true) — instead check that removing marks and re-adding count... The meaningful check: marks === count of `[[fn:` in text, and shown + marks reconstruct: `text.split(/\[\[fn:\d+\]\]/).join('')` === shown. Fine, do that.
- Draft: for each item, look up record by id, compare text_as_stored.
- Known quirks computed at load: paragraph 0 count + example; shared symbols count + example; joint count + example; duplicated pinpoints (same title+paragraph appearing >1 time) count + example; leading mismatches count + example.

Checks run after each search over hits. Header shows "n checks pass" green or "n checks failed" red, red dot on tab 04.

13. Chart FIG.01: Chart.js horizontal bars, one per committee (of hits), ranked desc, value at end of bar, axis from zero, red bars. Click bar → tick that committee alone. aria-label with numbers, fallback table beside.

Chart.js 4 preloaded. Bar chart with indexAxis 'y'. Data labels at end of bar — use a plugin or just put values in labels? Simplest: use `afterDatasetsDraw` plugin to draw values at end of bars, or set the category labels to include value? The plan says "the value at the end of each bar". I'll write a small inline plugin drawing the number at bar end. Also gridlines: at most ten light gridlines — set maxTicksLimit 10 on x axis. Gaps narrower than bar: barPercentage ~0.9? "gaps narrower than a bar" means categoryPercentage/barPercentage such that gap < bar width: barPercentage 0.8, categoryPercentage 0.9 gives gap = 0.1*... hmm. bar thickness = categoryPercentage * barPercentage * slot. Gap = categoryPercentage*(1-barPercentage)*slot. For gap < bar: (1-bp) < bp → bp > 0.5. Use barPercentage 0.85, categoryPercentage 0.9.

Click handler: chart.getElementsAtEventForMode → tick only that committee.

14. Search box behaviour: focus on load; while empty and focused, show syntax help list with 3 examples as options (buttons) that fill and run; closes when typing starts. Enter searches. Echo line after search. Error message for unbalanced quote/paren.

15. Pagination: 25 per page, "Show 25 more" button.

16. Row rendering: article per row, heading with badges etc. Click row toggles open panel with buttons: Copy citation, Copy quotation, Add to draft, Context prev|next. Context opens paragraph ±1 of same title inline in grey.

Long paragraphs: >700 chars shown first 700 cut at word + "Show the full paragraph (N words)". white-space: pre-wrap.

Marks removed line: "3 footnote marks removed · show as stored" link toggles to stored text.

Amber notes: leading mismatch ("the text begins '45.' but the record is para. 41: check the document"), lettered subpara, shared pinpoint (two records share this pinpoint), joint GC.

17. Order select: "year, newest first" default; options: document order, most matches first. "Most matches first" — matches per what? Probably per document (title) count of hits, descending. I'll implement: sort by hits-per-title desc, then year desc, title, paragraph. Document order: by title then paragraph ascending? "document order" — group by document: sort by title (alphabetical? or by year of doc?) then paragraph. I'll do title asc, paragraph asc. Default: year desc, title, paragraph asc.

18. Left rail hidden on Draft tab. Header always visible. Tabs: role="tablist", arrow-key navigation.

19. Clickable count ≤ ~7 per view: tabs(4) + search + filter heading(s). Filter rail has one numbered heading "01 Committee, years, document" containing committee checkboxes, years, document select. Wait — the plan says "Then one numbered heading, closed until clicked: 01 Committee, years, document. Committee: ... Years: ... Document: ...". So one collapsible section containing all three filter groups. Clickable on overview: 4 tabs + search box + 1 filter heading = 6. Good.

Chips: active filters show as removable chips under big number.

20. Design: paper #f4f0e8, ink #1d1b18, rules #d9d2c3, accent #9b2335. Serif Georgia for title/big numbers/figure titles; monospace labels 11-12px uppercase letter-spaced; sans 16px body. mark: pale yellow bg (#f6e9a8?) bold dark text. Amber notes (#8a5a00 on pale?). Green pass (#1e6b3a). Focus ring red.

21. Footer: source and built, "Counting, matching and sorting are done by this page's code; no model is called." Credits line: Chart.js MIT.

22. No external loads. All inline.

23. `hidden` attribute rule: add `[hidden]{display:none!important}`.

24. Copy fallback: if navigator.clipboard.writeText refused (or unavailable), show selectable box with "Select and copy". aria-live message with exact string sent.

25. studio.ask never called. Good.

Now sizes: 7,304 records — performance matters. Precompute norm per record at load (7304 regex replaces — fine). Search: build regex per term, test each record's norm — 7304 tests per term, fine.

Highlight: only for shown rows (25 per page + expanded), fine.

Checks: highlight check over all hits — building highlight regex and testing each hit's shown text; hits could be thousands (empty query = 7304). Testing 7304 regexes is OK-ish. But "every hit shows at least one mark" — we only render 25; the check should test all hits. 7304 regex tests fine.

Marks check over all hits: string ops on up to 7304 records — each text up to ~1287 words. Could be a few MB total; fine.

Let me now think about the query parser in detail.

Tokenizer:
- Skip whitespace.
- `"` or `“` or `”` or `„` starts a phrase until matching closing quote (straight `"` or curly `”`). If none → error "unbalanced quote".
- `(` `)` tokens.
- Word: run of non-space, non-paren, non-quote chars. If word is `AND`/`OR`/`NOT` (exact capitals) → operator. If starts with `-` and length>1 → NOT + rest as word (rest may have trailing `*`? "-child*" → NOT child*). If word is exactly `-` → treat as word? Edge; treat as NOT with empty → error? I'll treat lone `-` as a word "-". Simpler: if starts with "-" and rest non-empty → NOT term(rest).
- Trailing `*` on word allowed.

Parser (recursive descent):
- parseOr: parseAnd (OR parseAnd)*
- parseAnd: parseNot (AND? parseNot)* — adjacent terms (no operator) also AND.
- parseNot: NOT parseNot | parsePrimary
- parsePrimary: `(` parseOr `)` | term

Echo generation: build English string from tree. E.g. term → `the word child` or `the phrase "best interests"` or `child* (any ending)`. AND → "… and …", OR → "… or …", NOT → "without …". For NOT-only query echo says "matches everything that lacks …". I'll produce echo like: `Paragraphs containing the phrase “best interests” and the word child` — per plan example. For OR: "containing X or Y". NOT: "not containing X". Let me build echo recursively returning a noun-phrase string, and the top line: "Paragraphs containing " + echo + "." If root is NOT-only (tree is Not(term) with single term), say "Paragraphs not containing the word X (a NOT-only query matches everything else)". Plan: "a NOT-only query matches everything that lacks the terms, and the echo says so."

Term regex over norm: escape word, trailing `*` → append `\w*`. Pattern: `(?<![\p{L}\p{N}])` + escaped + `(?![\p{L}\p{N}])`, flags `u`. For phrase: words (split on whitespace after normalising query) joined by `\s+`, wrapped in same boundaries. Note: phrase words themselves may contain `*`? Keep simple: phrases don't support `*` inside (or apply per word). I'll apply: each word in phrase, if ends with `*`, use `\w*` for that word. Fine.

Query normalisation: same normaliser applied to the raw query string before tokenizing? Careful: normalising collapses whitespace and lowercases — but we need to detect capital AND/OR/NOT before lowercasing. So tokenize the raw query first (detect operators on raw tokens), then normalise each term's text. Quotes: detect curly quotes in raw. Good approach: tokenize raw; for each term token, normalise its content (quotes→straight etc., lowercase) then build regex.

Highlight regex from terms: for each term (word or phrase), build pattern over shown text:
- For each char in normalised term: if `"` → `["“”„]`, `'` → `['‘’‚]`, `-` → `[-\u2010-\u2015\u00AD]` (hyphens/dashes), else escape.
- Word: boundaries `(?<![\p{L}\p{N}])` ... `(?![\p{L}\p{N}])`, flags `giu`. Trailing `*` → `\w*`.
- Phrase: words joined by `(?:\s|\[\[fn:\d+\]\])+`. Hmm but shown text has fn removed; still allow. Also whitespace in shown text includes nbsp and line breaks — `\s` with `u` flag matches nbsp? `\s` in JS matches \u00A0 yes (it's whitespace). Line breaks yes. Good.
- Combine all positive terms (not NOT terms) into one alternation regex with `g` flag for highlighting.

Highlight application: escape HTML of shown text first, then wrap matches in `<mark>`. But careful: escaping changes characters? HTML-escaping only changes & < > — quotes stay as-is (we don't escape quotes in text content). So run regex on the escaped string? The regex includes quote classes which would match `&quot;`? We don't escape quotes, so fine. But `&amp;` etc. — the term chars are letters mostly; `&` in term would be escaped to `&amp;` in HTML and regex `&` wouldn't match. Edge case, ignore (terms with & are rare). Actually safer: run the highlight regex on the raw shown text, collect match ranges, then build HTML by escaping segments and wrapping matched segments. I'll do that: iterate matches with exec, build parts.

Wait, but the gap pattern `(?:\s|\[\[fn:\d+\]\])+` — shown text has fn removed so gaps are just whitespace. OK.

Also note: shown text may contain `[[fn:N]]` when "show as stored" is toggled — then highlight should still work; the gap pattern handles it. But when showing stored text, do we highlight? The toggle swaps text; I'll re-render highlight on whichever text is shown. Simpler: highlight function takes text; for stored text the fn marks are present and gap pattern covers them. But individual word matches inside... fine.

Hmm, actually simpler: always highlight over the shown text (marks removed). When user toggles "show as stored", re-render with stored text and same highlight regex (gap pattern includes fn marks). Good.

Now the "matched, not highlighted" check: for each hit, test highlight regex (without g, or with) against shown text; if no match and query has positive terms → list. This can happen e.g. when norm matched via normalisation (curly quote in query matched straight in text? no—both normalised). Actually norm and shown differ only by fn removal and case; regexes are equivalent modulo quote/dash classes which are supersets. Should mostly match. Fine.

Committee filter: checkbox per committee code present in data (from records' `committee` field — but joint records have one `committee` field; the filter uses record's committees set). Build list of all codes appearing in any record's committees set, sorted. Display with full name. After a search, show hits in brackets.

Hits per committee for chart: for each hit, for each code in its committees set, increment. Joint counts under both.

Filter logic: record passes if (committees ∩ ticked) non-empty AND year within [from,to] AND (docSelect empty or record.title === selected title). Document select options: short_title grouped by committee optgroup — but a record's title may map to multiple committees (joint). Group by record.committee for the optgroup label. Value = title (titles distinct per doc? 188 distinct titles; use title as value). Hmm, two different symbols could share a title? Possibly; use title as value, fine.

Wait — document select "a select of short_title grouped by committee". Options labelled short_title, value = title. OK.

Chips: if committee filter ≠ all ticked → chip "Committees: n of k" removable (untick → back to all? removing chip resets committees to all). Year chip if ≠ min/max. Document chip if selected. Each chip has × to remove.

Search flow: on search, compute hits = records where tree matches AND filters pass. Update: big number, summary, chart, checkbox counts, results (reset page to 25), checks, header status, echo line.

Empty query: tree = null → matches all (subject to filters); summary says "no search words".

Now checks details:

Header: "n checks pass" — count of passing checks among the check list; if any fail → red "n checks failed" and red dot on tab 04. Checks list (tab 04), each line: name, detail, pass/fail. Checks:

1. Query understood — echo + term count, or parse error. Pass if no error (or if error, it's shown as failed? Plan: "a parse error appears here too" — I'd mark it as "check failed"? Hmm, a parse error isn't a data check failure... I'll show it as a line with "check failed" in red since results are empty. Actually if parse error, no search runs; show error in box and in checks as failed line. Fine.)
2. Totals — rows listed across pages (i.e., hits count) equals hits; checkbox counts sum = hits + jointHits. Pass if equal.
3. Chart total — bars sum = hits + jointHits.
4. Highlight — every hit has ≥1 mark unless NOT-only; list matched-not-highlighted (count + up to few examples). Pass if none.
5. Normalisation — if query contains straight quote/apostrophe/hyphen: report how many hits contain only curly/dash forms (i.e., hits whose raw text contains the curly form but not the straight). Pass (informational) — it's a "pass" line stating forms matched. I'll make it pass with detail.
6. Numbering — list hits with leading≠paragraph (both numbers), shared pinpoints, lettered subparas — these are warnings, not failures? Plan says checks are pass/fail; numbering issues are data quirks — I'd mark "check failed" only if... hmm. Actually these are informational: the check "numbering" passes if every hit's pinpoint is unambiguous? The plan: "Numbering. Hits whose leading number differs from paragraph, with both numbers; hits that share a pinpoint...; hits that are lettered sub-paragraphs." It doesn't say fail. I'll show them as a line with count and examples, marked "pass" if zero, else "check failed" with pinpoints concerned? But plan says "A failed check marks rows; it never drops them" — rows already carry amber notes. Hmm, but making numbering quirks "fail" would make header red often. The header shows "n checks pass" or "n checks failed" — with quirks present, numbering check would fail on many searches. I think that's intended: the app honestly reports. But then almost always red... Only when hits include quirky records. Hmm.

Let me reconsider: maybe numbering check passes when the app correctly flagged them (i.e., every hit with leading mismatch has the amber note). That's a self-check: "every hit whose leading number differs from paragraph is flagged on its row". That passes always if code correct. I'll implement: check that all such hits are flagged (they are, by construction) → pass, but list them with both numbers as detail. Similarly marks check: verify marks count equals `[[fn:` count and reconstruction — pass. Draft check: compare stored — pass unless mismatch.

So checks are genuine self-verifications; failures indicate bugs/edge cases. Good — header usually green.

7. Marks — for every hit: marks === count of `[[fn:` in text; and text with marks removed === shown. Pass/fail.
8. Draft — each item's text_as_stored equals looked-up record's text. Pass/fail.

Known quirks (computed at load, shown before any search): counts + example each: paragraph 0; shared symbols (symbol with >1 title); joint (symbol with ≥2 committee codes); duplicated pinpoints (same title+paragraph >1 record); leading mismatches (leading && leading≠paragraph). Each with count and an example citation.

Now the header line: "`records.length` paragraphs from n General Comments (distinct title) of k committees, year min–max", source linked to source_url. Top-level gc has `title`, `source`, `count` (string "7304"), `records`. Does it have `source_url`? The uhri has source_url; gc described as `{title, source, count, records}`. Hmm — plan says "`source` linked to `source_url`". Maybe gc has source_url too; I'll use `WORKSHOP_DATA.gc.source_url` if present else link to source text without href... I'll do: if source_url exists, link; else plain text. Footer: source and built — gc may have `built`? Not listed. I'll show `source` and `built` if present, else just source. Use defensive access.

Now layout structure:

```
<header> label, h1, dataline, checks status right
<nav tabs> 01 OVERVIEW · 02 PARAGRAPHS · 03 DRAFT (n) · 04 CHECK & METHOD
<div class="layout">
  <aside rail> FILTERS ... (hidden on draft tab)
  <main> tab panels
</div>
<footer>
```

Tabs with role="tablist", buttons role="tab" aria-selected, panels role="tabpanel". Arrow keys move between tabs.

Left rail: 
- "FILTERS" heading + "Clear all" button
- big number (aria-live) "279" + "matching paragraphs of 7,304"
- chips container
- search: label "SEARCH THE PARAGRAPHS", input, Search button; help list (when empty+focused); echo line; error line; note line about whole words/normalisation.
- filter section: button "01 COMMITTEE, YEARS, DOCUMENT" aria-expanded; content: committee checkboxes with all/none; years from/to; document select.

Wait — clickable count: tabs 4 + search box + filter heading = 6 on overview. The Search button — is it clickable counted? Plan says "Clickable: 4 tabs, search box, 1 filter heading = 6". OK they don't count the button. Fine.

Tab 02 clickable: 4 tabs + search + 1 heading + order select + show more = 8. Plan says 8. OK.

Tab 03: rail hidden; 4 tabs + 3 buttons = 7.

Tab 04: 6 (4 tabs + search + heading).

Now, rendering results: 25 per page with "Show 25 more". Each row:

```
<article class="row" data-id>
  <button class="rowhead"> (or clickable article) 
    <div class="meta"> [badge CRC] short_title · <a symbol> · <span class="pinpoint">para. 18</span> · 2011 </div>
    <p class="text">highlighted text (truncated if long)</p>
    <div class="marksline">3 footnote marks removed · <button>show as stored</button></div>
    <div class="note amber">…</div>
  </button>
  <div class="detail" hidden>
    buttons: Copy citation | Copy quotation | Add to draft | Context: previous | next
    context area
  </div>
</article>
```

Rows as `<article>` with a heading — plan says "rows are `<article>`s with a heading". I'll make the row header a `<button>` containing an `<h3>`-ish? Heading inside button is invalid-ish; instead article > h3 > button. I'll do `<article><h3><button class="rowhead">…meta…</button></h3><div class="body">text…</div><div class="detail">…</div></article>`. Clicking anywhere on article header toggles. Simpler: whole article clickable via button wrapping meta+text? Text contains links (symbol) — nested interactive elements problem. I'll make the rowhead button contain meta line only, and clicking the text area also toggles (add click handler on article, ignoring clicks on links/buttons). Keep it simple: a button.rowhead with meta; clicking article body toggles too via handler that checks event target closest('a,button') is null.

Detail panel: three buttons + context links. Context: "previous | next" — clicking loads paragraph-1 / paragraph+1 of same title inline in grey with its own pinpoint. Implement: find records with same title and paragraph === p-1 / p+1 (or for subpara/preamble, just ±1 on paragraph). Show as grey block with pinpoint + text (highlighted? no, grey, maybe with marks removed). Include its own citation? "with its own pinpoint". I'll show pinpoint + text.

Copy citation: builds citation string. Copy quotation: `“` + copiedText + `” ` + citation, where copiedText = shown text (marks removed) with leading "N. " dropped if leading===paragraph. Wait — "the copied quotation drops the '12. ' at the start" — drop from shown text. Also for long paragraphs, copy whole text (not truncated). Yes: "copy and draft take the whole text".

Add to draft: pushes item, updates tab label, re-render draft tab, persist.

Draft tab: list items: quotation as copied (in quotes), citation, remove button. Copy all: items joined: quotation + "\n" + citation + "\n\n". Download .txt same content. Download .csv with BOM: header row + rows, all fields double-quoted, escape internal quotes by doubling. UTF-8 BOM: use `\uFEFF` prefix. Download via Blob + URL.createObjectURL + a.click(). Blob is fine offline.

localStorage: try/catch; key "verbatim-draft-gc". On load, restore. Hint: "kept in localStorage when allowed, in memory otherwise".

Order select options: "Year, newest first" (default), "Document order", "Most matches first". 

Summary line: "279 of 7,304 paragraphs match · 8 committees · 1990–2023" (committees among hits, year range among hits) + "no search words" when empty query. Plus order text: "sorted by year, newest first, then by document and paragraph".

Chart: FIG.01 "Paragraphs per committee". Only committees with >0 hits? "one bar per committee, ranked by value" — over hits. If no hits, show "no matches". Bar click → tick that committee alone (set all others unticked, that one ticked, re-run). aria-label: "Bar chart. CRC: 2091 paragraphs, CEDAW: ...". Fallback table beside with same numbers.

Chart.js config: type 'bar', indexAxis 'y', data labels via plugin afterDatasetsDraw drawing value at end. Colors: bars #9b2335. Grid: x axis grid light #d9d2c3, maxTicksLimit 10; y axis grid display false. Tooltips maybe. onClick handler.

Also "axis from zero": beginAtZero true.

Now the search help list: when input empty and focused → show `<div class="syntax">` with lines:
- `a space or AND joins words · OR · NOT or a leading minus`
- `"an exact phrase" in double quotes`
- `( ) parentheses`
- `a star at the end of a word for any ending (child* finds children)`
- `operators in capitals; lower-case "or" is a word`
- three example buttons: `"best interests" AND child`, `(torture OR ill-treatment) NOT detention`, `"reasonable accommodation"`.
Closes when typing starts (input event with value → hide). Also hide on blur? "While the box is empty and has focus" — show on focus if empty, hide on input if non-empty, show again if cleared and focused. Implement with focus/blur/input handlers.

Echo line after search: e.g. `Paragraphs containing the phrase “best interests” and the word child`. Build from tree.

Echo builder: 
- term word: `the word ${display}` (display original-ish; use normalised? show as typed). For wildcard: `the word ${w}* (any ending)`.
- phrase: `the phrase “${phrase}”`.
- AND: `${a} and ${b}`; OR: `${a} or ${b}`; NOT: `not ${a}` → phrase "without X"? Top line: "Paragraphs containing X and Y". For NOT: "Paragraphs containing X and not Y" reads odd; use "… and without Y". I'll make NOT echo = `without ${inner}`. OR at top: "Paragraphs containing X or Y". NOT-only root: "Paragraphs without X — a NOT-only query matches everything that lacks these terms". Good enough.

Term count for check: count leaf terms.

Now normalisation function:

```js
function norm(s){
  return s
    .replace(/\[\[fn:\d+\]\]/g, '')   // for norm, remove marks
    .replace(/[“”„]/g, '"')
    .replace(/[‘’‚]/g, "'")
    .replace(/[–—­]/g, '-')   // en dash, em dash, soft hyphen
    .replace(/\s+/g, ' ')      // includes nbsp? \s matches \u00A0 in JS? Yes, \s includes \u00A0.
    .toLowerCase()
    .trim();
}
```

Wait: `\s` in JS regex matches [\f\n\r\t\v\u0020\u00a0\u1680\u2000-\u200a\u2028\u2029\u202f\u205f\u3000\ufeff]. Yes includes nbsp and line breaks. Good. But order: remove fn marks first (they contain no whitespace anyway). Also trim.

Hmm — but for norm we remove fn marks; for shown text we also remove them. Same replace.

Note: the plan says norm = text with `[[fn:N]]` removed, then char maps, whitespace collapse, lowercase. Good.

Query normalisation for terms: apply same char maps + lowercase but NOT whitespace collapse per term? For a phrase, we split into words on whitespace and join with `\s+` in regex, so collapse is fine. For single word, no spaces anyway. I'll normalise term content with the same function (minus fn removal, harmless).

Term regex builder:

```js
function termRegex(term){ // term = {type:'word'|'phrase', text, wildcard}
  const words = term.text.split(/\s+/).filter(Boolean).map(w=>{
    const esc = w.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    return w.endsWith('*') ? esc.slice(0,-2) + '\\w*' : esc;  // careful: escaped '*' is '\*'
  });
  ...
}
```

Careful: escaping turns `*` into `\*`. Better: check trailing `*` on raw word before escaping: `const wc = w.endsWith('*'); const core = wc ? w.slice(0,-1) : w; const esc = escape(core); return wc ? esc + '\\w*' : esc;`

Pattern: `(?<![\p{L}\p{N}])(?:${words.join('\\s+')})(?![\p{L}\p{N}])` with flags 'u'. For single word same. Note: lookbehind support — modern browsers fine.

Hmm, one subtlety: `(?<![\p{L}\p{N}])` before a pattern starting with a quote char: e.g. phrase `"best interests"` normalised to `"best interests"` — the leading `"` in the term. In norm text, quotes are straight `"`. Boundary before `"` — preceding char is space, not letter → ok. But if text has `“best` normalised to `"best` — fine.

But wait: should the boundary apply around quotes? If query phrase is `"best interests"` including quotes, the regex includes literal `"` chars, boundaries around them. In norm, `"` is not \p{L} so boundary conditions: before `"` must not be letter — in text `say"best` (no space) it wouldn't match; fine.

Actually, should I strip quotes from phrase terms? The user types `"best interests"` — the quotes delimit the phrase; the phrase content is `best interests`. Yes! Tokenizer: on encountering a quote char, read until closing quote; the term text is the content between quotes (quotes are delimiters, not part of term). But a user might want to search for a literal quote char... edge case; plan says phrase in double quotes = exact phrase. So strip delimiters. But then a phrase like `"best interests"` searches for `best interests` — good. However the plan's normalisation note: "curly quotes pasted from Word still make a phrase" — tokenizer treats “ ” as delimiters too. Good.

Hmm wait, but then how would one search text containing quotes? Not needed.

Highlight regex: same terms but char classes for quote/apostrophe/hyphen in case the shown text has curly forms — but shown text retains curly quotes! E.g. text: `the Committee said “best interests”` — shown text has curly quotes; norm has straight. Query phrase `best interests` (no quotes) → highlight regex `best\s+interests` matches regardless. But if query includes a quote char inside... since we strip delimiters, terms rarely contain quotes. But a word like `State's` → normalised `state's` → highlight pattern: `state` + `['‘’‚]` + `s`. Good, that's why the classes matter. And hyphen: `non-state` → `non` + `[-\u2010-\u2015\u00AD]` + `state`. Good.

Highlight pattern builder:

```js
function hiPattern(term){
  const words = term.text.split(/\s+/).filter(Boolean).map(w=>{
    let pat = '';
    for(const ch of w){
      if(ch==='"') pat += '["“”„]';
      else if(ch==="'") pat += "['‘’‚]";
      else if(ch==='-') pat += '[-\\u2010-\\u2015\\u00AD]';
      else pat += ch.replace(/[.*+?^${}()|[\]\\]/g,'\\$&');
    }
    const wc = w.endsWith('*');
    if(wc) pat = pat.slice(0, ?) ...
  });
}
```

Wildcard with classes: if word ends with `*`, the last char before `*`... e.g. `child*` → pattern `child\w*`. If word is `state-*`? weird; handle: strip trailing `*`, build pattern for rest, append `\w*`. But if rest ends with a class like quote... rare. Implementation: `const wc = w.endsWith('*'); const core = wc? w.slice(0,-1): w; let pat = charsToPattern(core); if(wc) pat += '\\w*';`

Then word pattern: `(?<![\p{L}\p{N}])(?:${pat})(?![\p{L}\p{N}])`. Phrase: words joined by `(?:\\s|\\[\\[fn:\\d+\\]\\])+`. Combined highlight regex: `(?:${wordPats.join('|')})` flags `giu`. For checking "has mark": use non-global test with `iu`.

Hmm, one issue: lookbehind `(?<![\p{L}\p{N}])` in highlight over shown text — shown text has original case; flag `iu` handles case. Good.

Now the Boolean tree evaluation: 

```js
function evalTree(node, norm){
  switch(node.t){
    case 'term': return node.re.test(norm);
    case 'not': return !evalTree(node.a, norm);
    case 'and': return evalTree(node.a,norm) && evalTree(node.b,norm);
    case 'or': return evalTree(node.a,norm) || evalTree(node.b,norm);
  }
}
```

Precompile `re` per term (non-global, 'u' flag).

Parser implementation:

```js
function tokenize(q){
  const toks=[]; let i=0;
  while(i<q.length){
    const c=q[i];
    if(/\s/.test(c)){i++;continue;}
    if(c==='('||c===')'){toks.push({k:c});i++;continue;}
    if(c==='"'||c==='“'||c==='”'||c==='„'){
      const close = (c==='„') ? '“' : '"'; // „ pairs with “
      // find closing: straight " or ” 
      let j=i+1, buf='';
      while(j<q.length){
        if(q[j]==='"'||q[j]==='”'){break;}
        buf+=q[j]; j++;
      }
      if(j>=q.length) return {error:'unbalanced quote'};
      toks.push({k:'term', text:buf, phrase:true}); i=j+1; continue;
    }
    // word
    let j=i;
    while(j<q.length && !/[\s()"“”„]/.test(q[j])) j++;
    const w=q.slice(i,j);
    if(w==='AND') toks.push({k:'AND'});
    else if(w==='OR') toks.push({k:'OR'});
    else if(w==='NOT') toks.push({k:'NOT'});
    else if(w.startsWith('-') && w.length>1) toks.push({k:'NOT'},{k:'term',text:w.slice(1)});
    else toks.push({k:'term', text:w});
    i=j;
  }
  return {toks};
}
```

Hmm „ pairs with “ in German style; simpler: treat any of `"“”„` as opening, closing is `"` or `”`. Fine.

Parser:

```js
function parse(toks){
  let p=0;
  function peek(){return toks[p];}
  function parseOr(){
    let left=parseAnd();
    while(peek()&&peek().k==='OR'){p++; const right=parseAnd(); left={t:'or',a:left,b:right};}
    return left;
  }
  function parseAnd(){
    let left=parseNot();
    while(peek() && (peek().k==='AND' || peek().k==='term' || peek().k==='NOT' || peek().k==='(')){
      if(peek().k==='AND') p++;
      const right=parseNot();
      left={t:'and',a:left,b:right};
    }
    return left;
  }
  function parseNot(){
    if(peek()&&peek().k==='NOT'){p++; return {t:'not',a:parseNot()};}
    return parsePrim();
  }
  function parsePrim(){
    const tk=peek();
    if(!tk) throw 'unexpected end of query';
    if(tk.k==='('){p++; const e=parseOr(); if(!peek()||peek().k!==')') throw 'unbalanced parenthesis'; p++; return e;}
    if(tk.k==='term'){p++; return makeTerm(tk);}
    throw 'unexpected '+tk.k;
  }
  const tree=parseOr();
  if(p<toks.length) throw 'unexpected '+toks[p].k;
  return tree;
}
```

makeTerm: normalise text; if empty → error. wildcard = endsWith('*') after normalisation? Normalising lowercases; `*` unaffected. Keep phrase flag.

Edge: term text after normalisation could be empty (e.g. `"-"` alone → word "-"? starts with '-' length 1 → falls to else, term text "-" → normalised "-" → regex boundary + `-`... matches hyphens. Whatever.)

Empty query → tree null.

Echo builder:

```js
function echo(node){
  if(!node) return '';
  switch(node.t){
    case 'term': return node.phrase ? `the phrase “${node.raw}”` : (node.wild? `the word ${node.raw}* (any ending)` : `the word ${node.raw}`);
    case 'not': return `without ${echo(node.a)}`;
    case 'and': return `${echo(node.a)} and ${echo(node.b)}`;
    case 'or': return `${echo(node.a)} or ${echo(node.b)}`;
  }
}
```

Top: `Paragraphs containing ${echo(tree)}` — for NOT-only root (t==='not' at root with single term): `Paragraphs without X — a NOT-only query matches everything that lacks these terms`. I'll detect root.t==='not' → special line. raw = original term text (as typed, trimmed).

Term count: count leaves.

Now per-record precompute at load:

```js
const R = WORKSHOP_DATA.gc.records;
const recs = R.map(r=>{
  const shown = r.text.replace(/\[\[fn:\d+\]\]/g,'');
  const marks = (r.text.match(/\[\[fn:\d+\]\]/g)||[]).length;
  const norm = normText(r.text);
  const leadM = r.text.match(/^(\d{1,3})\.\s/);
  const leading = leadM ? +leadM[1] : null;
  const subM = r.text.match(/^\(([a-z]{1,4})\)/);
  const pinpoint = subM ? 'subpara. ('+subM[1]+')' : (r.paragraph===0 ? 'preamble' : 'para. '+r.paragraph);
  const codes = new Set();
  const symCodes = r.symbol.match(/\b(CAT|CCPR|CED|CEDAW|CERD|CESCR|CMW|CRC|CRPD)\b/g)||[];
  symCodes.forEach(c=>codes.add(c));
  if(/CAT\/OP/.test(r.symbol)) codes.add('CAT-OP');
  codes.add(r.committee);
  const committees=[...codes];
  const joint = symCodes.length>1; // two codes in symbol
  ...
});
```

Hmm joint: "CMW/C/GC/7–CERD/C/GC/38" — symCodes = [CMW, CERD] → joint. "CRC/C/GC/23, CMW/C/GC/4" → [CRC, CMW] → joint. But careful: `\bCAT\b` in "CAT/OP/..." matches CAT too, plus CAT-OP added. A CAT-OP record would have committees {CAT, CAT-OP}? Hmm — "CAT-OP" for `CAT/OP`: the symbol "CAT/OP/CAT/10" contains "CAT" twice → codes {CAT} plus CAT-OP → {CAT, CAT-OP}. Is that right? The plan: "the codes found in symbol ... plus 'CAT-OP' for CAT/OP plus committee". So yes, a CAT/OP symbol yields both CAT and CAT-OP. That means filtering CAT includes SPT records. That's per spec. OK.

But wait — does `\b(CAT|...)\b` match "CAT" inside "CAT-OP" written literally in symbol? Symbols use "CAT/OP/..." format presumably. Fine.

shared: precompute map symbol→set of titles; shared = titles.size>1.

citation: 
```js
function docName(title){ 
  const i = title.search(/[:]|\son\s/);  // first colon or " on "
  return i>0 ? title.slice(0,i).trim() : title;
}
```
Hmm "up to the first colon or ' on '". Use regex `/^(.*?)(?::|\son\b)/` — take group 1. If no match, whole title. E.g. "General Recommendation No. 29: ..." → "General Recommendation No. 29". "General comment No. 27 (2025) on economic..." → "General comment No. 27 (2025)". Good.

citation = shared ? `${r.committee}, ${docName(r.title)} (${r.symbol}), ${pinpoint}` : `${r.symbol}, ${pinpoint}`.

copiedText (for quotation): shown text; if leading!==null && leading===r.paragraph → strip leading `^\d{1,3}\.\s`. 

quotation = `“${copied}” ${citation}`.

Now filters state:

```js
state = { tree:null, error:null, query:'', ticked:Set(allCodes), yFrom:minYear, yTo:maxYear, doc:'', order:'year', page:25, draft:[] }
```

hits computed on run(): filter recs by tree + filters.

Committee checkbox list: all codes sorted (maybe custom order: put in a sensible order — alphabetical fine, or by count desc). I'll sort by total record count desc. Each label: checkbox + code + full name + `<span class="hits">[n]</span>` after search.

Full names map:

```js
const FULL = {
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
Fallback: code itself.

Years inputs: number inputs preset min/max. On change → re-run.

Document select: optgroups by committee (r.committee), options value=title label=short_title. Sorted by committee then short_title. Note: 188 titles — fine.

Chips: container under big number; render chips for: committees narrowed ("committees: 3 of 10 ×"), years ("years: 1990–2023 ×"), doc ("document: short_title ×"). Click × removes that filter (reset to default) and re-runs.

Clear all: resets everything (query too? "Clear all" under FILTERS — I'll clear filters and query, re-run).

Now rendering functions. Because 7304 records, avoid re-rendering everything unnecessarily; results render only `page` rows.

Row HTML build with DOM creation or template strings? Template strings with escaping — need escapeHtml for text. I'll build with string concat + escapeHtml, and highlight via range-based wrapping.

highlightHTML(text, terms): 
```js
function highlightHTML(text, hiRe){
  if(!hiRe) return escapeHtml(text);
  hiRe.lastIndex=0;
  let out='', last=0, m;
  while((m=hiRe.exec(text))){
    if(m[0].length===0){hiRe.lastIndex++; continue;}
    out += escapeHtml(text.slice(last,m.index)) + '<mark>'+escapeHtml(m[0])+'</mark>';
    last = m.index+m[0].length;
  }
  out += escapeHtml(text.slice(last));
  return out;
}
```

hiRe built from positive terms (not under NOT). Collect terms via tree walk skipping 'not' subtrees? "NOT terms are never highlighted" — terms under a NOT should not highlight. Walk tree: collect terms where path doesn't go through 'not'. Implement collectTerms(node, neg=false).

Truncation: if shown.length>700: cut = shown.slice(0,700); cut at last space → cut = cut.slice(0, cut.lastIndexOf(' ')); display + ' …' + button "Show the full paragraph (N words)". Word count = shown.split(/\s+/).length.

Row detail: when open, show buttons. Context: prev/next links — find in same title: records with same title and paragraph === r.paragraph-1 (or +1). For subpara/preamble just use paragraph number arithmetic; if not found, disable. Context area shows grey block: pinpoint + text (marks removed, escaped, maybe truncated at 700 too? keep full but pre-wrap; fine, show full).

Copy functions:

```js
async function copyText(t, msg){
  try{ await navigator.clipboard.writeText(t); live(msg); }
  catch(e){ show fallback box with text, "Select and copy"; live(...); }
}
```

Fallback: a fixed div near top of results or a modal-ish inline box: `<div id="copyfallback" hidden><textarea readonly>…</textarea><p>Select and copy</p></div>`. Show it with the text; user selects. aria-live message: `Copied: “CCPR/C/GC/37, para. 12”` — exact string sent.

Draft persistence:

```js
let storeOK=true;
try{ localStorage.setItem('__t','1'); localStorage.removeItem('__t'); }catch(e){ storeOK=false; }
function saveDraft(){ if(storeOK){ try{localStorage.setItem('verbatim-gc-draft', JSON.stringify(state.draft));}catch(e){storeOK=false;} } }
```

Load on start.

Draft item: {id, citation, quotation, symbol, paragraph, pinpoint, committee, short_title, year, text_copied, text_as_stored, doc_url}. text_copied = copiedText (marks removed, leading dropped if applicable); text_as_stored = r.text.

CSV: 
```js
function csvCell(s){ return '"'+String(s).replace(/"/g,'""')+'"'; }
const header = ['citation','symbol','paragraph','pinpoint','committee','short_title','year','text_copied','text_as_stored','doc_url'];
rows...
const blob = new Blob(['\uFEFF'+lines.join('\r\n')], {type:'text/csv;charset=utf-8'});
```

Download helper: create object URL, a.download = 'general-comments-draft.csv', click, revoke.

Checks rendering (tab 04): function runChecks() returns array of {name, detail, ok}. Called after each search. Header status updated.

Check implementations:

1. Query understood: if error → {ok:false, detail:'parse error: '+error}. else {ok:true, detail: `${termCount} term(s); ${echoLine}`}.
2. Totals: listed = hits.length; checkboxSum = sum of per-committee hit counts; jointExtra = checkboxSum - hits.length; ok = (checkboxSum === hits.length + jointExtra) trivially true... hmm. The real check: rows listed across pages equal hits — i.e., rendered rows count (min(page, hits)) plus... Actually "Rows listed across pages equal the hits" means if you clicked through all pages, total rows = hits. That's by construction. The meaningful check: per-committee counts sum = hits + joint hits (joint counted twice). Compute jointHits = number of hits with committees.length>1. checkboxSum should equal hits + jointHits. ok = checkboxSum === hits.length + jointHits. Detail shows both.
3. Chart total: bars sum === hits + jointHits. Same numbers; ok true. Detail shows both.
4. Highlight: if tree has positive terms: count hits where hiRe doesn't match shown → list up to 5 with citation; ok = count===0. If NOT-only: ok true, detail "NOT-only query: no highlighting expected".
5. Normalisation: if query raw contains `"`, `'`, or `-` (straight forms): count hits whose raw text contains the curly/dash counterpart but not the straight form... Simplify: detail: "query contains straight quote/apostrophe/hyphen; curly and dash forms were matched too; N hits contain only the curly/dash forms". Compute: for hits, check if shown text contains e.g. `’` while query had `'`. I'll compute per char type present in query. ok=true (informational pass). If query has none, detail "query has no straight quote, apostrophe or hyphen".
6. Numbering: collect hits with leading!==null && leading!==paragraph → list (citation, both numbers); shared pinpoint: group hits by title+paragraph, those with >1 → list; lettered subparas → count. ok = true if all flagged? I'll set ok=true always but detail lists counts; hmm plan wants pass/fail lines. I'll mark ok = (mismatches.length===0 && dupPin.length===0 && subparas===0)? That would fail often. But these are "known quirks" — the app flags them on rows; the check verifies flagging: ok = every such hit carries a note (by construction true). I'll do: ok true, detail: "3 leading-number mismatches (e.g. …), 1 shared pinpoint, 2 lettered sub-paragraphs — all flagged on their rows". Pass.
7. Marks: for each hit: marks === count of `[[fn:` in text && text.replace(fnRe,'')===shown. ok = all pass. Detail "7,304 hits checked" (or hits count).
8. Draft: for each draft item: find record by id, compare text_as_stored. ok = all equal. Detail "n items checked".

Header: passCount = checks.filter(ok).length; if all ok → green dot "n checks pass" else red "n checks failed" + red dot on tab 04 (add class).

Known quirks at load (before search): compute over all records:
- paragraph 0 count + example citation
- shared symbols count (distinct symbols with >1 title) + example
- joint count + example
- duplicated pinpoints: group by title+'|'+paragraph over all records, size>1 → count of extra records? "duplicated pinpoints" count = number of (title,paragraph) groups with >1 record; example.
- leading mismatches count + example.

Render in tab 04 top section "Known quirks of this file".

Now the chart. Chart.js:

```js
const ctx = document.getElementById('fig1');
chart = new Chart(ctx, {
  type:'bar',
  data:{labels, datasets:[{data, backgroundColor:'#9b2335', borderWidth:0, barPercentage:0.85, categoryPercentage:0.9}]},
  options:{
    indexAxis:'y',
    responsive:true, maintainAspectRatio:false,
    scales:{
      x:{beginAtZero:true, grid:{color:'#d9d2c3'}, ticks:{color:'#1d1b18', maxTicksLimit:10, precision:0}, border:{color:'#d9d2c3'}},
      y:{grid:{display:false}, ticks:{color:'#1d1b18', font:{family:'ui-monospace, Menlo, Consolas, monospace', size:11}}, border:{display:false}}
    },
    plugins:{legend:{display:false}, tooltip:{callbacks:{label: c=>' '+c.parsed.x+' paragraphs'}}},
    onClick:(e)=>{ const pts=chart.getElementsAtEventForMode(e.nativeEvent||e, 'nearest', {intersect:true}, true); if(pts.length){ const i=pts[0].index; tickAlone(labels[i]); } }
  },
  plugins:[valueLabelsPlugin]
});
```

valueLabels plugin:
```js
const valueLabels = {
  id:'valueLabels',
  afterDatasetsDraw(chart){
    const {ctx}=chart; const meta=chart.getDatasetMeta(0); const x=chart.scales.x;
    ctx.save(); ctx.fillStyle='#1d1b18'; ctx.font='12px ui-monospace, Menlo, Consolas, monospace'; ctx.textAlign='left'; ctx.textBaseline='middle';
    meta.data.forEach((bar,i)=>{ const v=chart.data.datasets[0].data[i]; ctx.fillText(String(v), bar.x+6, bar.y); });
    ctx.restore();
  }
};
```

Canvas height: set container height based on number of bars (e.g. bars*28+40 px) to avoid squishing; wrap in div with style height. With ≤10 committees, fine. Set maintainAspectRatio:false and container height = max(200, n*30+60).

aria-label on canvas: `Bar chart of paragraphs per committee: CRC 2091, CEDAW 1500, …`. Fallback content inside canvas tag. Table beside: same numbers, `<caption>`.

Chart update: chart.data.labels=..., chart.update(). If hits empty → show "no matches" and clear chart.

tickAlone(code): set ticked = new Set([code]); update checkboxes UI; run().

Now tab switching: buttons with data-tab; panels. Arrow key nav on tablist: keydown ArrowRight/Left → move focus+activate.

Rail hidden on draft tab: when tab 03 active, add hidden to aside (and layout becomes single column). Use class on body.

Search input focus on load: `input.focus()`.

Now header dataline: `${R.length} paragraphs from ${titles.size} General Comments (distinct title) of ${committees.size} committees, ${minYear}–${maxYear}` — wait "n General Comments (distinct title)". And source linked: `<a href="${gc.source_url}">${gc.source}</a>` if source_url else source text. Also top-level count is string "7304" — use R.length per plan.

Title: "Verbatim finder: General Comments and General Recommendations". Label: "UN TREATY BODIES · GENERAL COMMENTS".

Footer: `${gc.source}${gc.built? ' · built '+gc.built : ''}` + " · Counting, matching and sorting are done by this page's code; no model is called." + Credits: "Chart.js 4 (MIT) for FIG.01."

Now, "How this is computed" lines: under FIG.01: "How this is computed: one count per committee over the paragraphs that match the query and filters; joint General Comments count under both committees, so the bars can add up to more than the hits." Under results summary maybe. Plan mentions chart note about joint. Also a "How this is computed" near the big number? Plan: "one 'How this is computed' line near every chart or number". Add under big number: "How this is computed: records whose normalised text matches the query and that pass the filters below." Good.

Method section on tab 04: "How this is computed" short form: describe load precompute, normalisation, parser, matching, citation building, copy. A few bullet lines.

Now let me also handle "show as stored" toggle per row: state per row id: storedShown bool. Re-render row text. Keep simple: re-render the results list on toggle (page preserved). Or toggle in place: replace the text element content. I'll do in-place: button click → swap textContent/innerHTML of the .text element and the marks line label. Store flag on element dataset.

Row open state: also re-render? I'll manage open row id in state; render function builds rows; clicking toggles openId and re-renders results (only page rows, cheap). But re-render loses "show full paragraph" expansion and stored toggle — keep per-row UI state in a Map keyed by id: {open, full, stored}. On re-render, apply. Good.

Context: when open and context clicked, store ctx in rowState {ctx:'prev'|'next'} and render context block.

Now performance: run() computes hits over 7304 records with tree eval — fine. Checks over hits — marks check does regex on each hit text; with 7304 hits and texts up to ~8KB, total maybe 20MB of regex — could be ~100ms-ish, acceptable. Highlight check similar. OK.

Sorting hits: default year desc, title asc, paragraph asc. "Most matches first": count hits per title, sort by count desc, then year desc, title, paragraph. "Document order": title asc, paragraph asc (then year). Implement comparators.

Summary: `${hits.length} of ${R.length} paragraphs match · ${commCount} committees · ${minHitYear}–${maxHitYear}` + (query? '' : ' · no search words'). Order line separate: "sorted by year, newest first, then by document and paragraph" / "sorted by document, then paragraph" / "sorted by most matches first, then year".

Now write the HTML. Structure:

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Verbatim finder · General Comments</title>
<style> ... </style>
</head>
<body>
<header class="top">
  <div class="kicker">UN TREATY BODIES · GENERAL COMMENTS</div>
  <h1>Verbatim finder: General Comments and General Recommendations</h1>
  <p class="dataline"><span id="dataline"></span> · <span id="srcline"></span></p>
  <div class="checkstatus" id="checkstatus"></div>
</header>
<nav class="tabs" role="tablist" aria-label="Views">
  <button role="tab" id="tab-0" aria-controls="panel-0" aria-selected="true" data-tab="0">01 OVERVIEW</button>
  <button role="tab" id="tab-1" ...>02 PARAGRAPHS</button>
  <button role="tab" id="tab-2" ...>03 DRAFT <span id="draftcount"></span></button>
  <button role="tab" id="tab-3" ...>04 CHECK & METHOD <span id="tab4dot"></span></button>
</nav>
<div class="layout" id="layout">
  <aside class="rail" id="rail">
    <div class="railhead"><span>FILTERS</span><button id="clearall">Clear all</button></div>
    <div class="bignum" id="bignum" aria-live="polite">7,304</div>
    <div class="biglabel">matching paragraphs <span id="ofTotal"></span></div>
    <div class="how">How this is computed: …</div>
    <div class="chips" id="chips"></div>
    <div class="searchbox">
      <label for="q">SEARCH THE PARAGRAPHS</label>
      <div class="qrow"><input id="q" type="text" autocomplete="off" spellcheck="false"><button id="searchbtn">Search</button></div>
      <div class="syntax" id="syntax" hidden> ... examples ... </div>
      <div class="echo" id="echo" aria-live="polite"></div>
      <div class="err" id="qerr"></div>
      <div class="hint">Whole words, any case. Curly and straight quotes, apostrophes, dashes and hyphens count as the same, and footnote marks are skipped, so State's finds State’s and a phrase can cross a footnote.</div>
    </div>
    <div class="filtersec">
      <button class="fhead" id="fhead" aria-expanded="false"><span class="fnum">01</span> COMMITTEE, YEARS, DOCUMENT <span class="chev">▾</span></button>
      <div class="fbody" id="fbody" hidden>
        <div class="fgroup">
          <div class="flabel">COMMITTEE <button id="allnone">all / none</button></div>
          <div id="committees"></div>
        </div>
        <div class="fgroup">
          <div class="flabel">YEARS</div>
          <div class="yrow"><input id="yfrom" type="number"> <span>–</span> <input id="yto" type="number"></div>
        </div>
        <div class="fgroup">
          <div class="flabel">DOCUMENT</div>
          <select id="docsel"><option value="">all documents</option>…</select>
        </div>
      </div>
    </div>
  </aside>
  <main class="main">
    <section class="panel" role="tabpanel" id="panel-0" aria-labelledby="tab-0"> overview </section>
    <section class="panel" role="tabpanel" id="panel-1" hidden> paragraphs </section>
    <section class="panel" role="tabpanel" id="panel-2" hidden> draft </section>
    <section class="panel" role="tabpanel" id="panel-3" hidden> check </section>
  </main>
</div>
<footer>…</footer>
<div id="copybox" hidden>…</div>
<script> ... </script>
</body>
</html>
```

Wait — the filter heading count: plan says "one numbered heading, closed until clicked: 01 Committee, years, document". So single collapsible. Good, matches.

Overview panel:
```html
<h2 class="figtitle"><span class="figno">FIG.01</span> Paragraphs per committee</h2>
<p class="hint">click a bar = tick that committee alone</p>
<div class="figwrap"><div class="chartbox" id="chartbox"><canvas id="fig1" role="img" aria-label="…">fallback text</canvas></div>
<table class="figtable" id="figtable"><caption>Paragraphs per committee (same numbers as FIG.01)</caption>…</table></div>
<p class="how">How this is computed: one count per committee over the paragraphs that match the query and filters. Joint General Comments count under both committees, so the bars can add up to more than the hits.</p>
```

Paragraphs panel:
```html
<p class="summary" id="summary" aria-live="polite"></p>
<div class="orderrow"><label for="order">Order</label><select id="order">…</select><span class="hint" id="orderhint"></span></div>
<p class="hint">This page retrieves; it never writes. Every paragraph shown is a record of the file, as stored.</p>
<div id="results"></div>
<button id="more" hidden>Show 25 more</button>
```

Draft panel:
```html
<h2>Your draft (<span id="dn"></span> quotations)</h2>
<p class="hint">Kept in localStorage when allowed, in memory otherwise.</p>
<div class="draftbtns"><button id="copyall">Copy all</button><button id="dlTxt">Download .txt</button><button id="dlCsv">Download .csv</button></div>
<div id="draftlist"></div>
```

Check panel:
```html
<h2>How the app checks itself</h2>
<div id="checks"></div>
<h2>Known quirks of this file</h2>
<div id="quirks"></div>
<h2>How this is computed</h2>
<div id="method"></div>
```

CSS: paper bg, etc. Let me write it.

```css
:root{ --paper:#f4f0e8; --ink:#1d1b18; --rule:#d9d2c3; --red:#9b2335; --amber:#8a5a00; --green:#1e6b3a; --markbg:#f3e6a2; }
*{box-sizing:border-box}
[hidden]{display:none!important}
html,body{margin:0;padding:0}
body{background:var(--paper);color:var(--ink);font:16px/1.5 -apple-system,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif;padding:0 20px 40px;max-width:1180px;margin:0 auto}
```

Hmm body max-width with margin auto — fine.

Header:
```css
.top{padding:22px 0 10px;border-bottom:1px solid var(--rule); position:relative}
.kicker{font:11px/1 ui-monospace,Menlo,Consolas,monospace;letter-spacing:.18em;color:var(--red)}
h1{font-family:Georgia,"Times New Roman",serif;font-weight:400;font-size:30px;margin:8px 0 6px;max-width:60ch}
.dataline{font-size:13px;color:#4a463f;margin:0}
.checkstatus{position:absolute;right:0;top:24px;font:11px ui-monospace,...;letter-spacing:.08em}
.dot{display:inline-block;width:9px;height:9px;border-radius:50%;margin-right:6px}
.dot.g{background:var(--green)} .dot.r{background:var(--red)}
```

Tabs:
```css
.tabs{display:flex;gap:2px;border-bottom:1px solid var(--rule);margin-top:6px}
.tabs [role=tab]{appearance:none;background:none;border:none;border-bottom:2px solid transparent;padding:10px 14px;font:12px ui-monospace,Menlo,Consolas,monospace;letter-spacing:.14em;color:#6b655a;cursor:pointer}
.tabs [role=tab][aria-selected=true]{color:var(--red);border-bottom-color:var(--red)}
.tabs [role=tab]:focus-visible{outline:3px solid var(--red);outline-offset:2px}
```

Layout:
```css
.layout{display:flex;gap:28px;align-items:flex-start;padding-top:18px}
.rail{width:300px;flex:0 0 300px;position:sticky;top:12px}
.main{flex:1;min-width:0}
body.draftmode .rail{display:none}
```

Hmm — hiding rail via class; but plan says rail hidden on draft tab. Use hidden attribute on rail when tab 2 active. But `[hidden]{display:none!important}` handles it. I'll toggle hidden attr.

Rail:
```css
.railhead{display:flex;justify-content:space-between;align-items:baseline;font:11px ui-monospace;letter-spacing:.18em;color:#6b655a;border-bottom:1px solid var(--rule);padding-bottom:6px}
#clearall{...small button}
.bignum{font-family:Georgia,serif;font-size:52px;line-height:1;margin-top:14px}
.biglabel{font:11px ui-monospace;letter-spacing:.12em;color:#6b655a;margin-top:4px}
.how{font-size:12px;color:#6b655a;margin-top:8px;border-top:1px dotted var(--rule);padding-top:6px}
.chips{display:flex;flex-wrap:wrap;gap:6px;margin-top:10px}
.chip{font:11px ui-monospace;border:1px solid var(--red);color:var(--red);padding:2px 6px;border-radius:2px;background:none;cursor:pointer}
```

Search:
```css
.searchbox{margin-top:18px;border-top:1px solid var(--rule);padding-top:12px}
.searchbox label{font:11px ui-monospace;letter-spacing:.16em;color:#6b655a;display:block;margin-bottom:6px}
.qrow{display:flex;gap:6px}
#q{flex:1;min-width:0;padding:8px 10px;font:14px ui-monospace,Menlo,Consolas,monospace;background:#fffdf8;border:1px solid var(--rule);color:var(--ink)}
#q:focus{outline:3px solid var(--red);outline-offset:1px}
button.act / #searchbtn{...}
.syntax{margin-top:8px;border:1px solid var(--rule);background:#fffdf8;padding:10px;font-size:12.5px}
.syntax .ex{display:block;...button-like}
.echo{margin-top:8px;font-size:13px;color:var(--ink)}
.err{margin-top:6px;color:var(--red);font-size:13px}
.hint{font-size:12px;color:#6b655a}
```

Filter section:
```css
.filtersec{margin-top:18px;border-top:1px solid var(--rule)}
.fhead{width:100%;text-align:left;background:none;border:none;padding:10px 0;font:12px ui-monospace;letter-spacing:.14em;cursor:pointer;display:flex;gap:8px;align-items:baseline;color:var(--ink)}
.fhead .fnum{color:var(--red)}
.fhead[aria-expanded=true]{color:var(--red)}
.fbody{border-top:1px dotted var(--rule);padding:10px 0 16px}
.flabel{font:11px ui-monospace;letter-spacing:.14em;color:#6b655a;margin:12px 0 6px;display:flex;justify-content:space-between}
.ck{display:flex;align-items:baseline;gap:7px;font-size:13px;padding:2px 0;cursor:pointer}
.ck input{accent-color:var(--red)}
.ck .code{font:11px ui-monospace;color:var(--red)}
.ck .hits{color:#6b655a;font:11px ui-monospace}
.yrow{display:flex;gap:6px;align-items:center}
.yrow input{width:80px;padding:5px 7px;border:1px solid var(--rule);background:#fffdf8;font:13px ui-monospace}
#docsel{width:100%;padding:6px;border:1px solid var(--rule);background:#fffdf8;font-size:13px}
```

Results rows:
```css
.row{border-bottom:1px solid var(--rule);padding:14px 0}
.rowhead{display:block;width:100%;text-align:left;background:none;border:none;padding:0;cursor:pointer;color:inherit;font:inherit}
.meta{display:flex;flex-wrap:wrap;gap:8px;align-items:baseline;font-size:13px}
.badge{font:11px ui-monospace;border:1px solid #8a8578;padding:1px 6px;letter-spacing:.06em;color:#4a463f}
.doc{color:#4a463f}
.sym{font:12px ui-monospace}
.sym a{color:var(--ink)}
.pin{color:var(--red);font:12px ui-monospace}
.yr{color:#6b655a;font:12px ui-monospace}
.rtext{margin:8px 0 0;white-space:pre-wrap;font-size:15px}
mark{background:var(--markbg);color:var(--ink);font-weight:700;padding:0 1px}
.marksline{font-size:12px;color:#8a8578;margin-top:6px}
.marksline button{background:none;border:none;color:#6b655a;text-decoration:underline;cursor:pointer;font-size:12px;padding:0}
.note{font-size:12.5px;color:var(--amber);margin-top:6px}
.detail{margin-top:10px;border-top:1px dotted var(--rule);padding-top:10px}
.detail .btns{display:flex;flex-wrap:wrap;gap:8px}
.btn{padding:6px 12px;border:1px solid var(--ink);background:none;cursor:pointer;font:12px ui-monospace;letter-spacing:.06em;color:var(--ink)}
.btn:hover{background:#eae4d6}
.btn.primary{border-color:var(--red);color:var(--red)}
.ctx{margin-top:8px;font-size:13px}
.ctxblock{margin-top:6px;color:#6b655a;font-size:13.5px;white-space:pre-wrap;border-left:2px solid var(--rule);padding-left:10px}
```

Draft:
```css
.ditem{border-bottom:1px solid var(--rule);padding:12px 0}
.dq{font-size:15px;white-space:pre-wrap}
.dc{font:12px ui-monospace;color:var(--red);margin-top:4px}
```

Checks:
```css
.check{display:flex;gap:10px;padding:8px 0;border-bottom:1px dotted var(--rule);font-size:14px}
.check .st{font:11px ui-monospace;letter-spacing:.1em;flex:0 0 110px}
.st.pass{color:var(--green)} .st.fail{color:var(--red)}
```

Chart:
```css
.figwrap{display:flex;gap:24px;align-items:flex-start;flex-wrap:wrap}
.chartbox{flex:1;min-width:320px;position:relative}
.figtable{border-collapse:collapse;font-size:13px}
.figtable caption{text-align:left;font:11px ui-monospace;letter-spacing:.12em;color:#6b655a;padding-bottom:6px}
.figtable th,.figtable td{border-bottom:1px solid var(--rule);padding:4px 10px 4px 0;text-align:left}
.figtable td.num{text-align:right;font-family:Georgia,serif}
.figtitle{font-family:Georgia,serif;font-weight:400;font-size:22px;margin:0 0 4px}
.figno{font:11px ui-monospace;color:var(--red);letter-spacing:.14em;margin-right:10px;vertical-align:middle}
```

Footer:
```css
footer{margin-top:34px;border-top:1px solid var(--rule);padding-top:10px;font:11px ui-monospace;letter-spacing:.06em;color:#6b655a;display:flex;justify-content:space-between;flex-wrap:wrap;gap:8px}
```

Focus ring global: `:focus-visible{outline:3px solid var(--red);outline-offset:2px}`.

Copy fallback box: fixed bottom:
```css
#copybox{position:fixed;left:16px;right:16px;bottom:16px;background:#fffdf8;border:1px solid var(--red);padding:12px;z-index:50}
#copybox textarea{width:100%;height:90px;font:12px ui-monospace}
```

Now JS. Let me write it carefully.

```js
(function(){
'use strict';
const GC = window.WORKSHOP_DATA.gc;
const R = GC.records;
const FN = /\[\[fn:\d+\]\]/g;

function normText(s){
  return s.replace(FN,'')
    .replace(/[“”„]/g,'"')
    .replace(/[‘’‚]/g,"'")
    .replace(/[–—­]/g,'-')
    .replace(/\s+/g,' ')
    .toLowerCase()
    .trim();
}
```

Wait: soft hyphen `\u00AD` — include in the dash class: `/[–—\u00AD]/g`. Also maybe `\u2010-\u2015` general hyphens. Use `/[\u2010-\u2015\u00AD]/g` → '-'. That covers hyphen, non-breaking hyphen, en/em dashes. Good.

Escape regex:
```js
function escRe(s){ return s.replace(/[.*+?^${}()|[\]\\]/g,'\\$&'); }
```

Term regex (over norm):
```js
function termRe(term){
  const words = term.text.split(/\s+/).filter(Boolean).map(w=>{
    const wc = w.endsWith('*');
    const core = wc ? w.slice(0,-1) : w;
    return escRe(core) + (wc ? '\\w*' : '');
  });
  const body = words.join('\\s+');
  return new RegExp('(?<![\\p{L}\\p{N}])' + body + '(?![\\p{L}\\p{N}])', 'u');
}
```

Hmm — if term.text is empty (e.g. phrase `""`), error at parse: "empty phrase".

Highlight pattern (over shown text):
```js
function hiPat(term){
  const words = term.text.split(/\s+/).filter(Boolean).map(w=>{
    const wc = w.endsWith('*');
    const core = wc ? w.slice(0,-1) : w;
    let p='';
    for(const ch of core){
      if(ch==='"') p+='["“”„]';
      else if(ch==="'") p+="['‘’‚]";
      else if(ch==='-') p+='[-\\u2010-\\u2015\\u00AD]';
      else p+=escRe(ch);
    }
    return p + (wc?'\\w*':'');
  });
  return words.join('(?:\\s|\\[\\[fn:\\d+\\]\\])+');
}
function hiRe(terms){
  if(!terms.length) return null;
  const body = terms.map(t=>'(?<![\\p{L}\\p{N}])(?:'+hiPat(t)+')(?![\\p{L}\\p{N}])').join('|');
  return new RegExp(body,'giu');
}
```

Wait — for a single word term, hiPat returns the word pattern; wrapping with boundaries fine. For phrase, words joined by gap pattern, wrapped in boundaries — good.

Hmm, one subtlety: `(?<![\p{L}\p{N}])` before a pattern that starts with a quote class `["“”„]` — lookbehind checks char before match start; if text is `“best` and pattern starts matching at `“`... but our terms don't include quote delimiters (stripped). If a term word contains a quote char inside (e.g. `don't` → `don` + class + `t`), fine.

Tokenizer + parser as planned. makeTerm:

```js
function makeTerm(tok){
  const raw = tok.text.trim();
  const text = normText(raw); // normalises quotes/dashes/case; also collapses spaces
  if(!text) throw new Error('empty phrase');
  return {t:'term', raw: raw.replace(/\s+/g,' '), text, phrase: !!tok.phrase, wild: raw.endsWith('*'), re: termRe({text})};
}
```

Wait normText removes fn marks — query won't have them; harmless. But normText lowercases — for echo I keep raw. wild detection: raw ends with '*' — after norm, text ends with '*' too (norm doesn't remove '*'). termRe handles trailing '*'. OK, drop separate wild flag; echo can check text.endsWith('*').

Hmm: normText trims and collapses whitespace — for phrase "best   interests" → "best interests" → regex `best\s+interests`. Good.

Parser errors: throw Error with message; catch in runSearch: show error in #qerr and checks.

Tree eval & term collection:

```js
function evalTree(n, s){
  if(n.t==='term') return n.re.test(s);
  if(n.t==='not') return !evalTree(n.a,s);
  if(n.t==='and') return evalTree(n.a,s)&&evalTree(n.b,s);
  return evalTree(n.a,s)||evalTree(n.b,s);
}
function collectTerms(n, neg, out){
  if(n.t==='term'){ if(!neg) out.push(n); }
  else if(n.t==='not') collectTerms(n.a, true, out);
  else { collectTerms(n.a, neg, out); collectTerms(n.b, neg, out); }
}
function countTerms(n){ return n.t==='term'?1: (n.t==='not'? countTerms(n.a) : countTerms(n.a)+countTerms(n.b)); }
```

Echo:

```js
function echoTree(n){
  if(n.t==='term') return n.phrase ? 'the phrase “'+n.raw+'”' : (n.text.endsWith('*') ? 'the word '+n.raw+' (any ending)' : 'the word '+n.raw);
  if(n.t==='not') return 'without '+echoTree(n.a);
  if(n.t==='and') return echoTree(n.a)+' and '+echoTree(n.b);
  return echoTree(n.a)+' or '+echoTree(n.b);
}
```

Precompute records:

```js
const symbolTitles = new Map();
R.forEach(r=>{ if(!symbolTitles.has(r.symbol)) symbolTitles.set(r.symbol,new Set()); symbolTitles.get(r.symbol).add(r.title); });

const FULL = {...};
const recs = R.map(r=>{
  const shown = r.text.replace(FN,'');
  const marks = (r.text.match(FN)||[]).length;
  const norm = normText(r.text);
  const lm = r.text.match(/^(\d{1,3})\.\s/);
  const leading = lm ? parseInt(lm[1],10) : null;
  const sm = r.text.match(/^\(([a-z]{1,4})\)/);
  const pinpoint = sm ? 'subpara. ('+sm[1]+')' : (r.paragraph===0 ? 'preamble' : 'para. '+r.paragraph);
  const codes = new Set();
  (r.symbol.match(/\b(CAT|CCPR|CED|CEDAW|CERD|CESCR|CMW|CRC|CRPD)\b/g)||[]).forEach(c=>codes.add(c));
  if(/CAT\/OP/.test(r.symbol)) codes.add('CAT-OP');
  if(r.committee) codes.add(r.committee);
  const committees = [...codes];
  const joint = (r.symbol.match(/\b(CAT|CCPR|CED|CEDAW|CERD|CESCR|CMW|CRC|CRPD)\b/g)||[]).length > 1;
  const shared = symbolTitles.get(r.symbol).size > 1;
  return {r, shown, marks, norm, leading, sub: sm?sm[1]:null, pinpoint, committees, joint, shared,
    citation: null, copied: null};
});
```

Citation computed lazily or at load — compute at load:

```js
function docName(t){ const m = t.match(/^(.*?)(?::|\son\b)/); return (m? m[1] : t).trim(); }
recs.forEach(o=>{
  o.citation = o.shared ? o.r.committee+', '+docName(o.r.title)+' ('+o.r.symbol+'), '+o.pinpoint : o.r.symbol+', '+o.pinpoint;
  let c = o.shown;
  if(o.leading!==null && o.leading===o.r.paragraph) c = c.replace(/^\d{1,3}\.\s/,'');
  o.copied = c;
  o.quotation = '“'+c+'” '+o.citation;
});
```

Wait — the leading-strip regex on shown: shown starts with the leading number (same as text start). `^\d{1,3}\.\s` — but shown may start with whitespace? text starts with number per leading match on text; shown = text minus fn marks; fn marks at start? unlikely. Use same regex on shown; if leading matched text, shown should too. Fine.

Hmm, careful: `o.r.paragraph` could be 0 (preamble) — leading null then. OK.

Also note: paragraph could be a string? Spec says int. OK.

Committee list for filter: all codes across recs, with counts:

```js
const codeCounts = new Map();
recs.forEach(o=>o.committees.forEach(c=>codeCounts.set(c,(codeCounts.get(c)||0)+1)));
const allCodes = [...codeCounts.keys()].sort((a,b)=>codeCounts.get(b)-codeCounts.get(a) || a.localeCompare(b));
```

Years: min/max over r.year.

Titles for doc select: distinct titles with their committee & short_title:

```js
const docList = [];
const seenT = new Set();
recs.forEach(o=>{ if(!seenT.has(o.r.title)){ seenT.add(o.r.title); docList.push({title:o.r.title, committee:o.r.committee, short:o.r.short_title, year:o.r.year}); } });
docList.sort((a,b)=> (a.committee||'').localeCompare(b.committee||'') || a.short.localeCompare(b.short));
```

Group by committee in select with optgroup.

State:

```js
const state = {
  tree:null, error:null, query:'',
  ticked:new Set(allCodes),
  yFrom:minYear, yTo:maxYear, doc:'',
  order:'year', shown:25,
  draft: loadDraft(),
  rowState:new Map()
};
```

Filters pass:

```js
function passes(o){
  for(const c of o.committees) if(state.ticked.has(c)) { var okC=true; break; }
  ...
}
```
Simpler:
```js
function passes(o){
  if(!o.committees.some(c=>state.ticked.has(c))) return false;
  const y=o.r.year; if(y<state.yFrom||y>state.yTo) return false;
  if(state.doc && o.r.title!==state.doc) return false;
  return true;
}
```

run():

```js
function run(){
  let hits = recs.filter(o=> passes(o) && (!state.tree || evalTree(state.tree, o.norm)));
  // sort
  ...
  state.hits = hits;
  renderAll();
}
```

Sorting comparators:

```js
const orders = {
  year: (a,b)=> b.r.year-a.r.year || a.r.title.localeCompare(b.r.title) || a.r.paragraph-b.r.paragraph,
  doc: (a,b)=> a.r.title.localeCompare(b.r.title) || a.r.paragraph-b.r.paragraph,
  matches: (a,b)=> (titleHits.get(b.r.title)-titleHits.get(a.r.title)) || b.r.year-a.r.year || a.r.title.localeCompare(b.r.title) || a.r.paragraph-b.r.paragraph
};
```

titleHits computed per run for 'matches'.

Per-committee hit counts:

```js
const perComm = new Map();
hits.forEach(o=>o.committees.forEach(c=>perComm.set(c,(perComm.get(c)||0)+1)));
const jointHits = hits.filter(o=>o.committees.length>1).length;
```

Render functions:

renderRail(): bignum = hits.length formatted (toLocaleString('en-US')), "of 7,304". chips. committee checkbox hit counts `[n]` (show after any run; before first run show totals? Plan: "after a search, its hits in brackets" — I'll always show counts of current hits; initial run happens at load with empty query so counts = totals. Fine.)

Actually run() at load with empty query → hits = all passing filters = all records. Good, everything populated initially.

renderChips(): 
- if ticked.size < allCodes.length → chip `committees ${ticked.size}/${allCodes.length} ×`
- if yFrom>minYear||yTo<maxYear → chip `years ${yFrom}–${yTo} ×`
- if doc → chip `document: ${short} ×`
Chip click: reset that filter, update UI controls, run().

renderOverview(): chart data from perComm (only codes with >0? include all ticked codes with 0? "one bar per committee, ranked by value" over hits — I'll include only committees with hits>0, ranked desc). Update chart + table + aria-label. If no hits: show message.

renderResults(): summary line, order hint, rows up to state.shown, more button.

Row rendering:

```js
function rowHTML(o){
  const st = state.rowState.get(o.r.id)||{};
  const text = st.stored ? o.r.text : o.shown;
  const hi = hiReGlobal; // built per run from positive terms
  const body = st.full || text.length<=700 ? highlightHTML(text, hi) : highlightHTML(cut700(text), hi) + ' …';
  ...
}
```

Hmm — highlight on truncated text: fine.

cut700: 
```js
function cut700(t){ let c=t.slice(0,700); const sp=c.lastIndexOf(' '); if(sp>400) c=c.slice(0,sp); return c; }
```

Word count for the button: `o.shown.split(/\s+/).length` words.

Notes (amber):
- leading mismatch: `the text begins ‘${leading}.’ but the record is ${pinpoint}: check the document`
- subpara: `a lettered sub-paragraph, numbered ${paragraph} by the file`
- shared pinpoint: need precomputed map title+paragraph → count>1: `two records share this pinpoint`
- joint: `joint General Comment`

Precompute dupPin: map key title+'|'+paragraph → count over all recs.

Row meta: badge(s) — committee badge: show o.r.committee badge; if joint show both badges (committees codes). Plan: "A joint General Comment ... shows both badges". So badges = o.committees codes. Plus short_title, symbol link, pinpoint, year.

Symbol link: `<a href="${o.r.doc_url}" target="_blank" rel="noopener">${o.r.symbol}</a>`.

Detail panel (when open): buttons with data-action and data-id:
- Copy citation → copyText(o.citation, 'Copied: '+o.citation)
- Copy quotation → copyText(o.quotation, ...)
- Add to draft → addToDraft(o)
- Context: previous | next — two buttons; on click set st.ctx and re-render.

Context block: find sibling: recs with same title and paragraph === o.r.paragraph±1. Build map title→sorted by paragraph list for quick lookup: titleMap: title → array of recs sorted by paragraph. prev = last with paragraph < o.r.paragraph; next = first with paragraph > o.r.paragraph. Show pinpoint + shown text (grey). If none, "no previous paragraph in this document".

Draft tab render: items list; each: quotation (dq), citation (dc), remove button. Buttons copy all / downloads. Tab label update: `03 DRAFT (${n})` — set span text `(${n})` or '' when 0? Plan: tab name carries count "03 DRAFT (4)". I'll always show `(n)`.

addToDraft(o): item = {id, citation, quotation, symbol, paragraph, pinpoint, committee, short_title, year, text_copied:o.copied, text_as_stored:o.r.text, doc_url}; avoid duplicates by id (if exists, note "already in draft"). push, save, renderDraft, update tab count.

Copy all: items.map(it=>it.quotation).join('\n\n')? Plan: "quotation, new line, citation, blank line between items" — but quotation already includes citation appended ("quotation as copied" = quotation + citation). Hmm: "each with its quotation as copied, its citation" — the stored quotation includes citation. Copy all: "quotation, new line, citation, blank line between items" — so item text = quotation + '\n' + citation? But quotation as copied already ends with citation... The plan for Copy quotation: copies shown text in quotation marks, a space, the citation. So quotation string = “text” citation. Then Copy all = each item's quotation + newline + citation? That duplicates. I'll interpret: each draft entry displays quotation (with citation) and citation line; Copy all joins entries as `quotation\n\n` where quotation already contains citation — hmm but plan explicitly says "quotation, new line, citation, blank line between items". To follow literally: entry = quotation + '\n' + citation + '\n\n'. Since quotation = “…” citation, that gives citation twice. Maybe their "quotation" in draft = just the quoted text, and citation separate. But "Copy quotation" copies text+citation together... The draft item fields include text_copied and citation separately. I'll make Copy all produce: `“text” citation` per item (i.e., it.quotation) joined with blank line — and display in draft list the quotation and citation on separate lines. That satisfies "quotation, new line, citation" visually if I store quotation as just the quoted text? Hmm.

Let me re-read: "**Copy quotation** copies the shown text in quotation marks, a space, the citation." So clipboard gets `“text” SYMBOL, para. N`. "**Add to draft** sends both to the Draft tab." Draft shows "each with its quotation as copied, its citation and a remove button". So draft item shows quotation-as-copied (which includes citation) AND citation separately. Copy all: "quotation, new line, citation, blank line between items" — I'll do per item: `it.quotation + '\n' + it.citation` joined by '\n\n'. Slight duplication but literal. Actually that looks odd. Alternative: quotation field stored = the quoted text only (`“text”`), and "as copied" means the copy action produced text+citation. Hmm. I'll store `quotation` = full copied string (text + citation) since "quotation as copied", and Copy all = items joined: `it.quotation` + '\n\n'... but plan says quotation, new line, citation. 

Decision: store both: `quotation` (the “text” part only, in quotes) and `citation`. Copy quotation button copies `quotation + ' ' + citation`. Draft displays quotation line then citation line. Copy all: `(quotation + '\n' + citation)` joined with '\n\n'. This matches the plan exactly. CSV text_copied = quotation + ' ' + citation? "text_copied" — the text as copied... I'll set text_copied = o.copied (the raw text without quotes/citation) — hmm "text_copied" ambiguous. I'll set text_copied = the full copied quotation string (quotation + ' ' + citation)? The field name says text copied. I'll use o.copied (the paragraph text that was copied). Actually "text_copied" vs "text_as_stored" — parallel fields: what was copied vs what's stored. Copied = shown text with leading dropped = o.copied. Good, use that.

So draft item: {id, citation, quotation: '“'+o.copied+'”', symbol, paragraph, pinpoint, committee, short_title, year, text_copied: o.copied, text_as_stored: o.r.text, doc_url}. Copy quotation button: copyText(item.quotation+' '+item.citation). Copy all: items.map(it=>it.quotation+'\n'+it.citation).join('\n\n'). 

Downloads: .txt = same as copy all. .csv as spec'd.

Checks render + header status:

```js
function runChecks(){
  const checks=[];
  const hits=state.hits||[];
  // 1 query
  if(state.error) checks.push({name:'Query understood', ok:false, detail:'parse error — '+state.error});
  else checks.push({name:'Query understood', ok:true, detail:(state.tree? countTerms(state.tree)+' term(s): '+echoLine : 'no search words (empty query matches all paragraphs that pass the filters)')});
  // 2 totals
  const jointHits = hits.filter(o=>o.committees.length>1).length;
  const sum = [...perComm.values()].reduce((a,b)=>a+b,0);
  checks.push({name:'Totals', ok: sum===hits.length+jointHits, detail:`rows listed across pages = ${hits.length} hits; committee counts sum to ${sum} = ${hits.length} hits + ${jointHits} joint hits`});
  // 3 chart
  checks.push({name:'Chart total', ok: sum===hits.length+jointHits, detail:`FIG.01 bars sum to ${sum}, hits ${hits.length} + joint ${jointHits}`});
  // 4 highlight
  const posTerms=[]; if(state.tree) collectTerms(state.tree,false,posTerms);
  if(posTerms.length){
    const hre = hiRe(posTerms);
    const bad = hits.filter(o=>!hre.test(o.shown));
    // reset lastIndex — test with non-global? hiRe has g flag; use separate test regex without g
    ...
  }
}
```

Careful with `g` flag and `.test` statefulness — create a non-global version for testing: `new RegExp(hre.source,'iu')`. I'll make hiRe(terms, global) param.

bad list: up to 5 citations: `matched, not highlighted: ${o.citation}`. ok = bad.length===0.

  // 5 normalisation
```js
  const q=state.query;
  const hasStraight = /["'-]/.test(q);
  if(hasStraight){
    // count hits whose shown text contains curly/dash form but not the straight counterpart of query chars
    let onlyCurly=0;
    hits.forEach(o=>{ const t=o.r.text; let has=false, hasC=false;
      if(q.includes('"') && t.includes('"') ) has=true; if(q.includes('"') && /[“”„]/.test(t)) hasC=true;
      ... 
    });
  }
```
Simplify: for each of `"`, `'`, `-` present in query: hits where shown contains the curly/dash variant. Count hits that contain any variant but not the straight char. Detail: `query contains straight quote/apostrophe/hyphen; curly and dash forms were matched too — N hits contain only the curly/dash forms`. ok:true.

  // 6 numbering
```js
  const mism = hits.filter(o=>o.leading!==null && o.leading!==o.r.paragraph);
  const subs = hits.filter(o=>o.sub);
  const dups = hits.filter(o=>dupPin.get(o.r.title+'|'+o.r.paragraph)>1);
  checks.push({name:'Numbering', ok:true, detail:`${mism.length} leading-number mismatches (${mism.slice(0,3).map(o=>o.citation+' text begins '+o.leading).join('; ')||'none'}); ${dups.length} shared pinpoints; ${subs.length} lettered sub-paragraphs — each flagged on its row`});
```
Hmm ok should maybe be true always (informational). But plan says lines are "pass" or "check failed". I'll mark ok = true (the app flagged them all — verified by construction) but if any exist, is that a "fail"? The header would be red whenever quirks present in hits, which is honest but noisy. The plan: "A failed check marks rows; it never drops them." — implies failed checks relate to rows being marked. Numbering quirks mark rows... I think marking them "check failed" when present is actually in spirit: the check is "numbering is clean"; if not clean, it says "check failed" with pinpoints concerned, and rows are marked. Hmm but then header shows failed often. The plan explicitly lists under checks: "Numbering. Hits whose leading number differs..." without saying pass/fail. And "A failed check marks rows; it never drops them" — suggests failed checks correspond to marked rows. I'll make Numbering check ok=false when mism/dups/subs exist, with detail listing them, since rows carry amber notes. Actually wait — that means searching anything touching para-0 preambles fails. Eh. It's honest: "check failed" = the file has numbering quirks in these hits, rows marked. I'll go with ok = (mism.length+dups.length+subs.length)===0, detail lists them. Hmm, but lettered sub-paragraphs are legitimately numbered by the file... The plan says rows carry the note "a lettered sub-paragraph, numbered 2 by the file" — a caution, not an error. 

Let me reconsider: the checks are "can I trust this" — the app verifying its own computation. Numbering check = "did the app flag every numbering quirk?" → always pass, detail lists quirks found. Marks check = "marks removed == count of [[fn: and reconstruction exact" → pass/fail real. Draft check real. Highlight real. Totals real. I'll go: Numbering ok=true with detail listing counts (it's a report of flagged rows). That keeps header meaningful. But then "check failed" rarely appears... fine, it appears when real problems occur.

Hmm, actually let me make Numbering ok = true but if there are mismatches the detail says "flagged on rows". OK.

  // 7 marks
```js
  let bad=0;
  hits.forEach(o=>{ const c=(o.r.text.match(/\[\[fn:/g)||[]).length; if(c!==o.marks || o.r.text.replace(FN,'')!==o.shown) bad++; });
  checks.push({name:'Footnote marks', ok:bad===0, detail:`for ${hits.length} hits, marks removed = count of [[fn: in the stored text and removing them reproduces the shown text exactly${bad?'; '+bad+' mismatches':''}`});
```

  // 8 draft
```js
  const byId=new Map(recs.map(o=>[o.r.id,o]));
  let dbad = state.draft.filter(it=>{ const o=byId.get(it.id); return !o || o.r.text!==it.text_as_stored; });
  checks.push({name:'Draft', ok:dbad.length===0, detail:`${state.draft.length} draft item(s) re-checked against the stored text${dbad.length?'; '+dbad.length+' differ':''}`});
```

Header: total checks = checks.length; failed = checks.filter(!ok).length; status: failed? red `${failed} of ${checks.length} checks failed` : green `${checks.length} checks pass`. Tab 04 dot: add red dot span when failed.

Quirks at load (over all recs):
```js
quirks = [
 {label:'paragraph 0 (preambles)', items: recs.filter(o=>o.r.paragraph===0), ex: first citation},
 {label:'symbols shared by several General Comments', ...},
 {label:'joint General Comments (two symbols in one record)', ...},
 {label:'duplicated pinpoints (same document and paragraph)', ...},
 {label:'leading number differs from the paragraph field', ...}
];
```
Render each: count + example citation.

Method section text: short bullets:
- Load: each record's normalised text, footnote-mark count, leading number, pinpoint, citation and committee codes are computed once at load.
- Normalisation: footnote marks removed; curly/straight quotes, apostrophes, dashes and hyphens unified; whitespace collapsed; lower case. The query is normalised the same way.
- Matching: the query parses to a Boolean tree (NOT, then AND, then OR; parentheses override; adjacent terms are AND). Each term is a whole-word regular expression over the normalised text; a trailing star allows any ending. Counting, filtering, sorting and highlighting are done by this page's code.
- Citation: built only from the record's fields — symbol, paragraph, committee and title; shared symbols get the committee and document name first. Nothing is invented; no model is called.

Now events wiring:

- searchbtn click & Enter in #q → doSearch().
- doSearch(): state.query = q.value; parse; if error → state.error, state.tree=null? Plan: "An unbalanced quote or parenthesis shows a message and no results." So on error: show message, results area shows nothing? "no results" — I'll set hits=[] and echo error. Set state.error=msg; state.tree=null; run() but with error flag → renderResults shows error message and no rows; checks show parse error. Hmm "no results" — yes empty results with the message. I'll keep hits computed as [] when error. Actually simpler: on error, set state.error and skip matching (hits=[]), render everything with error shown in box + echo area + checks.
- input event: if value non-empty → hide syntax; if empty and focused → show syntax.
- focus → if empty show syntax; blur → hide syntax? "While the box is empty and has focus, a short list opens" — hide on blur. OK.
- example buttons: set q.value = example; doSearch().
- clearall: reset query, ticked=all, years, doc, order? keep order; run; clear input; hide syntax.
- committee checkbox change → update ticked; run().
- all/none button: toggles — if all ticked → none; else all. Label "all / none" — clicking sets all if not all ticked else none. Then run.
- yfrom/yto change → clamp, run.
- docsel change → run.
- fhead click → toggle aria-expanded + hidden on fbody.
- order change → state.order; run() (re-sort; keep shown count? reset shown to 25? keep). I'll keep shown.
- more button → state.shown += 25; renderResults.
- tabs click/arrow → switchTab(i).
- row interactions via event delegation on #results: click on [data-action].
- copybox close button.

switchTab(i): update aria-selected, hidden panels, rail hidden when i===2, body class. Also when switching to 1 or 0 re-render? Not needed; render once per run. But chart needs resize when panel becomes visible (Chart.js with hidden canvas has 0 size). Solution: when switching to tab 0, call chart.resize() or re-render chart. I'll call renderOverview() on tab switch to 0 (chart.update()). Chart.js handles resize if container visible; call `chart.resize()` after unhiding. I'll just re-run renderOverview() which updates data and calls chart.update(); if canvas was display:none, Chart.js may have stale size — call chart.resize() first. Should be OK.

Keyboard on tablist: keydown on nav: ArrowRight/ArrowLeft/Home/End → focus & activate.

aria-live regions: bignum, summary, copied message (#live). 

Copy:

```js
const liveEl = ...;
async function copyText(t, label){
  let ok=false;
  try{ if(navigator.clipboard && navigator.clipboard.writeText){ await navigator.clipboard.writeText(t); ok=true; } }catch(e){ ok=false; }
  if(ok){ live(label+' — copied: '+t); }
  else { showCopyBox(t); live(label+' — clipboard refused; select and copy from the box'); }
}
```

showCopyBox: fill textarea, unhide, focus+select.

live(msg): set textContent of #live (aria-live polite). To re-announce same message, append zero-width? Just set textContent; fine.

Number formatting: `n.toLocaleString('en-US')`.

Now the syntax help content:

```
<div class="syntax" id="syntax" hidden>
  <div>a space or AND joins words · OR · NOT or a leading minus</div>
  <div>"an exact phrase" in double quotes</div>
  <div>( parentheses )</div>
  <div>a star at the end of a word for any ending (child* finds children)</div>
  <div>operators in capitals; lower-case "or" is a word</div>
  <div class="exs">Try:
    <button class="ex" data-q='"best interests" AND child'>"best interests" AND child</button>
    <button class="ex" data-q='(torture OR ill-treatment) NOT detention'>(torture OR ill-treatment) NOT detention</button>
    <button class="ex" data-q='"reasonable accommodation'>"reasonable accommodation"</button>
  </div>
</div>
```

Examples as options that fill and run — buttons with data-q; click → q.value=data-q; doSearch(). Arrow keys: "the example list opens with the arrow keys" — make examples focusable buttons; Down arrow from input moves focus to first example? I'll add: keydown on #q ArrowDown → focus first .ex. Buttons naturally arrow-navigable? Not automatically; add roving? Keep simple: ArrowDown focuses first example; Tab works anyway.

Now header dataline: `${R.length.toLocaleString()} paragraphs from ${titles.size} General Comments (distinct title) of ${allCodes.length} committees, ${minYear}–${maxYear}`. Source: GC.source linked to GC.source_url if present.

Wait — "n General Comments (distinct title)" — 188 distinct titles but 159 symbols; the plan says "n General Comments (distinct `title`)". Use titles.size.

Footer: `${GC.source||'WORKSHOP_DATA.gc'}${GC.built? ' · built '+GC.built:''} · Counting, matching and sorting are done by this page's code; no model is called.` plus credits: `Credits: Chart.js 4 (MIT) renders FIG.01.` Put credits as separate line.

Now — one more detail: "the top-level `count` is the string '7304'" — use R.length.

Edge: `year` may be missing? Spec says filled. Defensive: `const y = r.year||0`.

Let me also handle the "show as stored" toggle: button in marksline: if marks>0 show "N footnote marks removed · show as stored" else nothing? Plan: "a grey line under it says '3 footnote marks removed · show as stored'". If 0 marks, show "no footnote marks" without link? I'll show line only if marks>0: "3 footnote marks removed · show as stored" / after toggle: "showing as stored · show without marks". If marks===0, show "no footnote marks in this paragraph" grey. Fine.

Toggle handler: st.stored=!st.stored; re-render results (renderResults()).

Full paragraph toggle: st.full=!st.full; re-render.

Row open: st.open=!st.open; re-render.

Context: st.ctx='prev'|'next'; re-render.

Since re-render rebuilds all shown rows (≤ maybe hundreds if user clicked show more many times — could be thousands of rows... "Show 25 more" repeatedly could render 7304 rows → slow). Cap? If hits large and user clicks more many times, rendering thousands of rows with highlight could be slow. Mitigate: cap shown at, say, 200 rows with note? Plan doesn't cap. I'll cap at 500 with a hint "showing first 500 of N — narrow the search to see more"? That deviates. Alternatively render incrementally without full re-render on toggle: toggle handlers update only that row's DOM. That's better: implement row update in place.

Simpler approach: event delegation; on toggle actions, update only the affected row element via targeted DOM ops:
- open toggle: toggle hidden on the row's .detail, set aria-expanded.
- stored toggle: replace .rtext innerHTML, update marksline.
- full toggle: replace .rtext innerHTML.
- ctx: fill .ctxblock.

So renderResults builds rows once per run; interactions mutate in place. Row state map still useful to persist across re-renders (e.g., after filter change). I'll keep rowState and apply on build.

Let me now write row build:

```js
function buildRow(o){
  const st = getRowState(o.r.id);
  const art=document.createElement('article'); art.className='row'; art.dataset.id=o.r.id;
  // header button
  const h=document.createElement('h3'); h.className='rowh';
  const btn=document.createElement('button'); btn.className='rowhead'; btn.setAttribute('aria-expanded', st.open?'true':'false');
  btn.innerHTML = metaHTML(o);
  h.appendChild(btn); art.appendChild(h);
  const body=document.createElement('div'); body.className='rbody';
  body.innerHTML = textHTML(o, st) + marksLineHTML(o, st) + notesHTML(o);
  art.appendChild(body);
  const det=document.createElement('div'); det.className='detail'; det.hidden=!st.open;
  det.innerHTML = detailHTML(o, st);
  art.appendChild(det);
  return art;
}
```

metaHTML:
```js
function metaHTML(o){
  const badges = o.committees.map(c=>`<span class="badge">${c}</span>`).join(' ');
  return `<span class="meta">${badges} <span class="doc">${esc(o.r.short_title)}</span> · <span class="sym"><a href="${esc(o.r.doc_url)}" target="_blank" rel="noopener">${esc(o.r.symbol)}</a></span> · <span class="pin">${esc(o.pinpoint)}</span> · <span class="yr">${o.r.year}</span></span>`;
}
```

textHTML(o, st): 
```js
const t = st.stored? o.r.text : o.shown;
let html;
if(st.full || t.length<=700) html = highlightHTML(t, state.hi);
else html = highlightHTML(cut700(t), state.hi) + ' … <button class="linkbtn fullbtn" data-action="full">Show the full paragraph ('+wordCount(o.shown)+' words)</button>';
return `<p class="rtext">${html}</p>`;
```

Hmm the "Show the full paragraph" button inside p — fine.

marksLineHTML:
```js
if(o.marks>0) return `<div class="marksline">${o.marks} footnote mark${o.marks>1?'s':''} removed · <button class="linkbtn" data-action="stored">${st.stored?'show without marks':'show as stored'}</button></div>`;
return `<div class="marksline">no footnote marks in this paragraph</div>`;
```

notesHTML:
```js
const notes=[];
if(o.leading!==null && o.leading!==o.r.paragraph) notes.push(`the text begins ‘${o.leading}.’ but the record is ${o.pinpoint}: check the document`);
if(o.sub) notes.push(`a lettered sub-paragraph, numbered ${o.r.paragraph} by the file`);
if(dupPin.get(o.r.title+'|'+o.r.paragraph)>1) notes.push('two records share this pinpoint');
if(o.joint) notes.push('joint General Comment');
return notes.length? `<div class="note">${notes.map(esc).join('<br>')}</div>`:'';
```

detailHTML:
```js
`<div class="btns">
  <button class="btn" data-action="cite">Copy citation</button>
  <button class="btn" data-action="quote">Copy quotation</button>
  <button class="btn primary" data-action="draft">Add to draft</button>
</div>
<div class="ctx">Context: <button class="linkbtn" data-action="ctxprev">previous</button> | <button class="linkbtn" data-action="ctxnext">next</button></div>
<div class="ctxblock" ${st.ctx?'':'hidden'}>${st.ctx? ctxHTML(o,st.ctx):''}</div>`
```

ctxHTML: find sibling via titleMap; show `<span class="pin">${pinpoint}</span> ${highlight? no, plain esc(shown)}` in grey.

Delegation on #results click:
```js
resultsEl.addEventListener('click', e=>{
  const b=e.target.closest('[data-action]'); if(!b) return;
  const art=e.target.closest('.row'); const id=art.dataset.id; const o=byId.get(id); const st=getRowState(id);
  const act=b.dataset.action;
  if(act==='cite') copyText(o.citation, 'Citation');
  else if(act==='quote') copyText(o.quotation, 'Quotation');
  else if(act==='draft') addToDraft(o);
  else if(act==='stored'){ st.stored=!st.stored; refreshRow(art,o,st); }
  else if(act==='full'){ st.full=true; refreshRow(art,o,st); }
  else if(act==='ctxprev'){ st.ctx = st.ctx==='prev'?null:'prev'; refreshRow(art,o,st); }
  else if(act==='ctxnext'){ st.ctx = st.ctx==='next'?null:'next'; refreshRow(art,o,st); }
});
```

Also rowhead click toggles open: separate handler: if e.target.closest('.rowhead') → st.open=!st.open; refreshRow. But rowhead contains the symbol link — clicking link shouldn't toggle; check `if(e.target.closest('a')) return;`.

refreshRow(art,o,st): update btn aria-expanded, det.hidden, and re-set body/det innerHTML. Simplest: replace art's rbody and detail innerHTML:

```js
function refreshRow(art,o,st){
  const btn=art.querySelector('.rowhead'); btn.setAttribute('aria-expanded', st.open?'true':'false');
  art.querySelector('.rbody').innerHTML = textHTML(o,st)+marksLineHTML(o,st)+notesHTML(o);
  const det=art.querySelector('.detail'); det.hidden=!st.open; det.innerHTML=detailHTML(o,st);
}
```

OK.

addToDraft:
```js
function addToDraft(o){
  if(state.draft.some(it=>it.id===o.r.id)){ live('Already in the draft: '+o.citation); return; }
  state.draft.push({id:o.r.id, citation:o.citation, quotation:'“'+o.copied+'”', symbol:o.r.symbol, paragraph:o.r.paragraph, pinpoint:o.pinpoint, committee:o.r.committee, short_title:o.r.short_title, year:o.r.year, text_copied:o.copied, text_as_stored:o.r.text, doc_url:o.r.doc_url});
  saveDraft(); renderDraft(); live('Added to draft: '+o.citation);
}
```

renderDraft: list + count + tab label.

Draft item HTML:
```html
<div class="ditem">
  <p class="dq">“…”</p>
  <p class="dc">citation</p>
  <button class="btn" data-rm="id">Remove</button>
</div>
```
Delegation on #draftlist.

Copy all / downloads:

```js
function draftText(){ return state.draft.map(it=>it.quotation+'\n'+it.citation).join('\n\n'); }
copyall → copyText(draftText(), 'Draft');
dlTxt → download('general-comments-draft.txt', draftText(), 'text/plain;charset=utf-8');
dlCsv → build csv with BOM.
```

download(name, content, type): Blob([content],{type}), URL.createObjectURL, a.click, revoke after timeout.

CSV:
```js
function toCSV(){
  const cols=['citation','symbol','paragraph','pinpoint','committee','short_title','year','text_copied','text_as_stored','doc_url'];
  const q=v=>'"'+String(v==null?'':v).replace(/"/g,'""')+'"';
  const lines=[cols.map(q).join(',')];
  state.draft.forEach(it=>lines.push(cols.map(c=>q(it[c])).join(',')));
  return '\uFEFF'+lines.join('\r\n');
}
```

Now the chart tick-alone: labels are committee codes; tickAlone(code): state.ticked=new Set([code]); sync checkboxes; run().

Checkbox sync: rebuild committee list HTML (with hit counts) — or update checked props. I'll re-render the committee container each run (cheap, 10 items).

Committee item HTML:
```html
<label class="ck"><input type="checkbox" data-code="CRC" ${ticked?'checked':''}> <span class="code">CRC</span> <span class="nm">Committee on the Rights of the Child</span> <span class="hits">[2,091]</span></label>
```
Change delegation on #committees.

Years inputs: set values at init; on 'change' → parse ints, clamp to [minYear,maxYear], if yFrom>yTo swap? Just clamp: yFrom=min(yFrom,yTo)... I'll read both, clamp each to range, if from>to set from=to. Update inputs, run.

Doc select: optgroups:
```js
let html='<option value="">all documents ('+docList.length+')</option>';
group by committee: iterate docList sorted; when committee changes, open optgroup label=committee (full name).
```

Now initial run: build everything, run() with empty query.

Also "the search box has focus on load": q.focus() at end. But focusing shows syntax list — good.

aria-live: bignum has aria-live polite; summary; #live for copied messages.

One more: "After a search, a line echoes the query as understood". Echo element updated in run(): if error → show error in #qerr and echo empty; else echo = `Paragraphs containing ${echoTree(tree)}` or for NOT-only root: special. Detect NOT-only: tree.t==='not' && tree.a.t==='term' (or any not-root) → `Paragraphs without X — a NOT-only query matches everything that lacks these terms`. I'll check root t==='not'.

Also empty query: echo = 'no search words — listing every paragraph that passes the filters'.

Summary line: `${fmt(hits.length)} of ${fmt(R.length)} paragraphs match · ${commCount} committees · ${ymin}–${ymax}` + (tree? '' : ' · no search words'). commCount = distinct committees among hits (union of committees). ymin/ymax over hits years. If hits empty: "0 of 7,304 paragraphs match".

Order hint: map order→text: year: 'sorted by year, newest first, then by document and paragraph'; doc: 'sorted by document, then paragraph'; matches: 'sorted by most matches first, then year, document and paragraph'.

Now — the "How this is computed" line under big number: "How this is computed: records whose normalised text matches the query and that pass the filters below; counting is done by this page's code."

FIG.01 aria-label: `Bar chart, paragraphs per committee: CRC 2,091; CEDAW 1,204; …` Build from data.

Fallback table: rows committee + count.

Chart container height: set style.height = (n*30+70)+'px' before update.

Now, potential pitfall: Chart.js preloaded as window.Chart — guard `if(window.Chart)`.

Let me also handle `paragraph` possibly being string in some records? Spec says int. I'll coerce `const p = +r.paragraph`.

dupPin map: key title+'|'+p → count.

titleMap: title → array of recs (for context). Build once.

byId map: id → rec object.

Now write the checks panel HTML: each check:
```html
<div class="check"><span class="st pass">pass</span><div><strong>Query understood.</strong> detail</div></div>
```
fail: `<span class="st fail">check failed</span>`.

Quirks:
```html
<div class="quirk"><strong>Preambles (paragraph 0): 33 records</strong> — e.g. CEDAW/C/GC/…, preamble</div>
```

Method: `<ul>` of lines.

Header check status: `<span class="dot g"></span> 8 checks pass` or red.

Tab 04 red dot: `<span class="dot r" id="tab4dot" hidden></span>` inside tab button.

Now let me also double check the "clickable ≤7" for tab 02: 4 tabs + search box + filter heading + order select + show more = 8 (plan says 8, fine — plan's own count).

Rail on draft tab hidden — but then tabs+3 buttons = 7. Good.

Now, one concern: `normText` uses `\s+`→' ' which also collapses the fn-mark removal gaps — fine.

Another: termRe with lookbehind — Safari 16.4+ supports lookbehind. Assume modern.

Highlight regex with `giu` and alternation of many terms — fine.

Edge: query with only `NOT x` → tree = not(term). evalTree works. posTerms empty → hiRe null → no highlight; check 4 handles NOT-only.

Edge: query `""` empty phrase → error 'empty phrase'.

Edge: `-` alone: tokenizer: w='-' starts with '-' but length 1 → falls to else → term '-' → normText('-') = '-' → regex `(?<![\p{L}\p{N}])-(?![\p{L}\p{N}])` matches hyphens. OK.

Now, "A hyphen is a boundary, so 'state' finds 'non-State'": norm of "non-State" → "non-state"; regex for "state": `(?<![\p{L}\p{N}])state(?![\p{L}\p{N}])` — in "non-state", before 's' is '-', not letter → matches. 

Wildcard `child*` → `child\w*` with boundaries: "children" → 'child' + 'ren' matches `\w*`, after 'n' end → ok. But also "childhood" matches — expected for prefix search.

Now the "matches" order needs titleHits per run.

Let me now also compute initial quirks examples.

Also plan: "28 symbols are annual reports... 14 hold more than one General Comment" — quirks section covers shared symbols.

Write the method text.

Now, about the header source line: GC fields: title, source, count, records. source_url maybe absent. I'll do:
```js
const src = GC.source ? (GC.source_url ? `<a href="${esc(GC.source_url)}">${esc(GC.source)}</a>` : esc(GC.source)) : 'WORKSHOP_DATA.gc';
```

Footer: `${esc(GC.source||'WORKSHOP_DATA.gc')}${GC.built?' · built '+esc(GC.built):''} · Counting, matching and sorting are done by this page's code; no model is called.` and credits line: `Credits: Chart.js 4 (MIT licence) renders FIG.01.`

Now assemble everything. Also add `<noscript>` maybe. Keep under 1500 lines — should be ~700-900 lines.

Let me write the final code now, carefully.

Also remember: before code block, at most three short sentences describing what I built. After: nothing.

One more check on the tab labels: "01 OVERVIEW · 02 PARAGRAPHS · 03 DRAFT (n) · 04 CHECK & METHOD". Use "·" separators? The plan shows tabs as `01 OVERVIEW · 02 RECORDS · …` — the · is separator in the plan text; I'll just have tab labels "01 OVERVIEW" etc. Fine.

Draft tab label: `03 DRAFT <span id="dcount">(0)</span>`.

Let me write CSS fully, then HTML skeleton, then JS.

Also: focus ring visible red: `:focus-visible{outline:3px solid var(--red); outline-offset:2px}` global.

Buttons `.btn` and `.linkbtn`:
```css
.linkbtn{background:none;border:none;padding:0;color:#6b655a;text-decoration:underline;cursor:pointer;font:inherit;font-size:inherit}
.linkbtn:hover{color:var(--red)}
```

Search button:
```css
#searchbtn{padding:8px 14px;background:var(--ink);color:var(--paper);border:1px solid var(--ink);cursor:pointer;font:12px ui-monospace;letter-spacing:.1em}
#searchbtn:hover{background:var(--red);border-color:var(--red)}
```

Clear all:
```css
#clearall{background:none;border:none;color:#6b655a;text-decoration:underline;cursor:pointer;font:11px ui-monospace;letter-spacing:.08em}
#clearall:hover{color:var(--red)}
```

all/none small button similar.

Now the JS in full. Let me be careful about ordering: define helpers, precompute, build UI, wire events, initial run.

Potential issue: 7304 records × normText with several regex replaces — fine.

Also `state.hi` built per run from positive terms (global regex for highlight). Store also non-global for checks.

Let me write:

```js
function computeHits(){
  const tree=state.tree;
  let hits=[];
  for(const o of recs){
    if(!passes(o)) continue;
    if(tree && !evalTree(tree,o.norm)) continue;
    hits.push(o);
  }
  return hits;
}
```

Sort per order.

Now renderOverview chart:

```js
let chart=null;
function renderOverview(){
  const data=[...perComm.entries()].filter(([,v])=>v>0).sort((a,b)=>b[1]-a[1]);
  const labels=data.map(d=>d[0]), vals=data.map(d=>d[1]);
  const box=document.getElementById('chartbox');
  if(!data.length){ box.innerHTML='<p class="hint">No paragraphs match — no bars to draw.</p>'; table...; return; }
  ...
}
```

Hmm if I replace box innerHTML I lose canvas. Better: keep canvas always; if no data, hide chartbox and show message div. I'll have a sibling `<p id="nohits" hidden>`.

Chart creation once (lazy on first render when visible). If created while hidden (panel 0 is default visible — panel 0 is the initial tab, so visible at load). Good: initial tab is 01 OVERVIEW, so chart renders fine at load. On tab switches back, call chart.resize().

aria-label update: canvas.setAttribute('aria-label', 'Bar chart of paragraphs per committee: '+data.map(d=>d[0]+' '+d[1].toLocaleString('en-US')).join('; ')).

Table: rebuild tbody.

onClick: use chart.getElementsAtEventForMode(e.nativeEvent, 'nearest', {intersect:true}, true). In Chart.js 4, handler receives (event, elements, chart); event.nativeEvent. I'll use `(evt)=>{ const pts = chart.getElementsAtEventForMode(evt.nativeEvent||evt, 'nearest', {intersect:true}, true); ... }`.

tickAlone(code): state.ticked=new Set([code]); renderCommittees(); run();

Now run():

```js
function run(){
  state.hits = computeHits();
  // perComm
  perComm.clear();
  state.hits.forEach(o=>o.committees.forEach(c=>perComm.set(c,(perComm.get(c)||0)+1)));
  // titleHits for matches order
  titleHits.clear();
  state.hits.forEach(o=>titleHits.set(o.r.title,(titleHits.get(o.r.title)||0)+1));
  sortHits();
  state.shown = Math.min(state.shown, ...) // keep
  buildHi();
  renderRail(); renderChips(); renderCommittees(); renderOverview(); renderResults(); renderChecks(); renderHeaderStatus();
}
```

Wait — should run reset shown to 25 on new search? Yes, on doSearch set state.shown=25. On filter changes keep? Simpler: reset to 25 on any run triggered by search/filter change; "show more" only increases. I'll reset shown=25 inside doSearch and filter handlers, not in run(). Actually simplest: run(resetPage) param. I'll set state.shown=25 in doSearch and in each filter change handler before run().

Hmm, but committee checkbox changes call run() — reset shown there too. I'll just always reset shown=25 in run() except when called from "more" button. Add param run(fromMore).

sortHits:
```js
function sortHits(){
  const h=state.hits;
  if(state.order==='doc') h.sort((a,b)=> a.r.title.localeCompare(b.r.title) || a.r.paragraph-b.r.paragraph);
  else if(state.order==='matches') h.sort((a,b)=> (titleHits.get(b.r.title)||0)-(titleHits.get(a.r.title)||0) || b.r.year-a.r.year || a.r.title.localeCompare(b.r.title) || a.r.paragraph-b.r.paragraph);
  else h.sort((a,b)=> b.r.year-a.r.year || a.r.title.localeCompare(b.r.title) || a.r.paragraph-b.r.paragraph);
}
```

renderResults:
```js
function renderResults(){
  const hits=state.hits;
  const n=hits.length;
  const commSet=new Set(); hits.forEach(o=>o.committees.forEach(c=>commSet.add(c)));
  const years=hits.map(o=>o.r.year).filter(y=>typeof y==='number');
  const ymin=years.length?Math.min(...years):null, ymax=years.length?Math.max(...years):null;
  let s = n? `${fmt(n)} of ${fmt(R.length)} paragraphs match · ${commSet.size} committees · ${ymin}–${ymax}` : `0 of ${fmt(R.length)} paragraphs match`;
  if(!state.tree && !state.error) s += ' · no search words';
  summaryEl.textContent = s;
  orderhint.textContent = orderText[state.order];
  // rows
  resultsEl.innerHTML='';
  const frag=document.createDocumentFragment();
  const upto=Math.min(state.shown, n);
  for(let i=0;i<upto;i++) frag.appendChild(buildRow(hits[i]));
  resultsEl.appendChild(frag);
  moreBtn.hidden = upto>=n;
  moreBtn.textContent = 'Show 25 more ('+fmt(Math.min(25, n-upto))+' of '+fmt(n-upto)+' left)';
  // error display
  if(state.error){ qerr.textContent=state.error; echoEl.textContent=''; }
  else { qerr.textContent=''; echoEl.textContent = state.tree? echoLine() : 'no search words — every paragraph that passes the filters is listed'; }
}
```

Hmm echoLine: `Paragraphs containing ${echoTree(state.tree)}` or NOT-only special.

Wait — when error, hits=[] and summary "0 of ... match" — plus qerr shows message. Plan: "An unbalanced quote or parenthesis shows a message and no results." Good.

buildHi:
```js
function buildHi(){
  const pos=[]; if(state.tree) collectTerms(state.tree,false,pos);
  state.hi = pos.length? hiRe(pos,true) : null;
  state.hiTest = pos.length? hiRe(pos,false) : null;
}
```

hiRe(terms, global): flags = 'iu'+(global?'g':'').

renderRail: bignum.textContent=fmt(n); ofTotal = 'of '+fmt(R.length)+' paragraphs'; how line static.

renderChips:
```js
function renderChips(){
  const chips=[];
  if(state.ticked.size<allCodes.length) chips.push({k:'comm', label:'committees '+state.ticked.size+'/'+allCodes.length});
  if(state.yFrom>minYear||state.yTo<maxYear) chips.push({k:'years', label:'years '+state.yFrom+'–'+state.yTo});
  if(state.doc){ const d=docByTitle.get(state.doc); chips.push({k:'doc', label:'document: '+(d?d.short:state.doc)}); }
  chipsEl.innerHTML = chips.map(c=>`<button class="chip" data-chip="${c.k}" title="remove this filter">${esc(c.label)} ✕</button>`).join('');
}
chipsEl.onclick: remove filter: comm→ticked=new Set(allCodes); years→reset; doc→''; sync controls; run();
```

renderCommittees: rebuild list with counts from perComm (0 if none).

```js
committeesEl.innerHTML = allCodes.map(c=>`<label class="ck"><input type="checkbox" data-code="${c}"${state.ticked.has(c)?' checked':''}><span class="code">${c}</span><span class="nm">${esc(FULL[c]||c)}</span><span class="hits">[${fmt(perComm.get(c)||0)}]</span></label>`).join('');
```

change handler: delegation: on 'change' of input[data-code] → update ticked; run().

allnone button: if all ticked → uncheck all else check all; run(). Label "all / none".

Years: inputs #yfrom #yto; on change: read, clamp, set back, run().

Doc select change: state.doc=value; run().

fhead toggle.

doSearch:
```js
function doSearch(){
  const q=qInput.value;
  state.query=q;
  state.shown=25;
  if(!q.trim()){ state.tree=null; state.error=null; run(); return; }
  try{
    const {toks}=tokenize(q);
    state.tree=parse(toks);
    state.error=null;
  }catch(err){ state.tree=null; state.error=err.message||String(err); }
  run();
}
```

parse throws Error('unbalanced quote') etc.

renderChecks: as planned; also update header status and tab4 dot.

Header status:
```js
function renderHeaderStatus(){
  const cs=state.checks||[];
  const failed=cs.filter(c=>!c.ok).length;
  statusEl.innerHTML = failed? `<span class="dot r"></span>${failed} of ${cs.length} checks failed` : `<span class="dot g"></span>${cs.length} checks pass`;
  tab4dot.hidden = failed===0;
}
```

Checks panel render:
```js
checksEl.innerHTML = cs.map(c=>`<div class="check"><span class="st ${c.ok?'pass':'fail'}">${c.ok?'pass':'check failed'}</span><div><strong>${esc(c.name)}.</strong> ${esc(c.detail)}</div></div>`).join('');
```

Quirks render once at load.

Method render once.

Tabs:
```js
const tabs=[...document.querySelectorAll('.tabs [role=tab]')];
function selectTab(i){
  tabs.forEach((t,j)=>{ t.setAttribute('aria-selected', j===i?'true':'false'); });
  panels.forEach((p,j)=> p.hidden = j!==i);
  rail.hidden = (i===2);
  if(i===0 && chart) chart.resize();
}
tabs.forEach((t,i)=>{
  t.addEventListener('click',()=>selectTab(i));
  t.addEventListener('keydown',e=>{
    if(e.key==='ArrowRight'){ e.preventDefault(); const n=(i+1)%tabs.length; tabs[n].focus(); selectTab(n); }
    if(e.key==='ArrowLeft'){ e.preventDefault(); const n=(i-1+tabs.length)%tabs.length; tabs[n].focus(); selectTab(n); }
    if(e.key==='Home'){e.preventDefault(); tabs[0].focus(); selectTab(0);}
    if(e.key==='End'){e.preventDefault(); tabs[tabs.length-1].focus(); selectTab(tabs.length-1);}
  });
});
```

Draft render:
```js
function renderDraft(){
  dcount.textContent='('+state.draft.length+')';
  dn.textContent=state.draft.length;
  if(!state.draft.length){ draftList.innerHTML='<p class="hint">Nothing collected yet — open 02 PARAGRAPHS, click a row, then “Add to draft”.</p>'; return; }
  draftList.innerHTML = state.draft.map(it=>`<div class="ditem"><p class="dq">${esc(it.quotation)}</p><p class="dc">${esc(it.citation)}</p><button class="btn" data-rm="${esc(it.id)}">Remove</button></div>`).join('');
}
```

draftlist click delegation: remove → filter, save, renderDraft, live.

localStorage load:
```js
function loadDraft(){
  try{ const s=localStorage.getItem('verbatim-gc-draft'); if(s){ const a=JSON.parse(s); if(Array.isArray(a)) return a; } }catch(e){}
  return [];
}
let storeOK=true;
try{ localStorage.setItem('__vgc','1'); localStorage.removeItem('__vgc'); }catch(e){ storeOK=false; }
function saveDraft(){ if(!storeOK) return; try{ localStorage.setItem('verbatim-gc-draft', JSON.stringify(state.draft)); }catch(e){ storeOK=false; } }
```

Hint text: storeOK? 'Kept in localStorage when allowed, in memory otherwise.' — dynamic: storeOK? 'Kept in this browser’s localStorage.' : 'Kept in memory only (localStorage refused).' Plan says hint says where kept: localStorage when allowed, in memory otherwise. I'll set text accordingly.

Copy box:
```html
<div id="copybox" hidden>
  <div class="cbhead"><span>Clipboard refused — select and copy</span><button id="cbclose" class="linkbtn">close</button></div>
  <textarea id="cbtext" readonly></textarea>
</div>
```

copyText:
```js
async function copyText(t, label){
  let ok=false;
  try{ await navigator.clipboard.writeText(t); ok=true; }catch(e){ ok=false; }
  if(ok) live(label+' copied: '+t);
  else { cbtext.value=t; copybox.hidden=false; cbtext.focus(); cbtext.select(); live(label+': clipboard refused — the text is in the box below, select and copy it'); }
}
```

live: `liveEl.textContent=msg;` — to retrigger, could append '\u200B' alternating; skip.

Now tokenize/parse code with errors as Error objects.

Also note: query normalisation for terms uses normText which strips fn marks — irrelevant. But normText lowercases — echo uses raw. Good.

One more: the plan says the echo example: "Paragraphs containing the phrase “best interests” and the word child". My echoTree for and: `the phrase “best interests” and the word child` → line: `Paragraphs containing the phrase “best interests” and the word child`. 

NOT-only: root not → `Paragraphs without the word detention — a NOT-only query matches everything that lacks these terms`. Implement: if tree.t==='not' → special.

Now quirks computation:

```js
function computeQuirks(){
  const q=[];
  const p0=recs.filter(o=>o.r.paragraph===0);
  q.push({label:'Preambles cited as “preamble” (paragraph 0)', n:p0.length, ex:p0.length?p0[0].citation:''});
  const sharedSyms=[...symbolTitles.entries()].filter(([,s])=>s.size>1);
  q.push({label:'Symbols shared by more than one General Comment', n:sharedSyms.length, ex: sharedSyms.length? sharedSyms[0][0]+' ('+sharedSyms[0][1].size+' titles)' : ''});
  const joint=recs.filter(o=>o.joint);
  q.push({label:'Joint General Comments (two symbols in one record)', n:joint.length, ex: joint.length? joint[0].citation:''});
  const dupGroups=[...dupPin.entries()].filter(([,c])=>c>1);
  q.push({label:'Duplicated pinpoints (same document and paragraph)', n:dupGroups.length, ex: dupGroups.length? dupGroups[0][0].replace('|',', '):''});
  const mism=recs.filter(o=>o.leading!==null && o.leading!==o.r.paragraph);
  q.push({label:'Leading number differs from the paragraph field', n:mism.length, ex: mism.length? mism[0].citation+' (text begins '+mism[0].leading+'.):''});
  return q;
}
```

Render quirks list.

Method lines:
```html
<ul class="method">
<li><strong>Load.</strong> For each of the N records the page computes once: the normalised text, the number of footnote marks, the leading number, the pinpoint, the citation and the committee codes.</li>
<li><strong>Normalisation.</strong> Footnote marks <code>[[fn:N]]</code> are removed; curly and straight quotes, apostrophes, dashes and hyphens are unified; all whitespace becomes one space; text is lower-cased. The query is normalised the same way, so curly quotes pasted from Word still match.</li>
<li><strong>Query.</strong> Tokens: “phrases”, ( ), AND OR NOT in capitals, a leading − as NOT, words with an optional trailing *. Adjacent terms are AND; precedence NOT, then AND, then OR; parentheses override. The parser returns a tree and an English echo, or an error.</li>
<li><strong>Matching.</strong> Each term is a whole-word regular expression over the normalised text (a trailing * allows any ending; a hyphen counts as a boundary, so state finds non-State). A record matches when the tree is true. Counting, filtering, sorting and highlighting are done by this page's code — deterministic, never estimated.</li>
<li><strong>Citation and quotation.</strong> Built only from the record's fields: symbol, paragraph, committee, title. Shared symbols get the committee and document name first. Preambles are “preamble”, lettered records “subpara. (b)”. No symbol, paragraph or URL is ever invented; no model is called and nothing leaves the browser.</li>
</ul>
```

Now, the header dataline: also include source link. 

Let me now also handle `esc()`:
```js
function esc(s){ return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;'); }
```

highlightHTML as planned using state.hi (global). Reset lastIndex each call.

Now — the "matches" order select options:
```html
<select id="order">
  <option value="year">year, newest first</option>
  <option value="doc">document order</option>
  <option value="matches">most matches first</option>
</select>
```

OK. Also the summary includes order text separately in #orderhint.

Now sizes: fine.

Let me also make sure the rail is sticky but page scrolls — fine.

Edge: `state.shown` initial 25.

"Show 25 more" click: state.shown+=25; renderResults(); (no full run needed — but checks reference hits; fine).

Actually renderResults uses state.hi — set. OK.

Now write everything out. I'll aim for clean, complete code.

One more detail — the plan wants the search input labelled; label for="q" text "SEARCH THE PARAGRAPHS". And "Search" button. Enter key: keydown on qInput if Enter → doSearch.

Syntax list show/hide:
```js
qInput.addEventListener('focus', ()=>{ if(!qInput.value) syntaxEl.hidden=false; });
qInput.addEventListener('blur', ()=>{ syntaxEl.hidden=true; });
qInput.addEventListener('input', ()=>{ syntaxEl.hidden = qInput.value.length>0 ? true : syntaxEl.hidden && false; });
```
Hmm: "it closes when typing starts" — on input with value → hide. If cleared while focused → show again? "While the box is empty and has focus" — yes show. Implement:
```js
qInput.addEventListener('input', ()=>{ syntaxEl.hidden = !(document.activeElement===qInput && !qInput.value); });
```
And ArrowDown on qInput → focus first .ex button.

Example buttons: class ex, data-q. Click → qInput.value=btn.dataset.q; doSearch(); (syntax hides via input? programmatic value doesn't fire input; call syntaxEl.hidden=true).

Now the checks: "Query understood" detail includes echo + term count. echoLine():
```js
function echoLine(){
  if(!state.tree) return 'no search words';
  if(state.tree.t==='not') return 'Paragraphs without '+echoTree(state.tree.a)+' — a NOT-only query matches everything that lacks these terms';
  return 'Paragraphs containing '+echoTree(state.tree);
}
```

Check 1 detail: `${countTerms(state.tree)} term(s) — ${echoLine()}`.

Normalisation check detail: compute:
```js
const q=state.query;
const straightChars = ['"',"'",'-'].filter(c=>q.includes(c));
if(straightChars.length){
  let onlyVariant=0;
  for(const o of hits){
    const t=o.r.text;
    let hasStraight=false, hasVariant=false;
    for(const c of straightChars){
      if(t.includes(c)) hasStraight=true;
      if(c==='"'&&/[“”„]/.test(t)) hasVariant=true;
      if(c==="'"&&/[‘’‚]/.test(t)) hasVariant=true;
      if(c==='-'&&/[\u2010-\u2015\u00AD]/.test(t)) hasVariant=true;
    }
    if(hasVariant && !hasStraight) onlyVariant++;
  }
  detail = `the query contains straight ${...}; curly and dash forms were matched too — ${onlyVariant} of ${hits.length} hits contain only the curly/dash forms`;
  ok=true;
} else { detail='the query contains no straight quote, apostrophe or hyphen'; ok=true; }
```

Fine.

Highlight check: use state.hiTest (non-global). bad = hits.filter(o=>!state.hiTest || !state.hiTest.test(o.shown)). If posTerms empty (NOT-only) → ok true, detail 'NOT-only query: no terms to highlight'. Else ok = bad===0, detail lists up to 5 citations + count.

Note: hiTest with 'iu' flags; test on shown (original case) — good.

Marks check as planned.

Draft check as planned.

Totals & chart checks as planned.

Now — one thing: perComm is module-level Map; renderChecks uses it. Fine.

Also the plan: "the checkboxes' bracketed counts sum to the hits plus joint hits" — that's check 2. Good.

Let me now also handle `docByTitle` map for chip label.

Write final HTML now. I'll write it in one go, being careful with template literals inside the script (no nested backtick issues).

Also careful: inside the HTML `<script>`, avoid `</script>` sequences in strings — none.

Also the `[[fn:N]]` regex in JS: `/\[\[fn:\d+\]\]/g` — fine.

Let me draft the complete file mentally and write it.

Regarding the chart value labels plugin and Chart.js v4 API: `plugins: [{id:'vals', afterDatasetsDraw(chart){...}}]` inline in config `plugins` array. Good.

Ticks font: Chart.js v4: `scales.y.ticks.font`. Colors: `ticks.color`. Grid: `grid.color`. Border: `border.color` (v4 uses `border` not `grid` for axis line). OK.

Also `maintainAspectRatio:false` with container height set.

For the table beside chart: two columns Committee / Paragraphs.

Now, the layout: rail 300px + main. On narrow screens, flex-wrap. Add media query: `@media (max-width:900px){ .layout{flex-direction:column} .rail{width:100%;flex:none;position:static} }`.

Alright — also the "How this is computed" under big number and near chart.

Time to write the answer. Before the code block: 2-3 short sentences. Then the single html block. Nothing after.

Let me write the code.

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Verbatim finder · UN General Comments</title>
<style>
:root{
  --paper:#f4f0e8; --ink:#1d1b18; --rule:#d9d2c3; --red:#9b2335;
  --amber:#8a5a00; --green:#1e6b3a; --mark:#f3e6a2; --mut:#6b655a; --soft:#8a8578;
}
*{box-sizing:border-box}
[hidden]{display:none!important}
html{margin:0}
body{
  margin:0 auto; max-width:1180px; padding:0 22px 46px;
  background:var(--paper); color:var(--ink);
  font:16px/1.55 -apple-system,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif;
}
:focus-visible{outline:3px solid var(--red); outline-offset:2px}
a{color:var(--ink)}
button{font-family:inherit}
...
```

I'll write it all now in the final answer. Let me make sure every id referenced in JS exists.

IDs: dataline, srcline, checkstatus, tabs (class), tab4dot, rail, bignum, oftotal, chips, q, searchbtn, syntax, echo, qerr, fhead, fbody, committees, allnone, yfrom, yto, docsel, clearall, panel-0..3, fig1, chartbox, nohits, figtable (tbody figtbody), summary, order, orderhint, results, more, dcount, dn, draftlist, copyall, dltxt, dlcsv, storehint, checks, quirks, method, live, copybox, cbtext, cbclose.

Panels: I'll query `.panel`.

Let me write the JS fully:

```js
(function(){
'use strict';
var GC = window.WORKSHOP_DATA.gc;
var R = GC.records;
var FN = /\[\[fn:\d+\]\]/g;
var esc = function(s){ return String(s==null?'':s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;'); };
var fmt = function(n){ return Number(n).toLocaleString('en-US'); };
function normText(s){
  return String(s).replace(FN,'')
    .replace(/[\u201C\u201D\u201E]/g,'"')
    .replace(/[\u2018\u2019\u201A]/g,"'")
    .replace(/[\u2010-\u2015\u00AD]/g,'-')
    .replace(/\s+/g,' ')
    .toLowerCase().trim();
}
function escRe(s){ return s.replace(/[.*+?^${}()|[\]\\]/g,'\\$&'); }
```

Note: using \u escapes avoids literal curly chars in source (safer). But the syntax help text includes curly quotes as literal text in HTML — fine.

termRe:
```js
function termRe(text){
  var words = text.split(/\s+/).filter(Boolean).map(function(w){
    var wc = w.charAt(w.length-1)==='*';
    var core = wc ? w.slice(0,-1) : w;
    return escRe(core) + (wc ? '\\w*' : '');
  });
  return new RegExp('(?<![\\p{L}\\p{N}])' + words.join('\\s+') + '(?![\\p{L}\\p{N}])', 'u');
}
```

hiPat / hiRe:
```js
function hiPat(text){
  var words = text.split(/\s+/).filter(Boolean).map(function(w){
    var wc = w.charAt(w.length-1)==='*';
    var core = wc ? w.slice(0,-1) : w;
    var p='';
    for(var i=0;i<core.length;i++){
      var ch=core.charAt(i);
      if(ch==='"') p+='["\u201C\u201D\u201E]';
      else if(ch==="'") p+="['\u2018\u2019\u201A]";
      else if(ch==='-') p+='[-\u2010-\u2015\u00AD]';
      else p+=escRe(ch);
    }
    return p + (wc?'\\w*':'');
  });
  return words.join('(?:\\s|\\[\\[fn:\\d+\\]\\])+');
}
function hiRe(terms, global){
  var body = terms.map(function(t){ return '(?<![\\p{L}\\p{N}])(?:'+hiPat(t.text)+')(?![\\p{L}\\p{N}])'; }).join('|');
  return new RegExp(body, 'iu'+(global?'g':''));
}
```

Tokenizer:
```js
function tokenize(q){
  var toks=[], i=0, n=q.length;
  while(i<n){
    var c=q.charAt(i);
    if(/\s/.test(c)){ i++; continue; }
    if(c==='('||c===')'){ toks.push({k:c}); i++; continue; }
    if(c==='"'||c==='\u201C'||c==='\u201D'||c==='\u201E'){
      var j=i+1, buf='';
      while(j<n && q.charAt(j)!=='"' && q.charAt(j)!=='\u201D'){ buf+=q.charAt(j); j++; }
      if(j>=n) throw new Error('unbalanced quote — a phrase needs a closing double quote');
      toks.push({k:'term', text:buf, phrase:true}); i=j+1; continue;
    }
    var j2=i;
    while(j2<n && !/[\s()"'\u201C\u201D\u201E]/.test(q.charAt(j2))) j2++;
    var w=q.slice(i,j2);
    if(w==='AND') toks.push({k:'AND'});
    else if(w==='OR') toks.push({k:'OR'});
    else if(w==='NOT') toks.push({k:'NOT'});
    else if(w.charAt(0)==='-' && w.length>1) toks.push({k:'NOT'},{k:'term',text:w.slice(1)});
    else toks.push({k:'term', text:w});
    i=j2;
  }
  return toks;
}
```

Wait — word chars: I excluded quotes from words, so a word like `don't` splits at the apostrophe: `don` + `'t`... `'t` starts with `'` which is not in my word-char exclusion? I excluded `"` and curly quotes but not apostrophe `'`. Let me include `'` (straight) in the delimiter set? If I exclude `'`, then `don't` → word `don`, then `'t` → starts with `'`... `'` is not quote-open in my tokenizer (only double quotes open phrases), so `'t` would be a word `'t` → normalised `'t` → regex with leading apostrophe class... messy. Better: allow apostrophe inside words (don't stays one word). So word delimiters: whitespace, parens, double quotes (straight+curly). Apostrophes stay in words. But then a phrase delimiter uses only double quotes — fine, matches plan ("an exact phrase" in double quotes).

So word loop: `while(j2<n && !/[\s()"\u201C\u201D\u201E]/.test(q.charAt(j2))) j2++;`

And `don't` → term text `don't` → norm → `don't` → regex `don't` with boundaries — in norm text "don't" appears as `don't` (apostrophe normalised to straight). Match works. Highlight: `don` + `['‘’‚]` + `t`. 

Parser:
```js
function parse(toks){
  var p=0;
  function peek(){ return toks[p]; }
  function parseOr(){
    var left=parseAnd();
    while(peek() && peek().k==='OR'){ p++; var r=parseAnd(); left={t:'or',a:left,b:r}; }
    return left;
  }
  function parseAnd(){
    var left=parseNot();
    while(peek() && (peek().k==='AND'||peek().k==='NOT'||peek().k==='term'||peek().k==='(')){
      if(peek().k==='AND') p++;
      var r=parseNot();
      left={t:'and',a:left,b:r};
    }
    return left;
  }
  function parseNot(){
    if(peek() && peek().k==='NOT'){ p++; return {t:'not', a:parseNot()}; }
    return parsePrim();
  }
  function parsePrim(){
    var tk=peek();
    if(!tk) throw new Error('unexpected end of query');
    if(tk.k==='('){ p++; var e=parseOr(); if(!peek()||peek().k!==')') throw new Error('unbalanced parenthesis'); p++; return e; }
    if(tk.k==='term'){ p++; return makeTerm(tk); }
    throw new Error('unexpected "'+tk.k+'"');
  }
  var tree=parseOr();
  if(p<toks.length) throw new Error('unexpected "'+toks[p].k+'"');
  return tree;
}
function makeTerm(tok){
  var raw=tok.text.replace(/\s+/g,' ').trim();
  var text=normText(tok.text);
  if(!text) throw new Error('empty phrase');
  return {t:'term', raw:raw, text:text, phrase:!!tok.phrase, re:termRe(text)};
}
```

evalTree, collectTerms, countTerms, echoTree as planned.

Precompute:
```js
var symbolTitles=new Map();
R.forEach(function(r){ var s=symbolTitles.get(r.symbol); if(!s){s=new Set(); symbolTitles.set(r.symbol,s);} s.add(r.title); });
var dupPin=new Map();
R.forEach(function(r){ var k=r.title+'|'+r.paragraph; dupPin.set(k,(dupPin.get(k)||0)+1); });
var FULL={ 'CAT':'Committee against Torture', 'CAT-OP':'Subcommittee on Prevention of Torture (SPT)', 'CCPR':'Human Rights Committee', 'CED':'Committee on Enforced Disappearances', 'CEDAW':'Committee on the Elimination of Discrimination against Women', 'CERD':'Committee on the Elimination of Racial Discrimination', 'CESCR':'Committee on Economic, Social and Cultural Rights', 'CMW':'Committee on Migrant Workers', 'CRC':'Committee on the Rights of the Child', 'CRPD':'Committee on the Rights of Persons with Disabilities' };
var SYMRE=/\b(CAT|CCPR|CED|CEDAW|CERD|CESCR|CMW|CRC|CRPD)\b/g;
function docName(t){ var m=String(t).match(/^(.*?)(?::|\son\b)/); return (m?m[1]:t).trim(); }
var recs=R.map(function(r){
  var shown=String(r.text).replace(FN,'');
  var marks=(String(r.text).match(FN)||[]).length;
  var norm=normText(r.text);
  var lm=String(r.text).match(/^(\d{1,3})\.\s/);
  var leading=lm?parseInt(lm[1],10):null;
  var sm=String(r.text).match(/^\(([a-z]{1,4})\)/);
  var pinpoint = sm ? 'subpara. ('+sm[1]+')' : (Number(r.paragraph)===0 ? 'preamble' : 'para. '+r.paragraph);
  var codes=new Set();
  var found=String(r.symbol).match(SYMRE)||[];
  found.forEach(function(c){codes.add(c);});
  if(/CAT\/OP/.test(r.symbol)) codes.add('CAT-OP');
  if(r.committee) codes.add(r.committee);
  var committees=Array.from(codes);
  var o={ r:r, shown:shown, marks:marks, norm:norm, leading:leading, sub:sm?sm[1]:null,
    pinpoint:pinpoint, committees:committees, joint:found.length>1, shared:symbolTitles.get(r.symbol).size>1 };
  o.citation = o.shared ? (r.committee+', '+docName(r.title)+' ('+r.symbol+'), '+pinpoint) : (r.symbol+', '+pinpoint);
  var c=shown;
  if(o.leading!==null && o.leading===Number(r.paragraph)) c=c.replace(/^\d{1,3}\.\s/,'');
  o.copied=c;
  o.quotation='\u201C'+c+'\u201D '+o.citation;
  return o;
});
var byId=new Map(recs.map(function(o){return [o.r.id,o];}));
var titleMap=new Map();
recs.forEach(function(o){ var a=titleMap.get(o.r.title); if(!a){a=[]; titleMap.set(o.r.title,a);} a.push(o); });
titleMap.forEach(function(a){ a.sort(function(x,y){ return x.r.paragraph-y.r.paragraph; }); });
```

Wait — `o.quotation` includes citation; but draft stores quotation (quoted text only) + citation separately. For the Copy quotation button I'll use o.quotation (text+citation). For draft item: quotation='\u201C'+o.copied+'\u201D', citation=o.citation. OK.

Committee codes list:
```js
var codeCounts=new Map();
recs.forEach(function(o){ o.committees.forEach(function(c){ codeCounts.set(c,(codeCounts.get(c)||0)+1); }); });
var allCodes=Array.from(codeCounts.keys()).sort(function(a,b){ return (codeCounts.get(b)-codeCounts.get(a)) || a.localeCompare(b); });
var minYear=Math.min.apply(null, R.map(function(r){return Number(r.year)||0;}));
var maxYear=Math.max.apply(null, R.map(function(r){return Number(r.year)||0;}));
var titles=new Set(R.map(function(r){return r.title;}));
```

docList:
```js
var docList=[], seenT={};
recs.forEach(function(o){ if(!seenT[o.r.title]){ seenT[o.r.title]=1; docList.push({title:o.r.title, committee:o.r.committee||'', short:o.r.short_title||o.r.title, year:o.r.year}); } });
docList.sort(function(a,b){ return a.committee.localeCompare(b.committee) || String(a.short).localeCompare(String(b.short)); });
var docByTitle=new Map(docList.map(function(d){return [d.title,d];}));
```

State + storage + elements. Then UI build. Then run.

Now writing renderResults etc. Also note the initial call: build UI, then run().

Also — the plan wants the search input to have focus on load; do `qInput.focus()` at end (after everything). This triggers focus handler showing syntax (empty). Good.

Potential issue: `Math.min.apply(null, arrayOf7304)` fine.

Now checks function:

```js
function runChecks(){
  var hits=state.hits, cs=[];
  // 1
  if(state.error) cs.push({name:'Query understood', ok:false, detail:'parse error — '+state.error+'. No results are shown.'});
  else if(!state.tree) cs.push({name:'Query understood', ok:true, detail:'no search words — the empty query matches every paragraph that passes the filters'});
  else cs.push({name:'Query understood', ok:true, detail: countTerms(state.tree)+' term(s) — '+echoLine()});
  // 2 totals
  var jointHits=hits.filter(function(o){return o.committees.length>1;}).length;
  var sum=0; perComm.forEach(function(v){sum+=v;});
  cs.push({name:'Totals', ok: sum===hits.length+jointHits, detail:'rows listed across all pages = '+fmt(hits.length)+' hits; the committees\u2019 bracketed counts sum to '+fmt(sum)+' = '+fmt(hits.length)+' hits + '+fmt(jointHits)+' joint hits'});
  // 3 chart
  cs.push({name:'Chart total (FIG.01)', ok: sum===hits.length+jointHits, detail:'the bars sum to '+fmt(sum)+'; hits '+fmt(hits.length)+' + joint hits '+fmt(jointHits)});
  // 4 highlight
  var pos=[]; if(state.tree) collectTerms(state.tree,false,pos);
  if(!pos.length) cs.push({name:'Highlight', ok:true, detail:'NOT-only query — no terms to highlight'});
  else {
    var bad=hits.filter(function(o){ state.hiTest.lastIndex=0; return !state.hiTest.test(o.shown); });
    cs.push({name:'Highlight', ok:bad.length===0, detail: bad.length===0 ? 'every one of the '+fmt(hits.length)+' hits shows at least one <mark>' : fmt(bad.length)+' hit(s) matched in the normalised text but show no highlight: '+bad.slice(0,5).map(function(o){return o.citation;}).join('; ')});
  }
  // 5 normalisation
  ...
  // 6 numbering
  var mism=hits.filter(function(o){return o.leading!==null && o.leading!==Number(o.r.paragraph);});
  var subs=hits.filter(function(o){return !!o.sub;});
  var dups=hits.filter(function(o){return dupPin.get(o.r.title+'|'+o.r.paragraph)>1;});
  cs.push({name:'Numbering', ok:true, detail: fmt(mism.length)+' leading-number mismatch(es) ('+(mism.slice(0,3).map(function(o){return o.citation+' — text begins '+o.leading+'.';}).join('; ')||'none')+'); '+fmt(dups.length)+' shared pinpoint(s); '+fmt(subs.length)+' lettered sub-paragraph(s) — each is flagged on its row'});
  // 7 marks
  var mbad=0;
  hits.forEach(function(o){ var c=(String(o.r.text).match(/\[\[fn:/g)||[]).length; if(c!==o.marks || String(o.r.text).replace(FN,'')!==o.shown) mbad++; });
  cs.push({name:'Footnote marks', ok:mbad===0, detail:'for '+fmt(hits.length)+' hits, the marks removed equal the count of [[fn: in the stored text, and removing them reproduces the shown text exactly'+(mbad?'; '+mbad+' mismatch(es)':'')});
  // 8 draft
  var dbad=state.draft.filter(function(it){ var o=byId.get(it.id); return !o || o.r.text!==it.text_as_stored; });
  cs.push({name:'Draft', ok:dbad.length===0, detail: fmt(state.draft.length)+' draft item(s) re-checked against the stored text of their record'+(dbad.length?'; '+dbad.length+' differ(s)':'')});
  state.checks=cs;
  renderChecks(); renderHeaderStatus();
}
```

Note: detail strings contain `<mark>` — I escape details when rendering... then `<mark>` would show literally. I'll not escape detail, or escape but write "mark" without brackets. I'll write 'at least one highlighted match' instead. Keep details plain text, escape on render.

renderChecks builds HTML with esc(detail).

OK. Now the overview render:

```js
var chart=null;
function renderOverview(){
  var data=Array.from(perComm.entries()).filter(function(e){return e[1]>0;}).sort(function(a,b){return b[1]-a[1];});
  var labels=data.map(function(e){return e[0];}), vals=data.map(function(e){return e[1];});
  var box=document.getElementById('chartbox');
  if(!data.length){
    box.hidden=true; document.getElementById('nohits').hidden=false;
    document.getElementById('figtbody').innerHTML='';
    return;
  }
  box.hidden=false; document.getElementById('nohits').hidden=true;
  box.style.height=Math.max(180, labels.length*30+70)+'px';
  var aria='Bar chart, paragraphs per committee: '+data.map(function(e){return e[0]+' '+fmt(e[1]);}).join('; ');
  var cv=document.getElementById('fig1');
  cv.setAttribute('aria-label', aria);
  if(!chart){
    chart=new Chart(cv.getContext('2d'), {
      type:'bar',
      data:{labels:labels, datasets:[{data:vals, backgroundColor:'#9b2335', borderWidth:0, barPercentage:0.85, categoryPercentage:0.9}]},
      options:{
        indexAxis:'y', responsive:true, maintainAspectRatio:false,
        onClick:function(evt){
          var pts=chart.getElementsAtEventForMode(evt.nativeEvent||evt,'nearest',{intersect:true},true);
          if(pts && pts.length){ tickAlone(chart.data.labels[pts[0].index]); }
        },
        scales:{
          x:{beginAtZero:true, border:{color:'#d9d2c3'}, grid:{color:'#e4ddcd'}, ticks:{color:'#1d1b18', maxTicksLimit:10, precision:0, font:{family:'ui-monospace, Menlo, Consolas, monospace', size:11}}},
          y:{grid:{display:false}, border:{display:false}, ticks:{color:'#1d1b18', font:{family:'ui-monospace, Menlo, Consolas, monospace', size:11}}}
        },
        plugins:{legend:{display:false}, tooltip:{callbacks:{label:function(c){return ' '+fmt(c.parsed.x)+' paragraphs';}}}}
      },
      plugins:[{id:'vals', afterDatasetsDraw:function(ch){
        var meta=ch.getDatasetMeta(0), x=ch.scales.x, ctx=ch.ctx;
        ctx.save(); ctx.fillStyle='#1d1b18'; ctx.font='12px ui-monospace, Menlo, Consolas, monospace'; ctx.textAlign='left'; ctx.textBaseline='middle';
        meta.data.forEach(function(bar,i){ ctx.fillText(fmt(ch.data.datasets[0].data[i]), bar.x+6, bar.y); });
        ctx.restore();
      }}]
    });
  } else {
    chart.data.labels=labels; chart.data.datasets[0].data=vals; chart.update();
  }
  document.getElementById('figtbody').innerHTML=data.map(function(e){return '<tr><th scope="row">'+esc(e[0])+'</th><td class="num">'+fmt(e[1])+'</td></tr>';}).join('');
}
```

tickAlone:
```js
function tickAlone(code){ state.ticked=new Set([code]); renderCommittees(); run(); }
```

renderCommittees:
```js
function renderCommittees(){
  document.getElementById('committees').innerHTML=allCodes.map(function(c){
    return '<label class="ck"><input type="checkbox" data-code="'+esc(c)+'"'+(state.ticked.has(c)?' checked':'')+'><span class="code">'+esc(c)+'</span><span class="nm">'+esc(FULL[c]||c)+'</span><span class="hits">['+fmt(perComm.get(c)||0)+']</span></label>';
  }).join('');
}
```

committees change delegation:
```js
document.getElementById('committees').addEventListener('change', function(e){
  var inp=e.target.closest('input[data-code]'); if(!inp) return;
  if(inp.checked) state.ticked.add(inp.dataset.code); else state.ticked.delete(inp.dataset.code);
  state.shown=25; run();
});
```

allnone:
```js
allnoneBtn.onclick=function(){
  if(state.ticked.size===allCodes.length) state.ticked=new Set(); else state.ticked=new Set(allCodes);
  renderCommittees(); state.shown=25; run();
};
```

Years:
```js
function syncYears(){ yfrom.value=state.yFrom; yto.value=state.yTo; }
yfrom.addEventListener('change', function(){ var v=parseInt(yfrom.value,10); if(isNaN(v)) v=minYear; v=Math.max(minYear,Math.min(maxYear,v)); state.yFrom=Math.min(v,state.yTo); syncYears(); state.shown=25; run(); });
yto similar with state.yTo=Math.max(v,state.yFrom).
```

Doc select build:
```js
function buildDocSelect(){
  var html='<option value="">all documents ('+docList.length+')</option>';
  var cur=null;
  docList.forEach(function(d){
    if(d.committee!==cur){ if(cur!==null) html+='</optgroup>'; cur=d.committee; html+='<optgroup label="'+esc(cur)+' — '+esc(FULL[cur]||cur)+'">'; }
    html+='<option value="'+esc(d.title)+'">'+esc(d.short)+' ('+d.year+')</option>';
  });
  if(cur!==null) html+='</optgroup>';
  docsel.innerHTML=html;
}
```

docsel change: state.doc=docsel.value; state.shown=25; run().

Chips:
```js
function renderChips(){
  var chips=[];
  if(state.ticked.size<allCodes.length) chips.push({k:'comm', label:'committees '+state.ticked.size+'/'+allCodes.length});
  if(state.yFrom>minYear||state.yTo<maxYear) chips.push({k:'years', label:'years '+state.yFrom+'\u2013'+state.yTo});
  if(state.doc){ var d=docByTitle.get(state.doc); chips.push({k:'doc', label:'document: '+(d?d.short:state.doc)}); }
  chipsEl.innerHTML=chips.map(function(c){ return '<button class="chip" data-chip="'+c.k+'" title="remove this filter">'+esc(c.label)+' \u2715</button>'; }).join('');
}
chipsEl.addEventListener('click', function(e){
  var b=e.target.closest('[data-chip]'); if(!b) return;
  var k=b.dataset.chip;
  if(k==='comm') state.ticked=new Set(allCodes);
  if(k==='years'){ state.yFrom=minYear; state.yTo=maxYear; syncYears(); }
  if(k==='doc'){ state.doc=''; docsel.value=''; }
  renderCommittees(); state.shown=25; run();
});
```

clearall:
```js
clearallBtn.onclick=function(){
  qInput.value=''; state.query=''; state.tree=null; state.error=null;
  state.ticked=new Set(allCodes); state.yFrom=minYear; state.yTo=maxYear; state.doc='';
  docsel.value=''; syncYears(); renderCommittees(); state.shown=25; run();
};
```

run():
```js
function run(){
  var hits=[];
  for(var i=0;i<recs.length;i++){
    var o=recs[i];
    if(!passes(o)) continue;
    if(state.tree && !evalTree(state.tree,o.norm)) continue;
    hits.push(o);
  }
  state.hits=hits;
  perComm.clear(); hits.forEach(function(o){ o.committees.forEach(function(c){ perComm.set(c,(perComm.get(c)||0)+1); }); });
  titleHits.clear(); hits.forEach(function(o){ titleHits.set(o.r.title,(titleHits.get(o.r.title)||0)+1); });
  sortHits();
  buildHi();
  renderRail(); renderChips(); renderOverview(); renderResults(); runChecks();
}
```

passes:
```js
function passes(o){
  var okC=false;
  for(var i=0;i<o.committees.length;i++) if(state.ticked.has(o.committees[i])){ okC=true; break; }
  if(!okC) return false;
  var y=Number(o.r.year)||0;
  if(y<state.yFrom||y>state.yTo) return false;
  if(state.doc && o.r.title!==state.doc) return false;
  return true;
}
```

renderRail: bignum.textContent=fmt(state.hits.length); oftotal.textContent='of '+fmt(R.length)+' paragraphs';

renderResults as planned. buildRow etc.

detailHTML:
```js
function detailHTML(o,st){
  return '<div class="btns">'
    +'<button class="btn" data-action="cite">Copy citation</button>'
    +'<button class="btn" data-action="quote">Copy quotation</button>'
    +'<button class="btn primary" data-action="draft">Add to draft</button>'
    +'</div>'
    +'<div class="ctx">Context: <button class="linkbtn" data-action="ctxprev">previous</button> | <button class="linkbtn" data-action="ctxnext">next</button></div>'
    +'<div class="ctxblock"'+(st.ctx?'':' hidden')+'>'+(st.ctx?ctxHTML(o,st.ctx):'')+'</div>';
}
function ctxHTML(o,dir){
  var arr=titleMap.get(o.r.title)||[];
  var idx=-1;
  for(var i=0;i<arr.length;i++) if(arr[i].r.id===o.r.id) {idx=i; break;}
  var sib = dir==='prev' ? (idx>0?arr[idx-1]:null) : (idx>=0&&idx<arr.length-1?arr[idx+1]:null);
  if(!sib) return '<span class="hint">no '+(dir==='prev'?'previous':'next')+' paragraph in this document</span>';
  return '<span class="pin">'+esc(sib.pinpoint)+'</span> '+esc(sib.shown);
}
```

Hmm — context by array position (sorted by paragraph) is better than paragraph±1 (handles subparas). Good.

textHTML:
```js
function textHTML(o,st){
  var t = st.stored ? String(o.r.text) : o.shown;
  var html;
  if(st.full || t.length<=700) html=highlightHTML(t);
  else html=highlightHTML(cut700(t))+' \u2026 <button class="linkbtn" data-action="full">Show the full paragraph ('+fmt(wordCount(o.shown))+' words)</button>';
  return '<p class="rtext">'+html+'</p>';
}
function wordCount(t){ return t.split(/\s+/).filter(Boolean).length; }
function cut700(t){ var c=t.slice(0,700); var sp=c.lastIndexOf(' '); if(sp>350) c=c.slice(0,sp); return c; }
function highlightHTML(t){
  if(!state.hi) return esc(t);
  state.hi.lastIndex=0;
  var out='', last=0, m;
  while((m=state.hi.exec(t))){
    if(m[0].length===0){ state.hi.lastIndex++; continue; }
    out+=esc(t.slice(last,m.index))+'<mark>'+esc(m[0])+'</mark>';
    last=m.index+m[0].length;
  }
  out+=esc(t.slice(last));
  return out;
}
```

marksLineHTML, notesHTML as planned.

buildRow:
```js
function getRowState(id){ var s=state.rowState.get(id); if(!s){ s={open:false,full:false,stored:false,ctx:null}; state.rowState.set(id,s);} return s; }
function buildRow(o){
  var st=getRowState(o.r.id);
  var art=document.createElement('article'); art.className='row'; art.dataset.id=o.r.id;
  var h=document.createElement('h3'); h.className='rowh';
  var btn=document.createElement('button'); btn.className='rowhead'; btn.type='button';
  btn.setAttribute('aria-expanded', st.open?'true':'false');
  btn.innerHTML=metaHTML(o);
  h.appendChild(btn); art.appendChild(h);
  var body=document.createElement('div'); body.className='rbody';
  body.innerHTML=textHTML(o,st)+marksLineHTML(o,st)+notesHTML(o);
  art.appendChild(body);
  var det=document.createElement('div'); det.className='detail'; det.hidden=!st.open;
  det.innerHTML=detailHTML(o,st);
  art.appendChild(det);
  return art;
}
```

metaHTML:
```js
function metaHTML(o){
  var badges=o.committees.map(function(c){return '<span class="badge">'+esc(c)+'</span>';}).join(' ');
  return '<span class="meta">'+badges+' <span class="doc">'+esc(o.r.short_title)+'</span>'
    +' \u00B7 <span class="sym"><a href="'+esc(o.r.doc_url)+'" target="_blank" rel="noopener">'+esc(o.r.symbol)+'</a></span>'
    +' \u00B7 <span class="pin">'+esc(o.pinpoint)+'</span>'
    +' \u00B7 <span class="yr">'+esc(o.r.year)+'</span></span>';
}
```

Results delegation:
```js
resultsEl.addEventListener('click', function(e){
  if(e.target.closest('a')) return;
  var head=e.target.closest('.rowhead');
  var art=e.target.closest('.row');
  if(!art) return;
  var o=byId.get(art.dataset.id); if(!o) return;
  var st=getRowState(o.r.id);
  if(head){ st.open=!st.open; refreshRow(art,o,st); return; }
  var b=e.target.closest('[data-action]'); if(!b) return;
  var act=b.dataset.action;
  if(act==='cite') copyText(o.citation,'Citation');
  else if(act==='quote') copyText(o.quotation,'Quotation');
  else if(act==='draft') addToDraft(o);
  else if(act==='stored'){ st.stored=!st.stored; refreshRow(art,o,st); }
  else if(act==='full'){ st.full=true; refreshRow(art,o,st); }
  else if(act==='ctxprev'){ st.ctx = st.ctx==='prev'?null:'prev'; refreshRow(art,o,st); }
  else if(act==='ctxnext'){ st.ctx = st.ctx==='next'?null:'next'; refreshRow(art,o,st); }
});
function refreshRow(art,o,st){
  art.querySelector('.rowhead').setAttribute('aria-expanded', st.open?'true':'false');
  art.querySelector('.rbody').innerHTML=textHTML(o,st)+marksLineHTML(o,st)+notesHTML(o);
  var det=art.querySelector('.detail'); det.hidden=!st.open; det.innerHTML=detailHTML(o,st);
}
```

more button:
```js
moreBtn.addEventListener('click', function(){ state.shown+=25; renderResults(); });
```

renderResults:
```js
function renderResults(){
  var hits=state.hits, n=hits.length;
  var commSet=new Set(); hits.forEach(function(o){o.committees.forEach(function(c){commSet.add(c);});});
  var ys=hits.map(function(o){return Number(o.r.year)||0;});
  var s;
  if(n) s=fmt(n)+' of '+fmt(R.length)+' paragraphs match \u00B7 '+commSet.size+' committees \u00B7 '+Math.min.apply(null,ys)+'\u2013'+Math.max.apply(null,ys);
  else s='0 of '+fmt(R.length)+' paragraphs match';
  if(!state.tree && !state.error) s+=' \u00B7 no search words';
  summaryEl.textContent=s;
  orderhint.textContent=orderText[state.order];
  resultsEl.innerHTML='';
  var frag=document.createDocumentFragment();
  var upto=Math.min(state.shown,n);
  for(var i=0;i<upto;i++) frag.appendChild(buildRow(hits[i]));
  resultsEl.appendChild(frag);
  moreBtn.hidden = upto>=n;
  if(n>upto) moreBtn.textContent='Show 25 more ('+fmt(n-upto)+' left)';
  if(state.error){ qerr.textContent=state.error; echoEl.textContent=''; }
  else { qerr.textContent=''; echoEl.textContent = state.tree ? echoLine() : 'no search words \u2014 every paragraph that passes the filters is listed, paged'; }
}
```

orderText map:
```js
var orderText={ year:'sorted by year, newest first, then by document and paragraph', doc:'sorted by document, then paragraph', matches:'sorted by most matches first, then year, document and paragraph' };
```

Draft:
```js
function renderDraft(){
  dcount.textContent='('+state.draft.length+')';
  dn.textContent=state.draft.length;
  if(!state.draft.length){ draftList.innerHTML='<p class="hint">Nothing collected yet \u2014 on 02 PARAGRAPHS, click a row, then \u201CAdd to draft\u201D.</p>'; return; }
  draftList.innerHTML=state.draft.map(function(it){
    return '<div class="ditem"><p class="dq">'+esc(it.quotation)+'</p><p class="dc">'+esc(it.citation)+'</p><button class="btn" data-rm="'+esc(it.id)+'">Remove</button></div>';
  }).join('');
}
draftList.addEventListener('click', function(e){
  var b=e.target.closest('[data-rm]'); if(!b) return;
  state.draft=state.draft.filter(function(it){return it.id!==b.dataset.rm;});
  saveDraft(); renderDraft(); live('Removed from draft');
});
```

copyall/dltxt/dlcsv:
```js
function draftText(){ return state.draft.map(function(it){ return it.quotation+'\n'+it.citation; }).join('\n\n'); }
copyallBtn.onclick=function(){ copyText(draftText(),'Draft'); };
dltxtBtn.onclick=function(){ download('general-comments-draft.txt', draftText(), 'text/plain;charset=utf-8'); };
dlcsvBtn.onclick=function(){ download('general-comments-draft.csv', toCSV(), 'text/csv;charset=utf-8'); };
function download(name, content, type){
  var blob=new Blob([content],{type:type});
  var url=URL.createObjectURL(blob);
  var a=document.createElement('a'); a.href=url; a.download=name; document.body.appendChild(a); a.click();
  setTimeout(function(){ URL.revokeObjectURL(url); a.remove(); }, 500);
}
function toCSV(){
  var cols=['citation','symbol','paragraph','pinpoint','committee','short_title','year','text_copied','text_as_stored','doc_url'];
  function q(v){ return '"'+String(v==null?'':v).replace(/"/g,'""')+'"'; }
  var lines=[cols.map(q).join(',')];
  state.draft.forEach(function(it){ lines.push(cols.map(function(c){return q(it[c]);}).join(',')); });
  return '\uFEFF'+lines.join('\r\n');
}
```

addToDraft:
```js
function addToDraft(o){
  if(state.draft.some(function(it){return it.id===o.r.id;})){ live('Already in the draft: '+o.citation); return; }
  state.draft.push({ id:o.r.id, citation:o.citation, quotation:'\u201C'+o.copied+'\u201D', symbol:o.r.symbol, paragraph:o.r.paragraph, pinpoint:o.pinpoint, committee:o.r.committee, short_title:o.r.short_title, year:o.r.year, text_copied:o.copied, text_as_stored:o.r.text, doc_url:o.r.doc_url });
  saveDraft(); renderDraft(); live('Added to draft: '+o.citation);
}
```

copyText + live + copybox:
```js
var liveEl=document.getElementById('live');
function live(msg){ liveEl.textContent=msg; }
var copybox=..., cbtext=...;
async function copyText(t,label){
  var ok=false;
  try{ if(navigator.clipboard && navigator.clipboard.writeText){ await navigator.clipboard.writeText(t); ok=true; } }catch(e){ ok=false; }
  if(ok){ live(label+' copied: '+t); }
  else{ cbtext.value=t; copybox.hidden=false; cbtext.focus(); cbtext.select(); live(label+': the clipboard refused \u2014 the exact text is in the box at the bottom, select and copy it'); }
}
cbclose.onclick=function(){ copybox.hidden=true; };
```

Search wiring:
```js
qInput.addEventListener('keydown', function(e){
  if(e.key==='Enter'){ e.preventDefault(); doSearch(); }
  else if(e.key==='ArrowDown'){ var ex=syntaxEl.querySelector('.ex'); if(ex && !syntaxEl.hidden){ e.preventDefault(); ex.focus(); } }
});
qInput.addEventListener('focus', function(){ if(!qInput.value) syntaxEl.hidden=false; });
qInput.addEventListener('blur', function(){ syntaxEl.hidden=true; });
qInput.addEventListener('input', function(){ syntaxEl.hidden = !(document.activeElement===qInput && !qInput.value); });
searchbtn.addEventListener('click', doSearch);
syntaxEl.addEventListener('click', function(e){
  var b=e.target.closest('.ex'); if(!b) return;
  qInput.value=b.dataset.q; syntaxEl.hidden=true; doSearch();
});
```

doSearch:
```js
function doSearch(){
  var q=qInput.value;
  state.query=q; state.shown=25;
  if(!q.trim()){ state.tree=null; state.error=null; run(); return; }
  try{
    var toks=tokenize(q);
    state.tree=parse(toks); state.error=null;
  }catch(err){ state.tree=null; state.error=(err && err.message) ? err.message : String(err); }
  run();
}
```

fhead:
```js
fhead.addEventListener('click', function(){
  var open=fhead.getAttribute('aria-expanded')==='true';
  fhead.setAttribute('aria-expanded', open?'false':'true');
  fbody.hidden=open;
});
```

order:
```js
orderSel.addEventListener('change', function(){ state.order=orderSel.value; state.shown=25; run(); });
```

Tabs as planned.

Init:
```js
buildDocSelect(); syncYears(); renderCommittees(); renderDraft();
document.getElementById('dataline').textContent = fmt(R.length)+' paragraphs from '+titles.size+' General Comments (distinct title) of '+allCodes.length+' committees, '+minYear+'\u2013'+maxYear;
srcline.innerHTML = GC.source ? (GC.source_url ? '<a href="'+esc(GC.source_url)+'" target="_blank" rel="noopener">'+esc(GC.source)+'</a>' : esc(GC.source)) : 'WORKSHOP_DATA.gc';
renderQuirks(); renderMethod();
run();
qInput.focus();
```

renderQuirks / renderMethod fill static containers.

Header/footer text set in HTML directly with placeholders filled by JS (dataline, srcline). Footer static text + source: I'll fill via JS too: `footEl.innerHTML = esc(GC.source||'WORKSHOP_DATA.gc')+(GC.built?' \u00B7 built '+esc(GC.built):'')+' \u00B7 Counting, matching and sorting are done by this page\u2019s code; no model is called.';` plus credits line separate div: 'Credits: Chart.js 4 (MIT licence) renders FIG.01.'

Wait — footer should show source and built. GC may not have built; handle.

Also storehint: `storehint.textContent = storeOK ? 'Kept in this browser\u2019s localStorage.' : 'Kept in memory only \u2014 localStorage is not allowed here.';` plus plan wording "localStorage when allowed, in memory otherwise" — I'll write: 'Kept in localStorage when allowed, in memory otherwise — currently: '+(storeOK?'localStorage':'memory')+'.'

Now HTML body content. Let me write the syntax help:

```html
<div class="syntax" id="syntax" hidden>
  <div class="sline">a space or <b>AND</b> joins words &middot; <b>OR</b> &middot; <b>NOT</b> or a leading minus</div>
  <div class="sline"><b>"an exact phrase"</b> in double quotes</div>
  <div class="sline"><b>(</b> parentheses <b>)</b></div>
  <div class="sline">a star at the end of a word for any ending (<b>child*</b> finds children)</div>
  <div class="sline">operators in capitals; lower-case "or" is a word</div>
  <div class="sline exs">Try:
    <button type="button" class="ex" data-q="&quot;best interests&quot; AND child">"best interests" AND child</button>
    <button type="button" class="ex" data-q="(torture OR ill-treatment) NOT detention">(torture OR ill-treatment) NOT detention</button>
    <button type="button" class="ex" data-q="&quot;reasonable accommodation&quot;">"reasonable accommodation"</button>
  </div>
</div>
```

Note data-q with quotes — use &quot; in attribute. Good.

Overview panel:

```html
<section class="panel" role="tabpanel" id="panel-0" aria-labelledby="tab-0">
  <h2 class="figtitle"><span class="figno">FIG.01</span>Paragraphs per committee</h2>
  <p class="hint">click a bar = tick that committee alone</p>
  <div class="figwrap">
    <div class="chartbox" id="chartbox"><canvas id="fig1" role="img" aria-label="Bar chart of paragraphs per committee">Your browser cannot draw the chart; the table beside it lists the same numbers.</canvas></div>
    <p id="nohits" class="hint" hidden>No paragraphs match — no bars to draw.</p>
    <table class="figtable">
      <caption>Paragraphs per committee — the same numbers as FIG.01</caption>
      <thead><tr><th scope="col">Committee</th><th scope="col" class="num">Paragraphs</th></tr></thead>
      <tbody id="figtbody"></tbody>
    </table>
  </div>
  <p class="how">How this is computed: one count per committee over the paragraphs that match the query and filters. Joint General Comments count under both committees, so the bars can add up to more than the hits.</p>
</section>
```

Paragraphs panel:

```html
<section class="panel" role="tabpanel" id="panel-1" aria-labelledby="tab-1" hidden>
  <p class="summary" id="summary" aria-live="polite"></p>
  <div class="orderrow">
    <label for="order">Order</label>
    <select id="order">
      <option value="year">year, newest first</option>
      <option value="doc">document order</option>
      <option value="matches">most matches first</option>
    </select>
    <span class="hint" id="orderhint"></span>
  </div>
  <p class="hint">This page retrieves; it never writes. Every paragraph shown is a record of the file, as stored.</p>
  <div id="results"></div>
  <button id="more" class="btn" hidden>Show 25 more</button>
</section>
```

Draft panel:

```html
<section class="panel" role="tabpanel" id="panel-2" aria-labelledby="tab-2" hidden>
  <h2 class="ptitle">Your draft (<span id="dn">0</span> quotations)</h2>
  <p class="hint" id="storehint"></p>
  <div class="draftbtns">
    <button class="btn" id="copyall">Copy all</button>
    <button class="btn" id="dltxt">Download .txt</button>
    <button class="btn" id="dlcsv">Download .csv</button>
  </div>
  <div id="draftlist"></div>
</section>
```

Check panel:

```html
<section class="panel" role="tabpanel" id="panel-3" aria-labelledby="tab-3" hidden>
  <h2 class="ptitle">How the app checks itself</h2>
  <p class="hint">Run after every search, over the paragraphs that match. A failed check marks rows; it never drops them.</p>
  <div id="checks"></div>
  <h2 class="ptitle">Known quirks of this file</h2>
  <p class="hint">Computed once at load, before any search.</p>
  <div id="quirks"></div>
  <h2 class="ptitle">How this is computed</h2>
  <div id="method"></div>
</section>
```

Rail:

```html
<aside class="rail" id="rail" aria-label="Filters">
  <div class="railhead"><span>FILTERS</span><button id="clearall" type="button">Clear all</button></div>
  <div class="bignum" id="bignum" aria-live="polite">0</div>
  <div class="biglabel" id="oftotal"></div>
  <p class="how">How this is computed: records whose normalised text matches the query and that pass the filters below; counted by this page's code.</p>
  <div class="chips" id="chips"></div>
  <div class="searchbox">
    <label for="q">SEARCH THE PARAGRAPHS</label>
    <div class="qrow">
      <input id="q" type="text" autocomplete="off" spellcheck="false" placeholder='try "torture" NOT "death penalty"'>
      <button id="searchbtn" type="button">Search</button>
    </div>
    <div class="syntax" id="syntax" hidden>…</div>
    <p class="echo" id="echo" aria-live="polite"></p>
    <p class="err" id="qerr"></p>
    <p class="hint">Whole words, any case. Curly and straight quotes, apostrophes, dashes and hyphens count as the same, and footnote marks are skipped, so State's finds State\u2019s and a phrase can cross a footnote.</p>
  </div>
  <div class="filtersec">
    <button class="fhead" id="fhead" type="button" aria-expanded="false" aria-controls="fbody"><span class="fnum">01</span> COMMITTEE, YEARS, DOCUMENT <span class="chev">\u25BE</span></button>
    <div class="fbody" id="fbody" hidden>
      <div class="fgroup">
        <div class="flabel"><span>COMMITTEE</span><button id="allnone" type="button">all / none</button></div>
        <div id="committees"></div>
      </div>
      <div class="fgroup">
        <div class="flabel"><span>YEARS</span></div>
        <div class="yrow"><input id="yfrom" type="number" step="1"> <span>\u2013</span> <input id="yto" type="number" step="1"></div>
      </div>
      <div class="fgroup">
        <div class="flabel"><span>DOCUMENT</span></div>
        <select id="docsel"></select>
      </div>
    </div>
  </div>
</aside>
```

Note: in HTML I can write literal characters (–, ▾, ’) since charset utf-8. In JS strings I'll use \u escapes or literal — literal fine too. I'll use literals in HTML, and in JS mostly literals are fine (file is utf-8). I'll use literal curly quotes in JS strings where needed — safe.

Header:

```html
<header class="top">
  <div class="kicker">UN TREATY BODIES \u00B7 GENERAL COMMENTS</div>  → literal "UN TREATY BODIES · GENERAL COMMENTS"
  <h1>Verbatim finder: General Comments and General Recommendations</h1>
  <p class="dataline"><span id="dataline"></span> · <span id="srcline"></span></p>
  <div class="checkstatus" id="checkstatus"></div>
</header>
```

Tabs:

```html
<nav class="tabs" role="tablist" aria-label="Views">
  <button role="tab" id="tab-0" aria-controls="panel-0" aria-selected="true" type="button">01 OVERVIEW</button>
  <button role="tab" id="tab-1" aria-controls="panel-1" aria-selected="false" type="button" tabindex="-1">02 PARAGRAPHS</button>
  <button role="tab" id="tab-2" aria-controls="panel-2" aria-selected="false" type="button" tabindex="-1">03 DRAFT <span id="dcount">(0)</span></button>
  <button role="tab" id="tab-3" aria-controls="panel-3" aria-selected="false" type="button" tabindex="-1">04 CHECK &amp; METHOD <span class="dot r" id="tab4dot" hidden></span></button>
</nav>
```

Roving tabindex: manage in selectTab: set tabindex -1 on unselected, 0 on selected.

Footer:

```html
<footer>
  <span id="footline"></span>
  <span>Credits: Chart.js 4 (MIT licence) renders FIG.01.</span>
</footer>
<div id="live" class="sr" aria-live="polite"></div>
<div id="copybox" hidden>…</div>
```

.sr visually hidden but aria-live: 
```css
.sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}
```

OK. Also the "Copied" aria-live message — #live serves.

Now double-check clickable counts and plan compliance... good enough.

One more plan item: "the top-level count is the string '7304'" — I use R.length; fine.

"records.length is the count" — yes.

Also plan: header right "green dot and 'n checks pass'". Implemented.

Also: "A narrowed filter shows as a small removable chip under the big number." Done.

Also: "While the box is empty and has focus, a short list opens under it with the syntax... and three examples as options that fill and run". Done.

Also: "One line under the box: 'Whole words, any case...'". Done.

Also: "After a search, a line echoes the query as understood". Done.

Now — the check "Totals: Rows listed across pages equal the hits" — my check compares sum of committee counts; also could compare rendered rows... fine.

Potential runtime concern: runChecks does hits.forEach with regex match on text for marks check — for 7304 hits each with match(/\[\[fn:/g) — fine.

Highlight check: hiTest.test on each shown — fine.

Now, one subtle bug: `state.hi` global regex used in highlightHTML with lastIndex reset — ok. But `hiRe` alternation with many terms and `g` — exec loop fine.

Another: in `hiPat`, phrase gap `(?:\s|\[\[fn:\d+\]\])+` — in a character-class-free context fine.

Also `termRe` for phrase: words joined `\s+` — norm has single spaces. Good.

Edge: query term with `*` only (`*`) → core empty → pattern `\w*` with boundaries → matches any word. OK.

Now — the `passes` year check uses Number(o.r.year)||0; if year missing → 0 → filtered out when yFrom>0. Years min 1972 so fine.

Let me also handle `r.paragraph` possibly string: Number() coercions where comparing. In sortHits I use a.r.paragraph-b.r.paragraph — if strings, subtraction coerces. OK. dupPin key uses raw paragraph — consistent.

In pinpoint: 'para. '+r.paragraph — fine.

Now write renderQuirks:

```js
function renderQuirks(){
  var q=[];
  var p0=recs.filter(function(o){return Number(o.r.paragraph)===0;});
  q.push(['Preambles cited as \u201Cpreamble\u201D (paragraph 0)', p0.length, p0.length?p0[0].citation:'']);
  var shared=Array.from(symbolTitles.entries()).filter(function(e){return e[1].size>1;});
  q.push(['Symbols shared by more than one General Comment', shared.length, shared.length? shared[0][0]+' ('+shared[0][1].size+' titles)' : '']);
  var joint=recs.filter(function(o){return o.joint;});
  q.push(['Joint General Comments (two symbols in one record)', joint.length, joint.length?joint[0].citation:'']);
  var dups=Array.from(dupPin.entries()).filter(function(e){return e[1]>1;});
  q.push(['Duplicated pinpoints (same document and paragraph)', dups.length, dups.length? dups[0][0].replace('|',', ') : '']);
  var mism=recs.filter(function(o){return o.leading!==null && o.leading!==Number(o.r.paragraph);});
  q.push(['Leading number differs from the paragraph field', mism.length, mism.length? mism[0].citation+' (text begins '+mism[0].leading+'.)' : '']);
  document.getElementById('quirks').innerHTML=q.map(function(e){
    return '<div class="quirk"><strong>'+esc(e[0])+': '+e[1]+'</strong>'+(e[2]?'<br><span class="hint">e.g. '+esc(e[2])+'</span>':'')+'</div>';
  }).join('');
}
```

renderMethod: static HTML list.

Now, the checkstatus initial before first run — run() called at init so fine.

Also — plan wants tab 04 red dot when checks failed; done via tab4dot.

Also — "the count, the summary line and the 'Copied' message are aria-live" — bignum aria-live, summary aria-live, live aria-live. Done.

Now CSS for .rowh h3: margin 0, font-size inherit. `.rowhead` full width.

Let me also ensure `.rtext` uses pre-wrap and the mark styling.

Also `.ptitle` serif 22px.

Also `.summary` font-size 15px.

Also `.orderrow` flex gap.

Also `.draftbtns` flex gap margin.

Also `.quirk` padding border-bottom dotted.

Also `.method li` margin.

Also `.check .st` width.

Also `.ex` buttons styling: monospace small, underline, display inline.

Also `.syntax .sline` margin 3px 0.

Also `.err` red.

Also `.echo` min-height maybe.

Also `.chip` styling.

Also `.badge`.

Also `.num` right align.

Also `.chartbox` width 100%.

Also `.figwrap` flex.

Also media query.

Also `.top` position relative for checkstatus absolute right.

Also `.tabs` overflow-x auto for small screens.

I think I'm ready to write the final output. Length will be large but under 1500 lines.

One more consideration: the plan says results rows: "committee badge and short_title; symbol linked...; the pinpoint and year". Done in meta.

"Paragraphs up to 700 characters are shown whole; longer ones show the first 700 cut at a word, with 'Show the full paragraph (1,287 words)'" — done.

"white-space: pre-wrap keeps stored line breaks" — .rtext pre-wrap. Done.

"An amber note sits on the row when needed" — done.

"A click on a row opens it in place, with three buttons and a 'Context: previous | next' link." — done.

Copy citation note: "A grey note names the style, 'UN short form'." — add in detail: `<div class="hint">citation style: UN short form</div>`. Add.

Also "After every copy an aria-live message shows the exact string sent." — live() does.

Also the check panel "open" — it's a tab, fine.

Also plan: "03 DRAFT (4)" tab name carries count — dcount span.

Also: "Download .csv (… UTF-8 with byte-order mark, fields double-quoted)" — done.

Also: "A hint says where it is kept" — storehint.

Also: header one line with source, n and years — dataline.

Also: "Every row that shows a document has its symbol, linked to doc_url in a new tab." — done.

Now, about `studio.ask` — never called. Good. No external resources. Chart.js from window.Chart.

Also guard: `if(!window.Chart)` — skip chart creation, table still works. I'll wrap chart creation in try/catch and if fails, hide chartbox show table only. Simple: `if(window.Chart){...} else { box.hidden=true; }`.

Let me also double check the tokenizer handles `NOT` at start: `-child` → NOT term. `NOT child` → NOT then term. Good.

Query `child*` → term with text `child*` → termRe: wc, core `child` → `child\w*`. Good.

Query with lowercase `or` → word `or` → term. Good.

Now — one thing about `normText` on query terms: it removes `[[fn:...]]` — irrelevant; lowercases; maps dashes. But it also collapses whitespace — for phrase terms good.

Edge: phrase containing `*` inside, e.g. `"child* ren"` — words: `child*` → `child\w*`, `ren`. Fine.

Now write everything. Also remember: at most three short sentences before the code block.

Let me also decide the `.how` under bignum text: "How this is computed: records whose normalised text matches the query and that pass the filters below; counted by this page's code, never estimated."

Also add title attribute? skip.

Writing final code now. I'll be careful with quotes inside JS strings (use single quotes mostly, escape as needed).

For the echo of wildcard: `n.text.endsWith('*')` — text is normalised (lowercase) but `*` preserved. raw is original. echo: `the word child* (any ending)`.

echoTree:
```js
function echoTree(n){
  if(n.t==='term'){
    if(n.phrase) return 'the phrase \u201C'+n.raw+'\u201D';
    if(n.text.charAt(n.text.length-1)==='*') return 'the word '+n.raw+' (any ending)';
    return 'the word '+n.raw;
  }
  if(n.t==='not') return 'without '+echoTree(n.a);
  if(n.t==='and') return echoTree(n.a)+' and '+echoTree(n.b);
  return echoTree(n.a)+' or '+echoTree(n.b);
}
function echoLine(){
  if(!state.tree) return '';
  if(state.tree.t==='not') return 'Paragraphs without '+echoTree(state.tree.a)+' \u2014 a NOT-only query matches everything that lacks these terms';
  return 'Paragraphs containing '+echoTree(state.tree);
}
```

OK. Also countTerms.

Also — `collectTerms` for highlight: skip terms under NOT:
```js
function collectTerms(n, neg, out){
  if(n.t==='term'){ if(!neg) out.push(n); return; }
  if(n.t==='not'){ collectTerms(n.a, true, out); return; }
  collectTerms(n.a, neg, out); collectTerms(n.b, neg, out);
}
```

Now finalize. Also the initial `state.shown=25`.

Also `renderRail` sets bignum & oftotal.

Also — after run(), if current tab is 0 and chart exists, chart.update already called in renderOverview. Fine.

Also selectTab(0) calls chart.resize() — guard chart exists.

Write it.

Also small thing: `.tabs [role=tab]` need `tabindex` management: selected tab tabindex 0, others -1. In selectTab set.

Also panels array: `var panels=[0,1,2,3].map(i=>document.getElementById('panel-'+i));`

Also rail hidden on tab 2: `rail.hidden = (i===2);`

Let me now also make sure the copybox doesn't block: fine.

Final check on line count — probably ~850 lines. OK.

Write the response: 2-3 sentences + code block.