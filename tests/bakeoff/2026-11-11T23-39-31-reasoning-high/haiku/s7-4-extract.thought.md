The user attached the PDF text and wants the app built to match the plan. Since the spec is long and detailed, I'll need to produce one complete HTML document that runs in the browser against the PDF text.

I'm checking the footer rules next: trailing lines get dropped while they're empty, start with "GE.", are only 6-digit groups, or are a bare 1-3 digit number, with a matching number recorded as the page number.

I'm working through the page-processing steps: after the header, I strip footer lines from the end of each page while they're blank, start with "GE.", are only 6-digit groups, or are a bare number, using a bare number that matches the page to record the page number. Body lines get collected across all pages, blank lines included for now, since headings depend on them.

I'm sorting the records by page and trimming each line, then moving on to classifying the body lines. The paragraph-start pattern needs care, since a bare number followed by a period could also show up in footnote text.

I'm checking how paragraph starts are matched: a number followed by a full stop and a space, like "12. ", should count as a paragraph start, while a bare number with no dot, such as a footnote "2 Summary for policymakers", should not. Cover lines like "6 November 2025" or "Distr.: General" fall outside that pattern and stay with the cover before the first paragraph.

I'm checking how paragraph starts get matched, and a line like "24. " counts while bare numbers with no dot don't. I'm also looking at the asterisk footnote lines, which I'll treat as suspect text. Heading detection is next: I need to see how single-letter or Roman numeral labels on their own lines get told apart from paragraph text.

I'm working out how labelled headings take their text: after a label line I skip any blank lines, then gather lines until the next label or paragraph start, with lowercase or parenthesised lines joined onto the previous heading line.

I'm checking how heading text gets collected after a label: each line runs until the next label or paragraph start, so a line like "Introduction" just before "1." counts as heading text, and I'm asking whether a heading spanning a page break or sitting mid-paragraph would break that rule.

I'm settling how heading text gets joined: after a label, the following lines up to the next label or paragraph start all count as heading text, and I can just join them with spaces rather than treating lowercase or parenthesised lines differently.

I'm weighing whether labelled headings should join every following line into one heading or split capitalised lines into separate headings, and I'm leaning toward joining everything with spaces since the difference is minor.

I'm settling how unlabelled headings get picked out: the candidate is the nearest non-blank body line before a paragraph start, since headings like "Right to work (art. 6)" sit one or two lines above the number. I'll treat that line as the heading unless it's a footnote or a label.

I'm now checking the heading candidates: a line counts only if it's under 90 characters, starts with a capital, and doesn't end in a full stop, semicolon, colon, comma or digit. If the line before it also passes that test and doesn't close a paragraph sentence, I'll treat the two as one two-line heading.

I'm settling how two-line unlabelled headings get joined: if the line before a candidate also passes the heading test and doesn't close off a paragraph sentence, I'll read the pair as one heading, which means a wrapped heading like "Right to work (art. 6) and the" followed by "environment" comes out as one piece.

I'm settling how two-line unlabelled headings get joined: if the candidate line passes the heading test and the line before it does too, I'll treat them as one heading, but I'm worried a paragraph's last two lines could both pass and produce false positives.

I'm settling the two-line heading case: a candidate line joins the one before it only when both pass the heading test, which covers a heading wrapping across two lines. The continuation line that starts lowercase fails that test, so it stays out of the heading.

I'm settling the two-line heading case now: if the last line before a paragraph start fails the heading test because it begins lowercase, it can't anchor the heading, so I'll check whether the line before it passes and treat the pair as one heading only in that case.

I'm settling the two-line heading rule: if the line just before a candidate heading also passes the same test, I'll join the two into one heading, so a wrapped heading before a paragraph number comes out as a single piece.

I'm working out how a heading that is not labelled gets picked out when it sits just before a paragraph number: blank lines between the candidate and the paragraph start can be skipped, since blanks are dropped anyway. Labelled headings consume their own lines first, so a line like "Right to work" under a label won't be treated as a separate candidate.

Labelled headings take every line up to the next label or paragraph start, so an unlabelled heading sitting just before a paragraph number ends up inside the labelled heading's text. I'm fine with that, since it's still heading text, but the counts would then mix labelled and unlabelled headings together.

I'm working through the case where a labelled heading is followed by an unlabelled one before the paragraph number, such as "Right to work (art. 6)" then "Children". Since labelled headings absorb every line up to the next paragraph start, the unlabelled line would end up in the same heading text, which I'm still weighing against how the counts should be kept separate.

I'm settling how labelled headings take their text: lines starting with a lowercase letter or an opening parenthesis join onto the heading line before them, while lines starting with a capital letter count as separate heading lines.

I'm settling how the section name gets chosen: the nearest heading before a paragraph becomes the section, with the labelled part kept separately, so I'll store each heading as an entry with its text, whether it was labelled, and its part.

Now I'm settling how the heading path is kept: a roman label resets the path, a lettered label extends it under the current part, and an unlabelled heading sits at the lowest level beneath those.

I'm settling how a heading that runs past its label gets filed: a label starts a new level in the stack, and anything without a label drops to the lowest level, so I'll store its full path for the section.

I'm deciding whether the cover lines before the first paragraph should count as cover, since the labelled "I." heading sits after them and some lines may be claimed as heading text instead.

I'm working out how the cover lines before the first paragraph get handled: the "I." label and its "Introduction" heading are picked out first, while the header symbol is dropped and the other top-of-page lines stay as cover.

I'm checking which cover lines sit before the first paragraph, such as the UN header, committee name and general comment title. An asterisked line that appears at the foot of page one is a footnote, so it belongs with the paragraph text rather than the cover.

I'm checking how body lines after a paragraph start get assigned, specifically the footnote lines that trail a paragraph and still count as paragraph text.

I'm checking how bare numbers and footnote-style lines in the body get flagged as suspect, since a footnote like "1" followed by text or "2 Summary for policymakers" can look like paragraph text and needs to be marked separately.

Checking how suspect flags carry across a paragraph that spans two pages: a suspect line marks everything after it on the same page, so I need to track the page of each line separately rather than the paragraph as a whole.

I'm making the footnote check work page by page: once a suspect line turns up on a page, every later body line on that same page gets flagged, and the marker clears when the page changes.

I'm checking the footnote rule: suspect checks apply only to lines inside a paragraph, not to headings or paragraph starts. Once a suspect line appears on a page, the lines after it on that same page are flagged too, and the flag resets when the page changes.

Now I'm checking how the paragraph-level footnote rule interacts with paragraphs that run across a page break, and whether the bare number at the start of a footnote is the only signal I need.

Now I'm settling the last checks: long paragraphs over 300 words get flagged, word counts split on whitespace, and lines ending in a hyphen get counted for the report. I'll also verify paragraph numbers run 1 to n in order and list any gaps or duplicates, and take the first words of each paragraph with footnote marks stripped.

I'm working out how to handle tokens that are only digits: a bare number gets dropped when the word before it ends in a full stop, comma or closing quote, unless that word is an abbreviation like "No." or "art.", so that "No. 3" keeps its number.

I'm now checking how digits attached to words or punctuation get handled, such as footnote marks stuck to the end of a word, and whether a stray number like "E/2003/22" should be cut or kept as a symbol.

I'm settling how a digit-only token gets handled, and whether the word before it ends in a full stop, comma or closing quote, with abbreviations like "No." or "art." kept, while digits stuck to the end of a word are cut from it.

I'm working out the token rules now: a digit-only token gets dropped when the word before it ends in a full stop, comma or closing quote, unless that word is an abbreviation such as "No." or "art.", so "No. 3" keeps its number. Digits stuck to the end of a word or punctuation mark get cut off, and a digit-only token after a closing quote and full stop, like "”. 3", is removed.

I'm checking how the first six words of each paragraph get pulled out, which means dropping footnote digits stuck to words and bare numbers after a full stop or closing quote, while keeping abbreviations like "No. 3". Then I'll normalise the quotes and dashes and compare against the reference list.

Next I'm pinning down what each exported record carries: the symbol, paragraph number, section, part, page range, the text, flags, the first-words check, citation, document link and limitations, with the text lines joined by a separator. I'm also weighing whether to keep the raw text alongside the cleaned version, since the spec says suspect lines stay inside their paragraph's text.

I'm settling on the last details: the paragraph text keeps its lines joined with a separator, the export carries the flags, citation, and limitations, and I'm not adding any extra raw-text field beyond what's already listed.

I'm settling how the footnote note in the limitations gets worded: if a paragraph is flagged for running over 300 words, I'll count its suspect lines and say how many may sit inside it, with the number matching the count.

Now I'm settling how the Markdown output is laid out: headings at level 1 become "##" and levels 2 and 3 become "###", placed in document order between the paragraphs.

Now I'm settling the export details: the Markdown headings and flagged notes are laid out, and the download handling for the sandboxed iframe is decided. I'll check that the JSON round trip matches the table row count.

I'm laying out the checks now: paragraph count against the reference, numbering from 1 to n with any gaps or duplicates, and first-word matches. Paragraphs flagged for possible footnote text will be listed as items to check against the PDF, not as failures.

I'm settling how the checks are counted for the summary: each one is a pass or a fail, and the flagged-paragraph note is listed as something to check against the PDF rather than counted either way. Checks that couldn't run are shown as not run and left out of the total.

I'm laying out the checks for the summary: header and footer checks on each page, the suspect-line count shown as information only, and a pass or fail tally where a red dot appears if any check fails.

Now I'm settling the checks for the summary: header and footer on each page, with page-number checks counted as pass or fail, and bare numbers and unlabelled headings listed as information only. I also want a check that every non-empty line is classified exactly once, so the counts add up to the total.

I'm assigning each non-empty line a single kind (cover, header, heading, paragraph or footer) through a helper that flags any double classification, so the final check can confirm every line was classified exactly once.

I'm assigning each line a single kind, with a helper that flags any line classified twice, so a final check can confirm all lines were sorted exactly once.

I'm finishing the export details and laying out the checks: paragraph count against the reference, numbering, first-word matches, flagged paragraphs as items to check against the PDF, and a per-line tally confirming every non-empty line is classified exactly once.

Now I'm laying out the table in tab 02, with columns for number, section, page, first line and check status. Each row expands to show the full paragraph with suspect lines outlined in red, the reference's first six words beside the found ones, a toggle for the PDF's own lines with page markers, and a button to copy the citation. I'm also adding a closed box above the table that lists the headings found, and a closed section in tab 01 for the flagged paragraphs.

I'm laying out the flagged paragraphs table on tab 01, with columns for paragraph, page, suspect lines and the reason each one is flagged. Each row opens that paragraph on tab 02 with the suspect lines highlighted.

I'm settling the suspect-line rules now: a bare 1-3 digit line counts as a bare number, and a line that starts with 1-3 digits, a space, and then a capital letter, a UN symbol, or a quotation mark gets flagged too.

I'm writing out the regex for suspect lines: a line starting with 1-3 digits and a space, followed by a capital letter or a quotation mark, gets flagged. I also have an asterisk-and-space check to add, plus a bare-number test for lines that are only digits with no full stop.

I'm working out how to count flagged paragraphs by page, using the pages where their suspect lines sit, and I'm treating a paragraph over 300 words without any suspect line as flagged on its own.

Now I'm working out how to count the flagged paragraphs by page, using each one's first page, and how to tally the suspect lines and the paragraphs they sit in. For the header line, I'm checking whether the reference has an adoption date before I write it.

I'm checking the footer rules: trailing lines are dropped while they're empty or made only of 6-digit groups, and I'm splitting each line by whitespace to test that. The date stamp and the "GE." line both count as footer. I'm also wondering whether a bare footnote number at the bottom of a page could be mistaken for a footer.

I'm dropping blank lines during the first pass over the PDF text, since the reference lines and the page markers are all that the display needs.

I'm working through how to classify the body lines in a single pass, tracking the current paragraph and its page as I go.

I'm working out how to walk through the body lines in a single pass, starting a new paragraph whenever a numbered start appears and classifying each line as I go. Labelled headings like "I." or "A." will open heading blocks that collect the text until the next label or paragraph start.

I'm working out the labelled headings next: a line like "I." or "A." opens a heading block that collects the text until the next label or paragraph start. The heading text only runs up to a paragraph start, so there's a small risk it swallows real paragraph text if a heading sits at a page end, though that looks unlikely here. The cover lines before the first numbered paragraph stay as cover.

Now I'm deciding how to handle labelled headings: I'll simply join their text lines together rather than splitting on capital-letter starts, since splitting risks mixing a heading with a neighbouring one.

I'm settling on a single joined block for labelled headings rather than trying to split out sub-headings, since splitting adds more risk of mixing titles than it saves.

I'm deciding how to spot headings that sit just before a paragraph start, so I plan to look back at the lines preceding each numbered paragraph, before classifying anything, instead of deciding as I go.

I'm working out the unlabelled-heading case: when a short line sits just before a numbered paragraph start, it should come out of the previous paragraph and become a heading, so I'd pop it from that paragraph's lines and mark it as heading.

I'm now writing the body classification pass, looping over the lines in order and starting a new paragraph at each numbered start. Labelled headings like "I." or "A." will collect their title lines until the next label or paragraph start. For unlabelled headings, I'll look back at the line just before each paragraph start and, if it passes the heading test, move it out of the previous paragraph and mark it as a heading.

I'm working out how to detect unlabelled headings: when a short line just before a paragraph start is heading-like, it should be pulled out of the previous paragraph and marked as a heading.

I'm checking whether a candidate heading line is already a suspect line before I move it out of the previous paragraph, since a suspect footnote continuation shouldn't be turned into a heading.

Now I'm working through the unlabelled-heading check at each paragraph start, looking back at the previous body lines and skipping any that were already flagged as suspect so a footnote continuation doesn't get turned into a heading.

I'm checking the case where the candidate heading line is also the first line of the paragraph itself, so popping it would leave the paragraph empty.

I'm settling on how to handle the start line of each paragraph, since its text sits on the numbered line rather than in a body line. To make the look-back simple, I'll store each paragraph's text as line objects that point back to their body position, so I can check and pop the right entry.

I'm now going through the body lines, tracking which paragraph each one belongs to, so that headings can be pulled out before the paragraph text is stored.

I'm deciding to classify each line once in a deferred pass: first working out which lines are headings, paragraphs, or cover, then assigning each kind a single time.

Now I'm settling on how to tally the classification: each line gets one bucket (cover, header, footer, heading, or paragraph), and I'll confirm that the bucket totals match the number of non-empty lines with no line counted twice.

Now I'm settling the line objects: each non-empty line gets an id, page, and trimmed text, and I'm building them page by page in order.

I'm going through how to classify each line into one bucket, with a check that every non-empty line lands in exactly one of cover, header, footer, heading, or paragraph. Footer lines are detected from the end of each page, and a bare number is treated as the page number only when it matches that page.

Now I'm writing the paragraph and heading split for the body lines, looping through them in order and pulling out any short line before a paragraph start that looks like a heading.

I'm setting up the heading stack to track the nesting of roman, letter, and unlabelled headings, so each heading knows its section and part.

I'm setting up the heading stack so each heading level replaces anything at or below it, and the paragraph's section comes from the nearest heading above, with the roman-level heading as its part when one exists.

I'm settling on how to name the section headings: each labelled heading keeps its label, so a paragraph's path reads as the roman number followed by the title, with the nearest heading above it as its section.

I'm working out how to detect the start of each paragraph in the body text, so I can pull any unlabelled heading out of the paragraph before it. I'll store each heading with its label and title so the path can be built later.

Writing the regex patterns for paragraph numbers and section labels, and noting that the roman-versus-letter check has to come before the letter match.

I'm now writing the paragraph-start check, testing each body line for a bare number followed by a period or a number with text, so I can split paragraphs at each start.

Still working out how to pull unlabelled headings out of the previous paragraph, checking the last line before each new paragraph start and skipping it if it's the paragraph's own first line.

Still working on the unlabelled-heading pull: I'm checking the last line of the current paragraph, and if the line before it also looks like a heading, taking both together and recording them as a level-3 heading.

I'm handling the unlabelled-heading case now: when a new paragraph starts, I look at the last line or two of the current paragraph, and if they look like a heading and aren't already flagged as suspect, I pull them out and record them as a level-3 heading ahead of the new paragraph.

I'm handling the case where the candidate heading line is also the paragraph's first line, which is excluded because the paragraph start is marked. I'm also checking that the line before a candidate isn't a paragraph line, since a lowercase opener like "... (see below)" would fail the heading test anyway. Unlabelled headings are treated as level 3, and I'm updating the heading stack so a new level-3 heading replaces any earlier one at that depth.

I'm treating an unlabelled line that precedes a paragraph start as a level-3 heading, and I'm making the heading stack drop any deeper levels when a new heading arrives. For heading paths that have gaps, I'll filter out the empty slots when building the path. Next I'm creating the paragraph object and recording its section and part from the stack.

Next I'm settling the paragraph-start handling: each new paragraph takes its section and part from the heading stack at that moment, and any unlabelled heading that was pulled from the end of the previous paragraph gets recorded before the new paragraph is created. If the paragraph opens with its number and text on one line, that first line is stored as the start of the paragraph; otherwise the number stands alone and the body lines that follow fill it in.

I'm settling how to bucket each line: instead of tracking assignments as I go, I'll decide every line's bucket at the end from the final paragraph, heading, cover, header, and footer lists. Then I'll count each id's bucket entries and expect exactly one per line.

Still writing the body-line parser...

I'm now handling unlabelled headings: when a new paragraph starts, I check the last line or two of the current paragraph, and if they look like a heading and aren't already suspect, I pull them out as a level-3 heading placed before the new paragraph. I'll rebuild the heading stack with holes filtered out, and capture each paragraph's section and part at the moment it starts.

I'm checking the paragraph-line branch next: if there's no open paragraph yet, the line goes to the cover, and otherwise it gets tested for footer-like text, with the footer page remembered so later lines on that page are treated as suspect too.

I'm checking whether a line that falls under an earlier footnote on the same page should also count as suspect, so later lines on that page get flagged too, but only the ones inside paragraphs. A paragraph start line itself stays unflagged even when it sits on that page, since the paragraph-start check runs first.

Now I'm finalizing the paragraph list after the loop: joining each paragraph's lines into one text, keeping the line breaks, and recording the page it starts on.

I'm settling on the paragraph-finalizing step: when the start line is alone, it gets a placeholder line with empty text so the paragraph still has its number to show, and empty text is dropped when joining.

Now I'm settling how the paragraph text gets assembled: the rest of the start line goes first, followed by the other lines, and the original lines are kept for the line-break export.

I'm sorting out the flagging rules now: a paragraph gets marked if it has suspect body lines or runs past 300 words, and the bare-number start lines themselves are never counted as suspect.

Now I'm settling the numbering check: the paragraphs' numbers should run 1 through n in order, so I'll look for gaps, duplicates, and out-of-order entries. For the first-word comparison, I'll take the first six words of each paragraph's text and check them against the reference entry for that number.

Still working out how the first-words check handles a reference entry that's missing, and writing the helper that takes the first six words of each paragraph.

Still writing the first-six-words helper, with the digit-stripping rules for footnote markers.

Still working through the first-six-words helper, deciding which trailing digits to strip from footnote markers and when a bare number after a sentence-ending word should be dropped.

Still working out how the first-words check handles a missing reference entry, and I'm tidying the token normalisation so the dash and quote variants compare equal.

Next I'm adding the tile for paragraph count, checking it against the reference's paragraph total and marking it red if they differ, or noting when the reference has no such total. Then I'm adding the first-words tile, which compares against the reference's first-word entries.

I'm laying out the tiles and the header status next: the paragraph count against the reference total, the first-words match, and how many paragraphs got flagged. The rail shows the same counts with a bar, and a closed "Every check" section will list each check with its values and status.

Now I'm settling how the "show rows" links behave: they'll jump to tab 02 and open the first affected row, falling back to just switching tabs when no rows are concerned.

I'm laying out the rest of tab 01: four tiles, a list of any first-word differences, buttons to download the paragraphs as JSON or Markdown, and two closed sections for every check and the flagged paragraphs. The table rows will be clickable, and the whole tab stays to about seven controls.

I'm laying out tab 02 now: a closed "Headings found" box above the table, with each row showing its number, section, page, first line, and check result. Expanding a row will show its full text, mark the suspect lines, and set the reference's first six words beside the ones found, with a button to copy a citation.

Now I'm laying out the rest of the tab-02 table, with each row expanding in place when clicked or activated from the keyboard.

Now I'm handling the expanded paragraph view: the full text is shown verbatim, with suspect lines wrapped in a red-bordered span inside one block of running text.

I'm setting the expanded paragraph view to show each line's text joined with spaces, with suspect lines wrapped in a marked span, and the start text left unmarked. Next I'm adding a toggle that reveals the PDF's own lines in order, with a "page N" marker wherever the page changes.

Now I'm working out the flagged-paragraph table on tab 01, with paragraph, page, suspect lines, and reason columns.

I'm writing the reason labels for each suspect line, sorting them into bare numbers, numbers followed by a space, asterisks, and continuation lines below a footnote, and I'm combining them per paragraph.

I'm working out the reason for each suspect line: a bare number or a number followed by a space gets its own label, an asterisk start gets another, and a line below a footnote gets a continuation label. When a line triggers the flag, its own reason is used, and the footnote tracking only moves forward from that point.

Now I'm defining the suspect check: a line counts as suspect if it's only one to three digits, starts with one to three digits followed by a capital letter, a UN document symbol, or a quotation mark, or starts with an asterisk and a space.

I'm working out the checks now: headers should appear on every page, and footers on every page except the first. For each, I'll compare the count of pages that have the marker against the expected count.

I'm laying out the page-level checks next: every page after the first should carry a page number in its footer, and the header symbol should appear on every page. For each check I'll compare the count of pages that have the marker against the expected count, and I'll note any bare numbers that were dropped from the footers and any pages whose first line isn't the document symbol. Each check gets a small record with its values, a pass, fail, or info status, and links back to the affected paragraphs.

Now I'm working out the nothing-lost check: counting every non-empty line across all pages and confirming each one lands in exactly one bucket, flagging any that don't.

Now I'm checking the closing part of the logic: each body line should be classified once, and the JSON export should round-trip with the same number of records.

I'm wrapping up the checks: the heading count, numbering, paragraph count against the reference, first-words mismatches, and the JSON round-trip, with the flagged and suspect lines kept as info and the pass/fail total shown at the end.

Now I'm writing the Markdown export, with a YAML header carrying the title and symbol.

Now I'm finishing the Markdown export: a YAML front-matter block with the title, symbol, source link, and the found-versus-expected paragraph and footnote counts, followed by each heading and paragraph in document order.

Now I'm writing the download helper that wraps the text in a blob and triggers a file save, plus the filename rule that swaps slashes for hyphens in the symbol.

Now I'm wrapping up the document header and footer: the symbol link, adoption date, page count, and source line, plus a note that everything runs locally in the page.

Now I'm finishing the document layout and deciding the initial state: if the PDF text data is missing, the page will show a plain message instead of the tabs. I'm settling the styling next, with a paper-and-ink palette, a red accent, a serif face for titles and numbers, monospace for labels, and sans-serif for body text, all kept compact.

Still writing the document styles...

Still writing styles...

Now I'm writing the page header: a kicker line, the title, the meta line, and a status line, followed by the two-column shell with the summary rail and the tabbed main area.

Now I'm wiring the page's state and rendering: the header, rail, and both tab panels get rebuilt from the pipeline result whenever something changes, with event handlers attached once through delegation.

Still working out the focus handling: after re-rendering a table row, the button a keyboard user just pressed disappears, so I'll need to restore focus to it.

I'm working on the progress-saving behavior for the row toggles: after a re-render the clicked button is gone, so I'll record a key on each control and refocus the matching element once the panel rebuilds.

Now I'm writing the object the pipeline returns, with the page counts, header and footer checks, headings, paragraphs, and the buckets used for the nothing-lost check.

Now I'm writing the pipeline's setup: sorting the page records, and preparing empty lists to collect the header, footer, and body lines along with any warnings.

Now I'm setting up the pipeline's per-page loop: each page's lines get numbered, and the first line is checked against the document symbol to record whether the header is present.

Now I'm walking through the pipeline's per-page footer handling: trailing footer lines are popped off each page, and a bare number that matches the page number is recorded as the page marker, while any other bare number is logged as removed.

Now I'm writing the body loop, which classifies each remaining line as a paragraph start, a continuation, or a heading.

Now I'm writing the paragraph-building loop, and this time I'm working out how each paragraph gets its path and first-line text.

Still working out the pipeline's heading state: I'm defining a helper that trims the heading stack to the right depth and records the current heading, and using the stack to derive the part and path labels for each paragraph.

Now I'm writing the body loop: each remaining line gets checked for whether it starts a new numbered paragraph, continues the current one, or looks like an unlabelled heading.

Now I'm taking the unlabelled heading candidates off the end of the current paragraph, first checking whether the line before them also looks like part of a heading, and then turning those lines into a level-3 heading with the combined title.

Next I'm wiring the paragraph and heading events into one ordered list, so the Markdown export can walk them in document order.

Now I'm finishing the body loop's paragraph handling: when a new numbered paragraph starts, any unlabelled heading lines sitting at the end of the previous paragraph get pulled out and turned into a level-3 heading, and then the new paragraph is recorded in document order.

Still writing the body loop, now the label-handling branch: it gathers the lines that follow a roman or letter label until the next label or paragraph start.

Still working on the label handling: I'm gathering the lines after a roman or letter label until the next label or paragraph start, and recording them as a heading.

Still working out the paragraph-building loop: I'm checking the lines that continue the current paragraph and deciding whether each one is a suspect footer line before it gets added.

Still working through the body loop: each remaining line either starts a new paragraph, continues the current one, or gets flagged as a suspect footer line, and I'm wiring the events so headings and paragraphs stay in document order.

Now I'm finishing the paragraph output: each paragraph's text gets assembled from its start-line remainder and its continuation lines, with the suspect footer lines filtered out.

Still wiring the paragraph output: each paragraph's text is joined from its lines and flagged if it has suspect lines or runs over 300 words.

Now I'm checking how each paragraph's first words line up with the reference, comparing them after normalizing quotes, dashes, and whitespace.

Now I'm writing the bucket map, tagging each line by whether it's header, footer, cover, heading, or paragraph text so the nothing-lost check can run afterward.

Now I'm sorting out how unlabelled heading lines and the cover lines are placed, then tallying which lines fall into no bucket or into more than one.

Now I'm checking the headings and header and footer counts, then confirming the page numbers run in order from 1 with no gaps.

Now I'm working out the gap and duplicate reporting: any paragraph number missing from the sequence gets listed with the paragraph before it and its page, and any repeated number gets listed with its page, falling back to an out-of-order note if neither applies.

Now I'm checking how the flagged paragraphs are reported, using each paragraph's start page for the table and collecting the distinct pages where suspect lines sit.

Now I'm laying out the list of checks, starting with the paragraph count against the reference and then the numbering check.

Now I'm laying out the checks: the paragraph count against the reference, then the numbering, with any gaps or duplicates listed.

Now I'm writing the checks list, pairing each comparison with a status and the rows or items that back it up. The duplicate and gap reporting, the suspect-line page counts, and the unlabelled heading list are all going into that same set of checks.

Still building the checks list: each comparison gets a status, and the failed and flagged rows are linked back to their paragraphs.

Now I'm wrapping up the tab-one content with a stats tile row, a list of the checks with their pass or fail status, and a flagged paragraphs table, and I'm setting up the export buttons above it.

Now I'm laying out the tab-two view: a headings box with a count, and a paragraph table captioned with how many were found against how many are expected, where each row expands to show the full text and the reference comparison.

Now I'm adding the copy-citation action: it sets a flag for that paragraph and shows "Copied" briefly before the row re-renders.

Still working on the tab layouts: the first tab gets a stats row, the checks list, and a flagged paragraphs table, and the second tab gets a headings box plus a paragraph table where each row expands to show the full text and its reference comparison.

Now I'm rendering each paragraph's full text in the expanded row, joining the lines with spaces and marking the suspect ones with a tooltip.

Still writing the paragraph-view code: each paragraph's lines get rendered in order, with a page marker whenever the page number changes and suspect lines flagged.

Still wiring the tab-one flagged rows: each row's first cell becomes a button, and a click handler on the rows catches both it and the row itself.

Now I'm building the rail and status area: a document card with the symbol and title, a paragraph count shown against the expected total, and a progress bar.

Now I'm sketching the rail's status area: a document card with the symbol and title, a paragraph count set against the expected total, and a progress bar.

Now I'm building the Markdown export, starting with a front-matter block that carries the title, symbol, adoption date, source URL, and extraction date.

Now I'm assembling the Markdown export: a front-matter block with the title, symbol, adoption date, source, and paragraph counts, followed by the headings and numbered paragraphs, with flagged paragraphs marked.

Still building the JSON export: a short phrase for that remaining code.

Now I'm writing the JavaScript for the page, which covers tab switching, the expandable paragraph rows, and the Markdown export.

Now I'm writing the JavaScript for the page, starting with the text parsing and the paragraph and heading checks.

Now I'm writing the regex helpers and the logic that tells a paragraph start apart from an abbreviation.

Still working on the paragraph parser: I'm writing the helpers that tell a real paragraph start from an abbreviation.

Still writing the parser helper: `firstSix` takes the first six tokens of a paragraph, dropping any stray footnote digits stuck to the end of a word.

Now I'm checking how the firstSix helper trims a token: a digit suffix stuck to a word gets dropped, but a standalone number after a closing mark or an abbreviation stays put.

Now I'm writing the normalisation helper, which swaps curly quotes and apostrophes for straight ones before any comparison.

Now I'm working through the footer and header checks, starting with how each page's lines are split and where the trailing lines get trimmed.

Still writing the body-line split: the header line is taken off each page and the trailing footer lines are popped, with bare page numbers recorded.

Now I'm writing the JavaScript that builds the first-words check and the tab-one list, with the expected count taken from the reference.

Now I'm working out how the heading path is tracked: each heading level replaces the entries below it, and the part-level label comes from the first entry.

Still writing the paragraph parser: the header and footer lines get stripped from each page, and I'm adding the loop that walks the remaining body lines to start each paragraph.

Still writing the body-line loop: I'm checking whether a paragraph's last line is a heading-like fragment that belongs to the next heading.

Still writing the paragraph-start code: the current line is recorded as a new paragraph's first line, with its page, section path, and part label set from the heading state.

Still writing the paragraph builder: each paragraph's lines are collected and checked for suspect text before the output list is built.

Still writing the paragraph builder: each paragraph's text is joined from its start and continuation lines, and suspect lines get collected as reasons for flagging it.

Still writing the paragraph builder: each paragraph's text is joined from its first line and continuation lines, and the reasons for flagging it are collected.

Now I'm assembling the kind counts over the whole set of lines, checking that the totals add up to everything collected.

Now I'm finishing the export step: each paragraph becomes a JSON record with its symbol, number, section, page range, text, flags, and citation.

Now I'm wrapping up the paragraph export and starting to set up the checks list.

I'm adding the check that compares the paragraph count with the reference total, marking it as a fail if they differ.

Still writing the check list: I'm working out the numbering check, looking for missing and duplicate paragraph numbers and whether they come out in order.

Now I'm checking the first-words test: it compares each paragraph's first six words with the reference list, and any paragraph without a matching entry counts as a mismatch.

Now I'm wrapping up the checks with the flagged-paragraph count, the suspect lines, and whether each page starts with the symbol. The footer check looks for page numbers on every page after the first.

Still wiring up the checks: the footer count comes out against the pages after the first, bare footer numbers get logged, and I'm tallying unlabelled headings and lines ending in a hyphen.

Now I'm checking the export records and the round-trip check, which parses the JSON back to make sure the paragraph count holds.

Now I'm wiring up the page's state, the header and rail rendering, and the tab panels.

Still wiring up the page state and the header and rail rendering, including the tab panels.

Now I'm wiring up the rail: the document card, the paragraph count bar, the flagged count with its hint, and the checks tally.

Now I'm wiring up the paragraph tab: a tile for the paragraphs found, compared against the document's expected count, with a bar that turns red when the two don't match.

Now I'm laying out the first tab's tiles: a paragraph count compared against the expected total, a first-words match tile, a flagged-paragraph tile, and a footnotes tile that notes they aren't separated.

Now I'm laying out the paragraph tab: the paragraph count against the expected total, the first-words match, the flagged count, and a note that footnotes stay in place, then the export buttons.

Still wiring up the check list: each check gets its name, a status label, and any items beneath it, with flagged paragraphs marked for a check against the PDF.

Now I'm wiring up the link for a failed check and the flagged-paragraphs fold, with a note about footnotes that still sit inside the text.

Still writing the flagged-paragraph table: each row links to its paragraph on tab 02, with the page, the suspect lines (up to two, then a count of the rest), and the reason.

Still writing the table markup for tab 02: a serif heading asks what each paragraph says, a foldable headings list sits above it, and the table caption carries the paragraph count against the expected total.

Now I'm writing the row renderer for the paragraph table: each row takes its number, section, and page range, a cut-down first line, and a check column that marks mismatched first words or possible footnote text.

Still writing the row renderer: each row's number links to its detail view, and the check column flags mismatched first words or possible footnote text.

Still writing the detail view: each paragraph's path is shown above its text, and the found and expected words are set side by side for comparison.

Still wiring up the detail view: each paragraph's path sits above its text, with the found and reference first six words set side by side, plus buttons to show the PDF lines or copy the citation.

Still writing the copy helper: it tries the clipboard API first and falls back to a hidden text area when that isn't available.

Still writing the copy helper: it falls back to a hidden text area when the clipboard API is unavailable, then shows a "Copied" state on the button for two seconds.

Now I'm wiring up keyboard navigation on the tab list, so the arrow keys and Home and End move between the two tabs.

Still wiring up the keyboard and click handling: the tab buttons switch panels, and clicking a row toggles its detail view.

Still wiring up the click handling: the tab buttons switch panels, and clicking a row toggles its detail view.

Still wiring up the click handling and the focus restore, checking that the detail buttons and the checks-panel link route through the same delegated handler.

Still wiring up the download handler, which pulls the export records from the current results and builds the file for the chosen format.

Still wiring up the download handler: it builds the markdown and JSON exports from the stored results and names each file after the document's symbol.

Still writing the stylesheet: the monospace labels, the serif headings, and the header spacing and status row.

Still writing the stylesheet: the tab bar, the rail and main layout, and the responsive rule that stacks them on narrow screens.

Still writing the stylesheet: the tab buttons get a red underline when selected, the tables get rules under the headers and cells, and the big numbers and tile grid sit alongside the shared button styles.

Still writing the stylesheet: the status colours, the bar and sus-span highlights, and the right-aligned numeric columns.

Still writing the stylesheet: the tab buttons and tables get their rules, and the big numbers and tiles sit alongside the shared button styles.

Now I'm writing the page markup: a header with the title and status row, then a two-column shell with the rail and main area.

Now I'm writing the page header and the two-column shell, with the rail on the left and the tab bar and panels in the main area.

Now I'm writing the JavaScript: a state object tracks the active tab, which rows are open, and the check and flagged-paragraph folds.

Now I'm wiring up the page's startup: if no PDF text is attached, the title and panel show a prompt to attach it, otherwise the document is analysed and everything gets rendered.

Now I'm defining the label-block handler: a line that matches the label pattern becomes a heading, and the lines after it up to the next label or start-of-entry marker are gathered under it.

Still writing the cover handling: lines before the first entry are collected as cover text, and the loop moves on to the next line.

Now I'm finishing the analysis function: it reads the reference paragraph count, treating a missing value as absent rather than zero, and checks whether reference first-words are available.

Checking the cover-page lines next, from the title block down to the asterisk on the end of the title.

Now I'm checking the cover-page handling against the footer rules: the "GE." footer line and the 6-digit date stamp both get dropped, so the cover ends up as just the title block and its asterisk.

Now I'm checking the export round trip: the rows get serialised to JSON and parsed back, and the record count has to match the paragraph table.

Still writing the check list: each check gets a status word, and any check with rows links to the first of them.

Still working out the summary counts: I'm deciding whether the "n of m checks pass" figure should count every listed check or only the pass and fail ones.

Now I'm defining the helper that escapes text before it goes into the page, then starting the main script that reads the attached PDF data.

Still writing the constants and the start-of-entry parser: a numbered line, or a bare number followed by a full stop, marks where a paragraph begins.

Still writing the footer detection: a line starting "GE." is dropped, as is a line made only of six-digit groups or a bare 1-3 digit number.

Now I'm finishing the analysis function, checking the reference paragraph count and whether reference first-words are available.

Still working out the analysis function: I'm sorting the pages, splitting each one into trimmed lines, and checking whether the first line matches the document symbol so the header can be dropped.

Now I'm working through the page headers and footers: each page's first line is checked against the document symbol, and trailing footer lines are peeled off, with bare page numbers matched against their page.

Now I'm putting together the paragraph loop's output: each paragraph's text is joined from its opening line and body lines, and any suspect lines or paragraphs running over 300 words are flagged as reasons.

Now I'm building the paragraph records: each one gets its text, its word count, any suspect lines as reasons, and a check of its opening words against the reference.

Now I'm building the per-paragraph summary: each one gets its text, word count, any suspect lines as reasons, and a check of its opening words against the reference.

Now I'm defining the bucketing step: each line gets tagged as header, footer, cover, or paragraph text so the counts can be totalled afterwards.

Now I'm finishing the paragraph records: each one gets its word count, any suspect lines as reasons, and a check of its opening words against the reference.

Still writing the analysis: I'm checking the paragraph counts, flagged pages and heading labels, then tallying the buckets so the totals can be checked against every line.

Now I'm working out the paragraph-level data: each paragraph gets its text, word count, and reasons for flagging, and the first-word check is set against the reference.

Now I'm building the export rows: each paragraph gets its symbol, number, section, page range, text, flags, first-word match, citation and limitations, and the JSON gets serialised and parsed back to check it.

Now I'm assembling the front matter for the export: title, symbol, adoption date, source link, extraction date, paragraph counts, and a footnote note.

Now I'm setting up the checks list, starting with the paragraph count against the reference figure.

Still working out how the checks get their status: each one resolves to pass, fail, or not run, and the numbering check lists any missing paragraph numbers.

Still writing the flagged-paragraph check: it's informational, so it counts the flagged paragraphs and the pages they fall on rather than passing or failing.

Still writing the flagged-paragraph note and the suspect-line summary, then moving on to the header and footer checks: each page's first line gets compared against the symbol, and I'm working out how footers are checked against the page list.

Still working out the footer-number check: I'm comparing which pages carry a page number against the full page list, and writing the status and summary text for it.

