Let me plan the app carefully.

Data: `WORKSHOP_DATA.pdf_text` with `title`, `symbol`, `doc_url`, `source`, `count`, `records` (page, text), `reference` {paragraphs, footnotes, adopted, first_words}.

Tasks:
1. Join pages in order (records sorted by page presumably already in order).
2. Remove lines that are only a page number, only the document symbol, or distribution code ("GE." + digits).
3. Footnote lines: a small number then text, at the foot of a page — removed and counted. Need heuristics: a line matching /^\d+\s/ or /^\d+/ at the bottom of a page... Footnote lines in PDF text typically look like "1 See ..." — a number followed by text. But paragraph starts are lines that begin with "N." (number + period). Footnotes might be "1 General Assembly resolution..." So: a line that starts with a small number (not followed by a period? or followed by anything) located at the foot of the page (last few lines of a page), and not a paragraph start. Hmm. Footnote numbers can repeat 1-30ish. Heuristic: within the last portion of a page, lines matching /^\d{1,2}\b/ that aren't the expected paragraph number followed by ".". Also superscript footnotes may have been converted oddly.

Let me think about typical CESCR GC PDF text. Footnotes at page foot like:
"1 See General Assembly resolution 76/300."
"2 E/2023/..."

The page foot might contain several footnote lines. The challenge: footnote lines might wrap — a footnote continuation line would be text without a number. The plan says "Footnote lines (a small number then text, at the foot of a page) are removed from the paragraphs and only counted." So only lines that start with a small number. Continuation lines would remain — but they'd end up appended to... hmm, they'd be part of the preceding paragraph or before the next paragraph start. That could pollute paragraph text. But the plan says what it says; keep it simple but try to be sensible.

Better approach: process page by page. For each page, split into lines. Determine which lines are header/footer/footnotes:
- header: lines matching document symbol exactly (E/C.12/GC/27), page number only (digits), "GE.25-xxxxx" distribution code.
- Also typical headers "United Nations", "Economic and Social Council"? The plan only says: only a page number, only the document symbol, or distribution code ("GE." followed by digits). Keep to that.

Footnotes: at the foot of a page. How to find "the foot"? Approach: scan lines from the bottom of the page upward; while a line matches a footnote pattern, mark it as footnote. Footnote pattern: /^\d{1,2}[\s.]/ followed by non-empty text, OR the line could be just... Hmm. Also continuation lines. Let me do: from the bottom, collect lines that are footnote starts (small number + text) or footnote continuations (non-empty text lines that come after a footnote start and before the next footnote start or page end). Stop when hitting an empty line followed by a non-footnote... This gets complex.

Simpler robust approach: The last line of a page might be a footnote. Footnote numbers per page are typically 1..k (small, ≤ maybe 40). Scan from bottom: a line is a footnote start if it matches /^(\d{1,2})\s+\S/ (number, space, text). Also match a possible "________" separator? Not mentioned.

Algorithm per page:
- lines = text.split('\n')
- Remove empty trailing lines tracking.
- i = lines.length - 1
- while i >= 0:
  - line = lines[i].trim()
  - if line is empty: break? No — footnotes may be separated from body by blank line but footnote lines themselves consecutive. Actually if we hit a blank line after processing footnote candidates, we can stop scanning (body could also end with numbers though — paragraph number alone on a line "5." at the bottom? possible!). Hmm, paragraph number stands alone on a line like "5." then paragraph text follows on next lines. If a page ends with "...text\n\n5.\n" — the "5." at the bottom is a paragraph start whose text continues on the next page! That's likely common in this document. So I must not treat a bare "5." line as a footnote.

Footnote start pattern: /^(\d{1,2})[\s]/ with following text on the same line, i.e. number followed by space and then more text (not just a period). E.g. "1 See..." Also could be "1. See..."? In UN docs footnotes usually "1 See". Let me define footnote start as: matches /^\d{1,2}\s+\S/ and NOT matching expected paragraph start pattern (^\d+\.$ or ^\d+\.\s). Also the number should be small (≤ 60, footnotes in GC27 — reference says how many footnotes total; unknown, maybe ~30).

Continuation: after identifying footnote starts from bottom, lines between consecutive footnote starts (upwards) that are non-empty text are also footnotes (wrapped continuation). But risky. Alternative: mark footnote start lines from the bottom, and also any line after (below) a footnote start until the next footnote start or a blank line or a paragraph-like line. Since we go bottom-up: once we've seen a footnote start, subsequent lines above it are continuation until we hit another footnote start or a blank line or a paragraph-like line.

Wait — going bottom-up: line at index j is footnote-start if /^\d{1,2}\s+\S/. Above it, continuation lines until blank line or another footnote start. Once we hit a blank line or a line that looks like body text with a blank line separation, stop.

Actually many PDF extractions don't have blank lines between footnotes and body. Hmm. Let me just do: scan from bottom; maintain state "inFootnotes". For each line from bottom up:
- trimmed empty → if inFootnotes, continue as removed? Blank lines we drop anyway or keep? Blank lines don't matter for paragraph text (we join lines). Let's keep blank lines but they don't affect. Actually for the footnote detection, treat blank as neutral: if inFootnotes already true, blank doesn't stop it necessarily... risky.

Simpler: stop the bottom scan when we hit a blank line AND we've collected at least one footnote, or when line doesn't match footnote/continuation patterns. Let me define:

```
function classifyPage(lines, removed) {
  // bottom-up footnote detection
  let i = lines.length - 1;
  // skip trailing empties
  while (i >= 0 && lines[i].trim() === '') i--;
  let inFn = false;
  const fnLines = [];
  while (i >= 0) {
    const t = lines[i].trim();
    if (t === '') { if (inFn) { fnLines.push({i, type:'blank'}); i--; continue; } else break; }
    const isFnStart = /^\d{1,2}\s+\S/.test(t) && !/^\d+\.\s*$/.test(t);
    if (isFnStart) { inFn = true; fnLines.push({i, type:'fn'}); i--; continue; }
    if (inFn) {
      // continuation if it's text and not a paragraph start and not too structured
      if (/^\d+\.$/.test(t) || /^(I|II|III|IV|V|VI|VII|VIII|IX|X)\./.test(t) ... hmm
```

This is getting complicated. Blank line handling: if inFn and we hit a blank line, footnotes are often contiguous without blanks between them but separated from body by a blank? In pdftotext output, usually no blank lines at all. Ugh.

Given I can't see the real data, I'll write a reasonable heuristic and the app itself shows the removed lines so the reader can verify. Also the counters compare with reference footnote count, so the reader can see if the count is off.

Let me settle on:

For each page (in order):
1. Split into lines (handle \r).
2. Filter out header/footer lines: trimmed matches:
   - /^\d{1,3}$/ (page number only) — but careful: a lone paragraph number line is "5." with a period, so /^\d+$/ without period is safe.
   - trimmed === symbol (exact) — the doc symbol E/C.12/GC/27.
   - /^GE\.\s*\d/i — "GE." followed by digits, maybe "GE.25-12345".
   - Maybe also lines like "United Nations", "Economic and Social Council"? Not per plan. Keep to plan.
   These are counted as "headers/footers" for the removed list.
3. Footnote detection from the bottom: iterate from last line upward. Track whether we're in the footnote zone. A line starts a footnote if it matches /^(\d{1,2})\s+/ and has more text after, and it is not a paragraph-number-only line. Once in footnote zone, non-empty lines that don't look like paragraph starts ("N." alone, or "N. text"?) — hmm, paragraph text lines could be caught as continuation. 

Danger: if the footnote zone scan runs too far up, we'd eat body text. Mitigation: stop when we hit a blank line, or when the line matches a paragraph-start pattern (/^\d+\./), or when line doesn't match footnote-start AND we're in zone but the line... continuation lines are allowed. Blank-line stop is the main guard. Also stop if line matches /^[A-Z]/+ section heading pattern like "I. Introduction"? Those are Roman numeral headings.

Actually also footnote-start pattern with number ≤ 99 but paragraph numbers go up to 90 and look like "90." (with period, alone on line). A footnote "2 E/2023/..." — number, space, text. A paragraph line like "2. The Committee..." starts "2." — with period. So requiring space after number (not period) distinguishes them mostly. But a footnote could be "2. See..."? Unlikely in UN style; footnotes are "2 See ...".

Also footnote might start with a number followed directly by non-space? Like superscript converted: "1See"? Possible. I'll allow /^\d{1,2}[^\d.]/ maybe. Keep it: /^\d{1,2}\s+\S/.

Additional guard: paragraph numbers "stand alone on their line" per the plan, e.g. "1.\nA clean, healthy...". So paragraph starts detected globally: a line that (after trimming) equals "N." where N is the next expected number. The plan says "A paragraph starts at a line that begins with the next expected number and a full stop". So the line begins with "N." — could be "N." alone or "N. text...". I'll handle both: /^N\.(?:\s|$)/.

Now the main split algorithm over the joined cleaned lines (with page tracking):

- expected = 1
- Walk through lines (each with page number attached).
- If line matches new RegExp("^" + expected + "\\.(\\s|$)") after trimming (or after stripping?) → start new paragraph: number = expected, page = current page; text starts with remainder of the line (if any) plus following lines until next paragraph start (expected+1) — also handle headings: Roman numeral section headings like "I. Introduction" should stay inside the preceding paragraph (as part of text) or... They'd fall between paragraphs. The plan says lettered sub-paragraphs stay inside; nothing about headings. Keep them inside the preceding paragraph text (they appear after a paragraph ends and before next number). Actually a heading after paragraph N and before N+1 would be appended to paragraph N's text. Acceptable — we don't edit text.

Hmm, but wait: heading "II." — Roman numeral, won't match ^\d+\. so fine.

- Numbers out of sequence (years, cross-refs like "(see A/75/982)" mid-text — those are inside lines, not line starts) don't start paragraphs because we only look for the expected next number.
- But what if a paragraph number was damaged (e.g., "2 7." or merged)? Then expected never matches and everything gets absorbed into previous paragraph, and count will be low — that's exactly what the tool should reveal (gaps). The table should show... "table numbers run 1,2,3 without gaps" is the success criterion, meaning if the code works, they do. If a number is missed, subsequent paragraphs won't start (since we require the exact next expected number). Hmm — if "27." is damaged, then expected=27 never found, and 28 won't match expected... So everything from 27 onward collapses into paragraph 26. That would give few rows. Alternative: allow skipping? The plan says "A paragraph starts at a line that begins with the next expected number" — strict. But also the numbers "run 1,2,3 without gaps" in success criteria. And "at least 30 rows appear".

Hmm, but maybe better: if we require exact next expected, one damaged number kills the rest. To be safer, maybe allow matching expected OR detecting that a line begins with any number+period where the number > expected? No — years like "2025." could... cross references at line start? Unlikely but "in its general comment No. 25 (2020)" mid-line. A line could start with a year? e.g. wrapping. Risky.

Compromise: primary rule strict expected match. But also, to be resilient: if we haven't found `expected` but find a line starting with `(expected+k).` for k in 1..3? That handles a missing/damaged number by skipping it — creating a gap which the tool should show. Hmm, but the table "numbers run without gaps" criterion suggests no gaps expected. Let me think about what the actual data looks like: 20 pages, 90 paragraphs, footnotes mixed in. The converter damage: hyphenation, broken line joins. Numbers usually intact.

I'll implement: match expected strictly first. Additionally, to avoid total collapse, if a line begins with a number M followed by "." where M > expected and M ≤ expected+5... no wait, that could match years (unlikely "2026." with period at line start... "A/75/982)." no). Actually risk: text like "paragraph 3." wrapping to line start? Meh.

Let me keep it simpler and true to plan: strict expected match. If the result has few rows, the app honestly shows "found N of 90". The reference check makes it verifiable. But the plan's success criteria says at least 30 rows and numbers without gaps — suggesting the data is well-behaved enough. Hmm, but I can't test. Let me add a mild fallback: after the strict scan, if found < some threshold... no, no hidden heuristics.

Actually, let me reconsider: maybe allow the paragraph number to appear at start of line either alone ("5.") or with text ("5. The Committee..."). The sample shows "1.\nA clean, healthy..." — number alone. Also handle possible leading spaces. Also the number might be attached to text without period space issues.

Another damage case: number line merged with footnote or symbol like "E/C.12/GC/27\n5." fine. Or "27" without period (damaged)? The plan says damage exists; the tool flags "Differs" via first words. If a paragraph start is missed entirely, that paragraph's text merges into the previous one and the previous paragraph's first words still match — the count would be 89 not 90 and there'd be a gap in numbers shown (e.g., ...25, 27, 28...). Wait no — with strict expected matching, if "26." is damaged, expected stays 26 forever, so 27 never starts. All subsequent collapse. The table would show 25 rows. Hmm.

Better: strict expected match, but with a resync: if a line starts with M. where M is expected+1 or expected+2 (i.e., a number slightly ahead), treat it as a start too, and mark the missed number(s) as gaps. This prevents collapse and reveals damage as gaps. The plan: "Numbers out of sequence (years, cross-references) do not start a paragraph." Years are 4-digit; cross-refs like "(see A/75/982)" don't start lines with digits+period typically. I'll allow lookahead window of, say, expected+1..expected+3, and only if the number is followed by "." exactly at line start. Years: "2025." starting a line — could happen in "adopted on 6 November 2025." wrapping? A line starting "2025." is conceivable... rare. To reduce risk: require the number ≤ 99? No — paragraph numbers go to 90, fine, but as a general doc... this doc has 90. Require number < 1000? Years excluded then. Paragraph numbers here max 90, so require ≤ 99? If the doc had >99 paragraphs it'd fail, but reference says 90. I'll require M ≤ expected + 3 and M < 100. Hmm, also require the rest of line after "M." to be empty or start appropriately (paragraph number alone, or text). 

Actually also: for strictness vs the plan, gaps: if we resync by skipping, the table will show a gap (e.g., missing 26). Should I show a placeholder row "26 — not found"? That would be helpful and honest: the tool "shows where the converter damaged the text". I'll list missing numbers between found ones as gap rows (or at least mark in counters). Keep simple: in the table, if a number in 1..maxFound is missing, show a row "not found in page text". Hmm, adds complexity but it's valuable. Let me include it simply: after collecting found paragraphs, for each number 1..reference.paragraphs (or up to max found), if missing, add a row flagged "not found". Actually reference.paragraphs=90 tells the range. Use numbers 1..refCount for gap detection.

Wait, but if resync allows jumps only up to +3, and expected number was truly damaged, we resync at expected+1 (which is the next real paragraph). Good. Years: "2025." at a line start with a period — I'll accept the small risk but add condition: number must be ≤ 2 digits. "2025" is 4 digits, excluded. 

Also paragraph numbers could be like "50 (c)"? No — that's sub-paragraphs inside text.

Footnote handling interplay: footnote starts like "3 See..." — number+space, no period — won't match paragraph pattern "M." good. But footnote continuations (wrapped text without number) if not removed, they'd be absorbed into the previous paragraph's text (since they appear after paragraph text before next number... wait, footnotes are at page bottom, so after the last body line of the page, before next page's header). If I remove only footnote-start lines, continuations pollute paragraph text — but "Differs" checks only first 6 words of the paragraph, so pollution at the end doesn't trigger flags. It does affect "full paragraph exactly as extracted" though. My bottom-up zone approach with continuation capture should handle most.

Let me define the footnote zone per page more carefully:

```
process page lines (after header/footer removal? or before?) 
```
Order: remove header/footer lines first (they're at top/bottom). Then detect footnotes from bottom. Then remaining lines go to stream.

Bottom-up:
```
let idx = lines.length - 1;
// skip trailing blanks
while (idx >= 0 && blank(idx)) idx--;
let inZone = false;
while (idx >= 0) {
  const t = trim(lines[idx]);
  if (t === '') {
    if (inZone) { /* blank inside footnotes? stop */ break; }
    break;
  }
  const fnStart = /^\d{1,2}\s+\S/.test(t) || /^\*\s?\d{0,2}/... 
```

Hmm also asterisk footnotes "* ..." — the doc might have one (the title has "*" — "sustainable development*" pointing to a footnote). Keep to digits.

```
  const isFnStart = /^\d{1,2}\s+\S/.test(t);
  const isParaStartLike = /^\d{1,3}\.$/.test(t); // "26." alone
  if (isFnStart) { mark footnote; inZone = true; idx--; continue; }
  if (inZone) {
    // continuation: plain text line
    if (isParaStartLike) break; // safety
    if (/^[IVX]+\.\s/.test(t)) break; // section heading
    mark as footnote continuation; idx--; continue;
  }
  break;
}
```

Blank stop: if blank encountered while inZone → stop (footnotes contiguous). If not inZone → stop. Actually if a footnote-start appears, lines above it up to previous footnote-start or blank are continuations. The blank-stop guards runaway. But what if there are no blank lines and body text follows directly? Then continuation capture would eat body lines! E.g., page bottom:
"...end of paragraph text
2 See E/2010/..."
Above "2 See..." is body text with no blank → we'd mark body line as continuation. Bad!

Guard: continuation lines should look like footnote content... hard to distinguish from body text. Hmm. Alternative: only capture footnote-start lines and lines that follow (below) a footnote start until another footnote start — i.e., continuation belongs to the footnote BELOW it? No — continuation of footnote 2 wraps to a line below "2 See..." (footnotes wrap downward). So going bottom-up: line order on page: [body..., "1 See...", "continuation of fn1...", "2 See...", "continuation..."]. Bottom-up: "continuation" (bottom), then "2 See...", then "continuation of fn1", then "1 See...", then body.

So bottom-up: we see continuation first (no number) — but we don't know it's a continuation until we see "2 See..." above it. So: scan from bottom, collecting candidate lines; when we hit a footnote-start, everything collected since the last footnote-start-or-start becomes continuation (valid). If we hit a blank or paragraph-start-like line before any footnote-start, discard collected candidates (they're body). But if body text directly precedes the first footnote-start (no blank), we'd wrongly include it.

Extra heuristic for continuation: footnote text lines are often shorter or start lowercase / continue sentences. Also footnotes frequently reference "See", symbols "A/...", "E/...", URLs. Honestly, in pdftotext output there usually IS a blank line between body and footnotes? Not reliably.

Pragmatic: limit continuation capture: a continuation candidate must NOT end with a period followed by nothing? No...

Alternative simpler approach the plan literally endorses: "Footnote lines (a small number then text, at the foot of a page) are removed from the paragraphs and only counted." — Only the numbered lines. Continuation lines stay (they'll be absorbed into the preceding paragraph's tail — harmless for first-words comparison, slightly polluting full text, and visible when the row expands). Hmm, but "the reader can verify nothing substantive was discarded" — continuation lines of footnotes remaining in paragraph text is damage visible in expanded text. It's a checking tool; honest display is okay.

But pollution could also end up BETWEEN the last body line of page N and the paragraph number line of page N+1... it stays inside the previous paragraph. Fine.

However! There's a worse case: if a paragraph number line is at the very bottom of a page and footnotes... no, footnotes come after body including that number line. The number line "26." at page bottom: is it "at the foot"? My bottom-up scan: trailing line "26." — not fnStart (has period, no space+text), if inZone... "26." is paraStartLike → break. Good, but only if inZone logic reaches it. If footnotes below it: "...body...\n26.\n1 See...\n..." — bottom-up: "1 See..." fnStart → inZone; then "26." → paraStartLike → break. 

But what if paragraph text continues on next page and the number "26." is followed by footnotes then next page header? Order: body lines, "26." (paragraph starts at page bottom? unlikely but), footnotes, [page break]. Fine per above.

What about a footnote number matching fnStart pattern that's actually... e.g. footnote "12 E/..." fine. What about list items in annex? Not here.

Decision: remove footnote-start lines only (small number + space + text, from bottom of page, stopping at blank/para-number/heading), and ALSO capture continuation lines only between two footnote-starts or below the last footnote-start when the page's remaining tail consists... I'll do this: bottom-up, maintain buffer; rules:

- If line is fnStart: flush buffer as continuations (mark all buffered), mark this line, inZone=true, continue up.
- Else if inZone: 
  - if blank → stop.
  - if paraStartLike (^\d{1,3}\.$) → stop.
  - if roman heading → stop.
  - else buffer it (potential continuation), continue up. But cap buffer? The danger: body text above footnotes without blank separation gets buffered, then when we stop (at blank or whatever) without hitting a fnStart above... wait no — inZone is true means we already saw a fnStart below. Lines above fnStart1 (the topmost footnote) that are body would be buffered, and then if we hit another fnStart above (unlikely) they'd be flushed wrongly, or if we stop at blank, buffered lines are NOT flushed (discarded from removal) → they stay as body. 

So the rule: buffered lines only become "removed" if a fnStart is found above them. If we stop (blank/paraStart/heading/page top) with buffered lines, those buffered lines are returned to body. But wait — that's wrong direction! Continuations are BELOW their fnStart? Let me re-examine: a footnote "2 See E/2010/5, para 5." wraps: line1: "2 See E/2010/5, para", line2: "5." or "para 5." — continuation is below line1. Bottom-up scan encounters line2 (continuation) BEFORE line1 (fnStart). So buffer line2, then hit "2 See..." fnStart → flush buffer as continuation. Correct!

And body text above fnStart1 (topmost footnote): buffered after passing fnStart1... wait no. Bottom-up order: [page top ... body ... fn1line1, fn1cont, fn2line1, fn2cont ... page bottom]. Bottom-up: fn2cont (buffer), fn2line1 (fnStart → flush fn2cont, mark), fn1cont (buffer), fn1line1 (fnStart → flush, mark), bodyline (inZone, buffer), more body (buffer)... until blank or paraStart-like or page top → stop, discard buffer. Body preserved unless a fnStart appears above (would only happen if body contains a line like "5 See..." which... cross references at line start? "see A/75/982" — doesn't start with digits+space. Could a body line start "16 November 2025"? A date at line start! "6 November 2025" — starts with "6 " + text → matches fnStart pattern! Hmm! If a wrapped line starts with a date fragment... e.g. "...adopted on 6\nNovember 2025..." — line "6 November 2025" would match /^\d{1,2}\s+\S/. Risk exists but requires the date to be in the footnote-zone scan region (bottom of page) — the scan stops at first blank/paraStart. If the last paragraph on the page has no blank lines (likely) and contains a wrapped date at the right place... Possible but rare. Also "1 January 2000" style dates appear in footnotes a lot (good) and body (risk).

Mitigation: fnStart number should be ≤ some max? Both cases small numbers. Check following word: if it's a month name or "November"? Footnotes rarely... hmm, "2 November 1998" could be a footnote date too. I'll add: fnStart excludes lines where the text after the number starts with a month name (January|February|...|December). That kills the date risk mostly. Nice touch.

Also blank lines: I need to decide whether blank lines are preserved in the stream. For paragraph text joining, I'll join lines with a space (or newline). Keep newlines in stored text? Display "exactly as extracted" — I'll join with "\n" preserved? The extracted text has \n\n between blocks. For first-words comparison I normalize whitespace. For display, show with original line breaks (white-space: pre-wrap). I'll store paragraph text as the lines joined with "\n" (keeping internal blanks? drop leading/trailing blanks). Actually to display "exactly as extracted", keep the lines as they are, joined by \n, but trim leading/trailing empty lines. Blank lines within? Between paragraph number and text there might be blank lines — trim leading. Internal blank lines (between paragraphs sections) — since text runs until next start, trailing blanks should be trimmed too.

Paragraph text construction: when a start line is "26." alone, text = subsequent lines until next start. When start line is "26. Some text", text begins with "Some text". Also handle possible damage where number and text merged weirdly like "26.The Committee" (no space): my regex /^(\d+)\.(?:\s+(\S.*))?$/ — if "26.The" then remainder "The"? /^(\d{1,3})\.(.*)$/ and remainder trimmed starts "The Committee". Let me use: match m = t.match(new RegExp(`^(${expected})(?:\\.)(.*)$`)) — wait must anchor number exactly: line begins with expected number then ".". Use regex `^N\.` on trimmed line; remainder = line.slice(match length). If remainder non-empty after trim, it's first text line.

But careful: expected=1 and line "1." vs a line "10." — `^1\.` doesn't match "10." since after "1" comes "0" not ".". Good. But expected=1 matching "1." — also cross-ref "(see paragraph 1." at line start? Starts with "(" — no. Good.

Resync: if line matches /^(\d{1,2})\.(?:\s|$)/ with number n where expected < n ≤ expected+3 → treat as start of paragraph n, note gap. Also strictly the "next expected" match takes priority; since expected is the smallest, check expected first: does line match `^expected\.`? If yes → start. Else check lookahead numbers.

Wait, one more: the number might be at line start but preceded by spaces — trim first. Also page headers removed before joining.

Also footnote zone removal happens per page BEFORE the paragraph scan (on the joined cleaned stream). Yes.

Roman numeral headings: "I." alone or "I. Introduction" — they don't match digit patterns, so they just become part of preceding paragraph text (trailing). Acceptable. Actually they'd be appended to previous paragraph's text (trailing). Trim? "exactly as extracted" — keep. Hmm, it might look odd but honest. Alternatively, could detect headings and keep them as separate "lines removed"? No — they're substantive structure; keep in text. Fine.

Counters:
- paragraphs found: found.length; "of reference.paragraphs".
- footnotes removed: fnCount; of reference.footnotes.
- differing: count of paragraphs where first words differ (excluding those with no reference entry? "no reference" shown instead of "Differs"). The counter "paragraphs whose opening words differ from the reference" — count only those with a reference entry that differ. Maybe also show no-reference count separately? Keep simple: counter counts differs only.

Word comparison: first six words, normalize: lowercase, strip punctuation (apostrophes? "State party's" — remove non-alphanumeric except maybe keep letters/digits). Reference first_words gives first six words of each numbered paragraph. Compare word arrays of length 6. Extract words: text.split on whitespace after replacing punctuation: `text.toLowerCase().replace(/[“”"'’()\[\]{}.,;:!?–—-]/g,' ')`? Hyphen: "well-being" — reference might hyphenate differently. Ignoring punctuation incl. hyphens: "well-being" → "well being" (two words) vs "wellbeing" (one)? Hmm, replacing hyphen with space changes word count. Risky either way. UN docs hyphenate consistently. I'll replace punctuation with '' (empty) except... apostrophes: "Committee's" → "committees" both sides equally. Em dash with spaces around → "— " becomes '' gluing words?! "environment — as" → "environmentas"?? No: replace [—–] with space. Let me: normalize = s.toLowerCase().replace(/[’']/g,'').replace(/[^a-z0-9]+/g,' ').trim().split(/\s+/). This turns hyphens into spaces ("well-being" → "well","being") — consistent on both sides since both texts derive from the same doc? Reference first_words presumably from clean text; extracted from PDF which may hyphenate across line breaks ("environ-\nment")! That's exactly the damage to detect — good, it should flag "Differs". But also non-damage hyphenation wrapping could cause false differs... which is precisely "converter damage" the tool flags. OK.

Take first 6 words of extracted paragraph text (after the number; note text lines joined — a hyphen at line end stays "environ-\nment" → normalized "environ" "ment" → differs. Good, that's damage detection.)

Compare with reference words (normalize same way, take 6). If reference missing → "no reference" mark.

Table row: number, page, first line (~90 chars) of text, symbol linked, "Differs" badge or "no reference" or maybe nothing/✓? Show "OK"? The plan: a "Differs" mark where mismatch. I'll show a small badge: "Differs" (red-ish), "no reference" (grey). Otherwise maybe subtle "matches" check — not required; keep column showing "Matches" lightly? Keep simple: show badge only when differs/no reference; column header "Check".

Checkbox "Show differences first": sort rows so marked (differs + no reference + not found) first, stable within.

Row click → expand full text below: paragraph text in a pre-wrap block ("exactly as extracted"), plus reference's first words beside it. Also for gap rows, expansion shows explanation.

Download CSV: columns: number, page, matches_reference (yes/no/no reference/not found), text (quoted). Build with proper CSV escaping (double quotes doubled). Blob download via URL.createObjectURL and anchor click. Filename: symbol + "-paragraphs.csv" with slashes replaced.

Removed lines list: collapsed `<details>`: "Lines removed as headers, footers and footnotes (N)". Group: headers/footers with page, footnotes with page. Show each line verbatim.

Layout/design: title, symbol link, one-line "raw PDF text, N pages, source: …". Counters as three stat cards. Note under them. Table. Notes "How this is computed" near counters and table.

Chart? Not needed. Keep no Chart.js (fine, it's optional — "Use it for charts" — no charts needed here).

Fonts: system stack, accent #1f6fb2, light bg #f6f8fa, base 16px.

Handle empty data: if no WORKSHOP_DATA.pdf_text or empty records, show message.

Now, page association: each line keeps its source page for "page where paragraph starts" and for removed lines listing. records may not be sorted; sort by page.

Edge: symbol appears in header lines like "E/C.12/GC/27" exact trimmed match. Also maybe with page number combined? Keep exact match plus maybe /^E\/C\.12\/GC\/27\s*$/ using the actual symbol from data (escape regex). Also distribution code: /^GE\.\s?\d+/ — plan says "GE." followed by digits. Also possibly "GE.25-00664(E)?" — allow /^GE\.\d.*/. Case sensitive probably.

Page-number-only lines: /^\d{1,3}$/ — but footnote continuation could be a bare number? Unlikely. Also a paragraph number alone is "N." with period — safe. But what about the digit-only line being a wrapped year "2025" alone? 4 digits — my regex {1,3} excludes 2025. Page numbers up to 20 here. Use /^\d{1,3}$/.

Hmm wait — also lines like "V. Conclusions" roman — keep.

Footnote numbering: could footnotes exceed 2 digits? reference.footnotes unknown count; GC27 with ~30 footnotes → 1-2 digits. Allow {1,2}. If reference has more, count mismatch shows. Fine.

Also, what about the footnote marker in the title "sustainable development*" — asterisk footnote at bottom of page 1: "* ..." line. My pattern won't catch; it'll be absorbed... it's at page 1 bottom → bottom-up scan: line "* The present general comment..." doesn't match fnStart → stop immediately (not inZone). Stays in stream → gets appended to... it's before paragraph 1? Page 1 has title, then "I.\n\nIntroduction\n\n1.\nA clean..." — the asterisk footnote is at page bottom, after paragraph 1 text probably. It'd be appended to paragraph 1's tail. Slightly dirty but visible and honest. Could add pattern /^\*/ for footnote too — "A small number then text" per plan... asterisk isn't a number. I could extend fnStart to /^(\*|\d{1,2})\s+\S/ or /^\*\s*\S/. I'll include asterisk-start lines in footnote zone detection too (harmless, more accurate). Hmm, plan says "a small number then text" — I'll include asterisk as a bonus; it's still a footnote marker. Fine, and count it as footnote removed. I'll note it in removed list.

Actually wait, danger: bullet "*" lines in body? Unlikely in this doc.

Now "at least 30 rows" and "N of 90" — fine.

Let me also handle: paragraph start line might have the number with no period due to damage — can't handle everything; strict per plan.

Section headings between paragraphs — appended to previous paragraph text. Hmm, actually that bugs me for "full paragraph exactly as extracted" — including a trailing "II." heading. But rules say never edit text. Alternatively, headings could be kept in the stream and simply end up wherever. It's a checking tool; okay.

Wait, actually — could a heading line like "II. Introduction" appear BEFORE paragraph 1 (after title)? Page 1: title lines, "I.\nIntroduction" hmm the sample shows "I.\n\nIntroduction\n\n1.\nA clean...". So "I." and "Introduction" lines precede "1." — they'd be in the stream before the first paragraph start. My scan: lines before first start are "preamble" — dropped? They're substantive-ish (title/heading). I'll collect them as... the removed-lines list is only headers/footers/footnotes. Preamble text before paragraph 1: show it in the removed list? No — "so the reader can see nothing substantive was discarded". Dropping the title/heading silently would discard substantive lines! Options: include preamble in a small "text before paragraph 1" note, or attach to... I'll display any pre-paragraph-1 leftover lines in the removed-lines details under a "other lines not in any paragraph" group — with a note. Also lines after the last paragraph (if any). Actually trailing lines after last paragraph end (e.g., nothing much). I'll show leftover-before and leftover-after groups in the details, clearly labeled as "shown, not discarded — review". Good honesty.

Hmm wait, careful: leftover after last paragraph could include the final footnotes already removed... no, those removed. Fine.

Let me now also double check the "expected" scan with page-joined stream. Implementation:

```
const stream = []; // {page, text}
pages.forEach(page records sorted) {
  let lines = rec.text.split(/\r?\n/);
  // classify
}
```

Classification per page:
1. For each line index, trimmed t:
   - isHeaderFooter: t === symbol || /^GE\.\s*\d/.test(t) || /^\d{1,3}$/.test(t)
   - Wait: page number could be like "2" or maybe " 2 ". trim handles.
   Hmm — GE. lines: "GE.25-00664" or "GE.25-00664(E)*"? /^GE\.\d/ ok.
2. Footnote zone: work on the array with header/footer already removed? The zone is at page bottom; footers (page number, GE code) are below footnotes. Remove them first (they're classified anywhere in the line list — actually restrict? A bare number line could theoretically be inside body... a wrapped line that is just a number? Extremely unlikely. Keep global removal for symbol and GE; for bare page numbers, restrict to first 3 and last 3 lines of the page to be safe? Plan says "Remove lines that are only a page number" — I'll restrict to top/bottom 4 lines to avoid eating a stray body number. Actually simpler: global. Risk minimal. Hmm, a date wrap "2025" alone as a line — 4 digits, excluded by {1,3}. A wrapped "16" alone? Like "...resolution 79/\n172." → "172." has period. "16\nNovember" → "16" bare! Possible mid-body. I'll restrict page-number removal to the first 4 and last 4 lines of the page. Good compromise.

3. Bottom-up footnote scan as designed.

Build removed list entries {page, text, kind: 'header/footer'|'footnote'|'continuation'}. Count footnotes = fnStart lines count (asterisk included).

Then stream = remaining lines (page attached). Blank lines kept in stream? For paragraph text, I'll join with "\n" and later trim blank edges. Keep blanks internal.

Paragraph scan:
```
let expected = 1;
const paras = []; // {num, page, lines: []}
const leftovers = [];
let current = null; // {num, page, lines}
for (line of stream) {
  const t = line.text.trim();
  let startNum = null;
  const m = t.match(/^(\d{1,3})\.(?:\s|$)/) || t.match(/^(\d{1,3})\.$/);
```
Wait combine: /^(\d{1,3})\.(.*)$/ then check the char after period is space or end. Let me: m = t.match(/^(\d{1,3})\.(?:\s+(.*))?$/) — matches "26." or "26. text..." but not "26.text" (damaged no-space). Also handle "26.text": /^(\d{1,3})\.(\S.*)$/ separately → treat remainder as text. Let me just do m = t.match(/^(\d{1,3})\.(.*)$/) and then num=+m[1], rest=m[2].trim()... but "26.5" would match as num 26 rest "5"! Cross-refs like "A/HRC/26/4" start with letter. "79/172." no. Decimal numbers at line start? Rare in this doc. But "26.4"? To be safe require rest === '' or rest starts with space? Damage case "26.The" — I'd like to catch. Compromise: accept if rest==='' or /^[\s(]/... no, "26.The" has no space. Ugh. Decide: accept rest === '' OR rest starts with space OR (rest starts with uppercase letter AND current scanning expects it)? Over-engineering. 

The plan says: "A paragraph starts at a line that begins with the next expected number and a full stop ('1.', then '2.' …); in this text the number usually stands alone on its line". So primary: number alone OR number+space+text. I'll match /^(\d{1,3})\.(?:\s|$)/ for starts. "26.The" won't start a paragraph → collapses → count drops → visible as gap/low count. It's a checking tool; fine. Also allow the "no space" variant? If I allow "26.The", then "26.5" (decimal) risk... In GC text, decimals at line start essentially never. Cross-reference "paragraph 26." starts with letters. I'll allow rest beginning with a letter as well: pattern: t === num+'.' or /^num\.\s/ or /^num\.[A-Z]/. Hmm "2025." (year+period at line start): 4 digits → excluded by {1,3}. "79/172." starts with "79/"? "79/172." — match ^(\d{1,3})\.(...) requires period right after digits — "79/172." has "/" after 79 → no match. OK. I'll include the no-space-letter variant.

Start determination:
```
function lineStart(t, n) {
  if (t === n + '.') return {rest:''};
  let m = t.match(new RegExp('^' + n + '\\.\\s+(.*)$')) ;
  if (m) return {rest: m[1]};
  m = t.match(new RegExp('^' + n + '\\.([A-Z].*)$'));
  if (m) return {rest: m[1]};
  return null;
}
```
In the loop:
```
let sn = null, rest='';
if (t !== '') {
  const direct = lineStart(t, expected);
  if (direct) { sn = expected; rest = direct.rest; }
  else {
    for (let k = 1; k <= 3 && sn === null; k++) {
      const look = lineStart(t, expected + k);
      if (look) { sn = expected + k; rest = look.rest; }
    }
  }
}
if (sn !== null) {
  current = {num: sn, page: line.page, lines: rest ? [rest] : []};
  paras.push(current);
  expected = sn + 1;
} else if (current) current.lines.push(line.text); // keep original (untrimmed? trimmed?) 
else leftoversBefore.push(line);
```
Keep original line text but I'll push trimmed? "exactly as extracted" — keep raw line text. But leading spaces from PDF... keep raw; display pre-wrap. Hmm, raw lines might have weird spacing; fine.

Wait — lookahead resync: if "26." damaged, we find "27." with expected=26, k=1 → sn=27, gap at 26. Then expected=28. Good. But danger: a line "2. " appearing when expected=5 (out-of-sequence cross-ref at line start, e.g. a wrapped line starting "2. The Committee reiterates..." from a quotation?). Lookahead only goes UP (expected+k), never down. Good — "Numbers out of sequence do not start a paragraph" — smaller numbers never match since expected only increases. But wait: what if the document restarts numbering or... no, 1..90.

Another subtle: expected could match a footnote-like line? Footnotes removed already.

What if paragraph number lines get merged with previous line (e.g., "...rights. 27.\n")? Then "27." isn't at line start → missed → gap via resync to 28. The tool shows gap. 

After scan: paragraphs with text = lines joined '\n', trimmed of blank edges. Also compute firstLine for display: first non-empty line, ~90 chars.

Gap rows: for num in 1..(paras.length? no — 1..maxNum where maxNum = max found or reference count). Let refCount = reference.paragraphs. Range = 1..Math.max(maxFound, refCount)? If code finds MORE than reference (over-splitting), show those too. Use range 1..max(maxFound, refCount). Rows: found or "not found".

Differs check: refWords = reference.first_words[String(num)]; if !refWords → status 'no reference'. Else compare first 6 normalized words of extracted text vs normalized refWords... wait refWords IS the first six words. normalize both, take 6 from extracted, compare arrays equal.

Counter 3: count of status==='differs' (among found). Maybe also count no-reference? Plan: "paragraphs whose opening words differ from the reference" — differs only.

Table columns: № | Page | First line | Check | Symbol(link). Expandable row beneath: full text (pre-wrap, monospace? maybe body font pre-wrap) + reference first words + comparison note.

Sorting with checkbox: default order by number. Checked: rows with status !== 'match' first (differs, no reference, not found), then rest, stable by number. I'll re-render on toggle.

CSV: header: paragraph,page,check,first_words_reference,text. Rows for found paragraphs (and gaps? "as many rows as the table" — include gap rows with text empty). Include all table rows so CSV row count matches. check values: "differs"/"matches"/"no reference"/"not found". Escape quotes.

Removed lines details: group by kind. Show page numbers.

Also "How this is computed" notes near counters and table, and near removed list.

Leftover lines: show in details under "Lines before the first paragraph" / "after the last" — labeled clearly as review items.

Now write the HTML. Keep under ~700 lines. No external resources. Vanilla JS. Include Chart.js? Not needed; skip (allowed — only use it if charts needed).

Design: 
- header with title (doc title from data), symbol linked, line "raw PDF text, N pages, source: …" (source field).
- counters: three cards with big numbers "N of 90" style.
- controls row: checkbox + download button.
- table.
- details removed lines.
- footer note.

Accent #1f6fb2. Light background #f5f7f9. Cards white with border. Badges: differs → #b3261e bg light; no reference → grey; matches → maybe green subtle "✓ matches"? I'll show a subtle "matches" badge in green to make table scannable; plan only requires Differs mark but showing matches is fine. Actually keep the Check column mostly showing "Differs" or "no reference" or empty-ish check "—"? A green check helps projector readability. I'll show "✓" with title. Hmm, keep textual: "matches" in green, "Differs" in red, "no reference" grey, "not found" red outline.

Row expansion: click row toggles a full-width row below (colspan). Render dynamically.

Reference first words beside full text: two-column layout in the expanded panel: left "As extracted" full text; right "Reference first words" + normalized comparison list maybe. Show the reference string verbatim.

Progressive details: for "not found" rows: expanded shows "No line starting 'N.' was found in the page text."

Line count concerns: fine.

Edge: reference.first_words keys are strings of numbers. reference.paragraphs = 90.

Let me also compute and show "pages: N" from records length (or count field).

CSV BOM for spreadsheet Excel? Add "\uFEFF" for Excel friendliness. Yes.

Download: create blob, a.download = "E_C_12_GC_27-paragraph-check.csv" derived from symbol replacing non-alnum with '_'.

Now normalize function:
```
function words(s){ return s.toLowerCase().replace(/[’‘]/g,"'").replace(/[^a-z0-9]+/g,' ').trim().split(/\s+/).filter(Boolean); }
```
Take slice(0,6).

For extracted text, use the paragraph's text (which starts with the first text line, number excluded). If number line was "1." alone, text starts "A clean, healthy...". Good.

Note: text joined includes internal blank lines and heading lines (e.g., "II." heading appended to previous para). First words unaffected (headings come after). But heading BEFORE para 1 — in leftovers.

Display first line: first non-blank line of text, truncated ~90 chars with ellipsis.

Also table needs symbol linked to doc_url in new tab — every row. "Every row that shows a document has its symbol" — yes include symbol cell with link.

Let me write the code.

Structure:

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Paragraph check — E/C.12/GC/27</title>
<style> ... </style>
</head>
<body>
<header>...</header>
<main>
  <section id="counters">...</section>
  <section id="controls">...</section>
  <section id="table">...</section>
  <details id="removed">...</details>
</main>
<script> ... </script>
</body>
</html>
```

CSS: base font 16px; system stack; accent #1f6fb2.

JS outline:

```js
(function(){
const D = window.WORKSHOP_DATA && window.WORKSHOP_DATA.pdf_text;
if (!D || !D.records || !D.records.length) { show message; return; }
const symbol = D.symbol || '';
const docUrl = D.doc_url || '';
const pages = D.records.slice().sort((a,b)=>a.page-b.page);
const ref = D.reference || {};
const refParas = ref.paragraphs;
const refNotes = ref.footnotes;
const refWords = ref.first_words || {};

function esc(s){...}

// classification
const stream = [];
const removed = []; // {page, text, kind}
let footnoteCount = 0;
const MONTHS = /^(January|February|March|April|May|June|July|August|September|October|November|December)\b/i;

pages.forEach(rec => {
  const lines = String(rec.text||'').split(/\r?\n/);
  const n = lines.length;
  const keep = new Array(n).fill(true);
  const isHF = i => {
    const t = lines[i].trim();
    if (!t) return false;
    if (symbol && t === symbol) return true;
    if (/^GE\.\s*\d/.test(t)) return true;
    if (/^\d{1,3}$/.test(t) && (i < 4 || i >= n-4)) return true;
    return false;
  };
  // pass 1: header/footer
  for (let i=0;i<n;i++) if (isHF(i)) { keep[i]=false; removed.push({page:rec.page, text:lines[i].trim(), kind:'header'}); }
  // pass 2: footnotes bottom-up
  let idx = n-1;
  while (idx>=0 && !keep[idx]) idx--; // skip removed trailing (footers)
  // also skip blanks
  while (idx>=0 && lines[idx].trim()==='') idx--;
  let inZone=false, buffer=[];
  const flushBuffer = () => { buffer.forEach(b=>{keep[b.i]=false; removed.push({page:rec.page, text:lines[b.i].trim(), kind:'footnote-continuation'});}); buffer=[]; };
  while (idx>=0) {
    const t = lines[idx].trim();
    if (t==='') break;
    const fnStart = (/^(\d{1,2}|\*)\s+\S/.test(t) && !/^\d{1,3}\./.test(t) && !MONTHS.test(t.replace(/^(\d{1,2}|\*)\s+/,'')));
```

Hmm wait: "1 See..." — t.replace(/^(\d{1,2}|\*)\s+/,'') = "See ..." → not month → fnStart true. Date "6 November 2025" → "November..." → month → false. Good. But footnote "2 November 1998 (date of adoption)"? Would be missed — acceptable, shows in paragraph text. Hmm, footnotes citing adoption dates... risk. Eh, keep it; the removed-list and diff counters let the reader see.

Wait also: /^\d{1,3}\./ excludes paragraph-like "26. text" from fnStart. But a footnote "3. See..."? UN footnotes don't use periods typically. OK.

Also fnStart shouldn't match when the line is a paragraph start for expected... paragraph starts are "N." alone or "N. text" (period) — excluded by the [^.] condition... my check !/^\d{1,3}\./ covers "N. anything". But what about paragraph start "N text" without period (damaged)? Then it might look like a footnote and get removed — damage visible via gap. Acceptable.

```
    if (fnStart) {
      flushBuffer();
      keep[idx]=false; removed.push({page:rec.page, text:t, kind:'footnote'});
      footnoteCount++;
      inZone = true;
      idx--; continue;
    }
    if (inZone) {
      if (/^\d{1,3}\.$/.test(t)) break;          // paragraph number waiting for text? unlikely at foot
      if (/^[IVXLC]+\.\s/.test(t)) break;        // heading
      if (/^[IVXLC]+\.$/.test(t)) break;
      buffer.push({i:idx}); idx--; continue;
    }
    break;
  }
```

Wait, buffer flush logic: buffer lines are ABOVE current, and get flushed when a fnStart found above them. But if we break with buffer non-empty (hit blank/paraStart/heading), buffered lines stay kept (body). But wait — inZone became true only after first fnStart; lines buffered BEFORE any fnStart seen (i.e., below the bottom-most fnStart, like wrapped footnote text at very bottom) — if we then hit fnStart, flush → removed. If we never hit fnStart (page bottom has no footnote-start lines), buffer discarded at break. Correct.

But one flaw: continuation lines ABOVE the topmost footnote get buffered only if inZone; they're flushed only if another fnStart found above. If the page has ONE footnote whose text wraps ABOVE?? No — wrapping goes below. Multiple footnotes: fn1 (topmost), its continuation below it, fn2, continuation... all handled: continuations get flushed when the fnStart above them is found. Body above fn1: buffered while inZone... then we hit blank → break, buffer discarded → kept. But if no blank between body and fn1, we keep buffering body lines until... we might reach page top (idx<0) with buffer discarded → kept. But wait — what if a body line matches fnStart pattern (like "6 November 2025" — excluded by month check; or "79 172"?)? "79 172." hmm "resolution 79/\n172." — line "172." trimmed — fnStart regex ^(\d{1,2})\s → 172 is 3 digits, no. What about "3 December" mid-body wrap → month-excluded. "16 See"? body wouldn't. I think acceptable.

But there's a subtle bug: lines buffered while inZone but never flushed stay kept — but they were lines between the bottom-most... no wait, they're above the topmost fnStart (body). Kept = correct.

Hmm, one more: blank line INSIDE footnotes (between fn1 and fn2)? My loop breaks at blank even inZone. Then fn2 (below blank, already processed? No — bottom-up: we process fn2 first (lower), buffer its continuation, then fn1? Order bottom-up: fn2cont, fn2, [blank?], fn1cont, fn1. If blank between fn1 and fn2 sections: at blank we break → fn1 never removed! Bad if blanks separate footnotes. pdftotext usually puts footnotes contiguous. Alternatively: blank in inZone → skip blank, continue? But blank between body and footnotes is the main guard... body is ABOVE footnotes, so the guard blank is above fn1 — encountered after fn1 processed. If I "skip blanks while inZone and continue", then after fn1, blank, then body lines get buffered, then page top — discarded. Still guarded by "flush only on fnStart". Actually the blank guard isn't even the critical one — flush-only-on-fnStart is. Let me make blanks non-terminating: while inZone, blank → idx-- continue (blank itself: keep? blanks don't matter in stream; keep). But then body above gets buffered and if it contains a fnStart-like line, wrongly removed. The month check helps. Hmm, also "1 See" in body? No.

But wait — there's a real hazard: paragraph text lines that begin with a small number, e.g., sub-paragraph "3 See"? No. SDG targets "16.3"? starts "16.3" → has period after 16? "16.3" → ^\d{1,3}\. matches → excluded from fnStart. OK.

Decision: blanks while inZone → skip (don't break), rely on flush-on-fnStart. Also break conditions: paragraph-number-like line, roman heading, or... maybe also lines that are very long? No. Also cap: stop if we've scanned more than, say, 15 lines from bottom without... no, footnotes can be long. Keep unbounded but with break conditions. Also stop if line looks like a full paragraph start "N. Text". Already break on /^\d{1,3}\.$/; also break on /^\d{1,3}\.\s/ (paragraph with inline text)? If a paragraph starts mid... a paragraph "26. The Committee..." would only be at page bottom if paragraph starts there — possible! Then footnotes below it. Bottom-up: footnotes processed, then "26. The Committee..." line — should break (it's body). Add break on /^\d{1,3}\.\s/. Yes.

Now the stream: after both passes, for i where keep[i], push {page: rec.page, text: lines[i]}.

Then paragraph scan as designed. One more consideration: the strict `expected` matching — check both trimmed forms. Also, the start line "1." — in the sample, "1.\nA clean, healthy..." Good.

Potential issue: the number might appear as "1." but with the footnote asterisk attached or weird unicode. Can't cover all.

After building paras (each with lines array), text = lines.join('\n').replace(/^\s+|\s+$/g,'') — careful: that strips leading/trailing blank lines and spaces. Use trim on the joined? Trim removes leading spaces of first line too — "exactly as extracted"... trimming edges is fine (it's just blank lines). I'll trim only blank lines at edges: 

```
function paraText(lines){
  let a = lines.slice();
  while (a.length && a[0].trim()==='') a.shift();
  while (a.length && a[a.length-1].trim()==='') a.pop();
  return a.join('\n');
}
```

Statuses:
```
function status(p){
  const rw = refWords[String(p.num)];
  if (rw === undefined) return {code:'noreference'};
  const w = words(p.text).slice(0,6);
  const r = words(rw).slice(0,6);
  return {code: (w.length===r.length && w.every((x,i)=>x===r[i])) ? 'match':'differs', refWords: rw, extracted: w};
}
```

Wait — words(rw): rw is already first six words; normalize anyway.

Rows array:
```
const rows = [];
const maxNum = Math.max(paras.length? paras[paras.length-1].num:0, refParas||0);
const byNum = new Map(paras.map(p=>[p.num,p]));
for (let n=1;n<=maxNum;n++){
  const p = byNum.get(n);
  if (p) { rows.push({num:n, page:p.page, text:paraText(p.lines), found:true}); }
  else rows.push({num:n, found:false});
}
```
But paras may include numbers > refParas (over-count) — range covers via maxNum. Also paras numbers beyond maxNum? maxNum includes last para num. OK.

foundCount = paras.length. differsCount = rows found with differs. 

Render counters: "N of 90" etc. If refParas undefined → show "N" and "reference: not available". Handle gracefully.

Table render function with sort mode. Row click → toggle expanded. I'll store expanded set of nums. Render expanded row after the clicked row: full text pre-wrap + reference panel.

CSV:
```
const q = v => '"' + String(v).replace(/"/g,'""') + '"';
lines: 'paragraph,page,check,reference_first_words,text'
rows: num, page or '', check label, refWords or '', text
```
Text may contain newlines — quoted CSV handles.

Download via blob.

Removed details: counts per kind; list items "p.{page}: text". Group headers: "Headers and footers (page numbers, document symbols, distribution codes)" and "Footnotes (numbered lines at the foot of a page)" and continuations maybe under footnotes. Also leftovers: lines before first paragraph / after last? Actually after last paragraph there are none (last para runs to end, minus footnotes). Leftover-before: title, headings. I'll show them under "Other lines kept out of paragraphs (title and headings before paragraph 1 — review)". Hmm — are they "removed"? They're not in any paragraph. Show them for transparency.

Wait, also roman headings between paragraphs end up INSIDE previous paragraph text (appended). That means paragraph N's text includes heading "II." + heading text. Hmm — should I instead keep headings as separate stream items that don't join paragraphs? The plan: "Text runs until the next start." — headings are part of the text run. But then "full paragraph exactly as extracted" includes trailing heading. It's verbatim, fine. Actually wait — would that break the first-words check? No, first words are at start.

Hmm, but actually — maybe I should strip nothing; verbatim is verbatim. OK.

Alternatively I could detect heading lines (/^[IVX]+\.\s/) and... no, keep simple, verbatim.

One more: blank line handling in paraText join keeps internal blanks — display fine.

First line for table: first non-blank line, slice 90 chars + '…'.

Let me now also add "How this is computed" notes:
- Under counters: "Found by the code from the page text; reference figures come from the file." (as specified) plus brief method.
- Near table: note about matching rule.

Title: use D.title, symbol linked. Line: "Raw PDF text, N pages, source: {source}."

Let me count reference availability: if refParas == null show "—".

Checkbox behavior: reorder rows; expanded states persist.

Accessibility: table with proper th, button semantics, aria-expanded maybe. Keep reasonable.

Now write CSS compactly.

Colors: bg #f4f6f8, card white, border #d8dee4, accent #1f6fb2, text #1c2733. Differs badge #b3261e on #fdecea; matches #1e7a3c on #e8f5ec; noreference grey #5a6672 on #eef1f4; notfound similar red outline.

Font: system stack.

Table: full width, borders bottom, hover bg. Expanded panel bg #fbfcfd, border-left accent.

Now JS render:

```
function render(){
  const tbody = ...;
  const ordered = diffFirst ? rows.slice().sort((a,b)=>(rank(a)-rank(b)) || (a.num-b.num)) : rows;
```
rank: not found/differs/noreference → 0 else 1.

Each found row:
```
<tr class="row found" data-num>
 <td class="num">n</td>
 <td>page</td>
 <td class="first">firstLine</td>
 <td><span class="badge ...">label</span></td>
 <td><a href=docUrl target=_blank>symbol</a></td>
</tr>
<tr class="expander hidden"><td colspan=5> panel </td></tr>
```
Click toggles.

Panel content: 
- label "Full paragraph as extracted (verbatim)": pre-wrap div with text.
- reference box: "Reference first words (from file): “...”" and for differs: "Extracted first six words: ... vs reference: ..." maybe show both normalized. Keep: show refWords verbatim; plus normalized comparison lists when differs.

For not found: "No line beginning 'N.' was found; the paragraph number may be damaged or merged in the raw text. Neighbouring paragraphs: ..." keep simple.

CSV button + checkbox in toolbar above table.

Let me write the final code now, aiming ~600 lines.

Also note: escape HTML everywhere (esc function).

Potential gotcha: `symbol` empty → skip link, show plain text.

Also the doc title in header; subtitle line with pages count = pages.length (records count) — "raw PDF text, N pages, source: …". Use D.count if present else records.length.

Adopted date (reference.adopted) — could show in header line? Not requested; skip or include subtly. Skip.

Write it.

Counters section note exactly: "Found by the code from the page text; reference figures come from the file."

Let me write out everything carefully.

One more detail on the fnStart regex: /^(\d{1,2}|\*)\s+\S/ — asterisk footnote "* The present general comment..." → matches (\*)\s+\S → yes. t.replace(/^(\d{1,2}|\*)\s+/,'') → rest; month check on rest.

Also make sure `/^\d{1,3}\./` exclusion: "1 See" no period → passes. "26. The" → excluded. Good.

Also footnote lines might start with number + non-breaking space or number attached: "1The"? skip.

Also break condition when scanning up: /^\d{1,3}\.\s/ (para with text) and /^\d{1,3}\.$/ and roman headings. Also maybe break if line is very long (>300 chars)? no.

Now, subtle: after removing header/footer lines, indexes — I use keep[] on original lines array; fine.

Trailing skip: `while (idx>=0 && !keep[idx]) idx--;` then skip blanks. But header/footer removal happened in pass 1 which is before pass 2 — yes order: pass1 then pass2. Good.

Edge: page with only header/footer → idx <0 → nothing.

Paragraph scan: `lineStart(t, n)` — build regexes carefully; n up to ~120.

```
function startMatch(t, n){
  const s = String(n);
  if (t === s + '.') return '';
  let m = t.match(new RegExp('^' + s + '\\.\\s+(.+)$'));
  if (m) return m[1];
  m = t.match(new RegExp('^' + s + '\\.([A-Z].*)$'));
  if (m) return m[1];
  return null;
}
```
Returns null if no match; '' if bare number (meaning no text on this line); else first text line. Careful: '' is falsy — handle with `!== null`.

Main loop:
```
let expected = 1, current = null;
const paras = []; const preLines = [];
for (const L of stream){
  const t = L.text.trim();
  if (t !== ''){
    let sn = null, rest = null;
    let r = startMatch(t, expected);
    if (r !== null){ sn = expected; rest = r; }
    else {
      for (let k=1;k<=3 && sn===null;k++){
        r = startMatch(t, expected+k);
        if (r !== null){ sn = expected+k; rest = r; }
      }
    }
    if (sn !== null){
      current = {num: sn, page: L.page, lines: rest ? [rest] : []};
      paras.push(current);
      expected = sn + 1;
      continue;
    }
  }
  if (current) current.lines.push(L.text);
  else preLines.push(L);
}
```
postLines: none (current absorbs to end). Fine — mention in details only preLines.

Wait — lookahead k up to 3: if 26 damaged, 27 found via k=1. If BOTH 26 and 27 damaged, 28 via k=2. OK.

Hmm, one risk with lookahead: stray line like "2. " when expected=5... lookahead only looks UP (6,7,8) not down (2). Stray "6." line in body when expected=5 but real para 6 comes later? E.g., cross-reference "paragraph 6." at a line start? Cross-refs like "(see para. 6.)" — line would start with "6." only if wrap puts it there: "...general comment No. 6.\n" hmm possible: "its general comment No.\n6. The Committee..." wait "No. 6." — the "6." could land at line start! E.g. "...comment No.\n6. (2020)..." — then t = "6. (2020)..." — startMatch: t === '6.'? no; '^6\.\s+(.+)' → matches "(2020)...". rest="(2020)...". Uh oh — if expected ≤ 6 ≤ expected+3, false start! But this requires the wrap AND expected in range. GC27 references "general comment No. 25 (2000)" etc. If line starts "25. (2000) on..." and expected happens to be 23-28... Then rest must also match [A-Z]? My second pattern requires [A-Z] after period, "(2020)" starts with "(" → no match! And first pattern requires \s+ after period: "25. (2000)" has space then "(2000)" — matches ^25\.\s+(.+)$!! Hmm. Danger.

Tighten: require rest (after "N. ") to start with a capital letter or digit? Paragraph text starts with capital: "A clean...", "The Committee...". Cross-ref "(2000)..." starts with paren. So: pattern '^N\.\s+([A-Z].*)$'. And bare 'N.' alone. And 'N\.([A-Z].*)' for no-space damage. Drop the general \s+(.+) pattern. Sub-paragraph "2. The" fine. What about paragraph starting with a number or quote mark? “...” starts with “ (curly quote). E.g., paragraph starting with a quotation: possible in GCs? Rare. Accept risk; gap detection covers.

Hmm, but also the exact-expected match has same constraint. Fine.

Actually wait, what about paragraph text beginning lowercase due to damage? Then missed → gap shown. Tool's job.

Let me also reconsider: should lookahead resync exist at all given plan says strictly "next expected"? The success criteria say numbers run without gaps, so presumably data is clean and lookahead never triggers except for genuine damage. I'll keep it — it makes the tool robust and gaps visible. But one more guard for lookahead: require that it only triggers... eh, with [A-Z] constraint, risk is low. Also require for lookahead that the number line is alone or text — same startMatch. OK.

Also: what about the numbered paragraph "90." being last, followed by nothing? fine.

What about roman numeral headings matching startMatch? "II. Introduction" — "II." not digits. Good.

Now, reference first_words check on paragraph 1: "A clean, healthy and sustainable environment" — extracted starts same → match. 

Counter 3 could be 0 if all fine — but plan expects the tool to show damage; data likely has some hyphenation damage causing differs. Fine either way.

Table first line 90 chars: `fl.length > 90 ? fl.slice(0,90)+'…' : fl`.

CSV check column values: 'matches' / 'differs' / 'no reference' / 'not found'.

Also add refWords column (verbatim from file) for found rows.

Now the "removed lines" details content: 
- summary sentence.
- group 1: headers/footers: list "p.3 — E/C.12/GC/27".
- group 2: footnotes: count footnoteCount, list with page.
- continuations: kind 'footnote-continuation' listed under footnotes group maybe separate subgroup. I'll show footnote starts and their continuations in one list, marking continuations with "↳" prefix. Simpler: separate small groups.

Also "Lines before paragraph 1 (kept out of the table — title and headings)": list preLines non-blank.

Let me now write the HTML file. Also remember: paragraph text "never edited" — we do trim blank edge lines; that's line-level, and we display lines joined with \n; original spacing within lines preserved. Also the start-line remainder: when number alone, text lines are raw. When "N. Text", the remainder drops "N. " prefix — necessary (it's the number). Note it.

Also, "Clicking row 1 shows text starting 'A clean, healthy and sustainable environment'" — yes.

Let me write the code now. I'll aim for clean, commented code.

Also handle: `doc_url` empty → render symbol without link.

Write CSS:

```css
:root{ --accent:#1f6fb2; ... }
*{box-sizing:border-box}
body{margin:0;font:16px/1.55 -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif;background:#f4f6f8;color:#1c2733;}
.wrap{max-width:1100px;margin:0 auto;padding:28px 24px 60px;}
header h1{...}
...
```

Table with sticky header maybe; fine.

Badges: inline-block, padding 2px 8px, radius 10px, font-size 13px.

Expanded panel: grid two columns (min 280px), gap.

Button: accent bg, white text.

Checkbox label.

Stat cards: flex, each with big number.

Now write JS fully. Also guard JSON weirdness.

Render function builds rows HTML string each time; attach one click handler via delegation on tbody: clicking a `tr.prow` toggles expansion. Expanded state stored in Set of nums; re-render preserves.

Simpler: build all rows including hidden expander rows; toggle class via delegation without full re-render. But checkbox reorder needs re-render. I'll re-render on toggle change and on row click just toggle the expander row's hidden class + aria.

Implementation detail: rows in DOM order: for each row: `<tr class="prow" data-num="n">...` then `<tr class="xrow" data-num="n" hidden><td colspan=5>...panel...</td></tr>`. Delegation: tbody click on tr.prow → find next sibling xrow, toggle hidden. Also keyboard: make prow tabindex=0, Enter/Space toggles. Nice for a11y; small addition.

Panel content builder (found):
```
<div class="panel">
  <div class="ptext"><h4>Full paragraph — exactly as extracted</h4><div class="verbatim">text</div>
   <p class="cite">Extracted from p.{page} of the raw PDF text; begins at the line “{num}.”</p></div>
  <div class="pref">
    <h4>Reference</h4>
    {if refWords: <p>First words in the reference file:</p><blockquote>“...”</blockquote>
       comparison: extracted six words vs reference six words (chips) if differs
     else <p>No entry for paragraph {num} in the reference — marked “no reference”, not “Differs”.</p>}
  </div>
</div>
```

For differs show both word lists:
```
<p>Extracted: a · clean · …</p><p>Reference: …</p>
```

Not found panel: message + maybe reference words if available ("Reference expects: “…”").

CSV build:
```
let csv = '\uFEFFparagraph,page,check,reference_first_words,text\n';
rows.forEach(r=>{
  csv += [r.num, r.found?r.page:'', label(r), r.found? (refWords[String(r.num)]??'') : '', r.found?r.text:''].map(q).join(',')+'\n';
});
```

Blob: type 'text/csv;charset=utf-8'.

Filename: (symbol||'document').replace(/[^\w.-]+/g,'_') + '-paragraph-check.csv'.

Counters:
1. big: foundCount, small: "of {refParas ?? '?'} paragraphs in the reference" — label "Paragraphs found". Show like "88 of 90".
2. "Footnotes removed": "{fnCount} of {refNotes ?? '?'}".
3. "Opening words differ": differsCount. Subtitle: "paragraphs whose first six words do not match" (+ maybe "n with no reference entry" if >0).

Note under: exact sentence + method summary.

Also honesty note if refParas missing.

Alright, also small note near table: "How this is computed: a paragraph starts at a line beginning with the next expected number followed by a full stop; text runs to the next start; lettered sub-paragraphs stay inside. 'Differs' compares the first six words, ignoring case, punctuation and spacing."

Also mention gaps: rows marked "not found".

Let me write the file. Estimate ~550 lines. Go.

Also careful: in HTML string building, escape text via esc().

Double-check month regex usage: 
```
const MONTH = /^(january|february|march|april|may|june|july|august|september|october|november|december)\b/i;
const rest = t.replace(/^(\d{1,2}|\*)\s+/, '');
fnStart = /^(\d{1,2}|\*)\s+\S/.test(t) && !/^\d{1,3}\./.test(t) && !MONTH.test(rest);
```
Wait, also exclude if line is like "2025 See"? 4 digits — ^\d{1,2}\s requires 1-2 digits then space; "2025 See" — \d{1,2} matches "20"? Then \s needs to match "2"? No — regex ^(\d{1,2})\s: after 1-2 digits must be whitespace; "2025 " after "20" comes "2" not space → backtrack to \d{1}="2", next "0" not space → no match. Good.

Asterisk footnote continuation: fine.

Also there may be lines like "Notes" heading before footnotes? "________" separator? If a separator line exists above footnotes, bottom-up: ...fn lines..., then "____" line: not fnStart, inZone → buffered; then blank or body → break, buffer discarded → separator stays in stream → appended to previous paragraph text. Minor. Could add separator pattern to break conditions: /^_+$|^—+$/. Add break. And maybe also treat as removed? Just break; it stays in text. Eh, add break condition.

Also footnote zone: what if page has NO footnotes but last body line is like "3 December 2025"? month-excluded. OK.

Another thought on `preLines`: page 1 contains title etc. Show them.

Also: what about text between... fine.

Now, "reference figures come from the file" — refParas = D.reference?.paragraphs; display.

Time to write. I'll be careful with template literals inside script (no issues). Use plain string concatenation or template literals — fine in HTML file (watch out for `</script>` sequences — none).

Line count target under 700. Let me write concisely but readable.

Also include a small legend for badges.

Also the toolbar: checkbox "Show differences first" + button "Download CSV" + maybe count "showing X rows". 

Write the code.

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Paragraph check · E/C.12/GC/27</title>
<style>
  :root{
    --accent:#1f6fb2; --accent-dark:#175a91;
    --bg:#f4f6f8; --card:#ffffff; --line:#d9dfe5; --ink:#1c2733; --muted:#5a6672;
    --red:#b3261e; --red-bg:#fdecea; --green:#1e7a3c; --green-bg:#e9f6ee; --grey-bg:#eef1f4;
  }
  *{box-sizing:border-box}
  body{margin:0;background:var(--bg);color:var(--ink);
    font:16px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;}
  .wrap{max-width:1120px;margin:0 auto;padding:30px 26px 70px;}
  ...
</style>
```

etc. Let me just write the full thing in the answer. I need to be thorough but concise. Also comments in code sparingly.

One more check — "Every row that shows a document has its symbol, linked to doc_url in a new tab." Yes, symbol cell with target=_blank rel=noopener.

Counter card markup:

```
<div class="stats">
  <div class="stat"><div class="big">88<span class="of">of 90</span></div><div class="lab">Paragraphs found</div></div>
  ...
</div>
<p class="how">Found by the code from the page text; reference figures come from the file. A paragraph starts ... </p>
```

Also mention adopted date? skip.

Now handle case refParas === undefined: `of ?` show "of —". Fine.

Write everything.

For the expandable rows, build via array map and join, then innerHTML. Event delegation on tbody.

Also the "not found" row: page '—', first line '— not found in the raw page text', badge 'not found', symbol link still shown (it's a document row... it doesn't show a document per se, but keep symbol link for context — harmless; the rule says every row that shows a document has symbol linked. I'll include symbol link in all rows).

Sort rank: differs/notfound/noreference → 0; matches → 1.

CSV label mapping: match→'matches', differs→'differs', noreference→'no reference', notfound→'not found'.

Let me write the removed-lines details:

```
<details class="removed">
 <summary>Lines removed as headers, footers and footnotes (N)</summary>
 <p class="how">…explanation…</p>
 <h4>Page furniture (page numbers, document symbol, distribution codes) — n lines</h4>
 <ul>…</ul>
 <h4>Footnote lines — n removed, counted</h4>
 <ul>…</ul>
 <h4>Continuation lines of footnotes — n</h4>
 <ul>…</ul>
 <h4>Lines before paragraph 1 (title and headings — not part of any paragraph, shown for review)</h4>
 <ul>…</ul>
</details>
```

List items: `p.{page}: “{text}”` — text could be long; truncate to ~140 chars with title attr full? Keep full but CSS wrap. Use truncation with ellipsis + title. Keep full text — verbatim principle. It's a details list; wrap is fine. I'll keep full.

Empty groups → show "none".

Counting: headerCount = removed.filter(kind==='header').length etc.

Edge: removed list could be long (20 pages × ~4 lines + footnotes ~40) — fine.

Now finalize the paragraph-start regexes with escaped numbers (digits fine).

Potential problem: `startMatch` with t like "1." when expected=1 — returns ''. rest='' → lines []. Then subsequent lines pushed. Good.

Also handle possibility that number line includes trailing spaces — trimmed t used.

Write panel for found rows:

```
function panelHTML(r){
  if(!r.found){
    const rw = refWords[String(r.num)];
    return `<td colspan="5"><div class="panel">
      <p>No line beginning “${r.num}.” was found in the raw page text. The number may be missing, merged into another line, or damaged by the PDF conversion.</p>
      ${rw?`<p class="refw">Reference expects this paragraph to begin: <blockquote>“${esc(rw)}”</blockquote></p>`:''}
    </div></td>`;
  }
  const rw = refWords[String(r.num)];
  let refBlock;
  if(rw === undefined){
    refBlock = `<p>The reference file has no entry for paragraph ${r.num}, so this row is marked <span class="badge b-noref">no reference</span>, not “Differs”.</p>`;
  } else {
    const ext = r.words6.join(' · ');
    const ref = words(rw).slice(0,6).join(' · ');
    refBlock = `<p>Reference first words:</p><blockquote>“${esc(rw)}”</blockquote>` +
      (r.check==='differs' ? `<p><strong>Comparison of the first six words</strong> (lower-case, punctuation ignored):</p>
        <p>Extracted: ${esc(ext)}</p><p>Reference: ${esc(ref)}</p>` : '');
  }
  return `<td colspan="5"><div class="panel">
    <div class="pcol"><h4>Full paragraph — exactly as extracted (verbatim)</h4><div class="verbatim">${esc(r.text)}</div>
      <p class="cite">Starts on page ${r.page} of the raw PDF text, at the line “${r.num}.”. Nothing in this text has been edited or paraphrased.</p></div>
    <div class="pcol"><h4>Reference</h4>${refBlock}</div>
  </div></td>`;
}
```

Precompute r.words6 and r.check at row build.

OK — also stats note: "How this is computed" text.

Let me count lines roughly as I write; keep CSS tight.

Also title of page/tab: "Paragraph check — {symbol}".

Header:
```
<header>
  <p class="kicker">Paragraph-level verification tool</p>
  <h1>{title}</h1>
  <p class="sub">Raw PDF text, {N} pages · source: {source} · {symbol link}</p>
</header>
```
Plan: "Title and symbol linked to doc_url, with one line: 'raw PDF text, N pages, source: …'". Good.

Now write final answer. Brief intro (≤3 sentences), code block, nothing after.

Let me make sure script handles missing reference gracefully (refWords = {}, refParas = null → display "of —" and note "reference figures not available in the file"). The data description says reference exists, but be safe.

One more consideration on stats card 3 label: "Opening words differ" big number = differsCount, sub "paragraphs whose first six words differ from the reference" and maybe "+m with no reference entry".

Also if foundCount > refParas (over-split), the "of 90" reads odd but honest; add note? The gaps/extra visible in table. fine.

Now write it all out. I'll write carefully to avoid JS syntax errors.

Regarding `words()` when text empty → [].slice(0,6) → [] vs ref length 6 → differs. Fine.

Also join for first line: `r.text.split('\n')` find first non-blank.

CSV: also include a header comment? No, keep clean columns: paragraph,page,check,reference_first_words,text.

Edge in CSV: text contains quotes/newlines — escaped by q().

Also add row count sanity: CSV rows = rows.length (matching table). Good.

Write now. Also remember base font 16px, projector-readable.

Final structure sizes fine. Let me produce the code.

```js
(function(){
  var D = window.WORKSHOP_DATA && window.WORKSHOP_DATA.pdf_text;
  var out = document.getElementById('app');
  if(!D || !D.records || !D.records.length){
    out.innerHTML = '<p class="empty">No PDF text found in WORKSHOP_DATA.pdf_text.</p>';
    return;
  }
  ...
})();
```

I'll use const/let, fine.

Detailed code:

```js
const D = window.WORKSHOP_DATA.pdf_text;
const symbol = D.symbol || '';
const docUrl = D.doc_url || '';
const ref = D.reference || {};
const refParas = (typeof ref.paragraphs === 'number') ? ref.paragraphs : null;
const refNotes = (typeof ref.footnotes === 'number') ? ref.footnotes : null;
const refWords = ref.first_words || {};
const pages = D.records.slice().sort((a,b)=>(a.page||0)-(b.page||0));
```

Classification:

```js
const MONTH = /^(january|february|march|april|may|june|july|august|september|october|november|december)\b/i;
const stream = [];
const removed = [];
let footnoteStarts = 0;

pages.forEach(rec=>{
  const lines = String(rec.text == null ? '' : rec.text).split(/\r?\n/);
  const n = lines.length;
  const keep = new Array(n).fill(true);
  const trimmed = lines.map(l=>l.trim());

  // pass 1: page furniture
  for(let i=0;i<n;i++){
    const t = trimmed[i];
    if(!t) continue;
    const furniture =
      (symbol && t === symbol) ||
      /^GE\.\s?\d/.test(t) ||
      (/^\d{1,3}$/.test(t) && (i<4 || i>=n-4));
    if(furniture){ keep[i]=false; removed.push({page:rec.page, text:t, kind:'furniture'}); }
  }

  // pass 2: footnotes from the bottom
  let idx = n-1;
  while(idx>=0 && (!keep[idx] || trimmed[idx]==='')) idx--;
  let inZone = false;
  let buffer = [];
  const flush = ()=>{ buffer.forEach(b=>{ keep[b]=false; removed.push({page:rec.page, text:trimmed[b], kind:'fncont'}); }); buffer=[]; };
  while(idx>=0){
    const t = trimmed[idx];
    if(t===''){ if(inZone){ idx--; continue; } break; }
    if(/^_+$/.test(t) || /^[-–—=]{3,}$/.test(t)){ if(inZone){ idx--; continue; } break; }
    const isFnStart =
      /^(\d{1,2}|\*)\s+\S/.test(t) &&
      !/^\d{1,3}\./.test(t) &&
      !MONTH.test(t.replace(/^(\d{1,2}|\*)\s+/,''));
    if(isFnStart){
      flush();
      keep[idx]=false;
      removed.push({page:rec.page, text:t, kind:'footnote'});
      footnoteStarts++;
      inZone = true; idx--; continue;
    }
    if(inZone){
      if(/^\d{1,3}\.(?:\s|$)/.test(t)) break;   // a paragraph start: body begins
      if(/^[IVXLCDM]+\.\s/.test(t)) break;      // section heading
      buffer.push(idx); idx--; continue;
    }
    break;
  }
```

Wait — blank skip when not inZone: break (blank at bottom after furniture — nothing). But actually if not inZone and we hit blank — but we pre-skipped trailing blanks; blanks inside mean... just break. Fine.

Hmm, careful: blank handling `if(t===''){ if(inZone){idx--;continue;} break; }` — when inZone, skipping blanks indefinitely could walk up through blank-separated body paragraphs, buffering everything, until a fnStart-like line appears in body. The [A-Z]-style guards: paragraph starts break. Most body lines don't match fnStart; the risk is a body line like "4 December" — month-excluded. "2 E/..." — body wouldn't. I'll also add a safety cap: stop buffering after 25 lines past the last fnStart? Footnote blocks are short. Let me add: if buffer.length > 30 → break (discard). Good safety.

Actually simpler: track linesSinceFn; if > 40 break. Add.

```
  for(let i=0;i<n;i++) if(keep[i]) stream.push({page:rec.page, text:lines[i]});
});
```

Paragraph scan (as designed). Then rows build, stats, render.

I think we're ready. Also the note about how differs computed near table.

Let me also double check expanded row click: delegation:

```
tbody.addEventListener('click', e=>{
  const tr = e.target.closest('tr.prow');
  if(!tr) return;
  const xr = tr.nextElementSibling;
  if(xr && xr.classList.contains('xrow')){
    const hid = xr.hasAttribute('hidden');
    if(hid) xr.removeAttribute('hidden'); else xr.setAttribute('hidden','');
    tr.setAttribute('aria-expanded', hid ? 'true':'false');
  }
});
```
Also keydown Enter/Space on prow.

Re-render on checkbox change: rebuild tbody preserving expanded set:
```
const openRows = new Set();
```
On toggle click, update set, and just toggle DOM (no re-render). On checkbox change, re-render with open states applied (xrow hidden = !openRows.has(num)).

Simplify: keep openRows; row click updates set + toggles DOM. Checkbox change → render().

Download button handler builds CSV from current rows (all rows, regardless of sort).

Alright, writing final HTML. Also CSS for .verbatim{white-space:pre-wrap; font-family: inherit?} Use slightly mono? "exactly as extracted" — a monospace hints rawness. I'll use ui-monospace stack at 14px. Good.

Also badges column width; table layout: use table with th scope.

Let me write it all now, final.

Counting stats:
- foundCount = paras.length
- differCount = rows.filter(r=>r.check==='differs').length
- norefCount = rows.filter(r=>r.found && r.check==='noreference').length
- gapCount = rows.filter(r=>!r.found).length

Show in note if any: "n paragraphs missing from the page text; m have no reference entry." Keep.

Stat 3 sub: "first six words do not match" and if noref>0 add "(+m with no reference entry)".

OK write.