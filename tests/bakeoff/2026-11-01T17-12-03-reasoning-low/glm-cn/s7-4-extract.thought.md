Build the tool. Need to parse pages: remove headers/footers, footnotes, split numbered paragraphs "N. text". Reference has paragraphs count, footnotes count, first_words. Compare first six words with reference; mark mismatches.

Parsing approach: join pages with markers, remove known header/footer lines (lines matching symbol, "United Nations", "Distr.:", "Original:", page numbers, "GE.25-..." etc). Actually simpler: process text per paragraph detection.

Strategy: concatenate all text with page boundaries. Build a "clean" stream: for each page, drop lines that are headers/footers. Header/footer detection: lines matching symbol regex, "United Nations", "Economic and Social Council", "Committee on...", "Distr.: General", date line, "Original: English", page number alone, "GE.\d", "* " footnote marker? Footnotes: usually at bottom, lines starting with a number followed by space or footnote separator. Tricky generically — but we only have this one document. Keep heuristics but reasonably general.

Simpler robust approach: scan the joined text for paragraph-start pattern: at line start, a number followed by "." and then capital or text (e.g. "1.\n" or "1. A clean,"). Footnote pattern: number followed by space or "/" (e.g. "1/ See..."). Footnotes appear after paragraphs; typically footnote lines like "1/ See A/..." — in UN docs footnotes use "n/". So paragraph number = /^\s*(\d{1,3})\.\s/ and footnote = /^\s*(\d{1,2})\/\s/.

Headers: repeated lines across pages — I can detect lines that appear on ≥ half the pages and are short, and drop them, plus lines that are exactly a page number, and lines at top of page before first real content. Do: per page, remove repeated lines (frequency across pages > pages/2 and length < 80), drop pure page numbers, drop lines matching distr/original/symbol patterns.

Footnote removal: once footnote marker pattern ^\d{1,2}/ appears, cut from there? Footnotes appear at page bottom in the source text mixed in. Approach: drop lines matching footnote pattern and subsequent lines until a paragraph-start or blank... Risky. Better: remove all lines that match footnote-start /^\d{1,3}\/\s/ and lines that follow within the footnote block until an empty line or a paragraph-number line. Also footnote marker lines might be like "1/ See E/2010/..." single-line footnotes, mostly.

Also the footnote separator line of asterisks or underscores — drop.

I'll implement: split text into lines per page; clean; join into a single string with "\n"; then walk lines, accumulate paragraphs: when line matches /^(\d{1,3})\.\s*/ and expected number is next (or any number), start a new paragraph. Stop paragraphs at footnote blocks: when a line matches /^(\d{1,3})[\/)]?\s+(See|A\/|E\/|...)... hmm.

Let me do footnote handling: track mode. In paragraph-accumulation, if line matches /^(\d{1,2})\/\s/ → footnote mode; skip lines until we hit a line matching paragraph-start or a header/blank-line followed by paragraph start? Footnotes may be multi-line and end before page footer. Since footnotes are per-page and after them come page footers (removed) then next page content starting with heading or paragraph. Simpler: in footnote mode, skip lines until a paragraph-start line appears. Headings like "II." would be skipped too — that loses only heading lines, fine. But footnote blocks might be followed by non-numbered paragraphs? In UN GC docs all body paragraphs are numbered. OK.

Also the title page has unnumbered intro lines; they'll be skipped (before paragraph 1). Good.

Reference first_words: {"1": "..."} compare first 6 words normalized (lowercase, strip punctuation) of extracted paragraph vs reference. Mark mismatch.

CSV download via Blob.

Show stats: found n vs reference n, footnotes found vs reference footnotes count. Count footnotes found (unique footnote markers). Also adopted info maybe. Table with para number, first line, match badge, click expand full text. Symbol linked.

Sanitize text for HTML display.

Let me write it. Word normalization: lowercase, replace non-alphanumeric with space, split, filter, take 6, join.

CSV: columns number, first_words_reference, match, text. Quote properly.

Chart? Not needed necessarily, but could add a small chart... spec says use Chart.js for charts; not required. Maybe a simple bar isn't needed. Skip charts; keep clean. Maybe include a small horizontal bar comparing found vs reference — could do a tiny chart. I'll add one small bar chart comparing found paragraphs vs reference and footnotes found vs reference. That's a nice visual. Keep it.

Also show pages processed count.

Header cleaning details: compute line frequency across pages (trimmed). Drop lines where count >= max(2, pages/2) and trimmed length < 100 — but careful: paragraph content lines won't repeat. Also drop lines matching: /^GE\.\d/, /^\d+$/ (page numbers), /^E\/C\.12\// (symbol), "United Nations", "Economic and Social Council", "Committee on Economic...", "Distr.: General", date line, "Original: English". The frequency approach handles these. Also "* " title footnote line. And lines of asterisks "*****".

Footnote count: count distinct footnote numbers found; report vs reference.

Edge: paragraph numbers restart? No.

Write code.