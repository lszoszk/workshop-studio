I only have a sample of page 1 data to work with, so I need to design parsing that's robust to variation. I'm thinking through how to classify each line in the page text—distinguishing blank lines, standalone page numbers, and other structural markers—to properly map records against the reference paragraphs, footnotes, and adopted text.

I'm realizing paragraph numbers can appear on their own line followed by the text on the next line, so I need my number-detection regex to handle both inline and standalone cases. The trickier problem is distinguishing a paragraph number (digits followed by a period) from a footnote marker (digits followed directly by text with no period), since both can appear as short numeric lines at the start of content.

I'm thinking footnotes should be identified by sequence—tracking the expected next footnote number and treating a page-foot line as a footnote start if it matches that number, with all subsequent wrapped lines on that page treated as footnote continuation until the page ends.

Edge cases worry me: a bare digit on its own line could be either a page number or a standalone footnote marker, so I need to disambiguate using the expected footnote sequence and position on the page rather than relying on a trailing period rule, which doesn't apply to numeric-only lines. I also need to account for inline superscript-style footnote markers that some PDF converters embed directly in body text.

I should also allow some tolerance when matching expected footnote numbers in sequence, since missing one would break detection for all subsequent ones -- accepting numbers slightly ahead of the last one rather than requiring an exact match. And I need to decide whether asterisk-marked footnotes (like title-page annotations) should be treated the same way as numbered ones.

There's also the edge case of footnotes continuing across page breaks, which I can't fully resolve but should flag as a limitation. I also need to identify header lines, like the standalone document symbol or the "GE.25-xxxxx (E)" print codes, using a pattern matching "GE." followed by digits.

I should treat text before the first numbered paragraph — the title block, "Distr.: General," etc. — as a separate transparent group rather than silently discarding it, so the user can see exactly what's being excluded. I'm also considering whether section headings between paragraphs should stay attached to the end of the preceding paragraph's text, since that's a visible artifact the user likely wants surfaced.

I'll keep the paragraph-start detection simple: a line matching a number followed by a period, where the number equals the expected next count, marks a new paragraph, while lettered sub-items like "(a)" remain part of the current paragraph's text.

The paragraph number itself should be excluded from the stored text, shown separately, since the reference first-words start right after the number. For comparison I'm normalizing words by lowercasing and stripping non-letter/digit characters, then comparing the first six tokens against the reference's first-words array, handling cases where lengths might not match exactly.

I'm also thinking through the "Differs" counter logic — tracking paragraphs where a reference exists but text doesn't match versus paragraphs with no reference at all. There's a real risk with the sequential numbering approach: if a single paragraph number fails to parse correctly in the PDF extraction, everything after it could get silently absorbed into the wrong paragraph since the algorithm strictly expects numbers in sequence, so I need to consider whether some recovery mechanism is worth adding despite the rule being strict.

I'm deciding to keep the strict matching simple, but add a diagnostic note at the end reporting where numbering stopped relative to the reference count, so the damage is visible rather than silent. I'm also weighing edge cases like cross-reference text wrapping across lines that could falsely trigger a paragraph match, and how to handle page tracking and blank lines when paragraphs span across page boundaries with headers/footnotes removed.

I'm leaning toward dropping blank lines entirely rather than preserving paragraph breaks, since collapsing whitespace is simpler than trying to faithfully reconstruct spacing, and I'll just note this behavior rather than overengineer it. I still need to handle lines that are just a bare page number without confusing them with footnote markers.

I'll resolve the ambiguity by prioritizing position: a bare-digits line is a page number if it sits at the very start or end of the page's non-empty lines, otherwise I'll check if it falls within the footnote number range to treat it as a footnote start.

I also need to handle separator lines of underscores or dashes, which often precede footnotes, by stripping them out as pure formatting artifacts rather than content.

Once such a separator is found, everything remaining on that page is likely the footnote zone, but I still need to validate footnote numbering using the expected-sequence check, since lines like "2020 report" or wrapped continuations such as "10 per cent" could falsely look like numbered footnotes. I'll apply the same sequence-based validation whether or not a separator zone is detected.

For actually matching a new footnote start, I'll require the number to immediately follow the last footnote number, with maybe a small tolerance range outside the zone versus stricter matching within it, to avoid false positives on body text that happens to start with a number.

I'll settle on accepting last+1..last+2 outside the footnote zone and last+1..last+5 inside it. For tracking removed lines, I'll store page, kind, and text, categorizing them as page numbers, document symbols, distribution codes, footnotes, separators, or pre-paragraph-1 lines, with footnote lines grouped by page in a scrollable details view since there could be hundreds. I also need to think about whether paragraph-start detection should take priority over footnote-line detection when a line could match either pattern.

I'm defining the paragraph-start regex to match numbered markers like "1." either standalone or followed by text, while also deciding to label front-matter lines before paragraph 1 distinctly in the removed-lines list, and handling edge cases like asterisk-prefixed footnote markers and section headings embedded within paragraph text.

For symbol-line detection, I'm checking whether a line equals the document symbol exactly or contains it alongside only digits/whitespace (like page numbers), using a regex that escapes the symbol and verifies the remainder is purely numeric or blank.

For the display, each row shows number, page, first line, symbol, and a differs indicator, and clicking expands a detail area showing the full text plus a comparison of reference versus extracted first words. I'll track expanded rows in a Set so re-renders preserve state, and add a "show differences first" sort option with subtle badges (checkmark for matches, grey for missing reference, warm color for mismatches) while keeping the accent blue as the primary color.

Now I'm working out the symbol column linking to doc_url, and the CSV export format with quoted fields, escaped quotes, preserved newlines, a BOM for Excel compatibility, and rows ordered by number with a header row, built via Blob and a download link. I'm also planning counters for paragraphs found versus reference, footnotes removed, and differences, plus a note clarifying that the code-derived numbers come from the page text while the reference figures come from the file, along with a warning panel for early-stopped or interrupted numbering sequences.

Writing the parser logic...

Still writing parser...

I'm weighing edge cases like date-like lines being misread as footnote starts when the counter is at zero, accepting some false positives since they'll be caught by count checks. For the asterisk marker and paragraph-start detection, I'm matching numbered paragraph markers against the expected sequence number, pushing the current block and starting a new one with the matched text when it lines up.

For in-zone handling, I'm deciding how to detect continuation lines versus new footnote starts based on whether the number falls within a small range after the last footnote number, and separately checking if a trailing bare-digit line is actually a page number rather than part of a footnote.

For paragraph text I'm building a display line by joining the paragraph's lines, collapsing whitespace, and truncating to roughly 90 characters with an ellipsis, plus extracting up to six normalized words (lowercased, stripped of non-letter/number characters) for comparison purposes. I'm also setting the status to 'noref' when no matching reference entry exists, otherwise computing a comparison status.

Now I'm planning the rendering: building a table with event delegation so clicking a row expands a detail view showing the full extracted paragraph alongside the reference's first words versus the extracted normalized words, highlighting mismatches, plus a collapsible section listing removed lines grouped by reason with per-kind counts and a scrollable container for long lists.

I'm also sketching layout and styling details -- column widths, a header line showing page count and source, and keeping the CSS/JS compact -- before finalizing the response with a brief explanation.

