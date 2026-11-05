I'm designing a complete app under about 1500 lines. The data is a WORKSHOP_DATA.pdf_text object with a title, symbol, doc URL, source, count, records, reference, and an optional built field. I'm now planning a pipeline that starts by sorting the records by page and splitting each page's text into lines, classifying the header and footer lines.

Now I'm working through the footer rule: from the end, dropping blank lines and lines that start with "GE." or match the six-digit or bare-number patterns, and stopping at the first line that doesn't match. Bare numbers equal to the page number count as page numbers, and any others get tracked as displaced. Next I'm setting up the body array of page-tagged lines, keeping blank lines so headings can be parsed.

Now I'm writing the parse loop: for each line, a blank gets skipped, a paragraph-start line opens a new paragraph, and a roman or single-letter label opens a heading that collects lines until the next label or paragraph start.

I'm settling how a heading gets its title: after the label, I'll skip blank lines, take the first non-blank line, and keep joining consecutive non-blank lines until a blank, another label, or a paragraph start stops the run. I'm accepting the risk that an unlabelled heading with no blank line before it could get glued onto the title.

I'm settling the heading title rule: after the label, take the first non-blank line as the title and keep joining following lines only while they start lowercase or with "(". Anything else ends the title and goes back to the main loop.

I'm weighing whether a heading's level should come from the label alone. Roman numerals mark parts and single letters mark subsections, but a lone "I" or "V" could be either, so I'm leaning toward treating it as a roman numeral whenever it matches the roman pattern, since letter subsections rarely reach those letters.

I'm settling how an unlabelled heading gets recognized: a line short enough, starting with a capital and not ending in punctuation, counts as a heading only when the paragraph start follows it directly, or when a second such line sits between it and that paragraph start.

I'm checking the unlabelled-heading rule against the paragraph's last line: a line that ends with a period fails the test, so a heading can't be mistaken for the end of a sentence. The worry I'm still weighing is a paragraph line that ends in a footnote digit and doesn't carry a period.

I'm checking the two-line unlabelled heading pattern first, since a line that passes the heading test and is followed by another such line and then a paragraph start would be a two-line heading. A single line followed directly by a paragraph start is the other case. I'm worried about a previous paragraph's last line that starts with a capital and lacks a full stop, which could be mistaken for a heading, but I'm accepting that as a rare edge case.

I'm checking the cover case: lines before the first paragraph start, where a heading test could fire on title text. I'll apply the unlabelled-heading test only once a paragraph has started, since the cover lines lead into the labelled headings anyway.

I'm now deciding what a paragraph record holds: its number, its lines with page and suspect flags, and its section, part, and section path. For a labelled heading I'm keeping the title alone for the section name, and building the full path from the part's label and title.

I'm now deciding how section names and paths get built: labelled headings keep their label in the name, sub-headings reset the unlabelled level, and the paragraph's path is the stack of part, subsection, and unlabelled heading. Next I'm defining the suspect-line test for stray page-number and footnote-like lines, marking such a line and every later line on the same page as suspect.

I'm now defining what counts as a suspect line: any line starting with a bare number of one to three digits followed by a capital letter, quotation mark, or asterisk, which would catch stray footnote or page-number text. I'm accepting that a paragraph line beginning with a number and then a word might get flagged, and I'll mark that line and every later line on the same page as suspect.

I'm working out how footnotes at the foot of a page get attached: a bare number on a page marks the start of suspect lines, and everything after it on that page is flagged. A paragraph split across a page break keeps its continuation on the next page unflagged. The open question is a footnote block that lands after a completed paragraph, right before a new page starts with a heading, since those footnote lines would end up attached to the previous paragraph.

Now I'm working through the flagging rules: a paragraph gets flagged when it is over 300 words, and its suspect lines are listed with the reason, such as a leading number, a bare number, or an asterisk. I'm also deciding how the text fields are built from the lines, joining them with spaces and collapsing extra spaces, while keeping a raw version that preserves line breaks.

Now I'm working out how to normalize the text, splitting it into words and dealing with digits glued onto the end of words or punctuation.

I'm deciding how to handle digits glued onto words or punctuation when normalizing the first words of a paragraph. The pull is toward cutting digits after punctuation like "waste.2", but cutting after letters risks breaking tokens such as "G20". I'm leaning toward cutting only after punctuation, since that's the case I need, and accepting that a few letter-digit words stay intact.

I'm working out how to normalize the first words of a paragraph: cutting digits glued to the end of a lowercase word or punctuation mark, while leaving things like "G20" alone. I'll drop a stray digit after a sentence-ending mark unless the word before it is an abbreviation such as "No." or "art.", then compare the first six normalized words after normalizing quotes and dashes.

I'm settling on how to report the checks: each one gets a pass, fail, or info status, and the header counts only the pass and fail ones. Right now I'm deciding whether checks that can't run should count toward that total.

I'm settling on how the checks report their status: a check is either a pass or a failure, and the info-style lines for flagged paragraphs and suspect lines are being weighed as to whether they should count toward the total.

I'm deciding how to show the check results: whether notes count toward the total, and whether the header should use the number of scored checks or every line. I'm leaning toward keeping flagged-paragraph and suspect-line entries as separate notes, not scored checks, and counting only the pass, fail, and not-run statuses in the "n of m checks pass" header.

I'm setting the checks to run against the reference counts: total paragraphs, numbering with gaps or duplicates, the first-words comparison, and header and footer page coverage. The flagged paragraphs and suspect lines will show up as notes rather than scored checks.

I'm now setting up the remaining checks on the rewritten parse: a numbering-free paragraph count, header and footer page coverage, and a tally of bare numbers and unlabelled headings as notes. The last one is a classification check that every non-empty line lands as header, footer, or body, so nothing is lost.

I'm setting up the last checks: a round-trip test that the exported records parse back to the same count, and a tally of hyphenated line endings noted without joining them. I'm also planning the summary rail with the document's symbol and a shortened title.

I'm now laying out the results view: a 2x2 grid of four summary tiles, a list of mismatches, and two buttons for taking the findings away. Below that I'll add two collapsed headings for the full check list and the flagged paragraphs, with tabs and arrow-key navigation.

Now I'm setting up the second tab's table: each row gets a button in the number cell that toggles an expanded detail row beneath it, with the whole row also clickable.

I'm now working out the paragraph detail panel: each paragraph shows its full path and text as one block of running text, with suspect lines marked by a thin red box. I'll also give it a toggle to show the raw PDF lines, with a page-start marker wherever the page changes, plus a copy-citation button, and let flagged rows open in the second tab with a link from each check to its rows.

I'm adding the link buttons for the flagged paragraphs, up to five per check, and then listing the mismatches under the tiles with a "and n more" tail. For exports I'm planning a JSON download and a Markdown one, with each paragraph carrying the headings that came before it so the Markdown keeps document order.

I'm settling how the export and flag details work: each paragraph gets the headings that came before it so the Markdown keeps document order, the extraction date is today's, and exports are disabled when there are no paragraphs. For the flag reasons, I'm mapping each suspect line to a plain label: a bare number, a leading number and space, an asterisk, or a paragraph over 300 words.

Writing the pipeline setup code...

I'm setting up the header and footer detection for each page: the first non-empty line is checked against the document symbol, and pages where it doesn't match get flagged as warnings.

Still writing the footer detection loop...

Still writing the parser setup: I'm defining the paragraph-start check, which matches a number followed by a period at the start of a line.

I'm deciding how to detect the header and footer lines in each page, and how to decide whether a line starts a numbered paragraph. A paragraph start is a number followed by a period at the beginning of a line. I'm also considering how to recognise lettered or roman headings and which lines count as plausible headings.

Still writing the paragraph parser: I'm stepping through the body lines and checking each one for a numbered start, which I'll track as the current paragraph while collecting the continuation lines beneath it.

Still writing the paragraph parser: I'm defining the paragraph-start pattern and the label lines, and collecting the heading text that follows each label.

Continuing the heading detection: a labelled heading is built from its label and wrapped title lines, with roman labels starting a new part and letter labels a subsection. Unlabelled headings are then checked as either a two-line or a one-line title sitting right before a paragraph start.

Still writing the paragraph parser: I'm checking whether a candidate title line is followed by a paragraph start, so the unlabelled-heading test looks at either one line or two before it.

Still writing the paragraph parser: I'm setting each paragraph's section to the current heading and its path to the part, subsection and unlabelled heading joined together, and holding the headings seen before it so they can be listed in order.

Still writing the paragraph parser: once a paragraph's lines are collected, I'm scanning each one for a suspect reason and tagging it. A flagged line marks the rest of its page as suspect, and a new flag on a later page starts over.

Still writing the suspect-reason check: a bare number or a number followed by a capital or quote mark gets its own flag label, and I'm framing the rest of the regex as I go.

Still writing the export and Markdown output: each paragraph carries its path and the headings before it, and I'm building the record for the Markdown view.

Still writing the Markdown export: I'm building the front matter and heading structure, with each paragraph listed under its headings in document order.

Now I'm laying out the four summary tiles: the paragraph count against the document's stated total, the first-word matches against the reference, the flagged count across pages, and the footnote note. Each checks list row will carry a name, the expected statement, the actual values, and a pass or fail mark.

Now I'm wiring up the paragraph rows so each one can expand in place. I'll toggle the detail row directly in the DOM, building it the first time it opens, and each expanded row gets a button that shows or hides its raw PDF lines.

Still writing the detail view: each paragraph's text is built from its lines with suspect ones highlighted, and the raw PDF lines are listed with page-start markers.

I'm working out how the flagged-paragraph table will look: each row gets a button that jumps to that paragraph, and the caption states the count in a serif line with the number in monospace. I'm also sorting out the table numbering, since the flagged table and the paragraph table need distinct labels.

Still writing the detail and checks logic: I'm adding the headings-found list, the bar that turns red when the counts differ, and the empty-state messages, then computing which first-word matches fail.

Still writing the numbering checks: I'm looking for duplicate paragraph numbers and any gaps in the sequence up to the highest number found.

Now I'm writing the rest of the page layout: the tile styles, the status dots, and the render functions for the second tab, which starts its paragraph table.

Still writing the paragraph table: each row has a number button that expands the detail in place, a section column, page range, and a first-line preview cut at a word boundary past 120 characters. The check column flags footnote-suspect paragraphs and first-word mismatches.

Still writing the event handling and the checks: I'm wiring click delegation for toggles, jump links, and rows, and assembling each check entry with its name, expected statement, values, and status.

I'm finishing the status logic for the rail: if any checks fail the dot goes red with a count, otherwise it shows how many checks pass, with a neutral dot when some haven't run. I'm also adding a note about hyphen handling and a round-trip check that parses the exported records and compares their count against the paragraphs found.

