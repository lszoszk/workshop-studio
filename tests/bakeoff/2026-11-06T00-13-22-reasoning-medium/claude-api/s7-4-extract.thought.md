I'm sketching out a full app that should land around 600 lines, well under the 1500 ceiling. The WORKSHOP_DATA.pdf_text field could be either an array of records or an object, so I'll handle both cases defensively. Next I'm thinking through how the pages get sorted and split into lines.

I'm working through the page-processing logic now: finding the header line that matches the symbol, peeling footer lines like the GE stamp and bare page numbers off the bottom, and checking the page number against the page index. Body lines get stored with their page and kind, and I'm stepping through them with a state machine that starts in the cover section.

I'm settling on a cover section that runs until the first labelled heading or paragraph start, and I'm noting that the page 1 footnote beginning with "* Adopted by the Committee" attaches to the last paragraph on that page. Next I'm planning a first pass that flags paragraph-start lines and roman or single-letter heading labels, keeping the two patterns separate since a paragraph start always begins with digits.

I'm defining the heading logic: when a lettered label appears, I collect the following lines as heading text, skipping blanks and stopping at the next label or paragraph start. Lines that wrap get joined, though I'm still weighing whether an unlabelled title line right before a paragraph should be absorbed into the heading.

I'm working out how to join the heading lines: a plain space join across the wrapped lines, since the page footers are already stripped out so there's no stray content to worry about. I'm also deciding the heading levels, with roman labels as parts and lettered ones as sections, and building a section path that combines the current part with the current heading.

I'm working out how to tell heading lines apart from paragraph text: a lettered or roman label starts a heading, and its lines run until the next label or paragraph start. Before the first paragraph, anything that isn't a labelled heading counts as cover material.

I'm now working out how to tell a heading's wrapped lines apart from an unlabelled title sitting just above a paragraph start. The plan is to treat a short line that begins with a capital and has no closing punctuation as a possible heading, and to check whether the line before it still belongs to the current paragraph before pulling it out.

I'm weighing whether to check the previous line for a paragraph tail before pulling a capitalised, unpunctuated line out as a heading. Plain lines of roughly 95 characters are common in this text, so the length cutoff alone may not be a reliable signal.

I'm checking the paragraph-start rule: a line counts as an unlabelled heading only if it has more than one line in the current paragraph, so I don't leave an empty paragraph behind. A number-alone line like "5." never qualifies because it has digits and a period. I'm also weighing how a heading that falls across a page break should be handled.

I'm weighing whether a footnote line sitting right before a paragraph start on the next page could be mistaken for an unlabelled heading. Footnote text often begins with a capital and lacks closing punctuation, so I might exclude lines that look like footnote starts.

I'm adding a same-page check to the unlabelled-heading rule, so a footnote line at the bottom of one page can't be mistaken for a heading that sits just above a paragraph start on the next page.

I'm working out how to decide which lines are suspect footnote starts: a bare number, a number followed by a capital or quotation mark, or a line beginning with an asterisk. Once one of these shows up on a page, I'm treating the remaining lines on that same page as suspect.

I'm checking which lines can be treated as suspect footnote starts: a bare number, a number followed by a capital or quotation mark, or a line beginning with an asterisk. Once one of those appears on a page, every later line on that same page gets marked as suspect, since footnote blocks run to the foot of the page.

I'm marking suspect footnote lines by tracking a suspect page: once a line on a page looks like a footnote start, every later line on that same page gets flagged, and the flag resets when the page changes.

I'm checking that a heading's line sits on the same page as the paragraph start that follows it, so a footnote's last line at a page foot doesn't get mistaken for a heading. I'm also noting that a heading split across a page break is a rare case I'll leave alone.

I'm settling on how to handle a labelled heading followed by an unlabelled title line: the first title line stays with the labelled heading, and any continuation lines get joined onto it.

I'm weighing whether a capital-start line after the first heading line should count as a separate heading or as a wrapped continuation of the title. The spec's wording points toward treating it as its own heading, but a title that wraps onto a second capitalised line would then be split wrongly, so I'll flag those cases for checking in the headings list.

I'm settling the heading rule: a capital-start line after the first heading line becomes its own heading, but I'm flagging cases where a wrapped title might be split that way.

I'm checking how the first words of each paragraph are pulled out, which means stripping footnote marks from the tokens, and then working through the abbreviations that a trailing number mustn't be mistaken for a mark on.

I'm working out how to strip footnote marks from the first words of each paragraph: a trailing number glued to a punctuation mark or word gets cut, but I need to skip abbreviations like "No." or "art." so their periods aren't mistaken for marks.

I'm checking how the footnote-mark stripping handles tokens that end in digits, so that things like "A/HRC/57/61" or "(2025)" stay intact while glued marks on words or punctuation get cut.

I'm checking how the first words get compared against the reference, normalising curly quotes, dashes and whitespace on both sides before matching. Paragraph text is built by joining its lines, with any paragraph over 300 words flagged, and suspect starts are recorded with the reasons they were triggered.

I'm settling how the paragraph text and its page markers get built for the toggle view: each paragraph's start page comes from its number line, its end page from the last line, and the view shows the number line first, then the lines with page markers wherever the page changes.

I'm laying out the expanded paragraph view: the lines get joined into running text, and any suspect line is wrapped in a red-outlined span so it stands out. The flagged-paragraphs table will show the paragraph, its page range, the suspect lines and the reasons, and clicking a row jumps to that paragraph on the second tab. Last, I'm setting up a list of checks, each with a title, a status and the rows it links to.

I'm settling the checks list: each check gets a title, a status, and a link button that jumps to the relevant rows, with the flagged-paragraph count shown as a note to verify rather than a failure. The summary line will count only the checks that actually pass or fail.

I'm settling the checks: the header and footer check passes only if every page except the first carries a page number, and I'm weighing how to count the total so that info-only items like the flagged paragraphs and headings stay out of the pass tally.

I'm laying out the rest of the interface: the summary numbers sit in a side rail that stays visible, and on narrow screens the rail stacks above the content. The second tab will hold a table of the paragraphs, and I'm keeping the number of clickable controls small, with link buttons only on failed checks.

I'm laying out how the paragraph table will work: each row gets a number button that expands a details row, and I'm putting a collapsed headings box above it that lists each heading's label, text, kind, level and page. Each first-line preview will be cut at about 120 characters on a word boundary.

I'm working out the expanded paragraph view now: the text gets shown as running text with each suspect line wrapped in a red-outlined span, and I'm planning a toggle to show the PDF's lines, a copy button for the citation, and downloads in JSON and Markdown, with the Markdown keeping headings and paragraphs in document order.

I'm working out the export fields now: the front matter takes today's date, the source URL and the adopted date from the reference, with the expected paragraph count falling back to "unknown" when it isn't given. For the JSON records I'm settling on the paragraph's identifying fields and page range, along with its text and the original lines, and I'm working out how the Markdown version keeps headings and paragraphs in document order.

I'm settling the JSON record fields and the Markdown layout, leaving paragraph text as is and skipping the duplicate raw-text field. Empty sections will export as blank strings, and downloads stay disabled until there are paragraphs. For the dataset, I'll treat the input as either an array of records or an object, sort the records by page, and use the document title for the header and rail.

I'm checking the header and footer handling next: the first non-empty line has to match the symbol, and the footer trimming drops empty lines, bare page numbers and document codes from the end of each page.

I'm laying out the parsing step: each page's lines go into one flat list with their page numbers, empty lines kept but ignored, and I'm counting the non-empty ones. Then the main loop walks that list by index, checking whether the next line starts a new paragraph on the same page.

I'm writing the parser loop now: it walks the body lines by index, skipping empty ones, and when a line matches the label pattern it marks it as a heading and starts collecting the continuation lines that follow.

I'm defining the heading parser now: when a line matches the label pattern it becomes a labelled heading, and the lines that follow that don't start a new paragraph get folded into its text, with lowercase or parenthesised continuations joined onto the previous part.

I'm now deciding how to tell a Roman-numeral heading from a letter subsection when both use single-letter labels like "I", "V" or "X". I'll track the last letter label, so that an "I." right after "H." reads as a letter and not as a Roman numeral, then keep parsing the body lines.

I'm setting the paragraph-start detection: a bare number like "1." or a number followed by text starts a new paragraph, and I'm skipping footnote-style numbers that don't have a dot. I'm also starting each paragraph record with its number, page, section and part, plus an empty list of lines to fill in.

I'm now handling the case where a line looks like a continuation of a heading rather than a new paragraph, folding it into the previous part when it belongs there, and checking the page boundary before doing so.

I'm working out how to tell apart a heading that wraps onto the line before a new paragraph. The previous line only joins the heading if it sits directly above on the same page and doesn't end a sentence, so a full stop at the end of the earlier paragraph keeps the two separate.

I'm checking how unlabelled headings get attached before a new paragraph, and whether a line that looks like a heading sits directly above it on the same page. The earlier heading-detection is what I'm now fixing, since a two-line heading wrapping onto the line before a paragraph still needs its first part folded in.

I'm finishing the paragraph-finalizing step: once the loop ends, each paragraph's lines get turned into text, with suspect marks carried over where a page changes.

I'm working out how to tell apart a heading that wraps onto the line before a new paragraph, and how to mark suspect lines and hyphenated endings for the paragraph's final text.

I'm laying out the stats for the paragraph count, with each tile showing its figure and how it was worked out. The rail bar fills by found over reference, capped at full width, and turns red whenever the two counts don't match.

I'm checking the first-words comparison now: a paragraph counts as matched only when the reference has a first word for it and the two are equal. Anything unmatched, including paragraphs missing from the reference and reference paragraphs never found in the document, goes into the mismatch list.

I'm laying out the tab-one tiles: paragraphs found against the reference count, first-word matches with a mismatch list that gets capped at ten lines, and a flagged-paragraphs count across pages. Each mismatch will link to the paragraph it concerns through an `openPara(n)` helper, which switches to the paragraph tab and scrolls to the row.

Next I'm defining the small DOM helper h(), which builds elements, sets classes and text, and wires up event handlers from an attributes object.

Writing the checks list next, starting with the paragraph count and the numbering check, which walks the paragraphs in order to catch gaps or repeats.

I'm now going through the checks in order: paragraph count, numbering, first words, then flagged paragraphs. The header and footer rule and the nothing-lost check are next. I still need to settle the counting rule, since the total check number is inconsistent between the list and the heading.

I'm settling on how to count the checks: the heading will show how many pass or fail or didn't run, with the informational notes listed separately and not counted.

I'm adding a notes section below the counted checks, and for the round-trip check I'll build the export JSON once at load. For the flagged-paragraph limitation I'm writing the footnote caveat with the suspect-line count, so a paragraph with suspect lines reads as having footnote text possibly inside it.

I'm now laying out the tab-one tiles and the check list. The paragraph-count and first-word tiles compare against the reference, and the mismatch list is capped at ten lines. Each flagged row will get a button that jumps to its paragraph.

Still writing the row rendering code...

Still writing the row detail code...

Still writing the paragraph-parsing helpers...

I'm now writing the function that cleans up the first words of each paragraph, a short helper that splits the text and keeps the first handful of words.

Still writing the word-cleanup helper, which stops at six words and drops stray footnote numbers glued onto words.

I'm checking how the cleanup helper treats leading digits and abbreviations like "No." or "article", so that real content numbers survive while stray footnote markers get dropped. Then I'm making sure every non-empty body line gets tagged as cover, heading, or paragraph, and that a header line only counts as a header when it matches the symbol.

I'm checking the remaining cover-line and page-number logic, and I'm writing the final markup for the rail, header status dot and window title.

I'm finalizing the compose step now: the remaining work is to write the full app carefully, keeping it under the length ceiling.

