Let me understand the task. The user wants a tool that:

1. Takes `WORKSHOP_DATA.pdf_text` — raw PDF text page by page
2. Splits it into numbered paragraphs (1, 2, 3, ...)
3. Removes page headers and footers
4. Keeps footnotes out of paragraph text
5. Shows how many paragraphs found vs. the reference count (`reference.paragraphs`)
6. A table with each paragraph's number and first line
7. Mark paragraphs whose first words differ from `reference.first_words`
8. Clicking a row shows the full paragraph
9. Download result as CSV

Data available: `WORKSHOP_DATA.pdf_text` = `{title, symbol, doc_url, source, count, records: [{page, text}], reference: {paragraphs, footnotes, adopted, first_words: {"1": "first six words...", ...}}}`.

The sample shows page 1 of E/C.12/GC/27. The real data has 20 pages. I need to write a robust parser:

- Concatenate pages, but detect page headers/footers. Common patterns in UN documents:
  - Header: symbol line like "E/C.12/GC/27", "United Nations", "Economic and Social Council", "Distr.: General", date "6 November 2025", "Original: English"
  - Footer: page number alone on a line, e.g. "2", possibly with symbol like "E/C.12/GC/27  2" or "GE.25-XXXXX (E) 061125"
  
Since I can't see the real data, I need heuristic cleaning:
- Remove lines that are just a page number (digits only, maybe with surrounding whitespace)
- Remove lines matching the document symbol (e.g., starts with the symbol from pdf_text.symbol)
- Remove known header lines: "United Nations", "Economic and Social Council", "Distr.: ...", "Original: ...", date lines like "6 November 2025"
- Footnotes: lines starting with a number followed by a superscript-ish marker... In PDF text, footnotes often appear as "1 text..." at the bottom of the page. Hard to detect generically. Heuristic: footnote lines often start with a small number followed by space and text, and appear after the main text. A common approach: a line matching /^\s*(\d{1,2})\s+(.+)/ where the number is small and the line is at the end of a page... risky.

Better approach: paragraphs in these General Comments are numbered "N." at the start, possibly with the number on its own line (as in the sample: "1.\nA clean, healthy..."). So paragraph detection: find occurrences of /^\s*(\d{1,3})\.\s*$/m or /^\s*(\d{1,3})\.\s+/m at line starts. But footnotes also start with numbers... footnotes in UN PDFs are usually like "1 See ..." with the number possibly followed by a space, not a period. Actually in E/C.12/GC/27 footnotes look like "1 Office of the United Nations High Commissioner..." Hmm, they might have a period? Typically UN footnotes: "1 OHCHR, ..." — number, space, text. Paragraph numbers: "1." with a period. So regex /^\s*(\d{1,3})\.\s/m distinguishes them. But some paragraphs might be "12. The Committee..." on one line. Handle both.

Also footnote markers in text are superscript numbers — in extracted text they may appear inline like "...sustainable development*". The sample shows "sustainable development*" with an asterisk. So footnotes may use asterisk or superscript digits. The reference says `footnotes` count. I should count footnotes found and show next to reference.footnotes too? The user asked: "Show how many paragraphs it found next to the number the document really has" — that's paragraphs. But also "keep the footnotes out of the paragraph text" — I can also show footnote count vs reference as a bonus. The reference has `footnotes` count, so showing "footnotes found: X (reference: Y)" is good honesty.

Footnote detection heuristic: lines at the end of a page that start with /^\s*\d{1,2}\s/ (number + space, no period) — but that could catch list items. In GC documents, footnotes appear after the main body text on the page where the marker occurs, often separated. A safer heuristic: a footnote line starts with a number 1-99 followed by whitespace and then text, AND the number is greater than... hmm. Actually in the sample page 1, the footnote marker is "*" — "sustainable development*". So footnotes might be asterisked. The extracted text may render footnote text at page bottom like "* text..." or "1 text...".

Given uncertainty, I'll implement:
- Split into lines per page.
- Classify lines:
  - Page-number-only lines: /^\s*\d{1,4}\s*$/ → footer (but careful: a paragraph number on its own line "1." has a period, so safe).
  - Symbol lines: line contains pdf_text.symbol → header/footer.
  - "United Nations", "Economic and Social Council", "General Assembly", etc. — generic UN header lines: /^(United Nations|Economic and Social Council|General Assembly|Human Rights Council|Security Council|Secretariat)$/i
  - Distr./Original lines: /^(Distr\.?|Original)\s*:/i
  - Date lines: /^\d{1,2} (January|...|December) \d{4}$/i
  - Footnote lines: /^\s*(\d{1,2}|[*†‡§])\s+\S/ at... hmm, risky. Let me think: footnote lines typically appear at the bottom of the page after the body. But without page-position info beyond line order, I can use: a line matching /^\s*\d{1,2}\s+[A-Z]/ that is NOT a paragraph start (no period after number) — in UN GC documents, body text rarely has lines starting with "12 Something" without a period... Actually it could in lists like "1. " no. Roman numeral lists? Possibly "(a) ...". I'll treat lines matching /^\s*(\d{1,2})\s{1,3}(\S.*)$/ where the captured number ≤ 99 as footnote candidates ONLY if they occur after the last paragraph-start on that page? That's too clever. 

Alternative: footnotes in these converted PDFs often appear as separate lines starting with the footnote number followed by a period? No — UN style: footnote number then space. Hmm, but actually many UN PDFs render footnotes as "1 Text" where "1" is superscript. The converter output keeps "1 Text".

Let me be pragmatic: I'll detect footnote lines as lines matching /^\s*(\d{1,3})\s+(.+)$/ (number, whitespace, text, no period after number) where the number is ≤ the reference footnote count (or ≤ 99), AND the line does not start a paragraph. But a wrapped paragraph line could start with a number... e.g., "2030" no (4 digits, and no space+text? "2030 agenda" could match \d{1,3}? "2030" is 4 digits so \d{1,3} won't match "2030" fully but regex ^\s*(\d{1,3})\s requires whitespace after 1-3 digits; "2030 agenda" — \d{1,3} could match "203" then next char "0" is not whitespace, so no match at that position; regex anchored at start: ^\s*(\d{1,3})\s — "2030" fails because after "203" comes "0". Good. But "16 3" no. A line like "3 per cent of..." would match. Risk exists but acceptable; I'll also require the footnote number to be ≤ 99 and the line to be relatively... hmm.

Actually, better: footnotes in UN documents appear at the bottom of the page, typically after a blank line following the body, and often the whole footnote block is at the end. Also footnote numbers are sequential per document (1, 2, 3...). I could collect candidate footnote lines and check if their numbers form an increasing sequence. Simpler robust approach: treat a line as a footnote if it matches /^\s*(\d{1,2})\s+\S/ AND the number is strictly greater than the previous footnote number seen (sequential) — footnote numbers increase monotonically through the document. That's a decent heuristic. But also the asterisk style: /^\s*\*\s+\S/ or /^\s*[†‡]\s/.

Hmm, but I also need to handle the case where footnote text is inline in the flow. Let me not over-engineer. The key deliverables:

1. Paragraph splitting: find paragraph starts /^\s*(\d{1,3})\.\s*(?:\n|$)/m — number + period at line start. Paragraph text = everything until the next paragraph start or end, with header/footer/footnote lines removed, joined with spaces (or newlines preserved?). For display, join lines with "\n" or space. PDF text has hard wraps; joining with space is typical. But some lines are list items. I'll join with a space but keep it simple; maybe preserve line breaks as spaces.

Wait — careful: paragraph number might be inline: "1. A clean, healthy..." on same line. Handle /^\s*(\d{1,3})\.\s+/ too. Combined regex on the full text: /(?:^|\n)\s*(\d{1,3})\.\s+/g? But "1." alone on a line followed by newline then text — the sample shows "1.\nA clean...". So pattern: line starts with number+period, then either end-of-line or space+text.

Also sub-paragraphs like "12(a)"? GCs sometimes have "(a)" lists — those stay within the paragraph. Fine.

Also there might be section headings like "I. Introduction" — "I." is roman, won't match \d. Good. But "A.", "B." fine. What about numbered sections in some docs like "1. Introduction" — that IS paragraph 1 in GCs. OK.

Edge: page footer might be like "E/C.12/GC/27" + page number "2" on separate lines, or "2 E/C.12/GC/27". Handle lines containing the symbol → drop. Lines that are only digits → drop (page numbers). But wait: could a paragraph number line "1." be confused? It has a period, so /^\d+$/ won't match. Good.

Also headers repeated on each page: symbol, "United Nations", "Economic and Social Council", "Distr.: General", "6 November 2025", "Original: English". My classifier handles these. Also possibly "GE.25-xxxxx" lines. Add pattern /^GE\.\d+/.

Also the first page has title block: "Committee on Economic, Social and Cultural Rights", "General comment No. 27 (2025) on economic, social and cultural rights and the environmental dimension of sustainable development*". These appear before paragraph 1, so they're naturally excluded (text before first paragraph start is dropped). Good — I only keep text from the first paragraph start onward. But footnotes could appear before? No.

But careful: the title contains "No. 27" — not at line start with period... "General comment No. 27 (2025)..." — line starts with "General", fine.

2. Footnote removal: within paragraph text, remove footnote lines. Footnote lines: at end of pages. Heuristic: line matches /^\s*(\d{1,2})\s+\S/ and number ≤ 99 and (number > last footnote number seen OR first) — sequential check. Also asterisk footnotes: /^\s*\*\s+\S/ or starting with "________" separator lines. Also footnote marker inline in text (superscript) — e.g., "development*" — the asterisk stays in text; that's fine, it's part of the sentence. Actually the reference first_words for para 1 is "A clean, healthy and sustainable environment" — six words: "A clean, healthy and sustainable environment". The raw text: "A clean, healthy and sustainable environment is an essential precondition..." — first six words match. Good.

Hmm wait, "first six words" — reference.first_words values are "the first six words of each numbered paragraph". So comparison: take first 6 words of my extracted paragraph (after cleaning) and compare to reference string. Normalize whitespace, maybe strip trailing punctuation? The reference presumably comes from the same extraction, so exact match after normalization should work if my cleaning is right. I'll normalize: collapse whitespace, trim. Compare case-sensitively? Maybe case-insensitive to be safe? The instruction: "mark every paragraph whose first words differ from the reference". I'll do exact comparison after whitespace normalization; maybe also compare with punctuation stripped? Risky either way. I'll compare normalized (collapse spaces, trim) exactly, and if mismatch, also try case-insensitive — no, keep it deterministic: exact normalized comparison. Hmm, but if my paragraph text starts with the number "1. A clean..." I must strip the leading "N." before taking first words. Yes — strip the paragraph marker.

Also hyphenation: PDF text may have "tr\nuncated" hyphen splits? The sample shows "tr\n[… rest omitted]" — actually the sample text itself was truncated in the preview, not hyphenated. Real data may have hyphenated line breaks ("sustain-\nable"). Should I dehyphenate? The reference first_words presumably derived from clean text. If the real PDF text has "well-\nbeing", joining with space gives "well- being" vs reference "well-being". To be safe, when joining lines within a paragraph, if a line ends with "-", join without space and remove the hyphen? That's standard dehyphenation. But it could wrongly merge legitimate hyphens at line breaks... In PDF extraction, a trailing hyphen at line end is almost always a soft hyphen. I'll do: when joining, if previous line ends with "-" and next starts with lowercase letter, join directly removing hyphen. Hmm, but reference might have been generated without dehyphenation. Uncertain. The sample page 1: "...droughts, and tr" — that's the preview truncation, not real. I'll implement dehyphenation but... risk: if reference was computed on raw joined text with "word-\nnext" → "word- next", my dehyphenated "wordnext" would mismatch. Alternatively join with space always: "word- next". Which matches reference? Unknown. 

Hmm. Let me think about what the reference generator likely did: "first_words: the first six words of each numbered paragraph". If they split on whitespace of the raw text, "sustainable development*" etc. For safety, maybe compare in a way tolerant to hyphenation: normalize by removing "- " sequences? I could compare after normalizing both sides: collapse whitespace AND remove spaces after hyphens? That would make "well- being" == "well-being". And dehyphenation "wellbeing" vs "well-being" would differ. So safer: join lines with space (no dehyphenation), and when comparing, normalize by collapsing whitespace and also removing whitespace following a hyphen on both sides. That handles both. Actually simpler: normalize function: s.replace(/\s+/g,' ').trim(), and for comparison also s.replace(/-\s+/g,'-'). Apply to both extracted and reference. Good.

Also the first words might include the paragraph number if reference includes it? "first_words": {"1": "A clean, healthy and sustainable environment"} — no number. Good.

3. UI requirements:
- Title, one-line description of data (source, n, years) at top. For pdf_text: title, symbol, source, count (pages), doc_url link.
- "How this is computed" note near every chart/number.
- Show found paragraphs count vs reference.paragraphs (and footnotes found vs reference.footnotes).
- Table: paragraph number + first line (first ~N words or first line of text). Clicking a row expands full paragraph.
- Mark mismatched paragraphs (first words differ from reference) — e.g., a ⚠ badge and row highlight.
- CSV download button: columns like paragraph, first_words, match (true/false), reference_first_words, full_text. Must be generated client-side with Blob — allowed (no network).
- Every row showing a document has symbol linked to doc_url — the doc header should link symbol → doc_url.
- Base font 16px, accent #1f6fb2, light background, no horizontal scroll, no external resources.
- Handle empty lists / missing values: if pdf_text missing or records empty, show message.

Also maybe a small chart? Not required. The user didn't ask for charts. Keep it a table tool. Maybe a summary bar: found vs reference. Could use Chart.js but not necessary; a simple comparison display is fine. The rules say "a short 'How this is computed' note near every chart or number" — I'll add notes near the counts.

CSV download: create Blob, URL.createObjectURL, anchor click. That's fine offline.

Let me now design the parser carefully.

```js
const pdf = window.WORKSHOP_DATA && window.WORKSHOP_DATA.pdf_text;
```

If !pdf or !Array.isArray(pdf.records) or empty → show "no data" message.

Steps:

```js
const symbol = pdf.symbol || "";
const pages = pdf.records.slice().sort((a,b)=> (a.page||0)-(b.page||0));
```

Build lines: for each page, split text into lines. Track page boundaries.

Line classification function `isBoilerplate(line)`:
- trim; if empty → skip
- if line === symbol or line starts with symbol (e.g., "E/C.12/GC/27  2" or "2  E/C.12/GC/27") → skip. Check `line.includes(symbol)` when symbol non-empty → skip. Careful: symbol could appear in body text? Unlikely at line start... includes anywhere in line — body text rarely contains the symbol. But footnote or body might reference "E/C.12/GC/27"? Possible in citations like "see E/C.12/GC/27". Hmm. Restrict: skip if line starts with symbol OR line ends with symbol OR line is symbol + digits. Let me do: `const s = symbol; if (s && (line === s || line.startsWith(s + " ") || line.endsWith(" " + s) || new RegExp("^\\d+\\s+" + escapeRegex(s) + "$").test(line) || new RegExp("^" + escapeRegex(s) + "\\s+\\d+$").test(line))) skip`. Simpler: strip digits and spaces from line and compare to symbol: `line.replace(/[\d\s]/g,'') === s` → skip. That catches "E/C.12/GC/27", "E/C.12/GC/27 2", "2 E/C.12/GC/27". Nice.
- /^United Nations$/i, /^(Economic and Social Council|General Assembly|Human Rights Council|Security Council|Trusteeship Council|International Court of Justice|Secretariat)$/i → skip
- /^(Distr|Distribution|Original|Language)\s*[.:]/i → skip... "Original: English", "Distr.: General". Pattern: /^(Distr\.?|Original|Gen\.?)\s*:/i
- Date line: /^\d{1,2}\s+(January|February|...|December)\s+\d{4}\.?$/i → skip. Also formats like "6 November 2025". Also "November 2025"? Add /^(January|...)\s+\d{4}$/i.
- Page number only: /^\d{1,4}$/ → skip (footer page number). But careful: could a paragraph number be on its own line without period? In this doc format, numbers have periods. Also footnote numbers on their own line? Footnote text usually follows on same line. I'll treat pure-digit lines as page numbers.
- GE line: /^GE\.\d+/i → skip.
- "para" markers? no.

Footnote detection: within the kept stream, a line is a footnote if:
- /^\s*(\d{1,2})\s+\S/ and the number ≤ 99 and number > lastFootnoteNum (monotonic) — but footnotes restart? In UN docs footnote numbering is continuous per document usually (1..N). Reference has total footnotes count. Alternatively number ≤ reference.footnotes if available.
- OR line starts with "* " / "† " / "‡ " / "§ " followed by text: /^\s*[*†‡§¶]\s+\S/ — but the title line ends with "*" attached to word, not line start. A footnote line starting with "* " is plausible.
- Also separator lines like "________" → skip.

But danger: a body line starting with a number+space, e.g., "2030" no (4 digits). "3 per cent" — possible in text but at line start after wrap? A wrapped line could start with "3 per cent of GDP..." Hmm. The monotonic constraint helps: footnote numbers increase; body line "3 per cent" would only be misclassified if 3 > lastFootnoteNum. Early in doc, lastFootnoteNum=0, so "3 per cent..." at line start would be misclassified. Risk.

Additional constraint: footnotes appear at the bottom of a page — i.e., after them, the next non-empty line is either end of page or another footnote or page footer. Hard to know "bottom" without page info — but I DO have page info (records per page). So: within a page's lines, footnote candidates are lines matching the number pattern that occur after the last "paragraph-ish" content? Hmm.

Alternative approach: footnotes in UN GC PDFs are typically separated from body by a horizontal rule or appear after the body text on the page. In extracted text, often there's a blank line then footnote lines. 

Let me use a different robust signal: footnote lines start with a number followed by whitespace, and the SAME number appears as a superscript marker in the body text of that page (e.g., "development1" or "development 1" or "development*"). Too complex.

Pragmatic approach: classify a line as footnote if it matches /^\s*(\d{1,2})\s{1,}\S/ AND (number ≤ maxFootnotes) AND (number === lastFootnoteNum + 1 OR number > lastFootnoteNum) AND the line is in the last portion of the page? I think I'll go with: footnote if matches number pattern AND number ≤ (reference.footnotes || 99) AND number > lastSeenFootnote. Plus asterisk-style. And also treat lines starting with a number+period? No, those are paragraphs.

Actually, wait — maybe simpler and safer: since paragraphs are delimited by "N." starts, footnote lines that fall INSIDE a paragraph's captured text are the problem. Footnote lines at page bottom fall inside whatever paragraph spans the page break. So I must remove them from the captured text. The monotonic heuristic is the main tool. Let me also require that footnote-candidate lines are short-ish? No, footnotes can be long.

Additional heuristic: footnote lines in UN PDFs often begin with the number and then the text, and the number is followed by TWO spaces or a tab in original, but extraction gives single space. Can't rely.

Another signal: footnote blocks usually come after a blank line at the end of the page's text. I can check: is there any non-footnote, non-boilerplate line AFTER this candidate within the same page? If the candidate is in the trailing run of the page (only footnotes/boilerplate/blank lines follow it within the page), it's likely a footnote. Combined with the number pattern, that's quite safe: body text lines have body text after them (unless the page ends mid-paragraph — then the trailing run is the paragraph's last lines, which don't start with "N " pattern usually... but could: "...costs 3\nper cent..." hmm, the line "per cent" doesn't start with number; the line starting with "3" would be "...costs 3" which ends the line, next line "per cent". So a line starting with "3 per cent" as a wrap-start is possible but less common).

I'll combine: candidate = matches /^\s*(\d{1,2})\s+\S/ (no period), number ≤ limit, number > lastFootnote, AND all following non-blank lines in the same page are also footnote-candidates or boilerplate. That trailing-run condition is strong. Let me implement per-page processing:

For each page:
1. lines = text.split(/\r?\n/)
2. classify each line: blank / boilerplate / paraStart / footnoteCandidate / body
3. Determine trailing footnote block: scan from end of page's lines; while line is blank/boilerplate/footnoteCandidate → mark; stop at first body/paraStart line. All footnoteCandidates in that trailing run → footnotes. But also footnoteCandidate lines NOT in trailing run (mid-page)? In UN layout footnotes are always at page bottom, so mid-page candidates are body text → keep as body. 

Hmm, but what if the page ends exactly at a paragraph end and footnotes follow — trailing run works. What if a footnote is long and wraps — multiple lines, only first starts with number; wrapped continuation lines don't match the pattern and are not boilerplate → they'd break the trailing run! E.g., footnote "1 See OHCHR, ... very long\nwrapped line". The wrapped line is body-classified, so trailing run stops before it, and then the "1 See..." line is not in trailing run → kept as body. Bad.

Fix: trailing run should allow continuation lines. Alternative: scan from end: skip blanks/boilerplate; then collect lines backwards while they are footnoteCandidate OR (continuation: not paraStart and not boilerplate and we're already in footnote mode). Hmm, getting complicated. Let me define: find the last paraStart or "strong body" line index... 

Simpler alternative: footnote mode per page: once we hit the first footnoteCandidate in the trailing region... circular.

Different approach: process lines sequentially with a state machine per page:
- state = body
- When we encounter a footnoteCandidate (number pattern, number > lastFootnote, ≤ limit): tentatively mark it and enter "maybe footnote" state. In this state, subsequent lines that are blank/boilerplate/footnoteCandidate/other-text are all absorbed as footnote UNTIL we hit a paraStart line or a new page. But body text after a footnote on the same page? In UN layout, footnotes are at the bottom, so after footnotes comes only footer. So: once a footnoteCandidate appears, everything after it on that page (except paraStart? no—paragraph can't start after footnotes on same page) is footnote/footer. Actually if a paragraph starts on the next page, the page ends. Within a page, after footnotes begin, only footnotes + footer remain. So rule: the FIRST footnoteCandidate on a page (satisfying number constraints) starts the footnote block; everything after it on that page is footnote/boilerplate (dropped from paragraphs). 

But false positive: a body line mid-page starting with "3 per cent" would wrongly start footnote block and drop the rest of the page. Mitigate with the number constraints: number must be > lastFootnote AND ≤ limit (reference.footnotes or 99) AND... also footnote numbers usually appear in increasing order and the first footnote of the doc is "1". A body line "3 per cent" when lastFootnote=0 would pass. Hmm.

Extra mitigation: require the candidate to be preceded by a blank line? In PDF extraction, there's usually a blank line between body and footnotes (the horizontal rule may vanish). Not guaranteed.

Alternative extra mitigation: check that the number appears as a marker in the body text of the same page: search page text for the number attached to a word (e.g., /[a-z\*]\s?3\b/ hmm). Superscript markers in extraction often appear as "development1" (no space) or "development 1". I could check: does the page's body text contain a word character immediately followed by the number (like /[A-Za-z\*)](\d{1,2})\b/)? For "3 per cent" body line, the page body would need "...word3" somewhere — unlikely. For real footnote 3, the body has "text3" or "text 3" marker. This is a decent signal but extraction may insert space: "development 3". Then /[A-Za-z]\s+3\b/ could false-positive on "article 3"! Ugh. "article 3" is common. So require no-space attachment: /[A-Za-z\*)\]]3(?!\d)/ — "development3". But extraction might give "development 3" with space... 

I'm overthinking. Given this is a workshop tool with a reference to check against, the honest approach: implement the heuristic, show found vs reference counts, and mark mismatches — the tool itself surfaces discrepancies. The user explicitly wants to see found vs real and mismatches. So even if heuristics are imperfect, the UI shows it. I'll use: footnoteCandidate = line matches /^\s*(\d{1,2})\s+\S/ with number ≤ limit and number > lastFootnoteNum, OR line matches /^\s*[*†‡]\s+\S/. First such candidate on a page starts footnote block for the rest of that page. Also handle the case where footnote number equals... if numbering restarts per page? UN GCs number footnotes continuously. OK.

Hmm wait, one more consideration: what if footnotes appear like "1" on its own line then text on next line? Pure digit line is classified as page number and dropped — fine either way, but then the text line after would be body... and it'd be after footnote block start? No — the "1" line is dropped as boilerplate before footnote detection, so the following text line is a body line mid-page. Edge case; accept.

Also: what about the paragraph text containing the footnote marker like "development*"? Keep as is.

Now paragraph extraction:
- Iterate pages in order, lines in order, skipping boilerplate and footnote-block lines.
- Maintain `current` paragraph: when line matches paraStart /^\s*(\d{1,3})\.\s*(.*)$/ → start new paragraph with number and remainder. Note: number must be plausible: 1..999. Also require that numbers are... could there be "1." in body mid-line? We anchor at line start. Also section headings "I." won't match. But what about list numbering like "1." inside a paragraph (sub-list)? GCs use (a), (b). Risk accepted. Also require sequential? Paragraph numbers should be increasing; if a line starts with "N." where N ≤ last paragraph number, it might be a false positive (e.g., a wrapped line starting with "3. something"?). I'll require N > lastParaNum OR N === lastParaNum+1? Real docs: paragraphs are 1,2,3,... sequential. I'll accept N > lastParaNum (monotonic), which also filters most false positives. Hmm, but what if a paragraph number repeats due to extraction duplication? Monotonic filter drops it — good.

Wait, but what about the very first page: "1." appears after the title block. Lines before first paraStart are dropped (title, headers). Good.

- Append body lines to current paragraph's lines array. If no current paragraph yet, drop (preamble).
- At the end, join each paragraph's lines: join with " "? Or preserve newlines? For "first line" display, I'll show first ~15 words. For full text, join lines with "\n"? PDF hard wraps make "\n" ugly but preserves structure; joining with space reflows. I'll join with a space, but handle hyphen: if line ends with "-" and next begins with a letter, join without space removing hyphen? As discussed, comparison normalization handles "- ". For display, I'll join with space and then collapse " -" ? Let me just join with " " and collapse multiple spaces. For dehyphenation in display: replace /-\s+/g with "-" when joining? That changes "well- being" → "well-being" which reads better. And for comparison, apply same normalization to reference. But if reference kept "well- being"... then mismatch would be flagged incorrectly. Hmm. The reference first_words are only 6 words — hyphenation at exactly the 6th word boundary is unlikely. I'll normalize both sides with `norm(s) = s.replace(/-\s+/g,'-').replace(/\s+/g,' ').trim()` for comparison, and for display join with space then collapse. Actually for display of full paragraph, I'll keep line breaks as spaces — fine.

Hmm, actually maybe better for display: keep the raw lines joined with "\n" inside a <pre>-ish block? The requirement: "Keep the full text of a paragraph available (click to expand)". I'll render full text with white-space: pre-wrap and join lines with "\n" — preserves the PDF line structure, honest to source. And first-line preview = first line of the paragraph (or first N words). "a table with each paragraph's number and first line" — first line literally. I'll show the first line (truncated with ellipsis via CSS) — but if the first line is very long, CSS ellipsis. Also maybe show first 12 words. I'll show the first line of the joined text; if empty (number on own line, text on next), the "first line" is the first non-empty line. Good.

Comparison: first 6 words of the cleaned paragraph text (joined with space, marker stripped) vs reference.first_words[String(n)]. Normalize both. If reference missing for that number → mark as "no reference" (neutral). If mismatch → mark ⚠.

Wait — "first six words": reference values like "A clean, healthy and sustainable environment" — count: A(1) clean(2) healthy(3) and(4) sustainable(5) environment(6). Yes 6 words. So I take first 6 words of my text: split on whitespace, take 6, join with space. Compare normalized. Note punctuation: "environment" vs "environment," — reference presumably exact from same source. I'll compare with normalization that also strips trailing punctuation? If reference is "A clean, healthy and sustainable environment" and my text gives same, fine. I'll do exact normalized compare; additionally, to be forgiving, also compare after removing all punctuation? If either matches, count as match? That could mask real diffs. The user wants to SEE diffs. I'll do exact normalized comparison (whitespace + hyphen-space normalization only). Hmm, also case: keep case-sensitive.

Actually, let me reconsider: maybe compare word-by-word with case-insensitive? No — deterministic exact is fine, and mismatches get displayed with both strings shown, so the user can judge. I'll show, for mismatched rows, the expected vs found first words in the expanded view.

Counts to show:
- Paragraphs found: X — reference says Y. Match/mismatch indicator.
- Footnotes found: X — reference says Y. (I count footnote lines/blocks found.)
- Pages: count of records.
- Also maybe: paragraphs with mismatching first words: Z.

CSV: columns: paragraph, first_words_found, first_words_reference, match, full_text. Escape quotes. Filename like `E_C_12_GC_27_paragraphs.csv` (sanitize symbol). Download via Blob.

UI layout:
- Header: title "Paragraph splitter — {pdf.title}", symbol linked to doc_url (new tab), source line: "Source: {pdf.source} · {count} pages · document {symbol}". Description of data: source, n (pages), years? pdf_text has no years; description: "Raw text of {symbol} as extracted from the PDF, {n} pages, from {source}." Include doc_url link.
- "How this works" note: explain cleaning rules (headers/footers removed: symbol lines, UN masthead lines, date lines, page numbers; footnotes = numbered lines at the foot of a page; paragraphs = lines starting with "N.").
- Summary cards: Paragraphs found vs reference (big numbers), footnotes found vs reference, mismatches count. Each with a small "how computed" note.
- Table: # | first line | status badge (OK / differs / no reference). Click row → expandable detail showing full paragraph text, found first words, reference first words (if any), and maybe which page it starts on. I'll track the page where each paragraph starts — nice touch: "starts on page X".
- CSV download button.
- If pdf_text missing/empty → message.

Also handle reference possibly missing (reference may be absent?) — spec says reference exists, but handle missing gracefully: show "no reference available".

Also the top-level description: "one-line description of the data (source, n, years) at the top". For pdf_text: source = pdf.source, n = count (pages). Years: not applicable; maybe use reference.adopted? reference has `adopted` — could show "adopted {adopted}". I'll include if present.

Let me also double check: "Every row that shows a document has its symbol, linked to doc_url in a new tab." — the header shows symbol → doc_url. Table rows are paragraphs of the same doc; I'll also put the symbol link in the header area and maybe in each expanded row? The rule says every row that shows a document — the doc is shown once in header. To be safe, in the expanded paragraph detail I can include "Source: symbol (link)". I'll add symbol link in header and in the detail footer. Fine.

Now, code structure. Single HTML file, inline CSS/JS. Use Chart.js? Not needed — no charts requested. The system prompt says use Chart.js for charts; if no charts, fine.

Let me write the parser code carefully.

```js
(function(){
  "use strict";
  var data = window.WORKSHOP_DATA || {};
  var pdf = data.pdf_text;
  var el = function(id){ return document.getElementById(id); };
  ...
})();
```

Parsing:

```js
var MONTHS = "January|February|March|April|May|June|July|August|September|October|November|December";
function escapeRe(s){ return s.replace(/[.*+?^${}()|[\]\\]/g, "\\$&"); }

function isBoilerplate(line, symbol){
  var t = line.trim();
  if(!t) return true;
  if(symbol){
    var stripped = t.replace(/[\d\s]/g, "");
    if(stripped === symbol.replace(/[\d\s]/g,"")) return true; // symbol ± page number
  }
  if(/^United Nations$/i.test(t)) return true;
  if(/^(Economic and Social Council|General Assembly|Human Rights Council|Security Council|Trusteeship Council|International Court of Justice|Secretariat)$/i.test(t)) return true;
  if(/^(Distr|Distribution|Original|Language|Status)\s*[.:]/i.test(t)) return true;
  if(new RegExp("^\\d{1,2}\\s+(" + MONTHS + ")\\s+\\d{4}\\.?$", "i").test(t)) return true;
  if(new RegExp("^(" + MONTHS + ")\\s+\\d{4}\\.?$", "i").test(t)) return true;
  if(/^\d{1,4}$/.test(t)) return true; // page number
  if(/^GE\.\d+/i.test(t)) return true;
  if(/^_+$/.test(t)) return true; // rules
  return false;
}
```

Wait: symbol stripped of digits/spaces — symbol "E/C.12/GC/27" → "E/C./GC/" — and line "E/C.12/GC/27 2" → "E/C./GC/" equal → boilerplate. But careful: line "2" alone → stripped "" ≠ symbol. OK. But what if symbol is empty → skip check.

Hmm, one problem: `t.replace(/[\d\s]/g,"")` on a body line that happens to equal symbol-without-digits? Only if line is exactly the symbol possibly with digits — body lines are longer. Fine.

Footnote candidate:

```js
function footnoteNum(line, limit, last){
  var m = line.match(/^\s*(\d{1,2})\s+\S/);
  if(m){
    var n = parseInt(m[1],10);
    if(n <= limit && n > last) return n;
  }
  var m2 = line.match(/^\s*([*†‡§])\s+\S/);
  if(m2) return 1000 + 0; // asterisk-style, always accept? hmm
  return 0;
}
```

Asterisk-style: return a sentinel that's > last always? Let me handle: if asterisk-style, treat as footnote start regardless of number. I'll return {type:'sym'} vs {type:'num', n}. Simplify: function returns truthy if candidate; track lastNum for numbered ones.

Main loop:

```js
var limit = (ref && typeof ref.footnotes === "number") ? ref.footnotes : 99;
var lastFoot = 0;
var paras = []; // {num, lines:[], page}
var footnotesFound = 0;
var cur = null;
var pages = (pdf.records||[]).slice().sort(function(a,b){ return (a.page||0)-(b.page||0); });
pages.forEach(function(p){
  var lines = String(p.text||"").split(/\r?\n/);
  var footnoteMode = false;
  lines.forEach(function(line){
    if(isBoilerplate(line, symbol)) return;
    if(footnoteMode) { 
      // count footnote lines? count blocks instead
      return; 
    }
    var pm = line.match(/^\s*(\d{1,3})\.\s*(.*)$/);
    if(pm){
      var n = parseInt(pm[1],10);
      if(!cur || n > cur.num){ // monotonic
        cur = {num:n, lines: pm[2] ? [pm[2]] : [], page: p.page};
        paras.push(cur);
        return;
      }
      // if n <= cur.num, treat as body? or ignore. Treat as body line appended.
    }
    var fm = line.match(/^\s*(\d{1,2})\s+\S/);
    if(fm){
      var fn = parseInt(fm[1],10);
      if(fn <= limit && fn > lastFoot){
        lastFoot = fn;
        footnotesFound++;
        footnoteMode = true;
        return;
      }
    }
    if(/^\s*[*†‡§]\s+\S/.test(line) && cur){ footnotesFound++; footnoteMode = true; return; }
    if(cur) cur.lines.push(line.trim());
  });
});
```

Hmm wait, issue: footnoteMode per page — reset at each page start (done via `var footnoteMode=false` inside forEach). Good.

Issue: paragraph start detection when n <= cur.num — e.g., false "3." line inside paragraph 5. Append as body. But also: what if the doc has paragraphs numbered non-monotonically due to extraction? Unlikely.

Another issue: the first paragraph "1." — before it, cur is null, lines dropped. But the check `if(!cur || n > cur.num)` — for the first paraStart, cur null → create. Good. But what if a "1." appears in the preamble (title area)? E.g., title "General comment No. 27" — no line-start "1.". OK.

Wait, there's a subtle problem: `pm` matches ANY line starting with digits+period, including something like "2025." at line start? \d{1,3} allows "202" then "5." — "2025." → ^\s*(\d{1,3})\. requires period right after 1-3 digits; "2025." has "2025" then "." — \d{1,3} matches "202", next char "5" ≠ "." → no match at start... regex is anchored ^, \d{1,3} greedy tries "202", then needs ".", gets "5" → backtrack to "20", needs ".", gets "2" → fail. So "2025." doesn't match. Good. But "20. " would match — a year "20." unlikely.

Also section headings like "II. " won't match. "A." no. Good.

But hmm — what about paragraphs where the number and text are separated by the number on its own line: "1.\nA clean..." — pm matches "1." with pm[2] = "" → lines start empty, then "A clean..." appended. Good.

Now, one more: what if a paragraph number line appears while footnoteMode is on (shouldn't happen since footnotes at page bottom)? If it does, we skip it — could lose a paragraph. Acceptable; but let me handle: in footnoteMode, if line matches paraStart with n > cur.num, end footnoteMode and start new paragraph? Footnotes are at page bottom, next page starts new content — but page boundary resets footnoteMode anyway. Within same page after footnotes, a paraStart shouldn't occur. I'll add the safety: if footnoteMode && pm && (!cur || n > cur.num) → footnoteMode=false, handle as para start. Let me restructure: check paraStart BEFORE footnoteMode check. But then a footnote line like "3. something"? Footnotes don't have "N." format (they're "N text"). But wait — could a footnote line be "12. See..."? If the converter kept the period... then it'd be misread as paragraph 12. The monotonic check (n > cur.num) might allow it if cur.num < 12. Hmm. In UN GC docs, footnote markers are superscript numbers without periods. I'll trust that.

Reorder: 
```js
lines.forEach(function(line){
  if(isBoilerplate(line,symbol)) return;
  var pm = line.match(/^\s*(\d{1,3})\.\s*(.*)$/);
  if(pm && (!cur || parseInt(pm[1],10) > cur.num)){
    cur = {...}; paras.push(cur); footnoteMode=false; return;
  }
  if(footnoteMode) return;
  ... footnote detection ...
  if(cur) cur.lines.push(line.trim());
});
```

Wait but if pm matches but n <= cur.num (false positive inside paragraph), we fall through to footnote check: "3. text" — fm regex requires \d{1,2}\s+\S — "3." has period so \s after digits fails ("3." → digits "3" then "." not \s) → no footnote match → appended as body. Good.

Footnote counting: count blocks or lines? reference.footnotes = "how many footnotes". I'll count footnote starts (numbered ones + symbol ones). Each footnoteMode trigger = 1 footnote. But a footnote's wrapped lines are skipped silently. Good: footnotesFound increments once per footnote start.

Hmm, but asterisk-style footnotes: multiple asterisk footnotes? Usually one "*" per doc or per page. Counting each trigger as one footnote is approximate. Fine — it's shown next to reference.

Now building paragraph text:

```js
function paraText(p){
  return p.lines.join(" ").replace(/\s+/g," ").trim();
}
```

Hmm — joining with space loses line structure. For full-text display I said keep newlines. Let me store lines and provide both: fullText = lines.join("\n") for display (pre-wrap), flat = lines.join(" ") for word ops. Actually for CSV, full text with newlines is fine (quoted). I'll use flat for first-words and CSV maybe with newlines escaped. CSV: I'll put full text with "\n" inside quotes — valid CSV. Or replace newlines with " ⏎ "? Keep real newlines, properly quoted. Fine.

First words:

```js
function firstWords(text, k){
  return text.split(/\s+/).filter(Boolean).slice(0,k).join(" ");
}
function norm(s){
  return String(s||"").replace(/-\s+/g,"-").replace(/\s+/g," ").trim();
}
```

Compare: norm(firstWords(flat,6)) === norm(ref.first_words[String(num)]).

Wait — should I take 6 words, or compare the whole reference string against my first-words? Reference value is exactly the first six words. So take first 6 words of mine and compare to reference string (normalized). But what if reference has different word count (e.g., 5 words)? Take max(6, refWords.length)? Safer: compare norm(firstWords(flat, 6)) with norm(refVal); if refVal has more than 6 words, also try firstWords(flat, refVal.split(/\s+/).length). I'll compute k = max(6, number of words in refVal). Good.

Status per paragraph: "ok" | "diff" | "noref".

Summary:
- found = paras.length; refCount = ref.paragraphs (number). Show "Found X numbered paragraphs — the document's reference says Y." with ✓/⚠.
- footnotes found vs ref.footnotes.
- mismatches count.

Table rendering: build rows via DOM (createElement) or innerHTML with escaping. I'll write an escapeHtml function and build with template strings + event delegation. Rows: `<tr data-i="...">` with cells: number, first line (first non-empty line, or first 20 words), badge. Click toggles a detail row below with full text (pre-wrap), found first words, reference first words, page start, symbol link.

Also add a filter? Not requested. Keep simple. Maybe a small text filter input? Not requested; skip to keep under line budget. Actually a search box could help with 20+ paragraphs... The doc has maybe ~40-60 paragraphs. A filter input is cheap and useful. I'll add a simple filter by number or text. Hmm, keep scope tight; the user asked specific things. I'll add it anyway? "Build a tool that splits..." — specific. I'll skip extra features except maybe showing page number column. Keep: # | starts on page | first line | status. 

CSV:

```js
function toCSV(rows){
  function q(v){ v = String(v==null?"":v); return '"' + v.replace(/"/g,'""') + '"'; }
  var head = ["paragraph","starts_on_page","first_words_found","first_words_reference","matches_reference","full_text"];
  ...
}
```

Download:

```js
var blob = new Blob([csv], {type:"text/csv;charset=utf-8"});
var a = document.createElement("a");
a.href = URL.createObjectURL(blob);
a.download = filename;
document.body.appendChild(a); a.click(); setTimeout(...revoke...)
```

Filename: (symbol||"document").replace(/[^\w.-]+/g,"_") + "_paragraphs.csv".

Header info: 
- Title: "Numbered-paragraph splitter" + doc title.
- Line: `{pdf.title} — {symbol} (link to doc_url, target _blank) · Source: {pdf.source} · {count} pages · adopted {ref.adopted}` — one-line description with source, n. Years: pdf has no year; use adopted if present. I'll phrase: "Raw PDF text of {symbol} ({pdf.title}), {n} pages, from {source}." plus adopted.

How-this-is-computed notes:
- Near summary: "Counted by this script: a paragraph starts at a line beginning with 'N.' (N increasing); page headers/footers (UN masthead, symbol lines, dates, page numbers) are dropped; footnotes are the numbered lines at the foot of a page and are kept out of the paragraph text. Reference values come from WORKSHOP_DATA.pdf_text.reference."
- Near table: "First line = first non-empty line of the cleaned paragraph. ⚠ = the first six words differ from the reference. Click a row for the full text."

Edge cases: pdf missing → show notice. records empty → notice. paras empty → notice "no paragraphs found".

Also handle `pdf.records` possibly not sorted — sort by page. Handle missing page → 0.

Also `count` field: pdf.count = number of pages presumably. Show "n = {pdf.count} pages (records: {records.length})".

Now the mismatch marking: rows with status "diff" get class "diff" (light red/amber background) and badge "⚠ differs". "ok" → "✓ matches". "noref" → "no reference".

Also show in summary: "Z paragraphs whose first words differ from the reference".

Let me also double-check the sample page 1 to validate the parser mentally:

Lines: "E/C.12/GC/27" → boilerplate (symbol). "United Nations" → bp. "Economic and Social Council" → bp. "Distr.: General" → bp. "6 November 2025" → date bp. "Original: English" → bp. "Committee on Economic, Social and Cultural Rights" → not bp, cur null → dropped (preamble). "General comment No. 27 (2025) on ..." → dropped. "I." → not paraStart (roman), cur null → dropped. "Introduction" → dropped. "1." → paraStart, cur={1, lines:[]}. "A clean, healthy and sustainable environment is an essential precondition for the" → body. ... etc. 

The title line "General comment No. 27 (2025) on economic, social and\ncultural rights and the environmental dimension of\nsustainable development*" — wrapped lines, all dropped since cur null. Good.

Footnote on page 1: the "*" footnote text at page bottom, e.g. "* OHCHR ..." → matches asterisk pattern → footnoteMode. But wait: my asterisk check requires cur non-null? I wrote `if(/^\s*[*†‡§]\s+\S/.test(line) && cur)`. If cur null (preamble), an asterisk line would be dropped anyway as body? If cur null, `if(cur) cur.lines.push` — dropped. Fine, no need for the cur condition; but footnoteMode should still trigger to skip rest of page — if cur null, nothing after matters anyway. Keep simple: trigger footnoteMode regardless.

Hmm, but danger: a body line starting with "*"? Like a bullet "* item"? In GCs, bullets are (a), (b) or dashes. A line starting "* " is likely a footnote. Accept.

Also numbered footnote "1 See resolution..." — fm matches, fn=1 ≤ limit, > lastFoot(0) → footnote. Good. But what if body text has a line starting "1 " mid-page before any footnote? E.g., "...in 2020.\n1 000 people..." hmm "1 000" with space — thousands separator! "1 000" would match fm (digits "1", space, "000..."). fn=1 > 0 → false footnote, drops rest of page! Dangerous. Mitigation: require the char after the number+space to be a letter (footnote text starts with a letter usually): /^\s*(\d{1,2})\s+[A-Za-z(*]/? "1 000" → after space is "0" digit → reject. "1 See" → "S" letter → accept. Also require fn ≤ limit (reference footnotes count, e.g., maybe 20-40). "1 000" rejected by letter requirement. Also "3 per cent" → "p" letter → accepted if 3 > lastFoot... risk remains but trailing-position helps? I removed trailing-position check in favor of first-candidate-starts-block. Hmm. Let me add BOTH: candidate must match number+space+letter AND (fn > lastFoot) AND fn ≤ limit. Plus maybe require that we're in the latter part of the page? Can't know page length reliably... Actually I can: precompute per page the index of the last line; a footnote block is at the end. Alternative: two-pass per page: first find candidate indices; the footnote block starts at the first candidate such that all subsequent non-boilerplate lines are candidates or continuations... complex.

Let me think about actual UN GC PDFs (E/C.12/GC/27 real one): footnotes are like "1 See ..." at page bottom after a blank line. Body text lines starting with "N word" are rare. The "3 per cent" scenario requires a line wrap exactly before "3 per cent" — possible but uncommon. And with fn > lastFoot constraint, once real footnotes 1..k are seen, later body "3 per cent" won't trigger (3 ≤ lastFoot). The vulnerable window is before the first footnote (lastFoot=0): any body line starting with "1 letter..." or "2 letter..." would falsely trigger. E.g., a line starting "2 0 2 5..."? digit after space → rejected. "1 January 2025" as a body line? That'd be a date line — caught by date regex only if full-line date; "1 January 2025" IS a full-line date → boilerplate. OK.

I think number+space+letter+monotonic+limit is reasonably safe. Additionally, I can require the candidate line to be preceded by a blank line OR be at... no, extraction may not keep the blank. I'll also add: candidate must NOT be followed (within same page, next non-blank line) by a paraStart? No...

Alternative stronger signal: footnote numbers in the doc are ≤ reference.footnotes (limit). If reference.footnotes is, say, 30, then body line "45 per cent" won't trigger. And monotonic. I'll accept residual risk — and the tool honestly reports found vs reference, so the user sees if it went wrong. Also mismatched first-words get flagged. Good enough for a workshop tool, and I'll note the heuristic in "How this is computed".

One more: what if footnotes use the format "1" then tab then text — extraction gives "1\tSee..." → \s+ covers tab. Good.

What about footnote continuation lines that start with a number? e.g., wrapped footnote "…resolution 68/268\n1 of 2..."? Rare. Skip.

Now also: "keep the footnotes out of the paragraph text" — done via footnoteMode. But footnote markers inline (superscript digits) remain in text, e.g., "development1" or "development 1". Should I strip inline markers? The reference first_words for para 1: "A clean, healthy and sustainable environment" — the raw has "sustainable development*" at end of para 1's first sentence — not in first 6 words. Inline markers elsewhere might affect first-6-words of other paragraphs if a marker lands in the first 6 words. E.g., "2. The Committee recalls its general comment No. 26..." fine. If a paragraph starts "3. Recalling resolution 12/3, ..." hmm. I could strip inline superscript markers: patterns like /([A-Za-z\*\)\]])(\d{1,2})(?=\s|$|[,.])/g → remove the digits? But that would also strip legitimate "article 16" no — that has space before digits and word before space: "article 16" → the regex requires letter immediately before digits (no space): "article16" would strip — but extraction usually keeps space: "article 16". Superscript markers usually attach directly: "development1". Hmm, but sometimes extraction inserts space. Risky to strip "word 12" patterns. I'll strip only attached digits: /([A-Za-z\*\)\]])(\d{1,2})(?![0-9])/g → "$1". Wait that would transform "CRC12" legit? Rare. And "2030" — \d{1,2} with (?!\d) prevents matching within longer numbers: "2030" → at "0" after "2"? The regex scans: "2030" — match attempt at "2": ([A-Za-z...]) requires preceding letter — "2030" preceded by space → no match at "2". At "0" (second char): preceded by "2" (digit, not in class) → no. So "2030" safe. "article16" → "articl" + "e16"? preceded by "e" letter, digits "16", next char maybe space → strips to "article". If the doc meant "article 16" extracted as "article16", stripping breaks it. Hmm. Trade-off. The reference first_words were presumably computed from text WITH markers or without? Unknown. 

Given uncertainty, I'll NOT strip inline markers (keep text honest to source), and rely on normalization for comparison. If markers cause mismatches, they show as ⚠ and the user sees both strings — that's the tool working as intended (surfacing diffs). Actually wait — the user wants to verify their own splitting against the reference; false mismatches from markers would be noise. But I can't know. Keep it simple: no inline stripping. Hmm, actually let me reconsider: the sample shows "sustainable development*" — asterisk attached. If reference first_words for some paragraph includes the marker... The reference for para 1 doesn't reach the asterisk. I'll leave markers in.

Actually, you know, let me reconsider once more: the reference `first_words` is described as "the first six words of each numbered paragraph" — presumably from the true document text. If the PDF extraction attaches superscript footnote numbers to words, the reference (if generated from the same raw text by the workshop authors) would include them too. Either way, exact comparison is the honest approach. Done deliberating.

Now, "first line" for the table: first non-empty line of the paragraph (raw line, trimmed). If the paragraph's first line is just the number ("1." alone), first non-empty line is the text line. I'll compute `firstLine = p.lines.find(l => l.trim()) || ""`. Display truncated via CSS (text-overflow ellipsis, max-width). Also maybe show first 6 words? The user said "first line". OK.

Detail expansion: clicking a row toggles a detail row: full text in a <div class="full"> with white-space:pre-wrap, using lines joined with "\n". Plus meta: "Paragraph N · starts on page P · first six words found: '...' · reference: '...' · status". Plus symbol link.

Let me now also compute per-paragraph start page: p.page recorded at creation. Good.

Summary section markup:

```
<div class="cards">
  <div class="card"><div class="big">42</div><div class="lbl">paragraphs found</div><div class="note">Reference: 42 — match ✓</div></div>
  <div class="card">...footnotes...</div>
  <div class="card">...mismatches...</div>
  <div class="card">...pages...</div>
</div>
```

Each card gets a "how computed" note. The requirement: "a short 'How this is computed' note near every chart or number" — I'll put a note under each card and a general method note.

Now write the HTML/CSS. Design: light background (#f5f7fa), white cards, accent #1f6fb2, system font stack, base 16px, max-width ~1000px container, table full width, sticky header maybe. No horizontal scroll: table with word-break. Badges: ok = green-ish? Keep palette restrained: accent blue for links/buttons, amber (#b45309 / bg #fef3c7) for warnings, green (#15803d / bg #dcfce7) for match. That's fine.

Buttons: "Download CSV" accent button. Also maybe "Expand all / collapse all"? Small nicety; cheap. I'll add.

Let me draft the full code.

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Paragraph splitter — UN document PDF text</title>
<style>
  :root{ --accent:#1f6fb2; --ink:#1c2733; --muted:#5b6b7b; --bg:#f4f6f9; --line:#d9e1ea; --warn-bg:#fdf3e3; --warn-ink:#8a5300; --ok-bg:#e8f4ec; --ok-ink:#1c6b3c; }
  *{box-sizing:border-box}
  body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif;}
  .wrap{max-width:1020px;margin:0 auto;padding:28px 20px 60px;}
  header.top{...}
  h1{font-size:1.5rem;margin:0 0 6px;}
  .sub{color:var(--muted);margin:0 0 4px;}
  a{color:var(--accent);}
  .card{background:#fff;border:1px solid var(--line);border-radius:10px;padding:16px 18px;margin:14px 0;}
  .cards{display:flex;flex-wrap:wrap;gap:12px;}
  .stat{flex:1 1 150px;background:#fff;border:1px solid var(--line);border-radius:10px;padding:12px 14px;}
  .stat .big{font-size:1.9rem;font-weight:700;color:var(--accent);}
  .stat .lbl{font-weight:600;}
  .stat .note{font-size:.85rem;color:var(--muted);margin-top:4px;}
  .how{font-size:.85rem;color:var(--muted);background:#eef3f8;border-left:3px solid var(--accent);padding:8px 12px;border-radius:0 8px 8px 0;margin:8px 0 0;}
  table{width:100%;border-collapse:collapse;background:#fff;}
  th,td{text-align:left;padding:9px 12px;border-bottom:1px solid var(--line);vertical-align:top;}
  th{background:#eef3f8;font-size:.85rem;text-transform:uppercase;letter-spacing:.04em;color:#3c4c5c;}
  tbody tr.data{cursor:pointer;}
  tbody tr.data:hover{background:#f2f7fc;}
  tr.diff{background:var(--warn-bg);}
  tr.diff:hover{background:#fbe9c8;}
  .num{font-weight:700;white-space:nowrap;}
  .firstline{color:#33414f;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;max-width:520px;}
  .badge{display:inline-block;font-size:.78rem;font-weight:600;padding:2px 8px;border-radius:999px;white-space:nowrap;}
  .badge.ok{background:var(--ok-bg);color:var(--ok-ink);}
  .badge.diff{background:#f8e3c0;color:var(--warn-ink);}
  .badge.noref{background:#e8edf3;color:var(--muted);}
  tr.detail td{background:#fbfcfe;}
  .full{white-space:pre-wrap;word-break:break-word;background:#fff;border:1px solid var(--line);border-radius:8px;padding:12px 14px;margin:8px 0;max-height:340px;overflow:auto;}
  .meta{font-size:.9rem;color:var(--muted);}
  .meta b{color:var(--ink);}
  button{background:var(--accent);color:#fff;border:0;border-radius:8px;padding:9px 16px;font-size:1rem;cursor:pointer;}
  button.ghost{background:#fff;color:var(--accent);border:1px solid var(--accent);}
  .toolbar{display:flex;gap:10px;align-items:center;flex-wrap:wrap;margin:14px 0;}
  .notice{background:#fff;border:1px solid var(--line);border-radius:10px;padding:18px;}
  .flag{font-weight:700;}
</style>
```

JS: as planned. Let me write it fully and carefully.

```js
(function(){
"use strict";
var DATA = window.WORKSHOP_DATA || {};
var pdf = DATA.pdf_text;
var container = document.getElementById("app");

function esc(s){ return String(s==null?"":s).replace(/[&<>"']/g, function(c){ return {"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]; }); }

if(!pdf || !Array.isArray(pdf.records) || !pdf.records.length){
  container.innerHTML = '<div class="notice"><h1>No PDF text loaded</h1><p>WORKSHOP_DATA.pdf_text is missing or has no pages, so there is nothing to split.</p></div>';
  return;
}

var symbol = pdf.symbol || "";
var ref = pdf.reference || {};
var pages = pdf.records.slice().sort(function(a,b){ return (Number(a.page)||0) - (Number(b.page)||0); });
var footnoteLimit = (typeof ref.footnotes === "number" && ref.footnotes > 0) ? ref.footnotes : 99;

var MONTHS = "January|February|March|April|May|June|July|August|September|October|November|December";
var symCore = symbol.replace(/[\d\s]/g,"");
function isBoilerplate(line){
  var t = line.replace(/\s+/g," ").trim();
  if(!t) return true;
  if(symCore && t.replace(/[\d\s]/g,"") === symCore) return true;
  if(/^United Nations$/i.test(t)) return true;
  if(/^(Economic and Social Council|General Assembly|Human Rights Council|Security Council|Trusteeship Council|International Court of Justice|Secretariat)$/i.test(t)) return true;
  if(/^(Distr|Distribution|Original|Language|Status)\s*[.:]/i.test(t)) return true;
  if(new RegExp("^\\d{1,2}\\s+(?:MONTHS)\\s+\\d{4}\\.?$","i")... 
```

Careful with building regex with MONTHS — just inline the alternation.

```js
  if(new RegExp("^\\d{1,2}\\s+(?:"+MONTHS+")\\s+\\d{4}\\.?$","i").test(t)) return true;
  if(new RegExp("^(?:"+MONTHS+")\\s+\\d{4}\\.?$","i").test(t)) return true;
  if(/^\d{1,4}$/.test(t)) return true;
  if(/^GE\.\d+/i.test(t)) return true;
  if(/^[-_—]{3,}$/.test(t)) return true;
  return false;
}
```

Wait: `/^\d{1,4}$/` — page numbers. But could a paragraph number line be "1." — has period, safe. Could a footnote number be alone on a line "1" then text next line? Then "1" dropped as page number and text line becomes body... but footnoteMode wouldn't trigger. Edge case, accept.

Hmm, also: what about lines like "E/C.12/GC/27" appearing mid-document as running header — caught by symCore. Also "A/HRC/..." style. Good.

Parse loop:

```js
var paras = [];
var cur = null;
var lastFoot = 0;
var footnoteCount = 0;
pages.forEach(function(p){
  var pageNo = (p.page!=null ? p.page : "?");
  var lines = String(p.text||"").split(/\r?\n/);
  var footnoteMode = false;
  for(var i=0;i<lines.length;i++){
    var raw = lines[i];
    if(isBoilerplate(raw)) continue;
    var t = raw.trim();
    var pm = t.match(/^(\d{1,3})\.\s*(.*)$/);
    if(pm){
      var n = parseInt(pm[1],10);
      if(!cur || n > cur.num){
        cur = { num:n, lines: pm[2] ? [pm[2].trim()] : [], page: pageNo };
        paras.push(cur);
        footnoteMode = false;
        continue;
      }
    }
    if(footnoteMode) continue;
    var fm = t.match(/^(\d{1,2})\s+([A-Za-z(])/);
    if(fm){
      var fn = parseInt(fm[1],10);
      if(fn <= footnoteLimit && fn > lastFoot){
        lastFoot = fn; footnoteCount++; footnoteMode = true; continue;
      }
    }
    if(/^[*†‡§¶]\s+\S/.test(t)){ footnoteCount++; footnoteMode = true; continue; }
    if(cur) cur.lines.push(t);
  }
});
```

Wait, issue: pm matches but n <= cur.num → falls through; then fm check: "3. text" — fm requires digits then \s; "3." → after "3" comes "." not \s → no match. Then asterisk no. Then appended to cur.lines as "3. text". OK.

But another subtle issue: pm with n > cur.num but it's actually a footnote with period? Discussed, accept.

Also: what if the document's paragraphs restart numbering or there are sub-numbers like "12.1"? "12.1 text" → pm matches "12." with remainder "1 text" → paragraph 12 with first line "1 text". Hmm, GCs don't use 12.1. Accept.

Also: what about "1." appearing in preamble before real para 1 (cur null → creates para 1 from preamble)? E.g., a line "1. Introduction" as a section heading? In GCs, "I. Introduction" is roman. But some docs use "1. Introduction" as heading AND paragraph 1 is separate... In E/C.12/GC/27, sections are "I. Introduction", "II. ..." roman. Fine.

Hmm wait, actually there's a risk: heading "II. General obligations" — "II." not digits. OK.

Text/first words:

```js
function flat(p){ return p.lines.join(" ").replace(/\s+/g," ").trim(); }
function firstWords(s,k){ var w = s.split(/\s+/).filter(Boolean); return w.slice(0,k).join(" "); }
function norm(s){ return String(s==null?"":s).replace(/-\s+/g,"-").replace(/\s+/g," ").trim(); }
var refFW = ref.first_words || {};
paras.forEach(function(p){
  p.text = flat(p);
  p.firstLine = p.lines.filter(function(l){return l;})[0] || "";
  var rv = refFW[String(p.num)];
  if(rv==null){ p.status="noref"; p.refWords=""; }
  else {
    var k = Math.max(6, String(rv).split(/\s+/).filter(Boolean).length);
    p.foundWords = firstWords(p.text, k);
    p.refWords = String(rv);
    p.status = (norm(p.foundWords) === norm(p.refWords)) ? "ok" : "diff";
  }
});
var diffs = paras.filter(function(p){return p.status==="diff";}).length;
```

Hmm — firstLine: p.lines may contain "" entries (when number alone on line, I only push pm[2] if non-empty, so lines[0] could be the text). filter(Boolean) picks first non-empty. But I pushed trimmed lines; empty ones only if pm[2] empty — I guarded. Body lines pushed as t (trimmed, non-empty since boilerplate filtered empties). OK.

Wait, one thing: `p.lines.push(t)` — t is trimmed line. Joining with " " for flat. For full display, join with "\n".

Rendering:

```js
var docUrl = pdf.doc_url || "";
var title = pdf.title || "(untitled document)";
var source = pdf.source || "unknown source";
var nPages = pdf.count != null ? pdf.count : pages.length;
```

Header:

```html
<header class="top">
  <h1>Split a UN document into its numbered paragraphs</h1>
  <p class="sub"><b>{esc(title)}</b> — symbol <a href=docUrl target=_blank rel=noopener>{esc(symbol)}</a></p>
  <p class="sub">Data: raw PDF text of this document, {nPages} pages ({pages.length} page records), from {esc(source)}. {adopted? "Adopted: "+esc(ref.adopted)+"." : ""} Reference for checking: {ref.paragraphs} paragraphs, {ref.footnotes} footnotes.</p>
</header>
```

Hmm "one-line description of the data (source, n, years) at the top" — I'll make one line: "Source: {source} · {symbol} · {n} pages of raw PDF text · adopted {adopted}". Years not applicable; adopted year covers it.

Method card ("How this is computed"):

"Each page's raw text is split into lines. Lines that are page furniture are dropped: the document symbol (with or without a page number), the UN masthead ('United Nations', 'Economic and Social Council', …), 'Distr.:'/'Original:' lines, date lines, lone page numbers and rule lines. A new paragraph starts at any line beginning with 'N.' where N is larger than the previous paragraph number. Footnotes — numbered lines ('1 …') at the foot of a page, or lines starting with '*', '†' — are counted separately and kept out of the paragraph text. Nothing is paraphrased: the full text of every paragraph is shown verbatim. All counting is done by this script in your browser; the reference numbers come from WORKSHOP_DATA.pdf_text.reference."

Stats row: 4 stats:
1. Paragraphs found: paras.length — note: "Reference says {ref.paragraphs} — {match? 'match' : 'DIFFERENT'}". 
2. Footnotes kept out: footnoteCount — "Reference: {ref.footnotes}".
3. Paragraphs whose first words differ: diffs — "of {paras.length} found; compared against reference.first_words".
4. Pages: pages.length — "records in WORKSHOP_DATA.pdf_text".

Each stat has its own small note (how computed). Good.

Table + toolbar:

```html
<div class="toolbar">
  <button id="csv">Download CSV</button>
  <button id="expand" class="ghost">Expand all</button>
  <input id="filter" placeholder="Filter by number or text…">
  <span class="meta" id="shown"></span>
</div>
```

Filter: on input, hide rows whose text doesn't include query (case-insensitive), also hide detail rows. Update "shown X of Y".

Table:

```html
<table id="tbl">
<thead><tr><th>#</th><th>Starts on page</th><th>First line</th><th>First words vs reference</th></tr></thead>
<tbody id="tbody"></tbody>
</table>
```

Rows built with DOM or string concat. I'll use string concat with esc() and then attach one click listener on tbody (delegation): find closest tr.data, toggle detail row. Detail row content pre-built in a hidden template? Simpler: on first expand, build detail row and insert after; toggle display. Or always render detail rows hidden (display:none) — with ~50 paragraphs fine. I'll render detail row right after each data row with class "detail" and style display:none; click toggles. Expand all toggles all.

Detail content:

```html
<tr class="detail"><td colspan="4">
  <div class="meta">Paragraph <b>N</b> · starts on page <b>P</b> · source: <a href=docUrl target=_blank>symbol</a></div>
  <div class="full">full text lines joined \n</div>
  <div class="meta">First words found: <b>“found”</b><br>Reference first words: <b>“ref”</b> — status badge</div>
</td></tr>
```

For diff rows, highlight the found vs ref. 

CSV:

```js
function csvCell(v){ v = String(v==null?"":v); return '"' + v.replace(/"/g,'""') + '"'; }
var rows = [["paragraph","starts_on_page","first_words_found","first_words_reference","matches_reference","full_text"]];
paras.forEach(function(p){
  rows.push([p.num, p.page, p.foundWords||"", p.refWords||"", p.status==="ok"?"yes":(p.status==="diff"?"NO":"no reference"), p.lines.join("\n")]);
});
var csv = rows.map(function(r){ return r.map(csvCell).join(","); }).join("\r\n");
```

Add BOM for Excel? "\uFEFF" + csv — helpful. OK.

Download handler with Blob + a.click + revoke.

Also handle ref.paragraphs missing: show "reference not available".

Also the "found vs real" display: big stat "42 found / 42 reference ✓". I'll render: big number = paras.length, note = "The document's reference says {ref.paragraphs}. {paras.length===ref.paragraphs ? "Exact match." : "DIFFERENT — see ⚠ rows."}"

Also mark rows: badge text: ok → "✓ matches", diff → "⚠ differs", noref → "no reference".

Also maybe a summary line above table: "Showing all {paras.length} paragraphs. ⚠ {diffs} differ from the reference first words."

Empty states: if paras.length===0 → notice "No numbered paragraphs found — check the cleaning rules above."

Let me also double check the "first line" column: user said "a table with each paragraph's number and first line". I include # and first line; adding page + status is bonus. Good.

Now, about `pdf.count` — description says `{title, symbol, doc_url, source, count, records}`; count likely = number of pages. I'll show "n = {count} pages" and if records.length differs, show both.

Also top description must include years? "source, n, years" — pdf_text has no years field; I'll include adopted year from reference if present: "adopted {ref.adopted}". If missing, omit. Fine.

Line count: keep under ~700 lines. Should be ~350-450 lines. Good.

Let me also consider: should I use Chart.js? No charts needed. The instructions say use Chart.js for charts — only if charts exist. Skip.

One more requirement check: "Every row that shows a document has its symbol, linked to doc_url in a new tab." — header shows symbol→doc_url; each detail row also shows symbol→doc_url. Table rows are paragraphs, not documents, but detail includes it. Good.

"Never call studio.ask on page load" — not used at all. Good.

"handle empty lists and missing values" — done.

Now write final code meticulously. I'll be careful with regex escaping in JS strings.

Also: the filter input — when filtering, detail rows should hide too. I'll give each pair a data-key attribute; on filter, iterate tbody children.

Implementation of render:

```js
var tbody = document.getElementById("tbody");
var html = "";
paras.forEach(function(p, idx){
  var badge = p.status==="ok" ? '<span class="badge ok">✓ matches</span>'
    : p.status==="diff" ? '<span class="badge diff">⚠ differs</span>'
    : '<span class="badge noref">no reference</span>';
  html += '<tr class="data' + (p.status==="diff" ? " diff" : "") + '" data-idx="' + idx + '">'
    + '<td class="num">' + p.num + '</td>'
    + '<td>' + esc(p.page) + '</td>'
    + '<td class="firstline" title="' + esc(p.firstLine) + '">' + esc(p.firstLine) + '</td>'
    + '<td>' + badge + '</td></tr>';
  html += '<tr class="detail" data-idx="' + idx + '" style="display:none"><td colspan="4">'
    + '<div class="meta">Paragraph <b>' + p.num + '</b> · starts on page <b>' + esc(p.page) + '</b> · document: <a href="' + esc(docUrl) + '" target="_blank" rel="noopener">' + esc(symbol) + '</a></div>'
    + '<div class="full">' + esc(p.lines.join("\n")) + '</div>'
    + '<div class="meta">First words found (this script): <b>' + esc(p.foundWords || firstWords(p.text,6)) + '</b><br>'
    + 'Reference first words: <b>' + esc(p.refWords || "(none)") + '</b><br>'
    + 'Comparison: ' + badge + '</div>'
    + '</td></tr>';
});
tbody.innerHTML = html;
```

Click delegation:

```js
tbody.addEventListener("click", function(e){
  var tr = e.target.closest("tr.data");
  if(!tr) return;
  var idx = tr.getAttribute("data-idx");
  var det = tbody.querySelector('tr.detail[data-idx="' + idx + '"]');
  if(det) det.style.display = det.style.display === "none" ? "" : "none";
});
```

Expand all button toggles: track state; set all details display "" and button text "Collapse all", or reverse.

Filter:

```js
document.getElementById("filter").addEventListener("input", function(){
  var q = this.value.trim().toLowerCase();
  var shown = 0;
  paras.forEach(function(p, idx){
    var hay = (p.num + " " + p.text).toLowerCase();
    var show = !q || hay.indexOf(q) !== -1;
    if(show) shown++;
    var d = tbody.querySelector('tr.data[data-idx="'+idx+'"]');
    var det = tbody.querySelector('tr.detail[data-idx="'+idx+'"]');
    if(d) d.style.display = show ? "" : "none";
    if(det && show && det.dataset.open === "1") det.style.display = "";
    else if(det) det.style.display = "none";
  });
  document.getElementById("shown").textContent = "Showing " + shown + " of " + paras.length + " paragraphs";
});
```

Hmm, detail open state tracking: simpler — when filtering, hide all details unless... let me track open set: `var open = {}`. On click toggle open[idx]. On filter, detail display = show && open[idx] ? "" : "none". Let me implement with open object.

CSV button:

```js
document.getElementById("csv").addEventListener("click", function(){
  var rows = [["paragraph","starts_on_page","first_words_found","first_words_reference","matches_reference","full_text"]];
  paras.forEach(function(p){
    rows.push([String(p.num), String(p.page), p.foundWords || firstWords(p.text,6), p.refWords || "", p.status==="ok"?"yes":(p.status==="diff"?"NO":"no reference"), p.lines.join("\n")]);
  });
  var csv = "\uFEFF" + rows.map(function(r){ return r.map(function(c){ c=String(c==null?"":c); return '"' + c.replace(/"/g,'""') + '"'; }).join(","); }).join("\r\n");
  var blob = new Blob([csv], {type:"text/csv;charset=utf-8"});
  var a = document.createElement("a");
  a.href = URL.createObjectURL(blob);
  a.download = (symbol ? symbol.replace(/[^\w.-]+/g,"_") : "document") + "_paragraphs.csv";
  document.body.appendChild(a); a.click();
  setTimeout(function(){ URL.revokeObjectURL(a.href); a.remove(); }, 500);
});
```

Stats rendering — build via innerHTML into #stats.

Header — build into #head.

Also note near table: "How this is computed: rows are the paragraphs found by the rules above, in document order. 'First line' is the first non-empty line of the cleaned paragraph. Click any row for the full verbatim text. ⚠ marks rows whose first six words differ from reference.first_words."

Also a note about CSV: "CSV columns: paragraph, page, first words found, reference first words, match, full text (verbatim, line breaks preserved)."

Edge: ref.first_words keys — use String(p.num). refFW may be object with numeric keys — JS object keys are strings anyway.

Also handle ref.paragraphs undefined: `var refParas = (typeof ref.paragraphs === "number") ? ref.paragraphs : null;`

Now assemble everything. Also add `<noscript>`? Not needed.

Let me also make sure no horizontal scrolling: .firstline has max-width and ellipsis; table-layout fixed? I'll set `table{table-layout:fixed}` with column widths: # 60px, page 90px, firstline auto, badge 130px. With table-layout fixed, firstline cell needs overflow hidden — set on td. Let me set widths via colgroup or th styles. Use `th:nth-child(1){width:56px}` etc. And `.firstline{overflow:hidden;text-overflow:ellipsis;white-space:nowrap;}` — with table-layout fixed this works.

Detail row colspan=4 fine.

Font sizes: base 16px set on body. Big stat 1.9rem ok.

Let me now also double-check the paragraph regex against a tricky case: a line like "10. The Committee..." → pm matches n=10. Good. A line "2." alone → matches, remainder "". Good.

What about lines with leading spaces? I trim first (t = raw.trim()), then match ^(\d{1,3})\. — good.

What about a paragraph number with more than 3 digits? No.

What about "0."? n=0, cur null → creates para 0? `!cur || n > cur.num` — cur null → creates para 0. Unlikely; fine.

Potential issue: the monotonic check `n > cur.num` — if extraction duplicates a page (same page twice), paragraphs would repeat with same numbers → second occurrence n == cur.num → not > → falls through, appended as body text to the previous paragraph. Hmm, that would duplicate text into previous para. But pages sorted; duplicates unlikely. Alternatively accept n >= cur.num? No — keep strict.

Wait, actually there's a subtle issue: what if a paragraph number appears at the start of a line due to wrapping, like "...resolution\n3. ..." — that IS a new paragraph. Fine.

Another: footnote lines like "2 The ..." where 2 ≤ lastFoot (already seen footnote 2)? Can't happen since footnotes increase. If numbering restarts per page (some docs restart footnotes each page with superscript per page?) — UN GCs use continuous numbering. If restart happened, fn > lastFoot fails → footnote treated as body → pollutes paragraph and footnote count low. The found-vs-reference display reveals it. Acceptable.

Hmm, actually, let me reconsider: maybe allow fn <= lastFoot if... no. Keep.

One more improvement: also treat lines matching /^\s*\d{1,2}\s+[A-Za-z]/ as footnote candidates ONLY when they occur after the last paragraph-start line of the page? No wait — footnotes occur after body text, and body text is within paragraphs... the last paragraph on the page started earlier. So footnote candidates are always after the last paraStart of the page — but so are all body lines. Doesn't discriminate. Keep current approach.

Actually, one more discriminator I can add cheaply: footnote blocks usually follow a blank line. In the raw page text, there's often an empty line before footnotes. I could require: the previous non-boilerplate line was blank OR it's the first content line of the page? Hmm, extraction may or may not preserve. I'll add a soft check: candidate accepted if (previous kept line was blank) OR (fn === lastFoot + 1)? No... Let me not over-constrain; current heuristics + honest reporting suffice.

Let me also count "footnotes found" — I count footnote starts. Also maybe count footnote lines? Reference says "how many footnotes" — starts is right.

Now, the top description line: "Source: {pdf.source} · {symbol} · n = {count} pages of raw PDF text · adopted {ref.adopted}". Also mention doc_url link. Let me write:

```html
<p class="sub">Document: <b>{title}</b> — <a href="{docUrl}" target="_blank" rel="noopener">{symbol}</a> (opens the UN document in a new tab)</p>
<p class="sub">Data: raw PDF text of this one document, page by page — source: {source}, n = {count} pages ({records.length} page records){adopted}. Reference for checking: {refParas} paragraphs, {refFoot} footnotes.</p>
```

OK. Writing final file now. I'll aim for clean, complete code.

Also remember: before the code block, at most three short sentences describing what I built; after the code block, nothing.

Let me write out the whole HTML now, carefully checking syntax.

Also — one more thought on `isBoilerplate` date regex: "6 November 2025" matches ^\d{1,2}\s+MONTHS\s+\d{4}\.?$ — good. Also possible "6 November 2025 " trailing space — trimmed. Also "November 2025" second regex. Also headers like "Distr.: General" — my regex /^(Distr|Distribution|Original|Language|Status)\s*[.:]/i — "Distr.:" → "Distr" + "." matches [.:] — yes. "Original: English" → "Original" + ":" ok.

Also possible header "E/C.12/GC/27" with trailing spaces — trimmed, symCore compare ok.

Also "Advance version"? Some docs have "Distr.: General ... Advance unedited version" — covered by Distr prefix.

Also possible line "United Nations" with extra words "United Nations Economic and Social Council"? My exact-match list wouldn't catch combined. Add: /^United Nations\b/ → if line starts with "United Nations" and length < 60? Hmm, body could say "United Nations" at line start... e.g., "United Nations human rights system..." as a wrapped line start? Possible! Exact match only is safer. But header "United Nations" is exact. Keep exact matches, plus maybe /^United Nations\s+(Economic and Social Council|General Assembly|...)$/ combined. I'll add a combined pattern: /^United Nations\s+(Economic and Social Council|General Assembly|Human Rights Council|Security Council)$/i.

Also committee name line "Committee on Economic, Social and Cultural Rights" appears on page 1 only (title block) — dropped because cur is null (preamble). But if it appeared on later pages (running header), it'd pollute. Add to boilerplate? It's doc-specific; generic approach: lines before first paragraph are dropped anyway; running headers on later pages would be a problem. Common running headers are symbol/masthead/date — covered. I'll also drop lines matching /^(Committee on|Human Rights Council|General Assembly)\b.*$/ ? Too aggressive — body text could start "Committee on ..."? Body lines starting with "Committee" happen ("Committee recommends..."). Hmm, but exact "Committee on Economic, Social and Cultural Rights" — I could drop lines that exactly equal common committee names? Overkill. The preamble-drop handles page 1. For later pages, UN GC running headers are just symbol + page number typically. Accept.

Now, also think: what if the first page's title block contains a line starting with digits+period? E.g., "General comment No. 27 (2025)..." — starts with "General". OK.

Alright, also the sample page 1 ends with footnote "* ..." presumably. Our asterisk rule catches it.

Let me also handle `p.text` used for filter — fine.

Write the code:

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Numbered-paragraph splitter — UN document raw PDF text</title>
<style>
:root{
  --accent:#1f6fb2; --ink:#1d2b38; --muted:#5c6c7c; --bg:#f4f6f9;
  --line:#d8e0e9; --ok-bg:#e6f3ea; --ok-ink:#1d6b3a;
  --warn-bg:#fdf1de; --warn-ink:#8a5300; --warn-line:#f0d9b0;
}
*{box-sizing:border-box}
html,body{margin:0;padding:0}
body{background:var(--bg);color:var(--ink);font:16px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif}
.wrap{max-width:1040px;margin:0 auto;padding:26px 18px 64px}
h1{font-size:1.45rem;line-height:1.25;margin:0 0 8px}
h2{font-size:1.05rem;margin:0 0 8px}
.sub{margin:2px 0;color:var(--muted)}
a{color:var(--accent)}
.card{background:#fff;border:1px solid var(--line);border-radius:10px;padding:16px 18px;margin:14px 0}
.how{font-size:.86rem;color:var(--muted);background:#edf3f9;border-left:3px solid var(--accent);padding:8px 12px;border-radius:0 8px 8px 0;margin-top:10px}
.stats{display:flex;flex-wrap:wrap;gap:12px;margin:14px 0}
.stat{flex:1 1 160px;background:#fff;border:1px solid var(--line);border-radius:10px;padding:12px 14px}
.stat .big{font-size:1.8rem;font-weight:700;color:var(--accent);line-height:1.1}
.stat .lbl{font-weight:600;margin-top:2px}
.stat .note{font-size:.83rem;color:var(--muted);margin-top:5px}
.stat.warn .big{color:var(--warn-ink)}
.stat.warn{border-color:var(--warn-line);background:var(--warn-bg)}
.toolbar{display:flex;gap:10px;align-items:center;flex-wrap:wrap;margin:16px 0 10px}
button{background:var(--accent);color:#fff;border:0;border-radius:8px;padding:9px 16px;font-size:.95rem;cursor:pointer}
button.ghost{background:#fff;color:var(--accent);border:1px solid var(--accent)}
input[type=search]{padding:8px 12px;border:1px solid var(--line);border-radius:8px;font-size:.95rem;min-width:220px}
table{width:100%;border-collapse:collapse;background:#fff;border:1px solid var(--line);table-layout:fixed}
th,td{padding:9px 12px;border-bottom:1px solid var(--line);text-align:left;vertical-align:top;font-size:.95rem}
th{background:#edf3f9;font-size:.78rem;text-transform:uppercase;letter-spacing:.05em;color:#3d4d5d}
th.c-num{width:58px} th.c-page{width:96px} th.c-badge{width:132px}
tbody tr.data{cursor:pointer}
tbody tr.data:hover{background:#f1f7fc}
tr.data.diff{background:var(--warn-bg)}
tr.data.diff:hover{background:#fae8c8}
td.num{font-weight:700}
td.firstline{overflow:hidden;text-overflow:ellipsis;white-space:nowrap;color:#33424f}
.badge{display:inline-block;font-size:.76rem;font-weight:700;padding:2px 9px;border-radius:999px;white-space:nowrap}
.badge.ok{background:var(--ok-bg);color:var(--ok-ink)}
.badge.diff{background:#f6dfae;color:var(--warn-ink)}
.badge.noref{background:#e7edf3;color:var(--muted)}
tr.detail td{background:#fbfcfe}
.full{white-space:pre-wrap;word-break:break-word;background:#fff;border:1px solid var(--line);border-radius:8px;padding:12px 14px;margin:10px 0;max-height:360px;overflow:auto;font-size:.93rem}
.meta{font-size:.88rem;color:var(--muted)}
.meta b{color:var(--ink)}
.notice{background:#fff;border:1px solid var(--line);border-radius:10px;padding:20px}
footer{margin-top:22px;color:var(--muted);font-size:.85rem}
</style>
</head>
<body>
<div class="wrap">
  <div id="head"></div>
  <div id="stats"></div>
  <div class="card">
    <h2>How this is computed</h2>
    <div id="method"></div>
  </div>
  <div class="toolbar">
    <button id="csvBtn" type="button">Download CSV</button>
    <button id="toggleAll" type="button" class="ghost">Expand all</button>
    <input id="filter" type="search" placeholder="Filter by number or text…">
    <span class="meta" id="shown"></span>
  </div>
  <div class="card" style="padding:0;overflow:hidden">
    <table>
      <thead><tr><th class="c-num">¶</th><th class="c-page">Page</th><th>First line of the paragraph</th><th class="c-badge">First words vs reference</th></tr></thead>
      <tbody id="tbody"></tbody>
    </table>
  </div>
  <div class="how" id="tableNote"></div>
  <footer>All counting, filtering and sorting is done by this script in your browser from <code>window.WORKSHOP_DATA.pdf_text</code>. No data leaves the page; no model is called.</footer>
</div>
<script>
...
</script>
</body>
</html>
```

Wait — the card with table has padding 0 and overflow hidden — fine.

Now the script. Let me write it fully:

```js
(function(){
"use strict";
var DATA = window.WORKSHOP_DATA || {};
var pdf = DATA.pdf_text || null;
var head = document.getElementById("head");
var stats = document.getElementById("stats");
var tbody = document.getElementById("tbody");

function esc(s){
  return String(s==null?"":s).replace(/[&<>"']/g,function(c){
    return {"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c];
  });
}

if(!pdf || !Array.isArray(pdf.records) || pdf.records.length===0){
  head.innerHTML = '<h1>Numbered-paragraph splitter</h1><p class="sub">No PDF text is loaded: <code>WORKSHOP_DATA.pdf_text</code> is missing or has no page records, so there is nothing to split.</p>';
  stats.innerHTML = "";
  document.querySelector(".toolbar").style.display = "none";
  document.querySelector("table").style.display = "none";
  return;
}

var symbol = pdf.symbol || "";
var docUrl = pdf.doc_url || "";
var title = pdf.title || "(untitled)";
var source = pdf.source || "unknown source";
var ref = pdf.reference || {};
var refParas = (typeof ref.paragraphs === "number") ? ref.paragraphs : null;
var refFoots = (typeof ref.footnotes === "number") ? ref.footnotes : null;
var refFW = (ref.first_words && typeof ref.first_words === "object") ? ref.first_words : {};
var pages = pdf.records.slice().sort(function(a,b){ return (Number(a && a.page)||0) - (Number(b && b.page)||0); });
var nPages = (typeof pdf.count === "number") ? pdf.count : pages.length;
var footnoteLimit = (refFoots && refFoots > 0) ? refFoots : 99;

var MONTHS = "January|February|March|April|May|June|July|August|September|October|November|December";
var symCore = symbol.replace(/[\d\s]/g,"");

function isBoilerplate(line){
  var t = line.replace(/\s+/g," ").trim();
  if(!t) return true;
  if(symCore && t.replace(/[\d\s]/g,"") === symCore) return true;
  if(/^United Nations$/i.test(t)) return true;
  if(/^United Nations\s+(Economic and Social Council|General Assembly|Human Rights Council|Security Council|Trusteeship Council)$/i.test(t)) return true;
  if(/^(Economic and Social Council|General Assembly|Human Rights Council|Security Council|Trusteeship Council|International Court of Justice|Secretariat)$/i.test(t)) return true;
  if(/^(Distr|Distribution|Original|Language|Status)\s*[.:]/i.test(t)) return true;
  if(new RegExp("^\\d{1,2}\\s+(?:"+MONTHS+")\\s+\\d{4}\\.?$","i").test(t)) return true;
  if(new RegExp("^(?:"+MONTHS+")\\s+\\d{4}\\.?$","i").test(t)) return true;
  if(/^\d{1,4}$/.test(t)) return true;
  if(/^GE\.\d+/i.test(t)) return true;
  if(/^[-_—]{3,}$/.test(t)) return true;
  return false;
}

var paras = [];
var cur = null;
var lastFoot = 0;
var footnoteCount = 0;

pages.forEach(function(p){
  var pageNo = (p && p.page != null) ? p.page : "?";
  var lines = String((p && p.text) || "").split(/\r?\n/);
  var footnoteMode = false;
  for(var i=0;i<lines.length;i++){
    if(isBoilerplate(lines[i])) continue;
    var t = lines[i].trim();
    var pm = t.match(/^(\d{1,3})\.\s*(.*)$/);
    if(pm){
      var n = parseInt(pm[1],10);
      if(!cur || n > cur.num){
        cur = { num:n, lines: pm[2] ? [pm[2].trim()] : [], page: pageNo };
        paras.push(cur);
        footnoteMode = false;
        continue;
      }
    }
    if(footnoteMode) continue;
    var fm = t.match(/^(\d{1,2})\s+([A-Za-z(])/);
    if(fm){
      var fn = parseInt(fm[1],10);
      if(fn <= footnoteLimit && fn > lastFoot){
        lastFoot = fn;
        footnoteCount++;
        footnoteMode = true;
        continue;
      }
    }
    if(/^[*†‡§¶]\s+\S/.test(t)){
      footnoteCount++;
      footnoteMode = true;
      continue;
    }
    if(cur) cur.lines.push(t);
  }
});

function flat(p){ return p.lines.join(" ").replace(/\s+/g," ").trim(); }
function firstWords(s,k){ return String(s||"").split(/\s+/).filter(Boolean).slice(0,k).join(" "); }
function norm(s){ return String(s==null?"":s).replace(/-\s+/g,"-").replace(/\s+/g," ").trim(); }

paras.forEach(function(p){
  p.text = flat(p);
  p.firstLine = p.lines.filter(function(l){ return l && l.trim(); })[0] || "";
  var rv = refFW[String(p.num)];
  if(rv == null){
    p.status = "noref"; p.foundWords = firstWords(p.text,6); p.refWords = "";
  } else {
    p.refWords = String(rv);
    var k = Math.max(6, p.refWords.split(/\s+/).filter(Boolean).length);
    p.foundWords = firstWords(p.text, k);
    p.status = (norm(p.foundWords) === norm(p.refWords)) ? "ok" : "diff";
  }
});

var diffs = paras.filter(function(p){ return p.status==="diff"; }).length;
```

Header render:

```js
var adoptedTxt = ref.adopted ? " · adopted " + esc(ref.adopted) : "";
head.innerHTML =
  '<h1>Split a UN document into its numbered paragraphs</h1>' +
  '<p class="sub"><b>' + esc(title) + '</b> — symbol <a href="' + esc(docUrl) + '" target="_blank" rel="noopener">' + esc(symbol || "(no symbol)") + '</a> (opens the UN document in a new tab)</p>' +
  '<p class="sub">Data: the raw PDF text of this one document, page by page — source: ' + esc(source) + ', n = ' + nPages + ' pages (' + pages.length + ' page records)' + adoptedTxt + '. Reference for checking: ' +
  (refParas!=null ? refParas + " paragraphs" : "no paragraph count") + ', ' +
  (refFoots!=null ? refFoots + " footnotes" : "no footnote count") + '.</p>';
```

Method text:

```js
document.getElementById("method").innerHTML =
  "<p style='margin:0 0 6px'>Each page's raw text is split into lines. Page furniture is dropped: the document symbol (with or without a page number), the UN masthead lines, <i>Distr.:</i> / <i>Original:</i> lines, date lines, lone page numbers and rule lines. A new paragraph starts at any line that begins with <b>“N.”</b> where N is larger than the previous paragraph number. Footnotes — lines at the foot of a page that begin with a number (“1 …”) or with “*” — are counted separately and kept out of the paragraph text. Nothing is paraphrased: every paragraph is shown verbatim.</p>" +
  '<div class="how">All counting is done by this script in your browser, deterministically, from <code>window.WORKSHOP_DATA.pdf_text</code>. The “reference” numbers come from <code>pdf_text.reference</code> that ships with the data.</div>';
```

Stats:

```js
function stat(big, lbl, note, warn){
  return '<div class="stat' + (warn ? " warn" : "") + '"><div class="big">' + big + '</div><div class="lbl">' + lbl + '</div><div class="note">' + note + '</div></div>';
}
var paraNote = refParas!=null
  ? "Reference says " + refParas + " — " + (paras.length === refParas ? "exact match ✓" : "DIFFERENT ⚠")
  : "No reference count in the data";
stats.innerHTML = '<div class="stats">' +
  stat(paras.length, "paragraphs found", "Counted by this script: lines starting with “N.” (N increasing). " + paraNote, refParas!=null && paras.length!==refParas) +
  stat(footnoteCount, "footnotes kept out", "Counted by this script: numbered or “*” lines at the foot of a page. " + (refFoots!=null ? "Reference says " + refFoots + (footnoteCount===refFoots ? " — exact match ✓" : " — DIFFERENT ⚠") : "No reference count."), refFoots!=null && footnoteCount!==refFoots) +
  stat(diffs, "paragraphs differing from reference", "First words of each found paragraph compared with pdf_text.reference.first_words. Of " + paras.length + " found.", diffs>0) +
  stat(pages.length, "pages of raw text", "Records in pdf_text.records (n = " + nPages + " in the data header).") +
  '</div>';
```

Table note:

```js
document.getElementById("tableNote").textContent = "";
document.getElementById("tableNote").innerHTML = "How this table is computed: rows are the paragraphs found by the rules above, in document order. “First line” is the first non-empty line of the cleaned paragraph. The badge compares the first six words of the paragraph with reference.first_words — ⚠ means they differ. Click any row to see the full verbatim paragraph text. The CSV download contains the same rows: paragraph, page, first words found, reference first words, match, full text.";
```

Table body:

```js
var html = "";
paras.forEach(function(p, idx){
  var badge = p.status==="ok" ? '<span class="badge ok">✓ matches</span>'
            : p.status==="diff" ? '<span class="badge diff">⚠ differs</span>'
            : '<span class="badge noref">no reference</span>';
  html += '<tr class="data' + (p.status==="diff" ? " diff" : "") + '" data-idx="' + idx + '">'
       +  '<td class="num">' + p.num + '</td>'
       +  '<td>' + esc(p.page) + '</td>'
       +  '<td class="firstline" title="' + esc(p.firstLine) + '">' + esc(p.firstLine) + '</td>'
       +  '<td>' + badge + '</td></tr>';
  html += '<tr class="detail" data-idx="' + idx + '" style="display:none"><td colspan="4">'
       +  '<div class="meta">Paragraph <b>' + p.num + '</b> · starts on page <b>' + esc(p.page) + '</b> · document: <a href="' + esc(docUrl) + '" target="_blank" rel="noopener">' + esc(symbol) + '</a></div>'
       +  '<div class="full">' + esc(p.lines.join("\n")) + '</div>'
       +  '<div class="meta">First words found by this script: <b>' + esc(p.foundWords) + '</b><br>'
       +  'Reference first words: <b>' + esc(p.refWords || "(none in reference)") + '</b><br>'
       +  'Comparison: ' + badge + '</div>'
       +  '</td></tr>';
});
tbody.innerHTML = html || '<tr><td colspan="4">No numbered paragraphs were found in the raw text — the cleaning rules above may need adjusting for this document.</td></tr>';
```

Interactions:

```js
var open = {};
tbody.addEventListener("click", function(e){
  var tr = e.target.closest ? e.target.closest("tr.data") : null;
  if(!tr) return;
  var idx = tr.getAttribute("data-idx");
  var det = tbody.querySelector('tr.detail[data-idx="' + idx + '"]');
  if(!det) return;
  open[idx] = !open[idx];
  det.style.display = open[idx] ? "" : "none";
});

var allOpen = false;
document.getElementById("toggleAll").addEventListener("click", function(){
  allOpen = !allOpen;
  paras.forEach(function(p, idx){
    open[idx] = allOpen;
    var det = tbody.querySelector('tr.detail[data-idx="' + idx + '"]');
    if(det) det.style.display = allOpen ? "" : "none";
  });
  this.textContent = allOpen ? "Collapse all" : "Expand all";
});

document.getElementById("filter").addEventListener("input", function(){
  var q = this.value.trim().toLowerCase();
  var shown = 0;
  paras.forEach(function(p, idx){
    var hay = (p.num + " " + p.text).toLowerCase();
    var show = !q || hay.indexOf(q) !== -1;
    if(show) shown++;
    var d = tbody.querySelector('tr.data[data-idx="' + idx + '"]');
    var det = tbody.querySelector('tr.detail[data-idx="' + idx + '"]');
    if(d) d.style.display = show ? "" : "none";
    if(det) det.style.display = (show && open[idx]) ? "" : "none";
  });
  document.getElementById("shown").textContent = "Showing " + shown + " of " + paras.length + " paragraphs";
});
document.getElementById("shown").textContent = "Showing " + paras.length + " of " + paras.length + " paragraphs";
```

CSV:

```js
document.getElementById("csvBtn").addEventListener("click", function(){
  var rows = [["paragraph","starts_on_page","first_words_found","first_words_reference","matches_reference","full_text_verbatim"]];
  paras.forEach(function(p){
    rows.push([String(p.num), String(p.page), p.foundWords, p.refWords,
      p.status==="ok" ? "yes" : (p.status==="diff" ? "NO" : "no reference"),
      p.lines.join("\n")]);
  });
  var csv = "\uFEFF" + rows.map(function(r){
    return r.map(function(c){
      c = String(c==null ? "" : c);
      return '"' + c.replace(/"/g,'""') + '"';
    }).join(",");
  }).join("\r\n");
  var blob = new Blob([csv], {type:"text/csv;charset=utf-8"});
  var a = document.createElement("a");
  a.href = URL.createObjectURL(blob);
  a.download = (symbol ? symbol.replace(/[^\w.-]+/g,"_") : "document") + "_paragraphs.csv";
  document.body.appendChild(a);
  a.click();
  setTimeout(function(){ URL.revokeObjectURL(a.href); a.remove(); }, 600);
});
```

Check: `e.target.closest` — fine in modern browsers.

One concern: `tbody.innerHTML = html` with detail rows — clicking a link inside detail row? Detail rows aren't tr.data so closest("tr.data") returns null when clicking inside detail — good, links work.

Also the `title` attribute on firstline cell with esc — esc escapes quotes as &quot; — good for attribute.

Also `esc(p.page)` — page may be number; esc handles via String().

Potential issue: `pm` regex on t after trim: `/^(\d{1,3})\.\s*(.*)$/` — for "1." → pm[2]="" → lines=[] then body lines appended. Good. For "71. The Committee..." → pm[2]="The Committee...". Good.

But wait: what about a line like "2030." — checked, no match. "Art. 3." mid-line — anchored, no.

What about lines like "12.34"? pm: \d{1,3}="12", then "." matches, remainder "34" → treated as paragraph 12 with first line "34"! Hmm — "12.34" could appear in text (a resolution number "12/34"? or decimal). At line start after wrap... possible but rare. Could add guard: remainder shouldn't start with a digit? If pm[2] starts with a digit, it's likely not a paragraph start (paragraph text starts with a letter usually, but could start with a digit e.g. "3. 2030 is..."). Hmm. Trade-off. Paragraph text CAN start with a digit ("12. 47 members..."). But "12.34" as a wrapped line start is also plausible. I'll add guard: if pm[2] matches /^\d/ AND the line has no space after the period (i.e., "12.34" no space) → treat as body. Actually pm regex `\.\s*(.*)` — "12.34" → after "." no space, remainder "34". "12. 34" → remainder "34" with space. Distinguish: require either end-of-line or whitespace after the period: change regex to /^(\d{1,3})\.(?:\s+(.*))?$/ — then "12.34" doesn't match (no whitespace after period, and not end). "1." matches with pm[2] undefined. "71. The..." matches. "12. 34" matches with remainder "34" — still a false positive but rarer. Good improvement:

`var pm = t.match(/^(\d{1,3})\.(?:\s+(.*))?$/);`

Then pm[2] may be undefined → lines = pm[2] ? [pm[2].trim()] : [].

Similarly footnote regex requires \s+ after digits — "1.See" won't match footnote (has period). Good.

Also the fm regex `/^(\d{1,2})\s+([A-Za-z(])/` — "1 See" ok; "1 000" → second char after space is "0" → no match. Good. But "1 (a)" would match — footnote starting with parenthesis? eh fine.

Hmm, also what about footnote lines like "10 See para..." — \d{1,2} matches "10". Good.

One more: the asterisk footnote check `/^[*†‡§¶]\s+\S/` — a body line starting with "* " as a bullet would falsely start footnote mode. In GCs, bullets are "(a)" or "–". Accept.

Also: what if footnoteMode triggers on the LAST content line of a page and the next page starts with a new paragraph — fine, footnoteMode resets per page.

What if a page has footnotes in the middle (two-column layout)? Not for UN docs. Fine.

Now — the "first line" column: for paragraph where number is on its own line, firstLine = first text line. Good.

Also I should double check: `p.lines.filter(...)` — lines are trimmed strings; empty string possible only if pm[2] was "" — guarded by `pm[2] ? ...`. Body pushes t which is non-empty (boilerplate filtered empties). OK.

Also: what if the same paragraph number appears legitimately twice (e.g., doc has "1." in an annex)? Monotonic drops it into previous para as body line "1. ..." — hmm, that line would be appended to previous paragraph's text. Slight pollution; acceptable.

Now the header "n = X pages" — also mention years? pdf_text has no year; adopted covers. Fine.

Also requirement: "a clear title, a one-line description of the data (source, n, years) at the top" — my sub line: "Data: the raw PDF text of this one document, page by page — source: X, n = 20 pages (20 page records) · adopted 2025." Good enough.

Let me also double-check the stats "warn" logic and that `stat()` escapes — I pass numbers and pre-escaped strings; paraNote includes refParas number — safe. OK.

Also the toolbar/table hidden when no data — I query ".toolbar" and "table" — they exist. OK.

Also `document.getElementById("tableNote")` — set innerHTML. Fine.

Check line count — roughly 300 lines. Good.

One more requirement: "Show how many paragraphs it found next to the number the document really has" — stat card 1 shows big "found" with note "Reference says N — exact match/DIFFERENT". Maybe make it more explicit: big shows "42 / 42"? I'll make big = paras.length + (refParas!=null ? " / " + refParas : "") and label "paragraphs found / reference". That's literally "next to". Let me do: big = paras.length + (refParas!=null ? " / " + refParas : ""), lbl = "found / reference". Note explains. Similarly footnotes: big = footnoteCount + (refFoots!=null ? " / " + refFoots : ""), lbl "footnotes found / reference". 

Also add a line above the table summarizing mismatches: I'll put in tableNote or a small line in toolbar area — the "shown" span covers count; add mismatch info to tableNote text (already mentions ⚠). Also maybe a stat card 3 covers it. Good.

Also: "mark every paragraph whose first words differ from the reference" — diff rows highlighted + badge ⚠. ✓.

"Clicking a row shows the full paragraph" ✓.

"Let me download the result as CSV" ✓.

Also ensure the page works if `ref` missing entirely: refParas null etc. — handled.

Also if `pdf.records` items lack text — String(p.text||"") handled.

I think there's one more subtlety: `symCore` when symbol empty → "" → falsy → skip check. Good.

Also `isBoilerplate` pure-digit line /^\d{1,4}$/ — what if a paragraph number line lost its period in extraction ("1" alone)? Then dropped as page number and text merges into previous para. Can't help; reference check will flag.

Edge: what if the document uses "1 ," or "1)" style? Not our case.

Now, also the requirement about rows showing documents with symbol+doc_url: header + each detail row. ✓.

Also "readable at projector distance (base font 16px)" ✓.

Let me also add `lang="en"`, meta viewport ✓.

Double-check no external resources: no links loaded as resources; anchors are fine (they're navigation, not resource loads). No fetch. ✓.

Chart.js not used — no charts. That's allowed ("Use it for charts" — only if charts).

Now finalize the code text. Also ensure I don't use `closest` on old browsers — fine.

One more check on the regex string in JS: `new RegExp("^\\d{1,2}\\s+(?:"+MONTHS+")\\s+\\d{4}\\.?$","i")` — MONTHS contains "|" — fine inside (?:...).

Also `/^[-_—]{3,}$/` — em dash included.

Write final answer: 2-3 sentences before the code block, then the html block, nothing after.

Let me also reconsider the paragraph-start regex once more with the sample: line "1." → t="1." → match /^(\d{1,3})\.(?:\s+(.*))?$/ → "1" + "." + end → pm[2] undefined → lines=[]. Next line "A clean, healthy..." → not pm, not footnote (starts with "A"), cur exists → push. 

But wait — footnote check happens before push: "A clean..." — fm regex needs digits at start → no. asterisk → no. push. ✓.

Line "sustainable development*" (title, cur null) → dropped since cur null... wait, order: pm no; footnoteMode false; fm no; asterisk regex: t starts with "sustainable" not "*" → no; `if(cur) cur.lines.push(t)` — cur null → dropped. ✓.

Footnote line at bottom e.g. "* See footnote..." → asterisk match → footnoteCount++, footnoteMode=true. ✓. But careful: what if the title's last line "sustainable development*" is followed by footnote text on the SAME line? Extraction usually separate. Fine.

What about a body line that begins with "*" like "* * *"? /^\*+\s*$/ — my rule requires \s+\S after; "* * *" → after first "*" comes " * *" — \s+ then \S="*" → matches → footnoteMode. "* * *" separators are usually caught by the rule-line regex? /^[-_—]{3,}$/ doesn't include "*". Add /^\*+$/ and /^\*\s*\*\s*\*+$/ to boilerplate. I'll add /^\*+(\s*\*+)*$/ → boilerplate. Minor; add `/^[\*\s]{3,}$/`? That could eat a body line of asterisks — unlikely in body. Add to isBoilerplate: `if(/^[*\s]{3,}$/.test(t)) return true;` — but careful: this runs before footnote check; a footnote line "* See..." has letters → not matched. OK add it.

Also add "para" markers? no.

I think we're good. One more: the detail row's `.full` uses esc(p.lines.join("\n")) with white-space:pre-wrap — newlines preserved. ✓.

CSV full text with real newlines inside quoted field — valid CSV. ✓.

Also add `rel="noopener"` on links ✓.

Final check of the "at most three short sentences" before code. Write: "I built a paragraph-splitting tool for WORKSHOP_DATA.pdf_text: it cleans page headers/footers and footnotes, extracts paragraphs starting at 'N.', and checks each one against the reference. It shows found-vs-reference counts, a clickable table with first lines and mismatch flags, and a CSV export. Everything runs offline in the browser."

Now produce the final HTML. Let me write it out completely and carefully, checking syntax as I go.

Also: `e.target.closest` — if e.target is a text node? In DOM events target is element. OK.

Also `tbody.querySelector` with attribute selector containing idx number — safe.

Let me write everything now.

Also small thing: in the stats, when refParas is null, big = paras.length only. Fine.

Also the h1 title: "Split a UN document into its numbered paragraphs". Good.

Also I realize: the user says "Show how many paragraphs it found next to the number the document really has" — the stat card does "found / reference". Also maybe add explicit sentence in method card: "Found X paragraphs; the reference says Y." The stat note covers it. OK.

Also handle case where paras.length===0: table shows the "no paragraphs" row; stats show 0. Fine.

Writing final output now. I'll count roughly — fine under 700 lines.

One more detail: `input[type=search]` styling; placeholder text. OK.

Also make sure `button` inside toolbar doesn't submit anything (type="button"). ✓.

Also the toggleAll button uses `this.textContent` — with addEventListener function, `this` is the button. ✓.

Done — write it.