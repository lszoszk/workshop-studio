Build the app. Plan parsing: join pages in order, remove header/footer lines, detect footnotes (lines starting with small number followed by space? at foot of page — hard; use heuristics), paragraphs start with "N. " next expected number.

Footnote detection: a line matching /^\d{1,2}\s/ at the foot of page before numbered paragraph lines... Simpler: lines that begin with a small number followed by space and that are not paragraph starts (out of sequence). But paragraph starts are "N. " with period. Footnote lines like "1/ " in UN docs actually... In this PDF, footnotes often appear as just digits or "See ..." at page foot. I'll use: a line matching /^\d{1,2}$/ (page number) removed; /^\d+\.\s/ paragraph start if matches expected next number; footnote lines: lines starting with a small number followed by "/" or space that are out of sequence and appear in the last portion of a page? Keep simple: treat lines matching /^(\d{1,2})\s+\S/ where number is not the expected next paragraph and the line is within the last 25% of the page's lines as footnotes. Count removed lines in general "removed lines" list with reason.

Reference first_words keyed by paragraph number strings.

Let me write it. CSV with quoted values, BOM maybe. Keep under 700 lines.

Parsing per page:
- lines = text.split(/\n/)
- clean lines: skip if /^\s*$/ (keep blank? not needed), skip if line.trim() is only digits (page number), skip if line.trim() === symbol, skip if /^GE\.\d+/ or contains "GE." followed by digits at start, skip "E/C.12/GC/27" (symbol). Also skip "United Nations"? Rules say only those three. Keep it.
- Footnotes: iterate lines; a line matching /^(\d{1,2})(\/|\s)/ where number not equal expected next and page-position in bottom third? Simplify: track expected next paragraph number; line starts with `${expected}. ` → paragraph start. Line starts with number+period where number != expected → not a start, just text. Footnote: line matches /^\d{1,2}\s/ or /^\d{1,2}\/\s/ and is in the last ~8 lines of the page. I'll do that.

Paragraph building: current paragraph object; append lines. Page where paragraph starts recorded.

Compare: first six words normalized: text after "N. " prefix. Strip leading paragraph number "N." from text for display? Keep text as extracted (never edited). For comparison, strip the leading "^\d+\.\s*" from the text. Normalize words: lowercase, remove punctuation.

Differs if reference has entry and words mismatch. If no reference entry → "no reference".

Write code now.