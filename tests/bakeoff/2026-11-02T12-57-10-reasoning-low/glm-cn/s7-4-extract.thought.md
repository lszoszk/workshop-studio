Build the app per plan. Need parser: join pages, remove header/footer lines, remove footnote lines, find paragraph starts with next expected number. Footnote detection: lines at foot of page starting with small number + text — tricky. I'll implement: within a page, track lines; a line matching /^\d{1,2}\s+\S/ after some content... Simpler heuristic: a footnote line is one whose first token is a small number that doesn't match the next expected paragraph number and appears below... The doc's footnotes are numbered 1..N in sequence per document? Reference.footnotes count exists. I'll implement: collect removedLines and footnote count; footnote lines are those matching /^\d+\s/ or starting with number where the number is not the expected paragraph number and the page position is in lower part? Hard to know position. I'll count lines matching /^\d{1,2}[. ]?\s+\p{L}/ that aren't paragraph starts, and are short-ish, as footnote lines (or continuation). Keep simple: footnote line = line starting with a number 1-99 followed by space(s) and text, where number != expected paragraph. Removed lines list shows them so user can check.

Footnotes in GC27 likely appear like "1 See ..." at page foot. Also footnote markers may be superscript converted to nothing. Just do the heuristic.

Paragraph start: line begins with "^{expected}\.\s". Continue until next such. Join lines with spaces.

Differs: first six words normalized vs reference first_words[n]; if no reference entry -> "no reference".

Write HTML with inline CSS/JS, table, expandable rows, CSV download via Blob.