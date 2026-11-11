I'm going to build a complete app, aiming for around 600 lines and staying well under 1500. Next I'm laying out the pipeline, starting with the shape of the data: a pdf_text object holding a title, symbol, document URL, source, count, records, reference, and an optional built field that I'll need to handle when it's missing.

Now I'm working out how to classify each line by its page and kind. The header is the first non-empty line, which should match the symbol, or I flag a warning. For the footer, I scan from the bottom, skipping blanks, accepting "GE." lines, six-digit groups, and bare numbers up to three digits, where a number equal to the page number counts as the page number and anything else is treated as displaced. The loop stops at the first line that doesn't fit, so footnote text protects itself. Body lines are everything left over, blanks included, tagged with their page.

Now I'm setting up the labelled-heading case: when a line is a roman numeral or single capital followed by a period, I'll gather the lines after it, skipping blanks, up until the next label or the start of a paragraph.

Next I'm settling how labelled headings get collected: after a roman numeral or single-capital label, I gather the non-blank lines that follow until the next label or a paragraph start, then join them into the heading text. If a roman numeral is in the mix, I'll record the part from it.

Now I'm sorting out how to tell roman-numbered section labels from lettered subsections: a roman label starts a new part only if its value follows the last one, so a lone "I." can open the sequence while letters stay subsections.

Now I'm deciding how to tell lettered subsections from roman-numbered section labels: a roman label opens a new part only when its value continues the sequence from the last one, so the lone "I." can start it.

I'm deciding how to handle wrapped heading lines: rather than treating a capitalised line as the start of a new heading, I'll join every line between a label and the next label or paragraph start into one title with spaces, since the spec says titles can wrap over two lines.

Now I'm checking how unlabelled headings get picked out: a non-empty line counts only if the line right after it opens a paragraph, it's no longer than 90 characters, it starts with a capital, and it doesn't end in punctuation or a digit. I'm still unsure whether a cover line just before the first numbered paragraph could slip through that test.

I'm working out how to spot unlabelled headings after the first paragraph, and how to handle a two-line title that sits just above one. The previous line should be non-empty, capitalised, under 90 characters, and not end in a full stop, so I'll pull it off the current paragraph and join it to the heading.

I'm checking a edge case in the two-line heading test: a paragraph's final line normally ends with a full stop, so it fails the terminal-punctuation check, and a footnote marker ending in a digit fails the digit check too. I still need to confirm that a closing quote followed by a period also counts as terminal punctuation.

I'm checking the two-line heading case against footnotes: a footnote's last line could start with a capital, stay under 90 characters, and lack terminal punctuation, so it might get pulled into a heading by mistake.

I'm treating a line as a possible two-line heading only when the line before it isn't part of a suspect footnote run, so footnote text can't get pulled into a heading. To do that, I'll track on each page whether a suspect line has already appeared in the current paragraph and flag any later lines that match.

I'm settling how to suspect-track footnote runs on each page: the flag resets at each paragraph start so a false positive can't spill over into later paragraphs on that page.

I'm checking whether a candidate line that sits in a suspect footnote run should be ruled out as a heading, since a footnote's last line could be followed by a page's first paragraph start after the footer and header are stripped.

I'm checking the footnote case: the last footnote line before a new page's first paragraph could look like a heading, so I'll block any candidate that sits inside a suspect footnote run, since that run continues to the end of the page.

I'm checking whether a heading candidate sits inside a suspect footnote run before accepting it. The suspect state gets set from each line as I go through the paragraph, and I'll test the candidate against either that page-level flag or a fresh suspect check on the line itself.

I'm checking which lines count as footnote text, so I'll treat bare numbers and numbers followed by a capital as suspect markers, and mark each line that comes after one on the same page.

Now I'm writing the rules for spotting numbered footnote markers: a bare number, a number before a capital letter, or a number before an opening quote or asterisk. I'll check that a line starting with a number and a capital, like "7 E/2003/22", still counts as footnote text, and that a body line starting that way is left alone.

Now I'm working out what counts as a suspect footnote line: a bare number, a number followed by a capital or quote mark, or a line starting with an asterisk. I'm also planning to label each flagged line with the reason it was triggered, and to flag any paragraph over 300 words. I still need to decide whether a line beginning with a number and a space, like "23. text", should count as suspect.

Now I'm settling how to pick out the first words of each paragraph: I'll split the text on whitespace and strip any footnote numbers glued to the end of a word, keeping digits that belong to the token itself.

Now I'm settling the rule for stripping footnote digits from the first words of each paragraph: a trailing number counts as a footnote mark only when it follows a letter or closing punctuation, while references like "E/2003/22" and standalone numbers stay as they are.

Now I'm settling how to strip footnote marks from the first few words: a trailing number counts as a footnote only after a letter or closing punctuation, and abbreviations like "No." or "art." keep their numbers.

I'm settling how the checks get counted in the header: a check counts toward the total only if it passes or fails, while flagged items and checks that didn't run are noted separately, since a flag isn't a failure.

I'm now defining the checks for the report header: paragraph count, numbering order, and first-word matching against the reference, counting only pass or fail results toward the total.

I'm working through the header checks now: the paragraph count, numbering order, and first-word matching against the reference, with flagged items kept separate from failures. For the headers and footers, I'm checking that every page has a running header and that every page except the first carries a page number, and I'm weighing whether a number on page 1 should also count as a pass.

I'm laying out how each line gets tagged: every line starts with no kind, the header and footer lines get marked first, and the classifier then assigns a kind to each remaining line in one pass. After that I'll count the lines still left without a kind, so nothing gets silently dropped.

I'm settling the remaining checks: a round-trip export test that serializes the records and parses them back to compare lengths, and a count of hyphen-ended lines reported as an info item.

I'm laying out the tab structure now: tab 01 gets four summary tiles, the mismatch list, two download buttons, and two closed sections for every check and the flagged paragraphs. Tab 02 gets the paragraph rows, which expand to show the full text, plus a closed "Headings found" box.

I'm settling the table layout now: each row gets a button in the "No." cell with aria-expanded, and clicking the row toggles the detail beneath it, with the open state kept in a set so the table can be re-rendered on each toggle.

I'm now wiring up the expanded row view: each paragraph's lines are joined into one verbatim block, with suspect lines boxed in red, and a toggle that reveals the PDF's individual lines, marked wherever a new page begins. Clicking a flagged item will open its paragraph in the table, scroll it into view, and focus it. The rail sits in a fixed left column with the document summary and check totals, staying visible at narrower widths.

I'm setting up the downloads now: a JSON export of the records, plus a Markdown version with front matter that lists headings and paragraphs in document order, using a shared events list so each heading and paragraph lands in the right place.

I'm settling the record fields now: each one gets a `limitations` note counting the suspect lines inside that paragraph, plus `part` from the nearest roman heading and `section` from the nearest heading, with labelled headings keeping their label.

I'm working out how to build the path for each record: a stack of part, letter, and unlabelled headings, where a higher-level heading resets the lower ones, and the section is the last item in that path.

Next I'm setting up the "Headings found" box, listing every heading in order with its kind and page, plus the paragraph count, split into roman, lettered, and unlabelled groups.

I'm also planning the header summary, showing how many checks pass out of the total and how many paragraphs are flagged, and escaping all values so they are written as plain text.

For the reference, I'll fall back to an empty object when it's missing, and only treat the paragraph count as usable when it's actually a number.

I'm laying out the flagged-paragraph table on tab 01 with paragraph, page, suspect-line count, and the reason for each flag, and a click on a row will open that paragraph on tab 02. The table gets a short caption with a mono label. I'm also setting up the copy-citation button to fall back to a hidden textarea if the clipboard API is blocked, and I'm capping the mismatch list at ten lines.

Now I'm writing the lines loop that parses each page's text, with the page info kept alongside.

Now I'm writing the header and footer detection for each page: the first non-blank line is checked against the document symbol, and the footer scan starts from the bottom, skipping blank lines and stopping once it reaches the header.

Now I'm checking the footer lines for each page, looking for the document code or a bare page number, and noting when a page number matches the page or doesn't.

Next I'm writing the main loop that walks the body lines in order, tracking the current part, letter, and unlabelled heading, and starting a new paragraph record whenever a numbered paragraph begins.

I'm writing the code that handles the labelled headings: when a line matches a roman numeral or a single capital letter followed by a period, it gets marked as a heading and the following lines are gathered to complete it.

Still writing the labelled-heading collector: it keeps gathering the lines after a label until it hits the next label or paragraph start, and blank lines get skipped.

Now I'm handling the labelled headings, where the heading text runs on across the lines after the label. I'm also checking how a paragraph start is recognized, watching for footnote lines that might look like numbered paragraphs.

Still writing the body loop: it skips blank lines and checks whether each remaining line could be a suspect start, then decides if it is a heading-like line before adding it to the current paragraph.

Still working through the paragraph-start logic: when a heading-like line sits just before a numbered paragraph, I'm checking whether the line above it should be folded into the same heading, and then recording the heading in order.

Still working on the paragraph-start logic: I'm checking whether a heading-like line just above a numbered paragraph should be folded into that heading, and whether blank lines between the heading and the number need to be skipped too.

Still working out the heading check: I'm weighing whether to skip blank lines when looking for the paragraph number that follows a heading-like line, since the layout puts the number on its own line.

Now I'm checking whether a line that looks like a heading comes just before a numbered paragraph, skipping any blank lines in between to find that next line. If the line right above it is also heading-like, it gets folded into the same heading.

Still working on the suspect-line checks: each paragraph line gets flagged when it looks like a footnote or stray marker, such as a bare number, a number followed by a space and a capital, or a leading asterisk, and the reason is recorded with the line.

Now I'm checking the footnote-style suspect lines and how a paragraph ends when a page break splits it: the continuation on the next page isn't suspect, so its text just joins the paragraph.

Still working on how each paragraph's page range is set: I'm weighing whether to use the page of the first text line or the page of the paragraph number, since they can differ when a number sits at the bottom of a page.

Now I'm settling the rendering approach: the page is built from static markup filled in by script at load, and each state change, like toggling a row or switching tabs, re-renders only the affected panel and puts focus back on the matching element.

Still writing the tab 01 markup: four tiles in a grid covering paragraphs found, first-word matches, flagged paragraphs, and footnote separation, each with its own how-computed note. Next comes the mismatch list and the takeaway section with its two heading buttons.

I'm settling how each check reports its result: a pass or fail status, a link to the rows it covers, and a "not run" or "for information" label where a check doesn't apply. Then I'll count the passing checks for the header and rail, add a download button, and wire up tab keyboard navigation.

Now I'm rendering each paragraph row, marking it with a check note: "first words differ" if the opening words don't match the reference, "may contain footnote text" if it was flagged, or "not compared" when there's no reference to check against. The expanded detail shows the file path, the text with suspect lines highlighted, and the reference's first words for comparison.

I'm finishing the export section now: each record gets its symbol, paragraph number, section, part, page range, text, flags, match result, citation, and document URL, plus the joined line text that the export also carries. A built field only goes in when the source data has one.

Now I'm checking the numbering: each paragraph should follow the one before it, and any gap or repeat gets recorded with its page. For the match checks, I'm collecting the paragraphs whose opening words differ from the reference, and the reference numbers that never showed up in the document.

I'm checking the export round trip next, building the records and confirming the parsed JSON has as many entries as the paragraphs. Then I'm counting lines by kind to make sure every non-blank line is classified and none is left unassigned.

Writing out the full code now, with the tab panels rendered from shared functions and a single delegated listener handling every action.

Still writing the table rows: a row is clickable as a whole and carries the same action as its first-cell button, while the expanded detail row has no click action of its own so text can be selected.

