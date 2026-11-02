Let me plan this app carefully.

Data: `WORKSHOP_DATA.pdf_text` with `title`, `symbol`, `doc_url`, `source`, `count`, `records: [{page, text}]`, `reference: {paragraphs, footnotes, adopted, first_words: {"1": "A clean, healthy and sustainable environment", ...}}`.

Algorithm:
1. Join pages in order: for each record, split text into lines. Remove lines that are:
   - only a page number (e.g., "2" or maybe "2 " — a line that is just digits)
   - only the document symbol (e.g., "E/C.12/GC/27")
   - distribution code: "GE." followed by digits (e.g., "GE.25-12345")
   These go into the "removed lines" list (with page number).
2. Footnote lines: at the foot of a page — a line starting with a small number followed by text, e.g., "1 Some footnote text..." or "* footnote". How to detect? The reference says footnotes count. Typical UN PDF text: footnotes appear as lines like "1 Text of footnote..." near the bottom, after the main text, often after a blank line, and the number is small (1-99?) and the line doesn't start a paragraph (paragraph starts are "N. " with a period). Footnote lines typically look like "1 Some text" (number + space + text, no period) or with superscript. Hmm, but paragraph lines are "1. text" with period. So a line matching /^\d{1,2}\s+\S/ (number, space, no period) could be a footnote. But careful: could there be other lines like that? E.g., list items "1 something"? In UN documents, footnotes are usually at the bottom of the page after the body. A heuristic: a line matching /^(\d{1,3})\s+(.+)$/ where the number is not followed by "." — treat as footnote. But also years like "2025 something"? "2025" is 4 digits; restrict to 1-2 digits maybe. Cross references like "see paragraph 12 above" don't start a line with a bare number typically.

   Actually the sample page 1 text includes "General comment No. 27 (2025)..." — that line starts with "General". The header lines: "E/C.12/GC/27", "United Nations", "Economic and Social Council", "Distr.: General", "6 November 2025", "Original: English", "Committee on Economic, Social and Cultural Rights", then title lines, then "I.", "Introduction", "1.", "A clean, healthy...". Hmm wait — in the sample, "1." appears on its own line and the text on the next line! "1.\nA clean, healthy and sustainable environment is an essential precondition..." So the paragraph number may be on its own line, with the text on the following line(s). So my paragraph-start detection must handle "N." alone on a line, then text follows.

   So: a line that is exactly "N." (digits + period, nothing else) OR begins with "N. " starts paragraph N. The rule says: "A paragraph starts where a line begins with the next expected number, a full stop and a space ('1. ', then '2. ' …). Numbers out of sequence (years, cross-references) do not start a paragraph." So only the *next expected* number starts a paragraph. That's a strong constraint: expected starts at 1; when we see a line starting with "1. " (or "1." alone), paragraph 1 starts; then expected becomes 2; only lines starting "2. " start paragraph 2; etc. This handles years like "2025. " — well "2025." wouldn't match expected small numbers anyway, but cross-references like "12. " inside text when expected is 5 won't start. Good.

   But wait — what about "1." on its own line followed by text on next line? The rule says line begins with "N. " (number, full stop, space). If the line is just "1." with no trailing space... In the sample, the text shows "1.\nA clean..." — the line is "1." possibly with trailing space trimmed. I should handle both: line matches /^(\d+)\.\s*$/ (number alone with period) → start paragraph, and the text begins on subsequent lines. And line matches /^(\d+)\.\s+(.*)$/ → start paragraph with first line of text.

   Also section headings like "I.", "Introduction", "II.", "General..." — "I." is Roman numeral, not digits, fine. But what about headings like "1. Introduction"? In some docs numbered headings exist. With the "next expected number" rule, if expected is 1 and a heading line is "1. Introduction" — hmm, that would falsely start paragraph 1. But in this document, headings are Roman numerals ("I. Introduction"), so fine. The rule given is explicit; follow it.

   Footnote detection: lines at foot of page. Heuristic: line matches /^(\d{1,2})\s+(\S.*)$/ (small number, whitespace, text, no period after number) → footnote. But could a paragraph continuation line start with a number? E.g., "2025 was the year..." — 4 digits, excluded by {1,2}. "3 per cent of..." — possible! Hmm. "3 per cent" would match. Risky. Better: footnotes appear at the foot of a page — after the last paragraph text, typically following a blank line or a separator. Common pattern in converted UN PDFs: footnotes at bottom like "1 See ..." or "________" separator then footnotes. 

   Alternative approach: footnote lines are those matching /^\d{1,2}\s/ that occur *after* we've seen... hmm. Let me think about what the actual data looks like. The sample only shows page 1 which has no footnotes visible (truncated). The reference says footnotes count exists. Typical E/C.12/GC/27 footnotes: e.g. page with "* The present general comment..." Actually GCs often have footnotes like "1 See Official Records..." at page bottoms.

   A safer heuristic combining position: a line is a footnote if it matches /^(\d{1,2})\s+\S/ AND (it appears after a blank line within the page, i.e., in the lower part of the page) — but "foot of a page" is hard to determine from text alone. Alternatively: footnote number is small AND the same number pattern... Hmm.

   Another approach: footnote lines match /^\d{1,3}\s/ but NOT /^\d+\.\s/ (paragraph start) and the number is ≤ some bound and... Let me think about false positives: lines starting with a bare number + space in body text. In UN documents, body text rarely starts a line with "3 per cent" — but line wrapping could produce it: e.g., "...in 2025,\n3 per cent of States..." Possible but rare. Also "60. " style? No.

   Actually, maybe better: footnotes in these converted texts often appear as lines like "1 Text..." where the number is followed by a space, and they occur after the main body — often the page ends with them. A common robust heuristic: treat a line as a footnote if it matches /^\d{1,2}\s+\S/ and we are not currently... hmm, but paragraph text can contain such lines mid-paragraph.

   Let me reconsider: maybe combine both: footnote if matches /^\d{1,2}\s+\S/ AND the previous line is blank OR previous line is a footnote OR we've already seen the page's paragraphs... Actually in PDF conversion, footnotes at the foot of the page are usually separated from body text by a horizontal rule or blank line, and they come after all body text of that page. But body text of the page continues... no, footnotes are at the bottom, so after them only page footer (page number, symbol) which we remove.

   Hmm, but a wrapped body line could start with "3 per cent". To reduce risk: require the number to be ≤ 99 and the line to come after a blank line? Not guaranteed.

   Alternative: since footnote numbers in a document typically restart or increment, and reference gives total footnotes count, I could count lines matching /^\d{1,2}\s+\S/ that are NOT paragraph starts and occur when... 

   Let me think about what the actual E/C.12/GC/27 text looks like. UN PDF-to-text (like the sample) puts footnotes at the bottom of the page, typically like:

   ```
   ...body text...
   
   1 See Committee on Economic, Social and Cultural Rights, general comment No. ...
   2 ...
   
   E/C.12/GC/27
   3
   ```

   Hmm, actually in many UN PDFs the footnote separator is a line of underscores or the footnotes just appear. The sample page 1 shows header lines then content. Page footers: symbol line and page number line (which we remove).

   Given uncertainty, I'll use this heuristic: a line is a footnote line if it matches /^(\d{1,2})\s+(\S.*)$/ (number 1–2 digits, whitespace, then text — no period after the number) AND it is not a paragraph start. Additionally, to avoid mid-paragraph false positives like "3 per cent", I can require that the line appears after a blank line OR after another footnote line within the page (i.e., in a "footnote block" at the foot). Hmm, but what if the converter doesn't put a blank line? 

   Actually, let me reconsider: maybe simpler and matching the spec: "Footnote lines (a small number then text, at the foot of a page) are removed from the paragraphs and only counted." The spec itself says the detection is "a small number then text". So the spec author intends: line matches small number + space + text → footnote. I'll implement: /^\d{1,3}\s+\S/ and not a paragraph-start pattern, and number ≤ 99? "small number" — I'll use 1–2 digits (≤99). But "2025" is 4 digits so years excluded. What about "10. " paragraph starts — those have a period, excluded. What about lines like "3 (a)"? Hmm, lettered sub-paragraphs are "(a) ..." typically, not "a)". 

   Risk: a wrapped line starting with e.g. "16 States" — would be misclassified as footnote and removed, damaging a paragraph. But the app's purpose is to *show* damage, and removed lines are shown in the collapsed list, so the reader can see. Also the "Differs" check would flag it. I think following the spec's simple rule is right. But to be a bit safer, I could add the condition that the footnote-looking line occurs after a blank line or at a position where... hmm. Let me look at the sample again: page 1 text ends with "tr\n[… rest of the page omitted in this sample]" — that's the sample truncation, not real data.

   I'll go with: footnote if line matches /^(\d{1,2})\s+\S/ (no period after number) — but also require that we are past... no. Keep simple per spec. Actually wait — one more consideration: what about lines like "1." alone (paragraph number on its own line)? That has a period, so not a footnote. Good. What about "2025" alone? Removed as page-number-like? "only a page number" — a line that is only digits. "2025" alone would be removed as "only a page number" — hmm, but a year alone on a line is unlikely. Page numbers in UN docs are like "2", "16". A line "2025" alone — could be a year in a table? Unlikely. The spec says remove lines that are only a page number. I'll remove lines matching /^\d{1,4}\s*$/ (only digits). Fine.

   Also remove lines that are only the document symbol: line.trim() === symbol, or starts with symbol? The header line is "E/C.12/GC/27". I'll remove lines whose trimmed content equals the symbol, or equals symbol + page-ish? Keep: trimmed === symbol. Also maybe lines like "E/C.12/GC/27" appear at top of each page. Also "GE.25-..." distribution: /^GE\.\s*\d/ or /^GE\.\d+/. Spec: "a distribution code ('GE.' followed by digits)". So /^GE\.\d+/.

   Also maybe "Distr.: General", "Original: English", "United Nations", "Economic and Social Council" header lines — spec doesn't say to remove those; they'd end up... where? They appear before paragraph 1 on page 1. Since paragraph 1 starts at "1.", the header lines before it would be... orphan text before the first paragraph. What do we do with text before paragraph 1? The spec says paragraphs start at expected numbers; text before the first paragraph start — I could discard it into the removed-lines list? Hmm, spec says removed lines are only page number / symbol / GE codes / footnotes. Header lines like "United Nations", "Distr.: General" would be pre-paragraph text. Options: attach to nothing and show in removed list as "other header lines"? The spec's collapsed list is "Lines removed as headers, footers and footnotes" — so header lines generally. I think it's reasonable to also remove common header lines: "United Nations", "Economic and Social Council", "Distr.: ...", "Original: ...", committee name, title lines? That gets complicated. 

   Simpler: text encountered before the first paragraph start (expected=1) is treated as front-matter and put into the removed-lines list labeled "before first paragraph". Also lines between... no, once paragraphs start, everything until next paragraph start belongs to current paragraph (including section headings like "II. ..." — those stay inside the preceding paragraph? Hmm, "II. Climate change" heading would be appended to the previous paragraph's text. That's what "text runs until the next start" implies. OK, follow spec.)

   Wait, but actually — headings like "I." and "Introduction" on page 1 come before "1.", so they're front matter. Good. But later, "II." headings appear mid-document after some paragraph — they'd be glued to the previous paragraph. That's per spec ("Text runs until the next start"). Fine — the app flags damage, doesn't repair.

   Hmm, but actually, should I remove lines like "United Nations", "Distr.: General" etc. explicitly? If I treat all pre-first-paragraph text as removed, that handles page 1. But headers repeat on every page! Page 2 might start with "E/C.12/GC/27" (removed as symbol), maybe "2" (removed as page number), but also possibly "United Nations"? Typically only page 1 has the full masthead; later pages have symbol + page number. But some have "E/C.12/GC/27" at top and page number at bottom. If a later page had extra header lines, they'd get glued into the current paragraph. To be safe, I'll also remove lines matching common masthead patterns: "United Nations", "Economic and Social Council", /^Distr\.:/, /^Original:/, and the committee name line? The committee name "Committee on Economic, Social and Cultural Rights" — I can derive from... hmm, hard-coding is discouraged ("never hard-code... names"). But these are document-specific header strings; I could remove lines that appear on page 1 before paragraph 1 automatically (front matter), and for later pages, remove lines equal to any front-matter line? That's clever: collect the set of lines that appear before the first paragraph on page 1 (the masthead), and remove identical lines on later pages. That's data-driven, not hard-coded. 

   Also title lines of the document appear on page 1 before "I." — they'd be in front matter. Good.

   But careful: a front-matter line might coincidentally equal a body line later (e.g., "Introduction" as a heading on a later page — "Introduction" appears as a section heading "I. Introduction"? In the sample, "Introduction" is its own line on page 1). If a later page has a section heading "Introduction" alone on a line, it'd be removed — minor. Acceptable? Hmm, could damage. But headings in this doc are like "II. Something" on one line probably. Risk is low. Alternatively only remove masthead lines that appear on page 1 before paragraph 1 AND contain no sentence-like content... Overthinking. I'll do: front-matter lines (before first paragraph start, on any page? no—) Let me define: while expected number is still 1 (no paragraph found yet), all non-removed lines go to "front matter" removed list. Once paragraph 1 starts, subsequent pages' header lines: remove lines that exactly match any front-matter line seen (masthead repetition), plus symbol/page-number/GE lines. That's reasonable.

   Hmm wait, actually there's a subtlety: what if page 1's masthead includes the title spanning multiple lines, and one of those lines is e.g. "General comment No. 27 (2025) on economic, social and" — unlikely to recur. Fine.

   Also, blank lines: keep them as paragraph separators within text? For display, I'll join lines with "\n" and render with white-space: pre-wrap. Blank lines within a paragraph — keep or drop? Keep for fidelity ("exactly as extracted"). But leading blank lines... I'll trim leading/trailing blank lines of each paragraph but keep internal structure. Hmm, "exactly as extracted" — I'll keep internal newlines, trim outer whitespace. Reasonable.

3. Paragraph detection details:
   - expected = 1
   - For each line (after removals), check if line starts a paragraph: match /^(\d+)\.(\s+(.*))?$/ — i.e., number, period, then either end-of-line or space+rest. If number === expected → start new paragraph with number, page = current page, text lines = [rest if present]. expected++. If number !== expected → not a start; treat as normal text line (could be a cross-reference "see 12. above" — but that wouldn't be at line start usually; if it is, it stays as text). 
   - Wait: what about "1." alone on a line — regex /^(\d+)\.$/ matches with rest undefined → paragraph starts, text begins next lines. Good.
   - Edge: what if a paragraph number appears like "10." but expected is 10 — good. What if the document skips a number (damage)? Then expected never advances and subsequent paragraphs get glued. The app flags via reference comparison? The reference first_words only checks opening words. If numbers skip, the table would have gaps — the spec says table numbers run 1,2,3 without gaps, so presumably the data is clean enough. But to be robust: if we encounter a line starting with "N." where N > expected and N ≤ expected + some gap? Spec says "Numbers out of sequence do not start a paragraph." Strictly: only next expected. But if the converter dropped a "5." line, then paragraph 5's text would glue to paragraph 4, and expected stays 5 forever, so paragraphs 6+ never start → table would stop at 4. That would fail "at least 30 rows". Hmm. But the spec explicitly says only the next expected number starts a paragraph, and the success criterion says numbers run without gaps — implying the data works with the strict rule. But to be safe against a missing number, I could allow: if line starts with "N." and N === expected → start; else if N > expected and N is "plausible" (e.g., N ≤ expected + 5?) — no, spec says out of sequence do not start. Years like "2025." — 4 digits. Cross-references "12. " when expected is 5 — must not start. If I allowed N > expected, "12." would falsely start. So strict rule it is. But then a single dropped number breaks everything after. Compromise: strict rule, but if we reach end of document with expected < some number and we found fewer paragraphs than... hmm. 

   Alternative robust approach: allow start if N === expected, OR (N > expected AND the line looks like a paragraph start AND N ≤ reference.paragraphs AND ... ) — can't distinguish from cross-reference "12." easily. Actually cross-references at line start like "12. The Committee..." — in UN text, cross-references are usually inline ("see para. 12 above"), not at line start with "12. ". A line starting "12. " at the start of a wrapped line could happen if text wraps right after "para." — e.g., "...see paragraph\n12. ..." no, that would be "12 above" not "12. ". Hmm, "12." with period at line start — could occur if the text has "resolution 12." wrapped. Rare.

   Given the spec is explicit and the success criteria expect it to work, I'll implement strict next-expected, but with a safety: if a line starts with "N." where N > expected and N ≤ reference.paragraphs and the previous paragraph is "complete"... too complex. Let me just also handle: if N > expected and N - expected is small (say ≤ 3) and the current paragraph already has text and the line's number N ≤ reference.paragraphs → treat as start (the missing numbers were lost). Hmm, but that could misfire on cross-references. 

   Actually, you know, let me think about what the real data likely is: 20 pages, 90 paragraphs, footnotes. The converter output — the sample shows "1." on its own line. Likely all paragraph numbers are on their own lines or followed by text. The strict rule should work. I'll implement strict, and additionally: if we're at end and expected hasn't reached reference count but we found lines starting with higher numbers... I'll add the fallback: a line starting with "N." starts a paragraph if N === expected, OR if N > expected AND N ≤ reference.paragraphs AND the line is the *first* non-blank line after a blank line? No — overengineering. 

   Hmm, let me reconsider once more. The spec: "A paragraph starts where a line begins with the next expected number, a full stop and a space ('1. ', then '2. ' …). Numbers out of sequence (years, cross-references) do not start a paragraph." Clear. Implement exactly that. If the data has a dropped number, the app shows fewer paragraphs and the counter shows it — that's the app working as intended (flagging damage). The success criteria say N close to 90, so presumably fine.

   Wait, one more: "1. " with space — but sample shows "1." alone. My regex handles both. Also possible: "1.\t" or multiple spaces. Use /^(\d+)\.(?:\s+(.*))?$/.

   Hmm, also what about numbers with leading zeros or "01."? Unlikely.

4. Footnote counting: count footnote lines removed. Reference footnotes count for comparison. My heuristic: line matches /^(\d{1,2})\s+\S/ and not paragraph-start. But wait — could a footnote line be like "1 See ..." — yes matches. Could footnotes be marked with "*" or "________"? Spec says "a small number then text". OK.

   But false positives: body lines starting with "3 per cent" etc. To mitigate, maybe require the footnote number to be ≤ 30? Footnotes per page are few. Hmm, "small number" — I'll say 1–2 digits. Also, footnotes usually come after body text on the page — but I won't use position. Actually, let me add a mild positional guard: footnote lines typically appear after a blank line (separator) — but not guaranteed. I'll keep it simple per spec: /^\d{1,2}\s+\S/ and not a paragraph start. Hmm, wait — what about lines like "2 (2025)"? matches → footnote. Could be a citation line... In GC text, citations are inline. I'll accept.

   Hmm, actually there's another risk: lettered sub-paragraphs "a) text" — start with letter, fine. What about "(a)" — fine.

   One more risk: lines like "16.3" SDG targets? Not in this doc.

   Also: what about the line "6 November 2025" (date in masthead)? It's before paragraph 1 → front matter. Good. "Distr.: General" → front matter. Good.

   But wait — what about page 2+: does the masthead repeat? If page 2 starts with "E/C.12/GC/27" then maybe "2" at bottom. If it also has "United Nations" etc., my front-matter-set removal handles it. I'll build the set of lines seen before paragraph 1 starts (on page 1) and remove exact matches on later pages. Also remove lines matching /^Distr\.:/ etc.? The front-matter set covers it if repeated. But what if page 2 has "Distr.: General" but page 1 had "Distr.: General" too — covered. OK.

   Hmm, but careful: front-matter set includes lines like "I." and "Introduction" and title lines. If a later page has heading "Introduction" alone... In this document, section headings are like "II. ..." — let me not worry.

   Actually wait, there's a subtle issue: the front matter on page 1 includes "I." and "Introduction" — but what if the document's section headings later are like "III." alone on a line then "Climate change" on next line? "III." is Roman, not digits, so not a paragraph start; it'd glue into previous paragraph. Fine per spec.

5. "Differs" check: paragraph's first six words vs reference.first_words[number]. Normalize: lowercase, strip punctuation, split on whitespace, take first 6, compare arrays. If reference has no entry → "no reference". If match → OK (no mark). Else "Differs" and show reference words.

   First six words of the paragraph: from the paragraph's text (joined lines), extract first 6 words. Normalization: remove punctuation (.,;:()"' etc.), lowercase, collapse spaces. Compare word-by-word.

   Note: reference first_words values are like "A clean, healthy and sustainable environment" (6 words). Compare normalized.

6. Table: one row per paragraph: number, page where it starts, first line ~90 chars, symbol link, Differs mark. Checkbox "Show differences first" sorts marked rows to top (stable). Clicking a row expands full paragraph beneath it (accordion), with reference first words shown beside it. Also maybe a "no reference" note.

7. CSV download: number, page, matches reference (yes/no/no reference), full text quoted. Build with proper CSV escaping (quote fields containing quotes/commas/newlines, double the quotes). Use Blob + URL.createObjectURL, download attribute. 

8. Collapsed list of removed lines: use <details> element. Each removed line with page number and reason (page number / symbol / distribution / footnote / front matter).

9. Counters: paragraphs found / reference.paragraphs; footnotes removed / reference.footnotes; differs count. Note text: "Found by the code from the page text; reference figures come from the file."

10. Header: title (from data), symbol linked to doc_url, line: "raw PDF text, N pages, source: …" — N = records.length, source = data.source. Also maybe "adopted" date from reference? Not required. Keep simple.

Design: clean, #1f6fb2 accent, system fonts, 16px base, max-width container ~960px, no horizontal scroll. Table with sticky header maybe. Keep under 700 lines.

Let me now write the parsing code carefully.

```js
const D = window.WORKSHOP_DATA.pdf_text;
const symbol = D.symbol;
const pages = D.records; // [{page, text}]
const ref = D.reference || {};
const refFirst = ref.first_words || {};

// classify lines
const removed = []; // {page, line, reason}
const paras = []; // {num, page, lines: []}
let expected = 1;
let frontMatter = []; // lines before first paragraph
let frontSet = new Set();
let current = null;

function isPageNumberLine(l){ return /^\d{1,4}$/.test(l); }
function isSymbolLine(l){ return l === symbol; }
function isDistLine(l){ return /^GE\.\s*\d/.test(l); }
function isFootnoteLine(l){ return /^\d{1,2}\s+\S/.test(l) && !/^\d+\.\s/.test(l) && !/^\d+\.$/.test(l); }
```

Wait, footnote regex /^\d{1,2}\s+\S/ — "1 See" matches. Paragraph start "1. text" — /^\d+\.\s/ doesn't match /^\d{1,2}\s/ because after digits comes "." not whitespace. So the extra checks unnecessary, but harmless. Actually "12. text": /^\d{1,2}\s/ — "12" then "." — no match since \s required right after digits. Good, so footnote regex alone suffices: /^\d{1,2}\s+\S/. But careful: "1. text" — digits "1", then "." — \s fails. Good.

Hmm wait, what about a line "1 " (number + space, nothing else)? \S fails → not footnote, not paragraph start (needs period). It'd be body text. Fine.

Paragraph start: /^(\d+)\.(?:\s+(.*))?$/ — but this would also match "2025." (year with period at line end)? "2025." alone on a line — matches with num=2025 ≠ expected → not a start, becomes text. OK. And "3.14"? matches num=3, rest="14"? No: /^(\d+)\.(?:\s+(.*))?$/ on "3.14" — after "3." comes "14" without whitespace, so (?:\s+...) optional group requires whitespace; "14" doesn't match \s, and the optional group can be empty but then $ must follow — "14" remains → no match. Good, "3.14" is not a paragraph start. 

But "12. The Committee..." when expected is 12 → starts. When expected is 5 → text. Good.

Processing per page:
```js
for (const rec of pages) {
  const lines = rec.text.split(/\r?\n/);
  for (let raw of lines) {
    const line = raw.replace(/\s+$/,''); // trim right; keep left? trim both
    const l = line.trim();
    if (l === '') { if (current) current.lines.push(''); continue; } // keep blank inside paragraph? maybe skip blanks to simplify; but "exactly as extracted" — I'll keep blanks only inside paragraphs, skip leading blanks.
    ...
  }
}
```

Hmm, blank lines: if current paragraph exists, push '' (preserve). If no current paragraph (before first), skip. When starting a new paragraph, don't include preceding blanks.

Classification order:
1. if isPageNumberLine(l) → removed (reason "page number")
2. else if isSymbolLine(l) → removed ("document symbol")
3. else if isDistLine(l) → removed ("distribution code")
4. else if frontSet.has(l) && current !== null → removed ("repeated header") — only after first paragraph started; before that, front matter.
5. else if current === null → frontMatter.push({page, line:l}); frontSet.add(l) — but only if expected===1 i.e., no paragraph yet. Actually current===null only before paragraph 1. But also: what if paragraph 1 never starts until page 2? Then page 2's masthead also front matter. Fine.
   Wait — but frontSet should only include masthead lines, and we add every pre-paragraph line. If paragraph 1 starts on page 1, frontSet = page-1 masthead lines. Good.
   Hmm, but one problem: what if a pre-paragraph line on page 1 is actually meaningful (like the title)? It's front matter — removed and shown in the list. Fine.
6. else check paragraph start: m = l.match(/^(\d+)\.(?:\s+(.*))?$/); if m && parseInt(m[1]) === expected → start new paragraph: current = {num: expected, page: rec.page, lines: m[2] ? [m[2]] : []}; paras.push(current); expected++.
   else if isFootnoteLine(l) → removed (reason "footnote"), footnoteCount++
   else → if current, current.lines.push(l); else frontMatter... (covered by 5).

Wait, order issue: footnote check should come before appending to current. And paragraph-start check before footnote (a paragraph start "1. text" isn't a footnote anyway). Also: should footnote check apply when current===null? Before paragraph 1, a line "1 See..." — hmm, if expected is 1 and line is "1 See..." (no period), it's a footnote-looking line but expected paragraph 1 hasn't started. On page 1 there are no footnotes before para 1. Edge case: treat as front matter. My order: front-matter check (current===null) comes before footnote check → goes to front matter. Acceptable.

Hmm wait, actually there's a subtle problem with frontSet removal: after paragraph 1 starts, any line exactly matching a front-matter line is removed as "repeated header". But what if a body line coincides? E.g., front matter contains "Introduction" (page 1 heading). If later a line is exactly "Introduction" — removed. Minor risk, acceptable. Actually, to reduce risk, maybe only add to frontSet lines that look like masthead: short lines without sentence-ending period? Hmm. The title lines end without period. "United Nations", "Economic and Social Council", "Distr.: General", "6 November 2025", "Original: English", "Committee on Economic, Social and Cultural Rights", "General comment No. 27 (2025) on economic, social and", "cultural rights and the environmental dimension of", "sustainable development*", "I.", "Introduction". The risky ones: "I." and "Introduction". Later section headings might be "II." on its own line — not in frontSet ("I." ≠ "II."). "Introduction" as a standalone line later — only if a section is titled "Introduction" again; unlikely mid-document. I'll keep it but maybe exclude lines that are single Roman numerals or single common words? Overthinking — keep simple: add all pre-paragraph-1 lines to frontSet. Actually hmm, let me exclude lines that match /^[IVX]+\.$/ (Roman numeral headings) from frontSet? No wait — those ARE headings that might repeat? Section headings "I.", "II." differ. If page 1 has "I." and later "I." appears again (unlikely). Keep all. Fine.

Actually, wait. Let me reconsider whether later pages even have masthead lines. In the sample, page 1 has the full masthead. Pages 2–20 likely start with "E/C.12/GC/27" (symbol, removed) and end with page number (removed). Possibly also "GE.25-xxxxx" on page 1 only. So frontSet may rarely trigger. Good.

Footnote counting: footnotesRemoved counter. Reference footnotes: ref.footnotes.

Now, "first line (about 90 characters)": take paragraph text (lines joined by ' '), slice 90 chars + '…' if longer.

First six words: from joined text: text.split(/\s+/).filter(Boolean), map normalize (lowercase, remove non-alphanumeric except keep letters/numbers — strip punctuation: w.replace(/[^\p{L}\p{N}]/gu,'')), filter empty, take 6. Reference: same normalization on refFirst[num]. Compare arrays element-wise. If refFirst[num] undefined → status "no reference". Else if equal → "match". Else "differs".

Note: reference first_words keys are strings "1".."90". Paragraph num is int → refFirst[String(num)].

Hmm — one concern: the paragraph's first six words — if the converter put "1." on its own line, the text starts with the actual words. Good. But what if the paragraph start line is "1. A clean..." — m[2] = "A clean...". Good.

Another concern: what if the first line of a paragraph in the PDF is a continuation... no.

What about paragraphs whose text begins with something like "(a)"? No, lettered sub-paras come after.

CSV: columns: number, page, matches_reference (yes/no/no reference), text. Escape: if field contains ", \n, \r → wrap in quotes and double quotes. Header row: "number,page,matches_reference,text". Download via Blob.

Sorting: checkbox "Show differences first" — when checked, rows with status "differs" (and maybe "no reference"? spec says "moves marked rows to the top" — marked = Differs) go first, stable order otherwise. I'll sort differs first, then no-reference? Spec: "A tick box 'Show differences first' moves marked rows to the top." Marked rows = those with "Differs" mark. I'll put differs first, keep others in original order. Maybe also no-reference after differs? Keep simple: differs first only.

Row click: toggle expansion — a detail row beneath with full text (pre-wrap) and reference first words beside it. Implementation: each paragraph = a <tbody> with two rows? Or a div-based list. Simpler: build table rows; on click, insert a <tr class="detail"><td colspan=5>...</td></tr> after it, or toggle. I'll re-render on toggle or use insertAdjacent. Let me do: clicking a row toggles an expanded row. I'll manage with a Set of expanded nums and re-render tbody. Re-render is simple and fine for ~90 rows.

Columns: # (number), Page, First line, Symbol (link), Match (✓ / Differs / no reference). Spec: "number, page where it starts, first line (about 90 characters), symbol linked to doc_url, and a 'Differs' mark". So symbol column with link on every row (same symbol). OK.

Detail content: full paragraph text exactly as extracted (pre-wrap), plus "Reference opening: …" shown beside it. Layout: two columns within the detail cell — paragraph text left, reference right? "with the reference's first words shown beside it" — I'll do a flex: full text (flex 2) and a side box (flex 1) with reference first words and status. On narrow screens stack.

Counters section: three stat cards: "Paragraphs found: N of 90", "Footnotes removed: M of K", "Opening words differ: X". Under: note "Found by the code from the page text; reference figures come from the file."

Also maybe show adopted date? Not required. Skip.

Removed lines collapsed list: <details><summary>Lines removed as headers, footers and footnotes (count)</summary> <ul> each: "p. X — [reason] — line text". Cap display? Could be many lines (20 pages × ~3 = 60 + footnotes). Fine to list all; maybe limit each line to 120 chars in the list. I'll show full but truncated with title attr. Keep simple: show text truncated to 140 chars.

Header: 
- h1: D.title
- line: symbol linked: <a href=doc_url>symbol</a>
- "Raw PDF text, N pages, source: D.source" — N = D.records.length. Also maybe "count" field — D.count is number of records (pages). Use records.length.

Wait, spec: "one line: 'raw PDF text, N pages, source: …' (N from the data)". Use D.records.length (or D.count). I'll use records.length and fall back to count.

"How this is computed" note near counters: "Found by the code from the page text; reference figures come from the file." — that's the required note. Also add a short method note: "Pages are joined in order; lines that are only a page number, the symbol, or a GE. distribution code are dropped; footnote lines (small number + text) are counted and removed; a paragraph starts at the next expected 'N.' line." Good to include as "How this is computed".

Now the "Differs" comparison detail: "comparing word by word while ignoring case, punctuation and extra spaces". Normalize each word: lowercase + strip punctuation. Punctuation: anything not letter/number. Use regex /[^\p{L}\p{N}’'-]/gu → remove? Keep apostrophes/hyphens? "don't" vs "dont" — reference and text both from same doc, likely identical. I'll strip all non-alphanumeric (unicode-aware). Compare first 6 words of each. If paragraph has fewer than 6 words? Then compare what's there — arrays of different length → differ (unless reference also shorter). Use: take up to 6 from each, compare lengths and items.

Edge: reference first_words might have exactly 6 words. Paragraph first 6 words normalized. Compare.

Now let me also double check the footnote heuristic against a possible pattern: UN footnotes in converted text sometimes appear as "1\nSee ..." (number alone on line, text next line)? Then "1" alone would be removed as page-number line! Hmm. That's a risk: a footnote number alone on a line would be classified as "page number" and removed — still removed and counted? It'd be counted as page-number removal, not footnote. The footnote counter would then undercount vs reference. The spec says footnote lines are "a small number then text" — same line. I'll trust that. But to hedge, maybe treat a lone small number (1–2 digits) that is NOT a plausible page number... page numbers go up to 20; footnote numbers could be up to ~30+. Can't distinguish. Keep spec rule: lone digits = page number line. Hmm, but wait — what if footnote is "1 See..." on one line — handled. OK.

Actually, hold on — let me reconsider the lone-number removal: "Remove lines that are only a page number". Page numbers 1–20. A lone "1" could be a footnote marker. But spec explicitly says remove lines that are only a page number. Follow spec.

Another consideration: the sample page-1 text shows the paragraph as "1.\nA clean, healthy..." — so "1." alone on a line. My paragraph-start regex handles "1." alone. But note: is "1." maybe "1. " with trailing space? I trim → "1.". Regex /^(\d+)\.(?:\s+(.*))?$/ matches "1." with m[2] undefined. Good.

But wait — danger: a line that is just "1." when expected is, say, 5 — e.g., a cross-reference ending a line? It'd be appended as text. Fine.

Another danger: front matter includes "I." — Roman, fine.

What about the title line "General comment No. 27 (2025) on economic, social and" — contains "27 (2025)" — not at line start. Fine.

Now, what about lines like "E/C.12/GC/27" appearing mid-page as footer — removed by symbol check. Also possibly "E/C.12/GC/27" with trailing spaces — trimmed. Also maybe "E/C.12/GC/27 " plus page? Some PDFs put "E/C.12/GC/27  2" — hmm, then line is "E/C.12/GC/27 2"? My symbol check (exact equality) fails; page-number check fails; it'd become body text glued to paragraph! Risk. Let me make symbol check: l === symbol || l.startsWith(symbol + ' ') || l === symbol + ' ' + digits? I'll do: if l === symbol || new RegExp('^' + escaped(symbol) + '\\s*\\d*$').test(l) → symbol/footer line. Escape symbol for regex. Good.

Also distribution: /^GE\.\s*\d+/ — also "GE.25-01234". Matches. Also maybe "Distr.: General" appears only page 1 (front matter). OK.

Also, what about "Original: English" etc. — front matter page 1.

Now — one more important thing: pages after page 1 might begin with the symbol line then content directly. Good.

Let me also handle: what if a page's text uses "\n\n" between paragraphs — blank lines preserved inside current paragraph; when new paragraph starts, we don't carry blanks. When rendering full text, trim leading/trailing blank lines.

Now the counters: "paragraphs found / paragraphs in the reference" → `${paras.length} of ${ref.paragraphs}`. Footnotes: `${footnoteCount} of ${ref.footnotes}`. Differs: count of status==='differs' (out of paras.length; maybe "X of N paragraphs"). Spec: "paragraphs whose opening words differ from the reference" — show count, maybe "X of N". I'll show "X of N paragraphs".

Success criteria: first counter reads "N of 90" — ref.paragraphs should be 90. Good.

Table rows: at least 30 — with 90 paragraphs, fine.

Row 1 click shows text starting "A clean, healthy and sustainable environment" — our para 1 text starts with that (after "1." line). Good.

CSV rows = table rows (all paragraphs). "as many rows as the table" — table shows all paragraphs (maybe all, no pagination). 90 rows fine.

Now write the HTML. Structure:

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
  <h1 id="docTitle"></h1>
  <p class="meta"><a id="docLink"></a></p>
  <p class="meta" id="sourceLine"></p>
</header>
<section class="stats">
  three cards + note
</section>
<section>
  <label><input type="checkbox" id="diffFirst"> Show differences first</label>
  <button id="csvBtn">Download CSV</button>
  <table>…</table>
</section>
<details id="removedDetails">…</details>
<script>…</script>
</body>
</html>
```

CSS: body font stack system, background #f7f9fb, container max-width 1000px, accent #1f6fb2. Table full width, th sticky? Keep simple. Status pills: .ok (green? use muted), .diff (red-ish #b3261e?), .noref (grey). Accent color for links/buttons #1f6fb2.

Keep under 700 lines total. Let's write it.

JS details:

```js
const D = window.WORKSHOP_DATA.pdf_text || {};
const records = Array.isArray(D.records) ? D.records : [];
const symbol = D.symbol || '';
const ref = D.reference || {};
const refFirst = ref.first_words || {};
const esc = s => String(s).replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
const symbolRe = symbol ? new RegExp('^' + esc(symbol) + '\\s*\\d*$') : null;

const removed = [];
const paras = [];
let expected = 1, current = null, footnotes = 0;
const frontSet = new Set();

const isDigits = l => /^\d{1,4}$/.test(l);
const isDist = l => /^GE\.\s*\d/.test(l);
const isFoot = l => /^\d{1,2}\s+\S/.test(l);
const paraStart = l => { const m = l.match(/^(\d+)\.(?:\s+(.*))?$/); return m ? {num:+m[1], rest: m[2] || ''} : null; };

for (const rec of records) {
  const page = rec.page;
  const lines = String(rec.text || '').split(/\r?\n/);
  for (const raw of lines) {
    const l = raw.trim();
    if (!l) { if (current) current.lines.push(''); continue; }
    if (isDigits(l)) { removed.push({page, reason:'page number', line:l}); continue; }
    if (symbolRe && symbolRe.test(l)) { removed.push({page, reason:'document symbol / footer', line:l}); continue; }
    if (isDist(l)) { removed.push({page, reason:'distribution code', line:l}); continue; }
    if (!current) { frontSet.add(l); removed.push({page, reason:'header (before first paragraph)', line:l}); continue; }
    if (frontSet.has(l)) { removed.push({page, reason:'repeated header', line:l}); continue; }
    const ps = paraStart(l);
    if (ps && ps.num === expected) {
      current = {num: expected, page, lines: ps.rest ? [ps.rest] : []};
      paras.push(current); expected++;
      continue;
    }
    if (isFoot(l)) { footnotes++; removed.push({page, reason:'footnote', line:l}); continue; }
    current.lines.push(l);
  }
}
```

Wait — issue: frontSet.add for pre-paragraph lines, but the check `if (!current)` happens before frontSet check — on page 1 before para 1, lines go to front matter. After para 1 starts, `frontSet.has(l)` removes repeats. But note: I add to frontSet AND removed with reason 'header'. Good.

Hmm, but one problem: blank lines when current exists are pushed as '' — but if a blank line occurs right before a new paragraph start, it's inside previous paragraph; when rendering, trim trailing blanks. Fine.

Another subtle issue: `if (!current)` — after paragraph 1 starts, current is never null again. Good.

Wait, another subtlety: what if the very first content line is "1." but expected=1 — starts. But what if masthead contains a line like "27." ? No.

Potential issue: paraStart regex on a line like "2025. The Committee..." — num=2025 ≠ expected → falls through to footnote check: /^\d{1,2}\s/ — "2025." has 4 digits then '.', no match → appended as text. Good.

Line "12. " when expected=5: ps.num=12≠5 → not start; isFoot? "12." then space — /^\d{1,2}\s/ requires whitespace immediately after 1-2 digits; "12." has '.' after "12" → no match → text. Good.

Line "3 per cent" when expected=5: isFoot matches → removed as footnote! False positive risk. Hmm. How likely is a wrapped line starting with "N <word>" where N is 1-2 digits? E.g., "...in\n3 per cent of cases..." Possible. But per spec, that's the rule. The app shows removed lines so reader can see. Also the paragraph would then differ from reference → flagged. Acceptable; spec dictates.

Hmm, actually wait — maybe I can reduce false positives: footnotes at the foot of a page usually come after the body text, and often after a blank line. I could require: isFoot(l) AND (previous line was blank OR previous line was a footnote OR ...). But if converter doesn't emit blank before footnotes, we'd miss them all. The spec's phrasing "(a small number then text, at the foot of a page)" suggests just the pattern. I'll go with pattern only. Actually — hmm, let me add one refinement that's safe: also treat as footnote if line matches /^\d{1,2}\s+\S/ — keep. Done deliberating.

Normalization for comparison:

```js
function normWords(s){
  return String(s).toLowerCase().split(/\s+/).map(w => w.replace(/[^\p{L}\p{N}]/gu,'')).filter(Boolean);
}
function firstSix(s){ return normWords(s).slice(0,6); }
function paraText(p){ return p.lines.join('\n').replace(/^\n+|\n+$/g,''); } // trim blank lines
```

Hmm, paraText joins with '\n' — internal blanks preserved. For first-line display: join lines with ' ' then collapse? "first line (about 90 characters)" — I'll take the text, replace newlines with ' ', collapse spaces, slice(0,90), add '…' if longer.

Status:
```js
function statusOf(p){
  const key = String(p.num);
  if (!(key in refFirst)) return {code:'noref', label:'no reference'};
  const a = firstSix(paraText(p)), b = firstSix(refFirst[key]);
  const same = a.length===b.length && a.every((w,i)=>w===b[i]);
  return same ? {code:'ok', label:'matches'} : {code:'diff', label:'Differs'};
}
```

Wait — refFirst values: "the first six words of each numbered paragraph" — so b has 6 words. a = first six of extracted. Compare. If paragraph text shorter than 6 words, lengths differ → differs. OK.

Hmm, one thing: paraText trims leading blank lines — but what if the paragraph's first line is blank because "1." was alone and next line blank? Then first words come after. Fine.

Edge: what if reference first_words includes the paragraph number? Sample: {"1": "A clean, healthy and sustainable environment"} — no number. Good.

Rendering:

```js
function render(){
  // stats
  // table body
}
```

Table build with DOM creation or innerHTML with escaping. I'll use innerHTML with an escape function for text content. Careful: paragraph text may contain <, >, & — escape.

```js
const escHtml = s => String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
```

Rows:
```html
<tr data-num="1" class="row ok">
  <td class="num">1</td>
  <td>1</td>
  <td class="firstline">A clean, healthy and sustainable environment is an essential…</td>
  <td><a href="doc_url" target="_blank" rel="noopener">E/C.12/GC/27</a></td>
  <td><span class="pill ok">matches</span></td>
</tr>
```
Differs rows get pill "Differs" (red) and maybe row class. no reference → grey pill "no reference".

Expanded detail row:
```html
<tr class="detail"><td colspan="5">
  <div class="detail-flex">
    <div class="fulltext">…pre-wrap…</div>
    <div class="refbox"><strong>Reference opening (first words)</strong><br>…</div>
  </div>
</td></tr>
```

Click handler on tbody (event delegation): find tr.row, toggle expanded set, re-render.

Sort: if checkbox checked, order = differs first (stable), else original. Use map with index.

CSV:
```js
function csvField(v){ v=String(v); return /[",\n\r]/.test(v) ? '"'+v.replace(/"/g,'""')+'"' : v; }
const rows = [['number','page','matches_reference','text']];
for (const p of paras){ rows.push([p.num, p.page, statusOf(p).code==='ok'?'yes':(statusOf(p).code==='diff'?'no':'no reference'), paraText(p)]); }
const csv = rows.map(r=>r.map(csvField).join(',')).join('\r\n');
const blob = new Blob([csv], {type:'text/csv;charset=utf-8'});
```
Download: a element with URL.createObjectURL, click, revoke.

Removed lines list: build <ul> with items: `p. {page} · {reason} · {line}` truncated to 160 chars.

Stats note: "Found by the code from the page text; reference figures come from the file." Plus a "How this is computed" paragraph describing the method.

Header line: `Raw PDF text, ${records.length} pages, source: ${D.source}` — spec: "raw PDF text, N pages, source: …". Also title h1 = D.title, and symbol link. Maybe also "Adopted …" from ref.adopted — optional; skip or include small. I'll include if present: "Adopted: …" — hmm, spec didn't ask; keep minimal but it's harmless. I'll skip to keep exactly to spec. Actually a tiny extra line is fine but let me keep to spec.

Also doc_url link on symbol in header: `<a href="${D.doc_url}">`.

Title of app: "Paragraph check — E/C.12/GC/27" — use symbol in <title>: `Paragraph checker · ${symbol}`.

Now, "How this is computed" near every chart or number — the counters get the note. Table gets a small note too maybe: "One row per paragraph found in the page text; click a row for the full extracted text." Good.

Let me also double-check the "Show differences first" behavior: "moves marked rows to the top" — marked = Differs. I'll sort: diff first, then noref? No — only marked (Differs). Others keep order. Implementation: 

```js
let order = paras.map((p,i)=>({p,i}));
if (diffFirst.checked) order.sort((a,b)=> (statusOf(b.p).code==='diff') - (statusOf(a.p).code==='diff') || a.i-b.i);
```
Array.prototype.sort is stable in modern JS, so `order.sort((a,b)=> diffB - diffA)` suffices, but include index tiebreak anyway.

Expanded state: Set of nums; when re-render after sort, keep expanded.

Now sizes: 90 paragraphs, each detail could be long — fine.

Let me also make sure: "Every row that shows a document has its symbol, linked to doc_url in a new tab." — symbol column with target=_blank. Header symbol link too.

Potential pitfall: `ref.paragraphs` might be 90; display "N of 90" — from data, not hard-coded. Good.

Let me now also think: does `records` have 20 pages with `page` numbers 1..20? Yes. Page where paragraph starts = rec.page of the page where the start line appeared. Good.

Now write final code. Aim ~350-450 lines. Let me draft CSS:

```css
:root{--accent:#1f6fb2;--ink:#1c2733;--muted:#5b6b7b;--line:#dfe6ee;--bg:#f6f8fa;--card:#fff;}
*{box-sizing:border-box}
body{margin:0;font:16px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;color:var(--ink);background:var(--bg)}
.wrap{max-width:1020px;margin:0 auto;padding:28px 20px 60px}
h1{font-size:1.5rem;margin:0 0 6px;line-height:1.3}
a{color:var(--accent)}
.meta{color:var(--muted);margin:2px 0}
.card{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:16px 18px;margin:18px 0}
.stats{display:flex;gap:14px;flex-wrap:wrap}
.stat{flex:1 1 200px;background:#fff;border:1px solid var(--line);border-radius:10px;padding:12px 16px}
.stat .big{font-size:1.35rem;font-weight:650}
.stat .lbl{color:var(--muted);font-size:.9rem}
.note{color:var(--muted);font-size:.9rem;margin-top:10px}
table{width:100%;border-collapse:collapse;background:#fff}
th,td{text-align:left;padding:8px 10px;border-bottom:1px solid var(--line);vertical-align:top;font-size:.95rem}
th{background:#eef3f8;position:sticky;top:0;font-size:.85rem;text-transform:uppercase;letter-spacing:.04em;color:#3d4c5c}
tr.row{cursor:pointer}
tr.row:hover{background:#f2f7fc}
tr.row.diff{background:#fdf3f2}
td.num{font-weight:650;white-space:nowrap}
.firstline{color:#33414f}
.pill{display:inline-block;padding:2px 9px;border-radius:999px;font-size:.8rem;font-weight:600;white-space:nowrap}
.pill.ok{background:#e6f4ea;color:#1e7e34}
.pill.diff{background:#fbe9e7;color:#b3261e}
.pill.noref{background:#eceff3;color:#5b6b7b}
tr.detail td{background:#fbfcfe}
.detail-flex{display:flex;gap:18px;flex-wrap:wrap}
.fulltext{flex:2 1 420px;white-space:pre-wrap;background:#fff;border:1px solid var(--line);border-radius:8px;padding:12px 14px;font-size:.92rem;max-height:340px;overflow:auto}
.refbox{flex:1 1 220px;background:#f2f7fc;border:1px solid var(--line);border-radius:8px;padding:12px 14px;font-size:.92rem}
.controls{display:flex;gap:16px;align-items:center;flex-wrap:wrap;margin:14px 0}
button{background:var(--accent);color:#fff;border:0;border-radius:8px;padding:9px 16px;font-size:.95rem;cursor:pointer}
button:hover{background:#185a92}
label.chk{display:flex;gap:8px;align-items:center;cursor:pointer}
details{margin:22px 0;background:#fff;border:1px solid var(--line);border-radius:10px;padding:12px 16px}
summary{cursor:pointer;font-weight:600}
.removed-list{list-style:none;margin:10px 0 0;padding:0;max-height:320px;overflow:auto;font-size:.88rem;color:#3d4c5c}
.removed-list li{padding:4px 0;border-bottom:1px dashed var(--line)}
.reason{color:var(--muted)}
footer? skip
```

Table wrapper for horizontal safety: wrap table in div with overflow-x:auto — but requirement says no horizontal scrolling on laptop; table with 5 columns fits. Still add wrapper for safety.

Now JS render functions. Also handle empty data gracefully (if no records, show message).

Let me write the whole file now.

Also: the "Differs" mark — spec says table has "a 'Differs' mark where the opening words do not match". I'll show pill "Differs" in the Match column; matches show "matches" (or a check ✓). no reference → "no reference".

Detail row shows reference's first words beside full text — for 'ok' rows too (show reference words). For noref: "No reference entry for this number."

CSV matches_reference values: "yes"/"no"/"no reference".

One more check on success criteria: "The downloaded CSV opens in a spreadsheet with as many rows as the table." Table shows all paragraphs (no pagination) → CSV rows = paras.length + header. Good.

Let me now also think about whether `paraStart` should require the number to be at line start after trim — yes, l is trimmed.

What about lines like "1.A clean" (no space)? Regex: /^(\d+)\.(?:\s+(.*))?$/ — "1.A" → after "1." comes "A" without \s → optional group empty, then $ fails → no match → treated as text/footnote? isFoot: /^\d{1,2}\s/ — "1.A" no whitespace → no. So it becomes body text of previous paragraph. Damage flagged. Fine.

Now, about counting "footnotes removed": I count footnote lines. Reference footnotes = number of footnotes (maybe counting footnote texts, possibly multi-line). If a footnote wraps to 2 lines, second line doesn't start with number → counted as body text! Hmm. That would glue footnote continuation into the paragraph. Risk. Mitigation: once a footnote line is seen on a page, subsequent non-blank lines until... hmm, until when? Until a paragraph start or end of page? Footnotes are at foot of page, so after the first footnote line, everything until page end (except symbol/page-number lines) is footnote continuation. But what if body text follows? In PDF layout, footnotes are at the bottom — after them only the footer. So rule: once we see a footnote line on a page, set pageFootnoteMode = true; subsequent lines (that aren't removed header/footer lines or paragraph starts) are also footnotes (count them? or count footnotes as number of footnote-start lines?). Reference counts footnotes — probably number of footnote entries, not lines. Hmm. If I count every footnote line including continuations, I might overcount vs reference if reference counts entries. If I count only lines starting with a number, I might undercount if... no — each footnote entry starts with its number on one line; continuations don't. So count = number of footnote-start lines = number of footnote entries (assuming each footnote's number is on the same line as its start, which the spec asserts: "a small number then text"). So: count footnote-start lines; continuation lines after a footnote start (until paragraph start / page end) are removed as "footnote (continued)" but not counted. 

But danger: what if a footnote appears mid-page (not at foot)? Then body text after it would be wrongly removed. In UN PDFs footnotes are at page foot. Accept.

Implement: per page, `let footMode = false;` reset each page. When isFoot(l) && !footMode → footnotes++, footMode=true, removed. When footMode && not paraStart && not header-removal → removed as 'footnote (continued)'. But careful: paragraph start check must come before footMode continuation check — a paragraph could start after footnotes? Only if footnotes mid-page; then paragraph start should still win. Order within loop for non-header lines:
1. paraStart && num===expected → new paragraph (footMode=false? set footMode=false since body resumes) 
2. isFoot(l) → footnote start (footnotes++, footMode=true)
3. footMode → footnote continuation (removed, not counted)
4. else → body text.

Hmm wait, but if footMode is true and a paragraph start appears, we start paragraph and set footMode=false. Good.

But also: blank lines — if footMode and blank line → keep footMode? Blank lines between footnotes — keep footMode true (don't reset). If current paragraph exists and blank line while footMode... blank lines: I push '' to current.lines if current — but if footMode, blank shouldn't go to paragraph. Order: handle blank first: if blank → if current && !footMode push '' else skip. Hmm, simpler: if blank, skip entirely (don't preserve blank lines). Does that violate "exactly as extracted"? The full text shown would have newlines between lines but no blank lines. Paragraph text "exactly as extracted" — I think preserving line breaks is enough; dropping blank lines is a display choice. But "never edited" — dropping blank lines is arguably editing. Hmm. I'll preserve blank lines within paragraphs (when not footMode), skip otherwise. Fine.

Also frontSet check placement: before paraStart? A repeated header line could theoretically match paraStart? No (headers aren't "N."). Order: digits/symbol/dist removals → if !current front matter → frontSet → paraStart → footnote → footMode → body. Wait, footMode continuation should be checked before body but after paraStart. And isFoot before footMode. Let me order:

```
if blank: ...
if isDigits → removed 'page number'
if symbolRe → removed 'symbol/footer'
if isDist → removed 'distribution code'
if !current → front matter (frontSet.add, removed 'header')
if frontSet.has(l) → removed 'repeated header'
ps = paraStart(l)
if ps && ps.num===expected → new para; footMode=false; continue
if isFoot(l) → footnotes++; footMode=true; removed 'footnote'; continue
if footMode → removed 'footnote (continued)'; continue
current.lines.push(l)
```

Hmm, one flaw: frontSet.has(l) check happens even on page 1 after para 1 starts — fine.

Another flaw: `!current` front-matter branch adds to frontSet — but what if paragraph 1 starts on page 3 (weird)? Then pages 1-2 all front matter. Fine.

Wait, there's also a subtle issue with frontSet: it includes lines from page 1 masthead like "United Nations". If body text later has a line exactly "United Nations" — removed wrongly. Rare. OK.

Now — the counters note and "How this is computed": I'll write: "How this is computed: pages are joined in order. Lines that are only a page number, the document symbol, or a 'GE.' distribution code are dropped. Footnote lines (a small number followed by text) are removed and counted. A paragraph starts where a line begins with the next expected number and a full stop ('1.', '2.', …); everything until the next start belongs to that paragraph. Found by the code from the page text; reference figures come from the file."

Good — includes required sentence.

Now build the render:

```js
const tbody = document.getElementById('tbody');
const expanded = new Set();
function statusOf(p){...} // cache in p._status
function render(){
  // stats
  statParas.innerHTML = `${paras.length} <span class="of">of ${ref.paragraphs ?? '—'}</span>`;
  ...
}
```

Simpler: set textContent pieces.

Let me write out full code now, carefully.

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Paragraph checker · E/C.12/GC/27</title>
```

Title should use symbol from data — set via JS: document.title = 'Paragraph checker · ' + symbol. In head I can put a generic title and update in script.

Full script:

```js
(function(){
"use strict";
var D = window.WORKSHOP_DATA && window.WORKSHOP_DATA.pdf_text ? window.WORKSHOP_DATA.pdf_text : {};
var records = Array.isArray(D.records) ? D.records : [];
var symbol = D.symbol || '';
var docUrl = D.doc_url || '#';
var source = D.source || '';
var ref = D.reference || {};
var refFirst = ref.first_words || {};
var refParas = (typeof ref.paragraphs === 'number') ? ref.paragraphs : null;
var refFoots = (typeof ref.footnotes === 'number') ? ref.footnotes : null;

document.title = 'Paragraph checker · ' + (symbol || 'UN document');
document.getElementById('docTitle').textContent = D.title || symbol || 'UN document';
var link = document.getElementById('docLink');
link.textContent = symbol || docUrl;
link.href = docUrl;
document.getElementById('sourceLine').textContent = 'Raw PDF text, ' + records.length + ' pages, source: ' + source;
```

Hmm "raw PDF text, N pages" — spec lowercase "raw PDF text, N pages, source: …". I'll write exactly: `Raw PDF text, ${n} pages, source: ${source}` — fine.

Parsing as planned. Then:

```js
function escHtml(s){return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');}
function normWords(s){return String(s).toLowerCase().split(/\s+/).map(function(w){return w.replace(/[^\p{L}\p{N}]/gu,'');}).filter(Boolean);}
function paraText(p){return p.lines.join('\n').replace(/^\s*\n+/,'').replace(/\n+\s*$/,'').replace(/\n{3,}/g,'\n\n');}
```

Hmm — trimming: lines joined; leading blank lines removed via replace(/^\n+/,'') after join? lines may start with '' entries. join('\n') then strip leading/trailing newlines: .replace(/^[\n\s]+/,'')? That would strip leading spaces of first line too — fine. Use .replace(/^\n+/,'').replace(/\n+$/,''). Internal multiple blanks collapse to max 2? "exactly as extracted" — don't collapse; just trim ends. OK: `.replace(/^\n+/,'').replace(/\n+$/,'')`.

firstLine display: `paraText(p).split('\n').map(s=>s.trim()).filter(Boolean).join(' ')` then collapse spaces, slice 90.

statusOf with caching:

```js
function statusOf(p){
  if (p._st) return p._st;
  var key = String(p.num), st;
  if (!Object.prototype.hasOwnProperty.call(refFirst, key)) st = {code:'noref', label:'no reference'};
  else {
    var a = normWords(paraText(p)).slice(0,6);
    var b = normWords(refFirst[key]).slice(0,6);
    var same = a.length===b.length && a.every(function(w,i){return w===b[i];});
    st = same ? {code:'ok', label:'matches'} : {code:'diff', label:'Differs'};
  }
  p._st = st; return st;
}
```

Render table:

```js
var tbody = ..., expanded = new Set(), diffFirst = ...;
function render(){
  var diffs = paras.filter(p=>statusOf(p).code==='diff').length;
  // stats
  el.paras.textContent = paras.length + (refParas!=null ? ' of ' + refParas : '');
  el.foots.textContent = footnotes + (refFoots!=null ? ' of ' + refFoots : '');
  el.diffs.textContent = diffs + ' of ' + paras.length + ' paragraphs';
  // order
  var order = paras.map(function(p,i){return {p:p,i:i};});
  if (diffFirstEl.checked) order.sort(function(a,b){ var d = (statusOf(b.p).code==='diff'?1:0) - (statusOf(a.p).code==='diff'?1:0); return d || a.i-b.i; });
  var html = '';
  order.forEach(function(o){
    var p=o.p, st=statusOf(p);
    var fl = firstLine(p);
    html += '<tr class="row ' + st.code + '" data-num="'+p.num+'">'
      + '<td class="num">'+p.num+'</td>'
      + '<td>'+p.page+'</td>'
      + '<td class="firstline">'+escHtml(fl)+'</td>'
      + '<td><a href="'+escHtml(docUrl)+'" target="_blank" rel="noopener">'+escHtml(symbol)+'</a></td>'
      + '<td><span class="pill '+st.code+'">'+st.label+'</span></td>'
      + '</tr>';
    if (expanded.has(p.num)) {
      var refTxt = Object.prototype.hasOwnProperty.call(refFirst, String(p.num)) ? refFirst[String(p.num)] : null;
      html += '<tr class="detail"><td colspan="5"><div class="detail-flex">'
        + '<div class="fulltext">'+escHtml(paraText(p))+'</div>'
        + '<div class="refbox"><strong>Reference opening words</strong><br>'
        + (refTxt ? escHtml(refTxt) : 'No reference entry for paragraph '+p.num+'.')
        + '<br><br><strong>Result:</strong> ' + st.label + '</div>'
        + '</div></td></tr>';
    }
  });
  tbody.innerHTML = html;
}
tbody.addEventListener('click', function(e){
  var tr = e.target.closest('tr.row'); if(!tr) return;
  var n = +tr.getAttribute('data-num');
  if (expanded.has(n)) expanded.delete(n); else expanded.add(n);
  render();
});
```

Note: e.target.closest — fine in modern browsers.

Removed lines list:

```js
var ul = document.getElementById('removedList');
ul.innerHTML = removed.map(function(r){
  var t = r.line.length>160 ? r.line.slice(0,160)+'…' : r.line;
  return '<li><span class="reason">p. '+r.page+' · '+escHtml(r.reason)+'</span> — '+escHtml(t)+'</li>';
}).join('');
document.getElementById('removedSummary').textContent = 'Lines removed as headers, footers and footnotes (' + removed.length + ')';
```

CSV:

```js
document.getElementById('csvBtn').addEventListener('click', function(){
  function f(v){ v=String(v); return /[",\n\r]/.test(v) ? '"'+v.replace(/"/g,'""')+'"' : v; }
  var rows = [['number','page','matches_reference','text']];
  paras.forEach(function(p){
    var st = statusOf(p).code;
    rows.push([p.num, p.page, st==='ok'?'yes':(st==='diff'?'no':'no reference'), paraText(p)]);
  });
  var csv = rows.map(function(r){return r.map(f).join(',');}).join('\r\n');
  var blob = new Blob([csv], {type:'text/csv;charset=utf-8'});
  var a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = (symbol ? symbol.replace(/[^\w.-]+/g,'_') : 'paragraphs') + '_paragraph_check.csv';
  document.body.appendChild(a); a.click(); document.body.removeChild(a);
  setTimeout(function(){URL.revokeObjectURL(a.href);}, 1000);
});
```

diffFirst change → render.

Empty data guard: if records.length===0 → show message in table area.

Also stats labels: "Paragraphs found", "Footnotes removed", "Opening words differ". With sub note.

HTML body:

```html
<div class="wrap">
<header>
  <h1 id="docTitle"></h1>
  <p class="meta">Symbol: <a id="docLink" target="_blank" rel="noopener"></a></p>
  <p class="meta" id="sourceLine"></p>
</header>

<section class="card">
  <div class="stats">
    <div class="stat"><div class="big" id="statParas"></div><div class="lbl">paragraphs found (reference: …)</div></div>
    ...
  </div>
  <p class="note">Found by the code from the page text; reference figures come from the file.</p>
  <p class="note"><strong>How this is computed:</strong> …</p>
</section>
```

Hmm, labels: for paras stat, big shows "N of 90", label "paragraphs found / in reference". For footnotes: "M of K", label "footnotes removed / in reference". For differs: "X of N", label "paragraphs whose opening words differ". Good.

Table section:

```html
<section class="card">
  <div class="controls">
    <label class="chk"><input type="checkbox" id="diffFirst"> Show differences first</label>
    <button id="csvBtn" type="button">Download CSV</button>
  </div>
  <p class="note">One row per paragraph found in the page text. Click a row to see the full extracted paragraph and the reference opening words. The symbol links to the document.</p>
  <div class="tablewrap">
  <table>
    <thead><tr><th>#</th><th>Page</th><th>First line</th><th>Symbol</th><th>Opening words</th></tr></thead>
    <tbody id="tbody"></tbody>
  </table>
  </div>
</section>

<details class="card" id="removedDetails">
  <summary id="removedSummary"></summary>
  <ul class="removed-list" id="removedList"></ul>
</details>
</div>
```

Column header "Opening words" for the match column — spec calls it a "Differs" mark; header "vs reference" maybe. I'll use "Opening words vs reference".

Now double-check the required note placement: "Under them: 'Found by the code from the page text; reference figures come from the file.'" — yes, under the three counters. ✓.

Check success: "first counter reads 'N of 90'" — big text "N of 90" where 90 = ref.paragraphs. ✓ (assuming data has 90).

"Clicking row 1 shows text starting 'A clean, healthy and sustainable environment'" — para 1 text: lines after "1." line → "A clean, healthy and sustainable environment is an essential precondition..." ✓.

"Every row marked 'Differs' shows the reference words it was compared with" — detail row shows refbox with reference opening words. ✓.

Now, one more consideration on paraStart regex and the expected-number rule with the sample: page 1 lines: "E/C.12/GC/27" (symbol removed), "United Nations" (front), "Economic and Social Council" (front), "Distr.: General" (front), "6 November 2025" (front — wait, isDigits? "6 November 2025" is not only digits → front matter ✓), "Original: English" (front), "Committee on Economic, Social and Cultural Rights" (front), "General comment No. 27 (2025) on economic, social and" (front), "cultural rights and the environmental dimension of" (front), "sustainable development*" (front), "I." (front), "Introduction" (front), "1." → paraStart num=1===expected → para 1 starts, lines=[] then "A clean, healthy..." pushed. ✓.

Wait — "Distr.: General" — isDist regex /^GE\.\s*\d/ — no. front matter ✓. But careful: is "6 November 2025" caught by isDigits? /^\d{1,4}$/ — no (has spaces). ✓.

Hmm — what about a line "2025" alone somewhere (year alone)? Removed as page number — acceptable per spec.

One more: the frontSet includes "I." — later, could a line "I." appear as a section heading mid-document? Sections are I, II, III... "I." only once. OK.

But wait — frontSet also includes "Introduction". If mid-document a heading line is exactly "Introduction" — unlikely. OK.

Another potential issue: pages 2+ might begin with lines like "E/C.12/GC/27" (removed) and possibly "2" at end (removed). But some UN PDFs repeat "United Nations" etc.? frontSet handles.

What about a page starting with the title continuation? No.

Now — footnotes in this document: E/C.12/GC/27 likely has footnotes like "* ..." or numbered. If they're asterisk footnotes ("* See ..."), my isFoot won't catch them; they'd glue into the last paragraph of the page. Then footnote counter = 0 vs reference K → shows mismatch, and the app honestly reports it. But spec says footnotes are "a small number then text" — trust it.

Hmm, wait — actually let me reconsider: maybe footnotes in the converted text look like "1\nText of footnote" (number alone, text next line)? Then "1" alone → isDigits → removed as "page number" (not counted as footnote). Footnote count would be 0. The spec explicitly describes footnote lines as "a small number then text" — same line. Trust.

Also possible: footnote lines like "1 See general comment No. 8..." — caught. ✓.

Now, the footMode continuation: after first footnote line on a page, subsequent lines until page end are footnote continuations — but what if the page's last body paragraph continues after... no, footnotes are at foot. But careful: what if a footnote-looking false positive occurs mid-paragraph (e.g., "3 per cent")? Then footMode=true and the REST OF THE PAGE gets removed as footnote continuation! That's catastrophic for that page — all remaining lines removed. Hmm! That's a real risk given my earlier concern. The spec's simple rule would have the same issue if implemented naively... but the spec says footnote lines are "at the foot of a page" — maybe I should use position: only treat footnote-start lines as footnotes if they occur after the last... hmm.

Let me add a positional guard to reduce damage: a footnote-start line only counts if it appears after a blank line OR after we've already seen ≥1 paragraph on this page AND ... hmm, still could be mid-paragraph after a blank line? Paragraphs in the PDF text: are there blank lines between paragraphs? In the sample, "1.\nA clean..." — no blank between "1." and text. Between paragraphs, likely blank line(s). So blank-line-then-"3 per cent" could still be a wrapped line? If paragraphs are separated by blank lines, a wrapped continuation wouldn't follow a blank line. So guard: footnote start requires previous non-removed line was blank OR footMode already true OR it's... hmm, but what if converter puts footnotes immediately after body without blank? 

Trade-off. Let me think about which failure is worse. If I require blank-line-before: risk missing footnotes that directly follow body text → they glue into last paragraph → paragraph differs flagged, footnote count low. If I don't require: a mid-paragraph "N word" line nukes the rest of the page. The second is much worse. But also, with footMode continuation, even the guard on the start line doesn't protect continuations... 

Alternative safer design: don't use footMode continuation at all. Just remove individual footnote-start lines (count them), and let continuation lines (if any) glue into the paragraph — flagged as differs, visible. Hmm, but then footnote text pollutes paragraphs.

Middle ground: footMode continuation only until the next blank line? I.e., footnote block = consecutive lines starting from a footnote-start line, continuing while lines are non-blank and not paragraph-starts and not header lines; a blank line ends footMode. Footnotes at page foot are usually contiguous (possibly with blank lines between them though...). Ugh.

Let me think about actual UN PDF conversion output. The sample page 1: header block, blank lines between blocks ("E/C.12/GC/27\n\nUnited Nations\n\nEconomic and Social Council\n\nDistr.: General\n6 November 2025\nOriginal: English\n\nCommittee..."). So blank lines exist between blocks. Footnotes at page bottom typically appear after a blank line, contiguous or with blanks between. Body paragraphs: "1.\nA clean, healthy...\n...truncated" — the sample shows continuous text; between paragraph 1 and 2 there's probably a blank line.

Given uncertainty, I'll implement: footnote-start requires that the previous kept line (in the current page, ignoring removed lines) was blank OR footMode is already true OR no paragraph has started yet on this page? Hmm, "no paragraph yet on this page" — page 1 footnotes? No.

Actually, simpler robust approach: footnote-start line = matches isFoot AND (previous line in raw page was blank OR footMode). And footMode continuation: non-blank, non-para-start, non-header lines while footMode; blank line sets footMode=false? But footnotes separated by blank lines would then end footMode, and the next footnote-start line still matches isFoot and (prev line blank) → starts again. ✓. And a false-positive "3 per cent" mid-paragraph: previous line is body text (non-blank) → NOT treated as footnote → stays in paragraph. ✓ Much safer! And a false positive right after a blank line (start of a wrapped... no—after a blank line comes a new paragraph or heading, which wouldn't start with "3 per cent" unless the paragraph's first wrapped line... the paragraph start line "5." comes first). Actually a paragraph's text could wrap such that a line starts with "3 per cent" — but that line's previous line is body text (non-blank) → safe. Only if the paragraph's FIRST text line starts with "3 per cent" (i.e., right after "5." line — previous line is "5." non-blank → safe; after blank? no). Hmm, what about a line right after a blank line inside a paragraph (if converter inserts blank lines mid-paragraph)? Unlikely.

So rule: isFoot(l) && (prevRawBlank || footMode) → footnote. Where prevRawBlank = the previous raw line of the page was blank (or it's the first line of the page? then no). Let me track `prevBlank` per page: set true when raw line is blank, false otherwise (after processing non-blank). Also footMode persists across blank lines? If footnotes are separated by blank lines, and I keep footMode true across blanks, then a body line after footnotes... there is none (footnotes at foot). But if footMode persists across a blank and then a paragraph start appears, paraStart check comes first → OK. Let me keep footMode sticky within the page once set (until a paragraph start resets it). And footnote-start condition: isFoot(l) && (footMode || prevBlank). Continuation: footMode && !paraStart && !isFoot-start... wait if footMode and line matches isFoot → it's another footnote start (count it). If footMode and line doesn't match isFoot → continuation (remove, don't count). If footMode and paraStart matches expected → new paragraph, footMode=false.

Hmm, but with footMode sticky, a false-positive footnote-start (after blank) would set footMode and then remove all subsequent non-para lines on the page. When could a line after a blank match isFoot? A new paragraph starts with "N." (paraStart, checked first) — safe. A heading line "3 something"? Headings are Roman numerals here. A wrapped line after blank — only if converter breaks oddly. I think acceptable.

Actually, wait: what about the very common pattern where the page footer is like "2" (removed) — fine.

Also: what if footnotes appear BEFORE body on a page? No.

OK, implement with prevBlank tracking. Also note: prevBlank should consider raw lines including removed ones? Use raw line blankness — simpler: track last raw line was blank.

Edge: first line of page is footnote-start? prevBlank=false initially, footMode=false → not footnote → glued. Unlikely (pages start with symbol header). Fine.

Now let me also reconsider: should footnote-start require prevBlank, or should I also allow "previous kept line was a footnote"? footMode covers that.

Alright. Another point: the removed-lines list reason for continuations: "footnote (continued)".

Now, counting: footnotes counts footnote-start lines only. Reference footnotes = number of footnotes. If each footnote is one entry starting with number → match. ✓.

Let me now also handle potential "\u00a0" non-breaking spaces — trim handles \s? \s includes \u00a0 in JS? Yes, \s matches \u00a0. Good. Also normalize internal nbsp in normWords split — \s covers it.

Now write everything. Also add a small "adopted" line? Skip.

Let me also make sure the app explains what it shows (requirement: "the app itself must explain what it shows") — the notes do that.

Line count check — should be fine under 700.

One more detail: `firstLine(p)`: 
```js
function firstLine(p){
  var t = paraText(p).split('\n').map(function(s){return s.trim();}).filter(Boolean).join(' ').replace(/\s+/g,' ');
  return t.length>90 ? t.slice(0,90)+'…' : t;
}
```

Stats elements: I'll structure:

```html
<div class="stat"><div class="big" id="statParas">–</div><div class="lbl">paragraphs found / in the reference</div></div>
<div class="stat"><div class="big" id="statFoots">–</div><div class="lbl">footnotes removed / in the reference</div></div>
<div class="stat"><div class="big" id="statDiffs">–</div><div class="lbl">paragraphs whose opening words differ</div></div>
```

render sets: statParas.textContent = paras.length + (refParas!=null?' of '+refParas:''); etc. statDiffs = diffs + ' of ' + paras.length.

Note under: "Found by the code from the page text; reference figures come from the file."

How-computed note: "How this is computed: the pages are joined in order. Lines that are only a page number, the document symbol, or a “GE.” distribution code are dropped. Footnote lines (a small number followed by text, at the foot of a page) are removed and counted. A paragraph starts where a line begins with the next expected number and a full stop (“1.”, “2.”, …); all text until the next start belongs to that paragraph. “Differs” compares the first six words with the reference, ignoring case, punctuation and extra spaces."

Good.

Also handle case records empty: tbody.innerHTML = '<tr><td colspan="5">No page text found in the attached file.</td></tr>'.

Write final HTML now. Also ensure no external resources. Use system fonts only.

Let me write the code fully and carefully, checking syntax mentally.

Also: `e.target.closest` — if e.target is a text node? In DOM events target is element. OK. But if click on <a> inside row — closest finds tr.row; clicking the symbol link would also toggle row AND open link. Hmm — clicking link opens new tab and toggles expansion. Slightly annoying but acceptable? Better: if e.target.closest('a')) return; Let me add that.

Also the checkbox label and button in controls.

Edge: paras could be empty → stats show 0.

Let me now also double check paraStart regex against a line like "1. A clean..." — m[1]="1", m[2]="A clean...". ✓. Against "10." alone ✓. Against "1.Introduction" (no space) — no match (needs \s or end) → falls to isFoot? "1.Introduction": /^\d{1,2}\s/ no → body text. OK.

Against "Art. 1." — starts with "Art" → no.

Against "2025." alone: num=2025, ≠ expected → not start; isFoot? "2025." → /^\d{1,2}\s/ — "20" then "2" not \s... regex ^\d{1,2}\s: tries "2" then needs \s but next is "0" → backtrack "20" then next "2" not \s → no match. → body text. Fine.

Now, `isDigits` /^\d{1,4}$/ — a line "90" (paragraph count?) unlikely. Page numbers up to 20. OK.

symbolRe: symbol "E/C.12/GC/27" → escaped "E/C\.12/GC/27" → regex ^E/C\.12/GC/27\s*\d*$ — matches "E/C.12/GC/27" and "E/C.12/GC/27 2". ✓.

isDist: /^GE\.\s*\d/ — "GE.25-01234" ✓. Also maybe "GE. 25..." ✓.

Now, frontSet: note that I add front-matter lines to frontSet — but I should NOT add lines that were removed as symbol/digits/dist (they're handled earlier). ✓ order.

One more: after para 1 starts, `if (!current)` never true again, so frontSet only grows on page 1 (or until para 1). ✓.

Also: what if the document has front matter on page 1 that includes a line matching isFoot, e.g., "27 (2025)..."? Not at start. OK.

Now the removed list could include long title lines — truncated to 160 chars. ✓.

CSV filename: symbol sanitized.

Let me also compute and show in the removed summary the breakdown? Keep simple: total count.

Now, write it all out. I'll aim for clean, complete code.

Also remember: before code block, at most three short sentences describing what I built. After code block: nothing.

Let me write the final answer.

One more check on the "How we will know it works" — "The table numbers run 1, 2, 3 … without gaps" — with strict expected rule, numbers are consecutive by construction (expected increments by 1 each start). ✓ "at least 30 rows" — depends on data; 90 paragraphs expected. ✓.

Also "paragraphs found / paragraphs in the reference" — "N of 90". ✓.

Potential gotcha: what if some paragraph start lines have the number and text but with the number being e.g. "1." followed by tab — \s covers tab. ✓.

What about Windows line endings — split(/\r?\n/). ✓.

Now write.

Also, I want the detail row's full text to be "exactly as extracted" — paraText preserves line breaks. ✓. And refbox beside it. ✓.

Let me write the code:

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Paragraph checker</title>
<style>
:root{--accent:#1f6fb2;--ink:#1c2733;--muted:#5b6b7b;--line:#dfe6ee;--bg:#f6f8fa}
*{box-sizing:border-box}
html,body{margin:0;padding:0}
body{font:16px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif;color:var(--ink);background:var(--bg)}
.wrap{max-width:1040px;margin:0 auto;padding:26px 20px 64px}
h1{font-size:1.45rem;line-height:1.3;margin:0 0 8px}
a{color:var(--accent)}
.meta{margin:2px 0;color:var(--muted)}
.card{background:#fff;border:1px solid var(--line);border-radius:10px;padding:16px 18px;margin:18px 0}
.stats{display:flex;gap:14px;flex-wrap:wrap}
.stat{flex:1 1 220px;border:1px solid var(--line);border-radius:10px;padding:12px 16px;background:#fbfcfe}
.stat .big{font-size:1.4rem;font-weight:700;color:var(--accent)}
.stat .lbl{color:var(--muted);font-size:.9rem;margin-top:2px}
.note{color:var(--muted);font-size:.9rem;margin:10px 0 0}
.controls{display:flex;align-items:center;gap:18px;flex-wrap:wrap;margin-bottom:6px}
button{background:var(--accent);color:#fff;border:0;border-radius:8px;padding:9px 16px;font-size:.95rem;cursor:pointer}
button:hover{background:#175a91}
label.chk{display:inline-flex;align-items:center;gap:8px;cursor:pointer;user-select:none}
.tablewrap{overflow-x:auto;margin-top:8px}
table{width:100%;border-collapse:collapse}
th,td{text-align:left;padding:8px 10px;border-bottom:1px solid var(--line);vertical-align:top;font-size:.94rem}
thead th{background:#eef3f8;font-size:.8rem;text-transform:uppercase;letter-spacing:.05em;color:#3d4c5c;white-space:nowrap}
tr.row{cursor:pointer}
tr.row:hover{background:#f2f7fc}
tr.row.diff{background:#fdf4f3}
tr.row.diff:hover{background:#fbeae8}
td.num{font-weight:700;white-space:nowrap}
.firstline{color:#33414f;min-width:280px}
.pill{display:inline-block;padding:2px 10px;border-radius:999px;font-size:.78rem;font-weight:700;white-space:nowrap}
.pill.ok{background:#e6f4ea;color:#1e7e34}
.pill.diff{background:#fbe9e7;color:#b3261e}
.pill.noref{background:#eceff3;color:#5b6b7b}
tr.detail td{background:#fbfcfe;padding:12px 10px}
.detail-flex{display:flex;gap:16px;flex-wrap:wrap}
.fulltext{flex:2 1 460px;white-space:pre-wrap;word-break:break-word;background:#fff;border:1px solid var(--line);border-radius:8px;padding:12px 14px;font-size:.92rem;max-height:360px;overflow:auto}
.refbox{flex:1 1 240px;background:#f2f7fc;border:1px solid var(--line);border-radius:8px;padding:12px 14px;font-size:.92rem}
details.card summary{cursor:pointer;font-weight:700}
.removed-list{list-style:none;margin:12px 0 0;padding:0;max-height:340px;overflow:auto;font-size:.88rem}
.removed-list li{padding:5px 0;border-bottom:1px dashed var(--line);color:#33414f}
.reason{color:var(--muted)}
</style>
</head>
<body>
<div class="wrap">
  <header>
    <h1 id="docTitle"></h1>
    <p class="meta">Symbol: <a id="docLink" target="_blank" rel="noopener"></a></p>
    <p class="meta" id="sourceLine"></p>
  </header>

  <section class="card">
    <div class="stats">
      <div class="stat"><div class="big" id="statParas">–</div><div class="lbl">paragraphs found / in the reference</div></div>
      <div class="stat"><div class="big" id="statFoots">–</div><div class="lbl">footnotes removed / in the reference</div></div>
      <div class="stat"><div class="big" id="statDiffs">–</div><div class="lbl">paragraphs whose opening words differ</div></div>
    </div>
    <p class="note">Found by the code from the page text; reference figures come from the file.</p>
    <p class="note"><strong>How this is computed:</strong> the pages are joined in order. Lines that are only a page number, the document symbol, or a “GE.” distribution code are dropped. Footnote lines (a small number followed by text, at the foot of a page) are removed and counted. A paragraph starts where a line begins with the next expected number and a full stop (“1.”, “2.”, …); all text until the next start belongs to that paragraph. “Differs” means the paragraph’s first six words do not match the reference’s, comparing word by word while ignoring case, punctuation and extra spaces.</p>
  </section>

  <section class="card">
    <div class="controls">
      <label class="chk"><input type="checkbox" id="diffFirst"> Show differences first</label>
      <button id="csvBtn" type="button">Download CSV</button>
    </div>
    <p class="note">One row per paragraph found in the page text; click a row to open the full paragraph exactly as extracted, with the reference’s opening words beside it. Every row links the symbol to the document.</p>
    <div class="tablewrap">
      <table>
        <thead><tr><th>#</th><th>Page</th><th>First line</th><th>Symbol</th><th>Opening words vs reference</th></tr></thead>
        <tbody id="tbody"></tbody>
      </table>
    </div>
  </section>

  <details class="card">
    <summary id="removedSummary">Lines removed as headers, footers and footnotes</summary>
    <ul class="removed-list" id="removedList"></ul>
  </details>
</div>

<script>
(function(){
"use strict";
var D = (window.WORKSHOP_DATA && window.WORKSHOP_DATA.pdf_text) || {};
var records = Array.isArray(D.records) ? D.records : [];
var symbol = D.symbol || "";
var docUrl = D.doc_url || "#";
var source = D.source || "";
var ref = D.reference || {};
var refFirst = ref.first_words || {};
var refParas = (typeof ref.paragraphs === "number") ? ref.paragraphs : null;
var refFoots = (typeof ref.footnotes === "number") ? ref.footnotes : null;

document.title = "Paragraph checker · " + (symbol || "UN document");
document.getElementById("docTitle").textContent = D.title || symbol || "UN document";
var link = document.getElementById("docLink");
link.textContent = symbol || docUrl;
link.href = docUrl;
document.getElementById("sourceLine").textContent = "Raw PDF text, " + records.length + " page" + (records.length===1?"":"s") + ", source: " + source;

/* ---------- split the raw page text ---------- */
function escRe(s){ return String(s).replace(/[.*+?^${}()|[\]\\]/g, "\\$&"); }
var symbolRe = symbol ? new RegExp("^" + escRe(symbol) + "\\s*\\d*$") : null;
function isDigits(l){ return /^\d{1,4}$/.test(l); }
function isDist(l){ return /^GE\.\s*\d/.test(l); }
function isFoot(l){ return /^\d{1,2}\s+\S/.test(l); }
function paraStart(l){ var m = l.match(/^(\d+)\.(?:\s+(.*))?$/); return m ? { num: +m[1], rest: m[2] || "" } : null; }

var removed = [];   // {page, reason, line}
var paras = [];     // {num, page, lines: []}
var footnotes = 0;
var expected = 1;
var current = null;
var frontSet = new Set();

for (var i = 0; i < records.length; i++){
  var rec = records[i];
  var page = rec.page;
  var rawLines = String(rec.text || "").split(/\r?\n/);
  var footMode = false;
  var prevBlank = false;
  for (var j = 0; j < rawLines.length; j++){
    var l = rawLines[j].trim();
    if (!l){
      if (current && !footMode) current.lines.push("");
      prevBlank = true;
      continue;
    }
    prevBlank = false;
    if (isDigits(l)){ removed.push({page:page, reason:"page number", line:l}); continue; }
    if (symbolRe && symbolRe.test(l)){ removed.push({page:page, reason:"document symbol / footer", line:l}); continue; }
    if (isDist(l)){ removed.push({page:page, reason:"distribution code", line:l}); continue; }
    if (!current){ frontSet.add(l); removed.push({page:page, reason:"header (before the first paragraph)", line:l}); continue; }
    if (frontSet.has(l)){ removed.push({page:page, reason:"repeated header", line:l}); continue; }
    var ps = paraStart(l);
    if (ps && ps.num === expected){
      current = { num: expected, page: page, lines: ps.rest ? [ps.rest] : [] };
      paras.push(current);
      expected++;
      footMode = false;
      continue;
    }
    if (isFoot(l) && (footMode || prevBlank)){
      footnotes++;
      footMode = true;
      removed.push({page:page, reason:"footnote", line:l});
      continue;
    }
    if (footMode){
      removed.push({page:page, reason:"footnote (continued)", line:l});
      continue;
    }
    current.lines.push(l);
  }
}
```

Wait — bug: `prevBlank = false;` set for every non-blank line, but I set it before the removal checks — fine, prevBlank refers to previous raw line. But note: I set prevBlank=false at top for non-blank, then checks. But the footnote-start condition uses prevBlank of the *previous* line — since I reset prevBlank=false when current line is non-blank BEFORE checking, the condition `prevBlank` at check time still holds the previous line's value? No! I set `prevBlank = false` immediately after the blank check, before using it in the footnote condition. Bug! Fix: capture `var wasBlank = prevBlank; prevBlank = false;` then use wasBlank.

Let me restructure:

```js
var l = rawLines[j].trim();
if (!l){ if (current && !footMode) current.lines.push(""); prevBlank = true; continue; }
var wasBlank = prevBlank;
prevBlank = false;
... use wasBlank in footnote condition ...
```

Also footMode should reset on blank? I decided sticky until paragraph start. But consider: footnotes at foot, then page ends. Next page footMode resets (declared per page). ✓. If a blank line occurs between body and footnotes, footMode still false until first footnote line — which requires wasBlank true → ✓ (blank before footnotes). If converter puts footnotes immediately after body without blank — missed; they'd glue into paragraph. Acceptable trade-off (safer).

Hmm, wait — actually, also consider: footnote-start when footMode already true — condition `(footMode || wasBlank)` ✓.

But one more scenario: footnote lines separated by blank lines: footnote1, blank, footnote2. After blank, prevBlank=true; footnote2 line: isFoot && wasBlank → counted ✓. footMode stays true across the blank (I don't reset on blank) — but the blank line itself: `if (current && !footMode) current.lines.push("")` — footMode true → not pushed ✓.

But danger: footMode sticky + a false positive after blank → rest of page removed. E.g., body line after blank starting with "3 per cent"? After a blank line comes a new paragraph start "N." (paraStart checked first) or a heading. If heading "3. Something"? paraStart num=3; if expected≠3 → not start; isFoot? "3." has period → no; footMode false → body text ✓. If heading "3 Something" (no period) after blank → false footnote! Then footMode nukes page. Risk accepted (rare).

Continue code:

```js
/* ---------- helpers ---------- */
function escHtml(s){ return String(s).replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;").replace(/"/g,"&quot;"); }
function normWords(s){
  return String(s).toLowerCase().split(/\s+/).map(function(w){ return w.replace(/[^\p{L}\p{N}]/gu, ""); }).filter(Boolean);
}
function paraText(p){
  return p.lines.join("\n").replace(/^\n+/, "").replace(/\n+$/, "");
}
function firstLine(p){
  var t = paraText(p).split("\n").map(function(s){ return s.trim(); }).filter(Boolean).join(" ").replace(/\s+/g, " ");
  return t.length > 90 ? t.slice(0, 90) + "…" : t;
}
function statusOf(p){
  if (p._st) return p._st;
  var key = String(p.num), st;
  if (!Object.prototype.hasOwnProperty.call(refFirst, key)){
    st = { code: "noref", label: "no reference" };
  } else {
    var a = normWords(paraText(p)).slice(0, 6);
    var b = normWords(refFirst[key]).slice(0, 6);
    var same = a.length === b.length && a.every(function(w, i){ return w === b[i]; });
    st = same ? { code: "ok", label: "matches" } : { code: "diff", label: "Differs" };
  }
  p._st = st;
  return st;
}
```

Render:

```js
var tbody = document.getElementById("tbody");
var diffFirstEl = document.getElementById("diffFirst");
var expanded = new Set();

function render(){
  var diffs = 0;
  for (var i = 0; i < paras.length; i++) if (statusOf(paras[i]).code === "diff") diffs++;
  document.getElementById("statParas").textContent = paras.length + (refParas != null ? " of " + refParas : "");
  document.getElementById("statFoots").textContent = footnotes + (refFoots != null ? " of " + refFoots : "");
  document.getElementById("statDiffs").textContent = diffs + " of " + paras.length;

  var order = paras.map(function(p, i){ return { p: p, i: i }; });
  if (diffFirstEl.checked){
    order.sort(function(a, b){
      var d = (statusOf(b.p).code === "diff" ? 1 : 0) - (statusOf(a.p).code === "diff" ? 1 : 0);
      return d || a.i - b.i;
    });
  }
  var html = "";
  if (!paras.length){
    html = '<tr><td colspan="5">No page text was found in the attached file.</td></tr>';
  }
  for (var k = 0; k < order.length; k++){
    var p = order[k].p, st = statusOf(p);
    html += '<tr class="row ' + st.code + '" data-num="' + p.num + '">'
      + "<td class='num'>" + p.num + "</td>"
      + "<td>" + p.page + "</td>"
      + "<td class='firstline'>" + escHtml(firstLine(p)) + "</td>"
      + '<td><a href="' + escHtml(docUrl) + '" target="_blank" rel="noopener">' + escHtml(symbol) + "</a></td>"
      + '<td><span class="pill ' + st.code + '">' + st.label + "</span></td>"
      + "</tr>";
    if (expanded.has(p.num)){
      var key = String(p.num);
      var refTxt = Object.prototype.hasOwnProperty.call(refFirst, key) ? refFirst[key] : null;
      html += '<tr class="detail"><td colspan="5"><div class="detail-flex">'
        + '<div class="fulltext">' + escHtml(paraText(p)) + "</div>"
        + '<div class="refbox"><strong>Reference opening words</strong><br>'
        + (refTxt != null ? escHtml(refTxt) : "No reference entry for paragraph " + p.num + ".")
        + "<br><br><strong>Result:</strong> " + st.label + "</div>"
        + "</div></td></tr>";
    }
  }
  tbody.innerHTML = html;
}

tbody.addEventListener("click", function(e){
  if (e.target.closest("a")) return;
  var tr = e.target.closest("tr.row");
  if (!tr) return;
  var n = +tr.getAttribute("data-num");
  if (expanded.has(n)) expanded.delete(n); else expanded.add(n);
  render();
});
diffFirstEl.addEventListener("change", render);
```

Removed list:

```js
document.getElementById("removedSummary").textContent = "Lines removed as headers, footers and footnotes (" + removed.length + ")";
document.getElementById("removedList").innerHTML = removed.map(function(r){
  var t = r.line.length > 160 ? r.line.slice(0, 160) + "…" : r.line;
  return "<li><span class='reason'>p. " + r.page + " · " + escHtml(r.reason) + "</span> — " + escHtml(t) + "</li>";
}).join("");
```

CSV:

```js
document.getElementById("csvBtn").addEventListener("click", function(){
  function f(v){ v = String(v); return /[",\n\r]/.test(v) ? '"' + v.replace(/"/g, '""') + '"' : v; }
  var rows = [["number", "page", "matches_reference", "text"]];
  for (var i = 0; i < paras.length; i++){
    var p = paras[i], st = statusOf(p).code;
    rows.push([p.num, p.page, st === "ok" ? "yes" : (st === "diff" ? "no" : "no reference"), paraText(p)]);
  }
  var csv = rows.map(function(r){ return r.map(f).join(","); }).join("\r\n");
  var blob = new Blob([csv], { type: "text/csv;charset=utf-8" });
  var a = document.createElement("a");
  a.href = URL.createObjectURL(blob);
  a.download = (symbol ? symbol.replace(/[^\w.-]+/g, "_") : "paragraphs") + "_paragraph_check.csv";
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  setTimeout(function(){ URL.revokeObjectURL(a.href); }, 2000);
});

render();
})();
</script>
</body>
</html>
```

Wait — one issue: `p._st` caching with statusOf — fine.

Another: in render, `paras.map` then sort — fine.

Check: `e.target.closest` — e.target could be the tbody itself if clicking padding; closest('tr.row') null → return. ✓.

Check colspan=5 matches 5 columns ✓.

Check the "Differs" pill label exactly "Differs" ✓; "no reference" ✓.

One more consideration: the spec says table row shows "symbol linked to doc_url" — ✓ every row.

"Clicking a row opens the full paragraph beneath it, exactly as extracted, with the reference's first words shown beside it." ✓ detail row beneath.

Also — "A tick box 'Show differences first'" ✓.

Potential issue: `frontSet.has(l)` — frontSet contains page-1 masthead lines; but note the title lines contain "General comment No. 27 (2025) on economic, social and" — if such a line repeated... fine.

Hmm, one more: what if page 1's masthead includes a line that is digits only, like "27"? isDigits catches first → removed as page number, not added to frontSet. Fine.

What about the line "I." — frontSet. Later "II." etc. not in set → body text glued to previous paragraph. Per spec, fine.

Now — the footnote heuristic with wasBlank: page footnotes typically preceded by blank line ✓.

Also — hmm, what about the very common UN footer pattern where the page number is at the TOP of the page (some docs) — handled by isDigits anywhere.

What about "E/C.12/GC/27" appearing at top of pages 2+ — symbolRe ✓.

I think there's one more subtle thing: the sample page 1 shows "Distr.: General\n6 November 2025\nOriginal: English" — all front matter ✓.

Also the sample shows the doc has "I.\nIntroduction\n1.\nA clean..." — wait, actually looking at sample: "sustainable development*\nI.\n\nIntroduction\n1.\nA clean, healthy..." — there's "I." then blank then "Introduction" then "1." then text. All before para 1 → front matter ✓.

Now, the success criterion "Clicking row 1 shows text starting 'A clean, healthy and sustainable environment'" — para 1 lines: after "1." line, next lines: "A clean, healthy and sustainable environment is an essential precondition for the\nenjoyment..." → paraText starts "A clean, healthy..." ✓.

Also check: could "1." line be "1. " with trailing space → trimmed to "1." ✓.

Edge: what if the converter emitted "1. A clean..." on one line — handled ✓.

Now the counters: refParas=90 presumably → "N of 90" ✓.

Line count of file: roughly 260 lines. ✓ under 700.

Also requirement: "Before the code block: at most three short sentences saying what you built or changed." I'll write 2-3 sentences.

Also — "the app itself must explain what it shows" ✓ via notes.

One more requirement check: "A 'Download CSV' button" ✓. "The CSV holds number, page, whether it matches the reference, and the full text with values quoted, built and saved in the browser." ✓ (quoting when needed — "with values quoted" — my f() quotes only when necessary; spec says "with values quoted" — maybe always quote the text field? To be safe, always quote text and matches columns? "values quoted" likely means properly quoted/escaped. I'll quote fields containing special chars — standard CSV. Hmm, to hew closer, I could always quote the text column. Let me always quote the text field: f always quotes? If I always quote all fields, spreadsheets handle fine. I'll make f always wrap in quotes and double internal quotes — simplest and satisfies "values quoted". Actually always-quoting is valid CSV. Do that: `return '"' + v.replace(/"/g,'""') + '"';` for all fields. Fine.

Also "built and saved in the browser" ✓ Blob.

Double-check no fetch/external ✓. Chart.js not needed ✓.

One more: "Every row that shows a document has its symbol, linked to doc_url in a new tab" ✓.

Also the header: "Title and symbol linked to doc_url, with one line: 'raw PDF text, N pages, source: …'" ✓.

I think there might be an issue with `prevBlank` when the previous raw line was removed (e.g., symbol line) — prevBlank=false then; footnote after symbol line? Footnotes are at foot, preceded by body/blank. Fine.

Also: what if a page begins directly with a footnote continuation from previous page? No.

Let me also reconsider `isDigits` removing a lone "1" that's actually a footnote marker on its own line — per spec, lone digits = page number. OK.

Now, also think: should blank lines inside paragraphs be preserved in CSV text? paraText keeps internal "\n\n" — CSV quotes them ✓.

Alright — also the note "Found by the code from the page text; reference figures come from the file." — exact sentence required ✓.

Also add data-source? No studio.ask used ✓.

Final check of the intro text before code: 2–3 sentences, no code. E.g.: "I built a paragraph-checking tool for E/C.12/GC/27: it splits the raw PDF text into numbered paragraphs, compares each opening against the reference answer key, and flags converter damage. Below the counters you can sort differences first, expand any row for the full extracted text, download a CSV, and inspect every removed header/footer/footnote line."

Good. Write final answer.