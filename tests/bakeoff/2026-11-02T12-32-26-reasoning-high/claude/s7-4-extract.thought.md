I need to build the app without seeing all the data, so I'll design the parser to be robust. Looking at the structure, the text format shows numbering and periods appearing on their own line, with the actual paragraph text following on the next line, so I'll need to handle that split pattern when parsing records.

For footnotes, this is trickier since they're embedded within page text rather than clearly delimited. I'm thinking through a heuristic: footnotes likely start with a number followed by text at the bottom of the page, so I may need to detect them by comparing against the expected paragraph sequence and treating out-of-sequence numbers as footnote markers.

I'll just test the heuristic and compare against the reference output rather than trying to anticipate every edge case. Once a line matches the expected footnote number, I'll treat everything from there to the end of the page as footnote text, since footnotes sit at the bottom of the page—there's some risk of collision with body text numbers, but that should be rare since the number has to match the exact expected sequence.

I need to disambiguate digit-only lines that could be either a page number or a footnote marker: if the number matches the expected footnote and is followed by non-numeric text, treat it as a footnote; otherwise if it matches the page number, treat it as a page marker. I should also double-check that numbered paragraph formats like "1.\nA clean" don't get mistaken for footnotes.

For the global cleanup, I'll strip page-number/symbol/GE lines regardless of which zone they're in, matching lines equal to the document symbol (e.g. "E/C.12/GC/27") or matching a pattern like "GE." followed by digits for the printing code line.

I also need to handle text before paragraph 1 — any preamble that never attaches to a numbered paragraph should be flagged in a "text before paragraph 1" category so nothing is silently discarded, and headings between paragraphs will just get absorbed into the end of the prior paragraph's extracted text, which is acceptable since it's shown exactly as extracted.

For line joining within a paragraph, I need to decide whether to preserve newlines for sub-items like "(a)" or just join everything with spaces for readability, noting this choice explicitly rather than treating it as silent editing.

A trickier issue: if a paragraph number is damaged in the source and never gets detected, every subsequent paragraph could fail to start correctly since detection depends on finding the next expected number in sequence. I need to think about how the spec's rule that out-of-sequence numbers don't start a paragraph interacts with this risk of cascading failure.

I also want to consider edge cases where a number stands alone on its line versus being followed by text, and how to avoid false positives from things like sub-list markers or roman numeral headings that aren't true paragraph numbers.

For comparing paragraph text to reference first-words, I'll strip punctuation, normalize unicode, split into words, and compare the first six words (or fewer if the reference has less), treating hyphenated terms consistently. I'm also tracking counters for paragraphs matched against the reference and footnotes removed, falling back to "no reference" when entries are missing.

Now I'm designing the results table with columns for number, page, first line, symbol, and a differs indicator, where clicking a row expands a detail section showing the full text alongside the reference words for comparison. I'm adding a "show differences first" sort option, keyboard accessibility for rows, and making sure differing rows display the reference words both inline and in the expanded detail, plus planning a CSV export with matching columns.

I'm working out the line-by-line parsing logic for each page: trimming lines, skipping blanks, and checking patterns like the distribution code prefix or an exact match to the symbol string to classify them as removed content.

For digit-only lines, I need to distinguish real footnote markers from page numbers—comparing against the expected footnote counter versus checking if the number matches the page's position in the document, since plain page numbers could appear anywhere near the start or end of non-empty lines.

A footnote continuing onto the next page could get misattributed to a paragraph, but I'll treat that as a rare edge case to ignore. For detecting a footnote start, I'm requiring the line number to match the expected footnote count and not look like a paragraph start, though I worry about body text that happens to begin with a matching number — I could add a positional constraint requiring the line fall within the lower portion of the page, but that breaks for short pages where footnotes sit near the top.

I'll skip the position constraint since it's unreliable, but nbsp counts as whitespace so numbered footnotes like "1 See" are handled fine. For asterisk-marked footnotes like the title adoption note, I'll detect lines starting with "*" followed by text as a separate "asterisk note" category, flagged in the UI rather than counted with the numbered footnotes.

Now I'm working out the paragraph-numbering regex, making sure digit-dot patterns like "12." only match paragraph starts (not footnotes) when not inside a footnote zone, and checking that the matched number equals the expected next paragraph. Lines before the first paragraph go into a preamble list, and I'm considering whether to flag trailing heading-like text (roman numerals or single capital letters followed by a period) that bleed into paragraph bodies.

I decide to leave heading lines attached to the preceding paragraph rather than splitting them out, noting this behavior honestly in the output rather than treating it as a detected issue. For the actual paragraph text, I'm truncating the first line to roughly 90 characters with an ellipsis, and setting up line-joining logic where lines starting with lettered or roman-numeral list markers like "(a)" or "(iv)" begin a new line instead of merging with the previous text.

Hyphenated words split across lines will just get joined with a literal space rather than being cleaned up, since that's intentionally left as-is so it can surface as a "Differs" flag in comparisons. I'm also planning out the rendering structure—header, three summary counter cards, a note, controls with a checkbox and CSV download button, then the table and expandable detail rows—using safe DOM text insertion throughout, with sorting that puts "Differs" rows first and an expand/collapse state tracked via a set of open row numbers.

Now I'm writing the parsing logic that walks through each PDF record's lines, detecting footnote markers, page numbers, and paragraph boundaries, including special handling for lines that are just digits matching expected page/footnote sequences near the start or end of a page's text.

For a lone number line that starts a footnote, I'll label it rather than merging it with the following line, keeping each footnote entry as a separate record tagged with its category.

I still need to handle headers that repeat the document symbol (like "E/C.12/GC/27") at the top of pages, and figure out whether page numbers might appear combined with that symbol on the same line — since the converter's output format here is uncertain, I should add a regex that catches standalone numeric lines as page markers too.

Then I'm setting up paragraph-start matching to build the current paragraph object with its number, page, and lines, pushing any remaining inline text, and finally assembling the output string per paragraph.

For comparison, I'm computing status by checking if the reference exists for each paragraph number and comparing first words, marking "no reference" when missing so the CSV can show yes/no/no-reference. I'm also planning footnote counts, a CSV filename derived from the symbol, and a detail row layout showing the full extracted paragraph alongside the reference's first words versus what the code found, with click-to-toggle rows.

