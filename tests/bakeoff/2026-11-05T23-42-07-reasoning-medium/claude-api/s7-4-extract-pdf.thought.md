I'm sketching out the app's data layer: a workshop object holding the PDF text, its records and reference details, which I'll handle whether it arrives as an array or an object. Next I'll lay out the processing pipeline.

I'm working out how to parse each page's lines: tagging them with their page and index, spotting the header that matches the symbol, and peeling off footer lines from the bottom until I hit real text. The blank lines stay in the body so heading detection still works.

I'm settling the parsing rules: each line gets tagged with its page and index, blank lines are kept for heading detection, and I'm checking for paragraph starts, labelled headings, and how the footer lines get stripped from the bottom of each page.

I'm weighing how to handle headings whose title runs onto a following line. Right now a labelled heading would swallow any unlabelled line after it, so I'm considering stopping the title at the first blank line once at least one title line has been read.

I'm weighing a tweak to the title rule: stop a labelled heading at a blank line unless the next non-blank line continues the title, starting lowercase or with a parenthesis. That should keep a stray unlabelled heading line from getting folded into the labelled one above it.

I'm now planning how to tell a labelled heading from an unlabelled one: a Roman numeral marks a part, while a letter, or a bare line that follows the heading structure, marks a subsection. Each heading's text becomes the current section, and I'll keep a running path from part to subsection to any unlabelled heading.

I'm now considering how to tell an unlabelled heading from the paragraph text around it: a short line that starts with a capital, lacks end punctuation, and sits just before a paragraph start counts as a heading. The worry is that a wrapped line in the middle of a paragraph could match the same test, so I'm checking whether the line before it also fits the pattern before joining the two into one heading.

I'm checking whether a line that looks like a heading really is one, and the main worry is a short wrapped line in the middle of a paragraph matching the same test. Since the previous line only counts if it sits at the end of the current paragraph, I'll also require that it isn't just the opening text of a paragraph, so a two-line heading can still be picked up.

I'm checking whether a line followed by a paragraph start is really a heading, and whether the line before it should join it as a two-line title. I'm also considering footnote lines at a page break, which could look like headings if they're short and start with a capital.

I'm checking whether a short line that comes right before a paragraph start can be a heading. It should only count if it's on the same page and doesn't end in punctuation that suggests it's part of the paragraph body, since footnote marks and quote endings could otherwise trip the test.

I'm adding a final guard for paragraph-ending lines: rejecting any line ending in a period, semicolon, colon, comma, digit, or question mark, and also any line ending in a closing quote or bracket right after one of those punctuation marks. Cover lines before the first paragraph get treated separately.

I'm settling how cover text gets separated from the body: everything before the first labelled heading or paragraph start counts as cover, and a footnote on page 1 should be handled by the suspect-line rule.

I'm marking which lines in each paragraph look like stray page furniture: bare page numbers, a number followed by a capitalised word or quotation mark, a UN document symbol, or a line starting with an asterisk. I'm also working out how a UN symbol at the start of a line gets matched so those lines can be stripped out of the body text.

I'm checking which footnote lines to flag as suspect: any line starting with digits and a capital, a quotation mark, or a UN symbol, plus everything after it on the same page. The open question is a footnote block that sits at the end of a paragraph and then carries over to the next page, where the following lines might get wrongly marked.

I'm checking a footnote edge case: a bare number followed by a line of text, with the rest of that page treated as footnote material, and whether a footnote near a heading could skew the detection.

I'm checking whether a short line right before a paragraph start is really a heading, and I'll require that it sits on the same page so footnote lines from the previous page don't get merged in. The footnote lines at the foot of a page are the risk here, since the first line on the next page could be a paragraph start with a footnote line just above it.

I'm settling on the paragraph text format: lines joined with spaces for the main text, and a separate raw version keeping the line breaks.

Now I'm settling how flagged pages get counted: a page counts once it has a suspect line inside one of its paragraphs, and an over-300-word paragraph gets its own row for the table.

I'm settling the word-count threshold for flagging a paragraph, then I'll check each token for footnote marks: stripping trailing digits only when they're glued to a letter or punctuation, so a standalone number or a reference like "2003/22" stays intact.

I'm settling how to pick out footnote marks from the first few words: a trailing number only counts when it's glued to a letter or punctuation, so references like "C.12" or "GC/27" might get clipped, and I'd rather require that the number is attached to a word and limit the check to the opening tokens.

I'm settling how to tell a footnote mark from a real number in the opening words: a trailing digit only gets clipped when it's glued to a lowercase letter or punctuation, and a standalone number after a sentence-ending mark gets dropped unless the word before it is an abbreviation like "No." or "art.". I'm still working out how the first six tokens get tokenised.

I'm checking the first six words of each paragraph after stripping footnote marks, then comparing them to the reference list. The checks are paragraph count, sequential numbering with no gaps or duplicates, and first-word mismatches, which only run when a reference exists. Pages flagged will be reported as information only.

I'm settling how the checks get reported: a note-status flag counts as a pass, failures are called out separately, and not-run checks don't count toward the pass total.

I'm laying out the output checks: confirming every page has a header, that page numbers appear on all pages except the first, and listing any bare numbers that got pulled out of the body. Then I'll tally the headings, labelled and unlabelled, and make sure every non-empty line is accounted for in some category.

I'm defining a per-paragraph check that counts the lines I classified, comparing that total against an independent count of the non-empty lines in the page text. Then I'll add a round-trip test on the JSON export and tally the hyphen-ending lines in the report.

I'm adding a line-end hyphen count as a small note check, then linking the flagged rows to a filtered view on tab 02 with a clear option. The rest is about keeping the click count low on the first tab.

I'm wrapping up the flagged-page detail view, which will show each page's raw lines with the suspect ones highlighted and the paragraph they belong to. Next I'm settling the export fields.

I'm now settling the export fields, including the paragraph text as a line-joined list, the section and part, the page range, flags, first-word match and citation. For the Markdown export I'm planning front matter, then headings in document order at level two or three, with each paragraph numbered in bold.

I'm wiring up the downloads next, naming each file from the symbol with slashes swapped for hyphens, and adding a copy-citation button that falls back to a textarea if the clipboard API isn't available. Then I'm moving to the paragraphs table on tab 02, where each row's number cell holds an expand button and the whole row toggles a detail row beneath it.

I'm setting up the expanded paragraph view so each suspect line is wrapped in a thin red box inside the running text, and I'm adding a toggle that shows the raw PDF lines with page-change markers. I'll let several rows stay open at once with a simple set, and add a collapsed headings list showing each heading's label and the paragraph it comes before.

I'm laying out the header with the title, the symbol link, the adoption date, the page count and the source, and putting a status dot beside it with the checks passed and the pages flagged. The main column gets the numbered tabs, and the layout stacks on narrow screens. For the footer I'm showing the source, the build date, or a dash when that's missing, and I'm treating the reference as absent unless it has a numeric paragraph count.

I'm laying out the summary tiles on tab 01: paragraphs found against the reference count, first words matching, and pages flagged, each with a short note on how it's computed. Below them I'll list up to ten mismatches and a "and n more" line for the rest, then add the closed headings for every check and the flagged pages.

I'm setting up the data layer next, reading the document from the workshop data and handling both array and object shapes. The records get sorted by page, and I'll split each page's text into lines.

I'm now setting up the page pipeline: for each record I split its text into lines and start tagging each one with its page.

I'm setting up the page pipeline now: for each record, I'm checking the first non-empty line for the symbol header and scanning up from the bottom to pick out footer lines, including the page number, GE codes and ISO-style trailing numbers.

I'm now writing the page pipeline: for each record I'll split its text into lines, check the first non-empty line for the symbol header, and peel footer lines off the bottom, treating page-number-only lines that don't match the page as displaced and noting them for the report.

I'm setting up the parse step now, with each paragraph built up line by line. I'll track the current section and part along the way.

I'm writing the paragraph-detection step: a numbered line like "12." or "12. text" opens a new paragraph, and I'm looping through the body lines, skipping blanks, and starting each paragraph with its number and the first line's text.

I'm turning to the paragraph parser: when a line is a numbered start, I'll split off the text after the number into its own line record that points back to the source line. The source line gets marked as a paragraph start with its number, and the new paragraph picks up the current section, part and path.

I'm adding the heading-detection branch: a Roman numeral or capital letter followed by a period marks a heading, and I'm collecting the title lines beneath it until I hit a paragraph start or another heading.

I'm adding the heading branch: a Roman numeral or capital letter followed by a period starts a heading, and I'll gather the title lines below it, stopping at a paragraph start or the next heading. Blank lines inside a title only count as continuing if the next line picks up in lowercase, and a heading with no title text still gets recorded.

I'm settling how each heading is stored: a Roman numeral marks a part and resets the subsection and unnumbered heading, while a letter marks a subsection under the current part. The section is then set to that heading's text.

I'm now handling the paragraph-ish lines that fall outside any numbered paragraph: if no paragraph is open, they're either cover text before the first paragraph or unclassified stray lines. When a paragraph is open, I'm checking whether the next non-blank line is a paragraph start, so I can decide whether the current line belongs to an unlabelled heading.

I'm working out the heading case now: a line that looks like a heading and sits right before a paragraph start on the same page gets pulled out of the paragraph, and if the line before it also looks like heading text, that one comes along too.

I'm checking whether a wrapped heading line that begins lowercase or with "(" should still be treated as the second line of a heading that sits right before a paragraph start, since the current rule requires a capital letter.

I'm making the unlabelled-heading check accept a second wrapped line that starts lowercase or with a parenthesis, as long as the line before it also passes the heading test on the same page. Lines that end in punctuation or run long are still ruled out, so a paragraph's final line can't be mistaken for a heading.

I'm checking the heading case here: when a paragraph's last line is followed directly by a paragraph start, I'd look back at the line before it, and if that also looks like heading text on the same page, I'd pull both out as a two-line heading and mark them accordingly, so a paragraph's own final line can't be mistaken for a heading.

I'm adding the paragraph-line branch: each remaining line gets pushed onto the open paragraph, tagged with its page and source. After a heading is recorded, the open paragraph is cleared so later stray lines don't attach to it, and each paragraph's path is built from its part, subsection and unnumbered heading.

I'm finalizing each paragraph: joining its lines into one text with whitespace tidied, and counting its words. Then I'm marking suspect lines, so a flagged line also covers the rest of its page until the page changes.

I'm checking how footnote and footer lines get trimmed from each paragraph, and I'm counting the words in each one. A paragraph is flagged when it has suspect lines or runs over 300 words, and I'm tracking which pages those suspect lines fall on.

I'm working out how to tally the footnote-trigger lines per page for each paragraph, and how many paragraphs are flagged for having suspect lines or running past 300 words. I'm also counting the hyphenated line breaks across the body and checking the classification totals.

I'm now deciding how to tally the classification: I'll count lines by kind across all line records, check that the paragraph-kind count matches the lines held in paragraphs, and look at the footer line for the GE job code.

Checking the page 1 footer lines next, along with whether a stray bare number near the bottom of a page is really a footnote marker. Then I'm counting how many distinct pages have suspect lines inside paragraphs.

I'm now writing the Markdown output: a front-matter block with the document's title, symbol, adoption date, source URL, extraction date, paragraph counts, and a note that footnotes weren't separated. After that, headings become section markers and each paragraph is rendered with its number in bold.

I'm now laying out the UI state and the rendering approach: a single render function that rebuilds the panels, with focus restored on whichever toggle the user just pressed. I'm also planning the tab keyboard handling and the compact CSS.

I'm writing the HTML shell now: a header with the document title, status and metadata, then a layout with a side rail and a tabbed main area, plus a footer.

I'm sketching the layout of the summary rail: a document card with the symbol and title, a paragraph count shown against the expected total with a bar that turns red when they don't match, and the number of flagged pages. Then I'll set up a 2x2 grid of tiles on the first tab, each built from a shared tile function that takes a label, a headline value, a note, a style class, and an explanation.

I'm now setting up the paragraph table: each row shows its number, section, page, first line and check status, with numbers right-aligned and rows filtered when a filter is active. Expanding a row adds a detail cell with the paragraph's path, and its text is rendered line by line, with suspect lines highlighted.

I'm now planning the paragraph table's row layout and its expandable detail: the paragraph's path, its text with suspect lines highlighted, the reference first words beside the found ones, and an optional view of the raw PDF lines with page markers.

I'm wrapping up the flagged-pages table: each row gets a click handler and expands to show the page's raw lines, with suspect lines marked and a link to the paragraph they sit in. Next I'll check the status of each validation check.

I'm writing the validation checks now, starting with the paragraph count against the expected total. Next I'm walking the paragraphs in order to check numbering for gaps and duplicates, recording any out-of-sequence paragraph and the page it's on.

I'm now writing the validation checks, moving through the paragraph count, numbering gaps, first-word mismatches, and suspect lines. Next I'm checking that every page has its header, whether page numbers appear in the footers of all pages but the first, and which displaced numbers were removed. Last come the notes on headings and hyphenated line breaks, along with the checks that nothing was lost and the export round-trips.

Total of twelve checks, and I'm tallying how many fail and how many pass or are notes, to feed the header status.

I'm writing the sanitizer for the first-words check: walking the tokens and dropping stray footnote numbers that follow a full stop, comma or closing quote, while still handling numbers glued onto the end of a word.

I'm writing a sanitizer for the first-words check, and I'm working out how to tell a stray footnote number from a real one. A number after a full stop, comma or closing quote gets dropped unless the word before it is an abbreviation, and numbers glued onto the end of a word need the same treatment.

I'm laying out the page's CSS and the JavaScript state: a current tab, which paragraphs are open, and which sections are expanded.

I'm writing the click handler for the tab view, which will react to clicks on any element carrying a data-act attribute.

I'm setting up the click handling so a click on a table row, or on the button inside it, opens that row, with focus returning to the button afterwards. Filter clicks will switch to the table tab and scroll it into view. I'm also adding keyboard handling for the tab list and the two download actions, and a copy button that changes its label to "Copied" without re-rendering.

I'm building the flagged-pages list next: for each paragraph I'm counting the suspect lines per page and noting which checks triggered them, so each row can show its page and reasons.

I'm filling in the flagged-pages list with a row for each page of each paragraph, counting its suspect lines and collecting the reasons, then sorting by page and paragraph.

I'm finishing the flagged-page details: each page shows its lines with the suspect ones highlighted, plus a pointer to the paragraph that sits there. I'm also deciding the footer text, then I'll write the final file.

