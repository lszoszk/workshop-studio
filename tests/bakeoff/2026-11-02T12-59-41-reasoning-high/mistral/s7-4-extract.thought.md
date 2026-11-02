Let me analyze the task. I need to build an HTML app that:

1. Splits raw PDF text of E/C.12/GC/27 into numbered paragraphs
2. Shows where the converter damaged text
3. Compares against reference (paragraphs count, footnotes count, first_words)

Data: `WORKSHOP_DATA.pdf_text` with `title`, `symbol`, `doc_url`, `source`, `count`, `records` (page, text), `reference` (paragraphs, footnotes, adopted, first_words).

Rules:
- Join pages in order
- Remove lines that are only a page number, only the document symbol, or distribution code ("GE." followed by digits)
- Footnote lines (small number then text at foot of page) removed and counted
- Paragraph starts at line beginning with next expected number + full stop ("1.", "2."...). Number usually stands alone on its line, paragraph on lines after. Numbers out of sequence don't start a paragraph. Text runs until next start.
- Lettered sub-paragraphs stay inside numbered paragraph
- "Differs" = first six words don't match reference, comparing word by word ignoring case, punctuation, extra spaces. If no reference entry, show "no reference"
- CSV: number, page, match status, full text quoted, built and saved in browser

Display:
1. Title + symbol linked to doc_url, one line "raw PDF text, N pages, source: …"
2. Three counters: paragraphs found / reference; footnotes removed / reference; paragraphs whose opening words differ. Note under: "Found by the code from the page text; reference figures come from the file."
3. Table: number, page where starts, first line (~90 chars), symbol linked to doc_url, "Differs" mark. Checkbox "Show differences first" moves marked rows to top. Clicking row opens full paragraph beneath, exactly as extracted, with reference's first words beside it.
4. "Download CSV" button
5. Collapsed list "Lines removed as headers, footers and footnotes"

Let me think about the parsing algorithm carefully.

The PDF text sample: page 1 starts with:
```
E/C.12/GC/27

United Nations

Economic and Social Council

Distr.: General
6 November 2025
Original: English

Committee on Economic, Social and Cultural Rights

General comment No. 27 (2025) on economic, social and
cultural rights and the environmental dimension of
sustainable development*
I.

Introduction
1.
A clean, healthy and sustainable environment is an essential precondition for the
enjoyment of economic, social and cultural rights. ...
```

So lines to remove: "E/C.12/GC/27" (symbol alone), "Distr.: General"? Hmm — the rule says remove lines that are only a page number, only the document symbol, or a distribution code ("GE." followed by digits). "Distr.: General" is not exactly "GE." followed by digits. But maybe in the real data the distribution line is like "GE.25-12345". The sample shows "Distr.: General" — hmm. The rule says distribution code ("GE." followed by digits). I'll implement: line matches /^GE\.\s*\d/ → remove. Also maybe "Distr.: General" — I could also remove lines starting with "Distr.:" — but the spec says only those three categories. To be safe, I'll remove: pure page number lines (^\d{1,4}$), symbol-only lines (line === symbol, or line matches the symbol pattern), and GE. codes. Maybe also "Distr.: General" and "Original: English"? The spec says "where it says nothing, keep it simple" — but the collapsed list is "Lines removed as headers, footers and footnotes". I'll remove the three specified categories plus maybe lines like "Distr.: General"? Hmm, better to stick to spec but be a bit generous: remove lines that are only a page number, only the symbol, GE. codes. Also perhaps "United Nations", "Economic and Social Council"? Those are headers. The spec says "Remove lines that are only a page number, only the document symbol, or a distribution code". I'll implement exactly those, but I might also treat "Distr.: General" as a header... Actually the sample page 1 shows "Distr.: General\n6 November 2025\nOriginal: English" — these are cover-page lines, not repeated headers. The repeated page headers in UN docs are usually the symbol on one line and "GE.xx-xxxxx" on another, plus page number. Let me just implement the three rules, and additionally remove lines matching /^Distr\.:/ and /^Original:/ maybe? The spec is explicit; adding more could remove substantive text? Unlikely — "Distr.:" lines are never paragraph text. But to be safe and honest, I'll remove exactly: page-number-only lines, symbol-only lines, GE. distribution codes. I could also add "Distr.: General" as header since it's clearly a header... The collapsed list title says "headers, footers and footnotes" so headers are expected. I'll include a small set of header patterns: symbol line, GE code, "Distr.: ..." line, "Original: ..." line? Hmm, "Original: English" — could that appear mid-paragraph? No. But keep it simple: I'll remove lines matching:
- /^\d{1,4}$/ (page number alone)
- line.trim() === symbol, or line matches /^E\/C\.12\/GC\/27$/ — better: compare to data symbol; also generic: line matches /^[A-Z]\// and equals symbol. I'll check `line.trim() === symbol`.
- /^GE\.\s*\d/ 
- /^Distr\.:/ and /^Original:/ — I'll include these as headers; they're safe.

Actually wait — the footnote detection: "Footnote lines (a small number then text, at the foot of a page)". In UN PDFs, footnotes appear at the bottom of the page like "1 Some text..." or "___________\n1 text". The sample page 1 ends with "tr\n[… rest of the page omitted in this sample]" — that's just the sample truncation. Real data has 20 pages with footnotes mixed in.

How to detect footnote lines? A line that starts with a small number (1-3 digits) followed by space and text, located near the foot of a page. But paragraph numbers also start lines with numbers... but paragraph starts are "next expected number + '.'". Footnote numbers typically don't have a full stop? In UN documents footnotes are like "1 Text of footnote" — actually often with the number followed by a space, no period. Hmm, but could be "1." too. The spec says "a small number then text, at the foot of a page". So detection: within the last few lines of a page's text (say last 6 lines?), a line matching /^\d{1,3}\s+\S/ (number, space, text, no period) → footnote. Also possibly a separator line of underscores "____" before footnotes.

But careful: paragraph number lines "1." stand alone — those have a period. Footnote lines "1 text" — number then space then text without period. But what if a footnote number line is just "1" alone? Unlikely.

Also, the footnote could span multiple lines (wrapped). Hmm. "Footnote lines (a small number then text, at the foot of a page) are removed from the paragraphs and only counted." Count = number of footnote lines? Or number of footnotes? Reference has `footnotes` count. The counter is "footnotes removed / footnotes in the reference". So we count footnotes — probably each footnote-start line counts as one footnote. But wrapped continuation lines also need removal. Hmm.

Let me think about the actual format of E/C.12/GC/27 PDF text. UN General Comments have footnotes like:

```
________________________________________________________________________
1	See ...
```

Actually in UN docs footnotes at page bottom: a horizontal line, then "1 Footnote text..." possibly wrapped over multiple lines.

Given the converter output, a page might look like:

```
...end of paragraph text on page 3
E/C.12/GC/27
GE.25-xxxxx
4
_________________________________________________________________
1	Some footnote text that may wrap
onto another line
2	Another footnote
5. Next paragraph starts...
```

Hmm wait, page number "4" alone — removed as page-number-only line. Symbol and GE removed. Then footnote separator "____..." — should be removed too (it's a footer). Then footnote lines.

Detection strategy per page:
1. Split page text into lines.
2. Remove header/footer lines: symbol-only, GE code, page-number-only, "Distr.:", "Original:", underscore separator lines (^[_—-]{5,}$).
3. Identify footnote region: lines near the end of the page that match /^\d{1,3}\s+\S/ (number + whitespace + text, no period after number) — but only if they appear after the last "real" content? Hmm, tricky. Actually the spec says "at the foot of a page". So: scan from the bottom? Or: a footnote line is a line matching /^\d{1,3}\s+\S/ where the number is NOT the next expected paragraph number followed by a period... wait paragraph starts have a period: "5." Footnotes: "1 text" — no period. But what if footnote is "1." with period? In UN style, footnotes in the PDF are typically "1" followed by tab/space. Let me consider: the paragraph-start rule requires "next expected number and a full stop". So "1." starts paragraph 1 only if expected is 1. A footnote "1 text" (no period) never starts a paragraph. So the rule "numbers out of sequence do not start a paragraph" handles it — but the footnote text would then be absorbed into the preceding paragraph! That's why we need to remove footnote lines separately.

So footnote detection: lines matching /^\d{1,3}\s+\S/ (small number, whitespace, then text — no period immediately after number) that occur in the foot region of a page. How to define foot region? Perhaps: after the last line of the page that... hmm. Alternative: any line matching /^\d{1,3}\s+\S/ where the number is not followed by "." — but a wrapped paragraph line could start with a number, e.g., "2025 was the year..." — "2025" is 4 digits, "small number" = 1-3 digits. A line like "3 countries..." mid-paragraph? Possible but rare. The spec says "at the foot of a page", so restrict to the last N lines of each page. What's N? Footnotes could be several lines each, multiple footnotes. Maybe: find the last paragraph-start line in the page; footnotes come after all body text? No — footnotes are at the foot, body text above. But body text can continue after... no, footnotes are at the bottom of the page, so all footnote lines are at the end of the page's text (after the last body line). But the page header lines (symbol, GE, page number) come at the start... or end? In the sample, page 1 has symbol at top. For subsequent pages, the header (symbol, GE code, page number) is typically at top, then body, then footnotes at bottom. But the converter might put the page number at the end? In the sample, page 1: symbol at very top. Hmm, the sample shows page 1 only.

Actually in many UN PDF-to-text conversions, each page begins with the symbol line and "GE.xx" line and page number, e.g.:

```
E/C.12/GC/27									GE.25-01234

5
```

or the page number at top. Hard to know exactly. Let me design robustly:

For each page:
- lines = text.split(/\r?\n/)
- Classify each line:
  - header/footer: /^\d{1,4}$/ (page number alone), symbol match, /^GE\./, /^Distr\.:/, /^Original:/, /^[-_—]{5,}$/ (separator)
  - footnote start: /^\d{1,3}\s+\S/ and NOT /^\d{1,3}\.\s/ — i.e., number followed by whitespace then text (no period). But only count/remove as footnote if in foot region.
  
Foot region determination: I'll say the foot region starts at the first line (scanning from top? no...). Hmm. Let me think differently: footnotes appear at the foot of the page, i.e., after the last body-text line. Body text lines are lines that are part of paragraphs. But we don't know paragraph boundaries yet.

Alternative approach: process pages sequentially, maintaining expected paragraph number. A line starts a new paragraph iff it matches `^${expected}\.\s*$` or `^${expected}\.\s+\S` (number + period, possibly alone on line or with text). The spec says "in this text the number usually stands alone on its line, with the paragraph on the lines after it" — "usually" implies sometimes the text follows on the same line. So paragraph start: line begins with expected number + "." — regex `^${n}\.(?:\s|$)`.

Footnote lines: "a small number then text, at the foot of a page". So within a page, after we've removed headers, look at the tail of the page: lines from some point to the end that match /^\d{1,3}\s+\S/ (no period). But wrapped footnote continuation lines don't start with a number. Hmm — "Footnote lines (a small number then text...) are removed from the paragraphs and only counted." Maybe in this document each footnote is a single line (converter put each footnote on one line). The reference `footnotes` count — if each footnote is one line, counting lines = counting footnotes. I'll assume footnote = one line starting with small number + space + text (no period), located in the foot region.

How to determine foot region robustly: A footnote line's number is small (1-3 digits) and NOT followed by a period. Paragraph-start lines have a period. Other body lines rarely start with "digit space text". But cross-references like "article 18" don't start lines usually. Years "2025" are 4 digits. So maybe simply: any line matching /^\d{1,3}\s+\S/ (number, whitespace, text, no period after number) is a footnote line — remove and count. But risk: a wrapped line in the body starting with e.g. "3 per cent of..." — possible in UN text! E.g., "3.5 million" would be "3.5" — has period, excluded. "3 per cent" — hmm, could occur at line start after wrapping. Risky but the spec explicitly says "at the foot of a page", so I should restrict to foot region.

Foot region: I'll define it as: within a page, once we hit a line that matches the footnote pattern AND we're past... hmm. Alternatively: the foot region is the maximal suffix of the page's lines (after header removal) where lines are footnote-starts or continuation lines? Continuation lines are indistinguishable from body text.

Let me reconsider. Maybe simpler: in this document, footnotes are separated from body by the horizontal rule line ("____..."). So: after a separator line (^[_—]{5,}$), all subsequent lines until the end of the page (or until a paragraph-start line?) are footnotes. Hmm, but a new paragraph could start after footnotes? No — footnotes are at the foot of the page; body text for the next paragraph continues on the next page. But wait — could a paragraph start on the same page below the footnotes? No, footnotes are at the bottom.

But actually, does the separator line exist in the converted text? The sample page 1 is truncated so we can't see. UN PDFs have a footnote separator line. The converter likely kept it as a line of underscores or maybe not.

Robust plan: For each page, after removing header lines (symbol, GE, page number, Distr, Original), scan lines. Track whether we're in the "foot" region: the foot region begins at the first line matching /^\d{1,3}\s+\S/ (small number + space + text, no period) that occurs after at least one non-empty body line AND ... hmm, still ambiguous.

Alternative: use the paragraph-start logic first. Process all lines of all pages in order, building paragraphs. Paragraph start = line matching `^${expected}\.(?:\s|$)`. When we encounter a line matching `^${expected}\.` we start a new paragraph. Now, footnote lines: lines matching /^\d{1,3}\s+\S/ where the number ≠ any plausible paragraph start... but a footnote "1 text" when expected is 5 — number 1 ≠ 5, so it wouldn't start a paragraph; it'd be absorbed into paragraph 5's text. To remove footnotes, detect them before paragraph assembly:

Within each page, find footnote lines: lines matching /^\d{1,3}\s+\S/ (no period after number) that are in the last portion of the page. Let me define: let bodyEnd = index of the last line in the page that is a paragraph start or... no.

Hmm, let me think about what the actual converted text looks like. UN document E/C.12/GC/27, 20 pages. Typical converted page:

```
E/C.12/GC/27

GE.25-12345

3

Some body text continuing from previous page
wrapping here.

4.
New paragraph text...

______________________________________________________________
1	Footnote text here
2	Another footnote
```

Or footnotes might appear as "1 Footnote text". Also the page number might be at top ("3") or bottom. The sample page 1 shows symbol at top, then "United Nations", "Economic and Social Council", "Distr.: General", "6 November 2025", "Original: English", then title, then "I.", "Introduction", "1.", "A clean, healthy...". So page 1 has no page number visible in the sample (or it's omitted). Subsequent pages likely: "E/C.12/GC/27" / "GE.xx" / page number at top, then body.

OK here's my robust approach:

For each page:
1. Split into lines, keep track of line index.
2. Remove & record as "removed lines": 
   - line.trim() === symbol (or matches symbol with whitespace)
   - /^GE\.\s*[\d]/ 
   - /^\d{1,4}$/ (page number alone)
   - /^Distr\.:/ , /^Original:/ (cover header)
   - /^[-_—=]{4,}$/ (footnote separator / horizontal rule)
   - empty lines are just skipped (not recorded? or recorded? I'll skip empties silently — they're not "lines removed as headers/footers/footnotes" per se; but the collapsed list should show removed lines. I'll record non-empty removed lines only.)
3. Footnote detection within remaining lines: I'll scan for lines matching /^\s*(\d{1,3})\s+(\S.*)$/ where the char after the number is whitespace (not a period). To restrict to "foot of page": I'll say a footnote line must appear after the last paragraph-start line of the page? No wait — footnotes come after body text, and body text includes paragraph starts. The last paragraph start on the page is above the footnotes. But what if a page has no paragraph start (continuation page)? Then all lines are body continuation, and footnotes at the bottom. Hmm.

Better: footnotes are at the foot — so scan from the END of the page backwards: collect lines while they are footnote-ish or... continuation lines are ambiguous.

Alternative pragmatic approach: treat ANY line matching /^\d{1,3}\s+\S/ (number + space + text, no period) as a footnote line, EXCEPT when the number equals the next expected paragraph number AND... no wait, paragraph starts have periods. "1." vs "1 text". A footnote line never has a period right after the number? In UN style, footnote markers in text are superscript numbers; at the foot, the line is like "1	Text" or "1 Text". I believe no period. But hmm, some UN docs format footnotes as "1. Text"? Let me think... In UN General Assembly documents, footnotes at page bottom: "________________\n1 Text of footnote." — I'm fairly confident it's number + tab, no period. Treaty body documents similar.

But the risk of body lines starting with "N text": e.g., a wrapped line "16.3 Promote the rule of law..." — has period. "3 per cent of GDP" — possible. To mitigate, restrict to foot region: I'll define foot region as starting at the first footnote-pattern line that appears after we've seen at least one paragraph-start or body line on that page AND all lines from there to the end (excluding headers) match footnote pattern or are continuations... ugh.

Let me simplify with a heuristic that matches the spec: "Footnote lines (a small number then text, at the foot of a page)". Implementation: for each page, look at the lines after header removal. Find indices of lines matching footnote pattern F = /^\d{1,3}\s+\S/ (and not /^\d{1,3}\./). If any exist, the foot region = from the FIRST such line to the end of the page, BUT only if that first such line is in the latter part of the page? Hmm, what if a body line mid-page matches F (e.g., "3 per cent")? Then everything after would be wrongly treated as footnotes. 

Alternative: foot region = from the LAST block of consecutive... no.

Hmm, let me think about what's actually in the data. The reference says `footnotes` count. E/C.12/GC/27 — General Comment 27 on environment. It probably has a handful of footnotes (maybe 5-15). Each footnote at the foot of a page. The converter output: footnote lines at the bottom of the page.

Practical approach: process page by page. Within a page, after removing headers, iterate lines top to bottom, building paragraphs (paragraph start = expected number + period). Additionally, maintain a flag: once we see a line matching F (small number + space + text, no period) — treat it and ALL subsequent non-header lines on this page as footnote region (remove & count each F-line as one footnote; continuation lines also removed but not counted). Wait but that would break if a body line matches F mid-page. How likely? Body lines starting with 1-3 digit number followed by space and text without period... In UN text, lines starting with numbers are usually paragraph numbers ("12.") or list items. A wrapped line could start with "2025" (4 digits — excluded by \d{1,3}? "2025" is 4 digits, /^\d{1,3}\s/ requires whitespace after 1-3 digits, so "2025 " — \d{1,3} would match "202" then next char "5" is not whitespace, so no match. Good.) "3 per cent" — matches. Risk exists but low. Also, the spec says footnotes are "at the foot of a page", so maybe I should require the F-line to be within the last, say, 40% of the page's lines? Or after the last paragraph start? Hmm.

Actually, here's a cleaner idea: footnotes appear at the foot of the page, i.e., AFTER all body text. Body text on a page ends before footnotes. The next page's body continues. So within a page, once we hit the first F-line, everything after (until page end) is footnote region — because footnotes are at the foot. The only failure mode is a body line matching F before the actual footnotes. To reduce that risk, I can add: the F-line's number should be ≤ some small bound (footnotes are numbered 1, 2, 3... per page, small). "Small number" — I'll use 1-2 digits? Footnote counts per page are small. /^\d{1,2}\s+\S/. "3 per cent" still matches. Hmm.

Additional guard: require that the F-line appears after at least one line of body text on the page AND that the footnote region is at the foot — i.e., there is no paragraph-start line after the first F-line on the same page? Actually that's a good guard: footnotes are at the foot, so no paragraph starts after them within the page. But a paragraph could start on the same page below footnotes? No — footnotes are physically at the bottom of the page. So: if a paragraph-start line (expected number + period) appears after an F-line on the same page, then that F-line was probably body text. Hmm, but paragraph starts after footnotes shouldn't happen.

Wait, actually — could a paragraph start line appear after footnotes on the same page? Only if the converter reordered, which it doesn't. So guard: foot region = from first F-line to end of page, but only if no paragraph-start line occurs after it. If a paragraph-start occurs after, then... complicated. Let me just also handle: process lines in order; when I see F-line, tentatively mark foot region start; if later a paragraph-start line appears on the same page, cancel the foot region (treat earlier F-lines as body). That's a reasonable robust heuristic.

Hmm, but actually there's another subtlety: what if the footnote separator line was removed as header, and footnotes follow, and then the NEXT page starts. Fine.

Also: what about the page number appearing at the END of the page text (footer)? /^\d{1,4}$/ removal handles it wherever it is. But careful: a paragraph number alone on a line is "12." with period — not matched by /^\d{1,4}$/. Good. But what about a line that is just "12" without period? That would be removed as page number — but per spec, paragraph numbers have periods. OK.

Wait, one more: the spec says "Remove lines that are only a page number, only the document symbol, or a distribution code ('GE.' followed by digits)". So exactly those three. I'll also remove the underscore separator (it's a footer) — the collapsed list is "Lines removed as headers, footers and footnotes", so footers include separators. And "Distr.: General" / "Original: English" — cover page lines; they'd otherwise be absorbed into... they come before paragraph 1, so they'd be "preamble" text not in any paragraph. That's fine — they're not in any paragraph, so they don't pollute paragraphs. But should they be in the removed list? They're headers. I'll remove lines matching /^Distr\.:/ and /^Original:/ as headers too — safe, they never appear in paragraph text. Hmm, but "keep it simple" and "where it says nothing, keep it simple". The spec's removal list is explicit; I'll implement those three plus the separator line and Distr/Original (clearly headers, and the list title mentions headers). Actually, let me be careful: "United Nations" and "Economic and Social Council" lines on page 1 — also headers. If I don't remove them, they become preamble (before paragraph 1) — not in any paragraph, harmless. But the removed-lines list is for the reader to verify nothing substantive was discarded. Preamble lines not in paragraphs... hmm, they'd just be dropped silently. To be transparent, maybe I should capture all lines before the first paragraph start as "preamble" and show them in the removed list too? That could be nice: the collapsed list shows everything removed. Let me do: lines before the first paragraph start (after header removal) are "preamble/cover lines" — include them in the removed list (categorized). Actually simpler: I'll remove known header patterns (symbol, GE, page number, Distr, Original, separator, "United Nations", "Economic and Social Council"?) — hmm, "United Nations" could theoretically appear in body text as a line? A wrapped line could be exactly "United Nations"! E.g., "...the work of the\nUnited Nations..." — possible! So don't remove "United Nations" as a pattern. Instead, treat pre-paragraph-1 lines as preamble and list them in the removed list. That's safer and more honest.

So algorithm:

```
pages = records sorted by page
allLines = [] // {page, line, index}
for each record: for each line of text.split('\n'): push {page, text: line}
```

Then process sequentially with expected = 1:

```
paragraphs = []  // {number, page, lines: []}
removed = []     // {page, line, reason}
footnotes = []   // {page, line} count
current = null
footMode per page...
```

Let me restructure per-page processing:

For each page:
  lines = raw lines
  kept = []
  for each line:
    t = line.trim()
    if t === '' → skip (blank)
    else if t === symbol → removed.push(header)
    else if /^GE\.\s*\d/.test(t) → removed.push(header)
    else if /^\d{1,4}$/.test(t) → removed.push(footer page number)
    else if /^Distr\.:/.test(t) || /^Original:/.test(t) → removed.push(header)
    else if /^[-_—=]{4,}$/.test(t) → removed.push(footer separator)
    else kept.push({page, text: line})
  
  Then footnote detection on kept: find first index i where F.test(kept[i].text) and no paragraph-start line after i on this page... Actually let me do it in the main loop instead, simpler:

Main loop over all kept lines across pages (in order), with page boundaries known:

```
expected = 1
current = null
for each line L (with page p):
  m = L.text.match(/^(\d+)\.(?:\s+(.*))?$/)  // number + period
  if m && parseInt(m[1]) === expected:
    // start new paragraph
    if current: paragraphs.push(current)
    current = {number: expected, page: p, lines: m[2] ? [m[2]] : []}
    expected++
    continue
  // footnote check: small number + space + text (no period), at foot of page
  if (/^\d{1,3}\s+\S/.test(L.text) && isFootOfPage(L)):
    footnotes.push(L); removed.push({reason:'footnote', ...})
    // and all subsequent lines on this page are footnote region
    ...
```

Hmm, the "foot of page" check needs lookahead. Let me precompute per page: for page p, let keptLines[p] = array. Compute footStart[p] = index of first line matching F such that no line after it (within the page) matches paragraph-start pattern for the expected number at that time... circular. 

Simpler: compute footStart[p] = first index i where F matches keptLines[p][i] AND for all j > i, keptLines[p][j] does NOT match /^\d+\./ (any number+period at line start — since paragraph starts always have number+period; body lines rarely start with "N." except cross-references like "12.3" — hmm "16.3" starts with digits+period! A wrapped line could start with "16.3 Promote...". Ugh.)

OK let me step back and think about likelihood. This is a workshop app; the data is fixed (E/C.12/GC/27, 20 pages). The reference gives `footnotes` count so I can sanity-check my count against it in the app (the app displays both). The spec's rule is simple: "Footnote lines (a small number then text, at the foot of a page) are removed from the paragraphs and only counted." 

I'll implement: within each page's kept lines, scan from the top; the foot region begins at the first line matching F = /^\d{1,3}\s+\S/ (number, whitespace, text — note: NOT followed by period) — and once in foot region, all remaining lines of the page are footnotes (each F-line counts as one footnote; non-F lines in the foot region are continuation lines, removed but not counted). Guard: if a line matching paragraph-start (expected number + period) appears after foot region start on the same page, we... hmm. Actually you know what — since footnotes are at the foot of the page and paragraphs never start below footnotes on the same page, if I see F-line then later a paragraph-start line on the same page, the F-line was body. But this is getting complex. 

Alternative simpler interpretation: maybe in this converted text, footnote lines are exactly lines matching /^\d{1,3}\s+\S/ anywhere (the converter put them at page foot anyway), and body lines never match because... risky.

Let me look at the sample again: page 1 text ends with "...droughts, and tr\n[… rest of the page omitted in this sample]" — the sample is truncated, so I can't see footnote format. 

Decision: implement foot region per page as: the maximal suffix of the page's kept lines that starts with an F-line and contains only F-lines and continuation lines, where "foot" means: first F-line index i such that i is in the last portion... 

You know, let me just go with: foot region = from the first F-line to the end of the page, with the guard that if a paragraph-start line (matching `^${expected}\.` at that point in processing) occurs after, we re-classify. Actually, let me do a two-pass approach:

Pass 1: identify paragraph starts across all kept lines (sequential, expected counter). This gives paragraph boundaries. Any line not inside a paragraph and not a header is either preamble (before para 1) or footnote-region.

Pass 2: lines after the last paragraph-start line of each page... no wait, footnotes can be on a page where a paragraph starts above them. Lines between paragraphs belong to the preceding paragraph. So: a page's kept lines = [body lines (belong to paragraphs or preamble)] + [footnote lines at end]. The footnote lines are those after the last body line. How to find the last body line? The foot region starts at the first F-line such that all subsequent lines on the page are F-lines or non-paragraph-start lines... 

Honestly, simplest robust rule given "at the foot of a page": foot region = suffix of page starting at first F-line, provided no paragraph-start line occurs after it on that page. If a paragraph-start occurs after, then move foot start to the next F-line after that paragraph start. I'll implement iteratively:

```
function findFootStart(keptLinesOfPage, expectedAtPageStart) {
  // returns index where footnotes begin, or -1
  // simulate: scan lines; track expected number as paragraphs start
  // first F-line after which no paragraph-start occurs on this page
}
```

Hmm, but expected changes across pages. Let me just do the main loop with a per-page "pending foot" buffer:

Process lines page by page. Within a page, accumulate lines into a buffer. When the page ends, decide: scan the buffer from the end? No...

OK here's another thought — process within page: iterate lines; maintain `footStart = null`. For each line:
- if paragraph-start (expected number + period): footStart = null (reset — footnotes can't be before a paragraph start on the same page... wait, they could be before? No: footnotes at foot, paragraph start above them. If we see a paragraph start, any earlier F-line was body text, so reset footStart to null and treat earlier F-lines as body). Then start new paragraph, expected++.
- else if F-line and footStart === null: footStart = current index (tentative).
- else: if footStart !== null, it's footnote region (continuation or F-line); else body line (append to current paragraph or preamble).

At page end, if footStart !== null: all lines from footStart on are footnotes → remove from paragraphs, count F-lines among them as footnotes, add all to removed list. If footStart === null: all lines are body.

Wait, but there's an issue: if footStart is set tentatively and then a paragraph-start appears later on the same page, I reset footStart = null — but the lines between old footStart and the paragraph start were already... in my iteration I haven't committed them yet if I buffer per page. Let me buffer per page: collect page's kept lines, run the above logic to find footStart, then commit: lines before footStart → main flow (paragraph assembly), lines from footStart → footnotes.

But paragraph assembly spans pages (a paragraph continues across pages). So main flow: I'll process page by page, and within each page first determine footStart, then feed the body lines (before footStart) into the global paragraph assembler, then handle footnote lines.

Paragraph assembler (global, across pages):
```
expected = 1
current = null  // {number, page, lines:[]}
preamble = []
for each body line L (in order):
  m = L.text.match(/^(\d+)\.(?:\s+(.*))?$/)
  if m && +m[1] === expected:
    if current: paragraphs.push(current)
    current = {number: expected, page: L.page, text: m[2] || ''}
    expected++
  else:
    if current: current.text += '\n' + L.text  (or append line)
    else: preamble.push(L)
if current: paragraphs.push(current)
```

Wait — but the paragraph-start regex: "A paragraph starts at a line that begins with the next expected number and a full stop ('1.', then '2.' …); in this text the number usually stands alone on its line". So line "1." alone → match with m[2] undefined. Line "1. Some text" → m[2] = "Some text". Also "Numbers out of sequence (years, cross-references) do not start a paragraph" — handled by requiring +m[1] === expected. E.g., line "2025." wouldn't match expected unless expected is 2025. Cross-reference "see paragraph 12." — line starts with "see", not a number. A line starting "12." when expected is 5 → not a start; it's body text (appended to current paragraph). Good.

Edge: what if a paragraph number line is like "10." but with leading spaces? I'll trim for matching but keep original for text. Let me match on trimmed line: `const t = L.text.trim(); m = t.match(/^(\d+)\.(?:\s+(.*))?$/)`. Hmm but "1." followed by text on same line: "1. A clean..." — m[2] = "A clean...". But careful: "16.3 Promote..." — t = "16.3 Promote..." → regex ^(\d+)\.(?:\s+(.*))?$ — "16" then "." then "3 Promote..." — \s+ requires whitespace after the period; "3" is not whitespace, so no match at "16." — but regex could match... ^(\d+)\. — \d+ is greedy: "16", then needs ".", yes ".", then (?:\s+(.*))?$ — next char "3" — \s+ fails, and $ fails. Backtrack: \d+ = "1", then "."? next char is "6", not ".". Fail. So "16.3 ..." doesn't match. 

But wait: what about "1." where expected=1 but it's actually a footnote "1." with period? Spec says footnotes are "a small number then text" — I'll assume no period. If a footnote were "1. text", it would match paragraph-start only if expected===1. Edge case, ignore.

Also sub-paragraphs: "Lettered sub-paragraphs stay inside their numbered paragraph" — e.g., lines "(a) ..." or "a)" — they don't match paragraph-start (not digits), so they're appended to current paragraph. Good, automatic.

Now footnote F regex: /^\d{1,3}\s+\S/ on trimmed line, and NOT /^\d{1,3}\./ (period right after number). Actually /^\d{1,3}\s/ already excludes "1." since after "1" comes "." not whitespace. But "12. text"? \d{1,3} matches "12", then "." — not \s, no match. Good. But "1 . text"? Unlikely. So F = /^\d{1,3}\s+\S/. Hmm, also footnote could be "1\tText" — \s covers tab. Good.

But wait — what about a footnote line where number is followed by period AND text, like "1. See resolution..."? Then F fails, and paragraph-start check: expected is like 5, so not a start → it'd be absorbed into the current paragraph as body. That would be wrong but per spec footnotes are "a small number then text" — I'll trust the format. Hmm, but to be safer, maybe I should ALSO treat lines matching /^\d{1,3}\.\s+\S/ in the foot region as footnotes... but they'd be caught by paragraph-start only if number===expected. In foot region (after footStart), I don't apply paragraph-start logic — I treat everything as footnote. Wait, in my per-page logic, once footStart is set, subsequent paragraph-start lines reset it. Hmm, but what if footnotes use "1." format and a paragraph starts after? Then footStart resets and footnotes get absorbed. Trade-offs. 

Let me reconsider: maybe don't reset on paragraph-start; instead, decide footStart as the LAST F-line run? Ugh.

Let me think about what the real converted text looks like. UN ODS PDFs: footnotes at page bottom, format:

```
___________________________________________________________________________
1	Text of footnote
```

Actually in many UN PDFs the footnote separator is a line, and footnotes are "1  text" with the number possibly followed by a period? Let me recall an actual UN doc... In General Assembly resolutions, footnotes appear as:

```
____________________
1	A/HRC/...
```

I believe no period. In ECOSOC documents (E/C.12/GC/27 is a treaty body doc from OHCHR), footnotes: "1 See ..." — I'm fairly confident: number, tab, text. OK, F = /^\d{1,3}\s+\S/ it is. And I'll keep the reset-on-paragraph-start guard? If footnotes never have periods, and body lines starting with "N text" are rare, the guard adds safety for body lines like "3 per cent..." appearing mid-page: if a paragraph starts after them, they're reclassified as body. But if "3 per cent" appears in the last paragraph of a page with no following paragraph-start on that page, it'd be misclassified as footnote. Hmm. Additional guard: footnote numbers are small AND typically the foot region is short. Maybe require footStart to be within the last X lines? No fixed X.

Alternative guard: footnote region must be at the foot — meaning after footStart, no more than, say, ... no.

You know what, let me add another signal: the footnote separator line (^[-_—=]{4,}$) — if present, footnotes come right after it. I remove separators as footers. I could use: footStart = first F-line after the last separator line on the page, if a separator exists; else first F-line with the paragraph-start guard. Hmm, over-engineering.

Let me just go with: per page, footStart = first index i such that F(kept[i]) and no j>i with paragraph-start-pattern... but paragraph-start depends on global expected. I'll compute paragraph starts globally first (pass 1 over all kept lines, ignoring footnotes — but footnote lines could falsely trigger paragraph starts? F-lines have no period, so they never match paragraph-start regex. And "1." footnote format would falsely trigger only if expected matches. OK).

Pass 1: global scan over kept lines (headers removed), find paragraph-start lines: line where trimmed matches /^(\d+)\.(?:\s|$)/ and number === running expected. Record their global indices. This gives paragraphs and their line ranges (each paragraph = lines from its start to before next start, across pages — but footnote lines within that range would be included; that's why pass 2).

Pass 2: per page, footStart = first F-line index i (within page) such that no paragraph-start line (from pass 1) lies after i on the same page. If multiple, take the first such i. Then lines [footStart..end] of that page are footnotes: remove from paragraph text, count F-lines as footnotes, add to removed list. Lines before footStart stay.

Wait, but pass 1 included footnote lines in paragraph text (since they don't match paragraph-start). Pass 2 removes them. But pass 1's paragraph-start detection could be affected? Footnote lines never match paragraph-start (no period), so no. But what if a footnote line is "1." format... ignore.

Hmm wait, one more issue: pass 1 paragraph-start detection uses running expected across ALL kept lines including footnote lines — footnote lines don't affect expected. Fine.

But actually there's a subtle issue with pass 2's guard: "no paragraph-start after i on the same page". Consider a page where body text has a line "3 per cent" (F-match) mid-page, then later a paragraph starts → guard fails for that i, we look for next F-line after the paragraph start. Good. Consider footnotes at page foot: first F-line has no paragraph-start after it on that page → footStart = that. Good. Consider a page with NO paragraph starts and body line "3 per cent" near the end → misclassified as footnote start, and everything after removed. Risk accepted (spec says footnotes are at foot; a body line matching F near page end with nothing after is indistinguishable from a footnote anyway).

Hmm, wait — actually there's another consideration: what if footnotes appear at the foot but the page ALSO has the next page's header at the end? No, headers are per-page at top typically. The /^\d{1,4}$/ page-number removal handles page numbers wherever they are. But danger: what if a paragraph number stands alone WITHOUT a period? Spec says numbers have full stops. OK.

Another danger: /^\d{1,4}$/ removing a line that's actually... a year alone on a line? "2025" alone — would be removed as page number. In body text, a year alone on a line is unlikely (wrapped text). Page numbers in this doc are 1-20. Fine.

Now, the "Differs" comparison: paragraph's first six words vs reference.first_words[number]. Normalize: lowercase, remove punctuation, split on whitespace. Compare word by word. If reference has no entry → "no reference". If match → OK (tick?). If differ → "Differs" mark, and show the reference words beside (in the expanded row: "reference's first words shown beside it").

First six words of paragraph: take paragraph text (joined lines), normalize: `text.toLowerCase().replace(/[^a-z0-9\s']/g, ' ')` hmm — need to handle punctuation. Let me do: `t.toLowerCase().replace(/[^\p{L}\p{N}\s]/gu, ' ').split(/\s+/).filter(Boolean).slice(0,6)`. Compare with reference first_words normalized the same way. Reference first_words: `{"1": "A clean, healthy and sustainable environment", ...}` — first six words. Compare arrays element-wise, length 6 each (or min length?). "comparing word by word" — I'll compare the first min(6, ref.length) words? Spec: "the paragraph's first six words are not the reference's, comparing word by word". I'll compare up to 6 words of each; if lengths differ within first 6, differs. Let me compare normalized arrays of first 6 words each, element-wise; equal length and all equal → match.

Counters:
- paragraphs found / reference.paragraphs → "N of 90"
- footnotes removed / reference.footnotes
- paragraphs whose opening words differ from reference (count of "Differs"; maybe also show "no reference" count separately? Spec: three counters: paragraphs found/ref; footnotes removed/ref; paragraphs whose opening words differ. I'll show differ count; maybe add "(X with no reference entry)" as small note. Keep simple: third counter = differ count, and I can note no-reference count in the note line. Actually spec says exactly three counters; I'll make the third "paragraphs whose opening words differ from the reference: X" and maybe append "· Y have no reference entry" — that's still one counter line. Fine.)

Table rows: number, page where it starts, first line (~90 chars) — "first line (about 90 characters)" — I'll take first 90 chars of the paragraph text (or first line up to 90 chars). I'll use first 90 chars of joined text, with ellipsis. Symbol linked to doc_url — every row shows symbol link (same symbol for all rows; fine, spec says so). "Differs" mark where opening words don't match; "no reference" shown distinctly.

Checkbox "Show differences first": moves marked rows (Differs; what about no-reference? "moves marked rows to the top" — marked = Differs mark. I'll move Differs rows first, then others in numeric order. Maybe no-reference also marked? Spec: 'a "Differs" mark where the opening words do not match' and 'If the reference has no entry for a number, show "no reference", not "Differs"'. So marks: "Differs" or "no reference" or (blank/✓). "Show differences first" moves marked rows to top — I'll interpret marked = Differs (and maybe no-reference too? "differences" = Differs). I'll move Differs rows to top; keep no-reference in place? Hmm, "moves marked rows to the top" — marked rows are those with a mark. I'll move both Differs and no-reference? The label says "Show differences first" — differences = Differs. I'll move only "Differs" rows to top, stable order otherwise. Actually, to be safe and useful, I'll sort: Differs first, then no-reference, then matches? No — spec says "moves marked rows to the top", marked = rows with the Differs mark. I'll do Differs first, rest in original order. Hmm, but "no reference" is also a kind of mark... The spec distinguishes them. I'll go with Differs only... Actually let me include both Differs and no-reference as "marked" — no wait. "Show differences first" — differences. Differs only. Keep it literal.

Clicking a row: expands beneath it showing full paragraph text exactly as extracted (in a <pre> or with preserved whitespace), with the reference's first words shown beside it. So expanded row: two columns — "Extracted text" (full) and "Reference first words" (the reference entry for that number, or "no reference"). Layout: a full-width row beneath with the full text and a side note. I'll do: expanded row contains a div with the full text (white-space: pre-wrap) and a small box "Reference: “...”" or "no reference entry".

Download CSV: columns number, page, match (e.g., "match" / "differs" / "no reference"), full text quoted. Build CSV in browser: header row `number,page,status,text`, each row with text quoted (escape " as ""). Use Blob + URL.createObjectURL + a.download click. "built and saved in the browser" — yes, Blob approach, no server.

Collapsed list: <details> element "Lines removed as headers, footers and footnotes" — list each removed line with page and reason (header/footer/footnote). Could be long (20 pages × ~3 header lines + footnotes) — fine inside <details>. Maybe cap display? Keep simple: list all, maybe with counts per reason at top. I'll show count summary + list (page, reason, text truncated to ~100 chars). Also preamble lines (before paragraph 1) — include them as "cover/preamble" removed lines? They're not headers/footers/footnotes... but they are removed from paragraphs. The list title says "Lines removed as headers, footers and footnotes". Preamble (cover page text like "United Nations", title, "I. Introduction") — hmm, "I." and "Introduction" are section headings, not removed per spec... they'd be preamble (before para 1). Should they be in the removed list? The reader wants to "see nothing substantive was discarded". I'll include preamble lines in the collapsed list under reason "before paragraph 1 (cover/heading)". That's honest. Actually wait — section headings like "I. Introduction", "II. ..." appear between paragraphs too! E.g., after paragraph 10, "II. Normative content" then "11." — the heading lines would be absorbed into paragraph 10's text (since they don't match paragraph-start). Hmm! Is that desired? The spec says "Text runs until the next start" — so yes, headings between paragraphs get absorbed into the preceding paragraph. That's per spec ("Lettered sub-paragraphs stay inside their numbered paragraph" — and headings too, implicitly). The spec doesn't say to remove section headings. So paragraph text may include trailing heading lines like "II. Normative content". That's "exactly as extracted" — fine. The first-six-words comparison only looks at the start, so headings at the end don't affect Differs. OK, keep simple: only remove the specified header/footer/footnote lines.

Hmm wait, but actually — should section headings be removed? Spec: "Remove lines that are only a page number, only the document symbol, or a distribution code." Only those. Plus footnotes. So headings stay in paragraph text. OK.

But then preamble (before para 1): lines like "United Nations", "Economic and Social Council", "6 November 2025", "Committee on Economic, Social and Cultural Rights", title lines, "I.", "Introduction". These are before paragraph 1 — not in any paragraph. I'll collect them as preamble and show in the removed list (reason "cover / before paragraph 1"). Good for transparency.

Now the counters note: "Found by the code from the page text; reference figures come from the file." — display under counters.

Header: title (from data.title), symbol linked to doc_url, one line: "raw PDF text, N pages, source: …" — N = records.length (or data.count). Use records.length; also data.count exists. I'll use records.length and mention source from data.source. Format: "Raw PDF text · 20 pages · source: …". Spec: one line: "raw PDF text, N pages, source: …". I'll write: `Raw PDF text, ${n} pages, source: ${source}`.

"How this is computed" note near every chart or number — add a small note near counters and table: e.g., "Paragraphs are found by scanning the joined page text for lines that begin with the next expected number followed by a full stop; footnote lines (small number + text at the foot of a page) are removed and counted; 'Differs' compares the first six words with the reference, ignoring case, punctuation and extra spaces."

Design: clean, system fonts, accent #1f6fb2, light background, base 16px, no horizontal scroll. Title, description line, counters as three stat cards, checkbox, table, download button, details list.

Table: columns: ¶ (number), Page, First line (90 chars), Document (symbol link), Check (✓ / Differs / no reference). Row click toggles expansion. Expanded row: full text in pre-wrap + reference words box.

Sorting with "Show differences first": re-render tbody order. Keep expansion state? Simple: re-render; expanded row closes on re-sort (acceptable) — or preserve by number. I'll preserve expanded number across re-render (store expandedNumber, re-expand after render). Nice touch.

CSV: number, page, status, text. Quote text: `"` + text.replace(/"/g,'""') + `"`. Join with commas, rows with \r\n. Blob type 'text/csv'. Filename like `E_C_12_GC_27_paragraphs.csv` — derive from symbol sanitized.

Now, first line ~90 chars: `const firstLine = para.text.split('\n')[0]` then slice to 90 chars + '…' if longer. Spec: "first line (about 90 characters)". I'll take the full first line but truncate display at 90 chars with ellipsis. Hmm — "first line (about 90 characters)" might mean show about 90 chars of the first line. I'll do: first line, truncated to 90 chars.

Wait — paragraph text: when number stands alone on its line, the paragraph text starts on the next line. So para.text = lines after the number line, joined with '\n'. If number line has text after "1.", include it. For row 1, text starts "A clean, healthy and sustainable environment..." — matches reference first_words["1"]. 

Now let me also double check the paragraph-start regex against lines like "1." — trimmed "1." matches ^(\d+)\.(?:\s+(.*))?$ with m[2] undefined. Good. Line "54. The Committee requests..." → m[2]="The Committee requests...". Good.

What about a line like "10." when expected is 10 — good. What if the converter put "10." and text on same line but with multiple spaces — fine.

Potential issue: what if a paragraph number line is "1 ."? Unlikely.

What about the very first lines of page 1: "E/C.12/GC/27" — removed (symbol). "United Nations" — preamble. "Economic and Social Council" — preamble. "Distr.: General" — removed as header (I added this pattern; spec didn't list it but it's clearly a header; hmm — spec says remove lines that are only page number / symbol / GE code. "Distr.: General" is none of those. If I don't remove it, it goes to preamble list — also fine and more literal. Let me NOT remove Distr/Original, and let them be preamble → shown in removed list as "before paragraph 1". That's more faithful to spec and still transparent. But wait — "Distr.: General" appears only on page 1 (cover). On other pages, headers are symbol + GE + page number. So preamble only from page 1. Good, simpler: remove only the three specified + separator lines? The separator (____) — spec doesn't mention it either. If present, it'd be absorbed into a paragraph (it's at page foot, after body, before footnotes — it would be appended to the current paragraph's text!). Hmm, that would pollute paragraph text with "______". The spec says footnote lines are removed; the separator is part of the footnote apparatus. I'll remove separator lines as footers (reason "footer") — justified as footer. And "GE." codes, symbol, page numbers per spec. Distr/Original → preamble (page 1 only). Actually hmm, "Distr.: General" — if I leave it as preamble it shows in the removed list, fine.

Wait, actually also: what about lines like "6 November 2025" on page 1 — preamble. Fine.

But hold on — what about page headers on pages 2-20: are they at the top of each page's text? Presumably "E/C.12/GC/27", "GE.25-xxxxx", and page number "2".."20". The page number line "2" matches /^\d{1,4}$/ → removed. But WAIT — danger: what if a paragraph number stands alone on a line WITHOUT a period due to converter damage? Spec says numbers have full stops ("begins with the next expected number and a full stop"). Trust it.

Another danger: page number line could be like "2 E/C.12/GC/27" combined? Then not matched. It'd be absorbed into paragraph text. Hmm. The spec's removal rules suggest the converter puts them on separate lines. Trust the spec.

Also the sample shows page 1 begins with "E/C.12/GC/27\n\nUnited Nations\n\nEconomic and Social Council\n\nDistr.: General\n6 November 2025\nOriginal: English\n\n..." — so symbol on its own line. Good.

Now footnote counting: reference.footnotes — count of footnotes in the document. My count = number of F-lines in foot regions. If each footnote is one line, matches. If a footnote wraps to 2 lines, my count overcounts (continuation lines don't match F, so not counted — only F-lines counted; a wrapped footnote has one F-line (its first line) + continuation lines → counted once. Good.) But if the footnote number and text are on separate lines? Unlikely.

Hmm, wait: what if footnote format is "1" alone on a line then text on next line? Then "1" alone matches /^\d{1,4}$/ → removed as "page number"! And miscounted. Risk. But spec says "a small number then text" — same line. OK.

Also: what if footnotes appear mid-page (not at foot)? Spec says at foot. OK.

Let me now also handle: the foot region detection per page — I said pass 1 finds paragraph starts globally, pass 2 per page finds footStart = first F-line with no paragraph-start after it on the same page. Let me refine: paragraph-start lines are known globally (indices in the kept-lines array). For page p with kept lines at global indices [a..b], footStart candidates = indices i in [a..b] where F matches and no paragraph-start index j in (i..b]. Take the smallest such i. If none, no footnotes on page.

Hmm wait, but there's a subtlety: what if the page has footnotes AND the next paragraph starts on the SAME page below the footnotes? Impossible physically. OK.

But another subtlety: what if a page's body contains an F-line (e.g., "3 per cent") and NO paragraph starts after it on that page, but the page is a continuation page (no paragraph start at all)? Then footStart = that F-line, and the rest of the page (real body text!) gets removed as footnotes. Bad. How likely is a body line starting with "N text" (1-3 digits, space, text)? Lines like "3 per cent of..." — in UN text, percentages usually written "3 per cent" — could start a wrapped line. Hmm. Risk exists. Mitigation: also require that the foot region is "at the foot" — e.g., footStart must be in the last 50% of the page? Or: the foot region should not contain too many lines? Or: footnote numbers are usually sequential from 1 within the page? 

Alternative mitigation: require F-line number ≤ 30 (footnotes per page are few)? "3 per cent" has number 3 ≤ 30. Doesn't help.

Alternative: check if there's a separator line before the F-line — if the page has a separator (____) line, footnotes follow it. Let me use: if page has separator lines, footStart = first F-line after the LAST separator on the page. If no separator, use the guard rule. Hmm, but I remove separators in the header-removal pass... I can record their positions.

Honestly, for this specific document, let me think about what's most likely: E/C.12/GC/27, 20 pages, has some footnotes (reference.footnotes maybe ~10-20). The converter output — footnotes at page foot, likely with separator line or just after body. Body lines starting with "N text": possible but let me add one more guard: the F-line must be followed (within the page) only by lines that are F-lines or short-ish continuation... no.

Pragmatic guard: footStart = first F-line i such that no paragraph-start after i on the page AND (there is a separator line before i on the page OR i is in the last 40% of the page's kept lines OR all lines after i are F-lines or... ). Hmm, getting complicated. 

Let me simplify: footStart = first F-line i such that no paragraph-start after i on the same page. Additionally, cap the damage: if the foot region contains a line that matches paragraph-start for a FUTURE expected number... no, future paragraph starts are on later pages.

Alternative: after computing footStart, sanity-check: the foot region's F-line numbers should be small and typically start near 1? Not necessarily (footnotes numbered continuously through the document! In UN docs, footnotes are numbered 1, 2, 3... continuously across the document, not per page). So footnote numbers could be like 15, 16 — still ≤ 2 digits. "Small number" = 1-3 digits covers it.

I think the guard "no paragraph-start after on same page" plus "F-line" is reasonable. The residual risk (body line "N text" in the last paragraph of a page with no following paragraph-start on that page) — accept. Actually, one more cheap guard: require the F-line to appear after at least one non-F body line on the page (trivially true) — meh.

Hmm, actually wait. Let me reconsider: maybe simpler and closer to spec: "Footnote lines (a small number then text, at the foot of a page)". Maybe the intended implementation is exactly: within each page, lines at the foot (i.e., after the last paragraph-start? no...). Or maybe: the last N lines? I'll go with my guard approach. And the app displays both my count and the reference count, so discrepancies are visible — that's the point of the tool ("shows where the converter damaged the text, so the reader can verify"). Actually the counters compare found vs reference — if my footnote detection is off, the counter shows it. That's acceptable and honest.

Hmm, but the success criteria: "The first counter reads 'N of 90' with N close to it" — only paragraphs counter is checked closely. Footnotes counter just needs to show both numbers. OK.

Now — one more important detail: paragraph text joining. When number stands alone, paragraph lines follow. I'll store para.lines = array of raw line texts (untrimmed? trimmed?). "Paragraph text is never edited or paraphrased, only displayed" — I'll keep the lines as-is (maybe trim trailing whitespace only? No — keep exactly, display with pre-wrap). I'll join with '\n' and display in white-space: pre-wrap. For first-words comparison, normalize handles whitespace.

For the "first line ~90 chars" in the table: use the first non-empty line of the paragraph? If number line had text, that's the first line. I'll compute display text = para.lines.join('\n'), firstLine = para.lines[0] (or first non-empty). Truncate to 90.

Wait, careful: if the number stands alone, para.lines[0] is the first text line. If "1. Text", I set lines = ["Text"]? I'll store the remainder after "N." as first line. Let me store para.raw = full text including... hmm, for CSV "full text" — should it include the "N." prefix? "the full text" of the paragraph — I'd say the paragraph text without the number marker, or with? The reference first_words for "1" is "A clean, healthy and sustainable environment" — the text after "1.". So paragraph text = lines after the number. For CSV, I'll include the number as a separate column, and text = paragraph text (without the "N." marker). Hmm, or include "N. text"? I'll keep text without the marker since number is its own column. Actually, "exactly as extracted" for display — the expanded view shows the paragraph as extracted; I could show "1." + text? The row already shows the number. I'll display the text lines as extracted (without re-adding the number). Hmm, "Clicking a row opens the full paragraph beneath it, exactly as extracted" — I'll show the full extracted text of the paragraph (the lines that belong to it). I think including the leading number line is more "exactly as extracted"... but the number is in the row already. I'll display text without the standalone number line but if the number line had inline text, include that text. Simpler: para.text = joined lines (excluding the bare number line). Display that. Fine.

Now, page where paragraph starts: the page of its start line. Good.

Let me now also think: do paragraphs span pages? Yes — a paragraph starting on page 3 may continue on page 4. The "page where it starts" = start page. Body lines on page 4 before the next paragraph-start belong to the current paragraph. My global assembler handles this since I process kept body lines in order across pages. But careful: page 4's header lines (symbol, GE, page number) are removed before assembly — good, otherwise they'd pollute. And page 4's footnotes removed — good.

Edge: what if a page's kept lines are ALL footnotes (footStart=0)? Then no body lines from that page. Fine.

Edge: preamble — lines before first paragraph start (page 1 cover). Collected, shown in removed list with reason "before paragraph 1". Also — what if expected never reaches some number (converter dropped a "N." line)? Then paragraphs would merge. The counter "N of 90" would show fewer. That's the tool's purpose — flag damage. But also "Numbers out of sequence do not start a paragraph" — if converter damaged "12." into "l2." then paragraph 12 merges into 11, and expected stays 12 forever, so subsequent "13." doesn't match expected 12 → everything merges into one giant paragraph! Hmm. That's a problem: one damaged number cascades. 

Should I handle that? Spec: "A paragraph starts at a line that begins with the next expected number and a full stop ('1.', then '2.' …); in this text the number usually stands alone on its line... Numbers out of sequence (years, cross-references) do not start a paragraph." Strictly, expected-only matching. But a single missed number cascades badly. Hmm — but maybe the reference expects exactly this strict behavior, and the document's numbers are all intact (the converter damage is in text, not numbers — "shows where the converter damaged the text"). The success criteria: "The table numbers run 1, 2, 3 … without gaps, and at least 30 rows appear" — so with strict matching, numbers run without gaps (by construction) and N should be close to 90. So the document's paragraph numbers are intact. Strict matching is correct per spec. But to be a bit more robust, I could allow: if a line matches /^(\d+)\./ with number > expected and number ≤ expected + small gap... no — spec explicitly says out-of-sequence numbers don't start paragraphs (to avoid years/cross-refs). Keep strict. If N ends up much lower than 90, the counter honestly shows it. But criteria says N close to 90 — trust the data.

Hmm, wait — one more: what about "1." appearing when expected=1 but it's actually... fine.

Also: what if a paragraph-start line has the number and text but the number is followed by period and NO space, like "1.Text"? Regex ^(\d+)\.(?:\s+(.*))?$ requires \s+ or end. "1.Text" — after "1." comes "T", not \s, not end → no match → treated as body. Hmm, should I allow "1.Text"? Spec: "begins with the next expected number and a full stop". I'll relax: ^(\d+)\.(.*)$ with m[2] trimmed — but then "16.3 Promote" would match with number 16! If expected were 16... dangerous. Keep requiring whitespace or end-of-line after the period: /^(\d+)\.(?:\s+(.*))?$/. "16.3" → no match (good). "1.Text" → no match (treated as body — acceptable, rare).

Hmm, but what about "1." followed by tab? \s covers tab. Good.

Now the reference first_words comparison. reference.first_words = {"1": "A clean, healthy and sustainable environment", ...}. Normalize function:

```
function normWords(s){
  return (s||'').toLowerCase().replace(/[^\p{L}\p{N}]+/gu,' ').trim().split(/\s+/).filter(Boolean);
}
```
This strips punctuation (commas, periods) and splits. Compare first 6 of paragraph vs first 6 of reference entry (reference entries are already ~6 words). Compare arrays: same length? Reference might have fewer than 6 words? "first six words" — entries are the first six words. I'll compare min length? Spec: "the paragraph's first six words are not the reference's, comparing word by word". I'll take up to 6 words from each and compare element-wise; if one has fewer, compare up to the shorter? Hmm — safer: compare the first min(6, a.length, b.length) words? If paragraph has ≥6 words and reference has 6, compare 6. If reference entry has 5 words (unlikely), compare 5. I'll compare arrays of first 6 from each, requiring equal length and equality. Actually if para has only 3 words (damaged), then a.length=3 vs b.length=6 → differ. Good — that flags damage.

Status: 'match' | 'differs' | 'no reference'.

Counter 3: count of 'differs'. I'll also show no-reference count in the note.

Now CSV: columns: number, page, status, text. Header: "number,page,status,text". Rows: `${n},${page},"${status}","${text.replace(/"/g,'""')}"`. Wait spec: "The CSV holds number, page, whether it matches the reference, and the full text with values quoted". So quote values — I'll quote status and text (and maybe all). I'll quote text and status; number/page numeric unquoted is fine, but "values quoted" — I'll quote text at least; let me quote all fields for safety? "with values quoted" — I'll quote the text field (and status). Number and page as plain numbers is fine for spreadsheets. Hmm, "the full text with values quoted" — the text value quoted. I'll do: number,page,status,text where status and text are quoted. Good enough. Actually let me quote all four to be safe: `"1","3","match","..."` — spreadsheets handle that fine. Eh, I'll quote status and text only; number/page plain. Fine.

Download: 
```
const blob = new Blob([csv], {type:'text/csv;charset=utf-8'});
const url = URL.createObjectURL(blob);
const a = document.createElement('a'); a.href=url; a.download=filename; a.click(); URL.revokeObjectURL(url);
```

Filename: symbol.replace(/[^\w.-]+/g,'_') + '_paragraphs.csv'.

Now the removed-lines list: <details><summary>Lines removed as headers, footers and footnotes (N lines)</summary> ... list. Each entry: `p. {page} · {reason} · {text truncated}`. Reasons: "header (symbol)", "header (distribution code)", "footer (page number)", "footer (separator)", "footnote", "before paragraph 1 (cover)". Wait — I decided Distr/Original go to preamble. Let me finalize removal categories:

- symbol line (t === symbol) → "header: document symbol"
- /^GE\.\s*\d/ → "header: distribution code"
- /^\d{1,4}$/ → "footer: page number"
- /^[-_—=]{4,}$/ → "footer: rule/separator"
- footnote lines (in foot region) → "footnote" (F-lines counted; continuation lines in foot region → "footnote (continuation)")
- preamble lines (before first paragraph start) → "before paragraph 1"

Hmm, wait: should blank lines be recorded? No, skip silently.

Also: what about lines after the last paragraph on the last page (e.g., "E/2026/..." or adoption line)? They'd be appended to the last paragraph. Per spec, text runs until next start — fine.

Now, one concern: the foot-region detection uses paragraph-start indices from pass 1. But pass 1 runs on kept lines INCLUDING footnote lines. Footnote lines don't match paragraph-start (no period after number)... unless a footnote is "1. text" format. If footnotes were "1. text" and expected===1 at that point... only page 1, expected=1 before para 1 starts — footnotes on page 1 would come after para 1 started (expected≥2), so "1." wouldn't match. Later pages: footnote numbers are large (continuous numbering), expected is paragraph number — could coincide! E.g., footnote "12. text" on page 5 when expected paragraph is 12 → false paragraph start! Hmm. But spec says footnotes are "a small number then text" — I'll trust no period. If the data has periods, my count vs reference will show mismatch — visible. OK.

Let me also double-check: "Remove lines that are only a page number" — /^\d{1,4}$/ on trimmed line. But what if page number line is "3 " with trailing space — trimmed handles. What if it's "- 3 -"? Not handled; trust format.

Now, what about the possibility that the page number appears at the TOP combined like "E/C.12/GC/27  3"? Then symbol check (t===symbol) fails, GE check fails, page-number check fails → line goes to body/preamble. On page 1 it'd be preamble (fine, listed). On later pages it'd pollute a paragraph. Trust the spec's assumption of separate lines.

Now let me think about the layout/HTML structure:

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
<header>
  <h1 id="docTitle"></h1>
  <p class="symbol-line"><a id="docLink"></a></p>
  <p class="meta" id="metaLine"></p>
</header>
<section class="stats">
  3 stat cards + note
</section>
<section class="controls">
  <label><input type="checkbox" id="diffFirst"> Show differences first</label>
  <button id="csvBtn">Download CSV</button>
</section>
<p class="how">How this is computed: ...</p>
<table id="tbl">...</table>
<details id="removed">...</details>
<script>...</script>
</body>
</html>
```

Wait — spec order: counters (2), then table (3) with checkbox, then CSV button (4), then collapsed list (5). I'll put controls (checkbox + button) above the table. Fine.

Table structure: thead: ¶ | Page | First line | Document | Check. tbody rows; expanded row = <tr class="expanded"><td colspan=5>...</td></tr> with full text + reference box.

Row click: toggle. Use event delegation on tbody.

"Show differences first" checkbox: on change, re-render order: differs first (stable), then others in numeric order. Preserve expanded state by number.

Rendering: build rows via DOM creation or innerHTML with escaping. Text contains special chars — must escape HTML. I'll write an esc() function and build with template strings + esc(). Or use DOM APIs. I'll use a helper `el(tag, cls, text)` or build strings with esc. Strings with esc is fine.

Full text display: `<div class="fulltext">` with textContent set (preserves newlines with pre-wrap). I'll create elements via DOM for the expanded content to avoid escaping issues, or use esc(). I'll use esc() consistently.

Reference box beside: in expanded row, layout: flex — left: "Extracted paragraph (page X)" + pre-wrap text; right (or below): "Reference first words: “...”" or "No reference entry for this number". Spec: "with the reference's first words shown beside it". I'll do a two-column flex: text (flex 2) and reference (flex 1). On narrow screens wrap.

Counters display: 
- Card 1: "Paragraphs found" big "N" small "of 90" → spec: 'The first counter reads "N of 90"'. So display "N of 90" prominently. Label: "Paragraphs found (reference: 90)"? I'll show big text `${found} of ${ref.paragraphs}` with label "paragraphs found / in reference".
- Card 2: `${footCount} of ${ref.footnotes}` label "footnotes removed / in reference".
- Card 3: `${diffCount}` label "paragraphs whose opening words differ" — maybe also "· X no reference". I'll add small sub-line: `${noRefCount} with no reference entry`.

Note under: "Found by the code from the page text; reference figures come from the file." Plus a "How this is computed" note. Spec requires: 'Under them: "Found by the code from the page text; reference figures come from the file."' — exact-ish text. I'll include that sentence verbatim, plus a longer how-computed note near the table.

Header line: title from data.title (e.g., "General comment No. 27 (2025) ..."), symbol linked: `<a href=doc_url>symbol</a>`. Meta line: `Raw PDF text, ${records.length} pages, source: ${source}`. Spec: "raw PDF text, N pages, source: …". I'll write: "Raw PDF text · N pages · source: …" — hmm, spec literally: one line: "raw PDF text, N pages, source: …". I'll do: `Raw PDF text, ${n} pages, source: ${source}`. Use data.source. Also maybe include data.count? records.length is N. Use records.length.

Also title: data.title — the sample pdf_text has `title` field. Use it. Also maybe show symbol big. Fine.

Now — "How this is computed" near every chart or number: I'll add a small note under the stats and one above the table:

Stats note: "Found by the code from the page text; reference figures come from the file. Paragraphs are counted by scanning the joined page text for lines that begin with the next expected number followed by a full stop; footnote lines (a small number then text at the foot of a page) are removed and counted."

Table note: "Each row is one numbered paragraph as extracted. 'Differs' means the first six words do not match the reference entry for that number, comparing word by word and ignoring case, punctuation and extra spaces. Click a row for the full text and the reference's first words."

Now, code size: keep under 700 lines. Fine.

Let me now write the parsing code carefully.

```js
const D = window.WORKSHOP_DATA.pdf_text;
const records = (D.records||[]).slice().sort((a,b)=>a.page-b.page);
const symbol = D.symbol || '';
const ref = D.reference || {};
const refFirst = ref.first_words || {};

// 1. collect lines per page
const pages = records.map(r => ({
  page: r.page,
  lines: String(r.text||'').split(/\r?\n/)
}));

// 2. classify header/footer lines
const kept = []; // {page, text, idx}
const removed = []; // {page, reason, text}
const sep = /^[-_—=]{4,}$/;
pages.forEach(p => {
  p.lines.forEach(raw => {
    const t = raw.trim();
    if (!t) return;
    if (t === symbol) { removed.push({page:p.page, reason:'header — document symbol', text:t}); return; }
    if (/^GE\.\s*\d/.test(t)) { removed.push({page:p.page, reason:'header — distribution code', text:t}); return; }
    if (/^\d{1,4}$/.test(t)) { removed.push({page:p.page, reason:'footer — page number', text:t}); return; }
    if (sep.test(t)) { removed.push({page:p.page, reason:'footer — rule/separator', text:t}); return; }
    kept.push({page:p.page, text:raw});
  });
});
```

Hmm wait — symbol check: what if symbol line has trailing spaces — trimmed, ok. What if the symbol appears with page number like "E/C.12/GC/27  4"? Not handled; accept.

Also — should I remove lines that are only the symbol with variations? t === symbol is fine.

```js
// 3. pass 1: find paragraph starts
const paraStart = []; // indices into kept
let expected = 1;
kept.forEach((L, i) => {
  const t = L.text.trim();
  const m = t.match(/^(\d+)\.(?:\s+(.*))?$/);
  if (m && parseInt(m[1],10) === expected) { paraStart.push(i); expected++; }
});
```

Wait — issue: `^(\d+)\.(?:\s+(.*))?$` — for "1." → m[1]="1", m[2]=undefined. For "1. text" → m[2]="text". For "12." ok. But also matches "2025." if expected===2025 — never. OK.

But hmm — what about a line like "1. " (number, period, trailing space)? trimmed → "1." fine.

```js
// 4. pass 2: per page, find foot region
const isFootLine = t => /^\d{1,3}\s+\S/.test(t);
// group kept indices by page
const byPage = new Map();
kept.forEach((L,i)=>{ if(!byPage.has(L.page)) byPage.set(L.page,[]); byPage.get(L.page).push(i); });
const footIdx = new Set();
byPage.forEach((idxs, page) => {
  const startSet = new Set(paraStart);
  // find first i in idxs with isFootLine and no paraStart after i within idxs
  for (let k=0;k<idxs.length;k++){
    const i = idxs[k];
    if (!isFootLine(kept[i].text.trim())) continue;
    let hasStartAfter = false;
    for (let j=k+1;j<idxs.length;j++){ if (startSet.has(idxs[j])) { hasStartAfter = true; break; } }
    if (!hasStartAfter) {
      // foot region = idxs[k..end]
      for (let j=k;j<idxs.length;j++) footIdx.add(idxs[j]);
      break;
    }
  }
});
```

Hmm wait — there's a flaw: if the first F-line has a paragraph-start after it (so it's body), we continue scanning; the NEXT F-line might have no start after → foot region from there. But what if there are two F-lines, first is body, second is a real footnote, and no start after second → foot region from second. Good. But what if first F-line is a real footnote and a paragraph-start appears after (impossible physically)... ok.

But another flaw: what if the page has body F-line early, then real footnotes at foot, no paragraph starts at all on the page? Then the FIRST F-line (body) would be taken as footStart → wrong. Accept residual risk.

Hmm, actually, wait. Let me reconsider — maybe add: prefer the LAST contiguous run? Alternative: foot region = the maximal suffix of the page where the FIRST line of the suffix is an F-line and... same thing. Or: choose the footStart as the first F-line after the last paragraph-start on the page (if any paragraph-start on page), else first F-line on page. That's equivalent-ish to my guard when starts exist. When no starts on page, first F-line. Same. OK keep.

Actually, hmm, one more improvement: footnotes usually come after a separator line. If the page has separator lines, footStart should be after the last separator. Let me incorporate: record separator positions per page (in kept-index space? separators are removed before kept...). Let me track separators as kept-line markers instead: instead of removing separators in step 2, mark them and remove later. Simpler: in step 2, when I see a separator, push to kept with a flag `sep:true`? Then in foot detection: footStart = first F-line after the last sep-flagged line on the page (if any sep on page); else the guard rule. And sep lines are removed (added to removed list) regardless.

Let me restructure: kept entries: {page, text, sep:boolean}. In step 2, separator → kept.push({page, text:t, sep:true}) AND removed.push(...). Then foot detection per page: lastSep = last index in idxs with sep flag; candidates = F-lines with index > lastSep (if lastSep exists) else all F-lines; footStart = first candidate with no paraStart after it on page. Then all lines from footStart to page end → footnotes. Also sep lines themselves are already in removed.

Hmm, but if separator exists and footnotes follow, footStart = first F-line after lastSep — good, and the "no paraStart after" guard still applies. If no separator, fallback guard. OK, but is this over-engineering? It adds robustness cheaply. I'll include it.

Wait, actually — do I even know separators exist in this text? Unknown. The code handles both. Fine.

```js
// 5. assemble paragraphs
const paragraphs = [];
const preamble = [];
let cur = null;
kept.forEach((L, i) => {
  if (footIdx.has(i)) {
    const t = L.text.trim();
    if (isFootLine(t)) footnotes.push({page:L.page, text:t});
    removed.push({page:L.page, reason: isFootLine(t)?'footnote':'footnote (continuation)', text:t});
    return;
  }
  if (L.sep) return; // already in removed
  const t = L.text.trim();
  const m = t.match(/^(\d+)\.(?:\s+(.*))?$/);
  if (m && parseInt(m[1],10) === cur? ... )
```

Hmm — careful: I need expected tracking consistent with pass 1. Let me just reuse paraStart: build a map from index → paragraph number. Then:

```js
const startNum = new Map(); // kept index -> paragraph number
paraStart.forEach((i,k)=> startNum.set(i, k+1));
let cur = null;
kept.forEach((L,i)=>{
  if (footIdx.has(i) || L.sep) { ...footnote/removed handling...; return; }
  if (startNum.has(i)) {
    if (cur) paragraphs.push(cur);
    const m = L.text.trim().match(/^(\d+)\.(?:\s+(.*))?$/);
    cur = { number: startNum.get(i), page: L.page, lines: m[2] ? [m[2]] : [] };
  } else {
    if (cur) cur.lines.push(L.text);
    else preamble.push({page:L.page, text:L.text.trim()});
  }
});
if (cur) paragraphs.push(cur);
```

Wait — but footnote handling inside this loop: I need footnotes counted and removed entries. Let me handle footIdx lines: if isFootLine → footnotes.push + removed reason 'footnote'; else removed reason 'footnote (continuation)'. And sep lines → already added to removed in step 2; skip here.

Hmm, but careful: preamble lines should also go into removed list (reason 'before paragraph 1'). I'll add them to removed with that reason. Actually let me keep preamble separate but also push to removed for the collapsed list. I'll push {reason:'before paragraph 1 (cover/heading)'}.

Wait, also: what about lines after the last paragraph start that are body (e.g., trailing "United Nations" footer at doc end, or "E/C.12/GC/27" at very end)? They append to last paragraph. Per spec, fine.

Then compute status per paragraph:

```js
function normWords(s){ return String(s||'').toLowerCase().replace(/[^\p{L}\p{N}]+/gu,' ').trim().split(/\s+/).filter(Boolean); }
paragraphs.forEach(p=>{
  const words = normWords(p.lines.join(' ')).slice(0,6);
  const refEntry = refFirst[String(p.number)];
  if (refEntry === undefined || refEntry === null || refEntry === '') { p.status='no reference'; p.refWords=''; }
  else {
    const rw = normWords(refEntry).slice(0,6);
    p.status = (words.length===rw.length && words.every((w,k)=>w===rw[k])) ? 'match' : 'differs';
    p.refWords = refEntry;
  }
  p.text = p.lines.join('\n');
});
```

Hmm — comparing lengths: if para has 6 words and ref has 6, fine. If para damaged to 3 words → lengths differ → differs. If ref entry has 6 words but para has 7+ → slice(0,6) both → compare 6. Good. Edge: ref entry might have more than 6 words? "first_words" = first six words, so 6. slice(0,6) safe.

Wait, one thing: `words.length===rw.length` — if ref has 6 and para has 6, ok. If para has fewer (short paragraph), differs — correct (damage). If para has more, sliced to 6. OK.

Hmm, but what if reference entry is empty string for some number? Treat as no reference? I'll treat missing key only as no reference; empty string → rw=[] and words.length>0 → differs. Eh, treat empty as no reference too. Fine.

Counters:
- found = paragraphs.length; refP = ref.paragraphs (number). Display `${found} of ${refP}`.
- footCount = footnotes.length; refF = ref.footnotes.
- diffCount = paragraphs.filter(p=>p.status==='differs').length; noRefCount = ...'no reference'.

Now rendering. Let me write the HTML/CSS.

CSS: 
```css
:root{--accent:#1f6fb2; --bg:#f5f7fa; --card:#fff; --border:#dde3ea; --text:#1c2733;}
*{box-sizing:border-box}
body{margin:0;font-family:system-ui,-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;font-size:16px;color:var(--text);background:var(--bg);line-height:1.5}
.wrap{max-width:1080px;margin:0 auto;padding:24px 20px 60px}
header... h1{font-size:1.5rem;margin:0 0 6px}
a{color:var(--accent)}
.meta{color:#4a5a68}
.stats{display:flex;gap:16px;flex-wrap:wrap;margin:20px 0 8px}
.stat{background:var(--card);border:1px solid var(--border);border-radius:10px;padding:14px 18px;min-width:200px;flex:1}
.stat .big{font-size:1.6rem;font-weight:700;color:var(--accent)}
.stat .lbl{font-size:.9rem;color:#4a5a68}
.note{font-size:.85rem;color:#5a6a78;margin:6px 0 0}
.controls{display:flex;gap:16px;align-items:center;margin:18px 0 10px;flex-wrap:wrap}
button{background:var(--accent);color:#fff;border:0;border-radius:8px;padding:9px 16px;font-size:1rem;cursor:pointer}
label.chk{display:flex;gap:8px;align-items:center;cursor:pointer}
table{width:100%;border-collapse:collapse;background:var(--card);border:1px solid var(--border);border-radius:10px;overflow:hidden}
th,td{padding:10px 12px;text-align:left;border-bottom:1px solid var(--border);vertical-align:top;font-size:.95rem}
th{background:#eef3f8;font-weight:600}
tbody tr.data{cursor:pointer}
tbody tr.data:hover{background:#f2f7fc}
td.num{font-weight:700;white-space:nowrap}
td.page{white-space:nowrap}
td.first{max-width:...}
.badge{display:inline-block;padding:2px 8px;border-radius:999px;font-size:.8rem;font-weight:600}
.badge.diff{background:#fde8e8;color:#b42318}
.badge.noref{background:#fff4e0;color:#9a6700}
.badge.ok{background:#e6f4ea;color:#1e7e34}
tr.expanded td{background:#fbfdff}
.fulltext{white-space:pre-wrap;font-size:.9rem;background:#fff;border:1px solid var(--border);border-radius:8px;padding:12px;max-height:320px;overflow:auto}
.refbox{...}
details{margin-top:22px;background:var(--card);border:1px solid var(--border);border-radius:10px;padding:12px 16px}
summary{cursor:pointer;font-weight:600}
.removed-list{...}
```

Table columns: ¶ | Page | First line | Document | Check. The "Document" column shows symbol link in every row — a bit repetitive but spec says so ("symbol linked to doc_url" per row). OK.

Expanded row content:
```html
<tr class="expanded"><td colspan="5">
  <div class="exp-grid">
    <div><div class="exp-h">Full paragraph as extracted (starts on page X)</div><div class="fulltext">...</div></div>
    <div><div class="exp-h">Reference first words</div><div class="refbox">“...”</div> or <div class="refbox noref">No reference entry for paragraph N</div></div>
  </div>
</td></tr>
```

exp-grid: display:flex; gap:16px; flex-wrap:wrap; children flex:1 1 320px.

Rendering approach: build tbody HTML string with esc() for all text. Row:

```js
function esc(s){return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');}
```

Row html:
```js
`<tr class="data" data-n="${p.number}">
  <td class="num">${p.number}.</td>
  <td class="page">${p.page}</td>
  <td class="first">${esc(firstLine90)}</td>
  <td><a href="${esc(D.doc_url)}" target="_blank" rel="noopener">${esc(symbol)}</a></td>
  <td>${badge}</td>
</tr>` + (expanded===p.number ? expandedRow : '')
```

firstLine90: `const fl = (p.lines.find(l=>l.trim())||'').trim(); fl.length>90 ? fl.slice(0,90)+'…' : fl`.

Badge: differs → `<span class="badge diff">Differs</span>`; no reference → `<span class="badge noref">no reference</span>`; match → `<span class="badge ok">matches</span>`. Spec: 'a "Differs" mark where the opening words do not match' — match rows can show a subtle tick "✓" or "matches". I'll show "✓ matches" green-ish. Fine.

Sorting: 
```js
function render(){
  const rows = paragraphs.slice();
  if (diffFirst.checked) rows.sort((a,b)=> (a.status==='differs'?0:1)-(b.status==='differs'?0:1)); // stable in modern JS
  tbody.innerHTML = rows.map(rowHtml).join('');
}
```
Array.prototype.sort is stable in modern browsers. Good.

Click handling:
```js
tbody.addEventListener('click', e=>{
  const tr = e.target.closest('tr.data'); if(!tr) return;
  const n = +tr.dataset.n;
  expanded = (expanded===n) ? null : n;
  render();
});
```

CSV:
```js
function downloadCSV(){
  const head = 'number,page,status,text';
  const rows = paragraphs.map(p=>{
    const text = '"' + p.text.replace(/"/g,'""') + '"';
    return [p.number, p.page, '"'+p.status+'"', text].join(',');
  });
  const csv = [head].concat(rows).join('\r\n');
  const blob = new Blob([csv], {type:'text/csv;charset=utf-8'});
  ...
}
```

Hmm, status quoted: `"match"`. Fine. Or unquoted. "values quoted" — quote text and status. OK.

Removed list rendering:
```js
removedList.innerHTML = removed.map(r=>`<li><span class="pg">p. ${r.page}</span> <span class="rs">${esc(r.reason)}</span> — ${esc(truncate(r.text,120))}</li>`).join('');
```
Summary: `Lines removed as headers, footers and footnotes (${removed.length} lines: ${footCount} footnote lines, ${headerCount} header/footer lines, ${preambleCount} before paragraph 1)`. Keep simpler: `(${removed.length} lines)`.

Also show counts by reason maybe. Keep simple.

Now — the "How this is computed" notes. Also the meta line. Also handle empty data gracefully (if records empty → show message). Add guards: if (!D || !records.length) show "no data".

Also — the spec says title and symbol linked to doc_url. I'll make the h1 the title, and below: `<a href=doc_url>symbol</a>` prominent. Meta: `Raw PDF text, ${records.length} pages, source: ${D.source}`.

Wait — also data.count exists; use records.length for N (actual). Fine.

Let me also double check the success criterion: "Clicking row 1 shows text starting 'A clean, healthy and sustainable environment'." With my parsing: page 1 lines: "E/C.12/GC/27" removed; "United Nations" preamble; "Economic and Social Council" preamble; "Distr.: General" preamble; "6 November 2025" preamble; "Original: English" preamble; "Committee on Economic, Social and Cultural Rights" preamble; "General comment No. 27 (2025) on economic, social and" preamble; "cultural rights and the environmental dimension of" preamble; "sustainable development*" preamble; "I." — hmm! "I." — trimmed "I." matches ^(\d+)\.? No — \d+ requires digits; "I." is a letter. Not a match. Preamble. Good. "Introduction" preamble. "1." → paragraph start, expected 1 ✓. Then "A clean, healthy and sustainable environment is an essential precondition for the" etc. → paragraph 1 lines. 

But wait — "General comment No. 27 (2025)..." — contains "27 (2025)" but line starts with "General" — not a number start. Fine. What about a line starting with "2025"? /^\d{1,4}$/ only if alone. "6 November 2025" — not alone. Fine.

Hmm — one more: "Distr.: General" — I decided preamble. But wait, is "Distr.: General" maybe followed by "GE.25-..." line? The sample shows "Distr.: General\n6 November 2025\nOriginal: English" — no GE on page 1. Later pages have GE codes. OK.

Now — potential problem: page numbers. Page 1 sample doesn't show a page number line. Pages 2-20 presumably have "2".."20" alone → removed as page number. But WAIT: what if the page number line is like "2" and my paragraph-start regex... "2" has no period → not a paragraph start. And /^\d{1,4}$/ removes it. But what if a paragraph number line lost its period due to damage, e.g., "12" alone? Then removed as page number AND paragraph 12 merges. The tool would show N < 90 — visible. OK.

Another subtle thing: the foot region detection — footnotes at the foot of a page come AFTER the page's body. But the page's header lines (symbol, GE, page number) — are they at the top or bottom of the page text? If at the bottom (some converters put page number at end), my removal handles them anywhere. But the foot-region detection operates on kept lines (headers already removed), so footnotes = last lines. If the page number were at the very end (after footnotes), it's removed as page number before foot detection — good, doesn't break the "suffix" logic since it's removed. 

Now, what if footnotes appear BEFORE the body on a page (weird)? No.

What about the LAST page (page 20) — might end with footnotes and no more body. Fine.

Also — what if a footnote line appears at the foot of a page where the last paragraph continues to the next page? Foot region = suffix; body lines before it belong to the paragraph. Good.

Edge: what if the ENTIRE page after headers is footnotes (footStart = 0)? Then no body lines; fine.

Now let me also think: could a paragraph-start line be INSIDE the foot region (after footStart)? My guard says footStart chosen such that no paraStart after it on the page — so no. But paraStart was computed including foot lines... foot lines don't match paraStart pattern (no period). Unless footnote "12. text" — then it might be in paraStart if expected===12! Then it's a "paragraph start" and the guard would prevent foot region before it... and the footnote would become a paragraph! Ugh. But per spec footnotes have no period. Accept.

Hmm, actually wait — let me reconsider the footnote format once more. UN treaty body documents (OHCHR): footnotes at the bottom of the page look like:

```
____________________________________________________________________
1	See general comment No. 8 (1990)...
```

Yes, number + tab. Some newer docs: "1  Text". No period. Confident enough.

But hmm, what about footnote continuation lines that start with a number? E.g., wrapped footnote "...resolution 2200 (1966)..." wrapping so next line starts with "2200"? 4 digits — F requires \d{1,3}\s — "2200 " → \d{1,3} matches "220", next char "0" not \s → no match. Good. "60 (1)" wrapping → line starts "60 (1)..." → F matches (60 + space)! But it's inside foot region already (continuation) — counted? In my assembly, foot region lines: isFootLine → counted as footnote; else continuation. A continuation line starting "60 (1)" would be counted as an extra footnote. Minor overcount. Could mitigate: within foot region, only count F-lines... that's what I do. Hmm, to reduce overcount: count only F-lines whose number is "small" — already 1-3 digits. "60" is 2 digits. Can't distinguish. Accept — the counter shows both numbers, and the removed list lets the reader verify. Actually — alternative: count footnotes as F-lines in foot region; the reference count will tell. If mismatch, visible. It's a checking tool after all. OK.

Hmm, actually, wait. Let me reconsider: maybe count footnotes differently — the spec says "Footnote lines (a small number then text, at the foot of a page) are removed from the paragraphs and only counted." So count = number of footnote lines removed. My approach matches the spec literally. Good.

Now, "paragraphs whose opening words differ" counter — third counter. Also maybe show no-reference count. I'll put in the stat card sub-line: "X differ · Y no reference entry". Hmm, spec says three counters: found/ref, footnotes/ref, differ count. I'll make card 3 big = diffCount, label "paragraphs whose opening words differ from the reference", sub = "Z paragraphs have no reference entry". Good.

Now write the full HTML. Also add a small "How this is computed" under stats (required note) and above table.

Let me also handle: what if ref.paragraphs is undefined? Guard with ?? '—'. Use `ref.paragraphs ?? '?'`.

Also the header: "Title and symbol linked to doc_url" — I'll link the symbol; maybe also link title? Spec: "Title and symbol linked to doc_url" — ambiguous; I'll link both title and symbol? "Title and symbol linked to doc_url" — I'll make the symbol a link, and the title plain (or also linked). I'll link the symbol prominently; title as h1 plain. Hmm, "Title and symbol linked to doc_url" could mean both are linked. I'll link both — harmless. Actually I'll make h1 contain a link to doc_url with the title text, and below a line with symbol link. Fine.

Let me now also think about the "first line (about 90 characters)" — I'll show up to 90 chars of the first non-empty line of the paragraph. If the paragraph's first line is short, show it fully.

Table width: 5 columns; first-line column should wrap. Set table-layout auto; give .first a max-width via CSS? With width:100% and word wrap, fine. To avoid horizontal scroll, keep table width 100% and let text wrap. The symbol link is long ("E/C.12/GC/27" — short). OK.

Now, the expanded row: full text can be long — max-height with scroll (320px) — acceptable, no animation.

Let me write the code now.

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Paragraph check — E/C.12/GC/27</title>
```

Wait — title should come from data, but <title> is static; I can set document.title in JS from D.title. I'll put a generic title and update via JS.

Let me draft the whole thing:

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Paragraph checker</title>
<style>
:root{--accent:#1f6fb2;--bg:#f4f6f9;--card:#ffffff;--border:#d9e0e8;--ink:#1b2733;--muted:#55636f}
*{box-sizing:border-box}
html,body{margin:0;padding:0}
body{font-family:system-ui,-apple-system,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif;font-size:16px;line-height:1.5;color:var(--ink);background:var(--bg)}
.wrap{max-width:1100px;margin:0 auto;padding:28px 20px 64px}
h1{font-size:1.45rem;line-height:1.3;margin:0 0 4px}
h1 a{color:inherit;text-decoration:none}
h1 a:hover{color:var(--accent)}
.sym{font-size:1.05rem;margin:0 0 4px}
.sym a{color:var(--accent);font-weight:600;text-decoration:none}
.sym a:hover{text-decoration:underline}
.meta{color:var(--muted);margin:0}
.stats{display:flex;flex-wrap:wrap;gap:14px;margin:22px 0 6px}
.stat{flex:1 1 220px;background:var(--card);border:1px solid var(--border);border-radius:10px;padding:14px 18px}
.stat .big{font-size:1.7rem;font-weight:700;color:var(--accent);line-height:1.2}
.stat .lbl{font-size:.92rem;color:var(--muted);margin-top:2px}
.note{font-size:.86rem;color:var(--muted);margin:8px 0 0;max-width:70ch}
.controls{display:flex;flex-wrap:wrap;align-items:center;gap:18px;margin:20px 0 12px}
.chk{display:flex;align-items:center;gap:8px;cursor:pointer;user-select:none}
button{background:var(--accent);color:#fff;border:0;border-radius:8px;padding:9px 18px;font-size:1rem;cursor:pointer;font-family:inherit}
button:hover{background:#185a94}
.how{font-size:.86rem;color:var(--muted);margin:0 0 10px;max-width:75ch}
.tablewrap{background:var(--card);border:1px solid var(--border);border-radius:10px;overflow-x:auto}
table{width:100%;border-collapse:collapse}
th,td{padding:9px 12px;text-align:left;vertical-align:top;border-bottom:1px solid var(--border);font-size:.94rem}
thead th{background:#edf2f7;font-size:.85rem;text-transform:uppercase;letter-spacing:.03em;color:#3c4a56}
tbody tr.data{cursor:pointer}
tbody tr.data:hover{background:#f1f7fc}
td.num{font-weight:700;white-space:nowrap}
td.pg{white-space:nowrap;color:var(--muted)}
td.doc a{color:var(--accent);text-decoration:none;white-space:nowrap}
td.doc a:hover{text-decoration:underline}
.badge{display:inline-block;padding:2px 9px;border-radius:999px;font-size:.78rem;font-weight:700;white-space:nowrap}
.b-diff{background:#fdecea;color:#b42318}
.b-noref{background:#fef3e2;color:#92610a}
.b-ok{background:#e8f4ec;color:#217a3c}
tr.exp td{background:#f8fbfe;padding:14px 16px}
.exp{display:flex;flex-wrap:wrap;gap:16px}
.exp>div{flex:1 1 340px;min-width:0}
.exp h3{font-size:.82rem;text-transform:uppercase;letter-spacing:.04em;color:#3c4a56;margin:0 0 6px}
.fulltext{white-space:pre-wrap;word-break:break-word;background:#fff;border:1px solid var(--border);border-radius:8px;padding:12px 14px;font-size:.9rem;max-height:340px;overflow:auto}
.refbox{background:#fff;border:1px solid var(--border);border-left:4px solid var(--accent);border-radius:8px;padding:12px 14px;font-size:.92rem}
.refbox.none{border-left-color:#c9a227;color:var(--muted)}
details{margin-top:24px;background:var(--card);border:1px solid var(--border);border-radius:10px;padding:12px 18px}
summary{cursor:pointer;font-weight:600}
summary span{color:var(--muted);font-weight:400}
.removed{margin:10px 0 4px;padding-left:0;list-style:none;font-size:.88rem;max-height:360px;overflow:auto}
.removed li{padding:4px 0;border-bottom:1px dashed #e6ebf1}
.removed .pg{display:inline-block;min-width:44px;color:var(--accent);font-weight:600}
.removed .rs{color:var(--muted)}
footer{margin-top:26px;font-size:.84rem;color:var(--muted)}
</style>
</head>
<body>
<div class="wrap">
  <h1 id="hTitle"></h1>
  <p class="sym"><a id="hSym" target="_blank" rel="noopener"></a></p>
  <p class="meta" id="hMeta"></p>

  <div class="stats">
    <div class="stat"><div class="big" id="sPar"></div><div class="lbl">paragraphs found / paragraphs in the reference</div></div>
    <div class="stat"><div class="big" id="sFoot"></div><div class="lbl">footnote lines removed / footnotes in the reference</div></div>
    <div class="stat"><div class="big" id="sDiff"></div><div class="lbl">paragraphs whose opening words differ from the reference</div></div>
  </div>
  <p class="note" id="sNote"></p>

  <div class="controls">
    <label class="chk"><input type="checkbox" id="diffFirst"> Show differences first</label>
    <button id="csvBtn" type="button">Download CSV</button>
  </div>

  <p class="how" id="howTbl"></p>

  <div class="tablewrap">
    <table>
      <thead><tr>
        <th>¶</th><th>Page</th><th>First line of the paragraph</th><th>Document</th><th>Check</th>
      </tr></thead>
      <tbody id="tbody"></tbody>
    </table>
  </div>

  <details id="detRemoved">
    <summary id="sumRemoved"></summary>
    <ul class="removed" id="ulRemoved"></ul>
  </details>

  <footer id="foot"></footer>
</div>
<script>
... 
</script>
</body>
</html>
```

JS:

```js
(function(){
"use strict";
var D = window.WORKSHOP_DATA && window.WORKSHOP_DATA.pdf_text;
function esc(s){return String(s==null?'':s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');}
if(!D || !D.records || !D.records.length){
  document.getElementById('hTitle').textContent='No data';
  document.querySelector('.wrap').insertAdjacentHTML('beforeend','<p>No pdf_text data was found in WORKSHOP_DATA.</p>');
  return;
}
var records = D.records.slice().sort(function(a,b){return (a.page||0)-(b.page||0);});
var symbol = D.symbol||'';
var docUrl = D.doc_url||'#';
var ref = D.reference||{};
var refFirst = ref.first_words||{};

document.title = (D.title||'Paragraph checker') + ' — paragraph check';
document.getElementById('hTitle').innerHTML = '<a href="'+esc(docUrl)+'" target="_blank" rel="noopener">'+esc(D.title||symbol)+'</a>';
var hs=document.getElementById('hSym'); hs.href=docUrl; hs.textContent=symbol;
document.getElementById('hMeta').textContent = 'Raw PDF text, '+records.length+' pages, source: '+(D.source||'—');

// --- parse ---
var kept=[], removed=[], footnotes=[];
var sepRe=/^[-_—=]{4,}$/;
records.forEach(function(r){
  var lines=String(r.text||'').split(/\r?\n/);
  lines.forEach(function(raw){
    var t=raw.trim();
    if(!t) return;
    if(t===symbol){removed.push({page:r.page,reason:'header · document symbol',text:t});return;}
    if(/^GE\.\s*\d/.test(t)){removed.push({page:r.page,reason:'header · distribution code',text:t});return;}
    if(/^\d{1,4}$/.test(t)){removed.push({page:r.page,reason:'footer · page number',text:t});return;}
    if(sepRe.test(t)){removed.push({page:r.page,reason:'footer · rule/separator',text:t});kept.push({page:r.page,text:t,sep:true});return;}
    kept.push({page:r.page,text:raw});
  });
});
```

Hmm wait — I push sep lines into kept with sep flag so foot detection can use them, and also into removed. Then in assembly, sep lines are skipped (already removed). OK.

```js
function isFootLine(t){return /^\d{1,3}\s+\S/.test(t);}
function paraStartMatch(t){var m=t.match(/^(\d+)\.(?:\s+(.*))?$/);return m?{n:parseInt(m[1],10),rest:m[2]||''}:null;}

// pass 1: paragraph starts
var expected=1, startNum=new Map();
kept.forEach(function(L,i){
  if(L.sep) return;
  var m=paraStartMatch(L.text.trim());
  if(m && m.n===expected){startNum.set(i,expected);expected++;}
});
```

Wait — careful: pass 1 must skip sep lines (they're not paragraph starts anyway — "____" doesn't match). Fine either way.

```js
// pass 2: foot regions per page
var byPage=new Map();
kept.forEach(function(L,i){var a=byPage.get(L.page);if(!a){a=[];byPage.set(L.page,a);}a.push(i);});
var footIdx=new Set();
byPage.forEach(function(idxs){
  var lastSep=-1;
  idxs.forEach(function(i,k){if(kept[i].sep)lastSep=k;});
  for(var k=(lastSep+1);k<idxs.length;k++){
    var i=idxs[k];
    if(kept[i].sep) continue;
    if(!isFootLine(kept[i].text.trim())) continue;
    var startAfter=false;
    for(var j=k+1;j<idxs.length;j++){if(startNum.has(idxs[j])){startAfter=true;break;}}
    if(!startAfter){
      for(var j2=k;j2<idxs.length;j2++) footIdx.add(idxs[j2]);
      break;
    }
  }
});
```

Hmm — wait, there's a bug: if lastSep exists, I start scanning from lastSep+1 — but footnotes come after the separator, good. If a body F-line exists before the separator, ignored — good. If no separator, scan from 0 with the startAfter guard. But one more: if lastSep exists but footnotes... always after separator. OK. But what if separator exists at page top (header rule)? Then lastSep is early, fine.

Edge: what if the foot region contains a sep line (multiple separators)? footIdx includes them; in assembly they're skipped as sep. Fine.

```js
// pass 3: assemble
var paragraphs=[], cur=null;
kept.forEach(function(L,i){
  if(footIdx.has(i)){
    var t=L.text.trim();
    var isF=isFootLine(t);
    if(isF) footnotes.push({page:L.page,text:t});
    removed.push({page:L.page,reason:isF?'footnote':'footnote · continuation line',text:t});
    return;
  }
  if(L.sep) return;
  if(startNum.has(i)){
    if(cur) paragraphs.push(cur);
    var m=paraStartMatch(L.text.trim());
    cur={number:startNum.get(i),page:L.page,lines:m.rest?[m.rest]:[]};
  } else if(cur){
    cur.lines.push(L.text);
  } else {
    removed.push({page:L.page,reason:'before paragraph 1 · cover/heading',text:L.text.trim()});
  }
});
if(cur) paragraphs.push(cur);
```

Wait — issue: lines pushed to cur.lines keep raw text (with leading spaces). For display pre-wrap that's fine. For first-words normalization, fine. For CSV, fine ("exactly as extracted"). But the first line for the table: `cur.lines.find(l=>l.trim())` then trim for display. OK.

Hmm — also: should I trim each line when joining? "never edited" — keep raw. But leading indentation in pre-wrap shows. Fine, it's "exactly as extracted".

```js
function normWords(s){return String(s||'').toLowerCase().replace(/[^\p{L}\p{N}]+/gu,' ').trim().split(/\s+/).filter(Boolean);}
paragraphs.forEach(function(p){
  p.text=p.lines.join('\n');
  var words=normWords(p.text).slice(0,6);
  var entry=refFirst[String(p.number)];
  if(entry==null||entry===''){p.status='no reference';p.ref='';}
  else{
    var rw=normWords(entry).slice(0,6);
    p.status=(words.length===rw.length&&words.every(function(w,k){return w===rw[k];}))?'match':'differs';
    p.ref=entry;
  }
});
var found=paragraphs.length;
var refP=(ref.paragraphs!=null?ref.paragraphs:'?');
var refF=(ref.footnotes!=null?ref.footnotes:'?');
var diffCount=paragraphs.filter(function(p){return p.status==='differs';}).length;
var noRef=paragraphs.filter(function(p){return p.status==='no reference';}).length;
```

Stats:
```js
document.getElementById('sPar').textContent=found+' of '+refP;
document.getElementById('sFoot').textContent=footnotes.length+' of '+refF;
document.getElementById('sDiff').textContent=String(diffCount)+(noRef?('  ('+noRef+' with no reference entry)'):'');
document.getElementById('sNote').textContent='Found by the code from the page text; reference figures come from the file. Paragraphs are found by scanning the joined page text for a line that begins with the next expected number and a full stop; footnote lines (a small number then text at the foot of a page) are removed and counted; “Differs” compares the first six words with the reference entry, ignoring case, punctuation and extra spaces.';
```

Hmm — the note under counters should include the exact sentence "Found by the code from the page text; reference figures come from the file." — included. Good.

Table note:
```js
document.getElementById('howTbl').textContent='How this is computed: pages are joined in order; lines that are only a page number, the document symbol or a “GE.” distribution code are dropped; each row is one numbered paragraph exactly as extracted. Click a row to open the full text beside the reference’s first words. “Differs” = the first six words do not match the reference for that number.';
```

Render:
```js
var tbody=document.getElementById('tbody');
var diffFirst=document.getElementById('diffFirst');
var expanded=null;
function firstLine(p){
  for(var i=0;i<p.lines.length;i++){var t=p.lines[i].trim();if(t)return t.length>90?t.slice(0,90)+'…':t;}
  return '';
}
function badge(p){
  if(p.status==='differs')return '<span class="badge b-diff">Differs</span>';
  if(p.status==='no reference')return '<span class="badge b-noref">no reference</span>';
  return '<span class="badge b-ok">✓ matches</span>';
}
function rowHtml(p){
  var h='<tr class="data" data-n="'+p.number+'">'
    +'<td class="num">'+p.number+'.</td>'
    +'<td class="pg">'+p.page+'</td>'
    +'<td class="first">'+esc(firstLine(p))+'</td>'
    +'<td class="doc"><a href="'+esc(docUrl)+'" target="_blank" rel="noopener">'+esc(symbol)+'</a></td>'
    +'<td>'+badge(p)+'</td>'
    +'</tr>';
  if(expanded===p.number){
    h+='<tr class="exp"><td colspan="5"><div class="exp">'
      +'<div><h3>Full paragraph as extracted · starts on page '+p.page+'</h3><div class="fulltext">'+esc(p.text)+'</div></div>'
      +'<div><h3>Reference first words for paragraph '+p.number+'</h3>'
      +(p.status==='no reference'
        ?'<div class="refbox none">No reference entry for this number in the file.</div>'
        :'<div class="refbox">“'+esc(p.ref)+'”'+(p.status==='differs'?'<br><strong>→ opening words differ.</strong>':'')+'</div>')
      +'</div></div></td></tr>';
  }
  return h;
}
function render(){
  var rows=paragraphs.slice();
  if(diffFirst.checked){
    rows.sort(function(a,b){return (a.status==='differs'?0:1)-(b.status==='differs'?0:1);});
  }
  tbody.innerHTML=rows.map(rowHtml).join('');
}
diffFirst.addEventListener('change',render);
tbody.addEventListener('click',function(e){
  var tr=e.target.closest?e.target.closest('tr.data'):null;
  if(!tr)return;
  var n=parseInt(tr.getAttribute('data-n'),10);
  expanded=(expanded===n)?null:n;
  render();
});
render();
```

Wait — expanded row: after re-render on click, the expanded row appears right after its data row. Good. But when sorting with diffFirst, expanded row follows the row wherever it lands. Good.

Hmm — one issue: clicking a link inside a row (the doc link) would also trigger row toggle. Check: if e.target.closest('a') → return (let link work). Add that.

CSV:
```js
document.getElementById('csvBtn').addEventListener('click',function(){
  var lines=['number,page,status,text'];
  paragraphs.forEach(function(p){
    var text='"'+p.text.replace(/"/g,'""')+'"';
    lines.push([p.number,p.page,'"'+p.status+'"',text].join(','));
  });
  var csv=lines.join('\r\n');
  var blob=new Blob([csv],{type:'text/csv;charset=utf-8'});
  var url=URL.createObjectURL(blob);
  var a=document.createElement('a');
  a.href=url;
  a.download=(symbol?symbol.replace(/[^\w.-]+/g,'_'):'pdf_text')+'_paragraphs.csv';
  document.body.appendChild(a);a.click();document.body.removeChild(a);
  setTimeout(function(){URL.revokeObjectURL(url);},1000);
});
```

Removed list:
```js
var footN=footnotes.length;
var hdrN=removed.filter(r=>r.reason.indexOf('header')===0||r.reason.indexOf('footer')===0).length;
var preN=removed.filter(r=>r.reason.indexOf('before paragraph 1')===0).length;
document.getElementById('sumRemoved').innerHTML='Lines removed as headers, footers and footnotes <span>('+removed.length+' lines: '+footN+' footnote lines, '+hdrN+' header/footer lines, '+preN+' cover lines before paragraph 1)</span>';
document.getElementById('ulRemoved').innerHTML=removed.map(function(r){
  var t=r.text.length>140?r.text.slice(0,140)+'…':r.text;
  return '<li><span class="pg">p. '+r.page+'</span><span class="rs">'+esc(r.reason)+'</span> — '+esc(t)+'</li>';
}).join('');
```

Footer:
```js
document.getElementById('foot').textContent='Source: '+ (D.source||'') +' · '+records.length+' pages joined in order · '+found+' paragraphs extracted · reference: '+refP+' paragraphs, '+refF+' footnotes'+(ref.adopted?(' · adopted '+ref.adopted):'')+'.';
```

Hmm, ref.adopted — reference has `adopted`. Could show "adopted ..." in header meta maybe. Optional. I'll include in footer if present.

Also — the meta line: "raw PDF text, N pages, source: …". Done.

One more check on the "Differs" definition: "paragraphs whose opening words differ from the reference" — counter 3 counts differs. Also rows marked. Good.

Now — the checkbox label "Show differences first" — exact text per spec. Good.

Potential issue: `e.target.closest` — e.target could be text node? In DOM events target is element. Fine. But if click on the expanded row's content — closest('tr.data') null → return. Good.

Also add: clicking row toggles; add aria? Keep simple but add `title` maybe. Fine.

Now — one more consideration on pass 1: `paraStartMatch` on trimmed line. What if a paragraph number line has trailing text on the same line, e.g., "1. A clean..."? Then rest = "A clean..." — first line of paragraph. Good.

What about lines like "1." appearing when expected is 1 but it's actually... fine.

What about the possibility that the number and text are separated but the number line is "1 ."? No.

Now — the success criterion "The table numbers run 1, 2, 3 … without gaps" — by construction (expected counter). "at least 30 rows" — depends on data; should be ~90.

"Clicking row 1 shows text starting 'A clean, healthy and sustainable environment'" — paragraph 1 lines: after "1." line, next lines. In the sample, "1." is alone, then "A clean, healthy and sustainable environment is an essential precondition for the". p.text starts with that line. ✓. And status: refFirst["1"]="A clean, healthy and sustainable environment" → normWords → ["a","clean","healthy","and","sustainable","environment"]; para first 6 words: "A clean, healthy and sustainable environment is..." → same 6. Match ✓.

Now, one concern: the sample page-1 text shows "sustainable development*\nI.\n\nIntroduction\n1.\nA clean..." — "I." line: trimmed "I." — paraStartMatch: ^(\d+)\. — "I" not digit → null. Good, preamble.

But wait — what about Roman numeral section headings like "II." "III."? Not digits. Good. What about "V."? fine.

What about a line "4." when expected is 4 — paragraph start ✓.

Another: what if the converter emits the paragraph number and text with the number at line start but with leading spaces "  1."? trimmed handles.

Now — footnote detection worry: what if footnotes in this doc are formatted as "1" alone on a line followed by text on the next line? Then "1" alone → removed as "footer · page number"! And the text line becomes... body/footnote-continuation. Hmm. That would corrupt counts. But spec explicitly describes footnote lines as "a small number then text" — same line. Trust.

What if footnote lines are like "* text" or "________"? Handled separator; asterisk footnotes — "a small number then text" per spec. Trust.

Now, another thought on the foot-region guard: consider page with body text, then footnotes, and the page's LAST body line happens to be a paragraph start (e.g., "12." alone at the very bottom, text on next page). Then paraStart exists at index k, footnotes after. My scan: first F-line after lastSep... if no sep, scan from 0: the F-lines are after the paraStart; for the first F-line, check startAfter — paraStart at earlier index, not after → footStart = first F-line ✓. Good.

Consider page where body has F-line "3 per cent" mid-page and a paragraph start later: scan: first F-line at k, startAfter=true → continue; next F-line (real footnote) → startAfter false → footStart there ✓. 

Consider page with no paragraph starts and body F-line near end (false positive): footStart = that line, rest of page removed as footnotes. The removed list shows them — reader can verify. Acceptable.

Now — hmm, one more important case: what if footnotes appear at the foot of a page AND the next paragraph starts on the SAME page after the footnotes? Physically impossible in the PDF. OK.

What if the converter put the NEXT page's header at the end of the current page's text? Headers removed anyway. OK.

Now let me also double check the GE regex: "GE." followed by digits — /^GE\.\s*\d/ — sample "GE.25-12345" ✓. Also maybe "GE. 25-..." fine.

Page number: /^\d{1,4}$/ — pages 1-20 ✓. But what if page number line is "20" and also... fine. What if a page number is "100"? \d{1,4} covers.

Hmm — wait, danger: what if a paragraph number line is just "12" WITHOUT period (converter damage)? Removed as page number → paragraph merges → counter shows fewer than 90. The tool flags it via counter. But also the removed list shows "12" as footer page number — reader can see. OK, that's the tool's purpose.

Now — the CSV "as many rows as the table" — paragraphs.length rows + header. Table rows = paragraphs.length (data rows). ✓.

Let me also make sure no horizontal scrolling: table inside .tablewrap with overflow-x:auto as safety; but content should fit. The first-line column wraps. OK.

Fonts: system stack ✓. Accent #1f6fb2 ✓. Base 16px ✓. Light background ✓.

Now, "Every row that shows a document has its symbol, linked to doc_url in a new tab" ✓ (target=_blank rel=noopener).

Let me also add `lang="en"`, meta viewport ✓.

One more requirement: "Before the code block: at most three short sentences saying what you built or changed. After it: nothing." So my reply: 1-3 sentences, then the html code block, nothing after.

Also — "the app itself must explain what it shows" — the notes do that.

Let me now also double-check the regex for paragraph start with rest: /^(\d+)\.(?:\s+(.*))?$/ — for "1." → matches, rest undefined → ''. For "1. text" → rest "text". For "10." ✓. For "2025." → n=2025, only if expected===2025 — never. For "16.3 x" → no match (as analyzed). For "3.5 million" → "3" then "." then "5" — \s+ fails, $ fails; backtrack \d+="3"? then need "." — next char after "3" is "." ✓ then (?:\s+...)? next "5" — optional group can be empty, then $ — "5 million" remains → fail. So no match ✓. Good — "3.5 million" won't start a paragraph.

But hmm — what about a line "12. " with trailing space — trimmed → "12." ✓.

What about "1.Introduction" (no space)? No match → body line. Acceptable.

Now — one more subtle thing: pass 1 uses trimmed text; pass 3 re-matches trimmed. Consistent.

Also — what if two consecutive paragraph-start lines (empty paragraph, e.g., "5." immediately followed by "6.")? Then paragraph 5 has lines=[] → text='' → firstLine '' → status: words=[] vs rw 6 → differs. Row shows empty first line. Fine, honest.

Now, the `Map` usage — fine in sandbox.

Unicode regex /[^\p{L}\p{N}]+/gu — supported in modern browsers. OK.

Let me also consider: `ref.first_words` keys are strings of numbers ("1"). String(p.number) ✓.

Now assemble final HTML. Also set `document.title`.

Also — the h1 link: title text might be long; fine.

Let me also reconsider the stat card 3 label: "paragraphs whose opening words differ from the reference" — big number = diffCount. If noRef>0, append small note. I'll put the noRef info in the note line instead to keep the big number clean. Actually I'll add a small sub-line in the card: `<div class="lbl">...` plus maybe. Keep: big = diffCount, lbl = "paragraphs whose opening words differ from the reference". And sNote includes: "... X paragraphs have no reference entry." Let me include in sNote: append sentence "Paragraphs with no reference entry are marked 'no reference' (N of them)." Good.

Wait, the required note text: 'Under them: "Found by the code from the page text; reference figures come from the file."' — I'll start sNote with exactly that sentence, then add the how-computed sentences. Good.

Also the header meta line must read "raw PDF text, N pages, source: …" — I'll write: "Raw PDF text, 20 pages, source: …". Capitalization fine.

Let me also handle D.count vs records.length — use records.length.

Edge: what if some records have same page? sort stable, fine.

Now, about the removed list — it might include the preamble cover lines (~10 lines) + per-page headers (20 pages × ~3 = 60) + footnotes. ~100 lines in a scrollable list. Fine.

One more: the spec says the collapsed list is "Lines removed as headers, footers and footnotes" — my summary text matches, with counts. The preamble lines are "before paragraph 1" — included in the list; summary mentions them. Slight extension but transparent. OK.

Let me also double check: "A tick box 'Show differences first' moves marked rows to the top." — my sort moves 'differs' rows to top. Should 'no reference' rows also move? "marked rows" — the mark is "Differs". I'll move only differs. Hmm... but one could argue no-reference rows are also "marked". The label says "differences" — differs only. Keep.

Now write everything out. Also ensure no external resources. No Chart.js needed (no charts required — counters and table; spec doesn't ask for charts). Fine — Chart.js optional.

Line count: well under 700.

Let me write the final code carefully, making sure JS is correct.

One more detail: in pass 2, `byPage` — Map keyed by page number. records sorted by page. kept lines in order. byPage preserves insertion order per page. ✓.

Also in pass 2, when lastSep exists, I start k at lastSep+1 — but I should also consider F-lines before lastSep? No — footnotes come after the separator. But what if the separator is at the TOP of the page (some docs have a header rule)? Then lastSep is early, and F-lines after it include body F-lines... the startAfter guard still applies. OK.

Hmm, actually one flaw: if the page has a separator at top (header rule) and footnotes at bottom without their own separator, lastSep = top rule, scan from there — first F-line might be a body line mid-page with a paraStart after → guard skips it → next F-line... eventually the real footnote. OK good.

Another flaw: if multiple separators (one at top, one before footnotes), lastSep = the one before footnotes ✓.

Now, pass 3: footIdx lines — I push to removed with reason footnote/continuation. But note: sep lines inside footIdx — they were already pushed to removed in pass 0 and have sep flag; in pass 3, `if(footIdx.has(i))` comes first — a sep line in footIdx would be pushed AGAIN as footnote continuation (since isFootLine false → 'footnote · continuation line'). Duplicate! Fix: check `if(L.sep) return;` BEFORE footIdx check? But sep lines are already in removed; skip them entirely in pass 3. Order: `if(L.sep) return; if(footIdx.has(i)){...}`. But wait — could a sep line be in footIdx? Yes if foot region includes it. So check sep first. ✓.

Also in pass 3, non-foot, non-sep, non-start lines before first paragraph → preamble → removed. ✓.

Let me also make sure `startNum` map: pass 1 sets startNum.set(i, expected) then expected++. ✓.

Now, rendering firstLine: p.lines may contain raw lines with leading whitespace; find first non-empty, trim, truncate 90. ✓.

CSV text: p.text = lines joined '\n' — raw lines may have leading spaces; fine, quoted.

Hmm — should CSV text include the paragraph number prefix "N."? Spec: "The CSV holds number, page, whether it matches the reference, and the full text" — number is separate column; text = full paragraph text. I'll keep text without the bare number line (number is in its own column). If the number line had inline text, that text is included as first line. Good.

Now — write the final answer. Before the code block: 2-3 short sentences. E.g.: "I built the paragraph-checking tool for E/C.12/GC/27: it joins the 20 raw PDF pages, splits them into numbered paragraphs, removes header/footer/footnote lines, and checks each paragraph's opening words against the reference file. Below is the complete app — open it and click any row to see the full extracted text beside the reference's first words."

Then the html block. Nothing after.

Let me now write the complete file mentally checking syntax.

Also: `e.target.closest('a')` guard for link clicks:
```js
tbody.addEventListener('click',function(e){
  if(e.target.closest('a'))return;
  var tr=e.target.closest('tr.data');
  ...
});
```

Also keyboard accessibility: make rows focusable? Add tabindex="0" and keydown Enter? Nice-to-have; add role="button"? Keep simple but add tabindex and Enter/Space handling — small addition. I'll add tabindex="0" on data rows and handle keydown. Eh — keep it minimal but accessible-ish: I'll add it.

Actually keep code lean; add tabindex + keydown Enter toggle. Fine.

Let me finalize CSS details and write it.

One more check — "Works on a laptop screen without horizontal scrolling": .wrap max-width 1100, table width 100%, .tablewrap overflow-x auto as fallback. The fulltext pre-wrap wraps. OK.

Also the h1 with link — title from data could contain "&" etc — esc() it. ✓.

Also `document.getElementById('hSym')` — set href and text. If doc_url empty, href '#'. Fine.

Write out now. Also double-check: no fetch, no external loads ✓. Chart.js not needed.

Counting lines — fine.

One more thought on counter 2 label: "footnote lines removed / footnotes in the reference" — spec: "footnotes removed / footnotes in the reference". I'll label "footnotes removed / footnotes in the reference". Big: `${footnotes.length} of ${refF}`.

Counter 1 label: "paragraphs found / paragraphs in the reference". Big: `${found} of ${refP}` → reads "N of 90" ✓.

Final check of the note under counters — must contain the exact sentence. ✓.

Also the "How this is computed" near the table ✓ and near counters ✓ (the note serves both; I'll also keep the table note).

Now produce final output.