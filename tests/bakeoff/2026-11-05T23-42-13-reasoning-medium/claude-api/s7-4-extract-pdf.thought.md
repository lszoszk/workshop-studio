I'm planning a large HTML document and sketching the data shape first: a PDF text object with title, symbol, doc URL, source, count, records, reference, and an optional "built" field that may be missing. Next I'm going to set up the processing pipeline, starting with sorting the pages and classifying each line as a header, footer, or body.

I'm classifying the lines on each page, with the cover and heading lines before the first paragraph, and the footnote lines inside the paragraphs. The header is the first non-empty line matching the symbol, and the footer is read from the end: "GE." lines, 6-digit groups, or a bare 1-3 digit number, stopping at the first line that doesn't match. A bare number that matches the page marks the page number, and any others get set aside.

I'm working out how to treat the suspect lines on each page: once one is flagged, every later paragraph line on that page gets flagged too, and I'm resetting that state per page, since a new paragraph shouldn't start after the footnotes anyway.

I'm making sure the suspect check runs before heading detection, since a footnote line at the bottom of a page could otherwise be mistaken for an unlabelled heading. Lines with a suspect flag, or that sit in a page's footnote block, won't be treated as headings, even if they start with a capital, are short, and lack ending punctuation.

I'm adding a pre-pass that tracks, per page, whether a footnote-like line has appeared after the first paragraph start, and marks everything after it on that page as footnote territory. Heading detection will then skip those lines, so a footnote fragment can't pass for an unlabelled heading. Since footnote blocks sit at the foot of each page, the real headings on that page come earlier and are unaffected.

I'm working out the cover detection: lines before the first heading or paragraph start count as cover, and I'm checking that a bare "I." heading isn't mistaken for cover text.

I'm settling on the heading format now: after an "I." or "A." style label, blank lines get skipped and everything up to the next label or paragraph start counts as heading text. A line starting lowercase or with "(" is treated as a wrap of the line before, so the heading ends up joined into one string.

I'm weighing whether to stop heading text at a blank line, since otherwise an unlabelled heading right after a labelled one could get swallowed into it.

I'm settling on the wrap rule for heading text: a blank line ends the heading once text has started, unless the next non-blank line begins lowercase or with "(", in which case it continues the title. The open question is whether a heading running onto a page boundary, with footnote lines between, causes trouble, and I'm leaving that edge case aside for now.

I'm settling how unlabelled headings get picked out: a non-empty line counts as one if the next non-empty body line is a paragraph start, with blank lines allowed in between. The guard against footnote text is that it can't end in punctuation, must start with a capital, and stays under 90 characters.

I'm adding a check so that a line ending in a closing quote after a period, like `.”`, doesn't pass as a heading line, since it still reads as the end of a paragraph sentence. Headings such as "Right to work (art. 6)" end without that kind of closing punctuation, so the exclusion leaves them alone.

I'm now settling the two-line heading case: a line that comes right before a heading candidate and passes the same test would be joined with it, but if it is really a paragraph's last line, it has already been added to the body. So I need to look ahead before assigning lines to paragraphs.

I'm checking each line for heading candidates by looking at the next non-empty line: if it's a paragraph start, the line counts as a heading, and if the pair before a paragraph start both pass the same test, they get joined into a two-line heading. The lookahead has to happen before lines are assigned to paragraphs, otherwise the first line would already be in the body.

I'm settling the heading boundary: a candidate line is only a heading if it doesn't end in a period, so a real paragraph's closing line can't be mistaken for one. The two-line case works the same way, with the lookahead done before lines are assigned to paragraphs, and the page's first body line after a break is safe because the previous page's lines are already in the footnote zone.

I'm settling the two-line heading case: if a line passes the heading test and the line after it does too, with a paragraph start following, the pair is joined into one heading. The first line can't be checked on its own, since its next non-empty neighbour isn't a paragraph start, so the two-line check has to run for it too. I'm also checking whether the order matters, and whether a real paragraph's last line could slip through when the next line also passes.

I'm checking the two-line heading case from the other direction: if the first line ends mid-sentence, it can't be a heading, and the second line only continues a paragraph that is still open. I'll also label headings by their level, treating a Roman numeral label as a part and a letter label as a subsection, with the most recent heading of any kind counting as the current section.

I'm settling how the heading path gets built: a roman-numeral label marks a part, a letter label a subsection, and an unlabelled heading sits at the bottom of that stack. Each heading then records its level, label, text and the paragraph it precedes, so the Markdown export can emit them in document order.

I'm working out how to handle lines that fall outside the cover and paragraph phases: an unlabelled heading gets recorded with the index of the next paragraph, and I'm still deciding where a stray body line goes when no paragraph is open yet.

I'm marking which body lines might be footnote text by scanning the page in order, and any line that matches the footnote pattern after the first paragraph starts sets a flag for the rest of that page. Lines inside that flagged zone get a suspect marker, and I'm handling label and heading lines separately, since the footnote zone can't cover them.

I'm reconsidering whether a regex for paragraph starts like "N. text" is safe, since footnote lines might also begin with a number and a period. I'm inclined to reset the footnote zone whenever a real paragraph start appears on the page, and to accept a small risk from footnotes that happen to begin with a number and a full stop.

I'm settling the suspect-line regex for footnotes: a bare number on its own line counts, and so does a number followed by a capital letter or a quotation mark, since footnote text usually opens that way. A footnote starting with a digit after the number could slip past this pattern, but it would only matter if an earlier trigger had already opened the zone.

I'm checking the suspect-line pattern against real paragraph starts, so a bare number or a number followed by a capital or quote marks footnote text, while a wrapped line that happens to begin with a number and capital stays in the body.

I'm settling the flagging rules now: a page gets flagged when one of its paragraphs has a suspect line, with the reason recorded, and paragraphs running past 300 words get marked on their own. I still need to decide whether those long paragraphs also put their page into the flagged-pages table.

I'm deciding whether a page gets flagged for review: if a page has a suspect line, it's flagged, and paragraphs over 300 words are marked too. I still need to settle whether a long paragraph with no suspect lines should add a row to the flagged-pages table.

I'm deciding how to flag pages for review: a page gets flagged if it has a suspect line inside a paragraph, and also if an over-300-word paragraph starts on it, so those long paragraphs still show up in the table.

I'm checking the flagging logic against the pre-pass: a paragraph start is a line like "N." with nothing after it, and the open question is whether to skip treating a number line as a paragraph start while the footnote zone is active, to avoid false positives.

I'm weighing whether to reset the footnote zone at each paragraph start or to leave it set, since a false trigger mid-page could otherwise hide real paragraphs. I'm keeping the reset, because a stray footnote like "3." is the smaller risk.

I'm weighing whether a false trigger partway through a page could hide a heading that sits before the next paragraph start, since the footnote zone would still be active at that point. Resetting only at paragraph starts means a stray match could swallow real headings, so I'm considering a narrower exception for heading lines.

I'm treating a heading as a candidate only when it isn't a footnote-zone line sitting at the end of its page. So the check is: skip it if the zone is active and the next line is on a different page. That keeps real headings on the same page as the next paragraph start from being lost.

I'm settling how each paragraph's text gets assembled: the lines are joined with single spaces and trimmed, with page markers inserted where the page changes, and suspect lines wrapped in a marker for display. I'll also count words per paragraph and derive a short leading-token preview with trailing footnote digits stripped.

I'm now checking whether a digit glued to the end of a word is a footnote mark or part of the word itself, like "COVID19" or a reference such as "E/C.12/GC/27". I'm thinking about limiting the cut to digits that follow a period, comma, quote, or bracket, or a letter.

I'm settling the digit-cutting rule for the first words: a footnote digit gets stripped only when it's glued to a letter or closing punctuation, so references like "GC/27" stay intact. I'm also deciding that a standalone number right after a word ending in a full stop, comma, or closing quote gets dropped, unless that word is a common abbreviation like "No." or "art."

I'm checking how the first words get trimmed: footnote digits glued to a word or punctuation are stripped, but a standalone number after a sentence-ending mark is dropped unless the preceding word is an abbreviation like "No." or "art.". I'm also normalizing curly quotes and dashes before comparing the first six words against the reference text.

I'm settling how the checks get tallied: each one is either a pass, a fail, a note, or not run. Notes such as flagged pages are information rather than failures, so they stay out of the count. The header and the rail will both read "n of m checks pass", where m only includes the checks that can pass or fail.

I'm settling how the checks get tallied: a check that can't run stays out of the count, and the flag-type notes are shown as information rather than passes or failures. For the paragraph count I'll compare what I found against the reference total, and for numbering I'll walk the sequence to catch gaps and duplicates.

I'm working through the remaining checks: flagging the first-words mismatches (with no reference entry counting as a mismatch) or marking the check as not run when there's no first-words data, then noting the flagged pages and suspect lines as information. For headers and footers I'm checking that every page has a header and that page numbers appear on all but the first page, listing anything displaced, and I still need to decide where to report hyphen-ended lines.

I'm settling the last checks: a line-ending note that counts hyphen-ended lines without joining them, a heading note that lists any unlabelled ones, and a "nothing lost" test comparing the raw non-empty line count with the sum of classified lines. I'll also round-trip the export JSON to confirm it keeps every paragraph, and show the footnotes and the progress bar against the reference totals.

I'm laying out the results view with two tabs, keyboard arrow navigation between them, and a fixed side rail beside the main column that stacks on narrow screens. The first tab will hold a 2x2 grid of summary tiles, a list of mismatches, and a takeaway section.

I'm settling how the flagged-pages table works: each page number becomes a button that expands a detail row showing that page's raw lines, with the suspect ones highlighted and the paragraph they belong to.

I'm writing the parse step now, reading each page's records and tagging every line with its page and index so the later checks can refer back to them.

I'm writing the parse step: each page's records are split into lines and tagged with their page and index, and I'm checking whether the first line matches the document symbol to mark it as a header.

I'm now writing the footer pass: walking up from the bottom of each page, I mark blank lines, the document code line, and bare page numbers as footer lines. Any page number that doesn't match its own page gets recorded as displaced.

I'm working out how the footer lines get marked, including blank lines inside the footer zone, and how body lines are told apart from headers and footers.

Now I'm wiring up the parse step: each page's text gets split into lines, and a line that matches the document symbol is marked as a header. Next I'm defining the patterns for paragraph starts and labels, and a check for suspect lines like bare numbers or lines opening with a stray asterisk.

Still writing the parse pass: I'm setting up the pre-pass that tracks whether the paragraph list has started, and I'm treating a Roman numeral or capital-letter label as a section start too, so the cover text before it is kept apart.

I'm finishing the classification pass, marking lines in the zone after a paragraph start as suspect if they look like bare numbers, numbered labels, or stray asterisks, and then starting the main loop that builds the paragraph and heading lists.

I'm laying out the main loop that walks the body lines and starts a paragraph whenever a numbered line appears, with a separate pass that picks out the section labels.

I'm writing the main loop that walks the body lines, starting a new paragraph at each numbered line and recording its section, while Roman or capital-letter labels begin heading blocks.

I'm writing the heading loop now: when a label line appears, I collect the text after it, skipping blank lines when the next line continues the sentence, and stop at the next paragraph start or label.

I'm now handling the heading lines: when a label appears, I gather the text after it, skipping blank lines when the sentence carries on, and stop at the next paragraph start or label.

I'm now writing the unlabelled-heading check: a line that looks like a heading and is followed by a numbered paragraph start is treated as a heading, with a two-line variant for headings that wrap onto a second line.

I'm defining the two-line heading check: a line counts as a heading if it passes the heading test, isn't suspect, and isn't a stray zone line from another page. The next step is to confirm the following line is also a heading candidate and that the paragraph start comes right after, with the line directly beside it.

I'm working out how the unlabelled headings get picked out and how a paragraph's last line is kept apart from a heading. The plan is to treat a line as a heading when it's followed by a numbered paragraph start, and to keep lines that run on without a full stop inside the paragraph.

I'm finishing the paragraph step: joining each paragraph's lines into text, keeping the raw line breaks alongside, and recording the page where it starts and ends. I'm also counting suspect lines and flagging any paragraph with suspects or over 300 words, and I'll handle the section path next.

I'm finishing the flagged-pages logic: each suspect line gets recorded against its page along with the reason it was flagged, which is the part still being written.

I'm working out the final checks, mainly whether the header and page-number tests should cover every page or all but the first, and how the summary table tallies the pages.

Still writing the export step: the JSON records builder maps each paragraph into a record with its symbol, number, section, part, pages, and text...

I'm now building the markdown export: a front-matter block with the title, extraction date, and source URL, then walking the paragraphs in order and inserting each heading before the paragraph it precedes, with level-one headings as ## and deeper ones as ###.

I'm setting up the export buttons next: a JSON records builder and a markdown export with front matter, with headings placed before their paragraphs. The download step will name the file from the document symbol and stay disabled when there are no paragraphs. I'm also planning the table caption and the expandable rows.

Now I'm building the expandable table rows: each paragraph number is a button that toggles a detail row, and clicking anywhere on the row does the same. The detail shows the section path, the full text with suspect lines marked, the reference-versus-found first words, a hidden view of the PDF's raw lines with page markers, and a copy-citation button.

I'm finishing the header and footer and the two summary tiles on the first tab: the paragraph count compared against the document's total, and the first-words match count against the reference.

Still writing the page styling: I'm setting the paper, ink, and accent colors, keeping the muted text readable, and then building the tabs with proper tab roles and roving focus.

I'm sorting out how the flagged pages panel will work: each page gets a row that opens a detail view listing its raw lines, with the suspect ones marked. I'm also thinking about the collapsible sections, which open and close on their own without affecting each other.

I'm writing the paragraph-rendering helper, which joins each paragraph's lines and wraps the suspect ones in a marked span. Next is a short first-line helper that trims long text at a word boundary with an ellipsis, and then the first-words check column, which shows a failed match or a footnote warning, or both, with "no reference" when there isn't one.

Still writing the numbering check in code: I'm walking the paragraphs in order, expecting each number to follow the one before it, and collecting any gaps or repeats as I go.

I'm now checking the numbering: each paragraph number should follow the last, and any gap or repeat gets noted with its page. Then I'm tallying up about ten checks in total, including the round trip through the JSON export, which I'll build once at click time.

I'm listing the check lines with their status labels, and linking to the rows only for failed or flagged checks. Heading counts will come from the labelled and unlabelled lists, and I'm keeping the first tab to seven clickable items or fewer.

Writing the first-words helper and the numbering check now...

Still writing the first-words helper now, stripping footnote numbers from the start of the paragraph text...

Still writing the first-words helper, stripping footnote numbers that trail words and dropping standalone digits after punctuation.

I'm writing the first-words helper now, dropping footnote numbers that trail words and bare digits after punctuation, and I'm normalising curly quotes and dashes so the comparison is consistent. Then I'll finish writing the full file with the tiles, the summary rail, and the table styling.

Still writing the event handling: clicks on the toggle buttons, paragraph rows, and flagged-page rows are delegated at the document level, and each one opens or closes its detail row.

Still wiring up the event handling: clicks on the paragraph rows and the flagged-page rows are caught at the table level, and each one opens or closes its detail row, with the button and the row sharing one handler so nothing fires twice.

I'm adding the mismatch list to the first-words check, capped at ten lines showing each paragraph's found and reference text, with a count of the rest.

